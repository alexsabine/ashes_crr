"""Life Sciences Phase A (Life_Sciences/DECLARATION_1.md, pushed before this script was written; prompt-log entry 217).

    uv run python Life_Sciences/checks/phase_a.py > Life_Sciences/checks/phase_a.txt

Synthetic worlds only; no data file is opened (R2, R11). Deterministic (fixed seeds, fixed grids); a rerun must be
byte-identical (R9). Every label is computed here from the numbers (R15).

  CD-1   H-L5 on the cell-size carrier: CV(arc) - CV(amplitude control) on adder, sizer and timer lineages
  G-CD3  H-CUT on replication initiation: W- (initiation adder + Cooper-Helmstetter) and W+ (initiation at the antipode)
         at three growth conditions; the standing runs/phaseA/gate_CUT.txt must read OPEN
  OL-3   the protocell division sits at the volume extremum (the H-CUT own-event comparison is empty)
  OL-2   A6/P3 memory and Eigen's error threshold, one SYNTHESIS row (harness labels)
  G-DS2  arc-threshold segmentation of synthetic nanopore squiggles against the domain's two-window t-test and a clock
  DS-3   the A1' step |dmu| sqrt(n) / sigma and where the domain detector misses

Operationalisations fixed here, before the first run, where the declaration left a detail open (AGENT_LOG 162):
  CD-1   'exactly 0 to round-off' = |CV(arc) - CV(amp)| <= 1e-9, occasions segment_end = 'exclusive' (the halving is the cut)
  G-CD3  initiation k is scored against the cycle [t_d, t_d') that contains it; the antipode is the first time after t_d with
         phi - phi(t_d) = pi (linear interpolation on the grid), used even if it falls after t_d'; tau = t_d' - t_d; the
         training half is the first half of the scored initiations (by time), the test half the rest; the domain rule's
         per-origin volume is u = v / n_o with n_o counted from the unit's own initiation and division events (starting 1);
         bootstrap 500 resamples of test initiations, seed 0; REDUCES is printed when W+ does not read PASS and at least
         half of the W+ units have |median e_CRR - median e_frac| < their step
  G-DS2  a boundary is the first sample of each new base; tolerance +-2 samples, greedy one-to-one matching in time order;
         aggregate F1 over reads (totals of TP, FP, FN); bootstrap 500 resamples of reads, seed 0
  DS-3   n = the smaller of the two dwells adjacent to the boundary; bins below 1 step and at or above 1 step; HOLDS if the
         miss-rate ratio (below / above) >= 2 at every level; also printed without the repeated-level boundaries
"""
import math
import os

import numpy as np
from scipy.signal import find_peaks

from crr.instrument.core import intrinsic_phase, regularity
from crr.synthesis.harness import make_row, outcome, print_rows, rel

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _w(c, a, b):
    return a if c else b


# ================================================================ CD-1: H-L5 on the cell-size carrier
def size_lineage(rule, n=300, seed=3, fs=100, noise=0.1, rate_cv=0.2):
    """Exponential growth from birth size v_b; adder divides at v_b + D, sizer at a fixed size S, timer after a fixed time;
    each target with 10 % noise, growth rate with 20 % spread per cycle; the daughter is half. Sampled at fs per unit time."""
    rng = np.random.default_rng(seed)
    x, ev, vb = [], [], 1.0
    for _ in range(n):
        lam = 0.7 * (1 + rate_cv * rng.standard_normal())
        lam = max(lam, 0.1)
        eps = 1 + noise * rng.standard_normal()
        if rule == "adder":
            vd = vb + 1.0 * eps
        elif rule == "sizer":
            vd = max(2.0 * eps, vb * 1.05)
        else:
            vd = vb * math.exp(lam * (math.log(2) / 0.7) * eps)
        T = math.log(vd / vb) / lam
        m = max(int(round(T * fs)), 2)
        ev.append(len(x))
        x.extend(vb * np.exp(lam * np.arange(m) / fs))
        vb = vb * math.exp(lam * m / fs) / 2.0
    return np.asarray(x), np.asarray(ev), 1.0 / fs


def cd1():
    print("[CD-1] H-L5 on the cell-size carrier: the arc of a monotone growth occasion is its amplitude (P1)")
    ok_all = True
    for rule in ("adder", "sizer", "timer"):
        x, ev, dt = size_lineage(rule)
        r = regularity(x, ev[20:], sigma=1.0, dt=dt, n_boot=500, seed=0, segment_end="exclusive")
        d = r["cv_arc"] - r["cv_amp"]
        ok = abs(d) <= 1e-9
        ok_all &= ok
        cls = ("CI includes 0" if r["ci95"][0] <= 0 <= r["ci95"][1]
               else _w(r["cv_arc"] < r["cv_clock"], "arc-regular", "clock-regular"))
        print(f"  {rule:5}: {r['n']} occasions, CV(arc) {r['cv_arc']:.6f}, CV(clock) {r['cv_clock']:.6f}, "
              f"CV(amplitude) {r['cv_amp']:.6f}; CV(arc) - CV(amp) = {d:+.3e} -> {_w(ok, 'identical', 'differ')}; "
              f"bare class (CI of CV(arc) - CV(clock) [{r['ci95'][0]:+.4f}, {r['ci95'][1]:+.4f}]): {cls}")
    print(f"  CD-1 prediction (control (i) can never be beaten on this carrier): {_w(ok_all, 'HOLDS', 'FAILS')}")
    print()


# ================================================================ G-CD3: H-CUT on replication initiation
DT = 0.5          # grid step, min
CD = 70.0         # C + D, min
DELTA_I = 1.0     # added per-origin volume between initiations
N_LIN, N_CYC, BURN = 10, 150, 20


def cell_lineage(tau_bar, seed):
    """W-: the initiation adder with Cooper-Helmstetter division (DECLARATION_1 G-CD3). Returns the grid log-volume, the
    initiation times and the division times (min)."""
    rng = np.random.default_rng(seed)
    lam0 = math.log(2) / tau_bar
    lam = lam0 * (1 + 0.1 * rng.standard_normal())
    u, v = DELTA_I, 1.0
    target = u + DELTA_I * (1 + 0.1 * rng.standard_normal())
    pending, inits, divs, logv = [], [], [], []
    t, k = 0.0, 0
    need = N_CYC + BURN + 2
    while len(divs) < need:
        g = math.exp(lam * DT)
        u *= g
        v *= g
        t = (k + 1) * DT
        k += 1
        if u >= target:
            inits.append(t)
            u /= 2.0
            target = u + DELTA_I * (1 + 0.1 * rng.standard_normal())
            pending.append(t + CD * (1 + 0.1 * rng.standard_normal()))
            pending.sort()
        while pending and pending[0] <= t:
            pending.pop(0)
            v /= 2.0
            divs.append(t)
            lam = lam0 * (1 + 0.1 * rng.standard_normal())
        logv.append(math.log(v))
    return np.asarray(logv), np.asarray(inits), np.asarray(divs)


def _interp_time(phi, idx0, target):
    """First grid time after index idx0 at which phi reaches target (linear interpolation); None if never."""
    seg = phi[idx0:]
    j = np.nonzero(seg >= target)[0]
    if len(j) == 0:
        return None
    j = int(j[0]) + idx0
    if j == idx0:
        return (j + 1) * DT
    f = (target - phi[j - 1]) / (phi[j] - phi[j - 1])
    return (j + f) * DT


def score_unit(logv, inits, divs, rng_seed=0):
    """Per-unit errors e = |t_init - t_rule| / tau for CRR (antipode), a fitted constant fraction and the initiation adder."""
    phi = intrinsic_phase(logv, detrend=True)
    tgrid = (np.arange(len(logv)) + 1) * DT
    v = np.exp(logv)
    # origin count from the unit's own events: doubles at each initiation, halves at each division
    ev = sorted([(ti, 2.0) for ti in inits] + [(td, 0.5) for td in divs])
    n_o = np.ones(len(tgrid))
    cur, j = 1.0, 0
    for i, tt in enumerate(tgrid):
        while j < len(ev) and ev[j][0] <= tt:
            cur *= ev[j][1]
            j += 1
        n_o[i] = cur
    u = v / n_o
    d_scored = divs[BURN:]
    rows = []
    for a, b in zip(d_scored[:-1], d_scored[1:]):
        ia = int(round(a / DT)) - 1
        ta = _interp_time(phi, ia, phi[ia] + math.pi)
        for ti in inits[(inits >= a) & (inits < b)]:
            rows.append((ti, a, b - a, ta))
    rows = [r for r in rows if r[3] is not None]
    if len(rows) < 20:
        return None
    half = len(rows) // 2
    train, test = rows[:half], rows[half:]
    f_hat = float(np.median([(ti - a) / tau for ti, a, tau, _ in train]))
    # the initiation adder: per-origin volume added between consecutive initiations (u just before minus u just after)
    idx = {ti: int(round(ti / DT)) - 1 for ti in inits}
    adds, prev_after = [], {}
    for p, q in zip(inits[:-1], inits[1:]):
        prev_after[q] = u[idx[p]]                         # u right after the halving at initiation p (grid sample at p)
    for ti, _, _, _ in train:
        if ti in prev_after:
            adds.append(u[idx[ti] - 1] - prev_after[ti])
    d_hat = float(np.median(adds))
    e_crr, e_frac, e_dom = [], [], []
    for ti, a, tau, ta in test:
        e_crr.append(abs(ti - ta) / tau)
        e_frac.append(abs(ti - (a + f_hat * tau)) / tau)
        if ti in prev_after:
            thr = prev_after[ti] + d_hat
            p_idx = int(np.nonzero(inits == ti)[0][0]) - 1
            start = idx[inits[p_idx]] + 1
            # the rule's own trajectory: u with the halvings of later initiations undone (AGENT_LOG 162, fixed after run 1:
            # searching the halved u slipped the prediction by a whole cycle whenever d_hat exceeded the realised add)
            later = np.searchsorted(inits, tgrid[start:], side="right") - (p_idx + 1)
            hit = np.nonzero(u[start:] * 2.0 ** later >= thr)[0]
            t_dom = tgrid[start + int(hit[0])] if len(hit) else np.inf
        else:
            t_dom = np.inf
        e_dom.append(abs(ti - t_dom) / tau)
    e_crr, e_frac, e_dom = map(np.asarray, (e_crr, e_frac, e_dom))
    taus = np.asarray([r[2] for r in test])

    def stat(ix):
        return float(np.median(e_crr[ix]) - min(np.median(e_frac[ix]), np.median(e_dom[ix])))

    rng = np.random.default_rng(rng_seed)
    n = len(test)
    boots = [stat(rng.integers(0, n, n)) for _ in range(500)]
    step = max(DT / float(np.median(taus)), 2.0 * float(np.std(boots)))
    all_ix = np.arange(n)
    d = stat(all_ix)
    return dict(n=n, f_hat=f_hat, d_hat=d_hat, m_crr=float(np.median(e_crr)), m_frac=float(np.median(e_frac)),
                m_dom=float(np.median(e_dom)), d=d, step=step, passes=d <= -step,
                ties_frac=abs(float(np.median(e_crr)) - float(np.median(e_frac))) < step,
                frac_init=float(np.median([(ti - a) / tau for ti, a, tau, _ in rows])))


def w_plus(logv, divs, seed):
    """W+: the same volume trace with each initiation moved to the antipode of the preceding division + N(0, 0.05 tau)."""
    rng = np.random.default_rng(10_000 + seed)
    phi = intrinsic_phase(logv, detrend=True)
    out = []
    for a, b in zip(divs[:-1], divs[1:]):
        ia = int(round(a / DT)) - 1
        ta = _interp_time(phi, ia, phi[ia] + math.pi)
        if ta is None:
            continue
        out.append(ta + 0.05 * (b - a) * rng.standard_normal())
    return np.asarray(sorted(out))


def gcd3():
    print("[G-CD3] H-CUT on replication initiation (W- the initiation adder, W+ initiation at the antipode)")
    txt = open(os.path.join(ROOT, "runs", "phaseA", "gate_CUT.txt")).read()
    cut_open = "GATE OPEN" in txt
    print(f"  standing gate_CUT (runs/phaseA/gate_CUT.txt): {_w(cut_open, 'OPEN', 'not OPEN')}")
    verdicts, reduces_any = [], False
    for tau_bar in (100.0, 50.0, 25.0):
        res = {"W-": [], "W+": []}
        for s in range(N_LIN):
            logv, inits, divs = cell_lineage(tau_bar, seed=1000 * int(tau_bar) + s)
            res["W-"].append(score_unit(logv, inits, divs))
            res["W+"].append(score_unit(logv, w_plus(logv, divs, s), divs))
        print(f"  tau_bar {tau_bar:.0f} min (C+D {CD:.0f} min):")
        lab = {}
        for w in ("W-", "W+"):
            units = [r for r in res[w] if r is not None]
            frac = sum(r["passes"] for r in units) / len(units)
            lab[w] = "PASS" if frac >= 0.8 else ("FAIL" if frac < 0.6 else "NOT DECIDED")
            print(f"    {w}: {len(units)} units ({N_LIN - len(units)} excluded, < 20 initiations); pass fraction "
                  f"{frac:.2f} -> {lab[w]}")
            for k, r in enumerate(units):
                print(f"      unit {k}: n {r['n']:3d}, init at cycle fraction (median) {r['frac_init']:.3f}, "
                      f"median e: antipode {r['m_crr']:.4f}, fitted fraction {r['m_frac']:.4f} (f {r['f_hat']:.3f}), "
                      f"initiation adder {r['m_dom']:.4f}; d {r['d']:+.4f}, step {r['step']:.4f} -> "
                      f"{_w(r['passes'], 'pass', 'no')}")
        units_p = [r for r in res["W+"] if r is not None]
        tie = sum(r["ties_frac"] for r in units_p) / len(units_p)
        red = lab["W+"] != "PASS" and tie >= 0.5
        reduces_any |= red
        ok = lab["W+"] == "PASS" and lab["W-"] == "FAIL"
        verdicts.append(ok)
        print(f"    W+ units where the antipode ties the fitted fraction within a step: {tie:.2f}"
              f"{_w(red, ' -> REDUCES (to a fixed cycle fraction)', '')}")
        print(f"    condition: W+ {lab['W+']}, W- {lab['W-']} -> {_w(ok, 'as required', 'NOT as required')}")
    gate = cut_open and all(verdicts)
    print(f"  G-CD3: {_w(gate, 'OPEN', 'CLOSED')}{_w(reduces_any, ' (REDUCES printed at one or more conditions)', '')}")
    print()
    return gate


# ================================================================ OL-3: the protocell division is the extremum
def ol3():
    rng = np.random.default_rng(5)
    x, divs, v = [], [], 1.0
    for _ in range(200):
        lam = 0.02 * (1 + 0.1 * rng.standard_normal())
        m = int(round(math.log(2 * (1 + 0.05 * rng.standard_normal())) / lam / DT))
        x.extend(v * np.exp(lam * DT * np.arange(1, m + 1)))
        v = x[-1] / 2.0
        divs.append(len(x))                   # the first sample after the halving
    x = np.asarray(x)
    pk, _ = find_peaks(x)
    divs = np.asarray(divs[:-1])
    near = np.array([np.min(np.abs(pk - (d - 1))) <= 1 for d in divs])
    print("[OL-3] protocell size sawtooth (200 cycles): divisions within one grid step of a volume maximum: "
          f"{near.mean():.4f} ({near.sum()}/{len(divs)}) -> the own event is the extremum; "
          f"H-CUT's own-event comparison is {_w(near.mean() == 1.0, 'empty', 'not empty')}")
    print()


# ================================================================ OL-2: A6 memory and Eigen's error threshold
SIGMA, LENGTH = 10.0, 50


def master_growth(mu, q, T=3000):
    """Iterate the master subsystem N_m(t) = sigma Q sum_k w_k N_m(t-1-k), w_k = (1-q) q^k, and return the asymptotic
    per-generation factor (renormalised each step; the system is linear)."""
    Qc = (1 - mu) ** LENGTH
    K = 1 if q == 0 else int(math.ceil(math.log(1e-13) / math.log(q)))
    w = (1 - q) * q ** np.arange(K)
    w /= w.sum()
    hist = np.ones(K)                          # hist[0] = generation t-1, hist[1] = t-2, ...
    fac = 1.0
    for _ in range(T):
        new = SIGMA * Qc * float(w @ hist)
        fac = new / hist[0]
        hist = np.concatenate(([new], hist[:-1])) / new
    return fac


def stationary_master(mu, q, T=6000):
    Qc = (1 - mu) ** LENGTH
    K = 1 if q == 0 else int(math.ceil(math.log(1e-13) / math.log(q)))
    w = (1 - q) * q ** np.arange(K)
    w /= w.sum()
    hm, hu = np.full(K, 0.5), np.full(K, 0.5)
    for _ in range(T):
        pm, pu = float(w @ hm), float(w @ hu)
        nm = SIGMA * Qc * pm
        nu = SIGMA * (1 - Qc) * pm + pu
        tot = nm + nu
        hm = np.concatenate(([nm], hm[:-1])) / tot
        hu = np.concatenate(([nu], hu[:-1])) / tot
    return hm[0] / (hm[0] + hu[0])


def mu_c(q, it=False):
    lo, hi = 1e-6, 0.2
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lam = master_growth(mid, q) if it else q + SIGMA * (1 - mid) ** LENGTH * (1 - q)
        lo, hi = (mid, hi) if lam > 1 else (lo, mid)
    return 0.5 * (lo + hi)


def ol2():
    eig = 1 - SIGMA ** (-1 / LENGTH)
    qs = (0.0, 0.5, 0.9)
    mc = {q: mu_c(q) for q in qs}
    mi = {q: mu_c(q, it=True) for q in qs}
    mu_half = 0.5 * eig
    xs = {q: stationary_master(mu_half, q) for q in qs}
    lam = {q: q + SIGMA * (1 - mu_half) ** LENGTH * (1 - q) for q in qs}
    x_eigen = (SIGMA * (1 - mu_half) ** LENGTH - 1) / (SIGMA - 1)
    crr, null = mc[0.9], mc[0.0]
    check = all(rel(mi[q], mc[q]) <= 1e-3 for q in qs)
    out = outcome(crr=crr, null=null, domain=eig, check=check)
    row = make_row(
        "life", f"Eigen's quasispecies, single-peak landscape (master fitness {SIGMA:g}, mutants 1, length {LENGTH}, "
        "no back mutation), with templates regenerated from the settled past",
        source="Life_Sciences/DECLARATION_1.md OL-2",
        Q="regenerating templates from the settled past with A6/P3 geometric age weights (offspring copied from templates of "
          "age k with weight (1-q) q^k) moves Eigen's error threshold mu_c",
        ingredient="A6 with P3 weights (q not fixed by CRR; q = 0.9 against q = 0)",
        null="q = 0: Eigen's discrete generations",
        domain=f"Eigen's threshold sigma (1-mu)^L = 1, mu_c = 1 - sigma^(-1/L) = {eig:.6f}; the renewal (Euler-Lotka) "
               "argument: a positive delay kernel moves the growth rate, not the sign of lambda - 1",
        numbers=(f"mu_c from the characteristic equation (lambda_m = q + sigma Q (1-q)): q 0 {mc[0.0]:.6f}, q 0.5 "
                 f"{mc[0.5]:.6f}, q 0.9 {mc[0.9]:.6f}; from iterating the dynamics: q 0 {mi[0.0]:.6f}, q 0.5 "
                 f"{mi[0.5]:.6f}, q 0.9 {mi[0.9]:.6f}; at mu = mu_c/2 = {mu_half:.6f}: stationary master fraction "
                 f"q 0 {xs[0.0]:.4f} (Eigen's (sigma Q - 1)/(sigma - 1) = {x_eigen:.4f}), q 0.5 {xs[0.5]:.4f}, q 0.9 "
                 f"{xs[0.9]:.4f}; master growth factor per generation q 0 {lam[0.0]:.4f}, q 0.5 {lam[0.5]:.4f}, "
                 f"q 0.9 {lam[0.9]:.4f}"),
        tg=f"mu_c(q 0.9) {crr:.6f} vs null mu_c(q 0) {null:.6f}: {_w(rel(crr, null) <= 1e-2, 'agree', 'differ')}",
        tn=f"Eigen's mu_c {eig:.6f}: {_w(rel(crr, eig) <= 1e-2, 'agree', 'differ')}",
        tc=f"the iterated thresholds match the characteristic equation within 0.1 % at every q: "
           f"{_w(check, 'holds', 'fails')}",
        out=out,
        reading=(f"memory of the settled past {_w(rel(lam[0.9], lam[0.0]) > 1e-3, 'changes', 'leaves unchanged')} how fast "
                 f"the master grows (factor {lam[0.9]:.4f} at q 0.9 against {lam[0.0]:.4f} at q 0), "
                 f"{_w(rel(xs[0.9], xs[0.0]) > 1e-3, 'changes', 'leaves unchanged')} the stationary master fraction "
                 f"({xs[0.9]:.4f} against {xs[0.0]:.4f}) and {_w(rel(crr, null) > 1e-2, 'moves', 'does not move')} the "
                 "threshold, which is where sigma Q crosses 1 (AGENT_LOG 162: this reading was hard-coded in the first run, "
                 "phase_a_run1.txt, and contradicted its own numbers on the stationary fraction; the words are now computed)"),
        weakness="a single-peak landscape without back mutation, the textbook case; q is free in CRR, so no q is predicted",
        child="Copying from older copies as well as new ones changes how fast the good copy spreads, but not the error "
              "rate at which it is lost.")
    print("[OL-2] SYNTHESIS row: A6 memory and Eigen's error threshold")
    print_rows([row])
    return row


# ================================================================ G-DS2 and DS-3: nanopore squiggle segmentation
N_READS, N_BASES = 200, 400
TOL = 2


def squiggles(s_level, seed):
    rng = np.random.default_rng(seed)
    reads = []
    for _ in range(N_READS):
        lev = rng.normal(0.0, s_level, N_BASES)
        rep = rng.random(N_BASES) < 0.05
        for j in range(1, N_BASES):
            if rep[j]:
                lev[j] = lev[j - 1]
        dw = np.maximum(np.rint(rng.gamma(2.0, 4.5, N_BASES)).astype(int), 2)
        x = np.repeat(lev, dw) + rng.standard_normal(int(dw.sum()))
        bounds = np.cumsum(dw)[:-1]
        dmu = np.abs(np.diff(lev))
        nmin = np.minimum(dw[:-1], dw[1:])
        reads.append((x, bounds, dmu, nmin))
    return reads


def match(det, truth):
    """Greedy one-to-one matching in time order within +-TOL; returns (tp, fp, fn, matched mask over truth)."""
    det = np.asarray(det)
    used = np.zeros(len(det), bool)
    hit = np.zeros(len(truth), bool)
    j = 0
    for i, b in enumerate(truth):
        while j < len(det) and det[j] < b - TOL:
            j += 1
        k = j
        while k < len(det) and det[k] <= b + TOL:
            if not used[k]:
                used[k] = True
                hit[i] = True
                break
            k += 1
    tp = int(hit.sum())
    return tp, len(det) - int(used.sum()), len(truth) - tp, hit


def sigma_hat(x):
    d = np.diff(x)
    return float(np.median(np.abs(d - np.median(d))) * 1.4826 / math.sqrt(2))


def arc_cuts(y, sig, theta):
    A = np.concatenate(([0.0], np.cumsum(np.abs(np.diff(y)) / sig)))
    cuts, last = [], 0.0
    while True:
        k = int(np.searchsorted(A, last + theta, side="left"))
        if k >= len(A):
            break
        cuts.append(k)
        last = A[k]
    return cuts


def movavg(x, w):
    c = np.cumsum(np.concatenate(([0.0], x)))
    m = (c[w:] - c[:-w]) / w
    pad = w // 2
    return np.concatenate((np.full(pad, m[0]), m, np.full(len(x) - len(m) - pad, m[-1])))


def tstat(x, w):
    c = np.cumsum(np.concatenate(([0.0], x)))
    c2 = np.cumsum(np.concatenate(([0.0], x * x)))
    n = len(x)
    t = np.zeros(n)
    i = np.arange(w, n - w + 1)
    mL = (c[i] - c[i - w]) / w
    mR = (c[i + w] - c[i]) / w
    vL = (c2[i] - c2[i - w]) / w - mL ** 2
    vR = (c2[i + w] - c2[i]) / w - mR ** 2
    t[i] = np.abs(mR - mL) / np.sqrt(np.maximum(vL + vR, 1e-12) / w)
    return t


GRIDS = {"A-raw": [(None, th) for th in np.arange(2.0, 40.01, 1.0)],
         "A-smooth": [(w, th) for w in (3, 5, 7) for th in np.arange(0.25, 20.01, 0.25)],
         "T": [(w, th) for w in (3, 5, 7) for th in np.arange(0.5, 15.01, 0.25)],
         "CL": [(None, k) for k in range(3, 21)]}


def detect(name, x, par, cache):
    w, th = par
    if name == "A-raw":
        return arc_cuts(x, cache["sig"], th)
    if name == "A-smooth":
        key = ("ma", w)
        if key not in cache:
            cache[key] = movavg(x, w)
        return arc_cuts(cache[key], cache["sig"], th)
    if name == "T":
        key = ("t", w)
        if key not in cache:
            cache[key] = tstat(x, w)
        pk, _ = find_peaks(cache[key], height=th, distance=2)
        return pk
    return list(range(th, len(x), th))


def counts(name, reads, par, caches):
    out = []
    for (x, b, _, _), c in zip(reads, caches):
        tp, fp, fn, hit = match(detect(name, x, par, c), b)
        out.append((tp, fp, fn, hit))
    return out


def f1(rows, ix=None):
    ix = range(len(rows)) if ix is None else ix
    tp = sum(rows[i][0] for i in ix)
    fp = sum(rows[i][1] for i in ix)
    fn = sum(rows[i][2] for i in ix)
    return 2 * tp / max(2 * tp + fp + fn, 1)


def gds2():
    print("[G-DS2] arc-threshold segmentation of synthetic squiggles against the domain's two-window t-test and a clock")
    print(f"  {N_READS} training + {N_READS} test reads of {N_BASES} bases per level; dwell Gamma(2, mean 9) >= 2 samples; "
          f"5 % repeated levels; noise sigma 1; tolerance +-{TOL} samples")
    ok_levels, ds3_ok = [], []
    for s_level in (1.0, 2.0, 4.0):
        tr = squiggles(s_level, seed=int(100 * s_level))
        te = squiggles(s_level, seed=int(100 * s_level) + 7)
        ctr = [{"sig": sigma_hat(r[0])} for r in tr]
        cte = [{"sig": sigma_hat(r[0])} for r in te]
        best, test_rows = {}, {}
        for name, grid in GRIDS.items():
            scores = [(f1(counts(name, tr, p, ctr)), i) for i, p in enumerate(grid)]
            sc, i = max(scores)
            best[name] = (grid[i], sc)
            test_rows[name] = counts(name, te, grid[i], cte)
        F = {k: f1(v) for k, v in test_rows.items()}
        arc = max(("A-raw", "A-smooth"), key=lambda k: F[k])
        rng = np.random.default_rng(0)

        def boot_se(a, b):
            n = len(te)
            ds = []
            for _ in range(500):
                ix = rng.integers(0, n, n)
                ds.append(f1(test_rows[a], ix) - f1(test_rows[b], ix))
            return float(np.std(ds))

        st_t = max(0.02, 2 * boot_se(arc, "T"))
        st_c = max(0.02, 2 * boot_se(arc, "CL"))
        st_rc = max(0.02, 2 * boot_se("A-raw", "CL"))
        beat_t = F[arc] >= F["T"] + st_t
        beat_c = F[arc] >= F["CL"] + st_c
        raw_clock = abs(F["A-raw"] - F["CL"]) < st_rc
        ok_levels.append(beat_t and beat_c)
        print(f"  level spread s = {s_level:g} sigma:")
        for name in GRIDS:
            (w, th), sc = best[name]
            par = f"w {w}, " if w is not None else ""
            print(f"    {name:8}: tuned {par}threshold {th:g} (train F1 {sc:.4f}) -> test F1 {F[name]:.4f}")
        print(f"    better arc detector {arc}: vs T {F[arc] - F['T']:+.4f} (step {st_t:.4f}) -> "
              f"{_w(beat_t, 'ahead', 'not ahead')}; vs CL {F[arc] - F['CL']:+.4f} (step {st_c:.4f}) -> "
              f"{_w(beat_c, 'ahead', 'not ahead')}; A-raw vs CL {F['A-raw'] - F['CL']:+.4f} (step {st_rc:.4f})"
              f"{_w(raw_clock, ' -> REDUCES (to a clock)', '')}")
        # DS-3 on the domain detector's test boundaries
        hits = np.concatenate([r[3] for r in test_rows["T"]])
        dmu = np.concatenate([r[2] for r in te])
        nmin = np.concatenate([r[3] for r in te])
        z = dmu * np.sqrt(nmin)
        below, above = z < 1.0, z >= 1.0
        mb, ma = 1 - hits[below].mean(), 1 - hits[above].mean()
        nonrep = dmu > 0
        mb2 = 1 - hits[below & nonrep].mean()
        ratio = mb / ma if ma > 0 else math.inf
        ds3_ok.append(ratio >= 2)
        print(f"    DS-3 (T's misses by the A1' step |dmu| sqrt(n) / sigma): below 1 step {below.sum()} boundaries, miss "
              f"rate {mb:.4f} ({mb2:.4f} without repeated levels); at or above 1 step {above.sum()}, miss rate "
              f"{ma:.4f}; ratio {ratio:.2f} -> {_w(ratio >= 2, 'holds', 'fails')}")
    gate = all(ok_levels)
    print(f"  G-DS2: {_w(gate, 'OPEN', 'CLOSED')}")
    print(f"  DS-3 prediction (misses below one step at least twice as often, every level): "
          f"{_w(all(ds3_ok), 'HOLDS', 'FAILS')} (the t-test's own power function: REDUNDANT-DOMAIN whichever way)")
    print(f"  under noise alone a raw arc advances by E|dx|/sigma = 2/sqrt(pi) = {2 / math.sqrt(math.pi):.4f} per sample")
    print()
    return gate


def main():
    print("Life Sciences Phase A (Life_Sciences/DECLARATION_1.md; prompt-log entry 217). Synthetic worlds only; no data opened.")
    print()
    cd1()
    g3 = gcd3()
    ol3()
    ol2()
    g2 = gds2()
    print(f"SUMMARY: G-CD3 {_w(g3, 'OPEN', 'CLOSED')}; G-DS2 {_w(g2, 'OPEN', 'CLOSED')}")


if __name__ == "__main__":
    main()
