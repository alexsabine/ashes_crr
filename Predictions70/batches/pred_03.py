"""PRED70 batch P03: remembered state (A6) and stability thresholds (Predictions70/DECLARATION.md; prompt-log entry 234).
Rows P03-1..P03-5 of Predictions70/declared.py (pushed at 8397478 before any model existed): [1] Beverton-Holt with
remembered density; [2] Nicholson's blowflies with the delayed density replaced by the remembered density; [3] the
cobweb with A6 price expectations; [4] SIS with contact reduced by remembered prevalence; [5] Goodwin's growth cycle with
the wage bargain on remembered employment. A6's weight is q = 0.5 per occasion (decides); q in {0.25, 0.5, 0.75} is printed
as a sensitivity only. Literature named by name and year only (R10, not fetched): Beverton and Holt 1957; Nicholson 1954;
Gurney, Blythe and Nisbet 1980; MacDonald 1978; Ezekiel 1938; Nerlove 1958; Goodwin 1967. Deterministic; well under 60 s."""
import math
import os
import sys

import numpy as np
from scipy.optimize import brentq

from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from declared import P  # noqa: E402

D = {p[0]: p for p in P}
QGRID = (0.25, 0.5, 0.75)
Q0 = 0.5
SENT = 1000.0      # encoding of "no loss of stability on the scan" (as batch_31 row 5)


def _w(cond, yes, no):
    return yes if cond else no


def _src(i):
    return f"PRED70 {i} (declared at 8397478; forecast {D[i][8]})"


def _decl(i):
    d = D[i]
    return dict(system=d[3], ingredient=d[4], Q=d[5], null=d[6], H0=d[7])


def _jac(F, z, h=1e-6):
    z = np.asarray(z, float); n = len(z); J = np.empty((n, n))
    for j in range(n):
        e = np.zeros(n); e[j] = h
        J[:, j] = (np.asarray(F(z + e)) - np.asarray(F(z - e))) / (2 * h)
    return J


# ---------------------------------------------------------------- P03-1 Beverton-Holt with remembered density
def _bh_J(R, q):
    """x_{n+1} = R x_n / (1 + (R - 1) M_n), M_n = (1 - q) x_n + q M_{n-1}; equilibrium x = M = 1; state (x_n, M_{n-1})."""
    fx = R / (1.0 + (R - 1.0)); fM = -R * (R - 1.0) / (1.0 + (R - 1.0)) ** 2
    if q == 0.0:
        return np.array([[fx + fM]])
    return np.array([[fx + fM * (1 - q), fM * q], [1 - q, q]])


BH_GRID = np.concatenate([np.arange(1.001, 20.0 + 1e-9, 0.001), np.arange(21.0, 1000.0 + 1e-9, 1.0)])


def _bh_loss(q):
    for R in BH_GRID:
        ev = np.linalg.eigvals(_bh_J(R, q))
        k = int(np.argmax(np.abs(ev)))
        if abs(ev[k]) >= 1.0 - 1e-12:
            kind = "flip" if abs(ev[k].imag) < 1e-9 and ev[k].real < 0 else ("Neimark-Sacker" if abs(ev[k].imag) >= 1e-9 else "fold")
            return float(R), kind
    return SENT, "none on the scan"


def _bh_sim(R, q, x0, n=3000):
    x, M = x0, x0
    for _ in range(n):
        M = (1 - q) * x + q * M
        x = R * x / (1.0 + (R - 1.0) * M)
    return abs(x - 1.0)


def r1():
    i = "P03-1"; d = _decl(i)
    crr, kind = _bh_loss(Q0); null, kind0 = _bh_loss(0.0); domain = SENT
    sims = [(R, x0, _bh_sim(R, Q0, x0)) for R in (1.5, 2.0, 5.0, 20.0, 100.0, 1000.0) for x0 in (0.01, 0.5, 3.0, 10.0)]
    worst = max(s[2] for s in sims)
    lin_ok = crr == SENT; sim_ok = worst < 1e-9
    check = lin_ok and sim_ok
    sens = "; ".join(f"q = {q}: {_w(_bh_loss(q)[0] == SENT, 'none', f'{_bh_loss(q)[0]:.3f}')}" for q in QGRID)
    rho_max = max(float(np.abs(np.linalg.eigvals(_bh_J(R, Q0))).max()) for R in (1.5, 2.0, 5.0, 20.0, 100.0, 1000.0))
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row("mem", d["system"] + "; model x_{n+1} = R x_n / (1 + (R - 1) M_n), M_n = (1 - q) x_n + q M_{n-1} (batch_31's A6 form), equilibrium (1, 1); linear scan R in (1, 1000] and nonlinear iteration",
                    source=_src(i),
                    Q=d["Q"] + f" (computed as: no eigenvalue of modulus >= 1 at the equilibrium for R in (1, 1000], encoded {SENT:.1f} when none; and every iterate from 4 initial densities at 6 values of R converges to 1)",
                    ingredient=d["ingredient"] + " (bounded Frechet mean of past densities, geometric weights q^k, q = 0.5)",
                    null=d["null"] + " (q = 0: Beverton-Holt, slope 1/R at the equilibrium)",
                    domain=d["H0"] + f" (encoded {SENT:.1f}: no loss of stability)",
                    numbers=f"first loss of stability: with memory {_w(crr == SENT, 'none on the scan', f'R = {crr:.3f} ({kind})')}; without memory {_w(null == SENT, 'none on the scan', f'R = {null:.3f} ({kind0})')}; largest spectral radius at R in (1.5, 2, 5, 20, 100, 1000) with memory {rho_max:.4f}; nonlinear iteration: largest |x - 1| after 3000 steps over 24 runs {worst:.2e}; q-grid sensitivity (first loss): {sens}",
                    tg=f"{crr:.3f} vs null {null:.3f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"Beverton-Holt's global stability, encoded {domain:.1f}: {_w(rel(crr, domain) <= TOL_N, 'agree', 'differ')}",
                    tc=f"no loss of stability on the scan: {_w(lin_ok, 'holds', 'fails')}; nonlinear convergence (|x - 1| < 1e-9): {_w(sim_ok, 'holds', 'fails')} -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=f"the Jacobian with memory has determinant q and trace 1 + q - (1 - q)(R - 1)/R, which stays inside the Jury triangle for every R > 1, so the monotone map stays stable {_w(check, 'as the scan and the iteration confirm', 'but the numbers disagree (see T-C)')}; memory {_w(crr == null, 'changes nothing about the threshold (there is none either way)', 'moves a threshold')}: the ingredient does no work on a map that cannot overshoot",
                    weakness="the sentinel encoding makes T-G agree whenever neither model loses stability, so REDUNDANT-IG here means 'no threshold to move', not a measured agreement; where A6 acts (the recruitment denominator only) is one modelling choice",
                    elegance="", child="")


# ---------------------------------------------------------------- P03-2 Nicholson's blowflies
PD_CANON = 8.0 / 0.175          # Gurney, Blythe and Nisbet 1980 values as commonly quoted (P = 8/day, delta = 0.175/day; not fetched)


def _b(Pd):
    return math.log(Pd) - 1.0       # f'(M*) = -delta b at the equilibrium M* = N0 ln(P/delta); time in units of 1/delta


def _hopf_pure(b):
    if b <= 1.0:
        return math.inf
    w = math.sqrt(b * b - 1.0)
    return (math.pi - math.atan(w)) / w


def _hopf_a6(b, q, lagged=True):
    """Characteristic lambda + 1 = -b K(lambda). lagged (primary): M(t) = (1-q) N(t-tau) + q M(t-tau), K = (1-q) z/(1 - q z);
    alternative: M(t) = (1-q) N(t) + q M(t-tau), K = (1-q)/(1 - q z); z = exp(-lambda tau). Returns the smallest delta*tau
    at which a root reaches the imaginary axis, inf if none exists for any tau."""
    if lagged:
        s = (q - b * (1 - q)) ** 2 - 1.0
        if s <= 0:
            return math.inf
        w = math.sqrt(s / (1 - q * q))
        z = complex(1.0, w) / (q * complex(1.0, w) - b * (1 - q))
    else:
        # (1 + i w)(1 - q z) = -b (1 - q) -> z = ((1 + i w) + b (1 - q)) / (q (1 + i w))
        # |z| = 1: (1 + b(1-q))^2 + w^2 = q^2 (1 + w^2) -> w^2 (1 - q^2) = q^2 - (1 + b(1-q))^2 < 0 always
        s = q * q - (1 + b * (1 - q)) ** 2
        if s <= 0:
            return math.inf
        w = math.sqrt(s / (1 - q * q)); z = (complex(1.0, w) + b * (1 - q)) / (q * complex(1.0, w))
    wt = (-math.atan2(z.imag, z.real)) % (2 * math.pi)
    if wt == 0.0:
        wt = 2 * math.pi
    return wt / w


def _hopf_gamma(b, q):
    """Gamma kernel with the A6 (lagged) kernel's mean tau/(1-q) and variance q tau^2/(1-q)^2: shape p = 1/q, scale
    theta = q tau/(1-q). lambda + 1 = -b (1 + theta lambda)^(-p). Smallest delta*tau with a root on the imaginary axis."""
    p = 1.0 / q
    lo = math.tan(math.pi / (2 * p)) if p > 1 else math.inf
    if not math.isfinite(lo):
        return math.inf
    hi = math.tan(min(math.pi / p, math.pi / 2 - 1e-12))
    uu = np.geomspace(lo * (1 + 1e-9), min(hi * (1 - 1e-9), 1e6), 20001)     # log grid: the magnitude's minimum sits near u = O(1)

    def m(u):
        w = math.tan(math.pi - p * math.atan(u)); return math.sqrt(1 + w * w) * (1 + u * u) ** (p / 2) - b
    vals = np.array([m(u) for u in uu])
    best = math.inf
    for k in range(len(uu) - 1):
        if vals[k] == 0 or vals[k] * vals[k + 1] < 0:
            u = brentq(m, uu[k], uu[k + 1], xtol=1e-14)
            w = math.tan(math.pi - p * math.atan(u)); theta = u / w
            best = min(best, theta * (1 - q) / q)
    return best


def _enc(x):
    return SENT if not math.isfinite(x) or x > SENT else x


def _fmt(x):
    return _w(math.isfinite(x) and x <= SENT, f"{x:.4f}", "none")


def _nich_sim(Pd, q, dtau, m=50, horizon=400.0, pert=0.1):
    """Exponential integrator on a grid h = tau/m (time in 1/delta) over max(`horizon`, 300 tau); returns max |N/N* - 1| over the last 5 tau."""
    tau = dtau; h = tau / m; Ns = math.log(Pd); n = m * int(math.ceil(max(horizon, 300.0 * tau) / tau))   # at least 300 tau: the memory's slow modes decay per tau
    N = np.empty(n + m + 1); M = np.empty(n + m + 1)
    N[:m + 1] = Ns * (1 + pert); M[:m + 1] = Ns * (1 + pert)
    eh = math.exp(-h); c1 = 1 - eh; c2 = 1 - c1 / h
    F = lambda Mv: Pd * Mv * math.exp(-Mv)
    for k in range(m, n + m):
        j = k + 1
        M[j] = (1 - q) * N[j - m] + q * M[j - m]                       # q = 0: the pure delay
        F0 = F(M[k]); F1 = F(M[j])
        N[j] = N[k] * eh + F0 * c1 + (F1 - F0) * c2
    return float(np.abs(N[-5 * m:] / Ns - 1).max())


def r2():
    i = "P03-2"; d = _decl(i)
    b = _b(PD_CANON)
    th_null = _hopf_pure(b); th_crr = _hopf_a6(b, Q0); th_dom = _hopf_gamma(b, Q0); th_alt = _hopf_a6(b, Q0, lagged=False)
    crr, null, domain = _enc(th_crr), _enc(th_null), _enc(th_dom)
    check = crr > null * (1 + TOL_G)
    amp_null = [(x, _nich_sim(PD_CANON, 0.0, x)) for x in (0.8 * th_null, 1.2 * th_null, 2.0, 10.0)]
    amp_crr = [(x, _nich_sim(PD_CANON, Q0, x)) for x in (0.5, 2.0, 10.0, 50.0)]
    sim_ok = amp_null[0][1] < 1e-3 and amp_null[1][1] > 1e-3 and (all(a < 1e-3 for _, a in amp_crr) if crr == SENT else True)
    sens_q = "; ".join(f"q = {q}: A6 {_fmt(_hopf_a6(b, q))}, moment-matched gamma (shape {1 / q:.2f}) {_fmt(_hopf_gamma(b, q))}" for q in QGRID)
    def _lab(Pd):
        c, n_, g = _enc(_hopf_a6(_b(Pd), Q0)), _enc(_hopf_pure(_b(Pd))), _enc(_hopf_gamma(_b(Pd), Q0))
        return outcome(crr=c, null=n_, domain=g, check=c > n_ * (1 + TOL_G))
    sens_P = "; ".join(f"P/delta = {Pd:.2f} (b = {_b(Pd):.3f}): pure {_fmt(_hopf_pure(_b(Pd)))}, A6 {_fmt(_hopf_a6(_b(Pd), Q0))}, gamma {_fmt(_hopf_gamma(_b(Pd), Q0))}, label there {_lab(Pd)}"
                       for Pd in (math.exp(3), PD_CANON, math.exp(5), math.exp(8), math.exp(10)))
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row("mem", d["system"] + f"; model dN/dt = P M e^(-M/N0) - delta N with M(t) = (1 - q) N(t - tau) + q M(t - tau) (the occasion is one delay tau; q = 0 is the pure delay), P/delta = {PD_CANON:.4f}; Hopf threshold on delta*tau from the characteristic equation on the imaginary axis, checked by integrating the delay equation",
                    source=_src(i),
                    Q=d["Q"] + f" (computed as: delta*tau at the first imaginary-axis root with memory against the pure delay; 'stabilising' means larger; encoded {SENT:.1f} when no root exists for any tau)",
                    ingredient=d["ingredient"] + " (bounded Frechet mean over past occasions of length tau, geometric weights, q = 0.5)",
                    null=d["null"] + " (Nicholson: lambda + delta = -delta b e^(-lambda tau))",
                    domain=d["H0"] + " (computed for the gamma kernel with the A6 kernel's mean 2 tau and variance 2 tau^2: shape 2, the 'strong' kernel)",
                    numbers=f"b = ln(P/delta) - 1 = {b:.4f}; Hopf delta*tau: pure delay {_fmt(th_null)}, A6 memory {_fmt(th_crr)}, moment-matched gamma {_fmt(th_dom)}; alternative reading M(t) = (1 - q) N(t) + q M(t - tau) {_fmt(th_alt)}; delay-equation integration, max |N/N* - 1| over the last 5 tau: pure delay at delta*tau = "
                            + ", ".join(f"{x:.4f}: {a:.2e}" for x, a in amp_null) + "; A6 at delta*tau = " + ", ".join(f"{x:.1f}: {a:.2e}" for x, a in amp_crr)
                            + f" (integration agrees with the characteristic equation: {_w(sim_ok, 'yes', 'NO')}); q-grid sensitivity: {sens_q}; P/delta sensitivity (q = 0.5): {sens_P}",
                    tg=f"{crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"moment-matched gamma kernel {domain:.4f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"threshold with memory {crr:.4f} > 1.01 x pure-delay threshold {null:.4f}: {_w(check, 'holds', 'fails')} -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=f"at the canonical P/delta the remembered density {_w(crr == SENT, 'never loses stability (the effective gain b(1 - q) - q stays below 1)', f'loses stability at delta*tau = {crr:.4f}')} while the pure delay loses it at {null:.4f}; the gamma kernel with the same mean and variance {_w(domain == SENT, 'is also never unstable here (the strong kernel needs b > 8)', f'loses it at {domain:.4f}')}, so the distributed-delay literature {_w(rel(crr, domain) <= TOL_N, 'already carries the qualitative answer', 'gives a different threshold')}; the P/delta sweep shows where finite thresholds appear and how the label would change there",
                    weakness=f"DEVIATION (modelling choice a reader could contest): the A6 occasion is taken as one delay tau, so q = 0 returns the pure delay (the declared null); the alternative reading with the current density inside the memory gives {_fmt(th_alt)}. The gamma comparator is moment-matched (my choice; declared.py names no shape). At the canonical P/delta both memory and gamma read 'none', so T-N agrees through the sentinel, not a measured number; P = 8, delta = 0.175 are quoted from memory (R10: not fetched)",
                    elegance="", child="")


# ---------------------------------------------------------------- P03-3 cobweb with A6 expectations
def _cobweb_coef(r, q):
    """p_t = (A - b pe_t)/d; pe_t = M_{t-1}; M_t = (1-q) p_t + q M_{t-1}. Linear coefficient of M_t on M_{t-1}."""
    A = 10.0
    F = lambda M: (1 - q) * (A - r * M) + q * M        # d = 1 w.l.o.g., r = b/d
    return (F(1.0 + 1e-6) - F(1.0 - 1e-6)) / 2e-6


def _cobweb_rc(q, grid=np.arange(0.0005, 10.0 + 1e-12, 0.0005)):
    for r in grid:
        if abs(_cobweb_coef(r, q)) >= 1.0 - 1e-9:
            return float(r)
    return SENT


def r3():
    i = "P03-3"; d = _decl(i)
    crr = _cobweb_rc(Q0); null = _cobweb_rc(0.0); w = 1 - Q0; domain = (2 - w) / w
    check = crr > 1.0 * (1 + TOL_G)
    at12 = _cobweb_coef(1.2, Q0); at12n = _cobweb_coef(1.2, 0.0)
    sens = "; ".join(f"q = {q}: r_c {_cobweb_rc(q):.4f} (Nerlove {(1 + q) / (1 - q):.4f})" for q in QGRID)
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row("mem", d["system"] + "; model: demand D = a - d p, supply S = c + b pe, market clearing, pe_t = M_{t-1}, M_t = (1 - q) p_t + q M_{t-1}; scan of the slope ratio r = b/d on a 0.0005 grid",
                    source=_src(i),
                    Q=d["Q"] + " (computed as: the first r = b/d at which the price map's coefficient reaches modulus 1, against 1.01)",
                    ingredient=d["ingredient"] + " (the expected price is the bounded Frechet mean of past prices, geometric weights, q = 0.5)",
                    null=d["null"] + " (pe_t = p_{t-1}: the cobweb theorem, r_c = 1)",
                    domain=d["H0"] + f" (w = 1 - q = {w}: (2 - w)/w = {domain:.4f})",
                    numbers=f"r_c: A6 {crr:.4f}, naive {null:.4f}, Nerlove {domain:.4f}; at the declared r = 1.2 the price coefficient is {at12:.4f} with memory ({_w(abs(at12) < 1, 'stable', 'unstable')}) and {at12n:.4f} without ({_w(abs(at12n) < 1, 'stable', 'unstable')}); q-grid sensitivity: {sens}",
                    tg=f"r_c {crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"Nerlove's bound {domain:.4f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"r_c = {crr:.4f} > 1.01: {_w(check, 'holds', 'fails')} -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=f"A6 expectations are Nerlove's adaptive expectations with w = 1 - q, so the critical slope ratio moves from {null:.4f} to {crr:.4f}, the domain's (2 - w)/w = {domain:.4f}; the market that explodes at r = 1.2 with naive expectations {_w(abs(at12) < 1 and abs(at12n) >= 1, 'settles', 'does not settle')} with remembered prices",
                    weakness="the identity A6 = adaptive expectations is exact, so this row is the domain's theorem read in CRR's words",
                    elegance=_w(check and abs(at12) < 1 <= abs(at12n), "Farmers who plant by a remembered average of past prices, not last year's price alone, stop the boom-and-bust swing that last-year's-price planting makes.", ""),
                    child=_w(check and abs(at12) < 1 <= abs(at12n), "If farmers only look at last year's price, they all plant too much, then too little, then too much. If they remember several years, the swings calm down.", ""))


# ---------------------------------------------------------------- P03-4 SIS with remembered prevalence
BETA, GAMMA, KSIS = 0.3, 0.1, 50.0


def _tm(q, occ=1.0 / GAMMA):
    return occ / math.log(1.0 / q)      # q per occasion (one mean infectious period) <-> exp(-occ/T_m) = q


def _sis(q, k=KSIS):
    Is = brentq(lambda I: BETA * (1 - I) / (1 + k * I) - GAMMA, 1e-12, 1 - 1e-12, xtol=1e-15)
    f2 = lambda z: np.array([BETA * (1 - z[0]) * z[0] / (1 + k * z[1]) - GAMMA * z[0], (z[0] - z[1]) / _tm(q)])
    f1 = lambda z: np.array([BETA * (1 - z[0]) * z[0] / (1 + k * z[0]) - GAMMA * z[0]])
    ev = np.linalg.eigvals(_jac(f2, [Is, Is], 1e-8)); ev0 = np.linalg.eigvals(_jac(f1, [Is], 1e-8))
    lead = ev[int(np.argmax(ev.real))]; lead0 = ev0[int(np.argmax(ev0.real))]
    return Is, lead, lead0, f2, f1


def _crossings(f, z0, zs, idx=0, dt=0.05, days=3000.0):
    z = np.array(z0, float); s_prev = np.sign(z[idx] - zs); n = 0
    for _ in range(int(round(days / dt))):
        k1 = f(z); k2 = f(z + dt / 2 * k1); k3 = f(z + dt / 2 * k2); k4 = f(z + dt * k3)
        z = z + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        s = np.sign(z[idx] - zs)
        if s != 0 and s != s_prev:
            n += 1; s_prev = s
    return n, abs(z[idx] - zs)


def r4():
    i = "P03-4"; d = _decl(i)
    Is, lead, lead0, f2, f1 = _sis(Q0)
    crr = abs(lead.imag); null = abs(lead0.imag)
    check = crr > 1e-12 and lead.real < 0 and null == 0.0
    nc, fin = _crossings(f2, [0.01, 0.01], Is); nc0, fin0 = _crossings(f1, [0.01], Is)
    sens_q = "; ".join(f"q = {q} (T_m {_tm(q):.2f} d): lambda {_sis(q)[1].real:.5f} {_sis(q)[1].imag:+.5f}i" for q in QGRID)
    sens_k = "; ".join(f"k = {k:g}: lambda {_sis(Q0, k)[1].real:.5f} {_sis(Q0, k)[1].imag:+.5f}i" for k in (5.0, 50.0, 500.0))
    out = outcome(crr=crr, null=null, domain=None, check=check)
    return make_row("mem", d["system"] + f"; model dI/dt = beta (1 - I) I/(1 + k P) - gamma I, k = {KSIS:g}, dP/dt = (I - P)/T_m with q = 0.5 per occasion of one mean infectious period 1/gamma, so T_m = (1/gamma)/ln(1/q) = {_tm(Q0):.4f} d; Jacobian at the endemic state by central differences; RK4 dt 0.05 d over 3000 d from I = P = 0.01",
                    source=_src(i),
                    Q=d["Q"] + " (computed as: |Im| of the leading eigenvalue at the endemic state with memory, Re < 0, against the one-dimensional model's)",
                    ingredient=d["ingredient"] + " (prevalence remembered with P3's geometric weights, continuous-time kernel)",
                    null=d["null"] + " (P = I: one-dimensional SIS, a real eigenvalue)",
                    domain=d["H0"],
                    numbers=f"endemic I* = {Is:.6f}; leading eigenvalue with memory {lead.real:.6f} {lead.imag:+.6f}i, without {lead0.real:.6f} {lead0.imag:+.6f}i; crossings of I* in the integration: with memory {nc} (final |I - I*| {fin:.2e}), without {nc0} (final {fin0:.2e}); q-grid sensitivity: {sens_q}; contact-response sensitivity (q = 0.5): {sens_k}",
                    tg=f"|Im| {crr:.6f} vs null {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no theorem cited",
                    tc=f"complex leading eigenvalue with Re < 0 under memory and a real one without: {_w(check, 'holds', 'fails')} -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=f"with remembered prevalence the endemic state is a {_w(check, 'stable focus', 'node or unstable point')} (the integration crosses I* {nc} times before settling, against {nc0} without memory): contact rebounds after prevalence has already fallen, the mechanism behind behavioural waves; information-dependent contact models with exponential memory kernels are an existing literature (d'Onofrio and Manfredi's line of work, named from memory, not fetched), so ADDS here is a candidate that a literature check may demote",
                    weakness=f"DEVIATION (modelling choice a reader could contest): q per occasion is mapped to a continuous exponential kernel with the occasion equal to one mean infectious period; the contact response k = {KSIS:g} is not in declared.py (taken from batch_31 row 2). A one-dimensional model can never oscillate, so 'absent without memory' is structural; any second variable with a lag gives the same focus",
                    elegance="", child="")


# ---------------------------------------------------------------- P03-5 Goodwin with remembered employment
ALPHA, BETA_L, SIGMA, GAM_PH, RHO_PH = 0.02, 0.01, 3.0, 0.9, 1.0     # Phillips curve Phi(v) = RHO_PH v - GAM_PH (linear)


def _goodwin(q):
    vs = (ALPHA + GAM_PH) / RHO_PH; us = 1 - SIGMA * (ALPHA + BETA_L)
    T = 1.0 / math.log(1.0 / q) if q > 0 else 0.0                       # occasion: one year (the annual wage round)
    f3 = lambda z: np.array([z[0] * (RHO_PH * z[2] - GAM_PH - ALPHA), z[1] * ((1 - z[0]) / SIGMA - ALPHA - BETA_L), (z[1] - z[2]) / T])
    f2 = lambda z: np.array([z[0] * (RHO_PH * z[1] - GAM_PH - ALPHA), z[1] * ((1 - z[0]) / SIGMA - ALPHA - BETA_L)])
    J3 = _jac(f3, [us, vs, vs], 1e-7); J2 = _jac(f2, [us, vs], 1e-7)
    ev3 = np.linalg.eigvals(J3); ev2 = np.linalg.eigvals(J2)
    c3 = ev3[np.abs(ev3.imag) > 1e-12]; c2 = ev2[np.abs(ev2.imag) > 1e-12]
    l3 = c3[0] if len(c3) else ev3[int(np.argmax(ev3.real))]; l2 = c2[0] if len(c2) else ev2[0]
    return us, vs, T, l3, l2, np.poly(J3), f3, f2


def _amp_ratio(f, z0, zs, dt=0.01, years=200.0):
    z = np.array(z0, float); d0 = float(np.linalg.norm(z[:2] - zs)); n = int(round(years / dt)); late = []
    for k in range(n):
        k1 = f(z); k2 = f(z + dt / 2 * k1); k3 = f(z + dt / 2 * k2); k4 = f(z + dt * k3)
        z = z + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        if k >= n - int(round(20.0 / dt)):
            late.append(float(np.linalg.norm(z[:2] - zs)))
    return max(late) / d0


def r5():
    i = "P03-5"; d = _decl(i)
    us, vs, T, l3, l2, poly, f3, f2 = _goodwin(Q0)
    crr = l3.real / abs(l3.imag); null = l2.real / abs(l2.imag); domain = 0.0
    check = crr < -TOL_G
    zs = np.array([us, vs]); z0 = [us * 1.01, vs]
    a3 = _amp_ratio(f3, [us * 1.01, vs, vs], zs); a2 = _amp_ratio(f2, z0, zs)
    sens = "; ".join(f"q = {q} (T {_goodwin(q)[2]:.3f} y): Re/|Im| {_goodwin(q)[3].real / abs(_goodwin(q)[3].imag):+.5f}" for q in QGRID)
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    grow = crr > 0
    return make_row("mem", d["system"] + f"; model du/dt = u (Phi(M) - alpha), dv/dt = v ((1 - u)/sigma - alpha - beta), dM/dt = (v - M)/T, Phi(v) = {RHO_PH:g} v - {GAM_PH:g}, alpha = {ALPHA}, beta = {BETA_L}, sigma = {SIGMA:g}; q = 0.5 per occasion of one year, T = 1/ln(1/q) = {T:.4f} y; Jacobian by central differences; RK4 dt 0.01 y over 200 y from a 1 % wage-share displacement",
                    source=_src(i),
                    Q=d["Q"] + " (computed as: Re/|Im| of the complex eigenvalue pair at the equilibrium with memory, against -0.01)",
                    ingredient=d["ingredient"] + " (employment remembered with P3's geometric weights, continuous-time kernel)",
                    null=d["null"] + " (Goodwin 1967: a centre, Re = 0)",
                    domain=d["H0"] + f" (encoded Re/|Im| = {domain:.1f})",
                    numbers=f"equilibrium u* = {us:.4f}, v* = {vs:.4f}; complex pair with memory {l3.real:.6f} {l3.imag:+.6f}i (Re/|Im| {crr:+.6f}), without {l2.real:.2e} {l2.imag:+.6f}i (Re/|Im| {null:+.2e}); characteristic polynomial with memory: lambda^3 + {poly[1]:.6f} lambda^2 + {poly[2]:.2e} lambda + {poly[3]:.6f}; late/initial displacement after 200 y: with memory {a3:.4f}, without {a2:.4f}; q-grid sensitivity: {sens}",
                    tg=f"Re/|Im| {crr:+.6f} vs null {null:+.2e}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"Goodwin's centre {domain:.1f}: {_w(rel(crr, domain) <= TOL_N, 'agree', 'differ')}",
                    tc=f"Re/|Im| = {crr:+.6f} < -0.01 (a stable focus): {_w(check, 'holds', 'fails')} -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=f"the lambda coefficient of the characteristic polynomial is {poly[2]:.2e}, zero up to differencing error (the remembered variable enters only through the wage equation and Goodwin's centre has no damping of its own), so Routh-Hurwitz (a1 a2 > a3) fails for every T > 0: memory turns the centre into an {_w(grow, 'unstable', 'stable')} focus, and the displacement {_w(a3 > 1, 'grows', 'shrinks')} by a factor {a3:.4f} over 200 years; a wage bargain on lagged employment is the known destabilising lag of the Goodwin literature (named, not fetched)",
                    weakness="the linear Phillips curve and the parameter values are my choices (declared.py names none); the sign of the result does not depend on them because the missing lambda term is structural",
                    elegance=_w(grow, "A swing that neither grows nor shrinks is pushed outward the moment it responds to where it was rather than where it is: a late push always adds energy.", ""),
                    child=_w(grow, "When you push a swing, you have to push at the right moment. If you push based on where the swing was a moment ago, you push late, and the swing goes higher and higher.", ""))


def main():
    return run_batch("PRED70 batch P03: remembered state (A6) and stability thresholds (Predictions70/DECLARATION.md; prompt-log entry 234)",
                     [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
