# Evidence: DFlash — Block Diffusion for Flash Speculative Decoding

**Source**: arXiv:2602.06036; ICML 2026
**Authors**: Jian Chen, Yesheng Liang, Zhijian Liu
**Verified via**: https://arxiv.org/abs/2602.06036

## Core idea
Replace autoregressive draft generation with a **block diffusion** model that generates all γ tokens in a SINGLE forward pass. T_draft ≈ O(1) w.r.t. γ (not O(γ)).

## Architecture
During prefill, inject hidden states from target model layers {l₁,...,l_m} into draft model's KV:
  H_ctx = RMSNorm(Wc[H^(l1);...;H^(lm)])
  Ki = [WiK Hctx; WiK Hd],  Vi = [WiV Hctx; WiV Hd]

Draft model takes: anchor token (the last accepted token) + γ MASK tokens
All positions within the block attend BIDIRECTIONALLY to each other AND to the injected context.
Output: γ logits in one forward pass regardless of γ.

The draft model shares the target's embedding layer and LM head (frozen).

## Key result
- >6x lossless acceleration across diverse models and tasks
- Up to 2.5x speedup over EAGLE-3

## Critical limitation (found in DSpark analysis)
No inter-token dependency: each position marginalizes over ALL possible preceding tokens rather than conditioning on the one actually sampled → SUFFIX DECAY.
- Position-wise conditional acceptance (from DSpark Fig 2): DFlash starts at 0.88 (Math) but drops to 0.78 by position 7 on Code, and from 0.72 to 0.63 on Chat
- Eagle3 is stable or increasing (0.53 → 0.74 on Chat) because it conditions on actual samples

## Cite
Jian Chen, Yesheng Liang, Zhijian Liu. DFlash: Block Diffusion for Flash Speculative Decoding. ICML 2026. arXiv:2602.06036.
