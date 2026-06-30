# Evidence: DSpark — Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation

**Source**: DSpark_paper.pdf in deepseek-ai/DeepSpec GitHub repo
**Authors**: Xin Cheng*, Xingkai Yu*, Chenze Shao*, Jiashi Li*, Yunfan Xiong* (equal contrib) + large DeepSeek-AI team
**Institution**: Peking University + DeepSeek-AI
**Verified via**: Direct PDF read (pages 1-13)

## Two problems DSpark solves
1. Parallel drafters (DFlash) have suffix decay due to missing inter-token dependency
2. Indiscriminate full-block verification wastes batch capacity under high concurrency

## Architecture: Semi-Autoregressive Generation (Section 3.1)

### Parallel stage (DFlash backbone, slightly modified)
- Runs one forward pass over anchor token + γ positions
- Outputs hidden states h₁,...,hγ and base logits U₁,...,Uγ
- Minor modification: treats anchor as first prediction position (not just anchor for masks)

### Sequential stage (lightweight head)
Adds a prefix-dependent transition bias Bₖ(x₀, x<k, xₖ) to the base logits:
  P(X|x₀) = ∏ₖ pₖ(xₖ|x₀,x<k)
  pₖ(v|x₀,x<k) = softmax(Uₖ(v) + Bₖ(x₀,x<k,v))

Two implementations:
- **Markov head**: B(xₖ₋₁,·) = W₁[xₖ₋₁]W₂  (r=256 low-rank, lookup + project)
  - First-order dependency on previous token; cheap per step
- **RNN head**: maintains recurrent state sₖ = σ(Wg zₖ)⊙sₖ₋₁ + (1−σ(Wg zₖ))⊙tanh(Wc zₖ)
  - Full intra-block history; zₖ = [sₖ₋₁; W₁[xₖ₋₁]; hₖ]

### Why it works
Sequential head is MUCH cheaper than the parallel backbone (T_sequential ≪ T_parallel), so drafting latency is still dominated by the parallel stage. But even a 1st-order Markov correction nearly eliminates suffix decay:
- Figure 2: DSpark conditional acceptance stays high and stable (≈0.89 on Math throughout positions 1-7) vs DFlash (0.88 → 0.78)
- A 2-layer DSpark outperforms 5-layer DFlash (Figure 3)

## Architecture: Confidence-Scheduled Verification (Section 3.2)

### Confidence head
cₖ = σ(w⊤[hₖ; W₁[xₖ₋₁]])   ∈ (0,1)
Supervised with: cₖ* = 1 − ½‖p_draft_k − p_target_k‖₁

### Sequential Temperature Scaling (STS)
Position-by-position calibration: for each position k, find temperature scalar that minimizes ECE of the cumulative product ∏_{i≤k} cᵢ. This corrects overconfidence while preserving ranking.

### Hardware-Aware Prefix Scheduler (Algorithm 1)
For R active requests, maximizes system throughput Θ = τ·SPS(B):
- τ = expected accepted tokens = Σᵣ(1 + Σⱼ aᵣ,ⱼ) where aᵣ,ⱼ = ∏_{i≤j} cᵣ,ᵢ
- B = batch size in tokens sent to target = Σᵣ(1 + ℓᵣ)
- SPS(B) = steps/second profiled once at startup (monotonically decreasing in B)
- Greedy: sort all candidate (r,j) extensions by aᵣ,ⱼ descending; admit until Θ stops increasing

Non-anticipating constraint: use early-stopping (break when Θ ≤ Θ_best) to avoid leaking future token information into the admission decision.

## Training
Three losses (position-weighted by wₖ = exp(-(k-1)/γ)):
- L_ce = -Σ wₖ log p_draft_k(x_k*)   (cross-entropy)
- L_tv = Σ wₖ ‖p_draft_k - p_target_k‖₁   (distribution matching → directly maximizes acceptance)
- L_conf = -Σ wₖ [cₖ* log cₖ + (1-cₖ*)log(1-cₖ)]   (confidence head BCE)
- L = 0.1·L_ce + 0.9·L_tv + 1.0·L_conf

## Experimental results (Table 1 — accepted length τ per round)
Target: Qwen3-4B
| Domain | Eagle3 | DFlash | DSpark |
|--------|--------|--------|--------|
| GSM8K  | 5.14   | 5.40   | **6.11** |
| MATH500| 4.62   | 4.85   | **5.78** |
| AIME25 | 3.92   | 4.15   | **4.89** |
| MBPP   | 3.69   | 4.40   | **5.13** |
| HumanEval | 4.16 | 4.74 | **5.38** |
| LiveCodeBench | 3.77 | 4.18 | **4.86** |
| MT-Bench | 2.39 | 3.07 | **3.64** |
| Alpaca | 2.26 | 2.96 | **3.54** |
| Arena-Hard | 2.55 | 2.83 | **3.29** |

Macro-average gains vs Eagle3: +30.9% (4B), +26.7% (8B), +30.0% (14B)
Macro-average gains vs DFlash: +16.3% (4B), +18.4% (8B), +18.3% (14B)

## Production results (DeepSeek-V4 serving)
- vs MTP-1 baseline: 60%–85% faster per-user generation at matched throughput (V4-Flash and V4-Pro)
- Enables SLA tiers (120 TPS Flash, 50 TPS Pro) that MTP-1 couldn't maintain
- Shifts the Pareto frontier: more users served at same latency

## What's missing / caveats
1. The semi-autoregressive architecture still inherits DFlash's backbone limitation: it cannot be directly applied when the base model changes architecture
2. The confidence scheduler's greedy optimality assumes a unimodal (smoothly decreasing) SPS(B) curve — they address non-smooth cases via engineering in Appendix A
3. All offline evaluation uses non-thinking mode; thinking mode (chain-of-thought) results are deferred
4. Training data: Open-PerfectBlend (1.3M samples), non-thinking mode responses only

## Cite
Xin Cheng, Xingkai Yu, Chenze Shao, Jiashi Li, Yunfan Xiong, et al. (DeepSeek-AI). DSpark_paper.pdf in github.com/deepseek-ai/DeepSpec, released June 2026.
