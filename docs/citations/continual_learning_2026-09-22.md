# Citations checked on the day — continual learning and catastrophic forgetting, 2026 (R10), 2026-09-22

Owner request (prompt-log entry 73): reference 2026 papers and cross-verify the Ω = 1 rule against existing
catastrophic-forgetting solutions. The cross-verification is `Continuous_Learning/CROSS_VERIFICATION.md`; the
computational battery is `theory/checks/omega_vs_methods.py` (pinned output beside it); this file is the
literature record.

**Access, stated once.** The execution environment's egress proxy blocked every full-text and abstract-page host
tried on the day: arxiv.org (abs, pdf, html, export), openaccess.thecvf.com, proceedings.iclr.cc,
huggingface.co, alphaxiv.org, pith.science, api.openalex.org, api.semanticscholar.org, api.crossref.org,
europepmc.org, openreview.net. No link returned a 404. Items marked **[S]** are search-engine renderings of an
arXiv or venue abstract and are **unverified against the source**; author lists and version numbers are given
only where the rendering displayed them. Items marked **[PubMed]** were located through the PubMed connector:
title, authors, journal, year and DOI are as PubMed records them, and the abstract was read there. Nothing here
is a result.

## A. Regularisation-based methods (the family the rule applies to)

| paper | record | what the rendering says |
|---|---|---|
| Liu et al. *Elastic Weight Consolidation Done Right for Continual Learning.* arXiv:2603.18596 (March 2026); CVPR 2026 | [S] | EWC's reliance on the Fisher information "results in gradient vanishing and inaccurate importance estimation in certain scenarios"; MAS imposes "redundant protection"; proposes Logits Reversal (LR) for importance estimation; EWC-DR "consistently outperforms EWC and its variants". |
| Yao et al. (as displayed: github yaoyz96/low-rank-cl). *Revisiting Weight Regularization for Low-Rank Continual Learning.* arXiv:2602.17559; ICLR 2026 | [S] | EWC-LoRA regularises "a shared low-rank update through EWC", estimating importance over the full-dimensional space from the low-rank representation; "a stability-plasticity trade-off superior to existing low-rank CL approaches". |
| Sliwa J, Schneider F, Hennig P, Hernández-Lobato JM. *Mitigating Forgetting in Low Rank Adaptation.* arXiv:2512.17720 (19 Dec 2025); OpenReview | [S] | LaLoRA: "applies a Laplace approximation to Low-Rank Adaptation ... constrains updates in high-curvature directions"; Llama fine-tuning for mathematical reasoning; "improved learning-forgetting trade-off". |
| Ramesh AA, Lewandowski A, Schmidhuber J. *Learning to Forget: Continual Learning with Adaptive Weight Decay.* arXiv:2604.27063 (29 Apr 2026) | [S] | "a fixed scalar weight decay drives this forgetting uniformly over time and uniformly across all parameters"; FADE "adapts per-parameter weight decay rates online via approximate meta-gradient descent", derived for the online linear setting, applied to the final layer. |
| *Attribution-Guided Continual Learning for Large Language Models.* arXiv:2605.05285 (v1 6 May 2026; v2 13 Jul 2026) | [S] | Layer-wise Relevance Propagation estimates parameter importance; "parameters critical to previous tasks are constrained to receive smaller updates". |
| van de Ven GM (as displayed). *On the Computation of the Fisher Information in Continual Learning.* arXiv:2502.11756; ICLR 2025 blogpost track | [S] | "the exact way in which the Fisher Information is computed is however rarely described, and multiple different implementations for it can be found online ... many currently reported results for EWC could likely be improved by changing the way the Fisher Information is computed." |
| According to PubMed: Wang J, Hu M, Li N, Al-Ali A, Suganthan PN. *Randomized neural network with adaptive forward regularization for online task-free class incremental learning.* Neural Networks 2026;203:109115. [doi 10.1016/j.neunet.2026.109115](https://doi.org/10.1016/j.neunet.2026.109115) | [PubMed] | edRVFL-kF adjusts "the intervention intensity of forward knowledge"; "to ... eliminate intractable tuning of -kF, we rebuild with online Bayesian learning and propose the plug-and-play edRVFL-kF-Bayes, enabling all hard ks ... to self-adapt". |
| According to PubMed: Wang J, Hu M, Li N, Al-Ali A, Suganthan PN. *Incremental Online Learning of Randomized Neural Network With Forward Regularization.* IEEE TPAMI 2026;48(5):5277–5293. [doi 10.1109/TPAMI.2026.3652081](https://doi.org/10.1109/TPAMI.2026.3652081) | [PubMed] | ridge (-R) and forward (-F) regularisation with "recursive weight updates and variable learning rates"; regret bounds. |
| According to PubMed: Liu S, Wang L, Yan R, Huo J, Li W, Gao Y. *A continual learning framework with long-term and multiple short-term memory networks.* Neural Networks 2026;200:108774. [doi 10.1016/j.neunet.2026.108774](https://doi.org/10.1016/j.neunet.2026.108774) | [PubMed] | identifies "limitations of the commonly used Euclidean distance-based regularizers" and proposes a Gaussian-mixture regulariser; "compatible with various weight regularization based algorithms". |
| According to PubMed: Tzanis E, Klontzas ME. *ReclAIm: A Multiagent Framework for Monitoring and Correcting Performance Decline in Medical Imaging AI.* Radiology: Artificial Intelligence 2026;8(4):e250923. [doi 10.1148/ryai.250923](https://doi.org/10.1148/ryai.250923) | [PubMed] | a fine-tuning workflow with "a parameter-anchoring regularization strategy to limit catastrophic forgetting"; performance restored "to within ±2% of baseline values". |
| According to PubMed: Zhai Z et al. *Rethinking softmax in incremental learning.* Neural Networks 2025;193:108017. [doi 10.1016/j.neunet.2025.108017](https://doi.org/10.1016/j.neunet.2025.108017) | [PubMed] | "the non-identifiability inherent in the standard softmax cross-entropy distillation loss"; imbalance-invariant and shift-sensitive alternatives improve LwF, LwM and LUCIR. |

## B. Projection, subspace and gradient-modification methods

| paper | record | what the rendering says |
|---|---|---|
| *KeepLoRA: Continual Learning with Residual Gradient Adaptation.* arXiv:2601.19659 (27 Jan 2026); ICLR 2026 | [S] | general knowledge "mainly encoded in the principal subspace", task-specific in the residual; new-task gradients projected "onto a subspace orthogonal to both the principal subspace of pre-trained model and the dominant directions of previous task features". |
| *Safety Alignment as Continual Learning: Mitigating the Alignment Tax via Orthogonal Gradient Projection.* arXiv:2602.07892 (v2) | [S] | OGPSA "estimates a low-rank reference subspace from gradients on a small set of general-capability data and removes from each safety gradient the component lying in this subspace". |
| *SafeAnchor: Preventing Cumulative Safety Erosion in Continual Domain Adaptation of Large Language Models.* arXiv:2604.17691 | [S] | "low-rank safety subspaces in LoRA parameter space via Fisher Information eigendecomposition", gradients constrained to the orthogonal complement, "threshold-triggered corrective replay". |
| Lu B, Deng Z et al. *Muon-OGD: Muon-based Spectral Orthogonal Gradient Projection for LLM Continual Learning.* arXiv:2605.08949 (9 May 2026) | [S] | projection methods "typically formulated under Euclidean parameter geometry ... governed by the Frobenius norm"; spectral-norm-aware projection. |
| *On the Plasticity and Stability for Post-Training Large Language Models.* arXiv:2602.06453 | [S] | in GRPO, "geometric conflict between plasticity and stability gradients"; Probabilistic Conflict Resolution models gradients as random variables and arbitrates "via an uncertainty-aware soft projection". |
| Hu Y, Yu Z, Cheng Z, Liu W, Song L. *Hidden Failure Modes of Gradient Modification under Adam in Continual Learning ...* arXiv:2604.22407 (April 2026) — **withdrawn by the authors** | [S] | gradient modification "upstream" of Adam has a hidden failure mode through the second-moment pathway; the rendering states the authors withdrew the manuscript over issues in the experimental design. Cited only for the caution. |
| Bach T et al. (as displayed). *Continual Safety Alignment via Gradient-Based Sample Selection.* arXiv:2604.17215; ACL Findings 2026 | [S] | "high-gradient samples cause greater safety degradation ... moderate-gradient samples enable task learning with minimal alignment loss"; filters high-gradient samples. |
| Awasthi A, Apolinario M, Roy K. *MANGO: Meta-Adaptive Network Gradient Optimization for Online Continual Learning.* arXiv:2605.19080 (18 May 2026) | [S] | "balances stability-plasticity via gradient-gating and meta-learned regularization". |

## C. Large-language-model forgetting, architecture and RLHF context

| paper | record | what the rendering says |
|---|---|---|
| *Mechanistic Analysis of Catastrophic Forgetting in Large Language Models During Continual Fine-tuning.* arXiv:2601.18699 (v1, v2) | [S] | twenty mid-2026 models; "gradient interference in attention weights, representational drift in intermediate layers, and loss landscape flattening"; forgetting "correlates strongly with task similarity"; Low-Rank Circuit Projection mitigates "up to 94.2% of ancestral capabilities". |
| Ganguli A (as displayed). *TFGN: Task-Free, Replay-Free Continual Pre-Training Without Catastrophic Forgetting at LLM Scale.* arXiv:2605.15053 (v2) | [S] | every published method "retains a buffer ... requires task identifiers ... applies a regularization penalty that scales poorly with model size, or operates at sentence-classification scale"; an architectural overlay; backward transfer −0.007 at 8B, "no Fisher penalty". |
| Alssum L, Itani H, Hammoud HAAK, Torr P, Bibi A, Ghanem B. *Unforgotten Safety: Preserving Safety Alignment of Large Language Models with Continual Learning.* arXiv:2512.10150 (10 Dec 2025) | [S] | frames safety degradation under fine-tuning as continual learning; regularisation-, memory- and merging-based CL approaches "consistently achieve lower attack success rates than standard fine-tuning". |
| Shenfeld I et al. *RL's Razor: Why Online Reinforcement Learning Forgets Less.* arXiv:2509.04259; ICLR 2026 | [S] | "the degree of forgetting is determined by the distributional shift, measured as the KL-divergence between the fine-tuned and base policy evaluated on the new task"; on-policy RL is "implicitly biased towards KL-minimal solutions". |
| Gauthier E, Bach F, Jordan MI. *Explaining and Preventing Alignment Collapse in Iterative RLHF.* arXiv:2605.04266 | [S] | a parameter-steering term dropped by standard iterative RLHF; foresighted policy optimization regularises it. Context only. |
| *Rethinking KL Regularization in RLHF: From Value Estimation to Gradient Optimization.* arXiv:2510.01555 (2025) | [S] | analyses KL regularisation implementations; context for the adaptive-KL comparison. |

## Named as context, not fetched

Kirkpatrick et al. 2017 (fetched on 2026-09-22 via PubMed, see `Continuous_Learning/CONTINUOUS_LEARNING.md` §10); Zenke et al. 2017 (PubMed); Li and Hoiem 2018 (PubMed); Aljundi et al. 2018; Buzzega et al. 2020; Chaudhry et al. 2019; Chen et al. 2018 (GradNorm); Guo et al. 2020 (MEGA); Désidéri 2012; Ziegler et al. 2019 (the adaptive KL controller); Farajtabar et al. 2020 (OGD); Saha et al. 2021 (GPM); Ritter et al. 2018 (online structured Laplace).
