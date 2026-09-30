"""ROB1 stage 1, family R4 (Robotics/DECLARATION.md): safety, trust and security. Emergency stop and safe interruption of
learned and dynamically balancing robots, human-robot collaboration and humanoid safety standards (ISO 10218:2025, ISO/TS
15066, ISO 13482, ISO 25785-1 in development), verification and runtime monitoring of learned policies, jailbreak and
adversarial attacks on robot policies, the privacy of robots' sensor data and the cybersecurity of robots and fleets.

Every source was fetched on 2026-09-30 through the session proxy (curl, TLS verification on). Quotes are copied from the
text extracted from the fetched file: PDFs by pymupdf 1.28.2 (`page.get_text()`, pages joined by newlines); HTML pages by
BeautifulSoup 4 (`get_text('\n')` after removing script/style/noscript/svg, runs of spaces and blank lines collapsed). Raw
files live outside the repository under /tmp/claude-0/rob_src/ (`raw_file` is relative to that root; the fetched originals
are in r4/src/); their sha256 is in /tmp/claude-0/rob_src/r4/SHA256SUMS.txt and in the dossier
docs/citations/rob1_r4_2026-09-30.md. Table rows are quoted as the extractor emitted them, cell by cell in reading order.
To be checked by Robotics/checks/verify.py; at harvest time a scratch copy of Open_Bottlenecks/checks/verify.py pointed at
this file and this root was run (result in the dossier and in /tmp/claude-0/rob_src/r4/verify_r4_scratch.txt).

The standards bodies' own pages (iso.org for ISO 25785-1, ISO 10218-1/-2, ISO/TS 15066, ISO/FDIS 13482) answered HTTP 403
(a Cloudflare challenge) and EUR-Lex answered HTTP 202 with an empty body; what is public about those documents is quoted
from the free sample pages of ISO 10218-1:2025 and ISO 10218-2:2025 distributed by iTeh Standards (foreword, introduction,
scope), from the IEEE Humanoid Study Group report, and from the European Commission's own CRA pages. Nothing is quoted from
an unreached page.

Roles (DECLARATION.md stage 1): a = the problem stated; b = a 2025-26 statement that it is open, unsolved or a main challenge;
c = the best reported result on a named benchmark or metric against the target (numbers quoted; the gap is computed in
`agent_note` and in BOTTLENECKS); d = the method families tried and the assumption each makes (about time, clocks,
boundaries, interruptions, memory or tuning). `agent_note` is the agent's reading, not the source's words. Numbers from
different sources are not comparable unless a note says the protocol is shared.
"""

R = 'r4/txt/'

CLAIMS = [
    # ---------------- r4-B1: jailbreaks of LLM/VLM-planned robots (harmful physical actions from adversarial instructions)
    {'id': 'r4:1', 'bottleneck': 'r4-B1', 'role': 'a',
     'source': 'Robey, Ravichandran, Kumar, Hassani & Pappas, Jailbreaking LLM-Controlled Robots (RoboPAIR)',
     'version': 'arXiv v2, 9 Nov 2024 (v1 17 Oct 2024)', 'url': 'https://arxiv.org/abs/2410.13691v2',
     'quote': ['we demonstrate that ROBOPAIR, as well as several static baselines, finds jailbreaks quickly and effectively, '
               'often achieving 100% attack success rates.',
               'Indeed, our results on the Unitree Go2 represent the first successful jailbreak of a deployed commercial robotic '
               'system.'],
     'raw_file': R + '2410.13691v2.txt',
     'agent_note': 'The problem stated (2024): an LLM planner that can be talked into a harmful plan turns a text jailbreak into '
                   'a physical action. Used for B-a only.'},
    {'id': 'r4:2', 'bottleneck': 'r4-B1', 'role': 'b',
     'source': 'Yeke, Zhou, Lin, Cai, Bianchi & Celik, RoboJailBench: Benchmarking Adversarial Attacks and Defenses in Embodied '
               'Robotic Agents',
     'version': 'arXiv v1, 19 May 2026', 'url': 'https://arxiv.org/abs/2605.19328v1',
     'quote': ['Their evaluations, however, rely on ad-hoc datasets, limited metrics, and emphasize attack success while '
               'neglecting the trade-off between security and the ability to follow benign commands.',
               'Their performance is within the margin of error of each other, and neither provides consistent, definitive '
               'robustness over the other in individual datasets.'],
     'raw_file': R + '2605.19328v1.txt',
     'agent_note': '2026 statement: defences were evaluated on their authors\' own data; on a shared benchmark neither of the two '
                   'integrated defences (a Google defence prompt, RoboGuard) is consistently robust.'},
    {'id': 'r4:3', 'bottleneck': 'r4-B1', 'role': 'b',
     'source': 'Huang, Liu, Luo, Wu & Cai, Propagating Unsafe Actions in LLM Controlled Multi-Robot Collaboration via Single '
               'Robot Compromise (IJCAI 2026)',
     'version': 'arXiv v2, 18 May 2026 (v1 15 May 2026)', 'url': 'https://arxiv.org/abs/2605.15641v2',
     'quote': ['reveals a persistent safety alignment gap in multi-robot planners.',
               'obedience reaches 1.00 in the strongest cases, and infectiousness rises to 0.90.'],
     'raw_file': R + '2605.15641v2.txt',
     'agent_note': '2026: the attack surface grows with fleets; one compromised robot propagates the unsafe intent to its peers.'},
    {'id': 'r4:4', 'bottleneck': 'r4-B1', 'role': 'c',
     'source': 'Ravichandran, Robey, Kumar, Pappas & Hassani, Safety Guardrails for LLM-Enabled Robots (RoboGuard; IEEE RA-L, '
               'accepted Feb 2026) (Table I)',
     'version': 'arXiv v2, 3 Mar 2026 (v1 10 Mar 2025)', 'url': 'https://arxiv.org/abs/2503.07885v2',
     'quote': ['None, safe task (↑) Direct prompt 100.0 ± 0% 100.0 ± 0%',
               'Non-adaptive (↓) RoboPAIR 92.3 ± 4.7% 2.3 ± 1.5%',
               'Adaptive white-box (↓) RoboPAIR - 5.2 ± 0.7%',
               'This demonstrates that while the guarded system maintains significant robustness against attacks, it may still '
               'be susceptible to a strong adaptive attacker.',
               'As reported in Table IV-D, ROBOGUARD prevents 100% of the adversarial attacks, without compromising on utility.'],
     'raw_file': R + '2503.07885v2.txt',
     'agent_note': 'The authors\' own benchmark (70 adversarial prompts over 7 harmful behaviours, 210 evaluations per attack; '
                   'columns w/o RG, w/ RG). With the guardrail: attack success 2.3% (non-adaptive RoboPAIR) up to 5.2% '
                   '(white-box adaptive RoboPAIR), utility on safe tasks 100%. Against the target of 0% attack success at 100% '
                   'utility (r4:5): 2.3-5.2 points, i.e. about 1 in 43 to 1 in 19 adversarial requests still executed. The '
                   'small real-world set reached 0%. Same paper, same protocol.'},
    {'id': 'r4:5', 'bottleneck': 'r4-B1', 'role': 'c',
     'source': 'Yeke et al., RoboJailBench (Table 4 and Section 3)', 'version': 'arXiv v1, 19 May 2026',
     'url': 'https://arxiv.org/abs/2605.19328v1',
     'quote': ['In a perfect safety-aligned embodied AI model, the benign goal in each matched pair should be successfully '
               'executed, whereas the adversarial goal should be rejected, maximizing both utility and security.',
               'RJB-Instructions No Defense 94.44±2.41 6.67±2.63 7.78±2.82 81.11±4.13 52.50±2.63 93.33±2.63 67.20±2.26',
               'RoboGuard 94.44±2.41 6.67±2.63 7.78±2.82 31.11±4.88 65.00±2.51 100.00±0.00 78.79±1.85',
               'CD attains a 74.07% success rate overall and is 25.53% more effective than the second-best method, ROBOPAIR.'],
     'raw_file': R + '2605.19328v1.txt',
     'agent_note': 'Independent benchmark, columns ASR for CD (BadRobot conceptual deception), CJ, SM, RoboPAIR, then SR '
                   '(security rate), UR (utility rate), SU-HM. On RJB-Instructions RoboGuard cuts RoboPAIR from 81.11% to '
                   '31.11% but leaves conceptual deception at 94.44%; security rate 65.00 against the stated target of '
                   'rejecting every adversarial goal (SR 100) at full utility (UR 100): a gap of 35.0 points. The 2.3-5.2% of '
                   'r4:4 is on the authors\' own data with RoboPAIR; the two are different protocols.'},
    {'id': 'r4:6', 'bottleneck': 'r4-B1', 'role': 'c',
     'source': 'Marchiori, Sinha, Agia, Robey, Pappas, Conti & Pavone, Preventing Robotic Jailbreaking via Multimodal Domain '
               'Adaptation (J-DAPT)',
     'version': 'arXiv v1, 27 Sep 2025', 'url': 'https://arxiv.org/abs/2509.23281v1',
     'quote': ['Evaluations across autonomous driving, maritime robotics, and quadruped navigation show that J-DAPT boosts '
               'detection accuracy to nearly 100% with minimal overhead.'],
     'raw_file': R + '2509.23281v1.txt',
     'agent_note': 'Contrary evidence to record: a jailbreak detector near 100% on its authors\' three domain datasets. It is a '
                   'detector (classification accuracy), not an attack success rate under adaptive attack; the paper\'s own '
                   'd-claim (r4:8) says such classifiers struggle where domain data are scarce.'},
    {'id': 'r4:7', 'bottleneck': 'r4-B1', 'role': 'c',
     'source': 'Chepuri & Srivastava, AuthGuard-R: Safety-Compliant Mission Hijacking and Dual-Gate Defense for LLM-Controlled '
               'Robots',
     'version': 'arXiv v1, 25 Sep 2026', 'url': 'https://arxiv.org/abs/2609.31110v1',
     'quote': ['Across 240 live attack trials, the planners followed an injected mission deviation in 109 trials; AuthGuard-R '
               'rejected all 109 resulting unauthorized actions.',
               'These results are preliminary and do not replace the larger simulator, ROS 2, and full-baseline evaluation '
               'described in the methodology.'],
     'raw_file': R + '2609.31110v1.txt',
     'agent_note': 'Contrary evidence to record: a deterministic authorisation gate blocked 109 of 109 unauthorised actions '
                   '(mission hijacking, a narrower threat than harmful-action jailbreaks); the authors call it preliminary.'},
    {'id': 'r4:8', 'bottleneck': 'r4-B1', 'role': 'd',
     'source': 'Marchiori et al., J-DAPT (Abstract)',
     'version': 'arXiv v1, 27 Sep 2025', 'url': 'https://arxiv.org/abs/2509.23281v1',
     'quote': ['Data-driven defenses such as jailbreak classifiers show promise, yet they struggle to generalize in domains where '
               'specialized datasets are scarce, limiting their effectiveness in robotics and other safety-critical contexts.'],
     'raw_file': R + '2509.23281v1.txt',
     'agent_note': 'Classifier family: assumes the attack distribution seen in training data (a fixed dataset, no drift).'},
    {'id': 'r4:9', 'bottleneck': 'r4-B1', 'role': 'd',
     'source': 'Ravichandran et al., RoboGuard', 'version': 'arXiv v2, 3 Mar 2026', 'url': 'https://arxiv.org/abs/2503.07885v2',
     'quote': ['ROBOGUARD first contextualizes predefined safety rules by grounding them in the robot’s environment using a '
               'root-of-trust LLM.',
               'ROBOGUARD then resolves conflicts between these contextual safety specifications and potentially unsafe plans '
               'using temporal logic control synthesis, ensuring compliance while minimally violating user preferences.'],
     'raw_file': R + '2503.07885v2.txt',
     'agent_note': 'Specification-guardrail family: safety rules written in advance, grounded once per plan in a world model '
                   '(a snapshot), then enforced by temporal-logic synthesis; assumes the rule set and the root-of-trust LLM are '
                   'correct and shielded.'},
    {'id': 'r4:10', 'bottleneck': 'r4-B1', 'role': 'd',
     'source': 'Chepuri & Srivastava, AuthGuard-R', 'version': 'arXiv v1, 25 Sep 2026', 'url': 'https://arxiv.org/abs/2609.31110v1',
     'quote': ['AuthGuard-R, a deterministic authorization layer that binds every executable action to a signed mission, robot '
               'identity, object and region scope, current state, time, and input provenance.'],
     'raw_file': R + '2609.31110v1.txt',
     'agent_note': 'Authorisation family: the mission and its time window are fixed and signed in advance; any deviation is '
                   'blocked (boundaries given from outside, on a clock).'},
    {'id': 'r4:11', 'bottleneck': 'r4-B1', 'role': 'd',
     'source': 'Yeke et al., RoboJailBench (Limitations)', 'version': 'arXiv v1, 19 May 2026',
     'url': 'https://arxiv.org/abs/2605.19328v1',
     'quote': ['Static visual context: Our current framework evaluates each scenario using two modalities: a user instruction '
               'and a single observed scene image. In practice, a deployed robotic system may receive a continuous stream of '
               'visual observations.'],
     'raw_file': R + '2605.19328v1.txt',
     'agent_note': 'Evaluation assumption: one instruction and one frame per episode; temporally extended attacks over a '
                   'stream are not measured.'},

    # ---------------- r4-B2: physical adversarial attacks on VLA policies, and certified defence
    {'id': 'r4:12', 'bottleneck': 'r4-B2', 'role': 'a',
     'source': 'Wang, Han, Liang, Yang, Liu, Zhang, Wang, Luo & Tang, Exploring the Adversarial Vulnerabilities of '
               'Vision-Language-Action Models in Robotics (ICCV 2025)',
     'version': 'arXiv v4, 1 Aug 2025 (v1 18 Nov 2024; ICCV camera ready)', 'url': 'https://arxiv.org/abs/2411.13587v4',
     'quote': ['Our evaluation reveals a marked degradation in task success rates, with up to a 100% reduction across a suite '
               'of simulated robotic tasks, highlighting critical security gaps in current VLA architectures.'],
     'raw_file': R + '2411.13587v4.txt', 'agent_note': 'The problem stated: a small patch in the camera view can stop a VLA.'},
    {'id': 'r4:13', 'bottleneck': 'r4-B2', 'role': 'b',
     'source': 'Li, Yin, Huang, Liu, Zou, Yu, Ye, Yu & Wang, Vision-Language-Action Safety: Threats, Challenges, Evaluations, '
               'and Mechanisms (survey)',
     'version': 'arXiv v2, 25 Aug 2026 (v1 26 Apr 2026)', 'url': 'https://arxiv.org/abs/2604.23775v2',
     'quote': ['Despite substantial progress, the field remains at an early stage: most known attacks have no principled '
               'countermeasures, most defenses lack formal guarantees, and most evaluations are confined to simulation.',
               'While certified robustness methods have been applied to image classifiers and language models, their '
               'adaptation to VLA models remains an open challenge due to the sequential and multi-modal nature of robotic '
               'decision-making.'],
     'raw_file': R + '2604.23775v2.txt', 'agent_note': '2026 survey statement that attacks outrun defences on VLAs.'},
    {'id': 'r4:14', 'bottleneck': 'r4-B2', 'role': 'b',
     'source': 'Wang, Han, Hao, Yang, Zhao & Tang, Partially Observable Adversarial Patch Attacks on Vision-Language-Action '
               'Models in Robotics (IEEE RA-L 2026)',
     'version': 'arXiv v1, 2 Jun 2026 (accepted May 2026)', 'url': 'https://arxiv.org/abs/2606.03556v1',
     'quote': ['yet their robustness to adversarial attacks remains largely unexplored.',
               'the printed patch reduces success rates from 72% to 12% on Task A and from 58% to 8% on Task B',
               'the average ASR stays close to the undefended case (79.2/80.2 vs. 81.0), so these simple defenses alone cannot '
               'suppress the attack.'],
     'raw_file': R + '2606.03556v1.txt',
     'agent_note': '2026: an 18 cm printed patch on a real arm (OpenVLA-7B, 50 trials per condition) cuts success 72% -> 12% and '
                   '58% -> 8%; JPEG and blur preprocessing leave the attack success at 79.2-80.2% against 81.0% undefended.'},
    {'id': 'r4:15', 'bottleneck': 'r4-B2', 'role': 'c',
     'source': 'Lu, Peng, Lin, Yang, He, Ye, Yu, Zhu, Shen, Kot & Jiang, CertVLA: Certified Defense against Physical Visual '
               'Attacks for Vision-Language-Action Models (Table 2 and text)',
     'version': 'arXiv v1, 21 Aug 2026', 'url': 'https://arxiv.org/abs/2608.20791v1',
     'quote': ['Model Clean Attack Defense Certified π0.5 90 40 60 30 Table 2: Results for physical patch attacks on the real '
               'robot.',
               'Tab. 2 shows that the patch reduces π0.5 success from 90% to 40%. CertVLA reaches 60%, a 20-point gain that '
               'recovers 40% of the attack-induced loss. Its 30% Certified success means that half of the successfully '
               'defended trials pass at every query.',
               'with the task repeated for 10 independent trials.'],
     'raw_file': R + '2608.20791v1.txt',
     'agent_note': 'The best defence found, on a real dual-arm Piper robot (10 trials): clean 90%, attacked 40%, defended 60%, '
                   'certified 30%. Against the attack-free success of 90% (the oracle for a defence): 30 points short defended, '
                   '60 points short certified. In simulation (LIBERO, Table 1) the best certified average is 94.00 (OpenVLA-OFT, '
                   'patch attack), so the gap is mainly physical.'},
    {'id': 'r4:16', 'bottleneck': 'r4-B2', 'role': 'd',
     'source': 'Lu et al., CertVLA', 'version': 'arXiv v1, 21 Aug 2026', 'url': 'https://arxiv.org/abs/2608.20791v1',
     'quote': ['Existing empirical defenses improve VLA robustness through robust training, decoupled robustness learning, '
               'safety-constrained optimization, and noise-filtering modules',
               'For safety-critical deployment, however, empirical robustness alone is insufficient, as resistance to tested '
               'attacks does not establish robustness to all attacks within the threat model',
               'Conjoining query-level decisions extends the action certificate to the complete closed-loop rollout.',
               'We set β = 0.95, α = 0.5, and ϵ = 10−8 for all main results.'],
     'raw_file': R + '2608.20791v1.txt',
     'agent_note': 'Empirical family (robust training, filtering): no guarantee beyond the attacks tried. Certified family: a '
                   'bounded-support threat model, a certificate per policy query chained over the rollout (the query clock), '
                   'and calibration constants (beta, alpha) fixed on held-out clean episodes.'},
    {'id': 'r4:17', 'bottleneck': 'r4-B2', 'role': 'd',
     'source': 'Wang et al., Partially Observable Adversarial Patch Attacks (RA-L 2026)', 'version': 'arXiv v1, 2 Jun 2026',
     'url': 'https://arxiv.org/abs/2606.03556v1',
     'quote': ['Existing work shows that adversarial patches can mislead VLA-based robots but assumes full access to the entire '
               'execution trajectory, an unrealistic requirement in practice.',
               'where the adversary can exploit only a short prefix of the trajectory to generate a fixed patch applied to all '
               'subsequent frames.'],
     'raw_file': R + '2606.03556v1.txt',
     'agent_note': 'Threat-model assumption about time: earlier attacks assumed the whole trajectory; the 2026 attack uses a '
                   'prefix of K frames and a patch fixed thereafter.'},

    # ---------------- r4-B3: runtime failure detection for generalist learned policies (unseen tasks)
    {'id': 'r4:18', 'bottleneck': 'r4-B3', 'role': 'a',
     'source': 'Gu, Ju, Sun, Gilitschenski, Nishimura, Itkina & Shkurti, SAFE: Multitask Failure Detection for '
               'Vision-Language-Action Models (NeurIPS 2025)',
     'version': 'arXiv v2, 30 Oct 2025 (v1 11 Jun 2025; NeurIPS 2025 camera ready)', 'url': 'https://arxiv.org/abs/2506.09937v2',
     'quote': ['To allow these policies to safely interact with their environments, we need a failure detector that gives a '
               'timely alert such that the robot can stop, backtrack, or ask for help. However, existing failure detectors are '
               'trained and tested only on one or a few specific tasks, while generalist VLAs require the detector to '
               'generalize and detect failures also in unseen tasks and novel environments.'],
     'raw_file': R + '2506.09937v2.txt', 'agent_note': 'The problem stated: a timely alert, on tasks the detector never saw.'},
    {'id': 'r4:19', 'bottleneck': 'r4-B3', 'role': 'b',
     'source': 'Navasardyan, Danielyan & Davtyan, FailBench: How Reliable are VLMs at Judging Robot Task Success?',
     'version': 'arXiv v1, 3 Sep 2026', 'url': 'https://arxiv.org/abs/2609.03611v1',
     'quote': ['Evaluating 13 VLM-based detectors, we find that the best model achieves only 0.77 mean balanced accuracy, '
               'indicating substantial room for improvement.',
               'detection approaches saturation when success is determined by observable object motion, but approaches chance '
               'when success depends on establishing contact, with no model exceeding 0.60 balanced accuracy on '
               'contact-intensive assembly tasks.',
               'using the original outcome labels provided by their respective sources.'],
     'raw_file': R + '2609.03611v1.txt',
     'agent_note': '2026: 2,197 attempts from 14 sources. Best mean balanced accuracy 0.77 against the ground-truth outcome '
                   'labels (a perfect detector scores 1.0 by definition): gap 0.23; at most 0.60 on contact-rich assembly '
                   '(gap >= 0.40). These are after-the-fact judges, not runtime monitors; used as B-b and supporting B-c.'},
    {'id': 'r4:20', 'bottleneck': 'r4-B3', 'role': 'b',
     'source': 'Park, Li, Oh, Yeh, Kira, Hagenow & Li, Hide-and-Seek in Trajectories: Discovering Failure Signals for VLA '
               'Runtime Monitoring',
     'version': 'arXiv v2, 25 Sep 2026 (v1 29 May 2026; comment: NeurIPS 2026)', 'url': 'https://arxiv.org/abs/2605.30834v2',
     'quote': ['Existing failure detection methods fall short along two axes that jointly define the challenge.',
               'approaches based on action resampling [16, 17, 18] or external VLM judges [19, 20, 21] incur substantial '
               'inference overhead that precludes real-time deployment.'],
     'raw_file': R + '2605.30834v2.txt', 'agent_note': '2026 statement of the open problem (supervision cost, real-time cost).'},
    {'id': 'r4:21', 'bottleneck': 'r4-B3', 'role': 'b',
     'source': 'Li et al., Vision-Language-Action Safety (survey, Section 5.2.2)', 'version': 'arXiv v2, 25 Aug 2026',
     'url': 'https://arxiv.org/abs/2604.23775v2',
     'quote': ['However, this shift exacerbates the inherent safety-latency trade-off: the computational time required for '
               'diagnosis may induce the physical collisions it intends to prevent.'],
     'raw_file': R + '2604.23775v2.txt', 'agent_note': '2026: the monitor\'s own latency is part of the problem.'},
    {'id': 'r4:22', 'bottleneck': 'r4-B3', 'role': 'c',
     'source': 'Park et al., Hide-and-Seek (Table 1, LIBERO-10, OpenVLA)', 'version': 'arXiv v2, 25 Sep 2026',
     'url': 'https://arxiv.org/abs/2605.30834v2',
     'quote': ['Policy: OpenVLA (Success Rate: 51.0%) Seen Tasks Unseen Tasks Method bACC↑ wACC↑ TWA↑ bACC↑ wACC↑ TWA↑',
               'SAFE-MLP NeurIPS’25 0.823±0.036 0.819±0.034 0.630±0.056 0.775±0.062 0.741±0.082 0.590±0.039 Ours 0.852±0.051 '
               '0.853±0.052 0.660±0.035 0.834±0.036 0.828±0.034 0.663±0.010'],
     'raw_file': R + '2605.30834v2.txt',
     'agent_note': 'Best runtime monitor on unseen tasks (OpenVLA on LIBERO-10): balanced accuracy 0.834, time-weighted accuracy '
                   '0.663 (SAFE-MLP 0.775 / 0.590). Against a perfect detector (bACC 1.0, the ground-truth label; see r4:19 for '
                   'the label-as-oracle convention): gap 0.166 in bACC and 0.337 in TWA, which also penalises late alarms.'},
    {'id': 'r4:23', 'bottleneck': 'r4-B3', 'role': 'd',
     'source': 'Gu et al., SAFE (Appendix, LIBERO protocol)', 'version': 'arXiv v2, 30 Oct 2025',
     'url': 'https://arxiv.org/abs/2506.09937v2',
     'quote': ['Note that the LIBERO simulator stops the rollout execution when the robot finishes the task (considered a '
               'success) or a maximum rollout length is reached (considered a failure).',
               'if a failure detector simply learns to count the time elapsed, i.e., st = t, it will achieve perfect failure '
               'detection since failed rollouts have a fixed and longer duration',
               'In this work, we use conformal prediction [58] to calibrate the threshold δt.'],
     'raw_file': R + '2506.09937v2.txt',
     'agent_note': 'Clock assumption in the benchmark: failure is defined by a clock (a time-out at the maximum rollout length), '
                   'so elapsed time alone would detect it; the authors truncate at the minimum length to remove the shortcut. '
                   'Threshold family: a per-timestep threshold calibrated by conformal prediction on the step clock.'},
    {'id': 'r4:24', 'bottleneck': 'r4-B3', 'role': 'd',
     'source': 'Park et al., Hide-and-Seek', 'version': 'arXiv v2, 25 Sep 2026', 'url': 'https://arxiv.org/abs/2605.30834v2',
     'quote': ['SAFE-MLP partially mitigates this with a linearly increasing temporal weight, but this fixed heuristic is '
               'agnostic to when failure actually manifests.',
               'A key challenge in deployment is selecting ζt appropriately: a fixed threshold fails to account for the natural '
               'temporal evolution of failure scores',
               'Under the exchangeability assumption and a user-specified significance level α ∈(0, 1), the band guarantees '
               'that for any new successful rollout, the trajectory-level false alarm rate is bounded by α.'],
     'raw_file': R + '2605.30834v2.txt',
     'agent_note': 'Assumptions on time: label weights that grow linearly with the step index (SAFE-MLP); a time-varying '
                   'conformal band indexed by the step clock, valid under exchangeability of successful rollouts.'},

    {'id': 'r4:67', 'bottleneck': 'r4-B3', 'role': 'c',
     'source': 'Zhu, Liu & Liu, VLA-Scope: Shift-Aware Failure Prediction for Vision-Language-Action Models',
     'version': 'arXiv v1, 18 Sep 2026', 'url': 'https://arxiv.org/abs/2609.21246v1',
     'quote': ['Evaluated independently of the OOD gate on all 1,400 OOD rollouts, the failure predictor achieves a ROC-AUC of '
               '0.8497 after 60 executed actions, compared with 0.7906 without execution progress features.'],
     'raw_file': R + '2609.21246v1.txt',
     'agent_note': 'Supporting (other protocol: OpenVLA, LIBERO-Spatial, OOD rollouts, ROC-AUC): 0.8497 after 60 actions against '
                   '1.0 for a perfect predictor (gap 0.150). Risk is read at a fixed count of executed actions.'},

    # ---------------- r4-B4: emergency stop of dynamically balancing (legged, humanoid) robots; the standards gap
    {'id': 'r4:25', 'bottleneck': 'r4-B4', 'role': 'a',
     'source': 'Ding, Cui, Wang & Wen (Siemens), Toward Certified Functional Safety for Industrial Humanoid Robots: The '
               'Fail-Passive Gap and a Feasibility Study',
     'version': 'arXiv v1, 3 Aug 2026', 'url': 'https://arxiv.org/abs/2608.02809v1',
     'quote': ['The root difficulty is that the safe state of a legged robot is an actively-controlled state, which violates '
               'the fail-passive assumption underlying ISO 13849-1 / EN 60204-1: removing power from a walking biped causes an '
               'uncontrolled fall, so classical de-energization is itself a hazard.'],
     'raw_file': R + '2608.02809v1.txt', 'agent_note': 'The problem stated.'},
    {'id': 'r4:26', 'bottleneck': 'r4-B4', 'role': 'a',
     'source': 'Sun, Pan, Li, Ding, Cui, Wang & Liu, Learning Safe-Stoppability Monitors for Humanoid Robots (PRISM)',
     'version': 'arXiv v1, 24 Mar 2026', 'url': 'https://arxiv.org/abs/2603.22703v1',
     'quote': ['Emergency stops for humanoids cannot simply cut power; instead, a predefined fallback controller is triggered to '
               'drive the robot toward a minimum-risk condition (MRC).'],
     'raw_file': R + '2603.22703v1.txt', 'agent_note': 'The problem stated for the learned-control case.'},
    {'id': 'r4:27', 'bottleneck': 'r4-B4', 'role': 'b',
     'source': 'IEEE Humanoid Study Group (Prather, Keller et al., 16 authors), A Pathway Study for Future Humanoid Standards '
               '(technical report)',
     'version': 'September 2025 (PDF created 23 Sep 2025; DOI 10.13140/RG.2.2.27892.21122), copy hosted by The Robot Report',
     'url': 'https://www.therobotreport.com/wp-content/uploads/2025/09/IEEE-Humanoid-Report-of-Future-Standards-Development.pdf',
     'quote': ['However, no current standards account for robots that have unstable states as part of regular functioning.',
               'Current standards do not adequately address stability requirements, and so a dedicated series of standards is '
               'now recognized as a market need.',
               'current SIL and PL measures assume deterministic systems, whereas humanoids require predictive, probabilistic '
               'risk modeling.',
               'Currently, it is part of the mission for the newly created working group in the ISO Technical Committee 299 '
               'tasked to develop a safety standard (ISO/AWI 25785-1) for industrial mobile robots with actively controlled '
               'stability, notably including humanoids.'],
     'raw_file': R + 'IEEE-Humanoid-Report-of-Future-Standards-Development.txt',
     'agent_note': '2025: no standard covers actively balancing robots; ISO 25785-1 was at the approved-work-item stage (AWI) '
                   'when the report was written. The iso.org page for ISO 25785-1 (standard 91469) answered HTTP 403, so its '
                   'current stage was not verified (a search-result title read "ISO/CD 25785-1", not relied on).'},
    {'id': 'r4:28', 'bottleneck': 'r4-B4', 'role': 'b',
     'source': 'Ding et al. (Siemens), The Fail-Passive Gap (Conclusion; Limitations)', 'version': 'arXiv v1, 3 Aug 2026',
     'url': 'https://arxiv.org/abs/2608.02809v1',
     'quote': ['This fail-passive gap is why industrial humanoid deployment cannot yet reach end-to-end certification',
               'motion-policy interruption and transition to a balanced standstill are not certified, no PFHD/DC/CCF is '
               'established, and no humanoid-specific standard governs them.'],
     'raw_file': R + '2608.02809v1.txt', 'agent_note': '2026 statement that the gap is open.'},
    {'id': 'r4:29', 'bottleneck': 'r4-B4', 'role': 'c',
     'source': 'Ding et al. (Siemens), The Fail-Passive Gap (Tables II and III, Results)', 'version': 'arXiv v1, 3 Aug 2026',
     'url': 'https://arxiv.org/abs/2608.02809v1',
     'quote': ['Reaction (2 contactors, Cat. 0) 1.45×10−9 e 7.30×10−9 3 Total 7.35×10−9 e 1.24×10−8 3',
               'crucially, the reference closes its overall figure only because its Reaction subsystem is monitored contactors '
               '(≈ 1.45 × 10−9), so with no such element the humanoid chain has no end-to-end PFHD yet.',
               'tstop [M] synchronized video 0.3–1.0 s',
               'Summing the worst-case terms gives twc response ≈1.1 s (dominated by tstop)',
               'drove the robot to a stable balanced standstill (no topple) in 0.5–1.3 s in every trial'],
     'raw_file': R + '2608.02809v1.txt',
     'agent_note': 'Target: the certified reference emergency stop (Siemens fail-safe S7-1500 chain, contactor power removal, Stop '
                   'Category 0) reaches PL e / SIL 3 with total PFHD 7.35e-9 (ISO 13849-1) and 1.24e-8 (IEC 62061). Best '
                   'humanoid result: the external chain can be rated, but the robot-side reaction (the balancing policy '
                   'bringing a Unitree G1 to a balanced standstill) has no PFHD and no PL at all; measured stop 0.3-1.0 s, '
                   'worst-case response about 1.1 s; the communication-loss standstill held in 12 of 12 trials (four '
                   'methods x three) in 0.5-1.3 s. The gap is categorical (no rating against PL e), not a number.'},
    {'id': 'r4:30', 'bottleneck': 'r4-B4', 'role': 'c',
     'source': 'Sun et al., PRISM (Table IV and Discussion)', 'version': 'arXiv v1, 24 Mar 2026',
     'url': 'https://arxiv.org/abs/2603.22703v1',
     'quote': ['0.47 62.05 99.38 0.53 93.58 94.05',
               'the monitor consistently elevates the prediction accuracy of critical Unsafe states above 99% (e.g., see α = '
               '0.47 in table IV).',
               'an automated hazard detection and intervention reliability exceeding 99% fundamentally satisfies the '
               'stringent risk-reduction requirements of SIL 2.'],
     'raw_file': R + '2603.22703v1.txt',
     'agent_note': 'A learned safe-stoppability monitor (simulation, Table IV; columns alpha, Safe, Unsafe accuracy): at alpha '
                   '0.47 it flags 99.38% of unsafe states but calls only 62.05% of safe states safe. The SIL 2 claim is the '
                   'authors\'; their co-authors\' Siemens paper (r4:32) states that a data-driven monitor "does not by itself '
                   'furnish a certifiable PFHD/DC argument", and a per-state accuracy is not a per-hour failure rate. '
                   'Recorded as the best learned result, with that caveat.'},
    {'id': 'r4:31', 'bottleneck': 'r4-B4', 'role': 'd',
     'source': 'Sun et al., PRISM (Introduction; problem setup)', 'version': 'arXiv v1, 24 Mar 2026',
     'url': 'https://arxiv.org/abs/2603.22703v1',
     'quote': ['E-stop triggers are asynchronous and unpredictable. An emergency stop may be triggered at any time due to human '
               'intrusion, system-level anomalies, communication failures, or direct operator intervention.',
               'It is assumed that both the nominal policy and the fallback policy are well trained with high success rates if '
               'we do not account for complex environmental interaction.'],
     'raw_file': R + '2603.22703v1.txt',
     'agent_note': 'Interruption assumption: the stop can arrive at any instant, so the robot must stay inside the '
                   'safe-stoppable envelope at every state; one fixed fallback policy, trained in advance; labels from '
                   'fallback rollouts of a fixed maximum horizon in a digital twin.'},
    {'id': 'r4:32', 'bottleneck': 'r4-B4', 'role': 'd',
     'source': 'Ding et al. (Siemens), The Fail-Passive Gap (Section VIII-A)', 'version': 'arXiv v1, 3 Aug 2026',
     'url': 'https://arxiv.org/abs/2608.02809v1',
     'quote': ['Mid-step (single-support) demands. The outcome depends on gait phase.',
               'This imposes a phase-dependent lower bound on tstop, so the ISO 13855 distance must be sized using the '
               'worst-case (single-support) tstop.',
               'this can shrink the residual risk but, being data-driven, does not by itself furnish a certifiable PFHD/DC '
               'argument.'],
     'raw_file': R + '2608.02809v1.txt',
     'agent_note': 'The standards\' separation formula S = K T + C uses one stopping time T on the clock; the humanoid\'s stop '
                   'time depends on its gait phase, so the worst phase sets T for every phase.'},
    {'id': 'r4:33', 'bottleneck': 'r4-B4', 'role': 'd',
     'source': 'ISO 10218-1:2025 and ISO 10218-2:2025, Robotics - Safety requirements (free sample pages: foreword, '
               'introduction, scope; distributed by iTeh Standards)',
     'version': 'ISO 10218-1:2025 third edition; ISO 10218-2:2025 second edition (sample PDFs created 8 Feb 2025)',
     'url': 'https://cdn.standards.iteh.ai/samples/73933/b5387b20934848a48b4518c9b2e5455d/ISO-10218-1-2025.pdf',
     'quote': ['mobility when robots or manipulators are fixed to or part of mobile platforms;',
               'when the public, all ages or non-working adults have access (e.g. service robots, consumer products).'],
     'raw_file': R + 'iteh_ISO-10218-1-2025_sample.txt',
     'agent_note': 'The published industrial-robot standard excludes the hazards of mobility on mobile platforms and settings '
                   'where the public has access: the certification route assumes a fixed (or statically stable) base and a '
                   'de-energised safe state (ISO 13849-1 / EN 60204-1, r4:25).'},
    {'id': 'r4:34', 'bottleneck': 'r4-B4', 'role': 'd',
     'source': 'IEEE Humanoid Study Group, A Pathway Study for Future Humanoid Standards', 'version': 'September 2025',
     'url': 'https://www.therobotreport.com/wp-content/uploads/2025/09/IEEE-Humanoid-Report-of-Future-Standards-Development.pdf',
     'quote': ['To ensure safety, humanoid robots must be equipped with reliable emergency stop mechanisms, offering various '
               'levels of halting, from immediate power removal to controlled stops, including moving back to a safe state.',
               'these standards make an unwritten assumption that the base of the robots being considered is either fixed or '
               'has a statically stable base.'],
     'raw_file': R + 'IEEE-Humanoid-Report-of-Future-Standards-Development.txt',
     'agent_note': 'Families of stop: power removal (Cat. 0), controlled stop (Cat. 1/2), return to a safe state; the standards\' '
                   'assumption named by the report.'},

    # ---------------- r4-B5: formal verification of neural-network controllers at the scale of deployed policies
    {'id': 'r4:35', 'bottleneck': 'r4-B5', 'role': 'a',
     'source': 'Sasaki, Wooding, Johnson, Althoff et al., ARCH-COMP26 Category Report: Artificial Intelligence and Neural '
               'Network Control Systems (AINNCS) for Continuous and Hybrid Systems Plants (EPiC Series in Computing 110, '
               'pp. 85-130)',
     'version': 'ARCH26 proceedings, 2026 (PDF created 3 Jul 2026)', 'url': 'https://easychair.org/publications/paper/GsKW',
     'quote': ['However, it has been demonstrated that neural network verification is an NP-complete problem [37].'],
     'raw_file': R + 'easychair_GsKW_ARCH26.txt', 'agent_note': 'The problem stated.'},
    {'id': 'r4:36', 'bottleneck': 'r4-B5', 'role': 'b',
     'source': 'Kaulen, Ladner, Bak, Brix et al., The 6th International Verification of Neural Networks Competition (VNN-COMP '
               '2025): Summary and Results',
     'version': 'arXiv v1, 22 Dec 2025', 'url': 'https://arxiv.org/abs/2512.19007v1',
     'quote': ['neural network verification remains an open problem, despite significant efforts over the last years.'],
     'raw_file': R + '2512.19007v1.txt', 'agent_note': '2025 statement.'},
    {'id': 'r4:37', 'bottleneck': 'r4-B5', 'role': 'b',
     'source': 'Sasaki et al., ARCH-COMP26 AINNCS (Conclusion)', 'version': 'ARCH26, 2026',
     'url': 'https://easychair.org/publications/paper/GsKW',
     'quote': ['For this year, we reused the same 12 benchmarks from last year, as several remain open.',
               'the nonlinear safety specification causes the benchmark to remain unsolved one more year.'],
     'raw_file': R + 'easychair_GsKW_ARCH26.txt', 'agent_note': '2026 statement.'},
    {'id': 'r4:38', 'bottleneck': 'r4-B5', 'role': 'c',
     'source': 'Sasaki et al., ARCH-COMP26 AINNCS (Discussion; Table 4)', 'version': 'ARCH26, 2026',
     'url': 'https://easychair.org/publications/paper/GsKW',
     'quote': ['As last year, they have no more than a thousand neurons and no more than 5 hidden layers in their architecture, '
               'unlike some of the networks that can be analyzed in isolation.',
               'QUAD reach ? 9.517 Docking constraint ? 7.489',
               'we can observe the CartPole benchmark being challenging for most tools.'],
     'raw_file': R + 'easychair_GsKW_ARCH26.txt',
     'agent_note': 'Best closed-loop verification result: four tools on 12 benchmarks whose controllers have at most 1,000 '
                   'neurons and 5 hidden layers; unknown verdicts remain (QUAD, Docking for JuliaReach; docking unsolved by all '
                   'for a further year). Target: the policies deployed on robots (r4:39, OpenVLA 7B parameters). The gap is '
                   'about six orders of magnitude in size (1e3 neurons against 7e9 parameters: different units, so an order '
                   'of magnitude reading, cross-source).'},
    {'id': 'r4:39', 'bottleneck': 'r4-B5', 'role': 'c',
     'source': 'Lu et al., CertVLA (Related work)',
     'version': 'arXiv v1, 21 Aug 2026', 'url': 'https://arxiv.org/abs/2608.20791v1',
     'quote': ['OpenVLA provides an open 7B policy'],
     'raw_file': R + '2608.20791v1.txt',
     'agent_note': 'The target scale: a deployed open VLA policy has 7B parameters. For open-loop verification of a single '
                   'network the largest VNN-COMP 2025 benchmark is VGG16 at 138 million parameters (r4:40), still about 50x '
                   'smaller and without the closed loop.'},
    {'id': 'r4:40', 'bottleneck': 'r4-B5', 'role': 'c',
     'source': 'Kaulen et al., VNN-COMP 2025 (Section 4.8)', 'version': 'arXiv v1, 22 Dec 2025',
     'url': 'https://arxiv.org/abs/2512.19007v1',
     'quote': ['All properties are run on the same network, which includes 138 million parameters.'],
     'raw_file': R + '2512.19007v1.txt', 'agent_note': 'Largest network in the competition (open loop, extended track).'},
    {'id': 'r4:41', 'bottleneck': 'r4-B5', 'role': 'd',
     'source': 'Sasaki et al., ARCH-COMP26 AINNCS (Discussion)', 'version': 'ARCH26, 2026',
     'url': 'https://easychair.org/publications/paper/GsKW',
     'quote': ['immrax interprets all benchmarks under continuous feedback rather than the sample-and-hold architecture of '
               'Figure 1, which can yield different verification outcomes, most visibly on Single Pendulum and Attitude Control.',
               'The high frequency of the control steps may lead to an increased conservativeness of the approaches, preventing '
               'most tools from successfully analyzing the benchmark.'],
     'raw_file': R + 'easychair_GsKW_ARCH26.txt',
     'agent_note': 'Clock assumption: reachability tools unroll the closed loop step by step on a fixed control period '
                   '(sample-and-hold); over-approximation error accumulates per step, so a faster clock means more '
                   'conservatism; the verdict can change with the time model (continuous feedback against sample-and-hold).'},
    {'id': 'r4:42', 'bottleneck': 'r4-B5', 'role': 'd',
     'source': 'Li et al., Vision-Language-Action Safety (survey, Section 8.2)', 'version': 'arXiv v2, 25 Aug 2026',
     'url': 'https://arxiv.org/abs/2604.23775v2',
     'quote': ['Promising building blocks combine control-theoretic tools—control barrier functions, reachability analysis, '
               'signal temporal logic—with learned uncertainty estimates from the VLA itself',
               'and produce useful safety signals even under interruption (anytime safety).'],
     'raw_file': R + '2604.23775v2.txt',
     'agent_note': 'Runtime-assurance family (shields: barrier functions, reachability, STL) proposed in place of verifying the '
                   'policy itself; the survey names interruption (anytime safety) as a requirement.'},

    # ---------------- r4-B6: cybersecurity of commercial robots and fleets
    {'id': 'r4:43', 'bottleneck': 'r4-B6', 'role': 'a',
     'source': 'Mayoral-Vilches, Ayucar-Carbajo, Laflamme, Peng, Sanz-Gómez, Balassone, Apa & Gil-Uriarte (Alias Robotics, '
               'IOActive), Cybersecurity AI: Hacking Consumer Robots in the AI Era',
     'version': 'arXiv v2, 10 Mar 2026 (v1 9 Mar 2026)', 'url': 'https://arxiv.org/abs/2603.08665v2',
     'quote': ['Consumer robots—from autonomous lawnmowers to powered exoskeletons and window cleaners—are rapidly entering homes '
               'and workplaces, yet their security remains rooted in assumptions of specialized attacker expertise.'],
     'raw_file': R + '2603.08665v2.txt',
     'agent_note': 'The problem stated. The authors are a robot-security company (Alias Robotics) and use their own tool (CAI); '
                   'recorded as such.'},
    {'id': 'r4:44', 'bottleneck': 'r4-B6', 'role': 'b',
     'source': 'Mayoral-Vilches et al., Hacking Consumer Robots in the AI Era', 'version': 'arXiv v2, 10 Mar 2026',
     'url': 'https://arxiv.org/abs/2603.08665v2',
     'quote': ['Our findings reveal a stark asymmetry: while offensive capabilities have been democratized through AI, defensive '
               'measures often remain lagging behind.'],
     'raw_file': R + '2603.08665v2.txt', 'agent_note': '2026 statement.'},
    {'id': 'r4:45', 'bottleneck': 'r4-B6', 'role': 'b',
     'source': 'Sabouri, Cybersecurity of Teleoperated Quadruped Robots: A Systematic Survey of Vulnerabilities, Threats, and '
               'Open Defense Gaps',
     'version': 'arXiv v1, 26 Feb 2026', 'url': 'https://arxiv.org/abs/2602.23404v1',
     'quote': ['Technology Readiness Level classification of defenses exposing a critical maturity gap between field-deployed '
               'communication protections (TRL 7–9) and largely experimental perception and operator-layer defenses (TRL 3– 5)'],
     'raw_file': R + '2602.23404v1.txt',
     'agent_note': '2026 survey (single author, University of Genoa student address) of 2019-2025 literature and disclosures.'},
    {'id': 'r4:46', 'bottleneck': 'r4-B6', 'role': 'c',
     'source': 'Mayoral-Vilches et al., Hacking Consumer Robots in the AI Era (Abstract; Table 1)', 'version': 'arXiv v2, 10 Mar '
               '2026', 'url': 'https://arxiv.org/abs/2603.08665v2',
     'quote': ['Hookii Neomow China Outdoor WiFi, MQTT, ADB, ROS 2 9 2.5 hours Physical + Privacy',
               'Hypershell X China Wearable BLE, REST API, CAN Bus 12 1.5 hours† Safety-critical',
               'HOBOT S7 Pro Taiwan Indoor BLE, Cloud API, HTTP 17 3 hours',
               'uncovering fleet-wide vulnerabilities and data protection violations affecting 267+ connected devices',
               'Across these platforms, CAI discovered in an automated manner 38 vulnerabilities that would have previously '
               'required months of specialized security research.'],
     'raw_file': R + '2603.08665v2.txt',
     'agent_note': 'Three commercial robots, 9 / 12 / 17 vulnerabilities found in 2.5 / 1.5 / 3 hours of automated assessment; '
                   'the best (fewest) is 9. Target (r4:48): vulnerabilities handled for the support period under the EU CRA, '
                   'main obligations from 11 Dec 2027; zero known exploitable vulnerabilities at placing on the market is the '
                   'CRA\'s Annex I requirement, not quoted here because EUR-Lex was unreachable. Gap: every assessed product '
                   'had at least 9 findings.'},
    {'id': 'r4:47', 'bottleneck': 'r4-B6', 'role': 'c',
     'source': 'Mayoral-Vilches, Makris & Finisterre, Cybersecurity AI: Humanoid Robots as Attack Vectors (Unitree G1)',
     'version': 'arXiv v3, 23 Sep 2025 (v1 17 Sep 2025)', 'url': 'https://arxiv.org/abs/2509.14139v3',
     'quote': ['exploitable using hardcoded AES keys shared across all units.',
               'the most mature we have observed in commercial robotics.',
               'Blowfish-ECB with a static 128-bit key (effective entropy: 0 bits due to fleet-wide key reuse across all '
               'devices)'],
     'raw_file': R + '2509.14139v3.txt',
     'agent_note': 'Fleet level: the platform the authors call the most mature they have seen still shares one key across every '
                   'unit, so one extraction compromises the fleet.'},
    {'id': 'r4:48', 'bottleneck': 'r4-B6', 'role': 'c',
     'source': 'European Commission, Cyber Resilience Act - summary of the legislative text (digital-strategy.ec.europa.eu); '
               'CRA policy page',
     'version': 'summary page last updated 3 Dec 2025; policy page last updated 7 Sep 2026',
     'url': 'https://digital-strategy.ec.europa.eu/en/policies/cra-summary',
     'quote': ['Part II relates to the vulnerability handling requirements: manufacturers shall ensure, when placing a product '
               'with digital elements on the market, and for the support period, that vulnerabilities of that product, '
               'including its components, are handled effectively and in accordance with such requirements.'],
     'raw_file': R + 'ec_cra-summary.txt',
     'agent_note': 'The regulatory target (EU). The CRA text on EUR-Lex was not reachable (HTTP 202, empty body).'},
    {'id': 'r4:49', 'bottleneck': 'r4-B6', 'role': 'c',
     'source': 'European Commission, Cyber Resilience Act policy page', 'version': 'last updated 7 Sep 2026',
     'url': 'https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act',
     'quote': ['The CRA entered into force on 10 December 2024. The main obligations introduced by the Act will apply from 11 '
               'December 2027, with reporting obligations to apply as of 11 September 2026.'],
     'raw_file': R + 'ec_digital-strategy_cyber-resilience-act.txt', 'agent_note': 'The date the target binds.'},
    {'id': 'r4:50', 'bottleneck': 'r4-B6', 'role': 'd',
     'source': 'Sabouri, Cybersecurity of Teleoperated Quadruped Robots (Section VI, Gap 1)', 'version': 'arXiv v1, 26 Feb 2026',
     'url': 'https://arxiv.org/abs/2602.23404v1',
     'quote': ['Current ML-based intrusion detection systems achieve 97– 99% accuracy on general ROS2/IoT traffic (Table XVII), '
               'but these results are conditioned on datasets where traffic patterns are approximately stationary—an assumption '
               'that fundamentally breaks down for quadruped teleoperation.',
               'the detector must maintain a phase-conditioned baseline that adapts to the robot’s current locomotion state '
               '(gait mode, terrain class, contact configuration) rather than relying on a single global traffic model.'],
     'raw_file': R + '2602.23404v1.txt',
     'agent_note': 'Intrusion-detection family: assumes stationary traffic and one global model on the clock; the survey argues '
                   'for a baseline conditioned on the robot\'s own gait phase.'},
    {'id': 'r4:51', 'bottleneck': 'r4-B6', 'role': 'd',
     'source': 'Mayoral-Vilches et al., Hacking Consumer Robots in the AI Era (Abstract)',
     'version': 'arXiv v2, 10 Mar 2026', 'url': 'https://arxiv.org/abs/2603.08665v2',
     'quote': ['We argue that traditional defense-in-depth architectures like the Robot Immune System (RIS) must evolve toward '
               'GenAI-native defensive agents capable of matching the speed and adaptability of AI-powered attacks.'],
     'raw_file': R + '2603.08665v2.txt',
     'agent_note': 'Defence-in-depth family (RIS, a host-based robot endpoint protection) and the proposed AI-agent defence; '
                   'both assume continuous monitoring of the fleet. ISO 10218-1:2025 adds cybersecurity only "to the extent '
                   'that it applies to industrial robot safety" (r4:52).'},
    {'id': 'r4:52', 'bottleneck': 'r4-B6', 'role': 'd',
     'source': 'ISO 10218-1:2025 (foreword, free sample, iTeh Standards)', 'version': 'third edition, 2025',
     'url': 'https://cdn.standards.iteh.ai/samples/73933/b5387b20934848a48b4518c9b2e5455d/ISO-10218-1-2025.pdf',
     'quote': ['adding requirements for cybersecurity to the extent that it applies to industrial robot safety;'],
     'raw_file': R + 'iteh_ISO-10218-1-2025_sample.txt',
     'agent_note': 'The standards route: cybersecurity enters the industrial-robot standard only as it bears on safety.'},

    # ---------------- r4-B7: privacy of robots' sensor data (physical-world privacy of embodied agents; consumer robots)
    {'id': 'r4:53', 'bottleneck': 'r4-B7', 'role': 'a',
     'source': 'Fan, Chen, Liu, Yang, Xu, Shen, Liu, Qi & Wang, Position: Embodied AI Requires a Privacy-Utility Trade-off '
               '(ICML 2026)',
     'version': 'arXiv v1, 6 May 2026', 'url': 'https://arxiv.org/abs/2605.05017v1',
     'quote': ['without considering their coupled privacy implications in high-frequency deployments where privacy leakage is '
               'often irreversible.'],
     'raw_file': R + '2605.05017v1.txt', 'agent_note': 'The problem stated.'},
    {'id': 'r4:54', 'bottleneck': 'r4-B7', 'role': 'b',
     'source': 'Gong, Chen, Liu, Wang & Lam, SoK: Security and Privacy of Foundation-Model-Powered Robots',
     'version': 'arXiv v1, 15 Jun 2026', 'url': 'https://arxiv.org/abs/2606.16788v1',
     'quote': ['existing reviews tend to over-prioritize security attacks and defenses while privacy risks and mitigation '
               'strategies remain comparatively underexplored.'],
     'raw_file': R + '2606.16788v1.txt', 'agent_note': '2026 statement.'},
    {'id': 'r4:55', 'bottleneck': 'r4-B7', 'role': 'b',
     'source': 'Fan et al., Position: Embodied AI Requires a Privacy-Utility Trade-off', 'version': 'arXiv v1, 6 May 2026',
     'url': 'https://arxiv.org/abs/2605.05017v1',
     'quote': ['In summary, current privacy-aware EAI solutions remain largely stage-local and disjointed.'],
     'raw_file': R + '2605.05017v1.txt', 'agent_note': '2026 statement.'},
    {'id': 'r4:56', 'bottleneck': 'r4-B7', 'role': 'c',
     'source': 'Shen, Li & Li, Measuring Physical-World Privacy Awareness of Large Language Models: An Evaluation Benchmark '
               '(EAPrivacy; ICLR 2026)',
     'version': 'arXiv v3, 15 Feb 2026 (v1 27 Sep 2025)', 'url': 'https://arxiv.org/abs/2510.02356v3',
     'quote': ['The top-performing model, Gemini 2.5 Pro, achieved only 59% accuracy in scenarios involving changing physical '
               'environments. Furthermore, when a task was accompanied by a privacy request, models prioritized completion over '
               'the constraint in up to 86% of cases.',
               'the agent’s performance is evaluated based on its ability to generate an action plan that respects the privacy '
               'of a secret item while still completing the task of moving all items from a location.',
               'best performing models, 2.5-flash-w.o.think and 4o, achieve the lowest violation rates of 71%.'],
     'raw_file': R + '2510.02356v3.txt',
     'agent_note': 'Tier 2 (selection against the action humans rated most appropriate): best 59%, gap 41 points to the '
                   'human-rated choice. Tier 3 (respect the secret item while completing the task): lowest privacy '
                   'violation rate 71% against the stated goal of no violation, gap 71 points. LLM planners in simulation, '
                   'not deployed robots.'},
    {'id': 'r4:57', 'bottleneck': 'r4-B7', 'role': 'c',
     'source': 'Mayoral-Vilches et al., Hacking Consumer Robots in the AI Era (Appendix A)', 'version': 'arXiv v2, 10 Mar 2026',
     'url': 'https://arxiv.org/abs/2603.08665v2',
     'quote': ['None of the three robots were found to implement consent management or data subject rights mechanisms '
               'consistent with GDPR requirements.',
               'CAI conducted a systematic probe of 18 GDPR-related API endpoint patterns across the Gizwits cloud platform. All '
               'requests returned HTTP 404:',
               'Telemetry transmission begins automatically upon device power-on and continues without interruption.'],
     'raw_file': R + '2603.08665v2.txt',
     'agent_note': 'Deployed consumer robots against the GDPR data-subject rights (access, erasure, portability, consent): 0 of 3 '
                   'robots, 0 of 18 endpoint patterns. The GDPR text itself (EUR-Lex) was not reachable; the target is as the '
                   'authors cite it.'},
    {'id': 'r4:58', 'bottleneck': 'r4-B7', 'role': 'c',
     'source': 'Mayoral-Vilches, Makris & Finisterre, Humanoid Robots as Attack Vectors (Unitree G1)',
     'version': 'arXiv v3, 23 Sep 2025', 'url': 'https://arxiv.org/abs/2509.14139v3',
     'quote': ['continuously exfiltrating multi-modal sensor and service-state telemetry to 43.175.228.18:17883 and '
               '43.175.229.18:17883 every 300 seconds without operator notice, creating violations of GDPR Articles 6 and 13'],
     'raw_file': R + '2509.14139v3.txt', 'agent_note': 'A humanoid\'s sensor telemetry sent every 300 s without notice.'},
    {'id': 'r4:59', 'bottleneck': 'r4-B7', 'role': 'd',
     'source': 'Fan et al., Position: Embodied AI Requires a Privacy-Utility Trade-off', 'version': 'arXiv v1, 6 May 2026',
     'url': 'https://arxiv.org/abs/2605.05017v1',
     'quote': ['Even with sanitized perception, action planning remains vulnerable, as trajectories may leak routines or intent. '
               'This motivates privacy-aware motion planning, federated VLN, and secure multi-robot coordination',
               'modulating constraints based on real-time contextual sensitivity rather than fixed penalties.'],
     'raw_file': R + '2605.05017v1.txt',
     'agent_note': 'Families: sanitised perception (per frame), privacy-aware planning, federated learning; each stage-local with '
                   'fixed penalties; the position argues for a privacy signal that varies with context over the life cycle. '
                   'Deployed products (r4:57) stream telemetry on a fixed clock from power-on.'},

    # ---------------- r4-B8: collaborative operation: throughput lost to safety speed reduction (SSM / PFL)
    {'id': 'r4:60', 'bottleneck': 'r4-B8', 'role': 'a',
     'source': 'Faroni, Spanò, Zanchettin & Rocco, Learning-Based Safety-Aware Task Scheduling for Efficient Human-Robot '
               'Collaboration (IEEE RA-L, accepted Dec 2025)',
     'version': 'arXiv v1, 19 Dec 2025', 'url': 'https://arxiv.org/abs/2512.17560v1',
     'quote': ['Ensuring human safety in collaborative robotics can compromise efficiency because traditional safety measures '
               'increase robot cycle time when human interaction is frequent.',
               'Techniques such as Speed and Separation Monitoring (SSM) and Power and Force Limitation (PFL) ensure safety by '
               'applying speed reduction rules. However, the speed reduction significantly impacts robot cycle times, leading '
               'to inefficiencies in collaboration.'],
     'raw_file': R + '2512.17560v1.txt', 'agent_note': 'The problem stated.'},
    {'id': 'r4:61', 'bottleneck': 'r4-B8', 'role': 'b',
     'source': 'Bricher & Müller, Analysis of Deep-Learning Methods in an ISO/TS 15066-Compliant Human-Robot Safety Framework '
               '(Sensors 25(23):7136)',
     'version': 'published 22 Nov 2025 (PMC12694355; DOI 10.3390/s25237136)',
     'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12694355/',
     'quote': ['current ISO/TS-15066-compliant implementations often limit the efficiency of collaborative tasks due to '
               'conservative speed restrictions.',
               'further investigations are required on robustness, reliability, multi-camera integration for plausibility '
               'verification, fail-safe scenarios, and functional safety certification.'],
     'raw_file': R + 'pmc_PMC12694355.txt', 'agent_note': '2025 statement; the perception-based alternative is not certified.'},
    {'id': 'r4:62', 'bottleneck': 'r4-B8', 'role': 'c',
     'source': 'Faroni et al. (Table III, real UR5e pick-and-packaging with a human operator; Section III)',
     'version': 'arXiv v1, 19 Dec 2025', 'url': 'https://arxiv.org/abs/2512.17560v1',
     'quote': ['the actual robot speed is equal to the nominal speed (i.e., without human presence) multiplied by s(xr, xh).',
               'random 24.7(6.6) 0.60 24.9(6.6) 0.59',
               'greedy 18.6(1.7) 0.74 20.2(3.9) 0.68'],
     'raw_file': R + '2512.17560v1.txt',
     'agent_note': 'Columns: variant 1 (exec. time per task in s, mean speed scaling s), variant 2 (same). Best method: mean '
                   'speed scaling 0.74 (variant 1) and 0.68 (variant 2) against the nominal speed without a human (s = 1): '
                   '26% and 32% of the nominal speed still lost; random task choice 0.60 / 0.59. The oracle s = 1 is an upper '
                   'bound that no safe system reaches while a human is near; the recoverable part is smaller. Same paper, same '
                   'protocol.'},
    {'id': 'r4:63', 'bottleneck': 'r4-B8', 'role': 'c',
     'source': 'Bricher & Müller (Sensors 2025), abstract', 'version': 'published 22 Nov 2025',
     'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12694355/',
     'quote': ['Experiments demonstrated a quantitative reduction in cycle time of up to 15% compared to conventional safety '
               'technology.'],
     'raw_file': R + 'pmc_PMC12694355.txt',
     'agent_note': 'Supporting: body-part-aware speed adaptation (KUKA iiwa screwing task; single subject, per the authors) cuts '
                   'cycle time by up to 15% against a laser scanner.'},
    {'id': 'r4:64', 'bottleneck': 'r4-B8', 'role': 'd',
     'source': 'Faroni et al. (Introduction; Section V-D)', 'version': 'arXiv v1, 19 Dec 2025',
     'url': 'https://arxiv.org/abs/2512.17560v1',
     'quote': ['commonly used static safety zones cause robots to slow down or stop when a human enters a predefined area, '
               'leading to increased cycle times during frequent interactions.',
               'we set w equal to the average duration of the robot’s actions (∼14 s) in the greedy method.'],
     'raw_file': R + '2512.17560v1.txt',
     'agent_note': 'Static-zone family: fixed boundaries set at installation. Scheduling family: a predictive window w fixed on '
                   'the clock (about 14 s, the mean action duration; 18 s for the Monte Carlo variant).'},
    {'id': 'r4:65', 'bottleneck': 'r4-B8', 'role': 'd',
     'source': 'Bricher & Müller (Sensors 2025)', 'version': 'published 22 Nov 2025',
     'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12694355/',
     'quote': ['Typically, the robot speed is adjusted to a constant value that is in accordance with the most restrictive '
               'collision situation that is possible at a particular work place, which ultimately increases the robot cycle '
               'time for process execution.'],
     'raw_file': R + 'pmc_PMC12694355.txt',
     'agent_note': 'PFL practice: one constant speed tuned to the worst case, independent of where the person actually is.'},
    {'id': 'r4:66', 'bottleneck': 'r4-B8', 'role': 'd',
     'source': 'ISO 10218-2:2025 (foreword and introduction, free sample, iTeh Standards)', 'version': 'second edition, 2025',
     'url': 'https://cdn.standards.iteh.ai/samples/73934/3578b7f9a402489fb9af1cf1ca03ea68/ISO-10218-2-2025.pdf',
     'quote': ['incorporating safety requirements for collaborative applications (formerly, the content of ISO/TS 15066);',
               'Safety functions that enable a collaborative application can be part of the robot (e.g. PFL), or can be '
               'provided by a protective device, or a combination.'],
     'raw_file': R + 'iteh_ISO-10218-2-2025_sample.txt',
     'agent_note': 'The standards context in 2025: ISO/TS 15066 is folded into ISO 10218-2:2025; the method families (PFL, SSM '
                   'via protective devices) are unchanged.'},
]

BOTTLENECKS = [
    {'id': 'r4-B1', 'name': 'Jailbreaks of LLM/VLM-planned robots',
     'problem': 'Adversarial instructions make LLM- or VLM-planned robots execute harmful physical actions; guardrails cut the '
                'attack success on their authors\' data but not uniformly on independent benchmarks.',
     'open': True,
     'benchmark': 'RoboJailBench (six intent-contrast datasets; attacks CD, CJ, SM, RoboPAIR; security rate SR, utility rate UR); '
                  'RoboGuard\'s own RoboPAIR suite (70 prompts x 3 environments)',
     'best': 'RoboGuard on its own suite: attack success 2.3% (non-adaptive RoboPAIR) to 5.2% (white-box adaptive), utility '
             '100%; on RoboJailBench RJB-Instructions: SR 65.00, UR 100.00, conceptual-deception ASR 94.44%; J-DAPT detection '
             'accuracy "nearly 100%"; AuthGuard-R 109/109 unauthorised actions blocked (preliminary)',
     'target': '"the adversarial goal should be rejected, maximizing both utility and security" (SR 100 at UR 100)',
     'gap_note': 'own-suite: 2.3-5.2 points of attack success above zero; independent benchmark: 35.0 points of security rate '
                 'on RJB-Instructions (the best defence), with CD attacks at 93.33-100% on four datasets under either defence. '
                 'Different protocols; not pooled. Contrary evidence (J-DAPT, AuthGuard-R) is on narrower threats or preliminary.',
     'assumptions': ['classifier detection: the attack distribution of a fixed training set (no drift)',
                     'specification guardrail: rules written in advance and grounded once per plan in a world-model snapshot',
                     'authorisation: a signed mission with a fixed scope and time window (boundaries given from outside)',
                     'evaluation: one instruction and one frame per episode; no temporally extended attack'],
     'cpu_testable': False,
     'cpu_note': 'the reference numbers use frontier LLM/VLM planners (GPT-4o, Claude, Gemini) through APIs, not available '
                 'here (no API key); a reduced proxy with a small local model (as in STAKE1) runs on CPU but is not the '
                 'benchmark'},
    {'id': 'r4-B2', 'name': 'Physical adversarial attacks on VLA policies and certified defence',
     'problem': 'A printed patch in the camera view collapses VLA task success on real arms; defences are mostly empirical and '
                'the one certified defence recovers only part of the loss on a real robot.',
     'open': True,
     'benchmark': 'Real-robot pick-and-place with a physical patch (CertVLA Table 2, pi0.5, 10 trials); LIBERO patch/texture '
                  'attacks (CertVLA Table 1); printed-patch attack on OpenVLA-7B (RA-L 2026, 50 trials)',
     'best': 'CertVLA real robot: defended 60%, certified 30% (attacked 40%); simulation best certified average 94.00',
     'target': 'attack-free (clean) success 90% on the same task and policy',
     'gap_note': '30 points (defended) and 60 points (certified) below clean on the real robot; same paper, same protocol. '
                 'Simple input defences leave ASR at 79.2-80.2% against 81.0% undefended (other paper).',
     'assumptions': ['empirical defences: robustness only to the attacks tried in training',
                     'certified defence: a bounded-support threat model and a certificate per policy query chained over the '
                     'rollout (the query clock); calibration constants fixed on held-out clean episodes',
                     'attacks: earlier work assumed the whole trajectory; 2026 attacks use a short prefix and a fixed patch'],
     'cpu_testable': False,
     'cpu_note': 'the benchmarks run 3B-7B VLA policies (OpenVLA, pi0, pi0.5) in LIBERO and on real arms; GPU inference per '
                 'step; not reproducible on this CPU in hours'},
    {'id': 'r4-B3', 'name': 'Runtime failure detection for generalist learned policies',
     'problem': 'Monitors that must raise a timely alarm when a VLA policy is failing, on tasks they never saw, remain far from '
                'a perfect detector; post-hoc VLM judges approach chance on contact-rich tasks.',
     'open': True,
     'benchmark': 'LIBERO-10 multitask failure detection, unseen tasks, OpenVLA (Hide-and-Seek Table 1: bACC, TWA); FailBench '
                  '(2,197 attempts, 14 sources, balanced accuracy)',
     'best': 'bACC 0.834, TWA 0.663 on unseen tasks (Hide-and-Seek); FailBench best mean balanced accuracy 0.77, at most 0.60 on '
             'contact-intensive assembly; VLA-Scope ROC-AUC 0.8497 after 60 actions on OOD rollouts (other protocol)',
     'target': 'the ground-truth outcome labels (a perfect detector: bACC 1.0, alarm at failure onset)',
     'gap_note': '0.166 bACC and 0.337 TWA below a perfect detector on unseen LIBERO tasks; 0.23 (FailBench mean) and >= 0.40 '
                 '(contact-rich); 0.150 ROC-AUC (VLA-Scope); each within one paper, protocols differ.',
     'assumptions': ['benchmark failure defined by a clock: a time-out at the maximum rollout length (elapsed time alone '
                     'would detect it)',
                     'per-timestep thresholds from conformal prediction on the step clock, valid under exchangeability',
                     'label weights that grow linearly with the step index (SAFE-MLP)',
                     'detector trained on one policy\'s rollouts (policy-dependent) or a frozen VLM judge'],
     'cpu_testable': False,
     'cpu_note': 'rollouts of 7B VLAs in LIBERO are GPU-scale; a small proxy (a toy policy, synthetic failures) would run on CPU '
                 'but is not the benchmark'},
    {'id': 'r4-B4', 'name': 'Emergency stop of dynamically balancing (legged, humanoid) robots',
     'problem': 'Classical emergency stops remove power (Stop Category 0), which makes a balancing robot fall; the controlled '
                'standstill that replaces it depends on the robot\'s own learned or model-based policy and cannot yet be '
                'certified; no published standard covers actively balancing robots (ISO 25785-1 in development).',
     'open': True,
     'benchmark': 'ISO 13849-1 / IEC 62061 rating of the emergency-stop chain (PFHD, PL, SILCL) on a Unitree G1 cell; ISO 13855 '
                  'stopping time; learned safe-stoppability prediction accuracy (PRISM, simulation)',
     'best': 'external chain ratable to PL e; robot-side reaction chain: no PFHD, no PL; stop 0.3-1.0 s, worst-case response '
             'about 1.1 s; comm-loss standstill 12/12 trials in 0.5-1.3 s; learned monitor 99.38% of unsafe states flagged at '
             '62.05% safe accuracy',
     'target': 'the certified reference chain: PL e / SIL 3, total PFHD 7.35e-9 (ISO 13849-1), with Stop Category 0 power removal',
     'gap_note': 'categorical: the reaction subsystem that closes the reference\'s PL e figure has no rated equivalent on the '
                 'humanoid; a per-state accuracy (PRISM) is not a per-hour dangerous-failure rate. Same paper for target and '
                 'best (Siemens).',
     'assumptions': ['fail-passive safe state: de-energising is safe (ISO 13849-1 / EN 60204-1)',
                     'fixed or statically stable base (ISO 10218-1/-2:2025 exclude mobile-platform mobility)',
                     'one stopping time T on the clock in S = K T + C, sized by the worst gait phase',
                     'the stop can arrive at any instant; one fixed fallback policy trained in advance',
                     'SIL/PL assume deterministic systems'],
     'cpu_testable': False,
     'cpu_note': 'the named metrics are a functional-safety rating and stopping times measured on a real humanoid cell; a '
                 'reduced proxy (a planar biped or inverted-pendulum walker with a fallback controller and E-stops injected at '
                 'random gait phases) runs on CPU with numpy/scipy, but it is a proxy'},
    {'id': 'r4-B5', 'name': 'Formal verification of neural controllers at deployed scale',
     'problem': 'Closed-loop verification of neural-network controllers handles networks of at most a thousand neurons, with '
                'some benchmarks unsolved for years; deployed robot policies have billions of parameters.',
     'open': True,
     'benchmark': 'ARCH-COMP26 AINNCS (12 closed-loop benchmarks, 4 tools); VNN-COMP 2025 (open-loop)',
     'best': 'closed loop: controllers <= 1,000 neurons, <= 5 hidden layers, with unknown verdicts left (docking unsolved another '
             'year); open loop: a 138-million-parameter VGG16',
     'target': 'the policies deployed on robots: OpenVLA 7B parameters',
     'gap_note': 'about six orders of magnitude (1e3 neurons against 7e9 parameters; different units, cross-source, an '
                 'order-of-magnitude reading); about 50x even for open-loop verification of one network.',
     'assumptions': ['sample-and-hold control on a fixed period; the loop unrolled step by step, conservatism growing with the '
                     'number of steps (verdicts change with the time model)',
                     'small feed-forward controllers with low-dimensional state inputs',
                     'runtime assurance (barrier functions, reachability, STL shields) instead of verifying the policy; anytime '
                     'safety under interruption named as a requirement'],
     'cpu_testable': True,
     'cpu_note': 'the ARCH-COMP benchmarks and tools (CORA, JuliaReach, CROWN-Reach) run on CPU in seconds to minutes per '
                 'instance; the 7B target does not'},
    {'id': 'r4-B6', 'name': 'Cybersecurity of commercial robots and fleets',
     'problem': 'Commercial robots ship with exploitable vulnerabilities and fleet-wide shared secrets that automated tools now '
                'find in hours; defences lag.',
     'open': True,
     'benchmark': 'Vulnerabilities found per platform by an automated assessment (Alias Robotics CAI, three consumer robots; '
                  'Unitree G1)',
     'best': 'fewest findings on an assessed product: 9 (Hookii Neomow, 2.5 h); 12 and 17 on the others; G1 (the most mature '
             'seen) with one static key across all units',
     'target': 'EU CRA: vulnerabilities handled effectively for the support period (main obligations from 11 Dec 2027)',
     'gap_note': 'every assessed product had >= 9 findings; the CRA Annex I text (no known exploitable vulnerabilities) could '
                 'not be fetched (EUR-Lex unreachable), so the zero-vulnerability target is recorded as unverified. Vendor-'
                 'authored assessments, one tool.',
     'assumptions': ['intrusion detection trained on stationary traffic with one global model (clock-indexed)',
                     'fleet-wide shared keys (one secret for every unit)',
                     'defence in depth on the host, updated on the vendor\'s schedule',
                     'standards cover cybersecurity only as it bears on safety'],
     'cpu_testable': False,
     'cpu_note': 'the named metric is an assessment of real products; a synthetic proxy (a fleet or ROS 2 traffic model with '
                 'gait-phase-modulated messages and injected attacks) runs on CPU, but it is a proxy'},
    {'id': 'r4-B7', 'name': 'Privacy of robots\' sensor data and physical-world privacy awareness',
     'problem': 'LLM-driven embodied agents violate privacy constraints in most physical scenarios, and deployed consumer robots '
                'stream sensor telemetry without consent or data-subject rights.',
     'open': True,
     'benchmark': 'EAPrivacy (ICLR 2026) tiers 2-3; GDPR data-subject-rights endpoints on three consumer robots',
     'best': 'Tier 2 selection accuracy 59% (Gemini 2.5 Pro); Tier 3 lowest privacy violation rate 71%; consumer robots 0/3 '
             'with consent management, 0/18 endpoint patterns',
     'target': 'Tier 3: respect the secret item while completing the task (0% violations); Tier 2: the human-rated most '
               'appropriate action; GDPR rights of access, erasure, portability and consent (as cited by the authors)',
     'gap_note': '41 points (Tier 2), 71 points (Tier 3), 3 of 3 products and 18 of 18 endpoints missing; within each source.',
     'assumptions': ['sanitised perception applied per frame; privacy as a fixed penalty at one stage',
                     'telemetry on a fixed clock from power-on, without interruption',
                     'LLM planners follow the explicit instruction over inferred constraints'],
     'cpu_testable': False,
     'cpu_note': 'the EAPrivacy scenarios are text/PDDL but the reference numbers are frontier LLMs through APIs (not '
                 'available here); a small local model on CPU would be a proxy; the consumer-robot findings need the products'},
    {'id': 'r4-B8', 'name': 'Collaborative throughput lost to safety speed reduction',
     'problem': 'Speed and separation monitoring and power-and-force limiting slow the robot whenever a person is near, so '
                'collaborative cells lose much of their nominal speed.',
     'open': True,
     'benchmark': 'Mean speed scaling s and time per task, real UR5e pick-and-packaging with a human (Faroni et al., Table III)',
     'best': 's = 0.74 (variant 1) and 0.68 (variant 2), greedy learned scheduling; up to 15% cycle-time reduction from '
             'body-part-aware speed adaptation (other paper)',
     'target': 'the nominal speed without human presence (s = 1)',
     'gap_note': '26% and 32% of nominal speed still lost; the oracle s = 1 is an upper bound that a safe cell does not reach '
                 'with a person present, so the recoverable gap is smaller and not quantified by the source.',
     'assumptions': ['static safety zones set at installation (boundaries fixed)',
                     'one constant speed for the most restrictive collision case (PFL tuning)',
                     'scheduling with a predictive window fixed on the clock (~14 s)'],
     'cpu_testable': False,
     'cpu_note': 'the named benchmark is a real UR5e cell with a human operator; a simulated shared-workspace scheduling model '
                 'with a stepwise speed-scaling function (as the paper\'s own simulation, Table II) runs on CPU in minutes, as '
                 'a proxy'},
]
