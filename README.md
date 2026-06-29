# Self-Driving Research Notes

**An agent workflow that researches a paper (or a researcher) largely on its own, then turns the result
into cited, undergraduate-friendly learning notes.**

The real deliverable here is not any single paper — it's a **repeatable research-and-teach pipeline**.
Each *instance* below applies the same workflow to a new target. This repo holds the workflow's
methodology plus the instances built so far.

> 🚧 **Ongoing project — kept up to date.** New instances are added over time as the workflow is applied
> to more papers and researchers, and the workflow itself keeps improving. Expect this list to grow.

> Repo name is still `pico-repro` for history; it now hosts the umbrella project.

## The method (how every instance is built)

```
parallel research fan-out   →   verify-before-writing   →   cited teaching HTML   →   (optional) demos   →   publish
   several subagents read         a skeptic fact-checks        history + plain-English        runnable, free/local
   different facets at once        every claim against          summaries + discussion
                                    primary sources              questions for students
```

The full process — including the bugs caught and the four claims a fact-check corrected — is documented,
with workflow diagrams, in **[`methodology.html`](methodology.html)**.

Guiding principles: **run it before you teach it**, **verify before you write**, **cite primary sources**,
and **free / local by default** (everything runs on a laptop CPU / Apple-MPS).

---

## Instances

### 1 · PICO — *What Matters in Practical Learned Image Compression*  *(in this repo)*

A study + simulation of Apple's **PICO** learned image codec
([arXiv:2605.05148](https://arxiv.org/abs/2605.05148), 2026): the history of image compression, how PICO
works step by step, what matters, and how it's scored — backed by citations — plus six free/local Python
demos that simulate each idea.

- Read: **[`index.html`](index.html)** · How it was built: **[`methodology.html`](methodology.html)**
- Run: the six demos in [`demos/`](demos/) (see *The PICO instance* below)

### 2 · Alisa Liu — NLP researcher paper-history  *(sibling notes; built with the same workflow)*

A guided tour of NLP researcher **Alisa Liu**'s body of work for undergraduates — bio, a research-arc
timeline, signature-paper summaries, full publication list, and discussion questions. Built via the same
3-agent parallel fan-out (whose verify pass caught a real misattribution before it shipped).

- Published as its own repo: **[WeiL11/alisa-liu-notes](https://github.com/WeiL11/alisa-liu-notes)** —
  with the same `index.html` (content) + `methodology.html` (method) pair.

### More instances coming…

This is a living project — additional papers and researchers will be added as the workflow is applied to them.

---

