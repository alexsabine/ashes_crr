"""Second follow-up (owner request, prompt-log entry 104): is the rule's SGD advantage at c = 16 a tuning-grid artefact?
adam_checks_2.txt [B3] shows the rule's derived weight settling between the grid-tuned lambda (0.03 at c = 16, 0.003 at
c = 256) and the edge; the tuning grid (theory/checks/omega_reprocessed.py GRID) has no point between 0.03 and 0.1.
Declared in Continuous_Learning/DECLARATION_ADAM_3.md before the first full run.

    [B4] The reduction test (CLAUDE.md section 6, EQ-1's logic): at each c, the fixed weight equal to the rule's median
         derived w (last 1000 steps, seed 0; smoothing 0 and 0.9) is run over the 5 seeds; REDUCES if its total is
         within 10 % of the rule's.
    [B5] A fine tuning grid: 60 log-spaced fixed weights from 1e-4 to 3 (the finite ones kept); the rule's total over the
         finely tuned fixed weight's. The rule is AHEAD if the ratio is below 0.9, TIES within 10 %, BEHIND above 1.1.
Every label is computed (R15). Run:
    uv run python Continuous_Learning/checks/adam_checks_3.py > Continuous_Learning/checks/adam_checks_3.txt
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "theory" / "checks"))
sys.path.insert(0, str(ROOT / "Continuous_Learning" / "checks"))
import adam_checks as ac  # noqa: E402
import adam_checks_2 as a2  # noqa: E402
import omega_sweeps as om  # noqa: E402

FINE = tuple(float(v) for v in np.logspace(-4, np.log10(3.0), 60))
TOL = ac.TOL


def main():
    H, F, a, b = om.make_model()
    print("Adam checks, second follow-up (Continuous_Learning/checks/adam_checks_3.py): the two-task quadratic, SGD; "
          f"fine grid {len(FINE)} log-spaced weights from {FINE[0]:g} to {FINE[-1]:g}")
    summary = []
    for c in ac.SCALES:
        Fc = c * F
        fine = [(lam, ac.ev("fixed", lam, H, Fc, a, b)) for lam in FINE]
        fin = [(lam, v) for lam, v in fine if np.isfinite(v)]
        best = min(fin, key=lambda t: t[1])
        print(f"[c = {c:g}] finely tuned fixed weight {best[0]:.5g}, total {best[1]:.4f} ({len(fin)} of {len(FINE)} weights finite)")
        for s in (0.0, 0.9):
            rule = a2.with_smooth(s, lambda: ac.ev("eq", 1.0, H, Fc, a, b))
            wmed = a2.median_w(H, Fc, a, b, s)
            fx = ac.ev("fixed", wmed, H, Fc, a, b)
            red = np.isfinite(fx) and abs(fx - rule) <= TOL * rule
            r = rule / best[1]
            lab = "AHEAD" if r < 1 - TOL else ("BEHIND" if r > 1 + TOL else "TIES")
            print(f"     smoothing {s:g}: rule {ac.f(rule)}; median derived w {wmed:.5g}; fixed at that w {ac.f(fx)} -> B4 {'REDUCES' if red else 'DOES NOT REDUCE'}; "
                  f"rule / finely tuned {r:.3f} -> B5 {lab}")
            summary.append(f"c={c:g} s={s:g}: {'REDUCES' if red else 'DOES NOT REDUCE'}, {lab}")
    print("summary: " + "; ".join(summary))


if __name__ == "__main__":
    main()
