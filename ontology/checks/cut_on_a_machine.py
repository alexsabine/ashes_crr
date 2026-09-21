"""Why the cut carries content when it is computed: five small facts about boundaries in finite arithmetic
(ontology/06_cut_as_content.md; owner request 2026-09-21, prompt-log entry 65). Every number that folder quotes about
machines, grids and cuts is printed here. Deterministic, no data, no dependence on the batteries. Run:
uv run python ontology/checks/cut_on_a_machine.py
"""
import math
from fractions import Fraction

import numpy as np
from scipy.signal import hilbert

from crr.instrument.core import antipodal_cuts, cv, intrinsic_phase


def fact_1_measure_of_a_point():
    print("[1] A point on a grid is a cell: the measure of one sample is 1/n of the record, never zero")
    for n in (100, 1000, 100000):
        print(f"     n = {n:6d} samples: measure of one sample = {1.0 / n:.2e} of the record; a cut placed at a sample owns that share")


def fact_2_dedekind_and_ulp():
    print("[2] A Dedekind cut has no member of its own, yet it is the number; on a machine the cut has a width")
    r2 = math.sqrt(2.0)
    for D in (10, 100, 1000):
        lower = max(Fraction(p, q) for q in range(1, D + 1) for p in range(0, 2 * q + 1) if Fraction(p, q) ** 2 < 2)
        upper = min(Fraction(p, q) for q in range(1, D + 1) for p in range(0, 2 * q + 1) if Fraction(p, q) ** 2 > 2)
        print(f"     rationals with denominator <= {D:4d}: nearest below sqrt 2 = {lower} = {float(lower):.6f}, nearest above = {upper} = {float(upper):.6f}, gap {float(upper - lower):.2e}; no rational squares to 2 (the cut is empty of rationals)")
    print(f"     float64: spacing (ulp) at 1.0 = {np.spacing(1.0):.3e}, at sqrt 2 = {np.spacing(r2):.3e}, at 1e6 = {np.spacing(1e6):.3e}: the finest cut a float can make has this width, and sqrt 2 in float64 is {r2!r} exactly, a rational")


def fact_3_delta_mass():
    print("[3] A delta has zero support and unit mass: on a grid it is one cell of height 1/dx, and it still integrates to 1")
    for n in (10, 100, 1000):
        x = np.linspace(-1, 1, n + 1); dx = x[1] - x[0]
        d = np.zeros_like(x); d[n // 2] = 1.0 / dx
        print(f"     n = {n:5d}: cell width {dx:.4f}, delta height {1.0 / dx:.1f}, integral (rectangle rule) = {float(np.sum(d) * dx):.6f}, support = one cell of width {dx:.4f}")


def fact_4_reset_jump():
    print("[4] A reset located at the cut is a finite displacement with no duration: counted as arc it is content, and a constant content lowers CV(arc) by arithmetic")
    rng = np.random.default_rng(0)
    rises = rng.normal(1.0, 0.2, 2000)
    jump = 1.0
    print(f"     2000 occasions, rise ~ N(1, 0.2), reset jump {jump:g} at every cut: CV(rise) = {cv(rises):.4f}; CV(rise + jump) = {cv(rises + jump):.4f}; ratio {cv(rises + jump) / cv(rises):.4f} (closed form 1/(1 + jump/mean rise) = {1 / (1 + jump / rises.mean()):.4f})")
    jumps = rng.normal(1.0, 0.2, 2000)
    print(f"     with a jump that varies like the rise (independent, same CV): CV(rise + jump) = {cv(rises + jumps):.4f} (a constant at the cut regularises; a variable one does not)")


def fact_5_nonlocal_phase():
    print("[5] The analytic-signal phase is a functional of the whole record: what the future does changes the phase before it, most at the nearest samples and less with distance (the Hilbert kernel 1/(pi t) has no compact support); a section computed from the settled samples alone is unchanged")
    n = 2000; k_ = np.arange(n)                                  # 40 samples per cycle, 20 per half-turn, 50 cycles
    x = np.sin(2 * math.pi * k_ / 40.0)
    def section(z):  # upward crossings of the known level 0: computable from the settled samples alone (a record mean would itself be two-sided)
        return np.flatnonzero((z[:-1] < 0) & (z[1:] >= 0)) + 1
    ph_x = intrinsic_phase(x); cuts_x = antipodal_cuts(ph_x); sx = section(x)
    for b in (1210, 1200):                                       # b = 1210 sits inside a cycle; b = 1200 is a cycle boundary of the periodic (FFT) transform
        alterations = {
            "future removed (record truncated at b, the causal reading)": x[:b].copy(),
            "future scaled by 3 (same phase)": np.where(k_ >= b, 3.0 * x, x),
            "future shifted by a quarter turn (same amplitude)": np.where(k_ >= b, np.sin(2 * math.pi * k_ / 40.0 + math.pi / 2), x),
        }
        print(f"     the future altered from sample {b} onward ({'inside a cycle' if b % 40 else 'at a cycle boundary, where the periodic transform sees no edge'}):")
        for name, y in alterations.items():
            ph_y = intrinsic_phase(y); cuts_y = antipodal_cuts(ph_y); sy = section(y)
            parts = [f"{d}: {abs(ph_y[b - d] - ph_x[b - d]) / math.pi:.4f}" for d in (1, 5, 20, 40, 100, 500)]
            last_x = int(cuts_x[cuts_x < b][-1]); cy = cuts_y[cuts_y < b]; last_y = int(cy[-1]) if len(cy) else -1
            same_sections = bool(np.array_equal(sx[sx < b - 1], sy[sy < b - 1]))
            print(f"        {name}: phase change (half-turns) at 1, 5, 20, 40, 100, 500 samples before: " + ", ".join(parts) + f"; last cut before b: sample {last_x} -> {last_y} ({last_y - last_x:+d}); section crossings before b {'identical' if same_sections else 'changed'}")


def main():
    print("The cut on a machine: five facts (ontology/06_cut_as_content.md). Deterministic; every number the folder quotes about grids, floats, deltas, resets and non-local phase is printed here.")
    print()
    fact_1_measure_of_a_point(); print()
    fact_2_dedekind_and_ulp(); print()
    fact_3_delta_mass(); print()
    fact_4_reset_jump(); print()
    fact_5_nonlocal_phase()


if __name__ == "__main__":
    main()
