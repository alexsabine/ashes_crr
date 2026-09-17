"""CRR on excitatory-inhibitory (E-I) networks: does any clause reach a known E-I result?
(owner request 2026-09-17, prompt-log entry 40; literature record in docs/citations/ei_networks_2026-09-17.md)

Twelve rows (eleven model systems and, on request, the removed C*Omega = 1 rupture rule run on two of them): Wilson-Cowan rate networks (inhibition-stabilised regime and the
paradoxical effect; Hopf onset of gamma and what sets its frequency; noisy PING cycles),
a balanced LIF network (van Vreeswijk-Sompolinsky), the two readings of "equanimity" on a
Gaussian update (equal precision vs Fisher speed 1) set against Tucker-Luu-Friston's
"balanced precision" framing, theta-gamma n:m locking (Tucker & Luu's Resonant Oscillatory
Coherence), branching-process avalanches at balance (Poil et al.), the stabilised supralinear
network (Ahmadian-Rubin-Miller), homeostatic scaling, a cortical travelling wave, and
population Fisher information under differential correlations. Grades under the issue-#21
rules; BORROWED and FLOW per row; H-L5 class where the system has its own events.

Model systems only; no dataset opened (R2). Deterministic (seeded). Run:
uv run python theory/retrodictions/ei_networks.py
"""
import math
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve

from crr.instrument.core import antipodal_cuts, arc_length, intrinsic_phase, occasions, poisson_transform, regularity, unit_sigma

ROWS = []


def row(cls, system, clause, borrowed, flow, derivation, known, verdict, grade, l5=None, weakness=""):
    ROWS.append(dict(cls=cls, system=system, clause=clause, borrowed=borrowed, flow=flow, derivation=derivation,
                     known=known, verdict=verdict, grade=grade, l5=l5, weakness=weakness))


def cv(x): x = np.asarray(x, float); return float(x.std(ddof=1) / abs(x.mean()))


_CACHE = {}


def l5_class(x, events, dt=1.0, segment_end="inclusive"):
    r = regularity(np.asarray(x, float), np.asarray(events, int), sigma=1.0, dt=dt, n_boot=200, seed=0, segment_end=segment_end)
    if abs(r["cv_arc"] - r["cv_clock"]) < 1e-3: lab = "tie"
    else: lab = "arc-regular" if r["cv_arc"] < r["cv_clock"] else "clock-regular"
    return lab, r["cv_arc"], r["cv_clock"]


# ================================================================ Wilson-Cowan rate networks
def _wc_fixed_point(W, h, f=lambda x: np.maximum(x, 0.0)):
    def g(r): return -r + f(W @ r + h)
    return fsolve(g, np.array([0.5, 0.5]))


def wc_isn_paradox():
    W_isn = np.array([[1.5, -1.0], [1.2, -0.5]]); W_non = np.array([[0.5, -1.0], [1.2, -0.5]])
    h = np.array([1.0, 0.5]); dh = np.array([0.0, 0.1])
    out = {}
    for name, W in (("ISN", W_isn), ("non-ISN", W_non)):
        r0 = _wc_fixed_point(W, h); r1 = _wc_fixed_point(W, h + dh)
        J = W - np.eye(2); stable = bool(np.all(np.linalg.eigvals(J).real < 0))
        out[name] = (r0, r1, stable, W[0, 0] > 1)
    (rI0, rI1, sI, eI), (rN0, rN1, sN, eN) = out["ISN"], out["non-ISN"]
    row("wc", "Wilson-Cowan E-I network: inhibition-stabilised regime and the paradoxical effect", "A4 (the (E, I) state is Markov: depth one); no clause reaches the regime",
        "threshold-linear Wilson-Cowan rate equations; ISN theory (Tsodyks 1997; Ozeki 2009)", "the recurrent weights and inputs (system-supplied)",
        f"ISN (w_EE = 1.5 > 1, stable: {sI}): extra drive to I moves I from {rI0[1]:.4f} to {rI1[1]:.4f} (paradoxical decrease) and E from {rI0[0]:.4f} to {rI1[0]:.4f}; non-ISN (w_EE = 0.5): I from {rN0[1]:.4f} to {rN1[1]:.4f} (increase)",
        "surround suppression is a withdrawal of excitation in an ISN (Ozeki 2009)", "no CRR clause concerns the sign of a steady-state response; the network is depth one, so the salience law is silent by A4",
        "OPEN", None, "the paradoxical effect is linear-algebra of the weight matrix; CRR adds nothing")


def _wc72(E, I, P, wEE):
    """Wilson & Cowan 1972 oscillatory parameter set (c_EI 12, c_IE 15, c_II 3, a_E 1.3, th_E 4, a_I 2, th_I 3.7, r = 1); w_EE and P registered."""
    def S(x, a, th): return 1 / (1 + math.exp(-a * (x - th))) - 1 / (1 + math.exp(a * th))
    return -E + (1 - E) * S(wEE * E - 12.0 * I + P, 1.3, 4.0), -I + (1 - I) * S(15.0 * E - 3.0 * I, 2.0, 3.7)


def wc_hopf_gamma():
    def rhs(t, y, wEE, tauI):
        dE, dI = _wc72(y[0], y[1], 1.25, wEE); return [dE, dI / tauI]
    def amp_freq(wEE, tauI):
        t = np.linspace(0, 400, 40001); sol = solve_ivp(rhs, (0, 400), [0.1, 0.05], t_eval=t, args=(wEE, tauI), method="RK45", rtol=1e-8, atol=1e-10)
        E = sol.y[0][20000:]; amp = float(E.max() - E.min())
        if amp < 1e-3: return amp, float("nan")
        cuts = antipodal_cuts(intrinsic_phase(E)); return amp, (len(cuts) - 1) / 2 / (t[-1] - t[20000])
    ws = (14.0, 15.0, 16.0, 18.0, 20.0); res = [amp_freq(w, 1.0) for w in ws]
    osc = [(w, a) for w, (a, f) in zip(ws, res) if a >= 1e-3]
    slope, icpt = np.polyfit([w for w, a in osc], [a * a for w, a in osc], 1); w_c = -icpt / slope
    taus = (1.0, 1.5, 2.0); f_tau = [amp_freq(16.0, tau)[1] for tau in taus]
    row("wc", "Wilson-Cowan E-I oscillator (1972 parameter set): onset of the E-I rhythm and what sets its frequency", "issue-#21 text criticality clause (rho ~ amplitude at a Hopf point); v3.1 O3 (nothing sets L)",
        "Hopf normal form (amplitude^2 linear in the control parameter past onset); Wilson-Cowan 1972; Brunel 2000 (frequency set by synaptic/membrane time scales)", "the recurrent gain w_EE, the drive P = 1.25 and the inhibitory time constant",
        "amplitude and frequency at w_EE = " + ", ".join(f"{w:g}: ({a:.3f}, {f:.4f})" for w, (a, f) in zip(ws, res)) + f"; amplitude^2 on the oscillating points fits w_EE linearly with onset w_c = {w_c:.2f} (Hopf scaling); at w_EE = 16 the frequency at tau_I = " + ", ".join(f"{tau:g}: {f:.4f}" for tau, f in zip(taus, f_tau)) + f" (ratio f(1)/f(2) = {f_tau[0] / f_tau[2]:.2f}, not the 2.00 of a pure 1/tau_I law)",
        "gamma emerges by a Hopf-type instability; its frequency is set by the inhibitory time scale (Brunel 2000: 'almost fully controlled by the synaptic time scale')", "the amplitude scaling at onset is the Hopf normal form's; the frequency is set by tau_I and the recurrent gains together; no CRR clause reaches the onset value w_c or the period",
        "OPEN", None, "CRR names the cycle as an occasion and is silent on its period and on where oscillation begins")


def wc_noisy_ping_cycles():
    def run(noise, seed=2, dt=0.01, n=120000):
        rng = np.random.default_rng(seed); E, I = 0.1, 0.05; Es = np.empty(n)
        for k in range(n):
            dE, dI = _wc72(E, I, 1.25, 16.0); xi = rng.standard_normal(2)
            E += dt * dE + noise * math.sqrt(dt) * xi[0]; I += dt * dI + noise * math.sqrt(dt) * xi[1]; Es[k] = E
        Es = Es[20000:]; cuts = antipodal_cuts(intrinsic_phase(Es))[2:-2]
        lab, ca, cc = l5_class(Es, cuts, dt); return len(cuts) - 1, lab, ca, cc, Es, cuts
    levels = (0.0, 0.003, 0.01, 0.03); out = [run(z) for z in levels]
    labs = sorted(set(o[1] for o in out[1:]))
    Es = out[2][4]; _CACHE["wc_noisy"] = (Es, out[2][5], 0.01)
    # metric sensitivity at the 0.01 level: E is a fraction active, so its Fisher carrier is Bernoulli (2 arcsin sqrt E);
    # read as a rate it is Poisson (2 sqrt E). The identity metric is what the row above used.
    carriers = (("identity", Es), ("Bernoulli-Fisher", 2 * np.arcsin(np.sqrt(np.clip(Es, 0, 1)))), ("Poisson-Fisher", poisson_transform(np.clip(Es, 0, None))))
    metric = []
    for name, y in carriers:
        cy = antipodal_cuts(intrinsic_phase(y))[2:-2]; lab_y, ca_y, cc_y = l5_class(y, cy, 0.01); metric.append((name, lab_y, ca_y, cc_y))
    row("wc", "Noisy Wilson-Cowan rhythm: are its half-cycles arc-regular or clock-regular?", "A3 (antipodal cut on the intrinsic phase), D5, H-L5, A1 (Fisher metric of the carrier)",
        "analytic-signal phase; the same Wilson-Cowan oscillator with additive white noise (registered levels); Bernoulli and Poisson Fisher carriers", "the noise level and the recurrent dynamics",
        "; ".join(f"noise {z:g}: {m} half-cycles, CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}" for z, (m, lab, ca, cc, _, _) in zip(levels, out)) + f"; classes over the three noisy levels: {labs}; at noise 0.01 under three carriers: "
        + ", ".join(f"{name} {lab_y} ({ca_y:.3f} vs {cc_y:.3f})" for name, lab_y, ca_y, cc_y in metric),
        "cortical gamma is a noisy oscillation with variable amplitude and frequency (bursts)", ("the instrument assigns arc-regular at every noisy level and under all three carriers; no clause predicts the class" if len(labs) == 1 and len(set(m[1] for m in metric)) == 1 else "the class changes with the noise level or the carrier; no clause predicts which class a noisy rhythm belongs to"),
        "OPEN", None, f"at noise 0 the CVs are not 0: the half-turn cut alternates on an asymmetric waveform (the A3 gate's S-C/S-E finding), so a share of every CV here is the instrument's; the margins |CV_arc - CV_clock| are {', '.join(f'{abs(ca - cc):.3f}' for _, _, ca, cc, _, _ in out)} (two below 0.01); class assignment on a model, not a result")


# ================================================================ balanced spiking network
def balanced_lif():
    rng = np.random.default_rng(4); NE, NI, K = 320, 80, 40; N = NE + NI
    J = 1.0 / math.sqrt(K); dt = 1e-4; T = 3.0; steps = int(T / dt); tau = 0.02; Vth, Vr = 1.0, 0.0
    mE, mI, gE, gI = 2.0, 1.6, 2.0, 1.8                                      # external drive (units of sqrt(K) J) and inhibitory weight ratios
    W = np.zeros((N, N))
    for i in range(N):
        pre_e = rng.choice(NE, K, replace=False); pre_i = NE + rng.choice(NI, K, replace=False)
        W[i, pre_e] = J; W[i, pre_i] = -J * (gE if i < NE else gI)
    h = np.where(np.arange(N) < NE, mE, mI) * math.sqrt(K) * J
    Wp = np.maximum(W, 0.0); Wn = np.minimum(W, 0.0)
    V = rng.random(N) * 0.5; spikes = [[] for _ in range(N)]; exc_in = np.zeros(N); inh_in = np.zeros(N); ext_in = np.zeros(N)
    n_tr = 5; traces = np.empty((steps, n_tr))
    for s in range(steps):
        fired = V >= Vth
        for i in np.where(fired)[0]: spikes[i].append(s)
        V[fired] = Vr
        f = fired.astype(float); e_part = Wp @ f; i_part = Wn @ f                # instantaneous synaptic kicks (units of threshold)
        if s > steps // 3: exc_in += e_part; inh_in += i_part; ext_in += h * dt / tau
        V += dt * (h - V) / tau + e_part + i_part
        traces[s] = V[:n_tr]
    isi = [np.diff(sp[5:]) * dt for sp in spikes[:NE] if len(sp) > 12]
    cvs = [cv(x) for x in isi if len(x) > 8]; med_cv = float(np.median(cvs))
    rate_e = np.mean([len(sp) for sp in spikes[:NE]]) / T; rate_i = np.mean([len(sp) for sp in spikes[NE:]]) / T
    E_tot = float((exc_in[:NE] + ext_in[:NE]).mean()); I_tot = float(inh_in[:NE].mean()); bal = abs(E_tot + I_tot) / E_tot
    reg = "irregular" if med_cv > 0.5 else "regular"
    # H-L5 on five E cells, membrane potential as the carrier (identity metric: a voltage has no Fisher carrier), spikes as own events.
    # traces[b-1] is the threshold sample and traces[b] the post-reset sample at spike b: "inclusive" counts the 1-sigma reset
    # jump inside every ISI's arc, "exclusive" is the rise only (the jump is the cut, A3).
    per = []
    for i in range(n_tr):
        ev = np.array(spikes[i][3:40])
        if len(ev) < 8: continue
        li, cai, cci = l5_class(traces[:, i], ev, dt); lx, cax, ccx = l5_class(traces[:, i], ev, dt, segment_end="exclusive")
        rises = [arc_length(traces[a:b, i], 1.0) for a, b in zip(ev[:-1], ev[1:])]
        per.append((i, li, cai, cci, lx, cax, ccx, float(np.median(rises))))
    _CACHE["lif"] = (traces[:, 0], np.array(spikes[0]), dt)
    n_arc_inc = sum(p[1] == "arc-regular" for p in per); n_arc_exc = sum(p[4] == "arc-regular" for p in per)
    lab = "arc-regular" if n_arc_exc > len(per) / 2 else ("clock-regular" if n_arc_exc < len(per) / 2 else "split")
    cax_mean = float(np.mean([p[5] for p in per])); ccx_mean = float(np.mean([p[6] for p in per]))
    row("spk", "Balanced E-I network of leaky integrate-and-fire neurons (sparse, strong synapses J = 1/sqrt K)", "D5 (spikes as own events), H-L5, A3 (the reset is the cut, not arc), A9 read as 'E and I balance' (a rename, see the next row)",
        "van Vreeswijk & Sompolinsky 1996 balance; Brunel 2000 asynchronous irregular state", "external drive, connectivity, synaptic strengths",
        f"N = {N}, K = {K}: mean rates E {rate_e:.1f} Hz, I {rate_i:.1f} Hz; ISI CV across {len(cvs)} E cells: median {med_cv:.2f} ({reg}); |net input|/total excitatory input = {bal:.3f} against the O(1/sqrt K) = {1 / math.sqrt(K):.3f} scale (cancellation); "
        f"H-L5 on {len(per)} E cells, reset jump counted (inclusive) -> rise only (exclusive): " + "; ".join(f"cell {i}: {li[:5]} ({cai:.3f} vs {cci:.3f}) -> {lx[:5]} ({cax:.3f} vs {ccx:.3f}), median rise arc {mr:.1f} sigma" for i, li, cai, cci, lx, cax, ccx, mr in per)
        + f"; arc-regular on {n_arc_inc}/{len(per)} cells with the jump counted, {n_arc_exc}/{len(per)} without it",
        "irregular firing (CV ~ 1) from cancellation of large E and I inputs; linear network response", f"{lab} on the rise alone: in the fluctuation-driven regime the arc per ISI is ten or more times the fixed chord, so the chord's regularity is not inherited; the earlier 'arc-regular' reading was the reset jump, a constant added to every arc (corrected 2026-09-17, AGENT_LOG 18); the balance itself is a sqrt-K scaling result that no CRR clause states",
        "DESCR", (lab, cax_mean, ccx_mean), "the E-I balance is not CRR's equanimity: it is a cancellation of two currents, not a weighting of past against present")


def equanimity_readings():
    prec_prior, prec_like = 1.0, 1.0
    K_equal = prec_like / (prec_prior + prec_like)                          # equal precision: posterior gain 1/2
    K_fisher = 0.5 * (math.sqrt(5) - 1)                                     # random walk at Fisher speed 1: 1/phi
    ratios = (0.1, 1.0, 10.0); infl = {r: (1 + r) ** 2 / (4 * r) for r in ratios}
    row("bayes", "Two readings of 'equanimity' on one Gaussian update; Tucker-Luu-Friston's 'balanced feedforward (excitatory) and feedback (inhibitory) precision'", "issue-#21 text A9 (equal precision) vs P4 at v = 1 (Fisher speed); the abstract of Tucker, Luu & Friston 2025 (Entropy 27:829)",
        "Bayesian fusion; scalar Kalman steady state", "none (a single update)",
        f"equal prior and likelihood precision gives gain {K_equal:.4f}; the random-walk filter at Fisher speed v = 1 gives gain {K_fisher:.4f}: the two readings called equanimity disagree on the same update. Equal-precision weighting is Bayes-optimal only at precision ratio 1: MSE inflation at ratios " + ", ".join(f"{r:g}: {infl[r]:.3f}x" for r in ratios),
        "optimal belief updating weights prior and likelihood by their precisions (inverse variances); the abstract states updating 'rests on balanced ... prior and likelihood precision'", "'balanced precision' is Bayes-optimal exactly when the precisions are equal and otherwise a bias; CRR's own two equanimity readings give different gains, so CRR cannot even state which balance it would predict",
        "TENSION", None, "the Tucker-Luu-Friston claim is the free-energy framing's, not CRR's; CRR inherits its limitation and adds an internal disagreement (retrodiction battery row 16)")


# ================================================================ oscillatory coupling (Tucker & Luu 2026)
def theta_gamma_locking():
    def run(w_th, w_ga, eps, n=5, m=1, T=200.0, dt=1e-3):
        # gamma phase pulled toward n:m = 5:1 with theta: d(gamma)/dt = w_ga + eps sin(n theta - m gamma); locks when |w_ga - n w_th| < eps
        th, ga = 0.0, 0.3; th_cross = []; ga_cross = []; steps = int(T / dt)
        for s in range(steps):
            th_new = th + dt * w_th; ga_new = ga + dt * (w_ga + eps * math.sin(n * th - m * ga))
            if math.floor(th_new / (2 * math.pi)) > math.floor(th / (2 * math.pi)): th_cross.append(s)
            if math.floor(ga_new / (2 * math.pi)) > math.floor(ga / (2 * math.pi)): ga_cross.append(s)
            th, ga = th_new, ga_new
        th_cross = np.array(th_cross); ga_cross = np.array(ga_cross)
        counts = [int(((ga_cross > a) & (ga_cross <= b)).sum()) for a, b in zip(th_cross[5:-1], th_cross[6:])]
        return counts
    w_th, w_ga, eps = 2 * math.pi * 6, 2 * math.pi * 31, 25.0
    locked = run(w_th, w_ga, eps); unlocked = run(w_th, w_ga, 0.0)
    cond = abs(w_ga - 5 * w_th) < eps
    row("osc", "Theta-gamma n:m phase-phase coupling (Tucker & Luu 2026: Resonant Oscillatory Coherence)", "A1' (unit = one gamma cycle), D5 (occasion = one theta cycle), natural time",
        "coupled phase oscillators; Arnold-tongue locking", "the intrinsic frequencies (6 Hz, 31 Hz) and the coupling",
        f"5:1 locking condition |w_gamma - 5 w_theta| = {abs(w_ga - 5 * w_th):.2f} rad/s < eps = {eps:g}: {cond}; with coupling, gamma cycles per theta cycle = {sorted(set(locked))} (CV {cv(locked):.3f}); without coupling (31/6 not an integer): {sorted(set(unlocked))} (CV {cv(unlocked):.3f})",
        "n:m locking fixes an integer number of gamma cycles per theta cycle; the abstract says a ROC 'persists long enough' for NMDA facilitation, with no duration given", "under locking the natural-time count of gamma per theta occasion is constant by definition of locking; a persistence threshold in gamma cycles and one in clock time are then the same statement, so CRR's clock adds nothing here",
        "DESCR", None, "the abstract's mechanism (ROC -> early LTP) is not quantified; the framework cannot be tested against it without a stated duration or ratio")


def avalanches_branching():
    rng = np.random.default_rng(9)
    def sizes(sig, n=20000, cap=100000):
        out = []
        for _ in range(n):
            a = 1; s = 1
            while a > 0 and s < cap:
                a = rng.poisson(sig * a); s += a
            out.append(s)
        return np.array(out)
    def slope(s):
        edges = np.unique(np.floor(np.logspace(0, 3, 16)).astype(int)); h, _ = np.histogram(s, bins=edges)
        x = np.log((edges[:-1] + edges[1:]) / 2); y = np.log(np.maximum(h / np.diff(edges), 1e-9)); m = h > 5
        return float(np.polyfit(x[m], y[m], 1)[0])
    s1, s08 = sizes(1.0), sizes(0.8)
    fisher_sigma = {s: 1 / s for s in (0.8, 1.0, 1.2)}                       # Poisson offspring: I(sigma) per unit ancestor = 1/sigma
    row("crit", "Neuronal avalanches at E-I balance as a critical branching process (Poil et al. 2012; Tucker-Luu-Friston 'criticality')", "issue-#21 text criticality clause; A1' (unit = one spike); no clause on exponents",
        "Galton-Watson branching process; power-law avalanche sizes at sigma = 1", "the branching ratio (set by E-I balance)",
        f"size-distribution log-log slope at sigma = 1: {slope(s1):.2f} (mean-field -1.5); at sigma = 0.8: {slope(s08):.2f} (exponential cutoff); Fisher information about sigma per ancestor = 1/sigma: " + ", ".join(f"{s:g}: {v:.3f}" for s, v in fisher_sigma.items()) + " (finite and smooth through sigma = 1)",
        "critical branching gives P(s) ~ s^(-3/2); balance tunes the branching ratio to 1", "the exponent is the branching process's; the Fisher metric of the control parameter does not diverge at the critical point (a third counterexample to the universal divergence claim)",
        "FAILS", None, "rule 4 / class dependence: 'criticality = Fisher divergence' is false on the standard model of neuronal avalanches; CRR reaches neither the exponent nor the balance condition")


def ssn_supralinear():
    k, n = 0.04, 2.0; W = np.array([[1.25, -0.65], [1.2, -0.5]])
    def resp(c):
        def g(r): return -r + k * np.maximum(W @ r + np.array([c, c]), 0) ** n
        return fsolve(g, np.array([1.0, 1.0]) * max(c, 1e-3) ** 1.5)
    ratios = {c: resp(2 * c)[0] / resp(c)[0] for c in (0.5, 2.0, 8.0, 32.0)}
    row("wc", "Stabilised supralinear network: supralinear-to-sublinear summation with contrast", "no clause",
        "Ahmadian, Rubin & Miller 2013; Hennequin et al. 2018", "the power-law gain and the recurrent weights",
        "E response ratio r(2c)/r(c) at c = " + ", ".join(f"{c:g}: {v:.2f}" for c, v in ratios.items()) + " (above 2 = supralinear, below 2 = sublinear)",
        "weak inputs sum supralinearly, strong inputs sublinearly (normalisation)", "no CRR clause reaches a steady-state input-output curve",
        "OPEN", None, "")


def homeostatic_scaling():
    r_target, tau_h = 5.0, 50.0; g = 0.3; rs = []
    for _ in range(4000):
        r = 20.0 * g; g += (r_target - r) / tau_h * 0.01; rs.append(r)
    row("plast", "Homeostatic synaptic scaling restoring a target rate after an E/I perturbation", "A4 (depth one), O1 (retention not claimed)",
        "synaptic scaling as first-order relaxation to a set point", "the scaling time constant and target",
        f"rate relaxes from {rs[0]:.2f} to {rs[-1]:.3f} Hz (target {r_target}); the relaxation is Markov in (g): no multi-occasion effect",
        "homeostatic plasticity maintains E/I balance (Poil et al. attribute balance to it)", "depth one: the framework predicts nothing beyond the state",
        "DESCR", None, "")


def travelling_wave():
    N = 60; om = 2 * math.pi * 6.0; kappa = 40.0; dt = 1e-3; steps = 4000; rng = np.random.default_rng(11)
    th = 2 * math.pi * np.arange(N) / N + 0.05 * rng.standard_normal(N)            # one winding round the ring (a twisted state) plus noise
    for s in range(steps):
        th = th + dt * (om + kappa * (np.sin(np.roll(th, -1) - th) + np.sin(np.roll(th, 1) - th)))
    grad = np.angle(np.exp(1j * np.diff(th))); phase_grad = float(grad.mean()); spread = float(grad.std())
    speed = om / phase_grad
    row("wave", "Cortical travelling wave (ring of coupled phase oscillators, twisted state): deep-layer 'excitatory travelling waves' (Tucker & Luu 2026)", "A3 (cut per half-turn at each site), D5",
        "Kuramoto ring; twisted state; wave speed = frequency x wavelength", "the intrinsic frequency, the winding number and the coupling",
        f"steady phase gradient {phase_grad:.4f} rad/site (2 pi/N = {2 * math.pi / N:.4f}; spread {spread:.1e}); wave speed omega/gradient = {speed:.1f} sites/s = f x N; each site cuts every half-turn by definition",
        "travelling waves propagate at speeds set by conduction, coupling and wavelength", "the antipodal cut is a definition on a phase rotor; the speed is the winding number's and the frequency's, and the coupling only stabilises the twist: no clause reaches it",
        "DESCR", None, "")


def population_fisher_differential():
    N_list = (10, 100, 1000, 10000); fprime = 1.0; sig2, eps = 1.0, 0.05
    I = {N: N * fprime ** 2 / sig2 / (1 + eps * N * fprime ** 2 / sig2) for N in N_list}   # Sigma = sig2 I + eps f'f'^T (Sherman-Morrison)
    row("code", "Population Fisher information with differential correlations (limit on the A1' unit of a neural population)", "A1' (unit = 1/sqrt(I) for the population)",
        "Moreno-Bote et al. 2014 (differential correlations saturate information)", "the tuning curves and the correlation structure",
        "I_pop at N = " + ", ".join(f"{N}: {v:.1f}" for N, v in I.items()) + f" -> saturates at 1/eps = {1 / eps:g}: the population's resolvable step floors at sqrt(eps)",
        "information-limiting correlations bound the population code", "A1' inherits the bound; whether E-I circuitry produces such correlations is not a CRR question",
        "DESCR", None, "")


# ================================================================ the older 'one Omega before rupture' rule (C*Omega = 1), on request (prompt-log entry 41)
def _arc_threshold_cuts(x, sigma, thresh):
    """The removed rule: cut when the arc since the last cut reaches thresh = 1/Omega sigma-units (a sigma-step counter)."""
    x = np.asarray(x, float); acc = 0.0; cuts = [0]
    for k in range(1, len(x)):
        acc += abs(x[k] - x[k - 1]) / sigma
        if acc >= thresh: cuts.append(k); acc = 0.0
    return np.array(cuts)


def omega_rupture_rule():
    Es, cuts, dt = _CACHE["wc_noisy"]; trace, sp, dtl = _CACHE["lif"]
    ext = np.array([Es[a:b + 1].max() - Es[a:b + 1].min() for a, b in zip(cuts[:-1], cuts[1:])])
    sig = unit_sigma(ext[: len(ext) // 2]); rho_wc = float(np.median(ext) / sig)                      # A1' unit from the training half; D1 resolution
    oc = occasions(Es, cuts, sig); C, Cs, Sv = oc.T
    per_half = [len(_arc_threshold_cuts(Es, sig, 1.0 / Om)) / len(cuts) for Om in (0.5, 1.0, 2.0)]
    ev = sp[3:40]; rises = np.array([arc_length(trace[a:b], 1.0) for a, b in zip(ev[:-1], ev[1:])]); chords = np.array([abs(trace[b - 1] - trace[a]) for a, b in zip(ev[:-1], ev[1:])])
    frac = []
    for a, b in zip(ev[:-1], ev[1:]):
        cum = np.cumsum(np.abs(np.diff(trace[a:b]))); frac.append((int(np.argmax(cum >= 1.0)) + 1) / (b - a) if cum[-1] >= 1.0 else 1.0)
    per_spike = [len(_arc_threshold_cuts(trace, 1.0, 1.0 / Om)) / len(sp) for Om in (0.5, 1.0, 2.0)]
    row("cut", "The removed 'one Omega before rupture' rule, C*Omega = 1, on the noisy Wilson-Cowan rhythm and the balanced LIF neuron", "issue-#21 text rupture clause C*Omega = 1 (v3.1 A3 note: a scalar reduction, 'not the axiom'; spec XI.1: removed); A1' (unit), D1 (rho measured, never predicted), D2-D4",
        "arc-length accumulation; the unit sigma of A1'", "the same dynamics as rows 3 and 4",
        f"noisy WC (noise 0.01): unit sigma = {sig:.4f} from the training half of the half-turn extents, rho = {rho_wc:.2f}; per antipodal half-turn C median {np.median(C):.2f} sigma, C* median {np.median(Cs):.2f}, S median {np.median(Sv):.2f} (S < 0 on {int((Sv < 0).sum())} occasions); "
        f"the rule cuts {per_half[0]:.2f}, {per_half[1]:.2f}, {per_half[2]:.2f} times per half-turn at Omega = 0.5, 1, 2 (it coincides with A3 iff rho = 1/Omega). LIF neuron 0 (sigma = threshold - reset = 1): rise arc median {np.median(rises):.2f} sigma against chord median {np.median(chords):.3f}; "
        f"the C = 1 cut fires at a median {np.median(frac):.2f} of the ISI and before the spike on {100 * np.mean(np.array(frac) < 1.0):.0f}% of ISIs; the rule cuts {per_spike[0]:.1f}, {per_spike[1]:.1f}, {per_spike[2]:.1f} times per spike at Omega = 0.5, 1, 2",
        "a neuron fires when its potential reaches threshold (C* = threshold - reset in the voltage carrier), not when its path length reaches a fixed value; a rhythm completes a cycle when its phase does",
        "the rule is a sigma-step counter: it fires every 1/Omega units of arc, so it agrees with the system's own event only where rho = 1/Omega (WC) or the rise is monotone so that C = C* (LIF, noise-free); on both E-I models it fires many times per event; the neuron's event is a chord condition (C* = 1), which is the opposite reading of 'one unit before rupture'",
        "FAILS", None, "rule 4 / class dependence: the clause is a clause of the older text only; v3.1 holds A3 and D1 (rho is measured), and the spec removed the rule for this reason; the row records what it would have predicted here so that the question 'was it used' has a number")


BATTERY = [wc_isn_paradox, wc_hopf_gamma, wc_noisy_ping_cycles, balanced_lif, equanimity_readings, theta_gamma_locking,
           avalanches_branching, ssn_supralinear, homeostatic_scaling, travelling_wave, population_fisher_differential, omega_rupture_rule]


def main():
    for f in BATTERY: f()
    print(f"CRR on E-I networks — {len(ROWS)} rows. Grades: SHARP CONSIST DESCR FAILS TENSION OPEN. Literature record: docs/citations/ei_networks_2026-09-17.md\n")
    for i, r in enumerate(ROWS, 1):
        print(f"[{i:2d}] ({r['cls']}) {r['system']}\n     clause:     {r['clause']}\n     BORROWED:   {r['borrowed']}\n     FLOW:       {r['flow']}"
              f"\n     derivation: {r['derivation']}\n     known:      {r['known']}\n     verdict:    {r['verdict']}\n     GRADE:      {r['grade']}"
              + (f"\n     H-L5 class: {r['l5'][0]} (CV_arc {r['l5'][1]:.3f}, CV_clock {r['l5'][2]:.3f})" if r['l5'] else "")
              + (f"\n     weakness:   {r['weakness']}" if r['weakness'] else ""))
    grades = ("SHARP", "CONSIST", "DESCR", "FAILS", "TENSION", "OPEN")
    print("\n" + "=" * 100 + "\nTALLY  " + "  ".join(f"{g}={sum(r['grade'] == g for r in ROWS)}" for g in grades))
    print(f"Does CRR add anything to what is known about E-I networks? Clauses that reach a known E-I result: 0 of {len(ROWS)} rows"
          " (every DESCR row is the domain's own result or a definition; the FAILS rows are clauses of the older text; the TENSION row is internal; the OPEN rows name no clause).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
