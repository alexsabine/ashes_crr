"""Claims for Relational_Reference_Memory/DECLARATION_2.md Part W, family F2 (positions P3, P5, P7), transcribed from the
dossier docs/citations/rrm2_f2_2026-09-30.md (fetched 2026-09-30; extracted texts held outside the repository under
/tmp/claude-0/rrm2_src/, named in `raw_file` relative to that root). Every quote is copied from a dossier blockquote.

'reading' is decided by the grading agent from the quote, for the investigator's review ('reading_by'). Reading policy
(RQM's, unchanged, as in claims.py), fixed before the readings were written and applied to every position:
  states       the source asserts (or reports as its own result) every predicate of the position, for at least one of the
               objects the position names, within the position's scope;
  close        the source asserts part of the position, or the position in a narrower or different scope;
  bears        relevant evidence or a bound that neither asserts nor negates the position;
  contradicts  the source asserts or reports the negation of the position within its scope.
Position-specific readings (fixed before the readings were written):
  P3  'states' needs a published method that keeps a few raw exemplars AND stored class statistics (or prototypes) and uses
      the kept exemplars to correct the stored statistics. Recomputing a class mean from the kept exemplars alone
      (iCaRL-style NME) is 'close'; a hybrid of exemplars and stored statistics in which the exemplars do not correct the
      statistics is 'close'; a source that only bears on the combination is 'bears'.
  P5  read against RRM's full transport (DECLARATION.md section 1): stored old-class feature statistics; a few KEPT anchor
      rows; the anchors' features stored at the cut; a relation map (ridge, in the anchors' dual form); transport by the
      anchors' measured movement, the part outside the anchors' span carried stale. A source with only part of this
      (a map fitted on current-task, generated or external data; references that are not kept anchors; a kernel rather
      than a linear relation) is 'close'. The caller's instruction: 'states' needs the full mechanism, partial = close.
  P7  'states': the source reports that a class-IL learner's feature drift is approximately linear or is well corrected by
      a linear map (including: a linear map performs as well as or better than non-linear ones). 'contradicts': the
      source reports that a linear map fails to capture the drift, or that a non-linear map is needed (as the caller
      defined it). A linear constraint imposed by design, or linear alignment of a different object (weights), is 'close'.
"""

RB = "grading agent; for the investigator's review"

CLAIMS = [
    # ------------------------------------------------------------------ P3
    {'id': 'w2:0', 'tag': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'Iscen, Zhang, Lazebnik, Schmid, "Memory-Efficient Incremental Learning Through Feature Adaptation" (MEA; '
               'arXiv:2004.00713; venue not verified on the day)',
     'version': 'v2, 24 Aug 2020', 'url': 'https://arxiv.org/abs/2004.00713',
     'quote': ['We also present Ours-hybrid, a variant of our method where we keep P images and L feature descriptors.',
               'Ours-hybrid shows that we can preserve features with smaller number of images and further improve accuracy.',
               'that maps output of the previous feature extractor ht−1 θ to the current feature extractor ht θ using the '
               'current task images X t.'],
     'raw_file': 'f2/src/pdf_2004.00713v2.txt',
     'agent_note': 'Close: a published hybrid of a few kept images and stored per-class feature vectors, and the stored '
                   'vectors are adapted as the network changes; but the adaptation network is trained on the current task '
                   'images, not on the kept images, so the kept exemplars do not correct the stored features.'},
    {'id': 'w2:1', 'tag': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'Goswami, Soutif-Cormerais, Liu, Kamath, Twardowski, van de Weijer, "Resurrecting Old Classes with New Data '
               'for Exemplar-Free Continual Learning" (ADC; arXiv:2405.19074; CVPR 2024)',
     'version': 'v1, 29 May 2024', 'url': 'https://arxiv.org/abs/2405.19074',
     'quote': ['We compare the last-task accuracy of ADC with exemplar-based NME where the exemplars are used to estimate the '
               'old class prototype positions in the new feature space.',
               'We show in Fig. 4 that ADC outperforms NME using 20 exemplars per class for CIFAR-100 (total memory size of '
               '2000 samples)'],
     'raw_file': 'f2/src/pdf_2405.19074v1.txt',
     'agent_note': 'Close (iCaRL-style): kept exemplars place the old prototypes in the new feature space by recomputation; '
                   'no stored statistic is corrected. Bears on the value of the niche: an exemplar-free drift estimate beat '
                   'NME with 20 exemplars per class on CIFAR-100.'},
    {'id': 'w2:2', 'tag': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'Nguyen, Dao, Nguyen, Le, Wong, "Memory-efficient Continual Learning with Prototypical Exemplar '
               'Condensation" (arXiv:2603.13804; CVPR 2026 Findings per the CVF listing)',
     'version': 'v2, 10 Apr 2026', 'url': 'https://arxiv.org/abs/2603.13804',
     'quote': ['we propose to further compress the memory footprint by synthesizing and storing prototypical exemplars, which '
               'can form representative prototypes when passed through the feature extractor.'],
     'raw_file': 'f2/src/pdf_2603.13804v2.txt',
     'agent_note': 'Close: a few stored (synthesised) exemplars per class stand in for the class prototype, which the '
                   'current extractor recomputes from them; recomputation, not correction of a stored statistic, and the '
                   'stored items are synthetic rather than kept raw rows.'},
    {'id': 'w2:3', 'tag': 'P3', 'reading': 'bears', 'reading_by': RB,
     'source': 'Lanzillotta, Meier, Hofmann, "Heads collapse, features stay: Why Replay needs big buffers" '
               '(arXiv:2512.07400; ICLR 2026)',
     'version': 'v2, 19 Mar 2026', 'url': 'https://arxiv.org/abs/2512.07400',
     'quote': ['while minimal buffers successfully anchor feature geometry and prevent deep forgetting, mitigating shallow '
               'forgetting typically requires substantially larger buffer capacities.',
               'Conversely, we identify that the “strong collapse” induced by small buffers leads to rank-deficient '
               'covariances and inflated class means, effectively blinding the classifier to true population boundaries.',
               'suggesting that explicitly correcting these statistical artifacts could unlock robust performance with '
               'minimal replay.'],
     'raw_file': 'f2/src/pdf_2512.07400v2.txt',
     'agent_note': 'Bears: class statistics estimated from a small buffer are biased (rank-deficient covariances, inflated '
                   'means), while a small buffer suffices to hold feature geometry; the paper proposes, but does not '
                   'implement, correcting the statistics. This is the gap a hybrid that keeps full-class statistics at the '
                   'cut and a few rows would address.'},
    {'id': 'w2:4', 'tag': 'P3', 'reading': 'bears', 'reading_by': RB,
     'source': 'Khademi Nori, Kim, Wang, "Federated Class-Incremental Learning: A Hybrid Approach Using Latent Exemplars and '
               'Data-Free Techniques to Address Local and Global Forgetting" (arXiv:2501.15356; ICLR 2025)',
     'version': 'v3, 13 Mar 2025', 'url': 'https://arxiv.org/abs/2501.15356',
     'quote': ['we propose an approach called Hybrid Rehearsal (HR), which utilizes latent exemplars and data-free techniques '
               'to address local and global forgetting, respectively.'],
     'raw_file': 'f2/src/pdf_2501.15356v3.txt',
     'agent_note': 'Bears: a published hybrid memory (stored latent exemplars plus generated data), but no class '
                   'statistics are corrected by the kept exemplars.'},
    {'id': 'w2:5', 'tag': 'P3', 'reading': 'bears', 'reading_by': RB,
     'source': 'Ho, Liu, Du, Gao, Xiang, "Prototype-Guided Memory Replay for Continual Learning" (arXiv:2108.12641; '
               'IEEE TNNLS)',
     'version': 'v3, 4 Mar 2023', 'url': 'https://arxiv.org/abs/2108.12641',
     'quote': ['Each meta-learned prototypical vector in {c1, ..., cL} serve as a reference to acquire samples that are '
               'representative for the correspond class.',
               'Our devised memory is dynamically updated, considering the renewal of the prototype for each class in each '
               'training epoch.'],
     'raw_file': 'f2/src/pdf_2108.12641v3.txt',
     'agent_note': 'Bears: prototypes and a few kept samples in one learner, in the reverse direction (the prototypes '
                   'select the kept samples; the samples do not correct stored statistics).'},
    # ------------------------------------------------------------------ P5
    {'id': 'w2:6', 'tag': 'P5', 'reading': 'states',
     'reading_by': "investigator (review of the grading agent's 'close'; AGENT_LOG 198)",
     'investigator_note': "P5's predicates, one by one: stored old-class statistics (class Gaussians) - yes; transported "
                          "by the measured feature movement of anchors (D = Fnew - Fold) - yes; the anchors kept (a fixed "
                          "set for the whole stream, features stored) - yes; a few (1,024 images against ImageNet-scale "
                          "data) - yes on the reading 'a small fixed set'. Anchor provenance (external, not stream rows) and "
                          "the relation's form (softmax kernel, not ridge) are not predicates of P5 as declared, so the "
                          "declared policy ('every predicate ... for at least one of the objects') reads STATES. Decided "
                          "on reading the agent's report, before grade_w.py was meant to run; a script error ran it once "
                          "under the agent's reading first (grade_w_run1.txt, pinned). grade_w.py prints the verdict under "
                          "the agent's reading beside it.",
     'source': 'Rao, Ha, Zhao, Liu, Alippi, "Scalable Analytic Classifiers with Associative Drift Compensation for '
               'Class-Incremental Learning of Vision Transformers" (LR-RGDA and HopDC; arXiv:2602.00144)',
     'version': 'v1, 29 Jan 2026', 'url': 'https://arxiv.org/abs/2602.00144',
     'quote': ['we posit that old class prototypes shift consistently with semantically related unlabelled anchors, allowing '
               'for precise recalibration without historical exemplars.',
               'Let A = {ai}N i=1 be a fixed set of unlabeled anchor images.',
               'this operation effectively computes a weighted average of anchor drifts, where weights are determined by the '
               'semantic similarity between the old class samples and the anchors in the original feature space.',
               'employ an auxiliary set of 1,024 unlabeled anchors drawn from ImageNet-1K (Deng et al., 2009). Following the '
               'settings of SLDC (Rao et al., 2026), we also utilize samples of the current task as supplement anchors.'],
     'raw_file': 'f2/src/pdf_2602.00144v1.txt',
     'agent_note': 'Close, and the NEAREST match to P5 found in either sweep. HopDC keeps a fixed anchor set for the whole '
                   'stream, stores the anchors\' features, measures their drift at each task (D = Fnew - Fold), samples '
                   'pseudo-features from each old class\'s stored Gaussian, moves them by a similarity-weighted average of '
                   'the anchor drifts, and re-estimates the stored mean and covariance. It differs from RRM in: the '
                   'anchors are external unlabeled images (ImageNet-1K), supplemented by current-task samples in the main '
                   'experiments, not kept training rows of the stream (and they are not replayed); the relation is a '
                   'top-k softmax attention (a kernel smoother), not RRM\'s linear ridge relation, so there is no '
                   'in-span/out-of-span split; the backbone is a pre-trained ViT. A reviewer who reads P5 at the level of '
                   'its wording (stored statistics transported by the measured movement of a kept anchor set) may read '
                   'this as STATES; the grading agent reads CLOSE because the transport rule and the anchor provenance '
                   'differ (judgement call, flagged in the dossier).'},
    {'id': 'w2:7', 'tag': 'P5', 'reading': 'close', 'reading_by': RB,
     'source': 'Rao, Xu, Li, Zhao, Liu, Ha, Alippi, "Compensating Distribution Drifts in Class-incremental Learning of '
               'Pre-trained Vision Transformers" (SLDC; arXiv:2511.09926; AAAI 2026)',
     'version': 'v1, 13 Nov 2025', 'url': 'https://arxiv.org/abs/2511.09926',
     'quote': ['The linear operator At ∈Rd×d for approximating Pt−1→t is obtained by solving the regularized least-square '
               'solution',
               'this paper proposes auxiliary data enrichment (ADE) to improve the prediction by leveraging unlabeled '
               'auxiliary data from arbitrary sources.',
               'ADE operates without requiring labeled data and remains consistent with the exemplar-free continual '
               'learning (CIL) framework since it does not preserve any task-relevant data from previous tasks.'],
     'raw_file': 'f2/src/pdf_2511.09926v1.txt',
     'agent_note': 'Close: alpha1-SLDC fits a ridge-regularised linear operator between old and new features and applies it '
                   'to each stored class Gaussian (mean A mu, covariance A Sigma A^T, per its Algorithm), which is RRM\'s '
                   'linear transport in primal form; the pairs are current-task features plus unlabeled auxiliary data '
                   'from an external source (ADE), not kept rows of past tasks; the paper stresses that it keeps no '
                   'task-relevant data.'},
    {'id': 'w2:8', 'tag': 'P5', 'reading': 'close', 'reading_by': RB,
     'source': 'Zhou, Sun, Ye, Zhan, "Expandable Subspace Ensemble for Pre-Trained Model-Based Class-Incremental Learning" '
               '(EASE; arXiv:2403.12030; CVPR 2024)',
     'version': 'v1, 18 Mar 2024', 'url': 'https://arxiv.org/abs/2403.12030',
     'quote': ['we design a semantic-guided prototype complement strategy that synthesizes old classes’ new features without '
               'using any old class instance.',
               'we measure the similarity between old and new classes in the old subspace (where all classes co-occur) and '
               'utilize it to reconstruct prototypes in the new embedding space.'],
     'raw_file': 'f2/src/pdf_2403.12030v1.txt',
     'agent_note': 'Close: an old class\'s prototype is stored as a relation (similarities) to references in the old space '
                   'and rebuilt from the references as seen in the new space, the owner\'s relational reading; the '
                   'references are the new classes\' prototypes, not kept anchors, and the content is a mean.'},
    {'id': 'w2:9', 'tag': 'P5', 'reading': 'close', 'reading_by': RB,
     'source': 'Toldo, Ozay, "Bring Evanescent Representations to Life in Lifelong Class Incremental Learning" (CVPR 2022; '
               'CVF open access)',
     'version': 'CVF open-access version (no arXiv version checked)',
     'url': 'https://openaccess.thecvf.com/content/CVPR2022/papers/Toldo_Bring_Evanescent_Representations_to_Life_in_'
            'Lifelong_Class_Incremental_Learning_CVPR_2022_paper.pdf',
     'quote': ['we propose a framework which aims to (i) model the semantic drift by learning the relationship between '
               'representations of past and novel classes among incremental steps, and (ii) estimate the feature drift, '
               'defined as the evolution of the representations learned by models at each incremental step.'],
     'raw_file': 'f2/src/cvf_Toldo_CVPR2022.txt',
     'agent_note': 'Close: stored past-class representations are updated through learned relations to the novel classes and '
                   'a feature-drift model; the references are current data, not kept anchors.'},
    {'id': 'w2:10', 'tag': 'P5', 'reading': 'close', 'reading_by': RB,
     'source': 'Cui, Zhou, Peng, "Bi-C2R: Bidirectional Continual Compatible Representation for Re-indexing Free Lifelong '
               'Person Re-identification" (arXiv:2512.25000; header: IEEE TPAMI)',
     'version': 'v1, 31 Dec 2025', 'url': 'https://arxiv.org/abs/2512.25000',
     'quote': ['we propose a Bidirectional Continuous Compatible Representation (Bi-C2R) framework to continuously update the '
               'gallery features extracted by the old model to perform efficient L-ReID in a compatible manner.',
               'forward transfer compromises the old data by employing new data to train the feature transfer network, '
               'where the transferred feature ignores the discriminativeness of the old knowledge.'],
     'raw_file': 'f2/src/pdf_2512.25000v1.txt',
     'agent_note': 'Close (retrieval, not class-IL): stored old-model features are transported to the new space by a '
                   'learned non-linear transfer network trained on new data; the paper names the bias of fitting on new '
                   'data, the bias kept anchors would address.'},
    {'id': 'w2:11', 'tag': 'P5', 'reading': 'close', 'reading_by': RB,
     'source': 'Honda, "Adversarial Pseudo-replay for Exemplar-free Class-incremental Learning" (APR; arXiv:2511.17973; '
               'WACV 2026)',
     'version': 'v1, 22 Nov 2025', 'url': 'https://arxiv.org/abs/2511.17973',
     'quote': ['A transfer matrix trained for each class using the adversarially generated samples calibrates a covariance '
               'matrix via simple matrix multiplication.',
               'The gap between old and new feature spaces are typically estimated using the new task data and preserved '
               'feature extractor.'],
     'raw_file': 'f2/src/pdf_2511.17973v1.txt',
     'agent_note': 'Close: stored per-class covariances are carried by a per-class linear transfer matrix fitted on points '
                   'placed at the old classes; the points are generated from current data each task (ADC\'s route), not '
                   'kept rows.'},
    {'id': 'w2:12', 'tag': 'P5', 'reading': 'bears', 'reading_by': RB,
     'source': 'Gu, Shim, Shkurti, "Preserving Linear Separability in Continual Learning by Backward Feature Projection" '
               '(BFP; arXiv:2303.14595; CVPR 2023)',
     'version': 'v3, 28 Jun 2023', 'url': 'https://arxiv.org/abs/2303.14595',
     'quote': ['we propose to learn a linear transformation that projects the new feature space back to the old one',
               'BFP can be integrated with existing experience replay methods and boost performance by a significant '
               'margin.'],
     'raw_file': 'f2/src/pdf_2303.14595v3.txt',
     'agent_note': 'Bears: a linear map between the new and old feature spaces is learned on the replay buffer and current '
                   'data, but it is used as a distillation constraint on the learner, not to transport stored statistics.'},
    # ------------------------------------------------------------------ P7
    {'id': 'w2:13', 'tag': 'P7', 'reading': 'states', 'reading_by': RB,
     'source': 'Gomez-Villa, Goswami, Wang, Bagdanov, Twardowski, van de Weijer, "Exemplar-free Continual Representation '
               'Learning via Learnable Drift Compensation" (LDC; arXiv:2407.08536; ECCV 2024)',
     'version': 'v1, 11 Jul 2024', 'url': 'https://arxiv.org/abs/2407.08536',
     'quote': ['The projector pt F can be any trainable mapping function. However, we found that a linear layer performs best '
               'in this task (see section 4.4).',
               'We observe that a single linear layer works better in both settings.'],
     'raw_file': 'f2/src/pdf_2407.08536v1.txt',
     'agent_note': 'States P7 (second disjunct): in its ablation (linear, linear + bias, linear + ReLU, two-layer MLP) a '
                   'single linear drift map compensated best, supervised and semi-supervised, on a learner trained from '
                   'scratch.'},
    {'id': 'w2:14', 'tag': 'P7', 'reading': 'states', 'reading_by': RB,
     'source': 'Rao, Xu, Li, Zhao, Liu, Ha, Alippi, "Compensating Distribution Drifts in Class-incremental Learning of '
               'Pre-trained Vision Transformers" (SLDC; arXiv:2511.09926; AAAI 2026)',
     'version': 'v1, 13 Nov 2025', 'url': 'https://arxiv.org/abs/2511.09926',
     'quote': ['The empirical results show that the linear operator can compensate for the distribution drift appropriately'],
     'raw_file': 'f2/src/pdf_2511.09926v1.txt',
     'agent_note': 'States P7 (second disjunct) for pre-trained ViTs under sequential fine-tuning; the same sentence goes on '
                   'to the residuals (w2:15). Two readings of one source, recorded as two claims.'},
    {'id': 'w2:15', 'tag': 'P7', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Rao, Xu, Li, Zhao, Liu, Ha, Alippi, "Compensating Distribution Drifts in Class-incremental Learning of '
               'Pre-trained Vision Transformers" (SLDC; arXiv:2511.09926; AAAI 2026)',
     'version': 'v1, 13 Nov 2025', 'url': 'https://arxiv.org/abs/2511.09926',
     'quote': ['but it still yields large prediction residuals when predicting the post-optimization deep features, implying '
               'that a nonlinear mapping is required. However, the direct implementation of popular nonlinear transformation '
               'such as multilayer perceptrons (MLPs) leads to overfitting and produces distributions that are less accurate '
               'than those obtained with linear operators.'],
     'raw_file': 'f2/src/pdf_2511.09926v1.txt',
     'agent_note': 'Contradicts P7 (first disjunct): the drift is not linear (large residuals, a non-linear map is required); '
                   'yet a full MLP is worse than the linear map, and the paper settles on a linear map plus a small '
                   'non-linear term ("weak-nonlinear").'},
    {'id': 'w2:16', 'tag': 'P7', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Rao, Ha, Zhao, Liu, Alippi, "Scalable Analytic Classifiers with Associative Drift Compensation for '
               'Class-Incremental Learning of Vision Transformers" (LR-RGDA and HopDC; arXiv:2602.00144)',
     'version': 'v1, 29 Jan 2026', 'url': 'https://arxiv.org/abs/2602.00144',
     'quote': ['This indicates that self-supervised features undergo more substantial and nonlinear representation drift when '
               'the backbone is aggressively updated.',
               'It confirms that using associative memory with unlabelled anchors is more effective than simple linear '
               'transformation of α1-SLDC for mitigating semantic drift.'],
     'raw_file': 'f2/src/pdf_2602.00144v1.txt',
     'agent_note': 'Contradicts P7 in the regime named (self-supervised pre-trained ViT, aggressive updates): the drift is '
                   'non-linear, and a local anchor-based interpolation beats the linear operator.'},
    {'id': 'w2:17', 'tag': 'P7', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Xu, Krawczyk, "Two-Way Is Better Than One: Bidirectional Alignment with Cycle Consistency for Exemplar-Free '
               'Class-Incremental Learning" (BiCyc; arXiv:2606.05675; ICLR 2026)',
     'version': 'v1, 4 Jun 2026', 'url': 'https://arxiv.org/abs/2606.05675',
     'quote': ['Across both splits, multilayer adapters consistently outperform a single linear map',
               'If new and old features differed by a single global affine transform, a linear adapter would suffice; the '
               'observed trade-offs instead point',
               'to content-dependent, anisotropic drift, which conditional/nonlinear adapters model more faithfully.'],
     'raw_file': 'f2/src/pdf_2606.05675v1.txt',
     'agent_note': 'Contradicts P7: on CIFAR-100 (10 and 20 tasks) a single linear map lost to multilayer adapters, read by '
                   'the authors as content-dependent, anisotropic drift. The authors add that a parameter-matched linear '
                   'control is still to be run, so capacity is not separated from architecture.'},
    {'id': 'w2:18', 'tag': 'P7', 'reading': 'close', 'reading_by': RB,
     'source': 'Xu, Krawczyk, "Geometry-Anchored Transport Framework for Exemplar-Free Class-Incremental Learning" (GATF; '
               'arXiv:2606.25347; ECCV 2026)',
     'version': 'v2, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.25347',
     'quote': ['The affine component captures the dominant global drift, while the residual network models localized '
               'non-linear corrections.'],
     'raw_file': 'f2/src/pdf_2606.25347v2.txt',
     'agent_note': 'Close: the dominant part of the drift is affine, with a non-linear residual.'},
    {'id': 'w2:19', 'tag': 'P7', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Xu, Krawczyk, "Geometry-Anchored Transport Framework for Exemplar-Free Class-Incremental Learning" (GATF; '
               'arXiv:2606.25347; ECCV 2026)',
     'version': 'v2, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.25347',
     'quote': ['As the backbone assimilates novel categories, the underlying embedding space undergoes continuous non-linear '
               'deformation.'],
     'raw_file': 'f2/src/pdf_2606.25347v2.txt',
     'agent_note': 'Contradicts P7 (first disjunct) as the paper\'s framing; stated as background rather than measured '
                   'alone. Two readings of one source, recorded as two claims (w2:18, w2:19).'},
    {'id': 'w2:20', 'tag': 'P7', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Xu, Jin, Sun, Xuan, Li, "Dual-Estimator: Decoupling Global and Local Semantic Shift for Drift Compensation '
               'in Class-Incremental Learning" (Dual-E; CVPR 2026; CVF open access)',
     'version': 'CVF open-access version (arXiv title search 2026-09-30: no result)',
     'url': 'https://openaccess.thecvf.com/content/CVPR2026/papers/Xu_Dual-Estimator_Decoupling_Global_and_Local_Semantic_'
            'Shift_for_Drift_Compensation_CVPR_2026_paper.pdf',
     'quote': ['realized as a linear mapping in the drift estimator, is affected by non-uniform semantic distributions, '
               'limiting the contribution of',
               'low-frequency semantics and leading to biased compensation for corresponding old classes.'],
     'raw_file': 'f2/src/cvf_DualEstimator_CVPR2026.txt',
     'agent_note': 'Contradicts P7 for one global linear map (biased compensation under non-uniform semantics); its remedy is '
                   'a mixture of local maps, each a linear layer, plus a low-rank global map, i.e. piecewise linear.'},
    {'id': 'w2:21', 'tag': 'P7', 'reading': 'bears', 'reading_by': RB,
     'source': 'Xu, Jin, Sun, Xuan, Li, "Class-Aware Drift Compensation for Non-Uniform Semantic Shift in Continual '
               'Learning" (CADC; CVPR 2026 Findings; CVF open access)',
     'version': 'CVF open-access version (arXiv title search 2026-09-30: no result)',
     'url': 'https://openaccess.thecvf.com/content/CVPR2026F/papers/Xu_Class-Aware_Drift_Compensation_for_Non-Uniform_'
            'Semantic_Shift_in_Continual_Learning_CVPRF_2026_paper.pdf',
     'quote': ['This work reveals that the semantic shifts of old-class representations are non-uniform [15] across different '
               'classes, and drift compensation should be performed in a class-aware manner according to the extent of '
               'feature drift.',
               'The drift estimator, implemented as a linear layer, models the transfer pattern in the representation space '
               'by fitting outputs from the old and new models.'],
     'raw_file': 'f2/src/cvf_CADC_CVPR2026F.txt',
     'agent_note': 'Bears: drift differs across classes, but the estimator stays a linear layer, with class-wise weighting '
                   'of its compensation; neither asserts nor negates approximate linearity.'},
    {'id': 'w2:22', 'tag': 'P7', 'reading': 'close', 'reading_by': RB,
     'source': 'Kim, Kim, Sohn, "Measuring Representational Shifts in Continual Learning: A Linear Transformation '
               'Perspective" (arXiv:2505.20970; ICML 2025)',
     'version': 'v3, 12 Jun 2025', 'url': 'https://arxiv.org/abs/2505.20970',
     'quote': ['we introduce a novel metric, representation discrepancy, which quantifies the minimum alignment error of two '
               'representation spaces under a linear transformation.',
               'This implies that there exists a linear transformation T that closely approximates two weight matrices of '
               'each layers, demonstrating that Assumption 1 holds in practice.'],
     'raw_file': 'f2/src/pdf_2505.20970v3.txt',
     'agent_note': 'Close: measures representation drift modulo the best linear map, and reports that the weight matrices '
                   'at two task indices are linearly alignable (a ReLU network on Split-CIFAR100, a ResNet on ImageNet); '
                   'the object is the weights, not the features, and the residual after linear alignment is its measure '
                   'of forgetting.'},
    {'id': 'w2:23', 'tag': 'P7', 'reading': 'close', 'reading_by': RB,
     'source': 'Gu, Shim, Shkurti, "Preserving Linear Separability in Continual Learning by Backward Feature Projection" '
               '(BFP; arXiv:2303.14595; CVPR 2023)',
     'version': 'v3, 28 Jun 2023', 'url': 'https://arxiv.org/abs/2303.14595',
     'quote': ['a method for continual learning that allows the new features to change up to a learnable linear '
               'transformation of the old features.',
               'we can also see that the performance already saturates with a linear projection layer and a more complex '
               'non-linear projection (BFP-2) does not improve further.'],
     'raw_file': 'f2/src/pdf_2303.14595v3.txt',
     'agent_note': 'Close: the drift is constrained to be linear by design (a regulariser), and a non-linear projector gives '
                   'no gain; this is not a report of how an unconstrained learner drifts.'},
    # ---------------------------------------------- leads passed on from the F3 sweep (coordinator, 2026-09-30)
    {'id': 'w2:24', 'tag': 'P5', 'reading': 'close', 'reading_by': RB,
     'source': 'Chaudhury, "Forgetting is Not Erasure: Recovering Latent Knowledge via Transport Keys" (arXiv:2606.02860; '
               'technical report)',
     'version': 'v1, 1 Jun 2026', 'url': 'https://arxiv.org/abs/2606.02860',
     'quote': ['We describe transport keys at a systems level as compact interface-alignment operators estimated from a small '
               'set of paired anchor activations and evaluated through model stitching.',
               'Anchors are ordinary examples from the earlier task and are passed through both checkpoints.',
               'it is inserted between an early portion of a post-update network and a late portion of the pre-update '
               'network, and it maps the new activation coordinate system back into a form that the old downstream '
               'computation can decode.'],
     'raw_file': 'f2/src/pdf_2606.02860v1.txt',
     'agent_note': 'Close: the anchor side matches RRM exactly: a few kept examples of the earlier task, passed through the '
                   'old and the updated network, give paired features, and an alignment map is fitted on them. The '
                   'transported object differs: live post-update activations are mapped back (new to old) into a kept copy '
                   'of the pre-update late network, which is not stored old-class statistics carried forward (old to new) '
                   'into the current space. It also needs the Task A checkpoint, not features stored at the cut. The '
                   'report is preliminary and gives no key-fitting equations.'},
    {'id': 'w2:25', 'tag': 'P7', 'reading': 'close', 'reading_by': RB,
     'source': 'Chaudhury, "Forgetting is Not Erasure: Recovering Latent Knowledge via Transport Keys" (arXiv:2606.02860; '
               'technical report)',
     'version': 'v1, 1 Jun 2026', 'url': 'https://arxiv.org/abs/2606.02860',
     'quote': ['transport keys recover most of the original Task A performance after sequential training on Task B.',
               'It corrects per-channel drift, such as changes in activation scale or offset.',
               'In the same-domain CIFAR experiments, this compact correction explains most of the recovered accuracy.'],
     'raw_file': 'f2/src/pdf_2606.02860v1.txt',
     'agent_note': 'Close: in a two-task split of CIFAR-100 (a task-A head kept, an intermediate interface), a per-channel '
                   'scale-and-offset correction (a diagonal affine map) explains most of the recovery; cross-channel mixing '
                   'matters more under domain shift. This is a different scope from class-IL feature drift at the '
                   'penultimate layer, and a preliminary report.'},
    {'id': 'w2:26', 'tag': 'P5', 'reading': 'bears', 'reading_by': RB,
     'source': 'Li, Xiao, Jiang, Zuo, Zhang, Yang, "A Stitch in Time Saves Nine: Preserving Policy Compatibility Under '
               'Perception Updates in End-to-End Autonomous Driving" (arXiv:2606.21509; T-ITS under review)',
     'version': 'v1, 19 Jun 2026', 'url': 'https://arxiv.org/abs/2606.21509',
     'quote': ['We study low-complexity model stitching methods, including linear and convolutional stitchers, for restoring '
               'compatibility between updated perception modules and frozen downstream policy modules.',
               'where A ∈Rn×n and b ∈R1×n are estimated from the paired anchors [30].'],
     'raw_file': 'f2/src/pdf_2606.21509v1.txt',
     'agent_note': 'Bears: an affine map fitted by least squares on paired anchors across a module retrain, applied to live '
                   'latents feeding a frozen downstream policy; it is not a continual learner, and no stored statistics '
                   'are transported.'},
    {'id': 'w2:27', 'tag': 'P7', 'reading': 'bears', 'reading_by': RB,
     'source': 'Li, Xiao, Jiang, Zuo, Zhang, Yang, "A Stitch in Time Saves Nine: Preserving Policy Compatibility Under '
               'Perception Updates in End-to-End Autonomous Driving" (arXiv:2606.21509; T-ITS under review)',
     'version': 'v1, 19 Jun 2026', 'url': 'https://arxiv.org/abs/2606.21509',
     'quote': ['This result suggests that, under small distribution shifts, the original and updated latent representations '
               'remain approximately linearly aligned.',
               'These results indicate that sensor-induced representation shifts require a more expressive compatibility '
               'mapping than a simple linear transformation.'],
     'raw_file': 'f2/src/pdf_2606.21509v1.txt',
     'agent_note': 'Bears (outside class-IL: a perception module retrained from a new initialisation, sensor set-up or domain): '
                   'the change is approximately linear for small shifts and not for larger ones, the same split by regime '
                   'that the class-IL sources show.'},
]
