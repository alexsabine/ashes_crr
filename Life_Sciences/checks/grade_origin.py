"""Grade OL-1 (origin-of-life theories against CRR's ingredients I1-I5) and DS-4 (mutation rate per generation against per
year), as declared in Life_Sciences/DECLARATION_1.md (pushed at ed4b04a before the sources were fetched).

    python3 Life_Sciences/checks/grade_origin.py > Life_Sciences/checks/grade_origin.txt

The per-claim readings in claims_origin.py are the investigator's (CONTAINS / CONFLICTS / SILENT, decided after reading the
quotes; the source agent proposed, the investigator kept or changed, and every change is listed in claims_origin.py). Labels
are computed here (R15):
  cell (theory, ingredient): CONTAINS if some claim CONTAINS and none CONFLICTS; CONFLICTS if some CONFLICTS and none
      CONTAINS; MIXED if both (counted for neither; AGENT_LOG 162); SILENT otherwise. REDUNDANT = CONTAINS.
  ingredient: DISCRIMINATES if at least one theory CONTAINS it and at least one CONFLICTS; NON-DISCRIMINATING otherwise.
  DS-4: AGREES if the per-generation spread < the per-year spread, DISAGREES if >, on one footing (same species set and
      statistic); SILENT if the sources do not state both on one footing.
Quotes are checked verbatim against the saved texts by verify_origin.py (output verify_origin.txt). Novelty is never judged.
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims_origin as C  # noqa: E402

ING = {'I1': 'A3 with O3: a cut needs a rotor, so the first cut needs the first self-sustaining cycle',
       'I2': 'A6: the next occasion is seeded from the settled past at bounded strength (heredity without accumulation)',
       'I3': "H-L5: the system's own events, not clock time, set its clock",
       'I4': 'D2 against D3: the travelled path against the shortest path (surplus S = C - C*)',
       'I5': 'Proposition 7 / A8: the cut has no content; nothing is fed by a future'}


def cell(readings):
    has_c, has_x = 'CONTAINS' in readings, 'CONFLICTS' in readings
    if has_c and has_x:
        return 'MIXED'
    if has_c:
        return 'CONTAINS'
    if has_x:
        return 'CONFLICTS'
    return 'SILENT'


def main():
    print('OL-1: origin-of-life theories against CRR ingredients I1-I5 (Life_Sciences/DECLARATION_1.md)')
    cl = [c for c in C.CLAIMS if c['ingredient'] in ING]
    theories = list(dict.fromkeys((c['theory'], c['name']) for c in cl))
    nq = sum(len(c['quote']) for c in cl)
    print(f'theories {len(theories)}, claims {len(cl)}, quotes {nq}; quotes verified in verify_origin.txt')
    print()
    grid = {}
    print(f"{'theory':46}" + ''.join(f'{i:>11}' for i in ING))
    for t, name in theories:
        row = []
        for i in ING:
            lab = cell([c['reading'] for c in cl if c['theory'] == t and c['ingredient'] == i])
            grid[(t, i)] = lab
            row.append(lab)
        print(f'{t + " " + name:46.46}' + ''.join(f'{x:>11}' for x in row))
    print()
    disc = 0
    for i, text in ING.items():
        n = collections.Counter(grid[(t, i)] for t, _ in theories)
        lab = 'DISCRIMINATES' if n['CONTAINS'] and n['CONFLICTS'] else 'NON-DISCRIMINATING'
        disc += lab == 'DISCRIMINATES'
        print(f"{i} {lab:18} CONTAINS (REDUNDANT) {n['CONTAINS']}, CONFLICTS {n['CONFLICTS']}, MIXED {n['MIXED']}, "
              f"SILENT {n['SILENT']} | {text}")
        for lab2 in ('CONTAINS', 'CONFLICTS', 'MIXED'):
            ts = [t for t, _ in theories if grid[(t, i)] == lab2]
            if ts:
                print(f"     {lab2.lower()}: {', '.join(ts)}")
    print(f'OL-1: {disc} of {len(ING)} ingredients discriminate between the theories '
          f"(the investigator's expectation, 0 of {len(ING)}: {'met' if disc == 0 else 'not met'})")
    changed = [c for c in cl if 'change' in c]
    print(f"investigator's changes to the proposed readings: {len(changed)}")
    for c in changed:
        print(f"  {c['theory']} {c['ingredient']}: {c['proposed']} -> {c['reading']} ({c['change']})")
    disc_p, lab_p = 0, []
    for i in ING:
        n = collections.Counter(cell([c['proposed'] for c in cl if c['theory'] == t and c['ingredient'] == i])
                                for t, _ in theories)
        d = bool(n['CONTAINS'] and n['CONFLICTS'])
        disc_p += d
        lab_p.append(f"{i} {'DISCRIMINATES' if d else 'non-discriminating'} ({n['CONTAINS']} contains, {n['CONFLICTS']} conflicts)")
    print(f"sensitivity, the agent's proposed readings: {disc_p} of {len(ING)} discriminate: " + '; '.join(lab_p))
    print()
    print("OL-1 signature predictions recorded (theory: the source's own test, as quoted; not graded)")
    for t, name in theories:
        ps = [c for c in C.CLAIMS if c['theory'] == t and c['ingredient'] == 'PRED']
        print(f"  {t} {name}: {len(ps)} claim(s), {sum(len(p['quote']) for p in ps)} quote(s)")
    print()
    d = C.DS4
    same = d['same_footing']
    if not same:
        lab = 'SILENT'
    else:
        lab = 'AGREES' if d['gen_fold'] < d['year_fold'] else ('DISAGREES' if d['gen_fold'] > d['year_fold'] else 'SILENT')
    print('DS-4: germline mutation rate, spread across species per generation against per year (own event = generation)')
    print(f"  per generation: {d['gen_fold']:g}-fold ({d['gen_basis']})")
    print(f"  per year: more than {d['year_fold']:g}-fold ({d['year_basis']})")
    print(f"  one footing (same species set and statistic): {'yes' if same else 'no'} -> DS-4 {lab}")
    if not same:
        print(f"  report only, not a grade: were the footing accepted, the per-generation spread would be the "
              f"{'narrower' if d['gen_fold'] < d['year_fold'] else 'wider'}")
    print(f"  the matched pair on one footing: {d['matched_pair']}")


if __name__ == '__main__':
    main()
