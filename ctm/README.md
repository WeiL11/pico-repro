# CTM — Continuous Thought Machines

**Method used:** v0.7 (generator-based, single-paper deep dive)
**Venue:** NeurIPS 2025 (Spotlight)
**Date added:** June 2026

Research direction 7: understanding Sakana AI's Continuous Thought Machines — a new neural architecture that reinstates neural timing and synchronization as core computation.

## What we studied

The CTM gives each neuron its own private temporal processing weights (Neuron-Level Models) and uses the cross-correlation of neuron activity histories — neural synchronization — as the latent representation. Internal ticks run on a self-generated timeline decoupled from the input data, and adaptive compute emerges naturally without any explicit halting module.

## Key concepts

| Concept | What it means |
|---|---|
| Internal ticks | The model "thinks" for T steps on its own timeline, even for a static image |
| Neuron-Level Models (NLMs) | Each neuron d has private weights θ_d; processes only its own history |
| Synchronization S^t | S^t = Z^t · (Z^t)^T: which neurons fire together = the latent state |
| Adaptive compute | Picks best-prediction and highest-certainty ticks per sample; no halting module |
| Binding hypothesis | Neuroscience basis: the brain encodes "same object" by synchronizing neurons |

## Files

- `index.html` — generated teaching notes  
- `notes.py` — the spec (edit and re-run to update)
- `_research/ctm.md` — evidence file
- `README.md` — this file

## Regenerate

```bash
python tools/build_notes.py ctm/notes.py
```

## Links

- Paper: https://arxiv.org/abs/2505.05522
- GitHub: https://github.com/SakanaAI/continuous-thought-machines
- Interactive demo: https://pub.sakana.ai/ctm
