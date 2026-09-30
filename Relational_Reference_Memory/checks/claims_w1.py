"""Claims for Relational_Reference_Memory/DECLARATION_2.md Part W, family F1 (positions P1 and P2), transcribed from the
dossier docs/citations/rrm2_f1_2026-09-30.md (fetched 2026-09-30; extracted texts held outside the repository under
/tmp/claude-0/rrm2_src/, named in `raw_file` relative to that root). Every quote is copied from a dossier blockquote;
verify_w.py checks each against its extracted text.

'reading' is decided by the grading agent from the quote, for the investigator's review ('reading_by'). Reading policy
(RQM's, unchanged), fixed before the readings were written and applied to every position:
  states       the source asserts (or reports as its own result) every predicate of the position, for at least one of the
               objects the position names, within the position's scope;
  close        the source asserts part of the position, or the position in a narrower or different scope;
  bears        relevant evidence or a bound that neither asserts nor negates the position;
  contradicts  the source asserts or reports the negation of the position within its scope. For an existential position
               ('is published', 'reduces forgetting') the negation is 'not'; a failure in a sub-regime the position does not
               claim is a bound ('bears').
P1 is read as: a 2025-26 source names the drift (staleness) of stored class statistics (prototypes, means, covariances,
cached head statistics) as a main limitation or core difficulty of exemplar-free or small-memory class-IL, in a setting
trained from scratch (cold start, or a standard split without external pretraining). A source that names the drift only
as one problem among others, or moves the main difficulty elsewhere while still naming the drift, is 'close'.
P2 is read, per the caller's instruction for this family, as: 'states' needs a same-protocol comparison in the paper
itself, trained from scratch, against a replay method with a stated realistic buffer (2000 exemplars on a 100-class set,
or 20 per class), in which the exemplar-free method is level or ahead; 'contradicts' needs a same-protocol table, from
scratch and at a realistic buffer, in which exemplar-free methods are clearly behind replay. Operationalised here (the
agent's, for review): 'level' is within about one point or ahead on the paper's main from-scratch setting(s); 'clearly
behind' is more than about two points behind the best replay row on most reported settings. A buffer below 20 per class,
an unstated buffer, or a stated buffer with only very weak replay rows makes 'close'; exemplar-free arms that are replay
methods run with the buffer removed, or a table mixed across settings, make 'bears'. The numbers are recorded in each
agent_note, as the paper reports them; numbers from different papers are not comparable.
"""

RB = "grading agent; for the investigator's review"

CLAIMS = [
    # ------------------------------------------------------------------ P1
    {'id': 'w1:0', 'tag': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Magistri, Trinci, Soutif-Cormerais, van de Weijer, Bagdanov, "EFC++: Elastic Feature Consolidation with '
               'Prototype Re-balancing for Cold Start Exemplar-free Incremental Learning" (arXiv:2503.10439; IJCV)',
     'version': 'v4, 28 Sep 2026', 'url': 'https://arxiv.org/abs/2503.10439',
     'quote': ['This is especially challenging for EFCIL since it requires high plasticity, resulting in feature drift which '
               'is difficult to compensate for in the exemplar-free setting.',
               'This confirms the challenges highlighted in Section 7.2 that our approach encounters when estimating the real '
               'class drift in Cold Start.',
               'From this analysis, we conclude that future work on Gaussian prototypes should prioritize more effective '
               'strategies for updating class means, beyond our current EFM approach.'],
     'raw_file': 'f1/src/pdf_2503.10439v4.txt',
     'agent_note': 'States P1 (cold start, from random initialisation): replacing the estimated class means by the real '
                   'ones is the largest gain in its oracle analysis, and the authors name the update of stored class means '
                   'as the priority for future work. No replay baseline is reported (P2 not graded).'},
    {'id': 'w1:1', 'tag': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Xu, Krawczyk, "Two-Way Is Better Than One: Bidirectional Alignment with Cycle Consistency for Exemplar-Free '
               'Class-Incremental Learning" (BiCyc; arXiv:2606.05675; ICLR 2026)',
     'version': 'v1, 4 Jun 2026', 'url': 'https://arxiv.org/abs/2606.05675',
     'quote': ['The core difficulty in prototype-based EFCIL is representation drift: as the backbone adapts to new tasks, '
               'the embedding geometry shifts and previously cached statistics become stale, biasing predictions toward '
               'recent classes.',
               'CIFAR-100 and TinyImageNet when training the feature extractor from scratch.'],
     'raw_file': 'f1/src/pdf_2606.05675v1.txt',
     'agent_note': "States P1 in the position's words ('core difficulty', 'cached statistics become stale'), with "
                   'from-scratch experiments.'},
    {'id': 'w1:2', 'tag': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Xu, Krawczyk, "Geometry-Anchored Transport Framework for Exemplar-Free Class-Incremental Learning" (GATF; '
               'arXiv:2606.25347; ECCV 2026)',
     'version': 'v2, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.25347',
     'quote': ['While maintaining class-conditional Gaussian statistics provides a principled classification strategy, these '
               'parametric summaries remain sensitive to anisotropic representation drift.',
               'The analytic anchor relies on an affine prior with EMA updates; while the residual network accommodates local '
               'non-linearities, severe nonlinear or highly non-stationary representation shifts may still challenge this '
               'linearized global approximation, particularly when covariance estimates are noisy or poorly conditioned.'],
     'raw_file': 'f1/src/pdf_2606.25347v2.txt',
     'agent_note': 'States P1: stored Gaussian class statistics are named as sensitive to drift, and the residual '
                   'difficulty of transporting them is its stated limitation; CIFAR-100, TinyImageNet and ImageNet-100 are '
                   'trained from scratch.'},
    {'id': 'w1:3', 'tag': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Xu, Jin, Sun, Xuan, Li, "Dual-Estimator: Decoupling Global and Local Semantic Shift for Drift Compensation in '
               'Class-Incremental Learning" (Dual-E; CVPR 2026, pp. 10799-10809; CVF open access)',
     'version': 'CVF open access camera-ready (no version number); not found on arXiv by title search on 2026-09-30',
     'url': 'https://openaccess.thecvf.com/content/CVPR2026/html/Xu_Dual-Estimator_Decoupling_Global_and_Local_Semantic_'
            'Shift_for_Drift_Compensation_CVPR_2026_paper.html',
     'quote': ['Although this approach demonstrates some effectiveness, it faces a critical limitation because continuously '
               'updating the backbone makes the stored intermediate representation obsolete [10, 18, 45], while freezing it '
               'compromises the model’s plasticity [42, 47].',
               'ResNet-18 [14] is used as the backbone and trained from scratch.'],
     'raw_file': 'f1/src/cvf_Xu_Dual-Estimator_Decoupling_Global_and_Local_Semantic_Shift_for_Drift_Compensation_CVPR_2026_'
                 'paper.txt',
     'agent_note': "States P1 ('a critical limitation': stored prototypes go obsolete as the backbone updates), from "
                   'scratch. Its comparisons are exemplar-free only (no replay row; P2 not graded).'},
    {'id': 'w1:4', 'tag': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Xu, Jin, Sun, Xuan, Li, "Class-Aware Drift Compensation for Non-Uniform Semantic Shift in Continual Learning" '
               '(CADC; CVPR 2026 Findings, pp. 7717-7727; CVF open access)',
     'version': 'CVF open access camera-ready (no version number); not found on arXiv by title search on 2026-09-30',
     'url': 'https://openaccess.thecvf.com/content/CVPR2026F/html/Xu_Class-Aware_Drift_Compensation_for_Non-Uniform_'
            'Semantic_Shift_in_Continual_Learning_CVPRF_2026_paper.html',
     'quote': ['In this work, we focus on Exemplar-Free Class Incremental Learning (EFCIL) under a cold-start setting, which '
               'poses a significant challenge as the model is trained from scratch without access to any prior knowledge.',
               'However, a key challenge in EFCIL is that the model’s ongoing evolution causes stored representations to '
               'become outdated, leading to semantic feature drift [7, 37]. Addressing such drift remains a critical '
               'challenge',
               'This issue is more severe in exemplar-free settings, where no stored samples anchor the old feature space.'],
     'raw_file': 'f1/src/cvf_Xu_Class-Aware_Drift_Compensation_for_Non-Uniform_Semantic_Shift_in_Continual_Learning_CVPRF_'
                 '2026_paper.txt',
     'agent_note': "States P1 for cold start from scratch ('a key challenge', 'remains a critical challenge'). Its third "
                   "sentence names the absence of stored samples to 'anchor the old feature space' as what makes the drift "
                   'worse: the problem RRM\'s kept anchors address, stated as a problem, not as a method.'},
    {'id': 'w1:5', 'tag': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Jučas, Pan, "Data-Free Reservoir Features for Efficient Long-Horizon Cold-Start Continual Learning" (CIRCLE; '
               'arXiv:2606.27095)',
     'version': 'v1, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.27095',
     'quote': ['Their main limitation is semantic drift [Yu et al., 2020]: as ϕ changes, old-class features shift and stored '
               'head statistics become outdated.',
               'All experiments follow the cold-start exemplar-free setting: no replay, no pre-training,'],
     'raw_file': 'f1/src/pdf_2606.27095v1.txt',
     'agent_note': "States P1 in its words ('main limitation', 'stored head statistics become outdated') for trained-"
                   'backbone methods under cold start; its own answer is to never train the features.'},
    {'id': 'w1:6', 'tag': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Honda, "Adversarial Pseudo-replay for Exemplar-free Class-incremental Learning" (APR; arXiv:2511.17973; '
               'WACV 2026)',
     'version': 'v1, 22 Nov 2025', 'url': 'https://arxiv.org/abs/2511.17973',
     'quote': ['The major cause of the catastrophic forgetting is the change in the feature extractor, also known as semantic '
               'drift [27] occurring when learning a new task. This leads to inconsistency between the preserved prototypes '
               'and features of past tasks extracted by the updated extractor.',
               'Only 1/T of the total classes are in the initial task.'],
     'raw_file': 'f1/src/pdf_2511.17973v1.txt',
     'agent_note': "States P1 ('the major cause'; preserved prototypes inconsistent with current features), with a cold "
                   'start among its settings. No replay baseline (joint only).'},
    {'id': 'w1:7', 'tag': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'He, Fang, Xu, Cui, Li, Chen, Zeng, Zhuang, "Semantic Shift Estimation via Dual-Projection and Classifier '
               'Reconstruction for Exemplar-Free Class-Incremental Learning" (DPCR; arXiv:2503.05423; ICML 2025)',
     'version': 'v4, 18 May 2025', 'url': 'https://arxiv.org/abs/2503.05423',
     'quote': ['However, their performance can be constrained by two key challenges: semantic shift in learned representations '
               'caused by incremental updates to the backbone, and decision bias in classifier training due to the absence '
               'of historical data',
               'The model is initialized randomly and all the categories are partitioned into T-tasks evenly.'],
     'raw_file': 'f1/src/pdf_2503.05423v4.txt',
     'agent_note': "States P1: semantic shift is one of 'two key challenges' of EFCIL, under cold start from random "
                   'initialisation. See w1:14 for its replay comparison.'},
    {'id': 'w1:8', 'tag': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Lu, Cao, Huang, Wang, Yang, Liu, "Restoring Forgotten Knowledge in Non-Exemplar Class Incremental Learning through Test-Time Semantic Evolution" '
               '(RoSE; arXiv:2503.16793)',
     'version': 'v1, 21 Mar 2025', 'url': 'https://arxiv.org/abs/2503.16793',
     'quote': ['As the network is trained, features from old classes drift in feature space, while the classifier fails to '
               'account for this drift, leading to wrong prediction.',
               'In the cold-start 10 tasks setting, RoSE surpasses SOTA'],
     'raw_file': 'f1/src/pdf_2503.16793v1.txt',
     'agent_note': 'States P1 for non-exemplar class-IL in cold and warm start: old-class features drift and the stored '
                   'classifier does not follow, which the whole method (test-time drift compensation) targets. No replay '
                   'row.'},
    {'id': 'w1:9', 'tag': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Hu, Yu, Zhang, Chen, Gao, "Confusion-Driven Self-Supervised Progressively Weighted Ensemble Learning for '
               'Non-Exemplar Class Incremental Learning" (CLOVER; NeurIPS 2025, DOI 10.52202/085713-2555)',
     'version': 'NeurIPS 2025 proceedings PDF (no version number)',
     'url': 'https://papers.nips.cc/paper_files/paper/2025/hash/6e1a97dfd2ce57ee4c006657ace4b9b6-Abstract-Conference.html',
     'quote': ['However, as the model undergoes continuous updates, these approaches inevitably experience prototype '
               'degradation [12], wherein the preserved prototypes of old classes diverge from their true distributions.',
               'However, the approach relies on a base task with abundant training data and has not yet been validated in a '
               'setting where all tasks contain an equal amount of data.'],
     'raw_file': 'f1/src/nips_CLOVER.txt',
     'agent_note': 'States P1 as the reason prototype-based NECIL is avoided: stored prototypes diverge from the true '
                   'distributions; CLOVER itself freezes the extractor after a large base task (ResNet-18, warm start; '
                   'cold start untested, by its own limitation).'},
    {'id': 'w1:10', 'tag': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Xu, Krawczyk, "Revisiting Prototype Rehearsal for Exemplar-Free Continual Learning: Manifold-Aware Boundary '
               'Sampling with Adaptive Class-Balanced Loss" (arXiv:2606.05695; CVPR 2026 Findings)',
     'version': 'v1, 4 Jun 2026', 'url': 'https://arxiv.org/abs/2606.05695',
     'quote': ['We argue that the performance gap stems not from the idea of prototype rehearsal per se, but from how it is '
               'typically instantiated',
               'Limitations. Our method still assumes that prototype estimates remain sufficiently informative as the feature '
               'space drifts'],
     'raw_file': 'f1/src/pdf_2606.05695v1.txt',
     'agent_note': 'Close: it still names drifting, stale prototypes (and its limitation assumes they stay informative), '
                   'but it places the main gap of prototype rehearsal in how synthetic samples are placed and in class '
                   'imbalance, not in the drift alone.'},
    {'id': 'w1:11', 'tag': 'P1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Wang, Guo, Li, Chen, "On the Discrimination and Consistency for Exemplar-Free Class Incremental Learning" (DCNet; arXiv:2501.15454; '
               'IJCAI 2025 per OpenReview/DBLP listing)',
     'version': 'v1, 26 Jan 2025', 'url': 'https://arxiv.org/abs/2501.15454',
     'quote': ['In EF-CIL, task-id prediction is more challenging due to the lack of inter-task interaction (e.g., replays of '
               'exemplars).'],
     'raw_file': 'f1/src/pdf_2501.15454v1.txt',
     'agent_note': 'Bears: names a different main difficulty of exemplar-free class-IL from scratch (task-id prediction '
                   'in a task-IL + OOD framework), not the drift of stored statistics; it does not deny the drift.'},
    {'id': 'w1:12', 'tag': 'P1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Tscheschner, Veas, Masana, "Incremental Learning with Repetition via Pseudo-Feature Projection" (Horde; arXiv:2502.19922)',
     'version': 'v1, 27 Feb 2025', 'url': 'https://arxiv.org/abs/2502.19922',
     'quote': ['Frozen feature extractors, on the other hand, avoid this issue since their representations remain fixed after '
               'the initial training, preventing catastrophic drift in the embedding space during the task sequence.'],
     'raw_file': 'f1/src/pdf_2502.19922v1.txt',
     'agent_note': 'Bears: frozen extractors are chosen to avoid embedding drift; the issue it names for trained '
                   'extractors is prototype estimation from incomplete class data under repetition.'},
    # ------------------------------------------------------------------ P2
    {'id': 'w1:13', 'tag': 'P2', 'reading': 'states', 'reading_by': RB,
     'source': 'Wang, Guo, Li, Chen, "On the Discrimination and Consistency for Exemplar-Free Class Incremental Learning" (DCNet; arXiv:2501.15454; '
               'IJCAI 2025 per OpenReview/DBLP listing)',
     'version': 'v1, 26 Jan 2025', 'url': 'https://arxiv.org/abs/2501.15454',
     'quote': ['This experimental setup is more challenging and realistic because it does not rely on a large initial task.',
               'All baselines train from scratch while maintaining a buffer M of 2000 samples. DCNet achieves a performance '
               'improvement of 0.9% and 5.5% over these advanced methods on two 10 tasks sequences. In the '
               'ImageNet-Subset-split10 task, our method slightly underperforms the state-of-the-art baseline.',
               'DER 64.5 38.3 66.85',
               'BEEF 2k 60.9 37.9 68.78',
               'TPL† 62.2 42.9 -',
               'DCNet 0 65.4 48.4 67.82'],
     'raw_file': 'f1/src/pdf_2501.15454v1.txt',
     'agent_note': 'States P2. Table 2, A_last, equal 10-task splits from scratch, replay at M = 2000: CIFAR-100 DCNet '
                   '65.4 vs best replay DER 64.5; Tiny-ImageNet 48.4 vs TPL 42.9; ImageNet-Subset 67.82 vs BEEF 68.78 '
                   '(0.96 behind). Caveats: DCNet is a task-IL + OOD method built on HAT (task-specific masks), trained '
                   '700 epochs with LARS; the baselines were either re-run or their numbers adopted from prior papers, so '
                   'the same-protocol claim is the paper\'s own.'},
    {'id': 'w1:14', 'tag': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'He, Fang, Xu, Cui, Li, Chen, Zeng, Zhuang, "Semantic Shift Estimation via Dual-Projection and Classifier '
               'Reconstruction for Exemplar-Free Class-Incremental Learning" (DPCR; arXiv:2503.05423; ICML 2025)',
     'version': 'v4, 18 May 2025', 'url': 'https://arxiv.org/abs/2503.05423',
     'quote': ['The experiments are conducted on CIFAR-100 and ImageNet-100 with the memory size M = 500, 1000 for storing '
               'exemplars.',
               'When the memory size is 500, all the EBCIL methods perform poorly and our DPCR outperforms them with '
               'considerable gap. With the increased memory size of 1000, the advantage of replaying exemplars begins to '
               'emerge.',
               'iCaRL-NCM (Rebuffi et al., 2017) 1000 46.78 62.62 40.71 57.47 44.46 62.60 35.68 54.24',
               'FOSTER (Wang et al., 2022) 1000 40.42 53.15 41.79 55.41 54.52 66.51 47.86 61.93',
               'DPCR (ours) - 49.59 62.13 40.72 54.91 53.24 68.18 40.82 57.94'],
     'raw_file': 'f1/src/pdf_2503.05423v4.txt',
     'agent_note': 'Close: same protocol (cold start, PyCIL, seed 1993), but the buffers are 500 and 1000 (5 and 10 per '
                   'class), below the realistic 2000. A_f at M = 1000: CIFAR-100 T=10 DPCR 49.59 vs iCaRL-NCM 46.78; T=20 '
                   '40.72 vs FOSTER 41.79; ImageNet-100 T=10 53.24 vs FOSTER 54.52; T=20 40.82 vs FOSTER 47.86. The '
                   "authors' own words: the replay advantage 'begins to emerge' at 1000."},
    {'id': 'w1:15', 'tag': 'P2', 'reading': 'states', 'reading_by': RB,
     'source': 'Liu, Chang, "Elastic Weight Consolidation Done Right for Continual Learning" (EWC-DR; arXiv:2603.18596; CVPR 2026)',
     'version': 'v3, 26 Mar 2026', 'url': 'https://arxiv.org/abs/2603.18596',
     'quote': ['All implementations are initialized and trained from scratch.',
               'iCaRL-NCM† Replay 58.56 54.19 50.51',
               'EWC-DR Regularization 63.75 60.94 53.45',
               'a replay-based† method (iCaRL [34] stores 20 samples per old class)',
               'In the CIFAR-100 big-start exemplar-free CIL setting, we report the average incremental accuracy (Aavg).'],
     'raw_file': 'f1/src/pdf_2603.18596v3.txt',
     'agent_note': 'States P2 against the one replay method it reports: CIFAR-100 big start (a large first task, from '
                   'scratch), A_avg at T = 5, 10, 20: EWC-DR 63.75, 60.94, 53.45 vs iCaRL-NCM (20 per old class) 58.56, '
                   '54.19, 50.51. Caveats: supplementary table; iCaRL (2017) is the only replay row; the metric is the '
                   'average incremental accuracy, not the last-task accuracy.'},
    {'id': 'w1:16', 'tag': 'P2', 'reading': 'states', 'reading_by': RB,
     'source': 'Tscheschner, Veas, Masana, "Incremental Learning with Repetition via Pseudo-Feature Projection" (Horde; arXiv:2502.19922)',
     'version': 'v1, 27 Feb 2025', 'url': 'https://arxiv.org/abs/2502.19922',
     'quote': ['The two rehearsal-based methods are excluded from the ranking and serve as an upper baseline (Joint [8]) and a '
               'reference point (Weight-Alignment (WA) [45]; n = 2000).',
               'All methods employ the same base feature extractor, a ResNet-18 [13] model that has been adjusted to the '
               'CIFAR input dimensions',
               'WA [45] 42.7 ± 2.3',
               'Hordem 62.9 ± 1.2',
               'PRAKA [40] 63.1 ± 2.5'],
     'raw_file': 'f1/src/pdf_2502.19922v1.txt',
     'agent_note': 'States P2 in its table, weakly: CIFAR-100 CIL 50/10 (a 50-class first session, no external '
                   'pretraining stated), average accuracy: WA with 2000 exemplars 42.7 vs Horde 62.9 and PRAKA 63.1 '
                   '(exemplar-free). Caveat: WA is the single replay row, a "reference point" excluded from the ranking; '
                   'its value was not checked against WA\'s own paper here.'},
    {'id': 'w1:17', 'tag': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'He, Fang, Chen, Tong, Chen, Wang, Chau, Zhuang, "REAL: Representation Enhanced Analytic Learning for '
               'Exemplar-Free Class-Incremental Learning" (arXiv:2403.13522; Knowledge-Based Systems)',
     'version': 'v3, 17 Dec 2025', 'url': 'https://arxiv.org/abs/2403.13522',
     'quote': ['outperforming existing exemplar-free methods and rivaling exemplar-based approaches.',
               'The base dataset contains half of the full data classes.',
               'With a larger K of 10 or more, REAL-DS even outperforms the leading exemplar-based method, FOSTER, and '
               'maintains this trend with increasing K.',
               'FOSTER [20] × 72.58 67.95 65.67 59.57 65.57 58.44 56.15 52.23',
               'REAL-DS (ours) ✓ 68.88 68.75 68.79 68.42 61.62 61.76 62.18 61.87'],
     'raw_file': 'f1/src/pdf_2403.13522v3.txt',
     'agent_note': 'Close: CIFAR-100, ResNet-32, base half from scratch (warm start), A_K at K = 5, 10, 25, 50: REAL-DS '
                   '61.62, 61.76, 62.18, 61.87 vs FOSTER 65.57, 58.44, 56.15, 52.23 (behind at K = 5, ahead at K >= 10). '
                   'Not states: the exemplar buffer of the replay rows is not stated in the text (the rows follow "the '
                   'official implementations"), and the backbone is frozen after the base phase. First posted 2024; '
                   'current version 2025.'},
    {'id': 'w1:18', 'tag': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Moon, Cho, "Expandable and Differentiable Dual Memories with Orthogonal Regularization for '
               'Exemplar-free Continual Learning" (EDD; arXiv:2511.09871; AAAI 2026)',
     'version': 'v1, 13 Nov 2025', 'url': 'https://arxiv.org/abs/2511.09871',
     'quote': ['In particular, despite using without buffer, it surpasses approaches that employ buffers, demonstrating its '
               'superiority.',
               'for buffer-based methods the memory buffer size was fixed at 500 in all experiments.'],
     'raw_file': 'f1/src/pdf_2511.09871v1.txt',
     'agent_note': 'Close: from scratch, ResNet-18, but the replay buffer is 500 (5 per class on CIFAR-100). S-CIFAR-100 '
                   '10 tasks: EDD 37.24 vs the best buffered rows LUCIR 30.57 and DualNet 28.96 (Table 1; RPC, '
                   '31.08, is regularization-based); plain ER and DER++ are not in the table.'},
    {'id': 'w1:19', 'tag': 'P2', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Khademi Nori, Kim, Wang, "Autoencoder-Based Hybrid Replay for Class-Incremental Learning" (AHR; arXiv:2505.05926; ICML 2025)',
     'version': 'v3, 16 May 2025', 'url': 'https://arxiv.org/abs/2505.05926',
     'quote': ['#Total Exemplars 200 200 200 2000 2000',
               'PEC N N 90.81 ±0.06 55.61 ±0.21 52.41 ±0.33 37.53 ±0.41 28.39 ±0.36',
               'BI-R-SI I W - 38.32 ±1.43 37.48 ±1.96 34.37 ±1.20 29.71 ±1.03',
               'iCaRL I D 93.06 ±0.33 89.63 ±0.61 73.29 ±0.73 49.38 ±0.62 43.51 ±0.68',
               'BiC E D 94.13 ±0.25 91.04 ±0.63 75.01 ±0.93 51.41 ±0.88 44.80 ±0.57'],
     'raw_file': 'f1/src/pdf_2505.05926v3.txt',
     'agent_note': 'Contradicts, on its protocol: CIFAR-100 10 tasks, 2000 exemplars, ResNet-32 (no pretraining named): '
                   'the best exemplar-free rows, PEC 37.53 (generative classifier) and BI-R-SI 34.37 (generative replay), '
                   'vs iCaRL 49.38 and BiC 51.41. Limit: its exemplar-free rows are generative-classifier and generative-'
                   'replay methods; no prototype or drift-compensation EFCIL method is in the table.'},
    {'id': 'w1:20', 'tag': 'P2', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Qiu, Xu, Meng, Zhang, Xu, Wu, Li, "Closing the Oracle Gap: Increment Vector Transformation for Class '
               'Incremental Learning" (IVT; '
               'arXiv:2509.21898)',
     'version': 'v1, 26 Sep 2025', 'url': 'https://arxiv.org/abs/2509.21898',
     'quote': ['The memory size |M| is set to 20 samples per class unless stated otherwise.',
               'For methods trained from scratch, the initial task comprises half of the classes',
               'EOPC [14] ✗ 65.06 55.69 8.93 63.64 54.05 8.24 61.35 51.24 11.94',
               'PODNet [5] ✗ 64.00 (0.54) 54.47 (0.88) 17.72 (0.27) 62.47 (0.51) 52.89 (0.80) 21.57 (0.38) 59.82 (0.84) '
               '50.71 (0.96) 25.90 (0.89) w/ IVT (Ours) ✗ 65.36 (0.24) 56.62 (0.47) 11.68 (0.47) 63.45 (0.72) 55.41 '
               '(0.72) 12.87 (0.47) 61.74 (0.98) 53.43 (1.15) 15.84 (0.76)',
               'FCS [31] ✓ 60.04 (0.14) 50.87 (0.22) 7.61 (0.09) 59.64 (0.06) 49.71 (0.32) 8.92 (0.15) 58.40 (0.06) 46.90 '
               '(0.13) 10.98 (0.27) w/ IVT (Ours) ✓ 60.96 (0.12) 52.07 (0.05) 6.80 (0.42) 60.99 (0.14) 51.63 (0.15) 7.79 '
               '(0.26) 60.18 (0.08) 49.72 (0.21) 7.00 (0.47)'],
     'raw_file': 'f1/src/pdf_2509.21898v1.txt',
     'agent_note': 'Contradicts, on its protocol: CIFAR-100, half the classes first, from scratch, 20 per class. Last '
                   'accuracy at 5, 10, 25 tasks: best exemplar-free (FCS + IVT) 52.07, 51.63, 49.72 vs PODNet + IVT '
                   '56.62, 55.41, 53.43 and EOPC 55.69, 54.05, 51.24 (3.7 to 4.6 points behind the best replay row in each setting). '
                   'Exemplar-free rows are ahead of iCaRL (47.46, 44.55, 40.32 in the same table), so the gap is to '
                   'strong replay only. The exemplar-free rows train 100 epochs with Adam, the replay rows 160 with SGD.'},
    {'id': 'w1:21', 'tag': 'P2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Cho, Moon, Chunara, Cho, Cha, "Forget Forgetting: Continual Learning in a World of Abundant Memory" '
               '(arXiv:2502.07274; ICLR 2026)',
     'version': 'v5, 18 Feb 2026', 'url': 'https://arxiv.org/abs/2502.07274',
     'quote': ['removing exemplars leads to severe performance degradation across all algorithms',
               'DER 63.95±1.9',
               'FOSTER 66.22±1.6',
               'Memory Size Method 0 DER 53.37 FOSTER 26.43 MEMO 43.98 Replay 26.07 iCaRL 29.03 BiC 28.29 WA 42.10',
               'results support our claim that exemplar-free CL is substantially more challenging and currently yields '
               'accuracy that is insufficient for many real-world deployments'],
     'raw_file': 'f1/src/pdf_2502.07274v5.txt',
     'agent_note': 'Bears: CIFAR-100 10 tasks, average class-IL accuracy: at 20 per class DER 63.95, FOSTER 66.22; at zero '
                   'memory the same replay methods fall to 26.07-53.37. Its exemplar-free arms are replay methods with the '
                   'buffer removed, not exemplar-free methods, so the table does not test the position; the general '
                   'assertion leans against it.'},
    {'id': 'w1:22', 'tag': 'P2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Nguyen, Dao, Nguyen, Le, Wong, "Memory-efficient Continual Learning with Prototypical Exemplar '
               'Condensation" (ProtoCore; arXiv:2603.13804; CVPR 2026 Findings, pp. 7675-7685)',
     'version': 'CVF open access camera-ready (quoted); arXiv v2, 10 Apr 2026',
     'url': 'https://openaccess.thecvf.com/content/CVPR2026F/html/Nguyen_Memory-efficient_Continual_Learning_with_'
            'Prototypical_Exemplar_Condensation_CVPRF_2026_paper.html',
     'quote': ['iCaRL 20 25.92±0.78 55.52±0.81 11.25',
               'C-Flat 20 26.81±0.94 65.18±0.56 11.84±0.38 74.95±2.05 14.37±0.68 65.98±1.88 5.05±1.17 63.77±1.54',
               'ADC 0 18.68±0.14 60.73±2.10 11.28±0.58 74.56±2.72 14.58±0.58 65.78±1.52 5.97±0.41 63.85±1.48'],
     'raw_file': 'f1/src/cvf_Nguyen_Memory-efficient_Continual_Learning_with_Prototypical_Exemplar_Condensation_CVPRF_2026_'
                 'paper.txt',
     'agent_note': 'Bears (mixed within one table): last accuracy A_T, replay at 20 per class vs ADC (2024, exemplar-free): '
                   'S-CIFAR-100 T=10 C-Flat 26.81 vs ADC 18.68 (behind); T=50 11.84 vs 11.28 (level); S-TinyImageNet '
                   'T=20 14.37 vs 14.58; S-ImageNet-1K T=100 5.05 vs 5.97 (ahead). The exemplar-free methods are 2024 '
                   'methods run by this paper, and all absolute numbers are low for their settings.'},
]
