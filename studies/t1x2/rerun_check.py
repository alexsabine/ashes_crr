"""R9 byte-identity check for study T1x2: one run per carrier (const, lr 0.01, seed 0) run twice through the
FROZEN scorer's run(); the two JSON records must be byte-identical (cmp). Writes runs/t1x2/rerun_<carrier>_{a,b}.json.
    uv run python studies/t1x2/rerun_check.py"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "runs" / "t1x2" / "frozen"))
import t1x2_score as B  # noqa: E402

bad = 0
for name in B.DATASETS:
    X, y, _ = B.load_pmlb_regression(name); tasks = B.make_tasks(X, y); base = B.train_base(tasks, X.shape[1]); fisher = base.per_sample_sq_grad(tasks[0][0], tasks[0][1])
    outs = []
    for tag in ("a", "b"):
        o = B.run("const", 0.01, 0, tasks, base, fisher); o["dataset"] = name
        p = ROOT / "runs" / "t1x2" / f"rerun_{name}_{tag}.json"; p.write_text(json.dumps(o, sort_keys=True) + "\n"); outs.append(p.read_bytes())
    same = outs[0] == outs[1]; bad += int(not same)
    print(f"{name}: rerun byte-identical {same}")
print("all byte-identical" if bad == 0 else f"{bad} carrier(s) differ")
sys.exit(1 if bad else 0)
