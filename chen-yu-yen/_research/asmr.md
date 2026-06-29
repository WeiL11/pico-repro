# Evidence — ASMR: Adaptive Sampling of k-Space for Rapid Pathology Prediction (ICML 2024)

Raw deep-read from the Pass-2 agent (archived per v0.6). Chen-Yu Yen = **first author** (co-equal* with
Singhal). arXiv:2406.04318 · ICML 2024 · code adaptive-sampling-mr.github.io.

## CONCEPT
An RL agent decides, one measurement at a time, which MRI k-space columns to collect next — chosen to
maximize *disease detection* (not image quality) — diagnosing with only ~8% of k-space.

## INTRO — problem & why
- MRI is slow because it samples **k-space** (the frequency domain); more lines = longer scan. Faster scans
  would enable population-scale screening.
- "Accelerated MRI" = undersample k-space. Usual approach = reconstruct-then-classify, but reconstruction is
  optimized for image similarity (SSIM), not diagnosis — at 12.5% sampling, reconstructions "started missing
  pathologies." Prior work (EMRT, 2023) skips reconstruction and detects pathology directly from sparse
  k-space, but with a FIXED heuristic sampling pattern. ASMR makes the choice **adaptive + learned**.

## METHOD
- k-space is acquired sequentially → frame as an MDP, train a policy that picks the next column given what's
  measured so far, optimized for the diagnosis.
- **State** sₜ = Mₜ ⊙ xF (acquired columns; full k-space never disclosed). **Action**: next column (Cartesian,
  column-wise; action space shrinks via dynamic masking). **Reward** R = log q_φ(y|sₜ₊₁) — log-likelihood a
  *frozen classifier* gives the true label (rewards measurements that improve the diagnosis, not fidelity).
  **Budget** T = columns × α (e.g. 8%).
- Policy trained with **PPO** (actor-critic). Inputs are frequency-domain → **KSPACE-NET** (Fourier conv →
  |iFFT| → ResNet-18). Two tricks (ablated): label-balanced training envs (data is 2–16% positive); explicit
  action masking (beats a −1 re-pick penalty).
- Contrast: LOUPE/DPS learn a fixed probabilistic mask; reconstruction-RL adapts but optimizes reconstruction;
  ASMR adapts AND optimizes classification.

## RESULTS
- fastMRI knee/brain/prostate, **8 pathology tasks** (imbalanced 1.43–23.88% positive); metric AUROC, 5 seeds.
- Headline: "within 2% of a fully-sampled classifier using only 8% of k-space" on 6/8 tasks (**12.5× accel**).
- Beats EMRT on 7/8; LOUPE/DPS on 6/8 (≥2.5% AUC on 7/8). vs reconstruction-RL: +2.88% knee, +7% brain.
  vs greedy non-adaptive: +1.87/7.01/9.82% (knee/brain/prostate); vs VDS random: +1.33/2/2.25%.
- Ablations: full ASMR 92.32 avg AUC (knee) > ablated variants.

## DISCUSSION / FUTURE / LIMITATIONS
- Single-coil only (modern scanners are multi-coil — untested); slice-level not volume-level; Cartesian
  column sampling. Safety: screening at scale risks false positives → needs extensive clinical trials.

## MOST IMPORTANT MISSING THING (per-paper)
ASMR optimizes detection of a **fixed, pre-specified** pathology list — not a diagnostic image. So (1) it can
only "see" what it was trained to look for; an **incidental finding** outside the label set may lie in
k-space regions it chose NOT to sample (bad for screening, whose point is catching the unexpected); (2) no
human-verifiable image (reconstruction bypassed) → trust/auditability concerns; (3) single-coil + slice-level
+ false-positive risk → the "within 2%" headline is a research-benchmark result, not a clinical tool. Best
read as fast *triage for known conditions*, paired with full imaging on positives.

## Sources used (agent)
- https://arxiv.org/abs/2406.04318 · https://arxiv.org/pdf/2406.04318 (Appendix B tables not paged line-by-line)
