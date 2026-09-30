"""ROB1 stage 4b tally (Robotics/DECLARATION_4B.md, pushed at d44e713; prompt-log entry 257): reads the pinned batch outputs
Robotics/batches/rob_01.txt .. rob_05.txt and tallies the harness OUTCOME of each declared application RA1-RA10.

Per row: the OUTCOME printed by the batch (computed there by the harness's outcome(), R15), the investigator's per-row forecast
as declared, whether the forecast was right, whether CRR's prediction Q held in the row's own model (read from the T-C line:
'-> Q holds' / '-> Q fails' / '-> not computable'; a T-C line that starts 'not scored' reads 'not scored'), whether the row
names CHOICES, and whether it records a change after a first run or a review ('CHANGE AFTER' / 'CHANGED AFTER' in the block).
Each batch's own TALLY line is recomputed from the parsed rows by the harness's tally_line and compared.

The declaration's overall forecast, each clause computed from the labels:
  F1  at least 8 of 10 rows read REDUNDANT-DOMAIN or REDUNDANT-IG;
  F2  at most 1 row reads ADDS, and it would be RA6;
  F3  WRONG is possible for RA1: scored literally, RA1's label is one of its declared pair {REDUNDANT-DOMAIN, WRONG};
      the stronger reading (no row other than RA1 reads WRONG) is printed with its own verdict and not scored.
The overall forecast HOLDS only if F1, F2 and F3 all hold. A missing row counts against F1 and is a miss per row.

Stdlib and the harness only; deterministic. This script was written after the five batch outputs existed; the forecasts are
the declaration's (d44e713), typed from it, not read from the outputs.
Run: uv run python Robotics/checks/tally_4b.py
"""
import collections
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
try:
    from crr.synthesis.harness import LABELS, tally_line
except ImportError:  # plain python3 from a checkout without the installed package
    sys.path.insert(0, os.path.join(ROOT, 'src'))
    from crr.synthesis.harness import LABELS, tally_line

BATCHES = [f"rob_{n:02d}.txt" for n in range(1, 6)]
REDUNDANT = ("REDUNDANT-DOMAIN", "REDUNDANT-IG")
# id: (the application, the robotics quantity the batch prints, the declared per-row forecast), from DECLARATION_4B.md
APPS = {
    "RA1": ("gait phase and the cut", "stopping or cutting error", ("REDUNDANT-DOMAIN", "WRONG")),
    "RA2": ("odometry drift has its own clock", "drift per km", ("REDUNDANT-DOMAIN",)),
    "RA3": ("charging as a cut on the robot's own state", "uptime per day", ("REDUNDANT-DOMAIN",)),
    "RA4": ("lost link and the empty cut", "mission value lost to avoidance", ("REDUNDANT-DOMAIN",)),
    "RA5": ("fleet update and rollback as a state-closed cut", "restore fidelity", ("REDUNDANT-DOMAIN",)),
    "RA6": ("event-triggered attitude control", "updates saved (energy and bandwidth)", ("REDUNDANT-DOMAIN", "ADDS")),
    "RA7": ("actuator wear by arc", "maintenance interval spread", ("REDUNDANT-DOMAIN",)),
    "RA8": ("swarm consensus with intermittent links", "rounds to consensus", ("REDUNDANT-DOMAIN",)),
    "RA9": ("handover timing on the partner's phase", "handover timing error", ("REDUNDANT-DOMAIN",)),
    "RA10": ("safe interruptibility of a learning robot", "policy distance under interruption", ("REDUNDANT-DOMAIN",)),
}


def verdict(ok):
    return "HOLDS" if ok else "FAILS"


def q_of(tc):
    if tc.startswith("not scored"):
        return "not scored"
    ends = re.findall(r"-> (Q holds|Q fails|not computable)", tc)
    if not ends:
        return "UNPARSED"
    return {"Q holds": "holds", "Q fails": "fails", "not computable": "not computable"}[ends[-1]]


def main():
    print("ROB1 stage 4b tally: ten robotics applications through the SYNTHESIS harness (Robotics/DECLARATION_4B.md, pushed at d44e713)")
    print("CHOICES: the pinned outputs read are rob_01.txt .. rob_05.txt exactly (a kept first run such as rob_03_run1.txt is not read); "
          "a row is found by 'source: ROB1 [4b ]RAn'; F3 is scored on its literal reading (RA1's label within its declared pair), "
          "the stronger reading (WRONG nowhere but RA1) printed, not scored")
    rows = {}; dup = []; missing = []; batch_checks = []; src_mismatch = []
    for name in BATCHES:
        f = os.path.join(ROOT, "Robotics", "batches", name)
        if not os.path.exists(f):
            missing.append(name); continue
        txt = open(f, encoding="utf-8").read()
        here = []
        for block in re.split(r"\n(?=\[\s*\d+\] )", txt):
            m = re.search(r"^\s+source:\s+ROB1 (?:4b )?(RA\d+)\b(.*)$", block, re.M)
            if not m:
                continue
            rid = m.group(1)
            oc = re.search(r"^\s+OUTCOME:\s+(\S+)", block, re.M).group(1)
            tc = re.search(r"^\s+T-C:\s+(.*)$", block, re.M).group(1).rstrip()
            fc = re.search(r"forecast ([A-Z-]+(?: or [A-Z-]+)*)", m.group(2))
            if fc is None or tuple(fc.group(1).split(" or ")) != APPS.get(rid, (None, None, ()))[2]:
                src_mismatch.append(rid)
            rec = dict(outcome=oc, q=q_of(tc), choices="CHOICE" in block, changed=bool(re.search(r"CHANGED? AFTER", block)),
                       batch=name[:-4])
            if rid in rows:
                dup.append(rid)
            rows[rid] = rec
            here.append(rec)
        printed = re.findall(r"^TALLY: .*$", txt, re.M)
        recomputed = tally_line(here)
        batch_checks.append((name[:-4], [r for r in APPS if r in rows and rows[r]["batch"] == name[:-4]],
                             bool(printed) and printed[-1] == recomputed))
    print(f"batch outputs read {len(BATCHES) - len(missing)} of {len(BATCHES)}" + (f"; missing {missing}" if missing else ""))
    for b, ids, ok in batch_checks:
        print(f"  {b}: rows {', '.join(ids) if ids else '(none)'}; its TALLY line recomputed by the harness's tally_line from the parsed rows: "
              + ("agrees" if ok else "DISAGREES"))
    extra = sorted(set(rows) - set(APPS))
    if dup or extra or src_mismatch:
        print(f"  duplicate rows {dup}; rows not declared {extra}; rows whose source line's forecast differs from the declaration {src_mismatch}")
    else:
        print("  no duplicate or undeclared row; every row's source line states the declared forecast")
    bad = sorted(r for r in rows if rows[r]["outcome"] not in LABELS)
    if bad:
        print(f"  OUTCOME not a harness label in {bad}")
    print()
    print(f"  {'row':5} {'outcome':17} {'forecast (declared)':27} {'hit':4} {'Q':15} {'choices':8} {'changed':8} {'batch':7} application; robotics quantity")
    for rid, (app, qty, fc) in APPS.items():
        if rid not in rows:
            print(f"  {rid:5} {'(no row)':17} {' or '.join(fc):27} {'no':4} {'-':15} {'-':8} {'-':8} {'-':7} {app}; {qty}"); continue
        r = rows[rid]
        print(f"  {rid:5} {r['outcome']:17} {' or '.join(fc):27} {'yes' if r['outcome'] in fc else 'no':4} {r['q']:15} "
              f"{'yes' if r['choices'] else '-':8} {'yes' if r['changed'] else '-':8} {r['batch']:7} {app}; {qty}")
    print()
    n = len(APPS)
    got = [r for r in APPS if r in rows]
    oc = collections.Counter(rows[r]["outcome"] for r in got)
    qc = collections.Counter(rows[r]["q"] for r in got)
    print(f"rows with an OUTCOME {len(got)} of {n}")
    print("outcomes:  " + ", ".join(f"{lab} {oc[lab]}" for lab in LABELS))
    for lab in LABELS:
        ids = [r for r in got if rows[r]["outcome"] == lab]
        if ids:
            print(f"  {lab:17} {', '.join(ids)}")
    print(f"CRR's prediction Q held in the row's own model (T-C line): {qc['holds']} of {len(got)}; failed {qc['fails']}; "
          f"not computable {qc['not computable']}; not scored {qc['not scored']}" + (f"; UNPARSED {qc['UNPARSED']}" if qc['UNPARSED'] else ""))
    hit = [r for r in got if rows[r]["outcome"] in APPS[r][2]]
    print(f"the investigator's per-row forecast was right on {len(hit)} of {n} rows; missed on "
          + (", ".join(f"{r} ({rows[r]['outcome'] if r in rows else 'no row'})" for r in APPS if r not in hit) or "none"))
    print(f"rows naming CHOICES {sum(rows[r]['choices'] for r in got)} of {len(got)}; rows recording a change after a first run or a review "
          f"{sum(rows[r]['changed'] for r in got)} of {len(got)}: {', '.join(r for r in got if rows[r]['changed']) or 'none'}")
    print()
    red = [r for r in got if rows[r]["outcome"] in REDUNDANT]
    f1 = len(red) >= 8
    adds = [r for r in got if rows[r]["outcome"] == "ADDS"]
    f2 = len(adds) <= 1 and all(r == "RA6" for r in adds)
    ra1 = rows["RA1"]["outcome"] if "RA1" in rows else None
    f3 = ra1 in APPS["RA1"][2]
    wrong_else = [r for r in got if rows[r]["outcome"] == "WRONG" and r != "RA1"]
    notred = ", ".join(r + " " + rows[r]["outcome"] for r in got if r not in red) or "none"
    absent = ", ".join(r for r in APPS if r not in rows)
    print("the declaration's overall forecast (d44e713), computed:")
    print(f"  F1 at least 8 of 10 read REDUNDANT-DOMAIN or REDUNDANT-IG: {len(red)} of {n} ({', '.join(red) or 'none'}); "
          f"not redundant: {notred}" + (f"; no row: {absent}" if absent else "") + f" -> {verdict(f1)}")
    print(f"  F2 at most 1 reads ADDS, and it would be RA6: ADDS {len(adds)} ({', '.join(adds) or 'none'}) -> {verdict(f2)}")
    print(f"  F3 WRONG is possible for RA1 (scored: RA1's label is REDUNDANT-DOMAIN or WRONG): RA1 reads {ra1 or '(no row)'} -> {verdict(f3)}")
    print(f"     not scored, the stronger reading (no row other than RA1 reads WRONG): WRONG elsewhere {', '.join(wrong_else) or 'none'} "
          f"-> {verdict(not wrong_else)}")
    failed = [k for k, ok in (("F1", f1), ("F2", f2), ("F3", f3)) if not ok]
    print(f"overall forecast: {verdict(not failed)}" + (f" (failed: {', '.join(failed)})" if failed else ""))
    robustness()


def robustness():
    """REPORT (added after the batches' reviews, 2026-09-30; decides nothing): whether each row's label survives the
    sensitivity readings its batch prints. RA2 and RA7 print a 40-seed sweep; RA4 prints its labels under three readings.
    A row whose label differs from the scored one in more than one printed cell is FRAGILE (CLAUDE.md's rule for a
    sensitivity table). Parsed from the pinned batch outputs; nothing is recomputed here."""
    txt = {b: open(os.path.join(ROOT, "Robotics", "batches", b), encoding="utf-8").read() for b in BATCHES}
    print()
    print("REPORT (added after the reviews; decides nothing): label robustness read from each batch's printed sensitivity")
    m = re.search(r"labels (?:are )?(\d+) ADDS, (\d+) REDUNDANT-DOMAIN: (\d+) of (\d+) differ from the scored label", txt["rob_01.txt"])
    if m:
        a, r, d, n = map(int, m.groups())
        print(f"  RA2  slip seeds 100-139: ADDS {a}, REDUNDANT-DOMAIN {r}; {d} of {n} differ from the scored label -> "
              f"{'FRAGILE' if d > 1 else 'not fragile'} (where T-N misses it misses on sampling noise, T-C holds)")
    else:
        print("  RA2  seed sweep line NOT FOUND")
    seeds = re.findall(r"^  seed (\d+): .*; (\S+)$", txt["rob_04.txt"], re.M)
    if seeds:
        c = collections.Counter(l for _, l in seeds)
        print(f"  RA7  duty seeds {seeds[0][0]}-{seeds[-1][0]}: " + ", ".join(f"{k} {v}" for k, v in sorted(c.items()))
              + f"; differ from REDUNDANT-DOMAIN (the scored label) {sum(v for k, v in c.items() if k != 'REDUNDANT-DOMAIN')} of {len(seeds)} -> "
              + ("FRAGILE" if sum(v for k, v in c.items() if k != 'REDUNDANT-DOMAIN') > 1 else "not fragile"))
    else:
        print("  RA7  seed sweep lines NOT FOUND")
    m = re.search(r"^RA4 READING-DEPENDENT.*$", txt["rob_02.txt"], re.M)
    print("  RA4  " + ("READING-DEPENDENT (the batch prints the labels by reading; see rob_02.txt)" if m else "no reading flag printed"))
    print("  reading: a stochastic row's T-N at the harness's 1 % relative tolerance can miss on sampling noise alone; where it"
          " misses and T-C holds, the harness reads ADDS. Such an ADDS is a tolerance artefact, not a CRR addition.")


if __name__ == "__main__":
    main()
