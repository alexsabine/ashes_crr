"""OB1 (Open_Bottlenecks/DECLARATION.md): check that every quote in claims_h1.py ... claims_h4.py appears in its extracted source text (run by hand; output pinned in verify.txt).

The extracted texts were saved by the literature agent outside the repository (third-party full texts, not committed),
under /tmp/claude-0/ob1_src/; each claim's `raw_file` is relative to that root.
Normalisation, applied to quote and text alike: Unicode NFKC; whitespace collapsed to one space. A hyphen at a line break
in the text may be read either as kept ("exemplar-free") or as a rejoin ("stabilityplasticity"), independently at each
break. A quote containing "[...]" is checked fragment by fragment. A raw file that is missing prints MISSING for each of
its quotes and is never counted as found.
Deterministic, stdlib only. Run: python3 Relational_Reference_Memory/checks/verify.py [raw-root]
"""
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib  # noqa: E402


class C:
    CLAIMS = [c for f in ('h1', 'h2', 'h3', 'h4') for c in importlib.import_module(f'claims_{f}').CLAIMS]

ROOT = '/tmp/claude-0/ob1_src'
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
    print('OB1 claims: verbatim check of every quote against its extracted source text')
    print(f'root: {root}')
    for c in C.CLAIMS:
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
            print(f"{status:9} {c['id']:6} {c['bottleneck']} {c['role']} quote {i} {c['raw_file']}")
    print()
    print(f'quotes found verbatim: {n_found} of {n_total} (claims {len(C.CLAIMS)}; raw files {len(cache)}, '
          f'missing {sum(v is None for v in cache.values())}); not found {n_total - n_found - n_missing}; '
          f'missing {n_missing}')
    for status, cid, i, q in bad:
        print(f'  {status} {cid} quote {i}: {q}')


if __name__ == '__main__':
    main()
