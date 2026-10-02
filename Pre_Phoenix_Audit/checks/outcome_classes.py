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

It then prints tallies (data status x class), the rows per class, and the rows carrying each flag word, a held-out
study-prefix x class table, a process-timing table (read only: the commit time of named commits, `git show -s
--format=%cI`, and the UTC time in named prompt-log headers; no clock is read, so the output is deterministic), and the
AGENT_LOG entries that mention each follow-up named in the log as a next step.
The ledger tables are the denominator table for the ledger only. The retrodictive banks (batteries, synthesis, PRED70) are NOT counted
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
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "ledger" / "LEDGER.md"
PROMPT_LOG = ROOT / "notebook" / "PROMPT_LOG.md"
AGENT_LOG = ROOT / "notebook" / "AGENT_LOG.md"

# Process timing: (study, requesting prompt-log entry or None, prereg hash commit, first scoring / VOID commit).
# The commits are the ones whose messages say 'prereg <study>' and '... scored' / 'VOID' (git log, read by the auditor);
# the prompt entry is the one the AGENT_LOG or the commit message names as the request. EQ2's first design prompt (17)
# is given; its run prompt is 32. EQ2R and EQ2R-CC name no request prompt; T1x2 is the replacement of T1x.
TIMING = (
    ("EQX", 3, "231f75b", "0d21b82"), ("MEAS", 7, "32f18c3", "57b6302"), ("MEAS2", 7, "57b6302", "9047ab7"),
    ("CARD", 9, "0c8fe04", "5c4311a"), ("EQ2", 17, "4ba6035", "455780b"), ("EQ2R", None, "231cb26", "d04b4c8"),
    ("EQ2R-CC", None, "708e9b1", "d04b4c8"), ("EQ3", 69, "daf50e7", "a6d39ff"), ("EQ4", 74, "a55be4d", "c4bdcf1"),
    ("BAYES-1", 84, "49072aa", "bb5ca5a"), ("T1x", 87, "ce825dd", "b809477"), ("T1x2", None, "b809477", "a1a3f30"),
    ("SEC1", 118, "0f67f2d", "3a9b930"), ("SCL1", 124, "17366b9", "3841ad8"), ("SCL2", 125, "679ae8b", "953857b"),
    ("SCL3", 127, "05318d4", "e9fb5f7"), ("RLAW", 137, "be82a3f", "72edf71"), ("SOTA1", 190, "de95c63", "45201f5"),
    ("SEC3", 227, "916d3d4", "c6422e2"), ("SEC4", 228, "278d0b4", "8574912"), ("SEC5", 238, "576a092", "d1bdd27"),
    ("SEC6", 257, "1bb1870", "0671a35"), ("SEC6R", 259, "20f7d06", "45669e6"),
)
# Follow-ups the AGENT_LOG names as a next step or a redesign (term, the entry that names it); the script prints every
# AGENT_LOG entry whose text contains the term, so a later entry would show that the follow-up was taken up.
FOLLOWUPS = (
    ("BAYES-1b", 67), ("H-REG", 130), ("LIFE1", 162), ("dose-matched", 122), ("ARC-R", 132), ("EQ5", 85),
    ("causal phase", 88), ("per-task normalisation", 95), ("settled occasions", 94), ("stronger criterion", 192),
    ("different reference", 238), ("surrogate harder", 71), ("arc-triggered refresh", 202), ("RW3", 158),
    ("equal exploration", 73),
)
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
    print()

    print("[7] Held-out rows: study prefix (row id up to the first '-') x outcome class (non-zero cells only)")
    pref = collections.OrderedDict()
    for r in held:
        pref.setdefault(r["rid"].split("-")[0], collections.Counter())[r["cls"]] += 1
    for p, c in pref.items():
        print(f"    {p:8s} rows {sum(c.values()):3d} | " + "; ".join(f"{k} {c[k]}" for k in ALL_CLASSES if c[k]))
    print()

    print("[8] Process timing (read only): prompt-log header time -> prereg hash commit -> first scoring/VOID commit")
    hdr = {}
    for line in PROMPT_LOG.read_text().splitlines():
        m = re.match(r"^## (\d+)[ .]", line)
        if m:
            t = re.search(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?)Z", line)
            hdr[int(m[1])] = t[1] if t else None

    def ctime(h):
        s = subprocess.run(["git", "show", "-s", "--format=%cI", h], cwd=ROOT, capture_output=True, text=True, check=True)
        return datetime.fromisoformat(s.stdout.strip())

    def utc(t):
        return t.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def ptime(n):
        s = hdr.get(n)
        return datetime.fromisoformat(s + ("" if len(s) > 16 else ":00") + "+00:00") if s else None

    print("    study    prompt (header UTC)          hash commit (UTC)            prompt->hash  first score commit (UTC)     hash->score  prev score->hash")
    prev = None
    for st, pn, hc, sc in TIMING:
        th, ts = ctime(hc), ctime(sc)
        tp = ptime(pn) if pn else None
        p2h = f"{(th - tp).total_seconds() / 60:9.1f} min" if tp else "        n/a  "
        h2s = f"{(ts - th).total_seconds() / 3600:8.2f} h"
        gap = f"{(th - prev).total_seconds() / 3600:8.2f} h" if prev is not None and th >= prev else "     n/a"
        print(f"    {st:8s} {('PL ' + str(pn) + ' ' + hdr[pn]) if pn else 'none named':28s} {hc} {utc(th):20s} "
              f"{p2h}  {sc} {utc(ts):20s} {h2s}  {gap}")
        prev = ts
    print("    'prev score->hash' = hours from the PREVIOUS row's first-score commit (table order) to this row's hash commit (n/a when")
    print("    this hash precedes it). Commit times are the authoritative clock (prompt-log correction note after entry 56). From entry")
    print("    57 on, a prompt header time is read 'from date -u at the moment of logging' (the same note), which can be later than")
    print("    receipt, so 'prompt->hash' is a lower bound on receipt->hash; it also excludes design work done before the request.")
    print()

    print("[9] Follow-ups named in the AGENT_LOG and every AGENT_LOG entry that mentions them")
    ent = []
    for line in AGENT_LOG.read_text().splitlines():
        m = re.match(r"^\| (\d+)( \(r\))? \|", line)
        if m: ent.append((int(m[1]), line))
    for term, named in FOLLOWUPS:
        ids = [n for n, l in ent if term in l]
        later = [n for n in ids if n > named]
        print(f"    {term:24s} named in entry {named:3d}; entries mentioning it: {', '.join(map(str, ids))}; later than {named}: "
              + (", ".join(map(str, later)) if later else "none"))


if __name__ == "__main__":
    main()
