"""Claims for OB1 stage 3, candidate C1 (Open_Bottlenecks/CRR_READING.md): arc-clocked optimiser timescales for the
stability gap. Transcribed from the dossier docs/citations/ob1_s3_c1_2026-09-30.md (sources fetched 2026-09-30; extracted
texts held outside the repository under /tmp/claude-0/ob1_s3/, named in `raw_file` relative to that root). Every quote is
copied from a dossier blockquote.

The mechanism searched (CRR_READING.md, C1): momentum / Adam moment averages that decay per unit of the learner's own change
(the step's KL between successive predictive distributions on a probe set, or its function- or parameter-space equivalent),
beta_t = beta ** (a_t / a_bar), rather than per step, so that stale moments are forgotten faster when a distribution shift
makes the per-step change jump; compared with step-clock moments and with NGM-SGD's fast timescale (arXiv:2507.14056).

'reading' is decided by the stage-3 agent from the quote, for the investigator's review ('reading_by'). Reading policy,
fixed before the readings were written (the caller's definitions):
  states       the source publishes the mechanism: an optimiser timescale, trigger or budget indexed by the learner's own
               accumulated change (KL, function-space, parameter-space or Fisher distance, or its per-step equivalent),
               used for the named purpose (forgetting stale optimiser memory at a distribution shift / the stability gap);
  close        a change-driven trigger or timescale, but on a different quantity (loss, likelihood, surprise, entropy,
               gradient norm or alignment) or for a different purpose (stationary convergence, oscillation control);
               also a reset of optimiser memory at a supplied or scheduled boundary (the clock the candidate replaces);
  bears        relevant evidence (on stale optimiser memory under shift, or on the step clock) that neither publishes
               nor negates the mechanism;
  contradicts  the source shows the mechanism (or its limiting case) fails or is inferior.
Grade rule (the caller's): REDUNDANT if any claim reads 'states'; else PARTLY REDUNDANT if any reads 'close'; else NOT FOUND
IN THE SWEEP. 'Not found' is never 'novel'.
"""

RB = "stage-3 agent; for the investigator's review"

CLAIMS = [
    # ------------------------------------------------ the frontier comparator (h1-B6)
    {'id': 'c1:0', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Rodriguez-Garcia, Ghosh, Ramaswamy, "Dynamic gain neuromodulation attenuates the stability gap under joint '
               'training" (NGM-SGD; arXiv:2507.14056)',
     'version': 'v3, 10 Aug 2026', 'url': 'https://arxiv.org/abs/2507.14056v3',
     'quote': ['Standard optimizers such as momentum-SGD (MSGD) (Rumelhart et al., 1986) and Adam (Kingma and Ba, 2015) '
               'introduce implicit multi-timescale regularization through momentum or adaptive learning rates, yet they still '
               'exhibit stability gaps.',
               'we introduce a dynamic gain scaling mechanism as a two-timescale optimization technique',
               'suggests that this form of uncertainty can be quantified as the Shannon entropy of the network’s readout:'],
     'raw_file': 'c1/txt/pdf_2507.14056v3.txt',
     'agent_note': 'Close: the frontier method for h1-B6 adds a fast timescale driven by a change signal read from the '
                   'learner, but the signal is the entropy of the current readout (an uncertainty level), not the size of '
                   'the step (the change between successive predictive distributions), and it modulates a forward-pass gain, '
                   'not the decay of the optimiser moments. CRR_READING.md calls the NGM-SGD timescale "loss-driven"; the '
                   'fetched text says entropy-driven.'},
    {'id': 'c1:1', 'tag': 'c1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Rodriguez-Garcia, Ghosh, Ramaswamy, NGM-SGD (arXiv:2507.14056), Appendix D and E: momentum resets at task '
               'switches',
     'version': 'v3, 10 Aug 2026', 'url': 'https://arxiv.org/abs/2507.14056v3',
     'quote': ['This was implemented by providing a task-change signal that forces the optimizer to clear its internal '
               'state, thereby removing all previously accumulated velocity',
               'momentum resets indeed reduce part of the instability in most of the cases (see highlighted colors), '
               'confirming that accumulated velocity can overshoot under abrupt loss-landscape shifts.',
               'The reset variants of MSGD and Adam exhibit mixed behaviour across benchmarks, sometimes reducing stability '
               'gaps and sometimes increasing them, indicating that resetting the optimizer state at task boundaries can '
               'lead to unstable optimization under replay.'],
     'raw_file': 'c1/txt/pdf_2507.14056v3.txt',
     'agent_note': 'Bears (the limiting case of C1, tested with an oracle): clearing the MSGD/Adam state at the supplied task '
                   'switch reduces part of the stability gap under joint training, still behind NGM-SGD, and is mixed '
                   '(sometimes worse) under replay. C1 predicts a graded, self-triggered version of this reset; the oracle '
                   'result bounds what forgetting stale moments can buy on this protocol. Not graded contradicts because '
                   'the reset is total and supplied, not arc-clocked.'},
    {'id': 'c1:2', 'tag': 'c1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Rodriguez-Garcia, Ghosh, Ramaswamy, NGM-SGD (arXiv:2507.14056), ablation Entropy-LR',
     'version': 'v3, 10 Aug 2026', 'url': 'https://arxiv.org/abs/2507.14056v3',
     'quote': ['Applying the entropy signal directly to the learning rate supports stronger acquisition of new tasks, but '
               'results in the largest average stability gap (Figure 4c,d).',
               'Entropy-dependent step-size adaptation alone is therefore insufficient to reproduce the transition-stabilizing '
               'effect of gain modulation.'],
     'raw_file': 'c1/txt/pdf_2507.14056v3.txt',
     'agent_note': 'Bears (a warning for C1): a change-driven optimiser adaptation that raises the effective step at a '
                   'transition gave the largest stability gap of the arms. Arc-clocked decay also lets the new gradient '
                   'dominate the moments faster at a switch; whether that deepens or shallows the dip is what a gate would '
                   'have to show.'},
    # ------------------------------------------------ momentum decay driven by the learner's own parameter velocity
    {'id': 'c1:3', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Karoni, Rajpal, Leimkuhler, Stoltz, "Adaptive Momentum and Nonlinear Damping for Neural Network Training" '
               '(iKFAD; arXiv:2602.00334; ICML 2026 per the arXiv comment)',
     'version': 'v2, 26 Jun 2026', 'url': 'https://arxiv.org/abs/2602.00334v2',
     'quote': ['we adopt a continuous-time formulation to introduce individual, adaptive momentum coefficients regulated by '
               'the kinetic energy of each model parameter.',
               'Having a friction or momentum coefficient that dynamically adapts based on the kinetic energy of the system '
               'would allow us to increase the damping when momenta are getting too high and decrease it when momenta are '
               'lower.',
               'We see that ξ is an exponentially weighted average of the squares of past momenta, i.e. kinetic energies.'],
     'raw_file': 'c1/txt/pdf_2602.00334v2.txt',
     'agent_note': 'Close, and the nearest in quantity: the momentum coefficient (discrete beta_n = exp(-(gamma + xi_n) dt)) '
                   'decays faster when the learner\'s own parameter velocity (momentum = rate of parameter change) has been '
                   'high, so memory is indexed by the learner\'s own movement rather than by the step count alone. It '
                   'differs from C1 in quantity (squared parameter velocity per coordinate, not the step\'s arc or KL '
                   'relative to its running mean), in form (added friction, not beta ** (a_t / a_bar)) and in purpose '
                   '(oscillation control in stationary training; no distribution shift or stability gap is studied).'},
    {'id': 'c1:4', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Karoni, Leimkuhler, Stoltz, "Friction-adaptive descent: a family of dynamics-based optimization methods" '
               '(FAD / KFAD; arXiv:2306.06738; J. Comput. Dyn. 2023 per the citing paper)',
     'version': 'v3 (fetched 2026-09-30)', 'url': 'https://arxiv.org/abs/2306.06738',
     'quote': ['we focus most of our attention on a specific variant: kinetic energy stabilization',
               'By introducing an auxiliary degree of freedom we create a dynamical system with improved stability, reducing '
               'oscillatory modes and accelerating convergence to minima.'],
     'raw_file': 'c1/txt/pdf_2306.06738v3.txt',
     'agent_note': 'Close: the predecessor of iKFAD, one adaptive friction (momentum decay) coefficient for all parameters, '
                   'driven by the kinetic energy of the parameter motion; purpose convergence and stability, no shift.'},
    # ------------------------------------------------ adaptive moment decay driven by a spike ratio
    {'id': 'c1:5', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Kassinos, "Kourkoutas-Beta: A Sunspike-Driven Adam Optimizer with Desert Flair" (arXiv:2508.12996)',
     'version': 'v2, 20 Aug 2025', 'url': 'https://arxiv.org/abs/2508.12996v2',
     'quote': ['replaces the fixed second-moment discount β2 with a layer-wise dynamic value driven by a bounded “sunspike” '
               'ratio: the current pooled gradient norm divided by an EMA (with coefficient α) of past norms, squashed to '
               '[0, 1).',
               'Large spikes lower β2 toward β2,min to react quickly; calm phases keep it near β2,max to smooth updates.'],
     'raw_file': 'c1/txt/pdf_2508.12996v2.txt',
     'agent_note': 'Close, and the nearest in form: an Adam discount lowered (memory shortened) when the current magnitude '
                   'jumps relative to its own running average, the shape of beta ** (a_t / a_bar). The quantity is the '
                   'gradient norm (a loss-side signal), not the learner\'s own change (step arc or KL); only beta2 is '
                   'adapted; the purpose is bursty gradients from sample-to-sample shifts in PDE surrogates and sequence '
                   'tasks, not the stability gap at a task switch.'},
    # ------------------------------------------------ restart / reset of optimiser memory at a change
    {'id': 'c1:6', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Sahu, Hogan, Wells, "On the Provable Suboptimality of Momentum SGD in Nonstationary Stochastic Optimization" '
               '(arXiv:2601.12238; ICML 2026 per the arXiv comment)',
     'version': 'v5, 24 Jul 2026', 'url': 'https://arxiv.org/abs/2601.12238v5',
     'quote': ['suggests resetting the momentum buffer after regime changes. One practical heuristic monitors the alignment',
               'This truncates stale velocity that would otherwise persist for',
               'Analyzing such restart rules rigorously, particularly whether they provably mitigate stale momentum under '
               'nonstationarity, is an interesting direction for future work.'],
     'raw_file': 'c1/txt/pdf_2601.12238v5.txt',
     'agent_note': 'Close: a self-triggered momentum restart after regime changes, to truncate stale velocity, stated as a '
                   'heuristic (not evaluated). The trigger is sustained misalignment between the new gradient and the '
                   'momentum buffer, not the size of the learner\'s own step; the action is a hard restart, not a decay '
                   'indexed by change.'},
    {'id': 'c1:7', 'tag': 'c1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Sahu, Hogan, Wells (arXiv:2601.12238), the drift penalty of fixed momentum',
     'version': 'v5, 24 Jul 2026', 'url': 'https://arxiv.org/abs/2601.12238v5',
     'quote': ['under distribution shift it incurs an explicit drift-amplification penalty that diverges as the momentum '
               'parameter',
               'in drift-dominated regimes, momentum is unavoidably worse because stale-gradient averaging forces '
               'systematic lag.'],
     'raw_file': 'c1/txt/pdf_2601.12238v5.txt',
     'agent_note': 'Bears: the theory behind C1\'s premise (stale momentum lags a moving optimum, with a lower bound), for '
                   'a fixed step-clock beta on strongly convex tracking problems.'},
    {'id': 'c1:8', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Ellis, Jackson, Lupu, Goldie, Fellows, Whiteson, Foerster, "Adam on Local Time: Addressing Nonstationarity '
               'in RL with Relative Adam Timesteps" (Adam-Rel; arXiv:2412.17113)',
     'version': 'v1, 22 Dec 2024', 'url': 'https://arxiv.org/abs/2412.17113v1',
     'quote': ['Rather than using the global timestep in the Adam update, Adam-Rel uses the local timestep within an epoch, '
               'essentially resetting Adam’s timestep to 0 after target changes.',
               'We demonstrate that this avoids large updates and reduces to learning rate annealing in the absence of such '
               'increases in gradient magnitude.'],
     'raw_file': 'c1/txt/pdf_2412.17113v1.txt',
     'agent_note': 'Close: Adam\'s clock is re-indexed ("local time") at each change of objective, but the change is supplied '
                   '(the target-network update), and the clock is still the step count since that change.'},
    {'id': 'c1:9', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Asadi, Fakoor, Sabach, "Resetting the Optimizer in Deep RL: An Empirical Study" (arXiv:2306.17833; NeurIPS '
               '2023 per the arXiv comment)',
     'version': 'v2, 15 Nov 2023', 'url': 'https://arxiv.org/abs/2306.17833v2',
     'quote': ['We demonstrate that this can contaminate the moment estimates because the optimization landscape can change '
               'arbitrarily from one iteration to the next one.',
               'each time we update the target network, we also reset the internal parameters of the optimizer.'],
     'raw_file': 'c1/txt/pdf_2306.17833v2.txt',
     'agent_note': 'Close: stale Adam moments after a change of objective, cured by a reset at the supplied change (the '
                   'target-network update, on a fixed schedule); no change-indexed decay.'},
    {'id': 'c1:10', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Huang, Zhu, Jin, Liu, Wang, Liu, "SPAM: Spike-Aware Adam with Momentum Reset for Stable LLM Training" '
               '(arXiv:2501.06842; ICLR 2025 per the PDF header)',
     'version': 'v2, 28 Feb 2025', 'url': 'https://arxiv.org/abs/2501.06842v2',
     'quote': ['By resetting the momentum terms at regular intervals of ∆T training iterations, we can prevent the lingering '
               'influence of anomalously large gradients on the optimizer’s state.'],
     'raw_file': 'c1/txt/pdf_2501.06842v2.txt',
     'agent_note': 'Close: resetting Adam\'s moments to forget stale (spiked) history, but on the step clock (every Delta T '
                   'iterations); the spike detection acts on the gradient (clipping), not on the moment timescale.'},
    {'id': 'c1:11', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': "O'Donoghue, Candès, \"Adaptive Restart for Accelerated Gradient Schemes\" (arXiv:1204.3982; Found. Comput. "
               'Math. 2015, venue not verified on the day)',
     'version': 'v1, 18 Apr 2012', 'url': 'https://arxiv.org/abs/1204.3982v1',
     'quote': ['This suggests a restart technique whereby we reset the momentum whenever we observe periodic behavior.',
               'The gradient scheme restarts whenever the momentum term and the negative gradient are making an obtuse angle.'],
     'raw_file': 'c1/txt/pdf_1204.3982v1.txt',
     'agent_note': 'Close (classical): momentum reset triggered by the trajectory itself (function increase, or '
                   'gradient-momentum angle), for convex convergence, not for distribution shift. The arXiv version '
                   'predates 2015.'},
    # ------------------------------------------------ shift-aware adaptation of Adam's use of stale moments
    {'id': 'c1:12', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Wang, Liu, Xiao, Liu, Yang, Xu, Pu, Zheng, Wang, Jiang, Zhang, Li, "CAdam: Confidence-Based Optimization for '
               'Online Learning" (arXiv:2411.19647)',
     'version': 'v2, 4 Jun 2025', 'url': 'https://arxiv.org/abs/2411.19647v2',
     'quote': ['Adam may use outdated momentum and the average of squared gradients, resulting in slower adaptation to '
               'distribution changes',
               'if not, it temporarily withholds updates and monitors potential shifts in data distribution in subsequent '
               'iterations.'],
     'raw_file': 'c1/txt/pdf_2411.19647v2.txt',
     'agent_note': 'Close: names C1\'s target (outdated Adam moments under distribution shift) and adapts to it without a '
                   'supplied boundary, but the signal is the sign consistency of momentum and gradient per coordinate, and '
                   'the action is to withhold updates, not to shorten the moment memory by the learner\'s own change.'},
    {'id': 'c1:13', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Rashidi, Ahmadi K. A., An, Wang, "Adaptive Momentum Coefficient for Neural Network Optimization" (AMoC; '
               'ECML PKDD 2020; author PDF at cs.yorku.ca; no arXiv version located)',
     'version': 'ECML PKDD 2020 author PDF (fetched 2026-09-30)', 'url': 'http://www.cs.yorku.ca/~aan/research/paper/ecml20.pdf',
     'quote': ['utilizes the inner product of the gradient and the previous update to the parameters, to effectively control '
               'the amount of weight put on the momentum term based on the change of direction in the optimization path.'],
     'raw_file': 'c1/txt/amoc_ecml20.txt',
     'agent_note': 'Close: a momentum weight set per step from the trajectory (direction change between gradient and the '
                   'previous parameter update); stationary optimisation, not shift, and direction rather than size of '
                   'change.'},
    # ------------------------------------------------ change-driven forgetting rates in online / Bayesian learning
    {'id': 'c1:14', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Galashov, Titsias, György, Lyle, Pascanu, Teh, Sahani, "Non-Stationary Learning of Neural Networks with '
               'Automatic Soft Parameter Reset" (arXiv:2411.04034; NeurIPS 2024 per the journal reference)',
     'version': 'v1, 6 Nov 2024', 'url': 'https://arxiv.org/abs/2411.04034v1',
     'quote': ['The amount of drift (and level of non-stationarity) is controlled by γt which are estimated online from the '
               'data.',
               'this approach adjusts the starting point θt of the update to a point ˜θt(γt), which is closer to the '
               'initialization and increases the learning rate proportionally to the drift.'],
     'raw_file': 'c1/txt/pdf_2411.04034v1.txt',
     'agent_note': 'Close: an optimiser timescale (the learning rate) and a soft reset set online by a detected drift, '
                   'without boundaries; the drift parameter is fitted by predictive likelihood (a loss-side quantity), and '
                   'the optimiser moments are not re-clocked.'},
    {'id': 'c1:15', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Li, Boyd, Smyth, Mandt, "Detecting and Adapting to Irregular Distribution Shifts in Bayesian Online '
               'Learning" (VBS; arXiv:2012.08101; NeurIPS 2021 per the arXiv comment)',
     'version': 'v3, 26 Oct 2021', 'url': 'https://arxiv.org/abs/2012.08101v3',
     'quote': ['if a change is detected–the model partially erases the information of past model updates by tempering to '
               'facilitate adaptation to the new data distribution.'],
     'raw_file': 'c1/txt/pdf_2012.08101v3.txt',
     'agent_note': 'Close: memory of past updates is shortened when a change is self-detected; detection is by model '
                   'evidence (likelihood), and the object forgotten is the posterior, not optimiser moments.'},
    {'id': 'c1:16', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Liakoni, Modirshanechi, Gerstner, Brea, "Learning in Volatile Environments with the Bayes Factor Surprise" '
               '(arXiv:1907.02936; Neural Computation 2021 per OpenReview/DBLP listing)',
     'version': 'v3, 23 Sep 2020', 'url': 'https://arxiv.org/abs/1907.02936v3',
     'quote': ['We demonstrate that in several existing approximate algorithms the Bayes Factor Surprise modulates the rate '
               'of adaptation to new observations.'],
     'raw_file': 'c1/txt/pdf_1907.02936v3.txt',
     'agent_note': 'Close: an adaptation (forgetting) rate modulated by a surprise signal (a likelihood ratio of the new '
                   'observation), in exponential-family estimators, not neural optimiser moments.'},
    {'id': 'c1:17', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Titsias, Galashov, Rannen-Triki, Pascanu, Teh, Bornschein, "Kalman Filter for Online Classification of '
               'Non-Stationary Data" (arXiv:2306.08448; ICLR 2024 per the journal reference)',
     'version': 'v1, 14 Jun 2023', 'url': 'https://arxiv.org/abs/2306.08448v1',
     'quote': ['Non-stationarity over the linear predictor weights is modelled using a “parameter drift” transition density, '
               'parametrized by a coefficient that quantifies forgetting.',
               'online SGD updates over the transition dynamics coefficient allows to adapt to the non-stationarity seen in '
               'data.'],
     'raw_file': 'c1/txt/pdf_2306.08448v1.txt',
     'agent_note': 'Close: a forgetting timescale adapted online to the stream\'s non-stationarity (by gradient on the '
                   'predictive likelihood), on a linear head over a representation; not the step\'s own change, not the '
                   'optimiser moments.'},
    {'id': 'c1:18', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Balsubramani, "Adaptive Bayes exactly tracks information over intrinsic time" (arXiv:2607.08789)',
     'version': 'v2, 26 Aug 2026', 'url': 'https://arxiv.org/abs/2607.08789v2',
     'quote': ['The cumulative cost defines a pathwise uncertainty clock, the intrinsic time of the realized sequence.',
               'The accounting also fixes a learning rate, inverse in the square root of intrinsic time.'],
     'raw_file': 'c1/txt/pdf_2607.08789v2.txt',
     'agent_note': 'Close: a learning-rate schedule indexed by a pathwise clock the update itself generates ("intrinsic '
                   'time"), not by the round count. The clock accumulates the per-round uncertainty cost (a tilted variance '
                   'of the losses under the learner\'s weights), not the KL between successive predictive distributions, '
                   'and the setting is exponential weights / online regret, not optimiser moments or the stability gap.'},
    {'id': 'c1:19', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Park, Park, Ko, Min, "Hybrid-TTA: Continual Test-time Adaptation via Dynamic Domain Shift Detection" '
               '(ICCV 2025, CVF open access)',
     'version': 'ICCV 2025 CVF open-access camera-ready', 'url': 'https://openaccess.thecvf.com/content/ICCV2025/papers/'
            'Park_Hybrid-TTA_Continual_Test-time_Adaptation_via_Dynamic_Domain_Shift_Detection_ICCV_2025_paper.pdf',
     'quote': ['DDSD captures this discrepancy by comparing the student’s predicted segmentation map and the teacher’s '
               'pseudo-label using the cross-entropy loss.',
               'At each time step t, this threshold is updated using an EMA of the newly calculated loss:'],
     'raw_file': 'c1/txt/cvf_iccv2025_hybridtta.txt',
     'agent_note': 'Close: a shift trigger read from the divergence between two of the learner\'s own predictive '
                   'distributions (EMA teacher vs student), against its own running average; it switches the tuning mode '
                   '(full vs efficient), not the decay of optimiser moments, and it compares slow and fast models rather '
                   'than successive steps.'},
    {'id': 'c1:25', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Hong, Lyu, Zhou, Spranger, "MECTA: Memory-Economic Continual Test-Time Model Adaptation" (ICLR 2023; '
               'OpenReview forum TIYamu7cK7, PDF NOT REACHED there (challenge page); read from the NSF PAR copy)',
     'version': 'ICLR 2023 camera-ready, NSF PAR record 10430106 (fetched 2026-09-30)',
     'url': 'https://par.nsf.gov/servlets/purl/10430106',
     'quote': ['where the parameter β ∈[0, 1] governs the memory length and therefore works as the forget gate.',
               'β should be large for avoiding the mixture of two distinct statistics.',
               'where D(·, ·) is a properly-defined distance function measuring distribution shifts.',
               'The distance function is inspired by Li et al. (2017), where the authors showed that ϕ1 and ϕ2 have larger '
               'KL divergence (based on a Gaussian assumption) if they are from distinct domains.'],
     'raw_file': 'c1/txt/nsf_mecta_10430106.txt',
     'agent_note': 'Close, and the nearest in form and purpose: an EMA whose memory length is set per step by a KL '
                   'divergence (beta_t = 1 - exp(-D), D a symmetric Gaussian KL), so that stale memory is dropped at a '
                   'distribution shift without a supplied boundary: the retained fraction is exp(-KL), a decay per unit of '
                   'KL. It differs from C1 in object (BatchNorm running statistics, not optimiser moments) and in quantity '
                   '(the KL between the running and the new batch feature statistics, i.e. the input distribution seen at '
                   'a layer, not the learner\'s own step between successive predictive distributions on a probe set).'},
    {'id': 'c1:26', 'tag': 'c1', 'reading': 'close', 'reading_by': RB,
     'source': 'Ramesh, Lewandowski, Schmidhuber, "Learning to Forget: Continual Learning with Adaptive Weight Decay" '
               '(FADE; arXiv:2604.27063)',
     'version': 'v1, 29 Apr 2026', 'url': 'https://arxiv.org/abs/2604.27063v1',
     'quote': ['a fixed scalar weight decay drives this forgetting uniformly over time and uniformly across all parameters',
               'We introduce Forgetting through Adaptive Decay (FADE), which adapts per-parameter weight decay rates online '
               'via approximate meta-gradient descent.'],
     'raw_file': 'c1/txt/pdf_2604.27063v1.txt',
     'agent_note': 'Close: a forgetting timescale freed from the uniform clock and adapted online in a continual stream; '
                   'the rate is set by meta-gradient on the loss, and the object is weight decay, not optimiser moments.'},
    # ------------------------------------------------ bears: evidence on stale memory and the step clock
    {'id': 'c1:20', 'tag': 'c1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Sahu, Sarkar, Hogan, Wells, "Adapt or Forget: Provable Tradeoffs Between Adam and SGD in Nonstationary Optimization" '
               '(arXiv:2605.04269)',
     'version': 'v2, 11 Sep 2026', 'url': 'https://arxiv.org/abs/2605.04269v2',
     'quote': ['in drift-dominated regimes, stale first-moment information and preconditioner perturbations can enlarge '
               'Adam’s tracking guarantee, potentially allowing vanilla SGD to attain a smaller tracking error.',
               'Hence larger 𝛽1 and 𝛽2 improve temporal averaging and preconditioner stability, respectively, at the cost of '
               'slower response to nonstationarity.'],
     'raw_file': 'c1/txt/pdf_2605.04269v2.txt',
     'agent_note': 'Bears: the noise-drift trade-off of fixed Adam memories that C1 would resolve by letting the memory '
                   'length follow the change; no adaptive beta is proposed.'},
    {'id': 'c1:21', 'tag': 'c1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Obis (supervisors Viering, van de Ven), "Reaching for Resilience: Understanding How Optimizers Affect the '
               'Stability Gap in Continual Learning" (BSc thesis, TU Delft, 22 June 2025)',
     'version': 'TU Delft repository PDF (fetched 2026-09-30)',
     'url': 'https://repository.tudelft.nl/file/File_356b427b-c259-4ad5-b47c-16cc7c234716',
     'quote': ['Our results reveal that increasing momentum amplifies the steepness and depth of the gap, while shortening '
               'its duration.',
               'RMSprop proves most effective in reducing the magnitude and duration of the drop while maintaining high '
               'overall performance.'],
     'raw_file': 'c1/txt/tudelft_obis_2025.txt',
     'agent_note': 'Bears: the momentum timescale changes the depth and duration of the stability gap in opposite '
                   'directions (rotated-digit tasks), so a C1 prediction on the dip alone is incomplete; a student thesis.'},
    {'id': 'c1:22', 'tag': 'c1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Kang, Lee, "Continual Learning of Numerous Tasks from Long-tail Distributions" (arXiv:2404.02754)',
     'version': 'v1, 3 Apr 2024', 'url': 'https://arxiv.org/abs/2404.02754v1',
     'quote': ['Existing works usually reset the optimizer states, i.e. a new instance of the optimizer is initialized every '
               'time',
               'We propose a method that reuses the optimizer states in Adam by maintaining a weighted average of the second '
               'moments from previous tasks.'],
     'raw_file': 'c1/txt/pdf_2404.02754v1.txt',
     'agent_note': 'Bears (the opposite direction): keeping Adam\'s second moments across tasks reduced forgetting, where '
                   'C1 would forget them faster at a switch; boundaries supplied.'},
    {'id': 'c1:23', 'tag': 'c1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Everett, Qiu, "Optimizer Memory Schedules for Outscaling the Overtraining Axis" (arXiv:2609.04577)',
     'version': 'v1, 4 Sep 2026', 'url': 'https://arxiv.org/abs/2609.04577v1',
     'quote': ['Fixed-momentum optimizers use a coefficient that keeps this timescale constant across training steps, '
               'whereas scheduled-memory optimizers vary it throughout training.',
               'An effective optimization clock is a reparameterization of training time that measures how much progress '
               'the optimizer has made through the problem’s spectrum, rather than simply counting updates.'],
     'raw_file': 'c1/txt/pdf_2609.04577v1.txt',
     'agent_note': 'Bears: optimiser memory as a timescale, scheduled against training time, and an "effective clock" '
                   '(accumulated learning rate) in the analysis; stationary pre-training, and the schedule is set in '
                   'advance, not by the learner\'s change.'},
    {'id': 'c1:24', 'tag': 'c1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Li, Fan, Tran, Yong, "Backpropagated Output Momentum: Relocating Optimizer History from Parameters to Task '
               'Space" (BOM; arXiv:2609.36738)',
     'version': 'v1, 29 Sep 2026', 'url': 'https://arxiv.org/abs/2609.36738v1',
     'quote': ['stores a compact moving average of prediction errors at the model output and reprojects that history through '
               'the current network at every step.'],
     'raw_file': 'c1/txt/pdf_2609.36738v1.txt',
     'agent_note': 'Bears: optimiser history kept in output (function) space rather than parameter space; its moving '
                   'average still decays per step.'},
]
