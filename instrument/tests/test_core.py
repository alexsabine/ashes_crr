import numpy as np
import pytest

from instrument.core import (antipodal_cuts, arc_length, chord, intrinsic_phase, occasions,
                             path_length, peak_cuts, regularity, surplus, unit_sigma)


def test_surplus_nonnegative_and_zero_iff_monotone():
    rng = np.random.default_rng(1)
    for _ in range(200):
        x = np.cumsum(rng.standard_normal(40))
        C, Cs, S = surplus(x)
        assert S >= -1e-12
    mono = np.sort(rng.standard_normal(40))
    assert abs(surplus(mono)[2]) < 1e-12


def test_arc_is_real_valued_not_floored():
    x = np.linspace(0, 0.9, 10)
    C, Cs, S = surplus(x, sigma=1.0)
    assert abs(C - 0.9) < 1e-12 and abs(S) < 1e-12  # an integer counter would give C=0, S=-0.9


def test_unit_rejects_degenerate_and_has_no_floor():
    with pytest.raises(ValueError):
        unit_sigma(np.ones(50))
    with pytest.raises(ValueError):
        unit_sigma(np.linspace(0, 1, 50) + 1e-6 * np.sin(np.arange(50)), min_sigma=1e-3)


def test_antipodal_cut_is_half_turn_on_a_sine():
    t = np.linspace(0, 20 * np.pi, 4000)
    x = np.sin(t)
    ph = intrinsic_phase(x)
    cuts = antipodal_cuts(ph, start=100)
    spacing = np.diff(ph[cuts])
    assert np.allclose(spacing, np.pi, atol=0.02)


def test_antipodal_and_peak_cuts_disagree_on_asymmetric_waveform():
    t = np.linspace(0, 20 * np.pi, 8000)
    x = np.sin(t) + 1.2 * np.sin(2 * t) + 0.6 * np.sin(3 * t)
    ph = intrinsic_phase(x)
    a = antipodal_cuts(ph, start=200)
    p = peak_cuts(x, prominence=0.3, distance=50)
    # nearest-peak distance from each antipodal cut, in samples: must not all coincide
    d = np.array([np.min(np.abs(p - c)) for c in a[1:]])
    assert np.median(d) > 20  # a symmetric sine gives ~0


def test_regularity_fm_sine_passes_trivially_documenting_the_gate():
    # constant amplitude, jittered period -> arc constant, clock varies: H-L5 "passes" for no reason
    rng = np.random.default_rng(0)
    periods = rng.uniform(80, 120, 60).astype(int)
    x = np.concatenate([np.sin(np.linspace(0, 2 * np.pi, p, endpoint=False)) for p in periods])
    ev = np.cumsum(np.r_[0, periods[:-1]])
    r = regularity(x, ev)
    assert r["cv_arc"] < 0.02 and r["cv_clock"] > 0.05


def test_path_length_dominates_endpoint():
    rng = np.random.default_rng(2)
    snaps = []
    logits = rng.standard_normal((64, 5))
    for _ in range(30):
        logits = logits + 0.3 * rng.standard_normal((64, 5))
        p = np.exp(logits); p /= p.sum(1, keepdims=True)
        snaps.append(p)
    r = path_length(snaps)
    assert r["C"] >= r["Cstar"] - 1e-9 and r["S"] > 0
