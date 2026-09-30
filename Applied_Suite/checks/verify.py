"""APP1 stage C (Applied_Suite/APPLICATIONS_DECLARATION.md): check that every quote in claims_m1.py ... claims_m3.py appears in its extracted source text (run by hand; output pinned in verify.txt).

The extracted texts were saved by the literature agents outside the repository (third-party full texts, not committed),
under /tmp/claude-0/app1_src/; each claim's `raw_file` is relative to that root.
Normalisation, applied to quote and text alike: Unicode NFKC; whitespace collapsed to one space. A hyphen at a line break
in the text may be read either as kept ("exemplar-free") or as a rejoin ("stabilityplasticity"), independently at each
break. A quote containing "[...]" is checked fragment by fragment. A raw file that is missing prints MISSING for each of
its quotes and is never counted as found. Each raw file's sha256 is also checked against the entry for it in its
family's SHA256SUMS.txt (<root>/m1..m3/SHA256SUMS.txt, written by the literature agents at fetch time). Quotes corrected or dropped after a first NOT FOUND are listed in each claims
module's VERIFY_CORRECTIONS; this script counts them and prints them, and never edits a claim.
Normalisation and matching are copied from Open_Bottlenecks/checks/verify.py.
Deterministic, stdlib only. Run: python3 Applied_Suite/checks/verify.py [raw-root]
"""
import hashlib
import importlib
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

FAMILIES = ('m1', 'm2', 'm3')
MODULES = {f: importlib.import_module(f'claims_{f}') for f in FAMILIES}


class C:
    CLAIMS = [c for f in FAMILIES for c in MODULES[f].CLAIMS]
    CORRECTIONS = [(f, x) for f in FAMILIES for x in getattr(MODULES[f], 'VERIFY_CORRECTIONS', [])]


ROOT = '/tmp/claude-0/app1_src'
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


def sums(root):
    """Every (path relative to root) -> sha256 listed in the families' SHA256SUMS.txt."""
    out = {}
    for f in FAMILIES:
        p = os.path.join(root, f, 'SHA256SUMS.txt')
        if not os.path.isfile(p):
            continue
        for line in open(p, encoding='utf-8'):
            if line.strip():
                h, name = line.rstrip('\n').split(None, 1)
                out[os.path.normpath(os.path.join(f, name.strip()))] = h
    return out


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else ROOT
    cache, n_found, n_total, n_missing, bad = {}, 0, 0, 0, []
    per_fam = {f: [0, 0] for f in FAMILIES}
    print('APP1 claims: verbatim check of every quote against its extracted source text')
    print(f'root: {root}')
    ids = [c['id'] for c in C.CLAIMS]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    for c in C.CLAIMS:
        fam = c['id'].split(':')[0]
        p = os.path.join(root, c['raw_file'])
        if p not in cache:
            cache[p] = norm_text(open(p, encoding='utf-8', errors='replace').read()) if os.path.isfile(p) else None
        text = cache[p]
        for i, q in enumerate(c['quote']):
            n_total += 1
            per_fam[fam][1] += 1
            if text is None:
                status = 'MISSING'
                n_missing += 1
            else:
                frags = [f for f in (norm_quote(x) for x in norm_quote(q).split('[...]')) if f]
                status = 'PASS' if frags and all(found(f, text) for f in frags) else 'NOT FOUND'
            n_found += status == 'PASS'
            per_fam[fam][0] += status == 'PASS'
            if status != 'PASS':
                bad.append((status, c['id'], i, q[:70]))
            print(f"{status:9} {c['id']:6} {c['application']:7} {c['role']:20} quote {i} {c['raw_file']}")
    print()
    for f in FAMILIES:
        nc = sum(c['id'].split(':')[0] == f for c in C.CLAIMS)
        print(f'family {f}: claims {nc}; quotes found {per_fam[f][0]} of {per_fam[f][1]}')
    listed = sums(root)
    raws = sorted({c['raw_file'] for c in C.CLAIMS})
    n_listed = n_match = 0
    unmatched = []
    for r in raws:
        p = os.path.join(root, r)
        h = listed.get(os.path.normpath(r))
        n_listed += h is not None
        ok = h is not None and os.path.isfile(p) and hashlib.sha256(open(p, 'rb').read()).hexdigest() == h
        n_match += ok
        if not ok:
            unmatched.append(r + (' (not listed)' if h is None else ' (sha256 differs or file missing)'))
    print(f'raw files cited: {len(raws)}; listed in SHA256SUMS.txt {n_listed}; sha256 matches {n_match}')
    for r in unmatched:
        print(f'  SHA256 {r}')
    print(f'duplicate claim ids: {len(dup)}' + (f' ({", ".join(dup)})' if dup else ''))
    n_corr = sum(x['action'] == 'corrected' for _, x in C.CORRECTIONS)
    n_drop = sum(x['action'] == 'dropped' for _, x in C.CORRECTIONS)
    print(f'verify corrections recorded (VERIFY_CORRECTIONS): {len(C.CORRECTIONS)} (corrected {n_corr}, dropped {n_drop})')
    for f, x in C.CORRECTIONS:
        print(f"  {f} {x['id']} quote {x['quote_index']}: {x['action']}")
    print(f'quotes found verbatim: {n_found} of {n_total} (claims {len(C.CLAIMS)}; raw files {len(cache)}, '
          f'missing {sum(v is None for v in cache.values())}); not found {n_total - n_found - n_missing}; '
          f'missing {n_missing}')
    for status, cid, i, q in bad:
        print(f'  {status} {cid} quote {i}: {q}')


if __name__ == '__main__':
    main()
