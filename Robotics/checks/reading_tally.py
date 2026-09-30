"""ROB1 stage 2 (Robotics/DECLARATION.md): the tally of Robotics/CRR_READING.md's reading column, computed (R15), with a
check that the rows are exactly the OPEN and CONTESTED bottlenecks of stage 1b (table.py's labels).
Deterministic, stdlib only. Run: python3 Robotics/checks/reading_tally.py
"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def main():
    md = open(os.path.join(HERE, '..', 'CRR_READING.md'), encoding='utf-8').read()
    rows = [ln for ln in md.splitlines() if re.match(r'^\| r\d-B\d', ln)]
    reading = {}
    for ln in rows:
        cells = [c.strip() for c in ln.strip('|').split('|')]
        rid = cells[0].split()[0]; lab = cells[-1]
        if lab.startswith('**DISAGREES'): k = 'DISAGREES (candidate)'
        elif lab.startswith('DISAGREES, already failed'): k = 'DISAGREES, already failed in the record'
        elif lab.startswith('RESTATES'): k = 'RESTATES'
        elif lab.startswith('SILENT'): k = 'SILENT'
        else: k = 'UNPARSED: ' + lab
        reading[rid] = k
    tab = open(os.path.join(HERE, 'table.txt'), encoding='utf-8').read()
    staged = {m.group(1) for m in re.finditer(r'^(r\d-B\d)\s+(OPEN \(double-checked\)|CONTESTED)', tab, re.M)}
    print('ROB1 stage 2: the CRR reading tallied from Robotics/CRR_READING.md; rows must be the OPEN and CONTESTED bottlenecks of table.txt')
    print(f'rows read {len(reading)}; OPEN or CONTESTED in table.txt {len(staged)}; missing from the reading {sorted(staged - set(reading))}; '
          f'extra in the reading {sorted(set(reading) - staged)}')
    c = collections.Counter(reading.values())
    for k in ('DISAGREES (candidate)', 'DISAGREES, already failed in the record', 'RESTATES', 'SILENT'):
        print(f'   {k:42} {c.get(k, 0):3}  ' + ' '.join(sorted(r for r, v in reading.items() if v == k)))
    for k in sorted(k for k in c if k.startswith('UNPARSED')):
        print(f'   {k} {c[k]}')
    n_dis = c.get('DISAGREES (candidate)', 0)
    print(f'forecast 2 (at most 3 read DISAGREES): {n_dis} -> {"holds" if n_dis <= 3 else "FAILS"}')


if __name__ == '__main__':
    main()
