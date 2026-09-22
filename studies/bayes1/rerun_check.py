"""R9 byte-identity check for study BAYES-1: one arm per carrier (the rule at Omega = 1, c = 1, seed 0) run twice through the
FROZEN scorer's run(); the two JSON records must be byte-identical (cmp). Writes runs/bayes1/rerun_<carrier>_{a,b}.json.
    uv run python studies/bayes1/rerun_check.py"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "runs" / "bayes1" / "frozen"))
import bayes1_score as B  # noqa: E402

bad = 0
for name in B.DATASETS:
    X, y, _ = B.load_pmlb_regression(name); chunks = B.make_stream(X, y); posts = B.exact_posteriors(chunks); lr = B.learning_rate(chunks)
    outs = []
    for tag in ("a", "b"):
        o = B.run("eq", 1.0, 1.0, 0, chunks, posts, lr); o["dataset"] = name
        p = ROOT / "runs" / "bayes1" / f"rerun_{name}_{tag}.json"; p.write_text(json.dumps(o, sort_keys=True) + "\n"); outs.append(p.read_bytes())
    same = outs[0] == outs[1]; bad += int(not same)
    print(f"{name}: rerun byte-identical {same}")
print("all byte-identical" if bad == 0 else f"{bad} carrier(s) differ")
sys.exit(1 if bad else 0)
