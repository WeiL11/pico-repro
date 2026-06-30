# Evidence: Leviathan et al. 2023 — Fast Inference from Transformers via Speculative Decoding

**Source**: arXiv:2211.17192; ICML 2023 (Oral presentation)
**Authors**: Yaniv Leviathan, Matan Kalman, Yossi Matias (Google)
**Verified via**: https://arxiv.org/abs/2211.17192

## Core insight
Verifying γ candidate tokens with the large target model requires only ONE forward pass — the same cost as generating a single token normally. So if a cheap draft model can propose γ plausible tokens, the total work is T_draft + T_verify ≈ T_target for γ tokens → speedup.

## Method
- Draft model M_d proposes γ candidate tokens x₁,...,xγ
- Target model M_t runs one forward pass computing p_t(xₖ) for all k simultaneously
- Accept token xₖ with probability min(1, p_t(xₖ)/p_d(xₖ)) — rejection sampling
- First rejection at position k discards xₖ,...,xγ; a bonus token is always generated from M_t
- Output distribution is IDENTICAL to M_t's distribution (lossless)

## Key formula
Accept xₖ with prob: min(1, p_t(xₖ) / p_d(xₖ))
If rejected: sample from adjusted distribution (p_t - min(p_t, p_d)) / normalization

## Results
- 2-3x speedup on T5-XXL vs T5X baseline
- Identical output distribution (mathematically proven)
- No model retraining required

## Notes
- The parallel verification only works because transformer attention can process all γ positions in parallel during one forward pass
- Tree-based extension (Miao et al. 2024) verifies multiple candidate paths simultaneously
