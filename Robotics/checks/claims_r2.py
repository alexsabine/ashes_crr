"""ROB1 stage 1, family R2 (Robotics/DECLARATION.md): robot learning. Generalist and foundation robot policies
(vision-language-action models), lifelong and continual robot learning, forgetting on adaptation, generalisation under
distribution shift and across embodiments, sim-to-real transfer, data scarcity and cost, long-horizon tasks, and
on-robot inference latency and compute.

Fetched 2026-09-30 through the session proxy. Every quote is copied from the text that pymupdf 1.28.2 extracted from the
fetched PDF (arXiv current version, per the abstract page's submission history), or, for the one web page (UC Berkeley
News), from a stdlib HTML-to-text extraction of the fetched page. Raw files live outside the repository under
/tmp/claude-0/rob_src/ (`raw_file` is relative to that root; this family's files are under r2/); their sha256 is in
/tmp/claude-0/rob_src/r2/SHA256SUMS.txt and in the dossier docs/citations/rob1_r2_2026-09-30.md. Table rows are quoted
as the extractor emitted them, cell by cell in reading order. Checked by Robotics/checks/verify.py.

Roles (DECLARATION.md stage 1): a = the problem stated; b = a 2025-26 statement that it is open, unsolved or a main
challenge; c = the best reported result on a named benchmark or metric against the target (a programme goal, a regulatory
requirement, a human baseline or an oracle; numbers quoted; the gap is computed in `agent_note` and in BOTTLENECKS); d = the
method families tried and the assumption each makes about time, clocks, boundaries, interruptions, memory or tuning.
`agent_note` is the agent's reading, not the source's words. Numbers from different papers are not comparable unless a note
says the protocol is shared. Where a source reports the target reached, it is recorded (role c) and said in the note.
"""

R = 'r2/txt/'

CLAIMS = [
    # ---------------- r2-B1: lifelong / continual robot learning: forgetting under sequential skill acquisition
    {'id': 'r2:1', 'bottleneck': 'r2-B1', 'role': 'a',
     'source': 'Liu, Zhu, Gao, Feng, Liu, Zhu & Stone, LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning (NeurIPS 2023 Datasets and Benchmarks)',
     'version': 'arXiv v2, 14 Oct 2023 (v1 5 Jun 2023)', 'url': 'https://arxiv.org/abs/2306.03310v2',
     'quote': ['the sequential nature of LLDM suggests that even minor forgetting over successive steps can potentially '
               'lead to a total failure in execution. As such, we consider the design of lifelong learning algorithms to be '
               'an open area of research in LLDM.',
               'we also implement sequential finetuning (SEQL) and multitask learning (MTL), which serve as a lower bound and '
               'upper bound for lifelong learning algorithms, respectively.'],
     'raw_file': R + '2306.03310v2.txt',
     'agent_note': 'The problem and the benchmark (2023, foundational; not used as B-b). MTL is named as the upper bound '
                   '(the oracle target); zero forgetting (NBT = 0) is the other natural target.'},
    {'id': 'r2:2', 'bottleneck': 'r2-B1', 'role': 'b',
     'source': 'Liu et al., Towards Long-Lived Robots: Continual Learning VLA Models via Reinforcement Fine-Tuning (LifeLong-RFT)',
     'version': 'arXiv v2, 16 May 2026 (v1 11 Feb 2026)', 'url': 'https://arxiv.org/abs/2602.10503v2',
     'quote': ['While such representations significantly reduce the data requirements for learning new tasks, directly '
               'applying SFT still results in severe catastrophic forgetting [47].',
               'However, these techniques struggle to scale to VLA settings involving both massive tasks and a high-capacity '
               'parameterization.'],
     'raw_file': R + '2602.10503v2.txt', 'agent_note': '2026 statement that forgetting under SFT adaptation of VLAs is open.'},
    {'id': 'r2:3', 'bottleneck': 'r2-B1', 'role': 'b',
     'source': 'Zeng et al., CRL-VLA: Continual Vision-Language-Action Learning',
     'version': 'arXiv v1, 3 Feb 2026', 'url': 'https://arxiv.org/abs/2602.03445v1',
     'quote': ['yet balancing stability (retaining old skills) and plasticity (learning new ones) remains a formidable '
               'challenge for existing methods.'],
     'raw_file': R + '2602.03445v1.txt', 'agent_note': '2026 statement (continual RL post-training of VLAs).'},
    {'id': 'r2:4', 'bottleneck': 'r2-B1', 'role': 'b',
     'source': 'Chen et al., PHASER: Phase-Aware and Semantic Experience Replay for Vision-Language-Action Models',
     'version': 'arXiv v2, 3 Jun 2026 (v1 2 Jun 2026)', 'url': 'https://arxiv.org/abs/2606.03598v2',
     'quote': ['deploying these models in open-ended environments requires continuously acquiring novel skills, a process '
               'that inevitably triggers severe catastrophic forgetting of previously learned behaviors.'],
     'raw_file': R + '2606.03598v2.txt', 'agent_note': '2026 statement.'},
    {'id': 'r2:5', 'bottleneck': 'r2-B1', 'role': 'b',
     'source': 'Nguyen et al., Self-Evolving AI for Humanoids: Mechanisms, Safety, and Evaluation of Post-Deployment Self-Improvement (survey)',
     'version': 'arXiv v1, 2 Sep 2026', 'url': 'https://arxiv.org/abs/2609.13236v1',
     'quote': ['The central challenge is therefore catastrophic forgetting.',
               'To our knowledge, no existing humanoid system explicitly enforces this type of monotonicity. We therefore view '
               'it as a necessary safety layer that remains largely an open problem rather than a solved one.'],
     'raw_file': R + '2609.13236v1.txt',
     'agent_note': '2026 survey statement for continual self-learning on a live sensorimotor stream; the second quote is '
                   'about protecting safety-critical behaviours from forgetting.'},
    {'id': 'r2:6', 'bottleneck': 'r2-B1', 'role': 'b',
     'source': 'Lei et al., Dynamic Mixture of Progressive Parameter-Efficient Expert Library for Lifelong Robot Learning (DMPEL, TMLR 05/2026)',
     'version': 'arXiv v3, 28 May 2026 (v1 6 Jun 2025, v2 23 Sep 2025)', 'url': 'https://arxiv.org/abs/2506.05985v3',
     'quote': ['However, we still observe a gradual decline in performance as the number of tasks increases.'],
     'raw_file': R + '2506.05985v3.txt',
     'agent_note': '2026 statement on the ultra-long sequence (K = 30 LIBERO tasks); the per-task curves are figures only.'},
    {'id': 'r2:7', 'bottleneck': 'r2-B1', 'role': 'c',
     'source': 'Liu, Kim, Liu, Liu & Zhu, Pretrained Vision-Language-Action Models are Surprisingly Resistant to Forgetting in Continual Learning (Tables 1 and 5)',
     'version': 'arXiv v2, 17 Mar 2026 (v1 4 Mar 2026)', 'url': 'https://arxiv.org/abs/2603.03818v2',
     'quote': ['Specifically, we found that simple Experience Replay (ER) works surprisingly well on VLAs, often achieving zero '
               'forgetting even with a small replay data size (e.g., 2% of training data in LIBERO benchmark suites).',
               'Table 5. Continual learning performance on LIBERO-10 for different replay buffer sample sizes: Average Success '
               'Rate (SR) and Negative Backward Transfer (NBT) for sample sizes 10, 100, and 1000.',
               'Pi0 0.576 ± 0.034 0.529 ± 0.035 0.584 ± 0.045 0.229 ± 0.066 0.563 ± 0.028 −0.068 ± 0.018',
               'GR00T 0.851 ± 0.007 0.766 ± 0.013 0.854 ± 0.011 0.525 ± 0.018 0.820 ± 0.017 0.059 ± 0.035',
               'Results are with sample size = 1000 (20% of dataset size per task), in accordance with LIBERO’s official setting.'],
     'raw_file': R + '2603.03818v2.txt',
     'agent_note': 'The strongest contrary evidence in this family, recorded as the best result. Target: zero forgetting '
                   '(NBT = 0). LIBERO-10 (the long suite), ER: at 1000 samples per task (20%) Pi0 NBT -0.068 and GR00T 0.059: '
                   'target reached (within noise). At 100 samples (2%) the best NBT is 0.229 (Pi0), GR00T 0.525; at 10 samples '
                   '0.529 and 0.766. So on LIBERO-10 the text\'s "zero forgetting ... 2%" does not hold; per the source\'s own '
                   'Table 5 the gap to NBT 0 is 0.229 at 2% and closed at 20%. The paper gives no multitask row.'},
    {'id': 'r2:8', 'bottleneck': 'r2-B1', 'role': 'c',
     'source': 'Chen et al., PHASER (Table 1)', 'version': 'arXiv v2, 3 Jun 2026', 'url': 'https://arxiv.org/abs/2606.03598v2',
     'quote': ['Table 1: Continual learning across three VLA backbones and two LIBERO suites. ASR ↑(50 rollouts ×10 '
               'tasks/cell after the final task); NBT ↓from 10×10 task-by-checkpoint matrix (Eq. (3)).',
               'ER 77.6 22.2 54.6 −5.6 51.6 46.7 31.4 35.6 39.4 47.8 33.0 33.3',
               'PHASER (Ours) 87.8 7.8 85.8 10.0 78.0 13.8 48.6 11.1 79.0 6.4 51.6 12.4',
               'Lower NBT indicates better retention, with NBT=0 implying zero forgetting.'],
     'raw_file': R + '2606.03598v2.txt',
     'agent_note': 'Columns: OpenVLA-OFT-7B (Goal ASR, NBT; Long ASR, NBT), QwenGR00T-3B (same), QwenOFT-3B (same). Best '
                   'final ASR on LIBERO-Long: 85.8 (OpenVLA-OFT-7B, NBT 10.0); with the 3B backbones whose action heads are '
                   'largely trained from scratch, 48.6 and 51.6. Target NBT 0: gaps 10.0 (7B), 11.1 and 12.4 (3B). A multitask '
                   'reference for OpenVLA-OFT on LIBERO-Long (91.1) exists only in another paper (claim r2:9), so the ASR gap '
                   '91.1 - 85.8 = 5.3 is CROSS-PAPER.'},
    {'id': 'r2:9', 'bottleneck': 'r2-B1', 'role': 'c',
     'source': 'Liu et al., LifeLong-RFT (Tables II, IV and V)', 'version': 'arXiv v2, 16 May 2026', 'url': 'https://arxiv.org/abs/2602.10503v2',
     'quote': ['TABLE IV: Continual learning performance on LIBERO.',
               'LIBERO-Long FWT (↑) – – 58.0 53.8 32.0 64.0 61.0 74.2 +13.2 NBT (↓) – – 21.0 14.2 14.1 31.4 17.3 12.8 -4.5 '
               'AUC (↑) – – 46.0 42.5 20.8 38.7 47.3 64.5 +17.2',
               'NORA-Long [26] RFT (Ours) 99.2 98.2 95.8 89.0 95.6',
               'OpenVLA-OFT [30] SFT 98.1 96.9 95.5 91.1 95.4',
               'In this stage, each new task consists of only 10 demonstrations, while 5 demonstrations per previously learned '
               'task are retained for Experience Replay (ER) [10, 35].',
               'Real-World FWT (↑) 58.8 46.3 56.3 80.0 +23.7 NBT (↓) 16.3 17.8 18.3 6.1 -12.2 AUC (↑) 47.9 35.1 44.2 75.9 +31.7'],
     'raw_file': R + '2602.10503v2.txt',
     'agent_note': 'Table IV columns: BUDS, LOTUS, SPECI (BC), pi0, OpenVLA, OpenVLA-OFT, NORA-Long (SFT), RFT (ours), delta. '
                   'LIBERO-Long continual (LOTUS protocol: 6 base tasks, then 4 new tasks with 10 demos each): best AUC 64.5, '
                   'NBT 12.8 (RFT). Table II (multitask, 50 demos per task): the same RFT model reaches 89.0 on LIBERO-Long. '
                   'Gap AUC 64.5 vs multitask 89.0 = 24.5 in one paper, but the data per task differ (10 vs 50 demos), so this '
                   'is an upper bound of the gap, not a like-for-like oracle. Real world (4 tasks, Table V): best NBT 6.1, '
                   'AUC 75.9; the multitask real-world overall is 87.5 (Table III).'},
    {'id': 'r2:10', 'bottleneck': 'r2-B1', 'role': 'c',
     'source': 'Wang, Fang, Shi & Zhou, OrthoSkillVLA: Continual Skill Learning via Gradient-Informed Skill Subspace Adaptation (PRCV 2026; Table 1)',
     'version': 'arXiv v1, 20 Aug 2026', 'url': 'https://arxiv.org/abs/2608.19589v1',
     'quote': ['We consider a replay-free continual skill learning setting where an embodied agent sequentially masters a '
               'repertoire of skills S = {S1, . . . , SK} without access to historical datasets.',
               'KeepLoRA [14] 0.90 ± 0.05 0.46 ± 0.16 0.72 ± 0.02 56.61 ± 7.22 OrthoSkillVLA 0.94 ± 0.03 0.13 ± 0.06 0.88 ± '
               '0.01 83.50 ± 1.42',
               'achieving an average success rate of 83.5% compared to the oracle’s 86.2%.'],
     'raw_file': R + '2608.19589v1.txt',
     'agent_note': 'Columns FWT, NBT, AUC, Final SR (%). Replay-free, three skills from LIBERO-100, averaged over three orders. '
                   'Final SR 83.50 against oracle routing (ground-truth skill identity) 86.2: gap 2.7 in the same paper; NBT '
                   '0.13 against 0. Small setting (three skills).'},
    {'id': 'r2:11', 'bottleneck': 'r2-B1', 'role': 'd',
     'source': 'Liu, Kim, Liu, Liu & Zhu (Pretrained VLAs resist forgetting)', 'version': 'arXiv v2, 17 Mar 2026', 'url': 'https://arxiv.org/abs/2603.03818v2',
     'quote': ['After completing policy learning for a task, ER stores a portion of that task’s data in a separate replay buffer.',
               'Sequential (Liu et al., 2023b), which simply carries over the model weights across tasks and continues '
               'finetuning on the current task data without any replay buffer, and (ii) EWC (Kirkpatrick et al., 2017a)'],
     'raw_file': R + '2603.03818v2.txt',
     'agent_note': 'Replay family: stored raw samples, written at the task boundary (boundary given), fixed buffer size per '
                   'task. Regularisation family (EWC): importance computed per finished task. Both assume given task '
                   'boundaries.'},
    {'id': 'r2:12', 'bottleneck': 'r2-B1', 'role': 'd',
     'source': 'Lei et al., DMPEL (TMLR 05/2026)', 'version': 'arXiv v3, 28 May 2026', 'url': 'https://arxiv.org/abs/2506.05985v3',
     'quote': ['During adaptation, we learn 10 epochs on each arriving task and evaluate every 2 epochs',
               'We perform expert coefficient replay for 10 epochs after each task.',
               'we prune underactivated low-rank experts every 10 tasks to control the linear growth of the library.',
               'Since TAIL requires oracle [...] task identifiers, we also provide the result of SeqFT (LoRA) to align with other methods.'],
     'raw_file': R + '2506.05985v3.txt',
     'agent_note': 'Expert-library (LoRA) family: a fixed epoch budget per arriving task, consolidation (coefficient replay) '
                   'after each task (boundary given), pruning on a task-count clock (every 10 tasks); some baselines need '
                   'oracle task identifiers.'},
    {'id': 'r2:13', 'bottleneck': 'r2-B1', 'role': 'd',
     'source': 'Chen et al., PHASER', 'version': 'arXiv v2, 3 Jun 2026', 'url': 'https://arxiv.org/abs/2606.03598v2',
     'quote': ['However, standard ER relies on a uniform sampling strategy that fundamentally misaligns with the temporal '
               'characteristics of robotic manipulation.',
               'an unsupervised change-point detector analyzes the low-level action signal to propose candidate temporal '
               'boundaries [10], with a following VLM processeing a subsampled trajectory video to semantically verify, '
               'refine, and label these candidates.'],
     'raw_file': R + '2606.03598v2.txt',
     'agent_note': 'Replay family, time assumption named: uniform sampling over clock time under-samples short phases; PHASER '
                   'allocates replay per phase, with phase boundaries from human annotation or from change points in the '
                   'action signal (Auto-PC). Task boundaries are still given.'},
    {'id': 'r2:14', 'bottleneck': 'r2-B1', 'role': 'd',
     'source': 'Nguyen et al., Self-Evolving AI for Humanoids (survey)', 'version': 'arXiv v1, 2 Sep 2026', 'url': 'https://arxiv.org/abs/2609.13236v1',
     'quote': ['Current humanoid controllers typically avoid this problem by training whole-body or manipulation policies in '
               'simulation or from demonstrations and then freezing them after deployment. As a result, neither further '
               'learning nor forgetting occurs [65, 11].'],
     'raw_file': R + '2609.13236v1.txt',
     'agent_note': 'The deployed default: freeze after deployment, so no on-robot adaptation at all (the problem avoided by '
                   'assumption).'},
    {'id': 'r2:15', 'bottleneck': 'r2-B1', 'role': 'b',
     'source': 'Liu et al., RoboFolDeX: A Physical-World Benchmark for Long-Horizon Robotic Manipulation of Deformable Objects',
     'version': 'arXiv v2, 18 Sep 2026 (v1 9 Sep 2026)', 'url': 'https://arxiv.org/abs/2609.10243v2',
     'quote': ['Direct joint training often introduces substantial interference in action generation, while continued '
               'training frequently causes the policy to forget previously acquired action behaviors.'],
     'raw_file': R + '2609.10243v2.txt', 'agent_note': '2026 real-robot observation (preliminary experiments, no table).'},

    # ---------------- r2-B2: fine-tuning a VLM into a VLA erodes the VLM's pretrained capabilities
    {'id': 'r2:16', 'bottleneck': 'r2-B2', 'role': 'a',
     'source': 'Hancock, Wu, Zha, Russakovsky & Majumdar, Actions as Language: Fine-Tuning VLMs into VLAs Without Catastrophic Forgetting (VLM2VLA)',
     'version': 'arXiv v1, 26 Sep 2025', 'url': 'https://arxiv.org/abs/2509.22195v1',
     'quote': ['learning to produce actions often diminishes the VLM’s foundational reasoning and multimodal understanding, '
               'hindering generalization to novel scenarios, instruction following, and semantic understanding.'],
     'raw_file': R + '2509.22195v1.txt', 'agent_note': 'The problem stated (2025).'},
    {'id': 'r2:17', 'bottleneck': 'r2-B2', 'role': 'b',
     'source': 'Dalal et al., Generalizable VLA Finetuning via Representation Anchoring and Language-Action Alignment (Anchor-Align)',
     'version': 'arXiv v2, 28 Sep 2026 (v1 15 Jul 2026)', 'url': 'https://arxiv.org/abs/2607.13429v2',
     'quote': ['However, BC finetuning progressively overwrites the pretrained representations that support visual and '
               'semantic generalization.',
               'In fact, BC finetuning corrupts the very prior that makes VLMs worth adapting, leading to two failure modes '
               'that persist even under good training practices.'],
     'raw_file': R + '2607.13429v2.txt', 'agent_note': '2026 statement.'},
    {'id': 'r2:18', 'bottleneck': 'r2-B2', 'role': 'b',
     'source': 'Liu et al., LifeLong-RFT', 'version': 'arXiv v2, 16 May 2026', 'url': 'https://arxiv.org/abs/2602.10503v2',
     'quote': ['However, Supervised Fine-Tuning (SFT), which serves as the primary mechanism for adapting VLAs to downstream '
               'domains, requires substantial amounts of task-specific data and is prone to catastrophic forgetting.'],
     'raw_file': R + '2602.10503v2.txt', 'agent_note': '2026 statement.'},
    {'id': 'r2:19', 'bottleneck': 'r2-B2', 'role': 'c',
     'source': 'Hancock et al., VLM2VLA (Table 1, multimodal understanding)', 'version': 'arXiv v1, 26 Sep 2025', 'url': 'https://arxiv.org/abs/2509.22195v1',
     'quote': ['Method #Params MMMU MMStar MME OCRBench MMB-en MMB-cn TextVQA DocVQA InfoVQA AI2D ChartQA RealWorldQA',
               'Gemma-3-12B-IT 12b 46.0 46.3 1182.3 75.0 76.9 74.7 68.9 80.6 50.4 78.5 55.1 50.6',
               'VLM2VLA (Ours) 12b 42.7 48.0 1391.7 63.9 68.5 67.6 64.9 78.4 46.2 74.0 58.3 43.3',
               'π0.5 3b 24.0 21.7 1061.9 6.8 6.8 0.3 10.0 4.6 7.7 27.0 5.1 2.7'],
     'raw_file': R + '2509.22195v1.txt',
     'agent_note': 'Target: the base VLM (Gemma-3-12B-IT) before action training. Best retention (VLM2VLA) is below the base '
                   'on 9 of 12 benchmarks: MMMU 42.7 vs 46.0 (-3.3), OCRBench 63.9 vs 75.0 (-11.1), MMB-en 68.5 vs 76.9 '
                   '(-8.4), MMB-cn 67.6 vs 74.7 (-7.1), TextVQA 64.9 vs 68.9 (-4.0), DocVQA 78.4 vs 80.6 (-2.2), InfoVQA 46.2 '
                   'vs 50.4 (-4.2), AI2D 74.0 vs 78.5 (-4.5), RealWorldQA 43.3 vs 50.6 (-7.3); ahead on MMStar, MME, ChartQA. '
                   'A co-trained generalist VLA (pi0.5, 3b) scores 0.3 to 27.0 on the text benchmarks (its own base VLM row '
                   'is not in this table).'},
    {'id': 'r2:20', 'bottleneck': 'r2-B2', 'role': 'd',
     'source': 'Hancock et al., VLM2VLA', 'version': 'arXiv v1, 26 Sep 2025', 'url': 'https://arxiv.org/abs/2509.22195v1',
     'quote': ['This alignment makes it possible to train VLAs solely with Low-Rank Adaptation (LoRA), thereby minimally '
               'modifying the VLM backbone and averting catastrophic forgetting.',
               'without expensive co-training on internet-scale VLM datasets.'],
     'raw_file': R + '2509.22195v1.txt',
     'agent_note': 'Families: low-rank adaptation of a frozen backbone (assumes a small parameter change suffices); '
                   'co-training with web VLM data (a fixed mixture ratio, tuned).'},
    {'id': 'r2:21', 'bottleneck': 'r2-B2', 'role': 'd',
     'source': 'Dalal et al., Anchor-Align', 'version': 'arXiv v2, 28 Sep 2026', 'url': 'https://arxiv.org/abs/2607.13429v2',
     'quote': ['Vision-Language Anchoring distills layer-wise representations from a frozen VLM copy to prevent this drift',
               'VLA-Adapter[Frozen] (Wang et al., 2025), which freezes the backbone, and MAPS (Huang et al., 2025), our '
               'reimplementation of module-wise proximity scheduling on VLA-Adapter',
               'Co-training + KI, our reimplementation of Knowledge Insulation (Driess et al., 2025) on VLA-Adapter'],
     'raw_file': R + '2607.13429v2.txt',
     'agent_note': 'Families: anchoring to a frozen copy of the pretrained VLM (the reference never moves), freezing the '
                   'backbone, proximity scheduling per module, co-training with gradient insulation. All take the '
                   'pretrained VLM as the fixed state to preserve.'},

    # ---------------- r2-B3: generalisation of VLA policies under distribution shift
    {'id': 'r2:22', 'bottleneck': 'r2-B3', 'role': 'a',
     'source': 'Fei et al., LIBERO-Plus: In-depth Robustness Analysis of Vision-Language-Action Models',
     'version': 'arXiv v3, 26 Dec 2025 (v1 15 Oct 2025, v2 24 Oct 2025)', 'url': 'https://arxiv.org/abs/2510.13626v3',
     'quote': ['Our analysis exposes critical weaknesses: models exhibit extreme sensitivity to perturbation factors, including '
               'camera viewpoints and robot initial states, with performance dropping from 95% to below 30% under modest '
               'perturbations.'],
     'raw_file': R + '2510.13626v3.txt', 'agent_note': 'The problem stated (2025).'},
    {'id': 'r2:23', 'bottleneck': 'r2-B3', 'role': 'b',
     'source': 'Zhou et al., LIBERO-PRO: Towards Robust and Fair Evaluation of Vision-Language-Action Models Beyond Memorization',
     'version': 'arXiv v2, 25 May 2026 (v1 4 Oct 2025)', 'url': 'https://arxiv.org/abs/2510.03827v2',
     'quote': ['Experimental results reveal that, although existing models achieve over 90% accuracy under the standard LIBERO '
               'evaluation, their performance collapses to 0.0% under our generalized setting.',
               'Overall, these results show that current VLA models, despite excelling on the standard LIBERO, lack true '
               'robustness and generalization'],
     'raw_file': R + '2510.03827v2.txt',
     'agent_note': '2025-26 statement. Main per-model results are a figure (Fig. 7); one number is in the text: pi0.5 0.38 '
                   'under position changes on libero-goal, OpenVLA and pi0 0.'},
    {'id': 'r2:24', 'bottleneck': 'r2-B3', 'role': 'b',
     'source': 'Morgan et al., Colosseum V2: Benchmarking Generalization for Vision-Language-Action Models (RA-L, accepted Sep 2026)',
     'version': 'arXiv v3, 18 Sep 2026 (v1 26 May 2026, v2 12 Sep 2026)', 'url': 'https://arxiv.org/abs/2605.27759v3',
     'quote': ['Despite the zero-shot perception and language capabilities of VLAs, their overall task performance often '
               'degrades under distribution shifts, revealing gaps in how these systems translate high-level understanding '
               'into robust behavior.',
               'Overall, Pose-Randomization remains a primary challenge for both models.'],
     'raw_file': R + '2605.27759v3.txt', 'agent_note': '2026 statement.'},
    {'id': 'r2:25', 'bottleneck': 'r2-B3', 'role': 'c',
     'source': 'Dalal et al., Anchor-Align (Tables 1 and 5)', 'version': 'arXiv v2, 28 Sep 2026', 'url': 'https://arxiv.org/abs/2607.13429v2',
     'quote': ['Table 1: Success rates on the LIBERO-PRO and LIBERO-Plus benchmarks.',
               'LAP (Zha et al., 2026) 93.2 95.0 12.4 66.9 88.1 99.2 54.0 72.6 92.5 95.5 76.1 81.8',
               'Anchor-Align VLA 97.0 96.2 22.6 71.9 87.2 99.6 59.1 96.3 97.4 99.0 96.9 90.3',
               'Anchor-Align VLA 98.4 99.8 97.2 90.8',
               'In the main paper (Tab. 1), we report robustness and generalization results on the LIBERO-Spatial suite'],
     'raw_file': R + '2607.13429v2.txt',
     'agent_note': 'Table 1 columns: LIBERO-PRO (Lang. Reph., Object Swap, Pos. Swap, Mean), LIBERO-Plus (Lang. Instr., Bg. '
                   'Text., Robot Init, Cam. View, Obj. Layout, Light Cond., Sensor Noise, Mean); Table 5 columns: Spatial, '
                   'Object, Goal, Long (unperturbed). Target: the same model unperturbed on LIBERO-Spatial, 98.4. Best under '
                   'position swap 22.6 (gap 75.8); robot initial state 59.1 (gap 39.3); LIBERO-PRO mean 71.9 (gap 26.5); '
                   'LIBERO-Plus mean 90.3 (gap 8.1). Fair reading: appearance axes are nearly closed (background 99.6, '
                   'lighting 99.0); spatial axes are not.'},
    {'id': 'r2:26', 'bottleneck': 'r2-B3', 'role': 'c',
     'source': 'Fei et al., LIBERO-Plus (Tables 1 and 2)', 'version': 'arXiv v3, 26 Dec 2025', 'url': 'https://arxiv.org/abs/2510.13626v3',
     'quote': ['Original Camera Robot Language Light Background Noise Layout',
               'OpenVLA-OFT 97.1 59.7 37.2 81.5 85.8 92.4 76.7 77.1',
               'OpenVLA-OFT_w 95.3 16.8 43.7 73.2 68.2 92.5 51.4 72.3',
               'UniVLA 95.2 4.3 50.3 71.8 59.1 80.0 25.3 34.3',
               'Ours 92.8 30.3 85.8 94.9 93.9 89.3 77.6 79.5'],
     'raw_file': R + '2510.13626v3.txt',
     'agent_note': 'Table 1 (success %, "Original" = unperturbed). OpenVLA-OFT: 97.1 unperturbed, 59.7 under camera change '
                   '(gap 37.4), 37.2 under robot initial state (gap 59.9). Best robot-initial-state cell in Table 1: 50.3 '
                   '(UniVLA, unperturbed 95.2, gap 44.9); OpenVLA-OFT_w 43.7 (unperturbed 95.3). Table 2 "Ours" (fine-tuned on >20,000 generalised '
                   'trajectories): total 79.5, robot 30.3. Supporting; the 2026 source (r2:25) is the best result.'},
    {'id': 'r2:27', 'bottleneck': 'r2-B3', 'role': 'c',
     'source': 'Morgan et al., Colosseum V2 (Sections V-C and V-D)', 'version': 'arXiv v3, 18 Sep 2026', 'url': 'https://arxiv.org/abs/2605.27759v3',
     'quote': ['Under this perturbation, the average decrease in success rate is 21.8% and 40.9% (Single-Arm, Bimanual) for ACT, '
               'and 12.9% and 51.4% for π0.5.',
               'Quantitatively, the mean of the success rates across all tasks with no perturbations is 29.2% and 44.5% for ACT '
               'on the Single-Arm and Bimanual test suites, respectively, compared to 21.2% and 12.6% for π0.5'],
     'raw_file': R + '2605.27759v3.txt',
     'agent_note': 'Supporting: on 28 new tasks even unperturbed success is low (best 44.5% bimanual, ACT; pi0.5 12.6%), and '
                   'pose randomisation removes a further 12.9 to 51.4 points.'},
    {'id': 'r2:28', 'bottleneck': 'r2-B3', 'role': 'd',
     'source': 'Fei et al., LIBERO-Plus', 'version': 'arXiv v3, 26 Dec 2025', 'url': 'https://arxiv.org/abs/2510.13626v3',
     'quote': ['Leveraging our highly automated generalization pipeline, we constructed an extensive training dataset com'
               'prising over 20,000 successful trajectories.',
               'models may be relying less on the language instruction than anticipated, potentially leveraging task cues '
               'from the visual context.'],
     'raw_file': R + '2510.13626v3.txt',
     'agent_note': 'Data-augmentation family: widen the training distribution (assumes the test shifts can be enumerated and '
                   'sampled in advance). Failure mode named: memorised visual context rather than instruction.'},
    {'id': 'r2:29', 'bottleneck': 'r2-B3', 'role': 'd',
     'source': 'Zhou et al., LIBERO-PRO', 'version': 'arXiv v2, 25 May 2026', 'url': 'https://arxiv.org/abs/2510.03827v2',
     'quote': ['Specifically, the evaluation tasks are identical to the training tasks, differing only by marginal '
               'perturbations in initial object states—variations so subtle as to be visually imperceptible.'],
     'raw_file': R + '2510.03827v2.txt',
     'agent_note': 'Evaluation assumption named: the standard protocol tests on the training tasks and layouts, so '
                   'memorisation scores as success.'},

    # ---------------- r2-B4: transfer to new embodiments
    {'id': 'r2:30', 'bottleneck': 'r2-B4', 'role': 'a',
     'source': 'Kawaharazuka, Oh, Yamada, Posner & Zhu, Vision-Language-Action Models for Robotics: A Review Towards Real-World Applications (IEEE Access)',
     'version': 'arXiv v1, 8 Oct 2025', 'url': 'https://arxiv.org/abs/2510.07077v1',
     'quote': ['While VLA models are increasingly trained on data from diverse robot embodiments, transferring policies '
               'across embodiments remains a major challenge.'],
     'raw_file': R + '2510.07077v1.txt', 'agent_note': 'The problem stated (2025; also a B-b statement).'},
    {'id': 'r2:31', 'bottleneck': 'r2-B4', 'role': 'b',
     'source': 'Domae et al., The Embodiment Gap in Robot Foundation Models (TMLR, August 2026)',
     'version': 'arXiv v1, 19 Aug 2026', 'url': 'https://arxiv.org/abs/2608.18433v1',
     'quote': ['These directions have expanded what can be shared. Substantial work still remains in turning shared structure '
               'into stable execution on the target robot.'],
     'raw_file': R + '2608.18433v1.txt', 'agent_note': '2026 survey statement.'},
    {'id': 'r2:32', 'bottleneck': 'r2-B4', 'role': 'b',
     'source': 'Liu et al., RoboFolDeX', 'version': 'arXiv v2, 18 Sep 2026', 'url': 'https://arxiv.org/abs/2609.10243v2',
     'quote': ['Differences in robot kinematics, camera configurations, control interfaces, and action representations lead '
               'to severe action-space interference and catastrophic forgetting.'],
     'raw_file': R + '2609.10243v2.txt', 'agent_note': '2026 real-robot observation (cross-embodiment joint and continued training).'},
    {'id': 'r2:33', 'bottleneck': 'r2-B4', 'role': 'c',
     'source': 'Yan et al., ZETA: A Controlled Study of Zero-Shot Cross-Embodiment VLA Transfer for Tabletop Manipulation (Tables 3 and 4)',
     'version': 'arXiv v2, 5 Sep 2026 (v1 2 Sep 2026)', 'url': 'https://arxiv.org/abs/2609.02546v2',
     'quote': ['State Action es APP GRP ARM FULL Average',
               'EEF-Delta EEF-Delta 91.5 ± 0.6 90.0 ± 1.1 78.3 ± 2.4 74.3 ± 0.9 60.4 ± 0.9 75.7 ± 1.3',
               'EEF-Delta EEF-Delta 100.0 97.5 92.5 87.5 81.9 89.9',
               'We score each rollout by task progress in [0, 100], with 100% denoting full completion'],
     'raw_file': R + '2609.02546v2.txt',
     'agent_note': 'Strict zero-shot transfer (target robot absent from all training). Columns: es (source embodiment), APP '
                   '(appearance-only), GRP (gripper-only), ARM (arm-only), FULL (full change), Average; mean task progress. '
                   'Target: progress on the source embodiment, same tasks. Simulation (Table 3, best representation): FULL '
                   '60.4 vs es 91.5 (gap 31.1), ARM 74.3 (gap 17.2). Real world (Table 4, 140 rollouts per model): FULL 81.9 '
                   'vs 100.0 (gap 18.1). The metric is progress with partial credit, not binary success.'},
    {'id': 'r2:34', 'bottleneck': 'r2-B4', 'role': 'd',
     'source': 'Yan et al., ZETA', 'version': 'arXiv v2, 5 Sep 2026', 'url': 'https://arxiv.org/abs/2609.02546v2',
     'quote': ['Experimental results show that local end-effector (EEF) state-action representations, the source embodiment '
               'diversity, and auxiliary co-training improve cross-embodiment transfer by around 15, 18, and 7 percentage '
               'points, respectively.',
               'adding only 5% target-embodiment data during pretraining improves average target-embodiment progress by 13.4 '
               'percentage points'],
     'raw_file': R + '2609.02546v2.txt',
     'agent_note': 'Families: a shared (end-effector, delta) action interface; source-embodiment diversity; auxiliary '
                   'co-training; exposure to target data. Assumes the target body can be reached through a fixed shared '
                   'action interface.'},
    {'id': 'r2:35', 'bottleneck': 'r2-B4', 'role': 'd',
     'source': 'Domae et al., The Embodiment Gap (TMLR)', 'version': 'arXiv v1, 19 Aug 2026', 'url': 'https://arxiv.org/abs/2608.18433v1',
     'quote': ['We then examine recent work through three overlapping research directions: sharing semantics and perception, '
               'sharing robot data and interfaces, and learning correspondence across embodiments.'],
     'raw_file': R + '2608.18433v1.txt', 'agent_note': 'The three method families.'},

    # ---------------- r2-B5: sim-to-real transfer
    {'id': 'r2:36', 'bottleneck': 'r2-B5', 'role': 'a',
     'source': 'Jin et al., Grounding Sim-to-Real Generalization in Robotic Manipulation: An Empirical Study with Vision-Language-Action Models',
     'version': 'arXiv v2, 29 Jun 2026 (v1 24 Mar 2026)', 'url': 'https://arxiv.org/abs/2603.22876v2',
     'quote': ['Given the high cost of real-world data collection, a practical alternative is to generate synthetic data '
               'through simulation. However, the resulting synthetic data often exhibits a significant gap from real-world '
               'distributions.'],
     'raw_file': R + '2603.22876v2.txt', 'agent_note': 'The problem stated.'},
    {'id': 'r2:37', 'bottleneck': 'r2-B5', 'role': 'b',
     'source': 'Ruan et al. (X Square Robot), X2Real Technical Report: An eXtensive simulation benchmark for real-world generalist policies (company technical report)',
     'version': 'arXiv v1, 23 Sep 2026', 'url': 'https://arxiv.org/abs/2609.27449v1',
     'quote': ['Generalist robot manipulation policies have developed rapidly, yet their reliable evaluation remains '
               'challenging due to fundamental flaws in existing simulation benchmarks: prominent sim-to-real gaps'],
     'raw_file': R + '2609.27449v1.txt', 'agent_note': '2026 statement (about evaluation in simulation).'},
    {'id': 'r2:38', 'bottleneck': 'r2-B5', 'role': 'b',
     'source': 'Liu et al., RoboFolDeX', 'version': 'arXiv v2, 18 Sep 2026', 'url': 'https://arxiv.org/abs/2609.10243v2',
     'quote': ['However, models and methods that achieve strong performance in simulation can suffer substantial degradation '
               'when deployed on real robots.'],
     'raw_file': R + '2609.10243v2.txt', 'agent_note': '2026 statement.'},
    {'id': 'r2:39', 'bottleneck': 'r2-B5', 'role': 'c',
     'source': 'Jin et al. (Table 3 and Lesson 5)', 'version': 'arXiv v2, 29 Jun 2026', 'url': 'https://arxiv.org/abs/2603.22876v2',
     'quote': ['Table 3: Effect of reinforcement learning (RL) and domain randomization (DR) on zero-shot Sim2Real performance '
               'across five tasks.',
               'SFT + RL + DR 60% 50.8% 87% 51.4% 72% 16.2% 68% 64.6% 67% 30.8%',
               'when domain randomization is incorporated during RL rollouts, the performance further improves to 42.8% in '
               'real-world evaluation and 70.8% in Sim-OOD'],
     'raw_file': R + '2603.22876v2.txt',
     'agent_note': 'OpenVLA-OFT, five tasks, columns Sim-OOD then Real per task. Best (SFT + RL + DR): real 42.8% average vs '
                   '70.8% for the same policy in held-out simulation: a transfer loss of 28.0 points; per task the real rate '
                   'is 50.8/51.4/16.2/64.6/30.8. Target used: the policy\'s own simulation success (no transfer loss); no '
                   'real-data-trained reference is reported.'},
    {'id': 'r2:40', 'bottleneck': 'r2-B5', 'role': 'c',
     'source': 'Ruan et al. (X Square Robot), X2Real (abstract and Section 1)', 'version': 'arXiv v1, 23 Sep 2026', 'url': 'https://arxiv.org/abs/2609.27449v1',
     'quote': ['achieving a 0.84 linear correlation between simulated and real-robot evaluation results.',
               'More specifically, we care about the linear correlation between the scores of the same model evaluated in '
               'simulation and on a real robot; ideally, this correlation should approach 1.0.'],
     'raw_file': R + '2609.27449v1.txt',
     'agent_note': 'Sim-to-real predictivity of evaluation: 0.84 against the stated target 1.0 (gap 0.16). Company report, '
                   'calibrated simulator.'},
    {'id': 'r2:41', 'bottleneck': 'r2-B5', 'role': 'c',
     'source': 'Morgan et al., Colosseum V2 (Section V-F)', 'version': 'arXiv v3, 18 Sep 2026', 'url': 'https://arxiv.org/abs/2605.27759v3',
     'quote': ['Real-world experiments indicate that COLOSSEUM V2 does not precisely predict the absolute success rate achieved '
               'on hardware due to the sim-to-real gap.',
               'where the coefficient of determination across all 35 task–perturbation pairs is R2 = 0.49.'],
     'raw_file': R + '2605.27759v3.txt',
     'agent_note': 'Supporting: R^2 = 0.49 between simulated and real success over 35 task-perturbation pairs (one policy, '
                   'five tasks); the relative effect of perturbations transfers better (mean absolute difference 12.3 points '
                   'after normalisation, stated in the same section).'},
    {'id': 'r2:42', 'bottleneck': 'r2-B5', 'role': 'd',
     'source': 'Jin et al.', 'version': 'arXiv v2, 29 Jun 2026', 'url': 'https://arxiv.org/abs/2603.22876v2',
     'quote': ['we empirically examine the primary determinants of Sim-to-Real generalization across four dimensions: '
               'multi-level domain randomization, photorealistic rendering, physics-realistic modeling, and reinforcement '
               'learning updates.',
               'episode-wise, where factors are sampled once per episode and fixed during rollout, and frame-wise, where '
               'factors are resampled at every simulation step.',
               'Frame-wise domain randomization yields better zero-shot transfer than episode-wise strategies'],
     'raw_file': R + '2603.22876v2.txt',
     'agent_note': 'Families: domain randomisation, rendering fidelity, physics fidelity, RL fine-tuning in simulation. Time '
                   'assumption named: the randomisation clock (per episode vs per simulation step); the finer clock transfers '
                   'better here.'},
    {'id': 'r2:43', 'bottleneck': 'r2-B5', 'role': 'd',
     'source': 'UC Berkeley News, "Are we truly on the verge of the humanoid robot revolution?" (interview with Ken Goldberg)',
     'version': 'web page dated August 27, 2025 (no last-updated date shown)',
     'url': 'https://news.berkeley.edu/2025/08/27/are-we-truly-on-the-verge-of-the-humanoid-robot-revolution/',
     'quote': ['Another approach is to create data by running simulations of robot motions, and that actually does work pretty '
               'well for robots running and performing acrobatics.',
               'But for dexterity — where the robot is actually doing something useful, like the tasks of a construction '
               'worker, plumber, electrician, kitchen worker or someone in a factory doing things with their hands — that has '
               'been very elusive, and simulation doesn’t seem to work.'],
     'raw_file': R + 'berkeley_news_2025-08-27.txt',
     'agent_note': 'Fairness: simulation-trained policies transfer well for locomotion and acrobatics (the family works there); '
                   'the open part is contact-rich manipulation.'},

    # ---------------- r2-B6: data scarcity and cost
    {'id': 'r2:44', 'bottleneck': 'r2-B6', 'role': 'a',
     'source': 'Kawaharazuka et al., VLA Models for Robotics: A Review Towards Real-World Applications (IEEE Access)',
     'version': 'arXiv v1, 8 Oct 2025', 'url': 'https://arxiv.org/abs/2510.07077v1',
     'quote': ['Second, high-quality robot demonstrations, often collected via teleoperation are expensive and difficult to '
               'scale.'],
     'raw_file': R + '2510.07077v1.txt', 'agent_note': 'The problem stated.'},
    {'id': 'r2:71', 'bottleneck': 'r2-B6', 'role': 'a',
     'source': 'Wang et al., Vision-Language-Action in Robotics: A Survey of Datasets, Benchmarks, and Data Engines (TMLR, per the arXiv comment)',
     'version': 'arXiv v1, 24 Apr 2026', 'url': 'https://arxiv.org/abs/2604.23001v1',
     'quote': ['Taken together, these findings suggest that the central challenge of VLA is not merely data scarcity, but the '
               'lack of unified abstractions that bridge perception, language grounding, and embodied control across '
               'heterogeneous platforms.'],
     'raw_file': R + '2604.23001v1.txt',
     'agent_note': 'A reframing, recorded for the double check: the source says scarcity is not the whole problem (possible '
                   'misframing of r2-B6). Id out of sequence: added after r2:70.'},
    {'id': 'r2:45', 'bottleneck': 'r2-B6', 'role': 'b',
     'source': 'Ye et al., Data Pyramid for Embodied Manipulation: A Survey',
     'version': 'arXiv v2, 8 Aug 2026 (v1 27 Jul 2026)', 'url': 'https://arxiv.org/abs/2607.24744v2',
     'quote': ['Multimodal foundation models learned to see and to speak by consuming the whole internet. Embodied agents admit '
               'no such shortcut, since they require data that couple observations with physical states and actions.'],
     'raw_file': R + '2607.24744v2.txt', 'agent_note': '2026 statement.'},
    {'id': 'r2:46', 'bottleneck': 'r2-B6', 'role': 'b',
     'source': 'UC Berkeley News (interview with Ken Goldberg; reports his Science Robotics papers of 27 Aug 2025)',
     'version': 'web page dated August 27, 2025', 'url': 'https://news.berkeley.edu/2025/08/27/are-we-truly-on-the-verge-of-the-humanoid-robot-revolution/',
     'quote': ['We don’t have anywhere near that amount of data to train robots, and 100,000 years is just the amount of text '
               'that we have to train language models. We believe that training robots is much more complex, so we’ll need '
               'much more data.'],
     'raw_file': R + 'berkeley_news_2025-08-27.txt',
     'agent_note': '2025 statement by the author. The Science Robotics paper itself (doi 10.1126/scirobotics.aea7390) '
                   'returned HTTP 403 and was not read.'},
    {'id': 'r2:47', 'bottleneck': 'r2-B6', 'role': 'c',
     'source': 'UC Berkeley News (Goldberg) and Ye et al., Data Pyramid survey (Section 7.2.1)',
     'version': 'web page dated August 27, 2025', 'url': 'https://news.berkeley.edu/2025/08/27/are-we-truly-on-the-verge-of-the-humanoid-robot-revolution/',
     'quote': ['To calculate this data gap, I looked at how much text data exists on the internet and calculated how long it '
               'would take a human to sit down and read it all. I found it would take about 100,000 years.',
               'And every eight hours of work gives you just eight more hours of data.'],
     'raw_file': R + 'berkeley_news_2025-08-27.txt',
     'agent_note': 'The target: about 100,000 years (the reading time of LLM text, stated by Goldberg as a lower bound on '
                   'what robots need). The best reported corpus is in claim r2:48. The comparison is Goldberg\'s analogy, not '
                   'a programme requirement: flagged as a weak target.'},
    {'id': 'r2:48', 'bottleneck': 'r2-B6', 'role': 'c',
     'source': 'Ye et al., Data Pyramid for Embodied Manipulation: A Survey (Sections 2.4 and 7.2.1)',
     'version': 'arXiv v2, 8 Aug 2026', 'url': 'https://arxiv.org/abs/2607.24744v2',
     'quote': ['Xiaomi-Robotics-1 [340] further reports pretraining on more than 100,000 hours of real-world UMI trajectories,',
               'AgiBot World Beta [26] reports one million trajectories and nearly 3,000 hours of data',
               'Although these quantities are not directly comparable because of differences in modality, processing, '
               'filtering, and training stage'],
     'raw_file': R + '2607.24744v2.txt',
     'agent_note': 'Best reported: >100,000 hours of real-world UMI trajectories (hand-held gripper data, not robot '
                   'teleoperation), about 11.4 years of continuous data; robot-collected: about 3,000 hours (AgiBot World). '
                   'Against Goldberg\'s 100,000 years (r2:47): 100,000 h / 8,766 h per year = 11.4 years, a factor of about '
                   '8,800 short; 3,000 h is a factor of about 290,000 short. CROSS-SOURCE and heterogeneous units (reading '
                   'time of text vs recorded interaction time); an order-of-magnitude reading only.'},
    {'id': 'r2:49', 'bottleneck': 'r2-B6', 'role': 'c',
     'source': 'Yu et al., A Survey on Efficient Vision-Language-Action Models (TPAMI, accepted)',
     'version': 'arXiv v3, 28 Sep 2026 (v1 27 Oct 2025, v2 2 Feb 2026)', 'url': 'https://arxiv.org/abs/2510.24795v3',
     'quote': ['(3) Inefficient Data Collection: The reliance on large-scale datasets, with examples like π0 [2] requiring over '
               '10,000 hours of robotic trajectories, results in a time-consuming and labor-intensive data collection '
               'pipeline that severely limits the applicability of such approaches.'],
     'raw_file': R + '2510.24795v3.txt',
     'agent_note': 'Supporting: a production VLA\'s robot data, over 10,000 hours (about 1.14 years).'},
    {'id': 'r2:50', 'bottleneck': 'r2-B6', 'role': 'd',
     'source': 'Ye et al., Data Pyramid survey', 'version': 'arXiv v2, 8 Aug 2026', 'url': 'https://arxiv.org/abs/2607.24744v2',
     'quote': ['In this work, we organize the embodied data ecosystem as a “pyramid” spanning five complementary sources: 1re'
               'al-robot data, 2UMI-style data, 3egocentric and exocentric data, 4simulation data, and 5general vision-language '
               'data.'],
     'raw_file': R + '2607.24744v2.txt',
     'agent_note': 'Families by source: teleoperated real-robot data (accrues at wall-clock rate, r2:47), hand-held UMI, human '
                   'video, simulation, web vision-language data.'},
    {'id': 'r2:51', 'bottleneck': 'r2-B6', 'role': 'd',
     'source': 'UC Berkeley News (Goldberg)', 'version': 'web page dated August 27, 2025',
     'url': 'https://news.berkeley.edu/2025/08/27/are-we-truly-on-the-verge-of-the-humanoid-robot-revolution/',
     'quote': ['This is a way to bootstrap the data collection process. For example, you could get a robot to perform a task '
               'well enough that people will buy it, and then collect data as it works.'],
     'raw_file': R + 'berkeley_news_2025-08-27.txt',
     'agent_note': 'Proposed family: engineered systems deployed first, data collected during useful work (fleet data).'},

    # ---------------- r2-B7: long-horizon, multi-step tasks with one generalist policy
    {'id': 'r2:52', 'bottleneck': 'r2-B7', 'role': 'a',
     'source': 'Bai et al. (Team Comet), Openpi Comet: Competition Solution For 2025 BEHAVIOR Challenge',
     'version': 'arXiv v3, 5 Jan 2026 (v1 10 Dec 2025, v2 12 Dec 2025)', 'url': 'https://arxiv.org/abs/2512.10071v3',
     'quote': ['Such tasks require orchestrated sequences of interdependent behaviors, where compounding errors and shifting '
               'state distributions can degrade performance over time.',
               'Consequently, achieving reliable long-horizon performance while preserving scalability and generality remains '
               'an open challenge.'],
     'raw_file': R + '2512.10071v3.txt', 'agent_note': 'The problem stated, and a 2025-26 statement that it is open.'},
    {'id': 'r2:53', 'bottleneck': 'r2-B7', 'role': 'b',
     'source': 'Larchenko, Zarin & Karnatak, Task adaptation of Vision-Language-Action model: 1st Place Solution for the 2025 BEHAVIOR Challenge',
     'version': 'arXiv v2, 21 Dec 2025 (v1 7 Dec 2025)', 'url': 'https://arxiv.org/abs/2512.06951v2',
     'quote': ['Long-horizon household manipulation remains challenging. Even with extensive engineering, we achieve only 26% '
               'success.'],
     'raw_file': R + '2512.06951v2.txt', 'agent_note': '2025 statement by the winning team ("26% success" is their q-score).'},
    {'id': 'r2:54', 'bottleneck': 'r2-B7', 'role': 'b',
     'source': 'Fan et al., RoboSPA: Can VLA Models Go Beyond Simple Scenes and Short-Horizon Tasks? (EMNLP 2026 main)',
     'version': 'arXiv v1, 4 Sep 2026', 'url': 'https://arxiv.org/abs/2609.05324v1',
     'quote': ['Notably, all models fail on the hardest Memory-Intensive Planning (MIP), revealing severe limitations in '
               'maintaining task-relevant memory over extended horizons.'],
     'raw_file': R + '2609.05324v1.txt', 'agent_note': '2026 statement.'},
    {'id': 'r2:55', 'bottleneck': 'r2-B7', 'role': 'c',
     'source': 'Bai et al. (Team Comet), Openpi Comet (Table 1, 2025 BEHAVIOR Challenge standard track)', 'version': 'arXiv v3, 5 Jan 2026',
     'url': 'https://arxiv.org/abs/2512.10071v3',
     'quote': ['Table 1: Results of 2025 BEHAVIOR Challenge for standard track and our post-challenge solution. Q-score for the '
               'test set is used for final ranking.',
               'Rank Team Full Task Success Rate Q-Score Validation Test Validation Test Comet (ours, post-challenge) 0.1500 '
               '0.3453 1 Robot Learning Collective 0.1120 0.1240 0.2605 0.2599 2 Comet (ours) 0.1440 0.1140 0.18301 0.2514'],
     'raw_file': R + '2512.10071v3.txt',
     'agent_note': '50 household tasks in simulation, one policy. Best test result (1st place): full task success 0.1240, '
                   'q-score (partial credit) 0.2599; best reported validation after the challenge: success 0.1500, q-score '
                   '0.3453. Target: full completion of every task (success 1.0), the benchmark\'s own goal; no human success '
                   'rate is reported. Gap in full success: 0.876 (test), 0.850 (post-challenge validation).'},
    {'id': 'r2:56', 'bottleneck': 'r2-B7', 'role': 'c',
     'source': 'Fan et al., RoboSPA (Table 2)', 'version': 'arXiv v1, 4 Sep 2026', 'url': 'https://arxiv.org/abs/2609.05324v1',
     'quote': ['Table 2: Performance comparison of four baseline VLA models on RoboSPA. We use Success Rate (SR) as the '
               'evaluation metric. Drop denotes the L1-to-L5 decrease.',
               'Memory-Intensive Planning 18.2 0.0 18.2 7.6 0.0 7.6 54.0 0.0 54.0 44.6 0.0 44.6 Average 24.1 7.7 16.4 29.3 7.0 '
               '22.3 71.2 23.1 48.1 58.8 15.9 42.9',
               'the best-performing model, π0.5, decreasing from 71.2% at L1 to 23.1% at L5.'],
     'raw_file': R + '2609.05324v1.txt',
     'agent_note': 'Columns per model (RDT, GO-1, pi0.5, X-VLA): L1, L5, Drop. Long-horizon procedural planning at the hardest '
                   'level (L5): best 23.1% (pi0.5); memory-intensive planning 0.0 for every model. Target: task completion '
                   '(100%); no human baseline reported. Gap 76.9 points at L5.'},
    {'id': 'r2:57', 'bottleneck': 'r2-B7', 'role': 'c',
     'source': 'Liu et al., RoboFolDeX (Table 3)', 'version': 'arXiv v2, 18 Sep 2026', 'url': 'https://arxiv.org/abs/2609.10243v2',
     'quote': ['Task Success Rate Average Time FoldScore Shirt 90.00% 2:29 76.88 Skirt 90.00% 1:54 81.25 Pants 100.00% 1:48 '
               '85.50 Towel 100.00% 1:40 86.50 Average 95.00% 1:58 82.53',
               'Table 3: Recovery-augmented multi-task real-robot results. A single π0 policy with RTC is trained using d'
               'emonstrations and recovery data from four garment categories.'],
     'raw_file': R + '2609.10243v2.txt',
     'agent_note': 'Contrary evidence, recorded for fairness: a real-robot long-horizon task (garment folding, about 2 minutes) '
                   'reaches 95.00% average success with recovery data (80.75% with demonstrations only, Table 2). Narrow task '
                   'family, held-out garments of the same categories; the target is nearly reached there. The open part is '
                   'breadth (many tasks, one policy: r2:55, r2:56).'},
    {'id': 'r2:58', 'bottleneck': 'r2-B7', 'role': 'd',
     'source': 'Bai et al. (Team Comet), Openpi Comet', 'version': 'arXiv v3, 5 Jan 2026', 'url': 'https://arxiv.org/abs/2512.10071v3',
     'quote': ['A common approach is to decompose tasks into subtasks (Lin et al., 2022; Shi et al., 2023; Tie et al., 2025) and '
               'train separate local policies. However, this strategy does not resolve the skill chaining problem'],
     'raw_file': R + '2512.10071v3.txt',
     'agent_note': 'Decomposition family: subtask boundaries fixed in advance, one local policy each; the transitions between '
                   'them are the unsolved part.'},
    {'id': 'r2:59', 'bottleneck': 'r2-B7', 'role': 'd',
     'source': 'Larchenko et al., BEHAVIOR 1st place', 'version': 'arXiv v2, 21 Dec 2025', 'url': 'https://arxiv.org/abs/2512.06951v2',
     'quote': ['Without memory of past actions or explicit stage tracking, the policy cannot distinguish these states and may '
               'execute incorrect actions.',
               'We introduce System 2 stage tracking: the model predicts the current task stage, and a voting mechanism '
               'filters noisy predictions to maintain stable stage estimates.',
               'Time limit: Task-specific (2× average human task completion time in the demo dataset)'],
     'raw_file': R + '2512.06951v2.txt',
     'agent_note': 'Memory assumption: a Markovian policy cannot tell visually identical stages apart; the fix is an explicit '
                   'stage counter from demonstration stages. Clock assumption of the benchmark: a wall-clock time limit set '
                   'at twice the human completion time.'},

    # ---------------- r2-B8: on-robot inference latency and compute
    {'id': 'r2:60', 'bottleneck': 'r2-B8', 'role': 'a',
     'source': 'Yu et al., A Survey on Efficient Vision-Language-Action Models (TPAMI, accepted)', 'version': 'arXiv v3, 28 Sep 2026',
     'url': 'https://arxiv.org/abs/2510.24795v3',
     'quote': ['(1) Real-Time Incompatibility: current VLAs suffer from high inference latency and insufficient control '
               'frequency [1], making them incompatible with the sub-second control cycles required for responsive and '
               'adaptive robotic manipulation'],
     'raw_file': R + '2510.24795v3.txt', 'agent_note': 'The problem stated (and a 2025-26 statement).'},
    {'id': 'r2:61', 'bottleneck': 'r2-B8', 'role': 'b',
     'source': 'Grover et al., Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies',
     'version': 'arXiv v2, 19 Mar 2026 (v1 16 Mar 2026)', 'url': 'https://arxiv.org/abs/2603.16952v2',
     'quote': ['Across the literature, quantization, pruning, and related optimizations improve deployability, but they do not, '
               'on current evidence, resolve the worst-case failures associated with memory contention, timing variability, '
               'thermal instability, and limited safety assurance.'],
     'raw_file': R + '2603.16952v2.txt', 'agent_note': '2026 statement.'},
    {'id': 'r2:62', 'bottleneck': 'r2-B8', 'role': 'b',
     'source': 'Yang et al., Jetson-PI: Towards Onboard Real-Time Robot Control via Foresight-Aligned Asynchronous Inference (CoRL 2026)',
     'version': 'arXiv v5, 5 Sep 2026 (v1 14 Jul 2026)', 'url': 'https://arxiv.org/abs/2607.12659v5',
     'quote': ['However, deploying VLA models on low-power onboard devices, such as the Jetson Orin, remains challenging due to '
               'their high computational complexity, which leads to substantial inference latency and low control frequency.'],
     'raw_file': R + '2607.12659v5.txt', 'agent_note': '2026 statement.'},
    {'id': 'r2:63', 'bottleneck': 'r2-B8', 'role': 'c',
     'source': 'Yang et al., Jetson-PI (Table 4)', 'version': 'arXiv v5, 5 Sep 2026', 'url': 'https://arxiv.org/abs/2607.12659v5',
     'quote': ['Table 4: Inference latency and control frequency on different devices, evaluated on LIBERO.',
               'Naive PI05 152.3 631.0 536.8 1420.8 1420.8 0.70',
               '+Intermediate Buffer & Unroll 79.5 210.3 123.1 412.9 165.1 6.06',
               '+Intermediate Buffer & Unroll 51.6 156.2 101.7 309.5 131.8 7.59',
               'As shown in Figure 1(a), using an RTX 4090 can reduce battery life by 6.0×'],
     'raw_file': R + '2607.12659v5.txt',
     'agent_note': 'Columns: ViT, LLM, Action Expert, Total (ms), Reaction Time (ms), Control Frequency (Hz); first two rows '
                   'Jetson Orin, the last row Jetson Thor. Best onboard: 6.06 Hz on Orin (reaction 165.1 ms), 7.59 Hz on Thor, '
                   'from 0.70 Hz naive. Target (claim r2:64): at least 10-20 Hz: short by 3.94-13.94 Hz on Orin (a factor '
                   '1.65-3.3). In the real-robot test (XR-1 on an Orin, Section 5.3) actions execute at 15 Hz; the frequency here is '
                   'the closed-loop update rate. On a desktop RTX 4090 the target is met (r2:65), at a 6.0x battery-life cost.'},
    {'id': 'r2:64', 'bottleneck': 'r2-B8', 'role': 'c',
     'source': 'Vishwanathan, Subramanian & Raghunathan, Characterizing VLA Models: Identifying the Action Generation Bottleneck for Edge AI Architectures (workshop paper)',
     'version': 'arXiv v1, 1 Mar 2026', 'url': 'https://arxiv.org/abs/2603.02271v1',
     'quote': ['Safe, dynamic manipulation in physical environments requires a consistent control frequency of at least 10–20 '
               'Hz.',
               'Figure 2 summarizes our profiling results and illustrates that (i) the latencies are ∼200 −300× higher than '
               'those needed for real-time (10Hz) operation'],
     'raw_file': R + '2603.02271v1.txt',
     'agent_note': 'The target (10-20 Hz), and a second best-vs-target reading: MolmoAct-7B (a reasoning VLA) on Jetson Orin '
                   'and Thor is 200-300x slower than 10 Hz. Workshop paper; the latency values themselves are in a figure.'},
    {'id': 'r2:65', 'bottleneck': 'r2-B8', 'role': 'c',
     'source': 'Yu et al., Efficient VLA survey (Table 1)', 'version': 'arXiv v3, 28 Sep 2026', 'url': 'https://arxiv.org/abs/2510.24795v3',
     'quote': ['Models Params.(↓) I.L.(ms) (↓) Freq.(Hz) (↑) Accelerator',
               'OpenVLA [1] 7B 166 6 RTX 4090 π0 [2] 3.3B 73 20/50 RTX 4090'],
     'raw_file': R + '2510.24795v3.txt',
     'agent_note': 'Desktop GPU (RTX 4090, up to 450 W per Jetson-PI Table 2): pi0 reaches 20/50 Hz with 73 ms latency, so the '
                   '10-20 Hz target is met off-board; OpenVLA 7B at 6 Hz is not. The bottleneck is onboard, low-power compute.'},
    {'id': 'r2:66', 'bottleneck': 'r2-B8', 'role': 'b',
     'source': 'Black, Galliker & Levine, Real-Time Execution of Action Chunking Flow Policies (RTC, NeurIPS 2025)',
     'version': 'arXiv v2, 5 Dec 2025 (v1 9 Jun 2025)', 'url': 'https://arxiv.org/abs/2506.07339v2',
     'quote': ['However, the high latency of state-of-the-art generalist models, including recent vision-language-action models '
               '(VLAs), poses a significant challenge.'],
     'raw_file': R + '2506.07339v2.txt', 'agent_note': '2025 statement.'},
    {'id': 'r2:67', 'bottleneck': 'r2-B8', 'role': 'd',
     'source': 'Black, Galliker & Levine, RTC (NeurIPS 2025)', 'version': 'arXiv v2, 5 Dec 2025', 'url': 'https://arxiv.org/abs/2506.07339v2',
     'quote': ['Chunking sacrifices the reactivity of a system to external stimuli and also introduces discontinuities in the '
               'transition points between chunks',
               'It generates the next action chunk while executing the current one, “freezing” actions guaranteed to execute '
               'and “inpainting” the rest.',
               'even in the presence of inference delays in excess of 300 milliseconds, corresponding to more than 30% of the '
               'model’s prediction horizon.'],
     'raw_file': R + '2506.07339v2.txt',
     'agent_note': 'Action chunking (open-loop execution between inference calls, chunk boundaries on a fixed step clock) and '
                   'asynchronous inference (the delay is assumed known and the committed prefix frozen). Fairness: RTC keeps '
                   'high success on precise tasks under >300 ms delay, so latency is partly absorbed by asynchrony.'},
    {'id': 'r2:68', 'bottleneck': 'r2-B8', 'role': 'd',
     'source': 'Yang et al., Jetson-PI (CoRL 2026)', 'version': 'arXiv v5, 5 Sep 2026', 'url': 'https://arxiv.org/abs/2607.12659v5',
     'quote': ['Based on this, we design a Confidence-based Scheduling Optimization approach, where the future correction module '
               'serves as the scheduler. Its predicted confidence determines when to invoke the VLM and the action expert.'],
     'raw_file': R + '2607.12659v5.txt',
     'agent_note': 'Scheduling family: the VLM is invoked when a confidence signal says so, not on a fixed clock (an '
                   'event-triggered invocation).'},
    {'id': 'r2:69', 'bottleneck': 'r2-B8', 'role': 'd',
     'source': 'Yu et al., Efficient VLA survey; Grover et al., edge survey', 'version': 'arXiv v3, 28 Sep 2026', 'url': 'https://arxiv.org/abs/2510.24795v3',
     'quote': ['Inspired by dual-process theories [120], [121], hierarchical VLAs bifurcate cognition into deliberate "System 2" '
               'reasoning and intuitive "System 1" execution.',
               'HiRT [44] and DP-VLA [97] establish low-frequency VLM guidance for high-frequency control'],
     'raw_file': R + '2510.24795v3.txt',
     'agent_note': 'Hierarchical (dual-rate) family: two fixed clocks, a slow planner and a fast controller. The edge survey\'s '
                   'figure labels the fast system 50-500 Hz (claim r2:70). Other families in the same survey: quantisation, '
                   'pruning, token reduction, one-step or parallel decoding.'},
    {'id': 'r2:70', 'bottleneck': 'r2-B8', 'role': 'd',
     'source': 'Grover et al., edge survey', 'version': 'arXiv v2, 19 Mar 2026', 'url': 'https://arxiv.org/abs/2603.16952v2',
     'quote': ['In robotic systems operating at 50–100 Hz, these delays appear as actuator jitter, delayed servo response, and '
               'degraded sensor fusion [170].',
               'A policy that initially runs near 20 Hz may stabilize at a much lower frequency after throttling, increasing '
               'perception staleness and reducing closed-loop responsiveness.',
               'Separating high-rate control from lower-rate semantic reasoning is one promising response to the tension '
               'between control-loop determinism and deliberative inference.',
               'System 1 (50-500 Hz) Fast Reflex Policy System 2 Semantic Planner Low Frequency'],
     'raw_file': R + '2603.16952v2.txt',
     'agent_note': 'Clock assumption: control loops at a fixed nominal rate (50-100 Hz); the achieved rate drifts with thermal '
                   'state, so the nominal clock is not the real one. Mitigation family: rate separation.'},
]

BOTTLENECKS = [
    {'id': 'r2-B1', 'name': 'Forgetting in lifelong robot learning (sequential skill acquisition)',
     'problem': 'A robot policy that learns new manipulation skills in sequence loses old ones unless it replays a large '
                'share of past data or routes by known task identity.',
     'open': True,
     'benchmark': 'LIBERO-10 continual learning with experience replay, NBT (negative backward transfer) at a replay budget of '
                  '100 samples per task (2%) (Liu et al. 2026, Table 5); supporting: PHASER Table 1, LifeLong-RFT Table IV, '
                  'OrthoSkillVLA Table 1',
     'best': 'NBT 0.229 at 2% replay (Pi0); NBT -0.068 / 0.059 at 20% replay (Pi0 / GR00T); PHASER final ASR 85.8, NBT 10.0 on '
             'LIBERO-Long (OpenVLA-OFT-7B); replay-free OrthoSkillVLA final SR 83.50 vs oracle routing 86.2',
     'target': 'zero forgetting, NBT = 0 ("NBT=0 implying zero forgetting", PHASER); multitask learning as the upper bound '
               '(LIBERO); oracle routing 86.2 (OrthoSkillVLA)',
     'gap_note': 'Open only under a small memory budget or a weak backbone: NBT 0.229 at 2% replay on LIBERO-10; closed at 20% '
                 'replay (Pi0 -0.068, GR00T 0.059, same paper). Replay-free with oracle routing as target: 2.7 points (three '
                 'skills). With 3B backbones whose action heads are trained from scratch, final ASR on LIBERO-Long 48.6-51.6 '
                 'and NBT 11.1-12.4 (PHASER). Contested by its own best source ("surprisingly resistant to forgetting"); the '
                 'double check should read it as CONTESTED unless a small-budget or real-world target is the one that counts.',
     'assumptions': ['task boundaries given: replay buffers are written and consolidation runs "after each task"',
                     'raw-sample replay with a fixed per-task budget (5 demonstrations; 2% or 20% of data)',
                     'uniform replay over clock time within a trajectory (PHASER: this under-samples short phases; phase '
                     'boundaries from annotation or change points in the action signal)',
                     'fixed epoch budget per arriving task; pruning on a task-count clock (every 10 tasks); some methods need '
                     'oracle task identifiers',
                     'deployed default: freeze the policy after deployment, so no on-robot learning at all'],
     'cpu_testable': False,
     'cpu_note': 'the named results fine-tune 3B-7B VLAs on GPUs; LIBERO\'s own small BC baselines (ResNet-T, ViT-T) with '
                 'robosuite rollouts could run a reduced proxy (few tasks, few epochs) on CPU in hours, but that is a proxy'},
    {'id': 'r2-B2', 'name': 'Erosion of pretrained VLM capabilities when fine-tuning into a VLA',
     'problem': 'Behaviour-cloning fine-tuning of a vision-language model on robot actions overwrites the representations and '
                'multimodal skills it was chosen for.',
     'open': True,
     'benchmark': 'Multimodal understanding benchmarks (MMMU, OCRBench, MMBench, TextVQA, DocVQA, InfoVQA, AI2D, RealWorldQA, '
                  'etc.) of the VLA against its base VLM (VLM2VLA Table 1)',
     'best': 'VLM2VLA (12B, LoRA, actions as language): MMMU 42.7, OCRBench 63.9, MMB-en 68.5, RealWorldQA 43.3',
     'target': 'the base VLM Gemma-3-12B-IT: MMMU 46.0, OCRBench 75.0, MMB-en 76.9, RealWorldQA 50.6',
     'gap_note': 'Below the base on 9 of 12 benchmarks, by 2.2 (DocVQA) to 11.1 (OCRBench) points; ahead on MMStar, MME and '
                 'ChartQA. A co-trained generalist VLA (pi0.5) scores 0.3-27.0 on the same text benchmarks. Same paper; one '
                 'best method; 2025 numbers (a 2026 B-b exists: Anchor-Align).',
     'assumptions': ['the pretrained VLM is the fixed reference to preserve: frozen backbone, anchoring to a frozen copy, '
                     'proximity to the initial weights',
                     'low-rank adaptation suffices to learn actions (small parameter change)',
                     'co-training with web data at a fixed, tuned mixture ratio; gradient insulation between action and '
                     'language heads'],
     'cpu_testable': False,
     'cpu_note': 'a 12B VLM fine-tune and 12 VQA benchmark evaluations need GPUs; a toy two-head network with a frozen-anchor '
                 'penalty could run on CPU but is not the benchmark'},
    {'id': 'r2-B3', 'name': 'Generalisation of VLA policies under distribution shift (positions, robot initial state, viewpoint)',
     'problem': 'VLA policies that score above 90% on standard benchmarks collapse when object positions, the robot\'s initial '
                'state or the camera change.',
     'open': True,
     'benchmark': 'LIBERO-PRO position swap and LIBERO-Plus robot-initial-state perturbations on the LIBERO-Spatial suite '
                  '(Anchor-Align Tables 1 and 5)',
     'best': 'position swap 22.6; robot initial state 59.1; LIBERO-PRO mean 71.9; LIBERO-Plus mean 90.3 (Anchor-Align VLA, '
             'Sep 2026)',
     'target': 'the same model unperturbed on LIBERO-Spatial, 98.4',
     'gap_note': 'Position swap 75.8 points; robot initial state 39.3; LIBERO-PRO mean 26.5; LIBERO-Plus mean 8.1 (same paper). '
                 'Appearance perturbations are nearly closed (background 99.6, lighting 99.0). On Colosseum V2 even '
                 'unperturbed success on new tasks is 12.6-44.5%.',
     'assumptions': ['the test shifts can be enumerated and sampled into training (generalised training sets of >20,000 '
                     'trajectories)',
                     'evaluation on the training tasks and layouts (the standard LIBERO protocol) measures capability',
                     'pretrained representations are preserved by anchoring or freezing'],
     'cpu_testable': False,
     'cpu_note': 'evaluating 0.5B-7B VLAs over thousands of LIBERO rollouts needs a GPU; the simulator itself runs on CPU'},
    {'id': 'r2-B4', 'name': 'Transfer to new robot embodiments',
     'problem': 'A policy trained on some robot bodies loses much of its task progress on an unseen body, and joint or '
                'continued training across bodies interferes.',
     'open': True,
     'benchmark': 'ZETA strict zero-shot cross-embodiment transfer, mean task progress on full-embodiment changes (Tables 3 '
                  'and 4)',
     'best': 'FULL 60.4 (simulation), 81.9 (real world), EEF-Delta state and action',
     'target': 'progress on the source embodiment: 91.5 (simulation), 100.0 (real world)',
     'gap_note': '31.1 points in simulation, 18.1 in the real world (140 rollouts per model); same paper; progress with partial '
                 'credit, not binary success. 5% target-embodiment data in pretraining recovers 13.4 points.',
     'assumptions': ['a fixed shared action interface (end-effector deltas) maps to every body',
                     'diversity of source bodies substitutes for target data',
                     'or target-embodiment data is available for pretraining or fine-tuning'],
     'cpu_testable': False,
     'cpu_note': 'the study pretrains a pi0.5-class VLA on 640K trajectories from 512 procedurally generated embodiments'},
    {'id': 'r2-B5', 'name': 'Sim-to-real transfer of manipulation policies',
     'problem': 'Policies trained or evaluated in simulation lose much of their success on real hardware, and simulated scores '
                'predict real scores only partly.',
     'open': True,
     'benchmark': 'Zero-shot sim-to-real success of OpenVLA-OFT on five bimanual tasks (Jin et al. Table 3); sim-real '
                  'correlation of evaluation scores (X2Real; Colosseum V2)',
     'best': 'real 42.8% average (SFT + RL + DR) vs 70.8% in held-out simulation; evaluation correlation 0.84 (X2Real, '
             'calibrated simulator); R^2 0.49 (Colosseum V2)',
     'target': 'no transfer loss (real equal to simulated success); correlation 1.0 ("ideally, this correlation should '
               'approach 1.0", X2Real)',
     'gap_note': 'Transfer loss 28.0 points (same paper, same policy); correlation short by 0.16. Fairness: sim-to-real works '
                 'well for locomotion and acrobatics (Goldberg); the open part is contact-rich manipulation.',
     'assumptions': ['domain randomisation on a fixed clock (per episode or per simulation step; per step transfers better)',
                     'rendering and physics fidelity close the gap',
                     'RL fine-tuning in simulation adds robustness'],
     'cpu_testable': False,
     'cpu_note': 'requires a physical robot for the real side; the simulation side uses GPU rendering'},
    {'id': 'r2-B6', 'name': 'Data scarcity and cost of robot interaction data',
     'problem': 'Robot data couple observations with actions and accrue at the wall-clock rate of collection, so corpora are '
                'far smaller than those behind language and vision models.',
     'open': True,
     'benchmark': 'Size of the largest reported robot-learning corpus, in hours, against the reading time of LLM training text',
     'best': '>100,000 hours of real-world UMI trajectories (Xiaomi-Robotics-1, 2026); about 3,000 hours of robot data '
             '(AgiBot World Beta); over 10,000 hours (pi0)',
     'target': 'about 100,000 years (Goldberg: the reading time of LLM text, stated as a lower bound for robots)',
     'gap_note': '100,000 h is about 11.4 years: a factor of about 8,800 short; 3,000 h, a factor of about 290,000. '
                 'CROSS-SOURCE, heterogeneous units, and the target is an analogy rather than a programme requirement: an '
                 'order-of-magnitude reading only. A 2026 survey argues the central challenge is not merely data scarcity '
                 '(possible misframing; for the double check).',
     'assumptions': ['teleoperated data accrue one hour per hour of operator time ("every eight hours of work gives you just '
                     'eight more hours of data")',
                     'cheaper substitutes transfer: hand-held UMI, human egocentric video, simulation, web data',
                     'fleet data collected during useful work, once engineered systems are good enough to deploy'],
     'cpu_testable': False,
     'cpu_note': 'a corpus-size gap is not a computation; nothing to run'},
    {'id': 'r2-B7', 'name': 'Long-horizon multi-step tasks with one generalist policy',
     'problem': 'Success falls sharply as tasks chain many steps, need memory of past stages, or span many household '
                'activities.',
     'open': True,
     'benchmark': '2025 BEHAVIOR Challenge (50 household tasks, OmniGibson), full task success rate and q-score (Openpi Comet '
                  'Table 1); RoboSPA long-horizon procedural planning at level L5 (Table 2)',
     'best': 'BEHAVIOR test full success 0.1240, q-score 0.2599 (1st place); post-challenge validation 0.1500 / 0.3453; '
             'RoboSPA L5 23.1% (pi0.5), memory-intensive planning 0.0 for all models',
     'target': 'full completion of every task (success 1.0; the benchmark goal); no human success rate reported',
     'gap_note': 'Full-success gap 0.876 (test) and 0.850 (validation); RoboSPA 76.9 points. Contrary evidence: a single '
                 'real-robot garment-folding policy reaches 95.00% with recovery data (RoboFolDeX Table 3), so narrow '
                 'long-horizon tasks are close to solved; breadth is not.',
     'assumptions': ['fixed subtask boundaries with separate local policies (skill chaining unsolved)',
                     'Markovian policies without memory; fixes add an explicit stage counter from demonstration stages',
                     'wall-clock time limits (twice the human completion time)',
                     'demonstrations of success only; recovery data added afterwards'],
     'cpu_testable': False,
     'cpu_note': 'BEHAVIOR needs Isaac Sim on RTX GPUs (the 1st-place team used 20 RTX 4090s; a full evaluation took under 2 days)'},
    {'id': 'r2-B8', 'name': 'On-robot inference latency and compute for VLA policies',
     'problem': 'Large VLA policies run on low-power onboard computers at a fraction of the control rate that dynamic '
                'manipulation needs.',
     'open': True,
     'benchmark': 'Closed-loop control frequency of pi0.5 on NVIDIA Jetson Orin, evaluated on LIBERO (Jetson-PI Table 4)',
     'best': '6.06 Hz (reaction time 165.1 ms) on Jetson Orin; 7.59 Hz on Jetson Thor (Jetson-PI, CoRL 2026)',
     'target': 'at least 10-20 Hz (Vishwanathan et al. 2026); fixed control loops of 50-100 Hz (Grover et al. 2026)',
     'gap_note': 'Short by 3.94-13.94 Hz on Orin (a factor 1.65-3.3) against 10-20 Hz; cross-paper target. Met off-board: '
                 'pi0 20/50 Hz on an RTX 4090 (a 6.0x battery-life cost per Jetson-PI). Asynchronous chunking (RTC) keeps '
                 'success under >300 ms delay, so part of the gap is absorbed by execution design.',
     'assumptions': ['action chunking: open-loop execution between inference calls on a fixed step clock',
                     'asynchronous inference with the delay known and the committed prefix frozen',
                     'dual-rate hierarchies with two fixed clocks (slow planner, fast controller at 50-500 Hz)',
                     'event-triggered invocation of the VLM by a confidence signal (Jetson-PI)',
                     'nominal loop rates that drift under thermal throttling'],
     'cpu_testable': False,
     'cpu_note': 'the named metric is hardware-specific (Jetson Orin); a synthetic scheduling model (clock-driven vs '
                 'event-driven replanning under delay) could run on CPU as a proxy'},
]
