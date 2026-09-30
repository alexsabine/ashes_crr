"""Claims for Relational_Reference_Memory/DECLARATION_2.md Part W, family F3 (positions P4 and P6), transcribed from the
dossier docs/citations/rrm2_f3_2026-09-30.md (fetched 2026-09-30; extracted texts held outside the repository under
/tmp/claude-0/rrm2_src/, named in `raw_file` relative to that root). Every quote is copied from a dossier blockquote.

'reading' is decided by the grading agent from the quote, for the investigator's review ('reading_by'). Reading policy
(RQM's, unchanged), fixed before the readings were written and applied to every position:
  states       the source asserts (or reports as its own result) every predicate of the position, for at least one of the
               objects the position names, within the position's scope;
  close        the source asserts part of the position, or the position in a narrower or different scope;
  bears        relevant evidence or a bound that neither asserts nor negates the position;
  contradicts  the source asserts or reports the negation of the position within its scope. For an existential position
               ('is published', 'is named') the negation is 'not'; a failure in a sub-regime the position does not
               claim is a bound ('bears').
P4 is read against its full predicate: an anchor-relative or relative representation (or an anchor-fitted latent alignment /
stitching map) used INSIDE ONE continual learner to keep its old representations usable across its OWN updates. Alignment
between two separately trained models, relational constraints without anchors, learned maps without anchors, or a frozen
backbone whose old features never drift, is 'close'.
P6 is read against both parts: an on-device or privacy-constrained continual-learning setting in which (a) a small store of
raw rows is kept or named acceptable and (b) a full (large) replay buffer is named infeasible or unacceptable; or a design
for a small raw buffer because a full one is infeasible. A source with only (a) or only (b), or whose small store is not raw
rows (latent codes, prototypes), is 'close'. A source arguing that large raw replay buffers are cheap or acceptable on device
is 'contradicts'.
"""

RB = "grading agent; for the investigator's review"

CLAIMS = [
    # ------------------------------------------------------------------ P4
    {'id': 'w3:0', 'tag': 'P4', 'reading': 'states', 'reading_by': RB,
     'source': 'Ranganathan, Dalal, Banerjee, "Continual Anchored Manifold Embeddings for Learning Stability (CAMELS)" '
               '(OpenReview bqievBMLYE; CoLLAs 2025 Workshop Track)',
     'version': 'OpenReview note, created 23 May 2025, modified 3 Aug 2025 (abstract only; PDF NOT REACHED, HTTP 403)',
     'url': 'https://openreview.net/forum?id=bqievBMLYE',
     'quote': ['Rather than constraining parameters or matching global prototypes, CAMELS anchors the internal structure of '
               'past tasks by preserving pairwise cosine similarities among replay samples—maintaining relative geometry '
               'without freezing coordinates and embeds different tasks in orthogonal subspaces.',
               'This formulation treats continual learning as the problem of preserving local isometries across evolving '
               'latent manifolds in high-dimensional embedding spaces.'],
     'raw_file': 'f3/src/or_bqievBMLYE_abstract.txt',
     'agent_note': 'States P4 from the abstract alone: relative geometry (pairwise cosine similarities among kept replay '
                   'samples, which act as anchors) is preserved inside one continual learner across its own updates. '
                   'Graded from the abstract served by the OpenReview API; the full text was not reached (workshop paper).'},
    {'id': 'w3:1', 'tag': 'P4', 'reading': 'states', 'reading_by': RB,
     'source': 'Chaudhury, "Forgetting is Not Erasure: Recovering Latent Knowledge via Transport Keys" (arXiv:2606.02860; '
               'technical report)',
     'version': 'v1, 1 Jun 2026', 'url': 'https://arxiv.org/abs/2606.02860',
     'quote': ['We describe transport keys at a systems level as compact interface-alignment operators estimated from a small '
               'set of paired anchor activations and evaluated through model stitching.',
               'To estimate a key, we use a small anchor set drawn from Task A. Anchors are ordinary examples from the earlier '
               'task and are passed through both checkpoints.'],
     'raw_file': 'f3/src/pdf_2606.02860v1.txt',
     'agent_note': "States P4: an alignment map fitted on a few kept old-task anchors, seen by the learner before and after "
                   'its own update, restores the use of old latent computation (stitching inside one continual learner). '
                   "It keeps the predecessor's late stages; it does not transport stored class statistics. Single-author "
                   'technical report.'},
    {'id': 'w3:2', 'tag': 'P4', 'reading': 'close', 'reading_by': RB,
     'source': 'Geng, Zhou, Zhou, "Language as an Anchor: Preserving Relative Visual Geometry for Domain Incremental '
               'Learning" (LAVA; arXiv:2511.14401)',
     'version': 'v1, 18 Nov 2025', 'url': 'https://arxiv.org/abs/2511.14401',
     'quote': ['we propose LAVA (Language-Anchored Visual Alignment), a novel DIL framework that replaces direct feature '
               'alignment with relative alignment driven by a text-based reference anchor. LAVA guides the visual '
               'representations of each incoming domain to preserve a consistent relative geometry, which is defined by '
               'mirroring the pairwise semantic similarities between the class names.',
               'Once the Visual Anchors are structurally aligned with the Text-based Anchor, the resulting visual geometry '
               'space becomes comparable across domains. We exploit this relative representation to facilitate effective '
               'class-wise aggregation of cross-domain features.',
               'we keep the visual encoder fθ frozen and maintain a pool of prompts'],
     'raw_file': 'f3/src/pdf_2511.14401v1.txt',
     'agent_note': 'Close: relative representations (cosine similarities to anchors, after Moschella et al.) inside one '
                   'domain-incremental learner, to keep the domains comparable. The backbone is frozen, so the anchors keep '
                   "domains consistent with each other rather than keeping old features valid across the learner's own "
                   'weight updates. Read states if P4 is read as "relative representations used inside a continual learner".'},
    {'id': 'w3:3', 'tag': 'P4', 'reading': 'close', 'reading_by': RB,
     'source': 'Cui, Zhou, Peng, "Bi-C2R: Bidirectional Continual Compatible Representation for Re-indexing Free Lifelong '
               'Person Re-identification" (arXiv:2512.25000; IEEE TPAMI header)',
     'version': 'v1, 31 Dec 2025', 'url': 'https://arxiv.org/abs/2512.25000',
     'quote': ['a bidirectional compatible transfer network is first designed to bridge the relationship between new and old '
               'knowledge and continuously update the old gallery features to the new feature space after the updating.',
               'However, historical gallery data typically suffers from direct saving due to the data privacy issue and the '
               'high re-indexing costs for large-scale gallery images.'],
     'raw_file': 'f3/src/pdf_2512.25000v1.txt',
     'agent_note': "Close: inside one lifelong learner, stored old features are carried into the new feature space after "
                   'each update (latent alignment), but by a learned transfer network, not by anchors or relative '
                   'coordinates.'},
    {'id': 'w3:4', 'tag': 'P4', 'reading': 'close', 'reading_by': RB,
     'source': 'Nguyen, Nguyen, Li, Pham, Nguyen, Doan, "Retrospective Feature Estimation for Continual Learning" (RFE, '
               'first titled "Forget but Recall: Incremental Latent Rectification"; arXiv:2406.17381; TMLR 2026)',
     'version': 'v2, 1 Feb 2026', 'url': 'https://arxiv.org/abs/2406.17381',
     'quote': ['RFE learns to reverse feature changes by aligning the features from the current trained DNN backward to the '
               'feature space of the old task, where performing predictions is easier.'],
     'raw_file': 'f3/src/pdf_2406.17381v2.txt',
     'agent_note': 'Close: latent alignment across the learner\'s own updates (current features mapped back to the old '
                   'space by learned retrospector modules); no anchors, no relative representation.'},
    {'id': 'w3:5', 'tag': 'P4', 'reading': 'close', 'reading_by': RB,
     'source': 'Cignoni, Cossu, Gomez-Villa, van de Weijer, Carta, "CLA: Latent Alignment for Online Continual Self-Supervised '
               'Learning" (arXiv:2507.10434; CoLLAs 2025)',
     'version': 'v2, 15 Jul 2025', 'url': 'https://arxiv.org/abs/2507.10434',
     'quote': ['We introduce Continual Latent Alignment (CLA), a novel SSL strategy for Online CL that aligns the '
               'representations learned by the current model with past representations to mitigate forgetting.',
               'CLA-R, stores past network output features in the memory buffer in pair with the original samples.'],
     'raw_file': 'f3/src/pdf_2507.10434v2.txt',
     'agent_note': 'Close: current representations are aligned to stored past representations of kept samples inside one '
                   'learner; an absolute (predictor-mapped) alignment used as a regulariser, not a relative representation.'},
    {'id': 'w3:6', 'tag': 'P4', 'reading': 'close', 'reading_by': RB,
     'source': 'Li, Xiao, Jiang, Zuo, Zhang, Yang, "A Stitch in Time Saves Nine: Preserving Policy Compatibility Under '
               'Perception Updates in End-to-End Autonomous Driving" (arXiv:2606.21509; T-ITS under review)',
     'version': 'v1, 19 Jun 2026', 'url': 'https://arxiv.org/abs/2606.21509',
     'quote': ['we formulate the model stitching problem for end-to-end autonomous driving and test the hypothesis that policy '
               'compatibility can be preserved through lightweight latent-space alignment.',
               'are estimated from the paired anchors [30].'],
     'raw_file': 'f3/src/pdf_2606.21509v1.txt',
     'agent_note': "Close: an anchor-fitted linear stitcher keeps a frozen downstream module valid after one system's "
                   'perception module is updated; the update is a retraining, not a continual learner\'s stream.'},
    {'id': 'w3:7', 'tag': 'P4', 'reading': 'bears', 'reading_by': RB,
     'source': 'Si, Qin, "Continual-learning rules shape representational drift" (arXiv:2608.16141)',
     'version': 'v2, 1 Sep 2026', 'url': 'https://arxiv.org/abs/2608.16141',
     'quote': ['Directly anchoring an old representation during replay likewise suppressed drift and impaired acquisition of '
               'subsequent tasks.'],
     'raw_file': 'f3/src/pdf_2608.16141v2.txt',
     'agent_note': 'Bears: anchoring old representations (absolute, not relative) inside a learner holds them valid at a '
                   'plasticity cost; a bound on the P4 route, not an instance of it.'},
    # ------------------------------------------------------------------ P6
    {'id': 'w3:8', 'tag': 'P6', 'reading': 'states', 'reading_by': RB,
     'source': 'Dong, Wang, Fang, Sun, Xu, Wang, Zhu, "Federated Class-Incremental Learning" (GLFC; arXiv:2203.11473; CVPR 2022)',
     'version': 'v1, 22 Mar 2022', 'url': 'https://arxiv.org/abs/2203.11473',
     'quote': ['where local clients often collect new classes continuously and have very limited storage memory to store old '
               'classes.',
               'FCIL requires these local clients to collaboratively train a global model to learn new classes continuously, '
               'with constraints on privacy preservation and limited memory storage'],
     'raw_file': 'f3/src/pdf_2203.11473v1.txt',
     'agent_note': 'States P6 for the federated (privacy-constrained) setting: clients keep a small exemplar memory of raw '
                   'old-class rows (|M| per class, far below the task data) because storage is very limited.'},
    {'id': 'w3:9', 'tag': 'P6', 'reading': 'states', 'reading_by': RB,
     'source': 'Wang, Xiang, Du, "FeDMRA: Federated Incremental Learning with Dynamic Memory Replay Allocation" (arXiv:2603.28455)',
     'version': 'v1, 30 Mar 2026', 'url': 'https://arxiv.org/abs/2603.28455',
     'quote': ['Unlike the fixed allocation of client exemplar memory, the proposed scheme emphasizes the rational allocation of '
               'limited storage resources among clients to improve model performance.'],
     'raw_file': 'f3/src/pdf_2603.28455v1.txt',
     'agent_note': 'States P6 for federated healthcare (privacy-preserving): a limited raw exemplar memory at each client is '
                   'the design, because storage is limited.'},
    {'id': 'w3:10', 'tag': 'P6', 'reading': 'close', 'reading_by': RB,
     'source': 'Kwon, Chauhan, Kumar, Hui, Mascolo, "Exploring System Performance of Continual Learning for Mobile and Embedded '
               'Sensing Applications" (arXiv:2110.13290; SEC 2021)',
     'version': 'v2, 23 Jun 2022', 'url': 'https://arxiv.org/abs/2110.13290',
     'quote': ['This is an interesting finding, making iCaRL a good candidate to perform IL on many embedded devices and '
               'smartphones with reasonable storage as only a few samples are required to be stored.',
               'As many modern computing platforms including smartphones and embedded devices have large storage capacity, '
               'the issue of storing a proportion of training samples can be minor.'],
     'raw_file': 'f3/src/pdf_2110.13290v2.txt',
     'agent_note': 'Close: states part (a) on device (a few stored raw samples are acceptable and work best); does not name '
                   'a full buffer as infeasible, and calls storing a proportion of the samples a minor issue.'},
    {'id': 'w3:11', 'tag': 'P6', 'reading': 'close', 'reading_by': RB,
     'source': 'Hayes, Kanan, "Online Continual Learning for Embedded Devices" (arXiv:2203.10681; CoLLAs 2022)',
     'version': 'v3, 15 Jul 2022', 'url': 'https://arxiv.org/abs/2203.10681',
     'quote': ['embedded devices have limited memory and compute capacity',
               'While effective, replay can be memory intensive due to the storage of its memory buffer.'],
     'raw_file': 'f3/src/pdf_2203.10681v3.txt',
     'agent_note': 'Close: names the memory cost of a replay buffer on embedded devices; does not name a small raw store as '
                   'the acceptable middle.'},
    {'id': 'w3:12', 'tag': 'P6', 'reading': 'close', 'reading_by': RB,
     'source': 'Verwimp, Aljundi, Ben-David, Bethge, Cossu, Gepperth, Hayes, Hüllermeier, Kanan, Kudithipudi, Lampert, Mundt, Pascanu, Popescu, Tolias, van de Weijer, Liu, Lomonaco, Tuytelaars, van de Ven, "Continual Learning: Applications and the Road '
               'Forward" (arXiv:2311.11908; TMLR 2024)',
     'version': 'v3, 28 Mar 2024', 'url': 'https://arxiv.org/abs/2311.11908',
     'quote': ['Yet sometimes this is not the case, because training happens on a more restricted (e.g. personal) device, then '
               'memory does become a constraint',
               'These tight constraints often make storing all user data and retraining from scratch infeasible, '
               'necessitating continual learning'],
     'raw_file': 'f3/src/pdf_2311.11908v3.txt',
     'agent_note': 'Close: on device, storing all data is infeasible (part b); a small raw store is not named as the '
                   'acceptable alternative.'},
    {'id': 'w3:13', 'tag': 'P6', 'reading': 'bears', 'reading_by': RB,
     'source': 'Verwimp et al., "Continual Learning: Applications and the Road Forward" (arXiv:2311.11908; TMLR 2024)',
     'version': 'v3, 28 Mar 2024', 'url': 'https://arxiv.org/abs/2311.11908',
     'quote': ['Two popular reasons for arguing a low storage solution are the cost of memory and privacy concerns, but these '
               'arguments are often not relevant in practice.'],
     'raw_file': 'f3/src/pdf_2311.11908v3.txt',
     'agent_note': 'Bears: off device, the storage-cost and privacy arguments for small memories are disputed (deleting data '
                   'does not remove it from derived models); the same paper excepts restricted devices (w3:12).'},
    {'id': 'w3:14', 'tag': 'P6', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Lee, Weerakoon, Choi, Zhang, Wang, Jeon, "Carousel Memory: Rethinking the Design of Episodic Memory for Continual Learning" '
               '(CarM; arXiv:2110.07276; extended version of DAC 2022)',
     'version': 'v3, 29 Dec 2022', 'url': 'https://arxiv.org/abs/2110.07276',
     'quote': ['In particular, in mobile and IoT devices, real-time data can be stored not just in high-speed RAMs but in '
               'internal storage devices as well, which offer significantly larger capacity than the RAMs. Based on this '
               'insight, we propose to exploit the abundant storage to preserve past experiences'],
     'raw_file': 'f3/src/pdf_2110.07276v3.txt',
     'agent_note': 'Contradicts part (b) on device: a large raw episodic memory is kept in device storage and swapped into '
                   'RAM; the RAM-bounded buffer is the limit it removes.'},
    {'id': 'w3:15', 'tag': 'P6', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Ma, Jeong, Zhang, Wang, Choi, Jeon, "Cost-effective On-device Continual Learning over Memory Hierarchy with '
               'Miro" (arXiv:2308.06053; ACM MobiCom 2023)',
     'version': 'v4, 5 Dec 2023', 'url': 'https://arxiv.org/abs/2308.06053',
     'quote': ['(1) Removable storage devices are cheap.',
               'Edge devices that adopt CL to preserve data privacy are typically energy-sensitive'],
     'raw_file': 'f3/src/pdf_2308.06053v4.txt',
     'agent_note': 'Contradicts part (b) on device: hierarchical raw replay memory on edge devices, with storage called '
                   'cheap; the cost it optimises is energy. It notes that as tasks scale the storage may be exceeded.'},
    {'id': 'w3:16', 'tag': 'P6', 'reading': 'bears', 'reading_by': RB,
     'source': 'Prabhu, Al Kader Hammoud, Dokania, Torr, Lim, Ghanem, Bibi, "Computationally Budgeted Continual Learning: '
               'What Does Matter?" (arXiv:2303.11165; CVPR 2023)',
     'version': 'v2, 15 Jul 2023', 'url': 'https://arxiv.org/abs/2303.11165',
     'quote': ['This is unreasonable for applications in-the-wild, where systems are primarily constrained by computational and '
               'time budgets, not storage.'],
     'raw_file': 'f3/src/pdf_2303.11165v2.txt',
     'agent_note': 'Bears: storage is called cheap for server-side CL; the scope is not on-device or privacy-constrained.'},
    {'id': 'w3:17', 'tag': 'P6', 'reading': 'close', 'reading_by': RB,
     'source': 'Wilson, "Latent Replay Detection: Memory-Efficient Continual Object Detection on Microcontrollers via Task-Adaptive '
               'Compression" (LRD; arXiv:2603.00138)',
     'version': 'v1, 24 Feb 2026', 'url': 'https://arxiv.org/abs/2603.00138',
     'quote': ['Existing continual learning methods require storing raw images—far exceeding MCU memory budgets of tens of '
               'kilobytes.',
               'LRD stores compressed feature representations instead of raw images, enabling a 64KB memory buffer to hold '
               '400+ exemplars compared to only 3-5 full images.'],
     'raw_file': 'f3/src/pdf_2603.00138v1.txt',
     'agent_note': 'Close: part (b) on microcontrollers; the small store it keeps is compressed latents, not raw rows (a raw '
                   'buffer of 3-5 images is named as what fits).'},
    {'id': 'w3:18', 'tag': 'P6', 'reading': 'close', 'reading_by': RB,
     'source': 'Motetti, Dugas du Villard, Risso, Burrello, Daghero, Macii, Poncino, Castellano, Basile, Jahier Pagliari, '
               '"MAUPITI: On-Device Prototype-Based Learning on a Smart Infrared Sensor" (arXiv:2608.07192; accepted, IEEE '
               'Embedded Systems Letters)',
     'version': 'v1, 7 Aug 2026', 'url': 'https://arxiv.org/abs/2608.07192',
     'quote': ['To avoid the memory overheads of backpropagation and replay buffers, we adopt a prototype-based Nearest Class '
               'Mean (NCM) classifier'],
     'raw_file': 'f3/src/pdf_2608.07192v1.txt',
     'agent_note': 'Close: part (b) under <32 kB on-chip memory; stores prototypes, no raw rows.'},
    {'id': 'w3:19', 'tag': 'P6', 'reading': 'close', 'reading_by': RB,
     'source': 'Li, Dutt, Liu, "Orion: Enabling Self-adaptive Memory Management for On-device Online Continual Learning" '
               '(arXiv:2605.26473)',
     'version': 'v1, 26 May 2026', 'url': 'https://arxiv.org/abs/2605.26473',
     'quote': ['When batch size increases, when the buffer grows, or when heavier plugins are enabled, the combined footprint '
               'often exceeds device capacity, which leads to OOM and unstable training.'],
     'raw_file': 'f3/src/pdf_2605.26473v1.txt',
     'agent_note': 'Close: on device the replay buffer competes for a fixed memory pool and is sized at run time; no small '
                   'raw store is named as the acceptable middle.'},
    {'id': 'w3:20', 'tag': 'P6', 'reading': 'close', 'reading_by': RB,
     'source': 'Ravaglia, Rusci, Nadalini, Capotondi, Conti, Benini, "A TinyML Platform for On-Device Continual Learning with '
               'Quantized Latent Replays" (arXiv:2110.10486; IEEE JETCAS 2021)',
     'version': 'v1, 20 Oct 2021', 'url': 'https://arxiv.org/abs/2110.10486',
     'quote': ['The main drawback of memory-based CL approaches concerns the high memory overhead for the storage of previous '
               'samples: the memory requirement can potentially grows over time preventing the applicability of these '
               'methods at the tiny scale'],
     'raw_file': 'f3/src/pdf_2110.10486v1.txt',
     'agent_note': 'Close: part (b) at the TinyML scale; the store kept is quantized latent replays, not raw rows.'},
    {'id': 'w3:21', 'tag': 'P6', 'reading': 'close', 'reading_by': RB,
     'source': 'Jiang, Hu, Song, Xie, Xu, "Study of Class-Incremental Radio Frequency Fingerprint Recognition Without '
               'Storing Exemplars" (arXiv:2601.03063)',
     'version': 'v1, 6 Jan 2026', 'url': 'https://arxiv.org/abs/2601.03063',
     'quote': ['Conventional static training and naive replay of stored exemplars are impractical due to growing class '
               'cardinality, storage cost, and privacy concerns.'],
     'raw_file': 'f3/src/pdf_2601.03063v1.txt',
     'agent_note': 'Close: part (b) for IoT device identification (storage and privacy); goes exemplar-free (Gaussian '
                   'mixtures of features), no small raw store.'},
    {'id': 'w3:22', 'tag': 'P6', 'reading': 'close', 'reading_by': RB,
     'source': 'Kumari, Reisenbüchler, Luttner, Schaadt, Feuerhake, Merhof, "Continual Domain Incremental Learning for '
               'Privacy-aware Digital Pathology" (GLRCL; arXiv:2409.06455; MICCAI 2024)',
     'version': 'v1, 10 Sep 2024', 'url': 'https://arxiv.org/abs/2409.06455',
     'quote': ['However, storing past samples may cause privacy violations [12], which can be a major bottleneck of such CL '
               'approaches in medical applications.',
               'performs similarly to rehearsal-based CL approaches that require large buffers causing serious privacy '
               'violations.'],
     'raw_file': 'f3/src/pdf_2409.06455v1.txt',
     'agent_note': 'Close: part (b) under privacy (large raw buffers named as privacy violations); the answer is buffer-free, '
                   'so no small raw store is named acceptable.'},
    {'id': 'w3:23', 'tag': 'P6', 'reading': 'close', 'reading_by': RB,
     'source': 'Sinhal, Sinhal, Sinhal, "Federated Continual Learning for Privacy-Preserving Hospital Imaging '
               'Classification" (DP-FedEPC; arXiv:2601.06742)',
     'version': 'v1, 11 Jan 2026', 'url': 'https://arxiv.org/abs/2601.06742',
     'quote': ['existing methods either ignore the stringent privacy constraints of healthcare or rely on replay buffers and '
               'public surrogate datasets that are difficult to justify in clinical settings.'],
     'raw_file': 'f3/src/pdf_2601.06742v1.txt',
     'agent_note': 'Close: part (b) under HIPAA/GDPR-type constraints; the method keeps prototypes, no raw rows.'},
    {'id': 'w3:24', 'tag': 'P6', 'reading': 'close', 'reading_by': RB,
     'source': 'Li, Wang, Xu, Xiao, Liu, Tu, Wang, Yang, Zhang, Yu, Guo, Li, "Unleashing the Power of Continual Learning on '
               'Non-Centralized Devices: A Survey" (arXiv:2412.13840)',
     'version': 'v2, 6 May 2025', 'url': 'https://arxiv.org/abs/2412.13840',
     'quote': ['In such cases, data collection in central entities, referred to as centralized training, is often infeasible or '
               'impractical due to limited communication resources, data privacy concerns, or country regulations.',
               'Experience Replay: Its main idea is to use cached data with limited memory buffers to help models retain the '
               'knowledge of previous tasks as they learn new ones'],
     'raw_file': 'f3/src/pdf_2412.13840v2.txt',
     'agent_note': 'Close: across distributed devices, central pooling is infeasible (privacy, regulation) and local replay '
                   'uses limited buffers; the survey does not tie the two into "small raw store acceptable, full not".'},
    {'id': 'w3:25', 'tag': 'P6', 'reading': 'bears', 'reading_by': RB,
     'source': 'Lanzillotta, Meier, Hofmann, "Heads collapse, features stay: Why Replay needs big buffers" (arXiv:2512.07400)',
     'version': 'v2, 19 Mar 2026', 'url': 'https://arxiv.org/abs/2512.07400',
     'quote': ['while minimal buffers successfully anchor feature geometry and prevent deep forgetting, mitigating shallow '
               'forgetting typically requires substantially larger buffer capacities.'],
     'raw_file': 'f3/src/pdf_2512.07400v2.txt',
     'agent_note': 'Bears: what a small raw buffer does and does not buy (features held, classifier not); no device or '
                   'privacy setting. Also relevant to P4 (a minimal buffer holds the feature geometry).'},
]
