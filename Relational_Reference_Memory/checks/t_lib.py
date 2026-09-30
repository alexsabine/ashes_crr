"""RRM2 test harness (DECLARATION_2.md Part T, pushed at a2719f0 before this file): learners with a drift record, for T1 (drift
diagnostic) and T3 (relational nearest-class-mean), and the list of the 30 SEEN carriers.

train(seed, data, K, learner) trains SEC1's MLP as one of
  FT     plain fine-tuning (anchors chosen for measurement only, never replayed)
  ANCH1  replay of the 20 first-task anchors (10 per class of task 1), as RRM-1's anchor replay
  ER20   experience replay with 20 raw rows per class (rqm_lib.run_er_pc's buffer rule)
and records at every cut: each settled class's feature mean (the STALE prototype), the first-task anchors' features H_A(cut)
and the relation map R. Anchor selection matches rrm_lib.run_rrm (form '1'): default_rng(30_000 + seed), 10 rows per class
of the first task, drawn at the first cut.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rrm_lib as L  # noqa: E402

R = L.R; S = L.S


def train(seed, Xtr, ytr, Xte, yte, K, learner, m_first=L.M_FIRST, beta=L.BETA, per_task=2, er_m=20):
    rng = np.random.default_rng(seed); net = S.MLP(rng, Xtr.shape[1], K, h=L.HID)
    arng = np.random.default_rng(30_000 + seed); brng = np.random.default_rng(10_000 + seed)
    anchors = np.zeros(0, dtype=int); bufX = np.zeros((0, Xtr.shape[1])); bufy = np.zeros(0, dtype=ytr.dtype)
    rec = {}          # class -> (stale mean, cut index)
    cuts = []         # per cut: (HA_cut, R)
    with np.errstate(all="ignore"):
        for j, task in enumerate(R.tasks_of(K, per_task)):
            ii = np.where(np.isin(ytr, task))[0]; X, y = Xtr[ii], ytr[ii]
            for _ in range(L.EPOCHS):
                perm = rng.permutation(len(y))
                for t in range(0, len(perm), L.BS):
                    jj = perm[t:t + L.BS]; x, yy = X[jj], y[jj]
                    if learner == "ANCH1" and len(anchors):
                        aa = anchors[brng.integers(0, len(anchors), L.ANCHOR_BS)]
                        x = np.concatenate([x, Xtr[aa]]); yy = np.concatenate([yy, ytr[aa]])
                    elif learner == "ER20" and len(bufy):
                        kk = brng.integers(0, len(bufy), len(yy))
                        x = np.concatenate([x, bufX[kk]]); yy = np.concatenate([yy, bufy[kk]])
                    _, g = S.ce_loss_grad(net, x, yy); net.set_flat(net.flat() - L.LR * g)
            if j == 0:
                anchors = np.concatenate([arng.permutation(np.where(ytr == c)[0])[:m_first] for c in task])
            if learner == "ER20":
                for c in task:
                    cc = np.where(ytr == c)[0]; pick = brng.permutation(cc)[:er_m]
                    bufX = np.concatenate([bufX, Xtr[pick]]); bufy = np.concatenate([bufy, ytr[pick]])
            HA = net.forward(Xtr[anchors])[0]; cuts.append((HA, L.relation(HA, beta)))
            for c in task:
                rec[c] = (net.forward(Xtr[ytr == c])[0].mean(0), j)
    return net, anchors, rec, cuts


def prototypes(net, Xtr, ytr, anchors, rec, cuts, seed, which):
    """which: ORACLE (current means), STALE, RRM (transported by the first-task anchors), DECOY (permuted anchors), HOPDC
    (HopDC's transport of the stored mean on the same anchors; DECLARATION_2 Amendment 1)."""
    out = {}
    with np.errstate(all="ignore"):
        HA_now = net.forward(Xtr[anchors])[0]
        perm = np.random.default_rng(40_000 + seed).permutation(len(anchors))
        for c, (mu, j) in rec.items():
            if which == "ORACLE":
                out[c] = net.forward(Xtr[ytr == c])[0].mean(0)
            elif which == "STALE":
                out[c] = mu
            elif which == "HOPDC":
                HA, Rm = cuts[j]
                out[c] = L.hopdc_transport(mu[None], HA, HA_now)[0]
            else:
                HA, Rm = cuts[j]
                out[c] = L.transport(mu[None], HA, HA_now[perm] if which == "DECOY" else HA_now, Rm)[0]
    return out


def ncm_acc(net, Xte, yte, protos):
    with np.errstate(all="ignore"):
        Z = net.forward(Xte)[0]
    cs = sorted(protos); P = np.stack([protos[c] for c in cs])
    d2 = (Z ** 2).sum(1)[:, None] - 2 * Z @ P.T + (P ** 2).sum(1)[None, :]
    return 100 * float((np.array(cs)[d2.argmin(1)] == yte).mean())


def seen_carriers():
    """The 30 SEEN carriers of RQM's DEV_DECLARATION: every carrier of SCL3, SEC3, SEC4 and SEC5 that the loader keeps."""
    P5 = R.P5
    out = []
    for study, table in (("scl3", P5.P3.SCL3_DATASETS), ("sec3", P5.P3.DATASETS), ("sec4", P5.P4.DATASETS), ("sec5", P5.DATASETS)):
        for did in dict(table):
            out.append((study, did))
    return out


CACHE = Path("/tmp/claude-0/rrm_cache")


def load_seen_cached(study, did):
    """R.load_seen through an npz cache outside the repository (the ARFF parse is slow); None if the loader excludes it."""
    CACHE.mkdir(parents=True, exist_ok=True); f = CACHE / f"{study}_{did}.npz"
    if f.exists():
        z = np.load(f, allow_pickle=False)
        if int(z["excluded"]):
            return None
        return z["Xtr"], z["ytr"], z["Xte"], z["yte"], int(z["K"]), str(z["name"])
    d = R.load_seen(did, study)
    if d is None:
        np.savez(f, excluded=1); return None
    Xtr, ytr, Xte, yte, K, name = d
    np.savez(f, excluded=0, Xtr=Xtr, ytr=ytr, Xte=Xte, yte=yte, K=K, name=name)
    return d
