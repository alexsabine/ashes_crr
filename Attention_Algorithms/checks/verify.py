"""Check that every quote in claims_f1-f3.py is a verbatim substring of its saved raw text (run by hand; output pinned).
Raw texts were saved by the literature agents in the session scratchpad (not committed: third-party texts).
Normalisation: html-unescape, removal of U+FFFE / U+00AD and of '-\\n' joins, whitespace collapsed.
Run: python3 Attention_Algorithms/checks/verify.py <scratchpad-root>
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims_f1, claims_f2, claims_f3  # noqa: E402,E401


def norm(s):
    s = html.unescape(s).replace('￾', '').replace('­', '')
    s = re.sub(r'-\n', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def main():
    root = sys.argv[1]
    cache, found, total, miss = {}, 0, 0, []
    for c in claims_f1.CLAIMS + claims_f2.CLAIMS + claims_f3.CLAIMS:
        p = os.path.join(root, c['raw_file'])
        if p not in cache:
            cache[p] = norm(open(p, encoding='utf-8', errors='replace').read()) if os.path.exists(p) else None
        for q in c['quote']:
            total += 1
            if cache[p] is not None and norm(q) in cache[p]:
                found += 1
            else:
                miss.append((c['id'], q[:80]))
    print(f'quotes verbatim in their saved texts: {found} of {total}')
    for i, q in miss:
        print(f'  MISSING {i}: {q}')


if __name__ == '__main__':
    main()
