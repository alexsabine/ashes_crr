"""Claims for SEC_Prior_Art/DECLARATION.md, family F3 (tuning-free and stable regularisation in continual learning; positions
S4, S5 and S6 primarily, with the S1, S2 and S3 statements met on the way), transcribed from the dossier
docs/citations/spa1_f3_2026-09-30.md (fetched 2026-09-30; extracted texts held outside the repository under
/tmp/claude-0/spa1_src/, named in `raw_file` relative to that root). Every quote is copied from a dossier blockquote.

'reading' is decided by the sweep agent from the quote, for the investigator's review ('reading_by'). Reading policy (RQM's,
unchanged), fixed before the readings were written and applied to every position:
  states       the source asserts (or reports as its own result) every predicate of the position, for at least one of the
               objects the position names, within the position's scope;
  close        the source asserts part of the position, or the position in a narrower or different scope;
  bears        relevant evidence or a bound that neither asserts nor negates the position;
  contradicts  the source asserts or reports the negation of the position within its scope.
Position-specific readings (fixed before the readings were written):
  S4  'states' needs a published continual-learning method (any model class, including continual linear regression) in
      which the penalty strength or prior precision is set WITHOUT per-dataset tuning, by a stated principled rule (a Bayes
      weight, marginal likelihood / evidence, a derived optimum, or a calibration). A tuning-free weight set by a heuristic
      rule (a loss ratio, a learned uncertainty weight), a principled rule outside continual learning, a closed-form rule
      for a coefficient that is not the penalty strength (a merging coefficient), or a derived optimum that depends on
      unknowns, is 'close'. Automated tuning (Bayesian optimisation, HPO frameworks) or evidence that the principled value
      does not suffice is 'bears'.
  S5  'states' needs a regularisation-based continual-learning source that bounds or clips the penalty's curvature (the
      importance, the Fisher, lambda * F) in relation to the step size (the product lr * lambda * F against 1 or 2) to
      prevent overshoot or divergence. Bounding the STEP SIZE by the penalty curvature (a per-parameter learning rate), a
      clip at a fixed constant not tied to the step size, or a step-size-dependent decay of the learning rate chosen by
      search, is 'close'. A generic step-size bound on a regularised objective is 'bears'.
  S6  'states' needs a report that a tuning-free Laplace or EWC-type weight is not behind (matches) a tuned lambda across
      several datasets. A fixed untuned weight used across experiments without the tuned comparison, a tuned value found
      near the principled one on one benchmark, or a principled method compared only against other methods, is 'close'.
      Reports that the principled weight is not the optimum, or that tuned-in-scenario lambdas do not transfer, are 'bears'
      (under RQM's existential reading they do not negate S6).
  S1, S2, S3  read as in the declaration and as F2 fixed them (claims_f2.py): S3 'states' includes a loss-change-over-
      displacement fit along the path used to set a continual-learning penalty.
"""

RB = "sweep agent; for the investigator's review"

CLAIMS = [
    # ------------------------------------------------------------------ S5: bounding the penalty curvature by the step size
    {'id': 'f3:0', 'tag': 'S5', 'reading': 'states', 'reading_by': RB,
     'source': 'Maltoni, Lomonaco, "Continuous Learning in Single-Incremental-Task Scenarios" (AR1; arXiv:1806.08568; the '
               'abstract page lists no journal reference; a Neural Networks 2019 version is listed by ScienceDirect, not '
               'verified on the day)',
     'version': 'v3, 22 Jan 2019', 'url': 'https://arxiv.org/abs/1806.08568',
     'quote': ['It is worth noting that in option 2, the Fk values can only increase as new batches are processed, '
               'potentially leading to divergence for large λ.',
               'In the above equation if, for some k, the product η · λ · Fk is greater than 1, the weight correction toward '
               'θ∗ k is excessive and we overshoot the desired value.',
               'where clip sets the matrix values exceeding maxF to the constant maxF .',
               'Given maxF and η we can easily determine the maximum value for λ as 1/(η · maxF ).',
               'Fk values are averaged and clipped to 0.001 thus allowing to work with higher λ and better control '
               'forgetting.'],
     'raw_file': 'f3/src/pdf_1806.08568v3.txt',
     'agent_note': 'States: in EWC (single consolidated Fisher) the product eta*lambda*F_k > 1 is named as the overshoot '
                   'condition; the Fisher is clipped at maxF and lambda is bounded by 1/(eta*maxF), i.e. '
                   'eta*lambda*F <= 1 for every coordinate. SEC4 clips at kappa/(lr*w) with kappa = 0.5 (half the Euler '
                   'edge 2; AR1 uses the no-overshoot bound 1). Differences: AR1 fixes maxF (0.001) and derives the '
                   'largest lambda from it, and it also averages rather than sums the Fishers; SEC4 fixes w and lr and '
                   'derives the clip. Same inequality, opposite direction of derivation.'},
    {'id': 'f3:1', 'tag': 'S5', 'reading': 'states', 'reading_by': RB,
     'source': 'Kutalev, Lapina, "Stabilizing Elastic Weight Consolidation method in practical ML tasks and using weight '
               'importances for neural network pruning" (arXiv:2109.10021; no venue on the abstract page)',
     'version': 'v3, 29 Oct 2021', 'url': 'https://arxiv.org/abs/2109.10021',
     'quote': ['Further, if Ωi ≥ 1 αλ, then after the optimization step the weight wi will not shift towards w∗ i but will '
               'jump over it.',
               'In the case Ωi ≥ 2 αλ, the weight wi will not only jump over the value of w∗ i , but the distance between wi '
               'and w∗ i will increase by a factor of (αλΩi −1).',
               'we used a stabilization mechanism that prevents the appearance in the regularizing contribution to the '
               'weight increment of values larger than the difference of the consolidated and current weight',
               'Thus the contribution to the anti-gradient of the regularizing component will not exceed the difference of '
               'weights even at any large importance of weight.'],
     'raw_file': 'f3/src/pdf_2109.10021v3.txt',
     'agent_note': 'States: the explicit-Euler edge of the EWC penalty (overshoot at Omega >= 1/(alpha*lambda), growth at '
                   'Omega >= 2/(alpha*lambda)) is derived, and the importance is soft-bounded as Omega/(alpha*lambda*Omega '
                   '+ 1) so that the penalty step never exceeds the distance to the anchor. A smooth saturation rather '
                   'than a hard clip; lambda is still chosen by grid search in the paper.'},
    {'id': 'f3:2', 'tag': 'S5', 'reading': 'close', 'reading_by': RB,
     'source': 'Jones, Sprague, "Continual Learning Through Expandable Elastic Weight Consolidation" (Continual Learning '
               'Workshop, NeurIPS 2018, per the PDF footer; PDF on the second author\'s JMU page)',
     'version': 'PDF as served on 2026-09-30 (w3.cs.jmu.edu/spragunr/papers/CL-2018_paper_75.pdf)',
     'url': 'https://w3.cs.jmu.edu/spragunr/papers/CL-2018_paper_75.pdf',
     'quote': ['as the number of tasks increases, preserving weights via EWC eventually results in numerical instability in '
               'the training process as the weight preservation penalty grows without bound.',
               'This will tend to cause learning to diverge rather than gradually freezing those weights as the penalty for '
               'changing them increases.',
               'we found the most effective approach to be adaptively scaling the learning rate on a per-parameter basis '
               'according to the Fisher Information values.',
               'This addresses the issue of training instability by decreasing the learning rate for exactly the '
               'parameters that are subject to large gradients as a result of the EWC penalty term.'],
     'raw_file': 'f3/src/jmu_sprague_CL2018.txt',
     'agent_note': 'Close: divergence of EWC under a growing penalty is reported, and the cure bounds the per-parameter STEP '
                   'SIZE by the penalty curvature (alpha_i = alpha / max{1, rho*lambda/2*sum F}) rather than clipping the '
                   'importance; the product alpha_i*lambda*F is bounded all the same (by 2*alpha/rho).'},
    {'id': 'f3:3', 'tag': 'S5', 'reading': 'close', 'reading_by': RB,
     'source': 'Lomonaco, Maltoni, Pellegrini, "Rehearsal-Free Continual Learning over Small Non-I.I.D. Batches" (AR1*; '
               'arXiv:1907.03799; CLVision Workshop at CVPR 2020 per the abstract page)',
     'version': 'v3, 21 Apr 2020', 'url': 'https://arxiv.org/abs/1907.03799',
     'quote': ['Firstly, the value of λ must be carefully calibrated: in fact, if its value is too high the optimal value of '
               'some parameters could be overshoot, leading to divergence (see discussion in Section 2 of [21]).',
               'where maxF is the maximum value for weight importance (we clip to maxF the Fk values larger than maxF ).',
               'Basically, the learning rate is reduced to 0 (i.e., complete freezing) for weights of highest importance'],
     'raw_file': 'f3/src/pdf_1907.03799v3.txt',
     'agent_note': 'Close: the same authors restate the overshoot/divergence condition and replace the penalty by a '
                   'learning-rate modulation eta*(1 - F/maxF) with F clipped at maxF; the clip is at a fixed constant and '
                   'the penalty is removed, so it bounds the step rather than the penalty curvature.'},
    {'id': 'f3:4', 'tag': 'S5', 'reading': 'close', 'reading_by': RB,
     'source': 'Ritter, Botev, Barber, "Online Structured Laplace Approximations For Overcoming Catastrophic Forgetting" '
               '(arXiv:1805.07810; NeurIPS 2018, venue not verified on the day)',
     'version': 'v1, 20 May 2018', 'url': 'https://arxiv.org/abs/1805.07810',
     'quote': ['We decay the initial learning rate for the second task depending on the hyperparameter to prevent the '
               'objective from diverging.',
               'We set k using a coarse grid search for each value of the hyperparameter λ in order to prevent the objective '
               'from diverging towards the end of training, in particular with the Kronecker factored curvature '
               'approximation.'],
     'raw_file': 'f3/src/pdf_1805.07810v1.txt',
     'agent_note': 'Close: divergence of the online Laplace penalty at large lambda is handled by a lambda-dependent '
                   'learning-rate decay whose constant is found by grid search; the step size is tied to the penalty '
                   'strength, not the curvature clipped by the step size.'},
    {'id': 'f3:5', 'tag': 'S5', 'reading': 'bears', 'reading_by': RB,
     'source': 'Yin, Farajtabar, Li, Levine, Mott, "Optimization and Generalization of Regularization-Based Continual '
               'Learning: a Loss Approximation Viewpoint" (arXiv:2006.10974)',
     'version': 'v3, 8 Feb 2021', 'url': 'https://arxiv.org/abs/2006.10974',
     'quote': ['it is beneficial to decrease the learning rate η, since when c decreases, the upper bound on η that '
               'guarantees the decay of F (i.e., 2(1 −1/c)/µ) also decreases.'],
     'raw_file': 'f3/src/pdf_2006.10974v3.txt',
     'agent_note': 'Bears: a step-size bound (eta <= 2(1-1/c)/mu, mu the smoothness of the regularised objective) for '
                   'regularisation-based continual learning; a bound on the learning rate, not a clip of the penalty.'},
    # ------------------------------------------------------------------ S4: tuning-free penalty or prior precision in CL
    {'id': 'f3:6', 'tag': 'S4', 'reading': 'states', 'reading_by': RB,
     'source': 'Daxberger, Kristiadi, Immer, Eschenhagen, Bauer, Hennig, "Laplace Redux -- Effortless Bayesian Deep '
               'Learning" (arXiv:2106.14806; NeurIPS 2021 camera-ready per the abstract page)',
     'version': 'v3, 14 Mar 2022', 'url': 'https://arxiv.org/abs/2106.14806',
     'quote': ['we update the LAs after each task as suggested by Ritter et al. [24] and improve upon their result by tuning '
               'the prior precision through marginal likelihood optimization during training, following Immer et al. [22]',
               'we describe how this can be combined with the evidence framework to update the prior online alleviating the '
               'need for a validation set, which is unlikely to be available in real continual learning scenarios.',
               'allows us to 1) adjust the regularization suitably per task and 2) avoid setting a hyperparameter thereby '
               'alleviating the need for validation data.'],
     'raw_file': 'f3/src/pdf_2106.14806v3.txt',
     'agent_note': 'States: a continual-learning Laplace in which the previous tasks\' Hessians enter at the Bayes weight 1 '
                   '(Eq. 16 of the appendix) and the prior precision is set per task by the marginal likelihood, with no '
                   'validation-tuned hyperparameter. One benchmark (Permuted-MNIST), compared with other Bayesian methods, '
                   'not with a tuned lambda (so S6 close at most; F1 records f1:40).'},
    {'id': 'f3:7', 'tag': 'S4', 'reading': 'states', 'reading_by': RB,
     'source': 'Nguyen, Li, Bui, Turner, "Variational Continual Learning" (VCL; arXiv:1710.10628; ICLR 2018 per the '
               'abstract page)',
     'version': 'v3, 20 May 2018', 'url': 'https://arxiv.org/abs/1710.10628',
     'quote': ['First, unlike MAP, EWC and SI, it does not have free parameters that need to be tuned on a validation set. '
               'This can be especially awkward in the online setting.',
               'Experimental results showed state-of-the-art performance when compared to previous continual learning '
               'approaches, even though VCL has no free parameters in its objective function.'],
     'raw_file': 'f3/src/pdf_1710.10628v3.txt',
     'agent_note': 'States: the previous posterior enters the objective at the Bayes weight (KL weight 1) with no tuned '
                   'strength, in continual learning. A variational posterior, not a Laplace penalty; the principle is the '
                   'one S4 names (a Bayes weight).'},
    {'id': 'f3:8', 'tag': 'S4', 'reading': 'states', 'reading_by': RB,
     'source': 'Zhao, Wang, Huang, Lin, "A Statistical Theory of Regularization-Based Continual Learning" '
               '(arXiv:2406.06213; ICML 2024 per the abstract page)',
     'version': 'v1, 10 Jun 2024', 'url': 'https://arxiv.org/abs/2406.06213',
     'quote': ['Tasks with larger sample size will be allocated with larger weights in the optimal regularization matrix, '
               'which is reasonable since they contain more information about w∗.',
               'This approximation makes the generalized ℓ2-regularized estimator a practical algorithm, which can be '
               'implemented without any underlying knowledge about the true parameter.',
               'Specifically, if all tasks have the same sample size, our method recovers the online EWC proposed by Schwarz '
               'et al. (2018) with the hyperparameter γ = 1.'],
     'raw_file': 'f3/src/pdf_2406.06213v1.txt',
     'agent_note': 'States within continual LINEAR regression: the optimal generalised-l2 penalty is derived as the '
                   'sample-size-weighted sum of the old tasks\' Hessians/Fishers divided by the current task size, '
                   'computable without tuning; this is SEC4\'s base arm (the task-size-weighted Fisher at a fixed weight). '
                   'A reader who requires a neural-network continual learner for S4 would read it close.'},
    {'id': 'f3:9', 'tag': 'S4', 'reading': 'close', 'reading_by': RB,
     'source': 'Huszár, "On Quadratic Penalties in Elastic Weight Consolidation" (arXiv:1712.03847; a note)',
     'version': 'v1, 11 Dec 2017', 'url': 'https://arxiv.org/abs/1712.03847',
     'quote': ['In order to have better control over the approximation, Kirkpatrick et al. [2017] introduce a task-specific '
               'hyper-parameter λA, which replaces the sample size NA.',
               'Therefore, sample size of each task has a non-negligible effect on the quality and behaviour of the '
               'approximation.'],
     'raw_file': 'f3/src/pdf_1712.03847v1.txt',
     'agent_note': 'Close: names the Bayes value of the EWC strength (the task sample size N_A times the empirical Fisher) '
                   'and records that EWC replaced it with a tuned hyperparameter; the note does not propose or test the '
                   'untuned value.'},
    {'id': 'f3:10', 'tag': 'S4', 'reading': 'close', 'reading_by': RB,
     'source': 'Hua, Shen, Zhao, Hsu, Jin, "Hyperparameter-free Continuous Learning for Domain Classification in Natural '
               'Language Understanding" (DWC; arXiv:2201.01420; NAACL 2021 per the journal reference)',
     'version': 'v1, 5 Jan 2022', 'url': 'https://arxiv.org/abs/2201.01420',
     'quote': ['Also, a novel scheme called dynamical weight consolidation is proposed to enable hyperparameter-free learning '
               'during the retrain process.',
               'The need for hyperparameter is an inherited problem of regularization-based continual learning.',
               'Previous works search for this hyperparameter by evaluating the whole task sequence, which is supposed not '
               'to be known.',
               'In our CCFI model, λ is updated dynamically based on current values of cross entropy and consolidation loss'],
     'raw_file': 'f3/src/pdf_2201.01420v1.txt',
     'agent_note': 'Close: a tuning-free EWC strength in continual learning, but set by a heuristic loss-ratio rule '
                   '(lambda = lg(cross entropy / consolidation loss)), not a Bayes weight, evidence or calibration. It is '
                   'the loss-ratio family the record\'s Omega = 1 rule belongs to.'},
    {'id': 'f3:11', 'tag': 'S4', 'reading': 'close', 'reading_by': RB,
     'source': 'Li, Lu, Dai, Huang, Ding, Lu, "BECAME: BayEsian Continual Learning with Adaptive Model MErging" '
               '(arXiv:2504.02666; ICML 2025 per the abstract page)',
     'version': 'v2, 29 May 2025', 'url': 'https://arxiv.org/abs/2504.02666',
     'quote': ['prior methods typically rely on empirical assumptions and carefully selected hyperparameters.',
               'we reformulate the merging mechanism using Bayesian continual learning principles and derive a closed-form '
               'solution for the optimal merging coefficient based on the Laplace approximation that adapts to the diverse '
               'characteristics of tasks.'],
     'raw_file': 'f3/src/pdf_2504.02666v2.txt',
     'agent_note': 'Close: a Laplace-derived, closed-form, untuned coefficient in continual learning, but for merging two '
                   'models, not for the penalty strength.'},
    {'id': 'f3:12', 'tag': 'S4', 'reading': 'close', 'reading_by': RB,
     'source': 'Karpel, Moroshko, Levinstein, Meir, Soudry, Evron, "Optimal L2 Regularization in High-dimensional '
               'Continual Linear Regression" (arXiv:2601.13844; ALT 2026 per the abstract page)',
     'version': 'v2, 13 Apr 2026', 'url': 'https://arxiv.org/abs/2601.13844',
     'quote': ['Furthermore, we prove that the optimal fixed regularization strength scales nearly linearly with the number '
               'of tasks T, specifically as T/ ln T.'],
     'raw_file': 'f3/src/pdf_2601.13844v2.txt',
     'agent_note': 'Close: a derived optimal isotropic strength for continual linear regression; a scaling law in T, not a '
                   'per-dataset value computed without tuning, and an isotropic (not Fisher) penalty.'},
    {'id': 'f3:13', 'tag': 'S4', 'reading': 'bears', 'reading_by': RB,
     'source': 'Levinstein, Attia, Schliserman, Sherman, Koren, Soudry, Evron, "Optimal Rates in Continual Linear Regression '
               'via Increasing Regularization" (arXiv:2506.06501)',
     'version': 'v2, 24 Oct 2025', 'url': 'https://arxiv.org/abs/2506.06501',
     'quote': ['Through this lens, we identify a fixed regularization strength that yields a near-optimal rate of '
               'O(log k/k).',
               'we derive an increasing regularization strength schedule that provably achieves an optimal rate of O(1/k).'],
     'raw_file': 'f3/src/pdf_2506.06501v2.txt',
     'agent_note': 'Bears: worst-case-rate theory for the isotropic strength (and a schedule) in continual linear '
                   'regression; no data-dependent tuning-free value.'},
    {'id': 'f3:14', 'tag': 'S4', 'reading': 'close', 'reading_by': RB,
     'source': 'Immer, Bauer, Fortuin, Rätsch, Khan, "Scalable Marginal Likelihood Estimation for Model Selection in Deep '
               'Learning" (arXiv:2104.04975; ICML 2021 per the abstract page)',
     'version': 'v3, 15 Jun 2021', 'url': 'https://arxiv.org/abs/2104.04975',
     'quote': ['we present a scalable marginal-likelihood estimation method to select both hyperparameters and network '
               'architectures, based on the training data alone.',
               'Our work shows that marginal likelihoods can improve generalization and be useful when validation data is '
               'unavailable (e.g., in nonstationary settings).'],
     'raw_file': 'f3/src/pdf_2104.04975v3.txt',
     'agent_note': 'Close: the principled prior-precision rule (online marginal likelihood) without validation data, '
                   'outside continual learning; Laplace Redux (f3:6) carries it into continual learning.'},
    {'id': 'f3:15', 'tag': 'S4', 'reading': 'close', 'reading_by': RB,
     'source': 'Lin, Antorán, Hernández-Lobato, "Online Laplace Model Selection Revisited" (arXiv:2307.06093; Advances in '
               'Approximate Bayesian Inference 2023 per the abstract page)',
     'version': 'v2, 9 Jan 2024', 'url': 'https://arxiv.org/abs/2307.06093',
     'quote': ['Online variants, which optimise NN parameters jointly with hyperparameters, like weight decay strength, have '
               'seen renewed interest in the Bayesian deep learning community.',
               'Here, online model selection prevents overfitting and outperforms validation-based early stopping.'],
     'raw_file': 'f3/src/pdf_2307.06093v2.txt',
     'agent_note': 'Close: online evidence-based selection of the prior precision (weight decay) justified; not continual '
                   'learning.'},
    {'id': 'f3:16', 'tag': 'S4', 'reading': 'close', 'reading_by': RB,
     'source': 'LUNCH: "Adaptive Balancing of Continual Learning via Hyperparameter Uncertainty" (OpenReview Q2Q4SyZ2a9; '
               'ICLR 2025 Conference Withdrawn Submission; abstract from the OpenReview search API; PDF NOT REACHED, HTTP '
               '403)',
     'version': 'OpenReview record as returned by the search API on 2026-09-30',
     'url': 'https://openreview.net/forum?id=Q2Q4SyZ2a9',
     'quote': ['Inspired by adaptive weighting in multi-task learning, we propose an innovative approach named Learning '
               'UNCertain Hyperparameters (LUNCH) for adaptive balancing of task contributions in CL.',
               'we formulate each CL-relevant hyperparameter as a function of optimizable uncertainty under homoscedastic '
               'assumption'],
     'raw_file': 'f3/src/or_Q2Q4SyZ2a9_abstract.txt',
     'agent_note': 'Close: continual-learning loss weights (regularisation and replay) set without tuning by a learned '
                   'homoscedastic-uncertainty weight; a heuristic from multi-task weighting, not a Bayes/evidence rule for '
                   'the Laplace precision. Withdrawn submission; abstract only.'},
    {'id': 'f3:17', 'tag': 'S4', 'reading': 'bears', 'reading_by': RB,
     'source': 'Zenke, Poole, Ganguli, "Continual Learning Through Synaptic Intelligence" (SI; arXiv:1703.04200; ICML 2017 '
               'per the abstract page)',
     'version': 'v3, 12 Jun 2017', 'url': 'https://arxiv.org/abs/1703.04200',
     'quote': ['If the path integral (Eq. 3) is evaluated precisely, c = 1 would correspond to an equal weighting of old and '
               'new memories. However, due to noise in the evaluation of the path integral (Eq. 3), c typically has to be '
               'chosen smaller than one to compensate.'],
     'raw_file': 'f3/src/pdf_1703.04200v3.txt',
     'agent_note': 'Bears: the path-fitted penalty has a principled strength c = 1, which the authors report does not '
                   'hold in practice because of noise; F1 reads this as S4 close (f1:35).'},
    {'id': 'f3:18', 'tag': 'S4', 'reading': 'bears', 'reading_by': RB,
     'source': 'Loo, Swaroop, Turner, "Generalized Variational Continual Learning" (GVCL; arXiv:2011.12328; ICLR 2021, '
               'venue not verified on the day)',
     'version': 'v1, 24 Nov 2020', 'url': 'https://arxiv.org/abs/2011.12328',
     'quote': ['Instead, our derivation produces an implicit value of λ = 1, i.e. equal weight between tasks of equal sample '
               'count. In practice it is found that algorithms such as Online EWC perform best when λ > 1, typically 10 '
               '−1000.'],
     'raw_file': 'f3/src/pdf_2011.12328v1.txt',
     'agent_note': 'Bears (S4 and S6): the Bayes-derived strength is 1 per sample-count-weighted task, and practice finds '
                   'lambda between 10 and 1000; the gap is treated as cold-posterior tempering, i.e. still a tuned '
                   'hyperparameter.'},
    # ------------------------------------------------------------------ S6: a tuning-free weight matching a tuned lambda
    {'id': 'f3:19', 'tag': 'S6', 'reading': 'close', 'reading_by': RB,
     'source': 'Aljundi, Babiloni, Elhoseiny, Rohrbach, Tuytelaars, "Memory Aware Synapses: Learning what (not) to forget" '
               '(MAS; arXiv:1711.09601; ECCV 2018 per the abstract page)',
     'version': 'v4, 5 Oct 2018', 'url': 'https://arxiv.org/abs/1711.09601',
     'quote': ['We use a regularization parameter λ of 1; note that no tuning of λ was performed as we assume no access to '
               'previous task data.',
               'For MAS, we used λ = 1 in all object recognition experiments while for SI[39] and EWC[12] we had to vary '
               'λ.'],
     'raw_file': 'f3/src/pdf_1711.09601v4.txt',
     'agent_note': 'Close: an untuned strength (lambda = 1) used across several object-recognition sequences, but for MAS '
                   '(not a Laplace/EWC weight) and not compared with MAS at a tuned lambda.'},
    {'id': 'f3:20', 'tag': 'S6', 'reading': 'close', 'reading_by': RB,
     'source': 'Nguyen, Li, Bui, Turner, "Variational Continual Learning" (VCL; arXiv:1710.10628; ICLR 2018)',
     'version': 'v3, 20 May 2018', 'url': 'https://arxiv.org/abs/1710.10628',
     'quote': ['Diagonal LP performs slightly worse than EWC both when λ = 1 and when the values of λ are tuned.',
               'Again, unlike VCL, EWC and SI benefited from a hyper-parameter search for λ, but a value close to 1 performs '
               'well in both cases.'],
     'raw_file': 'f3/src/pdf_1710.10628v3.txt',
     'agent_note': 'Close: the Laplace (LP) at lambda = 1 is reported beside the tuned lambda on Permuted MNIST, and on Split '
                   'MNIST a value near 1 performs well; two benchmarks, and the untuned value is not shown to match the '
                   'tuned one across many datasets.'},
    {'id': 'f3:21', 'tag': 'S6', 'reading': 'bears', 'reading_by': RB,
     'source': 'Ritter, Botev, Barber, "Online Structured Laplace Approximations For Overcoming Catastrophic Forgetting" '
               '(arXiv:1805.07810)',
     'version': 'v1, 20 May 2018', 'url': 'https://arxiv.org/abs/1805.07810',
     'quote': ['if it strongly deviates from its natural value of 1, our approximation is a poor one and over- or '
               'underestimates the uncertainty about the parameters.',
               'Overestimating the uncertainty leads to a need for regularization in the form of reducing the width of the '
               'approximate posterior, as the value that optimizes the validation error is λ = 3.',
               'We note that some regularization is still necessary, suggesting that even the Kronecker factored '
               'approximation overestimates the variance in the posterior'],
     'raw_file': 'f3/src/pdf_1805.07810v1.txt',
     'agent_note': 'Bears: the Bayes weight 1 is the natural value, but the tuned optimum departs from it (3 for the '
                   'diagonal on Permuted MNIST), read as a mis-scaled curvature: the gap SEC\'s calibration targets.'},
    {'id': 'f3:22', 'tag': 'S6', 'reading': 'bears', 'reading_by': RB,
     'source': 'Cha, Cho, "Hyperparameters in Continual Learning: A Reality Check" (arXiv:2403.09066; TMLR 2025 per the '
               'abstract page)',
     'version': 'v5, 28 Oct 2025', 'url': 'https://arxiv.org/abs/2403.09066',
     'quote': ['it overestimates the CL capacity of algorithms and relies on unrealistic hyperparameter tuning, which is not '
               'feasible for real-world applications.',
               'Hyperparameters of CL algorithms are tuned in the first phase and applied in the second phase to evaluate '
               'the algorithms.'],
     'raw_file': 'f3/src/pdf_2403.09066v5.txt',
     'agent_note': 'Bears: in-scenario tuning (what SEC4\'s tuned-lambda baseline does, in-sample on the scored seeds) '
                   'overstates methods; the proposed protocol tunes on one dataset and evaluates on another, which is '
                   'SEC4-T\'s transferred-lambda comparison.'},
    {'id': 'f3:23', 'tag': 'S6', 'reading': 'bears', 'reading_by': RB,
     'source': 'Lee, Hellan, Ericsson, Crowley, Storkey, "Hyperparameter Selection in Continual Learning" '
               '(arXiv:2404.06466; preprint; the ICLR 2025 version was withdrawn per OpenReview)',
     'version': 'v2, 14 Mar 2025', 'url': 'https://arxiv.org/abs/2404.06466',
     'quote': ['However, end-of-training HPO is unrealistic as in the real world a learner can only train over the',
               'the most common hyperparameters that are tuned are the learning rate and regularisation coefficients, which '
               'are crucial to tune to get good performance'],
     'raw_file': 'f3/src/pdf_2404.06466v2.txt',
     'agent_note': 'Bears (S6 and S1): regularisation coefficients must be tuned for good performance, and the usual '
                   'end-of-training tuning is unrealistic; no tuning-free weight is proposed.'},
    {'id': 'f3:24', 'tag': 'S6', 'reading': 'bears', 'reading_by': RB,
     'source': 'van de Ven, "On the Computation of the Fisher Information in Continual Learning" (arXiv:2502.11756; ICLR '
               '2025 blogpost track per the abstract page)',
     'version': 'v1, 17 Feb 2025', 'url': 'https://arxiv.org/abs/2502.11756',
     'quote': ['when using the BATCHED option of computing the Fisher, EWC requires a hyperparameter orders of magnitude '
               'larger than the best hyperparameter for the EXACT option.',
               'do not simply “use the best performing hyperparameter(s) from another paper”'],
     'raw_file': 'f3/src/pdf_2502.11756v1.txt',
     'agent_note': 'Bears (S6; S1 states in F1 f1:1): the best lambda moves by orders of magnitude with the Fisher\'s '
                   'computation, so a lambda does not transfer across implementations; the scale problem SEC calibrates.'},
    # ------------------------------------------------------------------ S1 met on the way
    {'id': 'f3:25', 'tag': 'S1', 'reading': 'close', 'reading_by': RB,
     'source': 'Li, Dangel, Tam, Raffel, "Fishers for Free? Approximating the Fisher Information Matrix by Recycling the '
               'Squared Gradient Accumulator" (arXiv:2507.18807; ICML 2025 spotlight per the abstract page)',
     'version': 'v1, 24 Jul 2025', 'url': 'https://arxiv.org/abs/2507.18807',
     'quote': ['the squaring of the average gradient introduces a factor of N difference in scale as in Equation (12).',
               'In practice, when training EWC from scratch, λFisher is unknown and must be tuned regardless'],
     'raw_file': 'f3/src/pdf_2507.18807v1.txt',
     'agent_note': 'Close: the Fisher estimate\'s scale depends on how it is computed (a factor N), and the EWC strength is '
                   'unknown and must be tuned; F1 reads the same source close (f1:9).'},
    # ------------------------------------------------------------------ S3 / S2 met on the way
    {'id': 'f3:26', 'tag': 'S3', 'reading': 'states', 'reading_by': RB,
     'source': 'Zenke, Poole, Ganguli, "Continual Learning Through Synaptic Intelligence" (SI; arXiv:1703.04200; ICML 2017)',
     'version': 'v3, 12 Jun 2017', 'url': 'https://arxiv.org/abs/1703.04200',
     'quote': ['The quadratic surrogate loss (green) is chosen to precisely match 3 aspects of the descent dynamics on the '
               'original loss function: the total drop in the loss function L(θ(0)) −L(θ(T)), the total net motion in '
               'parameter space θ(0) −θ(T), and achieving a minimum at the endpoint θ(T).',
               'Note that this surrogate loss is different from a quadratic approximation defined by the Hessian at the '
               'minimum (purple dashed line).',
               'Again the normalization in (5), at zero damping, removes the scale of movement in parameter space (di)2, '
               'and so the normalized Q matrix becomes identical to the diagonal Hessian.'],
     'raw_file': 'f3/src/pdf_1703.04200v3.txt',
     'agent_note': 'States (as F1 f1:23 and F2 f2:11 read it): a per-coordinate curvature fitted along the path travelled '
                   '(loss drop over squared net displacement, a secant-type fit) sets the continual-learning penalty. It '
                   'REPLACES the Fisher rather than rescaling it, and the strength c is still tuned (f3:17); Benzing '
                   '(f2:12) finds the estimate dominated by gradient-noise bias.'},
    {'id': 'f3:27', 'tag': 'S2', 'reading': 'close', 'reading_by': RB,
     'source': 'Chaudhry, Dokania, Ajanthan, Torr, "Riemannian Walk for Incremental Learning: Understanding Forgetting and '
               'Intransigence" (RWalk; arXiv:1801.10112; ECCV 2018, venue not verified on the day)',
     'version': 'v3, 14 Aug 2018', 'url': 'https://arxiv.org/abs/1801.10112',
     'quote': ['we define parameter importance as the ratio of the change in the loss to its influence in '
               'DKL(pθ(t)∥pθ(t+1)).',
               'We augment Fisher with a parameter importance score which is accumulated over the entire training '
               'trajectory of ˜Lk (similar to [26]).',
               'This can be ensured by individually normalizing them to be in the interval [0, 1].',
               'Whereas, EWC [7] and PI [26] are highly sensitive to λ, making them relatively less reliable for IL.'],
     'raw_file': 'f3/src/pdf_1801.10112v3.txt',
     'agent_note': 'Close (F2 f2:8 reads it close): the score is, per step and coordinate, the observed loss change divided '
                   'by the Fisher-predicted change (1/2 F dtheta^2), accumulated along the path, i.e. an observed-over-'
                   'Fisher ratio like SEC\'s c/rho; but it is ADDED to the Fisher after both are normalised to [0, 1] '
                   '(which discards the absolute scale SEC fixes), and lambda is still tuned.'},
    {'id': 'f3:28', 'tag': 'S3', 'reading': 'close', 'reading_by': RB,
     'source': 'Chaudhry, Dokania, Ajanthan, Torr, "Riemannian Walk for Incremental Learning" (RWalk; arXiv:1801.10112)',
     'version': 'v3, 14 Aug 2018', 'url': 'https://arxiv.org/abs/1801.10112',
     'quote': ['We augment Fisher with a parameter importance score which is accumulated over the entire training '
               'trajectory of ˜Lk (similar to [26]).'],
     'raw_file': 'f3/src/pdf_1801.10112v3.txt',
     'agent_note': 'Close: a path-accumulated, Fisher-relative score sets part of the continual-learning penalty; it is a '
                   'dimensionless importance (loss change over Fisher-KL), not a curvature scale, and it is normalised.'},
    {'id': 'f3:29', 'tag': 'S2', 'reading': 'close', 'reading_by': RB,
     'source': 'Vander Eeckt, Van hamme, "Continual Learning With Quasi-Newton Methods" (CSQN; arXiv:2503.19939; IEEE Access '
               '13, 2025 per the journal reference)',
     'version': 'v1, 25 Mar 2025', 'url': 'https://arxiv.org/abs/2503.19939',
     'quote': ['we introduce Continual Learning with Sampled Quasi-Newton (CSQN), which leverages Quasi-Newton methods to '
               'compute more accurate Hessian approximations.',
               'To obtain Sk and Y k at iteration k from scratch, SQN methods sample points ˜xi ∈Rn with i = 1, .., M in '
               'the neighborhood of xk.',
               'For each experiment, we selected the value of λ with the best performance on the validation sets of all '
               'tasks'],
     'raw_file': 'f3/src/pdf_2503.19939v1.txt',
     'agent_note': 'Close (as F1 f1:18 and F2 f2:6): the diagonal Fisher is the initial estimate B0 and is CORRECTED '
                   'additively by a low-rank quasi-Newton term built from Hessian-vector products at points sampled around '
                   'the task optimum (not along the path); lambda is still chosen on validation sets of all tasks.'},
    {'id': 'f3:30', 'tag': 'S2', 'reading': 'close', 'reading_by': RB,
     'source': 'Moser, Anwar, Nauen, Muralidhara, Raue, Schuster, Frolov, Dengel, "Layers Matter: Why Continual Learning '
               'Regularization Should Be Layer-Adaptive" (arXiv:2608.15901)',
     'version': 'v1, 16 Aug 2026', 'url': 'https://arxiv.org/abs/2608.15901',
     'quote': ['Diagonal-Fisher weights cannot recover this eigenvalue.',
               'To measure sℓon a real network, run power iteration on H(ℓ,ℓ) using Hessian-Vector Products (HVPs).',
               'Among regularizers of the form in Eq. 13, the choice that matches the oracle’s penalty on this direction, '
               'up to one global constant shared across layers, is λℓ∝sℓ.'],
     'raw_file': 'f3/src/pdf_2608.15901v1.txt',
     'agent_note': 'Close (as F1 f1:17 and F2 f2:7): per-layer penalty weights proportional to an HVP-measured top Hessian '
                   'eigenvalue, applied to EWC in the BERT experiment; the factor is the curvature itself (not its ratio '
                   'to the Fisher), relative across layers, and one global constant is still swept.'},
]
