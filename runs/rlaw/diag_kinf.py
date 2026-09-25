"""RLAW post-hoc diagnostic (not a verdict; AGENT_LOG 129): the frozen K(v) returns NaN at v = inf.

The frozen moments estimator (rlaw_lib.mom_v) returns v = inf when the lag-1 autocovariance of the first differences is
non-negative (no measurement-noise component). K(inf) should be its limit, 1; the frozen K evaluates inf*(inf-inf) = NaN,
and logerr() then counts the unit outside every band, and the tracking Spearman sees a NaN. This touches only the cells
where alpha* = K(v) is taken on the instrument unit (own:off) with the moments estimator (v:mom). This script imports the
frozen scorer unchanged, counts the v = inf units per cell, and re-scores those cells with K(inf) = 1. It changes no
frozen file and no registered verdict: the ledger rows are the frozen scorer's."""
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "frozen"))
import rlaw_score as S  # noqa: E402

K0 = S.K


def K_limit(v):
    v = np.asarray(v, float); return np.where(np.isinf(v), 1.0, K0(np.where(np.isinf(v), 0.0, v)))


def main():
    raw = pathlib.Path("data/raw/rlaw"); table = S.rate_table()
    cells = [c for c in S.CELLS if c["vest"] == "mom"]
    print("RLAW diagnostic: units with v = inf under the moments estimator, and the mom cells re-scored with K(inf) = 1")
    for dom, builder, tracking in S.DOMAINS:
        if dom == "twostep": continue  # the two-step domain does not use mom_v (its 'v' factor is the alpha grid)
        for c in cells:
            S.K = K0; recs = S.measure(builder(raw, c), c, table)
            used = [r for r in recs if r["excluded"] is None]
            ninf = sum(1 for r in used if np.isinf(r["v"])); nnan = sum(1 for r in used if not np.isfinite(r["alpha_star"]))
            v0 = S.verdicts(recs, dom, tracking)
            S.K = K_limit; recs2 = S.measure(builder(raw, c), c, table); v1 = S.verdicts(recs2, dom, tracking); S.K = K0
            keys = ["row", "level", "baseline"] + (["tracking"] if tracking else [])
            ch = [k for k in keys if v0[k] != v1[k]]
            print(f"{S.ROW[dom]} {S.cell_name(c)}: units {len(used)}, v=inf {ninf}, alpha* non-finite {nnan}; "
                  f"frozen within x2 {v0['within_x2']} -> K(inf)=1 {v1['within_x2']}; "
                  + "; ".join(f"{k} {v0[k]}->{v1[k]}" for k in keys) + f"; verdicts changed: {', '.join(ch) if ch else 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
