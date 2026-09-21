"""Synthesis batch 26: rows 126-127 of QUEUE.md (prompt-log entry 61), the last batch (the queue ends at row 127).
Loop-gravity battery [7] the polymer harmonic oscillator (a Mathieu spectrum: the fundamental scale mu against the
state's own Fisher unit, D1's resolution as the domain's expansion parameter); [8] the instrument's unit estimator run
on the area spectrum's gaps (A1' run whole: the rejection clause against the ungated estimate).
Literature is cited by name and year only, not fetched (R10). No dataset opened (R2). Deterministic."""
import math
import sys

import numpy as np
from scipy import optimize, special
from scipy.signal import savgol_coeffs, savgol_filter

from crr.instrument.core import unit_sigma
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch


def _word(cond, yes, no):
    return yes if cond else no


# ---------------------------------------------------------------- 126 [7] the polymer oscillator: the lattice step in the state's own unit
def _E_level(n, mu):
    """Level n of H = sin^2(mu p)/(2 mu^2) + x^2/2 from the Mathieu characteristic value a_n (the source's model, AGENT_LOG 28)."""
    q = 1.0 / (4.0 * mu ** 4)
    return float((mu ** 2 / 2.0) * (special.mathieu_a(n, q) + 1.0 / (2.0 * mu ** 4)))


def _departure(n, mu):
    return (_E_level(n, mu) - (n + 0.5)) / (n + 0.5)


def _a_large_q(n, q):
    """Mathieu a_n(q) for large q (DLMF 28.8.1, eight terms), s = 2n + 1, h = sqrt(q); in polymer variables s/h = rho_n^2."""
    s = 2 * n + 1; h = math.sqrt(q)
    return sum([-2 * h * h, 2 * s * h, -(s * s + 1) / 8.0, -(s ** 3 + 3 * s) / (2 ** 7 * h), -(5 * s ** 4 + 34 * s * s + 9) / (2 ** 12 * h * h),
                -(33 * s ** 5 + 410 * s ** 3 + 405 * s) / (2 ** 17 * h ** 3), -(63 * s ** 6 + 1260 * s ** 4 + 2943 * s * s + 486) / (2 ** 20 * h ** 4),
                -(527 * s ** 7 + 15617 * s ** 5 + 69001 * s ** 3 + 41607 * s) / (2 ** 25 * h ** 5)])


def _departure_domain(n, mu):
    q = 1.0 / (4.0 * mu ** 4)
    return ((mu ** 2 / 2.0) * (_a_large_q(n, q) + 1.0 / (2.0 * mu ** 4)) - (n + 0.5)) / (n + 0.5)


def r1():
    mus, n_max = (0.2, 0.3), 6
    grid = []
    for mu in mus:
        for n in range(n_max):
            s = 2 * n + 1; E = _E_level(n, mu); d = _departure(n, mu)
            rho_n = mu * math.sqrt(4 * n + 2)                                  # lattice step over the state's Fisher unit 1/sqrt(4 Var p) = 1/sqrt(4n+2)
            rho_x = 2.0 * math.sqrt(2.0 * E) / mu                              # the swing (extent of one monotone half-cycle) in lattice steps
            grid.append((mu, n, E, d, rho_n, rho_x, -(rho_n ** 2 / 16.0) * (1.0 + 1.0 / s ** 2), _departure_domain(n, mu), E / (1.0 / (2.0 * mu ** 2))))
    mu0, n0 = 0.2, 5; s0 = 2 * n0 + 1                                          # reference level: the source's highest level at its smaller mu
    rho0 = mu0 * math.sqrt(4 * n0 + 2); d0 = _departure(n0, mu0); E0 = _E_level(n0, mu0); rhox0 = 2.0 * math.sqrt(2.0 * E0) / mu0
    partners = []                                                              # levels of other mu with the SAME rho_n as the reference
    for nb in (1, 2, 3, 4):
        sb = 2 * nb + 1; mub = rho0 / math.sqrt(4 * nb + 2); qb = 1.0 / (4.0 * mub ** 4)
        db = _departure(nb, mub); dom = _departure_domain(nb, mub)
        partners.append((nb, mub, qb, db, db / d0, (1.0 + 1.0 / sb ** 2) / (1.0 + 1.0 / s0 ** 2), dom, rel(db, dom), rel(db, d0) <= TOL_N))
    partners_x = []                                                            # levels of other mu with the SAME rho_x as the reference (the null reading)
    for nb in (2, 3, 4):
        mub = 2.0 * math.sqrt(2.0 * (nb + 0.5)) / rhox0
        for _ in range(30):
            mub = 2.0 * math.sqrt(2.0 * _E_level(nb, mub)) / rhox0
        partners_x.append((nb, mub, 1.0 / (4.0 * mub ** 4), 2.0 * math.sqrt(2.0 * _E_level(nb, mub)) / mub, mub * math.sqrt(4 * nb + 2), _departure(nb, mub), _departure(nb, mub) / d0))
    P = {p[0]: p for p in partners}; PX = {p[0]: p for p in partners_x}
    mu_n0 = rho0 / math.sqrt(2.0); q_n0 = 1.0 / (4.0 * mu_n0 ** 4)             # the n = 0 partner, outside the large-q regime (printed, not used)
    def _split(n, mu):                                                         # parity splitting b_(n+1) - a_n of level n (in a)
        q = 1.0 / (4.0 * mu ** 4); return float(special.mathieu_b(n + 1, q) - special.mathieu_a(n, q))
    split = {mu: _split(n0, mu) for mu in mus}; E_s = {mu: 1.0 / (2.0 * mu ** 2) for mu in mus}
    crr, null, dom = P[2][3], PX[2][5], P[2][6]                                # decisive: the n = 2 partner (its mu is the nearest to the source's 0.3)
    check = all(p[8] for p in partners)
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    tg_ok = rel(crr, null) <= TOL_G; tn_ok = rel(crr, dom) <= TOL_N
    n_pass = sum(p[8] for p in partners)
    return make_row("lqg",
        "The polymer harmonic oscillator H = sin^2(mu p)/(2 mu^2) + x^2/2 (the source's convention: q = 1/(4 mu^4), level n from the Mathieu characteristic value a_n, the b_(n+1) partner the other parity): the momentum is periodic (the Hamiltonian has period pi/mu in p), the position a lattice of step mu; levels n = 0..5 at mu = 0.2 and 0.3 (the source's grid) and at the mu values that hold the resolution fixed",
        source="theory/retrodictions/loop_gravity.txt [7] (DESCR)",
        Q="the fundamental scale enters level n only through its resolution rho_n (D1) with the state's own unit (A1'): sigma_n = 1/sqrt(QFI_n) = 1/sqrt(4n + 2), the quantum Cramer-Rao length of the n-th state under translation (the polymer step IS a translation, e^(i mu p)), so rho_n = mu/sigma_n = mu sqrt(4n + 2) = 2 mu Delta p_n, and the relative departure of E_n from n + 1/2 is one function of rho_n for every mu",
        ingredient="A1'/D1 (the unit as the system's own resolvable step, read as the quantum Cramer-Rao length of the state; rho = the lattice step counted in it)",
        null="D1 with the swing as the extent and the lattice as the unit: rho_x = 2 sqrt(2 E_n)/mu, the source battery's puncture-count reading of rho (extent over quantum)",
        domain="the Mathieu large-q expansion a_n(q) ~ -2q + 2s sqrt(q) - (s^2 + 1)/8 - (s^3 + 3s)/(2^7 sqrt(q)) - ... (Goldstein 1927; Meixner-Schafke 1954; DLMF 28.8.1; names and years only, not fetched, R10), which in polymer variables is a double series in rho_n^2 = s/sqrt(q) = 2 mu^2 s and 1/s^2: E_n/(n + 1/2) - 1 = -(rho_n^2/16)(1 + 1/s^2) - (rho_n^4/256)(1 + 3/s^2) - ...; first order is the (mu p)^2 correction of polymer quantum mechanics (Ashtekar-Fairhurst-Willis 2003, the source's citation)",
        numbers=(f"source grid (separatrix E_s = 1/(2 mu^2) = {E_s[0.2]:.3f} at mu = 0.2, {E_s[0.3]:.3f} at mu = 0.3; parity splitting b_6 - a_5 in a: {split[0.2]:.1e} at mu = 0.2, {split[0.3]:.3f} at mu = 0.3): "
                 + "; ".join(f"mu = {mu:g}, n = {n}: E = {E:.4f} (E/E_s = {es:.4f}), departure {d:+.5f}, rho_n = {rn:.4f} (rho_n^2/2 = {rn * rn / 2:.4f}), rho_x = {rx:.2f}, leading term -(rho_n^2/16)(1 + 1/s^2) = {lead:+.5f}, expansion {dm:+.5f}" for mu, n, E, d, rn, rx, lead, dm, es in grid)
                 + f"; reference mu = {mu0:g}, n = {n0}: departure {d0:+.5f}, rho_n = {rho0:.4f}, rho_x = {rhox0:.3f}; the n = 0 level with this rho_n would sit at mu = {mu_n0:.4f} (q = {q_n0:.2f}, outside the large-q regime, not used); fixed-rho_n partners: "
                 + "; ".join(f"n = {nb}, mu = {mub:.4f} (q = {qb:.1f}): departure {db:+.5f}, ratio to the reference {r:.4f} (domain leading-order factor (1 + 1/s^2)/(1 + 1/{s0}^2) = {f:.4f}), expansion {dm:+.5f} (relative difference {rd:.1e}), within {TOL_N:g}: {_word(ok, 'yes', 'no')}" for nb, mub, qb, db, r, f, dm, rd, ok in partners)
                 + "; fixed-rho_x partners: " + "; ".join(f"n = {nb}, mu = {mub:.4f} (q = {qb:.1f}, rho_x = {rx:.3f}, rho_n = {rn:.4f}): departure {db:+.5f}, ratio to the reference {r:.4f}" for nb, mub, qb, rx, rn, db, r in partners_x)),
        tg=f"departure at the fixed-rho_n partner (n = 2, mu = {P[2][1]:.4f}) {crr:+.5f} vs null, the fixed-rho_x partner (n = 2, mu = {PX[2][1]:.4f}) {null:+.5f}: {_word(tg_ok, 'agree', 'differ')}",
        tn=f"the Mathieu expansion gives {dom:+.5f} for that level (relative difference {rel(crr, dom):.1e}), and its variables are rho_n^2 and 1/s^2: the domain {_word(tn_ok, 'has', 'does not have')} Q",
        tc=f"every fixed-rho_n partner (n = 1..4) within {TOL_N:g} of the reference departure: {_word(check, 'holds', 'fails')} ({n_pass} of {len(partners)}: " + ", ".join(f"n = {nb} off by {abs(r - 1):.4f}" for nb, mub, qb, db, r, f, dm, rd, ok in partners) + ")",
        out=out,
        reading=(f"the unit does real work (T-G: at equal rho_n the departures agree to {abs(P[2][4] - 1):.3f}, at equal rho_x they differ by a factor {1 / PX[2][6]:.2f}), and the number it produces is the domain's own expansion parameter: rho_n^2 = 4 mu^2 <p^2>_n = (2 mu Delta p)^2 is (mu p)^2 in the state, and rho_n^2/2 is E/E_s, the pendulum's energy in units of its separatrix (rho_n^2/2 = {grid[5][4] ** 2 / 2:.4f} against E/E_s = {grid[5][8]:.4f} at the reference); "
                 f"the collapse onto one function of rho_n is the classical limit of the Mathieu asymptotics, and its breaking at fixed rho_n is the 1/s^2 series (at fixed rho_n, 1/s = 2 mu^2/rho_n^2, the effective Planck constant): the observed ratios {P[2][4]:.4f} (n = 2) and {P[4][4]:.4f} (n = 4) against the leading-order factors {P[2][5]:.4f} and {P[4][5]:.4f}. "
                 f"The synthesis reading is {out}: the domain has both the collapse and its breaking; the source row's 'fundamental unit against an estimated one' resolves, on this carrier, into a unit that is the domain's (mu, a translation step) counted in a unit that is information geometry's (the state's Cramer-Rao length), and their ratio is the domain's (mu p). The swing-over-lattice reading of rho (the source battery's puncture count) is not the variable the spectrum depends on"),
        weakness=(f"the source's grid and convention (levels from a_n; the b_(n+1) parity partner of level 5 is degenerate to {split[0.2]:.1e} in a at mu = 0.2 and split by {split[0.3]:.3f} at mu = 0.3, where E_5/E_s = {grid[11][8]:.3f}, near the separatrix); mu = 0.1 is outside the Mathieu routine's reliable range (AGENT_LOG 28) and the n = 0 partner (mu = {mu_n0:.4f}, q = {q_n0:.2f}) outside the large-q expansion, so partners are n = 1..4 with q from {P[1][2]:.1f} to {P[4][2]:.1f}; "
                  "the check is the harness's 1 % tolerance on a collapse the domain says is only asymptotic; the domain supplies a rotor (the momentum circle) on which A3 was not run, since the source row's clause is A1'/D1; the lattice step is taken as mu (the kinematical shift e^(i mu p)), while this Hamiltonian couples sites 2 mu apart, a factor that rescales rho_n and changes no ratio"),
        elegance="A grid only shows when it is coarser than the blur of what sits on it, and the oscillator's blur sharpens as it climbs, so the grid shows in the high levels first; one number, grid step over blur, says how much.",
        child="A picture made of tiny tiles looks smooth from far away; you only see the tiles when you draw something about as small as a tile. A swinging weight draws with a sharper and sharper pencil the higher it swings, so up high the tiles start to show through.")


# ---------------------------------------------------------------- 127 [8] the unit estimator on the area spectrum's gaps: A1' run whole
def _f4(j):
    """Fourth derivative of sqrt(j(j+1)) with respect to j (closed form)."""
    w = j * (j + 1.0); wp = 2.0 * j + 1.0
    return -(15.0 / 16.0) * w ** -3.5 * wp ** 4 + 4.5 * w ** -2.5 * wp ** 2 - 3.0 * w ** -1.5


def r2():
    js_all = np.arange(1, 400) / 2.0                                           # the source's all-j two-state counting for gamma
    gamma = optimize.brentq(lambda g: float(np.sum(2.0 * np.exp(-2.0 * math.pi * g * np.sqrt(js_all * (js_all + 1))))) - 1.0, 0.05, 1.0)
    js = np.arange(1, 61) / 2.0; A = 8.0 * math.pi * gamma * np.sqrt(js * (js + 1)); gaps = np.diff(A)
    g30 = gaps[:30]                                                            # the source's call: the first 30 gaps, window 9, order 2, MAD, no min_sigma
    sig = unit_sigma(g30)
    step_min = float(gaps.min()); step_lim = 4.0 * math.pi * gamma; A_gap = float(A[0]); slope_j = 8.0 * math.pi * gamma
    rejected = {}
    for name, ms in (("smallest gap", step_min), ("area gap A(1/2)", A_gap)):
        try:
            unit_sigma(g30, min_sigma=ms); rejected[name] = False
        except ValueError:
            rejected[name] = True
    windows = (5, 7, 9, 11, 13, 15, 17, 21); sweep = [(w, unit_sigma(g30, detrend_window=w)) for w in windows]
    lw = np.log([w for w, _ in sweep]); ls = np.log([s for _, s in sweep])
    slope_w = float(np.polyfit(lw, ls, 1)[0])
    c9 = savgol_coeffs(9, 2); k = np.arange(9) - 4; c4 = float(np.sum(c9 * k ** 4)) / 24.0
    i_int = np.arange(4, 26)                                                   # interior indices at window 9 (the edges use scipy's polynomial extrapolation)
    res = g30 - savgol_filter(g30, 9, 2)
    d4gap = slope_j * (_f4(js[i_int + 1]) - _f4(js[i_int])) * 0.5 ** 4          # d^4 gap/di^4: gap_i = A(j_i + 1/2) - A(j_i), d/di = (1/2) d/dj
    pred = -c4 * d4gap
    scale_res = 1.4826 * float(np.median(np.abs(res[i_int] - np.median(res[i_int]))))
    scale_pred = 1.4826 * float(np.median(np.abs(pred - np.median(pred))))
    lev9 = math.sqrt(1.0 - float(savgol_coeffs(9, 2)[4])); lev21 = math.sqrt(1.0 - float(savgol_coeffs(21, 2)[10]))   # leverage factors on white residuals (batch 06 row 4)
    src_gap_20, src_gap_30 = float(gaps[38]), float(gaps[58])                  # the last gaps of the source's j <= 20 and j <= 30 arrays
    crr, null, dom = step_min, sig, step_lim                                  # A1' whole: the estimate is rejected and the quantisation step is the unit
    check = rejected["smallest gap"] and rejected["area gap A(1/2)"] and slope_w > 2.0 and sig / step_min < 1e-3
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    tg_ok = rel(crr, null) <= TOL_G; tn_ok = rel(crr, dom) <= TOL_N
    return make_row("lqg",
        f"The LQG area spectrum A_j = 8 pi gamma sqrt(j(j+1)) l_P^2, gamma = {gamma:.4f} (the source's all-j two-state counting), j = 1/2 .. 30; the instrument's unit_sigma on its first 30 consecutive gaps as the source ran it (window 9, order 2, MAD, no quantisation step named), and as A1' is written (the quantisation step named, min_sigma)",
        source="theory/retrodictions/loop_gravity.txt [8] (DESCR)",
        Q="run whole, A1' on a fundamental spectrum returns the spectrum's own step: its estimated unit is the detrender's truncation error of the spectrum's closed form, it lies below the smallest change the spectrum has, and the clause 'reject the record if sigma is below the instrument's quantisation step' fires, so the unit of area is the named quantum, 4 pi gamma l_P^2 per half-step of j; the number the source printed exists only with that clause dropped",
        ingredient="A1' whole (one occasion statistic, the named detrender, 1.4826 MAD, and the rejection at the instrument's quantisation step, min_sigma), D1",
        null="the same estimator with the rejection clause dropped (the source's call): the residual scale 1.4826 MAD of the gaps about their Savitzky-Golay fit",
        domain="the spacing of the single-puncture area spectrum converges to 4 pi gamma l_P^2 per half-step of j (dA/dj -> 8 pi gamma; Rovelli-Smolin 1995; Ashtekar-Lewandowski 1997; names and years only, not fetched, R10), and the area gap A(1/2) = 4 sqrt(3) pi gamma is the smallest eigenvalue; for the estimate: a symmetric quadratic Savitzky-Golay fit is exact to cubics, so its residual on a smooth sequence is -c4 g'''' + O(g^(6)), c4 = sum_k w_k k^4/24",
        numbers=(f"A(1/2) = {A_gap:.4f} l_P^2; gaps {gaps[0]:.4f} (j = 1/2 -> 1) down to {gaps[-1]:.5f} (j = 29.5 -> 30), smallest {step_min:.5f}, limit 4 pi gamma = {step_lim:.5f} (8 pi gamma = {slope_j:.4f} is dA/dj, the slope per unit j, which the source printed as the gaps' limit); "
                 f"ungated estimate (window 9): sigma = {sig:.3e} l_P^2 = {sig / step_min:.1e} of the smallest gap, {sig / A_gap:.1e} of the area gap; gated: min_sigma = smallest gap -> {_word(rejected['smallest gap'], 'record rejected', 'returned')}, min_sigma = A(1/2) -> {_word(rejected['area gap A(1/2)'], 'record rejected', 'returned')}; "
                 f"window sweep (order 2, MAD): " + ", ".join(f"{w}: {s:.2e}" for w, s in sweep) + f", log-log slope d ln sigma/d ln window = {slope_w:.2f} (a unit would not move; the leverage factor on white residuals moves it from {lev9:.4f} to {lev21:.4f} over windows 9 to 21, AGENT_LOG 30); "
                 f"truncation term at window 9: c4 = {c4:.4f}, scale of -c4 d^4 gap/di^4 over the interior indices {scale_pred:.3e} against the residual's scale there {scale_res:.3e} (relative difference {rel(scale_pred, scale_res):.3f})"),
        tg=f"A1' whole, the named step {crr:.5f} l_P^2, vs null, the ungated estimate {null:.3e}: {_word(tg_ok, 'agree', 'differ')}",
        tn=f"the spectrum's limit 4 pi gamma = {dom:.5f} (relative difference {rel(crr, dom):.1e}): the domain {_word(tn_ok, 'has', 'does not have')} Q",
        tc=f"rejected at both named steps, estimate below 1e-3 of the step, and the estimate moving with the window (slope > 2): {_word(check, 'holds', 'fails')}",
        out=out,
        reading=(f"the rejection clause does real work (T-G: with it the record has no estimated unit and the quantisation step is the unit; without it the estimator returns {sig:.2e} l_P^2), and what it hands back is the domain's constant: the synthesis reading is {out}, a definition read back, which is the source row's own DESCR content in the harness's terms. "
                 f"The ungated number is the fourth-derivative truncation term of the spectrum's closed form under the registered window ({scale_pred:.2e} predicted, {scale_res:.2e} measured on the interior, {rel(scale_pred, scale_res):.1%} apart), and it scales as window^{slope_w:.1f}: it measures the detrender, not the horizon. Recorded, not repaired: the source's '-> 8 pi gamma asymptotically' names the slope dA/dj; the last gaps it printed ({src_gap_20:.3f} at j = 20, {src_gap_30:.3f} at j = 30) converge to 4 pi gamma = {step_lim:.3f}"),
        weakness=("a single-puncture spectrum: the total area of N punctures has eigenvalues 8 pi gamma sum_i sqrt(j_i(j_i+1)) whose spacing falls with area (the quasi-continuous spectrum: Rovelli-Smolin 1995, Barreira-Carfora-Rovelli 1996, names and years only, not fetched), on which the smallest step and hence A1''s named unit is not this constant, and D1's rho = A/step is synthesis row 11's puncture count; "
                  "the rejection clause is CRR's, its trigger value (which step to name) is the domain's, and the harness's T-N cannot separate 'the domain has the constant' from 'the constant was named from the domain'; the truncation comparison is on the interior indices only (scipy's edge fit differs) and omits the sixth-derivative term"),
        elegance="A ruler cannot report a tick finer than the finest tick that exists: when the wobble you measure is far below the smallest step the world has, throw the wobble away and count steps. A rule with no knobs.",
        child="If a floor is made of tiles, the tile is the smallest step there is: you cannot stand halfway inside one. If your ruler says the floor wobbles by a thousandth of a tile, it is measuring its own scratches, not the floor, so you throw that away and count tiles instead.")


def main():
    return run_batch("Synthesis batch 26: rows 126-127 (prompt-log entry 61)", [r1(), r2()])


if __name__ == "__main__":
    sys.exit(main())
