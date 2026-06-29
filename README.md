# PICO — *What Matters in Practical Learned Image Compression* (study notes + simulation)

Reading notes + runnable concept demos for Apple's **PICO** paper,
[*What Matters in Practical Learned Image Compression*](https://arxiv.org/abs/2605.05148)
(arXiv:2605.05148, 2026). Built as a **teaching companion for undergraduates**: it explains the
history of image compression, how PICO works, what matters, and how it's scored — backed by
citations — and ships small **free/local Python demos** that simulate each idea.

This is **not** a reproduction of the codec; it is an educational explainer. Everything runs free and
local on CPU or Apple-MPS in seconds to a few minutes.

## About this project (the bigger picture)

The real goal here is **not just PICO**. This repo is the **first instance** of a larger effort: building
an **efficient agent workflow that can do research largely on its own**, and turn the results into
**learning-progress notes shared with undergraduates**. The repeatable method — parallel research
fan-out → *verify-before-writing* (fact-check against primary sources) → cited teaching HTML → optional
demos → publish — is documented in **[`methodology.html`](methodology.html)**.

- **Instance #1 — PICO** (this repo): Apple's learned-image-compression paper, taught + simulated.
- **Instance #2 — Alisa Liu**: a paper-history study of an NLP researcher, built with the same workflow
  (a sibling notes set; reach out if you'd like it published too).

The rest of this README is the PICO instance.

## The two pages (open these)

- **[`index.html`](index.html)** — the reading notes: history → JPEG walkthrough → how PICO works step by
  step → what matters → how it's scored → discussion questions → references.
- **[`methodology.html`](methodology.html)** — a behind-the-scenes report (with workflow diagrams) on how
  these notes were researched, built, and fact-checked, plus a faster parallel plan for next time.

## What PICO is (one paragraph)

PICO is the first *practical* learned image codec optimised *directly for human perception* instead of
PSNR. The paper is a large ablation study — of all the design choices in a learned codec, which actually
improve rate–distortion? It reports **2.3–3× bitrate savings vs AV1/AV2/VVC/ECM/JPEG-AI** and **20–40%
vs prior learned codecs** in human studies, encoding a 12 MP image in as little as ~230 ms on an
iPhone 17 Pro Max.

## "What matters" (paper Table 1 — BD-rate vs the naive alternative)

| Design choice | BD-rate | Simulated in |
|---|---|---|
| **Haar resampling** | ~19.5% vs pixel-reshuffle (~8.9% vs stride-2 conv) | `demo2` |
| **One-shot autoregressive context** | ~10.3% | `demo4` |
| **Learned scales** (ConvScale) | ~9.6% | `demo5` (architecture) |
| **Learned quantization width** | ~8.2% | `demo3` |
| all of the above together | ~31.7% | — |

Plus the deepest finding: training for **perception** (LPIPS / MS-SSIM / GAN), evaluated by **human
studies**, beats training for PSNR by a wide margin.

## Setup

```bash
cd pico-repro
pip install -r requirements.txt
```

Requirements: `torch`, `torchvision`, `numpy`, `pillow`, `matplotlib` (all free; MPS/CUDA optional).

## Run the demos

Each script prints a short lesson and writes a figure into `assets/`.

```bash
python demos/demo1_transform_coding.py     # transform coding & the rate–distortion trade-off
python demos/demo2_haar_resampling.py      # invertible Haar wavelets vs lossy strided conv
python demos/demo3_quantization.py         # STE, additive-noise rate proxy, adaptive bit allocation
python demos/demo4_hyperprior_entropy.py   # entropy model: factorized -> hyperprior -> context
python demos/demo5_ablation_rd.py          # pipeline diagram + "what matters" charts (no training)
python demos/demo6_jpeg_pipeline.py        # how JPEG works on real pixels (and how it fails at low bitrate)

# optional: actually train the tiny end-to-end codec (~3 min on MPS)
python demos/demo5_ablation_rd.py --train
```

Then open **[`index.html`](index.html)** in a browser — it embeds the generated figures.

## What each demo shows

- **demo1 — transform coding.** Quantizing 8×8 DCT coefficients beats quantizing raw pixels by several dB
  at the same bitrate.
- **demo2 — Haar resampling.** A 2D Haar transform down-then-up reconstructs an image *exactly* (~99 dB),
  while stride-2 + bilinear loses detail (~28.6 dB). PICO's biggest architectural lever.
- **demo3 — quantization.** STE (gradient through rounding), the additive-noise rate proxy, and why
  content-adaptive bit allocation (reverse water-filling) lifts the whole RD curve.
- **demo4 — entropy model.** On a correlated, heteroscedastic latent, estimated bits/symbol drop
  monotonically: factorized → hyperprior → +autoregressive context.
- **demo5 — the codec.** Draws the mean-scale-hyperprior pipeline and the paper's ablation ranking. The
  file also contains `TinyCodec`, a faithful-in-spirit codec you can train with `--train`.
- **demo6 — how JPEG works.** Runs the real JPEG pipeline on actual pixels (YCbCr/chroma subsampling, one
  8×8 block's DCT + quantization, real low-bitrate blocky artefacts) — the baseline PICO moves away from.

## Repo layout

```
pico-repro/
  index.html          reading notes (open this) — embeds the figures
  methodology.html    how the notes were built, with workflow diagrams
  README.md
  requirements.txt
  demos/              common.py + demo1..demo6
  assets/             PNG figures generated by the demos
  data/               cached Kodak test image(s) — git-ignored, fetched on first run
```

## Scope & honesty

**Reproduced (in spirit, at small scale):** the mean-scale hyperprior pipeline, transform coding, Haar
resampling, STE/noise quantization, learned `q`, hyperprior + autoregressive context, and the
rate-as-estimated-entropy formulation.

**Not reproduced (explained only):** the neural architecture search, on-device runtime targets, a real
range-coder bitstream (we report estimated entropy as bpp), the GAN discriminator and text/tiling losses,
the quality levels (8 coarse, interpolated to 71), and large-scale training. A 3-minute toy will not
reproduce the paper's ablation *ordering*; the clean per-component evidence is in demos 2–4.

## Sources

- Paper: <https://arxiv.org/abs/2605.05148>
- Apple ML Research: <https://machinelearning.apple.com/research/compression>
- Project page: <https://apple.github.io/ml-pico/>

Full numbered citations are in [`index.html`](index.html) (References section).
