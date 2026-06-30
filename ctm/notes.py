"""
CTM — Continuous Thought Machines notes.py
Research direction 7: Sakana AI NeurIPS 2025 Spotlight.
Topic: reinstate neural timing and synchronization as core AI computation.
"""

NOTES = {
    "name": "Continuous Thought Machines",
    "title_suffix": "research reading notes",
    "subtitle": "What if AI learned to think in brainwaves? — Sakana AI reintroduces neural timing and synchrony as computation",
    "meta_html": (
        "Luke Darlow, Ciaran Regan, Sebastian Risi, Jeffrey Seely, Llion Jones &mdash; "
        "Sakana AI / Univ.&nbsp;Tsukuba / IT Univ.&nbsp;Copenhagen &mdash; "
        '<a href="https://arxiv.org/abs/2505.05522">arXiv:2505.05522</a> &middot; '
        '<a href="https://github.com/SakanaAI/continuous-thought-machines">GitHub</a> &middot; '
        "NeurIPS 2025 (Spotlight)"
    ),
    "tags": ["NeurIPS 2025", "Neural Dynamics", "Synchronization", "Adaptive Compute", "Sakana AI"],
    "who_heading": "What it is",
    "studynote_html": (
        "<p>CTM asks a question most deep learning papers don&rsquo;t: <em>what if we took the temporal "
        "dynamics inside individual neurons seriously?</em> The authors give each neuron its own private "
        "weights, let them generate rich activity histories, and then use <strong>which neurons fire "
        "together over time</strong> (synchronization) as the model&rsquo;s latent representation. "
        "It&rsquo;s biologically inspired &mdash; and it produces some surprising emergent behaviors.</p>"
        "<p>One thing to keep in mind as you read: the authors are explicit that this is <em>not</em> "
        "trying to beat the state of the art. The goal is to show a new kind of neural network is "
        "possible &mdash; and to invite the community to explore it.</p>"
    ),
    "hook_html": (
        "<p class=\"lead\">The most surprising thing is <strong>where the information lives</strong>. "
        "In a transformer, the latent representation is a vector of activations at a given instant &mdash; "
        "a <em>snapshot</em>. In the CTM, the representation is a <em>relationship</em>: the inner "
        "product of each pair of neurons&rsquo; activity <em>over time</em>, "
        "S<sup>t</sup> = Z<sup>t</sup>&nbsp;&middot;&nbsp;(Z<sup>t</sup>)<sup>T</sup>. Two neurons "
        "are &ldquo;synchronized&rdquo; if they have tended to fire at the same internal ticks. "
        "This is exactly the neuroscience <em>binding hypothesis</em> &mdash; that the brain encodes "
        "&ldquo;this edge and this color belong to the same object&rdquo; by synchronizing the "
        "neurons that represent them. The model is not told to synchronize anything; it learns to "
        "use synchrony as a tool because it turns out to be a powerful representation.</p>"
        "<p>The second surprise: adaptive compute comes <em>for free</em>. There is no halting "
        "module, no learned stopping signal. The model just picks the tick with the best prediction "
        "and the tick with the highest certainty, averages them in the loss, and the rest follows "
        "&mdash; easy images get answered early, hard ones keep thinking.</p>"
    ),
    "stats": [
        ("NeurIPS 2025", "Spotlight paper — competitive tier"),
        ("5 authors", "Sakana AI + Univ. Tsukuba + IT Univ. Copenhagen"),
        ("6 task domains", "Mazes, ImageNet, parity, sorting, Q&A, RL"),
        ("Open-source", "Code + checkpoints at github.com/SakanaAI/continuous-thought-machines"),
    ],
    "edu_html": (
        "The CTM is a <strong>neural network architecture</strong> that explicitly incorporates "
        "<strong>neural dynamics over time</strong> as its core mechanism, rather than treating neurons "
        "as simple weighted-sum units. It is inspired by biological principles — specifically "
        "<em>temporal coding</em> (information encoded in the timing of neural activity) and "
        "<em>neural synchrony</em> (the binding hypothesis: neurons representing related features "
        "synchronize their activity). The CTM is not a language model or a vision model specifically — "
        "it is a general architecture demonstrated on diverse tasks."
    ),
    "arc": [
        {
            "yr": "1980s–1997",
            "title": "RNNs and LSTMs: temporal processing, uniform neurons",
            "html": (
                "Recurrent networks give neural networks a sense of time: the hidden state carries "
                "information across sequence steps. LSTMs (Hochreiter &amp; Schmidhuber, 1997) add "
                "gating for long-range memory. But all neurons share the same weight matrices &mdash; "
                "each neuron is just a row of a shared W. No individual temporal identity."
            ),
        },
        {
            "yr": "2017",
            "title": "Transformers: attention replaces recurrence",
            "html": (
                "Vaswani et al. replace sequential processing with self-attention: all positions "
                "interact in parallel. Dominant today. But attention attends over <em>input</em> "
                "positions, not over an internal thought timeline. There is no time dimension "
                "decoupled from the data."
            ),
        },
        {
            "yr": "2021",
            "title": "PonderNet and adaptive compute: variable depth",
            "html": (
                "Graves (2016) and Banino et al. (PonderNet, 2021) add an explicit halting module "
                "that lets the model stop early for easy inputs. Adaptive depth as a design choice. "
                "But it requires a dedicated halting component bolted on top of the base model."
            ),
        },
        {
            "yr": "2024–25",
            "title": "Renewed interest in recurrence and reasoning",
            "html": (
                "Papers like Mamba and RWKV show recurrent models can compete with transformers "
                "on language. Separately, scaling laws appear to plateau, and the community starts "
                "asking what&rsquo;s missing. Sakana AI argues one missing piece is <em>neural "
                "temporal dynamics</em> &mdash; not just recurrence, but genuine per-neuron "
                "temporal identity and synchrony."
            ),
        },
        {
            "yr": "2025",
            "title": "CTM: neuron-level models + synchronization as representation",
            "html": (
                "Darlow, Regan, Risi, Seely, Jones (Sakana AI) give every neuron its own private "
                "weights, let them process their own activity histories, and use the inner product "
                "of those histories as the latent state. Adaptive compute emerges without a halting "
                "module. Demonstrated on mazes, ImageNet, parity, RL. NeurIPS 2025 Spotlight."
            ),
            "hl": True,
        },
    ],
    "start": [
        '<a href="https://sakana.ai/ctm/">Sakana AI blog post</a> &mdash; non-technical intro '
        "with visualizations. Watch the maze-solving video. This is the right first step.",
        '<a href="https://pub.sakana.ai/ctm">Interactive website</a> &mdash; see the neurons '
        "synchronize in real time as the CTM solves a maze.",
        'Read Section 3 of the <a href="https://arxiv.org/abs/2505.05522">paper</a> '
        "(Method): Figure 3 (architecture diagram), then Sections 3.1 (internal ticks), "
        "3.2 (synapse model), 3.3 (NLMs), 3.4 (synchronization). The pseudocode listings "
        "are clear and short.",
        "Then read Sections 4 (mazes) and 5 (ImageNet) for the empirical demonstrations. "
        "Focus on Figure 2 (ImageNet attention paths) and Figure 4 (maze generalization).",
    ],
    "papers": [
        {
            "title_html": "Continuous Thought Machines",
            "badge": "NeurIPS 2025 Spotlight",
            "concept": "Give each neuron its own private temporal processing weights; use the cross-correlation of neuron activity histories (synchronization) as the latent representation; get adaptive compute for free.",
            "key_finding": (
                "Using <strong>neural synchronization</strong> &mdash; which neurons fire together "
                "over an internal thought timeline &mdash; as the latent representation produces "
                "a model that builds internal world maps (solves mazes without positional encoding), "
                "learns to &lsquo;look around&rsquo; images without being told to, and acquires "
                "<strong>adaptive compute depth as an emergent property</strong> of its loss function "
                "&mdash; no halting module needed."
            ),
            "intro": (
                "Modern neural networks treat neurons as nearly identical: each neuron is a row of "
                "a shared weight matrix, receiving inputs and producing a scalar output. This is "
                "computationally convenient but biologically unrealistic &mdash; in the brain, "
                "individual neurons have unique temporal dynamics, and the <em>timing</em> of their "
                "firing encodes information. The <strong>binding hypothesis</strong> in neuroscience "
                "suggests that the brain links disparate features (color, shape, location) into a "
                "unified percept by <em>synchronizing</em> the neurons that represent them. "
                "CTM asks: what if an artificial neural network used the same principle? "
                "Instead of a single shared hidden state, give each neuron its own private MLP "
                "parameters to process its own activity history. Use the <em>synchrony pattern</em> "
                "of those histories as the latent representation. Run the network for T "
                "&ldquo;internal ticks&rdquo; that are <em>decoupled from any input sequence</em> "
                "&mdash; the model thinks on a self-generated timeline even for a static image."
            ),
            "method": (
                "<strong>Setup.</strong> Standard networks: one forward pass, one hidden state, "
                "all neurons share weights. CTM: run T internal ticks on a separate "
                "&ldquo;thought timeline.&rdquo; At each tick t → t+1: "
                "<strong>(1) Synapse model</strong> (shared, U-NET MLP) takes the current "
                "post-activations + attention output → produces pre-activations: "
                "<div class=\"formula\">a<sup>t</sup> = f<sub>&#x03B8;<sub>syn</sub></sub>(concat(z<sup>t</sup>, o<sup>t</sup>)) &#x2208; &#x211D;<sup>D</sup></div>"
                "<strong>(2) History</strong>: store the last M pre-activations: "
                "A<sup>t</sup> = [a<sup>t&#x2212;M+1</sup>, ..., a<sup>t</sup>] &#x2208; &#x211D;<sup>D&#xD7;M</sup>. "
                "<strong>(3) Neuron-Level Models (NLMs)</strong>: each neuron d has its OWN private "
                "parameters &#x03B8;<sub>d</sub> (a small MLP): "
                "<div class=\"formula\">z<sup>t+1</sup><sub>d</sub> = g<sub>&#x03B8;<sub>d</sub></sub>( A<sup>t</sup><sub>d</sub> ) <em>(each neuron processes only its own history)</em></div>"
                "<strong>(4) Synchronization</strong> &mdash; the latent representation. "
                "Collect all post-activation histories Z<sup>t</sup> = [z<sup>1</sup>,...,z<sup>t</sup>] "
                "&#x2208; &#x211D;<sup>D&#xD7;t</sup> and compute: "
                "<div class=\"formula\">S<sup>t</sup> = Z<sup>t</sup> &#xB7; (Z<sup>t</sup>)<sup>T</sup> &#x2208; &#x211D;<sup>D&#xD7;D</sup></div>"
                "S<sup>t</sup><sub>ij</sub> is large when neurons i and j have been firing together. "
                "With learnable temporal decay r<sub>ij</sub>: "
                "<div class=\"formula\">S<sup>t</sup><sub>ij</sub> = (Z<sup>t</sup><sub>i</sub> &#xB7; diag(R<sup>t</sup><sub>ij</sub>) &#xB7; Z<sup>t</sup><sub>j</sub>) / &#x221A;(&#x03A3;<sub>&#x03C4;</sub> [R<sup>t</sup><sub>ij</sub>]<sub>&#x03C4;</sub>)</div>"
                "Sub-sample D<sub>out</sub> neuron pairs from S<sup>t</sup>, project: "
                "y<sup>t</sup> = W<sub>out</sub> &#xB7; S<sup>t</sup><sub>out</sub> (outputs), "
                "q<sup>t</sup> = W<sub>in</sub> &#xB7; S<sup>t</sup><sub>action</sub> (attention query). "
                "<strong>(5) Cross-attention to data</strong>: "
                "<div class=\"formula\">o<sup>t</sup> = Attention(Q = q<sup>t</sup>,&nbsp; KV = FeatureExtractor(data)) <em>(attention uses synchrony as the query)</em></div>"
                "<strong>Adaptive compute (no halting module).</strong> "
                "The model outputs y<sup>t</sup> at every tick. For each data point, pick dynamically: "
                "t<sub>1</sub> = argmin<sub>t</sub>(loss), t<sub>2</sub> = argmax<sub>t</sub>(certainty): "
                "<div class=\"formula\">L = ( L<sup>t<sub>1</sub></sup> + L<sup>t<sub>2</sub></sup> ) / 2</div>"
                "Since t<sub>1</sub> and t<sub>2</sub> are data-dependent, easy inputs get answered "
                "at small t<sub>1</sub> &mdash; fewer ticks used, no explicit stop signal needed."
            ),
            "results": (
                "<strong>2D Mazes (39&#xD7;39, no positional encoding)</strong>: CTM "
                "significantly outperforms LSTM (1&#x2013;3 layers) and feed-forward baselines "
                "across all path lengths. Trained on 39&#xD7;39, generalizes to 99&#xD7;99 mazes "
                "by re-applying the same learned policy &mdash; suggesting it learned a general "
                "procedure, not a lookup. Emergent: keeps exploring beyond its training horizon. "
                "<strong>ImageNet-1K (50 internal ticks, ResNet-152 backbone)</strong>: "
                "<strong>72.47%</strong> top-1, <strong>89.89%</strong> top-5 (not SOTA, by design). "
                "Native adaptive compute: at 0.8 certainty threshold, most examples decided in "
                "&lt;10 of 50 ticks. Excellent calibration emerges naturally. "
                "Learns to &lsquo;look around&rsquo; images (Figure 2b): attention traces "
                "intuitive inspection paths without any training signal for this behavior. "
                "<strong>Parity (64-bit sequences)</strong>: CTM with 75&#x2013;100 ticks "
                "achieves perfect accuracy on some seeds; LSTM plateaus at ~60%. "
                "Attention head develops interpretable left-to-right scanning strategy (Figure 6d)."
            ),
            "discussion": (
                "The authors are explicit this is not a benchmark paper. The contribution is: "
                "<em>showing the architecture is possible and surprisingly capable</em>, and "
                "inviting the community to build on it. The emergent adaptive compute and "
                "interpretable attention are the most interesting findings &mdash; behaviors that "
                "arise without being explicitly trained for. "
                "Future work (from the paper): scaling NLMs, applying to language models, "
                "understanding WHY synchrony works as a representation, and exploring the "
                "formal connection to spiking neural networks."
            ),
            "figure": {
                "svg": '''<svg viewBox="0 0 720 260" xmlns="http://www.w3.org/2000/svg"><defs><marker id="ctm1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#5b6776"/></marker><marker id="ctm1b" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#2e86ab"/></marker><marker id="ctm1g" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#3a7d44"/></marker><marker id="ctm1p" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#6a4c93"/></marker></defs><g font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="11.5" text-anchor="middle"><text x="360" y="16" font-size="12" font-weight="700" fill="#1c2430">One internal tick  t &#x2192; t+1</text><rect x="8" y="26" width="116" height="50" rx="9" fill="#cfe8f3" stroke="#2e86ab"/><text x="66" y="45" font-weight="700">Synapse model</text><text x="66" y="59" font-size="10">U-NET MLP</text><text x="66" y="72" font-size="10">a&#x1D57; = f(z&#x1D57;, o&#x1D57;)</text><rect x="154" y="26" width="128" height="50" rx="9" fill="#fff3cd" stroke="#e09f3e"/><text x="218" y="44" font-weight="700">History buffer</text><text x="218" y="57" font-size="10">A&#x1D57; = [a&#x1D57;&#x207B;&#x1D39;&#x207A;&#xB9;...a&#x1D57;]</text><text x="218" y="70" font-size="10">M recent ticks</text><line x1="124" y1="51" x2="152" y2="51" stroke="#2e86ab" stroke-width="1.6" marker-end="url(#ctm1b)"/><rect x="312" y="26" width="158" height="50" rx="9" fill="#e9e1f4" stroke="#6a4c93"/><text x="391" y="44" font-weight="700">Neuron-Level Models</text><text x="391" y="58" font-size="10">each neuron d: private &#x03B8;&#x1D49;</text><text x="391" y="71" font-size="10">z&#x1D57;&#x207A;&#xB9;&#x1D49; = g&#x1D9c;&#x1D49;(A&#x1D57;&#x1D49;)</text><line x1="282" y1="51" x2="310" y2="51" stroke="#6a4c93" stroke-width="1.6" marker-end="url(#ctm1p)"/><rect x="500" y="26" width="212" height="50" rx="9" fill="#fde9ec" stroke="#d1495b"/><text x="606" y="43" font-weight="700" fill="#a83246">Synchronization</text><text x="606" y="57" font-size="10">Z&#x1D57; = [z&#xB9;,...,z&#x1D57;] &#x2208; &#x211D;&#x1D35;&#xD7;&#x1D57;</text><text x="606" y="70" font-size="10">S&#x1D57; = Z&#x1D57; &#xB7; (Z&#x1D57;)&#x1D40; &#x2208; &#x211D;&#x1D35;&#xD7;&#x1D35;</text><line x1="470" y1="51" x2="498" y2="51" stroke="#d1495b" stroke-width="1.6" marker-end="url(#ctm1)"/><text x="360" y="104" font-size="10" fill="#5b6776" font-style="italic">latent representation = synchrony pattern, not a single snapshot</text><rect x="500" y="118" width="212" height="50" rx="9" fill="#f1f6fa" stroke="#8a97a6"/><text x="606" y="137" font-weight="700">Sub-sample + project</text><text x="606" y="151" font-size="10">y&#x1D57; = W&#x2090;&#x2099;&#x209C; &#xB7; S&#x1D57;&#x2090;&#x2099;&#x209C; &#x2192; output</text><text x="606" y="164" font-size="10">q&#x1D57; = W&#x1D35;&#x2099; &#xB7; S&#x1D57;&#x2090;&#x2C7C;&#x209C; &#x2192; attn query</text><line x1="606" y1="76" x2="606" y2="116" stroke="#5b6776" stroke-width="1.6" marker-end="url(#ctm1)"/><rect x="154" y="118" width="166" height="50" rx="9" fill="#d6ecd2" stroke="#3a7d44"/><text x="237" y="136" font-weight="700">Cross-attention to data</text><text x="237" y="150" font-size="10">o&#x1D57; = Attn(Q=q&#x1D57;, KV=data)</text><text x="237" y="164" font-size="10">attends using sync as query</text><line x1="500" y1="143" x2="322" y2="143" stroke="#3a7d44" stroke-width="1.6" marker-end="url(#ctm1g)"/><line x1="237" y1="168" x2="66" y2="168" stroke="#5b6776" stroke-width="1.2" stroke-dasharray="4 3"/><line x1="66" y1="168" x2="66" y2="78" stroke="#5b6776" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#ctm1)"/><text x="148" y="189" font-size="10" fill="#5b6776" font-style="italic">o&#x1D57; feeds back into synapse model at next tick</text><rect x="8" y="206" width="474" height="48" rx="9" fill="#fff8ec" stroke="#e09f3e"/><text x="237" y="223" font-weight="700" font-size="11">Adaptive compute (no halting module)</text><text x="237" y="237" font-size="10">pick t&#x2081; = argmin loss, t&#x2082; = argmax certainty per sample &#x2192; L = (L&#x1D57;&#xB9; + L&#x1D57;&#xB2;)/2</text><text x="237" y="251" font-size="10" fill="#5b6776">easy inputs stop early; hard ones keep ticking &#x2014; emerges from loss, not a halting module</text></g></svg>''',
                "caption": "One internal tick of the CTM. The synapse model (shared) produces pre-activations; each neuron runs its own private MLP on its personal history to produce post-activations; the synchronization matrix S&#x1D57; = Z&#x1D57; &#xB7; (Z&#x1D57;)&#x1D40; captures which neurons fire together; this becomes the query for cross-attention to the data; the attention output feeds back in the next tick. Adaptive compute emerges: the loss picks the best-prediction and highest-certainty ticks per sample.",
            },
            "missing": (
                "<strong>This is explicitly not a SOTA paper.</strong> "
                "ImageNet 72.47% top-1 is far below modern models (~90%+). "
                "The O(D&sup2;) synchronization matrix grows expensive at large D, and "
                "each neuron having private weights increases parameter count. "
                "There are no language model experiments &mdash; the most obvious "
                "next direction. The theoretical reason WHY synchrony is a good "
                "representation remains open. Seed sensitivity in the parity task "
                "suggests some instability. "
                "The comparison is against LSTM and FF baselines; no comparison with "
                "modern SSMs (Mamba, RWKV), modern transformers, or PonderNet on the "
                "same tasks."
            ),
            "cite": (
                "Luke Darlow, Ciaran Regan, Sebastian Risi, Jeffrey Seely, Llion Jones. "
                "<em>Continuous Thought Machines.</em> "
                "NeurIPS 2025 (Spotlight). "
                '<a href="https://arxiv.org/abs/2505.05522">arXiv:2505.05522</a> &middot; '
                '<a href="https://github.com/SakanaAI/continuous-thought-machines">GitHub</a> &middot; '
                '<a href="_research/ctm.md">evidence</a>'
            ),
        },
    ],
    "list_rows": [
        ("2025", '<a href="https://arxiv.org/abs/2505.05522">Continuous Thought Machines</a>',
         "NeurIPS 2025 (Spotlight)", "Darlow, Regan, Risi, Seely, Jones (Sakana AI)", "—"),
        ("2021", "PonderNet: Learning to Ponder",
         "arXiv 2021", "Banino et al. (DeepMind)", "~300"),
        ("2021", "Liquid Time-Constant Networks (LTCNs)",
         "Nature Machine Intelligence 2021", "Hasani et al.", "~500"),
        ("2019", "Recurrent Models of Visual Attention (RAM)",
         "NeurIPS 2014 (cited 2019 variants)", "Mnih et al.", "~2000"),
        ("2017", "Attention is All You Need",
         "NeurIPS 2017", "Vaswani et al.", "~100000"),
        ("1997", "Long Short-Term Memory",
         "Neural Computation 1997", "Hochreiter &amp; Schmidhuber", "~80000"),
    ],
    "discuss": [
        "The CTM uses <strong>synchronization</strong> S<sup>t</sup> = Z<sup>t</sup>&nbsp;&#xB7;&nbsp;(Z<sup>t</sup>)<sup>T</sup> as its latent, "
        "rather than a single snapshot z<sup>t</sup>. The paper says 'snapshot representations were too constraining.' "
        "Can you think of a task where the snapshot would be equally good? And one where synchrony gives a "
        "meaningful advantage?",
        "The CTM achieves <strong>adaptive compute without a halting module</strong>: it just picks the tick of "
        "minimum loss and the tick of maximum certainty per sample, and averages their losses. "
        "Does this feel like 'true' adaptive compute, or is it more like a soft attention over ticks? "
        "How would you know which ticks the model actually relies on?",
        "The maze experiment uses no positional encodings, forcing the CTM to build an internal world model. "
        "It then generalizes from 39&#xD7;39 to 99&#xD7;99 by re-applying the same policy. "
        "Is this convincing evidence of a 'general procedure'? What experiment would you design to "
        "further test whether the CTM has actually learned something like graph search?",
        "Neuron-Level Models give each neuron its own private MLP of width d<sub>hidden</sub>. "
        "The total parameter count scales as D &times; d<sub>hidden</sub>&sup2; for the NLMs alone. "
        "For D=1024 and d<sub>hidden</sub>=64, that's 4M parameters just for NLMs. "
        "How do you think the benefits and costs of NLMs would scale as D grows to 10k or 100k?",
        "The paper positions CTM as distinct from Spiking Neural Networks (SNNs): it uses continuous "
        "values and is trained with backprop, while SNNs use discrete spike events and often require "
        "specialized learning rules. But the inspiration (neural timing, synchrony) is similar. "
        "What would a hybrid look like? What would you lose and gain?",
    ],
    "complete_html": (
        "<p>These notes cover the CTM paper and its immediate context. Not covered:</p>"
        "<ul>"
        "<li><strong>Spiking Neural Networks (SNNs)</strong>: discrete spike timing, event-driven computation, "
        "hardware efficiency — the CTM draws inspiration from but is explicitly distinct.</li>"
        "<li><strong>Liquid State Machines &amp; Reservoir Computing</strong>: random fixed recurrent networks "
        "with only the readout trained; related in spirit to rich internal dynamics.</li>"
        "<li><strong>Mamba &amp; modern SSMs</strong>: selective state space models; strong on language; "
        "not compared against CTM in the paper.</li>"
        "<li><strong>Neuroscience binding hypothesis</strong>: the theoretical basis for synchrony as "
        "a binding mechanism (Gray &amp; Singer 1989, Eckhorn et al. 1988); the paper motivates CTM "
        "with this but doesn&rsquo;t deeply engage with the neuroscience literature.</li>"
        "<li><strong>Language modeling</strong>: CTM is not tested on any language task; this is the "
        "most obvious next direction and explicitly deferred.</li>"
        "</ul>"
        "<p>Citation counts for 2025 papers are not yet reliable.</p>"
    ),
    "sources_html": (
        "<ul>"
        "<li><strong>CTM paper</strong>: PDF read directly from arXiv (pages 1&#x2013;8). All numbers "
        "from the paper text. "
        '<a href="_research/ctm.md">evidence file</a></li>'
        "<li><strong>Abstract and metadata</strong>: <a href=\"https://arxiv.org/abs/2505.05522\">arXiv:2505.05522</a> "
        "(confirmed NeurIPS 2025 Spotlight).</li>"
        "<li><strong>GitHub</strong>: README read via GitHub API from "
        "<a href=\"https://github.com/SakanaAI/continuous-thought-machines\">SakanaAI/continuous-thought-machines</a>.</li>"
        "<li><strong>Citation counts</strong>: not fetched; 2025 paper marked &mdash;. Earlier papers are rough estimates.</li>"
        "</ul>"
    ),
}
