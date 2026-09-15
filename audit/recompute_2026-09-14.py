"""Recompute every number the 2026-09-14 ledger quotes from the raw jsonl in
archive/cl_ledger_2026-09-14/, and score each pre-registered line as written.

    uv run python audit/recompute_2026-09-14.py > audit/recompute_2026-09-14.txt

Rules applied (CLAUDE.md): R1 (a number exists only if a script prints it),
R6 (per-seed, not means alone; full precision at boundaries), R7 (the constant
a rule reduces to is reported). Nothing here touches data or re-runs a model;
it reads the archived outputs only. Exit code 0 always: this is a report.
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

A = Path(__file__).resolve().parent.parent / "archive" / "cl_ledger_2026-09-14"


def rows(name):
    out = []
    for line in (A / name).read_text().splitlines():
        line = line.strip()
        if line.startswith("{"):
            out.append(json.loads(line))
    return out


def cfg(r, *keys):
    return tuple(r.get(k) for k in keys)


KEYS = ("dataset", "method", "replay", "kind", "Om", "ratio", "metric", "smooth", "lr", "bs", "tasklen", "buf")


def group(rs):
    g = defaultdict(list)
    for r in rs:
        g[cfg(r, *KEYS)].append(r)
    return g


def acc(v, field="acc"):
    v = sorted(v, key=lambda r: r["seed"])
    return np.array([r[field] * 100 for r in v]), [r["seed"] for r in v]


def fmt(a):
    return f"{a.mean():.4f} (seeds {', '.join(f'{x:.2f}' for x in a)})"


def find(g, **kw):
    hits = [v for k, v in g.items() if all(dict(zip(KEYS, k)).get(a) == b for a, b in kw.items())]
    assert len(hits) == 1, (kw, len(hits))
    return hits[0]


print("=" * 100)
print("RECOMPUTE of archive/cl_ledger_2026-09-14 — equanimity (EQ) claims")
print("=" * 100)

eq3 = group(rows("results_eq3.jsonl"))
adv = group(rows("results_adv.jsonl"))
eq4 = group(rows("results_eq4.jsonl"))
t3 = group(rows("results_t3.jsonl"))
comp = group(rows("results_compute.jsonl"))

# ---------------------------------------------------------------- §3 landscapes
print("\n[§3] 'Ω = 1 is the sharp interior optimum in 6/6 landscapes; ±√2 costs 5–45 pts'")
print("     ratio=ema smooth=0.98 WCAP=50, standard stream, seeds 0–2; values = final acc %")
land_ok = 0
for ds in ("kmnist", "mnist", "fmnist"):
    for r in (0.1, 0.2):
        line = {}
        for om in (0.5, 0.71, 1.0, 1.41, 2.0):
            a, _ = acc(find(eq3, dataset=ds, method="eq", replay=r, kind="standard", Om=om, ratio="ema"))
            line[om] = a
        best = max(line, key=lambda o: line[o].mean())
        c1 = line[1.0].mean() - line[0.71].mean(); c2 = line[1.0].mean() - line[1.41].mean()
        wmed = [round(x["w_med"], 2) for x in sorted(find(eq3, dataset=ds, method="eq", replay=r, kind="standard", Om=1.0, ratio="ema"), key=lambda q: q["seed"])]
        ok = best == 1.0 and min(c1, c2) > 1.0
        land_ok += ok
        print(f"  {ds:7s} r={r}: " + "  ".join(f"Ω={o}:{line[o].mean():.2f}" for o in line)
              + f"  | best Ω={best}  cost(0.71)={c1:+.2f} cost(1.41)={c2:+.2f}  -> {'as claimed' if ok else 'NOT as claimed'}"
              + f"  | median w at Ω=1 per seed {wmed}")
print(f"  landscapes as claimed: {land_ok}/6")

# ---------------------------------------------------------------- §3 compute claim
print("\n[§3] 'r = 0.2 matches 100 % replay at 40 % less compute'  (EQ Ω=1 ema r=0.2 vs ER r=1.0)")
for ds in ("kmnist", "mnist", "fmnist"):
    e, _ = acc(find(eq3, dataset=ds, method="eq", replay=0.2, kind="standard", Om=1.0, ratio="ema"))
    er1, _ = acc(find(eq3, dataset=ds, method="er", replay=1.0, kind="standard"))
    er02, _ = acc(find(eq3, dataset=ds, method="er", replay=0.2, kind="standard"))
    ce = find(eq3, dataset=ds, method="eq", replay=0.2, kind="standard", Om=1.0, ratio="ema")[0]["compute_per_sample"]
    c1 = find(eq3, dataset=ds, method="er", replay=1.0, kind="standard")[0]["compute_per_sample"]
    print(f"  {ds:7s} EQ(0.2,Ω=1)={fmt(e)}  ER(1.0)={fmt(er1)}  ER(0.2)={fmt(er02)}  Δ(EQ−ER1.0)={e.mean()-er1.mean():+.2f}  compute {ce:.3f} vs {c1:.3f} ({100*(1-ce/c1):.0f}% less)")

# ---------------------------------------------------------------- §4 A1 reduction
print("\n[§4 A1] 'fixed w = 1 (61.4) within 1.0 of adaptive (62.5)' — KMNIST r=0.2, seeds 0–2")
e, s_e = acc(find(eq3, dataset="kmnist", method="eq", replay=0.2, kind="standard", Om=1.0, ratio="ema"))
fixed = {}
for w in (1.0, 2.0, 4.0, 8.0):
    fixed[w], _ = acc(find(adv, dataset="kmnist", method="eq", replay=0.2, kind="standard", Om=w, ratio="fixed"))
    print(f"  fixed w={w}: {fmt(fixed[w])}")
print(f"  adaptive Ω=1: {fmt(e)}")
d = e - fixed[1.0]
print(f"  adaptive − fixed(w=1): mean {d.mean():.4f}  per seed {[f'{x:+.2f}' for x in d]}")
print(f"  prereg A1: FAIL (adaptivity irrelevant) if some fixed w within 1.0 -> at full precision the gap is {d.mean():.4f},"
      f" i.e. {'WITHIN' if d.mean() <= 1.0 else 'NOT within'} 1.0; the ledger's '61.4 vs 62.5' rounds both sides and reads 1.1.")
print(f"  per-seed: {int((d <= 1.0).sum())}/3 seeds within 1.0; {int((d >= 1.0).sum())}/3 seeds ≥ 1.0  -> verdict FRAGILE at the boundary (R6)")
print(f"  ER-sum ≡ fixed w = 1 in this pipeline (g = g_stream_mean + 1·g_replay_mean). ER(r) in the same pipeline is the")
print(f"  concatenated-batch mean, i.e. fixed w = r with lr scaled by bs/(bs+rb): fixed w=0.2..0.5 was never run (results_adv2 lost).")
print(f"  Effective replay weight of the adaptive rule at Ω=1 (median w per seed): {[round(x['w_med'],2) for x in sorted(find(eq3, dataset='kmnist', method='eq', replay=0.2, kind='standard', Om=1.0, ratio='ema'), key=lambda q: q['seed'])]}")
print(f"  and at Ω=1.41: {[round(x['w_med'],2) for x in sorted(find(eq3, dataset='kmnist', method='eq', replay=0.2, kind='standard', Om=1.41, ratio='ema'), key=lambda q: q['seed'])]} (acc {fmt(acc(find(eq3, dataset='kmnist', method='eq', replay=0.2, kind='standard', Om=1.41, ratio='ema'))[0])}) vs fixed w=4: {fmt(fixed[4.0])}, w=2: {fmt(fixed[2.0])}")

# ---------------------------------------------------------------- §4 A2 MEGA
print("\n[§4 A2] loss-ratio balancing (MEGA-I) — KMNIST r=0.2")
for sm in (0.0, 0.98):
    m, _ = acc(find(adv, dataset="kmnist", method="eq", replay=0.2, kind="standard", Om=1.0, ratio="mega", smooth=sm))
    dd = e - m
    print(f"  MEGA smooth={sm}: {fmt(m)}   adaptive − MEGA: mean {dd.mean():+.2f} per seed {[f'{x:+.2f}' for x in dd]}  -> {'≥1.0 in ' + str(int((dd>=1).sum())) + '/3 seeds'}")

# ---------------------------------------------------------------- §4 A3 invariance
print("\n[§4 A3] optimum stays at Ω = 1 under lr ×¼, ×4 and batch 5, 20 (KMNIST r=0.2)")
for lab, kw in (("lr=0.0125", dict(lr=0.0125, bs=10)), ("lr=0.2", dict(lr=0.2, bs=10)), ("bs=5", dict(lr=0.05, bs=5)), ("bs=20", dict(lr=0.05, bs=20))):
    line = {}
    for om in (0.5, 0.71, 1.0, 1.41, 2.0):
        line[om], _ = acc(find(adv, dataset="kmnist", method="eq", replay=0.2, kind="standard", Om=om, ratio="ema", **kw))
    best = max(line, key=lambda o: line[o].mean())
    nb = sorted(line, key=lambda o: -line[o].mean())[1]
    print(f"  {lab:10s} " + "  ".join(f"Ω={o}:{line[o].mean():.2f}" for o in line) + f"  | best Ω={best}, runner-up Ω={nb} trails by {line[best].mean()-line[nb].mean():.2f}")

# ---------------------------------------------------------------- §4 metric
print("\n[§4] 'Euclidean norm gives the same optimum (62.1)' — KMNIST r=0.2 smooth=0.98")
for om in (0.71, 1.0, 1.41):
    a, _ = acc(find(eq4, dataset="kmnist", method="eq", replay=0.2, kind="standard", Om=om, ratio="ema", metric="euclid"))
    print(f"  euclid Ω={om}: {fmt(a)}")
print(f"  fisher Ω=1:   {fmt(e)}")

# ---------------------------------------------------------------- T3
print("\n[§5 T3] abundant memory (buffer 500 → 5000), KMNIST: final acc / last-task acc")
for lab, kw in (("ER(1.0)", dict(method="er", replay=1.0)), ("EQ(0.2,Ω=1 ema)", dict(method="eq", replay=0.2, Om=1.0, ratio="ema")), ("fixed w=1 (0.2)", dict(method="eq", replay=0.2, Om=1.0, ratio="fixed"))):
    a5, _ = acc(find(t3, dataset="kmnist", kind="standard", buf=500, **kw)); a50, _ = acc(find(t3, dataset="kmnist", kind="standard", buf=5000, **kw))
    l5, _ = acc(find(t3, dataset="kmnist", kind="standard", buf=500, **kw), "last_task_acc"); l50, _ = acc(find(t3, dataset="kmnist", kind="standard", buf=5000, **kw), "last_task_acc")
    print(f"  {lab:18s} acc {a5.mean():.2f} → {a50.mean():.2f}   last-task {l5.mean():.2f} → {l50.mean():.2f}  (Δ last-task {l50.mean()-l5.mean():+.2f}; per seed {[f'{x:+.1f}' for x in l50-l5]})")
print("  prereg T3: FAIL if EQ's last-task acc drops by > 2.0 or ER's does not drop.")

# ---------------------------------------------------------------- prereg-vs-run mismatch
print("\n[PREREG_equanimity.md vs run_eq*.sh] hypotheses as written vs what was run")
print("  Q1–Q4 are written for r = 0.05 with Ω ∈ {0.25, 0.5, 1, 2, 4}. run_eq.sh ran r ∈ {0.2, 0.5} with ratio=unbiased;")
print("  run_eq3.sh ran r ∈ {0.1, 0.2} with ratio=ema and a different Ω grid. No r = 0.05 EQ run exists in the bundle.")
print("  -> Q1, Q2, Q4 cannot be scored as pre-registered; the ledger's §3 scores a different design (labelled 'estimator")
print("     finalised post hoc on KMNIST seed 0'). Q3 (LM regime, r=0.05) was never run (LM EQ ran at r ∈ {0.1, 0.25}).")
un = group(rows("results_eq.jsonl"))
print("  results_eq.jsonl (ratio=unbiased, the first estimator), KMNIST standard:")
for r in (0.2, 0.5):
    line = {}
    for om in (0.25, 0.5, 1.0, 2.0, 4.0):
        line[om], _ = acc(find(un, dataset="kmnist", method="eq", replay=r, kind="standard", Om=om, ratio="unbiased"))
    print(f"    r={r}: " + "  ".join(f"Ω={o}:{line[o].mean():.2f}" for o in line))

# ---------------------------------------------------------------- T1 path length
print("\n[§5 T1] path length vs endpoint, lm/results_path.jsonl (n = 20, in-sample R² of log F as pre-registered)")
P = rows("lm/results_path.jsonl")
F = np.log(np.array([r["F"] for r in P]))
def r2(x, y):
    X = np.c_[np.ones(len(x)), x]; b = np.linalg.lstsq(X, y, rcond=None)[0]; res = y - X @ b
    return 1 - res @ res / ((y - y.mean()) @ (y - y.mean()))
for k in ("C_new", "C_old", "E_new", "E_old"):
    x = np.array([r[k] for r in P])
    print(f"  R²(log F ~ {k}) = {r2(x, F):.4f}   R²(log F ~ log {k}) = {r2(np.log(x), F):.4f}")
print("  ledger quotes 0.887 (C_new) / 0.901 (C_old) vs 0.756 (E_new); E_old was 'reported, not a candidate'.")
print("  Under the strengthened baseline (theory/SCOPE.md §4.1: E_old is a required endpoint predictor) the pass line")
print("  is R²(best C) ≥ R²(best E) + 0.05. See the numbers above. Also: lr is not controlled (5 lrs × 2 schedules × 2 seeds).")
lrs = sorted(set(r["lr"] for r in P))
print("  within-lr check (does path beat endpoint once lr is fixed? 4 runs per lr):")
for lr in lrs:
    sub = [r for r in P if r["lr"] == lr]
    f = np.array([r["F"] for r in sub])
    print(f"    lr={lr}: F={np.round(f,3).tolist()}  C_new={np.round([r['C_new'] for r in sub],2).tolist()}  E_new={np.round([r['E_new'] for r in sub],3).tolist()}  E_old={np.round([r['E_old'] for r in sub],3).tolist()}")

# ---------------------------------------------------------------- T2
print("\n[§5 T2] LM 4-domain stream, lm/results_t2.jsonl (seeds 0–1): D0 bpb (forgetting) / domain bpb (plasticity)")
T2 = rows("lm/results_t2.jsonl")
def mean_of(method, replay):
    v = [r for r in T2 if r["method"] == method and r["replay"] == replay]
    return np.mean([r["D0_bpb"] for r in v]), np.mean([r["dom_bpb"] for r in v]), [round(r["D0_bpb"], 3) for r in v]
for lab, m, r in (("ER(0.25)", "er", 0.25), ("ER(0.5)", "er", 0.5), ("EQ(0.1,Ω=1)", "eq", 0.1), ("EQ(0.25,Ω=1)", "eq", 0.25), ("KLrep(0.25,λ=10)", "klrep", 0.25)):
    d0, dm, per = mean_of(m, r)
    print(f"  {lab:18s} D0 {d0:.3f} (seeds {per})  dom {dm:.3f}")
d0_eq, _, _ = mean_of("eq", 0.25); d0_kl, _, _ = mean_of("klrep", 0.25)
print(f"  prereg T2 PASS line: EQ(0.25) within 0.03 bpb of KLrep(0.25) on D0 -> gap {d0_eq-d0_kl:+.3f}: {'PASS' if d0_eq-d0_kl <= 0.03 else 'FAIL as pre-registered'}")
print("  lm/results_t2b.jsonl holds four klrep rows for 'λ=1, λ=3' but the script does not print λ: the rows are attributable")
print("  only by run order (R1 violation: the ledger's λ=1 / λ=3 numbers are transcriptions).")
print("  No fixed-w or ER-sum arm exists in the LM regime: the reduction test cannot be scored there.")

# ---------------------------------------------------------------- hashes
print("\n[R2] pre-registration hashes: none of the five PREREG_*.md has a HASH.txt or .ots in the bundle ('sha256 in the shell logs').")
print("     Every archived row therefore carries prereg hash = 'not in bundle' and unseen = N (all datasets in data/SEEN.md).")
print("\n[§10] mlp_bench.py's docstring carries an 8 Sept results table (CRR-CLS 0.874 etc.) that no jsonl in the bundle reproduces.")
