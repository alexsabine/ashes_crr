"""Study SEC4 — a robust SEC: the secant-calibrated Laplace weight with a stability guard chosen on SEEN data, tested on a THIRD
unseen family (the pooled OpenML suites 14, 218, 379 and 457). Owner request: prompt-log entry 228; prereg/sec4/DEV_DECLARATION.md (the development stage) and
prereg/sec4/PREREG.md (the test).

WHAT IS FROZEN BESIDE THIS FILE (runs/sec4/frozen/): byte copies of runs/sec3/frozen/{sec1_score,scl2_score,scl3_score,sec3_score}.py.
This file adds only:
  (1) run_guard(): SEC1's run() for 'bayes_sec' with one of three guards (DEV_DECLARATION.md): 'raw' (SEC3's fallback),
      'clip' (per-coordinate clip of the importance at kappa / (lr w)), 'scale' (whole-importance rescale to margin kappa);
      below a guard's bound the code path is SEC1's (the identity D-ID);
  (2) dev(): the development stage on the 16 SEEN carriers (SCL3's 10, SEC3's 6), with the selection rule and D-GATE;
  (3) run_carrier() and score() for the test family: SEC1's run_all (every arm, unchanged) plus the chosen guard at the
      primary window, the retained window cells and the other two guards (reports), with CPU timing in a separate file.

    uv run python studies/sec4/sec4_score.py dev                # development on SEEN carriers (DEV_DECLARATION.md)
    uv run python studies/sec4/sec4_score.py all <OpenML id> [--out F]
    uv run python studies/sec4/sec4_score.py score <results.jsonl ...>
    uv run python studies/sec4/sec4_score.py check
    uv run python studies/sec4/sec4_score.py smokefull [--out F]
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np  # noqa: E402

_HERE = Path(__file__).resolve()
FROZEN = _HERE.parent.name == "frozen"
ROOT = _HERE.parents[3] if FROZEN else _HERE.parents[2]
sys.path.insert(0, str(_HERE.parent if FROZEN else ROOT / "runs" / "sec3" / "frozen"))
import sec3_score as P3  # noqa: E402  (SEC3's scorer: it loads SCL3's loader and SEC1's learner, and times every run)
L = P3.L; S = P3.S
S.run = P3._run                 # SEC4 times its own runs below; SEC1's run() is restored untouched

# ---------------------------------------------------------------- registered constants (DEV_DECLARATION.md, PREREG.md)
KAPPA = 0.5                      # the clip and rescale guards' margin: half the explicit-Euler stability edge
RAW_BOUND = 1.0                  # SEC3's fallback bound
VARIANTS = ("clip", "scale", "raw")                 # tie order of the selection rule
CHOSEN = "clip"                  # chosen by dev() on SEEN carriers (prereg/sec4/dev_SEC4.txt, D-GATE OPEN); the test's primary arm
KEEP_CELLS = P3.KEEP_CELLS; THREE = P3.THREE; SHARE = P3.SHARE; MIN_B = P3.MIN_B; SEEDS = S.SEEDS
DEV_SCL3 = dict(P3.SCL3_DATASETS); DEV_SEC3 = dict(P3.DATASETS)
DEV_EXCLUDED = {40685}           # shuttle: excluded in SEC3 (K 2)
DIVERGED = ("cnae-9", "dionis", "fabert")
MIN_N = 4                        # fewer scored carriers than this: SEC4-1 is NOT DECIDABLE (PREREG.md)
DIV_FRAC = 0.5                   # SEC4-2: a seed below this fraction of the tuned accuracy is a divergence
DATASETS = {46906: ('anneal', 4, 2), 1459: ('artificial-characters', 10, 2), 1466: ('cardiotocography', 10, 2), 23380: ('cjs', 6, 2),
            1476: ('gas-drift', 6, 2), 375: ('JapaneseVowels', 8, 2), 46980: ('MIC', 8, 2), 1491: ('one-hundred-plants-margin', 10, 2),
            377: ('synthetic_control', 6, 2)}   # OpenML id -> (name, K requested, classes per task): prereg/sec4/carrier_selection.txt
TIMES: list = []


def run_guard(seed, Xtr, ytr, Xte, yte, K, per_task, variant, fs=S.FS, fe=S.FE, kappa=KAPPA, raw_bound=RAW_BOUND,
              lr=S.LR, bs=S.BS, epochs=S.EPOCHS, hidden=S.HID):
    """SEC1's run() for 'bayes_sec' with a guard. variant 'none' is SEC1's bayes_sec exactly (D-ID)."""
    t0 = time.process_time()
    rng = np.random.default_rng(seed)
    d = Xtr.shape[1]; net = S.MLP(rng, d, K, h=hidden); n = net.flat().size
    tasks = [tuple(range(i, i + per_task)) for i in range(0, K, per_task)]
    imp_bayes = np.zeros(n); imp_bayes_raw = np.zeros(n); theta_star = None
    wlog = []; svals = []; n_fallback = 0; fired = 0; margins = []
    cap = kappa / (lr * S.BAYES_W)
    with np.errstate(all="ignore"):
        for ti, task in enumerate(tasks):
            ii_task = np.where(np.isin(ytr, task))[0]; n_task = len(ii_task)
            imp_used = imp_bayes / n_task
            if theta_star is not None and variant != "none":                                  # GUARD
                m = lr * S.BAYES_W * float(np.max(imp_used)); margins.append(m)
                if variant == "raw" and not (m < raw_bound):
                    imp_used = imp_bayes_raw / n_task; fired += 1
                elif variant == "clip" and not (m < kappa):
                    imp_used = np.minimum(imp_used, cap); fired += 1
                elif variant == "scale" and not (m < kappa):
                    imp_used = imp_used * (kappa / m); fired += 1
            total = epochs * int(math.ceil(n_task / bs)); n_s = max(1, int(math.ceil(fs * total))); n_e = max(1, int(math.ceil(fe * total)))
            s_th = np.zeros(n); s_g = np.zeros(n); e_th = np.zeros(n); e_g = np.zeros(n); k_step = 0
            for ep in range(epochs):
                perm = rng.permutation(ii_task)
                for t in range(0, len(perm), bs):
                    ii = perm[t:t + bs]; x, y = Xtr[ii], ytr[ii]
                    L_p, g_p = S.ce_loss_grad(net, x, y)
                    theta_before = net.flat()
                    if k_step < n_s: s_th += theta_before; s_g += g_p
                    if k_step >= total - n_e: e_th += theta_before; e_g += g_p
                    k_step += 1
                    if theta_star is None:
                        net.set_flat(theta_before - lr * g_p); continue
                    dth = theta_before - theta_star; g_q = 2 * imp_used * dth
                    w = S.BAYES_W
                    wlog.append(float(w))
                    net.set_flat(theta_before - lr * (g_p + w * g_q))
            theta_now = net.flat().copy()
            f = np.zeros(n)
            for _ in range(S.N_FISHER):
                ii = ii_task[rng.integers(0, len(ii_task), bs)]; f += S.ce_loss_grad(net, Xtr[ii], ytr[ii])[1] ** 2
            f_task = f / S.N_FISHER * bs
            dth = e_th / n_e - s_th / n_s; dg = e_g / n_e - s_g / n_s; nn = float(dth @ dth)
            c = float(dg @ dth) / nn if nn > S.DTH_FLOOR else float("nan"); rho = float((f_task * dth) @ dth) / nn if nn > S.DTH_FLOOR else float("nan")
            if nn > S.DTH_FLOOR and np.isfinite(c) and np.isfinite(rho) and c > 0 and rho > 0: s = c / rho
            else: s = 1.0; n_fallback += 1
            svals.append(float(s))
            imp_bayes = imp_bayes + n_task * s * f_task
            imp_bayes_raw = imp_bayes_raw + n_task * f_task
            theta_star = theta_now
    rec = dict(mode=f"bayes_sec_{variant}", value=float(kappa if variant in ("clip", "scale") else raw_bound), seed=int(seed), fs=float(fs), fe=float(fe),
               acc=100 * net.acc(Xte, yte), s=svals, n_fallback=int(n_fallback), guard_fired=int(fired), guard_margins=[round(x, 6) for x in margins],
               w_med=float(np.median(wlog)) if wlog else None, finite=bool(np.all(np.isfinite(net.flat()))))
    TIMES.append(dict(mode=rec["mode"], value=rec["value"], seed=rec["seed"], fs=rec["fs"], fe=rec["fe"], cpu_s=time.process_time() - t0))
    return rec


def _timed(*a, **k):
    t0 = time.process_time(); o = P3._run(*a, **k)
    TIMES.append(dict(mode=o["mode"], value=o["value"], seed=o["seed"], fs=o["fs"], fe=o["fe"], cpu_s=time.process_time() - t0))
    return o


# ---------------------------------------------------------------- development on SEEN carriers (DEV_DECLARATION.md)
def _pinned(path):
    """Tuned lambda, its accuracy and step, and unguarded SEC, from a pinned SEC1-arm results file. Rows without window
    fields (SCL3's safety-harness rows, which carry an 'arm' label) are not SEC1 arms and are skipped."""
    g = {}; sec = []
    for line in open(path):
        r = json.loads(line)
        if "arm" in r or r.get("fs") != S.FS or r.get("fe") != S.FE: continue
        if r.get("mode") == "fixed": g.setdefault(r["value"], []).append(r["acc"])
        elif r.get("mode") == "bayes_sec": sec.append(r["acc"])
    tuned = max(g, key=lambda w: np.mean(g[w]))
    return tuned, float(np.mean(g[tuned])), S.step_of(g[tuned]), float(np.mean(sec))


def dev():
    print("SEC4 guard development on the 16 SEEN carriers (prereg/sec4/DEV_DECLARATION.md); tuned lambda and step from pinned results")
    print("=" * 118)
    X, y = S._synthetic(); Xs, ys, meta = L.select_classes(X, y, 10); K = meta["classes_used"]; data = S.split_standardise(Xs, ys, K)
    d_id = {}
    for v in VARIANTS:
        same = []
        for seed in SEEDS:
            a = P3._run("bayes_sec", 0.0, seed, *data, K, 2)
            b = run_guard(seed, *data, K, 2, v, kappa=float("inf"), raw_bound=float("inf"))
            same.append(a["acc"] == b["acc"] and a["s"] == b["s"] and b["guard_fired"] == 0)
        d_id[v] = all(same)
        print(f"D-ID {v}: with an infinite bound equals SEC1's bayes_sec on the synthetic stream: {sum(same)}/{len(same)} -> {'holds' if d_id[v] else 'FAILS'}")
    res = {v: {} for v in VARIANTS}; base = {}
    carriers = [(did, "scl3", DEV_SCL3) for did in DEV_SCL3] + [(did, "sec3", DEV_SEC3) for did in DEV_SEC3 if did not in DEV_EXCLUDED]
    for did, study, table in carriers:
        name = table[did][0]; L.DATASETS = table
        Xs, ys, meta = L.load_openml(did); K = meta["classes_used"]; data = S.split_standardise(Xs, ys, K)
        tuned, tacc, step, secu = _pinned(ROOT / "runs" / study / f"results_{did}.jsonl")
        base[name] = dict(tuned=tuned, tacc=tacc, step=step, secu=secu)
        line = f"[{name}] ({study}) tuned {tuned:g}: {tacc:.4f}, step {step:.4f}; unguarded SEC {secu:.4f} ({secu - tacc:+.4f})"
        for v in VARIANTS:
            os_ = [run_guard(s, *data, K, 2, v) for s in SEEDS]
            acc = float(np.mean([o["acc"] for o in os_])); fired = sum(o["guard_fired"] for o in os_)
            res[v][name] = dict(acc=acc, fired=fired, seeds=[o["acc"] for o in os_])
            line += f"\n     {v:5}: {acc:.4f} [{' '.join('%.2f' % o['acc'] for o in os_)}] −tuned {acc - tacc:+.4f}, fired {fired}"
        print(line, flush=True)
    L.DATASETS = DATASETS
    print("=" * 118)
    nb = lambda v, d: res[v][d]["acc"] - base[d]["tacc"] > -base[d]["step"]  # noqa: E731
    counts = {v: sum(nb(v, d) for d in base) for v in VARIANTS}
    ok_carriers = [d for d in base if base[d]["secu"] - base[d]["tacc"] > -base[d]["step"]]
    interf = {v: sum(res[v][d]["fired"] for d in ok_carriers) for v in VARIANTS}
    print(f"unguarded SEC not behind: {len(ok_carriers)}/{len(base)} (pinned)")
    for v in VARIANTS:
        print(f"{v:5}: not behind {counts[v]}/{len(base)}; firings where unguarded SEC was already not behind {interf[v]}; "
              f"divergence carriers not behind {sum(nb(v, d) for d in DIVERGED)}/3")
    chosen = sorted(VARIANTS, key=lambda v: (-counts[v], interf[v], VARIANTS.index(v)))[0]
    need = math.ceil(0.75 * len(base))
    d_count = counts[chosen] >= need; d_fix = sum(nb(chosen, d) for d in DIVERGED) >= 2
    print(f"CHOSEN (most not behind; ties: fewest interfering firings, then {VARIANTS}): {chosen}")
    print(f"D-COUNT {counts[chosen]}/{len(base)} (need {need}) -> {'holds' if d_count else 'FAILS'}; D-ID -> {'holds' if d_id[chosen] else 'FAILS'}; "
          f"D-FIXES {sum(nb(chosen, d) for d in DIVERGED)}/3 (need 2) -> {'holds' if d_fix else 'FAILS'}")
    print("D-GATE " + ("OPEN" if (d_count and d_id[chosen] and d_fix) else "CLOSED"))


# ---------------------------------------------------------------- the test family (OpenML suites 14, 218, 379, 457)
def run_carrier(did, out, tout, synthetic=False):
    if synthetic:
        X, y = S._synthetic(); Xs, ys, meta = L.select_classes(X, y, 10); meta = dict(file="synthetic", sha256="none", openml_id=did, **meta); name = "synthetic"
    else:
        L.DATASETS = DATASETS; name = DATASETS[did][0]; Xs, ys, meta = L.load_openml(did)
    per_task = 2
    if meta["excluded"]:
        print(json.dumps(dict(dataset=name, **meta)), file=out, flush=True); return
    K = meta["classes_used"]; data = S.split_standardise(Xs, ys, K)
    S.run = _timed
    try:
        S.run_all(name, data, K, per_task, meta, out)
    finally:
        S.run = P3._run
    for seed in SEEDS:
        arms = [(CHOSEN, (S.FS, S.FE))] + [(CHOSEN, c) for c in KEEP_CELLS] + [(v, (S.FS, S.FE)) for v in VARIANTS if v != CHOSEN]
        for v, (fs, fe) in arms:
            o = run_guard(seed, *data, K, per_task, v, fs=fs, fe=fe); o["dataset"] = name
            print(json.dumps(o), file=out, flush=True)
    for t in TIMES:
        t["dataset"] = name; print(json.dumps(t), file=tout, flush=True)
    TIMES.clear()


def _mean(rows, mode, value=None, fs=S.FS, fe=S.FE):
    v = [r["acc"] for r in rows if r.get("mode") == mode and (value is None or abs(r["value"] - value) <= 1e-6 * max(1.0, abs(value)))
         and r["fs"] == fs and r["fe"] == fe]
    return (float(np.mean(v)), v) if v else (None, [])


def score(paths):
    by = {}
    for p in paths:
        for line in open(p):
            o = json.loads(line)
            if "mode" in o: by.setdefault(o["dataset"], []).append(o)
            elif o.get("excluded"): by.setdefault(o["dataset"], None)
    times = {}
    for p in paths:
        tp = Path(str(p).replace("results_", "times_"))
        if tp != Path(p) and tp.exists():
            for line in open(tp):
                t = json.loads(line); times.setdefault(t["dataset"], []).append(t)
    excl = sorted(d for d, v in by.items() if v is None); names = sorted(d for d, v in by.items() if v is not None)
    G = f"bayes_sec_{CHOSEN}"
    print("=" * 118)
    print(f"SEC4 scoring (prereg/sec4/PREREG.md): the guarded SEC ({CHOSEN}) as the arm under test, SCL3/SEC3 thresholds, the saving rows")
    print("=" * 118)
    print(f"carriers scored {len(names)}: {names}; excluded {len(excl)}: {excl}")
    R = {}
    for d in names:
        rows = by[d]
        g = {}
        for r in rows:
            if r.get("mode") == "fixed" and r["fs"] == S.FS and r["fe"] == S.FE: g.setdefault(r["value"], []).append(r["acc"])
        gm = {w: float(np.mean(v)) for w, v in sorted(g.items())}
        gs = {}
        for r in rows:
            if r.get("mode") == "fixed_sec" and r["fs"] == S.FS and r["fe"] == S.FE: gs.setdefault(r["value"], []).append(r["acc"])
        tuned = max(gm, key=gm.get); step = S.step_of(g[tuned]); tuned_s = max(gs, key=lambda w: np.mean(gs[w]))
        guard_rows = [o for o in rows if o.get("mode") == G and o["fs"] == S.FS and o["fe"] == S.FE]
        r = dict(step=step, tuned=tuned, tacc=gm[tuned], tuned_s=tuned_s, grid=gm, n_cfg=len(gm),
                 g=_mean(rows, G)[0], g_seeds=_mean(rows, G)[1], fired=sum(o["guard_fired"] for o in guard_rows),
                 u=_mean(rows, "bayes_sec", 0.0)[0], u_seeds=_mean(rows, "bayes_sec", 0.0)[1], raw=_mean(rows, "bayes", 0.0)[0], eq=_mean(rows, "eq", 1.0)[0],
                 others={v: _mean(rows, f"bayes_sec_{v}")[0] for v in VARIANTS if v != CHOSEN},
                 sens={c: _mean(rows, G, None, *c)[0] for c in KEEP_CELLS},
                 best3=max(THREE, key=lambda w: gm[w]) if all(w in gm for w in THREE) else None, n_seeds=len(g[tuned]))
        r["best3_acc"] = gm[r["best3"]] if r["best3"] else None
        R[d] = r
    for d in names:
        others = [math.log(R[o]["tuned"]) for o in names if o != d]
        if others:
            lam = math.exp(float(np.median(others))); snap = min(S.EWC_COARSE, key=lambda w: abs(math.log(w) - math.log(lam)))
            R[d]["loco"] = snap; R[d]["loco_acc"] = R[d]["grid"][snap]
        else:
            R[d]["loco"] = None; R[d]["loco_acc"] = None
    for d in names:
        r = R[d]
        print(f"\n[{d}] step {r['step']:.4f}; tuned lambda {r['tuned']:g} ({r['n_cfg']} grid configurations): {r['tacc']:.4f}")
        print("   raw grid: " + "  ".join(f"{w:g}:{v:.2f}" for w, v in r["grid"].items()))
        print(f"   guarded SEC ({CHOSEN}) {r['g']:.4f} [{' '.join('%.2f' % a for a in r['g_seeds'])}] −tuned {r['g'] - r['tacc']:+.4f}; fired {r['fired']}")
        print(f"   unguarded SEC {r['u']:.4f} [{' '.join('%.2f' % a for a in r['u_seeds'])}] −tuned {r['u'] - r['tacc']:+.4f}; raw Laplace {r['raw']:.4f} ({r['raw'] - r['tacc']:+.4f}); "
              f"rule Ω=1 {r['eq']:.4f} ({r['eq'] - r['tacc']:+.4f}); other guards " + ", ".join(f"{v} {a - r['tacc']:+.4f}" for v, a in r["others"].items()))
        if r["best3"] is not None:
            print(f"   3-point sweep: best {r['best3']:g} {r['best3_acc']:.4f}; guarded SEC − best3 {r['g'] - r['best3_acc']:+.4f}")
        if r["loco"] is not None:
            print(f"   transferred lambda {r['loco']:g}: {r['loco_acc']:.4f} −tuned {r['loco_acc'] - r['tacc']:+.4f}")
        print("   window cells (guarded) − tuned: " + "  ".join(f"{c[0]:g}/{c[1]:g}:{v - r['tacc']:+.2f}" for c, v in r["sens"].items()))
    N = len(names); need = math.ceil(SHARE * N)
    nb = lambda a, r: a - r["tacc"] > -r["step"]  # noqa: E731
    print("\n" + "-" * 118)
    k = sum(nb(R[d]["g"], R[d]) for d in names)
    v1 = "NOT DECIDABLE (fewer than %d carriers scored)" % MIN_N if N < MIN_N else ("PASS" if k >= need else "FAIL")
    print(f"SEC4-1 tuning-free, the guarded SEC ({CHOSEN}) not behind the tuned lambda: {k}/{N} (need {need}) -> {v1}; "
          + ", ".join(f"{d}:{R[d]['g'] - R[d]['tacc']:+.4f} (step {R[d]['step']:.2f})" for d in names))
    ku = sum(nb(R[d]["u"], R[d]) for d in names); kr = sum(nb(R[d]["raw"], R[d]) for d in names); ke = sum(nb(R[d]["eq"], R[d]) for d in names)
    print(f"   beside it (report): unguarded SEC {ku}/{N}; raw Laplace {kr}/{N}; the rule Ω=1 {ke}/{N}")
    div = [d for d in names if any(a < DIV_FRAC * R[d]["tacc"] for a in R[d]["g_seeds"])]
    divu = [d for d in names if any(a < DIV_FRAC * R[d]["tacc"] for a in R[d]["u_seeds"])]
    print(f"SEC4-2 no divergence: carriers with a guarded seed below half the tuned accuracy: {div} ({len(div)}) -> {'PASS' if not div else 'FAIL'}; unguarded (report): {divu}")
    B = [d for d in names if R[d]["loco"] is not None and not nb(R[d]["loco_acc"], R[d])]
    if len(B) >= MIN_B:
        kt = sum(nb(R[d]["g"], R[d]) for d in B); needt = math.ceil(SHARE * len(B))
        print(f"SEC4-T the saving is SEC's: B = {B} ({len(B)}); guarded SEC not behind on {kt}/{len(B)} (need {needt}) -> {'PASS' if kt >= needt else 'FAIL'}")
    else:
        print(f"SEC4-T: NOT DECIDABLE (a transferred lambda is behind on only {len(B)} carriers, need >= {MIN_B})")
    kp = sum(R[d]["best3"] is not None and R[d]["g"] - R[d]["best3_acc"] > -R[d]["step"] for d in names)
    print(f"SEC4-P guarded SEC (1 configuration) not behind the 3-point mini-sweep (3): {kp}/{N} (need {need}) -> {'PASS' if kp >= need else 'FAIL'}")
    flips = sum(nb(R[d]["g"], R[d]) != nb(v, R[d]) for d in names for v in R[d]["sens"].values())
    print(f"SEC4-S sensitivity over the retained window cells: flips in {flips} of {sum(len(R[d]['sens']) for d in names)} -> {'FRAGILE' if flips > 1 else 'not fragile'}")
    print("SEC4-K compute (report; CPU seconds from the timing files):")
    for d in names:
        t = times.get(d, [])
        cpu = lambda mode, val=None, fs=S.FS, fe=S.FE: sum(x["cpu_s"] for x in t if x["mode"] == mode and x["fs"] == fs and x["fe"] == fe  # noqa: E731
                                                          and (val is None or abs(x["value"] - val) <= 1e-6 * max(1.0, abs(val))))
        full = cpu("fixed"); gcpu = cpu(G); raw = cpu("bayes", 0.0)
        print(f"   {d}: configurations full sweep {R[d]['n_cfg']}, guarded SEC 1; CPU s full {full:.1f}, guarded SEC {gcpu:.1f}"
              + (f" (share {gcpu / full:.4f}), raw Laplace {raw:.1f} (overhead x{gcpu / raw if raw else float('nan'):.3f})" if full else ""))
    print("SEC4-E guard firings (report): " + "; ".join(f"{d}: {R[d]['fired']}" for d in names))


def data_check():
    man = {}
    for line in open(ROOT / "data" / "manifests" / "sec4.sha256"):
        if line.strip(): h_, pth = line.split()[:2]; man[pth] = h_
    bad = []
    for did, (name, _, _) in DATASETS.items():
        for ext in ("arff", "json"):
            pth = f"data/raw/openml/{did}_{name}.{ext}"; got = S.sha256(ROOT / pth) if (ROOT / pth).exists() else None
            print(f"{did} {name} .{ext}: sha256 {got} manifest {man.get(pth)} -> {'ok' if got and got == man.get(pth) else 'MISMATCH'}")
            if not got or got != man.get(pth): bad.append(f"{name}.{ext}")
    print("data check: " + (f"all {2 * len(DATASETS)} raw files match data/manifests/sec4.sha256" if not bad else f"MISMATCH {bad}: the study stops"))
    return not bad


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "dev": dev()
    elif cmd == "check": sys.exit(0 if data_check() else 1)
    elif cmd == "all":
        did = int(sys.argv[2])
        outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else f"runs/sec4/results_{did}.jsonl"
        tp = sys.argv[sys.argv.index("--times") + 1] if "--times" in sys.argv else outp.replace("results_", "times_")
        with open(outp, "w") as out, open(tp, "w") as tout: run_carrier(did, out, tout)
    elif cmd == "score": score(sys.argv[2:])
    elif cmd == "smokefull":
        outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "/tmp/results_sec4_smoke.jsonl"
        with open(outp, "w") as out, open(outp.replace("results_", "times_"), "w") as tout: run_carrier(0, out, tout, synthetic=True)
        score([outp])
    else: raise SystemExit(__doc__)
