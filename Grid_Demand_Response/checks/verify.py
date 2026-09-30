"""Check that every quote in claims.py appears verbatim in its raw_file (the dossier's extracted text of the fetched source).

The raw texts were saved by the literature agents outside the repository (/tmp/claude-0/dr1_src/F1..F5/; third-party full
texts, not committed). A quote is split at "[...]" (the dossier's marked omissions) and every fragment is searched in the raw
text after the dossiers' declared normalisation (docs/citations/dr1_f1..f5_2026-09-29.md, "Quote rules"):
  - HTML entities unescaped; U+200B (zero-width space) and U+00A0 read as spaces; U+00AD (soft hyphen) and U+FFFE removed;
  - whitespace collapsed; the space that tag stripping leaves before , . ; : ) ] and after ( [ removed;
  - a line-break hyphen between two word characters either rejoined ("toler-\\nance" -> "tolerance") or kept as a genuine
    hyphen ("time-\\nconsuming" -> "time-consuming"); both variants of the raw text are searched.
Match modes, in order: 'exact' (found with no hyphen treatment needed), 'rejoined', 'kept', and a last-resort
'hyphen-insensitive' (all whitespace and hyphens removed from both sides), which is reported separately and counted as found.
A raw file that does not exist is reported MISSING and its fragments are never counted as found.
Deterministic; stdlib only. Run: cd /home/user/ashes_crr && uv run python Grid_Demand_Response/checks/verify.py [raw-root]
(raw-root, if given, replaces the prefix /tmp/claude-0/dr1_src of every raw_file.)
"""
import collections
import hashlib
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims as C  # noqa: E402

DEFAULT_ROOT = '/tmp/claude-0/dr1_src'
MODES = ('exact', 'rejoined', 'kept', 'hyphen-insensitive')


def norm(s):
    s = html.unescape(s)
    s = s.replace('​', ' ').replace(' ', ' ').replace('­', '').replace('￾', '')
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r' ([,.;:)\]])', r'\1', s)
    s = re.sub(r'([(\[]) ', r'\1', s)
    return s.strip()


def squash(s):
    return re.sub(r'[\s\-]', '', s)


HYPHEN_BREAK = re.compile(r'(?<=\w)-[ \t]*\n\s*(?=\w)')


def load(path, cache):
    if path not in cache:
        if not os.path.exists(path):
            cache[path] = None
        else:
            raw = open(path, encoding='utf-8', errors='replace').read()
            with open(path, 'rb') as f:
                digest = hashlib.sha256(f.read()).hexdigest()
            plain = norm(raw)
            rejoined = norm(HYPHEN_BREAK.sub('', raw))
            kept = norm(HYPHEN_BREAK.sub('-', raw))
            cache[path] = (plain, rejoined, kept, squash(plain), digest)
    return cache[path]


def match(fragment, texts):
    plain, rejoined, kept, squashed, _ = texts
    f = norm(fragment)
    if f in plain:
        return 'exact'
    if f in rejoined:
        return 'rejoined'
    if f in kept:
        return 'kept'
    if squash(f) in squashed:
        return 'hyphen-insensitive'
    return None


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ROOT
    cache, modes, lines = {}, collections.Counter(), []
    n_quotes = n_frag = n_notfound = n_missing = 0
    for c in C.CLAIMS:
        path = c['raw_file'].replace(DEFAULT_ROOT, root, 1)
        texts = load(path, cache)
        cm, missed = collections.Counter(), []
        for q in c['quote']:
            n_quotes += 1
            for frag in q.split('[...]'):
                if not frag.strip():
                    continue
                n_frag += 1
                if texts is None:
                    cm['MISSING'] += 1
                    continue
                m = match(frag, texts)
                cm[m or 'NOT FOUND'] += 1
                if m is None:
                    missed.append(f"    NOT FOUND {c['id']}: {norm(frag)[:100]}")
        modes.update(cm)
        n_notfound += cm['NOT FOUND']
        n_missing += cm['MISSING']
        status = 'MISSING' if cm['MISSING'] else ('NOT FOUND' if cm['NOT FOUND'] else 'found')
        detail = ', '.join(f'{k} {cm[k]}' for k in MODES + ('NOT FOUND', 'MISSING') if cm[k])
        lines.append(f"  {c['id']:6} {status:9} quotes {len(c['quote'])}, fragments {sum(cm.values())} ({detail}) "
                     f"{os.path.relpath(path, root)}")
        lines.extend(missed)
    print('DR1 section 1: verbatim check of every quote in claims.py against its raw_file')
    print(f'raw root: {root}')
    print(f'claims {len(C.CLAIMS)}; quotes {n_quotes}; fragments (split at "[...]") {n_frag}')
    print('fragments by mode: ' + ', '.join(f'{k} {modes[k]}' for k in MODES)
          + f'; NOT FOUND {n_notfound}; MISSING {n_missing}')
    found = n_frag - n_notfound - n_missing
    verdict = 'ALL FOUND' if found == n_frag and n_frag > 0 else 'NOT ALL FOUND'
    print(f'quotes verified: {found} of {n_frag} fragments found; {verdict}')
    print()
    print('per claim:')
    for ln in lines:
        print(ln)
    print()
    print('raw files read (sha256 of the file as read):')
    for path in sorted(cache):
        t = cache[path]
        print(f"  {t[4] if t else 'MISSING':64} {os.path.relpath(path, root)}")


if __name__ == '__main__':
    main()
