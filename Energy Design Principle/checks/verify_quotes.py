"""Check that every quote in energy_rows.py is a verbatim substring of its saved raw text (run by hand; output pinned).

The raw texts were saved by the literature agents in the session scratchpad (not committed: third-party full texts).
Normalisation: html-unescape, removal of U+FFFE / U+00AD and of '-\n' hyphenation joins, whitespace collapsed.
Run: python3 "Energy Design Principle/checks/verify_quotes.py" <raw-root>
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import energy_rows as R  # noqa: E402


def norm(s):
    s = html.unescape(s).replace('￾', '').replace('­', '')
    s = re.sub(r'-\n', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def main():
    root = sys.argv[1]
    cache, found, total, missing = {}, 0, 0, []
    for i, r in enumerate(R.ROWS):
        p = os.path.join(root, r['raw_file'])
        if p not in cache:
            cache[p] = norm(open(p, encoding='utf-8', errors='replace').read()) if os.path.exists(p) else None
        for q in r['quote']:
            total += 1
            ok = cache[p] is not None and norm(q) in cache[p]
            found += ok
            if not ok:
                missing.append((i, r['mech'], r['source'][:40], q[:60]))
    print(f'quotes found verbatim: {found} of {total} (rows {len(R.ROWS)})')
    for m in missing:
        print('  NOT FOUND', m)


if __name__ == '__main__':
    main()
