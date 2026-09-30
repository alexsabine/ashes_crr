"""ROB1 stage 1b, family R2 (Robotics/DECLARATION.md): the double check of the robot-learning bottlenecks r2-B1 ... r2-B8.

Written by a second agent that did not harvest family R2. For every bottleneck in `claims_r2.BOTTLENECKS` it searched
independently (different queries and sources from the harvester's; log in /tmp/claude-0/rob_src/r2x/search/queries.txt)
for the strongest contrary evidence: a 2025-26 source reporting the target reached on the named metric, a deployed system
that does it, or a source arguing that the bottleneck is misframed. It also re-read the harvester's quotes and numbers
against the harvester's raw texts (/tmp/claude-0/rob_src/r2/txt/); a scratch copy of Open_Bottlenecks/checks/verify.py
pointed at claims_r2.py read "quotes found verbatim: 145 of 145 (claims 71; raw files 30, missing 0)".

Every source was fetched on 2026-09-30 through the session proxy with curl (TLS verification on). arXiv: the abstract page
(for the current version and its history) and the PDF of that version. Text was extracted with the harvester's own
extractors (copied to r2x/): PDFs by pymupdf 1.28.2 (`page.get_text()`, pages joined by newlines); HTML by BeautifulSoup 4
(`get_text('\\n')` after removing script/style/noscript/svg, runs of spaces and blank lines collapsed); the one NVIDIA
developer-forum post was read from the forum's own Discourse JSON (`/t/368788.json`, first post's `cooked` HTML, tags
replaced by line breaks). Raw files live outside the repository under /tmp/claude-0/rob_src/ (`raw_file` is relative to that
root; the fetched originals are in r2x/src/); their sha256 is in /tmp/claude-0/rob_src/r2x/SHA256SUMS.txt and in the dossier
docs/citations/rob1_r2_2026-09-30.md (section "Stage 1b double check"). Claims that re-check the harvester's own sources
point at the harvester's raw texts under r2/txt/.

Fields. role = 'x' (a double-check claim). `refutes` = the bottleneck the claim bears on. `contrary` = True when the claim
is contrary evidence (the target reached, a deployed system that does it, or a misframing argument); False when it is a
re-check of the harvester's reading (a number or a target the harvester got wrong or overstated), which bears on the
bottleneck's B-c but is not evidence that the bottleneck is closed. `shows_target_reached` = True only if the verified
quote shows the target reached on the named metric of that bottleneck (the named metric as the harvester's BOTTLENECKS
entry states it: the quantity and the target, not necessarily the same paper's protocol; every True says in its note how
the protocol differs). `agent_note` is the double-checker's reading, fair to both sides; it is not the source's words.
Company statements, vendor tutorials, forum posts and trade press are recorded as such.

CHECKS: one entry per bottleneck: what was searched, what was found, and `harvester_errors` (quotes or numbers the
harvester got wrong or overstated; an empty list when none was found). Every harvester quote was found verbatim; the
errors listed are readings and "best result" choices, not misquotes.
"""

R = 'r2x/txt/'

CLAIMS = [
    # ---------------- r2-B1: forgetting in lifelong robot learning
    {'id': 'r2x:1', 'bottleneck': 'r2-B1', 'role': 'x', 'refutes': 'r2-B1', 'contrary': True, 'shows_target_reached': True,
     'source': 'Zhu, Hong, Sun, ... Yuan, Zeng & Chen, Can Vision-Language-Action Models Learn from Real-World Data Continually '
               'without Forgetting? (real-world benchmark, pi0.5)',
     'version': 'arXiv v3, 8 Aug 2026 (v1 26 May 2026, v2 28 Jul 2026)', 'url': 'https://arxiv.org/abs/2605.26820v3',
     'quote': ['we find that naive sequential fine-tuning leads to severe catastrophic forgetting, whereas a well-configured '
               'experience replay (ER) approach can effectively mitigate forgetting and outperform joint multi-task training '
               'under equivalent computational budgets.',
               'from −8.95 (ρB = 0.002) to +0.25 (ρB = 0.02) and +1.50 (ρB = 0.2), proving that a modest buffer (ρB = 0.02) '
               'is already highly effective.',
               'ER 100.0 95.0 100.0 96.0 95.0 97.2 +1.5 +11.4',
               'Joint training 97.5 95.0 33.3 92.0 95.0 82.6 – –',
               'yielding an average BWT of −2.7'],
     'raw_file': R + '2605.26820v3.txt',
     'agent_note': 'The strongest contrary evidence for r2-B1, and on real robots. The harvester named NBT at a 2% replay budget '
                   '(Pi0, LIBERO-10: NBT 0.229) and said the check should read the bottleneck as contested "unless a small-budget '
                   'or real-world target is the one that counts". Here the budget is 2% of all past data (rho_B = 0.02, shared '
                   'across tasks, so smaller per task than Liu et al.\'s 100 samples per task) and the final average BWT is +0.25: '
                   'no forgetting (BWT = -NBT). At the paper\'s default 20% budget ER keeps 97.2 average success on both 5-task '
                   'streams (BWT +1.5, +1.9), above joint multi-task training (82.6, 83.2), i.e. the multitask "upper bound" is '
                   'exceeded. Differences from the named protocol: 5 real tasks per stream (not LIBERO-10\'s 10 simulated tasks), '
                   'pi0.5 backbone, one sensitivity figure (the stream it uses is not stated in the text). Fair to the harvester: '
                   'on the 10-task heterogeneous real stream the average BWT is -2.7 and a uniform replay schedule lost up to '
                   '46.7 points on bimanual tasks (Fig. 7), so heterogeneous streams still forget without tuning; and the same '
                   'paper argues simulated LIBERO results "systematically overestimate" robustness to forgetting.'},
    {'id': 'r2x:2', 'bottleneck': 'r2-B1', 'role': 'x', 'refutes': 'r2-B1', 'contrary': True, 'shows_target_reached': False,
     'source': 'Hu, Shim, Tang, Sung, Liu, Stone & Martin-Martin, Simple Recipe Works: Vision-Language-Action Models are Natural '
               'Continual Learners with Reinforcement Learning (Reinforcement Learning Journal 2026; RLC 2026)',
     'version': 'arXiv v3, 11 Jul 2026 (v1 12 Mar 2026, v2 1 Jun 2026); comment "Accepted at RLC 2026; Best paper award at ICRA26 '
                'RL4IL Workshop"', 'url': 'https://arxiv.org/abs/2603.11653v3',
     'quote': ['simple Seq. FT with low-rank adaptation (LoRA) is remarkably strong: it achieves high plasticity, exhibits little to '
               'no forgetting, and retains strong zero-shot generalization',
               'libero-spatial Sequential Fine-Tuning 81.2±0.4 +24.3 0.3±0.5 3.9±1.5 57.1±1.1 +5.6',
               'libero-long-horizon Sequential Fine-Tuning 89.8±0.9 +6.8 -2.4±1.0 0.5±0.1 86.6±0.2 +3.3',
               'Multitask (Oracle) 90.5±0.8 +7.5 – – 85.2±0.5 +1.8',
               'The results indicate that Seq. FT maintains high knowledge retention even as the number of sequential tasks '
               'scales to 30.',
               'Supervised fine-tuning instead of RL 29.9±2.3 -27.0 78.7±1.9 -53.8±0.0 1.1±0.9 -50.4',
               'Each of our base models are obtained by performing supervised fine-tuning with a small amount of in-domain data, '
               'so that the model has non-zero initial success rate.'],
     'raw_file': R + '2603.11653v3.txt',
     'agent_note': 'Contrary: with no replay at all, sequential LoRA fine-tuning of OpenVLA-OFT-7B by on-policy RL (GRPO) keeps '
                   'NBT at 0.3 (libero-spatial), 1.0 (libero-object) and -2.4 (libero-long-horizon) percent, within 0.7-4.6 '
                   'points of the multitask oracle, and retention holds over a 30-task sequence (figure only). This contradicts the '
                   'problem statement "loses old ones unless it replays a large share of past data or routes by known task '
                   'identity" for the RL post-training regime. Not marked as reaching the named target because the named '
                   'protocol is imitation (ER over demonstrations) and the same paper shows supervised fine-tuning in its place '
                   'forgets catastrophically (NBT 78.7 on libero-spatial); the base models were primed with in-domain SFT data '
                   '(initial success 55.6-83.0%), 4-5 tasks per sequence, and RL needs a reward and a simulator. So: closed for '
                   'continual RL of a large pretrained VLA with LoRA; open for continual imitation under a small memory.'},
    {'id': 'r2x:3', 'bottleneck': 'r2-B1', 'role': 'x', 'refutes': 'r2-B1', 'contrary': False, 'shows_target_reached': False,
     'source': 'Liu, Kim, Liu, Liu & Zhu, Pretrained VLAs are Surprisingly Resistant to Forgetting (Appendix B.1 and Table 1; the '
               'harvester\'s own source, re-read)',
     'version': 'arXiv v2, 17 Mar 2026', 'url': 'https://arxiv.org/abs/2603.03818v2',
     'quote': ['Following the same setting as LIBERO (Liu et al., 2023b), we use a replay buffer size = 1000 transitions (i.e., '
               'state-action pairs) per task across all methods, which is approximately 15 −20% of the full task dataset.',
               'Pi0 0.879 ± 0.008 0.019 ± 0.019 0.897 ± 0.011 −0.011 ± 0.034 0.732 ± 0.015 −0.005 ± 0.010 0.563 ± 0.028 '
               '−0.068 ± 0.018 0.768 ± 0.017 −0.016 ± 0.022',
               'When the buffer size is 2% (100 samples per task), pretrained VLAs such as Pi0 and GR00T still have low NBT '
               'around 0.1–0.2'],
     'raw_file': 'r2/txt/2603.03818v2.txt',
     'agent_note': 'Re-check of the harvester\'s named metric. The 2% budget (100 samples per task) is not LIBERO\'s protocol: '
                   'LIBERO\'s own setting is 1000 transitions per task (about 15-20% of a task\'s data, i.e. still a small '
                   'absolute memory), and under it Pi0 averages NBT -0.016 over the four LIBERO suites (target reached; GR00T '
                   '0.027). The harvester reported this (r2:7) but chose the non-standard 2% budget as the named metric, which is '
                   'the setting where the bottleneck stays open. The "20%" is the paper\'s round figure; the appendix says '
                   'approximately 15-20% and counts transitions, not demonstrations. Supports CONTESTED more than OPEN.'},
    {'id': 'r2x:4', 'bottleneck': 'r2-B1', 'role': 'x', 'refutes': 'r2-B1', 'contrary': False, 'shows_target_reached': False,
     'source': 'Chen et al., PHASER (Table 1; the harvester\'s own source, re-read)',
     'version': 'arXiv v2, 3 Jun 2026', 'url': 'https://arxiv.org/abs/2606.03598v2',
     'quote': ['MIR 81.6 15.6 82.2 10.0 76.2 10.4 29.8 32.2 73.6 9.3 41.0 19.6',
               'iCaRL 50.2 42.0 46.4 45.0 70.0 8.9 37.0 23.3 65.0 13.0 33.0 6.0',
               'All replay methods share per-task buffer within each cell (OV-7B: B=110/180; QG/QO-3B: B=1000)'],
     'raw_file': 'r2/txt/2606.03598v2.txt',
     'agent_note': 'Re-check of r2:8. The harvester gave the NBT gaps of PHASER (10.0 on OpenVLA-OFT-7B LIBERO-Long; 11.1 and '
                   '12.4 on the 3B backbones) as the gaps to NBT 0. They are not the best NBT in the table: on OV-7B LIBERO-Long '
                   'plain ER has NBT -5.6 (no forgetting, but final success only 54.6, harvester-quoted row) and MIR ties PHASER '
                   'at 10.0; on QwenOFT-3B LIBERO-Long iCaRL has NBT 6.0 (success 33.0). Low NBT with low success means the model '
                   'did not learn the later tasks well, so NBT alone is a weak target; the harvester conflated the best method by '
                   'success with the best forgetting number. Minor.'},

    # ---------------- r2-B2: erosion of pretrained VLM capabilities when fine-tuning into a VLA
    {'id': 'r2x:5', 'bottleneck': 'r2-B2', 'role': 'x', 'refutes': 'r2-B2', 'contrary': True, 'shows_target_reached': False,
     'source': 'Yang, Li, Wang, ... Pang, InstructVLA: Vision-Language-Action Instruction Tuning from Understanding to Manipulation '
               '(ICLR 2026; Table 1)',
     'version': 'arXiv v2, 3 Mar 2026 (v1 23 Jul 2025); header "Published as a conference paper at ICLR 2026"',
     'url': 'https://arxiv.org/abs/2507.17520v2',
     'quote': ['InstructVLA surpasses baseline VLMs on multi-modal tasks',
               'Eagle2 (Li et al., 2025c) 1.5B 43.1 53.8 56.4 1572.1 818 45.8 74.9 79.1 88.0 65.8 79.3 82.3 63.1',
               'InstructVLA-Generalist(S.) 1.5B 43.8 54.0 56.0 1548.0 829 42.8 76.3 78.2 86.0 63.7 78.9 82.9 63.5',
               'it not only outperforms the co-trained baseline Magma, but is also comparable to its base model Eagle2',
               'employs multimodal training with mixture-of-experts adaptation to jointly optimize embodied reasoning and action '
               'generation on both standard VLM corpora and a curated 650K-sample VLA-IT dataset'],
     'raw_file': R + '2507.17520v2.txt',
     'agent_note': 'Contrary, and a better "best" than the harvester\'s. Columns: MMMU, MM-Vet, MMStar, MME-P, OCRBench, HallB, '
                   'MMB, TextVQA, DocVQA, InfoVQA, AI2D, ChartQA, RWQA. Against its own base VLM Eagle2 (1.5B), InstructVLA-'
                   'Generalist(S.) is at or above the base on 6 of 13 (MMMU +0.7, MM-Vet +0.2, OCRBench +11, MMB +1.4, ChartQA '
                   '+0.6, RWQA +0.4) and below on 7 by 0.2-3.0 points (HallB -3.0, InfoVQA -2.1, DocVQA -2.0, TextVQA -0.9, AI2D '
                   '-0.4, MMStar -0.4) and MME-P -24.1 of 1572. The harvester\'s best (VLM2VLA) was below its base on 9 of 12 by '
                   'up to 11.1. Not the target (the base on every benchmark), and it relies on co-training with VLM corpora, a '
                   'family the harvester listed; but the erosion is down to a few points, i.e. roughly within benchmark noise.'},
    {'id': 'r2x:6', 'bottleneck': 'r2-B2', 'role': 'x', 'refutes': 'r2-B2', 'contrary': True, 'shows_target_reached': False,
     'source': 'Zhang, Luo, Hu, ... Chen (Tsinghua, ByteDance Seed), UAM: A Dual-Stream Perspective on Forgetting in VLA Training '
               '(Table 2)',
     'version': 'arXiv v2, 18 May 2026 (v1 15 May 2026)', 'url': 'https://arxiv.org/abs/2605.15735v2',
     'quote': ['with no parameter freezing, no gradient stopping, and no auxiliary VL co-training, UAM retains over 95% of the '
               'underlying VLM’s multimodal capability',
               'we initialize both the VLM expert and the dorsal expert using the pre-trained Bagel [13] checkpoint',
               'BAGEL [13] 7B MoT 55.3 1687 2388 85.0 67.2 73.1 — —',
               'UAM(Ours) 7B MoT 53.7 1607 2289 83.7 63.4 68.2 61.3 84.2'],
     'raw_file': R + '2605.15735v2.txt',
     'agent_note': 'Contrary on the mechanism: action-only end-to-end training (no frozen weights, no VQA co-training) keeps '
                   'most of the VLM, where OpenVLA-style training loses all of it. Against its base BAGEL: MMMU 53.7 vs 55.3 '
                   '(-1.6), MME-P 1607 vs 1687, MME-S 2289 vs 2388, MMBench 83.7 vs 85.0 (-1.3), MM-Vet 63.4 vs 67.2 (-3.8), '
                   'MathVista 68.2 vs 73.1 (-4.9). Below the base on all six comparable benchmarks, so the target is not reached; '
                   'the paper itself calls the loss an "embodiment tax" of under 5%.'},
    {'id': 'r2x:7', 'bottleneck': 'r2-B2', 'role': 'x', 'refutes': 'r2-B2', 'contrary': True, 'shows_target_reached': False,
     'source': 'Yu, Lian, Lin, ... Chen, TwinBrainVLA: Unleashing the Potential of Generalist VLMs for Embodied Tasks via '
               'Asymmetric Mixture-of-Transformers',
     'version': 'arXiv v2, 30 Jan 2026 (v1 20 Jan 2026); "Work in progress"', 'url': 'https://arxiv.org/abs/2601.14133v2',
     'quote': ['coordinates two isomorphic VLM pathways: a frozen generalist (also called "Left Brain") and a trainable specialist '
               '(also called "Right Brain").',
               'the POPE score of Qwen3-VL drops from 88.87% to near-zero (0.04%).',
               'While Co-Training is frequently suggested as a countermeasure, our experiments show that it merely mitigates the '
               'symptoms rather than providing a fundamental solution.'],
     'raw_file': R + '2601.14133v2.txt',
     'agent_note': 'A misframing argument, weak: if the VLA keeps an untouched frozen copy of the VLM beside a trainable copy, '
                   'the VLM\'s capabilities are retained by construction, so the question becomes the cost (two VLM pathways) and '
                   'whether the action pathway can use them, not erosion as such. The paper reports no VQA scores for its own '
                   'model, so nothing here shows the named metric. The same paper supports the bottleneck strongly: plain VLA '
                   'training takes POPE from 88.87% to 0.04%, and co-training only "mitigates the symptoms".'},

    # ---------------- r2-B3: generalisation under distribution shift
    {'id': 'r2x:8', 'bottleneck': 'r2-B3', 'role': 'x', 'refutes': 'r2-B3', 'contrary': True, 'shows_target_reached': False,
     'source': 'Tsai, Jhang, Tai, Lai, Wong, Hsu & Chen, Direct Action-Head Injection of A Grounded 3D Point Unlocks Spatial and '
               'Task Generalization (Table 1)',
     'version': 'arXiv v1, 26 Jun 2026', 'url': 'https://arxiv.org/abs/2606.27663v1',
     'quote': ['On LIBERO-PRO, our method improves the average success rate of GR00T-N1.6 from 31.2 to 77.5 points under task '
               'perturbation and from 28.1 to 60.2 points under position perturbation',
               'π0.5 [5] 94.8 96.0 95.4 20.0 54.6 37.3 36.0 58.0 47.0',
               'π0.5 + Ours 97.0 98.2 97.6 70.6 81.2 75.9 75.0 69.4 72.2',
               'We obtain 2D oracle target points from simulator-provided segmentation and object-center information'],
     'raw_file': R + '2606.27663v1.txt',
     'agent_note': 'Contrary on the harvester\'s "best". Columns: LIBERO in-distribution (Object, Spatial, Avg), LIBERO-PRO task '
                   'perturbation (Object, Spatial, Avg), LIBERO-PRO position perturbation (Object, Spatial, Avg). On LIBERO-Spatial '
                   'under position perturbation plain pi0.5 already scores 58.0 and pi0.5 with the 3D-point module 69.4 (in '
                   'distribution 98.2: gap 28.8), against the harvester\'s best 22.6 (gap 75.8) from Anchor-Align, whose table '
                   'compares only small-backbone models (0.5B). Caveats: the module receives oracle 2D target points from the '
                   'simulator (the paper lifts them to 3D and argues a detector or VLM could supply them), and "position '
                   'perturbation" here and Anchor-Align\'s "Pos. Swap" are both LIBERO-PRO\'s position axis as far as the texts '
                   'say, but identical protocols were not verified. Target (no loss against the unperturbed 98.4) not reached.'},
    {'id': 'r2x:9', 'bottleneck': 'r2-B3', 'role': 'x', 'refutes': 'r2-B3', 'contrary': True, 'shows_target_reached': False,
     'source': 'AgiBot Research Team, GE-Act 2.0: Pretraining and Scaling a World-Action Model for Robotic Manipulation (company '
               'technical report; Appendix Table 5)',
     'version': 'arXiv v1, 4 Sep 2026 (comment "Technical report by the AgiBot Research Team")', 'url': 'https://arxiv.org/abs/2609.05588v1',
     'quote': ['We SFT GE-Act 2.0 on the standard LIBERO training data and evaluate it on seven LIBERO-Plus perturbation axes',
               'StarVLA 52.5 49.8 88.5 95.7 95.7 73.0 76.9 74.1 π0.5 78.4 73.6 80.8 96.2 94.1 89.0 84.5 84.4 GE-Act 2.0 94.1 '
               '50.7 81.4 94.0 60.5 95.5 83.1 80.4',
               'Robot-state and especially background perturbations remain the principal weaknesses, showing that robustness is '
               'not yet uniform across the seven axes.'],
     'raw_file': R + '2609.05588v1.txt',
     'agent_note': 'Contrary on the harvester\'s "best" for the robot-initial-state axis. Columns: Camera, Robot, Language, Light, '
                   'Background, Noise, Layout, Overall (over all 10,030 LIBERO-Plus instances). Trained only on standard LIBERO, '
                   'pi0.5 scores 73.6 under robot-initial-state perturbation and 84.4 overall; GE-Act 2.0 scores 94.1 under camera '
                   'change. The harvester\'s best robot-init number was 59.1 (Anchor-Align, LIBERO-Spatial suite only; not the '
                   'same subset, so not strictly comparable). The source itself says robot-state shifts remain a principal '
                   'weakness; no unperturbed reference is given in this table, and pi0.5\'s standard LIBERO scores are in the 90s, '
                   'so the robot-state gap is still about 20 points. Narrows the gap; does not close it.'},
    {'id': 'r2x:10', 'bottleneck': 'r2-B3', 'role': 'x', 'refutes': 'r2-B3', 'contrary': True, 'shows_target_reached': False,
     'source': 'Li, Zhang, Zhai, Lin & Wang, VLA Models Are More Generalizable Than You Think: Revisiting Physical and Spatial '
               'Modeling (CVPR 2026, open-access version)',
     'version': 'CVPR 2026 open access (CVF watermark: identical to the accepted version); no arXiv version checked',
     'url': 'https://openaccess.thecvf.com/content/CVPR2026/papers/Li_VLA_Models_Are_More_Generalizable_Than_You_Think_Revisiting_Physical_CVPR_2026_paper.pdf',
     'quote': ['We show that this brittleness primarily arises from misalignment in Spatial Modeling, rather than Physical Modeling.',
               'improves Libero viewpoint accuracy from 48.5% to 87.1% with only 4K parameters.',
               'Together, these results reveal substantial untapped robustness in pretrained VLA models and demonstrate that '
               'targeted, minimal visual adaptation is sufficient [...] to restore viewpoint generalization.'],
     'raw_file': R + 'cvpr2026_li_vla_more_generalizable.txt',
     'agent_note': 'A partial misframing argument for the viewpoint axis: the collapse under a new camera is a misaligned visual '
                   'encoder, repaired by a one-shot adaptation of 4K-4.7M parameters (48.5% -> 87.1%, 90.8% with FLA). It needs '
                   'one demonstration in the new viewpoint, so it is adaptation, not zero-shot generalisation, and it does not '
                   'touch the named metrics (position swap, robot initial state).'},

    # ---------------- r2-B4: transfer to new embodiments
    {'id': 'r2x:11', 'bottleneck': 'r2-B4', 'role': 'x', 'refutes': 'r2-B4', 'contrary': True, 'shows_target_reached': True,
     'source': 'Piseno, Tevet & Liu (Stanford), Cloak: Zero-Shot Cross-Embodiment Manipulation by Masking the End-Effector from the '
               'VLA (CoRL 2026; Tables 1 and 4)',
     'version': 'arXiv v2, 25 Sep 2026 (v1 22 Jun 2026); footer "10th Conference on Robot Learning (CoRL 2026)"',
     'url': 'https://arxiv.org/abs/2606.22836v2',
     'quote': ['Cloak-VLA transfers zero-shot to various unseen embodiments, including another gripper, another arm, and a '
               'five-fingered hand, while preserving the source embodiment’s performance.',
               'Across all three unseen embodiments, Cloak-VLA remains close to the source embodiment progression rate of 88.0, '
               'to 85.1 on the UMI gripper, 86.3 on the YAM arm, and 81.8 on the Sharpa hand.',
               'Cloak-VLA (ours) 97.9 ±2.1 91.7 ±6.0 70.8 ±9.6 91.8 ±4.3 88.0 ±3.3',
               'Cloak-VLA (ours) 93.8 ±3.3 97.2 ±2.8 70.8 ±11.9 83.4 ±6.5 86.3 ±3.7',
               'For each task, we generate 12 randomized instances of objects, placements, and prompts, for a total of 48 trials.',
               'For the Sharpa, we designed a camera mount with an offset that places the fingers at roughly the same image '
               'location as the original gripper.'],
     'raw_file': R + '2606.22836v2.txt',
     'agent_note': 'Target reached on the harvester\'s named quantity: mean task progress (partial credit) after a zero-shot '
                   'full-embodiment change, against progress on the source embodiment, in the real world. Cloak-VLA (pi0.5 '
                   'fine-tuned on DROID only, Franka + Robotiq) on the unseen YAM arm and gripper: 86.3 +/- 3.7 against 88.0 +/- '
                   '3.3 on the source (difference 1.7, inside one SEM); binary success 70.8 +/- 6.6 against 75.0 +/- 6.3 (Table 4). '
                   'ZETA\'s best full-change real result, the harvester\'s B-c, was 81.9 against 100.0. Differences from ZETA: '
                   'another benchmark (4 DROID-style tasks, 48 trials per embodiment), tip-pose retargeting through inverse '
                   'kinematics of the known target body, and wrist-camera masking; the five-fingered hand stays 6.2 points below '
                   'the source (81.8 vs 88.0) with a custom camera mount. Fair summary: reached for arm-and-gripper changes that '
                   'IK can bridge; open for bodies with a different grasp mechanism.'},
    {'id': 'r2x:12', 'bottleneck': 'r2-B4', 'role': 'x', 'refutes': 'r2-B4', 'contrary': False, 'shows_target_reached': False,
     'source': 'Yan et al., ZETA (Section 5.1 and Table 4; the harvester\'s own source, re-read)',
     'version': 'arXiv v2, 5 Sep 2026', 'url': 'https://arxiv.org/abs/2609.02546v2',
     'quote': ['Table 4: Real-world results for RQ1. Each entry averages task progress on open the fryer and water the flower.',
               'with 10 trials per task–embodiment pair, yielding 2 × 7 × 10 = 140 real-world rollouts per model.'],
     'raw_file': 'r2/txt/2609.02546v2.txt',
     'agent_note': 'Re-check of r2:33. "140 rollouts per model" is the total over all seven embodiments; the FULL cell (81.9) '
                   'rests on two tasks and 10 trials per task-embodiment pair, a small subset of the 140. The number is quoted '
                   'correctly; its precision is overstated by attaching the 140 to the FULL gap.'},

    # ---------------- r2-B5: sim-to-real transfer
    {'id': 'r2x:13', 'bottleneck': 'r2-B5', 'role': 'x', 'refutes': 'r2-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'Tian, Yang, Xie, Cai, Shi, ... Pang (Shanghai AI Laboratory), InternData-A1: Pioneering High-Fidelity Synthetic Data '
               'for Pre-training Generalist Policy (CVPR 2026)',
     'version': 'arXiv v1, 20 Nov 2025 (CVPR 2026 per the CVF open-access listing found by search)', 'url': 'https://arxiv.org/abs/2511.16651v1',
     'quote': ['This paper provides the first evidence that synthetic data alone can match the performance of the strongest '
               'π-dataset in pre-training a VLA model',
               'for regular tasks such as Sort Rubbish and [...] Wipe Stain, which mainly involve basic skills (pick, place, move), '
               '200 simulated episodes already achieve performance comparable to 200 real ones.',
               'the simulation-to-real data ratio for equivalent performance narrows to within 8:1—and in some cases, even '
               'approaches 1:1.',
               'ten selected simulated tasks achieve direct sim-to-real transfer with an average success rate exceeding 50%.'],
     'raw_file': R + '2511.16651v1.txt',
     'agent_note': 'A misframing argument plus partial evidence. The harvester\'s target was "no transfer loss (real equal to '
                   'simulated success)" for one policy; this source frames the target as simulated data being worth real data, '
                   'and reports it reached at 1:1 on two basic tasks and within 8:1 on two harder ones (30 rollouts each), and '
                   'synthetic-only pretraining matching pi0\'s pretraining. It does not report a policy\'s simulated success '
                   'beside its real success, so the named metric is not shown; zero-shot real success on ten tasks is above 50% '
                   'on average, not near 100%.'},
    {'id': 'r2x:14', 'bottleneck': 'r2-B5', 'role': 'x', 'refutes': 'r2-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'Kim, Saito, Kim, Ikeuchi, Choo & Matsushita (KAIST, Microsoft Research Asia), Object-Centric Residual RL for '
               'Zero-Shot Sim-to-Real VLA Enhancement (Table 1)',
     'version': 'arXiv v1, 17 Jun 2026', 'url': 'https://arxiv.org/abs/2606.18953v1',
     'quote': ['Close Drawer 11.3/20 ±3.2 19.7/20 ±0.6 14/20 20/20',
               'Average 7.6/20 ±1.7 17.2/20 ±0.9 8.4/20 15.2/20',
               'On the real robot, the sim-trained residual transfers zero-shot to all five tasks, raising the average success '
               'rate from 42% to 76% without any real-world RL or fine-tuning.'],
     'raw_file': R + '2606.18953v1.txt',
     'agent_note': 'Columns: simulation Base, +Residual; real robot Base, +Residual. The simulation-trained residual reaches 17.2/20 '
                   '(86%) in simulation and 15.2/20 (76%) on the real robot: a transfer loss of 10 points, against the '
                   'harvester\'s 28.0; on Close Drawer there is no loss (19.7/20 sim, 20/20 real). Only the residual is trained in '
                   'simulation; the base VLA is trained on real teleoperation, and the residual sees object poses, not images. '
                   'Narrows the gap; the named target (no loss on average) is not reached.'},
    {'id': 'r2x:15', 'bottleneck': 'r2-B5', 'role': 'x', 'refutes': 'r2-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'Jain, Zhang, Arora, Chen, Torne, Irshad, ... (14 authors), PolaRiS: Scalable Real-to-Sim Evaluations for Generalist Robot Policies',
     'version': 'arXiv v2, 30 Dec 2025 (v1 18 Dec 2025)', 'url': 'https://arxiv.org/abs/2512.16881v2',
     'quote': ['PolaRiS evaluations match the real-world performance of state-of-the-art generalist policies out of the box with an '
               'average Pearson correlation of r= 0.9. PolaRiS evaluations also strongly correlate (r= 0.98) with policy scores '
               'in RoboArena',
               'the worst-case correlation across all six tested environments is r= 0.81.',
               'we emphasize that the simulated evaluations in our experiments only capture a small subset of the capabilities '
               'tested in RoboArena'],
     'raw_file': R + '2512.16881v2.txt',
     'agent_note': 'Contrary on the evaluation-predictivity half of r2-B5. The harvester\'s best sim-real correlation was 0.84 '
                   '(X2Real, a company report) against the ideal 1.0; PolaRiS reports 0.9 on average over six real environments '
                   '(worst 0.81) and 0.98 against RoboArena scores, with the caveat that it covers a subset of RoboArena\'s '
                   'capabilities. 0.98 "approaches 1.0" but is not 1.0, and it is a correlation across policies, which says '
                   'nothing about the transfer loss of a sim-trained policy (the other named metric).'},
    {'id': 'r2x:16', 'bottleneck': 'r2-B5', 'role': 'x', 'refutes': 'r2-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'Wang, Hao, Hu, Li, Ma, Ramani, Moon & Kwon (Purdue, Samsung SDS), ReVeal: A Reconstruction-Aware Real-to-Sim '
               'Framework for VLA Policy Evaluation; and Ranawaka et al., SimFoundry',
     'version': 'ReVeal arXiv v1, 20 Sep 2026', 'url': 'https://arxiv.org/abs/2609.23910v1',
     'quote': ['achieves the highest Pearson correlation (r = 0.960) and the lowest MMRV (0.102) and MAE (0.050).'],
     'raw_file': R + '2609.23910v1.txt',
     'agent_note': 'Corroborates r2x:15: a September 2026 real-to-sim pipeline reaches r = 0.960 between simulated and real '
                   'success for pi0.5, GR00T N1.7 and SmolVLA (the best of its reconstruction pipelines). SimFoundry (arXiv '
                   '2606.28276 v4, 5 Aug 2026; claim r2x:17) reports 0.911, and 0.95 with sub-task scoring. Correlations of '
                   '0.91-0.98 are now reported; none is 1.0.'},
    {'id': 'r2x:17', 'bottleneck': 'r2-B5', 'role': 'x', 'refutes': 'r2-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'Ranawaka, Wong, Pai, Chu, Dai, Moghani, ... (18 authors), SimFoundry: Modular and Automated Scene Generation for Policy Learning and Evaluation',
     'version': 'arXiv v4, 5 Aug 2026 (v1 26 Jun 2026, v2 4 Jul 2026, v3 21 Jul 2026)', 'url': 'https://arxiv.org/abs/2606.28276v4',
     'quote': ['with a mean Pearson correlation of 0.911 and MMRV of 0.018',
               'We introduce a sub-task evaluation procedure that increases policy eval correlations from a mean Pearson score of '
               '0.90 to 0.95.'],
     'raw_file': R + '2606.28276v4.txt',
     'agent_note': 'See r2x:16. Seven tasks, five policy types (pi, GR00T and DreamZero families).'},

    # ---------------- r2-B6: data scarcity and cost
    {'id': 'r2x:18', 'bottleneck': 'r2-B6', 'role': 'x', 'refutes': 'r2-B6', 'contrary': True, 'shows_target_reached': False,
     'source': 'Generalist AI (company statement), GEN-1: Scaling Embodied Foundation Models to Mastery (blog)',
     'version': 'dated April 2, 2026 (no later update shown); fetched 2026-09-30', 'url': 'https://generalistai.com/blog/gen-1',
     'quote': ['It improves average success rates to 99% on tasks where previous models achieve 64%, completes tasks roughly 3x '
               'faster than state of the art, and requires only 1 hour of robot data for each of these results.',
               'trained on our dataset which now includes over half a million hours of high-fidelity physical interaction data.',
               'the base foundation model is trained without any robot data—it instead uses data from low-cost wearable devices '
               'on humans doing millions of activities',
               'not all tasks that we have attempted are able to hit these rates.'],
     'raw_file': R + 'generalistai_gen-1.txt',
     'agent_note': 'A company claim, not peer reviewed, with no benchmark or independent evaluation. Two bearings on r2-B6. (1) The '
                   'best corpus is larger than the harvester\'s: over 500,000 hours (about 57 years) of physical interaction data '
                   'from wearables, against the harvester\'s 100,000 hours (Xiaomi, UMI) and 3,000 hours of robot data; still a '
                   'factor of about 1,750 short of Goldberg\'s 100,000 years, so the (weak, cross-source) target is not reached. '
                   '(2) Misframing: if pretraining on cheap human wearable data needs only about 1 hour of robot data per task for '
                   '99% success, the scarce resource is not robot data. Tasks are simple and short; the company says not all '
                   'attempted tasks reach these rates.'},
    {'id': 'r2x:19', 'bottleneck': 'r2-B6', 'role': 'x', 'refutes': 'r2-B6', 'contrary': True, 'shows_target_reached': False,
     'source': 'Generalist AI (company statement), GEN-0 / Embodied Foundation Models That Scale with Physical Interaction (blog)',
     'version': 'dated 4 Nov 2025 (URL path); fetched 2026-09-30', 'url': 'https://generalistai.com/blog/nov-04-2025-GEN-0',
     'quote': ['is pretrained on our in-house robotics dataset, which includes over 270,000 hours of real-world diverse manipulation '
               'data, growing at a rate of 10,000 hours a week and accelerating.'],
     'raw_file': R + 'generalistai_gen0_2025-11-04.txt',
     'agent_note': 'Earlier company figure, supporting r2x:18: already in November 2025 a reported corpus (270,000 hours) was 2.7x '
                   'the harvester\'s best (100,000 hours), growing at 10,000 hours a week (about 1.1 years of data per week). At '
                   'that rate the harvester\'s gap to 100,000 years would take roughly 1,700 years, so it is not closed by '
                   'collection alone; the argument is that the gap is the wrong measure.'},

    # ---------------- r2-B7: long-horizon tasks with one generalist policy
    {'id': 'r2x:20', 'bottleneck': 'r2-B7', 'role': 'x', 'refutes': 'r2-B7', 'contrary': True, 'shows_target_reached': False,
     'source': 'Physical Intelligence (Amin, Aniceto, ... Levine, ... Zhou), pi*0.6: a VLA That Learns From Experience',
     'version': 'arXiv v2, 19 Nov 2025 (v1 18 Nov 2025); company paper', 'url': 'https://arxiv.org/abs/2511.14759v2',
     'quote': ['we were able to run it to make espresso drinks for 13 hours straight, fold novel laundry items in a new home for '
               'over two hours without interruptions, and assemble boxes that are used for real packaging in a factory.',
               'On all of the tasks except diverse laundry, the success rate of the final π∗ 0.6 model is in the 90%+ range.'],
     'raw_file': R + '2511.14759v2.txt',
     'agent_note': 'Contrary for narrow long-horizon tasks in deployment: multi-step real tasks (espresso drinks, box assembly, '
                   'laundry) at 90%+ success after task-specific RL with human corrections, and runs of hours. This repeats, '
                   'with a stronger source, the harvester\'s own concession (RoboFolDeX 95%). It is one generalist model '
                   'specialised per task, not one policy across 50 household activities, so the named metric (BEHAVIOR full '
                   'success, breadth) is not touched. Company paper.'},
    {'id': 'r2x:21', 'bottleneck': 'r2-B7', 'role': 'x', 'refutes': 'r2-B7', 'contrary': True, 'shows_target_reached': False,
     'source': 'Generalist AI (company statement), GEN-1 blog, Reliability section',
     'version': 'dated April 2, 2026', 'url': 'https://generalistai.com/blog/gen-1',
     'quote': ['can perform several tasks at high levels of reliability over long durations without intervention. We show here 6 '
               'tasks: kitting auto parts for more than an hour, folding t-shirts 86 times in a row, servicing robot vacuums over '
               '200 times in a row, packing blocks over 1,800 times in a row, folding boxes over 200 times in a row, and packing '
               'phones over 100 times in a row.'],
     'raw_file': R + 'generalistai_gen-1.txt',
     'agent_note': 'Company claim of long unattended runs on six narrow tasks (videos, no benchmark). Same reading as r2x:20: '
                   'reliability over time on repeated narrow tasks is being reached; breadth over many long household tasks is '
                   'not.'},
    {'id': 'r2x:22', 'bottleneck': 'r2-B7', 'role': 'x', 'refutes': 'r2-B7', 'contrary': True, 'shows_target_reached': False,
     'source': 'Choe, Sangeetha, Coogan & Kousik, Make Your VLA More Robust Without More Data By Interleaving Motion Planning (MPVI; BEHAVIOR-1K, 50 tasks)',
     'version': 'arXiv v1, 31 May 2026', 'url': 'https://arxiv.org/abs/2606.00985v1',
     'quote': ['These challenges persist despite finetuning on large human teleoperated mobile manipulation data, indicating that '
               'more data alone may not resolve the problem.',
               'MPVI increases the mean Q-Score across all 50 tasks by 113% with progress gains on 31 tasks',
               'the latter relies on human-engineered, task-specific heuristics that limit generalization beyond the evaluation '
               'tasks.'],
     'raw_file': R + '2606.00985v1.txt',
     'agent_note': 'A misframing argument on the "one generalist policy" part of r2-B7: interleaving a classical motion planner '
                   'and detector with a pi0.5 VLA more than doubles task progress on the same 50 BEHAVIOR tasks without more '
                   'data. It also notes the 1st-place 12.4% used task-specific heuristics. The absolute Q-score is only in a figure, '
                   'so the named metric (full success 1.0) is not shown reached.'},
    {'id': 'r2x:23', 'bottleneck': 'r2-B7', 'role': 'x', 'refutes': 'r2-B7', 'contrary': False, 'shows_target_reached': False,
     'source': 'Stanford Vision and Learning Lab, 2026 BEHAVIOR Challenge (programme page)',
     'version': 'live page, (c) 2026, fetched 2026-09-30; no last-updated date shown',
     'url': 'https://behavior.stanford.edu/challenge/index.html',
     'quote': ['100 full-length household tasks',
               'The 2026 challenge is intended as a shared benchmark for testing robot foundation models, imitation learning, '
               'reinforcement learning, task and motion planning, memory systems, SLAM, and LLM-assisted policies under the same '
               'realistic evaluation protocol.'],
     'raw_file': R + 'behavior_challenge_2026_index.txt',
     'agent_note': 'Re-check of the named benchmark: the 2026 edition doubles the task set to 100 and was still open on the day '
                   '(submission deadline 16 Oct 2026 on the page), so no newer full-success number exists; 0.124 (2025, 50 tasks) '
                   'stands. The organisers now admit planners, SLAM and LLM-assisted systems, not only one generalist policy.'},

    # ---------------- r2-B8: on-robot inference latency and compute
    {'id': 'r2x:24', 'bottleneck': 'r2-B8', 'role': 'x', 'refutes': 'r2-B8', 'contrary': True, 'shows_target_reached': True,
     'source': 'NVIDIA Jetson AI Lab (vendor tutorial), OpenPi pi0.5 on Jetson Thor',
     'version': 'live page, (c) 2026 NVIDIA; pins openpi commit 15a9616 of 2026-06-16; no last-updated date shown; fetched 2026-09-30',
     'url': 'https://www.jetson-ai-lab.com/tutorials/openpi_on_thor/',
     'quote': ['Benchmarked on Jetson AGX Thor Developer Kit (JetPack 7.2, MAXN power mode), [...] action horizon 10:',
               'TensorRT FP8 ~54 ~53 2.4x',
               'TensorRT FP8 + NVFP4 ~49 ~48 ~2.7x',
               'Total inference time: 48.84 ± 0.16 ms',
               'Fastest; accuracy typically ≈ 0.99, see Step 12'],
     'raw_file': R + 'jetson_ai_lab_openpi_on_thor.txt',
     'agent_note': 'Target reached on Jetson Thor, one of the two devices in the harvester\'s B-c table. pi0.5 (the pi05_libero '
                   'checkpoint) runs end to end in about 49 ms (FP8 + NVFP4) or 54 ms (FP8, cosine 0.9995 to PyTorch): about 18-20 '
                   'Hz, inside the 10-20 Hz target, against the harvester\'s best on Thor of 7.59 Hz (Jetson-PI, 131.8 ms reaction '
                   'time) and 20 Hz only off-board. Caveats: a vendor tutorial; latency per inference with a 10-step action '
                   'horizon, not a closed-loop success-rate evaluation (accuracy checked only by cosine similarity of actions); '
                   'Thor draws more power than Orin. Not shown on Jetson Orin, the device the harvester named first (RhinoVLA, '
                   'r2x:25, says Orin "has limited compute headroom for 10 Hz VLA inference"). Fair summary: closed on Thor, open '
                   'on Orin-class compute.'},
    {'id': 'r2x:25', 'bottleneck': 'r2-B8', 'role': 'x', 'refutes': 'r2-B8', 'contrary': True, 'shows_target_reached': False,
     'source': 'Huixi Technology (Zhang, Zhou, Ding, He, ...), RhinoVLA Technical Report (company technical report)',
     'version': 'arXiv v4, 17 Jul 2026 (v1 5 Jun 2026, v2 30 Jun 2026, v3 8 Jul 2026)', 'url': 'https://arxiv.org/abs/2606.07383v4',
     'quote': ['RhinoVLA achieves downstream performance comparable to π0.5 at a similar parameter scale, while reaching 11.69 Hz '
               'end-to-end inference on Huixi R1, meeting the 10 Hz real-time closed-loop control target.',
               'Orin has limited compute headroom for 10 Hz VLA inference, while Thor offers higher performance at a much higher '
               'system cost.'],
     'raw_file': R + '2606.07383v4.txt',
     'agent_note': 'Contrary, weaker: a pi0.5-scale model co-designed with an edge SoC reaches 11.69 Hz end to end, the low end of '
                   'the target. Not pi0.5 itself and not a Jetson, so not the named metric. It supports the harvester on Orin and '
                   'frames Thor\'s success as a cost question.'},
    {'id': 'r2x:26', 'bottleneck': 'r2-B8', 'role': 'x', 'refutes': 'r2-B8', 'contrary': True, 'shows_target_reached': False,
     'source': 'Independent developer post on the NVIDIA Developer Forums ("Real-Time Inference on Thor & RTX ..."), and the PhyAI '
               'paper\'s third-party measurement of the same engine (FlashRT)',
     'version': 'forum post created 2026-05-02 (edited the same day), read from the Discourse JSON',
     'url': 'https://forums.developer.nvidia.com/t/real-time-inference-on-thor-rtx-pi0-5-gr00t-n1-6-1-7-thor-23-hz-rtx-5090-50-80hz/368788',
     'quote': ['Pi0.5 — Jetson AGX Thor (SM110): 44 ms (23 Hz)',
               'Pi0 — Jetson AGX Thor (SM110): 46 ms (22 Hz)'],
     'raw_file': R + 'nvidia_forum_368788.txt',
     'agent_note': 'Unreviewed developer claim, recorded only as corroboration of r2x:24: pi0.5 at 44 ms on Thor. The PhyAI paper '
                   '(r2x:27) measured the same engine\'s pi0 at 49.5 ms on Thor in FP8. Not counted as target evidence on its own.'},
    {'id': 'r2x:27', 'bottleneck': 'r2-B8', 'role': 'x', 'refutes': 'r2-B8', 'contrary': True, 'shows_target_reached': False,
     'source': 'Wang, Xu, Cai, Sun, Zhang, Qian, ... (26 authors), PhyAI: Real-Time Physical AI at the Edge, Scalable Rollouts in the Cloud (Section 5.2)',
     'version': 'arXiv v3, 14 Aug 2026 (v1 4 Aug 2026, v2 5 Aug 2026)', 'url': 'https://arxiv.org/abs/2608.03682v3',
     'quote': ['The two PI0 FlashRT measurements use FP8, with 49.5 ms on Thor and 19.7 ms on RTX 5090, so they are not '
               'precision-matched to the corresponding PhyAI results.'],
     'raw_file': R + '2608.03682v3.txt',
     'agent_note': 'Independent (paper) measurement of a pi0 runtime on Jetson Thor at 49.5 ms (about 20 Hz), consistent with the '
                   'vendor figure in r2x:24. pi0, not pi0.5.'},
    {'id': 'r2x:28', 'bottleneck': 'r2-B8', 'role': 'x', 'refutes': 'r2-B8', 'contrary': True, 'shows_target_reached': False,
     'source': 'Figure AI (company statement), Helix: A Vision-Language-Action Model for Generalist Humanoid Control',
     'version': 'dated February 20, 2025; fetched 2026-09-30', 'url': 'https://www.figure.ai/news/helix',
     'quote': ['Helix is the first VLA that runs entirely onboard embedded low-power-consumption GPUs, making it immediately ready '
               'for commercial deployment.',
               'System 2 (S2): An onboard internet-pretrained VLM operating at 7-9 Hz for scene understanding and language '
               'comprehension',
               'S1 executes as a separate real-time process, maintaining the critical 200Hz control loop required for smooth '
               'whole upper body action. It takes both the latest observation and the most recent S2 latent vector.'],
     'raw_file': R + 'figure_helix.txt',
     'agent_note': 'A misframing argument from a deployed (company-claimed) system: the large VLM need not run at the control '
                   'rate. Helix runs its VLM on board at 7-9 Hz, below the 10-20 Hz target, while a small visuomotor policy closes '
                   'the loop on the latest observation at 200 Hz on board. The harvester listed dual-rate hierarchies as a method '
                   'family; this is a deployed instance claiming the loop rate that dynamic manipulation needs. Not the named '
                   'metric (pi0.5 on a Jetson), and the VLM itself is still below 10 Hz, which supports the literal bottleneck.'},
]

CHECKS = [
    {'bottleneck': 'r2-B1',
     'searched': ['WebSearch: lifelong robot learning LIBERO zero forgetting matches multitask upper bound 2026 VLA continual',
                  'arXiv 2605.26820v3 (real-world continual VLA, pi0.5) read in full; arXiv 2603.11653v3 (Simple Recipe, continual RL) '
                  'read in full',
                  'Harvester raw texts re-read: 2603.03818v2 (Tables 1, 5, 6, 7 and Appendix B.1), 2606.03598v2 (Table 1)'],
     'finding': 'NOT OPEN by the table rule, CONTESTED in substance. On real robots, experience replay with a 2% buffer (of all '
                'past data) gives final average BWT +0.25, i.e. no forgetting, and at 20% ER beats joint multi-task training '
                '(97.2 vs 82.6/83.2) on 5-task streams (Zhu et al., Aug 2026). In simulation, LIBERO\'s own protocol (1000 '
                'transitions per task) already gives Pi0 NBT -0.016 averaged over four suites (the harvester\'s source), and '
                'replay-free sequential LoRA + on-policy RL gives NBT within about 1 point of zero and within 0.7-4.6 points of '
                'the multitask oracle, over up to 30 tasks (Hu et al., RLC 2026). What stays open: supervised (imitation) continual '
                'fine-tuning with very small memories on long simulated suites (Pi0 NBT 0.229 at 100 samples per task on '
                'LIBERO-10; SFT in place of RL gives NBT 78.7), heterogeneous real streams (10-task BWT -2.7, with large losses '
                'under uniform replay), and small backbones. Fair summary: closed for large pretrained VLAs with replay at '
                'LIBERO\'s budget or with RL; open for low-memory imitation and weak backbones.',
     'harvester_errors': ['Named metric chosen off-protocol: the harvester named NBT at 100 samples per task (2%), but LIBERO\'s '
                          'official ER budget is 1000 transitions per task (about 15-20%), where the same source reports the '
                          'target reached (Pi0 average NBT -0.016). The harvester disclosed this (r2:7) and flagged the '
                          'bottleneck as likely CONTESTED, so this is a framing choice, not a misquote.',
                          '"20% replay" is the source\'s round figure; its appendix says approximately 15-20% and counts '
                          'transitions (state-action pairs), not demonstrations. Minor.',
                          'r2:8 PHASER: the NBT gaps given (10.0 on OV-7B, 11.1 and 12.4 on 3B) are PHASER\'s, not the best NBT in '
                          'the table: plain ER has NBT -5.6 on OV-7B LIBERO-Long (with only 54.6 success) and iCaRL 6.0 on '
                          'QwenOFT-3B LIBERO-Long. Best-by-success was reported as best-by-forgetting. Minor.']},
    {'bottleneck': 'r2-B2',
     'searched': ['WebSearch: VLA retains full VLM capabilities multimodal benchmarks MMMU MMStar no degradation vision-language-action 2026',
                  'WebSearch: UAM "Dual-Stream Perspective on Forgetting in VLA Training" arXiv',
                  'arXiv 2507.17520v2 (InstructVLA, ICLR 2026), 2605.15735v2 (UAM), 2601.14133v2 (TwinBrainVLA) read; 2606.19297v1 '
                  '(Act2Answer, knowledge retention in VLAs) screened: supports the bottleneck, not used'],
     'finding': 'CONTESTED, not closed. The erosion is now a few points rather than the harvester\'s up-to-11: InstructVLA '
                '(ICLR 2026, co-trained with VLM corpora) is at or above its base Eagle2 on 6 of 13 multimodal benchmarks and within '
                '0.2-3.0 points on the other 7; UAM (May 2026, action-only training with a second visual pathway) keeps over 95% '
                'of its base BAGEL, below it on all six comparable benchmarks by 1.3-4.9 points. A frozen-copy design '
                '(TwinBrainVLA) retains the VLM by construction at twice the VLM cost, a misframing argument that reports no VQA '
                'scores. No source shows a VLA at or above its base on every benchmark; plain VLA training still collapses the VLM '
                '(POPE 88.87% -> 0.04%).',
     'harvester_errors': ['"best" understated: the harvester took VLM2VLA (Sep 2025; below its base on 9 of 12 by up to 11.1) as '
                          'the best retention result. InstructVLA (arXiv v2 Mar 2026, ICLR 2026) and UAM (May 2026) retain more, '
                          'within about 3 and 5 points of their bases. The gap in the BOTTLENECKS entry (2.2-11.1 points) '
                          'overstates the 2026 state.']},
    {'bottleneck': 'r2-B3',
     'searched': ['WebSearch: LIBERO-PRO position perturbation robust VLA achieves high success 2026 state of the art LIBERO-Plus robot initial state',
                  'WebSearch: LIBERO-Plus benchmark new state of the art total success camera robot perturbation 2026 arXiv VLA robustness 85%',
                  'WebSearch: "LIBERO-PRO" "position" perturbation success rate improved 2026 VLA spatial generalization method outperforms pi0.5',
                  'arXiv 2606.27663v1 (3D-point injection), 2609.05588v1 (GE-Act 2.0), 2604.11757v2 (StarVLA-alpha, ECCV 2026: LIBERO-Plus '
                  'robot 64.3, total 79.7; screened), 2608.01826v1 (MVUCF: GR00T-N1.6 LIBERO-Plus total 42.8 -> 65.2; screened), '
                  '2605.11817v2 (ICML 2026, in-domain LIBERO-Plus only; screened), 2512.07472v1 (affordance field; screened); CVPR 2026 '
                  'Li et al. (open access PDF)',
                  'Harvester raw texts re-read: Anchor-Align Tables 1 and 5 (baselines and backbone), LIBERO-Plus Table 1'],
     'finding': 'CONTESTED, not closed. The harvester\'s best numbers came from a paper comparing only small (0.5B) models; larger '
                'VLAs do better. Under LIBERO-PRO position perturbation on LIBERO-Spatial plain pi0.5 scores 58.0 and 69.4 with a '
                '3D grounding module (oracle target points from the simulator), against the harvester\'s 22.6; under LIBERO-Plus '
                'robot-initial-state perturbation pi0.5 scores 73.6 (all suites), against 59.1. Camera change is largely repaired '
                'by one-shot visual adaptation (48.5% -> 87.1%, CVPR 2026) or by a world-action model (94.1%). No source shows '
                'spatial shifts without loss against the unperturbed ~96-98; the gaps are about 20-30 points, not 40-76.',
     'harvester_errors': ['"best: position swap 22.6; robot initial state 59.1" understates the state of the art: both come from '
                          'Anchor-Align, whose Table 1 compares only 0.5B-backbone models and none of pi0.5 or GR00T; pi0.5 alone '
                          'reports 58.0 (position, LIBERO-Spatial; Tsai et al., Jun 2026) and 73.6 (robot, LIBERO-Plus all suites; '
                          'GE-Act 2.0, Sep 2026). The gaps 75.8 and 39.3 are therefore overstated. Protocol identity '
                          '("Pos. Swap" vs "position perturbation", Spatial suite vs all suites) was not verified, so the '
                          'comparison is cross-paper.']},
    {'bottleneck': 'r2-B4',
     'searched': ['WebSearch: zero-shot cross-embodiment transfer new robot without target data success rate matches 2026 VLA "zero-shot" embodiment humanoid',
                  'arXiv 2606.22836v2 (Cloak, CoRL 2026) read in full; 2602.10556v2 (LAP) and 2609.21983v1 (SkelWAM) screened',
                  'Harvester raw text re-read: ZETA Section 5.1, Tables 3 and 4'],
     'finding': 'NOT OPEN by the table rule, CONTESTED in substance. Cloak (Stanford, CoRL 2026) transfers a pi0.5 policy trained '
                'only on Franka + Robotiq data zero-shot to an unseen YAM arm and gripper at 86.3 +/- 3.7 task progress against '
                '88.0 +/- 3.3 on the source (and 70.8 vs 75.0 binary success), i.e. no measurable loss, in the real world; to an '
                'unseen UMI gripper at 85.1. This uses inverse-kinematics retargeting of the known target body and masking of the '
                'end-effector in the wrist view. The five-fingered hand is still 6.2 points below the source, and the harvester\'s '
                'broader statement (joint or continued training across bodies interferes) is not addressed. Fair summary: closed '
                'for arm-and-gripper changes that IK can bridge; open for bodies with a different grasp mechanism and for '
                'multi-embodiment co-training.',
     'harvester_errors': ['"Real world (140 rollouts per model)": 140 is the total over seven embodiments and two tasks; the FULL '
                          'cell (81.9) rests on 10 trials per task-embodiment pair. The quote is right; the precision attached to '
                          'the FULL gap is overstated. Minor.']},
    {'bottleneck': 'r2-B5',
     'searched': ['WebSearch: zero-shot sim-to-real manipulation real-world success matches simulation success 2026 VLA trained purely on synthetic data',
                  'WebSearch: InternData-A1 arXiv synthetic data pre-training generalist policy matches real robot pre-training pi0',
                  'WebSearch: real-to-sim policy evaluation Pearson correlation 0.9 real-world success generalist policies 2025 2026 Gaussian splatting PolaRiS',
                  'arXiv 2511.16651v1 (InternData-A1), 2606.18953v1 (object-centric residual RL), 2512.16881v2 (PolaRiS), 2609.23910v1 '
                  '(ReVeal), 2606.28276v4 (SimFoundry) read; 2609.18293v1 (function-preserving real-to-sim-to-real) screened; '
                  'Sim2Real-VLA (ICLR 2026, OpenReview) seen in search results only, not fetched'],
     'finding': 'CONTESTED on both halves, not closed. Transfer loss: a simulation-trained residual policy loses 10 points (86% sim, '
                '76% real, five real tasks; none on one task), against the harvester\'s 28.0; synthetic data is reported worth real '
                'data at 1:1 on basic tasks and within 8:1 on harder ones (InternData-A1, CVPR 2026), a reframing of the target. '
                'Evaluation predictivity: real-to-sim evaluators now report Pearson r of 0.91 (SimFoundry), 0.95 with sub-task '
                'scoring, 0.960 (ReVeal) and 0.98 against RoboArena (PolaRiS; 0.9 on average, worst 0.81), against the harvester\'s '
                'best 0.84. No source shows zero transfer loss on average or a correlation of 1.0.',
     'harvester_errors': ['"evaluation correlation 0.84 (X2Real)" is not the best reported: PolaRiS (Dec 2025) reports 0.9 on '
                          'average and 0.98 against RoboArena, ReVeal (Sep 2026) 0.960, SimFoundry (Aug 2026) 0.911-0.95. The gap '
                          'to 1.0 is about 0.02-0.09, not 0.16.']},
    {'bottleneck': 'r2-B6',
     'searched': ['WebSearch: Generalist AI GEN-0 270,000 hours real-world manipulation data scaling laws robotics',
                  'Generalist AI blog: GEN-0 (4 Nov 2025), GEN-1 (2 Apr 2026), GEN-1.5 (19 Aug 2026; screened: one-shot learning, '
                  'no corpus size); The Robot Report on GEN-1 (3 Apr 2026; trade press, screened, the primary blog used instead)',
                  'Harvester raw text re-read: Data Pyramid survey (no mention of Generalist\'s corpus)'],
     'finding': 'CONTESTED as framed; the target is not reached. The largest reported interaction corpus is a company claim of over '
                '500,000 hours from wearable devices (Generalist, Apr 2026; 270,000 hours already in Nov 2025), about 57 years, '
                'still a factor of about 1,750 short of the harvester\'s 100,000-year analogy. The same company claims 99% success '
                'on simple tasks with about 1 hour of robot data per task after pretraining without robot data, i.e. that robot '
                'data is not the binding constraint; the harvester\'s own sources make the same point (a TMLR survey: "not merely '
                'data scarcity"; Goldberg\'s article title: engineering can close the gap). The Generalist claims are not '
                'independently evaluated.',
     'harvester_errors': ['"best: >100,000 hours ... (Xiaomi-Robotics-1, 2026)" understates the largest reported corpus: '
                          'Generalist reported 270,000 hours in Nov 2025 and over half a million hours in Apr 2026 (company '
                          'statements). The gap "a factor of about 8,800" is then about 1,750; the harvester\'s survey source did '
                          'not list company corpora.']},
    {'bottleneck': 'r2-B7',
     'searched': ['WebSearch: BEHAVIOR-1K challenge 2026 results success rate q-score 50 household tasks improved',
                  'arXiv export API: all:"BEHAVIOR-1K", newest first (19 entries screened by abstract: StageGuard, Spatial Grafting, '
                  'ForesightFlow, StarVLA, MPVI and others; none reports full success above the 2025 winners)',
                  '2026 BEHAVIOR Challenge page; arXiv 2511.14759v2 (pi*0.6); arXiv 2606.00985v1 (MPVI); Generalist GEN-1 blog'],
     'finding': 'OPEN on the named metric; narrow long-horizon tasks near solved. No 2025-26 source reports BEHAVIOR full success '
                'above 0.124 (test) or 0.15 (post-challenge validation); the 2026 edition (100 tasks) was still open on the day. '
                'Deployed narrow long-horizon tasks reach 90%+ with hours of unattended running (pi*0.6: espresso for 13 hours, '
                'boxes in a factory; Generalist GEN-1: kitting for over an hour), as the harvester conceded. A misframing argument: '
                'a VLA interleaved with a classical planner more than doubles BEHAVIOR task progress with no more data (MPVI), and '
                'the organisers now admit planners and LLM-assisted systems, so "one generalist policy" is a design choice rather '
                'than the benchmark\'s requirement.',
     'harvester_errors': []},
    {'bottleneck': 'r2-B8',
     'searched': ['WebSearch: Figure Helix vision-language-action runs entirely onboard embedded low-power GPUs 200 Hz System 1 7-9 Hz',
                  'WebSearch: pi0 OR pi0.5 VLA Jetson AGX Orin OR Thor real-time inference Hz onboard 2026 arXiv latency ms achieves 10 Hz 20 Hz',
                  'NVIDIA Jetson AI Lab tutorial (OpenPi pi0.5 on Thor); NVIDIA developer forum post 368788 (Discourse JSON); arXiv '
                  '2606.07383v4 (RhinoVLA), 2608.03682v3 (PhyAI); Figure AI Helix page; Intel Open Edge Platform article on pi0.5 '
                  '(screened: performance per watt vs Orin, no absolute rate used)',
                  'Harvester raw text re-read: Jetson-PI Table 4 (all rows)'],
     'finding': 'NOT OPEN by the table rule on Jetson Thor; OPEN on Jetson Orin. NVIDIA\'s own tutorial runs pi0.5 on Jetson AGX '
                'Thor in about 49 ms (FP8 + NVFP4) or 54 ms (FP8), i.e. 18-20 Hz, inside the 10-20 Hz target, against the '
                'harvester\'s best on Thor of 7.59 Hz; an independent developer reports 44 ms and a paper measures a pi0 runtime at '
                '49.5 ms on Thor. These are latency benchmarks, not closed-loop success evaluations. On Orin no source reaches 10 '
                'Hz for pi0.5 (a 2026 company report says Orin "has limited compute headroom for 10 Hz VLA inference"); a '
                'pi0.5-scale model on a Chinese edge SoC reaches 11.69 Hz. Misframing: a deployed dual-system VLA (Figure Helix, '
                'Feb 2025) runs its VLM on board at 7-9 Hz and closes the control loop at 200 Hz with a small policy.',
     'harvester_errors': ['"best: 7.59 Hz on Jetson Thor (Jetson-PI)" understates the best reported rate for pi0.5 on Thor: a '
                          'TensorRT FP8/NVFP4 build reaches about 49 ms per inference (NVIDIA Jetson AI Lab, 2026), i.e. about 20 '
                          'Hz. Jetson-PI\'s own naive Thor latency (457.9 ms) is also far above NVIDIA\'s PyTorch BF16 figure '
                          '(~132 ms); the two setups differ (not investigated).']},
]
