"""Retrodictive grading of CRR's predictions for the mechanisms that save energy in AI training and execution.

Declared in `Energy Design Principle/DECLARATION_1.md` (pushed at db871f6 before the dossiers were fetched). Rows are in
`energy_rows.py`, extracted from `docs/citations/energy_{accounting,training,inference}_2026-09-25.md`, every number inside a
verbatim quote. Labels are computed here (R15). Run: python3 "Energy Design Principle/checks/retro_energy.py"

The declaration's rule, as implemented:
- cost ratio r = C_X / C_Y (a cost where higher is better, e.g. throughput or goodput, is inverted): SAVES r <= 0.90,
  COSTS r >= 1.10, SAME otherwise;
- quality step: 0-100 scale max(1.0, 2 sd); 0-1 scale max(0.01, 2 sd); lower-is-better max(1 % of Y, 2 sd);
  AHEAD / BEHIND by at least a step, NOT BEHIND otherwise;
- codes: '+' SAVES and not BEHIND (matched-compute rows: not BEHIND); '0' SAME or COSTS, or SAVES and BEHIND;
  '0d' |dQ| < step; 'q+' AHEAD; 'q-' BEHIND; '=' SAVES;
- a row missing a quantity its code needs is listed, not graded (a cost-only row is graded only under '=').
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import energy_rows as R  # noqa: E402

PRED = {'E1': '+', 'E2a': '+', 'E2b': '0d', 'E3': '+', 'E4': '0', 'E5': '+', 'E6a': 'q-', 'E6b': 'q+', 'E7': '+',
        'E8': '+', 'E9': '+', 'E10': '+', 'E11': '0d', 'E12': '+', 'E13': '+',
        'I1': '+', 'I2a': '+', 'I2b': '0', 'I3': 'q+', 'I4': '=', 'I5': '=', 'I6': '+', 'I7': '+', 'I8': '+', 'I11': '0'}
KIND = {'E4': 'COMPARATIVE', 'E2a': 'COMPARATIVE', 'E2b': 'COMPARATIVE', 'E6a': 'COMPARATIVE', 'E6b': 'COMPARATIVE',
        'E9': 'COMPARATIVE', 'E11': 'COMPARATIVE', 'I2b': 'COMPARATIVE', 'I11': 'COMPARATIVE', 'I4': 'INHERITED',
        'I5': 'INHERITED'}
SILENT = ['E14', 'E15', 'I9', 'I10', 'I12']
ORDER = list(PRED)


def cost_label(r):
    if r.get('x_cost') is None or r.get('y_cost') is None:
        return None, None
    x, y = float(r['x_cost']), float(r['y_cost'])
    ratio = (y / x) if r.get('cost_higher_is_better') else (x / y)
    return ratio, ('SAVES' if ratio <= 0.90 else 'COSTS' if ratio >= 1.10 else 'SAME')


def quality_label(r):
    if r.get('x_quality') is None or r.get('y_quality') is None:
        return None, None, None
    x, y = float(r['x_quality']), float(r['y_quality'])
    sds = [s for s in (r.get('x_quality_sd'), r.get('y_quality_sd')) if s is not None]
    sd2 = 2 * max(sds) if sds else 0.0
    if r['higher_is_better']:
        step = max(1.0 if r['scale'] == 100 else 0.01, sd2)
        d = x - y
    else:
        step = max(0.01 * abs(y), sd2)
        d = y - x  # positive = X better
    return d, step, ('AHEAD' if d >= step else 'BEHIND' if d <= -step else 'NOT BEHIND')


def grade(code, r):
    """True / False, or None when the row lacks a quantity the code needs."""
    ratio, cl = cost_label(r)
    d, step, ql = quality_label(r)
    if code == '=':
        return None if cl is None else cl == 'SAVES'
    if code in ('q+', 'q-', '0d'):
        if ql is None:
            return None
        return {'q+': ql == 'AHEAD', 'q-': ql == 'BEHIND', '0d': abs(d) < step}[code]
    if code == '+':
        if r.get('matched_compute'):
            return None if ql is None else ql != 'BEHIND'
        if cl is None or ql is None:
            return None
        return cl == 'SAVES' and ql != 'BEHIND'
    if code == '0':
        if cl is None or ql is None:
            return None
        return cl in ('SAME', 'COSTS') or (cl == 'SAVES' and ql == 'BEHIND')
    raise ValueError(code)


def fmt(v, p=4):
    return '—' if v is None else f'{v:.{p}f}'


def main():
    rows = R.ROWS
    print('Retrodictive grading of DECLARATION_1 (Energy Design Principle), rows from checks/energy_rows.py')
    print(f'rows extracted: {len(rows)}; silent mechanisms (listed, not graded): {", ".join(SILENT)}')
    print('cost ratio X/Y: SAVES <= 0.90, COSTS >= 1.10; quality step: max(1 point | 0.01 | 1 % of Y, 2 sd)')
    print()
    print('Per row (graded rows marked AGREES / DISAGREES; rows lacking a needed quantity marked listed)')
    summary = {}
    for m in ORDER + SILENT:
        rs = [r for r in rows if r['mech'] == m]
        for r in rs:
            ratio, cl = cost_label(r)
            d, step, ql = quality_label(r)
            g = grade(PRED[m], r) if m in PRED else None
            tag = 'silent' if m in SILENT else ('listed' if g is None else ('AGREES' if g else 'DISAGREES'))
            mc = ' [matched compute]' if r.get('matched_compute') else ''
            print(f"  {m:4} {r['source'][:44]:44} {r['location'][:14]:14} X={r['x_label'][:28]:28} Y={r['y_label'][:24]:24} "
                  f"cost {fmt(ratio)} {cl or '—':5}  dQ {fmt(d, 3)} step {fmt(step, 3)} {ql or '—':10}{mc}  -> {tag}")
    print()
    print(f"{'mech':5} {'kind':12} {'pred':4} {'rows':>4} {'graded':>6} {'agree':>5}  outcome")
    for m in ORDER:
        rs = [r for r in rows if r['mech'] == m]
        gs = [grade(PRED[m], r) for r in rs]
        g = [x for x in gs if x is not None]
        ag = sum(g)
        outcome = ('NOT REPORTED' if not g else 'AGREES' if ag == len(g) else 'DISAGREES' if ag == 0 else 'MIXED')
        summary[m] = (outcome, ag, len(g))
        print(f"{m:5} {KIND.get(m, 'CLASS'):12} {PRED[m]:4} {len(rs):4d} {len(g):6d} {ag:5d}  {outcome}")
    print()
    tot = collections.Counter(o for o, _, _ in summary.values())
    print('Mechanism outcomes:', ', '.join(f'{k} {v}' for k, v in sorted(tot.items())))
    crr = {m: v for m, v in summary.items() if KIND.get(m, 'CLASS') != 'INHERITED'}
    tc = collections.Counter(o for o, _, _ in crr.values())
    print('CRR readings only (INHERITED excluded):', ', '.join(f'{k} {v}' for k, v in sorted(tc.items())))
    print(f"Rows agreeing: {sum(a for _, a, _ in summary.values())} of {sum(n for _, _, n in summary.values())} graded rows")


if __name__ == '__main__':
    main()
