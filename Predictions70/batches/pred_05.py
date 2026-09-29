"""PRED70 batch P05: continual learning and optimisation (synthetic), rows P05-1..P05-5 of Predictions70/declared.py
(declared at commit 8397478, prompt-log entry 234, before any model existed). Q, the null, H0 and the forecast are
imported from declared.py and printed verbatim; the model details declared.py leaves open (dimensions, step sizes,
horizons, seeds) are chosen here and printed with each row.
  [1] P05-1 two-task linear regression, SGD + EWC: forgetting against path length and the old-probe endpoint (D6/H-T1)
  [2] P05-2 heavy-ball momentum on a two-task quadratic with the equanimity weight Omega = 1 (H-EQ)
  [3] P05-3 SGD with warm restarts on a noisy quadratic, restarts at antipodal cuts of the loss phase (A3)
  [4] P05-4 early stopping of a noisy linear model at the first antipodal cut of the validation-loss phase (A3)
  [5] P05-5 online mean estimation under drift: the A6 bounded mean against the Kalman filter (A6, q = 0.5)
Deterministic (fixed seeds, fixed grids), no data files, no network. Every verdict word is computed from the numbers (R15).
Run: uv run python Predictions70/batches/pred_05.py > Predictions70/batches/pred_05.txt
"""
import math
import os
import sys

import numpy as np

from crr.instrument.core import antipodal_cuts, intrinsic_phase, kl_gauss, path_length
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from declared import P as DECLARED  # noqa: E402

DECL = {p[0]: dict(id=p[0], batch=p[1], cls=p[2], system=p[3], ingredient=p[4], Q=p[5], null=p[6], H0=p[7], forecast=p[8])
        for p in DECLARED}
Q_GRID = (0.25, 0.5, 0.75)          # A6 sensitivity grid (q = 0.5 decides)


def _w(cond, yes, no):
    return yes if cond else no


def _src(D):
    return f"PRED70 {D['id']} (declared at 8397478; forecast {D['forecast']})"


def _qh(check):
    return "-> not computable" if check is None else _w(check, "-> Q holds", "-> Q fails")


# ---------------------------------------------------------------- [1] P05-1 path length vs old-probe endpoint (EWC)
SCHEDS = ("constant", "sawtooth", "cosine_restarts", "grad_noise", "loop")
LRS = (0.02, 0.05, 0.1)
LAMS = (0.0, 0.3, 1.0, 3.0)


def _mult(s, t):
    if s == "sawtooth":
        return 1.0 - 0.9 * ((t % 20) / 20.0)
    if s == "cosine_restarts":
        return 0.5 * (1 + math.cos(math.pi * (t % 25) / 25.0))
    return 1.0


def _t1_runs(wear=0.0, d=20, n=200, n_probe=200, T=100, bs=10, noise_sd=0.3):
    rng = np.random.default_rng(0)
    thA = rng.standard_normal(d); thB = thA + 1.5 * rng.standard_normal(d)
    sA = np.exp(rng.uniform(-0.7, 0.7, d)); sB = np.exp(rng.uniform(-0.7, 0.7, d))
    XA = rng.standard_normal((n, d)) * sA; yA = XA @ thA + noise_sd * rng.standard_normal(n)
    XB = rng.standard_normal((n, d)) * sB; yB = XB @ thB + noise_sd * rng.standard_normal(n)
    XAt = rng.standard_normal((n_probe, d)) * sA; yAt = XAt @ thA + noise_sd * rng.standard_normal(n_probe)
    probe_ind = rng.standard_normal((n_probe, d)) * sA; probe_new = rng.standard_normal((n_probe, d)) * sB
    th0 = np.linalg.lstsq(XA, yA, rcond=None)[0]
    FA = XA.T @ XA / n                                                         # Fisher of task A (Gaussian, unit variance)
    LA = lambda th: 0.5 * float(np.mean((XA @ th - yA) ** 2)); LAt = lambda th: 0.5 * float(np.mean((XAt @ th - yAt) ** 2))
    out = []
    for k in range(len(SCHEDS) * len(LRS) * len(LAMS)):
        s = SCHEDS[k % 5]; lr = LRS[(k // 5) % 3]; lam = LAMS[k // 15]
        rr = np.random.default_rng(1000 + k)
        th = th0.copy(); po, pi, pn = [XA @ th], [probe_ind @ th], [probe_new @ th]; wacc = 0.0
        for t in range(T):
            if s == "loop" and (t // 10) % 2 == 1:
                idx = rr.integers(0, n, bs); g = XA[idx].T @ (XA[idx] @ th - yA[idx]) / bs
            else:
                idx = rr.integers(0, n, bs); g = XB[idx].T @ (XB[idx] @ th - yB[idx]) / bs
            g = g + lam * FA @ (th - th0)                                      # EWC penalty (lam/2)(th - th0)' F_A (th - th0)
            if s == "grad_noise":
                g = g + rr.standard_normal(d)
            step = -lr * _mult(s, t) * g; th = th + step; wacc += float(np.linalg.norm(step))
            po.append(XA @ th); pi.append(probe_ind @ th); pn.append(probe_new @ th)
        if not np.all(np.isfinite(th)):
            raise RuntimeError(f"P05-1 run {k} diverged")
        a, b, c = path_length(po, kl=kl_gauss), path_length(pi, kl=kl_gauss), path_length(pn, kl=kl_gauss)
        out.append(dict(k=k, lr=lr, lam=lam, s=s, F=LA(th) - LA(th0) + wear * wacc, Fh=LAt(th) - LAt(th0) + wear * wacc,
                        C_old=a["C"], E_old=a["E"], S_old=a["S"], C_ind=b["C"], E_ind=b["E"], C_new=c["C"], E_new=c["E"]))
    return out


def _r2(pred, F, fit, cov=None):
    cols = [np.ones(int(fit.sum())), pred[fit]] + ([cov[fit]] if cov is not None else [])
    coef = np.linalg.lstsq(np.column_stack(cols), F[fit], rcond=None)[0]
    hc = [np.ones(int((~fit).sum())), pred[~fit]] + ([cov[~fit]] if cov is not None else [])
    Fh = F[~fit]; Fp = np.column_stack(hc) @ coef
    return 1.0 - float(np.sum((Fh - Fp) ** 2)) / float(np.sum((Fh - Fh.mean()) ** 2))


def r1():
    D = DECL["P05-1"]
    runs = _t1_runs(); runs_w = _t1_runs(wear=0.5)
    A = lambda rs, key: np.array([r[key] for r in rs])
    fit = np.array([r["k"] % 2 == 0 for r in runs]); F = A(runs, "F"); Fh = A(runs, "Fh"); lr = A(runs, "lr")
    R = {k: _r2(A(runs, k), F, fit) for k in ("C_old", "C_new", "E_old", "E_new")}
    crr = max(R["C_old"], R["C_new"]); kC = "C_old" if R["C_old"] >= R["C_new"] else "C_new"
    null = R["E_old"]
    Eo = A(runs, "E_old"); lemma_gap = float(np.max(np.abs(F - Eo)))
    domain = 1.0 - float(np.sum((F[~fit] - Eo[~fit]) ** 2)) / float(np.sum((F[~fit] - F[~fit].mean()) ** 2))   # lemma, no fit
    check = crr >= null + 0.05
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    P = {k: _r2(A(runs, k), F, fit, cov=lr) for k in ("C_old", "C_new", "E_old")}
    Rh = {k: _r2(A(runs, k), Fh, fit) for k in ("C_ind", "C_new", "E_ind", "E_new")}
    Fw = A(runs_w, "F"); Rw = {k: _r2(A(runs_w, k), Fw, fit) for k in ("C_old", "C_new", "E_old", "E_new")}
    pc_ok = max(Rw["C_old"], Rw["C_new"]) >= max(Rw["E_old"], Rw["E_new"]) + 0.05
    sneg = float(np.mean(A(runs, "S_old") < 0))
    Cr = A(runs, "C_old"); spread = float(Cr.max() / Cr.min())
    return make_row(D["cls"], D["system"] + " [model: linear regression d = 20, tasks A and B of 200 samples (S-H geometry, noise sd 0.3), start at the task-A least-squares optimum, 100 SGD steps on task B (batch 10) with the EWC penalty (lam/2)(theta - theta_A)' F_A (theta - theta_A); 60 runs = 5 schedules (constant, sawtooth, cosine restarts, gradient noise, loop back to A) x lr {0.02, 0.05, 0.1} x lam {0, 0.3, 1, 3}; forgetting F = rise of the task-A training loss (1/2 MSE); held-out R^2 of a linear fit, even runs fit, odd runs score]",
                    source=_src(D),
                    Q=D["Q"] + " (computed as: held-out R^2 of the better path predictor, C_old or C_new = sum sqrt(2 KL_step) on a probe, >= held-out R^2 of E_old + 0.05)",
                    ingredient=D["ingredient"] + ": path length C = sum_t sqrt(2 KL_t) (path_length, kl_gauss) against the endpoint E",
                    null=D["null"] + " (computed as: held-out R^2 of E_old = KL(p_0 || p_T) on the task-A inputs)",
                    domain=D["H0"] + " (computed as: the lemma's predictor F = E_old with no fitted coefficient, held-out R^2)",
                    numbers=(f"held-out R^2: C_old {R['C_old']:.4f}, C_new {R['C_new']:.4f}, E_old {R['E_old']:.6f}, E_new {R['E_new']:.4f}; "
                             f"lemma: max |F - E_old| over 60 runs = {lemma_gap:.2e}, no-fit R^2 {domain:.6f}; path length spread across runs {spread:.2f}x; S_old < 0 in {sneg:.0%} of runs; "
                             f"lr-controlled R^2 (lr as covariate): C_old {P['C_old']:.4f}, C_new {P['C_new']:.4f}, E_old {P['E_old']:.6f}; "
                             f"battery form (independent task-A probe, forgetting on a held-out task-A set): C_ind {Rh['C_ind']:.4f}, C_new {Rh['C_new']:.4f}, E_ind {Rh['E_ind']:.4f}, E_new {Rh['E_new']:.4f}; "
                             f"positive control (wear 0.5 x path added to F, S-H2 form): best path {max(Rw['C_old'], Rw['C_new']):.4f} against best endpoint {max(Rw['E_old'], Rw['E_new']):.4f} ({_w(pc_ok, 'path wins by >= 0.05: the instrument sees path dependence', 'VIOLATION: the instrument is blind to path dependence')})"),
                    tg=f"R^2 path ({kC}) {crr:.4f} vs null E_old {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the lemma's no-fit predictor gives R^2 {domain:.6f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"R^2 path {crr:.4f} >= R^2 E_old {null:.4f} + 0.05: {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=(f"on a convex learner with an EWC penalty the forgetting is the old-probe endpoint KL itself (largest gap {lemma_gap:.1e}), so the endpoint explains {null:.4f} of the held-out variance and the path "
                             f"{crr:.4f}; the penalty and the schedules change how the learner travels but not what the loss at the end depends on; the battery form "
                             f"(independent probe, held-out forgetting) {_w(max(Rh['C_ind'], Rh['C_new']) >= max(Rh['E_ind'], Rh['E_new']) + 0.05, 'reverses', 'keeps')} the ordering"),
                    weakness="one geometry (the S-H surrogate's), 60 runs; the old probe of the decisive reading is the task-A training inputs, where the SCOPE lemma is exact; the battery-form reading is printed beside it",
                    elegance="On a bowl-shaped learner, how much of the old task is lost depends only on where the learner ends, never on the road it took: a winding road and a straight one to the same place cost the same.",
                    child="If you walk away from your house, how far you are from home depends only on where you are standing now, not on how many loops you walked on the way.")


# ---------------------------------------------------------------- [2] P05-2 heavy-ball + equanimity weight
SMOOTH, WCAP, DEN_FLOOR = 0.9, 1e4, 1e-12            # the registered estimator (theory/checks/omega_sweeps.py)
OMEGA9 = (0.25, 0.35, 0.5, 0.71, 1.0, 1.41, 2.0, 2.83, 4.0)


def _eq_model(seed=0, d=5, mismatch=16.0):
    rng = np.random.default_rng(seed)
    H = np.diag(rng.uniform(0.5, 2.0, d)); F = mismatch * np.diag(rng.uniform(0.5, 2.0, d))
    a = rng.standard_normal(d); b = a + 1.5 * rng.standard_normal(d)
    return H, F, a, b


def _obj(H, F, a, b, th):
    th = np.atleast_2d(th)
    return 0.5 * np.einsum("gi,ij,gj->g", th - a, H, th - a) + 0.5 * np.einsum("gi,ij,gj->g", th - b, F, th - b)


def _hb_fixed(H, F, a, b, W, lr=0.01, beta=0.9, steps=4000, noise=0.0, seed=0):
    rng = np.random.default_rng(seed); W = np.asarray(W, float)[:, None]
    th = np.tile(b, (len(W), 1)); v = np.zeros_like(th); ok = np.ones(len(W), bool)
    for _ in range(steps):
        gp = (th - a) @ H + noise * rng.standard_normal(th.shape); gq = (th - b) @ F + noise * rng.standard_normal(th.shape)
        v = beta * v - lr * (gp + W * gq); th = th + v
        bad = ~np.all(np.isfinite(th), axis=1) | (np.linalg.norm(th, axis=1) > 1e6); ok &= ~bad; th[bad] = 0.0; v[bad] = 0.0
    return th, ok


def _hb_rule(H, F, a, b, omega, lr=0.01, beta=0.9, steps=4000, noise=0.0, seed=0):
    rng = np.random.default_rng(seed); th = b.copy(); v = np.zeros_like(th); ep = eq = None; wl = []
    for _ in range(steps):
        gp = H @ (th - a) + noise * rng.standard_normal(len(th)); gq = F @ (th - b) + noise * rng.standard_normal(len(th))
        ep = gp if ep is None else SMOOTH * ep + (1 - SMOOTH) * gp; eq = gq if eq is None else SMOOTH * eq + (1 - SMOOTH) * gq
        w = min(omega * np.linalg.norm(ep) / max(np.linalg.norm(eq), DEN_FLOOR), WCAP); wl.append(w)
        v = beta * v - lr * (gp + w * gq); th = th + v
        if not np.all(np.isfinite(th)) or np.linalg.norm(th) > 1e6:
            return th, wl, False
    return th, wl, True


def r2():
    D = DECL["P05-2"]
    H, F, a, b = _eq_model()
    W = np.logspace(-2, 2, 81)
    thW, okW = _hb_fixed(H, F, a, b, W)
    objW = np.where(okW, _obj(H, F, a, b, thW), np.inf); iW = int(np.argmin(objW)); w_best = float(W[iW]); null = float(objW[iW])
    th1, wl1, ok1 = _hb_rule(H, F, a, b, 1.0)
    crr = float(_obj(H, F, a, b, th1)[0]) if ok1 else float("inf")
    th_star = np.linalg.solve(H + F, H @ a + F @ b); domain = float(_obj(H, F, a, b, th_star)[0])
    grid = np.logspace(-4, 6, 2001)
    dist = [np.linalg.norm(np.linalg.solve(H + l * F, H @ a + l * F @ b) - th1) for l in grid]
    lam_eff = float(grid[int(np.argmin(dist))]); dmin = float(min(dist))
    check = rel(crr, null) <= TOL_G
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    lam_edge = (2 * (1 + 0.9) / 0.01 - np.diag(H).max()) / np.diag(F).max()
    diverged = int((~okW).sum())
    land = {}
    for om in OMEGA9:
        th, wl, ok = _hb_rule(H, F, a, b, om); land[om] = float(_obj(H, F, a, b, th)[0]) if ok else float("inf")
    om_best = min(land, key=land.get)
    # sensitivity: mini-batch noise sd 0.5 on both gradients, 5 seeds, the CLAUDE.md fixed grid
    fg = (0.25, 0.5, 1.0, 2.0, 4.0); nz = {}
    for s in range(5):
        th, ok = _hb_fixed(H, F, a, b, fg, noise=0.5, seed=s); o = _obj(H, F, a, b, th)
        for w_, oo, k_ in zip(fg, o, ok):
            nz.setdefault(w_, []).append(oo if k_ else np.inf)
        th, wl, ok = _hb_rule(H, F, a, b, 1.0, noise=0.5, seed=s); nz.setdefault("rule", []).append(float(_obj(H, F, a, b, th)[0]) if ok else np.inf)
    nzm = {k: float(np.mean(v)) for k, v in nz.items()}; nb = min(fg, key=lambda w_: nzm[w_])
    nz_ok = rel(nzm["rule"], nzm[nb]) <= TOL_G
    weight_step = abs(math.log2(lam_eff / w_best)) <= 1.0
    fp = []
    for l in np.logspace(-3, 3, 13):                                             # the rule's update on the Pareto curve at Omega = 1
        thl = np.linalg.solve(H + l * F, H @ a + l * F @ b); gp_, gq_ = H @ (thl - a), F @ (thl - b)
        fp.append(float(np.linalg.norm(gp_ + np.linalg.norm(gp_) / np.linalg.norm(gq_) * gq_) / np.linalg.norm(gp_)))
    fp_max = max(fp); fp_all = fp_max <= 1e-9
    return make_row(D["cls"], D["system"] + " [model: L_present = (theta - a)' H (theta - a)/2, past term the exact quadratic (Laplace) L_past = (theta - b)' F (theta - b)/2, d = 5, F 16x H in scale (the omega_sweeps geometry, seed 0); heavy-ball v <- 0.9 v - 0.01 g, theta <- theta + v, 4000 steps from the past optimum b; exact gradients; the rule w = Omega |g_present|/|g_past| with the registered estimator (EMA 0.9 of the gradient vectors, cap 1e4, floor 1e-12); metric: total loss L_present + L_past at the end]",
                    source=_src(D),
                    Q=D["Q"] + " (computed as: the total loss at Omega = 1 within one resolvable step, TOL_G = 1 % relative, of the best fixed weight's; the fixed weights are 81 log-spaced values in [0.01, 100])",
                    ingredient=D["ingredient"] + ": g = g_present + w g_past, w = Omega |g_present| / |g_past|, Omega = 1",
                    null=D["null"] + " (computed as: the lowest total loss over the 81 fixed weights under the same heavy-ball run)",
                    domain=D["H0"] + " (computed as: the closed-form minimum of L_present + L_past, the Laplace weight 1)",
                    numbers=(f"total loss: Omega = 1 {crr:.6f} (median w {np.median(wl1):.4g}; nearest fixed-weight equilibrium lambda_eff = {lam_eff:.4g}, distance {dmin:.1e}); best fixed weight w = {w_best:.4g}: {null:.6f}; "
                             f"closed-form Laplace minimum {domain:.6f}; fixed weights diverged: {diverged} of {len(W)} (heavy-ball edge lambda* = {lam_edge:.3f}); "
                             f"Omega landscape: " + ", ".join(f"{om:g}: {land[om]:.4f}" for om in OMEGA9) + f" (best Omega {om_best:g}); "
                             f"|update| / |g_present| at Omega = 1 on 13 points of the Pareto curve, lambda in [1e-3, 1e3]: max {fp_max:.1e}; "
                             f"weight reading: lambda_eff / best w = {lam_eff / w_best:.3f} ({_w(weight_step, 'within', 'outside')} one step of the doubling grid); "
                             f"noise sd 0.5, 5 seeds, mean total loss: rule {nzm['rule']:.4f}, fixed " + ", ".join(f"{w_:g}: {nzm[w_]:.4f}" for w_ in fg) + f" (rule {_w(nz_ok, 'within', 'outside')} 1 % of the best fixed {nb:g})"),
                    tg=f"total loss Omega = 1 {crr:.6f} vs best fixed {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')} (relative {rel(crr, null):.4f})",
                    tn=f"the Laplace minimum {domain:.6f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"Omega = 1 within one step (1 %) of the best fixed weight: {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=(f"under heavy-ball momentum and exact gradients the rule at Omega = 1 {_w(check, 'lands', 'does not land')} on the best fixed weight's loss "
                             f"(it stops on the Pareto curve at lambda_eff = {lam_eff:.4g}, where the best fixed weight is {w_best:.4g}); "
                             f"{_w(fp_all, 'every point of that curve is a fixed point of the rule at Omega = 1 (largest update ' + f'{fp_max:.1e}' + '), so where it stops is set by the start and the dynamics, not by the ratio', 'the curve is not a set of fixed points of the rule (largest update ' + f'{fp_max:.1e}' + ')')}; with mini-batch noise the rule is {_w(nz_ok, 'within', 'outside')} 1 % of the best fixed weight"),
                    weakness="one quadratic geometry (the omega_sweeps model), one momentum and step size; 'a step' is read as the harness's 1 % on the total loss, the weight reading is printed beside it",
                    elegance="", child="")


# ---------------------------------------------------------------- [3] P05-3 SGDR restarts at antipodal cuts
NQ_D, NQ_T, ETA_MAX, ETA_MIN = 10, 2000, 1.0, 0.0
NQ_H = np.logspace(-2, 0, NQ_D)


def _sgdr(mode, P, seed, cuts=None):
    rng = np.random.default_rng(seed); th = np.full(NQ_D, 10.0); L = np.empty(NQ_T); last = 0; nres = 0
    cutset = set() if cuts is None else set(int(c) for c in cuts)
    for t in range(NQ_T):
        if (mode == "fixed" and t - last >= P) or (mode == "given" and t in cutset and t > 0):
            last = t; nres += 1
        tau = t - last
        eta = ETA_MIN + (ETA_MAX - ETA_MIN) * 0.5 * (1 + math.cos(math.pi * min(tau, P) / P))
        th = th - eta * (NQ_H * th + np.sqrt(NQ_H) * rng.standard_normal(NQ_D))
        L[t] = 0.5 * float(np.sum(NQ_H * th * th))
        if mode == "cut" and t >= 2:
            ph = intrinsic_phase(L[:t + 1])
            if ph[-1] - ph[last] >= math.pi:           # the loss phase has advanced half a turn since the last restart
                last = t + 1; nres += 1
    return L[-1], nres, L


def r3():
    D = DECL["P05-3"]
    seeds = range(10); PS = (200, 250, 400, 500, 1000)
    fixed = {P: float(np.mean([_sgdr("fixed", P, s)[0] for s in seeds])) for P in PS}
    noR = float(np.mean([_sgdr("fixed", NQ_T, s)[0] for s in seeds]))
    Pb = min(PS, key=fixed.get); null = fixed[Pb]
    cr = [_sgdr("cut", Pb, s) for s in seeds]
    crr = float(np.mean([c[0] for c in cr])); nres = float(np.mean([c[1] for c in cr]))
    # second reading: two-pass, restarts at antipodal_cuts of the full-horizon loss phase of the best fixed-period run
    tp, tpn = [], []
    for s in seeds:
        Lref = _sgdr("fixed", Pb, s)[2]; cuts = antipodal_cuts(intrinsic_phase(Lref))
        r = _sgdr("given", Pb, s, cuts=cuts); tp.append(r[0]); tpn.append(r[1])
    two = float(np.mean(tp))
    check = crr < null; check2 = two < null
    internal = check != check2
    out = outcome(crr=crr, null=null, domain=None, check=check, internal=internal)
    return make_row(D["cls"], D["system"] + f" [model: L = sum_i h_i theta_i^2 / 2, d = {NQ_D}, h log-spaced in [0.01, 1], gradient noise sqrt(h_i) N(0, 1), theta_0 = 10; {NQ_T} SGD steps; within a cycle the step size anneals by a cosine from {ETA_MAX:g} to {ETA_MIN:g} over P steps and is held at {ETA_MIN:g} after P; 10 seeds, common random numbers across arms; final loss = the noise-free L(theta_T), seed mean]",
                    source=_src(D),
                    Q=D["Q"] + " (computed as: restart when the analytic-signal phase of the loss trace so far, intrinsic_phase, has advanced by pi since the last restart; the cosine keeps the best fixed period as its nominal length; lower seed-mean final loss than the best fixed period)",
                    ingredient=D["ingredient"] + ": the restart is the cut, fired at the oriented half-turn of the loss phase",
                    null=D["null"] + f" (computed as: the best of P in {{{', '.join(str(p) for p in PS)}}} by seed-mean final loss)",
                    domain=D["H0"],
                    numbers=(f"seed-mean final loss: antipodal restarts {crr:.5f} (mean {nres:.1f} restarts in {NQ_T} steps); fixed periods " + ", ".join(f"P = {p}: {fixed[p]:.5f}" for p in PS)
                             + f" (best P = {Pb}); no restart (one anneal over the horizon, reported, not a restart schedule): {noR:.5f}; "
                             f"second reading (two-pass: restarts at antipodal_cuts of the best fixed run's full loss trace): {two:.5f} (mean {np.mean(tpn):.1f} restarts)"),
                    tg=f"final loss {crr:.5f} vs null {null:.5f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no theorem cited",
                    tc=f"antipodal restarts lower than the best fixed period: online {_w(check, 'holds', 'fails')}, two-pass {_w(check2, 'holds', 'fails')} ({_w(internal, 'the readings disagree', 'the readings agree')}) {_qh(check)}",
                    out=out,
                    reading=(f"on a noisy quadratic the final loss is set by how far the step size has annealed when the budget ends; the loss phase advances by half a turn "
                             f"about every {NQ_T / max(nres, 1):.0f} steps (the end-of-record analytic phase of a falling curve reaches pi quickly), so the antipodal learner "
                             f"{_w(check, 'ends lower', 'ends higher')} than the best fixed period ({crr:.5f} against {null:.5f}); the two-pass reading {_w(check2, 'ends lower', 'ends higher')} ({two:.5f})"),
                    weakness="the online phase is the analytic signal of the trace so far, whose last sample carries the Hilbert edge effect; the two-pass reading avoids it but uses the future; the loss read is the noise-free loss",
                    elegance="", child="")


# ---------------------------------------------------------------- [4] P05-4 early stopping at the first antipodal cut
def _es_seed(seed, n=50, d=40, nv=50, nt=2000, sd=1.0, lr=0.01, T=3000, bs=10):
    rng = np.random.default_rng(seed); w = 2.0 * rng.standard_normal(d) / math.sqrt(d)
    X = rng.standard_normal((n, d)); y = X @ w + sd * rng.standard_normal(n)
    Xv = rng.standard_normal((nv, d)); yv = Xv @ w + sd * rng.standard_normal(nv)
    Xt = rng.standard_normal((nt, d)); yt = Xt @ w + sd * rng.standard_normal(nt)
    th = np.zeros(d); TH = np.empty((T, d))
    for t in range(T):
        TH[t] = th; idx = rng.integers(0, n, bs); th = th - lr * X[idx].T @ (X[idx] @ th - y[idx]) / bs
    val = 0.5 * np.mean((Xv @ TH.T - yv[:, None]) ** 2, axis=0); test = 0.5 * np.mean((Xt @ TH.T - yt[:, None]) ** 2, axis=0)
    return val, test


def _patience(val, p):
    best = 0
    for t in range(1, len(val)):
        if val[t] < val[best]:
            best = t
        if t - best >= p:
            break
    return best


def _first_cut_offline(val):
    c = antipodal_cuts(intrinsic_phase(val))
    return (int(c[1]), True) if len(c) > 1 else (len(val) - 1, False)


def _first_cut_online(val):
    for t in range(1, len(val)):
        ph = intrinsic_phase(val[:t + 1])
        if ph[-1] - ph[0] >= math.pi:
            return t
    return len(val) - 1


def r4():
    D = DECL["P05-4"]
    seeds = range(20); PAT = (5, 10, 20, 50, 100); P0 = 10
    off, on, pat, found, tcut, ton, oracle = [], [], {p: [] for p in PAT}, 0, [], [], []
    hz = {1500: [], 6000: []}
    for s in seeds:
        val, test = _es_seed(s)
        tc, f = _first_cut_offline(val); found += int(f); off.append(test[tc]); tcut.append(tc)
        to = _first_cut_online(val); on.append(test[to]); ton.append(to)
        for p in PAT:
            pat[p].append(test[_patience(val, p)])
        oracle.append(float(test.min()))
        for Th in hz:
            v2, t2 = _es_seed(s, T=Th); hz[Th].append(t2[_first_cut_offline(v2)[0]])
    crr = float(np.mean(off)); null = float(np.mean(pat[P0])); onl = float(np.mean(on))
    pm = {p: float(np.mean(v)) for p, v in pat.items()}
    beats = lambda x, y: x < y and rel(x, y) > TOL_G
    check = beats(crr, null); check2 = beats(onl, null)
    internal = check != check2
    flips = [p for p in PAT if beats(crr, pm[p]) != check]
    hflip = [Th for Th in hz if beats(float(np.mean(hz[Th])), null) != check]
    out = outcome(crr=crr, null=null, domain=None, check=check, internal=internal)
    return make_row(D["cls"], D["system"] + " [model: linear regression d = 40, 50 training, 50 validation and 2000 test samples, label noise sd 1, true weights N(0, 4/d); SGD from zero, batch 10, step 0.01, horizon 3000 steps; test loss = 1/2 MSE at the returned step; 20 seeds, seed mean]",
                    source=_src(D),
                    Q=D["Q"] + " (computed as: the first antipodal cut after the start, antipodal_cuts on intrinsic_phase of the validation-loss trace over the horizon; the seed-mean test loss lower than patience's by more than TOL_G = 1 %)",
                    ingredient=D["ingredient"] + ": stop at the first oriented half-turn of the validation-loss phase",
                    null=D["null"] + f" (computed as: patience {P0}, the checkpoint with the lowest validation loss restored)",
                    domain=D["H0"],
                    numbers=(f"seed-mean test loss: first antipodal cut {crr:.5f} (cut found within the horizon in {found}/20 seeds; median cut step {int(np.median(tcut))}); "
                             f"patience " + ", ".join(f"{p}: {pm[p]:.5f}" for p in PAT) + f"; oracle (lowest test loss on the path) {np.mean(oracle):.5f}; "
                             f"second reading (online: the phase of the trace so far, stop at its first half-turn): {onl:.5f} (median stop step {int(np.median(ton))}); "
                             f"horizon sensitivity of the offline cut: 1500 steps {np.mean(hz[1500]):.5f}, 3000 steps {crr:.5f}, 6000 steps {np.mean(hz[6000]):.5f}"),
                    tg=f"test loss {crr:.5f} vs null {null:.5f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no theorem cited",
                    tc=(f"the cut beats patience {P0} by more than 1 %: offline {_w(check, 'holds', 'fails')}, online {_w(check2, 'holds', 'fails')} ({_w(internal, 'the readings disagree', 'the readings agree')}); "
                        f"the verdict {_w(flips, 'flips against patience ' + ', '.join(str(p) for p in flips), 'is the same against every patience on the grid')} "
                        f"and {_w(hflip, 'flips at horizon ' + ', '.join(str(h) for h in hflip), 'holds at every horizon')} {_qh(check)}"),
                    out=out,
                    reading=(f"the validation loss of a noisy linear model falls and then rises as the model fits noise; the first half-turn of its phase lands at step {int(np.median(tcut))} (median), "
                             f"and the test loss there is {crr:.5f} against {null:.5f} for patience {P0}; online the analytic phase of a falling trace reaches pi within a few steps "
                             f"(median {int(np.median(ton))}), so the causal cut stops almost at once ({onl:.5f})"),
                    weakness="one model size and noise level; the offline cut depends on the horizon (printed); patience restores the best validation checkpoint, which the cut does not",
                    elegance="", child="")


# ---------------------------------------------------------------- [5] P05-5 A6 bounded mean against the Kalman filter
def _ema_mse(a, sw2, sv2):
    return ((1 - a) ** 2 * sw2 + a ** 2 * sv2) / (1 - (1 - a) ** 2)


def _kalman_ss(sw2, sv2):
    Pp = 0.5 * (sw2 + math.sqrt(sw2 * sw2 + 4 * sw2 * sv2))                   # prior variance: Pp^2 - sw2 Pp - sw2 sv2 = 0
    K = Pp / (Pp + sv2)
    return K, (1 - K) * Pp


def r5():
    D = DECL["P05-5"]
    sw, sv, T, burn = 1.0, 1.0, 200000, 1000
    rng = np.random.default_rng(0)
    mu = np.cumsum(sw * rng.standard_normal(T)); y = mu + sv * rng.standard_normal(T)
    def a6(q):
        M = np.empty(T); S = 0.0; Wt = 0.0
        for t in range(T):
            S = y[t] + q * S; Wt = 1.0 + q * Wt; M[t] = S / Wt                 # normalised geometric weights q^k (bounded mean)
        return float(np.mean((M[burn:] - mu[burn:]) ** 2))
    m = 0.0; Pv = 0.0; E = np.empty(T)
    for t in range(T):
        Pp = Pv + sw * sw; K = Pp / (Pp + sv * sv); m = m + K * (y[t] - m); Pv = (1 - K) * Pp; E[t] = m
    kal = float(np.mean((E[burn:] - mu[burn:]) ** 2))
    Kss, Pss = _kalman_ss(sw * sw, sv * sv)
    mq = {q: a6(q) for q in Q_GRID}
    crr, null, domain = mq[0.5], kal, Pss
    check = rel(crr, null) <= TOL_G
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    cf = _ema_mse(0.5, sw * sw, sv * sv)
    ratios = (0.01, 0.1, 0.5, 1.0, 10.0)
    band = [r_ for r_ in ratios if rel(_ema_mse(0.5, r_, 1.0), _kalman_ss(r_, 1.0)[1]) <= TOL_G]
    return make_row(D["cls"], D["system"] + f" [model: random-walk mean mu_t = mu_(t-1) + N(0, {sw:g}^2), observation y_t = mu_t + N(0, {sv:g}^2) (unit variances), mu_0 = 0 known; {T} steps, seed 0, error = MSE of the estimate of mu_t after {burn} steps]",
                    source=_src(D),
                    Q=D["Q"] + " (computed as: relative difference of the two mean squared errors <= TOL_G)",
                    ingredient=D["ingredient"] + ": the bounded Frechet (Euclidean: weighted) mean of the observations with P3 weights q^k over age k, normalised over the available history, q = 0.5",
                    null=D["null"] + " (computed as: the time-varying Kalman filter with the known variances)",
                    domain=D["H0"] + " (computed as: the closed-form steady-state posterior variance)",
                    numbers=(f"MSE: A6 q = 0.5 {crr:.5f} (closed form for an EMA of gain 1 - q = 0.5: {cf:.5f}), Kalman {kal:.5f}, steady-state Kalman {Pss:.5f} (gain K = {Kss:.5f}); "
                             f"q grid: " + ", ".join(f"q = {q:g}: {mq[q]:.5f} ({rel(mq[q], kal):.4f} from Kalman)" for q in Q_GRID)
                             + f"; closed form over the drift-to-noise ratio sw^2/sv^2 in {{{', '.join(f'{r_:g}' for r_ in ratios)}}}: A6 q = 0.5 within 1 % of Kalman at {_w(band, ', '.join(f'{r_:g}' for r_ in band), 'none')}"),
                    tg=f"MSE {crr:.5f} vs Kalman {null:.5f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')} (relative {rel(crr, null):.4f})",
                    tn=f"the steady-state Kalman variance {domain:.5f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"A6 within 1 % of Kalman: {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=(f"A6 with q = 0.5 is an exponential moving average of gain 0.5, and the steady-state Kalman filter is an exponential moving average of gain {Kss:.4f}; "
                             f"they coincide only when the drift-to-noise ratio makes the Kalman gain 0.5 (sw^2/sv^2 = 0.5), so at unit variances the A6 tracker is "
                             f"{_w(check, 'within', 'outside')} 1 % ({rel(crr, null):.4f}); a fixed q is a fixed gain, and the Kalman filter sets its gain from the variances A6 does not use"),
                    weakness="the variances are not named in declared.py; unit variances were chosen and decide the verdict (the closed-form band where Q would hold is printed); the domain value is the Kalman variance, so T-N repeats T-G here",
                    elegance="A memory that fades by a fixed half each step is a fixed way of listening; the best way of listening depends on how fast the world moves compared with how blurry your view of it is, and a fixed memory is best for only one such world.",
                    child="If you guess where a wandering friend is by mixing what you see now with what you guessed before, how much to trust the new look depends on how fast your friend moves and how foggy it is. One fixed mix is only best for one kind of day.")


def main():
    return run_batch("PRED70 batch P05: continual learning and optimisation (prompt-log entry 234; Predictions70/DECLARATION.md, declared at 8397478)",
                     [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
