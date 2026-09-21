"""Synthesis batch 16: rows 76-80 of QUEUE.md (prompt-log entry 61). Cognitive-collective battery [3] retention under
variable-rate interference, forgetting in natural time vs clock time, P5 (DESCR); [5] simulated annealing of a two-level
system, three schedules of identical Fisher length (CONSIST); [6] GARCH(1,1) volatility clustering vs i.i.d. returns,
exceedance events (DESCR); [7] Kuramoto synchronisation transition, N = 1000, Lorentzian frequencies (DESCR); [8]
rock-paper-scissors replicator with an attracting heteroclinic cycle (CONSIST; synthesis.py row 7 already re-read its
epoch arc as the simplex edge length pi, so this row reads the boundary approach under A1'/D1 instead). All five source
rows are in theory/retrodictions/cognitive_collective.txt; their models are re-implemented here (nothing imported from
the battery scripts). Deterministic (fixed seeds, fixed grids, explicit RK4, an exact zero-order-hold integrator for the
linear relaxation); no data file opened (R2). Run:
  uv run python theory/retrodictions/synthesis_batches/batch_16.py
"""
import math
import sys

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import norm

from crr.instrument.core import cv, regularity
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

SRC = "theory/retrodictions/cognitive_collective.txt"


def _word(cond, yes, no):
    return yes if cond else no


def _agree(a, b, tol=TOL_G):
    return _word(rel(a, b) <= tol, "agree", "differ")


def _r2(y, X):
    """R^2 of y on a linear fit in the columns of X (with intercept); the source battery's estimator."""
    X = np.atleast_2d(np.asarray(X, float)); X = X.T if X.shape[0] < X.shape[1] else X
    A = np.c_[X, np.ones(len(X))]; y = np.asarray(y, float)
    coef, *_ = np.linalg.lstsq(A, y, rcond=None); res = y - A @ coef
    return float(1 - res.var() / y.var())


# ---------------------------------------------------------------- 76 [3] retention in natural time: Jost's law as a rate property
def r1():
    rho, lam_w, lam_s = 20.0, 4.0, 0.4                              # the source's unit and wake / sleep interference rates (per hour)
    K, c = 4.0, 1.0                                                  # the trace-time carrier: lambda = K/(t + c), lambda(0) = the wake rate

    def rate(t):
        return lam_w if (t % 24.0) < 16.0 else lam_s

    # the source row's model, reproduced (seed 3, 300 items, delays 0.5-24 h)
    rng = np.random.default_rng(3); n_items = 300
    t24 = np.linspace(0, 24.0, 2401); lam24 = np.array([rate(t) for t in t24])
    A24 = np.concatenate([[0], np.cumsum(0.5 * (lam24[1:] + lam24[:-1]) * np.diff(t24))])
    delays = rng.uniform(0.5, 24.0, n_items); Ad = np.interp(delays, t24, A24)
    R = np.exp(-Ad / rho) * np.exp(0.05 * rng.standard_normal(n_items))
    r2_nat, r2_clk = _r2(np.log(R), Ad), _r2(np.log(R), delays)

    # the two carriers over 72 h, 1000 samples per hour
    tt = np.linspace(0, 72.0, 72001); dt = tt[1] - tt[0]
    lam_env = np.array([rate(t) for t in tt])
    A_env = np.concatenate([[0], np.cumsum(0.5 * (lam_env[1:] + lam_env[:-1]) * np.diff(tt))])   # environment time: the same stream for every trace
    A_tr = lambda s: K * np.log((s + c) / c)                                                        # trace time: the rate decays since the trace's own learning

    def ln_R_env(t_learn):
        return -(A_env - np.interp(t_learn, tt, A_env)) / rho

    def ln_R_tr(t_learn):
        s = np.clip(tt - t_learn, 0.0, None); return -A_tr(s) / rho

    def frate(lnR, t):                                               # instantaneous clock-time forgetting rate -d ln R / dt, central difference
        i = int(round(t / dt)); return float(-(lnR[i + 1] - lnR[i - 1]) / (2 * dt))

    t_eval, t_old, t_young = 25.0, 0.0, 24.0                         # ages 25 h and 1 h at the moment of evaluation
    jost_env = frate(ln_R_env(t_old), t_eval) / frate(ln_R_env(t_young), t_eval)
    jost_tr = frate(ln_R_tr(t_old), t_eval) / frate(ln_R_tr(t_young), t_eval)
    beta, psi = 1.0 / c, K / rho                                     # Wickelgren power law R = (1 + beta t)^-psi: rate psi beta / (1 + beta t)
    wick = (1 + beta * (t_eval - t_young)) / (1 + beta * (t_eval - t_old))
    phase_ratio = frate(ln_R_env(12.0), 20.0) / frate(ln_R_env(0.0), 8.0)   # equal age 8 h: one evaluated asleep, one awake
    rate_ratio = lam_s / lam_w

    def local_exp(lnR, t):                                           # -d ln R / d ln(t + c)
        return (t + c) * frate(lnR, t)

    ts = (4.0, 8.0, 20.0, 28.0)
    le_env = [local_exp(ln_R_env(0.0), t) for t in ts]; le_tr = [local_exp(ln_R_tr(0.0), t) for t in ts]

    def fit_psi(lnR, w):
        m = (tt >= 0.5) & (tt <= w); return float(-np.polyfit(np.log((tt[m] + c) / c), lnR[m], 1)[0])

    ws = (8.0, 24.0, 72.0)
    psi_env = [fit_psi(ln_R_env(0.0), w) for w in ws]; psi_tr = [fit_psi(ln_R_tr(0.0), w) for w in ws]
    TOL_FD = 1e-6                                                    # tolerance for the central-difference rate estimator (truncation error below 1e-7 on this grid)
    d_env, d_phase, d_tr = rel(jost_env, 1.0), rel(phase_ratio, rate_ratio), rel(jost_tr, wick)
    check = d_env <= TOL_FD and d_phase <= TOL_FD and d_tr <= TOL_FD
    out = outcome(crr=jost_tr, null=1.0, domain=wick, check=check)
    return make_row("cog",
        f"Retention R = exp(-A/rho) in natural time (A = the count of interference events since learning, rho = {rho:g}) on two interference carriers: the source's environment-time carrier (wake {lam_w:g}/h for 16 h, sleep {lam_s:g}/h for 8 h, the same stream for every trace) and a trace-time carrier lambda = K/(t + c) with K = {K:g}/h, c = {c:g} h (the rate decays since the trace's own learning: P5's p = 1)",
        source=f"{SRC} [3] (DESCR)",
        Q="under exponential retention in natural time the instantaneous clock-time forgetting rate of a trace is lambda(now)/rho, so Jost's second law (of two traces of equal strength the older forgets more slowly) holds iff the interference rate a trace sees decays with the trace's own age: on the environment-time carrier two traces of ages 1 h and 25 h forget at the same rate at every moment (ratio 1, no Jost's law) and the sleep/wake asymmetry is the rate ratio lambda_s/lambda_w independent of rho; on the trace-time carrier the ratio is (t_young + c)/(t_old + c), which is the Wickelgren power law's own ratio",
        ingredient="A1'/D1 (one interference event = one step; time is natural time A(t)), with P5's calculus on it (P5 is standard calculus, not CRR-proper); O1 leaves rho a fit",
        null="the clock: retention exponential in clock time, exp(-t/tau), whose Jost ratio is 1 on every carrier",
        domain="Jost 1897 (second law); Wickelgren 1974 power law R = (1 + beta t)^-psi, whose forgetting rate psi beta/(1 + beta t) gives the Jost ratio (1 + beta t_young)/(1 + beta t_old); Wixted 2004 (Jost's law as the signature of a decelerating forgetting function); Anderson & Schooler 1991 (the power law of forgetting mirrors the environment's own recurrence statistics); Jenkins & Dallenbach 1924 (sleep/wake asymmetry). Named only, not fetched (R10)",
        numbers=(f"source model reproduced ({n_items} items, delays 0.5-24 h): R^2 of log retention on natural time {r2_nat:.3f}, on clock time {r2_clk:.3f}; "
                 f"environment-time carrier: forgetting-rate ratio old (25 h) / young (1 h) at the same moment = {jost_env:.4f}; equal age 8 h evaluated asleep / awake = {phase_ratio:.4f} (lambda_s/lambda_w = {rate_ratio:.4f}); "
                 f"local exponent -d ln R/d ln(t + c) at t = {', '.join(f'{t:g}' for t in ts)} h: {', '.join(f'{v:.4f}' for v in le_env)} (it cycles with the phase of day); power-law exponent fitted over 0.5-{', 0.5-'.join(f'{w:g}' for w in ws)} h: {', '.join(f'{v:.4f}' for v in psi_env)} (it drifts with the window); "
                 f"trace-time carrier: ratio old / young = {jost_tr:.4f} (Wickelgren with beta = 1/c = {beta:g}/h, psi = K/rho = {psi:.4f}: {wick:.4f}); local exponent at the same t: {', '.join(f'{v:.4f}' for v in le_tr)} (constant K/rho = {psi:.4f}); fitted exponent over the same windows: {', '.join(f'{v:.4f}' for v in psi_tr)}"),
        tg=f"Jost ratio {jost_tr:.4f} (natural time, trace-time carrier) vs null {1.0:.4f} (clock-time exponential): {_agree(jost_tr, 1.0)}",
        tn=f"the Wickelgren power law gives {wick:.4f}: the domain {_word(rel(jost_tr, wick) <= TOL_N, 'has', 'does not have')} Q",
        tc=f"environment carrier ratio = 1 within {TOL_FD:g} (relative difference {d_env:.1e}: {_word(d_env <= TOL_FD, 'yes', 'no')}), asleep/awake ratio = lambda_s/lambda_w within {TOL_FD:g} ({d_phase:.1e}: {_word(d_phase <= TOL_FD, 'yes', 'no')}), trace-time ratio = Wickelgren's within {TOL_FD:g} ({d_tr:.1e}: {_word(d_tr <= TOL_FD, 'yes', 'no')}): {_word(check, 'holds', 'fails')}",
        out=out,
        reading=(f"what natural time adds on this carrier beyond the Omori rows (batch 04 row 1, batch 07 row 5: the compensator homogenises the events) is a diagnostic: Jost's law is not a property of the trace but of which clock the interference keeps; on the source's environment-time carrier P5 predicts no Jost's law (ratio {jost_env:.4f}) and the sleep/wake asymmetry as a bare rate ratio ({phase_ratio:.4f}), and the forgetting curve is not a power law (fitted exponent {psi_env[0]:.2f} -> {psi_env[-1]:.2f} across windows); Jost's law appears only where the rate decays since the trace's own learning (ratio {jost_tr:.4f}), and there P5's p = 1 is the Wickelgren power law, whose own rate ratio it is; "
                 f"the domain has both halves (Wixted 2004 reads Jost's law off a decelerating forgetting function; Anderson & Schooler 1991 derive the deceleration from the environment's recurrence rate), so the source row's 'restatement of the interference hypothesis' stands with the Jost reading added and the outcome is {out}"),
        weakness="rho is not fixed (O1), so the trace-time exponent K/rho is a fit and only ratios are rho-free; the trace-time carrier's decaying rate is a model of item-specific interference (context fading), not of the environment's event stream, and which of the two a memory sees is the empirical question the source row said no row has opened (retention data with recorded event rates, absent from data/SEEN.md); the environment-time result is exact because every trace reads the same A(t)",
        elegance="Forgetting keeps a clock, and the question is whose: if the world's events do the erasing, an old memory and a new one fade at the same rate tonight; if the erasing comes from the memory's own fading context, the old one fades slower. Jost's old law is the tell, with no knobs.",
        child="Suppose every noisy thing that happens rubs a little off your memories. If the noise comes from the world, an old memory and a new one get rubbed at the same rate on the same day. If the noise comes from things that look like the memory itself, those get rarer as time goes on, so the old memory is safer than the new one. Whether old memories fade slower tells you where the rubbing comes from.")


# ---------------------------------------------------------------- 77 [5] annealing: the normalised step among equal-length schedules
def r2():
    D, tau_r, b0, b1 = 1.0, 1.0, 0.2, 5.0                            # the source's two-level system and endpoints
    p_eq = lambda b: 1.0 / (1.0 + np.exp(b * D))
    g = lambda b: D * D * p_eq(b) * (1 - p_eq(b))                    # Fisher metric g_bb = Var(E)
    bs = np.linspace(b0, b1, 40001)
    cum = np.concatenate([[0], np.cumsum(np.sqrt(g(0.5 * (bs[1:] + bs[:-1]))) * np.diff(bs))]); L = float(cum[-1])
    sched = {"linear in T": lambda s: 1.0 / (1.0 / b0 + s * (1.0 / b1 - 1.0 / b0)),
             "linear in beta": lambda s: b0 + s * (b1 - b0),
             "constant Fisher speed": lambda s: np.interp(s * L, cum, bs)}

    def integrate(f, tau, n):
        """dp/dt = -(p - p_eq(beta(t)))/tau_r with p_eq held at its mid-step value: exact zero-order-hold step."""
        from scipy.signal import lfilter
        dt = tau / n; pe_mid = p_eq(f((np.arange(n) + 0.5) / n)); a = math.exp(-dt / tau_r)
        p = lfilter([1 - a], [1, -a], pe_mid, zi=[a * p_eq(b0)])[0]
        pe_end = p_eq(f((np.arange(n) + 1.0) / n))
        return float(np.sum(dt * (p - pe_end) ** 2 / (pe_end * (1 - pe_end))))

    def speed_cv(f, tau, n=40000):
        s = (np.arange(n) + 0.5) / n; b = f(s); v = np.sqrt(g(b)) * np.abs(np.gradient(b, s) / tau)
        return float(v.std() / v.mean())

    taus = (40.0, 400.0, 4000.0); res = {}
    for tau in taus:
        n = int(1000 * tau); res[tau] = {k: integrate(f, tau, n) for k, f in sched.items()}
    cvs = {k: speed_cv(f, taus[0]) for k, f in sched.items()}       # the speed profile's CV is duration-free
    bound = {tau: tau_r ** 2 * L ** 2 / tau for tau in taus}
    tau_reg = 400.0; crr = res[tau_reg]["constant Fisher speed"]; null = res[tau_reg]["linear in beta"]; dom = bound[tau_reg]
    least = all(min(res[tau], key=res[tau].get) == "constant Fisher speed" for tau in taus)
    tau_slow = 4000.0
    ratio_ok = all(rel(res[tau_slow][k] / res[tau_slow]["constant Fisher speed"], 1 + cvs[k] ** 2) <= 0.02 for k in ("linear in T", "linear in beta"))
    check = least and ratio_ok and rel(crr, dom) <= TOL_N
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("ai",
        f"Simulated annealing of a two-level system (gap D = {D:g}, relaxation time tau_r = {tau_r:g}) from beta = {b0:g} to {b1:g} along three schedules of identical Fisher length L = {L:.4f}, integrated exactly (zero-order hold) at durations tau = {', '.join(f'{t:g}' for t in taus)}; the source's tau = {taus[0]:g} and a registered slow arm tau = {tau_reg:g}",
        source=f"{SRC} [5] (CONSIST)",
        Q="among cooling schedules of equal Fisher length, the one that advances by equal Fisher-normalised steps per unit clock time (H-EQ's Omega = 1 read as a schedule: equal pull per tick in the Fisher norm) has the least lag, tau_r^2 L^2/tau in the slow limit, and any other schedule of the same length carries (1 + CV(v)^2) times it, CV(v) the coefficient of variation of its Fisher speed",
        ingredient="H-EQ (the normalised step: equal Fisher-norm displacement per unit time, Omega = 1) read as a schedule; D2 supplies L (not proper)",
        null="the un-normalised step: equal beta per tick (linear in beta), the plain schedule with the same endpoints and the same length",
        domain="Salamon & Berry 1983 (dissipation >= L^2 tau_r/tau by Cauchy-Schwarz, equality at constant thermodynamic speed); Salamon, Nulton, Andresen et al. 1988 (constant thermodynamic speed annealing); Sivak & Crooks 2012. Named only, not fetched (R10)",
        numbers=("; ".join(f"tau = {tau:g}: lag integral " + ", ".join(f"{k} {res[tau][k]:.6f}" for k in sched) + f"; bound tau_r^2 L^2/tau = {bound[tau]:.6f}; least lag: {min(res[tau], key=res[tau].get)}" for tau in taus)
                 + "; Fisher-speed CV: " + ", ".join(f"{k} {cvs[k]:.4f}" for k in sched)
                 + f"; lag ratios to the constant-speed schedule at tau = {tau_slow:g}: " + ", ".join(f"{k} {res[tau_slow][k] / res[tau_slow]['constant Fisher speed']:.4f} (1 + CV(v)^2 = {1 + cvs[k] ** 2:.4f})" for k in ("linear in T", "linear in beta"))
                 + f"; at tau = {taus[0]:g}: " + ", ".join(f"{k} {res[taus[0]][k] / res[taus[0]]['constant Fisher speed']:.4f}" for k in ("linear in T", "linear in beta"))
                 + f"; constant-speed lag over the bound: " + ", ".join(f"tau = {tau:g}: {res[tau]['constant Fisher speed'] / bound[tau]:.4f}" for tau in taus)),
        tg=f"lag of the normalised-step schedule {crr:.6f} vs null (equal beta per tick) {null:.6f} at tau = {tau_reg:g}: {_agree(crr, null)}",
        tn=f"Salamon-Berry's bound tau_r^2 L^2/tau = {dom:.6f} at tau = {tau_reg:g}: the domain {_word(rel(crr, dom) <= TOL_N, 'has', 'does not have')} Q",
        tc=f"constant speed least at every tau ({_word(least, 'yes', 'no')}), lag ratios within 2 % of 1 + CV(v)^2 at tau = {tau_slow:g} ({_word(ratio_ok, 'yes', 'no')}), constant-speed lag within 1 % of the bound at tau = {tau_reg:g} ({_word(rel(crr, dom) <= TOL_N, 'yes', 'no')}): {_word(check, 'holds', 'fails')}",
        out=out,
        reading=(f"the normalised step does work against the plain schedule (T-G: {crr:.6f} against {null:.6f}) and what it produces is the domain's own theorem: the Cauchy-Schwarz bound written in the length of the path and its duration, saturated at constant thermodynamic speed, with the excess of any other schedule of the same length carried by the variance of its speed (ratios {res[tau_slow]['linear in T'] / res[tau_slow]['constant Fisher speed']:.4f} and {res[tau_slow]['linear in beta'] / res[tau_slow]['constant Fisher speed']:.4f} against 1 + CV^2 = {1 + cvs['linear in T'] ** 2:.4f} and {1 + cvs['linear in beta'] ** 2:.4f}); "
                 f"the source row's 'the length cannot rank schedules of equal length' is exact, and the quantity that ranks them is a speed profile the domain named in 1983-88; batch 06 row 1 found the same theorem from the path-against-endpoint side; the outcome is {out}"),
        weakness=f"the reading of H-EQ as 'equal Fisher step per tick' is a reading, not a clause (H-EQ balances two gradients, not a schedule against its clock); at the source's duration tau = {taus[0]:g} the constant-speed lag sits {100 * (res[taus[0]]['constant Fisher speed'] / bound[taus[0]] - 1):.1f} % above the slow-limit bound and the linear-in-T ratio {res[taus[0]]['linear in T'] / res[taus[0]]['constant Fisher speed']:.2f} is off 1 + CV^2 = {1 + cvs['linear in T'] ** 2:.2f}, so the theorem is the slow-driving one and the registered arm is tau = {tau_reg:g}; one relaxation time, constant along the path (the two-dial trap of batch 10 row 5 is where that fails)",
        elegance="Three cooling recipes cover the same distance in the system's own ruler; the one that moves the same small amount every second wastes least, and every other recipe pays exactly for how uneven its pace is. A rule with one number, the unevenness of the pace.",
        child="Three ways to cool something down the same distance in the same time. The way that goes at one steady pace, measured by how much the thing can actually feel, wastes the least. Rushing some parts and dawdling others always costs extra, and the extra is just how uneven the pace was.")


# ---------------------------------------------------------------- 78 [6] GARCH exceedances in the system's own unit
def r3():
    n, om, al, be, thr = 1600000, 1e-6, 0.09, 0.90, 3.0            # the source's GARCH(1,1) (seed 5), 40x its length; the source's 3-sigma threshold
    sig2 = om / (1 - al - be); rng = np.random.default_rng(5)
    h = sig2; r = np.empty(n); hh = np.empty(n)
    for t in range(n):
        e = rng.standard_normal(); hh[t] = h; r[t] = math.sqrt(h) * e; h = om + al * r[t] ** 2 + be * h
    eps = r / np.sqrt(hh)                                            # returns in the system's own unit: one conditional standard deviation
    p = 2 * norm.cdf(-thr)
    # the domain's value: exceedances of the own unit are i.i.d. Bernoulli(p), gaps geometric, the arc of an occasion (exclusive: the
    # exceedance return is the cut) is a sum of N - 1 i.i.d. |eps| truncated to |eps| <= thr
    Z = 1 - p
    m_in = quad(lambda u: 2 * u * norm.pdf(u), 0, thr)[0] / Z; s2_in = quad(lambda u: 2 * u * u * norm.pdf(u), 0, thr)[0] / Z; v_in = s2_in - m_in ** 2
    EN1, VN1 = (1 - p) / p, (1 - p) / p ** 2
    cv_arc_th = math.sqrt(EN1 * v_in + VN1 * m_in ** 2) / (EN1 * m_in); cv_clk_th = math.sqrt(1 - p); idx_th = cv_clk_th / cv_arc_th
    res = {}
    for name, x, carrier in (("outside unit (3 unconditional sigma)", r / math.sqrt(sig2), np.cumsum(r)),
                             ("own unit (3 conditional sigma)", eps, np.cumsum(eps))):
        ev = np.where(np.abs(x) > thr)[0]
        rr = regularity(carrier, ev, sigma=1.0, dt=1.0, n_boot=500, seed=0, segment_end="exclusive")
        gaps = np.diff(ev); ac = float(np.corrcoef(gaps[:-1], gaps[1:])[0, 1])
        blocks = (np.abs(x) > thr).astype(float).reshape(-1, 100).sum(axis=1); disp = float(blocks.var(ddof=1) / blocks.mean())
        res[name] = dict(n=len(ev), rate=len(ev) / n, cv_gap=cv(gaps), ac=ac, disp=disp, cv_arc=rr["cv_arc"], cv_clock=rr["cv_clock"],
                         idx=rr["cv_clock"] / rr["cv_arc"], diff=rr["diff"], ci=rr["ci95"])
    o, w = res["outside unit (3 unconditional sigma)"], res["own unit (3 conditional sigma)"]
    crr, null, dom = w["idx"], o["idx"], idx_th
    check = abs(w["ac"]) <= 0.05 and abs(w["diff"]) < 0.01 and rel(w["rate"], p) <= 0.1

    def cls(d):
        lab = "tie" if abs(d) < 1e-3 else _word(d < 0, "arc-regular", "clock-regular")
        return lab if (lab == "tie" or abs(d) >= 0.01) else f"{lab} by {abs(d):.4f}, below the 0.01 the source battery treats as a reading"

    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("econ",
        f"GARCH(1,1) daily returns (omega = {om:g}, alpha = {al:g}, beta = {be:g}, persistence {al + be:g}; {n} steps, seed 5) with exceedance events |return| > {thr:g} units, the unit being either the outside constant (the unconditional standard deviation, the source's rule) or the system's own resolvable step (the conditional standard deviation sqrt(h_t), the GARCH state); log-price carrier, exclusive segmentation (the exceedance return is the cut)",
        source=f"{SRC} [6] (DESCR)",
        Q="the volatility clustering of exceedances, and with it the arc-regular class the source row found, belongs to the outside unit: counted in the system's own resolvable step the exceedances are i.i.d. Bernoulli with rate 2 Phi(-3), their gaps are geometric with CV sqrt(1 - p) and no autocorrelation, and the arc-against-clock margin sits below the 0.01 the source battery treats as a reading, at the compound-geometric index",
        ingredient="A1'/D1 (the unit is the system's own resolvable step: one conditional standard deviation, the Markov state of A4), D5 (occasion = interval between own-unit exceedances), H-L5's class claim",
        null="the outside unit: the unconditional standard deviation, the source's rule-2 event, with the same threshold and segmentation",
        domain="the GARCH definition (Bollerslev 1986: r_t = sqrt(h_t) eps_t with eps_t i.i.d. N(0, 1), so exceedances of the conditional scale are Bernoulli(2 Phi(-3)) and their gaps geometric); the standardised-residual diagnostics of the domain (Ljung-Box on eps^2, Engle-Ng) test exactly this; Clark 1973 subordination for the outside-unit reading. Named only, not fetched (R10)",
        numbers=("; ".join(f"{k}: {v['n']} events (rate {v['rate']:.5f}), gap CV {v['cv_gap']:.4f}, lag-1 gap autocorrelation {v['ac']:+.4f}, dispersion index of counts per 100 steps {v['disp']:.4f}, CV(arc) {v['cv_arc']:.4f}, CV(clock) {v['cv_clock']:.4f}, class index CV(clock)/CV(arc) {v['idx']:.4f}, CV(arc) - CV(clock) {v['diff']:+.4f} with paired-bootstrap 95 % CI [{v['ci'][0]:+.4f}, {v['ci'][1]:+.4f}]: {cls(v['diff'])}" for k, v in res.items())
                 + f"; domain's value in the own unit: p = 2 Phi(-{thr:g}) = {p:.5f}, gap CV sqrt(1 - p) = {cv_clk_th:.4f}, interior |eps| mean {m_in:.4f} and variance {v_in:.4f}, CV(arc) {cv_arc_th:.4f}, class index {idx_th:.4f}, dispersion index 1 - p = {1 - p:.4f}"),
        tg=f"class index {crr:.4f} (own unit) vs null {null:.4f} (outside unit): {_agree(crr, null)}",
        tn=f"the compound-geometric index of the GARCH definition gives {dom:.4f}: the domain {_word(rel(crr, dom) <= TOL_N, 'has', 'does not have')} Q",
        tc=f"own-unit lag-1 autocorrelation within 0.05 of 0 ({_word(abs(w['ac']) <= 0.05, 'yes', 'no')}), |CV(arc) - CV(clock)| below 0.01 ({_word(abs(w['diff']) < 0.01, 'yes', 'no')}), rate within 10 % of 2 Phi(-3) ({_word(rel(w['rate'], p) <= 0.1, 'yes', 'no')}): {_word(check, 'holds', 'fails')}",
        out=out,
        reading=(f"the unit does work (T-G: index {crr:.4f} against {null:.4f}; dispersion {w['disp']:.2f} against {o['disp']:.2f}) and what it removes is the source row's reading: the clustering, the positive gap autocorrelation ({o['ac']:+.3f}) and the arc-regular margin ({o['diff']:+.3f}, CI excluding 0) all belong to measuring returns against a constant the system does not keep; in its own step the process is the i.i.d. innovation sequence the model is built from, its exceedances are memoryless and the class margin CV(arc) - CV(clock) is {w['diff']:+.4f} against the definition's {cv_arc_th - cv_clk_th:+.4f}, {_word(abs(w['diff']) < 0.01 and abs(cv_arc_th - cv_clk_th) < 0.01, 'both', 'not both')} below the 0.01 the source battery treats as a reading, the index sitting at the value the definition fixes ({dom:.4f}); "
                 f"this is the statement the domain's residual diagnostics make (standardised residuals carry no clustering), so the source's 'subordination reading the domain already has' becomes, under A1', 'the domain's own definition of the model', and the outcome is {out}; the same move as batch 04 row 1 (the compensator homogenises an Omori sequence) on an economic carrier"),
        weakness="h_t is latent on real data and would have to come from a fitted model, so the own unit is the model's unit and a prereg on daily index returns would be testing the fit (which is what the domain's diagnostics do); one persistence, one threshold, Gaussian innovations (the domain's value assumes them); the outside-unit index here is exclusive and unclustered, so it is not the source's 1.243, which was inclusive and declustered on 300 events",
        elegance="Measure a market's jumps against a ruler it does not keep and they come in clusters; measure them against its own ruler, the size of today's wobble, and they come one at a time with no memory. The clustering was the ruler's.",
        child="On some days a market jiggles a lot and on others hardly at all. If you call a move 'big' by one fixed ruler, the big moves bunch up on the jiggly days. If instead you call it big compared with that day's own jiggle, the big moves are spread out at random, like coin flips. The bunching came from using the wrong ruler.")


# ---------------------------------------------------------------- 79 [7] Kuramoto with an age-weighted mean field
def r4():
    N, gam, tau_m, omega0 = 1000, 0.5, 1.0, 1.0                      # the source's N and Lorentzian width; registered: P3 memory tau_m, centre omega0
    Kc0 = 2 * gam; rng = np.random.default_rng(6)
    omega_c = gam * np.tan(math.pi * (rng.random(N) - 0.5)); theta0 = rng.uniform(0, 2 * math.pi, N)

    def order(K, tau, w0, dt=0.02, n_tr=6000, n_me=2000):
        """theta_i' = omega_i + K |Z| sin(arg Z - theta_i) with Z the mean field (tau = 0) or its P3 age-weighted mean tau Z' = z - Z."""
        th = theta0.copy(); om = omega_c + w0; Z = np.mean(np.exp(1j * th)); rs, ph = [], []
        for s in range(n_tr + n_me):
            z = np.mean(np.exp(1j * th))
            Z = Z + dt * (z - Z) / tau if tau > 0 else z
            th += dt * (om + K * np.abs(Z) * np.sin(np.angle(Z) - th))
            if s >= n_tr:
                rs.append(abs(z)); ph.append(np.angle(z))
        ph = np.unwrap(np.array(ph)); return float(np.mean(rs)), float(np.std(rs)), float((ph[-1] - ph[0]) / (dt * (n_me - 1)))

    def oa_memory(K, tau, w0):
        """Rotating OA solution z = r e^{i Omega t}, Z = z/(1 + i Omega tau): Omega = w0 - Omega tau (K/(1 + Omega^2 tau^2) - gam), r^2 = 1 - 2 gam (1 + Omega^2 tau^2)/K."""
        f = lambda Om: Om - w0 + Om * tau * (K / (1 + (Om * tau) ** 2) - gam)
        Om = brentq(f, -20.0, 20.0); r2 = 1 - 2 * gam * (1 + (Om * tau) ** 2) / K
        return (math.sqrt(r2) if r2 > 0 else 0.0), Om

    Kc_mem = 2 * gam * (1 + (omega0 * tau_m / (1 + gam * tau_m)) ** 2); Om_c = omega0 / (1 + gam * tau_m)

    # the domain's theorem (Lee-Ott-Antonsen: delayed field Z = int h(s) z(t - s) ds, h the exponential kernel): incoherence loses
    # stability to a mode e^{i Omega t} when (K/2) Re hhat(Omega) = gam and Omega = w0 + (K/2) Im hhat(Omega); hhat by quadrature
    hhat = lambda Om: complex(quad(lambda s: np.exp(-s / tau_m) / tau_m * math.cos(Om * s), 0, 60 * tau_m)[0], -quad(lambda s: np.exp(-s / tau_m) / tau_m * math.sin(Om * s), 0, 60 * tau_m)[0])
    Om_dom = brentq(lambda Om: Om - omega0 - gam * hhat(Om).imag / hhat(Om).real, -20.0, 20.0); Kc_dom = 2 * gam / hhat(Om_dom).real

    Ks = (1.2, 1.6, 2.0, 3.0); sim = {}
    for K in Ks:
        sim[K] = dict(mem=order(K, tau_m, omega0), plain=order(K, 0.0, omega0), oa_mem=oa_memory(K, tau_m, omega0), oa_plain=(math.sqrt(max(0.0, 1 - Kc0 / K)), omega0))
    K0 = 2.0; centred = dict(mem=order(K0, tau_m, 0.0), plain=order(K0, 0.0, 0.0), oa=oa_memory(K0, tau_m, 0.0))
    far = all(abs(sim[K]["mem"][0] - sim[K]["oa_mem"][0]) <= 0.03 and abs(sim[K]["mem"][2] - sim[K]["oa_mem"][1]) <= 0.03 for K in (2.0, 3.0))
    below = sim[1.2]["mem"][0] < 0.5 * sim[1.2]["plain"][0]
    inert = abs(centred["mem"][0] - centred["plain"][0]) <= 0.03
    check = far and below and inert
    out = outcome(crr=Kc_mem, null=Kc0, domain=Kc_dom, check=check)
    return make_row("col",
        f"Kuramoto model, N = {N}, Lorentzian frequencies (width gamma = {gam:g}, centre omega0 = {omega0:g}), each oscillator pulled toward the P3 age-weighted mean of the past mean fields (tau_m Z' = z - Z, tau_m = {tau_m:g}) instead of the instantaneous mean field; Euler dt = 0.02, 6000 transient + 2000 measured steps, seed 6; Ott-Antonsen reduction of both models",
        source=f"{SRC} [7] (DESCR)",
        Q="seeding each oscillator from the settled past of the population (A6 with P3 age weights: the mean field seen is the exponentially age-weighted mean of past mean fields) leaves the Kuramoto threshold untouched for a population centred at zero and raises it, for a population rotating at omega0, to K_c = 2 gamma (1 + (omega0 tau_m/(1 + gamma tau_m))^2), the locked frequency at onset being omega0/(1 + gamma tau_m)",
        ingredient="A6 (the seed is a bounded-strength mean of the settled past) with P3 (geometric age weights, in continuous time the exponential kernel of time constant tau_m); the mean is Kuramoto's own (chordal), not the Fisher-Rao Frechet mean",
        null="Kuramoto's instantaneous mean field (tau_m = 0): K_c = 2 gamma at every centre",
        domain="Lee, Ott & Antonsen 2009 (large coupled oscillator systems with heterogeneous interaction delays: the OA equation with the delayed field Z = int h(s) z(t - s) ds; an exponentially distributed delay is P3's kernel); Yeung & Strogatz 1999 for a single delay. Named only, not fetched (R10)",
        numbers=(f"K_c with memory {Kc_mem:.4f} (Omega at onset {Om_c:.4f}), without {Kc0:.4f}; the delayed-field theorem with hhat by quadrature: K_c = {Kc_dom:.4f}, Omega = {Om_dom:.4f}; "
                 + "; ".join(f"K = {K:g}: memory r {sim[K]['mem'][0]:.3f} (sd {sim[K]['mem'][1]:.3f}, rotation {sim[K]['mem'][2]:.3f}; OA {sim[K]['oa_mem'][0]:.3f}, {sim[K]['oa_mem'][1]:.3f}), no memory r {sim[K]['plain'][0]:.3f} (sd {sim[K]['plain'][1]:.3f}, rotation {sim[K]['plain'][2]:.3f}; OA {sim[K]['oa_plain'][0]:.3f}, {sim[K]['oa_plain'][1]:.3f})" for K in Ks)
                 + f"; centred population (omega0 = 0) at K = {K0:g}: memory r {centred['mem'][0]:.3f}, no memory {centred['plain'][0]:.3f}, OA {centred['oa'][0]:.3f} for both; finite-N floor 1/sqrt N = {1 / math.sqrt(N):.4f}"),
        tg=f"K_c with the P3-weighted seed {Kc_mem:.4f} vs null (instantaneous mean field) {Kc0:.4f}: {_agree(Kc_mem, Kc0)} (at omega0 = 0 the steady states {_word(inert, 'agree', 'differ')} within 0.03: r {centred['mem'][0]:.3f} vs {centred['plain'][0]:.3f})",
        tn=f"the delayed-field theorem gives K_c = {Kc_dom:.4f}: the domain {_word(rel(Kc_mem, Kc_dom) <= TOL_N, 'has', 'does not have')} Q",
        tc=f"simulated r and rotation within 0.03 of the memory OA at K = 2 and 3 ({_word(far, 'yes', 'no')}), r with memory below half of r without at K = 1.2 ({_word(below, 'yes', 'no')}), memory inert at omega0 = 0 within 0.03 ({_word(inert, 'yes', 'no')}): {_word(check, 'holds', 'fails')}",
        out=out,
        reading=(f"A6 with P3 does work on a rotating population (T-G: the threshold moves from {Kc0:.4f} to {Kc_mem:.4f}, and at K = 1.2 the population with memory stays near the incoherent state, r {sim[1.2]['mem'][0]:.3f}, {sim[1.2]['mem'][0] * math.sqrt(N):.1f} times the finite-N floor, where the memoryless one locks, r {sim[1.2]['plain'][0]:.3f}) because an age-weighted past field lags a rotating present by arctan(Omega tau_m) and is shorter by 1/sqrt(1 + Omega^2 tau_m^2), which is the Sakaguchi-Kuramoto phase lag and a weaker coupling; the source's centred Lorentzian is the one frame in which the settled past and the present coincide, so the source row could not have seen it; "
                 f"the domain has it as distributed interaction delays, P3's kernel being the exponential delay distribution, and the outcome is {out}; on the source's own question (the criticality clause) nothing changes: rho -> 0 at onset is the finite-N floor, which the memory shifts along K without altering"),
        weakness=f"the mean is Kuramoto's chordal mean, not A6's Fisher-Rao Frechet mean (they differ near onset, where the phase spread is wide); the mapping of an 'occasion' to a slice of the mean field is a reading (D5 has no cut here: the population has no own event); near onset the finite-N r exceeds the OA value (K = 1.6: {sim[1.6]['mem'][0]:.3f} against {sim[1.6]['oa_mem'][0]:.3f}), so the check is made at K = 2 and 3 only; one tau_m, one omega0, one seed",
        elegance="A crowd that follows where the crowd was a moment ago, not where it is, needs more persuasion to fall into step whenever the crowd is drifting; if the crowd stands still, remembering changes nothing. One picture: memory of a moving target is a lag plus a shrink.",
        child="Imagine dancers trying to clap together by copying the group. If each dancer copies what the group was doing a moment ago, and the group's beat is drifting, everyone is always a little behind and it takes a stronger pull to get them clapping together. If the beat is not drifting, copying the past works just as well as copying the present.")


# ---------------------------------------------------------------- 80 [8] the heteroclinic cycle in a population's own unit
def r5():
    a, b, dt, t_max = 1.3, 1.0, 0.01, 400.0                          # the source's attracting case (loss a = 1.3, win b = 1), window and start
    A = np.array([[0.0, -a, b], [b, 0.0, -a], [-a, b, 0.0]])

    def rhs(y):
        x = np.exp(y - np.max(y)); x /= x.sum(); Ax = A @ x; return Ax - x @ Ax

    y = np.log(np.array([0.4, 0.35, 0.25])); dom = int(np.argmax(y)); t = 0.0
    ep, seg, lnmin_seg, t_start, y_start = [], [], [], 0.0, y.copy()
    while t < t_max:
        k1 = rhs(y); k2 = rhs(y + 0.5 * dt * k1); k3 = rhs(y + 0.5 * dt * k2); k4 = rhs(y + dt * k3)
        y = y + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0; t += dt
        yn = y - np.logaddexp.reduce(y); seg.append(np.exp(yn)); lnmin_seg.append(float(yn.min()))
        d = int(np.argmax(y))
        if d != dom:
            X = np.asarray(seg); ys = y_start - np.logaddexp.reduce(y_start)
            ep.append(dict(dur=t - t_start, arc=2.0 * float(np.linalg.norm(np.diff(np.sqrt(X), axis=0), axis=1).sum()),
                           ln_inv_entrant=float(-ys[d]), ln_inv_min=float(-min(lnmin_seg))))
            dom, seg, lnmin_seg, t_start, y_start = d, [np.exp(yn)], [float(yn.min())], t, y.copy()
    durs = np.array([e["dur"] for e in ep]); arcs = np.array([e["arc"] for e in ep])
    Le = np.array([e["ln_inv_entrant"] for e in ep]); Lm = np.array([e["ln_inv_min"] for e in ep])
    k_late = 8
    slope_e, c_e = np.polyfit(Le[-k_late:], durs[-k_late:], 1); slope_m, c_m = np.polyfit(Lm[-k_late:], durs[-k_late:], 1)
    growth = float(Le[-1] / Le[-2])
    Ns = (1e2, 1e3, 1e4, 1e6, 1e9); caps = {}
    for Nn in Ns:
        k = next((i for i, e in enumerate(ep) if e["ln_inv_min"] > math.log(Nn)), len(ep))   # first epoch in which a strategy falls below one individual
        caps[Nn] = dict(n_res=k, last=float(durs[k - 1]), interp=float(np.interp(math.log(Nn), Lm, durs)))
    eps_out = 0.01                                                   # an outside floor: a survey resolving 1 % of the population, whatever N
    cap_out = float(np.interp(math.log(1 / eps_out), Lm, durs))
    crr, null, dom_v = float(slope_m), 0.0, 1.0 / a
    check = rel(slope_e, 1.0 / b) <= 0.02 and rel(slope_m, 1.0 / a) <= 0.02 and rel(growth, a / b) <= 0.02
    out = outcome(crr=crr, null=null, domain=dom_v, check=check)
    return make_row("evo",
        f"Rock-paper-scissors replicator with an attracting heteroclinic cycle (loss a = {a:g}, win b = {b:g}; RK4 in log coordinates, dt = {dt:g}, window {t_max:g}, start (0.4, 0.35, 0.25)), read in a population's own unit: one individual, the smallest frequency step 1/N (A1'), D1 rho = N",
        source=f"{SRC} [8] (CONSIST)",
        Q="the heteroclinic slowing has a cap set by the population's own unit: an epoch's duration is (1/b) ln(1/eps) + c with eps the entrant's frequency at its start, the exiting strategy contracts to eps^(a/b), so an epoch is resolvable only while eps^(a/b) >= 1/N and the longest resolvable epoch grows by 1/a per e-fold of population, T_max = (1/a) ln N + c'; the source's unbounded lengthening, and its arc-regular class, belong to the continuum",
        ingredient="A1'/D1 (the unit is the system's own smallest step, one individual; rho = N is reported, never predicted), D5 (occasion = dominance epoch); D2 the arc (not proper)",
        null="an outside floor (a survey resolving 1 % of the population): the cap is the same for every N, so it grows by 0 per e-fold of N",
        domain="the saddle-passage law of a heteroclinic cycle (passage time (1/lambda_u) ln(1/eps) + O(1), contraction eps -> eps^(lambda_s/lambda_u); Hofbauer & Sigmund 1998 ch. 17, May & Leonard 1975) and the finite-population trichotomy of Reichenbach, Mobilia & Frey 2006 (extinction time ~ ln N when the cycle attracts). Named only, not fetched (R10)",
        numbers=(f"{len(ep)} epochs in the window; last 12 durations {durs[-12]:.2f} -> {durs[-1]:.2f}, arcs {arcs[-12]:.4f} -> {arcs[-1]:.4f} (pi = {math.pi:.4f}); ln(1/entrant) at the epoch start {Le[-12]:.3f} -> {Le[-1]:.3f}, ratio of consecutive values at the end {growth:.4f} (a/b = {a / b:.4f}); "
                 f"regression of duration on ln(1/entrant), last {k_late} epochs: slope {slope_e:.4f} (1/b = {1 / b:.4f}), intercept {c_e:.4f}; on ln(1/deepest frequency in the epoch): slope {slope_m:.4f} (1/a = {1 / a:.4f}), intercept {c_m:.4f}; "
                 + "; ".join(f"N = {Nn:.0e}: {caps[Nn]['n_res']} resolvable epochs, last resolvable duration {caps[Nn]['last']:.2f}, cap interpolated at one individual {caps[Nn]['interp']:.2f}" for Nn in Ns)
                 + f"; outside floor {eps_out:g}: cap {cap_out:.2f} at every N"),
        tg=f"growth of the cap per e-fold of N: {crr:.4f} (own unit) vs null {null:.4f} (outside floor): {_agree(crr, null)}",
        tn=f"the saddle-passage law gives 1/lambda_s = 1/a = {dom_v:.4f}: the domain {_word(rel(crr, dom_v) <= TOL_N, 'has', 'does not have')} Q",
        tc=f"duration slope on ln(1/entrant) within 2 % of 1/b ({_word(rel(slope_e, 1.0 / b) <= 0.02, 'yes', 'no')}), on ln(1/deepest) within 2 % of 1/a ({_word(rel(slope_m, 1.0 / a) <= 0.02, 'yes', 'no')}), contraction ratio within 2 % of a/b ({_word(rel(growth, a / b) <= 0.02, 'yes', 'no')}): {_word(check, 'holds', 'fails')}",
        out=out,
        reading=(f"the unit does work (T-G: with one individual as the step the cap grows by {crr:.4f} per e-fold of N, with an outside floor by {null:.1f}) and what it produces is the domain's saddle arithmetic: the entrant sets the duration at 1/b per e-fold, the exit contracts by a/b, so a population of N runs the cycle for {caps[1e6]['n_res']} of the window's {len(ep)} epochs at N = 1e6 and its longest resolvable epoch lasts {caps[1e6]['last']:.2f} (the cap interpolated at one individual {caps[1e6]['interp']:.2f}) against the continuum's {durs[-1]:.2f}; "
                 f"read with A6's clause ('a system that re-counts its past stops cutting'): each epoch's entrant is the compounded contraction of every past epoch, the cut rate falls toward zero, and the arc-regularity synthesis.py row 7 found (arc {arcs[-1]:.4f} per epoch) is that of a system that is stopping; in its own unit it stops at extinction, the ln N law of the finite-population domain; the outcome is {out}"),
        weakness="the check applies the unit as a floor on the deterministic flow (an epoch counts while every strategy stays above one individual), not a stochastic simulation with demographic noise, so extinction is placed where the continuum crosses 1/N and not where a finite population's fluctuations reach it; the intercepts c, c' are the window's, not a theorem's; one a, one start",
        elegance="A game that remembers every past round slows down forever, and a population of N players can only slow down until one strategy is down to its last player. The size of the crowd, not the game, sets how long the longest round can be.",
        child="In rock-paper-scissors played by a whole crowd, each strategy takes turns being the winner, and every turn lasts longer than the last because the losing strategy gets squeezed smaller and smaller. But a strategy cannot be smaller than one person. So the turns can only get so long, and how long depends on how big the crowd is: a bigger crowd, longer turns, and then one strategy disappears.")


def main():
    return run_batch("Synthesis batch 16: rows 76-80 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
