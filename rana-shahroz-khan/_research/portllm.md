# Evidence — PortLLM: Training-Free, Portable Model Patches (ICLR 2025)

Raw deep-read (archived per v0.7). R. M. Shahroz Khan = **first author**. arXiv:2410.10870 · ICLR 2025.

## CONCEPT
Carry a fine-tuned model's knowledge forward to a *newer* base-model version by saving the fine-tune as a small
reusable "patch" (a LoRA delta) and just adding it to the updated model — no retraining.

## INTRO — problem & why
- LoRA: freeze W₀, learn low-rank ΔW = B·A (r=8 downstream); W_new = W₀ + BA. Cheap but still needs GPU training.
- "Evolving base models" modeled as **continued pretraining**: θ' = θ + Δθ. Re-fine-tuning each new version is
  costly (compute — Llama2-13B up to 8×A6000; recurring biannual updates; data may be access/privacy-locked).
- Q: "How to leverage the personalized knowledge captured in the first fine-tuned LLM to update evolving LLMs?"

## METHOD
- **Patch** = the LoRA delta Δθᵢ = B·A from fine-tuning the OLD base θ. Store BA, not a whole model.
- **Apply to new model** without re-fine-tuning: θ'ᵢ ≈ θ' + Δθᵢ (Eq.6) — a simple weight add, runs in seconds, 0
  trainable params.
- **Why it transfers** (theory §3.3): θ'ᵢ = (θ'+Δθᵢ) + (Δθ'ᵢ − Δθᵢ); the residual R is negligible because task
  patches are **low-rank** while base models are full-rank. Empirically R's Frobenius norm ~**136×** smaller than the
  naive-update term (per-dataset 79–194×); max singular value ~66×.

## RESULTS
- Models: Mistral-7B, Llama2-7B, Llama3.1-8B, Gemma2-9B. 7 tasks (BoolQ/SST-2/MRPC/RTE/WNLI/WinoGrande/GSM8K),
  zero-shot. Continued-pretraining data: OpenOrca/SlimOrca/OpenPlatypus/AlpacaGPT4.
- Within ~1 pt of REAL re-fine-tuning on most tasks; **beats** it on WNLI (83.10 vs 82.08) and **GSM8K (41.32 vs
  34.95)** — and the un-patched updated model scored only 15.16 on GSM8K (patch lifts to 41.32).
- Gap to real fine-tune ≤ 0.73%; sometimes outperforms by up to 5.53%. Works even if continued pretraining was
  full-weight (not LoRA).
- Cost (SST-2, Mistral-7B): **0** trainable params (vs 21M); GPU mem 28.71 vs 350.61 GB (**12.2×**); GPU hours
  0.0083 vs 40.65 (**4897×**).

## DISCUSSION / FUTURE / LIMITATIONS
- Future: across DIFFERENT architectures (via model merging). Limitation/assumption: task patches low-rank vs the
  pretraining update; benefit depends on the pretraining data (OpenPlatypus hurt WNLI). Tested θ→one evolved θ',
  same architecture.

## MOST IMPORTANT MISSING THING (per-paper)
Only validated when the SAME model lineage evolves via **continued pretraining** (same architecture/weight shape).
Real provider updates can change architecture/tokenizer/hidden-size or retrain from scratch → no coordinate
correspondence, can't add the old delta. The paper's own future work names cross-architecture as unsolved. So PortLLM
= cheap knowledge portability across successive *same-architecture checkpoints*, not a universal patch surviving a
real architectural version jump.

## Sources used (agent)
- https://arxiv.org/abs/2410.10870 · /pdf (Tables 1,2,4,5,6 verified) · /html v2
