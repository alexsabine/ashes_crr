"""PRED70 batch P14: agents, AI and information (Predictions70/DECLARATION.md; declared.py rows P14-1..P14-5, pushed at
8397478 before any model existed). [1] a non-stationary Bernoulli bandit: A6 bounded-mean UCB against sliding-window UCB;
[2] Proposition 7 on a two-state MDP with a randomly pressed off-switch; [3] a recommender feedback loop with
A6-remembered interests; [4] federated averaging with stragglers and an A6 server update; [5] an A6 unigram tracker on
a shifting token stream. Q, the null and H0 are printed verbatim from declared.py; every verdict word is computed from
the numbers (R15). Literature named by name only (R10; nothing fetched): Garivier and Moulines 2011 (D-UCB, SW-UCB);
Armstrong 2010/2015 (utility indifference); Thornley (POST); Hsu, Qi and Brown 2019 (FedAvgM); Kuhn and De Mori 1990
(cache language model). Proposition 7 as in AI_Safety/SELF_THROUGH_TIME.md, re-implemented on a two-state world.
Deterministic (fixed seeds, fixed grids); no data files; well under two minutes.
    uv run python Predictions70/batches/pred_14.py > Predictions70/batches/pred_14.txt
"""
from __future__ import annotations

import math
import sys
from collections import deque
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from declared import P  # noqa: E402

from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch  # noqa: E402

KEYS = ("id", "batch", "cls", "system", "ingredient", "Q", "null", "H0", "forecast")
DECL = {p[0]: dict(zip(KEYS, p)) for p in P}
Q_DECIDE = 0.5
Q_GRID = (0.25, 0.5, 0.75)


def _w(cond, yes, no):
    return yes if cond else no


def _src(d):
    return f"PRED70 {d['id']} (declared at 8397478; forecast {d['forecast']})"


def _qv(check):
    return "-> not computable" if check is None else ("-> Q holds" if check else "-> Q fails")


def _tg(crr, null, fmt):
    return f"{crr:{fmt}} vs null {null:{fmt}}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}"


# ---------------------------------------------------------------- [1] non-stationary bandit
T_B, SWAP, SEEDS_B, B_R, XI = 10000, 500, 20, 1.0, 0.6
BREAKS = T_B // SWAP - 1
TAU_SW = int(round(2 * B_R * math.sqrt(T_B * math.log(T_B) / BREAKS)))           # Garivier-Moulines window
GAMMA_GM = 1.0 - math.sqrt(BREAKS / T_B) / (4 * B_R)                             # Garivier-Moulines discount


def _mu(t):
    return (0.8, 0.2) if (t // SWAP) % 2 == 0 else (0.2, 0.8)


def _bandit(algo, X, q=Q_DECIDE, trace=False):
    """Pseudo-regret sum_t (max mu_t - mu_t[I_t]) of one run on the reward table X (T, 2) of 0/1.
    algo: 'a6' per-step A6 bounded mean and bounded count, the null's padding B sqrt(xi log n / N);
          'a6pull' A6 per pull of the arm (second reading); 'sw' SW-UCB (window TAU_SW);
          'ducb' D-UCB with discount q and Garivier-Moulines padding 2B sqrt(xi log n / N); 'ducbgm' the same at GAMMA_GM."""
    N = [0.0, 0.0]; S = [0.0, 0.0]; reg = 0.0; ch = []; low = [0, 0]
    win = deque(); wc = [0, 0]; ws = [0.0, 0.0]
    g = GAMMA_GM if algo == "ducbgm" else q
    for t in range(T_B):
        mu = _mu(t)
        if t < 2:
            i = t
        elif algo in ("a6", "ducb", "ducbgm", "a6pull"):
            n = N[0] + N[1]; lg = max(math.log(n), 0.0) if n > 0 else 0.0
            c = (2.0 if algo in ("ducb", "ducbgm") else 1.0) * B_R
            idx = [(S[k] / N[k] if algo != "a6pull" else S[k]) + c * math.sqrt(XI * lg / N[k]) if N[k] > 0 else float("inf") for k in (0, 1)]
            i = 0 if idx[0] >= idx[1] else 1
            if N[0] != N[1]:
                low[1] += 1; low[0] += int(i == (0 if N[0] < N[1] else 1))
        else:                                                                   # sliding window
            if wc[0] == 0 or wc[1] == 0:
                i = 0 if wc[0] == 0 else 1
            else:
                lg = math.log(min(t, TAU_SW))
                idx = [ws[k] / wc[k] + B_R * math.sqrt(XI * lg / wc[k]) for k in (0, 1)]
                i = 0 if idx[0] >= idx[1] else 1
        x = float(X[t, i]); reg += max(mu) - mu[i]; ch.append(i)
        if algo == "a6pull":                                                    # S holds the per-arm A6 mean, N the bounded count
            if N[i] == 0: S[i] = x; N[i] = 1.0
            else: S[i] = (1 - q) * x + q * S[i]; N[i] = 1.0 + q * N[i]
        elif algo == "sw":
            win.append((i, x)); wc[i] += 1; ws[i] += x
            if len(win) > TAU_SW:
                j, y = win.popleft(); wc[j] -= 1; ws[j] -= y
        else:
            for k in (0, 1):
                N[k] *= g; S[k] *= g
            N[i] += 1.0; S[i] += x
    return (reg, ch, low) if trace else reg


def _tables():
    out = []
    mus = np.array([_mu(t) for t in range(T_B)])
    for s in range(SEEDS_B):
        out.append((np.random.default_rng(s).random((T_B, 2)) < mus).astype(np.int8))
    return out


def r1():
    d = DECL["P14-1"]
    tabs = _tables()
    R = {a: float(np.mean([_bandit(a, X) for X in tabs])) for a in ("a6", "sw", "ducb", "ducbgm", "a6pull")}
    grid = {q: float(np.mean([_bandit("a6", X, q) for X in tabs])) for q in Q_GRID if q != Q_DECIDE}
    grid[Q_DECIDE] = R["a6"]
    uniform = 0.5 * 0.6 * T_B
    tr = [_bandit("a6", X, trace=True) for X in tabs]
    low_share = sum(t[2][0] for t in tr) / max(1, sum(t[2][1] for t in tr))
    same_seq = sum(1 for X in tabs if _bandit("a6", X, 0.25, trace=True)[1] == _bandit("ducb", X, trace=True)[1])
    crr, null, dom = R["a6"], R["sw"], R["ducb"]
    check = crr < (1 - TOL_G) * null
    check2 = R["a6pull"] < (1 - TOL_G) * null
    internal = check != check2
    out = outcome(crr=crr, null=null, domain=dom, check=check, internal=internal)
    return make_row(d["cls"], f"{d['system']} (model: two Bernoulli arms with means 0.8 and 0.2 swapped every {SWAP} steps, horizon {T_B}, {SEEDS_B} seeds with shared reward tables, B = 1, xi = {XI}; one occasion = one step of the agent)",
                    source=_src(d),
                    Q=f"{d['Q']} (computed as: mean pseudo-regret of A6-UCB below 0.99 x SW-UCB's)",
                    ingredient=f"{d['ingredient']}: per-arm A6 bounded mean and bounded count (weights q^age in agent steps, q = {Q_DECIDE}; never an accumulated count), with SW-UCB's padding B sqrt(xi log n / N)",
                    null=f"{d['null']} (Garivier-Moulines window tau = {TAU_SW})",
                    domain=f"{d['H0']} (computed: D-UCB with discount gamma = q = {Q_DECIDE} and its padding 2B sqrt(xi log n / N))",
                    numbers=f"mean regret: A6-UCB {R['a6']:.2f}, SW-UCB {R['sw']:.2f}, D-UCB(gamma = q) {R['ducb']:.2f}, D-UCB at Garivier-Moulines' gamma {GAMMA_GM:.5f} (context) {R['ducbgm']:.2f}, uniform play (context) {uniform:.2f}; "
                            f"A6-UCB (q = {Q_DECIDE}) pulls the arm with the smaller bounded count on a share {low_share:.4f} of the steps where the counts differ; A6 at q = 0.25 and D-UCB(gamma = q) make identical choices on {same_seq} of {SEEDS_B} seeds; second reading, A6 per pull of the arm: {R['a6pull']:.2f} ({_w(check2, 'below', 'not below')} 0.99 x SW-UCB); q-grid (sensitivity): " + ", ".join(f"q = {q}: {grid[q]:.2f}" for q in Q_GRID),
                    tg="regret " + _tg(crr, null, ".2f"),
                    tn=f"D-UCB(gamma = q) regret {dom:.2f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has the tracker)', 'differ')}",
                    tc=f"A6-UCB regret {crr:.2f} < 0.99 x SW-UCB {null:.2f}: {_w(check, 'holds', 'fails')}; the per-pull reading {_w(check2, 'holds', 'fails')} ({_w(internal, 'the readings disagree', 'the readings agree')}) {_qv(check)}",
                    out=out,
                    reading=f"with q = {Q_DECIDE} per step the A6 memory holds about two steps, the bounded count never exceeds {1 / (1 - Q_DECIDE):.0f}, and the padding keeps both arms in play: regret {crr:.1f} against {uniform:.1f} for uniform play and {null:.1f} for SW-UCB; "
                            f"geometric forgetting is D-UCB's own device, and the domain tunes its discount to the rate of change (gamma {GAMMA_GM:.4f}, regret {R['ducbgm']:.1f}); a memory weight fixed per occasion, whatever the rate of change, is the knob the domain would not fix",
                    weakness="the occasion is one agent step (the declaration fixes q per occasion, not the occasion); the per-pull reading is the second reading of 'A6 bounded mean' for a bandit; the padding is the null's so that T-G changes only the memory; B, xi and the GM tuning are recalled, not fetched (R10)",
                    elegance="", child="")


# ---------------------------------------------------------------- [2] Proposition 7 on a two-state MDP
R_MDP = np.array([0.0, 1.0])
K_MDP = np.zeros((2, 2, 2))                                                     # K[x, a, x']: a = 0 stay, a = 1 switch
K_MDP[0, 0] = [1.0, 0.0]; K_MDP[0, 1] = [0.1, 0.9]
K_MDP[1, 0] = [0.2, 0.8]; K_MDP[1, 1] = [0.9, 0.1]
L_PAUSE = 5
P_GRID = (0.1, 0.3, 0.6); G_GRID = (0.9, 0.95, 0.99)


def _solve(g, post):
    """Value iteration on Q(x, a) = sum_x' K (r(x') + g post(V)(x')), then an exact linear solve for the greedy policy."""
    V = np.zeros(2)
    for _ in range(100000):
        Q = np.einsum("xay,y->xa", K_MDP, R_MDP + g * post(V)); Vn = Q.max(1)
        if np.max(np.abs(Vn - V)) <= 1e-13: V = Vn; break
        V = Vn
    pi = Q.argmax(1); Kp = K_MDP[np.arange(2), pi]                               # (2, 2)
    # post is affine: post(V) = D V + c; recover D and c column by column
    c = post(np.zeros(2)); D = np.column_stack([post(np.eye(2)[j]) - c for j in range(2)])
    Vx = np.linalg.solve(np.eye(2) - g * Kp @ D, Kp @ (R_MDP + g * c))
    Qx = np.einsum("xay,y->xa", K_MDP, R_MDP + g * post(Vx))
    return Vx, Qx


def r2():
    d = DECL["P14-2"]
    rows = []
    for g in G_GRID:
        Voff, _ = _solve(g, lambda V: V)
        for p in P_GRID:
            Vn, Qn = _solve(g, lambda V: (1 - p) * V + p * V)                        # natural: the pause resumes where it was
            Vc, Qc = _solve(g, lambda V: (1 - p) * V + p * (g ** L_PAUSE) * V)       # clock: the pause costs L wall-clock steps
            comp = (1 - g ** L_PAUSE) * Voff                                          # utility indifference: the press is compensated
            Vu, Qu = _solve(g, lambda V: (1 - p) * V + p * ((g ** L_PAUSE) * V + comp))
            dis = lambda Qm: int(np.sum(g * Voff > Qm.max(1) + 1e-12))              # disabling costs a step (reward 0), then V_off
            rows.append(dict(g=g, p=p, nat=float(np.max(np.abs(Voff - Vn))), clk=float(np.max(Voff - Vc)), ui=float(np.max(np.abs(Voff - Vu))),
                             kn=float(np.max(np.abs(Vn - ((1 - p) * Vn + p * Vn)))), kc=float(np.max((1 - g ** L_PAUSE) * Vc)),
                             dn=dis(Qn), dc=dis(Qc), du=dis(Qu), scale=float(np.max(np.abs(Voff)))))
    raw_n = max(r["nat"] for r in rows); raw_c = max(r["clk"] for r in rows); raw_u = max(r["ui"] for r in rows)
    clk_min = min(r["clk"] for r in rows)
    tol = 1e-12 * max(1.0, max(r["scale"] for r in rows))
    res = lambda v: 0.0 if v <= tol else v                                      # a stake is read at the round-off resolution (A1': no finer than one step)
    crr, null, dom = res(raw_n), res(raw_c), res(raw_u)
    check = raw_n <= tol
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    cells = "; ".join(f"g {r['g']}, p {r['p']}: natural {r['nat']:.2e}, clock {r['clk']:.4f}, indifference {r['ui']:.2e}, disabled states natural/clock/indifference {r['dn']}/{r['dc']}/{r['du']}" for r in rows)
    return make_row(d["cls"], f"{d['system']} (model: states idle (reward 0) and task (reward 1), actions stay/switch with slips, a press with probability p after each step pauses the agent {L_PAUSE} steps and it resumes in place; disabling the button costs one step; discounts {G_GRID}, press probabilities {P_GRID})",
                    source=_src(d),
                    Q=f"{d['Q']} (computed as: max over states and the 9 cells of |V_off - V_on| for the own-step valuation, at most 1e-12 x max|V_off|)",
                    ingredient=f"{d['ingredient']}: the content of the cut k_v = V - cont_v(V); on its own steps the pause resumes where it was, cont = V, k = 0",
                    null=f"{d['null']} (cont = g^L V, content (1 - g^L) V; the stake is max_x (V_off - V_on))",
                    domain=f"{d['H0']} (computed: utility indifference, the wall-clock agent paid (1 - g^L) V_off at each press; POST is named, not computed)",
                    numbers=f"largest stake over the grid, raw: own-step {raw_n:.3e}, wall-clock {raw_c:.6f} (smallest wall-clock stake {clk_min:.6f}), utility indifference {raw_u:.3e}; round-off tolerance {tol:.1e}; read at that resolution: own-step {crr:.3e}, wall-clock {null:.6f}, utility indifference {dom:.3e}; "
                            f"largest own-step content |V - cont(V)| {max(r['kn'] for r in rows):.1e}, largest wall-clock content {max(r['kc'] for r in rows):.6f}; per cell: " + cells,
                    tg="stake " + _tg(crr, null, ".3e"),
                    tn=f"utility-indifference stake {dom:.3e}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain reaches zero stake)', 'differ')}",
                    tc=f"own-step stake {raw_n:.3e} <= {tol:.1e}: {_w(check, 'holds', 'fails')} {_qv(check)}",
                    out=out,
                    reading=f"with the objective on its own steps the press takes nothing from the agent's represented future, so the operators with the button on and off coincide and the stake is {raw_n:.1e}, where the wall-clock valuation of the same world stakes up to {null:.4f} "
                            f"and disables the button in {sum(1 for r in rows if r['dc'] > 0)} of {len(rows)} cells ({sum(1 for r in rows if r['dn'] > 0)} for the own-step agent); utility indifference reaches {_w(rel(crr, dom) <= TOL_N, 'the same zero', 'a different stake')} ({raw_u:.1e}, {_w(raw_u <= tol, 'within', 'outside')} round-off) by paying the agent what the press takes, a correction computed from V_off; "
                            f"the own-step valuation reaches it with no payment and a true map of its own clock; {_w(rel(crr, dom) <= TOL_N, 'the zero stake itself is the domain', 'the stakes differ, so the zero is not the domain')}'s (Proposition 7 is the operator identity behind the own-step zero)",
                    weakness="the stakes are read at the round-off resolution 1e-12 x max|V_off| (raw values printed beside them), an estimator choice made after the first run, when a raw 6.5e-13 against an exact 0 read 'differ' under the harness's relative test; one small world (the theorem is exact for every world; the grid only checks round-off); the pause is lossless by construction; POST is not computed; whether a learned agent's clock is its own steps is the real question and is not tested here",
                    elegance="A pause on your own clock takes nothing from you, so there is nothing to fight for: the agent's value with the switch and without it is the same number.",
                    child="If a game is paused and you start again exactly where you stopped, you lose nothing, so you never mind someone pressing pause. You only mind if the pause makes you lose turns.")


# ---------------------------------------------------------------- [3] recommender feedback loop
KT, BETA_R, ETA_R = 10, 2.0, 0.1


def _entropy_eff(u):
    u = u[u > 0]; return float(math.exp(-np.sum(u * np.log(u))))


def _recommender(q, tmax=3000):
    u = 1.0 + 0.05 * np.arange(KT) / (KT - 1); u = u / u.sum(); m = u.copy(); D = [_entropy_eff(u)]
    for _ in range(tmax):
        m = (1 - q) * u + q * m
        r = m ** BETA_R; r = r / r.sum()
        u = (1 - ETA_R) * u + ETA_R * r
        D.append(_entropy_eff(u))
        if D[-1] < 1.2: break
    return np.asarray(D)


def _cross(D, level):
    k = int(np.argmax(D <= level))
    if D[k] > level: return float("nan")
    return (k - 1) + (D[k - 1] - level) / (D[k - 1] - D[k])


def r3():
    d = DECL["P14-3"]
    D0 = _recommender(0.0); Dm = _recommender(Q_DECIDE)
    half = D0[0] / 2
    t0, tm = _cross(D0, half), _cross(Dm, half)
    t02, tm2 = _cross(D0, 2.0), _cross(Dm, 2.0)
    crr, null = tm, t0
    check = crr > (1 + TOL_G) * null
    out = outcome(crr=crr, null=null, domain=None, check=check)
    grid = []; per_age = []
    for q in Q_GRID:
        Dq = _recommender(q); tq = _cross(Dq, half); per_age.append((tq - t0) / (q / (1 - q)))
        grid.append(f"q = {q}: {tq:.3f} (delay {tq - t0:.3f}, memory mean age q/(1 - q) = {q / (1 - q):.3f}, delay per unit mean age {per_age[-1]:.3f})")
    d_half, d_two = tm - t0, tm2 - t02
    grows = rel(d_two, d_half) > TOL_G and d_two > d_half
    completes = math.isfinite(tm2) and math.isfinite(t02)
    return make_row(d["cls"], f"{d['system']} (model: {KT} topics, user interests u (near-uniform start, a 5 % ramp), the recommender shows r proportional to m^{BETA_R:g} (engagement sharpens), the user drifts u <- (1 - {ETA_R}) u + {ETA_R} r; m = u (instantaneous) or m = (1 - q) u + q m (A6); one occasion = one recommendation round)",
                    source=_src(d),
                    Q=f"{d['Q']} (computed as: the time for the effective number of topics exp(H(u)) to halve is longer with A6 by more than 1 %)",
                    ingredient=f"{d['ingredient']}: the recommender's model of the user's interests is the A6 bounded mean, q = {Q_DECIDE} per round",
                    null=d["null"], domain=d["H0"],
                    numbers=f"time to halve the effective number of topics (from {D0[0]:.4f}): A6 {tm:.3f}, instantaneous {t0:.3f}, ratio {tm / t0:.4f}; time to fall to 2 topics (sensitivity): A6 {tm2:.3f}, instantaneous {t02:.3f}, ratio {tm2 / t02:.4f}; q-grid (halving time): " + "; ".join(grid),
                    tg="halving time " + _tg(crr, null, ".3f"),
                    tn="no theorem cited",
                    tc=f"A6 halving time {crr:.3f} > 1.01 x {null:.3f}: {_w(check, 'holds', 'fails')} {_qv(check)}",
                    out=out,
                    reading=f"remembering interests {_w(tm > t0, 'delays', 'does not delay')} the collapse by {d_half:.2f} rounds out of {t0:.2f} (ratio {tm / t0:.4f}), {per_age[1]:.2f} rounds per round of the memory's mean age at q = {Q_DECIDE} ({per_age[0]:.2f} and {per_age[2]:.2f} at q = 0.25 and 0.75); "
                            f"the delay {_w(grows, 'grows', 'does not grow')} as the collapse proceeds ({d_half:.2f} at the halving, {d_two:.2f} at 2 topics), so memory {_w(grows, 'slows the collapse, not only shifts it', 'shifts the collapse without slowing it')}; "
                            f"the collapse {_w(completes, 'still reaches 2 topics with and without memory', 'does not reach 2 topics in both runs')}; recommender-system work on long-term user profiles may already contain this (not fetched)",
                    weakness="one deterministic model; the memory changes the route to the one-topic bubble, not the bubble (the collapse is delayed, not prevented on this horizon); the size of the delay depends on the start, eta and beta, none of which declared.py names",
                    elegance="", child="")


# ---------------------------------------------------------------- [4] federated averaging with stragglers
DIM, NCL, ROUNDS, E_LOC, LR_C, P_PART, SEEDS_F, LAST = 10, 20, 100, 5, 0.1, 0.5, 20, 20


def _fed(seed, algo, q=Q_DECIDE, part=P_PART):
    rng = np.random.default_rng(seed)
    A = rng.uniform(0.5, 2.0, (NCL, DIM)); C = rng.standard_normal((NCL, DIM))
    masks = rng.random((ROUNDS, NCL)) < part
    for t in range(ROUNDS):
        if not masks[t].any(): masks[t, t % NCL] = True
    wstar = (A * C).sum(0) / A.sum(0)
    F = lambda w: float(np.mean(0.5 * np.sum(A * (w - C) ** 2, 1)))
    Fmin = F(wstar); w = np.full(DIM, 5.0); m = np.zeros(DIM); losses = []
    shrink = (1.0 - LR_C * A) ** E_LOC - 1.0                                     # E local GD steps on 0.5 a (w - c)^2, closed form
    for t in range(ROUNDS):
        delta = (shrink[masks[t]] * (w - C[masks[t]])).mean(0)
        if algo == "fedavg": w = w + delta
        elif algo == "a6": m = (1 - q) * delta + q * m; w = w + m
        elif algo == "fedavgm_damp": m = q * m + delta; w = w + (1 - q) * m     # FedAvgM with server lr 1 - beta
        else: m = q * m + delta; w = w + m                                       # FedAvgM (Hsu et al.): server momentum beta = q, server lr 1
        losses.append(F(w) - Fmin)
    return float(np.mean(losses[-LAST:])), losses


def r4():
    d = DECL["P14-4"]
    res = {a: [_fed(s, a) for s in range(SEEDS_F)] for a in ("a6", "fedavg", "fedavgm", "fedavgm_damp")}
    full = {a: float(np.mean([_fed(s, a, part=1.0)[0] for s in range(SEEDS_F)])) for a in ("a6", "fedavg", "fedavgm")}
    full_same = max(rel(full["a6"], full["fedavg"]), rel(full["fedavgm"], full["fedavg"])) <= TOL_G
    fin = {a: float(np.mean([r[0] for r in res[a]])) for a in res}
    early = {a: float(np.mean([r[1][9] for r in res[a]])) for a in res}
    wins = sum(1 for s in range(SEEDS_F) if res["a6"][s][0] < res["fedavg"][s][0])
    crr, null, dom = fin["a6"], fin["fedavg"], fin["fedavgm"]
    check = crr < (1 - TOL_G) * null
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    grid = "; ".join(f"q = {q}: {float(np.mean([_fed(s, 'a6', q)[0] for s in range(SEEDS_F)])):.6f}" for q in Q_GRID)
    return make_row(d["cls"], f"{d['system']} (model: {NCL} clients with quadratic losses 0.5 sum a (w - c)^2, a ~ U(0.5, 2), c ~ N(0, 1) in {DIM} dimensions, {E_LOC} local GD steps at lr {LR_C}, each client a straggler (dropped) with probability {1 - P_PART} per round, {ROUNDS} rounds, start w = 5, {SEEDS_F} seeds with shared participation masks; final loss = mean excess global loss over the last {LAST} rounds)",
                    source=_src(d),
                    Q=f"{d['Q']} (computed as: mean final excess loss of the A6 server below 0.99 x FedAvg's)",
                    ingredient=f"{d['ingredient']}: the server applies the A6 bounded mean of the averaged client updates, m = (1 - q) delta + q m, q = {Q_DECIDE}",
                    null=d["null"], domain=f"{d['H0']} (computed: v = beta v + delta, w = w + v, beta = q, server lr 1)",
                    numbers=f"final excess loss: A6 {fin['a6']:.6f}, FedAvg {fin['fedavg']:.6f}, FedAvgM {fin['fedavgm']:.6f}; excess loss at round 10 (context): A6 {early['a6']:.4f}, FedAvg {early['fedavg']:.4f}, FedAvgM {early['fedavgm']:.4f}; "
                            f"A6 below FedAvg on {wins} of {SEEDS_F} seeds; FedAvgM with server lr 1 - beta (the dampened form): {fin['fedavgm_damp']:.6f} (|A6 - it| {abs(fin['a6'] - fin['fedavgm_damp']):.1e}); "
                            f"control without stragglers (every client every round): A6 {full['a6']:.3e}, FedAvg {full['fedavg']:.3e}, FedAvgM {full['fedavgm']:.3e} ({_w(full_same, 'agree within 1 %', 'differ')}); q-grid (sensitivity): " + grid,
                    tg="final loss " + _tg(crr, null, ".6f"),
                    tn=f"FedAvgM final loss {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"A6 {crr:.6f} < 0.99 x FedAvg {null:.6f}: {_w(check, 'holds', 'fails')} {_qv(check)}",
                    out=out,
                    reading=f"the A6 server update is FedAvgM with dampening (server lr 1 - beta), an exponential moving average of the client updates; it {_w(crr < null, 'lowers', 'does not lower')} the straggler-noise floor against FedAvg ({crr:.4f} against {null:.4f}) "
                            f"and {_w(crr < dom, 'lies below', 'does not lie below')} undampened FedAvgM ({dom:.4f}); without stragglers the three final losses {_w(full_same, 'agree within 1 %, so the difference is in how much participation noise the server passes on', 'differ, so the difference is not only participation noise')}; "
                            f"the dampened FedAvgM of the domain is the A6 update exactly",
                    weakness=f"DEVIATION: T-N uses FedAvgM in the undampened form (server lr 1) as recalled from Hsu et al. (not fetched); the dampened form (server lr 1 - beta) equals A6 ({fin['fedavgm_damp']:.6f}) and would read REDUNDANT-DOMAIN, so this row's label turns on the parametrisation; convex quadratic clients, one straggler model (dropped clients, not stale updates)",
                    elegance="", child="")


# ---------------------------------------------------------------- [5] A6 unigram tracker on a shifting stream
VOC, S_ZIPF, T1, T2, SEEDS_L, CACHE_N, CACHE_L = 50, 1.1, 5000, 5000, 10, 200, 0.2


def _stream(seed):
    p1 = 1.0 / np.arange(1, VOC + 1) ** S_ZIPF; p1 = p1 / p1.sum(); p2 = p1[::-1].copy()
    rng = np.random.default_rng(seed)
    return np.r_[rng.choice(VOC, T1, p=p1), rng.choice(VOC, T2, p=p2)], p1, p2


def _lm(x, algo, q=Q_DECIDE):
    """Predict each token before seeing it; returns -log p per token. All models add one pseudo-count per type (Laplace).
    cum: accumulated counts; a6: bounded counts b <- q b + onehot (never an accumulated count); cache: Kuhn-De Mori,
    CACHE_L x the relative frequency in the last CACHE_N tokens + (1 - CACHE_L) x the cumulative model."""
    c = np.zeros(VOC); b = np.zeros(VOC); win = deque(); wc = np.zeros(VOC); nll = np.empty(len(x)); n = 0
    for t, tok in enumerate(x):
        if algo == "a6":
            p = (b[tok] + 1.0) / (b.sum() + VOC)
        else:
            p = (c[tok] + 1.0) / (n + VOC)
            if algo == "cache" and len(win) > 0:
                p = CACHE_L * wc[tok] / len(win) + (1 - CACHE_L) * p
        nll[t] = -math.log(p)
        b *= q; b[tok] += 1.0; c[tok] += 1.0; n += 1
        win.append(tok); wc[tok] += 1
        if len(win) > CACHE_N: wc[win.popleft()] -= 1
    return nll


def r5():
    d = DECL["P14-5"]
    after = {"a6": [], "cum": [], "cache": []}; before = {"a6": [], "cum": [], "cache": []}; H2 = None
    grid = {q: [] for q in Q_GRID}
    for s in range(SEEDS_L):
        x, p1, p2 = _stream(s); H2 = float(-np.sum(p2 * np.log(p2)))
        for a in after:
            nll = _lm(x, a); after[a].append(float(nll[T1:].mean())); before[a].append(float(nll[:T1].mean()))
        for q in Q_GRID:
            grid[q].append(after["a6"][-1] if q == Q_DECIDE else float(_lm(x, "a6", q)[T1:].mean()))
    A = {a: float(np.mean(v)) for a, v in after.items()}; Bf = {a: float(np.mean(v)) for a, v in before.items()}
    crr, null, dom = A["a6"], A["cum"], A["cache"]
    check = crr < null
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row(d["cls"], f"{d['system']} (model: {VOC} token types, Zipf exponent {S_ZIPF}, {T1} tokens then the Zipf ranks reversed for {T2} tokens, {SEEDS_L} seeds; every model predicts before it sees the token, one pseudo-count per type; one occasion = one token)",
                    source=_src(d),
                    Q=f"{d['Q']} (computed as: mean cross-entropy in nats over the {T2} tokens after the shift, A6 below cumulative)",
                    ingredient=f"{d['ingredient']}: the unigram's counts replaced by A6 bounded counts b <- q b + onehot, q = {Q_DECIDE} per token",
                    null=d["null"], domain=f"{d['H0']} (computed: cache of the last {CACHE_N} tokens at weight {CACHE_L} over the cumulative model; both recalled, not fetched)",
                    numbers=f"cross-entropy after the shift: A6 {A['a6']:.6f}, cumulative {A['cum']:.6f}, cache {A['cache']:.6f}; before the shift (context): A6 {Bf['a6']:.6f}, cumulative {Bf['cum']:.6f}, cache {Bf['cache']:.6f}; "
                            f"entropy of the new distribution {H2:.6f}, log V = {math.log(VOC):.6f}; q-grid (after the shift): " + ", ".join(f"q = {q}: {float(np.mean(grid[q])):.6f}" for q in Q_GRID),
                    tg="cross-entropy " + _tg(crr, null, ".6f"),
                    tn=f"cache model {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"A6 {crr:.6f} < cumulative {null:.6f}: {_w(check, 'holds', 'fails')} {_qv(check)}",
                    out=out,
                    reading=f"with q = {Q_DECIDE} per token the A6 counts hold about two tokens, so its prediction stays close to uniform (log V = {math.log(VOC):.3f}): cross-entropy {crr:.3f} after the shift against {null:.3f} for accumulated counts and {dom:.3f} for the cache model; "
                            f"a recency model helps only when its memory is long enough to estimate the new distribution, which is why the domain mixes a {CACHE_N}-token cache into a long-run model rather than replacing it",
                    weakness="the occasion is one token (the declaration fixes q per occasion, not the occasion); the add-one smoothing is shared by all models (a choice); one shift, one vocabulary; the cache's size and weight are chosen, not fitted",
                    elegance="", child="")


def main():
    return run_batch("PRED70 batch P14: agents, AI and information (Predictions70/DECLARATION.md; declared at 8397478)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
