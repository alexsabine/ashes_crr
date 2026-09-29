"""PRED70 batch P10: social systems and networks (Predictions70/DECLARATION.md; prompt-log entry 234). Rows P10-1..P10-5 of
Predictions70/declared.py (pushed in commit 8397478 before any model existed). [1] DeGroot averaging on a ring with
A6-remembered neighbours' opinions; [2] a Hawkes process against the A6 geometric kernel on occasions; [3] Schelling
segregation with A6-remembered neighbourhood composition; [4] Nagel-Schreckenberg traffic with braking on an A6-remembered
headway; [5] Daley-Kendall rumours with spreaders stopping on A6-remembered encounters. Literature named by name and year
only (R10): DeGroot 1974; Hawkes 1971; Ogata 1981; Schelling 1971; Nagel and Schreckenberg 1992; Daley and Kendall 1965.
Deterministic; about 60 s."""
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from declared import P  # noqa: E402

D = {p[0]: p for p in P}
QGRID = (0.25, 0.5, 0.75)
Q0 = 0.5


def _w(cond, yes, no):
    return yes if cond else no


def _decl(pid):
    _, _, cls, system, ingredient, Q, null, H0, forecast = D[pid]
    return cls, system, ingredient, Q, null, H0, f"PRED70 {pid} (declared at 8397478; forecast {forecast})"


def _qh(check):
    return _w(check is None, "-> not computable", _w(check, "-> Q holds", "-> Q fails"))


# ---------------------------------------------------------------- [1] DeGroot on a ring with remembered neighbours
DG_N = 50


def _ring(s):
    W = np.diag(s).astype(float)
    for i in range(DG_N):
        W[i, (i - 1) % DG_N] += (1 - s[i]) / 2; W[i, (i + 1) % DG_N] += (1 - s[i]) / 2
    return W


def _degroot(s, x0, q):
    """x_{t+1} = S x_t + A m_t, m_t = (1 - q) x_t + q m_{t-1} (every agent sees neighbour j's A6-remembered opinion m_j;
    own opinion instantaneous; m_{-1} = x_0). State (x_t, m_{t-1})."""
    W = _ring(s); S = np.diag(np.diag(W)); A = W - S; I = np.eye(DG_N)
    M = np.block([[S + (1 - q) * A, q * A], [(1 - q) * I, q * I]])
    ev = np.linalg.eigvals(M); ev = ev[np.argsort(-np.abs(ev))]
    tau = -1.0 / math.log(abs(ev[1]))
    evl, vl = np.linalg.eig(W.T); pi = np.real(vl[:, int(np.argmin(np.abs(evl - 1)))]); pi = pi / pi.sum()
    kap = q / (1 - q); ell = np.concatenate([pi, kap * (pi @ A)])
    left_ok = float(np.abs(ell @ M - ell).max()) < 1e-12
    z0 = np.concatenate([x0, x0]); c_th = float(ell @ z0 / ell.sum())
    z = z0.copy(); steps = 0
    while np.ptp(z[:DG_N]) > 1e-12 and steps < 200000:
        z = M @ z; steps += 1
    return dict(c=c_th, c_sim=float(z[:DG_N].mean()), tau=tau, steps=steps, pix=float(pi @ x0), left_ok=left_ok)


def r1():
    cls, system, ing, Q, nul, H0, src = _decl("P10-1")
    rng = np.random.default_rng(0); s = 0.2 + 0.4 * rng.random(DG_N); x0 = rng.random(DG_N)
    res = {q: _degroot(s, x0, q) for q in (0.0,) + QGRID}
    hom = {q: _degroot(np.full(DG_N, 1 / 3), x0, q) for q in (0.0, Q0)}
    crr, null = res[Q0]["tau"], res[0.0]["tau"]
    shift = rel(res[Q0]["c"], res[0.0]["c"]); slower = crr / null - 1.0
    unchanged = shift <= TOL_N; check = unchanged and slower > TOL_G
    out = outcome(crr=crr, null=null, domain=None, check=check)
    grid = "; ".join(f"q = {q}: consensus {res[q]['c']:.6f}, tau {res[q]['tau']:.2f}" for q in QGRID)
    sims_ok = all(abs(res[q]["c"] - res[q]["c_sim"]) < 1e-9 and res[q]["left_ok"] for q in (0.0,) + QGRID)
    return make_row(cls, f"{system} (computed as: row-stochastic ring, self-weight s_i = 0.2 + 0.4 u_i, (1 - s_i)/2 to each neighbour, u and x_0 uniform, seed 0; memory initialised at x_0; convergence time tau = -1/ln|lambda_2| of the iteration)",
                    source=src, Q=Q, ingredient=f"{ing}: each neighbour's opinion enters as m_j = (1 - q) x_j + q m_j(previous), q = 0.5 per round",
                    null=nul, domain=H0,
                    numbers=f"consensus: A6 {res[Q0]['c']:.10f}, instantaneous {res[0.0]['c']:.10f}, relative shift {shift:.2e}; DeGroot's eigenvector-weighted mean pi.x_0 = {res[0.0]['pix']:.10f}; "
                            f"convergence time: A6 {crr:.2f} rounds, instantaneous {null:.2f} (slower by {100 * slower:.1f} %; rounds to a spread below 1e-12: {res[Q0]['steps']} vs {res[0.0]['steps']}); "
                            f"homogeneous ring (s = 1/3, sensitivity): consensus shift {rel(hom[Q0]['c'], hom[0.0]['c']):.2e}, tau {hom[Q0]['tau']:.2f} vs {hom[0.0]['tau']:.2f}; q-grid (sensitivity only): {grid}; "
                            f"conserved-quantity consensus equals the simulated one and is a left eigenvector: {_w(sims_ok, 'yes', 'NO')}",
                    tg=f"convergence time {crr:.2f} vs null {null:.2f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="DeGroot's theorem gives the memoryless consensus (checked in T-C); no rate is cited for the memory variant",
                    tc=f"consensus unchanged within 1 % (shift {100 * shift:.3f} %: {_w(unchanged, 'yes', 'no')}) and convergence slower by more than 1 % ({100 * slower:.1f} %: {_w(slower > TOL_G, 'yes', 'no')}): {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=f"with remembered neighbours the conserved quantity is pi.x + (q/(1 - q)) (pi A).m, not pi.x, so the consensus moves by {shift:.2e} (relative) on this heterogeneous ring ({_w(unchanged, 'below', 'above')} the 1 % resolution) and by {rel(hom[Q0]['c'], hom[0.0]['c']):.2e} on the homogeneous one, where pi A is proportional to pi; averaging over remembered opinions {_w(slower > 0, 'slows', 'speeds')} convergence by {100 * slower:.1f} %; consensus with memory or shift registers is an existing literature, mostly on acceleration with extrapolating weights (not checked for this averaging form)",
                    weakness="'unchanged' is read at the declaration's 1 % resolution; the consensus does move (exactly) whenever self-weights differ, and a more heterogeneous ring or other initial opinions could move it past 1 %; one ring, one draw",
                    elegance="", child="")


# ---------------------------------------------------------------- [2] Hawkes process against the A6 kernel on occasions
HK_MU, HK_AL, HK_BE, HK_T, HK_DT = 1.0, 0.6, 1.0, 5000.0, 0.01


def _hawkes_events(seed=0):
    """Ogata thinning for lambda(t) = mu + sum alpha exp(-beta (t - t_i)); branching alpha/beta = 0.6."""
    U = np.random.default_rng(seed).random(4_000_000).tolist(); ui = 0
    t, ex, ev = 0.0, 0.0, []
    while True:
        lbar = HK_MU + ex; w = -math.log(U[ui]) / lbar; ui += 1
        t += w; ex *= math.exp(-HK_BE * w)
        if t > HK_T:
            break
        if U[ui] * lbar <= HK_MU + ex:
            ev.append(t); ex += HK_AL
        ui += 1
    return np.array(ev)


def _intensities(ev, q):
    """On the grid: the Hawkes intensity; the A6 kernel on occasions (event age k: each past event weighs alpha q^k,
    S <- q S + alpha at each event; D5 [M]: an occasion of a point process is one inter-event interval)."""
    grid = (np.arange(int(round(HK_T / HK_DT))) + 0.5) * HK_DT
    lh = np.empty(len(grid)); l6 = np.empty(len(grid))
    j, ex, S, tl, ne, evl = 0, 0.0, 0.0, 0.0, len(ev), ev.tolist()
    for k, g in enumerate(grid.tolist()):
        while j < ne and evl[j] < g:
            ex = ex * math.exp(-HK_BE * (evl[j] - tl)) + HK_AL; tl = evl[j]; S = q * S + HK_AL; j += 1
        lh[k] = HK_MU + ex * math.exp(-HK_BE * (g - tl)); l6[k] = HK_MU + S
    return grid, lh, l6


def _clock_readings(ev, grid, q):
    """Occasions as clock steps of width Delta = ln(1/q)/beta (a width read off the domain's beta): continuous age
    q^{(t - t_i)/Delta} and whole-occasion age q^{floor((t - t_i)/Delta)}."""
    dlt = math.log(1 / q) / HK_BE; n = len(grid)
    cont = np.full(n, HK_MU); diff = np.zeros(n + 1)
    K = int(math.ceil(math.log(1e-16) / math.log(q)))
    for ti in ev.tolist():
        i0 = int(math.ceil(ti / HK_DT - 0.5))
        i1 = min(n, int(math.ceil((ti + K * dlt) / HK_DT - 0.5)))
        if i0 < n:
            cont[i0:i1] += HK_AL * q ** ((grid[i0:i1] - ti) / dlt)
        for k in range(K):
            a = int(math.ceil((ti + k * dlt) / HK_DT - 0.5)); b = int(math.ceil((ti + (k + 1) * dlt) / HK_DT - 0.5))
            if a >= n:
                break
            diff[a] += HK_AL * q ** k; diff[min(b, n)] -= HK_AL * q ** k
    return cont, HK_MU + np.cumsum(diff)[:n]


def r2():
    cls, system, ing, Q, nul, H0, src = _decl("P10-2")
    ev = _hawkes_events()
    rr = {}
    for q in QGRID:
        grid, lh, l6 = _intensities(ev, q)
        rr[q] = math.sqrt(np.mean((l6 - lh) ** 2) / np.mean(lh ** 2))
    grid, lh, l6 = _intensities(ev, Q0)
    nrm = math.sqrt(np.mean(lh ** 2))
    e_null = math.sqrt(np.mean((HK_MU - lh) ** 2)) / nrm
    e_fit = math.sqrt(np.mean((lh.mean() - lh) ** 2)) / nrm
    cont, flo = _clock_readings(ev, grid, Q0)
    e_cont = math.sqrt(np.mean((cont - lh) ** 2)) / nrm; e_floor = math.sqrt(np.mean((flo - lh) ** 2)) / nrm
    crr, null, domain = rr[Q0], e_null, 0.0
    check = crr <= TOL_N
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row(cls, f"{system} (computed as: mu = {HK_MU}, alpha = {HK_AL}, beta = {HK_BE} (branching {HK_AL / HK_BE:.1f}), T = {HK_T:.0f}, Ogata thinning, seed 0; intensities compared on a {HK_DT} grid by relative RMS difference)",
                    source=src, Q=Q, ingredient=f"{ing}: geometric weights q^k over occasion age k, q = 0.5, with occasions the inter-event intervals (CRR D5 [M]); the same jump alpha per event as Hawkes",
                    null=nul, domain=H0,
                    numbers=f"{len(ev)} events (rate {len(ev) / HK_T:.3f}; stationary theory {HK_MU / (1 - HK_AL / HK_BE):.3f}); relative RMS distance from the Hawkes intensity: A6 on occasions {crr:.4f}; Poisson at mu {e_null:.4f}; Poisson at the mean rate {e_fit:.4f}; the Hawkes process itself {domain:.1f}; "
                            f"q-grid (sensitivity only): " + "; ".join(f"q = {q}: {rr[q]:.4f}" for q in QGRID) + "; "
                            f"clock-step readings (sensitivity, not CRR's occasion): continuous age with Delta = ln(1/q)/beta {e_cont:.2e}; whole-occasion age {e_floor:.4f}",
                    tg=f"distance {crr:.4f} vs Poisson {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the exponential-kernel Hawkes process is at distance {domain:.1f} from itself: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"the A6 kernel reproduces the Hawkes intensity (distance {crr:.4f} <= {TOL_N:.2f}): {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=f"with occasions counted in events, the A6 kernel forgets by event count, not by clock time, so its excitation settles at alpha/(1 - q) = {HK_AL / (1 - Q0):.2f} whatever the spacing and the intensity stays {_w(crr > TOL_N, 'far from', 'close to')} the Hawkes intensity ({crr:.4f}); with occasions as clock steps of width ln(1/q)/beta, a width taken from the domain's own beta, the geometric kernel {_w(e_cont <= 1e-9, 'becomes', 'does not become')} the exponential kernel with a continuous age ({e_cont:.1e}) and {_w(e_floor <= TOL_N, 'also', 'not')} with a whole-occasion age ({e_floor:.4f})",
                    weakness="DEVIATION (reading): 'occasion' is read as an inter-event interval, CRR's own definition for a point process (D5 [M]); the forecaster's reading (a geometric kernel in clock steps) is printed and would reproduce Hawkes by algebra, but needs a step width that CRR does not fix; the intensities are compared on the Hawkes path, not on a path simulated from the A6 intensity",
                    elegance="", child="")


# ---------------------------------------------------------------- [3] Schelling with remembered composition
SC_L, SC_VAC, SC_TOL, SC_SWEEPS, SC_SEEDS = 50, 0.1, 0.4, 100, 40


def _like_frac(G):
    A = (G == 1).astype(float); B = (G == 2).astype(float); O = (G > 0).astype(float)
    ca = np.zeros(G.shape); cb = np.zeros(G.shape); co = np.zeros(G.shape)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx or dy:
                ca += np.roll(np.roll(A, dx, 0), dy, 1); cb += np.roll(np.roll(B, dx, 0), dy, 1); co += np.roll(np.roll(O, dx, 0), dy, 1)
    same = np.where(G == 1, ca, np.where(G == 2, cb, 0.0))
    return np.where(co > 0, same / np.maximum(co, 1.0), 1.0)


def _schelling(seed, q, reset=True):
    """Torus L x L, 10 % vacant, two equal groups, Moore neighbourhood; per sweep (one occasion) every agent updates its
    remembered like-fraction M = (1 - q) f + q M and moves to a random vacancy when M < tolerance. reset: a mover's
    memory restarts at its new neighbourhood's composition; else it carries its old memory."""
    rng = np.random.default_rng(seed)
    cells = rng.permutation(SC_L * SC_L); nv = int(SC_VAC * SC_L * SC_L); half = (SC_L * SC_L - nv) // 2
    G = np.zeros(SC_L * SC_L, int); G[cells[nv:nv + half]] = 1; G[cells[nv + half:]] = 2; G = G.reshape(SC_L, SC_L)
    M = _like_frac(G)
    for _ in range(SC_SWEEPS):
        M = np.where(G > 0, (1 - q) * _like_frac(G) + q * M, 0.0)
        unhappy = np.argwhere((G > 0) & (M < SC_TOL))
        if len(unhappy) == 0:
            break
        rng.shuffle(unhappy)
        vac = [tuple(v) for v in np.argwhere(G == 0)]
        for i, j in unhappy.tolist():
            k = int(rng.integers(len(vac))); vi, vj = vac[k]
            G[vi, vj] = G[i, j]; G[i, j] = 0; vac[k] = (i, j)
            M[vi, vj] = np.nan if reset else M[i, j]; M[i, j] = 0.0
        if reset:
            M = np.where(np.isnan(M), _like_frac(G), M)
    f = _like_frac(G)
    return float(f[G > 0].mean())


def r3():
    cls, system, ing, Q, nul, H0, src = _decl("P10-3")
    seeds = range(SC_SEEDS)
    seg = {q: np.array([_schelling(sd, q) for sd in seeds]) for q in (0.0,) + QGRID}
    carry = np.array([_schelling(sd, Q0, reset=False) for sd in seeds])
    crr, null = float(seg[Q0].mean()), float(seg[0.0].mean())
    d = seg[Q0] - seg[0.0]; lower = int(np.sum(d < 0)); higher = int(np.sum(d > 0))
    drop = (null - crr) / null; check = drop > TOL_G
    out = outcome(crr=crr, null=null, domain=None, check=check)
    return make_row(cls, f"{system} (computed as: {SC_L} x {SC_L} torus, {int(100 * SC_VAC)} % vacant, two equal groups, Moore neighbourhood, an agent content when its (remembered) like-fraction >= {SC_TOL}; one sweep = one occasion; unhappy agents move to random vacancies; {SC_SWEEPS} sweeps; segregation index = mean like-neighbour fraction; {SC_SEEDS} paired seeds)",
                    source=src, Q=Q, ingredient=f"{ing}: M = (1 - q) f + q M per sweep, q = 0.5; a mover's memory restarts at its new neighbourhood",
                    null=nul, domain=H0,
                    numbers=f"final segregation index (mean over seeds): A6 {crr:.4f}, instantaneous {null:.4f}; drop {100 * drop:.2f} %; per-seed paired difference: mean {d.mean():+.4f}, sd {d.std(ddof=1):.4f}, A6 lower on {lower}/{SC_SEEDS}, higher on {higher}/{SC_SEEDS}; "
                            f"q-grid (sensitivity only): " + "; ".join(f"q = {q}: {seg[q].mean():.4f}" for q in QGRID) + f"; memory carried across moves (sensitivity): {carry.mean():.4f}",
                    tg=f"index {crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no theorem cited",
                    tc=f"memory lowers the final index by more than 1 % ({100 * drop:.2f} %): {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=f"the remembered like-fraction lags the present one, so agents react later; the final segregation index moves by {100 * drop:.2f} % ({_w(drop > 0, 'lower', 'higher')} with memory, lower on {lower} of {SC_SEEDS} seeds), {_w(check, 'more', 'less')} than the 1 % the Q needs{_w(check, '', '; the delay changes when agents move more than where the town ends')}",
                    weakness="one Schelling variant (random-vacancy moves, synchronous decisions, sequential relocation); 'final' is after 100 sweeps; the per-seed spread is printed beside the mean",
                    elegance="", child="")


# ---------------------------------------------------------------- [4] Nagel-Schreckenberg with remembered headway
NS_L, NS_VMAX, NS_P, NS_WARM, NS_MEAS = 2000, 5, 0.3, 1000, 2000


def _ns_flow(rho, q):
    """Ring of L cells; acceleration, braking to min(gap, floor(m)) with m the A6-remembered headway
    m <- (1 - q) gap + q m (q = 0: the standard rule, braking to gap), random slowdown p, move. Flow per cell per step."""
    rng = np.random.default_rng(int(round(rho * 1e5)))
    N = int(round(rho * NS_L)); x = np.sort(rng.choice(NS_L, N, replace=False)); v = np.zeros(N, int)
    m = ((np.roll(x, -1) - x - 1) % NS_L).astype(float); tot = 0
    for t in range(NS_WARM + NS_MEAS):
        gap = (np.roll(x, -1) - x - 1) % NS_L
        m = (1 - q) * gap + q * m
        v = np.minimum(v + 1, NS_VMAX)
        v = np.minimum(v, np.minimum(gap, np.floor(m).astype(int)))
        v = np.where((rng.random(N) < NS_P) & (v > 0), v - 1, v)
        x = (x + v) % NS_L
        if t >= NS_WARM:
            tot += int(v.sum())
    return tot / (NS_MEAS * NS_L)


def _ns_peak(q, step):
    rhos = np.round(np.arange(0.05, 0.20 + 1e-9, step), 5)
    J = np.array([_ns_flow(r, q) for r in rhos]); k = int(np.argmax(J))
    return float(rhos[k]), float(J[k])


def r4():
    cls, system, ing, Q, nul, H0, src = _decl("P10-4")
    fine = 0.0025
    rc = {q: _ns_peak(q, fine) for q in (0.0, Q0)}
    rc.update({q: _ns_peak(q, 0.005) for q in (0.25, 0.75)})
    crr, null = rc[Q0][0], rc[0.0][0]
    raise_ = (crr - null) / null; check = raise_ > TOL_G
    out = outcome(crr=crr, null=null, domain=None, check=check)
    return make_row(cls, f"{system} (computed as: ring of {NS_L} cells, vmax {NS_VMAX}, p = {NS_P}, warm-up {NS_WARM}, {NS_MEAS} measured steps; jam-transition density = the density of maximal flow on a {fine} grid over 0.05-0.20; braking to min(gap, floor(m)))",
                    source=src, Q=Q, ingredient=f"{ing}: m = (1 - q) gap + q m per step, q = 0.5, the headway the driver brakes to",
                    null=nul, domain=H0,
                    numbers=f"density of maximal flow: A6 {crr:.4f} (flow {rc[Q0][1]:.4f}), instantaneous {null:.4f} (flow {rc[0.0][1]:.4f}); change {100 * raise_:+.1f} %; "
                            f"q-grid (sensitivity only; q = 0.25 and 0.75 on a 0.005 grid): " + "; ".join(f"q = {q}: {rc[q][0]:.4f} (flow {rc[q][1]:.4f})" for q in QGRID),
                    tg=f"density {crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="H0 gives a direction for anticipation (looking ahead), not a number for memory (looking back)",
                    tc=f"memory raises the jam-transition density by more than 1 % ({100 * raise_:+.1f} %): {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=f"a driver who brakes to a remembered headway brakes to the smaller of the remembered and the actual gap, so after a close approach it stays cautious while the gap opens; the flow peak {_w(crr < null, 'moves down', 'moves up')} from density {null:.4f} to {crr:.4f} and the capacity {_w(rc[Q0][1] < rc[0.0][1], 'falls', 'rises')} from {rc[0.0][1]:.4f} to {rc[Q0][1]:.4f}{_w(rc[Q0][1] < rc[0.0][1] and crr < null, ': memory acts as the opposite of anticipation here', '')}",
                    weakness="DEVIATION (model): braking to the remembered headway alone lets cars overlap when the remembered gap exceeds the actual one, so the rule brakes to min(actual gap, floor(remembered gap)); with that safety constraint memory can only add caution; one seed per density (paired across arms); the density of maximal flow is read on a grid (step 0.0025, about 2 % of the density)",
                    elegance="", child="")


# ---------------------------------------------------------------- [5] Daley-Kendall with remembered encounters
DK_N, DK_RUNS = 20000, 10


def _dk_run(q, seed):
    """Daley-Kendall pair model (jump chain): every pair containing a spreader meets with equal probability. Ignorant met:
    it becomes a spreader. Spreader or stifler met: the spreader records a 'knower' encounter; spreader-spreader: both do.
    A spreader stops with probability m, its A6-remembered knower fraction over its own encounters (normalised geometric
    weights q^k over encounter age k; q = 0: m = 1 on meeting a knower, the Daley-Kendall rule)."""
    rng = np.random.default_rng(seed)
    st = [0] * DK_N; mm = [0.0] * DK_N; ww = [0.0] * DK_N
    st[0] = 1; spr = [0]; where = {0: 0}
    R = rng.random(1_000_000).tolist(); ri = 0

    def upd(i, ind):
        w = 1.0 + q * ww[i]; mm[i] = (ind + q * ww[i] * mm[i]) / w; ww[i] = w

    def stop(i):
        k = where.pop(i); last = spr.pop()
        if last != i:
            spr[k] = last; where[last] = k
        st[i] = 2

    while spr:
        if ri + 5 >= len(R):
            R = rng.random(1_000_000).tolist(); ri = 0
        i = spr[int(R[ri] * len(spr))]; j = int(R[ri + 1] * (DK_N - 1)); ri += 2
        if j >= i:
            j += 1
        sj = st[j]
        if sj == 0:
            upd(i, 0.0); st[j] = 1; where[j] = len(spr); spr.append(j)
        elif sj == 1:
            if R[ri] >= 0.5:        # a spreader-spreader pair is drawn twice as often from the spreader's side: halve it
                ri += 1; continue
            upd(i, 1.0); upd(j, 1.0); a, b = R[ri + 1], R[ri + 2]; ri += 3
            if b < mm[j]:
                stop(j)
            if a < mm[i]:
                stop(i)
        else:
            upd(i, 1.0)
            if R[ri] < mm[i]:
                stop(i)
            ri += 1
    return st.count(0) / DK_N


def r5():
    cls, system, ing, Q, nul, H0, src = _decl("P10-5")
    x_dk = brentq(lambda x: x - math.exp(-2.0 * (1.0 - x)), 0.05, 0.5)
    runs = {q: np.array([_dk_run(q, sd) for sd in range(DK_RUNS)]) for q in (0.0,) + QGRID}
    crr, null, domain = float(runs[Q0].mean()), float(runs[0.0].mean()), float(x_dk)
    se = float(runs[Q0].std(ddof=1) / math.sqrt(DK_RUNS)); se0 = float(runs[0.0].std(ddof=1) / math.sqrt(DK_RUNS))
    change = rel(crr, domain); check = change > TOL_G
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row(cls, f"{system} (computed as: population {DK_N}, one initial spreader, pair-model jump chain, {DK_RUNS} runs per arm, seeds 0-{DK_RUNS - 1})",
                    source=src, Q=Q, ingredient=f"{ing}: a spreader stops with probability equal to its remembered fraction of encounters with people who already knew (normalised weights q^k over encounter age, q = 0.5)",
                    null=nul, domain=H0,
                    numbers=f"final fraction never hearing: A6 {crr:.4f} (se {se:.4f}), instantaneous {null:.4f} (se {se0:.4f}); Daley-Kendall root of x = exp(-2(1 - x)): {domain:.6f}; change from it {100 * change:.1f} %; "
                            f"q-grid (sensitivity only): " + "; ".join(f"q = {q}: {runs[q].mean():.4f}" for q in QGRID),
                    tg=f"fraction {crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"Daley-Kendall's {domain:.4f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}; the memoryless simulation reproduces it {_w(rel(null, domain) <= 0.02, 'within 2 %', 'NOT within 2 %')} ({100 * rel(null, domain):.2f} %)",
                    tc=f"the never-hearing fraction changes by more than 1 % from {domain:.3f} ({100 * change:.1f} %): {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=f"a spreader who remembers mostly meeting people who had not heard stops less readily on its first knower, so spreaders live longer and the never-hearing fraction {_w(crr < domain, 'falls', 'rises')} from {domain:.4f} to {crr:.4f}; the effect is a lower effective stopping probability, and rumour models with a stopping probability below one are an existing generalisation that may already give this number (not checked)",
                    weakness="one reading of 'remembered encounters' (the stopping probability equals the remembered knower fraction; a new spreader has no memory); finite population and 10 runs per arm (standard errors printed)",
                    elegance="", child="")


def main():
    return run_batch("PRED70 batch P10: social systems and networks (Predictions70/DECLARATION.md; prompt-log entry 234; declared at 8397478)",
                     [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
