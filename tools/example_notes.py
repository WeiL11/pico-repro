"""Example spec for build_notes.py — copy this per direction, fill from the
Pass-2 deep-read outputs, then run:  python tools/build_notes.py <dir>/notes.py

All prose fields are raw HTML (use <strong>, <a href>, <em>, <div class="formula">…).
Optional fields can be omitted. Badge: "1st" (red) or "co-first"/"2nd" (green) etc.
"""

NOTES = {
    "name": "Example Researcher",
    "title_suffix": "research reading notes",
    "subtitle": "A guided tour of a researcher’s work: what they keep trying to solve, the arc, and what to read first.",
    "meta_html": 'PhD, Some University. <a href="#" style="color:#bfe0f2">homepage</a> · <a href="#" style="color:#bfe0f2">Scholar</a>',
    "tags": ["theme one", "theme two"],
    "studynote_html": '<p>Reading notes on <strong>Example Researcher</strong>. Read the <a href="#arc">arc</a> first, then '
                      '<a href="#start">Start here</a>.</p>\n  <p class="muted">How these were built: <a href="methodology.html">methodology.html</a>.</p>',
    "hook_html": '<p class="lead">The recurring question in their work is <strong>X</strong>.</p>\n'
                 '  <p>They seem especially interested in <strong>Y</strong>.</p>',
    "stats": [("Affiliation", "where they are"), ("Advisor", "who"), ("Theme", "the through-line"), ("~Cites", "approx.")],
    "edu_html": 'Education: … <span class="unv">self-reported</span>',
    "arc": [
        {"yr": "20XX–20YY · era one", "title": "First phase", "html": "What happened, with <strong>key</strong> papers.", "hl": True},
        {"yr": "20YY · era two", "title": "Pivot", "html": "The next phase.", "hl": True},
    ],
    "start": [
        '<strong><a href="#papers">Paper A</a></strong> — the core idea.',
        '<strong><a href="#papers">Paper B</a></strong> — the extension.',
    ],
    "papers": [
        {
            "title_html": "Paper A: a clear title",
            "badge": "1st",
            "concept": "One-line concept of the paper.",
            "intro": "The problem and <strong>why</strong> it matters; define jargon.",
            "method": "How it works. A formula can go inline: <div class=\"formula\">y = f(x)</div>",
            "results": "Concrete numbers from the paper. Mark unsure ones <span class=\"unv\">unverified</span>.",
            "discussion": "Limitations and future work.",
            "missing": "The single most important caveat — then answer it.",
            "cite": '<strong>Example Researcher</strong> (1st), Co-author. Venue Year. '
                    '<a href="#">link</a> · <a href="_research/paper-a.md">evidence</a>',
        },
    ],
    "list_rows": [
        ("20YY", '<a href="#">Paper B</a>', "Venue", "<strong>1st</strong>", "12"),
        ("20XX", '<a href="#">Paper A</a>', "Venue", "co-1st", "34"),
    ],
    "discuss": [
        "<strong>Question one?</strong> A prompt for the students.",
        "<strong>Question two?</strong> Another prompt.",
    ],
    "complete_html": '<p class="muted">A scope note: what these notes deliberately don’t cover, and why.</p>',
    "sources_html": '<p>Built from homepage + DBLP + arXiv; each paper deep-read into <a href="_research/">_research/</a>.</p>\n'
                    '  <div class="callout warn"><strong>Caveats:</strong> citation counts approximate; flag unverified items here.</div>',
}
