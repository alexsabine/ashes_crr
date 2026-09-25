# Citations checked on the day — the Ω = 1 equal-pull rule against multi-objective optimisation and gradient balancing (R10), 2026-09-25

Literature check requested through the orchestrating session on 2026-09-25. It reads the repository's result on the rule
w = Ω‖ĝ_p‖/‖ĝ_q‖ (`Continuous_Learning/CONTINUOUS_LEARNING.md` §4.1, §4.2, §4.4, §4.5 and §5) against multi-objective
optimisation (MOO), multi-task gradient balancing and continual learning framed as a Pareto problem. Nothing here is a
result (R8). The inferences in the last section are labelled as inferences and are not ledger rows.

**Fetch date.** Every source was fetched on 2026-09-25 (UTC). The raw fetched text is in the session scratchpad
(`lit0925/pareto/`, one `<id>.abs.txt` and `<id>.full.txt` per arXiv paper, plus the PDFs and code files named below). The
scratchpad is not committed.

**Access, stated once.**
- **What loaded.** arxiv.org loaded on the day, unlike 2026-09-22 and 2026-09-23, when the proxy blocked it
  (`continual_learning_2026-09-22.md`, `continual_learning_2026-09-23.md`):
  - abstract pages at `arxiv.org/abs/<id>`, with the title checked against each id before use;
  - HTML full text at `arxiv.org/html/<id>vN`, which returned the rendered paper for every id tried, including pre-2023
    papers.
- **Other hosts that loaded.** comptes-rendus.academie-sciences.fr (Désidéri 2012, PDF), proceedings.mlr.press (abstract
  pages), raw.githubusercontent.com (PMLR PDF; LibMTL code), iclr.cc (virtual poster page) and
  proceedings.neurips.cc.
- **Blocked or refused.**
  - openreview.net redirected to a bot challenge (`/challenge?redirect=...`), and its APIs (api.openreview.net,
    api2.openreview.net) returned 403. The IMTL paper (ICLR 2021) exists only on OpenReview, so its full text was not read.
  - discovery.ucl.ac.uk and researchgate.net returned 403.
  - The api.semanticscholar.org search returned 429. The semanticscholar.org root returned 200.
  - The export.arxiv.org API was not used, as instructed.
- **No 404s.** No link returned a 404.
- **Search.** Web search was used for discovery only.

**How the text was extracted.** arXiv HTML was converted to text by a local script that keeps each formula's LaTeX
`alttext`. The script also dropped some text after a literal `<`, so a few formulas are truncated in the saved files. No
quote below is taken from a truncated span. Where a quote contains mathematics, it is transliterated from that LaTeX and
marked *(math transliterated)*. The words are verbatim. PDFs were converted with pypdfium2. In Désidéri's formulas the
extraction lost the norm bars; where this matters it is said.

**Tags.**
- **[F]**: the full text was fetched and the quote was read in it.
- **[A]**: the abstract or venue page was read, not the paper.
- **[code]**: the quote is from the authors' or a reference implementation's source code, read on the day.
- **[S]**: a search-engine rendering only, unverified.
- **[title]**: the title was seen, not the content.

## Q1. MGDA: the min-norm point, Pareto-stationarity, and whether MGDA stops anywhere on the front

| work | version and date | URL | quote (verbatim from the fetched text) | tag |
|---|---|---|---|---|
| Désidéri J-A. *Multiple-gradient descent algorithm (MGDA) for multiobjective optimization.* C. R. Acad. Sci. Paris, Ser. I 350 (2012) 313–318 | journal version; received 6 March 2012, online 29 March 2012 | https://comptes-rendus.academie-sciences.fr/mathematique/articles/10.1016/j.crma.2012.03.014/ (PDF at `/mathematique/item/10.1016/j.crma.2012.03.014.pdf`) | Definition 1.1: "The design-point Y 0 is said to be Pareto-stationary iff there exists a convex combination of the gradient-vectors, {ui}, that is equal to zero". The algorithm, step (i): "If ω = 0 (or sufficiently small), stop." "The above MGDA can stop after a finite number of iterations if a Pareto-stationary design-point has been reached." Remark 3: "If the gradients are not normalized (Si = 1, ∀i), the direction of the minimum-norm element ω is expected to be mostly influenced by the gradients of small norms in the family". Of the normalisations listed next: "The first formula is a standard normalization: it has the merit of providing a stable definition". The first formula is ∇J_i/‖∇J_i‖; the PDF extraction lost the norm bars, and this reading is the author of this dossier's. | [F] |
| Sener O, Koltun V. *Multi-Task Learning as Multi-Objective Optimization.* NeurIPS 2018. arXiv:1810.04650 | v2, 11 Jan 2019 (v1 10 Oct 2018) | https://arxiv.org/abs/1810.04650 | "Any solution that satisfies these conditions is called a Pareto stationary point. Although every Pareto optimal point is Pareto stationary, the reverse may not be true." "Désidéri (2012) showed that either the solution to this optimization problem is 0 and the resulting point satisfies the KKT conditions, or the solution gives a descent direction that improves all tasks." *(math transliterated)* Of the two-point min-norm problem: "As the geometry suggests, the solution is either an edge case or a perpendicular vector." | [F] |
| Lin X, Zhen H-L, Li Z, Zhang Q, Kwong S. *Pareto Multi-Task Learning.* NeurIPS 2019. arXiv:1912.12854 | v1, 30 Dec 2019 | https://arxiv.org/abs/1912.12854 | "If θ_t is Pareto critical, then d_t = 0 ∈ ℝ^n and α_t = 0." *(math transliterated)* On MGDA: "this method does not have a systemic way to incorporate different trade-off preference information. As shown in Fig. 2, running the algorithm multiple times can only generate some solutions in the middle of the Pareto front on the synthetic example." | [F] |
| Liu B, Liu X, Jin X, Stone P, Liu Q. *Conflict-Averse Gradient Descent for Multi-task Learning* (CAGrad). NeurIPS 2021. arXiv:2110.14048 | v2, 21 Feb 2024 (v1 26 Oct 2021) | https://arxiv.org/abs/2110.14048 | "most of them lack convergence guarantee and/or could converge to any Pareto-stationary point." "unlike our method, MGDA is designed to converge to an arbitrary point on the Pareto set, without explicit control of which point it will converges to." "PCGrad also converges to an arbitrary Pareto point without explicit control of which point it will arrive at." From the toy experiment: "MGDA and PCGrad converge to different Pareto-stationary points depending on θ_init." *(math transliterated)* | [F] |
| Navon A, Shamsian A, Achituve I, Maron H, Kawaguchi K, Chechik G, Fetaya E. *Multi-Task Learning as a Bargaining Game* (Nash-MTL). ICML 2022. arXiv:2202.01017 | v2, 8 Jul 2022 (v1 2 Feb 2022) | https://arxiv.org/abs/2202.01017 | From the convergence proof: "We first note that if for some step we reach a Pareto stationary solution the algorithm halts and sequence stays fixed at that point and therefore converges" | [F] |
| Senushkin D, Patakin N, Kuznetsov A, Konushin A. *Independent Component Alignment for Multi-Task Learning* (Aligned-MTL). CVPR 2023. arXiv:2305.19000 | v1, 30 May 2023 | https://arxiv.org/abs/2305.19000 | "Approaches aiming to find a Pareto-stationary solution (such as Fig. 1c and Fig. 1d) terminate once the Pareto front is first reached, as a result, they might provide a suboptimal solution." "IMTL [27], and Nash-MTL [37] aims at finding Pareto-stationary solution (Def. 1). As a result, they terminate optimization once they reach a solution in the Pareto front. Accordingly, the final result strongly depends on an initialization point". "Methods that guarantee only Pareto-front convergence (such as IMTL[27] and NashMTL [37]) fail to achieve global optimum ... and converge to an arbitrary Pareto-front solution with unknown task balance." | [F] |
| Yu T, Kumar S, Gupta A, Levine S, Hausman K, Finn C. *Gradient Surgery for Multi-Task Learning* (PCGrad). NeurIPS 2020. arXiv:2001.06782 | v4, 22 Dec 2020 (v1 19 Jan 2020) | https://arxiv.org/abs/2001.06782 | "A sub-optimal solution occurs when the cosine similarity between the gradients of the two tasks is exactly −1, i.e. the gradients directly conflict, leading to zero gradient after applying PCGrad. However, in practice, since we are using SGD, which is a noisy estimate of the true batch gradients, the cosine similarity between the gradients of two tasks in a minibatch is unlikely to be −1, thus avoiding this scenario." *(math transliterated)* | [F] |
| Gupta K, Murthy S, Karabag MO, Topcu U, Fridovich-Keil D. *Cooperative Bargaining Games Without Utilities: Mediated Solutions from Direction Oracles* (DiBS). NeurIPS 2025. arXiv:2505.14817 | v2, 16 Oct 2025 (v1 20 May 2025) | https://arxiv.org/abs/2505.14817 | On the plain sum of normalised gradients, their eq. 2: "it is natural to construct a simple bargaining procedure which utilizes the sum of normalized gradients". Example 2, the game on x² and (x−1)² over [0,1]: "Let eq. 2 be initialized at some x_0 ∈ (0,1), x_0 ≠ 1/2. Then, because [the two normalised gradients are opposite], we get convergence at x = x_0, which is not a fair solution as x_0 can be initialized arbitrarily in (0,1) far away from x = 1/2." *(math transliterated; bracket paraphrases a formula)* "In such a situation, both algorithms stop wherever initialized and find points which are technically Pareto stationary, but heavily favor one agent." | [F] |
| Murthy S, Gupta K, Karabag MO, Fridovich-Keil D, Topcu U. *Monotonic Transformation Invariant Multi-task Learning* (DiBS-MTL). arXiv:2509.23948 | v2, 2 Feb 2026 (v1 28 Sep 2025) | https://arxiv.org/abs/2509.23948 | Appendix C, the losses x² + (y−1)² and x² + (y+1)²: "Then any point of the form (0, y), y ∈ [−1, 1] is a valid solution that IMTL-G can give. Even though all such points are Pareto stationary solutions, only (0,0) is balanced in the sense that it is equidistant to these symmetric functions". "IMTL-G is a gradient-based method, which tries to find an update direction which has an equal projection on all task gradient vectors. Though this equal projection property brings invariance to monotonic nonaffine transformations, it also renders IMTL-G susceptible to task domination" *(math transliterated)* | [F] |

## Q2. Equal-projection and equal-norm balancing: what each balances, its fixed points, whether it selects a point, its step bound or scale property

| work | version and date | URL | quote (verbatim from the fetched text) | tag |
|---|---|---|---|---|
| Liu L, Li Y, Kuang Z, Xue J-H, Chen Y, Yang W, Liao Q, Zhang W. *Towards Impartial Multi-task Learning* (IMTL). ICLR 2021 | ICLR 2021 poster page (OpenReview id IMPnRXEWpvr; full text blocked) | https://iclr.cc/virtual/2021/poster/2894 | "for the task-shared parameters, we optimize the scaling factors via a closed-form solution, such that the aggregated gradient (sum of raw gradients weighted by the scaling factors) has equal projections onto individual tasks." "our IMTL can converge to similar results even when the task losses are designed to have different scales, and thus it is scale-invariant." | [A] |
| same (IMTL), secondary description | search rendering | https://www.researchgate.net/publication/354436676_Towards_Impartial_Multi-task_Learning (as rendered) | the rendering says the scaling-factor problem "is equivalent to finding the angle bisector of gradients from all tasks in geometry". Not verified against the paper | [S] |
| LibMTL (median-research-group), `LibMTL/weighting/IMTL.py`, `MGDA.py`, `DB_MTL.py` | main at commit 4336804847eaa5e0b924b743d76beec7ac3fdc97 (git ls-remote, 2026-09-25) | https://github.com/median-research-group/LibMTL | IMTL-G: `grads_unit = grads/torch.norm(grads, p=2, dim=-1, keepdim=True)`, `U = grads_unit[0:1].repeat(self.task_num-1, 1) - grads_unit[1:]`, `alpha = torch.cat((1-alpha.sum().unsqueeze(0), alpha), dim=0)`, so the weights sum to one and equalise projections onto the unit gradients. MGDA: `if ntype == 'l2': gn = grads.pow(2).sum(-1).sqrt()`, with the two-vector solver `gamma = -1.0 * ( (v1v2 - v2v2) / (v1v1+v2v2 - 2*v1v2) )`. DB-MTL: `alpha = u_grad.max() / (u_grad + 1e-8)` on an EMA `self.grad_buffer` | [code] |
| Chen Z, Badrinarayanan V, Lee C-Y, Rabinovich A. *GradNorm.* ICML 2018. arXiv:1711.02257 | v4, 12 Jun 2018 (v1 7 Nov 2017) | https://arxiv.org/abs/1711.02257 | "Note that α = 0 will always try to pin the norms of backpropagated gradients from each task to be equal at W." *(math transliterated)* "Renormalize w_i(t+1) so that Σ_i w_i(t+1) = T" *(math transliterated)* "GradNorm also matches or surpasses the performance of exhaustive grid search methods, despite only involving a single asymmetry hyperparameter α." | [F] |
| Navon et al. *Nash-MTL.* arXiv:2202.01017 | v2, 8 Jul 2022 | https://arxiv.org/abs/2202.01017 | "Axiom 2.4 means that the solution does not take into account the gradients’ norms but rather treats all of them the same, as if they were normalized." "if all g_i are orthogonal we get α_i = 1/‖g_i‖ and Δθ = Σ g_i/‖g_i‖ which is the obvious scale invariant solution." *(math transliterated)* "We note that the optimal solution under Nash-MTL for the two tasks case is equivalent to independently normalizing each gradient and summing with equal weights." On IMTL-G: "We note that this update direction satisfies all of the Nash axioms except for Pareto optimally. Thus, unlike our proportionally fair approach, it can settle for a sub-optimal solution for the sake of fairness." Step size in Theorem 5.4: "Set μ^(t) = min_{i∈[K]} 1/(LKα_i^(t))." *(math transliterated)* | [F] |
| Senushkin et al. *Aligned-MTL.* arXiv:2305.19000 | v1, 30 May 2023 | https://arxiv.org/abs/2305.19000 | "Aligned-MTL provably converges to an optimal point with pre-defined task-specific weights". "Differently, Aligned-MTL drifts along the Pareto front and provably converges to the optimum w.r.t. pre-defined tasks weights." Its scale: "we choose the largest scale that guarantees convergence to the optimum of an original problem (Eq. 1): this is a minimal singular value of an initial gradient matrix". The aligned gradients are "orthogonal (non-conflicting) and of equal magnitude (non-dominant)". | [F] |
| Liu et al. *CAGrad.* arXiv:2110.14048 | v2, 21 Feb 2024 | https://arxiv.org/abs/2110.14048 | "CAGrad balances the objectives automatically and still provably converges to a minimum over the average loss. It includes the regular gradient descent (GD) and the multiple gradient descent algorithm (MGDA) in the multi-objective optimization (MOO) literature as special cases." "For any c ≥ 1, all the fixed points of CAGrad are Pareto-stationary points" *(math transliterated)* | [F] |
| Liu B, Feng Y, Stone P, Liu Q. *FAMO: Fast Adaptive Multitask Optimization.* NeurIPS 2023. arXiv:2306.03792 | v3, 30 Oct 2023 (v1 6 Jun 2023) | https://arxiv.org/abs/2306.03792 | "We introduce FAMO, an MTL optimizer that decreases task losses approximately at equal rates while using only O(1) space and time per iteration." *(math transliterated)* "Therefore, the minimum points of Σ_{i=1}^k log ℓ_i(θ) are all stationary points of (13)." *(math transliterated)* The SI baseline "minimizes Σ_k log L^k(θ), as SI is invariant to any scalar multiplication of task losses" *(math transliterated)* | [F] |
| Yu et al. *PCGrad.* arXiv:2001.06782 | v4, 22 Dec 2020 | https://arxiv.org/abs/2001.06782 | Theorem 1: "the PCGrad update rule with step size t ≤ 1/L will converge to either (1) a location in the optimization landscape where cos(φ_12) = −1 or (2) the optimal value L(θ*)." *(math transliterated)* | [F] |
| Lin et al. *Pareto MTL.* arXiv:1912.12854 | v1, 30 Dec 2019 | https://arxiv.org/abs/1912.12854 | "Pareto MTL decomposes a given MTL problem into several subproblems with a set of preference vectors. Each MTL subproblem aims at finding one Pareto solution in its restricted preference region." "We show that the proposed Pareto MTL can be reformulated as a linear scalarization approach to solve MTL with dynamically adaptive weights." | [F] |
| Mahapatra D, Rajan V. *Multi-Task Learning with User Preferences: Gradient Descent with Controlled Ascent in Pareto Optimization* (EPO). ICML 2020, PMLR 119 | PMLR page | https://proceedings.mlr.press/v119/mahapatra20a.html | "A common requirement in MTL applications, that cannot be addressed by these methods, is to find a solution satisfying userspecified preferences with respect to task-specific losses." "Our unique approach combines multiple gradient descent with carefully controlled ascent to traverse the Pareto front in a principled manner, which also makes it robust to initialization." | [A] |
| Mahapatra D, Rajan V. *Exact Pareto Optimal Search for Multi-Task Learning and Multi-Criteria Decision-Making* (EPO Search). arXiv:2108.00597 | v2, 17 Sep 2023 (v1 2 Aug 2021) | https://arxiv.org/abs/2108.00597 | "Chebyshev scalarization (CS) is a well-known approach to obtain an Exact Pareto Optimal (EPO), i.e., a solution on the Pareto front (PF) that intersects the ray defined by the inverse of the weights." "When initialized on the PF, EPO Search can trace the PF and converge to the required EPO solution at a linear rate of convergence." | [F] |
| Lin B, Jiang W, Ye F, Zhang Y, Chen P, Chen Y-C, Liu S, Tsang IW, Kwok JT. *Dual-Balancing for Multi-Task Learning* (DB-MTL). Neural Networks (accepted). arXiv:2308.12029 | v3, 26 Nov 2025 (v1 23 Aug 2023) | https://arxiv.org/abs/2308.12029 | "we achieve gradient-magnitude balancing by normalizing each task’s gradient to the same magnitude as the maximum gradient norm". It uses an EMA of task gradients: "Exponential moving average (EMA), which is popularly used in adaptive gradient methods (e.g., RMSProp [48], AdaDelta [60], and Adam [22]), is used to estimate" the expected gradient. "After normalization, all tasks contribute with comparable magnitudes to the update direction." On the scale: "when all task gradient norms are small, model θ_k is close to a stationary solution for all tasks, and α_k should be small so that the solution will no longer change." *(math transliterated)* | [F] |
| Ban H, Ji K. *Fair Resource Allocation in Multi-Task Learning* (FairGrad). ICML 2024. arXiv:2402.15638 | v2, 2 Jul 2024 (v1 23 Feb 2024) | https://arxiv.org/abs/2402.15638 | "FairGrad with proportional fairness resembles Nash-MTL (Navon et al., 2022), and can find more balanced solutions along the Pareto front." "Max-min fairness emphasizes more on the less-fortune task with a smaller gradient magnitude." On stochastic gradients: "(Zhou et al., 2022) proposed a correlation-reduced stochastic gradient manipulation method to address the non-convergence issue of MGDA, CAGrad, and PCGrad in the stochastic setting." | [F] |
| Quinton P, Rey V. *Jacobian Descent for Multi-Objective Optimization* (UPGrad). arXiv:2406.16232 | v3, 3 Feb 2025 (v1 23 Jun 2024) | https://arxiv.org/abs/2406.16232 | "In a step of GD, the update scales proportionally to the gradient norm. Small gradients thus lead to small updates, and conversely, large gradients lead to large updates. To maintain coherence with GD, it would be natural that the rows of the Jacobian also contribute to the aggregation proportionally to their norm." Their Table 1 marks IMTL-G, Nash-MTL, MGDA, CAGrad and Aligned-MTL as not "Linear under scaling". | [F] |
| Yuan J, Zhang R. *Equitable Multi-task Learning* (EMTL). arXiv:2306.09373 | v2, 19 Jun 2023 | https://arxiv.org/abs/2306.09373 | "we ... find that regularizing relative contribution of different tasks (i.e. value of task-specific loss divides its raw gradient norm) in updating shared parameter can improve generalization performance of MTL." | [A] |
| Chen W, Lin B, Zhang X, Lin X, Zhao H, Zhang Q, Kwok JT. *Gradient-Based Multi-Objective Deep Learning: Algorithms, Theories, Applications, and Beyond* (survey). arXiv:2501.10945 | v3, 6 Aug 2025 (v1 19 Jan 2025) | https://arxiv.org/abs/2501.10945 | "IMTL-G(rad) (Liu et al., 2021a) aims to find d that has equal projections on all objective gradients." *(math transliterated)* "Dual-Balancing Multi-Task Learning (DB-MTL) (Lin et al., 2023) also normalizes all objective gradients to the same magnitude." | [F] |

## Q3. Scalarisation against Pareto methods, and "scalarisation is enough"

| work | version and date | URL | quote (verbatim from the fetched text) | tag |
|---|---|---|---|---|
| Xin D, Ghorbani B, Garg A, Firat O, Gilmer J. *Do Current Multi-Task Optimization Methods in Deep Learning Even Help?* NeurIPS 2022. arXiv:2209.11379 | v1, 23 Sep 2022 | https://arxiv.org/abs/2209.11379 | "It can be easily shown that any solution to problem (1) is guaranteed to be Pareto optimal." "These results suggest that, at least for convex setups, sweeping the task weights should be sufficient for full exploration of the Pareto frontier. In particular, in the convex setting it is provable that no algorithm can outperform properly chosen scalarization that has been trained to convergence." "all of the MTO algorithms in our study simply yield performance trade-off points on the scalarization Pareto front." "Even subtle choices regarding the hyper-parameter grid can drastically change the results." | [F] |
| Kurin V, De Palma A, Kostrikov I, Whiteson S, Kumar MP. *In Defense of the Unitary Scalarization for Deep Multi-Task Learning.* NeurIPS 2022. arXiv:2201.04122 | v4, 8 Mar 2023 (v1 11 Jan 2022) | https://arxiv.org/abs/2201.04122 | "We show that unitary scalarization, coupled with standard regularization and stabilization techniques from single-task learning, matches or improves upon the performance of complex multi-task optimizers". "no SMTO consistently outperforms unitary scalarization in spite of the added complexity and overhead." On MGDA as run: "In practice, per-task gradients are rescaled before applying MGDA: the original authors’ implementation [54] relies on" dividing each gradient by its norm times its loss *(formula paraphrased)*. "The convergence of MGDA to a Pareto-stationary point is still guaranteed after normalization [14]." | [F] |
| Hu Y, Xian R, Wu Q, Fan Q, Yin L, Zhao H. *Revisiting Scalarization in Multi-Task Learning: A Theoretical Perspective.* NeurIPS 2023. arXiv:2308.13985 | v2, 22 Sep 2023 (v1 27 Aug 2023) | https://arxiv.org/abs/2308.13985 | "scalarization is inherently incapable of full exploration, especially for those Pareto optimal solutions that strike the balanced trade-offs between multiple tasks." "This leads to the conclusion that scalarization is in general incapable of tracing out the Pareto front." | [A] |
| Mahapatra, Rajan. *EPO Search.* arXiv:2108.00597 | v2, 17 Sep 2023 | https://arxiv.org/abs/2108.00597 | "Figure 1(a) shows how linear scalarization can have non-unique Pareto optimal points (red) for the same weight r; among the 3 optima, the green one, a saddle point for LS (5), cannot be attained." *(math transliterated)* | [F] |
| Gama GS, Grassi V Jr. *Uniform Loss vs. Specialized Optimization: A Comparative Analysis in Multi-Task Learning.* arXiv:2505.10347 | v3, 20 Mar 2026 (v1 15 May 2025) | https://arxiv.org/abs/2505.10347 | "Our findings indicate that SMTOs perform well compared to uniform loss and that fixed weights can achieve competitive performance compared to SMTOs." | [A] |
| Elich C, Kirchdorfer L, Köhler JM, Schott L. *Examining Common Paradigms in Multi-Task Learning.* GCPR 2024. arXiv:2311.04698 | v5, 15 Aug 2024 (v1 8 Nov 2023) | https://arxiv.org/abs/2311.04698 | "We show that Adam’s mechanism to estimate a parameter-specific learning rate is partially loss-scale invariant and hypothesize that this could contribute to Adams effectiveness in MTL." "We emphasize differences in gradient magnitude as the main distinguishing factor." | [F] |
| Lin B, Ye F, Zhang Y, Tsang IW. *Reasonable Effectiveness of Random Weighting: A Litmus Test for Multi-Task Learning.* TMLR. arXiv:2111.10603 | v2, 27 Jul 2022 (v1 20 Nov 2021) | https://arxiv.org/abs/2111.10603 | "RW methods can achieve comparable performance with state-of-the-art baselines. Therefore, we think that the RW methods are important baselines for MTL" | [A] |
| Kendall A, Gal Y, Cipolla R. *Multi-Task Learning Using Uncertainty to Weigh Losses for Scene Geometry and Semantics.* CVPR 2018. arXiv:1705.07115 | v3, 24 Apr 2018 (v1 19 May 2017) | https://arxiv.org/abs/1705.07115 | "We interpret minimising this last objective with respect to σ_1 and σ_2 as learning the relative weight of the losses L_1(W) and L_2(W) adaptively, based on the data." *(math transliterated)* "the homoscedastic noise and task loss is able to converge to the same minima." | [F] |

## Q4. Continual learning as a stability–plasticity (bi-objective) problem, and gradient balancing between current and past

| work | version and date | URL | quote (verbatim from the fetched text) | tag |
|---|---|---|---|---|
| Guo Y, Liu M, Yang T, Rosing T. *Improved Schemes for Episodic Memory-based Lifelong Learning* (MEGA-I, MEGA-II). NeurIPS 2020. arXiv:1909.11763 | v7, 15 Dec 2020 (v1 25 Sep 2019) | https://arxiv.org/abs/1909.11763 | MEGA-I: "α_1(w) = 1, α_2(w) = ℓ_ref(w;ζ)/ℓ_t(w;ξ) if ℓ_t(w;ξ) > ε" *(math transliterated)*. MEGA-II: "We use g_mix to denote the desired mixed stochastic gradient which has the same magnitude as ∇ℓ_t(w;ξ)." *(math transliterated)* It maximises a loss-weighted sum of the cosines to the two gradients, eq. (8). In one limiting case: "α_2(w) = ‖∇ℓ_t(w;ξ)‖_2/‖∇ℓ_ref(w;ζ)‖_2, provided that ‖∇ℓ_ref(w;ζ)‖_2 ≠ 0" *(math transliterated)*. "we show that GEM and A-GEM are degenerate cases of MEGA-I and MEGA-II which consistently put the same emphasis on the current task, regardless of how the loss changes over time." | [F] |
| Lopez-Paz D, Ranzato M. *Gradient Episodic Memory for Continual Learning* (GEM). NIPS 2017. arXiv:1706.08840 | v6, 13 Sep 2022 (v1 26 Jun 2017) | https://arxiv.org/abs/1706.08840 | "we propose a model for continual learning, called Gradient Episodic Memory (GEM) that alleviates forgetting, while allowing beneficial transfer of knowledge to previous tasks." | [A] |
| Wu Y, Wang H, Zhao P, Zheng Y, Wei Y, Huang L. *Mitigating Catastrophic Forgetting in Online Continual Learning by Modeling Previous Task Interrelations via Pareto Optimization* (POCL). ICML 2024, PMLR 235:53892–53908 | PMLR PDF | https://proceedings.mlr.press/v235/wu24ab.html (PDF via raw.githubusercontent.com/mlresearch/v235) | "we first reformulate replay-based CL methods as a unified hierarchical gradient aggregation framework." "the main task of searching for u can be reframed as the assignment of different weights λi to different g m i of previous tasks with a fixed weight on the prioritized gradient of the current task gn." (PDF extraction; the sub- and superscripts are flattened.) | [F] |
| Lai S, Zhao Z, Zhu F, Lin X, Zhang Q, Meng G. *Pareto Continual Learning: Preference-Conditioned Learning and Adaption for Dynamic Stability-Plasticity Trade-off* (ParetoCL). arXiv:2503.23390. AAAI 2025 per a search rendering [S] | v1, 30 Mar 2025 | https://arxiv.org/abs/2503.23390 | "Experience replay methods ... neglect the dynamic nature of the stability-plasticity trade-off and aim to find a fixed and unchanging balance, resulting in suboptimal adaptation during training and inference." "we propose to formulate experience replay as a MOO problem." "The preference vector α = (α_1, α_2) determines the trade-off between stability and plasticity" *(math transliterated)* | [F] |
| Nair S, Eryilmaz A, Liu J. *PMF-CL: Pareto-Minimal-Forgetting Continual Learner for Conflicting Tasks.* arXiv:2605.19145 | v2, 29 May 2026 (v1 18 May 2026) | https://arxiv.org/abs/2605.19145 | "For convex problems, it is known that any Pareto optimal solution on the Pareto front can be found by appropriately choosing a preference vector α^(T) ∈ Δ^T" *(math transliterated)*. Their preference is "in terms of the number of training samples as: α_t^(T) = n_t/Σ_{k=1}^T n_k" *(math transliterated)*, and Lemma 3.5 states that this "is equivalent to the solution of the global optimization problem". | [F] |
| Lu P, Caprio M, Eaton E, Lee I. *IBCL: Zero-shot Model Generation under Stability-Plasticity Trade-offs.* arXiv:2305.14782 | v4, 14 Oct 2025 (v1 24 May 2023) | https://arxiv.org/abs/2305.14782 | "only a few focus on obtaining models for specified trade-off preferences." IBCL "generates one Pareto-optimal model per given trade-off via convex combination without additional training." | [A] |
| Shah N, Arya G, Bharath BN, Prasad R. *Theoretical Foundations of Continual Learning via Drift-Plus-Penalty* (COLD). TMLR (accepted). arXiv:2606.08452 | v1, 7 Jun 2026 | https://arxiv.org/abs/2606.08452 | "At each task, both methods minimize the current task loss while maintaining a virtual queue that tracks deviations from long-term stability on previously learned tasks, capturing the stability-plasticity trade-off as a regulated dynamical process." "We establish stability and convergence guarantees that characterize this trade-off through a tunable control parameter." | [F] |

## Q5. Principled justifications for equal weighting or equal pull

| work | version and date | URL | quote (verbatim from the fetched text) | tag |
|---|---|---|---|---|
| Navon et al. *Nash-MTL.* arXiv:2202.01017 | v2, 8 Jul 2022 | https://arxiv.org/abs/2202.01017 | "Nash (1953) showed that for such payoff set U, the two-player bargaining problem has a unique solution that satisfies the following properties or axioms: Pareto optimality, symmetry, independence of irrelevant alternatives, and invariant to affine transformations." *(math transliterated; the HTML renders "solutionthat", where a footnote marker was dropped)* "Symmetry: The solution should be invariant to permuting the order of the players." "We argue that in the MTL setting, it is natural to require axioms 2.1-2.3. Axiom 2.4, in our mind, is the only non-natural assumption used by the Nash bargaining solution in the context of MTL." | [F] |
| Shamsian A, Navon A, Glazer N, Kawaguchi K, Chechik G, Fetaya E. *Auxiliary Learning as an Asymmetric Bargaining Game* (AuxiNash). ICML 2023. arXiv:2301.13501 | v2, 5 Jun 2023 (v1 31 Jan 2023) | https://arxiv.org/abs/2301.13501 | "The symmetry assumption, however, implies that each player is interchangeable which is not the case for auxiliary learning. Naturally, our main concern is the main task and the auxiliaries are there to support it, not compete with it." "The symmetric case is a special case of GNBS with uniform preferences p_i = 1/K" *(math transliterated)*. Claim 4.1 gives the solution "at any non-Pareto stationary point θ" as Σ α_i g_i with "G^⊤Gα = p/α" *(math transliterated)*. "One simple solution is to treat the preferences p_i as hyperparameters and set them via grid search." | [F] |
| Gupta et al. *DiBS.* arXiv:2505.14817 | v2, 16 Oct 2025 | https://arxiv.org/abs/2505.14817 | "we show that the bargaining solutions found by our algorithm also satisfy the axioms of symmetry and (under slightly stronger conditions) independence of irrelevant alternatives". The rule weights each normalised gradient by the agent's distance to its own preferred state: "DiBS gives more importance to those agents who are further away from their preferred states". "fixed points of DiBS exist, all its fixed points are Pareto stationary points". "unlike popular approaches such as the Nash and Kalai Smorodinsky bargaining solutions, our approach is invariant to monotonic nonaffine transformations" | [F] |
| Murthy et al. *DiBS-MTL.* arXiv:2509.23948 | v2, 2 Feb 2026 | https://arxiv.org/abs/2509.23948 | "In contrast, even if the iteratations are started at (0, 0.9), DiBS will return the balanced point (0,0) as a solution." *(math transliterated)* "the NBS is invariant to only affine agent (or task) loss transformations, and can change if the agent (or task) losses undergo monotonic nonaffine transformations." | [F] |
| Liu et al. *FAMO.* arXiv:2306.03792 | v3, 30 Oct 2023 | https://arxiv.org/abs/2306.03792 | "At each step, decrease all task losses at an equal rate as much as possible". The stationary points are the minima of the sum of log losses (Q2 row). "FAMO performs similarly to NashMTL and achieves a balanced loss decrease even when the two task losses are improperly scaled." | [F] |
| Ban, Ji. *FairGrad.* arXiv:2402.15638 | v2, 2 Jul 2024 | https://arxiv.org/abs/2402.15638 | "Nash-MTL (Navon et al., 2022) aims to achieve proportional fairness among tasks by formulating the problem as a bargaining game, attaining a balanced solution that is not dominated by any single large gradient." | [F] |
| Kendall et al. (uncertainty weighting). arXiv:1705.07115 | v3, 24 Apr 2018 | https://arxiv.org/abs/1705.07115 | "This construction can be trivially extended to arbitrary combinations of discrete and continuous loss functions, allowing us to learn the relative weights of each loss in a principled and well-founded way." | [F] |

**Counts.** 35 sources: 26 [F], 8 [A], 1 [code]. There is 1 [S] rendering: the IMTL "angle bisector" sentence, plus the
AAAI venue of ParetoCL. There are no [title]-only items. Every arXiv id's title was checked on its abstract page on the day.

## Bearing on Ω = 1 (inference, labelled as such)

Everything in this section is the dossier author's reading. It is not a ledger row and adds no number.

**1. The continuum of equilibria is already known for this family.** The repository's result (§4.1, §4.2) is this: with
exact gradients, the rule at Ω = 1 is stationary at every point of the Pareto curve and stops wherever it first meets it.
That result is already in the literature, both in general and for this exact update.
- *The general statement.* MGDA stops at any Pareto-stationary point. Désidéri's step (i) is "If ω = 0 ..., stop", and Pareto
  MTL gives "d_t = 0" at a Pareto-critical point. CAGrad reports that "MGDA and PCGrad converge to different
  Pareto-stationary points depending on θ_init". Aligned-MTL says Pareto-stationary approaches "terminate once the Pareto front is first reached"
  (verbatim from the fetched text; corrected from a paraphrase at commit time) and that "the final result strongly depends on an initialization point". Nash-MTL's own proof says the
  algorithm "halts" at a Pareto-stationary point.
- *The exact update.* The rule at Ω = 1 with instantaneous norms is g_p + (‖g_p‖/‖g_q‖)g_q = ‖g_p‖(u_p + u_q), where
  u_p and u_q are the unit gradients. This is the plain sum of normalised gradients scaled by ‖g_p‖.
  - Gupta et al. (DiBS, NeurIPS 2025, Example 2) show, on x² and (x−1)², that this sum "converge[s] at x = x_0" from any
    start. That is the repository's one-dimensional knife edge at Ω = 1 (§4.1), published.
  - Murthy et al. (DiBS-MTL, Appendix C) show the same in two dimensions for IMTL-G: "any point of the form (0, y) ... is a
    valid solution".
- *What is not found.* The sources read do not state that Ω ≠ 1 removes every interior equilibrium and slides the learner to
  an end of the front. Nor do they state the smoothing-lag dependence of §4.5. Not finding them is not evidence that they
  are unpublished. In the MOO vocabulary, an asymmetric weighting of unit vectors, u_p + Ω u_q, has no interior
  Pareto-stationary fixed points. This is a one-line consequence of the definition of Pareto stationarity, so it is
  unlikely to count as a new result.

**2. The published methods mathematically closest to the rule.** With two terms, several published methods point in the
same direction as the rule at Ω = 1: the bisector u_p + u_q. They differ from it, and from each other, only in the scalar
step length.
- Nash-MTL states that its two-task solution "is equivalent to independently normalizing each gradient and summing with
  equal weights".
- IMTL-G gives the same direction. Its weights sum to one and equalise the projections onto the unit gradients. By algebra
  this forces equal-length components, so the direction is u_p + u_q and the length is ‖g_p‖‖g_q‖/(‖g_p‖+‖g_q‖) (see the
  LibMTL code).
- MGDA gives it with the "standard normalization" of Désidéri's Remark 3, which is the `l2` option in LibMTL. With two unit
  vectors the min-norm weight is 1/2.
- DB-MTL is the closest in construction. It keeps an EMA of each task gradient (β), normalises each to unit length and
  scales the sum by the largest EMA norm. The rule also uses an EMA (s = 0.9), but only inside the ratio, and it scales by
  the present term's norm instead of the maximum.
- In continual learning, MEGA-II (2019/2020) is the closest. At equal current and memory losses, the maximiser of its eq.
  (8) is the bisector (∂/∂β[cos β + cos(θ̃ − β)] = 0 gives β = θ̃/2). Its length is fixed at exactly ‖∇ℓ_t‖, which is a
  tighter version of the rule's step bound ‖update‖ ≤ (1 + Ω)‖g_p‖ (§4.4). In one limit MEGA-II also writes the weight
  α₂ = ‖∇ℓ_t‖/‖∇ℓ_ref‖.
- Taken with the VQGAN adaptive weight already recorded (`continual_learning_2026-09-23.md`), the rule at Ω = 1 is best
  described as follows: *the two-task Nash-MTL / IMTL-G / normalised-MGDA direction, with the present gradient's length as
  the step scale*.
- Its one distinctive scale property is asymmetry. It is invariant to rescaling the past term and linear in rescaling the
  present term. Quinton and Rey argue for the opposite design, "linear under scaling" in every term.
- Ω ≠ 1 has a published counterpart in AuxiNash's asymmetric preference p. Their Claim 4.1 has a simple case: with
  orthogonal gradients, G^⊤Gα = p/α gives α_i = √p_i/‖g_i‖, so Ω plays the role of √(p_q/p_p). This holds only at
  orthogonality.
- The two differ in one respect. GNBS keeps the disagreement point, so it still halts at every Pareto-stationary point for
  any p. The rule at Ω ≠ 1 does not halt, because it solves no bargaining problem.

**3. Principles that select a Pareto point, and what CRR could claim.**
- **Symmetry and equal weighting.** The only principle in the literature that yields *equal* weighting is the symmetry
  axiom of Nash bargaining. Nash-MTL requires it, and DiBS satisfies it. That is the nearest published analogue of
  "equanimity".
- **Symmetry does not choose a point.** Nash-MTL and IMTL-G are symmetric and still stop anywhere on the front (Aligned-MTL;
  DiBS-MTL Appendix C). The axiom fixes the step direction, not the endpoint.
- **Principles that do choose a point:**
  - DiBS weights each unit gradient by the distance to that agent's own optimum. It returns the balanced point in the
    symmetric example from any start. In continual learning the past optimum θ* is the stored anchor, but the present
    optimum is unknown during training.
  - FAMO with decay γ > 0 has as stationary points the minima of Σ log ℓ_i, which is the scale-invariant (SI) objective.
  - PMF-CL chooses preferences by sample counts, α_t = n_t/Σn_k, and proves that this recovers global ERM. This is the
    repository's Bayes weight w_B = n_q/n_p (§4.3), published for continual learning in May 2026.
  - Kendall et al. choose weights by homoscedastic noise, which is maximum likelihood.
  - Pareto MTL, EPO, ParetoCL, IBCL, Aligned-MTL and GNBS use an explicit preference.
- **What CRR could claim.** It could claim the symmetry axiom, but that axiom does not by itself choose a trade-off.
  AuxiNash's objection also applies directly to continual learning: symmetry "implies that each player is interchangeable
  which is not the case for auxiliary learning". The present task and an accumulating past are not interchangeable in
  general, and PMF-CL's count-weighting encodes exactly that asymmetry.
- **Scalarisation.** Xin et al. show two things. In the convex setting, "no algorithm can outperform properly chosen
  scalarization". Specialised optimisers "simply yield ... trade-off points on the scalarization Pareto front", and a coarse
  grid misleads. This is the published form of the repository's finding (`ADAM_AND_PRIOR_ART.md` B5, where a 10-point grid
  had hidden the finely tuned constant).
- **Adam.** Elich et al.'s partial loss-scale invariance of Adam is the published form of `ADAM_AND_PRIOR_ART.md` A1–A3.
- **Noise.** PCGrad's remark that SGD noise makes exact antiparallel gradients unlikely is the published counterpart of the
  plateau under noise (§4.5). FairGrad records a non-convergence issue of MGDA, CAGrad and PCGrad in the stochastic setting.

**4. What a test would have to show for Ω = 1 to be more than a Pareto-stationary stopping rule.**
- **(a) The rule ties its published equivalents or it does not.** At equal compute, register as arms the two-term
  Nash-MTL/normalised sum, IMTL-G, MGDA with l2 normalisation, DB-MTL (EMA plus max-norm scale), MEGA-II and the VQGAN
  weight. If Ω = 1 ties them, the ledger wording should say it *reduces to normalised-gradient summation*, as EQX said it
  reduces to a constant under replay (R7).
- **(b) Say which Pareto point, and why.** Pre-register a prediction of *which* point the rule reaches, independent of
  start, step size and smoothing lag.
  - A ready-made must-fail surrogate exists: the symmetric pair x² + (y∓1)² (DiBS-MTL Appendix C) or x² and (x−1)²
    (DiBS Example 2).
  - Any rule claiming a selection principle must return the symmetric point from every start. The exact rule at Ω = 1 does
    not; its endpoint is the start.
  - A positive control is DiBS, which does return that point.
- **(c) Beat finely tuned scalarisation.** Beat a finely tuned scalarisation and the count-weighted (Bayes / PMF-CL)
  scalarisation on unseen carriers. Per Xin et al., this cannot happen on a convex problem trained to convergence, so the
  surrogate gate must include a convex case where Ω = 1 must fail.
- **(d) Survive Adam.** Survive the optimiser most models use, where a fixed weight is already partly scale-invariant (Elich
  et al.; A1–A3).
- **(e) Test scale robustness against methods that also claim it.** Nash-MTL, IMTL-G, FAMO/SI, DiBS and Adam all claim
  scale robustness. Only an advantage over them, not over a fixed λ under SGD, would be specific to the rule.

The literature supports this reading of the rule: a scale-free normalised-gradient step that stops wherever it meets the
front. As such it is already published (IMTL-G, Nash-MTL at K = 2, normalised MGDA, DB-MTL, MEGA-II). What CRR would need
to add is a principle that picks the endpoint, and the symmetry it appeals to does not pick one.
