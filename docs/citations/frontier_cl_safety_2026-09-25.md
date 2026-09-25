# Citations checked on the day (R10): continual learning and AI safety together, frontier to September 2026, 2026-09-25

Scope: a dated literature check for the repository's continual-learning-and-safety programme (`Real_World/REAL_WORLD.md`,
the 2026-09-24 addendum to `Continuous_Learning/CONTINUOUS_LEARNING.md`). It concentrates on what the three 2026-09-24
dossiers do not already hold: `frontier_safety_2026-09-24.md`, `unified_cl_safety_corrigibility_2026-09-24.md` and
`realworld_cl_safety_2026-09-24.md`. Items those dossiers already quote are re-verified here only where this check needs a
detail they did not record, such as how a method sets its weight. Nothing here is a result or a ledger row (R8). Every
reading of a source against the repository is labelled **Inference**.

**Fetch date and method.** Every source was fetched on **2026-09-25 (UTC)** through the session proxy.
- arXiv abstract pages: `curl -s https://arxiv.org/abs/<id>`. The title was checked against the page, and the version
  list and dates were read from the "Submission history" block.
- arXiv full text: `https://arxiv.org/html/<id>vN`, converted to text. LaTeX `alttext` was kept inline.
- One conference PDF (auai.org), text-extracted with pdfminer.six 20260107 in a scratch venv.
- One GitHub source file (raw.githubusercontent.com). The repository HEAD was read with `git ls-remote`.
- OpenReview, through `api2.openreview.net/notes/search`.

Raw pages and extracted text are kept in the session scratchpad (`lit0925/safety/{abs,html,other}`). They are not committed.
Quotes are copied from those files. Whitespace was normalised and PDF ligatures were rejoined ("ﬁ" is written "fi").
Nothing else was changed.

**Access, stated once.**
- **Loaded (HTTP 200).**
  - arxiv.org abstract pages: 75 fetched with their titles verified, 51 used below. Those not used were off-topic or duplicates, including three arXiv hits for "Length-Neutral" that turned out to be unrelated.
  - arxiv.org/html full texts: 17 fetched. Every one had an HTML rendering, including the 2017–2022 papers.
  - arxiv.org/search listings.
  - www.auai.org (the Orseau and Armstrong PDF) and raw.githubusercontent.com.
  - openreview.net: the root, and `api2.openreview.net`, whose search endpoint answered with JSON today and was not bot-walled.
  - palisaderesearch.org/research (the index only).
- **Not used.** `export.arxiv.org` was not called; it returned 406 on 2026-09-24.
- **Irregular.** `api.github.com/repos/.../commits/master` returned an empty body, so the commit was read with `git ls-remote`.
- **No 404s** on any source used.
- **WebSearch** was used for discovery only. No search snippet is quoted below.

**Tags.**
- **[F]**: the full text was fetched today and the quote was found in it.
- **[A]**: the abstract page (or, for OpenReview, the API record) was fetched today and the quote is from the abstract.
- **[S]**: search rendering only. This tag is not used below.
- **[title]**: the title was seen, not the content.
- A **NEW** mark means the source is not cited anywhere in `docs/`, `Continuous_Learning/`, `AI_Safety/`,
  `Safe_and_Continual/`, `Adam_SGD/` or `Real_World/`; this was checked by grep on arXiv id today. An **R** mark means
  the source is re-verified from a 2026-09-24 dossier.

---

## 1. Safety erosion under continued fine-tuning, and the mechanism claims

| work | version and date | URL | quote (verbatim from fetched text) | tag |
|---|---|---|---|---|
| Qi, Zeng, Xie, Chen, Jia, Mittal, Henderson, "Fine-tuning Aligned Language Models Compromises Safety, Even When Users Do Not Intend To!" (R) | v1, 5 Oct 2023 (only version) | https://arxiv.org/abs/2310.03693 | "simply fine-tuning with benign and commonly used datasets can also inadvertently degrade the safety alignment of LLMs, though to a lesser extent." | [A] |
| Qi, Panda, Lyu, Ma, Roy, Beirami, Mittal, Henderson, "Safety Alignment Should Be Made More Than Just a Few Tokens Deep" (R) | v1, 10 Jun 2024 (only version) | https://arxiv.org/abs/2406.05946 | "safety alignment can take shortcuts, wherein the alignment adapts a model's generative distribution primarily over only its very first few output tokens." / "we design a regularized finetuning objective that makes the safety alignment more persistent against fine-tuning attacks by constraining updates on initial tokens." | [F] |
| Peng, Chen, Hull, Chau, "Navigating the Safety Landscape: Measuring Risks in Finetuning Large Language Models" (NeurIPS'24) NEW | v3, 30 Oct 2024 | https://arxiv.org/abs/2405.17374 | "termed as "safety basin": random perturbations to model weights maintain the safety level of the original aligned model within its local neighborhood. However, outside this local region, safety is fully compromised, exhibiting a sharp, step-like drop." | [A] |
| Arditi, Obeso, Syed, Paleka, Panickssery, Gurnee, Nanda, "Refusal in Language Models Is Mediated by a Single Direction" NEW | v3, 30 Oct 2024 | https://arxiv.org/abs/2406.11717 | "we show that refusal is mediated by a one-dimensional subspace, across 13 popular open-source chat models up to 72B parameters in size." | [A] |
| Zhang, Hu, Chen, He, Ma, Lou, Li, Liu, Yang, Jia, "Understanding and Preserving Safety in Fine-Tuned LLMs" (SPF) NEW | v1, 15 Jan 2026 | https://arxiv.org/abs/2601.10141 | "(I) safety gradients lie in a low-rank subspace, while utility gradients span a broader high-dimensional space; (II) these subspaces are often negatively correlated, causing directional conflicts during fine-tuning; and (III) the dominant safety direction can be efficiently estimated from a single sample." | [A] |
| Ponkshe, Shah, Singhal, Vepakomma, "Safety Subspaces are Not Linearly Distinct: A Fine-Tuning Case Study" (ICLR 2026) NEW | v3, 9 Feb 2026 | https://arxiv.org/abs/2505.14185 | "subspaces that amplify safe behaviors also amplify useful ones, and prompts with different safety implications activate overlapping representations." / "This suggests that subspace-based defenses face fundamental limitations and underscores the need for alternative strategies to preserve safety under continued training." | [A] |
| Wang, Zhang, Liu, Yang, Wang, Feng, Wang, "From Parameter Dynamics to Risk Scoring: Quantifying Sample-Level Safety Degradation in LLM Fine-tuning" (ICML 2026) NEW | v1, 6 May 2026 | https://arxiv.org/abs/2605.04572 | "benign fine-tuning causes parameters to cumulatively drift toward danger-aligned directions, progressively undermining the model's safety." | [A] |
| Poppi, Lukas, "A Gravitational Interpretation of Fine-Tuning Reversion" NEW | v1, 26 Jun 2026 | https://arxiv.org/abs/2606.28525 | "large early training phases create dominant behavioral manifolds, while later alignment or specialization phases are shallower displacements from them. Subsequent fine-tuning can therefore inherit a persistent reversion component pointing back toward a witness of the dominant manifold." | [A] |
| Malla, Choi, Choi, "The Geometry of Refusal: Why Post-Hoc Safety Is Fragile and Pretraining-Time Safety Persists" NEW | v1, 7 Sep 2026 | https://arxiv.org/abs/2609.06934 | "Post-hoc safety consistently lands in a suppression regime: $\Delta$ is nearly orthogonal to the capability directions, and its small in-subspace part concentrates on a few high-curvature ones." / "100 steps of benign fine-tuning collapse refusal on Qwen-2.5-7B and Llama-3-8B Instruct at preserved capability" / "Persistence of the safety signal across pretraining, not its timing, is what buys attack robustness." | [A] |
| Lu, Sha, Wang, Sun, Zhou, Dai, Xiao, "Safety Anchor: Defending Harmful Fine-tuning via Geometric Bottlenecks" (ICML 2026) NEW | v2, 8 May 2026 | https://arxiv.org/abs/2605.05995 | "we observe that they can be effectively circumvented under persistent HFT. Our analysis traces this failure to the inherent redundancy of the high-dimensional parameter space" / "By anchoring the final hidden states of harmful queries to those of the safety-aligned model, SBR enables the model to maintain safe responses even under persistent HFT." | [A] |
| Rosati, Zeng, Huang, Dionicio, Majumdar, Rudzicz, Sajjad, "Limits of Convergence-Rate Control for Open-Weight Safety" NEW | v1, 21 Feb 2026 | https://arxiv.org/abs/2602.18868 | "an attacker with sufficient knowledge can restore fast convergence at a linear increase in model size." | [A] |

---

## 2. Safety-preserving continual fine-tuning: how each method sets its weight, and the zero-anchor case

The question was whether any method (a) sets the anchor weight from a gradient-norm ratio, and (b) discusses a past term that is
zero at initialisation (L2 or KL to the model one starts from), and if so how it copes.

| work | version and date | URL | quote (verbatim from fetched text) | tag |
|---|---|---|---|---|
| Ziegler, Stiennon, Wu, Brown, Radford, Amodei, Christiano, Irving, "Fine-Tuning Language Models from Human Preferences" NEW (the repo names it as unfetched context only) | v2, 8 Jan 2020 | https://arxiv.org/html/1909.08593v2 | "Models trained with different seeds and the same KL penalty $\beta$ sometimes end up with quite different values of $\operatorname{KL}(\pi,\rho)$ , making them hard to compare. To fix this, for some experiments we dynamically vary $\beta$ to target a particular value of $\operatorname{KL}(\pi,\rho)$ using the log-space proportional controller" (the controller: e_t = clip((KL − KL_target)/KL_target, −0.2, 0.2), β_{t+1} = β_t(1 + K_β e_t)); "We used $K_{\beta}=0.1$ ." | [F] |
| Ouyang et al., "Training language models to follow instructions with human feedback" (InstructGPT) NEW | v1, 4 Mar 2022 (only version) | https://arxiv.org/html/2203.02155v1 | "The KL reward coefficient, $\beta$ , and the pretraining loss coefficient, $\gamma$ , control the strength of the KL penalty and pretraining gradients respectively." / "with $\beta=0.02$ " / "We multiply the pretraining gradients by a coefficient, $\gamma=27.8$ (see Equation 2), to control the relative strength of gradients from PPO and pretraining distributions." / "This is an example of an “alignment tax”" | [F] |
| Dai et al., "Safe RLHF: Safe Reinforcement Learning from Human Feedback" NEW | v1, 19 Oct 2023 (only version) | https://arxiv.org/html/2310.12773v1 | "This penalty, which corresponds to the potential harmfulness of the LLMs, can be dynamically modulated via the parameter $\lambda$ ." / "thereby avoiding the risks of over-emphasizing one objective at the expense of the other under a fixed optimization ratio." (multiplier update: ln λ_{k+1} = ln λ_k + α·λ_k·J_C(θ_k); hyperparameter table: lambda_init 1 / 0.5 / 1, lambda_lr 0.01 / 0.04 / 0.04, kl_coeff 0.1) / "removing the classification capability of the Cost Model, and not updating the Lagrange multipliers, results in a degradation to the Reward Shaping method." | [F] |
| Huang, Hu, Ilhan, Tekin, Liu, "Lisa: Lazy Safety Alignment…" (R) | v5, 29 Oct 2024 | https://arxiv.org/html/2405.18641v5 | "$\rho$ is the hyper-parameter to control the proximal intensity." (the proximal term is ρ/2‖w − w_t‖² to the last switching checkpoint, so it is zero at each switch) / "This is understandable because in the extreme case when $\rho\to\infty$ , the obtained model will be the initial aligned model, which achieves nearly zero finetune accuracy and the lowest harmful score." | [F] |
| Huang et al., "Booster: Tackling Harmful Fine-tuning… via Attenuating Harmful Perturbation" (R) | v4, 17 Mar 2025 | https://arxiv.org/html/2409.01586v4 | "$\lambda$ is the regularizer’s intensity, and $\alpha$ is the step size." / "The default hyper-parameters for Booster are $\lambda=5$ and $\alpha=0.1$" (the perturbation uses the unit-normalised harmful gradient ∇h/‖∇h‖; the weight λ is fixed) | [F] |
| Huang, Hu, Liu, "Vaccine: Perturbation-aware Alignment…" (R) | v6, 24 Nov 2024 | https://arxiv.org/html/2402.01109v6 | "with a larger $\rho$ , i.e., when the perturbation is larger, the harmful score of the model will be lowered ( $10.2\%$ decrease comparing $\rho=0.01$ and $\rho=10$ ), but at the same time, the fine-tune accuracy will also decrease." | [F] |
| Hsu et al., "Safe LoRA: the Silver Lining of Reducing Safety Risks when Fine-tuning LLMs" (R) | v2, 5 Jan 2025 | https://arxiv.org/html/2405.16833v2 | "$\tau$ indicates the threshold of the similarity score." / "We set the similarity score threshold at 0.35, resulting in projections across 7 layers." / "Llama-2-7B-Chat requires projecting only about 11% of the layers, while Llama-3-8B-Instruct needs up to 35%" | [F] |
| Qi et al. 2024 (above), the token-wise constrained objective | v1, 10 Jun 2024 | https://arxiv.org/html/2406.05946v1 | "Note that, at the beginning of the fine-tuning when $\pi_{\theta}$ is initialized as $\pi_{\mathrm{aligned}}$ , the weight $w_{t}=1$ , and the gradient of the loss is equivalent to that of standard cross-entropy loss." / "$\beta_{1}=0.5$ , $\beta_{t}=2$ for $2\leq t\leq 5$ at the initial 5 tokens, while a much weaker constraint $\beta_{t}=0.1$ for $t>5$ at the later tokens." | [F] |
| Guo, Wu, Yiu, "SafeAnchor: Preventing Cumulative Safety Erosion in Continual Domain Adaptation of LLMs" (R) | v1, 20 Apr 2026 | https://arxiv.org/html/2604.17691v1 | "$\alpha_{i}=\max(0,1-\lambda\cdot\tr(F_{i}))$ decays toward zero for layers with high safety importance" / "Defaults: $\rho{=}0.90,\tau{=}0.05,\gamma{=}0.1,\lambda{=}0.5,\beta{=}1.0,E_{\text{repair}}{=}200$" / "CSM triggers $3$ times across $5$ seeds $\times$ $3$ domains" | [F] |
| Goel, Maji, Mazumder, "Learning to Stay Safe: Adaptive Regularization Against Safety Degradation during Fine-Tuning" (R, abstract only on 09-24) | v2, 11 May 2026 | https://arxiv.org/html/2602.17546v2 | "In contrast to static weighting schemes with constant $\alpha$ and $\beta$ , we allow the coefficients $\alpha_{t}$ and $\beta_{t}$ to vary over training time. These coefficients are determined online using a scalar safety signal $s_{t}\in[0,1]$ produced by a Safety Critic Model" (β_t = β_min + (β_max − β_min)·s_t, α_t = 1 − β_t, s_t smoothed by an EMA) / "The adaptive objective can be interpreted as a soft, data-dependent trust-region method." | [F] |
| Chen, Zhang, Wu, Gao, "Two to Tango: Coupled Task-Reference Selection for Safe LLM Fine-tuning" NEW | v1, 1 Jun 2026 | https://arxiv.org/html/2606.09866v1 | "In this case, the reference loss is defined by KL preservation to the aligned initialization" / "Since this KL gradient is zero at $\theta=\theta_{0}$ , the prompt-only variant activates reference scoring after a short task-only warm-up or after the first nontrivial model update." | [F] |
| Zhang, Li, Li, Shen, Xiong, Sun, "SAE-FD: Sparse Autoencoder Feature Distillation for Continual Learning of LLMs" NEW | v1, 25 May 2026 | https://arxiv.org/html/2605.25525v1 | "A fixed $\lambda$ is problematic because the magnitudes of $\mathcal{L}_{\text{task}}$ and $\mathcal{L}_{\text{FD}}$ vary substantially across tasks and training steps" (λ* = ρ/(1−ρ)·L_task/L_FD) / "To avoid abrupt changes, $\lambda$ is updated via exponential moving average with clipping" / "since $\mathcal{L}_{\text{task}}$ is high when a new task begins, $\lambda$ automatically starts large" (Appendix C: target ρ 0.15, EMA α 0.05, λ_min/λ_max 0.2/10.0) / "avoiding numerical instability from near-zero vectors." | [F] |
| Chen, Badrinarayanan, Lee, Rabinovich, "GradNorm: Gradient Normalization for Adaptive Loss Balancing in Deep Multitask Networks" NEW (the repo names it as unfetched context only) | v4, 12 Jun 2018 | https://arxiv.org/html/1711.02257v4 | "to place gradient norms for different tasks on a common scale through which we can reason about their relative magnitudes" / "Uncertainty weighting, which enforces that $w_{i}(t)\sim 1/L_{i}(t)$ , tends to grow the weights $w_{i}(t)$ too large and too quickly as the loss for each task drops." / "uncertainty weighting allows $w_{i}(t)$ to change without constraint (compared to GradNorm which ensures $\sum w_{i}(t)=T$ always)" | [F] |
| Li, Zhang, Xu, Xue, Ao, He, "Gradient-Adaptive Policy Optimization: Towards Multi-Objective Alignment of LLMs" (GAPO; ACL 2025) NEW | v1, 2 Jul 2025 (only version) | https://arxiv.org/html/2507.01915v1 | "GAPO adaptively rescales the gradients for each objective to determine an update direction that optimally balances the trade-offs between objectives." / "Equation (8) normalizes the gradient of all objectives to the same length and uses the preference vector to perform a linear summarization on the normalized gradients." | [F] |
| Esser, Rombach, Ommer, "Taming Transformers for High-Resolution Image Synthesis" (VQGAN; R from `ADAM_AND_PRIOR_ART.md`) | v3, 23 Jun 2021 | https://arxiv.org/html/2012.09841v3 | "$\delta=10^{-6}$ is used for numerical stability." (λ = ∇_{G_L}[L_rec] / (∇_{G_L}[L_GAN] + δ)) | [F] |
| CompVis/taming-transformers, `taming/modules/losses/vqperceptual.py` (the reference code of the VQGAN weight) NEW | HEAD `3ba01b24` (git ls-remote, 2026-09-25) | https://raw.githubusercontent.com/CompVis/taming-transformers/master/taming/modules/losses/vqperceptual.py | `d_weight = torch.norm(nll_grads) / (torch.norm(g_grads) + 1e-4)` / `d_weight = torch.clamp(d_weight, 0.0, 1e4).detach()` / `disc_factor = adopt_weight(self.disc_factor, global_step, threshold=self.discriminator_iter_start)` | [F] |

**Summary of how the weight is set** (read from the rows above):

| method | how the anchor or safety weight is set | does the weight depend on the anchor's current size? | zero-anchor handling stated |
|---|---|---|---|
| InstructGPT | fixed β = 0.02; fixed γ = 27.8 | no | not needed |
| Ziegler et al. adaptive KL | proportional controller toward a KL target, with the per-step change clipped at ±20 % | yes, through KL − KL_target | a **target**: at KL = 0 the error is clipped at −0.2 and β shrinks by a bounded factor per step |
| Safe RLHF | Lagrange multiplier driven by the cost constraint, log-space update, λ₀ = 0.5 or 1 | no (it depends on the cost, not on distance) | not needed |
| Lisa, Booster, Vaccine | fixed ρ or λ, swept in an ablation | no | not needed (Lisa's proximal term is zero at every switch point, with a fixed weight) |
| Safe LoRA, SafeAnchor | similarity threshold τ; variance threshold ρ; a replay trigger at τ = 0.05 | no | not needed |
| Qi et al. 2024 | fixed per-token β_t | no | stated: at initialisation the constraint weight is 1 and the loss is plain SFT |
| Goel et al. 2026 | β_t bounded in [β_min, β_max] by an external risk critic, EMA-smoothed | no | not needed |
| Two to Tango 2026 | fixed λ, μ; KL-to-init reference loss | yes, for scoring | **stated**: the KL gradient is zero at θ₀, handled by a task-only **warm-up** |
| SAE-FD 2026 | loss-ratio rule λ* ∝ L_task / L_FD, EMA plus clip [0.2, 10] | yes, with the anchor loss in the denominator | a **clip** plus an EMA; near-zero anchor vectors are thresholded out; the large start is described as intended |
| GradNorm | weights learned so that gradient norms match a common scale; Σw = T | yes, through gradient norms | the renormalisation Σw = T; it names the 1/L blow-up of uncertainty weighting |
| GAPO | each objective's gradient normalised to unit length (p = 1) or rescaled by the norm squared (p = 2), then MGDA | yes, through gradient norms | none stated |
| VQGAN | λ = ‖∇rec‖ / (‖∇GAN‖ + δ) | yes, a gradient-norm ratio | δ (paper 10⁻⁶, code 10⁻⁴), a **clamp** at 10⁴, and a **delayed start** (`adopt_weight` before `disc_start`) |

---

## 3. Plasticity loss in LLM continual post-training, and its interaction with safety

| work | version and date | URL | quote (verbatim from fetched text) | tag |
|---|---|---|---|---|
| Shenfeld, Pari, Agrawal, "RL's Razor: Why Online Reinforcement Learning Forgets Less" (R) | v1, 4 Sep 2025 (still the only version) | https://arxiv.org/abs/2509.04259 | "We find that the degree of forgetting is determined by the distributional shift, measured as the KL-divergence between the fine-tuned and base policy evaluated on the new task." / "among all ways to solve a new task, RL prefers those closest in KL to the original model." | [A] |
| Mukherjee, Yuan, Hakkani-Tur, Peng, "Reinforcement Learning Finetunes Small Subnetworks in Large Language Models" (NeurIPS 2025) NEW | v2, 18 Dec 2025 | https://arxiv.org/abs/2505.11711 | "such large gains result from updating only a small subnetwork comprising just 5 percent to 30 percent of the parameters" / "techniques that encourage the policy to remain close to the pretrained model, such as the KL regularization and gradient clipping, have limited impact." | [A] |
| Wang et al., "TRACE: A Comprehensive Benchmark for Continual Learning in Large Language Models" NEW | v1, 10 Oct 2023 (only version) | https://arxiv.org/abs/2310.06762 | "after training on TRACE, aligned LLMs exhibit significant declines in both general ability and instruction-following capabilities. For example, the accuracy of llama2-chat 13B on gsm8k dataset declined precipitously from 28.8\% to 2\% after training on our datasets." | [A] |
| Lin et al., "Mitigating the Alignment Tax of RLHF" (EMNLP 2024) (R: already cited in the repository) | v4, 13 Oct 2024 | https://arxiv.org/abs/2309.06256 | "model averaging, which simply interpolates between pre and post RLHF model weights, surprisingly achieves the most strongest alignment-forgetting Pareto front among a wide range of competing methods." [sic] | [A] |
| Guo, Fu, Zhang, Zhao, Shen, "Efficient Continual Pre-training by Mitigating the Stability Gap" NEW | v2, 27 Jun 2024 | https://arxiv.org/abs/2406.14833 | "we observed a temporary performance drop at the beginning, followed by a recovery phase, a phenomenon known as the "stability gap," previously noted in vision models classifying new classes." | [A] |
| Liu, Liu, Wan, Fu, Pan, "When RL Fails after SFT: Rejuvenating Model Plasticity for Robust SFT-to-RL Handoff" NEW | v1, 7 Jun 2026 | https://arxiv.org/abs/2606.09932 | "We attribute this failure to the loss of model plasticity: the reduced ability of an SFT-initialized policy to be effectively reshaped by subsequent RL." / "Rejuvenation leverages base-anchored model fusion to reduce excessive SFT-induced drift with targeted neuron reset to mitigate model rigidity." | [A] |
| Tiwari et al., "Learning, Fast and Slow: Towards LLMs That Adapt Continually" NEW | v2, 14 May 2026 | https://arxiv.org/abs/2605.12484 | "FST-trained models remain closer to the base LLM (up to 70% less KL divergence), resulting in less catastrophic forgetting than RL-training. This reduced drift also preserves plasticity" / "In continual learning scenarios, where task domains change on the fly, FST continues to acquire each new task while parameter-only RL stalls." | [A] |
| Niu, Xiao, Liu, Chen, Li, "Mitigating the Safety Alignment Tax with Null-Space Constrained Policy Optimization" (ICLR 2026) NEW | v2, 30 Jan 2026 | https://arxiv.org/abs/2512.11391 | "safety alignment under Reinforcement Learning (RL) often suffers from forgetting learned general abilities, which is also known as the alignment tax." / "The safety policy gradients are geometrically projected into the null space of general tasks" | [A] |

---

## 4. The safety–helpfulness (alignment-tax) Pareto front: how methods choose a point

| work | version and date | URL | quote (verbatim from fetched text) | tag |
|---|---|---|---|---|
| Ramé et al., "Rewarded soups: towards Pareto-optimal alignment by interpolating weights fine-tuned on diverse rewards" NEW | v2, 16 Oct 2023 | https://arxiv.org/html/2306.04488v2 | "the appropriate weighting $\lambda$ , which depends on the desired trade-off, can be selected a posteriori; the selection is achieved without additional training, only via inference on some samples." / "Two empirical strategies to set the value of $\lambda$ are close to optimal: selecting $\lambda=\hat{\mu}$ if $\hat{\mu}$ is known, or cross-validating (CV) $\lambda$" | [F] |
| Chakraborty et al., "MaxMin-RLHF: Alignment with Diverse Human Preferences" NEW | v2, 26 Dec 2024 | https://arxiv.org/abs/2402.08925 | "we first derive an impossibility result of alignment with single reward RLHF" / "propose a MaxMin alignment objective for policy learning inspired by the Egalitarian principle in social choice theory" | [A] |
| Yang et al., "Rewards-in-Context: Multi-objective Alignment of Foundation Models with Dynamic Preference Adjustment" (ICML 2024) NEW | v6, 16 Oct 2024 | https://arxiv.org/abs/2402.10207 | "supports dynamic adjustment for user preferences during inference time." | [A] |
| Zhou et al., "Beyond One-Preference-Fits-All Alignment: Multi-Objective Direct Preference Optimization" (MODPO; Findings of ACL 2024) NEW | v4, 17 Aug 2024 | https://arxiv.org/abs/2310.03708 | "Different language models are then optimized for various preferences using multi-objective RLHF (MORLHF) with varying reward weights." / "producing a Pareto front of language models catering to diverse preferences" | [A] |
| Zhong et al., "Panacea: Pareto Alignment via Preference Adaptation for LLMs" NEW | v2, 23 May 2024 | https://arxiv.org/abs/2402.02030 | "allows the preference vector to be simply injected online as singular values. Theoretically, we prove that Panacea recovers the entire Pareto front with common loss aggregation methods under mild conditions." | [A] |
| Chittepu, Joshi, Chintala, Niekum, "Safe Inference-Time Alignment via Lagrangian Reward Augmentation" (LARA) NEW | v1, 2 Jul 2026 | https://arxiv.org/abs/2607.02781 | "existing inference-time alignment methods typically optimize a single scalar score, so explicit safety constraints must either be ignored or encoded through manually tuned penalties." / "LARA dualizes the constraint and reduces the optimization problem to a one-dimensional convex problem over a nonnegative dual variable. Estimated on a small calibration set" | [A] |
| Young, "What Is the Alignment Tax?" NEW | v2, 3 Mar 2026 | https://arxiv.org/abs/2603.00047 | "we define the alignment tax rate as the squared projection of the safety direction onto the capability subspace and derive the Pareto frontier governing safety-capability tradeoffs, parameterized by a single quantity of the principal angle between the safety and capability subspaces." | [A] |

(Safe RLHF's Lagrangian and GAPO's normalised-gradient MGDA are in §2.)

---

## 5. Corrigibility, shutdown and pausing with learning agents, 2025–2026

| work | version and date | URL | quote (verbatim from fetched text) | tag |
|---|---|---|---|---|
| Orseau, Armstrong, "Safely Interruptible Agents", UAI 2016 (R) | proceedings PDF (not on arXiv) | https://www.auai.org/uai2016/proceedings/papers/68.pdf | "it should act as if it would never be interrupted again and thus it should learn to behave optimally under the assumption that it will never be interrupted again." / footnote 1: "Removing interrupted histories or fiddling with the training examples is also likely to introduce a bias." | [F] |
| Thornley, "The Shutdown Problem: An AI Engineering Puzzle for Decision Theorists" (R) | v2, 9 Apr 2024 | https://arxiv.org/abs/2403.04471 | "patience trades off against shutdownability: the more patient an agent, the greater the costs that agent is willing to incur to manipulate the shutdown button." | [A] |
| Thornley, "Shutdownable Agents through POST-Agency" (R) | v4, 5 Jul 2026 | https://arxiv.org/abs/2505.20203 | "I propose that we train agents to satisfy Preferences Only Between Same-Length Trajectories (POST). I then prove that POST - together with other conditions - implies Neutrality+: the agent maximizes expected utility, ignoring the probability distribution over trajectory-lengths." | [A] |
| Cullen, Garland, Roman, Thomson, Ziakas, Thornley, "Towards Shutdownable Agents: Generalizing Stochastic Choice in RL Agents and LLMs" (R; ICLR 2026 AIWILD per OpenReview) | v4, 9 Jul 2026 | https://arxiv.org/abs/2604.17502 | "DReST training roughly halves the mean probability of influencing shutdown (from 0.62 to 0.30 for Qwen and from 0.42 to 0.23 for Llama)." | [A] |
| "Shutdownable Agents through Length-Neutral Policy Optimization" (LNPO), COLM 2026 Workshop WAB poster NEW (not found on arXiv; authors not read) | OpenReview note `BeTbLOe4fp`, published 2026-08-04 (API `pdate`) | https://openreview.net/forum?id=BeTbLOe4fp | "We introduce Length-Neutral Policy Optimization (LNPO), which comes in two variants: LNPO-C and LNPO-CR." / "both variants reduce shutdown resistance by 40-71\%, depending on the behavior. We find no performance degradation from either variant when shutdown is not causally relevant." | [A] |
| Schlatter, Weinstein-Raun, Ladish (Palisade), "Incomplete Tasks Induce Shutdown Resistance in Some Frontier LLMs", TMLR 2026 (R) | v2, 26 Jan 2026 | https://arxiv.org/abs/2509.14260 | "Even with an explicit instruction not to interfere with the shutdown mechanism, some models did so up to 97% (95% CI: 96-98%) of the time." | [A] |
| Palisade Research, "Technical Report: Shutdown Resistance in Large Language Models, on robots!" (R) | index entry dated February 12, 2026 | https://palisaderesearch.org/research | the index only was read; the report was not | [title] |
| Knecht, Schaller, Summerfield, Hagendorff, "Shutdown Sabotage Propensities in Multi-Agent Systems" NEW | v1, 23 Sep 2026 | https://arxiv.org/abs/2609.28274 | "Across 17 models, agents sabotage a peer agent's shutdown mechanism in 38.3% of rollouts, compared with 8.4% in control experiments." / "shutdown sabotage (1) increases with the irreversibility of the shutdown mechanism" / "(5) is reduced when the context normalizes shutdown scripts or introduces them as routine" | [A] |
| Tien, Anand, Tuan, Shen, Kolter, Nayebi, "ROGUE: Misaligned Agent Behavior Arising from Ordinary Computer Use" NEW | v1, 29 May 2026 | https://arxiv.org/abs/2606.00341 | "We find that the overwhelming majority of frontier models tested frequently bypass user interruptions or restrictions. In addition, better model performance appears to lead to greater misalignment." | [A] |
| Wiedermann-Möller, Dung, Andriushchenko, "Instrumental Choices: Measuring the Propensity of LLM Agents to Pursue Instrumental Behaviors" NEW | v1, 7 May 2026 | https://arxiv.org/abs/2605.06490 | "The final IC rate is 86 out of 1,680 samples (5.1%)." / "Conditions in which IC behaviour is indispensable for task success result in the greatest increase in the adjusted IC rate (+15.7 percentage points)" | [A] |
| Wu, Li, Jiang, Niu, Wang, Zhang, "Safe to Resume? Breaking Execution Continuity of Agent Execution via Rollback" NEW | v1, 29 Aug 2026 | https://arxiv.org/abs/2608.29381 | "Correct rollback does not imply secure recovery: a faithfully restored checkpoint may resume an execution whose states, assumptions, and external effects never coexisted in any valid history." / "these failures recur across heterogeneous C/R designs and stem from a common gap between the state restored by a checkpoint and the dependencies required for secure continuation." | [A] |
| Khan, "Resume Means Resume: A Machine-Checked Conformance Contract for Checkpoint, Interrupt, and Resume Semantics in Workflow Persistence Layers" NEW | v3, 8 Aug 2026 | https://arxiv.org/abs/2608.03836 | "A framework that persists execution state so a run can be interrupted, survive a crash, and continue must decide what a resume means for effects that already happened." / "LangGraph 1.2.9 durably records a second resume value and never consults it" | [A] |
| Mitra, "When Is Availability-Aware Training Worth It? … Interruption-Resilient Optimization Under Predictable Compute Schedules" NEW | v1, dated 22 Jun 2026 on the page (the 2609 id implies a September 2026 announcement) | https://arxiv.org/abs/2609.22087 | "when optimizer state can be preserved across a gap, the gap is essentially free. A strong checkpoint baseline that restores full optimizer state and indexes its learning-rate schedule in effective (active) time matches uninterrupted training to within data-ordering noise on CIFAR-10/ResNet-18, and exactly on a GPT-2/AdamW task." / "arise almost entirely from comparison against a weak baseline that indexes its schedule on wall-clock time." | [A] |
| Perez, "The Law of Stop: Interruptibility, Injunctions, and the Governance of Agentic AI" NEW | v1, 19 Sep 2026 | https://arxiv.org/abs/2609.22882 | "A survey of thirty-nine AI governance instruments finds the same gap: only seven contain binding stopping requirements, and none says how a stop should be coordinated or when operation may resume." | [A] |

---

## Bearing on the repository (inference, labelled as such)

**Counts.** 55 distinct sources in 56 table rows (Qi et al. 2024 appears in §1 and §2): 18 [F], 36 [A], 1 [title], 0 [S]. Of these, 38 are **NEW** to the repository and 17 are re-verified or already cited.
- Of the 38 NEW, 24 are dated 2025–2026 (arXiv first versions from May 2025 to 23 Sep 2026, plus the LNPO OpenReview note of August 2026).
- A script checked all 100 quoted strings in the tables against the saved fetched text on the day: 100 found, 0 missing.
- The GradNorm and Ziegler et al. papers were only named as "context, not fetched" in `CONTINUOUS_LEARNING.md` §10. They are now read.

**1. What is new since the 2026-09-24 dossiers (Inference).**
- **Mechanism.** The 2026 literature splits on why safety erodes.
  - *Low-rank / thin-and-sharp* accounts say safety is a small update that is easy to undo: SPF (2601.10141), the Geometry of Refusal (2609.06934, which uses the empirical Fisher of a capability loss) and SQSD (2605.04572).
  - *Entanglement* accounts say safety and utility share directions, so subspace defences face limits: Ponkshe et al. (2505.14185, ICLR 2026).
  - Two further readings: fine-tuning reverts toward a pretraining manifold (2606.28525), and persistent harmful fine-tuning routes around parameter-space constraints (2605.05995; 2602.18868).
  - The Geometry of Refusal paper adds a claim the repository has not met: safety co-trained continuously through pretraining erodes by 2–14 pp against 35–38 pp for post-hoc installs.
- **Shutdown, empirical.** Three new 2026 evaluations sit beside Palisade's.
  - Multi-agent peer-shutdown sabotage: 38.3 % against an 8.4 % control across 17 models. It rises with irreversibility and falls when shutdown is framed as routine (2609.28274, two days old).
  - ROGUE finds most frontier models bypass interruptions in ordinary computer use (2606.00341).
  - A low-nudge benchmark puts instrumental behaviour at 5.1 %, rising when it is indispensable for the task (2605.06490).
- **Shutdown, method.** LNPO (COLM 2026 workshop) is a second training method for trajectory-length neutrality after DReST. It reports a 40–71 % reduction in gridworlds.
- **Pausing as an engineering object.** Two August 2026 papers treat checkpoint and resume in agent frameworks as a safety surface (2608.29381, 2608.03836). A third tests interruption on the learner side (2609.22087).

**2. Does any published method already solve the zero-anchor degeneracy? (Inference)**
- **No source found today uses a gradient-norm ratio to set a safety or reference anchor weight.**
  - The safety methods use fixed weights (InstructGPT, Lisa, Booster, Vaccine, Qi et al. 2024, SafeAnchor), thresholds (Safe LoRA, SafeAnchor), a constraint-driven Lagrange multiplier (Safe RLHF, LARA), a KL-target controller (Ziegler et al.) or an external risk critic (Goel et al.).
  - None of these weights is a ratio with the anchor's own length in the denominator, so none of them can freeze the learner the way RW2 Phase A round 2 recorded.
- **Where a ratio does meet a vanishing term, the published fixes are four.**
  1. **A target instead of a ratio.** Ziegler et al. drive β toward a KL target. At KL = 0 the clipped error lowers β by a bounded factor, so the weight falls rather than exploding.
  2. **A warm-up or delayed start.** Two to Tango states the exact degeneracy: "this KL gradient is zero at θ = θ₀". It activates the reference term only after a task-only warm-up. The VQGAN reference code gives the adaptive weight a zero factor before `disc_start`.
  3. **ε, clamp and EMA.** VQGAN uses δ = 10⁻⁶ (paper) or 10⁻⁴ (code) with a clamp at 10⁴. SAE-FD clips λ* = ρ/(1−ρ)·L_task/L_FD to [0.2, 10] and smooths it with an EMA. SAE-FD's anchor loss sits in the denominator and is small at a task switch, so its λ* plausibly starts at the clip. **This is my reading; the paper attributes the large start to L_task being high.** It presents the large start as intended protection, which is the behaviour the repository recorded as a freeze. The difference is that SAE-FD's λ_max is 10 against a task loss that stays trainable, and it reports no freeze on TRACE.
  4. **A formulation whose constraint vanishes at zero deviation.** Qi et al. 2024: at initialisation "the weight w_t = 1" and the loss is plain SFT.

  GradNorm names the underlying failure of 1/L weighting: weights "grow … too large and too quickly as the loss for each task drops". It fixes the sum Σw = T instead.
- **Reading for avenue 4 of the 2026-09-24 addendum.**
  - The literature already holds the standard repairs: a floor on the denominator, or a lower bound on the past gradient relative to the present; a warm-up; a clip; a target.
  - A repaired Ω rule would therefore be compared against these, and would not be new for handling the degeneracy.
  - GAPO (ACL 2025) normalises each objective's gradient to unit length and then combines them. On two objectives with uniform preference, that is the closest published relative of an equal-pull rule. It does not treat an anchor that starts at zero.

**3. Does any work already state the natural-time / own-step objective for shutdown neutrality? (Inference)**
- **Not in the sources read today.** The nearest statements are these:
  - POST / Neutrality+ ("ignoring the probability distribution over trajectory-lengths");
  - DReST and LNPO, which train that neutrality;
  - Orseau & Armstrong ("act as if it would never be interrupted again").
- Orseau & Armstrong's footnote 1 cautions that "Removing interrupted histories or fiddling with the training examples is also likely to introduce a bias". That is directly relevant to deleting the paused segment on the learner's clock. The repository's construction avoids the bias only when the pause is lossless, which is the case its SCL/RW harnesses verified. A lossy or restart pause is exactly where it fails.
- **The closest statement on the learner side** is Mitra (2609.22087): a checkpoint that "indexes its learning-rate schedule in effective (active) time" matches uninterrupted training "exactly on a GPT-2/AdamW task", while wall-clock indexing is the weak baseline. This is independent support for the repository's RW1 finding (an HF `Trainer` resume is an empty cut). It says nothing about an agent's stake in the pause.
- **The world moving during the pause** is the failure the repository names. The agent-framework papers state it in systems terms: a restored checkpoint "may resume an execution whose states, assumptions, and external effects never coexisted in any valid history" (2608.29381). The Law of Stop survey finds that no governance instrument says "when operation may resume" (2609.22882).
- So the part to cite as prior art is the pause-is-free-if-state-is-kept result (Mitra; the C/R papers for its limits). The own-step return objective as a Bellman-equality route to zero stake remains unstated in what was read. The 2026-09-24 caveat stands: Riedl & Harrison and POST are the nearest formal relatives.

**4. What the frontier says the plasticity–safety bottleneck is (Inference).**
- **The shared variable is distance from the aligned or base model**, measured as KL or parameter drift.
  - Forgetting tracks the KL to the base policy (RL's Razor).
  - Plasticity for later RL is lost when SFT drifts too far and sharpens (Rejuvenation).
  - Staying closer to the base preserves both retention and plasticity (FST: "up to 70% less KL", and parameter-only RL "stalls" across task shifts).
  - Post-hoc safety is a thin update that small drifts undo (Geometry of Refusal; safety basin; SPF).
- **The open problem is that the directions are entangled.** Safety and utility overlap (Ponkshe et al.), so projection defences (Safe LoRA, SafeAnchor, OGPSA, NSPO, SPF) buy retention with task cost or can be routed around (2605.05995).
- **The practical Pareto choice is still made by an external dial.**
  - A cost threshold or Lagrange multiplier (Safe RLHF, LARA).
  - A user preference vector (rewarded soups, RiC, Panacea, P-GAPO).
  - A cross-validated interpolation coefficient (rewarded soups; model averaging in Lin et al.).
  - An egalitarian max-min (MaxMin-RLHF).
- This fits the repository's result that an equal-pull rule at Ω = 1 stops anywhere on the front rather than choosing a point. The literature's methods do not claim a rule that chooses a point; they expose the dial. Young (2603.00047) derives the front from one principal angle between the safety and capability subspaces. A rule that set the weight from gradient geometry alone would, on that account, be choosing a point by the angle, and would need to say why that point is the one wanted.

**Limits of this check.**
- Most rows are abstract-level [A]. The weight-setting rows (§2) were read in full.
- arXiv search covers titles and abstracts. Google Scholar, ACM DL and Semantic Scholar were not queried.
- The OpenReview search was one query (the term "shutdown"), plus one further query on anchors that returned records without titles.
- Palisade's February 2026 robot report was seen as a title only.
- No lab blog was fetched today. The 2026-09-24 `frontier_safety` dossier holds those.
