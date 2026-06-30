"""
DeepSpec / Speculative Decoding — notes.py
Research direction: how DeepSeek cut LLM inference latency 60–85% in production.
Covers the full arc from the original speculative decoding paper (2023) to DSpark (2026).
"""

NOTES = {
    "name": "DeepSpec",
    "title_suffix": "speculative decoding reading notes",
    "subtitle": "How DeepSeek made LLM inference 60–85% faster in production — and what it took to get there",
    "meta_html": "DeepSeek-AI &amp; Peking University &mdash; <a href=\"https://github.com/deepseek-ai/DeepSpec\">github.com/deepseek-ai/DeepSpec</a> &middot; released June 2026",
    "tags": ["Speculative Decoding", "LLM Inference", "Draft Model", "DeepSeek", "ICML 2026"],
    "who_heading": "What it is",
    "studynote_html": (
        "<p>This page covers <strong>speculative decoding</strong> &mdash; the technique behind DeepSeek&rsquo;s "
        "DeepSpec open-source framework. The big question: how do you serve an LLM 60–85% faster "
        "<em>without changing the model or its output</em>? The answer turns out to involve a clever trick "
        "about what transformers can do in parallel, and a surprising discovery that a tiny sequential correction "
        "on top of a parallel drafter is worth far more than making the drafter bigger.</p>"
        "<p>Reading order: <strong>Leviathan 2023</strong> (the idea) → <strong>EAGLE-3</strong> "
        "(autoregressive frontier) → <strong>DFlash</strong> (break the sequential wall) → "
        "<strong>DSpark</strong> (fix what breaks &amp; ship to production).</p>"
    ),
    "hook_html": (
        "<p class=\"lead\">The most interesting thing here is a <strong>counterintuitive empirical result</strong>: "
        "fully <em>parallel</em> draft models (DFlash) outperform fully <em>sequential</em> ones (EAGLE-3) "
        "on average accepted length &mdash; even though each parallel position ignores all the others. "
        "The reason is that the <em>first</em> draft position carries the highest leverage (a miss there "
        "throws away the entire block), and a parallel model can afford a much deeper architecture because "
        "its drafting time doesn’t grow with block size. DSpark&rsquo;s insight: get the depth advantage "
        "at position 1 <em>and</em> fix the dependency problem at positions 2–7 with a tiny sequential "
        "head that costs almost nothing. &ldquo;A little autoregression goes a long way.&rdquo;</p>"
    ),
    "stats": [
        ("5,054 stars", "GitHub stars at launch (June 2026)"),
        ("3 algorithms", "Eagle3, DFlash, DSpark — all in one training framework"),
        ("60–85%", "per-user speed gain vs MTP-1 baseline in DeepSeek-V4 production"),
        ("MIT license", "fully open-source, including checkpoints"),
    ],
    "edu_html": (
        "DeepSpec is an <strong>algorithm-driven training repository</strong> for speculative decoding draft models, "
        "open-sourced by DeepSeek-AI alongside the DeepSpark paper. It contains data preparation, training code, "
        "and evaluation scripts for three draft-model algorithms. The headline algorithm, <strong>DSpark</strong>, "
        "is currently deployed inside DeepSeek-V4 (Flash and Pro) serving real user traffic."
    ),
    "arc": [
        {
            "yr": "2022–23",
            "title": "Speculative decoding invented",
            "html": (
                "Leviathan, Kalman &amp; Matias (Google) show that a target transformer can <em>verify</em> "
                "γ candidate tokens in one forward pass &mdash; the same cost as generating 1. Use a cheap "
                "draft model to propose the candidates, run rejection sampling, and generation is 2–3× "
                "faster with <strong>identical output distribution</strong>. Accepted at ICML 2023 as an Oral. "
                "DeepMind’s Chen et al. independently reach the same idea (&ldquo;speculative sampling&rdquo;)."
            ),
        },
        {
            "yr": "2024",
            "title": "EAGLE: smarter autoregressive drafting",
            "html": (
                "Li et al. propose drafting at the <em>feature level</em> (predicting next hidden states, not "
                "next tokens), which gives tighter coupling to the target model. EAGLE-2 adds dynamic draft tree "
                "construction. Strong baseline, but autoregressive: T_draft ∝ γ."
            ),
        },
        {
            "yr": "2025",
            "title": "EAGLE-3: training-time test, scales with data",
            "html": (
                "The feature-prediction approach hits a ceiling: more training data doesn’t help because the "
                "feature distribution at inference differs from training. EAGLE-3 switches to direct token "
                "prediction, adds multi-layer feature fusion, and introduces <em>training-time test (TTT)</em> "
                "to close the train/test gap. Reaches ~6.5× speedup. Still autoregressive."
            ),
        },
        {
            "yr": "2026 (Jan)",
            "title": "DFlash: the sequential wall falls",
            "html": (
                "Chen, Liang &amp; Liu (ICML 2026) inject the target model’s hidden states into the draft "
                "model as KV context, then let all γ draft positions attend <em>bidirectionally</em> to "
                "each other and to the target context. Result: all γ tokens in a <strong>single forward "
                "pass</strong>. T_draft ≈ O(1) w.r.t. γ. Gains 2.5× over EAGLE-3. But without "
                "inter-token dependency, later positions suffer &ldquo;suffix decay.&rdquo;"
            ),
            "hl": True,
        },
        {
            "yr": "2026 (Jun)",
            "title": "DSpark: fix what breaks, ship to production",
            "html": (
                "DeepSeek-AI + Peking University release DSpark: (1) a semi-autoregressive head that adds "
                "intra-block dependency at near-zero latency cost on top of DFlash’s parallel backbone, "
                "and (2) a confidence-scheduled verifier that dynamically truncates low-confidence draft "
                "suffixes based on real-time engine load. Deployed in DeepSeek-V4. Open-sourced as DeepSpec. "
                "<strong>60–85% faster</strong> than MTP-1 baseline at matched throughput."
            ),
            "hl": True,
        },
    ],
    "start": [
        '<strong><a href="https://arxiv.org/abs/2211.17192">Leviathan et al. 2023</a></strong> &mdash; '
        "the original paper. Read the abstract and the algorithm once to internalize the draft/verify loop. "
        "The key equation: accept x<sub>k</sub> with probability min(1, p<sub>t</sub>(x<sub>k</sub>) / "
        "p<sub>d</sub>(x<sub>k</sub>)).",
        '<strong><a href="https://arxiv.org/abs/2602.06036">DFlash (Chen et al. 2026)</a></strong> &mdash; '
        "understand how KV injection makes a single-pass block drafter possible. Focus on Figure 1 and "
        "the H_ctx equation.",
        '<strong>DSpark paper</strong> (PDF in the <a href="https://github.com/deepseek-ai/DeepSpec">repo</a>) '
        "&mdash; Figure 1 (architecture overview), Section 3.1 (semi-autoregressive), Figure 2 "
        "(position-wise conditional acceptance), Section 3.2 (confidence scheduling), Table 1 (results).",
        '<strong>EAGLE-3 (<a href="https://arxiv.org/abs/2503.01840">arXiv:2503.01840</a>)</strong> &mdash; '
        "read after DSpark to understand why the autoregressive frontier plateaued and what TTT achieves.",
    ],
    "papers": [
        {
            "title_html": "Fast Inference from Transformers via Speculative Decoding",
            "badge": "foundational",
            "concept": "A cheap draft model proposes a block of tokens; the target model verifies all in one parallel pass and accepts the longest consistent prefix. Identical output, 2–3× faster.",
            "key_finding": "Transformer verification is <strong>free in parallel</strong>: verifying γ tokens costs the same as generating 1, so any cheap draft model that proposes plausible tokens yields a lossless speedup. On T5-XXL: <strong>2–3× faster</strong> with mathematically identical outputs.",
            "intro": (
                "Autoregressive decoding is a serial bottleneck: each token requires a full forward pass. "
                "The insight is that <em>verification</em> is much cheaper than <em>generation</em>: a "
                "target transformer can score all γ positions in parallel in one pass (the same cost "
                "as producing 1 token) by leveraging the fact that attention is already computed over all "
                "positions. So if a small, fast draft model can propose γ plausible candidates, we get "
                "γ tokens for the price of 1 verification."
            ),
            "method": (
                "<strong>Setup.</strong> You have a large target model M<sub>t</sub> and a much cheaper "
                "draft model M<sub>d</sub>. <strong>Baseline (standard decoding):</strong> "
                "<div class=\"formula\">L = T<sub>target</sub> &times; (number of tokens) <em>(one full forward pass per token)</em></div> "
                "<strong>What speculative decoding changes.</strong> Draft M<sub>d</sub> proposes a block "
                "x<sub>1</sub>,...,x<sub>γ</sub>. M<sub>t</sub> runs <em>one</em> forward pass, "
                "computing p<sub>t</sub>(x<sub>k</sub>) for all k simultaneously. Accept each token: "
                "<div class=\"formula\">accept x<sub>k</sub> with prob  min(1,  p<sub>t</sub>(x<sub>k</sub>) / p<sub>d</sub>(x<sub>k</sub>)) <em>(rejection sampling)</em></div> "
                "First rejection at k discards x<sub>k</sub>,...,x<sub>γ</sub>; M<sub>t</sub> "
                "always generates one bonus token. <strong>Why the output is identical:</strong> the "
                "accept/reject rule is exactly the Radon-Nikodym correction that recovers p<sub>t</sub>&rsquo;s "
                "distribution even when the draft is wrong. Latency per accepted token: "
                "L = (T<sub>draft</sub> + T<sub>verify</sub>) / τ, where τ = expected accepted "
                "tokens/cycle. Improving τ (better draft) or lowering T<sub>draft</sub> (faster draft) "
                "both help."
            ),
            "results": (
                "T5-XXL vs T5X baseline: <strong>2–3× speedup</strong>. Output distribution is "
                "mathematically identical (proven via rejection sampling theory). No model retraining. "
                "Works for any pair of models (no architectural constraint); practical speedup depends on "
                "the draft acceptance rate and the draft model’s cost."
            ),
            "discussion": (
                "The entire subsequent literature (EAGLE, DFlash, DSpark) is about answering: "
                "<em>how do you maximize τ at minimum T<sub>draft</sub>?</em> Tree-based verification "
                "(Miao et al. 2024) extends the idea by verifying multiple draft <em>paths</em> in one "
                "target pass."
            ),
            "figure": {
                "svg": '''<svg viewBox="0 0 700 170" xmlns="http://www.w3.org/2000/svg"><defs><marker id="sd1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#5b6776"/></marker><marker id="sd1g" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#3a7d44"/></marker><marker id="sd1r" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#b3402f"/></marker></defs><g font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="12" text-anchor="middle"><rect x="10" y="60" width="100" height="44" rx="9" fill="#eef2f6" stroke="#8a97a6"/><text x="60" y="80" font-weight="700">draft model</text><text x="60" y="95" font-size="10.5">(fast, small)</text><rect x="140" y="32" width="34" height="26" rx="5" fill="#ffe7b3" stroke="#e09f3e"/><text x="157" y="49" font-weight="700" font-size="11">x&#x2081;</text><rect x="182" y="32" width="34" height="26" rx="5" fill="#ffe7b3" stroke="#e09f3e"/><text x="199" y="49" font-weight="700" font-size="11">x&#x2082;</text><rect x="224" y="32" width="34" height="26" rx="5" fill="#ffe7b3" stroke="#e09f3e"/><text x="241" y="49" font-weight="700" font-size="11">x&#x2083;</text><rect x="266" y="32" width="46" height="26" rx="5" fill="#ffe7b3" stroke="#e09f3e"/><text x="289" y="49" font-weight="700" font-size="11">&#x2026; x&#x03b3;</text><line x1="110" y1="82" x2="138" y2="82" stroke="#5b6776" stroke-width="1.6" marker-end="url(#sd1)"/><line x1="110" y1="82" x2="138" y2="45" stroke="#5b6776" stroke-width="1.6" marker-end="url(#sd1)"/><text x="122" y="77" font-size="9.5" fill="#5b6776">propose</text><rect x="340" y="56" width="120" height="52" rx="9" fill="#cfe8f3" stroke="#2e86ab"/><text x="400" y="78" font-weight="700">target model</text><text x="400" y="93" font-size="10.5">1 forward pass</text><line x1="314" y1="45" x2="338" y2="72" stroke="#5b6776" stroke-width="1.6" marker-end="url(#sd1)"/><line x1="314" y1="82" x2="338" y2="82" stroke="#5b6776" stroke-width="1.6" marker-end="url(#sd1)"/><text x="326" y="65" font-size="9.5" fill="#5b6776">verify</text><rect x="500" y="30" width="80" height="26" rx="5" fill="#d6ecd2" stroke="#3a7d44"/><text x="540" y="47" font-size="11" font-weight="700">x&#x2081; x&#x2082; &#x2713;</text><rect x="500" y="66" width="80" height="26" rx="5" fill="#f6d9d4" stroke="#b3402f"/><text x="540" y="83" font-size="11" font-weight="700">x&#x2083; rejected</text><rect x="500" y="102" width="90" height="26" rx="5" fill="#d6ecd2" stroke="#3a7d44"/><text x="545" y="119" font-size="11" font-weight="700">bonus x* &#x2713;</text><line x1="460" y1="72" x2="498" y2="43" stroke="#3a7d44" stroke-width="1.6" marker-end="url(#sd1g)"/><line x1="460" y1="78" x2="498" y2="79" stroke="#b3402f" stroke-width="1.6" marker-end="url(#sd1r)"/><line x1="460" y1="82" x2="498" y2="115" stroke="#3a7d44" stroke-width="1.6" marker-end="url(#sd1g)"/><text x="400" y="148" font-size="11" fill="#5b6776" font-style="italic">accept prefix x&#x2081;x&#x2082; + target bonus &#x2192; 3 tokens for the cost of 1 verification</text></g></svg>''',
                "caption": "Speculative decoding loop: the draft model proposes a block of &#x03b3; candidate tokens; the target model scores all in one parallel pass; the longest accepted prefix + one bonus token are kept. Output is identical to sampling from the target directly."
            },
            "missing": (
                "Speedup is limited by the draft acceptance rate &tau;, which depends entirely on draft "
                "quality. If the draft is bad (low &tau;), the verification overhead dominates and you "
                "can slow down vs greedy decoding. The paper doesn&rsquo;t solve the draft-quality "
                "problem &mdash; that&rsquo;s what EAGLE, DFlash, and DSpark are about."
            ),
            "cite": (
                'Yaniv Leviathan, Matan Kalman, Yossi Matias (Google). '
                '<em>Fast Inference from Transformers via Speculative Decoding.</em> '
                'ICML 2023 (Oral). <a href="https://arxiv.org/abs/2211.17192">arXiv:2211.17192</a> '
                '&middot; <a href="_research/leviathan2023.md">evidence</a>'
            ),
        },
        {
            "title_html": "EAGLE-3: Scaling up Inference Acceleration via Training-Time Test",
            "badge": "autoregressive frontier",
            "concept": "Direct token prediction + multi-layer feature fusion + a training-time test technique that closes the train/test distribution gap — lets the draft model scale with more data, reaching ~6.5× speedup.",
            "key_finding": "Switching from <strong>feature prediction to token prediction</strong>, fusing hidden states from <strong>multiple target layers</strong>, and bridging the train/test gap with <em>training-time test (TTT)</em> lets the draft model finally scale with more data: <strong>up to 6.5×</strong> speedup and ~<strong>1.4×</strong> over EAGLE-2.",
            "intro": (
                "EAGLE (2024) drafts by predicting the target&rsquo;s next <em>hidden state</em> (feature-level "
                "autoregression). Problem: the hidden-state distribution at inference differs from training "
                "(the model hasn&rsquo;t seen the specific prompt&rsquo;s features during training). More "
                "data hits diminishing returns. EAGLE-3 rethinks the prediction target: draft directly in "
                "<em>token space</em>, use multi-layer features, and make training look like inference."
            ),
            "method": (
                "<strong>Setup.</strong> An autoregressive draft model conditions each position on all "
                "previously <em>sampled</em> tokens, giving high quality at later positions &mdash; "
                "but T<sub>draft</sub> ∝ γ, forcing small block sizes. "
                "<strong>Three changes in EAGLE-3:</strong> "
                "<strong>(1) Token prediction</strong>: the draft model predicts the next token id directly, "
                "not the next hidden state: "
                "<div class=\"formula\">p(x<sub>k+1</sub> | x<sub>≤k</sub>, H<sub>multi</sub>) <em>(token-space, not feature-space)</em></div> "
                "<strong>(2) Multi-layer fusion</strong>: feed hidden states from multiple target layers "
                "H<sub>multi</sub> = [H<sup>(l<sub>1</sub>)</sup>;...;H<sup>(l<sub>m</sub>)</sup>] so "
                "the draft sees richer representations. "
                "<strong>(3) Training-Time Test (TTT)</strong>: during training, augment the input features "
                "to simulate the inference-time distribution &mdash; specifically, at TTT horizon T=7, the "
                "draft model is also conditioned on its <em>own previous outputs</em> from earlier timesteps "
                "(as it would be at test time). This closes the train/test gap and allows more training "
                "data to actually improve accuracy."
            ),
            "results": (
                "Up to <strong>6.5× speedup</strong> on diverse benchmarks, ~<strong>1.4×</strong> "
                "over EAGLE-2. In the DeepSpec comparison (Table 1, same setup as DFlash/DSpark): "
                "Qwen3-4B GSM8K τ = 5.14, MATH500 = 4.62 &mdash; strong on structured tasks, "
                "weaker on chat (MT-Bench = 2.39, Alpaca = 2.26). Still slower than DFlash/DSpark "
                "because T<sub>draft</sub> ∝ γ."
            ),
            "discussion": (
                "EAGLE-3 represents the practical ceiling for <em>autoregressive</em> drafters. The "
                "TTT insight (making training look like inference) is reusable beyond EAGLE. "
                "Whether the token-vs-feature question matters more than architecture depth remains open."
            ),
            "figure": {
                "svg": '''<svg viewBox="0 0 680 150" xmlns="http://www.w3.org/2000/svg"><defs><marker id="e3a" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#5b6776"/></marker></defs><g font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="12" text-anchor="middle"><rect x="10" y="52" width="96" height="52" rx="9" fill="#eef2f6" stroke="#8a97a6"/><text x="58" y="74" font-weight="700">target model</text><text x="58" y="89" font-size="10">multiple layers</text><rect x="132" y="30" width="88" height="26" rx="7" fill="#ffe7b3" stroke="#e09f3e"/><text x="176" y="47" font-weight="700" font-size="11">H&#x207F;&#x207F;&#x207F; = top layer</text><rect x="132" y="62" width="88" height="26" rx="7" fill="#ffe7b3" stroke="#e09f3e"/><text x="176" y="79" font-weight="700" font-size="11">H&#x207F; = mid layer</text><rect x="132" y="94" width="88" height="26" rx="7" fill="#ffe7b3" stroke="#e09f3e"/><text x="176" y="111" font-weight="700" font-size="11">H&#x2081; = low layer</text><g stroke="#5b6776" stroke-width="1.5" fill="none"><line x1="106" y1="75" x2="130" y2="43" marker-end="url(#e3a)"/><line x1="106" y1="78" x2="130" y2="75" marker-end="url(#e3a)"/><line x1="106" y1="81" x2="130" y2="107" marker-end="url(#e3a)"/></g><rect x="242" y="52" width="96" height="52" rx="9" fill="#e9e1f4" stroke="#6a4c93"/><text x="290" y="74" font-weight="700">fusion</text><text x="290" y="89" font-size="10">concat + project</text><g stroke="#5b6776" stroke-width="1.5" fill="none"><line x1="220" y1="43" x2="240" y2="70" marker-end="url(#e3a)"/><line x1="220" y1="75" x2="240" y2="76" marker-end="url(#e3a)"/><line x1="220" y1="107" x2="240" y2="82" marker-end="url(#e3a)"/></g><rect x="368" y="52" width="128" height="52" rx="9" fill="#cfe8f3" stroke="#2e86ab"/><text x="432" y="71" font-weight="700">draft model</text><text x="432" y="85" font-size="10">autoregressive</text><text x="432" y="99" font-size="10">token prediction</text><line x1="338" y1="78" x2="366" y2="78" stroke="#5b6776" stroke-width="1.5" marker-end="url(#e3a)"/><rect x="526" y="52" width="140" height="52" rx="9" fill="#d6ecd2" stroke="#3a7d44"/><text x="596" y="70" font-weight="700">draft tokens</text><text x="596" y="85" font-size="10">x&#x2081;, x&#x2082;, ... x&#x03b3;</text><text x="596" y="99" font-size="10">(sequential)</text><line x1="496" y1="78" x2="524" y2="78" stroke="#5b6776" stroke-width="1.5" marker-end="url(#e3a)"/><text x="340" y="136" font-size="10.5" fill="#5b6776" font-style="italic">TTT: training sees augmented features matching inference distribution</text></g></svg>''',
                "caption": "EAGLE-3 extracts hidden states from multiple target layers, fuses them, and feeds the result to an autoregressive draft model that predicts token ids (not features). Training-time test (TTT) augments training inputs to match inference-time feature distributions."
            },
            "missing": (
                "EAGLE-3 is still autoregressive: T<sub>draft</sub> grows linearly with block size γ, "
                "forcing block sizes around 4–7 to keep drafting latency low. DFlash and DSpark can "
                "afford γ=16 or more at the same latency budget. This is the fundamental gap, "
                "not a deficit in TTT or multi-layer fusion."
            ),
            "cite": (
                'Yuhui Li, Fangyun Wei, Chao Zhang, Hongyang Zhang. '
                '<em>EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test.</em> '
                'arXiv 2025. <a href="https://arxiv.org/abs/2503.01840">arXiv:2503.01840</a> '
                '&middot; <a href="_research/eagle3.md">evidence</a>'
            ),
        },
        {
            "title_html": "DFlash: Block Diffusion for Flash Speculative Decoding",
            "badge": "ICML 2026",
            "concept": "Inject the target model's hidden states into the draft model as KV context, then let all γ draft positions attend bidirectionally in one forward pass — O(1) drafting time regardless of block size.",
            "key_finding": "By conditioning the draft on the target&rsquo;s own hidden states (KV injection) and generating all tokens via a <strong>single bidirectional forward pass</strong>, DFlash achieves <strong>&gt;6× lossless speedup</strong> and <strong>2.5× over EAGLE-3</strong> &mdash; but acceptance decays at later block positions because no token depends on the ones before it.",
            "intro": (
                "The sequential wall in autoregressive drafting: T<sub>draft</sub> ∝ γ, so you can&rsquo;t "
                "afford large blocks. DFlash breaks this by making the draft model a <em>block diffusion model</em>: "
                "all positions are predicted simultaneously in one pass. The key enabling idea is "
                "<strong>KV injection</strong> &mdash; rich context features extracted from the target model "
                "are injected into the draft model&rsquo;s key-value pairs, so the draft knows what the "
                "target would have attended to, even without conditioning on previously sampled tokens."
            ),
            "method": (
                "<strong>Setup.</strong> Target model runs prefill, producing hidden states "
                "H<sup>(l<sub>1</sub>)</sup>,...,H<sup>(l<sub>m</sub>)</sup> at layers l<sub>1</sub>,...,l<sub>m</sub>. "
                "<strong>Baseline (autoregressive drafter):</strong> "
                "<div class=\"formula\">x<sub>k</sub> = draft(x<sub>1</sub>,...,x<sub>k-1</sub>) &nbsp; &rarr; &nbsp; T<sub>draft</sub> ∝ γ</div> "
                "<strong>What DFlash changes.</strong> Compress the target&rsquo;s hidden states into a "
                "context summary, inject into draft&rsquo;s attention as additional K, V: "
                "<div class=\"formula\">H<sub>ctx</sub> = RMSNorm( W<sub>c</sub> [H<sup>(l<sub>1</sub>)</sup>; … ;H<sup>(l<sub>m</sub>)</sup>] )</div>"
                "<div class=\"formula\">K<sub>i</sub> = [W<sub>i</sub><sup>K</sup> H<sub>ctx</sub> ; W<sub>i</sub><sup>K</sup> H<sub>d</sub>], &nbsp; V<sub>i</sub> = [W<sub>i</sub><sup>V</sup> H<sub>ctx</sub> ; W<sub>i</sub><sup>V</sup> H<sub>d</sub>]</div>"
                "Feed anchor token + γ mask tokens; all draft positions attend "
                "<em>bidirectionally</em> to each other and to H<sub>ctx</sub>. Single forward pass "
                "→ all γ logits simultaneously. T<sub>draft</sub> ≈ O(1) w.r.t. γ. "
                "<strong>Why KV injection is the enabling trick:</strong> without it, each position has no "
                "information about what the target actually computed &mdash; the context summary H<sub>ctx</sub> "
                "gives the draft a strong prior so it can predict well even without seeing other draft tokens."
            ),
            "results": (
                "<strong>&gt;6× lossless acceleration</strong> across diverse models/tasks. "
                "<strong>Up to 2.5× over EAGLE-3</strong>. DeepSpec Table 1: Qwen3-4B GSM8K "
                "τ = 5.40 (vs Eagle3 5.14), Arena-Hard τ = 2.83 (vs Eagle3 2.55). "
                "DFlash consistently beats EAGLE-3 despite per-position independence, because the "
                "<em>first</em> position has much higher capacity (deeper network, O(1) cost)."
            ),
            "discussion": (
                "The suffix-decay limitation (Fig 2 in DSpark): DFlash&rsquo;s conditional acceptance "
                "rate drops from 0.88 to 0.78 by position 7 on Code, and 0.72 to 0.63 on Chat, "
                "because later positions marginalize over all possible preceding tokens instead of "
                "conditioning on the one actually sampled. This motivates DSpark&rsquo;s sequential head."
            ),
            "figure": {
                "svg": '''<svg viewBox="0 0 680 180" xmlns="http://www.w3.org/2000/svg"><defs><marker id="df1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#5b6776"/></marker></defs><g font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="12" text-anchor="middle"><rect x="10" y="66" width="96" height="50" rx="9" fill="#eef2f6" stroke="#8a97a6"/><text x="58" y="88" font-weight="700">target model</text><text x="58" y="103" font-size="10">(prefill)</text><rect x="134" y="58" width="100" height="34" rx="7" fill="#ffe7b3" stroke="#e09f3e"/><text x="184" y="79" font-weight="700" font-size="11">H<tspan font-size="9">ctx</tspan> (KV)</text><line x1="106" y1="91" x2="132" y2="75" stroke="#5b6776" stroke-width="1.6" marker-end="url(#df1)"/><rect x="10" y="128" width="96" height="34" rx="9" fill="#f4f4f4" stroke="#9aa4af"/><text x="58" y="148" font-size="11" fill="#5b6776">anchor + &#x03b3; masks</text><rect x="248" y="46" width="200" height="106" rx="10" fill="#cfe8f3" stroke="#2e86ab"/><text x="348" y="68" font-weight="700">draft model (bidirectional)</text><text x="348" y="84" font-size="10.5">all positions attend to each other</text><text x="348" y="99" font-size="10.5">AND to H<tspan font-size="9">ctx</tspan></text><text x="348" y="114" font-size="10.5">ONE forward pass</text><line x1="134" y1="75" x2="246" y2="75" stroke="#5b6776" stroke-width="1.6" marker-end="url(#df1)"/><line x1="106" y1="145" x2="246" y2="125" stroke="#5b6776" stroke-width="1.6" marker-end="url(#df1)"/><rect x="478" y="66" width="186" height="50" rx="9" fill="#d6ecd2" stroke="#3a7d44"/><text x="571" y="87" font-weight="700">x&#x2081; x&#x2082; x&#x2083; ... x&#x03b3;</text><text x="571" y="102" font-size="10.5">all tokens, 1 pass</text><line x1="448" y1="99" x2="476" y2="91" stroke="#5b6776" stroke-width="1.6" marker-end="url(#df1)"/><text x="348" y="168" font-size="10.5" fill="#5b6776" font-style="italic">T<tspan font-size="9">draft</tspan> &#x2248; O(1) w.r.t. &#x03b3; &#x2014; but no inter-token dependency &#x2192; suffix decay</text></g></svg>''',
                "caption": "DFlash injects the target model&rsquo;s hidden states as KV context into the draft model, then runs a single bidirectional forward pass over the anchor token + &#x03b3; mask positions. All &#x03b3; draft logits are produced simultaneously. The trade-off: each position doesn&rsquo;t know what the others sampled &rarr; suffix decay."
            },
            "missing": (
                "Suffix decay is the key unresolved problem: because positions are independent, each "
                "marginalizes over all possible preceding tokens rather than the one actually sampled. "
                "Multi-modal collisions (&ldquo;of course&rdquo; vs &ldquo;no course&rdquo;) push later "
                "positions toward contradictory predictions. DSpark&rsquo;s contribution is a fix for "
                "exactly this. Also: DFlash requires its KV-injection setup to be compatible with the "
                "target model&rsquo;s layer structure &mdash; cross-architecture transfer is not addressed."
            ),
            "cite": (
                'Jian Chen, Yesheng Liang, Zhijian Liu. '
                '<em>DFlash: Block Diffusion for Flash Speculative Decoding.</em> '
                'ICML 2026. <a href="https://arxiv.org/abs/2602.06036">arXiv:2602.06036</a> '
                '&middot; <a href="_research/dflash.md">evidence</a>'
            ),
        },
        {
            "title_html": "DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation",
            "badge": "DeepSeek 2026",
            "concept": "Combine DFlash's fast parallel backbone with a lightweight sequential head that injects intra-block dependency — then add a confidence-based verifier that dynamically prunes the draft block to maximize system throughput. Deployed in DeepSeek-V4.",
            "key_finding": "A tiny sequential correction on top of DFlash&rsquo;s parallel backbone raises macro-average accepted length by <strong>+16–18%</strong> vs DFlash and <strong>+27–31%</strong> vs Eagle3, while a confidence scheduler routes verification compute only to tokens likely to survive &mdash; together achieving <strong>60–85% faster</strong> per-user generation in DeepSeek-V4 production.",
            "intro": (
                "DFlash showed that parallel drafting beats autoregressive drafting on average. But "
                "Figure 2 in the DSpark paper reveals a clean mechanistic story: DFlash wins at "
                "<em>position 1</em> (deeper architecture, ~0.88 vs Eagle3&rsquo;s 0.81 on Math) "
                "but loses by positions 2–7 (acceptance decays to 0.78 on Code, while Eagle3 "
                "is stable or rising). DSpark&rsquo;s design question: can we get DFlash&rsquo;s "
                "capacity advantage at position 1 <em>plus</em> Eagle3&rsquo;s dependency quality "
                "at later positions, without making the drafter slow? Answer: yes &mdash; the "
                "sequential correction is so cheap it barely changes T<sub>draft</sub>."
            ),
            "method": (
                "<strong>Setup.</strong> Starting from DFlash as the parallel backbone: one forward "
                "pass produces hidden states h<sub>1</sub>,...,h<sub>γ</sub> and base logits "
                "U<sub>1</sub>,...,U<sub>γ</sub>. The base logits treat each position "
                "independently (no dependency). <strong>Component 1: Semi-autoregressive generation.</strong> "
                "Add a lightweight sequential head that computes a prefix-dependent transition bias "
                "B<sub>k</sub>(x<sub>0</sub>, x<sub>&lt;k</sub>, x<sub>k</sub>), blending it with "
                "the parallel logits: "
                "<div class=\"formula\">p<sub>k</sub>(v | x<sub>0</sub>, x<sub>&lt;k</sub>) = softmax( U<sub>k</sub>(v) + B<sub>k</sub>(x<sub>0</sub>, x<sub>&lt;k</sub>, v) )</div>"
                "The <strong>Markov head</strong> variant: B(x<sub>k−1</sub>, &middot;) = W<sub>1</sub>[x<sub>k−1</sub>]·W<sub>2</sub> "
                "(low-rank r=256 embedding lookup + projection). Just looking up one token and adding "
                "a bias &mdash; negligible latency. The <strong>RNN head</strong> variant keeps a "
                "recurrent state s<sub>k</sub> for full history: "
                "<div class=\"formula\">s<sub>k</sub> = σ(W<sub>g</sub>z<sub>k</sub>) &odot; s<sub>k-1</sub> + (1−σ(W<sub>g</sub>z<sub>k</sub>)) &odot; tanh(W<sub>c</sub>z<sub>k</sub>)</div>"
                "A <strong>2-layer DSpark outperforms a 5-layer DFlash</strong> (Figure 3): "
                "sequential modeling is more parameter-efficient than parallel depth. "
                "<strong>Component 2: Confidence-scheduled verification.</strong> "
                "A confidence head predicts P(token k survives | prefix accepted): "
                "<div class=\"formula\">c<sub>k</sub> = σ( w<sup>&#x22a4;</sup> [h<sub>k</sub> ; W<sub>1</sub>[x<sub>k-1</sub>]] )</div>"
                "Prefix survival probability: a<sub>r,j</sub> = ∏<sub>i≤j</sub> c<sub>r,i</sub>. "
                "The hardware-aware prefix scheduler then picks per-request verification lengths "
                "ℓ<sub>1</sub>,...,ℓ<sub>R</sub> to maximize system throughput: "
                "<div class=\"formula\">maximize Θ = τ &times; SPS(B) &nbsp;&nbsp; where &nbsp; "
                "τ = &Sigma;<sub>r</sub>(1 + &Sigma;<sub>j≤ℓ<sub>r</sub></sub> a<sub>r,j</sub>), &nbsp; "
                "B = &Sigma;<sub>r</sub>(1 + ℓ<sub>r</sub>)</div>"
                "SPS(B) is the engine&rsquo;s profiled throughput curve (steps/sec vs batch size). "
                "Greedy solution: sort all (request, position) candidates by survival probability "
                "a<sub>r,j</sub> descending; admit until Θ stops improving. "
                "Sequential Temperature Scaling calibrates c<sub>k</sub> position-by-position so "
                "the cumulative product accurately reflects true acceptance probability."
            ),
            "results": (
                "<strong>Offline (Table 1, no confidence scheduler):</strong> vs DFlash on Qwen3-4B &mdash; "
                "GSM8K: <strong>6.11 vs 5.40</strong>; MBPP: <strong>5.13 vs 4.40</strong>; "
                "MT-Bench: <strong>3.64 vs 3.07</strong>. Macro-avg improvement: "
                "+16.3% (4B), +18.4% (8B), +18.3% (14B) over DFlash; "
                "+30.9%, +26.7%, +30.0% over Eagle3. "
                "<strong>Production (DeepSeek-V4 live traffic):</strong> "
                "vs MTP-1 baseline: <strong>60–85% faster</strong> per-user generation at matched "
                "throughput. Enables SLA tiers (120 TPS Flash, 50 TPS Pro) that were "
                "previously unattainable. Shifts the Pareto frontier of LLM serving."
            ),
            "discussion": (
                "The production results are the most important: DSpark doesn&rsquo;t just improve "
                "a benchmark metric, it shifts the <em>feasibility frontier</em> &mdash; performance "
                "tiers that were impossible before become achievable. The confidence scheduler is "
                "why: under high concurrency, verifying low-confidence suffix tokens wastes batch "
                "capacity that could serve other requests; adaptive truncation recovers that capacity. "
                "All evaluation uses non-thinking mode; thinking mode (chain-of-thought) deferred."
            ),
            "figure": {
                "svg": '''<svg viewBox="0 0 700 220" xmlns="http://www.w3.org/2000/svg"><defs><marker id="dsp1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#5b6776"/></marker><marker id="dsp1g" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#3a7d44"/></marker><marker id="dsp1r" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#b3402f"/></marker></defs><g font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="11.5" text-anchor="middle"><text x="180" y="18" font-size="10.5" fill="#2e86ab" font-weight="700">&#x2460; Parallel backbone (DFlash)</text><rect x="10" y="28" width="108" height="50" rx="9" fill="#cfe8f3" stroke="#2e86ab"/><text x="64" y="50" font-weight="700">DFlash block</text><text x="64" y="64" font-size="10">h&#x2081;...h&#x03b3;, U&#x2081;...U&#x03b3;</text><text x="64" y="78" font-size="9.5">1 forward pass</text><text x="310" y="18" font-size="10.5" fill="#6a4c93" font-weight="700">&#x2461; Sequential head (Markov)</text><rect x="154" y="28" width="132" height="50" rx="9" fill="#e9e1f4" stroke="#6a4c93"/><text x="220" y="48" font-weight="700">B<tspan font-size="9">k</tspan>(x<tspan font-size="9">k-1</tspan>, &#xB7;)</text><text x="220" y="62" font-size="10">= W&#x2081;[x<tspan font-size="9">k-1</tspan>]W&#x2082;</text><text x="220" y="76" font-size="9.5">lightweight per-step</text><line x1="118" y1="53" x2="152" y2="53" stroke="#5b6776" stroke-width="1.6" marker-end="url(#dsp1)"/><rect x="312" y="28" width="142" height="50" rx="9" fill="#fff3cd" stroke="#e09f3e"/><text x="383" y="48" font-weight="700">draft tokens</text><text x="383" y="62" font-size="10">p<tspan font-size="9">k</tspan>(v) = softmax(U<tspan font-size="9">k</tspan>+B<tspan font-size="9">k</tspan>)</text><text x="383" y="76" font-size="9.5">dependency restored</text><line x1="286" y1="53" x2="310" y2="53" stroke="#5b6776" stroke-width="1.6" marker-end="url(#dsp1)"/><text x="560" y="18" font-size="10.5" fill="#3a7d44" font-weight="700">&#x2462; Confidence head</text><rect x="482" y="28" width="126" height="50" rx="9" fill="#d6ecd2" stroke="#3a7d44"/><text x="545" y="48" font-weight="700">c<tspan font-size="9">k</tspan> = &#x03c3;(w&#x22a4;[h<tspan font-size="9">k</tspan>;emb])</text><text x="545" y="62" font-size="10">survival prob</text><text x="545" y="76" font-size="9.5">per position</text><line x1="454" y1="53" x2="480" y2="53" stroke="#5b6776" stroke-width="1.6" marker-end="url(#dsp1)"/><line x1="0" y1="100" x2="700" y2="100" stroke="#e3e8ee" stroke-width="1"/><text x="350" y="120" font-size="10.5" fill="#5b6776" font-weight="700">&#x2463; Hardware-Aware Prefix Scheduler: maximize &#x0398; = &#x03c4; &#xD7; SPS(B)</text><rect x="10" y="132" width="136" height="64" rx="9" fill="#f3f7fb" stroke="#8a97a6"/><text x="78" y="152" font-weight="700">req 1: c&#x2081;c&#x2082;c&#x2083;c&#x2084;</text><text x="78" y="167" font-size="10">survival: a&#x2081;,&#x2081;..a&#x2081;,&#x2084;</text><text x="78" y="182" font-size="10">&#x2113;&#x2081;* = 3 (drop c&#x2084;)</text><rect x="156" y="132" width="136" height="64" rx="9" fill="#f3f7fb" stroke="#8a97a6"/><text x="224" y="152" font-weight="700">req 2: c&#x2081;c&#x2082;c&#x2083;c&#x2084;</text><text x="224" y="167" font-size="10">low-conf suffix</text><text x="224" y="182" font-size="10">&#x2113;&#x2082;* = 2 (drop c&#x2083;c&#x2084;)</text><rect x="310" y="132" width="106" height="64" rx="9" fill="#fdeef0" stroke="#b3402f"/><text x="363" y="157" font-size="10.5" fill="#b3402f">wasted verify</text><text x="363" y="172" font-size="10">occupies batch</text><text x="363" y="187" fill="#b3402f" font-size="10">capacity</text><rect x="436" y="132" width="122" height="64" rx="9" fill="#d6ecd2" stroke="#3a7d44"/><text x="497" y="157" font-weight="700">saved capacity</text><text x="497" y="171" font-size="10">serve more users</text><text x="497" y="185" font-size="10">same throughput</text><line x1="316" y1="164" x2="434" y2="164" stroke="#3a7d44" stroke-width="2" stroke-dasharray="5 3" marker-end="url(#dsp1g)"/><text x="375" y="158" font-size="9.5" fill="#3a7d44">scheduler prunes</text></g></svg>''',
                "caption": "DSpark architecture: &#x2460; DFlash parallel backbone (one pass, all positions). &#x2461; Lightweight sequential head adds a transition bias based on the previous sampled token (Markov) or full history (RNN), restoring intra-block dependency. &#x2462; Confidence head estimates per-position survival probability. &#x2463; Hardware-aware scheduler prunes low-confidence suffix tokens across all concurrent requests to maximize total system throughput."
            },
            "missing": (
                "Production results are compelling but not controlled: the comparison is vs the prior "
                "MTP-1 baseline, not vs DFlash or Eagle3 under the same serving setup. Also: all results "
                "are in <em>non-thinking mode</em>; thinking-mode (chain-of-thought) performance is "
                "explicitly deferred. The scheduler&rsquo;s greedy optimality relies on the SPS(B) curve "
                "being unimodal (smoothly decreasing); non-smooth hardware profiles and asynchronous "
                "pipelines require additional engineering (Appendix A)."
            ),
            "cite": (
                'Xin Cheng, Xingkai Yu, Chenze Shao, Jiashi Li, Yunfan Xiong, et al. (Peking Univ + DeepSeek-AI). '
                '<em>DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation.</em> '
                '2026. <a href="https://github.com/deepseek-ai/DeepSpec">GitHub/deepseek-ai/DeepSpec</a> '
                '(DSpark_paper.pdf) &middot; <a href="_research/dspark.md">evidence</a>'
            ),
        },
    ],
    "list_rows": [
        ("2026", '<a href="https://github.com/deepseek-ai/DeepSpec">DSpark (DeepSpec codebase)</a>',
         "DeepSeek (production + open-source)", "Xin Cheng, Xingkai Yu, et al.", "—"),
        ("2026", '<a href="https://arxiv.org/abs/2602.06036">DFlash: Block Diffusion for Flash Speculative Decoding</a>',
         "ICML 2026", "Jian Chen, Yesheng Liang, Zhijian Liu", "—"),
        ("2025", '<a href="https://arxiv.org/abs/2503.01840">EAGLE-3: Scaling up Inference Acceleration via TTT</a>',
         "arXiv 2025", "Yuhui Li, Fangyun Wei, Chao Zhang, Hongyang Zhang", "—"),
        ("2024", "EAGLE-2: Dynamic Draft Tree Structure for Efficient Retrieval",
         "EMNLP 2024", "Yuhui Li et al.", "~500"),
        ("2024", "EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty",
         "ICML 2024", "Yuhui Li, Fangyun Wei, Chao Zhang, Hongyang Zhang", "~600"),
        ("2024", "SpecInfer / tree-based speculative decoding (Miao et al.)",
         "ASPLOS 2024", "Xupeng Miao et al.", "~400"),
        ("2023", '<a href="https://arxiv.org/abs/2302.01318">Speculative Sampling (DeepMind)</a>',
         "arXiv 2023", "Charlie Chen, Sebastian Borgeaud, et al. (DeepMind)", "~1000"),
        ("2023", '<a href="https://arxiv.org/abs/2211.17192">Fast Inference via Speculative Decoding (Google)</a>',
         "ICML 2023 (Oral)", "Yaniv Leviathan, Matan Kalman, Yossi Matias", "~1500"),
    ],
    "discuss": [
        "The DSpark paper shows a 2-layer DSpark outperforms a 5-layer DFlash. What does this tell us about the relative "
        "value of depth (more parameters) vs inter-token dependency modeling? Is there a general lesson here for architecture design?",
        "The confidence scheduler maximizes Ψ = τ &times; SPS(B) subject to a non-anticipating constraint. "
        "Why does losslessness require the non-anticipating property? What would go wrong if the scheduler could look "
        "at all draft tokens before deciding verification lengths?",
        "DFlash generates all γ tokens bidirectionally in one pass. EAGLE-3 generates them autoregressively left-to-right. "
        "For which types of tasks do you expect each approach to have a larger advantage &mdash; and why? "
        "(Hint: think about whether the task’s structure makes later tokens predictable from earlier ones.)",
        "DSpark is deployed in DeepSeek-V4 serving real user traffic but evaluated only in non-thinking mode. "
        "What challenges do you anticipate for applying confidence-scheduled verification to chain-of-thought "
        "(thinking mode) outputs, where early rejection of a reasoning step could have outsized downstream consequences?",
        "The hardware-aware scheduler uses a pre-profiled SPS(B) curve. How should the scheduler be adapted "
        "if the serving system has heterogeneous hardware (different GPU types with different SPS curves) "
        "across requests in the same batch?",
    ],
    "complete_html": (
        "<p>These notes cover the <strong>draft-model design</strong> axis of speculative decoding. Not covered:</p>"
        "<ul>"
        "<li><strong>Tree-based verification</strong> (SpecInfer, Miao et al. 2024): verifying multiple draft paths "
        "in one target pass &mdash; orthogonal to draft quality and composable with DSpark.</li>"
        "<li><strong>Draft model training data</strong>: DeepSpec uses Open-PerfectBlend in non-thinking mode; "
        "the effect of thinking-mode training data is deferred in the paper.</li>"
        "<li><strong>Cross-architecture portability</strong>: DSpark/DFlash inherit KV-injection coupling to the "
        "target&rsquo;s layer structure. How to transfer across architectures is not addressed.</li>"
        "<li><strong>Draft model compression</strong>: quantizing the draft model to reduce T_draft further.</li>"
        "<li><strong>Medusa and variants</strong>: parallel draft heads on top of the target model itself "
        "(no separate draft model).</li>"
        "</ul>"
        "<p>Citation counts for 2025–2026 papers are not yet reliable; only 2023–2024 counts are cited above.</p>"
    ),
    "sources_html": (
        "<ul>"
        "<li><strong>DSpark paper</strong>: PDF read directly from <a href=\"https://github.com/deepseek-ai/DeepSpec\">deepseek-ai/DeepSpec</a> "
        "(pages 1–13). All numbers cross-checked against the paper text. "
        "<a href=\"_research/dspark.md\">evidence file</a></li>"
        "<li><strong>DFlash</strong>: abstract and key claims from <a href=\"https://arxiv.org/abs/2602.06036\">arXiv:2602.06036</a>. "
        "<a href=\"_research/dflash.md\">evidence file</a></li>"
        "<li><strong>EAGLE-3</strong>: abstract and key claims from <a href=\"https://arxiv.org/abs/2503.01840\">arXiv:2503.01840</a>. "
        "<a href=\"_research/eagle3.md\">evidence file</a></li>"
        "<li><strong>Leviathan et al. 2023</strong>: abstract from <a href=\"https://arxiv.org/abs/2211.17192\">arXiv:2211.17192</a>. "
        "<a href=\"_research/leviathan2023.md\">evidence file</a></li>"
        "<li><strong>Citation counts</strong>: not fetched (Google Scholar unreliable from automation); "
        "2023–2024 figures are estimates from Semantic Scholar. 2025–2026 papers marked —.</li>"
        "<li><strong>Production numbers</strong> (60–85%): from DSpark paper abstract and Section 5 (deployed on DeepSeek-V4).</li>"
        "</ul>"
    ),
}
