"""Surrogate battery: synthetic signals with NO CRR content.

Every hypothesis must FAIL on the surrogates theory/CRR.md names for it before
it may enter a pre-registration (CLAUDE.md rule R4). Generators are
deterministic given `seed`. Each returns (x, events, meta) where `events` are
the sample indices of the signal's own boundary events (or None).
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp


def _cycles(periods, shape, amps=None):
    amps = np.ones(len(periods)) if amps is None else amps
    xs, ev, pos = [], [0], 0
    for p, a in zip(periods, amps):
        u = np.linspace(0, 2 * np.pi, int(p), endpoint=False)
        xs.append(a * shape(u)); pos += int(p); ev.append(pos)
    return np.concatenate(xs), np.asarray(ev[:-1])


def S_A_sine(n=60, period=100, seed=0):
    return _cycles(np.full(n, period), np.sin) + ({"name": "S-A sine"},)


def S_A1_fm_sine(n=60, seed=0, jitter=0.2):
    rng = np.random.default_rng(seed)
    p = rng.uniform(100 * (1 - jitter), 100 * (1 + jitter), n)
    return _cycles(p, np.sin) + ({"name": "S-A' FM sine (constant amplitude)"},)


def S_A2_am_sine(n=60, seed=0, jitter=0.3):
    rng = np.random.default_rng(seed)
    a = rng.uniform(1 - jitter, 1 + jitter, n)
    return _cycles(np.full(n, 100), np.sin, a) + ({"name": "S-A'' AM sine (constant period)"},)


def S_A3_amfm_sine(n=60, seed=0):
    rng = np.random.default_rng(seed)
    p = rng.uniform(80, 120, n); a = rng.uniform(0.7, 1.3, n)
    return _cycles(p, np.sin, a) + ({"name": "S-A''' AM+FM sine"},)


def S_B_sine_bump(n=60, seed=0, bump=0.15):
    rng = np.random.default_rng(seed)
    p = rng.uniform(90, 110, n); a = rng.uniform(0.9, 1.1, n)
    def shape(u):  # bump on the descent
        return np.sin(u) + bump * np.exp(-((u - 4.2) ** 2) / 0.08)
    return _cycles(p, shape, a) + ({"name": "S-B sine + dicrotic bump"},)


def S_C_lobed_ramp(n=60, seed=0, lam=1.0):
    rng = np.random.default_rng(seed)
    p = rng.uniform(90, 110, n); a = rng.uniform(0.9, 1.1, n)
    def shape(u):
        ramp = u / (2 * np.pi)
        lobes = lam * (0.3 * np.sin(np.clip(u * 3, 0, np.pi)) ** 2 + 0.2 * np.sin(np.clip((u - 2) * 3, 0, np.pi)) ** 2)
        return ramp + lobes
    return _cycles(p, shape, a) + ({"name": f"S-C lobed ramp (lambda={lam})"},)


def S_D_noisy_sine(n=60, seed=0, rho=20.0):
    rng = np.random.default_rng(seed)
    x, ev = _cycles(np.full(n, 100), np.sin)
    return x + rng.standard_normal(len(x)) * (2.0 / rho), ev, {"name": f"S-D sine + white noise (rho~{rho})"}


def S_E_asymmetric(n=60, seed=0):
    rng = np.random.default_rng(seed)
    p = rng.uniform(90, 110, n); a = rng.uniform(0.9, 1.1, n)
    return _cycles(p, lambda u: np.sin(u) + 1.2 * np.sin(2 * u) + 0.6 * np.sin(3 * u), a) + ({"name": "S-E asymmetric multi-harmonic"},)


def S_F_vanderpol(mu=5.0, T=400.0, dt=0.05, seed=0):
    f = lambda t, y: [y[1], mu * (1 - y[0] ** 2) * y[1] - y[0]]
    sol = solve_ivp(f, (0, T), [2.0, 0.0], t_eval=np.arange(0, T, dt), rtol=1e-8, atol=1e-10)
    x = sol.y[0][int(50 / dt):]
    # events: upward zero crossings
    ev = np.where((x[:-1] < 0) & (x[1:] >= 0))[0]
    return x, ev, {"name": f"S-F van der Pol mu={mu}"}


def S_G_relaxation(n=60, seed=0, thresh_cv=0.15):
    """Integrate-and-fire with clock-regular firing by construction: the threshold
    is drawn per cycle but the *time* to reach it is fixed; amplitude varies."""
    rng = np.random.default_rng(seed)
    T = 100
    xs, ev, pos = [], [0], 0
    for _ in range(n):
        thr = 1.0 * rng.normal(1, thresh_cv)
        ramp = np.linspace(0, thr, T, endpoint=False)
        xs.append(ramp); pos += T; ev.append(pos)
    return np.concatenate(xs), np.asarray(ev[:-1]), {"name": "S-G relaxation osc. (clock-regular, amplitude-variable)"}


def S_G2_relaxation_arc_regular(n=60, seed=0, rate_cv=0.15):
    """Fixed threshold, variable charging rate: arc constant, clock variable."""
    rng = np.random.default_rng(seed)
    xs, ev, pos = [], [0], 0
    for _ in range(n):
        T = int(100 * rng.normal(1, rate_cv))
        xs.append(np.linspace(0, 1.0, T, endpoint=False)); pos += T; ev.append(pos)
    return np.concatenate(xs), np.asarray(ev[:-1]), {"name": "S-G2 relaxation osc. (arc-regular by construction)"}


BATTERY = [S_A_sine, S_A1_fm_sine, S_A2_am_sine, S_A3_amfm_sine, S_B_sine_bump,
           S_C_lobed_ramp, S_D_noisy_sine, S_E_asymmetric, S_F_vanderpol,
           S_G_relaxation, S_G2_relaxation_arc_regular]
