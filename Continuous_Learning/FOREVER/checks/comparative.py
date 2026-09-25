"""Comparative investigation: CRR against FOREVER on synthetic continual-learning worlds (Continuous_Learning/FOREVER/
DECLARATION_2.md, pushed before this script existed; prompt-log entry 181). Rung R4; every label computed here (R15).

FOREVER (arXiv 2601.03938 v2) is decomposed into its choices (clock, unit, measured quantity, replay weight, anchor,
replay sampling); each is swapped for the choice a CRR commitment makes (D2/D6 Fisher arc, A1' robust unit, D3 chord,
H-EQ step-bounded weight, A6+P3 normalised age-weighted anchor, P3 age-weighted sampling, P2 surplus-weighted sampling).
Every event-based arm has the same replay budget (six events per task plus the end-of-task consolidation), so arms differ
only in when replay happens and how it acts. Data, initialisation and current-task batch order are identical across arms
for a given (world, seed): the comparison is paired.
"""
import itertools
import multiprocessing as mp
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "src"))
from crr.instrument.core import kl_step  # noqa: E402

DAYS = (1, 2, 4, 7, 15, 30); S_DEFAULT = 24; LAM = 0.05; GMIN, GMAX = 0.5, 3.0; GAMMA = 1.0
R_EV = 5; BUF_PER = 10; STEPS = 300; BS = 10; LR = 0.05; Q_AGE = 0.5; OMEGA = 1.0; EMA_S = 0.9; WCAP = 1e4
N_TR, N_TE, D, RANK = 400, 200, 20, 4
NOISE_SD, MEAN_SD, DRIFT_SD, CONFLICT = 2.0, 1.0, 1.0, False     # Amendment 1 (declared: 1.0, 1.5, 1.5)
BETA_GRID = (1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.3, 1.0, 3.0)
SEEDS = tuple(range(10)); TUNE_SEEDS = (100, 101, 102, 103, 104)

WORLDS = {  # name: model, classes, tasks, dead features, init factor on P, lr multipliers per task, class-incremental
    "W1 base": dict(model="lora", K=4, T=5, dead=0, pinit=1.0, lrm=None, cil=False),
    "W2 null movement": dict(model="lora", K=4, T=5, dead=8, pinit=1.0, lrm=None, cil=False),
    "W3 parametrisation": dict(model="lora", K=4, T=5, dead=0, pinit=4.0, lrm=None, cil=False),
    "W4 learning rates": dict(model="lora", K=4, T=5, dead=0, pinit=1.0, lrm=(1, 4, 0.25, 2, 0.5), cil=False),
    "W5 convex": dict(model="linear", K=4, T=5, dead=0, pinit=1.0, lrm=None, cil=False),
    "W6 class-incremental": dict(model="mlp", K=10, T=5, dead=0, pinit=1.0, lrm=None, cil=True),
    "W7 long": dict(model="lora", K=4, T=15, dead=0, pinit=1.0, lrm=None, cil=False),
}
#        name        clock     unit      weight     anchor   sampling
ARMS = {
    "B0 fine-tune": None, "B1 ER-mix": "ermix",
    "B2 FIR": dict(clock="fir", unit="sum", weight="forever", anchor="last", samp="uniform"),
    "B3 STC": dict(clock="steps", unit="sum", weight="forever", anchor="last", samp="uniform"),
    "F FOREVER": dict(clock="euclid", unit="sum", weight="forever", anchor="last", samp="uniform"),
    "C1 Fisher arc": dict(clock="fisher", unit="sum", weight="forever", anchor="last", samp="uniform"),
    "C2 + A1' unit": dict(clock="fisher", unit="median", weight="forever", anchor="last", samp="uniform"),
    "C3 Fisher chord": dict(clock="chord", unit="sum", weight="forever", anchor="last", samp="uniform"),
    "C4 H-EQ weight": dict(clock="euclid", unit="sum", weight="heq", anchor="last", samp="uniform"),
    "C5 A6 anchor": dict(clock="euclid", unit="sum", weight="forever", anchor="a6", samp="uniform"),
    "C6 P3 sampling": dict(clock="euclid", unit="sum", weight="forever", anchor="last", samp="p3"),
    "C7 P2 sampling": dict(clock="euclid", unit="sum", weight="forever", anchor="last", samp="p2"),
    "CRR-full": dict(clock="fisher", unit="median", weight="heq", anchor="a6", samp="p3"),
}


def softmax(z):
    z = z - z.max(axis=1, keepdims=True); e = np.exp(z); return e / e.sum(axis=1, keepdims=True)


# ---------------------------------------------------------------- models: params are lists of arrays
class Model:
    def __init__(self, kind, d, K, rng, pinit):
        self.kind = kind
        if kind == "lora":
            self.W0 = rng.normal(0, 0.05, size=(d, K))
            self.p = [rng.normal(0, 0.1, size=(d, RANK)) * pinit, rng.normal(0, 0.1, size=(RANK, K)) / pinit]
        elif kind == "linear":
            self.p = [rng.normal(0, 0.05, size=(d, K))]
        else:
            H = 32
            self.p = [rng.normal(0, np.sqrt(2 / d), size=(d, H)), np.zeros(H), rng.normal(0, np.sqrt(1 / H), size=(H, K)), np.zeros(K)]

    def probs(self, X, p=None):
        p = self.p if p is None else p
        if self.kind == "lora": return softmax(X @ (self.W0 + p[0] @ p[1]))
        if self.kind == "linear": return softmax(X @ p[0])
        h = np.maximum(X @ p[0] + p[1], 0); return softmax(h @ p[2] + p[3])

    def grads(self, X, Y):
        n = len(X)
        if self.kind == "lora":
            G = X.T @ (self.probs(X) - Y) / n; return [G @ self.p[1].T, self.p[0].T @ G]
        if self.kind == "linear":
            return [X.T @ (self.probs(X) - Y) / n]
        W1, b1, W2, b2 = self.p; z = X @ W1 + b1; h = np.maximum(z, 0); P = softmax(h @ W2 + b2)
        dL = (P - Y) / n; gW2 = h.T @ dL; gb2 = dL.sum(0); dh = dL @ W2.T * (z > 0)
        return [X.T @ dh, dh.sum(0), gW2, gb2]


def flat(ps): return np.concatenate([x.ravel() for x in ps])
def dist(a, b): return float(np.sqrt(sum(np.sum((x - y) ** 2) for x, y in zip(a, b))))
def fisher_len(pa, pb): return float(np.sqrt(max(2 * kl_step(pa, pb), 0.0)))


# ---------------------------------------------------------------- data
def make_world(w, seed):
    cfg = WORLDS[w]; rng = np.random.default_rng(10_000 + seed); K, T, dead = cfg["K"], cfg["T"], cfg["dead"]
    tasks = []
    if cfg["cil"]:
        M = rng.normal(0, MEAN_SD, size=(K, D))
        for t in range(T):
            cls = np.array([2 * t, 2 * t + 1])
            def draw(n):
                y = cls[np.arange(n) % 2]; return M[y] + rng.normal(0, NOISE_SD, size=(n, D)), y
            tasks.append((draw(N_TR), draw(N_TE)))
    else:
        M0 = rng.normal(0, MEAN_SD, size=(K, D))
        for t in range(T):
            Mt = M0 + rng.normal(0, DRIFT_SD, size=(K, D))
            if CONFLICT and t > 0: Mt = Mt[rng.permutation(K)]           # the same regions change label: tasks conflict
            def draw(n, Mt=Mt):
                y = np.arange(n) % K; return Mt[y] + rng.normal(0, NOISE_SD, size=(n, D)), y
            tasks.append((draw(N_TR), draw(N_TE)))
    out = []
    for (Xtr, ytr), (Xte, yte) in tasks:
        if dead: Xtr = np.concatenate([Xtr, np.zeros((len(Xtr), dead))], 1); Xte = np.concatenate([Xte, np.zeros((len(Xte), dead))], 1)
        out.append((Xtr, np.eye(K)[ytr], Xte, yte))
    model = Model(cfg["model"], D + dead, K, rng, cfg["pinit"])
    return cfg, out, model


# ---------------------------------------------------------------- one run
def run(w, seed, arm, beta_base, S=S_DEFAULT):
    cfg, tasks, model = make_world(w, seed); a = ARMS[arm]; T = cfg["T"]
    rb = np.random.default_rng(20_000 + seed); rr = np.random.default_rng(30_000 + seed); rn = np.random.default_rng(40_000 + seed)
    buf = []; anchors = []; surplus = []; acc = np.zeros((T, T)); replay_batches = 0
    for t, (Xtr, Ytr, Xte, yte) in enumerate(tasks):
        lr = LR * (cfg["lrm"][t] if cfg["lrm"] else 1.0)
        bX = np.concatenate([b[0] for b in buf]) if buf else None; bY = np.concatenate([b[1] for b in buf]) if buf else None
        probe = np.concatenate([Xtr[:100]] + ([bX[:100]] if buf else []))
        p_start = model.probs(probe); p_prev = p_start
        eu, fi, ch = [], [], []; mu0 = mu = None; fired = 0; ema_o = ema_a = None
        if a not in (None, "ermix") and t > 0:
            if a["anchor"] == "last": anc = anchors[-1]
            else:
                wts = np.array([Q_AGE ** (t - 1 - k) for k in range(t)]); wts /= wts.sum()
                anc = [sum(wk * anchors[k][i] for k, wk in enumerate(wts)) for i in range(len(model.p))]
            if a["samp"] == "uniform": tp = np.array([1.0] * t)
            elif a["samp"] == "p3": tp = np.array([Q_AGE ** (t - 1 - k) for k in range(t)])
            else: s = np.array(surplus); tp = np.exp(s / max(s.mean(), 1e-12))
            tp = tp / tp.sum()
        fir_steps = [int(round(STEPS * (j + 1) / 7)) for j in range(len(DAYS))]

        def replay_event():
            nonlocal replay_batches, ema_o, ema_a
            ema_o = ema_a = None
            r = (mu / mu0) if (mu0 and mu is not None) else 1.0
            for _ in range(R_EV):
                ks = rr.choice(t, size=BS, p=tp); idx = [rr.integers(0, len(buf[k][0])) for k in ks]
                X = np.stack([buf[k][0][i] for k, i in zip(ks, idx)]); Y = np.stack([buf[k][1][i] for k, i in zip(ks, idx)])
                g_old = model.grads(X, Y); g_anc = [2 * (x - y) for x, y in zip(model.p, anc)]
                if a["weight"] == "forever":
                    wt = beta_base * float(np.clip(1 + GAMMA * (r - 1), GMIN, GMAX))
                else:
                    fo, fa = flat(g_old), flat(g_anc)
                    ema_o = fo if ema_o is None else EMA_S * ema_o + (1 - EMA_S) * fo
                    ema_a = fa if ema_a is None else EMA_S * ema_a + (1 - EMA_S) * fa
                    wt = min(OMEGA * np.linalg.norm(ema_o) / max(np.linalg.norm(ema_a), 1e-12), WCAP)
                model.p = [x - lr * (go + wt * ga) for x, go, ga in zip(model.p, g_old, g_anc)]
                replay_batches += 1

        for step in range(1, STEPS + 1):
            i = rb.integers(0, len(Xtr), BS); g = model.grads(Xtr[i], Ytr[i])
            if a == "ermix" and t > 0:
                j = rr.integers(0, len(bX), BS)
                g2 = model.grads(bX[j], bY[j]); g = [x + y for x, y in zip(g, g2)]; replay_batches += 1
            old = [x.copy() for x in model.p]
            model.p = [x - lr * gx for x, gx in zip(model.p, g)]
            if cfg["dead"]:                                           # movement that changes no prediction (W2)
                model.p[0] = model.p[0].copy(); model.p[0][-cfg["dead"]:] += rn.normal(0, 0.01, size=(cfg["dead"], model.p[0].shape[1]))
            p_now = model.probs(probe)
            eu.append(dist(model.p, old)); fi.append(fisher_len(p_prev, p_now)); ch.append(fisher_len(p_start, p_now)); p_prev = p_now
            if step == S: mu0 = float(np.mean(eu)); mu = mu0
            elif step > S: mu = (1 - LAM) * mu + LAM * eu[-1]
            if a in (None, "ermix") or t == 0 or step < S or fired >= len(DAYS): continue
            if a["clock"] == "fir": due = step >= fir_steps[fired]
            else:
                if a["clock"] == "steps": val, day = step, S
                elif a["clock"] == "chord": val, day = ch[-1], ch[S - 1]
                else:
                    seq = eu if a["clock"] == "euclid" else fi
                    val = float(np.sum(seq)); day = (float(np.sum(seq[:S])) if a["unit"] == "sum" else S * float(np.median(seq[:S])))
                due = day > 0 and val >= DAYS[fired] * day
            if due:
                replay_event(); fired += 1; p_prev = model.probs(probe)
        if a not in (None, "ermix") and t > 0:
            while fired < len(DAYS): replay_event(); fired += 1           # unreached thresholds fire at the task's end
            replay_event()                                                # end-of-task consolidation (Algorithm 1, line 23)
        # settle the occasion: anchor, buffer, surplus S = C - C* on the Fisher probe (D4)
        anchors.append([x.copy() for x in model.p])
        k = np.random.default_rng(50_000 + 97 * seed + t).choice(len(Xtr), BUF_PER, replace=False); buf.append((Xtr[k], Ytr[k]))
        surplus.append(max(float(np.sum(fi)) - ch[-1], 0.0))
        for j in range(t + 1):
            acc[t, j] = 100.0 * float(np.mean(np.argmax(model.probs(tasks[j][2]), 1) == tasks[j][3]))
    op = float(np.mean(acc[T - 1])); bwt = float(np.mean([acc[T - 1, j] - acc[j, j] for j in range(T - 1)]))
    return dict(world=w, seed=seed, arm=arm, op=op, bwt=bwt, replay_batches=replay_batches, S=S)


def _job(args): return run(*args)


def label(d, step):
    m = float(np.mean(d)); return "AHEAD" if m > step else "BEHIND" if m < -step else "TIE"


def main():
    print("Comparative investigation: CRR against FOREVER on synthetic continual-learning worlds (Continuous_Learning/FOREVER/DECLARATION_2.md)")
    print(f"constants: days {DAYS}, S {S_DEFAULT}, EMA lambda {LAM}, clip [{GMIN}, {GMAX}], gamma {GAMMA}; replay event {R_EV} steps; buffer {BUF_PER}/task; "
          f"{STEPS} steps/task; batch {BS}; lr {LR}; q {Q_AGE}; Omega {OMEGA}, EMA {EMA_S}, cap {WCAP:g}; seeds {SEEDS[0]}-{SEEDS[-1]}")
    with mp.Pool(4) as pool:
        tune = pool.map(_job, [("W1 base", s, "F FOREVER", b) for b in BETA_GRID for s in TUNE_SEEDS])
        n = len(TUNE_SEEDS)
        scores = {b: float(np.mean([r["op"] for r in tune[i * n:(i + 1) * n]])) for i, b in enumerate(BETA_GRID)}
        beta = max(scores, key=scores.get)
        print("beta_base tuned for FOREVER on W1, tuning seeds 100-104: " + ", ".join(f"{b:g}: {scores[b]:.2f}" for b in BETA_GRID) + f" -> {beta:g}")
        jobs = [(w, s, arm, beta) for w in WORLDS for arm in ARMS for s in SEEDS]
        res = pool.map(_job, jobs)
        sens = pool.map(_job, [(w, s, arm, beta, Sx) for w in ("W2 null movement", "W5 convex") for Sx in (12, 48)
                               for arm in ("F FOREVER", "C1 Fisher arc") for s in SEEDS])
    R = {(r["world"], r["arm"], r["seed"]): r for r in res}
    labels = {}
    for w in WORLDS:
        print(f"\n== {w}  ({WORLDS[w]['model']}, K {WORLDS[w]['K']}, {WORLDS[w]['T']} tasks)")
        f = np.array([R[(w, 'F FOREVER', s)]["op"] for s in SEEDS])
        print("   arm | OP mean (sd) | BWT mean | replay batches/run | vs F: mean diff, step, label")
        for arm in ARMS:
            o = np.array([R[(w, arm, s)]["op"] for s in SEEDS]); b = np.mean([R[(w, arm, s)]["bwt"] for s in SEEDS])
            rb = int(np.mean([R[(w, arm, s)]["replay_batches"] for s in SEEDS]))
            if arm == "F FOREVER":
                print(f"   {arm} | {o.mean():.2f} ({o.std(ddof=1):.2f}) | {b:.2f} | {rb} | reference"); continue
            d = o - f; step = max(1.0, 2 * d.std(ddof=1) / np.sqrt(len(d))); lab = label(d, step); labels[(w, arm)] = lab
            print(f"   {arm} | {o.mean():.2f} ({o.std(ddof=1):.2f}) | {b:.2f} | {rb} | {d.mean():+.2f}, {step:.2f}, {lab}")
    # headroom precondition H0 (Amendment 1): fine-tune mean BWT <= -10 and FOREVER mean OP <= 95
    H0 = {}
    print("\n== headroom H0 (Amendment 1): fine-tune mean BWT <= -10 and FOREVER mean OP <= 95")
    for w in WORLDS:
        bw = float(np.mean([R[(w, 'B0 fine-tune', s)]["bwt"] for s in SEEDS])); fo = float(np.mean([R[(w, 'F FOREVER', s)]["op"] for s in SEEDS]))
        H0[w] = bw <= -10 and fo <= 95
        print(f"   {w}: fine-tune BWT {bw:.2f}, FOREVER OP {fo:.2f} -> {'holds' if H0[w] else 'FAILS: reported, excluded from the gate and the predictions'}")
    print(f"   worlds excluded: {sum(not v for v in H0.values())} of {len(H0)}")
    # sensitivity: C1 vs F in W2 and W5 at S = 12 and 48
    SR = {(r["world"], r["arm"], r["seed"], r["S"]): r for r in sens}
    print("\n== sensitivity: C1 against F at S = 12 and 48 (primary S = 24)")
    flips = 0
    for w in ("W2 null movement", "W5 convex"):
        for Sx in (12, 48):
            d = np.array([SR[(w, 'C1 Fisher arc', s, Sx)]["op"] - SR[(w, 'F FOREVER', s, Sx)]["op"] for s in SEEDS])
            step = max(1.0, 2 * d.std(ddof=1) / np.sqrt(len(d))); lab = label(d, step); flip = lab != labels[(w, "C1 Fisher arc")]; flips += flip
            print(f"   {w}, S {Sx}: {d.mean():+.2f}, step {step:.2f}, {lab}{' (flips)' if flip else ''}")
    print(f"   flips {flips} of 4 -> {'FRAGILE' if flips > 1 else 'not fragile'}")
    # gate for the clock claims
    if not (H0["W5 convex"] and H0["W2 null movement"]):
        print("\n== gate for the clock claims: a gate world fails H0 -> GATE NOT DECIDABLE"); g_fail = g_pass = False
    g_fail = H0["W5 convex"] and all(labels[("W5 convex", c)] != "AHEAD" for c in ("C1 Fisher arc", "C2 + A1' unit", "C3 Fisher chord"))
    g_pass = H0["W2 null movement"] and labels[("W2 null movement", "C1 Fisher arc")] == "AHEAD"
    print(f"\n== gate for the clock claims: no clock arm AHEAD in W5 (must fail): {g_fail}; C1 AHEAD in W2 (must pass): {g_pass} -> "
          f"{'GATE OPEN' if g_fail and g_pass else 'GATE CLOSED'}")
    L = labels; W = [w for w in WORLDS if H0[w]]                    # predictions count only worlds that pass H0
    def lw(w, arm): return L[(w, arm)] if H0[w] else "EXCLUDED"
    preds = {
        "P1 C1 AHEAD of F in W2": lw("W2 null movement", "C1 Fisher arc") == "AHEAD",
        "P2 C1, C2, C3 TIE with F in W5": all(lw("W5 convex", c) == "TIE" for c in ("C1 Fisher arc", "C2 + A1' unit", "C3 Fisher chord")),
        "P3 C1 TIE or AHEAD in W3": lw("W3 parametrisation", "C1 Fisher arc") in ("TIE", "AHEAD"),
        "P4 B3 (step clock) BEHIND F in W4": lw("W4 learning rates", "B3 STC") == "BEHIND",
        "P5 C4 TIE in W1": lw("W1 base", "C4 H-EQ weight") == "TIE",
        "P6 C5 TIE in W1-W6 and not BEHIND in W7": all(L[(w, "C5 A6 anchor")] == "TIE" for w in W if w != "W7 long") and lw("W7 long", "C5 A6 anchor") not in ("BEHIND", "EXCLUDED"),
        "P7 C6 BEHIND in at least one of W1, W6, W7": any(lw(w, "C6 P3 sampling") == "BEHIND" for w in ("W1 base", "W6 class-incremental", "W7 long")),
        "P8 C7 TIE everywhere": all(L[(w, "C7 P2 sampling")] == "TIE" for w in W),
        "P9 B1 AHEAD in at least 5 of 7 (of the worlds passing H0, scaled: >= 5/7 of them)": sum(L[(w, "B1 ER-mix")] == "AHEAD" for w in W) >= 5 * len(W) / 7,
        "P10 CRR-full not BEHIND in at least 4 of 7 (scaled: >= 4/7 of the worlds passing H0)": sum(L[(w, "CRR-full")] != "BEHIND" for w in W) >= 4 * len(W) / 7,
    }
    print("\n== predictions")
    for k, v in preds.items(): print(f"   {k}: {'HOLDS' if v else 'FAILS'}")
    print(f"\n== label counts per arm across the {len(W)} worlds passing H0 (AHEAD / TIE / BEHIND against F)")
    for arm in ARMS:
        if arm == "F FOREVER": continue
        c = [L[(w, arm)] for w in W]
        print(f"   {arm}: {c.count('AHEAD')} / {c.count('TIE')} / {c.count('BEHIND')}  ({', '.join(c)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
