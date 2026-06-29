# Evidence — DeepCC / "Wanna Make Your TCP Scheme Great for Cellular Networks?" (IEEE JSAC 2021)

Raw deep-read from the Pass-2 agent (archived per v0.6: per-claim provenance). Source of truth for the
content-page claims about this paper. Chen-Yu Yen = 2nd author (co-first per his homepage).
Links: arXiv:1912.11735 (precursor, same idea) · JSAC vol.39(1), pp.265–279, 2021.

## CONCEPT
A deep-RL *plug-in* (DeepCC) that sits on top of any existing TCP and steers it to keep latency low on
cellular networks, without replacing TCP.

## INTRO — problem & why
- Cellular bandwidth varies wildly at ms timescales; towers keep deep buffers → **bufferbloat**.
- Throughput-greedy TCPs (Cubic, BBR) fill those buffers → high throughput but huge self-inflicted latency,
  bad for gaming/VR/video calls. Paper: Cubic/BBR "achieve very high throughput … with large delays caused
  by the bufferbloat phenomenon."
- Bet: don't reinvent TCP (hard to deploy) — **boost the TCP you already have** to hit an app delay target.

## METHOD
- Treat underlying TCP as black box; DeepCC only **caps** the congestion window: `cwnd_max = 2^α · cwnd`,
  α ∈ [−1,1] (≈ halve…double the cap). Underlying TCP still probes bandwidth between caps → beats a pure
  clean-slate learned version by ~10% utilization.
- RL loop per RTT. **State:** avg delay d, #samples n, avg delivery rate p, cwnd — normalized vs Target,
  stacked over m=20 steps. **Action:** continuous α. **Reward:** + below Target, − above; scaled by
  throughput×samples.
- Algorithm: **DDPG** (actor–critic for continuous actions); 2 FC hidden layers × 1000 neurons.
- Deployability: a lightweight kernel **Monitor** shim gathers stats independent of the TCP (Cubic/BBR/
  Westwood/Illinois). Per-socket plug-in. CAVEAT: the DRL agent here is a **user-space TensorFlow prototype**.

## RESULTS
- Mahimahi emulation (T-Mobile LTE traces; 2M+ training steps); 23+ real LTE traces (T-Mobile/Verizon/AT&T);
  real-world over GENI + NYC cell clients.
- Boosting Cubic / BBR → **~300% / ~175% lower queuing delay**. Illinois → **~4× lower delay**, throughput −9%.
- Dcubic (Cubic+DeepCC): **4× lower queuing delay**, throughput −~11%. Beats Sprout, Verus, C2TCP, Copa,
  LEDBAT, PCC-Vivace, Remy, Indigo, Aurora.
- Beats own clean-slate variant by ~10% utilization. Fairness Jain 0.936–0.987. Real-world ≈ emulation.

## DISCUSSION / FUTURE / LIMITATIONS
- No theoretical guarantees (true of all CC over uncertain Internet); generalization to unseen networks is an
  open research question. Current version only boosts throughput-oriented TCP to cut delay; leans on cellular
  per-client traffic isolation. Overhead: user-space agent is the bottleneck → kernel impl is future work.

## MOST IMPORTANT MISSING THING (per-paper)
Numbers come from a **user-space prototype** validated mostly on **single-flow** cellular links — the setting
that hides the hard deployment problems. (1) Running a 2×1000 DDPG net every RTT in user space is costly; line-
rate, many-socket behavior isn't shown. (2) Multi-flow coexistence: delay-targeting works partly *because*
cellular isolates each client; on a shared bottleneck a DeepCC flow holding back could be starved by an
aggressive Cubic/BBR flow. Fairness was measured among DeepCC flows, not a hostile mix.

## Sources used (agent)
- https://arxiv.org/abs/1912.11735 · https://ar5iv.labs.arxiv.org/html/1912.11735
- https://nyuscholars.nyu.edu/en/publications/ · Semantic Scholar paper page
