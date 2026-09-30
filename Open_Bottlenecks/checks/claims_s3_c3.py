"""Claims for OB1 stage 3 (Open_Bottlenecks/DECLARATION.md), candidate C3 of Open_Bottlenecks/CRR_READING.md:
arc-triggered consolidation in boundary-free (task-free) continual learning. Transcribed from the dossier
docs/citations/ob1_s3_c3_2026-09-30.md (sources fetched 2026-09-30; extracted texts held outside the repository under
/tmp/claude-0/ob1_s3/, named in `raw_file` relative to that root). Every quote is copied from a dossier blockquote.

The mechanism graded (CRR_READING.md, C3): consolidate (freeze prompts or experts, snapshot, anchor a regulariser, add an
expert) when the learner's OWN accumulated change since the last consolidation (KL / Fisher / function / parameter
distance, i.e. the arc since the last cut) crosses a unit, instead of at supplied boundaries, "every I steps", or at shifts
detected over a fixed batch window or sample budget.

'reading' is decided by the stage-3 agent from the quote, for the investigator's review ('reading_by'). Readings (fixed by
the stage-3 brief before the search):
  states       the source publishes the mechanism: a consolidation trigger, timescale or budget indexed by the learner's
               own accumulated change (KL, function, parameter or Fisher distance, or its per-step equivalent), used for
               consolidation (freeze, snapshot, anchor, add an expert) in a stream;
  close        a change-driven trigger or timescale, but with a different quantity (loss value, loss deviation, data
               distribution, gradient/Fisher of the incoming data) or for a different purpose (reset, communication,
               merge gating, regulariser strength, compute allocation);
  bears        relevant evidence (the frontier's triggers named, a survey of detector families, a clock-indexed
               alternative, a detector comparison) that neither publishes nor negates the mechanism;
  contradicts  the source shows the mechanism fails or is inferior.
Grade rule (the brief): REDUNDANT if any 'states'; PARTLY REDUNDANT if any 'close'; else NOT FOUND IN THE SWEEP.
"""

RB = "stage-3 agent; for the investigator's review"

CLAIMS = [
    # ---------------------------------------------------------------- A. task-free consolidation triggered by the loss
    {'id': 'c3:0', 'tag': 'c3', 'reading': 'close', 'reading_by': RB,
     'source': 'Aljundi, Kelchtermans, Tuytelaars, "Task-Free Continual Learning" (arXiv:1812.03596; CVPR 2019)',
     'version': 'v3, 19 Aug 2019', 'url': 'https://arxiv.org/abs/1812.03596v3',
     'quote': ['In the online case, the data is streaming without knowledge of a task’s start or end (i.e. when '
               'distribution shifts occur). So we need a mechanism to determine when to update the importance weights.',
               'Whenever the model is in such a stable area, it’s a good time to consolidate the knowledge by updating '
               'the importance weights.',
               'We monitor the mean and the variance of the losses in this window and trigger an importance weight '
               'update whenever they are both lower than a given threshold.'],
     'raw_file': 'c3/txt/1812.03596v3.txt',
     'agent_note': 'Close: the founding task-free consolidation trigger. Consolidation (MAS importance update, anchoring) '
                   'is triggered by the learner\'s own loss (a plateau after a peak), inside a sliding window of losses: '
                   'a change-driven trigger with a different quantity (loss level and variance, not accumulated '
                   'KL/parameter distance since the last consolidation).'},
    {'id': 'c3:1', 'tag': 'c3', 'reading': 'close', 'reading_by': RB,
     'source': 'Wei, Li, Marculescu, "Online-LoRA: Task-free Online Continual Learning via Low Rank '
               'Adaptation" (arXiv:2411.05663; WACV 2025)',
     'version': 'v1, 8 Nov 2024', 'url': 'https://arxiv.org/abs/2411.05663v1',
     'quote': ['There brings the need for a mechanism to determine when to initialize the new LoRA parameters.',
               'At these plateaus, it is best to consolidate the learned knowledge by freezing the current LoRA weights '
               'and initializing a pair of new, trainable LoRA parameters.',
               'A plateau is identified when both metrics fall below a predefined threshold'],
     'raw_file': 'c3/txt/2411.05663v1.txt',
     'agent_note': 'Close: exactly C3\'s action (freeze the current adapter, add a new one, re-estimate importance) in a '
                   'task-free stream, but the trigger is Aljundi-style loss plateaus over a sliding loss window, not '
                   'the accumulated own change.'},
    {'id': 'c3:2', 'tag': 'c3', 'reading': 'close', 'reading_by': RB,
     'source': 'Zhu, Majzoubi, Jain, Choromanska, "TAME: Task Agnostic Continual Learning using Multiple Experts" (arXiv:2210.03869; '
               'CVPR 2024 Workshop on Continual Learning in Computer Vision)',
     'version': 'v2, 2 Jun 2024', 'url': 'https://arxiv.org/abs/2210.03869v2',
     'quote': ['the strategy for switching between tasks hinges on an extremely simple observation that for each new '
               'coming task there occurs a statistically-significant deviation in the value of the loss function that '
               'marks the onset of this new task.',
               'a smoothed version of the loss is calculated, through an exponentially weighted moving average (EWMA)'],
     'raw_file': 'c3/txt/2210.03869v2.txt',
     'agent_note': 'Close: expert switching/creation (a consolidation of the previous expert) triggered by a significant '
                   'deviation of the EWMA-smoothed loss; quantity is the loss, not the accumulated change.'},
    {'id': 'c3:3', 'tag': 'c3', 'reading': 'close', 'reading_by': RB,
     'source': 'Caccia, Rodríguez, Ostapenko et al., "Online Fast Adaptation and Knowledge Accumulation: a New Approach '
               'to Continual Learning" (OSAKA / Continual-MAML; arXiv:2003.05856; NeurIPS 2020)',
     'version': 'v3, 20 Jan 2021', 'url': 'https://arxiv.org/abs/2003.05856v3',
     'quote': ['The simple yet effective context shift detection mechanism works by monitoring the difference in loss '
               'with respect to the previous task and is controlled by a hyperparameter γ',
               'One can think of the update after the task boundary detection as a knowledge consolidation phase.'],
     'raw_file': 'c3/txt/2003.05856v3.txt',
     'agent_note': 'Close: a self-detected boundary triggers a knowledge-consolidation phase (slow-weight update), '
                   'detected from a loss difference against a threshold γ; quantity is the loss.'},
    # ---------------------------------------------------------------- B. triggers on the data (window, novelty, discrepancy)
    {'id': 'c3:4', 'tag': 'c3', 'reading': 'close', 'reading_by': RB,
     'source': 'Han, Zhang, Zhu, Guo, "Unifying Detection and Adaptation in Task-Free Continual Learning" (FiUni; '
               'arXiv:2608.27070; Findings of EMNLP 2026)',
     'version': 'v1, 27 Aug 2026', 'url': 'https://arxiv.org/abs/2608.27070v1',
     'quote': ['matching the Fisher principal subspace of each incoming batch window with historical subspaces.',
               'This maximum similarity reflects whether the current data can be explained by existing Fisher subspaces.',
               'When sn,max < τlow, FiUni considers the current data geometrically distinct from historical phases and '
               'allocates a new LoRA subspace using the current Fisher principal subspace'],
     'raw_file': 'c3/txt/2608.27070v1.txt',
     'agent_note': 'Close: self-detected boundaries in Fisher geometry trigger new/expand/reuse of LoRA subspaces, but '
                   'the Fisher is that of each incoming data window (K-FAC factors of the window), compared with stored '
                   'subspaces: a data-side signal over a count-indexed window, not the learner\'s accumulated change.'},
    {'id': 'c3:5', 'tag': 'c3', 'reading': 'close', 'reading_by': RB,
     'source': 'Wang, Lu, Yao, Gong, "Self-Expansion of Pre-trained Models with Mixture of Adapters for Continual '
               'Learning" (SEMA; arXiv:2403.18886; venue not verified on the day)',
     'version': 'v3, 27 Mar 2025', 'url': 'https://arxiv.org/abs/2403.18886v3',
     'quote': ['an expansion signal at layer l is triggered when significantly new patterns are identified.',
               'When a new task t arrives, the method scans all samples in the first epoch to decide whether to expand '
               'the model.'],
     'raw_file': 'c3/txt/2403.18886v3.txt',
     'agent_note': 'Close: expansion (a new adapter) triggered by a distribution-shift indicator (z-score of '
                   'representation-descriptor reconstruction error); a data-novelty quantity, and the scan is made at '
                   'task arrival (task-oriented), not boundary-free.'},
    {'id': 'c3:6', 'tag': 'c3', 'reading': 'close', 'reading_by': RB,
     'source': 'Ye, Bors, "Task-Free Continual Learning via Online Discrepancy Distance Learning" (ODDL; '
               'arXiv:2210.06579; NeurIPS 2022)',
     'version': 'v1, 12 Oct 2022', 'url': 'https://arxiv.org/abs/2210.06579v1',
     'quote': ['However, the expansion criterion used by these approaches relies on the change of the loss when training '
               'each time, which does not have any theoretical guarantees.',
               'If the current memory distribution PMi is sufficiently different from each component (satisfies Eq. '
               '(15)), G will add a new component to preserve the knowledge of the current memory Mi'],
     'raw_file': 'c3/txt/2210.06579v1.txt',
     'agent_note': 'Close: expansion (freeze the old components, add one) triggered by a discrepancy distance between the '
                   'memory distribution and each component, against a threshold λ; a distribution-discrepancy quantity, '
                   'not the learner\'s own accumulated change. Also attests that CURL/CN-DPM expansion uses the change of '
                   'the loss.'},
    {'id': 'c3:7', 'tag': 'c3', 'reading': 'close', 'reading_by': RB,
     'source': 'Kirkpatrick, Pascanu, Rabinowitz et al., "Overcoming catastrophic forgetting in neural networks" (EWC; '
               'arXiv:1612.00796; venue not verified on the day), Atari experiment',
     'version': 'v2, 25 Jan 2017', 'url': 'https://arxiv.org/abs/1612.00796v2',
     'quote': ['we allow for the addition of new generative models if they explain recent data better than the existing '
               'pool of models by using a training procedure inspired by the forget me not process',
               'In order to apply EWC, we compute the Fisher information matrix at each task switch.',
               'We partition time into windows of a particular width W.'],
     'raw_file': 'c3/txt/1612.00796v2.txt',
     'agent_note': 'Close: consolidation (Fisher + anchor) at inferred task switches, the switches inferred by a '
                   'generative model of the observations over time windows of width W: a data-likelihood trigger on a '
                   'window clock.'},
    {'id': 'c3:8', 'tag': 'c3', 'reading': 'close', 'reading_by': RB,
     'source': 'Titsias, Schwarz, Matthews, Pascanu, Teh, "Functional Regularisation for Continual Learning with '
               'Gaussian Processes" (FRCL; arXiv:1901.11356; ICLR 2020)',
     'version': 'v4, 11 Feb 2020', 'url': 'https://arxiv.org/abs/1901.11356v4',
     'quote': ['This can be achieved by using a divergence measure between distributions such as the symmetrised KL '
               'divergence,',
               'When each score ℓi is close to zero this indicate that the input distribution has changed so that a task '
               'switch can be detected.',
               'Thus our idea has close links to Bayesian surprise (Itti & Baldi, 2006).'],
     'raw_file': 'c3/txt/1901.11356v4.txt',
     'agent_note': 'Close: a KL in the learner\'s function space (GP prior vs posterior predictive at each new input) '
                   'detects task boundaries for functional consolidation; but it scores the novelty of each input '
                   '(posterior falls back to prior far from data), per minibatch, not the change the learner has '
                   'accumulated since the last consolidation.'},
    # ---------------------------------------------------------------- C. own-change quantities, other purposes
    {'id': 'c3:9', 'tag': 'c3', 'reading': 'close', 'reading_by': RB,
     'source': 'Mishra, "RDumb++: Drift-Aware Continual Test-Time Adaptation" (arXiv:2601.15544; also OpenReview TTU at '
               'ICLR 2026 and CAO poster)',
     'version': 'v1, 22 Jan 2026', 'url': 'https://arxiv.org/abs/2601.15544v1',
     'quote': ['RDumb depends on a fixed reset interval (e.g., every 1000 steps), which is fundamentally non-adaptive.',
               'KL divergence quantifies how much the model’s predictive belief has shifted relative to its historical '
               'expectation.',
               'These mechanisms allow the model to detect when accumulated adaptation becomes harmful and to recover '
               'before prediction collapse occurs.'],
     'raw_file': 'c3/txt/2601.15544v1.txt',
     'agent_note': 'Close (nearest in quantity): replaces a clock ("every 1000 steps") by a KL on the model\'s own '
                   'predictive distribution; but the score is a standardized per-sample KL spike against a reference '
                   '(EMA z-score > k), not an accumulated arc, and the action is a reset (C2\'s purpose) in test-time '
                   'adaptation, not consolidation.'},
    {'id': 'c3:10', 'tag': 'c3', 'reading': 'close', 'reading_by': RB,
     'source': 'Hoang, Vo, Do, "Persistent Test-time Adaptation in Recurring Testing Scenarios" (PeTTA; '
               'arXiv:2311.18193; NeurIPS 2024)',
     'version': 'v4, 2 Nov 2024', 'url': 'https://arxiv.org/abs/2311.18193v4',
     'quote': ['Sensing the Divergence of θt. We first equip PeTTA with a mechanism for measuring its divergence from θ0.',
               'the Mahalanobis distance of the first moment of the feature embedding vectors is compared.',
               'a pair of (λt, αt) is adaptively chosen at each step'],
     'raw_file': 'c3/txt/2311.18193v4.txt',
     'agent_note': 'Close: the learner\'s own accumulated divergence from its anchor sets the anchor-regulariser weight '
                   'λt and the EMA update rate αt continuously (own change indexes a timescale and a regulariser); but '
                   'the anchor is fixed at θ0 and nothing is triggered (no new snapshot, freeze or expert).'},
    {'id': 'c3:11', 'tag': 'c3', 'reading': 'close', 'reading_by': RB,
     'source': 'Hoy, Celik, "STABLE: Gated Continual Learning for Large Language Models" (arXiv:2510.16089)',
     'version': 'v1, 17 Oct 2025', 'url': 'https://arxiv.org/abs/2510.16089v1',
     'quote': ['Each adapter merge is treated as a candidate update that must pass through a gate,',
               'KL divergence, quantifying distributional shift between the base and adapted models.',
               'If the gate threshold is exceeded, the update is rescaled through a LoRA specific clipping procedure or '
               'rejected.'],
     'raw_file': 'c3/txt/2510.16089v1.txt',
     'agent_note': 'Close: a KL budget on the learner\'s own change (base vs adapted) in sequential LoRA merging; but '
                   'it gates, clips or rejects each merge, rather than triggering a consolidation when accumulated '
                   'change crosses a unit, and the edits arrive already segmented.'},
    {'id': 'c3:12', 'tag': 'c3', 'reading': 'close', 'reading_by': RB,
     'source': 'Liu, Diao, Lu et al., "ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries in Large '
               'Language Models" (arXiv:2505.24864)',
     'version': 'v1, 30 May 2025', 'url': 'https://arxiv.org/abs/2505.24864v1',
     'quote': ['as training progresses, the KL term may increasingly dominate the loss, leading to diminishing policy '
               'updates.',
               'Periodically, we hard-reset the reference policy πref to a more recent snapshot of the online policy πθ, '
               'and reinitialize the optimizer states.',
               'When validation performance stagnates or degrades, we perform a hard reset of the reference model and '
               'optimizer.'],
     'raw_file': 'c3/txt/2505.24864v1.txt',
     'agent_note': 'Close: re-anchoring the KL regulariser at a snapshot of the online policy (C3\'s "snapshot / anchor '
                   'a regulariser") in a long stream, motivated by accumulated KL; but triggered periodically or by '
                   'validation stagnation, not by the accumulated own change crossing a unit.'},
    {'id': 'c3:13', 'tag': 'c3', 'reading': 'close', 'reading_by': RB,
     'source': 'Kamp, Adilova, Sicking et al., "Efficient Decentralized Deep Learning by Dynamic Model Averaging" '
               '(arXiv:1807.03210; venue not verified on the day)',
     'version': 'v2, 13 Nov 2018', 'url': 'https://arxiv.org/abs/1807.03210v2',
     'quote': ['This operator only communicates when the model divergence exceeds a divergence threshold ∆.',
               'Thus, the first choice for the reference model is the average model from the last synchronization step.'],
     'raw_file': 'c3/txt/1807.03210v2.txt',
     'agent_note': 'Close (nearest in trigger structure): each learner monitors ||f_t - r||^2 <= Delta against the '
                   'snapshot taken at the last synchronization, and acts only when its own accumulated parameter '
                   'distance since that event crosses the threshold, instead of every b rounds. Different purpose '
                   '(communication / averaging, not consolidation against forgetting) and Euclidean parameter '
                   'distance, not KL arc.'},
    {'id': 'c3:14', 'tag': 'c3', 'reading': 'close', 'reading_by': RB,
     'source': 'Zehtabi, Hosseinalipour, Brinton, "Decentralized Event-Triggered Federated Learning with Heterogeneous '
               'Communication Thresholds" (arXiv:2204.03726; venue not verified on the day)',
     'version': 'v2, 23 Nov 2022', 'url': 'https://arxiv.org/abs/2204.03726v2',
     'quote': ['communication at a device is triggered once the instantaneous local model is sufficiently different than '
               'the outdated local model.'],
     'raw_file': 'c3/txt/2204.03726v2.txt',
     'agent_note': 'Close: event-triggered broadcast when the normalized parameter distance between the current model '
                   'and the last broadcast snapshot exceeds a threshold (the threshold itself decays with the iteration '
                   'count). Same trigger structure as Kamp et al.; purpose is communication.'},
    {'id': 'c3:15', 'tag': 'c3', 'reading': 'close', 'reading_by': RB,
     'source': 'Jayasinghe, Gontero, Trivedi, "When Robots Sleep: Offline Skill Consolidation for Shared-Policy Robot Learning" '
               '(arXiv:2606.17493)',
     'version': 'v1, 16 Jun 2026', 'url': 'https://arxiv.org/abs/2606.17493v1',
     'quote': ['We therefore use a wake-end proximity gate to decide when sleep should remain close to the previous '
               'consolidated checkpoint.',
               'This quantity is used only as a conservative anchoring trigger, not as a behavioral shift estimate or '
               'memory-reliability certificate.'],
     'raw_file': 'c3/txt/2606.17493v1.txt',
     'agent_note': 'Close: a parameter distance to stored wake-end snapshots (c_i = ||theta - theta_wake_i||_2) '
                   'triggers anchoring to the previous consolidated checkpoint; but it is evaluated at supplied skill '
                   'boundaries (sleep after each skill) and switches the anchor on when the distance is small.'},
    {'id': 'c3:16', 'tag': 'c3', 'reading': 'close', 'reading_by': RB,
     'source': 'Seo, Koh, Choi et al., "Budgeted Online Continual Learning by Adaptive Layer Freezing and Frequency-based '
               'Sampling" (arXiv:2410.15143; ICLR 2025 Spotlight)',
     'version': 'v2, 16 Mar 2025', 'url': 'https://arxiv.org/abs/2410.15143v2',
     'quote': ['we propose ‘adaptive layer freezing’, which chooses the best layers to freeze by maximizing the Fisher '
               'Information (FI) gained by the model for each batch, given a fixed computation budget.',
               'we propose to freeze layers that learn little information per computational cost by measuring '
               '‘information’ (I) gained by each layer during training.'],
     'raw_file': 'c3/txt/2410.15143v2.txt',
     'agent_note': 'Close: freezing driven by the Fisher information each batch gives the learner (a per-step own-change '
                   'proxy); but the decision is per mini-batch compute allocation (skip updating layers), not '
                   'consolidation when the accumulated change since the last consolidation crosses a unit.'},
    # ---------------------------------------------------------------- D. bears
    {'id': 'c3:17', 'tag': 'c3', 'reading': 'bears', 'reading_by': RB,
     'source': 'Lee, Ha, Zhang, Teh, Kim, "A Neural Dirichlet Process Mixture Model for Task-Free Continual Learning" '
               '(CN-DPM; arXiv:2001.00689; ICLR 2020)',
     'version': 'v2, 14 Jan 2020', 'url': 'https://arxiv.org/abs/2001.00689v2',
     'quote': ['Once the STM reaches its maximum capacity M, we stop the data inflow for a while and train a new expert '
               'with the data in the STM for multiple epochs until convergence. We call this procedure sleep phase.'],
     'raw_file': 'c3/txt/2001.00689v2.txt',
     'agent_note': 'Bears: the canonical count-indexed consolidation in task-free CL (a new expert when a buffer of '
                   'novel points reaches M samples), the frontier assumption C3 denies.'},
    {'id': 'c3:18', 'tag': 'c3', 'reading': 'bears', 'reading_by': RB,
     'source': 'Aguilar, Zainal, Kavehei, "Metaplasticity as adaptive gradient preconditioning for incremental learning" '
               '(SynGAP; arXiv:2608.14634)',
     'version': 'v1, 27 Jul 2026', 'url': 'https://arxiv.org/abs/2608.14634v1',
     'quote': ['Unlike methods [...] compute importance metrics at the task boundary, SynGAP maintains a continuous '
               'estimate of parameter importance.',
               'where α ∈[0, 1) is the metaplastic retention rate, and Ft(θ) is the instantaneous Fisher information '
               'evaluated on the current batch.'],
     'raw_file': 'c3/txt/2608.14634v1.txt',
     'agent_note': 'Bears: the other boundary-free route, removing the trigger altogether by continuous consolidation '
                   'with a per-step EMA of the Fisher (a step-clock timescale).'},
    {'id': 'c3:19', 'tag': 'c3', 'reading': 'bears', 'reading_by': RB,
     'source': 'Yuan, Sun, Luo, Chen, "LargeMonitor: Monitoring Online Task-Free Continual Learning via Large Pretrained Models" '
               '(arXiv:2606.09430; v2 withdrawn, comment "The solved problem is not siginifcant enough")',
     'version': 'v1, 8 Jun 2026 (v2, 16 Sep 2026, withdrawn)', 'url': 'https://arxiv.org/abs/2606.09430v1',
     'quote': ['Existing online TFCL paradigms primarily rely on parameter-efficient prompt tuning or dynamic structure '
               'expansion driven by training-coupled optimization dynamics, such as empirical loss fluctuations or '
               'evolving latent distances.',
               'the tuning or expansion cues in existing methods depend heavily on training-coupled dynamics (e.g., '
               'gradient-matching coefficients, empirical loss values, or evolving latent distances), which can '
               'inevitably drift or require per-dataset threshold tuning'],
     'raw_file': 'c3/txt/2606.09430v1.txt',
     'agent_note': 'Bears: a 2026 characterisation of task-free triggers as loss fluctuations, gradient matching or latent '
                   'distances, with a critique (drift, per-dataset threshold tuning) that would apply to an arc '
                   'threshold as well. Withdrawn in v2; quoted from v1.'},
    {'id': 'c3:20', 'tag': 'c3', 'reading': 'bears', 'reading_by': RB,
     'source': 'Cossu, Giannini, Ziffer et al., "A Practical Guide to Streaming Continual Learning" (arXiv:2603.01677; Neurocomputing 674, 2026)',
     'version': 'v1, 2 Mar 2026', 'url': 'https://arxiv.org/abs/2603.01677v1',
     'quote': ['Error rate-based methods, such as ADWIN [23], the Early Drift Detection Method [24], EWMA [25], and EWMA '
               'for Concept Drift Detection [26], track the online classification errors of base learners to identify '
               'noteworthy deviations.',
               'Data distribution-based approaches assess discrepancies between historical and incoming data, making '
               'them appropriate for detecting input or virtual drift.'],
     'raw_file': 'c3/txt/2603.01677v1.txt',
     'agent_note': 'Bears: the streaming-learning taxonomy of drift detectors lists error-rate and data-distribution '
                   'families (and multiple-testing ensembles); no family indexed by the learner\'s own parameter or '
                   'predictive change is named.'},
    {'id': 'c3:21', 'tag': 'c3', 'reading': 'bears', 'reading_by': RB,
     'source': 'Cheruvu, Sethi, Bhatnagar, Narava, Jha, "Boundary-Free Continual Reinforcement Learning via Online '
               'Task-Shift Detection" (OpenReview 15Vitz6Txt; Continual RL @ RLC 2026 workshop; abstract only)',
     'version': 'OpenReview note, created 30 May 2026 (full text NOT REACHED: OpenReview PDF behind a challenge)',
     'url': 'https://openreview.net/forum?id=15Vitz6Txt',
     'quote': ['Many continual reinforcement learning (CRL) methods assume that task boundaries are known, allowing '
               'transfer and consolidation to be triggered at predefined times.',
               'the statistical detector is the most reliable boundary-free trigger, achieving high detection quality '
               'with no false positives. While the implicit and hybrid detectors suffer from frequent within-task '
               'fires.',
               'learned drift detectors require stronger controls for within-task representation change.'],
     'raw_file': 'c3/txt/or_15Vitz6Txt_abstract.txt',
     'agent_note': 'Bears (a caution for C3): replacing the oracle consolidation trigger, a data-side statistical '
                   'detector beat a learner-internal prediction-error drift detector, which fired within tasks because '
                   'representations change within a task. An arc trigger also accumulates within-task change; this is '
                   'not a test of it, so not contradicts.'},
    {'id': 'c3:22', 'tag': 'c3', 'reading': 'bears', 'reading_by': RB,
     'source': 'Julian, Koh, Bifet, "Timed Dynamic Expansion for Continual Learning" (TIDE; OpenReview CA4yNpLTAU; '
               'submitted to ICLR 2026; abstract only)',
     'version': 'OpenReview note, created 20 Sep 2025 (full text NOT REACHED: OpenReview PDF behind a challenge; no '
                'arXiv version found)',
     'url': 'https://openreview.net/forum?id=CA4yNpLTAU',
     'quote': ['rigid growth schedules often expand capacity unnecessarily on stable tasks while failing to protect '
               'against interference that arises later within a task.',
               'We propose Timed Dynamic Expansion (TIDE), a method that stabilises expansion by creating adapters only '
               'at the moments they are needed'],
     'raw_file': 'c3/txt/or_CA4yNpLTAU_abstract.txt',
     'agent_note': 'Bears, possibly more: expansion timed within a task instead of on a schedule; the abstract does not '
                   'name the trigger quantity (Fisher appears only in the inference gating). If the full text triggers '
                   'on accumulated parameter/Fisher change, this would move to close or states. NOT REACHED.'},
    {'id': 'c3:23', 'tag': 'c3', 'reading': 'bears', 'reading_by': RB,
     'source': 'Basterrech, Wozniak, "Tracking changes using Kullback-Leibler divergence for the continual learning" '
               '(arXiv:2210.04865; IEEE SMC 2022)',
     'version': 'v1, 10 Oct 2022', 'url': 'https://arxiv.org/abs/2210.04865v1',
     'quote': ['This article introduces a novel method for monitoring changes in the probabilistic distribution of '
               'multi-dimensional data streams. As a measure of the rapidity of changes, we analyze the popular '
               'Kullback-Leibler divergence.'],
     'raw_file': 'c3/txt/2210.04865v1.txt',
     'agent_note': 'Bears: KL as a rate of change of the DATA stream (between chunks), for drift prediction; neither the '
                   'learner\'s own change nor a consolidation trigger.'},
]
