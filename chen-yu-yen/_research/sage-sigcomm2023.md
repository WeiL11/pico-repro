# Evidence — "Computers Can Learn from the Heuristic Designs…" (Sage, SIGCOMM 2023)

Raw deep-read from the Pass-2 agent (archived per v0.6). Chen-Yu Yen = first-listed author (co-first per his
homepage/brief — **not independently confirmed from the PDF**, flag on page). ACM SIGCOMM 2023, pp.255–274,
DOI 10.1145/3603269.3604838. System = **Sage**. Code: github.com/Soheil-ab/sage.

> Evidence caveat: ACM/arXiv full text was paywalled/403 to the agent. Method reconstructed from the official
> open-source release (README + `sage_rl/` source + training config) + the SIGCOMM talk + 3 independent
> benchmark papers. **Sage's own headline % numbers are UNVERIFIED** (not quoted).

## CONCEPT
A CC algorithm a computer *learned by itself* by watching decades of human-designed CC schemes — and ended
up beating its own teachers.

## INTRO — problem & why
- Two camps: hand-designed heuristics (Cubic, BBR) — robust, deployable, plateau; vs clean-slate learned CC
  (Aurora/Remy/PCC/Indigo) — overhead, poor convergence, bad generalization, often loses to Cubic in the wild.
- Sage asks: learn from the *existing heuristic designs themselves* and synthesize something better.
- Builds on **Orca / "Classic Meets Modern" (SIGCOMM 2020, same authors)**: Orca ran a classic scheme
  underneath + a deep-RL agent on top. Sage is the next step — learn from *many* heuristics *offline* into a
  single standalone data-driven policy ("standing on the shoulders" of 40 years of CC).

## METHOD
- Treat every Linux CC scheme as a **teacher**; log their (state, action) traces; use **offline RL** to
  distill a policy that improves on all of them. NOT behavioral cloning (would only match best teacher), NOT
  online RL/DAgger (no live interaction) — offline RL with value estimation stitches the better-than-average
  actions across teachers.
- Learner = **Recurrent CRR** (Critic-Regularized Regression; distributional critic, 101 atoms, vmin0/vmax500;
  on Acme/TF2). Policy & critic: 2-layer MLP(256, leaky-ReLU) → LSTM(1024), seq len 50. **Obs**: 69-dim
  (throughput, RTT/min-RTT, cwnd, in-flight, loss…). **Action**: scalar in [−2,2] → pow(2,·) = ×0.25…×4
  multiplier on rate/cwnd each 10 ms (relative action → transfers across link speeds). **Reward**:
  throughput-vs-delay "power".
- Training: a Policy Collector runs kernel schemes (teacher pool BBRv2, Cubic, Vegas; repo also ships Orca,
  DeepCC, C2TCP, NATCP) in Mahimahi → two trace sets (Set 1 = changing single-flow conditions; Set 2 =
  TCP-friendliness/fairness). Offline dataset → recurrent-CRR (7-day training). Deployed as kernel module
  "TCP Pure" (Linux 4.19) + user-space inference (Orca-style split).

## RESULTS
- Sage's own paper numbers: **UNVERIFIED** (paywall) — not quoted.
- Independent third-party re-runs (verified): STRENGTHS — resilient to non-congestive (random) loss where
  Cubic suffers (LEO study arXiv:2510.25498); good intra-RTT (same base-RTT) fairness for most queue sizes
  (Sussex arXiv:2510.25105, credited to Set-2 training). WEAKNESSES — "unstable outside its training range,
  oscillating its sending rate, slow convergence" (Sussex); lowest goodput under frequent bandwidth/RTT
  change & periodic base-RTT change (LEO); weak inter-RTT fairness (no such traces in pool).
- Overhead: kernel module + user-space inference, 10 ms polling; exact CPU numbers unverified.

## DISCUSSION / FUTURE / LIMITATIONS
- Insight: offline RL over logged heuristic behavior can *exceed* the heuristics, because a learned critic
  picks good decisions from many teachers. But you only learn what's in the pool → blind spots map to trace
  gaps (inter-RTT fairness; continuous variation). Fix = richer trace pool (offline design makes adding
  teachers cheap). Black-box (uninterpretable); needs patched kernel + heavy 7-day offline training.

## MOST IMPORTANT MISSING THING (per-paper)
Sage is only as good as the heuristics in its training pool — its "mastery" does NOT transfer to regimes it
never saw a teacher operate in. Independent re-evals confirm: shines on in-pool-like conditions, but
destabilizes / underperforms Cubic under continuously changing bandwidth/RTT and unequal-RTT competition
(cases absent from its pool). Read the "computers can master CC" headline as "distill and surpass the *union
of their teachers* — within the envelope those teachers covered." Open question (unanswered): can a learned
CC generalize *beyond* any heuristic it was shown?

## Sources used (agent)
- ACM DOI 10.1145/3603269.3604838 (full text 403) · github.com/Soheil-ab/sage (code/config/source)
- NYU Scholars page · SIGCOMM 2023 program + talk youtube _3-n8_1JwnU
- arXiv:2510.25105 (Sussex) · arXiv:2510.25498 (LEO) — independent benchmarks
