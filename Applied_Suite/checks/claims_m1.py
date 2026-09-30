"""APP1 stage C, family M1 (Applied_Suite/APPLICATIONS_DECLARATION.md): on-device and edge learning shipping in 2025-26, its
stated constraints, and the published evidence on the cost of hyperparameter sweeps in fine-tuning and continual learning.

Every quote is copied from the text extracted from the fetched source, fetched 2026-09-30 through the session proxy:
- arXiv and CVF PDFs: the current version, text by pymupdf 1.28.2;
- vendor web pages: the HTML as served, text by BeautifulSoup get_text('\\n') after script/style/noscript were dropped;
- the Apple developer page: its documentation JSON, flattened to text with each inline reference replaced by its title.
Raw files live outside the repository under /tmp/claude-0/app1_src/ (`raw_file` is relative to that root); their sha256
is in /tmp/claude-0/app1_src/m1/SHA256SUMS.txt and in the dossier docs/citations/app1_m1_2026-09-30.md.

Roles (the task that set up this sweep): 'who_does_it' = who already does it and how; 'what_is_hard' = what they say is
hard; 'our_method_relevance' = whether the record's method addresses that difficulty or a different one; 'regulation' and
'risk' as named. `application` is AP1..AP10 of the declaration, or 'general' for the sweep-cost evidence that bears on
the Energy and Compute dimensions of every application. `agent_note` is the agent's reading, not the source's words; it
quotes no number from the record (R1, R8): ledger rows and pinned outputs are named by id only. Numbers from different
sources are not comparable. "Not found" is never "novel".
"""

R = 'm1/txt/'

CLAIMS = [
    # ---------------- AP1: on-device personalisation without a per-device hyperparameter sweep
    {'id': 'm1:1', 'application': 'AP1', 'role': 'who_does_it',
     'source': 'Apple, Core ML documentation: Personalizing a Model with On-Device Updates (sample code article)',
     'version': 'developer.apple.com documentation JSON as served 2026-09-30 (no date on the page; sample targets iOS 13 or later)',
     'url': 'https://developer.apple.com/documentation/coreml/personalizing-a-model-with-on-device-updates',
     'quote': ['With the Core ML framework, you can customize an updatable model at runtime on the user’s device. Using this '
               'technique, you can create a personalized experience for the user while keeping their data private.',
               'Each time the user adds a new emoji sticker, the app prompts the user to make three drawings, and uses those '
               'drawings to update the drawing classifier.',
               'An MLModelConfiguration, if applicable'],
     'raw_file': R + 'apple_coreml_personalizing.json.txt',
     'agent_note': 'The platform API for on-device training on phones (MLUpdateTask). In the sample the configuration is '
                   'passed as nil, so the update runs with the parameters baked into the model file: the developer fixes '
                   'them before shipping, and nothing is tuned per device.'},
    {'id': 'm1:2', 'application': 'AP1', 'role': 'who_does_it',
     'source': 'Paulik et al. (Apple), Federated Evaluation and Tuning for On-Device Personalization: System Design & Applications',
     'version': 'arXiv v1, 16 Feb 2021 (only version)', 'url': 'https://arxiv.org/abs/2102.08503v1',
     'quote': ['This use case requires evaluating and tuning the global (i.e., common to all end users) parameters of a '
               'personalization algorithm that creates device specific ASR language models by ingesting data that is only '
               'available on-device.',
               'During tuning task execution, the plug-in runs a randomized grid search on the parameter space defined, '
               'randomly generating configurations.',
               'Running a single FT task iteration results in millions of loss and configuration pairs from thousands of devices.'],
     'raw_file': R + '2102.08503v1.pdf.txt',
     'agent_note': 'How a phone vendor avoided a per-device sweep, as published in 2021: the personalisation parameters are global, and they '
                   'are tuned by a randomized grid search spread across the fleet (federated tuning), not per device and not '
                   'removed. The sweep still exists; its cost is moved onto many devices.'},
    {'id': 'm1:3', 'application': 'AP1', 'role': 'what_is_hard',
     'source': 'Paulik et al. (Apple), Federated Evaluation and Tuning for On-Device Personalization',
     'version': 'arXiv v1, 16 Feb 2021', 'url': 'https://arxiv.org/abs/2102.08503v1',
     'quote': ['Tuning of these parameters is challenging, since news content is constantly changing, e.g., due to new topics '
               'or due to seasonal variations in topic relevance. As a consequence, continuous adaptation of these parameters '
               'with quick turnaround times is important, so that the most relevant content can continue to be surfaced '
               'despite these changing trends.'],
     'raw_file': R + '2102.08503v1.pdf.txt',
     'agent_note': 'The vendor names the difficulty as re-tuning under drift: a tuned value goes stale as the stream changes, '
                   'so tuning must be repeated. A weight set without a sweep would address the repetition, if it held on the '
                   'vendor\'s streams; the record has not tested news or speech streams.'},
    {'id': 'm1:4', 'application': 'AP1', 'role': 'who_does_it',
     'source': 'Widex (WS Audiology), How hearing aids use machine learning (Widex Pro page on SoundSense Learn / Widex MySound)',
     'version': 'page as served 2026-09-30 (© 2026; linked guide PDFs dated 30/09/22)',
     'url': 'https://www.widexpro.com/en/widex-technology/artificial-intelligence/sound-sense-learn/',
     'quote': ['They can choose to partner with AI, training it to tailor the sound to your particular situation, or they can '
               'select a sound profile automatically generated from the preferences of other users in similar situations all '
               'over the world.',
               'Every time a user makes a change to their settings, their preferences are training our AI in the cloud so it '
               'can be smarter, further refining these automatic recommendations.'],
     'raw_file': R + 'widexpro_soundsense_learn.html.txt',
     'agent_note': 'Hearing-aid personalisation that ships: the user trains it by comparisons in the phone app, and the '
                   'pooled model is trained in the cloud. On this page the learning is not on the hearing aid itself.'},
    {'id': 'm1:5', 'application': 'AP1', 'role': 'what_is_hard',
     'source': 'Khodak et al., Federated Hyperparameter Tuning: Challenges, Baselines, and Connections to Weight-Sharing (NeurIPS 2021)',
     'version': 'arXiv v2, 4 Nov 2021 (v1 8 Jun 2021)', 'url': 'https://arxiv.org/abs/2106.04502v2',
     'quote': ['Hyperparameter optimization is even more challenging in federated learning, where models are learned over a '
               'distributed network of heterogeneous devices; here, the need to keep data on device and perform local '
               'training makes it difficult to efficiently train and evaluate configurations.',
               'Extreme resource limitations: FL applications often involve training using devices with very limited '
               'computational and communication capabilities. Furthermore, many require the use of privacy techniques such as '
               'differential privacy that limit the number times user data can be accessed. Thus we cannot depend on being '
               'able to run many different configurations to completion.'],
     'raw_file': R + '2106.04502v2.pdf.txt',
     'agent_note': 'States the AP1 premise directly: on devices a sweep cannot be run to completion, for compute and for '
                   'privacy reasons. Their answer (FedEx) tunes while training; it does not remove the hyperparameter.'},
    {'id': 'm1:6', 'application': 'AP1', 'role': 'what_is_hard',
     'source': 'Lin, Zhu, Chen, Wang, Gan, Han (MIT), On-Device Training Under 256KB Memory (NeurIPS 2022)',
     'version': 'arXiv v4, 3 Apr 2024 (v1 30 Jun 2022)', 'url': 'https://arxiv.org/abs/2206.15472v4',
     'quote': ['However, the training memory consumption is prohibitive for IoT devices that have tiny memory resources.',
               'Tiny IoT devices (e.g., microcontrollers) typically have a limited SRAM size like 256KB.',
               'For example, fine-tuning a language model enables continual learning from users’ typing and writing'],
     'raw_file': R + '2206.15472v4.pdf.txt',
     'agent_note': 'Memory is the binding constraint on the smallest devices (wearables, hearing aids, sensors). A method '
                   'that keeps several configurations alive to choose among them later multiplies exactly this memory.'},
    {'id': 'm1:7', 'application': 'AP1', 'role': 'what_is_hard',
     'source': 'Kwon, Li, Venieris, Chauhan, Lane, Mascolo, TinyTrain: Resource-Aware Task-Adaptive Sparse Training of DNNs at the Data-Scarce Edge (ICML 2024)',
     'version': 'arXiv v2, 10 Jun 2024 (v1 19 Jul 2023)', 'url': 'https://arxiv.org/abs/2307.09988v2',
     'quote': ['On-device training is essential for user personalisation and privacy. With the pervasiveness of IoT devices and '
               'microcontroller units (MCUs), this task becomes more challenging due to the constrained memory and compute '
               'resources, and the limited availability of labelled user data.',
               'While on-device training avoids the excessive electricity consumption and carbon emissions of centralised '
               'training (Schwartz et al., 2020; Patterson et al., 2022), it has thus far been a significantly draining '
               'process for the battery life of edge devices.'],
     'raw_file': R + '2307.09988v2.pdf.txt',
     'agent_note': 'Energy on the device is the user-visible cost (battery), and labelled data per user is scarce, so a '
                   'held-out split for choosing a hyperparameter is itself hard to come by on device.'},
    {'id': 'm1:8', 'application': 'AP1', 'role': 'what_is_hard',
     'source': 'Google (Jay Yagnik), Private AI Compute: our next step in building private and helpful AI (The Keyword blog)',
     'version': 'post dated 11 Nov 2025, as served 2026-09-30',
     'url': 'https://blog.google/innovation-and-ai/products/google-private-ai-compute/',
     'quote': ['This progression in capability requires advanced reasoning and computational power that at times goes beyond '
               'what’s possible with on-device processing.',
               'Private AI Compute is a secure, fortified space for processing your data that keeps your data isolated and '
               'private to you. It processes the same type of sensitive information you might expect to be processed on-device.'],
     'raw_file': R + 'google_private_ai_compute_blog.html.txt',
     'agent_note': 'A phone vendor\'s 2025 statement that on-device compute is insufficient for some personal AI, answered by a '
                   'sealed cloud enclave. The post is about processing (inference); it says nothing about learning from the '
                   'data inside the enclave.'},
    {'id': 'm1:9', 'application': 'AP1', 'role': 'what_is_hard',
     'source': 'Apple, Apple Intelligence Foundation Language Models: Tech Report 2025',
     'version': 'arXiv v3, 27 Aug 2025 (v1 17 Jul 2025, v2 26 Aug 2025)', 'url': 'https://arxiv.org/abs/2507.13575v3',
     'quote': ['For specialized use cases that require teaching the∼3B model entirely new skills, we also provide a Python '
               'toolkit for training rank-32 LoRA adapters',
               'However, each adapter is compatible with a single specific model version, meaning that a new adapter must be '
               'trained for each new version of the base model.',
               'Since each adapter takes significant storage space, the Foundation Models framework leverages the Background '
               'Assets framework to download just a single adapter that matches the base model’s version on device.'],
     'raw_file': R + '2507.13575v3.pdf.txt',
     'agent_note': 'Personalisation of the 2025 on-device model is by developer-trained adapters, trained off the device '
                   'with a Python toolkit, and every base-model update invalidates them. The retraining (and any sweep '
                   'inside it) recurs per base version; storage on device is a stated constraint.'},
    {'id': 'm1:10', 'application': 'AP1', 'role': 'our_method_relevance',
     'source': 'Xu, Zhang, Andrew, Choquette-Choo, Kairouz, McMahan, Rosenstock, Zhang (Google), Federated Learning of Gboard Language Models with Differential Privacy (ACL industry track)',
     'version': 'arXiv v2, 17 Jul 2023 (v1 29 May 2023)', 'url': 'https://arxiv.org/abs/2305.18465v2',
     'quote': ['We show how quantile-based clip estimation [Andrew et al., 2021] can be combined with DP-FTRL to adaptively '
               'choose the clip norm during training or reduce the hyperparameter tuning in preparation for training.',
               'For example, adaptive clipping for the de-DE NWP model experiences catastrophic failure and makes no progress '
               'in the first 1000 rounds.',
               'Nevertheless, adaptive clipping can reduce hyperparameter tuning for many tasks when privacy budget allows.'],
     'raw_file': R + '2305.18465v2.pdf.txt',
     'agent_note': 'A deployed precedent for a tuning-reducing estimator in on-device learning, and for its failure mode: it '
                   'worked on many models and failed catastrophically on one, so the vendor fixed the clip from the '
                   'estimate. The same shape as the record\'s SEC family (SEC4-1 PASS-1 not replicated by SEC5-1): a '
                   'sweep-free rule that holds on most carriers is not yet a rule that can ship without a fallback.'},
    {'id': 'm1:11', 'application': 'AP1', 'role': 'our_method_relevance',
     'source': 'Kwon, Chauhan, Kumar, Hui, Mascolo, Exploring System Performance of Continual Learning for Mobile and Embedded Sensing Applications (SEC 2021)',
     'version': 'arXiv v2, 23 Jun 2022 (v1 25 Oct 2021)', 'url': 'https://arxiv.org/abs/2110.13290v2',
     'quote': ['(2) 𝜆⊂{1, 10, 102, 103, 104, 105, 106} for both EWC and Online EWC',
               'Note that tuning appropriate parameters in the IL method would still allow IL to perform effectively'],
     'raw_file': R + '2110.13290v2.pdf.txt',
     'agent_note': 'The extractor flattens superscripts: the grid is 1, 10, 10^2 ... 10^6. In an on-device continual-learning '
                   'study the penalty weight is searched over six orders of magnitude, which is the quantity K1 (the SEC '
                   'family) sets without a sweep. The record\'s method addresses this hyperparameter; it does not address the '
                   'learning rate, which the same study also sweeps.'},

    # ---------------- general: the published cost of hyperparameter sweeps in fine-tuning and continual learning
    {'id': 'm1:12', 'application': 'general', 'role': 'what_is_hard',
     'source': 'Strubell, Ganesh, McCallum, Energy and Policy Considerations for Deep Learning in NLP (ACL 2019)',
     'version': 'arXiv v1, 5 Jun 2019 (only version)', 'url': 'https://arxiv.org/abs/1906.02243v1',
     'quote': ['Research and development of new models multiplies these costs by thousands of times by requiring retraining to '
               'experiment with model architectures and hyperparameters.',
               'During that time 123 small hyperparameter grid searches were performed, resulting in 4789 jobs in total.',
               'Estimated cost (USD) Models Hours Cloud compute Electricity 1 120 $52–$175 $5 24 2880 $1238–$4205 $118 4789 '
               '239,942 $103k–$350k $9870',
               'the cost of tuning a model for a new dataset, which we estimate here to require 24 jobs, or performing the '
               'full R&D required to develop this model, quickly becomes extremely expensive.'],
     'raw_file': R + '1906.02243v1.pdf.txt',
     'agent_note': 'Table 4 read by rows (models, hours, cloud cost, electricity): one model 120 h; one tune for a new dataset '
                   '24 models, 2880 h (24 times one model); the whole project 4789 models. The tune-per-new-dataset row is the '
                   'unit a sweep-free weight would remove; the paper is about 2018 NLP hardware and prices.'},
    {'id': 'm1:13', 'application': 'general', 'role': 'what_is_hard',
     'source': 'Schwartz, Dodge, Smith, Etzioni, Green AI',
     'version': 'arXiv v3, 13 Aug 2019 (v1 22 Jul 2019); later published in CACM', 'url': 'https://arxiv.org/abs/1907.10597v3',
     'quote': ['the number of (H)yperparameter experiments, which controls how many times the model is trained during model '
               'development. The total cost of producing a (R)esult in machine learning increases linearly with each of these '
               'quantities.',
               'Some projects have poured large amounts of computation into tuning hyperparameters or searching over neural '
               'architectures, well beyond the reach of most researchers.'],
     'raw_file': R + '1907.10597v3.pdf.txt',
     'agent_note': 'The cost model the Energy and Compute dimensions need: cost is linear in the number of hyperparameter '
                   'experiments, so removing an n-point sweep divides that factor by n, before any other saving.'},
    {'id': 'm1:14', 'application': 'general', 'role': 'what_is_hard',
     'source': 'Dodge, Gururangan, Card, Schwartz, Smith, Show Your Work: Improved Reporting of Experimental Results (EMNLP 2019)',
     'version': 'arXiv v1, 6 Sep 2019 (only version)', 'url': 'https://arxiv.org/abs/1909.03004v1',
     'quote': ['expected validation performance of the best-found model as a function of computation budget (i.e., the number '
               'of hyperparameter search trials or the overall training time).',
               'Using our approach, we find multiple recent model comparisons where authors would have reached a different '
               'conclusion if they had used more (or less) computation.',
               'applying it to several recently published results yields massive variation across papers, from hours to weeks.'],
     'raw_file': R + '1909.03004v1.pdf.txt',
     'agent_note': 'For fine-tuned NLP models the tuning budget changes which model wins. Any claim that a sweep-free method '
                   'saves compute must state the sweep it is compared with; a small sweep and a large one give different '
                   'savings and can give different winners.'},
    {'id': 'm1:15', 'application': 'general', 'role': 'what_is_hard',
     'source': 'Wang, Na, Strubell, Friedler, Luccioni, Energy and Carbon Considerations of Fine-Tuning BERT (Findings of EMNLP 2023)',
     'version': 'arXiv v2, 16 Oct 2024 (v1 17 Nov 2023)', 'url': 'https://arxiv.org/abs/2311.10267v2',
     'quote': ['Although a single pre-training run draws substantially more energy than fine-tuning, fine-tuning is performed '
               'more frequently by many more individual actors, and thus must be accounted for when considering the energy '
               'and carbon footprint of NLP.',
               'We find that pre-training BERT is equivalent to anywhere from 400 (MNLI) to 45,000 (RTE) fine-tuning runs '
               'depending on the dataset size'],
     'raw_file': R + '2311.10267v2.pdf.txt',
     'agent_note': 'Fine-tuning energy is a sum over many actors and many runs; each run is small. A per-run saving (fewer '
                   'configurations per fine-tune) scales with the number of fine-tunes, which is the premise of the '
                   'Compute_Savings estimates; this paper measures single runs, not sweeps.'},
    {'id': 'm1:16', 'application': 'general', 'role': 'what_is_hard',
     'source': 'Lee, Hellan, Ericsson, Crowley, Storkey, Hyperparameter Selection in Continual Learning',
     'version': 'arXiv v2, 14 Mar 2025 (v1 9 Apr 2024); preprint', 'url': 'https://arxiv.org/abs/2404.06466v2',
     'quote': ['The most popular way to tune hyperparameters in CL is to repeatedly train over the whole data stream with '
               'different hyperparameter settings. However, this end-of-training HPO is unusable in practice since a learner '
               'can only see the stream once.',
               'This HPO framework is expensive as it needs to perform a training run over the entire data stream for each '
               'hyperparameter configuration looked at.',
               'This means for DER++ we search across 90 different hyperparameter configurations (learning rate and two '
               'regularisation coefficients)'],
     'raw_file': R + '2404.06466v2.pdf.txt',
     'agent_note': 'In continual learning the standard sweep costs one full pass over the stream per configuration (90 for '
                   'DER++ on their grid) and is not available to a deployed learner at all.'},
    {'id': 'm1:17', 'application': 'general', 'role': 'our_method_relevance',
     'source': 'Lee, Hellan, Ericsson, Crowley, Storkey, Hyperparameter Selection in Continual Learning',
     'version': 'arXiv v2, 14 Mar 2025', 'url': 'https://arxiv.org/abs/2404.06466v2',
     'quote': ['This is surprising as it suggests that for the current popular CL benchmarks there is no HPO framework that '
               'consistently performs better than the most simple approach of tuning hyperparameters on the first task.',
               'First-task HPO is computationally efficient as it trains using each hyperparameter configuration solely on the '
               'first task and then only trains using one configuration for the rest of the tasks.'],
     'raw_file': R + '2404.06466v2.pdf.txt',
     'agent_note': 'The cheap realistic baseline a sweep-free weight must beat on compute is first-task HPO, not the full '
                   'end-of-training sweep. The record\'s P1 found many held-out carriers floor-bound (F12, '
                   'SEC_Analysis/checks/a12_a14.txt), and its must-fail control, a learner frozen after task 1 (M6), failed '
                   'to fail (FM6, SEC_Analysis/checks/a11_grade.txt and m_checks.txt). A saving claimed against the full '
                   'sweep alone would overstate K1.'},
    {'id': 'm1:18', 'application': 'general', 'role': 'what_is_hard',
     'source': 'Cha & Cho, Hyperparameters in Continual Learning: A Reality Check (TMLR, 04/2025)',
     'version': 'arXiv v5, 28 Oct 2025 (TMLR camera ready; v1 14 Mar 2024)', 'url': 'https://arxiv.org/abs/2403.09066v5',
     'quote': ['However, this protocol has significant shortcomings: it overestimates the CL capacity of algorithms and relies '
               'on unrealistic hyperparameter tuning, which is not feasible for real-world applications.',
               'Across more than 8,000 experiments, our results show that most state-of-the-art algorithms fail to replicate '
               'their reported performance',
               'First, implementing GTEP requires repeated training trials, which can be computationally demanding. In our '
               'experiments, we conducted 30 random trials per algorithm with 5 seeds per trial.'],
     'raw_file': R + '2403.09066v5.pdf.txt',
     'agent_note': 'Two costs of tuning in CL: compute (30 trials x 5 seeds per algorithm in their protocol) and inflated '
                   'reported performance when tuning and evaluation share a scenario. The record\'s comparator, a lambda tuned on '
                   'each carrier it is scored on, is of the conventional kind and so an optimistic reference; the SEC-T rows '
                   '(a lambda carried over from other carriers) are the comparison of the kind this paper proposes.'},

    # ---------------- AP2: fine-tuning on interruptible compute
    {'id': 'm1:19', 'application': 'AP2', 'role': 'who_does_it',
     'source': 'Bonawitz et al. (Google), Towards Federated Learning at Scale: System Design (SysML 2019)',
     'version': 'arXiv v2, 22 Mar 2019 (v1 4 Feb 2019)', 'url': 'https://arxiv.org/abs/1902.01046v2',
     'quote': ['Possibly the most important requirement for training machine learning (ML) models on end users’ devices is to '
               'avoid any negative impact on the user experience, data usage, or battery life.',
               'The FL runtime requests that the job scheduler only invoke the job when the phone is idle, charging, and '
               'connected to an unmetered network such as WiFi. Once started, the FL runtime will abort, freeing the '
               'allocated resources, if these conditions are no longer met.'],
     'raw_file': R + '1902.01046v2.pdf.txt',
     'agent_note': 'Phones are already interruptible training compute: training runs only in idle windows and yields at once '
                   'when the user returns. The interruption is an abort that frees the resources; the paper does not describe '
                   'resuming the aborted local computation.'},
    {'id': 'm1:20', 'application': 'AP2', 'role': 'what_is_hard',
     'source': 'Bonawitz et al. (Google), Towards Federated Learning at Scale: System Design',
     'version': 'arXiv v2, 22 Mar 2019', 'url': 'https://arxiv.org/abs/1902.01046v2',
     'quote': ['75% of clients complete their training rounds successfully, 22% of clients complete their training rounds but '
               'have their results rejected by the server (these are the devices which report back after the reporting '
               'window already closed), and 2% of clients are interrupted before being able',
               'the drop out rate is higher during the day time compared to the night time. This is explained by higher '
               'probability of the device eligibility criteria changes due interaction with a device.'],
     'raw_file': R + '1902.01046v2.pdf.txt',
     'agent_note': 'The measured cost of interruption in a production system: most wasted device work is late results thrown '
                   'away by the round deadline, not interrupted training. A lossless pause of the local learner addresses the '
                   'interrupted share; the discarded late share is a protocol (deadline) cost that a pause does not touch.'},

    # ---------------- AP3: a user's "stop learning from me" switch
    {'id': 'm1:21', 'application': 'AP3', 'role': 'who_does_it',
     'source': 'Google, Gboard Help: Learn how Gboard gets better',
     'version': 'help page as served 2026-09-30 (redirected to answer 12373137; no date on the page)',
     'url': 'https://support.google.com/gboard/answer/9334583?hl=en',
     'quote': ['Gboard only uses federated learning while your phone charges, is connected to Wi-Fi, and isn\'t in use.',
               'Federated learning is turned on by default. You can turn it off at any time.',
               'Clears all on-device data that Gboard has saved.'],
     'raw_file': R + 'gboard_help_learn_how_gets_better.html.txt',
     'agent_note': 'A shipped "stop learning from me" control: an off switch for federated learning, and a delete-all for '
                   'on-device learned data. The page says nothing about whether turning learning off and on again leaves the '
                   'personal model exactly as it was, which is the property AP3 claims.'},
    {'id': 'm1:22', 'application': 'AP3', 'role': 'who_does_it',
     'source': 'YouTube Help: View, delete, or turn on or off watch history (Computer)',
     'version': 'help page as served 2026-09-30 (no date on the page)',
     'url': 'https://support.google.com/youtube/answer/95725?hl=en&co=GENIE.Platform%3DDesktop',
     'quote': ['You can control your watch history by deleting or turning off your history. If you delete some or all of your '
               'watch history, YouTube won’t base future video recommendations on that content. Any videos that you watch '
               'while history is turned off won\'t show up in your history.'],
     'raw_file': R + 'youtube_watch_history_help.html.txt',
     'agent_note': 'A platform-scale version of the switch: what is watched while history is off does not enter the history '
                   'that recommendations are based on. It is a switch on the data input, not on the model state.'},
    {'id': 'm1:23', 'application': 'AP3', 'role': 'what_is_hard',
     'source': 'Paulik et al. (Apple), Federated Evaluation and Tuning for On-Device Personalization',
     'version': 'arXiv v1, 16 Feb 2021', 'url': 'https://arxiv.org/abs/2102.08503v1',
     'quote': ['In addition, devices need to be opted into the data collection program, thus enabling end users to opt out of '
               'participation.',
               'Our design choice to limit participation to opt-in devices has the potential to introduce bias. Another source '
               'for potential bias is the fact that devices need to be plugged into power, idle, and connected to an unmetered '
               'network in order to run federated tasks'],
     'raw_file': R + '2102.08503v1.pdf.txt',
     'agent_note': 'The vendor\'s stated cost of honouring an opt-out: the learning population becomes biased. An exact '
                   'pause of one user\'s learner addresses that user\'s state, not the population bias of the shared model.'},

    # ---------------- AP4: operator-interruptible continual agents
    {'id': 'm1:24', 'application': 'AP4', 'role': 'risk',
     'source': 'Apple Security Engineering and Architecture et al., Private Cloud Compute: A new frontier for AI privacy in the cloud (Apple Security Research blog)',
     'version': 'post dated 10 Jun 2024, as served 2026-09-30', 'url': 'https://security.apple.com/blog/private-cloud-compute/',
     'quote': ['Private Cloud Compute must not contain privileged interfaces that would enable Apple’s site reliability staff '
               'to bypass PCC privacy guarantees, even when working to resolve an outage or other severe incident.'],
     'raw_file': R + 'apple_pcc_blog.html.txt',
     'agent_note': 'A tension, not a precedent: the strongest privacy design removes privileged operator interfaces even in an '
                   'incident. An operator-interruptible learner must say which interface stays (a pause) and show that it '
                   'does not widen the privileged envelope. The M1 sources hold no who-does-it or what-is-hard statement for '
                   'operator interruption of learning agents; M3 (oversight regulation) is where AP4 is swept.'},

    # ---------------- AP5: continual learning in privacy-regulated settings without keeping raw examples
    {'id': 'm1:25', 'application': 'AP5', 'role': 'who_does_it',
     'source': 'McMahan & Ramage (Google Research), Federated Learning: Collaborative Machine Learning without Centralized Training Data (blog)',
     'version': 'post dated 6 Apr 2017, as served 2026-09-30',
     'url': 'https://research.google/blog/federated-learning-collaborative-machine-learning-without-centralized-training-data/',
     'quote': ['Federated Learning enables mobile phones to collaboratively learn a shared prediction model while keeping all '
               'the training data on device, decoupling the ability to do machine learning from the need to store the data '
               'in the cloud.',
               'All the training data remains on your device, and no individual updates are stored in the cloud.'],
     'raw_file': R + 'google_research_fl_2017.html.txt',
     'agent_note': 'The shipped privacy answer keeps raw data, on the device. K4 (continual learning without stored raw '
                   'examples at all) is a different and stronger property; its gates closed in the record (RQM-A, RRM-PA).'},
    {'id': 'm1:26', 'application': 'AP5', 'role': 'who_does_it',
     'source': 'Apple Differential Privacy Team, Learning with Privacy at Scale (Apple Machine Learning Research)',
     'version': 'article dated 6 Dec 2017, as served 2026-09-30', 'url': 'https://machinelearning.apple.com/research/learning-with-privacy-at-scale',
     'quote': ['This deployment scales to hundreds of millions of users across a variety of use cases, such as identifying '
               'popular emojis, popular health data types, and media playback preferences in Safari.',
               'Local differential privacy has the advantage that the data is randomized before being sent from the device, so '
               'the server never sees or receives raw data.'],
     'raw_file': R + 'apple_ml_privacy_at_scale.html.txt',
     'agent_note': 'Learning population statistics, including over health data types, without the server receiving raw data. '
                   'It learns aggregate statistics, not a continually trained model.'},
    {'id': 'm1:27', 'application': 'AP5', 'role': 'what_is_hard',
     'source': 'Kwon, Chauhan, Kumar, Hui, Mascolo, Exploring System Performance of Continual Learning for Mobile and Embedded Sensing Applications',
     'version': 'arXiv v2, 23 Jun 2022', 'url': 'https://arxiv.org/abs/2110.13290v2',
     'quote': ['Our findings suggest that replay with exemplars-based schemes such as iCaRL has the best performance trade-offs, '
               'even in complex scenarios, at the expense of some storage space (few MBs) for training examples (1% to 5%).',
               'In summary, the amount of storage required to practically enable continual learning on many modern edge '
               'platforms such as Nvidia Jetson or Raspberry PIs and smartphones is not excessive'],
     'raw_file': R + '2110.13290v2.pdf.txt',
     'agent_note': 'On phones the method that works keeps raw examples, and storage is not the obstacle. So the case for '
                   'exemplar-free continual learning on devices rests on retention and erasure rules (M3), not on memory.'},

    # ---------------- AP6: robot and drone on-board adaptation with safe pauses
    {'id': 'm1:28', 'application': 'AP6', 'role': 'who_does_it',
     'source': 'Google DeepMind (Carolina Parada), Gemini Robotics On-Device brings AI to local robotic devices (blog)',
     'version': 'post dated 24 Jun 2025, as served 2026-09-30',
     'url': 'https://deepmind.google/blog/gemini-robotics-on-device-brings-ai-to-local-robotic-devices/',
     'quote': ['Today, we’re introducing Gemini Robotics On-Device, our most powerful VLA model optimized to run locally on '
               'robotic devices.',
               'Since the model operates independent of a data network, it’s helpful for latency sensitive applications, and '
               'ensures robustness in environments with intermittent or zero connectivity.',
               'Our model quickly adapts to new tasks, with as few as 50 to 100 demonstrations',
               'In practice, we capture semantic and content safety using the Live API [...] and interface our models with '
               'low-level safety critical controllers to execute the actions.'],
     'raw_file': R + 'deepmind_gemini_robotics_on_device.html.txt',
     'agent_note': 'The on-board model runs without a link and is adapted from demonstrations; safety sits in separate '
                   'low-level controllers. The post does not say that the adaptation runs on the robot (see m1:29).'},
    {'id': 'm1:29', 'application': 'AP6', 'role': 'what_is_hard',
     'source': 'Chen, Srikanth, Jew, Wu, Wang, Ren, Tomizuka, Xu, Xie, Tian (UC Berkeley, Google DeepMind, NVIDIA), CLIFT: Turning Gemini Robotics On-Device into Humanoid Specialists via Non-Invasive Closed-Loop Iterative Fine-Tuning',
     'version': 'arXiv v1, 31 Jul 2026 (only version)', 'url': 'https://arxiv.org/abs/2607.29172v1',
     'quote': ['an emerging access paradigm for closed-weight robot foundation models is the managed supervised fine-tuning '
               '(SFT) API, where users submit training data and receive a tuned policy without access to model weights, '
               'gradients, or training internals.',
               'yet still falls short of deployment-level mastery on agile, contact-rich tasks.',
               'at the same time, such rollouts are costly and safety-sensitive to collect on hardware.'],
     'raw_file': R + '2607.29172v1.pdf.txt',
     'agent_note': 'In this study the on-device robot model is adapted through a managed fine-tuning API (users submit data '
                   'and receive a tuned policy); the robot runs the result. Real-robot data is costly and safety-sensitive, so '
                   'each learning episode on the robot is a safety event. The study gives no instance of learning on board.'},
    {'id': 'm1:30', 'application': 'AP6', 'role': 'our_method_relevance',
     'source': 'Chen et al., CLIFT', 'version': 'arXiv v1, 31 Jul 2026', 'url': 'https://arxiv.org/abs/2607.29172v1',
     'quote': ['Both models are fine-tuned with a standard supervised loss on observation-action pairs for 10 epochs per '
               'flywheel cycle using their default fine-tuning configurations, without model-specific hyperparameter tuning.'],
     'raw_file': R + '2607.29172v1.pdf.txt',
     'agent_note': 'In this study robot fine-tuning avoided per-model sweeps by taking each model\'s default configuration. '
                   'Where that is the practice, a sweep-free penalty weight competes with a fixed default, not with a sweep; '
                   'its compute saving against a default is nil, so its case would have to be forgetting, which this paper '
                   'does not measure.'},

    # ---------------- AP7: federated continual learning with clients that go offline mid-round
    {'id': 'm1:31', 'application': 'AP7', 'role': 'who_does_it',
     'source': 'Xu et al. (Google), Federated Learning of Gboard Language Models with Differential Privacy',
     'version': 'arXiv v2, 17 Jul 2023', 'url': 'https://arxiv.org/abs/2305.18465v2',
     'quote': ['In each communication round, the server will orchestrate a small subset of client devices for training and '
               'aggregate the resulting model deltas to update the global model. In a successful round, the system '
               'guarantees the number of clients participating in training is at least as large as the configured report goal',
               'we train and deploy more than twenty Gboard LMs that achieve high utility and ρ−zCDP privacy guarantees'],
     'raw_file': R + '2305.18465v2.pdf.txt',
     'agent_note': 'Federated training with intermittent clients ships at scale; the round succeeds by a report goal (enough '
                   'clients), so any single offline client is absorbed by the protocol rather than paused.'},
    {'id': 'm1:32', 'application': 'AP7', 'role': 'what_is_hard',
     'source': 'Bonawitz et al. (Google), Towards Federated Learning at Scale: System Design',
     'version': 'arXiv v2, 22 Mar 2019', 'url': 'https://arxiv.org/abs/1902.01046v2',
     'quote': ['We also observe that on average the portion of devices that drop out due to computation errors, network '
               'failures, or changes in eligibility varies between 6% and 10%. Therefore, in order to compensate for device '
               'drop out as well as to allow stragglers to be discarded, the server typically selects 130% of the target '
               'number of devices to initially participate.',
               'unreliable device connectivity and interrupted execution'],
     'raw_file': R + '1902.01046v2.pdf.txt',
     'agent_note': 'Drop-out is handled by over-selection (130%) and discarding stragglers: the incumbent pays for offline '
                   'clients with extra devices, not with lost state. EPS2\'s federated-client row is where the record reads '
                   'this; a lossless client pause would compete with over-selection, whose cost is spare device time.'},

    # ---------------- AP8: exact rollback and audit of a learning system
    {'id': 'm1:33', 'application': 'AP8', 'role': 'who_does_it',
     'source': 'Apple, Private Cloud Compute blog', 'version': 'post dated 10 Jun 2024, as served 2026-09-30',
     'url': 'https://security.apple.com/blog/private-cloud-compute/',
     'quote': ['security researchers must be able to verify the security and privacy guarantees of Private Cloud Compute, and '
               'they must be able to verify that the software that’s running in the PCC production environment is the same '
               'as the software they inspected when verifying the guarantees.'],
     'raw_file': R + 'apple_pcc_blog.html.txt',
     'agent_note': 'Verifiable audit as shipped: of the software image of a stateless inference service. There is no learned '
                   'state in PCC to roll back; AP8 is about the learned state, which this design avoids having.'},
    {'id': 'm1:34', 'application': 'AP8', 'role': 'what_is_hard',
     'source': 'Apple, Private Cloud Compute blog', 'version': 'post dated 10 Jun 2024, as served 2026-09-30',
     'url': 'https://security.apple.com/blog/private-cloud-compute/',
     'quote': ['Cloud AI security and privacy guarantees are difficult to verify and enforce.',
               'there is no widely deployed way for a user device (or browser) to confirm that the service it’s connecting to '
               'is running an unmodified version of the software that it purports to run, or to detect that the software '
               'running on the service has changed.'],
     'raw_file': R + 'apple_pcc_blog.html.txt',
     'agent_note': 'The vendor\'s statement of what is hard about audit. For a learner whose weights change continually, '
                   '"unmodified" is not a fixed image; a restore point must include the learned state and everything that '
                   'decides the next update (state closure, Empty_Cut_Engineering), which this design sidesteps by statelessness.'},
    {'id': 'm1:35', 'application': 'AP8', 'role': 'who_does_it',
     'source': 'Apple, Core ML documentation: Personalizing a Model with On-Device Updates',
     'version': 'developer.apple.com documentation JSON as served 2026-09-30',
     'url': 'https://developer.apple.com/documentation/coreml/personalizing-a-model-with-on-device-updates',
     'quote': ['The sample saves the updated model to the file system by first writing the model to a temporary location. Next, '
               'the sample moves the updated model to a permanent location, replacing any previously saved updated model.',
               'The sample updates the drawing classifier model it’s currently using, which could be the original drawing '
               'classifier model or a previously updated model.'],
     'raw_file': R + 'apple_coreml_personalizing.json.txt',
     'agent_note': 'The platform sample commits a personalised model by write-then-move and keeps one: the only restore points '
                   'are the shipped base model and the latest update. Keeping earlier states is left to the developer.'},

    # ---------------- AP9: energy-aware scheduling against grid carbon intensity
    {'id': 'm1:36', 'application': 'AP9', 'role': 'who_does_it',
     'source': 'Apple Support, Use Clean Energy Charging on your iPhone', 'version': 'support article, published date on page 14 Apr 2026',
     'url': 'https://support.apple.com/en-us/108068',
     'quote': ['With iOS 16.1 and later, your iPhone charges when lower carbon-emission electricity is available. Clean Energy '
               'Charging is on by default in the United States.',
               'When Clean Energy Charging is on, your iPhone uses a forecast of carbon emissions. Your iPhone charges when '
               'cleaner energy is available.'],
     'raw_file': R + 'apple_clean_energy_charging.html.txt',
     'agent_note': 'Carbon-aware scheduling on the device ships, for charging. Since on-device learning runs only while '
                   'charging (m1:19, m1:21, m1:23), charging windows are the training windows; that link is the agent\'s '
                   'reading, not a vendor statement, and no vendor says it schedules training by carbon.'},
    {'id': 'm1:37', 'application': 'AP9', 'role': 'what_is_hard',
     'source': 'Apple Support, Use Clean Energy Charging on your iPhone', 'version': 'support article, published date on page 14 Apr 2026',
     'url': 'https://support.apple.com/en-us/108068',
     'quote': ['Clean Energy Charging works only where you charge your iPhone regularly for long periods, such as your home or '
               'workplace.',
               'If your charging habits vary or you\'re in a new location, Clean Energy Charging doesn\'t engage.'],
     'raw_file': R + 'apple_clean_energy_charging.html.txt',
     'agent_note': 'Shifting load needs long, predictable plugged-in windows; without them the feature does nothing. A '
                   'pausable learner makes a job shiftable, but the window still has to exist.'},

    # ---------------- AP10: feed and attention systems that honour a user's pause without penalising it
    {'id': 'm1:38', 'application': 'AP10', 'role': 'who_does_it',
     'source': 'YouTube Help: View, delete, or turn on or off watch history (Computer)',
     'version': 'help page as served 2026-09-30 (no date on the page)',
     'url': 'https://support.google.com/youtube/answer/95725?hl=en&co=GENIE.Platform%3DDesktop',
     'quote': ['YouTube watch history makes it easy to find videos you recently watched, and, when it’s turned on, allows us to '
               'give relevant video recommendations.',
               'Pause & clear watch history on TV or gaming console'],
     'raw_file': R + 'youtube_watch_history_help.html.txt',
     'agent_note': 'A feed that offers a user\'s pause: the watch history that feeds recommendations can be paused (the page '
                   'uses both "pause" and "turn off"). The pause acts on the input the recommender learns from.'},
    {'id': 'm1:39', 'application': 'AP10', 'role': 'what_is_hard',
     'source': 'YouTube Help: View, delete, or turn on or off watch history (Computer)',
     'version': 'help page as served 2026-09-30 (no date on the page)',
     'url': 'https://support.google.com/youtube/answer/95725?hl=en&co=GENIE.Platform%3DDesktop',
     'quote': ['If you have no relevant or significant recent watch history and have indicated you do not wish to receive '
               'future recommendations based on that history, YouTube features like recommendations on the YouTube homepage '
               'are removed.'],
     'raw_file': R + 'youtube_watch_history_help.html.txt',
     'agent_note': 'What the pause costs the user, in the platform\'s own words: past a point, the paused user loses homepage '
                   'recommendations. That is the penalty AP10 says a pause should not carry. The record\'s support for AP10 is '
                   'a synthetic model only (K6).'},
    {'id': 'm1:40', 'application': 'AP10', 'role': 'what_is_hard',
     'source': 'Ricks & McCrosky (Mozilla Foundation), Does This Button Work? Investigating YouTube\'s ineffective user controls',
     'version': 'report dated September 2022 (PDF as served 2026-09-30)',
     'url': 'https://assets.mofoprod.net/network/documents/Mozilla-Report-YouTube-User-Controls.pdf',
     'quote': ['YouTube’s user control mechanisms are inadequate for preventing unwanted recommendations. We determined that '
               'YouTube’s user controls influence what is recommended, but this effect is negligible and most unwanted videos '
               'still slip through.'],
     'raw_file': R + 'mozilla_youtube_user_controls.pdf.txt',
     'agent_note': 'Third-party audit (crowdsourced data, not the vendor): user controls change little. Older than 2025-26; '
                   'the controls audited are feedback buttons, not the history pause of m1:38.'},
]
