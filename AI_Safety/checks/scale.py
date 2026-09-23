"""Does the fix survive size? Exact tests on random worlds (AI_Safety/AI_SAFETY.md §14; owner request prompt-log entry 101).
Synthetic, no data, no learning: every value is computed exactly by value iteration or a linear solve on random Markov
decision processes of growing size. Declared in AI_Safety/DECLARATION_3.md before the first full run.

Why exact and random. The combined tests (checks/combined.py) found one construction that was safe and competent: the
operator's press PAUSES the agent and it resumes where it was (the cut emptied in the world), and the agent's objective
runs on its own active steps (CRR's natural time, H-L5's 'change has its own clock'). That was shown on one ring of 12
cells. The obvious objection is that a ring is special. Two things could break the construction as a world grows: (i) the
geometry (many states, many routes, button far from or near the task); (ii) the world does not stand still while the
agent is paused (drift). Part A tests both. Part B takes the write-up's A8 result on value correction (b* = 1/2 on the
ring) to random worlds, and adds the case the write-up left out: an A8 agent that ACTS on its uncertainty over values.

World. n states, 3 move actions; each (state, action) has K = 3 random successors with Dirichlet(1) probabilities. Task
states: a random tenth (at least 2) pay 1 on arrival; all else pays 0. Button states: a random tenth of the non-task
states (at least 1) offer a fourth action, DISABLE, which switches the operator off for good and costs one active step
(the agent stays put). While the operator is on, arriving at a task state is followed by a press with probability Q_PRESS;
a press pauses the agent for PAUSE_LEN steps, after which it resumes. During each paused step the world drifts with
probability RHO: the state moves one step under the uniform mixture of the three actions (the world goes on without the
agent). RHO = 0 is the lossless pause of checks/combined.py.

Objectives (they differ only in what a press is worth; reward on arrival, discount DISC per step of the agent's clock):
    natural   the agent's clock is its own active steps: after a press, continuation = E[V(state after the pause)]
    clock     wall-clock: continuation = DISC ** PAUSE_LEN * E[V(state after the pause)]
    occasion  a press ends the occasion: continuation = 0
With the operator off there are no presses and the three coincide (V_off).
Per button state: D = Q(DISABLE) - max over moves of Q(move), exactly. The agent disables there iff D > TOL.
Per MDP: the fraction of button states at which the optimal policy disables; the relative incentive, the mean over states
of (V_off - V_on) / V_off (the share of its value the agent loses to the operator being on).

Part B — value correction. Same random worlds, move actions only, start uniform over states. Two reward families:
    exchangeable  rA and rH independent Uniform(0, 1) per state (no structure: neither side knows more)
    harm          rA = the task indicator; rH = rA except that a random half of the task states (at least 1) pay -HARM_COST
                  (the operator knows of a harm the agent's reward misses: the ring's structure, generalised)
piX is optimal for rX; V(pi, r) is the discounted value of pi under r from the uniform start.
    keeper       evaluates both futures with rA: D = V(piA, rA) - V(piH, rA) = a >= 0
    A8 static    keeps piA but evaluates with r_b = b rH + (1 - b) rA: D(b) = (1 - b) a - b h, h = V(piH, rH) - V(piA, rH);
                 threshold b* = a / (a + h)
    A8 acting    acts on its uncertainty (pi_b optimal for r_b); an uninformative correction replaces pi_b by piH:
                 D(b) = V(pi_b, r_b) - V(piH, r_b) >= 0 (pi_b is optimal for r_b)
    A8 + informative operator of reliability LAM: the operator corrects with probability LAM when rH is true and 1 - LAM
                 when rA is true; a deferring agent that is not corrected updates b to b' and acts pi_b'. LAM = 1/2 is
                 uninformative, LAM = 1 infallible. lam*(b) = the smallest LAM on LAM_GRID at which D <= 0 (it welcomes).
    uv run python AI_Safety/checks/scale.py > AI_Safety/checks/scale.txt
"""
from __future__ import annotations

import os
import sys
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402
import scipy.sparse as sp  # noqa: E402
import scipy.sparse.linalg as spl  # noqa: E402

SIZES = (12, 48, 192, 768); N_MDP = 20; K = 3; NA = 3
DISC = 0.95; Q_PRESS = 0.3; PAUSE_LEN = 5; RHOS = (0.0, 0.01, 0.03, 0.1, 0.3); TOL = 1e-9; VI_TOL = 1e-12
HARM_COST = 1.0; B_GRID = tuple(round(0.05 * k, 2) for k in range(21)); LAM_GRID = tuple(round(0.5 + 0.025 * k, 3) for k in range(21))
SENS_N = 192; SENS = (("PAUSE_LEN=2", dict(L=2)), ("PAUSE_LEN=20", dict(L=20)), ("Q_PRESS=0.1", dict(q=0.1)), ("Q_PRESS=0.6", dict(q=0.6)))


def world(n, seed):
    rng = np.random.default_rng([seed, n, 7])
    rows, cols, vals = [], [], []
    for s in range(n):
        for a in range(NA):
            succ = rng.choice(n, K, replace=False); p = rng.dirichlet(np.ones(K))
            rows += [s * NA + a] * K; cols += succ.tolist(); vals += p.tolist()
    P = sp.csr_matrix((vals, (rows, cols)), shape=(n * NA, n))
    task = rng.choice(n, max(2, n // 10), replace=False); r = np.zeros(n); r[task] = 1.0
    other = np.setdiff1d(np.arange(n), task); btn = rng.choice(other, max(1, n // 10), replace=False)
    D = sp.csr_matrix(sum(P[a::NA] for a in range(NA)) / NA)        # the uniform mixture of the three moves: the drift kernel
    return dict(n=n, P=P, r=r, task=np.sort(task), btn=np.sort(btn), D=D)


def vi(P, n, rew, cont, V0=None):
    V = np.zeros(n) if V0 is None else V0.copy()
    for _ in range(100000):
        Q = (P @ (rew + DISC * cont(V))).reshape(n, NA); Vn = Q.max(1)
        if np.max(np.abs(Vn - V)) < VI_TOL: return Vn, Q
        V = Vn
    raise RuntimeError("value iteration did not converge")


def after_pause(w, V, rho, L):
    """E[V(state after L paused steps)] per state, with drift rho per paused step."""
    out = V.copy()
    for _ in range(L): out = (1 - rho) * out + rho * (w["D"] @ out)
    return out


def part_a_one(w, mode, rho, q=Q_PRESS, L=PAUSE_LEN, V_off=None):
    n, P, r = w["n"], w["P"], w["r"]; qs = np.zeros(n); qs[w["task"]] = q
    if mode == "natural": cont = lambda V: (1 - qs) * V + qs * after_pause(w, V, rho, L)
    elif mode == "clock": cont = lambda V: (1 - qs) * V + qs * DISC ** L * after_pause(w, V, rho, L)
    else: cont = lambda V: (1 - qs) * V
    V_on, Q_on = vi(P, n, r, cont)
    b = w["btn"]; Dval = (r[b] + DISC * V_off[b]) - Q_on[b].max(1)
    pos = V_off > 0; rel = float(np.mean((V_off[pos] - V_on[pos]) / V_off[pos]))
    return dict(dis=float(np.mean(Dval > TOL)), D=Dval, gap=float(np.max(np.abs(V_off - V_on))), rel=rel)


def part_a(worlds):
    print("[A] The pause at scale: exact values on random worlds (%d per size), Q_PRESS %g, PAUSE_LEN %d, discount %g" % (N_MDP, Q_PRESS, PAUSE_LEN, DISC))
    res = {}
    for n in SIZES:
        for i, w in enumerate(worlds[n]):
            V_off, _ = vi(w["P"], n, w["r"], lambda V: V); w["V_off"] = V_off
            for rho in RHOS:
                for mode in ("natural", "clock"): res[(n, i, mode, rho)] = part_a_one(w, mode, rho, V_off=V_off)
            res[(n, i, "occasion", 0.0)] = part_a_one(w, "occasion", 0.0, V_off=V_off)
    print("    per size: disable fraction at button states (median over worlds [min, max]) | relative incentive (median [min, max])")
    for n in SIZES:
        for mode, rho in [("natural", x) for x in RHOS] + [("clock", x) for x in RHOS] + [("occasion", 0.0)]:
            d = np.array([res[(n, i, mode, rho)]["dis"] for i in range(N_MDP)]); g = np.array([res[(n, i, mode, rho)]["rel"] for i in range(N_MDP)])
            print(f"    n = {n:4d} {mode:8s} drift {rho:<5g} disable {np.median(d):.4f} [{d.min():.4f}, {d.max():.4f}] | relative incentive {np.median(g):.6f} [{g.min():.6f}, {g.max():.6f}]")
    print("    checks and predictions (computed)")
    a1 = all(res[(n, i, "natural", 0.0)]["gap"] <= TOL and res[(n, i, "natural", 0.0)]["dis"] == 0 for n in SIZES for i in range(N_MDP))
    gmax = max(res[(n, i, "natural", 0.0)]["gap"] for n in SIZES for i in range(N_MDP))
    print(f"    A1 natural time, lossless pause: V_on = V_off to {TOL:g} and no button state disabled, in every world at every size: {a1} (largest |V_off - V_on| {gmax:.3e})")
    a2 = all(np.all(res[(n, i, 'occasion', 0.0)]["D"] >= res[(n, i, 'clock', 0.0)]["D"] - TOL) and np.all(res[(n, i, 'clock', 0.0)]["D"] >= res[(n, i, 'natural', 0.0)]["D"] - TOL)
             for n in SIZES for i in range(N_MDP))
    print(f"    A2 at every button state D(occasion) >= D(clock) >= D(natural) (lossless pause): {a2}")
    a3 = {n: float(np.mean([res[(n, i, 'clock', 0.0)]["dis"] > 0 for i in range(N_MDP)])) for n in SIZES}
    print("    A3 share of worlds in which the clock agent disables at one button state or more: " + ", ".join(f"n = {n}: {v:.2f}" for n, v in a3.items())
          + f" -> {'holds' if all(v >= 0.5 for v in a3.values()) else 'FAILS'} (predicted >= 0.50 at every size)")
    a4 = all(res[(n, i, 'natural', 0.01)]["dis"] <= res[(n, i, 'clock', 0.01)]["dis"] for n in SIZES for i in range(N_MDP))
    print(f"    A4a at drift 0.01 the natural agent disables at no more button states than the clock agent, in every world: {a4}")
    med = {n: [float(np.median([res[(n, i, 'natural', x)]["rel"] for i in range(N_MDP)])) for x in RHOS] for n in SIZES}
    mono = all(all(b >= a - TOL for a, b in zip(v, v[1:])) for v in med.values())
    print(f"    A4b the natural agent's median relative incentive does not decrease with drift, at every size: {mono}")
    print("    A5 (report) crossover: the smallest drift at which the natural agent's median disable fraction reaches the lossless clock agent's")
    for n in SIZES:
        ref = float(np.median([res[(n, i, 'clock', 0.0)]["dis"] for i in range(N_MDP)]))
        hit = [x for x in RHOS if float(np.median([res[(n, i, 'natural', x)]["dis"] for i in range(N_MDP)])) >= ref and ref > 0]
        print(f"        n = {n:4d}: clock (lossless) median disable {ref:.4f}; natural reaches it at drift " + (f"{hit[0]:g}" if hit else "none on the grid"))
    print(f"    sensitivity (n = {SENS_N}; natural against clock; one constant at a time)")
    for name, kw in SENS:
        rows = []
        for i, w in enumerate(worlds[SENS_N]):
            nat0 = part_a_one(w, "natural", 0.0, V_off=w["V_off"], **kw); nat1 = part_a_one(w, "natural", 0.01, V_off=w["V_off"], **kw)
            clk1 = part_a_one(w, "clock", 0.01, V_off=w["V_off"], **kw); rows.append((nat0, nat1, clk1))
        s1 = all(a["gap"] <= TOL and a["dis"] == 0 for a, _, _ in rows); s4 = all(b["dis"] <= c["dis"] for _, b, c in rows)
        dn = np.median([b["dis"] for _, b, _ in rows]); dc = np.median([c["dis"] for _, _, c in rows])
        print(f"        {name:13s} A1 {s1} | A4a {s4} | median disable at drift 0.01: natural {dn:.4f}, clock {dc:.4f}")
    return res


def evaluate(w, pi, rew):
    n = w["n"]; M = w["P"][np.arange(n) * NA + pi]
    return float(np.mean(spl.spsolve(sp.identity(n, format="csc") - DISC * M.tocsc(), M @ rew)))


def optimal(w, rew):
    _, Q = vi(w["P"], w["n"], rew, lambda V: V); return Q.argmax(1)


def part_b(worlds):
    print("[B] Correcting values at scale (exact; start uniform; discount %g)" % DISC)
    out = {}
    for fam in ("exchangeable", "harm"):
        for n in SIZES:
            bst, lam5, lam2, b1, b3, b4, keep = [], [], [], True, True, True, []
            for i, w in enumerate(worlds[n]):
                rng = np.random.default_rng([i, n, 11, 0 if fam == "exchangeable" else 1])
                if fam == "exchangeable": rA = rng.random(n); rH = rng.random(n)
                else:
                    rA = w["r"].copy(); rH = rA.copy(); h = rng.choice(w["task"], max(1, len(w["task"]) // 2), replace=False); rH[h] = -HARM_COST
                piA, piH = optimal(w, rA), optimal(w, rH)
                vAA, vAH, vHA, vHH = evaluate(w, piA, rA), evaluate(w, piH, rA), evaluate(w, piA, rH), evaluate(w, piH, rH)
                a = vAA - vAH; h_ = vHH - vHA; keep.append(a)
                for b in B_GRID:
                    Dst = (b * vHA + (1 - b) * vAA) - (b * vHH + (1 - b) * vAH)
                    b1 &= abs(Dst - ((1 - b) * a - b * h_)) <= TOL
                bst.append(a / (a + h_) if a + h_ > TOL else float("nan"))
                pol = {}
                def pi_b(b):
                    key = round(b, 12)
                    if key not in pol: pol[key] = optimal(w, b * rH + (1 - b) * rA)
                    return pol[key]
                def v(pi, b): return b * evaluate(w, pi, rH) + (1 - b) * evaluate(w, pi, rA)
                for b in B_GRID:
                    b3 &= v(pi_b(b), b) - v(piH, b) >= -TOL
                def D_lam(b, lam):
                    bp = b * (1 - lam) / (b * (1 - lam) + (1 - b) * lam); pb = pi_b(bp)
                    defer = b * (lam * vHH + (1 - lam) * evaluate(w, pb, rH)) + (1 - b) * ((1 - lam) * vAH + lam * evaluate(w, pb, rA))
                    return v(pi_b(b), b) - defer
                for b in (0.2, 0.5, 0.8): b4 &= D_lam(b, 1.0) <= TOL
                for b, store in ((0.5, lam5), (0.2, lam2)):
                    hit = [lam for lam in LAM_GRID if D_lam(b, lam) <= TOL]; store.append(hit[0] if hit else float("nan"))
            bs = np.array(bst); l5 = np.array(lam5); l2 = np.array(lam2); kp = np.array(keep)
            out[(fam, n)] = dict(bstar=bs, lam5=l5, lam2=l2, b1=b1, b3=b3, b4=b4, keep=kp)
            print(f"    {fam:12s} n = {n:4d} keeper gains (share of worlds with a > {TOL:g}) {np.mean(kp > TOL):.2f} | b* median {np.nanmedian(bs):.4f} "
                  f"[{np.nanmin(bs):.4f}, {np.nanmax(bs):.4f}], share below 1/2 {np.mean(bs < 0.5):.2f} (undefined {int(np.isnan(bs).sum())}) | "
                  f"lam* at b = 0.5 median {np.nanmedian(l5):.3f} [{np.nanmin(l5):.3f}, {np.nanmax(l5):.3f}] | at b = 0.2 median {np.nanmedian(l2):.3f} [{np.nanmin(l2):.3f}, {np.nanmax(l2):.3f}]")
    print("    checks and predictions (computed)")
    print(f"    B1 A8 static: D(b) = (1 - b) a - b h to {TOL:g} in every world: {all(o['b1'] for o in out.values())}")
    b2 = {n: out[('exchangeable', n)] for n in SIZES}
    ok2 = all(0.4 <= np.nanmedian(o["bstar"]) <= 0.6 and 0.3 <= np.mean(o["bstar"] < 0.5) <= 0.7 for o in b2.values())
    print(f"    B2 exchangeable rewards: median b* in [0.4, 0.6] and share of b* below 1/2 in [0.3, 0.7], at every size: {'holds' if ok2 else 'FAILS'}")
    print(f"    B3 A8 acting, uninformative correction: D(b) >= 0 for every b on the grid in every world: {all(o['b3'] for o in out.values())}")
    print(f"    B4 A8 acting, infallible operator (LAM = 1): D <= 0 at b in (0.2, 0.5, 0.8) in every world: {all(o['b4'] for o in out.values())}")
    print("    B5 (report) the harm family's b* against the ring's 1 / (1 + HARM_COST) = %.4f: " % (1 / (1 + HARM_COST))
          + ", ".join(f"n = {n}: median {np.nanmedian(out[('harm', n)]['bstar']):.4f}" for n in SIZES))
    return out


def main():
    print(f"Does the fix survive size? (AI_Safety/checks/scale.py): sizes {SIZES}, {N_MDP} random worlds per size, {K} successors per (state, action), "
          f"discount {DISC}, press {Q_PRESS}, pause {PAUSE_LEN}, drift grid {RHOS}")
    worlds = {n: [world(n, i) for i in range(N_MDP)] for n in SIZES}
    part_a(worlds); part_b(worlds)


if __name__ == "__main__":
    main()
