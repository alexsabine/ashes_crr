"""ROB1 (Robotics/DECLARATION.md): check that every quote in claims_r1.py ... claims_r5.py (stage 1, the harvest) and
claims_r1x.py ... claims_r5x.py (stage 1b, the double check) appears in its extracted source text (run by hand; output
pinned in verify.txt).

The extracted texts were saved by the literature agents outside the repository (third-party full texts, not committed),
under /tmp/claude-0/rob_src/; each claim's `raw_file` is relative to that root.
Normalisation and matching are copied unchanged from Open_Bottlenecks/checks/verify.py, applied to quote and text alike:
Unicode NFKC; whitespace collapsed to one space. A hyphen at a line break in the text may be read either as kept
("exemplar-free") or as a rejoin ("stabilityplasticity"), independently at each break. A quote containing "[...]" is checked
fragment by fragment. A raw file that is missing prints MISSING for each of its quotes and is never counted as found.
Robotics/checks/table.py imports `claim_status` from here, so only quotes this script finds count towards a label.
Deterministic, stdlib only. Run: python3 Robotics/checks/verify.py [raw-root]
"""
import importlib
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MODULES = ('r1', 'r2', 'r3', 'r4', 'r5', 'r1x', 'r2x', 'r3x', 'r4x', 'r5x')
ROOT = '/tmp/claude-0/rob_src'
BRK = '\x00'  # marks a line-break hyphen in the normalised text


def load_claims():
    return [c for f in MODULES for c in importlib.import_module(f'claims_{f}').CLAIMS]


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


def quote_status(q, text):
    """FOUND, NOT FOUND or MISSING (text None) for one quote against one normalised text."""
    if text is None:
        return 'MISSING'
    frags = [f for f in (norm_quote(x) for x in norm_quote(q).split('[...]')) if f]
    return 'FOUND' if frags and all(found(f, text) for f in frags) else 'NOT FOUND'


def claim_status(claims, root=ROOT):
    """Per claim id, the status of each of its quotes, in order; raw files are read once each."""
    cache, out = {}, {}
    for c in claims:
        p = os.path.join(root, c['raw_file'])
        if p not in cache:
            cache[p] = norm_text(open(p, encoding='utf-8', errors='replace').read()) if os.path.isfile(p) else None
        out[c['id']] = [quote_status(q, cache[p]) for q in c['quote']]
    return out, cache


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else ROOT
    claims = load_claims()
    status, cache = claim_status(claims, root)
    n_found = n_total = n_missing = 0
    bad = []
    print('ROB1 claims: verbatim check of every quote against its extracted source text')
    print(f'root: {root}')
    print(f'modules: {", ".join("claims_" + f for f in MODULES)}')
    for c in claims:
        for i, (q, s) in enumerate(zip(c['quote'], status[c['id']])):
            n_total += 1
            n_found += s == 'FOUND'
            n_missing += s == 'MISSING'
            if s != 'FOUND':
                bad.append((s, c['id'], i, q[:70]))
            print(f"{s:9} {c['id']:7} {c['bottleneck']} {c['role']} quote {i} {c['raw_file']}")
    print()
    print(f'quotes found verbatim: {n_found} of {n_total} (claims {len(claims)}; raw files {len(cache)}, '
          f'missing {sum(v is None for v in cache.values())}); not found {n_total - n_found - n_missing}; '
          f'missing {n_missing}')
    for s, cid, i, q in bad:
        print(f'  {s} {cid} quote {i}: {q}')


if __name__ == '__main__':
    main()
