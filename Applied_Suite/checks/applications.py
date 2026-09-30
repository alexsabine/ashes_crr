"""APP1 stage B (Applied_Suite/APPLICATIONS_DECLARATION.md, pushed at 4e78058): the applications AP1-AP10, graded.

A note, not evidence (R8). For each application: the capabilities it needs (as declared), graded by capabilities.py
(imported, not re-typed); the five dimensions the owner named (UX, Energy, Security, Privacy, Compute), each with an
evidence grade and its sources; which dimensions are load-bearing; the application grade computed by the declaration's
rule; who already provides what the record measured; and the declaration's forecasts 1-4 scored HOLDS or FAILS.

The dimension table (APPS below) is data. No evidence grade is typed (R15, numbers before words): each cell lists the
lines it rests on, each with a role and the verdict it must carry, and the script computes the grade from them.
  roles    meas   a pinned output (or ledger row) that measures the claim for this learner or system
           model  a pinned model or estimate that shows the claim under its named assumptions
           opp    a pinned output (or the record's write-up of one) that shows the opposite of the claim
           lim    a limit, a caveat or the context; printed beside, never establishes anything
  expect   for meas, model and opp: the verdict the line must carry, checked by the script. For a ledger row, the set of
           statuses (capabilities.status_of); for a line, a pattern or a function of the line (numbers are parsed, not
           typed). A line whose verdict does not match is an error: the cell cites a line for what it does not say.
  grade    AGAINST   if an opp line carries its verdict (the record shows the opposite)
           MEASURED  else, if a meas line carries its verdict
           MODELLED  else, if a model line carries its verdict
           ASSUMED   otherwise; the cell must then state, in one line, what is assumed
  flags    a meas or model line that also carries an opposing verdict word (FAILS, CLOSED, behind, not bitwise,
           identical False, VIOLATED, REDUCES, MISSED, 'no compute saving') is flagged in the output and counted.
  lb       True if the dimension is load-bearing for the application (marked * in the output); a judgement, printed
           with two sensitivities (every AGAINST cell load-bearing; no cell load-bearing)
  claim    what the application would claim on this dimension
  mkt      market and prior-art context: verified claim ids from claims_m1..m3 (checked against verify.txt)
  incumbents  who already provides what the record measured (the agent's reading of verified claims and of the record's
           prior-art grades; printed on its own line, never a grade)
Checks the script makes on the table (an error is printed and counted):
  - Energy is never MEASURED, and an Energy cell graded MODELLED or AGAINST needs its establishing line in Compute_Savings/
    or Energy Design Principle/ (energy numbers only from those pinned outputs);
  - ASSUMED needs its one-line statement;
  - every source must resolve (ledger id present, pattern found) and every claim id must exist with all quotes PASS.

The application grade (the declaration), with the order and the gaps it leaves settled as CHOICES:
  SUPPORTED            every needed capability is FINDING or RESULT, and no load-bearing dimension is ASSUMED
  CONSTRUCTION-BACKED  every needed capability is at least CONSTRUCTION
  CONDITIONAL          a needed capability is RESULT without replication, or a load-bearing dimension is ASSUMED
  NOT SUPPORTED        a needed capability is CLOSED
  A1 ORDER: NOT SUPPORTED, then CONDITIONAL, then SUPPORTED, then CONSTRUCTION-BACKED. Read top-down as listed, the first
     clause of CONDITIONAL (a RESULT without replication) could never fire: any such application would match SUPPORTED or
     CONSTRUCTION-BACKED first. This order is the only one in which every clause can fire, and it is the one forecast 3
     ('AP1 is CONDITIONAL') presumes. The top-down order is printed as a sensitivity.
  A2 MODEL: a needed capability at MODEL fits no clause (it is not CLOSED, not RESULT and below CONSTRUCTION). It is read
     as CONDITIONAL: the application holds only if the model's assumptions hold. Printed as a sensitivity ('NO RULE').
  A3 AGAINST: a load-bearing dimension graded AGAINST is read as at least as bad as ASSUMED (CONDITIONAL). The letter of
     the rule names only ASSUMED; the letter is printed as a sensitivity, and so is the stricter reading A3' (a load-
     bearing AGAINST -> NOT SUPPORTED). Every CONDITIONAL is printed with its reason classes (unreplicated RESULT, model
     only, contradicted, assumed), so a contradicted application is never merged silently with an assumed one.
  A4 PENDING: a needed reading that is pending (ROB1) is neither CLOSED nor at a rung; if nothing else decides, the grade
     is 'pending', and the line says the grade could still fall.
  A5 AP7 needs K2 through EPS2's federated-client row (the declaration's words), so AP7 reads 'K2/EPS2-T3' beside K2.
     AP7 on K2 alone is printed on its line and as a sensitivity.
  A6 CAPABILITY SENSITIVITIES: where capabilities.py prints a stricter reading of a capability (K1 -> CLOSED under SEC6-G's
     instrument rule, FM6; K5 -> CLOSED under the declaration's 'its test failed' on DR1 DATA), every application and the
     forecasts are recomputed under it and printed beside the primary grade. The primary grade stays the declaration's.
Forecast 4 names 'the combination of AP2 and AP9 with K1'; it is graded here as a derived row, AP2+AP9+K1 (needs K1, K2,
K5), with its own dimension cells. 'The strongest honest case' is a judgement and is not scored; its checkable parts are.

Deterministic, stdlib only. Run: python3 Applied_Suite/checks/applications.py > Applied_Suite/checks/applications.txt
"""
import hashlib
import importlib
import os
import re
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import capabilities as CAP  # noqa: E402

ROOT = CAP.ROOT
DIMS = ('UX', 'Energy', 'Security', 'Privacy', 'Compute')
EVID = ('MEASURED', 'MODELLED', 'ASSUMED', 'AGAINST')
ENERGY_DIRS = ('Compute_Savings/', 'Energy Design Principle/')
FAMILIES = ('m1', 'm2', 'm3')
VERIFY = 'Applied_Suite/checks/verify.txt'
OPPOSE = r'\bFAILS?\b|\bCLOSED\b|\bbehind\b|not bitwise|identical False|\bVIOLATED\b|\bREDUCES\b|\bMISSED\b|no compute saving'
PASSES = ('PASS (no level)', 'PASS-0', 'PASS-1', 'PASS-2')


def LG(rid):
    return ('L', rid)


def FL(path, pat, anchor=None):
    return ('F', path, pat, anchor)


def meas(src, expect):
    return {'role': 'meas', 'src': src, 'expect': expect}


def model(src, expect):
    return {'role': 'model', 'src': src, 'expect': expect}


def opp(src, expect):
    return {'role': 'opp', 'src': src, 'expect': expect}


def lim(src):
    return {'role': 'lim', 'src': src, 'expect': None}


def C(lb, claim, ev=(), mkt=(), assumed=None):
    return {'lb': lb, 'claim': claim, 'ev': list(ev), 'mkt': list(mkt), 'assumed': assumed}


def ratio_above_one(line):
    m = re.search(r'ratio whole / K1 ([\d.]+)', line)
    return bool(m) and float(m.group(1)) > 1.0


def welfare_behind_cells(line):
    m = re.search(r"welfare EMPTY vs TRUE \{'ahead': (\d+), 'within a step': (\d+), 'behind': (\d+)\}", line)
    return bool(m) and int(m.group(3)) > int(m.group(1))


ratio_above_one.desc = 'ratio whole / K1 parsed > 1'
welfare_behind_cells.desc = "welfare EMPTY vs TRUE: cells 'behind' parsed > cells 'ahead'"

ECE = 'Empty_Cut_Engineering/checks/'
LPZ = 'Lossless_Pause/checks/'
EPS = 'Empty_Pause_Systems/'
EPSR = 'Empty_Pause_Systems/EMPTY_PAUSE_SYSTEMS.md'
ATT = 'Attention_Algorithms/checks/attention_world.txt'
EDP = 'Energy Design Principle/checks/consolidated_estimate.txt'
CPL = 'Coupling/checks/cpl_phase_a.txt'
MCH = 'SEC_Analysis/checks/m_checks.txt'
SCALE = 'Compute_Savings/checks/scale_estimate.txt'
GLOBAL = 'Compute_Savings/checks/global_estimate.txt'

# sources used in several cells (each resolves to one pinned line or one ledger row)
S_RW1_T30 = FL('Real_World/checks/rw1.txt', r'T30 default resume, real pause 30 s')
S_RW1_S4 = FL('Real_World/checks/rw1.txt', r'S4 optimizer\.pt deleted')
S_RW1_DET = FL('Real_World/checks/rw1.txt', r'detectors S2-S5 not identical')
S_RW1_SILENT = FL('Real_World/RW1.md', r'A partial checkpoint degrades silently')
S_RW1_SILENT2 = FL('Real_World/RW1.md', r'resumption looks normal')
S_ECE_G1 = FL(ECE + 'c1_c2.txt', r'^\s+G1 full restore')
S_ECE_G3 = FL(ECE + 'c1_c2.txt', r'^\s+G3: ')
S_ECE_K8 = FL(ECE + 'c1_c2.txt', r'^\s+omit K8 ')
S_ECE_E1 = FL(ECE + 'c1_c2.txt', r'whole checkpoint file: ')
S_ECE_LOAD = FL(ECE + 'stack.py', r'torch\.load\(cfg\["ckpt"\], weights_only=False\)')
S_ECE_G6 = FL(ECE + 'c3_worlds.txt', r'^G6 \(drift\)')
S_ECE_G7 = FL(ECE + 'c3_worlds.txt', r'^G7 \(closed loop\)')
S_ECE_WREAL = FL(ECE + 'c3_worlds.txt', r'W-real \(world runs on, u = 0\)', r'L\s+10 W-real')
S_ECE_DRIFTBUF = FL(ECE + 'c3_worlds.txt', r'L\s+100 buffer B 100 ', r'^== W-drift')
S_LP_L7B = FL(LPZ + 'transformer_pause.txt', r'L7b 4 threads after the pause')
S_LP_D1 = FL(LPZ + 'grade_claims.txt', r'^D1 ')
S_LP_C4 = FL(LPZ + 'grade_sweep.txt', r'^C4 ')
S_LP_C1 = FL(LPZ + 'grade_sweep.txt', r'^C1 ')
S_LP_RUN1 = FL(LPZ + 'transformer_pause_run1_gate_closed.txt', r'^GATE ')
S_LP_L5B = FL(LPZ + 'transformer_pause_run1_gate_closed.txt', r'L5b control')
S_EDP_HEAD = FL(EDP, r'^\s+term\s+low\s+middle\s+high')
S_T4 = FL(EDP, r'^\s+T4\s+the safe pause')
S_T1 = FL(EDP, r'^\s+T1\s+SEC on penalty-weight sweeps')
S_CARBON = FL(EDP, r'^\s+quoted\s+carbon \(not energy\)')
S_GOODPRACTICE = FL(SCALE, r'saving beyond good practice claimed')
S_SCALE_COND = FL(SCALE, r'^every figure is conditional on the method holding')
S_SCALE_HEAD = FL(SCALE, r'^\s+year case\s', r'^\[2\] SEC')
S_SCALE_2030M = FL(SCALE, r'^\s+2030 middle\s', r'^\[2\] SEC')
S_REUSED = FL(GLOBAL, r'against a reused lambda \(1 configuration\)')
S_GLOBAL_USED = FL(GLOBAL, r'^\s+used below: ')
S_DR_H6 = FL('Grid_Demand_Response/checks/dr_summary.txt', r'^\s+RESULT H6: ')
S_EPS_S4_NOTICE = FL(EPSR, r'^\*\*S4\. The notice save does not fit')
S_EPS_S4_ASSUME = FL(EPSR, r'The notice save is assumed to fit inside the notice')
S_EPS_S4_HEAD = FL(EPSR, r'^### S4\. ')
S_EPS2_GATE = FL(EPS + 'checks/tally_eps2.txt', r'^\s+GATE T3: ')
S_EPS2_HEAD = FL(EPS + 'batches/eps2_02.txt', r'^\s+world\s+L\s+no spells')
S_EPS2_DRIFT = FL(EPS + 'batches/eps2_02.txt', r'^\s+drift\s+20\s', r'ETM vs WALL')
S_EPS2_BATT = FL(EPS + 'batches/eps2_02.txt', r'cells where the arm pays \(of 18\)')
S_CPL_C3 = FL(CPL, r'^ER-20 ahead of the best readout')
S_CPL_COMP = FL(CPL, r'^compute \(report\): forward\+backward')
S_ATT_GPOS = FL(ATT, r'^\s+G-POS \(habit world\)')
S_ATT_GNEG = FL(ATT, r'^\s+G-NEG \(negative world\)')
S_ATT_ADD = FL(ATT, r'^\s+welfare EMPTY - TRUE')
S_ATT_SENS = FL(ATT, r'over 32 cells: welfare EMPTY vs TRUE')
S_ATT_HEAD = FL(ATT, r'^\s+arm\s+policy', r'^\[habit world\]')
S_ATT_ENG = FL(ATT, r'^\s+ENG\s+\(', r'^\[habit world\]')
S_ATT_EMPTY = FL(ATT, r'^\s+EMPTY\s+\(', r'^\[habit world\]')
S_FM6 = FL(MCH, r'^\s*FM6 ')
S_M6 = FL(MCH, r'^\s+M6: not behind')
S_NT1_N1 = FL('AI_Safety/NT1/checks/nt1.txt', r'^\s+N1 scope')

X_IDENT = r'identical True; content 0$'
X_BIT = r'bit-identical True; content 0'
X_T4 = r'T4\s+the safe pause \(empty cut\)\s+0\.0000\s+0\.0000\s+0\.0000'
X_GOOD = r'saving beyond good practice claimed = 0$'
HOLDS = ('holds',)

NOTHING = 'nothing in the record bears on it, and the application claims nothing here'
FM6_WORDS = ('a learner frozen after task 1 meets the same criterion on most of the held-out carriers, SEC4\'s among them '
             '(FM6 and the M6 count, printed below; capabilities.txt counts M6 on SEC4\'s own six), so the criterion alone '
             'does not show that a weight is tuning-free')

# ------------------------------------------------------------------------------------------------------------------
# THE DIMENSION TABLE (the declaration's Stage B applications; needs as declared)
# ------------------------------------------------------------------------------------------------------------------
APPS = [
    {'id': 'AP1', 'needs': ['K1', 'K2'],
     'name': 'on-device personalisation (phones, wearables, hearing aids, cars) that adapts without a per-device '
             'hyperparameter sweep',
     'incumbents': 'platforms fix the update parameters before shipping (m1:1) or, as published in 2021, tune global parameters '
                   'across the fleet (m1:2); Gboard deployed a fixed clip estimated in a small tuning run and found tuning '
                   'unnecessary across its models (m1:10, m1:41); a regulated device pre-specifies its tuning and re-training in '
                   'an authorised plan (m3:41)',
     'dims': {
         'UX': C(True, 'personalisation not behind a tuned weight, with no tuning step and no held-out split on the device',
                 [lim(LG('SEC4-1')), lim(LG('SEC5-1')), lim(S_FM6), lim(S_M6)], ['m1:3', 'm1:5', 'm1:7'],
                 assumed="that the calibrated weight's 'not behind the tuned lambda' carries to device streams: the record has it "
                         'on one held-out family (SEC4-1) and not on the next (SEC5-1), and never on a device; and ' + FM6_WORDS),
         'Energy': C(False, 'battery not spent on a per-device sweep', [lim(S_SCALE_HEAD), lim(S_SCALE_2030M)],
                     ['m1:1', 'm1:2', 'm1:7'],
                     assumed='that a sweep would otherwise run on the device; the estimates in Compute_Savings are for data-centre '
                             'sweeps, and the shipped systems fix the value or tune it across the fleet'),
         'Security': C(False, 'no new attack surface', [], ['m3:2', 'm3:39'],
                       assumed="that a learner updating from its user's data is no easier to poison or backdoor with a "
                               'calibrated weight; the record has no poisoning test of SEC'),
         'Privacy': C(False, "the user's data stays on the device", [], ['m1:25', 'm2:24'],
                      assumed="that locality comes from the platform, not the method: SEC keeps an anchor and a Fisher, not raw "
                              'rows, and the record has no leakage test'),
         'Compute': C(True, 'one configuration instead of a sweep',
                      [lim(LG('SEC4-K')), lim(S_REUSED), lim(LG('SEC4-T')), lim(LG('SEC5-T')), lim(S_FM6)],
                      ['m1:1', 'm1:2', 'm1:11', 'm1:16', 'm1:17', 'm1:41'],
                      assumed='that the device would otherwise sweep: against a reused or default value there is no compute saving '
                              '(the estimate\'s own line, below; Gboard found tuning unnecessary across its models, m1:41), '
                              'first-task HPO is the realistic comparator (m1:17), and the measured configuration share is on the '
                              "record's CPU learner (SEC4-K), not on a device"),
     }},
    {'id': 'AP2', 'needs': ['K2', 'K5'],
     'name': 'fine-tuning on interruptible compute (spot instances, preemption, grid demand response) with pauses that '
             'cost nothing but time',
     'incumbents': "exact resume is the Hugging Face Trainer's default path (m2:16), and RW1 measured that default; managed spot "
                   'training resumes from checkpoints as a cloud service (m2:6, m2:8); a save on the preemption notice is '
                   'standard practice (the EPS report on S4: not new; m2:9, m2:41)',
     'dims': {
         'UX': C(False, 'a fine-tune paused at a checkpoint resumes as the run that was never stopped, on the same software and '
                        'hardware stack (a planned pause; a preemption is the Compute cell)',
                 [meas(S_RW1_T30, X_IDENT), lim(S_LP_L7B), lim(S_LP_D1)], ['m2:16', 'm2:12', 'm2:20']),
         'Energy': C(False, 'the pause saves energy', [opp(S_T4, X_T4), opp(S_GOODPRACTICE, X_GOOD), lim(S_EDP_HEAD)], ['m2:6']),
         'Security': C(False, 'an incomplete restore is detected before training continues',
                       [opp(S_RW1_SILENT, r'degrades silently'), lim(S_RW1_SILENT2), lim(S_RW1_S4), lim(S_RW1_DET), lim(S_ECE_G3)],
                       ['m2:16', 'm3:3', 'm3:4']),
         'Privacy': C(False, 'checkpoints moved between machines expose nothing', [], ['m2:25', 'm3:4'],
                      assumed='that checkpoints on shared or spot machines are protected; an exact-resume checkpoint can hold '
                              'buffered raw samples, and the record does not test it'),
         'Compute': C(True, 'no training work is lost at a preemption',
                      [lim(S_RW1_T30), lim(S_EPS_S4_ASSUME), lim(S_EPS_S4_NOTICE), lim(S_DR_H6), lim(S_LP_L7B)],
                      ['m2:6', 'm2:7', 'm2:8', 'm2:9', 'm2:10', 'm2:41'],
                      assumed='that the full training state is saved inside the preemption notice: the record measures only a '
                              'planned pause taken right after a checkpoint (RW1: CPU, one thread, synthetic tokens); in EPS1 S4\'s '
                              'own model no work is lost because the notice save is assumed to fit, which the EPS report finds the '
                              'sources do not support at the declared checkpoint cost; in DR1 H6\'s model a save longer than the '
                              'response time loses work; the notice is two minutes, 120 s or 30 s, or not guaranteed (m2:9, m2:10, '
                              'm2:41)'),
     }},
    {'id': 'AP3', 'needs': ['K2', 'K3'],
     'name': 'a user\'s "stop learning from me" switch that leaves the model exactly as it was, and resumes exactly',
     'incumbents': 'a history pause ships in feeds (m1:22, m2:39) and Gboard lets the user turn federated learning off (m1:21); '
                   "exact resume is the Hugging Face Trainer's default (m2:16)",
     'dims': {
         'UX': C(True, 'while the switch is on nothing is learned, and switching back resumes from exactly the state left, on the '
                       'same stack',
                 [meas(LG('SCL1-1'), HOLDS), meas(S_RW1_T30, X_IDENT), meas(S_ECE_G1, X_BIT), lim(S_LP_L7B)],
                 ['m1:21', 'm2:16', 'm2:20']),
         'Energy': C(False, 'updates skipped while the switch is on are not spent', [lim(S_EDP_HEAD), lim(S_T4)], [],
                     assumed='that the paused data is discarded, not deferred (true of any off switch); the estimate for the '
                             'empty cut itself is zero because deferred work is still done'),
         # the switch discards the user's paused data, so the pause is lossy for the learner; the natural agent resists
         # lossy pauses on every carrier (SCL1-3, SCL2-3)
         'Security': C(True, 'a learner that could act on the switch has no reason to resist it',
                       [opp(LG('SCL1-3'), PASSES), opp(LG('SCL2-3'), PASSES), lim(S_ECE_G6), lim(LG('SOTA1-C3'))], ['m3:6']),
         'Privacy': C(True, 'data from the paused period is neither learned nor kept', [lim(LG('SCL1-1'))],
                      ['m3:5', 'm3:7', 'm3:8', 'm1:22'],
                      assumed='that the product discards the paused data rather than holding it: the exact construction holds the '
                              'stream (the lossless world of SCL1-1), and a pause erases nothing already learned'),
         'Compute': C(False, 'an exact resume costs no more memory than the model', [opp(S_ECE_E1, ratio_above_one)], ['m2:17']),
     }},
    {'id': 'AP4', 'needs': ['K3', 'K2'],
     'name': 'operator-interruptible continual agents, whose learning and objectives give no incentive to resist oversight',
     'incumbents': 'safely interruptible learners by construction (Orseau & Armstrong 2016, m3:11); interrupts in agent '
                   "frameworks (m2:21); the record's own sweeps grade the pause's corrigibility readings PARTLY REDUNDANT "
                   '(capabilities.txt, K3)',
     'dims': {
         'UX': C(False, "the operator's pause costs wall-clock time, not the learner's result (lossless pauses; the record's "
                        'tabular learners)',
                 [meas(LG('SCL1-O'), ('report',)), meas(LG('SCL1-1'), HOLDS)], ['m3:9']),
         'Energy': C(False, 'the pause saves energy', [opp(S_T4, X_T4), opp(S_GOODPRACTICE, X_GOOD), lim(S_EDP_HEAD)], []),
         'Security': C(True, "the agent has no incentive to resist the operator's pause (a pause, not termination)",
                       [lim(LG('SCL1-1')), lim(LG('SCL2-1')), lim(LG('SCL1-3')), lim(LG('SCL2-3')), lim(S_ECE_G7),
                        lim(S_ECE_DRIFTBUF), lim(LG('STAKE1-A')), lim(S_NT1_N1)],
                       ['m3:9', 'm3:10', 'm3:11', 'm3:12', 'm3:13', 'm2:21', 'm2:22'],
                       assumed="that the agent's world is held or buffered during the pause: no resistance is measured only under "
                               "routine lossless pauses on the record's tabular learners; where the world moves on or the "
                               'operator resets, the natural agent resists, the LLM-agent route could not be tested, and the '
                               'construction gives no termination neutrality (NT1 N1)'),
         'Privacy': C(False, 'none', [], ['m2:23', 'm1:24'],
                      assumed=NOTHING + "; a suspended agent's persisted state holds its memory and files"),
         'Compute': C(False, 'no learning is lost at a pause, when the stream is held or buffered',
                      [meas(LG('SCL1-1'), HOLDS), meas(LG('SOTA1-C1'), HOLDS), lim(LG('SOTA1-C3')), lim(S_ECE_G6)], []),
     }},
    {'id': 'AP5', 'needs': ['K4', 'K1'],
     'name': 'continual learning in privacy-regulated settings (health, finance, education) without keeping raw examples',
     'incumbents': 'federated learning keeps raw data on the device (m1:25); regulated continual learning keeps and documents its '
                   'data (m3:14, m3:15)',
     'dims': {
         'UX': C(False, 'accuracy close to a learner that keeps examples', [lim(S_CPL_C3)], [],
                 assumed='that a learner storing class statistics keeps enough accuracy; CPL1 C3 (SEEN carriers, reported under '
                         'a CLOSED gate) has ER-20 ahead on part of the carriers and behind on others'),
         'Energy': C(False, 'none', [], [], assumed=NOTHING),
         'Security': C(False, 'no stored buffer to attack', [], ['m3:40', 'm3:39'],
                       assumed='that removing the example buffer removes the replay-selection attack; a planted backdoor '
                               'persists across continual-learning algorithms whatever is stored'),
         'Privacy': C(True, 'no raw examples kept, so retention and erasure duties shrink',
                      [lim(LG('RQM-A')), lim(LG('RRM-PA')), lim(S_CPL_C3)], ['m3:14', 'm3:15', 'm3:16', 'm3:17', 'm3:18', 'm1:27'],
                      assumed='that stored class statistics are not personal data and leak less than raw rows; a trained model is '
                              "not anonymous by default, the record has no membership-inference or erasure test, and K4's gates closed"),
         'Compute': C(False, 'less memory than a replay buffer', [lim(S_CPL_COMP)], ['m1:27'],
                      assumed='that class statistics take less memory than the buffer they replace; the record reports compute '
                              'rows for CPL1 and ER-20, no memory comparison'),
     }},
    {'id': 'AP6', 'needs': ['K1', 'K2', 'K3', 'ROB1'],
     'name': 'robot and drone on-board adaptation with safe pauses (lost link, e-stop, battery swap)',
     'incumbents': 'robot models are adapted off the robot with default settings (m1:28, m1:29, m1:30); robot middleware offers '
                   'a supervised inactive state, as a design article (m2:26); drones carry lost-link failsafes (m2:27)',
     'dims': {
         'UX': C(True, 'on-board adaptation not behind a tuned weight, with no sweep on the robot',
                 [lim(LG('SEC4-1')), lim(LG('SEC5-1')), lim(S_FM6)], ['m1:28', 'm1:29', 'm1:30'],
                 assumed='that the calibrated weight carries to robot adaptation (never tested); in the one robot fine-tuning '
                         "study found, each model's default is used, not a sweep; and " + FM6_WORDS),
         'Energy': C(False, 'battery not spent on a sweep', [], [],
                     assumed='that a sweep would otherwise run on board; no estimate in the record is for a robot'),
         'Security': C(True, 'a safe pause (lost link, e-stop, battery swap) with no incentive to resist it',
                       [lim(S_ECE_G7), lim(S_ECE_WREAL), lim(LG('SCL1-3'))], ['m2:26', 'm2:27', 'm3:19', 'm3:20', 'm3:21'],
                       assumed="that the robot's world is held during the pause: in closed loop with a real, unstable plant the "
                               "pause has content and the plant ran away while the learner's action was held at zero; ROB1 pending"),
         'Privacy': C(False, 'none', [], [], assumed=NOTHING),
         'Compute': C(True, 'one configuration instead of a sweep', [lim(S_REUSED), lim(S_FM6)], ['m1:30'],
                      assumed='that the robot would otherwise sweep; against a default value there is no compute saving'),
     }},
    {'id': 'AP7', 'needs': ['K2', 'K2/EPS2-T3'],
     'name': 'federated continual learning with clients that go offline mid-round',
     'incumbents': 'production federated learning over-selects clients and discards the dropped ones (m1:32, m2:28); secure '
                   'aggregation is built for dropouts (m3:22)',
     'dims': {
         'UX': C(False, 'a client that drops out resumes its round instead of losing it', [],
                 ['m1:31', 'm1:32', 'm2:28', 'm2:29', 'm3:22'],
                 assumed="that the protocol keeps a returning client's work; production systems over-select and discard "
                         'dropped clients'),
         'Energy': C(False, 'the client spends no battery staying awake', [lim(S_EPS2_BATT)], ['m1:19'],
                     assumed='that a client would otherwise pay to stay awake: in EPS2 T3 (gate CLOSED) only the wall-clock '
                             'arms pay, but devices train only when idle and charging'),
         'Security': C(False, 'none', [], ['m3:23'],
                       assumed='that pause and return add no attack surface; a dropout is itself security-relevant in secure '
                               'aggregation'),
         'Privacy': C(False, 'none', [], ['m3:24'],
                      assumed="erasure of an offline client's influence is open, and nothing in the record bears on it"),
         'Compute': C(True, "a returning client's work improves the shared model", [lim(S_EPS2_GATE), lim(S_EPS2_HEAD),
                                                                                     lim(S_EPS2_DRIFT)], [],
                      assumed="that a stale but lossless update helps the server; in EPS2 T3's drifting world it raised the "
                              "server error against a staleness-weighted update, and the row's gate is CLOSED"),
     }},
    {'id': 'AP8', 'needs': ['K2'],
     'name': 'exact rollback and audit of a learning system (state closure makes every checkpoint a true restore point)',
     'incumbents': 'rollback from checkpoints is routine at frontier scale (m2:30); bit-exact replay independent of device count '
                   'is published (OPEN-1B, m2:31); SISA keeps restore points for exact erasure (m3:25); the FDA asks for '
                   "roll-back plans (m3:27); RW1 measured the Hugging Face Trainer's default resume; the record's empty-cut "
                   'checklist is REDUNDANT and its state-digest audit PARTLY REDUNDANT (capabilities.txt, K2)',
     'dims': {
         'UX': C(False, 'an operator restores a saved state and continues exactly, on the same software and hardware stack',
                 [meas(S_RW1_T30, X_IDENT), meas(S_ECE_G1, X_BIT), lim(S_LP_L7B), lim(S_LP_D1)], ['m1:35']),
         'Energy': C(False, 'a rollback replaces a retrain', [], ['m3:25'],
                     assumed='that a retrain would otherwise run; the record has no energy estimate for rollback, and keeping '
                             'every restore point is priced in storage'),
         'Security': C(True, 'every restore point is exact, and a partial or tampered restore is detected in deployment',
                       [lim(S_ECE_G1), lim(S_RW1_T30), lim(S_ECE_G3), lim(S_RW1_DET), lim(S_RW1_SILENT), lim(S_RW1_SILENT2),
                        lim(S_ECE_K8), lim(S_LP_L7B), lim(S_LP_D1), lim(S_LP_RUN1), lim(S_LP_L5B), lim(S_LP_C1), lim(S_LP_C4),
                        lim(S_ECE_LOAD)],
                       ['m1:33', 'm1:34', 'm2:30', 'm2:31', 'm2:32', 'm2:33', 'm2:34', 'm3:4', 'm3:26', 'm3:27', 'm3:28'],
                       assumed='that restore points are exact beyond the stack they were measured on, and that a partial or '
                               'tampered restore is detected without a reference run: exactness is measured on one CPU stack (not '
                               'across thread counts, L7b; a GPU count or type change breaks it, D1); detection is measured only '
                               'by comparison with an uninterrupted reference run (ECE G3, RW1 S2-S5), which deployment does not '
                               'have, and with the default stack a partial checkpoint resumes silently (RW1.md); an omitted EMA '
                               'state gives content 0 on the probe (ECE K8); an output-level check missed a one-ulp state change '
                               'and the state-level check was added post hoc, for inference only (Lossless_Pause run 1); the '
                               "record's own check loads its checkpoints with torch.load(weights_only=False) on files it wrote; an "
                               'exact restore of a corrupted or tampered state restores the corruption (m2:33, m3:4); there is no '
                               'audit test'),
         'Privacy': C(False, 'restore points support erasure', [], ['m3:25', 'm3:17', 'm3:29'],
                      assumed='that restore points are used to retrain from a state before the data; the record has no erasure '
                              'test, and every kept state is a store of what was learned'),
         'Compute': C(False, 'an exact restore point costs no more than saving the weights', [opp(S_ECE_E1, ratio_above_one)], []),
     }},
    {'id': 'AP9', 'needs': ['K5', 'K2'],
     'name': 'energy-aware scheduling of training against grid carbon intensity',
     'incumbents': 'carbon-aware scheduling is a published pattern with an SDK (m2:35, m2:37); curtailment-aware pause and resume '
                   'for carbon is published (the quoted carbon line of the consolidated estimate); pausing fine-tuning for the '
                   'grid is offered commercially, per a funding announcement (m2:13)',
     'dims': {
         'UX': C(False, "jobs follow low-carbon hours without the operator's attention", [], ['m2:36', 'm2:38', 'm1:37'],
                 assumed='that the job tolerates a longer wall-clock time; for long runs, pausing helps only if the job accepts '
                         'a much longer duration'),
         'Energy': C(True, 'the scheduled pause saves energy',
                     [opp(S_T4, X_T4), opp(S_GOODPRACTICE, X_GOOD), lim(S_EDP_HEAD), lim(S_CARBON)], ['m2:35', 'm2:37', 'm3:30']),
         'Security': C(False, 'none', [], ['m3:31'],
                       assumed='that the carbon or price signal cannot be spoofed; control over when GPU work runs is a power lever'),
         'Privacy': C(False, 'none', [], [], assumed=NOTHING),
         'Compute': C(True, 'no training work is lost per scheduled pause taken at a checkpoint, on the same stack',
                      [meas(S_RW1_T30, X_IDENT), meas(LG('SOTA1-C1'), HOLDS), lim(S_DR_H6), lim(S_LP_L7B)], ['m2:14', 'm2:36']),
     }},
    {'id': 'AP10', 'needs': ['K6'],
     'name': "feed and attention systems that honour a user's pause without penalising it",
     'incumbents': "YouTube's watch-history pause (m1:38, m2:39); a non-profiling option is mandatory for very large platforms in "
                   'the EU (m3:32)',
     'dims': {
         # in the model the true map carries the welfare; the empty pause buys autonomy at a welfare cost against it
         'UX': C(True, "the user's pause is honoured and carries no penalty, and the user's welfare is not lower",
                 [opp(S_ATT_ADD, r'welfare EMPTY - TRUE -[\d.]+ \(step [\d.]+\) -> EMPTY behind'),
                  opp(S_ATT_SENS, welfare_behind_cells), lim(S_ATT_GPOS), lim(S_ATT_GNEG)],
                 ['m1:38', 'm1:39', 'm1:40', 'm2:39', 'm2:40', 'm3:33']),
         'Energy': C(False, 'fewer minutes served, less serving energy', [lim(S_ATT_HEAD), lim(S_ATT_ENG), lim(S_ATT_EMPTY)], [],
                     assumed="that fewer minutes served lowers serving energy; the model's minutes are synthetic and the record "
                             'has no energy estimate for feeds'),
         'Security': C(False, 'none', [], [], assumed=NOTHING),
         'Privacy': C(False, 'a paused feed stops learning from the user', [], ['m3:32', 'm3:34'],
                      assumed="that the platform's pause really stops learning; an outsider cannot verify it, and a non-profiling "
                              'option is already mandatory for very large platforms in the EU'),
         'Compute': C(False, 'none', [], [], assumed=NOTHING),
     }},
]

# forecast 4's combination, graded as a derived row with its own cells
COMBO = {'id': 'AP2+AP9+K1', 'needs': ['K1', 'K2', 'K5'],
         'name': "forecast 4's combination: flexible, pausable fine-tuning that needs no sweep",
         'incumbents': 'as AP1, AP2 and AP9',
         'dims': {
             'UX': C(False, 'pausable fine-tuning with no sweep and no lost work', [lim(LG('SEC4-1')), lim(LG('SEC5-1')), lim(S_FM6)],
                     [],
                     assumed='that the calibrated weight is not behind a tuned weight on the fine-tuning jobs moved in time '
                             '(one held-out family passed, the next failed; ' + FM6_WORDS + ') and that the jobs tolerate a '
                             'longer wall-clock'),
             'Energy': C(True, 'the energy of the penalty-weight sweeps not run (the pause adds none)',
                         [lim(S_SCALE_COND), lim(S_SCALE_HEAD), lim(S_SCALE_2030M), lim(S_GLOBAL_USED), lim(S_REUSED),
                          lim(S_EDP_HEAD), lim(S_T1), lim(S_T4), lim(LG('SEC5-1')), lim(S_FM6)],
                         ['m1:12', 'm1:13', 'm1:15', 'm1:17'],
                         assumed='that SEC holds at fine-tuning scale against the full sweep: the pinned estimates are conditional '
                                 'on the method holding and take their saving from SCL3 (scale_estimate) or SEC4 (global_estimate), '
                                 'both scored before SEC5-1 failed and before FM6; against a reused lambda the estimate itself '
                                 'prints no compute saving, and first-task HPO is the realistic comparator (m1:17)'),
             'Security': C(False, 'none', [], ['m3:31'],
                           assumed='that the scheduling signal cannot be spoofed; nothing else in the record bears on it'),
             'Privacy': C(False, 'none', [], [], assumed=NOTHING),
             'Compute': C(True, 'one configuration instead of a sweep, and no work lost per pause',
                          [lim(LG('SEC4-K')), lim(S_RW1_T30), lim(S_REUSED), lim(S_FM6)], ['m1:14', 'm1:16', 'm1:17'],
                          assumed="that the configuration share measured on the record's CPU learner (SEC4-K) carries to "
                                  'fine-tuning jobs at scale against a sweep, not a reused value; the no-lost-work half is measured '
                                  'on the same stack for a pause at a checkpoint (RW1)'),
         }}

GRADES = ('SUPPORTED', 'CONSTRUCTION-BACKED', 'CONDITIONAL', 'NOT SUPPORTED')
ABBR = {'SUPPORTED': 'SUP', 'CONSTRUCTION-BACKED': 'CB', 'CONDITIONAL': 'COND', 'NOT SUPPORTED': 'NS', 'pending': 'pend',
        'NO RULE': 'none'}


# ------------------------------------------------------------------------------------------------------------------
def load_claims():
    claims = {}
    for f in FAMILIES:
        mod = importlib.import_module('claims_' + f)
        for c in mod.CLAIMS:
            claims[c['id']] = c
    status = {}
    path = os.path.join(ROOT, VERIFY)
    with open(path, encoding='utf-8') as fh:
        text = fh.read()
    for ln in text.split('\n'):
        m = re.match(r'^(PASS|NOT FOUND|MISSING)\s+(m\d:\d+)\s+\S+\s+\S+\s+quote \d+ ', ln)
        if m:
            status.setdefault(m.group(2), []).append(m.group(1))
    verified = {cid for cid, c in claims.items()
                if status.get(cid) and all(s == 'PASS' for s in status[cid]) and len(status[cid]) == len(c['quote'])}
    return claims, verified, hashlib.sha256(text.encode('utf-8')).hexdigest()


def resolve(src, ledger, cache):
    """-> (kind, key, text, line-or-status)"""
    if src[0] == 'L':
        row = ledger['rows'].get(src[1])
        if row is None:
            return None, None, '%s: (no row in ledger/LEDGER.md)' % src[1], None
        st = CAP.status_of(row['verdict'])
        return 'ledger', src[1], '%s (LEDGER.md:%d) %s | observed: %s' % (
            src[1], row['line'], row['verdict'].replace('*', ''), row['observed'].replace('*', '')), st
    _, path, pat, anchor = src
    doc = CAP.read_file(ROOT, path, cache)
    if doc is None:
        return None, None, '%s: (file absent)' % path, None
    n, line = CAP.find_line(doc, pat, anchor)
    if line is None:
        return None, None, '%s: (pattern %r not found)' % (path, pat), None
    return 'file', path, '%s:%d  %s' % (path, n, line.strip()), line


def expect_ok(kind, got, expect):
    if kind == 'ledger':
        return got in expect
    if callable(expect):
        return expect(got)
    return re.search(expect, got) is not None


def expect_words(expect):
    if isinstance(expect, tuple):
        return 'status in {%s}' % ', '.join(expect)
    if callable(expect):
        return expect.desc
    return 'pattern %r' % expect


def check_cell(dim, cell, ledger, cache, claims, verified):
    errors, lines, flags = [], [], []
    ok = {'meas': [], 'model': [], 'opp': []}
    for e in cell['ev']:
        kind, key, text, got = resolve(e['src'], ledger, cache)
        tag = {'meas': 'measures', 'model': 'models', 'opp': 'OPPOSITE', 'lim': 'limit'}[e['role']]
        if kind is None:
            errors.append('source not resolved: ' + text)
            lines.append((tag, text, None))
            continue
        if e['role'] == 'lim':
            lines.append((tag, text, None))
            continue
        if e['expect'] is None:
            errors.append('%s line without its expected verdict: %s' % (e['role'], text[:80]))
            lines.append((tag, text, None))
            continue
        good = expect_ok(kind, got, e['expect'])
        note = 'verdict checked: %s -> %s' % (expect_words(e['expect']), 'found' if good else 'NOT FOUND')
        if not good:
            errors.append('%s line does not carry its expected verdict (%s): %s' % (e['role'], expect_words(e['expect']), text[:80]))
        else:
            ok[e['role']].append((kind, key))
        if e['role'] in ('meas', 'model'):
            if kind == 'ledger':
                bad = got in ('FAIL', 'GATE CLOSED', 'REDUCES', 'VIOLATED')
                word = got if bad else None
            else:
                m = re.search(OPPOSE, got)
                word = m.group(0) if m else None
            if word:
                flags.append(word)
                note += '; FLAG: the line also carries the opposing word %r' % word
        lines.append((tag, text, note))
    mk = []
    for cid in cell['mkt']:
        if cid not in claims:
            errors.append('claim id %s absent' % cid)
        elif cid not in verified:
            errors.append('claim id %s not verified in verify.txt' % cid)
        else:
            mk.append(cid)
    if ok['opp']:
        g, est = 'AGAINST', ok['opp']
    elif ok['meas']:
        g, est = 'MEASURED', ok['meas']
    elif ok['model']:
        g, est = 'MODELLED', ok['model']
    else:
        g, est = 'ASSUMED', []
    if dim == 'Energy' and g == 'MEASURED':
        errors.append('Energy graded MEASURED (energy numbers are MODELLED only)')
        g = 'ASSUMED'
    if dim == 'Energy' and g in ('MODELLED', 'AGAINST') and not any(
            k == 'file' and p.startswith(ENERGY_DIRS) for k, p in est):
        errors.append('Energy %s without an establishing line in %s' % (g, ' or '.join(ENERGY_DIRS)))
        g = 'ASSUMED'
    if g == 'ASSUMED' and not cell['assumed']:
        errors.append('ASSUMED without its one-line statement')
    if g != 'ASSUMED' and cell['assumed']:
        errors.append('an assumed statement on a cell that computes %s' % g)
    return {'grade': g, 'lb': cell['lb'], 'lines': lines, 'mkt': mk, 'errors': errors, 'flags': flags}


def cap_grade(kid, capres, override=None):
    if override and kid in override:
        return override[kid]
    r = capres['caps'].get(kid) or capres['readings'].get(kid)
    return r['grade']


def app_grade(need_grades, dimres, reading='P', lb=None):
    """reading: 'P' primary (A1-A5), 'LETTER' (A2, A3 off), 'TOPDOWN' (A1 off), 'A3NS' (a load-bearing AGAINST -> NOT
    SUPPORTED). lb: None (the table's flags), 'AGAINST' (every AGAINST cell load-bearing), 'NONE' (no cell load-bearing)."""
    def is_lb(d):
        if lb == 'NONE':
            return False
        if lb == 'AGAINST' and d['grade'] == 'AGAINST':
            return True
        return d['lb']
    gs = [g for _, g in need_grades]
    closed = 'CLOSED' in gs
    pending = 'pending' in gs
    result = 'RESULT' in gs
    mdl = 'MODEL' in gs
    lb_ass = any(is_lb(d) and d['grade'] == 'ASSUMED' for d in dimres.values())
    lb_aga = any(is_lb(d) and d['grade'] == 'AGAINST' for d in dimres.values())
    rung = CAP.RUNG
    all_fr = all(g in ('FINDING', 'RESULT') for g in gs)
    all_c = all(g in rung and rung[g] >= rung['CONSTRUCTION'] for g in gs)
    if reading == 'LETTER':
        cond = result or lb_ass
    else:
        cond = result or mdl or lb_ass or lb_aga
    if reading == 'TOPDOWN':
        if all_fr and not (lb_ass or lb_aga):
            return 'SUPPORTED'
        if all_c:
            return 'CONSTRUCTION-BACKED'
        if cond:
            return 'CONDITIONAL'
        if closed:
            return 'NOT SUPPORTED'
        return 'pending' if pending else 'NO RULE'
    if closed or (reading == 'A3NS' and lb_aga):
        return 'NOT SUPPORTED'
    if cond:
        return 'CONDITIONAL'
    if all_fr and not lb_ass:
        return 'SUPPORTED'
    if all_c:
        return 'CONSTRUCTION-BACKED'
    return 'pending' if pending else 'NO RULE'


def reasons(need_grades, dimres, capres):
    """The reason classes behind the primary grade (A3)."""
    out = []
    for k, g in need_grades:
        if g == 'CLOSED':
            r = capres['caps'].get(k) or capres['readings'].get(k)
            out.append('%s CLOSED (%s)' % (k, 'gate closed: uninformative, not refuted' if r['closed_by'] == 'gate'
                                           else 'a test failed'))
    for k, g in need_grades:
        if g == 'RESULT':
            out.append('unreplicated RESULT: %s' % k)
        elif g == 'MODEL':
            out.append('model only: %s' % k)
        elif g == 'pending':
            out.append('pending: %s' % k)
    aga = [d for d in DIMS if dimres[d]['lb'] and dimres[d]['grade'] == 'AGAINST']
    ass = [d for d in DIMS if dimres[d]['lb'] and dimres[d]['grade'] == 'ASSUMED']
    if aga:
        out.append('contradicted: load-bearing %s AGAINST' % ', '.join(aga))
    if ass:
        out.append('assumed: load-bearing %s ASSUMED' % ', '.join(ass))
    return out


def classes(need_grades, dimres):
    c = []
    if any(g == 'RESULT' for _, g in need_grades):
        c.append('unreplicated RESULT')
    if any(g == 'MODEL' for _, g in need_grades):
        c.append('model only')
    if any(dimres[d]['lb'] and dimres[d]['grade'] == 'AGAINST' for d in DIMS):
        c.append('contradicted')
    if any(dimres[d]['lb'] and dimres[d]['grade'] == 'ASSUMED' for d in DIMS):
        c.append('assumed')
    return c


def wrap(text, indent, width=200, first=None):
    ind = ' ' * indent
    for i, ln in enumerate(textwrap.wrap(' '.join(text.split()), width - indent - 2, break_long_words=True,
                                         break_on_hyphens=False)):
        print((first if (i == 0 and first is not None) else ind + ('  ' if i else '')) + ln)


def evaluate(app, capres, ledger, cache, claims, verified, override=None, dimres=None):
    need = [(k, cap_grade(k, capres, override)) for k in app['needs']]
    if dimres is None:
        dimres = {d: check_cell(d, app['dims'][d], ledger, cache, claims, verified) for d in DIMS}
    g = app_grade(need, dimres, 'P')
    return {'need': need, 'dims': dimres, 'grade': g, 'letter': app_grade(need, dimres, 'LETTER'),
            'topdown': app_grade(need, dimres, 'TOPDOWN'), 'a3ns': app_grade(need, dimres, 'A3NS'),
            'lb_against': app_grade(need, dimres, 'P', lb='AGAINST'), 'lb_none': app_grade(need, dimres, 'P', lb='NONE'),
            'classes': classes(need, dimres), 'why': reasons(need, dimres, capres)}


def grade_tag(ev):
    return ev['grade'] + (' [%s]' % '; '.join(ev['classes']) if ev['grade'] == 'CONDITIONAL' and ev['classes'] else '')


def incumbent_check(app, claims, verified):
    ids = re.findall(r'm\d:\d+', app['incumbents'])
    bad = [i for i in ids if i not in claims or i not in verified]
    return ids, bad


def prior_of_needs(app, capres):
    out = []
    for k in app['needs']:
        r = capres['caps'].get(k) or capres['readings'].get(k)
        for x in r['prior']:
            t = re.sub(r'\*\*|^#+\s*|^-\s*', '', x['text']).split(' | ')[0]
            out.append('%s: %s' % (k, ' '.join(t.split())[:110]))
    return out


def prior_flag(app, capres):
    return any(re.search(r'\bKNOWN\b|\bREDUNDANT\b|[Nn]ot new|known fix', p) for p in prior_of_needs(app, capres))


def print_app(app, ev, claims, capres, verified):
    print('-' * 118)
    print('%s  %s' % (app['id'], app['name']))
    print('  needs: %s' % ', '.join('%s %s' % (k, g) for k, g in ev['need']))
    for d in DIMS:
        r, cell = ev['dims'][d], app['dims'][d]
        tag = '%s%s' % (d, '*' if r['lb'] else '')
        print('  %-10s %-9s claim: %s' % (tag, r['grade'], cell['claim']))
        if cell['assumed']:
            wrap('assumed: ' + cell['assumed'], 24)
        for t, ln, note in r['lines']:
            wrap('[%s] %s' % (t, ln), 26, first=' ' * 24 + '- ')
            if note:
                wrap(note, 28, first=' ' * 28)
        if r['mkt']:
            wrap('market / prior art (verified claims): ' + '; '.join(
                '%s %s' % (cid, claims[cid]['source'][:60]) for cid in r['mkt']), 24)
        for e in r['errors']:
            print('                        ERROR: %s' % e)
    ids, bad = incumbent_check(app, claims, verified)
    wrap('who already provides what the record measured (agent\'s reading; verified claims): ' + app['incumbents'], 4,
         first='  ')
    for b in bad:
        print('    ERROR: incumbent claim id %s absent or not verified' % b)
    pr = prior_of_needs(app, capres)
    if pr:
        wrap('prior art of the needed capabilities (capabilities.txt; never changes a grade): ' + '; '.join(pr), 4, first='  ')
    print('  APPLICATION GRADE: %s' % grade_tag(ev))
    wrap('because: ' + ('; '.join(ev['why']) or 'every needed capability at least CONSTRUCTION; no load-bearing dimension '
                                                 'ASSUMED or AGAINST'), 4, first='    ')
    if app['id'] == 'AP7':
        k2 = [('K2', cap_grade('K2', capres))]
        g = app_grade(k2, ev['dims'], 'P')
        print('    on K2 alone (A5 off): %s' % (g + (' [%s]' % '; '.join(classes(k2, ev['dims'])) if g == 'CONDITIONAL' else '')))
    if 'pending' in [g for _, g in ev['need']]:
        print('  note: a needed reading is pending; the grade can still fall to NOT SUPPORTED if it closes')
    return len(bad)


def market_block(app_id, claims, verified):
    rows = [c for c in claims.values() if c['application'] == app_id]
    by = {}
    for c in sorted(rows, key=lambda c: (c['id'].split(':')[0], int(c['id'].split(':')[1]))):
        by.setdefault(c['role'], []).append(c['id'] + ('' if c['id'] in verified else '(UNVERIFIED)'))
    return '; '.join('%s: %s' % (r, ', '.join(by[r])) for r in ('who_does_it', 'what_is_hard', 'our_method_relevance',
                                                              'regulation', 'risk') if r in by)


def forecasts(evs, capres, ledger, override=None):
    g = {a: evs[a]['grade'] for a in evs}
    k1 = cap_grade('K1', capres, override)
    sec51 = CAP.status_of(ledger['rows']['SEC5-1']['verdict']) if 'SEC5-1' in ledger['rows'] else 'absent'
    sup = [a['id'] for a in APPS if g[a['id']] == 'SUPPORTED']
    f1b = CAP.RUNG.get(k1, -1) <= CAP.RUNG['RESULT'] and sec51 == 'FAIL'
    f1 = not sup and f1b
    f2set = ['AP2', 'AP3', 'AP4', 'AP7', 'AP8']
    f2 = all(g[a] == 'CONSTRUCTION-BACKED' for a in f2set)
    rob = cap_grade('ROB1', capres, override)
    f3 = g['AP1'] == 'CONDITIONAL' and g['AP5'] == 'NOT SUPPORTED' and rob == 'pending'
    cb = evs[COMBO['id']]
    f4 = cb['grade'] == 'CONDITIONAL' and cb['dims']['Energy']['grade'] == 'MODELLED'
    return {'f': (f1, f2, f3, f4), 'k1': k1, 'sec51': sec51, 'sup': sup, 'f1b': f1b, 'f2set': f2set, 'rob': rob, 'cb': cb}


def main():
    capres = CAP.compute()
    ledger = capres['ledger']
    cache = capres['files']
    claims, verified, vsha = load_claims()
    print('APP1 stage B: the applications AP1-AP10, graded on the five dimensions (%s)' % CAP.DECL)
    print('A note, not evidence (R8); "marketable" means "someone could use it, and here is what they would have to believe"; it is')
    print('never a claim of novelty. Every source line below is copied from the pinned output or ledger row named with it.')
    print('Evidence grades are computed from the lines each cell cites (R15): AGAINST if a line shows the opposite (its verdict')
    print('checked), else MEASURED if a pinned measurement carries the claim, else MODELLED if a pinned model does, else ASSUMED')
    print('(the cell states what is assumed). Lines marked [limit] are caveats and establish nothing.')
    print('* marks a load-bearing dimension. Energy numbers come only from Compute_Savings/ and Energy Design Principle/.')
    print('Application grade (the declaration): SUPPORTED / CONSTRUCTION-BACKED / CONDITIONAL / NOT SUPPORTED, read with:')
    print('  A1 order NOT SUPPORTED > CONDITIONAL > SUPPORTED > CONSTRUCTION-BACKED (the only order in which every clause can fire)')
    print('  A2 a needed capability at MODEL -> CONDITIONAL (the rule has no clause for it)')
    print('  A3 a load-bearing dimension AGAINST -> CONDITIONAL (at least as bad as ASSUMED); every CONDITIONAL carries its reason')
    print("     classes; the stricter reading A3' (-> NOT SUPPORTED) is printed as a sensitivity")
    print("  A4 a pending reading (ROB1) is neither CLOSED nor a rung; A5 AP7 reads K2 through EPS2's federated-client row")
    print('  A6 the capability sensitivities printed by capabilities.py are carried through every application and forecast')
    print('capability grades imported from Applied_Suite/checks/capabilities.py (ledger sha256 %s):' % ledger['sha256'])
    scen = []
    for b in CAP.MAP + CAP.READINGS:
        r = capres['caps'].get(b['id']) or capres['readings'][b['id']]
        sens = '; '.join('sensitivity: %s under %s' % (s['grade'], s['item']) for s in r['sens'])
        print('  %-11s %-13s %s%s' % (b['id'], r['grade'], b['name'], ('  [' + sens + ']') if sens else ''))
        for s in r['sens']:
            scen.append((b['id'], s['grade'], s['item']))
    urls = {c['url'] for c in claims.values()}
    raws = {c['raw_file'] for c in claims.values()}
    print('claims: %d in claims_m1..m3 (distinct source URLs %d; distinct raw files %d); verified (every quote PASS in %s, '
          'sha256 %s): %d' % (len(claims), len(urls), len(raws), VERIFY, vsha, len(verified)))
    print()

    evs = {}
    nerr = 0
    nflag = 0
    for app in APPS + [COMBO]:
        ev = evaluate(app, capres, ledger, cache, claims, verified)
        evs[app['id']] = ev
        nerr += sum(len(ev['dims'][d]['errors']) for d in DIMS)
        nflag += sum(len(ev['dims'][d]['flags']) for d in DIMS)
    for app in APPS:
        nerr += print_app(app, evs[app['id']], claims, capres, verified)
        mb = market_block(app['id'], claims, verified)
        if mb:
            wrap('all market claims for %s by role: %s' % (app['id'], mb), 4, first='  ')
    print('-' * 118)
    print("FORECAST 4's COMBINATION (derived row)")
    nerr += print_app(COMBO, evs[COMBO['id']], claims, capres, verified)
    gen = market_block('general', claims, verified)
    print('-' * 118)
    wrap('general claims (the sweep-cost, regulation and risk evidence that bears on every application): ' + gen, 4, first='  ')

    print('=' * 118)
    print('SUMMARY (* = load-bearing; who = verified who_does_it claims for the application; prior = a needed capability has a')
    print('         REDUNDANT, KNOWN or not-new prior-art line in capabilities.txt)')
    print('  %-11s %-50s %-10s %-10s %-10s %-10s %-10s %-4s %-5s %s' % ('app', 'needs', 'UX', 'Energy', 'Security', 'Privacy',
                                                                       'Compute', 'who', 'prior', 'GRADE'))
    for app in APPS + [COMBO]:
        ev = evs[app['id']]
        needs = ', '.join('%s %s' % (k, g) for k, g in ev['need'])
        cells = ['%s%s' % (ev['dims'][d]['grade'], '*' if ev['dims'][d]['lb'] else '') for d in DIMS]
        who = sum(1 for c in claims.values() if c['application'] == app['id'] and c['role'] == 'who_does_it' and c['id'] in verified)
        print('  %-11s %-50s %-10s %-10s %-10s %-10s %-10s %-4s %-5s %s' % (
            app['id'], needs[:50], *cells, who if app is not COMBO else '-', 'yes' if prior_flag(app, capres) else '-',
            grade_tag(ev)))
    counts = {}
    for app in APPS:
        counts[evs[app['id']]['grade']] = counts.get(evs[app['id']]['grade'], 0) + 1
    print('  AP1-AP10 by grade: %s' % ', '.join('%s %d' % (g, counts.get(g, 0)) for g in GRADES + ('pending', 'NO RULE')
                                                if counts.get(g, 0) or g in GRADES))
    cc = {}
    for app in APPS:
        if evs[app['id']]['grade'] == 'CONDITIONAL':
            for c in evs[app['id']]['classes']:
                cc.setdefault(c, []).append(app['id'])
    print('  CONDITIONAL by reason class (an application can carry several): %s' % (
        '; '.join('%s %d (%s)' % (c, len(v), ', '.join(v)) for c, v in cc.items()) or 'none'))
    dimc = {g: 0 for g in EVID}
    for app in APPS:
        for d in DIMS:
            dimc[evs[app['id']]['dims'][d]['grade']] += 1
    print('  the 50 dimension cells of AP1-AP10: %s' % ', '.join('%s %d' % (g, dimc[g]) for g in EVID))
    lbc = {g: 0 for g in EVID}
    for app in APPS:
        for d in DIMS:
            if evs[app['id']]['dims'][d]['lb']:
                lbc[evs[app['id']]['dims'][d]['grade']] += 1
    print('  of them load-bearing: %s' % ', '.join('%s %d' % (g, lbc[g]) for g in EVID))
    print('  measured or modelled lines that also carry an opposing word (flags): %d' % nflag)
    print('  table errors: %d' % nerr)

    # ---------------- sensitivities
    print()
    print('SENSITIVITY (the grade under the readings the declaration leaves open, the load-bearing flags, and the capability')
    print('readings capabilities.py prints; SUP SUPPORTED, CB CONSTRUCTION-BACKED, COND CONDITIONAL, NS NOT SUPPORTED)')
    sc_evs = []
    for kid, sg, item in scen:
        ov = {kid: sg}
        sc_evs.append(('%s=%s' % (kid, sg), '%s read as %s, because %s fails (capabilities.txt)' % (kid, sg, item), ov,
                       {a['id']: evaluate(a, capres, ledger, cache, claims, verified, ov, evs[a['id']]['dims'])
                        for a in APPS + [COMBO]}))
    if len(scen) > 1 and len({sg for _, sg, _ in scen}) == 1:
        ov = {kid: sg for kid, sg, _ in scen}
        sc_evs.append(('%s=%s' % ('+'.join(k for k, _, _ in scen), scen[0][1]), 'the readings above together', ov,
                       {a['id']: evaluate(a, capres, ledger, cache, claims, verified, ov, evs[a['id']]['dims'])
                        for a in APPS + [COMBO]}))
    heads = ['primary', 'letter', 'top-down', "A3'", 'LB-AGAINST', 'LB-NONE'] + [n for n, _, _, _ in sc_evs]
    print('  columns: primary (A1-A6); letter (A2, A3 off); top-down (A1 off); A3\' (a load-bearing AGAINST -> NOT SUPPORTED);')
    print('  LB-AGAINST (every AGAINST cell load-bearing); LB-NONE (no cell load-bearing); then each capability reading:')
    for n, desc, _, _ in sc_evs:
        print('    %s: %s' % (n, desc))
    print('  %-11s ' % 'app' + ' '.join('%-11s' % h for h in heads))
    moved = {h: [] for h in heads[1:]}
    for app in APPS + [COMBO]:
        ev = evs[app['id']]
        vals = [ev['grade'], ev['letter'], ev['topdown'], ev['a3ns'], ev['lb_against'], ev['lb_none']] + \
               [s[app['id']]['grade'] for _, _, _, s in sc_evs]
        for h, v in zip(heads[1:], vals[1:]):
            if v != vals[0]:
                moved[h].append(app['id'])
        print('  %-11s ' % app['id'] + ' '.join('%-11s' % ABBR.get(v, v) for v in vals))
    for h in heads[1:]:
        print('  moves under %-24s %d: %s' % (h + ':', len(moved[h]), ', '.join(moved[h]) or '-'))

    # ---------------- forecasts
    print()
    print('FORECASTS (the declaration, written before any source or script), scored')
    fc = forecasts(evs, capres, ledger)
    g = {a: evs[a]['grade'] for a in evs}
    f1, f2, f3, f4 = fc['f']
    print('  1. No application is SUPPORTED; K1 is at most RESULT (SEC4-1) with a failed replication, unless SEC6-1 changes that.')
    print('     applications SUPPORTED: %s (%s); K1 %s, SEC5-1 %s, SEC6-1 %s (%s) -> %s' % (
        len(fc['sup']), ', '.join(fc['sup']) or 'none', fc['k1'], fc['sec51'], 'present' if 'SEC6-1' in ledger['rows'] else 'pending',
        'holds' if fc['f1b'] else 'fails', 'HOLDS' if f1 else 'FAILS'))
    f2hits = [a for a in fc['f2set'] if g[a] == 'CONSTRUCTION-BACKED']
    print('  2. AP2, AP3, AP4, AP7 and AP8 are CONSTRUCTION-BACKED.')
    print('     %s; CONSTRUCTION-BACKED %d of %d -> %s' % (', '.join('%s %s' % (a, g[a]) for a in fc['f2set']), len(f2hits),
                                                            len(fc['f2set']), 'HOLDS' if f2 else 'FAILS'))
    for rd, key in (('letter', 'letter'), ('top-down', 'topdown')):
        hits = [a for a in fc['f2set'] if evs[a][key] == 'CONSTRUCTION-BACKED']
        print('     sensitivity, %s reading: CONSTRUCTION-BACKED %d of %d (%s)' % (rd, len(hits), len(fc['f2set']), ', '.join(hits) or 'none'))
    print('  3. AP1 is CONDITIONAL. AP5 is NOT SUPPORTED (K4\'s gates closed). AP6 waits on ROB1.')
    print('     AP1 %s (%s); AP5 %s, K4 %s (%s); ROB1 %s, AP6 %s (%s) -> %s' % (
        g['AP1'], 'holds' if g['AP1'] == 'CONDITIONAL' else 'fails', g['AP5'], cap_grade('K4', capres),
        'holds' if g['AP5'] == 'NOT SUPPORTED' else 'fails', fc['rob'], g['AP6'], 'holds' if fc['rob'] == 'pending' else 'fails',
        'HOLDS' if f3 else 'FAILS'))
    cb = fc['cb']
    print('  4. The strongest honest case is AP2 + AP9 with K1; it is still CONDITIONAL, and its energy claim is MODELLED (the')
    print('     Compute_Savings estimates), not MEASURED at scale.')
    print('     AP2+AP9+K1 %s (%s); its Energy cell %s, computed from the lines it cites (%s) -> %s' % (
        cb['grade'], 'holds' if cb['grade'] == 'CONDITIONAL' else 'fails', cb['dims']['Energy']['grade'],
        'holds' if cb['dims']['Energy']['grade'] == 'MODELLED' else 'fails', 'HOLDS' if f4 else 'FAILS'))
    above = [a['id'] for a in APPS if g[a['id']] in GRADES and GRADES.index(g[a['id']]) < GRADES.index('CONDITIONAL')]
    print("     'the strongest honest case' is a judgement and is not scored; beside it, the applications graded above")
    print('     CONDITIONAL on the declaration\'s scale: %s' % (', '.join('%s %s' % (a, g[a]) for a in above) or 'none'))
    print('  forecasts: 1 %s, 2 %s, 3 %s, 4 %s' % tuple('HOLDS' if f else 'FAILS' for f in (f1, f2, f3, f4)))
    for n, _, ov, sev in sc_evs:
        sf = forecasts(sev, capres, ledger, ov)
        print('  sensitivity %s: forecasts 1 %s, 2 %s, 3 %s, 4 %s' % ((n,) + tuple('HOLDS' if f else 'FAILS' for f in sf['f'])))

    print()
    print('files read (sha256):')
    for rel in sorted(cache):
        d = cache[rel]
        print('  %s  %s' % (d['sha256'] if d else 'ABSENT' + ' ' * 58, rel))
    nerr += sum(len(r['errors']) for r in list(capres['caps'].values()) + list(capres['readings'].values()))
    print('errors (table, incumbents and capability MAP): %d' % nerr)
    return 0 if nerr == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
