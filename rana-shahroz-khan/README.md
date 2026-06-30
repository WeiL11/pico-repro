# Direction: Rana M. Shahroz Khan

A research direction of the [Self-Driving Research Notes](../README.md) project — the **first built with the
v0.7 HTML generator**. Reading notes on **Rana Muhammad Shahroz Khan** (UNC Chapel Hill CS PhD, advisor
Tianlong Chen; Anthropic Research Fellow 2026). Theme: **efficient + trustworthy LLM adaptation** (LoRA/PEFT
for evolving LLMs, multi-agent LLM safety, reward-free SFT), rooted in optimal-transport / model-compression
undergrad work at Vanderbilt.

- **[`index.html`](index.html)** — the content (generated from [`notes.py`](notes.py) via
  [`../tools/build_notes.py`](../tools/build_notes.py)): a "what I find most interesting" opening, research-arc
  timeline, four foldable per-paper deep dives (PortLLM, ORAL, Agents Under Siege, TMS), full list, discussion
  questions, completeness + honesty boxes.
- **[`methodology.html`](methodology.html)** — how it was built (v0.7), with telemetry.
- **[`_research/`](_research/)** — archived deep-read evidence (one file per paper), so every claim is traceable.
- **[`DECISIONS.md`](DECISIONS.md)** — the decision log; **[`notes.py`](notes.py)** — the generator spec.

To regenerate the page after editing the spec: `python tools/build_notes.py rana-shahroz-khan/notes.py`.

## Honesty
All four signature papers are arXiv-available (no paywall). **Name collision:** the naval / ship-hull "Shahroz
Khan" is a different person — everything here traces to DBLP pid 339/7435 / Scholar pdmMa3UAAAAJ. Citation
counts are approximate (mid-2026). TMS is a 2026 preprint (venue unconfirmed); CAR-LoRA ICLR-2026 track worth
confirming.
