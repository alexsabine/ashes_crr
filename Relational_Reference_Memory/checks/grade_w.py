"""RRM2 Part W (Relational_Reference_Memory/DECLARATION_2.md, pushed at a2719f0 before any search): grade positions P1-P7
against the frontier sweep (dossiers docs/citations/rrm2_f{1,2,3}_2026-09-30.md; claims in claims_w1-3.py) by RQM's rule,
and compute the declared worth rule:
  MIXED if states and contradicts; else REDUNDANT if states; else PARTLY REDUNDANT if close; else NOT FOUND IN THE SWEEP.
  WORTH PURSUING iff P1 in {REDUNDANT, MIXED} and P2, P3, P5 not REDUNDANT; otherwise NOT WORTH PURSUING (failing
  positions named). P4, P6, P7 reported, not gating.
Deterministic, stdlib only; does not read the raw source texts. Run: python3 Relational_Reference_Memory/checks/grade_w.py
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims_w1, claims_w2, claims_w3  # noqa: E402

CLAIMS = claims_w1.CLAIMS + claims_w2.CLAIMS + claims_w3.CLAIMS

# (id, position, forecast): copied from DECLARATION_2.md Part W
POSITIONS = [
    ('P1', '2025-26 papers still name the drift of stored class statistics as a main limitation of exemplar-free or '
           'small-memory class-IL trained from scratch', 'REDUNDANT'),
    ('P2', 'a 2025-26 exemplar-free method trained from scratch reports class-IL accuracy level with or ahead of replay at a '
           'realistic buffer, on the same protocol (the gap is closed)', 'MIXED'),
    ('P3', 'hybrids that keep a few exemplars and class statistics, and use the kept exemplars to correct the stored '
           'statistics, are published', 'PARTLY REDUNDANT'),
    ('P4', 'anchor-relative or relative representations are used inside one continual learner to keep old representations '
           'valid', 'PARTLY REDUNDANT'),
    ('P5', "transporting stored old-class statistics by the measured feature movement of a few kept anchors (RRM's "
           'transport) is published', 'PARTLY REDUNDANT'),
    ('P6', 'on-device or privacy-constrained continual learning is named as a setting where a small store of raw rows is '
           'acceptable and a full replay buffer is not', 'REDUNDANT'),
    ('P7', 'the feature drift of a class-IL learner is reported to be approximately linear, or well corrected by a linear '
           'map', 'MIXED'),
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
    print("RRM2 Part W: positions P1-P7 graded against the frontier sweep (DECLARATION_2.md)")
    print(f"claims {len(CLAIMS)} ({', '.join(f'{k} {fams[k]}' for k in sorted(fams))}); sources {len(srcs)}; "
          "quotes verified in verify_w.txt")
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
    fail = []
    if rows['P1'][0] not in ('REDUNDANT', 'MIXED'):
        fail.append('P1 (the problem is not shown to be live)')
    for pid, why in (('P2', 'the gap to replay is closed'), ('P3', 'the niche is filled'), ('P5', 'the transport is published')):
        if rows[pid][0] == 'REDUNDANT':
            fail.append(f'{pid} ({why})')
    print()
    print('worth rule: WORTH PURSUING iff P1 REDUNDANT or MIXED, and P2, P3, P5 not REDUNDANT')
    print('VERDICT: ' + ('WORTH PURSUING' if not fail else 'NOT WORTH PURSUING; failing: ' + '; '.join(fail)))
    print('not found is never read as novel; WORTH means only that a test is not redundant before it runs')


if __name__ == '__main__':
    main()
