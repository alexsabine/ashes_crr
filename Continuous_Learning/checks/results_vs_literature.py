"""Our continual-learning accuracies beside the floors and baselines that the published benchmarks use (prompt-log entry 177).

Reads the pinned per-run records of EQ2, EQ3, EQ4 (runs/eq*/results_*.jsonl), SEC1 (runs/sec1/results_*.jsonl) and SCL3
(runs/scl3/results_*.jsonl). No new run; no verdict. Every number printed here is a mean over the pinned seeds of the
registered primary cell (smooth 0.9, cap 1e4, hidden 256, 3 epochs, lr 0.05, batch 10, the 'std' regime, no operator).

Reference quantities, computed from each carrier's own class counts (stored in task order by the scorers):
- last-task floor: the test share of the last task's classes, in percent. A class-incremental learner that has kept only
  the last task, and knows it perfectly, scores exactly this. The published class-IL benchmarks report the plain
  fine-tuned network ("None", "SGD") at this floor on Split MNIST.
- majority: the test share of the largest class (predicting it always).
- chance: 100 / K.
Arms (means over seeds; the tuned lambda is the best fixed weight on the coarse grid, in sample, as every scorer tunes it):
- EWC 0.1: the smallest fixed EWC weight on the grid (the nearest arm to plain fine-tuning; there is no lambda = 0 arm).
- EWC tuned; the rule (Omega = 1, mode 'eq'); Bayes (Laplace 1/2); SEC (the calibrated Laplace weight, SEC1/SCL3 only).
- replay family (EQ2-EQ4 only): ER (best fixed replay weight), DER++ (best fixed alpha); and LwF (best fixed weight).
"""
import glob
import json
import pathlib

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
PRIMARY = dict(smooth=0.9, wcap=10000.0, hidden=256, epochs=3, lr=0.05, bs=10)


def load(path):
    rows = [json.loads(line) for line in open(path)]
    return rows[0], rows[1:]


def primary(r):
    return all(r.get(k, v) == v for k, v in PRIMARY.items()) and r.get("regime", "std") == "std" and r.get("world") in (None, "none") \
        and r.get("fs", 0.1) == 0.1 and r.get("fe", 0.1) == 0.1


def mean_acc(rows, **sel):
    a = [r["acc"] for r in rows if all(r.get(k) == v for k, v in sel.items()) and primary(r)]
    return (float(np.mean(a)), len(a)) if a else (float("nan"), 0)


def best_fixed(rows, **sel):
    vals = sorted(set(r["value"] for r in rows if r.get("mode") == "fixed" and all(r.get(k) == v for k, v in sel.items()) and primary(r)))
    best = (float("nan"), None)
    for v in vals:
        m, n = mean_acc(rows, mode="fixed", value=v, **sel)
        if n and (best[1] is None or m > best[0]): best = (m, v)
    return best


def step_of(rows, lam, **sel):
    """The protocol's resolvable step: max(1.0 point, 2 standard errors of the tuned arm) (Continuous_Learning §6.2)."""
    a = np.array([r["acc"] for r in rows if r.get("mode") == "fixed" and r.get("value") == lam and all(r.get(k) == v for k, v in sel.items()) and primary(r)])
    return max(1.0, 2 * a.std(ddof=1) / np.sqrt(len(a))) if len(a) > 1 else float("nan")


def floors(h):
    K = int(h["K"]); pt = int(h["per_task"])
    # EQ2's records carry no class counts; its three carriers are balanced in the files (mfeat_*: 200 per class; texture:
    # 500 per class, 5500 rows over 11 classes with one class dropped), so n / K per class is used there
    cc = np.array(h["class_counts"], float) if "class_counts" in h else np.full(K, h["n"] / K)
    return 100 * cc[-pt:].sum() / cc.sum(), 100 * cc.max() / cc.sum(), 100.0 / K, K // pt


def fmt(x):
    return "   n/a" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:6.2f}"


def main():
    print("Our class-incremental accuracies beside the published benchmarks' reference points (means over seeds, primary cell; no verdict)")
    print("columns: K tasks | last-task floor | majority | chance || EWC 0.1 | EWC tuned (lambda) | rule O=1 | Bayes | SEC || ER best | DER++ best | LwF best"
          " || rule - floor | ER best - rule")
    summary = []
    for study, pat in (("EQ2", "runs/eq2/results_*.jsonl"), ("EQ3", "runs/eq3/results_*.jsonl"), ("EQ4", "runs/eq4/results_*.jsonl"),
                       ("SEC1", "runs/sec1/results_*.jsonl"), ("SCL3", "runs/scl3/results_*.jsonl")):
        print(f"\n== {study}")
        for f in sorted(glob.glob(str(ROOT / pat))):
            h, rows = load(f)
            if h.get("excluded"): print(f"   {h['dataset']}: excluded by the class rule"); continue
            fl, maj, ch, T = floors(h)
            if study in ("SEC1", "SCL3"):
                ewc01 = mean_acc(rows, mode="fixed", value=0.1)[0]; tuned, lam = best_fixed(rows)
                rule = mean_acc(rows, mode="eq", value=1.0)[0]; bayes = mean_acc(rows, mode="bayes")[0]; sec = mean_acc(rows, mode="bayes_sec", value=0.0)[0]
                er = der = lwf = agem = gnorm = mega = float("nan"); step = step_of(rows, lam)
            else:
                ewc01 = mean_acc(rows, method="ewc", mode="fixed", value=0.1)[0]; tuned, lam = best_fixed(rows, method="ewc")
                rule = mean_acc(rows, method="ewc", mode="eq", value=1.0)[0]; bayes = mean_acc(rows, method="ewc", mode="bayes")[0]; sec = float("nan")
                er = best_fixed(rows, method="er")[0]; der = best_fixed(rows, method="derpp")[0]; lwf = best_fixed(rows, method="lwf")[0]
                agem = mean_acc(rows, method="ewc", mode="agem")[0]; gnorm = mean_acc(rows, method="ewc", mode="gradnorm")[0]
                mega = mean_acc(rows, method="ewc", mode="mega")[0]; step = step_of(rows, lam, method="ewc")
            lam_s = f"{lam:g}" if lam is not None else "n/a"
            print(f"   {h['dataset']}: K {h['K']} T {T} | {fl:6.2f} | {maj:6.2f} | {ch:6.2f} || {fmt(ewc01)} | {fmt(tuned)} ({lam_s}) | {fmt(rule)} | {fmt(bayes)} | {fmt(sec)}"
                  f" || {fmt(er)} | {fmt(der)} | {fmt(lwf)} || {fmt(rule - fl)} | {fmt(er - rule)}")
            inert = (tuned - ewc01) <= step
            print(f"      step {step:.2f}; tuned - EWC 0.1 {tuned - ewc01:.2f} -> {'INERT (tuning lambda moves nothing beyond a step)' if inert else 'load-bearing'}"
                  + ("" if np.isnan(agem) else f"; published weight-setting rules run here: A-GEM {agem:.2f}, GradNorm {gnorm:.2f}, MEGA-I {mega:.2f}"))
            summary.append(dict(study=study, ds=h["dataset"], fl=fl, ch=ch, ewc01=ewc01, tuned=tuned, rule=rule, bayes=bayes, sec=sec, er=er, der=der,
                                lwf=lwf, agem=agem, gnorm=gnorm, mega=mega, step=step, inert=inert))
    S = summary; n = len(S)
    print("\n== Summary over all carriers and studies (a carrier scored in two studies counts twice)")
    reg = [s for s in S if not np.isnan(s["er"])]
    print(f"   carriers with a replay arm (EQ2-EQ4): {len(reg)}; ER best ahead of the rule on {sum(s['er'] > s['rule'] for s in reg)}; "
          f"median (ER best - rule) {np.median([s['er'] - s['rule'] for s in reg]):.2f}; median (DER++ best - rule) {np.median([s['der'] - s['rule'] for s in reg]):.2f}")
    print(f"   rule within 5 points of its last-task floor on {sum(s['rule'] - s['fl'] < 5 for s in S)} of {n}; below the floor on {sum(s['rule'] < s['fl'] for s in S)}")
    print(f"   EWC tuned within 5 points of the floor on {sum(s['tuned'] - s['fl'] < 5 for s in S)} of {n}; "
          f"EWC tuned - EWC 0.1: median {np.median([s['tuned'] - s['ewc01'] for s in S]):.2f}, max {max(s['tuned'] - s['ewc01'] for s in S):.2f}")
    print(f"   rule - EWC 0.1: median {np.median([s['rule'] - s['ewc01'] for s in S]):.2f}; rule - EWC tuned: median {np.median([s['rule'] - s['tuned'] for s in S]):.2f}")
    print(f"   LwF best ahead of EWC tuned on {sum(s['lwf'] > s['tuned'] for s in reg)} of {len(reg)} (the published class-IL ordering: LwF above the regularisers)")
    print(f"   rule ahead of A-GEM on {sum(s['rule'] > s['agem'] for s in reg)}, of GradNorm on {sum(s['rule'] > s['gnorm'] for s in reg)}, of MEGA-I on {sum(s['rule'] > s['mega'] for s in reg)} (of {len(reg)})")
    ine = [s for s in S if s["inert"]]
    print(f"   INERT carriers (EWC tuned within a step of EWC 0.1): {len(ine)} of {n}: " + ", ".join(f"{s['study']}/{s['ds']}" for s in ine))
    sc = [s for s in S if not np.isnan(s["sec"])]
    print(f"   SEC carriers: {len(sc)}; SEC - floor median {np.median([s['sec'] - s['fl'] for s in sc]):.2f}; SEC within 5 points of the floor on {sum(s['sec'] - s['fl'] < 5 for s in sc)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
