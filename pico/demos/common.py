"""
common.py — shared helpers for the PICO concept demos.

Everything here is free / local. No network is required: if the Kodak image
cannot be downloaded we fall back to a deterministic synthetic image that still
contains edges, gradients and texture so the demos remain meaningful.

Paper: "What Matters in Practical Learned Image Compression" (Apple PICO),
arXiv:2605.05148.
"""
from __future__ import annotations

import math
import os
import urllib.request
from pathlib import Path

import numpy as np
import torch

# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent          # pico-repro/
ASSETS = ROOT / "assets"
DATA = ROOT / "data"
ASSETS.mkdir(exist_ok=True)
DATA.mkdir(exist_ok=True)


# ----------------------------------------------------------------------------
# Device
# ----------------------------------------------------------------------------
def get_device() -> torch.device:
    """Prefer Apple-MPS, then CUDA, else CPU. Demos are tiny so CPU is fine too."""
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


# ----------------------------------------------------------------------------
# Image loading
# ----------------------------------------------------------------------------
# A public Kodak test image (the classic "parrots"). Used everywhere in image
# compression papers. If offline we synthesise something with similar structure.
_KODAK_URL = "https://r0k.us/graphics/kodak/kodak/kodim23.png"
_KODAK_FILE = DATA / "kodim23.png"


def _synthetic_image(size: int = 256) -> np.ndarray:
    """Deterministic RGB image with gradients, edges, circles and texture."""
    rng = np.random.default_rng(0)
    y, x = np.mgrid[0:size, 0:size].astype(np.float32) / size
    r = 0.5 + 0.5 * np.sin(8 * math.pi * x)                       # vertical stripes
    g = y.copy()                                                  # smooth gradient
    b = ((x - 0.5) ** 2 + (y - 0.5) ** 2 < 0.08).astype(np.float32)  # a disk (edge)
    img = np.stack([r, g, b], axis=-1)
    # add a textured corner so high-frequency content exists
    tex = rng.random((size // 4, size // 4, 3)).astype(np.float32)
    img[: size // 4, : size // 4] = tex
    return np.clip(img, 0, 1)


def load_image(size: int = 256, gray: bool = False) -> np.ndarray:
    """
    Return an HxW(x3) float32 image in [0, 1], centre-cropped/resized to `size`.
    Tries the cached/Kodak image first, then a synthetic fallback.
    """
    from PIL import Image

    arr = None
    try:
        if not _KODAK_FILE.exists():
            urllib.request.urlretrieve(_KODAK_URL, _KODAK_FILE)  # may raise offline
        im = Image.open(_KODAK_FILE).convert("RGB")
        # centre crop to square then resize
        w, h = im.size
        s = min(w, h)
        im = im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))
        im = im.resize((size, size), Image.LANCZOS)
        arr = np.asarray(im, dtype=np.float32) / 255.0
        source = "Kodak kodim23"
    except Exception as e:  # noqa: BLE001 - any failure -> synthetic
        arr = _synthetic_image(size)
        source = f"synthetic (offline: {type(e).__name__})"

    if gray:
        arr = arr @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    load_image.source = source  # type: ignore[attr-defined]
    return arr


# ----------------------------------------------------------------------------
# Metrics
# ----------------------------------------------------------------------------
def psnr(a: np.ndarray, b: np.ndarray, data_range: float = 1.0) -> float:
    mse = float(np.mean((a.astype(np.float64) - b.astype(np.float64)) ** 2))
    if mse <= 1e-12:
        return 99.0
    return 10.0 * math.log10(data_range ** 2 / mse)


def entropy_bits_per_symbol(symbols: np.ndarray) -> float:
    """Shannon (zeroth-order) entropy in bits/symbol of an integer array.

    This is the information-theoretic lower bound an ideal entropy coder would
    reach; we use it as a stand-in for the real bit-rate (no range coder)."""
    flat = symbols.astype(np.int64).ravel()
    if flat.size == 0:
        return 0.0
    _, counts = np.unique(flat, return_counts=True)
    p = counts / counts.sum()
    return float(-(p * np.log2(p)).sum())


def gaussian_bits(values: np.ndarray, mu: np.ndarray, sigma: np.ndarray,
                  bin_width: float = 1.0) -> float:
    """Estimated bits to encode `values` quantized to `bin_width`, under a
    Gaussian(mu, sigma) model. This is exactly how learned codecs estimate rate:
    bits = -log2( P(bin) ) where P(bin) = CDF(v+w/2) - CDF(v-w/2)."""
    sigma = np.maximum(sigma, 1e-6)
    def cdf(x):
        return 0.5 * (1.0 + erf_np((x - mu) / (sigma * math.sqrt(2.0))))
    upper = cdf(values + bin_width / 2)
    lower = cdf(values - bin_width / 2)
    p = np.clip(upper - lower, 1e-12, 1.0)
    return float(-np.log2(p).sum())


def erf_np(x: np.ndarray) -> np.ndarray:
    """Vectorised erf without scipy (Abramowitz & Stegun 7.1.26)."""
    sign = np.sign(x)
    x = np.abs(x)
    t = 1.0 / (1.0 + 0.3275911 * x)
    y = 1.0 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
                - 0.284496736) * t + 0.254829592) * t * np.exp(-x * x)
    return sign * y


# ----------------------------------------------------------------------------
# Plotting
# ----------------------------------------------------------------------------
def save_fig(fig, name: str) -> Path:
    """Save a matplotlib figure into assets/ and return the path."""
    out = ASSETS / name
    fig.savefig(out, dpi=110, bbox_inches="tight", facecolor="white")
    import matplotlib.pyplot as plt
    plt.close(fig)
    print(f"  saved -> assets/{name}")
    return out


def banner(title: str) -> None:
    line = "=" * 70
    print(f"\n{line}\n{title}\n{line}")
