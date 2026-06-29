"""
Demo 3 — Quantization: STE, the noise proxy, and content-adaptive bin width.

Quantization is the only *lossy* step and it is not differentiable, so codecs
use two tricks the paper relies on:

  * STE (straight-through estimator): forward pass rounds; backward pass passes
    the gradient through unchanged, so the encoder can still be trained.
  * Additive U(-0.5, 0.5) noise: a differentiable stand-in for round(y) whose
    distribution matches the quantized one, used to estimate the *rate*.

PICO also learns a per-content **quantization width** q (ablation ~8.2% BD-rate
when removed). Instead of one global bin size it predicts how finely to quantize
each coefficient. This demo shows *why that helps*: not all coefficients carry
equal information. Quantizing high-variance (low-frequency) coefficients finely
and low-variance (high-frequency) ones coarsely — adaptive bit allocation —
gives a strictly better rate-distortion curve than a single uniform step,
especially at low bitrate (this is the "reverse water-filling" result).

We measure the variance of each 8x8 DCT frequency on a real image, then compare
two ways to spend a bit budget across those 64 coefficients:
  (A) uniform   — same number of bits for every frequency
  (B) optimal   — reverse water-filling: spend bits where variance is high,
                  drop near-zero-variance frequencies (content-adaptive width)
Optimal allocation is never worse and wins big at low bitrate.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np  # noqa: E402
import torch  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import common  # noqa: E402

N = 8


def ste_round(x: torch.Tensor) -> torch.Tensor:
    """round on the forward pass, identity gradient on the backward pass."""
    return x + (torch.round(x) - x).detach()


def demo_ste() -> str:
    torch.manual_seed(0)
    w = torch.tensor([0.2, -0.7, 1.4], requires_grad=True)
    target = torch.tensor([3.0, -1.0, 0.0])
    opt = torch.optim.SGD([w], lr=0.3)
    for _ in range(200):
        opt.zero_grad()
        loss = ((ste_round(w * 2.0) - target) ** 2).mean()
        loss.backward()                      # grad nonzero ONLY because of STE
        opt.step()
    return (f"  STE optimisation reached round(2w)={torch.round(w*2).tolist()} "
            f"(target {target.tolist()}) — gradients flowed through rounding.")


def dct_matrix(n: int) -> np.ndarray:
    k = np.arange(n)[:, None]
    x = np.arange(n)[None, :]
    D = np.cos(np.pi * (2 * x + 1) * k / (2 * n)) * np.sqrt(2.0 / n)
    D[0] *= 1.0 / np.sqrt(2.0)
    return D.astype(np.float32)


def block_dct(x, D):
    h, w = x.shape
    out = np.empty_like(x)
    for i in range(0, h, N):
        for j in range(0, w, N):
            out[i:i + N, j:j + N] = D @ x[i:i + N, j:j + N] @ D.T
    return out


def block_idct(c, D):
    h, w = c.shape
    out = np.empty_like(c)
    for i in range(0, h, N):
        for j in range(0, w, N):
            out[i:i + N, j:j + N] = D.T @ c[i:i + N, j:j + N] @ D
    return out


def alloc_optimal(sigma2: np.ndarray, rbar: float):
    """Reverse water-filling: choose theta so the average rate == rbar.
    Returns (per-band bits, total distortion D, theta)."""
    lo, hi = 1e-9, float(sigma2.max())
    for _ in range(100):                      # bisection on the water level theta
        theta = 0.5 * (lo + hi)
        bits = np.maximum(0.0, 0.5 * np.log2(sigma2 / theta))
        if bits.mean() > rbar:                # too many bits -> raise water level
            lo = theta
        else:
            hi = theta
    bits = np.maximum(0.0, 0.5 * np.log2(sigma2 / theta))
    # distortion: coded bands sit at theta, dropped bands keep full variance
    D = np.where(bits > 0, theta, sigma2).mean()
    return bits, D, theta


def main() -> None:
    common.banner("Demo 3: quantization — STE, noise proxy, adaptive bin width")
    print(demo_ste())

    # additive-noise proxy vs rounding
    torch.manual_seed(0)
    y = torch.randn(100_000) * 1.5
    rounded = torch.round(y)
    noised = y + (torch.rand_like(y) - 0.5)

    # image -> 8x8 DCT -> per-frequency variance (across all blocks)
    img = common.load_image(256, gray=True)
    print(f"  image source: {common.load_image.source}")
    x = (img * 255.0).astype(np.float32)
    D = dct_matrix(N)
    coeffs = block_dct(x - 128.0, D)
    h, w = coeffs.shape
    blocks = coeffs.reshape(h // N, N, w // N, N).transpose(0, 2, 1, 3).reshape(-1, N * N)
    sigma2 = blocks.var(axis=0) + 1e-6        # variance of each of the 64 frequencies

    rates = np.linspace(0.1, 4.0, 30)         # average bits / coefficient (=bits/pixel)
    mean_var = sigma2.mean()
    psnr_uni, psnr_opt = [], []
    for rbar in rates:
        D_uni = mean_var * 2.0 ** (-2.0 * rbar)            # uniform: same bits each band
        _, D_opt, _ = alloc_optimal(sigma2, rbar)          # optimal water-filling
        psnr_uni.append(10 * np.log10(255.0 ** 2 / D_uni))
        psnr_opt.append(10 * np.log10(255.0 ** 2 / D_opt))

    # bit map at a representative low rate, for the visual
    bits_map, _, _ = alloc_optimal(sigma2, 0.5)
    bits_map = bits_map.reshape(N, N)

    print("\n  optimal vs uniform bit allocation (PSNR at matched rate):")
    for i in range(0, len(rates), 5):
        rbar, pu, po = rates[i], psnr_uni[i], psnr_opt[i]
        print(f"   {rbar:4.2f} bpp : uniform {pu:5.2f} dB   |  optimal {po:5.2f} dB"
              f"   (+{po-pu:.2f} dB)")
    assert all(po >= pu - 1e-6 for po, pu in zip(psnr_opt, psnr_uni))

    # ---- figure -----------------------------------------------------------
    fig, ax = plt.subplots(1, 3, figsize=(13, 4.0))
    ax[0].hist(rounded.numpy(), bins=np.arange(-6, 7) - 0.5, density=True,
               alpha=0.6, label="round(y)", color="#2e86ab")
    ax[0].hist(noised.numpy(), bins=60, density=True, alpha=0.5,
               label="y + U(-.5,.5)", color="#e09f3e")
    ax[0].set_title("Noise proxy ≈ rounding\n(differentiable rate model)", fontsize=10)
    ax[0].legend(fontsize=8)
    ax[0].set_xlabel("value")

    im = ax[1].imshow(bits_map, cmap="viridis")
    ax[1].set_title("optimal bits per 8x8\nfrequency @ 0.5 bpp", fontsize=10)
    ax[1].set_xlabel("freq x"); ax[1].set_ylabel("freq y")
    fig.colorbar(im, ax=ax[1], fraction=0.046)

    ax[2].plot(rates, psnr_uni, "o-", ms=3, color="#d1495b", label="uniform bits/band")
    ax[2].plot(rates, psnr_opt, "s-", ms=3, color="#2e86ab", label="adaptive (optimal)")
    ax[2].set_xlabel("rate (bits / pixel)")
    ax[2].set_ylabel("PSNR (dB)")
    ax[2].set_title("Adaptive allocation wins\n(esp. at low bitrate)", fontsize=10)
    ax[2].grid(alpha=0.3); ax[2].legend(fontsize=8)
    fig.tight_layout()
    common.save_fig(fig, "demo3_quantization.png")
    print("\n  Takeaway: spending bits where they matter (content-adaptive bin")
    print("  width) lifts the whole RD curve — PICO ablation ~8% BD-rate.")


if __name__ == "__main__":
    main()
