"""POST HOC (critic follow-up 1; not declared)

DR1 follow-up 1 to check H7: the scored performance-power point is GPU-scoped, not fleet-scoped. An unscored sensitivity.

Binding declaration: Grid_Demand_Response/DECLARATION.md (pushed at e67e8ee; never edited here), section 2, row H7:
  Q: a throttle also has zero content on the own clock; its energy per step is lower; the curtailed MW per unit of delay is
     compared.   Forecast: Q holds.
Nothing in this file was declared. It was written after DR1's first run and after skeptic 3 of the DR1 verification
(Grid_Demand_Response/checks/verification.md, H7) refuted H7 (severity major): dr_h7.py labels McDonald et al.'s 150 W point
p_M = 863/1068 SOURCED and uses it as the power fraction of the whole 100 MW fleet, but the point is GPU energy (measured with
GPU tools; docs/citations/dr1_followup1_2026-09-29.md section 1), and the F4 dossier's own reading of that source says "A cap
limits the GPU's maximum draw, not the facility's".

What this does. dr_h7.py is imported unchanged (its sources, arms, per-event arithmetic and scored SRC curve are reused; this
file edits nothing). The fleet's power under a throttle at throughput t is read as g p(t) + 1 - g: a GPU share g follows the
scored SRC GPU curve p(t), the rest (1 - g) is not throttled. The fleet's energy per own step during the event is then
(g p(t) + 1 - g)/t. H7's Q clauses are recomputed exactly as dr_h7.py's SENSITIVITY 1 recomputes them (Q1 by stakes only),
for g in {28/51 = 8 x 0.7 kW / 10.2 kW (from two F5 quotes), 0.6, 0.7, 0.8, 1.0}; g = 1.0 is dr_h7.py's implicit reading and
must reproduce its pinned numbers. The flip points of Q2(a) and Q2(b) in g are computed in closed form and checked against the
drlib counts. Every verdict word printed is computed from the numbers (R15). Rung R4 at most (synthetic model); a note, not
evidence (R8). Deterministic; stdlib only (via drlib).

    cd /home/user/ashes_crr && uv run python Grid_Demand_Response/checks/followup_1.py > Grid_Demand_Response/checks/followup_1.txt
"""
from __future__ import annotations

import re
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import drlib as dl  # noqa: E402
import dr_h7 as h7  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
CIT = REPO / "docs" / "citations"
F4, F5, FU = "dr1_f4_2026-09-29.md", "dr1_f5_2026-09-29.md", "dr1_followup1_2026-09-29.md"
TEXT = {f: (CIT / f).read_text(encoding="utf-8") for f in (F4, F5, FU)}
PINNED_H7 = (Path(__file__).resolve().parent / "dr_h7.txt").read_text(encoding="utf-8")
ZERO, ONE = Fr(0), Fr(1)


def ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


# id, dossier(s) the quote must be found in, citation, verbatim quote, regex giving the numbers
SOURCES = [
    dict(id="DGX", fs=(F5, FU), src="NVIDIA DGX H100 datasheet",
         quote="GPU 8x NVIDIA H100 Tensor Core GPUs GPU memory 640GB total Performance 32 petaFLOPS FP8 NVIDIA® NVSwitch™ 4x "
               "System power usage ~10.2kW max",
         rx=r"GPU ([0-9]+)x NVIDIA H100 .* System power usage ~([0-9.]+)kW max"),
    dict(id="H100-TDP", fs=(F5, FU), src="NVIDIA H100 product page",
         quote="Max Thermal Design Power (TDP) Up to 700W (configurable) 350-400W (configurable)",
         rx=r"Up to ([0-9]+)W \(configurable\) ([0-9]+)-([0-9]+)W \(configurable\)"),
    dict(id="H100-COLS", fs=(FU,), src="NVIDIA H100 product page", quote="H100 SXM H100 NVL", rx=r"(H100 SXM) (H100 NVL)"),
    dict(id="MCD-TOOLS", fs=(FU,), src="McDonald et al., arXiv:2205.09646 v1",
         quote="Broadly, these tools enable monitoring of GPU usage on a node and the collection of metrics on Streaming "
               "Multi-processor (SM) utilization, GPU memory footprint, power draw, GPU temperatures, PCI Express (PCIe) "
               "bandwidth, and several other hardware settings.",
         rx=r"(monitoring of GPU usage on a node).*(power draw)"),
    dict(id="MCD-PERGPU", fs=(FU,), src="McDonald et al., arXiv:2205.09646 v1",
         quote="On our system, this data is collected on every node and every GPU assigned to a job.",
         rx=r"(every GPU assigned to a job)"),
    dict(id="MCD-150", fs=(F4, FU), src="McDonald et al., arXiv:2205.09646 v1",
         quote="Averaging across each choice of conﬁguration, a 150W bound on power utilization led to an average 13.7% decrease in "
               "energy usage and 6.8% increase in training time compared to the default maximum.",
         rx=r"average ([0-9.]+)% decrease in energy usage and ([0-9.]+)% increase in training time"),
    dict(id="MCD-PUE-G", fs=(FU,), src="McDonald et al., arXiv:2205.09646 v1 (citing Ascierto and Lawrence, 2020)",
         quote="A highly efﬁcient datacenter will have a PUE close to 1, such that the facility energy overhead is minimal, while the "
               "global average for PUE is 1.59 (Ascierto and Lawrence, 2020).",
         rx=r"global average for PUE is ([0-9.]+)"),
    dict(id="MCD-PUE-M", fs=(FU,), src="McDonald et al., arXiv:2205.09646 v1",
         quote="For instance the average PUE in January is 1.05 while in July it is 1.49, a 42% difference.",
         rx=r"January is ([0-9.]+) while in July it is ([0-9.]+)"),
]
# the F4 dossier's own Reading of McDonald et al. (an investigator's reading, not a quote; line-wrapped in the dossier)
F4_WARNING = "A cap limits the GPU's maximum draw, not the facility's"

POST_FIRST_RUN_CHANGES: list[str] = []


def load_sources() -> tuple[dict, list]:
    got, bad = {}, []
    for s in SOURCES:
        miss = [f for f in s["fs"] if s["quote"] not in TEXT[f]]
        if miss:
            bad.append(f"{s['id']}: quote not found verbatim in {', '.join(miss)}")
            continue
        m = re.search(s["rx"], s["quote"])
        if not m:
            bad.append(f"{s['id']}: numbers not parsed from the quote")
            continue
        got[s["id"]] = m.groups()
    return got, bad


def f(x, d=6) -> str:
    return "-" if x is None else f"{float(x):.{d}f}"


def fleet_curve(src, tM, pM, g):
    """The fleet's power fraction at throughput t: g p_src(t) + 1 - g, as an exact piecewise-linear drlib curve (a linear map
    of the SRC curve's points)."""
    return dl.power_pw([(ZERO, (1 - g) + g * src(ZERO)), (tM, (1 - g) + g * pM), (ONE, ONE)])


def recompute(curve, etm_idle=ZERO):
    """H7's Q clauses under a curve, exactly as dr_h7.py's SENSITIVITY 1 (Q1 by stakes only; x* not recomputed), over its
    scored cells (D x H) and depths. etm_idle != 0 only in the context reading (the paused fleet keeps drawing 1 - g)."""
    etm = dl.ETM if etm_idle == 0 else dl.Arm("ETM-idle", "own", "own", idle=etm_idle)
    mx, n1, a_ok, b_ok, n2, n3 = ZERO, 0, 0, 0, 0, 0
    dirs = {"throttle more": 0, "pause more": 0, "equal": 0}
    a_fail, b_fail = [], []
    for D in h7.DS:
        for H in HS:
            job = dl.Job(h7.W, D, h7.R)
            K = len(dl.every(h7.SPACING, H, job.W))
            pe_e = h7.per_event(job, etm, H)
            eps_e = (h7.W + K * pe_e["net"]) / h7.W
            for x in XS:
                a = h7.thr(x, curve, "own")
                pe = h7.per_event(job, a, H)
                bs = [abs(dl.stake(job, a, H, n) - job.rate * pe["o"]) for n in range(K)]
                mx, n1 = max([mx] + bs), n1 + len(bs)
                qa = pe["eps"] < 1
                qb = (h7.W + K * pe["net"]) / h7.W < eps_e
                a_ok, b_ok, n2 = a_ok + int(qa), b_ok + int(qb), n2 + 1
                if not qa:
                    a_fail.append((D, H, x))
                if not qb:
                    b_fail.append((D, H, x))
                s_t, s_e = pe["slope"], pe_e["slope"]
                if s_t is not None and s_e is not None:
                    n3 += 1
                    dirs["throttle more" if s_t > s_e else "pause more" if s_t < s_e else "equal"] += 1
    q1 = mx == 0
    q2 = a_ok == n2 and b_ok == n2
    q3 = n3 == n2                                 # C5: Q3 holds iff the comparison is computable (both delays > 0) everywhere
    q = "not computable" if not q3 else ("holds" if (q1 and q2) else "fails")
    line = (f"Q1 max {f(mx, 6)} over {n1} -> {'holds' if q1 else 'fails'}; Q2(a) {a_ok}/{n2}, (b) {b_ok}/{n2} -> "
            f"{'holds' if q2 else 'fails'}; Q3 throttle more {dirs['throttle more']}, pause more {dirs['pause more']}, equal "
            f"{dirs['equal']} of {n2}; Q under this curve: {q}")
    return dict(q1=q1, q2=q2, q3=q3, n3=n3, q=q, a_ok=a_ok, b_ok=b_ok, n=n2, dirs=dirs, line=line, a_fail=a_fail, b_fail=b_fail)


def main() -> int:
    print("POST HOC (critic follow-up 1; not declared)")
    print()
    print("DR1 follow-up 1 to check H7: the scored power point is GPU-scoped; the fleet's power read as g x GPU + (1 - g). An unscored")
    print(f"sensitivity. Binding declaration Grid_Demand_Response/DECLARATION.md (declared at {dl.DECL_AT}; not edited). dr_h7.py and")
    print("dr_h7.txt are not edited: dr_h7.py is imported unchanged. Rung R4 at most (synthetic model); a note, not evidence (R8).")
    print()
    got, bad = load_sources()
    h7got, h7bad = h7.load_sources()
    warn_ok = ws(F4_WARNING) in ws(TEXT[F4])
    print("SOURCED INPUTS (each quote checked verbatim, at run time, against every dossier named; numbers parsed from the quote)")
    for s in SOURCES:
        ok = s["id"] in got
        print(f"  [{s['id']}] {s['src']} ({', '.join(s['fs'])}): {'found' if ok else 'NOT FOUND'}; parsed {got.get(s['id'])}")
        print(f"      '{s['quote']}'")
    print(f"  F4 dossier Reading of McDonald et al. (an investigator's reading, not a quote; whitespace-normalised match): "
          f"'{F4_WARNING}' -> {'found' if warn_ok else 'NOT FOUND'}")
    print(f"  dr_h7.py's own sources (dr_h7.load_sources, unchanged): {len(h7got)} of {len(h7.SOURCES)} found")
    print()
    if bad or h7bad or not warn_ok:
        print("  FAILURES: " + "; ".join(bad + h7bad + ([] if warn_ok else ["F4 warning not found"])))
        print("RESULT FOLLOW-UP 1: not computable (a sourced quote failed)")
        return 1

    # ---------------------------------------------------------------------------- the GPU share g
    n_gpu, kw = dl.q(got["DGX"][0]), dl.q(got["DGX"][1])
    tdp_sxm, nvl_lo, nvl_hi = (dl.q(v) for v in got["H100-TDP"])
    g_src = n_gpu * tdp_sxm / (kw * 1000)
    g_nvl = n_gpu * nvl_hi / (kw * 1000)
    pue_g = dl.q(got["MCD-PUE-G"][0])
    pue_jan, pue_jul = (dl.q(v) for v in got["MCD-PUE-M"])

    # ---------------------------------------------------------------------------- dr_h7's scored curve, rebuilt as dr_h7 builds it
    e_dec, t_inc = (dl.q(v) for v in h7got["MCD-150"])
    T_M, E_M = 1 + t_inc / 100, 1 - e_dec / 100
    tM, pM = 1 / T_M, E_M / T_M
    xM = 1 - tM
    flex = tuple(dl.q(v) / 100 for v in h7got["FLEX"])
    H_phx = dl.q(h7got["PHX-3H"][0])
    global HS, XS
    HS = (dl.q(1), H_phx, dl.q(4), dl.q(6))
    XS = (xM,) + tuple(sorted(set(flex)))
    src = dl.power_pw([(ZERO, ZERO), (tM, pM), (ONE, ONE)])

    print("INPUTS AND LABELS")
    print(f"  LABELLING FIX (post first run of dr_h7.py; listed here, not applied, since this follow-up edits no other file): dr_h7.py's")
    print(f"    SRC point (t_M, p_M) = ({tM}, {pM}) = ({f(tM, 6)}, {f(pM, 6)}) is SOURCED as a GPU-scoped average-power fraction")
    print(f"    (MCD-TOOLS, MCD-PERGPU: GPU tools, per GPU; V100s at 150 W of a 250 W default). Using it as the power fraction of the")
    print(f"    whole fleet is the reading g = 1 (all fleet power is throttled GPU power): ASSUMED, not SOURCED, and unprinted in dr_h7.")
    print(f"  g_src = {g_src} = {f(g_src, 6)} = {dl.g(n_gpu)} GPUs x {dl.g(tdp_sxm)} W / {dl.g(kw)} kW: two SOURCED numbers (DGX, H100-TDP),")
    print(f"    one ASSUMED equivalence (the DGX H100's GPUs are the 700 W SXM form: H100-COLS gives SXM and NVL columns, and the")
    print(f"    datasheet names neither) and one CHOICE (the ratio of the two maxima, TDP and '~10.2kW max', is the GPU share at")
    print(f"    full power; a node's non-GPU draw at full GPU load is not quoted). Node level: no PUE applied.")
    print(f"  g in {{0.6, 0.7, 0.8}}: ASSUMED grid points (the follow-up task's); g = 1: dr_h7.py's implicit reading (reproduction check)")
    print(f"  CHOICE: the non-GPU share (1 - g) is not throttled (constant power during the event), so the fleet's power fraction at")
    print(f"    throughput t is g p(t) + 1 - g, with p the SRC GPU curve unchanged (its ASSUMED (0, 0) lower end kept); the fleet's energy")
    print(f"    per own step during the event is (g p(t) + 1 - g)/t. The pause's power while paused stays 0 (dr_h7's ASSUMED; a context")
    print(f"    reading below gives the paused fleet 1 - g). W, R, D, H, K, P = 100 MW, the depths x and every arm are dr_h7's, unchanged.")
    print()

    # exactness of the fleet curve
    GRID = [("g_src (SOURCED + ASSUMED equivalence)", g_src), ("ASSUMED", dl.q("0.6")), ("ASSUMED", dl.q("0.7")),
            ("ASSUMED", dl.q("0.8")), ("dr_h7's implicit reading", ONE)]
    exact = all(fleet_curve(src, tM, pM, g)(1 - x) == g * src(1 - x) + 1 - g for _, g in GRID for x in XS + (ZERO,))
    print(f"FLEET CURVE CHECK: g p(t) + 1 - g equals the piecewise-linear drlib fleet curve at every depth and at t = 1 for every g "
          f"-> {'exact' if exact else 'NOT EXACT'}")
    print()

    # ---------------------------------------------------------------------------- per-depth table
    print("PER-DEPTH TABLE (fleet reading; P = 100 MW). Per g and depth x: GPU power fraction p(t) (SRC), fleet power fraction")
    print("p_f = g p + 1 - g, fleet energy per own step p_f/t (Q2(a) needs < 1), curtailed MW P (1 - p_f), and MW curtailed per hour")
    print("of delay P (1 - p_f)/x against ETM's P H/(H + R) at H = 1 and 6")
    print(f"  {'g':>9} {'x':>9} {'t':>9} {'p(t)':>9} {'p_f':>9} {'p_f/t':>9} {'MW':>9} {'MW/h del':>9} {'ETM H=1':>8} {'ETM H=6':>8}  Q2(a)")
    for _, g in GRID:
        for x in XS:
            t = 1 - x
            p = src(t)
            pf = g * p + 1 - g
            e1, e6 = [dl.q(H) / (dl.q(H) + h7.R) * h7.P_MW for H in (1, 6)]
            print(f"  {f(g, 6):>9} {f(x, 6):>9} {f(t, 6):>9} {f(p, 6):>9} {f(pf, 6):>9} {f(pf / t, 6):>9} {f(h7.P_MW * (1 - pf), 3):>9} "
                  f"{f(h7.P_MW * (1 - pf) / x, 3):>9} {f(e1, 3):>8} {f(e6, 3):>8}  {'holds' if pf / t < 1 else 'fails'}")
    print()

    # ---------------------------------------------------------------------------- closed-form flip points
    print("FLIP POINTS IN g (closed form, SRC GPU curve, pause idle 0)")
    print("  Q2(a) at depth x holds iff (g p + 1 - g)/t < 1, i.e. g > g_a(x) = x / (1 - p(1 - x)).")
    print("  Q2(b) at (x, H) holds iff the throttle's net energy per event H (p_f - t) = H (x - g (1 - p)) is below ETM's R, i.e.")
    print("  g > g_b(x, H) = (x - R/H) / (1 - p) (C8's accounting; D does not enter).")
    ga = {x: x / (1 - src(1 - x)) for x in XS}
    gb = {(x, H): (x - h7.R / H) / (1 - src(1 - x)) for x in XS for H in HS}
    for x in XS:
        print(f"    x = {f(x, 6)}: g_a = {f(ga[x], 6)} (exact {ga[x]}); g_b over H = "
              + ", ".join(f"{dl.g(H)}: {f(gb[(x, H)], 6)}" for H in HS))
    ga_max = max(ga.values())
    gb_max = max(gb.values())
    gq = max(ga_max, gb_max)
    xa = max(XS, key=lambda x: ga[x])
    print(f"  Q2(a) holds at every depth iff g > {f(ga_max, 6)} (set by x = {f(xa, 2)}); Q2(b) holds everywhere iff g > {f(gb_max, 6)};")
    print(f"  so Q (with Q1 and Q3 as computed below) holds iff g > {f(gq, 6)}. g_src = {f(g_src, 6)} is "
          f"{'below' if g_src <= gq else 'above'} it.")
    print()

    # ---------------------------------------------------------------------------- the recomputation per g
    print("RECOMPUTED Q CLAUSES PER g (dr_h7.py's SENSITIVITY 1 method: 2 D x 4 H cells x 4 depths = 32 pairs; Q1 by stakes only)")
    res = {}
    agree = 0
    for lab, g in GRID:
        r = recompute(fleet_curve(src, tM, pM, g))
        res[g] = r
        pa = sum(int(g > ga[x]) for D in h7.DS for H in HS for x in XS)
        pb = sum(int(g > gb[(x, H)]) for D in h7.DS for H in HS for x in XS)
        ok = pa == r["a_ok"] and pb == r["b_ok"]
        agree += int(ok)
        print(f"  g = {f(g, 6)} ({lab}): {r['line']}")
        fa = sorted({x for _, _, x in r["a_fail"]})
        fb = sorted({(x, H) for _, H, x in r["b_fail"]})
        print(f"      Q2(a) fails at depths {', '.join(f(x, 2) for x in fa) or 'none'}; Q2(b) fails at (x, H) "
              f"{', '.join(f'({f(x, 2)}, {dl.g(H)})' for x, H in fb) or 'none'}; closed-form counts (a) {pa}, (b) {pb} -> "
              f"{'agree' if ok else 'DISAGREE'} with drlib")
    print(f"  closed-form flip points agree with the drlib counts at {agree} of {len(GRID)} g values")
    print()

    # ---------------------------------------------------------------------------- reproduction of dr_h7 at g = 1
    m = re.search(r"^  SRC   : (.*)$", PINNED_H7, re.M)
    pinned_src = m.group(1) if m else None
    rep = pinned_src == res[ONE]["line"]
    m2 = re.search(r"^RESULT H7: Q (holds|fails|not computable);", PINNED_H7, re.M)
    scored = m2.group(1) if m2 else None
    print("REPRODUCTION (g = 1 against the pinned dr_h7.txt)")
    print(f"  pinned SENSITIVITY 1 SRC line: {pinned_src}")
    print(f"  this file at g = 1:            {res[ONE]['line']}")
    print(f"  -> {'reproduced' if rep else 'NOT REPRODUCED'}; the pinned scored verdict (RESULT H7) reads 'Q {scored}'")
    print()

    # ---------------------------------------------------------------------------- context readings (not scored)
    print("CONTEXT (not scored)")
    print(f"  C-a  the NVL column instead of SXM (H100-TDP's 350-400 W; upper end {dl.g(nvl_hi)} W): g = {f(g_nvl, 6)}; "
          f"Q under it: {recompute(fleet_curve(src, tM, pM, g_nvl))['q']}")
    print(f"  C-b  facility level, PUE from McDonald et al. (MCD-PUE-G {dl.g(pue_g)}, cited by them; MCD-PUE-M {dl.g(pue_jan)} and "
          f"{dl.g(pue_jul)}, their own):")
    print(f"       if the facility overhead tracks the IT load, the share is unchanged (g = g_src); if it is fixed (CHOICE), g = g_src / PUE:")
    for pue in (pue_jan, pue_jul, pue_g):
        gg = g_src / pue
        r = recompute(fleet_curve(src, tM, pM, gg))
        print(f"       PUE {dl.g(pue)}: g = {f(gg, 6)}; Q2(a) {r['a_ok']}/{r['n']}, (b) {r['b_ok']}/{r['n']}; Q under it: {r['q']}")
    print("  C-c  the paused fleet keeps drawing the non-GPU share (ETM idle = 1 - g; CHOICE, the symmetric reading of skeptic 3's")
    print("       item 7): Q2(b) and the Q3 direction recomputed")
    for lab, g in GRID:
        r = recompute(fleet_curve(src, tM, pM, g), etm_idle=1 - g)
        print(f"       g = {f(g, 6)}: {r['line']}")
    print()

    # ---------------------------------------------------------------------------- fragility and result
    qv_src = res[g_src]["q"]
    flips = [g for _, g in GRID if res[g]["q"] != scored]
    holds_at = [g for _, g in GRID if res[g]["q"] == "holds"]
    fragile = len(flips) > 1
    print("FRAGILITY (CHOICE: CLAUDE.md section 4's rule, 'a verdict that flips in > 1 cell is reported as fragile', applied to this")
    print("g grid against the pinned scored verdict)")
    print(f"  the pinned scored verdict 'Q {scored}' differs from the recomputed verdict at {len(flips)} of {len(GRID)} g values "
          f"({', '.join(f(g, 6) for g in flips) or 'none'}); Q holds at {', '.join(f(g, 6) for g in holds_at) or 'none'}")
    print(f"  -> H7 is {'FRAGILE' if fragile else 'not fragile'} in g")
    print()
    print("POST-FIRST-RUN CHANGES (to this file): " + ("none" if not POST_FIRST_RUN_CHANGES else "; ".join(POST_FIRST_RUN_CHANGES)))
    print("LABELLING FIX TO LIST FOR dr_h7.py (post first run; not applied here): the SRC point is GPU-scoped; reading it as the fleet's")
    print("  power fraction is the ASSUMED g = 1.")
    print()
    print(f"RESULT FOLLOW-UP 1 (POST HOC, unscored): at the sourced GPU share g = {f(g_src, 6)} ({g_src}) Q {qv_src} "
          f"(Q2(a) {res[g_src]['a_ok']}/{res[g_src]['n']}, (b) {res[g_src]['b_ok']}/{res[g_src]['n']}); Q holds only for g > "
          f"{f(gq, 6)}; the pinned verdict 'Q {scored}' (g = 1) is {'reproduced' if rep else 'NOT reproduced'} and differs at "
          f"{len(flips)} of {len(GRID)} g values -> H7 {'FRAGILE' if fragile else 'not fragile'}")
    return 0


HS: tuple = ()
XS: tuple = ()

if __name__ == "__main__":
    sys.exit(main())
