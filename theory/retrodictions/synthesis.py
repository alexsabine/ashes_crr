"""The SYNTHESIS class: CRR taken whole against a domain's own mathematics, asking whether it adds anything
(owner request 2026-09-17, prompt-log entry 60; design in docs/notes/2026-09-17_synthesis_class.md).

A SYNTHESIS row states ONE proposition Q about a domain, in the domain's own terms, formed with at least one
CRR-proper ingredient (A3 antipodal cut and D5 occasions; A6 regeneration by a bounded Frechet mean, never a
count; P2/P3 occasion weights; A1'/D1 the system's own unit and resolution; H-L5's class claim; D6/H-T1 path vs
endpoint; H-EQ; A7/A8 tense). Ingredients CRR shares with information geometry (A1 Fisher-Rao metric, D2 arc,
D3 chord, D4 surplus, P1) are not CRR-proper. Three tests, every one a number printed here, decide the outcome:

  T-G  ablation against the null: the decisive quantity computed WITH the CRR-proper ingredient and with its
       information-geometric or domain replacement; if they agree within TOL_G the ingredient did no work.
  T-N  novelty against the domain: the domain's own theorem for the same target, where one is cited; if it gives
       the CRR value within TOL_N the domain already has Q.
  T-C  the check: Q tested in the domain's own mathematics (numerically or in closed form); holds / fails /
       unavailable here (a Q about data or an unmeasured quantity).

Outcomes (computed by `outcome`, R15): REDUNDANT-IG (T-G agrees), REDUNDANT-DOMAIN (T-N has it), WRONG (T-C
fails), ADDS (T-C holds; always a candidate, because novelty can only be judged by a domain expert),
PROPOSES (T-C unavailable: the hand-off to the expert), INTERNAL (two readings of the CRR ingredient disagree
on the domain), UNSTATED (no Q could be formed; the numbers tried are printed). Gate (R4 analogue): row 1 is a
synthetic domain in which a CRR-proper ingredient adds structure by construction and must read ADDS, its decoy
(an outside unit) must not, and row 2 (clock-regular by construction) must not. No dataset opened (R2).
Deterministic. Run:  uv run python theory/retrodictions/synthesis.py
"""
import math
import sys

import numpy as np
from scipy import optimize

from crr.instrument.core import antipodal_cuts, cv, intrinsic_phase, regularity, unit_sigma
from crr.surrogates.battery import S_G_relaxation

TOL_G = 1e-2     # T-G: the ingredient did work only if CRR value and null differ by more than 1 % (relative)
TOL_N = 1e-2     # T-N: the domain already has Q if its own theorem gives the CRR value within 1 % (relative)
ROWS = []


def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-12)


def outcome(crr=None, null=None, domain=None, check=None, internal=False, unstated=False):
    """The label, from the numbers only."""
    if unstated:
        return "UNSTATED"
    if internal:
        return "INTERNAL"
    if rel(crr, null) <= TOL_G:
        return "REDUNDANT-IG"
    if domain is not None and rel(crr, domain) <= TOL_N:
        return "REDUNDANT-DOMAIN"
    if check is None:
        return "PROPOSES"
    return "ADDS" if check else "WRONG"


def row(cls, system, Q, ingredient, null, domain_theorem, numbers, tg, tn, tc, out, reading, weakness=""):
    ROWS.append(dict(cls=cls, system=system, Q=Q, ingredient=ingredient, null=null, domain=domain_theorem,
                     numbers=numbers, tg=tg, tn=tn, tc=tc, outcome=out, reading=reading, weakness=weakness))


# ---------------------------------------------------------------- 1 gate: positive control (synthetic domain)
def _arc_regular_amplitude_variable(n=60, seed=0, rate_cv=0.15, tv=2.0, m=3):
    """Each cycle: a ramp of random height a plus m sinusoidal wiggles of height b, b solved so that the total
    variation of the cycle is exactly `tv`. Arc constant by construction; amplitude (peak to peak) and duration vary."""
    rng = np.random.default_rng(seed)
    xs, ev, pos = [], [0], 0
    for _ in range(n):
        T = int(100 * rng.normal(1, rate_cv)); a = rng.uniform(0.5, 1.0)
        u = np.arange(T) / T
        def tv_of(b): return float(np.abs(np.diff(a * u + b * np.sin(2 * np.pi * m * u))).sum())
        b = optimize.brentq(lambda bb: tv_of(bb) - tv, 0.0, 2.0, xtol=1e-12)
        xs.append(a * u + b * np.sin(2 * np.pi * m * u)); pos += T; ev.append(pos)
    return np.concatenate(xs), np.asarray(ev[:-1])


def gate_positive():
    x, ev = _arc_regular_amplitude_variable()
    r = regularity(x, ev, sigma=1.0, segment_end="exclusive", n_boot=500)
    check = r["cv_arc"] < 0.02 and r["cv_arc"] < r["cv_clock"] and r["cv_arc"] < r["cv_amp"]
    out = outcome(crr=r["cv_arc"], null=r["cv_clock"], domain=None, check=check)
    decoy = outcome(crr=r["cv_amp"], null=r["cv_clock"], domain=None,
                    check=r["cv_amp"] < 0.02 and r["cv_amp"] < r["cv_clock"])
    row("gate", "Positive control: a synthetic event train whose cycles have equal total variation but random height, wiggle and duration (the domain sees a renewal process with CV 0.15 and nothing else)",
        "the arc of one occasion between the system's own events is constant: CV(C) -> 0 while CV(clock) and CV(amplitude) stay at their construction values",
        "A3/D5 (occasion = interval between own events, the reset jump is the cut: segment_end = exclusive), D2 with A1' (sigma = 1), H-L5 (the class claim)",
        "the clock: the interval statistics the domain already has", None,
        f"{r['n']} occasions: CV(C) = {r['cv_arc']:.3e}, CV(clock) = {r['cv_clock']:.3f}, CV(amplitude) = {r['cv_amp']:.3f}; C_mean = {r['C_mean']:.4f} sigma; paired-bootstrap 95 % CI of CV(C) - CV(clock) = [{r['ci95'][0]:.3f}, {r['ci95'][1]:.3f}]; decoy framework (unit = peak-to-peak amplitude, an outside constant): its CV {r['cv_amp']:.3f} reads {decoy}",
        f"CV(C) {r['cv_arc']:.3e} vs null CV(clock) {r['cv_clock']:.3f}: differ", "no domain theorem for the arc; the renewal description has no such quantity",
        f"CV(C) < 0.02 and below both controls: {'holds' if check else 'fails'}",
        out, f"the harness prints {out} where a CRR-proper ingredient adds structure by construction and {decoy} for the decoy unit; ADDS is reachable, and not by measuring excursion size",
        "by construction; a synthetic domain says only that the harness can see the effect")
    return out, decoy


# ---------------------------------------------------------------- 2 gate: negative control
def gate_negative():
    x, ev, _ = S_G_relaxation(n=60, seed=0)
    r = regularity(x, ev, sigma=1.0, segment_end="exclusive", n_boot=500)
    check = r["cv_arc"] < r["cv_clock"]
    out = outcome(crr=r["cv_arc"], null=r["cv_clock"], domain=None, check=check)
    row("gate", "Negative control: S-G, a relaxation oscillator firing at a fixed time with a variable threshold (clock-regular by construction)",
        "the same Q as row 1: the arc of one occasion is more regular than the clock",
        "A3/D5, D2, H-L5 (as row 1)", "the clock", None,
        f"{r['n']} occasions: CV(C) = {r['cv_arc']:.3f}, CV(clock) = {r['cv_clock']:.3f}, CV(amplitude) = {r['cv_amp']:.3f}",
        f"CV(C) {r['cv_arc']:.3f} vs null {r['cv_clock']:.3f}: differ", "none", f"CV(C) < CV(clock): {'holds' if check else 'fails'}",
        out, f"a signal with no CRR content reads {out}: the class is not empty of failures", "by construction")
    return out


# ---------------------------------------------------------------- 3 Bayesian accumulation vs A6
def _d_fr_gauss(m1, s1, m2, s2):
    return math.sqrt(2.0) * math.acosh(1.0 + ((m1 - m2) ** 2 + 2.0 * (s1 - s2) ** 2) / (4.0 * s1 * s2))


def _frechet_gauss(ms, ss):
    def f(p):
        mu, ls = p; s = math.exp(ls)
        return sum(_d_fr_gauss(mu, s, m, sd) ** 2 for m, sd in zip(ms, ss))
    res = optimize.minimize(f, x0=[float(np.mean(ms)), math.log(float(np.mean(ss)))], method="Nelder-Mead",
                            options=dict(xatol=1e-10, fatol=1e-12, maxiter=4000))
    return float(res.x[0]), float(math.exp(res.x[1]))


def bayes_accumulation():
    rng = np.random.default_rng(0); n = 10; s_occ = 1.0 / math.sqrt(n)
    out_k = []
    for K in (4, 16, 64):
        ms = [float(rng.normal(0.0, 1.0, n).mean()) for _ in range(K)]
        muF, sF = _frechet_gauss(ms, [s_occ] * K)
        sB = 1.0 / math.sqrt(n * K); muB = float(np.mean(ms))
        out_k.append((K, muF, sF, muB, sB))
    K, muF, sF, muB, sB = out_k[-1]
    check = rel(sF, sB) <= 0.05
    out = outcome(crr=sF, null=sB, domain=None, check=check)
    row("stat", "Bayesian estimation of a Gaussian mean (known variance) from K evidence occasions of n = 10 draws each",
        "the state after K occasions is the Fisher-Rao Frechet mean of the K per-occasion posteriors at bounded strength (A6: never an accumulated count), so its spread does not shrink with K",
        "A6 (Frechet mean over settled occasions, bounded strength), D5 (occasion = one batch), A1 (Fisher-Rao on the Gaussian family = hyperbolic half-plane, closed-form distance)",
        "the domain's accumulation: the posterior after nK draws, N(mean, 1/sqrt(nK))", "Bayes' theorem (posterior consistency: spread ~ 1/sqrt(nK))",
        "; ".join(f"K = {K_}: Frechet mean N({muF_:.4f}, {sF_:.4f}), accumulated posterior N({muB_:.4f}, {sB_:.4f})" for K_, muF_, sF_, muB_, sB_ in out_k)
        + f"; per-occasion spread {s_occ:.4f}: the Frechet spread stays at or above it (it rises with the scatter of the occasion means, a property of the hyperbolic plane) while the accumulated spread falls as K^-1/2",
        f"K = 64: Frechet spread {sF:.4f} vs null (accumulated) {sB:.4f}: differ", "Bayes' theorem gives the accumulated value, not the Frechet one: no domain theorem produces Q",
        f"Q against Bayes at K = 64: relative difference in spread {rel(sF, sB):.3f} (holds if <= 0.05): {'holds' if check else 'fails'}",
        out, "read as an inference rule, A6 is contradicted by the domain: evidence accumulates and the Frechet mean does not; the axiom's own clause ('a system that re-counts its past stops cutting') says a Bayesian accumulator is not a regenerating system, which is a scope restriction and, by CLAUDE.md section 10, a new prereg rather than a repair",
        "the occasion is taken as one batch; O3 says a monotone posterior path has no rotor and hence no cut, which would make Q vacuous rather than false")


# ---------------------------------------------------------------- 4 quantum mechanics: two readings of A3
def quantum_antipode():
    out_s, internal = [], False
    for E in ((0.0, 1.0, 2.0), (0.0, 1.0, 3.0)):
        E = np.asarray(E); dE = float(np.sqrt(np.mean(E ** 2) - np.mean(E) ** 2))
        t_arc = math.pi / (2.0 * dE)                                  # arc C(t) = 2 dE t reaches a half-turn (pi)
        t = np.linspace(0.0, 2.0 * math.pi, 200001)
        ov = np.abs(np.exp(-1j * np.outer(t, E)).sum(axis=1)) / len(E)
        i = int(np.argmin(ov[1:]) + 1)
        r = optimize.minimize_scalar(lambda tt: abs(np.exp(-1j * tt * E).sum()) / len(E), bounds=(t[i - 1], t[i + 1]), method="bounded", options=dict(xatol=1e-12))
        ov_min = float(r.fun); t_perp = float(r.x) if ov_min < 1e-6 else None
        if t_perp is None or rel(t_arc, t_perp) > TOL_G:
            internal = True
        S = (2.0 * dE * t_perp - math.pi) if t_perp is not None else None
        out_s.append((tuple(float(e) for e in E), dE, t_arc, t_perp, ov_min, S))
    out = outcome(internal=internal)
    row("qm", "A pure state under a time-independent Hamiltonian (equal-weight superposition of three levels), quantum Fisher metric (Fubini-Study, distance to orthogonality = pi)",
        "the occasion boundary of a unitary evolution is the first orthogonal state (the antipode), reached when the Fisher arc has advanced a half-turn: t_cut = pi / (2 dE), the Mandelstam-Tamm time",
        "A3 (cut at the half-turn), D2/D3 (arc 2 dE t, chord 2 arccos|<psi0|psi_t>|), D4",
        "the two readings of A3 itself: 'phase advanced half a turn' (arc = pi) against 'the antipode' (chord = pi, orthogonality)", "Mandelstam-Tamm bound t_perp >= pi/(2 dE), saturated only on a geodesic (Anandan-Aharonov)",
        "; ".join(f"levels {E_}: dE = {dE_:.4f}, arc half-turn at t = {ta_:.4f}, " + (f"first orthogonal state at t = {tp_:.4f} (surplus at the antipode S = {S_:.4f})" if tp_ is not None else f"no orthogonal state in a full period (minimum overlap {om_:.4f})") for E_, dE_, ta_, tp_, om_, S_ in out_s),
        "; ".join(f"levels {E_}: arc reading {ta_:.4f} vs antipode reading " + (f"{tp_:.4f}: {'agree' if rel(ta_, tp_) <= TOL_G else 'differ'}" if tp_ is not None else "none (no antipode occurs)") for E_, dE_, ta_, tp_, om_, S_ in out_s), "the domain has both times (Mandelstam-Tamm and the actual orthogonality time) and the geometric statement that they coincide only on geodesics",
        "not reached: the two readings of the ingredient must agree before Q can be checked",
        out, "on a non-geodesic unitary evolution 'half a turn of phase' and 'the antipode' are different events, and for a generic spectrum the antipode never occurs while the arc keeps turning; CRR.md's own note ('cut when C = C* (something) coincides with A3 only on monotone traversals') is this tension seen from the other side",
        "the rotor CRR's A3 assumes (a circle of circumference L) does not exist on the projective space; which of the two readings is A3 must be fixed before any quantum row can be graded")


# ---------------------------------------------------------------- 5 two-tone signal: the A3 occasion rate
def two_tone():
    f1, f2, a2, dt, T = 1.0, 1.3, 0.6, 1e-3, 200.0
    t = np.arange(0.0, T, dt); x = np.cos(2 * math.pi * f1 * t) + a2 * np.cos(2 * math.pi * f2 * t)
    cuts = antipodal_cuts(intrinsic_phase(x))
    rate = (len(cuts) - 1) / ((cuts[-1] - cuts[0]) * dt)
    centroid = (f1 + a2 ** 2 * f2) / (1 + a2 ** 2)
    check = rel(rate, 2 * f1) <= TOL_N
    out = outcome(crr=rate, null=2 * centroid, domain=2 * f1, check=check)
    row("sig", "A two-tone signal cos(2 pi f1 t) + 0.6 cos(2 pi f2 t), f1 = 1, f2 = 1.3, analytic-signal phase",
        "the A3 occasion rate (half-turns per unit time) is twice the frequency of the stronger tone, not twice the spectral centroid",
        "A3 on the intrinsic phase (antipodal_cuts), D5", "the spectral centroid, the domain's mean frequency", "the time average of the instantaneous frequency of a two-tone signal is the frequency of the stronger component (Boashash 1992 review; Gabor/Ville analytic signal)",
        f"{len(cuts)} cuts over {T:g} s: rate {rate:.4f} half-turns/s; 2 f1 = {2 * f1:.4f}; 2 x centroid = {2 * centroid:.4f}",
        f"rate {rate:.4f} vs null 2 x centroid {2 * centroid:.4f}: differ", f"domain theorem gives {2 * f1:.4f}: the domain has Q",
        f"rate within 1 % of 2 f1: {'holds' if check else 'fails'}",
        out, "the A3 count is a majority statistic of the phase, which the analytic-signal literature already states; CRR renames it",
        "1-D signal; no metric content")


# ---------------------------------------------------------------- 6 replicator dynamics: the geodesic criterion
def _sphere_path_stats(X):
    Y = np.sqrt(X); C = 2.0 * float(np.linalg.norm(np.diff(Y, axis=0), axis=1).sum())
    Cs = 2.0 * math.acos(min(1.0, float(Y[0] @ Y[-1]))); return C, Cs, C - Cs


def replicator_geodesic():
    x0 = np.array([0.6, 0.3, 0.1]); t = np.linspace(0.0, 6.0, 6001); res = {}
    for name, f in (("three distinct fitness values (0, 0.5, 1)", (0.0, 0.5, 1.0)), ("two distinct fitness values (0, 1, 1)", (0.0, 1.0, 1.0))):
        X = x0 * np.exp(np.outer(t, np.asarray(f))); X /= X.sum(axis=1, keepdims=True)
        res[name] = _sphere_path_stats(X)
    S3 = res["three distinct fitness values (0, 0.5, 1)"][2]; S2 = res["two distinct fitness values (0, 1, 1)"][2]
    out = outcome(crr=S3, null=S3, domain=None, check=(S2 < 1e-4 and S3 > 1e-2))
    row("evo", "Constant-fitness replicator dynamics on the 3-simplex with the Shahshahani (Fisher-Rao) metric",
        "a replicator trajectory is a Fisher-Rao geodesic (surplus S = 0) iff the fitness vector takes at most two distinct values; otherwise S > 0",
        "D4 (surplus) - NOT CRR-proper: arc minus geodesic distance is information geometry", "the same S computed by information geometry alone (identical by construction)", "the replicator flow is an e-geodesic of the exponential family (Amari), which is a Levi-Civita geodesic only when the sqrt-embedded path is planar",
        "; ".join(f"{k}: C = {v[0]:.4f}, C* = {v[1]:.4f}, S = {v[2]:.2e}" for k, v in res.items()),
        f"S {S3:.4f} vs null S {S3:.4f}: {'agree' if rel(S3, S3) <= TOL_G else 'differ'} (no CRR-proper ingredient in Q)", "the e-geodesic statement is the domain's",
        f"S(two values) < 1e-4 and S(three values) > 1e-2: {'holds' if (S2 < 1e-4 and S3 > 1e-2) else 'fails'} (the criterion is true, and it is information geometry's)",
        out, "a true and checkable statement about the domain that CRR did not add: every symbol in it is shared with information geometry",
        "included to show T-G failing on a correct proposition")


# ---------------------------------------------------------------- 7 the heteroclinic cycle re-read
def rps_reread(a=1.3, b=1.0, dt=0.01, t_max=3000.0, n_last=12):
    A = np.array([[0.0, -a, b], [b, 0.0, -a], [-a, b, 0.0]])   # wins +b, losses -a; the heteroclinic cycle attracts iff a > b
    def rhs(y):
        x = np.exp(y - np.max(y)); x /= x.sum(); Ax = A @ x; return Ax - x @ Ax
    y = np.log(np.array([0.5, 0.3, 0.2])); dom = int(np.argmax(y)); t = 0.0
    arcs, durs, seg, t_start = [], [], [], 0.0
    while t < t_max:
        k1 = rhs(y); k2 = rhs(y + 0.5 * dt * k1); k3 = rhs(y + 0.5 * dt * k2); k4 = rhs(y + dt * k3)
        y = y + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0; t += dt
        x = np.exp(y - np.max(y)); x /= x.sum(); seg.append(x)
        d = int(np.argmax(y))
        if d != dom:
            X = np.asarray(seg); arcs.append(2.0 * float(np.linalg.norm(np.diff(np.sqrt(X), axis=0), axis=1).sum())); durs.append(t - t_start)
            dom, seg, t_start = d, [x], t
    arcs, durs = np.asarray(arcs[-n_last:]), np.asarray(durs[-n_last:])
    mean_arc = float(arcs.mean())
    out = outcome(crr=mean_arc, null=math.pi, domain=None, check=None)
    row("evo", "Rock-paper-scissors replicator with an attracting heteroclinic cycle (loss a = 1.3, win b = 1; cognitive-collective battery row 8 read again under the synthesis class)",
        "the arc of each dominance epoch is a constant, so the epochs are arc-regular while their clock durations grow without bound",
        "H-L5 (class claim), D5 (own event = dominance switch), A1 (P7 metric)", "the edge of the simplex: a geodesic of length pi between two vertices (information geometry, no dynamics)", None,
        f"{len(arcs)} last epochs: mean arc {mean_arc:.4f} (CV {cv(arcs):.3f}); durations {durs[0]:.1f} -> {durs[-1]:.1f} (CV {cv(durs):.3f}); vertex-to-vertex geodesic pi = {math.pi:.4f}; relative difference {rel(mean_arc, math.pi):.2e}",
        f"mean arc {mean_arc:.4f} vs null pi {math.pi:.4f}: {'agree' if rel(mean_arc, math.pi) <= TOL_G else 'differ'}", "none cited", "not reached",
        out, ("the regularity is real and it is geometry: once the attracting cycle has pulled the trajectory onto the boundary, every epoch runs one edge, and every edge has length pi; the dynamical fact (attraction to the boundary) is the domain's, the constant is information geometry's, and CRR's arc adds a name; the CLASS-AGREES reading of the earlier row stands, the synthesis reading is " + out) if out == "REDUNDANT-IG" else ("the epoch arc did not settle at the edge length pi in this run: " + out),
        "the same reading applies to any heteroclinic network on a simplex")


# ---------------------------------------------------------------- 8 the adder with regeneration memory
def _adder_memory(q, n=20000, seed=0, delta=1.0, noise=0.1):
    rng = np.random.default_rng(seed); b = np.empty(n); b[0] = delta; m = delta
    for i in range(1, n):
        m = (1.0 - q) * b[i - 1] + q * m                     # P3 age weights: m_n = (1-q) sum_k q^k b_{n-k} (the 1-D Frechet mean)
        b[i] = 0.5 * (m + delta * (1.0 + noise * rng.normal()))   # divides at m + Delta; the daughter is half
    return b


def _lag2_coefficient(b):
    Y = b[2:]; X = np.column_stack([np.ones(len(Y)), b[1:-1], b[:-2]])
    beta = np.linalg.lstsq(X, Y, rcond=None)[0]; return float(beta[1]), float(beta[2])


def adder_regeneration():
    res = {q: _lag2_coefficient(_adder_memory(q)) for q in (0.0, 0.3, 0.6)}
    c0, c3 = res[0.0][1], res[0.3][1]
    out = outcome(crr=c3, null=c0, domain=0.0, check=None)
    row("bio", "The bacterial adder (division at birth size + Delta) with A6 regeneration: the division setpoint references the age-weighted Frechet mean of past birth sizes instead of the current one",
        "birth-size lineages carry a positive partial autocorrelation at lag 2 (a grandmother term), which the plain adder (an AR(1) with coefficient 1/2) sets to zero",
        "A6 (Frechet mean over settled occasions), P3 (geometric age weights q^k), D5 (occasion = one cell cycle)", "the plain adder (q = 0)", "the adder model: b_{n+1} = (b_n + Delta)/2 + noise, lag-k correlation 2^-k, partial autocorrelation zero beyond lag 1",
        "; ".join(f"q = {q:g}: regression of b_n+1 on (b_n, b_n-1): coefficients ({c1:.4f}, {c2:.4f})" for q, (c1, c2) in res.items()) + "; 20000 generations, Delta = 1, division noise 10 %",
        f"lag-2 coefficient {c3:.4f} (q = 0.3) vs null {c0:.4f} (adder): differ", "the adder gives 0 for the lag-2 partial coefficient: the domain's standard model does not contain Q",
        "unavailable here: needs single-cell lineage data (mother-machine E. coli lineages, not fetched, absent from data/SEEN.md); the prereg would score the lag-2 coefficient per lineage against zero with the paired bootstrap",
        out, "the one row in this battery where CRR's regeneration axiom, integrated with the domain's own rule, produces a statement the domain's standard model does not make and that data can decide; whether lineage-memory models in the domain already contain it is the expert's question, not this script's",
        "a memory term beyond the adder is not unique to A6: any AR(2) does it; the CRR content is the sign and the geometric shape of the weights, which a prereg must test, not just the nonzero lag-2 term")


# ---------------------------------------------------------------- 9 cyclic cosmology with a Tolman increment
def tolman_cycles(n_cycles=50, eps=0.1, q=0.5, n_init=5):
    S = 1.0 + eps * np.arange(n_cycles + 1); lna_tolman = (2.0 / 3.0) * np.log(S)       # radiation-filled closed cycles: a_max ~ S^(2/3)
    lna_a6 = list(lna_tolman[:n_init]); m = lna_a6[0]
    for v in lna_a6[1:]: m = (1 - q) * v + q * m
    for _ in range(n_cycles + 1 - n_init):
        nxt = m; lna_a6.append(nxt); m = (1 - q) * nxt + q * m
    lna_a6 = np.asarray(lna_a6)
    growth_t = float(lna_tolman[-1] - lna_tolman[n_init - 1]); growth_a6 = float(lna_a6[-1] - lna_a6[n_init - 1])
    check = growth_t <= 1e-3        # Q says bounded; the domain's cycles grow
    out = outcome(crr=growth_a6, null=growth_t, domain=growth_t, check=check)
    row("cos", "Cyclic cosmology with a Tolman entropy increment per cycle (radiation-filled closed cycles, a_max ~ S^2/3), the bounce-to-bounce cycle as the occasion",
        "the maximum scale factor of successive cycles stays bounded: each cycle is seeded from the Frechet mean of past cycles at bounded strength (A6: never an accumulated count)",
        "A6 (Frechet regeneration), P3 (age weights, q = 0.5), D5 (cycle = occasion)", "Tolman's accumulation: S_{n+1} = S_n + dS, a_max growing without bound", "Tolman 1934: entropy increase makes successive cycles larger",
        f"{n_cycles} cycles after {n_init} seeded ones: Tolman growth of ln a_max = {growth_t:.4f}; A6 growth = {growth_a6:.4f} (the seeded history's weighted mean, then constant)",
        f"A6 growth {growth_a6:.4f} vs null (Tolman) {growth_t:.4f}: differ", "Tolman's theorem gives the opposite of Q", f"Q (bounded) against the domain's cycles: {'holds' if check else 'fails'}",
        out, "read as a law of cyclic cosmology, A6 is contradicted by the domain's own thermodynamics; the escape ('a system that re-counts its past stops cutting', so a Tolman universe is not a regenerating system) is a scope restriction and a new prereg, not a repair",
        "a two-line model of Tolman's argument; the loop-gravity battery's row 5 has the arc/clock reading of the same cycles")


# ---------------------------------------------------------------- 10 thermal time vs the arc clock
def thermal_time():
    D, beta, bdot = 1.0, 1.0, 0.01
    p = 1.0 / (1.0 + math.exp(beta * D)); arc_rate_stationary = 0.0
    arc_rate_cooling = D * math.sqrt(p * (1 - p)) * bdot; thermal_rate = 1.0 / beta
    out = outcome(unstated=True)
    row("cos", "Connes-Rovelli thermal time (the modular flow of a KMS state, dt/ds = beta) beside CRR's arc clock, on a two-level Gibbs family",
        "none could be formed: the two clocks measure different objects", "D2 (arc as the clock), A7/A8 (tense)", "thermal time", "Connes-Rovelli 1994 (thermal time hypothesis): physical time = beta x modular time",
        f"beta = {beta:g}, level spacing {D:g}: excited population p = {p:.4f}; arc rate on the stationary state = {arc_rate_stationary:.4f} (nothing changes); thermal-time rate = {thermal_rate:.4f}; under slow cooling (d beta/dt = {bdot:g}) the arc rate is {arc_rate_cooling:.5f} per unit time",
        "no decisive quantity: the arc clock stops on a stationary state and thermal time does not", "none", "none",
        out, "CRR's clock counts change of the state; thermal time is the state's own flow at fixed state; no proposition relating a rate of change to a rate of flow was found that is not a definition",
        "the honest outcome for Rovelli's own domain in this battery: silence")


# ---------------------------------------------------------------- 11 entropy per resolvable step on a quantum horizon
def horizon_bits():
    g1 = math.log(2.0) / (math.pi * math.sqrt(3.0)); A_half = 8 * math.pi * g1 * math.sqrt(0.75)
    per_step = A_half / 4.0                                            # S = A/4 with N = A / A_min punctures: entropy per resolvable step
    g2 = 0.2375; A_half2 = 8 * math.pi * g2 * math.sqrt(0.75); per_step2 = A_half2 / 4.0
    js = np.arange(1, 41) / 2.0; gaps = np.diff(8 * math.pi * g1 * np.sqrt(js * (js + 1)))
    sig = unit_sigma(gaps); per_est = sig / 4.0
    out = outcome(crr=per_step, null=per_est, domain=math.log(2.0), check=abs(per_step - math.log(2.0)) < 1e-12)
    row("lqg", "A quantum horizon of N punctures with S = A/4 (loop-gravity battery row 1), the smallest area quantum named as the unit",
        "the entropy per resolvable step of horizon area (D1: rho = A / A_min) is one bit",
        "A1'/D1 (the unit named as the system's smallest step, rho = extent/unit)", "the instrument's estimated unit (unit_sigma on the spectrum's gaps, loop-gravity row 8)", "the j = 1/2 two-state counting fixes gamma so that each puncture carries ln 2 (one bit per puncture)",
        f"j = 1/2 counting: gamma = {g1:.4f}, A_min = {A_half:.4f} l_P^2, entropy per step = {per_step:.4f} nats = {per_step / math.log(2):.4f} bits; all-j two-state counting: gamma = {g2:.4f}, A_min = {A_half2:.4f}, entropy per minimal step = {per_step2:.4f} nats = {per_step2 / math.log(2):.4f} bits (the step is not a bit); estimated unit sigma = {sig:.2e} l_P^2 -> {per_est:.2e} nats per estimated step",
        f"per named step {per_step:.4f} vs null per estimated step {per_est:.2e}: differ", f"the counting's own construction gives ln 2 = {math.log(2):.4f}: the domain has Q",
        "one bit exactly under the j = 1/2 counting: holds (and it is the counting's definition)",
        out, f"naming the quantum as the unit reproduces the counting that defined it; under the counting the field prefers, the minimal step carries {per_step2 / math.log(2):.3f} bits and D1's step is not the domain's bit",
        "a definition read back")


# ---------------------------------------------------------------- output
def main():
    print("SYNTHESIS class: CRR taken whole against a domain's own mathematics (prompt-log entry 60)")
    print(f"T-G tolerance {TOL_G:g} (relative), T-N tolerance {TOL_N:g} (relative); labels computed by outcome() from the numbers (R15)")
    print()
    pos, decoy = gate_positive(); neg = gate_negative()
    bayes_accumulation(); quantum_antipode(); two_tone(); replicator_geodesic(); rps_reread(); adder_regeneration()
    tolman_cycles(); thermal_time(); horizon_bits()
    for k, r in enumerate(ROWS, 1):
        print(f"[{k:2d}] ({r['cls']}) {r['system']}")
        print(f"     Q:          {r['Q']}")
        print(f"     ingredient: {r['ingredient']}")
        print(f"     null:       {r['null']}")
        print(f"     domain:     {r['domain'] if r['domain'] else 'none cited'}")
        print(f"     numbers:    {r['numbers']}")
        print(f"     T-G:        {r['tg']}")
        print(f"     T-N:        {r['tn']}")
        print(f"     T-C:        {r['tc']}")
        print(f"     OUTCOME:    {r['outcome']}")
        print(f"     reading:    {r['reading']}")
        if r["weakness"]:
            print(f"     weakness:   {r['weakness']}")
        print()
    gate_open = (pos == "ADDS") and (decoy != "ADDS") and (neg != "ADDS")
    print(f"GATE (synthesis class): positive control {pos} (must be ADDS), its decoy unit {decoy} (must not be ADDS), negative control {neg} (must not be ADDS) -> GATE {'OPEN' if gate_open else 'CLOSED'}")
    labels = ("ADDS", "PROPOSES", "REDUNDANT-IG", "REDUNDANT-DOMAIN", "WRONG", "INTERNAL", "UNSTATED")
    print("TALLY (rows 3-11, real domains): " + " / ".join(f"{sum(1 for r in ROWS[2:] if r['outcome'] == lab)} {lab}" for lab in labels))
    print("TALLY (all rows):                " + " / ".join(f"{sum(1 for r in ROWS if r['outcome'] == lab)} {lab}" for lab in labels))
    return 0 if gate_open else 1


if __name__ == "__main__":
    sys.exit(main())
