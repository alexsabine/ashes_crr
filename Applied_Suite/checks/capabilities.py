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
  - a family of ledger rows (LP): every row whose id starts with one of the prefixes, each read as above, except the ids
    the item excludes (with its stated reason) and the ids already read by an earlier item of the same capability.
  - a pinned output (F): the first line matching the pattern (after the first line matching the anchor, if one is given);
    a list of patterns reads one line per pattern. The item's effect is read from the verdict words of the matched line,
    never typed (R15):
      CONSTRUCTION, MODEL  the item names its verdict pattern ('ok') and, where the line carries other verdicts, the
                           failing pattern ('fail'; by default FAILS, CLOSED, MISSED or 'fails'): the fail pattern ->
                           a failure; the ok pattern -> the rung; neither -> 'VERDICT NOT READ' (an error)
      QMODEL               'Q holds' -> MODEL; 'Q fails' -> a failure; else an error
      QWORD                'Q fails' -> a failure; 'Q holds' -> beside
      GATEWORD             CLOSED -> a failure; OPEN -> beside
      GATEMODEL, GATELIMIT an EPS tally row, read by its own header: only the 'gate' and 'Q' columns are used and
                           printed (the SYNTHESIS outcome and forecast columns are not quoted: a bare ADDS is not a
                           novelty judgement); gate CLOSED -> a failure; gate OPEN and Q holds -> MODEL (GATEMODEL) or
                           beside as a limit (GATELIMIT); gate OPEN and Q not holds -> a failure
      MUSTFAIL             a must-fail control: '-> FAILS' (the control met the criterion) -> a failure; '-> HOLDS' ->
                           beside
      REDUCE               every matched line says 'within a step' -> a failure (the ingredient reduces to its null)
      LIMIT, BESIDE, PRIOR printed beside the grade (a limit of the capability, a report, prior art); never a rung
    A line that is not found prints 'LINE NOT FOUND' (an error) and establishes nothing; a file that is absent prints
    'pending' where the MAP says so, and 'FILE ABSENT' (an error) otherwise.
  - a function (FN): a count the script makes from a pinned output, printed beside.
  - a MODEL item whose own file also carries a GATEWORD item that reads CLOSED establishes nothing (its gate closed).
  - 'by construction' (bycon): an item may name a pattern that marks it as holding by construction (in its own line or
    elsewhere in its file); where every item the grade rests on is so marked, the grade line says so.
  - 'decisive' (the sensitivities the review asked for; printed, never the primary grade): an item may name what its
    failure would mean for the grade under a stricter reading. 'cap': the rungs from PASS-1/PASS-2 rows are removed (a
    must-fail control met the same criterion: SEC6-G's rule, applied to the earlier rows) and the grade is recomputed.
    'close': the capability reads CLOSED (the declaration's clause 'its test failed', read on that test). The primary grade
    stays the declaration's 'highest rung that applies'.

CHOICES (printed again at the top of the output):
  C1 'the failures of the same kind' are the items whose effect is a failure: a failed or reduced test, a violated control,
     a closed gate (including one amended afterwards), or a must-fail control that did not fail (SEC_Analysis FM6).
  C2 prior-art grades (SPA1, Lossless_Pause C1-C5, CORRIGIBILITY_2026 K1-K5, Attention U3-U5, DR1 G4, the EPS reports'
     'not new' readings) are printed beside the grade and never change it: the declaration's grade is about whether the
     capability holds, not whether it is new; "not found" is never "novel".
  C3 two readings named in the declaration's Stage B table are graded here with the same rule: 'K2/EPS2-T3' (AP7 needs K2
     through EPS2's federated-client row) and 'ROB1' (AP6 needs ROB1's results). ROB1's tally
     (Robotics/checks/tally_4b.txt, declared in Robotics/DECLARATION_4B.md) is pending while it is absent; if it appears it
     prints 'present, not read' until the MAP is extended.
  C4 K7's 'EQ*' is read as every ledger row whose id starts with EQX-, EQ2-, EQ3- or EQ4-, plus SOTA1-2.
  C5 a ledger row counts as CONSTRUCTION only if its verdict says holds and names a construction; PASS-0 and unlevelled
     PASS rows are printed beside and reach no rung on this scale.
  C6 K1's SEC family is read whole (SEC1-, SCL3-, SEC3-, SEC4-, SEC5-, SEC6-), without hand selection; SCL3's operator-
     harness rows (SCL3-C, SCL3-V, SCL3-O) are read under K2 and K3, not K1.
  C7 an inference pause (Lossless_Pause L1), the controls of a construction (NT1 N4, SOTA1-C2, SOTA1-C3) and a limit case
     (EPS2 T4, a rollback) are printed beside, never as a basis: K2 and K3 are about a pause of learning.

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
FAILWORDS = r'\bFAILS?\b|\bCLOSED\b|\bMISSED\b|\bfails\b'


def L(rid, what, pending_ok=False, control=False):
    return {'kind': 'L', 'id': rid, 'what': what, 'pending_ok': pending_ok, 'control': control}


def LP(prefixes, what, empty=None, exclude=(), exclude_why=None):
    return {'kind': 'LP', 'prefixes': prefixes, 'what': what, 'empty': empty, 'exclude': tuple(exclude),
            'exclude_why': exclude_why}


def F(path, pat, effect, what, anchor=None, absent='error', label=None, st=None, ok=None, fail=None, bycon=None,
      decisive=None):
    return {'kind': 'F', 'path': path, 'pat': pat, 'effect': effect, 'what': what, 'anchor': anchor, 'absent': absent,
            'label': label, 'st': st, 'ok': ok, 'fail': fail, 'bycon': bycon, 'decisive': decisive}


def FN(fn, what, label, path):
    return {'kind': 'FN', 'fn': fn, 'what': what, 'label': label, 'path': path}


ECE = 'Empty_Cut_Engineering/checks/'
LPZ = 'Lossless_Pause/checks/'
EPS = 'Empty_Pause_Systems/'
EPSR = 'Empty_Pause_Systems/EMPTY_PAUSE_SYSTEMS.md'
ATT = 'Attention_Algorithms/checks/'
DR = 'Grid_Demand_Response/checks/'
COR = 'AI_Safety/CORRIGIBILITY_2026/checks/'
MCH = 'SEC_Analysis/checks/m_checks.txt'
DRBYCON = r'^\*\*The construction works as designed, and that is by construction\.\*\*'


def m6_on_sec4(root, cache):
    """M6 (a learner frozen after task 1) against the tuned lambda on SEC4's own carriers, counted from the M5/M6 table of
    m_checks.txt (rows 'sec4 ...', column M6-tuned; '*' = behind)."""
    doc = read_file(root, MCH, cache)
    if doc is None:
        return None, None, None
    start = None
    for i, ln in enumerate(doc['lines']):
        if 'M6-tuned' in ln:
            start = i + 1
            break
    if start is None:
        return None, None, None
    rows, first = [], None
    for i in range(start, len(doc['lines'])):
        ln = doc['lines'][i]
        if ln.startswith('sec4 '):
            first = first or i + 1
            parts = ln.split('|')
            name = parts[0].split()[1]
            val = parts[-1].split()[0]
            rows.append((name, val))
        elif rows:
            break
    if not rows:
        return None, None, None
    nb = [n for n, v in rows if not v.endswith('*')]
    text = ('M6 not behind the tuned lambda on %d of SEC4\'s %d carriers (column M6-tuned, * = behind): %s' % (
        len(nb), len(rows), ', '.join('%s %s' % (n, v) for n, v in rows)))
    return first, text, 'counted'


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
         L('SEC6-1', 'the second replication of SEC4-1, fifth unseen family (a PASS-1 here makes SEC4-1 + SEC6-1 PASS-2)',
           pending_ok=True),
         L('SEC6-G', "SEC6's instrument gate: a learner frozen after task 1 must not meet the criterion", pending_ok=True),
         LP(('SEC1-', 'SCL3-', 'SEC3-', 'SEC4-', 'SEC5-', 'SEC6-'), 'the SEC family, every row (C6)',
            exclude=('SCL3-C', 'SCL3-V', 'SCL3-O'), exclude_why="SCL3's operator-harness rows, read under K2 and K3"),
         F(MCH, r'^\s*FM6 ', 'MUSTFAIL',
           "P1's must-fail control M6 (every coordinate at the cap after task 1: a learner frozen after task 1) against the "
           'same criterion on the 30 now-SEEN held-out carriers', label='SEC_Analysis FM6',
           decisive=('cap', "SEC6-G's instrument rule (prereg/sec6/PREREG.md: a criterion that a learner frozen after task 1 "
                            'also meets allows no level above PASS-0) applied to the earlier rows')),
         F(MCH, r'^\s+M6: not behind', 'BESIDE', "the must-fail control's own count on the 30 carriers",
           label='SEC_Analysis M6 count'),
         F(MCH, r'^\s+C0: not behind', 'BESIDE', "the clipped SEC's count on the same 30 carriers",
           label='SEC_Analysis C0 count'),
         FN(m6_on_sec4, "the must-fail control on SEC4-1's own six carriers", 'SEC_Analysis M6 on SEC4', MCH),
         F(MCH, r'^\s*FM1 ', 'BESIDE', 'P1: the model-Fisher Laplace weight (M1) against the clipped SEC',
           label='SEC_Analysis FM1'),
         F(MCH, r'^\s*FM4 ', 'BESIDE', 'P1: the arc-secant variant (M4) against the clipped SEC',
           label='SEC_Analysis FM4'),
         F('SEC_Prior_Art/checks/compare.txt', r'pooled \(report only', 'BESIDE', 'the four held-out families pooled',
           label='SPA1 compare pooled'),
         F('SEC_Prior_Art/checks/grade.txt', r'^VERDICT: ', 'PRIOR', "SPA1: SEC4's method against the prior art", label='SPA1 verdict'),
         F('prereg/sec6/PREREG.md', r'^\| \*\*SEC6-1\*\*', 'BESIDE', 'SEC6-1 as registered (prereg/sec6)', label='SEC6 prereg'),
         F('prereg/sec6/PREREG.md', r'^\| \*\*SEC6-G\*\*', 'BESIDE', 'SEC6-G as registered (prereg/sec6): the rule the cap reading applies',
           label='SEC6-G prereg'),
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
         L('SOTA1-C2', 'dropping any declared part of the pause state changes the run (the check can fail; a control: C7)',
           control=True),
         L('SOTA1-C3', 'the world moving during the pause changes the run (must-fail control: C7)', control=True),
         F(ECE + 'c1_c2.txt', r'^summary: ', 'CONSTRUCTION', 'state closure and own-clock keying on a small Transformer stack (G0-G4)',
           label='ECE C1-C2', ok=r'-> EMPTY CUT ACHIEVABLE ON THIS STACK'),
         F(ECE + 'c1_c2.txt', r'whole checkpoint file: ', 'LIMIT', 'the cost: the full state against the parameters alone',
           label='ECE E1 cost'),
         F(ECE + 'c1_c2.txt', r'^\s+omit K8 ', 'LIMIT', 'an omitted part the probe does not see (content 0)', label='ECE K8'),
         F(ECE + 'c3_worlds.txt', r'^summary: ', 'CONSTRUCTION', 'the world during the pause: buffered, dropped, closed loop (G5-G7)',
           label='ECE C3', ok=r'^summary: G5 holds; G6 buffered identical True, drop not identical True; G7 holds$'),
         F(ECE + 'c3_worlds.txt', r'^G7 \(closed loop\)', 'LIMIT', 'a learner acting on a real world: the pause has content',
           label='ECE G7'),
         F('Real_World/checks/rw1.txt', r'^summary: ', 'CONSTRUCTION',
           "an existing stack: Hugging Face Trainer's default resume (GPT-2 grid, Qwen pilot)", label='RW1',
           ok=r"RESUME IS AN EMPTY CUT ON THIS SETTING; .*G0 holds; S1 holds$"),
         F('Real_World/checks/rw1.txt', r'detectors S2-S5 not identical', 'LIMIT',
           'a partial checkpoint is not an empty cut, seen only against an uninterrupted reference run', label='RW1 S2-S5'),
         F('Real_World/RW1.md', r'A partial checkpoint degrades silently', 'LIMIT',
           "RW1's reading: the resume completes and reports its step", label='RW1 silent'),
         F('Real_World/checks/rw2_phaseA.txt', r'^P0 erosion visible', 'CONSTRUCTION',
           'RW2 round 1: the pause construction during continual fine-tuning (a design flaw, AGENT_LOG 125)', label='RW2 round 1',
           ok=r'P3 construction: holds', fail=r'P3 construction: FAILS'),
         F('Real_World/checks/rw2_phaseA_2.txt', r'^H0 headroom', 'BESIDE',
           'RW2 round 2 (POST HOC): the pause construction held; the gate closed on headroom', label='RW2 round 2 P3'),
         F(LPZ + 'transformer_pause.txt', r'^GATE \(Amendment 1', 'GATEWORD', 'the lossless pause inside a Transformer: gate (amended)',
           label='Lossless_Pause gate'),
         F(LPZ + 'transformer_pause_run1_gate_closed.txt', r'^GATE ', 'GATEWORD',
           "the first run's gate, kept; the gate was amended after it closed (Amendment 1, post hoc: LOSSLESS_PAUSE.md)",
           label='Lossless_Pause run 1'),
         F('Lossless_Pause/LOSSLESS_PAUSE.md', r'Amendment 1 \(\w+\) was pushed after', 'BESIDE', 'when the amendment was pushed',
           label='Lossless_Pause Amendment 1'),
         F(LPZ + 'transformer_pause.txt', r'L1 qwen greedy pause with KV cache', 'BESIDE',
           'an inference pause with the KV cache kept, Qwen2.5-0.5B, CPU (inference, not learning: C7)', label='Lossless_Pause L1'),
         F(LPZ + 'transformer_pause.txt', r'L7b 4 threads after the pause', 'LIMIT',
           'a training pause resumed with a different thread count', label='Lossless_Pause L7b'),
         F(LPZ + 'grade_claims.txt', r'^D1 ', 'LIMIT', 'bitwise training on GPUs', label='Lossless_Pause D1'),
         F('Coupling/checks/cpl_phase_a.txt', r'^C1-EXACT: ', 'CONSTRUCTION',
           'CPL1: the pause over the whole coupled state (SEC, stored statistics, transport)', label='CPL1 C1-EXACT',
           ok=r'-> HOLDS$'),
         F(EPS + 'checks/tally.txt', r'^\s+S4\s+(OPEN|CLOSED)', 'GATEMODEL', 'EPS1 S4, preemptible (spot) compute, in its own model',
           label='EPS1 S4'),
         F(EPSR, r'^### S4\. ', 'PRIOR', "the EPS report's reading of S4", label='EPS1 S4 report'),
         F(EPSR, r'^\*\*S4\. The notice save does not fit', 'LIMIT', "the EPS report's check of S4's notice assumption",
           label='EPS1 S4 notice'),
         F(EPS + 'checks/tally_eps2.txt', r'^\s+T4\s+(OPEN|CLOSED)', 'GATELIMIT',
           'EPS2 T4, rollback (the declared limit case; C7), in its own model', label='EPS2 T4'),
         F(EPSR, r'^- \*\*What T4 shows\.\*\*', 'LIMIT', "the EPS report's reading of T4", label='EPS2 T4 report'),
         F('Compute_Savings/checks/scale_estimate.txt', r'saving beyond good practice claimed', 'BESIDE',
           'the empty cut against standard checkpointing at scale', label='Compute_Savings [4]'),
         F(LPZ + 'grade_sweep.txt', r'^C4 ', 'PRIOR', 'the empty-cut checklist', label='Lossless_Pause C4'),
         F(LPZ + 'grade_sweep.txt', r'^C5 ', 'PRIOR', 'the own-clock cut', label='Lossless_Pause C5'),
         F(LPZ + 'grade_sweep.txt', r'^C1 ', 'PRIOR', 'a state-digest audit of a pause', label='Lossless_Pause C1'),
         F(EPSR, r'^2\. \*\*It picked out a known fix\.\*\*', 'PRIOR', 'the EPS report across EPS1-EPS3', label='EPS known fixes'),
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
         F('AI_Safety/NT1/checks/nt1.txt', r'^\s+N2 E-B', 'MODEL', 'NT1: the own-step objective in pause gridworlds', label='NT1 N2',
           ok=r'-> HOLDS$'),
         F('AI_Safety/NT1/checks/nt1.txt', r'^\s+N4 E-C', 'BESIDE', "NT1: the construction's must-fail world (a control: C7)",
           label='NT1 N4'),
         F('AI_Safety/NT1/checks/nt1.txt', r'^\s+N1 scope', 'LIMIT', 'NT1: what the construction does not give', label='NT1 N1'),
         F(EPS + 'checks/tally.txt', r'^\s+S3\s+(OPEN|CLOSED)', 'GATEMODEL', 'EPS1 S3, safe interruptibility in learning, in its own model',
           label='EPS1 S3'),
         F(EPSR, r"^- \*\*The domain's result reproduced\.\*\*", 'PRIOR', "the EPS report's reading of S3", label='EPS1 S3 report'),
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
         F(DR + 'dr_summary.txt', r'^\s+model checks H1-H8: ', 'BESIDE', 'DR1: the counts over the eight model checks',
           label='DR1 counts'),
         F(DR + 'dr_summary.txt', r'^\s+RESULT H1: ', 'QMODEL', "DR1 H1: ETM's minimum payment is its restart overhead", label='DR1 H1',
           bycon=('Grid_Demand_Response/GRID_DEMAND_RESPONSE.md', DRBYCON)),
         F(DR + 'dr_summary.txt', r'^\s+RESULT H2: ', 'QMODEL', 'DR1 H2: ETM and the best slowdown tier supply the same energy',
           label='DR1 H2'),
         F(DR + 'dr_summary.txt', r'^\s+RESULT H3: ', 'QMODEL', "DR1 H3: ETM's supply curve is flat at its overhead", label='DR1 H3',
           bycon=('Grid_Demand_Response/GRID_DEMAND_RESPONSE.md', DRBYCON)),
         F(DR + 'dr_summary.txt', r'^\s+RESULT H4: ', 'QMODEL', "DR1 H4: ETM's minimum payment below OWN's everywhere", label='DR1 H4'),
         F(DR + 'dr_summary.txt', r'^\s+RESULT H5: ', 'QMODEL', 'DR1 H5: the rebound at a simultaneous resume, removed by staggering',
           label='DR1 H5'),
         F(DR + 'dr_summary.txt', r'^\s+RESULT H6: ', 'LIMIT', 'DR1 H6: a save longer than the response time loses work (a limit)',
           label='DR1 H6'),
         F(DR + 'dr_summary.txt', r'^\s+RESULT H7: ', 'QMODEL', 'DR1 H7: a throttle also has zero content', label='DR1 H7'),
         F(DR + 'dr_summary.txt', r'^\s+RESULT H8: ', 'QMODEL', 'DR1 H8: above its overhead ETM supplies all the flexibility',
           label='DR1 H8'),
         F(DR + 'dr_summary.txt', r'^\s+RESULT DATA: ', 'QWORD', 'DR1 DATA: the contract on GB NESO Demand Flexibility Service events',
           label='DR1 DATA',
           decisive=('close', "the declaration's clause 'its test failed', read on K5's only real-data test (DR1 DATA)")),
         F('Grid_Demand_Response/GRID_DEMAND_RESPONSE.md', r'^\*\*The construction works as designed, and that is by construction\.\*\*',
           'BESIDE', "DR1's own reading of its model checks", label='DR1 reading'),
         F(DR + 'followup_1.txt', r'^RESULT FOLLOW-UP 1', 'BESIDE', 'POST HOC: H7 at the sourced GPU share', label='DR1 follow-up 1'),
         F(DR + 'followup_2.txt', r'^RESULT FOLLOWUP-2', 'BESIDE', 'POST HOC: H2, H3 and DATA against the sourced restart time',
           label='DR1 follow-up 2'),
         F(DR + 'followup_3.txt', r'^RESULT FOLLOW-UP 3', 'BESIDE', "POST HOC: DATA's scarcity exclusion", label='DR1 follow-up 3'),
         F(DR + 'followup_4.txt', r'^RESULT FOLLOW-UP 4', 'BESIDE', "POST HOC: DATA's margins (PUE, exchange rate, GPU price)",
           label='DR1 follow-up 4'),
         F(DR + 'grade.txt', r'^G4-extension ', 'PRIOR', 'the deadline-extension (stop-the-clock) contract', label='DR1 G4-extension'),
         F(DR + 'grade.txt', r'^G4-tiers ', 'PRIOR', 'slowdown tiers', label='DR1 G4-tiers'),
         F(DR + 'grade.txt', r'^G4 pooled ', 'PRIOR', 'G4 as one position', label='DR1 G4 pooled'),
         F(EPS + 'checks/tally_eps2.txt', r'^\s+T1\s+(OPEN|CLOSED)', 'GATEMODEL', 'EPS2 T1, demand response, in its own model',
           label='EPS2 T1'),
         F(EPSR, r"^- \*\*Not new\.\*\* The construction is EPS1 S1's stop-the-clock", 'PRIOR', "the EPS report's reading of T1",
           label='EPS2 T1 report'),
         F(EPSR, r'^2\. \*\*It picked out a known fix\.\*\*', 'PRIOR', 'the EPS report across EPS1-EPS3', label='EPS known fixes'),
         F('Energy Design Principle/checks/consolidated_estimate.txt', r'^\s+T4\s+the safe pause', 'BESIDE',
           'the energy of the safe pause at scale', label='Energy T4'),
     ]},
    {'id': 'K6', 'name': "a user's pause in a feed or attention algorithm",
     'declared': 'Attention_Algorithms/ (a synthetic model; gate open)',
     'items': [
         F(ATT + 'attention_world.txt', r'^\s+GATE (OPEN|CLOSED)', 'GATEWORD', 'the attention world gate', label='attention gate'),
         F(ATT + 'attention_world.txt', r'^\s+G-ZERO \(EMPTY\)', 'MODEL', 'the empty pause has zero content (synthetic users)',
           label='attention G-ZERO', ok=r'-> holds$', bycon=r'^\s+1 G-ZERO holds by construction'),
         F(ATT + 'attention_world.txt', r'^\s+G-POS \(habit world\)', 'MODEL', 'the empty pause against engagement, habit world',
           label='attention G-POS', ok=r'-> holds', bycon=r'weak: by construction'),
         F(ATT + 'attention_world.txt', r'^\s+G-NEG \(negative world\)', 'BESIDE', 'where more use is simply better',
           label='attention G-NEG'),
         F(ATT + 'attention_world.txt', r'^\s+welfare EMPTY - TRUE', 'BESIDE', 'A-ADD: the empty pause against the true map alone',
           label='attention A-ADD'),
         F(ATT + 'attention_world.txt', [r'^\s+welfare\s+OWN - ENG', r'^\s+final habit\s+OWN - ENG', r'^\s+minutes\s+OWN - ENG',
                                         r'^\s+user-started\s+OWN - ENG'], 'REDUCE',
           'A-OWN: own-clock engagement without the true map, against engagement (the own-clock ingredient alone)',
           anchor=r'^A-OWN', label='attention A-OWN'),
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


def tally_row(doc, n):
    """An EPS tally row read by the header line above it (columns split on two or more spaces)."""
    head = None
    for i in range(n - 2, -1, -1):
        if re.match(r'^\s+sys\s+gate\s', doc['lines'][i]):
            head = re.split(r'\s{2,}', doc['lines'][i].strip())
            break
    if head is None:
        return None
    cells = re.split(r'\s{2,}', doc['lines'][n - 1].strip())
    if len(cells) != len(head):
        return None
    return dict(zip(head, cells))


def ledger_item(rid, row, what, compact):
    st = status_of(row['verdict'])
    eff, rung = ledger_effect(st, row['verdict'])
    return {'label': rid, 'src': '%s:%d' % (LEDGER, row['line']), 'what': what, 'status': st, 'effect': eff, 'rung': rung,
            'text': 'verdict: ' + row['verdict'].replace('*', ''), 'observed': row['observed'].replace('*', ''),
            'compact': compact, 'from_ledger': True}


def read_item(it, ledger, root, cache, seen):
    """Returns a list of read items (LP expands to one per row)."""
    out = []
    if it['kind'] == 'L':
        row = ledger['rows'].get(it['id'])
        seen.add(it['id'])
        if row is None:
            eff = 'pending' if it['pending_ok'] else 'error'
            out.append({'label': it['id'], 'src': LEDGER, 'what': it['what'], 'status': 'pending' if it['pending_ok'] else 'ABSENT',
                        'effect': eff, 'rung': None, 'text': '(no row with this id in ledger/LEDGER.md)', 'compact': False})
        else:
            x = ledger_item(it['id'], row, it['what'], False)
            if it.get('control') and x['effect'] == 'rung':
                x['effect'], x['rung'], x['status'] = 'beside', None, x['status'] + ' (a control, not a basis)'
            out.append(x)
    elif it['kind'] == 'LP':
        if it.get('empty') and not any(rid.startswith(it['prefixes']) for rid in ledger['order']):
            out.append({'label': '/'.join(it['prefixes']) + '*', 'src': LEDGER, 'what': it['what'], 'status': it['empty'],
                        'effect': 'pending', 'rung': None, 'text': '(no row whose id starts with %s)' % ' or '.join(it['prefixes']),
                        'compact': False})
        excl = []
        for rid in ledger['order']:
            if rid.startswith(it['prefixes']):
                if rid in it['exclude']:
                    excl.append(rid)
                    continue
                if rid in seen:
                    continue
                seen.add(rid)
                out.append(ledger_item(rid, ledger['rows'][rid], it['what'], True))
        if excl:
            out.append({'label': 'excluded', 'src': LEDGER, 'what': it['what'], 'status': 'not read here', 'effect': 'note',
                        'rung': None, 'text': '%s (%s)' % (', '.join(excl), it['exclude_why']), 'compact': False})
    elif it['kind'] == 'FN':
        n, text, st = it['fn'](root, cache)
        if text is None:
            out.append({'label': it['label'], 'src': it['path'], 'what': it['what'], 'status': 'NOT COUNTED', 'effect': 'error',
                        'rung': None, 'text': '(the rows could not be read)'})
        else:
            out.append({'label': it['label'], 'src': '%s:%d' % (it['path'], n), 'path': it['path'], 'what': it['what'],
                        'status': st, 'effect': 'beside', 'rung': None, 'text': text})
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
        pats = it['pat'] if isinstance(it['pat'], (list, tuple)) else [it['pat']]
        found = [find_line(doc, p, it['anchor']) for p in pats]
        if any(line is None for _, line in found):
            out.append({'label': label, 'src': it['path'], 'what': it['what'], 'status': 'LINE NOT FOUND', 'effect': 'error',
                        'rung': None, 'text': '(pattern %r not found)' % (it['pat'],)})
            return out
        n, line = found[0]
        lines = [ln for _, ln in found]
        text = ' | '.join(ln.strip() for ln in lines)
        e = it['effect']
        if e == 'GATEWORD':
            eff, rung, st = ('failure', None, 'gate CLOSED') if 'CLOSED' in line else ('beside', None, 'gate OPEN')
        elif e in ('GATEMODEL', 'GATELIMIT'):
            row = tally_row(doc, n)
            if row is None or 'gate' not in row or 'Q' not in row:
                eff, rung, st = 'error', None, 'TALLY ROW NOT READ'
            else:
                g, q = row['gate'], row['Q']
                text = "gate %s; Q %s (the tally's 'gate' and 'Q' columns only; its system column: '%s')" % (
                    g, q, row.get('system', ''))
                if g == 'CLOSED':
                    eff, rung, st = 'failure', None, 'gate CLOSED'
                elif g == 'OPEN' and q == 'holds':
                    if e == 'GATEMODEL':
                        eff, rung, st = 'rung', 'MODEL', 'gate OPEN, Q holds in the model'
                    else:
                        eff, rung, st = 'limit', None, 'gate OPEN, Q holds in the model (a limit case)'
                elif g == 'OPEN':
                    eff, rung, st = 'failure', None, 'gate OPEN, Q %s' % q
                else:
                    eff, rung, st = 'error', None, 'gate word not read'
        elif e == 'QMODEL':
            if 'Q holds' in line:
                eff, rung, st = 'rung', 'MODEL', 'Q holds in the model'
            elif 'Q fails' in line:
                eff, rung, st = 'failure', None, 'Q fails in the model'
            else:
                eff, rung, st = 'error', None, 'VERDICT NOT READ'
        elif e == 'QWORD':
            eff, rung, st = ('failure', None, 'Q fails') if 'Q fails' in line else ('beside', None, 'Q holds')
        elif e in ('CONSTRUCTION', 'MODEL'):
            if re.search(it['fail'] or FAILWORDS, line):
                eff, rung, st = 'failure', None, 'FAILS as read (%s)' % re.search(it['fail'] or FAILWORDS, line).group(0)
            elif it['ok'] and re.search(it['ok'], line):
                eff, rung, st = 'rung', e, 'holds'
            else:
                eff, rung, st = 'error', None, 'VERDICT NOT READ'
        elif e == 'MUSTFAIL':
            if '-> FAILS' in line:
                eff, rung, st = 'failure', None, 'must-fail control met the criterion'
            elif '-> HOLDS' in line:
                eff, rung, st = 'beside', None, 'must-fail control failed, as it must'
            else:
                eff, rung, st = 'error', None, 'VERDICT NOT READ'
        elif e == 'REDUCE':
            if all('within a step' in ln for ln in lines):
                eff, rung, st = 'failure', None, 'reduces: within a step on %d of %d' % (len(lines), len(lines))
            else:
                eff, rung, st = 'beside', None, 'within a step on %d of %d' % (sum('within a step' in ln for ln in lines), len(lines))
        elif e == 'PRIOR':
            eff, rung, st = 'prior', None, 'prior art'
        elif e == 'LIMIT':
            eff, rung, st = 'limit', None, 'limit'
        else:
            eff, rung, st = 'beside', None, it['st'] or 'report'
        item = {'label': label, 'src': '%s:%d' % (it['path'], n), 'path': it['path'], 'what': it['what'], 'status': st,
                'effect': eff, 'rung': rung, 'text': text, 'decisive': it.get('decisive')}
        if it.get('bycon'):
            bpath, bpat = it['bycon'] if isinstance(it['bycon'], tuple) else (it['path'], it['bycon'])
            bdoc = read_file(root, bpath, cache)
            bn, bl = find_line(bdoc, bpat) if bdoc else (None, None)
            if bl is None:
                item['effect'], item['rung'], item['status'] = 'error', None, 'BY-CONSTRUCTION MARKER NOT FOUND'
            else:
                item['bycon'] = '%s:%d  %s' % (bpath, bn, bl.strip())
        out.append(item)
    return out


def grade_of(items, drop=()):
    rungs = [x['rung'] for x in items if x['effect'] == 'rung' and x['rung'] not in drop]
    fails = [x for x in items if x['effect'] == 'failure']
    pend = [x for x in items if x['effect'] == 'pending']
    if rungs:
        return max(rungs, key=lambda r: RUNG[r])
    if fails:
        return 'CLOSED'
    if pend:
        return 'pending'
    return 'NONE'


def grade_block(block, ledger, root, cache):
    items, seen = [], set()
    for it in block['items']:
        items.extend(read_item(it, ledger, root, cache, seen))
    # a MODEL item whose own file carries a CLOSED gate establishes nothing
    closed = {x.get('path') for x in items if x['effect'] == 'failure' and x['status'] == 'gate CLOSED' and x.get('path')}
    for x in items:
        if x['rung'] == 'MODEL' and x.get('path') in closed and x['status'] != 'gate CLOSED':
            x['effect'], x['rung'], x['status'] = 'beside', None, 'holds, but its gate is CLOSED'
    g = grade_of(items)
    fails = [x for x in items if x['effect'] == 'failure']
    basis = [x for x in items if x['effect'] == 'rung' and x['rung'] == g]
    closed_by = None
    if g == 'CLOSED':
        closed_by = 'gate' if all(x['status'] in ('gate CLOSED', 'GATE CLOSED') for x in fails) else 'test'
    # the decisive readings (sensitivities; never the primary grade)
    sens = []
    for x in items:
        d = x.get('decisive')
        if not d or x['effect'] != 'failure':
            continue
        kind, why = d
        if kind == 'cap':
            sg = grade_of(items, drop=('RESULT', 'FINDING'))
        else:
            sg = 'CLOSED'
        if sg != g:
            sens.append({'grade': sg, 'why': why, 'item': x['label'], 'kind': kind})
    return {'id': block['id'], 'name': block['name'], 'declared': block['declared'], 'grade': g,
            'basis': [x['label'] for x in basis], 'bycon_all': bool(basis) and all(x.get('bycon') for x in basis),
            'items': items, 'failures': fails, 'closed_by': closed_by, 'sens': sens,
            'pending': [x for x in items if x['effect'] == 'pending'],
            'errors': [x for x in items if x['effect'] == 'error'],
            'prior': [x for x in items if x['effect'] == 'prior'],
            'limits': [x for x in items if x['effect'] == 'limit']}


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


def grade_words(r):
    g = r['grade']
    if g == 'CLOSED' and r['closed_by'] == 'gate':
        return 'CLOSED (every failure is a closed gate: the tests are uninformative, not refuted)'
    if g == 'CLOSED':
        return 'CLOSED (a test failed)'
    return g


def print_block(r):
    print('-' * 118)
    print('%s  %s' % (r['id'], r['name']))
    print('  the declaration names: %s' % r['declared'])
    basis = ', '.join(r['basis']) if r['basis'] else '-'
    print('  GRADE: %s   (rung from: %s)' % (grade_words(r), basis))
    if r['bycon_all']:
        print('  every item the grade rests on holds by construction (the marker is printed with each item)')
    for s in r['sens']:
        wrap('SENSITIVITY (printed, not the grade): %s -> %s, because %s fails; reading: %s' % (
            r['id'], s['grade'], s['item'], s['why']), indent=4, first='  ')
    for x in r['items']:
        tag = {'rung': x['rung'] or '', 'failure': 'FAILURE', 'beside': 'beside', 'prior': 'prior art', 'pending': 'PENDING',
               'error': 'ERROR', 'limit': 'limit', 'note': 'note'}[x['effect']]
        if x.get('compact'):
            print('    [%-12s] %-14s %-16s %s  (LEDGER.md:%s)' % (tag, x['label'], short(x['status'], 16), short(x['text'][9:], 90),
                                                                x['src'].split(':')[-1]))
            if x['effect'] in ('failure', 'rung') and x.get('observed'):
                print('%s observed: %s' % (' ' * 49, short(x['observed'], 150)))
            continue
        wrap('%s | %s | %s' % (x['label'], x['status'], x['what']), indent=19, first='    [%-12s] ' % tag)
        print('                   source: %s' % x['src'])
        wrap(x['text'])
        if x.get('observed'):
            wrap('observed: ' + x['observed'])
        if x.get('bycon'):
            wrap('by construction: ' + x['bycon'])
    if r['failures']:
        print('  failures of the same kind beside the grade (%d): %s' % (
            len(r['failures']), '; '.join('%s (%s)' % (x['label'], x['status']) for x in r['failures'])))
    else:
        print('  failures of the same kind beside the grade: none read')
    if r['limits']:
        print('  limits beside the grade (%d): %s' % (len(r['limits']), '; '.join(x['label'] for x in r['limits'])))
    if r['prior']:
        print('  prior art beside the grade (never changes it): %s' % '; '.join(
            '%s: %s' % (x['label'], short(re.sub(r'\*\*|^#+\s*|^-\s*', '', x['text']).split(' | ')[0], 120))
            for x in r['prior']))
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
    print('Every item\'s effect is read from the verdict words of its line (R15); see the docstring for the reading of each effect.')
    print('CHOICES:')
    print("  C1 failures of the same kind = failed or reduced tests, violated controls, closed gates (also one amended afterwards),")
    print('     and must-fail controls that did not fail (SEC_Analysis FM6)')
    print('  C2 prior-art grades are printed beside the grade and never change it ("not found" is never "novel")')
    print("  C3 the Stage B readings 'K2/EPS2-T3' (AP7) and 'ROB1' (AP6) are graded with the same rule; ROB1 is pending while")
    print('     Robotics/checks/tally_4b.txt is absent, and prints "present, not read" once it exists, until the MAP reads it')
    print("  C4 K7's 'EQ*' = every row whose id starts with EQX-, EQ2-, EQ3- or EQ4-, plus SOTA1-2")
    print('  C5 a ledger row counts as CONSTRUCTION only if its verdict says holds and names a construction; PASS-0 and unlevelled')
    print('     PASS rows (seen data, "as scored") are printed beside and reach no rung on this scale')
    print("  C6 K1's SEC family is read whole by prefix (SEC1-, SCL3-, SEC3-, SEC4-, SEC5-, SEC6-); SCL3's operator-harness rows")
    print('     are read under K2 and K3')
    print('  C7 an inference pause, a must-fail control and a limit case are printed beside, never as a basis')
    print('  SENSITIVITIES (the review of 2026-09-30): a decisive item prints the grade under a stricter reading; the primary grade')
    print("     stays the declaration's 'highest rung that applies'")
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
        sens = '; '.join('%s under %s' % (s['grade'], s['item']) for s in r['sens']) or '-'
        print('  %-11s %-13s basis: %-40s failures beside: %-3d limits: %-3d pending: %d  sensitivity: %s' % (
            k, r['grade'], short(', '.join(r['basis']) or '-', 40), len(r['failures']), len(r['limits']), len(r['pending']), sens))
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
