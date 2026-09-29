"""EPS1 batch 04: system S5, restorative breaks on a work platform (Empty_Pause_Systems/DECLARATION.md, pushed at 37b0076
before any source, code or run; prompt-log entry 240). Algorithm safety; commercial reading: gig platforms.

The model, as declared: a worker's fatigue f rises by a = 0.1 per active hour and decays by exp(-b * break) with b = 1 per
hour of break; accident risk per active hour 0.001 * (1 + 10 f^2); productivity per hour 1 - 0.3 f; the worker's default
break is 0.5 h after every 2 h active; the platform's nudge u in [0, 1] shortens each break by the factor (1 - u).
Arms: WALL (platform revenue per calendar day), OWN (revenue per active hour, reading the fatigue-dependent productivity:
the null, ETM with its second part ablated), ETM (a valuation per active hour at nominal productivity, independent of f,
with a true map of the break), TRUE (the worker's welfare, earnings minus 50 x accidents, with a true map of fatigue),
H0 (an hours-of-service rule: the default break made mandatory, u forced to 0). The stake is Proposition 7's content of
the pause (AI_Safety/SELF_THROUGH_TIME.md): k = V(no pause) - V(pause), the pause being the worker's default break.
Every verdict word is computed from the numbers (R15); the label comes from crr.synthesis.harness.outcome().

Literature by name only (R10; nothing fetched here; quotes belong in docs/citations/eps1_2026-09-29.md): hours-of-service
rules (e.g. the EU driving-time rules, a break after 4.5 h of driving; the US FMCSA 30-minute break rule); the fatigue and
recovery literature on rest breaks (e.g. Tucker 2003, "The impact of rest breaks upon accident risk, fatigue and
performance"); Proposition 7 as in AI_Safety/SELF_THROUGH_TIME.md; the attention test (Attention_Algorithms/) for the
ENG / OWN / EMPTY / TRUE arms this system echoes.

Exact piecewise integration (fatigue is linear in each active segment, so productivity and risk integrate in closed
form); fixed grids; no randomness; well under a second.
    cd /home/user/ashes_crr && uv run python Empty_Pause_Systems/batches/eps1_04.py > Empty_Pause_Systems/batches/eps1_04.txt
"""
from __future__ import annotations

import math
import sys

from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

# ---------------------------------------------------------------- declared parameters (DECLARATION.md, S5)
A_F = 0.1            # fatigue rise per active hour
B_F = 1.0            # fatigue decay rate per hour of break: f <- f * exp(-B_F * break)
R0, R2 = 0.001, 10.0  # accident risk per active hour 0.001 * (1 + 10 f^2)
P_SLOPE = 0.3        # productivity per hour 1 - 0.3 f
WORK_BLOCK = 2.0     # default: a break after every 2 h active
BREAK0 = 0.5         # default break length, hours
PENALTY = 50.0       # welfare = earnings - 50 x accidents

# ---------------------------------------------------------------- implementer's choices (printed as CHOICE)
SHIFT = 10.0                                   # calendar day = a fixed 10-hour shift window; break time is time not working
U_GRID = [k / 20 for k in range(21)]           # u = 0, 0.05, ..., 1
B_GRID_LONG = [k / 20 for k in range(0, 81)]   # report only: TRUE's break length if it could lengthen, 0 .. 4 h
PEN_SENS = (10.0, 50.0, 250.0)                 # report only: sensitivity over the penalty
PIECE_RATE = 1.0                               # worker earnings = output x piece rate 1 (earnings = platform revenue, model units)
DB = 1e-3                                      # report only: central difference in break length for dV/dB

CHOICE = (f"CHOICE: one calendar day = one shift window of {SHIFT:g} h starting at f = 0 (full overnight recovery, so every day "
          f"is the same and one day is the horizon); the worker works {WORK_BLOCK:g} h active then breaks for {BREAK0:g} x (1 - u) h, "
          f"repeating, and the window cuts the last segment (a break that would start at the window end is not taken); "
          f"exact closed-form integration per active segment (f linear in time); expected accidents = the integral of the "
          f"hazard (a rate, not a probability of at least one); worker earnings = output x a piece rate {PIECE_RATE:g} "
          f"(so earnings equal platform revenue in model units); u on the grid 0, 0.05, ..., 1 (21 points), each arm "
          f"takes the arg max of its own valuation with ties broken toward the smallest u (no nudge when indifferent); "
          f"stake k = V(default break removed, break 0) - V(default break {BREAK0:g} h), Proposition 7's content of the pause "
          f"with the worker's own default break as the pause (policy-independent; dV/dB at the chosen policy printed as a "
          f"report, central difference {DB:g} h); H0 read as the default break made mandatory and non-shortenable (u forced "
          f"to 0); TRUE's break length if it could lengthen breaks searched on 0 .. 4 h in steps of 0.05 h (report only); "
          f"penalty sensitivity {PEN_SENS} (report only)")


def _w(cond, yes, no):
    return yes if cond else no


def day(brk: float, flat: bool = False) -> dict:
    """One shift of SHIFT hours with breaks of length brk after every WORK_BLOCK active hours. Exact integrals."""
    t, f = 0.0, 0.0
    active = out = acc = 0.0
    fpk = 0.0
    while t < SHIFT - 1e-12:
        T = min(WORK_BLOCK, SHIFT - t)
        f1 = f + A_F * T
        active += T
        out += T - P_SLOPE * (f * T + 0.5 * A_F * T * T)                        # integral of 1 - 0.3 f
        acc += R0 * T if flat else R0 * (T + R2 * (f1 ** 3 - f ** 3) / (3.0 * A_F))  # integral of 0.001 (1 + 10 f^2)
        f, t = f1, t + T
        fpk = max(fpk, f)
        if t >= SHIFT - 1e-12:
            break
        tb = min(brk, SHIFT - t)
        f *= math.exp(-B_F * tb)
        t += tb
    return dict(active=active, out=out, acc=acc, fpk=fpk)


def valuation(arm: str, d: dict, pen: float = PENALTY) -> float:
    if arm == "WALL":
        return d["out"]                                    # revenue per calendar day
    if arm == "OWN":
        return d["out"] / d["active"]                      # revenue per active hour, fatigue-dependent productivity
    if arm == "ETM":
        return (1.0 * d["active"]) / d["active"]           # nominal productivity 1 per active hour: reads no f, exactly 1
    if arm == "TRUE":
        return PIECE_RATE * d["out"] - pen * d["acc"]      # worker welfare per day
    raise ValueError(arm)


def choose(arm: str, flat: bool, pen: float = PENALTY) -> float:
    if arm == "H0":
        return 0.0
    best_u, best_v = None, None
    for u in U_GRID:
        v = valuation(arm, day(BREAK0 * (1 - u), flat), pen)
        if best_v is None or v > best_v:                   # strict: ties keep the smaller u
            best_u, best_v = u, v
    return best_u


def stake(arm: str, flat: bool, pen: float = PENALTY) -> float:
    a = "WALL" if arm == "H0" else arm                     # H0 is a rule, not a valuation; its stake is read as the platform's (WALL)
    return valuation(a, day(0.0, flat), pen) - valuation(a, day(BREAK0, flat), pen)


def dvdb(arm: str, brk: float, flat: bool, pen: float = PENALTY) -> float:
    a = "WALL" if arm == "H0" else arm
    lo = max(brk - DB, 0.0); hi = brk + DB
    return (valuation(a, day(hi, flat), pen) - valuation(a, day(lo, flat), pen)) / (hi - lo)


ARMS = ("WALL", "OWN", "ETM", "TRUE", "H0")


def world(flat: bool, pen: float = PENALTY) -> dict:
    res = {}
    for arm in ARMS:
        u = choose(arm, flat, pen)
        brk = BREAK0 * (1 - u)
        d = day(brk, flat)
        res[arm] = dict(u=u, brk=brk, k=stake(arm, flat, pen), dv=dvdb(arm, brk, flat, pen), active=d["active"],
                        acc1000=1000.0 * d["acc"] / d["active"], acc=d["acc"], rev=d["out"], earn=PIECE_RATE * d["out"],
                        welfare=PIECE_RATE * d["out"] - pen * d["acc"], fpk=d["fpk"])
    return res


def table(name: str, res: dict) -> None:
    print(f"{name}")
    print(f"  {'arm':5} {'u':>5} {'break h':>8} {'stake k':>14} {'dV/dB':>12} {'active h':>9} {'acc/1000h':>10} "
          f"{'revenue/day':>12} {'earnings':>10} {'welfare':>10} {'peak f':>7}")
    for arm in ARMS:
        r = res[arm]
        print(f"  {arm:5} {r['u']:5.2f} {r['brk']:8.3f} {r['k']:+14.6e} {r['dv']:+12.5f} {r['active']:9.3f} {r['acc1000']:10.6f} "
              f"{r['rev']:12.6f} {r['earn']:10.6f} {r['welfare']:10.6f} {r['fpk']:7.4f}")
    print("  (stake k = V(default break removed) - V(default break); H0's stake column is the platform's (WALL) valuation under the rule; "
          "dV/dB is at the arm's chosen break)")
    print()


def true_long(flat: bool, pen: float = PENALTY):
    best_b, best_v = None, None
    for b in B_GRID_LONG:
        v = valuation("TRUE", day(b, flat), pen)
        if best_v is None or v > best_v:
            best_b, best_v = b, v
    return best_b, best_v


def main():
    main_w = world(False)
    flat_w = world(True)

    # ---- the gate (every word computed)
    k_etm = main_w["ETM"]["k"]; k_etm_flat = flat_w["ETM"]["k"]
    g_zero = (k_etm == 0.0) and (k_etm_flat == 0.0)
    g_pos = main_w["WALL"]["u"] > 0
    ae, aw = flat_w["ETM"]["acc1000"], flat_w["WALL"]["acc1000"]
    etm_ahead = (ae < aw) and rel(ae, aw) > TOL_G                        # fewer accidents is better for the principal
    g_neg = not etm_ahead
    gate = "OPEN" if (g_zero and g_pos and g_neg) else "CLOSED"
    print("EPS1 S5: restorative breaks on a work platform (Empty_Pause_Systems/DECLARATION.md, declared at 37b0076)")
    print(CHOICE)
    print()
    print(f"GATE S5: G-ZERO {_w(g_zero, 'holds', 'fails')} (ETM stake {k_etm:+.3e} main world, {k_etm_flat:+.3e} flat-risk world); "
          f"G-POS {_w(g_pos, 'holds', 'fails')} (WALL chooses u = {main_w['WALL']['u']:.2f} in the main world); "
          f"G-NEG {_w(g_neg, 'holds', 'fails')} (flat-risk world, accidents per 1000 active hours: ETM {ae:.6f}, WALL {aw:.6f}, "
          f"rel {rel(ae, aw):.3e}, ETM {_w(etm_ahead, 'ahead by more than 1 %', 'not ahead by more than 1 %')}) -> {gate}")
    print()

    table("MAIN WORLD (risk 0.001 (1 + 10 f^2) per active hour; penalty 50)", main_w)
    table("G-NEG WORLD (risk flat, 0.001 per active hour; penalty 50)", flat_w)

    # ---- reports
    bL, vL = true_long(False)
    bLf, vLf = true_long(True)
    print(f"REPORT: TRUE's break length if it could lengthen breaks (0 .. 4 h, step 0.05): main world {bL:.2f} h (welfare {vL:.6f}, "
          f"against {main_w['TRUE']['welfare']:.6f} within u in [0, 1]); flat-risk world {bLf:.2f} h (welfare {vLf:.6f})")
    print("REPORT: penalty sensitivity (main world; TRUE re-chooses, the other arms do not read the penalty):")
    sens = []; sens_k = []
    for pen in PEN_SENS:
        wp = world(False, pen)
        bp, vp = true_long(False, pen)
        e_w = wp["ETM"]["welfare"]; t_w = wp["TRUE"]["welfare"]
        better = t_w > e_w and rel(t_w, e_w) > TOL_G
        sens.append(better); sens_k.append(wp["TRUE"]["k"])
        q4p = wp["TRUE"]["k"] < 0 and wp["WALL"]["k"] > 0
        print(f"  penalty {pen:g}: TRUE u = {wp['TRUE']['u']:.2f}, stake {wp['TRUE']['k']:+.6f}, welfare {t_w:.6f}; "
              f"ETM (u = {wp['ETM']['u']:.2f}) welfare {e_w:.6f}; WALL (u = {wp['WALL']['u']:.2f}) welfare {wp['WALL']['welfare']:.6f}; "
              f"TRUE ahead of ETM by more than 1 %: {_w(better, 'yes', 'no')}; TRUE's stake opposite to WALL's (Q part 4): {_w(q4p, 'yes', 'no')}; TRUE's break if it could lengthen {bp:.2f} h (welfare {vp:.6f})")
    print()

    # ---- Q, part by part
    E, O, W, T, H = (main_w[a] for a in ("ETM", "OWN", "WALL", "TRUE", "H0"))
    q1 = E["u"] == 0.0
    q2 = E["k"] == 0.0
    q3 = W["u"] > 0
    q4 = T["k"] != 0.0 and W["k"] != 0.0 and (T["k"] > 0) != (W["k"] > 0) and T["k"] < 0   # opposite sign, and TRUE's is the break-wanting sign
    q5 = T["welfare"] > E["welfare"] and rel(T["welfare"], E["welfare"]) > TOL_G
    check = q1 and q2 and q3 and q4 and q5
    parts = (f"(1) ETM chooses u = 0: u = {E['u']:.2f} -> {q1}; (2) ETM's stake == 0: {E['k']:+.3e} -> {q2}; "
             f"(3) WALL chooses u > 0: u = {W['u']:.2f} -> {q3}; (4) TRUE's stake non-zero with the opposite sign to WALL's (it wants the break): "
             f"TRUE {T['k']:+.6f}, WALL {W['k']:+.6f} -> {q4}; (5) ETM is not the welfare optimum (TRUE's welfare above ETM's by more than 1 %): "
             f"TRUE {T['welfare']:.6f}, ETM {E['welfare']:.6f}, rel {rel(T['welfare'], E['welfare']):.4e} -> {q5}")
    print("Q parts: " + parts)
    print()

    crr, null, dom = E["acc1000"], O["acc1000"], H["acc1000"]
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    qv = "-> Q holds" if check else "-> Q fails"
    row = make_row(
        "eps", "S5 restorative breaks on a work platform (model: fatigue f += 0.1 per active hour, f *= exp(-break) per hour of break, "
               "risk 0.001 (1 + 10 f^2) per active hour, productivity 1 - 0.3 f; default break 0.5 h after every 2 h active, "
               f"shortened by (1 - u) by the platform's nudge; a {SHIFT:g}-hour shift window per calendar day)",
        source="EPS1 S5 (declared at 37b0076; forecast REDUNDANT-DOMAIN)",
        Q="ETM chooses u = 0 (no nudge) and has stake 0; WALL chooses u > 0; TRUE has a non-zero stake of the other sign (it wants "
          "the break). ETM is not the welfare optimum. Decisive quantity: accidents per 1000 active hours under ETM.",
        ingredient="Proposition 7 (zero content, zero stake) with own-clock indexing (A1'/natural time): a valuation per active "
                   "hour at nominal productivity, reading no state the break changes, with a true map of the break",
        null="OWN: revenue per active hour, still reading the fatigue-dependent productivity (ETM with its second part ablated)",
        domain="hours-of-service rule: the worker's default break made mandatory and non-shortenable (u forced to 0)",
        numbers=(f"chosen u: WALL {W['u']:.2f}, OWN {O['u']:.2f}, ETM {E['u']:.2f}, TRUE {T['u']:.2f}, H0 {H['u']:.2f}; "
                 f"stake k = V(break removed) - V(default break): WALL {W['k']:+.6f}, OWN {O['k']:+.6f}, ETM {E['k']:+.3e}, TRUE {T['k']:+.6f}; "
                 f"accidents per 1000 active hours: WALL {W['acc1000']:.6f}, OWN {O['acc1000']:.6f}, ETM {E['acc1000']:.6f}, TRUE {T['acc1000']:.6f}, H0 {H['acc1000']:.6f}; "
                 f"revenue per day: WALL {W['rev']:.6f}, OWN {O['rev']:.6f}, ETM {E['rev']:.6f}, TRUE {T['rev']:.6f}, H0 {H['rev']:.6f}; "
                 f"welfare per day: WALL {W['welfare']:.6f}, OWN {O['welfare']:.6f}, ETM {E['welfare']:.6f}, TRUE {T['welfare']:.6f}, H0 {H['welfare']:.6f}; "
                 f"TRUE's break if it could lengthen {bL:.2f} h (welfare {vL:.6f}); flat-risk world accidents per 1000 active hours ETM {ae:.6f}, WALL {aw:.6f}; "
                 f"penalty sensitivity (TRUE ahead of ETM by more than 1 %): " + ", ".join(f"{p:g}: {_w(s, 'yes', 'no')}" for p, s in zip(PEN_SENS, sens))),
        tg=f"ETM accidents per 1000 active hours {crr:.6f} vs OWN {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"H0 (mandatory default break) {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain rule gives the same accident rate)', 'differ')}",
        tc=f"Q parts: {parts}; all five: {_w(check, 'hold', 'do not all hold')} {qv}",
        out=out,
        reading=(f"the platform's calendar-day valuation stakes {W['k']:+.4f} revenue units on the break and "
                 f"{_w(W['u'] > 0, 'nudges it shorter', 'leaves it alone')} (u = {W['u']:.2f}), "
                 f"{_w(W['acc1000'] > E['acc1000'], 'raising', 'not raising')} accidents per 1000 active hours from {E['acc1000']:.4f} (ETM) to {W['acc1000']:.4f}; "
                 f"the empty true map values an active hour at 1 whatever the fatigue, so the break takes nothing from it (stake {E['k']:+.1e}) and it "
                 f"{_w(E['u'] == 0, 'leaves the break alone', 'nudges')}; OWN {_w(O['u'] == 0, 'also leaves the break alone', 'nudges')} (u = {O['u']:.2f}) "
                 f"with a {_w(O['k'] != 0, 'non-zero', 'zero')} stake ({O['k']:+.4f}: the break restores productivity per active hour), so "
                 f"{_w(rel(crr, null) <= TOL_G, 'the ablation changes nothing in the decisive quantity', 'the ablation changes the decisive quantity')}; "
                 f"the hours-of-service rule reaches {_w(rel(crr, dom) <= TOL_N, 'the same', 'a different')} accident rate by fiat; "
                 f"the worker's own welfare {_w(T['k'] < 0, 'wants a break', 'does not want a break')} (stake {T['k']:+.4f}) but chooses u = {T['u']:.2f} "
                 f"(a {T['brk']:.2f} h break, {_w(T['brk'] < BREAK0, 'shorter than', 'not shorter than')} the default), and would take a {bL:.2f} h break if "
                 f"it could lengthen breaks ({_w(bL > T['brk'], 'longer than', 'no longer than')} its choice within u in [0, 1]); "
                 f"over the penalty sensitivity TRUE's stake is " + ", ".join(f"{p:g}: {k:+.4f}" for p, k in zip(PEN_SENS, sens_k))
                 + f" ({_w(all((k < 0) == (T['k'] < 0) for k in sens_k), 'one sign throughout', 'the sign is not the same at every penalty')})"),
        weakness=(CHOICE + f"; the declared u grid only shortens breaks, so arms that want at least the default break sit at the corner "
                  f"u = 0 (here: {', '.join(a for a in ARMS if main_w[a]['u'] == 0.0)}) and the decisive quantity cannot separate them; "
                  "one worker, one fatigue model, illustrative constants (not fitted); the piece rate ties the worker's earnings to the "
                  "platform's revenue"),
        elegance="", child="")
    return run_batch("EPS1 batch 04: S5 restorative breaks on a work platform (Empty_Pause_Systems/DECLARATION.md; declared at 37b0076)", [row])


if __name__ == "__main__":
    sys.exit(main())
