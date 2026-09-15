"""Gate contracts (#3): every control verdict, the zero-violation GATE OPEN
run via main(), the violation flag on inverted controls, and battery
determinism (R9). Pins the MUST_FAIL/MUST_PASS contracts of
src/crr/surrogates/gate.py."""
import io
from contextlib import redirect_stdout

import numpy as np
import pytest

from crr.surrogates import battery, gate
from crr.surrogates.battery import (S_A1_fm_sine, S_A2_am_sine, S_A_sine,
                                    S_E_asymmetric, S_F_duffing, S_F_roessler,
                                    S_F_vanderpol, S_G2_relaxation_arc_regular,
                                    S_G_relaxation, S_H2_wear_learner,
                                    S_H_convex_learner)


def _passes(gate_fn, gen):
    x, ev, meta = gen()
    out = gate_fn(x, ev, meta)
    assert out is not None, f"{meta['name']}: gate returned n/a (row not scored)"
    return out[0]


def _row(name):
    for g in battery.BATTERY:
        if g()[2]["name"] == name:
            return g
    raise AssertionError(f"no battery row named {name!r}")


# --- gate_L5 control verdicts -------------------------------------------------

def test_gate_L5_negative_controls_fail():
    assert _passes(gate.gate_L5, S_A_sine) is False
    assert _passes(gate.gate_L5, S_A2_am_sine) is False
    assert _passes(gate.gate_L5, S_G_relaxation) is False


def test_gate_L5_positive_controls_pass():
    assert _passes(gate.gate_L5, S_A1_fm_sine) is True
    assert _passes(gate.gate_L5, S_G2_relaxation_arc_regular) is True


# --- gate_CUT control verdicts ------------------------------------------------

def test_gate_CUT_negative_controls_fail():
    assert _passes(gate.gate_CUT, S_A_sine) is False
    assert _passes(gate.gate_CUT, S_F_vanderpol) is False  # mu=5.0
    assert _passes(gate.gate_CUT, _row("S-F van der Pol mu=1.0")) is False


def test_gate_CUT_positive_control_passes():
    assert _passes(gate.gate_CUT, S_E_asymmetric) is True


# --- gate_T1 control verdicts -------------------------------------------------

def test_gate_T1_negative_control_fails():
    runs, _, _ = S_H_convex_learner()
    out = gate.gate_T1(runs, None, {})
    assert out is not None
    assert out[0] is False


def test_gate_T1_positive_control_passes():
    runs, _, _ = S_H2_wear_learner()
    out = gate.gate_T1(runs, None, {})
    assert out is not None
    assert out[0] is True


def test_gate_T1_reports_lr_partial_r2():
    runs, _, _ = S_H2_wear_learner()
    _, detail = gate.gate_T1(runs, None, {})
    assert "partial-R2(+lr)" in detail


# --- main(): zero-violation GATE OPEN -----------------------------------------

def _run_main(hyp):
    buf = io.StringIO()
    with redirect_stdout(buf):
        bad = gate.main(hyp)
    return bad, buf.getvalue()


@pytest.mark.parametrize("hyp", ["L5", "CUT", "T1"])
def test_gate_open_with_no_violations(hyp):
    bad, out = _run_main(hyp)
    assert bad == 0
    assert "GATE OPEN" in out
    assert "VIOLATION" not in out


# --- violation flagging on inverted synthetic controls ------------------------

def test_main_flags_inverted_negative_control(monkeypatch):
    # Invert the contract: the S-A' FM sine POSITIVE control is listed as a
    # negative one. main() must flag the row and close the gate.
    monkeypatch.setitem(gate.MUST_FAIL, "L5", {"S-A' FM sine (constant amplitude)"})
    monkeypatch.setitem(gate.MUST_PASS, "L5", set())
    bad, out = _run_main("L5")
    assert bad >= 1
    assert "VIOLATION" in out
    assert "GATE CLOSED" in out
    assert "S-A' FM sine (constant amplitude)" in out


# --- battery registrations ----------------------------------------------------

def test_battery_rows_registered_with_parameter_names():
    names = [g()[2]["name"] for g in battery.BATTERY]
    for lam in ("0.0", "0.25", "0.5", "1.0"):
        assert f"S-C lobed ramp (lambda={lam})" in names
    for r in ("5.0", "10.0", "20.0", "40.0", "80.0"):
        assert f"S-D sine + white noise (rho~{r})" in names
    assert "S-F van der Pol mu=1.0" in names
    assert "S-F van der Pol mu=5.0" in names
    assert any("Rossler" in n for n in names)
    assert any("Duffing" in n for n in names)


# --- battery determinism (R9) -------------------------------------------------

def test_battery_deterministic_on_rerun():
    for gen in (S_A1_fm_sine, S_F_vanderpol, S_F_roessler, S_F_duffing):
        x1, ev1, m1 = gen()
        x2, ev2, m2 = gen()
        assert m1["name"] == m2["name"]
        assert np.array_equal(x1, x2)
        assert np.array_equal(ev1, ev2)
