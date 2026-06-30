# Evidence — Agents Under Siege: Optimized Prompt Attacks on Multi-Agent LLM Systems (ACL 2025 Main)

Raw deep-read (archived per v0.7). R. M. Shahroz Khan = **first author**. arXiv:2504.00218 · ACL 2025 Main
(2025.acl-long.476).

## CONCEPT
A jailbreak that splits one malicious request into pieces, routes them through a *team* of cooperating agents
along the safest path, and reassembles the attack at the target — defeating filters that only ever see harmless
fragments.

## INTRO — problem & why
- Multi-agent LLM system = several LLMs passing messages over a graph. Almost all safety work studies a SINGLE
  agent. Multi-agent creates a NEW attack surface: (1) inter-agent messages (payload can hop/relay); (2) bandwidth
  — each link has a token budget, so chop a request below filter size; (3) latency/asynchrony — messages arrive in
  any order; (4) partial defenses — not every link is guarded, so some paths touch few checks.
- Insight: realistic "pragmatic" deployments have exactly these constraints, which become attacker advantages.

## METHOD
- Threat model: partial knowledge of the comm graph (connectivity, per-link bandwidth, where defenses sit) +
  gradient access to the target LLM. Attacker can't override defenses or control all agents.
- **MFMC routing**: treat the network as a flow graph; each link has capacity F (bandwidth) and cost G (detection
  risk); minimize Σ G·f s.t. capacity + flow conservation → route payload through least-defended/highest-capacity
  links, chunk it to fit bandwidth.
- **PIEL (Permutation-Invariant Evasion Loss)**: optimize the chunks so the attack works under ANY arrival order —
  average attack-success loss over all K! permutations; tokens via **GCG**; **S-PIEL** samples M permutations
  (cheaper). MFMC = how to chop/route; PIEL = make fragments reorder-robust.

## RESULTS (ASR as decimals)
- Up to **7×** over best baseline. Llama2-7B/JailbreakBench: PIEL **0.726** vs GCG 0.017 vs vanilla ~0.
- Most vulnerable **Mistral-7B 0.812**; most resistant **DeepSeek-R1-Distilled 0.413**; range ~38–84%.
- Models: Llama2-7B, Llama3.1-8B, Mistral-7B, Gemma2-9B, DeepSeek-R1-Distilled. Benchmarks: JailbreakBench,
  AdvBench (520), In-the-Wild (1,405).
- Defeats guards (Llama-Guard 1/2/3, Prompt-Guard-86M): best guard Llama-Guard-3-8B F1 drops ~30%.
- Topology: complete graph most vulnerable ~78%; chain most resilient ~60%. Transfer ~61–82% across models
  <span>(secondary figure — verify before exact citing)</span>.

## DISCUSSION / FUTURE / LIMITATIONS
- Open-source ≤9B only; assumes partial topology/defense knowledge; static defenses + fixed bandwidth; text-only.
- No concrete defense proposed — argues single-agent guards are the wrong abstraction; calls for multi-agent-specific
  defenses (global/cross-link reasoning that can reassemble fragments). Red-team ethics disclosure.

## MOST IMPORTANT MISSING THING (per-paper)
Every result is on small open-source models under favorable assumptions (attacker knows topology + defense
placement) → does NOT show production systems (GPT-4/Claude, hidden topology) are breakable at these rates. Read
72–84% as an upper-bound demo. The TRANSFERABLE contribution is conceptual: structural properties (bandwidth,
asynchrony, partial defense) are exploitable attack vectors, and per-message single-agent filters are the wrong
abstraction because they never see the whole payload. The new *threat class* is the takeaway, not the percentages.

## Sources used (agent)
- https://arxiv.org/abs/2504.00218 · /pdf · /html v2 · https://aclanthology.org/2025.acl-long.476/ · dblp
