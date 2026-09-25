"""Headroom calibration for Declaration 2 (Amendment 1): baselines only (B0 fine-tune, F FOREVER, B1 ER-mix), calibration
seed 999, which is not a scored seed. Run after the declared generator showed no headroom on a seed-0 smoke run; its
output chose the generator constants of Amendment 1. No CRR arm is run here."""
import comparative as c

VARIANTS = [("declared generator", dict(NOISE_SD=1.0, MEAN_SD=1.5, DRIFT_SD=1.5, CONFLICT=False, BUF_PER=50, R_EV=10)),
            ("variant 1", dict(NOISE_SD=2.0, MEAN_SD=1.0, DRIFT_SD=0.7, CONFLICT=True, BUF_PER=20, R_EV=5)),
            ("variant 2", dict(NOISE_SD=2.5, MEAN_SD=1.0, DRIFT_SD=0.5, CONFLICT=True, BUF_PER=10, R_EV=5)),
            ("variant 3 (chosen)", dict(NOISE_SD=2.0, MEAN_SD=1.0, DRIFT_SD=1.0, CONFLICT=False, BUF_PER=10, R_EV=5))]
print("Headroom calibration, seed 999 (not scored), beta_base 1e-3, baselines only: OP / BWT")
for name, v in VARIANTS:
    for k, x in v.items(): setattr(c, k, x)
    print(f"{name}: {v}")
    worlds = list(c.WORLDS) if name == "declared generator" else ["W1 base", "W5 convex", "W6 class-incremental"]
    for w in worlds:
        out = []
        for arm in ("B0 fine-tune", "F FOREVER", "B1 ER-mix"):
            r = c.run(w, 999, arm, 1e-3); out.append(f"{arm.split()[0]} {r['op']:.1f}/{r['bwt']:.1f}")
        print(f"   {w} | " + " ; ".join(out))
