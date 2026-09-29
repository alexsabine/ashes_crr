"""Grade positions U1-U8 against the literature sweep (Attention_Algorithms/DECLARATION.md §2, pushed at 0273a1c before
any search). Grades are computed from the investigator-reviewed per-claim readings in claims_f1.py, claims_f2.py and
claims_f3.py: U1-U5, U7 REDUNDANT if any 'states', PARTLY REDUNDANT if any 'close', else NOT FOUND IN THE SWEEP (never read
as novel); U6 MIXED if any 'mixed', else ESTABLISHED if any 'established', else WEAK if any 'weak'; U8 ADDRESSED if any
'addresses'. Global figures (tag 'G') are listed for the arithmetic.
Run: python3 Attention_Algorithms/checks/grade.py
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims_f1, claims_f2, claims_f3  # noqa: E402,E401

CLAIMS = claims_f1.CLAIMS + claims_f2.CLAIMS + claims_f3.CLAIMS
U = {'U1': 'engagement or retention objectives value the user\'s return (session end / time away is a loss)',
     'U2': 'that stake produces re-engagement actions (notification volume, autoplay, no natural stop)',
     'U3': '(CRR) an own-clock valuation: the pause has zero content, no incentive to shorten it (the empty pause)',
     'U4': '(CRR, shared) the true map: the pause as the user\'s own stop; the objective the user\'s reflective value',
     'U5': '(CRR) U3 and U4 as one construction',
     'U6': 'long-term effects of engagement-optimised feeds on users',
     'U7': 'company countermeasures leave the stake intact, mostly opt-in, weak evidence of effect',
     'U8': 'the tension: an empty pause costs engagement and revenue (incentives, regulation)'}
EXPECTED = {'U1': 'REDUNDANT', 'U2': 'REDUNDANT', 'U3': 'PARTLY REDUNDANT', 'U4': 'PARTLY REDUNDANT or REDUNDANT',
            'U5': 'NOT FOUND IN THE SWEEP or PARTLY REDUNDANT', 'U6': 'MIXED', 'U7': 'REDUNDANT', 'U8': 'ADDRESSED'}


def grade(tag, n):
    if tag == 'U6':
        return 'MIXED' if n['mixed'] else ('ESTABLISHED' if n['established'] else ('WEAK' if n['weak'] else 'NO EVIDENCE IN THE SWEEP'))
    if tag == 'U8':
        return 'ADDRESSED' if n['addresses'] else 'NOT ADDRESSED IN THE SWEEP'
    return 'REDUNDANT' if n['states'] else ('PARTLY REDUNDANT' if n['close'] else 'NOT FOUND IN THE SWEEP')


def main():
    fam = collections.Counter(c['id'].split(':')[0] for c in CLAIMS)
    src = len({c['url'] for c in CLAIMS})
    print('Attention algorithms: U1-U8 against the sweep of 2026-09-28 (DECLARATION.md §2)')
    print(f"claims {len(CLAIMS)} ({', '.join(f'{k} {v}' for k, v in sorted(fam.items()))}) from {src} distinct URLs; quotes verified in verify.txt")
    print()
    hit = 0
    for tag, text in U.items():
        cs = [c for c in CLAIMS if c['tag'] == tag]
        n = collections.Counter(c['reading'] for c in cs)
        g = grade(tag, n)
        ok = g in EXPECTED[tag].split(' or ')
        hit += ok
        print(f"{tag} {g:26} ({', '.join(f'{k} {v}' for k, v in sorted(n.items())) or 'no claims'}) | {text}")
        print(f"     declared expectation: {EXPECTED[tag]} -> {'met' if ok else 'NOT met'}")
        keep = {'U6': ('established', 'mixed'), 'U8': ('addresses',)}.get(tag, ('states', 'close'))
        for c in cs:
            if c['reading'] in keep:
                print(f"     {c['reading']:11} {c['source'][:88]} ({str(c['version'])[:24]})")
    print(f"declared expectations met: {hit} of {len(U)}")
    print()
    print('Global figures in the sweep (tag G):')
    for c in CLAIMS:
        if c['tag'] == 'G':
            print(f"  {c['id']:6} {c.get('value', float('nan')):>14g} {c.get('unit', ''):28} {c.get('year', '')} | {c['source'][:70]}")


if __name__ == '__main__':
    main()
