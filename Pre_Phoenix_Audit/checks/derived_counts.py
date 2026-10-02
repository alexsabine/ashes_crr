"""PRE-PHOENIX INTERPRETIVE AUDIT — NO VERDICTS ALTERED.

Prints the counts the lineage notes derived by hand (marked 'auditor's count (derived)'), so that the audit report quotes
only numbers a committed script prints (R1). It reads pinned outputs and the ledger; it writes nothing and runs nothing.

    uv run python Pre_Phoenix_Audit/checks/derived_counts.py > Pre_Phoenix_Audit/checks/derived_counts.txt

Every section names the file it reads. A count here is a reading of pinned numbers, not a re-score: no verdict changes.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(rel):
    return (ROOT / rel).read_text().splitlines()


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


SOURCES = [
    "ledger/LEDGER.md",
    "Epistemic_Review/checks/ladder.txt",
    "Predictions70/checks/tally.txt",
    "runs/t1x2/score.txt",
    "SEC_Analysis/checks/m_checks.txt",
    "SEC_Analysis/checks/gate_posthoc.txt",
    "prereg/sec7/dev/gate7.txt",
    "Continuous_Learning/checks/results_vs_literature.txt",
    "Relational_Reference_Memory/checks/t1_seen.txt",
    "Coupling/checks/cpl_phase_a.txt",
    "Pre_Phoenix_Audit/checks/outcome_classes.txt",
    "Pre_Phoenix_Audit/notes/PROCESS.md",
    "data/manifests/eq2r.sha256",
    "data/manifests/t1x.sha256",
    "data/manifests/bayes1.sha256",
    "data/manifests/sec6.sha256",
]


def f(x):
    return f"{x:+.4f}"


def d1_ladder_passes():
    print("[D1] Held-out PASS rows by lineage (Epistemic_Review/checks/ladder.txt, the rung R6 and R7 lines)")
    line = [x for x in read("Epistemic_Review/checks/ladder.txt") if "rung R6 PASS-0 on held-out data" in x][0]
    r6 = re.search(r"held-out data: (\d+) \(([^)]*)\)", line)
    ids = [s.strip() for s in r6.group(2).split(",")]
    r7 = re.search(r"R7 PASS-1: (\d+) \(([^)]*)\)", line)
    sec = [i for i in ids if i.startswith(("SCL3-", "SEC"))]
    eq = [i for i in ids if i.startswith(("EQ2-", "EQ3-", "EQ4-"))]
    other = [i for i in ids if i not in sec and i not in eq]
    print(f"   R6 PASS-0 rows: {r6.group(1)} (parsed {len(ids)})")
    print(f"   SEC family (SCL3-*, SEC*): {len(sec)} {sec}")
    print(f"   EQ family (EQ2-*, EQ3-*, EQ4-*): {len(eq)} {eq}")
    print(f"   other: {len(other)} {other}")
    print(f"   R7 PASS-1: {r7.group(1)} ({r7.group(2)})")


def d2_rlaw():
    print("\n[D2] RLAW rows (ledger/LEDGER.md; excluded from the ladder by the owner's instruction, prompt-log entry 139)")
    rows = [x for x in read("ledger/LEDGER.md") if x.startswith("| RLAW-")]
    fails = []
    for r in rows:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        verdict = cells[-3].replace("**", "")
        if verdict.startswith("FAIL") and "no counted verdict" not in verdict:
            fails.append(cells[0])
    print(f"   RLAW rows {len(rows)}; verdict starting FAIL (excluding 'no counted verdict') {len(fails)}: {fails}")


def d3_pred70():
    print("\n[D3] PRED70 rows the harness labels REDUNDANT whose prediction Q fails (Predictions70/checks/tally.txt)")
    lines = read("Predictions70/checks/tally.txt")
    hdr = [x for x in lines if x.lstrip().startswith("id ") and " outcome " in x][0]
    co, cf, ch, cq, cd = (hdr.index(k) for k in (" outcome", " forecast", " hit", " Q ", " dev"))
    out = []
    for x in lines:
        if re.match(r"\s+P\d\d-\d\s", x):
            outcome, q = x[co:cf].strip(), x[cq:cd].strip()
            if outcome in ("REDUNDANT-IG", "REDUNDANT-DOMAIN"):
                out.append((x.split()[0], outcome, q))
    red = len(out)
    failed = [i for i, _, q in out if q == "fails"]
    print(f"   REDUNDANT rows parsed {red}; Q held {sum(q == 'holds' for _, _, q in out)}; Q fails {len(failed)}: {failed}")


def d4_t1x2():
    print("\n[D4] T1x2: best path against the weaker endpoint comparators (runs/t1x2/score.txt, the T1x-1 lines)")
    carrier = None
    worse_new = worse_ewc = n = 0
    for x in read("runs/t1x2/score.txt"):
        m = re.match(r"\[(\S+)\]", x)
        if m:
            carrier = m.group(1)
        if "T1x-1 held-out R^2" in x:
            v = dict(re.findall(r"(C_new|C_old|E_new|E_old|ewc):(-?\d+\.\d+)", x))
            v = {k: float(s) for k, s in v.items()}
            best_path = max(v["C_new"], v["C_old"])
            dn, de = best_path - v["E_new"], best_path - v["ewc"]
            n += 1; worse_new += dn <= -0.05; worse_ewc += de < 0
            print(f"   {carrier:22} best path {best_path:.3f}  E_new {v['E_new']:.3f}  ewc {v['ewc']:.3f}  "
                  f"path - E_new {dn:+.3f}  path - ewc {de:+.3f}")
    print(f"   path - E_new <= -0.05 on {worse_new}/{n}; path behind ewc on {worse_ewc}/{n}")


def d5_sec_subset():
    print("\n[D5] SEC: carriers on which the do-nothing control (M6 / edge) is BEHIND the tuned lambda")
    print("   (a) P1 mechanism runs (SEC_Analysis/checks/m_checks.txt, second table; C0 - tuned = (M6 - tuned) - (M6 - C0);")
    print("       the M6-behind set is the '*' marks of SEC_Analysis/checks/gate_posthoc.txt). POST HOC, carriers now SEEN.")
    lines = read("SEC_Analysis/checks/m_checks.txt")
    h = [i for i, x in enumerate(lines) if "M6-tuned    M6-C0" in x][0]
    table = {}
    for x in lines[h + 1:]:
        m = re.match(r"(\w+)\s+(\S+)\s+(\d+\.\d+) \|.*\|\s*(-?\+?\d+\.\d+)\*?\s+(-?\+?\d+\.\d+)\s*$", x)
        if not m:
            break
        table[m.group(2)] = (float(m.group(3)), float(m.group(4)), float(m.group(5)))
    behind = []
    for x in read("SEC_Analysis/checks/gate_posthoc.txt"):
        behind += re.findall(r"(\S+) -?\+?\d+\.\d+ \(step \d+\.\d+\)\*", x)
    nb = 0
    for c in behind:
        step, m6t, m6c0 = table[c]
        c0t = m6t - m6c0
        nb += c0t > -step
        print(f"      {c:22} M6 - tuned {f(m6t)}  C0 - tuned {f(c0t)} (step {step:.3f}) -> {'not behind' if c0t > -step else 'BEHIND'}")
    print(f"      clipped SEC (C0) not behind on {nb}/{len(behind)} of the carriers where M6 is behind")
    print("   (b) SEC7 development, SEEN, random class order, balanced accuracy (prereg/sec7/dev/gate7.txt); development, not evidence")
    tot = nb7 = ah7 = 0; ahead = []
    for x in read("prereg/sec7/dev/gate7.txt"):
        m = re.search(r"\[(\S+)\].*step (\d+\.\d+);.*edge \S+ \((-?\+?\d+\.\d+): BEHIND\); clipped SEC \S+ \((-?\+?\d+\.\d+): (not behind|BEHIND)\)", x)
        if m:
            tot += 1; d = float(m.group(4)); nb7 += m.group(5) == "not behind"
            if d > float(m.group(2)):
                ah7 += 1; ahead.append(m.group(1))
    print(f"      edge BEHIND on {tot}; clipped SEC not behind on {nb7}/{tot}; ahead by more than its step on {ah7}/{tot} {ahead}")


def d6_eq_margins():
    print("\n[D6] H-EQ rule (Omega = 1) against the in-sample tuned EWC lambda on the LOAD-BEARING carriers of EQ2-EQ4")
    print("   (Continuous_Learning/checks/results_vs_literature.txt; margin = 'rule O=1' - 'EWC tuned'; a report line, no verdict)")
    study = None; pos = []; neg = []
    lines = read("Continuous_Learning/checks/results_vs_literature.txt")
    for i, x in enumerate(lines):
        m = re.match(r"== (\S+)", x)
        if m:
            study = m.group(1)
        m = re.match(r"\s+(\S+): K .*\|\|\s+(\S+) \|\s+(\S+) \(\S+\) \|\s+(\S+) \|", x)
        if m and study in ("EQ2", "EQ3", "EQ4") and "load-bearing" in lines[i + 1]:
            d = float(m.group(4)) - float(m.group(3))
            (pos if d > 0 else neg).append((m.group(1), d))
    g = lambda d: f"{d:+.2f}"  # noqa: E731  (the table prints two decimals; the ledger rows carry more)
    print(f"   load-bearing carriers {len(pos) + len(neg)}; rule ahead {len(pos)}: " + ", ".join(f"{c} {g(d)}" for c, d in pos))
    print(f"   rule behind {len(neg)}: " + ", ".join(f"{c} {g(d)}" for c, d in neg))
    mfeat = [c for c, _ in pos if c.startswith("mfeat_")]
    print(f"   of the carriers where the rule is ahead, mfeat_* (one 2000-digit record set, prereg/scl3/PREREG.md) {len(mfeat)}/{len(pos)}")


def d7_rrm_drift():
    print("\n[D7] Kept-anchor transport on the SEEN carriers where there is drift to fix (report lines only; post hoc; SEEN)")
    rep = [x for x in read("Coupling/checks/cpl_phase_a.txt") if x.startswith("REPORT under FT: ORACLE ahead of STALE")][0]
    drift = re.findall(r"'([^']+)'", rep)
    print(f"   drift-to-fix carriers (Coupling/checks/cpl_phase_a.txt REPORT under FT): {drift}")
    rows = {}
    for x in read("Relational_Reference_Memory/checks/t1_seen.txt"):
        m = re.match(r"\s+(\S+)\s+(FT|ANCH1|ER20)\s+(\S+)\s+(\S+)\s", x)
        if m:
            rows[(m.group(1), m.group(2))] = float(m.group(4))
    for learner in ("FT", "ANCH1"):
        vals = [(c, rows[(c, learner)]) for c in drift if (c, learner) in rows]
        print(f"   {learner}: NCM RRM - STALE (Relational_Reference_Memory/checks/t1_seen.txt, 'summary' block): "
              + ", ".join(f"{c} {f(v)}" for c, v in vals) + f" -> positive on {sum(v > 0 for _, v in vals)}/{len(vals)} (no step printed)")


def d8_timing():
    print("\n[D8] Request -> hash and hash -> score (Pre_Phoenix_Audit/checks/outcome_classes.txt [8]; commit times)")
    lines = read("Pre_Phoenix_Audit/checks/outcome_classes.txt")
    i0 = [i for i, x in enumerate(lines) if x.startswith("[8]")][0]
    named = []; within = []
    for x in lines[i0 + 2:]:
        if not x.startswith("    ") or x.startswith("    'prev"):
            break
        m = re.match(r"\s+(\S+)\s+PL \d+ .*?\s(\d+\.\d+) min\s", x)
        if m:
            named.append((m.group(1), float(m.group(2))))
            if float(m.group(2)) <= 25.0:
                within.append(m.group(1))
    print(f"   studies with a named request prompt {len(named)}; hashed within 25 min of the prompt's header time {len(within)}: {within}")
    print("   others: " + ", ".join(f"{n} {t} min" for n, t in named if t > 25.0))
    print("   (a lower bound on receipt -> hash: prompt header times from entry 57 on are logging times, outcome_classes.txt [8] note)")
    prev = []
    for x in lines[i0 + 2:]:
        if not x.startswith("    ") or x.startswith("    'prev"):
            break
        m = re.search(r"(\d+\.\d+) h\s+(\d+\.\d+) h\s*$", x)
        if m:
            prev.append((x.split()[0], float(m.group(2))))
    under = [n for n, h in prev if h < 24.0]
    print(f"   'prev score->hash' defined on {len(prev)} rows (table order, not lineage order); under 24 h on {len(under)}; "
          f"range {min(h for _, h in prev):.2f} to {max(h for _, h in prev):.2f} h; over 24 h: "
          + ", ".join(f"{n} {h:.2f} h" for n, h in prev if h >= 24.0))


def d9_consumed():
    print("\n[D9] Held-out carriers fetched for studies whose primary verdict was VOID or NOT DECIDABLE (data/manifests/*.sha256)")
    tot = 0
    for study, row in (("eq2r", "EQ2R-VOID"), ("t1x", "T1X-VOID"), ("bayes1", "BAYES1-B0"), ("sec6", "SEC6-1")):
        files = [x.split()[1] for x in read(f"data/manifests/{study}.sha256") if x.strip()]
        carriers = sorted({Path(f).name.split(".")[0] for f in files})
        tot += len(carriers)
        print(f"   {study:7} ({row}): {len(carriers)} carriers")
    print(f"   total {tot}")


def d10_gates():
    print("\n[D10] Gates closed before confirmatory data (Pre_Phoenix_Audit/notes/PROCESS.md section 3(a) table; the reason class")
    print("      is the process reader's JUDGEMENT; this only tallies the table as written)")
    lines = read("Pre_Phoenix_Audit/notes/PROCESS.md")
    i0 = [i for i, x in enumerate(lines) if x.startswith("### 3(a)")][0]
    i1 = [i for i, x in enumerate(lines) if x.startswith("### 3(b)")][0]
    rows = [x for x in lines[i0:i1] if re.match(r"\| \d+ \|", x)]
    print(f"   gates in the table: {len(rows)}")
    oc = [x for x in read("Pre_Phoenix_Audit/checks/outcome_classes.txt") if x.strip().startswith("GATE CLOSED (before data) (")][0]
    n_gate = re.search(r"\((\d+)\):", oc).group(1)
    print(f"   the ledger's own GATE CLOSED rows (outcome_classes.txt [3]): {n_gate}")


def d11_late_instrument():
    print("\n[D11] Held-out VOID / NOT DECIDABLE / UNINFORMATIVE rows by when the study was first scored")
    print("      (outcome_classes.txt [7] cells; first-score commit dates from outcome_classes.txt [8])")
    lines = read("Pre_Phoenix_Audit/checks/outcome_classes.txt")
    i7 = [i for i, x in enumerate(lines) if x.startswith("[7]")][0]
    i8 = [i for i, x in enumerate(lines) if x.startswith("[8]")][0]
    cells = {}
    for x in lines[i7 + 1:i8]:
        m = re.match(r"\s+(\S+)\s+rows\s+\d+ \|(.*)", x)
        if m:
            n = sum(int(k) for c, k in re.findall(r"(VOID|NOT DECIDABLE|UNINFORMATIVE) (\d+)", m.group(2)))
            cells[m.group(1)] = n
    first = {}
    for x in lines[i8 + 2:]:
        m = re.match(r"\s+(\S+)\s+.*?\s(\w{7}) (2026-\d\d-\d\d)T\S+\s+\d+\.\d+ h", x)
        if m:
            first[m.group(1).upper().replace("-", "")] = m.group(3)
    late = early = 0
    for k, n in cells.items():
        d = first.get(k.upper().replace("-", ""))
        if d is None:
            print(f"   {k}: {n} (no first-score date matched; counted as early)")
            early += n
        elif d >= "2026-09-25":
            late += n
        else:
            early += n
    print(f"   first scored on or after 2026-09-25: {late}; before: {early}; total {late + early}")


def main():
    print("PRE-PHOENIX INTERPRETIVE AUDIT — NO VERDICTS ALTERED: derived counts (Pre_Phoenix_Audit/checks/derived_counts.py)")
    print("reads pinned outputs and the ledger; writes nothing; every count is a reading, not a re-score")
    for s in SOURCES:
        print(f"   {s} sha256 {sha(s)}")
    print()
    d1_ladder_passes(); d2_rlaw(); d3_pred70(); d4_t1x2(); d5_sec_subset(); d6_eq_margins(); d7_rrm_drift(); d8_timing(); d9_consumed(); d10_gates(); d11_late_instrument()


if __name__ == "__main__":
    main()
