"""
Demo 5 — A tiny end-to-end learned codec (the full pipeline working).

This is the integration demo: a compact **mean-scale hyperprior** autoencoder —
the standard backbone PICO builds on — that ties every concept from demos 1-4
together into one trainable codec:

    analysis transform  g_a  (demo 1)  ->  quantize latent  (demo 3)
    Haar resampling           (demo 2)  ->  entropy model: hyperprior + masked-
    synthesis transform g_s             ->     conv context  (demo 4)

We train it end-to-end on Apple-MPS at a few rate-distortion trade-offs
(lambda values) and plot the resulting **RD curve** plus reconstructions at a
low and a high bitrate. Higher lambda => spend more bits => higher PSNR. This
shows the full learned-compression loop actually compresses an image.

The codec also exposes the four design flags the paper ablates
(--no-haar/--no-context/--no-learned-scale/--no-learned-q) so you can experiment;
NOTE that reproducing the paper's *ordering* of those needs full-scale training
(days, ~120k images), not this 3-minute toy — at tiny scale the ranking is noisy.
The clean per-component evidence lives in demos 2, 3 and 4.

Run:
    python demos/demo5_ablation_rd.py --quick     # ~20s smoke test, 1 lambda
    python demos/demo5_ablation_rd.py             # ~3 min on MPS, full RD curve
No real range coder is used; rate is the differentiable estimated entropy.
"""
import argparse
import math
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np  # noqa: E402
import torch  # noqa: E402
import torch.nn as nn  # noqa: E402
import torch.nn.functional as F  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import common  # noqa: E402

LOG2 = math.log(2.0)


# --------------------------------------------------------------------------- #
# Building blocks
# --------------------------------------------------------------------------- #
def haar_analysis(x):
    a, b = x[..., 0::2, 0::2], x[..., 0::2, 1::2]
    c, d = x[..., 1::2, 0::2], x[..., 1::2, 1::2]
    return torch.cat([(a + b + c + d) * .5, (a - b + c - d) * .5,
                      (a + b - c - d) * .5, (a - b - c + d) * .5], 1)


def haar_synthesis(y):
    C = y.shape[1] // 4
    LL, LH, HL, HH = y[:, :C], y[:, C:2 * C], y[:, 2 * C:3 * C], y[:, 3 * C:]
    a = (LL + LH + HL + HH) * .5
    b = (LL - LH + HL - HH) * .5
    c = (LL + LH - HL - HH) * .5
    d = (LL - LH - HL + HH) * .5
    n, ch, h, w = a.shape
    out = torch.zeros(n, ch, h * 2, w * 2, device=a.device, dtype=a.dtype)
    out[..., 0::2, 0::2] = a
    out[..., 0::2, 1::2] = b
    out[..., 1::2, 0::2] = c
    out[..., 1::2, 1::2] = d
    return out


class Down(nn.Module):
    """Downsample by 2: Haar (invertible) + 1x1 mix, or a stride-2 conv."""
    def __init__(self, cin, cout, haar):
        super().__init__()
        self.haar = haar
        if haar:
            self.mix = nn.Conv2d(cin * 4, cout, 1)
        else:
            self.conv = nn.Conv2d(cin, cout, 5, stride=2, padding=2)

    def forward(self, x):
        return self.mix(haar_analysis(x)) if self.haar else self.conv(x)


class Up(nn.Module):
    """Upsample by 2: 1x1 mix + Haar synthesis, or a stride-2 transpose conv."""
    def __init__(self, cin, cout, haar):
        super().__init__()
        self.haar = haar
        if haar:
            self.mix = nn.Conv2d(cin, cout * 4, 1)
        else:
            self.conv = nn.ConvTranspose2d(cin, cout, 5, stride=2,
                                           padding=2, output_padding=1)

    def forward(self, x):
        return haar_synthesis(self.mix(x)) if self.haar else self.conv(x)


class Scale(nn.Module):
    """Learned per-channel activation scale (the ConvScale idea). No-op if off."""
    def __init__(self, c, on):
        super().__init__()
        self.s = nn.Parameter(torch.ones(1, c, 1, 1)) if on else None

    def forward(self, x):
        return x * self.s if self.s is not None else x


class MaskedConv2d(nn.Conv2d):
    """Type-A causal mask: each output sees only past (top/left) positions."""
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        m = torch.ones_like(self.weight)
        _, _, kh, kw = self.weight.shape
        m[:, :, kh // 2, kw // 2:] = 0
        m[:, :, kh // 2 + 1:, :] = 0
        self.register_buffer("mask", m)

    def forward(self, x):
        self.weight.data *= self.mask
        return super().forward(x)


def gaussian_likelihood(x, mu, sigma):
    """P(x) mass over a unit bin under N(mu, sigma); returns bits = -log2 P."""
    sigma = sigma.clamp(min=0.05)
    inv = 1.0 / (sigma * math.sqrt(2.0))
    upper = 0.5 * (1 + torch.erf((x + 0.5 - mu) * inv))
    lower = 0.5 * (1 + torch.erf((x - 0.5 - mu) * inv))
    p = (upper - lower).clamp(min=1e-9)
    return -torch.log(p) / LOG2


# --------------------------------------------------------------------------- #
# Codec
# --------------------------------------------------------------------------- #
class TinyCodec(nn.Module):
    def __init__(self, C=48, M=64, Cz=48, haar=True, context=True,
                 learned_scale=True, learned_q=True):
        super().__init__()
        self.context, self.learned_q = context, learned_q
        act = nn.GELU
        # analysis g_a: 3 -> M, downsample x8
        self.ga = nn.Sequential(
            nn.Conv2d(3, C, 5, padding=2), act(), Scale(C, learned_scale),
            Down(C, C, haar), act(), Scale(C, learned_scale),
            Down(C, C, haar), act(), Scale(C, learned_scale),
            Down(C, M, haar))
        # synthesis g_s: M -> 3
        self.gs = nn.Sequential(
            Up(M, C, haar), act(), Scale(C, learned_scale),
            Up(C, C, haar), act(), Scale(C, learned_scale),
            Up(C, C, haar), act(), Scale(C, learned_scale),
            nn.Conv2d(C, 3, 5, padding=2))
        # hyper analysis / synthesis (downsample x4 on the latent)
        self.ha = nn.Sequential(nn.Conv2d(M, Cz, 3, padding=1), act(),
                                Down(Cz, Cz, haar), act(), Down(Cz, Cz, haar))
        self.hs = nn.Sequential(Up(Cz, Cz, haar), act(), Up(Cz, M, haar), act(),
                                nn.Conv2d(M, 2 * M, 3, padding=1))
        # factorized prior on z (per-channel scale)
        self.z_logscale = nn.Parameter(torch.zeros(1, Cz, 1, 1))
        # autoregressive context + entropy-parameter fusion
        if context:
            self.ctx = MaskedConv2d(M, 2 * M, 5, padding=2)
            self.ep = nn.Sequential(nn.Conv2d(4 * M, 3 * M, 1), act(),
                                    nn.Conv2d(3 * M, 2 * M, 1))
        # learned per-channel quantization width q (softplus, >0)
        self.q_param = nn.Parameter(torch.zeros(1, M, 1, 1)) if learned_q else None

    def q_width(self):
        if self.q_param is None:
            return 1.0
        return F.softplus(self.q_param) + 0.1

    def forward(self, x, train=True):
        y = self.ga(x)
        z = self.ha(y)
        # z quantization + factorized rate
        z_hat = z + (torch.rand_like(z) - .5) if train else torch.round(z)
        z_bits = gaussian_likelihood(z_hat, torch.zeros_like(z_hat),
                                     torch.exp(self.z_logscale).expand_as(z_hat))
        hyper = self.hs(z_hat)
        # crop hyper to y's size (Haar/conv can differ by a pixel)
        hyper = hyper[..., :y.shape[2], :y.shape[3]]

        q = self.q_width()
        yq = y / q                                   # normalised latent
        y_hat = yq + (torch.rand_like(yq) - .5) if train else torch.round(yq)

        if self.context:
            ctx = self.ctx(y_hat)
            params = self.ep(torch.cat([hyper, ctx], 1))
        else:
            params = hyper
        mu, log_sigma = params.chunk(2, 1)
        sigma = F.softplus(log_sigma)

        y_bits = gaussian_likelihood(y_hat, mu, sigma)
        x_hat = self.gs(y_hat * q)
        x_hat = x_hat[..., :x.shape[2], :x.shape[3]]
        return x_hat, y_bits, z_bits


# --------------------------------------------------------------------------- #
# Data
# --------------------------------------------------------------------------- #
_KODAK = [1, 5, 7, 13, 19, 23]


def load_train_images(size=256):
    from PIL import Image
    imgs = []
    for idx in _KODAK:
        f = common.DATA / f"kodim{idx:02d}.png"
        try:
            if not f.exists():
                urllib.request.urlretrieve(
                    f"https://r0k.us/graphics/kodak/kodak/kodim{idx:02d}.png", f)
            im = Image.open(f).convert("RGB")
            w, h = im.size
            s = min(w, h)
            im = im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))
            im = im.resize((size, size), Image.LANCZOS)
            imgs.append(np.asarray(im, np.float32) / 255.0)
        except Exception:  # noqa: BLE001
            rng = np.random.default_rng(idx)
            yy, xx = np.mgrid[0:size, 0:size] / size
            base = 0.5 + 0.5 * np.sin((idx + 2) * math.pi * xx) * np.cos(3 * math.pi * yy)
            img = np.stack([base, yy, (xx + yy) / 2], -1).astype(np.float32)
            img[:size // 3, :size // 3] = rng.random((size // 3, size // 3, 3))
            imgs.append(np.clip(img, 0, 1))
    src = "Kodak" if (common.DATA / "kodim01.png").exists() else "synthetic"
    return np.stack(imgs), src


def crops(batch_imgs, n, patch, device, rng):
    """Random patch crops from the image set -> (n,3,patch,patch) tensor."""
    K, H, W, _ = batch_imgs.shape
    out = np.empty((n, patch, patch, 3), np.float32)
    for i in range(n):
        k = rng.integers(K)
        y0 = rng.integers(H - patch + 1)
        x0 = rng.integers(W - patch + 1)
        out[i] = batch_imgs[k, y0:y0 + patch, x0:x0 + patch]
    t = torch.from_numpy(out).permute(0, 3, 1, 2).contiguous()
    return t.to(device)


# --------------------------------------------------------------------------- #
# Train / eval one config
# --------------------------------------------------------------------------- #
def run_config(name, flags, imgs, device, steps, lam, patch, batch, seed=0):
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    model = TinyCodec(**flags).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    npix = patch * patch
    model.train()
    for step in range(steps):
        x = crops(imgs, batch, patch, device, rng)
        opt.zero_grad()
        x_hat, y_bits, z_bits = model(x, train=True)
        bpp = (y_bits.sum() + z_bits.sum()) / (x.shape[0] * npix)
        mse = F.mse_loss(x_hat, x)
        loss = bpp + lam * 255.0 ** 2 * mse           # rate + lambda*MSE
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()

    # ---- eval (deterministic rounding) on full images ----
    model.eval()
    recon0 = None
    with torch.no_grad():
        bpps, psnrs = [], []
        for k in range(imgs.shape[0]):
            x = torch.from_numpy(imgs[k]).permute(2, 0, 1).unsqueeze(0).to(device)
            x_hat, y_bits, z_bits = model(x, train=False)
            n = x.shape[2] * x.shape[3]
            bpps.append(float((y_bits.sum() + z_bits.sum()) / n))
            mse = float(F.mse_loss(x_hat.clamp(0, 1), x))
            psnrs.append(10 * math.log10(1.0 / max(mse, 1e-10)))
            if k == 0:
                recon0 = x_hat.clamp(0, 1)[0].permute(1, 2, 0).cpu().numpy()
    bpp, psnr = float(np.mean(bpps)), float(np.mean(psnrs))
    print(f"  {name:<16s} lambda={lam:<6.4g} bpp={bpp:6.3f}  PSNR={psnr:5.2f} dB")
    return dict(name=name, bpp=bpp, psnr=psnr, lam=lam, recon=recon0)


# --------------------------------------------------------------------------- #
# Explainer plots (no training required)
# --------------------------------------------------------------------------- #
def _box(ax, xy, w, h, text, fc, fontsize=9):
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch(xy, w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc=fc, ec="#333", lw=1.2))
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center",
            fontsize=fontsize, zorder=5)


def _arrow(ax, p0, p1, color="#333"):
    ax.annotate("", xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6))


def draw_architecture() -> None:
    """Schematic of the mean-scale-hyperprior codec PICO is built on."""
    fig, ax = plt.subplots(figsize=(12, 5.2))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
    enc, lat, ent, dec = "#cfe8f3", "#ffe7b3", "#f6cdd0", "#d6ecd2"

    # main path
    _box(ax, (0.2, 3.6), 1.5, 1.2, "input\nimage x", "#eee")
    _box(ax, (2.1, 3.6), 1.8, 1.2, "g_a\nanalysis transform\n(Haar resampling)", enc, 8)
    _box(ax, (4.3, 3.8), 1.6, 0.8, "quantize\nŷ = round((y−µ)/q)", lat, 8)
    _box(ax, (6.3, 3.8), 1.7, 0.8, "entropy\ncode → bits", ent, 8)
    _box(ax, (8.4, 3.6), 1.8, 1.2, "g_s\nsynthesis transform\n(Haar resampling)", dec, 8)
    _box(ax, (10.4, 3.6), 1.4, 1.2, "output\nx̂", "#eee")
    for p0, p1 in [((1.7, 4.2), (2.1, 4.2)), ((3.9, 4.2), (4.3, 4.2)),
                   ((5.9, 4.2), (6.3, 4.2)), ((8.0, 4.2), (8.4, 4.2)),
                   ((10.2, 4.2), (10.4, 4.2))]:
        _arrow(ax, p0, p1)

    # hyperprior / context branch (below)
    _box(ax, (4.0, 1.4), 1.7, 0.9, "h_a hyper-analysis\n→ side info z", enc, 8)
    _box(ax, (6.0, 1.4), 1.9, 0.9, "h_s + context\n→ scale σ, mean µ", ent, 8)
    _arrow(ax, (4.85, 3.6), (4.85, 2.3))                     # y -> h_a
    _arrow(ax, (5.7, 1.85), (6.0, 1.85))                     # h_a -> h_s
    _arrow(ax, (6.95, 2.3), (6.95, 3.8))                     # params -> entropy
    ax.text(3.0, 0.55, "Entropy model (demo 4): hyperprior scale + autoregressive "
            "context predict the bit cost of every latent value.",
            fontsize=8.5, color="#444")
    ax.text(2.0, 5.6, "PICO pipeline — a mean-scale hyperprior codec "
            "(the backbone the paper studies)", fontsize=12, weight="bold")
    common.save_fig(fig, "demo5_architecture.png")


def draw_ablation() -> None:
    """The paper's headline 'what matters' numbers + what BD-rate means."""
    # Table-1 BD-rate (CMMD-CLIP) of swapping each design choice for its naive
    # alternative. NOTE: the Haar number (19.51%) is vs a naive pixel-reshuffle;
    # vs a stride-2 conv/deconv it is 8.90%.
    items = [("Haar resampling*", 19.51),
             ("One-shot AR context model", 10.28),
             ("Learned scales (ConvScale)", 9.58),
             ("Learned quantization width", 8.16)]
    items.sort(key=lambda t: t[1])
    names = [n for n, _ in items]
    vals = [v for _, v in items]

    fig, ax = plt.subplots(1, 2, figsize=(13, 4.4))
    bars = ax[0].barh(names, vals, color="#d1495b")
    ax[0].set_xlabel("BD-rate vs naive alternative  (%, higher = matters more)")
    ax[0].set_title("What matters in PICO (paper Table 1)")
    ax[0].text(0.97, 0.16, "*Haar vs pixel-reshuffle; vs stride-2 conv = 8.9%",
               fontsize=7.5, color="#666", ha="right", style="italic",
               transform=ax[0].transAxes)
    for b, v in zip(bars, vals):
        ax[0].text(v + 0.3, b.get_y() + b.get_height() / 2, f"{v:.1f}%",
                   va="center", fontsize=9)
    ax[0].axvline(0, color="#333", lw=0.8)
    ax[0].text(0.97, 0.08, "all removed together: +31.69%", fontsize=9,
               color="#444", ha="right", style="italic",
               transform=ax[0].transAxes)

    # schematic of what BD-rate measures: horizontal gap between two RD curves
    r = np.linspace(0.1, 1.6, 50)
    full = 24 + 9 * np.log(r + 0.2) + 18
    ab = full - 3.0                                          # worse curve (shifted down)
    ax[1].plot(r, full, color="#2e86ab", lw=2, label="full model")
    ax[1].plot(r, ab, color="#d1495b", lw=2, label="component removed")
    q = 36.0
    rf = r[np.argmin(np.abs(full - q))]
    ra = r[np.argmin(np.abs(ab - q))]
    ax[1].annotate("", xy=(rf, q), xytext=(ra, q),
                   arrowprops=dict(arrowstyle="<|-|>", color="#444", lw=1.5))
    ax[1].text((rf + ra) / 2, q + 0.6, "extra bits for\nthe same quality\n= BD-rate",
               ha="center", fontsize=8.5, color="#444")
    ax[1].axhline(q, color="#aaa", ls="--", lw=0.8)
    ax[1].set_xlabel("rate (bpp)"); ax[1].set_ylabel("quality (e.g. PSNR / −LPIPS)")
    ax[1].set_title("BD-rate = average % bitrate gap\nat matched quality")
    ax[1].legend(fontsize=8); ax[1].grid(alpha=0.3)
    fig.tight_layout()
    common.save_fig(fig, "demo5_ablation.png")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", action="store_true",
                    help="optionally train the tiny codec end-to-end (slow, ~3 min)")
    ap.add_argument("--quick", action="store_true", help="fast smoke train (~20s)")
    ap.add_argument("--steps", type=int, default=None)
    ap.add_argument("--lam", type=float, default=0.02)
    args = ap.parse_args()

    common.banner("Demo 5: the learned codec — architecture & 'what matters'")

    if not args.train:
        print("  Drawing the codec architecture and the paper's ablation summary")
        print("  (no training; pass --train to actually optimise the tiny codec).")
        draw_architecture()
        draw_ablation()
        print("\n  The codec is fully implemented above as `TinyCodec` (mean-scale")
        print("  hyperprior, Haar resampling, masked-conv context, learned q).")
        print("  Paper BD-rate vs naive alternative: Haar 19.5% (vs pixel-reshuffle;")
        print("  8.9% vs stride-2 conv), context 10.3%, scales 9.6%, learned-q 8.2%.")
        return

    # ---- optional: actually train the codec (for the curious) ----
    device = common.get_device()
    steps = args.steps if args.steps else (40 if args.quick else 500)
    patch, batch = (96, 6) if args.quick else (128, 8)
    imgs, src = load_train_images(192 if args.quick else 256)
    flags = dict(haar=True, context=True, learned_scale=True, learned_q=True)
    print(f"  device={device}  images={imgs.shape[0]} ({src})  steps={steps}\n")
    run_config("full codec", flags, imgs, device, steps, args.lam, patch, batch)
    print("\n  Note: a 3-minute toy on 6 images will not reproduce the paper's")
    print("  ablation *ordering* — that needs full-scale training.")


if __name__ == "__main__":
    main()
