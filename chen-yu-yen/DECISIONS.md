# Decision log — Chen-Yu (Robin) Yen direction

A running record of choices for this direction (v0.6 method requirement: keep a decision log in the repo).

## Context
- Goal: a reading-notes direction on the researcher **Chen-Yu (Robin) Yen**, applying the v0.6 method
  (two-pass, per-claim provenance, evidence in `_research/`, completeness critic, output-quality gate, telemetry).
- No profile URL was given → identity must be established from primary sources first.

## Decisions
- **D1 — Slim Pass 1 (v0.6):** one combined agent does identify + publication list + arc (instead of 3),
  with a ~8–12 fetch budget. Summaries fold into Pass 2.
- **D2 — Pipeline (v0.6):** launch Pass 2 deep-reads as soon as Pass 1 returns a confirmed paper list.
- **D3 — Evidence (v0.6):** each deep-read agent's full output is saved under `_research/` so every claim
  on the content page is traceable.
- **D4 — Paper selection (decided):** deep-read his **first / co-first** papers — they show *his*
  contribution best: (1) Classic Meets Modern (SIGCOMM 2020, co-first, his most-cited ~369), (2) Computers
  Can Learn from the Heuristic Designs (SIGCOMM 2023, co-first), (3) Wanna Make Your TCP Scheme Great…
  cellular TCP (IEEE JSAC 2021, co-first), (4) ASMR (ICML 2024, **first author**, the MRI pivot). CFR-RL
  (JSAC 2020, middle, ~241 cites) and SGLB (SIGCOMM 2025, middle, industry) → full-list + brief only.
- **D5 — Citation counts:** taken from his Google Scholar profile (user `OqRO_psAAAAJ`; total ~828, h-index 7);
  marked approximate. Semantic Scholar per-author totals were unreliable (100+ name collisions).
- **D6 — Disambiguation:** confirmed via homepage + DBLP + Scholar + arXiv + NYU page + LinkedIn; advisor
  H. Jonathan Chao + co-author Soheil Abbasloo are the load-bearing ties. Excluded a Purdue genetics
  "Yu-Chen Yen"; the 2014 Pacific Graphics paper attribution is only moderately confident → flag on the page.

## Telemetry (time per step)
- Pass 1 (1 agent, identify+map): ~117 s, 11 tool uses, ~38k tokens.
- Pass 2 (4 deep-reads, parallel): Orca ~311 s, Sage ~231 s, DeepCC ~113 s, ASMR ~123 s → wall-clock ~311 s.
  (Orca/Sage slow: SIGCOMM PDFs paywalled → reconstructed from authors' survey + code + third-party benchmarks.)
- Completeness critic + quality gate (1 agent): ~73 s — caught the implicit unifying theme, author-order pitfalls,
  ASMR different-lab, 2014 namesake; all fixed before publish.
- Total: 6 agents, ≈16 min summed compute / ≈8 min parallel wall-clock (+ assembly).
- v0.6 deviation: none material. Slimmer than the Alisa runs (6 agents vs 9).

## Resolved
- Who: **Chen-Yu (Robin) Yen** — NYU ECE PhD (advisor H. Jonathan Chao); ML-for-systems (Internet
  congestion control / transport / RL-for-networks), pivot to ML-for-MRI (ASMR), then ByteDance (SGLB).
- Deep-read count: 4 (the first/co-first papers above).
