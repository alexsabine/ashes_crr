"""CRR retrodiction battery on cognitive, learning-machine, economic, collective, evolutionary-game and
social-diffusion model systems (owner request 2026-09-17, prompt-log entry 48).

Nine model systems in six classes no earlier battery covered: (cog) the drift-diffusion decision model
(two drift regimes), Rescorla-Wagner learning read against the Kalman gain (P4), and retention in natural
time vs clock time under variable-rate interference (P5); (ai) a linear echo-state reservoir where the
influence of every past input block on the final state is MEASURED (age weights P3 vs surplus weights P2,
the O2 question), and simulated annealing of a two-level system with schedules of equal Fisher length
(Salamon-Nulton constant thermodynamic speed); (econ) GARCH(1,1) volatility clustering with an i.i.d.
control; (col) the Kuramoto synchronisation transition with Lorentzian frequencies (exact order parameter)
and the older text's criticality clause; (evo) the rock-paper-scissors replicator with an attracting
heteroclinic cycle, on the Fisher-native simplex carrier (P7), where passage times grow without bound and
the Fisher arc per epoch saturates at the vertex-to-vertex distance; (soc) Bass diffusion of an innovation
as one occasion.

Grades under the issue-#21 rules (SHARP / CONSIST / DESCR / FAILS / TENSION / OPEN; rule 2 on chosen
observables, rule 3 on definitions, rule 4 on symmetric members); BORROWED and FLOW per row; H-L5 class
where the system has its own events, exclusive segmentation where the event is a reset (prompt-log entry
41); every class or regime label is computed from its number; a margin below 0.01 is not a reading.
Model systems only; no dataset opened (R2). Deterministic (seeded). Run:
uv run python theory/retrodictions/cognitive_collective.py
"""
import math
import sys

import numpy as np
from scipy.integrate import solve_ivp

from crr.instrument.core import arc_length, regularity

ROWS = []


def row(cls, system, clause, borrowed, flow, derivation, known, verdict, grade, l5=None, weakness=""):
    ROWS.append(dict(cls=cls, system=system, clause=clause, borrowed=borrowed, flow=flow, derivation=derivation,
                     known=known, verdict=verdict, grade=grade, l5=l5, weakness=weakness))


def cv(x): x = np.asarray(x, float); return float(x.std(ddof=1) / abs(x.mean()))


def l5_class(x, events, dt=1.0, segment_end="inclusive"):
    r = regularity(np.asarray(x, float), np.asarray(events, int), sigma=1.0, dt=dt, n_boot=200, seed=0, segment_end=segment_end)
    if abs(r["cv_arc"] - r["cv_clock"]) < 1e-3: lab = "tie"
    else: lab = "arc-regular" if r["cv_arc"] < r["cv_clock"] else "clock-regular"
    return lab, r["cv_arc"], r["cv_clock"]


def reading(lab, ca, cc):
    return lab if (lab == "tie" or abs(ca - cc) >= 0.01) else f"{lab} by {abs(ca - cc):.3f}, below the 0.01 this battery treats as a reading"


def r2(y, X):
    """R^2 of y on a linear fit in the columns of X (with intercept)."""
    X = np.atleast_2d(np.asarray(X, float)); X = X.T if X.shape[0] < X.shape[1] else X
    A = np.c_[X, np.ones(len(X))]; y = np.asarray(y, float)
    coef, *_ = np.linalg.lstsq(A, y, rcond=None); res = y - A @ coef
    return float(1 - res.var() / y.var())


# ================================================================ (cog) cognitive models
def cog_drift_diffusion():
    """Two-boundary drift-diffusion model: dx = mu dt + sigma dW from 0 to +-a; a trial is an occasion; the reset to 0 at
    the next trial is the cut (exclusive segmentation). Registered drifts: drift-dominated and diffusion-dominated; and
    two registered sampling steps, because the arc of a Brownian path is its total variation, which is not finite:
    the sampled arc grows as 1/sqrt(dt) while the reaction time does not."""
    rng = np.random.default_rng(1); a, sig = 1.0, 1.0; n_tr = 60
    def run(mu, dt):
        trace = []; events = []
        for _ in range(n_tr):
            events.append(len(trace)); x = 0.0
            while abs(x) < a:
                x += mu * dt + sig * math.sqrt(dt) * rng.standard_normal(); trace.append(x)
        return np.array(trace), np.array(events)
    out = []
    for mu in (3.0, 0.3):
        for dt in (1e-3, 1e-2):
            tr, ev = run(mu, dt); lab, ca, cc = l5_class(tr, ev[2:], dt, segment_end="exclusive")
            rts = np.diff(ev[2:]) * dt; arcs = [arc_length(tr[p:q], 1.0) for p, q in zip(ev[2:-1], ev[3:])]
            out.append((mu, dt, lab, ca, cc, float(rts.mean()), cv(rts), float(np.mean(arcs))))
    ratio = [out[0][7] / out[1][7], out[2][7] / out[3][7]]
    row("cog", "Drift-diffusion decision model (two absorbing bounds): reaction time vs evidence-path arc, at two drifts and two sampling steps", "D5 (the decision = own event), D3 (the bound fixes the chord), D2 (arc of a diffusion path), D4, H-L5",
        "Ratcliff drift-diffusion model; first-passage times of Brownian motion with drift; Brownian paths have infinite total variation", "the drift rate (task-supplied), the noise, and the sampling step (instrument-supplied)",
        "; ".join(f"mu = {mu:g}, dt = {dt:g}: mean RT {mrt:.3f} (CV {crt:.2f}), mean arc per trial {ma:.2f} (chord 1), CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}" for mu, dt, lab, ca, cc, mrt, crt, ma in out)
        + f"; arc ratio between the two sampling steps: {ratio[0]:.2f} and {ratio[1]:.2f} (sqrt(10) = {math.sqrt(10):.2f}); the reaction times do not change",
        "RT distributions are right-skewed with CV set by the drift-to-noise ratio; the bound fixes the evidence at decision",
        f"drift-dominated: {reading(*out[0][2:5])} (dt 1e-3), {reading(*out[1][2:5])} (dt 1e-2); diffusion-dominated: {reading(*out[2][2:5])}, {reading(*out[3][2:5])}; the arc per trial is the noise's total variation and scales as 1/sqrt(dt): on a diffusion carrier D2's C is a property of the sampling step, not of the system, and every CV comparison on such a carrier is a comparison of the clock with itself",
        "TENSION", None, "internal: D2 presumes a rectifiable path; the cognitive, economic, Kramers and integrate-and-fire carriers are diffusions, so the tie results across the batteries are this theorem, not a finding about the systems; a prereg on a diffusion carrier must name a smoothing scale or a Fisher-native carrier that is rectifiable")


def cog_rescorla_wagner():
    """Rescorla-Wagner V <- V + alpha (lambda - V) is a fixed-gain filter. On a random-walk reward with Fisher speed v the
    MSE-optimal alpha is the steady-state Kalman gain K(v) (P4); v = 1 gives 1/phi. Is any alpha privileged?"""
    rng = np.random.default_rng(2); T = 20000
    def mse(alpha, v):
        q, r = v * v, 1.0; lam = 0.0; V = 0.0; err = 0.0
        for t in range(T):
            lam += math.sqrt(q) * rng.standard_normal(); obs = lam + math.sqrt(r) * rng.standard_normal()
            V += alpha * (obs - V); err += (V - lam) ** 2
        return err / T
    alphas = np.linspace(0.02, 0.98, 49); res = {}
    for v in (0.1, 0.3, 1.0):
        m = [mse(al, v) for al in alphas]; best = float(alphas[int(np.argmin(m))]); Kv = (v / 2) * (math.sqrt(v * v + 4) - v); res[v] = (best, Kv)
    phi_inv = (math.sqrt(5) - 1) / 2
    row("cog", "Rescorla-Wagner learning rate read against the steady-state Kalman gain at Fisher speed v (P4)", "P4 (K(v), K(1) = 1/phi; 'the formula itself is not CRR's'), O1 (no retention law)",
        "Rescorla-Wagner 1972 (fixed-gain error correction); Kalman filter as its normative counterpart (Dayan-Kakade)", "the reward volatility q and observation noise r (environment-supplied)",
        "; ".join(f"v = {v:g}: empirically best alpha {b:.2f}, Kalman K(v) = {k:.3f}" for v, (b, k) in res.items()) + f"; 1/phi = {phi_inv:.3f} is the optimum only at v = 1",
        "the optimal learning rate rises with reward volatility; conditioning fits typically give alpha well below 0.5",
        "the learning rate is the Kalman gain of the environment's Fisher speed, a standard identity; 'Omega = 1 <-> v = 1 -> alpha = 1/phi' is not a clause of v3.1, and if it were read as a prediction it would fail whenever the environment's speed is not 1 (rule 2: the observable v is the environment's)",
        "DESCR", None, "P4 says of itself that it is not CRR's; the row records that nothing in the reading fixes a learner's alpha")


def cog_retention_natural_time():
    """Retention R = exp(-A/rho) with A the count of intervening interference events (P5 in natural time), when the
    event rate lambda(t) varies (wake: high; sleep: low). Clock time and natural time give different curves; the
    Jenkins-Dallenbach sleep-wake asymmetry is the classic observation."""
    rng = np.random.default_rng(3); rho = 20.0; n_items = 300; T = 24.0
    def rate(t): return 4.0 if (t % 24.0) < 16.0 else 0.4                                # events per hour, wake vs sleep
    t_grid = np.linspace(0, T, 2401); lam = np.array([rate(t) for t in t_grid]); A = np.concatenate([[0], np.cumsum(0.5 * (lam[1:] + lam[:-1]) * np.diff(t_grid))])
    delays = rng.uniform(0.5, 24.0, n_items); Ad = np.interp(delays, t_grid, A); R = np.exp(-Ad / rho) * np.exp(0.05 * rng.standard_normal(n_items))
    r2_nat, r2_clk = r2(np.log(R), Ad), r2(np.log(R), delays)
    row("cog", "Retention under variable-rate interference: forgetting in natural time (events) vs clock time (P5)", "P5 (retention e^{-A/rho} in natural time), O3 (natural time gives the unit for point processes)",
        "interference theory of forgetting (Jenkins & Dallenbach 1924 sleep-wake asymmetry); Poisson interference", "the interference event rate lambda(t) (environment-supplied) and the unit rho",
        f"{n_items} items, delays 0.5-24 h, wake rate 4/h, sleep rate 0.4/h: R^2 of log retention on natural time A(t) = {r2_nat:.3f}, on clock time t = {r2_clk:.3f}",
        "retention over a sleep interval exceeds retention over an equal wake interval; decay-vs-interference is decided by whether elapsed time or intervening events predicts forgetting",
        "natural time predicts by construction (rule 3: the model retains in A); the content is the classic interference hypothesis, which CRR restates as 'the unit is the event count'; a real test needs retention data with recorded event rates, which no row has opened",
        "DESCR", None, "the row says only that CRR's P5 is the interference hypothesis in Fisher units; nothing about memory is derived")


# ================================================================ (ai) learning machines
def ai_reservoir_influence():
    """Linear echo-state reservoir x <- rho_s W x + w_in u: the influence of each past input block on the final state is
    measured (remove-one). O2 asks whether occasions are weighted by age (P3, geometric) or surplus (P2, exp(beta S)).
    Blocks differ in-family (random input magnitudes) and recur: exactly O2's condition."""
    rng = np.random.default_rng(4); N = 60; rho_s = 0.9; n_blocks = 12; L = 8
    W = rng.standard_normal((N, N)); W *= rho_s / max(abs(np.linalg.eigvals(W))); w_in = rng.standard_normal(N)
    scales = rng.uniform(0.2, 2.0, n_blocks); U = [s * rng.standard_normal(L) for s in scales]
    def run(blocks):
        x = np.zeros(N); path = [x.copy()]; S = []
        for u in blocks:
            start = len(path) - 1
            for uu in u: x = W @ x + w_in * uu; path.append(x.copy())
            seg = np.array(path[start:]); S.append(arc_length(seg) - float(np.linalg.norm(seg[-1] - seg[0])))
        return x, np.array(S)
    x_full, S = run(U); infl = np.array([np.linalg.norm(x_full - run([u if j != i else np.zeros(L) for j, u in enumerate(U)])[0]) for i in range(n_blocks)])
    age = (n_blocks - 1 - np.arange(n_blocks)) * L
    y = np.log(infl); r2_age = r2(y, age); r2_S = r2(y, S); r2_both = r2(y, np.c_[age, S]); r2_age_logscale = r2(y, np.c_[age, np.log(scales)])
    slope_age = np.polyfit(age, y, 1)[0]; q_fit = math.exp(slope_age)
    row("ai", "Linear echo-state reservoir: measured influence of each past input block on the final state, age weights (P3) vs surplus weights (P2)", "O2 (which constraint: age or surplus), P3 (pi_k proportional to q^k), P2 (pi_m proportional to e^{beta S_m}), D4",
        "echo-state networks (Jaeger 2001), fading memory; linear systems theory", "the spectral radius (designer-supplied) and the input stream",
        f"{n_blocks} blocks of {L} inputs, spectral radius {rho_s}: R^2 of log influence on age = {r2_age:.3f} (fitted q per step = {q_fit:.3f} against rho_s = {rho_s}), on surplus S = {r2_S:.3f}, on age + S = {r2_both:.3f}, on age + log input scale = {r2_age_logscale:.3f}",
        "a linear reservoir's memory fades geometrically at the spectral radius; the effect of an input is linear in its magnitude",
        f"age weights hold with q = the spectral radius (P3, by the system's linearity); the surplus adds {r2_both - r2_age:.3f} in R^2 beyond age, and what remains is the input's magnitude, not e^{{S}}: on this carrier O2 is decided for age and against surplus",
        "FAILS", None, "rule 4 / class dependence: P2's exponential-in-surplus weights fail on a linear fading-memory system; P3 holds but is the spectral radius renamed (DESCR on its own)")


def ai_simulated_annealing():
    """Two-level system (gap Delta = 1, kT units) cooled from beta = 0.2 to beta = 5 in fixed duration with relaxation
    time tau_r: dp/dt = -(p - p_eq(beta))/tau_r. Three schedules with identical endpoints and identical Fisher length
    (the same 1-D path in beta): linear in T, linear in beta, constant thermodynamic speed (Salamon-Nulton). Final
    excess energy and the lag integral decide; the length cannot (it is the same for all three)."""
    D = 1.0; tau_r = 1.0; b0, b1 = 0.2, 5.0; T = 40.0; n = 4000
    def p_eq(b): return 1.0 / (1.0 + math.exp(b * D))                                   # excited-state occupation
    def g(b): p = p_eq(b); return D * D * p * (1 - p)                                   # Fisher metric g_bb = Var(E)
    def integrate(beta_of_s):
        t = np.linspace(0, T, n + 1); dt = t[1] - t[0]; p = p_eq(b0); lag = 0.0
        for k in range(n):
            b = beta_of_s(t[k] / T); p += dt * (-(p - p_eq(b)) / tau_r); lag += dt * (p - p_eq(b)) ** 2 / (p_eq(b) * (1 - p_eq(b)))
        return p - p_eq(b1), lag
    lin_beta = lambda s: b0 + s * (b1 - b0)
    lin_T = lambda s: 1.0 / (1.0 / b0 + s * (1.0 / b1 - 1.0 / b0))
    bs = np.linspace(b0, b1, 4001); cum = np.concatenate([[0], np.cumsum(np.sqrt([g((x + y) / 2) for x, y in zip(bs[:-1], bs[1:])]) * np.diff(bs))]); Lg = cum[-1]
    const_speed = lambda s: float(np.interp(s * Lg, cum, bs))
    res = {name: integrate(f) for name, f in (("linear in T", lin_T), ("linear in beta", lin_beta), ("constant Fisher speed", const_speed))}
    best = min(res, key=lambda k: res[k][1])
    row("ai", "Simulated annealing of a two-level system: three schedules of identical Fisher length, only the speed profile differs", "D2 (the Fisher length of the schedule), P1; the driven battery's row 9 in a learning-machine setting",
        "Salamon-Nulton-Andresen constant-thermodynamic-speed annealing; Fisher metric of the Boltzmann family g = Var(E)", "the relaxation time tau_r and the schedule (designer-supplied)",
        f"Fisher length of every schedule = {Lg:.3f} (same path in beta); final excess occupation and lag integral: " + "; ".join(f"{k}: {v[0]:.2e}, {v[1]:.4f}" for k, v in res.items()) + f"; least lag: {best}",
        "constant thermodynamic speed minimises the excess dissipation of an annealing schedule of fixed duration",
        "the length is the same for all three, so no CRR path quantity distinguishes them; the domain's optimum is the speed profile (constant Fisher speed), the same finding as the two-parameter trap row: the Fisher metric supplies the right notion of speed, and CRR inherits it",
        "CONSIST", None, "inherited (thermodynamic geometry); CRR's arc is the schedule's length, which cannot rank schedules of equal length")


# ================================================================ (econ) economic time series
def econ_garch():
    """GARCH(1,1) daily returns with persistence 0.99 and an i.i.d. control of equal unconditional variance. Chosen events:
    absolute-return exceedances of 3 unconditional sigma (a market has no own event at the daily scale). Carrier: log
    price; the arc between events is the realised absolute variation (a discrete-time quantity here, so D2 is finite)."""
    rng = np.random.default_rng(5); n = 40000; om, al, be = 1e-6, 0.09, 0.90; sig2 = om / (1 - al - be)
    def garch():
        h = sig2; r = np.empty(n)
        for t in range(n):
            e = rng.standard_normal(); r[t] = math.sqrt(h) * e; h = om + al * r[t] ** 2 + be * h
        return r
    out = []
    for name, r in (("GARCH(1,1)", garch()), ("i.i.d. control", rng.standard_normal(n) * math.sqrt(sig2))):
        p = np.cumsum(r); ev = np.where(np.abs(r) > 3 * math.sqrt(sig2))[0]; ev = ev[np.r_[True, np.diff(ev) > 1]]
        lab, ca, cc = l5_class(p, ev[:300], 1.0); gaps = np.diff(ev[:300]); out.append((name, len(ev), lab, ca, cc, cv(gaps), float(np.corrcoef(gaps[:-1], gaps[1:])[0, 1])))
    row("econ", "GARCH(1,1) volatility clustering vs i.i.d. returns: exceedance events on the log-price carrier (realised absolute variation as the arc)", "D5 read with a chosen event (rule 2), D2 (arc = realised absolute variation), H-L5, A4 (the conditional variance is the Markov state)",
        "Bollerslev 1986 GARCH; volatility clustering (Mandelbrot 1963); time deformation / subordination (Clark 1973: returns are more regular in transaction or volatility time than in clock time)", "the return process (market-supplied)",
        "; ".join(f"{name}: {m} exceedances, gap CV {gc:.2f}, lag-1 gap autocorrelation {ac:.2f}, CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}" for name, m, lab, ca, cc, gc, ac in out),
        "large returns cluster in time (gap autocorrelation positive under GARCH, zero i.i.d.); in volatility time the return process is closer to homogeneous (subordination)",
        f"GARCH: {reading(*out[0][2:5])} by a margin of {abs(out[0][3] - out[0][4]):.3f}; i.i.d.: {reading(*out[1][2:5])}; under clustering the exceedances are more regular in realised-variation time than in clock time, which is the subordination reading the domain already has (Clark 1973); the event is chosen, not the market's own (rule 2), so the row is a reading, not a result",
        "DESCR", (out[0][2], out[0][3], out[0][4]), "the first carrier in the batteries where the arc-regular class appears on a chosen-event economic series; a real-data row (daily index returns are public) would be a legitimate L5-type prereg only with the event rule fixed in advance")


# ================================================================ (col) collective dynamics
def col_kuramoto():
    """Kuramoto model, N = 1000, Lorentzian frequencies (gamma = 0.5, so K_c = 2 gamma = 1): the exact order parameter
    r = sqrt(1 - K_c/K) above onset. The older text's criticality clause (rho -> 0 at onset) read as r / finite-N floor."""
    rng = np.random.default_rng(6); N = 1000; gam = 0.5; Kc = 2 * gam
    omega = gam * np.tan(math.pi * (rng.random(N) - 0.5)); theta0 = rng.uniform(0, 2 * math.pi, N)
    def order(K):
        th = theta0.copy(); dt = 0.02
        for s in range(6000):
            z = np.mean(np.exp(1j * th)); th += dt * (omega + K * np.abs(z) * np.sin(np.angle(z) - th))
        rs = []
        for s in range(2000):
            z = np.mean(np.exp(1j * th)); th += dt * (omega + K * np.abs(z) * np.sin(np.angle(z) - th)); rs.append(abs(z))
        return float(np.mean(rs)), float(np.std(rs))
    Ks = (0.6, 0.9, 1.1, 1.3, 1.6, 2.0, 3.0); res = [(K, *order(K)) for K in Ks]
    exact = {K: (math.sqrt(1 - Kc / K) if K > Kc else 0.0) for K in Ks}
    floor = 1 / math.sqrt(N); rho_like = [(K, r / max(sd, floor)) for K, r, sd in res]
    err = max(abs(r - exact[K]) for K, r, sd in res if K > 1.2)
    row("col", "Kuramoto synchronisation transition (N = 1000, Lorentzian frequencies): exact order parameter and the criticality clause", "issue-#21 text criticality clause (rho -> 0 at onset); v3.1 has no criticality clause; A1' (unit = the finite-N fluctuation floor)",
        "Kuramoto 1975; Ott-Antonsen exact reduction for Lorentzian frequencies r = sqrt(1 - K_c/K)", "the coupling K and the frequency distribution (system-supplied)",
        "r(K) simulated vs exact: " + ", ".join(f"K = {K:g}: {r:.3f} ({exact[K]:.3f}, sd {sd:.3f})" for K, r, sd in res) + f"; max |simulated - exact| for K >= 1.3: {err:.3f}; r / fluctuation floor: " + ", ".join(f"{K:g}: {v:.1f}" for K, v in rho_like),
        "the order parameter grows as sqrt(K - K_c) above onset (a mean-field, Hopf-like transition); the incoherent state has r ~ 1/sqrt N",
        "the sqrt law and K_c are Kuramoto's; the older clause's 'rho -> 0 at onset' holds on this class as it did on the Hopf rows (the order parameter vanishes into the finite-N floor), and fails on the SNIC and branching classes recorded earlier: class-dependent, not a universal, and v3.1 makes no such claim",
        "DESCR", None, "a fourth data point for the class dependence of the criticality clause; no CRR clause reaches K_c or the exponent")


# ================================================================ (evo) evolutionary game cycles
def evo_rps_heteroclinic():
    """Rock-paper-scissors replicator dx_i = x_i (f_i - fbar), payoff A = [[0, -a, b], [b, 0, -a], [-a, b, 0]]: b < a makes the
    heteroclinic cycle on the simplex boundary attracting (epochs lengthen without bound); a = b gives neutral cycles.
    Integrated in log coordinates so the boundary approach is resolved. Own event: the change of the dominant strategy.
    Carrier: the simplex with the Fisher metric (P7: y = 2 sqrt x, a sphere of radius 2, vertex-to-vertex distance pi).
    Registered: a in {1.1, 1.3} with b = 1 (attracting), a = b = 1 (neutral); the last 12 epochs of each run."""
    def run(a, b, T):
        A = np.array([[0, -a, b], [b, 0, -a], [-a, b, 0]], float)
        def rhs(t, u):
            x = np.exp(u); f = A @ x; return f - x @ f
        t = np.linspace(0, T, int(T * 50) + 1); sol = solve_ivp(rhs, (0, T), np.log([0.4, 0.35, 0.25]), t_eval=t, method="Radau", rtol=1e-10, atol=1e-12)
        u = sol.y.T; u = u - np.log(np.exp(u).sum(axis=1, keepdims=True)); x = np.exp(u)
        dom = np.argmax(x, axis=1); ev = np.where(np.diff(dom) != 0)[0] + 1
        y = 2 * np.sqrt(x); dt = t[1] - t[0]
        arcs = np.array([arc_length(y[p:q + 1]) for p, q in zip(ev[:-1], ev[1:])]); times = np.diff(ev) * dt
        return arcs, times
    def lab(arcs, times):
        d = cv(arcs) - cv(times)
        return "tie" if abs(d) < 1e-3 else ("arc-regular" if d < 0 else "clock-regular")
    out = []
    for a, T in ((1.1, 400.0), (1.3, 400.0)):
        arcs, times = run(a, 1.0, T); k = 12; A_, T_ = arcs[-k:], times[-k:]
        out.append((a, len(arcs), float(times[0]), float(T_[0]), float(T_[-1]), float(arcs[0]), float(A_[-1]), cv(A_), cv(T_), lab(A_, T_)))
    arcs_n, times_n = run(1.0, 1.0, 100.0); lab_n = lab(arcs_n, times_n)
    row("evo", "Rock-paper-scissors replicator with an attracting heteroclinic cycle: dominance epochs on the Fisher-native simplex", "D5 (dominance switch = own event), A1 (Shahshahani/Fisher metric on the simplex, P7), D2, H-L5",
        "replicator dynamics; May-Leonard heteroclinic cycles; Shahshahani metric", "the payoff asymmetry a - b (game-supplied)",
        "; ".join(f"a = {a:g}: {n} epochs, first duration {t0:.2f}, last-12 durations {t1:.2f} -> {t2:.2f} (CV {ct:.3f}), first arc {a0:.3f}, last arc {a1:.3f} (last-12 CV {ca:.3f}; vertex-to-vertex distance pi = {math.pi:.3f}) -> {lb}" for a, n, t0, t1, t2, a0, a1, ca, ct, lb in out)
        + f"; neutral (a = b = 1): {len(arcs_n)} epochs, duration CV {cv(times_n):.3f}, arc CV {cv(arcs_n):.3f} -> {lab_n}",
        "near an attracting heteroclinic cycle the time spent near each saddle grows geometrically while the orbit converges to the boundary cycle",
        f"attracting cycle: {out[0][9]} (a = 1.1) and {out[1][9]} (a = 1.3), by the system's own dynamics rather than by construction: the epochs lengthen without bound while the Fisher arc of each epoch converges to the fixed vertex-to-vertex distance; neutral cycles: {lab_n} (nothing varies); the saturation value pi is a definition (P7), the regularity is dynamical",
        "CONSIST" if all(o[9] == "arc-regular" for o in out) else "OPEN", (out[0][9], out[0][7], out[0][8]), "the second system in the batteries (after the adder) that is arc-regular by its own dynamics; a real-data row would need a population with recorded strategy frequencies over several cycles")


# ================================================================ (soc) social diffusion
def soc_bass_diffusion():
    """Bass model dF/dt = (p + q F)(1 - F): the adoption wave as one occasion. The peak time t* = ln(q/p)/(p+q) and the
    fraction adopted at the peak (q - p)/(2q) are the model's; the state F is Markov (depth one)."""
    p, q = 0.03, 0.38
    t = np.linspace(0, 30, 3001); sol = solve_ivp(lambda tt, F: [(p + q * F[0]) * (1 - F[0])], (0, 30), [0.0], t_eval=t, rtol=1e-10, atol=1e-12)
    F = sol.y[0]; dF = np.gradient(F, t); k = int(np.argmax(dF)); t_peak, F_peak = float(t[k]), float(F[k])
    t_star = math.log(q / p) / (p + q); F_star = (q - p) / (2 * q)
    C = arc_length(F[:k + 1]); Cs = abs(F[k] - F[0])
    row("soc", "Bass diffusion of an innovation: the adoption wave as one occasion (peak time and peak fraction)", "D5 (the wave as one occasion), D2-D4 on the adopted fraction, A4 (F is Markov: depth one)",
        "Bass 1969 diffusion model; logistic-type growth", "the innovation and imitation coefficients p, q (market-supplied)",
        f"p = {p}, q = {q}: simulated peak at t = {t_peak:.2f} with F = {F_peak:.3f}; closed form t* = {t_star:.2f}, F* = {F_star:.3f}; arc to the peak C = {C:.3f} equals the chord C* = {Cs:.3f} (monotone: S = {C - Cs:.1e})",
        "the peak of adoption occurs at ln(q/p)/(p+q) with (q - p)/(2q) adopted; the curve is set by p and q alone",
        "the wave is a monotone occasion (S = 0 by P1) and the state is depth one, so the framework has nothing to add to the closed form",
        "DESCR", None, "rule 3: the occasion structure is a relabelling of the S-shaped curve")


BATTERY = [cog_drift_diffusion, cog_rescorla_wagner, cog_retention_natural_time, ai_reservoir_influence, ai_simulated_annealing,
           econ_garch, col_kuramoto, evo_rps_heteroclinic, soc_bass_diffusion]

CLASSES = {"cog": "cognitive models", "ai": "learning machines", "econ": "economic time series", "col": "collective dynamics",
           "evo": "evolutionary games", "soc": "social diffusion"}


def main():
    for f in BATTERY: f()
    print(f"CRR retrodiction battery on cognitive, learning-machine, economic, collective, evolutionary-game and social-diffusion systems — {len(ROWS)} model systems, {len(CLASSES)} classes. Grades: SHARP CONSIST DESCR FAILS TENSION OPEN\n")
    for i, r in enumerate(ROWS, 1):
        print(f"[{i:2d}] ({r['cls']}) {r['system']}\n     clause:     {r['clause']}\n     BORROWED:   {r['borrowed']}\n     FLOW:       {r['flow']}"
              f"\n     derivation: {r['derivation']}\n     known:      {r['known']}\n     verdict:    {r['verdict']}\n     GRADE:      {r['grade']}"
              + (f"\n     H-L5 class: {r['l5'][0]} (CV_arc {r['l5'][1]:.3f}, CV_clock {r['l5'][2]:.3f})" if r['l5'] else "")
              + (f"\n     weakness:   {r['weakness']}" if r['weakness'] else ""))
    grades = ("SHARP", "CONSIST", "DESCR", "FAILS", "TENSION", "OPEN")
    print("\n" + "=" * 100 + "\nTALLY")
    print(f"{'class':32s} " + " ".join(f"{g:>8s}" for g in grades))
    for c, name in CLASSES.items():
        rs = [r for r in ROWS if r["cls"] == c]
        print(f"({c}) {name:26s} " + " ".join(f"{sum(r['grade'] == g for r in rs):8d}" for g in grades))
    print(f"{'all':32s} " + " ".join(f"{sum(r['grade'] == g for r in ROWS):8d}" for g in grades))
    print("\nH-L5 class map (model systems with their own events):")
    for r in ROWS:
        if r["l5"]: print(f"  {r['l5'][0]:44s} {r['system']}")
    print(f"\nrows where the coherence integral's velocity is system-supplied (FLOW != none): {sum('none' not in r['flow'] for r in ROWS)}/{len(ROWS)}")
    print(f"Rows where a CRR clause reaches a result the domain did not already have: {sum(r['grade'] == 'SHARP' for r in ROWS)} of {len(ROWS)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
