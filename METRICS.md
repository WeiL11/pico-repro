# Metrics ledger (v0.7 self-improving loop)

One row per direction, newest first — the measurable signal the retro step optimizes against.
Filled from each direction's `DECISIONS.md`. (Earlier rows approximate; per-fetch counts not all logged.)

| Direction | Method | Agents | Wall-clock (∥) | Gate catches | Unverified left | Paywall blocks |
|---|---|---|---|---|---|---|
| Rana M. Shahroz Khan | v0.7 | 1 + 4 + 1 = 6 | **~5 min** | 3 (theme implicit, CAR-LoRA is 1st-author, OT roots) | TMS venue, CAR-LoRA track | **0** (all arXiv) |
| Chen-Yu Yen | v0.6 | 1 + 4 + 1 = 6 | ~8 min | 4 (theme, author-order, ASMR-lab, 2014 namesake) | Orca/Sage exact %, Sage co-first | ACM ×2 |
| Alisa Liu (v2, fresh) | v0.4 | 3 + 6 = 9 | ~10 min | co-first confirmed; same-name excluded | citation counts | Scholar |
| Alisa Liu (v1) | v0.3→0.4 | 3 + 6 = 9 | ~12 min | **Infini-gram misattribution**; DBLP namesake | citation counts | Scholar |
| PICO | v0.1→0.2 | sequential + 2 review | (build-heavy) | 4 paper-claim fixes (Haar %, tiling, 71, latency) | — | — |

## What the trend says (read this before the next run)
- **v0.7 worked:** the generator + arXiv-available papers got the Rana Khan run to **~5 min** (vs ~8 min) with the
  same 6 agents — the assembly-time and paywall costs both dropped.
- **Paywall thrashing is still the top *latent* cost** when papers are behind ACM/IEEE (Chen-Yu Yen: 2 papers ≈ 5–7 min).
  → the fail-fast-on-paywalls backlog item is worth adopting the next time a subject's key papers aren't on arXiv.
- Agent count is stable at 6 (slim Pass 1 + per-paper Pass 2 + critic) without losing quality.
- The verify gate + quality gate keep catching real errors every run (this run: the unifying theme + a 5th first-author
  paper) → keep them; they pay for themselves.
