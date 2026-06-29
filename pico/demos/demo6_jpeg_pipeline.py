"""
Demo 6 — How JPEG actually works, on real pixels.

JPEG is the hand-designed signal-processing pipeline we've used for ~30 years.
This demo runs its key steps on a real image so you can SEE each one, then shows
how it fails at low bitrate (the blocky artefacts) — the failure mode PICO avoids
by *regenerating* texture instead of *approximating* coefficients.

It produces three figures:
  assets/jpeg_pipeline.png    color split (YCbCr) + chroma subsampling
  assets/jpeg_block_dct.png   one 8x8 block: DCT -> quantization table -> rebuild
  assets/jpeg_quality.png     real JPEGs at several qualities, with zoomed crops

No special libraries — uses Pillow's real JPEG encoder for the quality sweep.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import common  # noqa: E402

N = 8

# The standard JPEG luminance quantization table (the "Q50" baseline). This
# single table is, essentially, JPEG's entire model of human vision.
JPEG_LUMA_Q = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]], dtype=np.float32)


def dct_matrix(n):
    k = np.arange(n)[:, None]
    x = np.arange(n)[None, :]
    D = np.cos(np.pi * (2 * x + 1) * k / (2 * n)) * np.sqrt(2.0 / n)
    D[0] *= 1.0 / np.sqrt(2.0)
    return D.astype(np.float32)


def rgb_to_ycbcr(rgb):
    m = np.array([[0.299, 0.587, 0.114],
                  [-0.168736, -0.331264, 0.5],
                  [0.5, -0.418688, -0.081312]], dtype=np.float32)
    ycc = rgb @ m.T
    ycc[..., 1:] += 0.5            # center chroma at 0.5 for display
    return ycc


# --------------------------------------------------------------------------- #
def fig_color(img):
    """YCbCr split + the effect of chroma subsampling (4:2:0)."""
    ycc = rgb_to_ycbcr(img)
    Y, Cb, Cr = ycc[..., 0], ycc[..., 1], ycc[..., 2]

    # simulate 4:2:0: downsample chroma by 2, then upsample back
    def sub420(c):
        small = c[::2, ::2]
        return np.repeat(np.repeat(small, 2, 0), 2, 1)[:c.shape[0], :c.shape[1]]
    ycc_sub = ycc.copy()
    ycc_sub[..., 1] = sub420(Cb)
    ycc_sub[..., 2] = sub420(Cr)

    # back to RGB for both full and subsampled chroma
    minv = np.array([[1.0, 0.0, 1.402],
                     [1.0, -0.344136, -0.714136],
                     [1.0, 1.772, 0.0]], dtype=np.float32)
    def to_rgb(y):
        t = y.copy(); t[..., 1:] -= 0.5
        return np.clip(t @ minv.T, 0, 1)
    rec_sub = to_rgb(ycc_sub)

    fig, ax = plt.subplots(1, 5, figsize=(15, 3.3))
    ax[0].imshow(img); ax[0].set_title("original RGB", fontsize=10)
    ax[1].imshow(Y, cmap="gray"); ax[1].set_title("Y (brightness)\neye is sensitive", fontsize=10)
    ax[2].imshow(Cb, cmap="gray"); ax[2].set_title("Cb (blue-diff)\neye is insensitive", fontsize=10)
    ax[3].imshow(Cr, cmap="gray"); ax[3].set_title("Cr (red-diff)\neye is insensitive", fontsize=10)
    psnr = common.psnr(img, rec_sub)
    ax[4].imshow(rec_sub); ax[4].set_title(f"chroma at 1/4 res (4:2:0)\n{psnr:.1f} dB — barely changes", fontsize=10)
    for a in ax:
        a.axis("off")
    fig.suptitle("Step 1-2: split brightness from colour, then throw away colour resolution",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    common.save_fig(fig, "jpeg_pipeline.png")


# --------------------------------------------------------------------------- #
def fig_block(img):
    """One 8x8 luminance block: pixels -> DCT -> quantize -> rebuild."""
    Y = (rgb_to_ycbcr(img)[..., 0] * 255.0).astype(np.float32)
    # pick a textured block (high local variance)
    best, pos = -1, (0, 0)
    for i in range(0, Y.shape[0] - N, N):
        for j in range(0, Y.shape[1] - N, N):
            v = Y[i:i + N, j:j + N].var()
            if v > best:
                best, pos = v, (i, j)
    i, j = pos
    block = Y[i:i + N, j:j + N]

    D = dct_matrix(N)
    coeff = D @ (block - 128.0) @ D.T            # DCT
    q = np.round(coeff / JPEG_LUMA_Q)            # quantize with the table
    deq = q * JPEG_LUMA_Q                         # de-quantize
    rec = (D.T @ deq @ D) + 128.0                 # inverse DCT
    nonzero = int((q != 0).sum())

    fig, ax = plt.subplots(1, 5, figsize=(15, 3.4))

    def heat(a, M, title, cmap, fmt="{:.0f}", vlog=False):
        show = np.log1p(np.abs(M)) if vlog else M
        a.imshow(show, cmap=cmap)
        for y in range(N):
            for x in range(N):
                a.text(x, y, fmt.format(M[y, x]), ha="center", va="center",
                       fontsize=6.5, color="#111")
        a.set_title(title, fontsize=10); a.set_xticks([]); a.set_yticks([])

    heat(ax[0], block, "8x8 block\n(pixel values)", "gray")
    heat(ax[1], coeff, "DCT coefficients\n(energy → top-left)", "coolwarm", "{:.0f}", vlog=True)
    heat(ax[2], JPEG_LUMA_Q, "JPEG quant table\n(coarser →)", "viridis")
    heat(ax[3], q, f"quantized\n({nonzero}/64 nonzero)", "coolwarm")
    ax[4].imshow(rec, cmap="gray")
    ax[4].set_title(f"rebuilt block\n{common.psnr(block/255, np.clip(rec,0,255)/255):.1f} dB",
                    fontsize=10); ax[4].axis("off")
    fig.suptitle("Step 3-5: inside one 8x8 block — the DCT compacts energy, "
                 "the table quantizes away high frequencies", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    common.save_fig(fig, "jpeg_block_dct.png")
    return nonzero


# --------------------------------------------------------------------------- #
def fig_quality(img):
    """Real JPEGs at several qualities (Pillow) with zoomed crops + bpp/PSNR."""
    from PIL import Image
    pil = Image.fromarray((img * 255).astype(np.uint8))
    H, W = img.shape[:2]
    qualities = [90, 25, 10, 5]
    ch, cw = H // 4, W // 4            # a zoom crop window
    cy, cx = H // 3, W // 3

    fig, ax = plt.subplots(2, len(qualities), figsize=(3.2 * len(qualities), 6.4))
    for k, qual in enumerate(qualities):
        buf = io.BytesIO()
        pil.save(buf, format="JPEG", quality=qual)
        nbytes = buf.tell()
        dec = np.asarray(Image.open(io.BytesIO(buf.getvalue())).convert("RGB"),
                         np.float32) / 255.0
        bpp = nbytes * 8 / (H * W)
        ps = common.psnr(img, dec)
        ax[0, k].imshow(dec); ax[0, k].axis("off")
        ax[0, k].set_title(f"JPEG q={qual}\n{bpp:.2f} bpp · {ps:.1f} dB", fontsize=10)
        crop = dec[cy:cy + ch, cx:cx + cw]
        ax[1, k].imshow(crop); ax[1, k].axis("off")
        ax[1, k].set_title("zoom (see 8x8 blocks)", fontsize=9)
    fig.suptitle("Step 6 & the failure mode: starve JPEG of bits and the 8x8 blocks appear",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    common.save_fig(fig, "jpeg_quality.png")


def main():
    common.banner("Demo 6: how JPEG works on real pixels (and how it fails)")
    img = common.load_image(256)
    print(f"  image source: {common.load_image.source}")
    fig_color(img)
    nz = fig_block(img)
    fig_quality(img)
    print(f"\n  One textured 8x8 block kept only {nz}/64 coefficients after the JPEG table.")
    print("  Low-quality JPEGs show the classic blocky artefacts — JPEG *approximates*")
    print("  the original coefficients. PICO instead *regenerates* a texture that looks")
    print("  right, learns every step, and optimises for perception (see demos 1-5).")


if __name__ == "__main__":
    main()
