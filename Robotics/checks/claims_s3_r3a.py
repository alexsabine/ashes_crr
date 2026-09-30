"""Claims for ROB1 stage 3 (Robotics/DECLARATION.md), candidate C-R3 (Robotics/CRR_READING.md, r4-B3), searcher A:
progress-indexed runtime failure detection for learned robot policies. Transcribed from the dossier
docs/citations/rob1_s3_r3a_2026-09-30.md (sources fetched 2026-09-30; raw files and extracted texts held outside the
repository under /tmp/claude-0/rob_s3/, named in `raw_file` relative to that root, with r3a/SHA256SUMS.txt beside them).
Every quote is copied from a dossier blockquote and was checked verbatim against its extracted text before this file was
written (normalisation as Robotics/checks/verify.py).

The mechanism searched (CRR_READING.md, C-R3): a runtime failure detector (anomaly or failure prediction, conformal
monitoring) for a learned robot policy whose thresholds or statistics are indexed by task progress, phase or the policy's own
accumulated change (progress-aware, phase-aligned, time-warped / DTW-aligned, progress-estimation-based monitoring) rather
than by the raw step index. The frontier comparator (stage 1, r4:23, r4:24): conformal thresholds per step index (SAFE's
functional conformal band; Hide-and-Seek's time-varying band). CRR's prediction: earlier detection at an equal false-alarm
rate on rollouts whose speed varies; the must-fail case is rollouts that all run at the same speed.

Positions (the caller's):
  P1  progress- or phase-indexed failure detection or conformal calibration for robot policies is published;
  P2  it is shown to detect earlier or more accurately than step-indexed thresholds;
  P3  the step-index mismatch (rollouts of different speed) is named as a problem.

'reading' is decided by the stage-3 agent from the quote, for the investigator's review ('reading_by'). Reading policy,
fixed before the readings were written:
  states       the source publishes the position as stated, for a robot (a learned policy or a robot behaviour): for P1 a
               runtime failure or anomaly detector whose threshold, calibration or detection statistic is indexed or
               conditioned on an estimate of task or execution progress, phase or the robot's own accumulated change, not on
               the step count alone; for P2 such an index compared with a step-indexed (per-timestep) threshold and reported
               earlier or more accurate; for P3 the source says that per-timestep thresholds or calibration fail or are
               unreliable because rollouts differ in speed, length or timing;
  close        a nearby mechanism that differs in one named respect: the index is an execution state or skill that is not
               progress; progress or accumulated change is the monitored signal rather than the index of the threshold; the
               comparison is against a fixed or context-free threshold rather than a step-indexed one, or is confounded; the
               setting is a neighbouring domain (batch process monitoring, functional-data statistics, teleoperated surgery);
               the step-index problem is named for a different reason (situation variation) or answered by adding the clock;
  contradicts  the source shows the mechanism (or its limiting case) fails or is inferior to a step-indexed threshold.
Clock-only frontier sources (SAFE, Hide-and-Seek, FAIL-Detect, Foresight and others: per-timestep bands) are listed in the
dossier as context (section F) and are not claims here. 'Not found' is never 'novel'.
"""

RB = "stage-3 agent (searcher A); for the investigator's review"
T = 'r3a/txt/'

CLAIMS = [
    # ------------------------------------------------ A. the foundational robot case: a progress-indexed likelihood threshold
    {'id': 'r3a:1', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Park, Erickson, Bhattacharjee, Kemp, "Multimodal Execution Monitoring for Anomaly Detection During Robot '
               'Manipulation" (IEEE ICRA 2016, doi 10.1109/ICRA.2016.7487160 per the search listing; open author copy in '
               'the Georgia Tech repository)',
     'version': 'ICRA 2016 conference PDF (PDF metadata: "2016 IEEE International Conference on Robotics and Automation, '
                'May 16-21, 2016, Stockholm", created 15 Feb 2016), Georgia Tech repository copy fetched 2026-09-30',
     'url': 'https://repository.gatech.edu/server/api/core/bitstreams/815fb414-6f8a-4218-99fd-411af2be5bce/content',
     'quote': ['In contrast to prior work, our system also uses a detection threshold that changes based on the execution '
               'progress.',
               'Our execution monitor performs anomaly detection by comparing the log-likelihood, log P(X|λ), of the '
               'observations, X, with a threshold, τ(γ), that depends on the estimated execution progress, γ.',
               'Our system represents execution progress, γ, using the probability mass function over hidden states given '
               'the current observations',
               'Each cluster is a time-based soft cluster that represents execution progress vectors that occurred at '
               'similar times during execution'],
     'raw_file': T + 'park_icra2016_gatech.txt',
     'agent_note': 'States P1 for a robot behaviour (a PR2 pushing and feeding behaviour, not a learned visuomotor policy): '
                   'the anomaly threshold is indexed by an estimate of execution progress (the HMM hidden-state distribution '
                   'inferred from the observations so far), not by the step count. Two differences from C-R3: the progress '
                   'variable is the monitor\'s own HMM state, not the policy\'s accumulated change in resolvable steps; and '
                   'the progress clusters are built with radial basis functions in time, and the matching cluster is chosen '
                   'by KL divergence between hidden-state distributions, so the clock enters the construction.'},
    {'id': 'r3a:2', 'position': 'P3', 'reading': 'states', 'reading_by': RB,
     'source': 'Park, Erickson, Bhattacharjee, Kemp (ICRA 2016), section IV-A "Representing Execution Progress"',
     'version': 'ICRA 2016 conference PDF (PDF metadata: "2016 IEEE International Conference on Robotics and Automation, '
                'May 16-21, 2016, Stockholm", created 15 Feb 2016), Georgia Tech repository copy fetched 2026-09-30',
     'url': 'https://repository.gatech.edu/server/api/core/bitstreams/815fb414-6f8a-4218-99fd-411af2be5bce/content',
     'quote': ['Even during non-anomalous executions, likelihood tends to vary significantly with the number of '
               'observations, which reduces the effectiveness of a constant detection threshold.',
               'Compared to directly using time, this would have the advantage of handling variability in the timing of a '
               'behavior’s execution.'],
     'raw_file': T + 'park_icra2016_gatech.txt',
     'agent_note': 'States P3: the authors motivate the progress index by the variability of execution timing, against '
                   'indexing by time directly. This is C-R3\'s own argument, published in 2016.'},
    {'id': 'r3a:3', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Park, Erickson, Bhattacharjee, Kemp (ICRA 2016), section V, the threshold comparison',
     'version': 'ICRA 2016 conference PDF (PDF metadata: "2016 IEEE International Conference on Robotics and Automation, '
                'May 16-21, 2016, Stockholm", created 15 Feb 2016), Georgia Tech repository copy fetched 2026-09-30',
     'url': 'https://repository.gatech.edu/server/api/core/bitstreams/815fb414-6f8a-4218-99fd-411af2be5bce/content',
     'quote': ['We also compared the performance of our time-varying likelihood threshold to two baseline methods from the '
               'literature: likelihood change detection [23] and fixed-threshold likelihood detection [19].',
               'The ROC curves in Fig. 10(a) Right show that for any given false-positive rate, our method had a higher '
               'true-positive rate than the two baseline methods.'],
     'raw_file': T + 'park_icra2016_gatech.txt',
     'agent_note': 'Close for P2: the progress-indexed threshold beats a fixed threshold and a change detector at every false '
                   'positive rate, but no step-indexed (per-timestep) threshold is among the baselines, so the comparison C-R3 '
                   'predicts is not made. The authors call their own progress-indexed threshold "time-varying". The journal '
                   'follow-up (Park, Kim, Kemp, Autonomous Robots 2019, 8 detectors) could not be read on the day (paywalled; '
                   'dossier section G).'},
    # ------------------------------------------------ B. a state-indexed threshold for a learned anomaly model
    {'id': 'r3a:4', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Park, Hoshi, Kemp, "A Multimodal Anomaly Detector for Robot-Assisted Feeding Using an LSTM-based Variational '
               'Autoencoder" (arXiv:1711.00614; IEEE RA-L 2018 by common citation, venue not verified on the day)',
     'version': 'arXiv v1, 2 Nov 2017 (the only version; comment "under review")', 'url': 'https://arxiv.org/abs/1711.00614v1',
     'quote': ['We introduce a varying threshold that changes over the estimated state of a task execution motivated by the '
               'dynamic threshold [3].',
               'In this paper, the state is the latent space representation of observations.',
               'HMM-GP: A likelihood-based classifier using an HMM introduced in [32]. We vary the likelihood threshold with '
               'respect to the distribution of hidden states.'],
     'raw_file': T + 'pdf_1711.00614v1.txt',
     'agent_note': 'Close for P1: the threshold is indexed by the estimated execution state (the LSTM-VAE latent of the '
                   'observation window), not by the step count, but the state is not a progress or phase variable. The '
                   'HMM-GP baseline is the group\'s progress-indexed threshold (hidden-state distribution) of the journal '
                   'version, described here second-hand.'},
    {'id': 'r3a:5', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Park, Hoshi, Kemp (arXiv:1711.00614), the thresholding comparison (Fig. 8)',
     'version': 'arXiv v1, 2 Nov 2017', 'url': 'https://arxiv.org/abs/1711.00614v1',
     'quote': ['The red curve shows the result of the proposed state-based thresholding. The yellow curve shows the result of '
               'conventional fixed thresholding. The state-based thresholding resulted in higher true positive rates given '
               'the same false positive rates.'],
     'raw_file': T + 'pdf_1711.00614v1.txt',
     'agent_note': 'Close for P2: a state-indexed threshold beats a fixed threshold at equal false positive rate; there is no '
                   'step-indexed comparator and the index is not progress.'},
    # ------------------------------------------------ C. a learned policy: the OOD detector conditioned on predicted task progress
    {'id': 'r3a:6', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Schneider, Welte, Rayyes, "RAFAIL: Relationship-Aware Failure Detection for Robotic Manipulation" '
               '(arXiv:2609.18324)',
     'version': 'arXiv v1, 16 Sep 2026 (the only version)', 'url': 'https://arxiv.org/abs/2609.18324v1',
     'quote': ['RAFAIL represents individual relationships from point-cloud observations and applies task-progress-conditioned '
               'and importance-gated OOD detection to each.',
               'Consequently, neither the VLM nor the importance/progress labelers are executed at deployment; the policy '
               'directly predicts relationship importance',
               'We use FiLM [20] to condition the RND OOD detector on the current task progress pt.',
               'A relationship-specific threshold θk ood is calibrated using CP [10].'],
     'raw_file': T + 'pdf_2609.18324v1.txt',
     'agent_note': 'States P1 for a learned policy (a ManiFlow flow-matching imitation policy on a UR10e): the failure '
                   'statistic (an RND OOD score per object relationship) is conditioned on task progress predicted by an '
                   'auxiliary head of the policy itself, and its threshold is calibrated by conformal prediction on successful '
                   'demonstrations. The progress label is distilled offline from VLM pairwise preferences (monotone in the '
                   'demonstration, not the clock). The conformal threshold itself is one number per relationship; the progress '
                   'enters through the score. No ablation removes the progress conditioning or replaces it by the step index, '
                   'so P2 is not shown here.'},
    # ------------------------------------------------ D. the policy's own progress read from its activations
    {'id': 'r3a:7', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Bhardwaj, Duan, Dan, Ma, Culbertson, "Decoding Task Progress from VLA Representations" (arXiv:2608.13474)',
     'version': 'arXiv v1, 13 Aug 2026 (the only version)', 'url': 'https://arxiv.org/abs/2608.13474v1',
     'quote': ['we probe the residual stream of π0.5 and find that task progress, the normalized time remaining in a '
               'trajectory, is linearly readable from the activations.',
               'We use the probe as a simple label-free OOD detector, which detects stalled task progress, and find it '
               'competitive with state-of-the-art methods.',
               'which measures the deviation between the predicted and actual progress. The rollout is flagged as '
               'out-of-distribution the first time Vτ(t) > δ.'],
     'raw_file': T + 'pdf_2608.13474v1.txt',
     'agent_note': 'Close for P1: the detector reads the policy\'s own internal progress (a linear probe on the VLA\'s '
                   'activations) and alarms when it falls behind the clock-expected progress (1 - t/E[T]) by a constant '
                   'margin. Progress is the monitored signal, not the index of the threshold; the probe is trained to '
                   'regress normalised time; and a slow but successful rollout would be flagged by construction, the opposite '
                   'of C-R3\'s invariance to rollout speed.'},
    {'id': 'r3a:8', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Bhardwaj et al. (arXiv:2608.13474), cross-task and held-out-perturbation results against SAFE',
     'version': 'arXiv v1, 13 Aug 2026', 'url': 'https://arxiv.org/abs/2608.13474v1',
     'quote': ['Under per-episode aggregation, Vτ achieves the best seen-task score (0.910) and is competitive on unseen tasks '
               '(0.851), trailing only SAFE-MLP (0.917).',
               'wins both unseen columns (per-replan 0.871, per-episode 0.960), beating both supervised SAFE detectors '
               'despite never observing any OOD examples.'],
     'raw_file': T + 'pdf_2608.13474v1.txt',
     'agent_note': 'Close for P2, and mixed: a progress-based detector against SAFE (the step-indexed functional-CP '
                   'frontier), scored by AUROC on injected image perturbations. It wins on held-out perturbation types and '
                   'trails SAFE-MLP on unseen tasks. The rollouts are not varied in speed, the metric is not detection time at '
                   'equal false-alarm rate, and progress is the signal rather than the index.'},
    # ------------------------------------------------ E. the policy's own accumulated change as the statistic (STAC)
    {'id': 'r3a:9', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Agia, Sinha, Yang, Cao, Antonova, Pavone, Bohg, "Unpacking Failure Modes of Generative Policies: Runtime '
               'Monitoring of Consistency and Progress" (Sentinel; arXiv:2410.04640; CoRL 2024 per the arXiv comment)',
     'version': 'arXiv v2, 10 Oct 2024 (v1 6 Oct 2024)', 'url': 'https://arxiv.org/abs/2410.04640v2',
     'quote': ['we propose to take the cumulative sum of statistical distances along a trajectory as a measure of the overall '
               'temporal consistency in a policy rollout.',
               'At runtime, we raise a failure warning at the moment that ηt exceeds a failure detection threshold γ, which '
               'we calibrate offline using the validation dataset of successful trajectories Dτ.',
               'we propose to use VLMs to monitor the task progress of the policy by providing them with the robot’s image '
               'observations up to the current timestep as a video.'],
     'raw_file': T + 'pdf_2410.04640v2.txt',
     'agent_note': 'Close for P1, and the nearest in quantity: STAC accumulates the statistical distance (MMD or KL) between '
                   'successive action-chunk distributions of the policy, i.e. the policy\'s own accumulated change, with one '
                   'conformal threshold calibrated on the maximum over successful trajectories. The accumulated change is the '
                   'alarm statistic, not the index against which a per-position threshold is read, so it is C-R3\'s quantity '
                   'in a different role. The separate VLM monitor checks task progress as a signal.'},
    {'id': 'r3a:10', 'position': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'Agia et al., Sentinel (arXiv:2410.04640), the VLM progress monitor',
     'version': 'arXiv v2, 10 Oct 2024', 'url': 'https://arxiv.org/abs/2410.04640v2',
     'quote': ['Differentiating between partial progress and task failure can be ambiguous for a slow moving robot, and thus, '
               'we also specify the current elapsed time t and the time limit for the task H.'],
     'raw_file': T + 'pdf_2410.04640v2.txt',
     'agent_note': 'Close for P3: the speed problem is named (a slow robot looks like a failing one), but the remedy is the '
                   'reverse of C-R3: the monitor is given the clock and the time limit.'},
    # ------------------------------------------------ F. phase-specific detectors in teleoperated surgery
    {'id': 'r3a:11', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Yasar, Alemzadeh, "Real-Time Context-aware Detection of Unsafe Events in Robot-Assisted Surgery" '
               '(arXiv:2005.03611; DSN 2020 per the arXiv comment)',
     'version': 'arXiv v2, 18 Jun 2020 (v1 7 May 2020)', 'url': 'https://arxiv.org/abs/2005.03611v2',
     'quote': ['Our approach integrates a surgical gesture classifier that infers the operational context from the '
               'time-series kinematics data of the robot with a library of erroneous gesture classifiers that given a '
               'surgical gesture can detect unsafe events.',
               'Being context-specific results in more accurate de-tection of erroneous gestures but worse reaction times.',
               'Table (VIII) shows that there is an improvement of 14.1% and 16.2% of AUC over non-context specific '
               'detection, for Suturing and Block Transfer tasks, respectively.',
               'On the other hand, the gesture-specific models result in negative reaction times (later detection of '
               'anomalies) and higher computation times due to the latency introduced for identifying the context.'],
     'raw_file': T + 'pdf_2005.03611v2.txt',
     'agent_note': 'Close for P2, and mixed: detectors indexed by the inferred phase (the surgical gesture) of a teleoperated '
                   'da Vinci trajectory are more accurate (AUC +14.1 and +16.2 %) than one detector without phase, but detect '
                   'later, because the phase must first be inferred. The comparator is phase-free, not step-indexed, and the '
                   'operator is a surgeon, not a learned policy. The later detection is a warning for C-R3\'s "earlier" '
                   'prediction: the own clock has to be estimated online, and that costs time.'},
    # ------------------------------------------------ G. industrial robot cycles of different duration, time-warped
    {'id': 'r3a:12', 'position': 'P3', 'reading': 'states', 'reading_by': RB,
     'source': 'Lacoquelle, Pucel, Travé-Massuyès, Reymonet, Enaux, "Warped Time Series Anomaly Detection" (WETSAND; '
               'arXiv:2404.12134; Vitesco Technologies, ONERA, LAAS-CNRS)',
     'version': 'arXiv v1, 18 Apr 2024 (the only version)', 'url': 'https://arxiv.org/abs/2404.12134v1',
     'quote': ['Notable challenges arise from the fact that a task performed multiple times may exhibit different duration in '
               'each repetition and that the time series reported by the sensors are irregularly sampled because of data '
               'gaps.',
               'Second, the cycles may vary in length, because the robot program contains physical tasks of variable '
               'duration (eg object gripping, bar code scans), or simply because the operator takes a manual action.'],
     'raw_file': T + 'pdf_2404.12134v1.txt',
     'agent_note': 'States P3 for robots (Universal Robots arms on a production line; scripted programs, not learned '
                   'policies): cycles of different duration are named as the obstacle to anomaly detection, and answered by '
                   'dynamic time warping to a Soft-DTW barycenter prototype.'},
    {'id': 'r3a:13', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Lacoquelle et al., WETSAND (arXiv:2404.12134), comparison with convolutional autoencoders',
     'version': 'arXiv v1, 18 Apr 2024', 'url': 'https://arxiv.org/abs/2404.12134v1',
     'quote': ['Given that the 2σ threshold results in F2 = 0.69 and the boxplot threshold results in F2 = 0.92, the '
               'threshold is set at the boxplot threshold for the experiments that follow.',
               'The time series are first last-value-padded to 24576 time steps, which is the maximal number of time steps '
               'of the cycles in the training set.',
               'and an F2 score of 0.10, which is a quite poor result.',
               'It yields an F2 score of 0.23, which is better that the previous CAE but is still much lower than the '
               'anomaly detection performance with WETSAND.'],
     'raw_file': T + 'pdf_2404.12134v1.txt',
     'agent_note': 'Close for P2: the time-warped detector (F2 0.92) far exceeds autoencoders run on step-indexed, padded '
                   'cycles (F2 0.10 and 0.23) on real robot cycles, but the comparison is confounded (the model class differs; '
                   'the authors attribute the autoencoders\' failure to reconstructing normal and abnormal cycles equally '
                   'well), it is offline per cycle, not runtime, and there is no equal-false-alarm detection-time measure.'},
    # ------------------------------------------------ H. the same prediction in process monitoring and functional-data statistics
    {'id': 'r3a:14', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Centofanti, Lepore, Kulahci, Spooner, "Real-time Monitoring of Functional Data" (FRTM; arXiv:2205.06256)',
     'version': 'arXiv v1, 12 May 2022 (the only version)', 'url': 'https://arxiv.org/abs/2205.06256v1',
     'quote': ['However, the identification of the appropriate reference distribution is a non-trivial problem, because '
               'processes could exhibit different temporal dynamics.',
               'FRTM method is compared with two simpler natural competing approaches, namely the monitoring in real-time '
               'with no alignment, referred to as NOAL, and the pointwise monitoring approach of the functional quality '
               'characteristic, referred to as PW.',
               'FRTM outperforms in terms of TDR both the NOAL and PW methods for all shift types and misalignments.',
               'The NOAL method is badly affected by large phase variation',
               'we clearly see that FRTM signals the OC condition much earlier than the competing methods.'],
     'raw_file': T + 'pdf_2205.06256v1.txt',
     'agent_note': 'Close for P2 only by domain: this is C-R3\'s prediction, shown in statistical process monitoring. A '
                   'real-time monitor that registers the running profile (aligns it in time to the reference) beats the same '
                   'monitor without alignment (NOAL, the step-indexed comparator) in true detection rate at controlled false '
                   'alarm rate, most under large phase variation, and signals earlier on penicillin batches. It is not a robot '
                   'or a learned policy.'},
    {'id': 'r3a:15', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Wang, Kurtek, Zhang, "Joint Registration and Conformal Prediction for Partially Observed Functional Data" '
               '(arXiv:2502.15000; J. Comput. Graph. Stat. 2026, doi 10.1080/10618600.2026.2634823 per the search listing, '
               'venue not verified on the day)',
     'version': 'arXiv v2, 19 Nov 2025 (v1 20 Feb 2025)', 'url': 'https://arxiv.org/abs/2502.15000v2',
     'quote': ['existing methods for functional data prediction often treat phase variation as negligible.',
               'We propose a novel framework that integrates registration into conformal prediction of the amplitude '
               'component for partial functional data. This results in more accurate prediction intervals, as compared to '
               'procedures that do not utilize registration, when functional data contains phase variation.',
               'However, when phase variation is present, the prediction band is less effective at capturing such geometric '
               'features, since their timing varies considerably across observations.'],
     'raw_file': T + 'pdf_2502.15000v2.txt',
     'agent_note': 'Close for P2 by domain and task: the statistical core of C-R3 for conformal bands. Functional conformal '
                   'prediction on the raw time axis (the method under SAFE\'s and FAIL-Detect\'s bands) loses when curves '
                   'differ in timing; registering (time-warping) partial curves before conformal prediction gives more '
                   'accurate intervals with coverage kept. It is prediction of missing segments, not failure detection, and not '
                   'robotics.'},
    {'id': 'r3a:16', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Rocha de Oliveira, de Juan, "Synchronization-Free Multivariate Statistical Process Control for Online '
               'Monitoring of Batch Process Evolution" (Front. Anal. Sci. 1:772844, doi 10.3389/frans.2021.772844)',
     'version': 'published 14 Jan 2022 (received 9 Sep 2021, accepted 27 Dec 2021); open-access JATS XML from the publisher',
     'url': 'https://www.frontiersin.org/journals/analytical-science/articles/10.3389/frans.2021.772844/xml',
     'quote': ['key process events do not occur at the same time point when comparing different NOC batch runs of the same '
               'process.',
               'Great progress has been made to develop strategies for batch alignment based on a maturity index or '
               'indicator variable coming directly from a process variable or estimated by PLS models or using more '
               'advanced algorithms, such as correlation optimized warping or dynamic time warping',
               'For a NOC observation, an additional indication of the batch process progress is provided based on the '
               'identification of the local MSPC model that provides the lowest residuals.',
               'The process progress in this approach plays the same role as the process maturity concept proposed by other '
               'authors'],
     'raw_file': T + 'frontiers_frans_2021_772844.txt',
     'agent_note': 'Close for P1 by domain: in batch process monitoring, control limits indexed by batch maturity (an '
                   'indicator variable), by warping (DTW, COW, Kassidas et al. 1998) or by an estimated process progress '
                   'instead of batch time are an established family, motivated by runs whose events do not occur at the same '
                   'time (P3). It is not robotics; the primary sources it cites (Kassidas et al. 1998; the indicator variable '
                   'of Nomikos and MacGregor) could not be read on the day.'},
    # ------------------------------------------------ I. the 2025-26 frontier names the step-index mismatch
    {'id': 'r3a:17', 'position': 'P3', 'reading': 'states', 'reading_by': RB,
     'source': 'Römer, Kobras, Worbis, Schoellig, "Failure Prediction at Runtime for Generative Robot Policies" (FIPER; '
               'arXiv:2510.09459; '
               'NeurIPS 2025 per the arXiv comment), Appendix C.4',
     'version': 'arXiv v2, 13 Oct 2025 (v1 10 Oct 2025)', 'url': 'https://arxiv.org/abs/2510.09459v2',
     'quote': ['We attribute this to the fact that these threshold types effectively compare the failure prediction score at '
               'timestep t against the scores in the calibration dataset for the same timestep.',
               'However, the higher TNR of the constant threshold shows that the CP band and time-varying threshold raise '
               'false alarms more frequently in generalization scenarios, where the policy may solve subtasks in varying '
               'order or with inconsistent timing.',
               'The time-varying threshold yields the highest TWA for FIPER'],
     'raw_file': T + 'pdf_2510.09459v2.txt',
     'agent_note': 'States P3 in the frontier\'s own words: per-timestep thresholds compare a score with calibration scores '
                   '"for the same timestep", and so raise more false alarms when the policy\'s timing varies. The same paper '
                   'finds the per-timestep threshold gives the best overall TWA, so the mismatch has a measured cost in true '
                   'negatives, not a verdict against step indexing. No progress index is tried.'},
    {'id': 'r3a:18', 'position': 'P3', 'reading': 'states', 'reading_by': RB,
     'source': 'Huang, Cai, Patel, Hajiha, Browne, Chen, "Failure Detection for Surgical Robot Imitation Policies via '
               'Flow-Matching World Modeling" (FoMo-FD; arXiv:2607.27511; submitted to IEEE RA-L per the arXiv comment)',
     'version': 'arXiv v1, 29 Jul 2026 (the only version)', 'url': 'https://arxiv.org/abs/2607.27511v1',
     'quote': ['Second, we use an episode-level threshold rather than a time-varying conformal band as in FAILDetect [13].',
               'Time-varying calibration can be effective when rollouts are temporally aligned, but surgical manipulation '
               'episodes may reach the same task stage at different time steps due to variation in initial conditions, '
               'contact dynamics, and policy execution.',
               'Future work could replace the time index with a progress- or state-conditioned calibration variable, '
               'enabling adaptive thresholds without assuming strict temporal alignment across rollouts.'],
     'raw_file': T + 'pdf_2607.27511v1.txt',
     'agent_note': 'States P3, and states C-R3\'s remedy as future work, for learned (ACT) imitation policies on the da Vinci '
                   'Research Kit: time-indexed conformal calibration assumes aligned rollouts; the same stage is reached at '
                   'different steps; replacing the time index by a progress- or state-conditioned calibration variable is '
                   'proposed. The paper itself uses one episode-level threshold.'},
    {'id': 'r3a:19', 'position': 'P3', 'reading': 'states', 'reading_by': RB,
     'source': 'Seligmann, Gospodinov, Dincer, Neumann, "VLA-FAIL: Efficient Task Failure Detection for Finetuned '
               'Vision-Language-Action Models" '
               '(arXiv:2606.21386)',
     'version': 'arXiv v1, 19 Jun 2026 (the only version)', 'url': 'https://arxiv.org/abs/2606.21386v1',
     'quote': ['determined via a time-constant conformal prediction band on calibration data [13].',
               'We do not use a time-dependent threshold [31, 13, 7] as it is not applicable to episodes that vary '
               'significantly in length, such as in our real-world Drawer task.'],
     'raw_file': T + 'pdf_2606.21386v1.txt',
     'agent_note': 'States P3: per-timestep thresholds are rejected because real-robot episodes vary in length. The remedy '
                   'is a constant threshold (no index), not a progress index.'},
    {'id': 'r3a:20', 'position': 'P3', 'reading': 'states', 'reading_by': RB,
     'source': 'Lee, Har, "Perturbation-Based Epistemic Uncertainty for Failure Detection in Vision-Language-Action Models" '
               '(arXiv:2606.20754)',
     'version': 'arXiv v3, 14 Sep 2026 (v1 18 Jun 2026, v2 31 Aug 2026)', 'url': 'https://arxiv.org/abs/2606.20754v3',
     'quote': ['We use a constant threshold because distribution shifts can alter execution speed and task progress, making '
               'timestep-wise alignment between calibration and evaluation rollouts unreliable.'],
     'raw_file': T + 'pdf_2606.20754v3.txt',
     'agent_note': 'States P3 in C-R3\'s terms (execution speed and task progress break timestep-wise alignment between '
                   'calibration and test rollouts); the remedy is again a constant threshold, not a progress index.'},
    {'id': 'r3a:21', 'position': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'Willibald, Lee, "Hierarchical Task Decomposition for Execution Monitoring and Error Recovery: '
               'Understanding the Rationale Behind Task Demonstrations" (arXiv:2505.04565; accepted in IJRR per the arXiv '
               'comment)',
     'version': 'arXiv v1, 7 May 2025 (the only version)', 'url': 'https://arxiv.org/abs/2505.04565v1',
     'quote': ['employed time-based Gaussian Mixture Regression (GMR) in previous works (Willibald et al. 2020; Eiband et al. '
               '2019, 2023b) to compute the Mahalanobis distance between the robot’s measured and expected proprioceptive '
               'sensor values. The probabilistic modeling allows the approach to scale the anomaly detection sensitivity '
               'depending on the current timestep.',
               'We employ GMR where expected feature values and allowed deviations are predicted by conditioning on the '
               'measured end-effector pose relative to the relevant coordinate system for the current skill. Conditioning '
               'anomaly detection on time or task progress would require consistent feature profiles across demonstrations, '
               'i.e. an exact replication of the situation in all runs.',
               'We argue that important features, such as contact forces, are influenced by interaction dynamics between the '
               'robot and the environment rather than time.'],
     'raw_file': T + 'pdf_2505.04565v1.txt',
     'agent_note': 'Close for P3, and a caution for C-R3: the group moved from time-indexed anomaly bounds (their earlier '
                   'work) to bounds conditioned on the measured end-effector pose within the current skill, arguing that '
                   'conditioning on time or on task progress both assume consistent profiles across runs. The argument is '
                   'stated, not measured; it rejects the progress index as well as the step index, in favour of a state '
                   'index.'},
]
