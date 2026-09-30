"""Claims for Relational_Reference_Memory/DECLARATION.md §6 (positions N1-N6), transcribed from the verified dossier
docs/citations/rrm_2026-09-30.md (fetched 2026-09-30; extracted texts held outside the repository under
/tmp/claude-0/rrm_src/, named in `raw_file` relative to that root). Every quote is copied from a dossier blockquote;
verify.py checks each against its extracted text.

'reading' is decided by the grading agent from the quote, for the investigator's review ('reading_by'). Reading policy
(RQM's, unchanged), fixed before the readings were written and applied to every position:
  states       the source asserts (or reports as its own result) every predicate of the position, for at least one of the
               objects the position names, within the position's scope;
  close        the source asserts part of the position, or the position in a narrower or different scope;
  bears        relevant evidence or a bound that neither asserts nor negates the position;
  contradicts  the source asserts or reports the negation of the position within its scope. For an existential position
               ('is published', 'reduces forgetting') the negation is 'not'; a failure in a sub-regime the position does not
               claim is a bound ('bears').
N5 is read against its full mechanism: stored old-class feature distributions, coordinates relative to a few KEPT anchors,
transport by the anchors' current features. A source that transports stored statistics by a map fitted on current-task
data, or that stores content relative to references that are not kept anchors, is 'close', not 'states'.
"""

RB = "grading agent; for the investigator's review"

CLAIMS = [
    # ------------------------------------------------------------------ N1
    {'id': 'rrm:0', 'tag': 'N1', 'reading': 'states', 'reading_by': RB,
     'source': 'Yu, Twardowski, Liu, Herranz, Wang, Cheng, Jui, van de Weijer, "Semantic Drift Compensation for '
               'Class-Incremental Learning" (SDC; arXiv:2004.00440; CVPR 2020)',
     'version': 'v1, 1 Apr 2020', 'url': 'https://arxiv.org/abs/2004.00440',
     'quote': ['we propose a new method to estimate the drift, called semantic drift, of features and compensate for it '
               'without the need of any exemplars. We approximate the drift of previous tasks based on the drift that is '
               'experienced by current task data.',
               'We aim at reducing the error that drift causes and propose a drift compensation to update previously computed '
               'prototypes. The main idea is to estimate the unknown drift according to the known drift of the current data '
               'during the training of the current task.'],
     'raw_file': 'src/pdf_2004.00440v1.txt',
     'agent_note': 'States N1: stored prototypes are corrected by the measured movement of reference points (current-task '
                   'embeddings, old vs new model). The reference points are current data, not kept anchors (N2).'},
    {'id': 'rrm:1', 'tag': 'N1', 'reading': 'states', 'reading_by': RB,
     'source': 'Gomez-Villa, Goswami, Wang, Bagdanov, Twardowski, van de Weijer, "Exemplar-free Continual Representation '
               'Learning via Learnable Drift Compensation" (LDC; arXiv:2407.08536; ECCV 2024)',
     'version': 'v1, 11 Jul 2024', 'url': 'https://arxiv.org/abs/2407.08536',
     'quote': ['We do not need to store any old images or features, or use any labels of the current data; we simply store '
               'only the old class prototypes and update them using the learned current task projector.',
               'The projector pt F can be any trainable mapping function. However, we found that a linear layer performs best '
               'in this task (see section 4.4).'],
     'raw_file': 'src/pdf_2407.08536v1.txt',
     'agent_note': 'States N1 with a linear map between the old and new feature spaces, learned on current-task data and '
                   'applied to stored prototypes: the same linear-transport form as RRM, with a different reference set.'},
    {'id': 'rrm:2', 'tag': 'N1', 'reading': 'states', 'reading_by': RB,
     'source': 'Goswami, Soutif-Cormerais, Liu, Kamath, Twardowski, van de Weijer, "Resurrecting Old Classes with New Data '
               'for Exemplar-Free Continual Learning" (ADC; arXiv:2405.19074; CVPR 2024)',
     'version': 'v1, 29 May 2024', 'url': 'https://arxiv.org/abs/2405.19074',
     'quote': ['To address this problem of feature drift estimation for exemplar-free methods, we propose to adversarially '
               'perturb the current samples such that their embeddings are close to the old class prototypes in the old model '
               'embedding space. We then estimate the drift in the embedding space from the old to the new model using the '
               'perturbed images and compensate the prototypes accordingly.'],
     'raw_file': 'src/pdf_2405.19074v1.txt',
     'agent_note': 'States N1: the reference points are adversarially moved current samples placed near each old prototype.'},
    {'id': 'rrm:3', 'tag': 'N1', 'reading': 'states', 'reading_by': RB,
     'source': 'Iscen, Zhang, Lazebnik, Schmid, "Memory-Efficient Incremental Learning Through Feature Adaptation" (MEA; '
               'arXiv:2004.00713)',
     'version': 'v2, 24 Aug 2020', 'url': 'https://arxiv.org/abs/2004.00713',
     'quote': ['Features are extracted using the old and new models from new class images to train a feature adaptation '
               'network. The learned feature adaptation network is applied to the preserved vectors to transform them into the '
               'new feature space.'],
     'raw_file': 'src/pdf_2004.00713v2.txt',
     'agent_note': 'States N1 for stored feature vectors (not statistics): the map is learned from how new-class images move '
                   'between the old and new model.'},
    {'id': 'rrm:4', 'tag': 'N1', 'reading': 'states', 'reading_by': RB,
     'source': 'He, Fang, Xu, Cui, Li, Chen, Zeng, Zhuang, "Semantic Shift Estimation via Dual-Projection and Classifier '
               'Reconstruction for Exemplar-Free Class-Incremental Learning" (DPCR; arXiv:2503.05423; ICML 2025)',
     'version': 'v4, 18 May 2025', 'url': 'https://arxiv.org/abs/2503.05423',
     'quote': ['Inspired by LDC (Gomez-Villa et al., 2024), we introduce a linear projection',
               'The classifier is reconstructed in the form of uncentered covariance and prototypes of each class and the '
               'estimated semantic shift can be compensated into the new classifier without accessing previous data.'],
     'raw_file': 'src/pdf_2503.05423v4.txt',
     'agent_note': 'States N1: stored per-class covariance and prototype statistics are carried by a linear projection '
                   'estimated from current-task embeddings under the old and new backbone.'},
    {'id': 'rrm:5', 'tag': 'N1', 'reading': 'states', 'reading_by': RB,
     'source': 'Rypeść, Cygert, Trzciński, Twardowski, "Task-recency bias strikes back: Adapting covariances in Exemplar-Free '
               'Class Incremental Learning" (AdaGauss; arXiv:2409.18265; NeurIPS 2024)',
     'version': 'v2, 26 Oct 2024', 'url': 'https://arxiv.org/abs/2409.18265',
     'quote': ['Therefore, we update memorized Gaussians representing past classes to recover ground truth representations.',
               'which maps features from the old latent space to the new one. We use only the current data from task t for '
               'that.'],
     'raw_file': 'src/pdf_2409.18265v2.txt',
     'agent_note': 'States N1 for stored Gaussians (means and covariances), with a learned adapter fitted on current data.'},
    {'id': 'rrm:6', 'tag': 'N1', 'reading': 'states', 'reading_by': RB,
     'source': 'Peng, Koniusz, Guo, Lovell, Moghadam, "Multivariate Prototype Representation for Domain-Generalized '
               'Incremental Learning" (TRIPS; arXiv:2309.13563)',
     'version': 'v1, 24 Sep 2023', 'url': 'https://arxiv.org/abs/2309.13563',
     'quote': ['With no old exemplars stored, we use knowledge distillation and estimate old class prototype drift as '
               'incremental training advances.',
               'During the incremental step t, we pass new class samples through the old (frozen) and the current models.'],
     'raw_file': 'src/pdf_2309.13563v1.txt',
     'agent_note': 'States N1 for stored multivariate Normal prototypes; the drift is estimated from new-class samples.'},
    {'id': 'rrm:7', 'tag': 'N1', 'reading': 'states', 'reading_by': RB,
     'source': 'Xu, Krawczyk, "Geometry-Anchored Transport Framework for Exemplar-Free Class-Incremental Learning" (GATF; '
               'arXiv:2606.25347; ECCV 2026)',
     'version': 'v2, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.25347',
     'quote': ['While maintaining class-conditional Gaussian statistics provides a principled classification strategy, these '
               'parametric summaries remain sensitive to anisotropic representation drift. Existing methods often transport '
               'these statistics across tasks using a decoupled, post-hoc paradigm',
               'First, we derive an Analytic Geometric Anchor via Mahalanobis-aligned regression to mitigate macroscopic '
               'anisotropic drift.'],
     'raw_file': 'src/pdf_2606.25347v2.txt',
     'agent_note': "States N1 and calls transport of stored Gaussian statistics an existing practice. Its 'anchor' is a "
                   'closed-form regression prior, not a set of kept rows.'},
    {'id': 'rrm:8', 'tag': 'N1', 'reading': 'states', 'reading_by': RB,
     'source': 'Jang, Han, Lee, Lee, Lee, Ko, "MPT: Missing Prototype Tracking via Barycentric Reconstruction in Vehicular '
               'Federated Learning" (arXiv:2609.12771)',
     'version': 'v1, 11 Sep 2026', 'url': 'https://arxiv.org/abs/2609.12771',
     'quote': ['MPT combines a barycentric decomposition that tracks drift shared with remaining-class prototypes, a '
               'covariance-based residual prediction that estimates out-of-span drift, and an adaptive calibration that weighs '
               'the remaining rare-class samples according to their reliability.'],
     'raw_file': 'src/pdf_2609.12771v1.txt',
     'agent_note': 'States N1 in federated learning: a departed class prototype is corrected by the measured movement of '
                   'reference prototypes. See rrm:24 for its bearing on N5.'},
    {'id': 'rrm:9', 'tag': 'N1', 'reading': 'states', 'reading_by': RB,
     'source': 'He, Qiu, Meng, Zhang, Xu, Wu, Li, "Continual Learning with Vision-Language Models via Semantic-Geometry '
               'Preservation" (SeGP-CL; arXiv:2603.12055; IEEE TCSVT 2026)',
     'version': 'v3, 30 Jul 2026', 'url': 'https://arxiv.org/abs/2603.12055',
     'quote': ['In post-training stage, we estimate anchor-induced raw-space drift to transfer old visual prototypes and '
               'perform dual-path inference by fusing cross-modal and visual cues.',
               'We introduce anchor-induced prototype transfer to update old visual prototypes without storing old-task data'],
     'raw_file': 'src/pdf_2603.12055v3.txt',
     'agent_note': "States N1 with the word 'anchor': old prototypes are transferred by drift measured on anchors. The "
                   'anchors are adversarial samples built from new-task seeds each task, not kept old rows.'},
    {'id': 'rrm:10', 'tag': 'N1', 'reading': 'close', 'reading_by': RB,
     'source': 'Ramanujan, Vasu, Farhadi, Tuzel, Pouransari, "Forward Compatible Training for Large-Scale Embedding '
               'Retrieval Systems" (FCT; arXiv:2112.02805; CVPR 2022)',
     'version': 'v2, 29 Mar 2022', 'url': 'https://arxiv.org/abs/2112.02805',
     'quote': ['To develop a powerful and flexible framework for model compatibility, we combine side-information with a '
               'forward transformation from old to new embeddings.'],
     'raw_file': 'src/pdf_2112.02805v2.txt',
     'agent_note': 'Close: stored gallery embeddings are carried to a new model by a learned transformation (retrieval, not '
                   'continual classification; embeddings, not class statistics).'},
    # ------------------------------------------------------------------ N2
    {'id': 'rrm:11', 'tag': 'N2', 'reading': 'close', 'reading_by': RB,
     'source': 'Gomez-Villa et al., "Exemplar-free Continual Representation Learning via Learnable Drift Compensation" '
               '(LDC; arXiv:2407.08536; ECCV 2024)',
     'version': 'v1, 11 Jul 2024', 'url': 'https://arxiv.org/abs/2407.08536',
     'quote': ['We compare the performance of LDC against Nearest-Mean of Exemplars (NME) which directly uses exemplars for old '
               'class prototype compensation and is explored in exemplar-based methods [10,43]. While it is easy to predict '
               'the updated positions of the old prototypes using original samples of old classes by NME, it is very '
               'challenging without exemplars in our settings.',
               'Without exemplars, pf only learns the projection from current task data. Consequently, due to biases in the '
               'current data, updates to some old class prototypes may not be perfect.'],
     'raw_file': 'src/pdf_2407.08536v1.txt',
     'agent_note': 'Close: using kept old-class exemplars to place old prototypes (NME) is named as standard, and current-data '
                   'estimation is named as biased. NME recomputes the mean of the kept rows; it does not estimate a drift '
                   'from them and apply it to a stored statistic of the rest of the class.'},
    {'id': 'rrm:12', 'tag': 'N2', 'reading': 'close', 'reading_by': RB,
     'source': 'Rebuffi, Kolesnikov, Sperl, Lampert, "iCaRL: Incremental Classifier and Representation Learning" '
               '(arXiv:1611.07725; CVPR 2017)',
     'version': 'v2, 14 Apr 2017', 'url': 'https://arxiv.org/abs/1611.07725',
     'quote': ['In the classincremental setting, we cannot make use of the true class mean, since all training data would have '
               'to be stored in order to recompute this quantity after a representation change. Instead, we use the average '
               'over a flexible number of exemplars'],
     'raw_file': 'src/pdf_1611.07725v2.txt',
     'agent_note': 'Close: the kept exemplars give the class mean under the current representation (recomputation, not a '
                   'transported stored statistic).'},
    {'id': 'rrm:13', 'tag': 'N2', 'reading': 'close', 'reading_by': RB,
     'source': 'De Lange, Tuytelaars, "Continual Prototype Evolution: Learning Online from Non-Stationary Data Streams" '
               '(CoPE; arXiv:2009.00919; ICCV 2021)',
     'version': 'v4, 6 Apr 2021', 'url': 'https://arxiv.org/abs/2009.00919',
     'quote': ['The main crux with storing representations is to prevent them from becoming obsolete as the embedding network '
               'evolves.',
               'Consequently, before using the evaluator they exhaustively recalculate the prototypes based on all exemplars '
               'in memory.'],
     'raw_file': 'src/pdf_2009.00919v4.txt',
     'agent_note': 'Close: stored representations go stale as the network evolves; the cited remedy recomputes prototypes '
                   'from the exemplar memory (CoPE itself updates prototypes online from batches that include replay).'},
    {'id': 'rrm:14', 'tag': 'N2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Goswami et al., "Resurrecting Old Classes with New Data for Exemplar-Free Continual Learning" (ADC; '
               'arXiv:2405.19074; CVPR 2024)',
     'version': 'v1, 29 May 2024', 'url': 'https://arxiv.org/abs/2405.19074',
     'quote': ['Now, the drift from old to new feature space is estimated using these adversarial samples, which serve as '
               'pseudo-exemplars for the old classes. We hypothesize that the pseudo-exemplars behave like the original '
               'exemplars in the feature space, and thus we exploit them to measure the drift.'],
     'raw_file': 'src/pdf_2405.19074v1.txt',
     'agent_note': 'Bears: drift measured on points placed at the old classes, but generated from current data, not kept.'},
    {'id': 'rrm:15', 'tag': 'N2', 'reading': 'bears', 'reading_by': RB,
     'source': 'Chaudhry, Gordo, Dokania, Torr, Lopez-Paz, "Using Hindsight to Anchor Past Knowledge in Continual Learning" '
               '(HAL; arXiv:2002.08165; AAAI 2021)',
     'version': 'v2, 2 Mar 2021', 'url': 'https://arxiv.org/abs/2002.08165',
     'quote': ['In this work, we complement experience replay with a new objective that we call “anchoring”, where the learner '
               'uses bilevel optimization to update its knowledge on the current task, while keeping intact predictions on '
               'some anchor points of past tasks.'],
     'raw_file': 'src/pdf_2002.08165v2.txt',
     'agent_note': 'Bears: kept anchor points of past tasks in continual learning, used to hold predictions fixed, not to '
                   'estimate drift or transport stored statistics.'},
    # ------------------------------------------------------------------ N3
    {'id': 'rrm:16', 'tag': 'N3', 'reading': 'states', 'reading_by': RB,
     'source': 'Moschella, Maiorca, Fumero, Norelli, Locatello, Rodolà, "Relative representations enable zero-shot latent '
               'space communication" (arXiv:2209.15430; ICLR 2023)',
     'version': 'v2, 7 Mar 2023', 'url': 'https://arxiv.org/abs/2209.15430',
     'quote': ['In this work, we propose the latent similarity between each sample and a fixed set of anchors as an alternative '
               'data representation, demonstrating that it can enforce the desired invariances without any additional '
               'training.',
               'Importantly, cos θ does not change if we apply the same angle-preserving transformation T to two vectors a and '
               'b, i.e., the cosine similarity is invariant to rotations, reflections, and rescaling. While this is not true '
               'for translations, NNs commonly employ normalization techniques'],
     'raw_file': 'src/pdf_2209.15430v2.txt',
     'agent_note': 'States N3 exactly (cosine to anchors; invariance to angle-preserving maps; translations excepted). Across '
                   'independently trained models, not across the training of one continual learner.'},
    {'id': 'rrm:17', 'tag': 'N3', 'reading': 'states', 'reading_by': RB,
     'source': 'Maiorca, Moschella, Fumero, Locatello, Rodolà, "Latent Space Translation via Inverse Relative Projection" '
               '(IRP; arXiv:2406.15057)',
     'version': 'v1, 21 Jun 2024', 'url': 'https://arxiv.org/abs/2406.15057',
     'quote': ['By formalizing the invertibility of angle-preserving relative representations and assuming the scale '
               'invariance of decoder modules in neural models, we can effectively use the relative space as an intermediary, '
               'independently projecting onto and from other semantically similar spaces.'],
     'raw_file': 'src/pdf_2406.15057v1.txt',
     'agent_note': 'States N3 (angle-preserving relative representations) and adds their invertibility.'},
    # ------------------------------------------------------------------ N4
    {'id': 'rrm:18', 'tag': 'N4', 'reading': 'states', 'reading_by': RB,
     'source': 'Cha, Lee, Shin, "Co2L: Contrastive Continual Learning" (arXiv:2106.14413)',
     'version': 'v1, 28 Jun 2021', 'url': 'https://arxiv.org/abs/2106.14413',
     'quote': ['We propose a novel preservation mechanism for contrastively learned representations, which works by '
               'self-distillation of instance-wise relations (Section 4.2)',
               'In the ablation of distillation, we empirically show that distillation preserves learned representations and '
               'efficiently uses buffered samples'],
     'raw_file': 'src/pdf_2106.14413v1.txt',
     'agent_note': 'States N4: instance-wise relation distillation preserves representations in continual learning.'},
    {'id': 'rrm:19', 'tag': 'N4', 'reading': 'states', 'reading_by': RB,
     'source': 'Gao, Zhao, Ghanem, Zhang, "R-DFCIL: Relation-Guided Representation Learning for Data-Free Class Incremental '
               'Learning" (arXiv:2203.13104; ECCV 2022)',
     'version': 'v2, 21 Jul 2022', 'url': 'https://arxiv.org/abs/2203.13104',
     'quote': ['In RRL, we introduce relational knowledge distillation to flexibly transfer the structural relation of new data '
               'from the old model to the current model.'],
     'raw_file': 'src/pdf_2203.13104v2.txt',
     'agent_note': 'States N4 for data-free class-IL.'},
    {'id': 'rrm:20', 'tag': 'N4', 'reading': 'states', 'reading_by': RB,
     'source': 'Asadi, Davari, Mudur, Aljundi, Belilovsky, "Prototype-Sample Relation Distillation: Towards Replay-Free '
               'Continual Learning" (PRD; arXiv:2303.14771; ICML 2023)',
     'version': 'v2, 6 Jun 2023', 'url': 'https://arxiv.org/abs/2303.14771',
     'quote': ['To continually adapt the prototypes without keeping any prior task data, we propose a novel distillation loss '
               'that constrains class prototypes to maintain relative similarities as compared to new task data.',
               'For each prior task prototype, we preserve the relative ordering of samples in the mini-batch.'],
     'raw_file': 'src/pdf_2303.14771v2.txt',
     'agent_note': 'States N4. Also bears on N5: an old prototype is kept current through its relations to current samples '
                   '(a relational constraint during training, not a stored relation used to rebuild content).'},
    {'id': 'rrm:21', 'tag': 'N4', 'reading': 'close', 'reading_by': RB,
     'source': 'Park, Kim, Lu, Cho, "Relational Knowledge Distillation" (RKD; arXiv:1904.05068; CVPR 2019)',
     'version': 'v2, 1 May 2019', 'url': 'https://arxiv.org/abs/1904.05068',
     'quote': ['We introduce a novel approach, dubbed relational knowledge distillation (RKD), that transfers mutual relations '
               'of data examples instead.',
               'The central tenet of our work is that what constitutes the knowledge is better presented by relations of the '
               'learned representations than individuals of those'],
     'raw_file': 'src/pdf_1904.05068v2.txt',
     'agent_note': 'Close: relational distillation, teacher to student; not about forgetting. It motivates relations by '
                   "Saussure's relational identity of signs, the nearest published framing to the owner's reading."},
    {'id': 'rrm:22', 'tag': 'N4', 'reading': 'close', 'reading_by': RB,
     'source': 'Douillard, Cord, Ollion, Robert, Valle, "PODNet: Pooled Outputs Distillation for Small-Tasks Incremental '
               'Learning" (arXiv:2004.13513; ECCV 2020)',
     'version': 'v3, 6 Oct 2020', 'url': 'https://arxiv.org/abs/2004.13513',
     'quote': ['fights catastrophic forgetting, remaining stable over long runs of small incremental tasks. Our model innovates '
               'on existing art with (1) an efficient spatial-based distillation-loss applied throughout the model'],
     'raw_file': 'src/pdf_2004.13513v3.txt',
     'agent_note': 'Close: distillation reduces forgetting, but of pooled per-sample activation statistics, not relations '
                   'between samples.'},
    # ------------------------------------------------------------------ N5
    {'id': 'rrm:23', 'tag': 'N5', 'reading': 'close', 'reading_by': RB,
     'source': 'Xu, Krawczyk, "Geometry-Anchored Transport Framework for Exemplar-Free Class-Incremental Learning" (GATF; '
               'arXiv:2606.25347; ECCV 2026)',
     'version': 'v2, 25 Jun 2026', 'url': 'https://arxiv.org/abs/2606.25347',
     'quote': ['After completing task t−1, we freeze the previous backbone ft−1 and train a new backbone ft using only the '
               'current-task dataset Dt.',
               'We estimate this linear relationship using paired current-task features',
               'we formulate the estimation of Pt, bt as a ridge-regularized Generalized Least Squares'],
     'raw_file': 'src/pdf_2606.25347v2.txt',
     'agent_note': 'Close, the nearest transport operation: stored class Gaussians carried by a ridge-regularised linear map '
                   'from old to new features. The pairs are current-task features, not kept anchors, and nothing is stored '
                   'in anchor-relative coordinates.'},
    {'id': 'rrm:24', 'tag': 'N5', 'reading': 'close', 'reading_by': RB,
     'source': 'Jang et al., "MPT: Missing Prototype Tracking via Barycentric Reconstruction in Vehicular Federated '
               'Learning" (arXiv:2609.12771)',
     'version': 'v1, 11 Sep 2026', 'url': 'https://arxiv.org/abs/2609.12771',
     'quote': ['The key idea is to decompose the rare-class prototype into two parts. The first is an in-span component, '
               'expressed by its barycentric relationship to the remaining-class prototypes. The second is an out-of-span '
               'component, captured by a residual that cannot be spanned by remaining classes. After each FL round, remaining '
               'vehicles re-embed local data using the updated backbone and report class-level prototypes and covariances.',
               'tracking shared drift through its departure-time barycentric relationship'],
     'raw_file': 'src/pdf_2609.12771v1.txt',
     'agent_note': "Close, the nearest published form of the owner's reading: content stored as a relation to references at "
                   'its cut, rebuilt from the references as seen now, with the same in-span / out-of-span split. Differs: '
                   'references are other classes\' prototypes re-embedded from live data (not kept raw anchors), the content '
                   'is one mean (the residual is adapted, not carried stale), federated rather than class-incremental.'},
    {'id': 'rrm:25', 'tag': 'N5', 'reading': 'close', 'reading_by': RB,
     'source': 'Iscen, Zhang, Lazebnik, Schmid, "Memory-Efficient Incremental Learning Through Feature Adaptation" (MEA; '
               'arXiv:2004.00713)',
     'version': 'v2, 24 Aug 2020', 'url': 'https://arxiv.org/abs/2004.00713',
     'quote': ['requires adapting the previously stored feature vectors to the updated feature space without having access to '
               'the corresponding original training images.',
               'Features are extracted using the old and new models from new class images to train a feature adaptation '
               'network.'],
     'raw_file': 'src/pdf_2004.00713v2.txt',
     'agent_note': 'Close: stored old-class features transported into the new space and replayed to the classifier; the map '
                   'is an MLP fitted on new-class images, not on kept anchors.'},
    {'id': 'rrm:26', 'tag': 'N5', 'reading': 'close', 'reading_by': RB,
     'source': 'Rypeść et al., "Task-recency bias strikes back: Adapting covariances in Exemplar-Free Class Incremental '
               'Learning" (AdaGauss; arXiv:2409.18265; NeurIPS 2024)',
     'version': 'v2, 26 Oct 2024', 'url': 'https://arxiv.org/abs/2409.18265',
     'quote': ['we train an auxiliary network (adapter), which we utilize to adapt the means and covariances of old classes to '
               'the latent space of the new feature extractor.'],
     'raw_file': 'src/pdf_2409.18265v2.txt',
     'agent_note': 'Close: stored class Gaussians transported by a learned map fitted on current data.'},
    {'id': 'rrm:27', 'tag': 'N5', 'reading': 'close', 'reading_by': RB,
     'source': 'Peng et al., "Multivariate Prototype Representation for Domain-Generalized Incremental Learning" (TRIPS; '
               'arXiv:2309.13563)',
     'version': 'v1, 24 Sep 2023', 'url': 'https://arxiv.org/abs/2309.13563',
     'quote': ['Our prototype representations are based on multivariate Normal distributions whose means and covariances are '
               'constantly adapted to changing model features to represent old classes well by adapting to the feature space '
               'drift. For old classes, we sample pseudo-features from the adapted Normal distributions with the help of '
               'Cholesky decomposition.'],
     'raw_file': 'src/pdf_2309.13563v1.txt',
     'agent_note': "Close: RRM's replay half (stored Gaussians, adapted to drift, sampled as pseudo-features); the drift is "
                   'estimated from new-class samples, with no kept anchors and no relative coordinates.'},
    {'id': 'rrm:28', 'tag': 'N5', 'reading': 'close', 'reading_by': RB,
     'source': 'Gomez-Villa et al., "Exemplar-free Continual Representation Learning via Learnable Drift Compensation" '
               '(LDC; arXiv:2407.08536; ECCV 2024)',
     'version': 'v1, 11 Jul 2024', 'url': 'https://arxiv.org/abs/2407.08536',
     'quote': ['In Table 6, instead of projecting a prototype per class, we project N stored features and use them to compute '
               'the class prototype at the classification stage. The results show that storing and projecting features do '
               'not present a significant advantage over projecting the class means.'],
     'raw_file': 'src/pdf_2407.08536v1.txt',
     'agent_note': 'Close: stored old-class features transported by a linear map (fitted on current data); reports no gain '
                   'over transporting the mean.'},
    {'id': 'rrm:29', 'tag': 'N5', 'reading': 'close', 'reading_by': RB,
     'source': 'Maiorca, Moschella, Norelli, Fumero, Locatello, Rodolà, "Latent Space Translation via Semantic Alignment" '
               '(arXiv:2311.00664; NeurIPS 2023)',
     'version': 'v2, 11 Feb 2024', 'url': 'https://arxiv.org/abs/2311.00664',
     'quote': ['Parallel anchors act as a "Rosetta stone" [Norelli et al., 2023], meaning they establish a semantic '
               'correspondence between their respective spaces',
               'The transformation T , derived solely from the subset of corresponding points, provides a robust and '
               'versatile foundation for model reuse and interoperability in diverse machine learning contexts.'],
     'raw_file': 'src/pdf_2311.00664v2.txt',
     'agent_note': "Close: RRM's transport step (a linear or affine map between two latent spaces fitted on a few paired "
                   'anchors, then applied to other points), across models rather than across one learner\'s training, and '
                   'applied to live encodings rather than stored class distributions.'},
    {'id': 'rrm:30', 'tag': 'N5', 'reading': 'close', 'reading_by': RB,
     'source': 'Maiorca et al., "Latent Space Translation via Inverse Relative Projection" (IRP; arXiv:2406.15057)',
     'version': 'v1, 21 Jun 2024', 'url': 'https://arxiv.org/abs/2406.15057',
     'quote': ['the inverse transformation method estimates the rescaling, rotation, and reflection separately, allowing us to '
               'reconstruct the absolute latent spaces from the relative representations.'],
     'raw_file': 'src/pdf_2406.15057v1.txt',
     'agent_note': 'Close: content held in anchor-relative coordinates and rebuilt as absolute coordinates in another space '
                   'from the anchors; cross-model, no stored class distributions, no continual learning.'},
    {'id': 'rrm:31', 'tag': 'N5', 'reading': 'bears', 'reading_by': RB,
     'source': 'Ramanujan et al., "Forward Compatible Training for Large-Scale Embedding Retrieval Systems" (FCT; '
               'arXiv:2112.02805; CVPR 2022)',
     'version': 'v2, 29 Mar 2022', 'url': 'https://arxiv.org/abs/2112.02805',
     'quote': ['If we are able to find a perfect transformation, the compatibility problem is solved because we can convert old '
               'to new embeddings without requiring access to the original images (no-backfilling). However, φold possibly '
               'discards information about the image that φnew does not.'],
     'raw_file': 'src/pdf_2112.02805v2.txt',
     'agent_note': "Bears: the limit of any transport of stored features (the declaration's 'outside the span, carried "
                   "stale'), stated for embedding upgrades."},
    # ------------------------------------------------------------------ N6
    {'id': 'rrm:32', 'tag': 'N6', 'reading': 'states', 'reading_by': RB,
     'source': 'Parisi, Kemker, Part, Kanan, Wermter, "Continual Lifelong Learning with Neural Networks: A Review" '
               '(arXiv:1802.07569; Neural Networks 2019)',
     'version': 'v4, 11 Feb 2019', 'url': 'https://arxiv.org/abs/1802.07569',
     'quote': ['we review computational approaches motivated by biological aspects of learning which include critical '
               'developmental stages and curriculum learning (Sec. 4.2)',
               'In particular, we discuss on how these components (see Fig. 5) can be used (independently or combined) to '
               'improve current approaches addressing lifelong learning.',
               'In a first organization phase, the neural map is trained with a high learning rate and large spatial '
               'neighbourhood size, allowing the network to reach an initial rough topological organization.',
               'However, the use of developmental strategies for artificial learning systems has shown to be a very complex '
               'practice.'],
     'raw_file': 'src/pdf_1802.07569v4.txt',
     'agent_note': 'States N6 for the developmental framing (critical periods, staged development, rough-then-fine '
                   'organisation) as a design source for lifelong learners. The object-relations framing (a first '
                   'reference object) was not found anywhere in the sweep.'},
    {'id': 'rrm:33', 'tag': 'N6', 'reading': 'states', 'reading_by': RB,
     'source': 'Erden, Faltings, "Foundations of a Developmental Design Paradigm for Integrated Continual Learning, '
               'Deliberative Behavior, and Comprehensibility" (arXiv:2502.13935; IEEE TETCI)',
     'version': 'v2, 18 Oct 2025', 'url': 'https://arxiv.org/abs/2502.13935',
     'quote': ['we introduce a system design, fueled by a novel learning approach conceptually grounded in principles of '
               'evolutionary developmental biology, that overcomes key limitations of current methods.'],
     'raw_file': 'src/pdf_2502.13935v2.txt',
     'agent_note': "States N6 for 'developmental' in the evolutionary-developmental-biology sense: a continual learner "
                   'designed from developmental principles. Not a psychological (infant) framing.'},
    {'id': 'rrm:34', 'tag': 'N6', 'reading': 'close', 'reading_by': RB,
     'source': 'Chen, Pitti, Quoy, Chen, "Developmental Predictive Coding Model for Early Infancy Mono and Bilingual Vocal '
               'Continual Learning" (arXiv:2412.17456; ICANN 2024)',
     'version': 'v1, 23 Dec 2024', 'url': 'https://arxiv.org/abs/2412.17456',
     'quote': ['we propose a novel approach using a small-sized generative neural network equipped with a continual learning '
               'mechanism based on predictive coding for mono- and bilingual speech sound learning (referred to as language '
               'sound acquisition during ”critical period”)'],
     'raw_file': 'src/pdf_2412.17456v1.txt',
     'agent_note': 'Close: an infant-development framing and a continual learner in one model, but the model is built to '
                   'reproduce infant phenomena, not designed from the framing to reduce forgetting.'},
    {'id': 'rrm:35', 'tag': 'N6', 'reading': 'close', 'reading_by': RB,
     'source': 'Cai, Lin, Nunna, Zhang, "Learning to See Through a Baby\'s Eyes: Early Visual Diets Enable Robust Visual '
               'Intelligence in Humans and Machines" (CATDiet; arXiv:2511.14440)',
     'version': 'v2, 24 Mar 2026', 'url': 'https://arxiv.org/abs/2511.14440',
     'quote': ['We introduce CATDiet, a developmentally inspired visual diet in SSL that emulates the progression of infant '
               'vision through 3 staged constraints: grayscale-to-color (C), blur-to-sharp (A), and preserved temporal '
               'continuity (T).'],
     'raw_file': 'src/pdf_2511.14440v2.txt',
     'agent_note': 'Close: increasing resolution (blur to sharp) taken from infant development to design training; the '
                   'learner is not a continual learner.'},
    {'id': 'rrm:36', 'tag': 'N6', 'reading': 'bears', 'reading_by': RB,
     'source': 'Xiang, Tan, Wan, Ma, "Coarse-To-Fine Incremental Few-Shot Learning" (arXiv:2111.14806)',
     'version': 'v1, 24 Nov 2021', 'url': 'https://arxiv.org/abs/2111.14806',
     'quote': ['to learn, normalize, and freeze a classifier’s weights from fine labels, once learning an embedding space '
               'contrastively from coarse labels.'],
     'raw_file': 'src/pdf_2111.14806v1.txt',
     'agent_note': 'Bears: coarse-to-fine resolution of the label space in class-IL, with no developmental framing.'},
]
