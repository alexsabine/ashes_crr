# Citations checked on the day — the Adam checks, the gradient-ratio family and the rupture detector (R10), 2026-09-23

Owner request (prompt-log entry 104): "Search online as necessary for prior art". This file is the literature record for
`Continuous_Learning/ADAM_AND_PRIOR_ART.md` and `Rupture_Detection/RUPTURE_DETECTION.md`. Nothing here is a result.

**Access, stated once.** The egress proxy blocked arxiv.org on the day (WebFetch of `arxiv.org/abs/2601.19788` returned
EGRESS_BLOCKED), as it did on 2026-09-22 (`continual_learning_2026-09-22.md`). No link returned a 404.

The records are marked as follows:
- **[S]** is a search-engine rendering of the abstract or venue page, unverified against the source.
- **[code]** means the text was read in the authors' public code on the day.
- **[named]** means the item is named from the rendering only.

## A. The gradient-ratio family (prior art for the rule's weight)

| work | record | what was read |
|---|---|---|
| Esser P, Rombach R, Ommer B. *Taming Transformers for High-Resolution Image Synthesis.* arXiv:2012.09841 (v1 17 Dec 2020; v2 and v3 listed); CVPR 2021 | [S] + [code] | the adaptive weight, read in `CompVis/taming-transformers`, `taming/modules/losses/vqperceptual.py`: `d_weight = torch.norm(nll_grads) / (torch.norm(g_grads) + 1e-4)`, then `torch.clamp(d_weight, 0.0, 1e4).detach()`; the gradients are taken at the decoder's last layer; the loss is `nll_loss + d_weight * disc_factor * g_loss + ...`. This is the rule's form, w = ‖g_present‖/‖g_other‖ with a cap of 1e4, without the EMA, published in 2020 |
| Wang S, Teng Y, Perdikaris P. *Understanding and mitigating gradient flow pathologies in physics-informed neural networks.* SIAM J. Sci. Comput. 43(5):A3055–A3081 (2021) | [S] | "a learning rate annealing algorithm that utilizes gradient statistics during model training to balance the interplay between different terms in composite loss functions". The formula was not read, so none is attributed |
| Chen Z, Badrinarayanan V, Lee C-Y, Rabinovich A. *GradNorm.* ICML 2018 | [named] (as 2026-09-22) | learned task weights equalising gradient norms; the battery row in `CROSS_VERIFICATION.md` |
| *Knowledge-Aware Evolution for Task-Free Streaming Federated Continual Learning with Arbitrary Class Overlap* (FedKACE). arXiv:2601.19788 (January 2026) | [S] | "an adaptive gradient-balanced replay scheme that utilizes the ratio of the squared L2 gradient norms to balance client-specific knowledge between new acquisition and old retention". One rendering describes the weight as the ratio of the buffer's squared gradient norm to the new data's, recomputed per epoch. The direction of the ratio is unverified. This is the closest published continual-learning use of a gradient-norm ratio as the replay weight. It postdates the owner's EPO filing (August 2025, owner's statement) and predates the repository's publication (2026-09-15) |

## B. Adam, decoupling and clipping

| work | record | what was read |
|---|---|---|
| Kingma DP, Ba J. *Adam.* arXiv:1412.6980; ICLR 2015 | [named] | the update is invariant to rescaling of the gradient, and the step is bounded by the step size. This is checked numerically here as A1, not taken from the paper |
| Loshchilov I, Hutter F. *Decoupled Weight Decay Regularization.* arXiv:1711.05101; ICLR 2019 | [S] | "L2 regularization and weight decay regularization are equivalent for standard stochastic gradient descent (when rescaled by the learning rate), but ... this is not the case for adaptive gradient algorithms, such as Adam"; the fix decouples the decay "from the optimization steps taken with respect to the loss function" (AdamW). The A5 check applies the rule's past pull in the same decoupled position |
| Seetharaman P, Wichern G, Pardo B, Le Roux J. *AutoClip: Adaptive Gradient Clipping for Source Separation Networks.* arXiv:2007.14469 (v1 25 Jul 2020); IEEE MLSP 2020 | [S] | the clipping threshold is "the p-th percentile of recently observed gradient norms", from "the history of gradient norms observed during training". This is prior art for EQ-B's present-gradient clip (κ × the largest kept length among the last N batches) |
| Polyak BT. *Some methods of speeding up the convergence of iteration methods.* 1964 | [named] | the heavy-ball method. Its stability bound on a quadratic, η λ_max < 2(1 + β), is the edge used in A8 and verified numerically there |

## C. Change detection and machine monitoring (prior art for the rupture detector)

| work | record | what was read |
|---|---|---|
| Page ES. *Continuous inspection schemes.* Biometrika 41:100–115 (1954) | [named] | the CUSUM, used unchanged in the battery for every windowing |
| Scheffer M, Bascompte J, Brock WA et al. *Early-warning signals for critical transitions.* Nature 461:53–59 (2009); PubMed 19727193 | [S] | "changes in statistical properties (variance, skewness, autocorrelation) may precede critical transitions". Variance and lag-1 autocorrelation are the `ews` baseline |
| Fyfe KR, Munck EDS. *Analysis of computed order tracking.* Mechanical Systems and Signal Processing 11:187–205 (1997) | [S] | computed order tracking resamples a vibration signal at constant shaft angle, by interpolation from a tachometer, so that analysis is "in orders" rather than hertz. This is prior art for sampling a variable-speed signal on its own phase |
| Tacholess order tracking (review of methods; e.g. *A Tacholess Order Tracking Method Based on Inverse Short Time Fourier Transform and Singular Value Decomposition for Bearing Fault Diagnosis*, Sensors 20(23):6924, 2020, doi 10.3390/s20236924) | [S] | the phase used for resampling is estimated from the vibration signal itself; "the Hilbert transform is used to estimate the instantaneous phase of reference shaft". This is prior art for taking the cut's phase from the analytic signal of the measured channel |
| Adams RP, MacKay DJC. *Bayesian Online Changepoint Detection.* arXiv:0710.3742 (2007) | [named] | not run in the battery (a stronger baseline to add in any registered study) |

## D. Patent context (information, not legal advice)

| source | record | what was read |
|---|---|---|
| EPO Guidelines for Examination G-II 3.3 (mathematical methods) and 3.3.1 (AI and ML) | [S] (xepc.eu; practitioner summaries) | a mathematical method "may contribute to the technical character of an invention by its application to a field of technology and/or by being adapted to a specific technical implementation". Among the Guidelines' examples: "the use of a neural network in a heart-monitoring apparatus for the purpose of identifying irregular heartbeats makes a technical contribution". The claim must be "functionally limited to a specific technical purpose". This is already recorded in `alexander_plan_2026-09-23.md` |
