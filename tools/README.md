# tools/

Helpers for the v0.7 method.

## `build_notes.py` — generate a direction's content page from a spec

Instead of hand-writing each `index.html`, fill a spec and generate it (free/local, stdlib only):

```bash
# 1. copy the example into your direction and fill it from the Pass-2 deep-read outputs
cp tools/example_notes.py <direction>/notes.py
# 2. generate the content page
python tools/build_notes.py <direction>/notes.py        # -> <direction>/index.html
```

The spec (`notes.py`) defines a dict `NOTES`; prose fields are raw HTML (so you can use `<strong>`,
`<a href>`, `<em>`, `<div class="formula">…`). See [`example_notes.py`](example_notes.py) for the schema and
which fields are optional. The generator emits the same structure/CSS as the existing directions: header,
study-group banner, "what I find most interesting" hook, who/stats + TOC, research-arc timeline, "start here",
foldable per-paper deep dives (Intro/Method/Results/Discussion + "most important missing" + citation), full
publication table, discussion questions, completeness box, and a sources/honesty box.

> The `methodology.html` (method page) for a direction is still written by hand — it's short and run-specific.
