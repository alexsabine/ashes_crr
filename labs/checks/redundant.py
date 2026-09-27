"""The redundant rows of the retrodictive bank (REDUNDANT-DOMAIN and REDUNDANT-IG), by theme, each with the CRR ingredient
it used and the domain's own result it landed on (prompt-log entry 225). Reads pinned text only; every outcome is the row's
own (R15); the theme map is labs/checks/themes.py's.

    python3 labs/checks/redundant.py > labs/checks/redundant.txt
"""
import collections
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank as B  # noqa: E402
import themes as T  # noqa: E402

CUT = 200


def rows_full(path):
    """bank.rows plus the ingredient and domain fields."""
    name = os.path.splitext(os.path.basename(path))[0]
    cur = None
    for line in open(path, encoding='utf-8'):
        m = re.match(r'^\[ ?(\d+)\] \((\S+)\) (.*)$', line.rstrip('\n'))
        if m:
            if cur:
                yield cur
            cur = {'file': name, 'row': int(m.group(1)), 'tag': m.group(2), 'system': m.group(3)}
            continue
        if cur is None:
            continue
        m = re.match(r'^\s+(ingredient|domain|OUTCOME):\s+(.*)$', line.rstrip('\n'))
        if m:
            cur[m.group(1)] = m.group(2).strip()
    if cur:
        yield cur


def c(s):
    s = s or ''
    return s if len(s) <= CUT else s[:CUT - 3] + '...'


def main():
    files = [os.path.join(B.RET, 'synthesis.txt')] + sorted(glob.glob(os.path.join(B.RET, 'synthesis_batches', 'batch_[0-9][0-9].txt')))
    rows = [r for f in files for r in rows_full(f) if r.get('OUTCOME', '').startswith('REDUNDANT')]
    n = collections.Counter(r['OUTCOME'] for r in rows)
    print('Redundant rows of the retrodictive bank, by theme (labs/checks/redundant.py; prompt-log entry 225)')
    print(f"rows {len(rows)}: REDUNDANT-DOMAIN {n['REDUNDANT-DOMAIN']} (a CRR-proper ingredient moved the number and landed on the "
          f"domain's own result), REDUNDANT-IG {n['REDUNDANT-IG']} (the CRR ingredient did no work: its null gives the same number)")
    ing = collections.Counter()
    for r in rows:
        for k in ('A3', 'A6', 'A1', 'H-L5', 'P1', 'P2', 'P3', 'P5', 'D6', 'H-EQ', 'A7', 'A8', 'O3'):
            if re.search(r'(^|[^A-Za-z0-9-])' + re.escape(k) + r'(?![0-9])', r.get('ingredient', '')):
                ing[k] += 1
    print('ingredients named on the redundant rows (a row may name several): ' + ', '.join(f'{k} {v}' for k, v in ing.most_common()))
    print()
    for name, _ in T.THEMES:
        rs = [r for r in rows if T.theme_of(r) == name]
        if not rs:
            continue
        print(f'== {name} ({len(rs)})')
        for r in rs:
            print(f"  [{r['file']} row {r['row']}] {r['OUTCOME']} | {c(r['system'])}")
            print(f"      ingredient: {c(r.get('ingredient'))}")
            print(f"      domain already has: {c(r.get('domain'))}")
        print()


if __name__ == '__main__':
    main()
