"""Claims for ROB1 stage 3 (Robotics/DECLARATION.md), candidate C-R1 (Robotics/CRR_READING.md, r4-B4), searcher B, independent
of searcher A: a phase-keyed stop for a dynamically balancing legged or humanoid robot. Transcribed from the dossier
docs/citations/rob1_s3_r1b_2026-09-30.md (sources fetched 2026-09-30; raw files and extracted texts held outside the
repository under /tmp/claude-0/rob_s3/, named in `raw_file` relative to that root, with r1b/SHA256SUMS.txt beside them).
Every quote was checked verbatim against its extracted text before this file was written (normalisation and matching as
Robotics/checks/verify.py: NFKC, whitespace collapsed, line-break hyphens either kept or rejoined, "[...]" checked fragment by
fragment). Searcher B read claims_s3_r1a.py first and searched differently: the Japanese-language journal literature (J-STAGE:
the full texts behind A's abstract-only HRP-2 records), learned-controller practice, deployed humanoid manuals, the patent text
behind A's patent claim, and industrial and aviation regulation (other machine classes). One claim (r1b:12) quotes searcher
A's OCR text of a patent A fetched; searcher B checked the quoted lines by eye against A's page image (r1a/ocr/..._p20.png).

The quotes from the three J-STAGE PDFs (r1b:1-6, r1b:8-9) are Japanese and are copied from the PDFs' text layers, which carry
spurious spaces (inherited from the scans' text layers) and a few OCR errors (e.g. "t∫" for "tf", "片 脚指示時間" for 片脚支持時間).
They are quoted as the text layer has them, because the check is mechanical; the agent_note gives an English rendering, which is
the searcher's translation, not a quote.

The mechanism searched (CRR_READING.md, C-R1): a stop (emergency stop, protective stop, safe stop, fall-safe stop) of a
dynamically balancing legged or humanoid robot that is initiated, timed or shaped by the gait's own phase (gait-phase-dependent
stopping, phase-aware stop trajectories, capture-point / stance-phase stopping, "stop at the next stance", phase-dependent
safe-state selection), as opposed to one stopping time on the clock sized by the worst gait phase. CRR's prediction: over stop
commands arriving uniformly in time, a phase-keyed stop has a lower worst case and a lower mean of stopping distance and falls,
at equal delay budget, than the best single clock-sized stop.

Positions (the caller's):
  P1  phase-dependent timing or shaping of a stop for a legged or humanoid robot is published;
  P2  it is shown to reduce worst-case or mean stopping distance, time or falls against a phase-independent stop;
  P3  it appears in a standard, a standards proposal or an industrial safety function (e.g. ISO 25785-1 drafts, IFR/industry
      white papers).

'reading' is decided by the stage-3 agent from the quote, for the investigator's review ('reading_by'). Reading policy: searcher
A's policy (claims_s3_r1a.py), adopted unchanged so that the two sweeps grade alike, with three additions, all fixed before
searcher B's readings were written:
  states       P1: the source designs, implements or specifies a stop of a walking or balancing legged/humanoid robot
               (emergency, protective, safe or commanded stop) whose initiation, timing or shape is set by where the gait is
               in its cycle (support phase, swing state, the next touchdown or apex, the capture point against the base of
               support);
               P2: a measured comparison (hardware or simulation) in which such a stop gives fewer falls, or a shorter
               stopping distance or time, than a phase-independent stop (immediate or clock-timed);
               P3: a standard, a standards draft or proposal, or an industrial safety function specifies phase-keyed timing
               or shaping of the stop;
  close        P1: the phase dependence of stopping is stated but no phase-keyed stop is designed; or the stop is conditioned
               on the robot's state but not keyed to the gait phase (learned stop policies, stoppability estimators,
               capturability constraints under a clock-timed stop); or an operational stop gated by the support state with a
               clock hysteresis; or the mechanism is shown in humans, not robots;
               P2: a state-dependent (not phase-keyed) stop decision compared with an unconditioned stop, or a qualitative
               claim of shorter stops with no measured phase-independent baseline; [addition B1] or a qualitative or analytic
               claim about how the stop's outcome depends on the phase at which it starts, with no measured phase-independent
               baseline;
               P3: a standard, proposal or industrial function that specifies a controlled (non-de-energising) stop or a
               stance/state-dependent safe state for legged robots without phase-keyed timing; or a manufacturer's patent of
               a phase-keyed stop with no evidence that it is a deployed or certified function; [addition B2] or a phase-keyed
               stop in operational but uncertified, non-industrial deployment (a research robot operated in public); or a
               regulation or certification rule that keys a stop decision or a protective function to the machine's own
               cycle or progress in another machine class (cyclic presses, aircraft take-off), not legged robots;
  contradicts  P1/P2: the source shows a phase-keyed stop infeasible, no better or worse than a phase-independent stop;
               P3: the source documents a standard, a standards route or an industrial safety function that sizes or budgets
               the stop by one clock time independent of the gait phase; [addition B3] or a deployed legged robot's safety
               function that applies the stop at the command instant irrespective of the gait phase (evidence against P3 for
               that standard or function; it cannot disprove existence elsewhere).
Grade (Robotics/DECLARATION.md stage 3): REDUNDANT, PARTLY REDUNDANT or NOT FOUND IN THE SWEEP, computed by the investigator's
grading script from these readings, not here. 'Not found' is never 'novel'.

READING_CHECKS: searcher B's check of each of searcher A's readings (is the reading justified by A's quotes under A's policy?);
A's quotes were re-matched against A's extracted texts (all 20 claims, every quote FOUND) before the checks were written.
"""

RB = "stage-3 agent (searcher B); for the investigator's review"
T = 'r1b/txt/'

CLAIMS = [
    # ------------------------------------------------ A. AIST, HRP-2: the pause (motion suspension) deferred to the gait's phase
    {'id': 'r1b:1', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Kaneko, Kanehiro, Morisawa, Kajita, Fujiwara, Harada & Hirukawa (AIST), "Motion Suspension System for Humanoids: '
               'Real-time Judgment and Motion Generation to suspend Humanoids" (ヒューマノイドの動作一時停止システム), Journal of '
               'the Robotics Society of Japan 25(2):289-298 (2007; DOI 10.7210/jrsj.25.289); an English version is listed in IEEE Xplore '
               'under IROS 2006 (not fetched)',
     'version': 'JRSJ 25(2), published 15 Mar 2007 (J-STAGE online 25 Aug 2010); J-STAGE PDF fetched 2026-09-30 (open access); '
                'text layer of the PDF',
     'url': 'https://www.jstage.jst.go.jp/article/jrsj1983/25/2/25_2_289/_pdf',
     'quote': ['We also propose a simple and effective method of real-time pattern generation to force humanoids to stop '
               'immediately by one step without falling.',
               '本 稿で提案するシステムで は,両 脚支持期の中間点でこの信号をHighレ ベルにし,そ の 他の期間はLowレ ベルにしている.',
               '判 定信号:Jflag-ψ がHigh信 号になったタイミングで早急に一時 停止動作を開始する必要は必ずしもなく,両脚支持期の中間点 '
               'で開始しても十分に効果があると判断した.',
               '基本方針3:新 規に生成する一時停止動作パターンに切り替 えるタイミングは,両 脚支持期の中間点で行うこと.',
               'ε は,目 標胴体位置から見て, 目標とする左右足裏位置が同じ距離にあるか否かを判別するた めの微小な正の値である.'],
     'raw_file': T + 'jstage_kaneko2007.txt',
     'agent_note': 'States P1, in its timing form ("stop at the next stance"), on hardware, 2006-07. Translation (B\'s): "In the '
                   'proposed system this signal [the suspension-start-enable signal] is set High at the midpoint of the double '
                   'support phase and Low at all other times"; "we judged that it is not necessary to start the suspension '
                   'motion immediately when the judgment signal goes High; starting it at the midpoint of the double support '
                   'phase is sufficiently effective"; "Basic policy 3: the switch to the newly generated suspension pattern is '
                   'made at the midpoint of the double support phase"; "epsilon is a small positive value for judging whether '
                   'the target left and right sole positions are at the same distance from the target body position". So the '
                   'pause of a walking HRP-2, requested by the operator or triggered by the robot\'s own posture and '
                   'landing-force sensors, is deferred to an event defined by the gait\'s own geometry (the feet equidistant '
                   'from the body), not to a clock time; then a constant deceleration brings the robot to rest within one step. '
                   'The system is called a motion suspension (一時停止, a temporary stop or pause) and resumes on the '
                   'operator\'s command. Full text, not an abstract.'},
    {'id': 'r1b:2', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Kaneko et al. (AIST), "Motion Suspension System for Humanoids", JRSJ 25(2):289-298 (2007), Section 3.3',
     'version': 'JRSJ 25(2), 15 Mar 2007; J-STAGE PDF fetched 2026-09-30',
     'url': 'https://www.jstage.jst.go.jp/article/jrsj1983/25/2/25_2_289/_pdf',
     'quote': ['両 脚支持期の初期や後期に,オ リジナルパターンから, 一定加速度で減速するような一時停止動作パターンに切り替え ると,'
               '切 り替えタイミング時のx軸 方向(Fig.6参 照)の 重心 速度が十分に減速しておらず,x\'軸 方向の支持多角形の範囲も '
               '狭いことから(x\'軸 方向の安定余裕が少ないことから),一 時 停止動作を実現可能な歩行速度の上限値が低くなる問題が出て くる.',
               '時 速2.5[km]ま では,提 案する一時停止動 作にて,HRP-2を1歩 以内に一時停止させることができるこ とを確認している.'],
     'raw_file': T + 'jstage_kaneko2007.txt',
     'agent_note': 'Close for P2 (addition B1). Translation: "if the switch to the constant-deceleration suspension pattern is '
                   'made early or late in the double support phase, the centre-of-mass velocity along x\' has not yet fallen '
                   'enough and the support polygon is narrow along x\', so the upper limit of the walking speed at which the '
                   'suspension can be realised becomes lower"; "we confirmed that up to 2.5 km/h the proposed suspension stops '
                   'HRP-2 within one step" (at 2.8 km/h the rear foot lifts, the stated limit). The phase dependence of the '
                   'stop\'s feasibility is argued from the gait\'s dynamics and the phase-keyed stop is shown on hardware, but '
                   'no immediate or clock-timed suspension is measured against it.'},
    {'id': 'r1b:3', 'position': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'Kaneko et al. (AIST), "Motion Suspension System for Humanoids", JRSJ 25(2):289-298 (2007), Section 4 (operation)',
     'version': 'JRSJ 25(2), 15 Mar 2007; J-STAGE PDF fetched 2026-09-30',
     'url': 'https://www.jstage.jst.go.jp/article/jrsj1983/25/2/25_2_289/_pdf',
     'quote': ['展 示会会場や研究室での運用を考え た場合には,実 験結果にも示す通り,提案する動作一時停止シ ステムは非常に有用である.'],
     'raw_file': T + 'jstage_kaneko2007.txt',
     'agent_note': 'Close for P3 (addition B2). Translation: "considering operation at exhibition venues and in the laboratory, '
                   'the proposed motion suspension system is very useful, as the experimental results show"; the same section '
                   'lists the cases met in current operation (objects thrown into or dropped in the demonstration space, a '
                   'person entering it, an operator\'s mistaken start command). A phase-keyed suspension in operational use by '
                   'a national laboratory, not a standard and not a certified industrial safety function.'},
    # ------------------------------------------------ B. AIST, HRP-2: emergency stop begun at the next double support
    {'id': 'r1b:4', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Morisawa, Kajita, Kaneko, Kanehiro, Nakaoka, Harada, Fujiwara & Hirukawa (AIST), "Motion Generation of Emergency '
               'Stop at Double Support Phase for Humanoid Robot by Pole Assignment" (極配置法によるヒューマノイドロボットの両脚期に'
               'おける緊急停止動作生成), Journal of the Robotics Society of Japan 26(4):341-350 (2008; DOI 10.7210/jrsj.26.341)',
     'version': 'JRSJ 26(4), published 15 May 2008 (J-STAGE online 25 Aug 2010); J-STAGE PDF fetched 2026-09-30 (open access; '
                'the site was briefly in maintenance and the fetch was repeated); text layer of the PDF',
     'url': 'https://www.jstage.jst.go.jp/article/jrsj1983/26/4/26_4_341/_pdf',
     'quote': ['Fig.4(a)停 止指令が単脚期(Single support phase:S.S.)で 与えられたとき,ロ ボットは既存の動作パター '
               'ンに従って動き,両脚期(Double support phase:D.S.)が 現 [...] われたとき停止動作を開始する.Fig.4(b)停 '
               '止指令が両脚期で 与えられたとき,そ の時点から停止動作を開始する',
               '停 止指令を単脚期中に 与え,両 脚期を検出した直後に停止動作を開始するようにした.',
               '信頼性と実時間性の観点から,ダ イナミクスの影響が少 ない両脚期に停止軌道を生成し'],
     'raw_file': T + 'jstage_morisawa2008.txt',
     'agent_note': 'States P1 in its timing form, on hardware. Translation: "(a) when the stop command is given in the single '
                   'support phase, the robot moves according to the existing motion pattern and starts the stop motion when the '
                   'double support phase appears; (b) when the stop command is given in the double support phase, the stop '
                   'motion starts at that moment"; in the experiments "the stop command was given during single support and the '
                   'stop motion started immediately after the double support phase was detected" (HRP-2, 1.125 and 2.5 km/h, '
                   'ten repetitions each); "for reliability and real-time computation, the stop trajectory is generated in the '
                   'double support phase, where the influence of the dynamics is small". This is exactly "stop at the next '
                   'stance" for an emergency stop. The [...] in the first quote elides only a page break (running head, page '
                   'number and the caption of Fig. 4).'},
    {'id': 'r1b:5', 'position': 'P2', 'reading': 'close', 'reading_by': RB,
     'source': 'Morisawa et al. (AIST), "Motion Generation of Emergency Stop at Double Support Phase ...", JRSJ 26(4) (2008), '
               'Sections 2 and 5.1',
     'version': 'JRSJ 26(4), 15 May 2008; J-STAGE PDF fetched 2026-09-30',
     'url': 'https://www.jstage.jst.go.jp/article/jrsj1983/26/4/26_4_341/_pdf',
     'quote': ['こ のように,両 脚期のどのタイミングで停止軌道を開 始するかによってZMPの 移動量が異なり,ZMPの 安定余裕が '
               '異なってくることが分かる.',
               'これらの結果から2.5[km/h]ま での直進歩行においては,両 脚 期のどのタイミングで停止動作を開始しても,安 定な停止軌道 '
               'を生成することが可能であることが分かる.',
               'この手法は収束計算を伴うため計算負荷が比較的 大きく,単脚期において着地軌道を新たに生成する際にモデル '
               'で考慮していない遊脚の慣性力の影響で着地時の床反力が大き くなり,低速の歩行にしか実用上適用できない問題があった.',
               'この手法は,動作パター ンの重心軌道とZMP軌 道が両脚期に交差するのを検出して停 止動作を開始するため,踊 '
               'りなどの複雑なステップを有する動 作パターンでは1歩以内に停止できない可能性がある.'],
     'raw_file': T + 'jstage_morisawa2008.txt',
     'agent_note': 'Close for P2 (addition B1), with a caution that cuts both ways. Translation: "thus the ZMP travel, and the '
                   'ZMP stability margin, differ with the timing within the double support phase at which the stop trajectory '
                   'starts" (simulation on the HRP-2 model); "up to 2.5 km/h a stable stop trajectory can be generated whatever '
                   'the timing within double support"; of the same authors\' 2005 method, which also re-plans from single '
                   'support: "the computational load is relatively large, and when a new landing trajectory is generated in '
                   'single support the swing leg\'s inertia, not in the model, raises the landing reaction force, so it was '
                   'practical only for slow walking"; of Kaneko\'s phase-triggered suspension (r1b:1): "because it starts the '
                   'stop on detecting the crossing of the CoG and ZMP trajectories in double support, it may fail to stop '
                   'within one step for motion patterns with complex steps such as dancing". So the phase dependence is '
                   'computed, the reason for deferring to double support is stated, and the cost of deferral (the wait for the '
                   'phase event) is named; no measured comparison against an immediate or clock-timed stop.'},
    {'id': 'r1b:6', 'position': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'Morisawa et al. (AIST), JRSJ 26(4) (2008), Introduction: the emergency stop system of the dinosaur-type biped '
               'robot operated at Expo 2005 (Aichi)',
     'version': 'JRSJ 26(4), 15 May 2008; J-STAGE PDF fetched 2026-09-30',
     'url': 'https://www.jstage.jst.go.jp/article/jrsj1983/26/4/26_4_341/_pdf',
     'quote': ['2005年3月25日 から同年9月25日 にかけて開催 された愛・地球博で185日 間運用展示を行った.恐 竜ロボット '
               'の長期の運用に当たり,動 作中の観客への安全性の確保および ロボットの転倒防止を目的として,緊 急停止システムを開発し '
               'た[4][5].'],
     'raw_file': T + 'jstage_morisawa2008.txt',
     'agent_note': 'Close for P3 (addition B2). Translation: "[AIST] operated and exhibited [a dinosaur-type biped robot] for 185 '
                   'days at Expo 2005 (Aichi), held 25 March to 25 September 2005; for its long-term operation an emergency stop '
                   'system was developed to ensure the safety of spectators during motion and to prevent the robot from '
                   'falling [4][5]", where [4] is Kaneko et al. (r1b:1, the stop deferred to the double-support midpoint) and '
                   '[5] is Morisawa et al. IROS 2005 (A\'s r1a:2, the stop shaped by the phase at the signal). A phase-keyed '
                   'stop in public operation for six months, twenty years ago; not a standard, not certified, not industrial. '
                   'The sentence cites both methods together, so which one ran on the dinosaur robot is not stated here.'},
    # ------------------------------------------------ C. Osaka University, HRP-2: the full text behind A's abstract-only records
    {'id': 'r1b:7', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Takubo, Inoue & Arai, "Emergent Stop by Using Preview ZMP Criteria Map for Humanoid Robot" (予見軌道の修正指標'
               'マップを用いたヒューマノイドロボットの緊急停止動作), Transactions of the JSME Series C 75(759):2986-2995 (2009; '
               'DOI 10.1299/kikaic.75.2986)',
     'version': 'Trans. JSME C 75(759), published 25 Nov 2009 (J-STAGE online 9 Jun 2017); English abstract from the J-STAGE '
                'article page, fetched 2026-09-30',
     'url': 'https://www.jstage.jst.go.jp/article/kikaic1979/75/759/75_KJ00005879351/_article/-char/ja/',
     'quote': ['The stable gait change is generated by adjusting the amount of the reference ZMP modification according to the '
               'timing of stop command.',
               'We make the map of relation among the reference ZMP modification length, the modification of step timing and '
               'the timing of the stop command for stable stop motion.'],
     'raw_file': T + 'jstage_takubo2009_page.txt',
     'agent_note': 'States P1: the journal version of A\'s r1a:4 (IROS 2006) and r1a:5 (ICRA 2007), for which A had abstracts '
                   'only. The stop\'s ZMP modification and its step timing are set from the timing of the stop command within '
                   'the gait (the full text, r1b:8, defines that timing from the start of single support).'},
    {'id': 'r1b:8', 'position': 'P1', 'reading': 'states', 'reading_by': RB,
     'source': 'Takubo, Inoue & Arai, Trans. JSME C 75(759) (2009), Sections 2.2, 3.5 and 3.6 (full text)',
     'version': 'Trans. JSME C 75(759), 25 Nov 2009; J-STAGE PDF fetched 2026-09-30 (open access); text layer of a scanned PDF '
                '(NII-ELS), with OCR errors',
     'url': 'https://www.jstage.jst.go.jp/article/kikaic1979/75/759/75_KJ00005879351/_pdf',
     'quote': ['片脚支持開始 時刻を基準とした緊急停止指令タイミングをtc,変更 後の目標歩幅をSi とする',
               'こ こで指令タイミングtc が前進停止限界時間tf 未満であれば,決定された修正 片脚支持時間の最大値, t∫以降であれば最小値を求め る.',
               'この時間より早く緊急停止指令が行われた場合は,ゼ ロ ステップ停止可能となり,遊脚の着地を必要としな い',
               'つまり,片脚支持期前の両脚支 持期中に停止指令が行われた場合,進行方向にある足 位置へ目標ZMP を定めることでいっ でも停止できる '
               'ことがわかる'],
     'raw_file': T + 'jstage_takubo2009.txt',
     'agent_note': 'States P1 in its shaping form. Translation: "tc is the emergency-stop command timing measured from the start of '
                   'single support, and S1 the modified step length"; "if the command timing tc is before the forward-stop limit '
                   'time tf, the maximum admissible modified single-support time is taken, and from tf on the minimum"; "if the '
                   'emergency stop command comes earlier than this time [0.265 s into single support in the example], a '
                   'zero-step stop is possible and the swing leg need not land"; "if the stop command arrives in the double '
                   'support phase before single support, the robot can stop at any time by setting the target ZMP on the front '
                   'foot" (OCR "いっ でも" = いつでも, "at any time"). The stop\'s mode, landing position and landing time are '
                   'selected from the phase of the command within the step.'},
    {'id': 'r1b:9', 'position': 'P2', 'reading': 'states', 'reading_by': RB,
     'source': 'Takubo, Inoue & Arai, Trans. JSME C 75(759) (2009), Section 3.4 and Fig. 10: retimed against unchanged single '
               'support time',
     'version': 'Trans. JSME C 75(759), 25 Nov 2009; J-STAGE PDF fetched 2026-09-30; text layer of a scanned PDF',
     'url': 'https://www.jstage.jst.go.jp/article/kikaic1979/75/759/75_KJ00005879351/_pdf',
     'quote': ['停止動作の比較対象として,片脚支持時間を 変更しないときの修正歩幅の最小値を図10 に破線で 示す.停止指令後に片脚支持時間を'
               '変更することで片 脚指示時間が一定のままの場合と比べ て修正歩幅を小 さくすることができることがわかる.'],
     'raw_file': T + 'jstage_takubo2009.txt',
     'agent_note': 'States P2, with cautions. Translation: "as a baseline for the stop motion, the minimum modified step length '
                   'when the single support time is not changed is shown by the broken line in Fig. 10; changing the single '
                   'support time after the stop command [by the rule keyed to tc, r1b:8] makes the modified step length smaller '
                   'than when the single support time stays constant" (OCR "片 脚指示時間" for 片脚支持時間). The comparison '
                   'runs over every command timing tc across single support (a curve, computed on the preview-control model), '
                   'and the metric is how far forward the swing foot must land to stop (a stopping-distance measure). '
                   'Cautions: simulation, a figure without tabulated numbers; the baseline keeps the step on its planned clock '
                   '(clock-timed landing) but still chooses its step length from the map at tc, so what is isolated is the '
                   'phase-keyed re-timing, not phase keying as a whole; no falls are counted; it is not the best worst-phase '
                   'clock stop at equal delay budget that CRR_READING.md names.'},
    # ------------------------------------------------ D. the learned-controller frontier: phase attested, then removed
    {'id': 'r1b:10', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'van Marum, Shrestha, Duan, Dugar, Dao & Fern (Oregon State University), "Revisiting Reward Design and '
               'Evaluation for Robust Humanoid Standing and Walking" (Digit; arXiv:2404.19173)',
     'version': 'arXiv v2, 30 Aug 2024 (v1 30 Apr 2024); arXiv comment "8 pages, 5 figs"; the venue (IROS 2024, per a search-result '
                'summary) was not verified on the day', 'url': 'https://arxiv.org/abs/2404.19173v2',
     'quote': ['1) Stand. The robot should stop if moving and stand in place with two feet on the ground.',
               'For example, this may involve hand-engineered cycle-time constraints in transitioning from waking to standing '
               '[12] or blending the outputs of the controllers at transition points [13, 15].',
               'in this work, we choose to train a single SaW controller that does not require any form of reference or '
               'clock-based inputs, and natively learns to switch freely between commands throughout the entire learning '
               'process.',
               'Additionally, when transitioning from walking to standing, requiring double foot contact will cause a policy '
               'to opt for the closest stance position rather than the most stable one.'],
     'raw_file': T + '2404.19173v2.txt',
     'agent_note': 'Close for P1. Reference [12] is Crowley et al., ICRA 2023 (A\'s r1a:7/r1a:8), so the source attests that '
                   'phase-keyed walk-to-stand transitions ("cycle-time constraints", sic "waking") are prior practice, calls them '
                   'hard to tune, and replaces them with a single learned policy without clock inputs that stops from any state '
                   '(no phase-keyed timing). Same laboratory as Crowley, so the attestation is not independent. No measured '
                   'comparison of the two ways of stopping.'},
    {'id': 'r1b:11', 'position': 'P1', 'reading': 'close', 'reading_by': RB,
     'source': 'Sun, Pan, Li, Ding, Cui, Wang & Liu, "Learning Safe-Stoppability Monitors for Humanoid Robots" (PRISM; Unitree '
               'G1; arXiv:2603.22703)',
     'version': 'arXiv v1, 24 Mar 2026 (the only version)', 'url': 'https://arxiv.org/abs/2603.22703v1',
     'quote': ['On the other hand, E-stop triggers are asynchronous and unpredictable. An emergency stop may be triggered at any '
               'time due to human intrusion, system-level anomalies, communication failures, or direct operator intervention.',
               'must maintain its state in the safe-stoppable envelope (SSE): a set of states from which the fallback controller '
               'can reliably drive the robot to a dynamically stable terminal condition',
               'By continuously evaluating whether the current state remains within SSE, the monitor can autonomously trigger '
               'E-stop behavior before catastrophic failure occurs',
               'identifies elevated risks during manipulation phases (Pick, Place) while ensuring high confidence during '
               'steady-state locomotion (Transfer, Leave).'],
     'raw_file': T + '2603.22703v1.txt',
     'agent_note': 'Close for P1 (state-conditioned, not gait-phase-keyed; not found by A, whose sweep had the companion '
                   'Safe-Stop paper r1a:13). The 2026 frontier frames the stop command as arriving at any instant and answers '
                   'with a learned state-level stoppability monitor that keeps the robot inside the stoppable set and may '
                   'trigger the stop itself; the phases it finds risky are task phases (pick, place), and steady walking is '
                   'judged highly stoppable. No phase-keyed timing; no comparison with a phase-independent stop.'},
    # ------------------------------------------------ E. deployed functions and patents: the stop on the clock or at the instant
    {'id': 'r1b:12', 'position': 'P3', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Reese, Abate, Chen, ... Wise, Velagapudi, ... (Agility Robotics), US Patent 12,560,948 B2 (A\'s r1a:16), '
               'method 350: the stop command\'s time limit',
     'version': 'US 12,560,948 B2, granted 24 Feb 2026; searcher A\'s USPTO image PDF and OCR text (r1a/txt/US12560948_ocr.txt); '
                'the quoted lines (col. 14, lines 33-41) checked by eye by searcher B against A\'s page image '
                'r1a/ocr/US12560948_p20.png',
     'url': 'https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12560948',
     'quote': ['In an example, the stop command carries a time [...] implementation time for a candidate reconfiguration.',
               'If the implementation time for the candidate reconfiguration is less than the time limit, the mobile robot 100 '
               'proceeds with implementing the candidate reconfiguration.'],
     'raw_file': 'r1a/txt/US12560948_ocr.txt',
     'agent_note': 'Contradicts P3 for this function (addition B3 not needed: a clock budget). The page image reads in full: "In '
                   'an example, the stop command carries a time limit. The mobile robot 100 compares this time limit to a known '
                   'implementation time for a candidate reconfiguration. If the implementation time ... is less than the time '
                   'limit, the mobile robot 100 proceeds with implementing the candidate reconfiguration. If not, the mobile '
                   'robot 100 attempts the comparison again for a different candidate reconfiguration." The OCR merged two '
                   'lines, so the elided fragment ("limit. The mobile robot 100 compares this time limit to a known") is marked '
                   '[...]. The patented protective stop is budgeted by a clock time carried by the command, and the safe pose '
                   'is chosen to fit it; no phase keying. It corroborates, from the primary source, the trade-press quote A '
                   'read as contradicts (r1a:17: "a fixed amount of time"). A patent embodiment ("In an example"), not proof of '
                   'the shipped function.'},
    {'id': 'r1b:13', 'position': 'P3', 'reading': 'contradicts', 'reading_by': RB,
     'source': 'Unitree Robotics, "G1 User Manual" (the humanoid used in r1a:9, r1a:11, r1a:13 and r1b:11)',
     'version': 'edition 1.1, 28 Oct 2024 (revision history in the manual); PDF hosted by a reseller (cistemlabs.ai), fetched '
                '2026-09-30; the regulator-hosted copy (fcc.report, FCC ID 2A5PE-YUSHU008) returned HTTP 403',
     'url': 'https://cistemlabs.ai/wp-content/uploads/2025/04/G1-USER-MANUAL-EN.pdf',
     'quote': ['Emergency Stop: When G1 appears in an unexpected state, press L1+A, G1 will enter damping mode and will slowly '
               'fall to the ground.',
               'Be familiar with the emergency braking method of the robot in case of instability / loss of control.'],
     'raw_file': T + 'g1_G1-USER-MANUAL-EN.txt',
     'agent_note': 'Contradicts P3 for this deployed function (addition B3): the emergency stop of the most widely used research '
                   'humanoid of 2025-26 puts the joints into damping at the command instant, whatever the gait is doing, and the '
                   'robot collapses; no phase keying and no balance. Firmware 1.0.4 moved the chord to L2+B with the same '
                   'behaviour (distributor documentation, not saved).'},
    # ------------------------------------------------ F. other machine classes: the same structure in regulation
    {'id': 'r1b:14', 'position': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'US 29 CFR 1910.217, "Mechanical power presses" (OSHA), paragraphs (c)(3)(iii)(d)-(e) and (h)(9)(v)',
     'version': 'Code of Federal Regulations, Title 29, vol. 5, revised as of 1 July 2021 (govinfo annual edition), fetched '
                '2026-09-30',
     'url': 'https://www.govinfo.gov/content/pkg/CFR-2021-title29-vol5/pdf/CFR-2021-title29-vol5-sec1910-217.pdf',
     'quote': ['Muting (bypassing of the protective function) of such device, during the upstroke of the press slide, is '
               'permitted for the purpose of parts ejection, circuit checking, and feeding.',
               'Ts = stopping time of the press measured at approximately 90° position of crankshaft rotation (seconds).',
               'Ts = Longest press stopping time, in seconds, computed by taking averages of multiple measurements at each of '
               'three positions (45 degrees, 60 degrees, and 90 degrees) of crankshaft angular position; the longest of the '
               'three averages is the stopping time to use.'],
     'raw_file': T + 'govinfo_cfr2021_1910_217.txt',
     'agent_note': 'Close for P3 (addition B2: another machine class). In US machine-safety regulation for a cyclic machine, the '
                   'stopping time is measured per phase of the cycle (crank angle), the safety distance is sized by the worst '
                   'phase\'s stopping time (the structure of ISO 13855 sizing by the worst gait phase, r1a:12), and the '
                   'protective function itself is keyed to the cycle phase (muted on the non-hazardous upstroke). Both sides of '
                   'C-R1 are therefore old regulatory practice for presses; neither concerns a legged robot, and the stop '
                   'itself is not timed by phase.'},
    {'id': 'r1b:15', 'position': 'P3', 'reading': 'close', 'reading_by': RB,
     'source': 'US 14 CFR 1.2, "Abbreviations and symbols" (FAA): the definition of V1 (used by 14 CFR 25.107 and 25.109, '
               'take-off speeds and accelerate-stop distance)',
     'version': 'Code of Federal Regulations, Title 14, vol. 1, revised as of 1 January 2025 (govinfo annual edition), fetched '
                '2026-09-30',
     'url': 'https://www.govinfo.gov/content/pkg/CFR-2025-title14-vol1/pdf/CFR-2025-title14-vol1-sec1-2.pdf',
     'quote': ['means the maximum speed in the takeoff at which the pilot must take the first action (e.g., apply brakes, reduce '
               'thrust, deploy speed brakes) to stop the airplane within the accelerate-stop distance.',
               'also means the minimum speed in the takeoff, following a failure of the critical engine at VEF, at which the '
               'pilot can continue the takeoff and achieve the required height above the takeoff surface within the takeoff '
               'distance.'],
     'raw_file': T + 'cfr2025_14_1_2.txt',
     'agent_note': 'Close for P3 (addition B2: another vehicle class). Transport-category certification selects the safe response '
                   'to an emergency (stop, or continue) from the vehicle\'s own progress through the take-off (a speed, V1), '
                   'not from a clock: phase-dependent safe-state selection written into a regulation. Not a legged robot.'},
]

READING_CHECKS = [
    {'claim_id': 'r1a:1', 'agree': True,
     'note': 'Justified: the quoted flow defers the emergency stop until the attitude can hold a stopped state (CoG over the '
             'supporting foot, ZMP in the stable region), and the patent ties that to the support phase ("particularly unstable '
             'during one-leg support period"). The trigger is a state test rather than an explicit phase variable, which the '
             'caller\'s list ("stop at the next stance") covers.'},
    {'claim_id': 'r1a:2', 'agree': True,
     'note': 'Justified: the stop motion starts from the Landing phase in single support and from the ZMP Transition phase in '
             'double support. B\'s r1b:4 (the same group, 2008) adds the deferral form: a stop commanded in single support begins '
             'at the next double support.'},
    {'claim_id': 'r1a:3', 'agree': True,
     'note': 'Justified as close: "within one step" against "more than two steps" is qualitative, and the comparator (patterns '
             'connected at each step) is itself keyed to the gait\'s step boundary. Morisawa 2008 (r1b:5) makes the same point '
             'about the cost of waiting for a phase event.'},
    {'claim_id': 'r1a:4', 'agree': True,
     'note': 'Justified, and confirmed from the full text: the journal version (r1b:7, r1b:8) defines the command timing tc from '
             'the start of single support and selects the stop mode, landing position and landing time from it.'},
    {'claim_id': 'r1a:5', 'agree': True,
     'note': 'Justified; the same confirmation from the journal full text (r1b:8).'},
    {'claim_id': 'r1a:6', 'agree': True,
     'note': 'Justified only under the caller\'s list, which names capture-point stopping as an instance of C-R1: the stopping '
             'strategy is chosen from the state (capture region against the base of support), not from a gait-phase variable. '
             'Read strictly as phase-keying it would be close. The grade does not rest on it: r1a:2, r1b:1, r1b:4 and r1b:8 state '
             'P1 on explicit phase.'},
    {'claim_id': 'r1a:7', 'agree': True,
     'note': 'Justified: the stand command is deferred to a foot-apex phase. It is an operational (end-of-run) stop, not a '
             'safety function; A\'s policy includes commanded stops. van Marum et al. (r1b:10) independently describe it as '
             '"hand-engineered cycle-time constraints", though from the same laboratory.'},
    {'claim_id': 'r1a:8', 'agree': True,
     'note': 'Justified under the policy (falls, hardware and simulation, phase-timed against immediate). Cautions A states '
             'hold: approximate counts ("less than 10%", "about 2 in 3"), the 100% arm confounded with a speed-command change, '
             'an operational stop, and an immediate comparator rather than the best clock-delayed stop. r1b:9 is a second, '
             'computed P2 comparison.'},
    {'claim_id': 'r1a:9', 'agree': True,
     'note': 'Justified as close: completion gated by double support with a 1.5 s clock hysteresis; operational, not a safety '
             'stop.'},
    {'claim_id': 'r1a:10', 'agree': True,
     'note': 'Justified as close: halt zeroes the command at once (relying on a capturability constraint), stop ramps over a '
             'fixed 2 s arrest time; neither is phase-keyed.'},
    {'claim_id': 'r1a:11', 'agree': True,
     'note': 'Justified as close: the phase dependence is stated and no phase-keyed stop is designed.'},
    {'claim_id': 'r1a:12', 'agree': True,
     'note': 'Justified: ISO 13855 sizing with the worst-case (single-support) stopping time is the clock-sized stop; evidence '
             'against P3 for that route only. The same worst-phase sizing is OSHA practice for presses (r1b:14).'},
    {'claim_id': 'r1a:13', 'agree': True,
     'note': 'Justified as close: a state-conditioned stop whose inputs exclude the motion phase; the authors name the '
             'continue-then-stop variant as unaddressed.'},
    {'claim_id': 'r1a:14', 'agree': True,
     'note': 'Justified as close: a state-conditioned stop-or-fall decision against always-stop; not phase.'},
    {'claim_id': 'r1a:15', 'agree': True,
     'note': 'Justified as close: the proposal grades e-stop levels and names swing-phase capturability as a stability '
             'criterion, and its double-stance, no-step mode (context checked) is a collaborative operating mode, not a '
             'phase-timed stop.'},
    {'claim_id': 'r1a:16', 'agree': True,
     'note': 'Justified as close, and reinforced: the same patent\'s method 350 gives the stop command a time limit and picks a '
             'reconfiguration whose known implementation time fits it (r1b:12), so the stop\'s timing is on the clock; the '
             'swing-foot-down deceleration shapes the stop by contact state without phase-keyed timing.'},
    {'claim_id': 'r1a:17', 'agree': True,
     'note': 'Justified as contradicts; second-hand, but now corroborated by the primary patent text (r1b:12).'},
    {'claim_id': 'r1a:18', 'agree': True,
     'note': 'Justified: the settle-then-cut E-stop cuts power after a clock timeout "regardless of current robot state".'},
    {'claim_id': 'r1a:19', 'agree': True,
     'note': 'Justified as close under the policy (a patent without evidence of deployment). B adds that a phase-keyed stop '
             'was in public operation for 185 days at Expo 2005 (r1b:6) and in exhibition use on HRP-2 (r1b:3), still neither '
             'certified nor industrial.'},
    {'claim_id': 'r1a:20', 'agree': True,
     'note': 'Justified as close: humans, not robots.'},
]

# Quotes corrected to the verbatim source text, or dropped, after a NOT FOUND in Robotics/checks/verify_s3.py; one dict per
# quote: {'id', 'quote_index', 'action': 'corrected' | 'dropped', 'old', 'new', 'reason'}. The first run of verify_s3.py
# (2026-09-30, root /tmp/claude-0/rob_s3) found every quote of this module verbatim, so nothing was corrected or dropped.
VERIFY_CORRECTIONS = []
