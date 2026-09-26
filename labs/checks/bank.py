"""The retrodictive bank as the labs' starting index (prompt-log entry 220): every SYNTHESIS row in the pinned outputs
theory/retrodictions/synthesis.txt and theory/retrodictions/synthesis_batches/batch_NN.txt, with its domain tag, its
source class (CONSIST / DESCR where the source row names one), its outcome, the literature-check status of the ADDS rows
(theory/retrodictions/synthesis_batches/literature_check.txt), its Q and its weakness (where a lab would start).
Nothing is computed from data; the script reads pinned text only, and every label is the row's own (R15).

    python3 labs/checks/bank.py > labs/checks/bank.txt
"""
import collections
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RET = os.path.join(ROOT, 'theory', 'retrodictions')
CUT = 240


def rows(path):
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
        m = re.match(r'^\s+(source|Q|OUTCOME|weakness):\s+(.*)$', line.rstrip('\n'))
        if m:
            cur[m.group(1)] = m.group(2).strip()
    if cur:
        yield cur


def lit_status():
    out, key = {}, None
    for line in open(os.path.join(RET, 'synthesis_batches', 'literature_check.txt'), encoding='utf-8'):
        m = re.match(r'^\[ ?\d+\] (batch_\d+) row (\d+):', line)
        if m:
            key = (m.group(1), int(m.group(2)))
        m = re.match(r'^\s+STATUS:\s+(.*)$', line)
        if m and key:
            out[key] = m.group(1).strip()
    return out


def cut(s):
    s = s or ''
    return s if len(s) <= CUT else s[:CUT - 3] + '...'


def main():
    files = [os.path.join(RET, 'synthesis.txt')] + sorted(glob.glob(os.path.join(RET, 'synthesis_batches', 'batch_[0-9][0-9].txt')))
    lit = lit_status()
    allrows = [r for f in files for r in rows(f)]
    print('The retrodictive bank: every SYNTHESIS row, as pinned (labs/checks/bank.py; prompt-log entry 220)')
    print(f'files {len(files)}, rows {len(allrows)}')
    tally = collections.Counter(r.get('OUTCOME', '?') for r in allrows)
    print('outcomes: ' + ', '.join(f'{k} {v}' for k, v in sorted(tally.items())))
    src = collections.Counter(m.group(1) for r in allrows for m in [re.search(r'\((CONSIST|DESCR)\)', r.get('source', ''))] if m)
    print('source classes named on the rows: ' + ', '.join(f'{k} {v}' for k, v in sorted(src.items())))
    litc = collections.Counter(lit.values())
    print('ADDS literature check: ' + ', '.join(f'{k}: {v}' for k, v in sorted(litc.items())))
    print()
    for lab in ('ADDS', 'PROPOSES', 'WRONG', 'INTERNAL', 'UNSTATED', 'REDUNDANT-DOMAIN', 'REDUNDANT-IG'):
        rs = [r for r in allrows if r.get('OUTCOME') == lab]
        print(f'==== {lab} ({len(rs)})')
        for r in rs:
            m = re.search(r'\((CONSIST|DESCR)\)', r.get('source', ''))
            extra = f" | literature: {lit[(r['file'], r['row'])]}" if (r['file'], r['row']) in lit else ''
            print(f"[{r['file']} row {r['row']}] ({r['tag']}) {cut(r['system'])}")
            print(f"    source class: {m.group(1) if m else 'not named'}{extra}")
            print(f"    Q: {cut(r.get('Q'))}")
            print(f"    edge (weakness): {cut(r.get('weakness'))}")
        print()


if __name__ == '__main__':
    main()
