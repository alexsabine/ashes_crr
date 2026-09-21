"""Synthesis batch 21: rows 101-105 of QUEUE.md (prompt-log entry 61). All five from the emptiness battery
(theory/retrodictions/emptiness.txt, script emptiness.py), CRR at zero:
[3] (DESCR) a closed loop, the endpoint says nothing changed and the arc says everything did: D6/H-T1 read on a domain where
    the closed loop has a name, the stochastic pump (a single site between two reservoirs driven round a cycle);
[4] (DESCR) the future has no content: A7/A8 read against the instrument's own cut, which is located with a two-sided
    analytic signal; the causal reading of A3 against the registered one, and the Poincare-section reading CRR.md names;
[5] (DESCR) the boundary of a Fisher-native carrier, an empty category: A6/P3 regeneration of a lost allele read on the
    domain that has a name for it, the seed bank (Kaj-Krone-Lascoux), and its genealogy;
[6] (DESCR) a count carrier that is mostly zero: spike trains at the bin scale and at four smoothing scales, with the
    Poisson train as the negative control (nothing varies but the clock);
[8] (DESCR) the Kalman identity P4 at zero and infinite Fisher speed: the steady-state filter as A6 regeneration with P3
    age weights q = 1 - K(v), and the two zeros as q -> 1 (the accumulated count A6 forbids) and q -> 0 (only Now).
Every number printed is computed here (R1); every verdict word is an f-string of a comparison (R15). No data file is
opened (R2). Nothing is imported from theory/retrodictions/*.py; the source rows' models are re-implemented. Deterministic:
fixed seeds, fixed grids, explicit RK4 on a fixed dt. Run:
  uv run python theory/retrodictions/synthesis_batches/batch_21.py
"""
import math
import sys

import numpy as np
from scipy.signal import hilbert, lfilter

from crr.instrument.core import antipodal_cuts, arc_length, intrinsic_phase, poisson_transform, regularity, rho, surplus, unit_sigma
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

SRC = "theory/retrodictions/emptiness.txt"


def ag(a, b, tol=TOL_G):
    return "agree" if rel(a, b) <= tol else "differ"


def hf(ok):
    return "holds" if ok else "fails"


def _f(v, nd=4):
    """A value at round-off prints in exponent form, never as -0.0000."""
    return f"{v:.1e}" if abs(v) < 10.0 ** (-nd - 1) else f"{v:.{nd}f}"


def _ci_word(ci):
    if ci[1] < 0.0:
        return "CI below 0"
    if ci[0] > 0.0:
        return "CI above 0"
    return "CI includes 0"


# ---------------------------------------------------------------- 101: emptiness [3] the closed loop on a stochastic pump
def r1(G=1.0, T=20.0, dt=0.005, n_tr=2, n_sc=3):
    """A single site (occupation p) between reservoirs L and R at equal chemical potential; couplings g_L(t) + g_R(t) = G,
    site energy set so the equilibrium occupation is f(t); master equation dp/dt = G (f - p); current through L is
    J_L = g_L (f - p). The state loop p(t) is prescribed and identical across protocols; only the split g_L/G differs."""
    w = 2 * math.pi / T
    p_t = lambda t: 0.5 + 0.25 * np.sin(w * t)
    pdot = lambda t: 0.25 * w * np.cos(w * t)
    f_t = lambda t: p_t(t) + pdot(t) / G
    protocols = (("A, g_L/G = 0.5 + 0.4 cos(wt) (a quarter turn ahead of p: an ellipse in the (g_L/G, p) plane)", lambda t: 0.5 + 0.4 * np.cos(w * t), 0.4 * 0.25 * math.pi),
                 ("B, g_L/G = 0.5 (a fixed split)", lambda t: 0.5 + 0.0 * t, 0.0),
                 ("C, g_L/G = 0.5 + 0.4 sin(wt) (in phase with p: a line, the reciprocal loop)", lambda t: 0.5 + 0.4 * np.sin(w * t), 0.0),
                 ("D, g_L/G = 0.5 - 0.4 cos(wt) (protocol A run backwards)", lambda t: 0.5 - 0.4 * np.cos(w * t), -0.4 * 0.25 * math.pi))
    t = np.arange(0.0, (n_tr + n_sc) * T + dt / 2, dt)
    p = np.empty(len(t)); p[0] = p_t(0.0) + 0.05                       # started off the target: the relaxation onto it is a check
    rhs = lambda tt, pp: G * (f_t(tt) - pp)
    for i in range(len(t) - 1):
        tt = t[i]; k1 = rhs(tt, p[i]); k2 = rhs(tt + dt / 2, p[i] + dt / 2 * k1); k3 = rhs(tt + dt / 2, p[i] + dt / 2 * k2); k4 = rhs(tt + dt, p[i] + dt * k3)
        p[i + 1] = p[i] + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    sc = t >= n_tr * T - 1e-9; ts = t[sc]; ps = p[sc]; fs = f_t(ts); dps = np.gradient(ps, ts)
    err = float(np.abs(ps - p_t(ts)).max())
    one = ts <= n_tr * T + T + 1e-9
    theta = 2.0 * np.arcsin(np.sqrt(ps[one]))                              # Fisher-Rao coordinate of the Bernoulli family
    C, Cs, S = surplus(theta)
    C_closed = 2.0 * (2.0 * math.asin(math.sqrt(0.75)) - 2.0 * math.asin(math.sqrt(0.25)))
    sig = float(np.trapezoid(dps * np.log(fs * (1 - ps) / ((1 - fs) * ps)), ts) / n_sc)   # entropy production per cycle, both links summed
    res = []
    for name, gL, area in protocols:
        g = gL(ts); Q = float(np.trapezoid(g * (fs - ps), ts) / n_sc)     # charge through L per cycle, the master equation's own current
        res.append((name, Q, area))
    QA, QB, QC, QD = (r[1] for r in res)
    same_effect = max(abs(QA - QB), abs(QA - QC), abs(QA - QD)) <= 1e-6 * max(abs(QA), 1e-12)
    domain_ok = all(abs(Q - area) <= 1e-4 for _, Q, area in res)
    areas_differ = max(abs(res[0][2] - res[k][2]) for k in (1, 2, 3)) > 1e-6
    holds_word = "the negation of Q, not Q" if areas_differ else "Q"
    out = outcome(crr=C, null=Cs, domain=None, check=same_effect)
    return make_row("pump", f"A stochastic pump: one site between two reservoirs at equal chemical potential, total coupling G = {G:g}, the occupation driven round the closed loop p(t) = 0.5 + 0.25 sin(wt), period {T:g} (dt = {dt:g}, RK4, {n_tr} transient and {n_sc} scored cycles), under four coupling protocols that leave p(t) untouched and move only the split g_L/G",
                    source=f"{SRC} [3] (DESCR)",
                    Q="what a closed loop of the state does, the content its endpoint hides, is a function of the arc it travelled: two cycles with the same state path (equal C, C* = 0, S = C) transport the same charge between the reservoirs",
                    ingredient="D6/H-T1 (path against endpoint) read on a driven cycle; D2/D3/D4 on the Bernoulli carrier supply C, C* and S (not CRR-proper); A3 supplies no cut (one cycle is taken as one occasion)",
                    null="the endpoint: the chord C* between the start and the end of the cycle, zero on a closed loop (the reading under which a cycle does nothing)",
                    domain="the stochastic pump (Sinitsyn and Nemenman 2007; Astumian 2007; Parrondo 1998): the charge pumped per slow cycle is the area the parameter loop encloses, a Berry-phase 2-form on the space of the rates, not a length; Purcell's scallop theorem is the same statement for a swimmer (a reciprocal loop carries nothing); all named only, not fetched (R10)",
                    numbers=f"state loop identical across protocols (max deviation of the simulated p from the prescribed loop {err:.1e}): Fisher-Rao arc per cycle C = {C:.4f} (closed form 2 [theta(0.75) - theta(0.25)] = {C_closed:.4f}), chord C* = {_f(Cs)}, surplus S = {S:.4f}; entropy production per cycle {sig:.5f} (identical by construction: sum over links of J ln(forward/backward) = dp/dt ln[f(1-p)/((1-f)p)], a functional of the state path alone); pumped charge per cycle through L: "
                            + "; ".join(f"{name}: {_f(Q, 5)} (area formula {_f(area, 5)})" for name, Q, area in res),
                    tg=f"path C = {C:.4f} vs endpoint C* = {_f(Cs)}: {ag(C, Cs)} (the ingredient sees the loop; the endpoint does not)",
                    tn=f"the domain's theorem is for the charge, not the arc: the enclosed area gives {_f(res[0][2], 5)} for A and {_f(res[1][2], 5)}, {_f(res[2][2], 5)}, {_f(res[3][2], 5)} for B, C, D at equal arc (simulated charges within 1e-4 of the area formula: {hf(domain_ok)}), so the domain holds {holds_word}",
                    tc=f"equal charge for equal arc (A, B, C, D within 1e-6 of each other): {hf(same_effect)}; A and D differ by {abs(QA - QD):.5f} at identical C, and B and C pump {_f(QB, 5)} and {_f(QC, 5)}",
                    out=out,
                    reading=f"the loop is where path and endpoint differ most, and it is also where the path fails: four cycles with the same state path (C = {C:.4f}, C* = {_f(Cs)}, S = {S:.4f}) pump {_f(QA, 5)}, {_f(QB, 5)}, {_f(QC, 5)} and {_f(QD, 5)}, because what a cycle transports is the area its parameter loop encloses (A is an ellipse, D the same ellipse the other way round, B a point and C a line), which no function of the state path can see; what the state path does fix is the dissipation ({sig:.5f} per cycle for all four), the Salamon-Berry side that batch 06 row 1 found the domain already has. The source row's 'all of the arc is surplus' stands as arithmetic; read as a rule that a system cares about S when C* = 0, it is {out} on the one domain where a closed loop has a name and a theorem",
                    weakness=f"one loop shape and one drive speed (w/G = {w / G:.2f}, not adiabatic; the identity Q = integral of (g_L/G) dp is exact at any speed here because G is held constant, so the area formula is exact rather than a slow-driving limit); the state is one-dimensional, so the state loop encloses nothing by construction and the parameter loop carries all the area, which is the cleanest case and also the least general; a learner's loop schedule (T1x) has a many-dimensional state and is not modelled here",
                    elegance="A scallop that only opens and closes cannot swim: back and forth along one line, however far, carries nothing, and only a loop that goes round something does. What a closed loop carries is the area it encloses, not the distance it travelled.",
                    child="Stir your soup round in a circle and the soup goes round with the spoon. Push the spoon back and forth along one line just as far, and the soup ends up where it started. How far the spoon travelled is not what matters; what matters is whether it went round something.")


# ---------------------------------------------------------------- 102: emptiness [4] the future has no content, read against the instrument's cut
def _delayed_phase(x, d, detrend=True):
    """The analytic-signal phase at sample t computed from the record x[:t+d+1]: d samples of future are fed to the cut.
    d = 0 is the causal reading (A7); d -> the whole record is the registered instrument (intrinsic_phase)."""
    n = len(x); ph = np.empty(n)
    for t in range(n):
        end = min(n, t + d + 1); seg = x[:end]
        if detrend:
            seg = seg - seg.mean()
        ph[t] = float(np.angle(hilbert(seg)[t])) if end >= 4 else 0.0
    return np.unwrap(ph)


def _cut_future(x, ds, detrend=True):
    ph2 = intrinsic_phase(x) if detrend else np.unwrap(np.angle(hilbert(x)))
    c2 = antipodal_cuts(ph2); hp = (c2[-1] - c2[0]) / (len(c2) - 1)
    lo, hi = c2[2], c2[-2]; rows = []
    for d in ds:
        phd = _delayed_phase(x, d, detrend); cc = antipodal_cuts(phd)
        e = np.angle(np.exp(1j * (phd - ph2)))[lo:hi] / math.pi
        off = (cc - c2)[2:-1] if len(cc) == len(c2) else None
        rows.append(dict(d=d, rms=float(np.sqrt((e ** 2).mean())), emax=float(np.abs(e).max()), n=len(cc),
                         mean=(float(off.mean()) if off is not None else None), amax=(int(np.abs(off).max()) if off is not None else None)))
    return c2, hp, rows


def _poincare_cuts(x):
    """CRR.md's named alternative: the section x = 0 crossed in either direction, known at the first sample past the crossing."""
    s = np.sign(x); s[s == 0] = 1
    return np.where(np.diff(s) != 0)[0] + 1


def r2(ds=(0, 5, 10, 25, 50, 100, 200), fix_tol=2):
    t = np.linspace(0, 10, 1001); x_sine = np.sin(2 * math.pi * t)                       # the source row's signal
    rng = np.random.default_rng(0); per = rng.uniform(80, 120, 12).astype(int)
    x_fm = np.concatenate([np.sin(2 * math.pi * np.arange(P) / P) for P in per])         # period jitter, constant amplitude (S-A' shape)
    u = np.linspace(0, 2 * math.pi * 10, 1001, endpoint=False); x_asym = np.sin(u) + 1.2 * np.sin(2 * u) + 0.6 * np.sin(3 * u)   # S-E shape
    cases = (("the source's sine, 100 samples per cycle, registered instrument (detrend = True)", x_sine, True),
             ("the same sine with the mean known (detrend = False)", x_sine, False),
             ("a period-jittered sine (80-120 samples per cycle, seed 0)", x_fm, True),
             ("the asymmetric multi-harmonic waveform (S-E shape), 100 samples per cycle", x_asym, True))
    res = []
    for name, x, det in cases:
        c2, hp, rows = _cut_future(x, ds, det)
        d_fix = next((r["d"] for r in rows if r["amax"] is not None and r["amax"] <= fix_tol), None)
        res.append((name, c2, hp, rows, d_fix))
    # the Poincare-section reading on the two symmetric signals, where it and the antipode coincide
    poinc = []
    for name, x, det in cases[:1] + cases[2:3]:
        c2 = antipodal_cuts(intrinsic_phase(x)); cp = _poincare_cuts(x)
        off = np.array([int(cp[np.argmin(np.abs(cp - c))] - c) for c in c2[2:-1]])
        poinc.append((name, len(cp), len(c2), float(off.mean()), int(np.abs(off).max())))
    pmax = max(p[4] for p in poinc)
    r0 = res[0][3][0]; hp0 = res[0][2]
    causal_off = (r0["mean"] / hp0) if r0["mean"] is not None else float("nan")          # the causal reading's cut offset, half-turns
    internal = r0["amax"] is None or r0["amax"] > fix_tol
    out = outcome(crr=causal_off, null=0.0, domain=None, check=None, internal=internal)
    def dfix(k):
        d, hp = res[k][4], res[k][2]
        return f"{d} samples of future ({d / hp:.2f} half-turns)" if d is not None else f"more than {ds[-1]} samples of future"
    d0_str = f"mean {r0['mean']:+.2f} samples, max {r0['amax']}" if r0["amax"] is not None else f"cut count {r0['n']} against {len(res[0][1])}"
    def line(name, c2, hp, rows, d_fix):
        s = f"{name}: {len(c2)} cuts, {hp:.1f} samples per half-turn; " + "; ".join(
            f"d = {r['d']}: phase error rms {r['rms']:.4f}, max {r['emax']:.4f} half-turns, " + (f"cut offsets mean {r['mean']:+.2f}, max {r['amax']} samples" if r['amax'] is not None else f"cut count {r['n']} (not {len(c2)})") for r in rows)
        return s + f"; smallest d on the grid with every cut within {fix_tol} samples: " + (f"{d_fix} ({d_fix / hp:.2f} half-turns)" if d_fix is not None else "none")
    return make_row("tense", "The instrument's own cut under A7: the antipodal cut on the analytic-signal phase (intrinsic_phase, two-sided Hilbert transform over the whole record) against the same cut located from the record up to t + d, d samples of future, d = 0 the causal reading; the source's sine, the same with the mean known, a period-jittered sine, and the asymmetric S-E waveform; the Poincare section (x = 0, either direction) as CRR.md's named causal alternative",
                    source=f"{SRC} [4] (DESCR)",
                    Q="the cut at Now is settled at Now: located from the settled past alone (A7: nothing is fed by a future), so the count n(t) that bounds A8's settled sum is available at t and the sum has no term ahead of Now in the instrument as well as in the theory",
                    ingredient="A7/A8 (relational tense: nothing is fed by a future) applied to A3 (the cut on the intrinsic phase) and D5 (the settled count n(t)); the intrinsic phase has two readings on this domain, the analytic signal (registered) and the Poincare section (named in CRR.md), which the row compares",
                    null="the registered cut itself (the two-sided reading, d = the whole record), which information geometry places wherever the phase says and to which tense is foreign",
                    domain="the ideal Hilbert transformer is non-causal: its impulse response 1/(pi t) is two-sided, so the analytic signal at t needs the record after t and a causal approximation needs a delay (Gabor 1946; Oppenheim and Schafer); a Poincare section is known at the first sample past the crossing, from that sample and the one before it; named only, not fetched (R10)",
                    numbers="; ".join(line(*r) for r in res) + "; Poincare-section reading against the registered cuts: " + "; ".join(f"{name}: {np_} section crossings against {n2} cuts, offset mean {m:+.2f}, max {mx} samples (each crossing declared at the sample past it, from that sample and the one before: no future)" for name, np_, n2, m, mx in poinc),
                    tg=f"causal reading (d = 0) cut offset {causal_off:+.3f} half-turns ({d0_str}) vs the registered reading 0: {ag(causal_off, 0.0)} (two readings of the cut on this domain)",
                    tn="none cited for the offset; the domain has the non-causality of the analytic signal as a theorem and supplies the causal section as the alternative",
                    tc="not reached: which intrinsic phase A3 cuts on must be fixed before Q can be checked; on the analytic reading Q " + hf(not internal) + f" (the cut needs {dfix(0)} on the source's own sine), on the Poincare reading the cuts sit within {pmax} sample of the registered ones with no future at all",
                    out=out,
                    reading=f"the theory's sentence is a definition and exact (the source row); the instrument that counts n(t) breaks it: the registered cut on the source's own sine sits {causal_off:+.3f} half-turns ({d0_str} samples) away from where the same rule puts it with the future withheld, and it settles to within {fix_tol} samples only once {dfix(0)} have arrived; with the mean known the settling takes {dfix(1)}, so the detrender consumes a share of the future the cut needs; on the asymmetric waveform the causal phase is not a phase at all ({res[3][3][0]['n']} cuts against {len(res[3][1])}, phase error up to {res[3][3][0]['emax']:.3f} half-turns). The Poincare reading, which CRR.md names and A7 admits, places the cuts on the symmetric signals within {pmax} sample of the registered ones from the settled samples alone. So A7 bears on the open question of batch 07 row 3 (which intrinsic phase A3 cuts on): the section respects tense and the analytic signal is an instrument for the settled record, not for Now: {out}",
                    weakness="the causal reading re-estimates the whole phase from a growing record and is the crudest causal estimator (no windowing, no phase-locked loop); a causal Hilbert FIR with a registered delay would need less future than the full cycle found here, but any delay above one sample is future fed to the cut; the Poincare section coincides with the antipode only on symmetric waveforms, so on the asymmetric one the section-versus-antipode question (H-CUT) is not re-opened here; the offset at d = 0 is measured on the interior cuts (first two and last dropped)",
                    elegance="You only know you have passed the top of a hill a few steps down the other side. The cut at Now can be named only later, by as much later as the shape of the hill demands; a line you can see yourself cross needs no later at all.",
                    child="When you walk over a hill in fog you cannot say exactly where the top was until you have gone a little past it and feel the ground going down. CRR's 'cut' is like the top: to place it the way the instrument does you need to see what comes next, so it cannot be named at the moment it happens. But if the cut is a line on the ground you step over, you know it the moment your foot lands.")


# ---------------------------------------------------------------- 103: emptiness [5] an empty category regenerated: the seed bank
def _pair_coalescence(N, q, P, seed=0, max_iter=400000):
    """P pairs of ancestral lineages in a Wright-Fisher population of N; each lineage's parent lives 1 + k generations back
    with P3 weights q^k on the age k >= 0 (the seed-bank kernel), chosen uniformly among the N; the pair coalesces when both
    land on the same individual of the same generation. Returns the coalescence depths."""
    rng = np.random.default_rng(seed)
    g = np.zeros((2, P), dtype=np.int64); ind = np.zeros((2, P), dtype=np.int64)
    ind[0] = rng.integers(0, N, P); ind[1] = (ind[0] + rng.integers(1, N, P)) % N
    alive = np.ones(P, bool); T = np.zeros(P, dtype=np.int64)
    for _ in range(max_iter):
        idx = np.where(alive)[0]
        if len(idx) == 0:
            break
        d0 = g[0, idx]; d1 = g[1, idx]; mv0 = d0 <= d1; mv1 = d1 <= d0; n0 = int(mv0.sum()); n1 = int(mv1.sum())
        B0 = rng.geometric(1 - q, n0) if q > 0 else np.ones(n0, dtype=np.int64)
        B1 = rng.geometric(1 - q, n1) if q > 0 else np.ones(n1, dtype=np.int64)
        g[0, idx[mv0]] += B0; ind[0, idx[mv0]] = rng.integers(0, N, n0)
        g[1, idx[mv1]] += B1; ind[1, idx[mv1]] = rng.integers(0, N, n1)
        same = (g[0, idx] == g[1, idx]) & (ind[0, idx] == ind[1, idx])
        T[idx[same]] = g[0, idx[same]]; alive[idx[same]] = False
    return T, int(alive.sum())


def r3(N=200, qs=(0.0, 0.5, 0.7), P=60000):
    # the exact value under the P3 kernel: a geometric jump is memoryless, so each past generation is visited by a lineage
    # independently with probability 1 - q; a joint visit has probability (1 - q)^2 and coalesces there with probability 1/N
    exact = {q: N / (1 - q) ** 2 for q in qs}
    sims = {}
    for q in qs:
        T, left = _pair_coalescence(N, q, P)
        sims[q] = (float(T.mean()), float(T.std(ddof=1) / math.sqrt(len(T))), left)
    beta = {q: 1 / (1 - q) for q in qs}                                                # mean delay E[B] = 1 + q/(1-q)
    kkl = {q: N * beta[q] ** 2 for q in qs}                                             # the domain's scaling: Kingman slowed by beta^2
    # the lost allele: settled frequencies at ages 3, 2, 1, 0 (now: lost), the next generation's expected frequency
    ps = np.array([0.30, 0.20, 0.10, 0.0]); ages = np.arange(len(ps))[::-1]
    seeds = []
    for q in (0.3, 0.5, 0.7):
        w = q ** ages; w = w / w.sum(); lin = float((w * ps).sum())
        th = 2.0 * np.arcsin(np.sqrt(ps)); fre = math.sin(float((w * th).sum()) / 2.0) ** 2
        seeds.append((q, lin, fre, float(w[-1])))
    q0 = 0.5
    crr, null, dom = exact[q0], exact[0.0], kkl[q0]
    z = {q: (sims[q][0] - exact[q]) / sims[q][1] for q in qs}
    both_pos = all(lin > 0 and fre > 0 for _, lin, fre, _ in seeds)
    check = all(abs(z[q]) <= 3.0 and sims[q][2] == 0 for q in qs) and both_pos
    pos_word = "both positive" if both_pos else "not both positive"
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("popgen", f"A lost allele (an empty category, a vertex of the simplex) regenerated from the settled generations: a Wright-Fisher population of N = {N} in which each individual's parent lives 1 + k generations back with P3 weights q^k (A6 with age weights, bounded strength), q = 0 the memoryless population; the genealogy of a pair of lineages simulated ({P} pairs, seed 0) and derived",
                    source=f"{SRC} [5] (DESCR)",
                    Q="under A6 the vertex is not absorbing: an allele absent from the current generation returns from the settled ones, and the price of that memory is a genealogy slowed by a fixed factor, the pair-coalescence time rising from N to N/(1 - q)^2 generations",
                    ingredient="A6 (the next occasion seeded from the settled past at bounded strength, never an accumulated count) with P3 (geometric age weights q^k), D5 [M] (occasion = one generation), A1 on the Bernoulli family (the Frechet mean is the mean in theta = 2 arcsin sqrt p)",
                    null="the memoryless Wright-Fisher population (q = 0): a lost allele stays lost (the vertex is absorbing, fixation probability u(0) = 0) and a pair coalesces in N generations on average",
                    domain="the seed bank (Kaj, Krone and Lascoux 2001; Blath, Gonzalez Casanova, Kurt and Spano 2013): with parents drawn from B generations back, B of mean beta, the ancestral process is Kingman's coalescent slowed by beta^2; named only, not fetched (R10)",
                    numbers="; ".join(f"q = {q:g}: simulated mean pair-coalescence time {sims[q][0]:.2f} generations (SE {sims[q][1]:.2f}, {sims[q][2]} unfinished), exact under the P3 kernel N/(1 - q)^2 = {exact[q]:.2f}, z = {z[q]:+.2f}; domain beta = {beta[q]:.4f}, N beta^2 = {kkl[q]:.2f}" for q in qs)
                            + "; the lost allele, settled frequencies 0.30, 0.20, 0.10 at ages 3, 2, 1 and 0 now: next generation's expected frequency " + "; ".join(f"q = {q:g}: {lin:.4f} (the domain's linear mixing), {fre:.4f} (A6's Frechet mean in theta), weight on the lost generation {w0:.3f}" for q, lin, fre, w0 in seeds),
                    tg=f"pair-coalescence time under A6/P3 at q = {q0:g}: {crr:.2f} vs null (memoryless) {null:.2f}: {ag(crr, null)}; the seed of the lost allele {seeds[1][2]:.4f} vs the null's 0: {ag(seeds[1][2], 0.0)}",
                    tn=f"the seed-bank scaling N beta^2 with beta = 1/(1 - q) gives {dom:.2f}: {ag(crr, dom, TOL_N)} (the domain has Q, kernel and factor)",
                    tc=f"simulation against the exact value within 3 SE at every q and both seeds of the lost allele positive: {hf(check)}",
                    out=out,
                    reading=f"the boundary row's 'empty category' is a lost allele, and the domain has a name for A6 on it: the seed bank, in which each generation is sown from the settled ones with a delay kernel, the P3 shape included; the vertex is then not absorbing (the lost allele's expected return is {seeds[1][1]:.4f} under the domain's linear mixing and {seeds[1][2]:.4f} under A6's Frechet mean at q = 0.5, {pos_word}), and the genealogy is Kingman's slowed by 1/(1 - q)^2 (exact under the geometric kernel; simulated {sims[q0][0]:.2f} against {exact[q0]:.2f}), which is Kaj-Krone-Lascoux's beta^2 with beta the kernel's mean delay. A6 with P3 is here the domain's own model, so Q is the domain's: {out}. What CRR adds is the Frechet mean in place of the linear mixture (seed {seeds[1][2]:.4f} against {seeds[1][1]:.4f}), a difference in the composition and not in the genealogy, which the kernel alone fixes",
                    weakness="the genealogical scaling depends on the kernel only, so the Frechet-versus-linear difference (A6's one proper content beyond P3) is not tested by the coalescent; A6's bounded strength is the finite mean of the kernel, which the domain also assumes; a real seed bank has a bounded delay and a dormancy fraction, not a geometric kernel from age 0; N and q are two registered values each",
                    elegance="A plant that vanishes from a field is not gone while its seeds lie in the soil: each spring's seedlings come from several past years, the nearer years more. Memory that fades by a fixed fraction each year is one number, and the same number says how much more slowly the field forgets.",
                    child="Some plants disappear from a field for a year and then come back, because seeds from earlier years are still waiting in the ground, and last year's seeds are more likely to sprout than older ones. So the field remembers its past for a while. CRR has a rule for remembering the past in exactly that way, and the seed scientists already use it.")


# ---------------------------------------------------------------- 104: emptiness [6] a mostly-zero count carrier: spike trains
def r4(dt=1e-3, T=100.0, taus=(0.005, 0.02, 0.1, 0.5), n_boot=2000):
    rng = np.random.default_rng(6)
    trains = []
    isi = rng.gamma(4.0, 0.025, 3000); trains.append(("gamma(4) renewal train, 10 Hz", isi))
    isi = rng.exponential(0.1, 3000); trains.append(("Poisson train, 10 Hz (nothing varies but the clock)", isi))
    out_isi = []
    for _ in range(800):
        out_isi.append(rng.gamma(4.0, 0.05))
        for _ in range(rng.integers(2, 6)):
            out_isi.append(0.004)
    trains.append(("bursting train (2-5 spikes at 4 ms, gamma(4) burst intervals)", np.array(out_isi)))
    res = []
    for name, isi in trains:
        t = np.cumsum(isi); t = t[t < T]; n = len(t)
        c = np.bincount(np.floor(t / dt).astype(int), minlength=int(round(T / dt)))
        y = poisson_transform(c); arc = arc_length(y); ev = np.where(c > 0)[0]
        doubles = int((c > 1).sum()); empty = float((c == 0).mean()); adjacent = int((np.diff(ev) == 1).sum())   # spikes in consecutive bins share their jumps
        r_inc = regularity(y, ev, segment_end="inclusive", n_boot=n_boot); r_exc = regularity(y, ev, segment_end="exclusive", n_boot=n_boot)
        try:
            unit_sigma(c[:5000]); u_counts = "returned a unit"
        except ValueError as e:
            u_counts = f"raised ValueError: {e}"
        d = np.diff(t); u_isi = unit_sigma(d)
        sm = []
        for tau in taus:
            lam = lfilter([1.0 / tau], [1.0, -math.exp(-dt / tau)], c.astype(float))           # causal exponential rate estimate
            r = regularity(poisson_transform(lam), ev, segment_end="exclusive", n_boot=n_boot)
            sm.append((tau, r))
        res.append(dict(name=name, n=n, empty=empty, doubles=doubles, adjacent=adjacent, arc=arc, inc=r_inc, exc=r_exc, u_counts=u_counts, u_isi=u_isi, rho=rho(float(d.mean()), u_isi), sm=sm))
    poisson = res[1]
    poisson_arc_regular_everywhere = all(r["ci95"][1] < 0.0 for _, r in poisson["sm"])
    bare_all = all(r["inc"]["cv_arc"] < r["inc"]["cv_clock"] for r in res)
    rejected_all = all(r["u_counts"].startswith("raised") for r in res)
    rej_word = "rejects all three count series" if rejected_all else "does not reject every count series"
    out = outcome(unstated=True)
    def line(r):
        return (f"{r['name']}: {r['n']} spikes in {int(round(T / dt))} bins of {dt * 1e3:g} ms, empty bins {r['empty']:.4f}, bins with 2 spikes {r['doubles']}, intervals of one bin (spikes in adjacent bins) {r['adjacent']}, arc of the whole count carrier {r['arc']:.1f} (4 per spike = {4 * r['n']}); per interspike occasion: jump counted C = {r['inc']['C_mean']:.4f}, CV(arc) = {_f(r['inc']['cv_arc'])}, jump excluded C = {r['exc']['C_mean']:.4f}, CV(arc) = {_f(r['exc']['cv_arc'])}, CV(clock) = {r['inc']['cv_clock']:.4f}; unit on the count series (first 5000 bins): {r['u_counts']}; unit on the interspike intervals: {r['u_isi']:.4f} s, rho = {r['rho']:.2f}; smoothed carrier (causal exponential rate, jump excluded): "
                + "; ".join(f"tau = {tau * 1e3:g} ms: C = {rr['C_mean']:.3f}, CV(arc) = {rr['cv_arc']:.4f}, CV(clock) = {rr['cv_clock']:.4f}, {_ci_word(rr['ci95'])}" for tau, rr in r["sm"]))
    return make_row("spikes", f"Three spike trains as count carriers at {dt * 1e3:g} ms bins over {T:g} s (seed 6): a gamma(4) renewal train, a Poisson train and a bursting train; the spike as the cut, the interspike interval as the occasion, the Fisher arc of the binned rate (poisson_transform) at the bin scale and on a causal exponentially smoothed rate at four time constants",
                    source=f"{SRC} [6] (DESCR)",
                    Q="none could be formed: on a mostly-zero count carrier the arc between spikes is the spike's own jump, a constant for every train, and on the smoothed carrier the class is the smoother's",
                    ingredient="tried: A1'/D1 (the unit on the count series and on the interspike intervals), A3/D5 (the spike as the cut, the jump as content or as cut), H-L5 (arc against clock between own events) on the bin-scale carrier and on smoothed carriers; D2 on the Poisson-rate carrier (P6, not proper)",
                    null="the clock: the interspike-interval statistics the domain already has (CV 1/sqrt(4) for the gamma(4) train, 1 for the Poisson train)",
                    domain="none needed: no Q was formed; the domain's own quantities for a train are the interspike-interval distribution and the count variance across windows (the Fano factor), which H-L5 on this carrier does not reach",
                    numbers="; ".join(line(r) for r in res),
                    tg=f"no decisive quantity: at the bin scale CV(arc) is {_f(res[0]['inc']['cv_arc'])} on the gamma train and {_f(res[2]['inc']['cv_arc'])} on the bursting train whatever the neuron does (every occasion carries the constant {res[0]['inc']['C_mean']:.4f}, or {res[0]['exc']['C_mean']:.4f} with the jump excluded), and {_f(res[1]['inc']['cv_arc'])} on the Poisson train only through the {res[1]['adjacent']} intervals of one bin and {res[1]['doubles']} double-occupied bin, where two spikes share a jump",
                    tn="none",
                    tc=f"none; the negative control on the smoothed carrier: the Poisson train reads arc-regular (CI of CV(arc) - CV(clock) below 0) at every smoothing scale: {hf(poisson_arc_regular_everywhere)}",
                    out=out,
                    reading=f"the source row said the unit does not exist on a mostly-zero carrier (unit_sigma {rej_word}) and that the arc is a sum of event-sized jumps; taken to a domain that has such trains, no proposition survives: at the bin scale every interspike occasion carries the same arc ({res[0]['inc']['C_mean']:.4f} with the jump, {res[0]['exc']['C_mean']:.4f} without), so CV(arc) is {_f(res[0]['inc']['cv_arc'])} on the gamma train and {_f(res[2]['inc']['cv_arc'])} on the bursting train, and the bare inequality CV(arc) < CV(clock) {hf(bare_all)} on all three trains by the arithmetic of the carrier, the natural-time clause of A1' (one spike = one step) rewritten in bins; on the smoothed carrier the arc per occasion is a concave function of the interval that the smoother fixes (C from {res[1]['sm'][0][1]['C_mean']:.3f} to {res[1]['sm'][-1][1]['C_mean']:.3f} on the Poisson train from tau = {taus[0] * 1e3:g} to {taus[-1] * 1e3:g} ms), and the Poisson train, in which nothing varies but the clock, reads arc-regular at every tau (CV(arc) {poisson['sm'][0][1]['cv_arc']:.4f} to {poisson['sm'][-1][1]['cv_arc']:.4f} against CV(clock) {poisson['sm'][0][1]['cv_clock']:.4f}), which by R4 says the smoothed carrier is not about CRR; the bin width and the time constant are both outside constants, the open A1' INTERNAL of batch 01 row 3 (event against window) and batch 14 row 5 (the smoothing scale moves the class) on a third carrier. The unit exists only on the intervals ({res[0]['u_isi']:.4f} s on the gamma train, rho = {res[0]['rho']:.2f}), where the domain's own statistic already lives: {out}",
                    weakness="three model trains and one bin width; the smoothed rate is a causal exponential estimator with four registered time constants, not a sweep; a membrane-potential carrier between spikes (batch 13 row 4) is a different carrier and is not repeated here; nothing here re-scores any ledger row",
                    elegance="Between two clicks of a Geiger counter there is nothing to add up: all the travel is in the clicks, and every click is the same size. On a train of clicks, distance is only the count.",
                    child="A Geiger counter clicks now and then. Between clicks nothing happens that you could measure, and every click is just a click, the same as the last. So if you try to measure how far the counter has 'travelled', all you can do is count the clicks, and that tells you nothing new about what made them.")


# ---------------------------------------------------------------- 105: emptiness [8] the Kalman identity at its two zeros as P3
def _riccati_gain(v, r=1.0, iters=100000):
    q = v * v * r; P = 1.0
    for _ in range(iters):
        Pn = P * r / (P + r) + q
        if abs(Pn - P) < 1e-15:
            P = Pn; break
        P = Pn
    return P / (P + r)


def r5(vs=(0.01, 0.1, 0.5, 1 / math.sqrt(2), 1.0, 2.0, 10.0, 100.0), n_seen=1000):
    K_closed = lambda v: (v / 2) * (math.sqrt(v * v + 4) - v)
    rows = []
    for v in vs:
        K = _riccati_gain(v)
        xh = 0.0; resp = []
        for tt in range(8):                                                             # impulse response of the steady-state filter
            y = 1.0 if tt == 0 else 0.0; xh = xh + K * (y - xh); resp.append(xh)
        ratios = [resp[i + 1] / resp[i] for i in range(7)]
        rows.append(dict(v=v, K=K, Kc=K_closed(v), q=1 - K, kbar=(1 - K) / K, ratio_min=min(ratios), ratio_max=max(ratios)))
    r1_ = next(r for r in rows if r["v"] == 1.0)
    crr = r1_["kbar"]; null = (n_seen - 1) / 2.0                                         # the accumulated count: n_seen observations weighted equally
    dom = (1 - r1_["K"]) / r1_["K"]                                                        # Muth: EWMA weight alpha = K, mean age (1 - alpha)/alpha
    check = all(abs(r["K"] - r["Kc"]) < 1e-9 and abs(r["ratio_min"] - r["q"]) < 1e-9 and abs(r["ratio_max"] - r["q"]) < 1e-9 for r in rows)
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    lo, hi = rows[0], rows[-1]
    golden = "equal to the gain itself, 1/phi (phi - 1 = 1/phi)" if abs(r1_["kbar"] - r1_["K"]) < 1e-9 else "not equal to the gain"
    return make_row("filter", "Scalar random-walk Kalman filter at steady state (observation variance r = 1, process variance q = v^2, Fisher speed v = sqrt(q/r)), its gain K(v) of P4 from the Riccati recursion and its impulse response, read as A6 regeneration from the settled observations with P3 age weights, across v from 0.01 to 100 (the two zeros of the source row approached from inside)",
                    source=f"{SRC} [8] (DESCR)",
                    Q="the filter's memory is P3: its weight on an observation of age k is K (1 - K)^k, so q_P3 = 1 - K(v) and the mean age is 1/K(v) - 1; the source row's two emptinesses are P3's two ends, K -> 0 the accumulated count (q -> 1, mean age ~ 1/v -> infinity, the count A6 forbids) and K -> 1 only Now (q -> 0)",
                    ingredient="A6 (regeneration from the settled past at bounded strength, never an accumulated count) with P3 (geometric age weights), read on P4 (which CRR.md says is not CRR's); O1 (retention depth) is what the row's mean age would be",
                    null=f"the accumulated count: the sample mean of all {n_seen} observations seen, every age weighted equally (mean age {null:.1f}), the v = 0 filter's own limit",
                    domain="Muth 1960 (optimal properties of exponentially weighted forecasts): for the local-level model the optimal one-step forecast is the EWMA with weight alpha = K, so the weight on age k is K (1 - K)^k; with Harrison 1967 and the steady-state Riccati equation; named only, not fetched (R10)",
                    numbers="; ".join(f"v = {r['v']:.4g}: K = {r['K']:.6f} (P4 closed form {r['Kc']:.6f}), impulse-response ratio {r['ratio_min']:.6f} to {r['ratio_max']:.6f}, q_P3 = 1 - K = {r['q']:.6f}, mean age {r['kbar']:.4f} (1/v = {1 / r['v']:.4f})" for r in rows),
                    tg=f"mean age of the settled past at v = 1 under P3: {crr:.6f} vs null (the accumulated count over {n_seen} observations) {null:.1f}: {ag(crr, null)}",
                    tn=f"Muth's EWMA weight alpha = K gives mean age (1 - K)/K = {dom:.6f}: {ag(crr, dom, TOL_N)} (the domain has Q)",
                    tc=f"Riccati gain equal to P4 within 1e-9 and impulse-response ratio equal to 1 - K within 1e-9 at all {len(rows)} speeds: {hf(check)}",
                    out=out,
                    reading=f"the steady-state filter weights its settled observations geometrically with ratio 1 - K(v) at every speed (impulse-response ratio {r1_['ratio_min']:.6f} at v = 1, 1 - K = {r1_['q']:.6f}), so the filter is A6 with P3 weights and P3's free q is fixed by the domain, q = 1 - K(v); the two emptinesses of the source row are the two ends of P3: at v = {lo['v']:g} the mean age is {lo['kbar']:.2f} (1/v = {1 / lo['v']:.0f}), the accumulated count A6 forbids, reached only at v = 0, and at v = {hi['v']:g} it is {hi['kbar']:.4f}, only Now; at v = 1 the mean age is {r1_['kbar']:.6f}, {golden}. The mapping is Muth's theorem (exponential smoothing is the optimal forecast of a random walk seen in noise) and the retention depth O1 declines to claim is 1/K(v) - 1 here, which batch 09 row 2 used as the source's D8 route; the reading of Omega = 1 (batch 02 row 4, batch 06 row 3) is untouched: {out}",
                    weakness="one state model (the random walk), for which P3's kernel is exact; on a mean-reverting or oscillatory model the steady-state filter's kernel is not geometric and P3 would be an approximation, the case O1 names and this row does not run; the null's mean age depends on the registered number of observations seen",
                    elegance="A filter that trusts its model completely stops listening; one with no model only listens. How far back it listens is one number, and it is the same number as how much it trusts the newest datum.",
                    child="Imagine guessing tomorrow's temperature from past days. If you believe the weather never really changes, you average every day you have ever seen and barely notice today. If you believe it changes wildly, you trust only today. In between, how many old days you keep counting and how much you trust today are one choice, one dial, not two.")


def main():
    return run_batch("Synthesis batch 21: rows 101-105 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
