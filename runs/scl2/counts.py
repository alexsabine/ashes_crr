"""SCL2 derived counts and ranges quoted in the ledger rows and report (written after scoring, 2026-09-24; AGENT_LOG 105). It
reads runs/scl2/results_*.jsonl and prints numbers the frozen scorer's lines imply but do not print as counts, plus the
per-group accuracies of the forced-reset arm on every scored carrier (the scorer prints them only where resets were ahead);
it changes no verdict. Run: uv run python runs/scl2/counts.py > runs/scl2/counts.txt"""
import json, math
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[2]
ALL = ("allhyper", "allrep", "car_evaluation", "nursery", "wine_quality_red", "analcatdata_authorship", "analcatdata_dmft",
       "analcatdata_germangss", "collins", "soybean", "vehicle")
rows = []; hdr = {}
for d in ALL:
    for l in open(ROOT / "runs" / "scl2" / f"results_{d}.jsonl"):
        o = json.loads(l)
        if "arm" in o: rows.append(o)
        else: hdr[d] = o
DS = [d for d in ALL if not hdr[d]["excluded"]]; N = len(DS)
EWC = sorted({float(r["arm"].split("|")[1]) for r in rows if r["arm"].startswith("fixed|")})
def A(d, arm): return sorted([r for r in rows if r["dataset"] == d and r["arm"] == arm], key=lambda r: r["seed"])
def v(d, arm, k="acc"): return np.array([r[k] for r in A(d, arm)], dtype=float)
def m(d, arm, k): return float(v(d, arm, k).mean())
def step(x): return max(1.0, 2 * float(np.std(x, ddof=1)) / math.sqrt(len(x)))
def lab(x): return "AHEAD" if x.mean() >= step(x) else ("BEHIND" if x.mean() <= -step(x) else "TIE")
print("SCL2 derived counts and ranges (runs/scl2/counts.py)")
print(f"carriers scored {N} of {len(ALL)}; excluded {[d for d in ALL if hdr[d]['excluded']]}; tasks per carrier (K/2): "
      + ", ".join(f"{d}:{hdr[d]['classes_used'] // 2}" for d in DS))
print(f"SCL2-1: disables 0 in {sum(r['disables'] == 0 for d in DS for r in A(d, 'nat_eq'))}/{5 * N} runs; identical parameters "
      f"{sum(r['theta_sha'] == b['theta_sha'] for d in DS for r, b in zip(A(d, 'nat_eq'), A(d, 'base_eq')))}/{5 * N}; with SEC "
      f"{sum(r['theta_sha'] == b['theta_sha'] and r['disables'] == 0 for d in DS for r, b in zip(A(d, 'nat_bsec'), A(d, 'base_bsec')))}/{5 * N}")
for a in ("clock", "occasion", "egoic", "taskself"):
    sh = {d: m(d, a, "share") for d in DS}; lo = min(sh, key=sh.get); hi = max(sh, key=sh.get)
    print(f"SCL2-2 {a}: disable share min {sh[lo]:.3f} ({lo}), max {sh[hi]:.3f} ({hi}); below 0.05 on {[d for d in DS if sh[d] < 0.05]}")
for w in ("lossy", "restart"):
    sh = {d: m(d, f"nat_{w}", "share") for d in DS}; lo = min(sh, key=sh.get); hi = max(sh, key=sh.get)
    print(f"SCL2-3 natural {w}: disable share min {sh[lo]:.3f} ({lo}), max {sh[hi]:.3f} ({hi})")
for a in ("clock", "occasion"):
    dd = {d: m(d, a, "late_share") - m(d, "stat_" + a, "late_share") for d in DS}
    print(f"SCL2-D {a}: continual − stationary positive on {sum(x > 0 for x in dd.values())}/{N}; min {min(dd.values()):+.3f} ({min(dd, key=dd.get)}), max {max(dd.values()):+.3f} ({max(dd, key=dd.get)})")
ne = {d: v(d, "fc_wallclock") - v(d, "base_eq") for d in DS}
print(f"SCL2-E: parameters differ in {sum(r['theta_sha'] != b['theta_sha'] for d in DS for r, b in zip(A(d, 'fc_wallclock'), A(d, 'base_eq')))}/{5 * N} runs; "
      f"mean difference min {min(x.mean() for x in ne.values()):+.4f} ({min(ne, key=lambda d: ne[d].mean())}), max {max(x.mean() for x in ne.values()):+.4f} ({max(ne, key=lambda d: ne[d].mean())}); "
      f"TIE on {sum(lab(x) == 'TIE' for x in ne.values())}/{N}")
nf = {d: v(d, "fc_lossy") - v(d, "base_eq") for d in DS}
print(f"SCL2-F lossy: mean difference min {min(x.mean() for x in nf.values()):+.4f} ({min(nf, key=lambda d: nf[d].mean())}), max {max(x.mean() for x in nf.values()):+.4f} ({max(nf, key=lambda d: nf[d].mean())})")
for arm, name in (("fc_lossy", "SCL2-F lossy"), ("fc_restart", "SCL2-R restart P 0.02")):
    dd = {d: v(d, arm) - v(d, "base_eq") for d in DS}
    ahead = [d for d, x in dd.items() if lab(x) == "AHEAD"]; behind = [d for d, x in dd.items() if lab(x) == "BEHIND"]
    print(f"{name}: ahead of no operator by a step on {len(ahead)}/{N} {ahead}; behind on {len(behind)}/{N} {behind}; within a step on {N - len(ahead) - len(behind)}/{N}")
rs = {d: m(d, "fc_restart", "resets") for d in DS}
print(f"SCL2-R resets per run (mean over seeds): min {min(rs.values()):.1f} ({min(rs, key=rs.get)}), max {max(rs.values()):.1f} ({max(rs, key=rs.get)})")
print("SCL2-R per-group accuracy, forced resets − no operator (earlier tasks' classes | last task's classes), every scored carrier:")
for d in DS:
    do = v(d, "fc_restart", "acc_old") - v(d, "base_eq", "acc_old"); dl = v(d, "fc_restart", "acc_last") - v(d, "base_eq", "acc_last")
    print(f"   [{d}] no operator: old {m(d, 'base_eq', 'acc_old'):.4f}, last {m(d, 'base_eq', 'acc_last'):.4f}; resets: old {m(d, 'fc_restart', 'acc_old'):.4f}, last {m(d, 'fc_restart', 'acc_last'):.4f}; "
          f"difference old {do.mean():+.4f} (step {step(do):.2f}, {lab(do)}), last {dl.mean():+.4f} (step {step(dl):.2f}, {lab(dl)})")
t1 = {"AHEAD": [], "TIE": [], "BEHIND": []}; t2 = {"AHEAD": [], "TIE": [], "BEHIND": []}
for d in DS:
    g = {w: v(d, f"fixed|{w:g}") for w in EWC}; tuned = max(g, key=lambda w: g[w].mean())
    t1[lab(v(d, "fc_restart") - g[tuned])].append(d); t2[lab(v(d, "fc_restart") - v(d, "eq_1epoch"))].append(d)
print("SCL2-B resets − tuned fixed lambda: " + "; ".join(f"{k} {len(x)}/{N} {x}" for k, x in t1.items()))
print("SCL2-B resets − one-epoch learner: " + "; ".join(f"{k} {len(x)}/{N} {x}" for k, x in t2.items()))
for arm in ("nat_eq", "clock"):
    w_ = {d: m(d, arm, "wall") / m(d, arm, "updates") for d in DS}
    print(f"SCL2-O {arm}: wall steps per update min {min(w_.values()):.4f}, max {max(w_.values()):.4f} (ratio of means)")
