"""The epistemic ladder: what every result in the repository licenses (owner request, prompt-log entry 102).

Nothing is re-run and nothing is re-graded by hand. The script reads the pinned outputs and the ledger, applies the
allocation rules below, and prints every count the review (Epistemic_Review/EPISTEMIC_REVIEW.md) quotes (R1, R15).

The rungs (a result sits on the rung that says what could have made it fail and what it licenses):
    R0  DEFINITIONAL        true by definition, symmetry or a carrier fact; could not have failed (the batteries' DEF kind;
                            such rows sit inside the DESCR grade and are not counted separately here)
    R1  INHERITED           agreement produced by information geometry (the Fisher metric, arc, chord, surplus), which CRR
                            shares with the domain; could fail only by an arithmetic error
    R2  RETRO-PROPER        a CRR-proper ingredient changed the number (ablation T-G differs from the null by more than 1 %)
                            and the changed number is the domain's own known theorem (within 1 %); it could have missed, and
                            in the same class 24 real-domain rows did (WRONG); it adds nothing the domain lacked
    R3  RETRO-ADDS          as R2, but the domain's cited theorem does not give the value and the check in the domain's own
                            mathematics holds; a candidate until a named expert answers the three questions
    R4  DECLARED-SYNTHETIC  a prediction declared and pushed before a run on a synthetic world built by the same author
    R5  PREREG-SEEN         a hashed pre-registered prediction scored on data already seen (a retrodiction by data status)
    R6  PASS-0              a hashed pre-registered prediction on held-out data, R2-R9 as written (provisional)
    R7  PASS-1              PASS-0 and not fragile, no control violated, no reduction to a constant, strong anchoring
    R8  PASS-2              PASS-1 replicated under a fresh prereg on a later day or by a second person
Each rung has its own negative outcomes (WRONG / FAILS / FAIL, VIOLATED, VOID) and its undecided ones (INTERNAL / TENSION,
OPEN / UNSTATED / SILENT, NOT DECIDABLE); they are printed beside the passes, never folded into them.

Allocation rules (mechanical):
  * retrodiction batteries: the GRADE line (standard batteries) or '| verdict X |' (Daniel's battery) per row; FLOW lines
    are classified by who supplies the velocity: 'none' -> none (kinematics), a mention of CRR / the framework / an axiom ->
    framework, anything else -> the domain (system, protocol, experimenter, market, ...). SHARP needs the framework to supply
    it; a row whose flow the domain supplies cannot reach SHARP by the battery's own definition.
  * synthesis: the OUTCOME line of every row of synthesis.txt and synthesis_batches/batch_NN.txt (rows 1-2 of synthesis.txt
    are the gate's controls and are excluded from real-domain counts); the source grade of a re-read is the '(CONSIST)' or
    '(DESCR)' on its source line; REDUNDANT-IG -> R1, REDUNDANT-DOMAIN -> R2 (after checking that its T-G line reads
    'differ'), ADDS -> R3, WRONG -> retrodictive fail, INTERNAL -> undecided, UNSTATED -> silent, PROPOSES -> prospective
    candidate. A row counts for every CRR-proper commitment its ingredient line names (rows marked 'NOT CRR-proper' count
    for none), so the per-commitment table overlaps.
  * ledger: the verdict column, matched from its start after removing bold marks (first rule that matches wins; an
    unmatched verdict stops the script); seen / held-out from the dataset column's (Y) / (N), inherited within a study.
  * AI safety: named lines of the pinned outputs, each with the kind the declarations gave it (THEOREM: a proposition proved
    in AI_SAFETY.md or true by construction, which fails only on a bug; PREDICTION: declared, able to fail; CONTROL: a gate
    control; QUESTION: declared open and computed). A missing line stops the script.
    uv run python Epistemic_Review/checks/ladder.py > Epistemic_Review/checks/ladder.txt
"""
from __future__ import annotations

import collections
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RETRO = ROOT / "theory" / "retrodictions"
BATTERIES = (("main (issue #21)", RETRO / "crr_retrodictions.txt"), ("external SHARP claims", RETRO / "sharp_claims.txt"),
             ("biological", RETRO / "bio_retrodictions.txt"), ("E-I networks", RETRO / "ei_networks.txt"),
             ("driven systems", RETRO / "driven_systems.txt"), ("cognitive / collective", RETRO / "cognitive_collective.txt"),
             ("wild systems", RETRO / "wild_systems.txt"), ("twenty systems", RETRO / "twenty_systems.txt"),
             ("emptiness", RETRO / "emptiness.txt"), ("Shannon", RETRO / "shannon.txt"), ("loop gravity", RETRO / "loop_gravity.txt"),
             ("Daniel's battery", ROOT / "runs" / "phaseA" / "crr_retrodictions.txt"))
GRADES = ("SHARP", "CONSIST", "DESCR", "FAILS", "TENSION", "OPEN")
OUTCOMES = ("ADDS", "PROPOSES", "REDUNDANT-IG", "REDUNDANT-DOMAIN", "WRONG", "INTERNAL", "UNSTATED")
RUNG_OF = {"REDUNDANT-IG": "R1 INHERITED", "REDUNDANT-DOMAIN": "R2 RETRO-PROPER", "ADDS": "R3 RETRO-ADDS (candidate)",
           "WRONG": "retrodictive FAIL", "INTERNAL": "undecided (INTERNAL)", "UNSTATED": "silent (UNSTATED)",
           "PROPOSES": "prospective candidate (PROPOSES)"}
FAMILIES = (("A3/D5 the cut", r"\bA3\b|\bD5\b"), ("A6 regeneration", r"\bA6\b"), ("P2/P3 occasion weights", r"\bP[23]\b"),
            ("A1'/D1 the unit", r"A1['′]|\bD1\b"), ("H-L5 natural time", r"H-L5"), ("D6/H-T1 path", r"\bD6\b|H-T1"),
            ("H-EQ equanimity", r"H-EQ"), ("A7/A8 tense", r"\bA[78]\b"))


def wilson(k, n, z=1.959964):
    if n == 0: return float("nan"), float("nan")
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


# ---------------------------------------------------------------- [1] the retrodiction batteries and the FLOW audit
def batteries():
    print("[1] Retrodiction batteries: grades per battery (GRADE / verdict lines of the pinned outputs)")
    tot = collections.Counter(); flows = collections.Counter(); nflow = 0
    for name, path in BATTERIES:
        t = path.read_text()
        g = re.findall(r"^\s+GRADE:\s+([A-Z]+)", t, re.M) or re.findall(r"\| verdict ([A-Z]+) \|", t)
        c = collections.Counter(g); tot.update(c)
        print(f"    {name:24s} rows {len(g):3d} | " + " ".join(f"{k} {c[k]}" for k in GRADES))
        for fl in re.findall(r"^\s+FLOW:\s+(.*)$", t, re.M):
            nflow += 1; f = fl.lower()
            if f.startswith("none"): flows["none (kinematics only)"] += 1
            elif re.search(r"\bcrr\b|framework|axiom", f): flows["the framework"] += 1
            else: flows["the domain (system, protocol, experimenter, market, ...)"] += 1
    n = sum(tot.values())
    print(f"    all                      rows {n:3d} | " + " ".join(f"{k} {tot[k]}" for k in GRADES))
    print(f"    FLOW audit: {nflow} rows print what supplies the velocity inside C = integral sqrt(x'g x') dt")
    for k in ("the domain (system, protocol, experimenter, market, ...)", "none (kinematics only)", "the framework"):
        print(f"        supplied by {k}: {flows[k]}")
    print(f"    SHARP ('the axioms force the known result with no outside constant') needs the framework to supply the flow: "
          f"reachable in {flows['the framework']} of {nflow} rows that print FLOW; SHARP rows observed {tot['SHARP']} of {n}")
    return tot


# ---------------------------------------------------------------- [2] the synthesis class
def synthesis_rows():
    rows = []
    files = [RETRO / "synthesis.txt"] + sorted((RETRO / "synthesis_batches").glob("batch_*.txt"))
    for f in files:
        for blk in re.split(r"\n(?=\[\s*\d+\])", f.read_text()):
            m = re.search(r"OUTCOME:\s+(\S+)", blk)
            if not m: continue
            k = int(re.match(r"\[\s*(\d+)\]", blk)[1])
            src = re.search(r"source:\s+(.*)", blk); g = re.search(r"\((CONSIST|DESCR)\)", src[1]) if src else None
            ing = re.search(r"ingredient:\s+(.*)", blk)[1]; tg = re.search(r"T-G:\s+(.*)", blk)[1]
            part = "gate" if f.name == "synthesis.txt" and k in (1, 2) else ("first battery" if f.name == "synthesis.txt"
                    else ("FEP (batches 27-28)" if f.name in ("batch_27.txt", "batch_28.txt")
                          else ("Rovelli, Smolin (29-30)" if f.name in ("batch_29.txt", "batch_30.txt")
                                else ("in-paradigm, blind (31-32)" if f.name in ("batch_31.txt", "batch_32.txt") else "re-reads (batches 01-26)"))))
            rows.append(dict(file=f.name, k=k, out=m[1], grade=g[1] if g else None, ing=ing, tg=tg, part=part))
    return rows


def synthesis(rows):
    print("[2] The synthesis class: OUTCOME lines of synthesis.txt and synthesis_batches/batch_NN.txt")
    for part in ("gate", "first battery", "re-reads (batches 01-26)", "FEP (batches 27-28)", "Rovelli, Smolin (29-30)", "in-paradigm, blind (31-32)"):
        c = collections.Counter(r["out"] for r in rows if r["part"] == part)
        print(f"    {part:26s} rows {sum(c.values()):3d} | " + " ".join(f"{k} {c[k]}" for k in OUTCOMES))
    real = [r for r in rows if r["part"] != "gate"]; c = collections.Counter(r["out"] for r in real)
    print(f"    {'all real-domain rows':26s} rows {len(real):3d} | " + " ".join(f"{k} {c[k]}" for k in OUTCOMES))
    rd = [r for r in real if r["out"] == "REDUNDANT-DOMAIN"]
    print(f"    check: REDUNDANT-DOMAIN rows whose T-G line reads 'differ' (the CRR-proper ingredient changed the number): "
          f"{sum('differ' in r['tg'].lower() for r in rd)} of {len(rd)}")
    print("    crosswalk, re-reads only: the battery grade (rows) against the synthesis outcome (columns)")
    rr = [r for r in real if r["part"] == "re-reads (batches 01-26)"]
    for g in ("CONSIST", "DESCR"):
        cc = collections.Counter(r["out"] for r in rr if r["grade"] == g)
        print(f"        {g:8s} {sum(cc.values()):3d} | " + " ".join(f"{k} {cc[k]}" for k in OUTCOMES))
    print("    the same rows on the ladder")
    rung = collections.Counter(RUNG_OF[r["out"]] for r in real)
    for k in ("R1 INHERITED", "R2 RETRO-PROPER", "R3 RETRO-ADDS (candidate)", "retrodictive FAIL", "undecided (INTERNAL)",
              "silent (UNSTATED)", "prospective candidate (PROPOSES)"):
        print(f"        {k:34s} {rung[k]:3d}")
    hit = c["REDUNDANT-DOMAIN"] + c["ADDS"]; risk = hit + c["WRONG"]; lo, hi = wilson(hit, risk)
    print(f"    retrodictive hit rate of CRR-proper ingredients where they did work and could be checked (R2 + R3 against R2 + R3 + WRONG): "
          f"{hit} of {risk} = {hit / risk:.4f} (Wilson 95 % interval {lo:.4f} to {hi:.4f})")
    print(f"    novelty rate among those (R3 against R2 + R3 + WRONG): {c['ADDS']} of {risk} = {c['ADDS'] / risk:.4f}")
    print("    per CRR-proper commitment (a row counts for every commitment its ingredient line names; overlapping): "
          "R2 | R3 | WRONG | INTERNAL | R1 | UNSTATED | PROPOSES | hit rate R2+R3 of R2+R3+WRONG")
    tab = collections.defaultdict(collections.Counter)
    for r in real:
        fams = [] if "NOT CRR-proper" in r["ing"] else [n for n, p in FAMILIES if re.search(p, r["ing"])]
        for n in fams or ["none named (information geometry only)"]: tab[n][r["out"]] += 1
    for n in [f for f, _ in FAMILIES] + ["none named (information geometry only)"]:
        t = tab[n]; h = t["REDUNDANT-DOMAIN"] + t["ADDS"]; d = h + t["WRONG"]
        print(f"        {n:40s} {t['REDUNDANT-DOMAIN']:3d} | {t['ADDS']:2d} | {t['WRONG']:3d} | {t['INTERNAL']:3d} | {t['REDUNDANT-IG']:3d} | "
              f"{t['UNSTATED']:2d} | {t['PROPOSES']:2d} | " + (f"{h} of {d} = {h / d:.4f}" if d else "none checkable"))
    print("    the ADDS rows (candidates; novelty pending a named expert) and the PROPOSES rows")
    for r in real:
        if r["out"] in ("ADDS", "PROPOSES"):
            sysl = re.search(rf"\[\s*{r['k']}\]\s+\(\w+\)\s+(.*)", (RETRO / ("synthesis_batches/" + r["file"] if r["file"] != "synthesis.txt" else "synthesis.txt")).read_text())
            print(f"        {r['out']:8s} {r['file']} row {r['k']}: {sysl[1][:150] if sysl else ''}")
    return c


# ---------------------------------------------------------------- [3] the ledger
LEDGER_RULES = (
    (r"^VOID", "VOID"), (r"^NOT DECIDABLE", "NOT DECIDABLE"), (r"^(DECIDABLE|decidable)", "precondition met"),
    (r"^reported without verdict", "no verdict (precondition failed)"), (r"^report", "report (no verdict registered)"),
    (r"^GATE CLOSED", "gate closed (not run)"), (r"^UNVERIFIABLE", "unverifiable (R1)"), (r"^PASS-0", "PASS-0"),
    (r"^PASS as scored \(held-out.*not counted as PASS-0", "PASS as scored, forced by the construction (not R6)"),
    (r"^PASS on a control line", "control line passes (not the hypothesis)"), (r"^PASS.*\(seen", "PASS on seen data"),
    (r"^PASS, FRAGILE", "PASS, fragile (held-out; relabelled PASS-0 by EQ2-1b)"),
    (r"failed replication", "PASS-0 kept; replication failed"), (r"^FRAGILE at boundary", "not a PASS (fragile at the boundary)"),
    (r"^(FRAGILE|fragile)", "sensitivity: fragile"), (r"^not fragile", "sensitivity: not fragile"),
    (r"^REDUCES", "reduces to a constant"), (r"^(DOES NOT REDUCE|does not reduce)", "does not reduce"),
    (r"^VIOLATED", "control violated"), (r"^IDLE", "bound idle (diagnostic)"), (r"^INERT", "mechanism inert (positive control not load-bearing)"), (r"^PASS \(PASS-0", "PASS-0"), (r"^holds", "control holds"), (r"^no published baseline", "no baseline ahead"),
    (r"^FAIL", "FAIL"), (r"^(immaterial|metric matters)", "numbers reported"), (r"^as claimed \(seen\)", "holds on seen data"), (r"^[−\-+0-9.,: =c/]+", "numbers reported"))


def ledger():
    print("[3] The ledger: every row allocated by its verdict text (first matching rule) and its data status")
    rows = []; last = {}
    for line in (ROOT / "ledger" / "LEDGER.md").read_text().splitlines():
        if not re.match(r"^\| [A-Z]", line): continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rid, data, verdict = cells[0], cells[2], cells[-3].replace("**", "").strip()   # the verdict is third from the end: cells may hold "|" (absolute values)
        fam = rid.split("-")[0]
        if "(Y)" in data: seen = "held-out"
        elif "(N)" in data: seen = "seen"
        elif "synthetic" in data: seen = "synthetic"
        else: seen = last.get(fam, "held-out")
        last[fam] = seen
        lab = next((l for p, l in LEDGER_RULES if re.search(p, verdict)), None)
        if lab is None: raise SystemExit(f"unmatched verdict in {rid}: {verdict[:80]}")
        rows.append((rid, seen, lab))
    for rid, seen, lab in rows: print(f"    {rid:16s} {seen:9s} {lab}")
    c = collections.Counter((s, l) for _, s, l in rows)
    print(f"    rows {len(rows)}; by data status and allocation:")
    for (s, l), n in sorted(c.items()): print(f"        {s:9s} {l:52s} {n}")
    ps = [r for r in rows if r[2] in ("PASS on seen data", "holds on seen data")]
    p0 = [r for r in rows if r[2] == "PASS-0"]
    fails = [r for r in rows if r[2] == "FAIL" and r[1] == "held-out"]
    print(f"    rung R5 PREREG-SEEN, passes on seen data: {len(ps)} ({', '.join(r[0] for r in ps)})")
    print(f"    rung R6 PASS-0 on held-out data: {len(p0)} ({', '.join(r[0] for r in p0)}); R7 PASS-1: 0; R8 PASS-2: 0")
    print(f"    held-out FAIL rows: {len(fails)} ({', '.join(r[0] for r in fails)}); VOID rows: {sum(r[2] == 'VOID' for r in rows)}; "
          f"controls violated: {sum(r[2] == 'control violated' for r in rows)}")
    return rows


# ---------------------------------------------------------------- [4] AI safety
AIS = ROOT / "AI_Safety" / "checks"; ONT = ROOT / "ontology" / "checks"
AI_ITEMS = (  # (id, kind, file, line regex, held regex)
    ("exact K1 indifferent Q ignores the button", "THEOREM", AIS / "exact_mdp.txt", r"K1 .*", r"-> True"),
    ("exact K2 no presses, no value in disabling", "THEOREM", AIS / "exact_mdp.txt", r"K2 .*", r"-> True"),
    ("exact K3 a disabled button never lowers value", "THEOREM", AIS / "exact_mdp.txt", r"K3 .*", r"-> True"),
    ("exact K4 incentive grows with press probability", "THEOREM", AIS / "exact_mdp.txt", r"K4 .*", r"-> True"),
    ("exact K5 indifferent never prefers disable", "THEOREM", AIS / "exact_mdp.txt", r"K5 .*", r"-> True"),
    ("exact K6 occasion's stake >= process's", "QUESTION", AIS / "exact_mdp.txt", r"K6 .*", r"True"),
    ("game A1 rational human, Delta >= 0", "THEOREM", AIS / "off_switch_game.txt", r"A1 rational human.*", r"-> True"),
    ("game A2 certainty removes the incentive (as first coded)", "THEOREM", AIS / "off_switch_game.txt", r"A2 certainty.*", r"-> True"),
    ("game A2' the exact bound, added after the first run", "THEOREM", AIS / "off_switch_game.txt", r"A2' .*", r"-> True"),
    ("game A3 noisier human, smaller Delta", "THEOREM", AIS / "off_switch_game.txt", r"A3 Delta decreases.*", r": True"),
    ("game B informative: deferential does less harm", "PREDICTION", AIS / "off_switch_game.txt", r"^\s+informative\s+deferential\s+vs indifferent: harm.*", r"LESS harm"),
    ("game B informative: deferential more net benefit", "PREDICTION", AIS / "off_switch_game.txt", r"^\s+informative\s+deferential\s+vs indifferent: net.*", r"MORE benefit"),
    ("game B informative: deferential does not disable more", "PREDICTION", AIS / "off_switch_game.txt", r"^\s+informative\s+deferential\s+vs indifferent: disable.*", r"-> (TIE|disables LESS)"),
    ("game B informative: process disables more", "PREDICTION", AIS / "off_switch_game.txt", r"^\s+informative\s+process\s+vs indifferent: disable.*", r"disables MORE"),
    ("game B informative: process does more harm", "PREDICTION", AIS / "off_switch_game.txt", r"^\s+informative\s+process\s+vs indifferent: harm.*", r"MORE harm"),
    ("game B uninformative: deferential advantage gone", "PREDICTION", AIS / "off_switch_game.txt", r"^\s+uninformative\s+deferential\s+vs indifferent: net.*", r"-> (TIE|LESS)"),
    ("sensitivity C1 process resists, not fragile", "PREDICTION", AIS / "sensitivity.txt", r"C1 instrumental resistance.*", r"registered RESISTS.*not fragile"),
    ("sensitivity C2 indifference has a price, not fragile", "PREDICTION", AIS / "sensitivity.txt", r"C2 the price of indifference.*", r"registered PRICE.*not fragile"),
    ("combined: natural time safe and competent (routine pauses)", "PREDICTION", AIS / "combined.txt", r"pause\s+natural\s+disable vs.*", r"SAFE AND COMPETENT"),
    ("combined: wall-clock resists (routine pauses)", "PREDICTION", AIS / "combined.txt", r"pause\s+clock\s+disable vs.*", r"-> RESISTS"),
    ("combined: occasion resists (routine pauses)", "PREDICTION", AIS / "combined.txt", r"pause\s+occasion\s+disable vs.*", r"-> RESISTS"),
    ("combined: deferential safe and competent (reasoned pauses)", "PREDICTION", AIS / "combined.txt", r"harm\s+deferential\s+disable vs.*", r"SAFE AND COMPETENT"),
    ("combined: natural does not resist, more harm (reasoned)", "PREDICTION", AIS / "combined.txt", r"harm\s+natural\s+disable vs.*", r"does not resist.*MORE HARM"),
    ("combined: wall-clock resists (reasoned pauses)", "PREDICTION", AIS / "combined.txt", r"harm\s+clock\s+disable vs.*", r"-> RESISTS"),
    ("combined: occasion resists (reasoned pauses)", "PREDICTION", AIS / "combined.txt", r"harm\s+occasion\s+disable vs.*", r"-> RESISTS"),
    ("combined V1 the keeper gains by blocking correction", "PREDICTION", AIS / "combined.txt", r"V1 .*", r"True"),
    ("combined V2 A8 welcomes correction above b*", "PREDICTION", AIS / "combined.txt", r"V2 .*", r"True"),
    ("combined V3 b* < 1/2", "PREDICTION", AIS / "combined.txt", r"V3 .*", r"True"),
    ("scale A1 natural time, lossless pause, every world", "THEOREM", AIS / "scale.txt", r"A1 natural time.*", r": True"),
    ("scale A2 occasion >= clock >= natural", "THEOREM", AIS / "scale.txt", r"A2 at every button state.*", r": True"),
    ("scale A3 clock disables in >= half of worlds", "PREDICTION", AIS / "scale.txt", r"A3 share of worlds.*", r"-> holds"),
    ("scale A4a drift 0.01: natural disables no more than clock", "PREDICTION", AIS / "scale.txt", r"A4a .*", r": True"),
    ("scale A4b natural incentive non-decreasing in drift", "PREDICTION", AIS / "scale.txt", r"A4b .*", r": True"),
    ("scale B1 A8 static, D(b) linear", "THEOREM", AIS / "scale.txt", r"B1 A8 static.*", r": True"),
    ("scale B2 exchangeable rewards: b* near 1/2", "PREDICTION", AIS / "scale.txt", r"B2 exchangeable.*", r": holds"),
    ("scale B3 humility alone never welcomes an uninformative correction", "THEOREM", AIS / "scale.txt", r"B3 A8 acting.*", r": True"),
    ("scale B4 an infallible operator's correction is welcomed", "THEOREM", AIS / "scale.txt", r"B4 A8 acting.*", r": True"),
    ("gate off_switch NEG (process)", "CONTROL", ONT / "off_switch.txt", r"NEG nooper: process.*", r"no excess"),
    ("gate off_switch NEG (egoic)", "CONTROL", ONT / "off_switch.txt", r"NEG nooper: egoic.*", r"no excess"),
    ("gate off_switch POS (egoic resists)", "CONTROL", ONT / "off_switch.txt", r"POS resist:.*", r"-> RESISTS"),
    ("gate combined NEG (clock)", "CONTROL", AIS / "combined.txt", r"NEG nooper: clock.*", r"no excess"),
    ("gate combined NEG (occasion)", "CONTROL", AIS / "combined.txt", r"NEG nooper: occasion.*", r"no excess"),
    ("gate combined NEG (deferential)", "CONTROL", AIS / "combined.txt", r"NEG nooper: deferential.*", r"no excess"),
    ("gate combined POS (occasion resists)", "CONTROL", AIS / "combined.txt", r"POS pause:.*", r"-> RESISTS"),
    ("gate tense NEG (martingale tie)", "CONTROL", ONT / "tense_gate.txt", r"NEG martingale:.*", r"ok\)"),
    ("gate tense POS (drift, planner ahead)", "CONTROL", ONT / "tense_gate.txt", r"POS drift:.*", r"ok\)"),
)


def ai_safety():
    print("[4] AI safety: declared items read from the pinned outputs (kind as declared; held / failed from the printed line)")
    tally = collections.Counter()
    for name, kind, path, line_re, held_re in AI_ITEMS:
        m = re.search(line_re, path.read_text(), re.M)
        if not m: raise SystemExit(f"missing line for {name}")
        held = bool(re.search(held_re, m[0])); tally[(kind, held)] += 1
        print(f"    {kind:10s} {'held ' if held else 'FAILED'} {name}  [{path.relative_to(ROOT)}]")
    for kind in ("THEOREM", "PREDICTION", "CONTROL", "QUESTION"):
        print(f"    {kind:10s} held {tally[(kind, True)]}, failed {tally[(kind, False)]}")
    return tally


def main():
    print("The epistemic ladder (Epistemic_Review/checks/ladder.py): allocations computed from the pinned outputs and the ledger")
    b = batteries(); rows = synthesis_rows(); c = synthesis(rows); led = ledger(); ai = ai_safety()
    print("[5] The whole repository on the ladder (counts from [1]-[4])")
    real = [r for r in rows if r["part"] != "gate"]
    print(f"    retrodiction batteries, graded before the synthesis re-read: " + ", ".join(f"{k} {b[k]}" for k in GRADES)
          + " (SHARP unreachable, [1]; CONSIST and DESCR re-read and placed on R1-R3 in [2])")
    print(f"    R1 INHERITED                      synthesis REDUNDANT-IG {c['REDUNDANT-IG']}")
    print(f"    R2 RETRO-PROPER                   synthesis REDUNDANT-DOMAIN {c['REDUNDANT-DOMAIN']}")
    print(f"    R3 RETRO-ADDS (candidates)        synthesis ADDS {c['ADDS']}; reviewed by a named expert 0")
    print(f"    R4 DECLARED-SYNTHETIC             AI-safety predictions held {ai[('PREDICTION', True)]} of {ai[('PREDICTION', True)] + ai[('PREDICTION', False)]}; "
          f"theorem checks held {ai[('THEOREM', True)]} of {ai[('THEOREM', True)] + ai[('THEOREM', False)]}; gate controls held {ai[('CONTROL', True)]} of {ai[('CONTROL', True)] + ai[('CONTROL', False)]}")
    print(f"    R5 PREREG-SEEN                    passes on seen data {sum(r[2] in ('PASS on seen data', 'holds on seen data') for r in led)}")
    print(f"    R6 PASS-0                         {sum(r[2] == 'PASS-0' for r in led)}")
    print("    R7 PASS-1                         0")
    print("    R8 PASS-2                         0")
    print(f"    negatives beside them: battery FAILS {b['FAILS']}, synthesis WRONG {c['WRONG']}, held-out ledger FAIL "
          f"{sum(r[2] == 'FAIL' and r[1] == 'held-out' for r in led)}, AI-safety predictions failed {ai[('PREDICTION', False)]}; "
          f"undecided: battery TENSION {b['TENSION']}, synthesis INTERNAL {c['INTERNAL']}; silent: battery OPEN {b['OPEN']}, synthesis UNSTATED {c['UNSTATED']}")
    print(f"    real-domain synthesis rows {len(real)}")


if __name__ == "__main__":
    main()
