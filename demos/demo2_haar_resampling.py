"""
Demo 2 — Haar-wavelet resampling vs strided convolution.

PICO's single biggest architectural lever (ablation: ~19.5% BD-rate increase
when removed) is using **2D Haar wavelets for every up/down-sampling step**
instead of the usual stride-2 convolution / transpose-convolution.

Why it matters:
  * A stride-2 conv that shrinks H,W by 2 typically THROWS AWAY information
    (it is not invertible) and aliases high-frequency detail.
  * The 2D Haar transform turns one HxWxC block into (H/2)x(W/2)x(4C): it keeps
    ALL the information (perfect reconstruction) and cleanly separates low- vs
    high-frequency sub-bands. The network resamples losslessly and decides what
    to spend bits on, instead of the resampler silently destroying detail.

This demo:
  1. shows the four Haar sub-bands (LL, LH, HL, HH),
  2. round-trips an image down-then-up with Haar  -> perfect reconstruction,
  3. round-trips with a fixed stride-2 (avg-pool) + bilinear-up baseline,
  4. compares reconstruction PSNR and error maps.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np  # noqa: E402
import torch  # noqa: E402
import torch.nn.functional as F  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import common  # noqa: E402

# Orthonormal Haar filters
_H = 1.0 / np.sqrt(2.0)


def haar_analysis(x: torch.Tensor) -> torch.Tensor:
    """HxW (1,C,H,W) -> (1,4C,H/2,W/2): [LL, LH, HL, HH] stacked on channels."""
    a = x[..., 0::2, 0::2]
    b = x[..., 0::2, 1::2]
    c = x[..., 1::2, 0::2]
    d = x[..., 1::2, 1::2]
    LL = (a + b + c + d) * 0.5      # 0.5 = (1/sqrt2)^2 -> orthonormal 2D
    LH = (a - b + c - d) * 0.5
    HL = (a + b - c - d) * 0.5
    HH = (a - b - c + d) * 0.5
    return torch.cat([LL, LH, HL, HH], dim=1)


def haar_synthesis(y: torch.Tensor) -> torch.Tensor:
    """Inverse of haar_analysis (perfect reconstruction)."""
    C = y.shape[1] // 4
    LL, LH, HL, HH = y[:, 0:C], y[:, C:2 * C], y[:, 2 * C:3 * C], y[:, 3 * C:4 * C]
    a = (LL + LH + HL + HH) * 0.5
    b = (LL - LH + HL - HH) * 0.5
    c = (LL + LH - HL - HH) * 0.5
    d = (LL - LH - HL + HH) * 0.5
    n, ch, h, w = a.shape
    out = torch.zeros(n, ch, h * 2, w * 2, dtype=a.dtype)
    out[..., 0::2, 0::2] = a
    out[..., 0::2, 1::2] = b
    out[..., 1::2, 0::2] = c
    out[..., 1::2, 1::2] = d
    return out


def main() -> None:
    common.banner("Demo 2: Haar-wavelet resampling vs strided conv")
    img = common.load_image(256)                         # HxWx3
    print(f"  image source: {common.load_image.source}")
    x = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).float()  # 1,3,H,W

    # 1+2) Haar down then up -> should be exact
    y = haar_analysis(x)
    x_haar = haar_synthesis(y)
    psnr_haar = common.psnr(x.numpy(), x_haar.numpy())

    # 3) baseline: stride-2 downsample (avg pool) then bilinear upsample
    down = F.avg_pool2d(x, 2)
    x_stride = F.interpolate(down, scale_factor=2, mode="bilinear", align_corners=False)
    psnr_stride = common.psnr(x.numpy(), x_stride.numpy())

    print(f"  Haar  down->up reconstruction PSNR : {psnr_haar:6.2f} dB  (lossless)")
    print(f"  Stride-2 down->up reconstruction   : {psnr_stride:6.2f} dB  (info lost)")

    # ---- figure -----------------------------------------------------------
    fig = plt.figure(figsize=(12, 6.5))

    # sub-bands of the luma channel
    yl = haar_analysis(x.mean(1, keepdim=True))[0]       # 4,H/2,W/2
    names = ["LL (low freq)", "LH", "HL", "HH (high freq)"]
    for i in range(4):
        ax = fig.add_subplot(2, 4, i + 1)
        band = yl[i].numpy()
        vlim = 1.0 if i == 0 else 0.3
        ax.imshow(band, cmap="gray", vmin=0 if i == 0 else -vlim, vmax=vlim)
        ax.set_title(f"Haar {names[i]}", fontsize=9)
        ax.axis("off")

    def show(ax, t, title):
        ax.imshow(np.clip(t[0].permute(1, 2, 0).numpy(), 0, 1))
        ax.set_title(title, fontsize=9)
        ax.axis("off")

    show(fig.add_subplot(2, 4, 5), x, "original")
    show(fig.add_subplot(2, 4, 6), x_haar, f"Haar round-trip\n{psnr_haar:.1f} dB")
    show(fig.add_subplot(2, 4, 7), x_stride, f"stride-2 round-trip\n{psnr_stride:.1f} dB")
    err = (x - x_stride).abs() * 4
    ax = fig.add_subplot(2, 4, 8)
    ax.imshow(np.clip(err[0].permute(1, 2, 0).numpy(), 0, 1))
    ax.set_title("stride-2 error (x4)\n(detail destroyed)", fontsize=9)
    ax.axis("off")

    fig.suptitle("Haar resampling is invertible & alias-free; strided conv loses information",
                 fontsize=12)
    fig.tight_layout()
    common.save_fig(fig, "demo2_haar_resampling.png")
    print("\n  Takeaway: invertible Haar resampling lets the network keep every")
    print("  detail and choose what to spend bits on -- PICO's #1 design lever.")


if __name__ == "__main__":
    main()
