"""Check that every quote in claims.py is a verbatim substring of its saved raw text (run by hand; output pinned).

Raw texts were saved by the literature agents in the session scratchpad (not committed: third-party full texts).
Normalisation: html-unescape, removal of U+FFFE / U+00AD and of '-\n' joins, whitespace collapsed.
Run: python3 AI_Safety/CORRIGIBILITY_2026/checks/verify_claims.py <raw-root>
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib  # noqa: E402


def norm(s):
    s = html.unescape(s).replace('￾', '').replace('­', '')
    s = re.sub(r'-\n', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def main():
    root = sys.argv[1]
    C = importlib.import_module(sys.argv[2] if len(sys.argv) > 2 else 'claims')
    cache, found, total, miss = {}, 0, 0, []
    for c in C.CLAIMS:
        p = os.path.join(root, c['raw_file'])
        if p not in cache:
            cache[p] = norm(open(p, encoding='utf-8', errors='replace').read()) if os.path.exists(p) else None
        for q in c['quote']:
            total += 1
            ok = cache[p] is not None and norm(q) in cache[p]
            found += ok
            if not ok:
                miss.append((c['id'], q[:70]))
    print(f'quotes found verbatim: {found} of {total} (claims {len(C.CLAIMS)})')
    for m in miss:
        print('  NOT FOUND', m)


if __name__ == '__main__':
    main()
