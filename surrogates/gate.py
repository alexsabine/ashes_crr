"""Hypothesis gate (CLAUDE.md R4).

    uv run python surrogates/gate.py L5
    uv run python surrogates/gate.py CUT

Prints one row per surrogate: the statistic, PASS/FAIL under the candidate
criterion, and whether that outcome is the one theory/CRR.md requires. Commit
the output into prereg/<study>/gate_<hyp>.txt. A hypothesis whose row for a
"must fail" surrogate reads PASS may not enter a pre-registration.
"""
from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, ".")
from instrument.core import (antipodal_cuts, intrinsic_phase, peak_cuts, regularity,  # noqa: E402
                             unit_sigma)
from surrogates.battery import BATTERY  # noqa: E402

# Negative controls: the hypothesis MUST fail here (no CRR content, or nothing to distinguish).
MUST_FAIL = {
    "L5": {"S-A sine", "S-A'' AM sine (constant period)",
           "S-G relaxation osc. (clock-regular, amplitude-variable)"},
    "CUT": {"S-A sine", "S-F van der Pol mu=5.0"},
}
# Positive controls: the hypothesis is TRUE by construction here and MUST pass,
# otherwise the instrument cannot see it.
MUST_PASS = {
    "L5": {"S-A' FM sine (constant amplitude)", "S-G2 relaxation osc. (arc-regular by construction)"},
    "CUT": {"S-E asymmetric multi-harmonic"},
}


def gate_L5(x, ev, meta):
    """CV(arc) < CV(clock) with the amplitude control: a PASS requires the arc
    inequality to hold AND arc to beat the amplitude-only CV."""
    if ev is None or len(ev) < 12:
        return None
    seg_amp = np.array([np.ptp(x[a:b]) for a, b in zip(ev[:-1], ev[1:])])
    try:
        sig = unit_sigma(seg_amp[: len(seg_amp) // 2])
    except ValueError:
        sig = 1.0
    r = regularity(x, ev, sigma=sig)
    passes = (r["cv_arc"] < r["cv_clock"]) and (r["ci95"][1] < 0) and (r["cv_arc"] < r["cv_amp"])
    return passes, f"cv_arc={r['cv_arc']:.3f} cv_clock={r['cv_clock']:.3f} cv_amp={r['cv_amp']:.3f} ci={r['ci95'][0]:.3f},{r['ci95'][1]:.3f}"


def gate_CUT(x, ev, meta):
    """Testability of A3: do antipodal and dominant-extremum cuts disagree?
    Period is taken from the phase; peak detection uses one max + one min per
    cycle (distance = 0.4 period, prominence = 0.3 range), as a physiology
    pipeline would. Phase counting starts at the first detected peak, so on a
    symmetric cycle antipodes land on troughs and the two coincide -> FAIL."""
    ph = intrinsic_phase(x)
    period = 2 * np.pi / max(np.median(np.diff(ph)), 1e-9)
    p = peak_cuts(x, prominence=0.3 * np.ptp(x), distance=max(int(0.4 * period), 2))
    if len(p) < 5:
        return None
    a = antipodal_cuts(ph, start=int(p[1]))
    if len(a) < 5:
        return None
    d = np.array([np.min(np.abs(p - c)) for c in a[1:]])
    disagree = np.median(d) / (period / 2)
    return disagree > 0.05, f"median |antipode-extremum| = {disagree:.3f} half-turns"


GATES = {"L5": gate_L5, "CUT": gate_CUT}


def main(hyp: str):
    g = GATES[hyp]
    print(f"gate for {hyp}\n  must FAIL on {sorted(MUST_FAIL[hyp])}\n  must PASS on {sorted(MUST_PASS[hyp])}\n")
    bad = 0
    for gen in BATTERY:
        x, ev, meta = gen()
        out = g(x, ev, meta)
        name = meta["name"]
        if out is None:
            print(f"  {name:55s} n/a")
            continue
        passes, detail = out
        if name in MUST_FAIL[hyp]:
            ok = not passes; why = "passes on a negative control"
        elif name in MUST_PASS[hyp]:
            ok = passes; why = "fails on a positive control (instrument cannot see the effect)"
        else:
            ok = True; why = ""
        flag = "" if ok else f"   <-- VIOLATION: {why}"
        bad += (not ok)
        print(f"  {name:55s} {'PASS' if passes else 'FAIL':4s}  {detail}{flag}")
    print()
    print("GATE OPEN" if bad == 0 else f"GATE CLOSED ({bad} violation(s)): restate the hypothesis or add a control")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1]) else 0)
