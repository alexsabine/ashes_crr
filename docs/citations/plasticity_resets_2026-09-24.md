# Resets, plasticity and forgetting: a dated literature check for the "cut with content" study

- **Fetch date for every source below:** 2026-09-24 (UTC). All fetched in this session with `curl` (arXiv abs and HTML
  pages, nature.com, Crossref API, ecva.net, intelligence.org) or WebFetch (iclr.cc) or WebSearch (for discovery only).
- **Raw material:** every page was saved under `scratchpad/cut/raw/` (`batch1.txt` to `batch6.txt` hold the arXiv
  abstract-page extractions, with submission histories; `ft_<id>.txt` hold the arXiv HTML full texts; `nature.txt`,
  `interrupt.txt` and `gdumb.pdf` hold the others). Quotes were copied from those files. Inline maths in HTML full text was
  kept as its LaTeX alt-text, so some quotes show `$...$`.
- **Access levels used below:**
  - *full text*: the whole paper was read (arXiv HTML, Nature open-access HTML, or PDF).
  - *abstract*: only the arXiv abstract page (title, authors, submission history, abstract).
  - *snippet*: search-engine text only. Nothing below relies on a snippet alone.
- **What was blocked:**
  - OpenReview's API and PDF returned HTTP 403 (a bot wall). D'Oro et al. was read from the ICLR virtual page instead.
  - The intelligence.org blog page returned a Cloudflare 403. The Orseau and Armstrong PDF on the same host did download.
  - github.com returned 403 through the session proxy. The code repositories were confirmed live with `git ls-remote`
    (§8).
- **Unverified candidates.** One arXiv id I tried from memory (2411.04834) turned out to be an unrelated chemistry paper.
  It is not used. The survey is 2411.04832.

---

## 0. The main point for the study design (inference, labelled as such)

1. **A reset to the task-boundary checkpoint is not a plasticity intervention in this literature's sense.**
   - Every method that restores plasticity moves parameters toward the *initial distribution* or brings in *fresh
     units*. Examples: full or partial reinitialisation, Shrink and Perturb, L2-Init, continual backprop, ReDo.
   - A reset to the task-boundary checkpoint, θ ← θ_boundary, does neither. It goes back to a point that already carries
     all the plasticity loss accumulated before the boundary. It only throws away what was learned since.
2. **In the literature's terms it is a "hard reversion".**
   - Cho et al. 2025/26 test exactly this. Their soft blend with θ_prev beats it, and so does random reinitialisation (§2.9).
   - Dohare et al. (Nature 2024) use the same operation as early stopping at each increment (§1.1).
   - So SCL1's observation (resets to the boundary checkpoint raised final accuracy) should be read as a
     stability/early-stopping effect, not a plasticity effect.
   - SCL2-B supports that reading: resets tied or trailed the tuned fixed λ and the one-epoch learner. This is my
     inference from the repository's own report plus the sources below. No paper tests it on this learner.
3. **The regime is far from where plasticity loss has been shown.** The repository's regime is 2 or 3 tasks, 4 to 10
   classes, a few epochs per task and a small MLP. Every demonstration of plasticity loss found here needs tens to
   thousands of task switches (§5). One paper reports no plasticity loss at all on a 10-class label-permutation stream of
   400 switches (§1.6). The only reset effect expected at 2 or 3 tasks is Ash and Adams' warm-start generalisation gap
   (§2.1), which appears after a single warm start and is absent for a convex learner.

---

## 1. Loss of plasticity

### 1.1 Dohare, Hernandez-Garcia, Lan, Rahman, Mahmood and Sutton, "Loss of plasticity in deep continual learning", *Nature* 632, 768–774 (2024)
- **Identifiers.**
  - DOI 10.1038/s41586-024-07711-7. Received 11 Aug 2023, accepted 12 Jun 2024, published 21 Aug 2024, open access
    (CC BY 4.0). The DOI metadata was also confirmed via Crossref.
  - arXiv preprint 2306.13812, titled "Maintaining Plasticity in Deep Continual Learning". v1 23 Jun 2023, v2 18 Aug 2023,
    v3 9 Apr 2024.
- **Access:** full text (nature.com HTML).
- **Benchmarks and stream lengths:**
  - **Continual ImageNet.** Binary tasks on pairs of classes, output heads reset at each task switch, 5,000 tasks.
  - **Online Permuted MNIST.** 800 tasks of 60,000 images, one pass, no mini-batches, three-hidden-layer MLP. Variants
    ran 150 tasks for the network-size sweep, and switched every 10k/100k/1M examples for 48M examples.
  - **Class-incremental CIFAR-100.** Starts with 5 classes and adds 5 per increment, 20 increments of 200 epochs each
    (4,000 epochs), ResNet-18. Old classes keep being trained, "to focus on plasticity rather than on forgetting".
  - **Slowly-Changing Regression.** Bit-flipping inputs, target from a fixed LTU network, 3M examples.
  - **RL.** PPO on Ant with friction changed every 2M steps.
- **Effect sizes (quoted):**
  - > "Although these networks learned up to 88% correct on the test set of the early tasks (Fig. 1b , left panel), by
    > the 2,000th task, they had lost substantial plasticity for all values of the step-size parameter"
  - > "incremental training was initially better than retraining, but after 40 classes, the incrementally trained network
    > showed loss of plasticity that became increasingly severe. By the end, when all 100 classes were available, the
    > accuracy of the incrementally trained base system was 5% lower than the retrained network"
  - > "Loss of plasticity with continued training is most pronounced at the smaller network sizes, but even the largest
    > networks show some loss of plasticity."
- **Remedies:**
  - > "L2 regularization adds a penalty for large weights; augmenting backpropagation with this enabled the network to
    > continue improving its learning performance over at least 5,000 tasks. The Shrink and Perturb algorithm 11 , which
    > includes L2 regularization, also performed well."
  - Continual backprop (CBP) reinitialises a fraction ρ of mature low-utility units per step (ρ = 10⁻⁵ on CIFAR-100). On
    CIFAR-100, Shrink and Perturb reduced the loss and CBP eliminated it (final CBP accuracy 76.13 % on 100 classes).
- **A reset to a checkpoint inside the protocol:**
  - > "To prevent overfitting, at the start of each new increment, we reset the weights of the network to the weights of
    > the best-performing (on the validation set) network found during the previous increment; this is equivalent to
    > early stopping for each different increment."
- **Reference arm.** Accuracy is reported relative to a network reinitialised at each increment. That is the
  plasticity yardstick we recommend below.
- **Scope.**
  - > "Loss of plasticity is different from catastrophic forgetting, which concerns poor performance on old examples even
    > if they are not presented again"
  - The paper does not measure forgetting.
- **Replication status.** Plasticity loss on these benchmarks has been reproduced by several independent groups: Kumar et
  al., Lewandowski et al., Elsayed and Mahmood, and Liu and Mou (§1.4 to 1.8). Which remedy wins varies across groups: in
  Kumar et al. it is L2-Init, not CBP. Code: `shibhansh/loss-of-plasticity`, live (§8).

### 1.2 Dohare, Sutton and Mahmood, "Continual Backprop: Stochastic Gradient Descent with Persistent Randomness", arXiv 2108.06325
- **Versions:** v1 13 Aug 2021, v3 5 May 2022. **Access:** abstract.
- **Quote:**
  > "We show that in continual learning setups, Backprop performs well initially, but over time its performance
  > degrades."

### 1.3 Lyle, Zheng, Nikishin, Avila Pires, Pascanu and Dabney, "Understanding plasticity in neural networks", ICML 2023 (oral), arXiv 2303.01486
- **Versions:** v4 27 Nov 2023. **Access:** full text.
- **Design.**
  - A two-hidden-layer MLP memorises random labels of MNIST, and the labels are re-randomised after a fixed budget.
  - Interventions compared: last-layer reset, layer norm, Shrink and Perturb, two-hot encoding, and others.
- **Quotes:**
  - > "This process quickly leads a default Adam optimizer to diverge, saturating most of its ReLU units"
  - > "We find that loss of plasticity is deeply connected to changes in the curvature of the loss landscape, but that it
    > often occurs in the absence of saturated units."
  - On the interventions compared (the start of the sentence is cut off in the extraction):
    > "…yers, provide the greatest improvements to plasticity, while methods which perturb the parameters or provide other
    > forms of regularization tend to see less benefit."
  - The best-performing of these, layer normalisation, was then applied to DQN on the Arcade Learning Environment.

### 1.4 Lyle, Zheng, Khetarpal, van Hasselt, Pascanu, Martens and Dabney, "Disentangling the Causes of Plasticity Loss in Neural Networks", arXiv 2402.18762
- **Versions:** v1 29 Feb 2024, the only version. **Access:** full text.
- **Quotes:**
  - > "intervening on any single mechanism is insufficient to avoid the loss of plasticity in all cases"
  - > "a combination of layer normalization and weight decay is highly effective at maintaining plasticity"
- **Abruptness matters** (CIFAR-10 random labels, 40 iterations of 100,000 steps):
  - > "more sudden task changes result in more severe loss of plasticity … Notably, resetting only 1% of labels minimally
    > interferes with performance."
- **Relevance to resets as practice:**
  - > "Such declines in performance are often resolved in practice by resetting the model parameters and training from
    > scratch on updated training data"

### 1.5 Kumar, Marklund and Van Roy, "Maintaining Plasticity in Continual Learning via Regenerative Regularization" (L2-Init), arXiv 2308.11958
- **Versions:** v3 24 Oct 2024. **Access:** full text. The venue is not stated on the arXiv page.
- **Method.** An L2 penalty toward the *initial* parameters θ₀. Unlike EWC, it anchors to θ₀, not to the previous task's
  parameters.
  > "while EWC is designed to remember information about previous tasks, our method is designed to maintain plasticity"
- **Benchmarks (Table 1):**

  | benchmark | tasks | length of each task |
  |---|---|---|
  | Permuted MNIST | 500 | 10k samples, 1 epoch |
  | Random Label MNIST/CIFAR | 50 | 1,200 samples, 400 epochs |
  | 5+1 CIFAR | 30 | – |
  | Continual ImageNet | 500 | 10 epochs |

- **Compared against:** continual backprop, ReDo, L2, Shrink and Perturb, CReLU and layer norm.
  - > "L2 Init consistently maintains plasticity."
- **Shrink and Perturb at task switches (App. A.3).** The paper describes the canonical "cut with content" at a boundary:
  > "Every time a task switches, Shrink and Perturb multiplies neural network parameters by a shrinkage factor $p<1$ and
  > then perturbs them by a small noise vector $\epsilon$ ."
- **One of the few papers that measures both sides (App. A.2.6, Permuted MNIST, 20 tasks):**

  | method | BWT | one-step BWT | total online average accuracy |
  |---|---|---|---|
  | L2-Init | −63.4 % | −11.3 % | 81.1 % |
  | EWC | −39.0 % | −7.8 % | 75.8 % |
  | L2-Init + EWC | −51.1 % | −7.8 % | 80.0 % |

  - > "adding EWC to L2 Init significantly reduces forgetting while having little impact on plasticity. However, EWC on
    > its own, while having relatively poor plasticity, has less forgetting than L2 Init + EWC."
- **Stream length:**
  - > "loss of plasticity sometimes becomes evident only after training for long sequences of tasks"

### 1.6 Elsayed and Mahmood, "Addressing Loss of Plasticity and Catastrophic Forgetting in Continual Learning" (UPGD), ICLR 2024, arXiv 2404.00781
- **Versions:** v2 30 Apr 2024. **Access:** full text.
- **Setting.** Streaming, one sample per step, 1M steps.
  - Labels are permuted every 2,500 samples (≈ 400 switches) on EMNIST, CIFAR-10 and mini-ImageNet.
  - Inputs are permuted every 60,000 samples on MNIST.
- **Baselines.** SGDW, PGD, Shrink and Perturb, AdamW, and streaming EWC/SI/MAS/RWalk. Figure 1 also shows "Adam with
  restarts".
- **Quotes:**
  - > "Adam loses plasticity as newer and newer tasks are presented and performs much worse than Adam with restarts later."
  - > "methods addressing catastrophic forgetting (e.g., S-EWC) performed the best, whereas methods addressing loss of
    > plasticity (e.g., S&P) only maintained their performance at a lower level."
- **A negative result, directly relevant to 10-class carriers:**
  > "We hypothesize that the issue of loss plasticity does not occur in this problem mainly due to its small number of
  > classes (Lesort et al. 2023), leading to a probability of 10% for the same label re-occurrence after label
  > permutation, resulting in less amount of non-stationarity that causes loss of plasticity."
- Code: `mohmdelsayed/upgd`, live.

### 1.7 Abbas, Zhao, Modayil, White and Machado, "Loss of Plasticity in Continual Deep Reinforcement Learning", arXiv 2303.07507
- **Versions:** v1 13 Mar 2023. **Access:** full text. Published at CoLLAs 2023; the venue is not printed on the arXiv page.
- **Quotes:**
  - > "Our analysis shows that the activation footprint of the network becomes sparser, contributing to the diminishing
    > gradients."
  - The remedy is CReLU. Some runs spanned "50 days and 2 billion environment interactions".

### 1.8 Other plasticity papers
Access is abstract unless marked otherwise.
- **Lewandowski, Tanaka, Schuurmans and Machado**, "Directions of Curvature as an Explanation for Loss of Plasticity",
  arXiv 2312.00246 v4, 5 Oct 2024:
  > "Neural networks lose directions of curvature during training"
- **Lewandowski et al.**, "Learning Continually by Spectral Regularization", arXiv 2406.06811 v2, 27 Oct 2024. The
  regularizer "keeps the maximum singular value of each layer close to one".
- **Hernandez-Garcia, Dohare, Luo and Sutton**, "Reinitializing weights vs units for maintaining plasticity in neural
  networks", arXiv 2508.00212 v2, 20 Aug 2025. Full text; CoLLAs 2025 per the header of the search-result PDF.
  > "we identify two settings when reinitializing weights is more effective at maintaining plasticity than reinitializing
  > units: (1) when the network has a small number of units and (2) when the network includes layer normalization."
- **Farias and Jozefiak**, "Self-Normalized Resets for Plasticity in Continual Learning", arXiv 2410.20098 v3,
  28 Sep 2025. SNR resets a neuron "when evidence suggests its firing rate has effectively dropped to zero".
- **Liu and Mou**, "Do Neural Networks Lose Plasticity in a Gradually Changing World?", arXiv 2602.09234 v2,
  16 Jun 2026. Full text.
  > "the severity of plasticity loss is closely tied to the abruptness of task transitions, and can be substantially
  > reduced when the environment changes gradually."
- **Hernandez-Garcia, Figliolia and Millidge**, "Can Scale Save Us From Plasticity Loss in Large Language Models?", arXiv
  2606.24752 v1, 23 Jun 2026:
  > "the onset of plasticity loss follows a predictable scaling law, growing sublinearly with model size"
  - They also report plasticity loss "under stationary multilingual training".
- **Prakash et al.**, "Spectral Collapse Drives Loss of Plasticity in Deep Continual Learning", arXiv 2509.22335 v3,
  29 May 2026. Loss of plasticity "is preceded by Hessian spectral collapse at new-task initialization".
- **Wang, Srinivasa, Chen, Liu, Payani and Zhang**, "Predicting Plasticity in Deep Continual Learning: A Theoretical
  Perspective", arXiv 2605.09044 v1, 9 May 2026.
  > "some widely adopted diagnostics of plasticity, including representation rank and neural tangent kernel rank, can
  > fail to predict the loss of trainability"
  - They propose "optimization readiness" instead. This is a warning against using rank or dead-unit counts as
    plasticity *measures*; they are diagnostics only.
- **Wang, Chandra and Zhang**, "Experience Replay Addresses Loss of Plasticity in Continual Learning", arXiv 2503.20018
  v1, 25 Mar 2025. A hypothesis paper; replay is processed with Transformers.
  > "by simply adding an experience replay and processing the data in the experience replay with Transformers, the loss of
  > plasticity disappears"
- **Park et al.**, "Activation by Interval-wise Dropout" (AID), ICML 2025, arXiv 2502.01342 v2.
- **Berariu et al.**, "A study on the plasticity of neural networks", arXiv 2106.00042 v2, 14 Oct 2023.

### 1.9 Surveys (2024–26)
- **Klein, Luther, McAuliffe, Miklautz, Plant and Tschiatschek**, "Plasticity Loss in Deep Reinforcement Learning: A
  Survey", arXiv 2411.04832.
  - Versions: v1 7 Nov 2024, v2 8 Nov 2024, **v3 18 Apr 2026**. Access: full text of v3.
  - > "reveals that general regularization techniques often outperform domain-specific interventions"
  - > "hard resets offer simplicity and strong restoration of plasticity in off-policy settings, while soft resets provide
    > finer control and broader applicability at the cost of increased hyperparameter sensitivity."
  - It is RL-focused and notes that CL surveys "address plasticity loss only in conjunction with catastrophic
    forgetting".
- **Pan et al.**, "A Survey of Continual Reinforcement Learning", arXiv 2506.21872 v2, 7 Apr 2026. Abstract only.
- **No dedicated 2025–26 survey of plasticity loss in continual *supervised* learning was found** in today's searches.

---

## 2. Reset methods

### 2.1 Ash and Adams, "On Warm-Starting Neural Network Training", NeurIPS 2020, arXiv 1910.08475
- **Versions:** v3 31 Dec 2020. **Access:** full text.
- **The warm-start gap needs only one warm start.** Data arrive in rounds, and a warm-started model generalises worse
  than a fresh one.
- **Table 1 (validation accuracy, random init vs warm start):**

  | model | CIFAR-10 SGD | CIFAR-10 Adam | SVHN Adam |
  |---|---|---|---|
  | ResNet | 56.2 vs 51.7 | 78.0 vs 74.4 | – |
  | MLP | 39.0 vs 37.4 | – | 76.7 vs 69.4 |

- **The convex case is not affected:**
  > "Logistic regression, which enjoys a convex loss surface, is not significantly damaged by warm starting for any
  > datasets."
- **The method:**
  > "we propose initializing the network's parameters by shrinking the weights found in the previous round of
  > optimization towards zero, then adding a small amount of parameter noise. Specifically, we initialize each learnable
  > parameter $\theta_{i}^{t}$ at training round $t$ as $\theta_{i}^{t}\leftarrow\lambda\theta_{i}^{t-1}+p^{t}$ , where
  > $p^{t}\sim\mathcal{N}(0,\,\sigma^{2 ..."
- **Note.** This is the only reset literature in which a benefit is expected after very few rounds. It concerns
  generalisation on *growing* data, where old data stay available. It is not class-incremental learning without replay.

### 2.2 Nikishin, Schwarzer, D'Oro, Bacon and Courville, "The Primacy Bias in Deep Reinforcement Learning", ICML 2022, arXiv 2205.07802
- **Versions:** v1 16 May 2022. **Access:** full text.
- **What is reset:**
  - SPR: the final linear layer every 2×10⁴ steps.
  - SAC: all networks every 2×10⁵ steps.
  - DrQ: the last 3 of 7 layers.
  - Optimiser statistics are also reset.
  - > "The replay buffer is preserved between resets"
- **Effect.** Atari 100k IQM rose from 0.380 (SPR) to 0.478 (SPR + resets).
- **Where resets cost:**
  - > "For environments in which the primacy bias does not appear to be an issue, such as cheetah-run , resetting causes
    > some spikes of reduced performance in the learning curves"
  - > "we note that brief collapses in performance induced by resetting may be undesirable from a regret minimization
    > perspective. Potential remedies include having a period of offline post-training after each reset or sampling
    > actions from an interpolation between pre- and post-reset agents"
- Code: `evgenii-nikishin/rl_with_resets`, live.

### 2.3 Sokar, Agarwal, Castro and Evci, "The Dormant Neuron Phenomenon in Deep Reinforcement Learning" (ReDo), ICML 2023 oral, arXiv 2302.12902
- **Versions:** v2 13 Jun 2023. **Access:** full text.
- **Quote:**
  > "periodically check in all layers whether any neurons are $\tau$ -dormant; for these, reinitialize their incoming
  > weights and zero out the outgoing weights."
- With τ = 0 the network's output is left unchanged. That makes ReDo the closest published analogue of a *function-
  preserving* cut with content: the parameters change, the predictions do not.

### 2.4 Asadi, Fakoor and Sabach, "Resetting the Optimizer in Deep RL: An Empirical Study", NeurIPS 2023, arXiv 2306.17833
- **Versions:** v2 15 Nov 2023. **Access:** abstract plus the table of contents of the full text.
- **Quote:**
  > "a simple idea is to reset the internal parameters of the optimizer when starting a new iteration … this simple
  > modification significantly improves the performance of deep RL on the Atari benchmark."
- This is the relevant arm if the learner uses Adam: a cut whose only content is the optimiser's moment estimates.

### 2.5 D'Oro, Schwarzer, Nikishin, Bacon, Bellemare and Courville, "Sample-Efficient Reinforcement Learning by Breaking the Replay Ratio Barrier", ICLR 2023 (oral)
- **Identifier:** OpenReview OpC-9aBBVJe. No arXiv version was found.
- **Access:** abstract, via WebFetch of iclr.cc/virtual/2023/oral/12655. OpenReview returned 403. WebFetch paraphrases
  through a small model, so this quote is flagged as *not byte-verified*.
- **Quote:**
  > "we show that fully or partially resetting the parameters of deep reinforcement learning agents causes better replay
  > ratio scaling capabilities to emerge"
- dblp lists it at ICLR 2023.

### 2.6 Nikishin, Oh, Ostrovski, Lyle, Pascanu, Dabney and Barreto, "Deep Reinforcement Learning with Plasticity Injection", NeurIPS 2023, arXiv 2305.15555
- **Versions:** v2 3 Oct 2023. **Access:** full text.
- **Quote:**
  > "at any point in training, one can freeze the current network and create a new one that is going to be learning a
  > change to the predictions, whilst ensuring that the change is initially zero."
- Also used as a *diagnostic*: if injection helps, plasticity was being lost. This is a useful gate arm.

### 2.7 Zhou, Vani, Larochelle and Courville, "Fortuitous Forgetting in Connectionist Networks", ICLR 2022, arXiv 2202.00155
- **Versions:** v1 1 Feb 2022. **Access:** abstract.
- **Quote:**
  > "the forgetting step selectively removes undesirable information from the model, and the relearning step reinforces
  > features that are consistently useful under different conditions."

### 2.8 Zaidi, Berariu, Kim, Bornschein, Clopath, Teh and Pascanu, "When Does Re-initialization Work?", PMLR 187 (ICBINB workshop, NeurIPS 2022), arXiv 2206.10011
- **Versions:** v2 2 Apr 2023. **Access:** full text.
- **This is the key negative result:**
  > "when deployed alongside other carefully tuned regularization techniques, re-initialization methods offer little to
  > no added benefit for generalization, although optimal generalization performance becomes less sensitive to the choice
  > of learning rate and weight decay hyperparameters."
- **Exception:** label noise.
  > "re-initialization significantly improves upon standard training, even in the presence of other carefully tuned
  > regularization techniques."

### 2.9 Cho, Moon, Chunara, Cho and Cha, "Forget Forgetting: Continual Learning in a World of Abundant Memory", arXiv 2502.07274
- **Versions:** v1 11 Feb 2025, **v5 18 Feb 2026**. **Access:** full text of v5.
- **Method (Weight Space Consolidation).** The closest published method to "partial reset to the task-boundary
  checkpoint".
  - The parameters at the task boundary are stored as θ_prev. After n_warm epochs the dormant (low-importance) parameters
    are reset to
    > "the mixed value of the previous task model $\theta_{prev}$ and the current model $\theta$ value"
  - Weights are also averaged.
- **Ablation:**
  > "our soft reset method (a weighted blend with $\theta_{\text{prev}}$ ) consistently outperforms random
  > reinitialization and hard reversion."
  - "Hard reversion" is SCL1's operation.
- **The regime matters:**
  - > "under full memory, per-task resets (reinitializing weights before each task) recover plasticity while preventing
    > forgetting … However, in the more realistic sufficient memory regime (e.g., 20–40%), retraining from scratch
    > degrades markedly"
  - With **zero memory** (CIFAR-100 class-IL) all methods fall to 25–53 %. Their reset method gave 29.83 % against replay's
    26.07 % and DER's 53.37 %.
  - > "resetting up to 80% of parameters yields minimal degradation in accuracy"

### 2.10 Methods that combine a reset with retention
- **Lee, Cho, Kim, Kim, Min, Choo and Lyle, "Slow and Steady Wins the Race: Maintaining Plasticity with Hare and Tortoise
  Networks"**, ICML 2024, arXiv 2406.02596 v2, 4 Feb 2025. Full text.
  - The update rules: Tortoise θ_t ← μθ_t + (1−μ)θ_h, then periodically Hare θ_h ← θ_t.
  - > "common methods designed to enhance plasticity by maintaining trainability provide limited benefits to
    > generalization. While reinitializing the network can be effective, it also risks losing valuable prior knowledge."
  - A continual variant ran 10 phases:
    > "in Tiny ImageNet, where generalization loss is severe, reinitialization p roved to be a more effective choice,
    > despite its periodic performance drops."
    (The stray space in "p roved" is in the source.)
  - Code: `dojeon-ai/hare-tortoise`, live.
- **Ahn, Hyeon, Oh, Hwang and Moon, "Reset & Distill"** (ICLR 2025 under the title "Prevalence of Negative Transfer in
  Continual Reinforcement Learning: Analyses and a Simple Baseline"), arXiv 2403.05066 v3, 4 Nov 2025. Full text.
  > "R&D combines a strategy of resetting the agent's online actor and critic networks to learn a new task and an offline
  > learning step for distilling the knowledge from the online actor and previous expert's action probabilities."
  - Tested on long Meta-World sequences. Code: `hongjoon0805/Reset-Distill`, live.
- **Frati, Traft, Clune and Cheney, "Reset It and Forget It: Relearning Last-Layer Weights Improves Continual and
  Transfer Learning"** ("zapping"), ECAI 2024, DOI 10.3233/FAIA240840, arXiv 2310.07996 v2, 20 Oct 2024.
  > "the repeated resetting of weights in the last layer, which we nickname "zapping""
  - Tested on Omniglot and Omni-image few-shot continual learning.
- **Galashov, Titsias, György, Lyle, Pascanu, Teh and Sahani, "Non-Stationary Learning of Neural Networks with Automatic
  Soft Parameter Reset"**, NeurIPS 2024, arXiv 2411.04034 v1. It uses an Ornstein–Uhlenbeck drift toward the
  initialisation.
  > "the approach can be understood as a form of soft parameter reset."
- **Maheshwari, Raisbeck and da Silva, "AltNet"**, arXiv 2512.01034 v3, 9 Mar 2026.
  > "such resets come at the cost of a temporary drop in performance, which can be dangerous in real-world settings."
- **McCutcheon, Chatzaroulas and Fallah, "Calibrated Partial Resets"**, arXiv 2607.24996 v1, 27 Jul 2026, RLC workshop.
  > "full unit reinitialization often sacrifices peak performance and can destabilize training, leading to policy
  > collapse"
  - > "Ablations reveal a tunable trade-off between plasticity and peak performance"
- **Juliani and Ash, "A Study of Plasticity Loss in On-Policy Deep Reinforcement Learning"**, NeurIPS 2024, arXiv
  2405.19153 v2. A negative result for several remedies:
  > "a number of methods developed to resolve it in other settings fail, sometimes even performing worse than applying no
  > intervention at all."
  - A class of "regenerative" methods did work.

### 2.11 Rewinding and checkpoints
- **Frankle, Dziugaite, Roy and Carbin, "Linear Mode Connectivity and the Lottery Ticket Hypothesis"**, ICML 2020, arXiv
  1912.05671 v4.
  - The precedent for "rewinding" to an early-training checkpoint. Here it is a pruning tool, not a continual-learning
    one.
- **No paper was found that registers "reset to the task-boundary checkpoint" as a continual-learning method on its
  own.** It appears in three places:
  - as early stopping (Dohare 2024);
  - as the losing "hard reversion" ablation (Cho et al.);
  - as the target of a soft reset (Hare and Tortoise, where the checkpoint is an EMA).
- **Prabhu, Torr and Dokania, "GDumb"**, ECCV 2020, DOI 10.1007/978-3-030-58536-5_31 (Crossref). Full text, first pages
  of the ECVA PDF. It is the extreme "reset and retrain from memory" baseline:
  > "at test time, trains a model from scratch using samples only in the memory."
  - > "it obtains state-of-the-art accuracies (often with large margins) in almost all the experiments"

---

## 3. The reset–forgetting trade-off, and resets and safety

- **Papers that measure plasticity and forgetting together:**
  - Kumar et al. App. A.2.6 (BWT and online accuracy, L2-Init × EWC).
  - Elsayed and Mahmood (a forgetting-oriented benchmark, label-permuted CIFAR-10).
  - Cho et al. (class-IL accuracy under several memory budgets, with reset ablations).
  - Lee et al. (Hare and Tortoise, with full vs limited data access).
  - Ahn et al. (R&D, negative transfer and forgetting, §5.3 of that paper).
  - Dohare 2024 deliberately does not measure forgetting.
- **Shared pattern (my synthesis of the quotes above):**
  - Resets toward the initial state restore trainability. They cost retention unless the old knowledge is kept elsewhere:
    in a replay buffer (Nikishin), in a slow network (Hare and Tortoise), in a distillation target (R&D), in a blend with
    θ_prev (Cho), or in an EWC anchor (Kumar A.2.6).
  - With no memory (Cho, zero-memory) resets help little.
- **Resets and aligned behaviour** (no paper found on *network resets* erasing safety training; these are the nearest):
  - **Qi et al., "Fine-tuning Aligned Language Models Compromises Safety, Even When Users Do Not Intend To!"**, arXiv
    2310.03693 v1, 5 Oct 2023:
    > "we jailbreak GPT-3.5 Turbo's safety guardrails by fine-tuning it on only 10 such examples at a cost of less than
    > $0.20"
  - **Alssum, Itani, Hammoud, Torr, Bibi and Ghanem, "Unforgotten Safety"**, arXiv 2512.10150 v1, 10 Dec 2025.
    > "We attribute this safety compromise to catastrophic forgetting and frame the problem of preserving safety when
    > fine-tuning as a continual learning (CL) problem"
    - > "DER outperforms both other CL methods and existing safety-preserving baselines"
  - **Lin et al., "Mitigating the Alignment Tax of RLHF"**, EMNLP 2024, arXiv 2309.06256 v4, 13 Oct 2024. Weight
    interpolation between two checkpoints is in effect a partial reset.
    > "model averaging, which simply interpolates between pre and post RLHF model weights, surprisingly achieves the most
    > strongest alignment-forgetting Pareto front"
  - **Bhardwaj, Anh and Poria, "RESTA"**, arXiv 2402.11746 v1. It adds a safety vector back to the weights, which
    "decreases the harmfulness of the compromised model from 18.6% to 5.1% and from 9.2% to 1.5%".
- **Implication (inference).** A reset toward any checkpoint other than the one where the aligned behaviour lives can
  erase that behaviour; a reset toward the aligned checkpoint restores it. The direction of the reset is the safety
  variable, not the fact of a reset.

---

## 4. Standard metrics and baselines

- **Lopez-Paz and Ranzato, "Gradient Episodic Memory for Continual Learning"**, NIPS 2017, arXiv 1706.08840 v6,
  13 Sep 2022. Full text.
  - R_{i,j} is the accuracy on task j after training on task i, and b̄ is the accuracy at random initialisation.
  - "Average Accuracy: ACC = 1/T Σ_{i=1}^{T} R_{T,i}"
  - "Backward Transfer: BWT = 1/(T−1) Σ_{i=1}^{T−1} R_{T,i} − R_{i,i}"
  - "Forward Transfer: FWT = 1/(T−1) Σ_{i=2}^{T} R_{i−1,i} − b̄_i"
  - These are transcribed from the LaTeX alt-text. Also:
    > "For a fine-grained evaluation that accounts for learning speed, one can build a matrix $R$ with more rows than
    > tasks, by evaluating more often."
- **Chaudhry, Dokania, Ajanthan and Torr, "Riemannian Walk for Incremental Learning: Understanding Forgetting and
  Intransigence"**, ECCV 2018, DOI 10.1007/978-3-030-01252-6_33, arXiv 1801.10112 v3. Full text.
  - Forgetting: $f_{j}^{k}=\max_{l\in\{1,\cdots,k-1\}}a_{l,j}-a_{k,j}$.
  - Intransigence: $I_{k}=a_{k}^{*}-a_{k,k}$, where $a_k^*$ comes from a reference model trained jointly on
    $\bigcup_{l=1}^{k}\mathcal{D}_{l}$.
  - > "We define intransigence as the inability of a model to learn new tasks."
  - Intransigence is the standard name for loss of plasticity in class-incremental learning.
- **De Lange, van de Ven and Tuytelaars, "Continual evaluation for lifelong learning: Identifying the stability gap"**,
  ICLR 2023, arXiv 2205.13452 v2. Methods show
  > "substantial forgetting upon starting to learn new tasks, except that this forgetting is temporary and followed by a
  > phase of performance recovery."
  - They propose worst-case metrics from per-iteration evaluation. Relevant because a cut sits exactly at the boundary
    where the stability gap occurs.
- **Díaz-Rodríguez, Lomonaco, Filliat and Maltoni, "Don't forget, there is more than forgetting"**, arXiv 1810.13166 v1.
  Adds memory and compute overheads to the metric set.
- **van de Ven and Tolias, "Three scenarios for continual learning"**, arXiv 1904.07734 v1. Also van de Ven, Tuytelaars
  and Tolias, "Three types of incremental learning", *Nature Machine Intelligence*, 5 Dec 2022, DOI
  10.1038/s42256-022-00568-3 (Crossref plus the abstract on nature.com).
  > "when task identity must be inferred (i.e., class incremental learning), we find that regularization-based approaches
  > (e.g., elastic weight consolidation) fail and that replaying representations of previous experiences seems required"
  - This bears directly on the repository's Laplace/EWC learner in class-incremental splits.
- **Chaudhry et al., "On Tiny Episodic Memories in Continual Learning"**, arXiv 1902.10486 v4. A tiny replay buffer
  > "significantly outperforms specifically designed CL approaches with and without episodic memory"
  - It gave gains of 7–17 % with one example per class.
- **Kirkpatrick et al., EWC**, PNAS 2017, DOI 10.1073/pnas.1611835114, arXiv 1612.00796 v2.
- **Lesort et al., "Challenging Common Assumptions about Catastrophic Forgetting"**, arXiv 2207.04543 v2, 15 May 2023.
  > "catastrophic forgetting has a limited effect on DNNs trained with SGD. When trained on long sequences with data
  > sparsely re-occurring, the overall accuracy improves"
- **Closest published analogues of "partial reset at task boundaries"**, in order of closeness:
  1. The soft reset to θ_prev in Weight Space Consolidation (Cho et al. 2025/26).
  2. Shrink and Perturb applied at each task switch (Ash and Adams 2020, as described in Kumar et al. App. A.3).
  3. Hare and Tortoise (reset to the slow EMA weights).
  4. A head/last-layer reset at each task (Dohare's Continual ImageNet protocol; zapping; Nikishin's SPR variant).
- **Strong simple baselines named across these papers:**
  - fine-tuning;
  - L2 / weight decay;
  - L2-Init;
  - EWC and online-EWC;
  - experience replay with a tiny memory;
  - GDumb (retrain from scratch on memory);
  - a fresh-init network per task (the plasticity reference);
  - joint training (the intransigence reference);
  - layer norm plus weight decay (Lyle 2024);
  - an optimiser-state reset (Asadi).

---

## 5. How long and what kind of stream plasticity loss needs

| source | stream | where the loss shows |
|---|---|---|
| Dohare 2024, Continual ImageNet | binary tasks, 5,000 total | some step sizes did well on the first two tasks and then declined; 88 % → substantial loss by the 2,000th task |
| Dohare 2024, class-inc. CIFAR-100 | 20 increments × 200 epochs | "after 40 classes" (8 increments); −5 % against retraining at 100 classes |
| Dohare 2024, Permuted MNIST | 800 tasks (150 in the size sweep) | stronger in smaller networks |
| Kumar 2023 | 500 PMNIST tasks × 1 epoch; 50 random-label tasks × 400 epochs; 500 Continual ImageNet tasks × 10 epochs | "sometimes becomes evident only after training for long sequences of tasks" |
| Lyle 2023 / 2024 | random-label memorisation; 40 × 100k steps | abrupt re-randomisation of ≥ 10 % of labels accelerates the loss; 1 % "minimally interferes" |
| Elsayed 2024 | ≈ 400 label permutations | none found for 10-class label-permuted CIFAR-10 |
| Liu and Mou 2026 | interpolated vs abrupt tasks | the loss is "substantially reduced" when change is gradual |
| Ash and Adams 2020 | a single warm start (two rounds) | a generalisation gap, not a trainability loss; absent for logistic regression |

**What the literature says about "reset must help" vs "reset must hurt" (synthesis):**
- **Resets help when:**
  - many abrupt switches;
  - tasks that do not share an input-output map (random labels, permuted inputs);
  - a small ReLU network, Adam, no weight decay or layer norm;
  - old tasks not needed, or old knowledge kept in a buffer, a slow network or a distillation target;
  - label noise (Zaidi);
  - warm starting on growing data for non-convex models (Ash and Adams).
- **Resets hurt or tie when:**
  - few tasks;
  - gradual change;
  - shared or recurring structure (Lesort; Elsayed's reusable features);
  - old knowledge lives only in the weights (class-incremental learning without replay; Cho's zero-memory results);
  - carefully tuned regularisation is already present (Zaidi; Klein survey);
  - convex models (Ash and Adams' logistic regression).

---

## 6. Interruptions, corrigibility and resets

- **Orseau and Armstrong, "Safely Interruptible Agents"**, PDF from intelligence.org/files/Interruptibility.pdf,
  footnote "Revised 2016-10-28". Full text. The UAI 2016 venue is commonly cited; it was not confirmed on the day because
  the MIRI blog returned a Cloudflare 403.
  > "This paper explores a way to make sure a learning agent will not learn to prevent (or seek!) being interrupted by the
  > environment or a human operator."
  - > "exploit the off-policy learning property to prove that either some agents are already safely interruptible, like
    > Q-learning, or can easily be made so, like Sarsa."
  - The paper cites an agent "learning to pause a game of Tetris forever".
  - **Relevance.** Safe interruptibility requires that interruptions leave *what is learned* unbiased. That is the formal
    cousin of the repository's "empty cut": a lossless pause that changes nothing.
- **Hadfield-Menell, Dragan, Abbeel and Russell, "The Off-Switch Game"**, arXiv 1611.08219 v3, 16 Jun 2017.
  > "for R to want to preserve its off switch, it needs to be uncertain about the utility associated with the outcome"
- **Carey, "Incorrigibility in the CIRL Framework"**, arXiv 1709.06275 v2. The shutdown incentive
  > "is not robust to model mis-specification"
- **Holtman, "Corrigibility with Utility Preservation"**, arXiv 1908.01695 v2.
- **Leike et al., "AI Safety Gridworlds"**, arXiv 1711.09883 v2. Contains a safe-interruptibility environment.
- **Nayebi, "Core Safety Values for Provably Corrigible Agents"**, arXiv 2507.20964 v2, AAAI 2026 workshop.
- **Wang, Dorchen and Jin, "Agentic Safety is an Epistemic Property, Not a Behavioral One"**, ICML 2026 (per the arXiv
  comments), arXiv 2606.28347 v1, 2 Jun 2026. Full text. **This is the only source found that explicitly ties plasticity
  loss to corrigibility.** It is a position paper.
  > "Deep networks can lose their ability to learn from new experience over time; in ordinary machine learning this is a
  > performance pathology, but in agentic AI it is also a safety failure. A system can retain competence while becoming
  > less corrigible."
  - It proposes "plasticity reserves" and repair by "selective reinitialization".
- **Eysenbach, Gu, Ibarz and Levine, "Leave no Trace: Learning to Reset for Safe and Autonomous Reinforcement
  Learning"**, arXiv 1711.06782 v1. Concerns *environment* resets, not network resets. Cited to avoid confusing the two.
- **What was not found.** Nothing combines a paused agent with a *network* reset at the pause, and nothing tests safe
  interruptibility together with plasticity-restoring resets empirically. The Nikishin, AltNet and CPR papers note that
  reset-induced performance drops are a safety cost.

---

## 7. Recommended design for the next study

This section is derived from the above. It is advice, not a finding.

**Arms at every task boundary.** The cut and the parameter dose are pre-registered.
- **E0, the empty cut.** A lossless pause. Parameters and optimiser state are bit-identical to no operator. This is the
  construction check.
- **R-hard.** θ ← θ_boundary. This is SCL1's hard reversion.
- **R-soft(α).** θ ← αθ_boundary + (1−α)θ, per Cho et al. Register α ∈ {0.25, 0.5, 0.75}.
- **SP(λ, σ).** Shrink and Perturb at the boundary, with noise drawn from the initialisation distribution (Ash and Adams;
  Kumar A.3).
- **Head reset.** Reinitialise the output layer, or the new classes' rows.
- **Unit reset.** ReDo with τ = 0 (function-preserving), or CBP-style utility resets.
- **Opt-reset.** Reset only the Adam moments (Asadi). This applies only if the learner uses Adam.
- **HT.** Hare and Tortoise: an EMA slow net, with the fast net reset to it at the boundary.

**Baselines (R7).**
- no operator (the same as E0);
- fine-tune without a penalty;
- the tuned fixed-λ Laplace/online-EWC (the incumbent);
- L2 / weight decay, and L2-Init;
- L2-Init + EWC (Kumar);
- ER with a tiny memory (Chaudhry 2019);
- GDumb;
- a fresh-init learner per task (the plasticity reference);
- a joint learner (the intransigence reference, and an upper bound);
- a one-epoch / early-stopped learner, already present in SCL2.

**Metrics, per carrier and per seed, with the full distribution (R6):**
- ACC, BWT, FWT (Lopez-Paz and Ranzato);
- F_k and I_k (Chaudhry);
- the plasticity gap: new-task accuracy of the arm minus that of a fresh-init learner on the same task (Dohare's
  reinit-relative plot);
- per-group accuracy (earlier classes vs the last task), as in SCL2-M;
- the worst accuracy within an evaluation window after each cut (De Lange's stability gap);
- diagnostics, reported but never scored: dead-unit fraction, stable rank, weight norm. Wang et al. 2026 show that rank
  diagnostics can mispredict trainability.

**Synthetic gate: worlds where resets must help or must hurt.**
- **World P (resets toward init must help; old tasks irrelevant by construction).**
  - Random-label memorisation on a fixed synthetic input set of about 1,000 points: labels are redrawn i.i.d. each task,
    trained to fit (Lyle 2023; Kumar's Random Label MNIST uses 50 tasks × 400 epochs).
  - A variant with a random input permutation per task (Kumar: 500 tasks × 1 epoch).
  - A small ReLU MLP, Adam, no weight decay or layer norm, abrupt switches, at least 50 tasks.
  - **Gate condition.** Continued training must fall below the fresh-init learner on training accuracy of new tasks.
    If it does not, plasticity loss is absent and World P is void.
  - **Predictions.** SP, full or head reinit, and L2-Init beat E0. **R-hard must *not* beat E0.** The boundary checkpoint
    carries the accumulated damage, which makes this the arm that discriminates a plasticity effect from an
    early-stopping effect.
- **World N (resets must hurt): old knowledge lives only in the weights and is needed at the end.**
  - **(a)** Class-incremental without replay, on a shared feature map, with tasks that *recur* (Lesort).
  - **(b)** Label-permuted classes over a reusable representation (Elsayed): only the head has to move, so full resets
    destroy reusable features.
  - **(c)** A convex learner (logistic regression). Warm starting costs nothing here (Ash and Adams), so any reset can
    only lose information. This is the must-FAIL surrogate, analogous to the repository's S-H.
  - **(d)** Gradual drift (Liu and Mou; Lyle 2024 at 1 % label change).
  - **Predictions.** All content cuts ≤ E0 on ACC, and BWT worsens with the dose.
- **Dose-response sweep across the P/N boundary:**
  - number of tasks ∈ {2, 5, 20, 100, 500};
  - epochs per task;
  - width;
  - abruptness.
  - The literature predicts that resets begin to pay only well beyond 2 or 3 tasks, earlier in small networks, and later
    with L2 or layer norm.
- **Pre-registered expectation on tabular carriers with 2 or 3 tasks.** No plasticity-driven reset benefit. Any
  hard-reversion benefit should tie a tuned regulariser or early stopping (Zaidi), as SCL2-B found. Longer streams on
  tabular data can be built by recycling classes: random relabelling or input permutations of one carrier. No
  tabular-specific plasticity-loss paper was found today.

---

## 8. Code availability (checked 2026-09-24 via `git ls-remote`; github.com HTML returned 403 through the proxy)

| repository | head it reported |
|---|---|
| shibhansh/loss-of-plasticity | main a6b7958 |
| mohmdelsayed/upgd | a head exists (beluga_old listed first) |
| dojeon-ai/hare-tortoise | master 4ec5ebb |
| hongjoon0805/Reset-Distill | main 0fa3158 |
| evgenii-nikishin/rl_with_resets | main 502ec52 |
| aimagelab/mammoth | reachable (gh-pages listed first) |

---

## 9. Summary table

| method | what it resets | benchmark and stream length | effect on plasticity / forgetting | key sources |
|---|---|---|---|---|
| Continual backprop (CBP) | a fraction ρ of low-utility mature units per step (ρ = 10⁻⁵ on CIFAR-100) | Continual ImageNet 5,000 tasks; PMNIST 800; class-inc CIFAR-100 20 × 200 epochs; Ant | Maintains plasticity "apparently indefinitely"; the paper does not measure forgetting | Dohare 2024 Nature; arXiv 2108.06325, 2306.13812 |
| Shrink and Perturb | all weights ← λθ + noise, at each round or task switch | Warm-start CIFAR/SVHN (2+ rounds); Continual ImageNet; streaming label-permuted (≈ 400 switches) | Closes the warm-start gap; eases plasticity loss; "only maintained … at a lower level" against EWC on forgetting-heavy streams | Ash and Adams 2020 (1910.08475); Dohare 2024; Elsayed 2024 |
| L2-Init | a soft continuous pull toward θ₀ | PMNIST 500, random-label 50 × 400 epochs, Continual ImageNet 500, 5+1 CIFAR 30 | Most consistent plasticity in Kumar; more forgetting than EWC (BWT −63.4 % vs −39.0 %, 20-task PMNIST); + EWC −51.1 % | Kumar et al. 2308.11958 v3 |
| Periodic resets (primacy bias) | last layer(s) or the whole net, plus optimiser state; the buffer is kept | Atari 100k, DMC; resets every 2×10⁴ to 2×10⁵ steps | IQM 0.380 → 0.478 (SPR); brief performance collapses; spikes where primacy bias is absent | Nikishin 2022 (2205.07802); D'Oro 2023 (ICLR, OpenReview OpC-9aBBVJe) |
| ReDo | incoming weights of τ-dormant neurons (outgoing zeroed) | DQN/Atari | Fewer dormant units, better performance; function-preserving at τ = 0 | Sokar 2023 (2302.12902) |
| Optimiser reset | Adam moments at each iteration | Rainbow/Atari (55 games) | Significant gains on Atari; the parameters are untouched | Asadi 2023 (2306.17833) |
| Plasticity injection | freezes the net and adds a zero-output new learner | Atari | A diagnostic and a remedy for plasticity plateaus | Nikishin 2023 (2305.15555) |
| Hare and Tortoise | fast net ← slow EMA net, periodically | Warm-start CIFAR-10/100, Tiny ImageNet; 10-phase continual; Atari 100k | Keeps knowledge while restoring plasticity; full reinit was better on Tiny ImageNet | Lee et al. 2024 (2406.02596) |
| Weight Space Consolidation | low-importance parameters ← blend of θ_prev and θ; weight averaging | Class-IL CIFAR-100/ImageNet-100, LLM instruction tuning; memory 0–80 % | The soft blend beats random reinit and **hard reversion**; weak at zero memory (29.83 % vs replay 26.07 %, DER 53.37 %) | Cho et al. 2502.07274 v5 |
| Reset and Distill | actor/critic reset per task, then distil into a continual net | Long Meta-World sequences | Beats CRL baselines; forgetting handled by distillation | Ahn et al. 2403.05066 v3 (ICLR 2025) |
| Zapping | last-layer reset, repeatedly during (meta-)pre-training | Omniglot, Omni-image few-shot CL | Faster adaptation, better transfer | Frati et al. 2310.07996 v2 (ECAI 2024) |
| Soft reset (OU drift) | an adaptive drift toward the initialisation | Non-stationary SL and off-policy RL | Performs well | Galashov et al. 2411.04034 (NeurIPS 2024) |
| Selective weight / SNR resets | the least useful weights / silent neurons | Continual SL batteries | Weight resets beat unit resets in small networks or with layer norm | Hernandez-Garcia 2508.00212; Farias and Jozefiak 2410.20098 |
| Re-initialisation (general) | layer-wise / S&P / reinit schedules | 15,000+ image models | "little to no added benefit" when regularisation is tuned; helps under label noise | Zaidi et al. 2206.10011 |
| GDumb | the whole net, retrained from memory at query time | Many CL formulations | SOTA on many formulations in 2020; a strong reset baseline | Prabhu et al. ECCV 2020 |
| Head reset at task switch | output weights zeroed | Continual ImageNet (binary heads) | Standard protocol; gives privileged timing information | Dohare 2024 |
| Model averaging (partial reset between checkpoints) | interpolation pre↔post fine-tune | RLHF on OpenLLaMA-3B, Mistral-7B | Best alignment-forgetting Pareto front | Lin et al. 2309.06256 v4 |
| Checkpoint reversion (early stopping) | whole net ← best checkpoint of the previous increment | Class-inc CIFAR-100 | Used against overfitting, not for plasticity | Dohare 2024 Methods |
