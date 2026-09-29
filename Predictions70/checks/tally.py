"""PRED70 tally (Predictions70/DECLARATION.md; prompt-log entry 234): reads the pinned batch outputs pred_01.txt..pred_14.txt
and compares each row with its declaration in declared.py. Per row: the harness outcome, whether CRR's prediction Q held in
the domain's own model (the T-C line ends '-> Q holds' / '-> Q fails' / '-> not computable'), and whether the investigator's
forecast of the outcome was right. The harness gate is read from theory/retrodictions/synthesis.txt (rows 1 and 2 must
read ADDS and WRONG). Beside it: the retrodictive bank's outcome shares (labs/checks/bank.txt).
Run: python3 Predictions70/checks/tally.py
"""
import collections
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'Predictions70'))
import declared  # noqa: E402

LABELS = ("ADDS", "PROPOSES", "REDUNDANT-IG", "REDUNDANT-DOMAIN", "WRONG", "INTERNAL", "UNSTATED")


def rows_of(path):
    txt = open(path).read()
    out = []
    for block in re.split(r"\n(?=\[\s*\d+\] )", txt):
        m = re.search(r"source:\s+PRED70 (P\d\d-\d)", block)
        if not m:
            continue
        oc = re.search(r"OUTCOME:\s+(\S+)", block)[1]
        tc = re.search(r"T-C:\s+(.*)", block)[1]
        q = 'holds' if tc.rstrip().endswith('-> Q holds') else ('fails' if tc.rstrip().endswith('-> Q fails') else
                                                              ('not computable' if tc.rstrip().endswith('-> not computable') else 'UNPARSED'))
        dev = 'DEVIATION' in block
        out.append((m[1], oc, q, dev))
    return out


def main():
    print('PRED70 tally: 70 declared predictions (Predictions70/DECLARATION.md, declared.py pushed at 8397478)')
    syn = open(os.path.join(ROOT, 'theory/retrodictions/synthesis.txt')).read()
    g = re.findall(r"OUTCOME:\s+(\S+)", syn)[:2]
    gate = g == ['ADDS', 'WRONG']
    print(f"harness gate (synthesis.txt rows 1, 2): {g[0]}, {g[1]} (need ADDS, WRONG) -> {'OPEN' if gate else 'CLOSED'}")
    decl = {p[0]: p for p in declared.P}
    got = {}
    missing_files = []
    for n in range(1, 15):
        f = os.path.join(ROOT, f'Predictions70/batches/pred_{n:02d}.txt')
        if not os.path.exists(f):
            missing_files.append(f'pred_{n:02d}.txt'); continue
        for rid, oc, q, dev in rows_of(f):
            got[rid] = (oc, q, dev)
    if missing_files:
        print(f"missing batch outputs: {missing_files}")
    print()
    print(f"  {'id':6} {'ingredient':16} {'outcome':17} {'forecast':17} {'hit':4} {'Q':15} dev  system")
    for rid, p in decl.items():
        if rid not in got:
            print(f"  {rid:6} {p[4][:16]:16} {'(no row)':17} {p[8]:17} {'-':4} {'-':15} -    {p[3][:60]}"); continue
        oc, q, dev = got[rid]
        print(f"  {rid:6} {p[4][:16]:16} {oc:17} {p[8]:17} {'yes' if oc == p[8] else 'no':4} {q:15} {'yes' if dev else '-':4} {p[3][:60]}")
    N = len(got)
    oc = collections.Counter(v[0] for v in got.values())
    qc = collections.Counter(v[1] for v in got.values())
    hit = sum(got[r][0] == decl[r][8] for r in got)
    fc = collections.Counter(decl[r][8] for r in decl)
    print()
    print(f"rows scored {N} of {len(decl)}; deviations flagged {sum(v[2] for v in got.values())}")
    print("outcomes:  " + ", ".join(f"{l} {oc[l]}" for l in LABELS))
    print("forecast:  " + ", ".join(f"{l} {fc[l]}" for l in LABELS))
    print(f"CRR's prediction Q held in the domain model: {qc['holds']} of {N}; failed {qc['fails']}; not computable {qc['not computable']}"
          + (f"; UNPARSED {qc['UNPARSED']}" if qc['UNPARSED'] else ''))
    adds = [r for r in got if got[r][0] == 'ADDS']
    print(f"held AND carried CRR content (ADDS): {len(adds)} of {N} ({', '.join(sorted(adds))})")
    red = sum(got[r][0] in ('REDUNDANT-IG', 'REDUNDANT-DOMAIN') for r in got)
    red_h = sum(got[r][0] in ('REDUNDANT-IG', 'REDUNDANT-DOMAIN') and got[r][1] == 'holds' for r in got)
    print(f"redundant (IG or DOMAIN): {red} of {N}, of which Q held {red_h}")
    print(f"the investigator's forecast of the outcome was right on {hit} of {N} ({hit / N:.4f})" if N else "no rows")
    by = collections.defaultdict(lambda: collections.Counter())
    for r in got:
        by[decl[r][4]][got[r][0]] += 1
    print("by ingredient: " + "; ".join(f"{k}: " + ", ".join(f"{l} {v}" for l, v in sorted(c.items())) for k, c in sorted(by.items())))
    exp = len(adds) < N / 3
    print(f"declared expectation 'fewer than a third hold AND carry CRR content (ADDS)': {len(adds)} < {N / 3:.2f} -> {'holds' if exp else 'MISSED'}")
    bank = open(os.path.join(ROOT, 'labs/checks/bank.txt')).read()
    m = re.search(r"outcomes: (.*)", bank)
    print(f"beside it, the retrodictive bank (166 rows): {m[1] if m else 'unread'}")


if __name__ == '__main__':
    main()
