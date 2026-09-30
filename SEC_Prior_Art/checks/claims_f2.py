"""Claims for SEC_Prior_Art/DECLARATION.md, family F2 (calibrating curvature; positions S2 and S3 primarily, with the S1, S4,
S5 and S6 statements met on the way), transcribed from the dossier docs/citations/spa1_f2_2026-09-30.md (fetched 2026-09-30;
extracted texts held outside the repository under /tmp/claude-0/spa1_src/, named in `raw_file` relative to that root). Every
quote is copied from a dossier blockquote.

'reading' is decided by the sweep agent from the quote, for the investigator's review ('reading_by'). Reading policy (RQM's,
unchanged), fixed before the readings were written and applied to every position:
  states       the source asserts (or reports as its own result) every predicate of the position, for at least one of the
               objects the position names, within the position's scope;
  close        the source asserts part of the position, or the position in a narrower or different scope;
  bears        relevant evidence or a bound that neither asserts nor negates the position;
  contradicts  the source asserts or reports the negation of the position within its scope.
Position-specific readings (fixed before the readings were written):
  S2  'states' needs all of: (i) a Fisher, empirical Fisher, GGN or Laplace precision (or a factored approximation of one) is
      MULTIPLIED by a factor; (ii) the factor is fitted to the loss's observed curvature (the gradient's or the loss's actual
      change: a secant, finite difference, line search or Hessian-vector product) so that the rescaled matrix matches it.
      A secant or HVP scale applied to a matrix that is not a Fisher/precision (an identity, an optimiser's own estimate), a
      Fisher rescaled against something other than the loss's observed curvature (its own norm, the exact Fisher's trace),
      a Fisher corrected additively rather than rescaled, or a factor that is the observed curvature itself rather than
      its ratio to the Fisher's claim, is 'close'. A scale on the precision chosen by validation is 'bears'.
  S3  'states' needs a curvature scale (or curvature estimate) fitted along the optimisation path actually travelled
      (quasi-Newton, secant, or a loss-change-over-displacement fit), used to set a continual-learning penalty or an online
      Laplace posterior. The same curvature used outside continual learning (optimisers, merging, a one-shot Laplace or
      variational posterior, model selection), or curvature sampled around the optimum rather than along the path, is
      'close'. Evidence that a path-based estimate does not measure what it claims is 'bears'.
  S1, S4, S5, S6  read as in the declaration; these are the F1/F3 positions, graded here only where an F2 source states them.
"""

RB = "sweep agent; for the investigator's review"

CLAIMS = [
    # ------------------------------------------------------------------ S2: rescaling a curvature by observed curvature
    {'id': 'f2:0', 'tag': 'S2', 'reading': 'close', 'reading_by': RB,
     'source': 'Martens, Grosse, "Optimizing Neural Networks with Kronecker-factored Approximate Curvature" (K-FAC; '
               'arXiv:1503.05671; ICML 2015, venue not verified on the day)',
     'version': 'v7, 8 Jun 2020', 'url': 'https://arxiv.org/abs/1503.05671',
     'quote': ['Given an update proposal ∆produced by multiplying the negative gradient −∇h by our approximate Fisher inverse '
               '(subject to the Tikhonov technique described in the previous subsection), the second stage of our proposed '
               'damping scheme re-scales ∆according to the quadratic model M as computed with the exact F, to produce a '
               'final update δ = α∆.',
               'Intuitively, this second stage of our damping scheme effectively compensates for the intrinsic inaccuracy of '
               'the approximate quadratic model (based on our approximate Fisher) used to generate the initial update '
               'proposal ∆, by essentially falling back on a more accurate quadratic model based on the exact Fisher.',
               'Intuitively, this rule tries to make λ as small as possible (and hence the implicit trust-region as large as '
               'possible) while maintaining the property that the quadratic model M(δ) remains a good local approximation to '
               'h (in the sense that it accurately predicts the value of h(θ + δ) for the δ which gets chosen at each '
               'iteration).'],
     'raw_file': 'f2/src/pdf_1503.05671v7.txt',
     'agent_note': 'Close: the approximate-Fisher step is re-scaled by one scalar computed from the exact Fisher along the '
                   'step direction, and the damping is adapted by the reduction ratio (actual loss change over the change '
                   'the quadratic model predicts). Two calibrations of an approximate curvature by a one-dimensional check, '
                   'but in an optimiser: the scalar multiplies the step, not a stored precision, and the first check is '
                   'against the exact Fisher, not the loss\'s secant.'},
    {'id': 'f2:1', 'tag': 'S2', 'reading': 'close', 'reading_by': RB,
     'source': 'Clarke, Hernández-Lobato, "Studying K-FAC Heuristics by Viewing Adam through a Second-Order Lens" (AdamQLR; '
               'arXiv:2310.14963; ICML 2024)',
     'version': 'v3, 13 Jun 2024', 'url': 'https://arxiv.org/abs/2310.14963',
     'quote': ['After choosing an update direction dt, a learning rate α is selected according to the second-order model M.',
               'finding an untuned AdamQLR setting can achieve comparable performance vs runtime to tuned benchmarks.'],
     'raw_file': 'f2/src/pdf_2310.14963v3.txt',
     'agent_note': 'Close: the scale of a diagonal (Adam) preconditioned step is set by the curvature along the step '
                   'direction (a GGN/Fisher-vector product in a quadratic model), and the untuned setting is reported '
                   'comparable to tuned baselines. An optimiser\'s learning rate, not a continual-learning precision.'},
    {'id': 'f2:2', 'tag': 'S2', 'reading': 'close', 'reading_by': RB,
     'source': 'Bioli et al., "Self-Scaled Broyden Family of Quasi-Newton Methods in JAX" (arXiv:2603.10599; technical '
               'note implementing the Oren-Luenberger self-scaled family)',
     'version': 'v1, 11 Mar 2026', 'url': 'https://arxiv.org/abs/2603.10599',
     'quote': ['The inverse Hessian approximation is then updated using the step sk = xk+1 −xk and the gradient difference yk =',
               'bk = s⊤ k Bksk y⊤ k sk',
               'The parameter τk controls the Self-Scaled variant (τk = 1 means no scaling) and is computed as'],
     'raw_file': 'f2/src/pdf_2603.10599v1.txt',
     'agent_note': 'Close (the mechanism, in optimisation): self-scaled quasi-Newton methods multiply the current curvature '
                   'approximation by a factor built from b_k, the ratio of the curvature the approximation claims along '
                   'the step (s^T B s) to the secant curvature the gradients showed (y^T s). SEC\'s s_j = c_j / rho_j is '
                   'this ratio with B = the task Fisher and s, y the mean-parameter and mean-gradient changes. The matrix '
                   'rescaled here is a quasi-Newton estimate, not a Fisher or a Laplace precision. Foundational sources '
                   '(Oren and Luenberger 1974; Nocedal and Wright 2006) were not fetched.'},
    {'id': 'f2:3', 'tag': 'S2', 'reading': 'close', 'reading_by': RB,
     'source': 'Tan, Ma, Dai, Qian, "Barzilai-Borwein Step Size for Stochastic Gradient Descent" (SGD-BB; arXiv:1605.04131; '
               'NeurIPS 2016, venue not verified on the day)',
     'version': 'v2, 23 May 2016', 'url': 'https://arxiv.org/abs/1605.04131',
     'quote': ['Instead, one can find ηt such that the residual of the secant equation is minimized',
               'SGD-BB takes the average of the stochastic gradients in one epoch as an estimation of the full gradient.',
               'the performance of SGD-BB and SVRG-BB is comparable to and sometimes even better than SGD and SVRG with '
               'best-tuned step sizes'],
     'raw_file': 'f2/src/pdf_1605.04131v2.txt',
     'agent_note': 'Close (the secant half of SEC): a scalar secant curvature of the loss, from gradient averages over an '
                   'epoch (SEC averages over the first and last 10 % of a task), replaces a tuned step size and matches '
                   'best-tuned SGD. No Fisher is rescaled; the curvature sets a step size.'},
    {'id': 'f2:4', 'tag': 'S2', 'reading': 'close', 'reading_by': RB,
     'source': 'Ma, "Apollo: An Adaptive Parameter-wise Diagonal Quasi-Newton Method for Nonconvex Stochastic Optimization" '
               '(arXiv:2009.13586)',
     'version': 'v6, 20 Aug 2021', 'url': 'https://arxiv.org/abs/2009.13586',
     'quote': ['It only requires first-order gradients and updates the approximation of the Hessian diagonally so that it '
               'satisfies a parameter-wise version of the weak secant condition (Wolfe, 1959).',
               'leading to the reasonable assumption of the weak secant condition (6).'],
     'raw_file': 'f2/src/pdf_2009.13586v6.txt',
     'agent_note': 'Close: a diagonal curvature estimate is corrected along the path so that its curvature along each step '
                   'equals the secant (the weak secant condition s^T B s = s^T y). SEC\'s rescaled Fisher satisfies the '
                   'same weak secant condition along the task\'s mean displacement; here the correction is a minimal '
                   'additive change to an optimiser\'s own diagonal, not a scalar on a Fisher, and not for continual '
                   'learning.'},
    {'id': 'f2:5', 'tag': 'S2', 'reading': 'close', 'reading_by': RB,
     'source': 'Gao, Liu, Huang, Wang, Wang, Xu, Yu, "A Trace-restricted Kronecker-Factored Approximation to Natural '
               'Gradient" (TKFAC; arXiv:2011.10741; venue not verified on the day)',
     'version': 'v1, 21 Nov 2020', 'url': 'https://arxiv.org/abs/2011.10741',
     'quote': ['which can hold the certain trace relationship between the exact and the approximate FIM.',
               'In TKFAC, we decompose each block of the approximate FIM as a Kronecker product of two smaller matrices and '
               'scaled by a coefficient related to trace.'],
     'raw_file': 'f2/src/pdf_2011.10741v1.txt',
     'agent_note': 'Close: a Fisher approximation is multiplied by a scalar fitted so that its trace matches the exact '
                   'Fisher\'s. The factor calibrates against the exact Fisher, not against the loss\'s observed curvature, '
                   'and is used in an optimiser.'},
    {'id': 'f2:6', 'tag': 'S2', 'reading': 'close', 'reading_by': RB,
     'source': 'Vander Eeckt, Van hamme, "Continual Learning With Quasi-Newton Methods" (CSQN; arXiv:2503.19939; IEEE Access '
               '13, 2025)',
     'version': 'v1, 25 Mar 2025', 'url': 'https://arxiv.org/abs/2503.19939',
     'quote': ['Furthermore, to enhance our method and make it a direct extension of EWC, we use EWC’s Hessian estimate, '
               'namely the diagonal of the FIM, as the initial Hessian approximation.',
               'Using SQN, we then improve this Hessian approximation, which is no longer restricted to being diagonal.',
               'Moreover, note that y is computed using ∇2f (xk)s instead of y = ∇f k −∇f (˜xi).'],
     'raw_file': 'f2/src/pdf_2503.19939v1.txt',
     'agent_note': 'Close: in continual learning, the EWC diagonal Fisher is the initial matrix of a BFGS/SR1 update fitted '
                   'to Hessian-vector products of the old task\'s loss, so the penalty curvature is corrected by observed '
                   'curvature. The correction is an additive low-rank term, not a rescaling of the Fisher, and lambda is '
                   'still selected on validation sets (claim f2:21).'},
    {'id': 'f2:7', 'tag': 'S2', 'reading': 'close', 'reading_by': RB,
     'source': 'Moser, Anwar, Nauen, Muralidhara, Raue, Schuster, Frolov, Dengel, "Layers Matter: Why Continual Learning '
               'Regularization Should Be Layer-Adaptive" (arXiv:2608.15901; preprint)',
     'version': 'v1, 16 Aug 2026', 'url': 'https://arxiv.org/abs/2608.15901',
     'quote': ['Per-parameter looks more flexible than per-layer, but each layer’s diagonal Fisher is a weak summary of its '
               'actual curvature, missing the top-eigenvalue information that controls forgetting.',
               'To measure sℓon a real network, run power iteration on H(ℓ,ℓ) using Hessian-Vector Products (HVPs).',
               'We test the one-parameter family λℓ∝(sℓ/smed)β, where smed is the median of the measured sℓ: β = 0 recovers '
               'uniform EWC, β = 1 recovers the literal measured schedule above',
               'The measured-s schedule underperforms uniform on both backbones, by 4–14% absolute.',
               'Trajectory drift away from the pretraining checkpoint, where the ratios at θ⋆need not hold along the '
               'optimizer path, is a third candidate'],
     'raw_file': 'f2/src/pdf_2608.15901v1.txt',
     'agent_note': 'Close, and the call that could move S2: in continual learning the EWC Fisher penalty of each layer is '
                   'multiplied by a factor from the loss\'s Hessian measured by HVP power iteration. For states: a Fisher '
                   'penalty rescaled by an HVP-measured curvature. For close: the factor is the layer\'s top Hessian '
                   'eigenvalue relative to the median layer, not the ratio of observed curvature to the curvature the '
                   'Fisher claims, so the Fisher\'s own scale is not calibrated out; the global strength c is still swept; '
                   'the literal schedule underperformed uniform EWC; the curvature is measured at the checkpoint, not '
                   'along the path (the authors name path drift as a candidate cause).'},
    {'id': 'f2:8', 'tag': 'S2', 'reading': 'close', 'reading_by': RB,
     'source': 'Chaudhry, Dokania, Ajanthan, Torr, "Riemannian Walk for Incremental Learning: Understanding Forgetting and '
               'Intransigence" (RWalk; arXiv:1801.10112; ECCV 2018, venue not verified on the day)',
     'version': 'v3, 14 Aug 2018', 'url': 'https://arxiv.org/abs/1801.10112',
     'quote': ['the importance of the parameter θi from training iteration t1 to t2 can be computed as',
               'where ∆θi(t) = θi(t + ∆t) −θi(t) and ϵ > 0.',
               'the accumulated change in the loss caused by the change in the parameter θi from time step t to t + ∆t.',
               'This can be ensured by individually normalizing them to be in the interval [0, 1].',
               'Whereas, EWC [7] and PI [26] are highly sensitive to λ, making them relatively less reliable for IL.'],
     'raw_file': 'f2/src/pdf_1801.10112v3.txt',
     'agent_note': 'Close, the nearest continual-learning object found for S2\'s ratio: RWalk\'s path score is, per '
                   'parameter, the loss change observed along the training path divided by the loss change the Fisher '
                   'predicts for the same step (1/2 F dtheta^2): an observed-over-Fisher-claimed ratio, as in SEC\'s '
                   'c_j / rho_j. But the score is ADDED to the Fisher as a second importance, both are normalised to '
                   '[0, 1] (which discards the units SEC calibrates), and lambda is still a hyperparameter.'},
    {'id': 'f2:9', 'tag': 'S2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Ritter, Botev, Barber, "Online Structured Laplace Approximations For Overcoming Catastrophic Forgetting" '
               '(arXiv:1805.07810; NeurIPS 2018, venue not verified on the day)',
     'version': 'v1, 20 May 2018', 'url': 'https://arxiv.org/abs/1805.07810',
     'quote': ['As modifying the objective would propagate into the recursion for the precision matrix, we instead place the '
               'multiplier on the Hessian of each log likelihood and update the precision as:',
               'As it acts directly on the parameter of a probability distribution, its optimal value can inform us about the '
               'quality of our approximation: if it strongly deviates from its natural value of 1, our approximation is a '
               'poor one and over- or underestimates the uncertainty about the parameters.',
               'We decay the initial learning rate for the second task depending on the hyperparameter to prevent the '
               'objective from diverging.'],
     'raw_file': 'f2/src/pdf_1805.07810v1.txt',
     'agent_note': 'Bears: in online Laplace continual learning the tuned multiplier is placed on each task\'s curvature, '
                   'and its departure from 1 is read as the curvature approximation\'s scale error. That is the problem '
                   'SEC calibrates, but here the multiplier is chosen by validation, not fitted to observed curvature. '
                   'The learning rate is decayed with the multiplier to avoid divergence (bears on S5).'},
    {'id': 'f2:10', 'tag': 'S2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Vander Eeckt, Van hamme, "Inverse-Hessian Regularization for Continual Learning in ASR" (IHR; '
               'arXiv:2601.14751; ICASSP 2026)',
     'version': 'v1, 21 Jan 2026', 'url': 'https://arxiv.org/abs/2601.14751',
     'quote': ['The scalar factor α rescales the adjusted update to have a comparable norm to the original update'],
     'raw_file': 'f2/src/pdf_2601.14751v1.txt',
     'agent_note': 'Bears: the scale of a K-FAC inverse-Hessian correction in continual learning is removed by norm '
                   'matching (with a tuned tau), a different route around the curvature\'s unknown scale; nothing is '
                   'fitted to observed curvature.'},
    # ------------------------------------------------------------------ S3: curvature fitted along the path, used in CL
    {'id': 'f2:11', 'tag': 'S3', 'reading': 'states', 'reading_by': RB,
     'source': 'Zenke, Poole, Ganguli, "Continual Learning Through Synaptic Intelligence" (SI; arXiv:1703.04200; ICML 2017)',
     'version': 'v3, 12 Jun 2017', 'url': 'https://arxiv.org/abs/1703.04200',
     'quote': ['The quadratic surrogate loss (green) is chosen to precisely match 3 aspects of the descent dynamics on the '
               'original loss function: the total drop in the loss function L(θ(0)) −L(θ(T)), the total net motion in '
               'parameter space θ(0) −θ(T), and achieving a minimum at the endpoint θ(T).',
               'Note that the term in the denominator (∆ν k)2 ensures that the regularization term carries the same units '
               'as the loss L.',
               'If the path integral (Eq. 3) is evaluated precisely, c = 1 would correspond to an equal weighting of old and '
               'new memories. However, due to noise in the evaluation of the path integral (Eq. 3), c typically has to be '
               'chosen smaller than one to compensate.',
               'here we used ξ = 0.1 and the value for c = 0.1 was determined via a coarse grid search on a heldout '
               'validation set.'],
     'raw_file': 'f2/src/pdf_1703.04200v3.txt',
     'agent_note': 'States (judgement call): SI fits, per parameter, the curvature of a quadratic surrogate to the loss drop '
                   'observed along the path actually travelled during the task over the squared net displacement (a '
                   'secant-style fit in the loss\'s own units), and uses it as the continual-learning penalty, with c = 1 '
                   'as the principled strength. It is not a rescaling of a Fisher (S2), and c was still tuned (0.1). '
                   'Benzing (claim f2:12) shows that as implemented the estimate is dominated by gradient-noise bias.'},
    {'id': 'f2:12', 'tag': 'S3', 'reading': 'bears', 'reading_by': RB,
     'source': 'Benzing, "Unifying Regularisation Methods for Continual Learning" (arXiv:2006.06357; AISTATS 2022 as '
               '"Unifying Importance Based Regularisation Methods for Continual Learning")',
     'version': 'v2, 3 Feb 2021', 'url': 'https://arxiv.org/abs/2006.06357',
     'quote': ['we show that for SI the relation to the Fisher – and in fact its performance – is due to a previously unknown '
               'bias.',
               'Removing the bias reduces performance of SI (SIU is worse), whereas isolating the bias does not affect or '
               'slightly improve performance.',
               'This demonstrates that SI relies on its bias, and not on the path integral, for its continual learning '
               'performance.'],
     'raw_file': 'f2/src/pdf_2006.06357v2.txt',
     'agent_note': 'Bears: the one published continual-learning importance fitted along the path (SI) works through a '
                   'gradient-noise bias that makes it approximately the square root of the Fisher, not through the path '
                   'integral; the unbiased path estimate performed worse. A caution for any path-fitted curvature, and a '
                   'difference from SEC, whose secant uses mean gradients over windows.'},
    {'id': 'f2:13', 'tag': 'S3', 'reading': 'close', 'reading_by': RB,
     'source': 'Krause, Borst, van Rij, "Structured Secant Methods to Select Smoothing Parameters for General Smooth Models" '
               '(qEFS; arXiv:2606.26804; preprint)',
     'version': 'v2, 20 Aug 2026', 'url': 'https://arxiv.org/abs/2606.26804',
     'quote': ['Estimates for these weights (i.e., smoothing parameters) can be obtained by optimizing the '
               'Laplace-approximate Bayesian marginal likelihood.',
               'Our qEFS method relies on structured limited-memory secant approximations to the Hessian of the '
               'log-likelihood and is principally first-order.',
               'We can then either retain the last Nu pairs of update vectors (vi, si) of the quasi-Newton routine or sample '
               'Nu steps (or rather perturbations) si'],
     'raw_file': 'f2/src/pdf_2606.26804v2.txt',
     'agent_note': 'Close: the curvature of a Laplace approximation is built from secant pairs retained from the '
                   'optimiser\'s own path and is used to set quadratic-penalty weights by marginal likelihood, without '
                   'tuning. Every ingredient of S3 except the scope: additive models (GAMs), not continual learning or an '
                   'online Laplace posterior over tasks. It builds the Hessian from secants rather than rescaling a '
                   'Fisher.'},
    {'id': 'f2:14', 'tag': 'S3', 'reading': 'close', 'reading_by': RB,
     'source': 'Zhang, Carpenter, Gelman, Vehtari, "Pathfinder: Parallel quasi-Newton variational inference" '
               '(arXiv:2108.03782; venue not verified on the day)',
     'version': 'v4, 16 May 2022', 'url': 'https://arxiv.org/abs/2108.03782',
     'quote': ['Pathfinder locates normal approximations to the target density along a quasi-Newton optimization path, with '
               'local covariance estimated using the inverse Hessian estimates produced by the optimizer.',
               'Pathfinder reconstructs the factors of the inverse Hessian approximations as needed using the optimization '
               'trajectory, as shown in Algorithm 3.'],
     'raw_file': 'f2/src/pdf_2108.03782v4.txt',
     'agent_note': 'Close: Gaussian (Laplace-type) posterior covariances from L-BFGS secant pairs along the optimisation '
                   'path; posterior inference, not a continual-learning penalty.'},
    {'id': 'f2:15', 'tag': 'S3', 'reading': 'close', 'reading_by': RB,
     'source': 'Perone, Silveira, Paula, "L2M: Practical posterior Laplace approximation with optimization-driven second '
               'moment estimation" (arXiv:2107.04695; ICML 2021 UDL workshop)',
     'version': 'v1, 9 Jul 2021', 'url': 'https://arxiv.org/abs/2107.04695',
     'quote': ['we show that, under some regularity conditions, the Laplace approximation can be easily constructed using the '
               'gradient second moment.',
               'without introducing any new hyperparameter.'],
     'raw_file': 'f2/src/pdf_2107.04695v1.txt',
     'agent_note': 'Close: the Laplace precision is taken from the optimiser\'s moving second moment accumulated along the '
                   'path. A Fisher-type estimate (squared gradients), not a secant, and not continual learning.'},
    {'id': 'f2:16', 'tag': 'S3', 'reading': 'close', 'reading_by': RB,
     'source': 'Li, Dangel, Tam, Raffel, "Fishers for Free? Approximating the Fisher Information Matrix by Recycling the '
               'Squared Gradient Accumulator" (Squisher; arXiv:2507.18807; ICML 2025)',
     'version': 'v1, 24 Jul 2025', 'url': 'https://arxiv.org/abs/2507.18807',
     'quote': ['adaptive gradient methods like the ubiquitous Adam optimizer compute a moving average of the squared gradient '
               'over the course of training.',
               'For EWC, we found that scaling the Squisher computed on batches of size B by N provided best performance, '
               'where N is the data set size on which the original Fisher was computed.',
               'In practice, when training EWC from scratch, λFisher is unknown and must be tuned regardless',
               'not tuning the value and using the default from Fisher provides suboptimal results.'],
     'raw_file': 'f2/src/pdf_2507.18807v1.txt',
     'agent_note': 'Close: EWC run on a curvature estimate accumulated along the optimisation path (Adam\'s squared-gradient '
                   'accumulator); its scale is set by a heuristic factor N and lambda is still tuned. A squared-gradient '
                   'estimate, not a secant; it also states S1 (lambda must be tuned).'},
    {'id': 'f2:17', 'tag': 'S3', 'reading': 'bears', 'reading_by': RB,
     'source': 'Yin, Sun, Wu, "Unbiased Online Curvature Approximation for Regularized Graph Continual Learning" '
               '(arXiv:2509.12727; preprint)',
     'version': 'v1, 16 Sep 2025', 'url': 'https://arxiv.org/abs/2509.12727',
     'quote': ['we propose a new unbiased online curvature approximation of the full FIM based on the model’s current learning '
               'state.'],
     'raw_file': 'f2/src/pdf_2509.12727v1.txt',
     'agent_note': 'Bears: the continual-learning penalty\'s Fisher is re-evaluated online at the current parameters while '
                   'the new task is learned; no scale is fitted, and the regularisation strength is set as in the original '
                   'methods.'},
    # ------------------------------------------------------------------ S1 (F1's position; stated by F2 sources)
    {'id': 'f2:18', 'tag': 'S1', 'reading': 'states', 'reading_by': RB,
     'source': 'Schwarz, Luketina, Czarnecki, Grabska-Barwinska, Teh, Pascanu, Hadsell, "Progress & Compress: A scalable '
               'framework for continual learning" (online EWC; arXiv:1805.06370; ICML 2018)',
     'version': 'v2, 2 Jul 2018', 'url': 'https://arxiv.org/abs/1805.06370',
     'quote': ['We counteract this issue by normalising the Fisher information matrices Fi for each task.',
               'treating each task equally rather than through an arbitrary scale of the original Fisher matrix.',
               'Note that the regularisation strength λ is not directly comparable between P&C and both EWC variants as the '
               'scale of the loss (policy gradients or policy distillation) is different.',
               'we chose the regularisation strength λ and forgetting coefficient γ by running a grid search'],
     'raw_file': 'f2/src/pdf_1805.06370v2.txt',
     'agent_note': 'States S1 (an F1 position): in continual learning the Fisher\'s scale is called arbitrary, lambda\'s '
                   'meaning depends on the loss\'s scale, and lambda is grid-searched. For S2 the per-task normalisation is '
                   'a rescaling of the Fisher by its own norm, not by observed curvature (bears).'},
    {'id': 'f2:19', 'tag': 'S1', 'reading': 'close', 'reading_by': RB,
     'source': 'Kunstner, Balles, Hennig, "Limitations of the Empirical Fisher Approximation for Natural Gradient Descent" '
               '(arXiv:1905.12558; NeurIPS 2019, venue not verified on the day)',
     'version': 'v3, 8 Jun 2020', 'url': 'https://arxiv.org/abs/1905.12558',
     'quote': ['One particular issue is the scaling of EF-preconditioned updates.',
               'This effect has to be counteracted by adapting the step size, which requires manual tuning and makes the '
               'selected step size dependent on the starting point',
               'but can be arbitrarily wrong if the assumption is violated, even at the minimum and with large N. In (A), '
               'the model is misspecified as it under-estimates the observation noise'],
     'raw_file': 'f2/src/pdf_1905.12558v3.txt',
     'agent_note': 'Close (optimisation, not continual learning): the empirical Fisher\'s scale is wrong, even at the '
                   'minimum under misspecified observation noise, and the compensating constant must be tuned by hand. '
                   'This is the error SEC\'s rho_j measures; no calibration is proposed.'},
    {'id': 'f2:20', 'tag': 'S1', 'reading': 'close', 'reading_by': RB,
     'source': 'van de Ven, "On the Computation of the Fisher Information in Continual Learning" (arXiv:2502.11756; ICLR 2025 '
               'blogpost track)',
     'version': 'v1, 17 Feb 2025', 'url': 'https://arxiv.org/abs/2502.11756',
     'quote': ['For example, when using the BATCHED option of computing the Fisher, EWC requires a hyperparameter orders of '
               'magnitude larger than the best hyperparameter for the EXACT option.',
               'Secondly, do not simply “use the best performing hyperparameter(s) from another paper”'],
     'raw_file': 'f2/src/pdf_2502.11756v1.txt',
     'agent_note': 'Close: in continual learning, the tuned lambda moves by orders of magnitude with the way the Fisher is '
                   'computed, i.e. with the Fisher\'s scale; the remedy offered is care and tuning, not calibration.'},
    {'id': 'f2:21', 'tag': 'S1', 'reading': 'close', 'reading_by': RB,
     'source': 'Vander Eeckt, Van hamme, "Continual Learning With Quasi-Newton Methods" (CSQN; arXiv:2503.19939; IEEE Access '
               '13, 2025)',
     'version': 'v1, 25 Mar 2025', 'url': 'https://arxiv.org/abs/2503.19939',
     'quote': ['For each experiment, we selected the value of λ with the best performance on the validation sets of all tasks '
               'and then repeated the experiment five times with this value of λ.'],
     'raw_file': 'f2/src/pdf_2503.19939v1.txt',
     'agent_note': 'Close: even with a quasi-Newton-corrected Fisher, lambda is chosen per benchmark on the validation sets '
                   'of all tasks; no reason tied to the Fisher\'s scale is stated.'},
    {'id': 'f2:22', 'tag': 'S1', 'reading': 'close', 'reading_by': RB,
     'source': 'Kao, Jensen, van de Ven, Bernacchia, Hennequin, "Natural continual learning: success is a journey, not '
               '(just) a destination" (NCL; arXiv:2106.08085; NeurIPS 2021)',
     'version': 'v2, 15 Dec 2021', 'url': 'https://arxiv.org/abs/2106.08085',
     'quote': ['previous work using the online Laplace approximation has found that large values of λ are generally required '
               'for good performance',
               'We again found that weight regularization with a KFAC approximation performed poorly with λ = 1, and that '
               'this poor performance could be partially rescued by optimizing over λ (Figure 3B).'],
     'raw_file': 'f2/src/pdf_2106.08085v2.txt',
     'agent_note': 'Close: in continual learning the Bayes weight lambda = 1 on a K-FAC Laplace failed and tuning rescued it '
                   'partly; no cause in the curvature\'s scale is stated. Bears on S6 (a tuning-free weight did not match '
                   'a tuned one here).'},
    {'id': 'f2:23', 'tag': 'S1', 'reading': 'close', 'reading_by': RB,
     'source': 'Kirkpatrick et al., "Overcoming catastrophic forgetting in neural networks" (EWC; arXiv:1612.00796; PNAS '
               '2017, venue not verified on the day)',
     'version': 'v2, 25 Jan 2017', 'url': 'https://arxiv.org/abs/1612.00796',
     'quote': ['λ sets how important the old task is compared to the new one',
               'weights given by the Fisher information matrix times a scaling factor λ which was optimized by hyperparameter '
               'search.'],
     'raw_file': 'f2/src/pdf_1612.00796v2.txt',
     'agent_note': 'Close: the founding paper tunes the Fisher\'s multiplier by hyperparameter search; the Fisher\'s scale is '
                   'not named as the reason.'},
    {'id': 'f2:24', 'tag': 'S1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Martens, "New insights and perspectives on the natural gradient method" (arXiv:1412.1193; JMLR 21, 2020)',
     'version': 'v11, 19 Sep 2020', 'url': 'https://arxiv.org/abs/1412.1193',
     'quote': ['As concrete evidence for why the empirical Fisher is, at best, a questionable choice for the curvature matrix, '
               'we will consider the following example.',
               'In this example we have that ∇h = θ, ¯F = θ2, while F = 1.'],
     'raw_file': 'f2/src/pdf_1412.1193v11.txt',
     'agent_note': 'Bears: on a quadratic whose curvature is 1 the empirical Fisher equals theta^2, so its scale depends on '
                   'where it is evaluated and vanishes at the minimum; optimisation, not continual learning.'},
    # ------------------------------------------------------------------ S4 (F3's position; stated by F2 sources)
    {'id': 'f2:25', 'tag': 'S4', 'reading': 'close', 'reading_by': RB,
     'source': 'Daxberger, Kristiadi, Immer, Eschenhagen, Bauer, Hennig, "Laplace Redux -- Effortless Bayesian Deep '
               'Learning" (arXiv:2106.14806; NeurIPS 2021)',
     'version': 'v3, 14 Mar 2022', 'url': 'https://arxiv.org/abs/2106.14806',
     'quote': ['For instance, it is typically beneficial to tune the prior variance γ2 used for inference',
               'When using the LA, however, marginal likelihood maximization (a.k.a. empirical Bayes or the evidence '
               'framework [34, 50]) constitutes a more principled alternative to tune these hyperparameters, and requires '
               'no validation data.'],
     'raw_file': 'f2/src/pdf_2106.14806v3.txt',
     'agent_note': 'Close: principled, validation-free prior-precision selection for Laplace approximations of deep '
                   'networks; not a continual-learning penalty, and the curvature itself is not rescaled (it sets the '
                   'prior, the additive term).'},
    {'id': 'f2:26', 'tag': 'S4', 'reading': 'close', 'reading_by': RB,
     'source': 'Immer, Bauer, Fortuin, Rätsch, Khan, "Scalable Marginal Likelihood Estimation for Model Selection in Deep '
               'Learning" (arXiv:2104.04975; ICML 2021)',
     'version': 'v3, 15 Jun 2021', 'url': 'https://arxiv.org/abs/2104.04975',
     'quote': ['we present a scalable marginal-likelihood estimation method to select both hyperparameters and network '
               'architectures, based on the training data alone.',
               'Finally, extending this work beyond supervised learning, e.g., to bandits, Bayesian optimization, active '
               'learning, or continual learning, is an important avenue for future research.'],
     'raw_file': 'f2/src/pdf_2104.04975v3.txt',
     'agent_note': 'Close: online marginal-likelihood selection of prior precisions from the training data alone; continual '
                   'learning is named as future work, so the continual-learning use is not claimed here.'},
    {'id': 'f2:27', 'tag': 'S4', 'reading': 'close', 'reading_by': RB,
     'source': 'Huszár, "On Quadratic Penalties in Elastic Weight Consolidation" (arXiv:1712.03847; note)',
     'version': 'v1, 11 Dec 2017', 'url': 'https://arxiv.org/abs/1712.03847',
     'quote': ['where NA is the number of i. i. d. observations in DA',
               'In order to have better control over the approximation, Kirkpatrick et al. [2017] introduce a task-specific '
               'hyper-parameter λA, which replaces the sample size NA.'],
     'raw_file': 'f2/src/pdf_1712.03847v1.txt',
     'agent_note': 'Close: the Laplace derivation of EWC gives the Bayes weight on the empirical Fisher as the task\'s sample '
                   'size (SEC\'s textbook w = 1/2 on the task-size-weighted Fisher); EWC replaced it by a free lambda. The '
                   'note derives the rule but does not report using it untuned.'},
    {'id': 'f2:28', 'tag': 'S4', 'reading': 'states', 'reading_by': RB,
     'source': 'Nguyen, Li, Bui, Turner, "Variational Continual Learning" (VCL; arXiv:1710.10628; ICLR 2018)',
     'version': 'v3, 20 May 2018', 'url': 'https://arxiv.org/abs/1710.10628',
     'quote': ['First, unlike MAP, EWC and SI, it does not have free parameters that need to be tuned on a validation set.',
               'whereas VCL’s objective is hyper-parameter free.'],
     'raw_file': 'f2/src/pdf_1710.10628v3.txt',
     'agent_note': 'States S4 (judgement; F3 grades S4): a continual learner whose prior is the previous posterior by Bayes\' '
                   'rule, with no strength to tune. It is variational, not a Laplace penalty on a Fisher.'},
    {'id': 'f2:29', 'tag': 'S4', 'reading': 'states', 'reading_by': RB,
     'source': 'Lee, Hong, Joo, Kim, "Continual Learning with Extended Kronecker-factored Approximate Curvature" '
               '(arXiv:2004.07507; CVPR 2020)',
     'version': 'v1, 16 Apr 2020', 'url': 'https://arxiv.org/abs/2004.07507',
     'quote': ['Therefore, if each task is equally important, then the importance hyperparameters are set to',
               'without any validation, where T is the number of tasks the model has learned so far.',
               'we introduce adaptive scaling hyperparameters αs and αt,'],
     'raw_file': 'f2/src/pdf_2004.07507v1.txt',
     'agent_note': 'States S4 (judgement; F3 grades S4): in a K-FAC Laplace continual learner the penalty weights are set '
                   'without validation by a counting rule (lambda_s = T/(T+1)), and an adaptive scale balances the '
                   'penalty and the new-task loss during training. The adaptive scale matches loss values, not curvature '
                   '(S2 bears); learning rate and damping are still chosen on the target task.'},
    # ------------------------------------------------------------------ S5 and S6 (F3's positions; met on the way)
    {'id': 'f2:30', 'tag': 'S5', 'reading': 'states', 'reading_by': RB,
     'source': 'Kutalev, Lapina, "Stabilizing Elastic Weight Consolidation method in practical ML tasks and using weight '
               'importances for neural network pruning" (arXiv:2109.10021; preprint)',
     'version': 'v3, 29 Oct 2021', 'url': 'https://arxiv.org/abs/2109.10021',
     'quote': ['Further, if Ωi ≥ 1 αλ, then after the optimization step the weight wi will not shift towards w∗ i but will jump '
               'over it.',
               'Thus, there will be an effect known as “gradient explosion”.',
               'To solve these problems, we used a stabilization mechanism that prevents the appearance in the regularizing '
               'contribution to the weight increment of values larger than the difference of the consolidated and current '
               'weight',
               'Thus the contribution to the anti-gradient of the regularizing component will not exceed the difference of '
               'weights even at any large importance of weight.'],
     'raw_file': 'f2/src/pdf_2109.10021v3.txt',
     'agent_note': 'States S5 (F3 grades S5; passed on): the explicit-step instability of the EWC penalty at importance '
                   'above 1/(alpha lambda) (explosion above 2/(alpha lambda)) is derived, and the importance is bounded by '
                   'the step size: the penalty uses Omega/(alpha lambda Omega + 1), a soft clip at 1/(alpha lambda). SEC4\'s '
                   'clip is the hard version at kappa/(lr w), kappa = 0.5.'},
    {'id': 'f2:31', 'tag': 'S6', 'reading': 'close', 'reading_by': RB,
     'source': 'Zheng, Zhang, van de Weijer, van de Ven, Du, Zhang, Tian, "Revisiting Weight Regularization for Low-Rank '
               'Continual Learning" (EWC-LoRA; arXiv:2602.17559; ICLR 2026)',
     'version': 'v1, 19 Feb 2026', 'url': 'https://arxiv.org/abs/2602.17559',
     'quote': ['With λ = 107, EWC-LoRA consistently achieves a favorable balance between stability and plasticity, without '
               'requiring dataset-specific tuning.'],
     'raw_file': 'f2/src/pdf_2602.17559v1.txt',
     'agent_note': 'Close (F3 grades S6; passed on): one fixed EWC strength (10^7 as rendered "107" by the extractor) is used '
                   'across datasets without dataset-specific tuning; it is a chosen constant, not a principled weight.'},
]
