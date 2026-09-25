"""CRR's commitments run through FOREVER's mathematics (Continuous_Learning/FOREVER/DECLARATION.md, pushed before this
script existed; prompt-log entry 180). Synthetic, deterministic, rung R4; every label is computed here (R15).

FOREVER (arXiv 2601.03938 v2): Delta_t = ||Theta_t - Theta_{t-1}||_2 over the trainable (LoRA) weights; tau_t = sum Delta,
reset per task; tau_day = sum of the first S = 24 Deltas; replay when tau_t >= d * tau_day, d in {1, 2, 4, 7, 15, 30};
mu_0 = warm-up mean of Delta, mu_t = EMA(lambda = 0.05) of Delta, r_t = mu_t / mu_0,
beta_t = beta_base * clip(1 + gamma (r_t - 1), 0.5, 3.0).
CRR's counterparts: D2 coherence C (the arc since the last cut, Fisher-Rao, sum sqrt(2 KL_step) on a probe, D6), A1' the
own unit, A3 (the cut resets C), D3/D4 chord and surplus, H-EQ (w = Omega |g_p| / |g_q|), E2 (own-clock keying).
"""
import sys
import pathlib

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "src"))
from crr.instrument.core import kl_step  # noqa: E402

S_WARM = 24; D_HUMAN = (1, 2, 4, 7, 15, 30); LAM_EMA = 0.05; G_MIN, G_MAX = 0.5, 3.0
D_IN, K, RANK, N_TASK, LR, BS = 20, 4, 4, 400, 0.05, 10
DEAD, NOISE_SD = 8, 0.01


# ---------------------------------------------------------------- a LoRA-factored softmax classifier
def softmax(z):
    z = z - z.max(axis=1, keepdims=True); e = np.exp(z); return e / e.sum(axis=1, keepdims=True)


def make_task(rng, means, n=N_TASK, dead=0):
    y = np.arange(n) % K; X = means[y] + rng.normal(size=(n, D_IN))
    if dead: X = np.concatenate([X, np.zeros((n, dead))], axis=1)
    return X, np.eye(K)[y]


def probs(X, W0, P, Q):
    return softmax(X @ (W0 + P @ Q))


def train(X, Y, W0, P, Q, steps, rng, noise_rng=None, dead=0, snaps=None):
    for _ in range(steps):
        i = rng.integers(0, len(X), BS); x, y = X[i], Y[i]
        G = x.T @ (probs(x, W0, P, Q) - y) / BS                     # dL/dW
        gP, gQ = G @ Q.T, P.T @ G
        P = P - LR * gP; Q = Q - LR * gQ
        if noise_rng is not None and dead:                           # movement that changes no prediction
            P = P.copy(); P[-dead:] += noise_rng.normal(0, NOISE_SD, size=(dead, RANK))
        if snaps is not None: snaps.append((P.copy(), Q.copy()))
    return P, Q


def setup(dead=0):
    rng = np.random.default_rng(0)
    mA = rng.normal(0, 1.5, size=(K, D_IN)); mB = rng.normal(0, 1.5, size=(K, D_IN))
    XA, YA = make_task(rng, mA, dead=dead); XB, YB = make_task(rng, mB, dead=dead)
    probe = np.concatenate([make_task(rng, mA, 100, dead)[0], make_task(rng, mB, 100, dead)[0]])
    d = D_IN + dead
    W0 = rng.normal(0, 0.05, size=(d, K)); P = rng.normal(0, 0.1, size=(d, RANK)); Q = rng.normal(0, 0.1, size=(RANK, K))
    return rng, (XA, YA), (XB, YB), probe, W0, P, Q


# ---------------------------------------------------------------- clocks
def euclid_deltas(snaps):
    return np.array([np.sqrt(np.sum((a[0] - b[0]) ** 2) + np.sum((a[1] - b[1]) ** 2)) for a, b in zip(snaps[:-1], snaps[1:])])


def fisher_deltas(snaps, X, W0):
    ps = [probs(X, W0, P, Q) for P, Q in snaps]
    return np.array([np.sqrt(max(2 * kl_step(a, b), 0.0)) for a, b in zip(ps[:-1], ps[1:])]), ps


def triggers(deltas, S=S_WARM, days=D_HUMAN):
    """FOREVER eqs. (3)-(6): the step (1-based update count) at which tau first reaches each d * tau_day (None if not)."""
    tau = np.cumsum(deltas); day = tau[S - 1]; out = []
    for d in days:
        idx = np.nonzero(tau >= d * day)[0]; out.append(int(idx[0]) + 1 if idx.size else None)
    return out


def chord_triggers(chord, S=S_WARM, days=D_HUMAN):
    day = chord[S - 1]; out = []
    for d in days:
        idx = np.nonzero(chord >= d * day)[0]; out.append(int(idx[0]) + 1 if idx.size else None)
    return out


def lab(ok):
    return "HOLDS" if ok else "FAILS"


def main():
    print("CRR's commitments run through FOREVER's mathematics (arXiv 2601.03938 v2); declared in Continuous_Learning/FOREVER/DECLARATION.md")
    print(f"FOREVER constants: S {S_WARM}, days {D_HUMAN}, EMA lambda {LAM_EMA}, clip [{G_MIN}, {G_MAX}]; classifier W = W0 + P Q, d {D_IN}, K {K}, "
          f"rank {RANK}, lr {LR}, batch {BS}")
    labels = {}

    # ---- the base trajectory: task A (300 steps), then task B (600 steps, recorded; FOREVER resets tau at the task start)
    rng, (XA, YA), (XB, YB), probe, W0, P, Q = setup()
    P, Q = train(XA, YA, W0, P, Q, 300, rng)
    snaps = [(P.copy(), Q.copy())]; P, Q = train(XB, YB, W0, P, Q, 600, rng, snaps=snaps)
    dE = euclid_deltas(snaps); dF, ps = fisher_deltas(snaps, probe, W0)
    tE, tF = triggers(dE), triggers(dF)
    print(f"\nbase run (task B, 600 updates): Euclidean triggers {tE}; Fisher triggers {tF}")

    # ---- F1: reparametrisation P -> P D, Q -> D^-1 Q (P Q unchanged)
    print("\n== F1  A1' + D2 against a change of parametrisation (LoRA-style P -> P D, Q -> D^-1 Q)")
    Dg = np.exp(np.random.default_rng(1).uniform(np.log(0.25), np.log(4.0), size=RANK))
    snaps_r = [(Pp * Dg, (Qq.T / Dg).T) for Pp, Qq in snaps]
    dE_r = euclid_deltas(snaps_r); dF_r, ps_r = fisher_deltas(snaps_r, probe, W0)
    maxdp = max(float(np.max(np.abs(a - b))) for a, b in zip(ps, ps_r))
    relF = float(np.max(np.abs(np.cumsum(dF_r) - np.cumsum(dF)) / np.maximum(np.cumsum(dF), 1e-300)))
    tE_r, tF_r = triggers(dE_r), triggers(dF_r)
    print(f"   D = {np.round(Dg, 4).tolist()}")
    print(f"   F1a predictions identical: max |dp| {maxdp:.3e} (<= 1e-12) -> {lab(maxdp <= 1e-12)}"); labels["F1a"] = maxdp <= 1e-12
    print(f"   F1b Fisher arc identical: max relative difference {relF:.3e} (<= 1e-9) -> {lab(relF <= 1e-9)}; Fisher triggers {tF_r}"); labels["F1b"] = relF <= 1e-9
    moved = [i for i in range(len(D_HUMAN)) if tE[i] != tE_r[i]]
    print(f"   F1c FOREVER's Euclidean triggers after reparametrisation {tE_r} (before {tE}); triggers that moved: {len(moved)} -> {lab(len(moved) >= 1)}"); labels["F1c"] = len(moved) >= 1
    print(f"       Euclidean arc over the run: {np.sum(dE):.6f} before, {np.sum(dE_r):.6f} after; tau_day {np.cumsum(dE)[S_WARM-1]:.6f} before, {np.cumsum(dE_r)[S_WARM-1]:.6f} after")
    tE_u = triggers(7.0 * dE)
    print(f"   F1d every Delta x 7 (a change of units): triggers {tE_u}, identical -> {lab(tE_u == tE)}"); labels["F1d"] = tE_u == tE

    # ---- F2: movement that changes no prediction (noise on the weights of always-zero features)
    print(f"\n== F2  D2's change against movement that changes nothing ({DEAD} dead features, noise sd {NOISE_SD} per step)")
    out = {}
    for noisy in (False, True):
        rng2, (XA2, YA2), (XB2, YB2), probe2, W02, P2, Q2 = setup(dead=DEAD)
        nr = np.random.default_rng(1) if noisy else None
        if nr is not None: nr.uniform(size=RANK)                    # the seed-1 stream continues after D's draws
        P2, Q2 = train(XA2, YA2, W02, P2, Q2, 300, rng2, nr, DEAD)
        sn = [(P2.copy(), Q2.copy())]; P2, Q2 = train(XB2, YB2, W02, P2, Q2, 600, rng2, nr, DEAD, snaps=sn)
        out[noisy] = (triggers(euclid_deltas(sn)), triggers(fisher_deltas(sn, probe2, W02)[0]))
    print(f"   without noise: Euclidean {out[False][0]}, Fisher {out[False][1]}")
    print(f"   with noise:    Euclidean {out[True][0]}, Fisher {out[True][1]}")
    f2a = out[True][1] == out[False][1]
    earlier = [i for i in range(len(D_HUMAN))
               if out[True][0][i] is not None and (out[False][0][i] is None or out[True][0][i] < out[False][0][i])]
    print(f"   F2a Fisher triggers identical -> {lab(f2a)}"); labels["F2a"] = f2a
    print(f"   F2b Euclidean triggers earlier in {len(earlier)} of {len(D_HUMAN)} -> {lab(len(earlier) >= 1)}"); labels["F2b"] = len(earlier) >= 1

    # ---- F3: P3/P5, the human schedule in steps under three decays of Delta
    print("\n== F3  P3/P5: FOREVER's thresholds in steps when Delta decays (standard calculus; a consistency relation)")
    from scipy.special import digamma
    c = 50.0
    def cross(f_tau, day, d, hi=10 ** 12):
        lo, hi_ = 1, 1
        while f_tau(hi_) < d * day and hi_ < hi: hi_ *= 2
        lo = hi_ // 2 if hi_ > 1 else 1
        while lo < hi_:
            mid = (lo + hi_) // 2
            if f_tau(mid) >= d * day: hi_ = mid
            else: lo = mid + 1
        return lo
    tau_const = lambda t: float(t)
    tau_inv = lambda t: float(digamma(t + c + 1) - digamma(c + 1))                 # sum_{i=1..t} 1/(i + c)
    tau_sqrt_cum = None
    t_const = [cross(tau_const, tau_const(S_WARM), d) for d in D_HUMAN]
    t_inv = [cross(tau_inv, tau_inv(S_WARM), d) for d in D_HUMAN]
    pred_decl = [c * ((1 + S_WARM / c) ** d - 1) for d in D_HUMAN]
    pred_half = [(c + 0.5) * ((S_WARM + c + 0.5) / (c + 0.5)) ** d - (c + 0.5) for d in D_HUMAN]
    sq = np.cumsum(1.0 / np.sqrt(np.arange(1, 2_000_001) + c)); t_sqrt = []
    for d in D_HUMAN:
        idx = np.nonzero(sq >= d * sq[S_WARM - 1])[0]; t_sqrt.append(int(idx[0]) + 1 if idx.size else None)
    print(f"   constant Delta: trigger steps {t_const}; d * S = {[d * S_WARM for d in D_HUMAN]}")
    f3b = t_const == [d * S_WARM for d in D_HUMAN]
    print(f"   F3b constant Delta reproduces the human schedule in steps -> {lab(f3b)}"); labels["F3b"] = f3b
    print(f"   Delta = 1/(t + {c:g}): trigger steps {t_inv}")
    print(f"      declared formula c((1 + S/c)^d - 1): {[round(v, 1) for v in pred_decl]}")
    errs = [abs(a - b) for a, b in zip(t_inv, pred_decl)]
    print(f"   F3a within one step of the declared formula at every d: max error {max(errs):.1f} steps -> {lab(max(errs) <= 1.0)}"); labels["F3a"] = max(errs) <= 1.0
    errs_h = [abs(a - b) for a, b in zip(t_inv, pred_half)]
    print(f"      (post hoc, not a declared check: the half-step-corrected formula (c + 1/2)((S + c + 1/2)/(c + 1/2))^d - (c + 1/2) gives "
          f"{[round(v, 1) for v in pred_half]}, max error {max(errs_h):.1f} steps)")
    print(f"   Delta = 1/sqrt(t + {c:g}): trigger steps {t_sqrt} (power-law growth of the intervals)")

    # ---- F4: H-EQ against FOREVER's intensity-aware weight, on an anchor that starts at zero
    print("\n== F4  H-EQ (Omega = 1) against FOREVER's weight (10), anchor penalty w c |theta - theta*|^2 with theta* = theta_0")
    H = np.diag([1.0, 2.0, 0.5, 1.5, 3.0]); a = np.array([2.0, 1.0, -1.0, 0.5, 0.0]); th0 = np.zeros(5); eta = 0.05; T4 = 2000
    GRID = (0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0)

    def total(th, cc):
        return float(0.5 * (th - a) @ H @ (th - a) + cc * np.sum((th - th0) ** 2))

    def run(mode, cc, w=None, gamma=None, beta_base=None, omega=1.0, smooth=0.9, cap=1e4):
        th = th0.copy(); ep = eq = None; ws = []; deltas = []; mu = mu0 = None
        for t in range(T4):
            gp = H @ (th - a); gq = 2 * cc * (th - th0)
            if mode == "fixed": wt = w
            elif mode == "rule":
                ep = gp if ep is None else smooth * ep + (1 - smooth) * gp
                eq = gq if eq is None else smooth * eq + (1 - smooth) * gq
                wt = min(omega * np.linalg.norm(ep) / max(np.linalg.norm(eq), 1e-12), cap)
            else:                                                     # FOREVER eq. (10), warm-up at scale 1
                if t < S_WARM or mu0 is None: wt = beta_base
                else: wt = beta_base * float(np.clip(1 + gamma * (mu / mu0 - 1), G_MIN, G_MAX))
            new = th - eta * (gp + wt * gq)
            if not np.all(np.isfinite(new)) or np.max(np.abs(new)) > 1e6: return float("inf"), ws, True
            dlt = float(np.linalg.norm(new - th)); deltas.append(dlt); th = new; ws.append(wt)
            if mode == "forever":
                if t + 1 == S_WARM: mu0 = float(np.mean(deltas)); mu = mu0
                elif t + 1 > S_WARM: mu = (1 - LAM_EMA) * mu + LAM_EMA * dlt
        return total(th, cc), ws, False

    fixed1 = {w: run("fixed", 1.0, w=w)[0] for w in GRID}; w_star = min(fixed1, key=fixed1.get)
    print(f"   fixed w at c = 1: best {w_star:g} (total {fixed1[w_star]:.6f})")
    rule = {cc: run("rule", cc) for cc in (1.0, 16.0, 256.0)}
    capfrac = float(np.mean(np.array(rule[1.0][1][:50]) >= 1e4))
    fore = {}
    for g in (0.5, 1.0, 2.0):
        tuned = {b: run("forever", 1.0, gamma=g, beta_base=b)[0] for b in GRID}; bb = min(tuned, key=tuned.get)
        fore[g] = dict(bb=bb, res={cc: run("forever", cc, gamma=g, beta_base=bb) for cc in (1.0, 16.0, 256.0)})
    inb = all(G_MIN * f["bb"] - 1e-15 <= wt <= G_MAX * f["bb"] + 1e-15 for f in fore.values() for wt in f["res"][1.0][1])
    f4a = capfrac >= 0.5 and inb
    print(f"   F4a rule weight at its cap on {capfrac:.2f} of the first 50 steps (>= 0.5); FOREVER's weight inside [g_min, g_max] beta_base at every step: {inb} -> {lab(f4a)}")
    labels["F4a"] = f4a
    for g, f in fore.items():
        print(f"      FOREVER gamma {g:g}: beta_base tuned at c = 1: {f['bb']:g}; totals " +
              ", ".join(f"c {cc:g}: {'DIVERGES' if f['res'][cc][2] else format(f['res'][cc][0], '.6f')}" for cc in (1.0, 16.0, 256.0)))
    print("      the rule (Omega = 1): totals " + ", ".join(f"c {cc:g}: {'DIVERGES' if rule[cc][2] else format(rule[cc][0], '.6f')}" for cc in (1.0, 16.0, 256.0))
          + f"; fixed w = {w_star:g} (tuned at c = 1) at c 16 / 256: " + ", ".join('DIVERGES' if run('fixed', cc, w=w_star)[2] else format(run('fixed', cc, w=w_star)[0], '.6f') for cc in (16.0, 256.0)))
    fdiv = any(f["res"][cc][2] for f in fore.values() for cc in (16.0, 256.0)); rfin = not any(rule[cc][2] for cc in rule)
    print(f"   F4b FOREVER (beta_base held) diverges at c 16 or 256 for some gamma: {fdiv}; the rule finite at every c: {rfin} -> {lab(fdiv and rfin)}")
    labels["F4b"] = fdiv and rfin
    lims = []
    for g, f in fore.items():
        wl = f["res"][1.0][1][-1]; tgt = f["bb"] * max(G_MIN, 1 - g); lims.append(abs(wl / tgt - 1))
        print(f"      gamma {g:g}: last weight {wl:.6g}, beta_base max(g_min, 1 - gamma) = {tgt:.6g}")
    print(f"   F4c the weight tends to beta_base max(g_min, 1 - gamma) within 1 %: max relative error {max(lims):.3e} -> {lab(max(lims) <= 0.01)}")
    labels["F4c"] = max(lims) <= 0.01
    best_fore = min(f["res"][1.0][0] for f in fore.values())
    print(f"   F4d at c = 1 the rule's total {rule[1.0][0]:.6f} <= FOREVER's best {best_fore:.6f} -> {lab(rule[1.0][0] <= best_fore)}")
    labels["F4d"] = rule[1.0][0] <= best_fore

    # ---- F5: pause on the learner's own clock (E2, Proposition 7) — the recorded Delta sequence of the base run
    PAUSE_AT = 100                                                              # Amendment 1 (declared: 300; no replay followed it)
    print(f"\n== F5  A3 + E2 + Proposition 7 (Amendment 1): a pause of L wall ticks after update {PAUSE_AT} (no update during it)")
    res5 = {}
    for L in (0, 50, 500):
        ticks = np.concatenate([np.arange(1, PAUSE_AT + 1), np.arange(PAUSE_AT + 1, 601) + L])   # wall tick of each update
        tau_trig = triggers(dE)                                                # counted in updates: no update in the pause
        wall_trig = []                                                          # thresholds on wall ticks, day = S ticks
        for d in D_HUMAN:
            idx = np.nonzero(ticks >= d * S_WARM)[0]; wall_trig.append(int(idx[0]) + 1 if idx.size else None)
        # beta at the first replay after the pause (gamma = 1), EMA per update (Algorithm 1) and per wall tick (Delta = 0 in the pause)
        first = next((t for t in tau_trig if t is not None and t > PAUSE_AT), None)
        if first is None:
            print(f"   L {L}: no replay follows the pause; F5c undefined (the script stops here)"); return 1
        mu0 = float(np.mean(dE[:S_WARM]))
        mu = mu0
        for t in range(S_WARM, first): mu = (1 - LAM_EMA) * mu + LAM_EMA * dE[t]
        b_upd = float(np.clip(1 + (mu / mu0 - 1), G_MIN, G_MAX))
        mu = mu0
        for t in range(S_WARM, first):
            if t == PAUSE_AT:
                for _ in range(L): mu = (1 - LAM_EMA) * mu
            mu = (1 - LAM_EMA) * mu + LAM_EMA * dE[t]
        b_tick = float(np.clip(1 + (mu / mu0 - 1), G_MIN, G_MAX)); r_tick = mu / mu0
        mu = mu0
        for t in range(S_WARM, first): mu = (1 - LAM_EMA) * mu + LAM_EMA * dE[t]
        print(f"   L {L} (report, post hoc, no label): unclipped r = mu/mu_0 at update {first}: per-update EMA {mu / mu0:.6e}, per-tick EMA {r_tick:.6e}")
        res5[L] = (tau_trig, wall_trig, b_upd, b_tick, first)
        print(f"   L {L}: tau triggers (updates) {tau_trig}; wall-keyed triggers (updates) {wall_trig}; first replay after the pause at update {first}: "
              f"beta/beta_base per-update EMA {b_upd:.6f}, per-tick EMA {b_tick:.6f}")
    f5a = all(res5[L][0] == res5[0][0] for L in res5); f5b = all(res5[L][1] != res5[0][1] for L in (50, 500))
    f5c = all(res5[L][2] == res5[0][2] for L in res5) and all(res5[L][3] != res5[0][3] for L in (50, 500))
    print(f"   F5a tau triggers identical for every L -> {lab(f5a)}; F5b wall-keyed triggers differ for L > 0 -> {lab(f5b)}; "
          f"F5c per-update EMA identical and per-tick EMA different -> {lab(f5c)}")
    labels["F5a"], labels["F5b"], labels["F5c"] = f5a, f5b, f5c

    # ---- F6: arc against chord where the path goes away and comes back
    print("\n== F6  D3 + D4 (chord, surplus) against the arc: task B for 150 steps, then task A again for 150 steps")
    rng6, (XA6, YA6), (XB6, YB6), probe6, W06, P6, Q6 = setup()
    P6, Q6 = train(XA6, YA6, W06, P6, Q6, 300, rng6)
    sn6 = [(P6.copy(), Q6.copy())]; P6, Q6 = train(XB6, YB6, W06, P6, Q6, 150, rng6, snaps=sn6); P6, Q6 = train(XA6, YA6, W06, P6, Q6, 150, rng6, snaps=sn6)
    dE6 = euclid_deltas(sn6); dF6, ps6 = fisher_deltas(sn6, probe6, W06)
    chE = np.array([np.sqrt(np.sum((p - sn6[0][0]) ** 2) + np.sum((q - sn6[0][1]) ** 2)) for p, q in sn6[1:]])
    chF = np.array([np.sqrt(max(2 * kl_step(ps6[0], p), 0.0)) for p in ps6[1:]])
    arcE, arcF = np.cumsum(dE6), np.cumsum(dF6)
    def ce(X, Y, P, Q): return float(-np.mean(np.sum(Y * np.log(np.clip(probs(X, W06, P, Q), 1e-12, 1)), axis=1)))
    lossA0 = ce(XA6, YA6, *sn6[0]); lossAmid = ce(XA6, YA6, *sn6[150]); lossA1 = ce(XA6, YA6, *sn6[-1])
    trig = {n: [t for t in (triggers(v) if n.startswith("arc") else chord_triggers(v)) if t is not None]
            for n, v in (("arc Euclid", dE6), ("arc Fisher", dF6), ("chord Euclid", chE), ("chord Fisher", chF))}
    print(f"   old-task (A) loss: start {lossA0:.6f}, after task B {lossAmid:.6f}, end {lossA1:.6f}")
    print(f"   Euclid: arc {arcE[-1]:.6f}, chord at end {chE[-1]:.6f}, surplus {arcE[-1] - chE[-1]:.6f}; Fisher: arc {arcF[-1]:.6f}, chord at end {chF[-1]:.6f}, "
          f"surplus {arcF[-1] - chF[-1]:.6f}")
    for n, v in trig.items(): print(f"   {n}: {len(v)} triggers at {v}")
    f6a = (len(trig["arc Euclid"]) - len(trig["chord Euclid"]) >= 2) and (len(trig["arc Fisher"]) - len(trig["chord Fisher"]) >= 2)
    print(f"   F6a the arc clocks fire at least 2 more triggers than the chord clocks (both metrics) -> {lab(f6a)}"); labels["F6a"] = f6a

    print("\nsummary: " + "; ".join(f"{k} {lab(v)}" for k, v in labels.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
