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
                    buf=200, lr=0.01, smooth=0.9, metric="euclid", wcap=20.0, noise_sd=0.3):
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
        perm = rng.permutation(n_task)
        for i in range(0, n_task, bs):
            idx = perm[i:i + bs]; xb, yb = X[idx], y[idx]
            g_p = 2 * xb.T @ (xb @ theta - yb) / len(idx)
            if nb > 0:
                sel = rng.choice(nb, min(rb, nb), replace=False)
                g_q = 2 * bufX[sel].T @ (bufX[sel] @ theta - bufy[sel]) / len(sel)
                if method == "fixed":
                    w = value
                elif method == "eq":
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


REPLAY_BATTERY = [S_R_convex_replay_constant, S_V_convex_replay_varying]


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
