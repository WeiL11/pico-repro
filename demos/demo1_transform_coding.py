"""
Demo 1 — Transform coding & the rate-distortion (RD) trade-off.

THE BIG PICTURE behind every image codec (JPEG, AV1, and learned codecs like
PICO): don't quantize pixels directly. First apply a *transform* that
concentrates energy into a few coefficients, THEN quantize. The same number of
bits then buys far less distortion.

This demo compares two ways of spending bits on the same image:
  (A) quantize pixels directly         (no transform)
  (B) quantize 8x8 block-DCT coeffs    (JPEG-style transform coding)

For several quantization step sizes we measure:
  rate      = zeroth-order entropy of the quantized symbols (bits/pixel)  -- an
              ideal-entropy-coder stand-in (no real bitstream is written)
  distortion= PSNR of the reconstruction

A learned codec replaces the fixed DCT with a *learned* non-linear transform
(an autoencoder), but the principle this demo shows is identical.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import common  # noqa: E402

N = 8  # DCT block size


def dct_matrix(n: int) -> np.ndarray:
    k = np.arange(n)[:, None]
    x = np.arange(n)[None, :]
    D = np.cos(np.pi * (2 * x + 1) * k / (2 * n)) * np.sqrt(2.0 / n)
    D[0] *= 1.0 / np.sqrt(2.0)
    return D.astype(np.float32)


def blockwise(img: np.ndarray, fn) -> np.ndarray:
    """Apply `fn` to every NxN block of a 2-D image."""
    h, w = img.shape
    out = np.empty_like(img)
    for i in range(0, h, N):
        for j in range(0, w, N):
            out[i:i + N, j:j + N] = fn(img[i:i + N, j:j + N])
    return out


def main() -> None:
    common.banner("Demo 1: transform coding & the rate-distortion trade-off")
    img = common.load_image(256, gray=True)          # HxW in [0,1]
    print(f"  image source: {common.load_image.source}")
    x = img * 255.0                                   # work in 0..255

    D = dct_matrix(N)
    fwd = lambda b: D @ b @ D.T                       # noqa: E731
    inv = lambda b: D.T @ b @ D                       # noqa: E731
    coeffs = blockwise(x - 128.0, fwd)               # DCT of every block

    steps = [2, 4, 8, 16, 32, 64, 96]
    rd_pixel, rd_dct = [], []
    for q in steps:
        # (A) quantize pixels directly
        qpix = np.round(x / q)
        rec_pix = np.clip(qpix * q, 0, 255)
        rd_pixel.append((common.entropy_bits_per_symbol(qpix),
                         common.psnr(x / 255, rec_pix / 255)))

        # (B) quantize DCT coefficients
        qc = np.round(coeffs / q)
        rec_dct = blockwise(qc * q, inv) + 128.0
        rec_dct = np.clip(rec_dct, 0, 255)
        rd_dct.append((common.entropy_bits_per_symbol(qc),
                       common.psnr(x / 255, rec_dct / 255)))

    # ---- figure -----------------------------------------------------------
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    rp, dp = zip(*rd_pixel)
    rc, dc = zip(*rd_dct)
    ax[0].plot(rp, dp, "o-", label="quantize pixels (no transform)", color="#d1495b")
    ax[0].plot(rc, dc, "s-", label="quantize 8x8 DCT (transform coding)", color="#2e86ab")
    ax[0].set_xlabel("rate  (bits / pixel, entropy)")
    ax[0].set_ylabel("distortion  (PSNR, dB) -- higher is better")
    ax[0].set_title("Same bits, far better quality with a transform")
    ax[0].grid(alpha=0.3)
    ax[0].legend(fontsize=8)

    # show a low-bit reconstruction of each, plus the original
    q = 48
    rec_pix = np.clip(np.round(x / q) * q, 0, 255)
    rec_dct = np.clip(blockwise(np.round(coeffs / q) * q, inv) + 128.0, 0, 255)
    panel = np.concatenate([x, rec_pix, rec_dct], axis=1) / 255.0
    ax[1].imshow(panel, cmap="gray", vmin=0, vmax=1)
    ax[1].set_title(f"original | pixel-quant | DCT-quant  (q={q})")
    ax[1].axis("off")
    fig.tight_layout()
    common.save_fig(fig, "demo1_transform_coding.png")

    # ---- console summary --------------------------------------------------
    print("\n  rate(bpp)  PSNR pixel | PSNR DCT   (matched step size)")
    for (rp_, dp_), (rc_, dc_), q in zip(rd_pixel, rd_dct, steps):
        print(f"   q={q:<3d}  pixel {dp_:5.2f}dB @ {rp_:.2f}bpp   "
              f"|  DCT {dc_:5.2f}dB @ {rc_:.2f}bpp")
    print("\n  Takeaway: at the same bitrate the transform wins by several dB.")
    print("  Learned codecs (PICO) replace the DCT with a *learned* transform.")


if __name__ == "__main__":
    main()
