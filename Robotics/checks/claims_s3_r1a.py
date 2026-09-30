"""Claims for ROB1 stage 3 (Robotics/DECLARATION.md), candidate C-R1 (Robotics/CRR_READING.md, r4-B4), searcher A:
a phase-keyed stop for a dynamically balancing legged or humanoid robot. Transcribed from the dossier
docs/citations/rob1_s3_r1a_2026-09-30.md (sources fetched 2026-09-30; raw files and extracted texts held outside the
repository under /tmp/claude-0/rob_s3/, named in `raw_file` relative to that root, with r1a/SHA256SUMS.txt beside them).
Every quote is copied from a dossier blockquote and was checked verbatim against its extracted text before this file was
written (normalisation as Robotics/checks/verify.py).

The mechanism searched (CRR_READING.md, C-R1): a stop (emergency stop, protective stop, safe stop, fall-safe stop) of a
dynamically balancing legged or humanoid robot that is initiated, timed or shaped by the gait's own phase (gait-phase-dependent
stopping, phase-aware stop trajectories, capture-point / stance-phase stopping, "stop at the next stance", phase-dependent
safe-state selection), as opposed to one stopping time on the clock sized by the worst gait phase (the frontier's assumption
in stage 1, harvester r4:32: S = K T + C with T the worst-case single-support stopping time). CRR's prediction: over stop
commands arriving uniformly in time, a phase-keyed stop has a lower worst case and a lower mean of stopping distance and falls,
at equal delay budget, than the best single clock-sized stop.

Positions (the caller's):
  P1  phase-dependent timing or shaping of a stop for a legged or humanoid robot is published;
  P2  it is shown to reduce worst-case or mean stopping distance, time or falls against a phase-independent stop;
  P3  it appears in a standard, a standards proposal or an industrial safety function (e.g. ISO 25785-1 drafts, IFR/industry
      white papers).

'reading' is decided by the stage-3 agent from the quote, for the investigator's review ('reading_by'). Reading policy,
fixed before the readings were written:
  states       P1: the source designs, implements or specifies a stop of a walking or balancing legged/humanoid robot
               (emergency, protective, safe or commanded stop) whose initiation, timing or shape is set by where the gait is
               in its cycle (support phase, swing state, the next touchdown or apex, the capture point against the base of
               support; the caller lists capture-point and stance-phase stopping as instances of C-R1);
               P2: a measured comparison (hardware or simulation) in which such a stop gives fewer falls, or a shorter
               stopping distance or time, than a phase-independent stop (immediate or clock-timed);
               P3: a standard, a standards draft or proposal, or an industrial safety function specifies phase-keyed timing
               or shaping of the stop;
  close        P1: the phase dependence of stopping is stated but no phase-keyed stop is designed; or the stop is conditioned
               on the robot's state but not keyed to the gait phase (learned stop policies, stoppability estimators,
               capturability constraints under a clock-timed stop); or an operational stop gated by the support state with a
               clock hysteresis; or the mechanism is shown in humans, not robots;
               P2: a state-dependent (not phase-keyed) stop decision compared with an unconditioned stop, or a qualitative
               claim of shorter stops with no measured phase-independent baseline;
               P3: a standard, proposal or industrial function that specifies a controlled (non-de-energising) stop or a
               stance/state-dependent safe state for legged robots without phase-keyed timing; or a manufacturer's patent of
               a phase-keyed stop with no evidence that it is a deployed or certified function;
  contradicts  P1/P2: the source shows a phase-keyed stop infeasible, no better or worse than a phase-independent stop;
               P3: the source documents a standard, a standards route or an industrial safety function that sizes or budgets
               the stop by one clock time independent of the gait phase (evidence against P3 for that standard or function;
               it cannot disprove existence elsewhere).
Grade (Robotics/DECLARATION.md stage 3): REDUNDANT, PARTLY REDUNDANT or NOT FOUND IN THE SWEEP, computed by the
investigator's grading script from these readings, not here. 'Not found' is never 'novel'.
"""

RB = "stage-3 agent (searcher A); for the investigator's review"
T = 'r1a/txt/'

CLAIMS = [
    # ------------------------------------------------ A. phase-keyed emergency stops of walking humanoids (P1)
    {'id': 'r1a:1', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Takahashi & Suzaki (Honda Giken Kogyo), "Emergency stop control system for mobile robot", US Patent 5,369,346 '
               '(filed 20 May 1993, priority JP 22 May 1992)',
     'version': 'US 5,369,346 A, granted 29 Nov 1994; USPTO image PDF fetched 2026-09-30, text by OCR (RapidOCR) of pages '
                '11-14, checked by eye against the page image for the quoted lines',
     'url': 'https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5369346',
     'quote': ['Further, if the robot is a legged mobile robot, its attitude is intrinsically unstable owing to the large '
               'changes that take place in the support polygon. The collision of such a robot with persons and objects '
               'cannot be reliably avoided simply by stopping it.',
               'It can thus be understood from the figure that the attitude of the biped walking robot is particularly '
               'unstable during one-leg support period.',
               'or not the ZMP is within the stable regions, whereby it [...] is determined whether or not the robot will be '
               'able to maintain its attitude in the stopped state if the emergency stop is executed.',
               'If the result of the determination is affirmative, control passes directly to step S118 in which walking or '
               'the robot motion is stopped, and if it [...] is negative, control passes to step S120 in which the walking '
               'speed is reduced and control is then returned to step S116.',
               'Steps 116 and 120 are then repeatedly executed until it is confirmed that a stable attitude has been reached '
               '(e.g. that the center of gravity is at the bottom [...] of the supporting foot), and control then passes to '
               'step S118.'],
     'raw_file': T + 'US5369346_ocr.txt',
     'agent_note': 'States P1, in 1992-94: on an emergency-stop signal the biped is not stopped at once; the controller checks '
                   'whether the current attitude (centre of gravity over the supporting foot, or ZMP inside the stable region, '
                   'which differs between one-leg and two-leg support) can hold a stopped state, and if not it keeps walking '
                   'at reduced speed until it can, then stops. The stop is timed by the gait\'s own state, not by a clock. '
                   'Not compared with an immediate or clock-timed stop.'},
    {'id': 'r1a:2', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Morisawa, Kajita, Harada, Fujiwara, Kanehiro, Kaneko & Hirukawa (AIST), "Emergency stop algorithm for walking '
               'humanoid robots", IEEE/RSJ IROS 2005, pp. 31-36 (DOI 10.1109/IROS.2005.1544955)',
     'version': 'IROS 2005 proceedings PDF (IEEE copyright line on p. 31); copy hosted by scispace.com, fetched 2026-09-30',
     'url': 'https://scispace.com/pdf/emergency-stop-algorithm-for-walking-humanoid-robots-1lkt3vh3zf.pdf',
     'quote': ['Since an emergency occurs at unpredictable timing and at any state of robot, the stopping motion must be '
               'generated in real-time.',
               'During the single support phase, a landing time and position are determined by evaluating the average '
               'velocity of the swing leg and the horizontal position of the COG. During the double support phase, the '
               'travel distance of the COG and the ZMP are evaluated.',
               'If the emergency signal is given in double support phase, the stop motion can also deal with the emergency '
               'by starting from ZMP Transition Phase.',
               'The stop motion generator postponed the touchdown time and extended the step length.'],
     'raw_file': T + 'morisawa2005_scispace.txt',
     'agent_note': 'States P1: the emergency stop of HRP-2 is shaped by the gait phase at which the signal arrives (from '
                   'single support it starts with a Landing phase whose touchdown time and position are re-planned; from '
                   'double support it starts at the ZMP Transition phase), and the stop completes within one step. Shown in '
                   'simulation from late single support and from double support, and on hardware from mid single support; '
                   'no stopping-distance table across phases.'},
    {'id': 'r1a:3', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Morisawa et al., "Emergency stop algorithm for walking humanoid robots" (IROS 2005), Introduction',
     'version': 'IROS 2005 proceedings PDF; copy hosted by scispace.com, fetched 2026-09-30',
     'url': 'https://scispace.com/pdf/emergency-stop-algorithm-for-walking-humanoid-robots-1lkt3vh3zf.pdf',
     'quote': ['However, these methods require more than two steps to stop the robot.',
               'In this paper, we propose a method to generate emergency stop motion in real-time which can lead the robot '
               'to stop within one step.'],
     'raw_file': T + 'morisawa2005_scispace.txt',
     'agent_note': 'Close for P2: the phase-shaped stop is said to stop within one step where earlier real-time pattern '
                   'generators (including Nishiwaki\'s, which connects patterns "every one step", i.e. at the gait\'s own step '
                   'boundaries) need more than two; this is a qualitative claim, with no measured phase-independent baseline. '
                   'It also warns that waiting for the gait\'s own step boundary is itself a slow way to stop: the gain here '
                   'comes from re-planning the current step from any instant, not from deferring the stop to a phase.'},
    {'id': 'r1a:4', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Tanaka, Takubo, Inoue & Arai (Osaka University), "Emergent stop for Humanoid Robots", IEEE/RSJ IROS 2006 '
               '(DOI 10.1109/IROS.2006.281833)',
     'version': 'IROS 2006; abstract only, reconstructed word for word from the OpenAlex record (abstract_inverted_index), '
                'fetched 2026-09-30; full text not reached (IEEE Xplore returned HTTP 202 with an '
                'empty body)',
     'url': 'https://doi.org/10.1109/IROS.2006.281833',
     'quote': ['The stable gait change is generated by adjusting the amount of the ZMP modification according to the timing '
               'of stop command.',
               'In this method, the humanoid robot can stop immediately within one step to avoid a collision',
               'The stop motion is typically divided two mode; single leg stop motion and double leg stop motion. The stop '
               'mode and the next landing position are decided according to the command time of the stop signal.'],
     'raw_file': T + 'openalex_10.1109_iros.2006.281833.txt',
     'agent_note': 'States P1 (abstract only): the stop of a walking HRP-2 is keyed to where in the gait cycle the command '
                   'arrives: the stop mode (single-leg or double-leg) and the next landing position are chosen from the '
                   'command time, using a precomputed map of ZMP modification against command timing.'},
    {'id': 'r1a:5', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Takubo, Tanaka, Inoue & Arai (Osaka University), "Emergent walking stop using 3-D ZMP modification criteria '
               'map for humanoid robot", IEEE ICRA 2007, pp. 2676-2681 (DOI 10.1109/ROBOT.2007.363869)',
     'version': 'ICRA 2007; abstract only, reconstructed word for word from the OpenAlex record (abstract_inverted_index), '
                'fetched 2026-09-30; full text not reached (IEEE Xplore returned HTTP 202 with an empty body)',
     'url': 'https://doi.org/10.1109/ROBOT.2007.363869',
     'quote': ['We make the map of relation among the ZMP modification length, the modification timing and the timing of the '
               'stop command for stable gait modification.',
               'In the single leg support phase, the next landing position and timing are decided according to command time '
               'of the stop signal. In the double leg support phase, the humanoid robot can stop anytime without changing '
               'standing position.'],
     'raw_file': T + 'openalex_10.1109_robot.2007.363869.txt',
     'agent_note': 'States P1 (abstract only): the successor of r1a:4; the stop\'s landing position and timing are set by the '
                   'gait phase at the command (single-leg support), while in double support the robot stops at once. This is '
                   'the phase-keyed shaping of the stop that C-R1 predicts, published in 2006-07 on HRP-2.'},
    {'id': 'r1a:6', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Pratt, Carff, Drakunov & Goswami (IHMC; Honda Research Institute), "Capture Point: A Step toward Humanoid Push '
               'Recovery", IEEE-RAS Humanoids 2006, pp. 200-207 (DOI 10.1109/ICHR.2006.321385)',
     'version': 'Humanoids 2006 conference PDF; copy hosted by scispace.com, fetched 2026-09-30 (the author-site copy at '
                'ambarish.com was not fetched: its TLS certificate is self-signed)',
     'url': 'https://scispace.com/pdf/capture-point-a-step-toward-humanoid-push-recovery-12jssfk8t5.pdf',
     'quote': ['we present methods for computing Capture Points and the Capture Region, the region on the ground where a '
               'humanoid must step to in order to come to a complete stop. The intersection between the Capture Region and '
               'the Base of Support determines which strategy the robot should adopt to successfully stop in a given '
               'situation.',
               'The robot is commanded to stop shortly after taking a step at about 3.9 seconds. It does so by lunging its '
               'upper body, without taking an additional step.'],
     'raw_file': T + 'pratt2006_capture_point.txt',
     'agent_note': 'States P1 under the caller\'s list (capture-point stopping is named as an instance of C-R1): the way a '
                   'walking biped stops (balance in place, lunge, or step, and where) is chosen from its current state '
                   'against the base of support; a commanded stop is simulated. The quantity is the capture point (a state), '
                   'not a gait-phase variable; if the investigator reads only explicit phase-keying as C-R1, this is close.'},
    # ------------------------------------------------ B. a phase-timed stop measured against an immediate one (P1, P2)
    {'id': 'r1a:7', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Crowley, Dao, Duan, Green, Hurst & Fern (Oregon State University), "Optimizing Bipedal Locomotion for The 100m '
               'Dash With Comparison to Human Running" (Cassie; arXiv:2508.03070; ICRA 2023, pp. 12205-12211 per the arXiv '
               'comment)',
     'version': 'arXiv v1, 5 Aug 2025 (the only version)', 'url': 'https://arxiv.org/abs/2508.03070v1',
     'quote': ['Instead when the controller receives the signal to stand it [...] waits until the phase is in a good position '
               'in the gait cycle and then swaps to the standing policy.',
               'When Cassie receives the signal to transition from stepping to standing, the controller waits for either of '
               'these two phases and swaps policies at that moment.'],
     'raw_file': T + '2508.03070v1.txt',
     'agent_note': 'States P1 in its timing form: a stop command arriving at any time is deferred to the gait\'s own phase '
                   '(either foot at its apex, read from the policy\'s clock) before the running policy is replaced by a '
                   'standing policy. It is an operational stop at the end of a record run, not a safety function.'},
    {'id': 'r1a:8', 'position': 'P2', 'reading': 'states', 'reading_by': RB,
     'source': 'Crowley et al., 100m dash (arXiv:2508.03070), Section V-C, stepping to standing',
     'version': 'arXiv v1, 5 Aug 2025 (the only version)', 'url': 'https://arxiv.org/abs/2508.03070v1',
     'quote': ['Prior to these adjustments the controller made the transition from stepping to standing immediately when given '
               'the signal to swap. This setup was severely unreliable and almost always failed, both on hardware and in '
               'simulation (less than 10% success rate).',
               'After making the controller wait for an apex phase the success rate soared to about 2 in 3 attempts, and '
               'with this final adjustment to the speed command it improved beyond expectations to 100% of >20 trials.'],
     'raw_file': T + '2508.03070v1.txt',
     'agent_note': 'States P2 (falls): on Cassie, hardware and simulation, the phase-timed stop took success from under 10% '
                   '(immediate, phase-independent swap) to about 2 in 3 (apex-timed), and to 100% of >20 trials with a '
                   'speed-command adjustment added. Cautions: counts are informal (no trial table for the first two arms); '
                   'the last step confounds the phase timing with the speed command; the comparator is an immediate stop, '
                   'not the best clock-delayed stop at equal delay budget that CRR_READING.md names; stopping distance and '
                   'time are not reported.'},
    {'id': 'r1a:9', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Peng, Bao & Zhou, "Gait-Conditioned Reinforcement Learning with Multi-Phase Curriculum for Humanoid '
               'Locomotion" (Unitree G1; arXiv:2505.20619)',
     'version': 'arXiv v3, 15 Sep 2025 (v1 27 May 2025)', 'url': 'https://arxiv.org/abs/2505.20619v3',
     'quote': ['If low speed and double support persist for a manually specified 1.5 s, it switches to Stand (ID = 0). This '
               'hysteresis prevents premature switching.'],
     'raw_file': T + '2505.20619v3.txt',
     'agent_note': 'Close: an operational walk-to-stand whose completion is gated by the support state (double support) with '
                   'a clock hysteresis (1.5 s); not a safety stop, and not compared with an ungated stop.'},
    {'id': 'r1a:10', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Scianca, Ferrari, De Simone, Lanari & Oriolo (Sapienza), "A behavior-based framework for safe deployment of '
               'humanoid robots", Autonomous Robots 45:435-456 (2021; DOI 10.1007/s10514-021-09978-5; CC BY)',
     'version': 'published version PDF (header "Autonomous Robots (2021) 45:435-456"), from the IRIS Sapienza repository, '
                'fetched 2026-09-30 (the Springer PDF link returned an HTML bot-check page)',
     'url': 'https://iris.uniroma1.it/bitstream/11573/1523804/3/Scianca_A-behavior-based_2021.pdf',
     'quote': ['Action: The robot will stop walking, ending in a double support configuration.',
               'The high-level velocity commands vx, vy, ω are immediately set to zero;',
               'The high-level velocity commands vx, vy, ω go from their current value to zero over a fixed arrest time;',
               'The arrest time used by stop is 2 s. As expected, the results indicate that with halt the robot stops '
               'immediately, almost bouncing back; whereas a much smoother finish is obtained using stop.'],
     'raw_file': T + 'scianca2021_iris.txt',
     'agent_note': 'Close, and the frontier\'s side in a safety framework: the emergency stop (halt) zeroes the velocity '
                   'command at once and relies on the MPC gait generator\'s capturability terminal constraint (a state '
                   'constraint); the graceful stop ramps the command to zero over a fixed arrest time on the clock (2 s) and '
                   'ends in double support. Both shown triggered during double support only; no phase-keyed timing.'},
    # ------------------------------------------------ C. the 2026 frontier: phase dependence stated, state-conditioned stops
    {'id': 'r1a:11', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Ding, Cui, Wang & Wen (Siemens), "Toward Certified Functional Safety for Industrial Humanoid Robots: The '
               'Fail-Passive Gap and a Feasibility Study" (Unitree G1; arXiv:2608.02809), Section VIII-A',
     'version': 'arXiv v1, 3 Aug 2026 (the only version)', 'url': 'https://arxiv.org/abs/2608.02809v1',
     'quote': ['The safe stop is thus a constrained stop—minimize stopping time/distance while remaining within the capturable '
               'region— with no analog in ISO 13849 / EN 60204-1.',
               'Mid-step (single-support) demands. The outcome depends on gait phase. In double-support the support polygon '
               'is large and deceleration is quick; if the demand arrives in single-support (swing), immediate freezing is '
               'generally infeasible and the controller must place the current step (reach a capture point) before holding '
               'a static posture.'],
     'raw_file': T + '2608.02809v1.txt',
     'agent_note': 'Close for P1: the 2026 industrial safety analysis states that the stop\'s course depends on the gait phase '
                   '(from swing, place the step first) and frames the safe stop as a constrained, capturability-bounded stop, '
                   'but designs no phase-keyed stop; the G1\'s own balancing policy performs the stop.'},
    {'id': 'r1a:12', 'position': 'P3', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Ding et al. (Siemens), The Fail-Passive Gap (arXiv:2608.02809), Sections V and VIII-A: ISO 13855 sizing',
     'version': 'arXiv v1, 3 Aug 2026 (the only version)', 'url': 'https://arxiv.org/abs/2608.02809v1',
     'quote': ['(i) T is dominated by the uncertified reaction chain (tstop depends on the balancing policy and gait phase), so '
               'S can only be bounded using worst-case measured tstop;',
               'This imposes a phase-dependent lower bound on tstop, so the ISO 13855 distance must be sized using the '
               'worst-case (single-support) tstop.'],
     'raw_file': T + '2608.02809v1.txt',
     'agent_note': 'Contradicts P3 for the current standards route only: under ISO 13855 (S = K T + C) the separation distance '
                   'takes one stopping time, the worst gait phase\'s, for every phase; this is the clock-sized stop that C-R1 '
                   'replaces, written into the certification practice the paper follows. It does not show that a draft such '
                   'as ISO 25785-1 lacks phase-keyed timing (its text was not reachable).'},
    {'id': 'r1a:13', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Long, Abbeel, Sreenath, Horowitz, Shi & Liu, "Humanoid Safe Stop via Learned Stoppability Value" (Safe-Stop; '
               'Unitree G1; arXiv:2609.02358)',
     'version': 'arXiv v1, 2 Sep 2026 (the only version)', 'url': 'https://arxiv.org/abs/2609.02358v1',
     'quote': ['Humanoid robots responding to emergency stop commands typically execute a fixed maneuver, without reasoning '
               'about whether a safe stop is actually feasible from the current state.',
               'Most systems react by zeroing the velocity command and relying on the [...] motion controller to decelerate.',
               'This observation excludes the behavior-policy variables: motion phase, reference trajectory, global position, '
               'perceptual map, task command, base height, and base linear velocity.',
               'Second, there may be transient states from which immediate stopping appears unrecoverable, while continuing '
               'the behavior policy would return the robot to stoppable region. The current framework does not reason this.'],
     'raw_file': T + '2609.02358v1.txt',
     'agent_note': 'Close: a state-conditioned emergency stop (a learned stop policy plus stoppability estimators choosing '
                   'stop or fall policy at the command) that deliberately excludes the motion phase from its inputs; the '
                   'authors name, as a limitation, the timing variant C-R1 predicts (continue the gait until the state is '
                   'stoppable, then stop) and say their framework does not do it. Their description of common practice '
                   '(zero the velocity command at once) is the phase-independent stop.'},
    {'id': 'r1a:14', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Long et al., Safe-Stop (arXiv:2609.02358), Section 5.4, runtime decision rule',
     'version': 'arXiv v1, 2 Sep 2026 (the only version)', 'url': 'https://arxiv.org/abs/2609.02358v1',
     'quote': ['We compare four rules: (a) stop-only, which always attempts πstop;',
               'the strict dual estimator gives the best safety, approving only 31 of 797 real failures.'],
     'raw_file': T + '2609.02358v1.txt',
     'agent_note': 'Close for P2: a state-dependent choice at the stop command (attempt the stop, or hand off to a damping fall '
                   'policy) is measured against always attempting the stop, and approves far fewer stops that end in a fall; '
                   'the conditioning is on proprioceptive state, not the gait phase, and stopping distance or time against a '
                   'phase-independent stop is not reported.'},
    # ------------------------------------------------ D. standards proposals and industrial safety functions (P3)
    {'id': 'r1a:15', 'position': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'IEEE Humanoid Study Group (Prather, Keller et al.), "A Pathway Study for Future Humanoid Standards" '
               '(technical report)',
     'version': 'September 2025 (DOI 10.13140/RG.2.2.27892.21122); copy hosted by The Robot Report; sha256 identical to the '
                'stage-1 harvester\'s copy',
     'url': 'https://www.therobotreport.com/wp-content/uploads/2025/09/IEEE-Humanoid-Report-of-Future-Standards-Development.pdf',
     'quote': ['Level 0: Immediate power cut to all components.',
               'Level 3: Robot views surroundings, then plans and takes action to quickly and as safely as possible move to a '
               'safe robot state.',
               'Examples of such constraints are one-step-capturability and stability regions [2]. These constraints are '
               'based on calculating the regions around the robot during a foot swing phase in which a robot would be able '
               'to stabilize itself if it places its foot down within the region, and then to always ensure the robot can '
               'reach this region.',
               'For a robot with two legs, that would mean with both feet on the ground and not taking any steps or at least '
               'not any step that could generate large or unpredictable displacement.'],
     'raw_file': T + 'IEEE-Humanoid-Report-of-Future-Standards-Development.txt',
     'agent_note': 'Close for P3: the standards proposal grades e-stop behaviour from power cut (Level 0) to a planned move to '
                   'a safe state (Level 3), names swing-phase capturability regions as a candidate minimum stability criterion '
                   'for a standard, and sketches a double-stance, no-step mode near humans; it does not specify that the stop '
                   'is timed or shaped by the gait phase.'},
    {'id': 'r1a:16', 'position': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'Reese, Abate, Chen, ... Wise, Velagapudi, ... (Agility Robotics), "Escalating hazard-response of dynamically '
               'stable mobile robot in a collaborative environment and related technology", US Patent 12,560,948 B2',
     'version': 'US 12,560,948 B2, granted 24 Feb 2026 (filed 28 Feb 2025; prior publication US 2025/0278092 A1, 4 Sep 2025); '
                'USPTO image PDF fetched 2026-09-30, text by OCR (RapidOCR); quoted lines chosen where the OCR is clean',
     'url': 'https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12560948',
     'quote': ['This can include transitioning the mobile robot 100 from a transportation state (e.g., an ambulating state) to '
               'a non-transportation state (e.g., a standing state).',
               'Relatedly, decelerating the mobile robot 100 can include moving one of the feet 116a, 116b into contact with '
               'a ground surface while the other of the feet 116a, 116b is in contact with the ground surface.',
               'Implementing a stop in accordance with at least some embodiments of the present technology can include '
               'moving the mobile robot 100 into a low-energy position before powering-off the mobile robot 100.'],
     'raw_file': T + 'US12560948_ocr.txt',
     'agent_note': 'Close for P3: the leading humanoid maker\'s patented hazard response and protective stop (Category-1/2) '
                   'decelerates a walking Digit by setting the swing foot down beside the stance foot (a stop that ends at the '
                   'next double stance) and then moves it to a low-energy pose (kneel) before power-off; the patent does not '
                   'state that the stop\'s timing is keyed to the gait phase, and every walk-to-stand ends in double support.'},
    {'id': 'r1a:17', 'position': 'P3', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Turk, "Why humanoid robots need their own safety rules", MIT Technology Review (quoting Pras Velagapudi, CTO, '
               'Agility Robotics, and Aaron Prather, IEEE Humanoid Study Group chair)',
     'version': 'published 11 Jun 2025 (page date); fetched 2026-09-30', 'url':
     'https://www.technologyreview.com/2025/06/11/1118519/humanoids-safety-rules/',
     'quote': ['Rather than instantly depowering (and likely falling down), the robot could decelerate more gently when, for '
               'instance, a person gets too close.',
               '“The robot basically has a fixed amount of time to try to get itself into a safe state,” Velagapudi says.'],
     'raw_file': T + 'techreview_humanoids_safety_rules.txt',
     'agent_note': 'Contradicts P3 for Digit\'s safety function as described by its maker (trade press, second-hand): the '
                   'controlled stop has a fixed time budget to reach the safe state, the clock-sized stop C-R1 replaces. A '
                   'journalist\'s paraphrase around a one-sentence quote; no specification.'},
    {'id': 'r1a:18', 'position': 'P3', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Boston Dynamics, Spot SDK, protos/bosdyn/api/estop.proto (the software E-Stop of the Spot quadruped)',
     'version': 'master branch at commit 04537ddafe0641d1751af3eb9e76cb785fc18594 (git ls-remote, 2026-09-30); file header '
                '"Copyright (c) 2023 Boston Dynamics"', 'url':
     'https://raw.githubusercontent.com/boston-dynamics/spot-sdk/master/protos/bosdyn/api/estop.proto',
     'quote': ['Prepare for loss of actuator power, then cut power.',
               'After timeout seconds has passed, the robot will try to get to a safe state prior [...] to disabling motor '
               'power. The robot response is equivalent to an ESTOP_LEVEL_SETTLE_THEN_CUT [...] which may involve the robot '
               'sitting down in order to prepare for disabling motor power.',
               'After cut_power_timeout seconds has passed, motor power will be disconnected [...] immediately regardless of '
               'current robot state. If this value is not set robot will default [...] to timeout plus a nominal expected '
               'duration to reach a safe state. In practice this [...] is typically 3-4 seconds.'],
     'raw_file': T + 'spot_sdk_estop.proto.txt',
     'agent_note': 'Contradicts P3 for a deployed legged robot\'s industrial E-stop: the settle-then-cut stop has a clock '
                   'budget after which power is cut "regardless of current robot state"; the settle (sit down) is a controlled '
                   'stop, but neither its timing nor its budget is keyed to the gait phase.'},
    {'id': 'r1a:19', 'position': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'Takahashi & Suzaki (Honda), US Patent 5,369,346 (r1a:1), read for P3',
     'version': 'US 5,369,346 A, granted 29 Nov 1994; OCR text as r1a:1',
     'url': 'https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5369346',
     'quote': ['It can thus be understood from the figure that the attitude of the biped walking robot is particularly '
               'unstable during one-leg support period.',
               'Steps 116 and 120 are then repeatedly executed until it is confirmed that a stable attitude has been reached '
               '(e.g. that the center of gravity is at the bottom [...] of the supporting foot), and control then passes to '
               'step S118.'],
     'raw_file': T + 'US5369346_ocr.txt',
     'agent_note': 'Close for P3 under the fixed policy: a manufacturer (Honda) patented a phase-keyed emergency stop for a '
                   'biped in 1994, but the sources found do not show it as a deployed or certified safety function. An '
                   'investigator who counts a manufacturer\'s patented safety function as "an industrial safety function" '
                   'would read this states.'},
    # ------------------------------------------------ E. the mechanism in human gait (foundational)
    {'id': 'r1a:20', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Hase & Stein, "Analysis of rapid stopping during human walking", Journal of Neurophysiology 80(1):255-261 '
               '(1998; DOI 10.1152/jn.1998.80.1.255; PMID 9658047)',
     'version': 'July 1998; abstract only, from Europe PMC (MEDLINE record), fetched 2026-09-30; the publisher full text '
                'returned HTTP 403',
     'url': 'https://europepmc.org/article/MED/9658047',
     'quote': ['The step cycle was divided into 16 parts, and the responses to stimuli in each part were analyzed separately. '
               'Subjects generally stopped with the right foot in front of the left or vice-versa, depending on when the '
               'stimulus was applied in the step cycle.',
               'A decision to take an additional step depends on whether the momentum of the body is sufficient to carry the '
               'center of mass in front of its support on the forward leg.'],
     'raw_file': T + 'europepmc_9658047.txt',
     'agent_note': 'Close (humans, not robots): rapid stopping in human gait is shaped by the phase of the step cycle at which '
                   'the stop signal arrives, and the extra-step decision is a capture-point-like test of momentum against the '
                   'forward support; the biological precedent the robotics sources follow.'},
]
