"""RLAW summary of the per-unit distributions (reads runs/rlaw/results.json, written by the frozen scorer).

Prints, per domain row, the primary cell's per-unit distribution of the signed log ratio log(alpha_hat/alpha*): its
quantiles, how many units fall below / above alpha*, how many alpha_hat <= 0 (kept and counted outside every band, as
registered), and how many v fits sit at the grid edge (flagged and kept). No verdict is computed here; the verdicts are the
frozen scorer's (runs/rlaw/score.txt). Every per-unit value is printed in score.txt."""
import json
import math
import pathlib
import sys

import numpy as np


def main(path="runs/rlaw/results.json"):
    d = json.loads(pathlib.Path(path).read_text())
    print("RLAW per-unit distributions, primary cell (v:ml own:on lag:+0 alt:no)")
    for dom, r in d["domains"].items():
        used = [u for u in r["units"] if not u.get("excluded")]
        nexc = len(r["units"]) - len(used)
        a = np.array([u["alpha_hat"] for u in used], float); p = np.array([u["alpha_star"] for u in used], float)
        pos = (a > 0) & np.isfinite(a) & np.isfinite(p) & (p > 0)
        lr = np.log(a[pos] / p[pos])
        ek = "alpha_edge" if dom == "twostep" else "v_edge"; edge = sum(bool(u.get(ek)) for u in used)
        q = np.quantile(lr, [0, 0.25, 0.5, 0.75, 1]) if lr.size else [math.nan] * 5
        print(f"{r['row']} ({dom}): units {len(used)} (excluded {nexc}); alpha_hat <= 0: {int(np.sum(~(a > 0)))}; "
              f"{'alpha' if dom == 'twostep' else 'v'} at grid edge: {edge}; log(alpha_hat/alpha*) min {q[0]:.3f} q25 {q[1]:.3f} median {q[2]:.3f} q75 {q[3]:.3f} max {q[4]:.3f}; "
              f"alpha_hat below alpha* {int(np.sum(lr < 0))}, above {int(np.sum(lr > 0))}; within x2 {int(np.sum(np.abs(lr) <= math.log(2)))}; "
              f"median alpha_hat {np.median(a[a > 0]):.4f}, median alpha* {np.median(p):.4f}")
    print(f"RLAW-U: {d['RLAW-U']}")
    print(f"RLAW-C: {d['RLAW-C']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
