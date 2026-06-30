# DeepSpec — Speculative Decoding

**Method used:** v0.7 (generator-based, one-pass deep-read)
**Date:** June 2026

Research direction 6: understanding [DeepSeek's DeepSpec](https://github.com/deepseek-ai/DeepSpec) framework and the speculative decoding research arc it sits in.

## What we studied

How do you make LLM inference 60–85% faster without changing the model or its outputs?
The answer is **speculative decoding** — a draft model proposes tokens, the target verifies them in one parallel pass.

Covers four papers in chronological order:

| Paper | Year | Key idea |
|---|---|---|
| Leviathan et al. (ICML 2023 Oral) | 2023 | Speculative decoding invented — verify γ tokens in 1 pass |
| EAGLE-3 (Li et al.) | 2025 | Direct token prediction + multi-layer fusion + TTT; best autoregressive drafter |
| DFlash (Chen et al., ICML 2026) | 2026 | Block diffusion — all γ tokens in 1 forward pass via KV injection |
| DSpark (Cheng, Yu, Shao, Li, Xiong et al., DeepSeek) | 2026 | Semi-autoregressive + confidence scheduling; 60–85% faster in production |

## Files

- `index.html` — generated teaching notes
- `notes.py` — the spec (edit this and re-run to update)
- `_research/` — evidence files (one per paper)
- `methodology.html` — how the v0.7 method was applied here

## Regenerate

```bash
python tools/build_notes.py deepspec/notes.py
```
