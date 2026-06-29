# Evidence — Orca / "Classic Meets Modern" (SIGCOMM 2020)

Raw deep-read from the Pass-2 agent (archived per v0.6). Abbasloo*, **Chen-Yu Yen*** (2nd-listed, **co-first /
equal contribution** — confirmed from his NYU homepage "*Co-first authors"), Chao. ACM SIGCOMM 2020,
pp.632–647, DOI 10.1145/3387514.3405892. System = **Orca**. His most-cited paper (~369).

> Evidence caveat: ACM PDF 403 to the agent; no arXiv version exists. Mechanism reconstructed from the
> authors' own survey "Congestion Control: A Renaissance with ML" (IEEE Network 2021) + the official code.
> **Exact evaluation percentages vs Cubic/BBR/Aurora are UNVERIFIED** (not quoted).

## CONCEPT
A **hybrid** CC scheme: classic TCP Cubic does the moment-to-moment work while a deep-RL agent periodically
nudges Cubic's congestion window — adaptivity of learning without discarding proven TCP engineering.

## INTRO — problem & why
- CC = how fast to send so you fill the pipe (bandwidth-delay product) without overflowing router queues.
  Tension: throughput (high) vs latency/RTT (low, hurt by queuing).
- Cubic (loss-based default) fills big buffers → high delay (bufferbloat), and backs off on non-congestion
  loss (cellular/Wi-Fi) → wastes bandwidth. Hand-tuned heuristics can't adapt to all paths.
- Clean-slate learned CC (Remy/PCC/Indigo/Aurora) has overhead, convergence issues, and **poor generalization
  to unseen networks** — often loses to Cubic in the wild.
- Orca's thesis: keep a battle-tested classic scheme as the safe fine-grained controller + add a learned
  coarse-grained supervisor.

## METHOD
- **Two-level (hierarchical) control of cwnd.** Fine-grained: plain Cubic runs underneath per-ACK (stability,
  low overhead, TCP-friendliness). Coarse-grained: every monitoring interval a deep-RL agent applies a
  **multiplicative factor to Cubic's cwnd** (it scales, doesn't set the raw rate).
- RL: **State** = averaged recent throughput, loss, delay (+ delivery rate, RTT, cwnd). **Action** = 2^α,
  ~−2<α<2 (bounded scale of the window → stable/predictable). **Reward** = throughput/latency/loss, around
  "power" = delivered-rate ÷ delay.
- Net = **RNN** (partial observability); trained with **TD3/DDPG**-style actor-critic (continuous actions),
  **offline** in emulation (TF + Gym + Mahimahi). Agent in user space talks to in-kernel Cubic.

## RESULTS (verified qualitative; exact % UNVERIFIED — paywall)
- Consistent high performance across diverse networks (Internet testbeds + emulation); greatly reduces the
  generalization/convergence/overhead problems of clean-slate schemes (e.g. Aurora).
- Only ~**6 hours** of emulated training; overhead **on par with Cubic/BBR**; **friendly to competing Cubic
  flows** (because Cubic is its underlying controller). Compared vs Cubic, BBRv2, Aurora.

## DISCUSSION / FUTURE / LIMITATIONS
- Strength: binding the learned action to an existing TCP keeps the action space small → stable, predictable,
  graceful out-of-distribution; near-deployable (low overhead, TCP-friendly).
- Open: still many quasi-hand-tuned design choices (reward/state/arch); kernel↔user-space split adds overhead;
  emulator-vs-reality gap. Future: transfer/meta-learning to adapt quickly to new networks.

## MOST IMPORTANT MISSING THING (per-paper)
Orca's adaptivity is **bounded by the classic scheme it sits on**: restricting the RL action to a bounded
multiplicative tweak of Cubic's window is *why* it generalizes better than clean-slate schemes — but it's a
ceiling: Orca can correct Cubic, not discover a radically different strategy, so where Cubic's loss-based
premise is wrong the gains are smaller than a fully-free controller might reach. The bet: bounded-but-reliable
> unbounded-but-fragile for the real Internet. (Also: quote exact eval numbers from the SIGCOMM PDF directly.)

## Sources used (agent)
- ACM DOI 10.1145/3387514.3405892 (403) · DBLP AbbaslooYC20 · homepage wp.nyu.edu/cyy/publications (co-first)
- IEEE Network 2021 survey (mechanism) · github.com/Soheil-ab/Orca (code)
