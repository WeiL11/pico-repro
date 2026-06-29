# Direction: PICO — *What Matters in Practical Learned Image Compression*

Research direction #1 of the [Self-Driving Research Notes](../README.md) project. A study + simulation of
Apple's **PICO** learned image codec ([arXiv:2605.05148](https://arxiv.org/abs/2605.05148), 2026).

- **[`index.html`](index.html)** — the content (reading notes: history of image compression → how PICO
  works → what matters → how it's scored → references).
- **[`methodology.html`](methodology.html)** — the method (how this direction was researched & built).
- **[`demos/`](demos/)** — six free/local Python demos that simulate each idea.

## What "what matters" means (paper Table 1 — BD-rate vs the naive alternative)

| Design choice | BD-rate | Simulated in |
|---|---|---|
| **Haar resampling** | ~19.5% vs pixel-reshuffle (~8.9% vs stride-2 conv) | `demo2` |
| **One-shot autoregressive context** | ~10.3% | `demo4` |
| **Learned scales** (ConvScale) | ~9.6% | `demo5` |
| **Learned quantization width** | ~8.2% | `demo3` |
| all of the above together | ~31.7% | — |

Plus the deepest finding: training for **perception** (LPIPS / MS-SSIM / GAN), judged by **human studies**,
beats training for PSNR by a wide margin.

## Run the demos

```bash
cd pico-repro/pico
pip install -r requirements.txt

python demos/demo1_transform_coding.py     # transform coding & the rate–distortion trade-off
python demos/demo2_haar_resampling.py      # invertible Haar wavelets vs lossy strided conv
python demos/demo3_quantization.py         # STE, additive-noise rate proxy, adaptive bit allocation
python demos/demo4_hyperprior_entropy.py   # entropy model: factorized -> hyperprior -> context
python demos/demo5_ablation_rd.py          # pipeline diagram + "what matters" charts (no training)
python demos/demo6_jpeg_pipeline.py        # how JPEG works on real pixels (and how it fails)

# optional: actually train the tiny end-to-end codec (~3 min on MPS)
python demos/demo5_ablation_rd.py --train
```

Each script prints a short lesson and writes a figure into `assets/`; then open `index.html`.

## Scope & honesty

**Reproduced (in spirit, at small scale):** the mean-scale hyperprior pipeline, transform coding, Haar
resampling, STE/noise quantization, learned `q`, hyperprior + autoregressive context, rate-as-estimated-entropy.

**Not reproduced (explained only):** the NAS, on-device runtime, a real range-coder bitstream, the GAN
discriminator and text/tiling losses, the 8→71 interpolated quality levels, and large-scale training. A
3-minute toy will not reproduce the ablation *ordering* — the clean per-component evidence is in demos 2–4.

## Sources

- Paper: <https://arxiv.org/abs/2605.05148> · Apple ML Research: <https://machinelearning.apple.com/research/compression>
- Project page: <https://apple.github.io/ml-pico/> · Full citations: in [`index.html`](index.html).
