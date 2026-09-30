"""Claims for ROB1 stage 3 (Robotics/DECLARATION.md), candidate C-R3 (Robotics/CRR_READING.md, r4-B3), searcher B:
progress-indexed runtime failure detection for learned robot policies. Searcher B worked independently of searcher A
(Robotics/checks/claims_s3_r3a.py). B read A's claims and dossier first. B then searched differently:
  - other terms: alignment to the nearest nominal timestep, memory-based temporal alignment, latent-state and hidden-state
    thresholds, duration-normalised movement-primitive time, distance-series, time-axis warping, angular resampling;
  - other communities: legged and biped robots, industrial-robot condition monitoring and its patents (Google Patents),
    aviation flight-data monitoring, rotating-machinery order tracking, spacecraft telemetry, mining equipment, automotive
    software supervision (AUTOSAR), batch-process theses;
  - older robot work and theses that A could not read: the first author's PhD dissertation behind Park et al. (ICRA 2016;
    Autonomous Robots 2019), Wu, Guan and Rojas (Applied Sciences 2019, through MDPI's resource server), Pastor et al.
    (ICRA 2011).

Transcribed from the dossier docs/citations/rob1_s3_r3b_2026-09-30.md. Sources were fetched 2026-09-30. Raw files and extracted
texts are held outside the repository under /tmp/claude-0/rob_s3/, named in `raw_file` relative to that root, with
r3b/SHA256SUMS.txt beside them. Every quote is copied from a dossier blockquote. Each quote was checked verbatim against its
extracted text with Robotics/checks/verify.py's matcher (claim_status, root /tmp/claude-0/rob_s3) before this file was final.
The WebSearch tool was unavailable (session budget used), so searches ran through public endpoints with curl
(r3b/search_queries.txt).

The mechanism searched (CRR_READING.md, C-R3): a runtime failure detector (anomaly or failure prediction, conformal
monitoring) for a learned robot policy whose thresholds or statistics are indexed by task progress, phase or the policy's own
accumulated change, rather than by the raw step index. The frontier comparator: conformal thresholds per step index (SAFE's
functional conformal band; FAIL-Detect's time-varying band). CRR's prediction: earlier detection at an equal false-alarm rate
on rollouts whose speed varies. The must-fail case: rollouts that all run at the same speed.

Positions (the caller's):
  P1  progress- or phase-indexed failure detection or conformal calibration for robot policies is published;
  P2  it is shown to detect earlier or more accurately than step-indexed thresholds;
  P3  the step-index mismatch (rollouts of different speed) is named as a problem.

Reading policy: searcher A's, copied unchanged so that the two searches grade alike. It was fixed before any reading below
was written.
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
Clock-only sources, and sources read for context (order tracking, arc-length alignment of demonstrations), are listed in the
dossier and are not claims. 'Not found' is never 'novel'.

READING_CHECKS holds searcher B's check of each of searcher A's readings: is 'states' (or 'close') justified by A's quote?
It was written after reading each of A's quotes in its extracted text, with about 350 characters of context on each side
(r3b/a_readings_context_check.txt; all 59 of A's quotes were re-found by the verify.py matcher on 2026-09-30).
"""

RB = "stage-3 agent (searcher B); for the investigator's review"
T = 'r3b/txt/'

FIDEL = ('Rolland, Mayran de Chamisso, Mouret, "Failure Identification in Imitation Learning via Statistical and Semantic '
         'Filtering" (FIDeL; arXiv:2604.13788; ICRA 2026 per the arXiv comment and the authors\' page)')
FIDEL_V = 'arXiv v1, 15 Apr 2026 (the only version; comment "8 pages, Appendix coming soon, accepted at ICRA 2026")'
FIDEL_U = 'https://arxiv.org/abs/2604.13788v1'

PARK_D = ('Park, "A Multimodal Execution Monitor for Assistive Robots" (PhD dissertation, Georgia Institute of Technology, '
          'May 2018; advisor C. C. Kemp)')
PARK_DV = ('dissertation PDF from the Georgia Tech repository (title page "May 2018", "Date Approved: January 17, 2018"; PDF '
           'created 8 Mar 2018), fetched 2026-09-30')
PARK_DU = 'https://repository.gatech.edu/server/api/core/bitstreams/e219959e-f114-42f2-81d2-e90d4058828e/content'

WU = ('Wu, Guan, Rojas, "A Latent State-Based Multimodal Execution Monitor with Anomaly Detection and Classification for Robot '
      'Introspection" (Applied Sciences 9(6):1072, 2019)')
WU_V = ('published 14 Mar 2019 (received 14 Jan, accepted 2 Mar 2019), open-access PDF from MDPI\'s resource server; the '
        'article pages on mdpi.com returned HTTP 403 to the session')
WU_U = 'https://mdpi-res.com/d_attachment/applsci/applsci-09-01072/article_deploy/applsci-09-01072.pdf'

CLAIMS = [
    # ------------------------------------------------ A. a learned policy: the conformal band read at the aligned nominal timestep
    {'id': 'r3b:1', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': FIDEL, 'version': FIDEL_V, 'url': FIDEL_U,
     'quote': ['We extend Conformal Prediction to handle both temporal and spatial variations, with memory-based temporal '
               'alignment that ensures robustness to variable execution speeds.',
               'The final anomaly score is obtained as the minimum transport cost across nominal timesteps:',
               'We extend the Conformal Prediction (CP) framework [18], [19] to define a dynamic threshold for our anomaly '
               'detector DA, accounting for both temporal structure and patch-level variations.',
               'At runtime, the current observation is aligned to its closest nominal timestep tmin using OT (Eq. (3)), and '
               'patch-level scores are compared to their corresponding bounds',
               'We additionally evaluated FIDeL on more realistic data by performing inference on trajectories generated with '
               'ACT [3], an IL policy.'],
     'raw_file': T + 'pdf_2604.13788v1.txt',
     'agent_note': 'States P1 for a learned policy (ACT imitation-policy rollouts on a real soldering task; the BotFails set is '
                   'teleoperated). This is the nearest published instance of C-R3\'s structure that either searcher found. The '
                   'conformal bound is a band per nominal timestep of the demonstrations, the form of SAFE\'s and '
                   'FAIL-Detect\'s bands. At run time it is read at the nominal timestep that the current observation is '
                   'matched to (the arg-min over nominal timesteps of an optimal-transport cost), not at the step count. The '
                   'stated purpose is robustness to variable execution speeds. Differences from C-R3: the index is a '
                   'position in the demonstration found by appearance matching, not the policy\'s accumulated change; nothing '
                   'forces it to be monotone; and the detector reads observations only (policy-independent). A did not find '
                   'this source.'},
    {'id': 'r3b:2', 'position': 'P3', 'reading': 'states', 'reading_by': RB,
     'source': FIDEL + ', related work', 'version': FIDEL_V, 'url': FIDEL_U,
     'quote': ['The closest work to ours, FAIL-Detect [12], performs runtime failure detection in imitation learning with '
               'Continuous Normalizing Flows (CNF) [47], but does not distinguish benign anomalies from task-critical failures '
               'and assumes that the task is performed with the same temporal consistency during inference as in '
               'demonstrations.',
               'Instead, our method relies on a representation based formulation that captures both temporal progression and '
               'spatial structure, enabling alignment across variable execution speeds, localized heatmaps, and more '
               'interpretable scores.'],
     'raw_file': T + 'pdf_2604.13788v1.txt',
     'agent_note': 'States P3. The time-varying band of the frontier method (FAIL-Detect, one of the step-indexed comparators '
                   'of C-R3) is said to assume that test rollouts keep the demonstrations\' timing. The remedy is alignment '
                   'across execution speeds, which is C-R3\'s remedy, not the constant threshold that FIPER, VLA-FAIL and '
                   'Lee and Har chose (r3a:17, r3a:19, r3a:20).'},
    {'id': 'r3b:3', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': FIDEL + ', thresholding comparison and limitations', 'version': FIDEL_V, 'url': FIDEL_U,
     'quote': ['CP-time, a standard conformal prediction approach using only temporal deviations from reference demonstrations.',
               'Gaussian assumption, a simpler baseline with thresholds derived from a Gaussian fit of calibration scores '
               '(mean and variance) at each timestep.',
               'Comparing CP variants, CP-time&space consistently improves over CP-time.',
               'Second, the method’s spatial and temporal invariance, though useful for robustness, can reduce sensitivity to '
               'fine-grained or order-dependent deviations.',
               'This is particularly problematic for non-Markovian anomalies, where the correctness of an action depends not '
               'only on the current state but also on the history of states or actions that preceded it.'],
     'raw_file': T + 'pdf_2604.13788v1.txt',
     'agent_note': 'Close for P2 at most, and a caution. The thresholding baselines differ in how the band is built (temporal '
                   'CP, temporal and spatial CP, a Gaussian fit), not in its index. None is described as read at the raw step '
                   'index, so the aligned index is never set against the step index, and no detection time is reported. If the '
                   'Gaussian baseline is read at the raw step, the comparison is confounded with the Gaussian assumption. The '
                   'authors name the cost of the invariance, unmeasured: alignment by appearance loses order- and '
                   'history-dependent faults. That is a failure mode a C-R3 gate must include.'},
    # ------------------------------------------------ B. the dissertation behind Park et al. (ICRA 2016; AuRo 2019), which A could not read
    {'id': 'r3b:4', 'position': 'P3', 'reading': 'states', 'reading_by': RB,
     'source': PARK_D + ', section 2.2.4 "Thresholding" and section 3.2.2', 'version': PARK_DV, 'url': PARK_DU,
     'quote': ['Narrowing down the range of operations, Serdio et al. introduced a time-varying threshold, allowing a tight '
               'decision boundary around low variance area for rolling mills [98]. However, time variations, such as delay or '
               'speed variation, easily break down the detection system.',
               'To address these concerns, Rodriguez et al. set cutoff probability thresholds over discretized time slices [58].',
               'The use of a time-varying likelihood threshold is similar to our work, but we do not directly use observations. '
               'Instead, we vary the threshold with respect to the hidden-state distribution, execution progress, estimated by '
               'an HMM.',
               'Compared to the direct use of time, the representation would have the advantage of handling variability in '
               'the timing of a behavior execution, but the true state path is hidden from the observer.'],
     'raw_file': T + 'park_dissertation_gatech2018.txt',
     'agent_note': 'States P3 more plainly than the ICRA paper (r3a:2): a time-varying (step-indexed) threshold "easily" breaks '
                   'under delay or speed variation, and the progress index is introduced against it. Two step-indexed '
                   'precursors are named: Serdio et al. (rolling mills) and Rodriguez et al. (robot assembly, thresholds over '
                   'discretised time slices). Neither was read here.'},
    {'id': 'r3b:5', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': PARK_D + ', chapter 4 (the execution monitor of the robot-assisted feeding system)', 'version': PARK_DV,
     'url': PARK_DU,
     'quote': ['For the detector, we combine two multimodal anomaly detectors, referred to as HMM-D [42], that use multivariate '
               'hidden Markov models (HMMs) and dynamic thresholds to determine anomalies.',
               'HMM-D is a binary (one-class) detector that learns a model from non-anomalous task executions and detects '
               'anomalies when the log-likelihood of a sequence of input signals is lower than a time-varying threshold. HMM-D '
               'dynamically changes the threshold depending on the progress of a current task execution.',
               'We then evaluated our execution monitoring system with Henry Evans, a person with quadriplegia in California, '
               'USA.'],
     'raw_file': T + 'park_dissertation_gatech2018.txt',
     'agent_note': 'States P1 for a robot behaviour (a PR2 feeding behaviour, not a learned visuomotor policy). It is the same '
                   'method as r3a:1, here run inside the group\'s feeding system and evaluated with a care recipient. It adds '
                   'no new mechanism; it shows that the progress-indexed threshold was used in a system tested with an end user.'},
    {'id': 'r3b:6', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': PARK_D + ', section 3.2.5, detection delay', 'version': PARK_DV, 'url': PARK_DU,
     'quote': ['HMM-F: A likelihood-based classifier with a fixed threshold [101].',
               'The HMM-D and -GP methods resulted in shorter detection delays with higher true positive rates.',
               'In this evaluation, we tuned the three detectors to have the same, small false positive rate (FPR) given a '
               'test set.',
               'While we do not explicitly test tasks that involved large timing variations, our tasks have timing variations '
               'as illustrated in Figure 3.4.'],
     'raw_file': T + 'park_dissertation_gatech2018.txt',
     'agent_note': 'Close for P2, and the nearest robot result on C-R3\'s own metric. Detection delay at an equal (small) false '
                   'positive rate is shorter for the two progress-indexed thresholds than for a fixed threshold, on simulated '
                   'step anomalies added to real feeding data. The comparator is a fixed threshold, not a step-indexed one, '
                   'and the author states that large timing variations were not tested. So the rollouts-of-varying-speed '
                   'comparison that C-R3 predicts is not made. Section 3.2 cites as its basis the ICRA 2016 paper and the '
                   'Autonomous Robots paper, then "submitted" (refs [42, 142]). Its Table 3.2 has eight methods (HMM-D, HMM-GP '
                   'and six baselines), none step-indexed. Whether the published journal version (AuRo 2019, not reached by '
                   'either searcher) differs was not checked.'},
    {'id': 'r3b:7', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': PARK_D + ', section 3.2 (HMM-D against HMM-KNN)', 'version': PARK_DV, 'url': PARK_DU,
     'quote': ['Cluster membership for HMM-D is based on temporal similarity. We also introduce another clustering-based '
               'algorithm, HMM-KNN, that uses clusters based on execution progress similarity.',
               'HMM-D shows similar but slightly lower performance, but it outperformed HMM-KNN. This result shows the '
               'training with the time-based RBFs was beneficial.'],
     'raw_file': T + 'park_dissertation_gatech2018.txt',
     'agent_note': 'Close for P2, and a caution. Both detectors read their threshold at the estimated progress at run time. '
                   'The one whose progress clusters were built with the clock (time-based radial basis functions) beat the '
                   'one built on progress similarity alone (AUC, Table 3.2). This is not a step-indexed comparator, so it is '
                   'not read contradicts. It warns that a purely own-clock construction was not the better one in the one '
                   'robot study that tried both.'},
    # ------------------------------------------------ C. a latent-state threshold on executions of varying speed (A could not fetch it)
    {'id': 'r3b:8', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': WU, 'version': WU_V, 'url': WU_U,
     'quote': ['The detector uses a dynamic log-likelihood threshold that varies by latent state for anomaly detection',
               'with a learned threshold ρ(z) that derives from the most likely estimated hidden state given current '
               'observations.',
               'Figure 7 illustrates hidden-state partitions for 20 nominal executions for Skill 3 that were carried out with '
               'varying speeds and goals.'],
     'raw_file': T + 'wu_applsci2019_mdpires.txt',
     'agent_note': 'Close for P1: the threshold is indexed by the most likely latent state of a nonparametric HMM (an execution '
                   'state within a skill, not an ordered progress variable). The nominal executions vary in speed, so the '
                   'index is meant to be free of the clock. The robot is a scripted Baxter kitting behaviour with DMP skills, '
                   'not a learned policy. A listed this paper as unreachable ("Access Denied").'},
    {'id': 'r3b:9', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': WU + ', section 7.1', 'version': WU_V, 'url': WU_U,
     'quote': ['We compare the results of our execution varying threshold with a fixed threshold presented in [2].',
               'From Figure 9, we see that for executions 2 and 4 our varying threshold detector identified anomalies that the '
               'fixed threshold method could not.',
               'This improved sensitivity reduces false negatives and helps us flag anomalies at times closer to the ground '
               'truth.',
               'Our results indicate that while the GD system had the HSD resulting in 16.6% better precision, our system had '
               '61.7% better recall.'],
     'raw_file': T + 'wu_applsci2019_mdpires.txt',
     'agent_note': 'Close for P2: the state-indexed threshold detects earlier (closer to the labelled onset) and misses less than '
                   'a fixed threshold, with lower precision than a gradient-based detector. The comparators are fixed and '
                   'gradient-based, not step-indexed; the timing evidence is two executions in a figure.'},
    # ------------------------------------------------ D. the per-step band on duration-normalised movement-primitive time (2011)
    {'id': 'r3b:10', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Pastor, Kalakrishnan, Chitta, Theodorou, Schaal, "Skill Learning and Task Outcome Prediction for '
               'Manipulation" (IEEE ICRA 2011)',
     'version': 'ICRA 2011 conference PDF (PDF metadata: "2011 IEEE International Conference on Robotics and Automation, May '
                '9-13, 2011, Shanghai"; created 11 Feb 2011), copy on a CMU faculty page fetched 2026-09-30',
     'url': 'https://www.cs.cmu.edu/~cga/print.2/Pastor_ICRA_2011.pdf',
     'quote': ['The function f does not directly depend on time; instead, it depends on a phase variable s, which monotonically '
               'changes from 1 towards 0 during a movement and is generated by the canonical system given by:',
               'The recorded signals were truncated using the start and end time of the DMP and are re-sampled such that each '
               'signal only contains 100 samples.',
               'monitor all sensor signals and compute at each time step for each signal a z-test using the weighted mean and '
               'weighted standard deviation from the training phase under the null-hypotheses with confidence c.',
               'managed to detect all 11 failures in the test set without triggering any false positives.'],
     'raw_file': T + 'pastor_icra2011_cmu.txt',
     'agent_note': 'Close for P1: the ancestor of the per-timestep band. The band is indexed by each trial\'s duration-normalised '
                   'movement-primitive time (100 samples between the primitive\'s start and end), which for a fixed temporal '
                   'scaling is a monotone function of the primitive\'s own phase variable. It is not an online progress '
                   'estimate: the resampling needs the trial\'s end time, and the test was replayed offline. The policy is '
                   'reinforcement-learned (PI2) chopstick manipulation on a PR2. A read only the later Sutanto et al. version '
                   'of the phase-indexed sensor traces (not used) and could not reach Pastor et al. (IROS 2011).'},
    # ------------------------------------------------ E. neighbouring communities: aviation flight-data monitoring; robot condition monitoring (patent)
    {'id': 'r3b:11', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Li, Hansman, "Anomaly Detection in Airline Routine Operations Using Flight Data Recorder Data" (MIT '
               'International Center for Air Transportation, Report No. ICAT-2013-4, based on L. Li\'s MIT PhD thesis, 2013)',
     'version': 'Report ICAT-2013-4, June 2013. Text read from a third-party mirror (silo.tips). MIT DSpace (handle '
                '1721.1/79344) served a human-verification page to the session, so the mirror text could not be checked '
                'against the MIT copy',
     'url': 'https://silo.tips/download/anomaly-detection-in-airline-routine-operations-using-flight-data-recorder-data',
     'quote': ['In order to map raw data into comparable vectors in the high dimensional space, time series data from different '
               'flights are anchored by a specific event to make temporal patterns comparable.',
               'For the approach phase, the time series are first transformed into a “distance-series” and then a number of '
               'samples are obtained backtracking from the touchdown point (Figure 3.8).',
               'Temporal reference is provided along the x-axis using the distance to touchdown to be consistent with other '
               'plots for the approach phase.'],
     'raw_file': T + 'li_silo_tips.txt',
     'agent_note': 'Close for P1 by domain. In aviation flight-data monitoring, the approach phase is indexed by the aircraft\'s '
                   'own progress (distance to touchdown) instead of time, so that flights are compared at like positions. '
                   'Detection is offline, by clustering, and there is no comparison with a time index. Provenance is weak '
                   '(a mirror).'},
    {'id': 'r3b:12', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Kawai, Nagahama (Kawasaki Jukogyo KK), "State monitoring device, state abnormality determination method, and '
               'state abnormality determination program", US 2023/0264355 A1 (family of TW I790696 B, WO 2022/024946 A1)',
     'version': 'US application publication 24 Aug 2023; priority 28 Jul 2020 (JP 2020-127513); text as rendered by Google '
                'Patents, fetched 2026-09-30',
     'url': 'https://patents.google.com/patent/US20230264355A1/en',
     'quote': ['a key feature of the DTW method is that it allows for nonlinear expansion and contraction of the time-series '
               'data in the direction of the time axis when calculating the degree of similarity.',
               'the DTW method can obtain the degree of dissimilarity (DTW distance) of two waveforms in a way that does not '
               'reflect differences in the time axis direction of the two waveforms, but reflects well differences in the '
               'amplitude and other aspects of the waveforms.',
               'evaluating delays and distortions in the time axis direction of time-series data may be effective in capturing '
               'the predictive sign of abnormality.',
               'In other words, while phase deviations as measurement errors are ignored, large phase deviations that indicate '
               'degradation of servo motors, etc., can be detected appropriately.'],
     'raw_file': T + 'gpat_US20230264355A1.txt',
     'agent_note': 'Close for P1, and a caution. An industrial playback robot\'s motor-current cycle is compared with a reference '
                   'cycle by a time-warped distance (the first embodiment), and trended over months. This is predictive '
                   'maintenance, not runtime failure detection of a task. The second embodiment bounds the time shift, '
                   'because timing distortion is itself a sign of degradation. Full invariance to the time axis discards that '
                   'sign. Together with r3b:3, this names the cost of an own-clock index: faults that show up as timing (a '
                   'slow or stalled servo, a hesitating policy) become invisible unless the clock is kept somewhere.'},
]

# searcher B's check of searcher A's readings (Robotics/checks/claims_s3_r3a.py), made against A's quotes in A's extracted
# texts with about 350 characters of context on each side (r3b/a_readings_context_check.txt; 59 of 59 quotes FOUND)
READING_CHECKS = [
    {'claim_id': 'r3a:1', 'agree': True,
     'note': 'In context the run-time threshold is selected by the estimated progress: tau(gamma) = mu - c sigma given the '
             'hidden-state distribution. The dissertation (r3b:7) adds that cluster membership was built by temporal '
             'similarity and that this beat progress-similarity clustering. States P1 holds for the run-time index; the clock '
             'enters the construction, as A notes.'},
    {'claim_id': 'r3a:2', 'agree': True,
     'note': 'Borderline, and supported elsewhere. The first quote is about constant thresholds, not per-timestep ones. The '
             'second is hedged ("would have the advantage"). The dissertation says it outright: time-varying thresholds '
             '"easily break down" under delay or speed variation (r3b:4).'},
    {'claim_id': 'r3a:3', 'agree': True,
     'note': 'Close: the baselines are change detection and a fixed threshold. The dissertation adds a detection-delay result at '
             'equal FPR, still against a fixed threshold (r3b:6).'},
    {'claim_id': 'r3a:4', 'agree': True,
     'note': 'Close: in context the "state" is the LSTM-VAE latent of the observation window, not an ordered progress '
             'variable.'},
    {'claim_id': 'r3a:5', 'agree': True, 'note': 'Close: fixed-threshold comparator, ROC only.'},
    {'claim_id': 'r3a:6', 'agree': True,
     'note': 'States P1 under the policy\'s "or detection statistic": the RND score is FiLM-conditioned on predicted progress, '
             'and the conformal threshold is one number per relationship. In context, progress is a normalised cumulative sum '
             'of learned positive increments (trained from VLM preferences), not normalised time. B checked the ablation '
             'section: every ablation keeps the progress conditioning, so P2 is not shown, as A says.'},
    {'claim_id': 'r3a:7', 'agree': True,
     'note': 'Close. The residual V_tau(t) = tau_pred - (1 - t/E[T]) sets the policy\'s own progress against the clock, so a '
             'slow successful rollout is flagged. The two clocks are compared, not swapped.'},
    {'claim_id': 'r3a:8', 'agree': True, 'note': 'Close: AUROC under injected perturbations; speed is not varied.'},
    {'claim_id': 'r3a:9', 'agree': True,
     'note': 'Close. In context the threshold is one quantile of the terminal cumulative score over successful trajectories, '
             'compared with the running sum at every step. The accumulated change is the statistic, not an index.'},
    {'claim_id': 'r3a:10', 'agree': True,
     'note': 'Close: the speed ambiguity is named and answered by adding the clock (elapsed time and time limit).'},
    {'claim_id': 'r3a:11', 'agree': True,
     'note': 'Close: phase-free comparator, teleoperated surgery; the later detection is a cost of inferring the phase online.'},
    {'claim_id': 'r3a:12', 'agree': True,
     'note': 'States P3 in the caller\'s wording (cycles of different duration named as the obstacle). In context the obstacle '
             'is to reusing state-of-the-art detectors on raw cycles, not per-timestep thresholds as such. The robots run '
             'scripted programs.'},
    {'claim_id': 'r3a:13', 'agree': True, 'note': 'Close: confounded comparison (model class differs), offline per cycle.'},
    {'claim_id': 'r3a:14', 'agree': True,
     'note': 'Close by domain. In context NOAL is the same monitor without alignment, so this is the cleanest published form '
             'of C-R3\'s P2, outside robotics.'},
    {'claim_id': 'r3a:15', 'agree': True, 'note': 'Close: prediction of missing segments, not failure detection.'},
    {'claim_id': 'r3a:16', 'agree': True, 'note': 'Close by domain; second-hand for the primary alignment papers.'},
    {'claim_id': 'r3a:17', 'agree': True,
     'note': 'States P3. The measured fact is the constant threshold\'s higher TNR; attributing it to varying order or timing '
             'is the authors\' reading. As A notes, the per-timestep threshold still has the best TWA.'},
    {'claim_id': 'r3a:18', 'agree': True,
     'note': 'States P3, and states C-R3\'s remedy as future work. FIDeL (r3b:1) had already published an aligned-index conformal '
             'band in April 2026.'},
    {'claim_id': 'r3a:19', 'agree': True, 'note': 'States P3 (episode length); the remedy is a constant threshold.'},
    {'claim_id': 'r3a:20', 'agree': True, 'note': 'States P3 in C-R3\'s terms (execution speed and task progress).'},
    {'claim_id': 'r3a:21', 'agree': True,
     'note': 'Close: the argument is stated, not measured. In context the authors cite Park et al. (2019) as the progress-'
             'conditioned alternative that they reject along with the time index.'},
]

# Quotes corrected to the verbatim source text, or dropped, after a NOT FOUND in Robotics/checks/verify_s3.py; one dict per
# quote: {'id', 'quote_index', 'action': 'corrected' | 'dropped', 'old', 'new', 'reason'}. The first run of verify_s3.py
# (2026-09-30, root /tmp/claude-0/rob_s3) found every quote of this module verbatim, so nothing was corrected or dropped.
VERIFY_CORRECTIONS = []
