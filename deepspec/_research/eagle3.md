# Evidence: EAGLE-3 — Scaling up Inference Acceleration via Training-Time Test

**Source**: arXiv:2503.01840; submitted March 2025
**Authors**: Yuhui Li, Fangyun Wei, Chao Zhang, Hongyang Zhang
**Verified via**: https://arxiv.org/abs/2503.01840

## Problem EAGLE-3 solves
EAGLE (2024) predicts next FEATURES (hidden states), conditioned on previous features + token. Limitation: scaling training data gives diminishing returns because the feature distribution at inference is different from training (distribution mismatch). EAGLE-3 fixes this.

## Key changes from EAGLE-2
1. **Direct token prediction** (not feature prediction) — removes the feature-level mismatch
2. **Multi-layer feature fusion** — uses hidden states from multiple layers of the target model, not just the top layer
3. **Training-Time Test (TTT)** — during training, the model receives augmented features that simulate what it sees at test time, closing the train/test distribution gap
   - TTT horizon = 7 (same as DSpark/DFlash block size in the comparison)

## Architecture
- Draft model gets token embeddings + hidden states from multiple target layers
- Single-layer transformer with feature fusion
- Autoregressive: each draft position conditions on all previously sampled draft tokens

## Results (from DSpark paper Table 1, re-evaluated on same setup)
- Qwen3-4B, GSM8K: τ = 5.14
- Qwen3-4B, MATH500: τ = 4.62
- Generally lower τ than DFlash/DSpark because autoregressive T_draft scales with block size

## Key limitation
Autoregressive drafting means T_draft ∝ γ, forcing smaller block sizes. Even with TTT, can't match parallel drafters at large block sizes.

## Cite
Yuhui Li, Fangyun Wei, Chao Zhang, Hongyang Zhang. arXiv 2503.01840, March 2025.
