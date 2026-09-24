"""Synthesis batch 31: MEMORY (A6 with P3 weights) in five classic threshold models (owner request 2026-09-24, prompt-log
entry 131). Declared blind in DECLARATION_31_32.md (sha256 86cfb0eb..., OpenTimestamps-stamped, pushed in commit 1232815
before this file existed). [1] Ricker stock-recruitment with remembered density; [2] SIR with behavioural distancing on
remembered prevalence; [3] optimal-velocity traffic with a remembered headway; [4] Samuelson's multiplier-accelerator with
permanent-income consumption; [5] the continuous logistic equation with remembered density. Literature named by name and
year only (R10): Ricker 1954; Beverton and Holt 1957; Bando et al. 1995; Samuelson 1939; Friedman 1957; Hutchinson 1948;
MacDonald 1978; Cushing 1977. Deterministic; under 60 s."""
import math
import sys

import numpy as np
from scipy.special import lambertw

from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch


def _w(cond, yes, no):
    return yes if cond else no


# ---------------------------------------------------------------- [1] Ricker with remembered density
def _ricker_rc(q, grid=np.arange(0.001, 20.0 + 1e-12, 0.001)):
    for r in grid:
        J = np.array([[1 - r * (1 - q), -r * q], [1 - q, q]])                   # state (x_n, M_{n-1}); equilibrium (1, 1)
        ev = np.linalg.eigvals(J); k = int(np.argmax(np.abs(ev)))
        if abs(ev[k]) >= 1.0 - 1e-12:
            kind = "flip (eigenvalue -1)" if abs(ev[k].imag) < 1e-9 and ev[k].real < 0 else ("Neimark-Sacker" if abs(ev[k].imag) >= 1e-9 else "fold (eigenvalue +1)")
            return float(r), kind
    return float("inf"), "none on the scan"


def _bh_loss(grid=np.arange(1.001, 20.0 + 1e-12, 0.001)):
    for r in grid:
        if abs(1.0 / r) >= 1.0 - 1e-12: return float(r)                          # Beverton-Holt at q = 0: slope at the equilibrium is 1/r
    return float("inf")


def r1():
    rc, kind = _ricker_rc(0.5); r0, kind0 = _ricker_rc(0.0); bh = _bh_loss()
    crr, null = rc, r0; check = rc > 2.02
    out = outcome(crr=crr, null=null, domain=None, check=check)
    return make_row("mem", "Ricker stock-recruitment x_{n+1} = x_n exp(r(1 - M_n)) with the remembered density M_n = (1 - q) x_n + q M_{n-1}, q = 0.5 (A6 with P3 weights), equilibrium (1, 1)",
                    source="DECLARATION_31_32.md row 31-1 (new system; MEMORY class)",
                    Q="the equilibrium first loses stability at r_c > 2.02: remembering density stabilises the Ricker map, as memory raised the cardiac-alternans threshold (batch 12 row 2)",
                    ingredient="A6 (the next occasion is seeded from the settled past at bounded strength) with P3's geometric age weights",
                    null="q = 0: the Ricker map, first loss of stability at r = 2",
                    domain="Ricker's flip at r = 2 (the null's value); no theorem cited for the memory variant",
                    numbers=f"r_c(q = 0.5) = {rc:.3f} ({kind}); r_c(q = 0) = {r0:.3f} ({kind0}); surrogate Beverton-Holt at q = 0: loss of stability on (1, 20]: {_w(math.isinf(bh), 'none (globally stable, as the domain says)', f'at r = {bh:.3f} (VIOLATION)')}",
                    tg=f"r_c {crr:.3f} vs null {null:.3f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no theorem cited for the memory variant (Ricker's r = 2 is the null's)",
                    tc=f"r_c(0.5) > 2.02: {_w(check, 'holds', 'fails')}",
                    out=out,
                    reading=f"memory moves the Ricker map's first instability from r = {r0:.3f} to r = {rc:.3f} ({kind}); a complex pair cannot cross because the Jacobian's determinant is q < 1, so the only exit is the flip, pushed out by averaging, the same mechanism as the alternans row: A6 damps the period-2 alternation of a one-dimensional map; whether fisheries' 'memory' models (lagged or averaged stock indices in harvest rules) already carry this threshold was not checked",
                    weakness="the remembered density enters the recruitment exponent only (one modelling choice of where A6 acts); the same flip-threshold algebra appeared in batch 12 row 2, so this row is not independent of it: it is the same lemma on a second map",
                    elegance="A fish population that reacts to how crowded it has been lately, not only to how crowded it is now, stops flipping between boom and bust until it is pushed much harder.",
                    child="Imagine fish that remember last year's crowding as well as this year's. They do not overreact, so the population stops jumping up and down every year.")


# ---------------------------------------------------------------- [2] SIR with remembered prevalence
def _sir_peak(k, Tm, beta0=0.3, gamma=0.1, I0=1e-4, dt=0.01, days=400.0):
    S, I, P = 1.0 - I0, I0, I0; peak = I; n = int(round(days / dt))
    def f(S, I, P):
        Pe = I if Tm == 0 else P; b = beta0 / (1.0 + k * Pe)
        return -b * S * I, b * S * I - gamma * I, (0.0 if Tm == 0 else (I - P) / Tm)
    for _ in range(n):
        a = f(S, I, P); b_ = f(S + 0.5 * dt * a[0], I + 0.5 * dt * a[1], P + 0.5 * dt * a[2])
        c = f(S + 0.5 * dt * b_[0], I + 0.5 * dt * b_[1], P + 0.5 * dt * b_[2]); d = f(S + dt * c[0], I + dt * c[1], P + dt * c[2])
        S += dt * (a[0] + 2 * b_[0] + 2 * c[0] + d[0]) / 6; I += dt * (a[1] + 2 * b_[1] + 2 * c[1] + d[1]) / 6; P += dt * (a[2] + 2 * b_[2] + 2 * c[2] + d[2]) / 6
        peak = max(peak, I)
    return peak


def r2():
    pm = _sir_peak(50.0, 10.0); p0 = _sir_peak(50.0, 0.0); sm = _sir_peak(0.0, 10.0); s0 = _sir_peak(0.0, 0.0)
    crr, null = pm, p0; ratio = pm / p0; check = ratio > 1.01; sur_ok = rel(sm, s0) <= 1e-9
    out = outcome(crr=crr, null=null, domain=None, check=check)
    return make_row("mem", "SIR epidemic (beta0 = 0.3/day, gamma = 0.1/day, R0 = 3, I0 = 1e-4) with behavioural distancing beta = beta0/(1 + k P), k = 50, P the A6-remembered prevalence dP/dt = (I - P)/T_m, T_m = 10 days; RK4 dt 0.01 over 400 days",
                    source="DECLARATION_31_32.md row 31-2 (new system; MEMORY class)",
                    Q="with remembered prevalence the epidemic's peak prevalence exceeds the instantaneous-response peak by more than 1 %: a lagged response overshoots",
                    ingredient="A6 with P3's exponential kernel (mean age T_m) as the prevalence the population responds to",
                    null="instantaneous response, P = I (the standard behavioural SIR)",
                    domain="none for the memory variant",
                    numbers=f"peak prevalence: remembered {pm:.6f}, instantaneous {p0:.6f}, ratio {ratio:.4f}; surrogate k = 0 (no response): {sm:.8f} against {s0:.8f}, relative difference {rel(sm, s0):.2e} ({_w(sur_ok, 'memory cannot matter, as required', 'VIOLATION')})",
                    tg=f"peak {crr:.6f} vs null {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no theorem cited for the memory variant",
                    tc=f"peak ratio above 1.01: {_w(check, 'holds', 'fails')}",
                    out=out,
                    reading=f"a population that distances on remembered prevalence reacts late, so the peak is {_w(ratio > 1, 'higher', 'lower')} than with instantaneous distancing (ratio {ratio:.4f}); behavioural epidemiology with memory kernels (information-dependent contact rates) is an existing literature that may already contain this comparison (not fetched)",
                    weakness="one parameter set; the direction may reverse at other k or T_m; the memory kernel is exponential (P3) by construction",
                    elegance="", child="")


# ---------------------------------------------------------------- [3] optimal-velocity traffic with a remembered headway
def _ov_threshold(Tm, a=1.0, step=0.0005, vmax=2.0):
    ks = np.linspace(math.pi / 400, math.pi, 400); z = np.exp(1j * ks) - 1.0
    for Vp in np.arange(step, vmax + 1e-12, step):
        if Tm == 0:
            M = np.zeros((len(ks), 2, 2), complex); M[:, 0, 1] = 1.0; M[:, 1, 0] = a * Vp * z; M[:, 1, 1] = -a
        else:
            M = np.zeros((len(ks), 3, 3), complex); M[:, 0, 1] = 1.0; M[:, 1, 1] = -a; M[:, 1, 2] = a * Vp
            M[:, 2, 0] = z / Tm; M[:, 2, 2] = -1.0 / Tm
        if np.linalg.eigvals(M).real.max() > 1e-9: return float(Vp)
    return float("inf")


def r3():
    vm = _ov_threshold(0.5); v0 = _ov_threshold(0.0)
    crr, null = vm, v0; check = vm < 0.495; sur_ok = abs(v0 - 0.5) <= 0.0005 + 1e-12
    out = outcome(crr=crr, null=null, domain=None, check=check)
    return make_row("mem", "optimal-velocity car following dv_n/dt = a (V(h~_n) - v_n), a = 1, with the A6-remembered headway dh~_n/dt = (h_n - h~_n)/T_m, T_m = 0.5; linear string stability of the uniform flow",
                    source="DECLARATION_31_32.md row 31-3 (new system; MEMORY class)",
                    Q="the string-stability threshold on V'(h*) falls below Bando's a/2 = 0.5 by more than 1 %: a driver who responds to remembered headway destabilises the platoon",
                    ingredient="A6 with P3's exponential kernel (mean age T_m) as the headway the driver responds to",
                    null="T_m = 0: Bando's model, threshold V' = a/2",
                    domain="Bando et al. 1995 (a/2) for the null; none for the memory variant",
                    numbers=f"threshold V'_c: remembered headway {vm:.4f}, instantaneous {v0:.4f} (surrogate: within one scan step of 0.5: {_w(sur_ok, 'yes', 'VIOLATION')})",
                    tg=f"V'_c {crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no theorem cited for the memory variant",
                    tc=f"V'_c < 0.495: {_w(check, 'holds', 'fails')}",
                    out=out,
                    reading=f"remembering headway {_w(vm < v0, 'lowers', 'raises')} the platoon's stability threshold from {v0:.4f} to {vm:.4f}; the traffic literature treats reaction delay (a pure delay) and finds it destabilising; an exponentially weighted perceived headway is a distributed delay, and whether its threshold is already in that literature (e.g. models with memory of past headways) was not checked",
                    weakness="linear stability only; one T_m; the remembered quantity is the headway, not the relative velocity (one modelling choice)",
                    elegance="", child="")


# ---------------------------------------------------------------- [4] Samuelson with permanent-income consumption
def _samuelson_vc(q, c=0.8, grid=np.arange(0.001, 10.0 + 1e-12, 0.001)):
    for v in grid:
        a1 = (1 - q) * c * (1 + v) + q; a2 = -(1 - q) * c * v                   # P_t = a1 P_{t-1} + a2 P_{t-2}
        if np.abs(np.linalg.eigvals(np.array([[a1, a2], [1.0, 0.0]]))).max() >= 1.0 - 1e-12: return float(v)
    return float("inf")


def r4():
    vq = _samuelson_vc(0.5); v0 = _samuelson_vc(0.0)
    crr, null = vq, v0; check = vq > 1.2625; sur_ok = abs(v0 - 1.25) <= 0.001 + 1e-12
    out = outcome(crr=crr, null=null, domain=None, check=check)
    return make_row("mem", "Samuelson's multiplier-accelerator Y_t = C_t + I_t + G, I_t = v (C_t - C_{t-1}), with permanent-income consumption C_t = c P_{t-1}, P_t = (1 - q) Y_t + q P_{t-1}, c = 0.8, q = 0.5",
                    source="DECLARATION_31_32.md row 31-4 (new system; MEMORY class)",
                    Q="the critical accelerator v_c exceeds Samuelson's 1/c = 1.25 by more than 1 %: permanent income stabilises the cycle",
                    ingredient="A6 with P3's geometric weights as the income consumption responds to (Friedman's permanent income is this kernel)",
                    null="q = 0: Samuelson's model, stability iff c v < 1",
                    domain="Samuelson 1939 (v_c = 1/c) for the null; none for the memory variant",
                    numbers=f"v_c: permanent income {vq:.3f}, Samuelson {v0:.3f} (surrogate: within one scan step of 1.25: {_w(sur_ok, 'yes', 'VIOLATION')})",
                    tg=f"v_c {crr:.3f} vs null {null:.3f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no theorem cited for the memory variant",
                    tc=f"v_c > 1.2625: {_w(check, 'holds', 'fails')}",
                    out=out,
                    reading=f"with consumption on permanent income the multiplier-accelerator stays stable up to v = {vq:.3f} against Samuelson's {v0:.3f}; the stabilising role of permanent income in accelerator models is plausibly in the macroeconomics literature (not fetched), so the label is a candidate and the direction may be the domain's",
                    weakness="the determinant of the recursion is (1 - q) c v, so the threshold follows in closed form, 1/((1 - q) c) when the loss is complex; a textbook exercise may already state it",
                    elegance="", child="")


# ---------------------------------------------------------------- [5] logistic with remembered density
def r5():
    grid = np.arange(0.01, 1000.0 + 1e-9, 0.01)
    lost = None
    for rT in grid:                                                             # T = 1: J = [[0, -r], [1, -1]]
        if np.linalg.eigvals(np.array([[0.0, -rT], [1.0, -1.0]])).real.max() >= 0: lost = float(rT); break
    crr = lost if lost is not None else 1000.0
    hut = None
    for rT in grid:                                                             # Hutchinson: rightmost root lambda tau = W0(-r tau)
        if lambertw(-rT, 0).real >= 0: hut = float(rT); break
    null = hut if hut is not None else 1000.0; domain = 1000.0
    check = lost is None; sur_ok = hut is not None and rel(hut, math.pi / 2) <= 0.01
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row("mem", "the continuous logistic equation dN/dt = r N (1 - M/K) with the A6-remembered density dM/dt = (N - M)/T; stability of N = K over r T in (0, 1000]",
                    source="DECLARATION_31_32.md row 31-5 (new system; MEMORY class; the weak-kernel theorem expected)",
                    Q="the equilibrium never loses stability: no Hopf bifurcation for r T in (0, 1000] (encoded 1000.0 when none is found)",
                    ingredient="A6 with P3's exponential kernel (mean age T) as the density the growth responds to",
                    null="Hutchinson's discrete delay tau = T: Hopf at r tau = pi/2",
                    domain="the weak (exponential) distributed-delay kernel is always stable (MacDonald 1978; Cushing 1977): encoded 1000.0",
                    numbers=f"loss of stability with remembered density: {_w(lost is None, 'none on the scan', f'at r T = {lost}')}; Hutchinson's delay: at r tau = {null:.4f} (pi/2 = {math.pi / 2:.4f}; surrogate {_w(sur_ok, 'within 1 %', 'VIOLATION')})",
                    tg=f"{crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the weak-kernel theorem gives {domain:.1f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"no eigenvalue with non-negative real part on the scan: {_w(check, 'holds', 'fails')}",
                    out=out,
                    reading="A6 in continuous time is the weak distributed-delay kernel, and the domain proved long ago that it never destabilises the logistic equilibrium, where the discrete delay does at r tau = pi/2: regeneration from the settled past at bounded strength is a stabilising memory, and population ecology already names it",
                    weakness="the Jacobian has trace -1/T and determinant r/T, so stability for all r T is immediate; the scan confirms what the algebra says",
                    elegance="Remembering the recent past smoothly, rather than reacting to one moment long ago, never makes a population swing out of control.",
                    child="If animals decide how many babies to have by remembering the last few seasons, the population settles down. If they only remember one season a long time ago, it can swing wildly.")


def main():
    return run_batch("Synthesis batch 31: MEMORY in five classic threshold models (prompt-log entry 131; DECLARATION_31_32.md)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
