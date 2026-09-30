"""Claims for SEC_Prior_Art/DECLARATION.md (study SPA1), family F1: the scale of the Fisher in continual learning and
Bayesian online learning (positions S1 and S6 primarily; S2-S5 tagged where a source bears on them), transcribed from the
dossier docs/citations/spa1_f1_2026-09-30.md (fetched 2026-09-30; extracted texts held outside the repository under
/tmp/claude-0/spa1_src/, named in `raw_file` relative to that root). Every quote is copied from a dossier blockquote.

'reading' is decided by the sweep agent from the quote, for the investigator's review ('reading_by'). Reading policy
(RQM's, unchanged, as in SEC_Prior_Art/DECLARATION.md), applied to every position:
  states       the source asserts (or reports as its own result) every predicate of the position, for at least one of the
               objects the position names, within the position's scope;
  close        the source asserts part of the position, or the position in a narrower or different scope;
  bears        relevant evidence or a bound that neither asserts nor negates the position;
  contradicts  the source asserts or reports the negation of the position within its scope.
Position-specific readings (written by the sweep agent before the readings below were entered):
  S1  'states': a continual-learning or Bayesian-deep-learning source asserts both (i) that the EWC/Laplace penalty weight
      has to be tuned away from its Bayes value or differs between settings, and (ii) that this is due, wholly or in part, to
      the scale or approximation error of the (empirical) Fisher / Laplace precision. One of (i), (ii) in scope, or both out
      of scope, is 'close'. Evidence that asserts neither (a reported optimum that differs between settings for another
      stated reason; a Fisher-scale error outside continual learning) is 'bears'. A source asserting that one penalty weight
      serves across datasets without dataset-specific tuning, in continual learning, is 'contradicts'.
  S2  'states': a Fisher or Laplace precision is multiplied by a factor fitted to the loss's observed curvature (secant,
      finite difference, line search or Hessian-vector check). A Fisher-based importance corrected, combined or replaced
      using observed curvature, per layer or per parameter, or an observed-to-Fisher ratio computed but not used as a
      rescaling, or a scale correction of an empirical Fisher outside continual learning, is 'close'.
  S3  'states': a curvature fitted along the optimisation path (quasi-Newton or secant style: loss or gradient change over
      the parameter displacement travelled during training) sets a continual-learning penalty or an online Laplace posterior.
      Quasi-Newton curvature sampled around the endpoint rather than along the path, or a path-based ratio used as
      preconditioner damping rather than as a penalty, is 'close'.
  S4  'states': a continual-learning method sets the penalty weight or prior precision without tuning, by a principled rule
      (Bayes weight, marginal likelihood, evidence, calibration), and says so. The rule outside continual learning, or a
      principled value derived in continual learning but then not used untuned, is 'close'.
  S5  'states': an EWC-type continual learner bounds or clips the penalty curvature or importance by the step size (the
      lr x lambda x F stability edge) to prevent divergence. A step size adapted to the Fisher or to lambda to prevent
      divergence, or importance bounded by a normalisation not tied to the step size, is 'close'.
  S6  'states': a tuning-free Laplace or EWC weight is reported to match (not be behind) a tuned lambda across many datasets.
      Narrower evidence (one dataset; a lambda fixed once and reused across datasets; a tuning-free Bayesian learner that is
      not a Laplace/EWC weight) is 'close'. Tuned-versus-untuned evidence that asserts neither (a raw lambda = 1 behind a
      tuned lambda on one benchmark; results on hyperparameter-selection protocols) is 'bears'.
"""

RB = "sweep agent; for the investigator's review"

CLAIMS = [
    # ------------------------------------------------------------------ S1
    {'id': 'f1:0', 'tag': 'S1', 'reading': 'states', 'reading_by': RB,
     'source': 'Ritter, Botev, Barber, "Online Structured Laplace Approximations For Overcoming Catastrophic Forgetting" '
               '(arXiv:1805.07810; NeurIPS 2018 per the proceedings reference in arXiv:2502.11756, not verified on the day)',
     'version': 'v1, 20 May 2018', 'url': 'https://arxiv.org/abs/1805.07810',
     'quote': ['As it acts directly on the parameter of a probability distribution, its optimal value can inform us about '
               'the quality of our approximation: if it strongly deviates from its natural value of 1, our approximation is '
               'a poor one and over- or underestimates the uncertainty about the parameters.',
               'We conclude from our results that the online Laplace approximation overestimates the uncertainty in the '
               'approximate posterior about the parameters for the permuted MNIST task, in particular with a [...] diagonal '
               'approximation to the Hessian. Overestimating the uncertainty leads to a need for regularization in the form '
               'of reducing the width of the approximate posterior, as the value that optimizes the validation error is '
               'λ = 3.',
               'We use an identical network architecture to the previous section and found stronger regularization of the '
               'approximate posterior to be necessary.'],
     'raw_file': 'f1/src/pdf_1805.07810v1.txt',
     'agent_note': 'States: the multiplier on the curvature has a natural (Bayes) value of 1; its tuned optimum deviates '
                   'because the curvature approximation mis-scales the posterior (more so for the diagonal), and the '
                   'optimum differs between benchmarks (3 on permuted MNIST; stronger on disjoint MNIST).'},
    {'id': 'f1:1', 'tag': 'S1', 'reading': 'states', 'reading_by': RB,
     'source': 'van de Ven, "On the Computation of the Fisher Information in Continual Learning" (arXiv:2502.11756; ICLR 2025 '
               'blogpost track)',
     'version': 'v1, 17 Feb 2025', 'url': 'https://arxiv.org/abs/2502.11756',
     'quote': ['λ is a hyperparameter that sets the relative importance of the new task compared to the old one(s).',
               'For example, when using the BATCHED option of computing the Fisher, EWC requires a hyperparameter orders of '
               'magnitude larger than the best hyperparameter for the EXACT option.',
               'Secondly, do not simply “use the best performing hyperparameter(s) from another paper”, especially if you '
               'cannot guarantee that the details of your implementation are the same as in the other paper.'],
     'raw_file': 'f1/src/pdf_2502.11756v1.txt',
     'agent_note': 'States: the scale of the Fisher estimate (exact, sampled, empirical, batched) moves the best lambda by '
                   'orders of magnitude, so lambda must be re-tuned per implementation; it recommends against reusing lambda.'},
    {'id': 'f1:2', 'tag': 'S1', 'reading': 'states', 'reading_by': RB,
     'source': 'Kao, Jensen, van de Ven, Bernacchia, Hennequin, "Natural continual learning: success is a journey, not (just) '
               'a destination" (NCL; arXiv:2106.08085; NeurIPS 2021)',
     'version': 'v2, 15 Dec 2021', 'url': 'https://arxiv.org/abs/2106.08085',
     'quote': ['Additionally, its Bayesian interpretation in theory prescribes a unique way of weighting the contributions of '
               'previous and current tasks to the loss. However, to perform well in practice, weight regularization approaches '
               'have been found to require ad-hoc re-weighting of the prior term by several orders of magnitude (Kirkpatrick '
               'et al., 2017; Ritter et al., 2018; van de Ven and Tolias, 2018). These shortcomings could be due to an '
               'inadequacy of the approximations used to construct the posterior (Section 2.1).',
               'We confirmed this here by performing a grid search over λ, which showed that KFAC with λ ∈[100, 1000] could '
               'perform comparably to the projection-based methods'],
     'raw_file': 'f1/src/pdf_2106.08085v2.txt',
     'agent_note': 'States (hedged: "could be due to"): the Bayes weight is unique in theory, practice needs a re-weighting by '
                   'orders of magnitude, and approximation inadequacy is named as a cause. The paper also offers a second '
                   'cause (Adam preconditioning), so the attribution to the Fisher is partial.'},
    {'id': 'f1:3', 'tag': 'S1', 'reading': 'close', 'reading_by': RB,
     'source': 'Schwarz, Luketina, Czarnecki, Grabska-Barwinska, Teh, Pascanu, Hadsell, "Progress & Compress: A scalable '
               'framework for continual learning" (arXiv:1805.06370; ICML 2018)',
     'version': 'v2, 2 Jul 2018', 'url': 'https://arxiv.org/abs/1805.06370',
     'quote': ['This results in Fisher matrices of variable norm. However, the goal of the algorithm is to protect each task '
               'equally. We counteract this issue by normalising the Fisher information matrices Fi for each task.',
               'treating each task equally rather than through an arbitrary scale of the original Fisher matrix.',
               'EWC was separately tuned choosing λ from [500, 1000, 1500, 2000, 2500, 3000]. As the scale of the losses '
               'differ, we selected λ for online EWC as applied in P&C among [25, 75, 125, 175].'],
     'raw_file': 'f1/src/pdf_1805.06370v2.txt',
     'agent_note': 'Close: the Fisher scale is called arbitrary (removed by normalisation), and lambda is re-tuned per method '
                   'because loss scales differ; the two are not joined into "lambda must be tuned because the Fisher scale is '
                   'wrong". Same PDF sha256 as the SEC5 dossier (docs/citations/sec5_2026-09-29.md).'},
    {'id': 'f1:4', 'tag': 'S1', 'reading': 'close', 'reading_by': RB,
     'source': 'Kirkpatrick et al., "Overcoming catastrophic forgetting in neural networks" (EWC; arXiv:1612.00796; PNAS 2017)',
     'version': 'v2, 25 Jan 2017', 'url': 'https://arxiv.org/abs/1612.00796',
     'quote': ['λ sets how important the old task is compared to the new one',
               'weights given by the Fisher information matrix times a scaling factor λ which was optimized by hyperparameter '
               'search.'],
     'raw_file': 'f1/src/pdf_1612.00796v2.txt',
     'agent_note': 'Close: lambda is a tuned scaling factor in the founding paper, framed as task importance, not as a '
                   'correction of the Fisher scale.'},
    {'id': 'f1:5', 'tag': 'S1', 'reading': 'close', 'reading_by': RB,
     'source': 'Huszár, "On Quadratic Penalties in Elastic Weight Consolidation" (arXiv:1712.03847; published as the PNAS 2018 '
               'letter "Note on the quadratic penalties in elastic weight consolidation")',
     'version': 'v1, 11 Dec 2017', 'url': 'https://arxiv.org/abs/1712.03847',
     'quote': ['Under some regularity conditions, the Laplace approximation becomes exact in the limit of infinite data '
               '[Ghosal et al., 1995], but for finite data it has a tendency to underestimate the true entropy of the '
               'posterior.',
               'Therefore, sample size of each task has a non-negligible effect on the quality and behaviour of the '
               'approximation. In order to have better control over the approximation, Kirkpatrick et al. [2017] introduce a '
               'task-specific hyper-parameter λA, which replaces the sample size NA.'],
     'raw_file': 'f1/src/pdf_1712.03847v1.txt',
     'agent_note': 'Close: lambda replaces the Bayes weight (the task size N_A) to control the approximation\'s quality; a '
                   'reason tied to the Laplace approximation, not a statement that lambda must be re-tuned per dataset.'},
    {'id': 'f1:6', 'tag': 'S1', 'reading': 'close', 'reading_by': RB,
     'source': 'Loo, Swaroop, Turner, "Generalized Variational Continual Learning" (GVCL; arXiv:2011.12328; venue not verified '
               'on the day)',
     'version': 'v1, 24 Nov 2020', 'url': 'https://arxiv.org/abs/2011.12328',
     'quote': ['However, the correspondence does not recover a key hyperparameter λ used by these methods that up-weights the '
               'quadratic regularization term. Instead, our derivation produces an implicit value of λ = 1, i.e. equal weight '
               'between tasks of equal sample count. In practice it is found that algorithms such as Online EWC perform best '
               'when λ > 1, typically 10 −1000. In this section, we view this λ hyperparameter as a form of cold posterior '
               'regularization.'],
     'raw_file': 'f1/src/pdf_2011.12328v1.txt',
     'agent_note': 'Close: the Bayes value is lambda = 1 and practice needs 10-1000; the cause offered is cold-posterior '
                   'tempering, not the Fisher scale.'},
    {'id': 'f1:7', 'tag': 'S1', 'reading': 'close', 'reading_by': RB,
     'source': 'Liu, Chang, "Elastic Weight Consolidation Done Right for Continual Learning" (EWC-DR; arXiv:2603.18596; CVPR '
               '2026)',
     'version': 'v3, 26 Mar 2026', 'url': 'https://arxiv.org/abs/2603.18596',
     'quote': ['Detailed analysis indicates that when the network achieves high confidence in accurate predictions, EWC '
               'produces a low-magnitude Fisher Information Matrix (FIM) due to the vanishing gradients.',
               'Aavg increases steadily as λ grows from 1,000 and reaches its peak around λ = 10,000–20,000.'],
     'raw_file': 'f1/src/pdf_2603.18596v3.txt',
     'agent_note': 'Close: the Fisher is too small where the model is confident (a scale error), and lambda is still swept '
                   '(peak 1e4-2e4); the fix is logit reversal, not a scale calibration, and lambda is not tied to the error.'},
    {'id': 'f1:8', 'tag': 'S1', 'reading': 'close', 'reading_by': RB,
     'source': 'Josifovski, Auddy, Malmir, Piater, Knoll, Navarro-Guerrero, "Continual Domain Randomization" '
               '(arXiv:2403.12193; IROS 2024)',
     'version': 'v2, 27 Aug 2024', 'url': 'https://arxiv.org/abs/2403.12193',
     'quote': ['we normalize the elements of F to be in the range [0.0,1.0] after each task. This normalization decouples the '
               'regularization constant λ from the arbitrary scaling of the Fisher information of individual tasks and allows '
               'us to use of a single value of λ for all tasks.'],
     'raw_file': 'f1/src/pdf_2403.12193v2.txt',
     'agent_note': 'Close: the Fisher\'s arbitrary scale would otherwise make lambda task-dependent; stated per task within one '
                   'RL stream, not per dataset, and lambda is still chosen.'},
    {'id': 'f1:9', 'tag': 'S1', 'reading': 'close', 'reading_by': RB,
     'source': 'Li, Dangel, Tam, Raffel, "Fishers for Free? Approximating the Fisher Information Matrix by Recycling the '
               'Squared Gradient Accumulator" (arXiv:2507.18807; ICML 2025 spotlight)',
     'version': 'v1, 24 Jul 2025', 'url': 'https://arxiv.org/abs/2507.18807',
     'quote': ['Unlike in previous settings, rescaling the Squisher does change the learning behavior in this setting as it '
               'modifies the regularization strength.',
               'In practice, when training EWC from scratch, λFisher is unknown and must be tuned regardless'],
     'raw_file': 'f1/src/pdf_2507.18807v1.txt',
     'agent_note': 'Close: the Fisher estimate\'s scale sets the effective strength, and lambda "must be tuned regardless"; '
                   'no per-dataset attribution.'},
    {'id': 'f1:10', 'tag': 'S1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Kunstner, Balles, Hennig, "Limitations of the Empirical Fisher Approximation for Natural Gradient Descent" '
               '(arXiv:1905.12558; NeurIPS 2019 per the proceedings reference in arXiv:2502.11756)',
     'version': 'v3, 8 Jun 2020', 'url': 'https://arxiv.org/abs/1905.12558',
     'quote': ['The EF is a good approximation of the Fisher at the minimum if this assumption is fulfilled (left panel), but '
               'can be arbitrarily wrong if the assumption is violated, even at the minimum and with large N.',
               'In such settings, the individual gradients, and thus the EF, will be close to zero at a minimum, whereas the '
               'Hessian will generally be nonzero.'],
     'raw_file': 'f1/src/pdf_1905.12558v3.txt',
     'agent_note': 'Bears (optimisation, not continual learning): the empirical Fisher can be arbitrarily wrong as a curvature, '
                   'and near zero at an interpolating minimum where the Hessian is not; this is the mechanism SEC\'s '
                   'calibration targets.'},
    {'id': 'f1:11', 'tag': 'S1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Martens, "New insights and perspectives on the natural gradient method" (arXiv:1412.1193; JMLR 21(146), 2020)',
     'version': 'v11, 19 Sep 2020', 'url': 'https://arxiv.org/abs/1412.1193',
     'quote': ['in order to correct for how the empirical Fisher doesn’t have the right “scale” (which is ultimately the reason '
               'why it does poorly in the example given at the end of Section 11.1).'],
     'raw_file': 'f1/src/pdf_1412.1193v11.txt',
     'agent_note': 'Bears (optimisation): the empirical Fisher is stated to have the wrong scale.'},
    {'id': 'f1:12', 'tag': 'S1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Wenzel et al., "How Good is the Bayes Posterior in Deep Neural Networks Really?" (arXiv:2002.02405; ICML 2020)',
     'version': 'v2, 2 Jul 2020', 'url': 'https://arxiv.org/abs/2002.02405',
     'quote': ['we demonstrate through careful MCMC sampling that the posterior predictive induced by the Bayes posterior yields '
               'systematically worse predictions compared to simpler methods including point estimates obtained from SGD. '
               'Furthermore, we demonstrate that predictive performance is improved significantly through the use of a “cold '
               'posterior” that overcounts evidence.'],
     'raw_file': 'f1/src/pdf_2002.02405v2.txt',
     'agent_note': 'Bears: in Bayesian deep learning the Bayes weighting (T = 1) is beaten by overcounting; no Fisher or '
                   'continual-learning claim.'},
    {'id': 'f1:13', 'tag': 'S1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Kutalev, Lapina, "Stabilizing Elastic Weight Consolidation method in practical ML tasks and using weight '
               'importances for neural network pruning" (arXiv:2109.10021; venue not stated)',
     'version': 'v3, 29 Oct 2021', 'url': 'https://arxiv.org/abs/2109.10021',
     'quote': ['From this reasoning, it follows that for a particular neural network architecture and a particular set of '
               'datasets in sequential learning, there exists an optimal value of λ, at which the maximum average accuracy '
               'after sequential training of all datasets is achieved. And this optimal value λ can be found empirically. '
               'For example, by a simple grid search.'],
     'raw_file': 'f1/src/pdf_2109.10021v3.txt',
     'agent_note': 'Bears: lambda is per architecture and dataset set, found by grid search (41 for an MLP, 675 for a CNN in '
                   'its Table 1); no attribution to the Fisher scale.'},
    {'id': 'f1:14', 'tag': 'S1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Yin, Farajtabar, Li, Levine, Mott, "Optimization and Generalization of Regularization-Based Continual '
               'Learning: a Loss Approximation Viewpoint" (arXiv:2006.10974)',
     'version': 'v3, 8 Feb 2021', 'url': 'https://arxiv.org/abs/2006.10974',
     'quote': ['In our experiments, we tune λ and report the results with the choice of λ that produces the best average test '
               'accuracy over all tasks.',
               'These results confirm our theoretical finding that an accurate Hessian approximation is important for '
               'regularization-based algorithms.'],
     'raw_file': 'f1/src/pdf_2006.10974v3.txt',
     'agent_note': 'Bears: lambda tuned; the accuracy of the Hessian approximation matters. No link between the two.'},
    {'id': 'f1:15', 'tag': 'S1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Jhajj, Lin, "Elastic Weight Consolidation for Knowledge Graph Continual Learning: An Empirical Evaluation" '
               '(arXiv:2512.01890; NeurIPS 2025 NORA workshop)',
     'version': 'v1, 1 Dec 2025', 'url': 'https://arxiv.org/abs/2512.01890',
     'quote': ['This suggests that optimal regularization strength depends on task construction: relation-grouped tasks require '
               'stronger protection of essential parameters, while randomly distributed tasks benefit from more flexibility.'],
     'raw_file': 'f1/src/pdf_2512.01890v1.txt',
     'agent_note': 'Bears: the best lambda differs between task constructions; the reason given is interference, not scale.'},
    {'id': 'f1:16', 'tag': 'S1', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Zheng, Zhang, van de Weijer, van de Ven, Du, Zhang, Tian, "Revisiting Weight Regularization for Low-Rank '
               'Continual Learning" (EWC-LoRA; arXiv:2602.17559; ICLR 2026)',
     'version': 'v1, 19 Feb 2026', 'url': 'https://arxiv.org/abs/2602.17559',
     'quote': ['Specifically, for the results in Table 2 and 4, a unified regularization strength is used across datasets. With '
               'λ = 107, EWC-LoRA consistently achieves a favorable balance between stability and plasticity, without '
               'requiring dataset-specific tuning.',
               'We observe that across all datasets, when using the empirical Fisher, the best overall performance is '
               'achieved around 107.',
               'In general, the Exact Fisher outperforms the Empirical Fisher, requiring a smaller regularization strength, '
               'but higher computational costs.'],
     'raw_file': 'f1/src/pdf_2602.17559v1.txt',
     'agent_note': 'Contradicts (judgement call): in EWC on LoRA over a pre-trained ViT, one lambda (1e7, extracted as "107") '
                   'is reported best across all datasets, without dataset-specific tuning. The third quote is close to S1 in '
                   'the other direction (the Fisher estimator moves the needed lambda). Scope differs from SEC (pre-trained '
                   'backbone, low-rank updates).'},
    # ------------------------------------------------------------------ S2
    {'id': 'f1:17', 'tag': 'S2', 'reading': 'close', 'reading_by': RB,
     'source': 'Moser, Anwar, Nauen, Muralidhara, Raue, Schuster, Frolov, Dengel, "Layers Matter: Why Continual Learning '
               'Regularization Should Be Layer-Adaptive" (arXiv:2608.15901; preprint)',
     'version': 'v1, 16 Aug 2026', 'url': 'https://arxiv.org/abs/2608.15901',
     'quote': ['each layer’s diagonal Fisher is a weak summary of its actual curvature, missing the top-eigenvalue information '
               'that controls forgetting.',
               'To measure sℓon a real network, run power iteration on H(ℓ,ℓ) using Hessian-Vector Products (HVPs).',
               'The measured-s schedule underperforms uniform on both backbones, by 4–14% absolute.',
               'Figure 11 reports avg-acc at the best c per cell.'],
     'raw_file': 'f1/src/pdf_2608.15901v1.txt',
     'agent_note': 'Close, and the nearest S2 source in F1: the EWC penalty is re-weighted per layer by the loss Hessian\'s '
                   'top eigenvalue measured with Hessian-vector products, because the diagonal Fisher misses the curvature. It '
                   'is a per-layer shape correction, the overall constant c is still grid-searched, and the literal measured '
                   'schedule lost to uniform EWC (a smoothed exponent did better).'},
    {'id': 'f1:18', 'tag': 'S2', 'reading': 'close', 'reading_by': RB,
     'source': 'Vander Eeckt, Van hamme, "Continual Learning With Quasi-Newton Methods" (CSQN; arXiv:2503.19939; IEEE Access '
               '13, 2025)',
     'version': 'v1, 25 Mar 2025', 'url': 'https://arxiv.org/abs/2503.19939',
     'quote': ['However, EWC relies on a Laplace approximation where the Hessian is simplified to the diagonal of the Fisher '
               'information matrix, assuming uncorrelated model parameters. This overly simplistic assumption often leads to '
               'poor Hessian estimates, limiting its effectiveness. To overcome this limitation, we introduce Continual '
               'Learning with Sampled Quasi-Newton (CSQN), which leverages Quasi-Newton methods to compute more accurate '
               'Hessian approximations.',
               'This means that the regularization loss of CSQN can be split into two terms: one term is related to B0 and '
               'therefore equal to EWC’s regularization loss, while the second term is related to S and Y and the '
               'corresponding rank-2M or rank-M Hessian approximations.'],
     'raw_file': 'f1/src/pdf_2503.19939v1.txt',
     'agent_note': 'Close: the Fisher diagonal is kept as B0 and corrected by a low-rank quasi-Newton (Hessian-vector) term; '
                   'an additive correction, not a rescaling of the Fisher.'},
    {'id': 'f1:19', 'tag': 'S2', 'reading': 'close', 'reading_by': RB,
     'source': 'Aguilar, Zainal, Herbozo Contreras, Huang, Kavehei, "Normative Loss Landscape Navigation: A Trajectory-Based '
               'Approach to Mitigating Forgetting in Incremental Learning" (TMLN; arXiv:2609.35926; preprint)',
     'version': 'v1, 28 Sep 2026', 'url': 'https://arxiv.org/abs/2609.35926',
     'quote': ['At the end of task k, we normalize this trajectory (computed in Eq. 2) against the Riemannian distance traveled, '
               'yielding the parameter-specific sensitivity score S(k) i (Eq. 3):',
               'This ensures that parameters historically vital for optimization are aggressively shielded, even if the '
               'diagonal Fisher incorrectly predicts a low local curvature.'],
     'raw_file': 'f1/src/pdf_2609.35926v1.txt',
     'agent_note': 'Close: per parameter, the loss drop observed along the task\'s path is divided by the Fisher\'s predicted '
                   'quadratic drop (S = omega / (F Delta^2 / 2), Eq. 3), an observed-to-Fisher ratio with the shape of SEC\'s '
                   's = c / rho; but the ratios are then normalised by their maximum (so the units are discarded) and enter '
                   'as additive damping of a preconditioner, not as a rescaling of a penalty. Posted two days before the sweep.'},
    {'id': 'f1:20', 'tag': 'S2', 'reading': 'close', 'reading_by': RB,
     'source': 'Martens, "New insights and perspectives on the natural gradient method" (arXiv:1412.1193; JMLR 21(146), 2020)',
     'version': 'v11, 19 Sep 2020', 'url': 'https://arxiv.org/abs/1412.1193',
     'quote': ['in order to correct for how the empirical Fisher doesn’t have the right “scale” (which is ultimately the reason '
               'why it does poorly in the example given at the end of Section 11.1).',
               'CG is invariant to the overall scale of its preconditioner (since it computes an optimal “step-size” at each '
               'step which automatically adjusts for the scale).'],
     'raw_file': 'f1/src/pdf_1412.1193v11.txt',
     'agent_note': 'Close (optimisation, not continual learning): empirical-Fisher preconditioners are combined with '
                   'Gauss-Newton estimates to correct their scale (Schaul et al. 2013), and CG\'s line-search step absorbs '
                   'the scale. No penalty.'},
    {'id': 'f1:21', 'tag': 'S2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Kirkpatrick et al., "Overcoming catastrophic forgetting in neural networks" (EWC; arXiv:1612.00796; PNAS 2017)',
     'version': 'v2, 25 Jan 2017', 'url': 'https://arxiv.org/abs/1612.00796',
     'quote': ['F has three key properties [Pascanu and Bengio, 2013]: (a) it is equivalent to the second derivative of the loss '
               'near a minimum'],
     'raw_file': 'f1/src/pdf_1612.00796v2.txt',
     'agent_note': 'Bears: EWC\'s premise that the Fisher equals the loss curvature near a minimum is the premise SEC\'s '
                   'calibration checks; if it held, s_j would be 1.'},
    {'id': 'f1:22', 'tag': 'S2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Schwarz et al., "Progress & Compress: A scalable framework for continual learning" (arXiv:1805.06370; ICML 2018)',
     'version': 'v2, 2 Jul 2018', 'url': 'https://arxiv.org/abs/1805.06370',
     'quote': ['We counteract this issue by normalising the Fisher information matrices Fi for each task.'],
     'raw_file': 'f1/src/pdf_1805.06370v2.txt',
     'agent_note': 'Bears: a published per-task rescaling of the Fisher, but by its own norm, not by observed loss curvature.'},
    # ------------------------------------------------------------------ S3
    {'id': 'f1:23', 'tag': 'S3', 'reading': 'states', 'reading_by': RB,
     'source': 'Zenke, Poole, Ganguli, "Continual Learning Through Synaptic Intelligence" (SI; arXiv:1703.04200; ICML 2017)',
     'version': 'v3, 12 Jun 2017', 'url': 'https://arxiv.org/abs/1703.04200',
     'quote': ['The quadratic surrogate loss (green) is chosen to precisely match 3 aspects of the descent dynamics on the '
               'original loss function: the total drop in the loss function L(θ(0)) −L(θ(T)), the total net motion in '
               'parameter space θ(0) −θ(T), and achieving a minimum at the endpoint θ(T).',
               'Note that this surrogate loss is different from a quadratic approximation defined by the Hessian at the '
               'minimum (purple dashed line).',
               'Note that the term in the denominator (∆ν k)2 ensures that the regularization term carries the same units as '
               'the loss L.',
               'It is important to stress that the path integral for importance is computed by integrating information along '
               'the entire learning trajectory (cf. Fig. 2).'],
     'raw_file': 'f1/src/pdf_1703.04200v3.txt',
     'agent_note': 'States (judgement call): SI\'s penalty curvature Omega = omega / Delta^2 is a quadratic fitted along the '
                   'path (the loss drop over the squared net displacement per parameter), a secant-style fit, used as the '
                   'continual-learning penalty, with units matched to the loss. It differs from SEC: it replaces the Fisher '
                   'instead of rescaling it, it is per parameter and loss-value based (not a gradient secant along the '
                   'mean-parameter change), and its strength c is tuned.'},
    {'id': 'f1:24', 'tag': 'S3', 'reading': 'close', 'reading_by': RB,
     'source': 'Vander Eeckt, Van hamme, "Continual Learning With Quasi-Newton Methods" (CSQN; arXiv:2503.19939; IEEE Access '
               '13, 2025)',
     'version': 'v1, 25 Mar 2025', 'url': 'https://arxiv.org/abs/2503.19939',
     'quote': ['In SQN methods, the Hessian approximation is obtained by sampling around the current estimate of the local '
               'optimum, meaning that the [...] Hessian is computed anew at each iteration without relying on previous ones.',
               'Most of the baselines, as well as our method, require choosing a hyper-parameter λ to determine the weight of '
               'the regularization.',
               'For each experiment, we selected the value of λ with the best performance on the validation sets of all tasks'],
     'raw_file': 'f1/src/pdf_2503.19939v1.txt',
     'agent_note': 'Close: quasi-Newton curvature sets the continual-learning penalty, but it is sampled around the endpoint, '
                   'not fitted along the path travelled, and lambda is still tuned per benchmark.'},
    {'id': 'f1:25', 'tag': 'S3', 'reading': 'close', 'reading_by': RB,
     'source': 'Aguilar, Zainal, Herbozo Contreras, Huang, Kavehei, "Normative Loss Landscape Navigation" (TMLN; '
               'arXiv:2609.35926; preprint)',
     'version': 'v1, 28 Sep 2026', 'url': 'https://arxiv.org/abs/2609.35926',
     'quote': ['we introduce a temporal constraint, which we term trajectory-modulated damping. We track the continuous path '
               '[...] integral [4] of the parameters to measure their historical contribution to loss reduction.',
               'To construct our dynamic damping tensor, we maintain a normalized running history of these trajectory scores '
               'for all tasks seen'],
     'raw_file': 'f1/src/pdf_2609.35926v1.txt',
     'agent_note': 'Close: a path-based observed-over-Fisher ratio is carried across tasks, but as preconditioner damping '
                   '(no penalty), max-normalised, with its own weight gamma.'},
    {'id': 'f1:26', 'tag': 'S3', 'reading': 'bears', 'reading_by': RB,
     'source': 'Moser et al., "Layers Matter: Why Continual Learning Regularization Should Be Layer-Adaptive" '
               '(arXiv:2608.15901; preprint)',
     'version': 'v1, 16 Aug 2026', 'url': 'https://arxiv.org/abs/2608.15901',
     'quote': ['Trajectory drift away from the pretraining checkpoint, where the ratios at θ⋆need not hold along the optimizer '
               'path, is a third candidate; the re-measurement experiment below isolates it.',
               'this locates the causes of the negative result above: drift is real but secondary, and magnitude smoothing is '
               'primary.'],
     'raw_file': 'f1/src/pdf_2608.15901v1.txt',
     'agent_note': 'Bears: endpoint curvature ratios need not hold along the path; re-measuring at each task boundary helped '
                   'only secondarily. No path-fitted curvature.'},
    {'id': 'f1:27', 'tag': 'S3', 'reading': 'bears', 'reading_by': RB,
     'source': 'Benzing, "Unifying Regularisation Methods for Continual Learning" (arXiv:2006.06357; AISTATS 2022 per the '
               'proceedings reference in arXiv:2502.11756)',
     'version': 'v2, 3 Feb 2021', 'url': 'https://arxiv.org/abs/2006.06357',
     'quote': ['Moreover, we show that for SI the relation to the Fisher – and in fact its performance – is due to a previously '
               'unknown bias.',
               '(a) We show that SI’s importance approximation is biased and that the bias rather than SI’s original '
               'motivation is responsible for its performance.'],
     'raw_file': 'f1/src/pdf_2006.06357v2.txt',
     'agent_note': 'Bears on reading SI as a path-fitted curvature: in practice SI\'s estimate is dominated by gradient-noise '
                   'bias (approximately the square root of the Fisher), not by the path integral.'},
    {'id': 'f1:28', 'tag': 'S3', 'reading': 'bears', 'reading_by': RB,
     'source': 'Lee, Hong, Joo, Kim, "Continual Learning With Extended Kronecker-Factored Approximate Curvature" (CVPR 2020, '
               'CVF open access)',
     'version': 'CVF open access, CVPR 2020', 'url': 'https://openaccess.thecvf.com/content_CVPR_2020/papers/Lee_Continual_'
                                                   'Learning_With_Extended_Kronecker-Factored_Approximate_Curvature_CVPR_2020_paper.pdf',
     'quote': ['our basic idea is to adaptively scale the source task penalty loss λsLs and target task loss λtLt during '
               'training so that they converge to similar values, and to expect that the source and target accuracy drops also '
               'would be similar.'],
     'raw_file': 'f1/src/cvf_Lee_CVPR2020.txt',
     'agent_note': 'Bears: the penalty is rescaled during training from observed loss values (balancing), not from curvature.'},
    # ------------------------------------------------------------------ S4
    {'id': 'f1:29', 'tag': 'S4', 'reading': 'states', 'reading_by': RB,
     'source': 'Daxberger, Kristiadi, Immer, Eschenhagen, Bauer, Hennig, "Laplace Redux -- Effortless Bayesian Deep Learning" '
               '(arXiv:2106.14806; NeurIPS 2021)',
     'version': 'v3, 14 Mar 2022', 'url': 'https://arxiv.org/abs/2106.14806',
     'quote': ['Further, we describe how this can be combined with the evidence framework to update the prior online alleviating '
               'the need for a validation set, which is unlikely to be available in real continual learning scenarios.',
               'This can be done by computing the eigendecomposition of the summed Kronecker factors [22] and allows us to 1) '
               'adjust the regularization suitably per task and 2) avoid setting a hyperparameter thereby alleviating the need '
               'for validation data.'],
     'raw_file': 'f1/src/pdf_2106.14806v3.txt',
     'agent_note': 'States: continual learning with a Laplace posterior (log-likelihood Hessians summed at unit weight) and the '
                   'prior precision set by marginal likelihood per task, with no validation. The evidence sets the isotropic '
                   'prior, not a multiplier on the curvature.'},
    {'id': 'f1:30', 'tag': 'S4', 'reading': 'states', 'reading_by': RB,
     'source': 'Nguyen, Li, Bui, Turner, "Variational Continual Learning" (VCL; arXiv:1710.10628; ICLR 2018)',
     'version': 'v3, 20 May 2018', 'url': 'https://arxiv.org/abs/1710.10628',
     'quote': ['VCL differs from the above methods in several ways. First, unlike MAP, EWC and SI, it does not have free '
               'parameters that need to be tuned on a validation set. This can be especially awkward in the online setting.',
               'EWC, diagonal LP and SI that employ tuned hyper-parameters λ whereas VCL’s objective is hyper-parameter free.'],
     'raw_file': 'f1/src/pdf_1710.10628v3.txt',
     'agent_note': 'States: a principled (variational Bayes, unit-weight KL) continual learner with no tuned weight. It is not '
                   'a Laplace/EWC weight.'},
    {'id': 'f1:31', 'tag': 'S4', 'reading': 'states', 'reading_by': RB,
     'source': 'Lee, Hong, Joo, Kim, "Continual Learning With Extended Kronecker-Factored Approximate Curvature" (CVPR 2020, '
               'CVF open access)',
     'version': 'CVF open access, CVPR 2020', 'url': 'https://openaccess.thecvf.com/content_CVPR_2020/papers/Lee_Continual_'
                                                   'Learning_With_Extended_Kronecker-Factored_Approximate_Curvature_CVPR_2020_paper.pdf',
     'quote': ['In our method, finding importance hyperparameters λs and λt using the source and target data is the same as '
               'optimizing the magnitude of the penalty loss, and thus, they should not be picked by validation over whole '
               'tasks.',
               'without any validation, where T is the number of tasks the model has learned so far.',
               'However, there is not a natural choice for such hyperparameters, unlike the importance hyperparameters.'],
     'raw_file': 'f1/src/cvf_Lee_CVPR2020.txt',
     'agent_note': 'States: the K-FAC penalty\'s importance weights are set by task count (T/(T+1), 1/(T+1)) without validation. '
                   'Learning rate and damping have no natural choice and are validated on the target task only.'},
    {'id': 'f1:32', 'tag': 'S4', 'reading': 'close', 'reading_by': RB,
     'source': 'Immer, Bauer, Fortuin, Rätsch, Khan, "Scalable Marginal Likelihood Estimation for Model Selection in Deep '
               'Learning" (arXiv:2104.04975; ICML 2021)',
     'version': 'v3, 15 Jun 2021', 'url': 'https://arxiv.org/abs/2104.04975',
     'quote': ['we present a scalable marginal-likelihood estimation method to select both hyperparameters and network '
               'architectures, based on the training data alone. Some hyperparameters can be estimated online during training, '
               'simplifying the procedure.',
               'Finally, extending this work beyond supervised learning, e.g., to bandits, Bayesian optimization, active '
               'learning, or continual learning, is an important avenue for future research.'],
     'raw_file': 'f1/src/pdf_2104.04975v3.txt',
     'agent_note': 'Close: online marginal-likelihood selection of prior precisions, outside continual learning (named as '
                   'future work there).'},
    {'id': 'f1:33', 'tag': 'S4', 'reading': 'close', 'reading_by': RB,
     'source': 'Loo, Swaroop, Turner, "Generalized Variational Continual Learning" (GVCL; arXiv:2011.12328)',
     'version': 'v1, 24 Nov 2020', 'url': 'https://arxiv.org/abs/2011.12328',
     'quote': ['Instead, our derivation produces an implicit value of λ = 1, i.e. equal weight between tasks of equal sample '
               'count.'],
     'raw_file': 'f1/src/pdf_2011.12328v1.txt',
     'agent_note': 'Close: the principled (Bayes) weight is derived in continual learning, then replaced by a tempered, tuned '
                   'lambda.'},
    {'id': 'f1:34', 'tag': 'S4', 'reading': 'close', 'reading_by': RB,
     'source': 'Huszár, "On Quadratic Penalties in Elastic Weight Consolidation" (arXiv:1712.03847; PNAS 2018 letter)',
     'version': 'v1, 11 Dec 2017', 'url': 'https://arxiv.org/abs/1712.03847',
     'quote': ['The Hessian of the negative log likelihood −log p(DB|θ) can be approximated as sample size times the diagonal '
               'Fisher information NB diag(FB,i) as before. Replacing NB by a hyperparameter λB, this gives rise to the '
               'following approximation:'],
     'raw_file': 'f1/src/pdf_1712.03847v1.txt',
     'agent_note': 'Close (the S4 rule: a principled value derived in continual learning, then not used untuned): the Bayes '
                   'weight SEC starts from (task size times the Fisher, i.e. w = 1/2 on the task-size-weighted Fisher) is '
                   'written down, and then replaced by a hyperparameter.'},
    {'id': 'f1:35', 'tag': 'S4', 'reading': 'close', 'reading_by': RB,
     'source': 'Zenke, Poole, Ganguli, "Continual Learning Through Synaptic Intelligence" (SI; arXiv:1703.04200; ICML 2017)',
     'version': 'v3, 12 Jun 2017', 'url': 'https://arxiv.org/abs/1703.04200',
     'quote': ['Finally, c is a strength parameter which trades off old versus new memories. If the path integral (Eq. 3) is '
               'evaluated precisely, c = 1 would correspond to an equal weighting of old and new memories. However, due to '
               'noise in the evaluation of the path integral (Eq. 3), c typically has to be chosen smaller than one to '
               'compensate.'],
     'raw_file': 'f1/src/pdf_1703.04200v3.txt',
     'agent_note': 'Close (the S4 rule: a principled value derived in continual learning, then not used untuned): c = 1 is '
                   'the equal-weighting value for a units-matched path curvature, but c is chosen below one.'},
    # ------------------------------------------------------------------ S5
    {'id': 'f1:36', 'tag': 'S5', 'reading': 'states', 'reading_by': RB,
     'source': 'Kutalev, Lapina, "Stabilizing Elastic Weight Consolidation method in practical ML tasks and using weight '
               'importances for neural network pruning" (arXiv:2109.10021)',
     'version': 'v3, 29 Oct 2021', 'url': 'https://arxiv.org/abs/2109.10021',
     'quote': ['In the case Ωi ≥ 2 αλ, the weight wi will not only jump over the',
               'Thus, there will be an effect known as “gradient explosion”.',
               'To solve these problems, we used a stabilization mechanism that prevents the appearance in the regularizing '
               'contribution to the weight increment of values larger than the difference of the consolidated and current '
               'weight',
               'Thus the contribution to the anti-gradient of the regularizing component will not exceed the difference of '
               'weights even at any large importance of weight.'],
     'raw_file': 'f1/src/pdf_2109.10021v3.txt',
     'agent_note': 'States: the stability edge (importance >= 2/(lr lambda) explodes) is derived for EWC under SGD, and the '
                   'importance is bounded as Omega/(lr lambda Omega + 1), so the penalty step never exceeds the distance to '
                   'the anchor (a soft cap at 1/(lr lambda), i.e. kappa -> 1). SEC4 hard-clips at kappa = 0.5.'},
    {'id': 'f1:37', 'tag': 'S5', 'reading': 'close', 'reading_by': RB,
     'source': 'Jones, Sprague, "Continual Learning Through Expandable Elastic Weight Consolidation" (James Madison University; '
               'file CL-2018_paper_75.pdf; venue not verified on the day)',
     'version': 'PDF as served on 2026-09-30', 'url': 'https://w3.cs.jmu.edu/spragunr/papers/CL-2018_paper_75.pdf',
     'quote': ['First, as the number of tasks increases, preserving weights via EWC eventually results in numerical instability '
               'in the training process as the weight preservation penalty grows without bound.',
               'In our experiments, we observed that EWC consistently diverged within 18 tasks when training a network with 1 '
               'hidden layer containing 20 nodes (learning rate = 0.1, λ = 15).',
               'This addresses the issue of training instability by decreasing the learning rate for exactly the parameters '
               'that are subject to large gradients as a result of the EWC penalty term.'],
     'raw_file': 'f1/src/jmu_CL-2018_paper_75.txt',
     'agent_note': 'Close: divergence of EWC at large accumulated penalty is reported, and fixed by a per-parameter learning '
                   'rate lowered by the Fisher and lambda (the step adapted, not the importance clipped).'},
    {'id': 'f1:38', 'tag': 'S5', 'reading': 'close', 'reading_by': RB,
     'source': 'Ritter, Botev, Barber, "Online Structured Laplace Approximations For Overcoming Catastrophic Forgetting" '
               '(arXiv:1805.07810)',
     'version': 'v1, 20 May 2018', 'url': 'https://arxiv.org/abs/1805.07810',
     'quote': ['We decay the initial learning rate for the second task depending on the hyperparameter to prevent the objective '
               'from diverging.',
               'We set k using a coarse grid search for each value of the hyperparameter λ in order to prevent the objective '
               'from diverging towards the end of training, in particular with the Kronecker factored curvature '
               'approximation.'],
     'raw_file': 'f1/src/pdf_1805.07810v1.txt',
     'agent_note': 'Close: the learning rate is tied to lambda to prevent divergence of a Laplace-penalised learner, by search '
                   'rather than by a stability-edge bound.'},
    {'id': 'f1:39', 'tag': 'S5', 'reading': 'close', 'reading_by': RB,
     'source': 'Aguilar, Zainal, Kavehei, "Metaplasticity as adaptive gradient preconditioning for incremental learning" '
               '(SynGAP; arXiv:2608.14634; preprint)',
     'version': 'v1, 27 Jul 2026', 'url': 'https://arxiv.org/abs/2608.14634',
     'quote': ['Raw FIM values can vary by orders of magnitude, contributing to instability in optimization. To translate the '
               'unbounded metaplastic state vector F into a stable learning mechanism, we introduce a globally normalized '
               'plasticity function, denoted g(F).'],
     'raw_file': 'f1/src/pdf_2608.14634v1.txt',
     'agent_note': 'Close: Fisher importance bounded (tanh of a mean-normalised Fisher) for stability, not by the step size; a '
                   'preconditioner, not a penalty.'},
    # ------------------------------------------------------------------ S6
    {'id': 'f1:40', 'tag': 'S6', 'reading': 'close', 'reading_by': RB,
     'source': 'Daxberger et al., "Laplace Redux -- Effortless Bayesian Deep Learning" (arXiv:2106.14806; NeurIPS 2021)',
     'version': 'v3, 14 Mar 2022', 'url': 'https://arxiv.org/abs/2106.14806',
     'quote': ['update the LAs after each task as suggested by Ritter et al. [24] and improve upon their result by tuning the '
               'prior precision through marginal likelihood optimization during training, following Immer et al. [22] '
               '(details in Appendix C.4).',
               'Using this scheme, the performance after 10 tasks is at around 96% accuracy, outperforming other Bayesian '
               'approaches for continual learning [7, 75, 76].'],
     'raw_file': 'f1/src/pdf_2106.14806v3.txt',
     'agent_note': 'Close: a tuning-free (evidence-set) Laplace continual learner improves on Ritter et al.\'s validation-tuned '
                   'result, on one benchmark (permuted MNIST) only.'},
    {'id': 'f1:41', 'tag': 'S6', 'reading': 'close', 'reading_by': RB,
     'source': 'Nguyen, Li, Bui, Turner, "Variational Continual Learning" (VCL; arXiv:1710.10628; ICLR 2018)',
     'version': 'v3, 20 May 2018', 'url': 'https://arxiv.org/abs/1710.10628',
     'quote': ['From this figure, VCL outperforms EWC, SI, and LP by large margins, even though they benefited from an '
               'extensive hyper-parameter search for λ.',
               'Again, unlike VCL, EWC and SI benefited from a hyper-parameter search for λ, but a value close to 1 performs '
               'well in both cases.'],
     'raw_file': 'f1/src/pdf_1710.10628v3.txt',
     'agent_note': 'Close: a tuning-free Bayesian learner matches or beats tuned-lambda EWC on several benchmarks, but it is '
                   'variational, not a Laplace weight. On split MNIST the tuned EWC lambda is itself near the Bayes value 1.'},
    {'id': 'f1:42', 'tag': 'S6', 'reading': 'close', 'reading_by': RB,
     'source': 'Zheng et al., "Revisiting Weight Regularization for Low-Rank Continual Learning" (EWC-LoRA; arXiv:2602.17559; '
               'ICLR 2026)',
     'version': 'v1, 19 Feb 2026', 'url': 'https://arxiv.org/abs/2602.17559',
     'quote': ['This finding facilitates the use of a unified regularization strength across datasets, eliminating the need for '
               'dataset-specific tuning.'],
     'raw_file': 'f1/src/pdf_2602.17559v1.txt',
     'agent_note': 'Close: one lambda, chosen once by a sweep, is reused across datasets (SEC4-T\'s "reused lambda" route), '
                   'not a tuning-free rule.'},
    {'id': 'f1:43', 'tag': 'S6', 'reading': 'bears', 'reading_by': RB,
     'source': 'Kao et al., "Natural continual learning" (NCL; arXiv:2106.08085; NeurIPS 2021)',
     'version': 'v2, 15 Dec 2021', 'url': 'https://arxiv.org/abs/2106.08085',
     'quote': ['we found that NCL, OWM, and DOWM outperformed KFAC with λ = 1 (Figure 3A; see also Duncker et al., 2020 for a '
               'comparison of DOWM and EWC).'],
     'raw_file': 'f1/src/pdf_2106.08085v2.txt',
     'agent_note': 'Bears: the raw Bayes weight (lambda = 1) K-FAC Laplace is behind; lambda in [100, 1000] is needed (f1:2). '
                   'This is the gap SEC\'s calibration is meant to close; no calibrated weight is tested.'},
    {'id': 'f1:44', 'tag': 'S6', 'reading': 'bears', 'reading_by': RB,
     'source': 'Ritter, Botev, Barber, "Online Structured Laplace Approximations For Overcoming Catastrophic Forgetting" '
               '(arXiv:1805.07810)',
     'version': 'v1, 20 May 2018', 'url': 'https://arxiv.org/abs/1805.07810',
     'quote': ['For the natural choice of λ = 1 (leftmost subfigure respectively), the network’s performance decays for the '
               'first task for both curvature approximations, yet it is able to learn the most recent task well.'],
     'raw_file': 'f1/src/pdf_1805.07810v1.txt',
     'agent_note': 'Bears: the natural (Bayes) lambda = 1 forgets; the tuned lambda = 3 is best on permuted MNIST.'},
    {'id': 'f1:45', 'tag': 'S6', 'reading': 'bears', 'reading_by': RB,
     'source': 'Cha, Cho, "Hyperparameters in Continual Learning: A Reality Check" (arXiv:2403.09066; TMLR 2025)',
     'version': 'v5, 28 Oct 2025', 'url': 'https://arxiv.org/abs/2403.09066',
     'quote': ['However, this protocol has significant shortcomings: it overestimates the CL capacity of algorithms and relies '
               'on unrealistic hyperparameter tuning, which is not feasible for real-world applications.',
               'Across more than 8,000 experiments, our results show that most state-of-the-art algorithms fail to replicate '
               'their reported performance, highlighting that their CL capacity has been significantly overestimated in the '
               'conventional evaluation protocol.'],
     'raw_file': 'f1/src/pdf_2403.09066v5.txt',
     'agent_note': 'Bears: in-scenario tuning (the tuned-lambda baseline SEC is compared with) overstates what a method '
                   'delivers on unseen scenarios; supports scoring against a transferred lambda (SEC4-T).'},
    {'id': 'f1:46', 'tag': 'S6', 'reading': 'bears', 'reading_by': RB,
     'source': 'Lee, Hellan, Ericson, Crowley, Storkey, "Hyperparameter Selection in Continual Learning" (arXiv:2404.06466; '
               'preprint)',
     'version': 'v2, 14 Mar 2025', 'url': 'https://arxiv.org/abs/2404.06466',
     'quote': ['We find that none of the HPO frameworks considered, including end-of-training HPO, perform consistently better '
               'than the rest on popular CL benchmarks.',
               'Surprisingly, we show that only fitting hyperparameters on the first task performs comparably to other '
               'realistic HPO frameworks for commonly used CL benchmarks.'],
     'raw_file': 'f1/src/pdf_2404.06466v2.txt',
     'agent_note': 'Bears: cheap hyperparameter selection is not consistently behind end-of-training tuning on standard '
                   'benchmarks, a weaker baseline than SEC\'s tuned lambda; not a tuning-free Laplace weight.'},
]
