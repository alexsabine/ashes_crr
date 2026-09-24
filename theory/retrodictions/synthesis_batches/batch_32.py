"""Synthesis batch 32: CYCLE, EVENT, MEMORY on a rotor and EQ-IG, five new systems in the classes where CRR works (owner
request 2026-09-24, prompt-log entry 131). Declared blind in DECLARATION_31_32.md (sha256 86cfb0eb..., OpenTimestamps-
stamped, pushed in commit 1232815 before this file existed). [1] the Brusselator under a slow drift of B: H-L5's class on
a Poisson carrier; [2] FitzHugh-Nagumo: H-CUT on the recovery event; [3] Lotka-Volterra with predators responding to
remembered prey; [4] the seasonally forced SIR: H-L5's class (measles-like); [5] event counting: resolvable steps between
two Poisson rates (A1'). Literature named by name and year only (R10): Prigogine and Lefever 1968; FitzHugh 1961;
Nagumo 1962; Lotka 1925; Volterra 1926; Anderson and May 1991; Anscombe 1948. Deterministic; under 60 s."""
import math
import sys

import numpy as np

from crr.instrument.core import antipodal_cuts, intrinsic_phase, peak_cuts
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch


def _w(cond, yes, no):
    return yes if cond else no


def _cv(v):
    v = np.asarray(v, float); return float(np.std(v) / abs(np.mean(v)))


def _rk4_path(f, z0, dt, n):
    z = np.array(z0, float); out = np.empty((n + 1, len(z0))); out[0] = z; t = 0.0
    for i in range(n):
        k1 = f(t, z); k2 = f(t + dt / 2, z + dt / 2 * k1); k3 = f(t + dt / 2, z + dt / 2 * k2); k4 = f(t + dt, z + dt * k3)
        z = z + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6; t += dt; out[i + 1] = z
    return out


# ---------------------------------------------------------------- [1] Brusselator: H-L5 on a Poisson carrier
def r1():
    A = 1.0; dt = 0.002; n = int(round(5000 / dt))
    def f(t, z):
        x, y = z; B = 3.0 + 0.3 * math.sin(2 * math.pi * t / 500.0)
        return np.array([A - (B + 1) * x + x * x * y, B * x - x * x * y])
    Z = _rk4_path(f, (1.0, 3.0), dt, n); t = np.arange(n + 1) * dt
    keep = t >= 500.0; x, y, t = Z[keep, 0], Z[keep, 1], t[keep]
    up = np.where((x[:-1] < 1.0) & (x[1:] >= 1.0))[0]
    dx = np.diff(x); dy = np.diff(y); xm = 0.5 * (x[1:] + x[:-1]); ym = 0.5 * (y[1:] + y[:-1])
    segF = np.sqrt(dx * dx / xm + dy * dy / ym); segE = np.sqrt(dx * dx + dy * dy)
    cF = np.cumsum(np.r_[0.0, segF]); cE = np.cumsum(np.r_[0.0, segE])
    arcF = np.diff(cF[up]); arcE = np.diff(cE[up]); per = np.diff(t[up])
    amp = np.array([x[a:b].max() - x[a:b].min() for a, b in zip(up[:-1], up[1:])])
    cvF, cvE, cvT, cvA = _cv(arcF), _cv(arcE), _cv(per), _cv(amp)
    crr, null = cvF, cvE; check = cvF < cvT and cvF < cvA
    out = outcome(crr=crr, null=null, domain=None, check=check)
    return make_row("event", "the Brusselator dx/dt = A - (B + 1) x + x^2 y, dy/dt = B x - x^2 y, A = 1, B(t) = 3 + 0.3 sin(2 pi t/500), RK4 dt 0.002 over t in [0, 5000] (first 500 discarded); own events: upward crossings of x = 1",
                    source="DECLARATION_31_32.md row 32-1 (new system; EVENT/CYCLE class)",
                    Q="under a slow drift of B the cycles are in H-L5's arc-regular class on the Poisson (concentration) carrier: CV(Fisher arc per cycle) < CV(period) and < CV(peak-to-trough amplitude of x)",
                    ingredient="H-L5 (the class claim: arc against clock between own events) with D5 (occasion = one cycle between Poincare crossings), arc on the Poisson carrier g = diag(1/x, 1/y)",
                    null="the arc with the identity metric (H-L5's control ii)",
                    domain="none cited",
                    numbers=f"{len(per)} cycles; CV of the Fisher arc {cvF:.4f}, of the identity arc {cvE:.4f}, of the period {cvT:.4f}, of the amplitude {cvA:.4f}; class index CV(clock)/CV(Fisher arc) {cvT / cvF:.4f}",
                    tg=f"CV(Fisher arc) {crr:.4f} vs null CV(identity arc) {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no theorem cited",
                    tc=f"CV(Fisher arc) below CV(period) and below CV(amplitude): {_w(check, 'holds', 'fails')}",
                    out=out,
                    reading=f"the Brusselator under a slow drift of B is {_w(cvF < cvT, 'arc-regular', 'clock-regular')} on the Poisson carrier (index {cvT / cvF:.4f}), and the Fisher arc is {_w(cvF < cvA, 'more', 'less')} regular than the amplitude control; the Poisson metric {_w(rel(cvF, cvE) <= TOL_G, 'makes no difference', 'changes the regularity')} against the identity arc ({cvF:.4f} against {cvE:.4f})",
                    weakness="one drift (amplitude 10 %, period 500, about 70 cycles per drift period); deterministic; a gate row for this system (a must-fail drift) is not in the standing gate",
                    elegance="", child="")


# ---------------------------------------------------------------- [2] FitzHugh-Nagumo: H-CUT on the recovery event
def _nearest(ev, marks):
    marks = np.asarray(marks, float); j = np.searchsorted(marks, ev)
    lo = np.abs(ev - marks[np.clip(j - 1, 0, len(marks) - 1)]); hi = np.abs(marks[np.clip(j, 0, len(marks) - 1)] - ev)
    return np.minimum(lo, hi)


def r2():
    dt = 0.01; n = int(round(20000 / dt))
    def f(t, z):
        v, w = z; I = 0.5 + 0.1 * math.sin(2 * math.pi * t / 2000.0)
        return np.array([v - v ** 3 / 3 - w + I, 0.08 * (v + 0.7 - 0.8 * w)])
    Z = _rk4_path(f, (-1.0, 1.0), dt, n); v = Z[:, 0]
    upi = np.where((v[:-1] < 0) & (v[1:] >= 0))[0]; dn = np.where((v[:-1] >= 0) & (v[1:] < 0))[0]
    ph = intrinsic_phase(v); cuts = antipodal_cuts(ph, start=int(upi[0])); ext = peak_cuts(v, prominence=0.5, distance=100)
    ev = dn[dn > upi[0]].astype(float)
    ev = ev[(ev > cuts[0]) & (ev < cuts[-1]) & (ev > ext[0]) & (ev < ext[-1])]
    dc = _nearest(ev, cuts); de = _nearest(ev, ext); frac = float(np.mean(dc < de))
    # surrogate: symmetric van der Pol (mu = 5), cuts started at the first maximum
    dt2 = 0.01; n2 = int(round(400 / dt2))
    Zv = _rk4_path(lambda t, z: np.array([z[1], 5.0 * (1 - z[0] ** 2) * z[1] - z[0]]), (2.0, 0.0), dt2, n2); xv = Zv[int(50 / dt2):, 0]
    extv = peak_cuts(xv, prominence=0.5, distance=100); mx = [i for i in extv if xv[i] > 0]
    cv_ = antipodal_cuts(intrinsic_phase(xv), start=int(mx[0])); evv = np.where((xv[:-1] >= 0) & (xv[1:] < 0))[0].astype(float)
    evv = evv[(evv > cv_[0]) & (evv < cv_[-1]) & (evv > extv[0]) & (evv < extv[-1])]
    sdiff = float(np.median(np.abs(_nearest(evv, cv_) - _nearest(evv, extv))))
    crr, null = frac, 0.5; check = frac >= 2 / 3
    # POST HOC (added after the first run; AGENT_LOG 109): the same statistic on a waveform with no dynamics (S-E,
    # sin t + 1.2 sin 2t + 0.6 sin 3t), events its downward zero crossings, cuts started at its first upward crossing
    ts = np.arange(0.0, 200 * 2 * math.pi, 0.01); xs = np.sin(ts) + 1.2 * np.sin(2 * ts) + 0.6 * np.sin(3 * ts)
    ups = np.where((xs[:-1] < 0) & (xs[1:] >= 0))[0]; dns = np.where((xs[:-1] >= 0) & (xs[1:] < 0))[0]
    cs = antipodal_cuts(intrinsic_phase(xs), start=int(ups[0])); es = peak_cuts(xs, prominence=0.5, distance=100)
    evs = dns[(dns > cs[0]) & (dns < cs[-1]) & (dns > es[0]) & (dns < es[-1])].astype(float)
    frac_se = float(np.mean(_nearest(evs, cs) < _nearest(evs, es))); forced = frac_se >= 2 / 3
    out = outcome(crr=crr, null=null, domain=None, check=check)
    return make_row("cycle", "FitzHugh-Nagumo dv/dt = v - v^3/3 - w + I(t), dw/dt = 0.08 (v + 0.7 - 0.8 w), I(t) = 0.5 + 0.1 sin(2 pi t/2000), RK4 dt 0.01 over t in [0, 20000]; own events: the recovery (downward crossing of v = 0)",
                    source="DECLARATION_31_32.md row 32-2 (new system; CYCLE class; H-CUT, gate runs/phaseA/gate_CUT.txt OPEN)",
                    Q="on at least 2/3 of recovery events the event is nearer an antipodal cut (A3 on the analytic-signal phase of v, started at the first upstroke) than to the nearest waveform extremum",
                    ingredient="A3 (the cut at the antipode of the intrinsic phase) through H-CUT (own events against antipode and extremum)",
                    null="chance, 0.5",
                    domain="none cited",
                    numbers=f"{len(ev)} recovery events; nearer the antipodal cut on {int(np.sum(dc < de))} ({frac:.4f}); median distance to the cut {np.median(dc):.1f} samples, to the extremum {np.median(de):.1f} samples; surrogate van der Pol (mu = 5, cuts started at a maximum): median |distance to cut - distance to extremum| {sdiff:.1f} samples ({_w(sdiff <= 2, 'coincide: nothing to test, as required', 'VIOLATION: they do not coincide')}); POST HOC surrogate with no dynamics (S-E, downward zero crossings): nearer the cut on {frac_se:.4f} ({_w(forced, 'reaches the declared 2/3: the statistic passes without dynamics', 'below 2/3')})",
                    tg=f"fraction {crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no theorem cited",
                    tc=f"fraction at least 2/3: {_w(check, 'holds', 'fails')}",
                    out=out,
                    reading=f"the FitzHugh-Nagumo recovery event sits nearer the {_w(frac > 0.5, 'antipodal cut', 'waveform extremum')} on {max(frac, 1 - frac):.4f} of cycles (median distances {np.median(dc):.1f} against {np.median(de):.1f} samples), so H-CUT {_w(check, 'holds at the declared 2/3', 'does not reach the declared 2/3')}; " + _w(forced, f"but the post hoc surrogate with no dynamics reaches {frac_se:.4f}: the analytic signal writes x = A cos(phi) exactly, so zero crossings of the (detrended) signal sit a half-turn apart by construction, and an event defined as a zero crossing lands on the antipodal cut by the arithmetic of the estimator, not by the system; by R4 this operationalisation of H-CUT is not about CRR and the ADDS label is not a candidate in substance", "and the post hoc surrogate with no dynamics stays below the threshold"),
                    weakness="the recovery event is a threshold crossing chosen by the author; the analytic-signal phase of a relaxation waveform is non-uniform, so where the antipode lands depends on the phase estimator (a Poincare-section phase is the named alternative and is not run)",
                    elegance="", child="")


# ---------------------------------------------------------------- [3] Lotka-Volterra with remembered prey
def _lv_eig(Tm, al=1.0, be=0.5, ga=0.5, de=0.25):
    xs, ys = ga / de, al / be
    J = np.array([[0.0, -be * xs, 0.0], [0.0, 0.0, de * ys], [1.0 / Tm, 0.0, -1.0 / Tm]])
    ev = np.linalg.eigvals(J); k = int(np.argmax(ev.real)); return ev[k]


def r3():
    e1 = _lv_eig(1.0); e0 = _lv_eig(1e-6)
    crr = float(e1.real); null = 0.0; check = e1.real > 0.01 * abs(e1.imag); sur_ok = abs(e0.real) <= 1e-4
    out = outcome(crr=crr, null=null, domain=None, check=check)
    return make_row("mem", "Lotka-Volterra dx/dt = x (1 - 0.5 y), dy/dt = y (0.25 M - 0.5), with predators responding to the A6-remembered prey dM/dt = (x - M)/T_m, T_m = 1; linear stability of the equilibrium (2, 2, 2)",
                    source="DECLARATION_31_32.md row 32-3 (new system; MEMORY on a rotor)",
                    Q="the neutral centre becomes an unstable spiral: the leading eigenvalue's real part exceeds 0.01 |imaginary part|",
                    ingredient="A6 with P3's exponential kernel as the prey density the predators respond to",
                    null="T_m -> 0: the classical centre, real part 0",
                    domain="none cited",
                    numbers=f"leading eigenvalue at T_m = 1: {e1.real:+.5f} {e1.imag:+.5f}i; surrogate T_m = 1e-6: real part {e0.real:+.2e} ({_w(sur_ok, 'centre recovered, as required', 'VIOLATION')})",
                    tg=f"real part {crr:+.5f} vs null {null:+.5f}: {_w(abs(crr - null) <= TOL_G * max(abs(e1.imag), 1e-12), 'agree', 'differ')}",
                    tn="no theorem cited",
                    tc=f"real part above 0.01 |Im|: {_w(check, 'holds', 'fails')}",
                    out=out,
                    reading=f"remembered prey {_w(e1.real > 0, 'destabilises', 'stabilises')} the predator-prey centre (leading eigenvalue {e1.real:+.5f} {e1.imag:+.5f}i): the lag between prey and the predators' response feeds the cycle; delayed Lotka-Volterra models are a known literature in which delays destabilise, so the direction is likely the domain's",
                    weakness="linear stability only; the harness's T-G compares a real part against 0, so 'differ' uses the eigenvalue's own scale (1 % of |Im|) rather than the relative rule",
                    elegance="", child="")


# ---------------------------------------------------------------- [4] the seasonally forced SIR: H-L5's class
def r4():
    b0, gam, mu = 1250.0, 365.0 / 14.0, 0.02; dt = 1e-4; n = int(round(200 / dt))
    def f(t, z):
        S, I = z; b = b0 * (1 + 0.25 * math.cos(2 * math.pi * t))
        return np.array([mu - b * S * I - mu * S, b * S * I - (gam + mu) * I])
    Z = _rk4_path(f, (0.06, 1e-4), dt, n); t = np.arange(n + 1) * dt
    keep = t >= 100.0; S, I, t = Z[keep, 0], Z[keep, 1], t[keep]
    m = I.mean(); up = np.where((I[:-1] < m) & (I[1:] >= m))[0]
    dS = np.diff(S); dI = np.diff(I); Sm = 0.5 * (S[1:] + S[:-1]); Im = 0.5 * (I[1:] + I[:-1])
    cF = np.cumsum(np.r_[0.0, np.sqrt(dS * dS / Sm + dI * dI / Im)]); cE = np.cumsum(np.r_[0.0, np.sqrt(dS * dS + dI * dI)])
    arcF = np.diff(cF[up]); arcE = np.diff(cE[up]); per = np.diff(t[up])
    cvF, cvE, cvT = _cv(arcF), _cv(arcE), _cv(per); cvR = _cv(np.maximum(np.round(per), 1.0))
    flat = max(cvF, cvT) < 1e-6                                                 # nothing varies: the gate's pure-sine case, the class is undefined
    crr = cvT / cvF; null = cvT / cvE; domain = cvR / cvF; check = crr < 1.0
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row("event", "seasonally forced SIR with births and deaths (fractions): beta(t) = 1250 (1 + 0.25 cos 2 pi t)/yr, gamma = 365/14 per yr, mu = 0.02/yr; RK4 dt 1e-4 yr over 200 yr, first 100 discarded; own events: upward crossings of I through its mean",
                    source="DECLARATION_31_32.md row 32-4 (new system; EVENT class; the ledger's MEAS2 rows found measles clock-regular in 17/17 cities)",
                    Q="H-L5 fails: the model is clock-regular, class index CV(clock)/CV(Fisher arc) < 1, in agreement with MEAS2-1 and MEAS2-2",
                    ingredient="H-L5 (the class claim) with D5 (occasion = inter-epidemic interval) on the Poisson carrier of (S, I)",
                    null="the class index with the identity-metric arc",
                    domain="phase-locking to the annual forcing: the index when the clock's CV is that of the intervals rounded to whole years",
                    numbers=f"{len(per)} epidemics; intervals (yr) {', '.join(f'{p:.3f}' for p in per[:6])}{' ...' if len(per) > 6 else ''}; CV of the period {cvT:.4f}, of the Fisher arc {cvF:.4f}, of the identity arc {cvE:.4f}, of the whole-year intervals {cvR:.4f}; class index {crr:.4f}",
                    tg=f"index {crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"phase-locking gives {domain:.4f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=_w(flat, f"not decidable: neither the clock nor the arc varies (CVs {cvT:.1e} and {cvF:.1e}), so the index is 0/0", f"class index below 1 (clock-regular): {_w(check, 'holds', 'fails')}"),
                    out=out,
                    reading=_w(flat, f"the declared tuple does not sit in the biennial regime: every interval is one year and neither the clock nor the arc varies (CVs {cvT:.1e} and {cvF:.1e}), so the model is the gate's pure-sine case, H-L5 has nothing to test, and the harness's REDUNDANT-IG reads 'the ingredient did no work'; the row neither agrees nor disagrees with the ledger's measles result, and a biennial tuple would be a new declaration", f"the forced SIR at these parameters is {_w(crr < 1, 'clock-regular', 'arc-regular')} (index {crr:.4f}), {_w(crr < 1, 'agreeing', 'disagreeing')} with the ledger's measles result"),
                    weakness="the parameter tuple was declared to be measles-like without a prior run; if the printed intervals are not biennial the row describes whatever regime the tuple produced; deterministic (no demographic noise)",
                    elegance="", child="")


# ---------------------------------------------------------------- [5] resolvable steps between two Poisson rates
def r5():
    l1, l2, T = 4.0, 9.0, 25.0
    crr = 2 * math.sqrt(T) * (math.sqrt(l2) - math.sqrt(l1))
    null = (l2 - l1) * T / math.sqrt(l1 * T)
    rng = np.random.default_rng(325); N1 = rng.poisson(l1 * T, 200000); N2 = rng.poisson(l2 * T, 200000)
    domain = float(np.mean(2 * np.sqrt(N2)) - np.mean(2 * np.sqrt(N1)))
    sd1, sd2 = float(np.std(2 * np.sqrt(N1))), float(np.std(2 * np.sqrt(N2)))
    out = outcome(crr=crr, null=null, domain=domain, check=None)
    return make_row("eqig", "event counting (photons, decays, spikes) at rates lambda1 = 4 and lambda2 = 9 per unit time, observed in windows of T = 25; A1': one event = one resolvable step",
                    source="DECLARATION_31_32.md row 32-5 (new system; EQ-IG class)",
                    Q="the number of resolvable steps between the two rates is 2 sqrt(T)(sqrt(lambda2) - sqrt(lambda1)) = 10: the Poisson family's Fisher arc in its own unit",
                    ingredient="A1' (the unit is the system's own resolvable step; for a point process, events) with D1's count of steps",
                    null="the clock-noise count (lambda2 - lambda1) T / sqrt(lambda1 T): the Gaussian unit at lambda1",
                    domain="Anscombe's variance-stabilising square-root transform: the difference of 2 sqrt(N) in units of its standard deviation (about 1), from 200000 simulated windows per rate (seed 325)",
                    numbers=f"CRR {crr:.4f}; null {null:.4f}; simulated difference of 2 sqrt(N) {domain:.4f} (standard deviations {sd1:.4f}, {sd2:.4f})",
                    tg=f"{crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the square-root transform gives {domain:.4f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc="not needed (the domain has Q)" if rel(crr, domain) <= TOL_N else "no check stated",
                    out=out,
                    reading="counting in the system's own unit gives the variance-stabilised distance statisticians use for counts: the square-root transform makes the Poisson noise one unit wide everywhere, so the arc between two rates is how many noise-widths apart they are; the Gaussian unit taken at one end overstates it",
                    weakness="a textbook identity (the Poisson family's Fisher metric is 1/lambda per unit time); the row is in the paradigm by design and was declared as expected REDUNDANT-DOMAIN",
                    elegance="Measured in its own flickers, the distance between a dim light and a bright one is how many flickers apart they are.",
                    child="Two lamps flicker at different speeds. If you count in flickers, you can say how many 'flicker-steps' apart they are, and that number stays fair whether the lamps are dim or bright.")


def main():
    return run_batch("Synthesis batch 32: CYCLE, EVENT, MEMORY on a rotor, EQ-IG (prompt-log entry 131; DECLARATION_31_32.md)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
