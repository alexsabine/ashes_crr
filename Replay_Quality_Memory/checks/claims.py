"""Claims for Replay_Quality_Memory/DECLARATION.md §2 (positions M1-M7), transcribed from the four verified dossiers
docs/citations/rqm_q{1,2,3,4}_2026-09-30.md (fetched 2026-09-30; extracted texts held outside the repository under
/tmp/claude-0/rqm_src/<family>/, named in `raw_file` relative to that root). Every quote is copied from a dossier
blockquote; verify.py checks each against its extracted text.

'reading' is decided by the grading agent from the quote, for the investigator's review ('reading_by'). The dossiers' own
tags were read but not copied: where this file differs from a dossier tag, the agent_note says why. Reading policy, fixed
before the readings were written and applied to every position:
  states       the source asserts (or reports as its own result) every predicate of the position, for at least one of the
               objects the position names, within the position's scope;
  close        the source asserts part of the position, or the position in a narrower or different scope;
  bears        relevant evidence or a bound that neither asserts nor negates the position;
  contradicts  the source asserts or reports the negation of the position within its scope. For an existential position
               ('can approach', 'can be compensated', 'can leak') the negation is 'cannot': a failure in a sub-regime the
               position does not claim is a bound ('bears'). For a universal position ('the main bottleneck is', 'equals
               exactly', 'stay well below') an in-scope counterexample contradicts it in part.
"""

RB = "grading agent; for the investigator's review"

CLAIMS = [
    # ------------------------------------------------------------------ M1
    {'id': 'q1:0', 'tag': 'M1', 'reading': 'states', 'reading_by': RB,
     'source': 'Goswami, Liu, Twardowski, van de Weijer, "FeCAM: Exploiting the Heterogeneity of Class Distributions in '
               'Exemplar-Free Continual Learning" (arXiv:2309.14062; NeurIPS 2023)',
     'version': 'v3, 12 Jan 2024', 'url': 'https://arxiv.org/abs/2309.14062',
     'quote': ['Interestingly, without updating the backbone network, our method obtains state-of-the-art results on several '
               'standard continual learning benchmarks.',
               'Despite storing a matrix per class, we have less memory overhead compared to exemplar-based methods and do not '
               'violate privacy concerns by storing images. Additionally, we compare our method against popular exemplar-based '
               'CIL methods in Table 3, where the memory buffer is set to 2K exemplars. Our method outperforms all others that '
               'do not expand the model significantly (see #P column for the number of parameters after the last task).',
               'FOSTER [60] 11.17 ✓ 67.9 60.2 69.9 63.1',
               'FeCAM(ours) 11.17 % 70.9 62.1 78.3 70.9'],
     'raw_file': 'q1/pdf_2309.14062v3.txt',
     'agent_note': 'States M1: class means and covariances on a backbone frozen after a large first task beat replay with a '
                   '2,000-exemplar buffer at equal parameter count (CIFAR-100 T=5 last 62.1 vs FOSTER 60.2). Warm start; the '
                   'memory comparison is not matched bytes.'},
    {'id': 'q3:0', 'tag': 'M1', 'reading': 'states', 'reading_by': RB,
     'source': 'Janson, Zhang, Aljundi, Elhoseiny, "A Simple Baseline that Questions the Use of Pretrained-Models in '
               'Continual Learning" (arXiv:2210.04428)',
     'version': 'v2, 29 Mar 2023', 'url': 'https://arxiv.org/abs/2210.04428',
     'quote': ['This baseline achieved 83.70% on 10-Split-CIFAR-100, surpassing most state-of-the-art continual learning '
               'methods, with all initialized by the same pre-trained transformer model.',
               'Ours 0 83.70 - ER [4] 50/class 82.53 16.46',
               'Joint - 90.85 -'],
     'raw_file': 'q3/pdf_2210.04428v2.txt',
     'agent_note': 'States M1 in its plainest form: class means on a frozen pretrained transformer (83.70) at or above ER '
                   'with 50 exemplars per class (82.53). Joint is 90.85.'},
    {'id': 'q3:1', 'tag': 'M1', 'reading': 'states', 'reading_by': RB,
     'source': 'Zhuang et al., "F-OAL: Forward-only Online Analytic Learning with Fast Training and Low Memory Footprint in '
               'Class Incremental Learning" (arXiv:2403.15751)',
     'version': 'v2, 4 Nov 2024', 'url': 'https://arxiv.org/abs/2403.15751',
     'quote': ['Cooperating with a pre-trained frozen encoder with Feature Fusion, F-OAL only needs to update a linear '
               'classifier by recursive least square.',
               'We assign 5,000 memory buffer sizes for replay-based methods.',
               'ER(ICRA 2019) ✓ 84.6 92.1 28.6 54.3 81.6 6.8',
               'F-OAL ✗ 86.5 92.5 54.0 75.9 87.3 17.5'],
     'raw_file': 'q3/pdf_2403.15751v2.txt',
     'agent_note': 'States M1: a closed-form head on accumulated statistics over a frozen pretrained ViT is at or above ER '
                   '(5,000 buffer, same backbone) on all six datasets (CIFAR-100 86.5 vs 84.6).'},
    {'id': 'q3:2', 'tag': 'M1', 'reading': 'states', 'reading_by': RB,
     'source': 'Hayes & Kanan, "Lifelong Machine Learning with Deep Streaming Linear Discriminant Analysis" '
               '(arXiv:1909.01520; CVPR Workshops 2020)',
     'version': 'v3, 17 Apr 2020', 'url': 'https://arxiv.org/abs/1909.01520',
     'quote': ['SLDA maintains one running mean per class and a shared covariance matrix that can be held fixed, or updated '
               'using an online update.',
               'SLDA (Plastic Σ) θF Yes 0.752',
               'iCaRL [44] θF , θG No 0.692',
               'Although SLDA cannot train the CNN’s hidden layers, it outperforms iCaRL overall and ends with a higher '
               'accuracy than End-to-End on ImageNet (see Fig. 1).'],
     'raw_file': 'q3/pdf_1909.01520v3.txt',
     'agent_note': 'States M1: class means and a shared covariance on a frozen base-initialised ResNet-18 outperform iCaRL '
                   '(rehearsal) on ImageNet (Omega_all 0.752 vs 0.692); below End-to-End on that metric (0.780).'},
    {'id': 'q3:3', 'tag': 'M1', 'reading': 'states', 'reading_by': RB,
     'source': 'Zhuang et al., "ACIL: Analytic Class-Incremental Learning with Absolute Memorization and Privacy '
               'Protection" (arXiv:2205.14922; NeurIPS 2022)',
     'version': 'v2, 10 Dec 2022', 'url': 'https://arxiv.org/abs/2205.14922',
     'quote': ['The network is first trained (i.e., phase #0) on the base dataset containing half of the full classes from '
               'the original dataset.',
               'The ACIL and LwF do not keep old data while other compared methods adopt the same replay settings (e.g., [2], '
               '[9]) by reserving 20 exemplars per old class.',
               'for 5-phase CIL, the ACIL gives an accuracy of 66.30% on CIFAR-100, which is slightly worse than the results '
               'from several combo techniques such as the “POD+AANets” combo (66.31%) by 0.01% and the “POD+AANets+RMM” '
               'combo (68.36%) by 2.06%. However, for 25-phase CIL, the ACIL (with 65.95%) outperforms these combo methods'],
     'raw_file': 'q3/pdf_2205.14922v2.txt',
     'agent_note': 'States M1 in warm start: an analytic head on a backbone frozen after a half-class base task is within '
                   '2.06 of replay (20/class) at K=5 and ahead at K=25. Its stored R (64 M elements) is larger than the 20/class '
                   'buffer on CIFAR-100 (Q3 dossier), so this is not a matched-memory comparison.'},
    {'id': 'q3:4', 'tag': 'M1', 'reading': 'states', 'reading_by': RB,
     'source': 'Zhuang et al., "GACL: Exemplar-Free Generalized Analytic Continual Learning" (arXiv:2403.15706; NeurIPS 2024)',
     'version': 'v3, 4 Nov 2024', 'url': 'https://arxiv.org/abs/2403.15706',
     'quote': ['To ensure a fair comparison, all methods utilize a frozen backbone.',
               'ER [35] ✕ 56.17±1.84 53.80±1.46 55.60±0.69',
               'GACL (ours) ✓ 57.99±2.46 56.24±3.12 70.31±0.06'],
     'raw_file': 'q3/pdf_2403.15706v3.txt',
     'agent_note': 'States M1 on a frozen pretrained ViT: GACL final 70.31 vs ER at memory 2000 55.60 (Si-Blurry). ER here '
                   'shares the frozen backbone, so it is not ER with a learning backbone.'},
    {'id': 'q1:1', 'tag': 'M1', 'reading': 'close', 'reading_by': RB,
     'source': 'Zhu, Zhang, Cheng, Liu, "PASS++" (arXiv:2407.14029)',
     'version': 'v1, 19 Jul 2024', 'url': 'https://arxiv.org/abs/2407.14029',
     'quote': ['We mainly train the model on half of the classes for the first task, and equal classes in the rest phases',
               'Without storing any old training samples, PASS++ is capable of alleviating the catastrophic forgetting problem '
               'in CIL, performing comparably with state-of-the-art exemplar-based approaches under different settings.'],
     'raw_file': 'q1/pdf_2407.14029v1.txt',
     'agent_note': 'Close: class means reach exemplar-based quality, but the backbone keeps learning (not fixed, not '
                   'pretrained), so the source asserts M1 outside its stated condition.'},
    {'id': 'q2:0', 'tag': 'M1', 'reading': 'close', 'reading_by': RB,
     'source': 'van de Ven, Siegelmann, Tolias, "Brain-inspired replay for continual learning with artificial neural '
               'networks", Nature Communications 11:4069 (2020)',
     'version': 'published online 2020-08-13 (HTML; PDF not reached)',
     'url': 'https://www.nature.com/articles/s41467-020-17866-2',
     'quote': ['Our method achieves state-of-the-art performance on challenging continual learning benchmarks (e.g., '
               'class-incremental learning on CIFAR-100) without storing data, and it provides a novel model for replay in '
               'the brain.',
               'To simulate development, we pre-trained the convolutional layers of our model on CIFAR-10, a dataset '
               'containing similar but non-overlapping images compared to CIFAR-100 35 . During the incremental training on '
               'CIFAR-100, those convolutional layers were frozen and we replayed only through the fully connected layers.'],
     'raw_file': 'q2/bir.txt',
     'agent_note': 'Close: a no-stored-data method works on CIFAR-100 only with frozen pre-trained layers, but the memory is '
                   'a generator (feature replay), not class statistics.'},
    {'id': 'q1:2', 'tag': 'M1', 'reading': 'bears', 'reading_by': RB,
     'source': 'He et al., "Semantic Shift Estimation via Dual-Projection and Classifier Reconstruction for Exemplar-Free '
               'Class-Incremental Learning" (DPCR; arXiv:2503.05423; ICML 2025)',
     'version': 'v4, 18 May 2025', 'url': 'https://arxiv.org/abs/2503.05423',
     'quote': ['It is worth mentioned that methods that freeze the backbone (e.g., ACIL, FeCAM, and DS-AL) are ineffective and '
               'demonstrate poor performance, whereas simple baselines like LwF and SDC can perform better. This observation '
               'highlights the limitations of freezing the backbone. Although freezing backbone can eliminate the semantic '
               'shift, it sacrifice the adaptation in new tasks then obtain low performance.'],
     'raw_file': 'q1/pdf_2503.05423v4.txt',
     'agent_note': "HARD READING. Q1's dossier tags this 'contradicts'. Read 'bears': M1 is existential ('can approach ... "
                   "when fixed or pretrained'); DPCR shows that a backbone fixed after a small first task (cold start) is "
                   'not enough, and compares with LwF/SDC, not with replay. It bounds M1 to good fixed features (large first '
                   "task or pretraining) without negating 'can'. If M1 were read as 'whenever the extractor is fixed', this "
                   "would be 'contradicts' and M1 would grade MIXED."},
    {'id': 'q3:5', 'tag': 'M1', 'reading': 'bears', 'reading_by': RB,
     'source': 'Jučas & Pan, "Data-Free Reservoir Features for Efficient Long-Horizon Cold-Start Continual Learning" '
               '(CIRCLE; arXiv:2606.27095)',
     'version': 'v1, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.27095',
     'quote': ['drift-compensation methods require repeated backbone training and increasingly expensive updates as the task '
               'horizon grows, while frozen-backbone methods are cheap but weak under cold start.',
               'However, in cold-start, the data available before freezing is only a small first task, resulting in '
               'non-transferable feature extractors biased towards initial classes.'],
     'raw_file': 'q3/pdf_2606.27095v1.txt',
     'agent_note': "Bears on M1's condition: features fixed after a small first task are weak (the same bound as q1:2)."},

    # ------------------------------------------------------------------ M2
    {'id': 'q1:3', 'tag': 'M2', 'reading': 'states', 'reading_by': RB,
     'source': 'Magistri, Trinci, Soutif-Cormerais, van de Weijer, Bagdanov, "Elastic Feature Consolidation for Cold Start '
               'Exemplar-Free Incremental Learning" (EFC; arXiv:2402.03917; ICLR 2024)',
     'version': 'v3, 30 May 2024', 'url': 'https://arxiv.org/abs/2402.03917',
     'quote': ['In this paper, we consider the challenging Cold Start scenario in which insufficient data is available in the '
               'first task to learn a high-quality backbone. This is especially challenging for EFCIL since it requires high '
               'plasticity, which results in feature drift which is difficult to compensate for in the exemplar-free setting.',
               'EFCIL with Cold Starts faces two main challenges: an alternative to feature distillation is required, since the '
               'backbone must adapt to new data, and an exemplar-free mechanism is needed to adapt previous-task classifiers to '
               'the changing backbone.'],
     'raw_file': 'q1/pdf_2402.03917v3.txt',
     'agent_note': 'States M2 for a learning backbone: feature drift is the named difficulty of exemplar-free class-IL.'},
    {'id': 'q1:4', 'tag': 'M2', 'reading': 'states', 'reading_by': RB,
     'source': 'Gomez-Villa, Goswami, Wang, Bagdanov, Twardowski, van de Weijer, "Exemplar-free Continual Representation '
               'Learning via Learnable Drift Compensation" (LDC; arXiv:2407.08536; ECCV 2024)',
     'version': 'v1, 11 Jul 2024', 'url': 'https://arxiv.org/abs/2407.08536',
     'quote': ['Exemplar-free class-incremental learning using a backbone trained from scratch and starting from a small first '
               'task presents a significant challenge for continual representation learning. Prototype-based approaches, when '
               'continually updated, face the critical issue of semantic drift due to which the old class prototypes drift to '
               'different positions in the new feature space. Through an analysis of prototype-based continual learning, we '
               'show that forgetting is not due to diminished discriminative power of the feature extractor, and can '
               'potentially be corrected by drift compensation.',
               'We showed that performance degradation in exemplar-free CP accumulation methods is largely due to feature drift.'],
     'raw_file': 'q1/pdf_2407.08536v1.txt',
     'agent_note': "States M2 in the strongest form found: degradation of prototype-accumulation methods is 'largely due to "
                   "feature drift', not to lost discriminative power."},
    {'id': 'q1:5', 'tag': 'M2', 'reading': 'states', 'reading_by': RB,
     'source': 'Magistri et al., "EFC++" (arXiv:2503.10439; International Journal of Computer Vision 134, 454 (2026))',
     'version': 'v4, 28 Sep 2026', 'url': 'https://arxiv.org/abs/2503.10439',
     'quote': ['However, we show that in high-plasticity Cold Start regimes, the joint optimization of the feature extractor '
               'and prototype-rehearsal based classifier used in EFC makes stored prototypes progressively misaligned with the '
               'evolving feature space.',
               'Nevertheless, the dominant source of improvement is explained by the class means. Replacing our estimated '
               'class means with real ones, while keeping the covariances fixed, leads to the largest improvement: 2.92% and '
               '5.33% on CIFAR-100, and 6.30% and 10.92% on ImageNet-1K, with respect to fixed statistics in the 10- and '
               '20-step settings, respectively.'],
     'raw_file': 'q1/pdf_2503.10439v4.txt',
     'agent_note': 'States M2 (stored prototypes go stale as the backbone learns) and locates the staleness mostly in the '
                   'means. Its own joint gap (q1:18) bounds how much of the total gap staleness explains.'},
    {'id': 'q1:6', 'tag': 'M2', 'reading': 'states', 'reading_by': RB,
     'source': 'Jučas & Pan, "Data-Free Reservoir Features for Efficient Long-Horizon Cold-Start Continual Learning" '
               '(CIRCLE; arXiv:2606.27095)',
     'version': 'v1, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.27095',
     'quote': ['Their main limitation is semantic drift [Yu et al., 2020]: as φ changes, old-class features shift and stored '
               'head statistics become outdated.'],
     'raw_file': 'q1/pdf_2606.27095v1.txt',
     'agent_note': "States M2 nearly word for word, for trained-backbone methods ('main limitation', 'stored head statistics "
                   "become outdated')."},
    {'id': 'q1:7', 'tag': 'M2', 'reading': 'states', 'reading_by': RB,
     'source': 'Xu & Krawczyk, "BiCyc: bidirectional alignment with cycle consistency" (arXiv:2606.05675; ICLR 2026)',
     'version': 'v1, 4 Jun 2026', 'url': 'https://arxiv.org/abs/2606.05675',
     'quote': ['In exemplar-free class-incremental learning (EFCIL), this challenge is amplified because past data cannot be '
               'stored, making representation drift for old classes particularly harmful. Prototype-based EFCIL is attractive '
               'for its efficiency, yet prototypes drift as the embedding space evolves; thus, projection-based drift '
               'compensation has become a popular remedy.',
               'Because EFCIL forbids storing past raw samples, μ t c cannot be recomputed exactly, and cached prototypes μ t−1 '
               'c become stale once ft is deployed.'],
     'raw_file': 'q1/pdf_2606.05675v1.txt',
     'agent_note': 'States M2 (cached prototypes become stale as the embedding evolves).'},
    {'id': 'q2:1', 'tag': 'M2', 'reading': 'states', 'reading_by': RB,
     'source': 'Wang, Zhang, Su, Zhu, "A Comprehensive Survey of Continual Learning: Theory, Method and Application" '
               '(arXiv:2302.00487; TPAMI)',
     'version': 'v3, 6 Feb 2024', 'url': 'https://arxiv.org/abs/2302.00487',
     'quote': ['However, a central challenge is the representation shift caused by sequentially updating the feature '
               'extractor, which reflects the feature-level catastrophic forgetting.'],
     'raw_file': 'q2/2302.00487v3.txt',
     'agent_note': "States M2 for feature-level replay ('a central challenge'); a survey statement."},
    {'id': 'q3:6', 'tag': 'M2', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Zhao et al., "Advancing Analytic Class-Incremental Learning through Vision-Language Calibration" (VILA; '
               'arXiv:2602.13670)',
     'version': 'v3, 7 May 2026', 'url': 'https://arxiv.org/abs/2602.13670',
     'quote': ['In this paper, we first conduct a systematic study to dissect the failure modes of PTM-based analytic CIL, '
               'identifying representation rigidity as the primary bottleneck.',
               'Our analysis suggests that while analytic learning effectively preserves historical knowledge within a given '
               'subspace, the feature space itself (typically frozen or narrowly adapted) may become rank-deficient for future '
               'distinct distributions.'],
     'raw_file': 'q3/pdf_2602.13670v3.txt',
     'agent_note': "HARD READING. M2 is universal ('the main bottleneck of statistics-based memory'); analytic CIL is a "
                   "statistics-based memory, and VILA names a different primary bottleneck for it (rigidity of frozen "
                   "features, where nothing drifts). Read 'contradicts' in part. If M2's colon clause ('as the backbone "
                   "learns') is read as restricting its scope to learning backbones, this is out of scope and 'bears', and "
                   'M2 would grade REDUNDANT.'},
    {'id': 'q3:7', 'tag': 'M2', 'reading': 'close', 'reading_by': RB,
     'source': 'Jučas & Pan, "Data-Free Reservoir Features for Efficient Long-Horizon Cold-Start Continual Learning" '
               '(CIRCLE; arXiv:2606.27095)',
     'version': 'v1, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.27095',
     'quote': ['This highlights a trade-off within cold-start EFCIL: training ϕ avoids representational bias but incurs drift '
               'and cost, while freezing ϕ enables efficient, drift-free updates but suffers from first-task bias.'],
     'raw_file': 'q3/pdf_2606.27095v1.txt',
     'agent_note': 'Close: drift is the bottleneck of one branch of a trade-off; freezing replaces it with first-task bias. '
                   'This is the corrected framing of M2.'},
    {'id': 'q3:8', 'tag': 'M2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Zhuang et al., "DS-AL: A Dual-Stream Analytic Learning for Exemplar-Free Class-Incremental Learning" '
               '(arXiv:2403.17503; AAAI 2024)',
     'version': 'v1, 26 Mar 2024', 'url': 'https://arxiv.org/abs/2403.17503',
     'quote': ['However, existing AL-based methods may suffer from an under-fitting dilemma because they rely solely on one '
               'linear projection.'],
     'raw_file': 'q3/pdf_2403.17503v1.txt',
     'agent_note': "Bears: names under-fitting as a problem of frozen-feature analytic methods ('may suffer'), without "
                   "calling it the main bottleneck. Q3's dossier tags it 'contradicts'."},
    {'id': 'q3:9', 'tag': 'M2', 'reading': 'bears', 'reading_by': RB,
     'source': 'He et al., "REAL: Representation Enhanced Analytic Learning for Exemplar-Free Class-Incremental Learning" '
               '(arXiv:2403.13522)',
     'version': 'v3, 17 Dec 2025', 'url': 'https://arxiv.org/abs/2403.13522',
     'quote': ['However, existing ACL techniques have two limitations: (1) The feature representations are less effective on '
               'unseen categories after the base phase, which limits performance in future phases. Existing ACL methods '
               'employ supervised learning to acquire representation and freeze the backbone after the base phase, resulting '
               'in less discriminative representations across unseen data categories. (2) The classifier does not effectively '
               'utilize the knowledge captured by the backbone.'],
     'raw_file': 'q3/pdf_2403.13522v3.txt',
     'agent_note': "Bears: two limitations of frozen-feature analytic memory, neither drift; not called 'main'. Q3's dossier "
                   "tags it 'contradicts'."},

    # ------------------------------------------------------------------ M3
    {'id': 'q1:8', 'tag': 'M3', 'reading': 'states', 'reading_by': RB,
     'source': 'Yu, Twardowski, Liu, Herranz, Wang, Cheng, Jui, van de Weijer, "Semantic Drift Compensation for '
               'Class-Incremental Learning" (SDC; arXiv:2004.00440; CVPR 2020)',
     'version': 'v1, 1 Apr 2020', 'url': 'https://arxiv.org/abs/2004.00440',
     'quote': ['In addition, we propose a new method to estimate the drift, called semantic drift, of features and compensate '
               'for it without the need of any exemplars. We approximate the drift of previous tasks based on the drift that is '
               'experienced by current task data.',
               'We outperform existing methods which do not require exemplars and obtain competitive results compared to '
               'methods which store exemplars.'],
     'raw_file': 'q1/pdf_2004.00440v1.txt',
     'agent_note': 'States M3 (its origin): the drift of old statistics is estimated from current-task data only.'},
    {'id': 'q1:9', 'tag': 'M3', 'reading': 'states', 'reading_by': RB,
     'source': 'Gomez-Villa et al., "Exemplar-free Continual Representation Learning via Learnable Drift Compensation" '
               '(LDC; arXiv:2407.08536; ECCV 2024)',
     'version': 'v1, 11 Jul 2024', 'url': 'https://arxiv.org/abs/2407.08536',
     'quote': ['LDC learns a projector that maps between the feature spaces of the consecutive tasks using only the data '
               'available at each task along with current and previous model. The trained projector is used at the end of each '
               'task to correct the stored old prototype positions.',
               'Without exemplars, pf only learns the projection from current task data. Consequently, due to biases in the '
               'current data, updates to some old class prototypes may not be perfect.'],
     'raw_file': 'q1/pdf_2407.08536v1.txt',
     'agent_note': 'States M3, with its own limit (current-data bias), which matters for streams of 2 classes per task.'},
    {'id': 'q1:10', 'tag': 'M3', 'reading': 'states', 'reading_by': RB,
     'source': 'Goswami, Soutif-Cormerais, Liu, Kamath, Twardowski, van de Weijer, "Resurrecting Old Classes with New Data '
               'for Exemplar-Free Continual Learning" (ADC; arXiv:2405.19074; CVPR 2024)',
     'version': 'v1, 29 May 2024', 'url': 'https://arxiv.org/abs/2405.19074',
     'quote': ['we propose to adversarially perturb the current samples such that their embeddings are close to the old class '
               'prototypes in the old model embedding space. We then estimate the drift in the embedding space from the old to '
               'the new model using the perturbed images and compensate the prototypes accordingly.',
               'The ADC method, as currently designed, requires the access to the task boundaries during training in order to '
               'trigger the computation of the old prototypes drift and to access a big enough quantity of current data.'],
     'raw_file': 'q1/pdf_2405.19074v1.txt',
     'agent_note': "States M3 (drift estimated from perturbed current data), with the limit 'a big enough quantity of "
                   "current data'."},
    {'id': 'q1:11', 'tag': 'M3', 'reading': 'states', 'reading_by': RB,
     'source': 'Rypeść, Cygert, Trzciński, Twardowski, "Task-recency bias strikes back: Adapting covariances in '
               'Exemplar-Free Class Incremental Learning" (AdaGauss; arXiv:2409.18265; NeurIPS 2024)',
     'version': 'v2, 26 Oct 2024', 'url': 'https://arxiv.org/abs/2409.18265',
     'quote': ['after training the feature extractor F on an incremental task, we train an auxiliary network (adapter), which '
               'we utilize to adapt the means and covariances of old classes to the latent space of the new feature extractor.',
               'We use only the current data from task t for that.'],
     'raw_file': 'q1/pdf_2409.18265v2.txt',
     'agent_note': 'States M3 for means and covariances, current data only.'},
    {'id': 'q1:12', 'tag': 'M3', 'reading': 'states', 'reading_by': RB,
     'source': 'Honda, "Adversarial Pseudo-replay for Exemplar-free Class-incremental Learning" (APR; arXiv:2511.17973; '
               'WACV 2026)',
     'version': 'v1, 22 Nov 2025', 'url': 'https://arxiv.org/abs/2511.17973',
     'quote': ['we introduce adversarial pseudo-replay (APR), a method that perturbs the images of the new task with '
               'adversarial attack, to synthesize the pseudo-replay images online without storing any replay samples.',
               'Moreover, we calibrate the covariance matrices to compensate for the semantic drift after each task, by '
               'learning a transfer matrix on the pseudo-replay samples.'],
     'raw_file': 'q1/pdf_2511.17973v1.txt',
     'agent_note': 'States M3: covariances moved by a transfer matrix learnt on pseudo-replay built from new-task images.'},
    {'id': 'q3:10', 'tag': 'M3', 'reading': 'states', 'reading_by': RB,
     'source': 'He et al., "Semantic Shift Estimation via Dual-Projection and Classifier Reconstruction for Exemplar-Free '
               'Class-Incremental Learning" (DPCR; arXiv:2503.05423; ICML 2025)',
     'version': 'v4, 18 May 2025', 'url': 'https://arxiv.org/abs/2503.05423',
     'quote': ['Since we can access the backbone θt−1 at task t, the semantic shift between the backbone θt and θt−1 can be '
               'estimated by a learnable model that captures the difference between embeddings extracted by θt−1 and θt.',
               'However, due to the constrain of EFCIL, the embeddings of previous tasks cannot be extracted by θt then the '
               'covariance and correlation can not be constructed directly.'],
     'raw_file': 'q3/pdf_2503.05423v4.txt',
     'agent_note': 'States M3: the shift is estimated on current-task data passed through the old and new backbones; stored '
                   'Gram matrices and means are calibrated through it.'},
    {'id': 'q1:13', 'tag': 'M3', 'reading': 'close', 'reading_by': RB,
     'source': 'Magistri et al., "EFC++" (arXiv:2503.10439; International Journal of Computer Vision 134, 454 (2026))',
     'version': 'v4, 28 Sep 2026', 'url': 'https://arxiv.org/abs/2503.10439',
     'quote': ['Comparing the two scenarios, we see that the average distance between the real class means and fixed '
               'prototypes is greater in the Cold Start setting, indicating that the representations are more prone to change '
               'compared to the Warm Start setting. Additionally, our prototype update rule (see Equations (15) and (16)) '
               'effectively mitigates prototype drift in both scenarios. However, it is less effective in the more challenging '
               'Cold Start scenario due to the greater representation drift.',
               'Table 7 Impact of Mean and Covariance Drift on EFC++ (CIFAR-100 Cold Start). Step Mean Covariance Accuracy '
               'Delta 10 Fixed Fixed 46.30 ± 1.45 — EFM Fixed 47.52 ± 0.68 +1.22 (Ours) EFM Real 47.37 ± 0.19 +1.07 Real Fixed '
               '49.22 ± 0.17 +2.92 Real Real 49.33 ± 0.20 +3.03'],
     'raw_file': 'q1/pdf_2503.10439v4.txt',
     'agent_note': 'Close, with a quantified limit: the current-data update recovers 1.22 of the 3.03 points that oracle '
                   'statistics recover (CIFAR-100 cold start, 10 steps).'},
    {'id': 'q2:2', 'tag': 'M3', 'reading': 'close', 'reading_by': RB,
     'source': 'Tong, Lu, Liu, Gong, "Model Inversion with Layer-Specific Modeling and Alignment for Data-Free Continual '
               'Learning" (PMI; arXiv:2510.26311; NeurIPS 2025)',
     'version': 'v1, 30 Oct 2025', 'url': 'https://arxiv.org/abs/2510.26311',
     'quote': ['Since ResNets are trained from scratch in CL, the feature representations of previous classes may shift after '
               'learning new tasks. To account for this, we update the mean and standard deviation of previous classes using '
               'synthetic data after each task.'],
     'raw_file': 'q2/2510.26311v1.txt',
     'agent_note': 'Close: stored class statistics are re-estimated after each task, but from synthetic (inverted) data, not '
                   'from current data only.'},
    {'id': 'q1:14', 'tag': 'M3', 'reading': 'bears', 'reading_by': RB,
     'source': 'Jučas & Pan, "Data-Free Reservoir Features for Efficient Long-Horizon Cold-Start Continual Learning" '
               '(CIRCLE; arXiv:2606.27095)',
     'version': 'v1, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.27095',
     'quote': ['In Section 4, we evaluate T ∈{50, 100} and an ImageNet-1k T = 500 stress test, and find that performance '
               'degrades sharply for trained-backbone drift-compensation methods in this regime.',
               'At T = 10, drift-compensation methods (EFC++, AdaGauss) perform best across all datasets, as limited task '
               'transitions keep drift-estimation errors small.'],
     'raw_file': 'q1/pdf_2606.27095v1.txt',
     'agent_note': "Q1's dossier tags this 'contradicts over long horizons'. Read 'bears': M3 is existential ('can be "
                   "compensated'); compensation works at T=10 and degrades sharply at T=50-100. A horizon bound, not a negation."},

    # ------------------------------------------------------------------ M4
    {'id': 'q3:11', 'tag': 'M4', 'reading': 'states', 'reading_by': RB,
     'source': 'Zhuang et al., "ACIL: Analytic Class-Incremental Learning with Absolute Memorization and Privacy '
               'Protection" (arXiv:2205.14922; NeurIPS 2022)',
     'version': 'v2, 10 Dec 2022', 'url': 'https://arxiv.org/abs/2205.14922',
     'quote': ['The absolute memorization is demonstrated in the sense that class-incremental learning using ACIL given present '
               'data would give identical results to that from its joint-learning counterpart which consumes both present and '
               'historical samples. This equality is theoretically validated.'],
     'raw_file': 'q3/pdf_2205.14922v2.txt',
     'agent_note': 'States M4: identical to joint (ridge) learning on the frozen features, from present data only.'},
    {'id': 'q3:12', 'tag': 'M4', 'reading': 'states', 'reading_by': RB,
     'source': 'Zhuang et al., "DS-AL: A Dual-Stream Analytic Learning for Exemplar-Free Class-Incremental Learning" '
               '(arXiv:2403.17503; AAAI 2024)',
     'version': 'v1, 26 Mar 2024', 'url': 'https://arxiv.org/abs/2403.17503',
     'quote': ['Therefore, models trained in a CIL manner yield identical results to those employing data from both current and '
               'historical phases concurrently.',
               'Upon freezing the backbone, the CIL is equivalent to its joint-learning counterpart as shown in Theorem 1.'],
     'raw_file': 'q3/pdf_2403.17503v1.txt',
     'agent_note': 'States M4, with the condition written in (frozen backbone).'},
    {'id': 'q3:13', 'tag': 'M4', 'reading': 'states', 'reading_by': RB,
     'source': 'Zhuang et al., "GACL: Exemplar-Free Generalized Analytic Continual Learning" (arXiv:2403.15706; NeurIPS 2024)',
     'version': 'v3, 4 Nov 2024', 'url': 'https://arxiv.org/abs/2403.15706',
     'quote': ['the weight obtained recursively is equal to its joint-learning counterpart, indicating that the GACL is a '
               '“completely non-forgetting” technique (under the condition of a frozen backbone).',
               'The ACIL [7] first converts a continual learning problem to a batch recursive least-squares problem, '
               'eliminating the need to store samples by preserving the correlation matrix, and the RanPAC [25] applies this '
               'trick to pre-trained models.'],
     'raw_file': 'q3/pdf_2403.15706v3.txt',
     'agent_note': 'States M4 (equality, no stored samples, frozen backbone).'},
    {'id': 'q3:14', 'tag': 'M4', 'reading': 'states', 'reading_by': RB,
     'source': 'Zhuang et al., "F-OAL: Forward-only Online Analytic Learning with Fast Training and Low Memory Footprint in '
               'Class Incremental Learning" (arXiv:2403.15751)',
     'version': 'v2, 4 Nov 2024', 'url': 'https://arxiv.org/abs/2403.15751',
     'quote': ['our approach achieves the identical solution to joint-learning on the whole dataset without preserving any '
               'historical exemplars, reducing the resource consumption.'],
     'raw_file': 'q3/pdf_2403.15751v2.txt',
     'agent_note': 'States M4.'},
    {'id': 'q3:15', 'tag': 'M4', 'reading': 'states', 'reading_by': RB,
     'source': 'Fang et al., "AIR: Analytic Imbalance Rectifier for Continual Learning" (arXiv:2408.10349)',
     'version': 'v2, 24 Sep 2026', 'url': 'https://arxiv.org/abs/2408.10349',
     'quote': ['AIR is an online exemplar-free approach with a frozen backbone as the feature extractor and a closed-form '
               'incremental classifier whose weight equals the joint-learning weight for the same class-weighted ridge '
               'objective.'],
     'raw_file': 'q3/pdf_2408.10349v2.txt',
     'agent_note': "States M4 with its exact scope: equality with joint learning 'for the same ... ridge objective'."},
    {'id': 'q1:15', 'tag': 'M4', 'reading': 'states', 'reading_by': RB,
     'source': 'Jučas & Pan, "Data-Free Reservoir Features for Efficient Long-Horizon Cold-Start Continual Learning" '
               '(CIRCLE; arXiv:2606.27095)',
     'version': 'v1, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.27095',
     'quote': ['A fixed φ enables closed-form head updates over frozen features, ensuring equivalence between continual '
               'training and joint training on all seen classes.',
               'For our CIRCLE, AT is invariant across task splits because continual training for CIRCLE is equivalent to '
               'joint training.'],
     'raw_file': 'q1/pdf_2606.27095v1.txt',
     'agent_note': 'States M4 on data-free (untrained) features, cold start by construction.'},
    {'id': 'q3:16', 'tag': 'M4', 'reading': 'close', 'reading_by': RB,
     'source': 'McDonnell, Gong, Parvaneh, Abbasnejad, van den Hengel, "RanPAC: Random Projections and Pre-trained Models '
               'for Continual Learning" (arXiv:2307.02251; NeurIPS 2023)',
     'version': 'v3, 16 Jan 2024', 'url': 'https://arxiv.org/abs/2307.02251',
     'quote': ['Both C and G will be invariant to the sequence in which the entirety of N training samples are presented, a '
               'property ideal for CL algorithms.'],
     'raw_file': 'q3/pdf_2307.02251v3.txt',
     'agent_note': 'Close: order invariance of the stored sufficient statistics (G, C), which implies the joint solution; '
                   'the quote does not itself say "equals joint training".'},
    {'id': 'q3:17', 'tag': 'M4', 'reading': 'bears', 'reading_by': RB,
     'source': 'Zhuang et al., "ACIL: Analytic Class-Incremental Learning with Absolute Memorization and Privacy '
               'Protection" (arXiv:2205.14922; NeurIPS 2022)',
     'version': 'v2, 10 Dec 2022', 'url': 'https://arxiv.org/abs/2205.14922',
     'quote': ['Even with several appealing features, the ACIL is naturally not as powerful as the BP-based joint learning. '
               'The ACIL is facilitated but also constrained by the fact that it freezes the training of CNN weights.',
               'Although theoretically the ACIL should give identical results regardless of K, the possible mild drop is likely '
               'caused by quantization errors since large K indicates more computation rounds hence more quantization '
               'operations'],
     'raw_file': 'q3/pdf_2205.14922v2.txt',
     'agent_note': "Bears on M4's scope: the equality is with joint ridge on frozen features, not with joint training of the "
                   'network; and it is exact in arithmetic, not in floating point.'},
    {'id': 'q3:18', 'tag': 'M4', 'reading': 'bears', 'reading_by': RB,
     'source': 'Hartley et al., "SPARCL: Spectral Partitioned Analytic Continual Learning" (arXiv:2608.21307)',
     'version': 'v1, 21 Aug 2026', 'url': 'https://arxiv.org/abs/2608.21307',
     'quote': ['Yet the usual forgetting narrative, centered on stochastic gradient overwriting, does not explain why analytic '
               'methods still drift on old classes despite exact recursive solvers. We identify the culprit as spectral '
               'interference: the joint ridge classifier for all tasks shares the inverse autocorrelation operator (R + λI)−1, '
               'so incoming task samples that load onto old dominant eigendirections dilute the spectrum and perturb old-class '
               'logits even when old labels are never revisited.'],
     'raw_file': 'q3/pdf_2608.21307v1.txt',
     'agent_note': 'Bears: equality with the joint ridge solution is not absence of forgetting, since the joint solution '
                   'itself moves old-class logits. It does not negate the equality.'},
    {'id': 'q4:0', 'tag': 'M4', 'reading': 'bears', 'reading_by': RB,
     'source': 'Alsulaimawi, "One-Shot Federated Ridge Regression: Exact Recovery via Sufficient Statistic Aggregation" '
               '(arXiv:2601.08216)',
     'version': 'v1, 13 Jan 2026', 'url': 'https://arxiv.org/abs/2601.08216',
     'quote': ['We formulate federated ridge regression as a distributed equilibrium problem where each client computes local '
               'sufficient statistics—the Gram matrix and moment vector—and transmits them once.',
               'At high privacy (low ε ≤0.5), DP-FedAvg outperforms private One-Shot. This occurs because One-Shot adds noise '
               'to d2 Gram matrix entries, and the subsequent matrix inversion can amplify noise when the perturbed matrix is '
               'ill-conditioned.'],
     'raw_file': 'q4/2601.08216.txt',
     'agent_note': 'Bears: the exact sufficient-statistic identity holds without privacy noise; under DP the closed form is '
                   'only approximate and inversion amplifies the noise.'},

    # ------------------------------------------------------------------ M5
    {'id': 'q2:3', 'tag': 'M5', 'reading': 'close', 'reading_by': RB,
     'source': 'Shin, Lee, Kim, Kim, "Continual Learning with Deep Generative Replay" (DGR; arXiv:1705.08690; NIPS 2017)',
     'version': 'v3, 12 Dec 2017', 'url': 'https://arxiv.org/abs/1705.08690',
     'quote': ['The performance is therefore equivalent to joint training on accumulated real data as long as the generator '
               'recovers the input distribution.',
               'One defect of the generative replay framework is that the efficacy of the algorithm heavily depends on the '
               'quality of the generator.'],
     'raw_file': 'q2/1705.08690v3.txt',
     'agent_note': 'Close: recovery (conditional on the generator) and the quality limit; no compute or drift claim.'},
    {'id': 'q2:4', 'tag': 'M5', 'reading': 'close', 'reading_by': RB,
     'source': 'Zhou, Wang, Qi, Ye, Zhan, Liu, "Class-Incremental Learning: A Survey" (arXiv:2302.03648; TPAMI)',
     'version': 'v2, 15 Jul 2024', 'url': 'https://arxiv.org/abs/2302.03648',
     'quote': ['On the other hand, the performance of generative replay methods relies on the quality of generated data. They '
               'are found to work well on simple datasets [166], [167] while failing in complex, largescale inputs [168].',
               'Additionally, recent advances in diffusion models reveal a promising way to generate instances with '
               'pre-trained diffusion models [51], while utilizing pre-trained models leads to an unfair comparison to other '
               'methods without extra information. Furthermore, when sequentially updating the generative model, the '
               'catastrophic forgetting phenomena can also be observed on these generative models [157], [158].'],
     'raw_file': 'q2/2302.03648v2.txt',
     'agent_note': "Close: quality and drift (generator forgetting), with recovery restricted to simple datasets; no "
                   "compute claim in the quotes. The nearest single statement of M5 found."},
    {'id': 'q2:5', 'tag': 'M5', 'reading': 'close', 'reading_by': RB,
     'source': 'Wang, Zhang, Su, Zhu, "A Comprehensive Survey of Continual Learning: Theory, Method and Application" '
               '(arXiv:2302.00487; TPAMI)',
     'version': 'v3, 6 Feb 2024', 'url': 'https://arxiv.org/abs/2302.00487',
     'quote': ['However, since continual learning of generative models is extremely difficult and requires significant '
               'resource overhead, generative replay is often limited to relatively simple datasets [422], [438]. An '
               'alternative is to convert the target of generative replay from data level to feature level, which can largely '
               'reduce the complexity of conditional generation and more adequately exploit semantic information.'],
     'raw_file': 'q2/2302.00487v3.txt',
     'agent_note': 'Close: compute ("resource overhead"), drift (continual learning of the generator) and quality (simple '
                   'datasets only); no comparison with stored replay.'},
    {'id': 'q2:6', 'tag': 'M5', 'reading': 'close', 'reading_by': RB,
     'source': 'Cywiński, Deja, Trzciński, Twardowski, Kuciński, "GUIDE: Guidance-based Incremental Learning with Diffusion '
               'Models" (arXiv:2403.03938)',
     'version': 'v2, 31 May 2024', 'url': 'https://arxiv.org/abs/2403.03938',
     'quote': ['As presented in Appendix B, the significant drawback of our method is the forgetting happening in the diffusion '
               'model itself. Our initial results suggest that because of the known issue of sample deficiency from '
               'low-density regions [40] forgetting in diffusion models manifests itself as a degradation of the diversity of '
               'generated samples, which has an important effect on the quality of rehearsal samples.',
               'An important drawback of all generative replay approaches is the computational burden associated with training '
               'and sampling from the diffusion model. This is also true for our method, which is computationally expensive.',
               'Method Time [GPU-hours] DGR VAE 1.28 DGR+distill 1.35 RTF 1.09 BIR 2.49 GFR 1.76 DDGR 111.96∗ DGR diffusion '
               '76.1 GUIDE 82.95'],
     'raw_file': 'q2/2403.03938v2.txt',
     'agent_note': 'Close: all three limits (drift inside the generator, quality, compute), but no claim that it recovers '
                   "much of stored replay's accuracy (no stored-replay arm)."},
    {'id': 'q2:7', 'tag': 'M5', 'reading': 'close', 'reading_by': RB,
     'source': 'Tong, Lu, Liu, Gong, "Model Inversion with Layer-Specific Modeling and Alignment for Data-Free Continual '
               'Learning" (PMI; arXiv:2510.26311; NeurIPS 2025)',
     'version': 'v1, 30 Oct 2025', 'url': 'https://arxiv.org/abs/2510.26311',
     'quote': ['First, generating inputs (e.g., images) solely from highly compressed output labels (e.g., classes) often causes '
               'drift between synthetic and real data. Replaying on such synthetic data can contaminate and erode knowledge '
               'learned from real data, further degrading inversion quality over time. Second, performing inversion is usually '
               'computationally expensive, as each iteration requires backpropagation through the entire model and many steps '
               'are needed for convergence.'],
     'raw_file': 'q2/2510.26311v1.txt',
     'agent_note': 'Close: drift, quality and compute for inversion replay in one paragraph; no stored-replay comparison.'},
    {'id': 'q2:8', 'tag': 'M5', 'reading': 'close', 'reading_by': RB,
     'source': 'Smith, Hsu, Balloch, Shen, Jin, Kira, "Always Be Dreaming: A New Approach for Data-Free Class-Incremental '
               'Learning" (ABD; arXiv:2106.09701; ICCV 2021)',
     'version': 'v2, 19 Aug 2021', 'url': 'https://arxiv.org/abs/2106.09701',
     'quote': ['Unfortunately, training a generative model is much more computationally and memory intensive compared to a '
               'classification model. Additionally, it is not clear whether generating images from the data distribution will '
               'violate data legality concerns because using a generative model increases the chance of memorizing potentially '
               'sensitive data [44].',
               'To our surprise, we found DGR [51] to perform poorly for class-incremental learning on this dataset (and in '
               'fact every dataset we experiment with)',
               'Our method and LWF.MC perform similarly, indicating that more work is needed to scale our approach to large '
               '224x224x3 images.'],
     'raw_file': 'q2/2106.09701v2.txt',
     'agent_note': 'Close: compute cost of generators, generative replay failing on its datasets, and a scaling limit for '
                   'inversion; recovery is partial in its own tables (see q2:18).'},
    {'id': 'q2:9', 'tag': 'M5', 'reading': 'close', 'reading_by': RB,
     'source': 'Jodelet, Liu, Phua, Murata, "Class-Incremental Learning using Diffusion Model for Distillation and Replay" '
               '(SDDR; arXiv:2306.17560; ICCV 2023 workshop)',
     'version': 'v2, 10 Oct 2023', 'url': 'https://arxiv.org/abs/2306.17560',
     'quote': ['These methods rely on the quality of the generated data, which poses a challenge for large scale datasets and is '
               'impacted by catastrophic forgetting when trained sequentially.',
               'Memory CIFAR100 T=5 T=10 Average Last Average Last Real 20 63.37 53.91 60.88 51.42 Synthetic 20 52.38 33.68 '
               '42.79 21.83 Synthetic 100 54.54 36.56 48.56 27.93 Synthetic 500 55.77 38.78 52.19 32.58'],
     'raw_file': 'q2/2306.17560v2.txt',
     'agent_note': 'Close: quality and generator forgetting stated; the same-method comparison (20 real/class 51.42 vs 500 '
                   'Stable-Diffusion images/class 32.58) shows the quality limit, not recovery.'},
    {'id': 'q2:10', 'tag': 'M5', 'reading': 'close', 'reading_by': RB,
     'source': 'Gao, Zhao, Ghanem, Zhang, "R-DFCIL: Relation-Guided Representation Learning for Data-Free Class Incremental '
               'Learning" (arXiv:2203.13104; ECCV 2022)',
     'version': 'v2, 21 Jul 2022', 'url': 'https://arxiv.org/abs/2203.13104',
     'quote': ['Though recent DFCIL works introduce techniques such as model inversion to synthesize data for previous classes, '
               'they fail to overcome forgetting due to the severe domain gap between the synthetic and real data.'],
     'raw_file': 'q2/2203.13104v2.txt',
     'agent_note': 'Close: the quality limit (domain gap) of inversion replay.'},
    {'id': 'q2:11', 'tag': 'M5', 'reading': 'bears', 'reading_by': RB,
     'source': 'Hsu, Liu, Ramasamy, Kira, "Re-evaluating Continual Learning Scenarios: A Categorization and Case for Strong '
               'Baselines" (arXiv:1810.12488)',
     'version': 'v4, 23 Jan 2019', 'url': 'https://arxiv.org/abs/1810.12488',
     'quote': ['The total static memory overhead is controlled to be the same among L2, Naive rehearsal, Naive rehearsal-C, '
               'online EWC, SI, MAS, GEM, and DGR. Each value is the average of 10 runs.',
               'GEM ✓ 98.42 ± 0.10 96.16 ± 0.35 92.20 ± 0.12 DGR ✓ 99.47 ± 0.03 95.74 ± 0.23 91.24 ± 0.33 RtF ✓ 99.66 ± 0.03 '
               '97.31 ± 0.11 92.56 ± 0.21'],
     'raw_file': 'q2/1810.12488v4.txt',
     'agent_note': "Bears on M5's recovery half: on split MNIST at equal static memory, generative replay recovers stored "
                   'replay (DGR 91.24 vs naive rehearsal 90.78, see q2:13). No cost claim.'},
    {'id': 'q2:12', 'tag': 'M5', 'reading': 'bears', 'reading_by': RB,
     'source': 'Gao & Liu, "DDGR: Continual Learning with Deep Diffusion-based Generative Replay", ICML 2023, PMLR 202',
     'version': 'PMLR 202 (2023)', 'url': 'https://proceedings.mlr.press/v202/gao23e/gao23e.pdf',
     'quote': ['Table H.4. The total time cost (s) of baselines on CIFAR100. Time cost (s) method NC=5 10 Finetuning 2421.40 '
               '3541.63 SI 3638.51 5167.41 EWC 5229.43 7114.12 MAS 6923.60 8491.71 IMM 8054.56 10324.09 DGR 69532.44 72543.57 '
               'DDGR 75692.41 87514.23',
               'Meanwhile, the instruction provided by the classifier to the diffusion model guarantees a high quality of '
               'synthetic samples that will not decrease as the tasks change.'],
     'raw_file': 'q2/ddgr_icml2023.txt',
     'agent_note': 'Bears: compute in numbers (DDGR 75692.41 s vs fine-tuning 2421.40 s at NC=5); it asserts that sample '
                   "quality does not decrease, against M5's drift clause (untested against GUIDE's finding, q2:6)."},

    # ------------------------------------------------------------------ M6
    {'id': 'q4:1', 'tag': 'M6', 'reading': 'states', 'reading_by': RB,
     'source': 'Pyrgelis, Troncoso, De Cristofaro, "Knock Knock, Who\'s There? Membership Inference on Aggregate Location '
               'Data" (arXiv:1708.06145; NDSS 2018)',
     'version': 'v2, 29 Nov 2017', 'url': 'https://arxiv.org/abs/1708.06145',
     'quote': ['We find that membership inference is a serious privacy threat, and show how its effectiveness depends on the '
               'adversary’s prior knowledge, the characteristics of the underlying location data, as well as the number of '
               'users and the timeframe on which aggregation is performed.',
               'With larger aggregation sizes, m = 500 or 1,000, performance drops closer to the random guess baseline '
               '(AUC = 0.5). Nonetheless, even for groups of 1,000 users, Adv can still infer membership of 60% of the target '
               'population with an AUC score higher than 0.6.',
               'Although differentially private mechanisms can indeed reduce the extent of the attacks, they also yield a '
               'significant loss in utility.'],
     'raw_file': 'q4/1708.06145.txt',
     'agent_note': 'States M6 for aggregates (sums over contributors): membership leaks, falling with the number of '
                   'contributors but not vanishing; DP is the mechanism that reduces it, at a utility cost.'},
    {'id': 'q4:2', 'tag': 'M6', 'reading': 'states', 'reading_by': RB,
     'source': 'Wang et al., "Taming Noise-Induced Prototype Degradation for Privacy-Preserving Personalized Federated '
               'Fine-Tuning" (arXiv:2604.27833)',
     'version': 'v1, 30 Apr 2026', 'url': 'https://arxiv.org/abs/2604.27833',
     'quote': ['Prototype-based Personalized Federated Learning (ProtoPFL) enables efficient multi-domain adaptation by '
               'communicating compact class prototypes, but directly sharing them poses privacy risks. A common defense involves '
               'perexample ℓ2 clipping before prototype computation to bound sensitivity, followed by isotropic Gaussian noise '
               'to enforce Local Differential Privacy (LDP).',
               '- NoLDP 0.9999±0.0000 257.7±65.0 100.00±0.00 0.6729±0.0124',
               'At ϵ = 1, all three mechanisms drive MIA ROC-AUC to chance (∼0.50) and throttle the FSH Top-1 Hit rate to '
               'roughly 20%.'],
     'raw_file': 'q4/2604.27833.txt',
     'agent_note': 'States M6 for class prototypes: membership inference above chance without noise (ROC-AUC 0.6729), '
                   'brought to chance by a DP mechanism. Reconstruction is scored at class level.'},
    {'id': 'q4:3', 'tag': 'M6', 'reading': 'states', 'reading_by': RB,
     'source': 'Farquhar & Gal, "Differentially Private Continual Learning" (arXiv:1902.06497; PiMLAI workshop, ICML 2018)',
     'version': 'v1, 18 Feb 2019', 'url': 'https://arxiv.org/abs/1902.06497',
     'quote': ['We estimate the likelihood of past data given the current model using differentially private generative models '
               'of old datasets.',
               'Without such guarantees, model inversion attacks against GANs are possible (Fredrikson et al., 2015).'],
     'raw_file': 'q4/1902.06497.txt',
     'agent_note': 'States M6 for generators: a generator of old data needs DP to carry a privacy claim (its attribution to '
                   'Fredrikson et al. for GANs is loose, as the Q4 dossier notes).'},
    {'id': 'q4:4', 'tag': 'M6', 'reading': 'states', 'reading_by': RB,
     'source': 'Tobaben, Alrawajfeh, Klasson, Heikkilä, Solin, Honkela, "Privacy Leakage via Output Label Space and '
               'Differentially Private Continual Learning" (arXiv:2411.04680; TMLR 08/2026)',
     'version': 'v6, 24 Aug 2026', 'url': 'https://arxiv.org/abs/2411.04680',
     'quote': ['These side-channels can completely invalidate privacy guarantees w.r.t. the sensitive data. Regardless whether '
               'a concrete attack exists, all operations accessing sensitive data must adhere to the DP definition (see Sec. 2).',
               'We use a pre-trained model fpre θ : X →RK as a frozen feature extractor without additional training during CL '
               '(Janson et al., 2022) to map inputs x to feature vectors v = f pre θ (x) ∈RK. The idea is to accumulate '
               'class-specific sums of these vectors under DP, and then classify points according to their cosine similarity '
               'with the class sums (see Alg. 1).'],
     'raw_file': 'q4/2411.04680.txt',
     'agent_note': 'States M6 for class-IL memories: leakage through side channels, and formal privacy only by a DP '
                   'mechanism on every operation, including accumulated class sums.'},
    {'id': 'q4:5', 'tag': 'M6', 'reading': 'states', 'reading_by': RB,
     'source': 'Carlini et al., "Extracting Training Data from Diffusion Models" (arXiv:2301.13188; USENIX Security 2023)',
     'version': 'v1, 30 Jan 2023', 'url': 'https://arxiv.org/abs/2301.13188',
     'quote': ['In this work, we show that diffusion models memorize individual images from their training data and emit them at '
               'generation time.',
               'Overall, our results show that diffusion models are much less private than prior generative models such as '
               'GANs, and that mitigating these vulnerabilities may require new advances in privacy-preserving training.'],
     'raw_file': 'q4/2301.13188.txt',
     'agent_note': 'States M6 for generators (diffusion models emit individual training images; mitigation needs '
                   'privacy-preserving training).'},
    {'id': 'q4:6', 'tag': 'M6', 'reading': 'close', 'reading_by': RB,
     'source': 'Homer et al., "Resolving individuals contributing trace amounts of DNA to highly complex mixtures using '
               'high-density SNP genotyping microarrays", PLoS Genetics 4(8): e1000167 (2008)',
     'version': 'published 29 Aug 2008 (HTML)',
     'url': 'https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1000167',
     'quote': ['These findings also suggest that composite statistics across cohorts, such as allele frequency or genotype '
               'counts, do not mask identity within genome-wide association studies.'],
     'raw_file': 'q4/homer2008.txt',
     'agent_note': 'Close: high-dimensional means leak membership; no mechanism is asserted in the quote.'},
    {'id': 'q4:7', 'tag': 'M6', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Zhu, Zhang, Wang, Yin, Liu, "Prototype Augmentation and Self-Supervision for Incremental Learning" (PASS), '
               'CVPR 2021',
     'version': 'CVF open-access camera-ready (no version number)',
     'url': 'https://openaccess.thecvf.com/content/CVPR2021/papers/Zhu_Prototype_Augmentation_and_Self-Supervision_for_'
            'Incremental_Learning_CVPR_2021_paper.pdf',
     'quote': ['Note that our method is non-exemplar based since we do not save any old samples, but to memorize one prototype '
               'in the deep feature space for each class, which is very memory efficient and has no privacy issues.'],
     'raw_file': 'q4/pass_cvpr2021.txt',
     'agent_note': "HARD READING. Asserts the negation of M6 for class means ('has no privacy issues'), untested in the "
                   "paper. The rule counts assertions, so 'contradicts'. If untested assertions were read 'bears', M6 "
                   'would grade REDUNDANT (as would q4:9, q4:10).'},
    {'id': 'q4:8', 'tag': 'M6', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Xu et al., "Stabilizing and Improving Federated Learning with Non-IID Data and Client Dropout" (ReBaFL; '
               'arXiv:2303.06314)',
     'version': 'v2, 15 Mar 2023', 'url': 'https://arxiv.org/abs/2303.06314',
     'quote': ['From the reconstructed results in Fig. 11, we can conclude that sharing feature prototypes will neither leak '
               'considerable information about the raw data, nor will they reveal any relationship between different image '
               'categories.',
               'Second, the feature prototype is an average of per-image feature vectors and the characteristics of individual '
               'images could be concealed.'],
     'raw_file': 'q4/2303.06314.txt',
     'agent_note': 'Contradicts in part, empirically: three inversion attacks on shared class prototypes recovered no '
                   "meaningful image (CIFAR-10). It tests reconstruction only, not membership, so it does not refute q4:1-q4:2."},
    {'id': 'q4:9', 'tag': 'M6', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Zhuang et al., "ACIL: Analytic Class-Incremental Learning with Absolute Memorization and Privacy '
               'Protection" (arXiv:2205.14922; NeurIPS 2022)',
     'version': 'v2, 10 Dec 2022', 'url': 'https://arxiv.org/abs/2205.14922',
     'quote': ['Instead, the Rk is cached to encrypt information for historical samples. However, it is impossible to '
               'reverse-engineer the process to obtain the original samples based on the Rk only, avoiding possible breaching '
               'of data privacy.',
               'Note that the “privacy” in CIL (i.e., cannot re-use past exemplars) may be different from the definition of '
               'other fields (such as data encryption).'],
     'raw_file': 'q4/2205.14922.txt',
     'agent_note': 'Contradicts as an assertion (the stored autocorrelation statistic cannot be reverse-engineered); no '
                   'attack is run, and the paper itself narrows "privacy" to not re-using exemplars.'},
    {'id': 'q4:10', 'tag': 'M6', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Magistri et al., "Elastic Feature Consolidation for Cold Start Exemplar-Free Incremental Learning" (EFC; '
               'arXiv:2402.03917; ICLR 2024)',
     'version': 'v3, 30 May 2024', 'url': 'https://arxiv.org/abs/2402.03917',
     'quote': ['Prototypes – differently than exemplars – offer a privacy-preserving way to mitigate forgetting.'],
     'raw_file': 'q4/2402.03917.txt',
     'agent_note': 'Contradicts as an assertion (prototypes called privacy-preserving without qualification or test).'},

    # ------------------------------------------------------------------ M7
    {'id': 'q2:13', 'tag': 'M7', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Hsu, Liu, Ramasamy, Kira, "Re-evaluating Continual Learning Scenarios: A Categorization and Case for Strong '
               'Baselines" (arXiv:1810.12488)',
     'version': 'v4, 23 Jan 2019', 'url': 'https://arxiv.org/abs/1810.12488',
     'quote': ['The total static memory overhead is controlled to be the same among L2, Naive rehearsal, Naive rehearsal-C, '
               'online EWC, SI, MAS, GEM, and DGR. Each value is the average of 10 runs.',
               'Naive rehearsal ✓ 99.40 ± 0.08 95.16 ± 0.49 90.78 ± 0.85 Naive rehearsal-C ✓ 99.57 ± 0.07 97.11 ± 0.34 '
               '95.59 ± 0.49',
               'GEM ✓ 98.42 ± 0.10 96.16 ± 0.35 92.20 ± 0.12 DGR ✓ 99.47 ± 0.03 95.74 ± 0.23 91.24 ± 0.33 RtF ✓ 99.66 ± 0.03 '
               '97.31 ± 0.11 92.56 ± 0.21'],
     'raw_file': 'q2/1810.12488v4.txt',
     'agent_note': 'Contradicts, squarely in scope (small MLP from scratch, split MNIST, equal static memory): DGR 91.24 and '
                   'RtF 92.56, storing no data, are not behind naive rehearsal 90.78 (compressed rehearsal is 95.59).'},
    {'id': 'q2:14', 'tag': 'M7', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'van de Ven & Tolias, "Three scenarios for continual learning" (arXiv:1904.07734)',
     'version': 'v1, 15 Apr 2019', 'url': 'https://arxiv.org/abs/1904.07734',
     'quote': ['For DGR and DGR+distill, a separate generative model was sequentially trained on all tasks. A symmetric '
               'variational autoencoder [VAE; 26] was used as generative model, with 2 fully connected hidden layers of 400 '
               '(split MNIST) or 1000 (permuted MNIST) units and a stochastic latent variable layer of size 100.',
               'DGR 99.50 (± 0.03) 95.72 (± 0.25) 90.79 (± 0.41) DGR+distill 99.61 (± 0.02) 96.83 (± 0.20) 91.79 (± 0.32) '
               'Replay + Exemplars iCaRL (budget = 2000) - - 94.57 (± 0.11)'],
     'raw_file': 'q2/1904.07734v1.txt',
     'agent_note': 'Contradicts in scope: small fully connected networks from scratch; generative replay without stored data '
                   '(DGR+distill 91.79) is within a few points of iCaRL with 2,000 stored exemplars (94.57), not well below. '
                   "This is also the source of the declaration's '90.79' replay figure, which is DGR (Q2 dossier S2)."},
    {'id': 'q2:15', 'tag': 'M7', 'reading': 'states', 'reading_by': RB,
     'source': 'van de Ven & Tolias, "Three scenarios for continual learning" (arXiv:1904.07734)',
     'version': 'v1, 15 Apr 2019', 'url': 'https://arxiv.org/abs/1904.07734',
     'quote': ['EWC 98.64 (± 0.22) 63.95 (± 1.90) 20.01 (± 0.06)',
               'DGR 99.50 (± 0.03) 95.72 (± 0.25) 90.79 (± 0.41) DGR+distill 99.61 (± 0.02) 96.83 (± 0.20) 91.79 (± 0.32) '
               'Replay + Exemplars iCaRL (budget = 2000) - - 94.57 (± 0.11)'],
     'raw_file': 'q2/1904.07734v1.txt',
     'agent_note': 'States M7 for the regularisation branch of exemplar-free methods, in scope (same small networks from '
                   'scratch): EWC 20.01 class-IL against iCaRL 94.57. The same table contradicts it for generative replay '
                   '(q2:14). These are two readings of one table, one per method family.'},
    {'id': 'q2:16', 'tag': 'M7', 'reading': 'states', 'reading_by': RB,
     'source': 'Gao, Zhao, Ghanem, Zhang, "R-DFCIL: Relation-Guided Representation Learning for Data-Free Class Incremental '
               'Learning" (arXiv:2203.13104; ECCV 2022)',
     'version': 'v2, 21 Jul 2022', 'url': 'https://arxiv.org/abs/2203.13104',
     'quote': ['These approaches may come through the first few tasks (i.e., short-term CIL), but they lose the '
               'stabilityplasticity balance when learning many tasks (i.e., long-term CIL).',
               'UCIR (CNN) [8] ✗ 55.73 ± 0.89 53.22 ± 0.71 50.08 ± 0.35 PODNet (CNN) [4] ✗ 56.19 ± 1.00 52.53 ± 0.55 '
               '49.14 ± 0.25 UCIR-DF (CNN) [8] ✓ 39.49 ± 0.81 25.54 ± 1.51 9.62 ± 0.73 PODNet-DF (CNN) [4] ✓ 40.54 ± 1.68 '
               '33.57 ± 2.48 20.18 ± 0.76 ABD [25] ✓ 50.55 ± 1.14 43.65 ± 2.40 25.27 ± 1.09 R-DFCIL (Ours) ✓ 54.76 ± 0.76 '
               '49.70 ± 0.61 30.01 ± 0.56'],
     'raw_file': 'q2/2203.13104v2.txt',
     'agent_note': 'States M7 at long horizons, in scope (ResNet-32 from scratch, no pretraining): every data-free method '
                   'is well below the exemplar methods at N=26 (best 30.01 vs UCIR 50.08), while R-DFCIL is near them at N=6 '
                   '(54.76 vs 55.73). Protocol: 50-class first task.'},
    {'id': 'q1:16', 'tag': 'M7', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'He et al., "Semantic Shift Estimation via Dual-Projection and Classifier Reconstruction for Exemplar-Free '
               'Class-Incremental Learning" (DPCR; arXiv:2503.05423; ICML 2025)',
     'version': 'v4, 18 May 2025', 'url': 'https://arxiv.org/abs/2503.05423',
     'quote': ['In this paper, we focus on the cold-start setting (Magistri et al., 2024), where the model is initialized '
               'randomly and the all tasks contains the same number of categories',
               'As shown in Table. 6, even comparing with the EBCIL methods, our DPCR can have competitive performance. When the '
               'memory size is 500, all the EBCIL methods perform poorly and our DPCR outperforms them with considerable gap. '
               'With the increased memory size of 1000, the advantage of replaying exemplars begins to emerge. However, our '
               'DPCR can still achieve the second best or even best results with T=10.',
               'iCaRL-NCM (Rebuffi et al., 2017) 1000 46.78 62.62 40.71 57.47'],
     'raw_file': 'q1/pdf_2503.05423v4.txt',
     'agent_note': 'Contradicts in part: from a random start (ResNet-18, cold start) the exemplar-free DPCR is ahead of '
                   'replay at 500 and 1,000 stored images at T=10. Not matched bytes (DPCR stores a d x d Gram per class), '
                   "and ResNet-18 is not a 'small model' in the repository's sense."},
    {'id': 'q2:17', 'tag': 'M7', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Liu et al., "Generative Feature Replay For Class-Incremental Learning" (GFR; arXiv:2004.09199; CVPR 2020 '
               'workshop)',
     'version': 'v1, 20 Apr 2020', 'url': 'https://arxiv.org/abs/2004.09199',
     'quote': ['For CIFAR-100, we modify the ResNet-18 network to use 3×3 kernels for the first convolutional layer and train '
               'the model from scratch†.',
               'It is interesting that our method with Gaussian replay performs quite well compared to iCaRL, but slightly '
               'worse than Rebalance.'],
     'raw_file': 'q2/2004.09199v1.txt',
     'agent_note': 'Contradicts in part: from scratch, per-class Gaussian feature replay (class statistics, no data) is near '
                   'the exemplar methods (iCaRL; Rebalance slightly ahead), not well below.'},
    {'id': 'q1:17', 'tag': 'M7', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Zhu, Zhang, Cheng, Liu, "PASS++" (arXiv:2407.14029)',
     'version': 'v1, 19 Jul 2024', 'url': 'https://arxiv.org/abs/2407.14029',
     'quote': ['Table 8 reports the setting where each task [...] contains equal classes without pre-trained model. '
               'Specifically, we divide each dataset into five tasks equally and the results show that our method performs '
               'better or is comparable with data replay method PODNet [15]. Since DER [17] is a strong data replay method with '
               'continually expandable feature extractor backbones, it could outperform our exemplar-free approach in this CIL '
               'setting.',
               'TABLE 8: CIL with equally divided classes in all tasks. Dataset CIFAR-100 TinyImageNet ImageNet-Subset Last Avg '
               'Last Avg Last Avg PODnet [15] 45.58 58.31 36.36 47.04 49.76 64.72 DER [17] 54.83 63.58 42.58 52.36 65.88 74.54 '
               'PASS++ 52.21 65.15 37.19 49.32 48.75 63.95'],
     'raw_file': 'q1/pdf_2407.14029v1.txt',
     'agent_note': 'Contradicts in part: equal 5-task split without pretraining, class means ahead of PODNet (replay) on '
                   'CIFAR-100 (52.21 vs 45.58) and behind DER, which also expands its backbone (54.83). Buffer size not stated '
                   'in the caption.'},
    {'id': 'q1:18', 'tag': 'M7', 'reading': 'bears', 'reading_by': RB,
     'source': 'Magistri et al., "EFC++" (arXiv:2503.10439; International Journal of Computer Vision 134, 454 (2026))',
     'version': 'v4, 28 Sep 2026', 'url': 'https://arxiv.org/abs/2503.10439',
     'quote': ['Joint Training 71.00',
               'As a final note, we report the performance under Joint Training, where the gap remains substantial. Closing '
               'this gap will likely require either a more advanced strategy than Gaussian prototypes or improved '
               'regularization techniques beyond those we proposed.'],
     'raw_file': 'q1/pdf_2503.10439v4.txt',
     'agent_note': "Q1's dossier reads this 'states in effect'. Read 'bears': from scratch, even oracle statistics (49.33, "
                   'q1:13) leave cold start far below joint training (71.00), but no replay baseline is reported, so M7 '
                   '(against replay) is not asserted.'},
    {'id': 'q1:19', 'tag': 'M7', 'reading': 'close', 'reading_by': RB,
     'source': 'Goswami, Liu, Twardowski, van de Weijer, "FeCAM: Exploiting the Heterogeneity of Class Distributions in '
               'Exemplar-Free Continual Learning" (arXiv:2309.14062; NeurIPS 2023)',
     'version': 'v3, 12 Jan 2024', 'url': 'https://arxiv.org/abs/2309.14062',
     'quote': ['The proposed approach needs a strong feature extractor or a large amount of data in the first task to learn good '
               'representations, as we do not learn new features but reuse the ones learned on the first task (or from '
               'pretrained network). Therefore, the method is not apt when training from scratch, starting with small tasks. We '
               'would then need to extend the theory to feature distributions which undergo feature drift during training; next '
               'to prototype drift [68] also covariance changes should be modeled.'],
     'raw_file': 'q1/pdf_2309.14062v3.txt',
     'agent_note': "Close: an exemplar-free statistics method 'not apt when training from scratch, starting with small tasks'; "
                   "no comparison with replay in that statement. Q1's dossier reads it 'states'."},
    {'id': 'q3:19', 'tag': 'M7', 'reading': 'close', 'reading_by': RB,
     'source': 'McDonnell, Gong, Parvaneh, Abbasnejad, van den Hengel, "RanPAC: Random Projections and Pre-trained Models '
               'for Continual Learning" (arXiv:2307.02251; NeurIPS 2023)',
     'version': 'v3, 16 Jan 2024', 'url': 'https://arxiv.org/abs/2307.02251',
     'quote': ['commencing CL with a powerful feature-extractor has opened up new ideas for avoiding forgetting that are unlikely '
               'to work when training from scratch.',
               'Limitations: The value of Eqs (4) and (5) are completely reliant on supply of a good generic feature extractor. '
               'For this reason, they are unlikely to be as powerful if used in CL methods that train networks from scratch.'],
     'raw_file': 'q3/pdf_2307.02251v3.txt',
     'agent_note': 'Close: the statistics methods are expected to be weaker from scratch; no replay comparison.'},
    {'id': 'q2:18', 'tag': 'M7', 'reading': 'bears', 'reading_by': RB,
     'source': 'Smith, Hsu, Balloch, Shen, Jin, Kira, "Always Be Dreaming: A New Approach for Data-Free Class-Incremental '
               'Learning" (ABD; arXiv:2106.09701; ICCV 2021)',
     'version': 'v2, 19 Aug 2021', 'url': 'https://arxiv.org/abs/2106.09701',
     'quote': ['Naive Rehearsal Coreset 34.0 ± 0.2 73.4 ± 0.8 24.0 ± 1.0 64.6 ± 2.1 14.9 ± 0.7 51.4 ± 2.9 LwF [36] Coreset '
               '39.4 ± 0.3 79.0 ± 0.0 27.4 ± 0.8 69.4 ± 0.4 16.6 ± 0.4 54.2 ± 2.2 BiC [61] Coreset 53.7 ± 0.4 87.5 ± 0.9 45.9 ± '
               '1.8 81.9 ± 2.0 37.5 ± 3.2 71.7 ± 3.4 Ours Synthetic 43.9 ± 0.9 78.6 ± 1.1 33.7 ± 1.2 69.6 ± 1.6 20.0 ± 1.4 52.5 '
               '± 2.5'],
     'raw_file': 'q2/2106.09701v2.txt',
     'agent_note': 'Bears (both ways within one table): from scratch on CIFAR-100, 10 tasks, inversion replay 33.7 is ahead '
                   'of naive rehearsal with 2,000 images (24.0) and well behind BiC with the same coreset (45.9).'},
]
