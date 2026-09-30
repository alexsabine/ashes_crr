"""ROB1 stage 1, family R1 (Robotics/DECLARATION.md): programmes. ARIA's robotics programmes and opportunity spaces, with
corroboration from other public programmes that state robotics targets (DARPA, EU Horizon/euROBIN, NSF).

Every source was fetched on 2026-09-30 through the session proxy. Quotes are copied from the text extracted from the fetched
file: PDFs by pymupdf 1.28.2 (`page.get_text()`, pages joined by newlines); HTML pages by BeautifulSoup 4 (`get_text('\n')`
after removing script/style/noscript/svg, runs of spaces and blank lines collapsed); the one Markdown file (the Robothon
results README) is used as fetched. Raw files live outside the repository under /tmp/claude-0/rob_src/ (`raw_file` is
relative to that root; the fetched originals are in r1/src/); their sha256 is in /tmp/claude-0/rob_src/r1/SHA256SUMS.txt and
in the dossier docs/citations/rob1_r1_2026-09-30.md. Table rows are quoted as the extractor emitted them, cell by cell in
reading order. To be checked by Robotics/checks/verify.py; at harvest time a scratch copy of Open_Bottlenecks/checks/verify.py
pointed at this file and this root read "quotes found verbatim: 114 of 114 (claims 49; raw files 26, missing 0)".

Roles (DECLARATION.md stage 1): a = the problem stated; b = a 2025-26 statement that it is open, unsolved or a main challenge;
c = the best reported result on a named benchmark or metric against the target (numbers quoted; the gap is computed in
`agent_note` and in BOTTLENECKS); d = the method families tried and the assumption each makes (about time, clocks,
boundaries, interruptions, memory or tuning). `agent_note` is the agent's reading, not the source's words. Numbers from
different sources are not comparable unless a note says the protocol is shared. Programme documents state targets; they
are the sources' goals, not measured facts, and a thesis's cost figures are the programme team's own rough estimates.
"""

R = 'r1/txt/'

CLAIMS = [
    # ---------------- r1-B1: dexterous manipulation, speed and generality against a human (ARIA Robot Dexterity)
    {'id': 'r1:1', 'bottleneck': 'r1-B1', 'role': 'a',
     'source': 'ARIA, Robot Dexterity - Handling our future, programme thesis (Jenny Read, Programme Director)',
     'version': 'v2 (PDF created 14 Jun 2024, modified 15 Jul 2024; the original v1 was published Feb 2024)',
     'url': 'https://aria.org.uk/media/xamlbwdo/aria-robotic-dexterity-programme-thesis.pdf',
     'quote': ['Despite steady progress, general dexterous manipulation remains an unsolved problem in robotics. Key challenges '
               'include handling previously unseen objects, including delicate and deformable items, in a variety of lighting '
               'conditions, while avoiding error and damage over long periods of time.',
               'Dexterous manipulation is a critical bottleneck to the wide adoption of robotics.'],
     'raw_file': R + 'aria-robotic-dexterity-programme-thesis.txt',
     'agent_note': 'The programme\'s problem statement (2024). The thesis sets no numeric dexterity target; targets are left to '
                   'the Creators (TA1.1 "Specify quantitative metrics wherever possible"), so the B-c target below is a human '
                   'baseline from an independent benchmark.'},
    {'id': 'r1:2', 'bottleneck': 'r1-B1', 'role': 'a',
     'source': 'ARIA, Robot Dexterity programme page',
     'version': 'live page fetched 2026-09-30 (no last-updated date shown; lists items dated to 28 Feb 2026)',
     'url': 'https://aria.org.uk/opportunity-spaces/adaptive-machines/robot-dexterity',
     'quote': ['Breakthroughs in AI are transforming robotic abilities, but the development of robot bodies has not kept pace '
               'with advances in computation. Robots cannot achieve the flexibility, speed, and precision of human manipulation, '
               'rendering them useless for many of the difficult or dangerous tasks where we need them most.',
               'Backed by £57m, this programme sits within the Adaptive Machines opportunity space'],
     'raw_file': R + 'aria_opportunity-spaces_adaptive-machines_robot-dexterity.txt',
     'agent_note': 'Current programme page. Recorded as a (not b) because the page carries no date for this text.'},
    {'id': 'r1:3', 'bottleneck': 'r1-B1', 'role': 'b',
     'source': 'ARIA external expert committee (Richardson, Caliskanelli, Rai et al.), Revolutionising the robotics ecosystem '
               'through enhanced modularity and interoperability (Robot Dexterity TA3 position paper), foreword by Jenny Read',
     'version': '2025 (undated PDF; the text reports a survey in Feb 2025 and a workshop on 13 Mar 2025; references accessed 12/08/2025)',
     'url': 'https://www.aria.org.uk/media/xnwais2c/aria-ta3-position-paper_master.pdf',
     'quote': ['As artificial intelligence continues to advance in areas such as language, perception, and reasoning, the gap '
               'between what machine intelligence can achieve in silico and what robots can physically do is becoming '
               'increasingly apparent.'],
     'raw_file': R + 'aria-ta3-position-paper_master.txt',
     'agent_note': '2025 programme statement that the physical-capability gap is open and widening relative to AI.'},
    {'id': 'r1:4', 'bottleneck': 'r1-B1', 'role': 'b',
     'source': 'Serra, Azevedo, Silva, Alcedo, Rouxel, So, Suarez, Albu-Schaeffer & Lima, Transferability Through Cooperative '
               'Competitions (the first euROBIN Coopetition, EU Horizon Europe grant 101070596, Nancy, Nov 2024)',
     'version': 'arXiv v1, 29 Mar 2026', 'url': 'https://arxiv.org/abs/2603.27770v1',
     'quote': ['Overall, results across the three leagues confirm that autonomy in previously unknown, dynamic, and '
               'unstructured settings remains an open challenge, particularly for manipulation tasks.',
               'Fully autonomous manipulation remained rare, and several teams relied on teleoperation or human assistance.',
               'However, performance declined in later milestones requiring dynamic perception and high-precision actions.'],
     'raw_file': R + '2603.27770v1.txt',
     'agent_note': '2026 statement from the EU robotics network of excellence that autonomous manipulation is open. The league '
                   'scores are in figures only; no number is taken from this source.'},
    {'id': 'r1:5', 'bottleneck': 'r1-B1', 'role': 'c',
     'source': 'So, Sarabakha, Wu, Culha, Abu-Dakka & Haddadin, Digital Robot Judge: Building a Task-centric Performance Database '
               'of Real-World Manipulation With Electronic Task Boards (IEEE Robotics & Automation Magazine), Table 6 and text',
     'version': 'accepted version, CC BY 4.0 (PDF dated 21 Mar 2024; Mondragon repository deposit 17 Jun 2024; issue 2024)',
     'url': 'https://hdl.handle.net/20.500.11984/6531',
     'quote': ['This group’s average trial completion time was 18.9 s, with a standard deviation of 9.5 s and a best time of 8.1 s.',
               'We found that the best robot performance is only 16% as fast as the best human performance across the entire set of tasks.',
               'SHumanBody,Human* 0.6 1.6 1.4 2.4 1.7 0.4 8.1',
               'SEpson-VT6,Team J 11 7 6 12 10 6 52',
               'SAnyRobot,AnyAlgorithm 11 5.8 5.1 12 0.2 1.9 52',
               'TABLE 6. Score in seconds and RTC for the trial protocol between the best robots and best human performance.'],
     'raw_file': R + 'DRJ_So2024_RAM.txt',
     'agent_note': 'Named benchmark: the Robothon electronic task board trial protocol (six subtasks ST1-ST6; Robothon 2021 and '
                   '2022). Same paper, same protocol. Best full trial: human 8.1 s against best robot 52 s (Team J, Epson VT6); '
                   'robot speed 8.1/52 = 0.156 of the human (the paper rounds to 16%), i.e. 6.4x slower. On one subtask (ST5, '
                   'battery handling) a purpose-built robot took 0.2 s against the human 1.7 s (8.5x faster, the paper\'s "9x"). '
                   'Human baseline: best of N = 10 people, at least 10 trials each.'},
    {'id': 'r1:6', 'bottleneck': 'r1-B1', 'role': 'c',
     'source': 'Robothon Grand Challenge results repository (organiser: Peter So, TUM MIRMI), README',
     'version': 'GitHub peterso/robothon-grand-challenge, main branch, fetched 2026-09-30; the Robothon 2025 scorecard PDF in the '
                'same repository was created 16 Mar 2026',
     'url': 'https://github.com/peterso/robothon-grand-challenge',
     'quote': ['10-minute time limit for fully autonomous solution, task board randomly placed by team and fixed on velcro strips '
               'prior to trial start.',
               '8 Applications, 8 Selected Teams, 1 Finisher, Best Time 106 seconds.',
               '29 Applications, 20 Selected Teams, 7 Finishers, Best Time 57 seconds.'],
     'raw_file': R + 'github_robothon-grand-challenge_README.txt',
     'agent_note': '2025 result on the successor board (TBv2025, a different protocol from r1:5): 1 of 8 selected teams completed '
                   'the fully autonomous trial within 10 minutes (12.5%), best 106 s; 2023 (TBv2023): 7 of 20, best 57 s. No '
                   'human time is published for TBv2023 or TBv2025, so no gap is computed from these rows.'},
    {'id': 'r1:7', 'bottleneck': 'r1-B1', 'role': 'a',
     'source': 'European Commission, Horizon Europe Work Programme 2026-2027, 7. Digital, Industry and Space, topic '
               'HORIZON-CL4-2026-05-DIGITAL-EMERGING-03 (Next-Generation Agile and Intelligent Robotics Platforms)',
     'version': 'Annex VII, PDF dated 29 Sep 2026 (file metadata)',
     'url': 'https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/wp-call/2026-2027/wp-7-digital-industry-and-space_horizon-2026-2027_en.pdf',
     'quote': ['Novel robot design technique, materials and control techniques for flexible and meticulous manipulation of robots '
               'in unstructured environment, with high autonomy and in collaboration with humans.',
               'To ensure relevance and uptake, solutions must address industrial demands for high speed, precision, and '
               'reliability, enabling deployment in real-time, high-performance operational contexts.'],
     'raw_file': R + 'wp-7-digital-industry-and-space_horizon-2026-2027_en.txt',
     'agent_note': 'EU programme corroboration: the expected outcome names the same capability as ARIA. No numeric target.'},
    {'id': 'r1:8', 'bottleneck': 'r1-B1', 'role': 'd',
     'source': 'ARIA, Robot Dexterity programme thesis', 'version': 'v2 (2024)',
     'url': 'https://aria.org.uk/media/xamlbwdo/aria-robotic-dexterity-programme-thesis.pdf',
     'quote': ['Brute force, computationally intensive control of rigid structures can only get us so far.',
               'Similarly in robotics, mechanical and electrical engineers design and build hardware, which is then animated '
               'either by human tele-operators or by algorithms designed by computer scientists[5].',
               'Biological organisms operate successfully with noisy, imprecise hardware and long, highly variable sensorimotor '
               'latencies (25ms for some proprioceptive reflexes, 200ms for saccades[7] in contrast to the high frequencies and '
               'low latencies (1ms) typical of robotic control.',
               'Recent developments in AI, including in reinforcement learning[3] and the use of multimodal LLMs to improve '
               'scene understanding,[4] will help to increase generalisability and adaptability.'],
     'raw_file': R + 'aria-robotic-dexterity-programme-thesis.txt',
     'agent_note': 'Families: (i) the "Genesis paradigm": rigid hardware, then control by teleoperation or by algorithms, with '
                   'high-rate fixed-clock control (about 1 ms loops, per the thesis); (ii) learned control (RL, VLA/LLM scene '
                   'understanding); (iii) ARIA\'s proposal, co-design of body and control ("Darwin paradigm"), which tolerates '
                   'long, variable latencies. Assumption named by the source: control runs on a fast fixed clock and the body '
                   'is fixed before control is designed.'},
    {'id': 'r1:9', 'bottleneck': 'r1-B1', 'role': 'd',
     'source': 'So et al., Digital Robot Judge (IEEE RAM)', 'version': 'accepted version, 2024',
     'url': 'https://hdl.handle.net/20.500.11984/6531',
     'quote': ['This clever technique was a great example of a purpose-built solution excelling in a single task.',
               'However, both winning robot teams were still far from achieving the general dexterity and speed of a human '
               'across all manipulation tasks.'],
     'raw_file': R + 'DRJ_So2024_RAM.txt',
     'agent_note': 'Specialised-fixture family: fast on one known subtask, slow across the set; it assumes the task is known in '
                   'advance.'},
    {'id': 'r1:10', 'bottleneck': 'r1-B1', 'role': 'd',
     'source': 'Serra et al., Transferability Through Cooperative Competitions (euROBIN)', 'version': 'arXiv v1, 29 Mar 2026',
     'url': 'https://arxiv.org/abs/2603.27770v1',
     'quote': ['referees noted that prior access to the task board may have encouraged tailored, task-specific solutions, '
               'raising concerns about robustness under more randomized conditions.',
               'Teams could opt for teleoperation, in which case referees specified the operator’s location.'],
     'raw_file': R + '2603.27770v1.txt',
     'agent_note': 'Assumptions: the task (board, sequence) is known and rehearsed beforehand; a human teleoperator is available '
                   'as fallback.'},

    # ---------------- r1-B2: legged locomotion range, endurance and robustness outside prepared ground (ARIA Robot Locomotion)
    {'id': 'r1:11', 'bottleneck': 'r1-B2', 'role': 'a',
     'source': 'ARIA, Robot Locomotion programme thesis (Jenny Read, Programme Director)',
     'version': 'v1.0 (PDF created 11 Jun 2026; feedback workshop 30 Jun - 1 Jul 2026)',
     'url': 'https://aria.org.uk/media/3yglnoch/programme-thesis_robot-locomotion.pdf',
     'quote': ['Legged robots can perform astonishing athletic feats, but a body that can briefly coordinate huge forces for a '
               'backflip is not necessarily one that can spend a shift carrying loads over uneven terrain without overheating, '
               'falling or breaking.',
               'Our central insight is that the limitations of current robots cannot be overcome by AI and control alone.'],
     'raw_file': R + 'programme-thesis_robot-locomotion.txt', 'agent_note': 'The problem stated by the programme (2026).'},
    {'id': 'r1:12', 'bottleneck': 'r1-B2', 'role': 'b',
     'source': 'Jenny Read (ARIA), Robot Locomotion: a possible ARIA programme (ARIA insights)',
     'version': '15 April 2026', 'url': 'https://aria.org.uk/insights/2026/robot-locomotion-a-possible-aria-programme',
     'quote': ['Animals still outperform robots on the combination of agility, range, and robustness that real-world locomotion demands.',
               'Until then, robots will remain confined to prepared environments, near charging points, and with short operating windows.'],
     'raw_file': R + 'aria_insights_2026_robot-locomotion-a-possible-aria-programme.txt',
     'agent_note': '2026 statement that the gap is open.'},
    {'id': 'r1:13', 'bottleneck': 'r1-B2', 'role': 'b',
     'source': 'ARIA, Robot Locomotion programme page ("Launching soon", backed by £60m)',
     'version': 'live page fetched 2026-09-30 (programme announced 2026)',
     'url': 'https://aria.org.uk/opportunity-spaces/adaptive-machines/robot-locomotion',
     'quote': ['Legged robots show remarkable agility, but cannot yet operate reliably for long periods beyond controlled '
               'environments such as warehouse floors.'],
     'raw_file': R + 'aria_opportunity-spaces_adaptive-machines_robot-locomotion.txt',
     'agent_note': '2026 (the programme did not exist before the April 2026 blog).'},
    {'id': 'r1:14', 'bottleneck': 'r1-B2', 'role': 'c',
     'source': 'Burden, Libby, Jayaram, Sponberg & Donelan, Why animals can outrun robots (Science Robotics 9(89):eadi9754)',
     'version': 'final accepted version dated 27 Feb 2024 (author server); published 2024',
     'url': 'http://faculty.washington.edu/sburden/_papers/BurdenEtAl2024scirob.pdf',
     'quote': ['The farthest walk by a legged robot on a single battery charge was Ranger’s 65 kilometer trek over the course of '
               '31 hours (11).',
               'First of all, the robot’s batteries have about 50-fold less useful energy per unit mass as animal fat',
               'exceptional athletes can run hundreds of kilometers over multiple days in a single outing. And they can do so '
               'over rough terrain whereas Ranger exploits the smoothness of the track it was designed to walk on',
               'Outside controlled environments, robot range is a distant second to that of animals.'],
     'raw_file': R + 'BurdenEtAl2024scirob.txt',
     'agent_note': 'Metric: range, distance on one charge. Best robot 65 km in 31 h (Ranger, on a smooth track). Target: the '
                   'human/animal baseline, "hundreds of kilometers" over rough terrain (with refuelling); the source gives no '
                   'single number, so the range gap is at least 1.5x on distance (taking 100 km as the floor of "hundreds") '
                   'and qualitative on terrain. Stored energy: batteries about 50x below fat per unit mass.'},
    {'id': 'r1:15', 'bottleneck': 'r1-B2', 'role': 'c',
     'source': 'Riener, Rabezzana & Zimmermann, Do robots outperform humans in human-centered domains? (Frontiers in Robotics '
               'and AI 10:1223946)',
     'version': 'published 7 Nov 2023 (HTML full text, open access)',
     'url': 'https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2023.1223946/full',
     'quote': ['The COT of MIT cheetah (0.52) came closest of all robots to the COT of a human (0.2–0.47).',
               'In contrast, the comparison of locomotion functions shows that robots are trailing behind in energy efficiency, '
               'operational time, and transportation costs.'],
     'raw_file': R + 'riener2023_frobt.txt',
     'agent_note': 'Metric: cost of transport (dimensionless; lower is better). Best robot 0.52 against the human 0.2-0.47: the '
                   'best robot is 1.1x to 2.6x the human value. Values are samples from different references (the authors say '
                   'CoT varies between references).'},
    {'id': 'r1:16', 'bottleneck': 'r1-B2', 'role': 'd',
     'source': 'Jenny Read (ARIA), Robot Locomotion: a possible ARIA programme', 'version': '15 April 2026',
     'url': 'https://aria.org.uk/insights/2026/robot-locomotion-a-possible-aria-programme',
     'quote': ['They rely on stiff, power-hungry actuators. They spend too much energy holding themselves up. They imitate '
               'compliance in software instead of benefiting from it mechanically. Animals do the opposite: they store and '
               'release energy elastically, exploit resonance, distribute function across body and controller, and use the '
               'environment, rather than treating every disturbance as an error to suppress.'],
     'raw_file': R + 'aria_insights_2026_robot-locomotion-a-possible-aria-programme.txt',
     'agent_note': 'Families: stiff actuators with software-emulated compliance and disturbance rejection (every deviation from a '
                   'reference is an error); ARIA\'s alternative, mechanical compliance, elastic storage and resonance. The '
                   'operating assumption stated alongside (r1:12): robots work near charging points with short operating '
                   'windows, i.e. the mission is cut by recharge interruptions.'},
    {'id': 'r1:17', 'bottleneck': 'r1-B2', 'role': 'd',
     'source': 'Burden et al., Why animals can outrun robots', 'version': 'final accepted version, 2024',
     'url': 'http://faculty.washington.edu/sburden/_papers/BurdenEtAl2024scirob.pdf',
     'quote': ['Larger runners have more time to react to sensor signals before they hit the ground, so we normalize time by the '
               'natural period of a runner’s limb.',
               'In addition, period-specific latency is at least 1,000 times longer in nerves than an Ethernet cable, and it is '
               'impractical for biology to close this gap (87).',
               'feedback control can enable robots to recover from substantial perturbations (32), the ability of animals in '
               'this regard is unmatched (33).'],
     'raw_file': R + 'BurdenEtAl2024scirob.txt',
     'agent_note': 'Clock assumption in the comparison itself: latency is measured in units of the limb\'s natural period, not '
                   'seconds. Robots win on period-specific latency by at least 1,000x yet lose on performance, so the gap is not '
                   'a control-latency gap. Family: feedback control for recovery from perturbations.'},

    # ---------------- r1-B3: persistent stratospheric platforms at low cost and high recovery (ARIA Enduring Atmospheric Platforms)
    {'id': 'r1:18', 'bottleneck': 'r1-B3', 'role': 'a',
     'source': 'ARIA, Enduring Atmospheric Platforms, programme thesis (Rico Chandra, Programme Director)',
     'version': 'v2.0 (undated; revises v1.0 "Perpetual Flight" of Aug 2025; states the call is to launch in late 2025)',
     'url': 'https://aria.org.uk/media/et5hsubs/programme-thesis-enduring-atmospheric-platforms.pdf',
     'quote': ['Existing HAPS approaches — using fossil fuels, solar power, or lighter-than-air vehicles — have so far proven too '
               'limited, fragile, costly, or impractical to deliver a scalable solution.',
               'Aircraft amortisation dominates operational costs, with 1 in 4 missions ending with aircraft loss [6].'],
     'raw_file': R + 'programme-thesis-enduring-atmospheric-platforms.txt', 'agent_note': 'The problem stated (2025).'},
    {'id': 'r1:19', 'bottleneck': 'r1-B3', 'role': 'b',
     'source': 'ARIA, Enduring Atmospheric Platforms, call for proposals',
     'version': 'V.2, dated 11 December 2025 (PDF title: "revised version 18/02")',
     'url': 'https://aria.org.uk/media/noffgx5z/programme-solicitation-enduring-atmospheric-platforms.pdf',
     'quote': ['However, existing HAPS approaches remain too limited to deliver a commercially scalable solution.',
               'The required power threshold of 300 W, and the forward-looking plan for 3kW provision, lies significantly '
               'beyond the capability of state-of-the-art platforms, forcing applicants to fundamentally reimagine power '
               'generation.'],
     'raw_file': R + 'programme-solicitation-enduring-atmospheric-platforms.txt',
     'agent_note': '2025 programme statement that the target lies beyond the state of the art.'},
    {'id': 'r1:20', 'bottleneck': 'r1-B3', 'role': 'b',
     'source': 'Paul Marks, AALTO maintains 2026 target for commercial operations, despite aircraft loss (Aerospace America, AIAA)',
     'version': 'published 6 May 2025', 'url': 'https://aerospaceamerica.aiaa.org/aalto-maintains-2026-target-for-commercial-operations-despite-aircraft-loss/',
     'quote': ['The company has yet to achieve its target of 200 days of continuous flight needed for mobile connectivity and '
               'Earth observation services, among other business cases.',
               'That aircraft crashed after 64 days, hitting severe turbulence in a storm as it descended from the stratosphere '
               'to the much denser troposphere.',
               'The final technological hurdle for HAPS is enhancing their availability and reliability, especially during '
               'take-off and recovery.',
               'after the company’s latest Zephyr 8 had to be ditched into the Indian Ocean for reasons the company is still '
               'investigating. The ultralight solar-electric aircraft had just completed its 67th day aloft in the stratosphere'],
     'raw_file': R + 'aerospaceamerica_aalto.txt',
     'agent_note': 'Trade press (the AIAA\'s magazine), used only with the company statement r1:22 beside it. The "200 days" '
                   'target is the journalist\'s paraphrase of AALTO; the third quote is Paul Stevens (Voltitude CEO) by email. The '
                   'last quote records that the 2025 record aircraft was lost at the end of its 67-day flight, as the 2022 one '
                   'was after 64 days.'},
    {'id': 'r1:21', 'bottleneck': 'r1-B3', 'role': 'c',
     'source': 'ARIA, Enduring Atmospheric Platforms, programme thesis (cost table; "rough order of magnitude estimates by '
               'programme team and industry experts")',
     'version': 'v2.0 (late 2025)', 'url': 'https://aria.org.uk/media/et5hsubs/programme-thesis-enduring-atmospheric-platforms.pdf',
     'quote': ['Fossil-fuel long-endurance UAVs (e.g., ScanEagle, fully burdened): ~£1,000/hr',
               'Solar HALE (e.g. Zephyr): ~£7,000/hr',
               '~85% of cost is aircraft amortization; 1 in 4 aircraft lost on ascent/descent',
               'Battery degradation primary limiting factor capping endurance to 2 months',
               'Enduring Atmospheric Platforms Threshold: ~£500/hr',
               '<25% of cost will be aircraft amortization; loss rate improved to 1 in 20',
               'Enduring Atmospheric Platforms Goal: ~£100/hr'],
     'raw_file': R + 'programme-thesis-enduring-atmospheric-platforms.txt',
     'agent_note': 'Metric: gross hourly operating cost and aircraft loss rate. Best persistent platform (solar HALE) about '
                   '£7,000/hr against the programme threshold £500/hr (14x over) and goal £100/hr (70x over); the cheapest '
                   'listed long-endurance aircraft (fossil UAV) about £1,000/hr (2x over the threshold) lacks the endurance. '
                   'Loss rate 1 in 4 (recovery 0.75) against 1 in 20 (0.95, matching the call\'s Rredeployment > 0.95).'},
    {'id': 'r1:22', 'bottleneck': 'r1-B3', 'role': 'c',
     'source': 'Amprius Technologies (battery supplier), press release: AALTO Zephyr Achieves World-Record 67-Day Flight',
     'version': 'published 21 May 2025', 'url': 'https://amprius.com/aalto-zephyr-achieves-world-record-67-day-flight-powered-by-amprius-ultra-high-energy-batteries/',
     'quote': ['a world-record-setting 67-day flight in the stratosphere, which concluded on April 28, 2025.',
               'surpassed Zephyr’s previous endurance record of 64 days and marks the longest continuous aircraft flight ever recorded.'],
     'raw_file': R + 'amprius_aalto_67day.txt',
     'agent_note': 'Company statement (with AALTO\'s CTO quoted). Endurance 67 days far exceeds the ARIA endurance target '
                   '(TWR > 1 week), so endurance alone is NOT the open part: the aircraft was lost at the end of this flight '
                   '(ditched; r1:20) as in 2022, which fits the thesis\'s 1-in-4 loss rate and keeps cost and recovery '
                   'open. The flight was from Kenya (tropics); the ARIA target is year-round near the UK.'},
    {'id': 'r1:23', 'bottleneck': 'r1-B3', 'role': 'c',
     'source': 'ARIA, Enduring Atmospheric Platforms, call for proposals (Section 3, technical metrics)',
     'version': 'V.2, 11 December 2025',
     'url': 'https://aria.org.uk/media/noffgx5z/programme-solicitation-enduring-atmospheric-platforms.pdf',
     'quote': ['Primary metric: Demonstrate delivery of 300 W power to a payload in the sky, within line of sight of a fixed point '
               'on the ground, over the duration of one week (50.4 kWh)',
               'Programme Target: Rredeployment > 0.95',
               'Programme Target: CGross< £500 / hour'],
     'raw_file': R + 'programme-solicitation-enduring-atmospheric-platforms.txt',
     'agent_note': 'The targets as registered in the call. 300 W x 168 h = 50.4 kWh (checks). The same document gives the 3 kW '
                   'future target as both "0.5 MWh" and "840 kWh" for one week; 3 kW x 168 h = 504 kWh, so "840 kWh" is an '
                   'internal inconsistency (5 kW), not used here.'},
    {'id': 'r1:24', 'bottleneck': 'r1-B3', 'role': 'd',
     'source': 'ARIA, Enduring Atmospheric Platforms, call for proposals', 'version': 'V.2, 11 December 2025',
     'url': 'https://aria.org.uk/media/noffgx5z/programme-solicitation-enduring-atmospheric-platforms.pdf',
     'quote': ['Solar HAPS: Typically limited by endurance (especially at high latitudes) and cost (including high bill of '
               'materials, low reuse rates). These limitations appear unlikely to be overcome by improvements in photovoltaics '
               'and batteries alone.',
               'Balloons: Typically limited by controllability (station keeping, recovery) and endurance.',
               'Airships: Typically limited by cost (aircraft cost, endurance), and airspeed.'],
     'raw_file': R + 'programme-solicitation-enduring-atmospheric-platforms.txt',
     'agent_note': 'Three families and their stated limits.'},
    {'id': 'r1:25', 'bottleneck': 'r1-B3', 'role': 'd',
     'source': 'ARIA, Enduring Atmospheric Platforms, programme thesis', 'version': 'v2.0 (late 2025)',
     'url': 'https://aria.org.uk/media/et5hsubs/programme-thesis-enduring-atmospheric-platforms.pdf',
     'quote': ['the limited specific energy of batteries, which forces deep daily discharge cycles that shorten battery life, '
               'capping mission length [3].'],
     'raw_file': R + 'programme-thesis-enduring-atmospheric-platforms.txt',
     'agent_note': 'Solar family\'s clock: the diurnal cycle sets one deep discharge per day, so battery wear (and mission '
                   'length) is counted in days/cycles; the programme\'s cost proxies (TWR, Rredeployment) are also per mission '
                   'and per hour.'},

    # ---------------- r1-B4: heavy-lift drones, payload-to-weight ratio (DARPA Lift Challenge)
    {'id': 'r1:26', 'bottleneck': 'r1-B4', 'role': 'a',
     'source': 'DARPA, Lift Challenge programme page', 'version': 'live page fetched 2026-09-30 (announces DLC-2 for summer 2028)',
     'url': 'https://www.darpa.mil/research/challenges/lift',
     'quote': ['Current multirotor drones, also known as unmanned aircraft systems (UAS), are simple, affordable, and easy to '
               'operate. But their payload-to-weight ratio is low, typically 1:1 or less.',
               'The DARPA Lift Challenge aims to revolutionize heavy vertical lift aviation by seeking novel drone designs '
               'capable of carrying payloads more than four times their weight.'],
     'raw_file': R + 'darpa_research_challenges_lift.txt',
     'agent_note': 'Problem and target (> 4:1) stated by the programme; ARIA\'s Robot Locomotion thesis names the same limit '
                   '("carrying meaningful payloads over useful distances quickly creates short range").'},
    {'id': 'r1:27', 'bottleneck': 'r1-B4', 'role': 'a',
     'source': 'ARIA, Robot Locomotion programme thesis', 'version': 'v1.0 (PDF created 11 Jun 2026)',
     'url': 'https://aria.org.uk/media/3yglnoch/programme-thesis_robot-locomotion.pdf',
     'quote': ['Quadcopters need no road, runway or landing strip, but carrying meaningful payloads over useful distances quickly '
               'creates short range, noise, downwash and safety risks.'],
     'raw_file': R + 'programme-thesis_robot-locomotion.txt',
     'agent_note': 'ARIA names the payload limit of multirotors as a locomotion bottleneck (no numeric target).'},
    {'id': 'r1:28', 'bottleneck': 'r1-B4', 'role': 'b',
     'source': 'Jenny Read (ARIA), Robot Locomotion: a possible ARIA programme', 'version': '15 April 2026',
     'url': 'https://aria.org.uk/insights/2026/robot-locomotion-a-possible-aria-programme',
     'quote': ['Delivery drones are now real, but current commercial systems remain tightly constrained on payload, range, wind '
               'tolerance, and noise.'],
     'raw_file': R + 'aria_insights_2026_robot-locomotion-a-possible-aria-programme.txt',
     'agent_note': '2026 programme statement that payload (among others) is a binding constraint.'},
    {'id': 'r1:29', 'bottleneck': 'r1-B4', 'role': 'b',
     'source': 'DARPA news, Lift Challenge results', 'version': '11 Aug 2026', 'url': 'https://www.darpa.mil/news/2026/lift-challenge-awards',
     'quote': ['While this did not achieve the Challenge goal of a 4:1 ratio, it still represents a success by DARPA’s definition.'],
     'raw_file': R + 'darpa_news_2026_lift-challenge-awards.txt',
     'agent_note': '2026 statement that the goal was not met on a scored run.'},
    {'id': 'r1:30', 'bottleneck': 'r1-B4', 'role': 'c',
     'source': 'DARPA news, Lift Challenge results', 'version': '11 Aug 2026', 'url': 'https://www.darpa.mil/news/2026/lift-challenge-awards',
     'quote': ['The top-performing aircraft, designed by AVIDrone, Inc., pushed the limits of electric helicopter design and '
               'demonstrated an unprecedented payload-to-weight ratio of 3.84:1.',
               'While this team’s aircraft did not complete a scored run, it achieved the highest ratio in the competition at '
               '9.63 to 1.'],
     'raw_file': R + 'darpa_news_2026_lift-challenge-awards.txt',
     'agent_note': 'Metric: payload-to-weight ratio on a scored 5-nautical-mile circuit (aircraft <= 55 lb). Best scored 3.84 '
                   'against the goal 4.0: 96% of the goal, short by 0.16. A non-scored run reached 9.63 (above the goal), so the '
                   'target has been exceeded outside the scoring rules: expect CONTESTED at stage 1b.'},
    {'id': 'r1:31', 'bottleneck': 'r1-B4', 'role': 'c',
     'source': 'DARPA, Lift Challenge programme page', 'version': 'live page fetched 2026-09-30',
     'url': 'https://www.darpa.mil/research/challenges/lift',
     'quote': ['The 4:1 payload-to-weight ratio is possible and likely just the beginning.',
               'Aircraft will continue to be 55 lbs. or less',
               'A new course design will double in length to 10 nautical miles (8 loaded, 2 unloaded)'],
     'raw_file': R + 'darpa_research_challenges_lift.txt',
     'agent_note': 'The programme reads the goal as within reach and raises the course length for DLC-2 (2028).'},
    {'id': 'r1:32', 'bottleneck': 'r1-B4', 'role': 'd',
     'source': 'DARPA news, Lift Challenge results', 'version': '11 Aug 2026', 'url': 'https://www.darpa.mil/news/2026/lift-challenge-awards',
     'quote': ['This team\'s design blended a tri-rotor into the propulsive design of a propeller-driven rotor by using servos to '
               'change blade and motor angles.',
               'This team created a novel, scalable concept that uses hot or cold turbine exhaust to drive the rotors, replacing '
               'driveshafts and mechanical linkages.',
               'The aircraft uses string-based support to individual motors to reduce hub structure and overall vehicle weight.'],
     'raw_file': R + 'darpa_news_2026_lift-challenge-awards.txt',
     'agent_note': 'Families: electric single-rotor helicopter (winner), convertible tri-rotor, exhaust-driven rotors, '
                   'tension-structure multirotor. All are airframe/propulsion designs; none states an assumption about clocks, '
                   'interruptions or memory. The metric itself is static (one loaded circuit).'},

    # ---------------- r1-B5: autonomous search in unknown, communication-denied environments (DARPA SubT)
    {'id': 'r1:33', 'bottleneck': 'r1-B5', 'role': 'a',
     'source': 'DARPA, Subterranean (SubT) Challenge programme page', 'version': 'page fetched 2026-09-30 (Final Event 21-24 Sep 2021)',
     'url': 'https://www.darpa.mil/research/challenges/subterranean',
     'quote': ['DARPA’s Subterranean (SubT) Challenge seeks to better equip warfighters and first responders to explore uncharted '
               'underground environments that are too dangerous, dark, or deep to risk human lives.'],
     'raw_file': R + 'darpa_research_challenges_subterranean.txt', 'agent_note': 'The problem stated by the programme.'},
    {'id': 'r1:34', 'bottleneck': 'r1-B5', 'role': 'a',
     'source': 'DARPA news, Team CERBERUS and Team Dynamo Win DARPA Subterranean Challenge Final Event', 'version': 'Sept 2021',
     'url': 'https://www.darpa.mil/news/2021/subterranean-challenge-winners',
     'quote': ['In time-sensitive missions, such as active combat operations or disaster response, warfighters and first '
               'responders face difficult terrain, unstable structures, degraded environmental conditions, severe communication '
               'constraints, and expansive areas of operation,'],
     'raw_file': R + 'darpa_news_2021_subterranean-challenge-winners.txt',
     'agent_note': 'Programme manager (Timothy Chung) naming communication constraints as part of the problem.'},
    {'id': 'r1:35', 'bottleneck': 'r1-B5', 'role': 'a',
     'source': 'ARIA, Robot Locomotion programme thesis, Appendix (hypothetical sewer-robot target profile)',
     'version': 'v1.0 (PDF created 11 Jun 2026)',
     'url': 'https://aria.org.uk/media/3yglnoch/programme-thesis_robot-locomotion.pdf',
     'quote': ['intermittent GPS, radio and visual signal loss',
               'Complete 80% of route distance without teleoperation.',
               'Complete 95% of route distance without teleoperation.',
               'Fewer than 1 physical intervention per kilometre.',
               'illustrative purposes and does not imply that such areas are our priority.'],
     'raw_file': R + 'programme-thesis_robot-locomotion.txt',
     'agent_note': 'ARIA\'s own example of the metrics a platform team would register: operation through intermittent signal '
                   'loss, threshold 80% / stretch 95% of route without teleoperation, < 1 physical intervention per km. '
                   'Explicitly illustrative; not used as the B-c target.'},
    {'id': 'r1:36', 'bottleneck': 'r1-B5', 'role': 'b',
     'source': 'Wang, Yu, Xu, Gao, Yang, Tang, Yu, Chen, Gao, Jian, Chen, Gao, Zhou & Wang, Multi-Robot System for Cooperative '
               'Exploration in Unknown Environments: A Survey',
     'version': 'arXiv v3, 21 May 2025 (v1 10 Mar 2025, v2 25 Apr 2025)', 'url': 'https://arxiv.org/abs/2503.07278v3',
     'quote': ['The complexity of these environments originates from four core challenges: denied GNSS signals, large-scale '
               'scenarios, tough terrains, and intermittent communication.',
               'Moreover, range constraints, arising from both the intrinsic limitations of hardware transmission capabilities '
               'and environmental attenuation effects, pose the risk of partial system disconnections. This challenge becomes '
               'particularly severe in extreme environments such as subterranean voids or deep-sea fields.',
               'Learning-based planning methods have demonstrated great potential in multi-robot coordination tasks, but their '
               'development is still in its early stages, with limited real-world applications.'],
     'raw_file': R + '2503.07278v3.txt', 'agent_note': '2025 survey statement that intermittent communication remains a core challenge.'},
    {'id': 'r1:37', 'bottleneck': 'r1-B5', 'role': 'b',
     'source': 'Serra et al., Transferability Through Cooperative Competitions (euROBIN Outdoor Robots League)',
     'version': 'arXiv v1, 29 Mar 2026', 'url': 'https://arxiv.org/abs/2603.27770v1',
     'quote': ['Dynamic navigation on staircases or crowded areas remained a major barrier.'],
     'raw_file': R + '2603.27770v1.txt', 'agent_note': '2026 corroboration for navigation in unstructured settings (small sample: '
                                                       'one UAV and two UGV teams).'},
    {'id': 'r1:38', 'bottleneck': 'r1-B5', 'role': 'c',
     'source': 'Tranzatto et al., Team CERBERUS Wins the DARPA Subterranean Challenge: Technical Overview and Lessons Learned',
     'version': 'arXiv v1, 11 Jul 2022 (the only version)', 'url': 'https://arxiv.org/abs/2207.04914v1',
     'quote': ['every team had 60 min to find as many of the 40 artifacts distributed along the course as possible, while having '
               'a limited number of available report attempts (to discourage false positives).',
               'A point was earned for each report that correctly identified an artifact’s class and its position within 5 m of '
               'the object’s ground-truth location.'],
     'raw_file': R + '2207.04914v1.txt',
     'agent_note': 'Defines the benchmark (SubT Final Event prize round) and its ceiling: 40 points in 60 minutes.'},
    {'id': 'r1:39', 'bottleneck': 'r1-B5', 'role': 'c',
     'source': 'DARPA news, Team CERBERUS and Team Dynamo Win DARPA Subterranean Challenge Final Event (final scores)',
     'version': 'Sept 2021', 'url': 'https://www.darpa.mil/news/2021/subterranean-challenge-winners',
     'quote': ['23: CERBERUS (CollaborativE walking & flying RoBots for autonomous ExploRation in Underground Settings), '
               'DARPA-funded winner of the $2,000,000 first place prize',
               '23: CSIRO Data61, DARPA-funded winner of the $1,000,000 second place prize',
               '18: MARBLE (Multi-agent Autonomy with Radar-Based Localization for Exploration), DARPA-funded winner of the '
               '$500,000 third place prize'],
     'raw_file': R + 'darpa_news_2021_subterranean-challenge-winners.txt',
     'agent_note': 'Best 23 of 40 artifacts (57.5%) in 60 min, tied by two teams; 17 artifacts not scored. The result is from '
                   '2021; the challenge has not been re-run, so no newer number on this benchmark exists in the sources.'},
    {'id': 'r1:40', 'bottleneck': 'r1-B5', 'role': 'd',
     'source': 'Tranzatto et al., Team CERBERUS Wins the DARPA SubT Challenge', 'version': 'arXiv v1, 11 Jul 2022',
     'url': 'https://arxiv.org/abs/2207.04914v1',
     'quote': ['If the Human Supervisor allocated a time budget for exploration out of communication range, the Homing Timer block '
               'checks whether the given budget has elapsed and if so, it triggers the homing functionality of the exploration planner.',
               'If the connection is lost (based on a threshold on consecutive, failed pings), it commands the robot to backtrack '
               'its path until the connection is reestablished.',
               'triggers a backtracking of the traversed path, called “Recovery Homing,” in case the robot does not move for a '
               'predefined amount of time.',
               'If the robot was out of communication range of the Base Station, the artifact’s class and location was stored on '
               'the robot and was transferred to the Base Station once the communication was re-established.'],
     'raw_file': R + '2207.04914v1.txt',
     'agent_note': 'Lost-link family of the winning team: clock-time budgets (homing timer set by a human; recovery after a '
                   'predefined time without motion), a ping-count threshold for declaring the link lost, and backtracking to '
                   'regain it; findings are buffered on board and forwarded on reconnection (store-and-forward memory).'},
    {'id': 'r1:41', 'bottleneck': 'r1-B5', 'role': 'd',
     'source': 'Wang et al., Multi-Robot System for Cooperative Exploration in Unknown Environments: A Survey',
     'version': 'arXiv v3, 21 May 2025', 'url': 'https://arxiv.org/abs/2503.07278v3',
     'quote': ['Furthermore, CERBERUS implements automated homing based on remaining mission time and supports multi-robot '
               'coordination through frontier sharing in the global graph.'],
     'raw_file': R + '2503.07278v3.txt',
     'agent_note': 'Independent 2025 description of the same clock-based homing (remaining mission time).'},

    # ---------------- r1-B6: off-road ground autonomy at human-driver speed (DARPA RACER) - not shown open
    {'id': 'r1:42', 'bottleneck': 'r1-B6', 'role': 'a',
     'source': 'DARPA, RACER (Robotic Autonomy in Complex Environments with Resiliency) programme page',
     'version': 'live page fetched 2026-09-30',
     'url': 'https://www.darpa.mil/research/programs/robotic-autonomy-in-complex-environments-with-resiliency',
     'quote': ['However, military off-road autonomy algorithms and capability development has lagged due to the challenging '
               'complexity of off-road terrain environments and need to travel in them at relevant speeds.',
               'At a minimum, the program goal is software performance to move off-road at speeds on par with a human driver.'],
     'raw_file': R + 'darpa_research_programs_robotic-autonomy-in-complex-environments-with-resiliency.txt',
     'agent_note': 'Problem and target. The target is relative (a human driver); no human-driver speed is published in the '
                   'fetched pages.'},
    {'id': 'r1:43', 'bottleneck': 'r1-B6', 'role': 'c',
     'source': 'DARPA news, RACER\'s off-road autonomous vehicles teams navigate third test', 'version': '11 Apr 2023',
     'url': 'https://www.darpa.mil/news/2023/off-road-autonomous-vehicles',
     'quote': ['During the most recent experiment, teams completed more than 55 driverless runs of between roughly four and 11 '
               'miles each, reaching speeds of about 25 miles per hour. The performers completed 246 miles over 24.6 total hours '
               'on course with a robotic fleet of 12 RFVs.',
               'They will also be required to increase speeds to twice that of the first phase performance metrics.'],
     'raw_file': R + 'darpa_news_2023_off-road-autonomous-vehicles.txt',
     'agent_note': 'Experiment 3 (Fort Irwin): 246 mi / 24.6 h = 10.0 mph average, about 25 mph peak. No human-driver speed on '
                   'the same course is given, so no gap can be computed. The Phase 2 target is relative (2x the Phase 1 '
                   'metrics, which are not published in the fetched pages).'},
    {'id': 'r1:44', 'bottleneck': 'r1-B6', 'role': 'c',
     'source': 'DARPA news, RACER Speeds Into a Second Phase', 'version': '23 Apr 2024',
     'url': 'https://www.darpa.mil/news/2024/racer-second-phase',
     'quote': ['Teams successfully completed over 30 autonomous runs on courses varying from 3 to 10 miles in length, achieving '
               'over 150 autonomous, unoccupied miles at speeds up to 30 miles per hour.'],
     'raw_file': R + 'darpa_news_2024_racer-second-phase.txt',
     'agent_note': 'Experiment 4 (late 2023): peak up to 30 mph; no average speed or human-driver comparison is given.'},
    {'id': 'r1:45', 'bottleneck': 'r1-B6', 'role': 'd',
     'source': 'DARPA news, RACER\'s finish line', 'version': '14 Jan 2026', 'url': 'https://www.darpa.mil/news/2026/racer-finish-line',
     'quote': ['users can now apply the RACER stack to any vehicle (equipped with appropriate sensors), turning it into an '
               'autonomous machine capable of operating in challenging off-road environments, independent of GPS or pre-mapped '
               'routes, and at mission-relevant speeds.',
               'Earlier autonomous systems were slow to adapt to a new environment, requiring weeks of retraining.',
               'According to Young, what would normally take weeks to retrain a new model can now be done in a day.'],
     'raw_file': R + 'darpa_news_2026_racer-finish-line.txt',
     'agent_note': 'Family: a platform-agnostic learned autonomy stack, retrained per new environment (weeks -> one day), not '
                   'dependent on GPS or maps. This is also the programme\'s own 2026 completion claim: no 2025-26 source found '
                   'here states the problem open, and no number compares RACER with a human driver.'},

    # ---------------- r1-B7: modularity and interoperability of robot hardware and software (ARIA Robot Dexterity TA3) - not shown open
    {'id': 'r1:46', 'bottleneck': 'r1-B7', 'role': 'a',
     'source': 'ARIA TA3 expert committee, Revolutionising the robotics ecosystem through enhanced modularity and interoperability',
     'version': '2025', 'url': 'https://www.aria.org.uk/media/xnwais2c/aria-ta3-position-paper_master.pdf',
     'quote': ['Most current RAS systems are not modular or easily interoperable, limiting flexibility, scalability and '
               'increasing the likelihood of rapid obsolescence.',
               'As a consequence, integration costs are embedded as a significant part of total installation cost.'],
     'raw_file': R + 'aria-ta3-position-paper_master.txt', 'agent_note': 'The problem stated.'},
    {'id': 'r1:47', 'bottleneck': 'r1-B7', 'role': 'b',
     'source': 'ARIA TA3 expert committee position paper, foreword (Jenny Read)', 'version': '2025',
     'url': 'https://www.aria.org.uk/media/xnwais2c/aria-ta3-position-paper_master.pdf',
     'quote': ['A key reason why robotics has not yet progressed as rapidly as AI is the problem this paper seeks to address: a '
               'fragmented ecosystem.'],
     'raw_file': R + 'aria-ta3-position-paper_master.txt', 'agent_note': '2025 statement that it is open.'},
    {'id': 'r1:48', 'bottleneck': 'r1-B7', 'role': 'b',
     'source': 'Serra et al., Transferability Through Cooperative Competitions (euROBIN)', 'version': 'arXiv v1, 29 Mar 2026',
     'url': 'https://arxiv.org/abs/2603.27770v1',
     'quote': ['Yet, low-level and hardware-dependent modules remained difficult to integrate due to platform specificity.'],
     'raw_file': R + '2603.27770v1.txt', 'agent_note': '2026 corroboration.'},
    {'id': 'r1:49', 'bottleneck': 'r1-B7', 'role': 'd',
     'source': 'Serra et al., Transferability Through Cooperative Competitions (euROBIN)', 'version': 'arXiv v1, 29 Mar 2026',
     'url': 'https://arxiv.org/abs/2603.27770v1',
     'quote': ['The event showed module reuse can reduce development effort and, in some cases, improve task performance.',
               'While opinions diverged on enforcing standards, many teams agreed that shared data formats and communication '
               'protocols would ease integrations.'],
     'raw_file': R + '2603.27770v1.txt',
     'agent_note': 'Families: shared modules/marketplace, common data formats and protocols, standards. No numeric integration '
                   'metric or target is published, so no B-c.'},
]

BOTTLENECKS = [
    {'id': 'r1-B1', 'name': 'Dexterous manipulation: speed and generality against a human',
     'problem': 'Robot manipulators match or beat a human on one rehearsed subtask but are several times slower across a varied '
                'set, and fully autonomous completion of a varied manipulation protocol remains rare.',
     'open': True,
     'benchmark': 'Robothon electronic task board trial protocol (six subtasks), DR.J remote judge (So et al., IEEE RAM, Table 6); '
                  'Robothon 2025 (TBv2025) completion count',
     'best': 'best robot full trial 52 s (Team J, Epson VT6; also the best any-robot composite); 2025: 1 of 8 teams finished, 106 s',
     'target': 'human baseline: best human full trial 8.1 s (N = 10 people, mean 18.9 s); ARIA sets no numeric target',
     'gap_note': 'robot speed 8.1/52 = 0.156 of the best human (6.4x slower; 2.75x slower than the human mean 18.9 s); the robot '
                 'beats the human only on ST5 (0.2 s vs 1.7 s) with a purpose-built fixture. Same paper, same protocol. The 2025 '
                 'board has no human time, so its 1/8 completion is reported without a gap.',
     'assumptions': ['rigid hardware fixed first, then control designed for it (the "Genesis paradigm"), on a fast fixed control '
                     'clock (about 1 ms loops, per ARIA) - clock',
                     'a human teleoperator as fallback during tasks - interruption/human in the loop',
                     'task and board known and rehearsed in advance; purpose-built fixtures per subtask - boundaries given',
                     'learned control (RL, VLA/LLM scene understanding) expected to add generality - tuning/data'],
     'cpu_testable': False,
     'cpu_note': 'the benchmark is a physical task board timed on real robots; a simulated manipulation proxy could run on CPU but '
                 'would not be the benchmark or its human baseline'},
    {'id': 'r1-B2', 'name': 'Legged locomotion: range, endurance and robustness outside prepared ground',
     'problem': 'Legged robots cannot yet operate for long periods over uneven ground carrying loads; animals and humans exceed them '
                'on range, energy per distance and robustness.',
     'open': True,
     'benchmark': 'range on one charge (Burden et al. 2024); cost of transport (Riener et al. 2023)',
     'best': 'Ranger 65 km in 31 h on one charge, on a smooth track; best robot CoT 0.52 (MIT Cheetah)',
     'target': 'human/animal baseline: athletes run "hundreds of kilometers over multiple days" over rough terrain; human CoT '
               '0.2-0.47; batteries hold about 50x less energy per unit mass than fat',
     'gap_note': 'range at least 1.5x (65 km vs the floor of "hundreds"), and on smooth ground only; CoT 1.1x-2.6x the human value '
                 'for the best robot. The sources give no single human range number; CoT samples come from different references.',
     'assumptions': ['stiff actuators with compliance emulated in software; every disturbance treated as an error to reject - '
                     'control on the robot\'s reference, not the body\'s dynamics',
                     'missions cut short by recharging: robots stay near charging points with short operating windows - '
                     'interruption',
                     'feedback control for recovery from perturbations',
                     'comparisons of latency normalised by the limb\'s natural period (Burden) rather than seconds - a body clock'],
     'cpu_testable': False,
     'cpu_note': 'range and CoT are measured on physical robots; a simulated legged proxy (MuJoCo-class) is CPU-feasible for short '
                 'gaits but not for the benchmark'},
    {'id': 'r1-B3', 'name': 'Persistent stratospheric platforms at low hourly cost and high recovery',
     'problem': 'High-altitude platforms can stay aloft for weeks, but at a cost per hour and an aircraft loss rate that rule out '
                'commercial service, and they cannot yet power a 300 W payload year-round at UK latitudes.',
     'open': True,
     'benchmark': 'ARIA EAP metrics: gross hourly operating cost CGross, redeployment (recovery) rate, 300 W for one week on station',
     'best': 'solar HALE (Zephyr) about £7,000/hr with 1 in 4 aircraft lost on ascent/descent (ARIA estimate); 67-day record '
             'flight (2025) ended with the aircraft lost',
     'target': 'CGross < £500/hr by programme end (goal £100/hr); Rredeployment > 0.95 (loss 1 in 20); 300 W for one week (50.4 kWh)',
     'gap_note': 'cost 14x over the threshold, 70x over the goal; recovery 0.75 vs > 0.95; endurance (> 1 week) already exceeded '
                 'by 67 days in the tropics, so it is not the open part; the 300 W payload power is stated to lie "significantly '
                 'beyond" the state of the art (no state-of-the-art watt figure quoted).',
     'assumptions': ['solar family: one deep battery discharge per day; battery wear counted in daily cycles caps mission length - '
                     'a diurnal clock',
                     'costs amortised per mission hour; each mission a boundary with a fixed probability of loss on '
                     'ascent/descent',
                     'balloons: limited station keeping and recovery; airships: cost and airspeed'],
     'cpu_testable': False,
     'cpu_note': 'the benchmark is a week-long flight demonstration; the programme\'s techno-economic cost model is CPU-computable, '
                 'but it is a model, not the benchmark'},
    {'id': 'r1-B4', 'name': 'Heavy-lift drones: payload-to-weight ratio',
     'problem': 'Multirotor drones typically lift no more than their own weight; the programme target is more than four times.',
     'open': True,
     'benchmark': 'DARPA Lift Challenge (DLC-1): payload-to-weight on a scored 5-nautical-mile circuit, aircraft <= 55 lb',
     'best': '3.84:1 (AVIDrone, scored); 9.63:1 in a run that was not scored (DefendTex)',
     'target': '4:1 (Challenge goal); typical current multirotor 1:1 or less',
     'gap_note': 'scored best is 96% of the goal (short by 0.16); an unscored run exceeded it 2.4x. Narrowly open under the '
                 'programme\'s own scoring; likely CONTESTED at the double check.',
     'assumptions': ['static metric: one loaded circuit; no clock, interruption or memory assumption stated',
                     'airframe and propulsion families (electric helicopter, convertible tri-rotor, exhaust-driven rotors, '
                     'tension-structure multirotor)'],
     'cpu_testable': False,
     'cpu_note': 'a flight-hardware benchmark; nothing about it runs on this machine'},
    {'id': 'r1-B5', 'name': 'Autonomous search in unknown, communication-denied environments',
     'problem': 'Robot teams exploring unknown underground spaces with intermittent communication find only part of what is there '
                'in the time allowed.',
     'open': True,
     'benchmark': 'DARPA SubT Challenge Final Event prize round (40 artifacts, 60 minutes, one human supervisor)',
     'best': '23 of 40 artifacts (CERBERUS and CSIRO Data61, tied; 2021)',
     'target': '40 of 40 artifacts in 60 minutes (the course total)',
     'gap_note': '57.5% of the artifacts; 17 unfound. The result is from 2021 and the benchmark has not been re-run; the 2025 '
                 'survey and 2026 euROBIN report still name intermittent communication and unstructured navigation as open.',
     'assumptions': ['lost link declared by a clock/count rule (a threshold on consecutive failed pings), then backtrack until '
                     'reconnection - interruption on a clock',
                     'out-of-range exploration bounded by a human-set time budget (homing timer) or remaining mission time - clock',
                     'recovery triggered after a predefined time without motion - clock',
                     'findings buffered on board and forwarded on reconnection - store-and-forward memory',
                     'learned planners early-stage, overfitting to training environments - tuning'],
     'cpu_testable': False,
     'cpu_note': 'the benchmark is a physical course (the SubT Virtual track needed a full robotics simulator); the lost-link rules '
                 'themselves could be simulated on CPU in a gridworld proxy'},
    {'id': 'r1-B6', 'name': 'Off-road ground autonomy at human-driver speed',
     'problem': 'Driving off-road autonomously at the speed of a human driver.',
     'open': False,
     'benchmark': 'DARPA RACER field experiments (E3 Fort Irwin 2023; E4 Texas 2023)',
     'best': 'E3: 246 miles in 24.6 hours (10.0 mph average), about 25 mph peak; E4: up to 30 mph',
     'target': '"speeds on par with a human driver" (no number published in the fetched pages)',
     'gap_note': 'not shown open: no human-driver speed is quoted, so no gap can be computed, and no 2025-26 source states the '
                 'problem open; DARPA reported the programme complete (14 Jan 2026) and transitioning.',
     'assumptions': ['a platform-agnostic learned autonomy stack retrained per new environment (weeks, now one day) - tuning',
                     'independent of GPS or pre-mapped routes'],
     'cpu_testable': False, 'cpu_note': 'full-size vehicles in field experiments'},
    {'id': 'r1-B7', 'name': 'Modularity and interoperability of robot systems',
     'problem': 'Robot hardware and software are rarely modular or interoperable, so integration is costly and modules are hard '
                'to reuse across platforms.',
     'open': False,
     'benchmark': 'none quantified (ARIA TA3 survey and workshop; euROBIN coopetition royalty scoring)',
     'best': 'none quoted', 'target': 'none quoted',
     'gap_note': 'not shown open: 2025-26 statements exist but no metric with a target is published; the euROBIN scores are in '
                 'figures only.',
     'assumptions': ['shared modules and a module marketplace; common data formats and protocols; standards'],
     'cpu_testable': False, 'cpu_note': 'an ecosystem property, not a benchmark'},
]
