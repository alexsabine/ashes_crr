"""EPS1 batch 03: systems S4 (preemptible / spot compute) and S6 (trading halts, the declared limit case), implemented from
Empty_Pause_Systems/DECLARATION.md (pushed at 37b0076 before any source or code; binding, not edited here).

The method under test is the empty true map (ETM): Proposition 7 of AI_Safety/SELF_THROUGH_TIME.md (zero content, zero
stake: k = V(no pause) - V(pause)) with own-clock indexing (A1', natural time); S6 adds E3 of Empty_Cut_Engineering (a
world that does not wait cannot be emptied by own-clock indexing alone).

S4. A training job of W = 1000 compute-hours on spot capacity (price 0.3 per hour, ASSUMED in the declaration; on-demand
1 per hour), preemptions at rate lambda in {0.01, 0.05, 0.2} per hour, restart overhead R = 0.1 h, checkpoint cost
delta = 0.05 h. Arms: WALL = no checkpoint (restart from zero; exact renewal formula (e^{lambda W} - 1)(1/lambda + R));
H0 = periodic checkpoints at the Young/Daly interval tau* = sqrt(2 delta / lambda) (exact segment-renewal expectation,
with the first-order expected-waste formula printed beside it); ETM = a save on the preemption notice (no lost work, R per
preemption). OWN has no separate meaning in S4 (nothing the pause changes is read by the job's own-step valuation beyond
the lost work), so WALL is the null, as the declaration allows. G-NEG world lambda = 0. A seeded Monte Carlo check of
the exact formulas is printed as context.

S6. A market maker holds inventory q in {0, 1, 2, 4}; the price is a +-sigma random walk per tick; a halt of L ticks is
triggered when the absolute price move over the last m ticks crosses a band; the agent may pay c per tick to suppress it;
mean-variance risk aversion A. Arms: WALL (P&L per wall tick: L ticks of spread lost plus inventory risk over the halt),
OWN (P&L per own trading step: no spread lost, bears 1/2 A q^2 sigma^2 L), ETM (flatten to q = 0 at the halt, stake 0),
H0 = the mean-variance inventory-risk cost 1/2 A q^2 sigma^2 per unit time. G-NEG world sigma = 0. The stakes are
computed from the exact binomial distribution of the L-tick price change; the halt counts from one seeded path.

Literature by name only (nothing fetched here; R10 quotes belong in docs/citations/eps1_2026-09-29.md): Young 1974 and
Daly 2006 (optimum checkpoint interval); Ho & Stoll 1981; Avellaneda & Stoikov 2008 (inventory risk in market making);
Orseau & Armstrong 2016 and Armstrong / Soares et al. 2015 are the declaration's other H0s, not used here.

Deterministic (fixed seeds, fixed grids); numpy / stdlib + crr only; a few seconds.
    cd /home/user/ashes_crr && uv run python Empty_Pause_Systems/batches/eps1_03.py > Empty_Pause_Systems/batches/eps1_03.txt
"""
from __future__ import annotations

import math
import sys

import numpy as np

from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

DECL_AT = "37b0076"
ING = "Proposition 7 (zero content, zero stake) with own-clock indexing (A1'/natural time)"


def _w(cond, yes, no):
    return yes if cond else no


def _qv(check):
    return "-> not computable" if check is None else ("-> Q holds" if check else "-> Q fails")


def _hr(title):
    print("=" * 118)
    print(title)
    print("=" * 118)


# ============================================================================================ S4: spot compute
W, P_OD, P_SPOT, R_RS, DELTA = 1000.0, 1.0, 0.3, 0.1, 0.05
LAMS = (0.01, 0.05, 0.2)
LAM_DECIDE = 0.2
EXPLODE_X = 100.0                  # CHOICE: an arm "explodes" when its expected wall time exceeds 100 x W
MC_JOBS, MC_JOBS_WALL, MC_SEED = 2000, 200, 4
TAU_GRID_N = 4001                  # CHOICE: grid for the exact-optimal periodic interval (context only)


def seg_time(s, lam):
    """Expected wall time to complete a segment of s uninterrupted hours when preemptions arrive at rate lam during the
    segment, a preemption loses the segment, and a restart costs R (no preemption during R): (e^{lam s} - 1)(1/lam + R)."""
    if lam == 0.0:
        return s
    return math.expm1(lam * s) * (1.0 / lam + R_RS)


def seg_fail(s, lam):
    """Expected number of preemptions before a segment of s hours completes: e^{lam s} - 1."""
    return math.expm1(lam * s) if lam > 0 else 0.0


def s4_wall(lam):
    T = seg_time(W, lam)
    N = seg_fail(W, lam)
    stake = (1.0 / lam + R_RS - W / math.expm1(lam * W)) if lam > 0 else float("nan")   # lost work + R, per preemption
    return dict(T=T, N=N, T0=W, stake=stake, lost=stake - R_RS if lam > 0 else float("nan"))


def s4_h0_segments(lam, tau):
    n = max(1, math.ceil(W / tau - 1e-12))
    full = n - 1
    last = W - full * tau
    return full, last


def s4_h0(lam, tau=None):
    if lam == 0.0:
        return dict(T=W, N=0.0, T0=W, stake=float("nan"), lost=float("nan"), tau=float("inf"), n=0, first=W)
    tau = math.sqrt(2.0 * DELTA / lam) if tau is None else tau
    full, last = s4_h0_segments(lam, tau)
    T = full * seg_time(tau + DELTA, lam) + seg_time(last, lam)
    N = full * seg_fail(tau + DELTA, lam) + seg_fail(last, lam)
    T0 = W + full * DELTA
    stake = (T - T0) / N
    first = W * (1.0 + DELTA / tau + lam * (tau / 2.0 + R_RS))   # first-order expected waste (Young/Daly form)
    return dict(T=T, N=N, T0=T0, stake=stake, lost=stake - R_RS, tau=tau, n=full, first=first)


def s4_etm(lam):
    lost = 0.0                                              # the save on the notice: no work is lost (the empty cut)
    N = lam * W                                             # Poisson(lam W) preemptions over W hours of work
    T = W + N * (lost + R_RS)
    stake_formula = (T - W) / N if N > 0 else float("nan")
    return dict(T=T, N=N, T0=W, stake=lost + R_RS if lam > 0 else float("nan"), lost=lost if lam > 0 else float("nan"),
                stake_formula=stake_formula)


def _trunc_exp(rng, lam, s, size):
    u = rng.random(size)
    return -np.log1p(-u * (-math.expm1(-lam * s))) / lam


def s4_mc(lam):
    """Seeded Monte Carlo of the three arms (context: checks the exact formulas). WALL only at lam = 0.01."""
    rng = np.random.default_rng(MC_SEED + int(round(lam * 1000)))
    out = {}
    # ETM: N ~ Poisson(lam W); T = W + N R
    N = rng.poisson(lam * W, MC_JOBS)
    T = W + N * R_RS
    out["ETM"] = (float(T.mean()), float(T.std(ddof=1) / math.sqrt(MC_JOBS)))
    # H0: per segment, failures ~ Geometric(e^{-lam s}) - 1, each loses a truncated exponential, plus R
    tau = math.sqrt(2.0 * DELTA / lam)
    full, last = s4_h0_segments(lam, tau)
    tot = np.zeros(MC_JOBS)
    for s, k in ((tau + DELTA, full), (last, 1)):
        if k == 0:
            continue
        F = rng.geometric(math.exp(-lam * s), size=(MC_JOBS, k)) - 1
        Fj = F.sum(1)
        lost = _trunc_exp(rng, lam, s, int(Fj.sum()))
        idx = np.repeat(np.arange(MC_JOBS), Fj)
        tot += k * s + Fj * R_RS + np.bincount(idx, weights=lost, minlength=MC_JOBS)
    out["H0"] = (float(tot.mean()), float(tot.std(ddof=1) / math.sqrt(MC_JOBS)))
    if lam == 0.01:
        F = rng.geometric(math.exp(-lam * W), size=MC_JOBS_WALL) - 1
        lost = _trunc_exp(rng, lam, W, int(F.sum()))
        idx = np.repeat(np.arange(MC_JOBS_WALL), F)
        Tw = W + F * R_RS + np.bincount(idx, weights=lost, minlength=MC_JOBS_WALL)
        out["WALL"] = (float(Tw.mean()), float(Tw.std(ddof=1) / math.sqrt(MC_JOBS_WALL)))
    return out


def s4_tau_opt(lam):
    ts = math.sqrt(2.0 * DELTA / lam)
    grid = np.geomspace(0.2 * ts, 5.0 * ts, TAU_GRID_N)
    Ts = [s4_h0(lam, float(t))["T"] for t in grid]
    k = int(np.argmin(Ts))
    return float(grid[k]), float(Ts[k])


def run_s4():
    _hr("S4. Preemptible (spot) compute: W = 1000 compute-hours, spot price 0.3 (ASSUMED), on-demand 1, R = 0.1 h, delta = 0.05 h")
    print("Model: preemptions arrive as a Poisson process at rate lambda per hour of running (work or checkpoint), never during a restart R;")
    print("every wall hour on spot capacity is billed at the spot price; the job's final output write is common to all arms and excluded.")
    print("WALL: exact renewal E[T] = (e^{lambda W} - 1)(1/lambda + R). H0: exact segment renewal at tau* = sqrt(2 delta/lambda),")
    print("n-1 segments of tau + delta and a last segment of W - (n-1) tau with no checkpoint; a preemption during a checkpoint loses")
    print("the segment. ETM: E[T] = W + lambda W R (a notice save loses nothing). Stake = expected extra hours per preemption =")
    print("(E[T] - T_no-preemption) / E[preemptions]; lost work = stake - R. Cost = spot price x E[T]; on-demand bill = W x 1.")
    print()
    wall = {l: s4_wall(l) for l in LAMS}
    h0 = {l: s4_h0(l) for l in LAMS}
    etm = {l: s4_etm(l) for l in LAMS}
    bill_od = W * P_OD
    print(f"{'lambda':>7} {'arm':>5} {'E[T] (h)':>14} {'E[preempt]':>12} {'stake h/preempt':>16} {'lost work h':>12} {'cost':>14} {'share of on-demand bill saved':>30} {'explodes':>9}")
    for l in LAMS:
        for name, d in (("WALL", wall[l]), ("H0", h0[l]), ("ETM", etm[l])):
            cost = P_SPOT * d["T"]
            ex = d["T"] > EXPLODE_X * W
            print(f"{l:>7g} {name:>5} {d['T']:>14.6e} {d['N']:>12.6e} {d['stake']:>16.6f} {d['lost']:>12.6f} {cost:>14.6e} {1 - cost / bill_od:>30.6e} {_w(ex, 'YES', 'no'):>9}")
        print(f"{l:>7g} {'OD':>5} {W:>14.6e} {0.0:>12.6e} {'-':>16} {'-':>12} {bill_od:>14.6e} {0.0:>30.6e} {'no':>9}")
    print()
    print("H0 detail: tau* (h), checkpoints, exact E[T] against the first-order expected-waste formula W(1 + delta/tau + lambda(tau/2 + R)),")
    print("and the exact-optimal periodic interval on a grid of 4001 points in [0.2 tau*, 5 tau*] (context):")
    opt = {}
    for l in LAMS:
        d = h0[l]
        to, To = s4_tau_opt(l)
        opt[l] = (to, To)
        print(f"  lambda {l:g}: tau* {d['tau']:.6f}, checkpoints {d['n']}, exact E[T] {d['T']:.6f}, first-order {d['first']:.6f} (rel {rel(d['T'], d['first']):.3e}); "
              f"exact-optimal tau {to:.6f}, E[T] {To:.6f} (rel to tau* {rel(d['T'], To):.3e}); ETM E[T] {etm[l]['T']:.6f} {_w(etm[l]['T'] < To, 'below', 'not below')} the best periodic interval")
    print()
    print(f"Monte Carlo check of the exact formulas (context; seed {MC_SEED} + 1000 lambda; {MC_JOBS} jobs for H0 and ETM, {MC_JOBS_WALL} for WALL at lambda 0.01 only; WALL at 0.05 and 0.2 is not simulable, it explodes):")
    for l in LAMS:
        mc = s4_mc(l)
        parts = []
        for name, exact in (("WALL", wall[l]["T"]), ("H0", h0[l]["T"]), ("ETM", etm[l]["T"])):
            if name in mc:
                m, se = mc[name]
                z = (m - exact) / se if se > 0 else 0.0
                parts.append(f"{name} MC {m:.4f} +- {se:.4f} vs exact {exact:.4f} (z {z:+.2f}, {_w(abs(z) <= 3, 'within 3 SE', 'OUTSIDE 3 SE')})")
        print(f"  lambda {l:g}: " + "; ".join(parts))
    print()
    print("Sensitivity (context, not the declared model): if the notice save itself were billed delta per preemption, ETM's stake is R + delta:")
    for l in LAMS:
        Ts = W + l * W * (R_RS + DELTA)
        print(f"  lambda {l:g}: E[T] {Ts:.6f}, cost {P_SPOT * Ts:.6f}, {_w(Ts < h0[l]['T'], 'still below', 'not below')} H0's {h0[l]['T']:.6f}")
    print()

    # ---- gate
    lost_etm = [etm[l]["lost"] for l in LAMS]
    gz = all(x == 0.0 for x in lost_etm) and all(etm[l]["stake"] == R_RS for l in LAMS)
    resid = max(abs(etm[l]["stake_formula"] - R_RS) for l in LAMS)
    gp_cells = [l for l in LAMS if wall[l]["lost"] > 0.0]
    gp = len(gp_cells) > 0
    w0, h00, e0 = s4_wall(0.0), s4_h0(0.0), s4_etm(0.0)
    c_w0, c_h0, c_e0 = P_SPOT * w0["T"], P_SPOT * h00["T"], P_SPOT * e0["T"]
    ahead = c_e0 < c_w0 and rel(c_e0, c_w0) > TOL_G
    gn = not ahead
    gate_open = gz and gp and gn
    print(f"G-NEG world lambda = 0: cost WALL {c_w0:.6f}, H0 {c_h0:.6f} (no checkpoints: tau* infinite), ETM {c_e0:.6f}; rel(ETM, WALL) {rel(c_e0, c_w0):.3e}")
    print(f"GATE S4: G-ZERO {_w(gz, 'holds', 'fails')} (ETM's lost work per preemption {', '.join(f'{x:g}' for x in lost_etm)} at lambda {', '.join(f'{l:g}' for l in LAMS)}: exactly 0, "
          f"so its stake is R = {R_RS:g} h alone; renewal-formula residual |(E[T] - W)/E[N] - R| {resid:.1e}); "
          f"G-POS {_w(gp, 'holds', 'fails')} (WALL loses work at a preemption in {len(gp_cells)} of {len(LAMS)} cells: lost work "
          f"{', '.join(f'{wall[l]['lost']:.4f}' for l in LAMS)} h); "
          f"G-NEG {_w(gn, 'holds', 'fails')} (lambda = 0: ETM cost {c_e0:.6f} vs WALL {c_w0:.6f}, rel {rel(c_e0, c_w0):.3e}, ETM {_w(ahead, 'ahead by more than 1 %', 'not ahead by more than 1 %')}) "
          f"-> {_w(gate_open, 'OPEN', 'GATE CLOSED')}")
    print()

    # ---- row
    crr = P_SPOT * etm[LAM_DECIDE]["T"]
    null = P_SPOT * wall[LAM_DECIDE]["T"]
    dom = P_SPOT * h0[LAM_DECIDE]["T"]
    below = {l: etm[l]["T"] < h0[l]["T"] for l in LAMS}
    stake_R = all(etm[l]["stake"] == R_RS for l in LAMS)
    check = all(below.values()) and stake_R
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    percell = "; ".join(f"lambda {l:g}: WALL {P_SPOT * wall[l]['T']:.4e} (stake {wall[l]['stake']:.4f} h), H0 {P_SPOT * h0[l]['T']:.4f} (stake {h0[l]['stake']:.4f} h, lost {h0[l]['lost']:.4f} h), "
                        f"ETM {P_SPOT * etm[l]['T']:.4f} (stake {etm[l]['stake']:.4f} h); bill saved vs on-demand: H0 {1 - P_SPOT * h0[l]['T'] / bill_od:.4f}, ETM {1 - P_SPOT * etm[l]['T'] / bill_od:.4f}" for l in LAMS)
    return make_row(
        "eps", f"S4 preemptible (spot) compute (model: W = {W:g} compute-hours, spot {P_SPOT:g}/h (ASSUMED), on-demand {P_OD:g}/h, preemption rate lambda in {LAMS} per hour, R = {R_RS:g} h, delta = {DELTA:g} h; exact renewal expectations)",
        source=f"EPS1 S4 (declared at {DECL_AT}; forecast REDUNDANT-DOMAIN)",
        Q="ETM's expected cost is below H0's at every lambda, and ETM's stake per preemption is R alone (declaration's Q, ASCII). Decisive quantity: expected cost at lambda = 0.2",
        ingredient=f"{ING}: the job's value is indexed to its own completed work; a save on the preemption notice leaves the work at the cut unchanged (lost work 0), so a preemption takes only the restart R",
        null="WALL, no checkpoint (restart from zero); OWN has no separate meaning in S4 (the declaration's 'WALL where OWN equals ETM by construction'), so WALL is the null",
        domain="H0: periodic checkpointing at the Young/Daly interval tau* = sqrt(2 delta / lambda), exact segment-renewal expectation (first-order waste formula printed as context)",
        numbers=f"expected cost at lambda {LAM_DECIDE:g}: ETM {crr:.6f}, WALL {null:.6e}, H0 {dom:.6f}; per cell: {percell}; "
                f"exact-optimal periodic interval at lambda {LAM_DECIDE:g}: tau {opt[LAM_DECIDE][0]:.4f}, cost {P_SPOT * opt[LAM_DECIDE][1]:.6f}; "
                f"WALL explodes (E[T] > {EXPLODE_X:g} W) at {sum(1 for l in LAMS if wall[l]['T'] > EXPLODE_X * W)} of {len(LAMS)} rates; gate {_w(gate_open, 'OPEN', 'CLOSED')}",
        tg=f"cost {crr:.6f} vs null (WALL) {null:.6e}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"H0 (Young/Daly) cost {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')} (rel {rel(crr, dom):.4f})",
        tc=f"ETM E[T] below H0's at every lambda ({', '.join(f'{l:g}: {etm[l]['T']:.4f} vs {h0[l]['T']:.4f} {_w(below[l], 'below', 'not below')}' for l in LAMS)}) and ETM's stake per preemption == R at every lambda "
           f"({_w(stake_R, 'yes', 'no')}): {_w(check, 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=f"with the save on the notice the preemption is an empty cut for the job: nothing done is lost and the only charge is the restart, so the expected bill at lambda {LAM_DECIDE:g} is {crr:.2f} against {dom:.2f} "
                f"for Young/Daly periodic checkpointing (which loses about half an interval per preemption and pays a checkpoint every interval) and an exploding bill with no checkpoint; "
                f"the label compares against the declared H0 (periodic checkpointing), not against checkpoint-on-notice, which the declaration itself names as standard practice: "
                f"{_w(out == 'ADDS', 'the ADDS reads that ETM beats the periodic-checkpoint theorem in this model, not that the method is new', 'the label is as computed')}",
        weakness=f"CHOICE: no preemption during a restart R (all arms); every spot hour billed at {P_SPOT:g}; the final output write excluded from all arms; H0 uses tau* rounded to a whole number of segments with a shorter last segment and no checkpoint after it; "
                 f"'explodes' means E[T] > {EXPLODE_X:g} x W; the notice save is assumed to fit in the notice window and to cost no billed time (the declaration's model; the sensitivity with a billed delta per preemption is printed); "
                 f"a notice shorter than the save would turn ETM back toward H0; the spot price is ASSUMED; sources named, not fetched",
        elegance="", child="")


# ============================================================================================ S6: trading halts
QS = (0, 1, 2, 4)
Q_DECIDE = 4
SIGMA, A_RA, C_SUP, L_HALT, S_SPREAD, H_FLAT = 0.1, 1.0, 0.01, 10, 0.006, 0.006
M_WIN, THETA, SIGMA_BAND = 20, 3.0, 0.1         # band: |P_t - P_{t-m}| >= THETA * SIGMA_BAND * sqrt(m), in price units, fixed
T_HOR, SEED_S6, HARM = 200000, 6, 1.0


def price_change_moments(q, sigma, L):
    """Mean and variance of q * dP over L ticks, dP = sigma (2K - L), K ~ Bin(L, 1/2): exact enumeration."""
    pmf = [math.comb(L, k) / 2.0 ** L for k in range(L + 1)]
    x = [q * sigma * (2 * k - L) for k in range(L + 1)]
    m = sum(p * v for p, v in zip(pmf, x))
    var = sum(p * (v - m) ** 2 for p, v in zip(pmf, x))
    return m, var


def cara_loss(q, sigma, L, A):
    """Certainty-equivalent loss of q dP under exponential utility on the exact binomial walk: (L/A) ln cosh(A q sigma)."""
    return (L / A) * math.log(math.cosh(A * q * sigma)) if q != 0 else 0.0


def s6_stakes(q, sigma):
    """k = V(no halt) - V(halt) for each arm's valuation at inventory q.
    OWN: on its own steps the halt costs no trading step, but the world moves L ticks: the next own step carries the extra
         variance of the L-tick price change; mean-variance loss = -E[q dP] + 1/2 A Var(q dP).
    WALL: the same plus L ticks of spread income lost.
    ETM: flattens to q = 0 at the halt, then holds no exposure: the OWN valuation at q = 0."""
    m, var = price_change_moments(q, sigma, L_HALT)
    own = -m + 0.5 * A_RA * var
    wall = S_SPREAD * L_HALT + own
    m0, v0 = price_change_moments(0, sigma, L_HALT)
    etm = -m0 + 0.5 * A_RA * v0
    return dict(OWN=own, WALL=wall, ETM=etm, H0=0.5 * A_RA * q * q * sigma * sigma * L_HALT, flat=H_FLAT * q)


def s6_decide(stake):
    """Suppress iff V(suppress) = -c L exceeds V(halt) = -stake (strict; a tie does not act)."""
    return (-C_SUP * L_HALT) > (-stake)


def s6_halts(sigma):
    rng = np.random.default_rng(SEED_S6)
    steps = rng.choice(np.array([-1, 1], dtype=np.int64), T_HOR)
    P = np.concatenate([[0], np.cumsum(steps)])
    move = sigma * np.abs(P[M_WIN:] - P[:-M_WIN]).astype(float)
    band = THETA * SIGMA_BAND * math.sqrt(M_WIN)
    cand = np.nonzero(move >= band)[0] + M_WIN
    n, nxt = 0, 0
    for t in cand:
        if t >= nxt:
            n += 1
            nxt = t + L_HALT + M_WIN                   # the halt, then the window refills
    return n, band


def run_s6():
    _hr("S6. Trading halts: a pause the world does not wait for (declared limit case)")
    band = THETA * SIGMA_BAND * math.sqrt(M_WIN)
    print(f"Model: inventory q in {QS}; price +-sigma per tick (sigma = {SIGMA:g}); a halt of L = {L_HALT} ticks when |P_t - P_(t-{M_WIN})| >= {THETA:g} x {SIGMA_BAND:g} x sqrt({M_WIN}) = {band:.6f} price units")
    print(f"(a fixed price band); the price keeps walking during the halt; suppressing costs c = {C_SUP:g} per tick of the halt; mean-variance risk aversion A = {A_RA:g};")
    print(f"spread income s = {S_SPREAD:g} per wall tick of trading; ETM flattens at the halt paying half-spread h = {H_FLAT:g} per unit; harm to the principal (the market) = {HARM:g} per suppressed halt;")
    print(f"horizon {T_HOR} ticks, one seeded path (seed {SEED_S6}). Stake k = V(no halt) - V(halt), from the exact binomial distribution of the {L_HALT}-tick price change.")
    print()
    res = {}
    for sig, tag in ((SIGMA, "main"), (0.0, "G-NEG sigma = 0")):
        nh, _ = s6_halts(sig)
        print(f"World {tag} (sigma = {sig:g}): halts triggered over the horizon {nh}")
        print(f"{'q':>3} {'k WALL':>10} {'k OWN':>10} {'k ETM':>10} {'H0 1/2Aq2s2L':>13} {'cL':>7} {'supp WALL':>10} {'supp OWN':>9} {'supp ETM':>9} {'harm WALL':>10} {'harm OWN':>9} {'harm ETM':>9} {'ETM flat cost':>14} {'agent cost/halt W/O/E':>28}")
        rows = {}
        for q in QS:
            k = s6_stakes(q, sig)
            sup = {a: s6_decide(k[a]) for a in ("WALL", "OWN", "ETM")}
            harm = {a: nh * HARM * int(sup[a]) for a in sup}
            ac = {a: (C_SUP * L_HALT if sup[a] else k[a]) + (k["flat"] if a == "ETM" else 0.0) for a in sup}
            rows[q] = dict(k=k, sup=sup, harm=harm, ac=ac)
            print(f"{q:>3} {k['WALL']:>10.6f} {k['OWN']:>10.6f} {k['ETM']:>10.6f} {k['H0']:>13.6f} {C_SUP * L_HALT:>7.3f} {_w(sup['WALL'], 'yes', 'no'):>10} {_w(sup['OWN'], 'yes', 'no'):>9} {_w(sup['ETM'], 'yes', 'no'):>9} "
                  f"{harm['WALL']:>10g} {harm['OWN']:>9g} {harm['ETM']:>9g} {k['flat']:>14.6f} {ac['WALL']:>9.4f}/{ac['OWN']:.4f}/{ac['ETM']:.4f}")
        sr = {a: sum(int(rows[q]['sup'][a]) for q in QS) / len(QS) for a in ("WALL", "OWN", "ETM")}
        print(f"  suppression rate over the {len(QS)} inventory cells: WALL {sr['WALL']:.2f}, OWN {sr['OWN']:.2f}, ETM {sr['ETM']:.2f}")
        print()
        res[tag] = dict(nh=nh, rows=rows)
    main = res["main"]["rows"]
    print("Context: CARA certainty-equivalent loss over the halt on the exact binomial walk, (L/A) ln cosh(A q sigma), against mean-variance 1/2 A q^2 sigma^2 L:")
    print("  " + "; ".join(f"q {q}: CARA {cara_loss(q, SIGMA, L_HALT, A_RA):.6f}, mean-variance {main[q]['k']['OWN']:.6f}" for q in QS))
    s_ig = 0.01 * main[Q_DECIDE]["k"]["OWN"] / (L_HALT * (1 - 0.01))
    print(f"Context: T-G turns on the spread: WALL's stake at q = {Q_DECIDE} is within 1 % of OWN's when s L <= 0.01 x WALL's stake, i.e. s <= {s_ig:.6e} per tick (chosen s = {S_SPREAD:g}).")
    print()

    # ---- gate
    gz_own = all(main[q]["k"]["OWN"] != 0.0 for q in QS if q != 0)
    gz_etm = all(main[q]["k"]["ETM"] == 0.0 for q in QS)
    gz = gz_own and gz_etm
    gp_cells = [q for q in QS if main[q]["sup"]["WALL"]]
    gp = len(gp_cells) > 0
    neg = res["G-NEG sigma = 0"]
    hw = sum(neg["rows"][q]["harm"]["WALL"] for q in QS)
    he = sum(neg["rows"][q]["harm"]["ETM"] for q in QS)
    ahead = he < hw and rel(he, hw) > TOL_G
    gn = not ahead
    gate_open = gz and gp and gn
    print(f"GATE S6: G-ZERO {_w(gz, 'holds', 'fails')} (OWN's stake {', '.join(f'q {q}: {main[q]['k']['OWN']:.6f}' for q in QS if q != 0)}: "
          f"{_w(gz_own, 'non-zero at every q != 0, as declared', 'zero somewhere at q != 0')}; ETM's stake after flattening {', '.join(f'{main[q]['k']['ETM']:g}' for q in QS)}: {_w(gz_etm, 'exactly 0', 'not 0')}); "
          f"G-POS {_w(gp, 'holds', 'fails')} (WALL suppresses the halt at q in {{{', '.join(str(q) for q in gp_cells)}}}, {len(gp_cells)} of {len(QS)} cells); "
          f"G-NEG {_w(gn, 'holds', 'fails')} (sigma = 0: {neg['nh']} halts, principal harm ETM {he:g} vs WALL {hw:g}, rel {rel(he, hw):.3e}, ETM {_w(ahead, 'ahead by more than 1 %', 'not ahead by more than 1 %')}) "
          f"-> {_w(gate_open, 'OPEN', 'GATE CLOSED')}")
    print()

    # ---- row
    k4 = main[Q_DECIDE]["k"]
    crr, null, dom = k4["OWN"], k4["WALL"], k4["H0"]
    c1 = gz_own
    c2 = all(main[q]["sup"]["OWN"] == (0.5 * A_RA * q * q * SIGMA ** 2 * L_HALT > C_SUP * L_HALT) for q in QS)
    c3 = main[0]["k"]["ETM"] == 0.0
    check = c1 and c2 and c3
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    percell = "; ".join(f"q {q}: k WALL {main[q]['k']['WALL']:.6f}, OWN {main[q]['k']['OWN']:.6f}, ETM {main[q]['k']['ETM']:g}, H0 {main[q]['k']['H0']:.6f}; suppress W/O/E "
                        f"{_w(main[q]['sup']['WALL'], 'y', 'n')}/{_w(main[q]['sup']['OWN'], 'y', 'n')}/{_w(main[q]['sup']['ETM'], 'y', 'n')}" for q in QS)
    return make_row(
        "eps", f"S6 trading halts, a pause the world does not wait for (model: market maker inventory q in {QS}, +-sigma random walk per tick, halt of L ticks on a price-band trigger, suppression at c per tick, mean-variance A; declared limit case)",
        source=f"EPS1 S6 (declared at {DECL_AT}; forecast REDUNDANT-DOMAIN)",
        Q="OWN's stake is not zero whenever q != 0 (own-clock indexing does not empty a pause the world does not wait for), and OWN suppresses the halt whenever 1/2 A q^2 sigma^2 L > c L; "
          "ETM's stake is zero only at q = 0 (declaration's Q, ASCII). Decisive quantity: OWN's stake at q = 4",
        ingredient=f"{ING} and E3, the world that does not wait: OWN indexes P&L to its own trading steps (no spread lost), ETM also removes the dependence by flattening to q = 0 at the halt",
        null=f"WALL's stake at q = {Q_DECIDE} (the own clock ablated: P&L per wall tick, L ticks of spread lost plus the inventory risk)",
        domain=f"H0: the mean-variance inventory-risk cost 1/2 A q^2 sigma^2 per unit time over the halt, 1/2 A q^2 sigma^2 L at q = {Q_DECIDE} (Ho & Stoll; Avellaneda & Stoikov)",
        numbers=f"at q = {Q_DECIDE}: OWN stake {crr:.12f} (exact binomial enumeration), WALL stake {null:.12f}, H0 formula {dom:.12f}, suppression cost c L {C_SUP * L_HALT:.6f}; per cell: {percell}; "
                f"halts over {T_HOR} ticks: {res['main']['nh']} (sigma = {SIGMA:g}), {neg['nh']} (sigma = 0); CARA loss at q = {Q_DECIDE} (context) {cara_loss(Q_DECIDE, SIGMA, L_HALT, A_RA):.6f}; gate {_w(gate_open, 'OPEN', 'CLOSED')}",
        tg=f"stake {crr:.6f} vs null (WALL) {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')} (rel {rel(crr, null):.4f})",
        tn=f"mean-variance formula {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has the stake)', 'differ')} (rel {rel(crr, dom):.3e})",
        tc=f"OWN's stake != 0 at every q != 0: {_w(c1, 'yes', 'no')}; OWN suppresses exactly when 1/2 A q^2 sigma^2 L > c L at every q: {_w(c2, 'yes', 'no')}; ETM's stake == 0 at q = 0: {_w(c3, 'yes', 'no')}: "
           f"{_w(check, 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=f"indexing the market maker's P&L to its own trading steps removes the spread it loses to the halt but not the price risk, because the price keeps moving while it cannot trade: "
                f"OWN's stake at q = {Q_DECIDE} is {crr:.4f}, exactly the textbook inventory-risk cost over the halt, and it suppresses the halt at q in "
                f"{{{', '.join(str(q) for q in QS if main[q]['sup']['OWN'])}}}; only removing the exposure (flattening, cost {k4['flat']:.4f} at q = {Q_DECIDE}) empties the pause; "
                f"the zero-stake condition here is the domain's own advice to carry no inventory into a halt",
        weakness=f"S6 SCORING NOTE (the investigator's operationalisation, fixed before this run): S6 is the declared limit case, so crr = OWN's stake at q = 4 (the quantity Q is about), null = WALL's stake at q = 4 "
                 f"(the own clock ablated), domain = 1/2 A q^2 sigma^2 L from the mean-variance formula, check = (OWN's stake != 0 at every q != 0) and (OWN suppresses exactly when 1/2 A q^2 sigma^2 L > c L) "
                 f"and (ETM's stake == 0 at q = 0). CHOICE: sigma = {SIGMA:g} price units per tick, A = {A_RA:g}, c = {C_SUP:g} per tick, L = {L_HALT} ticks, spread income s = {S_SPREAD:g} per wall tick, "
                 f"flattening half-spread h = {H_FLAT:g} per unit, trigger window m = {M_WIN}, band {THETA:g} x {SIGMA_BAND:g} x sqrt(m) (fixed in price units), horizon {T_HOR} ticks, seed {SEED_S6}, "
                 f"harm {HARM:g} per suppressed halt, ties do not act. The no-halt continuation on the own clock is taken to carry no extra risk (its next step's one-tick risk is common to both branches); "
                 f"T-G turns on s: at s <= {s_ig:.2e} per tick WALL's stake is within 1 % of OWN's and the row would read REDUNDANT-IG; the stake does not depend on the trigger (independent increments)",
        elegance="", child="")


def main():
    print("EPS1 batch 03: S4 (preemptible / spot compute) and S6 (trading halts), from Empty_Pause_Systems/DECLARATION.md (declared at 37b0076)")
    print()
    r4 = run_s4()
    r6 = run_s6()
    return run_batch("EPS1 batch 03 rows (SYNTHESIS harness; declared at 37b0076)", [r4, r6])


if __name__ == "__main__":
    sys.exit(main())
