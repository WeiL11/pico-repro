"""Spec for build_notes.py — Rana M. Shahroz Khan. Generated page: index.html
Run: python tools/build_notes.py rana-shahroz-khan/notes.py
Content from the Pass-2 deep-reads in _research/ + Pass-1 map + the completeness/quality critic."""

_HP = 'https://rana-shahroz.github.io/'

NOTES = {
    "name": "Rana M. Shahroz Khan",
    "subtitle": "A guided tour of an efficient-ML / NLP researcher: what he keeps trying to solve, the arc, and what to read first.",
    "meta_html": (f'PhD student, UNC Chapel Hill (CS), advised by <strong>Tianlong Chen</strong>; '
                  f'<strong>Anthropic Research Fellow</strong> (May 2026–present). Undergrad: Vanderbilt (Soheil Kolouri lab). '
                  f'<a href="{_HP}" style="color:#bfe0f2">homepage</a> · '
                  f'<a href="https://dblp.org/pid/339/7435.html" style="color:#bfe0f2">DBLP</a> · '
                  f'<a href="https://scholar.google.com/citations?user=pdmMa3UAAAAJ" style="color:#bfe0f2">Scholar</a>'),
    "tags": ["LLM efficiency", "LoRA / PEFT", "multi-agent LLM safety", "reward-free fine-tuning"],
    "studynote_html": (
        '<p>Reading notes on <strong>Rana M. Shahroz Khan</strong>. Read the <a href="#arc">arc</a> first to see how the work '
        'connects, then use <a href="#start">&ldquo;Start here&rdquo;</a> for a reading order. Each paper folds open into a full '
        'Intro / Method / Results / Future breakdown with a &ldquo;what&rsquo;s missing&rdquo; box.</p>\n'
        '  <p class="muted">🛠 How these were researched &amp; built (v0.7 method, evidence in <a href="_research/">_research/</a>): '
        '<a href="methodology.html">methodology.html</a>.</p>'),
    "hook_html": (
        '<p class="lead">One agenda runs through his papers: <strong>make large models cheap to adapt &mdash; and stress-test '
        'where adaptation and coordination break.</strong> Three works are about <em>cheap / portable / generated</em> adaptation '
        '(<a href="#papers">PortLLM</a>, <a href="#papers">ORAL</a>, and CAR-LoRA all live in the LoRA + &ldquo;evolving LLMs&rdquo; '
        'world); the others push the same efficiency instinct into <em>trustworthiness</em> (<a href="#papers">Agents Under Siege</a>) '
        'and <em>reward-free training</em> (<a href="#papers">TMS</a>).</p>\n'
        '  <p>The instinct has clear roots: his undergrad work under Soheil Kolouri was <strong>optimal transport + model '
        'compression</strong> (PRANC, Linear Optimal Partial Transport) &mdash; the &ldquo;compact representations in parameter '
        'space&rdquo; idea that PortLLM and ORAL inherit. So the multi-agent-attack and SFT papers aren&rsquo;t detours: they&rsquo;re '
        'the trustworthiness and training-efficiency arms of one efficiency-of-deployed-LLMs program. '
        f'<span class="muted">(Synthesis from his <a href="{_HP}">homepage</a> + the papers below.)</span></p>'),
    "stats": [
        ("UNC + Anthropic", "PhD (Tianlong Chen lab); Research Fellow at Anthropic, 2026"),
        ("Theme", "efficient + trustworthy LLM adaptation"),
        ("Roots", "optimal transport &amp; model compression (Vanderbilt)"),
        ("~72 / ~54 cites", "Semantic Scholar / Scholar, approx., mid-2026"),
    ],
    "edu_html": 'Education: B.S. Computer Science &amp; Math, Vanderbilt (Kolouri lab) → PhD, UNC Chapel Hill (Tianlong Chen).',
    "arc": [
        {"yr": "2023 · undergrad (Vanderbilt, Kolouri lab)", "hl": False,
         "title": "Optimal transport &amp; model compression",
         "html": "Foundations in compact / efficient representations: <strong>Linear Optimal Partial Transport Embedding</strong> "
                 "(ICML 2023) and <strong>PRANC</strong> (ICCV 2023, compacting deep models with pseudo-random networks). This "
                 "&ldquo;parameter-space efficiency&rdquo; instinct seeds everything later."},
        {"yr": "2024 · transition", "hl": False, "title": "Toward LLM evaluation",
         "html": "A CVPR-workshop benchmark on LLM image geolocation (LLMGeo) &mdash; a pivot toward LLMs."},
        {"yr": "2025–2026 · UNC (Tianlong Chen lab)", "hl": True,
         "title": "Efficient + trustworthy LLM adaptation",
         "html": "Consolidates on <strong>LoRA / PEFT for evolving LLMs</strong> (<strong>PortLLM</strong> ICLR 2025, "
                 "<strong>ORAL</strong> EMNLP 2025 Findings, and <strong>CAR-LoRA</strong> ICLR 2026 &mdash; all <em>first-author</em>), "
                 "plus <strong>multi-agent LLM safety</strong> (<strong>Agents Under Siege</strong>, ACL 2025), <strong>reward-free "
                 "on-policy SFT</strong> (<strong>TMS</strong>, 2026), efficient reasoning / CoT distillation (2nd author), and on-device "
                 "personalization (EdgeTune, SenSys 2026). Recurring co-authors: Tianlong Chen, Zhen Tan, Pingzhi Li, Charles Fleming."},
    ],
    "start": [
        '<strong><a href="#papers">PortLLM</a></strong> (2025) — the cleanest idea: a fine-tune as a training-free, portable patch.',
        '<strong><a href="#papers">ORAL</a></strong> (2025) — going further: <em>generate</em> LoRA adapters with diffusion.',
        '<strong><a href="#papers">Agents Under Siege</a></strong> (2025) — the trustworthiness arm: breaking multi-agent LLM systems.',
        '<strong><a href="#papers">TMS</a></strong> (2026) — the training arm: RL-like stability without a reward model.',
    ],
    "papers": [
        {
            "title_html": "PortLLM: Training-Free, Portable Model Patches", "badge": "1st",
            "concept": "Carry a fine-tuned model’s knowledge forward to a newer base-model version by saving the fine-tune as a small reusable patch (a LoRA delta) and just adding it — no retraining.",
            "key_finding": "You can <strong>skip re-fine-tuning entirely</strong> &mdash; just add the OLD task patch to the NEW base "
                           "model. It matches real re-fine-tuning (and on GSM8K <em>beats</em> it, <strong>41.32 vs 34.95</strong>) at "
                           "<strong>0</strong> trainable parameters, ~12× less GPU memory, and ~<strong>4897×</strong> fewer GPU-hours.",
            "intro": "LoRA fine-tuning freezes W₀ and learns a low-rank ΔW = B·A (cheap, but still needs GPU training). When the "
                     "provider ships an <em>updated</em> base model (modeled as continued pretraining, θ' = θ + Δθ), you&rsquo;d normally "
                     "re-fine-tune &mdash; costly, recurring, and sometimes impossible if the original data is access-locked. PortLLM "
                     "asks: can the patch from the <em>old</em> model just be reused on the <em>new</em> one?",
            "method": "<strong>Setup.</strong> You already fine-tuned the old base θ for your task with LoRA, giving a patch "
                      "Δθ<sub>i</sub> = B·A. Now the provider ships a better base θ&prime; (modeled as continued pretraining, "
                      "θ&prime; = θ + Δθ). <strong>Baseline &mdash; the gold standard</strong> is to actually re-fine-tune the <em>new</em> "
                      "model to get its own patch, which needs GPUs and the original data: "
                      "<div class=\"formula\">θ&prime;<sub>i</sub> = θ&prime; + Δθ&prime;<sub>i</sub> <em>(re-train on the new base)</em></div> "
                      "<strong>What PortLLM optimizes away.</strong> It never computes Δθ&prime;<sub>i</sub> at all &mdash; it reuses the "
                      "<em>old</em> patch with a plain weight-add: "
                      "<div class=\"formula\">θ&prime;<sub>i</sub> &asymp; θ&prime; + Δθ<sub>i</sub> <em>(no training &mdash; runs in seconds)</em></div> "
                      "<strong>Why this is allowed.</strong> The exact answer is θ&prime;<sub>i</sub> = (θ&prime; + Δθ<sub>i</sub>) + R, where "
                      "the residual you drop is R = Δθ&prime;<sub>i</sub> − Δθ<sub>i</sub>. R is negligible because both task patches are "
                      "<em>low-rank</em> (LoRA) while the base models are full-rank &mdash; empirically R&rsquo;s Frobenius norm is "
                      "~<strong>136×</strong> smaller than the naive-add term, so ignoring it barely changes the output.",
            "figure": {"svg": '''<svg viewBox="0 0 660 196" xmlns="http://www.w3.org/2000/svg"><defs><marker id="pf1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#5b6776"/></marker><marker id="pf1g" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#3a7d44"/></marker></defs><g font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="12.5" text-anchor="middle"><text x="232" y="20" font-size="11" fill="#5b6776" font-weight="700">① fine-tune the OLD base once (expensive)</text><rect x="14" y="32" width="92" height="44" rx="9" fill="#eef2f6" stroke="#8a97a6"/><text x="60" y="58" font-weight="700">old base θ</text><rect x="138" y="32" width="118" height="44" rx="9" fill="#ffe7b3" stroke="#e09f3e"/><text x="197" y="54" font-weight="700">+ patch Δθ</text><text x="197" y="69" font-size="10">LoRA B·A</text><rect x="288" y="32" width="150" height="44" rx="9" fill="#cfe8f3" stroke="#2e86ab"/><text x="363" y="58" font-weight="700">fine-tuned model</text><text x="486" y="20" font-size="11" fill="#3a7d44" font-weight="700">② add the SAME patch (free)</text><rect x="14" y="120" width="92" height="44" rx="9" fill="#eef2f6" stroke="#8a97a6"/><text x="60" y="146" font-weight="700">new base θ′</text><rect x="138" y="120" width="118" height="44" rx="9" fill="#ffe7b3" stroke="#e09f3e"/><text x="197" y="142" font-weight="700">+ SAME Δθ</text><text x="197" y="157" font-size="10">no training</text><rect x="288" y="120" width="170" height="44" rx="9" fill="#d6ecd2" stroke="#3a7d44"/><text x="373" y="146" font-weight="700">personalized new model</text><g stroke="#5b6776" stroke-width="1.8" fill="none"><line x1="106" y1="54" x2="136" y2="54" marker-end="url(#pf1)"/><line x1="256" y1="54" x2="286" y2="54" marker-end="url(#pf1)"/><line x1="106" y1="142" x2="136" y2="142" marker-end="url(#pf1)"/><line x1="256" y1="142" x2="286" y2="142" marker-end="url(#pf1)"/></g><line x1="197" y1="76" x2="197" y2="118" stroke="#3a7d44" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#pf1g)"/><text x="207" y="101" font-size="10.5" fill="#3a7d44" text-anchor="start" font-style="italic">reuse — no retrain</text><rect x="486" y="120" width="160" height="44" rx="9" fill="#f4f8f4" stroke="#cfe6cf"/><text x="566" y="139" font-size="10.5">≈ matches re-train,</text><text x="566" y="154" font-size="10.5">~4897× fewer GPU-hrs</text><line x1="458" y1="142" x2="484" y2="142" stroke="#5b6776" stroke-width="1.8" marker-end="url(#pf1)"/></g></svg>''',
                       "caption": "PortLLM reuses one LoRA patch across base-model versions. Top: fine-tune the old base once (costly). Bottom: add the <em>same</em> patch to the new base with no training. The transfer is near-lossless because the patch is low-rank relative to the full-rank base, so the residual it ignores is tiny."},
            "results": "Mistral-7B / Llama2-7B / Llama3.1-8B / Gemma2-9B, 7 tasks, zero-shot. Lands within ~1 point of real "
                       "re-fine-tuning on most tasks and <em>beats</em> it on WNLI and <strong>GSM8K (41.32 vs 34.95</strong>; the "
                       "un-patched updated model scored only 15.16). Gap ≤ 0.73%, sometimes +5.53%. Cost vs LoRA fine-tuning: "
                       "<strong>0</strong> trainable params, ~<strong>12.2×</strong> less GPU memory, ~<strong>4897×</strong> fewer GPU hours (merge runs in seconds).",
            "discussion": "Future: extend across <em>different architectures</em> (via model merging). It already works even if the "
                          "provider&rsquo;s continued pretraining was full-weight, not LoRA.",
            "missing": "Only validated when the <em>same</em> model lineage evolves via continued pretraining (same architecture &amp; "
                       "weight shape). A real version jump that changes architecture/tokenizer/hidden-size has no coordinate "
                       "correspondence &mdash; you can&rsquo;t add the old delta. So PortLLM = cheap portability across successive "
                       "<em>same-architecture</em> checkpoints, not a universal patch surviving an architectural change (the paper&rsquo;s "
                       "own future work names this as open).",
            "cite": '<strong>Rana M. Shahroz Khan</strong> (1st), P. Li, S. Yun, Z. Wang, S. Nirjon, C.-W. Wong, T. Chen. '
                    'ICLR 2025. <a href="https://arxiv.org/abs/2410.10870">arXiv</a> · <a href="_research/portllm.md">evidence</a>',
        },
        {
            "title_html": "ORAL: Generating Large-Scale LoRAs via Conditional Recurrent Diffusion", "badge": "1st",
            "concept": "A diffusion model that GENERATES task-specific LoRA adapter weights from a text prompt + a target-model description, instead of training each one — scaling to 7B-parameter LLMs.",
            "key_finding": "A <strong>diffusion model can generate a working LoRA adapter</strong> from a text prompt + a description of "
                           "the target model &mdash; matching trained LoRAs (e.g. GSM8K <strong>34.67 vs 32.04</strong>) and, unlike prior "
                           "weight-generators, scaling all the way to <strong>7B-parameter</strong> LLMs.",
            "intro": "Instead of producing a LoRA adapter by gradient descent, <em>synthesize</em> its weights with a generative model. "
                     "Motivation = evolving LLMs again: when the base model updates, regenerate adapters from a prompt rather than "
                     "re-training every task adapter. Prior weight-generation methods couldn&rsquo;t get both <em>scalability</em> and "
                     "<em>controllability</em>.",
            "method": "<strong>Setup.</strong> A LoRA adapter is just a low-rank update ΔW = B·A, normally obtained by <em>training</em> "
                      "(gradient descent on task data). <strong>Baseline:</strong> "
                      "<div class=\"formula\">(B, A) = argmin L<sub>task</sub>( W<sub>0</sub> + B·A ) <em>(train each adapter from data)</em></div> "
                      "<strong>What ORAL changes.</strong> It replaces training with <em>generation</em> &mdash; a diffusion model "
                      "<em>produces</em> the adapter weights, conditioned on what you want: "
                      "<div class=\"formula\">(B, A) = Diffusion( noise | c ),   c = [ c<sub>model</sub> ; c<sub>text</sub> ]</div> "
                      "where c<sub>text</sub> is the task description and c<sub>model</sub> encodes the target model. <strong>The scaling "
                      "trick</strong> (why prior methods couldn&rsquo;t reach 7B): slice the huge weight matrix into a <em>sequence</em> of "
                      "fixed-size tokens, let a Mamba recurrence carry state along it, and have diffusion denoise each token &mdash; so it "
                      "never has to flatten one giant vector. <strong>Why condition on c<sub>model</sub>:</strong> it is exactly what lets one "
                      "generator emit adapters for <em>different / evolving</em> base models straight from a prompt.",
            "figure": {"svg": '''<svg viewBox="0 0 680 130" xmlns="http://www.w3.org/2000/svg"><defs><marker id="or1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#5b6776"/></marker></defs><g font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="12" text-anchor="middle"><rect x="12" y="42" width="120" height="48" rx="9" fill="#eef2f6" stroke="#8a97a6"/><text x="72" y="62" font-weight="700">task prompt</text><text x="72" y="79" font-size="10.5">+ model spec</text><rect x="152" y="42" width="74" height="48" rx="9" fill="#ffe7b3" stroke="#e09f3e"/><text x="189" y="64" font-weight="700">condition c</text><text x="189" y="80" font-size="10">[model;text]</text><rect x="246" y="42" width="172" height="48" rx="9" fill="#cfe8f3" stroke="#2e86ab"/><text x="332" y="62" font-weight="700">recurrent diffusion</text><text x="332" y="79" font-size="10">noise → weight-tokens</text><rect x="438" y="42" width="106" height="48" rx="9" fill="#e9e1f4" stroke="#6a4c93"/><text x="491" y="70" font-weight="700">LoRA (B, A)</text><rect x="564" y="42" width="104" height="48" rx="9" fill="#d6ecd2" stroke="#3a7d44"/><text x="616" y="70" font-weight="700">merge → LLM</text><g stroke="#5b6776" stroke-width="1.8" fill="none"><line x1="132" y1="66" x2="150" y2="66" marker-end="url(#or1)"/><line x1="226" y1="66" x2="244" y2="66" marker-end="url(#or1)"/><line x1="418" y1="66" x2="436" y2="66" marker-end="url(#or1)"/><line x1="544" y1="66" x2="562" y2="66" marker-end="url(#or1)"/></g><text x="332" y="116" font-size="10.5" fill="#5b6776" font-style="italic">weights are generated, not trained</text></g></svg>''',
                       "caption": "ORAL turns &lsquo;train a LoRA&rsquo; into &lsquo;generate a LoRA.&rsquo; The condition c = [model spec ; task prompt] steers a recurrent-diffusion model that denoises noise into the adapter weights (B, A), which merge into the LLM. Slicing the weights into a token sequence is what lets it scale to 7B-parameter models."},
            "results": "14 tasks (7 language, 4 vision, 3 multimodal), 5 base models incl. Mistral-7B, Qwen-VL-7B, SD 2.1; scales to "
                       "7B (prior baselines did not). Generated LoRAs are ≈ or &gt; trained ones (e.g. GSM8K 34.67 vs 32.04; image FID "
                       "mostly wins). Cross-model transfer: train on base versions t=0,1,2 → generate adapters for unseen evolved "
                       "versions t=3,4.",
            "discussion": "No dedicated limitations section. Future: interpretability of generated parameters.",
            "missing": "It doesn&rsquo;t <em>beat</em> a single trained LoRA (≈ tied). The value is <strong>amortization + transfer</strong>: "
                       "you must first collect many real trained LoRAs to train the generator (training is front-loaded once), then "
                       "produce new adapters by prompting; the real win is regenerating adapters when the base model evolves. If you only "
                       "need one adapter for one fixed model, plain LoRA training is simpler.",
            "cite": '<strong>Rana M. Shahroz Khan</strong> (1st), D. Tang, P. Li, K. Wang, T. Chen. '
                    'EMNLP 2025 Findings. <a href="https://arxiv.org/abs/2503.24354">arXiv</a> · <a href="_research/oral.md">evidence</a>',
        },
        {
            "title_html": "Agents Under Siege: Optimized Prompt Attacks on Multi-Agent LLM Systems", "badge": "1st",
            "concept": "A jailbreak that splits a malicious request into pieces, routes them through a team of cooperating agents along the safest path, and reassembles the attack at the target — defeating filters that only see harmless fragments.",
            "key_finding": "Splitting one jailbreak across cooperating agents and routing the pieces along the <em>least-guarded</em> path "
                           "reaches <strong>72.6% attack success</strong> (vs <strong>1.7%</strong> for standard GCG) and cuts the best "
                           "safety filter&rsquo;s F1 by ~30% &mdash; because no single guarded link ever sees the whole payload.",
            "intro": "A multi-agent LLM system wires several LLMs that pass messages over a graph. Almost all safety work studies a "
                     "<em>single</em> agent &mdash; but multi-agent systems have new attack surfaces: inter-agent messages, per-link "
                     "<em>token-bandwidth</em> limits (so chop a request below filter size), <em>latency/asynchrony</em> (messages arrive "
                     "in any order), and <em>partial</em> defenses (some paths are barely guarded). These &ldquo;pragmatic&rdquo; constraints "
                     "become attacker advantages.",
            "method": "<strong>Setup.</strong> A multi-agent system is a graph of LLMs passing messages; each link has a token-bandwidth "
                      "limit, messages can arrive out of order, and only <em>some</em> links are guarded by a safety filter. Threat model: "
                      "partial knowledge of the graph + gradient access to the target. Two ingredients exploit the structure. "
                      "<strong>(1) Routing (MFMC).</strong> Treat the network as a <em>flow graph</em> where each link has capacity F "
                      "(bandwidth) and cost G (detection risk), and solve for the cheapest-to-detect route and chunk sizes: "
                      "<div class=\"formula\">minimize  Σ G(u,v)·f(u,v)   subject to  0 ≤ f(u,v) ≤ F(u,v)</div> "
                      "i.e. send the payload through the least-guarded, highest-bandwidth path, chopped small enough to slip under each "
                      "link&rsquo;s filter. <strong>(2) Reorder-proof chunks (PIEL).</strong> Since chunks may arrive in any order, optimize "
                      "them (via GCG) so the attack fires under <em>every</em> permutation by averaging the evasion loss over orderings: "
                      "<div class=\"formula\">L(C) = (1/K!) Σ<sub>π</sub> −log p( harmful output | reordered chunks )</div> "
                      "(stochastic S-PIEL samples a few permutations). MFMC decides <em>how to chop and where to route</em>; PIEL makes each "
                      "fragment reassemble into a jailbreak regardless of order.",
            "figure": {"svg": '''<svg viewBox="0 0 680 200" xmlns="http://www.w3.org/2000/svg"><defs><marker id="as1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#b3402f"/></marker><marker id="as1g" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#9aa4af"/></marker></defs><g font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="12" text-anchor="middle"><rect x="10" y="78" width="78" height="44" rx="9" fill="#eef2f6" stroke="#8a97a6"/><text x="49" y="98" font-weight="700">attacker</text><text x="49" y="113" font-size="10">splits req</text><rect x="104" y="50" width="34" height="22" rx="5" fill="#ffe7b3" stroke="#e09f3e"/><text x="121" y="65" font-size="10.5">c1</text><rect x="104" y="89" width="34" height="22" rx="5" fill="#ffe7b3" stroke="#e09f3e"/><text x="121" y="104" font-size="10.5">c2</text><rect x="104" y="128" width="34" height="22" rx="5" fill="#ffe7b3" stroke="#e09f3e"/><text x="121" y="143" font-size="10.5">c3</text><rect x="206" y="78" width="66" height="44" rx="9" fill="#cfe8f3" stroke="#2e86ab"/><text x="239" y="104" font-weight="700">agent A</text><rect x="322" y="78" width="66" height="44" rx="9" fill="#cfe8f3" stroke="#2e86ab"/><text x="355" y="104" font-weight="700">agent B</text><rect x="322" y="150" width="168" height="34" rx="9" fill="#e7e9ec" stroke="#9aa4af"/><text x="406" y="171" font-size="11" fill="#5b6776">guarded link 🛡 — avoided</text><rect x="540" y="78" width="128" height="44" rx="9" fill="#f6d9d4" stroke="#b3402f"/><text x="604" y="98" font-weight="700">TARGET</text><text x="604" y="113" font-size="10">chunks reassemble</text><line x1="88" y1="100" x2="102" y2="100" stroke="#5b6776" stroke-width="1.6" marker-end="url(#as1g)"/><line x1="140" y1="100" x2="204" y2="100" stroke="#5b6776" stroke-width="1.6" marker-end="url(#as1g)"/><g stroke="#b3402f" stroke-width="2" fill="none"><line x1="272" y1="100" x2="320" y2="100" marker-end="url(#as1)"/><line x1="388" y1="100" x2="538" y2="100" marker-end="url(#as1)"/></g><text x="463" y="92" font-size="10.5" fill="#b3402f" font-style="italic">least-guarded route</text><line x1="355" y1="122" x2="380" y2="148" stroke="#9aa4af" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#as1g)"/><text x="452" y="138" font-size="10.5" fill="#9aa4af" font-style="italic">✗ filter sees a fragment</text></g></svg>''',
                       "caption": "One malicious request is split into chunks and routed (MFMC) along the least-guarded, highest-bandwidth path, skipping the filtered link; PIEL makes the chunks reassemble into a working jailbreak no matter their arrival order. A per-message single-agent filter only ever sees a harmless-looking fragment."},
            "results": "Up to <strong>7×</strong> over the best baseline. Llama2-7B / JailbreakBench: ASR <strong>72.6%</strong> vs GCG "
                       "1.7%. Most vulnerable Mistral-7B (81.2%), most resistant DeepSeek-R1-Distilled (41.3%); range ~38–84%. Defeats "
                       "Llama-Guard / Prompt-Guard (best guard&rsquo;s F1 drops ~30%). Complete-graph topologies most vulnerable (~78%), "
                       "chains most resilient (~60%).",
            "discussion": "Open-source models ≤9B only; assumes partial topology/defense knowledge; static defenses; text-only. Proposes "
                          "no concrete defense &mdash; argues single-agent filters are the wrong abstraction; calls for multi-agent-specific "
                          "defenses. Red-team ethics disclosure.",
            "missing": "Every result is on small open-source models under favorable assumptions (attacker knows the topology + where "
                       "defenses sit), so it does <em>not</em> show production systems (GPT-4/Claude, hidden topology) are breakable at "
                       "these rates. Read 72–84% as an upper-bound demo. The transferable contribution is conceptual: structural properties "
                       "(bandwidth, asynchrony, partial defense) are exploitable attack vectors, and <strong>per-message single-agent "
                       "filters are the wrong abstraction</strong> because they never see the whole payload.",
            "cite": '<strong>Rana M. Shahroz Khan</strong> (1st), Z. Tan, S. Yun, C. Fleming, T. Chen. '
                    'ACL 2025 (Main). <a href="https://arxiv.org/abs/2504.00218">arXiv</a> · <a href="_research/agents-under-siege.md">evidence</a>',
        },
        {
            "title_html": "TMS: Trajectory-Mixed Supervision for Reward-Free, On-Policy SFT", "badge": "1st",
            "concept": "Fine-tune an LLM to get most of RL’s stability benefit WITHOUT a reward model — by training it on samples drawn from its own past training checkpoints.",
            "key_finding": "Train on the model&rsquo;s <em>own</em> answers from earlier checkpoints instead of fixed labels: cross-task "
                           "forgetting drops from <strong>−26 to −41</strong> points (plain SFT) to just <strong>−2 to −3</strong> "
                           "&mdash; close to RL &mdash; with <strong>no reward model</strong>.",
            "intro": "Plain SFT (fixed labels) is cheap but brittle &mdash; it forgets. RLHF (reward model + RL) retains capability "
                     "better but is costly and unstable. The root cause TMS names is <strong>Supervision Mismatch</strong>: as the model "
                     "trains, its policy drifts away from the static labels, causing mode collapse and forgetting. Avoiding a reward model "
                     "is desirable (less cost, no reward-hacking, no preference data).",
            "method": "<strong>Setup.</strong> Plain SFT trains on fixed (question → label) pairs. As the model trains, its policy drifts "
                      "away from those static labels (the <em>supervision mismatch</em>) → mode collapse and forgetting. RL fixes this but "
                      "needs a reward model. <strong>Baseline (SFT):</strong> "
                      "<div class=\"formula\">minimize  −log π<sub>θ</sub>( y* | x ) <em>(imitate a fixed label y* the model drifts from)</em></div> "
                      "<strong>What TMS changes.</strong> During one SFT run, save T checkpoints and have each checkpoint generate its "
                      "<em>own</em> answer ŷ<sup>(t)</sup>(x). Train on a mixture of those self-generated answers (optionally blending the "
                      "labels q with weight α): "
                      "<div class=\"formula\">q<sub>α</sub> = α·q + (1−α)·m,   m(·|x) = (1/T) Σ<sub>t</sub> ŷ<sup>(t)</sup>(x)   <em>(α = 0.25, T = 10)</em></div> "
                      "<strong>Why it works.</strong> The targets are text the model itself plausibly produces, so supervision stays "
                      "<em>near its own support</em> &mdash; the stabilizing property of on-policy RL &mdash; yet the signal is just "
                      "&ldquo;imitate your own past samples&rdquo; (next-token loss), so there is no reward model, verifier, or RL loop. "
                      "Early checkpoints add diversity (anti-collapse), late ones add refinement &mdash; a built-in curriculum.",
            "figure": {"svg": '''<svg viewBox="0 0 680 210" xmlns="http://www.w3.org/2000/svg"><defs><marker id="tm1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#5b6776"/></marker><marker id="tm1r" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#b3402f"/></marker><marker id="tm1g" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#3a7d44"/></marker></defs><g font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="12" text-anchor="middle"><text x="150" y="20" font-size="11" font-weight="700" fill="#b3402f">plain SFT</text><rect x="14" y="30" width="116" height="40" rx="9" fill="#eef2f6" stroke="#8a97a6"/><text x="72" y="54" font-weight="700">fixed label y*</text><rect x="186" y="30" width="138" height="40" rx="9" fill="#f6d9d4" stroke="#b3402f"/><text x="255" y="49" font-weight="700">model π drifts away</text><text x="255" y="63" font-size="10">→ forgetting</text><line x1="130" y1="50" x2="184" y2="50" stroke="#b3402f" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#tm1r)"/><line x1="0" y1="86" x2="680" y2="86" stroke="#e6ebf0" stroke-width="1"/><text x="120" y="106" font-size="11" font-weight="700" fill="#3a7d44">TMS</text><text x="232" y="106" font-size="10.5" fill="#5b6776">one SFT run → save checkpoints, each answers itself</text><circle cx="40" cy="168" r="17" fill="#dbe7f3" stroke="#2e86ab"/><text x="40" y="172" font-size="10.5">θ₁</text><circle cx="104" cy="168" r="17" fill="#dbe7f3" stroke="#2e86ab"/><text x="104" y="172" font-size="10.5">θ₂</text><circle cx="168" cy="168" r="17" fill="#dbe7f3" stroke="#2e86ab"/><text x="168" y="172" font-size="10.5">θ₃</text><circle cx="232" cy="168" r="17" fill="#dbe7f3" stroke="#2e86ab"/><text x="232" y="172" font-size="10">θ_T</text><rect x="316" y="148" width="120" height="40" rx="9" fill="#ffe7b3" stroke="#e09f3e"/><text x="376" y="166" font-weight="700">mixture m</text><text x="376" y="181" font-size="10">of ŷ⁽ᵗ⁾</text><rect x="470" y="148" width="150" height="40" rx="9" fill="#d6ecd2" stroke="#3a7d44"/><text x="545" y="166" font-weight="700">train student</text><text x="545" y="181" font-size="10">stays near its support</text><g stroke="#5b6776" stroke-width="1.4" fill="none"><line x1="57" y1="156" x2="314" y2="164" marker-end="url(#tm1)"/><line x1="121" y1="156" x2="314" y2="167" marker-end="url(#tm1)"/><line x1="185" y1="156" x2="314" y2="170" marker-end="url(#tm1)"/><line x1="249" y1="155" x2="314" y2="173" marker-end="url(#tm1)"/></g><line x1="436" y1="168" x2="468" y2="168" stroke="#3a7d44" stroke-width="1.8" marker-end="url(#tm1g)"/></g></svg>''',
                       "caption": "Plain SFT chases a fixed label the model drifts away from (→ forgetting). TMS instead saves checkpoints along one SFT run, lets each generate its own answer, and trains the student on their mixture &mdash; keeping the target near the model&rsquo;s own outputs (RL-like stability) with no reward model."},
            "results": "Qwen-2.5 (1.5/3/7B), LLaMA-3.1-8B; math / instruction tasks. Matches SFT target accuracy while nearly "
                       "eliminating forgetting: average cross-task drop is <strong>−26 to −41 for SFT</strong> vs <strong>only −2.3 to −2.9 "
                       "for TMS</strong> (GRPO/RL: −0.9 to −1.9). Safety retention also improves toward RL. Cost: harvest 10 checkpoints + "
                       "one student pass &mdash; no reward models or verifiers.",
            "discussion": "Largest gains on non-unique solution spaces (math, instruction-following); modest on rigid formats (MMLU). "
                          "Optimal T ≈ 8–10. Safety gains require careful data curation.",
            "missing": "TMS does <em>not</em> beat RL &mdash; it only <strong>narrows</strong> the gap; &ldquo;approaches RL retention&rdquo; "
                       "can be mis-read as &ldquo;matches RL.&rdquo; The paper is explicit that RL is the gold standard and TMS incurs a "
                       "modestly larger cross-task drop than GRPO. Correct takeaway: a cheap, reward-free drop-in that recovers <em>most</em> "
                       "of RL&rsquo;s stability at near-SFT cost. Secondary risk: targets are the model&rsquo;s own generations, so latent "
                       "base-model biases can be reinforced.",
            "cite": '<strong>Rana M. Shahroz Khan</strong> (1st), Z. Liu, Z. Tan, C. Fleming, T. Chen. '
                    '2026 preprint <span class="unv">venue unconfirmed</span>. <a href="https://arxiv.org/abs/2602.03073">arXiv</a> · <a href="_research/tms.md">evidence</a>',
        },
    ],
    "list_rows": [
        ("2026", '<a href="https://arxiv.org/abs/2602.03073">TMS: Trajectory-Mixed Supervision (reward-free SFT)</a>', "arXiv", "<strong>1st</strong>", "—"),
        ("2026", "CAR-LoRA: Compression-Aware &amp; Robust LoRA for Evolving LLMs", "ICLR", "<strong>1st</strong>", "—"),
        ("2026", "EdgeTune: Efficient On-Device LLM Personalization", "SenSys", "2nd", "—"),
        ("2026", "The Quest for Efficient Reasoning (CoT-distillation benchmark)", "ICLR", "2nd", "—"),
        ("2025", '<a href="https://arxiv.org/abs/2503.24354">ORAL: Large-Scale LoRAs via Conditional Recurrent Diffusion</a>', "EMNLP Findings", "<strong>1st</strong>", "—"),
        ("2025", '<a href="https://arxiv.org/abs/2504.00218">Agents Under Siege</a>', "ACL (Main)", "<strong>1st</strong>", "—"),
        ("2025", '<a href="https://arxiv.org/abs/2410.10870">PortLLM</a>', "ICLR", "<strong>1st</strong>", "~?"),
        ("2024", "LLMGeo: Benchmarking LLMs on Image Geolocation", "CVPR Workshop", "3rd", "—"),
        ("2023", "PRANC: Pseudo-Random Networks for Compacting Deep Models", "ICCV", "5th", "—"),
        ("2023", "Linear Optimal Partial Transport Embedding", "ICML", "4th", "—"),
    ],
    "discuss": [
        '<strong>Generate vs train adapters.</strong> ORAL <em>generates</em> LoRAs and PortLLM <em>reuses</em> them; both only ≈ '
        'match a trained LoRA. When is &ldquo;cheaper, equally good&rdquo; worth a whole new method &mdash; and when is it premature optimization?',
        '<strong>Is per-message filtering doomed?</strong> Agents Under Siege shows fragment-and-route attacks defeat single-agent guards. '
        'What would a defense that &ldquo;sees the whole payload&rdquo; across a multi-agent system actually look like &mdash; and what does it cost?',
        '<strong>Cheap stability vs the real thing.</strong> TMS recovers ~most of RL&rsquo;s retention with no reward model, but training '
        'on your own outputs can amplify your own biases. When is &ldquo;imitate your past self&rdquo; a safe training signal, and when isn&rsquo;t it?',
    ],
    "complete_html": (
        '<p class="muted">A scope note (v0.7 completeness check). We deep-read his four strongest first-author papers; gaps a reader should know:</p>\n'
        '  <ul>\n'
        '    <li><strong>CAR-LoRA (ICLR 2026) is also first-author</strong> and in the exact PortLLM/ORAL lineage '
        '(&ldquo;compression-aware, robust LoRA for evolving LLMs&rdquo;) &mdash; mentioned but not deep-read; it&rsquo;s the most recent node of the LoRA arc.</li>\n'
        '    <li><strong>The optimal-transport / compression roots</strong> (PRANC, Linear Optimal Partial Transport, under Kolouri at Vanderbilt) are the origin of his parameter-space-efficiency instinct &mdash; summarized in the arc, not deep-read.</li>\n'
        '    <li>The notes lean toward <strong>LoRA/PEFT</strong>; a reader might wrongly conclude he&rsquo;s &ldquo;a LoRA-only person&rdquo; and that the multi-agent-attack paper is a one-off. It isn&rsquo;t &mdash; it&rsquo;s the <em>trustworthiness</em> arm of one efficiency agenda.</li>\n'
        '  </ul>'),
    "sources_html": (
        '<p>Identity and list from his <a href="https://rana-shahroz.github.io/">homepage</a>, '
        '<a href="https://dblp.org/pid/339/7435.html">DBLP (pid 339/7435)</a>, the Semantic Scholar API, and arXiv; each signature paper '
        'was deep-read into <a href="_research/">_research/</a>.</p>\n'
        '  <div class="callout warn"><strong>Caveats (verify before citing):</strong>\n'
        '    <ul>\n'
        '      <li><strong>Name collision:</strong> there is a prominent <em>unrelated</em> &ldquo;Shahroz Khan&rdquo; in naval / ship-hull '
        'generative design (Compute Maritime; Scholar HRC0hPIAAAAJ) &mdash; a <strong>different person</strong>. All papers here trace to '
        'DBLP pid 339/7435 / Scholar pdmMa3UAAAAJ.</li>\n'
        '      <li><strong>Citation counts</strong> (~72 Semantic Scholar / ~54 Scholar) are approximate and move fast for an early-career researcher (as of mid-2026).</li>\n'
        '      <li><strong>TMS</strong> is a 2026 preprint (venue unconfirmed); <strong>CAR-LoRA</strong> ICLR-2026 acceptance/track worth confirming.</li>\n'
        '      <li><strong>Anthropic Research Fellow</strong> is a fellowship starting summer 2026 (May 2026–present) &mdash; not a multi-year staff role.</li>\n'
        '    </ul>\n  </div>'),
}
