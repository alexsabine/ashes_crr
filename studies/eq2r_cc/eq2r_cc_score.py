"""Study EQ2R-CC — compute-cost scoring layer over the EQ2R results (prereg/eq2r_cc/PREREG.md).

Question: does the normalised penalty step save compute? Not per step (it adds two vector norms and an
EMA to a fixed-lambda step: CC-1 checks the logged forward/backward passes are identical), but in the
tuning budget: a tuned lambda costs the whole grid, the rule costs one configuration (CC-2), and, on the
capacity x epochs array, whether the rule at one epoch reaches the tuned lambda at three (CC-3).

    uv run python studies/eq2r_cc/eq2r_cc_score.py <results.jsonl ...>

Reads the EQ2/EQ2R results files (fields: dataset, method, mode, value, seed, smooth, wcap, regime, acc,
fwd_bwd_per_sample, n_stream, hid, epochs). Every number printed is computed here.
"""
import json
import math
import sys

import numpy as np

SEEDS = (0, 1, 2, 3, 4); SMOOTH = 0.9; WCAP = 1e4; HID = 256; EPOCHS = 3
LAMBDA_DEFAULT = 30.0          # the best single lambda across EQ2's carriers (ledger EQ2-1); learned on EQ2, named here (R3)
BUDGET_RATIO = 0.1             # CC-2: the rule's tuning-inclusive compute must be <= this fraction of the tuned lambda's
ARRAY_CARRIER = "mfeat_karhunen"


def load(paths):
    rows = []
    for p in paths:
        for line in open(p):
            if line.startswith("{"):
                o = json.loads(line)
                if "acc" in o: rows.append(o)
    return rows


def sel(rows, name, method, mode, value=None, hid=HID, epochs=EPOCHS):
    v = [r for r in rows if r["dataset"] == name and r["method"] == method and r["mode"] == mode and r.get("regime", "std") == "std"
         and r["smooth"] == SMOOTH and r["wcap"] == WCAP and r.get("hid", HID) == hid and r.get("epochs", EPOCHS) == epochs
         and (value is None or abs(r["value"] - value) < 1e-6)]
    return sorted(v, key=lambda r: r["seed"])


def compute(runs):
    """Forward+backward sample passes summed over the runs (5 seeds of one configuration)."""
    return float(sum(r["fwd_bwd_per_sample"] * r["n_stream"] for r in runs))


def main(paths):
    rows = load(paths); ds = sorted(set(r["dataset"] for r in rows))
    print("=" * 112); print("EQ2R-CC compute-cost scoring — rows CC-1..3 as pre-registered in prereg/eq2r_cc/PREREG.md; per-seed values in brackets"); print("=" * 112)
    cc1_ok = True; cc2_parts = []; cc2_notbehind = {}; cc2_beats_default = {}; cc2_ratio = {}
    for d in ds:
        grid = {}
        for r in rows:
            if r["dataset"] == d and r["method"] == "ewc" and r["mode"] == "fixed" and r.get("regime", "std") == "std" and r.get("hid", HID) == HID and r.get("epochs", EPOCHS) == EPOCHS:
                grid.setdefault(round(r["value"], 6), []).append(r)
        grid = {w: sorted(v, key=lambda r: r["seed"]) for w, v in grid.items() if len(v) == len(SEEDS)}
        tuned = max(grid, key=lambda w: np.mean([r["acc"] for r in grid[w]])); tv = np.array([r["acc"] for r in grid[tuned]])
        se = tv.std(ddof=1) / math.sqrt(len(tv)); step = max(1.0, 2 * se)
        rule = sel(rows, d, "ewc", "eq", 1.0); rv = np.array([r["acc"] for r in rule])
        default = grid.get(round(LAMBDA_DEFAULT, 6)); dv = np.array([r["acc"] for r in default]) if default else None
        # CC-1: per-step compute identical (logged passes per sample equal seed by seed)
        eq_passes = all(abs(a["fwd_bwd_per_sample"] - b["fwd_bwd_per_sample"]) < 1e-12 for a, b in zip(rule, grid[tuned]))
        cc1_ok = cc1_ok and eq_passes
        print(f"\n[{d}] step = {step:.4f}; tuned lambda = {tuned:g} over {len(grid)} configurations")
        print(f"   CC-1 passes per stream sample: rule {rule[0]['fwd_bwd_per_sample']:.4f}, tuned lambda {grid[tuned][0]['fwd_bwd_per_sample']:.4f} -> {'identical' if eq_passes else 'DIFFER'}")
        # CC-2: tuning-inclusive compute
        c_tuned = sum(compute(v) for v in grid.values()); c_rule = compute(rule); ratio = c_rule / c_tuned; cc2_ratio[d] = ratio
        nb = (rv.mean() - tv.mean()) > -step; cc2_notbehind[d] = nb
        print(f"   CC-2 tuning-inclusive compute (sample passes): tuned lambda {c_tuned:.3e} over {len(grid)} configs, rule {c_rule:.3e} over 1 config, ratio {ratio:.4f} (budget <= {BUDGET_RATIO})")
        print(f"        accuracy: tuned {tv.mean():.4f} [{' '.join(f'{q:.2f}' for q in tv)}], rule {rv.mean():.4f} [{' '.join(f'{q:.2f}' for q in rv)}], rule - tuned {rv.mean() - tv.mean():+.4f} -> {'not behind' if nb else 'BEHIND by a step'}")
        if dv is not None:
            bd = (rv.mean() - dv.mean()) >= step; cc2_beats_default[d] = bd
            print(f"        default lambda = {LAMBDA_DEFAULT:g} (1 config, same compute as the rule): {dv.mean():.4f} [{' '.join(f'{q:.2f}' for q in dv)}], rule - default {rv.mean() - dv.mean():+.4f} -> {'rule ahead by a step' if bd else 'default suffices'}")
        else:
            print(f"        default lambda = {LAMBDA_DEFAULT:g} not on the grid for this carrier"); cc2_beats_default[d] = False
    n = len(ds); cc2 = all(cc2_notbehind.values()) and all(r <= BUDGET_RATIO for r in cc2_ratio.values()) and sum(cc2_beats_default.values()) * 3 >= 2 * n
    print("\n" + "-" * 112)
    print(f"CC-1 per-step compute: {'PASS (the rule adds no passes; only two norms and an EMA)' if cc1_ok else 'FAIL'}")
    print(f"CC-2 tuning compute: not behind on {sum(cc2_notbehind.values())}/{n} carriers; compute ratio <= {BUDGET_RATIO} on {sum(r <= BUDGET_RATIO for r in cc2_ratio.values())}/{n}; ahead of the default lambda by a step on {sum(cc2_beats_default.values())}/{n} (needs >= 2/3) -> {'PASS' if cc2 else 'FAIL'}"
          + ("" if sum(cc2_beats_default.values()) * 3 >= 2 * n else " (a transferred default lambda gives the saving without CRR)"))
    # CC-3: one epoch with the rule vs three epochs tuned, on the array carrier
    if ARRAY_CARRIER in ds:
        rows_a = [r for r in rows if r["dataset"] == ARRAY_CARRIER]
        grid3 = {}
        for r in rows_a:
            if r["method"] == "ewc" and r["mode"] == "fixed" and r.get("regime", "std") == "std" and r.get("hid", HID) == HID and r.get("epochs", EPOCHS) == EPOCHS:
                grid3.setdefault(round(r["value"], 6), []).append(r["acc"])
        tuned3 = max(grid3, key=lambda w: np.mean(grid3[w])); tv3 = np.array(grid3[tuned3]); step3 = max(1.0, 2 * tv3.std(ddof=1) / math.sqrt(len(tv3)))
        rule1 = sel(rows, ARRAY_CARRIER, "ewc", "eq", 1.0, hid=HID, epochs=1)
        if len(rule1) == len(SEEDS):
            r1 = np.array([r["acc"] for r in rule1]); c3 = compute(rule1) / sum(compute(sorted([r for r in rows_a if r["method"] == "ewc" and r["mode"] == "fixed" and r.get("regime", "std") == "std" and r.get("hid", HID) == HID and r.get("epochs", EPOCHS) == EPOCHS and abs(r["value"] - w) < 1e-6], key=lambda r: r["seed"])) for w in grid3)
            ok3 = (r1.mean() - tv3.mean()) > -step3
            print(f"CC-3 one epoch with the rule vs three epochs tuned on {ARRAY_CARRIER}: rule(1 epoch) {r1.mean():.4f} [{' '.join(f'{q:.2f}' for q in r1)}], tuned(3 epochs) {tv3.mean():.4f}, diff {r1.mean() - tv3.mean():+.4f} (step {step3:.2f}); compute ratio incl. tuning {c3:.4f} -> {'PASS' if ok3 else 'FAIL'}")
        else:
            print(f"CC-3: the epochs = 1 rule cell is not in these results (n/a on EQ2's files)")
    else:
        print("CC-3: array carrier not present (n/a)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
