"""CRR retrodiction battery on systems far from the earlier batteries (owner request 2026-09-17/18, prompt-log
entry 51): road traffic (Nagel-Schreckenberg stop-and-go), human handwriting (the isochrony principle),
mast seeding in trees (the resource-budget model), pulsar glitches (threshold-release models and the
size/waiting-time correlations), immune imprinting (antigenic seniority as a third memory class), maintenance
scheduling (odometer vs calendar under variable usage), a dripping tap (Tate's law), and cache replacement
(LRU as age weights, LFU as the accumulated count A6 forbids).

Grades under the issue-#21 rules (SHARP / CONSIST / DESCR / FAILS / TENSION / OPEN; rule 2 on chosen
observables, rule 3 on definitions, rule 4 on symmetric members); BORROWED and FLOW per row; H-L5 class where
the system has its own events, exclusive segmentation where the event is a reset (prompt-log entry 41); every
class or regime label computed from its number; a margin below 0.01 is not a reading; on noisy carriers the
arc is the sampled arc at the stated step (prompt-log entry 48's D2 finding). Model systems only; no dataset
opened (R2). Deterministic (seeded). Run:
uv run python theory/retrodictions/wild_systems.py
"""
import math
import sys

import numpy as np

from crr.instrument.core import arc_length, regularity

ROWS = []


def row(cls, system, clause, borrowed, flow, derivation, known, verdict, grade, l5=None, weakness=""):
    ROWS.append(dict(cls=cls, system=system, clause=clause, borrowed=borrowed, flow=flow, derivation=derivation,
                     known=known, verdict=verdict, grade=grade, l5=l5, weakness=weakness))


def cv(x): x = np.asarray(x, float); return float(x.std(ddof=1) / abs(x.mean()))


def l5_class(x, events, dt=1.0, segment_end="inclusive"):
    r = regularity(np.asarray(x, float), np.asarray(events, int), sigma=1.0, dt=dt, n_boot=200, seed=0, segment_end=segment_end)
    if abs(r["cv_arc"] - r["cv_clock"]) < 1e-3: lab = "tie"
    else: lab = "arc-regular" if r["cv_arc"] < r["cv_clock"] else "clock-regular"
    return lab, r["cv_arc"], r["cv_clock"]


def lab_of(arcs, times):
    d = cv(arcs) - cv(times)
    return "tie" if abs(d) < 1e-3 else ("arc-regular" if d < 0 else "clock-regular")


def reading(lab, ca, cc):
    return lab if (lab == "tie" or abs(ca - cc) >= 0.01) else f"{lab} by {abs(ca - cc):.3f}, below the 0.01 this battery treats as a reading"


# ================================================================ (traf) road traffic
def traf_nagel_schreckenberg():
    """Nagel-Schreckenberg cellular automaton (v_max 5, randomisation p 0.3, density 0.15: the jammed regime). One tagged
    car; own event = coming to a stop; carrier = its velocity; occasion = stop to stop (the stop is a state, not a jump:
    inclusive segmentation)."""
    rng = np.random.default_rng(1); L = 1000; N = 150; vmax = 5; p = 0.3; T = 4000
    pos = np.sort(rng.choice(L, N, replace=False)); vel = np.zeros(N, int); vtrace = np.empty(T)
    for t in range(T):
        gap = (np.roll(pos, -1) - pos - 1) % L
        vel = np.minimum(vel + 1, vmax); vel = np.minimum(vel, gap); slow = rng.random(N) < p; vel = np.where(slow & (vel > 0), vel - 1, vel)
        pos = (pos + vel) % L; vtrace[t] = vel[0]
    stops = np.where((vtrace[1:] == 0) & (vtrace[:-1] > 0))[0] + 1
    lab, ca, cc = l5_class(vtrace, stops[2:], 1.0)
    gaps = np.diff(stops[2:]); arcs = [arc_length(vtrace[a:b + 1]) for a, b in zip(stops[2:-1], stops[3:])]
    row("traf", "Nagel-Schreckenberg traffic (jammed regime): a tagged car's stop-to-stop occasions on its velocity carrier", "D5 (the stop = own event), D2 (arc of the velocity path), H-L5",
        "Nagel-Schreckenberg 1992 cellular automaton; stop-and-go waves", "the density, the randomisation p and the other cars (system-supplied)",
        f"{len(stops)} stops in {T} steps; mean stop-to-stop interval {gaps.mean():.1f} steps (CV {cv(gaps):.2f}), mean velocity arc per occasion {np.mean(arcs):.1f} (CV {cv(arcs):.2f}); CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}",
        "jams propagate upstream at a characteristic speed; a car's stop-to-stop interval is set by the jam spacing, which the randomisation makes broadly distributed",
        f"{reading(lab, ca, cc)}: a car that stops and restarts traverses a velocity path whose arc is roughly twice v_max whenever it reaches free flow and less when it crawls; the class is set by how often it crawls, a property of the density, not of any clause",
        "OPEN", (lab, ca, cc), "class assignment on a model at one density; the known results (jam speed, fundamental diagram) are not reached by any clause")


# ================================================================ (motor) handwriting
def motor_isochrony():
    """Minimum-jerk strokes of random amplitude A under three timing laws: isochrony (duration fixed regardless of A, the
    handwriting principle), constant peak speed (duration proportional to A), and the empirical weak scaling T ~ A^0.25.
    Own event = stroke onset; arc = A (the stroke is monotone); clock = its duration."""
    rng = np.random.default_rng(2); n = 200; A = np.exp(0.5 * rng.standard_normal(n)); noise = 1 + 0.05 * rng.standard_normal(n)
    laws = (("isochrony (T fixed)", np.ones(n)), ("constant peak speed (T ~ A)", A), ("empirical T ~ A^0.25", A ** 0.25))
    out = [(name, cv(A), cv(T * noise), lab_of(A, T * noise)) for name, T in laws]
    row("motor", "Handwriting strokes (minimum-jerk): the isochrony principle vs constant-speed timing", "D5 (stroke onset = own event), D2 (arc = stroke amplitude, monotone so S = 0), H-L5",
        "Viviani & Terzuolo isochrony; minimum-jerk model (Flash & Hogan 1985); the two-thirds power law", "the timing law of the motor system (physiology-supplied)",
        "; ".join(f"{name}: CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}" for name, ca, cc, lab in out),
        "stroke duration is nearly independent of stroke size (isochrony), so speed scales with size; the exact exponent of the residual dependence is debated",
        f"isochrony: {reading(*out[0][3:4], out[0][1], out[0][2])}; constant speed: {reading(out[1][3], out[1][1], out[1][2])}; empirical exponent: {reading(out[2][3], out[2][1], out[2][2])}; the motor system is clock-regular by its own law, the mirror image of the adder, and the framework only names the class the law already fixes",
        "DESCR", None, "rule 3: the class is the timing law renamed; the first system in the batteries that is clock-regular by physiology rather than by construction, and it says the clock claim of H-L5 has a natural counter-class")


# ================================================================ (eco) mast seeding
def eco_mast_seeding():
    """Isagi resource-budget model: a tree accumulates photosynthate P each year; when the store S exceeds L it flowers,
    spending (1 + k) times the excess (k = fruit cost / flower cost). k < 1 converges to annual flowering (the model's
    fixed point); k > 1 gives irregular masting. Weather makes P vary (registered CV 0.3). Registered k in {1.5, 3};
    k = 0.5 is run only to show the annual fixed point. Own event = mast year; carrier = the store S (the depletion is
    the cut: exclusive segmentation)."""
    rng = np.random.default_rng(3); L = 1.0; P0 = 0.3; T = 3000
    def run(k):
        S = 0.0; trace = np.empty(T); events = []
        for t in range(T):
            P = P0 * (1 + 0.3 * rng.standard_normal()); S += P
            if S > L:
                events.append(t); S = S - (1 + k) * (S - L)
            trace[t] = S
        return trace, np.array(events)
    _, ev_annual = run(0.5); n_annual = len(ev_annual)
    out = []
    for k in (1.5, 3.0):
        trace, ev = run(k); lab, ca, cc = l5_class(trace, ev[5:], 1.0, segment_end="exclusive"); gaps = np.diff(ev[5:])
        out.append((k, len(ev), float(gaps.mean()), cv(gaps), lab, ca, cc))
    row("eco", "Mast seeding (Isagi resource-budget model) with weather-driven production: mast years as occasions", "D5 (mast year = own event), A3 (the depletion is the cut, exclusive segmentation), D2 (arc of the resource store), H-L5",
        "Isagi et al. 1997 resource budget; Satake & Iwasa 2000 (k > 1 gives chaotic masting)", "the photosynthate rate (weather-supplied) and the depletion coefficient k",
        f"k = 0.5: {n_annual} masts in {T} years (annual flowering, the fixed point); " + "; ".join(f"k = {k:g}: {n} masts, mean interval {mi:.1f} years (CV {ci:.2f}), CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}" for k, n, mi, ci, lab, ca, cc in out),
        "mast intervals are irregular when the fruiting cost exceeds the flowering cost (k > 1); masting is resource-driven, not calendar-driven",
        f"k = 1.5: {reading(*out[0][4:7])}; k = 3: {reading(*out[1][4:7])}; the tree is an adder whose starting store after a mast varies with the overshoot, so the arc to the next threshold varies as much as or more than the interval: the resource-budget model is not in the arc-regular class even though it is resource-driven, and the framework's slogan would have predicted otherwise",
        "OPEN", (out[1][4], out[1][5], out[1][6]), "class assignment on a model; a resource-driven system that is not arc-regular because the reset is variable: the class needs both a fixed chord and a fixed reset, which the adder has and the masting tree does not")


# ================================================================ (astro) pulsar glitches
def astro_pulsar_glitches():
    """Threshold-release (reservoir) models of glitching: the crust-superfluid lag accumulates at a fixed rate and a glitch
    releases it. Model A: the threshold varies from glitch to glitch and the release is complete (size_n = threshold_n).
    Model B: the threshold is fixed and the released fraction varies. A6 says the next occasion is seeded from the settled
    past: a forward dependence (waiting time after a glitch set by its size). Which correlation each model produces."""
    rng = np.random.default_rng(4); n = 400; rate = 1.0
    thr = 1.0 * (1 + 0.2 * rng.standard_normal(n)); size_A = thr.copy(); wait_A = thr / rate                         # wait_n precedes size_n (time to reach threshold_n)
    frac = np.clip(0.5 + 0.2 * rng.standard_normal(n), 0.05, 0.95); lag = 1.0; size_B = np.empty(n); wait_B = np.empty(n)
    for i in range(n):
        wait_B[i] = (1.0 - lag) / rate if i > 0 else 0.0; size_B[i] = frac[i] * 1.0; lag = 1.0 - size_B[i]
    def corr(a, b): return float(np.corrcoef(a, b)[0, 1])
    back_A, fwd_A = corr(size_A[1:], wait_A[1:]), corr(size_A[:-1], wait_A[1:])
    back_B, fwd_B = corr(size_B[1:], wait_B[1:]), corr(size_B[:-1], wait_B[1:])
    row("astro", "Pulsar glitches as threshold release: backward vs forward size/waiting-time correlations in two reservoir models", "A6 (the next occasion is seeded from the settled past: a forward dependence), D5 (glitch = own event), A8 (a comparative forecast from settled occasions)",
        "superfluid-reservoir (snowplough) glitch models; size/waiting-time correlation analysis", "the spin-down rate and the threshold or release statistics (star-supplied)",
        f"model A (variable threshold, full release): corr(size_n, preceding wait_n) = {back_A:.2f} (backward), corr(size_n, following wait_n+1) = {fwd_A:.2f} (forward); model B (fixed threshold, variable release): backward {back_B:.2f}, forward {fwd_B:.2f}",
        "glitching pulsars show size/waiting-time correlations of either kind; which kind is a property of the pulsar",
        "A6 read as universal predicts a forward dependence of the next occasion on the settled one; model A has none (the next glitch is set by the next threshold, not by the past release), model B has it exactly; so the forward correlation is a signature of which quantity varies, not a consequence of regeneration",
        "FAILS", None, "rule 4 / class dependence: on the variable-threshold model the settled occasion carries no information about the next; A6 holds only where the release, not the threshold, varies; the real forecast (A8) is model B's and is the domain's own")


# ================================================================ (immu) immune imprinting
def immu_antigenic_seniority():
    """Antigenic seniority as a toy model of imprinting: exposures m = 1..6; the response weight of exposure m is s^(m-1)
    (earliest strongest). Variant (i): equal cross-reactivity, so influence is seniority alone; variant (ii): an antigenic-
    distance kernel exp(-|d|/2) to a test strain beyond the last exposure. The influence of each settled exposure on the
    final titre is MEASURED by removal. Three memory classes are now on record: recency (reservoir, P3), wiping-out
    (Preisach), primacy (this row)."""
    rng = np.random.default_rng(5); s = 0.6; pos = np.cumsum(rng.uniform(0.5, 1.5, 6)); test = pos[-1] + 0.5
    w = s ** np.arange(6); age = np.arange(6)[::-1]
    out = []
    for name, sim in (("equal cross-reactivity", np.ones(6)), ("antigenic-distance kernel", np.exp(-np.abs(test - pos) / 2.0))):
        def titre(mask): return float(np.sum(w[mask] * sim[mask]))
        full = titre(np.ones(6, bool)); infl = np.array([full - titre(np.arange(6) != i) for i in range(6)])
        q_fit = float(np.exp(np.polyfit(age, np.log(infl), 1)[0])); r_age = float(np.corrcoef(age, np.log(infl))[0, 1])
        out.append((name, infl, q_fit, r_age))
    row("immu", "Immune imprinting (antigenic seniority): measured influence of each settled exposure on the final titre", "P3 (age weights, pi_k proportional to q^k), P2 (surplus weights), A6; O2 (which constraint)",
        "antigenic seniority / original antigenic sin (Lessler et al. 2012 as the seniority form); cross-reactivity as a similarity kernel", "the exposure history and the similarity kernel (immunology-supplied)",
        "; ".join(f"{name}: influence by exposure order = {', '.join(f'{v:.3f}' for v in infl)}, geometric age fit q = {q:.2f} (1/s = {1 / s:.2f}), correlation(age, log influence) = {r:.2f}" for name, infl, q, r in out),
        "antibody responses are dominated by the first strains encountered (imprinting); later exposures add progressively less; cross-reactivity modulates this",
        f"seniority alone gives age weights with q = {out[0][2]:.2f} > 1, the opposite of fading memory; with the distance kernel the oldest-strongest ordering is partly masked (q = {out[1][2]:.2f}); P2 gives uniform weights because the exposures have equal surplus; the row is constructed (rule 3) but records a third memory class, primacy, beside recency and wiping-out, none of which the framework distinguishes",
        "DESCR", None, "rule 3: the model encodes the answer; the value is taxonomic: any T5 prereg must say which of the three memory classes its carrier belongs to before the gate")


# ================================================================ (eng) maintenance scheduling
def eng_odometer_vs_calendar():
    """Wear accumulates with a usage rate u(t) that varies (Ornstein-Uhlenbeck, registered CV 0.3); failure when wear
    crosses a Weibull-like threshold (CV 0.1); replacement resets wear. Own event = failure; carrier = wear (the reset is
    the cut, exclusive segmentation). Arc = usage accumulated (the odometer); clock = calendar time."""
    rng = np.random.default_rng(6); dt = 0.01; n_ev = 80
    def run(usage_cv, thr_cv):
        ou = 0.0; W = 0.0; trace = []; events = []; thr = 1.0 * (1 + thr_cv * rng.standard_normal(n_ev)); i = 0; t = 0
        while i < n_ev:
            ou += dt * (-0.05 * ou) + usage_cv * math.sqrt(2 * 0.05 * dt) * rng.standard_normal(); u = max(1.0 + ou, 0.05)
            W += u * dt; trace.append(W); t += 1
            if W >= thr[i]: events.append(t); W = 0.0; i += 1
        return np.array(trace), np.array(events)
    out = []
    for name, ucv, tcv in (("variable usage, tight threshold", 0.3, 0.1), ("steady usage, variable threshold", 0.0, 0.3)):
        tr, ev = run(ucv, tcv); lab, ca, cc = l5_class(tr, ev[3:], dt, segment_end="exclusive"); out.append((name, lab, ca, cc))
    row("eng", "Maintenance scheduling: odometer (usage-based) vs calendar intervals under variable usage", "D5 (failure = own event), A3 (the replacement is the cut, exclusive segmentation), D2 (arc = accumulated usage), H-L5",
        "wear-threshold reliability models; usage-based vs time-based preventive maintenance", "the usage rate (operator-supplied) and the wear threshold (component-supplied)",
        "; ".join(f"{name}: CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}" for name, lab, ca, cc in out),
        "usage-based intervals (mileage, cycles) beat calendar intervals when usage varies; calendar intervals suffice when usage is steady",
        f"variable usage: {reading(*out[0][1:4])}; variable threshold: {reading(*out[1][1:4])}; the odometer is the arc and the practice is the class map: the framework names what every fleet manager already does",
        "DESCR", None, "rule 3: the adder mechanism in an engineered setting; the everyday reading of 'change has its own clock' is a mileage counter")


# ================================================================ (fluid) dripping tap
def fluid_dripping_tap():
    """Tate's law: a drop detaches when its weight exceeds the surface-tension force, so the drop mass is fixed by the
    nozzle and the liquid; the interval is mass / flow rate. Registered: variable flow (OU, CV 0.2) with fixed drop mass
    (CV 0.03); steady flow with variable pinch-off mass (CV 0.2, a proxy for the chaotic dripping regime). Own event = drop;
    carrier = the hanging mass (the detachment is the cut, exclusive segmentation)."""
    rng = np.random.default_rng(7); dt = 0.005; n_ev = 100
    def run(flow_cv, mass_cv):
        ou = 0.0; m = 0.0; trace = []; events = []; mstar = 1.0 * (1 + mass_cv * rng.standard_normal(n_ev)); i = 0; t = 0
        while i < n_ev:
            ou += dt * (-0.1 * ou) + flow_cv * math.sqrt(2 * 0.1 * dt) * rng.standard_normal(); Q = max(1.0 + ou, 0.05)
            m += Q * dt; trace.append(m); t += 1
            if m >= mstar[i]: events.append(t); m = 0.0; i += 1
        return np.array(trace), np.array(events)
    out = []
    for name, fcv, mcv in (("Tate regime, variable flow", 0.2, 0.03), ("variable pinch-off mass, steady flow", 0.0, 0.2)):
        tr, ev = run(fcv, mcv); lab, ca, cc = l5_class(tr, ev[3:], dt, segment_end="exclusive"); out.append((name, lab, ca, cc))
    row("fluid", "Dripping tap: Tate's-law drops under variable flow vs variable pinch-off mass", "D5 (drop = own event), A3 (detachment = the cut, exclusive segmentation), D2 (arc = hanging mass), H-L5",
        "Tate's law (1864); the dripping faucet as a chaotic system (Shaw 1984) for the second regime", "the flow rate (tap-supplied) and the pinch-off mass (liquid- and nozzle-supplied)",
        "; ".join(f"{name}: CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}" for name, lab, ca, cc in out),
        "at low flow the drop mass is fixed by surface tension and the drip interval by the flow; at higher flow the drop size becomes irregular and the dripping chaotic",
        f"Tate regime: {reading(*out[0][1:4])}; variable mass: {reading(*out[1][1:4])}; a kitchen adder: the drop is arc-regular exactly where Tate's law holds, and the law, not the framework, says where that is",
        "DESCR", None, "rule 3: the same mechanism as the adder, the spring-slider and the odometer; included because the owner asked for systems far from the earlier ones, and it shows how ordinary the arc-regular class is when a threshold fixes the chord")


# ================================================================ (comp) cache replacement
def comp_cache_replacement():
    """Cache replacement on a Zipf(alpha = 0.8) request stream over 1000 items with a 50-item cache: LRU keeps the most
    recently used (age weights, P3), LFU keeps the most frequently used (an accumulated count, which A6 says a regenerating
    system never returns: 'a system that re-counts its past stops cutting'). Stationary popularity vs popularity that is
    re-drawn every 2000 requests (drift)."""
    rng = np.random.default_rng(8); N = 1000; C = 50; n_req = 40000; alpha = 0.8
    ranks = np.arange(1, N + 1); pz = ranks ** (-alpha); pz /= pz.sum()
    def stream(drift):
        perm = rng.permutation(N); out = np.empty(n_req, int)
        for t in range(n_req):
            if drift and t % 2000 == 0 and t > 0: perm = rng.permutation(N)
            out[t] = perm[rng.choice(N, p=pz)]
        return out
    def hit_rate(req, policy):
        cache = {}; hits = 0; clock = 0
        for x in req:
            clock += 1
            if x in cache:
                hits += 1; cache[x] = (cache[x][0] + 1, clock)
            else:
                if len(cache) >= C:
                    victim = min(cache, key=(lambda k: cache[k][1]) if policy == "LRU" else (lambda k: (cache[k][0], cache[k][1])))
                    del cache[victim]
                cache[x] = (1, clock)
        return hits / len(req)
    res = {}
    for name, drift in (("stationary", False), ("drifting", True)):
        req = stream(drift); res[name] = (hit_rate(req, "LRU"), hit_rate(req, "LFU"))
    row("comp", "Cache replacement: LRU (age weights) vs LFU (an accumulated count) on stationary and drifting Zipf request streams", "A6 ('regeneration returns a reweighted content, never an accumulated count'), P3 (age weights), O2",
        "LRU/LFU cache analysis; Zipf popularity; the recency-frequency trade-off", "the request stream (workload-supplied)",
        "; ".join(f"{name}: hit rate LRU {lru:.3f}, LFU {lfu:.3f} ({'LFU' if lfu > lru else 'LRU'} ahead by {abs(lfu - lru):.3f})" for name, (lru, lfu) in res.items()),
        "frequency-based replacement wins on stationary popularity, recency-based replacement wins under drift; both keep evicting",
        f"an engineered memory that re-counts its past (LFU) does not stop cutting: it evicts on every miss and outperforms age weights on the stationary stream by {res['stationary'][1] - res['stationary'][0]:.3f}; under drift age weights win by {res['drifting'][0] - res['drifting'][1]:.3f}; A6's prohibition of the count is false as a universal and the choice between count and age is the workload's (O2 again, decided by stationarity)",
        "FAILS", None, "rule 4 / class dependence: A6's 'never an accumulated count' fails on a working counting memory; what survives is that the better weighting depends on whether the past recurs in-family (O2's own condition)")


BATTERY = [traf_nagel_schreckenberg, motor_isochrony, eco_mast_seeding, astro_pulsar_glitches, immu_antigenic_seniority,
           eng_odometer_vs_calendar, fluid_dripping_tap, comp_cache_replacement]

CLASSES = {"traf": "road traffic", "motor": "human motor control", "eco": "plant ecology", "astro": "neutron stars",
           "immu": "immunology", "eng": "maintenance engineering", "fluid": "fluid mechanics", "comp": "computer systems"}


def main():
    for f in BATTERY: f()
    print(f"CRR retrodiction battery on systems far from the earlier batteries — {len(ROWS)} model systems, {len(CLASSES)} classes. Grades: SHARP CONSIST DESCR FAILS TENSION OPEN\n")
    for i, r in enumerate(ROWS, 1):
        print(f"[{i:2d}] ({r['cls']}) {r['system']}\n     clause:     {r['clause']}\n     BORROWED:   {r['borrowed']}\n     FLOW:       {r['flow']}"
              f"\n     derivation: {r['derivation']}\n     known:      {r['known']}\n     verdict:    {r['verdict']}\n     GRADE:      {r['grade']}"
              + (f"\n     H-L5 class: {r['l5'][0]} (CV_arc {r['l5'][1]:.3f}, CV_clock {r['l5'][2]:.3f})" if r['l5'] else "")
              + (f"\n     weakness:   {r['weakness']}" if r['weakness'] else ""))
    grades = ("SHARP", "CONSIST", "DESCR", "FAILS", "TENSION", "OPEN")
    print("\n" + "=" * 100 + "\nTALLY")
    print(f"{'class':32s} " + " ".join(f"{g:>8s}" for g in grades))
    for c, name in CLASSES.items():
        rs = [r for r in ROWS if r["cls"] == c]
        print(f"({c}) {name:24s} " + " ".join(f"{sum(r['grade'] == g for r in rs):8d}" for g in grades))
    print(f"{'all':32s} " + " ".join(f"{sum(r['grade'] == g for r in ROWS):8d}" for g in grades))
    print("\nH-L5 class map (model systems with their own events):")
    for r in ROWS:
        if r["l5"]: print(f"  {r['l5'][0]:44s} {r['system']}")
    print(f"\nrows where the coherence integral's velocity is system-supplied (FLOW != none): {sum('none' not in r['flow'] for r in ROWS)}/{len(ROWS)}")
    print(f"Rows where a CRR clause reaches a result the domain did not already have: {sum(r['grade'] == 'SHARP' for r in ROWS)} of {len(ROWS)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
