"""Synthesis batch 19: rows 91-95 of QUEUE.md (prompt-log entry 61). Twenty-systems battery [12] fibre-bundle model of
cascading failure, bursts and the critical load (DESCR); [13] TD(lambda) on the 19-state random walk, accumulating against
replacing eligibility traces (DESCR); [14] the Kovacs memory effect in a two-mode glass model (DESCR); [15] Elo ratings, the
best K-factor against skill volatility (DESCR); [16] cricket chirps under drifting temperature, Dolbear's law (DESCR).
Source rows are in theory/retrodictions/twenty_systems.txt; their models are re-implemented here (nothing imported from the
battery script). Deterministic (fixed seeds, fixed grids, explicit Euler steps at the source's step); no data file opened (R2).
Three earlier rows read an A6/P3 memory kernel as an ADDS candidate with the caution that any exponential kernel does the
same (synthesis row 8, batch 12 row 2, batch 17 row 1); row 3 here reaches the same kernel from the other side (what a
single exponential kernel cannot do) and says so. Run:
  uv run python theory/retrodictions/synthesis_batches/batch_19.py
"""
import math
import sys

import numpy as np

from crr.instrument.core import arc_length, cv, regularity
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

TW = "theory/retrodictions/twenty_systems.txt"


def _word(cond, yes, no):
    return yes if cond else no


def _agree(a, b, tol=TOL_G):
    return _word(rel(a, b) <= tol, "agree", "differ")


def _hf(cond):
    return _word(cond, "holds", "fails")


# ---------------------------------------------------------------- 91 [12] fibre bundle: the antipode against the extremum
def _bundle(thr):
    """Equal-load-sharing bundle under quasi-static load: returns (max load per fibre, broken fraction at that load,
    burst sizes). The source's loop."""
    thr = np.sort(np.asarray(thr, float)); N = len(thr); alive = N; loads = []; broken = []; bursts = []
    while alive > 0:
        k = N - alive; F = thr[k] * alive; loads.append(F / N); broken.append(k / N); s = 0
        while alive > 0 and thr[N - alive] * alive <= F:
            alive -= 1; s += 1
        bursts.append(s)
    loads = np.asarray(loads); i = int(np.argmax(loads))
    return float(loads[i]), float(broken[i]), np.asarray(bursts)


def _daniels(kind, k=None):
    """Daniels' critical point 1 - P(x_c) = x_c p(x_c): (broken fraction P(x_c), critical load x_c (1 - P(x_c)), load at the
    antipode P = 1/2, i.e. x_median / 2)."""
    if kind == "uniform":
        return 0.5, 0.25, 0.25
    xc = k ** (-1.0 / k); Pc = 1.0 - math.exp(-1.0 / k); xm = math.log(2.0) ** (1.0 / k)
    return Pc, xc * (1.0 - Pc), xm / 2.0


def r1():
    N = 20000; n_seed = 20; anti = 0.5
    rng = np.random.default_rng(12); sc_src, xb_src, bursts = _bundle(rng.random(N))
    edges = np.array([1, 2, 4, 8, 16, 32]); cnt = np.array([((bursts >= lo) & (bursts < hi)).sum() for lo, hi in zip(edges[:-1], edges[1:])], float)
    dens = cnt / np.diff(edges); mids = np.sqrt(edges[:-1] * edges[1:]); ok = dens > 0
    slope = float(np.polyfit(np.log(mids[ok]), np.log(dens[ok]), 1)[0])
    k_coincide = 1.0 / math.log(2.0)
    dists = [("uniform", None), ("Weibull k = 1", 1.0), ("Weibull k = 2", 2.0), ("Weibull k = 5", 5.0), (f"Weibull k = 1/ln 2 = {k_coincide:.4f}", k_coincide)]
    res = []
    for name, k in dists:
        Pc, load_c, load_anti = _daniels("uniform" if k is None else "weibull", k)
        sims = []; loads = []
        for s in range(n_seed):
            g = np.random.default_rng(100 + s); thr = g.random(N) if k is None else g.weibull(k, N)
            sc, xb, _ = _bundle(thr); sims.append(xb); loads.append(sc)
        sims = np.asarray(sims); loads = np.asarray(loads)
        d_anti = abs(sims.mean() - anti); d_ext = abs(sims.mean() - Pc); coincide = abs(Pc - anti) < 1e-9
        res.append(dict(name=name, k=k, Pc=Pc, load_c=load_c, load_anti=load_anti, sim=float(sims.mean()), sd=float(sims.std(ddof=1)),
                        load_sim=float(loads.mean()), d_anti=d_anti, d_ext=d_ext, coincide=coincide))
    # decisive: the Weibull k = 2 bundle (the first registered non-flat distribution)
    w2 = res[2]; crr = anti; null = w2["Pc"]; domain = w2["Pc"]
    noncoincide = [r for r in res if not r["coincide"]]
    check = all(r["d_anti"] <= r["d_ext"] for r in noncoincide)
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    n_ext = sum(1 for r in noncoincide if r["d_ext"] < r["d_anti"])
    before = ", ".join(f"{r['k']:g}" for r in noncoincide if r["Pc"] > anti); after = ", ".join(f"{r['k']:g}" for r in noncoincide if r["Pc"] < anti)
    numbers = (f"source reproduced (seed 12, N = {N}, uniform thresholds): maximum load per fibre {sc_src:.4f} (Daniels 1/4), broken fraction at it {xb_src:.4f}, "
               f"{len(bursts)} bursts, size-distribution log-log slope on 1..32 = {slope:.2f}; the antipode on the intact-fraction carrier: theta = 2 arcsin sqrt(p) runs 0 to pi, "
               f"so half a turn from all-intact is P = {anti:.4f} of the fibres broken; Daniels' condition at the antipode reads x_median h(x_median) = 1, which the Weibull family "
               f"meets at one shape only, k = 1/ln 2 = {k_coincide:.4f}; per registered threshold distribution ({n_seed} bundles of {N} fibres each, seeds 100-{100 + n_seed - 1}): " +
               "; ".join(f"{r['name']}: Daniels' broken fraction at the critical load {r['Pc']:.4f}, critical load per fibre {r['load_c']:.4f} (simulated {r['load_sim']:.4f}), "
                         f"load per fibre at the antipode {r['load_anti']:.4f}; simulated broken fraction at maximum load {r['sim']:.4f} (sd {r['sd']:.4f}): "
                         f"|sim - antipode| {r['d_anti']:.4f}, |sim - extremum| {r['d_ext']:.4f}: "
                         + _word(r["coincide"], "antipode and extremum coincide", _word(r["d_ext"] < r["d_anti"], "the extremum is nearer", "the antipode is nearer"))
                         for r in res))
    return make_row("mat", f"Equal-load-sharing fibre bundle (Daniels) under quasi-static load, N = {N} fibres, the collapse (the maximum sustainable load) as the bundle's own event; "
                    "the intact fraction as a Bernoulli carrier (one fibre = one step, A1'); thresholds uniform (the source's) and Weibull with shapes 1, 2, 5 and 1/ln 2",
                    source=f"{TW} [12] (DESCR)",
                    Q="the bundle's collapse sits at the antipode of the intact-fraction carrier, half a turn from all-intact (half the fibres broken, the pole-start p = 1/2 cut of batch 09), "
                      "and not at the extremum of the load curve, for every threshold distribution",
                    ingredient="A3 / H-CUT (the own event at the phase antipode rather than at the extremum) read on the Bernoulli carrier of the intact fraction (theta = 2 arcsin sqrt(p), the "
                               "carrier batch 09 rows 3-4 read the pole-start cut on), D5 (the burst as the occasion), A1' (one fibre = one step)",
                    null="the extremum: Daniels' critical point, the maximum of x (1 - P(x)) (the domain's own location of the collapse)",
                    domain="Daniels 1945: the bundle's strength is max_x x (1 - P(x)), attained where 1 - P(x_c) = x_c p(x_c); for Weibull thresholds of shape k the broken fraction at the "
                           "critical load is 1 - exp(-1/k) and for uniform thresholds it is 1/2; Hemmer and Hansen 1992 for the burst exponent",
                    numbers=numbers,
                    tg=f"antipode {crr:.4f} vs null (Daniels' extremum, Weibull k = 2) {null:.4f}: {_agree(crr, null)}",
                    tn=f"Daniels' theorem gives {domain:.4f} for the Weibull k = 2 bundle: {_agree(crr, domain, TOL_N)}" + _word(rel(crr, domain) <= TOL_N, " (the domain has Q)", " (the domain puts the collapse elsewhere)"),
                    tc=f"the simulated collapse nearer the antipode than the extremum on every non-coincident distribution: {_hf(check)} (the extremum is nearer on {n_ext} of {len(noncoincide)})",
                    out=out,
                    reading=f"on the source's uniform bundle the antipode and the extremum are one point (Daniels' broken fraction {res[0]['Pc']:.4f}, the antipode {anti:.4f}; simulated {res[0]['sim']:.4f}), so the "
                            "source's bundle is the symmetric case H-CUT's own text excludes (nothing to test), and the coincidence is the flat distribution's: at the median the uniform hazard times the "
                            f"median threshold is exactly 1. Off the flat distribution the two part and the bundle's own event stays with the extremum (Weibull k = 2: simulated {w2['sim']:.4f} against "
                            f"Daniels {w2['Pc']:.4f} and the antipode {anti:.4f}; the extremum is nearer on {n_ext} of {len(noncoincide)} non-coincident distributions), because the collapse is the maximum of "
                            f"the load curve by the domain's definition of strength; the antipode is passed before the collapse at k = {before} (Daniels' broken fraction above 1/2) and after it at k = {after}, and the load carried at the "
                            f"antipode ({w2['load_anti']:.4f} at k = 2) is {_word(w2['load_anti'] < w2['load_c'], 'below', 'not below')} the critical load ({w2['load_c']:.4f}). The critical load and the burst exponent stay the bundle's, as the source said; the "
                            f"synthesis reading of the antipode is {out}",
                    weakness="the Bernoulli carrier is a segment of arc pi, not a rotor, so 'half a turn' is the pole-start reading of A3 (batch 09) and not A3 as CRR.md states it for cyclic carriers; "
                             "the collapse is an extremum by definition, so H-CUT's extremum sits at offset zero by construction and only the antipode's offset is informative; the simulated broken "
                             "fraction at maximum load carries the finite-size argmax noise (sd printed, of order N^-1/3 on the flat top of the uniform curve); citation by name and year only, not fetched (R10)")


# ---------------------------------------------------------------- 92 [13] TD(lambda): the bounded trace is first-visit Monte Carlo
N_STATES = 19
TRUE_V = np.linspace(-1, 1, N_STATES + 2)[1:-1]


def _episode(rng):
    s = N_STATES // 2 + 1; states = []; rewards = []
    while 0 < s < N_STATES + 1:
        s2 = s + (1 if rng.random() < 0.5 else -1); r = 1.0 if s2 == N_STATES + 1 else (-1.0 if s2 == 0 else 0.0)
        states.append(s); rewards.append(r); s = s2
    return states, rewards


def _td_offline(V, states, rewards, lam, alpha, replacing):
    """One episode's TD(lambda) increment with updates applied at the end (gamma = 1). Returns (dV, max trace)."""
    z = np.zeros(N_STATES + 2); dV = np.zeros(N_STATES + 2); zmax = 0.0
    for t, (s, r) in enumerate(zip(states, rewards)):
        s2 = states[t + 1] if t + 1 < len(states) else None
        z *= lam; z[s] = 1.0 if replacing else z[s] + 1.0; zmax = max(zmax, float(z.max()))
        delta = r + (V[s2] if s2 is not None else 0.0) - V[s]; dV += alpha * delta * z
    return dV, zmax


def _mc(V, states, rewards, alpha, first):
    """One episode's Monte Carlo increment (gamma = 1): first-visit or every-visit."""
    G = np.cumsum(rewards[::-1])[::-1]; dV = np.zeros(N_STATES + 2); seen = set()
    for t, s in enumerate(states):
        if first and s in seen:
            continue
        seen.add(s); dV[s] += alpha * (G[t] - V[s])
    return dV


def _rms_run(method, alpha, seed, lam=1.0, n_ep=10):
    """RMS value error after n_ep episodes; method in {acc_on, rep_on, acc_off, rep_off, mc_first, mc_every}. Returns (rms, max trace)."""
    rng = np.random.default_rng(seed); V = np.zeros(N_STATES + 2); zmax = 0.0
    for _ in range(n_ep):
        st, rw = _episode(rng)
        if method in ("acc_on", "rep_on"):
            z = np.zeros(N_STATES + 2); replacing = method == "rep_on"
            for t, (s, r) in enumerate(zip(st, rw)):
                s2 = st[t + 1] if t + 1 < len(st) else None
                z *= lam; z[s] = 1.0 if replacing else z[s] + 1.0; zmax = max(zmax, float(z.max()))
                delta = r + (V[s2] if s2 is not None else 0.0) - V[s]; V += alpha * delta * z
        elif method in ("acc_off", "rep_off"):
            dV, zm = _td_offline(V, st, rw, lam, alpha, method == "rep_off"); V += dV; zmax = max(zmax, zm)
        else:
            V += _mc(V, st, rw, alpha, method == "mc_first")
    with np.errstate(over="ignore", invalid="ignore"):
        err = np.sqrt(np.mean((V[1:-1] - TRUE_V) ** 2))
    return float(err) if np.isfinite(err) else float("inf"), zmax


def _fmt_rms(x):
    return f"{x:.3f}" if np.isfinite(x) and x < 1e3 else "diverged (> 1e3)"


def r2():
    alphas = (0.05, 0.1, 0.2, 0.4); n_runs = 50
    rng = np.random.default_rng(13); V0 = rng.normal(0, 0.3, N_STATES + 2); V0[0] = V0[-1] = 0.0
    st, rw = _episode(rng)
    d_rep, z_rep = _td_offline(V0, st, rw, 1.0, 0.1, True); d_acc, z_acc = _td_offline(V0, st, rw, 1.0, 0.1, False)
    m_first = _mc(V0, st, rw, 0.1, True); m_every = _mc(V0, st, rw, 0.1, False)
    e_rep_first = float(np.abs(d_rep - m_first).max()); e_acc_every = float(np.abs(d_acc - m_every).max()); e_rep_every = float(np.abs(d_rep - m_every).max())
    visits = max(st.count(s) for s in set(st))
    table = {}; zmax_all = {}
    for method in ("acc_on", "rep_on", "acc_off", "rep_off", "mc_first", "mc_every"):
        table[method] = {}; zmax_all[method] = 0.0
        for al in alphas:
            runs = [_rms_run(method, al, s) for s in range(n_runs)]
            table[method][al] = float(np.mean([r[0] for r in runs])); zmax_all[method] = max(zmax_all[method], max(r[1] for r in runs))
    best = {m: min(table[m], key=table[m].get) for m in table}
    crr = table["rep_off"][best["rep_off"]]; null = table["acc_off"][best["acc_off"]]; domain = table["mc_first"][best["rep_off"]]
    exact = max(e_rep_first, e_acc_every) < 1e-12
    bounded = zmax_all["rep_off"] <= 1.0 + 1e-12 and zmax_all["acc_off"] > 1.0
    across = all(abs(table["rep_off"][al] - table["mc_first"][al]) < 1e-9 for al in alphas) and all(abs(table["acc_off"][al] - table["mc_every"][al]) < 1e-9 or not np.isfinite(table["acc_off"][al]) for al in alphas)
    check = exact and bounded and across
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    def _tab(m):
        return ", ".join(f"alpha {al:g}: {_fmt_rms(table[m][al])}" for al in alphas)
    numbers = (f"one seeded episode (seed 13, {len(st)} steps, most-visited state seen {visits} times, V drawn N(0, 0.3)): lambda = 1 offline, max |replacing-trace increment - first-visit MC increment| = {e_rep_first:.1e}, "
               f"max |accumulating-trace increment - every-visit MC increment| = {e_acc_every:.1e}, max |replacing - every-visit| = {e_rep_every:.4f}; largest trace value in that episode: replacing {z_rep:.1f}, accumulating {z_acc:.1f} "
               f"(the visit count); RMS value error after 10 episodes, mean over {n_runs} seeded runs (the same episodes for every method), lambda = 1: "
               f"offline replacing: {_tab('rep_off')}; offline first-visit MC: {_tab('mc_first')}; offline accumulating: {_tab('acc_off')}; offline every-visit MC: {_tab('mc_every')}; "
               f"online (the source's estimator) replacing: {_tab('rep_on')}; online accumulating: {_tab('acc_on')}; largest trace over all 500 episodes: replacing {zmax_all['rep_off']:.1f}, accumulating {zmax_all['acc_off']:.1f}; "
               f"best alpha: replacing offline {best['rep_off']:g}, accumulating offline {best['acc_off']:g}")
    return make_row("rl", "TD(lambda) on the source's 19-state random walk (gamma = 1, start at the centre, +1 / -1 at the ends), lambda = 1, accumulating against replacing eligibility traces, "
                    "scored offline (increments applied at the end of the episode) beside the source's online estimator, 50 runs of 10 episodes on a common set of episodes",
                    source=f"{TW} [13] (DESCR)",
                    Q="the eligibility of a state read as A6's bounded content (never an accumulated count: z <= 1, the replacing trace) makes the lambda = 1 learner the first-visit Monte Carlo "
                      "estimator, unbiased and bounded in step, where the accumulated count (z = number of visits, the accumulating trace) makes it the every-visit estimator with an effective "
                      "step that grows with revisits",
                    ingredient="A6 (regeneration at bounded strength, never an accumulated count) with P3 (the trace's decay (gamma lambda)^k is the geometric age weight), D5 (occasion = one step of the walk)",
                    null="the accumulated count: the accumulating trace z <- z + 1 on every visit (Sutton 1988), the source's default",
                    domain="Singh and Sutton 1996: with gamma = 1 and offline updates, TD(1) with replacing traces is first-visit Monte Carlo and TD(1) with accumulating traces is every-visit Monte "
                           "Carlo; the replacing trace is bounded by 1 and the first-visit estimate is unbiased",
                    numbers=numbers,
                    tg=f"replacing-trace RMS {crr:.4f} (alpha {best['rep_off']:g}) vs null (accumulating, alpha {best['acc_off']:g}) {null:.4f}: {_agree(crr, null)}",
                    tn=f"first-visit Monte Carlo at the same alpha gives {domain:.4f}: {_agree(crr, domain, TOL_N)}" + _word(rel(crr, domain) <= TOL_N, " (the domain has Q: the bounded trace is the first-visit estimator)", ""),
                    tc=f"increment identities below 1e-12 (replacing = first-visit, accumulating = every-visit): {_word(exact, 'yes', 'no')}; replacing trace bounded by 1 and accumulating above 1: {_word(bounded, 'yes', 'no')}; "
                       f"the identities hold across all 50 runs at every alpha: {_word(across, 'yes', 'no')}: {_hf(check)}",
                    out=out,
                    reading=f"A6's clause does work on this carrier (T-G: {crr:.4f} against {null:.4f}; online, the source's estimator, the accumulated trace {_fmt_rms(table['acc_on'][0.2])} at alpha 0.2 against the "
                            f"bounded trace's {_fmt_rms(table['rep_on'][0.2])}), and what it produces is Singh and Sutton's theorem: on this walk every return within an episode is the terminal reward, so the "
                            "two traces differ only by the count of visits, which multiplies the step (the largest accumulated trace over 500 episodes was "
                            f"{zmax_all['acc_off']:.0f}), and the offline replacing learner is first-visit Monte Carlo to {e_rep_first:.1e}. 'Never an accumulated count' is the replacing trace, P3's "
                            "geometric weight is the trace decay the domain designed, and the domain proved the equivalence and the bound thirty years ago (and has since replaced both traces with "
                            "the dutch trace of true online TD(lambda), van Seijen and Sutton 2014, which neither reading names). The source's 'the count-vs-cap choice is the learner's' stands; the "
                            f"synthesis reading is {out}",
                    weakness="gamma = 1 is what makes the equivalence exact (Singh and Sutton's theorem is for the undiscounted case); the online numbers are the source's estimator and differ from the "
                             "offline ones by the within-episode updates; the RMS table is at the source's four alphas only; citations by name and year only, not fetched (R10)",
                    elegance="Count each place once per trip, however many times you pass through it. One rule with no knob, and it is the difference between a memory that stays bounded and one that runs away.",
                    child="Imagine walking back and forth along a corridor of doors and keeping a tally of which doors you passed, to decide which ones led you to the prize at the end. If you add a mark "
                          "every time you pass a door, the doors you dithered in front of get huge tallies and your guesses swing wildly. If you just mark each door once per walk, every walk counts "
                          "the same and the guesses settle down.")


# ---------------------------------------------------------------- 93 [14] Kovacs: what a single P3 kernel cannot do
E_ACT, T0 = 8.0, 1.0


def _deq(T):
    return (T - T0) * 0.1


def _kovacs(w, tau0, T1=0.8, t1=30.0, t_end=400.0, dt=0.01):
    """The source's linear multi-mode model under the Kovacs protocol (Euler at the source's step). Returns
    (T2, hump, deviation at the jump, mode deviations at the jump, tau at T2, history trace of delta)."""
    w = np.asarray(w, float); tau0 = np.asarray(tau0, float)

    def tau(T):
        return tau0 * np.exp(E_ACT * (1.0 / T - 1.0 / T0))

    def integrate(a, T, t_stop):
        n = int(round(t_stop / dt)); out = np.empty(n)
        for k in range(n):
            a = a + dt * (-(a - w * _deq(T)) / tau(T)); out[k] = a.sum()
        return a, out

    a = w * _deq(T0); a, hist = integrate(a, T1, t1)
    T2 = T0 + a.sum() / 0.1; d = a - w * _deq(T2); a2, path = integrate(a.copy(), T2, t_end)
    hump = float(np.max(np.abs(path - _deq(T2)))); start = float(abs(path[0] - _deq(T2)))
    return T2, hump, start, d, tau(T2), np.r_[0.0, hist]


def r3():
    w2, tau2 = (0.6, 0.4), (1.0, 20.0)
    T2, hump2, start2, d, tt, hist = _kovacs(w2, tau2)
    t_star = math.log(tt[1] / tt[0]) / (1.0 / tt[0] - 1.0 / tt[1]); hump_closed = abs(d[0]) * abs(math.exp(-t_star / tt[1]) - math.exp(-t_star / tt[0]))
    tau_p3 = float(np.dot(w2, tau2)); tau_p3_T2 = tau_p3 * math.exp(E_ACT * (1.0 / T2 - 1.0 / T0))
    _, hump_p3, _, _, _, _ = _kovacs((1.0,), (tau_p3,))
    _, hump_p3_fast, _, _, _, _ = _kovacs((1.0,), (tau2[0],))
    # the source's control: equilibrium at T2 held at T2
    a_eq = np.asarray(w2) * _deq(T2); tau_T2 = np.asarray(tau2) * np.exp(E_ACT * (1.0 / T2 - 1.0 / T0)); ctrl = []
    a = a_eq.copy()
    for _ in range(int(round(400.0 / 0.01))):
        a = a + 0.01 * (-(a - a_eq) / tau_T2); ctrl.append(a.sum())
    ctrl_dev = float(np.max(np.abs(np.asarray(ctrl) - _deq(T2))))
    grid = []
    for t1 in (5.0, 30.0, 100.0):
        T2k, hk, sk, dk, _, hk_hist = _kovacs(w2, tau2, t1=t1); arc = arc_length(hk_hist); chord = abs(hk_hist[-1] - hk_hist[0])
        _, hp, _, _, _, _ = _kovacs((1.0,), (tau_p3,), t1=t1)
        grid.append((t1, T2k, hk, sk, abs(dk[0]), arc, chord, hp))
    crr = hump_p3; null = hump2; domain = hump_closed
    check = rel(crr, domain) <= TOL_N
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    humps = [g[2] for g in grid]; arcs = [g[5] for g in grid]; p3_max = max(g[7] for g in grid); dev_max = max(g[3] for g in grid)
    mono = (np.argsort(humps) == np.argsort(arcs)).all()
    numbers = (f"the source's protocol reproduced: quench T0 = {T0:g} -> T1 = 0.8 held 30, jump to T2 = {T2:.4f} where delta = delta_eq(T2) (deviation at the jump {start2:.1e}); two-mode kernel "
               f"(w = {w2}, tau0 = {tau2}; at T2 tau = {tt[0]:.3f}, {tt[1]:.3f}): Kovacs hump {hump2:.6f}, closed form |d| |e^-t*/tau2 - e^-t*/tau1| = {hump_closed:.6f} at t* = {t_star:.3f} with the mode "
               f"deviations at the jump d = ({d[0]:+.6f}, {d[1]:+.6f}) (equal and opposite: the volume is at equilibrium, the modes are not); the source's control (equilibrium at T2 held at T2): "
               f"{ctrl_dev:.1e}; A6/P3 kernel, one exponential with tau0 = {tau_p3:.1f} (the w-weighted mean of the two tau0; {tau_p3_T2:.2f} at T2): hump {hump_p3:.1e}; at tau = {tau2[0]:g}: {hump_p3_fast:.1e}; "
               "the same endpoint, other histories (t1 = 5, 30, 100 at T1 = 0.8): " +
               "; ".join(f"t1 = {g[0]:g}: T2 = {g[1]:.4f}, deviation at the jump {g[3]:.1e}, |d| = {g[4]:.6f}, hump {g[2]:.6f} (P3 kernel {g[7]:.1e}); arc of delta over the history {g[5]:.6f}, chord {g[6]:.6f}"
                         for g in grid) +
               f"; the hump ordered as the arc: {_word(mono, 'yes', 'no')}")
    return make_row("mat", "The source's two-mode linear glass model (delta = a1 + a2, da_i/dt = -(a_i - w_i delta_eq(T))/tau_i(T), Arrhenius tau_i with E = 8) under the Kovacs protocol, Euler at "
                    "dt = 0.01, against the same protocol on the kernel A6 with P3 gives: one exponential (one history constraint) with tau0 the w-weighted mean of the two tau0",
                    source=f"{TW} [14] (DESCR)",
                    Q="a glass whose settled thermal history acts on its volume through A6 with P3 (a bounded geometric age weight under one mean-age constraint: exponential smoothing of "
                      "delta_eq(T(t)), the one-mode relaxation) shows no Kovacs memory effect: at delta = delta_eq(T2) it stays there, whatever the history",
                    ingredient="A6 (the next state seeded from the settled past by a bounded weighted mean, one MaxEnt history constraint) with P3 (geometric age weights, mean age fixed), D5 [M] "
                               "(occasion = one time step of the thermal history); on the 1-D volume carrier the Frechet mean is the weighted mean",
                    null="the domain's kernel: the two-mode Prony series (a mixture of two exponentials, two relaxation times), the source's model",
                    domain="Kovacs 1963 (the memory experiment); multi-mode linear relaxation (TNM / KAHR): the volume after the jump is sum_i d_i e^{-t/tau_i} with d_1 = -d_2 at the jump, a hump of "
                           "height |d| |e^{-t*/tau2} - e^{-t*/tau1}| that vanishes identically when the relaxation function is a single exponential",
                    numbers=numbers,
                    tg=f"hump under the A6/P3 kernel {crr:.1e} vs null (two-mode kernel) {null:.6f}: {_agree(crr, null)}",
                    tn=f"the multi-mode theorem gives {domain:.6f} for the glass: {_agree(crr, domain, TOL_N)}" + _word(rel(crr, domain) <= TOL_N, " (the domain has Q)", " (the domain's glass remembers; Q says it does not)"),
                    tc=f"Q's hump ({crr:.1e}) within 1 % of the domain's ({domain:.6f}): {_hf(check)}",
                    out=out,
                    reading=f"read as the memory rule for the settled thermal history, A6 with P3 is the one-mode model, and the one-mode model is the one kernel that has no Kovacs effect (hump at most {p3_max:.1e} at "
                            f"every t1 against the two-mode {null:.6f}, closed form {domain:.6f}): the effect is the signature of at least two relaxation times, a kernel that is a mixture of geometric "
                            f"weights and not a single MaxEnt kernel under one constraint. The same endpoint (deviation at the jump at most {dev_max:.1e} in every history) gives humps from "
                            f"{min(humps):.6f} to {max(humps):.6f}, so the source's 'the path matters' stands, and the arc of delta over the history does not order the humps either "
                            f"({_word(mono, 'it does', 'ordered as the arc: no')}): what fixes the hump is the mode split |d|, the hidden coordinate the source named. This is the A6/P3 kernel of synthesis row 8, batch 12 row 2 "
                            "and batch 17 row 1 met from the other side: there the caution was that any exponential kernel produces the effect claimed; here a domain has an effect that no single "
                            f"exponential kernel can produce, and the CRR-specific content (one constraint, bounded strength) is exactly what excludes it. The synthesis reading is {out}",
                    weakness="the glass has no own events (O3), so 'occasion = one time step' is a modelling step and A6's Frechet mean is exponential smoothing on a 1-D carrier; a P3 kernel with a second "
                             "constraint would be a different (non-mixture) kernel and is not CRR.md's; the two-mode model is the source's, linear and with one Arrhenius energy, not a TNM nonlinearity; "
                             "the escape 'a system that re-counts its past stops cutting' does not apply (the glass accumulates nothing, it remembers a split); citation by name and year only, not fetched (R10)",
                    elegance="A memory that fades at one speed cannot tell two stories at once. The glass looks settled, but a fast part has overshot and a slow part is still catching up, and only a memory with two speeds can hold that.",
                    child="Squeeze a sponge and let it go: it springs back. Now imagine a sponge with a quick part and a slow part. Warm it so the quick part has already sprung back but the slow part is "
                          "still moving, and the sponge is exactly its normal size for a moment, yet it keeps changing, bulging out and coming back. A sponge with only one speed could never do that.")


# ---------------------------------------------------------------- 94 [15] Elo: the K-factor in the game's own unit
SCALE = 400.0 / math.log(10.0)


def _Kg(v):
    return (v / 2.0) * (math.sqrt(v * v + 4.0) - v)


def _elo_source(K, v, rng, T=20000):
    """The source's estimator: a fresh skill path per call (shared generator), fixed opponent at 0."""
    skill = 0.0; R = 0.0; ll = 0.0; info = 0.0
    for _ in range(T):
        skill += v * 30.0 * rng.standard_normal(); p = 1.0 / (1.0 + math.exp(-skill / SCALE)); S = 1.0 if rng.random() < p else 0.0
        E = 1.0 / (1.0 + math.exp(-R / SCALE)); ll -= S * math.log(max(E, 1e-9)) + (1.0 - S) * math.log(max(1.0 - E, 1e-9)); R += K * (S - E); info += p * (1.0 - p)
    return ll / T, info / T


def _elo_fixed_crn(v, Ks, T=20000, seed=15):
    """The source's model on one skill path for every K (common random numbers)."""
    rng = np.random.default_rng(seed); Ks = np.asarray(Ks, float)
    skill = np.cumsum(v * 30.0 * rng.standard_normal(T)); p = 1.0 / (1.0 + np.exp(-skill / SCALE)); S = (rng.random(T) < p).astype(float)
    R = np.zeros(len(Ks)); ll = np.zeros(len(Ks))
    for t in range(T):
        E = 1.0 / (1.0 + np.exp(-R / SCALE)); ll -= S[t] * np.log(np.maximum(E, 1e-9)) + (1.0 - S[t]) * np.log(np.maximum(1.0 - E, 1e-9)); R += Ks * (S[t] - E)
    return ll / T, float(np.mean(p * (1.0 - p))), float(np.abs(skill).mean())


def _elo_pool(sw, Ks, pool_sd, T=50000, seed=0):
    """Skill random walk (sw rating points per game) against opponents drawn around the player's skill (pool_sd), common random numbers."""
    rng = np.random.default_rng(seed); Ks = np.asarray(Ks, float)
    skill = np.cumsum(sw * rng.standard_normal(T)); opp = pool_sd * rng.standard_normal(T); u = rng.random(T)
    p = 1.0 / (1.0 + np.exp(opp / SCALE)); S = (u < p).astype(float); R = np.zeros(len(Ks)); ll = np.zeros(len(Ks))
    for t in range(T):
        E = 1.0 / (1.0 + np.exp(-(R - (skill[t] + opp[t])) / SCALE)); ll -= S[t] * np.log(np.maximum(E, 1e-12)) + (1.0 - S[t]) * np.log(np.maximum(1.0 - E, 1e-12)); R += Ks * (S[t] - E)
    return ll / T, float(np.mean(p * (1.0 - p)))


def r4():
    Ks = (2, 4, 8, 16, 32, 64, 128, 256); vs = (0.03, 0.1, 0.3)
    rng = np.random.default_rng(15); src = {}
    for v in vs:
        res = {K: _elo_source(K, v, rng) for K in Ks}; best = min(res, key=lambda K: res[K][0])
        src[v] = (best, min(r[1] for r in res.values()), max(r[1] for r in res.values()), min(r[0] for r in res.values()), max(r[0] for r in res.values()))
    crn = {}
    for v in vs:
        ll, info, ab = _elo_fixed_crn(v, Ks); i = int(np.argmin(ll)); sw = v * 30.0
        crn[v] = (Ks[i], info, ab, _Kg(sw * math.sqrt(info) / SCALE) * SCALE / info, ll)
    step = 2.0 ** 0.25; Kgrid = 2.0 ** (np.arange(0, 33) / 4.0); cells = []
    for pool_sd in (200.0, 600.0):
        for sw in (3.5, 10.0, 35.0):
            ll, info = _elo_pool(sw, Kgrid, pool_sd); i = int(np.argmin(ll))
            x = np.log(Kgrid[i - 1:i + 2]); y = ll[i - 1:i + 2]; a, b, _ = np.polyfit(x, y, 2); kfit = math.exp(-b / (2.0 * a))
            sig = SCALE / math.sqrt(info); vF = sw / sig; kpred = _Kg(vF) * SCALE / info; knull = _Kg(sw)
            cells.append(dict(pool=pool_sd, sw=sw, info=info, sig=sig, vF=vF, kpred=kpred, knull=knull, kgrid=float(Kgrid[i]), kfit=kfit, ratio=kfit / kpred, inv=kfit * info / SCALE, Kg=_Kg(vF)))
    c = cells[1]; crr = c["kpred"]; null = c["knull"]; domain = _Kg(c["sw"] * math.sqrt(c["info"]) / SCALE) * SCALE / c["info"]
    within = [abs(math.log(x["ratio"])) <= math.log(step) for x in cells]; check = all(within)
    ratios_txt = ", ".join(f"{x['ratio']:.3f}" for x in cells); max_steps = max(abs(math.log(x["ratio"])) for x in cells) / math.log(step)
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    src_mono = src[0.03][0] <= src[0.1][0] <= src[0.3][0]; crn_mono = crn[0.03][0] <= crn[0.1][0] <= crn[0.3][0]
    src_range = src[0.3][4] - src[0.3][3]; crn_range = float(crn[0.3][4].max() - crn[0.3][4].min())
    numbers = ("the source's estimator reproduced (seed 15, T = 20000 games, fixed opponent at 0, a fresh skill path per (K, v) call): " +
               "; ".join(f"v = {v:g}: best K = {src[v][0]}, <p(1-p)> across the eight K calls {src[v][1]:.3f}-{src[v][2]:.3f}, log-loss {src[v][3]:.4f}-{src[v][4]:.4f}" for v in vs) +
               f"; best K non-decreasing in v: {src_mono}; the same model on one skill path per v for all K (common random numbers, seed 15): " +
               "; ".join(f"v = {v:g}: best K = {crn[v][0]}, <p(1-p)> = {crn[v][1]:.3f}, mean |skill| {crn[v][2]:.0f} points, K predicted from the Fisher unit {crn[v][3]:.1f}, log-loss over K {np.round(crn[v][4], 4).tolist()}" for v in vs) +
               f"; non-decreasing: {crn_mono}; the pool model (opponents drawn at the player's skill + N(0, pool) points, T = 50000, K on a 2^(1/4) grid 1-256, optimum by a parabola in ln K around the grid minimum): " +
               "; ".join(f"pool {x['pool']:g}, s_w = {x['sw']:g}: <E(1-E)> = {x['info']:.4f}, sigma_game = scale/sqrt<E(1-E)> = {x['sig']:.1f} points, v_F = {x['vF']:.4f}, K predicted {x['kpred']:.2f} (null, rating point as the unit: {x['knull']:.3f}), "
                         f"best K on the grid {x['kgrid']:.2f}, fitted {x['kfit']:.2f}, ratio {x['ratio']:.3f}; K <E(1-E)>/scale = {x['inv']:.4f} against K(v_F) = {x['Kg']:.4f}" for x in cells) +
               f"; cells within one grid step (factor {step:.3f}) of the prediction: {sum(within)} of {len(cells)}")
    return make_row("games", "Elo ratings (R <- R + K (S - E), E logistic on the 400/ln 10 scale) of a player whose skill is a random walk, the source's fixed-opponent model reproduced and rerun on "
                    "common random numbers, and a pool model (opponents around the player's skill) at two pool widths and three skill volatilities",
                    source=f"{TW} [15] (DESCR)",
                    Q="the best K-factor is the Kalman gain at the skill's Fisher speed, in the game's own unit: sigma_game = scale/sqrt<E(1-E)> rating points (one game's resolvable step), v_F = "
                      "s_w/sigma_game, K* = K(v_F) sigma_game^2/scale, so K* <E(1-E)>/scale = K(v_F) is invariant to the rating convention, and K* in rating points grows as the pool's outcomes become "
                      "predictable (<E(1-E)> -> 0)",
                    ingredient="A1'/D1 (the unit is the system's own resolvable step, here the rating change one game resolves, not the rating point) integrated with P4 (the Riccati gain, which CRR.md says is not "
                               "CRR's) and A6/P3 read as the fixed gain (batch 15 row 5)",
                    null="the rating point as the unit: K(v) evaluated with s_w in rating points (the source's reading, K on the rating scale with no unit)",
                    domain="the extended Kalman filter on the Bradley-Terry model (Glickman 1999, Glicko; Ingram 2021, Elo as a one-step Kalman filter): linearising E about the rating gives an observation of "
                           "the skill with variance scale^2/(E(1-E)), so the steady-state gain in rating points is K(v_F) scale/<E(1-E)>",
                    numbers=numbers,
                    tg=f"K* in the game's unit {crr:.2f} vs null (rating point as the unit) {null:.3f} at pool 200, s_w = 10: {_agree(crr, null)}",
                    tn=f"the extended-Kalman gain gives {domain:.2f}: {_agree(crr, domain, TOL_N)}" + _word(rel(crr, domain) <= TOL_N, " (the domain has Q)", ""),
                    tc=f"fitted optimum within one grid step of the prediction in every cell: {_hf(check)} ({sum(within)} of {len(cells)}; ratios {ratios_txt})",
                    out=out,
                    reading=f"the unit does work (T-G: {crr:.2f} against {null:.3f}), and what it produces is the domain's own filter: in every cell the log-loss optimum sits within {max_steps:.2f} "
                            f"grid steps of K(v_F) scale/<E(1-E)> (ratios {min(x['ratio'] for x in cells):.3f}-{max(x['ratio'] for x in cells):.3f}), and the same skill volatility wants a larger K in the wider pool "
                            f"({cells[1]['kfit']:.1f} at pool 200 against {cells[4]['kfit']:.1f} at pool 600 for s_w = 10) because one game resolves less there (sigma_game {cells[1]['sig']:.0f} against {cells[4]['sig']:.0f} points). "
                            f"The source's grid (best K = {src[0.03][0]}, {src[0.1][0]}, {src[0.3][0]}) compared each K on a different skill path, and at v = 0.3 the loss varies {_word(src_range > crn_range, 'more', 'less')} between its paths (range {src_range:.3f}, with "
                            f"<p(1-p)> from {src[0.3][1]:.3f} to {src[0.3][2]:.3f}) than between K values on one path (range {crn_range:.3f}); on one path per v the optimum is {crn[0.03][0]}, {crn[0.1][0]}, {crn[0.3][0]} against {crn[0.03][3]:.1f}, {crn[0.1][3]:.1f}, {crn[0.3][3]:.1f} "
                            f"predicted, still non-decreasing ({crn_mono}), and the rise is the fixed opponent's: as the skill wanders away from 0 (mean |skill| {crn[0.03][2]:.0f}, {crn[0.1][2]:.0f}, {crn[0.3][2]:.0f} points) the games saturate "
                            f"(<p(1-p)> {crn[0.03][1]:.3f}, {crn[0.1][1]:.3f}, {crn[0.3][1]:.3f}) and the unit grows. The source's ordering survives on one path; its values 128 and 256 were the paths' differences "
                            f"(recorded here, the pinned output not edited); the synthesis reading is {out}, the Rescorla-Wagner reading of batch 15 row 5 with the unit made explicit by a logistic observation",
                    weakness="the prediction is a linearised, fixed-gain approximation (the exact optimum for a logistic observation is not a fixed K), so the check is within one grid step and not within 1 %; "
                             "the pool width and the skill volatility are registered grids, not measured; a real pool's <E(1-E)> is an estimate from the rating differences; citations by name and year only, not "
                             "fetched (R10)",
                    elegance="A game you were sure about teaches almost nothing, so a rating must move further per surprise when the games stop being surprising. The step size is not a number to pick; it is how much one game can tell you.",
                    child="If you always play people much weaker than you and win, one more win says almost nothing about how good you are, so your score should hardly move. If you play people about "
                          "as good as you, every game is real news, and your score can move a lot. The best amount to move after a game is how much that game could actually tell you.")


# ---------------------------------------------------------------- 95 [16] cricket chirps: the arc is the stroke count times the stroke
def _song(T, gamma, fs=2000, n_p0=4, amp_noise=0.03, seed=1):
    """Pulse-train song at drifting temperature: chirp rate r_c = (T - 4)/10 (the source's Dolbear law), chirp duration a quarter
    period, pulse (wing-stroke) rate r_p proportional to r_c^gamma (gamma = 1: pulses per chirp conserved), each stroke a half-sine
    of height A (3 % jitter per chirp). Returns (trace, chirp onsets, pulses per chirp)."""
    rng = np.random.default_rng(seed); segs = []; onsets = []; counts = []; idx = 0; rc0 = (20.0 - 4.0) / 10.0
    for Tk in T:
        rc = (Tk - 4.0) / 10.0; period = 1.0 / rc; rp = 4.0 * n_p0 * rc0 * (rc / rc0) ** gamma; dur = period / 4.0
        n_pulse = max(1, int(round(rp * dur))); A = 1.0 * (1.0 + amp_noise * rng.standard_normal())
        ns = int(round(period * fs)); seg = np.zeros(ns); pp = int(round(fs / rp)); half = max(1, pp // 2)
        for j in range(n_pulse):
            a = j * pp
            if a + half < ns:
                seg[a:a + half] = A * np.sin(np.pi * np.arange(half) / half)
        onsets.append(idx); segs.append(seg); idx += ns; counts.append(n_pulse)
    return np.concatenate(segs), np.asarray(onsets), np.asarray(counts)


def r5():
    rng = np.random.default_rng(16); n = 300; T = 20 + 4 * np.cumsum(0.1 * rng.standard_normal(n)); T = np.clip(T, 12, 30)
    rate = (T - 4) / 10.0; intervals = 1.0 / rate; chirp_arc = 1.0 * (1 + 0.03 * rng.standard_normal(n))
    src_arc, src_clock = cv(chirp_arc), cv(intervals)
    fs = 2000; res = {}
    for gamma in (1.0, 0.5, 1.5):
        x, ev, counts = _song(T, gamma, fs=fs)
        r = regularity(x, ev, dt=1.0 / fs, segment_end="exclusive")
        lab = _word(abs(r["cv_arc"] - r["cv_clock"]) < 0.01, "tie (below the 0.01 reading margin)", _word(r["cv_arc"] < r["cv_clock"], "arc-regular", "clock-regular"))
        ci_lab = _word(r["ci95"][1] < 0, "arc-regular", _word(r["ci95"][0] > 0, "clock-regular", "undecided"))
        amp_lab = _word(r["ci95_amp"][0] > 0, "the amplitude control is the more regular", _word(r["ci95_amp"][1] < 0, "the arc beats the amplitude control", "tie with the amplitude control (CI includes 0)"))
        res[gamma] = dict(r=r, counts=counts, lab=lab, ci_lab=ci_lab, amp_lab=amp_lab, cv_count=cv(counts))
    g1 = res[1.0]["r"]; crr = g1["cv_arc"]; null = g1["cv_amp"]
    # T-N: with the pulse count conserved, arc = count x stroke, so the domain's CV(arc) is the stroke's CV (Walker: pulses per chirp conserved)
    x1, ev1, c1 = _song(T, 1.0, fs=fs)
    strokes = np.array([np.ptp(x1[a:b]) for a, b in zip(ev1[:-1], ev1[1:])]); domain = cv(strokes)
    check = (res[1.0]["r"]["ci95_amp"][0] <= 0 <= res[1.0]["r"]["ci95_amp"][1]) and res[1.0]["r"]["ci95"][1] < 0
    amp_wins_both = all(res[g]["r"]["ci95_amp"][0] > 0 for g in (0.5, 1.5)); arc_rises = all(res[g]["r"]["cv_arc"] > res[1.0]["r"]["cv_arc"] for g in (0.5, 1.5))
    flips = res[1.5]["ci_lab"] != res[1.0]["ci_lab"]
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    def _cell(g):
        d = res[g]; r = d["r"]
        return (f"gamma = {g:g} (pulses per chirp {d['counts'].min()}-{d['counts'].max()}, CV {d['cv_count']:.4f}): {r['n']} occasions, CV(arc) = {r['cv_arc']:.4f}, CV(clock) = {r['cv_clock']:.4f}, "
                f"CV(amplitude) = {r['cv_amp']:.4f}, C_mean = {r['C_mean']:.3f}, CI95 of CV(arc) - CV(clock) [{r['ci95'][0]:.4f}, {r['ci95'][1]:.4f}], of CV(arc) - CV(amplitude) "
                f"[{r['ci95_amp'][0]:.1e}, {r['ci95_amp'][1]:.1e}]: {d['lab']} (by the CI {d['ci_lab']}); {d['amp_lab']}")
    numbers = (f"the source's model reproduced (seed 16, 300 chirps, temperature {T.min():.1f}-{T.max():.1f}): chirp-interval CV {src_clock:.4f}, chirp-arc CV {src_arc:.4f}; the pulse-train song "
               f"({fs} samples/s, the chirp onset as the cut, exclusive segmentation): " + "; ".join(_cell(g) for g in (1.0, 0.5, 1.5)) +
               f"; at gamma = 1 the stroke height's CV across chirps is {domain:.4f}")
    return make_row("acoust", "Cricket chirps under the source's drifting temperature (a clipped random walk, 300 chirps) built as a pulse train: chirp rate by Dolbear's law (T - 4)/10, a chirp of "
                    "wing strokes at a pulse rate proportional to the chirp rate to the power gamma (gamma = 1: pulses per chirp conserved), each stroke one half-sine, the chirp onset as the cut",
                    source=f"{TW} [16] (DESCR)",
                    Q="the song is in H-L5's arc-regular class beyond the amplitude control only through the pulse count: in the cricket's own unit (A1': one wing stroke = one step) the arc of a chirp "
                      "cycle is the number of strokes times the stroke, so when the pulse rate and the chirp rate share one temperature law (gamma = 1, the domain's conserved pulses per chirp) the arc "
                      "is the amplitude control times a constant, CV(arc) = CV(amplitude) identically, and when they do not the amplitude control is the more regular quantity",
                    ingredient="H-L5 (the class claim, with its control (i), the excursion amplitude), A1' (natural time: one wing stroke = one step, the pulse count as the chirp's length in the cricket's unit), "
                               "D5 (occasion = chirp to chirp), A3 read as 'the onset is the cut' (exclusive segmentation), D2 with the identity metric on the sound envelope",
                    null="H-L5's control (i): the peak-to-peak amplitude of the occasion, one wing stroke",
                    domain="Dolbear 1897: the chirp rate is linear in temperature; Walker 1962: the pulse rate and the chirp rate of Gryllus rise linearly with temperature together, so the pulses per chirp "
                           "are conserved and the chirp is the same motor pattern run faster (temperature coupling, Doherty 1985)",
                    numbers=numbers,
                    tg=f"CV(arc) {crr:.4f} vs null (CV of the amplitude control) {null:.4f} at gamma = 1: {_agree(crr, null)}",
                    tn=f"the conserved pulse count gives CV(arc) = CV(stroke) = {domain:.4f}: {_agree(crr, domain, TOL_N)}" + _word(rel(crr, domain) <= TOL_N, " (the domain has Q: the chirp is the same pattern run faster)", ""),
                    tc=f"at gamma = 1 the amplitude CI includes 0 and the clock CI lies below 0: {_hf(check)}; at gamma = 0.5 {res[0.5]['amp_lab']} and the class is {res[0.5]['ci_lab']}; at gamma = 1.5 {res[1.5]['amp_lab']} and the class is {res[1.5]['ci_lab']}",
                    out=out,
                    reading=f"geometry, as batch 18 read the laser and the geyser: a chirp is {res[1.0]['counts'].min()} strokes of height A, its arc is {res[1.0]['counts'].min()} x 2A, and the amplitude control is 2A, so at gamma = 1 the two CVs are one number "
                            f"({crr:.4f}; the paired CI of the difference [{g1['ci95_amp'][0]:.1e}, {g1['ci95_amp'][1]:.1e}] cannot exclude 0) and H-L5 as CRR.md states it, beyond control (i), reads REDUNDANT-IG. "
                            f"The class against the clock (CV {g1['cv_clock']:.4f}, CI [{g1['ci95'][0]:.4f}, {g1['ci95'][1]:.4f}]) is Dolbear's law read backwards: the clock carries the temperature and the pattern does not. "
                            f"When the two temperature laws part (gamma = 0.5, 1.5) the pulse count varies ({res[0.5]['counts'].min()}-{res[0.5]['counts'].max()}, {res[1.5]['counts'].min()}-{res[1.5]['counts'].max()}), the arc's CV {_word(arc_rises, 'rises', 'moves')} to "
                            f"{res[0.5]['r']['cv_arc']:.4f} and {res[1.5]['r']['cv_arc']:.4f}, the amplitude control {_word(amp_wins_both, 'wins both', 'does not win both')}, and at gamma = 1.5 the class {_word(flips, 'flips to', 'stays')} {res[1.5]['ci_lab']}: the class is the ratio of the two "
                            "temperature coefficients, a quantity Walker measured, not a prediction. The source's 'a thermometer made of arc-regularity' stands as Dolbear's; the synthesis reading is "
                            f"{out}",
                    weakness="the pulse count is an integer by construction (the cricket's natural time), so the count's CV is quantised at 300 chirps; the sound envelope has no statistical metric (the identity "
                             "metric is the source's stand-in) and the half-sine stroke is a cartoon of a wing stroke; the gamma grid is registered, not measured, and Walker's linear laws are cited by name and "
                             "year only, not fetched (R10); no H-CUT proposition was formed, since the onset is placed by construction",
                    elegance="Warm the cricket and it sings the same song faster; count the strokes and the song never changes, count the seconds and you have a thermometer. Two ways of counting, one of them the cricket's own.",
                    child="A cricket's chirp is a few flicks of its wings, always the same flicks. On a warm night it chirps quickly and on a cool night slowly, but each chirp still has the same flicks in it. "
                          "So if you count the flicks you learn nothing about the weather, and if you count the chirps in a minute you can tell the temperature. Dolbear worked that out in 1897.")


def main():
    return run_batch("Synthesis batch 19: rows 91-95 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
