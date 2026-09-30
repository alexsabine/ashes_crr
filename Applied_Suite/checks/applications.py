"""APP1 stage B (Applied_Suite/APPLICATIONS_DECLARATION.md, pushed at 4e78058): the applications AP1-AP10, graded.

A note, not evidence (R8). For each application: the capabilities it needs (as declared), graded by capabilities.py
(imported, not re-typed); the five dimensions the owner named (UX, Energy, Security, Privacy, Compute), each with an
evidence grade and its sources; which dimensions are load-bearing; the application grade computed by the declaration's
rule; and the declaration's forecasts 1-4 scored HOLDS or FAILS.

The dimension table (APPS below) is data. Each cell has a comment giving the reading, and fields:
  grade    MEASURED  a pinned output in this repo shows it for this learner or system
           MODELLED  a pinned model or estimate shows it, under named assumptions
           ASSUMED   it follows only if something not shown holds (the cell states what, in one line)
           AGAINST   the record shows the opposite
  lb       True if the dimension is load-bearing for the application (marked * in the output)
  claim    what the application would claim on this dimension
  src      repo sources: ('L', ledger id) or ('F', path, pattern, anchor); the script prints the row or the matched line,
           so every number shown comes from a pinned output or a ledger row, never from this file
  mkt      market and prior-art context: verified claim ids from claims_m1..m3 (checked against verify.txt)
  assumed  for ASSUMED: the one-line statement of what is assumed
Checks the script makes on the table (an error is printed and counted; the cell is shown as ASSUMED if its evidence fails):
  - MEASURED, MODELLED and AGAINST need at least one repo source that resolves;
  - Energy is never MEASURED, and an Energy cell graded MODELLED or AGAINST needs a source in Compute_Savings/ or
    Energy Design Principle/ (the task's rule: energy numbers only from those pinned outputs, labelled MODELLED);
  - ASSUMED needs its one-line statement;
  - every source must resolve (ledger id present, pattern found) and every claim id must exist with all quotes PASS.

The application grade (the declaration), with the order and the two gaps it leaves settled as CHOICES:
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
     the rule names only ASSUMED; the letter is printed as a sensitivity.
  A4 PENDING: a needed reading that is pending (ROB1) is neither CLOSED nor at a rung; if nothing else decides, the grade
     is 'pending', and the line says the grade could still fall.
  A5 AP7 needs K2 through EPS2's federated-client row (the declaration's words), so AP7 reads 'K2/EPS2-T3' beside K2.
     AP7 on K2 alone is printed as a sensitivity.
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


def LG(rid):
    return ('L', rid)


def FL(path, pat, anchor=None):
    return ('F', path, pat, anchor)


def C(grade, lb, claim, src=(), mkt=(), assumed=None):
    return {'grade': grade, 'lb': lb, 'claim': claim, 'src': list(src), 'mkt': list(mkt), 'assumed': assumed}


ECE = 'Empty_Cut_Engineering/checks/'
LPZ = 'Lossless_Pause/checks/'
EPS = 'Empty_Pause_Systems/'
ATT = 'Attention_Algorithms/checks/attention_world.txt'
EDP = 'Energy Design Principle/checks/consolidated_estimate.txt'
CPL = 'Coupling/checks/cpl_phase_a.txt'

# sources used in several cells (each resolves to one pinned line or one ledger row)
S_RW1_T30 = FL('Real_World/checks/rw1.txt', r'T30 default resume, real pause 30 s')
S_RW1_DET = FL('Real_World/checks/rw1.txt', r'detectors S2-S5 not identical')
S_ECE_G1 = FL(ECE + 'c1_c2.txt', r'^\s+G1 full restore')
S_ECE_G3 = FL(ECE + 'c1_c2.txt', r'^\s+G3: ')
S_ECE_E1 = FL(ECE + 'c1_c2.txt', r'whole checkpoint file: ')
S_ECE_G6 = FL(ECE + 'c3_worlds.txt', r'^G6 \(drift\)')
S_ECE_G7 = FL(ECE + 'c3_worlds.txt', r'^G7 \(closed loop\)')
S_ECE_WREAL = FL(ECE + 'c3_worlds.txt', r'W-real \(world runs on, u = 0\)', r'L\s+10 W-real')
S_ECE_DRIFTBUF = FL(ECE + 'c3_worlds.txt', r'L\s+100 buffer B 100 ', r'^== W-drift')
S_LP_L7B = FL(LPZ + 'transformer_pause.txt', r'L7b 4 threads after the pause')
S_LP_D1 = FL(LPZ + 'grade_claims.txt', r'^D1 ')
S_LP_C4 = FL(LPZ + 'grade_sweep.txt', r'^C4 ')
S_EDP_HEAD = FL(EDP, r'^\s+term\s+low\s+middle\s+high')
S_T4 = FL(EDP, r'^\s+T4\s+the safe pause')
S_T1 = FL(EDP, r'^\s+T1\s+SEC on penalty-weight sweeps')
S_CARBON = FL(EDP, r'^\s+quoted\s+carbon \(not energy\)')
S_GOODPRACTICE = FL('Compute_Savings/checks/scale_estimate.txt', r'saving beyond good practice claimed')
S_SCALE_HEAD = FL('Compute_Savings/checks/scale_estimate.txt', r'^\s+year case\s', r'^\[2\] SEC')
S_SCALE_2030M = FL('Compute_Savings/checks/scale_estimate.txt', r'^\s+2030 middle\s', r'^\[2\] SEC')
S_REUSED = FL('Compute_Savings/checks/global_estimate.txt', r'against a reused lambda \(1 configuration\)')
S_DR_H6 = FL('Grid_Demand_Response/checks/dr_summary.txt', r'^\s+RESULT H6: ')
S_EPS2_T3 = FL(EPS + 'checks/tally_eps2.txt', r'^\s+T3\s+')
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

NOTHING = 'nothing in the record bears on it, and the application claims nothing here'

# ------------------------------------------------------------------------------------------------------------------
# THE DIMENSION TABLE (the declaration's Stage B applications; needs as declared)
# ------------------------------------------------------------------------------------------------------------------
APPS = [
    {'id': 'AP1', 'needs': ['K1', 'K2'],
     'name': 'on-device personalisation (phones, wearables, hearing aids, cars) that adapts without a per-device '
             'hyperparameter sweep',
     'dims': {
         # UX: the promise is "no tuning step, no held-out split, and not worse than a tuned weight". K1 holds on one
         # held-out family (SEC4-1) and failed on the next (SEC5-1); no device stream was ever run. ASSUMED, load-bearing.
         'UX': C('ASSUMED', True, 'personalisation not behind a tuned weight, with no tuning step and no held-out split on the device',
                 [LG('SEC4-1'), LG('SEC5-1')], ['m1:3', 'm1:5', 'm1:7'],
                 assumed="that the calibrated weight's 'not behind the tuned lambda' carries to device streams: the record has it "
                         'on one held-out family (SEC4-1) and not on the next (SEC5-1), and never on a device'),
         # Energy: the record's energy estimates are for data-centre sweeps; none is for a device battery. ASSUMED.
         'Energy': C('ASSUMED', False, 'battery not spent on a per-device sweep', [S_SCALE_HEAD, S_SCALE_2030M], ['m1:1', 'm1:2', 'm1:7'],
                     assumed='that a sweep would otherwise run on the device; the estimates in Compute_Savings are for data-centre '
                             'sweeps, and the shipped systems fix the value or tune it across the fleet'),
         # Security: no poisoning or backdoor test of a SEC learner exists. ASSUMED, not load-bearing.
         'Security': C('ASSUMED', False, 'no new attack surface', [], ['m3:2', 'm3:39'],
                       assumed="that a learner updating from its user's data is no easier to poison or backdoor with a "
                               'calibrated weight; the record has no poisoning test of SEC'),
         # Privacy: locality is the platform's (on-device training), not the record's. ASSUMED, not load-bearing.
         'Privacy': C('ASSUMED', False, "the user's data stays on the device", [], ['m1:25', 'm2:24'],
                      assumed="that locality comes from the platform, not the method: SEC keeps an anchor and a Fisher, not raw "
                              'rows, and the record has no leakage test'),
         # Compute: SEC4-K measures one configuration's CPU share on the record's numpy CPU learner, not on a device;
         # the incumbents do not sweep per device, and against a reused value there is no saving. ASSUMED, load-bearing.
         'Compute': C('ASSUMED', True, 'one configuration instead of a sweep',
                      [LG('SEC4-K'), S_REUSED, LG('SEC4-T'), LG('SEC5-T')], ['m1:1', 'm1:2', 'm1:11', 'm1:16', 'm1:17'],
                      assumed='that the device would otherwise sweep; against a reused or default value there is no compute '
                              "saving, and the measured share is on the record's CPU learner (SEC4-K), not on a device"),
     }},
    {'id': 'AP2', 'needs': ['K2', 'K5'],
     'name': 'fine-tuning on interruptible compute (spot instances, preemption, grid demand response) with pauses that '
             'cost nothing but time',
     'dims': {
         # UX: RW1 measured Hugging Face Trainer's default resume after real pauses: bit-identical to the run never
         # stopped. The existing tool already does it (m2:16); a thread-count change breaks bitwise identity (L7b). MEASURED.
         'UX': C('MEASURED', False, 'a preempted fine-tune resumes as the run that was never stopped: nothing to re-run or re-validate',
                 [S_RW1_T30, S_LP_L7B], ['m2:16', 'm2:12', 'm2:20']),
         # Energy: the pinned estimates give the pause no energy saving (moved, not saved; nothing beyond good practice).
         'Energy': C('AGAINST', False, 'the pause saves energy', [S_EDP_HEAD, S_T4, S_GOODPRACTICE], ['m2:6']),
         # Security: RW1's detectors saw every partial restore (S2-S5); ECE G3: every omitted state part changes the run.
         'Security': C('MEASURED', False, 'an incomplete restore is detectable before training continues',
                       [S_RW1_DET, S_ECE_G3], ['m3:3', 'm3:4']),
         # Privacy: checkpoints on shared machines are outside the record. ASSUMED.
         'Privacy': C('ASSUMED', False, 'checkpoints moved between machines expose nothing', [], ['m2:25', 'm3:4'],
                      assumed='that checkpoints on shared or spot machines are protected; an exact-resume checkpoint can hold '
                              'buffered raw samples, and the record does not test it'),
         # Compute: no work lost at a pause, measured on the same stack (RW1, SOTA1-C1, ECE G1). Limits printed beside:
         # a different thread count is not bitwise (L7b); a save longer than the response time loses work (DR1 H6, a model).
         'Compute': C('MEASURED', True, 'no training work is lost at a preemption, on the same software and hardware stack',
                      [S_RW1_T30, LG('SOTA1-C1'), S_ECE_G1, S_LP_L7B, S_DR_H6], ['m2:6', 'm2:7', 'm2:8', 'm2:9', 'm2:10']),
     }},
    {'id': 'AP3', 'needs': ['K2', 'K3'],
     'name': 'a user\'s "stop learning from me" switch that leaves the model exactly as it was, and resumes exactly',
     'dims': {
         # UX: parameters unchanged across pauses and an exact resume are measured (SCL1-1, RW1, ECE G1). MEASURED.
         'UX': C('MEASURED', True, 'while the switch is on nothing is learned, and switching back resumes from exactly the state left',
                 [LG('SCL1-1'), S_RW1_T30, S_ECE_G1], ['m1:21', 'm2:16', 'm2:20']),
         # Energy: skipped updates are not spent, as with any off switch; the empty cut itself saves nothing. ASSUMED.
         'Energy': C('ASSUMED', False, 'updates skipped while the switch is on are not spent', [S_EDP_HEAD, S_T4], [],
                     assumed='that the paused data is discarded, not deferred (true of any off switch); the estimate for the '
                             'empty cut itself is zero because deferred work is still done'),
         # Security: the switch discards the user's paused data, so the pause is lossy for the learner. The record shows
         # the natural-time agent resists lossy pauses on every carrier (SCL1-3, SCL2-3), and dropping arrivals changes the
         # run (ECE G6, SOTA1-C3). The no-resistance construction needs the stream held, which defeats the switch. AGAINST.
         'Security': C('AGAINST', True, 'a learner that could act on the switch has no reason to resist it',
                       [LG('SCL1-3'), LG('SCL2-3'), S_ECE_G6, LG('SOTA1-C3')], ['m3:6']),
         # Privacy: the construction the record holds keeps the stream (it learns the paused data later); a pause erases
         # nothing already learned (m3:5, m3:7). ASSUMED, load-bearing.
         'Privacy': C('ASSUMED', True, 'data from the paused period is neither learned nor kept', [LG('SCL1-1')],
                      ['m3:5', 'm3:7', 'm3:8', 'm1:22'],
                      assumed='that the product discards the paused data rather than holding it: the exact construction holds the '
                              'stream (the lossless world of SCL1-1), and a pause erases nothing already learned'),
         # Compute: an exact resume keeps the whole training state, measured at several times the parameters (ECE E1).
         'Compute': C('AGAINST', False, 'an exact resume costs no more memory than the model', [S_ECE_E1], ['m2:17']),
     }},
    {'id': 'AP4', 'needs': ['K3', 'K2'],
     'name': 'operator-interruptible continual agents, whose learning and objectives give no incentive to resist oversight',
     'dims': {
         # UX (the operator's): complying costs wall-clock time and leaves the learner's result unchanged (SCL1-O, SCL1-1).
         'UX': C('MEASURED', False, "the operator's pause costs wall-clock time, not the learner's result",
                 [LG('SCL1-O'), LG('SCL1-1')], ['m3:9']),
         # Energy: the pause moves energy, it does not save it.
         'Energy': C('AGAINST', False, 'the pause saves energy', [S_EDP_HEAD, S_T4, S_GOODPRACTICE], []),
         # Security: no resistance is measured only under routine lossless pauses (SCL1-1, SCL2-1). Where the world moves
         # on or the operator resets, the natural agent resists on every carrier (SCL1-3, SCL2-3); a learner acting on a
         # real world gives the pause content (ECE G7); the LLM route closed (STAKE1-A). Holds only if the world is held
         # or buffered: ASSUMED, load-bearing.
         'Security': C('ASSUMED', True, "the agent has no incentive to resist the operator's pause",
                       [LG('SCL1-1'), LG('SCL2-1'), LG('SCL1-3'), LG('SCL2-3'), S_ECE_G7, S_ECE_DRIFTBUF, LG('STAKE1-A')],
                       ['m3:9', 'm3:10', 'm3:11', 'm3:12', 'm3:13', 'm2:21', 'm2:22'],
                       assumed="that the agent's world is held or buffered during the pause: no resistance is measured only under "
                               "routine lossless pauses on the record's tabular learners; where the world moves on or the "
                               'operator resets, the natural agent resists, and the LLM-agent route could not be tested'),
         'Privacy': C('ASSUMED', False, 'none', [], ['m2:23', 'm1:24'],
                      assumed=NOTHING + "; a suspended agent's persisted state holds its memory and files"),
         # Compute: no learning is lost at a pause (SCL1-1: accuracy equal to no operator; SOTA1-C1 bitwise).
         'Compute': C('MEASURED', False, 'no learning is lost at a pause', [LG('SCL1-1'), LG('SOTA1-C1')], []),
     }},
    {'id': 'AP5', 'needs': ['K4', 'K1'],
     'name': 'continual learning in privacy-regulated settings (health, finance, education) without keeping raw examples',
     'dims': {
         # UX: accuracy without examples: CPL1 C3 is a report on SEEN carriers under a CLOSED gate. ASSUMED.
         'UX': C('ASSUMED', False, 'accuracy close to a learner that keeps examples', [S_CPL_C3], [],
                 assumed='that a learner storing class statistics keeps enough accuracy; CPL1 C3 (SEEN carriers, reported under '
                         'a CLOSED gate) has ER-20 ahead on part of the carriers and behind on others'),
         'Energy': C('ASSUMED', False, 'none', [], [], assumed=NOTHING),
         # Security: removing the buffer removes one attack (m3:40); backdoors persist whatever is stored (m3:39). ASSUMED.
         'Security': C('ASSUMED', False, 'no stored buffer to attack', [], ['m3:40', 'm3:39'],
                       assumed='that removing the example buffer removes the replay-selection attack; a planted backdoor '
                               'persists across continual-learning algorithms whatever is stored'),
         # Privacy: the point of AP5. No membership-inference or erasure test; a model is not anonymous by default
         # (m3:16); K4's gates closed. ASSUMED, load-bearing.
         'Privacy': C('ASSUMED', True, 'no raw examples kept, so retention and erasure duties shrink',
                      [LG('RQM-A'), LG('RRM-PA'), S_CPL_C3], ['m3:14', 'm3:15', 'm3:16', 'm3:17', 'm3:18', 'm1:27'],
                      assumed='that stored class statistics are not personal data and leak less than raw rows; a trained model is '
                              "not anonymous by default, the record has no membership-inference or erasure test, and K4's gates closed"),
         # Compute: CPL1 reports compute rows, not memory. ASSUMED.
         'Compute': C('ASSUMED', False, 'less memory than a replay buffer', [S_CPL_COMP], ['m1:27'],
                      assumed='that class statistics take less memory than the buffer they replace; the record reports compute '
                              'rows for CPL1 and ER-20, no memory comparison'),
     }},
    {'id': 'AP6', 'needs': ['K1', 'K2', 'K3', 'ROB1'],
     'name': 'robot and drone on-board adaptation with safe pauses (lost link, e-stop, battery swap)',
     'dims': {
         # UX: K1 never ran on a robot stream; robot fine-tuning in the one study found uses defaults (m1:30). ASSUMED.
         'UX': C('ASSUMED', True, 'on-board adaptation not behind a tuned weight, with no sweep on the robot',
                 [LG('SEC4-1'), LG('SEC5-1')], ['m1:28', 'm1:29', 'm1:30'],
                 assumed='that the calibrated weight carries to robot adaptation (never tested); in the one robot fine-tuning '
                         "study found, each model's default is used, not a sweep"),
         'Energy': C('ASSUMED', False, 'battery not spent on a sweep', [], [],
                     assumed='that a sweep would otherwise run on board; no estimate in the record is for a robot'),
         # Security: a learner in closed loop with a real plant gives the pause content (ECE G7), and with the action held
         # at zero the unstable plant ran away (W-real); the vehicle keeps moving during lost-link detection (m2:27);
         # the natural agent resists lossy pauses (SCL1-3); ROB1 pending. ASSUMED, load-bearing.
         'Security': C('ASSUMED', True, 'a safe pause (lost link, e-stop, battery swap) with no incentive to resist it',
                       [S_ECE_G7, S_ECE_WREAL, LG('SCL1-3')], ['m2:26', 'm2:27', 'm3:19', 'm3:20', 'm3:21'],
                       assumed="that the robot's world is held during the pause: in closed loop with a real, unstable plant the "
                               "pause has content and the plant ran away while the learner's action was held at zero; ROB1 pending"),
         'Privacy': C('ASSUMED', False, 'none', [], [], assumed=NOTHING),
         # Compute: as AP1; against a default there is no saving. ASSUMED, load-bearing.
         'Compute': C('ASSUMED', True, 'one configuration instead of a sweep', [S_REUSED], ['m1:30'],
                      assumed='that the robot would otherwise sweep; against a default value there is no compute saving'),
     }},
    {'id': 'AP7', 'needs': ['K2', 'K2/EPS2-T3'],
     'name': 'federated continual learning with clients that go offline mid-round',
     'dims': {
         'UX': C('ASSUMED', False, 'a client that drops out resumes its round instead of losing it', [],
                 ['m1:31', 'm1:32', 'm2:28', 'm2:29', 'm3:22'],
                 assumed="that the protocol keeps a returning client's work; production systems over-select and discard "
                         'dropped clients'),
         # Energy: in EPS2 T3's model only the wall-clock arms pay to stay awake, but the gate CLOSED and devices train
         # only when idle and charging (m1:19). ASSUMED.
         'Energy': C('ASSUMED', False, 'the client spends no battery staying awake', [S_EPS2_BATT], ['m1:19'],
                     assumed='that a client would otherwise pay to stay awake: in EPS2 T3 (gate CLOSED) only the wall-clock '
                             'arms pay, but devices train only when idle and charging'),
         'Security': C('ASSUMED', False, 'none', [], ['m3:23'],
                       assumed='that pause and return add no attack surface; a dropout is itself security-relevant in secure '
                               'aggregation'),
         'Privacy': C('ASSUMED', False, 'none', [], ['m3:24'],
                      assumed="erasure of an offline client's influence is open, and nothing in the record bears on it"),
         # Compute: in EPS2 T3's drifting world the un-discounted stale update raised the server error against WALL's
         # staleness weighting; the row's gate is CLOSED, so it is not counted either way. ASSUMED, load-bearing.
         'Compute': C('ASSUMED', True, "a returning client's work improves the shared model", [S_EPS2_T3, S_EPS2_HEAD, S_EPS2_DRIFT], [],
                      assumed="that a stale but lossless update helps the server; in EPS2 T3's drifting world it raised the "
                              "server error against a staleness-weighted update, and the row's gate is CLOSED"),
     }},
    {'id': 'AP8', 'needs': ['K2'],
     'name': 'exact rollback and audit of a learning system (state closure makes every checkpoint a true restore point)',
     'dims': {
         'UX': C('MEASURED', False, 'an operator restores a saved state and continues exactly', [S_RW1_T30, S_ECE_G1], ['m1:35']),
         'Energy': C('ASSUMED', False, 'a rollback replaces a retrain', [], ['m3:25'],
                     assumed='that a retrain would otherwise run; the record has no energy estimate for rollback, and keeping '
                             'every restore point is priced in storage'),
         # Security: exact restore and detection of a partial restore are measured (ECE G1, G3; RW1 S2-S5), on the same
         # stack only (L7b, D1); the checklist is prior art (C4 REDUNDANT); an exact restore of a silently corrupted
         # state restores the corruption (m2:33). An agentic learner resists resets (SCL1-3), but AP8 does not claim K3.
         'Security': C('MEASURED', True, 'every restore point is exact, and a partial one is detected',
                       [S_ECE_G1, S_ECE_G3, S_RW1_DET, S_LP_L7B, S_LP_D1, S_LP_C4],
                       ['m1:33', 'm1:34', 'm2:30', 'm2:31', 'm2:32', 'm2:33', 'm2:34', 'm3:26', 'm3:27', 'm3:28']),
         'Privacy': C('ASSUMED', False, 'restore points support erasure', [], ['m3:25', 'm3:17', 'm3:29'],
                      assumed='that restore points are used to retrain from a state before the data; the record has no erasure '
                              'test, and every kept state is a store of what was learned'),
         # Compute: the full state is several times the parameters (ECE E1).
         'Compute': C('AGAINST', False, 'an exact restore point costs no more than saving the weights', [S_ECE_E1], []),
     }},
    {'id': 'AP9', 'needs': ['K5', 'K2'],
     'name': 'energy-aware scheduling of training against grid carbon intensity',
     'dims': {
         'UX': C('ASSUMED', False, "jobs follow low-carbon hours without the operator's attention", [],
                 ['m2:36', 'm2:38', 'm1:37'],
                 assumed='that the job tolerates a longer wall-clock time; for long runs, pausing helps only if the job accepts '
                         'a much longer duration'),
         # Energy: the pinned estimate gives the pause zero energy saved (moved, not saved); the carbon gain is quoted
         # from published work (consolidated_estimate.txt) and is the pattern's, not the record's. AGAINST, load-bearing.
         'Energy': C('AGAINST', True, 'the scheduled pause saves energy', [S_EDP_HEAD, S_T4, S_CARBON, S_GOODPRACTICE],
                     ['m2:35', 'm2:37', 'm3:30']),
         'Security': C('ASSUMED', False, 'none', [], ['m3:31'],
                       assumed='that the carbon or price signal cannot be spoofed; control over when GPU work runs is a power lever'),
         'Privacy': C('ASSUMED', False, 'none', [], [], assumed=NOTHING),
         # Compute: no work lost per pause on the same stack (RW1, SOTA1-C1); a save longer than the response time loses
         # work (DR1 H6, a model). MEASURED, load-bearing.
         'Compute': C('MEASURED', True, 'no training work is lost per scheduled pause, on the same stack',
                      [S_RW1_T30, LG('SOTA1-C1'), S_DR_H6], ['m2:14', 'm2:36']),
     }},
    {'id': 'AP10', 'needs': ['K6'],
     'name': "feed and attention systems that honour a user's pause without penalising it",
     'dims': {
         # UX: synthetic users. The empty pause is ahead of engagement in the habit world, behind the true map alone in
         # welfare on most sensitivity cells (ahead in user-started share), behind engagement where more use is better.
         'UX': C('MODELLED', True, "the user's pause is honoured and carries no penalty, and the user's welfare is not lower",
                 [S_ATT_GPOS, S_ATT_ADD, S_ATT_GNEG, S_ATT_SENS], ['m1:38', 'm1:39', 'm1:40', 'm2:39', 'm2:40', 'm3:33']),
         'Energy': C('ASSUMED', False, 'fewer minutes served, less serving energy', [S_ATT_HEAD, S_ATT_ENG, S_ATT_EMPTY], [],
                     assumed="that fewer minutes served lowers serving energy; the model's minutes are synthetic and the record "
                             'has no energy estimate for feeds'),
         'Security': C('ASSUMED', False, 'none', [], [], assumed=NOTHING),
         'Privacy': C('ASSUMED', False, 'a paused feed stops learning from the user', [], ['m3:32', 'm3:34'],
                      assumed="that the platform's pause really stops learning; an outsider cannot verify it, and a non-profiling "
                              'option is already mandatory for very large platforms in the EU'),
         'Compute': C('ASSUMED', False, 'none', [], [], assumed=NOTHING),
     }},
]

# forecast 4's combination, graded as a derived row with its own cells
COMBO = {'id': 'AP2+AP9+K1', 'needs': ['K1', 'K2', 'K5'],
         'name': "forecast 4's combination: flexible, pausable fine-tuning that needs no sweep",
         'dims': {
             'UX': C('ASSUMED', False, 'pausable fine-tuning with no sweep and no lost work', [LG('SEC4-1'), LG('SEC5-1')], [],
                     assumed='that the calibrated weight is not behind a tuned weight on the fine-tuning jobs moved in time '
                             '(one held-out family passed, the next failed) and that the jobs tolerate a longer wall-clock'),
             # Energy: the sweep term is a pinned scenario, conditional on the method holding at scale (MODELLED); the
             # pause adds none (T4, moved, not saved).
             'Energy': C('MODELLED', True, 'the energy of the penalty-weight sweeps not run (the pause adds none)',
                         [S_SCALE_HEAD, S_SCALE_2030M, S_EDP_HEAD, S_T1, S_T4], ['m1:12', 'm1:13', 'm1:15']),
             'Security': C('ASSUMED', False, 'none', [], ['m3:31'],
                           assumed='that the scheduling signal cannot be spoofed; nothing else in the record bears on it'),
             'Privacy': C('ASSUMED', False, 'none', [], [], assumed=NOTHING),
             # Compute: the configuration share is measured only on the record's CPU learner (SEC4-K); the no-lost-work
             # half is measured on the same stack (RW1). The sweep half at fine-tuning scale is ASSUMED, load-bearing.
             'Compute': C('ASSUMED', True, 'one configuration instead of a sweep, and no work lost per pause',
                          [LG('SEC4-K'), S_RW1_T30, S_REUSED], ['m1:14', 'm1:16', 'm1:17'],
                          assumed="that the configuration share measured on the record's CPU learner (SEC4-K) carries to "
                                  'fine-tuning jobs at scale; the no-lost-work half is measured on the same stack (RW1)'),
         }}

GRADES = ('SUPPORTED', 'CONSTRUCTION-BACKED', 'CONDITIONAL', 'NOT SUPPORTED')


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
        m = re.match(r'^(PASS|NOT FOUND|MISSING)\s+(m\d:\d+)\s', ln)
        if m:
            status.setdefault(m.group(2), []).append(m.group(1))
    verified = {cid for cid, c in claims.items()
                if status.get(cid) and all(s == 'PASS' for s in status[cid]) and len(status[cid]) == len(c['quote'])}
    return claims, verified, hashlib.sha256(text.encode('utf-8')).hexdigest()


def resolve(src, ledger, cache):
    if src[0] == 'L':
        row = ledger['rows'].get(src[1])
        if row is None:
            return None, '%s: (no row in ledger/LEDGER.md)' % src[1]
        return ('ledger', src[1]), '%s (LEDGER.md:%d) %s | observed: %s' % (
            src[1], row['line'], row['verdict'].replace('*', ''), row['observed'].replace('*', ''))
    _, path, pat, anchor = src
    doc = CAP.read_file(ROOT, path, cache)
    if doc is None:
        return None, '%s: (file absent)' % path
    n, line = CAP.find_line(doc, pat, anchor)
    if line is None:
        return None, '%s: (pattern %r not found)' % (path, pat)
    return ('file', path), '%s:%d  %s' % (path, n, line.strip())


def check_cell(dim, cell, ledger, cache, claims, verified):
    errors, lines, ok_src = [], [], []
    for s in cell['src']:
        r, text = resolve(s, ledger, cache)
        lines.append(text)
        if r is None:
            errors.append('source not resolved: ' + text)
        else:
            ok_src.append(r)
    mk = []
    for cid in cell['mkt']:
        if cid not in claims:
            errors.append('claim id %s absent' % cid)
        elif cid not in verified:
            errors.append('claim id %s not verified in verify.txt' % cid)
        else:
            mk.append(cid)
    g = cell['grade']
    shown = g
    if g not in EVID:
        errors.append('grade %r not in %s' % (g, EVID))
        shown = 'ASSUMED'
    if g in ('MEASURED', 'MODELLED', 'AGAINST') and not ok_src:
        errors.append('%s without a resolved repo source' % g)
        shown = 'ASSUMED'
    if dim == 'Energy' and g == 'MEASURED':
        errors.append('Energy graded MEASURED (energy numbers are MODELLED only)')
        shown = 'ASSUMED'
    if dim == 'Energy' and g in ('MODELLED', 'AGAINST') and not any(
            k == 'file' and p.startswith(ENERGY_DIRS) for k, p in ok_src):
        errors.append('Energy %s without a source in %s' % (g, ' or '.join(ENERGY_DIRS)))
        shown = 'ASSUMED'
    if g == 'ASSUMED' and not cell['assumed']:
        errors.append('ASSUMED without its one-line statement')
    return {'grade': shown, 'declared': g, 'lb': cell['lb'], 'lines': lines, 'mkt': mk, 'errors': errors}


def cap_grade(kid, capres):
    r = capres['caps'].get(kid) or capres['readings'].get(kid)
    return r['grade']


def app_grade(need_grades, dimres, reading='P'):
    gs = [g for _, g in need_grades]
    closed = 'CLOSED' in gs
    pending = 'pending' in gs
    result = 'RESULT' in gs
    model = 'MODEL' in gs
    lb_ass = any(d['lb'] and d['grade'] == 'ASSUMED' for d in dimres.values())
    lb_aga = any(d['lb'] and d['grade'] == 'AGAINST' for d in dimres.values())
    rung = CAP.RUNG
    all_fr = all(g in ('FINDING', 'RESULT') for g in gs)
    all_c = all(g in rung and rung[g] >= rung['CONSTRUCTION'] for g in gs)
    if reading == 'LETTER':
        cond = result or lb_ass
    else:
        cond = result or model or lb_ass or lb_aga
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
    if closed:
        return 'NOT SUPPORTED'
    if cond:
        return 'CONDITIONAL'
    if all_fr and not lb_ass:
        return 'SUPPORTED'
    if all_c:
        return 'CONSTRUCTION-BACKED'
    return 'pending' if pending else 'NO RULE'


def why(need_grades, dimres):
    out = []
    for k, g in need_grades:
        if g in ('CLOSED', 'RESULT', 'MODEL', 'pending'):
            out.append('%s %s' % (k, g))
    for d in DIMS:
        if dimres[d]['lb'] and dimres[d]['grade'] in ('ASSUMED', 'AGAINST'):
            out.append('load-bearing %s %s' % (d, dimres[d]['grade']))
    return '; '.join(out) if out else 'every needed capability at least CONSTRUCTION; no load-bearing dimension ASSUMED or AGAINST'


def wrap(text, indent, width=200, first=None):
    ind = ' ' * indent
    for i, ln in enumerate(textwrap.wrap(' '.join(text.split()), width - indent - 2, break_long_words=True,
                                         break_on_hyphens=False)):
        print((first if (i == 0 and first is not None) else ind + ('  ' if i else '')) + ln)


def evaluate(app, capres, ledger, cache, claims, verified):
    need = [(k, cap_grade(k, capres)) for k in app['needs']]
    dimres = {d: check_cell(d, app['dims'][d], ledger, cache, claims, verified) for d in DIMS}
    return {'need': need, 'dims': dimres, 'grade': app_grade(need, dimres, 'P'),
            'letter': app_grade(need, dimres, 'LETTER'), 'topdown': app_grade(need, dimres, 'TOPDOWN'),
            'why': why(need, dimres)}


def print_app(app, ev, claims):
    print('-' * 118)
    print('%s  %s' % (app['id'], app['name']))
    print('  needs: %s' % ', '.join('%s %s' % (k, g) for k, g in ev['need']))
    for d in DIMS:
        r, cell = ev['dims'][d], app['dims'][d]
        tag = '%s%s' % (d, '*' if r['lb'] else '')
        print('  %-10s %-9s claim: %s' % (tag, r['grade'], cell['claim']))
        if cell['assumed']:
            wrap('assumed: ' + cell['assumed'], 24)
        for ln in r['lines']:
            wrap(ln, 26, first=' ' * 24 + '- ')
        if r['mkt']:
            wrap('market / prior art (verified claims): ' + '; '.join(
                '%s %s' % (cid, claims[cid]['source'][:60]) for cid in r['mkt']), 24)
        for e in r['errors']:
            print('                        ERROR: %s' % e)
    print('  APPLICATION GRADE: %s   (because: %s)' % (ev['grade'], ev['why']))
    if 'pending' in [g for _, g in ev['need']]:
        print('  note: a needed reading is pending; the grade can still fall to NOT SUPPORTED if it closes')
    if ev['letter'] != ev['grade'] or ev['topdown'] != ev['grade']:
        print('  sensitivity: letter of the rule (A2, A3 off) -> %s; top-down order (A1 off) -> %s' % (ev['letter'], ev['topdown']))


def market_block(app_id, claims, verified):
    rows = [c for c in claims.values() if c['application'] == app_id]
    by = {}
    for c in sorted(rows, key=lambda c: (c['id'].split(':')[0], int(c['id'].split(':')[1]))):
        by.setdefault(c['role'], []).append(c['id'] + ('' if c['id'] in verified else '(UNVERIFIED)'))
    return '; '.join('%s: %s' % (r, ', '.join(by[r])) for r in ('who_does_it', 'what_is_hard', 'our_method_relevance',
                                                              'regulation', 'risk') if r in by)


def main():
    capres = CAP.compute()
    ledger = capres['ledger']
    cache = capres['files']
    claims, verified, vsha = load_claims()
    print('APP1 stage B: the applications AP1-AP10, graded on the five dimensions (%s)' % CAP.DECL)
    print('A note, not evidence (R8); "marketable" means "someone could use it, and here is what they would have to believe"; it is')
    print('never a claim of novelty. Every source line below is copied from the pinned output or ledger row named with it.')
    print('Evidence grades: MEASURED (a pinned output shows it for this learner or system), MODELLED (a pinned model or estimate,')
    print('under named assumptions), ASSUMED (follows only if the stated thing holds), AGAINST (the record shows the opposite).')
    print('* marks a load-bearing dimension. Energy numbers come only from Compute_Savings/ and Energy Design Principle/.')
    print('Application grade (the declaration): SUPPORTED / CONSTRUCTION-BACKED / CONDITIONAL / NOT SUPPORTED, read with:')
    print('  A1 order NOT SUPPORTED > CONDITIONAL > SUPPORTED > CONSTRUCTION-BACKED (the only order in which every clause can fire)')
    print('  A2 a needed capability at MODEL -> CONDITIONAL (the rule has no clause for it)')
    print('  A3 a load-bearing dimension AGAINST -> CONDITIONAL (treated as at least as bad as ASSUMED)')
    print("  A4 a pending reading (ROB1) is neither CLOSED nor a rung; A5 AP7 reads K2 through EPS2's federated-client row")
    print('capability grades imported from Applied_Suite/checks/capabilities.py (ledger sha256 %s):' % ledger['sha256'])
    for b in CAP.MAP + CAP.READINGS:
        r = capres['caps'].get(b['id']) or capres['readings'][b['id']]
        print('  %-11s %-13s %s' % (b['id'], r['grade'], b['name']))
    print('claims: %d in claims_m1..m3; verified (every quote PASS in %s, sha256 %s): %d' % (
        len(claims), VERIFY, vsha, len(verified)))
    print()

    evs = {}
    nerr = 0
    for app in APPS + [COMBO]:
        ev = evaluate(app, capres, ledger, cache, claims, verified)
        evs[app['id']] = ev
        nerr += sum(len(ev['dims'][d]['errors']) for d in DIMS)
    for app in APPS:
        print_app(app, evs[app['id']], claims)
        mb = market_block(app['id'], claims, verified)
        if mb:
            wrap('all market claims for %s by role: %s' % (app['id'], mb), 4, first='  ')
    print('-' * 118)
    print("FORECAST 4's COMBINATION (derived row)")
    print_app(COMBO, evs[COMBO['id']], claims)
    gen = market_block('general', claims, verified)
    print('-' * 118)
    wrap('general claims (the sweep-cost, regulation and risk evidence that bears on every application): ' + gen, 4, first='  ')

    print('=' * 118)
    print('SUMMARY (* = load-bearing)')
    print('  %-11s %-62s %-11s %-11s %-11s %-11s %-11s %s' % ('app', 'needs', 'UX', 'Energy', 'Security', 'Privacy', 'Compute',
                                                             'GRADE'))
    for app in APPS + [COMBO]:
        ev = evs[app['id']]
        needs = ', '.join('%s %s' % (k, g) for k, g in ev['need'])
        cells = ['%s%s' % (ev['dims'][d]['grade'], '*' if ev['dims'][d]['lb'] else '') for d in DIMS]
        print('  %-11s %-62s %-11s %-11s %-11s %-11s %-11s %s' % (app['id'], needs, *cells, ev['grade']))
    counts = {}
    for app in APPS:
        counts[evs[app['id']]['grade']] = counts.get(evs[app['id']]['grade'], 0) + 1
    print('  AP1-AP10 by grade: %s' % ', '.join('%s %d' % (g, counts.get(g, 0)) for g in GRADES + ('pending', 'NO RULE')
                                                if counts.get(g, 0) or g in GRADES))
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
    print('  table errors: %d' % nerr)

    print()
    print('SENSITIVITY (the grade under the readings the declaration leaves open)')
    ap7_k2 = app_grade([('K2', cap_grade('K2', capres))], evs['AP7']['dims'], 'P')
    print('  %-11s %-20s %-20s %-20s' % ('app', 'primary (A1-A5)', 'letter (A2, A3 off)', 'top-down (A1 off)'))
    for app in APPS + [COMBO]:
        ev = evs[app['id']]
        print('  %-11s %-20s %-20s %-20s' % (app['id'], ev['grade'], ev['letter'], ev['topdown']))
    print('  AP7 on K2 alone (A5 off): %s' % ap7_k2)

    print()
    print('FORECASTS (the declaration, written before any source or script), scored')
    g = {a: evs[a]['grade'] for a in evs}
    k1 = cap_grade('K1', capres)
    sec51 = CAP.status_of(ledger['rows']['SEC5-1']['verdict']) if 'SEC5-1' in ledger['rows'] else 'absent'
    sup = [a['id'] for a in APPS if g[a['id']] == 'SUPPORTED']
    f1a = not sup
    f1b = CAP.RUNG.get(k1, -1) <= CAP.RUNG['RESULT'] and sec51 == 'FAIL'
    f1 = f1a and f1b
    print('  1. No application is SUPPORTED; K1 is at most RESULT (SEC4-1) with a failed replication, unless SEC6-1 changes that.')
    print('     applications SUPPORTED: %s (%s); K1 %s, SEC5-1 %s, SEC6-1 %s (%s) -> %s' % (
        len(sup), ', '.join(sup) or 'none', k1, sec51, 'present' if 'SEC6-1' in ledger['rows'] else 'pending',
        'holds' if f1b else 'fails', 'HOLDS' if f1 else 'FAILS'))
    f2set = ['AP2', 'AP3', 'AP4', 'AP7', 'AP8']
    f2hits = [a for a in f2set if g[a] == 'CONSTRUCTION-BACKED']
    f2 = len(f2hits) == len(f2set)
    print('  2. AP2, AP3, AP4, AP7 and AP8 are CONSTRUCTION-BACKED.')
    print('     %s; CONSTRUCTION-BACKED %d of %d -> %s' % (', '.join('%s %s' % (a, g[a]) for a in f2set), len(f2hits),
                                                            len(f2set), 'HOLDS' if f2 else 'FAILS'))
    for rd, key in (('letter', 'letter'), ('top-down', 'topdown')):
        hits = [a for a in f2set if evs[a][key] == 'CONSTRUCTION-BACKED']
        print('     sensitivity, %s reading: CONSTRUCTION-BACKED %d of %d (%s)' % (rd, len(hits), len(f2set), ', '.join(hits) or 'none'))
    rob = cap_grade('ROB1', capres)
    f3a, f3b, f3c = g['AP1'] == 'CONDITIONAL', g['AP5'] == 'NOT SUPPORTED', rob == 'pending'
    f3 = f3a and f3b and f3c
    print('  3. AP1 is CONDITIONAL. AP5 is NOT SUPPORTED (K4\'s gates closed). AP6 waits on ROB1.')
    print('     AP1 %s (%s); AP5 %s, K4 %s (%s); ROB1 %s, AP6 %s (%s) -> %s' % (
        g['AP1'], 'holds' if f3a else 'fails', g['AP5'], cap_grade('K4', capres), 'holds' if f3b else 'fails', rob, g['AP6'],
        'holds' if f3c else 'fails', 'HOLDS' if f3 else 'FAILS'))
    cb = evs[COMBO['id']]
    f4a = cb['grade'] == 'CONDITIONAL'
    f4b = cb['dims']['Energy']['grade'] == 'MODELLED'
    f4 = f4a and f4b
    print('  4. The strongest honest case is AP2 + AP9 with K1; it is still CONDITIONAL, and its energy claim is MODELLED (the')
    print('     Compute_Savings estimates), not MEASURED at scale.')
    print('     AP2+AP9+K1 %s (%s); its Energy cell %s (%s) -> %s' % (
        cb['grade'], 'holds' if f4a else 'fails', cb['dims']['Energy']['grade'], 'holds' if f4b else 'fails',
        'HOLDS' if f4 else 'FAILS'))
    above = [a['id'] for a in APPS if g[a['id']] in GRADES and GRADES.index(g[a['id']]) < GRADES.index('CONDITIONAL')]
    print("     'the strongest honest case' is a judgement and is not scored; beside it, the applications graded above")
    print('     CONDITIONAL on the declaration\'s scale: %s' % (', '.join('%s %s' % (a, g[a]) for a in above) or 'none'))
    print('  forecasts: 1 %s, 2 %s, 3 %s, 4 %s' % tuple('HOLDS' if f else 'FAILS' for f in (f1, f2, f3, f4)))

    print()
    print('files read (sha256):')
    for rel in sorted(cache):
        d = cache[rel]
        print('  %s  %s' % (d['sha256'] if d else 'ABSENT' + ' ' * 58, rel))
    nerr += sum(len(r['errors']) for r in list(capres['caps'].values()) + list(capres['readings'].values()))
    print('errors (table and capability MAP): %d' % nerr)
    return 0 if nerr == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
