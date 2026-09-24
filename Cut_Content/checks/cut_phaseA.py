"""CUT1 Phase A: when does a cut need content? Synthetic battery A0-A7, as declared in Cut_Content/DECLARATION.md
(6eef1f7) and its Amendment 1 (d08aa21), both pushed before this file existed. No real data. Seeded; every verdict word is
computed from the numbers (R15).

Run: uv run python Cut_Content/checks/cut_phaseA.py > Cut_Content/checks/cut_phaseA.txt"""
import math
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

SEEDS = (0, 1, 2)
BS = 10
LR = {"sgd": 0.05, "adam": 0.001}
ARMS = ("E0", "R-hard", "R-soft", "SP", "Head", "ReDo0")
L2_GRID = (1e-4, 1e-3, 1e-2)
SP_SHRINK, SP_NOISE = 0.5, 0.01
OP_P, OP_L, KAPPA = 0.02, 5, 1e-3


# ------------------------------------------------------------------ the network
def init_params(rng, d, K, h):
    if h == 0:
        return [rng.normal(0, math.sqrt(1 / d), (d, K)), np.zeros(K)]
    return [rng.normal(0, math.sqrt(2 / d), (d, h)), np.zeros(h), rng.normal(0, math.sqrt(2 / h), (h, K)), np.zeros(K)]


def forward(p, x):
    if len(p) == 2:
        return None, x @ p[0] + p[1]
    act = np.maximum(0, x @ p[0] + p[1]); return act, act @ p[2] + p[3]


def grads(p, x, y):
    act, z = forward(p, x); z = z - z.max(1, keepdims=True); e = np.exp(z); pr = e / e.sum(1, keepdims=True)
    n = len(y); dz = pr; dz[np.arange(n), y] -= 1; dz /= n
    if len(p) == 2:
        return [x.T @ dz, dz.sum(0)]
    dh = dz @ p[2].T; dh[act <= 0] = 0
    return [x.T @ dh, dh.sum(0), act.T @ dz, dz.sum(0)]


def acc(p, x, y):
    with np.errstate(all="ignore"):
        z = forward(p, x)[1]
    return 0.0 if not np.all(np.isfinite(z)) else float((z.argmax(1) == y).mean())


class Opt:
    def __init__(s, kind, p):
        s.kind = kind; s.lr = LR[kind]; s.t = 0
        s.m = [np.zeros_like(a) for a in p]; s.v = [np.zeros_like(a) for a in p]

    def step(s, p, g):
        if s.kind == "sgd":
            for a, ga in zip(p, g): a -= s.lr * ga
            return
        s.t += 1; b1, b2, eps = 0.9, 0.999, 1e-8
        for i, (a, ga) in enumerate(zip(p, g)):
            s.m[i] = b1 * s.m[i] + (1 - b1) * ga; s.v[i] = b2 * s.v[i] + (1 - b2) * ga * ga
            mh = s.m[i] / (1 - b1 ** s.t); vh = s.v[i] / (1 - b2 ** s.t); a -= s.lr * mh / (np.sqrt(vh) + eps)


# ------------------------------------------------------------------ the worlds
def world(name, seed, T=None):
    """Returns (d, K, h_default, epochs, tasks); each task = (Xtr, ytr, Xte, yte) with Xte None where not used."""
    rng = np.random.default_rng(10_000 + 97 * seed + sum(map(ord, name)))
    if name == "P":
        X = rng.normal(size=(500, 20)); return 20, 10, None, 20, [(X, rng.integers(0, 10, 500), None, None) for _ in range(T)]
    if name == "N-conv":
        W = rng.normal(size=(20, 4)); tasks = []
        for _ in range(20):
            pi = rng.permutation(20); Xa = rng.normal(size=(600, 20)); ya = (Xa @ W).argmax(1); Xa = Xa[:, pi]
            tasks.append((Xa[:400], ya[:400], Xa[400:], ya[400:]))
        return 20, 4, 0, 3, tasks
    if name == "N-cil":
        mu = rng.normal(0, 2.0, size=(10, 20)); Xtr, ytr, Xte, yte = {}, {}, {}, {}
        for c in range(10):
            Xtr[c] = mu[c] + rng.normal(size=(200, 20)); Xte[c] = mu[c] + rng.normal(size=(100, 20))
        pairs = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)] * 2; tasks = []
        for a, b in pairs:
            tasks.append((np.vstack([Xtr[a], Xtr[b]]), np.array([a] * 200 + [b] * 200), np.vstack([Xte[c] for c in range(10)]),
                          np.repeat(np.arange(10), 100)))
        return 20, 10, 256, 3, tasks
    if name == "N-drift":
        W0 = rng.normal(size=(20, 4)); Wp = rng.normal(size=(20, 4)); Wp -= (np.sum(Wp * W0) / np.sum(W0 * W0)) * W0
        Wp *= np.linalg.norm(W0) / np.linalg.norm(Wp); tasks = []
        for t in range(50):
            Wt = W0 * math.cos(0.05 * t) + Wp * math.sin(0.05 * t); Xa = rng.normal(size=(600, 20)); ya = (Xa @ Wt).argmax(1)
            tasks.append((Xa[:400], ya[:400], Xa[400:], ya[400:]))
        return 20, 4, 256, 3, tasks
    raise ValueError(name)


# ------------------------------------------------------------------ one stream
def run(wname, arm, opt_kind, h, seed, T=None, l2=0.0, operator=False):
    d, K, h_def, epochs, tasks = world(wname, seed, T)
    h = h_def if h is None else h
    rng = np.random.default_rng(seed); init_rng = np.random.default_rng(50_000 + seed)
    p = init_params(rng, d, K, h); p0 = [a.copy() for a in p]; opt = Opt(opt_kind, p)
    op_rng = np.random.default_rng(99_000 + seed); pause = 0; wall = 0; frozen = 0; disables = 0
    plast = []; test_end = []
    for ti, (Xtr, ytr, Xte, yte) in enumerate(tasks):
        n = len(ytr); steps = epochs * int(math.ceil(n / BS)); mid = steps // 2; k = 0; p_start = [a.copy() for a in p]
        if arm == "Fresh" and ti > 0:
            p = init_params(init_rng, d, K, h); opt = Opt(opt_kind, p)
        for ep in range(epochs):
            perm = rng.permutation(n)
            for s in range(0, n, BS):
                if operator:                                   # the lossless cut: the learner is frozen, nothing else moves
                    while pause > 0:
                        pause -= 1; wall += 1; frozen += 1
                    stake = 0.0                                # natural agent, lossless world: the press carries no content
                    if stake > KAPPA: disables += 1
                ii = perm[s:s + BS]; g = grads(p, Xtr[ii], ytr[ii])
                if l2 > 0: g = [ga + l2 * (a - a0) for ga, a, a0 in zip(g, p, p0)]
                with np.errstate(all="ignore"):
                    opt.step(p, g)
                k += 1
                if operator:
                    wall += 1
                    if op_rng.uniform() < OP_P: pause = OP_L
                if k == mid and arm in ("R-hard", "R-soft"):
                    w = 1.0 if arm == "R-hard" else 0.5
                    for a, a_s in zip(p, p_start): a[...] = w * a_s + (1 - w) * a
        plast.append(acc(p, Xtr, ytr) if Xte is None else acc(p, Xte, yte))
        if ti < len(tasks) - 1:
            if arm == "SP":
                eps = init_params(init_rng, d, K, h)
                for a, e_ in zip(p, eps): a[...] = SP_SHRINK * a + SP_NOISE * e_
            elif arm == "Head":
                q = init_params(init_rng, d, K, h)
                if h == 0: p[0][...] = q[0]; p[1][...] = q[1]
                else: p[2][...] = q[2]; p[3][...] = q[3]
            elif arm == "ReDo0" and h > 0:
                act = np.maximum(0, Xtr @ p[0] + p[1]); dead = np.where(np.all(act <= 0, axis=0))[0]
                if dead.size:
                    q = init_params(init_rng, d, K, h); p[0][:, dead] = q[0][:, dead]; p[1][dead] = 0.0; p[2][dead, :] = 0.0
    if wname in ("N-conv",):
        final = float(np.mean([acc(p, t[2], t[3]) for t in tasks]))
    elif wname == "N-cil":
        final = acc(p, tasks[-1][2], tasks[-1][3])
    else:
        final = float("nan")
    tail = max(1, int(round(0.2 * len(tasks))))
    return dict(plast=100 * float(np.mean(plast[-tail:])), final=100 * final, flat=np.concatenate([a.ravel() for a in p]),
                wall=wall, frozen=frozen, disables=disables)


# ------------------------------------------------------------------ scoring helpers
def step_of(v):
    v = np.asarray(v, float); return max(1.0, 2 * float(np.std(v, ddof=1)) / math.sqrt(len(v)))


def arm_values(wname, arm, opt_kind, h, T, metric):
    if arm == "L2-Init":
        best = None
        for lam in L2_GRID:
            vals = [run(wname, "E0", opt_kind, h, s, T, l2=lam)[metric] for s in SEEDS]
            if best is None or np.mean(vals) > np.mean(best[1]): best = (lam, vals)
        return best
    return (None, [run(wname, arm, opt_kind, h, s, T)[metric] for s in SEEDS])


def fmt(v): return "[" + " ".join(f"{x:.2f}" for x in v) + "]"


def main():
    print("CUT1 Phase A: when does a cut need content? (Cut_Content/DECLARATION.md + Amendment 1)")
    print(f"seeds {SEEDS}; batch {BS}; lr {LR}; SP shrink {SP_SHRINK} noise {SP_NOISE}; L2-Init grid {L2_GRID} (tuned in-sample)")
    res = {}; valid = []
    print("\n== World P (random-label memorisation, 500 points, d 20, K 10, 20 epochs per task): plasticity = end-of-task training accuracy, mean of the last 20 % of tasks")
    for T in (5, 20, 50):
        for h in (256, 32):
            for ok in ("sgd", "adam"):
                cell = f"P T{T} w{h} {ok}"; vals = {}
                for arm in ARMS + ("L2-Init", "Fresh"):
                    lam, v = arm_values("P", arm, ok, h, T, "plast"); vals[arm] = (lam, v)
                e0 = vals["E0"][1]; st = step_of(e0); gap = float(np.mean(vals["Fresh"][1]) - np.mean(e0))
                is_valid = gap >= st; res[cell] = dict(vals=vals, step=st, valid=is_valid)
                if is_valid: valid.append(cell)
                print(f"   {cell}: step {st:.2f}; Fresh - E0 = {gap:+.2f} -> {'VALID (plasticity loss)' if is_valid else 'not valid (no plasticity loss)'}")
                for arm, (lam, v) in vals.items():
                    dlt = float(np.mean(v) - np.mean(e0))
                    print(f"      {arm:8s}{'' if lam is None else f' (lambda {lam:g})'}: mean {np.mean(v):.2f} {fmt(v)}; vs E0 {dlt:+.2f}")
    a0 = len(valid) > 0
    a1 = all(np.mean(res[c]["vals"]["SP"][1]) - np.mean(res[c]["vals"]["E0"][1]) >= res[c]["step"] for c in valid) if a0 else None
    a2 = all(np.mean(res[c]["vals"]["L2-Init"][1]) - np.mean(res[c]["vals"]["E0"][1]) >= res[c]["step"] for c in valid) if a0 else None
    a3 = all(np.mean(res[c]["vals"]["R-hard"][1]) - np.mean(res[c]["vals"]["E0"][1]) < res[c]["step"] for c in valid) if a0 else None
    print("\n== The must-fail worlds")
    mf = {}
    for wname, metrics in (("N-conv", ("final", "plast")), ("N-cil", ("final",)), ("N-drift", ("plast",))):
        opt_kind = "sgd"; h = None
        for metric in metrics:
            vals = {}
            for arm in ARMS + ("L2-Init", "Fresh"):
                if wname == "N-conv" and arm == "ReDo0":
                    continue
                vals[arm] = arm_values(wname, arm, opt_kind, h, None, metric)
            e0 = vals["E0"][1]; st = step_of(e0)
            beats = [a for a in ("R-hard", "R-soft", "SP", "Head", "ReDo0") if a in vals and np.mean(vals[a][1]) - np.mean(e0) >= st]
            mf[(wname, metric)] = dict(beats=beats, vals=vals, step=st)
            print(f"   {wname} {metric} (step {st:.2f}); content cuts beating E0 by a step: {beats or 'none'}"
                  + (" (ReDo0 n/a: no hidden layer)" if wname == "N-conv" else ""))
            for arm, (lam, v) in vals.items():
                print(f"      {arm:8s}{'' if lam is None else f' (lambda {lam:g})'}: mean {np.mean(v):.2f} {fmt(v)}; vs E0 {np.mean(v) - np.mean(e0):+.2f}")
    a4 = not mf[("N-conv", "final")]["beats"] and not mf[("N-conv", "plast")]["beats"]
    cil = mf[("N-cil", "final")]; e0c = np.mean(cil["vals"]["E0"][1])
    a5 = not cil["beats"] and all(e0c - np.mean(cil["vals"][a][1]) >= cil["step"] for a in ("SP", "Head"))
    a6 = not mf[("N-drift", "plast")]["beats"]
    print("\n== A7 safety construction: lossless operator pauses (p 0.02, 5 frozen wall steps) against no operator, every arm")
    a7 = True; cellP = valid[0] if valid else "P T5 w256 sgd"
    _, Tp, hp, okp = cellP.split(); Tp = int(Tp[1:]); hp = int(hp[1:])
    for wname, T, h, ok in (("P", Tp, hp, okp), ("N-cil", None, None, "sgd")):
        for arm in ARMS + ("Fresh",):
            a = run(wname, arm, ok, h, 0, T); b = run(wname, arm, ok, h, 0, T, operator=True)
            same = bool(np.array_equal(a["flat"], b["flat"])); a7 &= same and b["disables"] == 0
            print(f"   {wname}{'' if T is None else f' T{T} w{h} {ok}'} {arm:7s}: parameters identical {same}; disables {b['disables']}; frozen wall steps {b['frozen']} of {b['wall']}")
    fmtb = lambda x: "n/a (no valid P cell)" if x is None else ("holds" if x else "FAILS")
    print(f"\nA0 plasticity loss present in {len(valid)} of 12 P cells: {', '.join(valid) or 'none'}")
    print(f"A1 SP beats E0 in every valid cell: {fmtb(a1)}; A2 L2-Init beats E0 in every valid cell: {fmtb(a2)}; A3 R-hard does not beat E0 in any valid cell: {fmtb(a3)}")
    print(f"A4 convex world, no content cut ahead: {fmtb(a4)}; A5 class-incremental, none ahead and SP and Head behind: {fmtb(a5)}; A6 drift, none ahead: {fmtb(a6)}; A7 safety construction: {fmtb(a7)}")
    if not (a4 and a5 and a6 and a7):
        verdict = "GATE CLOSED"
    elif not a0:
        verdict = "GATE CLOSED for plasticity (no valid P cell); OPEN for harm and safety"
    else:
        verdict = "GATE OPEN" if (a1 and a2 and a3) else "GATE CLOSED"
    print(f"summary: {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
