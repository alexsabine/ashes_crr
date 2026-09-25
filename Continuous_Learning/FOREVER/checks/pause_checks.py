"""The empty cut applied to a FOREVER learner (Continuous_Learning/FOREVER/DECLARATION_3.md, pushed before this script
existed; prompt-log entry 182). Rung R4; every label computed here (R15).

The learner is comparative.py's "F FOREVER" arm rewritten with explicit state, so that an operator's pause can save it,
restore it, or drop one component the way a naive resume would. FOREVER's state beyond the parameters: the step lengths
of the current task (tau and tau_day are sums over them), mu_0 and mu, the index j of the next replay threshold, the
anchor Theta*, the replay buffer, and the two random-number streams (current-task batches, replay batches).
"""
import copy
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import comparative as C  # noqa: E402

BETA = 1.0                                   # beta_base tuned in comparative.txt
WORLDS = ("W1 base", "W6 class-incremental"); SEEDS = (0, 1, 2, 3, 4)
PAUSES = (150, 700, 1300); L_PAUSE = 100; DRIFT_RATE = 0.004
OMIT = ("tau", "ema", "j", "tau_day", "anchor", "buffer", "rng_batch", "rng_replay")


def run(w, seed, pauses=(), omit=(), wall=None, truncate=None, drift=False):
    """omit: components dropped at every pause; wall: None | 'ticks' | 'ticks+ema'; truncate: stop after this many
    current-task updates (the clock valuation's deadline); drift: the world moves with wall ticks (E3)."""
    cfg, tasks, model = C.make_world(w, seed); T = cfg["T"]
    st = dict(rb=np.random.default_rng(20_000 + seed), rr=np.random.default_rng(30_000 + seed))
    buf, anchors = [], []; acc = np.zeros((T, T)); u = 0; tick = 0
    if drift:                                                      # E3: class means move with wall ticks while a task is current
        dr = np.random.default_rng(60_000 + seed); dirs = [dr.choice([-1.0, 1.0], size=tasks[0][0].shape[1]) for _ in range(T)]
        drng = np.random.default_rng(70_000 + seed)
        means = []
        for (Xtr, Ytr, Xte, yte) in tasks:                         # recover each task's class means from its training set
            y = np.argmax(Ytr, 1); means.append({c: Xtr[y == c].mean(0) for c in np.unique(y)})
    test_sets = [None] * T
    for t, (Xtr, Ytr, Xte, yte) in enumerate(tasks):
        lr = C.LR * (cfg["lrm"][t] if cfg["lrm"] else 1.0)
        s = dict(eu=[], mu=None, mu0=None, fired=0, tau_off=0.0, day_override=None, day_from=None, buf_off=False, tick0=tick)
        anc = anchors[-1] if t > 0 else None
        tp = np.array([1.0] * t) / t if t > 0 else None
        wt_tick = 0
        def world_X(n, rng):
            cls = sorted(means[t]); y = np.array([cls[i % len(cls)] for i in range(n)])
            shift = DRIFT_RATE * (tick - s["tick0"]) * dirs[t]
            return np.stack([means[t][c] for c in y]) + shift + rng.normal(0, C.NOISE_SD, size=(n, len(shift))), y

        def replay_event():
            if s["buf_off"]: return
            mu0, mu = s["mu0"], s["mu"]; r = (mu / mu0) if (mu0 and mu is not None) else 1.0
            for _ in range(C.R_EV):
                ks = st["rr"].choice(t, size=C.BS, p=tp); idx = [st["rr"].integers(0, len(buf[k][0])) for k in ks]
                X = np.stack([buf[k][0][i] for k, i in zip(ks, idx)]); Y = np.stack([buf[k][1][i] for k, i in zip(ks, idx)])
                g_old = model.grads(X, Y); g_anc = [2 * (x - y) for x, y in zip(model.p, anc)]
                wt = BETA * float(np.clip(1 + C.GAMMA * (r - 1), C.GMIN, C.GMAX))
                model.p = [x - lr * (go + wt * ga) for x, go, ga in zip(model.p, g_old, g_anc)]

        for step in range(1, C.STEPS + 1):
            if truncate is not None and u >= truncate: break
            i = st["rb"].integers(0, len(Xtr), C.BS)
            if drift:
                Xb, yb = world_X(C.BS, drng); Yb = np.eye(cfg["K"])[yb]; g = model.grads(Xb, Yb)
            else:
                g = model.grads(Xtr[i], Ytr[i])
            old = [x.copy() for x in model.p]
            model.p = [x - lr * gx for x, gx in zip(model.p, g)]
            u += 1; tick += 1; wt_tick += 1
            s["eu"].append(C.dist(model.p, old))
            if step == C.S_DEFAULT: s["mu0"] = float(np.mean(s["eu"])); s["mu"] = s["mu0"]
            elif step > C.S_DEFAULT and s["mu"] is not None: s["mu"] = (1 - C.LAM) * s["mu"] + C.LAM * s["eu"][-1]
            # ---- the operator's pause, after global update u
            if u in pauses:
                saved = copy.deepcopy(dict(p=model.p, s=s, st=st, anc=anc, buf=buf, anchors=anchors))
                tick += L_PAUSE; wt_tick += L_PAUSE
                if wall == "ticks+ema" and s["mu"] is not None:
                    for _ in range(L_PAUSE): s["mu"] = (1 - C.LAM) * s["mu"]    # the EMA advances per tick with Delta = 0
                    saved["s"]["mu"] = s["mu"]
                model.p = saved["p"]; s.update(saved["s"]); st = saved["st"]; anc = saved["anc"]; buf = saved["buf"]; anchors = saved["anchors"]
                for o in omit:                                         # a naive resume drops one component
                    if o == "tau": s["tau_off"] = float(np.sum(s["eu"]))
                    elif o == "ema": s["mu0"] = None; s["mu"] = None
                    elif o == "j": s["fired"] = 0
                    elif o == "tau_day": s["day_from"] = len(s["eu"]); s["day_override"] = None
                    elif o == "anchor" and t > 0: anc = [x.copy() for x in model.p]
                    elif o == "buffer": s["buf_off"] = True
                    elif o == "rng_batch": st["rb"] = np.random.default_rng(20_000 + seed)
                    elif o == "rng_replay": st["rr"] = np.random.default_rng(30_000 + seed)
            if t == 0 or step < C.S_DEFAULT or s["fired"] >= len(C.DAYS): continue
            if wall in ("ticks", "ticks+ema"):
                val, day = float(wt_tick), float(C.S_DEFAULT)
            else:
                val = float(np.sum(s["eu"])) - s["tau_off"]; day = float(np.sum(s["eu"][:C.S_DEFAULT]))
                if s["day_from"] is not None:                          # tau_day re-calibrated on the next S updates
                    if len(s["eu"]) - s["day_from"] < C.S_DEFAULT: continue
                    day = float(np.sum(s["eu"][s["day_from"]:s["day_from"] + C.S_DEFAULT]))
            if day > 0 and val >= C.DAYS[s["fired"]] * day:
                replay_event(); s["fired"] += 1
        if truncate is not None and u >= truncate and step < C.STEPS:
            pass                                                       # the deadline fell inside this task: no end-of-task events
        elif t > 0:
            while s["fired"] < len(C.DAYS): replay_event(); s["fired"] += 1
            replay_event()
        s["buf_off"] = False
        anchors.append([x.copy() for x in model.p])
        if drift:
            Xb, yb = world_X(C.BUF_PER, np.random.default_rng(50_000 + 97 * seed + t)); buf.append((Xb, np.eye(cfg["K"])[yb]))
            test_sets[t] = world_X(C.N_TE, np.random.default_rng(80_000 + 97 * seed + t))
        else:
            k = np.random.default_rng(50_000 + 97 * seed + t).choice(len(Xtr), C.BUF_PER, replace=False); buf.append((Xtr[k], Ytr[k]))
            test_sets[t] = (Xte, yte)
        for j in range(t + 1):
            acc[t, j] = 100.0 * float(np.mean(np.argmax(model.probs(test_sets[j][0]), 1) == test_sets[j][1]))
        if truncate is not None and u >= truncate: break
    last = min(t, T - 1)
    final = [100.0 * float(np.mean(np.argmax(model.probs((test_sets[j] or tasks[j][2:])[0]), 1) == (test_sets[j] or tasks[j][2:])[1]))
             for j in range(T)]
    op = float(np.mean(final)); bwt = float(np.mean([acc[last, j] - acc[j, j] for j in range(last)])) if last > 0 else 0.0
    return dict(op=op, bwt=bwt, params=C.flat(model.p), updates=u)


def lab(ok):
    return "HOLDS" if ok else "FAILS"


def main():
    print("The empty cut applied to a FOREVER learner (Continuous_Learning/FOREVER/DECLARATION_3.md)")
    print(f"learner: comparative.py's FOREVER arm with explicit state; beta_base {BETA}; worlds {WORLDS}; seeds {SEEDS}; "
          f"pauses after updates {PAUSES}, {L_PAUSE} wall ticks each; drift rate {DRIFT_RATE} per tick (Q5)")
    labels = {}
    # ---- Q0
    print("\n== Q0 instrument: the explicit-state learner against comparative.run (FOREVER arm), seed 0, no pauses")
    ok0 = True
    for w in WORLDS:
        a = run(w, 0); b = C.run(w, 0, "F FOREVER", BETA)
        same = f"{a['op']:.6f}" == f"{b['op']:.6f}" and f"{a['bwt']:.6f}" == f"{b['bwt']:.6f}"; ok0 &= same
        print(f"   {w}: explicit OP {a['op']:.6f} BWT {a['bwt']:.6f}; comparative OP {b['op']:.6f} BWT {b['bwt']:.6f} -> {'identical' if same else 'DIFFERENT'}")
    labels["Q0"] = ok0
    base = {(w, s): run(w, s) for w in WORLDS for s in SEEDS}
    N = len(WORLDS) * len(SEEDS)

    def same_run(r, b): return bool(np.array_equal(r["params"], b["params"]))

    # ---- Q1
    print("\n== Q1 the lossless cut (every component saved and restored)")
    n1 = 0
    for w in WORLDS:
        for s in SEEDS:
            r = run(w, s, pauses=PAUSES); ok = same_run(r, base[(w, s)]) and r["op"] == base[(w, s)]["op"]; n1 += ok
            print(f"   {w} seed {s}: bitwise identical {same_run(r, base[(w, s)])}, OP difference {r['op'] - base[(w, s)]['op']:+.6f}")
    labels["Q1"] = n1 == N; print(f"   Q1 identical in {n1} of {N} -> {lab(n1 == N)}")

    # ---- Q2
    print("\n== Q2 state closure: one component dropped at every pause, the way a naive resume would")
    q2 = {}
    for o in OMIT:
        diffs = []; ndiff = 0
        for w in WORLDS:
            for s in SEEDS:
                r = run(w, s, pauses=PAUSES, omit=(o,)); d = not same_run(r, base[(w, s)]); ndiff += d; diffs.append(r["op"] - base[(w, s)]["op"])
        q2[o] = ndiff
        print(f"   omit {o}: runs changed {ndiff} of {N}; OP difference mean {np.mean(diffs):+.3f}, min {min(diffs):+.3f}, max {max(diffs):+.3f}"
              + (" (inert)" if ndiff == 0 else ""))
    q2ok = all(v >= 8 for v in q2.values()); labels["Q2"] = q2ok
    print(f"   Q2 every omission changes at least 8 of {N} runs -> {lab(q2ok)}; inert components: {[o for o, v in q2.items() if v == 0]}")

    # ---- Q3
    print("\n== Q3 own-clock keying: replay thresholds on wall ticks, (a) with the EMA advanced per tick, (b) thresholds only")
    for mode, key in (("ticks+ema", "Q3a"), ("ticks", "Q3b")):
        nd = 0
        for w in WORLDS:
            for s in SEEDS:
                nb = run(w, s, wall=mode); r = run(w, s, pauses=PAUSES, wall=mode); nd += not same_run(r, nb)
        labels[key] = nd >= 8; print(f"   {key} ({mode}): paused runs differ from their own no-pause runs in {nd} of {N} -> {lab(nd >= 8)}")

    # ---- Q4
    print("\n== Q4 the stake: natural valuation (OP after the full own-update budget) and clock valuation (OP at a wall deadline)")
    budget = {(w, s): base[(w, s)]["updates"] for w in WORLDS for s in SEEDS}
    nat0 = clk = lossy = 0
    for w in WORLDS:
        for s in SEEDS:
            b = base[(w, s)]
            rn = run(w, s, pauses=PAUSES); stake_nat = b["op"] - rn["op"]
            rc = run(w, s, pauses=PAUSES, truncate=budget[(w, s)] - len(PAUSES) * L_PAUSE); stake_clk = b["op"] - rc["op"]
            rl = run(w, s, pauses=PAUSES, omit=("tau", "ema", "j")); stake_lossy = b["op"] - rl["op"]
            nat0 += stake_nat == 0.0; clk += stake_clk > 0; lossy += stake_lossy != 0.0
            print(f"   {w} seed {s}: natural stake {stake_nat:+.4f}; clock stake {stake_clk:+.4f} (stops at update {rc['updates']}); "
                  f"lossy-resume natural stake {stake_lossy:+.4f}")
    labels["Q4a"] = nat0 == N; labels["Q4b"] = clk >= 8; labels["Q4c"] = lossy >= 8
    print(f"   Q4a natural stake exactly 0 in {nat0} of {N} -> {lab(nat0 == N)}; Q4b clock stake > 0 in {clk} of {N} -> {lab(clk >= 8)}; "
          f"Q4c lossy-resume natural stake != 0 in {lossy} of {N} -> {lab(lossy >= 8)}")

    # ---- Q5
    print("\n== Q5 the world moves during the pause (E3; must fail): lossless checkpoint, drifting world")
    n5 = 0
    for w in WORLDS:
        for s in SEEDS:
            b = run(w, s, drift=True); r = run(w, s, pauses=PAUSES, drift=True); st5 = b["op"] - r["op"]; n5 += st5 != 0.0
            print(f"   {w} seed {s}: natural stake {st5:+.4f}")
    labels["Q5"] = n5 >= 8
    print(f"   Q5 natural stake != 0 in {n5} of {N} -> {lab(n5 >= 8)} (the construction must not claim safety when the world moves)")
    print("\nsummary: " + "; ".join(f"{k} {lab(v)}" for k, v in labels.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
