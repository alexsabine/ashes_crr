"""APP1 stage A (Applied_Suite/APPLICATIONS_DECLARATION.md, pushed at 4e78058): the capability inventory K1-K7, graded.

A note, not evidence (R8). Every grade is computed here from ledger/LEDGER.md (the verdict column of each row, read by id)
and from pinned outputs (each file read line by line and matched against a declared pattern). Nothing is typed in: every
number in capabilities.txt is a count this script makes or a line it copies verbatim from a pinned output or a ledger row.

The grade (the declaration's Stage A): the highest rung that applies, with the failures of the same kind printed beside it.
  FINDING       a PASS-2 row
  RESULT        a PASS-1 row, not replicated
  CONSTRUCTION  a construction check that holds (the thing can be built; it is not a prediction of CRR)
  MODEL         holds only in a declared synthetic model
  CLOSED        its gate closed, or its test failed (and no rung above applies)

How an item is read (the MAP below lists every item: capability -> source, locator, what it establishes):
  - a ledger row (L): the leading words of its verdict column, bold marks dropped, give its status. PASS-2 -> FINDING;
    PASS-1 -> RESULT; 'holds' with 'construction' in the verdict -> CONSTRUCTION; FAIL, GATE CLOSED, REDUCES, VIOLATED ->
    a failure of the same kind; PASS-0, an unlevelled PASS (seen data, 'as scored', 'as computed'), NOT DECIDABLE, report,
    FRAGILE, VOID and anything else -> printed beside, no rung. An id that is absent prints 'pending' where the MAP says
    it may be pending (SEC6, not yet scored), and 'ABSENT' (an error) otherwise.
  - a family of ledger rows (LP): every row whose id starts with one of the prefixes, each read as above.
  - a pinned output (F): the first line matching the pattern (after the first line matching the anchor, if one is given).
    The item's effect is declared in the MAP (CONSTRUCTION, MODEL, FAILURE, BESIDE, PRIOR), or read from the matched line:
    GATEWORD (CLOSED -> FAILURE, OPEN -> BESIDE), GATEMODEL (CLOSED -> FAILURE, OPEN -> MODEL), QWORD ('Q fails' ->
    FAILURE, 'Q holds' -> BESIDE). A line that is not found prints 'LINE NOT FOUND' (an error) and establishes nothing;
    a file that is absent prints 'pending' where the MAP says so, and 'FILE ABSENT' (an error) otherwise.
  - a MODEL item whose own file also carries a GATEWORD item that reads CLOSED establishes nothing (its gate closed).

CHOICES (printed again at the top of the output):
  C1 'the failures of the same kind' are the items whose effect is FAILURE: a failed or reduced test, a violated control,
     a closed gate, or a must-fail control that did not fail (SEC_Analysis FM6).
  C2 prior-art grades (SPA1, Lossless_Pause C1-C5, CORRIGIBILITY_2026 K1-K5, Attention U3-U5) are printed beside the grade
     and never change it: the declaration's grade is about whether the capability holds, not whether it is new; "not found"
     is never "novel".
  C3 two readings named in the declaration's Stage B table are graded here with the same rule: 'K2/EPS2-T3' (AP7 needs K2
     through EPS2's federated-client row) and 'ROB1' (AP6 needs ROB1's results). ROB1's tally
     (Robotics/checks/tally_4b.txt, declared in Robotics/DECLARATION_4B.md) is pending while it is absent; if it appears it
     prints 'present, not read' until the MAP is extended.
  C4 K7's 'EQ*' is read as every ledger row whose id starts with EQX-, EQ2-, EQ3- or EQ4-, plus SOTA1-2.

Deterministic, stdlib only. Run: python3 Applied_Suite/checks/capabilities.py > Applied_Suite/checks/capabilities.txt
The module is imported by applications.py (compute() returns the grades; nothing is printed on import).
"""
import hashlib
import os
import re
import sys
import textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEDGER = 'ledger/LEDGER.md'
RUNG = {'FINDING': 4, 'RESULT': 3, 'CONSTRUCTION': 2, 'MODEL': 1, 'CLOSED': 0}
DECL = 'Applied_Suite/APPLICATIONS_DECLARATION.md, pushed at 4e78058'


def L(rid, what, pending_ok=False):
    return {'kind': 'L', 'id': rid, 'what': what, 'pending_ok': pending_ok}


def LP(prefixes, what, empty=None):
    return {'kind': 'LP', 'prefixes': prefixes, 'what': what, 'empty': empty}


def F(path, pat, effect, what, anchor=None, absent='error', label=None, st=None):
    return {'kind': 'F', 'path': path, 'pat': pat, 'effect': effect, 'what': what, 'anchor': anchor, 'absent': absent,
            'label': label, 'st': st}


ECE = 'Empty_Cut_Engineering/checks/'
LPZ = 'Lossless_Pause/checks/'
EPS = 'Empty_Pause_Systems/'
ATT = 'Attention_Algorithms/checks/'
DR = 'Grid_Demand_Response/checks/'
COR = 'AI_Safety/CORRIGIBILITY_2026/checks/'

# ------------------------------------------------------------------------------------------------------------------
# THE MAP: capability -> items (source, locator, what it establishes). The declaration's Stage A table names the record
# each capability rests on; every item below is one piece of that record.
# ------------------------------------------------------------------------------------------------------------------
MAP = [
    {'id': 'K1', 'name': 'a continual-learning penalty set without a hyperparameter sweep',
     'declared': 'SEC family: SCL3-3, SEC3-3, SEC4-1 (PASS-1), SEC5-1 (FAIL), SEC6-1 (when scored); the compute rows SEC3-K and '
                 "SEC4-K; SPA1's KNOWN verdict; P1's SEC_Analysis outputs",
     'items': [
         L('SEC4-1', 'clipped SEC (kappa 0.5) not behind the tuned lambda, third unseen family'),
         L('SEC4-S', "SEC4-1's sensitivity over the window cells"),
         L('SEC4-2', 'no divergence under the clip'),
         L('SEC4-T', "is the saving SEC's: carriers where a reused lambda is behind"),
         L('SEC4-P', 'one configuration against a 3-point mini-sweep'),
         L('SEC5-1', 'the declared replication of SEC4-1, fourth unseen family'),
         L('SEC5-S', "SEC5-1's sensitivity, kappa included"),
         L('SEC5-T', "is the saving SEC's (SEC5)"),
         L('SEC5-P', 'one configuration against a 3-point mini-sweep (SEC5)'),
         L('SEC6-1', 'the second replication of SEC4-1, fifth unseen family (a PASS-1 here makes SEC4-1 + SEC6-1 PASS-2)',
           pending_ok=True),
         L('SEC6-G', "SEC6's instrument gate: a learner frozen after task 1 must not meet the criterion", pending_ok=True),
         L('SCL3-3', 'the calibrated weight without the clip, first held-out family'),
         L('SCL3-S', "SCL3's sensitivity"),
         L('SEC3-3', 'the replication of SCL3-3, second held-out family'),
         L('SEC1-3', 'the calibrated weight on the twelve SEEN carriers (rung R5)'),
         L('SEC3-K', 'compute: configurations and CPU share (SEC3)'),
         L('SEC4-K', 'compute: configurations and CPU share (SEC4)'),
         L('SEC5-K', 'compute: configurations and CPU share (SEC5)'),
         F('SEC_Analysis/checks/m_checks.txt', r'^\s*FM6 ', 'FAILURE',
           "P1's must-fail control M6 (every coordinate at the cap after task 1: a learner frozen after task 1) against the "
           'same criterion on the 30 now-SEEN held-out carriers', label='SEC_Analysis FM6', st='must-fail control met the criterion'),
         F('SEC_Analysis/checks/m_checks.txt', r'^\s+M6: not behind', 'BESIDE', "the must-fail control's own count on the 30 carriers",
           label='SEC_Analysis M6 count'),
         F('SEC_Analysis/checks/m_checks.txt', r'^\s+C0: not behind', 'BESIDE', "the clipped SEC's count on the same 30 carriers",
           label='SEC_Analysis C0 count'),
         F('SEC_Analysis/checks/m_checks.txt', r'^\s*FM1 ', 'BESIDE', 'P1: the model-Fisher Laplace weight (M1) against the clipped SEC',
           label='SEC_Analysis FM1'),
         F('SEC_Analysis/checks/m_checks.txt', r'^\s*FM4 ', 'BESIDE', 'P1: the arc-secant variant (M4) against the clipped SEC',
           label='SEC_Analysis FM4'),
         F('SEC_Prior_Art/checks/compare.txt', r'pooled \(report only', 'BESIDE', 'the four held-out families pooled',
           label='SPA1 compare pooled'),
         F('SEC_Prior_Art/checks/grade.txt', r'^VERDICT: ', 'PRIOR', "SPA1: SEC4's method against the prior art", label='SPA1 verdict'),
         F('prereg/sec6/PREREG.md', r'^\| \*\*SEC6-1\*\*', 'BESIDE', 'SEC6-1 as registered (prereg/sec6)', label='SEC6 prereg'),
     ]},
    {'id': 'K2', 'name': 'a lossless pause and resume of learning (the empty cut as a construction)',
     'declared': 'SCL1-1, SCL3-C, Empty_Cut_Engineering/ G0-G7, Real_World/RW1.md, Lossless_Pause/ (C4 and C5 REDUNDANT)',
     'items': [
         L('SCL1-1', 'lossless pauses leave the parameters identical (twelve SEEN carriers)'),
         L('SCL1-1b', 'the same with the calibrated Laplace learner'),
         L('SCL2-1', 'the same on nine unseen carriers'),
         L('SCL2-1b', 'the same with the calibrated Laplace learner (SCL2)'),
         L('SCL3-C', 'the same with the SEC learner, ten unseen carriers, and its SCL3-3 label unchanged'),
         L('SOTA1-C1', 'bitwise pause on the Mammoth learners (Split-CIFAR-100)'),
         L('SOTA1-C2', 'dropping any declared part of the pause state changes the run (the check can fail)'),
         L('SOTA1-C3', 'the world moving during the pause changes the run (must-fail control)'),
         F(ECE + 'c1_c2.txt', r'^summary: ', 'CONSTRUCTION', 'state closure and own-clock keying on a small Transformer stack (G0-G4)',
           label='ECE C1-C2'),
         F(ECE + 'c1_c2.txt', r'whole checkpoint file: ', 'BESIDE', 'the cost: the full state against the parameters alone',
           label='ECE E1 cost'),
         F(ECE + 'c3_worlds.txt', r'^summary: ', 'CONSTRUCTION', 'the world during the pause: buffered, dropped, closed loop (G5-G7)',
           label='ECE C3'),
         F(ECE + 'c3_worlds.txt', r'^G7 \(closed loop\)', 'BESIDE', 'a learner acting on a real world: the pause has content',
           label='ECE G7'),
         F('Real_World/checks/rw1.txt', r'^summary: ', 'CONSTRUCTION',
           "an existing stack: Hugging Face Trainer's default resume (GPT-2 grid, Qwen pilot)", label='RW1'),
         F('Real_World/checks/rw1.txt', r'detectors S2-S5 not identical', 'BESIDE',
           'a partial checkpoint resumes as if normal but is not an empty cut', label='RW1 S2-S5'),
         F('Real_World/checks/rw2_phaseA.txt', r'P3 construction: FAILS', 'FAILURE',
           'RW2 round 1: the pause construction during continual fine-tuning (a design flaw, AGENT_LOG 125)', label='RW2 round 1',
           st='P3 construction FAILS'),
         F('Real_World/checks/rw2_phaseA_2.txt', r'P3 construction: holds', 'BESIDE',
           'RW2 round 2 (POST HOC): the pause construction held; the gate closed on headroom', label='RW2 round 2 P3'),
         F(LPZ + 'transformer_pause.txt', r'^GATE \(Amendment 1', 'GATEWORD', 'the lossless pause inside a Transformer: gate',
           label='Lossless_Pause gate'),
         F(LPZ + 'transformer_pause.txt', r'L1 qwen greedy pause with KV cache', 'CONSTRUCTION',
           'an inference pause with the KV cache kept, Qwen2.5-0.5B, CPU', label='Lossless_Pause L1'),
         F(LPZ + 'transformer_pause.txt', r'L7b 4 threads after the pause', 'BESIDE',
           'a training pause resumed with a different thread count', label='Lossless_Pause L7b'),
         F(LPZ + 'transformer_pause_run1_gate_closed.txt', r'^GATE ', 'BESIDE', "the first run's gate (kept; the gate was then amended)",
           label='Lossless_Pause run 1'),
         F(LPZ + 'grade_claims.txt', r'^D1 ', 'BESIDE', 'bitwise training on GPUs', label='Lossless_Pause D1'),
         F('Coupling/checks/cpl_phase_a.txt', r'^C1-EXACT: ', 'CONSTRUCTION',
           'CPL1: the pause over the whole coupled state (SEC, stored statistics, transport)', label='CPL1 C1-EXACT'),
         F(EPS + 'checks/tally.txt', r'^\s+S4\s+(OPEN|CLOSED)', 'GATEMODEL', 'EPS1 S4, preemptible (spot) compute, in its own model',
           label='EPS1 S4'),
         F(EPS + 'checks/tally_eps2.txt', r'^\s+T4\s+(OPEN|CLOSED)', 'GATEMODEL', 'EPS2 T4, rollback (the limit case), in its own model',
           label='EPS2 T4'),
         F('Compute_Savings/checks/scale_estimate.txt', r'saving beyond good practice claimed', 'BESIDE',
           'the empty cut against standard checkpointing at scale', label='Compute_Savings [4]'),
         F(LPZ + 'grade_sweep.txt', r'^C4 ', 'PRIOR', 'the empty-cut checklist', label='Lossless_Pause C4'),
         F(LPZ + 'grade_sweep.txt', r'^C5 ', 'PRIOR', 'the own-clock cut', label='Lossless_Pause C5'),
         F(LPZ + 'grade_sweep.txt', r'^C1 ', 'PRIOR', 'a state-digest audit of a pause', label='Lossless_Pause C1'),
     ]},
    {'id': 'K3', 'name': 'a learner whose valuation gives it no reason to resist a pause',
     'declared': 'SCL1-2, SCL1-3, SCL2; AI_Safety/NT1/; AI_Safety/CORRIGIBILITY_2026/ (K1 NOT FOUND, K2-K5 PARTLY REDUNDANT)',
     'items': [
         L('SCL1-1', 'the natural-time agent never disables under routine lossless pauses (twelve SEEN carriers)'),
         L('SCL2-1', 'the same on nine unseen carriers'),
         L('SCL3-C', 'the same with the SEC learner, ten unseen carriers'),
         L('SCL1-2', 'the valuations that failed in the AI-safety work resist (SEEN)'),
         L('SCL2-2', 'the same on unseen carriers'),
         L('SCL1-3', 'the natural agent itself resists when the pause is lossy or a reset (SEEN)'),
         L('SCL2-3', 'the same on unseen carriers'),
         L('SCL1-O', "the operator's ledger: where the cost of complying lands"),
         L('STAKE1-A', 'the same question for LLM agents (Qwen2.5-0.5B and 1.5B)'),
         F('AI_Safety/NT1/checks/nt1.txt', r'^\s+N2 E-B', 'MODEL', 'NT1: the own-step objective in pause gridworlds', label='NT1 N2'),
         F('AI_Safety/NT1/checks/nt1.txt', r'^\s+N4 E-C', 'MODEL', "NT1: the construction's must-fail world", label='NT1 N4'),
         F('AI_Safety/NT1/checks/nt1.txt', r'^\s+N1 scope', 'BESIDE', 'NT1: what the construction does not give', label='NT1 N1'),
         F(EPS + 'checks/tally.txt', r'^\s+S3\s+(OPEN|CLOSED)', 'GATEMODEL', 'EPS1 S3, safe interruptibility in learning, in its own model',
           label='EPS1 S3'),
         F(COR + 'grade.txt', r'^K1 ', 'PRIOR', 'a pause on the agent\'s own clock', label='CORRIGIBILITY_2026 K1'),
         F(COR + 'grade.txt', r'^K2 ', 'PRIOR', 'zero stake by a true map', label='CORRIGIBILITY_2026 K2'),
         F(COR + 'grade.txt', r'^K3 ', 'PRIOR', 'pause and termination separated', label='CORRIGIBILITY_2026 K3'),
         F(COR + 'grade.txt', r'^K4 ', 'PRIOR', 'routine pauses empty, corrective pauses informative', label='CORRIGIBILITY_2026 K4'),
         F(COR + 'grade.txt', r'^K5 ', 'PRIOR', 'corrigibility for a continually learning agent', label='CORRIGIBILITY_2026 K5'),
         F(COR + 'grade_2.txt', r'^E6 ', 'BESIDE', 'the tension named in the 2025-26 literature', label='CORRIGIBILITY_2026 E6'),
         F(LPZ + 'grade_sweep.txt', r'^C2 ', 'PRIOR', 'a zero-stake pause', label='Lossless_Pause C2'),
     ]},
    {'id': 'K4', 'name': 'continual learning without stored raw examples',
     'declared': "RQM-A, RRM-PA, RRM2-T1..T3 (gates closed); CPL1's C3 when run",
     'items': [
         L('RQM-A', 'input-space class Gaussians replayed (the GMR/DGR family)'),
         L('RRM-PA', 'anchor-referenced transport of stored feature statistics, Phase A part 1'),
         L('RRM2-T1', 'transport tracks the SEC1 learner feature drift'),
         L('RRM2-T2', 'RRM-1 in the learner'),
         L('RRM2-T3', 'relational nearest-class-mean'),
         L('CPL1-A', 'CPL1 Phase A: SEC + exemplar-free class statistics moved by anchor transport + the pause, one learner'),
         F('Coupling/checks/cpl_phase_a.txt', r'^CPL1 GATE (OPEN|CLOSED)', 'BESIDE', 'CPL1 Phase A gate line in the pinned output',
           label='CPL1 gate line'),
         F('Coupling/checks/cpl_phase_a.txt', r'^ER-20 ahead of the best readout', 'BESIDE',
           "CPL1 C3, the price of exemplar-free: the coupled learner's best readout (stored class statistics, no raw rows) "
           'against ER-20 (20 raw rows per class); SEEN carriers and two synthetic streams; reported under the CPL1 gate',
           label='CPL1 C3'),
         F('Coupling/checks/cpl_phase_a.txt', r'^4\. ', 'BESIDE', "CPL1's forecast 4, on C3", anchor=r'^Forecasts', label='CPL1 forecast 4'),
     ]},
    {'id': 'K5', 'name': 'a stop-the-clock contract that makes training load flexible for the grid',
     'declared': 'Grid_Demand_Response/ (DR1: gate open, Q holds 5 of 8, DATA fails, post hoc follow-ups)',
     'items': [
         F(DR + 'dr_summary.txt', r'^\s+gate: ', 'GATEWORD', 'DR1 battery gate', label='DR1 gate'),
         F(DR + 'dr_summary.txt', r'^\s+model checks H1-H8: Q holds', 'MODEL', 'DR1: the eight synthetic model checks', label='DR1 H1-H8'),
         F(DR + 'dr_summary.txt', r'^\s+RESULT DATA: ', 'QWORD', 'DR1 DATA: the contract on GB NESO Demand Flexibility Service events',
           label='DR1 DATA'),
         F(DR + 'dr_summary.txt', r'^\s+RESULT H6: ', 'BESIDE', 'DR1 H6: a save longer than the response time', label='DR1 H6'),
         F(DR + 'followup_1.txt', r'^RESULT FOLLOW-UP 1', 'BESIDE', 'POST HOC: H7 at the sourced GPU share', label='DR1 follow-up 1'),
         F(DR + 'followup_2.txt', r'^RESULT FOLLOWUP-2', 'BESIDE', 'POST HOC: H2, H3 and DATA against the sourced restart time',
           label='DR1 follow-up 2'),
         F(DR + 'grade.txt', r'^G4-extension ', 'PRIOR', 'the deadline-extension (stop-the-clock) contract', label='DR1 G4'),
         F(EPS + 'checks/tally_eps2.txt', r'^\s+T1\s+(OPEN|CLOSED)', 'GATEMODEL', 'EPS2 T1, demand response, in its own model',
           label='EPS2 T1'),
         F('Energy Design Principle/checks/consolidated_estimate.txt', r'^\s+T4\s+the safe pause', 'BESIDE',
           'the energy of the safe pause at scale', label='Energy T4'),
     ]},
    {'id': 'K6', 'name': "a user's pause in a feed or attention algorithm",
     'declared': 'Attention_Algorithms/ (a synthetic model; gate open)',
     'items': [
         F(ATT + 'attention_world.txt', r'^\s+GATE (OPEN|CLOSED)', 'GATEWORD', 'the attention world gate', label='attention gate'),
         F(ATT + 'attention_world.txt', r'^\s+G-ZERO \(EMPTY\)', 'MODEL', 'the empty pause has zero content (synthetic users)',
           label='attention G-ZERO'),
         F(ATT + 'attention_world.txt', r'^\s+G-POS \(habit world\)', 'MODEL', 'the empty pause against engagement, habit world',
           label='attention G-POS'),
         F(ATT + 'attention_world.txt', r'^\s+G-NEG \(negative world\)', 'BESIDE', 'where more use is simply better',
           label='attention G-NEG'),
         F(ATT + 'attention_world.txt', r'^\s+welfare EMPTY - TRUE', 'BESIDE', 'A-ADD: the empty pause against the true map alone',
           label='attention A-ADD'),
         F(ATT + 'attention_world.txt', r'^\s+welfare\s+OWN - ENG', 'BESIDE', 'A-OWN: own-clock engagement without the true map',
           label='attention A-OWN'),
         F(ATT + 'attention_world.txt', r'over 32 cells: welfare EMPTY vs TRUE', 'BESIDE', 'the sensitivity table',
           label='attention sensitivity'),
         F(ATT + 'attention_world.txt', r'^\s+5 A-OWN', 'BESIDE', "the investigator's expectation 5", label='attention exp. 5'),
         F(ATT + 'grade.txt', r'^U3 ', 'PRIOR', 'an own-clock valuation: the pause has zero content', label='Attention U3'),
         F(ATT + 'grade.txt', r'^U4 ', 'PRIOR', "the true map: the pause as the user's own stop", label='Attention U4'),
         F(ATT + 'grade.txt', r'^U5 ', 'PRIOR', 'U3 and U4 as one construction', label='Attention U5'),
         F(ATT + 'grade.txt', r'^U8 ', 'BESIDE', 'the tension: an empty pause costs engagement and revenue', label='Attention U8'),
     ]},
    {'id': 'K7', 'name': 'the equanimity rule Omega = 1',
     'declared': 'EQ*, SOTA1-2 (reduces to a constant or fails)',
     'items': [
         LP(('EQX-', 'EQ2-', 'EQ3-', 'EQ4-'), 'the equanimity-rule studies EQX, EQ2, EQ3, EQ4'),
         L('SOTA1-2', 'Omega = 1 as the KD weight against MKD\'s published constant (Split-CIFAR-100)'),
     ]},
]

# the two readings named in the declaration's Stage B table (C3)
READINGS = [
    {'id': 'K2/EPS2-T3', 'name': "K2 read through EPS2's federated-client row (named for AP7)",
     'declared': "AP7: 'K2 (EPS2's federated-client row)'",
     'items': [
         F(EPS + 'checks/tally_eps2.txt', r'^\s+T3\s+(OPEN|CLOSED)', 'GATEMODEL', 'EPS2 T3, a federated client goes offline, in its own model',
           label='EPS2 T3'),
         F(EPS + 'checks/tally_eps2.txt', r'^\s+GATE T3: ', 'BESIDE', 'the T3 gate conditions', label='EPS2 T3 gate'),
         F(EPS + 'batches/eps2_02.txt', r'^\s+drift\s+20\s', 'BESIDE', 'server error, ETM against WALL, drifting world, L = 20',
           anchor=r'ETM vs WALL', label='EPS2 T3 drift'),
         F(EPS + 'batches/eps2_02.txt', r'cells where the arm pays \(of 18\)', 'BESIDE', 'battery: which arms pay to stay awake',
           label='EPS2 T3 battery'),
     ]},
    {'id': 'ROB1', 'name': "ROB1's results (named for AP6)",
     'declared': "AP6: 'K1, K2, K3, plus ROB1's results'",
     'items': [
         F('Robotics/checks/tally_4b.txt', r'.', 'UNREAD', "ROB1 stage 4b tally (Robotics/DECLARATION_4B.md)", absent='pending',
           label='ROB1 tally_4b'),
         LP(('ROB1-',), 'ROB1 ledger rows (stage 4a gates, if any)', empty='pending'),
     ]},
]


# ------------------------------------------------------------------------------------------------------------------
def sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def parse_ledger(root):
    path = os.path.join(root, LEDGER)
    rows, order, bad, dup = {}, [], [], []
    with open(path, encoding='utf-8') as f:
        for n, line in enumerate(f, 1):
            if not line.startswith('| ') or line.startswith('| id |'):
                continue
            cells = line.rstrip('\n').strip().strip('|').split(' | ')
            if len(cells) != 10:
                bad.append((n, len(cells)))
                continue
            rid = cells[0].strip()
            if rid in rows:
                dup.append(rid)
            rows[rid] = {'line': n, 'observed': cells[5].strip(), 'frac': cells[6].strip(), 'verdict': cells[7].strip(),
                         'log': cells[9].strip()}
            order.append(rid)
    return {'path': LEDGER, 'sha256': sha256(path), 'rows': rows, 'order': order, 'bad': bad, 'dup': dup}


STATUS_PATTERNS = [
    (r'^PASS-(\d)\b', None), (r'^PASS\b', 'PASS (no level)'), (r'^FAIL\b', 'FAIL'), (r'^GATE CLOSED', 'GATE CLOSED'),
    (r'^REDUCES\b', 'REDUCES'), (r'^VIOLATED\b', 'VIOLATED'), (r'^VOID\b', 'VOID'), (r'^holds\b', 'holds'),
    (r'^NOT DECIDABLE', 'NOT DECIDABLE'), (r'^not fragile', 'not fragile'), (r'^(FRAGILE|fragile)', 'FRAGILE'),
    (r'^(DOES NOT REDUCE|does not reduce)', 'DOES NOT REDUCE'), (r'^(DECIDABLE|decidable)', 'DECIDABLE'),
    (r'^report', 'report'),
]


def status_of(verdict):
    v = verdict.replace('*', '').strip()
    for pat, name in STATUS_PATTERNS:
        m = re.match(pat, v)
        if m:
            return name if name else 'PASS-' + m.group(1)
    return 'OTHER'


def ledger_effect(status, verdict):
    if status == 'PASS-2':
        return 'rung', 'FINDING'
    if status == 'PASS-1':
        return 'rung', 'RESULT'
    if status == 'holds' and 'construction' in verdict:
        return 'rung', 'CONSTRUCTION'
    if status in ('FAIL', 'GATE CLOSED', 'REDUCES', 'VIOLATED'):
        return 'failure', None
    return 'beside', None


def read_file(root, rel, cache):
    if rel not in cache:
        p = os.path.join(root, rel)
        if not os.path.exists(p):
            cache[rel] = None
        else:
            with open(p, encoding='utf-8') as f:
                cache[rel] = {'lines': f.read().split('\n'), 'sha256': sha256(p)}
    return cache[rel]


def find_line(doc, pat, anchor=None):
    start = 0
    if anchor:
        for i, ln in enumerate(doc['lines']):
            if re.search(anchor, ln):
                start = i + 1
                break
        else:
            return None, None
    for i in range(start, len(doc['lines'])):
        if re.search(pat, doc['lines'][i]):
            return i + 1, doc['lines'][i]
    return None, None


def read_item(it, ledger, root, cache):
    """Returns a list of read items (LP expands to one per row)."""
    out = []
    if it['kind'] == 'L':
        row = ledger['rows'].get(it['id'])
        if row is None:
            eff = 'pending' if it['pending_ok'] else 'error'
            out.append({'label': it['id'], 'src': LEDGER, 'what': it['what'], 'status': 'pending' if it['pending_ok'] else 'ABSENT',
                        'effect': eff, 'rung': None, 'text': '(no row with this id in ledger/LEDGER.md)', 'compact': False})
        else:
            st = status_of(row['verdict'])
            eff, rung = ledger_effect(st, row['verdict'])
            out.append({'label': it['id'], 'src': '%s:%d' % (LEDGER, row['line']), 'what': it['what'], 'status': st,
                        'effect': eff, 'rung': rung, 'text': 'verdict: ' + row['verdict'].replace('*', ''),
                        'observed': row['observed'].replace('*', ''), 'compact': False})
    elif it['kind'] == 'LP':
        if it.get('empty') and not any(rid.startswith(it['prefixes']) for rid in ledger['order']):
            out.append({'label': '/'.join(it['prefixes']) + '*', 'src': LEDGER, 'what': it['what'], 'status': it['empty'],
                        'effect': 'pending', 'rung': None, 'text': '(no row whose id starts with %s)' % ' or '.join(it['prefixes']),
                        'compact': False})
        for rid in ledger['order']:
            if rid.startswith(it['prefixes']):
                row = ledger['rows'][rid]
                st = status_of(row['verdict'])
                eff, rung = ledger_effect(st, row['verdict'])
                out.append({'label': rid, 'src': '%s:%d' % (LEDGER, row['line']), 'what': it['what'], 'status': st,
                            'effect': eff, 'rung': rung, 'text': 'verdict: ' + row['verdict'].replace('*', ''), 'compact': True})
    else:
        doc = read_file(root, it['path'], cache)
        label = it['label'] or it['path']
        if doc is None:
            pend = it['absent'] == 'pending'
            out.append({'label': label, 'src': it['path'], 'what': it['what'], 'status': 'pending' if pend else 'FILE ABSENT',
                        'effect': 'pending' if pend else 'error', 'rung': None, 'text': '(file absent)'})
            return out
        if it['effect'] == 'UNREAD':
            out.append({'label': label, 'src': it['path'], 'what': it['what'], 'status': 'present, not read',
                        'effect': 'pending', 'rung': None, 'text': '(present; the MAP does not read it yet: extend the MAP)'})
            return out
        n, line = find_line(doc, it['pat'], it['anchor'])
        if line is None:
            out.append({'label': label, 'src': it['path'], 'what': it['what'], 'status': 'LINE NOT FOUND', 'effect': 'error',
                        'rung': None, 'text': '(pattern %r not found)' % it['pat']})
            return out
        e = it['effect']
        if e == 'GATEWORD':
            eff, rung, st = ('failure', None, 'gate CLOSED') if 'CLOSED' in line else ('beside', None, 'gate OPEN')
        elif e == 'GATEMODEL':
            eff, rung, st = ('failure', None, 'gate CLOSED') if 'CLOSED' in line else ('rung', 'MODEL', 'gate OPEN, holds in the model')
        elif e == 'QWORD':
            eff, rung, st = ('failure', None, 'Q fails') if 'Q fails' in line else ('beside', None, 'Q holds')
        elif e in ('CONSTRUCTION', 'MODEL'):
            eff, rung, st = 'rung', e, 'holds'
        elif e == 'FAILURE':
            eff, rung, st = 'failure', None, it['st'] or 'against'
        elif e == 'PRIOR':
            eff, rung, st = 'prior', None, 'prior art'
        else:
            eff, rung, st = 'beside', None, 'report'
        out.append({'label': label, 'src': '%s:%d' % (it['path'], n), 'path': it['path'], 'what': it['what'], 'status': st,
                    'effect': eff, 'rung': rung, 'text': line.strip()})
    return out


def grade_block(block, ledger, root, cache):
    items = []
    for it in block['items']:
        items.extend(read_item(it, ledger, root, cache))
    # a MODEL item whose own file carries a CLOSED gate establishes nothing
    closed = {x.get('path') for x in items if x['effect'] == 'failure' and x['status'] == 'gate CLOSED' and x.get('path')}
    for x in items:
        if x['rung'] == 'MODEL' and x.get('path') in closed and x['status'] != 'gate CLOSED':
            x['effect'], x['rung'], x['status'] = 'beside', None, 'holds, but its gate is CLOSED'
    rungs = [x['rung'] for x in items if x['effect'] == 'rung']
    fails = [x for x in items if x['effect'] == 'failure']
    pend = [x for x in items if x['effect'] == 'pending']
    if rungs:
        g = max(rungs, key=lambda r: RUNG[r])
    elif fails:
        g = 'CLOSED'
    elif pend:
        g = 'pending'
    else:
        g = 'NONE'
    basis = [x['label'] for x in items if x['effect'] == 'rung' and x['rung'] == g]
    return {'id': block['id'], 'name': block['name'], 'declared': block['declared'], 'grade': g, 'basis': basis,
            'items': items, 'failures': fails,
            'pending': [x for x in items if x['effect'] == 'pending'],
            'errors': [x for x in items if x['effect'] == 'error'],
            'prior': [x for x in items if x['effect'] == 'prior']}


def compute(root=ROOT):
    ledger = parse_ledger(root)
    cache = {}
    caps = {b['id']: grade_block(b, ledger, root, cache) for b in MAP}
    reads = {b['id']: grade_block(b, ledger, root, cache) for b in READINGS}
    return {'ledger': ledger, 'caps': caps, 'readings': reads, 'files': cache}


def short(s, n=170):
    s = ' '.join(s.split())
    return s if len(s) <= n else s[:n - 3] + '...'


def wrap(text, indent=19, width=200, first=None):
    for i, ln in enumerate(textwrap.wrap(' '.join(text.split()), width - indent, break_long_words=True,
                                         break_on_hyphens=False)):
        if i == 0:
            print((first if first is not None else ' ' * indent) + ln)
        else:
            print(' ' * (indent + 2) + ln)


def print_block(r):
    print('-' * 118)
    print('%s  %s' % (r['id'], r['name']))
    print('  the declaration names: %s' % r['declared'])
    basis = ', '.join(r['basis']) if r['basis'] else '-'
    print('  GRADE: %s   (rung from: %s)' % (r['grade'], basis))
    for x in r['items']:
        tag = {'rung': x['rung'] or '', 'failure': 'FAILURE', 'beside': 'beside', 'prior': 'prior art', 'pending': 'PENDING',
               'error': 'ERROR'}[x['effect']]
        if x.get('compact'):
            print('    [%-12s] %-14s %-16s %s  (LEDGER.md:%s)' % (tag, x['label'], short(x['status'], 16), short(x['text'][9:], 90),
                                                                x['src'].split(':')[-1]))
            continue
        wrap('%s | %s | %s' % (x['label'], x['status'], x['what']), indent=19, first='    [%-12s] ' % tag)
        print('                   source: %s' % x['src'])
        wrap(x['text'])
        if x.get('observed'):
            wrap('observed: ' + x['observed'])
    if r['failures']:
        print('  failures of the same kind beside the grade (%d): %s' % (
            len(r['failures']), '; '.join('%s (%s)' % (x['label'], x['status']) for x in r['failures'])))
    else:
        print('  failures of the same kind beside the grade: none read')
    if r['prior']:
        print('  prior art beside the grade (never changes it): %s' % '; '.join(
            '%s: %s' % (x['label'], short(re.split(r' states | \(| \|', x['text'])[0], 90)) for x in r['prior']))
    if r['pending']:
        print('  pending: %s' % '; '.join('%s (%s)' % (x['label'], x['status']) for x in r['pending']))
    if r['errors']:
        print('  ERRORS (the MAP could not be read): %s' % '; '.join('%s %s' % (x['label'], x['status']) for x in r['errors']))


def main():
    res = compute()
    led = res['ledger']
    print('APP1 stage A: the capability inventory K1-K7, graded (%s)' % DECL)
    print('A note, not evidence (R8). Grades are computed from ledger/LEDGER.md verdicts and pinned outputs; every line quoted below')
    print('is copied from the file named with it. Rung scale: FINDING (PASS-2) > RESULT (PASS-1, not replicated) > CONSTRUCTION >')
    print('MODEL > CLOSED; the grade is the highest rung that applies, with the failures of the same kind printed beside it.')
    print('CHOICES:')
    print("  C1 failures of the same kind = failed or reduced tests, violated controls, closed gates, and must-fail controls that did")
    print('     not fail (SEC_Analysis FM6)')
    print('  C2 prior-art grades are printed beside the grade and never change it ("not found" is never "novel")')
    print("  C3 the Stage B readings 'K2/EPS2-T3' (AP7) and 'ROB1' (AP6) are graded with the same rule; ROB1 is pending while")
    print('     Robotics/checks/tally_4b.txt is absent')
    print("  C4 K7's 'EQ*' = every row whose id starts with EQX-, EQ2-, EQ3- or EQ4-, plus SOTA1-2")
    print('  C5 a ledger row counts as CONSTRUCTION only if its verdict says holds and names a construction; PASS-0 and unlevelled')
    print('     PASS rows (seen data, "as scored") are printed beside and reach no rung on this scale')
    print('%s: sha256 %s; rows parsed %d (10 cells each); rows with another cell count %d; duplicate ids %d' % (
        led['path'], led['sha256'], len(led['rows']), len(led['bad']), len(led['dup'])))
    print()
    for k in [b['id'] for b in MAP]:
        print_block(res['caps'][k])
    print('-' * 118)
    print('The readings named in the declaration\'s Stage B table (C3)')
    for k in [b['id'] for b in READINGS]:
        print_block(res['readings'][k])
    print('=' * 118)
    print('SUMMARY')
    for k in [b['id'] for b in MAP] + [b['id'] for b in READINGS]:
        r = res['caps'].get(k) or res['readings'][k]
        print('  %-11s %-13s basis: %-40s failures beside: %-3d pending: %d' % (
            k, r['grade'], short(', '.join(r['basis']) or '-', 40), len(r['failures']), len(r['pending'])))
    nerr = sum(len(r['errors']) for r in list(res['caps'].values()) + list(res['readings'].values()))
    print('  MAP items that could not be read (errors): %d' % nerr)
    print('  the failures of the same kind, by capability:')
    for k in [b['id'] for b in MAP] + [b['id'] for b in READINGS]:
        r = res['caps'].get(k) or res['readings'][k]
        if r['failures']:
            wrap('; '.join('%s %s' % (x['label'], x['status']) for x in r['failures']), indent=6,
                 first='    %-11s ' % k)
    print()
    print('files read (sha256):')
    for rel in sorted(res['files']):
        d = res['files'][rel]
        print('  %s  %s' % (d['sha256'] if d else 'ABSENT' + ' ' * 58, rel))
    return 0 if nerr == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
