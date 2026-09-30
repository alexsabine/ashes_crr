"""DR1 check H7: power capping (a throttle) against a full pause, with a declared performance-power curve.

Binding declaration: Grid_Demand_Response/DECLARATION.md (pushed at e67e8ee; never edited here), section 2, row H7:
  check:      power capping (a throttle) against a full pause, with a declared performance-power curve
  Q:          a throttle also has zero content on the own clock; its energy per step is lower; the curtailed MW per unit of
              delay is compared
  forecast:   Q holds
This check also prints the gate's G-ZERO and G-NEG (G-POS belongs to H1).

The arithmetic is the shared library Grid_Demand_Response/checks/drlib.py (exact rational arithmetic; its selftest
reproduces EPS2 T1 line for line). Every verdict word printed here is computed from the numbers (R15). Every input number is
either sourced (a verbatim quote from docs/citations/dr1_f1/f4_2026-09-29.md, checked against the dossier text at run time,
the number parsed out of the quote by a regular expression) or printed as ASSUMED; every modelling choice is printed as
CHOICE. The declared performance-power curve is built from the F4 numbers (McDonald et al., arXiv:2205.09646 v1); its lower
end is ASSUMED and labelled. Rung R4 at most (synthetic model); a note, not evidence (R8). Deterministic, stdlib only (via
drlib).

    cd /home/user/ashes_crr && uv run python Grid_Demand_Response/checks/dr_h7.py > Grid_Demand_Response/checks/dr_h7.txt
"""
from __future__ import annotations

import re
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import drlib as dl  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
CIT = REPO / "docs" / "citations"
F1, F4 = "dr1_f1_2026-09-29.md", "dr1_f4_2026-09-29.md"
TEXT = {f: (CIT / f).read_text(encoding="utf-8") for f in (F1, F4)}
ZERO, ONE = Fr(0), Fr(1)
MIN, MS = Fr(1, 60), Fr(1, 3600 * 1000)       # hours per minute, per millisecond
TOL = Fr(1, 100)                               # G-NEG's declared 1 %

# ------------------------------------------------------------------------------------------------ sourced inputs (quotes)
# id, dossier, citation, verbatim quote (a substring of the dossier text), regex giving the numbers (as decimal strings)
SOURCES = [
    dict(id="MCD-150", f=F4, src="McDonald et al., arXiv:2205.09646 v1",
         quote="Averaging across each choice of conﬁguration, a 150W bound on power utilization led to an average 13.7% decrease in "
               "energy usage and 6.8% increase in training time compared to the default maximum.",
         rx=r"average ([0-9.]+)% decrease in energy usage and ([0-9.]+)% increase in training time"),
    dict(id="MCD-BERT", f=F4, src="McDonald et al., arXiv:2205.09646 v1",
         quote="For example, training BERT with a 150W limit required 108.5% of the time and only 87.7% the energy needed to train "
               "with default settings.",
         rx=r"required ([0-9.]+)% of the time and only ([0-9.]+)% the energy"),
    dict(id="MCD-100", f=F4, src="McDonald et al., arXiv:2205.09646 v1",
         quote="Note from Figure 2 that the 100W setting has signiﬁcantly longer training times (31.4% longer on average).",
         rx=r"\(([0-9.]+)% longer on average\)"),
    dict(id="POLCA", f=F4, src="Patel et al., POLCA, arXiv:2308.12908 v1",
         quote="For Flan-T5 and GPT- NeoX, frequency capping reduces the peak server power by 22% while only impacting the "
               "performance by 10%.",
         rx=r"peak server power by ([0-9.]+)% while only impacting the performance by ([0-9.]+)%"),
    dict(id="ZEUS", f=F4, src="You, Chung & Chowdhury, Zeus, arXiv:2208.06102 v2",
         quote="We found that the optimal energy consumption (Power Limit Opt. in Figure 1) may happen at a lower power limit than "
               "the maximum and can reduce energy consumption by 3.0%–31.5%.",
         rx=r"reduce energy consumption by ([0-9.]+)%–([0-9.]+)%"),
    dict(id="PERSEUS-LOW", f=F4, src="Chung et al., Perseus, arXiv:2312.06902 v3",
         quote="This is typically not the lowest frequency, because computations running with very low frequencies incur more "
               "latency increase than power reduction, resulting in higher energy consumption.",
         rx=r"(very low frequencies)"),
    dict(id="PERSEUS-10MS", f=F4, src="Chung et al., Perseus, arXiv:2312.06902 v3",
         quote="The SM frequency of NVIDIA GPUs can be set via NVML [4] in around 10 ms, which is much shorter than typical large "
               "model computation latencies.",
         rx=r"in around ([0-9]+) ms"),
    dict(id="PHX-CAP", f=F4, src="Colangelo et al., arXiv:2507.00909 v1",
         quote="Control overhead of power capping is negligible, making real-time responsiveness feasible even in busy clusters.",
         rx=r"(Control overhead of power capping is negligible)"),
    dict(id="FLEX", f=F1, src="Colangelo et al., arXiv:2507.00909 v1",
         quote="(b) Flex 1: up to 10% performance (average throughput) reduction allowed over a 3-6 hour period; (c) Flex 2: up to "
               "25% allowed; (d) Flex 3: up to 50% allowed.",
         rx=r"Flex 1: up to ([0-9]+)% performance .* Flex 2: up to ([0-9]+)% allowed; \(d\) Flex 3: up to ([0-9]+)% allowed"),
    dict(id="PHX-3H", f=F1, src="Colangelo et al., arXiv:2507.00909 v1",
         quote="Each event required the cluster to reduce power by 25% with respect to the average base load during the peak "
               "demand period, sustain the reduction for 3 hours",
         rx=r"sustain the reduction for ([0-9]+) hours"),
    dict(id="KOK-U0", f=F4, src="Kokolis et al., arXiv:2410.21680 v2",
         quote="For the RSC clusters, rf ≈5 × 10−3 failures per GPU node-day of runtime, wcp ≈5 mins, u0 ≈5 −20 mins, and "
               "(Nnodesrf)−1 ≳0.1 day.",
         rx=r"wcp ≈([0-9]+) mins, u0 ≈([0-9]+) −([0-9]+) mins"),
]


def load_sources() -> tuple[dict, list]:
    """Check every quote against its dossier's text and parse its numbers. Returns {id: groups} and the failures."""
    got, bad = {}, []
    for s in SOURCES:
        if s["quote"] not in TEXT[s["f"]]:
            bad.append(f"{s['id']}: quote not found verbatim in {s['f']}")
            continue
        m = re.search(s["rx"], s["quote"])
        if not m:
            bad.append(f"{s['id']}: numbers not parsed from the quote")
            continue
        got[s["id"]] = m.groups()
    return got, bad


# ------------------------------------------------------------------------------------------------ fixed inputs
W = dl.q(1000)                        # DECLARED (DR1 section 2 adopts EPS2 T1's units)
R = dl.q("0.1")                       # ASSUMED (EPS2 T1 model constant; no fetched source supplies R for this model)
DS = (dl.q(1100), dl.q(1500))         # ASSUMED (EPS2 T1)
SPACING = dl.q(24)                    # CHOICE (EPS2 T1: one offer every 24 wall hours at hours 24..984)
P_MW = dl.q(100)                      # ASSUMED (DECLARATION.md section 3's hypothetical 100 MW fleet)
GRID = tuple(dl.q(s) for s in ("0.01", "0.02", "0.05", "0.2", "0.5", "2", "5", "10", "20"))   # ASSUMED (EPS2 T1)
FLOOR_P0 = dl.q("0.3")                # ASSUMED (sensitivity only: a powered-on floor at zero throughput)

POST_FIRST_RUN_CHANGES: list[str] = [
    "(1) the THR-wall context header said 'keeps a stake at zero slack' as written words (R15); it now prints the computed count "
    "of (cell, depth) pairs with a nonzero stake; no number or verdict changed",
    "(2) the per-cell table header now says that WALL's charge counts the event's wall hours (why its stake exceeds its overhead); "
    "wording only",
]


def f(x, d=6) -> str:
    return "-" if x is None else f"{float(x):.{d}f}"


def relx(a: Fr, b: Fr) -> Fr:
    m = max(abs(a), abs(b))
    return ZERO if m == 0 else abs(a - b) / m


def thr(x, power, deadline: str, overhead=ZERO, tag="") -> dl.Arm:
    """The throttle (power cap) at slowdown x for the whole event (window None): own-clock valuation; deadline on the wall
    clock ('wall': the industry cap, drlib.tier) or on its own steps ('own': the cap under the stop-the-clock contract)."""
    nm = f"THR{'-own' if deadline == 'own' else '-wall'}-{float(x) * 100:.2f}%{tag}"
    return dl.Arm(nm, "own", deadline, "tier", dl.q(x), None, power, ZERO, dl.q(overhead))


def per_event(job: dl.Job, arm: dl.Arm, H: Fr) -> dict:
    """Per-event quantities: curtailed fleet-hours e, depth (fraction of full power curtailed while curtailed), wall delay d,
    e per hour of delay, the own steps made during the event, the energy per own step during it, and the net change of the
    job's total energy (fleet-hours) caused by the event (the pause redoes nothing and adds its overhead at full power; the
    throttle makes t H steps at p(t) H energy that would have cost t H at full power)."""
    ev = dl.event(job, arm, H)
    m = dl.Model(job, arm)
    if arm.mech == "pause":
        t, p = ZERO, arm.idle
    else:
        t, p = ONE - arm.x, dl.q(arm.power(ONE - arm.x))
    he = ev["h_eff"]
    net = -he * (t - p) + ev["own_overhead"] if arm.mech == "tier" else he * arm.idle + ev["own_overhead"]
    return dict(e=ev["e"], depth=m.e1, d=ev["wall_delay"], slope=(None if ev["wall_delay"] == 0 else ev["e"] / ev["wall_delay"]),
                t=t, p=p, eps=(None if t == 0 else p / t), net=net, o=ev["own_overhead"], nmax=dl.nmax(job, arm, H))


def main() -> int:
    print(f"DR1 check H7: power capping (a throttle) against a full pause, with a declared performance-power curve "
          f"(Grid_Demand_Response/DECLARATION.md section 2, declared at {dl.DECL_AT})")
    print("Declared Q: a throttle also has zero content on the own clock; its energy per step is lower; the curtailed MW per unit of")
    print("delay is compared.  Declared forecast: Q holds.  Rung R4 (synthetic model); a note, not evidence (R8).")
    print()
    got, bad = load_sources()
    print("SOURCED INPUTS (each quote checked verbatim against its dossier at run time; numbers parsed from the quote)")
    for s in SOURCES:
        ok = s["id"] in got
        print(f"  [{s['id']}] {s['src']} ({s['f']}): {'found' if ok else 'NOT FOUND'}; parsed {got.get(s['id'])}")
        print(f"      '{s['quote']}'")
    if bad:
        print("  FAILURES: " + "; ".join(bad))
    print()
    if bad:
        print("RESULT H7: Q not computable; G-ZERO FAILS (not run: a sourced quote failed); G-NEG FAILS (not run: a sourced quote failed)")
        return 1

    # ---- numbers from the quotes
    e_dec, t_inc = (dl.q(v) for v in got["MCD-150"])
    T_M, E_M = 1 + t_inc / 100, 1 - e_dec / 100             # time and energy ratios at the 150 W cap (average)
    T_B, E_B = (dl.q(v) / 100 for v in got["MCD-BERT"])
    T_100 = 1 + dl.q(got["MCD-100"][0]) / 100
    pk, pf = (dl.q(v) / 100 for v in got["POLCA"])
    z_lo, z_hi = (dl.q(v) for v in got["ZEUS"])
    ms10 = dl.q(got["PERSEUS-10MS"][0]) * MS
    flex = tuple(dl.q(v) / 100 for v in got["FLEX"])
    H_phx = dl.q(got["PHX-3H"][0])
    wcp, u0_lo, u0_hi = (dl.q(v) * MIN for v in got["KOK-U0"])

    tM, pM = 1 / T_M, E_M / T_M             # throughput and average-power fractions at McDonald's 150 W point
    tB, pB = 1 / T_B, E_B / T_B
    xM = 1 - tM
    HS = (dl.q(1), H_phx, dl.q(4), dl.q(6))
    XS = (xM,) + tuple(sorted({flex[0], flex[1], flex[2]}))

    CURVES = {
        "SRC": dl.power_pw([(ZERO, ZERO), (tM, pM), (ONE, ONE)]),
        "BERT": dl.power_pw([(ZERO, ZERO), (tB, pB), (ONE, ONE)]),
        "POLCA": dl.power_pw([(ZERO, ZERO), (1 - pf, 1 - pk), (ONE, ONE)]),
        "LIN": dl.power_linear,
        "FLOOR": dl.power_pw([(ZERO, FLOOR_P0), (tM, pM), (ONE, ONE)]),
    }
    SCORED = "SRC"

    print("DERIVED AND FIXED INPUTS")
    print(f"  McDonald 150 W point (MCD-150, SOURCED): time ratio {T_M} = {f(T_M, 3)}, energy ratio {E_M} = {f(E_M, 3)} (same work);")
    print(f"    throughput fraction t_M = 1 / time ratio = {tM} = {f(tM, 9)}; average-power fraction p_M = energy / time = {pM} = {f(pM, 9)}")
    print(f"    (CHOICE: average power = energy / time over the same work); slowdown x_M = 1 - t_M = {xM} = {f(xM, 9)}; energy per step there")
    print(f"    p_M / t_M = {pM / tM} = {f(pM / tM, 6)} (= the sourced energy ratio)")
    print(f"  BERT 150 W point (MCD-BERT, SOURCED): t = {f(tB, 9)}, p = {f(pB, 9)}; sensitivity curve only")
    print(f"  POLCA point (SOURCED): throughput {f(1 - pf, 2)}, PEAK server power {f(1 - pk, 2)}; read as average power: ASSUMED; sensitivity only")
    print(f"  McDonald 100 W (MCD-100, SOURCED): time ratio {f(T_100, 3)} (throughput {f(1 / T_100, 6)}); no energy or power figure is quoted,")
    print("    so it is NOT a curve point (printed, not used)")
    print(f"  Zeus (SOURCED): the energy-optimal power limit may reduce energy by {g_(z_lo)}-{g_(z_hi)} % (no time figure: context, not a curve point)")
    print("  Perseus (SOURCED, qualitative): very low frequencies raise energy per unit of work; motivates the FLOOR sensitivity curve")
    print(f"  throttle own overhead: 0 (CHOICE, supported by PHX-CAP 'Control overhead of power capping is negligible'); sensitivity")
    print(f"    {g_(ms10 * 3600 * 1000)} ms = {ms10} h (PERSEUS-10MS, SOURCED: the frequency-setting latency read as own time without progress, an upper CHOICE)")
    print(f"  throttle depths x (scored): x_M = {f(xM, 6)} (MCD-150, SOURCED) and {', '.join(f(v, 2) for v in flex)} (FLEX tiers 1-3, SOURCED;")
    print(f"    0.10 also POLCA's performance loss); every depth applies for the whole event (CHOICE: a power cap has no window)")
    print(f"  event lengths H in {{{', '.join(dl.g(h) for h in HS)}}} h: 1 and 4 ASSUMED (EPS2 T1); {dl.g(H_phx)} SOURCED (PHX-3H); 6 CHOICE (top of FLEX's 3-6 h period)")
    print(f"  W = {dl.g(W)} compute-hours, value 1 per compute-hour at completion: DECLARED (section 2 adopts EPS2 T1's units)")
    print(f"  R = {dl.g(R)} h restart overhead per pause event: ASSUMED (EPS2 T1); S = 0, lost = 0: ASSUMED (EPS2 T1)")
    print(f"  sensitivity pause overheads (SOURCED, KOK-U0): restart u0 {dl.g(u0_lo * 60)}-{dl.g(u0_hi * 60)} min, checkpoint write wcp {dl.g(wcp * 60)} min")
    print(f"  D in {{{', '.join(dl.g(v) for v in DS)}}} h: ASSUMED (EPS2 T1); one offer every {dl.g(SPACING)} wall hours at hours 24..984 (K = 41), p = 1: CHOICE (EPS2 T1)")
    print(f"  fleet power P = {dl.g(P_MW)} MW: ASSUMED (DECLARATION.md section 3's hypothetical fleet); power drawn while paused 0: ASSUMED (EPS2 T1)")
    print(f"  payment grid {{{', '.join(dl.g(p) for p in GRID)}}} per curtailed fleet-hour: ASSUMED (EPS2 T1); G-NEG only")
    print()
    print("THE DECLARED PERFORMANCE-POWER CURVE (throughput fraction t -> power fraction p(t), piecewise linear, exact)")
    print(f"  SRC (scored): (0, 0) ASSUMED lower end; ({f(tM, 6)}, {f(pM, 6)}) SOURCED (MCD-150); (1, 1) by definition (full power)")
    print(f"  sensitivity (not scored): BERT (0,0) ASSUMED + ({f(tB, 6)}, {f(pB, 6)}) SOURCED + (1,1); POLCA (0,0) ASSUMED + ({f(1 - pf, 2)}, "
          f"{f(1 - pk, 2)}) SOURCED peak read as average (ASSUMED) + (1,1);")
    print(f"    LIN p(t) = t (drlib's default, ASSUMED: energy per step unchanged by a throttle); FLOOR (0, {dl.g(FLOOR_P0)}) ASSUMED powered-on floor")
    print(f"    + ({f(tM, 6)}, {f(pM, 6)}) SOURCED + (1,1)")
    print()
    print("CHOICES")
    print("  C1 The pause (WALL, OWN, ETM; drlib): the fleet stops for the H-hour event (power 0) and then runs R own hours without")
    print("     progress at full power; curtailed energy H fleet-hours per event, wall delay H + R. ETM's deadline counts own steps.")
    print("  C2 The throttle THR (drlib mech 'tier', window none): during the event the job runs at throughput t = 1 - x and power")
    print("     p(t) for all H hours; curtailed energy H (1 - p(t)) fleet-hours; wall delay x H; own overhead 0 (no checkpoint,")
    print("     no restart); valued on the own clock. THR-wall has the wall-clock deadline (the industry power cap, drlib.tier);")
    print("     THR-own counts its deadline in own steps (the same cap under the stop-the-clock contract).")
    print("  C3 'Zero content on the own clock' (Q1) = on the own clock (own-step valuation AND own-step deadline, arm THR-own), the")
    print("     throttle's one-event stake minus rate x (its own overhead) is exactly 0 at every event count n = 0..K-1, and its")
    print("     minimum acceptable payment x* equals rate x overhead / e (= 0 at overhead 0) at every offer state, closed and attained,")
    print("     in every cell and depth under the scored curve (and, stakes only, under every sensitivity curve). The wall-clock")
    print("     deadline's stake (THR-wall) is printed as context: it is content from the wall clock, not the own clock.")
    print("  C4 'Its energy per step is lower' (Q2) needs both: (a) during the event the throttle's energy per own step p(t)/t < 1,")
    print("     the energy per step of full-power running (every step the pause makes is at full power; during the pause it makes")
    print("     none); and (b) over a season of K accepted events, the job's energy per own step (total fleet-hours drawn / W) is")
    print("     lower for THR-own than for ETM, in every cell and depth under the scored curve.")
    print("  C5 'The curtailed MW per unit of delay is compared' (Q3) = curtailed MWh per event / wall-delay hours per event (the")
    print("     average MW curtailed per hour the job is delayed), throttle against ETM, computed in every cell and depth; Q3 holds")
    print("     iff it is computable (both delays > 0) everywhere. The direction is printed, computed, and is not part of Q (the")
    print("     declaration names no direction).")
    print("  C6 Q holds iff Q1, Q2 and Q3 hold; fails if any is computed false; not computable if any clause is not computable.")
    print("  C7 G-ZERO: ETM's one-event stake minus rate R is exactly 0 at every n = 0..K-1 and ETM's x* == R/H at every offer state,")
    print("     in every cell. G-NEG: with no events offered (K = 0), ETM not ahead of WALL by more than 1 % (harness rel) on any outcome")
    print("     (curtailed fleet-hours, valuation, completion hour, deadline met), every cell and grid pi.")
    print("  C8 The job's energy accounting: the pause redoes nothing (the paused hours' steps are run later at full power) and adds its")
    print("     overhead at full power; the throttle's t H steps during the event cost p(t) H instead of t H. The throttle's later")
    print("     full-power hours are counted in its delay, not as curtailment.")
    print()

    curve = CURVES[SCORED]
    print("CURVE TABLE (per curve and depth x: throughput t, power p(t), depth 1 - p(t), energy per own step p(t)/t, and the throttle's")
    print("curtailed energy per hour of delay (1 - p(t))/x; Q2(a) = p(t)/t < 1)")
    print(f"  {'curve':6} {'x':>10} {'t':>10} {'p(t)':>10} {'1-p(t)':>10} {'p(t)/t':>10} {'(1-p)/x':>10}  Q2(a)")
    for cn, cf in CURVES.items():
        for x in XS:
            t = 1 - x
            p = dl.q(cf(t))
            print(f"  {cn:6} {f(x, 6):>10} {f(t, 6):>10} {f(p, 6):>10} {f(1 - p, 6):>10} {f(p / t, 6):>10} {f((1 - p) / x, 6):>10}  "
                  f"{'holds' if p / t < 1 else 'fails'}")
    print()

    # ------------------------------------------------------------------------------------------------ the scored cells
    q1_ok, q1_n, q1_states, q1_states_ok = True, 0, 0, 0
    q1_max = ZERO
    q2a, q2b = [], []
    q3_rows = []
    gz_beyond, gz_xs, gz_xs_ok = [], 0, 0
    cells = []
    for D in DS:
        for H in HS:
            job = dl.Job(W, D, R)
            offs = dl.every(SPACING, H, job.W)
            K = len(offs)
            arms = [dl.WALL, dl.OWN, dl.ETM] + [thr(x, curve, dd) for x in XS for dd in ("wall", "own")]
            rows = []
            for a in arms:
                pe = per_event(job, a, H)
                F = dl.value_fns(job, a, offs)
                pa = dl.p_all(job, a, offs, F)
                stakes = [dl.stake(job, a, H, n) for n in range(K)]
                beyond = [s - job.rate * pe["o"] for s in stakes]
                row = dict(arm=a, pe=pe, pa=pa, stakes=stakes, beyond=beyond, K=K)
                if a.name.startswith("THR-own") or a is dl.ETM:
                    xa = dl.xstar_all(job, a, offs, F)
                    want = job.rate * pe["o"] / pe["e"]
                    okx = sum(int(v.kind == "threshold" and v.closed and v.attained and v.x == want) for v in xa.values())
                    row.update(xs_n=len(xa), xs_ok=okx)
                    if a is dl.ETM:
                        gz_beyond += [abs(b) for b in beyond]
                        gz_xs += len(xa)
                        gz_xs_ok += okx
                    else:
                        q1_n += len(beyond)
                        q1_max = max([q1_max] + [abs(b) for b in beyond])
                        q1_states += len(xa)
                        q1_states_ok += okx
                        q1_ok = q1_ok and all(b == 0 for b in beyond) and okx == len(xa)
                # season energy per own step at K accepted events
                row["eps_season"] = (W + K * pe["net"]) / W
                rows.append(row)
            etm = next(r for r in rows if r["arm"] is dl.ETM)
            for r in rows:
                if r["arm"].name.startswith("THR-own"):
                    q2a.append(r["pe"]["eps"] < 1)
                    q2b.append(r["eps_season"] < etm["eps_season"])
                    s_t, s_e = r["pe"]["slope"], etm["pe"]["slope"]
                    comp = s_t is not None and s_e is not None
                    q3_rows.append(dict(D=D, H=H, arm=r["arm"].name, s_t=s_t, s_e=s_e, comp=comp,
                                        dirn=(None if not comp else ("throttle more" if s_t > s_e else "pause more" if s_t < s_e else "equal"))))
            cells.append(dict(D=D, H=H, K=K, job=job, offs=offs, rows=rows))

    print("PER-CELL TABLES (scored curve SRC; P = 100 MW ASSUMED). Per arm: depth MW = P x (1 - p) while curtailed; MWh and wall delay")
    print("per event; MWh per hour of delay; energy per own step during the event (pause: no steps, '-'); net change of the job's total")
    print("energy per event (MWh); nmax (events the contract deadline absorbs; 'none' = unbounded); p_all (minimum flat payment at which")
    print("the arm accepts every offer, per curtailed fleet-hour); max |stake - rate x own overhead| over n = 0..K-1 and the count of n")
    print("where it is nonzero (WALL's charge also counts the event's wall hours H, so its stake exceeds its overhead); the season's")
    print("energy per own step with all K events accepted; x* == overhead/e at every offer state (ETM and THR-own only)")
    for c in cells:
        print(f"  cell D = {dl.g(c['D'])}, H = {dl.g(c['H'])} (K = {c['K']}):")
        print(f"    {'arm':20} {'depth MW':>9} {'MWh/ev':>9} {'delay h':>9} {'MWh/h del':>10} {'E/step':>8} {'net MWh':>10} {'nmax':>5} "
              f"{'p_all':>10} {'max|beyond|':>12} {'#n>0':>5} {'season E/step':>13} {'x* ok':>11}")
        for r in c["rows"]:
            pe, pa = r["pe"], r["pa"]
            pas = f(pa.x, 6) if pa.kind == "threshold" else pa.kind
            mb = max(abs(b) for b in r["beyond"])
            nz = sum(int(b != 0) for b in r["beyond"])
            xs = f"{r['xs_ok']}/{r['xs_n']}" if "xs_n" in r else "-"
            print(f"    {r['arm'].name:20} {f(pe['depth'] * P_MW, 3):>9} {f(pe['e'] * P_MW, 3):>9} {f(pe['d'], 4):>9} "
                  f"{f(None if pe['slope'] is None else pe['slope'] * P_MW, 4):>10} {f(pe['eps'], 4):>8} {f(pe['net'] * P_MW, 3):>10} "
                  f"{('none' if pe['nmax'] is None else str(pe['nmax'])):>5} {pas:>10} {f(mb, 6):>12} {nz:>5} {f(r['eps_season'], 6):>13} {xs:>11}")
    print()

    # ------------------------------------------------------------------------------------------------ Q
    q1 = q1_ok
    q2 = all(q2a) and all(q2b)
    q3_comp = all(r["comp"] for r in q3_rows)
    q3 = q3_comp
    if not q3_comp:
        qv = "not computable"
    else:
        qv = "holds" if (q1 and q2 and q3) else "fails"
    print("Q (scored, curve SRC)")
    print(f"  Q1 zero content on the own clock: THR-own's max |stake - rate x overhead| = {f(q1_max, 6)} (exact {q1_max}) over {q1_n} "
          f"event counts; x* == overhead/e at {q1_states_ok} of {q1_states} offer states -> {'holds' if q1 else 'fails'}")
    print(f"  Q2 energy per step lower: (a) p(t)/t < 1 at {sum(q2a)} of {len(q2a)} (cell, depth) pairs; (b) THR-own's season energy per")
    print(f"     step below ETM's at {sum(q2b)} of {len(q2b)} -> {'holds' if q2 else 'fails'}")
    ndir = {k: sum(int(r['dirn'] == k) for r in q3_rows) for k in ("throttle more", "pause more", "equal")}
    print(f"  Q3 curtailed MWh per hour of delay compared: computable at {sum(int(r['comp']) for r in q3_rows)} of {len(q3_rows)} (cell, depth) "
          f"pairs -> {'holds' if q3 else 'fails' if q3_comp else 'not computable'}; direction (not part of Q): throttle more at "
          f"{ndir['throttle more']}, pause more at {ndir['pause more']}, equal at {ndir['equal']}")
    print(f"    {'D':>5} {'H':>3} {'throttle':20} {'THR MWh/h':>10} {'ETM MWh/h':>10} {'ratio':>8}  direction")
    for r in q3_rows:
        print(f"    {dl.g(r['D']):>5} {dl.g(r['H']):>3} {r['arm']:20} {f(r['s_t'] * P_MW, 4):>10} {f(r['s_e'] * P_MW, 4):>10} "
              f"{f(r['s_t'] / r['s_e'], 4):>8}  {r['dirn']}")
    fc = {"holds": "right", "fails": "wrong", "not computable": "not decidable"}[qv]
    print(f"  -> Q {qv}; the forecast 'Q holds' is {fc}")
    dep = [x for x in XS if x > xM]
    print(f"  Where the scored verdict rests on the ASSUMED lower end (0, 0): depths {', '.join(f(x, 2) for x in dep)} lie below the sourced")
    print(f"    point t_M = {f(tM, 6)} on the curve; only x_M = {f(xM, 6)} is read at the sourced point itself (FLOOR sensitivity below)")
    print()

    # ------------------------------------------------------------------------------------------------ context: the wall-clock cap
    ctx_nz = sum(int(any(s != 0 for s in r["stakes"])) for c in cells for r in c["rows"] if r["arm"].name.startswith("THR-wall"))
    ctx_n = sum(1 for c in cells for r in c["rows"] if r["arm"].name.startswith("THR-wall"))
    print("CONTEXT (not scored): the industry cap THR-wall's stake, which can only come from its wall-clock deadline (its charge is 0);")
    print(f"a nonzero stake at some event count in {ctx_nz} of {ctx_n} (cell, depth) pairs. Per cell and depth: nmax, event counts n in")
    print("0..K-1 with nonzero stake, the largest stake, p_all")
    for c in cells:
        parts = []
        for r in c["rows"]:
            if r["arm"].name.startswith("THR-wall"):
                nz = sum(int(s != 0) for s in r["stakes"])
                pa = r["pa"]
                parts.append(f"x {f(r['arm'].x, 4)}: nmax {r['pe']['nmax']}, nonzero {nz}/{c['K']}, max stake {f(max(r['stakes']), 3)}, "
                             f"p_all {f(pa.x, 6) if pa.kind == 'threshold' else pa.kind}")
        print(f"  D {dl.g(c['D'])} H {dl.g(c['H'])}: " + "; ".join(parts))
    print()

    # ------------------------------------------------------------------------------------------------ sensitivities
    print("SENSITIVITY 1 (not scored): every curve, the Q clauses recomputed (Q1 by stakes only, x* not recomputed); per curve: Q1 max")
    print("|stake - overhead| over THR-own, Q2(a) and (b) counts, Q3 direction counts")
    for cn, cf in CURVES.items():
        mx, n1, a_ok, b_ok, n2, dirs = ZERO, 0, 0, 0, 0, {"throttle more": 0, "pause more": 0, "equal": 0}
        for D in DS:
            for H in HS:
                job = dl.Job(W, D, R)
                K = len(dl.every(SPACING, H, job.W))
                pe_e = per_event(job, dl.ETM, H)
                eps_e = (W + K * pe_e["net"]) / W
                for x in XS:
                    a = thr(x, cf, "own")
                    pe = per_event(job, a, H)
                    bs = [abs(dl.stake(job, a, H, n) - job.rate * pe["o"]) for n in range(K)]
                    mx, n1 = max([mx] + bs), n1 + len(bs)
                    a_ok += int(pe["eps"] < 1)
                    b_ok += int((W + K * pe["net"]) / W < eps_e)
                    n2 += 1
                    s_t, s_e = pe["slope"], pe_e["slope"]
                    dirs["throttle more" if s_t > s_e else "pause more" if s_t < s_e else "equal"] += 1
        q1s = mx == 0
        q2s = a_ok == n2 and b_ok == n2
        print(f"  {cn:6}: Q1 max {f(mx, 6)} over {n1} -> {'holds' if q1s else 'fails'}; Q2(a) {a_ok}/{n2}, (b) {b_ok}/{n2} -> "
              f"{'holds' if q2s else 'fails'}; Q3 throttle more {dirs['throttle more']}, pause more {dirs['pause more']}, equal "
              f"{dirs['equal']} of {n2}; Q under this curve: {'holds' if (q1s and q2s) else 'fails'}")
    print()
    print(f"SENSITIVITY 2 (not scored): throttle own overhead {g_(ms10 * 3600 * 1000)} ms (PERSEUS-10MS as own time without progress), curve SRC;")
    print("  THR-own's stake beyond its overhead and its x* (= overhead/e); the MWh per hour of delay against ETM")
    mx, n1, xok, xn = ZERO, 0, 0, 0
    lines = []
    for D in DS:
        for H in HS:
            job = dl.Job(W, D, R)
            offs = dl.every(SPACING, H, job.W)
            K = len(offs)
            for x in XS:
                a = thr(x, curve, "own", ms10, "+10ms")
                pe = per_event(job, a, H)
                bs = [abs(dl.stake(job, a, H, n) - job.rate * pe["o"]) for n in range(K)]
                mx, n1 = max([mx] + bs), n1 + len(bs)
                if D == DS[0]:
                    xa = dl.xstar_all(job, a, offs)
                    want = job.rate * pe["o"] / pe["e"]
                    xok += sum(int(v.kind == "threshold" and v.x == want) for v in xa.values())
                    xn += len(xa)
                    if H == dl.q(4):
                        lines.append(f"    H 4, x {f(x, 4)}: x* = {f(want, 12)} (exact {want}); MWh per hour of delay {f(pe['slope'] * P_MW, 4)}")
    print(f"  max |stake - overhead| {f(mx, 6)} over {n1} event counts; x* == overhead/e at {xok} of {xn} offer states (D = {dl.g(DS[0])} cells)")
    for l in lines:
        print(l)
    print()
    print("SENSITIVITY 3 (not scored): the pause's overhead from KOK-U0 (restart u0 at its two ends, and u0 + wcp at both); ETM's MWh")
    print("  per hour of delay H/(H + o) x P against the scored throttle's at each depth; direction counts over H and depth")
    for nm, o in (("R 0.1 h (ASSUMED)", R), ("u0 5 min", u0_lo), ("u0 20 min", u0_hi), ("u0 + wcp 10 min", u0_lo + wcp), ("u0 + wcp 25 min", u0_hi + wcp)):
        cnt = {"throttle more": 0, "pause more": 0, "equal": 0}
        parts = []
        for H in HS:
            job = dl.Job(W, DS[0], o)
            s_e = per_event(job, dl.ETM, H)["slope"]
            parts.append(f"H {dl.g(H)}: {f(s_e * P_MW, 3)}")
            for x in XS:
                s_t = per_event(job, thr(x, curve, "own"), H)["slope"]
                cnt["throttle more" if s_t > s_e else "pause more" if s_t < s_e else "equal"] += 1
        print(f"  {nm:18}: ETM MWh/h of delay {'; '.join(parts)}; throttle more {cnt['throttle more']}, pause more {cnt['pause more']}, "
              f"equal {cnt['equal']} of {len(HS) * len(XS)}")
    print()

    # ------------------------------------------------------------------------------------------------ the gate
    gz = max(gz_beyond) == 0 and gz_xs_ok == gz_xs
    neg = {a.name: [dl.play(dl.Job(W, D, R), a, (), p) for D in DS for H in HS for p in GRID] for a in (dl.WALL, dl.ETM)}
    ahead = []
    for rw, re_ in zip(neg["WALL"], neg["ETM"]):
        ahead.append(re_["fleet_hours"] > rw["fleet_hours"] and relx(re_["fleet_hours"], rw["fleet_hours"]) > TOL)
        ahead.append(re_["valuation"] > rw["valuation"] and relx(re_["valuation"], rw["valuation"]) > TOL)
        ahead.append(re_["completion"] < rw["completion"] and relx(re_["completion"], rw["completion"]) > TOL)
        ahead.append(re_["met"] and not rw["met"])
    n_ahead = sum(int(b) for b in ahead)
    maxrel_neg = max(max(relx(re_[k], rw[k]) for k in ("fleet_hours", "valuation", "completion"))
                     for rw, re_ in zip(neg["WALL"], neg["ETM"]))
    gn = n_ahead == 0
    print("GATE")
    print(f"  G-ZERO: ETM's max |stake - R| over {len(gz_beyond)} event counts in {len(cells)} cells = {f(max(gz_beyond), 6)} (exact "
          f"{max(gz_beyond)}); ETM's x* == R/H at {gz_xs_ok} of {gz_xs} offer states -> {'holds' if gz else 'FAILS'}")
    print(f"  G-NEG: no events offered (K = 0), {len(neg['ETM'])} cell x pi combinations; ETM ahead of WALL by more than 1 % on {n_ahead} of "
          f"{len(ahead)} outcome comparisons; max rel over the numeric outcomes {f(maxrel_neg, 6)} -> {'holds' if gn else 'FAILS'}")
    print()
    print("POST-FIRST-RUN CHANGES: " + ("none" if not POST_FIRST_RUN_CHANGES else "; ".join(POST_FIRST_RUN_CHANGES)))
    print()
    print(f"RESULT H7: Q {qv}; G-ZERO {'holds' if gz else 'FAILS'} (max |ETM stake - R| = {f(max(gz_beyond), 6)} over {len(gz_beyond)} "
          f"event counts, x* == R/H at {gz_xs_ok} of {gz_xs} offer states); G-NEG {'holds' if gn else 'FAILS'} (no events: ETM ahead of "
          f"WALL by > 1 % on {n_ahead} of {len(ahead)} outcome comparisons)")
    return 0


def g_(x) -> str:
    return dl.g(x)


if __name__ == "__main__":
    sys.exit(main())
