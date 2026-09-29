"""EPS1 tally (Empty_Pause_Systems/DECLARATION.md; prompt-log entry 240): reads the pinned batch outputs eps1_01.txt..eps1_04.txt.
Per system: the gate line (G-ZERO, G-POS, G-NEG; OPEN or CLOSED, as computed by the batch), the harness OUTCOME of its row,
whether CRR's prediction Q held (the T-C line ends '-> Q holds' / '-> Q fails' / '-> not computable'), and whether the
investigator's forecast (REDUNDANT-DOMAIN for all seven, declared at 37b0076) was right. Rows of a system whose gate is
CLOSED are printed and not counted (DECLARATION.md). Written before any batch output existed.
Run: python3 Empty_Pause_Systems/checks/tally.py
"""
import collections
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
LABELS = ("ADDS", "PROPOSES", "REDUNDANT-IG", "REDUNDANT-DOMAIN", "WRONG", "INTERNAL", "UNSTATED")
SYSTEMS = {"S1": "approval gates for tool-using agents", "S2": "reporting to an overseer", "S3": "safe interruptibility in learning",
           "S4": "preemptible (spot) compute", "S5": "restorative breaks on a work platform", "S6": "trading halts (the limit case)",
           "S7": "resuming a controller after an operator pause"}
FORECAST = {s: "REDUNDANT-DOMAIN" for s in SYSTEMS}


def main():
    print("EPS1 tally: the empty-true-map pause on seven systems (Empty_Pause_Systems/DECLARATION.md, pushed at 37b0076)")
    gates = {}; rows = {}; missing = []
    for n in range(1, 5):
        f = os.path.join(ROOT, f'Empty_Pause_Systems/batches/eps1_{n:02d}.txt')
        if not os.path.exists(f):
            missing.append(os.path.basename(f)); continue
        txt = open(f).read()
        for s, body, verdict in re.findall(r"^GATE (S\d): (.*) -> (OPEN|CLOSED)\s*$", txt, re.M):
            gates[s] = (verdict, body)
        for block in re.split(r"\n(?=\[\s*\d+\] )", txt):
            m = re.search(r"source:\s+EPS1 (S\d)", block)
            if not m:
                continue
            oc = re.search(r"OUTCOME:\s+(\S+)", block)[1]
            tc = re.search(r"T-C:\s+(.*)", block)[1].rstrip()
            q = 'holds' if tc.endswith('-> Q holds') else ('fails' if tc.endswith('-> Q fails') else ('not computable' if tc.endswith('-> not computable') else 'UNPARSED'))
            dev = 'DEVIATION' in block or 'CHOICE' in block
            rows[m[1]] = (oc, q, dev)
    if missing:
        print(f"missing batch outputs: {missing}")
    print()
    print(f"  {'sys':4} {'gate':7} {'outcome':17} {'forecast':17} {'hit':4} {'Q':15} choices  system")
    for s, name in SYSTEMS.items():
        g = gates.get(s, ("(none)", ""))[0]
        if s not in rows:
            print(f"  {s:4} {g:7} {'(no row)':17} {FORECAST[s]:17} {'-':4} {'-':15} -        {name}"); continue
        oc, q, dev = rows[s]
        print(f"  {s:4} {g:7} {oc:17} {FORECAST[s]:17} {'yes' if oc == FORECAST[s] else 'no':4} {q:15} {'yes' if dev else '-':8} {name}")
    print()
    for s in SYSTEMS:
        if s in gates:
            print(f"  GATE {s}: {gates[s][1]} -> {gates[s][0]}")
    counted = [s for s in rows if gates.get(s, ("CLOSED",))[0] == "OPEN"]
    closed = [s for s in SYSTEMS if gates.get(s, ("(none)",))[0] != "OPEN"]
    oc = collections.Counter(rows[s][0] for s in counted); qc = collections.Counter(rows[s][1] for s in counted)
    print()
    print(f"systems with a row {len(rows)} of {len(SYSTEMS)}; gate OPEN and counted {len(counted)}; gate CLOSED or absent (not counted) {len(closed)}: {closed}")
    print("outcomes (counted):  " + ", ".join(f"{l} {oc[l]}" for l in LABELS))
    print(f"CRR's prediction Q held in the system's own model (counted): {qc['holds']} of {len(counted)}; failed {qc['fails']}; "
          f"not computable {qc['not computable']}" + (f"; UNPARSED {qc['UNPARSED']}" if qc['UNPARSED'] else ''))
    hit = sum(rows[s][0] == FORECAST[s] for s in counted)
    print(f"the investigator's forecast (REDUNDANT-DOMAIN) was right on {hit} of {len(counted)} counted rows")
    print(f"declared expectation 'ETM does what it is built to do (G-ZERO) in S1-S5 and S7, and fails as predicted in S6': "
          + ("holds" if all(gates.get(s, ("",))[0] == "OPEN" and "G-ZERO holds" in gates[s][1] for s in SYSTEMS) else "see the gate lines"))


if __name__ == '__main__':
    main()
