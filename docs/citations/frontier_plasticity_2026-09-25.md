# Citations checked on the day: the plasticity bottleneck and the prior art for H-REG (R10), 2026-09-25

This file records literature checked on the day for the hypothesis H-REG. H-REG is about to be declared from CRR's A6 and P3:
an EWC-style past term whose per-task Fisher penalties carry normalised age weights π_k ∝ q^age with Σπ_k = 1.
Nothing here is a result. Every number below is a number printed in a cited source. None was computed by this repository (R1).

**Fetch date.** Every source was fetched on 2026-09-25 (UTC), between 01:48 and 01:58 UTC, in this session.

**Raw material.** Saved under `scratchpad/lit0925/plasticity/` (session scratchpad, not committed):
- `abs_<id>.txt`: the arXiv abstract page (title, authors, submission history, comments, abstract).
- `ft_<id>.txt`: HTML full text. It comes from ar5iv (latest version) or from arxiv.org/html/<id>vN where a vN is named.
- `reply_pmc.txt`, `iclr_kurle.txt`, `gh_ewc_on.py`, `gh_ewc.py` and `cr_*.json` (Crossref metadata).
- `MANIFEST.sha256`: the sha256 of all 78 raw files.

Quotes were copied from those files. In the HTML full texts, inline maths is kept as its LaTeX alt-text, so some quotes
show `$...$`. Inside table cells, a literal `|` in a quote is written `\|` so the table does not break. Read `\|` as `|`,
and `\|\|` as `||`.

**Access, stated once.**
- **What loaded.**
  - arxiv.org abstract pages and arxiv.org/html full texts.
  - ar5iv.labs.arxiv.org.
  - nature.com (Dohare et al. full text).
  - pmc.ncbi.nlm.nih.gov. The Kirkpatrick et al. reply loaded in full. The same host was blocked on 2026-09-23.
  - api.crossref.org, and PubMed through its connector.
  - iclr.cc (the ICLR 2020 virtual poster page).
  - raw.githubusercontent.com (Mammoth and Avalanche source files).
  - `git ls-remote` to github.com: Mammoth HEAD `e75a491c69fd729edeb01431afb753d9157d9a81`, Avalanche HEAD
    `eb075be393e1f458b2c352514ff6c17b5a2c0f4e`.
- **What was blocked.**
  - openreview.net: the root answered 200, but `/pdf?id=` and `api2.openreview.net` answered 403. `/forum` answered a
    307 redirect. WebFetch of the PDF returned only a browser-verification page (a bot wall). Kurle et al. (ICLR 2020)
    was therefore read only from the ICLR virtual page (abstract).
  - api.semanticscholar.org answered 429 (rate limit). The semanticscholar.org root answered 200 but was not used.
  - www.pnas.org answered 403. The PNAS letters were read through PMC instead.
  - Europe PMC's REST full-text endpoint answered 500.
  - github.com HTML answered 403. api.github.com gave no usable response.
- **No 404s.** No link returned a 404.
- **Search.** WebSearch was used for discovery only. No quote below rests on a search rendering alone.
- **Titles checked.** Every arXiv id was checked against the title on its abstract page before use. All matched.

**Tags.**
- **[F]**: the full text (or the source file, for code) was opened and the quote read there.
- **[A]**: only the abstract page was read: arXiv abs, the ICLR virtual page, or PubMed metadata.
- **[S]**: a search rendering only. Unverified. Not used for any quote.
- **[title]**: the title was seen, not the content.

The dossier of 2026-09-24 (`docs/citations/plasticity_resets_2026-09-24.md`) covers the plasticity literature at greater
depth, with benchmark sizes. §1 below re-verifies its core items today and adds 2025–26 LLM work. §2, the prior art for
H-REG, is new.

---

## 1. Loss of plasticity: mechanism named, intervention proposed

| work | version and date | URL | quote (verbatim) | mechanism → intervention | tag |
|---|---|---|---|---|---|
| Dohare, Hernandez-Garcia, Lan, Rahman, Mahmood, Sutton, "Loss of plasticity in deep continual learning" | *Nature* 632, 768–774, published 2024-08-21 (Crossref), DOI 10.1038/s41586-024-07711-7; preprint arXiv 2306.13812 v3, 2024-04-09 | https://www.nature.com/articles/s41586-024-07711-7 | "standard deep-learning methods gradually lose plasticity in continual-learning settings until they learn no better than a shallow network"; "sustained deep learning requires a random, non-gradient component to maintain variability and plasticity"; "L2 regularization adds a penalty for large weights; augmenting backpropagation with this enabled the network to continue improving its learning performance over at least 5,000 tasks. The Shrink and Perturb algorithm11, which includes L2 regularization, also performed well." | loss of variability → continual backprop (reinitialise a small fraction of less-used units); L2; Shrink and Perturb | [F] |
| Lyle, Zheng, Nikishin, Avila Pires, Pascanu, Dabney, "Understanding plasticity in neural networks" | arXiv 2303.01486 v4, 2023-11-27; ICML 2023 (oral) | https://arxiv.org/abs/2303.01486 | "We find that loss of plasticity is deeply connected to changes in the curvature of the loss landscape, but that it often occurs in the absence of saturated units." | curvature change → parameterisation and optimisation choices (layer norm among them) | [A] |
| Lyle, Zheng, Khetarpal, van Hasselt, Pascanu, Martens, Dabney, "Disentangling the Causes of Plasticity Loss in Neural Networks" | arXiv 2402.18762 v1, 2024-02-29 | https://arxiv.org/abs/2402.18762 | "loss of plasticity can be decomposed into multiple independent mechanisms and that, while intervening on any single mechanism is insufficient to avoid the loss of plasticity in all cases, intervening on multiple mechanisms in conjunction results in highly robust learning algorithms"; "a combination of layer normalization and weight decay is highly effective at maintaining plasticity" | several independent mechanisms → layer norm + weight decay | [A] |
| Kumar, Marklund, Van Roy, "Maintaining Plasticity in Continual Learning via Regenerative Regularization" (L2 Init) | arXiv 2308.11958 v3, 2024-10-24 | https://arxiv.org/html/2308.11958v3 | "$\displaystyle\mathcal{L}_{\text{reg}}(\theta)=\mathcal{L}_{\text{train}}(\theta)+\lambda\|\|\theta-\theta_{0}\|\|_{2}^{2},$ where $\lambda$ is the regularization strength and $\theta_{0}$ is the vector of parameter values at time step $0$ ."; "EWC does not regularize towards initial parameters, but rather towards parameters at the end of each previous task. Thus, while EWC is designed to remember information about previous tasks, our method is designed to maintain plasticity."; Table 2: "EWC on its own, while having relatively poor plasticity, has less forgetting than L2 Init + EWC." | parameters drift away from a recruitable state → L2 pull to θ₀, one fixed λ, independent of the task count | [F] |
| Sokar, Agarwal, Castro, Evci, "The Dormant Neuron Phenomenon in Deep Reinforcement Learning" (ReDo) | arXiv 2302.12902 v2, 2023-06-13; ICML 2023 (oral) | https://arxiv.org/abs/2302.12902 | "an agent's network suffers from an increasing number of inactive neurons, thereby affecting network expressivity"; "ReDo ... Recycles Dormant neurons throughout training" | dormant units → recycle them | [A] |
| Nikishin, Schwarzer, D'Oro, Bacon, Courville, "The Primacy Bias in Deep Reinforcement Learning" | arXiv 2205.07802 v1, 2022-05-16; ICML 2022 | https://arxiv.org/abs/2205.07802 | "a tendency to rely on early interactions and ignore useful evidence encountered later"; "tackles the primacy bias by periodically resetting a part of the agent" | overfitting to early data → periodic partial resets | [A] |
| Nikishin, Oh, Ostrovski, Lyle, Pascanu, Dabney, Barreto, "Deep Reinforcement Learning with Plasticity Injection" | arXiv 2305.15555 v2, 2023-10-03; NeurIPS 2023 | https://arxiv.org/abs/2305.15555 | "plasticity injection, a minimalistic intervention that increases the network plasticity without changing the number of trainable parameters or biasing the predictions" | (diagnostic) → add a fresh sub-network whose initial output is cancelled | [A] |
| Ash, Adams, "On Warm-Starting Neural Network Training" | arXiv 1910.08475 v3, 2020-12-31; NeurIPS 2020 | https://ar5iv.labs.arxiv.org/html/1910.08475 | "$\theta_{i}^{t}\leftarrow\lambda\theta_{i}^{t-1}+p^{t}$ , where $p^{t}\sim\mathcal{N}(0,\,\sigma^{2})$ and $0<\lambda<1$ ."; "For warm-started models, gradients from new, unseen data tend to be much larger magnitude than those from data the model has seen before."; "The success of the shrink and perturb trick may lie in its ability to standardize gradients while preserving a model's learned hypothesis." | warm-start generalisation gap and gradient imbalance → shrink and perturb at each round | [F] |
| Abbas, Zhao, Modayil, White, Machado, "Loss of Plasticity in Continual Deep Reinforcement Learning" | arXiv 2303.07507 v1, 2023-03-13 | https://arxiv.org/abs/2303.07507 | "the activation footprint of the network becomes sparser, contributing to the diminishing gradients"; "Concatenated ReLUs (CReLUs) activation function" | sparse activations, vanishing gradients → CReLU | [A] |
| Elsayed, Mahmood, "Addressing Loss of Plasticity and Catastrophic Forgetting in Continual Learning" (UPGD) | arXiv 2404.00781 v2, 2024-04-30; ICLR 2024 | https://arxiv.org/abs/2404.00781 | "applies smaller modifications to more useful units, protecting them from forgetting, and larger modifications to less useful units, rejuvenating their plasticity" | forgetting and plasticity loss together → utility-gated perturbed gradient descent | [A] |
| Klein, Luther, McAuliffe, Miklautz, Plant, Tschiatschek, "Plasticity Loss in Deep Reinforcement Learning: A Survey" | arXiv 2411.04832 v3, 2026-04-18 | https://arxiv.org/abs/2411.04832 | "organize over 50 mitigation strategies into the first comprehensive taxonomy of the field"; "general regularization techniques often outperform domain-specific interventions" | survey | [A] |
| Hernandez-Garcia, Figliolia, Millidge, "Can Scale Save Us From Plasticity Loss in Large Language Models?" | arXiv 2606.24752 v1, 2026-06-23 | https://arxiv.org/abs/2606.24752 | "the onset of plasticity loss follows a predictable scaling law, growing sublinearly with model size"; "We also find evidence of plasticity loss under stationary multilingual training" | plasticity loss in GPT-style LLMs, 5M–314M parameters → none proposed; scale alone insufficient | [A] |
| Springer, Goyal, Wen, Kumar, Yue, Malladi, Neubig, Raghunathan, "Overtrained Language Models Are Harder to Fine-Tune" | arXiv 2503.19206 v2, 2025-03-28 | https://arxiv.org/abs/2503.19206 | "extended pre-training can make models harder to fine-tune, leading to degraded final performance. We term this phenomenon catastrophic overtraining."; "arises from a systematic increase in the broad sensitivity of pre-trained parameters to modifications" | parameter sensitivity grows with the token count → reassess the pretraining budget | [A] |
| Han, Bordt, Zhang, Kakade, "Weight Decay Improves Language Model Plasticity" | arXiv 2602.11137 v2, 2026-05-28 | https://arxiv.org/abs/2602.11137 | "larger weight decay increases the plasticity of the pretrained model, resulting in greater performance gains downstream after fine-tuning" | pretraining hyperparameters → larger weight decay | [A] |
| Zheng, Cai, Qiu, Ma, "Spurious Forgetting in Continual Learning of Language Models" | arXiv 2501.13453 v1, 2025-01-23; ICLR 2025 | https://arxiv.org/abs/2501.13453 | "such performance drops often reflect a decline in task alignment rather than true knowledge loss"; "we introduce a Freezing strategy that fix the bottom layers of the model" | early steps disrupt task alignment → freeze the bottom layers | [A] |
| Guo, Fu, Zhang, Zhao, Shen, "Efficient Continual Pre-training by Mitigating the Stability Gap" | arXiv 2406.14833 v2, 2024-06-27 | https://arxiv.org/abs/2406.14833 | "we observed a temporary performance drop at the beginning, followed by a recovery phase, a phenomenon known as the "stability gap,"" | stability gap in LLM continual pretraining → subset multi-epoch, high-quality sub-corpus, pretraining-like mixture | [A] |
| Ibrahim, Thérien, Gupta, Richter, Anthony, Lesort, Belilovsky, Rish, "Simple and Scalable Strategies to Continually Pre-train Large Language Models" | arXiv 2403.08763 v4, 2024-09-04 | https://arxiv.org/abs/2403.08763 | "a simple and scalable combination of learning rate (LR) re-warming, LR re-decaying, and replay of previous data is sufficient to match the performance of fully re-training from scratch on all available data" | distribution shift → LR re-warm/re-decay + replay | [A] |
| Liu et al., "Representation Collapse in Sequential Post-Training of Large Language Models" | arXiv 2605.30524 v1, 2026-05-28 ("work in progress") | https://arxiv.org/abs/2605.30524 | "The central hypothesis is that excessive representation concentration is not merely a geometric curiosity: it predicts reduced plasticity during later adaptation" | representation concentration → replay, feature refresh, diversity regularisation (a hypothesis, per the abstract) | [A] |

**What §1 says about regularisers (sourced).**
- A pull toward a *fixed* point with a *fixed* strength that does not grow with the task count restores plasticity: L2,
  L2 Init and weight decay (Dohare; Kumar; Lyle 2024; Han).
- A pull toward the *previous task's* parameters (EWC) is recorded as costing plasticity (Kumar Table 2).

---

## 2. The prior-art question for H-REG

**H-REG, as specified to this check.**
- **Penalty.** Σ_k π_k (θ − θ*_k)ᵀ F_k (θ − θ*_k).
- **Weights.** π_k ∝ q^age, normalised to Σ_k π_k = 1.
- **Strength.** The total strength stays at one task's Laplace strength whatever the task count T.
- **Anchor.** Completing the square, the penalty equals (θ − θ̄)ᵀ F̄ (θ − θ̄) + const, with F̄ = Σπ_k F_k and
  θ̄ = F̄⁻¹ Σ π_k F_k θ*_k.
- **Alternative.** Bayes/Laplace accumulation, whose strength grows with T.

### 2.1 Sources

| work | version and date | URL | quote (verbatim) | tag |
|---|---|---|---|---|
| Kirkpatrick et al., "Overcoming catastrophic forgetting in neural networks" (EWC) | arXiv 1612.00796 v2, 2017-01-25; *PNAS* 114 (2017), DOI 10.1073/pnas.1611835114 | https://ar5iv.labs.arxiv.org/html/1612.00796 | "When moving to a third task, task C, EWC will try to keep the network parameters close to the learned parameters of both task A and B. This can be enforced either with two separate penalties, or as one by noting that the sum of two quadratic penalties is itself a quadratic penalty."; "For each task, a penalty is added with anchor point given by the current value of the parameters and with weights given by the Fisher information matrix times a scaling factor $\lambda$ which was optimized by hyperparameter search." | [F] |
| Huszár, "On Quadratic Penalties in Elastic Weight Consolidation" | arXiv 1712.03847 v1, 2017-12-11; *PNAS* 115(11) E2496–E2497 (2018-02-20), DOI 10.1073/pnas.1717042115, PMID 29463735 | https://ar5iv.labs.arxiv.org/html/1712.03847 | "our derivation suggests that only a single penalty should be maintained, and it should be anchored at $\theta^{\ast}_{S}$ , where $S$ is the latest task learned."; "By placing a penalty around both $\theta^{\ast}_{A}$ and $\theta^{\ast}_{B}$ we are essentially double-counting the data from task $A$ ."; "To a degree this systematic bias can be counterbalanced by setting $\lambda_{T}$ such that EWC assigns higher importance to tasks learned later." | [F] |
| Kirkpatrick et al., "Reply to Huszár: The elastic weight consolidation penalty is empirically valid" | *PNAS* 115(11) E2498 (2018-02-20), DOI 10.1073/pnas.1800157115, PMID 29463734, PMC5856563 | https://pmc.ncbi.nlm.nih.gov/articles/PMC5856563/ | "we used Bayesian evidence accumulation as an inspiration rather than a dogma"; "Our penalty forces the network to remember older tasks more vividly, which might compensate for the fact that older tasks are harder to remember."; "it may be practically better to keep the regularization penalty tied to the point where the Fisher was computed." | [F] |
| Schwarz, Luketina, Czarnecki, Grabska-Barwinska, Teh, Pascanu, Hadsell, "Progress & Compress" (online EWC) | arXiv 1805.06370 v2, 2018-07-02; ICML 2018 | https://ar5iv.labs.arxiv.org/html/1805.06370 | "the accumulation of Fisher regularisers can over-constrain the network parameters leading to impaired learning of new tasks"; "where $\gamma<1$ is a hyperparameter associated with removing the approximation term associated with the previous presentation of task $i$"; "the method can, via the $\gamma$ down-weighting, explicitly forget older tasks in a graceful and controlled (rather than catastrophic) manner"; "Without forgetting, EWC misbehaves when the model runs out of capacity"; App. A: "The difference between EWC and online-EWC is in their weighting of the past experiences, with EWC putting more weight on the initial tasks and online-EWC favouring the most recent past." Reported settings: "online EWC ( $\lambda=17.5,\gamma=0.95)$", "P&C ( $\lambda=15.0,\gamma=0.99)$". | [F] |
| Chaudhry, Dokania, Ajanthan, Torr, "Riemannian Walk for Incremental Learning: Understanding Forgetting and Intransigence" (EWC++, RWalk) | arXiv 1801.10112 v3, 2018-08-14; ECCV 2018, DOI 10.1007/978-3-030-01252-6_33 | https://ar5iv.labs.arxiv.org/html/1801.10112 | "We define intransigence as the inability of a model to learn new tasks."; "Intuitively, if a model is heavily regularized over previous tasks to preserve knowledge, it will forget less but have high intransigence."; "$I_{k}=a_{k}^{*}-a_{k,k}\ ,$"; "$F_{\theta}^{t}=\alpha F_{\theta}^{t}+(1-\alpha)F_{\theta}^{t-1}\ ,$ ... $t$ represents the training iterations"; "At the end of each task, we simply store $F_{\theta}^{t}$ as $F_{\theta^{k-1}}$ and use it to regularize the next task" | [F] |
| Ritter, Botev, Barber, "Online Structured Laplace Approximations For Overcoming Catastrophic Forgetting" | arXiv 1805.07810 v1, 2018-05-20 | https://ar5iv.labs.arxiv.org/html/1805.07810 | "$\Lambda_{t+1}=\lambda H_{t+1}(\mu_{t+1})+\Lambda_{t}$"; "This hyperparameter provides a way of trading off retaining performance on previous tasks against having sufficient flexibility for learning a new one."; "Using a large value of $\lambda=100$ ... the network's performance now stays at a high level — for the Kronecker factored approximation it remembers it perfectly — which comes at the cost of being unable to learn new tasks well." | [F] |
| Loo, Swaroop, Turner, "Generalized Variational Continual Learning" | arXiv 2011.12328 v1, 2020-11-24 | https://ar5iv.labs.arxiv.org/html/2011.12328 | "We will now show that surprisingly as $\beta\rightarrow 0$ , we recover a special case of Online EWC."; "our derivation produces an implicit value of $\lambda=1$ , i.e. equal weight between tasks of equal sample count. In practice it is found that algorithms such as Online EWC perform best when $\lambda>1$ , typically $10-1000$ ."; "we view this $\lambda$ hyperparameter as a form of cold posterior regularization"; "Note that in Online EWC, there is another parameter $\gamma$ , that down-weights the previous Fisher matrices. ... we can introduce this hyperparameter by taking the KL divergence priors and posteriors at different temperatures ... However, we do not find that this approach improves performance." | [F] |
| Kurle, Cseke, Klushyn, van der Smagt, Günnemann, "Continual Learning with Bayesian Neural Networks for Non-Stationary Data" | ICLR 2020 (virtual poster SJlsFpVtDB). OpenReview PDF 403, so the version was not seen | https://iclr.cc/virtual_2020/poster_SJlsFpVtDB.html | "Furthermore, we propose Bayesian forgetting and a Gaussian diffusion process for adapting to non-stationary data." The defining equation was **not read** (bot wall). | [A] |
| Bonnet, Cottart, Hirtzlin, Januel, Dalgaty, Vianello, Querlioz, "Bayesian continual learning and forgetting in neural networks" (MESU) | arXiv 2504.13569 v1, 2025-04-18; *Nature Communications* 16, 9614 (2025-10-30), DOI 10.1038/s41467-025-64601-w (Crossref) | https://arxiv.org/html/2504.13569v1 | "First, all tasks are treated equally, even those that have grown less relevant over time, potentially leading to capacity issues."; "we introduce a forgetting mechanism using a truncated posterior ... where the model only retains the last $N$ tasks"; "when $N$ approaches infinity, the forgetting effect disappears. Over long time scales, we show in Methods that $\bm{\sigma}^{2}$ then scales as $(H_{D}(\bm{\mu}_{0})t)^{-1}$ . This parallels how EWC/SI accumulate importance estimates over time."; "choosing a finite $N$ ensures that $\bm{\sigma}^{2}$ instead converges to $\frac{1}{N}\frac{1}{H_{D}(\bm{\mu}_{0})+\frac{1}{N\bm{\sigma}_{\text{prior}}^{2}}}$ ... Thus, MESU retains some plasticity rather than freezing all parameters completely"; "FOO-VB Diagonal, which applies Bayesian updates without forgetting, attempts to retain all information indefinitely, eventually exhausting the capacity of the network. As new tasks are presented, its plasticity collapses" | [F] |
| Titsias, Galashov, Rannen-Triki, Pascanu, Teh, Bornschein, "Kalman Filter for Online Classification of Non-Stationary Data" | arXiv 2306.08448 v1, 2023-06-14; ICLR 2024 | https://ar5iv.labs.arxiv.org/html/2306.08448 | "$=\mathcal{N}(w_{n}\|\gamma_{n}w_{n-1},(1-\gamma_{n}^{2})\sigma_{w}^{2}I),\ \ n\geq 1.\ \ \ \ \text{Parameter drift}$"; "The time-dependent parameter $\gamma_{n}$ takes values in $[0,1]$ and quantifies the memory or forgetting of the process."; "Hence, the variance $\sigma_{w}^{2}$ of the regression parameters remains constant through time."; "$m_{n}^{-}=\gamma_{n}m_{n-1},\ \ \ A_{n}^{-}=\gamma_{n}^{2}A_{n-1}+(1-\gamma_{n}^{2})\sigma_{w}^{2}I.$" | [F] |
| Lai, Bernstein, "Generalized Forgetting Recursive Least Squares: Stability and Robustness Guarantees" | arXiv 2308.04259 v3, 2024-05-06; IEEE TAC (per arXiv comments, November 2024 issue) | https://arxiv.org/html/2308.04259v2 (v2 HTML read; v3 is the latest listed) | "A classical method to introduce forgetting in RLS is called exponential forgetting, where a forgetting factor $0<\lambda\leq 1$ is introduced which provides exponentially higher weighting to more recent measurements and data"; the cost (eq. 37) is quoted below the table; "$\displaystyle=\lambda P_{k}^{-1}+\phi_{k}^{\rm T}\phi_{k},$" (eq. 38, for $P_{k+1}^{-1}$) | [F] |
| Kessler, Cobb, Rudner, Zohren, Roberts, "On Sequential Bayesian Inference for Continual Learning" | arXiv 2301.01828 v3, 2025-01-07; *Entropy* 25(6) 884, DOI 10.3390/e25060884 | https://arxiv.org/abs/2301.01828 | "We find that this approach fails to prevent catastrophic forgetting demonstrating the difficulty in performing sequential Bayesian inference in neural networks."; "we discuss how task data imbalances can cause forgetting" | [A] |
| Lee, Kim, Jun, Ha, Zhang, "Overcoming Catastrophic Forgetting by Incremental Moment Matching" (IMM) | arXiv 1703.08475 v3, 2018-01-30; NIPS 2017 | https://ar5iv.labs.arxiv.org/html/1703.08475 | "Mean-IMM averages the parameters of two networks in each layer, using mixing ratios $\alpha_{k}$ with $\sum^{K}_{k}\alpha_{k}=1$ ."; mode-IMM: "$\displaystyle\mu^{*}_{1:K}=\Sigma^{*}_{1:K}\cdot(\mbox{$\sum^{K}_{k}$}\alpha_{k}\Sigma^{-1}_{k}\mu_{k})$", "$\displaystyle\Sigma^{*}_{1:K}=(\mbox{$\sum^{K}_{k}$}\alpha_{k}\Sigma^{-1}_{k})^{-1}$", "For covariance, we use the inverse of a Fisher information matrix"; "transfer techniques break this assumption; thus the optimal $\alpha$ is shifted to larger than $1/k$ ." | [F] |
| Matena, Raffel, "Merging Models with Fisher-Weighted Averaging" | arXiv 2111.09832 v2, 2022-08-26 | https://ar5iv.labs.arxiv.org/html/2111.09832 | "$\theta^{*}=\text{argmax}_{\theta}\sum_{i}\lambda_{i}\log p(\theta\|\theta_{i},I)$ where $\lambda_{i}\geq 0,\sum_{i}\lambda_{i}=1$ ."; "$\theta^{*(j)}=\frac{\sum_{i=1}^{M}\lambda_{i}F_{i}^{(j)}\theta_{i}^{(j)}}{\sum_{i=1}^{M}\lambda_{i}F_{i}^{(j)}},$" | [F] |
| Marouf, Roy, Tartaglione, Lathuilière, "Weighted Ensemble Models Are Strong Continual Learners" (CoMA, CoFiMA) | arXiv 2312.08977 v4, 2024-12-11; ECCV 2024 | https://arxiv.org/html/2312.08977 | "Note that, when $\lambda=\frac{1}{t}$ , Eq. (3) is strictly equivalent to the average in Eq. (2) ... However, our experiments highlight that such a parameter choice might result in suboptimal performances"; "we propose to perform a non-uniform averaging giving higher importance to the latest tasks ... This is obtained by using a constant weight parameter $\lambda$ ."; "$\boldsymbol{\theta}^{*}=\frac{\sum_{t=1}^{T}\mbox{\bf F}_{t}\boldsymbol{\theta}_{t}}{\sum_{t=1}^{T}\mbox{\bf F}_{t}},$" (eq. 6); "$\boldsymbol{\theta}_{t}^{*}=\frac{\lambda\mbox{\bf F}_{t}\boldsymbol{\theta}_{t}+(1-\lambda)\mbox{\bf F}_{t-1}\boldsymbol{\theta}^{*}_{t-1}}{\lambda\mbox{\bf F}_{t}+(1-\lambda)\mbox{\bf F}_{t-1}},$" (eq. 7); "We set the batch size to 128, $\lambda\!=\!0.4$ for supervised and $\lambda\!=\!0.2$ for self-supervised pre-training" | [F] |
| Tomilin et al., "MEAL: A Benchmark for Continual Multi-Agent Reinforcement Learning" | arXiv 2506.14990 v3, 2026-06-18; ICML 2026 (per arXiv comments) | https://arxiv.org/html/2506.14990v3 | "across 10 tasks, both methods appear similarly stable, since the accumulated Fisher penalty in EWC has not yet become overly restrictive. Over 100 tasks, however, standard EWC increasingly over-regularizes the shared backbone, limiting plasticity and leading to earlier performance saturation, whereas Online EWC retains capacity by exponentially decaying past importance weights."; App. I.1: "The regularizer grows with every task, anchoring the network more tightly to older solutions. Consequently, plasticity decays over time"; "EWC's cumulative Fisher anchors performance but pulls the shared trunk toward a compromise averaged over all past tasks, washing out their task-specific role structure." | [F] |
| Rahman, Coull, Wright, "On the Limitations of Continual Learning for Malware Classification" | arXiv 2208.06568 v1, 2022-08-13; CoLLAs 2022 | https://ar5iv.labs.arxiv.org/html/2208.06568 | "The quadratic term of the regularization loss grows linearly with the increase of task which hinders to enable EWC be truly applicable in a practical continual learning scenario where the tasks keep growing." | [F] |
| Kim, "Non-Equilibrium Stochastic Dynamics as a Unified Framework for Insight and Repetitive Learning: A Kramers Escape Approach to Continual Learning" | arXiv 2604.04154 v1, 2026-04-05 | https://arxiv.org/abs/2604.04154 | "we identify the EWC penalty term as an energy barrier whose height grows linearly with the number of accumulated tasks, yielding an exponential collapse of the transition rate predicted analytically and confirmed numerically" | [A] (full text fetched; only the abstract claim is quoted) |
| Mammoth (aimagelab), `models/ewc_on.py` | HEAD `e75a491c69fd729edeb01431afb753d9157d9a81` (git ls-remote, 2026-09-25) | https://raw.githubusercontent.com/aimagelab/mammoth/master/models/ewc_on.py | `self.fish *= self.args.gamma` / `self.fish += fish` / `self.checkpoint = self.net.get_params().data.clone()`; `penalty = self.args.e_lambda * (self.fish * ((self.net.get_params() - self.checkpoint) ** 2)).sum()` | [F] (code) |
| Avalanche (ContinualAI), `avalanche/training/plugins/ewc.py` | HEAD `eb075be393e1f458b2c352514ff6c17b5a2c0f4e` (git ls-remote, 2026-09-25) | https://raw.githubusercontent.com/ContinualAI/avalanche/master/avalanche/training/plugins/ewc.py | docstring: "`separate` to keep a separate penalty for each previous experience. `online` to keep a single penalty summed with a decay factor over all previous tasks." (line breaks removed); update: `init_tensor=self.decay_factor * old_imp.expand(curr_imp.shape)` / `+ curr_imp.data,` | [F] (code) |

Also opened, not quoted:
- Adel, "The Bayesian Approach to Continual Learning: An Overview", arXiv 2507.08922 v3, 2026-07-05. [A]; the abstract has
  no statement on forgetting weights.
- Nguyen, Li, Bui, Turner, "Variational Continual Learning", arXiv 1710.10628 v3. [A]

Two further sources, from Online EWC's own record (P&C eq. (9), [F] above), fix the online-EWC recursion:

> "$\displaystyle F^{*}_{i}=\gamma F^{*}_{i-1}+F_{i}$"

> "$\displaystyle-\log p(\mathcal{T}_{i}|\theta)+\frac{1}{2}\|\theta-\theta^{*}_{i-1}\|^{2}_{\gamma F^{*}_{i-1}}$" (eq. 8)

The same recursion appears in MEAL App. I.1 (eq. 10) as "$F^{(k)}_{\text{online}}=\gamma F^{(k-1)}_{\text{online}}+F_{k},$" with
"the decay factor $\gamma\in(0,1)$".

RLS with exponential forgetting, the cost (Lai & Bernstein eq. 37, [F]):

> "$\displaystyle J_{k}(\hat{\theta})=\sum_{i=0}^{k}\lambda^{k-i}\|y_{i}-\phi_{i}\hat{\theta}\|^{2}+\lambda^{k+1}\|\theta-\theta_{0}\|_{P_{0}^{-1}}^{2}$"

Huszár's decomposition of the single penalty into per-task penalties (eq. 12–13, [F]) shows the two anchorings can be
converted into each other:

> "$\displaystyle\frac{1}{2}\sum_{i}\left(\sum_{t\leq T}\lambda_{t}F_{t,i}+\lambda_{\text{prior}}\right)(\theta_{i}-\theta^{\ast}_{T,i})^{2}=\frac{1}{2}\sum_{t\leq T}\sum_{i}\lambda_{t}F_{t,i}(\theta_{i}-\tilde{\theta}_{t,i})^{2}+\lambda_{\text{prior}}\sum_{i}\theta_{i}^{2}+\text{constant},$"

### 2.2 Classification against H-REG's three features

The three features are:
- **(a)** the weights decay geometrically with age;
- **(b)** the weights are normalised to a fixed total (Σ = 1), so the strength does not grow with T;
- **(c)** the anchor: the Fisher-weighted mean of past optima ("mean"), the last parameters ("last"), or another point.

Each cell is read off the defining equation or sentence quoted in §2.1.

| method | (a) geometric decay | (b) normalised, fixed total | (c) anchor | penalty or merge |
|---|---|---|---|---|
| EWC, separate penalties (Kirkpatrick 2017; Avalanche `mode="separate"`) | no (one λ for every task) | no: the total grows with T (Rahman; MEAL; Kim) | mean: the sum of per-task penalties, each anchored at its own θ*_t, is one quadratic around the Fisher-weighted mean (Kirkpatrick's "sum of two quadratic penalties") | penalty |
| Huszár single-penalty Laplace (eq. 11) / Ritter online Laplace | no | no: Λ_{t+1} = λH_{t+1} + Λ_t | last: θ*_S, the latest task | penalty |
| Online EWC (Schwarz 2018; Mammoth `ewc_on`; Avalanche `mode="online"`) | **yes**, γ per task: F*_i = γF*_{i−1} + F_i | no: unnormalised; the total tends to about F̄/(1−γ) for stationary F, bounded but not fixed at small T | last: θ*_{i−1} | penalty |
| EWC++ (Chaudhry 2018) | **yes**, but per *training iteration* (α per step), not per task | **yes**: a convex combination α, (1−α) of Fishers (a moving average) | last: θ^{k−1} | penalty |
| RLS with exponential forgetting (Lai & Bernstein, eq. 37–38) | **yes**, λ^{k−i} | no: P⁻¹ = λP⁻¹ + φᵀφ, a discounted sum | the running estimate (a filter, not a penalty) | filter |
| Kalman drift (Titsias 2023) | **yes**, γ_n per step, learned online | the posterior precision is bounded by the drift process, not by normalisation | the mean shrinks toward the prior mean: m⁻ = γm | filter |
| MESU (Bonnet 2025) | no: a truncated window of the last N tasks (Bayesian, equal weight inside the window) | **bounded**: σ² tends to about 1/(N·H), a fixed window size, independent of t | variational mean | Bayesian update |
| Bayesian forgetting (Kurle 2020) | not verified (defining equation not read) | not verified | not verified | Bayesian update |
| GVCL (Loo 2020) | the γ variant is introduced via temperatures and was "not found" to help | no: λ is a cold-posterior multiplier, typically 10–1000 in online EWC | last (VCL prior = previous posterior) | penalty (KL) |
| mode-IMM (Lee 2017) | no (α tuned; 1/k named as the Bayesian default) | **yes**: Σα_k = 1 | **mean**: μ* = (Σα_kΣ_k⁻¹)⁻¹Σα_kΣ_k⁻¹μ_k, with Σ_k⁻¹ from the Fisher | merge after training |
| Fisher merging (Matena 2021) | no | **yes**: Σλ_i = 1 | **mean**: Σλ_iF_iθ_i / Σλ_iF_i | merge |
| CoFiMA (Marouf 2024) | **yes**, approximately: a constant λ recursion "giving higher importance to the latest tasks" (eq. 7 uses F_{t−1}, not an accumulated Fisher) | **yes**: λ, (1−λ) | **mean**: eq. 6 is exactly Σ_tF_tθ_t / Σ_tF_t | merge after each task |
| L2 Init (Kumar 2024) | n/a | **yes, trivially**: one fixed λ, independent of T | θ₀ (initial parameters) | penalty |
| De Lange 2023 stability/plasticity split | n/a | **yes**: α and (1−α) on the present and past gradients | n/a | gradient weighting |

---

## 3. The stability–plasticity trade-off and a weight set by gradient-norm balancing

| work | version and date | URL | quote (verbatim) | tag |
|---|---|---|---|---|
| De Lange, van de Ven, Tuytelaars, "Continual evaluation for lifelong learning: Identifying the stability gap" | arXiv 2205.13452 v2, 2023-03-30; ICLR 2023 (spotlight) | https://ar5iv.labs.arxiv.org/html/2205.13452 | "we disentangle the continual learning gradients of the objective $\mathcal{L}$ in $\alpha$ -weighed plasticity and stability gradients $\nabla\mathcal{L}=\alpha\nabla\mathcal{L}_{\text{plasticity}}+(1-\alpha)\nabla\mathcal{L}_{\text{stability}}$"; "directly after the task transition, we indeed have $\|\|\nabla\mathcal{L}_{\text{stability}}\|\|\approx 0$ because the replayed samples are exclusively from $T_{1}$ ."; "Due to the imbalance of the stability and plasticity gradients, the plasticity gradient will dominate and potentially result in forgetting." | [F] |
| Ash, Adams (as in §1) | arXiv 1910.08475 v3 | https://ar5iv.labs.arxiv.org/html/1910.08475 | Fig. 5 caption: "Our proposed trick balances these respective magnitudes while still allowing models to benefit from their first round of training"; "These imbalanced gradient contributions are known to be problematic for optimization in mutli-task learning scenarios" | [F] |
| Chen, Badrinarayanan, Lee, Rabinovich, "GradNorm" | arXiv 1711.02257 v4, 2018-06-12; ICML 2018, PMLR 793–802 | https://arxiv.org/abs/1711.02257 | "a gradient normalization (GradNorm) algorithm that automatically balances training in deep multitask models by dynamically tuning gradient magnitudes"; "despite only involving a single asymmetry hyperparameter $\alpha$" | [A] |
| Esser, Rombach, Ommer, "Taming Transformers for High-Resolution Image Synthesis" (the VQGAN adaptive weight) | arXiv 2012.09841 v3, 2021-06-23 | https://ar5iv.labs.arxiv.org/html/2012.09841 | "$\lambda=\frac{\nabla_{G_{L}}[\mathcal{L}_{\text{rec}}]}{\nabla_{G_{L}}[\mathcal{L}_{\text{GAN}}]+\delta}$ ... $\nabla_{G_{L}}[\cdot]$ denotes the gradient of its input w.r.t. the last layer $L$ of the decoder, and $\delta=10^{-6}$ is used for numerical stability." | [F] |
| Guo, Liu, Yang, Rosing, "Improved Schemes for Episodic Memory-based Lifelong Learning" (MEGA) | arXiv 1909.11763 v7, 2020-12-15; NeurIPS 2020 (spotlight) | https://ar5iv.labs.arxiv.org/html/1909.11763 | "both A-GEM and GEM always put the same emphasis on the current task, regardless of how the loss changes over time"; MEGA-I: "$\alpha_{1}(w)=1,\alpha_{2}(w)=\ell_{\text{ref}}(w;\zeta)/\ell_{t}(w;\xi)$" when "$\ell_{t}(w;\xi)>\epsilon$" | [F] |
| Qiang et al., "On the Plasticity and Stability for Post-Training Large Language Models" (PCR) | arXiv 2602.06453 v1, 2026-02-06 | https://arxiv.org/abs/2602.06453 | "We identify a root cause as the geometric conflict between plasticity and stability gradients, which leads to destructive interference."; "PCR dynamically arbitrates conflicts via an uncertainty-aware "soft projection" mechanism" | [A] |
| Prashant, Zhu, Creo, Salimi, "Fine-Tuning Without Forgetting via Loss-Adaptive Learning Rates" (FINCH) | arXiv 2605.20005 v1, 2026-05-19 | https://arxiv.org/abs/2605.20005 | "per-step forgetting is bounded by the product of the learning rate and the square root of the current training loss"; "FINCH reduces forgetting by 93% on average while matching the task performance of standard fine-tuning" | [A] |

**Found and not found (sourced, then labelled).**
- **Sourced.** Several sources name the balance of the *gradient magnitudes* of old and new data as the mechanism:
  - Ash and Adams: shrink and perturb "balances these respective magnitudes".
  - De Lange et al.: the stability gradient is ≈ 0 at the task switch, so the plasticity gradient dominates.
  - Qiang et al.: gradient conflict.
- **Sourced.** Published weights set by a gradient-norm ratio or a loss ratio exist: GradNorm, the VQGAN adaptive weight
  and MEGA-I.
- **Not found (inference, labelled).** Among the sources read, none sets a *regulariser* weight (EWC λ) by gradient-norm
  balancing in continual learning. That is not evidence that no such paper exists.
- **Already covered.** The closest published object for the repository's Ω rule is still the VQGAN weight
  (`Continuous_Learning/ADAM_AND_PRIOR_ART.md` B1).

---

## 4. Bearing on H-REG (inference, labelled as such)

Everything in this section is my inference from the sources above. None of it is a sourced claim, and none of it is a
result. The algebra below is elementary (completing the square; geometric series). No script prints it, so it carries no
number, and it enters no ledger row.

### 4.1 Which prior work is closest

1. **For the penalty's form, the closest is EWC with separate penalties.**
   - That is Kirkpatrick et al. 2017, implemented as Avalanche `mode="separate"`.
   - Its sum of per-task penalties, each anchored at its own θ*_t, is exactly H-REG's anchoring. Kirkpatrick et al. say
     so themselves ("the sum of two quadratic penalties is itself a quadratic penalty"). The minimum of that sum is the
     Fisher-weighted mean of past optima.
   - H-REG = separate-penalty EWC with per-task weights λ_t = λπ_t.
   - Huszár (2017/18) already raises per-task λ_t: "setting λ_T such that EWC assigns higher importance to tasks learned
     later". He calls the multi-anchor form a double count. Kirkpatrick et al.'s reply defends it on empirical grounds:
     it makes the network "remember older tasks more vividly".
   - So the *anchor* choice in H-REG is a known and disputed choice, not a new one.
2. **For the weights, the closest is online EWC (Schwarz et al. 2018).**
   - It has the geometric age decay, with γ in the role of q. It is the standard implementation in Mammoth and Avalanche.
   - Online EWC's F* = Σ γ^age F_k is H-REG's F̄ multiplied by (1 − q^n)/(1 − q), for n past tasks and γ = q.
   - That factor tends to 1/(1 − q) as n grows. So after about 1/(1 − q) tasks, H-REG's total strength differs from online
     EWC's only by a constant that a tuned λ absorbs.
   - The "fixed total independent of T" is therefore already an *asymptotic* property of every geometric-decay scheme:
     online EWC, and RLS with exponential forgetting (Lai & Bernstein eq. 38).
   - Normalisation changes only the transient over the first ~1/(1 − q) tasks, and the q → 1 limit.
3. **For "normalised to Σ = 1 and anchored at the Fisher-weighted mean", the closest objects are merges, not penalties.**
   - mode-IMM (Σα_k = 1, Fisher precisions) and Fisher merging (Σλ_i = 1).
   - Above all CoFiMA: eq. 6 is exactly Σ_tF_tθ_t / Σ_tF_t, and eq. 7 is a constant-λ recursion "giving higher importance
     to the latest tasks".
   - CoFiMA sets θ to that point after each task. H-REG instead *pulls toward* it during training, with strength F̄.
   - CoMA's λ = 1/t case, the uniform average, "might result in suboptimal performances" (Marouf et al.). That is a direct
     warning about H-REG's q → 1 limit, though in a merge setting on pretrained ViTs.
4. **For "bounded total so plasticity survives", the closest Bayesian object is MESU's truncated posterior.**
   - Its precision tends to about N·H, a fixed window, instead of growing like t·H.
   - Its paper names the failure of unbounded accumulation ("its plasticity collapses") and the cure (a finite N).
   - MESU bounds with a hard window, not geometric weights. Its anchor is a variational mean, not a Fisher-weighted mean of
     optima.

### 4.2 What, if anything, is not already in the literature

- **Found in no source read.** No source states the exact combination:
  - a training-time quadratic penalty,
  - per-task Fisher and per-task anchors (the Fisher-weighted-mean anchor),
  - geometric age weights normalised to Σπ_k = 1 at every T, including small T.
- **Each ingredient is published.**
  - The anchor: separate-penalty EWC, IMM, Fisher merging, CoFiMA.
  - The geometric decay: online EWC, RLS forgetting, Kalman drift.
  - The normalisation: EWC++ over iterations; IMM, Fisher merging and CoFiMA over models.
  - The bounded-strength motive: Schwarz, Chaudhry, MESU, MEAL, Kim.
- **What remains is small.** It is the small-T schedule of the normalisation, plus the pairing of a multi-anchor penalty
  with geometric normalised weights.
- **This is not a claim that the combination is novel.** The literature is large, and ~40 sources were read. A named
  domain expert would have to answer that (`CLAUDE.md` §7, SYNTHESIS / ADDS).
- **The CRR-proper part is the rule "strength equals one task's, never a count" (A6).** For a Laplace learner, that rule
  is a *deliberate departure from Bayes*:
  - with q → 1, H-REG gives the uniform average F̄ = mean F_k;
  - Bayes/Laplace gives n · mean F_k.
  - So H-REG(q → 1) is Laplace divided by n.
  - GVCL frames an overall multiplier on the Laplace term as cold-posterior tempering, and reports the tuned λ at 10–1000
    for online EWC, far *above* Bayes. H-REG at q → 1 moves *below* Bayes by 1/n.
  - Which direction the data favour is an empirical question. The sources agree that the tuned λ is not the Bayes λ.

### 4.3 A fair R7 baseline set for an H-REG prereg (inference)

Minimum, each with its reference implementation named and its commit recorded.

**Accumulation and decay baselines.**
1. **Laplace/EWC accumulation at the Bayes weight**, and at a **tuned λ**. These are the repository's existing arms
   (§4.3 of `Continuous_Learning/CONTINUOUS_LEARNING.md`; SEC for the calibrated Fisher).
2. **Online EWC (Schwarz 2018)**: Mammoth `ewc_on` at `e75a491c…`, with γ on the same grid as q and λ tuned per carrier.
   This is the baseline H-REG most likely reduces to.
3. **Separate-penalty EWC**: Avalanche `mode="separate"` at `eb075be3…`. It has the same multi-anchor as H-REG, is
   unnormalised, and weights every task equally.
4. **EWC++ (Chaudhry 2018)**: the moving-average Fisher, normalised, anchored at the last parameters.

**Two ablations that isolate H-REG's two choices** (both are required, or a win cannot be attributed):
5. **H-REG with the anchor moved to the last parameters.** This is online EWC with λ rescaled by (1 − q)/(1 − qⁿ). It
   isolates the anchor.
6. **H-REG with the normalisation removed.** This is separate-penalty EWC with q^age weights. It isolates the
   normalisation.

**Plasticity and merge baselines.**
7. **L2 Init (Kumar 2024)** and **Shrink and Perturb at boundaries (Ash & Adams 2020).** These are the strongest simple
   plasticity baselines. Both hold a fixed strength independent of T. If H-REG's argument is "bounded strength keeps
   plasticity", a fixed pull to θ₀ is the simplest thing that does that.
8. **CoFiMA / mode-IMM**: a Fisher-weighted merge to the same point θ̄, with the same normalised weights. This tests
   whether *pulling toward* θ̄ beats *jumping to* it.

**Reporting.**
- Report Chaudhry's intransigence I_k and forgetting per task index k, not only final accuracy (R6). The mechanism claim
  is about how I_k grows with k.
- **Stream length is the binding constraint.**
  - With one past task (a 2-task stream), H-REG, online EWC, EWC and Bayes-Laplace coincide up to λ.
  - The repository's EQ/SCL carriers have 2 or 3 tasks.
  - MEAL shows EWC and online EWC look alike at 10 tasks and diverge only by 100 tasks.
  - Dohare, Kumar and Elsayed need tens to thousands of switches to show plasticity loss.
  - A carrier rule that guarantees n ≫ 1/(1 − q) past tasks is needed. Otherwise the gate (R4) should find that H-REG
    cannot be told apart from online EWC, and it should close.

### 4.4 A prediction that separates H-REG from γ-decayed online EWC (inference)

Take both at the same q = γ, each with λ tuned on the same budget. The tuned λ absorbs every constant factor. Three
differences remain, and only these can separate the methods.

1. **The anchor** (from n = 2 past tasks on).
   - Online EWC pulls toward θ*_{T−1}. H-REG pulls toward θ̄, the Fisher-weighted mean of all past optima.
   - **Prediction:** on a stream whose task optima drift in a consistent direction (for example a rotating or
     drifting-feature stream), H-REG keeps the *oldest* tasks better and learns the *newest* task worse than online EWC.
   - It shows as a retention profile over task age: H-REG's is flatter. Online EWC's decays with age, so its oldest-task
     accuracy is lower.
   - On a stream whose optima scatter without a direction, the two anchors coincide on average and the difference should
     vanish.
   - This follows the MEAL App. I.1 observation (the cumulative multi-anchor penalty "pulls the shared trunk toward a
     compromise averaged over all past tasks") and the Kirkpatrick–Huszár exchange.
2. **The small-n schedule** (n below ~1/(1 − q)).
   - Online EWC's strength grows like (1 − qⁿ)/(1 − q) with n. H-REG's stays flat.
   - **Prediction:** with λ fixed across the stream, intransigence I_k rises with k over the first ~1/(1 − q) tasks under
     online EWC and stays flat under H-REG. Forgetting shows the mirror image.
   - A per-k analysis (R6) can score this. A final-accuracy median cannot.
3. **The q → 1 limit.**
   - Online EWC tends to Bayes-like counting: strength ∝ n, rising I_k, "over-regularizes" (MEAL), "plasticity collapses"
     (MESU on FOO-VB).
   - H-REG tends to the uniform average: flat I_k, but each old task's pull diluted as 1/n.
   - **Prediction:** at q near 1 on a long stream, H-REG has lower intransigence and higher forgetting of *each* old task
     than online EWC, and the forgetting of the oldest task grows with n.
   - This is the stability cost that A6's "never a count" buys, and it is the regime where the CoMA λ = 1/t warning
     applies.
   - If H-REG at q → 1 does *not* show that dilution, the normalisation is not doing what A6 says.

A surrogate gate (R4) follows from 4.4:
- **Must pass: a drifting-optimum learner.** Here the anchor matters: a convex quadratic learner whose task optima move
  along a line.
- **Must fail: a scattered-optimum learner and any 2-task stream.** There H-REG and online EWC must tie within one
  resolvable step.
- If the gate cannot be built so that both hold, H-REG reduces to online EWC with a λ schedule. The stop condition (R12)
  then applies.
