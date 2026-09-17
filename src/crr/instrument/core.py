"""CRR instrument. Implements the definitions in theory/CRR.md.

Every function is pure, deterministic, and takes its constants as arguments
so that a pre-registration can name them. No integer step counting anywhere.
"""
from __future__ import annotations

import numpy as np
from scipy.signal import find_peaks, hilbert, savgol_filter
from scipy.stats import binomtest


# ---------------------------------------------------------------- unit (A1')
def unit_sigma(stat: np.ndarray, detrend_window: int = 9, detrend_order: int = 2,
               scale: str = "mad", min_sigma: float | None = None) -> float:
    """sigma = robust scale of the residual of ONE occasion statistic across occasions.

    stat            per-occasion statistic on TRAINING occasions only
    detrend_window  savgol window (odd); named in the prereg
    scale           "mad" -> 1.4826*MAD ; "std" -> std
    min_sigma       instrument quantisation step; if sigma < min_sigma the record is
                    rejected (raise) rather than floored. No additive epsilon.
    """
    stat = np.asarray(stat, float)
    if len(stat) < detrend_window + 2:
        raise ValueError("too few occasions for the named detrender")
    res = stat - savgol_filter(stat, detrend_window, detrend_order)
    if scale == "mad":
        sig = 1.4826 * np.median(np.abs(res - np.median(res)))
    elif scale == "std":
        sig = float(np.std(res, ddof=1))
    else:
        raise ValueError(scale)
    if not np.isfinite(sig) or sig <= 0:
        raise ValueError("degenerate residual: record rejected (no floor is applied)")
    if min_sigma is not None and sig < min_sigma:
        raise ValueError(f"sigma {sig:.3g} below instrument step {min_sigma:.3g}: record rejected")
    return float(sig)


def rho(extent: float, sigma: float) -> float:
    """Resolution rho = extent / sigma (A1'): how many resolvable steps the
    trace spans. For REPORTING (gates, reports, preregs) only — never used
    inside a threshold (R5: thresholds are never finer than one resolvable
    step, and rho is not a criterion input)."""
    return float(extent / sigma)

# ---------------------------------------------------------------- arc (D2), chord (D3), surplus (D4)
def arc_length(x: np.ndarray, sigma: float = 1.0, metric: np.ndarray | None = None) -> float:
    """Real-valued Fisher–Rao arc of a sampled path, in units of sigma.

    x       (T,) or (T,d) samples
    metric  None -> identity; (d,) -> diagonal g; (d,d) -> full g (constant)
    """
    x = np.atleast_2d(np.asarray(x, float).T).T if np.ndim(x) == 1 else np.asarray(x, float)
    dx = np.diff(x, axis=0)
    if metric is None:
        step = np.sqrt((dx * dx).sum(axis=1))
    elif np.ndim(metric) == 1:
        step = np.sqrt((dx * dx * metric).sum(axis=1))
    else:
        step = np.sqrt(np.einsum("ti,ij,tj->t", dx, metric, dx))
    return float(step.sum() / sigma)


def chord(x: np.ndarray, sigma: float = 1.0, metric: np.ndarray | None = None) -> float:
    x = np.atleast_2d(np.asarray(x, float).T).T if np.ndim(x) == 1 else np.asarray(x, float)
    d = x[-1] - x[0]
    if metric is None:
        c = np.sqrt((d * d).sum())
    elif np.ndim(metric) == 1:
        c = np.sqrt((d * d * metric).sum())
    else:
        c = np.sqrt(d @ metric @ d)
    return float(c / sigma)


def surplus(x: np.ndarray, sigma: float = 1.0, metric: np.ndarray | None = None) -> tuple[float, float, float]:
    """(C, C*, S) with S = C - C* >= 0 by P1, up to floating-point round-off.

    Report the sign distribution alongside any S verdict (CLAUDE.md §3.1
    item 5); never clamp."""
    C = arc_length(x, sigma, metric)
    Cs = chord(x, sigma, metric)
    return C, Cs, C - Cs


# ---------------------------------------------------------------- phase and cuts (A3)
def intrinsic_phase(x: np.ndarray, detrend: bool = True) -> np.ndarray:
    """Unwrapped analytic-signal phase (radians). One choice of intrinsic phase;
    a prereg may name another (Poincaré section) — both must be reported."""
    x = np.asarray(x, float)
    if detrend:
        x = x - np.mean(x)
    return np.unwrap(np.angle(hilbert(x)))


def antipodal_cuts(phase: np.ndarray, start: int = 0, half_turn: float = np.pi) -> np.ndarray:
    """Indices where the phase has advanced by half a turn since the last cut.
    This IS the cut of A3. Oriented: only forward crossings count.

    The target phase advances by exactly half_turn from the previous *target*
    (sub-sample crossing), not from the sample where the crossing was detected,
    so discretisation does not accumulate. The returned index is the sample
    nearest the interpolated crossing.

    Cuts are STRICTLY increasing. When the phase advances by more than one
    half-turn between consecutive samples (sampling below ~4 samples per half
    turn), several targets map to the same nearest sample; the colliding cut
    is dropped, not re-used. A record that drops cuts this way is undersampled
    and should be excluded by the prereg's minimum-sampling-density rule
    (~4 samples per half turn)."""
    cuts = [start]
    target = phase[start] + half_turn
    i = start + 1
    n = len(phase)
    while i < n:
        if phase[i] >= target:
            # linear interpolation between i-1 and i
            p0, p1 = phase[i - 1], phase[i]
            frac = 0.0 if p1 == p0 else (target - p0) / (p1 - p0)
            cut = int(round(i - 1 + frac))
            target += half_turn
            if cut <= cuts[-1]:
                # collision: this sample is also the nearest sample for the
                # previous target. Drop it (strictly increasing cuts); the
                # phase already advanced, so the target keeps moving.
                pass
            else:
                cuts.append(cut)
            # do not advance i: several targets may be crossed in one sample of a fast phase
            if phase[i] < target:
                i += 1
        else:
            i += 1
    return np.asarray(cuts)


def peak_cuts(x: np.ndarray, prominence: float, distance: int) -> np.ndarray:
    """Extremum-based segmentation (NOT the cut). Provided so studies can show
    where it disagrees with antipodal_cuts; results based on this alone say
    nothing about A3."""
    x = np.asarray(x, float)
    pk, _ = find_peaks(x, prominence=prominence, distance=distance)
    tr, _ = find_peaks(-x, prominence=prominence, distance=distance)
    return np.sort(np.concatenate([pk, tr]))


def occasions(x: np.ndarray, cuts: np.ndarray, sigma: float = 1.0):
    """Per-occasion (C, C*, S) between consecutive cuts."""
    out = []
    for a, b in zip(cuts[:-1], cuts[1:]):
        out.append(surplus(x[a:b + 1], sigma))
    return np.asarray(out)


# ---------------------------------------------------------------- regularity (H-L5)
def cv(v: np.ndarray) -> float:
    """Coefficient of variation, UNSIGNED by convention: the denominator is
    |mean(v)|, so a statistic whose mean is negative (or whose sign convention
    is flipped) gets the same CV as its negation. The CV must not depend on
    the sign convention of the trace. Needs len(v) >= 2 (ddof=1)."""
    v = np.asarray(v, float)
    return float(np.std(v, ddof=1) / abs(np.mean(v)))


def regularity(x: np.ndarray, events: np.ndarray, sigma: float = 1.0, dt: float = 1.0,
               n_boot: int = 2000, seed: int = 0, segment_end: str = "inclusive") -> dict:
    """H-L5 statistic with a paired bootstrap on CV(C) - CV(clock).

    events  sample indices of the system's own boundary events; raises
            ValueError below 3 events (2 occasions — the minimum the
            ddof=1 CVs need)
    segment_end  "inclusive" (default): occasion k is x[a:b+1], from event a
            to event b, so a jump located AT event b (an instantaneous
            reset, as in a threshold-reset neuron) is counted inside the
            arc of every occasion — a constant added to every C that lowers
            CV(C) by arithmetic. "exclusive": occasion k is x[a:b], from the
            sample at event a to the sample before event b, so the jump is
            the cut and not arc (A3: the cut has no content). Named in the
            prereg; a class that changes between the two is reported as such.
    Returns CVs for arc, clock, amplitude (control i), the mean arc per
    occasion in sigma (C_mean), identity-metric arc is the
    same as arc here (1-D; control ii applies in >1-D), and the paired
    bootstrap 95% CIs for both differences: cv_arc - cv_clock (the H-L5
    criterion) and cv_arc - cv_amp (the amplitude control, CRR.md [H-L5]
    control (i); on constant-period signals arc and peak-to-peak amplitude
    are proportional, so their CVs tie at instrument resolution and only a
    CI excluding 0 on the amplitude side is a match).
    For scoring across units/levels/subjects use sign_test_units (R6)."""
    x = np.asarray(x, float)
    events = np.asarray(events)
    if len(events) < 3:
        raise ValueError("regularity needs >= 3 events (>= 2 occasions)")
    if segment_end not in ("inclusive", "exclusive"):
        raise ValueError(segment_end)
    C, T, A = [], [], []
    for a, b in zip(events[:-1], events[1:]):
        seg = x[a:b + 1] if segment_end == "inclusive" else x[a:b]
        C.append(arc_length(seg, sigma))
        T.append((b - a) * dt)
        A.append(np.ptp(seg) / sigma)
    C, T, A = map(np.asarray, (C, T, A))
    rng = np.random.default_rng(seed)
    diffs = []
    amp_diffs = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(C), len(C))
        diffs.append(cv(C[idx]) - cv(T[idx]))
        amp_diffs.append(cv(C[idx]) - cv(A[idx]))
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    alo, ahi = np.percentile(amp_diffs, [2.5, 97.5])
    return dict(n=len(C), C_mean=float(C.mean()), cv_arc=cv(C), cv_clock=cv(T), cv_amp=cv(A),
                diff=cv(C) - cv(T), ci95=(float(lo), float(hi)),
                diff_amp=cv(C) - cv(A), ci95_amp=(float(alo), float(ahi)))


# ---------------------------------------------------------------- learners (D6)
def kl_step(p_old: np.ndarray, p_new: np.ndarray) -> float:
    """mean_probe KL(p_old || p_new) for categorical predictive distributions (N, K).

    Rows are renormalised after clipping so the inputs are proper
    distributions again; the clip only guards the log against zeros."""
    p_old = np.clip(p_old, 1e-12, 1); p_new = np.clip(p_new, 1e-12, 1)
    p_old = p_old / p_old.sum(axis=1, keepdims=True)
    p_new = p_new / p_new.sum(axis=1, keepdims=True)
    return float(np.mean(np.sum(p_old * (np.log(p_old) - np.log(p_new)), axis=1)))


def kl_gauss(mu_old: np.ndarray, mu_new: np.ndarray, var: float = 1.0) -> float:
    """mean_probe KL(N(mu_old, var) || N(mu_new, var)) for fixed-variance Gaussian
    predictives (N,) — the predictive family of a regression model. Here
    sqrt(2 KL) equals the Fisher–Rao distance exactly (SCOPE.md P8)."""
    mu_old = np.asarray(mu_old, float); mu_new = np.asarray(mu_new, float)
    return float(np.mean((mu_old - mu_new) ** 2) / (2.0 * var))


def path_length(snapshots: list[np.ndarray], kl=kl_step) -> dict:
    """C = sum_t sqrt(2 KL_t), E = KL(p_0 || p_T), C* = sqrt(2E), S = C - C*.

    snapshots  per-step predictive distributions on ONE fixed probe set;
               raises ValueError below 2 snapshots (there is no KL step)
    kl         kl_step (categorical, (N,K)) or kl_gauss (regression, (N,));
               named in the prereg
    S may be negative here: sqrt(2 KL) is the FR length only to second order
    (exactly for kl_gauss), so P1 is not guaranteed and the sign distribution
    must be reported (CLAUDE.md §3.1 item 5)."""
    if len(snapshots) < 2:
        raise ValueError("path_length needs >= 2 snapshots (>= 1 KL step)")
    steps = [np.sqrt(2 * kl(a, b)) for a, b in zip(snapshots[:-1], snapshots[1:])]
    C = float(np.sum(steps))
    E = kl(snapshots[0], snapshots[-1])
    Cs = float(np.sqrt(2 * E))
    return dict(C=C, E=E, Cstar=Cs, S=C - Cs)


def sign_test_units(unit_stats: list[dict]) -> tuple[float, float]:
    """Cross-unit scoring for H-L5 (R6): per-unit first, then an exact sign test.

    unit_stats  one regularity() dict per unit (subject/level/seed)
    Returns (fraction of units with cv_arc < cv_clock, exact two-sided
    binomial sign-test p under the null 'no direction'). A pooled verdict
    alone can hide per-unit failures (the median trap R6 forbids); score
    per unit and report both numbers."""
    if not unit_stats:
        raise ValueError("sign_test_units needs at least one unit")
    wins = [u["cv_arc"] < u["cv_clock"] for u in unit_stats]
    k = int(np.sum(wins)); n = len(wins)
    return k / n, float(binomtest(k, n, 0.5, alternative="two-sided").pvalue)


# ---------------------------------------------------------------- rate carriers (SCOPE.md P6, P9)
def poisson_transform(lam: np.ndarray) -> np.ndarray:
    """y = 2*sqrt(lam): on a Poisson-rate carrier the Fisher-Rao arc of lam(t) equals the
    total variation of y (P6, P9). Feeding y to arc_length / regularity with the identity
    metric IS the Fisher-Rao arc of the rate. lam must be >= 0 (counts or rates)."""
    lam = np.asarray(lam, float)
    if np.any(lam < 0):
        raise ValueError("poisson_transform needs a non-negative rate")
    return 2.0 * np.sqrt(lam)


def onset_events(cases: np.ndarray, rise_factor: float = 2.0, floor_frac: float = 0.25,
                 min_cases: float = 20.0, min_gap: int = 20) -> np.ndarray:
    """Epidemic onsets — the system's own boundary events on a count series.

    One onset per peak-recession-rise. Since the last onset let M = max(cases) at index
    t_M and m = min(cases) over the samples AFTER t_M (the recession). An onset fires at
    the first t with
        cases[t] >= rise_factor * m,   m <= floor_frac * M   (the epidemic has receded),
        cases[t] >= min_cases,         t - last_onset >= min_gap.
    Before the first onset, M and m are taken over the samples seen so far in the same
    way. No smoothing, no peak finder; every constant is a named parameter to be listed
    in the prereg and swept in the sensitivity table. Returns sample indices."""
    c = np.asarray(cases, float)
    ev = []
    last = 0; M = c[0]; t_M = 0; m = np.inf
    for t in range(1, len(c)):
        if c[t - 1] >= M:
            M = c[t - 1]; t_M = t - 1; m = np.inf          # new peak: the recession restarts
        else:
            m = min(m, c[t - 1])
        if (t - last >= min_gap and np.isfinite(m) and c[t] >= min_cases
                and c[t] >= rise_factor * m and m <= floor_frac * M):
            ev.append(t); last = t; M = c[t]; t_M = t; m = np.inf
    return np.asarray(ev, int)
