"""PRED70 batch P13: engineering and control (Predictions70/DECLARATION.md; declared.py rows P13-1..P13-5, pushed at 8397478
before any model existed). [1] PI control with actuator saturation and an A6-bounded integral; [2] a relay thermostat
with hysteresis against the antipodal cut of its temperature phase; [3] M/M/1 busy periods in customers served against
clock time; [4] the TCP AIMD sawtooth under random loss (H-L5); [5] A6 at q = 0.5 against simple exponential smoothing.
Q, the null and H0 are printed verbatim from declared.py; every verdict word is computed from the numbers (R15).
Literature named by name only (R10; nothing fetched): Kendall 1951 (busy period); Mathis et al. 1997 (AIMD random loss);
Brown 1956 / Holt 1957 (exponential smoothing); Astrom and Hagglund (anti-windup; describing function of a relay).
Deterministic (fixed seeds, fixed grids); no data files; well under two minutes.
    uv run python Predictions70/batches/pred_13.py > Predictions70/batches/pred_13.txt
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from declared import P  # noqa: E402

from crr.instrument.core import antipodal_cuts, cv, intrinsic_phase, regularity  # noqa: E402
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


# ---------------------------------------------------------------- [1] PI with saturation, A6-bounded integral
TAU, TS, KP, KI, UMAX, REF, NSTEP = 5.0, 1.0, 1.0, 0.3, 1.1, 1.0, 300


def _pi(mode, q=Q_DECIDE):
    """First-order plant y+ = a y + (1 - a) u (ZOH, a = exp(-Ts/tau)), unit step reference, u = clip(Kp e + Ki I).
    mode: 'plain' I = I + Ts e; 'a6' I = Ts/(1 - q) * M, M = (1 - q) e + q M (the A6 remembered error, bounded mean);
    'leaky' I = q I + Ts e (the domain's leaky integrator, leak q per sample); 'clamp' conditional integration."""
    a = math.exp(-TS / TAU); y = 0.0; I = 0.0; M = 0.0; ys = []; nsat = 0
    for _ in range(NSTEP):
        e = REF - y
        if mode == "plain":
            I = I + TS * e; Iterm = I
        elif mode == "a6":
            M = (1 - q) * e + q * M; Iterm = TS / (1 - q) * M
        elif mode == "leaky":
            I = q * I + TS * e; Iterm = I
        else:                                                                   # clamp: integrate only when unsaturated
            v_try = KP * e + KI * (I + TS * e)
            if abs(v_try) <= UMAX: I = I + TS * e
            Iterm = I
        v = KP * e + KI * Iterm; u = min(max(v, -UMAX), UMAX); nsat += int(abs(v) > UMAX)
        y = a * y + (1 - a) * u; ys.append(y)
    ys = np.asarray(ys)
    return ys, max(0.0, float(ys.max() - REF) / REF), float(REF - ys[-1]), nsat


def r1():
    d = DECL["P13-1"]
    y6, os6, off6, s6 = _pi("a6"); yp, osp, offp, sp = _pi("plain"); yl, osl, offl, sl = _pi("leaky"); yc, osc, offc, sc = _pi("clamp")
    same = float(np.max(np.abs(y6 - yl)))
    crr, null, dom = os6, osp, osl
    check = crr < (1 - TOL_G) * null
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    grid = []
    for q in Q_GRID:
        _, o, f, _s = _pi("a6", q); _, ol, fl, _s = _pi("leaky", q)
        grid.append(f"q = {q}: overshoot {o:.6f} (leaky {ol:.6f}), final offset {f:.6f}")
    return make_row(d["cls"], f"{d['system']} (model: first-order plant tau = {TAU}, sample period Ts = {TS} = one occasion, Kp = {KP}, Ki = {KI}, |u| <= {UMAX}, unit step, {NSTEP} samples)",
                    source=_src(d),
                    Q=f"{d['Q']} (computed as: relative overshoot max(y) - r of the A6-integral loop below 0.99 x the plain-integral loop's)",
                    ingredient=f"{d['ingredient']}: the integral replaced by Ts/(1 - q) x the A6 bounded mean of the error, M = (1 - q) e + q M, q = {Q_DECIDE}",
                    null=d["null"], domain=f"{d['H0']} (computed: leaky integrator I = q I + Ts e with the same leak; clamped conditional integration printed)",
                    numbers=f"overshoot: A6 {os6:.6f}, plain {osp:.6f}, leaky {osl:.6f}, clamped {osc:.6f}; final offset (r - y at the end): A6 {off6:.6f}, plain {offp:.6f}, leaky {offl:.6f}, clamped {offc:.6f}; "
                            f"saturated samples: A6 {s6}, plain {sp}, leaky {sl}, clamped {sc} (model check, windup present: plain overshoot above the clamped one {_w(osp > osc, 'yes', 'NO')}); max |y_A6 - y_leaky| over the run {same:.3e}; q-grid (sensitivity, q = 0.5 decides): " + "; ".join(grid),
                    tg="overshoot " + _tg(crr, null, ".6f"),
                    tn=f"leaky-integrator overshoot {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"A6 overshoot {crr:.6f} < 0.99 x plain {null:.6f}: {_w(check, 'holds', 'fails')} {_qv(check)}",
                    out=out,
                    reading=f"the A6-bounded integral is algebraically the leaky integrator with leak q per occasion (trajectories differ by {same:.1e}); it {_w(check, 'removes', 'does not remove')} the windup overshoot "
                            f"({osp:.4f} -> {os6:.4f}; the clamp gives {osc:.4f}); with q = {Q_DECIDE} per sample its settled offset is {off6:.4f} where the plain and clamped integrators reach {offp:.4f} and {offc:.4f}: "
                            f"{_w(off6 > max(offp, offc) + 1e-6, 'the bounded integral trades the zero-error guarantee for the missing windup, the known trade of the leaky anti-windup', 'the bounded integral keeps zero error')}",
                    weakness="one plant, one gain pair; the occasion is one control sample (a choice: the declaration fixes q per occasion, not the occasion); the scale Ts/(1 - q) on the bounded mean (so the newest error enters with the plain integral's weight Ts) is a choice, and the overshoot is 0 at every q of the grid; overshoot is the only target Q names, so the offset the bounded integral costs is reported, not scored",
                    elegance="", child="")


# ---------------------------------------------------------------- [2] relay thermostat with hysteresis
def _thermo(Th, Ta=10.0, lo=19.5, hi=20.5, tau=1.0, dt=1e-4, ncyc=60):
    """dT/dt = (Ta - T)/tau + u (Th - Ta)/tau, exact exponential update per step; relay on below lo, off above hi."""
    T = lo; u = 1; xs = []; on_ev = []; off_ev = []; k = 0
    decay = math.exp(-dt / tau)
    while len(off_ev) < ncyc + 1:
        target = Th if u else Ta
        T = target + (T - target) * decay; k += 1
        if u and T >= hi: u = 0; off_ev.append(k)
        elif not u and T <= lo: u = 1; on_ev.append(k)
        xs.append(T)
    return np.asarray(xs), np.asarray(on_ev) - 1, np.asarray(off_ev) - 1


def _antipode_fraction(Th):
    x, on_ev, off_ev = _thermo(Th)
    ph = intrinsic_phase(x)
    first, last = 10, len(off_ev) - 10                                          # score away from the Hilbert edges
    start = int(off_ev[first])
    cuts = antipodal_cuts(ph, start=start)
    fc, fo, dev = [], [], []
    for k in range(first, last - 1):
        a, b = off_ev[k], off_ev[k + 1]; Pk = b - a
        odd = cuts[(cuts > a) & (cuts < b)]
        on = on_ev[(on_ev > a) & (on_ev < b)]
        if len(odd) != 1 or len(on) != 1:
            continue
        fc.append((odd[0] - a) / Pk); fo.append((on[0] - a) / Pk); dev.append(abs(odd[0] - on[0]) / Pk)
    even_dev = []
    for k in range(first + 1, last - 1):
        near = cuts[np.argmin(np.abs(cuts - off_ev[k]))]
        even_dev.append(abs(near - off_ev[k]) / (off_ev[k + 1] - off_ev[k]))
    return (float(np.mean(fc)), float(np.mean(fo)), float(np.max(dev)), len(fc), float(np.max(even_dev)),
            float(np.mean(np.diff(off_ev[first:last]))) * 1e-4)


def r2():
    d = DECL["P13-2"]
    fc, fo, dmax, n, evdev, per = _antipode_fraction(40.0)
    fcs, fos, dmaxs, ns, evs, pers = _antipode_fraction(30.0)
    dom = 0.5
    crr, null = fc, fo
    check = dmax <= TOL_N
    check_sym = dmaxs <= TOL_N
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row(d["cls"], f"{d['system']} (model: dT/dt = (Ta - T)/tau + u (Th - Ta)/tau, Ta = 10, Th = 40 (heating twice as fast as cooling at 20), band [19.5, 20.5], tau = 1, exact update dt = 1e-4, 60 cycles, cycles 10-50 scored)",
                    source=_src(d),
                    Q=f"{d['Q']} (computed as: the antipodal cut of the analytic-signal phase anchored at a switch-off falls on the next switch-on within 1 % of the period, every scored cycle)",
                    ingredient=f"{d['ingredient']}: intrinsic_phase + antipodal_cuts of the instrument, anchored at a switch-off",
                    null=f"{d['null']} (the exact switching rule: the switch-on fraction of the cycle after the switch-off)",
                    domain=f"{d['H0']} (computed: the describing function's first-harmonic input crosses the two thresholds half a period apart, fraction {dom})",
                    numbers=f"fraction of the period from switch-off to: the antipodal cut {fc:.6f}, the actual switch-on (thresholds) {fo:.6f}; largest per-cycle |cut - switch| {dmax:.6f} of a period over {n} cycles; "
                            f"even cuts against switch-offs: largest deviation {evdev:.6f} of a period; period {per:.6f}; symmetric control Th = 30 (equal heating and cooling rates at 20): cut {fcs:.6f}, switch-on {fos:.6f}, largest deviation {dmaxs:.6f} over {ns} cycles ({_w(check_sym, 'the cut sits on the switch', 'the cut misses the switch')})",
                    tg="switch-on fraction " + _tg(crr, null, ".6f"),
                    tn=f"describing-function fraction {dom}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has the cut)', 'differ')}",
                    tc=f"largest per-cycle deviation {dmax:.6f} <= {TOL_N:g} of a period: {_w(check, 'holds', 'fails')} {_qv(check)}",
                    out=out,
                    reading=f"on the asymmetric thermostat the analytic-signal antipode falls {fc:.4f} of the period after the switch-off, the relay actually switches on at {fo:.4f}: the antipode {_w(check, 'sits on the switch', 'misses the switch')} and {_w(rel(fc, dom) <= TOL_N, 'sits at', 'misses')} the describing function's half period; "
                            f"with equal heating and cooling rates the two {_w(check_sym, 'coincide, as symmetry requires', 'still differ')} ({fcs:.4f} against {fos:.4f}); the relay switches at its thresholds, which are the extrema of the temperature, and where the cut of the phase falls depends on the waveform's shape, which the switching rule does not consult",
                    weakness="DEVIATION: H0 names two readings; the exact threshold rule is used as the null (as declared) and the describing function's half-period spacing as the T-N value; the 1 % of a period tolerance for 'occurs at the antipode' is the harness's TOL_N, not declared for this row; one asymmetry (2:1) and its symmetric control",
                    elegance="", child="")


# ---------------------------------------------------------------- [3] M/M/1 busy periods
def _busy(M, rho, mu=1.0, seed=0):
    """Jump-chain simulation: in a busy period each event is an arrival w.p. rho/(1 + rho), else a departure; the
    inter-event times are Exp(lambda + mu), so the clock length of a period with E events is Gamma(E, lambda + mu)."""
    rng = np.random.default_rng(seed)
    lam = rho * mu; pa = lam / (lam + mu)
    qlen = np.ones(M, np.int64); served = np.zeros(M, np.int64); events = np.zeros(M, np.int64)
    act = np.arange(M)
    while act.size:
        arr = rng.random(act.size) < pa
        qlen[act] += np.where(arr, 1, -1); served[act] += (~arr).astype(np.int64); events[act] += 1
        act = act[qlen[act] > 0]
    B = rng.gamma(events.astype(float), 1.0 / (lam + mu))
    return served.astype(float), B


def r3():
    d = DECL["P13-3"]
    rho = 0.8; M = 1_000_000
    N, B = _busy(M, rho)
    cvN, cvB = cv(N), cv(B)
    kN = math.sqrt(rho * (1 + rho) / (1 - rho)); kB = math.sqrt((1 + rho) / (1 - rho))
    nb = 50; diffs = np.array([cv(N[i::nb]) - cv(B[i::nb]) for i in range(nb)])
    se = float(diffs.std(ddof=1) / math.sqrt(nb)); lo, hi = float(diffs.mean() - 1.96 * se), float(diffs.mean() + 1.96 * se)
    crr, null, dom = cvN, cvB, kN
    check = (cvN < cvB) and hi < 0
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row(d["cls"], f"{d['system']} (model: {M} busy periods, service rate 1, jump-chain simulation, seed 0)",
                    source=_src(d),
                    Q=f"{d['Q']} (computed as: CV of the number served per busy period below the CV of its clock length, the batch-means 95 % interval of the difference below 0)",
                    ingredient=f"{d['ingredient']}: busy-period length counted in customers served",
                    null=d["null"], domain=f"{d['H0']} (computed: Kendall's CV of the number served, sqrt(rho (1 + rho)/(1 - rho)))",
                    numbers=f"CV: customers served {cvN:.6f} (Kendall {kN:.6f}), clock {cvB:.6f} (Kendall sqrt((1 + rho)/(1 - rho)) = {kB:.6f}); mean served {N.mean():.4f} (1/(1 - rho) = {1 / (1 - rho):.4f}); "
                            f"difference {cvN - cvB:.6f}, 95 % batch-means interval [{lo:.6f}, {hi:.6f}] ({nb} batches); ratio of squared CVs {cvN ** 2 / cvB ** 2:.6f} (Kendall's ratio {kN ** 2 / kB ** 2:.6f}, rho = {rho})",
                    tg="CV " + _tg(crr, null, ".6f"),
                    tn=f"Kendall's CV of the number served {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"CV served {cvN:.6f} < CV clock {cvB:.6f} with the interval below 0: {_w(check, 'holds', 'fails')} {_qv(check)}",
                    out=out,
                    reading=f"counting a busy period in customers served {_w(cvN < cvB, 'is less variable than', 'is not less variable than')} timing it by the clock ({cvN:.4f} against {cvB:.4f}); the busy-period moments of queueing theory give the ratio of squared CVs as {kN ** 2 / kB ** 2:.4f}, which is rho, "
                            f"(simulated {cvN ** 2 / cvB ** 2:.4f}), because the clock length adds the service-time noise to the count's; natural time is the queue's own count and the domain has both distributions",
                    weakness="one load; the CV of the number served tends to the clock's as rho -> 1 (ratio rho), so the natural-time advantage shrinks in heavy traffic, where queues matter most",
                    elegance=f"Counting a busy spell in customers served is less jumpy than timing it with a clock, and the size of the difference is the load itself: the squared spreads differ by exactly the factor rho.",
                    child="At a busy shop counter, how many people get served before it goes quiet is steadier than how many minutes it stays busy, because the minutes also depend on how slow each person is.")


# ---------------------------------------------------------------- [4] TCP AIMD sawtooth
def _aimd(p=0.01, dt=0.01, nloss=2000, seed=0, poisson_rate=None):
    """Fluid AIMD: the window grows by 1 per RTT (dt of an RTT per step); a loss in a step has probability 1 - exp(-h dt)
    with hazard h = p W (per-packet random loss, W packets per RTT) or a constant hazard (Poisson loss in time)."""
    rng = np.random.default_rng(seed)
    W = 1.0 / math.sqrt(p); xs = []; ev = []; k = 0
    while len(ev) < nloss:
        U = rng.random(100000)
        for u in U:
            h = poisson_rate if poisson_rate is not None else p * W
            if u < 1.0 - math.exp(-h * dt):
                W = max(W / 2.0, 1.0); ev.append(k)
            else:
                W += dt
            xs.append(W); k += 1
            if len(ev) >= nloss: break
    return np.asarray(xs), np.asarray(ev)


def r4():
    d = DECL["P13-4"]
    dt = 0.01
    x, ev = _aimd()
    ev = ev[10:]                                                                # drop the start-up losses
    rex = regularity(x, ev, sigma=1.0, dt=dt, n_boot=2000, seed=0, segment_end="exclusive")
    rin = regularity(x, ev, sigma=1.0, dt=dt, n_boot=2000, seed=0, segment_end="inclusive")
    xp, evp = _aimd(poisson_rate=1.0 / float(np.mean(np.diff(ev)) * dt))
    evp = evp[10:]
    rpo = regularity(xp, evp, sigma=1.0, dt=dt, n_boot=2000, seed=0, segment_end="exclusive")
    crr, null, dom = rex["cv_arc"], rex["cv_clock"], 1.0
    check = rex["ci95"][1] < 0
    chk_in = rin["ci95"][1] < 0
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row(d["cls"], f"{d['system']} (model: fluid AIMD, window +1 per RTT, halved at a loss (floor 1), per-packet loss probability 0.01 (hazard 0.01 W per RTT), step {dt} RTT, 2000 losses, the first 10 dropped, seed 0)",
                    source=_src(d),
                    Q=f"{d['Q']} (computed as: regularity() on the window, events = losses, segment_end 'exclusive' (the halving is the cut); CV(arc) < CV(clock) with the paired-bootstrap 95 % CI below 0, n_boot 2000, seed 0)",
                    ingredient=f"{d['ingredient']}: the arc of the congestion window between losses (identity metric, sigma 1)",
                    null=d["null"], domain=f"{d['H0']} (computed: a Poisson loss process has CV 1 between losses)",
                    numbers=f"exclusive: CV(arc) {rex['cv_arc']:.6f}, CV(clock) {rex['cv_clock']:.6f}, difference {rex['diff']:.6f}, CI [{rex['ci95'][0]:.6f}, {rex['ci95'][1]:.6f}], n = {rex['n']}; "
                            f"inclusive (the halving jump counted in the arc; sensitivity): CV(arc) {rin['cv_arc']:.6f}, difference {rin['diff']:.6f}, CI [{rin['ci95'][0]:.6f}, {rin['ci95'][1]:.6f}] ({_w(chk_in, 'CI below 0', 'CI not below 0')}); "
                            f"Poisson loss in time at the same mean rate (exclusive): CV(arc) {rpo['cv_arc']:.6f}, CV(clock) {rpo['cv_clock']:.6f}, CI [{rpo['ci95'][0]:.6f}, {rpo['ci95'][1]:.6f}]",
                    tg="CV " + _tg(crr, null, ".6f"),
                    tn=f"H0's Poisson CV {dom:.1f}: {_w(rel(crr, dom) <= TOL_N, 'agree', 'differ')}",
                    tc=f"exclusive CI upper end {rex['ci95'][1]:.6f} < 0: {_w(check, 'holds', 'fails')} {_qv(check)}",
                    out=out,
                    reading=f"between losses the window rises one packet per RTT, so its arc is the elapsed time in RTTs less one step: CV(arc) {rex['cv_arc']:.4f} against CV(clock) {rex['cv_clock']:.4f}, the same clock in other units; "
                            f"counting the halving jump as arc {_w(chk_in, 'lowers', 'does not lower')} the CV ({rin['cv_arc']:.4f}), which is the arithmetic of adding half the peak window to every occasion, not a clock of change; "
                            f"H0's Poisson loss times {_w(rel(rex['cv_clock'], 1.0) <= TOL_N, 'match', 'do not match')} per-packet random loss in time (CV(clock) {rex['cv_clock']:.4f}), since the loss hazard grows with the window",
                    weakness="DEVIATION: segment_end 'exclusive' (the halving is the cut, A3) decides; declared.py does not name it, and the inclusive reading's verdict is printed beside it; one loss rate; fixed RTT (a queue-dependent RTT would decouple arc from clock)",
                    elegance="", child="")


# ---------------------------------------------------------------- [5] A6 at q = 0.5 against simple exponential smoothing
def _series(T=400, seed=0):
    rng = np.random.default_rng(seed)
    t = np.arange(T, dtype=float)
    lvl = np.where(t >= 100, 4.0, 0.0) + np.where(t >= 200, -6.0, 0.0) + np.where(t >= 300, 3.0, 0.0)
    return 0.05 * t + lvl + rng.standard_normal(T)


def _a6_explicit(x, q):
    """The A6 bounded Frechet (Euclidean) mean with geometric weights: (1 - q) q^k on x_{n-k}, k < n, and q^n on the
    first observation (weights sum to 1), computed as an explicit weighted mean, not a recursion."""
    out = np.empty(len(x))
    for n in range(len(x)):
        k = np.arange(n + 1); w = (1 - q) * q ** k; w[-1] = q ** n
        out[n] = float(np.dot(w, x[n - k]))
    return out


def _a6_normalised(x, q):
    out = np.empty(len(x))
    for n in range(len(x)):
        k = np.arange(n + 1); w = q ** k; w = w / w.sum()
        out[n] = float(np.dot(w, x[n - k]))
    return out


def _ses(x, alpha):
    s = np.empty(len(x)); s[0] = x[0]
    for n in range(1, len(x)):
        s[n] = alpha * x[n] + (1 - alpha) * s[n - 1]
    return s


def _holt(x, alpha=0.5, beta=0.1):
    l, b = x[0], 0.0; f = np.empty(len(x)); f[0] = x[0]
    for n in range(1, len(x)):
        f[n] = l + b
        ln = alpha * x[n] + (1 - alpha) * (l + b); b = beta * (ln - l) + (1 - beta) * b; l = ln
    return f                                                                    # f[n] is the forecast of x[n]


def _mse(level, x):
    return float(np.mean((x[1:] - level[:-1]) ** 2))                           # one-step forecast of x[n+1] is level[n]


def r5():
    d = DECL["P13-5"]
    x = _series()
    a6 = _a6_explicit(x, Q_DECIDE); ses = _ses(x, 0.5); nrm = _a6_normalised(x, Q_DECIDE)
    gap = float(np.max(np.abs(a6 - ses))); scale = float(np.max(np.abs(x)))
    tol = 1e-12 * scale
    gnrm = np.abs(nrm - ses); above = np.nonzero(gnrm > tol)[0]; n_below = int(above[-1]) + 1 if above.size else 0
    crr, null, dom = _mse(a6, x), _mse(x, x), _mse(ses, x)
    holt = float(np.mean((x[1:] - _holt(x)[1:]) ** 2))
    check = gap <= tol
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    grid = []
    for q in Q_GRID:
        a = _a6_explicit(x, q)
        grid.append(f"q = {q}: max |A6 - SES(alpha 0.5)| {float(np.max(np.abs(a - ses))):.3e}, max |A6 - SES(alpha {1 - q})| {float(np.max(np.abs(a - _ses(x, 1 - q)))):.3e}, MSE {_mse(a, x):.6f}")
    return make_row(d["cls"], f"{d['system']} (model: x_t = 0.05 t + level shifts +4 at t = 100, -6 at 200, +3 at 300, + N(0, 1) noise, T = 400, seed 0; one-step-ahead forecasts)",
                    source=_src(d),
                    Q=f"{d['Q']} (computed as: the explicit A6 weighted mean equals the SES recursion (alpha 0.5, initial level x_0) at every step to 1e-12 x max|x|)",
                    ingredient=f"{d['ingredient']}: the bounded Frechet mean with weights (1 - q) q^k on the past and q^n on the first observation",
                    null=f"{d['null']} (the naive forecast x_t)",
                    domain=f"{d['H0']} (computed: SES recursion with alpha = 0.5)",
                    numbers=f"one-step MSE: A6 {crr:.6f}, no memory {null:.6f}, SES(0.5) {dom:.6f}, Holt (alpha 0.5, beta 0.1; context) {holt:.6f}; max |A6 - SES| {gap:.3e} (tolerance {tol:.3e}); "
                            f"the normalised-truncated reading (weights q^k / sum over the available past): largest gap to SES {float(gnrm.max()):.3e}, below tolerance at every step from {n_below} on; q-grid (sensitivity): " + "; ".join(grid),
                    tg="MSE " + _tg(crr, null, ".6f"),
                    tn=f"SES(0.5) MSE {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"max |A6 - SES| {gap:.3e} <= {tol:.3e}: {_w(check, 'holds', 'fails')} {_qv(check)}",
                    out=out,
                    reading=f"A6 with geometric weight q per occasion is simple exponential smoothing with alpha = 1 - q, so the declared equality at q = 0.5 holds because 1 - q = q there; at q = 0.25 and 0.75 the A6 mean equals SES at alpha 0.75 and 0.25, not at 0.5 (grid); "
                            f"on a trend with level shifts both lag the trend (MSE {crr:.3f} against Holt's {holt:.3f}): exponential smoothing is the domain's name for A6",
                    weakness="the equality is algebraic; the normalised-truncated reading of the weights differs from SES only in its start-up, which decays as q^n; the Holt comparison is context, not the declared target",
                    elegance="Half what you just saw and half what you remembered is the whole rule, and forecasters have used it for seventy years under the name exponential smoothing.",
                    child="To guess tomorrow, take half of today's number and half of your last guess. That simple rule is what weather and sales forecasters call smoothing.")


def main():
    return run_batch("PRED70 batch P13: engineering and control (Predictions70/DECLARATION.md; declared at 8397478)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
