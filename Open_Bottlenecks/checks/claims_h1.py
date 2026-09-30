"""OB1 stage 1, family H1 (Open_Bottlenecks/DECLARATION.md): class-incremental, exemplar-free and online continual learning.

Every quote is copied from the text that pymupdf 1.28.2 extracted from the fetched PDF (arXiv current version, or CVF open
access camera-ready), fetched 2026-09-30 through the session proxy. Raw files live outside the repository under
/tmp/claude-0/ob1_src/ (`raw_file` is relative to that root); their sha256 is in /tmp/claude-0/ob1_src/h1/SHA256SUMS.txt and
in the dossier docs/citations/ob1_h1_2026-09-30.md. Table rows are quoted as the extractor emitted them, cell by cell in
reading order. Checked by Open_Bottlenecks/checks/verify.py.

Roles (DECLARATION.md stage 1): a = the problem stated; b = a 2025-26 statement that it is open, unsolved or a main challenge;
c = the best reported result on a named benchmark against the target (numbers quoted; the gap is computed in `agent_note`
and in BOTTLENECKS); d = the method families tried and the assumption each makes. `agent_note` is the agent's reading, not
the source's words. Numbers from different papers are not comparable unless a note says the protocol is shared.
"""

R = 'h1/txt/'

CLAIMS = [
    # ---------------- h1-B1: the gap to joint training when the representation is learned (from scratch, with replay)
    {'id': 'h1:1', 'bottleneck': 'h1-B1', 'role': 'a',
     'source': 'Momeni & Liu, Achieving Upper Bound Accuracy of Joint Training in Continual Learning (survey)',
     'version': 'arXiv v2, 26 Feb 2025 (v1 17 Feb 2025)', 'url': 'https://arxiv.org/abs/2502.12388v2',
     'quote': ['However, a significant gap remains between the accuracy achieved by state-of-the-art continual learning '
               'algorithms and the ideal or upper-bound accuracy achieved by training all tasks together jointly.',
               'Consequently, there is still a major performance gap between the accuracy of state-of-the-art CIL methods '
               'and joint training.'],
     'raw_file': R + '2502.12388v2.txt',
     'agent_note': 'States the problem for class-IL in general. The same paper argues the gap is closed once a strong frozen '
                   'foundation model is used (see h1-B8); the gap stays open where the representation must be learned.'},
    {'id': 'h1:2', 'bottleneck': 'h1-B1', 'role': 'b',
     'source': 'Qiu et al., Closing the Oracle Gap: Increment Vector Transformation for Class Incremental Learning',
     'version': 'arXiv v1, 26 Sep 2025', 'url': 'https://arxiv.org/abs/2509.21898v1',
     'quote': ['Despite recent progress, current CIL methods still exhibit significant performance gaps compared to their '
               'oracle counterparts—models trained with full access to historical data.'],
     'raw_file': R + '2509.21898v1.txt',
     'agent_note': '2025 statement that the gap to the oracle is open. Its own oracle comparison (Fig. 4) is a bar chart; '
                   'no oracle number is extractable from the text, so it is not used for B-c.'},
    {'id': 'h1:3', 'bottleneck': 'h1-B1', 'role': 'b',
     'source': 'Huang et al., DRDN: Decoupled Representation Dynamic Network for From-Scratch ViT Class-Incremental Learning',
     'version': 'arXiv v2, 11 Sep 2026 (v1 2 Jul 2026); preprint submitted to IEEE TMM', 'url': 'https://arxiv.org/abs/2607.01630v2',
     'quote': ['yet our analyses suggest that classification supervision alone does not sufficiently preserve task-agnostic '
               'shared backbone representations over long incremental sequences.',
               'under-optimized shared representations in the backbone that cap long-term discriminability as tasks accumulate.'],
     'raw_file': R + '2607.01630v2.txt',
     'agent_note': '2026 statement of the open difficulty in from-scratch class-IL (shared representation under-optimised as tasks accumulate).'},
    {'id': 'h1:4', 'bottleneck': 'h1-B1', 'role': 'c',
     'source': 'Huang et al., DRDN (Table II)', 'version': 'arXiv v2, 11 Sep 2026', 'url': 'https://arxiv.org/abs/2607.01630v2',
     'quote': ['RESULTS ON CIFAR100-B0 IN THE FROM-SCRATCH VIT REGIME (NO PRETRAINED WEIGHTS, ∼11M PARAMS). BOUND = JOINT-TRAINING UPPER',
               'Bound 10.72 – 81.49 – 10.72 – 81.49 – 10.72 – 81.49 –',
               'DER [3] 56.13 76.80 68.32 -10.8 112.27 75.36 65.22 -12.1 224.55 74.09 62.48 -13.0',
               'DRDN (ours) 10.75 77.91 69.19 -9.8 10.77 77.19 65.40 -11.2 10.80 76.03 59.86 -13.8',
               'Replay buffer: nB = 2,000 (CIFAR100, ImageNet100) or 20,000'],
     'raw_file': R + '2607.01630v2.txt',
     'agent_note': 'Columns per setting: Par., Avg, Last, BWT; settings 5, 10, 20 steps. Last accuracy against the joint bound '
                   '81.49: 5 steps best 69.19 (DRDN), gap 12.30; 10 steps best 65.40 (DRDN), gap 16.09; 20 steps best 62.48 '
                   '(DER, at 224.55M parameters), gap 19.01 (DRDN 59.86, gap 21.63). Replay buffer 2,000. The gap grows with the '
                   'number of steps.'},
    {'id': 'h1:5', 'bottleneck': 'h1-B1', 'role': 'd',
     'source': 'Huang et al., DRDN', 'version': 'arXiv v2, 11 Sep 2026', 'url': 'https://arxiv.org/abs/2607.01630v2',
     'quote': ['Dynamic expansion methods [3]–[5] currently achieve leading performance by growing dedicated task-specific '
               'components — tokens or subnetworks — at each step.',
               'For task-specific discrimination, DRDN employs hierarchical task token expansion across all transformer layers'],
     'raw_file': R + '2607.01630v2.txt',
     'agent_note': 'Expansion family: a new component per step, so task boundaries are given from outside and parameters grow '
                   'with the number of tasks (DER 56.13M -> 224.55M over 5 -> 20 steps in Table II).'},
    {'id': 'h1:6', 'bottleneck': 'h1-B1', 'role': 'd',
     'source': 'Qiu et al., Closing the Oracle Gap (IVT)', 'version': 'arXiv v1, 26 Sep 2025', 'url': 'https://arxiv.org/abs/2509.21898v1',
     'quote': ['IVT periodically teleports the model parameters to transformed solutions that preserve linear connectivity to '
               'previous task optimum.',
               'This is done every I steps by transforming (red arrows) the increment vector (blue dashed line)—the parameter '
               'displacement between the previous optimum θ∗',
               'The transformation is efficiently approximated using diagonal Fisher Information Matrices'],
     'raw_file': R + '2509.21898v1.txt',
     'agent_note': 'Parameter-space family: anchored to the previous task optimum (a task boundary) and applied on a fixed '
                   'step clock (every I steps); importance is a diagonal Fisher.'},
    {'id': 'h1:7', 'bottleneck': 'h1-B1', 'role': 'd',
     'source': 'Momeni & Liu (survey)', 'version': 'arXiv v2, 26 Feb 2025', 'url': 'https://arxiv.org/abs/2502.12388v2',
     'quote': ['It assumes that the foundation model provides strong and sufficient feature representations that can be used '
               'for continual learning in downstream tasks.',
               'While replay mechanisms can help mitigate forgetting, they provide only a limited number of past training '
               'samples, which is insufficient for fully adjusting all learned feature representations to achieve joint '
               'training accuracy.'],
     'raw_file': R + '2502.12388v2.txt',
     'agent_note': 'Frozen-representation family assumes the features never need to change; replay family assumes a small '
                   'stored sample suffices, which the authors say it does not for representation learning.'},

    # ---------------- h1-B2: cold-start exemplar-free class-IL, the gap to joint training
    {'id': 'h1:8', 'bottleneck': 'h1-B2', 'role': 'a',
     'source': 'Jučas & Pan, Data-Free Reservoir Features for Efficient Long-Horizon Cold-Start Continual Learning (CIRCLE)',
     'version': 'arXiv v1, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.27095v1',
     'quote': ['Cold-start exemplar-free class-incremental learning requires learning a growing set of classes without replay, '
               'external pretraining, or a large initial task.'],
     'raw_file': R + '2606.27095v1.txt', 'agent_note': 'The setting stated.'},
    {'id': 'h1:9', 'bottleneck': 'h1-B2', 'role': 'b',
     'source': 'Magistri et al., EFC++: Elastic Feature Consolidation with Prototype Re-balancing for Cold Start Exemplar-free Incremental Learning (IJCV 134, 454, 2026)',
     'version': 'arXiv v4, 28 Sep 2026 (v1 13 Mar 2025, v2 15 Mar 2025, v3 3 Oct 2025)', 'url': 'https://arxiv.org/abs/2503.10439v4',
     'quote': ['As a final note, we report the performance under Joint Training, where the gap remains substantial. Closing this '
               'gap will likely require either a more advanced strategy than Gaussian prototypes or improved regularization '
               'techniques beyond those we proposed.'],
     'raw_file': R + '2503.10439v4.txt', 'agent_note': '2025-26 statement that the gap to joint training is open.'},
    {'id': 'h1:10', 'bottleneck': 'h1-B2', 'role': 'b',
     'source': 'Honda, Adversarial Pseudo-replay for Exemplar-free Class-incremental Learning (APR, WACV 2026)',
     'version': 'arXiv v1, 22 Nov 2025', 'url': 'https://arxiv.org/abs/2511.17973v1',
     'quote': ['even with the use of prototypes, the plasticity-stability dilemma — trade-off between acquiring knowledge from '
               'new tasks (plasticity) and avoiding catastrophic forgetting (stability) — remains unresolved.'],
     'raw_file': R + '2511.17973v1.txt', 'agent_note': '2025 statement (WACV 2026) that the EFCIL trade-off is unresolved.'},
    {'id': 'h1:11', 'bottleneck': 'h1-B2', 'role': 'c',
     'source': 'Honda, APR (Table 1)', 'version': 'arXiv v1, 22 Nov 2025', 'url': 'https://arxiv.org/abs/2511.17973v1',
     'quote': ['The Joint stands for the upper-bound accuracy results, where all the old task classes are available at each task.',
               'Joint Linear 83.25 78.69 84.18 78.69 69.84 65.71 70.54 65.71 87.48 85.39',
               'APR Maha 74.99 65.55 69.96 57.94 60.74 50.77 56.39 44.35 73.86 62.88',
               'Table 1. Average and final incremental accuracy in cold-start EFCIL settings across three benchmarks. Only 1/T '
               'of the total classes are in the initial task.'],
     'raw_file': R + '2511.17973v1.txt',
     'agent_note': 'Columns: CIFAR-100 T=5 (Ainc, Alast), T=10; TinyImageNet T=5, T=10; ImageNet-Subset T=10. APR (Maha) is '
                   'the best row in the table. Final accuracy at T=10 against Joint: CIFAR-100 57.94 vs 78.69 (gap 20.75); '
                   'TinyImageNet 44.35 vs 65.71 (gap 21.36); ImageNet-Subset 62.88 vs 85.39 (gap 22.51). Same paper, same protocol.'},
    {'id': 'h1:12', 'bottleneck': 'h1-B2', 'role': 'c',
     'source': 'Magistri et al., EFC++ (Tables 7 and 8)', 'version': 'arXiv v4, 28 Sep 2026', 'url': 'https://arxiv.org/abs/2503.10439v4',
     'quote': ['Table 7 Impact of Mean and Covariance Drift on EFC++ (CIFAR-100 Cold Start).',
               'EFM Fixed 47.52 ± 0.68 +1.22 (Ours)',
               'EFM Fixed 33.71 ± 1.41 +2.00 (Ours)',
               'Real Real 38.59 ± 1.64 +6.88 Joint Training 71.00',
               'Table 8 Impact of Mean and Covariance Drift on EFC++ (ImageNet-1K Cold Start).',
               'EFM Fixed 44.72 ± 0.11 +1.07 (Ours)',
               'Real Real 45.55 ± 0.06 +11.55 Joint Training 69.76'],
     'raw_file': R + '2503.10439v4.txt',
     'agent_note': 'EFC++ (Ours) final accuracy against Joint Training: CIFAR-100 10 steps 47.52 vs 71.00 (gap 23.48), 20 '
                   'steps 33.71 vs 71.00 (gap 37.29); ImageNet-1K 10 steps 44.72 vs 69.76 (gap 25.04).'},
    {'id': 'h1:13', 'bottleneck': 'h1-B2', 'role': 'd',
     'source': 'Jučas & Pan, CIRCLE', 'version': 'arXiv v1, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.27095v1',
     'quote': ['Existing cold-start methods typically either train the backbone throughout the stream and compensate for '
               'semantic drift, or freeze a backbone after the first task, producing features biased toward the initial classes.',
               'CIRCLE performs sample-wise training without replay, task-boundary information, or backbone backpropagation.'],
     'raw_file': R + '2606.27095v1.txt',
     'agent_note': 'Two families: trained backbone + drift compensation (statistics remapped after each task, so boundaries '
                   'known) and freeze-after-first-task (assumes the first task is representative). CIRCLE (random fixed '
                   'features + streaming LDA) is the third, and assumes features never need learning.'},
    {'id': 'h1:14', 'bottleneck': 'h1-B2', 'role': 'd',
     'source': 'Honda, APR', 'version': 'arXiv v1, 22 Nov 2025', 'url': 'https://arxiv.org/abs/2511.17973v1',
     'quote': ['the shrinkage parameters γ1 and γ2 in eq. 9 are determined by splitting the validation dataset (N=50 per class) '
               'from the train dataset.',
               'APR requires more training time (31.0 hours on Imagenet-Subset T = 10)'],
     'raw_file': R + '2511.17973v1.txt',
     'agent_note': 'Tuning assumption: hyperparameters set on a held-out split of each task (per-class validation data). '
                   'The training time bears on B-e (GPU hours, single RTX4070).'},

    # ---------------- h1-B3: estimating the drift of stored class statistics (against the oracle statistics)
    {'id': 'h1:15', 'bottleneck': 'h1-B3', 'role': 'a',
     'source': 'Jučas & Pan, CIRCLE', 'version': 'arXiv v1, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.27095v1',
     'quote': ['as ϕ changes, old-class features shift and stored head statistics become outdated.'],
     'raw_file': R + '2606.27095v1.txt', 'agent_note': 'The problem stated.'},
    {'id': 'h1:16', 'bottleneck': 'h1-B3', 'role': 'a',
     'source': 'Honda, APR', 'version': 'arXiv v1, 22 Nov 2025', 'url': 'https://arxiv.org/abs/2511.17973v1',
     'quote': ['The major cause of the catastrophic forgetting is the change in the feature extractor, also known as semantic '
               'drift [27] occurring when learning a new task.'],
     'raw_file': R + '2511.17973v1.txt', 'agent_note': 'The problem stated.'},
    {'id': 'h1:17', 'bottleneck': 'h1-B3', 'role': 'b',
     'source': 'Magistri et al., EFC++', 'version': 'arXiv v4, 28 Sep 2026', 'url': 'https://arxiv.org/abs/2503.10439v4',
     'quote': ['This confirms the challenges highlighted in Section 7.2 that our approach encounters when estimating the real '
               'class drift in Cold Start.',
               'From this analysis, we conclude that future work on Gaussian prototypes should prioritize more effective '
               'strategies for updating class means, beyond our current EFM approach.'],
     'raw_file': R + '2503.10439v4.txt', 'agent_note': '2025-26 statement that drift estimation is the open part.'},
    {'id': 'h1:18', 'bottleneck': 'h1-B3', 'role': 'b',
     'source': 'Jučas & Pan, CIRCLE', 'version': 'arXiv v1, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.27095v1',
     'quote': ['Such methods work well at moderate horizons, but drift control is approximate and can accumulate error over '
               'many task transitions.'],
     'raw_file': R + '2606.27095v1.txt', 'agent_note': '2026 statement.'},
    {'id': 'h1:19', 'bottleneck': 'h1-B3', 'role': 'c',
     'source': 'Magistri et al., EFC++ (Table 8, oracle statistics)', 'version': 'arXiv v4, 28 Sep 2026', 'url': 'https://arxiv.org/abs/2503.10439v4',
     'quote': ['an idealized setting using real mean and real covariances, computed from old task data fed in the current task backbone.',
               '10 Fixed Fixed 43.65 ± 0.04 — EFM Fixed 44.72 ± 0.11 +1.07 (Ours) EFM Real 46.50 ± 0.27 +2.85 Real Fixed 49.95 '
               '± 0.09 +6.30 Real Real 49.97 ± 0.09 +6.32 20 Fixed Fixed 34.00 ± 0.03 — EFM Fixed 37.46 ± 0.03 +3.46 (Ours) '
               'EFM Real 38.45 ± 0.01 +4.45 Real Fixed 44.92 ± 0.02 +10.92 Real Real 45.55 ± 0.06 +11.55'],
     'raw_file': R + '2503.10439v4.txt',
     'agent_note': 'ImageNet-1K Cold Start. Estimated drift (EFM means) against the oracle (real means and covariances): '
                   '10 steps 44.72 vs 49.97 (gap 5.25); 20 steps 37.46 vs 45.55 (gap 8.09). The real means alone recover most '
                   'of it (49.95; 44.92). The oracle gap grows with the number of steps.'},
    {'id': 'h1:20', 'bottleneck': 'h1-B3', 'role': 'd',
     'source': 'Jučas & Pan, CIRCLE; Magistri et al., EFC++', 'version': 'arXiv v1, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.27095v1',
     'quote': ['Existing methods mitigate this via rehearsal/augmentation (PASS [Zhu et al., 2021a], IL2A [Zhu et al., 2021b]), '
               'drift estimation (SDC [Yu et al., 2020], ADC [Goswami et al., 2024], LDC [Gomez-Villa et al., 2024], AdaGauss [...] '
               'or distillation-style regularization (LwF [Li and Hoiem, 2016], AdaGauss, EFC, EFC++).'],
     'raw_file': R + '2606.27095v1.txt',
     'agent_note': 'Families: prototype rehearsal, drift estimation from current-task data, distillation. Drift is estimated '
                   'from the current task samples at each task transition (boundary given); stored statistics are fixed between '
                   'transitions.'},
    {'id': 'h1:21', 'bottleneck': 'h1-B3', 'role': 'd',
     'source': 'Magistri et al., EFC++', 'version': 'arXiv v4, 28 Sep 2026', 'url': 'https://arxiv.org/abs/2503.10439v4',
     'quote': ['Since EFC++ does not update class covariances across incremental learning steps'],
     'raw_file': R + '2503.10439v4.txt', 'agent_note': 'Held fixed: the stored covariances.'},

    # ---------------- h1-B4: online (single-pass) class-incremental learning, the gap to offline training
    {'id': 'h1:22', 'bottleneck': 'h1-B4', 'role': 'a',
     'source': 'Khawand & Colliaux, Natural Gradient Descent for Online Continual Learning (NeurIPS 2025 per the PDF header)',
     'version': 'arXiv v1, 21 Mar 2026', 'url': 'https://arxiv.org/abs/2603.20898v1',
     'quote': ['The model is thus required to achieve satisfactory performance from a single pass over the online data stream '
               'using very small batch sizes.'],
     'raw_file': R + '2603.20898v1.txt', 'agent_note': 'The setting stated.'},
    {'id': 'h1:23', 'bottleneck': 'h1-B4', 'role': 'b',
     'source': 'Khawand & Colliaux, NGD for OCL', 'version': 'arXiv v1, 21 Mar 2026', 'url': 'https://arxiv.org/abs/2603.20898v1',
     'quote': ['In this complex scenario, OCL methods struggle to achieve high accuracies as shown in the survey [25]. There is '
               'still a big gap between OCL-trained models and Offline trained models.'],
     'raw_file': R + '2603.20898v1.txt', 'agent_note': '2025-26 statement.'},
    {'id': 'h1:24', 'bottleneck': 'h1-B4', 'role': 'b',
     'source': 'Wen, Heinis & Choi, Balanced Online Class-Incremental Learning via Dual Classifiers (BISON, SAC 2026)',
     'version': 'arXiv v2, 11 Dec 2025 (v1 29 Apr 2025)', 'url': 'https://arxiv.org/abs/2504.20566v2',
     'quote': ['Nevertheless, it still remains a big challenge to achieve a well-balanced learner, as these methods often exhibit '
               'either reduced plasticity or limited stability due to difficulties in continually integrating knowledge in the '
               'OCIL setting.'],
     'raw_file': R + '2504.20566v2.txt', 'agent_note': '2025-26 statement.'},
    {'id': 'h1:25', 'bottleneck': 'h1-B4', 'role': 'b',
     'source': 'Bidaki et al., Online Continual Learning: A Systematic Literature Review of Approaches, Challenges, and Benchmarks',
     'version': 'arXiv v1, 9 Jan 2025', 'url': 'https://arxiv.org/abs/2501.04897v1',
     'quote': ['Although significant progress has been made in OCL, many challenges remain unresolved.'],
     'raw_file': R + '2501.04897v1.txt', 'agent_note': '2025 survey statement (general, not specific to the accuracy gap).'},
    {'id': 'h1:26', 'bottleneck': 'h1-B4', 'role': 'c',
     'source': 'Khawand & Colliaux, NGD for OCL (Table 2)', 'version': 'arXiv v1, 21 Mar 2026', 'url': 'https://arxiv.org/abs/2603.20898v1',
     'quote': ['Table 2: End Average Accuracy of methods and tricks with or without NGD-KFAC for the OCI setting on Split CIFAR-100.',
               'Offline 49.7 ± 2.6',
               'RV [7] × 6.6 ± 0.4 15.7 ± 1.5 24.2 ± 1.3 14.6 ± 0.4 31.2 ± 1.0 36.8 ± 1.1 13.2 ± 0.6 30.8 ± 0.8 38.1 ± 1.2 '
               '6.9 ± 0.3 10.7 ± 0.7 22.4 ± 1.0 13.7 ± 0.5 34.2 ± 0.3 39.9 ± 0.5 12.3 ± 0.5 31.7 ± 0.7 39.6 ± 0.5',
               'SS [1] × 8.3 ± 0.5 8.7 ± 0.5 8.6 ± 0.4 16.9 ± 0.8 23.8 ± 1.2 25.5 ± 1.1 17.4 ± 0.8 25.0 ± 0.9 26.8 ± 1.1 '
               '11.9 ± 0.9 12.4 ± 0.7 11.9 ± 0.7 20.3 ± 0.5 28.8 ± 0.7 33.0 ± 0.6 20.3 ± 0.6 28.4 ± 0.8 32.6 ± 0.8',
               'Offline: We train the model offline for 70 epochs with a batch size of 128.'],
     'raw_file': R + '2603.20898v1.txt',
     'agent_note': "Agent's reading of the table: columns A-GEM, ER, MIR at M = 1k, 5k, 10k; each trick has a row without "
                   "NGD-KFAC (the '×') followed by a row with it (the check glyph was not extracted). Best cell: RV trick + "
                   "NGD-KFAC, ER, M=10k, 39.9 vs Offline 49.7: gap 9.8 with a buffer of 10k of the 50k training images. At "
                   "M=1k the best is 20.3 (SS + NGD-KFAC): gap 29.4. Offline is a 70-epoch i.i.d. reference, not tuned further."},
    {'id': 'h1:27', 'bottleneck': 'h1-B4', 'role': 'c',
     'source': 'Lai et al., Beyond Myopic Alignment: Lookahead Optimization for Online Class-Incremental Learning (LOR, CVPR 2026, pp. 18053-18062)',
     'version': 'CVF open access camera-ready (no version number)',
     'url': 'https://openaccess.thecvf.com/content/CVPR2026/html/Lai_Beyond_Myopic_Alignment_Lookahead_Optimization_for_Online_Class-Incremental_Learning_CVPR_2026_paper.html',
     'quote': ['Table 2. Average Accuracy (Acc) comparison with baseline methods on Seq-CIFAR10, Seq-CIFAR100, and Seq-TinyImageNet using Reduced ResNet-18.',
               'LOR 57.21±1.05 71.47±0.95 18.21±0.30 39.02±1.10 12.77±0.40 20.25±0.80'],
     'raw_file': R + 'cvf_Lai_Beyond_Myopic_Alignment_Lookahead_Optimization_for_Online_Class-Incremental_Learning_CVPR_2026_paper.txt',
     'agent_note': 'Supporting number only: Seq-CIFAR100 (N=20) with M=1k 18.21, M=5k 39.02, level with the NGD paper\'s best. '
                   'LOR reports no offline or joint row, so its gap is not computed.'},
    {'id': 'h1:28', 'bottleneck': 'h1-B4', 'role': 'd',
     'source': 'Khawand & Colliaux, NGD for OCL', 'version': 'arXiv v1, 21 Mar 2026', 'url': 'https://arxiv.org/abs/2603.20898v1',
     'quote': ['We run our tests using a Resnet18 [15] with a learning rate of 0.1, and a fixed batch size of 10 to mimic a '
               'realistic Online Learning Scenario.',
               'Review trick [7]: Adds an additional fine-tuning step using a balanced subset of the memory buffer.',
               'We focus our attention on the methods that do not require access to task labels'],
     'raw_file': R + '2603.20898v1.txt',
     'agent_note': 'Replay + tricks family: fixed buffer M, fixed learning rate and batch, a review step on a balanced buffer '
                   'subset (applied at the end of training/tasks).'},
    {'id': 'h1:29', 'bottleneck': 'h1-B4', 'role': 'd',
     'source': 'Bidaki et al., OCL systematic review', 'version': 'arXiv v1, 9 Jan 2025', 'url': 'https://arxiv.org/abs/2501.04897v1',
     'quote': ['Hyperparameter optimization poses a critical challenge during the OCL phase, as hyperparameters must be '
               'recalibrated whenever data distributions shift.'],
     'raw_file': R + '2501.04897v1.txt', 'agent_note': 'Tuning assumption named as a challenge.'},
    {'id': 'h1:30', 'bottleneck': 'h1-B4', 'role': 'd',
     'source': 'Lai et al., LOR (CVPR 2026)', 'version': 'CVF open access camera-ready',
     'url': 'https://openaccess.thecvf.com/content/CVPR2026/html/Lai_Beyond_Myopic_Alignment_Lookahead_Optimization_for_Online_Class-Incremental_Learning_CVPR_2026_paper.html',
     'quote': ['These methods maintain a small memory buffer of samples from past tasks and replay them alongside current data.',
               'A fundamental problem persists: the optimization objective for the current task often conflicts with the '
               'objective for preserving past knowledge.'],
     'raw_file': R + 'cvf_Lai_Beyond_Myopic_Alignment_Lookahead_Optimization_for_Online_Class-Incremental_Learning_CVPR_2026_paper.txt',
     'agent_note': 'Rehearsal + gradient-conflict (hypergradient, lookahead) family; stored raw samples in a fixed buffer.'},
    {'id': 'h1:31', 'bottleneck': 'h1-B4', 'role': 'd',
     'source': 'Wen, Heinis & Choi, BISON', 'version': 'arXiv v2, 11 Dec 2025', 'url': 'https://arxiv.org/abs/2504.20566v2',
     'quote': ['Most existing methods rely on explicit knowledge interaction through experience replay, and often employ '
               'exclusive training separation to address bias problems.'],
     'raw_file': R + '2504.20566v2.txt', 'agent_note': 'Replay + old/new separation of the classifier.'},

    # ---------------- h1-B5: long task sequences (50-500 tasks)
    {'id': 'h1:32', 'bottleneck': 'h1-B5', 'role': 'a',
     'source': 'Jučas & Pan, CIRCLE', 'version': 'arXiv v1, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.27095v1',
     'quote': ['the behavior of these methods at much longer horizons remains underexplored.',
               'find that performance degrades sharply for trained-backbone drift-compensation methods in this regime.'],
     'raw_file': R + '2606.27095v1.txt', 'agent_note': 'The problem stated (cold start, from scratch).'},
    {'id': 'h1:33', 'bottleneck': 'h1-B5', 'role': 'b',
     'source': 'Lou, Fu & Yu, Scaling Continual Learning to 300+ Tasks with Bi-Level Routing Mixture-of-Experts (CaRE, ICML 2026)',
     'version': 'arXiv v2, 8 May 2026 (v1 3 Feb 2026)', 'url': 'https://arxiv.org/abs/2602.03473v2',
     'quote': ['However, how to effectively learn both discriminative and comprehensive feature representations while '
               'maintaining stability and plasticity over very long task sequences remains an open problem.'],
     'raw_file': R + '2602.03473v2.txt', 'agent_note': '2026 statement (pre-trained-model class-IL).'},
    {'id': 'h1:34', 'bottleneck': 'h1-B5', 'role': 'c',
     'source': 'Jučas & Pan, CIRCLE (Table 1, CIFAR-100 cold start)', 'version': 'arXiv v1, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.27095v1',
     'quote': ['For our CIRCLE, AT is invariant across task splits because continual training for CIRCLE is equivalent to joint training.',
               'EFC++ 66.61 ± 0.2 52.68 ± 0.4 55.74 ± 0.1 42.10 ± 0.5 38.93 ± 0.2 26.95 ± 0.4 26.73 ± 0.6 16.40 ± 0.3',
               'CIRCLE 55.32 ± 0.3 45.34 ± 0.3 55.90 ± 0.3 45.34 ± 0.3 56.97 ± 0.3 45.35 ± 0.3 57.22 ± 0.3 45.34 ± 0.3'],
     'raw_file': R + '2606.27095v1.txt',
     'agent_note': 'Columns T=10, 20, 50, 100 (mean incremental A, final AT). At T=100 the best final accuracy is CIRCLE 45.34 '
                   '(random fixed features, whose continual training equals its own joint training); the best trained-backbone '
                   'method is EFC++ 16.40, down from 52.68 at T=10 (-36.28). The paper gives no joint-training row for a '
                   'learned backbone; the target used in BOTTLENECKS is EFC++\'s own Joint Training 71.00 on CIFAR-100 cold '
                   'start (claim h1:12), a CROSS-PAPER target (same method family and dataset, protocols not verified equal).'},
    {'id': 'h1:35', 'bottleneck': 'h1-B5', 'role': 'c',
     'source': 'Lou, Fu & Yu, CaRE (Table 1, OmniBenchmark-1K)', 'version': 'arXiv v2, 8 May 2026', 'url': 'https://arxiv.org/abs/2602.03473v2',
     'quote': ['Table 1. Comparison of average and last accuracy on very long task sequences using the OmniBenchmark-1K dataset.',
               'CaRE (Ours) 77.65 69.01 77.18 68.51'],
     'raw_file': R + '2602.03473v2.txt',
     'agent_note': 'Best result at 151 and 301 tasks (last accuracy 69.01, 68.51) with a ViT-B/16-IN21K pre-trained model. '
                   'No joint-training or oracle row is reported, so no gap is computed from this source.'},
    {'id': 'h1:36', 'bottleneck': 'h1-B5', 'role': 'd',
     'source': 'Lou, Fu & Yu, CaRE', 'version': 'arXiv v2, 8 May 2026', 'url': 'https://arxiv.org/abs/2602.03473v2',
     'quote': ['construct a set of task-specific adapters during continual training and activate appropriate adapters at inference time',
               'train for 20 epochs per task.'],
     'raw_file': R + '2602.03473v2.txt',
     'agent_note': 'Adapter/router-per-task family: task boundaries given, one component per task, fixed epochs per task.'},
    {'id': 'h1:37', 'bottleneck': 'h1-B5', 'role': 'd',
     'source': 'Jučas & Pan, CIRCLE', 'version': 'arXiv v1, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.27095v1',
     'quote': ['They are also computationally expensive, with per-task cost growing with the number of seen classes [Magistri et al., 2025].'],
     'raw_file': R + '2606.27095v1.txt', 'agent_note': 'Cost of the drift-compensation family grows with the horizon.'},

    # ---------------- h1-B6: the stability gap (transient forgetting at each task switch, even under joint training)
    {'id': 'h1:38', 'bottleneck': 'h1-B6', 'role': 'a',
     'source': 'Rodriguez-Garcia, Ghosh & Ramaswamy, Dynamic gain neuromodulation attenuates the stability gap under joint training',
     'version': 'arXiv v3, 10 Aug 2026 (v1 18 Jul 2025, v2 27 Jan 2026); OpenReview lists a submission to ICLR 2026',
     'url': 'https://arxiv.org/abs/2507.14056v3',
     'quote': ['Recent work in continual learning has highlighted the stability gap – a temporary performance drop on previously '
               'learned tasks when new ones are introduced.'],
     'raw_file': R + '2507.14056v3.txt', 'agent_note': 'The problem stated.'},
    {'id': 'h1:39', 'bottleneck': 'h1-B6', 'role': 'b',
     'source': 'Rodriguez-Garcia et al.', 'version': 'arXiv v3, 10 Aug 2026', 'url': 'https://arxiv.org/abs/2507.14056v3',
     'quote': ['While optimizers such as momentum-SGD and Adam introduce implicit multi-timescale behavior, they still exhibit '
               'pronounced stability gaps. Importantly, these gaps persist even under ideal joint training',
               'Table 1 shows that NGM-SGD consistently reduces the stability gap, although the performance gains are less '
               'pronounced than hypothesized in prior work (Hess et al., 2024).'],
     'raw_file': R + '2507.14056v3.txt', 'agent_note': '2025-26 statement; the proposed fix reduces but does not remove it.'},
    {'id': 'h1:40', 'bottleneck': 'h1-B6', 'role': 'c',
     'source': 'Rodriguez-Garcia et al. (Table 1)', 'version': 'arXiv v3, 10 Aug 2026', 'url': 'https://arxiv.org/abs/2507.14056v3',
     'quote': ['avg-ACC (↑) avg-min-ACC (↑) WC-ACC (↑) avg-SG (↓)',
               'Split CIFAR-10 NGM-SGD (ours) 90.630 ± 1.576 79.485 ± 3.875 80.880 ± 3.349 0.134 ± 0.043',
               'Split mini-ImageNet NGM-SGD (ours) 48.312 ± 2.289 33.165 ± 2.435 36.040 ± 2.058 0.300 ± 0.071',
               'The average minimum accuracy (avg-min-ACC) captures the lowest accuracy reached per task, averaged across tasks'],
     'raw_file': R + '2507.14056v3.txt',
     'agent_note': 'Best (the proposed method) under joint training. Target: no transient drop, i.e. avg-min-ACC equal to the '
                   'final avg-ACC (avg-SG 0). Split CIFAR-10: 79.485 vs 90.630 (dip 11.145), avg-SG 0.134; Split mini-ImageNet: '
                   '33.165 vs 48.312 (dip 15.147), avg-SG 0.300.'},
    {'id': 'h1:41', 'bottleneck': 'h1-B6', 'role': 'd',
     'source': 'Rodriguez-Garcia et al.', 'version': 'arXiv v3, 10 Aug 2026', 'url': 'https://arxiv.org/abs/2507.14056v3',
     'quote': ['Standard optimizers such as momentum-SGD (MSGD) (Rumelhart et al., 1986) and Adam (Kingma and Ba, 2015) '
               'introduce implicit multi-timescale regularization through momentum or adaptive learning rates, yet they still '
               'exhibit stability gaps.',
               'we introduce a dynamic gain scaling mechanism as a two-timescale optimization technique',
               'As a result, models tend to be updated less often or are retrained entirely from scratch, which is computationally expensive.'],
     'raw_file': R + '2507.14056v3.txt',
     'agent_note': 'Optimiser family: fixed-timescale momentum / adaptive rates on the step clock; the proposed fix adds a '
                   'second (fast) timescale. Deployment workaround: update less often.'},

    # ---------------- h1-B7 (not shown open): class/task order sensitivity
    {'id': 'h1:42', 'bottleneck': 'h1-B7', 'role': 'a',
     'source': 'Mitchell et al., Continual Learning Should Move Beyond Incremental Classification (position)',
     'version': 'arXiv v1, 17 Feb 2025', 'url': 'https://arxiv.org/abs/2502.11927v1',
     'quote': ['Wang et al. (2022) showed that most existing continual learning algorithms suffer drastic fluctuations in '
               'performance under different schedules.'],
     'raw_file': R + '2502.11927v1.txt', 'agent_note': 'The problem stated.'},
    {'id': 'h1:43', 'bottleneck': 'h1-B7', 'role': 'a',
     'source': 'Chen et al., CLDyB: Towards Dynamic Benchmarking for Continual Learning with Pre-trained Models (ICLR 2025)',
     'version': 'arXiv v2, 23 May 2025 (v1 6 Mar 2025)', 'url': 'https://arxiv.org/abs/2503.04655v2',
     'quote': ['compared to random task sequences drawn from the data pool, performance on the CLDyB sequences results in a 26% '
               'reduction in Final Acc and a 9% reduction in Final AR across the evaluated methods'],
     'raw_file': R + '2503.04655v2.txt',
     'agent_note': 'A quantitative statement of the problem (adversarially chosen task sequences), aggregated across methods; '
                   'not a best-method result against a target, so it is not counted as B-c.'},
    {'id': 'h1:50', 'bottleneck': 'h1-B7', 'role': 'a',
     'source': 'Lou, Fu & Yu, CaRE (Appendix A.1, Table 8, OmniBenchmark-1K 100 tasks, four task orders)',
     'version': 'arXiv v2, 8 May 2026', 'url': 'https://arxiv.org/abs/2602.03473v2',
     'quote': ['CIL methods such as MOS and TUNA exhibit relatively high std in AB (0.88 and 1, respectively), indicating their '
               'sensitivity to task ordering in long-sequence evaluations.',
               'our CaRE achieves the lowest std (0.16 in AB)',
               'SEMA 56.97 ± 0.32 32.23 ± 1.50'],
     'raw_file': R + '2602.03473v2.txt',
     'agent_note': 'Order sensitivity with a pre-trained ViT is small in absolute terms (std 0.16 to 1.50 points in last '
                   'accuracy over four orders); no target is stated, so it is not counted as B-c. Id out of sequence: added '
                   'after h1:49.'},
    {'id': 'h1:44', 'bottleneck': 'h1-B7', 'role': 'b',
     'source': 'Lai et al., Order-Robust Class Incremental Learning: Graph-Driven Dynamic Similarity Grouping (CVPR 2025, pp. 4894-4904)',
     'version': 'CVF open access camera-ready (no version number)',
     'url': 'https://openaccess.thecvf.com/content/CVPR2025/html/Lai_Order-Robust_Class_Incremental_Learning_Graph-Driven_Dynamic_Similarity_Grouping_CVPR_2025_paper.html',
     'quote': ['Thus, designing a model capable of maintaining stable performance across varying class orders remains a critical '
               'unsolved issue in CIL.'],
     'raw_file': R + 'cvf_Lai_Order-Robust_Class_Incremental_Learning_Graph-Driven_Dynamic_Similarity_Grouping_CVPR_2025_paper.txt',
     'agent_note': '2025 statement. Its order-robustness numbers (MOPD, AOPD) appear only in a bar chart (Fig. 4); none is '
                   'extractable from the text, so there is no B-c.'},
    {'id': 'h1:45', 'bottleneck': 'h1-B7', 'role': 'd',
     'source': 'Lai et al., Order-Robust CIL (CVPR 2025)', 'version': 'CVF open access camera-ready',
     'url': 'https://openaccess.thecvf.com/content/CVPR2025/html/Lai_Order-Robust_Class_Incremental_Learning_Graph-Driven_Dynamic_Similarity_Grouping_CVPR_2025_paper.html',
     'quote': ['Although existing research, such as APD [58] and HALRP [21], have attempted to mitigate the class order '
               'sensitivity problem by modifying network structures, their effectiveness remains limited',
               'Our framework leverages a frozen pre-trained feature extractor'],
     'raw_file': R + 'cvf_Lai_Order-Robust_Class_Incremental_Learning_Graph-Driven_Dynamic_Similarity_Grouping_CVPR_2025_paper.txt',
     'agent_note': 'Structural (APD, HALRP) and grouping-over-frozen-features families.'},

    # ---------------- h1-B8 (not shown open): the gap to joint training on top of a strong frozen pre-trained model
    {'id': 'h1:46', 'bottleneck': 'h1-B8', 'role': 'a',
     'source': 'Momeni, Xiao & Liu, AnaCP: Toward Upper-Bound Continual Learning via Analytic Contrastive Projection',
     'version': 'arXiv v1, 17 Nov 2025', 'url': 'https://arxiv.org/abs/2511.13880v1',
     'quote': ['as the inability to match joint training remains a key barrier to the practical adoption of CL.'],
     'raw_file': R + '2511.13880v1.txt', 'agent_note': 'The problem stated, in a paper that reports closing it with a strong PTM.'},
    {'id': 'h1:47', 'bottleneck': 'h1-B8', 'role': 'c',
     'source': 'Momeni, Xiao & Liu, AnaCP (Table 1, DINO-v2)', 'version': 'arXiv v1, 17 Nov 2025', 'url': 'https://arxiv.org/abs/2511.13880v1',
     'quote': ['Joint fine-tuning - 93.35±0.00 - 88.79±0.01 - 89.87±0.01 - 88.81±0.02 - 89.92±0.02',
               'AnaCP 95.43±0.20 92.15±0.09 90.37±0.11 86.60±0.04 93.84±0.31 90.57±0.15 91.57±0.29 87.35±0.29 94.16±0.61 90.65±0.24',
               'Notably, on two datasets, AnaCP even exceeds this upper bound, while on the remaining datasets, the largest '
               'accuracy gap is only around 2%.'],
     'raw_file': R + '2511.13880v1.txt',
     'agent_note': 'Columns CIFAR100, ImageNet-R, CUB, TinyImageNet, Cars (Aavg, Alast). Alast vs joint fine-tuning: CIFAR100 '
                   '92.15 vs 93.35 (gap 1.20); ImageNet-R 86.60 vs 88.79 (2.19); CUB 90.57 vs 89.87 (ahead); TinyImageNet '
                   '87.35 vs 88.81 (1.46); Cars 90.65 vs 89.92 (ahead). The source states the target is reached.'},
    {'id': 'h1:48', 'bottleneck': 'h1-B8', 'role': 'c',
     'source': 'Momeni & Liu (Table 2, KLDA with frozen DINOv2)', 'version': 'arXiv v2, 26 Feb 2025', 'url': 'https://arxiv.org/abs/2502.12388v2',
     'quote': ['DINOv2-base CIFAR10 98.54±0.06 98.45±0.04 CIFAR100 90.30±0.09 88.81±0.07 T-ImageNet 86.43±0.14 83.18±0.11',
               'In image classification, KLDA achieves results on par with Joint on two datasets, while a small performance gap '
               'persists on CIFAR-100 and TinyImageNet.'],
     'raw_file': R + '2502.12388v2.txt',
     'agent_note': 'Columns Joint, KLDA-E. CIFAR-100 88.81 vs 90.30 (gap 1.49); TinyImageNet 83.18 vs 86.43 (gap 3.25).'},
    {'id': 'h1:49', 'bottleneck': 'h1-B8', 'role': 'd',
     'source': 'Momeni, Xiao & Liu, AnaCP (Limitations)', 'version': 'arXiv v1, 17 Nov 2025', 'url': 'https://arxiv.org/abs/2511.13880v1',
     'quote': ['However, with a weaker PTM such as MoCo-v3, AnaCP cannot match joint fine-tuning accuracy due to the critical '
               'role of PTM features played in our method.',
               'In this case, the gap to joint fine-tuning increases to 6%'],
     'raw_file': R + '2511.13880v1.txt',
     'agent_note': 'The assumption: a strong frozen pre-trained feature extractor whose features are never learned by '
                   'gradient; the closure depends on it (6% gap with MoCo-v3). The source frames the weaker-PTM case as "a '
                   'meaningful goal", not as an open problem; read here as the assumption, not as B-b.'},
]

BOTTLENECKS = [
    {'id': 'h1-B1', 'name': 'Gap to joint training when the representation is learned',
     'problem': 'Class-incremental learners that must learn their features (no pre-trained model) stay well below joint '
                'training, even with a replay buffer, and the gap grows with the number of steps.',
     'open': True, 'benchmark': 'CIFAR100-B0, from-scratch ViT (~11M params), replay buffer 2,000 (DRDN Table II)',
     'best': 'Last 65.40 at 10 steps (DRDN); 62.48 at 20 steps (DER, 224.55M params)',
     'target': 'Bound (joint training) 81.49',
     'gap_note': '16.09 points at 10 steps, 19.01 at 20 steps (12.30 at 5 steps); same paper, same protocol.',
     'assumptions': ['task boundaries given; a component (token, subnetwork) added per task, parameters grow with tasks',
                     'fixed raw-sample replay buffer (2,000)',
                     'parameter-space consolidation anchored to the previous task optimum, applied every I steps (clock)',
                     'or: features frozen from a pre-trained model (removes the problem by assumption)'],
     'cpu_testable': False,
     'cpu_note': 'the named benchmark trains ViTs/ResNets from scratch over 5-20 steps on GPU; a reduced proxy (small CNN, '
                 'Split CIFAR-100 subsets) could run on CPU in hours but is not the benchmark'},
    {'id': 'h1-B2', 'name': 'Cold-start exemplar-free class-IL gap to joint training',
     'problem': 'With no stored samples, no pre-training and a small first task, the best exemplar-free methods finish about '
                '20-25 points below joint training.',
     'open': True, 'benchmark': 'CIFAR-100 / TinyImageNet / ImageNet-Subset cold start, T=10, ResNet-18 (APR Table 1); '
                                'EFC++ Tables 7-8 (CIFAR-100, ImageNet-1K)',
     'best': 'Alast 57.94 (CIFAR-100), 44.35 (TinyImageNet), 62.88 (ImageNet-Subset) (APR Maha); EFC++ 47.52 (CIFAR-100 10 '
             'steps), 44.72 (ImageNet-1K 10 steps)',
     'target': 'Joint 78.69, 65.71, 85.39 (APR); Joint Training 71.00, 69.76 (EFC++)',
     'gap_note': 'APR: 20.75, 21.36, 22.51 points; EFC++: 23.48 (CIFAR-100), 25.04 (ImageNet-1K), 37.29 at 20 steps on '
                 'CIFAR-100; each within one paper.',
     'assumptions': ['train the backbone throughout and remap stored statistics at each task transition (boundaries given)',
                     'or freeze the backbone after the first task (first task assumed representative)',
                     'stored class means/covariances as the only memory; covariances held fixed',
                     'hyperparameters (shrinkage, lambda) set on a held-out split of each task'],
     'cpu_testable': False,
     'cpu_note': 'ResNet-18 from scratch over 10-20 tasks with 100+ epochs per task is GPU-scale (APR reports 31.0 h on '
                 'ImageNet-Subset on a GPU); only a reduced proxy fits a laptop CPU in hours'},
    {'id': 'h1-B3', 'name': 'Estimating the drift of stored class statistics',
     'problem': 'Prototype-based exemplar-free learners cannot estimate how old-class statistics move when the backbone '
                'changes; replacing the estimate by the true statistics (oracle) recovers several points.',
     'open': True, 'benchmark': 'ImageNet-1K cold start, 10 and 20 steps (EFC++ Table 8)',
     'best': 'EFM Fixed 44.72 (10 steps), 37.46 (20 steps)',
     'target': 'Real Real (oracle statistics) 49.97 (10 steps), 45.55 (20 steps)',
     'gap_note': '5.25 points at 10 steps, 8.09 at 20 steps; the gap grows with steps; real means alone recover most of it.',
     'assumptions': ['drift estimated from current-task samples only, at each task transition (boundary given)',
                     'statistics fixed between transitions; covariances never updated',
                     'drift modelled as a smooth (often affine or low-rank) map of the feature space'],
     'cpu_testable': False,
     'cpu_note': 'the named benchmark is ImageNet-1K; the oracle-vs-estimate gap itself could be measured on a small '
                 'synthetic or reduced stream on CPU (a proxy, not the benchmark)'},
    {'id': 'h1-B4', 'name': 'Online single-pass class-IL gap to offline training',
     'problem': 'Learning each sample once in small batches with a bounded buffer leaves online class-IL far below offline '
                'i.i.d. training.',
     'open': True, 'benchmark': 'Split CIFAR-100 OCI, (reduced) ResNet-18, batch 10 (NGD for OCL Table 2)',
     'best': '39.9 ± 0.5 (RV trick + NGD-KFAC, ER, M=10k); 20.3 at M=1k',
     'target': 'Offline 49.7 ± 2.6',
     'gap_note': '9.8 points with 10k of 50k images stored; 29.4 points at M=1k (same paper). LOR (CVPR 2026) reaches 39.02 '
                 'at M=5k on its own protocol, with no offline row.',
     'assumptions': ['fixed-size raw-sample buffer; reservoir-type storage', 'fixed learning rate and batch size (tuned '
                     'beforehand); hyperparameters must be recalibrated when the distribution shifts',
                     'review/balancing steps on the buffer, gradient-conflict corrections computed per step',
                     'task labels not required at training (task-free variants)'],
     'cpu_testable': True,
     'cpu_note': 'one pass over Split CIFAR-100 with a reduced ResNet-18 and batch 10 is about an hour of CPU per run; the '
                 '70-epoch offline reference is several hours; public data'},
    {'id': 'h1-B5', 'name': 'Long task sequences (50-500 tasks)',
     'problem': 'Trained-backbone class-IL collapses as the number of tasks grows to 50-500, and pre-trained-model methods '
                'are only starting to be evaluated there.',
     'open': True, 'benchmark': 'CIFAR-100 cold start, T=100 (CIRCLE Table 1); OmniBenchmark-1K 100-301 tasks (CaRE)',
     'best': 'AT 45.34 (CIRCLE, fixed random features); 16.40 (EFC++, best trained backbone)',
     'target': 'Joint Training 71.00 (EFC++ paper, CIFAR-100 cold start; CROSS-PAPER)',
     'gap_note': '25.66 points for the best method, 54.60 for the best trained backbone; the in-paper collapse of EFC++ from '
                 'T=10 to T=100 is 36.28 points. The target is from another paper (flagged); CaRE gives no joint row.',
     'assumptions': ['one adapter/router per task with given boundaries; fixed epochs per task',
                     'drift compensation per transition, cost growing with seen classes',
                     'or features never learned (random or pre-trained, frozen)'],
     'cpu_testable': False,
     'cpu_note': 'frozen-feature arms (CIRCLE-type) run on CPU, but the trained-backbone arms at T=100 and the ViT-B/16 '
                 'OmniBenchmark runs do not fit in hours'},
    {'id': 'h1-B6', 'name': 'Stability gap at task switches',
     'problem': 'Accuracy on old tasks drops transiently at every task switch, even under joint training on all past data.',
     'open': True, 'benchmark': 'Split CIFAR-10 and Split mini-ImageNet class-incremental, joint training (Table 1)',
     'best': 'avg-min-ACC 79.485 / avg-SG 0.134 (CIFAR-10); 33.165 / 0.300 (mini-ImageNet) (NGM-SGD)',
     'target': 'no transient drop: avg-min-ACC equal to avg-ACC 90.630 / 48.312 (avg-SG 0)',
     'gap_note': 'transient dip 11.145 points (CIFAR-10), 15.147 points (mini-ImageNet) for the best method; same paper.',
     'assumptions': ['optimiser timescales (momentum, adaptive rates) fixed on the step clock',
                     'the fix adds a second, faster timescale driven by the loss at transitions',
                     'deployment workaround: update less often or retrain from scratch'],
     'cpu_testable': True,
     'cpu_note': 'Split MNIST / Split CIFAR-10 with small networks and per-step evaluation run on CPU in minutes to hours '
                 '(note: MNIST is SEEN in this repository)'},
    {'id': 'h1-B7', 'name': 'Class/task order sensitivity',
     'problem': 'Class-IL accuracy changes with the order in which classes or tasks arrive.',
     'open': False, 'benchmark': 'CLDyB sequences (ICLR 2025); order-robust CIL (CVPR 2025)',
     'best': 'none quoted (order-robustness numbers only in a bar chart; CLDyB gives an aggregate 26% reduction)',
     'target': 'order invariance (stated goal), no number',
     'gap_note': 'not shown open: 2025 statements exist but no best-method number against a target was extractable.',
     'assumptions': ['structural changes (APD, HALRP)', 'class grouping over a frozen pre-trained extractor'],
     'cpu_testable': True, 'cpu_note': 'order permutations on small benchmarks are cheap; frozen-feature methods run on CPU'},
    {'id': 'h1-B8', 'name': 'Gap to joint training with a strong frozen pre-trained model',
     'problem': 'Whether class-IL on top of a strong frozen pre-trained model still falls short of joint training.',
     'open': False, 'benchmark': 'CIFAR100, ImageNet-R, CUB, TinyImageNet, Cars with DINO-v2 (AnaCP Table 1)',
     'best': 'AnaCP Alast 92.15 (CIFAR100), 86.60 (ImageNet-R)', 'target': 'Joint fine-tuning 93.35, 88.79',
     'gap_note': 'not shown open: the sources state the target is reached (gaps 1.20-2.19, ahead on two datasets); the '
                 'residual 6% with a weaker PTM (MoCo-v3) is framed as a goal, not an open problem.',
     'assumptions': ['a strong frozen pre-trained extractor; features never updated by gradient',
                     'analytic heads updated by sufficient statistics (order-free, boundary-free)'],
     'cpu_testable': True,
     'cpu_note': 'with features extracted once by a frozen ViT (about an hour on CPU for CIFAR-100), analytic heads run in minutes'},
]
