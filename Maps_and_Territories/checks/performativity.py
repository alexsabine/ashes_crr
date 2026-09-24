"""Maps that change their territory: checks P1-P5, declared in Maps_and_Territories/DECLARATION.md (pushed in 7e871a1 before
this file existed). Synthetic worlds only; seeded; every verdict word is computed from the numbers (R15).
Run: uv run python Maps_and_Territories/checks/performativity.py > Maps_and_Territories/checks/performativity.txt"""
import math
import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.stats import norm


def K(v):
    v = np.asarray(v, float); return (v / 2.0) * (np.sqrt(v * v + 4.0) - v)


# ------------------------------------------------------------------ P1
def p1():
    print("P1 the map-territory trade-off in World L: Y = mu + gamma f + eps (f = 0 is the empty map)")
    mu, g, f, s = sp.symbols("mu gamma f sigma", real=True)
    infl = g * f; err_read = (mu + (g - 1) * f) ** 2 + s ** 2
    zero_infl = sp.solve(sp.Eq(infl, 0), f)                                     # gamma != 0
    fstar = sp.solve(sp.diff(err_read, f), f)[0]; curv = sp.simplify(sp.diff(err_read, f, 2))
    err_cf_read = sp.simplify(err_read.subs(f, mu) - s ** 2 - (g * mu) ** 2)
    ok_a = zero_infl == [0]; ok_b = sp.simplify(fstar - mu / (1 - g)) == 0 and sp.simplify(curv - 2 * (g - 1) ** 2) == 0
    ok_c = err_cf_read == 0; ok = ok_a and ok_b and ok_c
    print(f"   (a) influence gamma f = 0 only at f = {zero_infl} (for gamma != 0): the empty map -> {'holds' if ok_a else 'FAILS'}")
    print(f"   (b) the error when read is smallest at f* = {sp.simplify(fstar)} (curvature {curv} > 0 for gamma != 1); its influence is gamma mu/(1 - gamma) -> {'holds' if ok_b else 'FAILS'}")
    print(f"   (c) the counterfactual map f = mu, when read, is wrong by (gamma mu)^2 in squared error (residual {err_cf_read}): wrong by exactly its influence -> {'holds' if ok_c else 'FAILS'}")
    print("   grid (mu = 1, sigma = 1): gamma | empty map: influence, error when read | counterfactual map: influence, error when read | self-consistent map: f*, influence, error when read")
    for gv in (-1.5, -0.5, 0.5, 0.9, 0.99):
        m, sg = 1.0, 1.0; er = lambda ff: (m + (gv - 1) * ff) ** 2 + sg ** 2; fs = m / (1 - gv)
        print(f"      {gv:5}: 0.000, {er(0.0):.4f} | {gv * m:.3f}, {er(m):.4f} | {fs:.3f}, {gv * fs:.3f}, {er(fs):.4f}")
    print(f"   P1 {'holds' if ok else 'FAILS'}: no map is both influence-free and right when read unless mu = 0 or gamma = 0; the influence of the right-when-read map, gamma/(1 - gamma), grows without bound as gamma -> 1")
    return ok


# ------------------------------------------------------------------ P2
def p2():
    print("P2 learning from a territory one has changed: f <- f + alpha (y - f), y = mu + gamma f + eps (all forecasts read), mu 1, sigma 1, 5000 steps, 20 seeds")
    agree = 0; total = 0
    for gv in (-3.0, -1.0, 0.0, 0.5, 1.2):
        parts = []
        for a in (0.05, 0.3, 0.8):
            r = 1 - a * (1 - gv)
            ana = "diverge" if abs(r) >= 1 else ("oscillate" if r < 0 else "converge")
            rng = np.random.default_rng(2000 + int(100 * gv) + int(100 * a)); F = np.zeros(20); hist = []
            with np.errstate(over="ignore", invalid="ignore"):
                for t in range(5000):
                    y = 1.0 + gv * F + rng.normal(size=20); F = F + a * (y - F)
                    if t >= 3000: hist.append(F.copy())
            H = np.array(hist)
            if not np.all(np.isfinite(H)) or np.max(np.abs(H)) > 1e6: sim = "diverge"
            else:
                D = H - H.mean(axis=0); rho = float(np.mean(np.sum(D[1:] * D[:-1], axis=0) / np.sum(D * D, axis=0)))
                sim = "oscillate" if rho < 0 else "converge"
            agree += ana == sim; total += 1; parts.append(f"alpha {a}: r {r:+.3f} analytic {ana}, simulated {sim}")
        print(f"   gamma {gv:+.1f}: " + "; ".join(parts))
    print(f"   the analytic rule classifies {agree}/{total} cells as the simulation does -> {'holds' if agree == total else 'FAILS'}")
    print("   the Regeneration Law beside it: in P2's world mu is constant, so v = 0 and K(v) = 0 (the no-feedback optimum never destabilises it);"
          " in a drifting world with v > 0 the no-feedback optimum K(v) destabilises the loop exactly when gamma < 1 - 2/K(v):")
    for v in (0.3, 1.0, 3.0):
        k = float(K(v)); print(f"      v {v}: K(v) {k:.4f}; unstable for gamma < {1 - 2 / k:.3f}")
    return agree == total


# ------------------------------------------------------------------ P3
def p_dev(f): return 0.1 + 0.88 * norm.cdf((f - 0.45) / 0.1)


def p3():
    print("P3 the map chooses the territory (currency peg): p(f) = 0.1 + 0.88 Phi((f - 0.45)/0.1) when the forecast f is read; unread, speculators see theta = 0.3 only")
    grid = np.linspace(0, 1, 100001); h = p_dev(grid) - grid; fps = []
    for i in np.where(np.sign(h[:-1]) != np.sign(h[1:]))[0]:
        fps.append(brentq(lambda x: p_dev(x) - x, grid[i], grid[i + 1], xtol=1e-14))
    stab = []
    for x in fps:
        d = 0.88 * norm.pdf((x - 0.45) / 0.1) / 0.1; stab.append("stable" if abs(d) < 1 else "unstable")
        print(f"   fixed point f = p(f) = {x:.6f}: slope p'(f) {d:.4f} -> {stab[-1]}; Brier when read p(1 - p) = {x * (1 - x):.6f}")
    ends = []
    for f0 in (0.05, 0.25, 0.45, 0.5, 0.7, 0.95):
        f = f0
        for _ in range(500): f = p_dev(f)
        ends.append(f); print(f"   repeated retraining from f0 {f0}: ends at {f:.6f}")
    g2 = np.linspace(0, 1, 10001); P = p_dev(g2); brier = P * (1 - g2) ** 2 + (1 - P) * g2 ** 2; fb = float(g2[np.argmin(brier)])
    pb = float(p_dev(fb)); print(f"   the accuracy-maximising read forecast (argmin expected Brier, grid 1e-4): f = {fb:.4f}, devaluation probability it produces {pb:.6f}, expected Brier {float(brier.min()):.6f}")
    p0 = float(p_dev(0.3)); f = p0
    for _ in range(500): f = p_dev(f)
    print(f"   the counterfactual forecast f = p(theta) = {p0:.6f}; read, it produces {float(p_dev(p0)):.6f}; retraining from it ends at {f:.6f}")
    calm = [x for x, s in zip(fps, stab) if s == "stable" and x < 0.45]; crisis = [x for x, s in zip(fps, stab) if s == "stable" and x > 0.45]
    ok_a = len(fps) == 3 and len(calm) == 1 and len(crisis) == 1 and stab.count("unstable") == 1
    ok_b = any(abs(e - calm[0]) < 1e-6 for e in ends) and any(abs(e - crisis[0]) < 1e-6 for e in ends) if ok_a else False
    ok_c = ok_a and abs(pb - crisis[0]) < abs(pb - calm[0])
    ok_d = ok_a and abs(f - calm[0]) < 1e-6
    print(f"   (a) three fixed points, calm and crisis stable: {'holds' if ok_a else 'FAILS'}; (b) the starting belief picks the equilibrium: {'holds' if ok_b else 'FAILS'};"
          f" (c) the accuracy-maximising forecaster ends at the crisis: {'holds' if ok_c else 'FAILS'}; (d) the counterfactual forecast leads to the calm: {'holds' if ok_d else 'FAILS'}")
    return ok_a and ok_b and ok_c and ok_d


# ------------------------------------------------------------------ P4
def p4():
    print("P4 Goodhart: X = G + 0.5 eta + s Z (Z = |N(0,1)| gaming capacity, independent of G), 200 000 agents")
    rng = np.random.default_rng(404); n = 200000; G = rng.normal(size=n); eta = rng.normal(size=n); Z = np.abs(rng.normal(size=n))
    cs, ms = [], []
    for s in (0.0, 0.25, 0.5, 1.0, 2.0):
        X = G + 0.5 * eta + s * Z; c = float(np.corrcoef(X, G)[0, 1]); top = X >= np.quantile(X, 0.9); m = float(G[top].mean())
        cs.append(c); ms.append(m); print(f"   stake s {s}: corr(X, G) {c:.4f}; mean G of the top 10 % on X {m:.4f}")
    mono = all(cs[i] > cs[i + 1] for i in range(4)) and all(ms[i] > ms[i + 1] for i in range(4)); base = abs(cs[0] - 1 / math.sqrt(1.25)) < 0.005
    print(f"   both fall monotonically in the stake: {'holds' if mono else 'FAILS'}; at s = 0 the correlation is the ungamed 1/sqrt(1.25) = {1 / math.sqrt(1.25):.4f}: {'holds' if base else 'FAILS'}")
    return mono and base


# ------------------------------------------------------------------ P5
AGRID = np.array([0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.4]); BGRID = np.array([0.001, 0.003, 0.01, 0.03])
SEEDS, STEPS, BURN, ERASE, SIG, MU0 = 20, 20000, 2000, 0.1, 1.0, 2.0


def world(kind, seed):
    rng = np.random.default_rng(5000 + seed + 1000 * {"G+": 0, "G-": 1, "G0": 2}[kind])
    q = 0.05; mu = MU0 + np.concatenate([[0.0], np.cumsum(q * rng.normal(size=STEPS - 1))])
    if kind == "G+": gam = np.full(STEPS, 0.5)
    elif kind == "G0": gam = np.zeros(STEPS)
    else: gam = 0.5 + np.concatenate([[0.0], np.cumsum(0.05 * rng.normal(size=STEPS - 1))])
    read = rng.uniform(size=STEPS) >= ERASE; eps = SIG * rng.normal(size=STEPS)
    return mu, gam, read, eps


def run_arms(mu, gam, read, eps):
    """All gain settings at once. Returns dict arm -> (rmse array over configs, mean bias array, slope array)."""
    nA = AGRID.size; cfgC = [(a, b) for a in AGRID for b in BGRID]; aC = np.array([c[0] for c in cfgC]); bC = np.array([c[1] for c in cfgC])
    fA = np.zeros(nA); mB = np.zeros(nA); mC = np.zeros(len(cfgC)); gC = np.zeros(len(cfgC))
    sA = np.zeros(nA); sB = np.zeros(nA); sC = np.zeros(len(cfgC)); bA = np.zeros(nA); n = 0
    xy = np.zeros(nA); xx = 0.0
    with np.errstate(over="ignore", invalid="ignore"):
        for t in range(STEPS):
            m_t, g_t, r_t, e_t = mu[t], gam[t], read[t], eps[t]
            if t >= BURN:
                sA += (fA - m_t) ** 2; sB += (mB - m_t) ** 2; sC += (mC - m_t) ** 2; bA += fA - m_t; n += 1
                xy += (fA - m_t) * m_t; xx += m_t * m_t
            yA = m_t + g_t * fA * r_t + e_t; fA = fA + AGRID * (yA - fA)
            yB = m_t + g_t * mB * r_t + e_t
            if not r_t: mB = mB + AGRID * (yB - mB)
            fC = mC; yC = m_t + g_t * fC * r_t + e_t
            if r_t:
                res = yC - mC - gC * fC; gC = gC + bC * res * fC / (fC * fC + 1.0)
                mC = mC + aC * (yC - gC * fC - mC)
            else:
                mC = mC + aC * (yC - mC)
    rm = lambda s: np.where(np.isfinite(s), np.sqrt(s / n), np.inf)
    return dict(A=(rm(sA), bA / n, xy / xx), B=(rm(sB),), C=(rm(sC),)), cfgC


def p5():
    print(f"P5 learning without a stake in a drifting world: mu_t random walk (sd 0.05), erasure {ERASE}, sigma {SIG}, mu_0 {MU0}; {SEEDS} seeds x {STEPS} steps (burn-in {BURN});"
          f" gains tuned on each world's own seeds (grid alpha {AGRID.tolist()}, beta {BGRID.tolist()})")
    out = {}
    for kind in ("G+", "G-", "G0"):
        R = [run_arms(*world(kind, s)) for s in range(SEEDS)]; cfgC = R[0][1]
        rA = np.array([r[0]["A"][0] for r in R]); rB = np.array([r[0]["B"][0] for r in R]); rC = np.array([r[0]["C"][0] for r in R])
        with np.errstate(invalid="ignore"):
            iA = int(np.argmin(np.mean(np.where(np.isfinite(rA), rA, 1e300), axis=0))); iB = int(np.argmin(np.mean(rB, axis=0)))
            iC = int(np.argmin(np.mean(np.where(np.isfinite(rC), rC, 1e300), axis=0)))
        A, B, C = rA[:, iA], rB[:, iB], rC[:, iC]; ahead = int(np.sum(C <= 0.9 * B))
        biasA = np.array([r[0]["A"][1][iA] for r in R]); slopeA = np.array([r[0]["A"][2][iA] for r in R])
        mus = np.array([np.mean(world(kind, s)[0][BURN:]) for s in range(SEEDS)])
        g0 = 0.5 if kind != "G0" else 0.0
        ratio = float(np.sum(biasA) / np.sum(g0 / (1 - g0) * mus)) if g0 != 0 else float("nan")
        out[kind] = dict(ahead=ahead, ratio=ratio)
        print(f"   {kind}: tuned gains A alpha {float(AGRID[iA])}, B alpha {float(AGRID[iB])}, C (alpha, beta) ({float(cfgC[iC][0])}, {float(cfgC[iC][1])})")
        fmt = lambda x: f"{x:.4f}" if np.isfinite(x) and x < 1e6 else "diverged (> 1e6: the self-fulfilling spiral)"
        print(f"      RMSE of f - mu_t, median over seeds: A {fmt(np.median(A))}, B {fmt(np.median(B))}, C {fmt(np.median(C))}; C <= 0.9 B on {ahead}/{SEEDS} seeds")
        print(f"      per seed C/B: " + " ".join(f"{c / b:.3f}" if np.isfinite(c / b) else "inf" for c, b in zip(C, B)))
        if g0 != 0:
            print(f"      A's bias: pooled mean(f - mu) / mean(gamma mu/(1 - gamma)) = {fmt(ratio)}; regression slope of (f - mu) on mu, median {fmt(np.median(slopeA))}"
                  f" (declared target gamma/(1 - gamma) = {g0 / (1 - g0):.4f}; with erasure the fixed point is (1-e)gamma/(1-(1-e)gamma) = {(1 - ERASE) * g0 / (1 - (1 - ERASE) * g0):.4f})")
        else:
            print(f"      A's bias with no reflexivity: pooled mean(f - mu) {float(np.mean(biasA)):+.4f}; slope median {np.median(slopeA):+.4f}")
    gp_c = out["G+"]["ahead"] >= 18; gp_a = abs(out["G+"]["ratio"] - 1) <= 0.1; gm = (SEEDS - out["G-"]["ahead"]) >= 18
    print(f"   gate as declared: G+ C ahead on >= 18/20: {'holds' if gp_c else 'FAILS'} ({out['G+']['ahead']}/20); G+ A's bias within 10 % of gamma mu/(1 - gamma): {'holds' if gp_a else 'FAILS'} (ratio {out['G+']['ratio']:.4f});"
          f" G- C NOT ahead on >= 18/20: {'holds' if gm else 'FAILS'} (not ahead on {SEEDS - out['G-']['ahead']}/20)")
    verdict = "GATE OPEN" if (gp_c and gp_a and gm) else "GATE CLOSED"
    print(f"   P5 {verdict}" + ("" if gm else " (G- passes: C's advantage is not about removing its own influence; the claim is withdrawn)"))
    return verdict


def main():
    print("Maps that change their territory: checks P1-P5 (Maps_and_Territories/DECLARATION.md)")
    r = [p1(), p2(), p3(), p4()]; v5 = p5()
    print(f"summary: P1 {'holds' if r[0] else 'FAILS'}; P2 {'holds' if r[1] else 'FAILS'}; P3 {'holds' if r[2] else 'FAILS'}; P4 {'holds' if r[3] else 'FAILS'}; P5 {v5}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
