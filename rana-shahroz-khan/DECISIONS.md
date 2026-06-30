# Decision log — Rana M. Shahroz Khan direction

v0.7 method. A running record of choices for this direction.

## Context
- Goal: reading-notes direction on **Rana M. Shahroz Khan**, applying v0.7 (slim Pass 1 → verify → pipelined
  per-paper Pass 2 → completeness critic + quality gate → generate page from spec → telemetry).
- No profile URL given → identity established from primary sources first.

## Decisions
- **D1 — Slim Pass 1 (1 agent)** with ~8–12 fetch budget: identify + paper list + arc + disambiguation.
- **D2 — Pipeline:** launch Pass 2 deep-reads as soon as a confirmed paper list exists.
- **D3 — Evidence:** each deep-read saved under `_research/` for traceability.
- **D4 — Watch the name collision:** there is a known *Shahroz Khan* in ship-hull / engineering-design
  generative ML — confirm whether that is or isn't this person before attributing papers.
- **D5 — Paper selection (decided):** deep-read his 4 strongest **first-author** papers (best show his
  contribution, and all arXiv-available → no paywall risk): (1) **PortLLM** (ICLR 2025) — training-free portable
  model patches; (2) **ORAL** (EMNLP 2025 Findings) — conditional recurrent diffusion to generate LoRAs;
  (3) **Agents Under Siege** (ACL 2025 Main) — optimized prompt attacks on multi-agent LLM systems;
  (4) **TMS** (2026 preprint) — reward-free on-policy SFT. CAR-LoRA (ICLR 2026, position unverified) and
  The Quest for Efficient Reasoning (ICLR 2026, 2nd author) → full-list + brief only. Vanderbilt-era papers
  (PRANC, LOPT, LLMGeo — middle/later author) → list only.
- **D6 — Citation counts:** Semantic Scholar API (~72 cites, h-index 5; Scholar ~54 earlier) — approximate.
- **D7 — Disambiguation (resolved):** confirmed via homepage + DBLP (pid 339/7435) + Semantic Scholar API
  (authorId 2204648295), co-author network Chen/Kolouri. The **ship-hull ShipHullGAN "Shahroz Khan" is a
  DIFFERENT person** (Compute Maritime; Scholar HRC0hPIAAAAJ) — excluded.

## Telemetry (time per step)
- Pass 1 (1 agent): ~115 s, 10 tool uses, ~33k tokens (after one transient rate-limit retry).
- Pass 2 (4 deep-reads, parallel): PortLLM ~108 s, ORAL ~101 s, Agents ~98 s, TMS ~92 s → wall-clock ~108 s.
  **All arXiv-available → no paywall thrashing** (vs ~311 s for the SIGCOMM-paywalled chen-yu-yen run).
- Completeness critic + quality gate (1 agent): ~89 s — confirmed CAR-LoRA first-author; named the unifying theme.
- Assemble: generated via `tools/build_notes.py` from `notes.py` (seconds; no hand-written HTML).
- Total: 6 agents, ~5 min parallel wall-clock. **Fastest direction so far** (v0.7 generator + arXiv-available papers).

## Resolved
- Who: **Rana Muhammad Shahroz Khan** — UNC Chapel Hill CS PhD (advisor Tianlong Chen) + Anthropic Research
  Fellow (2026); efficient ML/NLP (LoRA/PEFT, CoT distillation, multi-agent LLM safety, reward-free SFT);
  Vanderbilt undergrad (Kolouri lab: optimal transport + model compression).
