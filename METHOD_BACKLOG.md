# Method backlog (v0.7 self-improving loop)

Candidate method improvements. After each direction, a **retro agent** reads that direction's
`DECISIONS.md` + `METRICS.md` + quality-gate output and appends concrete, testable deltas here.
The user reviews; **adopted** items bump the version in `methodology.html` and move to the Adopted list.

## Open candidates (proposed, awaiting decision)
- [ ] **Fail-fast on paywalls.** Cap each agent at ~6 fetches; on a 403/paywall, immediately fall back to
      arXiv / abstract / secondary sources and stop retrying. *Evidence:* Chen-Yu Yen — Orca (30 fetches,
      311 s) and Sage (27 fetches, 231 s) thrashed ACM paywalls; ~5–7 min lost. *(proposed by v0.6 retro;
      user deferred 2026-06-29)*
- [ ] **Prefer arXiv-HTML / abstract over full PDFs** unless key numbers are missing. *(deferred)*
- [ ] **Group closely-related papers into one deep-read agent** (shared context) instead of one-per-paper. *(deferred)*

## Adopted
- **v0.7 (2026-06-29):** HTML generator `tools/build_notes.py` (fill a spec → generate the content page,
  instead of hand-writing); + this self-improving loop (per-run `METRICS.md` scorecard, an auto-retro agent
  proposing deltas here, the user as approval gate, versioned `methodology.html`).
- **v0.6:** pipeline-not-barrier; per-agent budgets; slimmer Pass 1; per-claim provenance verified once;
  `_research/` evidence; decision log; completeness critic; output-quality gate; cross-run diff; telemetry;
  batched status. (See methodology.html changelog.)

## How a retro runs (the loop)
1. A direction finishes → its metrics are in `METRICS.md`, decisions in `DECISIONS.md`.
2. Run a **retro agent**: "given this run's scorecard + gate output, propose 1–3 testable method deltas."
3. Append them here under *Open candidates*.
4. User approves/rejects → adopted deltas bump `methodology.html` (version + changelog) and apply next run.
5. Next run's metrics show whether the change actually helped (regression check).
