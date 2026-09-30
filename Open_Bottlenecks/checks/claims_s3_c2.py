"""Claims for Open_Bottlenecks/DECLARATION.md Stage 3, candidate C2 (CRR_READING.md): arc-triggered refresh for plasticity
loss under task switches (continual RL, and supervised). Transcribed from the dossier docs/citations/ob1_s3_c2_2026-09-30.md
(sources fetched 2026-09-30 through the session proxy; the extracted texts are held outside the repository under
/tmp/claude-0/ob1_s3/, named in `raw_file` relative to that root; sha256 of every fetched file in
/tmp/claude-0/ob1_s3/c2/SHA256SUMS.txt and of every search page in /tmp/claude-0/ob1_s3/c2/SHA256SUMS_search.txt).
Every quote is copied from the text that pymupdf 1.28.2 extracted from the fetched arXiv PDF, or, for OpenReview-only
entries whose PDF returned HTTP 403, from the abstract field of the OpenReview API search result (written out verbatim to
c2/src/or_<id>_abstract.txt by json.load). Whitespace is normalised and line-break hyphens may be rejoined (the verifier's
rule); nothing else is changed.

The mechanism searched (CRR_READING.md, C2; the caller's statement): a refresh (reset, shrink-perturb, soft reset or
re-initialisation) triggered when the learner's OWN accumulated change since the last refresh (KL between successive
predictive distributions on a probe set, function distance, parameter or Fisher distance, or a divergence budget) crosses
a unit, in place of a fixed clock schedule or a supplied boundary (the Oracle).

Readings (the caller's definitions, fixed before the readings were written):
  states       the source publishes the mechanism: a refresh trigger, timescale or budget indexed by the learner's own
               accumulated change (KL / function / parameter / Fisher distance, or its per-step equivalent), used for the
               named purpose (plasticity loss or refresh under task switches / non-stationarity);
  close        a change-driven refresh trigger (or timescale) on a different quantity (loss or prediction error, reward,
               input or batch-norm statistics, entropy or prediction concentration, neuron firing, evidence of new data),
               or the own-change quantity used for a different purpose or a different action;
  bears        relevant evidence (the frontier's clock or Oracle assumption stated, a clock-scheduled refresh, a result on
               resets in general) that neither publishes nor negates the mechanism;
  contradicts  a source showing the mechanism fails or is inferior.
'reading' is the stage-3 agent's, for the investigator's review ('reading_by').
"""

RB = "stage-3 agent; for the investigator's review"

CLAIMS = [
    # ------------------------------------------------------------------ close: change-triggered refresh, CTTA
    {'id': 'c2:0', 'tag': 'c2', 'reading': 'close', 'reading_by': RB,
     'source': 'Mishra, "RDumb++: Drift-Aware Continual Test-Time Adaptation" (arXiv:2601.15544; OpenReview lists it at '
               '"TTU at ICLR 2026 (Main)")',
     'version': 'v1, 22 Jan 2026', 'url': 'https://arxiv.org/abs/2601.15544',
     'quote': ['RDumb depends on a fixed reset interval (e.g., every 1000 steps), which is fundamentally non-adaptive.',
               'Can we detect distribution drift during inference, and reset the model only when necessary?',
               'For each incoming sample, we compute the KL divergence between the current distribution pt and the '
               'reference qt:',
               'KL divergence quantifies how much the model’s predictive belief has shifted relative to its historical '
               'expectation.',
               'Upon detecting drift, RDumb++ applies one of two reset strategies depending on the model variant.',
               'RDumb++ triggers a reset exactly when a statistically significant deviation is detected.'],
     'raw_file': 'c2/src/pdf_2601.15544v1.txt',
     'agent_note': 'The closest in form: a full reset or a soft reset toward the initial parameters (theta <- lambda*theta0 '
                   '+ (1-lambda)*theta), triggered by a KL divergence of the model\'s predictive distribution, replacing '
                   'a fixed reset clock. Close, not states: (i) the trigger is a per-sample z-score of KL against an '
                   'EMA reference (a change-point spike detector), not the accumulated own change since the last reset '
                   'crossing a unit; (ii) the purpose is collapse under continual test-time adaptation, not plasticity '
                   'loss under task switches in RL. It shows a KL-of-own-predictions trigger for resets is published.'},
    {'id': 'c2:1', 'tag': 'c2', 'reading': 'close', 'reading_by': RB,
     'source': 'Lim, Hwang, Lee, "When and Where to Reset Matters for Long-Term Test-Time Adaptation" (ASR; '
               'arXiv:2603.03796; ICLR 2026)',
     'version': 'v1, 4 Mar 2026', 'url': 'https://arxiv.org/abs/2603.03796',
     'quote': ['However, their periodic resets lead to suboptimal adaptation, as they occur independently of the actual '
               'risk of collapse.',
               'We introduce an adaptive reset scheme that triggers a reset only when a high risk of collapse is detected.',
               'Others trigger resets only when extremely high predictive confidence (Niu et al., 2023) or severe '
               'distribution shifts from the source domain (Wang et al., 2024) are detected.',
               'adjusting the regularization coefficient based on parameter divergence from the pre-trained state '
               '(Hoang et al., 2024)'],
     'raw_file': 'c2/src/pdf_2603.03796v1.txt',
     'agent_note': 'Close: an adaptive reset trigger replacing a periodic one, but the quantity is prediction '
                   'concentration (entropy of the batch-mean prediction) against its EMA, not accumulated own change; '
                   'purpose is TTA collapse. Its related work names three further triggers (confidence, SAR; shift from '
                   'the source domain, DA-TTA; parameter divergence from the pre-trained state used to set a '
                   'regulariser, PeTTA), none of them an accumulated-arc unit.'},
    {'id': 'c2:2', 'tag': 'c2', 'reading': 'close', 'reading_by': RB,
     'source': 'Wang, Tong, Lan, Wang, Zhu, Chen et al., "Adaptive and Balanced Re-initialization for Long-timescale '
               'Continual Test-time Domain Adaptation" (ABR; arXiv:2602.06328; ICASSP 2026)',
     'version': 'v1, 6 Feb 2026', 'url': 'https://arxiv.org/abs/2602.06328',
     'quote': ['ABR performs weight re-initialization using adaptive intervals. The adaptive interval is determined based '
               'on the change in label flip.',
               'We refer to the predicted class differences between the two models as the label flip [9, 10] at the '
               'current time.',
               'If we perform re-initialization immediately after the sharp increase in the label flip, performance '
               'would be better preserved during later adaptation.',
               'resets the model by a fixed time interval tuned using the related validation dataset.'],
     'raw_file': 'c2/src/pdf_2602.06328v1.txt',
     'agent_note': 'Borderline close/states; graded close. The trigger quantity IS the learner\'s own per-step functional '
                   'change: the label flip between the current model and the model at the previous step (weighted by '
                   'confidence, EMA-smoothed), which is a discrete per-step analogue of the arc. The re-initialisation '
                   'interval is set by it, replacing a tuned fixed interval. Close, not states, because (i) the rule '
                   'fires on the SLOPE of a rise from the running minimum (change-point on the per-step change), not on '
                   'the accumulated change since the last refresh crossing a unit, and (ii) the purpose is long-term '
                   'CTTA performance (error accumulation), not plasticity loss under task switches in RL.'},
    {'id': 'c2:3', 'tag': 'c2', 'reading': 'close', 'reading_by': RB,
     'source': 'Niloy, Ahmed, Raychaudhuri, Oymak, Roy-Chowdhury, "Effective Restoration of Source Knowledge in '
               'Continual Test Time Adaptation" (arXiv:2311.04991; WACV 2024)',
     'version': 'v1, 8 Nov 2023', 'url': 'https://arxiv.org/abs/2311.04991',
     'quote': ['Previous research has demonstrated the benefits of resetting the model to its original parameters when a '
               'domain change occurs, but these approaches rely on an oracle with additional domain knowledge for '
               'detecting such changes.',
               'this paper introduces an unsupervised domain change detection method that is capable of identifying '
               'domain shifts in dynamic environments and subsequently resets the model parameters to the original '
               'source pre-trained values.',
               'As the model encounters more test batches from the same domain, the running statistics gradually align '
               'with the statistics of the domain, resulting in a decrease in the KL divergence.'],
     'raw_file': 'c2/src/pdf_2311.04991v1.txt',
     'agent_note': 'Close: exactly the Oracle-replacement move (a reset at a self-detected domain change instead of an '
                   'oracle boundary), but the detector watches a KL between batch-norm (input feature) statistics, a '
                   'property of the data stream, not the learner\'s accumulated own change; purpose CTTA.'},
    {'id': 'c2:4', 'tag': 'c2', 'reading': 'close', 'reading_by': RB,
     'source': 'Hoang, Vo, Do, "Persistent Test-time Adaptation in Recurring Testing Scenarios" (PeTTA; '
               'arXiv:2311.18193; NeurIPS 2024)',
     'version': 'v4, 2 Nov 2024', 'url': 'https://arxiv.org/abs/2311.18193',
     'quote': ['which senses when the model is diverging towards collapse and adjusts the adaptation strategy',
               'We first equip PeTTA with a mechanism for measuring its divergence from θ0.',
               'Other studies explore reset (recovering the initial model parameters) strategies [59, 45], periodically '
               'or upon the running entropy loss approaches a threshold [41].',
               'Our PeTTA is reset-free by achieving an adaptable continual test-time training.'],
     'raw_file': 'c2/src/pdf_2311.18193v4.txt',
     'agent_note': 'Close (different action): the quantity is the learner\'s own divergence from its initial state '
                   '(Mahalanobis distance of class-wise feature means from the source), which is own-change-indexed, '
                   'but it continuously scales a regulariser and the EMA rate; it does not trigger a refresh, and is '
                   'explicitly reset-free. Purpose: TTA collapse.'},
    # ------------------------------------------------------------------ close: change-triggered refresh, plasticity / RL
    {'id': 'c2:5', 'tag': 'c2', 'reading': 'close', 'reading_by': RB,
     'source': 'Galashov, Titsias, György, Lyle, Pascanu, Teh et al., "Non-Stationary Learning of Neural Networks with '
               'Automatic Soft Parameter Reset" (arXiv:2411.04034; NeurIPS 2024)',
     'version': 'v1, 6 Nov 2024', 'url': 'https://arxiv.org/abs/2411.04034',
     'quote': ['strategies often involve hard resets based on heuristics like detecting dormant units [47], assessing '
               'neuron utility [13, 12], or simply after a fixed number of steps [43].',
               'The amount by which the parameters move towards the initialization and the amount of learning rate '
               'increase are controlled by the drift parameters which are learned online.',
               'A suitable choice of an objective to select γt is predictive likelihood which quantifies the '
               'probability of new data under our current parameters and drift model.'],
     'raw_file': 'c2/src/pdf_2411.04034v1.txt',
     'agent_note': 'Close: a data-driven soft reset toward the initialisation for plasticity loss under non-stationarity '
                   '(supervised and off-policy RL), with no clock and no boundary; but the reset amount is chosen by the '
                   'predictive likelihood of the NEXT batch (surprise of new data), not by the accumulated own change '
                   'since the last reset. Same purpose, different quantity.'},
    {'id': 'c2:6', 'tag': 'c2', 'reading': 'close', 'reading_by': RB,
     'source': 'Su, Dai, Zhang, "Revisiting Clustering of Neural Bandits: Selective Reinitialization for Mitigating Loss '
               'of Plasticity" (SeRe; arXiv:2506.12389; KDD 2025)',
     'version': 'v3, 2 Dec 2025', 'url': 'https://arxiv.org/abs/2506.12389',
     'quote': ['the adaptive change detection mechanism adjusts the reinitialization frequency according to the degree of '
               'non-stationarity',
               'we maintain a change detection statistic using the Page-Hinkley (PH) method [25, 46], a variant of the '
               'Cumulative Sum (CUSUM) test.',
               'This design accumulates the absolute prediction error, ensuring that we detect both underestimation and '
               'overestimation of rewards'],
     'raw_file': 'c2/src/pdf_2506.12389v3.txt',
     'agent_note': 'Close: re-initialisation for plasticity loss whose rate is driven by an ACCUMULATED statistic crossing '
                   'a threshold (Page-Hinkley / CUSUM) - structurally the arc-crosses-a-unit rule - but the accumulated '
                   'quantity is the absolute reward-prediction error, not the learner\'s own change; neural bandits, '
                   'not continual RL chains.'},
    {'id': 'c2:7', 'tag': 'c2', 'reading': 'close', 'reading_by': RB,
     'source': 'Farias, Jozefiak, "Self-Normalized Resets for Plasticity in Continual Learning" (SNR; arXiv:2410.20098; '
               'ICLR 2025 poster per OpenReview G82uQztzxl)',
     'version': 'v3, 28 Sep 2025', 'url': 'https://arxiv.org/abs/2410.20098',
     'quote': ['resetting a neuron’s weights when evidence suggests its firing rate has effectively dropped to zero',
               'In contrast to SNR, existing reset-criteria define a single reset-threshold or reset-frequency for a '
               'neural network.'],
     'raw_file': 'c2/src/pdf_2410.20098v3.txt',
     'agent_note': 'Close: an evidence-triggered (hypothesis-test) per-neuron reset for plasticity loss, in place of a '
                   'fixed reset frequency; the quantity is a neuron\'s inter-firing time, not accumulated own change.'},
    {'id': 'c2:8', 'tag': 'c2', 'reading': 'close', 'reading_by': RB,
     'source': 'Cheruvu, Sethi, Bhatnagar, Narava, Jha, "Boundary-Free Continual Reinforcement Learning via Online '
               'Task-Shift Detection" (OpenReview 15Vitz6Txt, Continual RL @ RLC 2026; PDF NOT REACHED, HTTP 403; '
               'not found on arXiv by title)',
     'version': 'OpenReview abstract as returned by the API search on 2026-09-30', 'url':
         'https://openreview.net/forum?id=15Vitz6Txt',
     'quote': ['Many continual reinforcement learning (CRL) methods assume that task boundaries are known, allowing '
               'transfer and consolidation to be triggered at predefined times.',
               'We replace the oracle with an online Task-Shift Detection Module and compare three trigger mechanisms: '
               'a Sliced-Wasserstein (Kolmogorov-Smirnov) statistical detector, an implicit detector based on '
               'prediction-error drift in a dual-head Task-Signature Network, and a hybrid finite-state cascade.',
               'While the implicit and hybrid detectors suffer from frequent within-task fires.'],
     'raw_file': 'c2/src/or_15Vitz6Txt_abstract.txt',
     'agent_note': 'Close: replaces the oracle boundary in continual RL with a self-detected trigger (the frontier '
                   'assumption C2 denies), on MinAtar; but the triggers are an input-distribution test and a '
                   'prediction-error drift detector, and they gate warm-up/integration (the WIP version adds reset), '
                   'not an own-change arc. Its finding that the learned detector fires within tasks is a warning for any '
                   'trigger on the learner\'s own change, which also moves within a task.'},
    {'id': 'c2:9', 'tag': 'c2', 'reading': 'close', 'reading_by': RB,
     'source': 'Nonaka, Ambrozak, Miskala-Dinc, Ercole, Prins, "Efficient Restarts in Non-Stationary Model-Free '
               'Reinforcement Learning" (arXiv:2510.11933; ARLET workshop at NeurIPS 2025)',
     'version': 'v1, 13 Oct 2025', 'url': 'https://arxiv.org/abs/2510.11933',
     'quote': ['scheduled restarts, in which restarts occur only at predefined timings, regardless of the incompatibility '
               'of the policy with the current environment dynamics.',
               'we introduce adaptive restarts, which detect change in the environment by looking at cumulative reward.',
               'worst-case environments can be constructed where these adaptive restarts will perform worse than '
               'scheduled ones.'],
     'raw_file': 'c2/src/pdf_2510.11933v1.txt',
     'agent_note': 'Close: RL restarts triggered by detected change instead of a schedule (tabular RestartQ-UCB), on a '
                   'reward quantity, for dynamic regret rather than network plasticity. Also bears: the authors note '
                   'adaptive restarts can lose to scheduled ones in constructed environments.'},
    {'id': 'c2:10', 'tag': 'c2', 'reading': 'close', 'reading_by': RB,
     'source': 'Li, Boyd, Smyth, Mandt, "Detecting and Adapting to Irregular Distribution Shifts in Bayesian Online '
               'Learning" (arXiv:2012.08101; NeurIPS 2021)',
     'version': 'v3, 26 Oct 2021', 'url': 'https://arxiv.org/abs/2012.08101',
     'quote': ['is detected–the model partially erases the information of past model updates by tempering to facilitate '
               'adaptation to the new data distribution.',
               'For every new batch of data, our scheme tests whether the new batch is compatible with the old data '
               'distribution, or more plausible under the assumption of a change.'],
     'raw_file': 'c2/src/pdf_2012.08101v3.txt',
     'agent_note': 'Close: a detected change triggers a partial reset (tempering of the posterior) of a neural or other '
                   'model, without boundaries; the detector is the evidence of the new batch (surprise), not own change.'},
    {'id': 'c2:11', 'tag': 'c2', 'reading': 'close', 'reading_by': RB,
     'source': 'Duran-Martin, Sánchez-Betancourt, Shestopaloff, Murphy, "A unifying framework for generalised Bayesian '
               'online learning in non-stationary environments" (BONE; arXiv:2411.10153; TMLR 03/2025)',
     'version': 'v3, 12 Mar 2025', 'url': 'https://arxiv.org/abs/2411.10153',
     'quote': ['designed to accommodate both gradual changes and sudden changes.',
               'we choose the conditional prior as either a hard reset to the prior',
               'a convex combination of the prior and the previous belief state (using an OU process)'],
     'raw_file': 'c2/src/pdf_2411.10153v3.txt',
     'agent_note': 'Close: a hard reset to the prior when the run-length (changepoint) posterior crosses a threshold, a '
                   'soft OU pull otherwise; the trigger is the changepoint probability from predictive likelihoods, not '
                   'own change; purpose online tracking under non-stationarity.'},
    {'id': 'c2:12', 'tag': 'c2', 'reading': 'close', 'reading_by': RB,
     'source': 'Solowjow, Trimpe, "Event-triggered Learning" (arXiv:1904.03042)',
     'version': 'v2, 23 Mar 2020', 'url': 'https://arxiv.org/abs/1904.03042',
     'quote': ['By monitoring the actual communication rate and comparing it to the one that is induced by the model, we '
               'detect a mismatch between model and reality and trigger model learning when needed.'],
     'raw_file': 'c2/src/pdf_1904.03042v2.txt',
     'agent_note': 'Close (older, different field): model re-learning triggered by an event (a statistical mismatch test) '
                   'instead of a schedule; the quantity is inter-communication times of a networked controller; purpose '
                   'communication efficiency and changing dynamics, not network plasticity.'},
    # ------------------------------------------------------------------ bears: the clock / Oracle assumption, stated
    {'id': 'c2:13', 'tag': 'c2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Juliani, Ash, "A Study of Plasticity Loss in On-Policy Deep Reinforcement Learning" (arXiv:2405.19153; '
               'NeurIPS 2024 spotlight per OpenReview MsUf8kpKTF)',
     'version': 'v2, 1 Nov 2024', 'url': 'https://arxiv.org/abs/2405.19153',
     'quote': ['Most of these are applied each time there is a training distribution change, implying that there must be '
               'awareness of when this occurs; in practice this information may be unavailable and difficult to detect.',
               'ReDo. This technique resets individual neurons within the network based on a dormancy criteria at fixed '
               'intervals (Sokar et al., 2023)',
               'Continuous interventions are desirable because they do not require an awareness of when a distribution '
               'shift has occurred, which can be challenging in practical scenarios where we want to mitigate plasticity '
               'loss.'],
     'raw_file': 'c2/src/pdf_2405.19153v2.txt',
     'agent_note': 'Bears: states the frontier assumption C2 denies (intermittent refreshes are applied at supplied '
                   'distribution changes or at fixed intervals) and names boundary detection as the difficulty; the '
                   'field\'s answer here is continuous interventions, not a self-detected trigger.'},
    {'id': 'c2:14', 'tag': 'c2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Tang, Obando-Ceron, Castro, Courville, Berseth, "Mitigating Plasticity Loss in Continual Reinforcement '
               'Learning by Reducing Churn" (C-CHAIN; arXiv:2506.00592; ICML 2025)',
     'version': 'v1, 31 May 2025', 'url': 'https://arxiv.org/abs/2506.00592',
     'quote': ['re-initialized every time the task is switched to be the oracle baseline.',
               'The oracle baseline learns each task from random initialization, thus free of the influence of task '
               'change.'],
     'raw_file': 'c2/src/pdf_2506.00592v1.txt',
     'agent_note': 'Bears: the Oracle that C2\'s prediction is measured against (a full re-initialisation at the supplied '
                   'task switch); no self-triggered refresh is among the compared methods.'},
    {'id': 'c2:15', 'tag': 'c2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Nikishin, Schwarzer, D\'Oro, Bacon, Courville, "The Primacy Bias in Deep Reinforcement Learning" '
               '(arXiv:2205.07802; ICML 2022)',
     'version': 'v1, 16 May 2022', 'url': 'https://arxiv.org/abs/2205.07802',
     'quote': ['periodically re-initialize the parameters of its last few layers while preserving the replay buffer.'],
     'raw_file': 'c2/src/pdf_2205.07802v1.txt',
     'agent_note': 'Bears: the clock-scheduled reset that C2 would replace.'},
    {'id': 'c2:16', 'tag': 'c2', 'reading': 'bears', 'reading_by': RB,
     'source': 'McCutcheon, Chatzaroulas, Fallah, "Calibrated Partial Resets: Preventing Policy Collapse in Continual '
               'Reinforcement Learning" (CPR; arXiv:2607.24996; RLC Continual RL Workshop, oral)',
     'version': 'v1, 27 Jul 2026', 'url': 'https://arxiv.org/abs/2607.24996',
     'quote': ['an optimizer that periodically pulls low-utility neurons toward their initialization',
               'Algorithm 1 CPR (utilities every step; resets every f steps)'],
     'raw_file': 'c2/src/pdf_2607.24996v1.txt',
     'agent_note': 'Bears: a 2026 frontier refresh, still on the step clock (every f steps), with utility setting only '
                   'the strength.'},
    {'id': 'c2:17', 'tag': 'c2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Nikishin, Oh, Ostrovski, Lyle, Pascanu, Dabney et al., "Deep Reinforcement Learning with Plasticity '
               'Injection" (arXiv:2305.15555; NeurIPS 2023)',
     'version': 'v2, 3 Oct 2023', 'url': 'https://arxiv.org/abs/2305.15555',
     'quote': ['The majority of the experiments use a single plasticity injection after 50M frames; otherwise, we '
               'explicitly specify the number and timesteps of injections.'],
     'raw_file': 'c2/src/pdf_2305.15555v2.txt',
     'agent_note': 'Bears: plasticity injection is timed by frame count, chosen by the experimenter.'},
    {'id': 'c2:18', 'tag': 'c2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Press, Schneider, Kümmerer, Bethge, "RDumb: A simple approach that questions our progress in continual '
               'test-time adaptation" (arXiv:2306.05401)',
     'version': 'v3, 3 Apr 2024', 'url': 'https://arxiv.org/abs/2306.05401',
     'quote': ['we introduce a simple baseline, “RDumb”, that periodically resets the model to its pretrained state.'],
     'raw_file': 'c2/src/pdf_2306.05401v3.txt',
     'agent_note': 'Bears: the clock-scheduled reset baseline that c2:0-c2:3 replace with change triggers.'},
    {'id': 'c2:19', 'tag': 'c2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Noukhovitch, Lavoie, Strub, Courville, "Language Model Alignment with Elastic Reset" (arXiv:2312.07551; '
               'NeurIPS 2023)',
     'version': 'v1, 6 Dec 2023', 'url': 'https://arxiv.org/abs/2312.07551',
     'quote': ['periodically reset the online model to an exponentially moving average (EMA) of itself, then reset the EMA '
               'model to the initial model.'],
     'raw_file': 'c2/src/pdf_2312.07551v1.txt',
     'agent_note': 'Bears: a refresh whose purpose is to limit drift (KL from the initial model), yet scheduled on the '
                   'clock; the drift is the objective\'s measure, not the trigger.'},
    {'id': 'c2:20', 'tag': 'c2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Zhou, Zhuang, Wang, "Stay Hungry, Keep Learning: Sustainable Plasticity for Deep Reinforcement Learning" '
               '(OpenReview hTrSxX3kiV, ICML 2025 poster; PDF not fetched; not found on arXiv by title)',
     'version': 'OpenReview abstract as returned by the API search on 2026-09-30',
     'url': 'https://openreview.net/forum?id=hTrSxX3kiV',
     'quote': ['Cycle reset involves a scheduled renewal of neurons'],
     'raw_file': 'c2/src/or_hTrSxX3kiV_abstract.txt',
     'agent_note': 'Bears: a 2025 reset framework for plasticity, scheduled.'},
    {'id': 'c2:21', 'tag': 'c2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Ma, Li, Zhang, Liu, Wang, Chen et al., "Revisiting Plasticity in Visual Reinforcement Learning: Data, '
               'Modules and Training Stages" (Adaptive RR; arXiv:2310.07418; ICLR 2024)',
     'version': 'v3, 19 May 2024', 'url': 'https://arxiv.org/abs/2310.07418',
     'quote': ['When the FAU difference between consecutive checkpoints drops below a minimal threshold (set at 0.001 in '
               'our experiments), marking the end of the early stage, we adjust the RR to 2.'],
     'raw_file': 'c2/src/pdf_2310.07418v3.txt',
     'agent_note': 'Bears: a plasticity-state-triggered switch (fraction of active units), acting on the replay ratio, '
                   'not a refresh, and not own change.'},
    {'id': 'c2:22', 'tag': 'c2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Chua, Precup, Richards, "Balancing Plasticity and Stability with Fast and Slow Successor Features" '
               '(arXiv:2605.26357; ICML 2026)',
     'version': 'v2, 27 May 2026', 'url': 'https://arxiv.org/abs/2605.26357',
     'quote': ['We find that methods favoring stability, such as synaptic consolidation, outperform approaches focused on '
               'plasticity, such as parameters resetting.',
               'maintaining plasticity (e.g., reset-based methods) is insufficient.'],
     'raw_file': 'c2/src/pdf_2605.26357v2.txt',
     'agent_note': 'Bears (not contradicts): under gradual, naturalistic drift, resets lose to consolidation. It does '
                   'not test a change-triggered reset, so it does not show the mechanism fails; it shows the refresh '
                   'family can be the wrong lever when there are no abrupt switches.'},
    {'id': 'c2:23', 'tag': 'c2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Cheruvu et al., "Boundary-Free Continual Reinforcement Learning via Online Task-Shift Detection" '
               '(OpenReview Sdd4jFgE63, CoLLAs 2026 Work-In-Progress Track, non-archival; PDF NOT REACHED, HTTP 403)',
     'version': 'OpenReview abstract as returned by the API search on 2026-09-30',
     'url': 'https://openreview.net/forum?id=Sdd4jFgE63',
     'quote': ['so transfer, reset, or consolidation steps can be triggered at predefined times.',
               'The results suggest that false-positive triggers are costly algorithmic interventions, not merely '
               'detection mistakes'],
     'raw_file': 'c2/src/or_Sdd4jFgE63_abstract.txt',
     'agent_note': 'Bears: names reset among the steps that CRL methods trigger at predefined times, and reports that '
                   'false-positive triggers are costly; the relevant risk for an own-change trigger.'},
    {'id': 'c2:24', 'tag': 'c2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Basterrech, Woźniak, "Tracking changes using Kullback-Leibler divergence for the continual learning" '
               '(arXiv:2210.04865; SMC 2022)',
     'version': 'v1, 10 Oct 2022', 'url': 'https://arxiv.org/abs/2210.04865',
     'quote': ['As a measure of the rapidity of changes, we analyze the popular Kullback-Leibler divergence.'],
     'raw_file': 'c2/src/pdf_2210.04865v1.txt',
     'agent_note': 'Bears: KL as a rate-of-change monitor for drift, on the data distribution; no refresh.'},
]
