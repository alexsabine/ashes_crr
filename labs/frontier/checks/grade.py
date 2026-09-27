"""Grade the frontier domains F1-F12 against CRR's retrodictive record (labs/frontier/DECLARATION.md, pushed at 289a79d
before any source was fetched; prompt-log entry 226).

    python3 labs/frontier/checks/grade.py > labs/frontier/checks/grade.txt

Inputs: claims.py (quotes transcribed from docs/citations/frontier_domains_2026-09-27_*.md and, for F1, the dossiers of
2026-09-23/25; checked verbatim by verify.py) and the investigator's per-domain readings in claims.READINGS, decided after
reading the quotes. The label is computed here from the readings by the declared rule (R15):
  reading CONFLICT-W                                  -> AVOID
  reading COMPATIBLE-P, CRR's direction named         -> RESTATES
  reading COMPATIBLE-P, not named, measurable H1/H0   -> GUIDES (a lab candidate; still needs the labs entry rule)
  reading COMPATIBLE-P, not named, not measurable     -> SILENT
  reading OUTSIDE                                     -> SILENT (outside the record)
'Not found in the fetched sources' is never read as novel.
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims as C  # noqa: E402

EXPECTED = {'F1': 'RESTATES', 'F2a': 'GUIDES', 'F2b': 'GUIDES',  # the declaration's F2 row, split after reading (AGENT_LOG 166)
            'F3': 'RESTATES', 'F4': 'RESTATES', 'F5': 'RESTATES', 'F6': 'GUIDES or RESTATES',
            'F7': 'GUIDES or RESTATES', 'F8': 'RESTATES', 'F9': 'RESTATES', 'F10': 'AVOID', 'F11': 'AVOID', 'F12': 'RESTATES'}


def label(r):
    if r['reading'] == 'CONFLICT-W':
        return 'AVOID'
    if r['reading'] == 'OUTSIDE':
        return 'SILENT'
    if r['direction_named']:
        return 'RESTATES'
    return 'GUIDES' if r['measurable_h1'] else 'SILENT'


def main():
    byid = {c['id']: c for c in C.CLAIMS}
    print('Frontier domains against CRR\'s retrodictive record (labs/frontier/DECLARATION.md; prompt-log entry 226)')
    n_q = sum(len(c['quote']) for c in C.CLAIMS)
    print(f'claims {len(C.CLAIMS)}, quotes {n_q} (verified in verify.txt); domains {len(C.READINGS)}')
    print()
    tally = collections.Counter()
    for r in C.READINGS:
        lab = label(r)
        tally[lab] += 1
        exp = EXPECTED[r['domain']]
        met = lab in exp.split(' or ')
        print(f"{r['domain']:3} {r['name']}")
        print(f"    reading {r['reading']} ({r['principle']}); CRR direction named in the sources: "
              f"{'yes' if r['direction_named'] else ('no' if r['direction_named'] is False else 'n/a')}; "
              f"measurable H1 against H0: {'yes' if r['measurable_h1'] else 'no'}")
        print(f"    -> {lab} (declared expectation: {exp}; {'met' if met else 'NOT met'})")
        for cid in r['bottleneck_claims']:
            c = byid[cid]
            print(f"    bottleneck [{cid}] {c['source'][:90]} ({c['version'][:40]}): \"{c['quote'][0][:220]}\"")
        for cid in r.get('h0_claims', []):
            c = byid[cid]
            print(f"    field's H0 [{cid}] {c['source'][:90]}: \"{c['quote'][0][:220]}\"")
        for cid in r['direction_claims']:
            c = byid[cid]
            print(f"    direction  [{cid}] {c['source'][:90]}: \"{c['quote'][0][:220]}\"")
        print(f"    note: {r['note']}")
        print()
    print('TALLY: ' + ', '.join(f'{k} {v}' for k, v in sorted(tally.items())))
    met = sum(label(r) in EXPECTED[r['domain']].split(' or ') for r in C.READINGS)
    print(f'declared expectations met: {met} of {len(C.READINGS)}')


if __name__ == '__main__':
    main()
