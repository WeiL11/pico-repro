# Self-Driving Research Notes

**An agent workflow that researches a paper (or a researcher) largely on its own, then turns the result
into cited, undergraduate-friendly learning notes.**

The real deliverable here is not any single paper — it's a **repeatable research-and-teach pipeline**.
Each *instance* below applies the same workflow to a new target. This repo holds the workflow's
methodology plus the instances built so far.

> Repo name is still `pico-repro` for history; it now hosts the umbrella project.

## The method (how every instance is built)

```
parallel research fan-out   →   verify-before-writing   →   cited teaching HTML   →   (optional) demos   →   publish
   several subagents read         a skeptic fact-checks        history + plain-English        runnable, free/local
   different facets at once        every claim against          summaries + discussion
                                    primary sources              questions for students
```

The full process — including the bugs caught and the four claims a fact-check corrected — is documented,
with workflow diagrams, in **[`methodology.html`](methodology.html)**.

Guiding principles: **run it before you teach it**, **verify before you write**, **cite primary sources**,
and **free / local by default** (everything runs on a laptop CPU / Apple-MPS).

---

## Instances

### 1 · PICO — *What Matters in Practical Learned Image Compression*  *(in this repo)*

A study + simulation of Apple's **PICO** learned image codec
([arXiv:2605.05148](https://arxiv.org/abs/2605.05148), 2026): the history of image compression, how PICO
works step by step, what matters, and how it's scored — backed by citations — plus six free/local Python
demos that simulate each idea.

- Read: **[`index.html`](index.html)** · How it was built: **[`methodology.html`](methodology.html)**
- Run: the six demos in [`demos/`](demos/) (see *The PICO instance* below)

### 2 · Alisa Liu — NLP researcher paper-history  *(sibling notes; built with the same workflow)*

A guided tour of NLP researcher **Alisa Liu**'s body of work for undergraduates — bio, a research-arc
timeline, signature-paper summaries, full publication list, and discussion questions. Built via the same
3-agent parallel fan-out (whose verify pass caught a real misattribution before it shipped).

- Lives in `MyClaude/alisa-liu-notes/index.html` (local). **Not yet published to GitHub** — open an issue /
  ask if you'd like it added here or as its own repo.

---

## The PICO instance — details

### What "what matters" means (paper Table 1 — BD-rate vs the naive alternative)

| Design choice | BD-rate | Simulated in |
|---|---|---|
| **Haar resampling** | ~19.5% vs pixel-reshuffle (~8.9% vs stride-2 conv) | `demo2` |
| **One-shot autoregressive context** | ~10.3% | `demo4` |
| **Learned scales** (ConvScale) | ~9.6% | `demo5` (architecture) |
| **Learned quantization width** | ~8.2% | `demo3` |
| all of the above together | ~31.7% | — |

Plus the deepest finding: training for **perception** (LPIPS / MS-SSIM / GAN), evaluated by **human
studies**, beats training for PSNR by a wide margin.

### Setup

```bash
cd pico-repro
pip install -r requirements.txt
```

Requirements: `torch`, `torchvision`, `numpy`, `pillow`, `matplotlib` (all free; MPS/CUDA optional).

### Run the demos

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

Then open **[`index.html`](index.html)** — it embeds the generated figures.

### What each demo shows

- **demo1 — transform coding.** Quantizing 8×8 DCT coefficients beats quantizing raw pixels by several dB.
- **demo2 — Haar resampling.** Haar down-then-up reconstructs *exactly* (~99 dB) vs stride-2 + bilinear (~28.6 dB).
- **demo3 — quantization.** STE, the additive-noise rate proxy, and why adaptive bit allocation lifts the RD curve.
- **demo4 — entropy model.** Bits/symbol drop monotonically: factorized → hyperprior → +autoregressive context.
- **demo5 — the codec.** Draws the mean-scale-hyperprior pipeline + the ablation ranking; trainable `TinyCodec` behind `--train`.
- **demo6 — how JPEG works.** The real JPEG pipeline on actual pixels (YCbCr/chroma, 8×8 DCT + quant, blocky artefacts).

### Repo layout

```
pico-repro/
  README.md           this file (umbrella + PICO instance)
  methodology.html    the agent workflow, with diagrams + a faster parallel plan
  index.html          PICO reading notes (open this) — embeds the figures
  requirements.txt
  demos/              common.py + demo1..demo6
  assets/             PNG figures generated by the demos
  data/               cached Kodak test image(s) — git-ignored, fetched on first run
```

### Scope & honesty (PICO instance)

**Reproduced (in spirit, at small scale):** the mean-scale hyperprior pipeline, transform coding, Haar
resampling, STE/noise quantization, learned `q`, hyperprior + autoregressive context, rate-as-estimated-entropy.

**Not reproduced (explained only):** the NAS, on-device runtime, a real range-coder bitstream, the GAN
discriminator and text/tiling losses, the quality levels (8 coarse, interpolated to 71), and large-scale
training. A 3-minute toy will not reproduce the ablation *ordering* — the clean per-component evidence is in demos 2–4.

### Sources (PICO)

- Paper: <https://arxiv.org/abs/2605.05148> · Apple ML Research: <https://machinelearning.apple.com/research/compression>
- Project page: <https://apple.github.io/ml-pico/>

Full numbered citations are in [`index.html`](index.html) (References section).
