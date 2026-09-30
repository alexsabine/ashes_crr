"""Claims for ROB1 stage 3 (Robotics/DECLARATION.md), candidate C-R2 (Robotics/CRR_READING.md, r1-B5), searcher B:
an own-progress budget for out-of-contact exploration. Searcher B worked independently of searcher A
(Robotics/checks/claims_s3_r2a.py), read A's claims first, and then searched other communities and terms: control theory
(event-based against periodic sampling and transmission), the underwater and space literature, patents, fielded mine-mapping
drones, SubT team papers that A did not read (CSIRO Data61 and Team Explorer), networking (queue-driven robotic ferrying), and
full texts that A could reach only as abstracts (Clark et al., RA-L 2021, from the first author's site).

Transcribed from the dossier docs/citations/rob1_s3_r2b_2026-09-30.md. Sources were fetched 2026-09-30. Raw files and extracted
texts are held outside the repository under /tmp/claude-0/rob_s3/, named in `raw_file` relative to that root, with
r2b/SHA256SUMS.txt beside them. Every quote is copied from a dossier blockquote. Each quote was checked verbatim against its
extracted text with Robotics/checks/verify.py's matcher (claim_status, root /tmp/claude-0/rob_s3) before this file was
final.

The mechanism searched (CRR_READING.md, C-R2): bound an out-of-communication excursion (exploration beyond radio range,
lost-link behaviour, return to comms) by the robot's own progress, that is, the information it has gathered since the last
contact (information gain, map growth, novelty, unreported data, artifact count). The frontier's alternative is a wall-clock
homing timer or the remaining mission time. CRR's prediction: more artifacts found per mission at an equal rate of failures to
return, against the best fixed timer tuned on other maps.

Positions (the caller's):
  P1  a return or rendezvous decision triggered by information or progress accumulated since the last contact is published;
  P2  it is compared with a fixed time budget and shown better (more coverage or artifacts at equal loss or return failure);
  P3  it is used in a fielded system (DARPA SubT teams, mine-mapping drones).

Reading policy: searcher A's, copied unchanged so that the two searches grade alike. It was fixed before any reading below
was written.
  states       the source publishes the position as stated. For P1: a return, relay, reconnection or rendezvous rule whose
               trigger or bound is a quantity of information or progress accumulated since the last contact (unreported
               data in a buffer, new observations, unshared map area, artifact count, a ratio of delivered to held
               information). For P2: such a rule measured against a clock rule and reported better. For P3: such a rule
               configured on a system run in the field or in a competition;
  close        a nearby mechanism that differs in one named respect:
                 - the accumulated information is one input to a learned or optimised policy rather than a stated trigger;
                 - the rule is described only second-hand or only in an abstract;
                 - the quantity is monitored but the trigger is not stated;
                 - the comparison is in a neighbouring setting (team communication events, sampling or transmission in
                   feedback control, acoustic transmissions) or on a different metric, or it is mixed;
  contradicts  the source shows the mechanism (or its limiting case) fails or is inferior to a clock rule.
Clock-only sources (the frontier's side: homing timers, lost-link timeouts, periodic uploads) are listed in the dossier as
context and are not claims. 'Not found' is never 'novel'.

READING_CHECKS holds searcher B's check of each of searcher A's readings: is 'states' (or 'close') justified by A's quote?
It was written after reading A's quotes in their extracted texts.
"""

RB = "stage-3 agent (searcher B); for the investigator's review"
T = 'r2b/txt/'

CLAIMS = [
    # ------------------------------------------------ Clark et al., full text (A had the abstract only: r2a:19)
    {'id': 'r2b:1', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Clark, Galante, Krishnamachari, Psounis, "A Queue-Stabilizing Framework for Networked Multi-Robot '
               'Exploration" (IEEE RA-L 6(2):2091-2098, 2021, doi 10.1109/LRA.2021.3061304), the Time Preference (TP) '
               'comparator, implemented from Spirin et al. (TAROS 2013)',
     'version': "author copy on the first author's site (pdfTeX, created 15 Apr 2021; no arXiv version); a search listing "
                'shows a "Correction to" notice for this paper (not read; its venue and date were not verified)',
     'url': 'https://lillyclark.github.io/files/Queue_Stabilizing_Framework.pdf',
     'quote': ['The closest work to ours is the work by Spirin et al. [28], which introduces a constraint on the ratio of '
               'information at the data sink and a crude approximation of total information across all mobile robots. '
               'Based on this constraint, robots choose a role-based controller (explore or return to the data sink).',
               'Time Preference (TP): This controller presented by Spirin et al. uses a target ratio ρ comparing the queue '
               'to the map size [28].',
               'where |mr(t)| is the number of visited cells, robots choose αr(t) ∈Ar(t) to minimize Y (αr(t)). Otherwise '
               'robots choose αr(t) ∈Ar(t) to minimize ∥αr(t) −D∥mr(t).'],
     'raw_file': T + 'clark_queue_stabilizing_lillyclark.txt',
     'agent_note': 'States P1. The full text gives the undelivered-information return rule as a formula, and the authors '
                   'implemented and ran it: the robot explores while 1 - q_r/|m_r| >= rho, where q_r is its untransferred '
                   'data queue and |m_r| its map size. Otherwise it heads for the data sink D. This is a ratio of delivered '
                   'to held information, one of the forms named in the policy. It settles what A could read only from '
                   "Spirin's abstract (r2a:11) and Clark's abstract (r2a:19). The paper's runs use rho = 0.35 and 0.99 "
                   '(Fig. 2 caption).'},
    {'id': 'r2b:2', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': "Clark et al., RA-L 2021, the queue-stabilizing (QS) controller's own mechanism",
     'version': "author copy on the first author's site (created 15 Apr 2021)",
     'url': 'https://lillyclark.github.io/files/Queue_Stabilizing_Framework.pdf',
     'quote': ['The crux of our approach is that a backlog in the data queue puts pressure on the robot to transmit this '
               'data and therefore move to recover a communication path to the data sink.',
               'We now introduce a queue qr(t) of untransferred data stored at robot r with the following dynamics:',
               'We assume Pr(Xi = 0) = Pr(Xi = 1), so the number of cells visited is the reduction in map entropy.',
               'But this approach assigns a utility to connectivity which does not depend on whether or not there is new '
               'information to share.'],
     'raw_file': T + 'clark_queue_stabilizing_lillyclark.txt',
     'agent_note': 'Close, and the nearest in units. The return pressure is the untransferred information itself: the queue '
                   'grows by the mutual information gained, I(alpha; m), which equals the reduction in map entropy. But it '
                   'drives a Lyapunov drift-plus-penalty controller rather than a stated threshold. It also acts through a '
                   'virtual delay queue that adds q_r at every step (information times waiting time), so it mixes the '
                   "robot's information with the clock. The paper draws C-R2's contrast itself: it criticises a "
                   'connectivity utility that does not depend on new information.'},
    {'id': 'r2b:3', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Clark et al., RA-L 2021, simulation results (coverage at the data sink)',
     'version': "author copy on the first author's site (created 15 Apr 2021)",
     'url': 'https://lillyclark.github.io/files/Queue_Stabilizing_Framework.pdf',
     'quote': ['QS outperforms UN, SC, and MO and slightly outperforms TP with respect to map coverage.',
               'MO can achieve the highest localizability (when minimizing CRB is the sole or primary objective), but '
               'suffers with respect to coverage from not adapting to the amount of untransferred data.',
               'This finding emphasizes that the choice of kq, kQ, kZ, kY which maximizes coverage depends on '
               'characteristics of the environment (see Table I).'],
     'raw_file': T + 'clark_queue_stabilizing_lillyclark.txt',
     'agent_note': 'Close for P2. The two rules that adapt to untransferred information (QS, and TP from Spirin et al.) '
                   'deliver more map to the sink than a fixed-weight connectivity objective (MO, after Benavides et al.). '
                   'The metric is map coverage at the data sink, averaged over six trials. None of the compared arms is a '
                   'time budget, so this is not the clock comparison P2 asks for. The best weights depend on the '
                   'environment (Table I). That is the tuning-transfer problem that C-R2 wants settled by tuning on other '
                   'maps.'},
    # ------------------------------------------------ Team CSIRO Data61 (SubT): stated in words; the fielded Urban rule was a clock
    {'id': 'r2b:4', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Hudson, Talbot, Cox, Williams, Hines, Pitt, Wood, Frousheger, ... O\'Brien, Jiang, Chen, Arkin (34 authors '
               'per the arXiv record; Team CSIRO Data61), "Heterogeneous Ground and Air Platforms, Homogeneous Sensing: '
               'Team CSIRO Data61\'s Approach to the DARPA Subterranean Challenge" (arXiv:2104.09053; Field Robotics 2, '
               '2022 per the arXiv journal reference)',
     'version': 'arXiv v1, 19 Apr 2021 (the only version)', 'url': 'https://arxiv.org/abs/2104.09053v1',
     'quote': ['If an agent, or group of agents, is disconnected from the base station and they accumulate significant '
               'information, they will return to communication range either independently or coordinating through task '
               'allocation (Section 5.2).',
               'The core tasks defined and used so far are explore, drop-comms-node, and sync-data (for agents who are out '
               'of comms range). Each task has a reward, which is discounted by the expected time it would take an agent '
               'to complete the task.'],
     'raw_file': T + 'pdf_2104.09053v1.txt',
     'agent_note': 'Close. The return trigger is stated only in words ("accumulate significant information"), with no unit '
                   'or threshold. In the Cave-event task allocation it enters as a sync-data task inside a reward-based '
                   "auction. The same team's detailed Urban-circuit paper (Williams et al., MFI 2020; dossier section F) "
                   'gives the fielded explore-sync trigger as a clock: "After three minutes it drives back to '
                   'communication range".'},
    {'id': 'r2b:5', 'position': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'Hudson et al. (Team CSIRO Data61), arXiv:2104.09053, data sharing (Mule) and lessons from the Urban '
               'Circuit',
     'version': 'arXiv v1, 19 Apr 2021', 'url': 'https://arxiv.org/abs/2104.09053v1',
     'quote': ['This includes synchronisation status for each peer, making it possible for agents to decide if they should '
               'return to base to deliver mission-critical data, as was done at the Urban and Cave events.',
               'The interruption caused when robots returned to synchronise data was a significant issue, as robots often '
               'did not return to the area being explored.'],
     'raw_file': T + 'pdf_2104.09053v1.txt',
     'agent_note': 'Close for P3. Returning to deliver unsynchronised data was fielded at the Urban and Cave events. But the '
                   "rule that fired at Urban was the three-minute explore-sync timer (the team's MFI 2020 paper, section "
                   "F), and the Cave rule is a reward in the task auction, not a stated information unit. The team's "
                   'lesson is about the cost of returning at all: robots did not go back to the region they had left.'},
    # ------------------------------------------------ a granted patent: data-amount and map-progress triggers for return to range
    {'id': 'r2b:6', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Van Meeteren, Shyshkov, Bachiochi, Fratini, Parobek (Travelers Indemnity Co), "Systems and methods for '
               'autonomous hazardous area data collection", US 11,710,411 B2 (application US16/870,071, filed 8 May 2020, '
               'granted 25 Jul 2023; also published as US20210350713A1)',
     'version': 'Google Patents full text of US11710411B2 (fetched 2026-09-30; the USPTO image PDF has no text layer)',
     'url': 'https://patents.google.com/patent/US11710411B2/en',
     'quote': ['In some embodiments, the upload routine may be triggered by a passage of a predetermined amount of time, an '
               'acquisition of a predetermined amount of data, a generation of a predetermined percentage or portion of a '
               'model and/or map of the area 310 , and/or a completion of a data collection routine (or a portion '
               'thereof).',
               'The aerial vehicle 306 may, for example, attempt to transmit (e.g., via the transmitter 318 ) autonomous '
               'mapping data to the base station 302 once a discrete portion of the area 310 has been mapped (e.g., a '
               'particular room of a building) and/or once the memory 340 reaches a threshold level of storage (e.g., '
               'eighty percent (80%) full).',
               'In some embodiments, such as in the case that the autonomous vehicle is determined to be out of range '
               '(e.g., at 422 ), the method 400 may proceed to conduct a navigation to return to range, at 424 .',
               'In some embodiments, such as in the case that the autonomous vehicle is attempting to return to range to '
               'offload data as a waypoint during a continued autonomous data collection routine, both the path to the '
               'in-range location and the path to return to the data collection routine may be taken into account in '
               'selecting a desirable in-range point.'],
     'raw_file': T + 'gp_US11710411.txt',
     'agent_note': "States P1, in the patent literature, which A's search did not cover. An autonomous drone mapping a "
                   'hazardous area ends its out-of-range excursion and navigates back into range to upload. The triggers '
                   'are listed as alternatives: an amount of data acquired, a portion of the map generated, memory 80% '
                   'full, or "a passage of a predetermined amount of time". The data "pit stop" resumes collection '
                   'afterwards. The patent lists the clock and the progress triggers side by side and compares neither. '
                   'Independent claim 1 leaves the triggering event unspecified. The embodiments name the data and map '
                   'triggers.'},
    # ------------------------------------------------ fielded mine-mapping drones (P3's named example)
    {'id': 'r2b:7', 'position': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'International Mining, "Emesent builds mining connections as Hovermap autonomy takes off" (interview with '
               'Emesent CEO Dr Stefan Hrabar, 21 Sep 2020): the company\'s own statement',
     'version': 'web page, posted 21 Sep 2020 (fetched 2026-09-30)',
     'url': 'https://im-mining.com/2020/09/21/emesent-builds-mining-connections-hovermap-autonomy-takes-off/',
     'quote': ['Hovermap is smartly designed to operate beyond the communication range of the operator.',
               'Hovermap self-navigates towards the waypoint, avoiding obstacles and building the map as it goes. Once it '
               'reaches the waypoint (or if the waypoint is impossible to reach), it automatically returns back to the '
               'operator. The map data is stored onboard Hovermap and when it returns back to within Wi-Fi range the new '
               'map data is uploaded to the tablet.',
               'A number of mines have been using AL2 to map their stopes and other areas beyond line-of-sight.',
               'Other considerations are returning in a safe and efficient way when the battery is running low, or what to '
               'do if waypoints cannot be reached.'],
     'raw_file': T + 'immining_2020_emesent.txt',
     'agent_note': 'Close for P3. A fielded mine-mapping drone (Hovermap AL2, used at mines) bounds its out-of-comms '
                   'excursion by progress towards an operator-set goal: the waypoint is reached, or found unreachable. It '
                   'also returns on low battery. It does not use a homing timer, but the unit is a place chosen by the '
                   'operator, not the information gathered since the last contact reaching a threshold.'},
    {'id': 'r2b:8', 'position': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'Emesent, "Emesent enables fully autonomous exploration and mapping of GPS-denied environments with latest '
               'Cortex and Commander releases" (press release, 29 Apr 2025)',
     'version': 'web page dated 29 Apr 2025 in its URL (fetched 2026-09-30)',
     'url': 'https://www.emesent.com/news/2025/04/29/emesent-enables-fully-autonomous-exploration-and-mapping-of-gps-'
            'denied-environments-with-latest-cortex-and-commander-releases',
     'quote': ['No need to set waypoints to plan a mission – simply designate a volume bounding box using Commander and '
               'Hovermap will autonomously explore the volume to map it completely and return to home.',
               'allowing surveyors to build an accurate picture of an unknown target area that’s beyond line of sight and '
               'communications range.'],
     'raw_file': T + 'emesent_2025_cortex.txt',
     'agent_note': 'Close for P3. The 2025 product ends the beyond-comms excursion when the designated volume is mapped '
                   'completely, that is, when exploration progress is complete (the frontier is exhausted). There is no '
                   'information unit per excursion; the whole task is one excursion. The 2020 release adds "automatic '
                   'return to home on low battery" (section F).'},
    {'id': 'r2b:9', 'position': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'Exyn Technologies, "How Do You Define Autonomy Level 4B?" (company web page): the company\'s own statement',
     'version': 'web page, undated (refers to 2021 as past; fetched 2026-09-30)',
     'url': 'https://www.exyn.com/news/how-do-you-define-autonomy-level-4b',
     'quote': ['our proprietary SLAM algorithm, ExynAI, is completely self-reliant for open-ended exploration and does not '
               'require any human interaction during flight to complete its mission.',
               'That fearless attitude to explore until the mission is complete or the battery is spent is unlike a human '
               'operator flying in an underground or unknown environment, especially beyond visual line of sight.'],
     'raw_file': T + 'exyn_level4b.txt',
     'agent_note': "Close for P3. The second fielded mine-mapping drone's excursion is bounded by mission completion or "
                   'battery, not by a homing timer. Neither is information accumulated since the last contact reaching a '
                   'unit.'},
    {'id': 'r2b:10', 'position': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'Ackerman, "Exyn Brings Level 4 Autonomy to Drones" (IEEE Spectrum, 27 Apr 2021), describing ExynAI with '
               "quotes from Exyn's CTO",
     'version': 'web article dated 27 Apr 2021 (fetched 2026-09-30)',
     'url': 'https://spectrum.ieee.org/exyn-brings-level-4-autonomy-to-drones',
     'quote': ['No GPS , no base station, no communications, no prior understanding of the space, nothing.',
               'You tell the drone where you want it to map, and it’ll take off and then decide on its own where and how '
               'to explore the space that it’s in, building up an obscenely high resolution lidar map as it goes and '
               'continuously expanding that map until it runs out of unexplored areas, at which point it’ll follow the '
               'map back home and land itself.'],
     'raw_file': T + 'spectrum_exyn_2021.txt',
     'agent_note': 'Close for P3 (a secondary source: a journalist\'s description). The return is triggered by the '
                   'information frontier running out ("until it runs out of unexplored areas"). That is the zero-rate '
                   'limit of an information trigger, reached once per mission. It is not a unit of information per '
                   'excursion.'},
    # ------------------------------------------------ control theory: own-change triggering against the clock at equal rate
    {'id': 'r2b:11', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Åström, Bernhardsson, "Comparison of Periodic and Event Based Sampling for First-Order Stochastic Systems" '
               '(14th IFAC World Congress, Beijing, 1999; the extended CDC 2002 version is "Comparison of Riemann and '
               'Lebesgue sampling for first order stochastic systems")',
     'version': 'Lund University Research Portal copy, file 8520116.pdf (IFAC 1999 paper; fetched 2026-09-30)',
     'url': 'https://lup.lub.lu.se/search/files/6208782/8520116.pdf',
     'quote': ['One possibility is to sample the system when the output has changed with a specified amount.',
               'The analysis shows that event based sampling gives better performance than periodic sampling.',
               'Another way to say this is that one must sample 4.7 times faster with Riemann sampling to get the same '
               'mean error variance.',
               'The figure shows that Lebesgue sampling gives substantially smaller variances for the same average '
               'sampling rates.'],
     'raw_file': T + 'astrom_lund_8520116.txt',
     'agent_note': "Close for P2, in a neighbouring setting: sampling in feedback control, not a robot's excursion. It is "
                   "the foundational form of C-R2's comparison. The contact event fires when the system's own change since "
                   'the last contact reaches a set amount, and it is compared with a clock at an equal average rate. The '
                   'own-change trigger wins (a variance ratio of 4.7 for the integrator). The record already names '
                   'event-triggered control as an established literature (DECLARATION.md).'},
    {'id': 'r2b:12', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Antunes, Hespanha, "Event-triggered control cannot improve the ℓ2 gain of h∞ optimal periodic control and '
               'transmit at a smaller average rate" (arXiv:2310.17033)',
     'version': 'arXiv v1, 25 Oct 2023 (the only version; IEEE TAC per the file name of the authors\' web copy, venue not '
                'verified on the day)',
     'url': 'https://arxiv.org/abs/2310.17033v1',
     'quote': ['We show that, under mild assumptions, there does not exist a controller and scheduler pair that strictly '
               'improves the optimal attenuation bound of periodic control with a smaller average transmission rate.',
               'In the h2 control setting, closely related to Linear Quadratic Gaussian Control (LQG), performance is '
               'measured by an average quadratic cost. Considered in this setting, ETC can (strictly) improve the average '
               'quadratic cost of optimal periodic control for the same, and even smaller, transmission rate;'],
     'raw_file': T + 'pdf_2310.17033v1.txt',
     'agent_note': 'Close for P2, in the same neighbouring setting as r2b:11, and it cuts the other way. Against a '
                   'worst-case (l2-gain) metric, no event trigger beats the best periodic schedule with fewer '
                   'transmissions. Against an average (h2) metric, event triggers can win. Whether an own-change trigger '
                   'beats the clock at equal rate depends on the metric. C-R2 is scored on a mean (artifacts per mission) '
                   'at an equal rate of failures, which is the favourable case.'},
    # ------------------------------------------------ underwater: surfacing on own uncertainty; event-vs-periodic acoustic transmission
    {'id': 'r2b:13', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Fernandes, Sahoo, Kothari, "Cooperative Localization for Autonomous Underwater Vehicles -- a comprehensive '
               'review" (arXiv:2307.06189), describing its reference [147] (location-confidence surfacing)',
     'version': 'arXiv v1, 12 Jul 2023 (the only version)', 'url': 'https://arxiv.org/abs/2307.06189v1',
     'quote': ['In [147], an approach that uses a measure of each AUV’s confidence of location (LC) estimate to fuse relative '
               'pose information through KF for reducing localization error is presented. When LC is below a limit for '
               'any of the swarm members, they return to the surface for a GPS fix.',
               'periodically surface for a GPS fix.'],
     'raw_file': T + 'pdf_2307.06189v1.txt',
     'agent_note': 'Close (second-hand, in a review). The return to contact (surfacing) is triggered by an accumulated own '
                   "quantity: the vehicle's location confidence falling below a limit. The clock alternative is named in "
                   'the same review (periodic surfacing). The quantity is navigation uncertainty, not information gathered, '
                   'so this is the H-L5 reading of drift rather than C-R2 as stated.'},
    {'id': 'r2b:14', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Fernandes, Sahoo, Kothari (arXiv:2307.06189), describing Meira et al. (its reference [87]): threshold-'
               'triggered against periodic acoustic transmission',
     'version': 'arXiv v1, 12 Jul 2023', 'url': 'https://arxiv.org/abs/2307.06189v1',
     'quote': ['In [87], Meira et al. coupled CL algorithm from [47] with a logic-based communication approach that transmits '
               'location information from ASV to AUV depending on a threshold instead of a pre-determined periodic '
               'transmission.',
               'It was demonstrated that the approach gives only marginally worse performance than periodic transmission '
               'but with almost 62.5% fewer transmissions.'],
     'raw_file': T + 'pdf_2307.06189v1.txt',
     'agent_note': 'Close for P2, and mixed (second-hand, neighbouring setting). A change-triggered transmission against a '
                   'periodic one: marginally worse accuracy at about 62.5% fewer transmissions. That is not a comparison at '
                   'an equal rate.'},
    # ------------------------------------------------ networking: queue-driven robotic ferrying (the lineage of Clark et al.)
    {'id': 'r2b:15', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Wang, Gasparri, Krishnamachari, "Robotic Message Ferrying for Wireless Networks using Coarse-Grained '
               'Backpressure Control" (arXiv:1308.2923)',
     'version': 'arXiv v1, 13 Aug 2013 (the only version)', 'url': 'https://arxiv.org/abs/1308.2923v1',
     'quote': ['In CBMF, the robots are matched to sources and sinks once every epoch to maximize a queue-differential-based '
               'weight. The matching controls both motion and transmission for each robot: if a robot is matched to a '
               'source, it moves towards that source and collects data from it; and if it is matched to a sink, it moves '
               'towards that sink and transmits data to it.'],
     'raw_file': T + 'pdf_1308.2923v1.txt',
     'agent_note': "Close. A robot's move to a sink (its return to deliver) is chosen by queue backlogs, that is, by data "
                   'held and not yet delivered. But the decisions are taken once per epoch of fixed length (a clock), the '
                   'setting is ferrying between static nodes rather than exploration, and the rule is a max-weight '
                   'matching rather than a threshold.'},
    # ------------------------------------------------ intermittent-connectivity planning (Caltech; CoSTAR-motivated)
    {'id': 'r2b:16', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Klaesson, Nilsson, Ames, Murray, "Intermittent Connectivity for Exploration in Communication-Constrained '
               'Multi-Agent Systems" (arXiv:1911.08626)',
     'version': 'arXiv v1, 19 Nov 2019 (the only version)', 'url': 'https://arxiv.org/abs/1911.08626v1',
     'quote': ['For this reason we require that a static base station is periodically updated with the progress.',
               'Since we do not assume continuous connectivity it is necessary to synthesize a plan that gets agents to '
               'frontiers, and also a plan that distributes the new information to the base station when frontier '
               'exploration is finished.'],
     'raw_file': T + 'pdf_1911.08626v1.txt',
     'agent_note': 'Close. The new information is carried back to the base once each planned round of frontier exploration '
                   'ends: one frontier visit per round, planned in advance as an integer program. The excursion is bounded '
                   'by a planned spatial goal, not by accumulated information reaching a unit. The paper itself says '
                   '"periodically".'},
    # ------------------------------------------------ a 2025 survey: new-voxel count triggers map sharing (UAV teams)
    {'id': 'r2b:17', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Wang, Yu, Xu, Chen, Gao, Yang, Tang, Yu, Gao, Jian, Chen, Gao, Zhou, Wang, "Multi-Robot System for '
               'Cooperative Exploration in Unknown Environments: A Survey" (arXiv:2503.07278), describing its reference '
               '[94] (Zhang et al.)',
     'version': 'arXiv v3, 21 May 2025 (v1 10 Mar 2025)', 'url': 'https://arxiv.org/abs/2503.07278v3',
     'quote': ['Zhang et al. [94] introduced a system where each unmanned aerial vehicle (UAV) constructs a locally improved '
               'OctoMap. When the number of newly discovered [...] voxels exceeds a predefined threshold, a sub-map sharing '
               'mechanism is triggered.'],
     'raw_file': T + 'pdf_2503.07278v3.txt',
     'agent_note': 'Close (second-hand; a communication event, not a return). Map sharing between UAVs is triggered when '
                   'new information since the last share (a count of newly discovered voxels) reaches a threshold. That is '
                   "C-R2's trigger on a communication event rather than on a movement back into range. The \"[...]\" "
                   'spans a page header and a figure caption in the extracted text.'},
]

# searcher B's check of searcher A's readings (Robotics/checks/claims_s3_r2a.py), made against A's quotes in A's extracted
# texts (all 65 of A's quotes were re-found by the verify.py matcher on 2026-09-30)
READING_CHECKS = [
    {'claim_id': 'r2a:1', 'agree': True,
     'note': 'The quote states a return to comms when the undelivered-data buffer exceeds 300 KB. Caution: the buffer also '
             'grows under congestion inside comms, so it is undelivered data rather than data gathered since the last '
             "contact. ACHORD's own 60 s timeout is a clock."},
    {'claim_id': 'r2a:2', 'agree': True,
     'note': 'In context the evaluation is in the SubT Finals course (Fig. 6: "exploration of the DARPA SubT Finals '
             'competition environment, day 2"), and the lessons speak of returning to comms "sparingly". It is fielded. The '
             'paper does not show that the buffer trigger fired, as A notes.'},
    {'claim_id': 'r2a:3', 'agree': True,
     'note': "States P3, but the contrast with the clock is weak in this source. The same paper has a 10-minute rule, and the "
             'authors read a large buffer as a sign that the robot "has explored autonomously for a long period of time" '
             '(a proxy for time out of contact).'},
    {'claim_id': 'r2a:4', 'agree': True, 'note': 'Close: the artifact count is monitored beside the clock out of range; no '
                                                 'combining rule is stated.'},
    {'claim_id': 'r2a:5', 'agree': True,
     'note': 'The quote states the artifact-count trigger (3 unreported), with a clock backstop that starts at the first '
             'unreported artifact.'},
    {'claim_id': 'r2a:6', 'agree': True, 'note': '"as configured during the Final Event Prize Run" makes it fielded.'},
    {'claim_id': 'r2a:7', 'agree': True,
     'note': 'Checked in context: the report-on-artifact behaviour is part of Greedy Explore ("like the previous, when an '
             'artifact was detected, the robot entered Report mode"), and Greedy Explore "was used through all phases of '
             'the competition".'},
    {'claim_id': 'r2a:8', 'agree': True,
     'note': "The survey's own taxonomy names information-triggered and time-triggered reconnection as members of one class. "
             'That is a statement of P1 at the class level.'},
    {'claim_id': 'r2a:9', 'agree': True,
     'note': 'Borderline. Recurrent connectivity is a planning constraint at each assigned observation location (a unit of '
             'one observation, no accumulation), not a threshold on accumulated information. It is still a reconnection '
             'keyed to new information, as the quote says.'},
    {'claim_id': 'r2a:10', 'agree': True,
     'note': "The quote is the authors' own experimental setup (\"In our experiments, we set r = 0.5\"), so the rule was "
             "implemented and run, not only reported. A's own policy would read a merely second-hand report as close. "
             'Clark et al. (r2b:1) independently give the same rule in formula form and ran it too.'},
    {'claim_id': 'r2a:11', 'agree': False,
     'note': 'The abstract quote does not state a return trigger: "agents choose their actions based on" a desired minimum '
             "ratio. A's own policy reads an abstract-only source as close. The substance (a return when the ratio falls) is "
             'confirmed by Clark et al. (r2b:1) and Banfi et al. (r2a:10), so the grade is unchanged.'},
    {'claim_id': 'r2a:12', 'agree': True,
     'note': 'Close: second-hand, the metric is exploration time, and the comparator is a rendezvous schedule.'},
    {'claim_id': 'r2a:13', 'agree': True,
     'note': 'Caution: the data per gathering action, D_i(g), is known in the plan, so the buffer bound is a scheduled count. '
             'When information accrues predictably, a count bound and a time bound can be scheduled alike. That is '
             "C-R2's must-fail case, and this source does not separate the two."},
    {'claim_id': 'r2a:14', 'agree': True,
     'note': 'The trigger is stated (the unreported-information rate against a predicted rate). The learned map prediction is '
             'an addition, not a replacement, of the accumulated-information term.'},
    {'claim_id': 'r2a:15', 'agree': True,
     'note': 'States P2 in direction. Robot failures are modelled and delivered coverage is scored. Differences from C-R2 as '
             "A notes: a rate rule with learned prediction, intervals swept on the test maps, and the n = 2 exception "
             'against final-relay-only.'},
    {'claim_id': 'r2a:16', 'agree': True,
     'note': 'The quote defines the parameter as "a threshold cap on the amount of new data". That is the nearest to C-R2\'s '
             'literal rule.'},
    {'claim_id': 'r2a:17', 'agree': True, 'note': 'Close: the map surplus is an input to a learned policy.'},
    {'claim_id': 'r2a:18', 'agree': True,
     'note': 'Close: distance efficiency, no failures modelled, and the stated exceptions.'},
    {'claim_id': 'r2a:19', 'agree': True,
     'note': 'Close on the abstract alone. Now superseded by the full text (r2b:1 to r2b:3): the paper publishes the TP rule '
             'as an implemented comparator (states P1), its own controller is backlog-driven (close), and neither arm is '
             'compared with a clock.'},
    {'claim_id': 'r2a:20', 'agree': True,
     'note': 'Close and mixed. These are team communication events, not returns, and both thresholds are sensitive to their '
             'settings.'},
]
