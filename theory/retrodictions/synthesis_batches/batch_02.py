"""Synthesis batch 02: rows 6-10 of QUEUE.md (prompt-log entry 61). main [9] two-level (Schottky) thermodynamic length T = inf -> 0;
main [10] harmonic-trap stiffness protocol, minimum-dissipation (slow-driving) protocol; main [12] 2-D Ising (Onsager) Fisher metric at
the critical point; main [13] scalar random-walk Kalman filter (P4); main [14] Cramer-Rao unit and Fisher additivity I_N = N I_1.

Every model is re-implemented from theory/retrodictions/crr_retrodictions.py (nothing imported from there; it runs on import); no data
files (R2); deterministic (fixed seed, fixed grids, quad with named break points). Run:
uv run python theory/retrodictions/synthesis_batches/batch_02.py > theory/retrodictions/synthesis_batches/batch_02.txt
"""
import math
import sys

import numpy as np
from scipy import optimize
from scipy.integrate import quad, simpson
from scipy.special import ellipe, ellipk

from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

SRC = "theory/retrodictions/crr_retrodictions.txt"


def _agree(a, b, tol):
    return "agree" if rel(a, b) <= tol else "differ"


def _holds(b):
    return "holds" if b else "fails"


# ---------------------------------------------------------------- 6 (main [9]) two-level system: where A3 cuts the thermal carrier
def r1():
    eps = 1.0
    sq_var = lambda b: eps * math.exp(-abs(b * eps) / 2.0) / (1.0 + math.exp(-abs(b * eps)))   # sqrt(Var E) = eps / (2 cosh(beta eps / 2)), overflow-safe
    arc_from_ground = lambda b: quad(sq_var, b, np.inf)[0]                                   # D2 arc from T = 0+ (beta = +inf) down to beta
    C_half = arc_from_ground(0.0)                                                             # T = 0+ -> T = inf (the source row's number)
    C_full = quad(sq_var, -np.inf, np.inf)[0]                                                 # T = 0+ -> T = inf -> T = 0- (full population inversion)
    approach = [(b, arc_from_ground(b)) for b in (-5.0, -10.0, -20.0)]
    # the null for A3: a peak cut on the domain's own landmark, the Schottky heat-capacity maximum C_V = x^2 e^x / (1 + e^x)^2, x = beta eps
    x_pk = optimize.minimize_scalar(lambda x: -(x * x * math.exp(x) / (1.0 + math.exp(x)) ** 2), bounds=(0.1, 10.0), method="bounded",
                                    options=dict(xatol=1e-12)).x
    p_pk = 1.0 / (1.0 + math.exp(x_pk)); C_pk = arc_from_ground(x_pk / eps)
    bhatt = 2.0 * math.acos(math.sqrt(0.0 * 1.0) + math.sqrt(1.0 * 0.0))                       # Bhattacharyya angle between p = 0 and p = 1 (Bernoulli family)
    check = rel(C_half, C_full / 2.0) <= TOL_N                                                # T = inf is the midpoint of the occasion
    out = outcome(crr=C_full, null=C_pk, domain=bhatt, check=check)
    return make_row("thermo", "Two-level (Schottky) system on its canonical carrier p(beta) = 1/(1 + e^(beta eps)), Fisher metric = Var E, traversed once from T = 0+ through T = inf to T = 0- (population inversion)",
                    source=f"{SRC} [9] (CONSIST)",
                    Q="the A3 cut of a two-level system on the thermal carrier is the fully inverted state T = 0-: no protocol at positive temperature ever completes an occasion, the arc from the ground state to the cut is pi, and T = inf is the exact midpoint (the source row's pi/2)",
                    ingredient="A3 (cut at half a turn of arc, pi, from the last cut) with D5; D2 with A1 (Var E) supplies the arc",
                    null="a peak cut on the domain's own landmark: the Schottky heat-capacity maximum",
                    domain="the Bhattacharyya angle between the two pure populations p = 0 and p = 1 is 2 arccos 0 = pi (information geometry of the Bernoulli family)",
                    numbers=f"arc T = 0+ -> T = inf: {C_half:.6f} (pi/2 = {math.pi / 2:.6f}); arc T = 0+ -> T = 0-: {C_full:.6f} (pi = {math.pi:.6f}); approach to the cut at negative temperature: "
                            + ", ".join(f"beta eps = {b:g}: {c:.4f}" for b, c in approach)
                            + f" (the cut is reached only as beta -> -inf); Schottky peak at beta eps = {x_pk:.4f} (excited population {p_pk:.4f}), arc from the ground state to it {C_pk:.4f}",
                    tg=f"arc at the A3 cut {C_full:.4f} vs null arc at the Schottky-peak cut {C_pk:.4f}: {_agree(C_full, C_pk, TOL_G)}",
                    tn=f"Bhattacharyya angle {bhatt:.6f} vs the A3 arc {C_full:.6f}: {_agree(C_full, bhatt, TOL_N)}" + (" (the domain has Q)" if rel(C_full, bhatt) <= TOL_N else ""),
                    tc=f"T = inf at half the cut arc: {C_half:.6f} vs {C_full / 2.0:.6f}: {_holds(check)}",
                    out=out,
                    reading=f"A3 placed on the beta line says the two-level system's occasion is the whole line, ground state to inverted state, and that the cut is population inversion; the arc it names, {C_full:.4f}, is the length of the Bernoulli family between its two pure points, which information geometry already gives as the Bhattacharyya angle; the domain (negative temperatures) already reads beta as the natural line with T = inf interior. The source row's pi/2 is the half of this that positive temperatures can reach.",
                    weakness="the thermal family is not a rotor (O3): 'half a turn' here is the scalar condition C = pi, which CRR.md says coincides with A3 only on monotone traversals (the beta line traversed once is monotone in p); the cut is reached only as a limit, so no finite protocol cuts",
                    elegance="The whole temperature line, cold through infinitely hot to 'hotter than infinite' (population inversion), is a single arc of length pi (a quarter circle) in the system's own geometry, and infinitely hot sits exactly at its midpoint: a picture with no knobs.",
                    child="Think of a dimmer switch that goes from all-off to all-on. Heating a two-level system only ever gets you to half-on, and physicists call half-on 'infinitely hot'. To go past it you would have to flip more than half the atoms up, which they call a negative temperature. So 'infinitely hot' is not the end of the switch's travel; it is exactly the middle.")


# ---------------------------------------------------------------- 7 (main [10]) harmonic-trap stiffness protocol under the domain's friction tensor
def r2():
    k1, k2, tau, gamma, beta = 1.0, 4.0, 1.0, 1.0, 1.0
    g = lambda k: 1.0 / (2.0 * k ** 2)                           # Fisher metric of exp(-beta k x^2 / 2) in k (any beta)
    tau_r = lambda k: gamma / (2.0 * k)                           # integral relaxation time of x^2 for the overdamped trap
    zeta = lambda k: g(k) * tau_r(k) / beta                       # friction tensor (Sivak-Crooks): beta int_0^inf <dX(0) dX(t)> dt = g tau_r / beta
    zeta_num = quad(lambda t: beta * 0.5 * (math.exp(-k1 * t / gamma) / (beta * k1)) ** 2, 0.0, np.inf)[0]   # the same integral done directly at k = k1 (Wick: <dx^2(0) dx^2(t)> = 2 <x0 xt>^2)
    t = np.linspace(0.0, tau, 4001); s = t / tau; c = math.log(k2 / k1)
    W = lambda k, kdot: float(simpson(zeta(k) * kdot ** 2, x=t))  # W_ex = int zeta k-dot^2 dt (linear response, slow driving)
    W_lin = W(k1 + (k2 - k1) * s, np.full_like(s, (k2 - k1) / tau))
    W_F = W(k1 * np.exp(c * s), k1 * np.exp(c * s) * c / tau)                                   # the Fisher geodesic (exponential k), the source row's protocol
    W_F_closed = gamma * c / (4.0 * beta * k1) * (1.0 - math.exp(-c * tau))                   # closed form of the same integral
    u1, u2 = k1 ** -0.5, k2 ** -0.5; u = u1 + (u2 - u1) * s
    W_Z = W(u ** -2.0, -2.0 * u ** -3.0 * (u2 - u1) / tau)                                       # the friction-tensor geodesic (k^-1/2 linear in t)
    L_Z = quad(lambda k: math.sqrt(zeta(k)), k1, k2)[0]; W_min = L_Z ** 2 / tau                 # Cauchy-Schwarz: W >= L_zeta^2 / tau, equality at constant zeta-speed
    L_F = abs(c) * math.sqrt(0.5 / beta)                                                          # the source row's Fisher-Rao length

    def W_modes(a):                                               # endpoint-preserving family ln k = ln k1 + c s + sum a_j sin(j pi s)
        a = np.asarray(a, float); j = np.arange(1, len(a) + 1)
        lnk = math.log(k1) + c * s + (a[:, None] * np.sin(np.pi * j[:, None] * s[None, :])).sum(0)
        dlnk = (c + (a[:, None] * np.pi * j[:, None] * np.cos(np.pi * j[:, None] * s[None, :])).sum(0)) / tau
        k = np.exp(lnk); return W(k, k * dlnk)
    res = optimize.minimize(W_modes, np.zeros(8), method="BFGS", options=dict(gtol=1e-10))
    W_num = float(res.fun); a1 = float(res.x[0])
    gF = lambda k: 1.0 / (2.0 * k ** 2)                           # the source row's functional (Fisher metric used as the friction), for the tie-back
    src_lin = quad(lambda tt: gF(k1 + (k2 - k1) * tt) * (k2 - k1) ** 2, 0.0, tau)[0]
    src_geo = quad(lambda tt: gF(k1 * math.exp(c * tt)) * (c * k1 * math.exp(c * tt)) ** 2, 0.0, tau)[0]
    gap = (W_F - W_min) / W_min
    check = W_F <= W_min * (1.0 + TOL_N)                          # Q: the Fisher geodesic is the minimum-dissipation protocol
    leaves = (W_num < W_F) and (abs(a1) > 1e-3)                   # the optimiser started at the Fisher geodesic moved away from it
    out = outcome(crr=W_F, null=W_Z, domain=W_min, check=check)
    return make_row("thermo", "Overdamped particle in a harmonic trap, stiffness protocol k1 -> k2 in time tau (beta = gamma = 1), excess work in the slow-driving linear-response form W_ex = int zeta(k) k-dot^2 dt with the friction tensor zeta = beta int <dX(0) dX(t)> dt",
                    source=f"{SRC} [10] (CONSIST)",
                    Q="the minimum-dissipation stiffness protocol is the constant-speed geodesic of the Fisher-Rao metric fixed by A1/A1' with one global scale (S = 0 in that metric): k(t) exponential",
                    ingredient="A1' (the metric is Fisher-Rao with its scale fixed once, globally, by the system's unit) with D4/P1 (S = 0 selects the geodesic)",
                    null="the geodesic of the domain's own dissipation metric, the friction tensor zeta = g tau_r(k): Fisher-Rao with a LOCAL scale, the relaxation time (k^-1/2 linear in t)",
                    domain="Sivak-Crooks 2012 (the source row's citation): W_ex >= L_zeta^2 / tau by Cauchy-Schwarz, with equality on the constant-speed geodesic of zeta",
                    numbers=f"zeta(k) = g tau_r = 1/(4 k^3): direct integral of the x^2 autocorrelation at k = {k1:g} gives {zeta_num:.6f} vs 1/(4 k^3) = {zeta(k1):.6f}; "
                            f"excess work under the domain's functional: linear protocol {W_lin:.5f}, Fisher geodesic (exponential k) {W_F:.5f} (closed form {W_F_closed:.5f}), friction-tensor geodesic {W_Z:.5f}, bound L_zeta^2/tau = {W_min:.5f} (L_zeta = {L_Z:.5f}); "
                            f"numerical minimum over an 8-mode endpoint-preserving family started AT the Fisher geodesic: {W_num:.5f} (first mode coefficient {a1:+.4f}, {res.nit} BFGS iterations); "
                            f"the source row's functional (Fisher metric as the friction) reproduced: linear {src_lin:.5f}, exponential {src_geo:.5f} = L_F^2/tau with L_F = {L_F:.5f}",
                    tg=f"Fisher-geodesic dissipation {W_F:.5f} vs null (friction-tensor geodesic) {W_Z:.5f}: {_agree(W_F, W_Z, TOL_G)} (relative gap {gap:+.2%})",
                    tn=f"the domain's minimum L_zeta^2/tau = {W_min:.5f} vs the CRR value {W_F:.5f}: {_agree(W_F, W_min, TOL_N)}",
                    tc=f"Fisher geodesic within {TOL_N:.0%} of the minimum: {_holds(check)} (it dissipates {gap:+.2%} relative to the bound; the numerical optimiser started at it {'leaves it' if leaves else 'stays at it'}, {W_num:.5f})",
                    out=out,
                    reading=f"the domain's dissipation metric is the Fisher metric times a relaxation time that varies along the protocol (tau_r = gamma/2k); A1' fixes the Fisher scale once, so CRR's geodesic is the domain's optimum only where tau_r is constant, and for the stiffness protocol it is {'not the optimum' if not check else 'the optimum'} ({gap:+.2%})"
                            + ("; the source row's 'known' line (exponential k(t) is the optimal slow protocol) was the Fisher geodesic, not the domain's minimum-dissipation protocol, so its CONSIST was graded against a misstated known" if not check else ""),
                    weakness="one system, one protocol, linear response only (the exact finite-time optimum with its end jumps is outside the cited functional); a metric that is Fisher times a local factor is conformal to Fisher, so a v3.2 that let the unit vary along the path would recover the domain's rule, at the price of A1' as stated",
                    elegance="The domain's rule has no knobs: drive at constant speed in the metric that includes how long the system takes to follow, so you slow down where it is slow. CRR's rule is the same picture with the ground assumed the same everywhere.",
                    child="If you pull a wagon with a wobbly load, you go slowest on the bumpy bits where the load takes longest to settle, not at one speed all the way. 'One speed all the way' is only right when the ground is the same everywhere; here it is not.")


# ---------------------------------------------------------------- 8 (main [12]) 2-D Ising: the length across the critical point
def r3():
    hits = [0]

    def Cv(K):                                                    # Onsager's exact specific heat per spin (units of k_B)
        k1 = 2.0 * math.sinh(2.0 * K) / math.cosh(2.0 * K) ** 2; k1p = 2.0 * math.tanh(2.0 * K) ** 2 - 1.0
        m = k1 * k1
        if m >= 1.0 - 1e-15:                                      # a quadrature node within rounding of K_c: clip the modulus (counted)
            m = 1.0 - 1e-15; hits[0] += 1
        Kk, Ek = ellipk(m), ellipe(m)
        return (2.0 / math.pi) * (K / math.tanh(2.0 * K)) ** 2 * (2.0 * Kk - 2.0 * Ek - (1.0 - k1p) * (math.pi / 2.0 + k1p * Kk))
    Kc = 0.5 * math.log(1.0 + math.sqrt(2.0))
    vals = [(d, Cv(Kc * (1.0 - d))) for d in (1e-1, 1e-2, 1e-3, 1e-4)]                          # the source row's table
    mono = all(vals[i + 1][1] > vals[i][1] for i in range(3))
    sq_g = lambda K: math.sqrt(Cv(K)) / K                         # sqrt of the per-spin Fisher metric in K = beta J: g_KK = Var(E/J)/N = Cv / K^2
    L_win = quad(sq_g, 0.5 * Kc, 1.5 * Kc, points=[Kc], limit=400)[0]
    inner, hits_per = [], []
    for d in (1e-1, 1e-2, 1e-3, 1e-4):
        h0 = hits[0]
        inner.append((d, quad(sq_g, Kc * (1.0 - d), Kc * (1.0 + d), points=[Kc], limit=400)[0])); hits_per.append(hits[0] - h0)
    shrink = all(inner[i + 1][1] < inner[i][1] for i in range(3)) and inner[-1][1] < 1e-2 * L_win
    L_ig = L_win                                                  # information geometry computes the identical integral: no CRR-proper ingredient in Q
    check = math.isfinite(L_win) and shrink
    out = outcome(crr=L_win, null=L_ig, domain=L_win, check=check)
    tried = ("A3/D5: the thermal family is not a rotor and has no own events (O3), no cut can be placed; H-L5: no events, no occasions; "
             "A6: no occasions to regenerate from; H-T1/H-EQ: no learner; A1'/D1: the unit of an N-spin equilibrium family is the Cramer-Rao step 1/sqrt(N g), "
             "so rho over a window is sqrt(N) times the length below, i.e. the domain's own count of distinguishable temperatures")
    return make_row("ising", "2-D Ising model (Onsager), Fisher metric per spin g_KK = Cv/K^2 with Cv the exact specific heat, on the window K in [Kc/2, 3Kc/2] through the critical point",
                    source=f"{SRC} [12] (CONSIST)",
                    Q="the Fisher-Rao length of a path through the 2-D Ising critical point is finite although the metric diverges there: the logarithmic singularity of sqrt(g) is integrable, so the critical point is a place of unbounded resolution over vanishing extent",
                    ingredient="D2 (arc) with A1 (Fisher metric = energy variance) - NOT CRR-proper; no proper ingredient attaches (tried: " + tried + ")",
                    null="the same length computed by information geometry (identical by construction)",
                    domain="thermodynamic length (Ruppeiner / Crooks): the same integral int sqrt(Cv)/K dK, with Onsager's Cv ~ -ln|1 - K/Kc| integrable",
                    numbers="Cv at |1 - K/Kc| = " + ", ".join(f"{d:g}: {c:.3f}" for d, c in vals) + (" (grows without bound)" if mono else " (not monotone)")
                            + f"; length over [Kc/2, 3Kc/2] = {L_win:.6f} (Kc = {Kc:.6f}); contribution of |1 - K/Kc| < delta: "
                            + ", ".join(f"{d:g}: {c:.3e}" for d, c in inner) + f"; modulus clip reached {hits[0]} times in total, per window " + ", ".join(f"{d:g}: {h}" for (d, _), h in zip(inner, hits_per)),
                    tg=f"length {L_win:.6f} vs null (information geometry's same integral) {L_ig:.6f}: {_agree(L_win, L_ig, TOL_G)} (no CRR-proper ingredient in Q)",
                    tn=f"the domain's thermodynamic length is the same integral, {L_win:.6f}: {_agree(L_win, L_win, TOL_N)}",
                    tc=f"length finite and the inner contribution shrinking to below 1 % of it: {_holds(check)} (innermost {inner[-1][1]:.3e} vs {1e-2 * L_win:.3e})",
                    out=out,
                    reading="the source row's content is Onsager's specific heat read as a metric, and every quantity that can be formed from it (the divergence, its integrability, the finite length, the distinguishable-temperature count) is information geometry's or the domain's; CRR's proper ingredients need a rotor, own events, occasions or a learner, and an equilibrium family has none, which is the same silence as the thermal-time row of the first battery",
                    weakness="the integrable divergence is a property of the 2-D class (log); in a class with alpha > 0 the length across Tc is still finite (sqrt(g) ~ |t|^-alpha/2 with alpha < 2), so even the finiteness is not specific to Onsager",
                    elegance="", child="")


# ---------------------------------------------------------------- 9 (main [13]) the scalar Kalman filter as an equanimity rule: two readings of H-EQ
def _kalman_ss(v, r=1.0, n_iter=3000):
    """Steady-state gain and prior variance of the scalar random-walk filter by iterating the Riccati recursion (q = v^2 r)."""
    q, P = v * v * r, 1.0
    for _ in range(n_iter):
        Pm = P + q; K = Pm / (Pm + r); P = (1.0 - K) * Pm
    return K, Pm


def r4():
    r = 1.0
    K_P4 = lambda v: (v / 2.0) * (math.sqrt(v * v + 4.0) - v)      # P4's closed form
    v_star = optimize.brentq(lambda v: _kalman_ss(v)[0] - 0.5, 0.1, 5.0, xtol=1e-14)
    rows = []
    for v in (0.5, v_star, 1.0, 2.0, 4.0):
        K, Pm = _kalman_ss(v); I_past, I_obs = 1.0 / Pm, 1.0 / r
        K_A = I_obs / (I_past + I_obs)                            # reading A (the ledger's: w = 1, the two quadratic losses summed) = precision weighting
        K_B = I_obs / ((I_obs / I_past) * I_past + I_obs)         # reading B (the v3.1 text: equal pull in the Fisher norm, w I_past = I_obs)
        ratio = math.sqrt(I_past / I_obs)                         # the literal formula's norm ratio at the w-solution divided by w
        rows.append((v, K, K_P4(v), K_A, K_B, Pm, ratio))
    v1 = [x for x in rows if x[0] == 1.0][0]; K1, KP1, KA1, KB1, Pm1, ratio1 = v1[1:]
    out_A = outcome(crr=KA1, null=K1, domain=KP1, check=rel(KA1, KP1) <= TOL_N)
    out_B = outcome(crr=KB1, null=K1, domain=KP1, check=rel(KB1, KP1) <= TOL_N)
    internal = rel(KA1, KB1) > TOL_G
    out = outcome(internal=internal)
    return make_row("filter", "Scalar random-walk Kalman filter at steady state (r = 1, q = v^2), the update read as a learner with a present batch (the observation, precision I_obs = 1/r) and a settled past (the prior, precision I_past = 1/P-)",
                    source=f"{SRC} [13] (CONSIST)",
                    Q="the steady-state Kalman gain is the equanimity weight: the update that balances settled past and present at Omega = 1 has gain K(v) of P4",
                    ingredient="H-EQ (Omega = 1) in its two readings in CRR.md: (A) the ledger's 'w = 1, sum the two batch means' and (B) the text's 'equal pull in the Fisher norm'",
                    null="ER-sum: the two quadratic losses summed with w = 1 (which is Bayes' precision weighting)",
                    domain="P4 / the steady-state Riccati equation: K(v) = (v/2)(sqrt(v^2 + 4) - v); CRR.md says the formula is not CRR's",
                    numbers="; ".join(f"v = {v:.4f}: Riccati K = {K:.6f}, P4 {KP:.6f}, reading A {KA:.6f}, reading B {KB:.6f} (P- = {Pm:.4f}, sqrt(I_past/I_obs) = {rt:.4f})" for v, K, KP, KA, KB, Pm, rt in rows)
                            + f"; the two readings cross at v* = {v_star:.6f} (1/sqrt 2 = {1 / math.sqrt(2):.6f}), where I_past = I_obs",
                    tg=f"reading A {KA1:.6f} vs null (ER-sum) {K1:.6f}: {_agree(KA1, K1, TOL_G)}; reading B {KB1:.6f} vs null {K1:.6f}: {_agree(KB1, K1, TOL_G)} (v = 1)",
                    tn=f"P4 gives {KP1:.6f}: reading A {_agree(KA1, KP1, TOL_N).replace('agree', 'agrees').replace('differ', 'differs')}, reading B {_agree(KB1, KP1, TOL_N).replace('agree', 'agrees').replace('differ', 'differs')}",
                    tc=f"not reached: readings A and B {_agree(KA1, KB1, TOL_G)} at v = 1 ({KA1:.4f} vs {KB1:.4f}); on its own, reading A would read {out_A} and reading B {out_B}",
                    out=out,
                    reading=f"on the one domain where the optimal balance of past and present is a theorem, H-EQ is not one rule: summing the losses (A) is Bayes' precision weighting and reduces to its own null, as the ledger found on learners; equal pull in the Fisher norm (B) fixes the gain at {KB1:.1f} for every v and is right only at v* = {v_star:.4f}, where the two precisions happen to be equal; the literal formula w = ||g_present||_F / ||g_past||_F has no fixed point here (its norm ratio at the w-solution is w sqrt(I_past/I_obs) = w x {ratio1:.4f} at v = 1, so the self-consistent w is 0 or infinite unless v = v*)",
                    weakness="the filter has one parameter and Gaussian losses, so 'gradient' and 'precision' are the same object; a learner's smoothed gradients need not be, which is where the ledger's EQ2 rows live",
                    elegance="", child="")


# ---------------------------------------------------------------- 10 (main [14]) the A1' unit against Fisher additivity
def r5():
    rng = np.random.default_rng(0); M = 400000; theta0, s_sys, s1 = 10.0, 1.0, 4.0
    res = []
    for N in (1, 4, 16, 64, 256, 1024):
        theta = rng.normal(theta0, s_sys, M)                                     # the system's own value on occasion m
        stat = theta + rng.normal(0.0, s1 / math.sqrt(N), M)                      # the within-occasion mean of N draws, from its exact sampling law N(theta_m, s1^2/N)
        sig = 1.4826 * float(np.median(np.abs(stat - np.median(stat))))          # A1' scale rule across occasions (no detrender: no trend by construction)
        res.append((N, sig, s1 / math.sqrt(N), math.sqrt(s_sys ** 2 + s1 ** 2 / N)))
    N_d, sig_d, crb_d, ltv_d = [x for x in res if x[0] == 256][0]
    sig_top = res[-1][1]
    check = rel(sig_top, s_sys) <= 0.05
    out = outcome(crr=sig_d, null=crb_d, domain=ltv_d, check=check)
    return make_row("estim", f"An occasion statistic measured as the mean of N iid draws (noise s1 = {s1:g}) on a system whose own value varies from occasion to occasion (s_sys = {s_sys:g}), {M} occasions per N, seed 0",
                    source=f"{SRC} [14] (DESCR)",
                    Q="the resolvable step of a recurring system, estimated across its own occasions (A1'), does not shorten as N^-1/2 with the number of draws per occasion: it saturates at the system's own between-occasion scatter, and Fisher additivity I_N = N I_1 governs only the instrument's part",
                    ingredient="A1' (the unit is the system's own resolvable step, the robust scale of one occasion statistic across occasions; 'the recording instrument's sample-level noise is not the unit') with D1",
                    null="the Cramer-Rao unit 1/sqrt(N I_1) = s1/sqrt(N) (the source row: N observations shorten the unit by sqrt N)",
                    domain="the law of total variance (one-way random-effects model): Var(stat) = s_sys^2 + s1^2/N",
                    numbers="; ".join(f"N = {N}: A1' unit {sig:.4f}, Cramer-Rao unit {crb:.4f}, total-variance unit {ltv:.4f}" for N, sig, crb, ltv in res),
                    tg=f"N = {N_d}: A1' unit {sig_d:.4f} vs null (Cramer-Rao) {crb_d:.4f}: {_agree(sig_d, crb_d, TOL_G)}",
                    tn=f"law of total variance gives {ltv_d:.4f}: {_agree(sig_d, ltv_d, TOL_N)}" + (" (the domain has Q)" if rel(sig_d, ltv_d) <= TOL_N else ""),
                    tc=f"saturation: A1' unit at N = {res[-1][0]} is {sig_top:.4f} vs the system's own scatter {s_sys:.4f} (within 5 %): {_holds(check)}",
                    out=out,
                    reading="A1''s refusal to take the instrument's noise as the unit is, in the domain's terms, the between-occasion variance component of a random-effects model, and Fisher additivity is the within component; the domain has both in one identity, and CRR's contribution is the modelling choice ([M]) of which component to call the unit, not a theorem",
                    weakness="the within-occasion mean is drawn from its exact Gaussian sampling law rather than from N draws, so Fisher additivity is used, not tested, and the row tests only the saturation; the instrument's unit_sigma adds a detrender whose leverage is not modelled here",
                    elegance="One rule with no knobs: the smallest step that counts is how much the system itself differs from one occasion to the next, not how finely the dial can be read.",
                    child="If a plant grows a different amount each day, buying a finer ruler does not make the days more alike. The smallest step worth talking about is how much the days differ from each other, and measuring more carefully only helps until you reach that.")


def main():
    return run_batch("Synthesis batch 02: rows 6-10 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
