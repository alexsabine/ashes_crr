"""APP1 stage C, family M2 (Applied_Suite/APPLICATIONS_DECLARATION.md, pushed at 4e78058): pause, preemption,
checkpointing, exact resume and flexible training load. What training infrastructure already provides in 2025-26 for
the applications AP1-AP10, and what its own documentation or authors say is hard.

Sources were fetched or re-checked on 2026-09-30 through the session proxy (TLS verified). Every quote is copied from the
text extracted from the fetched file: PDF text by pymupdf 1.28.2 (arXiv current version), HTML by tag stripping (script,
style, noscript and svg blocks removed, entities unescaped), Apple's documentation from its JSON render (the "text" runs,
joined). Raw files live outside the repository under /tmp/claude-0/app1_src/ (`raw_file` is relative to that root):
  - m2/txt/       sources new to this family, fetched 2026-09-30 (log: m2/FETCH_LOG.txt);
  - m2/reused/    extracted texts carried over from the DR1, EPS2, Lossless_Pause and sweep dossiers (PDFs of the same
                  arXiv version, so the text is unchanged), with every URL re-checked on 2026-09-30 (m2/reused/REACH_LOG.txt);
  - m2/reused/recheck/  the HTML pages as re-fetched on 2026-09-30 (quoted from today's copy, not the older one).
sha256 of every file: /tmp/claude-0/app1_src/m2/SHA256SUMS.txt, and per source in docs/citations/app1_m2_2026-09-30.md.
The normalisation for the verbatim check is Open_Bottlenecks/checks/verify.py's (NFKC, whitespace collapsed, a line-break
hyphen read as kept or rejoined). A quote containing "[...]" is checked fragment by fragment.

Roles (the declaration's stage C): 'who_does_it' = who already provides it and how; 'what_is_hard' = what the provider or
the authors say is hard; 'our_method_relevance' = a source that bears directly on whether the record's method addresses
that difficulty; 'regulation'; 'risk'. `agent_note` is the agent's reading, not the source's words. It names the record
only by file or ledger id and quotes no number from the record (R8). "Not found" is never "novel". Nothing here grades an
application; the grading is Applied_Suite/checks/applications.py's.
"""

T = 'm2/txt/'          # fetched new on 2026-09-30
U = 'm2/reused/'       # carried over from an earlier dossier (PDF text of the same version)
V = 'm2/reused/recheck/'  # HTML re-fetched on 2026-09-30

CLAIMS = [
    # ------------------------------------------------------------------ AP1: on-device personalisation
    {'id': 'm2:1', 'application': 'AP1', 'role': 'who_does_it',
     'source': 'Google Privacy Sandbox, "On-Device Personalization - personalization with enhanced privacy protection" (Android technical explainer)',
     'version': 'Privacy Sandbox documentation page, "Last updated 2025-12-18 UTC"',
     'url': 'https://privacysandbox.google.com/protections/on-device-personalization',
     'quote': ['This is the current plan of record for testing ODP in Beta. The timeline is subject to change.',
               'On-Device Training + Inference',
               'Start rolling out to eligible Android T+ devices.'],
     'raw_file': T + 'odp_overview.html.txt',
     'agent_note': 'Android platform on-device training, as a beta with a stated roll-out (the timeline table places the '
                   'roll-out in Q3 2025). The companion page "Create a federated learning job" documents federated '
                   'averaging with fixed Gaussian noise (fetched; same "Last updated" date). The page says nothing about how '
                   'an on-device training job is paused or resumed, nor about per-device hyperparameters.'},
    {'id': 'm2:2', 'application': 'AP1', 'role': 'who_does_it',
     'source': 'Bonawitz et al. (Google), Towards Federated Learning at Scale: System Design (SysML 2019)',
     'version': 'arXiv 1902.01046v2, 22 Mar 2019 (v1 4 Feb 2019)', 'url': 'https://arxiv.org/abs/1902.01046v2',
     'quote': ['The FL runtime requests that the job scheduler only invoke the job when the phone is idle, charging, and '
               'connected to an unmetered network such as WiFi. Once started, the FL runtime will abort, freeing the '
               'allocated resources, if these conditions are no longer met.'],
     'raw_file': T + 'pdf_1902.01046v2.pdf.txt',
     'agent_note': 'The deployed pattern for on-device training: the device learns only in a narrow window and the job is '
                   'aborted, not paused, when the window closes. Old (2019) but it is the production design that later '
                   'systems cite (FeLiX, m2:29). The abort is at the level of a federated round, so the cost of the '
                   'interruption is a lost local update, not a corrupted model.'},
    {'id': 'm2:3', 'application': 'AP1', 'role': 'who_does_it',
     'source': 'Google AI Edge, "On-Device Training with LiteRT" (tutorial)',
     'version': 'developers.google.com page, "Last updated 2026-05-28 UTC" (the ai.google.dev URL redirects here)',
     'url': 'https://ai.google.dev/edge/litert/models/ondevice_training',
     'quote': ['For a model to be trained and used on a device, you must be able to perform several separate operations, '
               'including train, infer, save, and restore functions for the model.',
               'tensors_to_save = [ weight . read_value () for weight in self . model . weights ]',
               'Note: The weights generated by this model are serialized into a TensorFlow 1 format checkpoint file.'],
     'raw_file': T + 'litert_ondevice_training.html.txt',
     'agent_note': 'The on-device training runtime exposes save and restore as model signatures. The second quote is the '
                   'tutorial\'s save function as extracted (code, spacing from tag stripping): it writes the model\'s weights. '
                   'The agent reads the listing as not saving optimizer state; what a resume restores is left to the '
                   'developer. Nothing on hyperparameter selection per device.'},
    {'id': 'm2:4', 'application': 'AP1', 'role': 'what_is_hard',
     'source': 'Android Developers, "Define work requests" (WorkManager)',
     'version': 'developer.android.com page, "Last updated 2026-09-16 UTC"',
     'url': 'https://developer.android.com/develop/background-work/background-tasks/persistent/getting-started/define-work',
     'quote': ['When multiple constraints are specified, your work will run only when all the constraints are met.',
               'In the event that a constraint becomes unmet while your work is running, WorkManager will stop your worker. '
               'The work will then be retried when all the constraints are met.'],
     'raw_file': T + 'android_workmanager_define.html.txt',
     'agent_note': 'The operating system, not the learner, decides when background work stops (for example when the device '
                   'leaves the charger). "Retried" means the work restarts; whether the learner resumes where it was is left '
                   'to the app. An on-device learner is therefore paused from outside, often, and must checkpoint its own state.'},
    {'id': 'm2:5', 'application': 'AP1', 'role': 'what_is_hard',
     'source': 'Apple Developer Documentation, BGProcessingTask (BackgroundTasks framework)',
     'version': 'Apple documentation (JSON render), iOS 13.0+, iPadOS 13.0+, Mac Catalyst 13.1+, tvOS 13.0+; undated',
     'url': 'https://developer.apple.com/documentation/backgroundtasks/bgprocessingtask',
     'quote': ['Although processing tasks can run for minutes, the system can interrupt the process.',
               'Processing tasks run only when the device is idle. The system terminates any background processing tasks '
               'running when the user starts using the device.'],
     'raw_file': T + 'apple_bgprocessingtask.json.txt',
     'agent_note': 'Fetched as https://developer.apple.com/tutorials/data/documentation/backgroundtasks/bgprocessingtask.json '
                   '(the page itself is rendered by script). On iOS the user picking up the phone ends background training; the '
                   'companion "expirationHandler" page (fetched) says the handler "may be called before the background process '
                   'uses the full amount of its allocated time". A pause arrives at the user\'s moment, not the learner\'s.'},

    # ------------------------------------------------------------------ AP2: fine-tuning on interruptible compute
    {'id': 'm2:6', 'application': 'AP2', 'role': 'who_does_it',
     'source': 'Amazon Web Services, "Managed Spot Training in Amazon SageMaker AI"',
     'version': 'AWS documentation page, undated', 'url': 'https://docs.aws.amazon.com/sagemaker/latest/dg/model-managed-spot-training.html',
     'quote': ['Managed spot training can optimize the cost of training models up to 90% over on-demand instances.',
               'SageMaker AI copies checkpoint data from a local path to Amazon S3. When the job is restarted, SageMaker AI '
               'copies the data from Amazon S3 back into the local path. The training job can then resume from the last '
               'checkpoint instead of restarting.'],
     'raw_file': T + 'aws_sagemaker_managed_spot.html.txt',
     'agent_note': 'Interruptible training with checkpoint and resume is a managed cloud product. The saving is the vendor\'s '
                   '"up to" figure on price, not energy. The platform moves checkpoint files; what they contain is the user\'s '
                   'script\'s business (m2:7).'},
    {'id': 'm2:7', 'application': 'AP2', 'role': 'what_is_hard',
     'source': 'Amazon Web Services, "Checkpoints in Amazon SageMaker AI"',
     'version': 'AWS documentation page, undated', 'url': 'https://docs.aws.amazon.com/sagemaker/latest/dg/model-checkpoints.html',
     'quote': ['you must properly set up your training script using callbacks or training APIs to save checkpoints to the '
               'local path',
               'The SageMaker Python SDK does not support high-level configuration for checkpointing frequency.',
               'SageMaker AI does not allow a maximum wait time greater than an hour for the job in order to limit wasted '
               'training time from interrupts.'],
     'raw_file': T + 'aws_sagemaker_checkpoints.html.txt',
     'agent_note': 'What the provider leaves to the user: which state is saved, and how often. Without checkpoints, jobs are '
                   'capped to limit wasted work. This is the gap a lossless-pause construction speaks to (state closure), but '
                   'the record shows it as a construction (K2), not as something the platform lacks.'},
    {'id': 'm2:8', 'application': 'AP2', 'role': 'who_does_it',
     'source': 'SkyPilot documentation, "Managed Jobs"',
     'version': 'docs.skypilot.ai "latest" (requested at docs.skypilot.co, redirected); undated',
     'url': 'https://docs.skypilot.co/en/latest/examples/managed-jobs.html',
     'quote': ['Automatically recovering from failures (job preemptions, GPU errors, node crashes, etc.) and retrying '
               'application errors.',
               'to save ~70% on GPU costs while maintaining reliability through automatic preemption recovery.',
               'To recover quickly from failures (hardware issues, preemptions, etc.), your job should checkpoint its state '
               'periodically to persistent storage.'],
     'raw_file': T + 'skypilot_managed_jobs.html.txt',
     'agent_note': 'Open-source, multi-cloud preemption recovery for training. Recovery relaunches the job; the job must '
                   'checkpoint itself. The ~70% is the project\'s own cost claim.'},
    {'id': 'm2:9', 'application': 'AP2', 'role': 'what_is_hard',
     'source': 'Amazon EC2 User Guide, "Spot Instance interruption notices"',
     'version': 'AWS documentation page, undated; re-fetched 2026-09-30, same sha256 as the DR1 F4 copy of 2026-09-30 00:08 UTC',
     'url': 'https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-instance-termination-notices.html',
     'quote': ['A Spot Instance interruption notice is a warning that is issued two minutes before Amazon EC2 stops or '
               'terminates your Spot Instance.',
               'Interruption notices are emitted on a best effort basis.'],
     'raw_file': V + 'aws_spot_notices.html.txt',
     'agent_note': 'Reused from docs/citations/dr1_f4_2026-09-29.md. The pause is imposed with two minutes\' warning at best; '
                   'Google Cloud Spot VMs default to no dedicated notice and a best-effort shutdown of up to 30 s (DR1 F4, '
                   're-checked today: reachable), and Azure Spot VMs give scheduled events "on a best effort basis up to 30 '
                   'seconds prior to the eviction" (azure_spot_vms, fetched today, not quoted as a claim). A pause that needs '
                   'a save must fit that window, or the state it saves periodically is the state it resumes from.'},
    {'id': 'm2:10', 'application': 'AP2', 'role': 'what_is_hard',
     'source': 'Thorpe et al., Bamboo: Making Preemptible Instances Resilient for Affordable Training of Large DNNs (NSDI 2023)',
     'version': 'arXiv 2204.12013v1, 26 Apr 2022 (only version; re-checked 2026-09-30)', 'url': 'https://arxiv.org/abs/2204.12013v1',
     'quote': ['While AWS spot instances have 2 minutes before preemption, GCP and Azure provide only 30 seconds, with GCP '
               'not even guaranteeing such a warning. For large models, this can be too short of a warning and may not leave '
               'sufﬁcient time to save model updates into a checkpoint.'],
     'raw_file': U + 'bamboo_2204.12013v1.txt',
     'agent_note': 'Reused from DR1 F4. The difficulty is the save inside the notice for large models; a small on-device or '
                   'fine-tuning state is a different regime (the passage gives no size threshold).'},
    {'id': 'm2:11', 'application': 'AP2', 'role': 'what_is_hard',
     'source': 'Wu et al., RLBoost: Harvesting Preemptible Resources for Cost-Efficient Reinforcement Learning on LLMs',
     'version': 'arXiv 2510.19225v3, 8 Apr 2026 (v1 22 Oct 2025)', 'url': 'https://arxiv.org/abs/2510.19225v3',
     'quote': ['These preemptible and fragmented resources, while poorly suited for training, align well with the rollout '
               'stage’s embarrassingly parallel and stateless nature.'],
     'raw_file': T + 'pdf_2510.19225v3.pdf.txt',
     'agent_note': 'A 2025-26 design choice: keep the stateful training step on reserved GPUs and put only stateless work on '
                   'preemptible capacity. It says interruptible compute is used where there is no state to lose, which is the '
                   'difficulty AP2 names.'},
    {'id': 'm2:12', 'application': 'AP2', 'role': 'what_is_hard',
     'source': 'PyTorch documentation, "torchrun (Elastic Launch)"',
     'version': 'PyTorch 2.14 docs, "Created On: May 12, 2026 | Last Updated On: May 12, 2026" (docs/stable redirects to 2.14)',
     'url': 'https://docs.pytorch.org/docs/2.14/elastic/run.html',
     'quote': ['all existing workers are stopped, a new WorkerGroup is formed, and all workers are started with a new RANK and',
               'DO NOT hard code assumptions about WORLD_SIZE as the world size can change as nodes are allowed to leave and join.'],
     'raw_file': T + 'pytorch_torchrun_2.14.html.txt',
     'agent_note': 'Elastic training is standard: a node leaving stops and restarts every worker under a new world size, and the '
                   'script is told to reload its checkpoint. A resume under a new world size is not the same trajectory '
                   '(OPEN-1B: "Changing the number of data parallel workers results in different batch orderings", '
                   'Lossless_Pause training dossier). The first quote ends at the tag boundary before "WORLD_SIZE".'},
    {'id': 'm2:13', 'application': 'AP2', 'role': 'who_does_it',
     'source': 'Emerald AI (Sivaram), "Sharing our Strategic Expansion Round: Emerald AI Raises $25 Million ..." (company blog)',
     'version': 'blog post dated March 31, 2026; re-fetched 2026-09-30, same sha256 as the DR1 F1 copy',
     'url': 'https://www.emeraldai.co/blog/sharing-our-strategic-expansion-round-emerald-ai-raises-25-million-to-transform-ai-data-centers-into-flexible-power-grid-assets',
     'quote': ['Temporal Flexibility: Slowing or pausing AI workloads such as fine-tuning runs that have some '
               'customer-designated flexibility on completion time.'],
     'raw_file': V + 'emerald_2026.html.txt',
     'agent_note': 'Reused from docs/citations/dr1_f1_2026-09-29.md. Pausing fine-tuning for the grid is a commercial offer in '
                   '2026, with flexibility set by the customer as a completion-time tolerance. Company announcement.'},
    {'id': 'm2:14', 'application': 'AP2', 'role': 'who_does_it',
     'source': 'Colangelo et al. (Emerald AI, NVIDIA, SRP, EPRI), Turning AI Data Centers into Grid-Interactive Assets: '
               'Results from a Field Demonstration in Phoenix, Arizona',
     'version': 'arXiv 2507.00909v1, 1 Jul 2025 (only version; re-checked 2026-09-30)', 'url': 'https://arxiv.org/abs/2507.00909v1',
     'quote': ['the trial achieved a 25% reduction in cluster power usage for three hours during peak grid events while '
               'maintaining AI quality of service (QoS) guarantees.',
               '(b) job pausing (de-prioritization), which temporarily pauses running jobs for steep reductions in power',
               'Both pausing and re-allocating resources for running jobs require checkpointing for training jobs to ensure '
               'forward progress and minimize the overhead associated with these knobs.',
               'we are able to treat checkpointing overhead as negligible for our relatively infrequent demand response events '
               'since training jobs often run for days (or even weeks) at a time.'],
     'raw_file': U + 'colangelo_2507.00909v1.txt',
     'agent_note': 'Reused from EPS2 and DR1 F1. A field demonstration in which pausing training jobs is one of the power '
                   'knobs. Checkpoint cost is called negligible only because events are rare; frequent events (AP9-style '
                   'carbon following) are the case it does not cover.'},
    {'id': 'm2:15', 'application': 'AP2', 'role': 'regulation',
     'source': 'Texas Senate Bill 6, 89th Legislature (Regular Session), enrolled version',
     'version': 'enrolled bill text (2025); re-fetched 2026-09-30, same sha256 as the DR1 F5 copy',
     'url': 'https://capitol.texas.gov/tlodocs/89R/billtext/html/SB00006F.htm',
     'quote': ['develops a protocol, including the installation of any necessary equipment or technology before the customer '
               'is interconnected, to allow the load to be curtailed during firm load shed.',
               'to develop a reliability service to competitively procure demand reductions from large load customers with a '
               'demand of at least 75 megawatts to be deployed in the event of an anticipated emergency condition.'],
     'raw_file': U + 'tx_sb6_enrolled.txt',
     'agent_note': 'Reused from docs/citations/dr1_f5_2026-09-29.md. In ERCOT, curtailability is a condition of connecting a '
                   'new large load, and emergency demand reduction is a procured service. A training cluster there must be '
                   'able to stop; the statute says nothing about how the job pauses or what it loses.'},

    # ------------------------------------------------------------------ AP3: "stop learning from me" and exact resume
    {'id': 'm2:16', 'application': 'AP3', 'role': 'who_does_it',
     'source': 'Hugging Face Transformers documentation, Trainer (TrainingArguments: Resuming Training)',
     'version': 'Transformers docs (version selector shows v5.17.0), fetched 2026-09-30',
     'url': 'https://huggingface.co/docs/transformers/main_classes/trainer',
     'quote': ['When resuming training, skip fast-forwarding through the dataset to reach the previous state.',
               '(slower resume but exact continuation)'],
     'raw_file': T + 'hf_trainer.html.txt',
     'agent_note': 'The Hugging Face Trainer\'s default resume path is documented as an exact continuation '
                   '(ignore_data_skip=False). Real_World/RW1.md reads HF Trainer resume as an empty cut on GPT-2 and a Qwen '
                   'pilot (a construction). A user-facing "stop learning from me" switch would sit on this machinery; the page '
                   'names no such switch.'},
    {'id': 'm2:17', 'application': 'AP3', 'role': 'what_is_hard',
     'source': 'Hugging Face Transformers documentation, Trainer (TrainingArguments)',
     'version': 'Transformers docs (version selector shows v5.17.0), fetched 2026-09-30',
     'url': 'https://huggingface.co/docs/transformers/main_classes/trainer',
     'quote': ['(faster resume but results won’t match interrupted training)',
               'Save only model weights, not optimizer/scheduler/RNG state. Significantly reduces checkpoint size but prevents '
               'resuming training from the checkpoint.'],
     'raw_file': T + 'hf_trainer.html.txt',
     'agent_note': 'Two documented ways to lose exactness: a fast resume that restarts the data order, and a weights-only '
                   'checkpoint that cannot resume at all. Exact resume costs checkpoint size and resume time.'},
    {'id': 'm2:18', 'application': 'AP3', 'role': 'who_does_it',
     'source': 'PyTorch, torchdata "Stateful DataLoader"',
     'version': 'TorchData 0.11.0 documentation (beta; docs.pytorch.org/data/beta redirects to meta-pytorch.org/data/beta)',
     'url': 'https://docs.pytorch.org/data/beta/torchdata.stateful_dataloader.html',
     'quote': ['StatefulDataLoader is a drop-in replacement for torch.utils.data.DataLoader which offers state_dict / '
               'load_state_dict methods for handling mid-epoch checkpointing',
               'By default, the state includes the number of batches yielded and uses this to naively fast-forward the '
               'sampler (map-style) or the dataset (iterable-style).'],
     'raw_file': T + 'torchdata_stateful_dataloader.html.txt',
     'agent_note': 'The data-order state, the part of a resume that CheckFreq (Lossless_Pause training dossier) found missing '
                   'in 2021, is now a library component. "Naively fast-forward" re-reads data to reach the position.'},
    {'id': 'm2:19', 'application': 'AP3', 'role': 'our_method_relevance',
     'source': 'Mitra, When Is Availability-Aware Training Worth It? A Benchmark and Empirical Study of Interruption-Resilient '
               'Optimization Under Predictable Compute Schedules',
     'version': 'arXiv 2609.22087v1 (abstract page "Submitted on 22 Jun 2026"; re-checked 2026-09-30)',
     'url': 'https://arxiv.org/abs/2609.22087v1',
     'quote': ['A baseline that preserves full optimizer state across a gap and advances its learning-rate schedule '
               'ineffective(active) time, not wall-clock time, reproduces uninterrupted training almost perfectly.',
               'Checkpoint(weak): preserve( θ,m,BN stats )across a gap but index the learning-rate schedule on wall-clocktime t. '
               'The schedule advances during idle gaps, over-annealing the learning rate at resumption.',
               '(B) when the data distribution drifts across the gap so that preserved state is stale.'],
     'raw_file': U + 'mitra_2609.22087v1.txt',
     'agent_note': 'Reused from docs/citations/sweep_prior_art_2026-09-25.md (P7); Lossless_Pause/checks/grade_sweep.txt reads '
                   'it as stating C4, the empty-cut checklist, which is graded REDUNDANT. It states the record\'s pause '
                   'construction (full state, schedule on active steps) as the honest baseline, and names wall-clock keying as '
                   'the failure and drift across the gap as the remaining cost. So the record\'s method addresses the '
                   'difficulty, and so does published practice. Spacing ("ineffective(active)", "wall-clocktime") is as '
                   'extracted.'},
    {'id': 'm2:20', 'application': 'AP3', 'role': 'what_is_hard',
     'source': 'PyTorch documentation, "Reproducibility" notes',
     'version': 'PyTorch 2.14 docs; re-fetched 2026-09-30 (first read in the Lossless_Pause training dossier, 2026-09-25)',
     'url': 'https://docs.pytorch.org/docs/2.14/notes/randomness.html',
     'quote': ['Completely reproducible results are not guaranteed across PyTorch releases, individual commits, or different '
               'platforms.'],
     'raw_file': V + 'pytorch_randomness.html.txt',
     'agent_note': '"Resumes exactly" holds on one software and hardware stack. A switch that must resume exactly after a '
                   'software update or a device change is a harder promise than a pause on the same stack.'},

    # ------------------------------------------------------------------ AP4: operator-interruptible continual agents
    {'id': 'm2:21', 'application': 'AP4', 'role': 'who_does_it',
     'source': 'LangChain, LangGraph documentation, "Interrupts"',
     'version': 'docs.langchain.com (LangGraph OSS, Python), page dateModified 2026-09-29', 'url': 'https://docs.langchain.com/oss/python/langgraph/interrupts',
     'quote': ['The interrupt function pauses graph execution and returns a value to the caller. When you call interrupt within '
               'a node, LangGraph saves the current graph state and waits for you to resume execution with input.',
               'Checkpointing keeps your place: the checkpointer writes the exact graph state so you can resume later, even '
               'when in an error state.'],
     'raw_file': T + 'langgraph_interrupts.html.txt',
     'agent_note': 'Human-in-the-loop pause and resume of an LLM agent, with persisted state, is a standard framework feature. '
                   'It pauses the agent\'s execution; it says nothing about learning or about the agent\'s incentives.'},
    {'id': 'm2:22', 'application': 'AP4', 'role': 'what_is_hard',
     'source': 'LangChain, LangGraph documentation, "Interrupts" (Rules of interrupts)',
     'version': 'docs.langchain.com, page dateModified 2026-09-29', 'url': 'https://docs.langchain.com/oss/python/langgraph/interrupts',
     'quote': ['The node restarts from the beginning of the node where the interrupt was called when resumed, so any code '
               'before the interrupt runs again',
               'Because interrupts work by re-running the nodes they were called from, side effects called before interrupt '
               'should (ideally) be idempotent.',
               'If interrupt is called after that call is made, it will be re-run multiple times when the node is resumed, '
               'potentially overwriting the initial update or creating duplicate records.'],
     'raw_file': T + 'langgraph_interrupts.html.txt',
     'agent_note': 'The resume is not state-closed at the node level: work before the pause is replayed, and the world may be '
                   'written twice. This is the world-content half of a pause (Empty_Cut_Engineering: state closure and the '
                   'world), which the record shows as a construction, not as a fix for this framework.'},
    {'id': 'm2:23', 'application': 'AP4', 'role': 'who_does_it',
     'source': 'Google Cloud documentation, "About GKE Agent Substrate"',
     'version': 'page "Last updated 2026-09-24 UTC"; re-fetched 2026-09-30 (first read in sweep_transformer_state, 2026-09-25)',
     'url': 'https://docs.cloud.google.com/kubernetes-engine/ai-ml/about-agent-substrate',
     'quote': ['an agent\'s working memory and files are preserved across sessions. The agent resumes from the exact point it paused.',
               'open network connections (such as database sessions or connections to MCP servers) aren\'t preserved when an '
               'agent suspends. Your agent code must handle reconnecting to external services when the agent resumes.',
               'gVisor can\'t snapshot live CUDA contexts.'],
     'raw_file': V + 'gke_agent_substrate.html.txt',
     'agent_note': 'A managed suspend and resume for agents on Kubernetes (2026). It lists what is kept (memory, files) and '
                   'what is not (connections, live GPU contexts); the agent\'s relation to the outside world is left to the '
                   'agent. No statement about oversight incentives.'},

    # ------------------------------------------------------------------ AP5: privacy-regulated continual learning
    {'id': 'm2:24', 'application': 'AP5', 'role': 'who_does_it',
     'source': 'Google Privacy Sandbox, "On-Device Personalization" (technical explainer), data model',
     'version': 'Privacy Sandbox documentation page, "Last updated 2025-12-18 UTC"',
     'url': 'https://privacysandbox.google.com/protections/on-device-personalization',
     'quote': ['Each raw data source will be stored either on the device or server-side, enabling local learning and inference.',
               'in a device-centric infrastructure, all raw data from the end-user tower remains at its origin, while the '
               'business\'s data remains stored on servers.'],
     'raw_file': T + 'odp_overview.html.txt',
     'agent_note': 'The deployed privacy answer is locality (raw data stays on the device), not the absence of stored examples '
                   'that AP5 names. M2 is an infrastructure family; the privacy and erasure sources are M3\'s.'},
    {'id': 'm2:25', 'application': 'AP5', 'role': 'what_is_hard',
     'source': 'Wan et al., ByteCheckpoint: A Unified Checkpointing System for Large Foundation Model Development (NSDI 2025)',
     'version': 'arXiv 2407.20143v4, 2 Apr 2025 (re-checked 2026-09-30)', 'url': 'https://arxiv.org/abs/2407.20143v4',
     'quote': ['CPU states include dataloader module, Random Number Generator (RNG) state, global training step number, and '
               'learning-rate scheduler, all stored in CPU memory.',
               'Our dataloader module incorporates a token buffer to cache input samples of varying lengths read from the data '
               'sources',
               'the token buffers should be copied to the destination workers for bitwise-correct resuming.'],
     'raw_file': U + 'bytecheckpoint_2407.20143v4.txt',
     'agent_note': 'Reused from the Lossless_Pause training dossier. The agent\'s inference, not the source\'s claim: the state '
                   'that makes a resume bit-exact can include buffered raw training samples, so an exact-resume checkpoint is '
                   'itself a store of training data. Exact resume (K2) and "no raw examples kept" (K4) pull against each other '
                   'unless the buffer is excluded or drained at the pause.'},

    # ------------------------------------------------------------------ AP6: robot and drone on-board adaptation
    {'id': 'm2:26', 'application': 'AP6', 'role': 'who_does_it',
     'source': 'ROS 2 design article, "Managed nodes" (node life cycle), Biggs and Foote',
     'version': 'design.ros2.org article, "Date Written: 2015-06, Last Modified: 2021-02"',
     'url': 'https://design.ros2.org/articles/node_lifecycle.html',
     'quote': ['To transition out of a primary state requires action from an external supervisory process, with the exception of '
               'an error being triggered in the Active state.',
               'This state represents a node that is not currently performing any processing.',
               'In the inactive state, any data that arrives on managed topics will not be read and or processed. Data '
               'retention will be subject to the configured QoS policy for the topic.'],
     'raw_file': T + 'ros2_node_lifecycle.html.txt',
     'agent_note': 'Robot middleware provides a supervised pause state for any node, which an on-board learner could use. What '
                   'happens to the world\'s data during the pause is a per-topic QoS setting, i.e. the content of the pause is '
                   'configured, not given. Nothing on learning.'},
    {'id': 'm2:27', 'application': 'AP6', 'role': 'what_is_hard',
     'source': 'PX4 Autopilot User Guide, "Safety Configuration (Failsafes)"',
     'version': 'PX4 User Guide, "main" branch docs, fetched 2026-09-30', 'url': 'https://docs.px4.io/main/en/config/safety.html',
     'quote': ['The Data Link Loss failsafe is triggered if the connection to the last MAVLink ground station like QGroundControl '
               'is lost.',
               'This must be kept short because the vehicle will continue to fly using the last known stick position until the '
               'timeout triggers.'],
     'raw_file': T + 'px4_safety.html.txt',
     'agent_note': 'A lost link is handled by a configured failsafe action; the vehicle does not stop while the loss is being '
                   'detected. For AP6 the difficulty is that the physical system keeps moving during a "pause"; the learner\'s '
                   'pause and the vehicle\'s are different things. Robotics sources proper are P5\'s (Robotics/).'},

    # ------------------------------------------------------------------ AP7: federated continual learning, clients offline
    {'id': 'm2:28', 'application': 'AP7', 'role': 'who_does_it',
     'source': 'Bonawitz et al. (Google), Towards Federated Learning at Scale: System Design (SysML 2019)',
     'version': 'arXiv 1902.01046v2, 22 Mar 2019', 'url': 'https://arxiv.org/abs/1902.01046v2',
     'quote': ['The server needs to work with the fact that many devices drop out during computation, and that availability of '
               'FL devices varies drastically over time.',
               'on average the portion of devices that drop out due to computation errors, network failures, or changes in '
               'eligibility varies between 6% and 10%.',
               'the server typically selects 130% of the target number of devices to initially participate.'],
     'raw_file': T + 'pdf_1902.01046v2.pdf.txt',
     'agent_note': 'Production federated learning handles clients that go offline mid-round by over-selecting and discarding '
                   'the missing ones. A dropped client\'s work is lost, not paused.'},
    {'id': 'm2:29', 'application': 'AP7', 'role': 'what_is_hard',
     'source': 'Garg et al., Robust Federated Learning Under Real-World Client Churn (FeLiX)',
     'version': 'arXiv 2607.06979v1, 8 Jul 2026', 'url': 'https://arxiv.org/abs/2607.06979v1',
     'quote': ['Mobile and edge devices are intermittently reachable due to battery, network, and user behavior.',
               'report mean client availability ranging from as low as 15% to roughly 50% of the total population.',
               'in the Google FL system, nearly 22% of updates arrive too late for aggregation and are rejected, while another '
               '2% are interrupted mid-computation.',
               'it can detect mid-round drop-offs—which affected 6–8% of all selections in our traces—and trigger an immediate '
               'replacement.'],
     'raw_file': T + 'pdf_2607.06979v1.pdf.txt',
     'agent_note': '2026 statement that client unavailability is the norm, with production figures quoted from other systems '
                   '(Google FL, PAPAYA, FLINT). The 22%/2% sentence is FeLiX\'s statement about the Google FL system and '
                   'carries no citation of its own; the paper\'s reference for that system is Bonawitz et al. (m2:28). '
                   'The remedy is replacement and delay-aware aggregation, not a pause of the client\'s learning. The '
                   '"traces" of the last quote are the paper\'s own experiments.'},

    # ------------------------------------------------------------------ AP8: exact rollback and audit
    {'id': 'm2:30', 'application': 'AP8', 'role': 'who_does_it',
     'source': 'Chowdhery et al. (Google), PaLM: Scaling Language Modeling with Pathways',
     'version': 'arXiv 2204.02311v5, 5 Oct 2022 (v1 5 Apr 2022)', 'url': 'https://arxiv.org/abs/2204.02311v5',
     'quote': ['We re-started training from a checkpoint roughly 100 steps before the spike started, and skipped roughly 200–500 '
               'data batches, which cover the batches that were seen before and during the spike.'],
     'raw_file': T + 'pdf_2204.02311v5.pdf.txt',
     'agent_note': 'Rollback to an earlier checkpoint is routine practice at frontier scale. The rollback here changes the '
                   'data (batches skipped), so it restores the weights, not the trajectory.'},
    {'id': 'm2:31', 'application': 'AP8', 'role': 'who_does_it',
     'source': 'Donaghy et al. (Gensyn), OPEN-1B: A Fully Auditable Training Run',
     'version': 'arXiv 2609.17380v1, 15 Sep 2026 (re-checked 2026-09-30)', 'url': 'https://arxiv.org/abs/2609.17380v1',
     'quote': ['this makes the entire training run bit-exact under replay, independent of device count and topology, enabling '
               'third-party audit of any training segment.'],
     'raw_file': U + 'open1b_2609.17380v1.txt',
     'agent_note': 'Reused from the Lossless_Pause training dossier. Bit-exact replay for audit is published and demonstrated '
                   'at 1B scale in 2026; Lossless_Pause/LOSSLESS_PAUSE.md reads it as the exception to prediction D1 '
                   '(bitwise training holds only on the same hardware, software and layout).'},
    {'id': 'm2:32', 'application': 'AP8', 'role': 'what_is_hard',
     'source': 'Donaghy et al. (Gensyn), OPEN-1B: A Fully Auditable Training Run',
     'version': 'arXiv 2609.17380v1, 15 Sep 2026', 'url': 'https://arxiv.org/abs/2609.17380v1',
     'quote': ['Determinism does not imply reproducibility. A training run can be perfectly repeatable on its own GPU while '
               'disagreeing with an identical run on a processor or a different GPU model. A framework’s deterministic mode '
               'addresses only the first case.',
               'We trade off compute performance for reproducibility.'],
     'raw_file': U + 'open1b_2609.17380v1.txt',
     'agent_note': 'A restore point is "true" only on the same stack, unless one pays for reproducible kernels (the same '
                   'section reports the performance cost; the Lossless_Pause dossier quotes it).'},
    {'id': 'm2:33', 'application': 'AP8', 'role': 'what_is_hard',
     'source': 'Ma (Harvard), Pei, Lausen, Karypis (Amazon Web Services), Understanding Silent Data Corruption in LLM Training',
     'version': 'arXiv 2502.12340v1, 17 Feb 2025', 'url': 'https://arxiv.org/abs/2502.12340v1',
     'quote': ['SDCs can lead models to converge to different optima with different weights and even cause spikes in the '
               'training loss.',
               'It indicates that before a loss spike appears, SDCs may have already affected model training for an unknown period.'],
     'raw_file': T + 'pdf_2502.12340v1.pdf.txt',
     'agent_note': 'Hardware faults corrupt state silently, so the last checkpoint before a visible failure may already be '
                   'bad. Exact restore of a corrupted state restores the corruption; knowing which checkpoint is clean is the '
                   'hard part, and state closure does not answer it.'},
    {'id': 'm2:34', 'application': 'AP8', 'role': 'what_is_hard',
     'source': 'Xia et al., TrainSDC: Characterizing and Mitigating Silent Data Corruption in Large Language Model Training',
     'version': 'arXiv 2608.30769v1, 31 Aug 2026', 'url': 'https://arxiv.org/abs/2608.30769v1',
     'quote': ['The damage may become visible only later as a loss spike or failed convergence, or remain hidden while degrading '
               'final model quality',
               'The online window persists within an uninterrupted training process but is not stored in the ordinary '
               'model/optimizer checkpoint.'],
     'raw_file': T + 'pdf_2608.30769v1.pdf.txt',
     'agent_note': 'The second quote is an instance of a checkpoint that is not state-closed: the protection\'s own running '
                   'state is outside the model/optimizer checkpoint, so a restart does not return the whole system to where '
                   'it was (the authors say their main runs were uninterrupted). Auxiliary state is where "every checkpoint '
                   'is a true restore point" fails in practice.'},

    # ------------------------------------------------------------------ AP9: training scheduled against carbon intensity
    {'id': 'm2:35', 'application': 'AP9', 'role': 'who_does_it',
     'source': 'Green Software Foundation, Green Software Patterns, "Use carbon-aware scheduling and region selection for AI workloads"',
     'version': 'patterns.greensoftware.foundation page, undated', 'url': 'https://patterns.greensoftware.foundation/operations/carbon-aware-ai-scheduling/',
     'quote': ['Pause and resume long-running training jobs based on carbon intensity thresholds where feasible',
               'Energy consumption remains largely unchanged for the same workload, though pausing and resuming may introduce '
               'minor checkpoint overhead.'],
     'raw_file': T + 'gsf_carbon_aware_ai_scheduling.html.txt',
     'agent_note': 'Pausing training on a carbon signal is an industry-body recommended pattern. The pattern itself says energy '
                   'is unchanged: the gain is in carbon intensity (when), not in energy (how much).'},
    {'id': 'm2:36', 'application': 'AP9', 'role': 'what_is_hard',
     'source': 'Green Software Foundation, Green Software Patterns, "Use carbon-aware scheduling and region selection for AI workloads" (Considerations)',
     'version': 'patterns.greensoftware.foundation page, undated', 'url': 'https://patterns.greensoftware.foundation/operations/carbon-aware-ai-scheduling/',
     'quote': ['Pausing and resuming training may introduce checkpoint overhead and minor efficiency loss',
               'Organizational SLAs and deadlines may constrain scheduling flexibility'],
     'raw_file': T + 'gsf_carbon_aware_ai_scheduling.html.txt',
     'agent_note': 'The two stated costs of carbon-following pauses: the checkpoint and the deadline. A pause that costs nothing '
                   'but time addresses the first; the second is untouched.'},
    {'id': 'm2:37', 'application': 'AP9', 'role': 'who_does_it',
     'source': 'Green Software Foundation, Carbon Aware SDK documentation, "Overview"',
     'version': 'carbon-aware-sdk.greensoftware.foundation docs, undated', 'url': 'https://carbon-aware-sdk.greensoftware.foundation/docs/overview',
     'quote': ['Companies including UBS and Vestas have already deployed the Carbon Aware SDK to build greener software',
               'By moving these workloads to a different time, the carbon emissions from the ML training can be reduced by up to '
               '15%, and by moving the location of the training this can be reduced even further, at times by up to 50% or more.'],
     'raw_file': T + 'casdk_overview.html.txt',
     'agent_note': 'Open-source tooling for time- and place-shifting is deployed. The percentages are the project\'s own "up to" '
                   'figures and cite no study on the page.'},
    {'id': 'm2:38', 'application': 'AP9', 'role': 'what_is_hard',
     'source': 'Dodge et al., Measuring the Carbon Intensity of AI in Cloud Instances (FAccT 2022)',
     'version': 'arXiv 2206.05229v1, 10 Jun 2022 (only version; re-checked 2026-09-30)', 'url': 'https://arxiv.org/abs/2206.05229v1',
     'quote': ['for very long runs like training a 6 billion parameter language model for 8 days (b), changing the start time '
               'by up to 24 hours leads to less than 1.5% reduction at best in any region.',
               'for very long runs like our 6 billion parameter language model training run in (b), which ran for 8 days, '
               'doubling the duration can lead to significant savings up to about 25%.'],
     'raw_file': U + 'dodge_2206.05229v1.txt',
     'agent_note': 'Reused from docs/citations/energy_accounting_2026-09-25.md (first quote). For long training runs, shifting the '
                   'start barely helps; pausing and resuming helps only if the job accepts a much longer wall-clock duration. '
                   'The difficulty is the deadline, not the pause mechanism.'},

    # ------------------------------------------------------------------ AP10: feeds that honour a user's pause
    {'id': 'm2:39', 'application': 'AP10', 'role': 'who_does_it',
     'source': 'YouTube Help, "View, delete, or turn on or off watch history"',
     'version': 'support.google.com help page (hl=en), undated', 'url': 'https://support.google.com/youtube/answer/95725?hl=en',
     'quote': ['YouTube watch history makes it easy to find videos you recently watched, and, when it’s turned on, allows us to '
               'give relevant video recommendations.',
               'Any videos that you watch while history is turned off won\'t show up in your history.',
               'Select Pause watch history or Clear all watch history'],
     'raw_file': T + 'youtube_watch_history.html.txt',
     'agent_note': 'A user-facing "stop learning from me" switch for a recommender exists and is named a pause. Outside M2\'s '
                   'infrastructure scope; recorded because AP10 needs a provider and M2 fetched it.'},
    {'id': 'm2:40', 'application': 'AP10', 'role': 'what_is_hard',
     'source': 'YouTube Help, "How YouTube recommendations work"',
     'version': 'support.google.com help page (hl=en), undated', 'url': 'https://support.google.com/youtube/answer/16089387?hl=en',
     'quote': ['To provide video recommendations on the homepage, our system primarily relies on your watch history. You can turn '
               'off and delete your watch history if you don’t prefer to have video recommendations on the homepage.',
               'If your YouTube watch history is off and you have no significant prior watch history, the homepage will continue '
               'to show the search bar and the left-side menu.'],
     'raw_file': T + 'youtube_how_recs_work.html.txt',
     'agent_note': 'Pausing the history removes homepage recommendations for a user with little history: the pause has a cost '
                   'to the user in the product as shipped. AP10 names exactly this (a pause "without penalising it"). The page '
                   'frames it as "a streamlined user experience". Attention_Algorithms/ holds the model-side reading.'},
]
