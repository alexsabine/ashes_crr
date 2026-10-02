"""Pre-Phoenix audit: a mechanical outcome class for every ledger row (read only; prompt-log entry 260).

This script ALTERS NOTHING. It reads ledger/LEDGER.md and imports Epistemic_Review/checks/ladder.py (unchanged) to
reuse its parser and its data-status rule, then prints, for every ledger row:
  * the row id;
  * its data status as ladder.py derives it (seen / held-out / synthetic; RLAW rows, which ladder.py skips at the
    owner's instruction, prompt-log entry 139, are printed as 'RLAW (outside ladder)');
  * ladder.py's own allocation (printed beside, never replaced);
  * a MECHANICAL outcome class computed from the verdict text by the first matching rule below;
  * two flags: INSTR (instrument / pipeline words in the verdict or in the prediction-to-per-unit cells) and GATE
    (a closed gate named anywhere in the verdict).

It then prints tallies (data status x class), the rows per class, and the rows carrying each flag word.
It is the denominator table for the ledger only. The retrodictive banks (batteries, synthesis, PRED70) are NOT counted
here; the audit notes quote them from Epistemic_Review/checks/ladder.txt and redundant_vs_fail.txt by line number.

    uv run python Pre_Phoenix_Audit/checks/outcome_classes.py > Pre_Phoenix_Audit/checks/outcome_classes.txt
"""
from __future__ import annotations

import collections
import contextlib
import hashlib
import importlib.util
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "ledger" / "LEDGER.md"
LADDER = ROOT / "Epistemic_Review" / "checks" / "ladder.py"

# The outcome-class rules, applied to the verdict text (the third cell from the end, '**' removed, as ladder.py reads it).
# First match wins. The brief's classes come first; classes the brief does not name are listed after them and printed
# under their own names (never folded into the brief's classes).
CLASS_RULES = (
    ("VOID", r"\bVOID\b"),
    ("GATE CLOSED (before data)", r"^GATE CLOSED"),
    ("UNINFORMATIVE", r"UNINFORMATIVE"),
    ("NOT DECIDABLE", r"NOT DECIDABLE"),
    ("PASS-1", r"^PASS-1"),
    ("PASS-0", r"^PASS-0|^PASS \(PASS-0"),
    ("FRAGILE", r"^(FRAGILE|fragile)|^PASS(?=.*FRAGILE)"),
    ("REDUCES / control violated / INERT (+IDLE)", r"^(REDUCES|VIOLATED|INERT|IDLE)"),
    ("construction", r"^holds(?=.*construction)"),
    ("PASS-other", r"^PASS|^as claimed|stays PASS-0"),
    ("report / no verdict", r"^report|^reported without verdict|no counted verdict"),
    ("FAIL", r"^FAIL"),
    # classes outside the brief's list
    ("other: control / reproduction holds", r"^holds"),
    ("other: not fragile (sensitivity)", r"^not fragile"),
    ("other: does not reduce", r"^(DOES NOT REDUCE|does not reduce)"),
    ("other: precondition met (DECIDABLE)", r"^(DECIDABLE|decidable)"),
    ("other: UNVERIFIABLE (R1)", r"^UNVERIFIABLE"),
    ("other: numbers reported / no baseline ahead", r"^(immaterial|metric matters|no published baseline)"),
)
BRIEF_CLASSES = [c for c, _ in CLASS_RULES if not c.startswith("other:")]
ALL_CLASSES = [c for c, _ in CLASS_RULES]

# INSTR flag: the brief's word list. Case-insensitive except VOID and STRING (upper case in the ledger's usage).
# 'crashed' is matched as crash/crashed/crashes; 'criterion cannot fail' is matched as 'cannot fail' because the ledger
# phrases it as "the criterion '<quoted criterion>' cannot fail" (RQM-A) and "'not behind the tuned lambda' cannot fail"
# (SEC7-A), which the literal phrase would miss.
INSTR_WORDS = (
    ("loader", r"(?i)\bloader\b"),
    ("crashed", r"(?i)\bcrash(ed|es)?\b"),
    ("VOID", r"\bVOID\b"),
    ("runner defect", r"(?i)runner defect|frozen runner"),
    ("STRING", r"\bSTRING\b"),
    ("could not act as agents", r"(?i)could not act as agents"),
    ("cannot fail", r"(?i)cannot fail"),
    ("no positive control", r"(?i)no positive control"),
    ("not a test of", r"(?i)not a test of"),
)
# Further words, the auditor's addition (printed separately; they do not set the INSTR flag).
EXTRA_WORDS = (
    ("defect", r"(?i)\bdefect"),
    ("design failure", r"(?i)design failure"),
    ("vacuous", r"(?i)\bvacuous\b"),
    ("TypeError", r"TypeError"),
    ("did not reach (optimiser)", r"(?i)did not reach the exact posterior"),
)
GATE_FLAG = r"(?i)gate[- ]?\w*\s+CLOSED|\bGC CLOSED|-G\s+CLOSED|GATE CLOSED"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_ladder():
    spec = importlib.util.spec_from_file_location("ladder_ro", LADDER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):          # ladder.ledger() prints its own section; it is not reproduced here
        rows = mod.ledger()
    return mod, rows


def ledger_rows():
    out = []
    for line in LEDGER.read_text().splitlines():
        if not re.match(r"^\| [A-Z]", line):       # ladder.py's own row test
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rid = cells[0]
        verdict = cells[-3].replace("**", "").strip()   # ladder.py's verdict cell
        body = " | ".join(cells[3:-3]).replace("**", "")  # prediction .. per-unit cells; '|' inside cells shifts columns,
        out.append((rid, verdict, body))                  # so they are joined rather than indexed
    return out


def classify(verdict: str) -> str:
    for name, pat in CLASS_RULES:
        if re.search(pat, verdict):
            return name
    raise SystemExit(f"unmatched verdict: {verdict[:100]}")


def words(text: str, table) -> list[str]:
    return [name for name, pat in table if re.search(pat, text)]


def main():
    mod, lrows = load_ladder()
    status = {rid: seen for rid, seen, _ in lrows}
    alloc = {rid: lab for rid, _, lab in lrows}
    rows = ledger_rows()
    crr2 = tuple(mod.CRR2_PREFIXES)

    print("PRE-PHOENIX AUDIT: mechanical outcome classes of every ledger row (Pre_Phoenix_Audit/checks/outcome_classes.py)")
    print("NO VERDICT ALTERED: the script reads ledger/LEDGER.md and imports Epistemic_Review/checks/ladder.py; it writes nothing.")
    print(f"ledger/LEDGER.md sha256 {sha(LEDGER)}")
    print(f"Epistemic_Review/checks/ladder.py sha256 {sha(LADDER)}")
    print()
    print("[0] Rules")
    print("  data status: ladder.py's rule (dataset cell '(Y)' -> held-out, '(N)' -> seen, 'synthetic' -> synthetic, else inherited")
    print("  within the study prefix); rows whose id starts with " + ", ".join(crr2) + " are skipped by ladder.py (prompt-log entry 139)")
    print("  and printed here as 'RLAW (outside ladder)'.")
    print("  verdict text: the third cell from the end with '**' removed (ladder.py's reading).")
    print("  outcome class: first matching rule (Python regular expressions on the verdict text):")
    for name, pat in CLASS_RULES:
        print(f"    {name:46s} {pat}")
    print("  INSTR flag (the brief's words; searched in the verdict and in the prediction-to-per-unit cells joined):")
    for name, pat in INSTR_WORDS:
        print(f"    {name:28s} {pat}")
    print("  extra words (auditor's addition; reported, do not set INSTR):")
    for name, pat in EXTRA_WORDS:
        print(f"    {name:28s} {pat}")
    print(f"  GATE flag: verdict matches {GATE_FLAG}")
    print()

    recs = []
    for rid, verdict, body in rows:
        st = "RLAW (outside ladder)" if rid.startswith(crr2) else status[rid]
        cls = classify(verdict)
        text = verdict + " || " + body
        iw = words(text, INSTR_WORDS)
        ew = words(text, EXTRA_WORDS)
        gate = bool(re.search(GATE_FLAG, verdict))
        recs.append(dict(rid=rid, st=st, alloc=alloc.get(rid, "(skipped by ladder.py)"), cls=cls, iw=iw, ew=ew, gate=gate,
                         verdict=verdict))

    print(f"[1] Every ledger row ({len(recs)} rows; ladder.py allocates {len(lrows)}, skips {len(recs) - len(lrows)})")
    print("    id | data status | ladder.py allocation | outcome class | flags")
    for r in recs:
        flags = []
        if r["iw"]: flags.append("INSTR[" + ",".join(r["iw"]) + "]")
        if r["gate"]: flags.append("GATE")
        if r["ew"]: flags.append("extra[" + ",".join(r["ew"]) + "]")
        print(f"    {r['rid']:22s} | {r['st']:21s} | {r['alloc']:52s} | {r['cls']:42s} | {' '.join(flags) or '-'}")
    print()

    statuses = ["held-out", "seen", "synthetic", "RLAW (outside ladder)"]
    tab = collections.Counter((r["st"], r["cls"]) for r in recs)
    print("[2] Tally: outcome class (rows) x data status (columns)")
    print(f"    {'class':46s} " + " ".join(f"{s[:10]:>10s}" for s in statuses) + f" {'all':>6s}")
    for c in ALL_CLASSES:
        n = [tab[(s, c)] for s in statuses]
        if sum(n) == 0: continue
        print(f"    {c:46s} " + " ".join(f"{k:10d}" for k in n) + f" {sum(n):6d}")
    tot = [sum(tab[(s, c)] for c in ALL_CLASSES) for s in statuses]
    print(f"    {'total':46s} " + " ".join(f"{k:10d}" for k in tot) + f" {sum(tot):6d}")
    nb = sum(1 for r in recs if r["cls"] in BRIEF_CLASSES)
    print(f"    rows in the brief's classes {nb}; rows in 'other:' classes {len(recs) - nb}")
    print()

    print("[3] Rows per class (in ledger order)")
    for c in ALL_CLASSES:
        ids = [r["rid"] for r in recs if r["cls"] == c]
        if not ids: continue
        print(f"    {c} ({len(ids)}):")
        for s in statuses:
            sids = [r["rid"] for r in recs if r["cls"] == c and r["st"] == s]
            if sids: print(f"        {s}: " + ", ".join(sids))
    print()

    print("[4] The INSTR flag (instrument / pipeline words) and the GATE flag")
    for name, _ in INSTR_WORDS:
        ids = [r["rid"] for r in recs if name in r["iw"]]
        print(f"    {name:26s} {len(ids):3d}: " + (", ".join(ids) if ids else "-"))
    fl = [r for r in recs if r["iw"]]
    print(f"    rows with INSTR set: {len(fl)}")
    ct = collections.Counter((r["cls"], r["st"]) for r in fl)
    for (c, s), n in sorted(ct.items()):
        print(f"        {c:46s} {s:22s} {n}")
    for name, _ in EXTRA_WORDS:
        ids = [r["rid"] for r in recs if name in r["ew"]]
        print(f"    extra '{name}' {len(ids)}: " + (", ".join(ids) if ids else "-"))
    g = [r for r in recs if r["gate"]]
    print(f"    rows with GATE set (a closed gate named in the verdict): {len(g)}")
    ct = collections.Counter((r["cls"], r["st"]) for r in g)
    for (c, s), n in sorted(ct.items()):
        print(f"        {c:46s} {s:22s} {n}")
    print("        " + ", ".join(r["rid"] for r in g))
    print()

    print("[5] Cross-check against ladder.py's allocation (printed, not reconciled)")
    p0_l = [r["rid"] for r in recs if r["alloc"] == "PASS-0"]
    p0_c = [r["rid"] for r in recs if r["cls"] == "PASS-0"]
    print(f"    ladder.py PASS-0 rows {len(p0_l)}; class PASS-0 here {len(p0_c)}; ladder PASS-0 rows classed otherwise here: "
          + (", ".join(f"{x} -> {next(r['cls'] for r in recs if r['rid'] == x)}" for x in p0_l if x not in p0_c) or "none"))
    f_l = [r["rid"] for r in recs if r["alloc"] == "FAIL" and r["st"] == "held-out"]
    f_c = [r["rid"] for r in recs if r["cls"] == "FAIL" and r["st"] == "held-out"]
    print(f"    ladder.py held-out FAIL rows {len(f_l)}; class FAIL held-out here {len(f_c)}; ladder held-out FAIL rows classed "
          "otherwise here: " + (", ".join(f"{x} -> {next(r['cls'] for r in recs if r['rid'] == x)}" for x in f_l if x not in f_c) or "none"))
    held = [r for r in recs if r["st"] == "held-out"]
    hp = [r for r in held if r["cls"] in ("PASS-1", "PASS-0")]
    hf = [r for r in held if r["cls"] == "FAIL"]
    hn = [r for r in held if r["cls"] in ("VOID", "NOT DECIDABLE", "UNINFORMATIVE")]
    print(f"    held-out rows {len(held)}: PASS-1 or PASS-0 {len(hp)}; FAIL {len(hf)}; VOID + NOT DECIDABLE + UNINFORMATIVE {len(hn)}")
    hfi = [r["rid"] for r in hf if r["iw"]]
    print(f"    held-out FAIL rows carrying the INSTR flag: {len(hfi)}" + (" (" + ", ".join(hfi) + ")" if hfi else ""))
    print()
    print("[6] Denominators kept apart: this table counts LEDGER rows only. The retrodiction batteries, the synthesis class and")
    print("    PRED70 are separate banks with their own denominators (Epistemic_Review/checks/ladder.txt [1]-[2], [5];")
    print("    Epistemic_Review/checks/redundant_vs_fail.txt [1]); they are not added to any count above.")


if __name__ == "__main__":
    main()
