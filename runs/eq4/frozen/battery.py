"""Surrogate battery: synthetic signals with NO CRR content.

Every hypothesis must FAIL on the surrogates theory/CRR.md names for it before
it may enter a pre-registration (CLAUDE.md rule R4). Generators are
deterministic given `seed`. Each returns (x, events, meta) where `events` are
the sample indices of the signal's own boundary events (or None).
"""
from __future__ import annotations

from functools import partial

import numpy as np
from scipy.integrate import solve_ivp



# ---------------------------------------------------------------- EQ-B present bound (prompt-log entry 74; theory/checks/omega_reprocessed.py [4])
EQB_KAPPA = 2.0; EQB_N_HIST = 50; EQB_N_MIN = 10


def _eqb_clip(g_p, hist, kappa=EQB_KAPPA, n_hist=EQB_N_HIST, n_min=EQB_N_MIN):
    """EQ-B: clip the present gradient to kappa x the LARGEST KEPT length among the last n_hist present batches (no clip
    until n_min lengths are known). The history holds the kept (post-clip) lengths, so a run of extreme batches can
    raise the bound by at most a factor kappa per batch (a geometric leak, bounded by kappa^run), while a legitimate
    regime change catches up at the same rate. The reference is the window MAXIMUM, not a median: on a softmax stream
    the median present-gradient length collapses toward zero as the task is learned (the information is in the tail),
    and a median-based bound clips the informative batches (AGENT_LOG 63). The caller resets `hist` at every task boundary."""
    n = float(np.linalg.norm(g_p))
    tau = kappa * float(np.max(hist[-n_hist:])) if len(hist) >= n_min else np.inf
    if n > tau:
        hist.append(tau); return g_p * (tau / n)
    hist.append(n); return g_p

def _cycles(periods, shape, amps=None):
    amps = np.ones(len(periods)) if amps is None else amps
    xs, ev, pos = [], [0], 0
    for p, a in zip(periods, amps):
        u = np.linspace(0, 2 * np.pi, int(p), endpoint=False)
        xs.append(a * shape(u)); pos += int(p); ev.append(pos)
    return np.concatenate(xs), np.asarray(ev[:-1])


def S_A_sine(n=60, period=100, seed=0):
    return _cycles(np.full(n, period), np.sin) + ({"name": "S-A sine"},)


def S_A1_fm_sine(n=60, seed=0, jitter=0.2):
    rng = np.random.default_rng(seed)
    p = rng.uniform(100 * (1 - jitter), 100 * (1 + jitter), n)
    return _cycles(p, np.sin) + ({"name": "S-A' FM sine (constant amplitude)"},)


def S_A2_am_sine(n=60, seed=0, jitter=0.3):
    rng = np.random.default_rng(seed)
    a = rng.uniform(1 - jitter, 1 + jitter, n)
    return _cycles(np.full(n, 100), np.sin, a) + ({"name": "S-A'' AM sine (constant period)"},)


def S_A3_amfm_sine(n=60, seed=0):
    rng = np.random.default_rng(seed)
    p = rng.uniform(80, 120, n); a = rng.uniform(0.7, 1.3, n)
    return _cycles(p, np.sin, a) + ({"name": "S-A''' AM+FM sine"},)


def S_B_sine_bump(n=60, seed=0, bump=0.15):
    rng = np.random.default_rng(seed)
    p = rng.uniform(90, 110, n); a = rng.uniform(0.9, 1.1, n)
    def shape(u):  # bump on the descent
        return np.sin(u) + bump * np.exp(-((u - 4.2) ** 2) / 0.08)
    return _cycles(p, shape, a) + ({"name": "S-B sine + dicrotic bump"},)


def S_C_lobed_ramp(n=60, seed=0, lam=1.0):
    rng = np.random.default_rng(seed)
    p = rng.uniform(90, 110, n); a = rng.uniform(0.9, 1.1, n)
    def shape(u):
        ramp = u / (2 * np.pi)
        lobes = lam * (0.3 * np.sin(np.clip(u * 3, 0, np.pi)) ** 2 + 0.2 * np.sin(np.clip((u - 2) * 3, 0, np.pi)) ** 2)
        return ramp + lobes
    return _cycles(p, shape, a) + ({"name": f"S-C lobed ramp (lambda={lam})"},)


def S_D_noisy_sine(n=60, seed=0, rho=20.0):
    rng = np.random.default_rng(seed)
    x, ev = _cycles(np.full(n, 100), np.sin)
    return x + rng.standard_normal(len(x)) * (2.0 / rho), ev, {"name": f"S-D sine + white noise (rho~{rho})"}


def S_E_asymmetric(n=60, seed=0):
    rng = np.random.default_rng(seed)
    p = rng.uniform(90, 110, n); a = rng.uniform(0.9, 1.1, n)
    return _cycles(p, lambda u: np.sin(u) + 1.2 * np.sin(2 * u) + 0.6 * np.sin(3 * u), a) + ({"name": "S-E asymmetric multi-harmonic"},)


def S_F_vanderpol(mu=5.0, T=400.0, dt=0.05, seed=0):
    f = lambda t, y: [y[1], mu * (1 - y[0] ** 2) * y[1] - y[0]]
    # explicit RK45 on a fixed eval grid: byte-identical across reruns on the
    # locked scipy (R9)
    sol = solve_ivp(f, (0, T), [2.0, 0.0], t_eval=np.arange(0, T, dt), method="RK45",
                    rtol=1e-8, atol=1e-10)
    x = sol.y[0][int(50 / dt):]
    # events: upward zero crossings
    ev = np.where((x[:-1] < 0) & (x[1:] >= 0))[0]
    return x, ev, {"name": f"S-F van der Pol mu={mu}"}


def S_F_roessler(T=1200.0, dt=0.05, seed=0):
    """Rössler attractor (a=0.2, b=0.2, c=5.7). Events: upward zero crossings
    of x. Chaotic: no control verdict is assigned to this row (CLAUDE.md §3.2
    lists it for coverage, not as a control)."""
    def f(t, y):
        return [-y[1] - y[2], y[0] + 0.2 * y[1], 0.2 + y[2] * (y[0] - 5.7)]
    # explicit RK45 on a fixed eval grid: byte-identical across reruns on the
    # locked scipy (R9)
    sol = solve_ivp(f, (0, T), [1.0, 0.0, 0.0], t_eval=np.arange(0, T, dt), method="RK45",
                    rtol=1e-8, atol=1e-10)
    x = sol.y[0][int(100 / dt):]
    ev = np.where((x[:-1] < 0) & (x[1:] >= 0))[0]
    return x, ev, {"name": "S-F Rossler (a=0.2, b=0.2, c=5.7)"}


def S_F_duffing(T=1000.0, dt=0.05, seed=0):
    """Forced double-well Duffing oscillator x'' + 0.15 x' - x + x^3 = 0.3 cos(t)
    (standard chaotic parameters: delta=0.15, gamma=0.3, omega=1). Events:
    upward zero crossings of x (interwell hops). Chaotic: no control verdict
    is assigned to this row (CLAUDE.md §3.2 lists it for coverage)."""
    def f(t, y):
        return [y[1], 0.3 * np.cos(t) - 0.15 * y[1] + y[0] - y[0] ** 3]
    # explicit RK45 on a fixed eval grid: byte-identical across reruns on the
    # locked scipy (R9)
    sol = solve_ivp(f, (0, T), [1.0, 0.0], t_eval=np.arange(0, T, dt), method="RK45",
                    rtol=1e-8, atol=1e-10)
    x = sol.y[0][int(100 / dt):]
    ev = np.where((x[:-1] < 0) & (x[1:] >= 0))[0]
    return x, ev, {"name": "S-F forced Duffing (delta=0.15, gamma=0.3, omega=1)"}


def S_G_relaxation(n=60, seed=0, thresh_cv=0.15):
    """Integrate-and-fire with clock-regular firing by construction: the threshold
    is drawn per cycle but the *time* to reach it is fixed; amplitude varies."""
    rng = np.random.default_rng(seed)
    T = 100
    xs, ev, pos = [], [0], 0
    for _ in range(n):
        thr = rng.normal(1, thresh_cv)
        ramp = np.linspace(0, thr, T, endpoint=False)
        xs.append(ramp); pos += T; ev.append(pos)
    return np.concatenate(xs), np.asarray(ev[:-1]), {"name": "S-G relaxation osc. (clock-regular, amplitude-variable)"}


def S_G2_relaxation_arc_regular(n=60, seed=0, rate_cv=0.15):
    """Fixed threshold, variable charging rate: arc constant, clock variable."""
    rng = np.random.default_rng(seed)
    xs, ev, pos = [], [0], 0
    for _ in range(n):
        T = int(100 * rng.normal(1, rate_cv))
        xs.append(np.linspace(0, 1.0, T, endpoint=False)); pos += T; ev.append(pos)
    return np.concatenate(xs), np.asarray(ev[:-1]), {"name": "S-G2 relaxation osc. (arc-regular by construction)"}


# ---------------------------------------------------------------- learner surrogates (H-T1, H-EQ)
# These do not return a signal; they return a list of fine-tuning RUNS. Each run
# is a dict with per-step predictions on a fixed old-task probe and a fixed
# new-task probe, plus the forgetting F it produced. The gate scores whether
# path length predicts F better than endpoint displacement (CLAUDE.md §5).

LEARNER_SCHEDULES = ("constant", "sawtooth", "cosine_restarts", "grad_noise", "loop")


def _lr_multiplier(schedule: str, t: int) -> float:
    if schedule == "constant" or schedule == "grad_noise" or schedule == "loop":
        return 1.0
    if schedule == "sawtooth":  # linear decay 1 -> 0.1 every 20 steps
        return 1.0 - 0.9 * ((t % 20) / 20.0)
    if schedule == "cosine_restarts":  # cosine 1 -> 0 every 25 steps
        return 0.5 * (1 + np.cos(np.pi * (t % 25) / 25.0))
    raise ValueError(schedule)


def _linear_finetune_runs(seed, n_runs, wear, d=20, n_train=200, n_probe=200, T=100,
                          lrs=(0.02, 0.05, 0.1), noise_sd=0.3, wear_gamma=0.0):
    """Linear model, squared loss (convex). Trained to the task-A optimum, then
    fine-tuned on task B under a schedule. Predictive family: N(x.theta, 1).

    wear=False (S-H): forgetting F = L_A(theta_T) - L_A(theta_0) on a held-out
        task-A set — a function of the endpoint only (SCOPE.md lemma).
    wear=True  (S-H2): F additionally accumulates gamma * ||delta theta|| per step —
        path-dependent damage by construction (the instrument must see it).
    """
    rng = np.random.default_rng(seed)
    thA = rng.standard_normal(d); thB = thA + 1.5 * rng.standard_normal(d)
    # tasks have different (anisotropic) input covariances so that endpoint
    # displacement on the NEW probe is not trivially the same number as on the OLD one
    sA = np.exp(rng.uniform(-0.7, 0.7, d)); sB = np.exp(rng.uniform(-0.7, 0.7, d))  # lr grid is stable for these
    XA = rng.standard_normal((n_train, d)) * sA; yA = XA @ thA + noise_sd * rng.standard_normal(n_train)
    XB = rng.standard_normal((n_train, d)) * sB; yB = XB @ thB + noise_sd * rng.standard_normal(n_train)
    XA_test = rng.standard_normal((n_probe, d)) * sA; yA_test = XA_test @ thA + noise_sd * rng.standard_normal(n_probe)
    probe_old = rng.standard_normal((n_probe, d)) * sA; probe_new = rng.standard_normal((n_probe, d)) * sB
    th0 = np.linalg.lstsq(XA, yA, rcond=None)[0]
    LA0 = np.mean((XA_test @ th0 - yA_test) ** 2)
    runs = []
    k = 0
    while len(runs) < n_runs:
        schedule = LEARNER_SCHEDULES[k % len(LEARNER_SCHEDULES)]
        lr = lrs[(k // len(LEARNER_SCHEDULES)) % len(lrs)]
        run_rng = np.random.default_rng(seed * 1000 + k)
        th = th0.copy(); pred_old = [probe_old @ th]; pred_new = [probe_new @ th]; wear_acc = 0.0
        for t in range(T):
            if schedule == "loop" and (t // 10) % 2 == 1:  # every other block trains back toward task A
                g = 2 * XA.T @ (XA @ th - yA) / n_train
            else:
                g = 2 * XB.T @ (XB @ th - yB) / n_train
            if schedule == "grad_noise":
                g = g + 1.0 * run_rng.standard_normal(d)
            step = -lr * _lr_multiplier(schedule, t) * g
            th = th + step; wear_acc += np.linalg.norm(step)
            pred_old.append(probe_old @ th); pred_new.append(probe_new @ th)
        if not np.all(np.isfinite(th)):
            raise RuntimeError(f"surrogate run diverged (schedule={schedule}, lr={lr}); lr grid must be stable")
        F = float(np.mean((XA_test @ th - yA_test) ** 2) - LA0)
        if wear:
            F += wear_gamma * wear_acc
        runs.append(dict(pred_old=pred_old, pred_new=pred_new, F=F, schedule=schedule, lr=lr, seed=k))
        k += 1
    return runs


def S_H_convex_learner(n_runs=60, seed=0):
    """S-H: convex learner. Forgetting is a function of the endpoint alone;
    H-T1 and H-EQ MUST FAIL here (theory/CRR.md §5, §3)."""
    return _linear_finetune_runs(seed, n_runs, wear=False), None, {"name": "S-H convex learner (endpoint-sufficient)"}


def S_H2_wear_learner(n_runs=60, seed=0, gamma=0.5):
    """S-H2: same convex learner with path-dependent damage added to forgetting
    by construction. Positive control: H-T1 MUST PASS or the instrument is blind."""
    return _linear_finetune_runs(seed, n_runs, wear=True, wear_gamma=gamma), None, {"name": "S-H2 wear learner (path-dependent by construction)"}


LEARNER_BATTERY = [S_H_convex_learner, S_H2_wear_learner]


# ---------------------------------------------------------------- replay-weighting surrogates (H-EQ)
# Convex learner with a replay buffer. The update is g = g_present_mean + w * g_past_mean,
# exactly the form of the equanimity rule (theory/CRR.md [H-EQ]) and of ER-sum (w = 1).
# The gate asks whether the ADAPTIVE w (Omega * ||g_present|| / ||g_past||) beats the best
# FIXED w, including the constant it reduces to (its own median w). Returns a runner.

def _replay_learner(scales, method, value, seed, d=32, n_task=2000, n_test=500, bs=10, r=0.2,
                    buf=200, lr=0.01, smooth=0.9, metric="euclid", wcap=20.0, noise_sd=0.3, kappa=EQB_KAPPA):
    """One online pass over K tasks (linear model, squared loss). Task k has LABEL scale
    scales[k]: y = scale * (x.theta_k + noise). Gradient magnitude scales with it, the Hessian
    (2 X'X) does not, so every arm is stable at the same lr. Returns normalised held-out MSE."""
    rng = np.random.default_rng(seed)
    K = len(scales)
    tasks = []
    for k, sc in enumerate(scales):
        th = rng.standard_normal(d)
        X = rng.standard_normal((n_task, d)); y = sc * (X @ th + noise_sd * rng.standard_normal(n_task))
        Xt = rng.standard_normal((n_test, d)); yt = sc * (Xt @ th + noise_sd * rng.standard_normal(n_test))
        tasks.append((X, y, Xt, yt))
    theta = np.zeros(d)
    bufX = np.zeros((buf, d)); bufy = np.zeros(buf); nb = 0; seen = 0
    ev_p = ev_q = None; Fd = np.full(d, 1e-3); wlog = []
    rb = max(1, int(round(r * bs)))
    for k in range(K):
        X, y, _, _ = tasks[k]
        perm = rng.permutation(n_task); hist = []
        for i in range(0, n_task, bs):
            idx = perm[i:i + bs]; xb, yb = X[idx], y[idx]
            g_p = 2 * xb.T @ (xb @ theta - yb) / len(idx)
            if method == "eqb": g_p = _eqb_clip(g_p, hist, kappa)
            if nb > 0:
                sel = rng.choice(nb, min(rb, nb), replace=False)
                g_q = 2 * bufX[sel].T @ (bufX[sel] @ theta - bufy[sel]) / len(sel)
                if method == "fixed":
                    w = value
                elif method in ("eq", "eqb"):
                    if ev_p is None: ev_p, ev_q = g_p.copy(), g_q.copy()
                    else: ev_p = smooth * ev_p + (1 - smooth) * g_p; ev_q = smooth * ev_q + (1 - smooth) * g_q
                    M = Fd if metric == "fisher" else 1.0
                    w = min(value * np.sqrt(np.sum(M * ev_p * ev_p) / max(np.sum(M * ev_q * ev_q), 1e-18)), wcap)
                else:
                    raise ValueError(method)
                wlog.append(w)
                g = g_p + w * g_q
            else:
                g = g_p
            theta = theta - lr * g
            Fd = 0.99 * Fd + 0.01 * g_p * g_p
            for j in idx:  # reservoir
                seen += 1
                if nb < buf: bufX[nb] = X[j]; bufy[nb] = y[j]; nb += 1
                else:
                    t = rng.integers(seen)
                    if t < buf: bufX[t] = X[j]; bufy[t] = y[j]
    per_task = []
    for (_, _, Xt, yt) in tasks:
        per_task.append(float(np.mean((Xt @ theta - yt) ** 2) / np.var(yt)))
    return dict(metric=float(np.mean(per_task)), per_task=per_task, w_med=float(np.median(wlog)) if wlog else None)


def S_R_convex_replay_constant(seed=0):
    """S-R: convex replay learner, all tasks at the same input scale. The present/past
    gradient-norm ratio is stationary, so a fixed w matches the adaptive rule: H-EQ
    (adaptivity beats the best constant) MUST FAIL here."""
    scales = (1.0, 1.0, 1.0, 1.0, 1.0)
    return (lambda method, value, s: _replay_learner(scales, method, value, s)), None, {"name": "S-R convex replay, constant label scale (adaptivity idle)"}


def S_V_convex_replay_varying(seed=0):
    """S-V: convex replay learner whose task LABEL scales swing 16x between consecutive
    tasks, so the present/past gradient-norm ratio swings ~16x and no single fixed w is
    right for every task. Positive control: adaptivity MUST PASS or the gate is blind."""
    scales = (1.0, 4.0, 0.25, 4.0, 0.25)
    return (lambda method, value, s: _replay_learner(scales, method, value, s)), None, {"name": "S-V convex replay, 16x label-scale swings (adaptivity load-bearing)"}


# ---------------------------------------------------------------- EWC / constraint surrogates (EQ2, issue #20 §3)
# Same convex stream as the replay family, but the past term is NOT replayed data:
#   S-W: the exact quadratic (Laplace) penalty of the past quadratic loss (EWC-online
#        with lambda removed -- the rule or the fixed w supplies the weight).
#   S-X: a logit-matching soft constraint on a frozen copy of the model (DER++/LwF
#        style): not a loss on the past task; its metric-optimal weight is a small
#        fraction of the present pull, so equal-length pulling over-regularises.
# The update stays g = g_present + w * g_past, so gate_EQ2 scores both against the
# same fixed-w grid it scores S-R on.

def _ewc_laplace_learner(scales, method, value, seed, d=32, n_task=2000, n_test=500, bs=10,
                         lr=0.01, smooth=0.9, wcap=1.5, noise_sd=0.3, kappa=EQB_KAPPA, mismatch=16.0,
                         offset=0.25, n_past=2):
    """One online pass over tasks that share a base solution (each task's optimum is
    `offset` away from the shared base: the continual fine-tuning regime). Tasks
    0..n_past-1 are the PAST phase: trained jointly on their pooled rows, then frozen
    into the exact Laplace penalty of that past quadratic loss -- anchor theta_star =
    where training stopped (the penalty gradient is exactly zero there), curvature
    F = mismatch * Xp'Xp / n_past_samples. The past loss is measured in units
    `mismatch` x the present term's (its Hessian is mismatch * 2 * Xp'Xp/n against the
    present's 2 * X'X/n ~ 2I): the 16x curvature-scale mismatch that makes a fixed
    lambda dataset-dependent. The penalty gradient carries NO lambda:
    g_q = 2 * (F @ (theta - theta_star)); the rule or the fixed w supplies the weight.
    Present tasks keep unit data scale; their LOSS is weighted by scales[k] (y is NOT
    scaled), so their pull magnitude swings 16x (4.0 -> 0.25) while their optima stay
    put -- a fixed lambda lands at a pull-dependent fraction of each gap, the rule at
    Omega re-derives the weight every step. The stream is task-balanced (n_past past
    vs the same number of present tasks): equal pull is then the symmetric compromise,
    which is the mechanism EQ2 claims. wcap=1.5, not the replay family's 20.0: with
    2*lambda_max(F) ~ 35, the cap keeps lr * w * 2 * lambda_max(F) ~ 0.5, so the
    penalty step stays a damped step, not an oscillator. Returns normalised held-out
    MSE over all tasks."""
    rng = np.random.default_rng(seed)
    K = len(scales)
    th_base = rng.standard_normal(d)
    tasks = []
    for k in range(K):
        th = th_base + offset * rng.standard_normal(d)
        X = rng.standard_normal((n_task, d)); y = X @ th + noise_sd * rng.standard_normal(n_task)
        Xt = rng.standard_normal((n_test, d)); yt = Xt @ th + noise_sd * rng.standard_normal(n_test)
        tasks.append((X, y, Xt, yt))
    Xp = np.vstack([tasks[k][0] for k in range(n_past)])    # pooled past rows
    yp = np.concatenate([tasks[k][1] for k in range(n_past)])
    theta = np.zeros(d)
    permp = rng.permutation(len(yp))
    for i in range(0, len(yp), bs):                  # train the past loss alone
        idx = permp[i:i + bs]
        theta = theta - lr * 2 * Xp[idx].T @ (Xp[idx] @ theta - yp[idx]) / len(idx)
    theta_star = theta.copy()                        # anchor: where the past loss ended
    F = mismatch * (Xp.T @ Xp / len(yp))             # exact Laplace curvature, 16x units
    ev_p = ev_q = None; wlog = []
    for k in range(n_past, K):
        X, y, _, _ = tasks[k]
        perm = rng.permutation(n_task); hist = []
        for i in range(0, n_task, bs):
            idx = perm[i:i + bs]; xb, yb = X[idx], y[idx]
            g_p = scales[k] * 2 * xb.T @ (xb @ theta - yb) / len(idx)   # pull swings, optimum does not
            if method == "eqb": g_p = _eqb_clip(g_p, hist, kappa)
            g_q = 2 * (F @ (theta - theta_star))     # penalty gradient, lambda removed
            if method == "fixed":
                w = value
            elif method in ("eq", "eqb"):
                if ev_p is None: ev_p, ev_q = g_p.copy(), g_q.copy()
                else: ev_p = smooth * ev_p + (1 - smooth) * g_p; ev_q = smooth * ev_q + (1 - smooth) * g_q
                w = min(value * np.sqrt(np.sum(ev_p * ev_p) / max(np.sum(ev_q * ev_q), 1e-18)), wcap)
            else:
                raise ValueError(method)
            wlog.append(w)
            theta = theta - lr * (g_p + w * g_q)
    per_task = []
    for (_, _, Xt, yt) in tasks:
        per_task.append(float(np.mean((Xt @ theta - yt) ** 2) / np.var(yt)))
    return dict(metric=float(np.mean(per_task)), per_task=per_task, w_med=float(np.median(wlog)) if wlog else None)

def _constraint_learner(scales, method, value, seed, d=32, n_task=2000, n_test=500, bs=10,
                        lr=0.01, smooth=0.9, wcap=2.0, noise_sd=0.3, kappa=EQB_KAPPA, logit_scale=4.0):
    """One online pass, all tasks at unit input and label scale. At each task boundary
    the model is frozen into a copy theta_prev; the past term is then a logit-matching
    CONSTRAINT on the current batch, mean_i (logit_scale * x_i . (theta -
    theta_prev))^2, with gradient
    g_q = 2 * logit_scale^2 * Xb'Xb (theta - theta_prev) / bs and NO lambda. The
    logit_scale is the DER++/LwF unit mismatch: logits are large-magnitude objects, so
    the constraint's natural weight is a small fraction of the present pull, and
    equal-length pulling over-regularises. The constraint is not a loss on the past
    task: its curvature is the current batch's own (rank <= bs of d, redrawn every
    step), so it descends no past loss. wcap=2.0: the constraint's effective curvature
    is logit_scale^2 x the batch Hessian, and the cap keeps lr * w * 2 * lambda_max
    safely under the overshoot bound at the family lr. During task 0 the copy equals
    the model (nothing is settled yet), so the constraint gradient is zero there."""
    rng = np.random.default_rng(seed)
    K = len(scales)
    tasks = []
    for k, sc in enumerate(scales):
        th = rng.standard_normal(d)
        X = rng.standard_normal((n_task, d)); y = sc * (X @ th + noise_sd * rng.standard_normal(n_task))
        Xt = rng.standard_normal((n_test, d)); yt = sc * (Xt @ th + noise_sd * rng.standard_normal(n_test))
        tasks.append((X, y, Xt, yt))
    theta = np.zeros(d)
    ev_p = ev_q = None; wlog = []
    for k in range(K):
        theta_prev = theta.copy()                    # frozen copy at the boundary (DER++/LwF style)
        X, y, _, _ = tasks[k]
        perm = rng.permutation(n_task); hist = []
        for i in range(0, n_task, bs):
            idx = perm[i:i + bs]; xb, yb = X[idx], y[idx]
            g_p = 2 * xb.T @ (xb @ theta - yb) / len(idx)
            if method == "eqb": g_p = _eqb_clip(g_p, hist, kappa)
            g_q = 2 * logit_scale ** 2 * (xb.T @ xb) @ (theta - theta_prev) / len(idx)   # logit-match gradient, no lambda
            if method == "fixed":
                w = value
            elif method in ("eq", "eqb"):
                if ev_p is None: ev_p, ev_q = g_p.copy(), g_q.copy()
                else: ev_p = smooth * ev_p + (1 - smooth) * g_p; ev_q = smooth * ev_q + (1 - smooth) * g_q
                w = min(value * np.sqrt(np.sum(ev_p * ev_p) / max(np.sum(ev_q * ev_q), 1e-18)), wcap)
            else:
                raise ValueError(method)
            wlog.append(w)
            theta = theta - lr * (g_p + w * g_q)
    per_task = []
    for (_, _, Xt, yt) in tasks:
        per_task.append(float(np.mean((Xt @ theta - yt) ** 2) / np.var(yt)))
    return dict(metric=float(np.mean(per_task)), per_task=per_task, w_med=float(np.median(wlog)) if wlog else None)


def S_W_ewc_laplace_replay(seed=0, mismatch=16.0):
    """S-W: convex learner whose past term is the exact quadratic (Laplace) penalty of
    a past quadratic loss (EWC-online, lambda removed), measured in units 16x the
    present term's (curvature scale mismatch=16), with the present loss weights
    swinging 16x (4.0 -> 0.25) against it. Positive control: the rule at Omega = 1
    must not be behind the tuned fixed weight (EQ2 MUST PASS) or the gate cannot see
    the mechanism."""
    scales = (1.0, 1.0, 4.0, 0.25)
    return (lambda method, value, s: _ewc_laplace_learner(scales, method, value, s, mismatch=mismatch)), None, \
        {"name": f"S-W EWC-Laplace convex replay, {int(round(mismatch))}x curvature-scale mismatch"}


def S_X_constraint_learner(seed=0):
    """S-X: convex learner whose past term is a logit-matching soft constraint on a
    frozen copy of the model (DER++/LwF style), not a loss on the past task: its
    metric-optimal weight is a small fraction of the present pull, so the same-length
    rule over-regularises. Negative control: EQ2 MUST FAIL here."""
    scales = (1.0, 1.0, 1.0, 1.0, 1.0)
    return (lambda method, value, s: _constraint_learner(scales, method, value, s)), None, \
        {"name": "S-X constraint learner, tuned weight a small fraction of present norm"}


# ---------------------------------------------------------------- nonconvex EWC / LwF surrogates (EQ2 positive control, issue #20)
# The convex S-W row shows that on a quadratic loss with a quadratic penalty a fixed weight
# is metric-optimal and the rule reduces to a constant (PR #23). The effect the EQ2 claim is
# about needs a present gradient that DECAYS as the task is learned (a softmax classifier),
# so that a fixed lambda right early in a task is too strong late in it; the rule co-scales
# the penalty step with the present step. S-Y is that learner. S-Y/LwF is the same network
# with a distillation constraint as the past term: the same-family negative control.
# Every constant is named here; the estimator constants (smooth, wcap) are the ones the EQ2
# prereg registers, and the row's own sensitivity to them is reported in the PR that adds it.

_SY_K, _SY_H, _SY_BS, _SY_LR, _SY_N_PER_CLASS, _SY_STEPS = 10, 32, 32, 0.05, 400, 150


def _sy_data(rng, d, sep, scale):
    mu = rng.standard_normal((_SY_K, d)) * sep
    X, y = [], []
    for c in range(_SY_K):
        X.append((mu[c] + rng.standard_normal((2 * _SY_N_PER_CLASS, d))) * scale)
        y.append(np.full(2 * _SY_N_PER_CLASS, c))
    X = np.concatenate(X); y = np.concatenate(y)
    te = np.zeros(len(y), bool)
    for c in range(_SY_K):
        ii = np.where(y == c)[0]; te[ii[: len(ii) // 2]] = True
    return (X[~te], y[~te]), (X[te], y[te])


def _sy_softmax(z):
    z = z - z.max(1, keepdims=True); p = np.exp(z); return p / p.sum(1, keepdims=True)


class _SyMLP:
    """Two-layer ReLU MLP, single softmax head over all _SY_K classes (class-IL)."""
    def __init__(self, rng, d):
        self.p = [rng.normal(0, np.sqrt(2 / d), (d, _SY_H)), np.zeros(_SY_H),
                  rng.normal(0, np.sqrt(2 / _SY_H), (_SY_H, _SY_K)), np.zeros(_SY_K)]
    def fwd(self, x):
        W1, b1, W2, b2 = self.p; h = np.maximum(0, x @ W1 + b1); return h, h @ W2 + b2
    def grad(self, x, dz, h):
        W1, b1, W2, b2 = self.p; dh = dz @ W2.T; dh[h <= 0] = 0
        return np.concatenate([(x.T @ dh).ravel(), dh.sum(0), (h.T @ dz).ravel(), dz.sum(0)])
    def flat(self): return np.concatenate([a.ravel() for a in self.p])
    def set_flat(self, v):
        i = 0
        for a in self.p:
            a[...] = v[i:i + a.size].reshape(a.shape); i += a.size
    def copy(self):
        m = _SyMLP.__new__(_SyMLP); m.p = [a.copy() for a in self.p]; return m
    def err(self, x, y):
        with np.errstate(all="ignore"):
            z = self.fwd(x)[1]
        if not np.all(np.isfinite(z)):
            return 1.0                                   # a diverged model: every prediction wrong
        return float((z.argmax(1) != y).mean())


def _sy_ce_grad(net, x, y):
    h, z = net.fwd(x); p = _sy_softmax(z); dz = p; dz[np.arange(len(y)), y] -= 1; dz /= len(y)
    return net.grad(x, dz, h)


_SY_POISON_AT = 0.25                                            # poisoned row: from step max(EQB_N_MIN, floor(_SY_POISON_AT * _SY_STEPS)) of each task after the first


def _sy_mlp_learner(method, value, seed, past="ewc", d=32, sep=1.4, scale=4.0,
                    smooth=0.9, wcap=1e4, n_fisher=20, kappa=EQB_KAPPA, poison=None):
    """One online pass over 5 tasks x 2 classes. past='ewc': online-EWC penalty gradient
    2*F*(theta - theta_star), lambda REMOVED, F the empirical Fisher accumulated at every
    boundary (mean squared per-batch gradient over n_fisher batches, times the batch size).
    past='lwf': distillation gradient on the current batch against the model frozen at the
    last boundary (LwF constraint, weight removed). method='fixed': w = value.
    method='eq': w = value * ||ema g_present|| / ||ema g_past|| (Euclidean, EMA of the
    gradient vectors, capped at wcap). method='eqb': the present gradient is first clipped by
    _eqb_clip (EQ-B; history reset at every task boundary), then as 'eq'. poison=(factor, run):
    `run` consecutive present gradients per task after the first are multiplied by `factor`
    (the positive control of the EQ-B gate). Returns the final class-IL ERROR rate over all classes
    (lower is better) and the median derived weight. Deterministic given the seed."""
    rng = np.random.default_rng(seed)
    (Xtr, ytr), (Xte, yte) = _sy_data(rng, d, sep, scale)
    net = _SyMLP(rng, d); n = net.flat().size
    fisher = np.zeros(n); theta_star = None; prev = None
    ema_p = ema_q = None; wlog = []; p_start = max(EQB_N_MIN, int(_SY_POISON_AT * _SY_STEPS))
    with np.errstate(all="ignore"):
        for task in range(5):
            cls = (2 * task, 2 * task + 1)
            ii_task = rng.permutation(np.where(np.isin(ytr, cls))[0]); hist = []
            for step in range(_SY_STEPS):
                ii = ii_task[rng.integers(0, len(ii_task), _SY_BS)]; x, y = Xtr[ii], ytr[ii]
                g_p = _sy_ce_grad(net, x, y)
                if poison is not None and task >= 1 and p_start <= step < p_start + poison[1]: g_p = poison[0] * g_p
                if method == "eqb": g_p = _eqb_clip(g_p, hist, kappa)
                g_q = None
                if past == "ewc" and theta_star is not None:
                    g_q = 2 * fisher * (net.flat() - theta_star)
                elif past == "lwf" and prev is not None:
                    h, z = net.fwd(x); zp = prev.fwd(x)[1]
                    g_q = net.grad(x, (_sy_softmax(z) - _sy_softmax(zp)) / _SY_BS, h)
                if g_q is None:
                    net.set_flat(net.flat() - _SY_LR * g_p); continue
                if method == "fixed":
                    w = value
                elif method in ("eq", "eqb"):
                    ema_p = g_p if ema_p is None else smooth * ema_p + (1 - smooth) * g_p
                    ema_q = g_q if ema_q is None else smooth * ema_q + (1 - smooth) * g_q
                    w = min(value * np.linalg.norm(ema_p) / max(np.linalg.norm(ema_q), 1e-12), wcap)
                else:
                    raise ValueError(method)
                wlog.append(w)
                net.set_flat(net.flat() - _SY_LR * (g_p + w * g_q))
            prev = net.copy()                            # boundary: frozen copy (LwF)
            if past == "ewc":                            # boundary: accumulate the empirical Fisher, reset the anchor
                f = np.zeros(n)
                for _ in range(n_fisher):
                    ii = ii_task[rng.integers(0, len(ii_task), _SY_BS)]
                    f += _sy_ce_grad(net, Xtr[ii], ytr[ii]) ** 2
                fisher = fisher + f / n_fisher * _SY_BS
                theta_star = net.flat().copy()
    return dict(metric=net.err(Xte, yte), w_med=float(np.median(wlog)) if wlog else None)


_SY_GRID_EWC = (0.0625, 0.25, 1.0, 4.0, 16.0, 64.0, 128.0, 256.0, 512.0, 1024.0)
_SY_GRID_LWF = (0.0625, 0.25, 0.5, 1.0, 2.0, 4.0, 16.0, 64.0)


def S_Y_mlp_online_ewc(seed=0):
    """S-Y: softmax MLP (class-IL, 5 tasks x 2 classes, one online pass) with online EWC; past
    term = penalty gradient 2*F*(theta - theta_star), lambda removed; inputs at scale 4, so
    F (a squared gradient) is 16x the unit-scale one. Positive control: the rule at Omega=1
    must not be behind the tuned fixed weight (EQ2 MUST PASS). The row's fixed_grid reaches
    1024 because the tuned weight sits in the hundreds (R7: the baseline must be able to win)."""
    return (lambda method, value, s: _sy_mlp_learner(method, value, s, past="ewc", scale=4.0)), None, \
        {"name": "S-Y softmax MLP, online EWC, 16x Fisher-scale mismatch (input scale 4)", "fixed_grid": _SY_GRID_EWC}


def S_Y_mlp_online_ewc_unit_scale(seed=0):
    """S-Y at unit input scale: informational row, no control role. Reported so the reader can
    see how much of the effect is the scale mismatch."""
    return (lambda method, value, s: _sy_mlp_learner(method, value, s, past="ewc", scale=1.0)), None, \
        {"name": "S-Y softmax MLP, online EWC, unit input scale (informational)", "fixed_grid": _SY_GRID_EWC}


def S_Y_mlp_online_ewc_cap100(seed=0):
    """S-Y with the ratio cap lowered to 100 (registered value 1e4): informational row. The
    derived weight sits in the thousands, so a low cap turns the rule into a weaker fixed
    weight than the tuned one; the pass is specific to the registered cap and the prereg
    sensitivity table must say so."""
    return (lambda method, value, s: _sy_mlp_learner(method, value, s, past="ewc", scale=4.0, wcap=100.0)), None, \
        {"name": "S-Y softmax MLP, online EWC, scale 4, cap=100 (informational)", "fixed_grid": _SY_GRID_EWC}


def S_Y_mlp_online_ewc_smooth080(seed=0):
    """S-Y with EMA smoothing 0.8 (registered 0.9): informational row."""
    return (lambda method, value, s: _sy_mlp_learner(method, value, s, past="ewc", scale=4.0, smooth=0.8)), None, \
        {"name": "S-Y softmax MLP, online EWC, scale 4, smooth=0.8 (informational)", "fixed_grid": _SY_GRID_EWC}


def S_Y_mlp_online_ewc_smooth098(seed=0):
    """S-Y with EMA smoothing 0.98 (registered 0.9): informational row."""
    return (lambda method, value, s: _sy_mlp_learner(method, value, s, past="ewc", scale=4.0, smooth=0.98)), None, \
        {"name": "S-Y softmax MLP, online EWC, scale 4, smooth=0.98 (informational)", "fixed_grid": _SY_GRID_EWC}


def S_Y_mlp_lwf_constraint(seed=0):
    """S-Y/LwF: the same network and stream; past term = distillation gradient on the current
    batch against the model frozen at the last boundary (LwF, weight removed): a constraint,
    not a loss on the past task. Negative control in the same nonconvex family: EQ2 MUST FAIL."""
    return (lambda method, value, s: _sy_mlp_learner(method, value, s, past="lwf", scale=4.0)), None, \
        {"name": "S-Y/LwF softmax MLP, distillation constraint (input scale 4)", "fixed_grid": _SY_GRID_LWF}


_SY_POISON = (1000.0, 5)                                        # (factor, run): omega_reprocessed.py [4], where the registered rule diverges on the quadratic


def S_Y_mlp_online_ewc_poisoned(seed=0):
    """S-Y with poisoned batches: five consecutive present gradients per task (after the first) multiplied by 1000.
    Positive control for EQB and EQBM (the registered rule amplifies the past step in proportion to the present
    gradient's length; EQ-B clips the present gradient first). The fixed-weight grid is scored on the same poisoned
    stream, so the tuned weight is tuned under poison (R7)."""
    return (lambda method, value, s: _sy_mlp_learner(method, value, s, past="ewc", scale=4.0, poison=_SY_POISON)), None, \
        {"name": "S-Y softmax MLP, online EWC, scale 4, poisoned batches (x1000, 5 per task)", "fixed_grid": _SY_GRID_EWC}


REPLAY_BATTERY = [S_R_convex_replay_constant, S_V_convex_replay_varying,
                  S_W_ewc_laplace_replay, S_X_constraint_learner,
                  S_Y_mlp_online_ewc, S_Y_mlp_online_ewc_unit_scale,
                  S_Y_mlp_online_ewc_cap100, S_Y_mlp_online_ewc_smooth080, S_Y_mlp_online_ewc_smooth098,
                  S_Y_mlp_lwf_constraint, S_Y_mlp_online_ewc_poisoned]


# ---------------------------------------------------------------- salience-replay surrogates (study SAL: the occasion-weight law on a learner)
# Synthetic class-IL streams for crr.instrument.replay.salience_replay. Each generator returns
# (runner, None, meta) with runner(lam, seed, **kw) -> the learner's result dict.
#   S-SAL-P  positive control: tasks of unequal difficulty, so their learning paths have unequal
#            surplus and the harder tasks are the ones forgotten; weighting replay by e^{S} must
#            help (MUST PASS).
#   S-SAL-F  flat negative control: identical task difficulty, so surplus is (nearly) equal across
#            tasks and the weights are uniform whatever lambda: the rule must add nothing (MUST FAIL).
#   S-SAL-D  decoupled negative control: equal difficulty, but gradient noise injected during two
#            tasks inflates their surplus without changing what is learned or forgotten; the
#            rule must not help (MUST FAIL).
_SAL_K, _SAL_D, _SAL_N = 10, 24, 300


def _sal_data(seed, seps):
    rng = np.random.default_rng(seed)
    X, y = [], []
    for c in range(_SAL_K):
        mu = rng.standard_normal(_SAL_D) * seps[c // 2]
        X.append(mu + rng.standard_normal((2 * _SAL_N, _SAL_D))); y.append(np.full(2 * _SAL_N, c))
    X = np.concatenate(X); y = np.concatenate(y)
    te = np.zeros(len(y), bool)
    for c in range(_SAL_K):
        ii = np.where(y == c)[0]; te[ii[:_SAL_N]] = True
    return X[~te], y[~te], X[te], y[te]


def _sal_runner(seps, grad_noise=None):
    from crr.instrument.replay import salience_replay
    def run(lam, seed, **kw):
        Xtr, ytr, Xte, yte = _sal_data(seed, seps)
        return salience_replay(Xtr, ytr, Xte, yte, _SAL_K, 2, lam, seed, hid=64, epochs=2, grad_noise=grad_noise, **kw)
    return run


def S_SAL_positive(seed=0):
    """S-SAL-P: five tasks with separations (2.0, 0.6, 2.0, 0.6, 2.0): the two hard tasks have
    higher surplus and are forgotten more under uniform replay; e^{S}-weighting MUST PASS."""
    return _sal_runner((2.0, 0.6, 2.0, 0.6, 2.0)), None, {"name": "S-SAL-P unequal task difficulty (surplus tracks forgetting)"}


def S_SAL_flat(seed=0):
    """S-SAL-F: five tasks of equal separation: surplus nearly equal, weights uniform for every
    lambda; the rule MUST FAIL (nothing to act on)."""
    return _sal_runner((1.2, 1.2, 1.2, 1.2, 1.2)), None, {"name": "S-SAL-F equal task difficulty (surplus flat)"}


def S_SAL_decoupled(seed=0):
    """S-SAL-D: equal separation, gradient noise (sd 0.3) during tasks 1 and 3 inflates their
    surplus without changing the task: surplus is decoupled from forgetting; MUST FAIL."""
    return _sal_runner((1.2, 1.2, 1.2, 1.2, 1.2), grad_noise={1: 0.3, 3: 0.3}), None, {"name": "S-SAL-D surplus inflated by gradient noise (decoupled from forgetting)"}


SALIENCE_BATTERY = [S_SAL_positive, S_SAL_flat, S_SAL_decoupled]


# ---------------------------------------------------------------- rate surrogates (H-L5 on count series, SCOPE.md P6/P9)
# Synthetic epidemic curves: non-negative rate lam(t) built from cycles, then Poisson
# counts. events = the true cycle starts (the onsets), known by construction.
# The concavity trap: under the Poisson metric arc = TV(2 sqrt lam), and sqrt halves the
# CV of a variable peak height, so a variable-amplitude, variable-period curve can show
# CV(arc) < CV(clock) with no CRR content. Control (i) (amplitude, scored in the SAME
# metric, by paired bootstrap) is what must catch it. S-P rows test exactly that.

def _rate_cycles(periods, peaks, shape, base=2.0, seed=0):
    rng = np.random.default_rng(seed)
    lam, ev, pos = [], [], 0
    for p, a in zip(periods, peaks):
        u = np.linspace(0, 1, int(p), endpoint=False)
        lam.append(base + a * shape(u)); ev.append(pos); pos += int(p)
    lam = np.concatenate(lam)
    counts = rng.poisson(lam).astype(float)
    return counts, np.asarray(ev)


def _hump(u):  # one epidemic hump per cycle: rise then fall, zero at both ends
    return np.sin(np.pi * u) ** 2


def _two_humps(u, h1, h2):  # two humps of heights h1, h2 inside one cycle
    return np.where(u < 0.5, h1 * np.sin(2 * np.pi * u) ** 2, h2 * np.sin(2 * np.pi * u) ** 2)


def S_P_am(n=60, seed=0, peak=400.0, jitter=0.3):
    rng = np.random.default_rng(seed)
    a = peak * rng.uniform(1 - jitter, 1 + jitter, n)
    x, ev = _rate_cycles(np.full(n, 52), a, _hump, seed=seed)
    return x, ev, {"name": "S-P AM epidemics (constant period, variable peak)"}


def S_P_fm(n=60, seed=0, peak=400.0, jitter=0.25):
    rng = np.random.default_rng(seed)
    p = rng.uniform(52 * (1 - jitter), 52 * (1 + jitter), n)
    x, ev = _rate_cycles(p, np.full(n, peak), _hump, seed=seed)
    return x, ev, {"name": "S-P FM epidemics (variable period, constant peak; arc ties amplitude)"}


def S_P_amfm(n=60, seed=0, peak=400.0):
    rng = np.random.default_rng(seed)
    p = rng.uniform(40, 64, n); a = peak * rng.uniform(0.7, 1.3, n)
    x, ev = _rate_cycles(p, a, _hump, seed=seed)
    return x, ev, {"name": "S-P AM+FM epidemics (the concavity trap: no CRR content)"}


def S_P_fm_compensating(n=60, seed=0, peak=400.0, jitter=0.25):
    """Variable period; each cycle has two humps whose heights sum to a constant, so the
    arc (sum of rises and falls) is constant while the peak amplitude varies: arc beats
    amplitude BY CONSTRUCTION. Positive control for 'beyond control (i)'."""
    rng = np.random.default_rng(seed)
    p = rng.uniform(52 * (1 - jitter), 52 * (1 + jitter), n)
    f = rng.uniform(0.3, 0.7, n)
    lam, ev, pos = [], [], 0
    for pk, fk in zip(p, f):
        u = np.linspace(0, 1, int(pk), endpoint=False)
        lam.append(2.0 + peak * _two_humps(u, fk, 1 - fk)); ev.append(pos); pos += int(pk)
    lam = np.concatenate(lam)
    return rng.poisson(lam).astype(float), np.asarray(ev), {"name": "S-P FM two-hump compensating (arc constant, amplitude variable)"}


def S_P_clock_regular_two_hump(n=60, seed=0, peak=400.0):
    """Constant period; two humps whose heights vary independently, so both arc and
    amplitude vary while the clock does not: clock-regular by construction, must FAIL."""
    rng = np.random.default_rng(seed)
    lam, ev, pos = [], [], 0
    for _ in range(n):
        u = np.linspace(0, 1, 52, endpoint=False)
        h1, h2 = rng.uniform(0.3, 1.0, 2)
        lam.append(2.0 + peak * _two_humps(u, h1, h2)); ev.append(pos); pos += 52
    lam = np.concatenate(lam)
    return rng.poisson(lam).astype(float), np.asarray(ev), {"name": "S-P clock-regular two-hump (constant period, variable arc)"}


RATE_BATTERY = [S_P_am, S_P_fm, S_P_amfm, S_P_fm_compensating, S_P_clock_regular_two_hump]

# One ROW per registered parameter value: the row name encodes the parameter
# (the gate keys MUST_FAIL/MUST_PASS on these names). The sweeps of S-C and
# S-D and the mu=1 van der Pol variant are separate rows of the same generator.
BATTERY = [
    S_A_sine, S_A1_fm_sine, S_A2_am_sine, S_A3_amfm_sine, S_B_sine_bump,
    *[partial(S_C_lobed_ramp, lam=lam) for lam in (0.0, 0.25, 0.5, 1.0)],
    *[partial(S_D_noisy_sine, rho=r) for r in (5.0, 10.0, 20.0, 40.0, 80.0)],
    S_E_asymmetric,
    S_F_vanderpol, partial(S_F_vanderpol, mu=1.0), S_F_roessler, S_F_duffing,
    S_G_relaxation, S_G2_relaxation_arc_regular,
]
