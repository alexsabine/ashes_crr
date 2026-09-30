"""RRM Phase A part 1 (DECLARATION.md section 3, pushed at 3a740f1 before this file): the transport mechanism in controlled
drift worlds, no learner. K = 10 Gaussian classes in d = 20 (SEC1's synthetic stream, split and standardised as SEC1), two
classes per task; a feature map f0(x) = ReLU(W0 x + b0) with 256 units; after every cut the map changes by T = 20 increments.
Score: nearest-class-mean accuracy (%) of the final features of the held-out rows of all classes, with each method's
prototypes. Seeds 0-4; step = max(1, 2 x SE over seeds) of the second arm of each comparison. Words computed (R15).
Run: uv run python Relational_Reference_Memory/checks/worlds.py
"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rrm_lib as L  # noqa: E402

S = L.S
SEEDS = (0, 1, 2, 3, 4)
H = 256; T = 20; EPS = 0.05


def data():
    X, y = S._synthetic(); Xs, ys, meta = L.R.L.select_classes(X, y, 10); K = meta["classes_used"]
    return (*S.split_standardise(Xs, ys, K), K)


class World:
    def __init__(s, regime, seed, d):
        s.regime = regime; s.r = np.random.default_rng(50_000 + seed); s.d = d
        s.W = s.r.normal(0, math.sqrt(2 / d), (d, H)); s.b = s.r.normal(0, 0.1, H); s.L = np.eye(H)

    def f(s, X):
        return np.maximum(0.0, X @ s.W + s.b) @ s.L.T

    def step(s):
        if s.regime == "UNSHARED":
            s.W = s.r.normal(0, math.sqrt(2 / s.d), (s.d, H)); s.b = s.r.normal(0, 0.1, H); return
        F = np.eye(H) + EPS * s.r.normal(0, 1 / math.sqrt(H), (H, H))
        if s.regime == "ROT":
            Q, Rr = np.linalg.qr(F); F = Q * np.sign(np.diag(Rr))
        s.L = F @ s.L


def ncm(Z, y, protos):
    cs = sorted(protos); P = np.stack([protos[c] for c in cs])
    d2 = ((Z[:, None, :] - P[None, :, :]) ** 2).sum(2)
    return 100 * float((np.array(cs)[d2.argmin(1)] == y).mean())


def one(regime, seed, Xtr, ytr, Xte, yte, K, form):
    w = World(regime, seed, Xtr.shape[1]); arng = np.random.default_rng(30_000 + seed); drng = np.random.default_rng(40_000 + seed)
    anchors = np.zeros(0, dtype=int); stored = {}
    for j, task in enumerate(L.R.tasks_of(K)):
        if form == "1":
            if j == 0:
                anchors = np.concatenate([arng.permutation(np.where(ytr == c)[0])[:L.M_FIRST] for c in task])
        else:
            anchors = np.concatenate([anchors] + [arng.permutation(np.where(ytr == c)[0])[:L.M_ACC] for c in task])
        idx = anchors.copy(); HA = w.f(Xtr[idx]); Rm = L.relation(HA); perm = drng.permutation(len(idx))
        for c in task:
            stored[c] = (w.f(Xtr[ytr == c]).mean(0), idx, HA, Rm, perm)
        for _ in range(T):
            w.step()
    Zte = w.f(Xte); out = {}
    out["ORACLE"] = ncm(Zte, yte, {c: w.f(Xtr[ytr == c]).mean(0) for c in range(K)})
    out["STALE"] = ncm(Zte, yte, {c: stored[c][0] for c in range(K)})
    out["RRM"] = ncm(Zte, yte, {c: L.transport(mu[None], HA, w.f(Xtr[idx]), Rm)[0] for c, (mu, idx, HA, Rm, perm) in stored.items()})
    out["DECOY"] = ncm(Zte, yte, {c: L.transport(mu[None], HA, w.f(Xtr[idx])[perm], Rm)[0] for c, (mu, idx, HA, Rm, perm) in stored.items()})
    return out


def step_of(v): return max(1.0, 2 * float(np.std(v, ddof=1)) / math.sqrt(len(v)))


def main():
    Xtr, ytr, Xte, yte, K = data()
    print(f"RRM Phase A part 1: drift worlds (DECLARATION.md section 3); K {K}, d {Xtr.shape[1]}, H {H}, T {T} increments per task, "
          f"eps {EPS}, beta {L.BETA}; anchors RRM-1 {L.M_FIRST}/class of task 1, RRM-A {L.M_ACC}/class per cut; seeds 0-4; NCM accuracy (%)")
    res = {}
    for form in ("1", "A"):
        for regime in ("SHARED", "ROT", "UNSHARED"):
            rows = [one(regime, s, Xtr, ytr, Xte, yte, K, form) for s in SEEDS]
            res[(form, regime)] = {k: [r[k] for r in rows] for k in rows[0]}
            print(f"\n[RRM-{form} {regime}]")
            for k, v in res[(form, regime)].items():
                print(f"   {k:7} mean {np.mean(v):7.2f}  seeds " + " ".join(f"{x:6.2f}" for x in v))
    print("\n" + "-" * 100)
    ok = {}
    for form in ("1", "A"):
        for regime in ("SHARED", "ROT"):
            a = res[(form, regime)]; st = step_of(a["STALE"]); d1 = np.mean(a["RRM"]) - np.mean(a["STALE"])
            so = step_of(a["ORACLE"]); d2 = np.mean(a["ORACLE"]) - np.mean(a["RRM"])
            ok[f"S-{form}-{regime}"] = d1 > st and d2 <= so
            print(f"G-SHARED RRM-{form} {regime}: RRM - STALE {d1:+.4f} (step {st:.4f}); ORACLE - RRM {d2:+.4f} (step {so:.4f}) -> "
                  f"{'holds' if ok[f'S-{form}-{regime}'] else 'FAILS'}")
        a = res[(form, "UNSHARED")]; so = step_of(a["RRM"]); d = np.mean(a["ORACLE"]) - np.mean(a["RRM"])
        ok[f"U-{form}"] = d > so
        print(f"G-UNSHARED RRM-{form}: ORACLE - RRM {d:+.4f} (step {so:.4f}): must be ahead by more than a step -> {'holds' if ok[f'U-{form}'] else 'FAILS'}")
        a = res[(form, "SHARED")]; sd = step_of(a["DECOY"]); d = np.mean(a["RRM"]) - np.mean(a["DECOY"])
        ok[f"D-{form}"] = d > sd
        print(f"G-DECOY RRM-{form} SHARED: RRM - DECOY {d:+.4f} (step {sd:.4f}) -> {'holds' if ok[f'D-{form}'] else 'FAILS'}")
    print("PART 1 GATE " + ("OPEN" if all(ok.values()) else "CLOSED"))


if __name__ == "__main__":
    main()
