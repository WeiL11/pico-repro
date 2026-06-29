"""
Demo 4 — Entropy modelling: hyperprior & autoregressive context.

After the transform and quantization, the codec must turn the integer latent
into bits. The number of bits is set by the *probability model*: bits = -log2 P.
A better model of the same latent => fewer bits (a lossless win).

PICO (like all modern learned codecs) builds the model in stages, each measured
here on a synthetic latent that is (i) heteroscedastic — its local scale varies
across space — and (ii) spatially correlated:

  (A) factorized, single global Gaussian   — one sigma for everything
  (B) hyperprior: per-element scale sigma   — a side channel says "how uncertain
      transmitted as side info               is each region" (PICO's scale decoder)
  (C) + autoregressive context: predict     — PICO's one-shot AR context model
      each value's mean mu from already-       (ablation ~10.3% BD-rate)
      decoded neighbours, code the residual

Each stage lowers the estimated bitrate. No real range coder is used; we report
the information-theoretic bits -log2 P that an ideal coder would achieve.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import common  # noqa: E402


def smooth(a: np.ndarray, passes: int = 3) -> np.ndarray:
    k = np.array([0.25, 0.5, 0.25])
    for _ in range(passes):
        a = np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 0, a)
        a = np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 1, a)
    return a


def make_latent(n: int = 128, seed: int = 0):
    """Return (quantized latent, true local scale 'amp').

    The latent = correlated_unit_noise * amp.  'amp' is a smooth amplitude map
    (the hyperprior's job is to transmit it); the correlation is what the
    autoregressive context can additionally exploit."""
    rng = np.random.default_rng(seed)
    # smooth amplitude map: calm (small scale) top-left -> busy (large) bottom-right
    yy, xx = np.mgrid[0:n, 0:n] / n
    amp = 0.6 + 4.0 * (0.5 * xx + 0.5 * yy)                  # 0.6 .. 4.6
    # spatially correlated, unit-variance field
    corr = smooth(rng.standard_normal((n, n)), passes=3)
    corr /= corr.std()
    latent = np.round(corr * amp)
    return latent, amp


def neighbour_predict(latent: np.ndarray) -> np.ndarray:
    """Causal AR predictor: mu = mean of the left & top decoded neighbours."""
    left = np.zeros_like(latent, dtype=np.float64)
    left[:, 1:] = latent[:, :-1]
    top = np.zeros_like(latent, dtype=np.float64)
    top[1:, :] = latent[:-1, :]
    return 0.5 * (left + top)


def window_std(a: np.ndarray, win: int = 8) -> np.ndarray:
    n = a.shape[0]
    s = np.zeros_like(a, dtype=np.float64)
    for i in range(0, n, win):
        for j in range(0, n, win):
            s[i:i + win, j:j + win] = a[i:i + win, j:j + win].std()
    return np.clip(s, 0.5, None)


def main() -> None:
    common.banner("Demo 4: entropy modelling — factorized -> hyperprior -> context")
    lat, amp = make_latent()
    npix = lat.size
    zeros = np.zeros_like(lat, dtype=np.float64)

    # (A) factorized: one global Gaussian
    bitsA = common.gaussian_bits(lat, np.full_like(lat, lat.mean(), dtype=np.float64),
                                 np.full_like(lat, lat.std(), dtype=np.float64))
    # (B) hyperprior: per-element scale (transmitted side info = true amp)
    bitsB = common.gaussian_bits(lat, zeros, np.clip(amp, 0.5, None))
    # (C) + context: predict mean from neighbours, scale on the residual
    muC = neighbour_predict(lat)
    sgC = window_std(lat - muC)
    bitsC = common.gaussian_bits(lat, muC, sgC)

    for name, b in [("A factorized (global Gaussian) ", bitsA),
                    ("B hyperprior (per-elem scale)  ", bitsB),
                    ("C + autoregressive context     ", bitsC)]:
        print(f"  {name}: {b/npix:5.3f} bits/symbol   ({b/1e3:6.1f} kbits total)")
    assert bitsA > bitsB > bitsC, "expected A > B > C bits"
    print(f"  hyperprior saves {100*(bitsA-bitsB)/bitsA:4.1f}% vs factorized;")
    print(f"  context saves a further {100*(bitsB-bitsC)/bitsB:4.1f}% on top.")

    # ---- figure -----------------------------------------------------------
    fig, ax = plt.subplots(1, 4, figsize=(15, 3.9))
    ax[0].imshow(lat, cmap="coolwarm")
    ax[0].set_title("quantized latent\n(calm -> busy)", fontsize=10)
    ax[0].axis("off")
    ax[1].imshow(amp, cmap="viridis")
    ax[1].set_title("hyperprior scale sigma\n(per-region uncertainty)", fontsize=10)
    ax[1].axis("off")
    ax[2].imshow(np.abs(lat - muC), cmap="magma")
    ax[2].set_title("AR residual |latent - mu|\n(small => few bits)", fontsize=10)
    ax[2].axis("off")

    names = ["A\nfactorized", "B\nhyperprior", "C\n+context"]
    vals = [bitsA / npix, bitsB / npix, bitsC / npix]
    bars = ax[3].bar(names, vals, color=["#d1495b", "#e09f3e", "#2e86ab"])
    ax[3].set_ylabel("bits / symbol")
    ax[3].set_title("Better model => fewer bits\nfor the *same* latent", fontsize=10)
    for b, v in zip(bars, vals):
        ax[3].text(b.get_x() + b.get_width() / 2, v, f"{v:.2f}",
                   ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    common.save_fig(fig, "demo4_hyperprior_entropy.png")
    print("\n  Takeaway: the entropy model is where bits are really saved.")
    print("  PICO's one-shot autoregressive context is a ~10% BD-rate lever.")


if __name__ == "__main__":
    main()
