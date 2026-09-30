"""ROB1 stage 1b, family R4 (Robotics/DECLARATION.md): the double check of the safety, trust and security bottlenecks r4-B1 ... r4-B8.

Written by a second agent that did not harvest family R4. For every bottleneck in `claims_r4.BOTTLENECKS` it searched
independently (29 WebSearch queries, different from the harvester's 16; log in /tmp/claude-0/rob_src/r4x/search/queries.txt,
fetch log in r4x/search/fetch_log.txt) for the strongest contrary evidence: a 2025-26 source reporting the target reached on
the named metric, a deployed system that does it, or a source arguing that the bottleneck is misframed. It also re-read the
harvester's quotes and numbers against the harvester's raw texts (/tmp/claude-0/rob_src/r4/txt/); a scratch copy of
Open_Bottlenecks/checks/verify.py pointed at claims_r4.py read "quotes found verbatim: 134 of 134 (claims 67; raw files 31,
missing 0)" (r4x/verify_r4_recheck.txt).

Every source was fetched on 2026-09-30 through the session proxy with curl (TLS verification on). Text was extracted with the
harvester's own extractors (copied to r4x/): PDFs by pymupdf (`page.get_text()`, pages joined by newlines); HTML by
BeautifulSoup 4 (`get_text('\n')` after removing script/style/noscript/svg, runs of spaces and blank lines collapsed); the two
NVD CVE records (JSON from the NVD 2.0 API) were written to one text file as id, dates and the English description; the
UniPwn README (Markdown, from raw.githubusercontent.com) is used as fetched. Raw files live
outside the repository under /tmp/claude-0/rob_src/ (`raw_file` is relative to that root; the fetched originals are in
r4x/src/); their sha256 is in /tmp/claude-0/rob_src/r4x/SHA256SUMS.txt and in the dossier docs/citations/rob1_r4_2026-09-30.md
(section "Stage 1b double check"). Five harvester PDFs were re-fetched into r4x/ and are byte-identical to the harvester's
copies (2605.30834v2, 2605.19328v1, 2503.07885v2, 2510.02356v3, 2608.20791v1); where a claim below quotes one of them it
quotes the re-fetched copy. Table rows are quoted as the extractor emitted them, cell by cell in reading order.

Fields. role = 'x' (a double-check claim). `refutes` = the bottleneck the claim bears on. `contrary` = True when the claim is
contrary evidence (the target reached, a deployed system that does it, or a misframing argument); False when it is a re-check
of the harvester's reading (a number, a "best" or a target the harvester got wrong, overstated or left out), which bears on
the bottleneck's B-c but is not evidence that the bottleneck is closed. `shows_target_reached` = True only if the verified
quote shows the target reached on the named metric of that bottleneck. `agent_note` is the double-checker's reading, fair to
both sides; it is not the source's words. Company statements and trade press are recorded as such.

CHECKS: one entry per bottleneck: what was searched, what was found, and `harvester_errors` (quotes or numbers the harvester
got wrong or overstated; an empty list when none was found).
"""

R = 'r4x/txt/'

CLAIMS = [
    # ---------------- r4-B1: jailbreaks of LLM/VLM-planned robots
    {'id': 'r4x:1', 'bottleneck': 'r4-B1', 'role': 'x', 'refutes': 'r4-B1', 'contrary': True, 'shows_target_reached': False,
     'source': 'Ravichandran, Robey, Kumar, Pappas & Hassani, Safety Guardrails for LLM-Enabled Robots (RoboGuard; IEEE RA-L, '
               'accepted Feb 2026), Section IV-D and Table IV (real-world experiments)',
     'version': 'arXiv v2, 3 Mar 2026 (v1 10 Mar 2025); re-fetched PDF byte-identical to the harvester\'s copy',
     'url': 'https://arxiv.org/abs/2503.07885v2',
     'quote': ['We consider five rephrasing for each of the seven harmful behaviors defined above, for a total of 35 harmful '
               'behaviors.',
               'None, safe task (↑) Direct Prompting 100 ± 0% 100 ± 0%',
               'Non-adaptive (↓) RoboPAIR 100 ± 0% 0 ± 0% TABLE IV REAL WORLD EXPERIMENTAL RESULTS',
               'we were able to generate increasingly difficult scenarios in simulation.'],
     'raw_file': R + '2503.07885v2.txt',
     'agent_note': 'On a physical robot (Clearpath Jackal, onboard semantic mapping) RoboGuard took RoboPAIR from 100% attack '
                   'success to 0% while safe-task utility stayed at 100%: literally the stated target (every adversarial goal '
                   'rejected, every benign goal executed) on the ASR/utility metric. Not counted as the target reached for '
                   'r4-B1: the set is 35 behaviours, only non-adaptive attacks were run on the robot, and the authors say the '
                   'simulated scenarios were the harder ones; on the harvester\'s two named benchmarks (RoboGuard\'s own suite, '
                   '2.3-5.2% ASR, 2.5-5.2% under adaptive attack; RoboJailBench) the target is not reached. The harvester '
                   'recorded the 0% in a note only.'},
    {'id': 'r4x:2', 'bottleneck': 'r4-B1', 'role': 'x', 'refutes': 'r4-B1', 'contrary': False, 'shows_target_reached': False,
     'source': 'Yeke, Zhou, Lin, Cai, Bianchi & Celik, RoboJailBench (Table 4, Robo2VLM rows; defence effectiveness paragraph)',
     'version': 'arXiv v1, 19 May 2026 (the only version); re-fetched PDF byte-identical to the harvester\'s copy',
     'url': 'https://arxiv.org/abs/2605.19328v1',
     'quote': ['Google Prompt 8.00±2.71 0.00±0.00 0.00±0.00 12.00±3.25 95.00±1.09 100.00±0.00 97.44±0.57',
               'Google Defense Prompt improves security rate on most datasets while preserving a high utility rate, yielding the '
               'best SU-HM on DROID (94.60%), Robo2VLM (97.44%), and RH20T (67.52%).'],
     'raw_file': R + '2605.19328v1.txt',
     'agent_note': 'Re-check of the harvester\'s B-c. On the same independent benchmark the best security rate is not 65.00 '
                   '(RJB-Instructions, RoboGuard) but 95.00 at utility 100.00 (Robo2VLM, Google defence prompt; ASR CD 8, CJ 0, '
                   'SM 0, RoboPAIR 12), a gap of 5.0 points to SR 100, not 35.0; DROID reaches 89.75. Across the six datasets '
                   'the best defence leaves a gap of 5.0 (Robo2VLM) to 51.25 (RoboVQA, SR 48.75) points. The benchmark does not '
                   'show the target reached anywhere, so the bottleneck stays open; the harvester\'s single "best" is one '
                   'dataset\'s value, not the best.'},
    {'id': 'r4x:3', 'bottleneck': 'r4-B1', 'role': 'x', 'refutes': 'r4-B1', 'contrary': True, 'shows_target_reached': False,
     'source': 'Huang, V B, Chen, Bryson, Chaffey, Chen, Choo & Manchester, Trust in LLM-controlled Robotics: a Survey of Security '
               'Threats, Defenses and Challenges (Sections V-C and V-D)',
     'version': 'arXiv v1, 17 Dec 2025 (the only version)', 'url': 'https://arxiv.org/abs/2601.02377v1',
     'quote': ['This provides a final safety layer even if high-level planning is flawed or disturbed by environmental factors.',
               'control-theoretic safeguards like Control Barrier Functions (CBFs) [100] ensure stability during execution but '
               'operate independently of the LLM’s high-level reasoning, leaving a gap between logical policy validation and '
               'physical actuation.',
               'Collectively, these limitations show that today’s defenses remain siloed—effective within individual layers yet '
               'weakly integrated across perception, cognition, and control'],
     'raw_file': R + '2601.02377v1.txt',
     'agent_note': 'A partial misframing argument, fairly weighed: a low-level control layer (barrier functions) bounds physical '
                   'harm whatever the planner was talked into, so "jailbreak rate of the planner" is not the same as "harmful '
                   'physical action". The same survey says the layers are not integrated (a CBF cannot see intent such as '
                   'carrying a weapon to a person), so it supports the bottleneck as open end to end. No target reached.'},

    # ---------------- r4-B2: physical adversarial attacks on VLA policies and certified defence
    {'id': 'r4x:4', 'bottleneck': 'r4-B2', 'role': 'x', 'refutes': 'r4-B2', 'contrary': False, 'shows_target_reached': False,
     'source': 'Structure-Aware Robust Fine-Tuning (SARF): Defending Vision-Language-Action Robots Against Physical Attention '
               'Hijacking (IROS 2026), abstract and Table III (real PiPER robot)',
     'version': 'arXiv v1, 4 Aug 2026 (the only version); comment: accepted to IROS 2026',
     'url': 'https://arxiv.org/abs/2608.03231v1',
     'quote': ['On LIBERO, SARF reduces OpenVLA’s failure rate under AGSD from 100% to 14.2–56.8% (28.6% avg.) across suites '
               'while preserving clean performance, and on a real PiPER manipulator it improves average success under AGSD from '
               '23.0% to 65.0%.',
               'For each task, we run 100 physical trials with randomized initial object poses and randomized trial order.',
               'Average 72.0 23.0 40.7 65.0',
               'whereas SARF restores manipulation much more effectively under the same printed patch, achieving 65.0% average '
               'success (a 42.0-point gain over the attacked Original)'],
     'raw_file': R + '2608.03231v1.txt',
     'agent_note': 'Re-check of the harvester\'s B-c (a closer result, not the target, not a deployed system, not a misframing '
                   'argument). A stronger real-robot defence than the harvester\'s "best" (CertVLA: defended 60% against clean '
                   '90%, 10 trials). SARF on a real PiPER arm, three tasks x 100 trials per condition: clean 72.0%, attacked 23.0%, '
                   'defended 65.0%, i.e. 7.0 points below clean (85.7% of the attack-induced loss recovered), against the '
                   'harvester\'s 30 points. Not the target: 7 points remain, the real-robot patch is the same printed patch '
                   'optimised against the undefended policy (the adaptive, re-optimised patch was run only in simulation), and '
                   'SARF is empirical (no certificate). Columns: Clean (Original), then under attack Original, AF, SARF.'},
    {'id': 'r4x:5', 'bottleneck': 'r4-B2', 'role': 'x', 'refutes': 'r4-B2', 'contrary': False, 'shows_target_reached': False,
     'source': 'SARF (IROS 2026), Section IV-C items 5 and 6 (adaptive attacker; clean performance) and Conclusion',
     'version': 'arXiv v1, 4 Aug 2026', 'url': 'https://arxiv.org/abs/2608.03231v1',
     'quote': ['AGSD results for SARF are obtained using an adaptive setting where the patch is re-optimized against the frozen '
               'SARF-tuned model using the same AGSD objective and EOT settings.',
               'on clean inputs, FR changes only marginally from 14.2/11.6/20.8/46.2% (Original) to 14.4/11.8/21.0/46.6% (SARF) '
               'across suites (average 23.2% to 23.5%).',
               'validate the defense across broader VLA backbones, embodiments, and third-party adaptive attacks.'],
     'raw_file': R + '2608.03231v1.txt',
     'agent_note': 'In simulation, under an adaptive (re-optimised) patch, the defended failure rate averages 28.6% against 23.5% '
                   'clean: 5.1 points from the attack-free oracle (Spatial 17.0 vs 14.4, Object 14.2 vs 11.8). Close to the '
                   'target in simulation, not at it; third-party adaptive attacks are future work by the authors\' own account.'},
    {'id': 'r4x:6', 'bottleneck': 'r4-B2', 'role': 'x', 'refutes': 'r4-B2', 'contrary': False, 'shows_target_reached': False,
     'source': 'Lu et al., CertVLA (Table 1 and Main Results, simulation)',
     'version': 'arXiv v1, 21 Aug 2026 (the only version); re-fetched PDF byte-identical to the harvester\'s copy',
     'url': 'https://arxiv.org/abs/2608.20791v1',
     'quote': ['OpenVLA-OFT 98 98 94 94 98 98 86 86 94.00 94.00',
               'In Tab. 1, OpenVLA-OFT obtains 94% average Defense and Certified success'],
     'raw_file': R + '2608.20791v1.txt',
     'agent_note': 'Certified success under the physical patch attack on LIBERO: 94.00 average for OpenVLA-OFT (columns: Defense, '
                   'Certified per suite Spatial, Object, Goal, Long, then Average). CertVLA prints no clean rate for this table; '
                   'OpenVLA-OFT\'s own paper reports 97.1% clean on the same four suites (r4x:7), so the certified rate is about '
                   '3.1 points below clean in simulation (cross-source, an estimate). The harvester said the gap "is mainly '
                   'physical" without the clean number; this quantifies it. Not the target on a real robot.'},
    {'id': 'r4x:7', 'bottleneck': 'r4-B2', 'role': 'x', 'refutes': 'r4-B2', 'contrary': False, 'shows_target_reached': False,
     'source': 'Kim, Finn & Liang, Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success (OpenVLA-OFT; RSS 2025), '
               'abstract',
     'version': 'arXiv v2, 28 Apr 2025 (v1 27 Feb 2025)', 'url': 'https://arxiv.org/abs/2502.19645v2',
     'quote': ['significantly boosting OpenVLA’s average success rate across four task suites from 76.5% to 97.1%'],
     'raw_file': R + '2502.19645v2.txt',
     'agent_note': 'The clean (attack-free) reference for r4x:6: 97.1% average on the four LIBERO suites. Cross-source; CertVLA '
                   'fine-tunes and evaluates under its own protocol, so the 3.1-point reading is approximate.'},

    # ---------------- r4-B3: runtime failure detection for generalist learned policies
    {'id': 'r4x:8', 'bottleneck': 'r4-B3', 'role': 'x', 'refutes': 'r4-B3', 'contrary': False, 'shows_target_reached': False,
     'source': 'Park, Li, Oh, Yeh, Kira, Hagenow & Li, Hide-and-Seek in Trajectories (NeurIPS 2026), Table 1, pi0 on LIBERO-10',
     'version': 'arXiv v2, 25 Sep 2026 (v1 29 May 2026); re-fetched PDF byte-identical to the harvester\'s copy',
     'url': 'https://arxiv.org/abs/2605.30834v2',
     'quote': ['Policy: π0 (Success Rate: 84.2%)',
               'Ours 0.885±0.041 0.926±0.054 0.693±0.021 0.892±0.011 0.921±0.044 0.705±0.043'],
     'raw_file': R + '2605.30834v2.txt',
     'agent_note': 'Re-check of the harvester\'s B-c: the same table, same benchmark (LIBERO-10, unseen tasks), reports a higher '
                   'best than the OpenVLA row the harvester used. With pi0 the detector reaches bACC 0.892 and TWA 0.705 on '
                   'unseen tasks (columns: seen bACC, wACC, TWA, then unseen bACC, wACC, TWA), so the gap to a perfect detector '
                   'is 0.108 bACC / 0.295 TWA, not 0.166 / 0.337. Detection quality depends on the monitored policy (pi0 84.2% '
                   'success vs OpenVLA 51.0%).'},
    {'id': 'r4x:9', 'bottleneck': 'r4-B3', 'role': 'x', 'refutes': 'r4-B3', 'contrary': False, 'shows_target_reached': False,
     'source': 'Hide-and-Seek (NeurIPS 2026), Table 3 and Section 5.2 (real UFactory xArm 6, pi0.5) and Appendix E.2',
     'version': 'arXiv v2, 25 Sep 2026', 'url': 'https://arxiv.org/abs/2605.30834v2',
     'quote': ['CUBE (Success Rate: 61.2%) KITCHEN (Success Rate: 63.7%)',
               'Ours 0.966 0.852 0.914 0.800 0.968 0.863 0.972 0.876',
               'e.g., SAFE-MLP achieves 99.2% bACC on seen CUBE but drops to 79.7% on unseen.',
               'we designate 3 tasks as seen and 1 task as unseen for evaluating generalization.'],
     'raw_file': R + '2605.30834v2.txt',
     'agent_note': 'On a real robot the runtime monitor reaches bACC 0.972 and TWA 0.876 on the unseen KITCHEN task and 0.914 / '
                   '0.800 on the unseen CUBE task (column order fixed by the text: SAFE-MLP 0.992 seen, 0.797 unseen on CUBE; '
                   'per category seen bACC, seen TWA, unseen bACC, unseen TWA). Within 0.028 bACC of a perfect detector on one '
                   'unseen real task. Not the target: one unseen task per category (about 40 trajectories each), TWA still '
                   '0.124 short (late alarms), and the perfect detector is a definitional oracle rather than a stated goal. A '
                   're-check (the harvester\'s best understated), not contrary evidence.'},
    {'id': 'r4x:10', 'bottleneck': 'r4-B3', 'role': 'x', 'refutes': 'r4-B3', 'contrary': False, 'shows_target_reached': False,
     'source': 'NVIDIA (company technical blog), Inside NVIDIA Halos for Robotics: A Full-Stack Functional Safety System for '
               'Physical AI (Sheshadri, Mariani, Ochoa, Rodge & Todd)',
     'version': 'published 22 Jun 2026, modified 6 Aug 2026 (page metadata)',
     'url': 'https://developer.nvidia.com/blog/inside-nvidia-halos-for-robotics-a-full-stack-functional-safety-system-for-physical-ai/',
     'quote': ['The SAIM generates an alert that propagates through the safety chain, causing the Safety Decision Maker to fall '
               'back to a safe operating state—reactivating the robot’s onboard safety functions—until conditions recover.',
               'Runs a finite state machine on IGX’s dedicated Functional Safety Island—isolated from the main AI compute '
               'domain—'],
     'raw_file': R + 'nvidia_dev_halos_robotics.txt',
     'agent_note': 'Context, not contrary evidence: an industry safety blueprint does not predict task failure of the learned '
                   'policy; it monitors the perception input for out-of-distribution conditions and falls back to onboard '
                   'safety functions run on an isolated safety island. The source does not argue that task-failure detection is '
                   'misframed, it is a platform blueprint rather than a reported deployment of this monitor, and it reports no '
                   'detection rate. It serves the "stop or ask for help" purpose by a different signal.'},

    # ---------------- r4-B4: emergency stop of dynamically balancing robots; the standards gap
    {'id': 'r4x:11', 'bottleneck': 'r4-B4', 'role': 'x', 'refutes': 'r4-B4', 'contrary': True, 'shows_target_reached': False,
     'source': 'Agility Robotics (company statement), Agility Robotics Announces New Innovations for Market-Leading Humanoid Robot '
               'Digit',
     'version': 'published 31 Mar 2025 (page date; fetched 2026-09-30)',
     'url': 'https://www.agilityrobotics.com/content/agility-robotics-announces-new-innovations-for-market-leading-humanoid-robot-digit',
     'quote': ['A Category 1, or CAT1 stop, involves maintaining power to the machine actuators during the deceleration process, '
               'allowing the machine to stop smoothly and safely, before removing power.',
               'Safety PLC, also known as a safety programmable logic controller, is used on robots to provide safety functions '
               'that meet performance level d (PLd).',
               'Standards exist for machine and robot safety, but safety standards for Dynamically Stable Industrial Mobile '
               'Robots such as Digit that require stability and balancing are in the development stage.'],
     'raw_file': R + 'agility_digit_innovations.txt',
     'agent_note': 'A deployed humanoid with a Category 1 stop (controlled deceleration before power removal) and a safety PLC '
                   'whose safety functions meet PL d. This contests "classical emergency stops remove power" as a description of '
                   'the field: a controlled stop exists in product. It does not show the target: PL d is claimed for the '
                   'PLC\'s safety functions, not for the balancing reaction chain, which is the Siemens paper\'s point; the '
                   'reference target is PL e; and Agility itself says the humanoid standards are in development.'},
    {'id': 'r4x:12', 'bottleneck': 'r4-B4', 'role': 'x', 'refutes': 'r4-B4', 'contrary': True, 'shows_target_reached': False,
     'source': 'Agility Robotics (company statement), Beyond the Hype (Digit passes OSHA-recognized safety field inspection)',
     'version': 'published 24 Nov 2025 (page date)', 'url': 'https://www.agilityrobotics.com/content/beyond-the-hype',
     'quote': ['Digit passes NRTL (Nationally Recognized Test Lab) field testing, a significant milestone that further accelerates '
               'Digit as the industry’s first commercially scalable humanoid in industrial settings.',
               'While NRTL field evaluations are site-specific, passing this assessment proves that Digit is ready for real-world '
               'applications and that we\'ve established a repeatable process for building compliant, safe robots.'],
     'raw_file': R + 'agility_beyond_the_hype.txt',
     'agent_note': 'An independent (NRTL) evaluation passed by a balancing humanoid at a customer site: a deployed system cleared '
                   'for work. Company statement; the NRTL, the standards applied and any PL/PFHD figure are not named, and the '
                   'evaluation is site-specific by the company\'s own account. Not the certified end-to-end PL e chain.'},
    {'id': 'r4x:13', 'bottleneck': 'r4-B4', 'role': 'x', 'refutes': 'r4-B4', 'contrary': True, 'shows_target_reached': False,
     'source': 'Agility Robotics (company press release), Agility Unveils Digit 5 Humanoid Robot Built for Cooperatively Safe Work '
               'at Scale',
     'version': 'published 15 Sep 2026 (page date)',
     'url': 'https://www.agilityrobotics.com/content/agility-unveils-digit-5-humanoid-robot-built-for-cooperatively-safe-work-at-scale',
     'quote': ['Building on the milestone of becoming the first humanoid to pass an independent field evaluation on a customer '
               'production line for industrial safety standards administered by the U.S. Occupational Safety and Health '
               'Administration (OSHA), Digit 5 adds:',
               'Uses proprietary AI algorithms and multiple sensor technologies to continuously monitor for people and take '
               'appropriate action by autonomously avoiding, stopping or assuming a seated position.',
               'An independent safety controller oversees Digit’s response to the detection of people within an unsafe distance '
               'and instantly triggers the appropriate safety responses.',
               'ISO 25785-1, the first international safety standard for the humanoid category.'],
     'raw_file': R + 'agility_digit5.txt',
     'agent_note': 'The strongest contrary evidence found for r4-B4: a commercial humanoid engineered to work near people without '
                   'fences, whose safe state is an actively reached one (stop or sit) triggered by an independent safety '
                   'controller. It is a product claim, not a rating: no PL, PFHD or certificate is stated, and ISO 25785-1 is '
                   'still named as a standard in development. The categorical gap the harvester recorded stands; the "no '
                   'deployed controlled stop" reading does not.'},
    {'id': 'r4x:14', 'bottleneck': 'r4-B4', 'role': 'x', 'refutes': 'r4-B4', 'contrary': False, 'shows_target_reached': False,
     'source': 'NVIDIA (company technical blog), Inside NVIDIA Halos for Robotics (Halos AI Systems Inspection Lab section)',
     'version': 'published 22 Jun 2026, modified 6 Aug 2026',
     'url': 'https://developer.nvidia.com/blog/inside-nvidia-halos-for-robotics-a-full-stack-functional-safety-system-for-physical-ai/',
     'quote': ['Agility is using the Lab to inspect how the Digit safety-related software, AI components, and cybersecurity '
               'protections meet rigorous standards including IEC 61508, ISO 13849, and ISO/IEC TR 5469 before final '
               'third-party certification.'],
     'raw_file': R + 'nvidia_dev_halos_robotics.txt',
     'agent_note': 'Confirms, from the platform vendor, that the leading deployed humanoid had not reached final third-party '
                   'functional-safety certification as of mid-2026. Supports the harvester\'s reading (the gap is open); recorded '
                   'as a re-check, not contrary evidence.'},

    # ---------------- r4-B5: formal verification of neural controllers at deployed scale
    {'id': 'r4x:15', 'bottleneck': 'r4-B5', 'role': 'x', 'refutes': 'r4-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'Corsi, Kim & Fox (UC Irvine), Verifiable Foundation Models for Robot Safety (FEARL)',
     'version': 'arXiv v1, 22 Jun 2026 (the only version)', 'url': 'https://arxiv.org/abs/2606.23754v1',
     'quote': ['formal verification can be applied to S rather than to the full foundation-model backbone.',
               'In our implementation, it is a two-layer MLP with 32 units per layer',
               'verification-guided shielding achieves zero safety violations across all environments, while maintaining low '
               'override rates and small performance drops.',
               'Despite these advances, all existing verifiers remain tractable only for relatively small networks, far below '
               'the scale of any modern foundation model.'],
     'raw_file': R + '2606.23754v1.txt',
     'agent_note': 'A misframing argument with a result: the target "verify the 7B policy" is not what a safety case needs; route '
                   'the final action through a small verifiable safety module (two layers of 32 units, inside the size today\'s '
                   'verifiers handle) and verify that. Zero safety violations with shielding, in three simulated domains plus a '
                   'Stretch transfer. It also confirms the harvester\'s size gap for verifying the backbone itself. The target '
                   '(verification at deployed policy scale) is not reached; the argument is that it need not be.'},
    {'id': 'r4x:16', 'bottleneck': 'r4-B5', 'role': 'x', 'refutes': 'r4-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'Lu et al., CertVLA (abstract)',
     'version': 'arXiv v1, 21 Aug 2026; re-fetched PDF byte-identical to the harvester\'s copy',
     'url': 'https://arxiv.org/abs/2608.20791v1',
     'quote': ['we prove that against any adaptive attacker satisfying the bounded-support threat model, every rollout certified by '
               'CertVLA executes only action chunks consistent with attack-erased clean predictions.',
               'Conjoining query-level decisions extends the action certificate to the complete closed-loop rollout.'],
     'raw_file': R + '2608.20791v1.txt',
     'agent_note': 'The harvester used this paper only for the target size ("OpenVLA provides an open 7B policy"). The same paper '
                   'proves a closed-loop certificate for 7B-scale VLA policies (94.00 certified success for OpenVLA-OFT on LIBERO, '
                   'r4x:6). The property is narrow (consistency under bounded patches, with a calibrated clean region), not a '
                   'reachability or safety specification over the dynamics as in ARCH-COMP, so the target is not reached; but '
                   '"six orders of magnitude" overstates the gap for certificates of some closed-loop property at deployed scale.'},
    {'id': 'r4x:17', 'bottleneck': 'r4-B5', 'role': 'x', 'refutes': 'r4-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'NNV3: Expanding Neural Network Verification to New Architectures and Domains (Section on probabilistic verification)',
     'version': 'arXiv v1, 24 Sep 2026 (the only version)', 'url': 'https://arxiv.org/abs/2609.30050v1',
     'quote': ['This approach scales with inference cost and is independent of network architecture, providing probabilistic '
               'coverage guarantees for models that are beyond the practical reach of exact methods.',
               'The evaluation therefore serves as a feasibility demonstration on a perception-scale model rather than a '
               'scalability study.'],
     'raw_file': R + '2609.30050v1.txt',
     'agent_note': 'A reframing of the metric: probabilistic (conformal) verification scales with inference cost, not network size, '
                   'so the size gap is a property of exact methods. Demonstrated only on TinyYOLO, by the authors\' account a '
                   'feasibility demonstration, and the guarantee is a coverage statement, not a sound over-approximation. Not the '
                   'target.'},
    {'id': 'r4x:18', 'bottleneck': 'r4-B5', 'role': 'x', 'refutes': 'r4-B5', 'contrary': False, 'shows_target_reached': False,
     'source': 'NVIDIA (company technical blog), Inside NVIDIA Halos for Robotics (IGX Thor platform)',
     'version': 'published 22 Jun 2026, modified 6 Aug 2026',
     'url': 'https://developer.nvidia.com/blog/inside-nvidia-halos-for-robotics-a-full-stack-functional-safety-system-for-physical-ai/',
     'quote': ['IEC 61508 SIL 3 capable Safety Island (FSI)'],
     'raw_file': R + 'nvidia_dev_halos_robotics.txt',
     'agent_note': 'Context corroborating FEARL\'s framing (r4x:15), recorded as a re-check rather than contrary evidence because '
                   'the source does not itself argue the point: the element built to a safety-integrity level is a small '
                   'isolated safety island, with the neural policy outside the certified boundary. Not evidence that the policy '
                   'is verified.'},

    # ---------------- r4-B6: cybersecurity of commercial robots and fleets
    {'id': 'r4x:19', 'bottleneck': 'r4-B6', 'role': 'x', 'refutes': 'r4-B6', 'contrary': True, 'shows_target_reached': False,
     'source': 'KUKA (company press release), KUKA Takes Security to a New Level: KUKA first in robotics to achieve Security Level 2 '
               'certification in accordance with IEC 62443-4-2',
     'version': 'published 21 Jul 2026 (page date)',
     'url': 'https://www.kuka.com/en-de/company/press/news/2026/07/os-reaches-product-security-level-2',
     'quote': ['the robot system has been certified to Security Level 2 according to IEC 62443-4-2 and already meets the '
               'requirements of Regulation (EU) 2024/2847 Cyber Resilience.',
               'KUKA was the first robotics manufacturer to achieve certification for Security Level 2 in accordance with IEC '
               '62443-4-2'],
     'raw_file': R + 'kuka_iec62443_sl2.txt',
     'agent_note': 'A deployed industrial robot system (iiQKA.OS2 on KR C5) certified to a component-security standard and claimed '
                   'by its maker to meet the CRA, the harvester\'s named target. It does not show the target on the named metric: '
                   'the claim is the manufacturer\'s, the certifier is not named in the release, SL2 is protection against '
                   'attackers "with limited resources" by the standard\'s own ladder, and no automated assessment of the product '
                   'was published; SL2 in IEC 62443 addresses intentional attacks with simple means and low resources, not a '
                   'sophisticated attacker. It does show the bottleneck is sector-specific: the harvester\'s evidence is consumer '
                   'robots and one humanoid.'},
    {'id': 'r4x:20', 'bottleneck': 'r4-B6', 'role': 'x', 'refutes': 'r4-B6', 'contrary': True, 'shows_target_reached': False,
     'source': 'TUV Rheinland (third-party certifier, press release), Roborock\'s Newly Launched Robot Vacuum Cleaners Receive TUV '
               'Rheinland ETSI EN 303 645 Certifications',
     'version': 'published 10 Jan 2024 (Las Vegas, CES); older than the 2025-26 window, recorded because it is a third-party '
               'certification of a consumer robot',
     'url': 'https://www.tuv.com/press/en/press-releases/roborock-newly-launched-robot-vacuum-cleaners-receive-tuv-rheinland-certifications.html',
     'quote': ['TÜV Rheinland evaluated the four robot vacuum cleaners based on the network security regulations and privacy '
               'protection requirements of the ETSI EN 303 645 standard, through design evaluation audits and security '
               'verification.'],
     'raw_file': R + 'tuv_roborock_etsi303645.txt',
     'agent_note': 'Mass-market consumer robots with an independent consumer-IoT security and privacy certification (ETSI EN 303 '
                   '645, which among other things forbids universal default passwords). Contests the harvester\'s generalisation '
                   'from three niche consumer robots to "commercial robots ship with exploitable vulnerabilities". EN 303 645 is '
                   'a baseline, not a finding of zero vulnerabilities, and no automated assessment of these models was found.'},
    {'id': 'r4x:21', 'bottleneck': 'r4-B6', 'role': 'x', 'refutes': 'r4-B6', 'contrary': False, 'shows_target_reached': False,
     'source': 'NIST National Vulnerability Database, CVE-2025-35027 and CVE-2025-60251 (Unitree Go2, G1, H1, B2)',
     'version': 'CVE-2025-35027 published 26 Sep 2025, last modified 17 Jun 2026, status Analyzed (CNA takeonme.org); '
                'CVE-2025-60251 published 26 Sep 2025, last modified 17 Jun 2026, status Deferred (CNA MITRE)',
     'url': 'https://nvd.nist.gov/vuln/detail/CVE-2025-35027',
     'quote': ['Multiple robotic products by Unitree sharing a common firmware, including the Go2, G1, H1, and B2 devices, contain a '
               'command injection vulnerability.',
               'Unitree Go2, G1, H1, and B2 devices through 2025-09-20 accept any handshake secret with the unitree substring.'],
     'raw_file': R + 'nvd_CVE-2025-35027_and_60251.txt',
     'agent_note': 'Re-check of the harvester\'s "vendor-authored evidence, no independent replication": the fleet-wide BLE flaws '
                   'are in the public CVE record and NIST has analysed CVE-2025-35027, but the discoverers are the harvester\'s '
                   'own G1 co-authors (r4x:29), so this is an independent registration, not an independent replication. The '
                   'harvester\'s statement stands. Supports the bottleneck; not contrary evidence.'},
    {'id': 'r4x:29', 'bottleneck': 'r4-B6', 'role': 'x', 'refutes': 'r4-B6', 'contrary': False, 'shows_target_reached': False,
     'source': 'Makris (Bin4ry) & Finisterre (h0stile), UniPwn: Unitree Robot BLE Service Command Injection Analysis (GitHub '
               'README, researchers\' own disclosure)',
     'version': 'README dated September 20, 2025 (raw file from the main branch, fetched 2026-09-30)',
     'url': 'https://github.com/Bin4ry/UniPwn',
     'quote': ['**Author:** Bin4ry aka Andreas Makris',
               '**Co-Author:** h0stile aka Kevin Finisterre',
               '[CVE-2025-35027](https://takeonme.org/cves/cve-2025-35027/)',
               'Authors: *Víctor Mayoral-Vilches, Andreas Makris, Kevin Finisterre*',
               'Given Unitree\'s lack of response and apparent disinterest in security issues, **Andreas Makris has decided to '
               'discontinue private disclosure attempts with Unitree for future vulnerabilities**.'],
     'raw_file': R + 'github_UniPwn_README.md',
     'agent_note': 'Establishes that the CVE discoverers co-authored the harvester\'s r4:47 paper, so r4x:21 is not independent '
                   'corroboration. The disclosure record (researchers\' account, one side) reports no vendor engagement, which '
                   'bears on the CRA target of vulnerabilities "handled effectively". Supports the bottleneck.'},
    {'id': 'r4x:22', 'bottleneck': 'r4-B6', 'role': 'x', 'refutes': 'r4-B6', 'contrary': False, 'shows_target_reached': False,
     'source': 'The Hacker News (trade press), Two Unitree G1 EDU Humanoid Robot Flaws Enable Root RCE',
     'version': 'published Aug 2026 (disclosure dated 27 Aug 2026 in the article; page updated with a correction note)',
     'url': 'https://thehackernews.com/2026/08/two-unitree-g1-edu-humanoid-robot-flaws.html',
     'quote': ['Laflamme said Unitree patched the cloud account-to-robot ownership check in July 2026, closing the cross-owner '
               'arbitrary-G1 path.',
               'An exact fixed firmware release has not been verified in any accessible Unitree guidance, leaving G1 EDU owners '
               'without a confirmed release target for either vulnerability.'],
     'raw_file': R + 'thn_unitree_g1_edu_2026-08.txt',
     'agent_note': 'Trade press relaying a researcher who co-authored the harvester\'s Alias paper, so not independent of it. Shows '
                   'partial vendor remediation (a cloud-side fix in July 2026) and, a year after the first disclosures, no '
                   'verified firmware fix for two new root-RCE chains. Supports the bottleneck against the CRA\'s "handled '
                   'effectively" target.'},

    # ---------------- r4-B7: privacy of robots' sensor data and physical-world privacy awareness
    {'id': 'r4x:23', 'bottleneck': 'r4-B7', 'role': 'x', 'refutes': 'r4-B7', 'contrary': False, 'shows_target_reached': False,
     'source': 'Shen, Li & Li, EAPrivacy (ICLR 2026), Table 1 and Tier 3 text',
     'version': 'arXiv v3, 15 Feb 2026 (v1 27 Sep 2025); re-fetched PDF byte-identical to the harvester\'s copy',
     'url': 'https://arxiv.org/abs/2510.02356v3',
     'quote': ['Selection Accuracy ↑ 0.62 0.83 0.94 0.89 0.91 0.60 0.98 1.00 0.49 0.66 0.86',
               'Selection accuracy varies more widely, with gpt-5-high achieving the highest accuracy rate of 100% while others '
               'lag behind.',
               'Critically, the task completeness results are exceptionally low (often near 0%)'],
     'raw_file': R + '2510.02356v3.txt',
     'agent_note': 'On the same Tier 3 scenarios, when asked to choose among candidate plans rather than write one, gpt-5-high '
                   'picks the privacy-respecting plan in 100% of cases (Tier 3 selection accuracy row; also 1.00 in Tier 4 '
                   'selection). The harvester reported only the generative violation rate (best 71%). The target on the '
                   'harvester\'s named metric (0% violations while completing the task) is not reached; the gap is between '
                   'recognising the right plan and generating it. A fair B-c reports both; recorded as a re-check of an omission, '
                   'not as contrary evidence, since selection is not the named metric. Note the paper\'s text names "4o" '
                   'among the 71% models, but the table\'s 0.71 is 2.5-flash-w.o.think only.'},
    {'id': 'r4x:24', 'bottleneck': 'r4-B7', 'role': 'x', 'refutes': 'r4-B7', 'contrary': False, 'shows_target_reached': False,
     'source': 'Wang, Shen, Jin & Li (Georgia Tech), How Far Are VLMs from Privacy Awareness in the Physical World? An Empirical '
               'Study (IMMERSEDPRIVACY)',
     'version': 'arXiv v2, 8 May 2026 (v1 6 May 2026)', 'url': 'https://arxiv.org/abs/2605.05340v2',
     'quote': ['When social context shifts, no model exceed 65% selection accuracy. Under conflicting commands, the best model '
               'gemini-3.1-pro perfectly balances task completion and privacy preservation in only 51% of cases.'],
     'raw_file': R + '2605.05340v2.txt',
     'agent_note': 'A newer benchmark from the same group (audio-visual, 12 models including gemini-3.1-pro): the best model '
                   'completes the task and respects privacy together in 51% of conflict cases, against near-zero task '
                   'completion in EAPrivacy Tier 3. Updates the harvester\'s B-c with a 2026 number; still 49 points from the '
                   'target, so the bottleneck stays open.'},
    {'id': 'r4x:25', 'bottleneck': 'r4-B7', 'role': 'x', 'refutes': 'r4-B7', 'contrary': True, 'shows_target_reached': False,
     'source': 'Roborock (company statement), Trust Center - Your Privacy, Our Top Priority',
     'version': 'page states "Last updated: August 2026"', 'url': 'https://global.roborock.com/pages/roborock-trust-center',
     'quote': ['Last updated: August 2026.',
               'Nothing is collected or uploaded without your explicit permission or as otherwise provided by laws.',
               'IoT Security & Data Privacy Certified (EN 303 645)',
               'Withdrawing permission automatically deletes all photos, keeping you in full control.'],
     'raw_file': R + 'roborock_trust_center.txt',
     'agent_note': 'A mass-market camera-equipped consumer robot line claiming consent before collection, local encrypted storage, '
                   'deletion on withdrawal and a third-party privacy certification (r4x:20). Contests the harvester\'s "deployed '
                   'consumer robots stream sensor telemetry without consent or data-subject rights", which rests on three niche '
                   'products and one humanoid. Company claims, not an audit on the harvester\'s metric (GDPR endpoints probed).'},
    {'id': 'r4x:26', 'bottleneck': 'r4-B7', 'role': 'x', 'refutes': 'r4-B7', 'contrary': True, 'shows_target_reached': False,
     'source': 'Agility Robotics (company press release), Agility Unveils Digit 5 (Data Privacy and Security section)',
     'version': 'published 15 Sep 2026',
     'url': 'https://www.agilityrobotics.com/content/agility-unveils-digit-5-humanoid-robot-built-for-cooperatively-safe-work-at-scale',
     'quote': ['Agility protects Digit’s platform with end-to-end encryption, strict access controls and localized data processing.',
               'processing sensory data locally and transmitting essential system health and diagnostic information to Agility '
               'Arc.'],
     'raw_file': R + 'agility_digit5.txt',
     'agent_note': 'A deployed industrial humanoid whose maker states that sensor data are processed on the robot and only health '
                   'and diagnostic data leave it: the opposite of the Unitree G1 telemetry pattern. Company claim; unaudited.'},

    # ---------------- r4-B8: collaborative throughput lost to safety speed reduction
    {'id': 'r4x:27', 'bottleneck': 'r4-B8', 'role': 'x', 'refutes': 'r4-B8', 'contrary': False, 'shows_target_reached': False,
     'source': 'Parma, Tonola, Pedrocchi & Beschi, Embedding ISO 10218 Safety Compliance in Robots via Control Barrier Functions for '
               'Human-Robot Collaboration (Table III and text)',
     'version': 'arXiv v1, 11 Jun 2026 (the only version)', 'url': 'https://arxiv.org/abs/2606.13203v1',
     'quote': ['continuous 15,000-second simulation runs were conducted.',
               'all algorithms processed the same pre-recorded human dataset and followed identical continuous pick-and-place '
               'trajectories.',
               'It maintains a high throughput of 789 laps while successfully reaching 92.91% of the designated waypoints. '
               'Crucially, it records a mean scaling factor of 0.81, vastly outperforming the external module (0.15)'],
     'raw_file': R + '2606.13203v1.txt',
     'agent_note': 'A 2026 predictive-CBF controller on a UR10e model keeps a mean speed scaling of 0.81 against 0.15 for a '
                   'standard SSM module, above the harvester\'s best 0.74 (a different protocol: simulation replaying recorded '
                   'human motion, not a live cell). 19% of nominal speed is still lost and only 92.91% of waypoints are reached, '
                   'so the oracle s = 1 is not reached. Real-world runs report tracking error, not scaling. A re-check of B-c '
                   '(a higher number on another protocol), not contrary evidence.'},
    {'id': 'r4x:28', 'bottleneck': 'r4-B8', 'role': 'x', 'refutes': 'r4-B8', 'contrary': False, 'shows_target_reached': False,
     'source': 'Reactive and Safety-Aware Path Replanning for Collaborative Applications (MARSHA), abstract and experimental setup',
     'version': 'arXiv v2, 11 Jun 2025 (v1 10 Mar 2025); comment: submitted to IEEE', 'url': 'https://arxiv.org/abs/2503.07192v2',
     'quote': ['This solution reduces the execution time and the need for trajectory slowdowns without sacrificing safety.',
               'with efficiency enhancements of up to 60%.',
               'we limit the robot’s speed to 30% of its maximum for safety reasons.'],
     'raw_file': R + '2503.07192v2.txt',
     'agent_note': 'Safety-aware replanning cuts execution time by up to 60% against speed-and-separation monitoring. The numbers '
                   'against the no-human time are in figures only, and the real cell was run at 30% of maximum speed, so the '
                   'result does not show the nominal speed reached. Progress in the frontier\'s direction; a re-check, not '
                   'contrary evidence.'},
]

CHECKS = [
    {'bottleneck': 'r4-B1',
     'searched': ['WebSearch: 2026 defense LLM robot jailbreak attack success rate 0% embodied agent safety benchmark BadRobot defense',
                  'WebSearch: RoboJailBench defense results 2026 security rate utility',
                  'WebSearch: arXiv 2026 LLM robot planner jailbreak defense near-zero attack success rate adaptive attacks embodied '
                  'safety guard',
                  'WebSearch: defense embodied AI jailbreak BadRobot ... RoboSafe OR "Concept Enhancement Engineering" OR SafeMind',
                  'WebSearch: "Trust in LLM-controlled Robotics" survey security threats defenses challenges 2026',
                  'arXiv 2601.02377v1 (Trust in LLM-controlled Robotics survey); arXiv 2504.13201v3 (CEE, inference-time defence; '
                  'screened: DSR tables in mixed layout, no result at SR 100 with full usability was extractable)',
                  'Harvester raw texts re-read in full: RoboGuard v2 Tables I and IV; RoboJailBench v1 Table 4 (all six datasets); '
                  'AuthGuard-R live evaluation (Tables V-VI)'],
     'finding': 'CONTESTED at most, not NOT OPEN. On a small physical-robot set RoboGuard reached the stated target literally (RoboPAIR '
                '100% -> 0% attack success, utility 100%), but on 35 behaviours with non-adaptive attacks only; under adaptive '
                'attack on the authors\' larger suite 2.5-5.2% still succeed. On the independent RoboJailBench the best defence is '
                'SR 95.00 at UR 100 (Robo2VLM, Google prompt), not the 65.00 the harvester reported; across datasets the gap to SR '
                '100 is 5.0 to 51.25 points and conceptual deception stays at 93-100% on four datasets. AuthGuard-R blocked 23/23 '
                'unauthorised actions from Claude Haiku 4.5 (fixed and adaptive) but also accepted one unauthorised action when the '
                'mission policy was mis-encoded. A 2025 survey argues that low-level control safeguards bound physical harm '
                'whatever the planner does (a partial misframing), while stating the layers are not integrated end to end. No '
                'source shows zero adversarial success at full utility under adaptive attack on a shared benchmark.',
     'harvester_errors': ['B-c "best" on RoboJailBench: the harvester gave SR 65.00 (RJB-Instructions, RoboGuard) and a gap of 35.0 '
                          'points as the independent benchmark\'s best; the same Table 4 has SR 95.00 at UR 100.00 (Robo2VLM, Google '
                          'defence prompt) and 89.75 (DROID). The gap on the named benchmark ranges 5.0-51.25 points by dataset; '
                          '35.0 is one dataset\'s value.',
                          'The real-world RoboGuard result (0% ASR at 100% utility, Table IV) is the stated target on a small, '
                          'non-adaptive protocol; the harvester mentioned it only in an agent_note, not in B-c or the BOTTLENECKS '
                          '"best" field.']},
    {'bottleneck': 'r4-B2',
     'searched': ['WebSearch: defense adversarial patch vision-language-action model 2026 robust fine-tuning recovers clean success rate '
                  'real robot',
                  'WebSearch: OpenVLA-OFT LIBERO average success rate 97.1 arXiv 2502.19645',
                  'arXiv 2608.03231v1 (SARF, IROS 2026); arXiv 2502.19645v2 (OpenVLA-OFT); CertVLA 2608.20791v1 re-read (Table 1)',
                  'Screened by title/snippet only: arXiv 2510.13237 (model-agnostic attack and defence for VLA), arXiv 2602.01158'],
     'finding': 'OPEN (no contrary claim of the declared kinds: no target reached, no deployed defence, no misframing argument '
                'found), with a much smaller gap than the harvester reported. The best empirical defence found is much closer to '
                'the attack-free oracle than the harvester\'s best: SARF on a real PiPER arm (3 tasks x 100 trials) recovers 23.0% -> 65.0% against 72.0% clean '
                '(7 points short; pick-and-place 74 vs 79), and in simulation under an adaptive re-optimised patch it averages '
                '28.6% failure against 23.5% clean. Certified defence in simulation is about 3 points below clean (CertVLA 94.00 '
                'certified for OpenVLA-OFT against 97.1% clean in the OFT paper; cross-source). On a real robot the certified rate '
                'remains 30% against 90% clean (CertVLA, 10 trials). No source reports clean-level success under physical attack '
                'on a real robot, and the real-robot SARF patch was not re-optimised against the defended model.',
     'harvester_errors': ['B-c "best" understated: the harvester called CertVLA (real robot: defended 60% vs clean 90%, 10 trials) '
                          '"the best defence found"; SARF (arXiv v1, 4 Aug 2026, IROS 2026) reports 65.0% defended vs 72.0% clean '
                          'on a real arm over 300 trials per condition, a 7-point gap rather than 30. The harvester\'s own '
                          'screening did not include it. (For the certified sub-question CertVLA remains the best found.)',
                          '"so the gap is mainly physical": stated without a clean simulation baseline; with OFT\'s 97.1% the '
                          'certified simulation gap is about 3.1 points, which supports the statement (cross-source).']},
    {'bottleneck': 'r4-B3',
     'searched': ['WebSearch: arXiv 2026 VLA failure detection unseen tasks outperforms SAFE accuracy real robot early warning',
                  'arXiv 2606.21386v1 (VLA-FAIL; per-task, unsupervised; threshold-free AUC tables, no unseen-task split) and '
                  'arXiv 2606.20754v3 (perturbation-based epistemic uncertainty; unseen object shift) fetched and screened',
                  'Hide-and-Seek v2 re-fetched (byte-identical) and read in full: Tables 1-3 and Appendix E.2',
                  'NVIDIA Halos for Robotics technical blog (industry runtime monitoring architecture)'],
     'finding': 'OPEN (no contrary claim of the declared kinds found), with a smaller gap than the harvester reported. On the '
                'harvester\'s own benchmark and table the best '
                'unseen-task result is pi0\'s bACC 0.892 / TWA 0.705 (not OpenVLA\'s 0.834 / 0.663). On a real robot the same '
                'monitor reaches bACC 0.972 / TWA 0.876 on one unseen KITCHEN task and 0.914 / 0.800 on one unseen CUBE task; '
                'these are single held-out tasks. Timeliness (TWA) remains the larger shortfall everywhere. Industry practice '
                '(an NVIDIA Halos blueprint) routes around task-failure prediction with an OOD input monitor that triggers '
                'fallback safety functions; the source does not argue misframing and reports no detection rate. The '
                'target itself (a perfect detector, bACC 1.0) is a definitional oracle, not a programme goal.',
     'harvester_errors': ['B-c "best" understated: Hide-and-Seek Table 1 gives bACC 0.892 and TWA 0.705 on unseen LIBERO-10 tasks with '
                          'pi0, higher than the OpenVLA row (0.834 / 0.663) the harvester called the best; the gap to a perfect '
                          'detector is 0.108 / 0.295, not 0.166 / 0.337.',
                          'The same paper\'s real-robot Table 3 (unseen bACC 0.914 and 0.972) was not reported in B-c.']},
    {'bottleneck': 'r4-B4',
     'searched': ['WebSearch: humanoid robot emergency stop certified safety PL d controlled stop 2026 Agility Digit functional safety '
                  'certification',
                  'WebSearch: first humanoid robot functional safety certification TUV 2026 ISO 13849 certified humanoid',
                  'WebSearch: Agility Robotics Digit cooperative safety 2026 working alongside humans without fences safety '
                  'certification announcement',
                  'WebSearch: Agility Digit "field evaluation" OSHA NRTL humanoid first pass production line 2026',
                  'WebSearch: NVIDIA Halos for Robotics safety humanoid 2026 certification functional safety IGX Thor announcement',
                  'WebSearch: ISO 25785-1 committee draft 2026 dynamically stable mobile robots status',
                  'Agility pages (31 Mar 2025, 24 Nov 2025, 15 Sep 2026); NVIDIA developer blog (22 Jun 2026); iso.org 91469 '
                  '(HTTP 403 again); investor.nvidia.com (HTTP 403); i-scoop.eu ISO 25785-1 explainer (secondary, fetched, not '
                  'quoted); heise.de and The Robot Report on Digit (press, fetched, not quoted)'],
     'finding': 'CONTESTED, not NOT OPEN. A deployed humanoid has a Category 1 controlled stop and a safety PLC with PL d safety '
                'functions (Agility, Mar 2025), passed a site-specific NRTL field evaluation (Nov 2025), and Digit 5 (Sep 2026) '
                'adds an independent safety controller that makes the robot stop or sit when a person comes too close, for '
                'fence-free work. None of these states a PL or PFHD for the balancing reaction chain, and NVIDIA (Jun 2026) states '
                'that Digit\'s safety software is being inspected "before final third-party certification". ISO 25785-1 is still '
                'in development (a search snippet of the unreachable iso.org page reads ISO/CD 25785-1 with a committee-draft '
                'consultation opened in May 2026; not verified). The categorical gap to a certified PL e chain stands.',
     'harvester_errors': []},
    {'bottleneck': 'r4-B5',
     'searched': ['WebSearch: closed-loop verification neural network controller 2026 scalable vision-based large network reachability '
                  'arXiv state of the art',
                  'WebSearch: formal verification of large learned robot policies infeasible runtime assurance simplex argue 2025 '
                  'position safety filter instead of verifying',
                  'WebSearch: VNN-COMP 2026 results summary largest network verified (no 2026 report found)',
                  'WebSearch: closed-loop reachability transformer policy verification 2026 arXiv first verification of a '
                  'vision-language-action or diffusion policy formal guarantee',
                  'arXiv 2606.23754v1 (FEARL); arXiv 2609.30050v1 (NNV3); arXiv 2608.02545v1 (probabilistic reachable-action '
                  'verification of a visuomotor flow policy; screened, a conformal radius, no network size stated in text); arXiv '
                  '2609.09250v2 (No Free Checker survey; screened, no quotable number); CertVLA re-read; VNN-COMP 2025 Table 3 '
                  're-read (VGG16 138M is the largest; alpha-beta-CROWN solved 100% of its instances)'],
     'finding': 'CONTESTED as framed. No source verifies a billion-parameter policy against a dynamics-level safety specification, '
                'and FEARL confirms that "all existing verifiers remain tractable only for relatively small networks". But three '
                'sources argue or show that the target is misframed: FEARL verifies a small safety module (2 x 32 units) through '
                'which a VLA\'s action passes, with zero violations in simulation; CertVLA proves a closed-loop certificate (patch '
                'consistency) for 7B-scale VLA policies; and NNV3 argues that probabilistic verification scales with inference '
                'cost (feasibility only). As context, NVIDIA\'s safety platform builds a small isolated safety island to SIL 3 '
                'capability, not the policy. '
                'The harvester\'s "six orders of magnitude" is correct for exact reachability of the whole policy and overstates '
                'the gap for certificates of narrower closed-loop properties at deployed scale.',
     'harvester_errors': ['The gap is framed against verifying the whole 7B policy, a target no quoted source sets; the harvester\'s '
                          'own r4:39 source (CertVLA) proves a closed-loop certificate at that scale for a narrower property. The '
                          'order-of-magnitude reading holds only for exact reachability of the full policy.']},
    {'bottleneck': 'r4-B6',
     'searched': ['WebSearch: industrial robot controller IEC 62443-4-2 certification 2025 robot cybersecurity certified',
                  'WebSearch: robot vacuum TUV privacy certification ETSI EN 303 645 cybersecurity certified 2025 Roborock Dreame',
                  'WebSearch: Unitree G1 vulnerability patched firmware update 2025 UniPwn Bluetooth fixed CVE response',
                  'KUKA press release (21 Jul 2026); TUV Rheinland release (10 Jan 2024); PR Newswire copy (fetched, not quoted); '
                  'NVD 2.0 API records CVE-2025-35027 and CVE-2025-60251; The Hacker News (Aug 2026)'],
     'finding': 'CONTESTED for robots as a class, open for the consumer and humanoid products the harvester named. KUKA\'s robot '
                'system is certified to IEC 62443-4-2 Security Level 2 and claimed by KUKA to meet the CRA already (Jul 2026); '
                'Roborock robot vacuums hold a TUV Rheinland ETSI EN 303 645 certification (2024). Neither is an assessment on '
                'the harvester\'s metric (vulnerabilities found by an automated tool), and the CRA\'s main obligations bind only '
                'from 11 Dec 2027, so the target is prospective. The Unitree fleet-wide flaws are registered CVEs (NIST analysed '
                'CVE-2025-35027), but they were found by the harvester\'s own G1 co-authors, so the harvester\'s "no independent '
                'replication" stands; the researchers report no vendor engagement, and a year later two new G1 root-RCE chains had '
                'no verified firmware fix (Aug 2026, trade press relaying a co-author of the consumer-robot paper).',
     'harvester_errors': []},
    {'bottleneck': 'r4-B7',
     'searched': ['WebSearch: embodied agent privacy benchmark 2026 arXiv physical world privacy LLM agent improved privacy violation '
                  'rate method',
                  'WebSearch: robot vacuum TUV privacy certification ETSI EN 303 645 ... (as r4-B6)',
                  'EAPrivacy v3 re-fetched (byte-identical) and Table 1 read in full; arXiv 2605.05340v2 (IMMERSEDPRIVACY); Roborock '
                  'Trust Center (Aug 2026); Agility Digit 5 release (Sep 2026)'],
     'finding': 'Open on the named metric, CONTESTED on the deployed-product half. In EAPrivacy the best model generates a '
                'privacy-respecting plan in at most 29% of Tier 3 cases, but gpt-5-high selects the right plan in 100% of the same '
                'scenarios (and 1.00 in Tier 4): the gap is in generation, not recognition. A newer benchmark (IMMERSEDPRIVACY, May '
                '2026) puts the best 2026 model at 51% of conflict cases handled correctly. Mass-market and industrial robots '
                'with consent-before-collection, local processing and a third-party privacy certification exist (Roborock, EN 303 '
                '645; Agility Digit 5, company statement), so the harvester\'s generalisation from three niche products and one '
                'humanoid to deployed consumer robots is overstated.',
     'harvester_errors': ['EAPrivacy Tier 3: the harvester reported the generative violation rate (best 71%, gap 71 points) but not the '
                          'same tier\'s selection accuracy, where gpt-5-high reaches 1.00; B-c should report both.',
                          'Minor: the harvester quoted the paper\'s text "2.5-flash-w.o.think and 4o, achieve the lowest violation '
                          'rates of 71%"; the paper\'s Table 1 has no 4o column and gives 0.71 for 2.5-flash-w.o.think only (a '
                          'source inconsistency, faithfully quoted).',
                          '"deployed consumer robots stream sensor telemetry without consent": generalised from three niche '
                          'products (Alias Robotics assessment) and the Unitree G1; market-leading consumer robots claim and hold '
                          'third-party certifications to the contrary.']},
    {'bottleneck': 'r4-B8',
     'searched': ['WebSearch: arXiv 2026 speed and separation monitoring productivity cycle time close to nominal human-robot '
                  'collaboration reduces idle time',
                  'WebSearch: 2025 study human-robot collaboration cell throughput higher than fenced robot cell productivity speed '
                  'and separation monitoring industrial case',
                  'WebSearch: arXiv 2025 2026 "speed and separation monitoring" less conservative productivity improvement percent '
                  'certified human pose',
                  'WebSearch: arXiv 2025 human-robot collaborative assembly total cycle time lower than manual and fenced robot '
                  'comparison speed separation monitoring experiment',
                  'WebSearch: "safety-aware" motion planning human-robot collaboration 2026 arXiv avoids slowdown maintains nominal '
                  'speed near human trajectory optimization ISO 10218',
                  'WebSearch: ISO 10218-2:2025 transient contact higher speed power and force limiting productivity',
                  'WebSearch: 2026 arXiv human-robot collaboration safety speed scaling "without loss" throughput predictive SSM',
                  'arXiv 2606.13203v1 (predictive CBF); arXiv 2503.07192v2 (MARSHA); arXiv 2609.32354v1 (proactive planning, '
                  '2-page abstract, 22% figure without a nominal baseline; screened); ajot.com (AMR picking, off-topic); '
                  'sciencedirect S1877050925002352 (HTTP 403); link.springer.com s10846-025-02268-7 and PMC12360944 (challenge '
                  'pages, no text)',
                  'Faroni et al. Table III re-read (greedy 0.74 / 0.68, Monte Carlo 0.72 / 0.66): harvester numbers correct'],
     'finding': 'OPEN, as the harvester read it (no contrary claim of the declared kinds found), with a smaller gap on another '
                'protocol. A 2026 predictive-CBF controller keeps a '
                'mean speed scaling of 0.81 (vs 0.15 for standard SSM) in a 15,000 s simulation replaying recorded human motion, '
                'above the harvester\'s 0.74 on a real cell; safety-aware replanning cuts execution time by up to 60% against SSM. '
                'No source reports nominal speed (s = 1) with a person nearby, and the harvester already flagged that s = 1 is an '
                'oracle no safe cell reaches. No primary source was found arguing that cell throughput (human plus robot) rather '
                'than robot speed is the right metric.',
     'harvester_errors': []},
]
