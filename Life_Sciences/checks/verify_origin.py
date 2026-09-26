"""Check every quote in claims_origin.py verbatim (whitespace collapsed) against its saved raw text in the session scratchpad.
The raw texts are not committed (as for AI_Safety/CORRIGIBILITY_2026); this output is pinned as verify_origin.txt.
    python3 Life_Sciences/checks/verify_origin.py <scratchpad dir> > Life_Sciences/checks/verify_origin.txt
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims_origin as C  # noqa: E402


def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def main(root):
    rows = [(c, q) for c in C.CLAIMS for q in c['quote']] + [(c, q) for c in C.DS4['claims'] for q in c['quote']]
    ok, bad = 0, []
    cache = {}
    for c, q in rows:
        f = os.path.join(root, c['raw_file'])
        if f not in cache:
            cache[f] = norm(open(f, encoding='utf-8', errors='replace').read())
        if norm(q) in cache[f]:
            ok += 1
        else:
            bad.append((c['raw_file'], q[:80]))
    print(f'quotes found verbatim: {ok} of {len(rows)} (claims {len(C.CLAIMS)} OL-1 + {len(C.DS4["claims"])} DS-4; '
          f'raw files {len(cache)})')
    for b in bad:
        print('  NOT FOUND', b)


if __name__ == '__main__':
    main(sys.argv[1])
