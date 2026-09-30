"""Grade RRM's positions N1-N6 (Relational_Reference_Memory/DECLARATION.md §6) against the literature sweep (dossier
docs/citations/rrm_2026-09-30.md), by the rule declared there ("rule as RQM"):
  MIXED                   if a position has at least one 'states' and at least one 'contradicts' claim;
  REDUNDANT               otherwise, if it has any 'states';
  PARTLY REDUNDANT        otherwise, if it has any 'close';
  NOT FOUND IN THE SWEEP  otherwise (never read as novel).
The per-claim readings are in claims.py (decided by the grading agent from the quotes, for the investigator's review); the
expected grades are the declaration's table, fixed before the sweep. Quotes are verified in verify.txt.
Deterministic, stdlib only; does not read the raw source texts. Run: python3 Relational_Reference_Memory/checks/grade.py
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims as C  # noqa: E402

# (id, position, expected grade): copied from DECLARATION.md §6
POSITIONS = [
    ('N1', 'correcting stored prototypes or statistics for feature drift by measuring how reference points move is '
           'published', 'REDUNDANT'),
    ('N2', 'estimating that drift from kept old-class exemplars or anchors, rather than from current-task data, is '
           'published', 'PARTLY REDUNDANT'),
    ('N3', 'representations relative to a set of anchors are invariant to angle-preserving changes of the latent space',
     'REDUNDANT'),
    ('N4', 'preserving relations between samples (relational distillation) reduces forgetting', 'REDUNDANT'),
    ('N5', 'storing old-class feature distributions in coordinates relative to a few kept anchors, and transporting them '
           "with the anchors' current features (RRM)", 'PARTLY REDUNDANT'),
    ('N6', 'developmental or object-relations framings (a first reference object, increasing resolution) used to design '
           'continual learners', 'PARTLY REDUNDANT'),
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
    bad = [c['id'] for c in C.CLAIMS if c['reading'] not in READINGS or c['tag'] not in {p[0] for p in POSITIONS}]
    assert not bad, f'claims with an unknown reading or tag: {bad}'
    fams = collections.Counter(c['id'].split(':')[0] for c in C.CLAIMS)
    srcs = {c['url'] for c in C.CLAIMS}
    print("RRM: positions N1-N6 graded against the literature sweep (DECLARATION.md §6)")
    print(f"claims {len(C.CLAIMS)} ({', '.join(f'{k} {fams[k]}' for k in sorted(fams))}); sources {len(srcs)}; readings by "
          f"{sorted({c['reading_by'] for c in C.CLAIMS})[0]}; quotes verified in verify.txt")
    print('rule: MIXED if states and contradicts; else REDUNDANT if states; else PARTLY REDUNDANT if close; '
          'else NOT FOUND IN THE SWEEP')
    print()
    rows = []
    for pid, text, expected in POSITIONS:
        cs = [c for c in C.CLAIMS if c['tag'] == pid]
        n = collections.Counter(c['reading'] for c in cs)
        lab = grade(n)
        hit = 'hit' if lab == expected else 'MISS'
        rows.append((pid, lab, expected, hit))
        print(f"{pid} {lab:22} expected {expected:22} {hit:4} | states {n['states']}, contradicts {n['contradicts']}, "
              f"close {n['close']}, bears {n['bears']}")
        print(f"     position: {text}")
        for c in sorted(cs, key=lambda c: (ORDER[c['reading']], c['id'].split(':')[0], int(c['id'].split(':')[1]))):
            print(f"     {c['reading']:11} {c['id']:6} {c['source'][:84]} ({c['version'][:22]})")
        print()
    hits = sum(r[3] == 'hit' for r in rows)
    print('summary (position, grade, expected, hit/miss)')
    for pid, lab, expected, hit in rows:
        print(f'  {pid}  {lab:22}  {expected:22}  {hit}')
    print(f'hits {hits} of {len(rows)}; misses: {", ".join(r[0] for r in rows if r[3] != "hit") or "none"}')
    print('not found is never read as novel')


if __name__ == '__main__':
    main()
