"""EXPLORATORY development run of the EQ4 scorer on the six SEEN EQ3 carriers (2026-09-22, prompt-log entry 74).
Purpose: choose the EQ-B clip constant kappa and check that the poisoned regime separates the registered rule from
EQ-B on real carriers, BEFORE the EQ4 prereg is hashed. These carriers are seen (data/SEEN.md); nothing here is
evidence or a ledger row; the prereg names this run as where kappa was learned (R3), and the held-out study runs on
other carriers on a later calendar day.
    uv run python studies/eq4/dev_seen.py <carrier>          # writes runs/eq4_dev/results_<carrier>.jsonl
    uv run python studies/eq4/dev_seen.py summary            # reads every results file, prints the comparison
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eq4_score as E  # noqa: E402

K_SEEN = {"mfeat_factors": 10, "mfeat_morphological": 10, "led7": 10, "led24": 10, "krkopt": 10, "fars": 8}
KAPPAS = (2.0, 4.0, 8.0)
OUT = E.ROOT / "runs" / "eq4_dev"


def main(name):
    X, y, meta = E.load_pmlb(name, K_SEEN[name]); K = meta["classes_used"]
    data = E.split_standardise(X, y, K)
    with open(OUT / f"results_{name}.jsonl", "w") as out:
        print(json.dumps(dict(dataset=name, exploratory=True, seen=True, **meta, K=K, per_task=2, kappas=KAPPAS)), file=out, flush=True)
        arms = [("ewc", "fixed", w, "std", E.KAPPA) for w in E.EWC_COARSE] + [("ewc", "eq", 1.0, "std", E.KAPPA)]
        arms += [("ewc", "eqb", 1.0, "std", k) for k in KAPPAS]
        arms += [("ewc", "fixed", w, "poison", E.KAPPA) for w in E.EWC_COARSE]
        arms += [("ewc", "fixedclip", w, "poison", k) for k in KAPPAS[:2] for w in E.EWC_COARSE]
        arms += [("ewc", "eq", 1.0, "poison", E.KAPPA)] + [("ewc", "eqb", 1.0, "poison", k) for k in KAPPAS]
        for method, mode, value, regime, kappa in arms:
            for seed in E.SEEDS:
                o = E.run(method, mode, value, seed, *data, K, 2, kappa=kappa, poison=(regime == "poison"))
                o["dataset"] = name; o["regime"] = regime; print(json.dumps(o), file=out, flush=True)


def summary():
    rows = []
    for p in sorted(OUT.glob("results_*.jsonl")):
        rows += [json.loads(l) for l in open(p) if l.startswith("{") and '"acc"' in l]
    ds = sorted(set(r["dataset"] for r in rows))

    def A(d, mode, value, regime, kappa, field="acc"):
        v = sorted([r for r in rows if r["dataset"] == d and r["mode"] == mode and abs(r["value"] - value) < 1e-6 and r["regime"] == regime and r["kappa"] == kappa], key=lambda r: r["seed"])
        assert len(v) == 5, (d, mode, value, regime, kappa, len(v)); return np.array([r[field] for r in v], float)

    print("EXPLORATORY (seen carriers; no verdict): EQ-B kappa choice and the poisoned regime")
    for d in ds:
        g = {w: A(d, "fixed", w, "std", E.KAPPA) for w in E.EWC_COARSE}; tuned = max(g, key=lambda w: g[w].mean()); tv = g[tuned]; step = E.step_of_public(tv)
        eq = A(d, "eq", 1.0, "std", E.KAPPA)
        line = f"[{d}] step {step:.2f}; tuned lambda {tuned:g}: {tv.mean():.2f}; rule Ω=1: {eq.mean():.2f} ({eq.mean()-tv.mean():+.2f})"
        for k in KAPPAS:
            b = A(d, "eqb", 1.0, "std", k); cf = A(d, "eqb", 1.0, "std", k, "clip_frac")
            line += f" | EQ-B k={k:g}: {b.mean():.2f} ({b.mean()-tv.mean():+.2f}; clip {cf.mean():.3f})"
        print(line)
        gp = {w: A(d, "fixed", w, "poison", E.KAPPA) for w in E.EWC_COARSE}; tp = max(gp, key=lambda w: gp[w].mean())
        eqp = A(d, "eq", 1.0, "poison", E.KAPPA); fin = A(d, "eq", 1.0, "poison", E.KAPPA, "finite"); wmax = A(d, "eq", 1.0, "poison", E.KAPPA, "w_max")
        line = f"   POISON: fixed tuned {tp:g}: {gp[tp].mean():.2f}; rule Ω=1: {eqp.mean():.2f} (finite {int(fin.sum())}/5, max w median {np.median(wmax):.3g})"
        for k in KAPPAS[:2]:
            gc = {w: A(d, "fixedclip", w, "poison", k) for w in E.EWC_COARSE}; tc = max(gc, key=lambda w: gc[w].mean())
            line += f" | fixed+clip k={k:g} tuned {tc:g}: {gc[tc].mean():.2f}"
        for k in KAPPAS:
            b = A(d, "eqb", 1.0, "poison", k); cf = A(d, "eqb", 1.0, "poison", k, "clip_frac")
            line += f" | EQ-B k={k:g}: {b.mean():.2f} (rule − EQ-B {eqp.mean()-b.mean():+.2f}; clip {cf.mean():.3f})"
        print(line)


if __name__ == "__main__":
    summary() if sys.argv[1] == "summary" else main(sys.argv[1])
