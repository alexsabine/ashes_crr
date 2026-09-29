"""Redundant / consistent / descriptive against fails, across the whole record, and a review of PRED70's WRONG rows
(owner request, prompt-log entry 235). Reads only pinned outputs:
  Epistemic_Review/checks/ladder.txt   (the retrodiction batteries' grades, the synthesis bank, the ledger allocations)
  Predictions70/checks/tally.txt       (PRED70 outcomes, Q held/failed, the post hoc amplitude-control column)
Part [2] applies ONE rule, written here before the table was filled: theory/CRR.md section 9 ("Summary of what could
fail"): only H-CUT, H-L5, H-T1 and H-EQ can fail; "Everything else in this document is definition, standard mathematics,
or open." A PRED70 WRONG row is therefore read in one of four classes (the investigator's reading, per row, below):
  FALSIFIES   a section-9 claim, applied inside its stated scope, failed (H-L5 on a carrier with its own events; H-CUT on
              a cyclic carrier with its own events where antipode and trigger differ)
  SCOPE       a section-9 claim failed where CRR itself says it must fail or does not apply (H-T1 on a convex learner:
              its declared must-fail; a cut on a carrier with no rotor: O3)
  APPLICATION an axiom or definition (A3 as a control or timing rule, A6 as a dynamical model) was applied as a domain
              model and the declared consequence failed; section 9 says these cannot falsify CRR, but they bound its reach
  KNOB        the failure rests on a value CRR does not fix (A6's weight q, P3; the occasion length, O1), declared at one
              value by the investigator
The harness rule is also checked: a row is REDUNDANT only if the CRR value agrees with the null (T-G) or the domain
(T-N) within 1 %; a WRONG row can reach WRONG only after both tests read 'differ'.
Run: python3 Epistemic_Review/checks/redundant_vs_fail.py
"""
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
L = open(os.path.join(ROOT, 'Epistemic_Review/checks/ladder.txt')).read()
T = open(os.path.join(ROOT, 'Predictions70/checks/tally.txt')).read()

# PRED70 WRONG rows: class and reason (INVESTIGATOR'S READING, applying section 9, O1, O3 and the SCOPE lemma)
READ = {
    'P02-1': ('FALSIFIES', 'H-L5 on a slider with its own slips: the arc is not more regular than the clock'),
    'P08-4': ('FALSIFIES', 'H-L5 on Red Queen cycles (own turns): clock more regular'),
    'P11-3': ('FALSIFIES', 'H-L5 per breath: breath duration more regular than the arc'),
    'P12-4': ('FALSIFIES', 'H-L5 on glacial terminations: the period is the regular quantity'),
    'P13-2': ('FALSIFIES', 'H-CUT on a relay thermostat (cyclic, own switching events): the switch is not at the antipode'),
    'P11-2': ('FALSIFIES', 'H-CUT on sleep onset (own event on the circadian cycle): onset is not at the antipode'),
    'P05-1': ('SCOPE', 'H-T1 on a convex learner: section 9 names it as H-T1\'s must-fail (SCOPE lemma)'),
    'P12-2': ('SCOPE', 'a cut on the thermohaline carrier, which has no rotor (O3: nothing sets L)'),
    'P05-3': ('APPLICATION', 'A3 used as a restart schedule: CRR does not claim a cut is an optimal control'),
    'P06-5': ('APPLICATION', 'A3 used as a ratchet switching rule: CRR does not claim optimality'),
    'P07-4': ('APPLICATION', 'A3 placed on the PRC crossover, a derived curve, not an own event'),
    'P03-5': ('APPLICATION', 'A6 as a dynamical model: the stabilising direction was the investigator\'s, not CRR\'s'),
    'P10-4': ('APPLICATION', 'A6 as a driver model: the capacity-raising direction was the investigator\'s'),
    'P10-2': ('APPLICATION', 'A6 per inter-event occasion (D5 [M]) is not the clock kernel of a Hawkes process'),
    'P05-5': ('KNOB', 'A6 at q = 0.5 against the Kalman filter: the matching q depends on the noise ratio'),
    'P14-1': ('KNOB', 'A6 at q = 0.5 in a bandit: a two-step memory; CRR does not fix q'),
    'P11-4': ('KNOB', 'A6 at a fixed q against pharmacokinetic accumulation: the q that matches is set by the elimination rate'),
    'P11-1': ('KNOB', 'A6 in the glucose model: the label turns on the occasion length (O1)'),
}


def grab(pat, text=L, cast=int):
    m = re.search(pat, text)
    return tuple(cast(g) for g in m.groups()) if m else None


def main():
    print('Redundant / consistent / descriptive against fails, and PRED70\'s WRONG rows under CRR.md section 9 (prompt-log 235)')
    print()
    print('[1] The counts, layer by layer (every number read from a pinned output)')
    b = grab(r'all\s+rows\s+(\d+) \| SHARP (\d+) CONSIST (\d+) DESCR (\d+) FAILS (\d+) TENSION (\d+) OPEN (\d+)')
    n, sh, co, de, fa, te, op = b
    print(f'  (a) retrodiction batteries, {n} rows: CONSIST {co} + DESCR {de} = {co + de} consistent/descriptive; FAILS {fa}; '
          f'TENSION {te}; OPEN {op}; SHARP {sh}  -> consistent/descriptive : fail = {co + de}:{fa} ({(co + de) / fa:.2f} to 1)')
    s = grab(r'all real-domain rows\s+rows\s+(\d+) \| ADDS (\d+) PROPOSES (\d+) REDUNDANT-IG (\d+) REDUNDANT-DOMAIN (\d+) WRONG (\d+) INTERNAL (\d+) UNSTATED (\d+)')
    n2, ad, pr, ri, rd, wr, it, us = s
    print(f'  (b) synthesis re-read, {n2} real-domain rows: REDUNDANT-IG {ri} + REDUNDANT-DOMAIN {rd} = {ri + rd} redundant; WRONG {wr}; '
          f'ADDS {ad}; INTERNAL {it}; PROPOSES {pr}; UNSTATED {us}  -> redundant : fail = {ri + rd}:{wr} ({(ri + rd) / wr:.2f} to 1)')
    for g in ('CONSIST', 'DESCR'):
        c = grab(rf'{g}\s+(\d+) \| ADDS (\d+) PROPOSES (\d+) REDUNDANT-IG (\d+) REDUNDANT-DOMAIN (\d+) WRONG (\d+) INTERNAL (\d+) UNSTATED (\d+)')
        print(f'      the {c[0]} {g} rows re-read: redundant {c[3] + c[4]}, WRONG {c[5]}, INTERNAL {c[6]}, ADDS {c[1]}, UNSTATED {c[7]}')
    oc = dict((k, int(v)) for k, v in re.findall(r'(ADDS|PROPOSES|REDUNDANT-IG|REDUNDANT-DOMAIN|WRONG|INTERNAL|UNSTATED) (\d+)',
                                                   re.search(r'outcomes:\s+(.*)', T)[1]))
    red = oc['REDUNDANT-IG'] + oc['REDUNDANT-DOMAIN']
    print(f"  (c) PRED70, 70 declared predictions: REDUNDANT-IG {oc['REDUNDANT-IG']} + REDUNDANT-DOMAIN {oc['REDUNDANT-DOMAIN']} = {red} "
          f"redundant; WRONG {oc['WRONG']}; ADDS {oc['ADDS']}; INTERNAL {oc['INTERNAL']}; UNSTATED {oc['UNSTATED']}  -> redundant : fail = "
          f"{red}:{oc['WRONG']} ({red / oc['WRONG']:.2f} to 1)")
    hf = grab(r'held-out\s+FAIL\s+(\d+)'); p0 = grab(r'held-out\s+PASS-0\s+(\d+)'); p1 = grab(r'held-out\s+PASS-1\s+(\d+)')
    print(f'  (d) the held-out ledger (pre-registered, unseen data): PASS-0 {p0[0]}, PASS-1 {p1[0]}, FAIL {hf[0]} '
          f'(no redundant grade exists on the ledger: a pass that reduces to a constant is its own allocation)')
    tot_red = co + de + ri + rd + red; tot_f = fa + wr + oc['WRONG']
    print(f'  retrodictive + synthetic layers together (a + b + c; rows of (b) are re-reads of (a), so this double-counts '
          f'by design): consistent/descriptive/redundant {tot_red}, fail {tot_f}')
    print()
    print('[2] PRED70\'s WRONG rows: should any be REDUNDANT?')
    rows = re.findall(r'^\s+(P\d\d-\d)\s+(.{16})\s+(\S+)\s+\S+\s+(yes|no)\s+(holds|fails|not computable)\s+(yes|-)\s+(PASS|FAIL|OPEN|-)', T, re.M)
    wrong = [r for r in rows if r[2] == 'WRONG']
    print(f'  WRONG rows in the tally: {len(wrong)}; rows with a class reading here: {len(READ)}; '
          f"missing: {sorted(set(r[0] for r in wrong) - set(READ)) or 'none'}")
    print('  the harness rule: a row is REDUNDANT only if the CRR value agrees with the null (T-G) or the domain (T-N) within '
          '1 %; a row reaches WRONG only when both read "differ" (src/crr/synthesis/harness.py: outcome()). Relabelling a '
          'WRONG row as REDUNDANT would need a tolerance changed after the result (R15; CLAUDE.md section 10). Rows that '
          f'qualify for REDUNDANT under the declared rule: 0 of {len(wrong)}')
    cls = {}
    for rid, ing, oc_, hit, q, dev, amp in wrong:
        c, why = READ[rid]; cls.setdefault(c, []).append(rid)
        print(f'    {rid} {ing.strip():16} {c:11} {why}')
    for c in ('FALSIFIES', 'SCOPE', 'APPLICATION', 'KNOB'):
        print(f'  {c:11} {len(cls.get(c, [])):2d}  {", ".join(cls.get(c, []))}')
    print()
    print('[3] The reverse direction: ADDS rows that are fails under section 9')
    hl5 = [r for r in rows if r[1].strip() == 'H-L5']
    s9 = {}
    for rid, ing, oc_, hit, q, dev, amp in hl5:
        s9[rid] = 'PASS' if (q == 'holds' and amp == 'PASS') else ('UNDETERMINED (amplitude not printed)' if (q == 'holds' and amp == '-') else 'FAIL')
    fails9 = [r for r in s9 if s9[r] == 'FAIL']
    adds_fail = [r[0] for r in hl5 if r[2] == 'ADDS' and s9[r[0]] == 'FAIL']
    print(f'  H-L5 fails "if CV_C >= CV_dt, or a control matches it" (section 9). PRED70 H-L5 rows {len(hl5)}: section-9 FAIL '
          f'{len(fails9)}, PASS {sum(v == "PASS" for v in s9.values())}, undetermined {sum(v.startswith("UNDET") for v in s9.values())} '
          f'({", ".join(r for r in s9 if s9[r] != "FAIL")})')
    print(f'  harness ADDS rows that are section-9 H-L5 FAILs (the amplitude control matches): {len(adds_fail)} ({", ".join(adds_fail)})')
    print()
    print('[4] PRED70 read under section 9 (a reading, not a relabel; the pinned harness labels stand)')
    fal = len(cls.get('FALSIFIES', [])) + len(adds_fail)
    print(f'  fails that count against a falsifiable CRR claim: {fal} (WRONG rows that falsify {len(cls.get("FALSIFIES", []))} '
          f'+ H-L5 ADDS rows failing their control {len(adds_fail)})')
    print(f'  fails that bound CRR\'s reach without falsifying it (APPLICATION + KNOB): '
          f'{len(cls.get("APPLICATION", [])) + len(cls.get("KNOB", []))}; fails CRR itself predicts (SCOPE): {len(cls.get("SCOPE", []))}')
    print(f"  redundant (consistent but not risky): {red}; surviving candidates (A6 ADDS): {oc['ADDS'] - len(adds_fail)}")


if __name__ == '__main__':
    main()
