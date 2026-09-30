"""SPA1 (SEC_Prior_Art/DECLARATION.md, pushed at 512ad74 before any search): grade positions S1-S6 against the three
dossiers docs/citations/spa1_f{1,2,3}_2026-09-30.md (claims_f1-f3.py; quotes checked in verify.txt) by RQM's rule, and
compute the declared verdict rule. Deterministic, stdlib only; does not read the raw source texts.
Run: python3 SEC_Prior_Art/checks/grade.py
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims_f1, claims_f2, claims_f3  # noqa: E402

CLAIMS = claims_f1.CLAIMS + claims_f2.CLAIMS + claims_f3.CLAIMS

# (id, position, forecast): copied from SEC_Prior_Art/DECLARATION.md
POSITIONS = [
    ('S1', 'the EWC/Laplace penalty strength lambda must be tuned per dataset because the (empirical) Fisher scale is wrong or '
           'arbitrary', 'REDUNDANT'),
    ('S2', "rescaling a Fisher or Laplace precision by a factor fitted to the loss's observed curvature is published",
     'PARTLY REDUNDANT'),
    ('S3', 'a curvature scale fitted along the optimisation path (quasi-Newton or secant style) is used to set a '
           'continual-learning penalty or an online Laplace posterior', 'PARTLY REDUNDANT'),
    ('S4', 'setting the penalty or prior precision without tuning, by a principled rule, is published for continual learning',
     'REDUNDANT'),
    ('S5', 'clipping or bounding the penalty curvature by the step size (the stability edge) is published for '
           'regularisation-based continual learning', 'PARTLY REDUNDANT'),
    ('S6', 'a tuning-free Laplace or EWC weight is reported to match a tuned lambda across many datasets',
     'NOT FOUND IN THE SWEEP'),
]
READINGS = ('states', 'close', 'bears', 'contradicts')
ORDER = {r: i for i, r in enumerate(('states', 'contradicts', 'close', 'bears'))}


def grade(n):
    if n['states'] and n['contradicts']:
        return 'MIXED'
    if n['states']:
        return 'REDUNDANT'
    if n['close']:
        return 'PARTLY REDUNDANT'
    return 'NOT FOUND IN THE SWEEP'


def main():
    bad = [c['id'] for c in CLAIMS if c['reading'] not in READINGS or c['tag'] not in {p[0] for p in POSITIONS}]
    assert not bad, f'claims with an unknown reading or tag: {bad}'
    ids = [c['id'] for c in CLAIMS]
    assert len(ids) == len(set(ids)), 'duplicate claim ids'
    fams = collections.Counter(c['id'].split(':')[0] for c in CLAIMS)
    srcs = {c['url'] for c in CLAIMS}
    print("SPA1: positions S1-S6 graded against the prior-art sweep of SEC4's method (SEC_Prior_Art/DECLARATION.md)")
    print(f"claims {len(CLAIMS)} ({', '.join(f'{k} {fams[k]}' for k in sorted(fams))}); sources {len(srcs)}; "
          "quotes verified in verify.txt")
    print('rule: MIXED if states and contradicts; else REDUNDANT if states; else PARTLY REDUNDANT if close; '
          'else NOT FOUND IN THE SWEEP')
    print()
    rows = {}
    for pid, text, expected in POSITIONS:
        cs = [c for c in CLAIMS if c['tag'] == pid]
        n = collections.Counter(c['reading'] for c in cs)
        lab = grade(n); hit = 'hit' if lab == expected else 'MISS'; rows[pid] = (lab, expected, hit)
        print(f"{pid} {lab:22} expected {expected:22} {hit:4} | states {n['states']}, contradicts {n['contradicts']}, "
              f"close {n['close']}, bears {n['bears']}")
        print(f"     position: {text}")
        for c in sorted(cs, key=lambda c: (ORDER[c['reading']], c['id'].split(':')[0], int(c['id'].split(':')[1]))):
            print(f"     {c['reading']:11} {c['id']:6} {c['source'][:84]} ({c['version'][:22]})")
        print()
    print('summary (position, grade, expected, hit/miss)')
    for pid, (lab, expected, hit) in rows.items():
        print(f'  {pid}  {lab:22}  {expected:22}  {hit}')
    hits = sum(r[2] == 'hit' for r in rows.values())
    print(f'hits {hits} of {len(rows)}; misses: {", ".join(p for p, r in rows.items() if r[2] != "hit") or "none"}')
    g = {p: r[0] for p, r in rows.items()}
    print()
    print('verdict rule (DECLARATION.md): KNOWN if (S2 or S3 REDUNDANT) and S4 REDUNDANT; else PARTLY KNOWN if any of S2-S5 is '
          'REDUNDANT or PARTLY REDUNDANT; else NOT FOUND IN THE SWEEP')
    hit = lambda p: g[p] in ('REDUNDANT', 'MIXED')  # noqa: E731
    if (hit('S2') or hit('S3')) and hit('S4'):
        v = 'KNOWN'
    elif any(g[p] in ('REDUNDANT', 'MIXED', 'PARTLY REDUNDANT') for p in ('S2', 'S3', 'S4', 'S5')):
        v = 'PARTLY KNOWN'
    else:
        v = 'NOT FOUND IN THE SWEEP'
    print(f'VERDICT: {v} (S2 {g["S2"]}, S3 {g["S3"]}, S4 {g["S4"]}, S5 {g["S5"]}, S6 {g["S6"]})')
    print("part by part: SEC's Fisher rescaling itself is S2 (" + g['S2'] + "); the stability clip is S5 (" + g['S5']
          + "); the tuning-free claim across many datasets is S6 (" + g['S6'] + ')')
    print('not found is never read as novel')


if __name__ == '__main__':
    main()
