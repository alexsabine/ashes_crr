"""Retrodictive grading of CRR's predictions for the mechanisms of state-of-the-art continual-learning methods.

Declared in `CL Design Principle/DECLARATION_1.md` (pushed at fe09261 before the dossiers were read). The rows are in
`ablation_rows.py`, extracted from the three dossiers `docs/citations/cl_sota_*_2026-09-25.md`, every number inside a
verbatim quote. Labels are computed here (R15). Run: python3 "CL Design Principle/checks/retro_sota.py"
"""
import collections
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ablation_rows as A  # noqa: E402

# DECLARATION_1: '+' removing the mechanism lowers accuracy by >= one step (with - without >= step);
# '0' |effect| < step; 'nb' not behind by more than one step (with - without > -step). M8 and M13 are stated as
# "replay - LwF >= step" and "ER - A-GEM >= step", i.e. '+' with the mechanism on the replay / ER side.
PRED = {'M1': '+', 'M2': '+', 'M3': '0', 'M4': '+', 'M5': '0', 'M6a': '+', 'M6b': '0', 'M7': '+', 'M8': '+',
        'M9': '+', 'M10': '+', 'M11': '+', 'M11b': '0', 'M12': '0', 'M13': '+', 'M14': 'nb', 'M17': '+', 'M18': '+'}
ORDER = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6a', 'M6b', 'M7', 'M8', 'M9', 'M10', 'M11', 'M11b', 'M12', 'M13', 'M14',
         'M17', 'M18']
# The declared setting is class-incremental with a buffer; M17's is a loss-of-plasticity setting and M18's is
# FOREVER's own benchmark (declared in the table), so those two are graded on the settings their sources report.
OWN_SETTING = {'M17', 'M18'}


def step(r):
    stds = [s for s in (r.get('with_std'), r.get('without_std')) if s is not None]
    return max(1.0, 2 * max(stds)) if stds else 1.0


def effect(r):
    e = r['with_value'] - r['without_value']
    return e if r.get('higher_is_better', True) else -e


def label(e, s):
    return 'helps' if e >= s else ('hurts' if e <= -s else 'no effect')


def agrees(pred, e, s):
    if pred == '+':
        return e >= s
    if pred == '0':
        return abs(e) < s
    if pred == 'nb':
        return e > -s
    raise ValueError(pred)


def in_scope(r):
    return r['mech'] in OWN_SETTING or r['setting'].startswith('class-IL')


def main():
    rows = [r for r in A.ROWS if not r.get('none')]
    print('Retrodictive grading of DECLARATION_1 (CL Design Principle), rows from checks/ablation_rows.py')
    print(f'rows extracted: {len(rows)}; silent mechanisms (not graded): {", ".join(A.SILENT)}')
    print('step = max(1.0, 2 x larger reported std of the pair); effect = with - without (sign flipped where lower is better)')
    print()
    hdr = f"{'mech':5} {'pred':4} {'graded':>6} {'out':>4} {'helps':>5} {'none':>5} {'hurts':>5} {'agree':>5} {'median eff':>10}  outcome"
    print(hdr)
    print('-' * len(hdr))
    summary = {}
    for m in ORDER:
        rs = [r for r in rows if r['mech'] == m]
        g = [r for r in rs if in_scope(r)]
        out = len(rs) - len(g)
        labs = collections.Counter(label(effect(r), step(r)) for r in g)
        ag = sum(agrees(PRED[m], effect(r), step(r)) for r in g)
        if not g:
            outcome = 'NOT REPORTED'
        elif ag == len(g):
            outcome = 'AGREES'
        elif ag == 0:
            outcome = 'DISAGREES'
        else:
            outcome = 'MIXED'
        med = statistics.median(effect(r) for r in g) if g else float('nan')
        summary[m] = (outcome, ag, len(g))
        print(f"{m:5} {PRED[m]:4} {len(g):6d} {out:4d} {labs['helps']:5d} {labs['no effect']:5d} {labs['hurts']:5d} "
              f"{ag:5d} {med:10.2f}  {outcome} ({ag}/{len(g)} rows agree)")
    print()
    print('Online / offline split (class-incremental rows only):')
    for m in ORDER:
        for mode in ('online', 'offline'):
            g = [r for r in rows if r['mech'] == m and r['setting'].startswith('class-IL') and mode in r['setting']]
            if g:
                ag = sum(agrees(PRED[m], effect(r), step(r)) for r in g)
                med = statistics.median(effect(r) for r in g)
                print(f"  {m:5} {mode:7} rows {len(g):3d}  agree {ag:3d}  median effect {med:7.2f}")
    print()
    tot = collections.Counter(o for o, _, _ in summary.values())
    print('Mechanism outcomes:', ', '.join(f'{k} {v}' for k, v in sorted(tot.items())))
    n_ag = sum(a for _, a, _ in summary.values())
    n_g = sum(n for _, _, n in summary.values())
    print(f'Rows agreeing: {n_ag} of {n_g} graded rows')
    print()
    print('Out-of-scope rows (task-IL, GCIL and other settings for M1-M16), listed and not graded:')
    for r in rows:
        if not in_scope(r):
            print(f"  {r['mech']:5} {r['source'][:40]:40} {r['setting'][:50]:50} {r['with_value']} vs {r['without_value']}")


if __name__ == '__main__':
    main()
