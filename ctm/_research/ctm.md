# Evidence: CTM — Continuous Thought Machines

**Source**: arXiv:2505.05522 v4 (Oct 2025); NeurIPS 2025 (Spotlight)
**Authors**: Luke Darlow, Ciaran Regan, Sebastian Risi, Jeffrey Seely, Llion Jones
**Institution**: Sakana AI (Tokyo); Univ. Tsukuba; IT Univ. Copenhagen
**Verified via**: Direct PDF read (pages 1-8) + arXiv abstract

## Core claim
Most ANNs abstract away individual neuron complexity. CTM reinstates:
1. Each neuron has its OWN private weight parameters (NLM)
2. Neural synchronization (which neurons fire together over time) IS the latent representation

## Full architecture (in order of a single forward step, t → t+1)

### Step 1: Synapse model (shared)
f_{θ_syn}: takes concat(z^t, o^t) → pre-activations a^t ∈ R^D
Implemented as a U-NET-esque MLP (deeper & more flexible = better in experiments)
o^t = attention output from previous tick (initialized to zeros at t=0)

### Step 2: History window
A^t = [a^{t-M+1}, ..., a^t] ∈ R^{D×M}  (M ≈ 10–100, last M pre-activations)

### Step 3: Neuron-Level Models (NLMs) — key innovation
Each neuron d ∈ {1,...,D} has PRIVATE parameters θ_d (a depth-1 MLP of width d_hidden):
z^{t+1}_d = g_{θ_d}(A^t_d)   (processes only neuron d's history, not other neurons)
This produces post-activations z^{t+1} ∈ R^D.

### Step 4: Synchronization — key innovation
Z^t = [z^1, ..., z^t] ∈ R^{D×t}   (non-fixed length history of post-activations)
S^t = Z^t · (Z^t)^T ∈ R^{D×D}   (inner product of each neuron's activity history)
S^t_ij = how much neurons i and j have been synchronized over the thought timeline
With temporal decay: S^t_ij = (Z^t_i · diag(R^t_ij) · Z^t_j) / sqrt(Σ_τ [R^t_ij]_τ)
where R^t_ij = [exp(-r_ij(t-1)), exp(-r_ij(t-2)), ..., exp(0)] with learnable decay r_ij ≥ 0

### Step 5: Sub-sampling & projection
Since S^t is D×D (can be huge), randomly sample D_out neuron pairs at training start:
S^t_out ∈ R^{D_out}   projected to y^t = W_out · S^t_out   (class outputs)
S^t_action ∈ R^{D_action}   projected to q^t = W_in · S^t_action   (attention query)

### Step 6: Cross-attention to data
o^t = Attention(Q=q^t, KV=FeatureExtractor(data))
o^t ∈ R^{d_attn} is concatenated with z^{t+1} → input for next tick's synapse model

## Loss function and adaptive compute
The model runs for T internal ticks and outputs y^t at each tick.
Select two special ticks per data point (dynamically):
- t_1 = argmin(L) = tick with minimum loss (best prediction)
- t_2 = argmax(C) = tick with maximum certainty C^t = 1 - normalized_entropy(y^t)
L = (L^{t_1} + L^{t_2}) / 2

Adaptive compute emerges: since t_1 and t_2 are dynamically selected, easy inputs get fewer ticks naturally. No explicit halting module needed.

## Results

### 2D Mazes (39×39, sequence of 100 actions)
- CTM strongly outperforms LSTM (1,2,3 layers) and FF baselines
- No positional encodings → must build internal world model
- Trained on 39×39, generalizes to 99×99 by re-applying learned policy
- Emergent: continues exploring beyond training horizon
- Setup: 75 internal ticks for CTM (50 also tested)

### ImageNet-1K (50 internal ticks, ResNet-152 backbone)
- 72.47% top-1, 89.89% top-5 (uncropped)
- NOT aiming for SOTA; focus is on dynamics, not benchmark
- Native adaptive compute: most images decided with <10 of 50 ticks at 0.8 certainty
- Excellent calibration emerges (well-calibrated probabilities vs. certainty threshold)
- Learns to "look around" the image: attention path emerges without training signal

### Parity (64-length binary sequences)
- CTM with 75-100 ticks achieves perfect accuracy on some seeds
- Outperforms LSTM significantly
- Figure 6d: attention head learns interpretable scanning strategy (scans sequence left-to-right)
- CTMs with 100 ticks >> 50 ticks >> 25 ticks (more thought steps = better)

### Other (Section 7): sorting, QA over MNIST, RL (CartPole, Acrobot, FourRooms)

## What's different from prior work
- LSTMs: uniform neurons, sequential data only, single hidden state
- Transformers: no temporal dynamics, attention over input tokens
- SNNs: discrete spike timing, hard to train with backprop
- PonderNet/ACT: adaptive compute bolted on with explicit halting mechanism
- CTM adaptive compute: EMERGES naturally from loss on t_1, t_2 without any halting module
- RAM (Recurrent Visual Attention): focuses on external glimpses; CTM's latent IS synchrony

## Key limitation (honest)
Authors explicitly state: "The goal of this work is to share the CTM, rather than pushing for new state-of-the-art results."
- ImageNet 72.47% top-1 is far behind current SOTA (~90%+)
- O(D^2) synchronization matrix is expensive at large D
- NLM parameter count scales with D (each neuron has private MLP)
- No language model experiments
- Theoretical understanding of WHY synchronization is a good representation = open
- Seed sensitivity on parity task (Section F.2)

## Cite
Luke Darlow, Ciaran Regan, Sebastian Risi, Jeffrey Seely, Llion Jones.
"Continuous Thought Machines." NeurIPS 2025 (Spotlight). arXiv:2505.05522.
GitHub: github.com/SakanaAI/continuous-thought-machines
