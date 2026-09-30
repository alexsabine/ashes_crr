"""RRM2 T4 (DECLARATION_2.md Part T, pushed at a2719f0 before this file): sensitivity, report only.
(a) drift worlds (DECLARATION.md section 3, SHARED and ROT), RRM-1: anchors per first-task class in {2, 5, 10, 20} x
    beta in {0.001, 0.01, 0.1} x eps in {0.02, 0.05, 0.1}; plus the anchor source 'spread' (2 rows per class of every
    class, chosen at the start: uses future data, an ORACLE DESIGN) at 10/class-equivalent M = 20, beta 0.01.
(b) T1 DIAG on POS (FT and ANCH1 learners): anchors per first-task class in {2, 5, 10, 20} x beta in {0.001, 0.01, 0.1}:
    drift explained and NCM RRM - STALE (the anchors replayed by ANCH1 change with the count).
No gate. Seeds 0-4. Run: uv run python Relational_Reference_Memory/checks/t4_sens.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "Replay_Quality_Memory" / "checks"))
import rrm_lib as L  # noqa: E402
import t_lib as T  # noqa: E402
import worlds as W  # noqa: E402
import phase_a as PA  # noqa: E402

SEEDS = (0, 1, 2, 3, 4)


def world_run(regime, seed, data, K, m, beta, eps, source):
    Xtr, ytr, Xte, yte = data
    W.EPS = eps; w = W.World(regime, seed, Xtr.shape[1]); arng = np.random.default_rng(30_000 + seed)
    tasks = L.R.tasks_of(K)
    if source == "spread":
        anchors = np.concatenate([arng.permutation(np.where(ytr == c)[0])[:2] for c in range(K)])
    stored = {}
    for j, task in enumerate(tasks):
        if source == "first" and j == 0:
            anchors = np.concatenate([arng.permutation(np.where(ytr == c)[0])[:m] for c in task])
        HA = w.f(Xtr[anchors]); Rm = L.relation(HA, beta)
        for c in task:
            stored[c] = (w.f(Xtr[ytr == c]).mean(0), HA, Rm)
        for _ in range(W.T):
            w.step()
    Zte = w.f(Xte); HA_now = w.f(Xtr[anchors])
    o = W.ncm(Zte, yte, {c: w.f(Xtr[ytr == c]).mean(0) for c in range(K)})
    s = W.ncm(Zte, yte, {c: v[0] for c, v in stored.items()})
    r = W.ncm(Zte, yte, {c: L.transport(mu[None], HA, HA_now, Rm)[0] for c, (mu, HA, Rm) in stored.items()})
    return o, s, r


def main():
    Xtr, ytr, Xte, yte, K = W.data(); data = (Xtr, ytr, Xte, yte)
    print("RRM2 T4 sensitivity (report only; DECLARATION_2.md Part T); seeds 0-4")
    print("\n(a) drift worlds, RRM-1: mean NCM accuracy (%) ORACLE / STALE / RRM, and RRM - STALE, ORACLE - RRM")
    for regime in ("SHARED", "ROT"):
        for eps in (0.02, 0.05, 0.1):
            for m in (2, 5, 10, 20):
                for beta in (0.001, 0.01, 0.1):
                    v = np.array([world_run(regime, s, data, K, m, beta, eps, "first") for s in SEEDS]).mean(0)
                    print(f"   {regime:6} eps {eps:<5} anchors/class {m:2} beta {beta:<6} {v[0]:6.2f} {v[1]:6.2f} {v[2]:6.2f}   "
                          f"{v[2] - v[1]:+7.2f} {v[0] - v[2]:+7.2f}")
            v = np.array([world_run(regime, s, data, K, 10, 0.01, eps, "spread") for s in SEEDS]).mean(0)
            print(f"   {regime:6} eps {eps:<5} SPREAD (oracle design) M 20 beta 0.01 {v[0]:6.2f} {v[1]:6.2f} {v[2]:6.2f}   "
                  f"{v[2] - v[1]:+7.2f} {v[0] - v[2]:+7.2f}")
    W.EPS = 0.05
    print("\n(b) T1 DIAG on POS: drift explained (1 - err_RRM/err_STALE) and NCM RRM - STALE, seed means")
    pdata, pK = PA.stream("POS"); pXtr, pytr, pXte, pyte = pdata
    for learner in ("FT", "ANCH1"):
        for m in (2, 5, 10, 20):
            for beta in (0.001, 0.01, 0.1):
                es, er, dn = [], [], []
                for s in SEEDS:
                    net, anchors, rec, cuts = T.train(s, *pdata, pK, learner, m_first=m, beta=beta)
                    P = {w: T.prototypes(net, pXtr, pytr, anchors, rec, cuts, s, w) for w in ("ORACLE", "STALE", "RRM")}
                    old = [c for c, (mu, j) in rec.items() if j < len(cuts) - 1]
                    es.append(np.mean([np.linalg.norm(P["STALE"][c] - P["ORACLE"][c]) for c in old]))
                    er.append(np.mean([np.linalg.norm(P["RRM"][c] - P["ORACLE"][c]) for c in old]))
                    dn.append(T.ncm_acc(net, pXte, pyte, P["RRM"]) - T.ncm_acc(net, pXte, pyte, P["STALE"]))
                print(f"   {learner:5} anchors/class {m:2} beta {beta:<6} drift explained {1 - np.mean(er) / np.mean(es):+.4f}  "
                      f"NCM RRM - STALE {np.mean(dn):+.4f}")


if __name__ == "__main__":
    main()
