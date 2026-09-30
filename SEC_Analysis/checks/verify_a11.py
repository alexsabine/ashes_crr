"""SEC_Analysis A11 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f): check that every quote in claims_a11.py appears in its
extracted source text (run by hand; output pinned in verify_a11.txt). POST HOC; no ledger row.

The extracted texts were saved outside the repository (third-party full texts, not committed), under
/tmp/claude-0/sec_an_src/; each claim's `raw_file` is relative to that root (sha256 in SHA256SUMS.txt there).
Normalisation (copied from Open_Bottlenecks/checks/verify.py), applied to quote and text alike: Unicode NFKC; whitespace
collapsed to one space. A hyphen at a line break in the text may be read either as kept ("exemplar-free") or as a rejoin
("stabilityplasticity"), independently at each break. A quote containing "[...]" is checked fragment by fragment. A raw
file that is missing prints MISSING for each of its quotes and is never counted as found.
It ends with the sha256 of every raw file it read. Deterministic, stdlib only. Run: uv run python SEC_Analysis/checks/verify_a11.py [raw-root] > SEC_Analysis/checks/verify_a11.txt
"""
import hashlib
import os
import re
import sys
import unicodedata

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from claims_a11 import CLAIMS  # noqa: E402

ROOT = '/tmp/claude-0/sec_an_src'
BRK = '\x00'  # marks a line-break hyphen in the normalised text


def norm_text(t):
    t = unicodedata.normalize('NFKC', t)
    t = re.sub(r'(\w)-[ \t]*\n\s*(\w)', lambda m: m.group(1) + BRK + m.group(2), t)
    return re.sub(r'\s+', ' ', t).strip()


def norm_quote(q):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', q)).strip()


def pattern(frag):
    """Regex for a fragment: each hyphen may be a line-break hyphen; a line-break hyphen may sit between two word chars."""
    out = []
    for i, ch in enumerate(frag):
        if ch == '-':
            out.append('(?:-|' + BRK + ')')
            continue
        out.append(re.escape(ch))
        if ch.isalnum() and i + 1 < len(frag) and frag[i + 1].isalnum():
            out.append(BRK + '?')
    return ''.join(out)


def found(frag, text):
    if frag in text.replace(BRK, '-') or frag in text.replace(BRK, ''):
        return True
    return re.search(pattern(frag), text) is not None


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else ROOT
    cache, n_found, n_total, n_missing, bad = {}, 0, 0, 0, []
    ids = [c['id'] for c in CLAIMS]
    assert len(ids) == len(set(ids)), 'duplicate claim ids'
    print('SEC_Analysis A11: verbatim check of every quote in claims_a11.py against its extracted source text')
    print('POST HOC; no ledger row. Sources fetched 2026-09-30 (versions in claims_a11.py)')
    print(f'root: {root}')
    for c in CLAIMS:
        p = os.path.join(root, c['raw_file'])
        if p not in cache:
            cache[p] = norm_text(open(p, encoding='utf-8', errors='replace').read()) if os.path.isfile(p) else None
        text = cache[p]
        for i, q in enumerate(c['quote']):
            n_total += 1
            if text is None:
                status = 'MISSING'
                n_missing += 1
            else:
                frags = [f for f in (norm_quote(x) for x in norm_quote(q).split('[...]')) if f]
                status = 'PASS' if frags and all(found(f, text) for f in frags) else 'NOT FOUND'
            n_found += status == 'PASS'
            if status != 'PASS':
                bad.append((status, c['id'], i, q[:70]))
            print(f"{status:9} {c['id']:7} {c['ingredient']} {c['role']:11} quote {i} {c['raw_file']}")
    print()
    print(f'quotes found verbatim: {n_found} of {n_total} (claims {len(CLAIMS)}; raw files {len(cache)}, '
          f'missing {sum(v is None for v in cache.values())}); not found {n_total - n_found - n_missing}; '
          f'missing {n_missing}')
    for status, cid, i, q in bad:
        print(f'  {status} {cid} quote {i}: {q}')
    print()
    print('raw files read (sha256 of the extracted text as read now; the fetch record is FETCH_LOG.txt in the root):')
    for rf in sorted({c['raw_file'] for c in CLAIMS}):
        p = os.path.join(root, rf)
        h = hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.isfile(p) else 'MISSING'
        print(f'  {h}  {rf}')


if __name__ == '__main__':
    main()
