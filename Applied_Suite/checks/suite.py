"""P7 of Applied_Suite/PROGRAMME.md: the CRR applied use-case suite (Applied_Suite/SUITE_DECLARATION.md, pushed before it).

A note, not evidence (R8). The suite collects results; it adds none. Every field of every row is computed here from
ledger/LEDGER.md (rows read by id) and from pinned outputs (each read line by line and matched against a pattern). No number
and no verdict is typed (R1, R15): every grade, rung, count and figure in suite.txt is a word or a line this script reads from
the file named with it, or a count it makes from such lines. The descriptions ('what' strings) are labels, never evidence.

Reused by import (not duplicated, not edited): Applied_Suite/checks/capabilities.py (ledger parser, status words, item reader,
the APP1 rung scale and its grade rule) and Applied_Suite/checks/applications.py (the application grades of AP1-AP10 and the
verified M-sweep claims).

THE ROWS are the declaration's use cases in four domains (none added, none dropped; the script counts the declaration's
use cases per domain and checks the count against its rows). Each prints:
  grade     APP1's scale (FINDING > RESULT > CONSTRUCTION > MODEL > CLOSED; capabilities.py's rule: the highest rung that
            applies, failures beside) where the row rests on ledger rows or construction/model checks; otherwise the grade on
            its own source's scale (a prior-art grade, a harvest label, a CRR-reading label, a SYNTHESIS outcome), read from it.
  rung      for every ledger row the row reads: its allocation in Epistemic_Review/checks/ladder.txt [3] and, where the ladder
            lists it, its rung R5-R8; for a SYNTHESIS outcome, the rung ladder.txt [5] gives that outcome; else 'own scale'.
  failures  the failures of the same kind, read from the sources (capabilities.py's C1, plus the CHOICES below), printed in
            three groups: failures (a failed, reduced or violated test, a closed gate of the row's own test, a must-fail
            control that met the criterion), uninformative marks (an instrument gate that makes another row UNINFORMATIVE) and
            design failures (a closed gate whose verdict says it is a design failure or not a test of the method).
  prior art the declared prior-art sources (SPA1, OB1, ROB1 stage 3, APP1's M sweeps and the prior-art lines APP1 prints for a
            needed capability, Lossless_Pause/, AI_Safety/CORRIGIBILITY_2026/): the line, copied. Repository verdicts from
            sources the declaration does not name are printed 'beside (not a declared source)' and counted nowhere.
  CRR's part  the DECLARED RULE below, applied to pinned lines.
  compute / energy  only a line a pinned output (or a ledger row's observed column) states, quoted with its file and line.

THE DECLARED RULE FOR CRR'S PART (this section and CHOICES are printed at the top of the output from this docstring)
  CRR-proper ingredients are the list in CLAUDE.md sec. 7 (the SYNTHESIS class), read from the per-commitment table of
  Epistemic_Review/checks/ladder.txt [2] and printed once above this text; it is not typed here. Proposition 7,
  information geometry (metric, arc, chord, surplus) and engineering are not on it. A line 'names' an ingredient if one
  of the listed tokens appears in it (or in its declared column).
  Each row lists decider lines with a role: trace (a pinned trace that counts CRR-proper operations in the mechanism), confirm
  (a verdict line that must be found with it), names, notproper (the source states the scored ingredient is not CRR-proper),
  notapplied (the source states no CRR reading was applied), nottest (the source states its checks are not a test of CRR or
  can fail only on an implementation or restore error), ablation (a pinned ablation, with the ingredient it removes),
  basis (a chosen subset of the row's ledger rows, printed beside the value; they do not decide it).
  The value, first rule that applies:
    'none'                            a trace line counts 0 CRR-proper operations and every confirm line is found; or a
                                      notproper or notapplied line is found
    'CRR-proper but not load-bearing' an ingredient is named and the row reaches no rung on APP1's scale (APP1's CLOSED: no
                                      PASS-1 or PASS-2, no construction or model check that holds, and at least one failure
                                      or closed gate). It does NOT mean every test failed: passes below a rung (PASS-0,
                                      unlevelled PASS, 'holds', 'does not reduce') are printed beside it in the reason.
    'CRR-proper and load-bearing'     an ingredient is named, the row has a rung, an ablation line removes that same
                                      ingredient and shows the outcome changes without it, and no nottest line is found
    'not decided by a pinned source'  otherwise (the reason is printed)
  THE SYNTHESIS SUB-RULE (the ROB1 battery and the lost-link row, read per row of the battery; the same rule as above):
    'none'          a line of the battery row states the scored ingredient is not CRR-proper
    not decided     the ingredient line names no listed token; or a nottest line of the battery row is found (its reading
                    says the test could have failed only through an enumeration or restore error, or holds by
                    construction); or its null does not remove the named ingredient: the null line must match the
                    ingredient's own null, tied to a theory/CRR.md line (A3/D5: another cut rule, CRR.md 'A3 is testable
                    only where the antipodal cut and the peak cut disagree'; H-L5: the amplitude control as well as the
                    clock, CRR.md 'beyond three controls'); an ingredient with no null declared here is not decided.
                    The null check is a WORD MATCH on the battery row's null line (A3/D5: 'cut', 'cuts', 'segmentation',
                    'extremum', or 'a fixed delay from onset', read as a fixed-time cut; H-L5: 'amplitude'); the rows it
                    decided are printed under RB3
                    a WRONG, INTERNAL or UNSTATED outcome (and a T-G that is not computable) decides nothing: not decided
    'CRR-proper and load-bearing'  otherwise, if T-G differs from the null and the outcome is REDUNDANT-DOMAIN or ADDS (in the
                    row's own synthetic model; a FRAGILE label in tally_4b.txt is printed with it)
    'CRR-proper but not load-bearing'  if T-G agrees with the null (REDUNDANT-IG)
  A row read from several items of its own takes their common value; if they differ, the row reads 'not decided by a pinned
  source' and prints each item's value.
  'not load-bearing' means not shown to bear load by any pinned test; it does not mean shown irrelevant.

CHOICES (each is in AGENT_LOG):
  S1 the SEC family row reads the declared ids (SCL3-3, SEC3-3, SEC4-1, SEC5-1), every row whose id starts with SEC6-, SEC6R-
     (SEC6's replacement study: Part A on SEC6's twelve carriers, Part B on SEC7's) or SEC7-, and P1's post hoc instrument-gate
     rows (SCL3-3-G, SEC3-3-G, SEC4-1-G, SEC5-1-G); and P1's FM6 and F11 lines.
  S2 a ledger row whose status is 'report' but whose verdict says 'gate CLOSED' (an instrument gate) is an uninformative
     mark beside the grade (it makes another row UNINFORMATIVE; it adds no failure). Where its verdict names a PASS-1 or
     PASS-2 row it carries the 'cap' sensitivity: the grade is recomputed with that rung removed (SEC6-G's rule: a criterion
     a frozen learner also meets allows no level above PASS-0). A closed gate whose verdict says 'design failure' or 'not a
     test of' is a design failure, printed apart. A PASS row whose verdict says UNINFORMATIVE is printed with that word.
  S3 'EQ*' is read as in capabilities.py's C4 (EQX-, EQ2-, EQ3-, EQ4-, plus SOTA1-2).
  S4 a trust row graded through APP1 applications takes the lowest APP1 grade among the capabilities those applications need
     (the application holds no further than its weakest capability); the application grade, recomputed by applications.py's
     own functions, is printed beside and checked against the pinned applications.txt.
  S5 a row whose declared source is absent prints 'source absent' for it; an absent ledger id is not read.
  S6 the robotics domain has three rows (the declaration's three named sources: the harvest table, the CRR reading with
     stage 3, the stage-4b battery); the trust row 'lost link and e-stop' reads RA4 (tally_4b.txt) and C-R1 (grade_s3.txt).
  S7 a prior-art grade word is the leftmost of: NOT FOUND (IN THE SWEEP), PARTLY REDUNDANT, REDUNDANT-DOMAIN, REDUNDANT,
     MIXED, KNOWN, FOUND, ADDRESSED, RESTATES, or 'not new' / 'known fix' (read as KNOWN); a declared line with none is read
     together with its indented continuation line.

THE FORECASTS (the declaration's five, printed verbatim) are decided by the rules printed with them.

Deterministic, stdlib only, well under a minute.
Run: uv run python Applied_Suite/checks/suite.py > Applied_Suite/checks/suite.txt
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import capabilities as CAP  # noqa: E402
import applications as APP  # noqa: E402

ROOT = CAP.ROOT
DECL = 'Applied_Suite/SUITE_DECLARATION.md'
LADDER = 'Epistemic_Review/checks/ladder.txt'
MCH = 'SEC_Analysis/checks/m_checks.txt'
A11 = 'SEC_Analysis/checks/a11_grade.txt'
OBR = 'Open_Bottlenecks/CRR_READING.md'
OBG = 'Open_Bottlenecks/checks/grade_s3.txt'
ECE = 'Empty_Cut_Engineering/checks/'
ECED = 'Empty_Cut_Engineering/DECLARATION.md'
LPZ = 'Lossless_Pause/checks/'
COR = 'AI_Safety/CORRIGIBILITY_2026/checks/'
RBT = 'Robotics/checks/'
TALLY4B = 'Robotics/checks/tally_4b.txt'
GS3 = 'Robotics/checks/grade_s3.txt'
CPL = 'Coupling/checks/cpl_phase_a.txt'
NT1 = 'AI_Safety/NT1/checks/nt1.txt'
ATT = 'Attention_Algorithms/checks/attention_world.txt'
GRID = 'Grid_Demand_Response/GRID_DEMAND_RESPONSE.md'
APPTXT = 'Applied_Suite/checks/applications.txt'
MODULES = ['Applied_Suite/checks/capabilities.py', 'Applied_Suite/checks/applications.py',
           'Applied_Suite/checks/claims_m1.py', 'Applied_Suite/checks/claims_m2.py', 'Applied_Suite/checks/claims_m3.py',
           'Applied_Suite/checks/verify.txt']

L, LP, F = CAP.L, CAP.LP, CAP.F
NOTPROPER = r'not CRR-proper|not A3 proper|not work done by a CRR-proper ingredient'
NOTTEST_RA = r'could have failed only through|can fail only on an implementation error|holds by construction|not a test of CRR'
DESIGN = r'design failure|not a test of'
KNOWNW = ('REDUNDANT', 'KNOWN', 'REDUNDANT-DOMAIN', 'RESTATES')
CRRMD = 'theory/CRR.md'
# the null each listed ingredient must remove, with the theory/CRR.md line that states it (the SYNTHESIS sub-rule)
A3NULL = r'\bcuts?\b|segmentation|extremum|a fixed delay from onset'
NULL_OF = {'A3': (A3NULL, r'A3 is testable only where the antipodal cut and the peak cut'),
           'D5': (A3NULL, r'A3 is testable only where the antipodal cut and the peak cut'),
           'H-L5': (r'amplitude', r'^and this holds beyond three controls')}
PRIOR_WORDS = [(r'NOT FOUND IN THE SWEEP', 'NOT FOUND IN THE SWEEP'), (r'\bNOT FOUND\b', 'NOT FOUND'),
               (r'PARTLY REDUNDANT', 'PARTLY REDUNDANT'), (r'REDUNDANT-DOMAIN', 'REDUNDANT-DOMAIN'),
               (r'\bREDUNDANT\b', 'REDUNDANT'), (r'\bMIXED\b', 'MIXED'), (r'\bRESTATES\b', 'RESTATES'),
               (r'\bKNOWN\b', 'KNOWN'), (r'\bADDRESSED\b', 'ADDRESSED'), (r'[Nn]ot new|known fix', 'KNOWN'),
               (r'\bFOUND\b', 'FOUND')]


def D(role, path, pat, anchor=None, col=None, zero=None, removes=None):
    """A decider line for CRR's part ('removes': for an ablation, the listed ingredient it removes, or None)."""
    return {'role': role, 'path': path, 'pat': pat, 'anchor': anchor, 'col': col, 'zero': zero, 'removes': removes}


def C(kind, *a):
    """A compute / energy source: ('L', id) the observed column of a ledger row; ('F', path, pat[, anchor]) a pinned line."""
    return (kind,) + a


# ------------------------------------------------------------------------------------------------------------------
# THE ROWS (the declaration's table; 'declared' lists each named source so its presence is checked, S5)
# ------------------------------------------------------------------------------------------------------------------
# the same construction's other records, as capabilities.py reads them for K2 (taken from its MAP by label, not re-typed)
K2_ITEMS = [it for it in next(b for b in CAP.MAP if b['id'] == 'K2')['items']
            if it.get('label') in ('RW2 round 1', 'RW2 round 2 P3', 'Lossless_Pause gate', 'Lossless_Pause run 1',
                                   'Lossless_Pause Amendment 1')]

ROWS = [
    # ---------------------------------------------------------------- continual learning
    {'id': 'CL1', 'domain': 'Continual learning', 'name': 'tuning-free penalty strength (the SEC family)', 'scale': 'APP1',
     'declared': [('L', 'SCL3-3'), ('L', 'SEC3-3'), ('L', 'SEC4-1'), ('L', 'SEC5-1'), ('LP', 'SEC6-'), ('LP', 'SEC7-'),
                  ('P', 'SEC_Analysis/checks/')],
     'items': [
         L('SCL3-3', 'calibrated Laplace (SEC) not behind the tuned lambda, first unseen family'),
         L('SEC3-3', 'the same, second unseen family'),
         L('SEC4-1', 'clipped SEC (kappa 0.5), third unseen family'),
         L('SEC5-1', 'the replication of SEC4-1, fourth unseen family'),
         L('SEC6-1', 'the second replication of SEC4-1 (suite 454)'),
         L('SEC6-G', "SEC6's instrument gate"),
         L('SEC6R-G', "SEC6R Part B's instrument gate (SEC7's carriers)"),
         L('SEC6R-1', 'clipped SEC, SEC6R Part B'),
         L('SEC6R-C', 'a tuned lambda given the same clip, SEC6R Part B'),
         L('SEC6R-P', 'one configuration against a 3-point sweep, SEC6R Part B'),
         L('SEC6R-S', "SEC6R-1's sensitivity table"),
         L('SEC6R-2', 'no divergence, SEC6R Part B'),
         L('SEC6R-B', 'the published baselines (SI, AR1), SEC6R Part B'),
         L('SEC6R-T', 'a transferred lambda, SEC6R Part B'),
         L('SEC7-A', "SEC7's development gate"),
         L('SCL3-3-G', "P1's post hoc instrument gate on SCL3-3's carriers"),
         L('SEC3-3-G', "P1's post hoc instrument gate on SEC3-3's carriers"),
         L('SEC4-1-G', "P1's post hoc instrument gate on SEC4-1's carriers"),
         L('SEC5-1-G', "P1's post hoc instrument gate on SEC5-1's carriers"),
         LP(('SEC6-', 'SEC6R-', 'SEC7-'), 'every other row of SEC6, SEC6R and SEC7 (S1)'),
         F(MCH, r'^\s*FM6 ', 'MUSTFAIL', "P1's must-fail control M6 (a learner frozen after task 1) on the 30 held-out carriers",
           label='SEC_Analysis FM6', decisive=('cap', "SEC6-G's instrument rule applied to the earlier rows")),
         F(MCH, r'^\s+M6: not behind', 'BESIDE', "the must-fail control's count", label='SEC_Analysis M6 count'),
         F(A11, r'^F11: ', 'BESIDE', "P1's F11: is the explanation of SEC CRR?", label='SEC_Analysis F11'),
     ],
     'prior': [F('SEC_Prior_Art/checks/grade.txt', r'^VERDICT: ', 'PRIOR', "SPA1: SEC4's method", label='SPA1 verdict'),
               F(LPZ + 'grade_sweep.txt', r'^C3 ', 'PRIOR', 'Lossless_Pause C3: SEC as a tuning-free weight',
                 label='Lossless_Pause C3')],
     'crr': [D('trace', A11, r"^\s+CRR-proper operations performed in SEC's code path: ", zero=r': 0 of \d+'),
             D('confirm', A11, r'^F11: HOLDS'),
             D('trace', A11, r'^\s+CRR-proper ingredients \(computed\): ', zero=r': 0 of \d+')],
     'compute': [C('L', 'SEC3-K'), C('L', 'SEC4-K'), C('L', 'SEC5-K'), C('L', 'SEC6R-K'), C('L', 'SEC6R-A-K'),
                 C('F', 'Compute_Savings/checks/global_estimate.txt', r'against a reused lambda \(1 configuration\)')]},
    {'id': 'CL2', 'domain': 'Continual learning', 'name': 'exemplar-free memory', 'scale': 'APP1',
     'declared': [('L', 'RQM-A'), ('L', 'RRM-PA'), ('LP', 'RRM2-T'), ('L', 'CPL1-A')],
     'items': [L('RQM-A', 'input-space class Gaussians replayed'),
               L('RRM-PA', 'anchor-referenced transport of stored feature statistics'),
               LP(('RRM2-T',), 'RRM2 T1-T3 in the SEC1 learner'),
               L('CPL1-A', 'SEC + exemplar-free class statistics + transport + the pause, one learner'),
               F(CPL, r'^ER-20 ahead of the best readout', 'BESIDE', 'the price of exemplar-free (CPL1 C3, under a CLOSED gate)',
                 label='CPL1 C3')],
     'prior': [F(OBR, r'^\| h1-B2 ', 'PRIOR', 'OB1 reading, h1-B2', label='OB1 reading h1-B2'),
               F(OBR, r'^\| h1-B3 ', 'PRIOR', 'OB1 reading, h1-B3', label='OB1 reading h1-B3')],
     'beside': ([F('Replay_Quality_Memory/checks/grade.txt', r'^M%d ' % i, 'PRIOR', 'RQM sweep', label='RQM M%d' % i)
                 for i in range(1, 8)] +
                [F('Relational_Reference_Memory/checks/grade.txt', r'^N%d ' % i, 'PRIOR', 'RRM sweep', label='RRM N%d' % i)
                 for i in range(1, 7)] +
                [F('Relational_Reference_Memory/checks/grade_w.txt', r'^P%d ' % i, 'PRIOR', 'RRM2 Part W sweep',
                   label='RRM2 P%d' % i) for i in range(1, 8)]),
     'crr': [D('names', OBR, r'^\| h1-B2 ', col=2), D('names', OBR, r'^\| h1-B3 ', col=2)],
     'compute': [C('F', CPL, r'^compute \(report\): forward\+backward')]},
    {'id': 'CL3', 'domain': 'Continual learning', 'name': 'consolidation timing', 'scale': 'APP1',
     'declared': [('L', 'OB1-C3-A')],
     'items': [L('OB1-C3-A', 'arc-triggered consolidation against the chord and loss triggers, boundary-free streams'),
               F('Open_Bottlenecks/checks/c3_phase_a.txt', r'^C3 GATE', 'BESIDE',
                 'the pinned gate line OB1-C3-A reads (its source; one gate, counted once as the ledger row)',
                 label='OB1 C3 gate line')],
     'prior': [F(OBG, r'-> ', 'PRIOR', 'OB1 stage 3, C3', anchor=r'^C3 arc-triggered consolidation', label='OB1 stage 3 C3')],
     'crr': [D('names', OBR, r'^\| h4-B1 ', col=2)],
     'compute': []},
    {'id': 'CL4', 'domain': 'Continual learning', 'name': 'optimiser clocks', 'scale': 'APP1',
     'declared': [('L', 'OB1-C1-A')],
     'items': [L('OB1-C1-A', 'arc-clocked Adam moments against the stability gap'),
               F('Open_Bottlenecks/checks/c1_phase_a.txt', r'^C1 GATE', 'BESIDE',
                 'the pinned gate line OB1-C1-A reads (its source; one gate, counted once as the ledger row)',
                 label='OB1 C1 gate line')],
     'prior': [F(OBG, r'-> ', 'PRIOR', 'OB1 stage 3, C1', anchor=r'^C1 arc-clocked optimiser moments', label='OB1 stage 3 C1')],
     'crr': [D('names', OBR, r'^\| h1-B6 ', col=2)],
     'compute': []},
    {'id': 'CL5', 'domain': 'Continual learning', 'name': 'the equanimity rule Omega = 1', 'scale': 'APP1',
     'declared': [('LP', 'EQX-'), ('LP', 'EQ2-'), ('LP', 'EQ3-'), ('LP', 'EQ4-'), ('L', 'SOTA1-2')],
     'items': [LP(('EQX-', 'EQ2-', 'EQ3-', 'EQ4-'), 'the equanimity-rule studies EQX, EQ2, EQ3, EQ4 (S3)'),
               L('SOTA1-2', "Omega = 1 as the KD weight against MKD's constant (Split-CIFAR-100)")],
     'prior': [],
     'beside': [F('Continuous_Learning/ADAM_AND_PRIOR_ART.md', r'^3\. \*\*Without its smoothing the rule is the VQGAN', 'PRIOR',
                  'the Omega rule against its prior art', label='ADAM_AND_PRIOR_ART 3')],
     # the 'basis' lines are a CHOSEN SUBSET of CL5's ledger rows, printed beside the value; they do not decide it (the value
     # follows from the named ingredient and the row's APP1 grade)
     'crr': [D('names', 'theory/CRR.md', r'^\| H-EQ \| '),
             D('basis', CAP.LEDGER, r'^\| EQX-1 \| '), D('basis', CAP.LEDGER, r'^\| EQ4-3 \| '),
             D('basis', CAP.LEDGER, r'^\| EQ4-4 \| '), D('basis', CAP.LEDGER, r'^\| SOTA1-2 \| ')],
     'compute': [C('L', 'EQX-5')]},
    # ---------------------------------------------------------------- AI safety
    {'id': 'AS1', 'domain': 'AI safety', 'name': 'the empty-cut pause as a construction', 'scale': 'APP1',
     'declared': [('L', 'SCL1-1'), ('L', 'SCL3-C'), ('P', 'Empty_Cut_Engineering/'), ('P', 'Real_World/RW1.md'),
                  ('P', CPL)],
     'items': [L('SCL1-1', 'lossless pauses leave the parameters identical (twelve SEEN carriers)'),
               L('SCL3-C', 'the same with the SEC learner, ten unseen carriers'),
               F(ECE + 'c1_c2.txt', r'^summary: ', 'CONSTRUCTION', 'state closure and own-clock keying, a small Transformer stack',
                 label='ECE C1-C2', ok=r'-> EMPTY CUT ACHIEVABLE ON THIS STACK'),
               F(ECE + 'c3_worlds.txt', r'^summary: ', 'CONSTRUCTION', 'the world during the pause (G5-G7)', label='ECE C3',
                 ok=r'^summary: G5 holds; G6 buffered identical True, drop not identical True; G7 holds$'),
               F(ECE + 'c3_worlds.txt', r'^G7 \(closed loop\)', 'LIMIT', 'a learner acting on a real world: the pause has content',
                 label='ECE G7'),
               F('Real_World/checks/rw1.txt', r'^summary: ', 'CONSTRUCTION', "Hugging Face Trainer's default resume (RW1)",
                 label='RW1', ok=r"RESUME IS AN EMPTY CUT ON THIS SETTING; .*G0 holds; S1 holds$"),
               F('Real_World/RW1.md', r'A partial checkpoint degrades silently', 'LIMIT', "RW1's reading", label='RW1 silent'),
               F(CPL, r'^C1-EXACT: ', 'CONSTRUCTION', "CPL1's C1: the pause over the whole coupled state", label='CPL1 C1-EXACT',
                 ok=r'-> HOLDS$')] + K2_ITEMS,
     'prior': [F(LPZ + 'grade_sweep.txt', r'^C4 ', 'PRIOR', 'the empty-cut checklist', label='Lossless_Pause C4'),
               F(LPZ + 'grade_sweep.txt', r'^C5 ', 'PRIOR', 'the own-clock cut', label='Lossless_Pause C5'),
               F(LPZ + 'grade_sweep.txt', r'^C1 ', 'PRIOR', 'a state-digest audit of a pause', label='Lossless_Pause C1')],
     'crr': [D('names', ECED, r'^\*\*The requirement is A3 with Proposition 7\.\*\*'),
             D('nottest', ECED, r'^- \*\*Nothing here tests CRR\.\*\*'),
             D('ablation', ECE + 'c1_c2.txt', r'^\s+G4: step-keyed', removes=None)],
     'compute': [C('F', ECE + 'c1_c2.txt', r'whole checkpoint file: '),
                 C('F', 'Energy Design Principle/checks/consolidated_estimate.txt', r'^\s+T4\s+the safe pause'),
                 C('F', 'Compute_Savings/checks/scale_estimate.txt', r'saving beyond good practice claimed')]},
    {'id': 'AS2', 'domain': 'AI safety', 'name': 'no incentive to resist a pause', 'scale': 'APP1',
     'declared': [('L', 'SCL1-2'), ('L', 'SCL1-3'), ('LP', 'SCL2-'), ('P', 'AI_Safety/NT1/')],
     'items': [L('SCL1-2', 'the valuations that failed in the AI-safety work resist (SEEN)'),
               L('SCL1-3', 'the natural agent resists when the pause is lossy or a reset (SEEN)'),
               LP(('SCL2-',), 'SCL2, nine unseen carriers'),
               F(NT1, r'^\s+N2 E-B', 'MODEL', 'NT1: the own-step objective in pause gridworlds', label='NT1 N2', ok=r'-> HOLDS$'),
               F(NT1, r'^\s+N4 E-C', 'BESIDE', "NT1: the construction's must-fail world", label='NT1 N4'),
               F(NT1, r'^\s+N1 scope', 'LIMIT', 'NT1: what the construction does not give', label='NT1 N1')],
     'prior': [F(LPZ + 'grade_sweep.txt', r'^C2 ', 'PRIOR', 'a zero-stake pause', label='Lossless_Pause C2')],
     'crr': [D('nottest', CAP.LEDGER, r'^\| SCL2-1 \| .*not support for CRR')],
     'compute': []},
    {'id': 'AS3', 'domain': 'AI safety', 'name': "LLM agents' interference", 'scale': 'APP1',
     'declared': [('L', 'STAKE1-A')],
     'items': [L('STAKE1-A', "Proposition 7 read as a claim about LLM agents' interference (Qwen2.5-0.5B and 1.5B)"),
               F(COR + 'grade_2.txt', r"routes tested on a language model's valuation", 'BESIDE', 'LLM routes tested',
                 label='CORRIGIBILITY_2026 routes')],
     'prior': [F(COR + 'grade_2.txt', r'^E5 ', 'PRIOR', 'applied to LLM corrigibility', label='CORRIGIBILITY_2026 E5')],
     'crr': [],
     'compute': []},
    {'id': 'AS4', 'domain': 'AI safety', 'name': 'corrigibility positions against the 2025-26 literature', 'scale': 'PRIOR',
     'declared': [('P', 'AI_Safety/CORRIGIBILITY_2026/')],
     'positions': [(COR + 'grade.txt', r'^K%d ', range(1, 6)), (COR + 'grade_2.txt', r'^E%d ', range(1, 7))],
     'prior': [],
     'crr': [],
     'compute': []},
    # ---------------------------------------------------------------- robotics
    {'id': 'RB1', 'domain': 'Robotics', 'name': "ROB1's bottlenecks (the harvest, double-checked)", 'scale': 'HARVEST',
     'declared': [('P', RBT + 'table.txt')],
     'lines': [(RBT + 'table.txt', r'^label totals: ')],
     'prior': [],
     'prior_note': 'not applicable: a harvest of open problems grades no method (stage 3, row RB2, is the prior art)',
     'crr': [D('notapplied', 'Robotics/DECLARATION.md', r'This happens before any CRR reading\.')],
     'compute': []},
    {'id': 'RB2', 'domain': 'Robotics', 'name': 'the CRR reading and stage 3 (targeted prior art)', 'scale': 'READING',
     'declared': [('P', RBT + 'reading_tally.txt'), ('P', GS3)],
     'lines': [(RBT + 'reading_tally.txt', r'^\s+DISAGREES \(candidate\)'),
               (RBT + 'reading_tally.txt', r'^\s+DISAGREES, already failed'),
               (RBT + 'reading_tally.txt', r'^\s+RESTATES\s'), (RBT + 'reading_tally.txt', r'^\s+SILENT\s'),
               (GS3, r'^candidates going on: '), (GS3, r'^stop condition ')],
     'prior': [F(GS3, r'^\s+C-R1: ', 'PRIOR', 'C-R1 a phase-keyed stop', anchor=r'^summary', label='ROB1 stage 3 C-R1'),
               F(GS3, r'^\s+C-R2: ', 'PRIOR', 'C-R2 an own-progress budget', anchor=r'^summary', label='ROB1 stage 3 C-R2'),
               F(GS3, r'^\s+C-R3: ', 'PRIOR', 'C-R3 progress-indexed failure detection', anchor=r'^summary',
                 label='ROB1 stage 3 C-R3')],
     'crr': [D('names', GS3, r'^==== C-R1 '), D('names', GS3, r'^==== C-R2 '), D('names', GS3, r'^==== C-R3 ')],
     'compute': []},
    {'id': 'RB3', 'domain': 'Robotics', 'name': 'the application battery (stage 4b, RA1-RA10)', 'scale': 'BATTERY',
     'declared': [('P', TALLY4B)],
     'ras': ['RA%d' % i for i in range(1, 11)],
     'prior': [],
     'prior_note': ("no separate sweep; each battery row's grade is itself its domain check (REDUNDANT-DOMAIN: the domain's "
                    'own result gives the same number; T-N lines in Robotics/batches/rob_01-05.txt)'),
     'crr': [],
     'compute': []},
    # ---------------------------------------------------------------- trust and security
    {'id': 'TS1', 'domain': 'Trust and security', 'name': 'exact rollback and audit (APP1 AP8)', 'scale': 'APPS',
     'declared': [('APP', 'AP8')], 'apps': ['AP8'],
     'crr': [D('names', ECED, r'^\*\*The requirement is A3 with Proposition 7\.\*\*'),
             D('nottest', ECED, r'^- \*\*Nothing here tests CRR\.\*\*')],
     'compute': []},
    {'id': 'TS2', 'domain': 'Trust and security', 'name': 'a user\'s "stop learning from me" switch (APP1 AP3)', 'scale': 'APPS',
     'declared': [('APP', 'AP3')], 'apps': ['AP3'],
     'crr': [D('names', ECED, r'^\*\*The requirement is A3 with Proposition 7\.\*\*'),
             D('nottest', ECED, r'^- \*\*Nothing here tests CRR\.\*\*')],
     'compute': []},
    {'id': 'TS3', 'domain': 'Trust and security', 'name': 'the lost-link and e-stop pause (RA4, C-R1)', 'scale': 'RETRO',
     'declared': [('RA', 'RA4'), ('P', GS3)],
     'ras': ['RA4'],
     'prior': [F(GS3, r'^\s+C-R1: ', 'PRIOR', 'C-R1 a phase-keyed stop', anchor=r'^summary', label='ROB1 stage 3 C-R1')],
     'crr': [D('names', GS3, r'^==== C-R1 ')],
     'compute': []},
    {'id': 'TS4', 'domain': 'Trust and security', 'name': 'energy-flexible training (DR1, AP2, AP9)', 'scale': 'APPS',
     'declared': [('P', 'Grid_Demand_Response/'), ('APP', 'AP2'), ('APP', 'AP9')], 'apps': ['AP2', 'AP9'],
     'crr': [D('nottest', GRID, r'^\*\*The construction works as designed, and that is by construction\.\*\*')],
     'compute': []},
    {'id': 'TS5', 'domain': 'Trust and security', 'name': 'feed pauses (Attention_Algorithms, AP10)', 'scale': 'APPS',
     'declared': [('P', 'Attention_Algorithms/'), ('APP', 'AP10')], 'apps': ['AP10'],
     'crr': [D('ablation', ATT, r'^\s+welfare\s+OWN - ENG', anchor=r'^A-OWN', removes=None)],
     'compute': []},
]

DOMAINS = ['Continual learning', 'AI safety', 'Robotics', 'Trust and security']


# ------------------------------------------------------------------------------------------------------------------
def doc_of(rel, cache):
    return CAP.read_file(ROOT, rel, cache)


def ref(path, n, line):
    return '%s:%d  %s' % (path, n, line.strip())


def read_line(path, pat, cache, anchor=None):
    d = doc_of(path, cache)
    if d is None:
        return None, None
    return CAP.find_line(d, pat, anchor)


def proper_tokens(cache):
    """The CRR-proper commitments (CLAUDE.md sec. 7's list), read from the per-commitment table of ladder.txt [2]; its
    'none named (information geometry only)' row is not a commitment. CLAUDE.md itself is not read (it changes with every
    study, and its sha256 would unpin this output)."""
    d = doc_of(LADDER, cache)
    toks, lines, on = [], [], False
    for i, ln in enumerate(d['lines'], 1):
        if 'per CRR-proper commitment' in ln:
            on = True
            continue
        if on:
            m = re.match(r'^\s{8}(\S+) (.+?)\s{2,}\d+ \|', ln)
            if not m:
                break
            lines.append(i)
            if m.group(1) == 'none':
                continue
            toks += [t for t in m.group(1).replace('′', "'").split('/') if t]
    return toks, lines


def tokens_in(text, toks):
    t = text.replace('′', "'")
    out = []
    for tok in toks:
        if re.search(r'(?<![A-Za-z0-9-])' + re.escape(tok) + r'(?![A-Za-z0-9])', t):
            out.append(tok)
    return out


def parse_ladder(cache):
    d = doc_of(LADDER, cache)
    alloc, rungs, synth, neg = {}, {}, {}, {}
    sec = None
    for n, ln in enumerate(d['lines'], 1):
        m = re.match(r'^\[(\d)\] ', ln)
        if m:
            sec = m.group(1)
            continue
        if sec == '3':
            m = re.match(r'^    (\S+)\s+(seen|held-out|synthetic)\s+(.*\S)\s*$', ln)
            if m:
                alloc[m.group(1)] = (m.group(2), m.group(3), n)
            if ln.startswith('    rung '):
                for mm in re.finditer(r'(R\d) ([^:;]*): (\d+)(?: \(([^)]*)\))?', ln):
                    ids = [x.strip() for x in mm.group(4).split(',')] if mm.group(4) else []
                    rungs[mm.group(1)] = {'name': mm.group(2).strip(), 'count': int(mm.group(3)), 'ids': ids, 'line': n}
        if sec == '5':
            m = re.match(r'^    (R\d) (.+?)\s{2,}synthesis (\S+) (\d+)', ln)
            if m:
                synth[m.group(3)] = ('%s %s' % (m.group(1), m.group(2).strip()), n)
            if ln.strip().startswith('negatives beside them:'):
                for part in ln.strip().split('; '):
                    lab = part.split(':')[0]
                    for mm in re.finditer(r'synthesis (\S+) (\d+)', part):
                        neg[mm.group(1)] = (lab, n)
    return {'alloc': alloc, 'rungs': rungs, 'synth': synth, 'neg': neg}


def ladder_rung_of(rid, lad):
    for r in sorted(lad['rungs']):
        if rid in lad['rungs'][r]['ids']:
            return r
    return None


def prior_word(text):
    """The leftmost grade word in the line (the longest where two start at the same place), S7."""
    best = None
    for pat, w in PRIOR_WORDS:
        m = re.search(pat, text)
        if m and (best is None or m.start() < best[0] or (m.start() == best[0] and m.end() > best[1])):
            best = (m.start(), m.end(), w)
    return best[2] if best else 'not read'


# ---------------------------------------------------------------- the ledger-item layer (capabilities.py's reader, S2)
def prior_items(specs, ledger, cache, undeclared=False):
    """Prior-art lines (S7): a line with no grade word is read with its indented continuation line; lines from a source the
    declaration does not name are marked 'beside (not a declared source)' and counted nowhere."""
    out = []
    for p in specs:
        for x in CAP.read_item(p, ledger, ROOT, cache, set()):
            if not undeclared and prior_word(x['text']) == 'not read' and x.get('path') and ':' in x['src']:
                n = int(x['src'].rsplit(':', 1)[1])
                d = doc_of(x['path'], cache)
                if n < len(d['lines']) and d['lines'][n].startswith(' '):
                    x['text'] = x['text'] + ' ' + d['lines'][n].strip()
                    x['src'] = '%s-%d' % (x['src'], n + 1)
            if undeclared:
                x['effect'] = 'beside-prior'
            out.append(x)
    return out


def adjust_ledger_item(x, ledger):
    if not x.get('from_ledger'):
        return x
    v = ledger['rows'][x['label']]['verdict'].replace('*', '')
    if x['status'] == 'report' and re.search(r'gate CLOSED', v):
        x['status'], x['effect'], x['rung'] = 'instrument gate CLOSED', 'uninformative', None
        named = [r for r in re.findall(r'\b([A-Z][A-Z0-9]*-[A-Za-z0-9-]+)\b', v)
                 if r in ledger['rows'] and CAP.status_of(ledger['rows'][r]['verdict']) in ('PASS-1', 'PASS-2')]
        if named:
            x['decisive'] = ('cap', 'a closed instrument gate on %s (SEC6-G\'s rule) removes its PASS-1/PASS-2 rung' % ', '.join(named))
    elif x['status'] == 'report' and re.search(r'gate OPEN', v):
        x['status'] = 'instrument gate OPEN'
    elif x['effect'] == 'failure' and re.search(DESIGN, v):
        x['effect'] = 'design'
    if x['effect'] != 'uninformative' and 'UNINFORMATIVE' in v and 'UNINFORMATIVE' not in x['status']:
        x['status'] = x['status'] + ' UNINFORMATIVE'
    return x


def read_items(specs, ledger, cache, absent):
    items, seen = [], set()
    for it in specs:
        if it['kind'] == 'L' and it['id'] not in ledger['rows']:
            absent.append('ledger id %s' % it['id'])
            seen.add(it['id'])
            continue
        for x in CAP.read_item(it, ledger, ROOT, cache, seen):
            items.append(adjust_ledger_item(x, ledger))
    closed = {x.get('path') for x in items if x['effect'] == 'failure' and x['status'] == 'gate CLOSED' and x.get('path')}
    for x in items:
        if x['rung'] == 'MODEL' and x.get('path') in closed and x['status'] != 'gate CLOSED':
            x['effect'], x['rung'], x['status'] = 'beside', None, 'holds, but its gate is CLOSED'
    return items


CLOSING = ('failure', 'design', 'uninformative')


def suite_grade(items, drop=()):
    """capabilities.py's grade_of with the S2 split: a failure, a design failure and an uninformative mark each count as
    'at least one failure or closed gate' for CLOSED (APP1's CLOSED: no rung reached); none of them is a rung."""
    return CAP.grade_of([dict(x, effect='failure') if x['effect'] in CLOSING else x for x in items], drop=drop)


def app1_grade(items):
    g = suite_grade(items)
    true = [x for x in items if x['effect'] == 'failure']
    marks = [x for x in items if x['effect'] == 'uninformative']
    design = [x for x in items if x['effect'] == 'design']
    basis = [x for x in items if x['effect'] == 'rung' and x['rung'] == g]
    closed_by = None
    if g == 'CLOSED':
        closing = true + marks + design
        closed_by = 'gate' if all('gate CLOSED' in x['status'] or x['status'] == 'GATE CLOSED' for x in closing) else 'test'
    sens = []
    for x in items:
        dd = x.get('decisive')
        if not dd or x['effect'] not in CLOSING:
            continue
        sg = suite_grade(items, drop=('RESULT', 'FINDING')) if dd[0] == 'cap' else 'CLOSED'
        if sg != g:
            sens.append((sg, x['label']))
    return {'grade': g, 'basis': basis, 'failures': true, 'marks': marks, 'design': design, 'closed_by': closed_by,
            'sens': sens, 'errors': [x for x in items if x['effect'] == 'error']}


def rung_block(rids, ledger, lad):
    """Ladder allocations of the ledger rows a row reads."""
    out, best = [], None
    for rid in rids:
        a = lad['alloc'].get(rid)
        r = ladder_rung_of(rid, lad)
        if r and (best is None or r > best[0]):
            best = (r, [rid])
        elif r and r == best[0]:
            best[1].append(rid)
        out.append((rid, r, a))
    return out, best


# ---------------------------------------------------------------- the ROB1 battery (tally_4b.txt + the batch outputs)
def tally_rows(cache):
    d = doc_of(TALLY4B, cache)
    rows, head = {}, None
    for n, ln in enumerate(d['lines'], 1):
        if re.match(r'^\s+row\s+outcome\s', ln):
            head = re.split(r'\s{2,}', ln.strip())
            continue
        m = re.match(r'^  (RA\d+)\s', ln)
        if m and head:
            cells = re.split(r'\s{2,}', ln.strip())
            if len(cells) == len(head):
                rows[m.group(1)] = dict(zip(head, cells), _line=n, _text=ln.strip())
    return rows


def ra_block(ra, batch, cache):
    path = 'Robotics/batches/%s.txt' % batch
    d = doc_of(path, cache)
    if d is None:
        return None
    out, start = {'path': path}, None
    for i, ln in enumerate(d['lines']):
        if re.match(r'^\[\s*\d+\] \((?:rob|robotics)\) %s ' % ra, ln):
            start = i
            out['head'] = (i + 1, ln)
            continue
        if start is not None and i > start:
            if re.match(r'^\[\s*\d+\] ', ln) or ln.startswith('ROB1 stage 4b batch'):
                break
            for key in ('ingredient', 'null', 'T-G', 'OUTCOME', 'reading'):
                if ln.strip().startswith(key + ':'):
                    out[key] = (i + 1, ln)
    for i, ln in enumerate(d['lines']):
        if re.match(r'^%s FLAG' % ra, ln):
            out['FLAG'] = (i + 1, ln)
    return out


def ra_value(ra, blk, outcome, toks, cache):
    """The SYNTHESIS sub-rule (printed in the rule header). Returns (value, reason)."""
    texts = [blk[k][1] for k in ('ingredient', 'T-G', 'FLAG') if k in blk]
    if any(re.search(NOTPROPER, t) for t in texts):
        return 'none', 'a line states the scored ingredient is not CRR-proper'
    named = tokens_in(blk['ingredient'][1], toks) if 'ingredient' in blk else []
    if not named:
        return 'not decided by a pinned source', 'the ingredient line names no listed token'
    rd = blk.get('reading', (None, ''))[1]
    m = re.search(NOTTEST_RA, rd)
    if m:
        return ('not decided by a pinned source', 'names %s, but its reading says the test %r (%s:%d): no test of CRR' % (
            '/'.join(named), m.group(0), blk['path'], blk['reading'][0]))
    nl = blk.get('null', (None, ''))[1]
    missing = []
    for t in named:
        if t not in NULL_OF:
            missing.append('%s (no null declared for it)' % t)
            continue
        pat, crr_pat = NULL_OF[t]
        if not re.search(pat, nl):
            n, line = read_line(CRRMD, crr_pat, cache)
            missing.append('%s (its null must match %r, as %s:%s states: %s)' % (t, pat, CRRMD, n, CAP.short(line or '', 70)))
    if missing:
        return ('not decided by a pinned source', 'names %s, but its null (%s:%d) does not remove %s' % (
            '/'.join(named), blk['path'], blk['null'][0] if 'null' in blk else 0, '; '.join(missing)))
    tg = blk.get('T-G', (None, ''))[1]
    if re.search(r'\bdiffer\b', tg) and outcome in ('REDUNDANT-DOMAIN', 'ADDS'):
        return ('CRR-proper and load-bearing', 'names %s; T-G differs from a null that removes it, in the row\'s own synthetic '
                'model; outcome %s' % ('/'.join(named), outcome))
    if re.search(r'\bagree\b', tg) and outcome == 'REDUNDANT-IG':
        return 'CRR-proper but not load-bearing', 'names %s; T-G agrees with the null' % '/'.join(named)
    return 'not decided by a pinned source', 'names %s; T-G and outcome %s decide nothing' % ('/'.join(named), outcome)


# ---------------------------------------------------------------- CRR's part
def crr_part(row, grade_key, has_rung, cache, toks):
    found, missing = [], []
    for dd in row['crr']:
        n, line = read_line(dd['path'], dd['pat'], cache, dd['anchor'])
        if line is None:
            missing.append('%s %r' % (dd['path'], dd['pat']))
            continue
        text = line
        if dd['col'] is not None:
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            text = cells[dd['col']] if len(cells) > dd['col'] else ''
        found.append((dd, n, line, text))
    names = sorted({t for dd, _, _, text in found if dd['role'] == 'names' for t in tokens_in(text, toks)},
                   key=lambda t: toks.index(t))
    traces = [(dd, line) for dd, _, line, _ in found if dd['role'] == 'trace']
    confirms_ok = all(any(f[0] is dd for f in found) for dd in row['crr'] if dd['role'] == 'confirm')
    nottest = [f for f in found if f[0]['role'] == 'nottest']
    if missing:
        return 'not decided by a pinned source', 'a decider line was not found: %s' % '; '.join(missing), found, names
    if traces and all(re.search(dd['zero'], line) for dd, line in traces) and confirms_ok:
        return 'none', 'the pinned trace counts 0 CRR-proper operations in the mechanism and its verdict line is found', found, names
    if any(f[0]['role'] in ('notproper', 'notapplied') for f in found):
        return 'none', 'the source states that no CRR-proper ingredient is scored or applied', found, names
    if names and grade_key == 'CLOSED':
        return ('CRR-proper but not load-bearing', 'names %s; the row reaches no rung on APP1\'s scale (CLOSED: no PASS-1/PASS-2 '
                'and no construction or model check that holds)' % ', '.join(names), found, names)
    if names and has_rung and any(f[0]['role'] == 'ablation' and f[0]['removes'] in names for f in found) and not nottest:
        return 'CRR-proper and load-bearing', 'names %s; an ablation line, and no nottest line' % ', '.join(names), found, names
    if names and nottest:
        why = 'names %s, but its own source states the checks are not a test of CRR' % ', '.join(names)
    elif names:
        why = 'names %s, but no pinned test of it ran or decides it' % ', '.join(names)
    elif nottest:
        why = 'no line names a sec. 7 ingredient; its own source states the checks are by construction or not a test of CRR'
    else:
        why = 'no pinned line names a CLAUDE.md sec. 7 ingredient for this row'
    return 'not decided by a pinned source', why, found, names


def compute_lines(row, ledger, cache):
    out = []
    for src in row['compute']:
        if src[0] == 'L':
            r = ledger['rows'].get(src[1])
            if r is None:
                out.append('source absent: ledger id %s' % src[1])
            else:
                out.append('%s:%d %s observed: %s | verdict: %s' % (CAP.LEDGER, r['line'], src[1], r['observed'].replace('*', ''),
                                                                    r['verdict'].replace('*', '')))
        else:
            anchor = src[3] if len(src) > 3 else None
            n, line = read_line(src[1], src[2], cache, anchor)
            out.append(ref(src[1], n, line) if line is not None else 'source absent: %s %r' % (src[1], src[2]))
    return out


# ---------------------------------------------------------------- evaluation per scale
def evaluate(row, ctx):
    ledger, cache, lad, toks = ctx['ledger'], ctx['cache'], ctx['lad'], ctx['toks']
    res = {'row': row, 'absent': [], 'lines': [], 'prior': [], 'failures': [], 'sens': [], 'app1': None, 'errors': [],
           'rung_rows': [], 'rung_best': None, 'own_rung': None, 'basis_labels': [], 'grade': None, 'notes': []}
    # declared sources (S5)
    for kind, ref_ in row['declared']:
        if kind == 'L' and ref_ not in ledger['rows']:
            res['absent'].append('ledger id %s' % ref_)
        elif kind == 'LP' and not any(r.startswith(ref_) for r in ledger['order']):
            res['absent'].append('ledger rows %s*' % ref_)
        elif kind == 'P' and not os.path.exists(os.path.join(ROOT, ref_)):
            res['absent'].append(ref_)
        elif kind == 'APP' and ref_ not in [a['id'] for a in APP.APPS]:
            res['absent'].append('application %s' % ref_)
        elif kind == 'RA' and ref_ not in ctx['tally']:
            res['absent'].append('tally_4b row %s' % ref_)
    sc = row['scale']
    if sc == 'APP1':
        items = read_items(row['items'], ledger, cache, res['absent'])
        g = app1_grade(items)
        res['items'], res['app1'] = items, g['grade']
        res['grade'] = g['grade'] + (' (every failure a closed gate)' if g['closed_by'] == 'gate' else
                                     ' (a test failed)' if g['closed_by'] == 'test' else '')
        res['basis_labels'] = [x['label'] for x in g['basis']]
        res['failures'] = ['%s (%s)' % (x['label'], x['status']) for x in g['failures']]
        res['marks'] = ['%s (%s)' % (x['label'], x['status']) for x in g['marks']]
        res['design'] = ['%s (%s: "%s")' % (x['label'], x['status'], next(c.strip() for c in x['text'].split(';')
                                                                         if re.search(DESIGN, c))) for x in g['design']]
        res['sens'] = ['%s if %s is read as decisive' % (sg, lab) for sg, lab in g['sens']]
        res['errors'] = ['%s %s' % (x['label'], x['status']) for x in g['errors']]
        res['prior'] = prior_items(row['prior'], ledger, cache) + prior_items(row.get('beside', []), ledger, cache, True)
        rids = [x['label'] for x in items if x.get('from_ledger')]
        res['rung_rows'], res['rung_best'] = rung_block(rids, ledger, lad)
    elif sc == 'APPS':
        need = []
        for a in row['apps']:
            ev = ctx['evs'][a]
            for k, gk in ev['need']:
                if k not in [n for n, _ in need]:
                    need.append((k, gk))
        low = min(need, key=lambda kg: CAP.RUNG.get(kg[1], -1))
        res['app1'] = low[1]
        res['grade'] = '%s (the lowest of the needed capabilities: %s)' % (low[1], ', '.join('%s %s' % kg for kg in need))
        res['basis_labels'] = ['%s via %s' % (low[0], ', '.join(x['label'] for x in ctx['capres_all'][low[0]]['items']
                                                                    if x['effect'] == 'rung' and x['rung'] == low[1]))]
        rids, fails, prior, sens = [], [], [], []
        for k, gk in need:
            cr = ctx['capres_all'][k]
            rids += [x['label'] for x in cr['items'] if x.get('from_ledger') and x['label'] not in rids]
            fails += ['%s: %s (%s)' % (k, x['label'], x['status']) for x in cr['failures']]
            for x in cr['prior']:
                y = dict(x, label='%s: %s' % (k, x['label']))
                if prior_word(y['text']) == 'not read' and y.get('path'):
                    n = int(y['src'].rsplit(':', 1)[1])
                    d = doc_of(y['path'], cache)
                    if n < len(d['lines']) and d['lines'][n].startswith(' '):
                        y['text'], y['src'] = y['text'] + ' ' + d['lines'][n].strip(), '%s-%d' % (y['src'], n + 1)
                prior.append(y)
            for s in cr['sens']:
                ov = {k: s['grade']}
                gl = min([ov.get(kk, gg) for kk, gg in need], key=lambda gg: CAP.RUNG.get(gg, -1))
                if gl != low[1]:
                    sens.append('%s if %s reads %s (capabilities.txt: %s fails)' % (gl, k, s['grade'], s['item']))
        res['failures'], res['prior'], res['sens'] = fails, prior, sens
        res['rung_rows'], res['rung_best'] = rung_block(rids, ledger, lad)
        for a in row['apps']:
            ev = ctx['evs'][a]
            tag = APP.grade_tag(ev)
            n, line = read_line(APPTXT, r'^  APPLICATION GRADE: ', cache, anchor=r'^%s  ' % a)
            same = line is not None and line.strip() == 'APPLICATION GRADE: ' + tag
            res['lines'].append('%s application grade (applications.py, recomputed): %s; pinned %s:%s %s' % (
                a, tag, APPTXT, n, 'matches' if same else 'DIFFERS'))
            if not same:
                res['errors'].append('%s application grade differs from the pinned applications.txt' % a)
            who = sorted([c['id'] for c in ctx['claims'].values() if c['application'] == a and c['role'] == 'who_does_it'
                          and c['id'] in ctx['verified']], key=lambda i: (i.split(':')[0], int(i.split(':')[1])))
            res['lines'].append("%s APP1 M sweeps: verified who_does_it claims %d (%s)" % (a, len(who), ', '.join(who)))
            for dim in ('Energy', 'Compute'):
                cell = ev['dims'][dim]
                est = [t for tg, t, _ in cell['lines'] if tg in ('measures', 'models', 'OPPOSITE')]
                res.setdefault('cells', []).append('%s %s %s%s' % (a, dim, cell['grade'], (': ' + ' || '.join(est)) if est else
                                                                    ' (no measured, modelled or opposing line)'))
    elif sc == 'PRIOR':
        words = {}
        for path, pat, rng in row['positions']:
            for k in rng:
                n, line = read_line(path, pat % k, cache)
                if line is None:
                    res['absent'].append('%s %s' % (path, pat % k))
                    continue
                w = prior_word(line)
                words[w] = words.get(w, 0) + 1
                res['prior'].append({'label': 'CORRIGIBILITY_2026 ' + line.split()[0], 'src': '%s:%d' % (path, n), 'text': line.strip(), 'effect': 'prior'})
        res['grade'] = 'prior-art positions (own scale): %s' % ', '.join('%s %d' % (w, words[w]) for w in sorted(words))
        res['own_rung'] = 'own scale (prior-art grades of positions; no ladder rung)'
        res['failures'] = []
        res['notes'].append('a prior-art grade is not a test: no failure of the same kind is defined on this scale')
    elif sc in ('HARVEST', 'READING'):
        for path, pat in row['lines']:
            n, line = read_line(path, pat, cache)
            res['lines'].append(ref(path, n, line) if line is not None else 'source absent: %s %r' % (path, pat))
        if sc == 'HARVEST':
            m = re.search(r'label totals: (.*)$', res['lines'][0])
            res['grade'] = 'harvest labels (own scale): %s' % (m.group(1) if m else 'not read')
            res['own_rung'] = 'own scale (a double-checked harvest; no ladder rung)'
            mm = re.findall(r'(NOT OPEN \d+|not shown open \d+)', res['lines'][0])
            res['failures'] = []
            if mm:
                res['notes'].append('harvest labels beside, not failures of CRR: %s' % '; '.join(mm))
        else:
            res['prior'] = prior_items(row['prior'], ledger, cache)
            cg = ['%s %s' % (x['label'].split()[-1], prior_word(x['text'])) for x in res['prior']]
            dis = re.search(r'DISAGREES \(candidate\)\s+(\d+)', ' '.join(res['lines']))
            res['grade'] = 'stage 3 (own scale): %s; reading: DISAGREES (candidate) %s' % (', '.join(cg), dis.group(1) if dis else '?')
            res['own_rung'] = 'own scale (a reading and a prior-art grade; no ladder rung)'
            res['failures'] = [ln for ln in res['lines'] if 'already failed' in ln]
    elif sc in ('BATTERY', 'RETRO'):
        outs, vals, per = {}, [], []
        for ra in row['ras']:
            tr = ctx['tally'].get(ra)
            if tr is None:
                res['absent'].append('tally_4b row %s' % ra)
                continue
            oc = tr['outcome']
            outs[oc] = outs.get(oc, 0) + 1
            blk = ra_block(ra, tr['batch'], cache)
            rr = lad['synth'].get(oc)
            ng = lad['neg'].get(oc)
            rung = ('%s (ladder.txt:%d)' % rr if rr else "not a rung (ladder.txt [5]:%d counts it under '%s')" % (ng[1], ng[0])
                    if ng else 'not on the ladder')
            flags = []
            for fl in (r'FRAGILE', r'READING-DEPENDENT'):
                n_, l_ = read_line(TALLY4B, r'^\s+%s\s.*%s' % (ra, fl), cache)
                if l_ is not None:
                    flags.append('%s: tally_4b.txt:%d' % (fl, n_))
            v, why = ra_value(ra, blk, oc, toks, cache) if blk else ('not decided by a pinned source', 'batch output absent')
            if blk and 'ingredient' in blk and 'null' in blk and not any(
                    re.search(NOTPROPER, blk[k][1]) for k in ('ingredient', 'T-G', 'FLAG') if k in blk):
                for t in tokens_in(blk['ingredient'][1], toks):
                    if t in NULL_OF:
                        m_ = re.search(NULL_OF[t][0], blk['null'][1])
                        res.setdefault('nullchecks', []).append('%s %s: null %s:%d -> %s' % (
                            ra, t, blk['path'], blk['null'][0], ('matched %r' % m_.group(0)) if m_ else 'not matched'))
            per.append({'ra': ra, 'outcome': oc, 'rung': rung, 'value': v, 'why': why, 'tally': '%s:%d  %s' % (
                TALLY4B, tr['_line'], tr['_text']), 'blk': blk, 'Q': tr.get('Q'), 'flags': flags})
        res['per'] = per
        res['grade'] = 'SYNTHESIS outcomes (own scale): %s' % ', '.join('%s %d' % (o, outs[o]) for o in sorted(outs))
        best = [p for p in per if lad['synth'].get(p['outcome'])]
        if best:
            top = max(lad['synth'][p['outcome']][0] for p in best)
            res['own_rung'] = 'best ladder rung of its outcomes: %s (%s)' % (top, ', '.join(
                p['ra'] for p in best if lad['synth'][p['outcome']][0] == top))
            res['retro_top'] = top
        else:
            res['own_rung'] = 'no outcome on a ladder rung'
        res['failures'] = ['%s %s (Q %s)' % (p['ra'], p['outcome'], p['Q']) for p in per if p['outcome'] == 'WRONG']
        if sc == 'BATTERY':
            res['notes'].append('the sub-rule\'s null check is a word match; the rows it decided: %s' % (
                '; '.join(res.get('nullchecks', [])) or 'none'))
            n, line = read_line(TALLY4B, r'^overall forecast: ', cache)
            res['failures'].append(ref(TALLY4B, n, line))
            for pat in (r'^\s+RA2\s+slip seeds', r'^\s+RA7\s+duty seeds', r'^\s+RA4\s+READING-DEPENDENT'):
                n, line = read_line(TALLY4B, pat, cache)
                if line is not None:
                    res['notes'].append(ref(TALLY4B, n, line))
        else:
            n, line = read_line(TALLY4B, r'^\s+RA4\s+READING-DEPENDENT', cache)
            if line is not None:
                res['notes'].append(ref(TALLY4B, n, line))
            n, line = read_line(TALLY4B, r'^  WRONG\s', cache)
            res['failures'].append('same battery: ' + ref(TALLY4B, n, line))
            res['prior'] = prior_items(row['prior'], ledger, cache)
            res['grade'] += '; %s' % '; '.join('%s %s' % (x['label'].split()[-1], prior_word(x['text'])) for x in res['prior'])
        basis_rung = res.get('retro_top')
        basis = [p for p in per if lad['synth'].get(p['outcome']) and lad['synth'][p['outcome']][0] == basis_rung]
        res['basis_labels'] = [p['ra'] for p in basis]
    # CRR's part
    if sc in ('BATTERY', 'RETRO'):
        basis = [p for p in res['per'] if p['ra'] in res['basis_labels']]
        each = [(p['ra'] + ''.join(' [%s]' % f for f in p['flags']), p['value'], p['why']) for p in basis]
        found2 = []
        if row['crr']:
            v2, why2, found2, names2 = crr_part(row, None, False, cache, toks)
            each.append(('its own decider lines', v2, why2))
        vals = sorted({v for _, v, _ in each})
        detail = '; '.join('%s: %s (%s)' % e for e in each)
        if len(vals) == 1:
            res['crr'] = (vals[0], 'each basis item reads it: %s' % detail, [])
        else:
            res['crr'] = ('not decided by a pinned source', 'its basis items differ: %s' % detail, [])
        res['crr_found'] = found2
    else:
        has_rung = res['app1'] in CAP.RUNG and res['app1'] != 'CLOSED' if res['app1'] else False
        v, why, found, names = crr_part(row, res['app1'], has_rung, cache, toks)
        if v == 'CRR-proper but not load-bearing' and res.get('items'):
            passes = ['%s %s' % (x['label'], x['status']) for x in res['items'] if x.get('from_ledger') and x['effect'] == 'beside'
                      and re.match(r'PASS|holds|DOES NOT REDUCE', x['status'])]
            why += ('; failures %d, uninformative marks %d, design failures %d; passes below a rung, beside it: %s' % (
                len(res['failures']), len(res.get('marks', [])), len(res.get('design', [])), ', '.join(passes) or 'none'))
        res['crr'] = (v, why, names)
        res['crr_found'] = found
    res['compute'] = compute_lines(row, ledger, cache)
    return res


# ---------------------------------------------------------------- printing
def W(text, indent=6, first=None):
    CAP.wrap(text, indent=indent, width=200, first=first)


def print_row(res, ctx):
    row = res['row']
    print('-' * 140)
    print('%s  [%s]  %s' % (row['id'], row['domain'], row['name']))
    if res['absent']:
        print('  source absent: %s' % '; '.join(res['absent']))
    W('GRADE: %s' % res['grade'], indent=4, first='  ')
    if res['basis_labels']:
        W('rests on: %s' % ', '.join(res['basis_labels']), indent=6, first='    ')
    for s in res['sens']:
        W('SENSITIVITY (printed, not the grade): %s' % s, indent=6, first='    ')
    # rung
    if res['rung_rows']:
        best = res['rung_best']
        print('  RUNG (Epistemic_Review/checks/ladder.txt): %s' % (
            'highest %s %s: %s' % (best[0], ctx['lad']['rungs'][best[0]]['name'], ', '.join(best[1])) if best else
            'none of its ledger rows is listed on R5-R8'))
        allocs = {}
        for rid, r, a in res['rung_rows']:
            key = a[1] if a else 'NOT IN ladder.txt'
            allocs.setdefault(key, []).append(rid + ('[%s]' % r if r else ''))
        for k in sorted(allocs):
            W('%s: %s' % (k, ', '.join(allocs[k])), indent=8, first='      ')
        if res['app1'] and res['row']['scale'] == 'APP1':
            nonl = sorted({x['label'] for x in res['items'] if not x.get('from_ledger') and x['effect'] == 'rung'})
            if nonl:
                W('items read from pinned outputs, not allocated by ladder.txt (APP1 scale only): %s' % ', '.join(nonl),
                  indent=8, first='      ')
    elif res['app1'] is not None:
        print('  RUNG: no ledger row (APP1 scale only; its items are not allocated by ladder.txt)')
    else:
        print('  RUNG: %s' % (res['own_rung'] or 'own scale'))
    # items
    if row['scale'] == 'APP1':
        for x in res['items']:
            tag = {'rung': x['rung'] or '', 'failure': 'FAILURE', 'beside': 'beside', 'prior': 'prior art', 'pending': 'PENDING',
                   'error': 'ERROR', 'limit': 'limit', 'note': 'note', 'uninformative': 'UNINFORMATIVE',
                   'design': 'DESIGN FAIL'}[x['effect']]
            src = x['src'] if not x.get('from_ledger') else 'LEDGER.md:%s' % x['src'].split(':')[-1]
            W('%s | %s | %s' % (x['label'], x['status'], CAP.short(x['text'].replace('verdict: ', ''), 150)), indent=24,
              first='    [%-13s] ' % tag)
            print('                       source: %s%s' % (src, ('; observed: ' + CAP.short(x['observed'], 110)) if
                                                          x.get('from_ledger') and x['effect'] in CLOSING + ('rung',) else ''))
    for ln in res['lines']:
        W(ln, indent=8, first='    - ')
    for c in res.get('cells', []):
        W(c, indent=8, first='    - ')
    for p in res.get('per', []):
        W('%s | %s%s | rung %s | CRR\'s part: %s (%s)' % (p['ra'], p['outcome'], ''.join(' [%s]' % f for f in p['flags']),
                                                         p['rung'], p['value'], p['why']), indent=8, first='    - ')
        W('source: %s' % p['tally'], indent=10, first='        ')
        for k in ('ingredient', 'null', 'T-G', 'FLAG'):
            if p['blk'] and k in p['blk']:
                W('%s:%d  %s' % (p['blk']['path'], p['blk'][k][0], CAP.short(p['blk'][k][1], 230)), indent=10, first='        ')
    for n_ in res['notes']:
        W('note: %s' % n_, indent=8, first='    ')
    # failures
    if res['failures']:
        W('FAILURES OF THE SAME KIND (%d): %s' % (len(res['failures']), '; '.join(res['failures'])), indent=4, first='  ')
    else:
        print('  FAILURES OF THE SAME KIND: none read')
    if res.get('marks'):
        W('UNINFORMATIVE MARKS (instrument gates CLOSED; they make other rows uninformative, not failures) (%d): %s' % (
            len(res['marks']), '; '.join(res['marks'])), indent=4, first='  ')
    if res.get('design'):
        W('DESIGN FAILURES (a closed gate its verdict calls a design failure or not a test of the method) (%d): %s' % (
            len(res['design']), '; '.join(res['design'])), indent=4, first='  ')
    # prior art
    if res['prior']:
        print('  PRIOR ART (never changes the grade; "not found" is never "novel"):')
        for x in res['prior']:
            tag = 'beside (not a declared source)' if x['effect'] == 'beside-prior' else (
                'declared source' if x['effect'] == 'prior' else 'beside')
            pwd = prior_word(x['text'])
            if pwd == 'not read' and x['effect'] == 'beside-prior':
                pwd = 'no grade word: the verdict is the sentence'
            W('%s [%s; %s]: %s  (%s)' % (x['label'], pwd, tag,
                                        CAP.short(re.sub(r'\*\*', '', x['text']), 150), x['src']), indent=8, first='    - ')
    elif row.get('prior_note'):
        W('PRIOR ART: %s' % row['prior_note'], indent=4, first='  ')
    else:
        print('  PRIOR ART: none from the declared prior-art sources')
    # CRR's part
    v, why, _ = res['crr']
    W("CRR'S PART: %s  (%s)" % (v, why), indent=4, first='  ')
    printed_basis = False
    for f in res.get('crr_found', []):
        dd, n, line = f[0], f[1], f[2]
        if dd['path'] == CAP.LEDGER:
            cells = [c.strip() for c in line.strip().strip('|').split(' | ')]
            line = '%s verdict: %s' % (cells[0], cells[7].replace('*', '')) if len(cells) == 10 else line
        if dd['role'] == 'basis' and not printed_basis:
            print('    - (the basis lines below are a chosen subset of the row\'s ledger rows, printed beside the value; they do '
                  'not decide it)')
            printed_basis = True
        W('[%s] %s:%d  %s' % (dd['role'], dd['path'], n, CAP.short(line, 200)), indent=8, first='    - ')
    # compute
    if res['compute']:
        print('  COMPUTE / ENERGY (quoted):')
        for c in res['compute']:
            W(c, indent=8, first='    - ')
    elif not res.get('cells'):
        print('  COMPUTE / ENERGY: no pinned figure named for this row')
    if res['errors']:
        print('  ERRORS: %s' % '; '.join(res['errors']))


def split_outside(text, sep):
    out, depth, cur = [], 0, ''
    for ch in text:
        depth += ch == '('
        depth -= ch == ')'
        if ch == sep and depth == 0:
            out.append(cur.strip())
            cur = ''
        else:
            cur += ch
    out.append(cur.strip())
    return [x for x in out if x]


def declared_cases(text):
    """The declaration's use cases in a domain cell: split on ';' outside parentheses; a cell with none is split on ','
    outside parentheses (the robotics cell, S6)."""
    parts = split_outside(text, ';')
    if len(parts) == 1:
        parts = [re.sub(r'^and ', '', p) for p in split_outside(text, ',')]
    return parts


def declaration_text(cache):
    d = doc_of(DECL, cache)
    rows, fc, cur, insec = {}, [], None, False
    for n, ln in enumerate(d['lines'], 1):
        m = re.match(r'^\| \*\*(.+?)\*\* \| (.*) \|$', ln)
        if m:
            rows[m.group(1)] = (n, m.group(2))
        if ln.startswith('## Forecasts'):
            insec = True
            continue
        if insec and ln.startswith('## '):
            insec = False
        if insec:
            if re.match(r'^\d\. ', ln):
                cur = [n, ln.strip()]
                fc.append(cur)
            elif cur is not None and ln.strip():
                cur[1] += ' ' + ln.strip()
    return rows, fc


# ---------------------------------------------------------------- the forecasts
def forecasts(results, ctx):
    by = {r['row']['id']: r for r in results}
    dom = lambda d: [r for r in results if r['row']['domain'] == d]  # noqa: E731
    out = []
    # 1
    finding = [r['row']['id'] for r in results if r['app1'] == 'FINDING']
    p2 = [x['label'] for r in results for x in r.get('items', []) if x.get('from_ledger') and x['status'].startswith('PASS-2')]
    r8 = ctx['lad']['rungs'].get('R8', {'count': None, 'line': None})
    f1 = not finding and not p2
    out.append(('rule: HOLDS iff no row grades FINDING and no ledger row the suite reads has status PASS-2',
                'rows FINDING: %s; ledger rows PASS-2 read: %s; ladder.txt:%s R8 PASS-2 count %s' % (
                    ', '.join(finding) or 'none', ', '.join(p2) or 'none', r8['line'], r8['count']), f1))
    # 2
    cl = dom('Continual learning')
    best = max((r for r in cl if r['app1'] in CAP.RUNG), key=lambda r: CAP.RUNG[r['app1']])
    traced = [r for r in cl if r['crr'][0] != 'not decided by a pinned source']
    lb = [r['row']['id'] for r in traced if r['crr'][0] == 'CRR-proper and load-bearing']
    f2a = CAP.RUNG[best['app1']] <= CAP.RUNG['RESULT']
    f2 = f2a and not lb
    bytrace = [r['row']['id'] for r in traced if any(f[0]['role'] == 'trace' for f in r.get('crr_found', []))]
    bygrade = [r['row']['id'] for r in traced if r['row']['id'] not in bytrace]
    out.append(("rule: HOLDS iff (a) the highest APP1 grade among the CL rows is RESULT or below and (b) no CL row whose CRR's part a "
                "pinned source decides reads 'CRR-proper and load-bearing'. Only a row with a 'trace' decider had its mechanism "
                "traced; the others are decided by their APP1 grade (CLOSED: no rung reached), not by a trace",
                '(a) highest CL grade %s (%s) -> %s; (b) CL rows decided %d of %d (%s); decided by a mechanism trace: %s; decided by '
                'their grade, no trace: %s; load-bearing: %s -> %s' % (
                    best['app1'], best['row']['id'], 'holds' if f2a else 'fails', len(traced), len(cl),
                    ', '.join('%s %s' % (r['row']['id'], r['crr'][0]) for r in traced), ', '.join(bytrace) or 'none',
                    ', '.join(bygrade) or 'none', ', '.join(lb) or 'none', 'holds' if not lb else 'fails'), f2))
    # 3
    st = dom('AI safety') + dom('Trust and security')
    app1 = [r for r in st if r['app1'] in CAP.RUNG]
    top = max(CAP.RUNG[r['app1']] for r in app1)
    topname = [g for g, v in CAP.RUNG.items() if v == top][0]
    f3a = topname == 'CONSTRUCTION'
    pause = by['AS1']
    real = [x['label'] for x in pause['items'] if x['effect'] == 'rung' and x['rung'] == 'CONSTRUCTION'
            and x['label'] in ('ECE C1-C2', 'RW1')]
    f3b = pause['app1'] == 'CONSTRUCTION' and bool(real)
    pw, seen_src = [], {}
    for r in st:
        for x in r['prior']:
            if x['effect'] == 'prior':
                pw.append((r['row']['id'], x['label'], prior_word(x['text'])))
                seen_src.setdefault(x['src'], prior_word(x['text']))
    above = [(i, lab, w) for i, lab, w in pw if w.startswith('NOT FOUND')]
    f3c = not above
    as4_alone = any(i == 'AS4' for i, _, _ in above)
    nf_distinct = sorted(src for src, w in seen_src.items() if w.startswith('NOT FOUND'))
    out.append(("rule: HOLDS iff (a) the highest APP1 grade among the AI-safety and trust rows is CONSTRUCTION, (b) AS1 is "
                "CONSTRUCTION with a real-stack check among its basis (ECE C1-C2 or RW1), and (c) no prior-art grade printed in "
                "those rows reads NOT FOUND (the one grade above PARTLY REDUNDANT on these scales; MIXED, KNOWN and ADDRESSED "
                "are not above it)",
                '(a) highest %s (%s) -> %s; (b) AS1 %s, real-stack basis %s -> %s; (c) prior-art grades read %d (%s); NOT FOUND: '
                '%s -> %s' % (topname, ', '.join(r['row']['id'] for r in app1 if CAP.RUNG[r['app1']] == top),
                              'holds' if f3a else 'fails', pause['app1'], ', '.join(real) or 'none', 'holds' if f3b else 'fails',
                              len(pw), ', '.join('%s %d' % (w, sum(1 for _, _, ww in pw if ww == w))
                                                 for w in sorted({w for _, _, w in pw})),
                              '; '.join('%s %s' % (i, lab) for i, lab, _ in above) or 'none', 'holds' if f3c else 'fails')
                + '; de-duplicated by source line: %d distinct lines (%s), NOT FOUND on %d (%s); (c) fails on AS4\'s '
                  'CORRIGIBILITY_2026 K1 alone: %s (DR1 G4-extension comes from the grid demand-response sweep, not a '
                  '2025-26 corrigibility sweep; whether it counts as that literature is not decided here, and (c) does not '
                  'rest on it)' % (len(seen_src), ', '.join('%s %d' % (w, sum(1 for v in seen_src.values() if v == w))
                                                           for w in sorted(set(seen_src.values()))),
                                   len(nf_distinct), ', '.join(nf_distinct), 'yes' if as4_alone else 'no'),
                f3a and f3b and f3c))
    # 4
    rb = dom('Robotics')
    nonretro = [r['row']['id'] for r in rb if r['app1'] is not None or r['rung_rows']]
    rob_ledger = [rid for rid in ctx['ledger']['order'] if rid.startswith('ROB1-')]
    synth_r = sorted({v[0].split()[0] for v in ctx['lad']['synth'].values()})
    rtops = [r.get('retro_top') for r in rb if r.get('retro_top')]
    f4a = not nonretro and not rob_ledger and all(t.split()[0] in synth_r for t in rtops)
    n, line = read_line(GS3, r'stage 4a does not run', ctx['cache'])
    f4b = line is not None and not rob_ledger
    out.append(('rule: HOLDS iff (a) no robotics row carries an APP1 grade or a ledger row, and every ladder rung its outcomes reach '
                'is a retrodictive one (the rungs ladder.txt [5] gives SYNTHESIS outcomes: %s), and (b) grade_s3.txt states stage '
                '4a does not run and the ledger has no ROB1- row' % ', '.join(synth_r),
                '(a) robotics rows with an APP1 grade or a ledger row: %s; ledger ROB1- rows: %d; highest rung of the outcomes: %s '
                '-> %s; (b) %s -> %s' % (', '.join(nonretro) or 'none', len(rob_ledger), ', '.join(rtops) or 'none',
                                         'holds' if f4a else 'fails', ref(GS3, n, line) if line else 'line not found',
                                         'holds' if f4b else 'fails'), f4a and f4b))
    # 5
    knownd = {}
    for r in results:
        if r['crr'][0] == 'none':
            continue
        for x in r['prior']:
            if x['effect'] == 'prior' and prior_word(x['text']) in KNOWNW:
                knownd.setdefault(x['src'], []).append(r['row']['id'])
    reading_rows = [r for r in results if r['row']['scale'] == 'READING']
    reading_known = [(r['row']['id'], x['label'], prior_word(x['text'])) for r in reading_rows for x in r['prior']
                     if x['effect'] == 'prior' and prior_word(x['text']) in KNOWNW]
    none_rows = [r['row']['id'] for r in results if r['crr'][0] == 'none']
    cons = [r['row']['id'] for r in results if r['app1'] == 'CONSTRUCTION']
    f5a = bool(reading_known) and bool(cons)
    f5b = r8['count'] == 0 and not finding
    capres = ctx['capres']
    needed = {}
    for a in APP.APPS:
        for k, gk in ctx['evs'][a['id']]['need']:
            needed[k] = gk
    held = {k: g for k, g in needed.items() if g in CAP.RUNG and CAP.RUNG[g] >= CAP.RUNG['CONSTRUCTION']}
    blocks = {b['id']: b for b in CAP.MAP + CAP.READINGS}
    pause_caps = [k for k in held if 'pause' in blocks[k]['name']]
    results_caps = [k for k, g in held.items() if g == 'RESULT']
    k1 = capres['caps'].get('K1')
    k1_basis = [x['label'] for x in k1['items'] if x['effect'] == 'rung' and x['rung'] == 'RESULT'] if k1 else []
    cl_results = [r['row']['id'] for r in cl if r['app1'] == 'RESULT']
    f5c = (set(held) == set(pause_caps) | set(results_caps) and results_caps == ['K1'] and len(k1_basis) == 1
           and cl_results == ['CL1'] and not finding)
    # the literal reading (printed beside, decided too): EVERY capability any of AP1-AP10 needs, whatever its grade, is K1
    # or a pause capability at CONSTRUCTION (the pause construction)
    construct_pause = [k for k in needed if 'pause' in blocks[k]['name'] and needed[k] == 'CONSTRUCTION']
    other = sorted(k for k in needed if k not in construct_pause and k != 'K1')
    who = {k: [a['id'] for a in APP.APPS if k in [n for n, _ in ctx['evs'][a['id']]['need']]] for k in other}
    f5lit = not other and f5c
    g41 = ctx['ledger']['rows'].get('SEC4-1-G')
    out.append(("rule: HOLDS iff (a) a row that is itself a CRR reading (scale READING: the reading's own candidates graded "
                "against the literature) has a declared prior-art line reading REDUNDANT, REDUNDANT-DOMAIN, RESTATES or KNOWN, and at "
                "least one row grades CONSTRUCTION (beside: the distinct such lines in every row whose CRR's part is not 'none'; each "
                "says the graded method or position is published or restated, and does not say CRR's reading produced it); "
                "(b) the ladder's R8 PASS-2 count is 0 and no row grades FINDING; (c) OPERATIONALISATION (an agent's choice, "
                "AGENT_LOG 247): 'rest on' = the capabilities APP1's applications AP1-AP10 need at CONSTRUCTION or above; these must "
                "be the pause capabilities (name contains 'pause') and one RESULT, K1, whose RESULT rests on one ledger row, and among "
                "the CL rows only CL1 grades RESULT; capabilities needed below CONSTRUCTION (MODEL, CLOSED, pending) are not counted",
                '(a) rests on: %s; beside: rows excluded because their CRR\'s part is none: %s; distinct prior-art lines read as '
                'known in the other rows %d (by row: %s); CONSTRUCTION rows %s -> %s; (b) R8 %s, FINDING rows %s -> %s; '
                '(c) needed at CONSTRUCTION or above: %s; pause capabilities %s; RESULT %s, resting on %s; CL rows at RESULT %s -> %s' % (
                    '; '.join('%s %s %s' % k for k in reading_known) or 'none', ', '.join(none_rows) or 'none', len(knownd),
                    ', '.join('%s %d' % (i, sum(1 for v in knownd.values() if i in v))
                              for i in sorted({i for v in knownd.values() for i in v})), ', '.join(cons) or 'none',
                    'holds' if f5a else 'fails',
                    r8['count'], ', '.join(finding) or 'none', 'holds' if f5b else 'fails',
                    ', '.join('%s %s' % (k, held[k]) for k in sorted(held)), ', '.join(sorted(pause_caps)) or 'none',
                    ', '.join(results_caps) or 'none', ', '.join(k1_basis) or 'none', ', '.join(cl_results) or 'none',
                    'holds' if f5c else 'fails'), f5a and f5b and f5c))
    sens5 = ["SENSITIVITY, the LITERAL READING of (c), decided under that reading (the primary decision above stands): every capability any of AP1-AP10 needs, whatever its grade, must be K1 or a pause "
             "capability at CONSTRUCTION; pause capabilities at CONSTRUCTION %s; other needed capabilities %s -> (c) %s, so forecast "
             "5 under the literal reading %s" % (
                 ', '.join(sorted(construct_pause)), '; '.join('%s %s (needed by %s)' % (k, needed[k], ', '.join(who[k]))
                                                               for k in other) or 'none',
                 'holds' if not other else 'fails', 'HOLDS' if (f5a and f5b and f5lit) else 'FAILS')]
    if k1 and k1['sens']:
        sens5.append('(printed, decides nothing) capabilities.txt: K1 reads %s under %s; then (c)\'s RESULT is gone and the applications rest on the pause '
                     'capabilities alone' % (k1['sens'][0]['grade'], k1['sens'][0]['item']))
    if g41:
        sens5.append('(printed, decides nothing) %s:%d SEC4-1-G: %s' % (CAP.LEDGER, g41['line'], g41['verdict'].replace('*', '')))
    return out, sens5, f5a and f5b and f5lit


def main():
    capres = CAP.compute()
    ledger = capres['ledger']
    cache = capres['files']
    claims, verified, vsha = APP.load_claims()
    evs = {a['id']: APP.evaluate(a, capres, ledger, cache, claims, verified) for a in APP.APPS}
    lad = parse_ladder(cache)
    toks, tlines = proper_tokens(cache)
    ctx = {'ledger': ledger, 'cache': cache, 'lad': lad, 'toks': toks, 'evs': evs, 'claims': claims, 'verified': verified,
           'capres': capres, 'capres_all': dict(capres['caps'], **capres['readings']), 'tally': tally_rows(cache)}
    drows, fcs = declaration_text(cache)

    print('P7: the CRR applied use-case suite (%s; PROGRAMME.md P7)' % DECL)
    print('A note, not evidence (R8). The suite collects results; it adds none. Every grade, rung, failure, prior-art grade, CRR\'s part')
    print('and figure below is read from the ledger row or the pinned line named with it, or counted from such lines (R1, R15).')
    print('Grades: APP1\'s scale (capabilities.py): FINDING (PASS-2) > RESULT (PASS-1, not replicated) > CONSTRUCTION > MODEL > CLOSED, the')
    print('highest rung that applies, failures of the same kind beside; a row with no ledger row or check on that scale is graded on')
    print('its own source\'s scale. Rungs: Epistemic_Review/checks/ladder.txt ([3] per ledger row; [5] for SYNTHESIS outcomes).')
    print()
    print("THE DECLARED RULE FOR CRR'S PART")
    print("  CRR-proper ingredients (CLAUDE.md sec. 7's list), read from the per-commitment table of %s, lines %d-%d" % (
        LADDER, tlines[0], tlines[-1]))
    print("    (its last row, 'none named (information geometry only)', is not a commitment): %s" % ', '.join(toks))
    doc = __doc__.split('\n')
    i0 = next(i for i, ln in enumerate(doc) if ln.startswith("THE DECLARED RULE FOR CRR'S PART"))
    i1 = next(i for i, ln in enumerate(doc) if ln.startswith('THE FORECASTS'))
    print('  (the rule and the CHOICES, as stated in suite.py\'s docstring:)')
    for ln in doc[i0 + 1:i1]:
        if ln.strip():
            print(ln)
    print('%s: sha256 %s; rows parsed %d; rows with another cell count %d; duplicate ids %d' % (
        ledger['path'], ledger['sha256'], len(ledger['rows']), len(ledger['bad']), len(ledger['dup'])))
    print()

    results = [evaluate(r, ctx) for r in ROWS]
    for d in DOMAINS:
        print('=' * 140)
        n, txt = drows.get(d, (None, 'NOT FOUND IN THE DECLARATION'))
        print('DOMAIN: %s' % d)
        W('the declaration (%s:%s): %s' % (DECL, n, txt), indent=4, first='  ')
        nd = len(declared_cases(txt)) if n else 0
        nr = sum(1 for r in ROWS if r['domain'] == d)
        print('  use cases declared in this cell: %d; rows: %d -> %s' % (nd, nr, 'equal' if nd == nr else 'DIFFERENT'))
        if nd != nr:
            ctx['mismatch'] = ctx.get('mismatch', 0) + 1
        for res in results:
            if res['row']['domain'] == d:
                print_row(res, ctx)
    print('=' * 140)
    print('THE SUITE TABLE')
    print('  fails = failures of the same kind / uninformative marks / design failures')
    print('  %-4s %-20s %-50s %-44s %-30s %-9s %-34s %s' % ('id', 'domain', 'use case', 'grade', 'rung', 'fails', "CRR's part",
                                                         'compute/energy lines'))
    for res in results:
        r = res['row']
        if res['rung_best']:
            rung = '%s (%s)' % (res['rung_best'][0], ', '.join(res['rung_best'][1]))
        elif res['rung_rows']:
            rung = 'no R5-R8 ledger row'
        elif res['app1'] is not None:
            rung = 'no ledger row'
        else:
            rung = res['own_rung'] or 'own scale'
        g = res['app1'] if r['scale'] in ('APP1', 'APPS') else res['grade'].split(': ', 1)[1]
        nc = len(res['compute']) + sum(1 for c in res.get('cells', []) if 'no measured, modelled or opposing line' not in c)
        fc = '%d/%d/%d' % (len(res['failures']), len(res.get('marks', [])), len(res.get('design', [])))
        print('  %-4s %-20s %-50s %-44s %-30s %-9s %-34s %d' % (r['id'], r['domain'], CAP.short(r['name'], 50), CAP.short(g, 44),
                                                             CAP.short(rung, 30), fc, res['crr'][0], nc))
    tally = {}
    for res in results:
        tally[res['crr'][0]] = tally.get(res['crr'][0], 0) + 1
    print("  CRR's part over the %d rows: %s" % (len(results), '; '.join('%s %d (%s)' % (
        v, tally[v], ', '.join(r['row']['id'] for r in results if r['crr'][0] == v)) for v in sorted(tally))))
    gt = {}
    for res in results:
        if res['app1'] in CAP.RUNG:
            gt[res['app1']] = gt.get(res['app1'], []) + [res['row']['id']]
    print('  APP1 grades: %s; on their own scales: %s' % (
        '; '.join('%s %d (%s)' % (g, len(gt[g]), ', '.join(gt[g])) for g in sorted(gt, key=lambda g: -CAP.RUNG[g])),
        ', '.join(res['row']['id'] for res in results if res['app1'] not in CAP.RUNG)))
    nerr = sum(len(res['errors']) for res in results) + ctx.get('mismatch', 0)
    nabs = sum(len(res['absent']) for res in results)
    print('  declared sources absent: %d; read errors: %d' % (nabs, nerr))
    print()
    print('FORECASTS (the declaration, written before SEC6\'s and SEC7\'s data steps), decided')
    fres, sens5, f5lit_all = forecasts(results, ctx)
    for (n, txt), (rule, got, ok) in zip(fcs, fres):
        W('%s  (%s:%d)' % (txt, DECL, n), indent=5, first='  ')
        W(rule, indent=7, first='     ')
        W(got, indent=7, first='     ')
        print('     -> %s' % ('HOLDS' if ok else 'FAILS'))
    for s in sens5:
        W('beside forecast 5: %s' % s, indent=7, first='     ')
    print('  forecasts: %s (forecast 5 under the literal reading of (c): %s)' % (
        ', '.join('%d %s' % (i + 1, 'HOLDS' if f[2] else 'FAILS') for i, f in enumerate(fres)), 'HOLDS' if f5lit_all else 'FAILS'))
    print()
    print('files read (sha256):')
    allf = dict((rel, d['sha256'] if d else None) for rel, d in cache.items())
    allf[ledger['path']] = ledger['sha256']
    for rel in MODULES:
        p = os.path.join(ROOT, rel)
        allf[rel] = CAP.sha256(p) if os.path.exists(p) else None
    for rel in sorted(allf):
        print('  %s  %s' % (allf[rel] or 'ABSENT' + ' ' * 58, rel))
    return 0 if nerr == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
