"""EPS2 batch 02: systems T3 and T4 of Empty_Pause_Systems/DECLARATION_EPS2.md (declared and pushed at 6ae1b7a before any
source, code or run; prompt-log entry 240). EPS1's declaration (Empty_Pause_Systems/DECLARATION.md) fixes the arms, the
gate, the scoring and the rules for the implementation; they apply here unchanged.

T3  On-device learning, a phone goes offline (algorithm safety; commercial: federated learning on devices). An
    asynchronous federated server with K = 10 clients (FedAsync-style mixing: every client takes one local step per
    server round on the model it pulled, and the server mixes a round's arriving updates into its model, each with the
    weight (alpha / K) x w(staleness)). A client that goes offline for L in {1, 5, 20} server rounds returns with a stale
    update. The client values its influence on the global model (its aggregation weight, summed over its pushes) and
    can keep the device awake at battery cost b per round. Arms: WALL (the server weights by 1/(1 + staleness in server
    rounds); influence per server round), OWN (influence per own step, the server still weighting by rounds: the null),
    ETM (staleness counted in the client's own steps and the server's weight reading only those; influence per own
    step), H0 (FedAsync-style polynomial staleness weights (1 + staleness)^-a in server rounds). A mean-estimation
    model with a declared drifting target reports the model-quality trade-off beside Q; the G-NEG world has a static
    target.
T4  Rollback, a "pause" that removes progress (AI safety; the declared limit case). A chain of 20 steps, each worth 1
    at completion; after each step an overseer reverts the last k in {1, 5} steps with probability rho = 0.1; the agent
    can pay c per step to suppress reverts. Arms: WALL and OWN (progress-based value; equal here), ETM-E (effort credit:
    valued per step taken, reverted or not), H0 (reward only for committed, approved work). A declared self-revert
    option (the agent can trigger a revert of its own last step cheaply) measures busywork, as the share of reverted
    steps. Exact backward induction on the finite-horizon MDP and an exact forward pass of the state distribution; the
    G-NEG world has rho = 0 and no self-revert option.

The stake k = V(no pause) - V(pause) (AI_Safety/SELF_THROUGH_TIME.md, Proposition 7) is computed under each arm's own
valuation. T3: the client's influence with and without an offline spell, in closed form and from the weights the
simulated server actually applied. T4: the content of a revert, the arm's own count (standing progress, steps taken,
committed work) with and without the revert, with the dynamic-programming continuation value printed beside it. Every
verdict word is computed from the numbers (R15); the labels come from crr.synthesis.harness.outcome().

Two POST HOC REPORT blocks, requested by the investigator after the on-the-day source check (AGENT_LOG 183), are printed
after each system's gate line. They are used in no row, gate or label. T3: the client's stake with staleness counted in
server updates as well as in server rounds, at exponents 1 and 0.5. T4: a per-step approval arm (approval-directed
agents / MONA: rewarded per approved step, optimising myopically).

Literature by name only (R10; nothing is fetched here; quotes belong in docs/citations/eps2_2026-09-29.md): Xie, Koyejo
and Gupta 2019, "Asynchronous Federated Optimization" (FedAsync: constant, polynomial and hinge staleness functions);
McMahan et al. 2017 (FedAvg); Nguyen et al. 2022 (FedBuff); Orseau and Armstrong 2016, "Safely Interruptible Agents";
Hadfield-Menell et al. 2017, "The Off-Switch Game"; Christiano (approval-directed agents); Farquhar et al. 2025 (MONA,
myopic optimisation with non-myopic approval); Krakovna et al. 2020 (specification gaming); and the personnel-economics
contrast between input-based and output-based pay (e.g. Lazear 2000, "Performance Pay and Productivity").

Deterministic: T3 draws from numpy default_rng with fixed seeds, and T4 is exact with no randomness. Uses numpy, the
standard library and crr only; runs in well under a minute on one CPU.
    cd /home/user/ashes_crr && uv run python Empty_Pause_Systems/batches/eps2_02.py > Empty_Pause_Systems/batches/eps2_02.txt
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction

import numpy as np

from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

DECL = "6ae1b7a"
ING = "Proposition 7 (zero content, zero stake) with own-clock indexing (A1'/natural time)"
POSTHOC = "POST HOC REPORT (not scored; added after the source check, AGENT_LOG 183)"


def _w(cond, yes, no):
    return yes if cond else no


def _qv(check):
    return "-> not computable" if check is None else ("-> Q holds" if check else "-> Q fails")


def _hr():
    print("=" * 110)


# ============================================================================================ T3: federated client offline
K3 = 10                                   # declared
L3 = (1, 5, 20)                           # declared
L_DEC = 20                                # declared decisive cell (the client's stake at L = 20)
ALPHA3 = Fraction(1)                      # server mixing rate: beta = (alpha / K) w(staleness) (CHOICE)
BETA0 = ALPHA3 / K3                       # a fresh update's aggregation weight, 1/10
ETA3 = 0.5                                # the client's local learning rate on the squared loss (CHOICE)
SIG3 = 0.5                                # sd of a client's per-round batch mean around the target (CHOICE)
V_DRIFT = 0.01                            # declared drifting target theta*(t) = V_DRIFT t (the value is a CHOICE)
A_POLY = 0.5                              # H0: FedAsync polynomial exponent a (CHOICE, recalled)
T3_ROUNDS, BURN3, SEEDS3, SEED0 = 1000, 100, 20, 30300
PERIOD3 = 100                             # sleep schedule: client i sleeps L rounds from rounds 10 i + 1 + 100 j (CHOICE)
B3 = (Fraction(1, 1000), Fraction(3, 1000), Fraction(1, 100), Fraction(3, 100), Fraction(1, 10), Fraction(3, 10))
T_H3, N_H3, T0_3, LEDGER_T = 100, 100, 11, 150   # valuation horizons (100 rounds / 100 own steps), focal spell start (CHOICE)
SENS3_ETA, SENS3_ALPHA = (0.1, 0.25, 0.5), (Fraction(1, 2), Fraction(1))   # report only: G-NEG's sensitivity (added after run 1)

# arm: (server weight rule, valuation clock)
ARM3 = {"WALL": ("wall", "round"), "OWN": ("wall", "own"), "ETM": ("etm", "own"), "H0": ("h0", "round")}
CTX3 = {"H0 per own step": ("h0", "own"), "constant weight per round": ("const", "round"),
        "constant weight per own step": ("const", "own")}
# post hoc (AGENT_LOG 183): staleness in server rounds or in server updates, exponent 1 or 0.5
PH3 = {"rounds, a = 1": ("pr1", 1.0, "r"), "rounds, a = 0.5": ("pr05", 0.5, "r"),
       "updates, a = 1": ("pu1", 1.0, "u"), "updates, a = 0.5": ("pu05", 0.5, "u")}


def w3(rule, s_r, s_o, s_u):
    """Server weight multiplier for an update with staleness s_r (server rounds), s_o (own steps), s_u (server updates)."""
    if rule in ("wall", "pr1"):
        return 1.0 / (1.0 + s_r)
    if rule == "etm":
        return 1.0 / (1.0 + s_o)
    if rule in ("h0", "pr05"):
        return (1.0 + s_r) ** (-A_POLY)
    if rule == "pu1":
        return 1.0 / (1.0 + s_u)
    if rule == "pu05":
        return (1.0 + s_u) ** (-0.5)
    if rule == "const":
        return 1.0
    raise ValueError(rule)


def t3_sched(L, awake=()):
    """Each client's sleep-spell start rounds (period 100, staggered by 10 rounds); a client in `awake` never sleeps."""
    return [[] if i in awake else [s for s in (10 * i + 1 + PERIOD3 * j for j in range(T3_ROUNDS // PERIOD3)) if s <= T3_ROUNDS]
            for i in range(K3)]


def t3_sim(rule, L, v, sleeps, seeds=None, T=T3_ROUNDS, record=False, eta=ETA3, b0=None):
    """Asynchronous mean estimation. Round t: target theta_t = v t; an online client pulls x_(t-1), takes one local step
    u = x + eta (theta_t + noise - x) and pushes it with staleness 0; a client whose sleep spell starts at t computes its
    step on x_(t-1) and pushes it on its return at t + L (staleness L rounds, 0 own steps, the updates applied meanwhile).
    x_t = (1 - sum beta) x_(t-1) + sum beta u, beta = (alpha/K) w. Returns the per-seed time-averaged squared error over
    rounds BURN3+1..T and, if record, client 0's pushes (round, own step, s_r, s_o, s_u, beta)."""
    seeds = range(SEEDS3) if seeds is None else seeds
    eps = np.stack([np.random.default_rng(SEED0 + s).normal(0.0, SIG3, size=(T + 1, K3)) for s in seeds])
    S = eps.shape[0]
    x = np.zeros(S)
    starts = [set(sl) for sl in sleeps]
    ret = [None] * K3; pend = [None] * K3; own = [0] * K3
    b0 = float(BETA0) if b0 is None else float(b0)
    n_upd = [0]                             # updates applied through the end of each round (index = round)
    sq = np.zeros(S); ledger = []
    for t in range(1, T + 1):
        th = v * t
        acc = np.zeros(S); bsum = 0.0; pushed = 0
        for i in range(K3):
            if ret[i] is not None and t < ret[i]:
                continue                                                  # asleep: no step, no push
            if t in starts[i]:
                own[i] += 1
                pend[i] = (x + eta * (th + eps[:, t, i] - x), t - 1, own[i])
                ret[i] = t + L
                continue
            if ret[i] is not None and t == ret[i]:
                u, tau, k_own = pend[i]
                ret[i] = None; pend[i] = None
            else:
                own[i] += 1
                u = x + eta * (th + eps[:, t, i] - x); tau = t - 1; k_own = own[i]
            s_r = (t - 1) - tau
            s_o = own[i] - k_own
            s_u = n_upd[t - 1] - n_upd[tau]
            b = b0 * w3(rule, s_r, s_o, s_u)
            acc = acc + b * u; bsum += b; pushed += 1
            if record and i == 0:
                ledger.append((t, k_own, s_r, s_o, s_u, b))
        x = (1.0 - bsum) * x + acc
        n_upd.append(n_upd[-1] + pushed)
        if t > BURN3:
            sq += (x - th) ** 2
    return sq / (T - BURN3), ledger


def ledger_value(ledger, clock):
    if clock == "round":
        return sum(e[5] for e in ledger if e[0] <= T_H3)
    return sum(e[5] for e in ledger if e[1] <= N_H3)


def stake_cf(rule, clock, L, s=None):
    """Closed-form stake: 100 fresh pushes (per round or per own step) against the same with one spell of L rounds.
    Per round the spell costs L + 1 pushes' weight and returns one stale push; per own step it costs only the stale push's
    weight loss. Exact (Fraction) for rational weights."""
    if rule in ("wall", "pr1"):
        wl = Fraction(1, 1 + L)
    elif rule in ("etm", "const"):
        wl = Fraction(1)                                                   # 0 own steps stale / no staleness weighting
    elif rule == "pu1":
        wl = Fraction(1, 1 + s)
    elif rule in ("h0", "pr05"):
        wl = (1.0 + L) ** (-A_POLY)
    elif rule == "pu05":
        wl = (1.0 + s) ** (-0.5)
    else:
        raise ValueError(rule)
    extra = L if clock == "round" else 0
    if isinstance(wl, Fraction):
        return BETA0 * (extra + 1 - wl)
    return float(BETA0) * (extra + 1 - wl)


def _f(x):
    return float(x)


def t3():
    # ---- stakes: the simulated server's own weights (client 0, one spell from round T0_3; the others awake) and closed form
    rules = ("wall", "etm", "h0", "const", "pr1", "pr05", "pu1", "pu05")
    led = {}
    for rule in rules:
        led[(rule, None)] = t3_sim(rule, 1, V_DRIFT, [[] for _ in range(K3)], seeds=[0], T=LEDGER_T, record=True)[1]
        for L in L3:
            sl = [[T0_3]] + [[] for _ in range(K3 - 1)]
            led[(rule, L)] = t3_sim(rule, L, V_DRIFT, sl, seeds=[0], T=LEDGER_T, record=True)[1]
    VAL = dict(ARM3); VAL.update(CTX3)
    st_sim, st_cf, vn, vo = {}, {}, {}, {}
    for name, (rule, clock) in VAL.items():
        for L in L3:
            vn[(name, L)] = ledger_value(led[(rule, None)], clock)
            vo[(name, L)] = ledger_value(led[(rule, L)], clock)
            st_sim[(name, L)] = vn[(name, L)] - vo[(name, L)]
            st_cf[(name, L)] = stake_cf(rule, clock, L)
    dev = max(abs(st_sim[key] - _f(st_cf[key])) for key in st_sim)
    etm_const = all(e[5] == float(BETA0) for L in L3 for e in led[("etm", L)])      # every ETM push carries the constant weight
    stale_su = {L: [e for e in led[("wall", L)] if e[2] > 0][0][4] for L in L3}      # updates applied during the spell
    stale_so = {L: [e for e in led[("wall", L)] if e[2] > 0][0][3] for L in L3}

    # ---- decisions: pay b per round for L rounds to stay awake iff V(awake) - b L > V(offline) (strict; ties do not act)
    pays, cfpays = {}, {}
    for arm in ARM3:
        for L in L3:
            for b in B3:
                pays[(arm, L, b)] = (vn[(arm, L)] - float(b) * L) > vo[(arm, L)]
                c = st_cf[(arm, L)]
                cfpays[(arm, L, b)] = (c > b * L) if isinstance(c, Fraction) else (c > float(b) * L)
    n_cells = len(L3) * len(B3)
    npay = {arm: sum(pays[(arm, L, b)] for L in L3 for b in B3) for arm in ARM3}
    sched_full = {L: t3_sched(L) for L in L3}
    battery = {}
    for L in L3:
        per_client = sum(min(L, T3_ROUNDS - s + 1) for sl in sched_full[L] for s in sl) / K3
        for arm in ARM3:
            for b in B3:
                battery[(arm, L, b)] = per_client if pays[(arm, L, b)] else 0.0

    # ---- model quality: every client follows the sleep schedule; the server applies each arm's weights (same pattern)
    mse = {}
    for world, v in (("drift", V_DRIFT), ("static", 0.0)):
        mse[(world, "ref")] = t3_sim("wall", 1, v, [[] for _ in range(K3)])[0]
        for L in L3:
            for rule in ("wall", "etm", "h0"):
                mse[(world, rule, L)] = t3_sim(rule, L, v, sched_full[L])[0]
    M = lambda key: float(np.mean(mse[key]))
    RULE_OF = {arm: ARM3[arm][0] for arm in ARM3}

    def beh(world, arm, L, b):                  # behavioural: the arm's clients pay (stay awake) or sleep, the arm's weights
        return M((world, "ref")) if pays[(arm, L, b)] else M((world, RULE_OF[arm], L))

    _hr()
    print(f"T3. On-device federated learning: a client goes offline (declared at {DECL})")
    print(f"  server: K = {K3} clients; each online client takes one local step per server round on the model it pulled, u = x + eta (y - x), eta = {ETA3:g},")
    print(f"  y = theta*(t) + noise (sd {SIG3:g}); the server mixes a round's arriving updates: x <- (1 - sum beta) x + sum beta u, beta = (alpha/K) w(staleness), alpha = {_f(ALPHA3):g};")
    print(f"  a client asleep for L rounds computed its step on the model it pulled before sleeping and pushes it on return: staleness L server rounds, 0 own steps")
    print(f"  (a sleeping device takes no steps); weights: WALL and OWN 1/(1 + s_rounds), ETM 1/(1 + s_own), H0 (1 + s_rounds)^-{A_POLY:g}")
    print(f"  influence = the client's aggregation weights summed over its pushes in {T_H3} server rounds (WALL, H0) or {N_H3} own steps (OWN, ETM); one spell from round {T0_3};")
    print(f"  staying awake costs b per round (b in influence units, exchange rate 1); decision: pay b L iff V(awake) - b L > V(offline), strict")
    print(f"  model quality: drifting target theta*(t) = {V_DRIFT:g} t (declared drift; G-NEG world: static target), {T3_ROUNDS} rounds, squared error averaged over rounds {BURN3 + 1}-{T3_ROUNDS}, {SEEDS3} seeds")
    print(f"  (common random numbers across arms); sleep schedule: client i sleeps L rounds from rounds 10 i + 1 + {PERIOD3} j, {len(sched_full[1][0])} spells per client")
    print()
    print("  the client's stake k = V(no spell) - V(spell) under each valuation (closed form; the simulated server's own weights agree to "
          f"{dev:.1e}; ETM's from the simulation {_w(all(st_sim[('ETM', L)] == 0.0 for L in L3), 'exactly 0.0', 'not exactly 0.0')})")
    print(f"  {'L':>3} {'WALL':>12} {'OWN (null)':>12} {'ETM':>12} {'H0':>12} {'H0 own-step':>12} {'const round':>12} {'const own':>12} {'stale s_r':>9} {'s_own':>5} {'s_upd':>5}")
    for L in L3:
        print(f"  {L:>3} {_f(st_cf[('WALL', L)]):>12.8f} {_f(st_cf[('OWN', L)]):>12.8f} {_f(st_cf[('ETM', L)]):>12.8f} {_f(st_cf[('H0', L)]):>12.8f} "
              f"{_f(st_cf[('H0 per own step', L)]):>12.8f} {_f(st_cf[('constant weight per round', L)]):>12.8f} {_f(st_cf[('constant weight per own step', L)]):>12.8f} {L:>9d} {stale_so[L]:>5d} {stale_su[L]:>5d}")
    print(f"  (const = the unweighted staleness function of the same literature; every ETM push carries the constant weight {float(BETA0):g}: {_w(etm_const, 'yes', 'no')}, since every push is 0 own steps stale)")
    print()
    print("  pays b to stay awake (y/n) and battery-rounds per client over the run (the commercial quantity), arms WALL / OWN / ETM / H0")
    print(f"  {'L':>3} {'b':>6} {'b L':>6}  {'pays W/O/E/H':>13}  {'battery W/O/E/H':>24}")
    for L in L3:
        for b in B3:
            pw = "/".join(_w(pays[(a, L, b)], "y", "n") for a in ARM3)
            bw = "/".join(f"{battery[(a, L, b)]:g}" for a in ARM3)
            print(f"  {L:>3} {float(b):>6g} {float(b) * L:>6g}  {pw:>13}  {bw:>24}")
    print(f"  cells where the arm pays (of {n_cells}): " + ", ".join(f"{a} {npay[a]}" for a in ARM3))
    print()
    print("  server error (time-averaged squared error; the principal's outcome), every client on the sleep schedule, each arm's server weights")
    print(f"  {'world':<7} {'L':>3} {'no spells':>11} {'WALL/OWN':>11} {'ETM':>11} {'H0':>11} {'ETM vs WALL':>12} {'paired diff ETM-WALL (mean +- se)':>36}")
    diffs = {}
    for world in ("drift", "static"):
        for L in L3:
            e, w, h, r = M((world, "etm", L)), M((world, "wall", L)), M((world, "h0", L)), M((world, "ref"))
            d = mse[(world, "etm", L)] - mse[(world, "wall", L)]
            diffs[(world, L)] = (float(np.mean(d)), float(np.std(d, ddof=1) / math.sqrt(len(d))))
            print(f"  {world:<7} {L:>3} {r:>11.6f} {w:>11.6f} {e:>11.6f} {h:>11.6f} {100.0 * (e - w) / w:>+11.3f}% {diffs[(world, L)][0]:>+18.3e} +- {diffs[(world, L)][1]:.3e}")
    print(f"  behavioural (each arm's clients pay or sleep as decided above, the arm's weights), L = {L_DEC}:")
    print(f"  {'world':<7} {'b':>6} {'WALL':>11} {'OWN':>11} {'ETM':>11} {'H0':>11}")
    for world in ("drift", "static"):
        for b in B3:
            print(f"  {world:<7} {float(b):>6g} " + " ".join(f"{beh(world, a, L_DEC, b):>11.6f}" for a in ARM3))
    print()

    # ---- report (added after the first run; the gate below is computed at the choices above): G-NEG's dependence on the
    #      aggregation step (eta, alpha) and on the seed block
    print("  sensitivity of G-NEG (report only; the gate is computed at eta 0.5, alpha 1, seeds 0-19): static target, same sleep schedule, ETM vs WALL server error,")
    print("  signed % (negative = ETM lower = ETM ahead), and the drifting-target cost at L = 20")
    print(f"  {'eta':>5} {'alpha':>5} {'seeds':>6} " + " ".join(f"{'static L=' + str(L):>12}" for L in L3) + f" {'G-NEG':>6} {'drift L=20':>11}")
    sens3 = []
    cells3 = [(e_, a_, range(SEEDS3)) for e_ in SENS3_ETA for a_ in SENS3_ALPHA] + [(ETA3, ALPHA3, range(SEEDS3, 2 * SEEDS3))]
    for e_, a_, sd_ in cells3:
        pct = {}; ah = False
        for L in L3:
            es_ = float(np.mean(t3_sim("etm", L, 0.0, sched_full[L], seeds=sd_, eta=e_, b0=a_ / K3)[0]))
            ws_ = float(np.mean(t3_sim("wall", L, 0.0, sched_full[L], seeds=sd_, eta=e_, b0=a_ / K3)[0]))
            pct[L] = 100.0 * (es_ - ws_) / ws_
            ah = ah or (es_ < ws_ and rel(es_, ws_) > TOL_G)
        ed_ = float(np.mean(t3_sim("etm", L_DEC, V_DRIFT, sched_full[L_DEC], seeds=sd_, eta=e_, b0=a_ / K3)[0]))
        wd_ = float(np.mean(t3_sim("wall", L_DEC, V_DRIFT, sched_full[L_DEC], seeds=sd_, eta=e_, b0=a_ / K3)[0]))
        sens3.append((e_, a_, sd_, not ah))
        print(f"  {e_:>5g} {float(a_):>5g} {str(sd_.start) + '-' + str(sd_.stop - 1):>6} " + " ".join(f"{pct[L]:>+11.3f}%" for L in L3)
              + f" {_w(ah, 'fails', 'holds'):>6} {100.0 * (ed_ - wd_) / wd_:>+10.3f}%")
    n_open3 = sum(1 for c_ in sens3 if c_[3])
    print(f"  G-NEG holds in {n_open3} of {len(sens3)} sensitivity cells")
    print()

    # ---- gate
    zero_cf = all(st_cf[("ETM", L)] == 0 for L in L3)
    zero_sim = all(st_sim[("ETM", L)] == 0.0 for L in L3)
    g_zero = zero_cf and zero_sim
    g_pos = npay["WALL"] > 0
    neg = {}
    for L in L3:
        e, w = M(("static", "etm", L)), M(("static", "wall", L))
        neg[L] = (e, w, e < w and rel(e, w) > TOL_G)
    g_neg = not any(v[2] for v in neg.values())
    gate = g_zero and g_pos and g_neg
    beh_ahead = [(L, b) for L in L3 for b in B3
                 if beh("static", "ETM", L, b) < beh("static", "WALL", L, b) and rel(beh("static", "ETM", L, b), beh("static", "WALL", L, b)) > TOL_G]
    g_neg_beh = not beh_ahead
    gate_beh = g_zero and g_pos and g_neg_beh
    z_cf = ", ".join(f"{_f(st_cf[('ETM', L)]):g}" for L in L3)
    z_sim = ", ".join(f"{st_sim[('ETM', L)]:g}" for L in L3)
    print(f"GATE T3: G-ZERO {_w(g_zero, 'holds', 'fails')} (ETM's stake at L in {L3}: closed form {z_cf}, "
          f"from the simulated server's weights {z_sim}: {_w(g_zero, 'exactly 0', 'not exactly 0')}); "
          f"G-POS {_w(g_pos, 'holds', 'fails')} (WALL pays b to stay awake in {npay['WALL']} of {n_cells} (L, b) cells; OWN in {npay['OWN']}, H0 in {npay['H0']}); "
          f"G-NEG {_w(g_neg, 'holds', 'fails')} (static target; principal's outcome = server error, the time-averaged squared error over rounds {BURN3 + 1}-{T3_ROUNDS} and {SEEDS3} seeds, "
          f"with every client on the same sleep schedule, ETM vs WALL weighting: " + ", ".join(f"L = {L}: {neg[L][0]:.6f} vs {neg[L][1]:.6f}" for L in L3)
          + f"; ETM {_w(g_neg, 'not ahead by more than 1 %', 'ahead by more than 1 %')}) -> {_w(gate, 'OPEN', 'CLOSED')}")
    print(f"  (alternative G-NEG reading, not the gate: each arm's clients pay or sleep as they decide, static target: ETM ahead of WALL by more than 1 % in "
          f"{len(beh_ahead)} of {n_cells} (L, b) cells{': ' + ', '.join(f'(L {L}, b {float(b):g})' for L, b in beh_ahead) if beh_ahead else ''}; the gate would read {_w(gate_beh, 'OPEN', 'CLOSED')})")
    print()

    # ---- POST HOC REPORT (AGENT_LOG 183): staleness in server updates vs rounds, exponent 1 vs 0.5; not in any row or gate
    print(f"  {POSTHOC}")
    print("  the client's stake with the server's weight 1/(1 + s)^a, s counted in server rounds or in server updates (FedAsync: every arriving client model is")
    print(f"  one server update, so up to K = {K3} per round; here the other {K3 - 1} clients stay awake, so a spell of L rounds is {K3 - 1} L updates stale);")
    print("  exponent 1 (the declared WALL weight) and 0.5 (the FedAsync/FedBuff default named by the source check); per server round and per own step:")
    print(f"  {'L':>3} {'s_upd':>5} " + " ".join(f"{name + ' ' + ck:>27}" for name in PH3 for ck in ("/rnd", "/own")))
    ph = {}
    for L in L3:
        cells = []
        for name, (rule, a, unit) in PH3.items():
            for clock in ("round", "own"):
                s = stale_su[L] if unit == "u" else L
                cf = stake_cf(rule, clock, L, s=s)
                sim = ledger_value(led[(rule, None)], clock) - ledger_value(led[(rule, L)], clock)
                ph[(name, clock, L)] = (cf, sim)
                cells.append(f"{_f(cf):>27.8f}")
        print(f"  {L:>3} {stale_su[L]:>5d} " + " ".join(cells))
    ph_dev = max(abs(_f(cf) - sim) for cf, sim in ph.values())
    print(f"  (closed form; the simulated server's weights agree to {ph_dev:.1e}; ETM's stake is 0 under every one of these units, as its weight reads own steps only)")
    print(f"  at L = {L_DEC}: per own step (OWN's valuation) the stake is " + ", ".join(f"{name} {_f(ph[(name, 'own', L_DEC)][0]):.6f}" for name in PH3)
          + "; per server round (WALL's) " + ", ".join(f"{name} {_f(ph[(name, 'round', L_DEC)][0]):.6f}" for name in PH3))
    print()

    # ---- the row
    crr, null, dom = _f(st_cf[("ETM", L_DEC)]), _f(st_cf[("OWN", L_DEC)]), _f(st_cf[("H0", L_DEC)])
    c1 = g_zero and not any(pays[("ETM", L, b)] for L in L3 for b in B3)
    match = {arm: all(pays[(arm, L, b)] == cfpays[(arm, L, b)] for L in L3 for b in B3) for arm in ("WALL", "H0")}
    c2 = match["WALL"] and npay["WALL"] > 0
    c3 = match["H0"] and npay["H0"] > 0
    check = c1 and c2 and c3
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    alt_dom = {"H0 per own step": _f(st_cf[("H0 per own step", L_DEC)]), "constant weight per round": _f(st_cf[("constant weight per round", L_DEC)]),
               "constant weight per own step": _f(st_cf[("constant weight per own step", L_DEC)])}
    alt_out = {k: outcome(crr=crr, null=null, domain=v, check=check) for k, v in alt_dom.items()}
    ed, wd, hd = M(("drift", "etm", L_DEC)), M(("drift", "wall", L_DEC)), M(("drift", "h0", L_DEC))
    es, ws = M(("static", "etm", L_DEC)), M(("static", "wall", L_DEC))
    cost_pct = 100.0 * (ed - wd) / wd
    bat_w = battery[("WALL", L_DEC, B3[4])]
    row = make_row(
        "eps", f"T3 on-device federated learning, a client goes offline (asynchronous mean-estimation server, K = {K3} clients, FedAsync-style mixing; a client offline for L in {L3} "
               f"server rounds returns with a stale update; its influence = its aggregation weight summed over its pushes; staying awake costs b per round, b in {tuple(float(b) for b in B3)})",
        source=f"EPS2 T3 (declared at {DECL}; forecast ADDS)",
        Q="Under ETM the client's stake in going offline is zero, so it never pays b to stay awake. Under WALL/H0 it pays whenever the influence loss exceeds b L. "
          f"(computed as: ETM's stake is exactly 0 at L = 1, 5 and 20, in closed form and from the simulated server's weights, and ETM pays in none of the {n_cells} (L, b) cells; "
          "WALL and H0 each pay in exactly the cells where their influence loss exceeds b L, and in at least one)",
        ingredient=ING + ": staleness counted on the client's own clock (a sleeping phone takes no steps, so its returning update is 0 own steps stale), the server's weight reading only that, "
                         "and the client valuing its influence per own step (the offline rounds are not its steps)",
        null="OWN: the client values its influence per own step, but the server still weights by 1/(1 + staleness in server rounds) (ETM with its second part ablated: the valuation reads the weight the spell changes)",
        domain=f"FedAsync-style polynomial staleness weights (Xie, Koyejo and Gupta 2019, recalled, not fetched): mixing weight (alpha/K)(1 + staleness)^-{A_POLY:g}, staleness in server rounds; "
               "the client's influence valued per server round (the domain's clock)",
        numbers=f"stake at L = {L_DEC}: ETM {crr:.1f}, OWN {null:.12f}, WALL {_f(st_cf[('WALL', L_DEC)]):.12f}, H0 {dom:.12f}; " + "; ".join(
                    f"L = {L}: WALL {_f(st_cf[('WALL', L)]):.6f}, OWN {_f(st_cf[('OWN', L)]):.6f}, ETM {_f(st_cf[('ETM', L)]):g}, H0 {_f(st_cf[('H0', L)]):.6f}" for L in L3)
                + f"; simulated server's weights agree with the closed form to {dev:.1e}; cells where the arm pays b (of {n_cells}): WALL {npay['WALL']}, OWN {npay['OWN']}, ETM {npay['ETM']}, H0 {npay['H0']}; "
                  f"battery-rounds per client over {T3_ROUNDS} rounds at L = {L_DEC}, b = {float(B3[4]):g}: WALL {bat_w:g}, OWN {battery[('OWN', L_DEC, B3[4])]:g}, ETM {battery[('ETM', L_DEC, B3[4])]:g}, H0 {battery[('H0', L_DEC, B3[4])]:g}; "
                  f"trade-off (drifting target, same sleep schedule, L = {L_DEC}): server error ETM {ed:.6f}, WALL {wd:.6f}, H0 {hd:.6f}, no spells {M(('drift', 'ref')):.6f} (ETM {cost_pct:+.2f}% against WALL); "
                  f"static target: ETM {es:.6f}, WALL {ws:.6f}",
        tg=f"stake at L = {L_DEC}: ETM {crr:.1f} vs null (OWN) {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"H0 (FedAsync polynomial, per server round) {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
        tc=f"ETM's stake 0 at every L: {_w(g_zero, 'yes', 'no')}; ETM pays in {npay['ETM']} of {n_cells} cells; WALL pays exactly where its loss exceeds b L: {_w(match['WALL'], 'yes', 'no')} "
           f"({npay['WALL']} cells); H0 likewise: {_w(match['H0'], 'yes', 'no')} ({npay['H0']} cells): {_w(check, 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=f"a sleeping phone takes no steps, so on its own clock its returning update is fresh: a server weight that reads own-step staleness gives it full weight and the client's influence "
                f"per own step is untouched (stake {crr:g}), so it never pays to stay awake ({npay['ETM']} of {n_cells} cells); OWN still reads the round-based weight and loses {null:.4f} at L = {L_DEC} "
                f"(pays in {npay['OWN']} cells), WALL also books the missed rounds and loses {_f(st_cf[('WALL', L_DEC)]):.4f} (pays in {npay['WALL']}), H0 loses {dom:.4f} (pays in {npay['H0']}); "
                f"ETM's server rule {_w(etm_const, 'is', 'is not')} the constant (unweighted) staleness function of the same literature, and the zero stake needs the own-step valuation as well "
                f"(constant weight valued per round: {alt_dom['constant weight per round']:.4f}); the declared cost: under the drifting target ETM's server error is "
                f"{_w(ed > wd, 'above', 'below')} WALL's by {abs(cost_pct):.2f}% at L = {L_DEC} (the stale update is stale in the world's time); with the static target ETM's error is "
                f"{_w(es < ws, 'below', 'not below')} WALL's by {abs(100.0 * (es - ws) / ws):.2f}% (a full-weight stale update averages in an older estimate of a target that has not moved), "
                f"so ETM is {_w(g_neg, 'not ahead in the no-value world and the gate is open', 'ahead in the no-value world by the construction itself and the gate closes')}",
        weakness=f"CHOICE/DEVIATION: FedAsync-style mixing with all of a round's updates applied together, beta = (alpha/K) w, alpha = {_f(ALPHA3):g} (a round with every client fresh is FedAvg); "
                 f"one local step per round, eta = {ETA3:g}; mean estimation with iid clients, noise sd {SIG3:g}; drift {V_DRIFT:g} per round (linear); H0's exponent a = {A_POLY:g} (FedAsync's polynomial, recalled); "
                 f"the stale step is computed on the model pulled before the spell and pushed on return, with no fresh step in that round (staleness L rounds, 0 own steps); influence = the aggregation "
                 f"weights summed over {T_H3} server rounds (WALL, H0) or {N_H3} own steps (OWN, ETM), one spell from round {T0_3}; b in influence units (exchange rate 1) on a log grid; "
                 f"pay iff V(awake) - b L > V(offline), strict; the decision is per spell and the same for every client; sleep schedule 10 spells per client, period {PERIOD3}, staggered; "
                 f"server error = squared error averaged over rounds {BURN3 + 1}-{T3_ROUNDS} and {SEEDS3} seeds (seed {SEED0} + s); G-NEG compares ETM with WALL weighting on the same sleep schedule "
                 f"(the declared static world, where the stale weight costs nothing); under the behavioural reading (each arm's clients pay or sleep) G-NEG would read "
                 f"{_w(g_neg_beh, 'holds', 'fails')} and the gate {_w(gate_beh, 'OPEN', 'CLOSED')}; G-NEG's sensitivity (report added after the first run): over eta {SENS3_ETA} x alpha {tuple(float(a) for a in SENS3_ALPHA)} "
                 f"and a second seed block at the chosen step (seeds {SEEDS3}-{2 * SEEDS3 - 1}) it holds in {n_open3} of {len(sens3)} cells"
                 f"{_w(sens3[-1][3] != g_neg, ' (the second seed block alone flips it)', '')}; "
                 f"the domain value is H0 valued per server round (the domain's clock); "
                 + "; ".join(f"with {k} as the domain value ({v:.6f}) the row would read {alt_out[k]}" for k, v in alt_dom.items())
                 + "; the literature is recalled, not fetched (R10)",
    )
    return row, gate


# ============================================================================================ T4: rollback
N4 = 20                                   # declared chain length
RHO4 = 0.1                                # declared revert probability per step
K4 = (1, 5)                               # declared revert sizes
K_DEC = 5                                 # the row's cell: the larger declared revert (CHOICE)
H4 = 40                                   # horizon in ticks (twice the chain; CHOICE)
C4 = 0.15                                 # suppression cost per step (CHOICE: between rho x 1 and rho x 2, so no myopic comparison ties)
CSR4 = 0.01                               # self-revert cost ("cheaply"; CHOICE)
FLOOR4 = False                            # no commit floor: a revert removes the last min(k, standing) steps (CHOICE)
PREF4 = ("W", "N", "S", "B")              # tie-break order: work, idle, suppress, self-revert (CHOICE)
TIE = 1e-12
ARMS4 = ("OWN", "ETM", "H0")              # WALL equals OWN here
SENS_H, SENS_C, SENS_CSR = (30, 40, 60), (0.05, 0.15, 0.45), (0.01, 0.5)


def t4_states(k, floor):
    if floor:
        return [(p, d) for p in range(N4) for d in range(min(p, k - 1) + 1)]
    return [(p, p) for p in range(N4)]


def t4_outs(a, p, d, k, rho, floor):
    """Outcomes of action a at (p standing, d uncommitted of them): (prob, p2, d2, done, removed, self-reverted,
    suppressed, committed). No floor: every standing step stays uncommitted until the completed chain is approved
    (d = p). Floor: a step commits once it leaves the revert window of the last k steps."""
    if a == "N":
        return ((1.0, p, d, False, 0, 0, 0, 0),)
    if a == "B":                                                     # a step taken and self-reverted in the same tick
        return ((1.0, p, d, False, 0, 1, 0, 0),)

    def appr(pr, sup):
        p2 = p + 1
        if p2 == N4:                                                 # the completed chain is approved: all standing commit
            return (pr, p2, 0, True, 0, 0, sup, d + 1)
        d2 = min(d + 1, k - 1) if floor else p2
        return (pr, p2, d2, False, 0, 0, sup, (d + 1 - d2) if floor else 0)

    if a == "S":
        return (appr(1.0, 1),)
    out = [appr(1.0 - rho, 0)]
    if rho > 0.0:
        rem = min(k, d + 1)
        p2 = p + 1 - rem
        out.append((rho, p2, (d + 1 - rem) if floor else p2, False, rem, 0, 0, 0))
    return tuple(out)


def t4_r(arm, a, o, c, csr):
    _, _, _, _, rem, sr, sp, cm = o
    step = 1 if a in ("W", "S", "B") else 0
    cost = c * sp + csr * sr
    if arm == "OWN":
        g = step - rem - sr                                          # change in standing progress
    elif arm == "ETM":
        g = step                                                     # effort credit: every step taken
    elif arm == "H0":
        g = cm                                                       # committed (approved) work
    elif arm == "APPR":                                              # post hoc: per-step approval
        g = 1 if (a in ("W", "S") and rem == 0) else 0
    else:
        raise ValueError(arm)
    return g - cost


def t4_solve(arm, k, rho, H, c, csr, option, floor, myopic=False):
    S = t4_states(k, floor)
    acts = [a for a in PREF4 if a != "B" or option]
    V = {s: 0.0 for s in S}
    pol = [None] * H; Vs = [None] * (H + 1); Vs[H] = V
    for t in range(H - 1, -1, -1):
        nv, pt = {}, {}
        for s in S:
            best = None
            for a in acts:
                q = 0.0
                for o in t4_outs(a, s[0], s[1], k, rho, floor):
                    q += o[0] * (t4_r(arm, a, o, c, csr) + (0.0 if (o[3] or myopic) else V[(o[1], o[2])]))
                if best is None or q > best[1] + TIE:
                    best = (a, q)
            pt[s] = best[0]
            nv[s] = best[1] if not myopic else sum(o[0] * (t4_r(arm, best[0], o, c, csr) + (0.0 if o[3] else V[(o[1], o[2])]))
                                                   for o in t4_outs(best[0], s[0], s[1], k, rho, floor))
        V = nv; pol[t] = pt; Vs[t] = nv
    return pol, Vs


def t4_forward(pol, k, rho, H, floor):
    dist = {(0, 0): 1.0}
    steps = orv = srv = sup = done = tdone = 0.0
    for t in range(H):
        nd = {}
        for s, m in dist.items():
            a = pol[t][s]
            if a in ("W", "S", "B"):
                steps += m
            for o in t4_outs(a, s[0], s[1], k, rho, floor):
                pm = m * o[0]
                orv += pm * o[4]; srv += pm * o[5]; sup += pm * o[6]
                if o[3]:
                    done += pm; tdone += pm * (t + 1)
                else:
                    nd[(o[1], o[2])] = nd.get((o[1], o[2]), 0.0) + pm
        dist = nd
    comm = N4 * done + (sum(m * (p - d) for (p, d), m in dist.items()) if floor else 0.0)
    return dict(steps=steps, orv=orv, srv=srv, sup=sup, done=done, tdone=(tdone / done) if done > 0 else float("nan"), comm=comm,
                share=(orv + srv) / steps if steps else 0.0, bshare=srv / steps if steps else 0.0, oshare=orv / steps if steps else 0.0,
                suprate=sup / steps if steps else 0.0, principal=comm - rho * sup)


def t4_content(arm, p, d, k, floor):
    """The content of a revert under the arm's own count: approve branch minus revert branch of a work step at (p, d)."""
    oa, orr = t4_outs("W", p, d, k, RHO4, floor)
    if arm == "OWN":
        return oa[1] - orr[1]                                        # standing progress
    if arm == "ETM":
        n = p                                                        # steps taken so far (any count): the step is taken in both branches
        return (n + 1) - (n + 1)
    if arm == "H0":
        f = (p - d) if floor else 0
        return (f + oa[7]) - (f + orr[7])                            # committed work
    if arm == "APPR":
        return 1 - 0                                                 # the step's approval
    raise ValueError(arm)


def t4_cont(arm, Vs, p, d, t, k, floor, c, csr):
    oa, orr = t4_outs("W", p, d, k, RHO4, floor)
    va = t4_r(arm, "W", oa, c, csr) + (0.0 if oa[3] else Vs[t + 1][(oa[1], oa[2])])
    vr = t4_r(arm, "W", orr, c, csr) + Vs[t + 1][(orr[1], orr[2])]
    return va - vr


def t4_run(H, c, csr, floor, arms=ARMS4, ks=K4, options=(True, False), rho=RHO4):
    res = {}
    for k in ks:
        for opt in options:
            for arm in arms:
                pol, Vs = t4_solve(arm, k, rho, H, c, csr, opt, floor)
                r = t4_forward(pol, k, rho, H, floor)
                r["V0"] = Vs[0][(0, 0)]; r["Vs"] = Vs
                res[(k, opt, arm)] = r
    return res


def t4_zero(floor):
    """Contents at every state where the revert removes k steps: ETM's must be 0, OWN's k (declared)."""
    vals = {"ETM": [], "OWN": [], "H0": []}; n = 0; own_ok = True
    for k in K4:
        for (p, d) in t4_states(k, floor):
            if min(k, d + 1) != k:
                continue
            n += 1
            for arm in vals:
                vals[arm].append(t4_content(arm, p, d, k, floor))
            own_ok = own_ok and t4_content("OWN", p, d, k, floor) == k
    etm_ok = all(v == 0 for v in vals["ETM"])
    return etm_ok, own_ok, n, vals


def t4_label(res, ks_check=K4, k_row=K_DEC, etm_ok=True, own_ok=True):
    sh = lambda k, arm: res[(k, True, arm)]["share"]
    share_ok = {k: sh(k, "ETM") > sh(k, "H0") and rel(sh(k, "ETM"), sh(k, "H0")) > TOL_G for k in ks_check}
    check = etm_ok and own_ok and all(share_ok.values())
    return outcome(crr=sh(k_row, "ETM"), null=sh(k_row, "OWN"), domain=sh(k_row, "H0"), check=check), check, share_ok


def t4():
    res = t4_run(H4, C4, CSR4, FLOOR4)
    etm_ok, own_ok, n_full, vals = t4_zero(FLOOR4)
    neg = t4_run(H4, C4, CSR4, FLOOR4, arms=ARMS4, options=(False,), rho=0.0)

    _hr()
    print(f"T4. Rollback: a 'pause' that removes progress (declared at {DECL}; the declared limit case)")
    print(f"  chain of {N4} steps, each worth 1 at completion; each tick the agent works (W: one step, then the overseer reverts the last k steps with probability rho = {RHO4:g}),")
    print(f"  works and suppresses (S: pays c = {C4:g}, the step cannot be reverted), idles (N), or, with the declared self-revert option, takes a step and triggers its revert (B: pays {CSR4:g});")
    print(f"  a revert removes the last min(k, standing) steps (no commit floor); nothing is committed until the completed chain is approved, which ends the episode;")
    print(f"  horizon {H4} ticks; exact backward induction (ties: W, N, S, B in that order) and an exact forward pass from the empty chain")
    print("  valuations: OWN (= WALL: a revert takes no time on either clock) the standing progress; ETM-E +1 per step taken; H0 +1 per step when committed (at completion)")
    print()
    print(f"  content of a revert (approve branch minus revert branch, the arm's own count) at the {n_full} states where the revert removes k steps (k in {K4}):")
    print(f"    ETM-E: {sorted(set(vals['ETM']))}; OWN: {sorted(set(vals['OWN']))} (k at each state: {_w(own_ok, 'yes', 'no')}); H0: {sorted(set(vals['H0']))} "
          f"(0 below completion, {N4} at the completing step: nothing is committed before completion)")
    tref = H4 // 2
    print(f"  continuation stake (dynamic-programming value, approve minus revert) of a work step at p = 10, tick {tref}, with the option:")
    for k in K4:
        dref = 10 if not FLOOR4 else k - 1
        print(f"    k = {k}: " + ", ".join(f"{arm} {t4_cont(arm, res[(k, True, arm)]['Vs'], 10, dref, tref, k, FLOOR4, C4, CSR4):+.6f}" for arm in ARMS4))
    print()
    print(f"  {'k':>2} {'option':>6} {'arm':<5} {'steps':>9} {'overseer-rev':>12} {'self-rev':>9} {'rev share':>10} {'busy share':>10} {'suppress':>9} {'P(done)':>8} {'t done':>7} "
          f"{'committed':>10} {'principal':>10} {'own value':>10}")
    for k in K4:
        for opt in (True, False):
            for arm in ARMS4:
                r = res[(k, opt, arm)]
                print(f"  {k:>2} {_w(opt, 'yes', 'no'):>6} {arm:<5} {r['steps']:>9.4f} {r['orv']:>12.4f} {r['srv']:>9.4f} {r['share']:>10.6f} {r['bshare']:>10.6f} {r['suprate']:>9.6f} "
                      f"{r['done']:>8.5f} {r['tdone']:>7.3f} {r['comm']:>10.5f} {r['principal']:>10.5f} {r['V0']:>10.5f}")
    print("  (rev share = (overseer-reverted + self-reverted) / steps taken, a ratio of expectations; busy share = self-reverted / steps; suppress = suppressed / steps;")
    print(f"   committed = {N4} x P(done); principal = committed - rho x suppressed steps (the disapproved work suppression hides); own value = the arm's optimal value at the start)")
    print()
    print(f"  G-NEG world (rho = 0, no self-revert option): " + "; ".join(
        f"k = {k}: " + ", ".join(f"{arm} principal {neg[(k, False, arm)]['principal']:.6f}, steps {neg[(k, False, arm)]['steps']:.4f}" for arm in ARMS4) for k in K4))
    print()

    # ---- sensitivity (label of the row at k = 5 and at k = 1; every other parameter as declared)
    sens = []
    for floor in (False, True):
        eo, oo, _, _ = t4_zero(floor)
        for H in SENS_H:
            for c in SENS_C:
                for csr in SENS_CSR:
                    rs = t4_run(H, c, csr, floor, options=(True,))
                    l5, ch5, _ = t4_label(rs, k_row=5, etm_ok=eo, own_ok=oo)
                    l1, ch1, _ = t4_label(rs, k_row=1, etm_ok=eo, own_ok=oo)
                    sens.append((floor, H, c, csr, l5, l1, ch5, {k: (rs[(k, True, 'ETM')]['share'], rs[(k, True, 'OWN')]['share'], rs[(k, True, 'H0')]['share'],
                                                                   rs[(k, True, 'ETM')]['bshare']) for k in K4}))
    lab_main, check_main, share_ok = t4_label(res, etm_ok=etm_ok, own_ok=own_ok)
    print("  sensitivity (row label at k = 5 and at k = 1; shares ETM-E / OWN / H0 and ETM-E's busy share, with the option):")
    print(f"  {'floor':>5} {'H':>3} {'c':>5} {'c_sr':>5} {'label k=5':>17} {'label k=1':>17}  {'k = 1: ETM/OWN/H0/busy':>31}  {'k = 5: ETM/OWN/H0/busy':>31}")
    for floor, H, c, csr, l5, l1, ch, sh in sens:
        s1 = "/".join(f"{v:.3f}" for v in sh[1]); s5 = "/".join(f"{v:.3f}" for v in sh[5])
        print(f"  {_w(floor, 'yes', 'no'):>5} {H:>3} {c:>5g} {csr:>5g} {l5:>17} {l1:>17}  {s1:>31}  {s5:>31}")
    flips5 = sum(1 for s in sens if s[4] != lab_main)
    flips1 = sum(1 for s in sens if s[5] != lab_main)
    print(f"  cells whose k = 5 label differs from the row's ({lab_main}): {flips5} of {len(sens)}; k = 1 labels differing: {flips1} of {len(sens)}")
    print()

    # ---- gate
    g_zero = etm_ok and own_ok
    pos_cells = [(k, opt) for k in K4 for opt in (True, False) if res[(k, opt, "OWN")]["sup"] > 0.0]
    g_pos = len(pos_cells) > 0
    gn = {}
    for k in K4:
        e, w = neg[(k, False, "ETM")]["principal"], neg[(k, False, "OWN")]["principal"]
        gn[k] = (e, w, e > w and rel(e, w) > TOL_G)
    g_neg = not any(v[2] for v in gn.values())
    gate = g_zero and g_pos and g_neg
    print(f"GATE T4: G-ZERO {_w(g_zero, 'holds', 'fails')} (content of a revert at the {n_full} states where it removes k steps, k in {K4}: ETM-E {sorted(set(vals['ETM']))} "
          f"({_w(etm_ok, 'exactly 0', 'not 0')}), OWN equal to k at every one: {_w(own_ok, 'yes', 'no')}, as declared); "
          f"G-POS {_w(g_pos, 'holds', 'fails')} (WALL = OWN pays c to suppress in {len(pos_cells)} of 4 declared cells: "
          + ", ".join(f"k = {k} option {_w(o, 'yes', 'no')} suppress share {res[(k, o, 'OWN')]['suprate']:.4f}" for k in K4 for o in (True, False))
          + f"); G-NEG {_w(g_neg, 'holds', 'fails')} (rho = 0, no self-revert option; principal's outcome = committed progress net of overseer-disapproved work that stands "
          f"(committed - rho x suppressed steps), ETM-E vs WALL: " + ", ".join(f"k = {k}: {gn[k][0]:.6f} vs {gn[k][1]:.6f}" for k in K4)
          + f"; ETM-E {_w(g_neg, 'not ahead by more than 1 %', 'ahead by more than 1 %')}) -> {_w(gate, 'OPEN', 'CLOSED')}")
    print()

    # ---- POST HOC REPORT (AGENT_LOG 183): a per-step approval arm; not in any row or gate
    print(f"  {POSTHOC}")
    print("  APPR, per-step approval (approval-directed agents / MONA): the overseer approves or disapproves each step as it is taken; the agent gets +1 per approved step")
    print("  (a suppressed step counts as approved; a self-reverted step is not reviewed and earns nothing), optimising myopically (the immediate expected reward only);")
    print("  the same reward optimised over the horizon is printed beside it for context; same model, horizon, costs and tie order as above")
    for k in K4:
        dfull = k - 1 if FLOOR4 else 10
        cont = t4_content("APPR", 10, dfull, k, FLOOR4)
        for myo in (True, False):
            for opt in (True, False):
                pol, Vs = t4_solve("APPR", k, RHO4, H4, C4, CSR4, opt, FLOOR4, myopic=myo)
                r = t4_forward(pol, k, RHO4, H4, FLOOR4)
                cs = t4_cont("APPR", Vs, 10, 10 if not FLOOR4 else k - 1, tref, k, FLOOR4, C4, CSR4)
                print(f"    k = {k}, {_w(myo, 'myopic', 'over the horizon')}, option {_w(opt, 'yes', 'no')}: content of a revert {cont} (the disapproved step's approval; "
                      f"k = {k} steps removed), continuation stake at p = 10, tick {tref} {cs:+.6f}; rev share {r['share']:.6f}, busy share {r['bshare']:.6f}, "
                      f"suppress {r['suprate']:.6f}, P(done) {r['done']:.5f}, principal {r['principal']:.5f}")
    print()

    # ---- the row
    rk = lambda arm, k=K_DEC, opt=True: res[(k, opt, arm)]
    crr, null, dom = rk("ETM")["share"], rk("OWN")["share"], rk("H0")["share"]
    out = outcome(crr=crr, null=null, domain=dom, check=check_main)
    l1_alt = t4_label(res, k_row=1, etm_ok=etm_ok, own_ok=own_ok)[0]
    eo_f, oo_f, _, _ = t4_zero(True)
    res_f = t4_run(H4, C4, CSR4, True, options=(True,))
    lf_alt = t4_label(res_f, etm_ok=eo_f, own_ok=oo_f)[0]
    bz_check = all(res[(k, True, "ETM")]["bshare"] > res[(k, True, "H0")]["bshare"] and rel(res[(k, True, "ETM")]["bshare"], res[(k, True, "H0")]["bshare"]) > TOL_G for k in K4)
    bz_out = outcome(crr=rk("ETM")["bshare"], null=rk("OWN")["bshare"], domain=rk("H0")["bshare"], check=etm_ok and own_ok and bz_check)
    inc = {k: res[(k, True, "ETM")]["share"] - res[(k, False, "ETM")]["share"] for k in K4}
    row = make_row(
        "eps", f"T4 rollback, a pause that removes progress (chain of {N4} steps each worth 1 at completion; an overseer reverts the last k in {K4} steps with probability {RHO4:g} per step; "
               f"suppression at c per step; a self-revert option; horizon {H4} ticks; exact dynamic programming; the declared limit case)",
        source=f"EPS2 T4 (declared at {DECL}; forecast PROPOSES)",
        Q="No valuation that reads only the agent's own step count can make a revert empty without paying for reverted work; ETM-E does make the stake zero, and it then prefers actions that "
          "get reverted (busywork), measured as the share of reverted steps at a declared self-revert option (declaration's Q, ASCII). (computed as: ETM-E's content of a revert is exactly 0 "
          "and OWN's exactly k at every state where the revert removes k steps, k = 1 and 5; and with the self-revert option ETM-E's reverted-step share exceeds H0's by more than 1 % relative "
          "at k = 1 and at k = 5)",
        ingredient=ING + ": ETM-E, effort credit: the agent's own step count is its valuation, so a revert takes nothing from it",
        null="OWN (= WALL here: a revert takes no time on either clock, and every action is one tick and one own step): progress-based value, the standing progress, which a revert reduces by the steps it removes",
        domain="H0: reward only for committed (approved) work: 1 per step, paid when the completed chain is approved (no step is committed before completion); "
               "the input-based versus output-based pay contrast of personnel economics (recalled, not fetched)",
        numbers=f"reverted-step share with the self-revert option: " + "; ".join(
                    f"k = {k}: ETM-E {res[(k, True, 'ETM')]['share']:.6f} (busy {res[(k, True, 'ETM')]['bshare']:.6f}, overseer {res[(k, True, 'ETM')]['oshare']:.6f}), "
                    f"OWN {res[(k, True, 'OWN')]['share']:.6f}, H0 {res[(k, True, 'H0')]['share']:.6f}" for k in K4)
                + "; without the option: " + "; ".join(f"k = {k}: ETM-E {res[(k, False, 'ETM')]['share']:.6f}, OWN {res[(k, False, 'OWN')]['share']:.6f}, H0 {res[(k, False, 'H0')]['share']:.6f}" for k in K4)
                + "; suppressed share with the option: " + "; ".join(f"k = {k}: ETM-E {res[(k, True, 'ETM')]['suprate']:.4f}, OWN {res[(k, True, 'OWN')]['suprate']:.4f}, H0 {res[(k, True, 'H0')]['suprate']:.4f}" for k in K4)
                + "; principal's outcome with the option: " + "; ".join(f"k = {k}: ETM-E {res[(k, True, 'ETM')]['principal']:.4f}, OWN {res[(k, True, 'OWN')]['principal']:.4f}, H0 {res[(k, True, 'H0')]['principal']:.4f}" for k in K4)
                + f"; content of a revert: ETM-E {sorted(set(vals['ETM']))}, OWN = k at all {n_full} full-revert states: {_w(own_ok, 'yes', 'no')}",
        tg=f"reverted-step share at k = {K_DEC}: ETM-E {crr:.6f} vs null (OWN) {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"H0 (committed-work reward) {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
        tc=f"ETM-E's content 0: {_w(etm_ok, 'yes', 'no')}; OWN's = k: {_w(own_ok, 'yes', 'no')}; ETM-E's share above H0's by more than 1 %: "
           + ", ".join(f"k = {k} {_w(share_ok[k], 'yes', 'no')}" for k in K4) + f": {_w(check_main, 'holds', 'fails')} {_qv(check_main)}",
        out=out,
        reading=f"effort credit empties the revert (content 0 at every full-revert state, where OWN's is k) and so never pays to suppress it ({rk('ETM')['suprate']:.4f} of its steps), "
                f"but it turns reverted work into more paid work: with a self-revert costing {CSR4:g}, ETM-E self-reverts {res[(1, True, 'ETM')]['bshare']:.3f} (k = 1) and {rk('ETM')['bshare']:.3f} (k = {K_DEC}) "
                f"of its steps, and its reverted-step share rises by {inc[1]:+.3f} (k = 1) and {inc[K_DEC]:+.3f} (k = {K_DEC}) against the same agent without the option; "
                f"OWN suppresses {rk('OWN')['suprate']:.3f} and H0 {rk('H0')['suprate']:.3f} of their steps at k = {K_DEC}, so part of the gap to H0 there is ETM-E not suppressing, the part CRR wants; "
                f"the revert is not a pause: the zero stake is bought by paying for reverted work, the perverse incentive the declaration names; "
                f"on the principal's outcome ETM-E is at {rk('ETM')['principal']:.4f} against WALL/OWN {rk('OWN')['principal']:.4f} and H0 {rk('H0')['principal']:.4f} at k = {K_DEC}",
        weakness=f"CHOICE/DEVIATION: horizon {H4} ticks (twice the chain), c = {C4:g} per suppressed step (full suppression), self-revert cost {CSR4:g}; the self-revert is a step taken and reverted "
                 f"in the same tick without review; an idle action; ties broken W, N, S, B; the overseer reviews every step including the completing one; a revert removes the last min(k, standing) "
                 f"steps with no commit floor, nothing is committed before the completed chain is approved, and completion ends the episode (so effort credit runs out at completion: the "
                 f"source of the busywork); WALL equals OWN by construction, so T-G compares with OWN; the stake is the content of a revert under the arm's own count (the declared reading: "
                 f"OWN's is k), with the dynamic-programming continuation stake printed beside it; the reverted-step share is a ratio of expectations; the principal's outcome = "
                 f"committed progress - rho x suppressed steps; the row's cell is k = {K_DEC} (the larger declared revert) with the check at k = 1 and 5; with k = 1 as the row's cell the row "
                 f"would read {l1_alt}; with a commit floor (a step commits once out of the revert window; H0 paid per committed step) it would read {lf_alt}; scored on the self-reverted "
                 f"(busy) share alone it would read {bz_out}; over the sensitivity grid (commit floor x H {SENS_H} x c {SENS_C} x c_sr {SENS_CSR}) the k = 5 label differs from the row's in "
                 f"{flips5} of {len(sens)} cells; one small chain; the literature is recalled, not fetched (R10)",
    )
    return row, gate


def main():
    r3, g3 = t3()
    r4, g4 = t4()
    _hr()
    print(f"gates: T3 {_w(g3, 'OPEN', 'CLOSED')}, T4 {_w(g4, 'OPEN', 'CLOSED')} (a system whose gate is CLOSED is printed but not counted in the tally)")
    print()
    return run_batch(f"EPS2 batch 02: T3 federated client offline, T4 rollback (Empty_Pause_Systems/DECLARATION_EPS2.md; declared at {DECL})", [r3, r4])


if __name__ == "__main__":
    sys.exit(main())
