"""CRR instrument. Implements the definitions in theory/CRR.md.

Every function is pure, deterministic, and takes its constants as arguments
so that a pre-registration can name them. No integer step counting anywhere.
"""
from __future__ import annotations

import numpy as np
from scipy.signal import find_peaks, hilbert, savgol_filter


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
    """(C, C*, S) with S = C - C* >= 0 exactly (P1)."""
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
    nearest the interpolated crossing."""
    cuts = [start]
    target = phase[start] + half_turn
    i = start + 1
    n = len(phase)
    while i < n:
        if phase[i] >= target:
            # linear interpolation between i-1 and i
            p0, p1 = phase[i - 1], phase[i]
            frac = 0.0 if p1 == p0 else (target - p0) / (p1 - p0)
            cuts.append(int(round(i - 1 + frac)))
            target += half_turn
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
    v = np.asarray(v, float)
    return float(np.std(v, ddof=1) / np.mean(v))


def regularity(x: np.ndarray, events: np.ndarray, sigma: float = 1.0, dt: float = 1.0,
               n_boot: int = 2000, seed: int = 0) -> dict:
    """H-L5 statistic with a paired bootstrap on CV(C) - CV(clock).

    events  sample indices of the system's own boundary events
    Returns CVs for arc, clock, amplitude (control i), identity-metric arc is the
    same as arc here (1-D; control ii applies in >1-D), and the bootstrap CI.
    """
    x = np.asarray(x, float)
    C, T, A = [], [], []
    for a, b in zip(events[:-1], events[1:]):
        seg = x[a:b + 1]
        C.append(arc_length(seg, sigma))
        T.append((b - a) * dt)
        A.append(np.ptp(seg) / sigma)
    C, T, A = map(np.asarray, (C, T, A))
    rng = np.random.default_rng(seed)
    diffs = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(C), len(C))
        diffs.append(cv(C[idx]) - cv(T[idx]))
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return dict(n=len(C), cv_arc=cv(C), cv_clock=cv(T), cv_amp=cv(A),
                diff=cv(C) - cv(T), ci95=(float(lo), float(hi)))


# ---------------------------------------------------------------- learners (D6)
def kl_step(p_old: np.ndarray, p_new: np.ndarray) -> float:
    """mean_probe KL(p_old || p_new) for categorical predictive distributions (N, K)."""
    p_old = np.clip(p_old, 1e-12, 1); p_new = np.clip(p_new, 1e-12, 1)
    return float(np.mean(np.sum(p_old * (np.log(p_old) - np.log(p_new)), axis=1)))


def path_length(prob_snapshots: list[np.ndarray]) -> dict:
    """C = sum_t sqrt(2 KL_t), E = KL(p_0 || p_T), C* = sqrt(2E), S = C - C*."""
    steps = [np.sqrt(2 * kl_step(a, b)) for a, b in zip(prob_snapshots[:-1], prob_snapshots[1:])]
    C = float(np.sum(steps))
    E = kl_step(prob_snapshots[0], prob_snapshots[-1])
    Cs = float(np.sqrt(2 * E))
    return dict(C=C, E=E, Cstar=Cs, S=C - Cs)
