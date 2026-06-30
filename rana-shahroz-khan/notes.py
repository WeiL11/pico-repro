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
            "intro": "LoRA fine-tuning freezes W₀ and learns a low-rank ΔW = B·A (cheap, but still needs GPU training). When the "
                     "provider ships an <em>updated</em> base model (modeled as continued pretraining, θ' = θ + Δθ), you&rsquo;d normally "
                     "re-fine-tune &mdash; costly, recurring, and sometimes impossible if the original data is access-locked. PortLLM "
                     "asks: can the patch from the <em>old</em> model just be reused on the <em>new</em> one?",
            "method": "Save the LoRA delta Δθᵢ = B·A as a portable <strong>patch</strong>. Apply it to the new model with a plain "
                      "weight add &mdash; no retraining: <div class=\"formula\">θ&prime;<sub>i</sub> &asymp; θ&prime; + Δθ<sub>i</sub> <em>(vs. actually re-fine-tuning the new model)</em></div> "
                      "Why it works (theory): the true result decomposes into the naive add plus a residual R = (Δθ'ᵢ − Δθᵢ); R is "
                      "negligible because task patches are <em>low-rank</em> while base models are full-rank &mdash; empirically R&rsquo;s "
                      "Frobenius norm is ~<strong>136×</strong> smaller than the naive term.",
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
            "intro": "Instead of producing a LoRA adapter by gradient descent, <em>synthesize</em> its weights with a generative model. "
                     "Motivation = evolving LLMs again: when the base model updates, regenerate adapters from a prompt rather than "
                     "re-training every task adapter. Prior weight-generation methods couldn&rsquo;t get both <em>scalability</em> and "
                     "<em>controllability</em>.",
            "method": "Three pieces. (1) <strong>Tokenize the weights</strong>: slice each layer&rsquo;s ΔW into fixed-size tokens + "
                      "positions → a sequence (the key to scaling). (2) <strong>Recurrent processing</strong> (a Mamba module) walks the "
                      "sequence carrying a hidden state → handles huge LoRA sets. (3) <strong>Diffusion</strong> denoises noise into real "
                      "weight-tokens, <em>conditioned</em> on <div class=\"formula\">c = [ c<sub>model</sub> ; c<sub>text</sub> ] <em>(target-model architecture + task description)</em></div> "
                      "The c_model encoding is what lets generated adapters transfer across evolving base models. Output reassembles into "
                      "B, A and merges normally.",
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
            "intro": "A multi-agent LLM system wires several LLMs that pass messages over a graph. Almost all safety work studies a "
                     "<em>single</em> agent &mdash; but multi-agent systems have new attack surfaces: inter-agent messages, per-link "
                     "<em>token-bandwidth</em> limits (so chop a request below filter size), <em>latency/asynchrony</em> (messages arrive "
                     "in any order), and <em>partial</em> defenses (some paths are barely guarded). These &ldquo;pragmatic&rdquo; constraints "
                     "become attacker advantages.",
            "method": "Threat model: partial knowledge of the comm graph + gradient access to the target. Two pieces: "
                      "<strong>(1) MFMC routing</strong> &mdash; treat the network as a flow graph with link capacity F (bandwidth) and cost "
                      "G (detection risk); minimize Σ G·f to route the payload through the least-defended, highest-capacity links, chunked "
                      "to fit bandwidth. <strong>(2) PIEL</strong> (Permutation-Invariant Evasion Loss) &mdash; optimize the chunks (via "
                      "GCG) so the attack works under <em>any</em> arrival order by averaging the success loss over all orderings "
                      "(stochastic S-PIEL samples a few). No single guarded link ever sees enough to refuse.",
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
            "intro": "Plain SFT (fixed labels) is cheap but brittle &mdash; it forgets. RLHF (reward model + RL) retains capability "
                     "better but is costly and unstable. The root cause TMS names is <strong>Supervision Mismatch</strong>: as the model "
                     "trains, its policy drifts away from the static labels, causing mode collapse and forgetting. Avoiding a reward model "
                     "is desirable (less cost, no reward-hacking, no preference data).",
            "method": "Three stages. (1) Run an ordinary SFT and save T=10 checkpoints; have each checkpoint <em>generate its own</em> "
                      "answer to each question. (2) Build a mixture over those self-generated answers (optionally blending 25% original "
                      "human labels). (3) Train the final model to imitate the mixture (next-token loss). It&rsquo;s <em>on-policy yet "
                      "reward-free</em>: targets are text the model itself plausibly produces (near its own support → RL-like stability), "
                      "but the signal is just &ldquo;imitate your own past samples&rdquo; &mdash; no reward, verifier, or RL loop. The "
                      "trajectory acts as a curriculum (early = diverse, late = refined).",
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
