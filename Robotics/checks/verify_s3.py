"""ROB1 stage 3 (Robotics/DECLARATION.md; candidates C-R1..C-R3 of Robotics/CRR_READING.md): check that every quote in
claims_s3_r1a.py ... claims_s3_r3b.py (searchers A and B for each candidate) appears in its extracted source text (run by hand;
output pinned in verify_s3.txt).

The extracted texts were saved by the literature agents outside the repository (third-party full texts, not committed),
under /tmp/claude-0/rob_s3/; each claim's `raw_file` is relative to that root.
Normalisation and matching are copied unchanged from Open_Bottlenecks/checks/verify_s3.py, applied to quote and text alike:
Unicode NFKC; whitespace collapsed to one space. A hyphen at a line break in the text may be read either as kept
("exemplar-free") or as a rejoin ("stabilityplasticity"), independently at each break. A quote containing "[...]" is checked
fragment by fragment. A raw file that is missing prints MISSING for each of its quotes and is never counted as found.
Each cited extracted text's sha256 is also checked against its entry in the searcher's <root>/<module>/SHA256SUMS.txt
(written by the literature agents at fetch time); a mismatch is printed and does not change a quote's status.
Quotes corrected or dropped after a first NOT FOUND are listed in each claims module's VERIFY_CORRECTIONS; this script counts
them and prints them, and never edits a claim. Robotics/checks/grade_s3.py imports `claim_status` from here, so only quotes
this script finds count towards a grade.
Deterministic, stdlib only. Run: python3 Robotics/checks/verify_s3.py [raw-root]
"""
import hashlib
import importlib
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MODULES = ('r1a', 'r1b', 'r2a', 'r2b', 'r3a', 'r3b')
ROOT = '/tmp/claude-0/rob_s3'
BRK = '\x00'  # marks a line-break hyphen in the normalised text


def load(mods=MODULES):
    return {f: importlib.import_module(f'claims_s3_{f}') for f in mods}


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
    """PASS, NOT FOUND or MISSING (text None) for one quote against one normalised text."""
    if text is None:
        return 'MISSING'
    frags = [f for f in (norm_quote(x) for x in norm_quote(q).split('[...]')) if f]
    return 'PASS' if frags and all(found(f, text) for f in frags) else 'NOT FOUND'


def claim_status(claims, root=ROOT):
    """Per claim id, the status of each of its quotes, in order; raw files are read once each."""
    cache, out = {}, {}
    for c in claims:
        p = os.path.join(root, c['raw_file'])
        if p not in cache:
            cache[p] = norm_text(open(p, encoding='utf-8', errors='replace').read()) if os.path.isfile(p) else None
        out[c['id']] = [quote_status(q, cache[p]) for q in c['quote']]
    return out, cache


def sums(root, mods=MODULES):
    """Every (path relative to root) -> sha256 listed in the searchers' SHA256SUMS.txt."""
    out = {}
    for f in mods:
        p = os.path.join(root, f, 'SHA256SUMS.txt')
        if not os.path.isfile(p):
            continue
        for line in open(p, encoding='utf-8'):
            if line.strip():
                h, name = line.rstrip('\n').split(None, 1)
                out[os.path.normpath(os.path.join(f, name.strip().lstrip('*')))] = h
    return out


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else ROOT
    mods = load()
    claims = [c for f in MODULES for c in mods[f].CLAIMS]
    corrections = [(f, x) for f in MODULES for x in getattr(mods[f], 'VERIFY_CORRECTIONS', [])]
    status, cache = claim_status(claims, root)
    n_found = n_total = n_missing = 0
    per_mod = {f: [0, 0] for f in MODULES}
    bad = []
    print('ROB1 stage 3 claims: verbatim check of every quote against its extracted source text')
    print(f'root: {root}')
    print(f'modules: {", ".join("claims_s3_" + f for f in MODULES)}')
    for c in claims:
        f = c['id'].split(':')[0]
        for i, (q, s) in enumerate(zip(c['quote'], status[c['id']])):
            n_total += 1
            per_mod[f][1] += 1
            n_found += s == 'PASS'
            per_mod[f][0] += s == 'PASS'
            n_missing += s == 'MISSING'
            if s != 'PASS':
                bad.append((s, c['id'], i, q[:70]))
            print(f"{s:9} {c['id']:7} {c['position']} {c['reading']:11} quote {i} {c['raw_file']}")
    print()
    for f in MODULES:
        nc = sum(c['id'].split(':')[0] == f for c in claims)
        print(f'module {f}: claims {nc}; quotes found {per_mod[f][0]} of {per_mod[f][1]}')
    ids = [c['id'] for c in claims]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    print(f'duplicate claim ids: {len(dup)}' + (f' ({", ".join(dup)})' if dup else ''))
    listed = sums(root)
    raws = sorted({c['raw_file'] for c in claims})
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
    print(f'extracted texts cited: {len(raws)}; listed in SHA256SUMS.txt {n_listed}; sha256 matches {n_match}')
    for r in unmatched:
        print(f'  SHA256 {r}')
    n_corr = sum(x['action'] == 'corrected' for _, x in corrections)
    n_drop = sum(x['action'] == 'dropped' for _, x in corrections)
    print(f'verify corrections recorded (VERIFY_CORRECTIONS): {len(corrections)} (corrected {n_corr}, dropped {n_drop})')
    for f, x in corrections:
        print(f"  {f} {x['id']} quote {x['quote_index']}: {x['action']}")
    print(f'quotes found verbatim: {n_found} of {n_total} (claims {len(claims)}; raw files {len(cache)}, '
          f'missing {sum(v is None for v in cache.values())}); not found {n_total - n_found - n_missing}; '
          f'missing {n_missing}')
    for s, cid, i, q in bad:
        print(f'  {s} {cid} quote {i}: {q}')


if __name__ == '__main__':
    main()
