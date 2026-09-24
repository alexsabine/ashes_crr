"""P5 re-tested (POST HOC, Maps_and_Territories/DECLARATION_2.md, pushed in 2fc2c1d before this file existed).

- Fresh seeds 20-39.
- A's bias is compared with the erasure-corrected fixed point (1-e) gamma mu / (1 - (1-e) gamma).
- Everything else is imported unchanged from performativity.py (Declaration 1).

Run: uv run python Maps_and_Territories/checks/performativity_2.py > Maps_and_Territories/checks/performativity_2.txt"""
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from performativity import AGRID, BGRID, BURN, ERASE, run_arms, world  # noqa: E402

SEED_RANGE = range(20, 40)


def main():
    print("P5 re-tested, POST HOC (Declaration 2): fresh seeds 20-39; A's bias against the erasure-corrected fixed point; all else as Declaration 1")
    out = {}
    for kind in ("G+", "G-"):
        R = [run_arms(*world(kind, s)) for s in SEED_RANGE]; cfgC = R[0][1]
        rA = np.array([r[0]["A"][0] for r in R]); rB = np.array([r[0]["B"][0] for r in R]); rC = np.array([r[0]["C"][0] for r in R])
        iA = int(np.argmin(np.mean(np.where(np.isfinite(rA), rA, 1e300), axis=0))); iB = int(np.argmin(np.mean(rB, axis=0)))
        iC = int(np.argmin(np.mean(np.where(np.isfinite(rC), rC, 1e300), axis=0)))
        A, B, C = rA[:, iA], rB[:, iB], rC[:, iC]; ahead = int(np.sum(C <= 0.9 * B))
        biasA = np.array([r[0]["A"][1][iA] for r in R]); mus = np.array([np.mean(world(kind, s)[0][BURN:]) for s in SEED_RANGE])
        g, e = 0.5, ERASE; target = (1 - e) * g / (1 - (1 - e) * g)
        ratio = float(np.sum(biasA) / np.sum(target * mus))
        fmt = lambda x: f"{x:.4f}" if np.isfinite(x) and abs(x) < 1e6 else "diverged (> 1e6: the self-fulfilling spiral)"
        out[kind] = dict(ahead=ahead, ratio=ratio)
        print(f"   {kind}: tuned gains A alpha {float(AGRID[iA])}, B alpha {float(AGRID[iB])}, C (alpha, beta) ({float(cfgC[iC][0])}, {float(cfgC[iC][1])})")
        print(f"      RMSE of f - mu_t, median over seeds: A {fmt(np.median(A))}, B {fmt(np.median(B))}, C {fmt(np.median(C))}; C <= 0.9 B on {ahead}/20 seeds")
        print("      per seed C/B: " + " ".join(f"{c / b:.3f}" for c, b in zip(C, B)))
        print(f"      A's bias: pooled mean(f - mu) / mean(target mu), target (1-e)gamma/(1-(1-e)gamma) = {target:.4f}: {fmt(ratio)}")
    gp_c = out["G+"]["ahead"] >= 18; gp_a = abs(out["G+"]["ratio"] - 1) <= 0.1; gm = (20 - out["G-"]["ahead"]) >= 18
    print(f"   gate: G+ C ahead on >= 18/20: {'holds' if gp_c else 'FAILS'} ({out['G+']['ahead']}/20); G+ A's bias within 10 % of the corrected target: {'holds' if gp_a else 'FAILS'} "
          f"(ratio {out['G+']['ratio']:.4f}); G- C NOT ahead on >= 18/20: {'holds' if gm else 'FAILS'} ({20 - out['G-']['ahead']}/20)")
    print(f"summary: P5 (post hoc) {'GATE OPEN' if (gp_c and gp_a and gm) else 'GATE CLOSED'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
