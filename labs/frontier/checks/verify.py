"""Check every quote in claims.py verbatim (whitespace collapsed) against its saved raw text in the session scratchpad.
    python3 labs/frontier/checks/verify.py <scratchpad dir> > labs/frontier/checks/verify.txt
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims as C  # noqa: E402


def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def main(root):
    ok, bad, cache = 0, [], {}
    rows = [(c, q) for c in C.CLAIMS for q in c['quote'] if q]
    for c, q in rows:
        f = os.path.join(root, c['raw_file'])
        if f not in cache:
            cache[f] = norm(open(f, encoding='utf-8', errors='replace').read())
        if norm(q) in cache[f]:
            ok += 1
        else:
            bad.append((c['id'], q[:70]))
    print(f'quotes found verbatim: {ok} of {len(rows)} (claims {len(C.CLAIMS)}; raw files {len(cache)})')
    for b in bad:
        print('  NOT FOUND', b)


if __name__ == '__main__':
    main(sys.argv[1])
