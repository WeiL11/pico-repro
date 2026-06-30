# Evidence — TMS: Trajectory-Mixed Supervision for Reward-Free, On-Policy SFT (2026 preprint)

Raw deep-read (archived per v0.7). R. M. Shahroz Khan = **first author**. arXiv:2602.03073 (Feb 2026; venue
unconfirmed — preprint).

## CONCEPT
Fine-tune an LLM to get most of RL's "stability" benefit WITHOUT building a reward model — by training the model
on samples drawn from its own past training checkpoints.

## INTRO — problem & why
- SFT = train on fixed (question→answer) labels: cheap, stable, but static labels → brittle, catastrophic
  forgetting. RLHF = train a reward model + RL: better retention but costly, unstable, needs reward engineering.
- On-policy = learn from answers sampled from the model as it currently is; off-policy = from a fixed source.
  Reward-free = no reward model/verifier at all.
- Root cause named: **Supervision Mismatch** — the model's evolving policy diverges from static labels → mode
  collapse + forgetting.

## METHOD
- **PLD (Policy-Label Divergence)** = E_x[ KL( q(·|x) ‖ π_θt(·|x) ) ]; it dips early then rises → drift predicts
  forgetting.
- **TMS**, 3 stages: (1) run ordinary SFT, save T=10 checkpoints; each checkpoint generates its OWN answer to each
  question. (2) Mixture m = uniform over those self-generated answers; optionally blend human labels q with α=0.25
  → q_α = α·q + (1−α)·m. (3) Train student to match q_α via forward KL (≈ pick a random checkpoint's answer, apply
  NLL).
- "On-policy yet reward-free": targets are text the model itself plausibly generates (near its own support → RL-like
  stability), but signal is just "imitate your own past samples" (no reward/verifier/RL loop). Trajectory = curriculum
  (early = diverse support, late = refined).

## RESULTS
- Qwen-2.5 (1.5/3/7B), LLaMA-3.1-8B, 3.2-1B; tasks MATH/GSM8K/Math-500/Countdown/IFEval/MMLU/ToolAlpaca + VQA;
  retention on ARC-C/HotpotQA/SafetyBench. Baselines SFT, iterative SFT, GRPO (RL).
- Matches SFT target accuracy while nearly eliminating forgetting: cross-task avg Δ — SFT **−26 to −41**, TMS
  **−2.3 to −2.9**, GRPO −0.9 to −1.9. (e.g. Qwen-1.5B MATH retention ARC-C: SFT 42.3 / TMS 65.4 / GRPO 66.7.)
- Safety retention (Qwen-3B SafetyBench): SFT 31.1 → TMS 35.0 → GRPO 35.4. Cost: harvest T=10 + one student pass;
  no reward models/verifiers.

## DISCUSSION / FUTURE / LIMITATIONS
- "RL remains the gold standard for retention" — TMS closely tracks but GRPO still wins slightly. Largest gains on
  non-unique solution spaces (math/IFEval); modest on rigid formats (MMLU). Optimal T≈8–10. Safety needs careful data
  curation (targets are model's own outputs).

## MOST IMPORTANT MISSING THING (per-paper)
TMS does NOT beat RL — it only **narrows** the gap; "approaches RL retention" can be mis-read as "matches RL." Paper
is explicit RL is the gold standard and TMS incurs a modestly larger cross-task drop than GRPO. Correct takeaway:
a cheap, reward-free drop-in that recovers MOST of RL's stability (SFT→RL retention gap from ~25–40 pts down to
~2–3) at near-SFT cost — not a leaderboard-topping RL replacement. Secondary risk: targets = model's own generations,
so latent base-model biases can be reinforced (why safety gains "require careful data curation").

## Sources used (agent)
- https://arxiv.org/abs/2602.03073 · /html v1 · ADS record (metadata)
