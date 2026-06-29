# Self-Driving Research Notes

**One project: build an agent workflow that researches a topic largely on its own, then turns the result
into cited, undergraduate-friendly learning notes — and keep improving that workflow.**

This repo is the home of that effort. Its top level **tracks the method itself** (how our research workflow
evolves); each **research direction** lives in its own subfolder and applies the current method.

> 🚧 Ongoing — new directions are added over time, and the method keeps improving.

## 📈 The method we are tracking

**[`methodology.html`](methodology.html)** is the living record of our research method and *how it has
progressed* (a changelog of what we learned each round). The current best method is a **two-pass** workflow —
broad parallel fan-out → verify-before-writing → one deep-read agent per paper → foldable cited HTML — under
three principles (explain the concept; align every claim with a cited source; every agent answers "what's the
most important thing missing?"). Each new direction must use the latest method here.

## Research directions

Each direction is a self-contained folder with its own **`README.md`**, **`index.html`** (content) and
**`methodology.html`** (the method as applied to that direction).

| # | Direction | Content | Method |
|---|---|---|---|
| 1 | **PICO** — learned image compression (Apple) | [`pico/index.html`](pico/index.html) | [`pico/methodology.html`](pico/methodology.html) |
| 2 | **Alisa Liu** — NLP researcher paper-history | [`alisa-liu/index.html`](alisa-liu/index.html) | [`alisa-liu/methodology.html`](alisa-liu/methodology.html) |

…more directions coming as the workflow is applied to new papers and researchers.

## Layout

```
pico-repro/
  README.md             this file — the umbrella
  methodology.html      THE living method + its progress (what the top level tracks)
  pico/                 direction 1: README + index.html + methodology.html + demos/ + assets/
  alisa-liu/            direction 2: README + index.html + methodology.html
```

## Principles (kept across every direction)

1. **Explain the concept well** — Intro (why) / Method (how) / Results / Discussion per paper; define jargon.
2. **Align every statement with the research, with clear citations** — read primary sources; never assert
   from memory; flag the unverified.
3. **Always answer "what's the most important thing missing?"** — a dedicated box per paper.
4. **Open each content page with a personal "what I find most interesting" take.**
5. **Free / local by default**, and the method is a living artifact we keep refining.
