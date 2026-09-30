"""Claims for ROB1 stage 3 (Robotics/DECLARATION.md), candidate C-R2 (Robotics/CRR_READING.md, r1-B5), searcher A:
an own-progress budget for out-of-contact exploration. Transcribed from the dossier docs/citations/rob1_s3_r2a_2026-09-30.md
(sources fetched 2026-09-30; raw files and extracted texts held outside the repository under /tmp/claude-0/rob_s3/, named in
`raw_file` relative to that root, with r2a/SHA256SUMS.txt beside them). Every quote is copied from a dossier blockquote and
was checked verbatim against its extracted text before this file was written (normalisation as Robotics/checks/verify.py).

The mechanism searched (CRR_READING.md, C-R2): bound an out-of-communication excursion (exploration beyond radio range,
lost-link behaviour, return to comms) by the robot's own progress, i.e. the information it has gathered since the last
contact (information gain, map growth, novelty, unreported data, artifact count), rather than by a wall-clock homing timer
or the remaining mission time. CRR's prediction: more artifacts found per mission at an equal rate of failures to return,
against the best fixed timer tuned on other maps.

Positions (the caller's):
  P1  a return or rendezvous decision triggered by information or progress accumulated since the last contact is published;
  P2  it is compared with a fixed time budget (timer, fixed interval, pre-set schedule or mission-time homing) and shown
      better (more coverage, information delivered or artifacts, at equal loss or return failure where the source models it);
  P3  it is used in a fielded system (DARPA SubT teams, mine-mapping drones, field deployments).

'reading' is decided by the stage-3 agent from the quote, for the investigator's review ('reading_by'). Reading policy,
fixed before the readings were written:
  states       the source publishes the position as stated: for P1 a return, relay, reconnection or rendezvous rule whose
               trigger or bound is a quantity of information or progress accumulated since the last contact (unreported
               data in a buffer, new observations, unshared map area, artifact count, a ratio of delivered to held
               information); for P2 such a rule measured against a clock rule and reported better; for P3 such a rule
               configured on a system run in the field or in a competition;
  close        a nearby mechanism that differs in one named respect: the accumulated information is one input to a learned
               or optimised policy rather than a stated trigger; the rule is described only second-hand or only in an
               abstract; the quantity is monitored but the trigger is not stated; the comparison is in a neighbouring
               setting (team communication events for task allocation) or on a different metric, or it is mixed;
  contradicts  the source shows the mechanism (or its limiting case) fails or is inferior to a clock rule.
Clock-only sources (the frontier's side: homing timers, fixed rendezvous intervals, latency bounds, battery-time returns) are
listed in the dossier as context and are not claims here. 'Not found' is never 'novel'.
"""

RB = "stage-3 agent (searcher A); for the investigator's review"
T = 'r2a/txt/'

CLAIMS = [
    # ------------------------------------------------ fielded SubT teams: CoSTAR (JPL) data-buffer trigger
    {'id': 'r2a:1', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Saboia, Clark, Thangavelu, Edlund, Otsu, ... Agha-mohammadi, "ACHORD: Communication-Aware Multi-Robot '
               'Coordination with Intermittent Connectivity" (Team CoSTAR; arXiv:2206.02245; RA-L 2022 per the search '
               'listing, venue not verified on the day)',
     'version': 'arXiv v1, 5 Jun 2022 (the only version)', 'url': 'https://arxiv.org/abs/2206.02245v1',
     'quote': ['the robots also maintain statistics on the reliable data that needs to be transferred to the base or other '
               'robots: (1) buffer size: the amount of data (in bytes) that needs to be transferred;',
               'Return to Comms: When the buffer sizes exceeds an upper bound (T u B = 300KB), the robot will sacrifice '
               'nominal exploration and instead move towards an area with strong comms.',
               'If the buffer size drops below a desired threshold (T l B = 200KB) before reaching the target checkpoint, '
               'nominal exploration continues immediately.'],
     'raw_file': T + 'pdf_2206.02245v1.txt',
     'agent_note': 'States P1 in C-R2\'s own terms: the out-of-contact excursion is ended by the amount of data gathered '
                   'and not yet delivered (the buffer, in bytes) reaching a fixed unit (300 KB), not by a timer. The unit is '
                   'bytes of reliable data (maps, artifact reports), not information gain in resolvable steps; a hysteresis '
                   'band (300/200 KB) is added. The only clock in the rule is a 60 s congestion timeout at the checkpoint.'},
    {'id': 'r2a:2', 'position': 'P3', 'reading': 'states', 'reading_by': RB,
     'source': 'Saboia et al., ACHORD (arXiv:2206.02245), evaluation and lessons learned',
     'version': 'arXiv v1, 5 Jun 2022 (the only version)', 'url': 'https://arxiv.org/abs/2206.02245v1',
     'quote': ['We evaluate our solution with respect to the comms performance in several challenging underground '
               'environments including the DARPA SubT Finals competition environment.',
               'If the network infrastructure covers enough of the environment, we found it was sufficient to return to '
               'comms sparingly. With sophisticated autonomy that can reliably determine when to return and transfer data, '
               'a small effective comms range and long outages are permissible.'],
     'raw_file': T + 'pdf_2206.02245v1.txt',
     'agent_note': 'States P3: the comms-aware coordination that contains the buffer-triggered Return to Comms (r2a:1) is the '
                   'system Team CoSTAR ran in the SubT Finals environment and a Kentucky Underground field test. The paper '
                   'does not count how often the trigger fired or isolate its effect on artifacts; it reports comms metrics '
                   '(maximum delay, up time, data rates).'},
    {'id': 'r2a:3', 'position': 'P3', 'reading': 'states', 'reading_by': RB,
     'source': 'Agha, Otsu, Morrell, ... (Team CoSTAR), "An Addendum to NeBula: Towards Extending TEAM CoSTAR\'s Solution to '
               'Larger Scale Environments" (arXiv:2504.13461; IEEE Trans. Field Robotics 1, 476-526, 2024 per the arXiv '
               'journal reference)',
     'version': 'arXiv v1, 18 Apr 2025 (the only version)', 'url': 'https://arxiv.org/abs/2504.13461v1',
     'quote': ['In this paper, we discuss a robotic autonomy solution deployed by Team CoSTAR at the DARPA SubT challenge.',
               'High buffer sizes indicate a robot has explored autonomously for a long period of time, and low data rates '
               'can be a sign of network congestion.',
               'For example, when the network performance state indicates that the buffers have grown too large, the robot '
               'will autonomously sacrifice nominal exploration and move towards a comms checkpoint with high SNR to return '
               'to comms and ensure this data is transferred.',
               'When the robot has been outside of the communications range of the base station for more than 10 minutes, '
               'the robot retraces its steps until communication is reestablished.',
               'Spot 4 went out of communication after 600 s into the run, and fell 80 s after that with 22 artifact '
               'messages still in its communication buffer.',
               'Later, Spot 3 approached the fallen robot to retrieve the data, and was able to transfer 10 messages to the '
               'base station.'],
     'raw_file': T + 'pdf_2504.13461v1.txt',
     'agent_note': 'States P3 (the buffer-grown return to comms in the deployed CoSTAR solution), with two cautions for the '
                   'investigator: the same team also used a clock rule (10 minutes out of range, in a limestone-mine test), '
                   'and the authors read the buffer as a proxy for time out of contact ("explored autonomously for a long '
                   'period of time"). The Final Event episode (a robot lost with 22 artifact messages in its buffer, 10 later '
                   'recovered by a data mule) is the failure-to-return cost that C-R2\'s prediction is scored on.'},
    {'id': 'r2a:4', 'position': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'Agha, Otsu, Morrell, Fan, Thakker, ... (Team CoSTAR), "NeBula: Quest for Robotic Autonomy in Challenging '
               'Environments; TEAM CoSTAR at the DARPA Subterranean Challenge" (arXiv:2103.11470; accepted in J. Field '
               'Robotics 2021 per the arXiv comment)',
     'version': 'arXiv v4, 18 Oct 2021 (v1 21 Mar 2021)', 'url': 'https://arxiv.org/abs/2103.11470v4',
     'quote': ['(iii) the information value (e.g., the numbers of detected artifacts) on each robot.',
               '(ii) how long each robot is out of the comm range, (iii) location of comm nodes',
               'Given these states, the mission planner will decide to deploy new robots, re-task or re-position active '
               'robots in the environment.',
               '(b) Return to Mesh Network, to ensure the data are communicated, then continue,'],
     'raw_file': T + 'pdf_2103.11470v4.txt',
     'agent_note': 'Close: the fielded mission planner monitors both the information a robot holds (its count of detected '
                   'artifacts) and the clock out of range, and has a Return to Mesh Network behaviour; the rule combining '
                   'them is not stated here (the buffer threshold is stated in r2a:1 and r2a:3).'},
    # ------------------------------------------------ fielded SubT teams: MARBLE (CU Boulder) artifact-count trigger
    {'id': 'r2a:5', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Biggie, Rush, Riley, Ahmad, Ohradzansky, Harlow, Miles, Torres, McGuire, Frew, Heckman, Humbert (Team '
               'MARBLE), "Flexible Supervised Autonomy for Exploration in Subterranean Environments" (arXiv:2301.00771; '
               'Field Robotics 3, 2023, doi 10.55417/fr.2023004 per arXiv)',
     'version': 'arXiv v2, 11 Apr 2023 (v1 2 Jan 2023)', 'url': 'https://arxiv.org/abs/2301.00771v2',
     'quote': ['Artifact monitor determines if the agent needs to return to communications to report the new information to '
               'the base station.',
               'The BOBCAT Artifact monitor which is triggered by 3 unreported artifacts or 5 minutes of exploration with a '
               'pending artifact, ultimately determines whether the robot should return to communications for unreported '
               'artifacts.',
               'There are at least 3 unreported artifacts, or it has been at least 5 minutes since the first unreported '
               'artifact was detected.'],
     'raw_file': T + 'pdf_2301.00771v2.txt',
     'agent_note': 'States P1: the return-to-comms decision is triggered by progress accumulated since the last contact, '
                   'counted in artifacts (3 unreported), with a clock backstop that starts only once there is something to '
                   'report (5 minutes since the first unreported artifact). The unit is an artifact count, one of the '
                   'quantities named in C-R2.'},
    {'id': 'r2a:6', 'position': 'P3', 'reading': 'states', 'reading_by': RB,
     'source': 'Biggie et al. (Team MARBLE), "Flexible Supervised Autonomy for Exploration in Subterranean Environments" '
               '(arXiv:2301.00771), configuration in the SubT Final Event',
     'version': 'arXiv v2, 11 Apr 2023', 'url': 'https://arxiv.org/abs/2301.00771v2',
     'quote': ['By default, and as configured during the Final Event Prize Run, artifact images not received by the base '
               'station are considered unreported artifacts, and will force the robot to return to communications until '
               'they are fully transmitted.',
               'Communicate with the base station, either by staying in or returning to communications.'],
     'raw_file': T + 'pdf_2301.00771v2.txt',
     'agent_note': 'States P3: the artifact-count trigger of r2a:5 was part of the configuration run in the DARPA SubT Final '
                   'Event Prize Run (MARBLE placed third, 18 points; harvester r1:39). No ablation against a timer is '
                   'reported.'},
    {'id': 'r2a:7', 'position': 'P3', 'reading': 'states', 'reading_by': RB,
     'source': 'Ohradzansky, Rush, Riley, Mills, Ahmad, McGuire, Biggie, Harlow, Miles, Frew, Heckman, Humbert (Team '
               'MARBLE), "Multi-Agent Autonomy: Advancements and Challenges in Subterranean Exploration" (arXiv:2110.04390; '
               'Field Robotics special issue, Phase I and II)',
     'version': 'arXiv v1, 8 Oct 2021 (the only version)', 'url': 'https://arxiv.org/abs/2110.04390v1',
     'quote': ['Once an artifact is detected, it switches its current mission mode from “Explore” to “Report”, and a path is '
               'planned back to the base station to relay the artifact information back.',
               'However, once a robot received acknowledgement from the base station that an artifact had been reported, '
               'the robot returned to Explore mode and continued to explore the environment until the next artifact was '
               'found.',
               'The Greedy Explore method was used through all phases of the competition, although communications beacons '
               'were not deployed during the initial tunnel event.'],
     'raw_file': T + 'pdf_2110.04390v1.txt',
     'agent_note': 'States P3 (and P1): in the Tunnel, Urban and Cave circuits the excursion was bounded by progress, one '
                   'artifact per excursion (explore until the next artifact, then return to report), not by a clock. It is '
                   'the unit-of-one limit of r2a:5.'},
    # ------------------------------------------------ academic multi-robot exploration: event-based (information-triggered) reconnection
    {'id': 'r2a:8', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Amigoni, Banfi, Basilico, "Multirobot Exploration of Communication-Restricted Environments: A Survey" (IEEE '
               'Intelligent Systems 32(6):48-57, 2017, doi 10.1109/MIS.2017.4531226; open author copy at the Politecnico di '
               'Milano repository)',
     'version': 'author manuscript, PoliMi repository handle 11311/1046659 (fetched 2026-09-30)',
     'url': 'https://re.public.polimi.it/retrieve/handle/11311/1046659/265235/ismultirobot.pdf',
     'quote': ['Event-based connectivity: robots must regain connection with some teammates according to a policy triggered '
               'by particular events, such as the discovery of new information about the environment or simply striking a '
               'given time.',
               'In presence of a fixed BS to which the gathered information should be relayed, the behavior of the robots '
               'is regulated by a utility function which considers the amount of information a robot has not yet delivered '
               'to the BS and the estimated amount of information known by the BS.'],
     'raw_file': T + 'amigoni_survey_ieeeis2017_polimi.txt',
     'agent_note': 'States P1 at the level of the field\'s taxonomy: reconnection triggered by the discovery of new '
                   'information and reconnection triggered by a clock are two named members of one published class '
                   '("event-based connectivity"), with the undelivered-information rule of Spirin et al. surveyed as an '
                   'instance.'},
    {'id': 'r2a:9', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Banfi, Quattrini Li, Rekleitis, Amigoni, Basilico, "Strategies for coordinated multirobot exploration with '
               'recurrent connectivity constraints" (Autonomous Robots 42(4):875-894, 2018, doi 10.1007/s10514-017-9652-y; '
               'open author copy at the Politecnico di Milano repository)',
     'version': 'author manuscript (file AURO2016.pdf), PoliMi repository (fetched 2026-09-30)',
     'url': 'https://re.public.polimi.it/retrieve/e0c31c0c-20c2-4599-e053-1705fe0aef77/AURO2016.pdf',
     'quote': ['With recurrent connectivity, robots have to connect with each other and with the BS each time they gather new '
               'information. This entails an online constraint scheme, where robots can disconnect for arbitrarily long '
               'periods, but they must be able to coordinate in order to report to the base station as soon as new '
               'information is acquired.',
               'Hollinger and Singh (2012) consider a general mission scenario in which robots must synchronously regain '
               'global connectivity with the BS after a fixed time interval.'],
     'raw_file': T + 'banfi_auro2018_polimi.txt',
     'agent_note': 'States P1 with the clock contrast drawn explicitly: the reconnection requirement is keyed to new '
                   'information (each new observation), not to a fixed time interval (periodic connectivity), and the '
                   'disconnection may be arbitrarily long in clock time. The unit is one new observation at an assigned '
                   'location.'},
    {'id': 'r2a:10', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Banfi et al. (Autonomous Robots 2018), description of the Utility strategy of Spirin, Cameron and de Hoog '
               '(TAROS 2013) used as its baseline',
     'version': 'author manuscript (file AURO2016.pdf), PoliMi repository (fetched 2026-09-30)',
     'url': 'https://re.public.polimi.it/retrieve/e0c31c0c-20c2-4599-e053-1705fe0aef77/AURO2016.pdf',
     'quote': ['In (Spirin et al, 2013), the robots’ behavior is regulated by a utility function, which considers the amount '
               'of information not delivered yet by a robot to the BS and the predicted amount of information known by the '
               'BS.',
               'Utility defines a distributed strategy where each robot chooses autonomously which frontier to explore in a '
               'greedy fashion and returns to the BS as soon as the ratio between the area supposed to be known at the BS '
               'and that known by the robot goes below a predefined value',
               'In our experiments, we set r = 0.5 to obtain a balanced, yet more exploration-prone, behavior.'],
     'raw_file': T + 'banfi_auro2018_polimi.txt',
     'agent_note': 'States P1 (as implemented in MRESim and re-run by Banfi et al.): return to base is triggered when the '
                   'information the robot holds but has not delivered grows relative to what the base knows (a ratio '
                   'threshold r; r = 0.5 in their runs). Second-hand but by users who ran the code; the primary abstract is '
                   'r2a:11.'},
    {'id': 'r2a:11', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Spirin, Cameron, de Hoog, "Time Preference for Information in Multi-agent Exploration with Limited '
               'Communication" (TAROS 2013, LNCS 8069, pp. 34-45, Springer 2014, doi 10.1007/978-3-662-43645-5_5)',
     'version': 'Springer chapter page, abstract only (full text paywalled; no open copy found by Semantic Scholar or '
                'OpenAlex on 2026-09-30)',
     'url': 'https://link.springer.com/chapter/10.1007/978-3-662-43645-5_5',
     'quote': ['in which agents choose their actions based on the time preference of the base station for information, which '
               'it encodes as the desired minimum ratio of base station utility to total agent utility.',
               'We then show that our approach performs competitively with existing exploration algorithms while offering '
               'additional flexibility'],
     'raw_file': T + 'spirin_taros2013_springer_page.txt',
     'agent_note': 'States P1 (primary source, abstract): the return decision is set by a minimum ratio of information at the '
                   'base to information held by the agents, i.e. by undelivered information, not by a timer. The full '
                   'text (its comparisons) could not be read on the day.'},
    {'id': 'r2a:12', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Banfi et al. (Autonomous Robots 2018), on the Utility strategy (Spirin et al. 2013) against role-based '
               'exploration (de Hoog et al.)',
     'version': 'author manuscript (file AURO2016.pdf), PoliMi repository (fetched 2026-09-30)',
     'url': 'https://re.public.polimi.it/retrieve/e0c31c0c-20c2-4599-e053-1705fe0aef77/AURO2016.pdf',
     'quote': ['We compare against it since it has been shown to complete exploration faster than the role-based strategy of '
               'de Hoog et al (2009)',
               'Note that this strategy does not embed the recurrent connectivity constraint, so robots can remain '
               'disconnected from the BS for an unpredictably long amount of time and are thus expected to explore more '
               'freely.'],
     'raw_file': T + 'banfi_auro2018_polimi.txt',
     'agent_note': 'Close for P2: a second-hand report that the undelivered-information return rule completed exploration '
                   'faster than role-based exploration, whose explorers return on a timed rendezvous schedule (de Hoog et '
                   'al. 2010, dossier context). The metric is exploration time, not artifacts at equal return failure, and '
                   'the comparator is a planned schedule rather than a fixed homing timer.'},
    {'id': 'r2a:13', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Guo, Zavlanos, "Multi-Robot Data Gathering Under Buffer Constraints and Intermittent Communication" '
               '(arXiv:1706.02092; IEEE T-RO 2018 per the citing NeBula addendum, venue not verified on the day)',
     'version': 'arXiv v2, 30 Oct 2017 (v1 7 Jun 2017)', 'url': 'https://arxiv.org/abs/1706.02092v2',
     'quote': ['All robots have a limited buffer to store the data. Thus the data gathered by source robots should be '
               'transferred to relay robots before their buffers overflow, respecting at the same time limited '
               'communication range for all robots.',
               'setting a buffer limit has the advantage that it forces the robots to relay the gathered data to the data '
               'center more frequently, before this limit is reached.',
               'Note that imposing time constraints (compared to buffer constraints that indirectly model urgency to '
               'deliver data) would change completely the problem formulation addressed in this paper and is part of our '
               'future work.'],
     'raw_file': T + 'pdf_1706.02092v2.txt',
     'agent_note': 'States P1 in a formal setting: each out-of-contact interval of a data-gathering robot is bounded by the '
                   'data it has gathered since the last transfer (the next meeting is scheduled at the first plan state '
                   'where the buffer would overflow), and the authors set this against a time constraint by name. No clock '
                   'comparison is run.'},
    # ------------------------------------------------ the relay decision driven by unreported information, compared with fixed schedules
    {'id': 'r2a:14', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Kim, Baek, Corah, Best, Moon, Scherer, "PRoID: Predicted Rate of Information Delivery in Multi-Robot '
               'Exploration and Relaying" (arXiv:2604.10433)',
     'version': 'arXiv v1, 12 Apr 2026 (the only version)', 'url': 'https://arxiv.org/abs/2604.10433v1',
     'quote': ['The central challenge is deciding when each robot should stop exploring and relay: this depends on what the '
               'robot is likely to find ahead, what information it uniquely holds, and whether immediate or future delivery '
               'is more valuable.',
               'We define RoID as the ratio of novel, reportable information to the estimated travel time back to the base '
               'station.',
               'under which the robot terminates exploration and initiates relay to the base station.',
               'Others trigger relay based on fixed information thresholds [11].'],
     'raw_file': T + 'pdf_2604.10433v1.txt',
     'agent_note': 'States P1: the return (relay) trigger is built on the information the robot holds and has not reported '
                   'since its last delivery (I_unreported over the travel time home), compared with a predicted rate '
                   'including learned map prediction of what lies ahead (rule Gamma_now > alpha * Gamma_pred). The paper '
                   'also names the pure fixed-information-threshold relay trigger (C-R2\'s form) as prior work: Clark et al., '
                   'RA-L 2021 (r2a:19), and criticises it for not scaling relay overhead with environment size.'},
    {'id': 'r2a:15', 'position': 'P2', 'reading': 'states', 'reading_by': RB,
     'source': 'Kim et al., PRoID (arXiv:2604.10433), baselines and results',
     'version': 'arXiv v1, 12 Apr 2026', 'url': 'https://arxiv.org/abs/2604.10433v1',
     'quote': ['Periodic Relay: Each robot relays to the base station at a fixed interval P, then resumes exploration. We '
               'evaluate P ∈{100,200,300} timesteps.',
               'PRoID outperforms the best periodic baseline (P = 300) by 11.8, 12.4, 10.5, and 7.8 percentage points at n '
               '= 2,3,4,5 respectively, and outperforms Final Relay Only by 1.3, 3.4, and 2.1 percentage points at n = '
               '3,4,5. At n = 2, Final Relay Only is marginally competitive (58.4% vs. 58.2%)',
               'Against the best periodic baseline (P = 300), PRoID-Safe achieves gains of 9.8 and 12.2 percentage points '
               'at n = 3 and n = 5 under λ = 1100, and 8.6 and 10.6 percentage points under the harsher λ = 900 '
               'condition.'],
     'raw_file': T + 'pdf_2604.10433v1.txt',
     'agent_note': 'States P2: an information-driven relay rule against the best fixed-interval relay (P in {100, 200, 300} '
                   'timesteps) and against exploring until the deadline (mission-time homing), scored as the coverage that '
                   'reached the base station, with robot failures modelled (lost robots lose undelivered data). It wins by '
                   '7.8-12.4 points against the best interval; against final-relay-only it wins at n = 3-5 but not at n = 2 '
                   '(58.2 vs 58.4). Differences from C-R2: the rule adds a learned map prediction, and the fixed interval '
                   'was swept on the same test maps, not tuned on other maps.'},
    {'id': 'r2a:16', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Zijlstra, Aplin, Hunt, "Multi-Robot Strategies for Communication-Constrained Exploration and Electrostatic '
               'Anomaly Characterization" (arXiv:2405.00586; iSpaRo 2024, doi 10.1109/iSpaRo60631.2024.10687957 per arXiv)',
     'version': 'arXiv v1, 1 May 2024 (the only version)', 'url': 'https://arxiv.org/abs/2405.00586v1',
     'quote': ['Every time a new cell is “seen” the robot gains data',
               'To determine when to go back and transfer a variable called ‘connectionTime’ is used. This is simply a '
               'threshold cap on the amount of new data the robot can receive, and in simulation, the lower the value the '
               'more often the robot will go back and transfer.',
               'Similar to the fixed base station system, the robot will decide to rendezvous when hitting a threshold '
               'called ‘connectionTime’.'],
     'raw_file': T + 'pdf_2405.00586v1.txt',
     'agent_note': 'States P1, almost literally C-R2\'s rule: the robot goes back to the base (or calls a rendezvous) when '
                   'the new data gathered since the last transfer reaches a fixed cap (despite the parameter\'s name, it is '
                   'a data count). No clock comparator; the study compares base-station and rendezvous architectures.'},
    {'id': 'r2a:17', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Tan, Ma, Liang, Chng, Cao, Sartoretti, "IR2: Implicit Rendezvous for Robotic Exploration Teams under Sparse '
               'Intermittent Connectivity" (arXiv:2409.04730)',
     'version': 'arXiv v3, 21 Oct 2025 (v1 7 Sep 2024)', 'url': 'https://arxiv.org/abs/2409.04730v3',
     'quote': ['IR2 allows robots to effectively reason about the longer-term trade-offs between disconnecting for solo '
               'exploration and reconnecting for information sharing.',
               'Second, the map-surplus utility si,j indicates how much additional map information a robot believes it '
               'possesses relative to other robots.',
               '∆Mmin the minimum map area difference to consider a non-zero si,j'],
     'raw_file': T + 'pdf_2409.04730v3.txt',
     'agent_note': 'Close: the reconnection drive is the map information a robot holds beyond its teammates (accumulated '
                   'since the last exchange), switched on above a minimum surplus, but it enters a learned policy as an '
                   'observation and a reward term, not as a stated trigger; the reconnection is inter-robot, not to a base.'},
    {'id': 'r2a:18', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Tan et al., IR2 (arXiv:2409.04730), comparison with a preplanned rendezvous at a fixed time budget',
     'version': 'arXiv v3, 21 Oct 2025', 'url': 'https://arxiv.org/abs/2409.04730v3',
     'quote': ['On the other hand, Preplanned involves robots agreeing on and adhering to a specified exploration time budget '
               'and rendezvous location. For Preplanned, the time budget is pre-set and constant',
               'For distance efficiency, we notice that IR2 outperforms Preplanned and Pursuit in all environments, by at '
               'least 27.0% and 6.6% respectively, except for the 2-robot Forest and Campus tests.'],
     'raw_file': T + 'pdf_2409.04730v3.txt',
     'agent_note': 'Close for P2: an information-surplus-driven (learned) reconnection beats a constant pre-set time budget '
                   'by at least 27.0% in distance efficiency, with stated exceptions (2 robots, open maps). The metric is '
                   'exploration efficiency, not artifacts at equal return failure, and no failures are modelled.'},
    {'id': 'r2a:19', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Clark, Galante, Krishnamachari, Psounis, "A Queue-Stabilizing Framework for Networked Multi-Robot '
               'Exploration" (IEEE RA-L 6(2):2091-2098, 2021, doi 10.1109/LRA.2021.3061304)',
     'version': 'abstract only, from the Semantic Scholar API record (full text paywalled; openAccessPdf CLOSED on Semantic '
                'Scholar and OpenAlex, no arXiv version, 2026-09-30)',
     'url': 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/LRA.2021.3061304',
     'quote': ['Robots explore autonomously and can store data locally in their queues.',
               'Because robots may fail in a non-deterministic manner, causing loss of the data in their queues, enabling '
               'communication is important.',
               'The result is a distributed online controller which autonomously and strategically breaks and restores '
               'connectivity as needed.',
               'achieve better coverage than two state of the art approaches.'],
     'raw_file': T + 'clark2021_s2_api.txt',
     'agent_note': 'Close (abstract only): breaking and restoring connectivity is driven by the data queued on each robot '
                   '(undelivered information, lost if the robot fails) under Lyapunov virtual-queue constraints that also '
                   'include queueing delay. PRoID (r2a:14) describes it as relay triggered by fixed information thresholds; '
                   'the exact rule and the two compared approaches could not be read on the day.'},
    {'id': 'r2a:20', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Zhang, Chen, Zhu, Luo, Guo, "CoCoPlan: Adaptive Coordination and Communication for Multi-robot Systems in '
               'Dynamic and Unknown Environments" (arXiv:2601.10116; IEEE RA-L 11(3):3270-3277, March 2026 per arXiv)',
     'version': 'arXiv v1, 15 Jan 2026 (the only version)', 'url': 'https://arxiv.org/abs/2601.10116v1',
     'quote': ['(I) FIX triggers planning when accumulated tasks reach a threshold N, and is adapted to enforce temporal '
               'constraints.',
               '(IV) FIMR [6] plans at regular intervals Tc, used only for communication optimization to preserve '
               'adaptivity.',
               'SubT FIX (N=3) 74.7±3.1 34.0±0.0 22.2±10.4 2.6±4.8 FIX (N=10) 95.3±6.6',
               'FIMR (Tc “ 35) 96.0±5.0', 'FIMR (Tc “ 80) 87.7±4.0',
               'Caves FIX (N=3) 81.7±5.9 34.7±0.4 21.6±11.6 2.6±5.2 FIX (N=10) 95.7±4.8',
               'FIMR (Tc “ 35) 83.7±4.5', 'FIMR (Tc “ 80) 90.7±6.8',
               'Greedy yields the lowest mean efficiency, and FIX with N “ 10 exhibits high variance, underscoring the '
               'weakness of fixed thresholds.'],
     'raw_file': T + 'pdf_2601.10116v1.txt',
     'agent_note': 'Close for P2, and mixed: team-wide communication events (not returns from an excursion) triggered by '
                   'accumulated progress (N finished tasks, FIX) against a fixed interval (Tc seconds, FIMR), both as '
                   'baselines, finished tasks as the metric ("“" is the PDF extraction of "="). With N = 10 the progress '
                   'trigger ties the best interval in SubT (95.3 vs 96.0) and beats both intervals in Caves (95.7 vs 83.7 '
                   'and 90.7); with N = 3 it is behind both intervals in SubT and behind Tc = 80 in Caves. Each fixed '
                   'threshold, on either clock, is sensitive to its setting; the authors\' adaptive planner beats both.'},
]
