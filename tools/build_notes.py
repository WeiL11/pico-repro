#!/usr/bin/env python3
"""
build_notes.py — generate a research-direction `index.html` from a structured spec.

Part of the v0.7 method: instead of hand-writing each content page, fill a spec
(a Python file defining a dict `NOTES`) and generate the HTML. Free / local, no
dependencies (stdlib only). Prose fields are raw HTML strings, so you can use
<strong>, <a>, <em>, <div class="formula">… inside them.

Usage:
    python tools/build_notes.py <direction>/notes.py            # -> <direction>/index.html
    python tools/build_notes.py <direction>/notes.py out.html

See tools/example_notes.py for the schema.
"""
import importlib.util
import os
import sys

CSS = r"""
  :root{--blue:#2e86ab;--red:#d1495b;--amber:#e09f3e;--green:#3a7d44;--purple:#6a4c93;
        --ink:#1c2430;--muted:#5b6776;--line:#e3e8ee;--bg:#f7f9fb;--card:#fff}
  *{box-sizing:border-box}
  body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.6}
  a{color:var(--blue)}
  header{background:linear-gradient(135deg,#1d2b3a,#2f5066);color:#fff;padding:52px 24px 38px}
  header .wrap{max-width:940px;margin:0 auto}
  header h1{margin:0 0 6px;font-size:30px}
  header .sub{font-size:16.5px;opacity:.92;margin:0 0 14px}
  header .meta{font-size:13.5px;opacity:.82}
  .tags{margin-top:14px}.tag{display:inline-block;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);border-radius:999px;padding:4px 12px;font-size:12.5px;margin:0 6px 6px 0}
  main{max-width:940px;margin:0 auto;padding:8px 24px 64px}
  section{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px 26px;margin:20px 0;box-shadow:0 1px 2px rgba(20,30,45,.04)}
  h2{font-size:21px;margin:2px 0 12px}h3{font-size:15.5px;margin:16px 0 6px}
  p{margin:9px 0}.lead{font-size:17px}.muted{color:var(--muted)}
  .studynote{background:#eef4fb;border:1px solid #cfe0f0;border-left:4px solid var(--blue);border-radius:0 12px 12px 0;padding:16px 20px;margin:20px 0}
  .studynote h2{font-size:18px;margin:0 0 6px}.studynote p{font-size:14.5px;margin:6px 0}
  .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin:14px 0}
  .stat{background:#f1f6fa;border:1px solid var(--line);border-radius:10px;padding:14px 16px}
  .stat b{display:block;font-size:17px;color:var(--blue)}.stat span{font-size:12.5px;color:var(--muted)}
  .timeline{position:relative;margin:18px 0 4px;padding-left:30px}
  .timeline::before{content:"";position:absolute;left:8px;top:6px;bottom:6px;width:2px;background:var(--line)}
  .era{position:relative;margin:0 0 18px}
  .era::before{content:"";position:absolute;left:-26px;top:5px;width:14px;height:14px;border-radius:50%;background:var(--blue);border:3px solid #fff;box-shadow:0 0 0 1px var(--line)}
  .era.hl::before{background:var(--red)}
  .era .yr{font-size:12px;color:var(--muted);font-weight:700;letter-spacing:.04em;text-transform:uppercase}
  .era h3{margin:2px 0 4px;font-size:15.5px}.era p{margin:5px 0}
  details.paper{border:1px solid var(--line);border-radius:11px;margin:12px 0;background:#fff;overflow:hidden}
  details.paper>summary{list-style:none;cursor:pointer;padding:14px 16px}
  details.paper>summary::-webkit-details-marker{display:none}
  details.paper>summary::before{content:"\25B8\00a0";color:var(--blue);font-weight:700}
  details.paper[open]>summary::before{content:"\25BE\00a0"}
  details.paper>summary h3{display:inline;font-size:16px;margin:0}
  details.paper>summary .concept{display:block;font-size:13px;color:var(--muted);margin:5px 0 0 16px}
  details.paper .body{padding:2px 16px 14px;border-top:1px solid var(--line);margin-top:10px}
  details.paper h4{margin:14px 0 3px;font-size:12.5px;color:var(--purple);text-transform:uppercase;letter-spacing:.04em}
  details.paper .body p{margin:4px 0;font-size:14px}
  .badge{display:inline-block;font-size:11px;border-radius:999px;padding:1px 8px;margin-left:6px;background:#eaf4ea;color:#2c6b34;border:1px solid #bfe0c2;vertical-align:middle}
  .badge.first{background:#fde9ec;color:#a83246;border-color:#f3c4cc}
  .miss{border-left:4px solid var(--red);background:#fdeef0;padding:10px 14px;border-radius:0 8px 8px 0;margin:12px 0;font-size:13.5px}
  .unv{background:#fff3cd;border:1px solid #f0d98c;border-radius:4px;padding:0 5px;font-size:11.5px;color:#7a5a00}
  .cite-line{font-size:12.5px;color:var(--muted);margin-top:12px;border-top:1px dashed var(--line);padding-top:8px}
  .formula{background:#11161d;color:#e6edf3;border-radius:8px;padding:8px 12px;font-family:ui-monospace,Menlo,monospace;font-size:12.5px;margin:6px 0;overflow:auto}
  table{border-collapse:collapse;width:100%;font-size:13.5px;margin:12px 0}
  th,td{border:1px solid var(--line);padding:7px 9px;text-align:left;vertical-align:top}th{background:#f1f6fa}
  ol.qbox{counter-reset:q;list-style:none;padding:0;margin:12px 0}
  ol.qbox li{position:relative;background:#f7fafc;border:1px solid var(--line);border-radius:10px;padding:12px 16px 12px 52px;margin:10px 0}
  ol.qbox li::before{counter-increment:q;content:"Q" counter(q);position:absolute;left:14px;top:12px;font-weight:800;color:var(--blue)}
  .callout{border-left:4px solid var(--amber);background:#fff8ec;padding:12px 16px;border-radius:0 8px 8px 0;margin:14px 0}
  .callout.warn{border-color:var(--red);background:#fdeef0}
  nav.toc{font-size:14px}nav.toc a{display:inline-block;margin:0 14px 6px 0}
  footer{max-width:940px;margin:0 auto;padding:0 24px 50px;color:var(--muted);font-size:13px}
"""


def _paper(p):
    badge = p.get("badge", "")
    cls = "badge first" if badge in ("1st", "first") else "badge"
    badge_html = f' <span class="{cls}">{badge}</span>' if badge else ""
    body = []
    for label, key in [("Intro &mdash; why", "intro"), ("Method &mdash; how", "method"),
                       ("Results", "results"), ("Discussion &amp; future", "discussion")]:
        if p.get(key):
            body.append(f'      <h4>{label}</h4>\n      <p>{p[key]}</p>')
    miss = f'      <div class="miss"><strong>⚠ Most important thing missing:</strong> {p["missing"]}</div>' if p.get("missing") else ""
    cite = f'      <p class="cite-line">{p["cite"]}</p>' if p.get("cite") else ""
    return (f'  <details class="paper">\n'
            f'    <summary><h3>{p["title_html"]}{badge_html}</h3>\n'
            f'      <span class="concept">{p.get("concept","")}</span></summary>\n'
            f'    <div class="body">\n' + "\n".join(body) + "\n" +
            (miss + "\n" if miss else "") + (cite + "\n" if cite else "") +
            f'    </div>\n  </details>')


def render(N):
    P = []
    A = P.append
    A('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A(f'<title>{N["name"]} &mdash; {N.get("title_suffix","research reading notes")}</title>')
    A(f"<style>{CSS}</style>\n</head>\n<body>")
    # header
    A('<header>\n  <div class="wrap">')
    A(f'    <h1>{N["name"]} &mdash; {N.get("title_suffix","research reading notes")}</h1>')
    A(f'    <p class="sub">{N.get("subtitle","")}</p>')
    if N.get("meta_html"):
        A(f'    <p class="meta">{N["meta_html"]}</p>')
    if N.get("tags"):
        A('    <div class="tags">' + "".join(f'<span class="tag">{t}</span>' for t in N["tags"]) + '</div>')
    A('  </div>\n</header>\n\n<main>')
    # study-group banner
    if N.get("studynote_html"):
        A(f'\n<div class="studynote">\n  <h2>📚 For our study group</h2>\n  {N["studynote_html"]}\n</div>')
    # opening hook
    if N.get("hook_html"):
        A('\n<section style="border-left:5px solid var(--amber)">\n  <h2>💡 What I find most interesting</h2>\n  '
          + N["hook_html"] + '\n</section>')
    # who
    if N.get("stats") or N.get("edu_html"):
        A('\n<section>\n  <h2>Who they are</h2>')
        if N.get("stats"):
            A('  <div class="grid">' + "".join(
                f'<div class="stat"><b>{b}</b><span>{s}</span></div>' for b, s in N["stats"]) + '</div>')
        if N.get("edu_html"):
            A(f'  <p class="muted">{N["edu_html"]}</p>')
        # TOC
        toc = ['<a href="#arc">Research arc</a>', '<a href="#start">Start here</a>',
               '<a href="#papers">Signature papers</a>', '<a href="#list">Full publication list</a>',
               '<a href="#discuss">Your turn</a>', '<a href="#complete">What&rsquo;s not covered</a>',
               '<a href="#sources">Sources &amp; honesty</a>']
        A('  <nav class="toc"><div style="height:1px;background:var(--line);margin:8px 0 10px"></div>'
          '<strong>Contents:</strong> ' + " ".join(toc) + '</nav>')
        A('</section>')
    # arc
    if N.get("arc"):
        A('\n<section id="arc">\n  <h2>The research arc</h2>\n  <div class="timeline">')
        for e in N["arc"]:
            hl = " hl" if e.get("hl") else ""
            A(f'    <div class="era{hl}"><div class="yr">{e["yr"]}</div>\n      <h3>{e["title"]}</h3>\n      <p>{e["html"]}</p></div>')
        A('  </div>\n</section>')
    # start here
    if N.get("start"):
        A('\n<section id="start">\n  <h2>Start here (a reading order)</h2>\n  <ol>')
        for li in N["start"]:
            A(f'    <li>{li}</li>')
        A('  </ol>\n</section>')
    # papers
    if N.get("papers"):
        A('\n<section id="papers">\n  <h2>Signature papers — deep dive</h2>')
        A('  <p class="muted">Folded by default &mdash; <strong>click a title</strong> to expand Intro → Method → Results → '
          'Discussion &amp; future + a red &ldquo;most important thing missing&rdquo; box.</p>')
        for p in N["papers"]:
            A(_paper(p))
        A('</section>')
    # full list
    if N.get("list_rows"):
        A('\n<section id="list">\n  <h2>Full publication list (newest first)</h2>')
        A('  <table>\n    <tr><th>Year</th><th>Paper</th><th>Venue</th><th>Role</th><th>~Cites</th></tr>')
        for row in N["list_rows"]:
            y, paper, venue, role, cites = row
            A(f'    <tr><td>{y}</td><td>{paper}</td><td>{venue}</td><td>{role}</td><td>{cites}</td></tr>')
        A('  </table>\n</section>')
    # discussion
    if N.get("discuss"):
        A('\n<section id="discuss">\n  <h2>Your turn: discussion questions</h2>\n  <ol class="qbox">')
        for li in N["discuss"]:
            A(f'    <li>{li}</li>')
        A('  </ol>\n</section>')
    # completeness
    if N.get("complete_html"):
        A(f'\n<section id="complete">\n  <h2>What these notes don&rsquo;t cover (completeness)</h2>\n  {N["complete_html"]}\n</section>')
    # sources
    if N.get("sources_html"):
        A(f'\n<section id="sources">\n  <h2>Sources &amp; honesty</h2>\n  {N["sources_html"]}\n</section>')
    A('\n</main>\n\n<footer>\n  <div style="height:1px;background:var(--line);margin:0 0 14px"></div>')
    A('  <p>Reading notes prepared for an undergraduate study group &mdash; a learning aid, not an official bibliography. '
      'Every paper links its primary source; please check the claims.</p>\n</footer>\n\n</body>\n</html>')
    return "\n".join(P) + "\n"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    spec_path = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(spec_path) or ".", "index.html")
    spec = importlib.util.spec_from_file_location("notes_spec", spec_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with open(out, "w") as f:
        f.write(render(mod.NOTES))
    print(f"wrote {out}  ({len(mod.NOTES.get('papers', []))} papers)")


if __name__ == "__main__":
    main()
