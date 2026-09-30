"""RRM arms (Relational_Reference_Memory/DECLARATION.md, pushed at 3a740f1 before this file): anchor-referenced transport of
stored feature Gaussians on SEC1's learner, with its controls. Shared baselines (FT, JOINT, ER, IGR, RFR) come from RQM's
harness (Replay_Quality_Memory/checks/rqm_lib.py) unchanged.

The transport (DECLARATION.md section 1): at a cut, anchors' hidden features H_A (M x h) and the relation map
R = (H_A H_A^T + beta_bar I)^-1 H_A, beta_bar = beta tr(H_A H_A^T) / M, are stored; a stored feature h is replayed as
h' = h + (H_A(now) - H_A(cut))^T R h. Exact (beta -> 0) when features change by a linear map and h lies in the anchors' span.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "Replay_Quality_Memory" / "checks"))
import rqm_lib as R  # noqa: E402

S = R.S
LR, BS, EPOCHS, HID = R.LR, R.BS, R.EPOCHS, R.HID
BETA = 0.01
M_FIRST = 10          # RRM-1: anchor rows per class of the first task (M = 20 with 2 classes per task)
M_ACC = 2             # RRM-A: anchor rows added per class at each cut
PSEUDO_BS = 10        # pseudo-features per step
ANCHOR_BS = 10        # anchor rows replayed per step


def relation(HA, beta=BETA):
    G = HA @ HA.T; M = len(HA); bb = beta * float(np.trace(G)) / M
    return np.linalg.solve(G + (bb if bb > 0 else beta) * np.eye(M), HA)


def transport(H, HA_cut, HA_now, Rm):
    """Rows of H (n x h) transported by the anchors' movement: H + (H R^T)(HA_now - HA_cut)."""
    return H + (H @ Rm.T) @ (HA_now - HA_cut)


def run_rrm(seed, Xtr, ytr, Xte, yte, K, form="1", mode="rrm", beta=BETA, m_first=M_FIRST, m_acc=M_ACC, per_task=2,
            force_off=False, return_mem=False):
    """mode: 'rrm' (transport), 'stale' (no transport), 'decoy' (transport with H_A(now) row-permuted by a fixed seeded
    permutation), 'anch' (anchor replay only, no feature Gaussians). form '1' (first-task anchors) or 'A' (accumulating)."""
    rng = np.random.default_rng(seed); net = S.MLP(rng, Xtr.shape[1], K, h=HID)
    arng = np.random.default_rng(30_000 + seed); brng = np.random.default_rng(10_000 + seed)
    prng = np.random.default_rng(20_000 + seed); drng = np.random.default_rng(40_000 + seed)
    anchors = np.zeros(0, dtype=int)          # indices into Xtr
    groups = []                                # per cut: (anchor idx, HA_cut, R, perm)
    gauss = {}                                 # class -> (mu, sd, group id)
    rot = [0]
    use_feat = mode != "anch"

    def pseudo(n):
        old = sorted(gauss); cs = [old[(rot[0] + i) % len(old)] for i in range(n)]; rot[0] = (rot[0] + n) % len(old)
        H = np.empty((n, HID)); now = {}
        for i, c in enumerate(cs):
            mu, sd, gid = gauss[c]; h = mu + sd * prng.standard_normal(HID)
            if mode in ("rrm", "decoy") and not force_off:
                idx, HA_cut, Rm, perm = groups[gid]
                if gid not in now:
                    HA_now = net.forward(Xtr[idx])[0]
                    now[gid] = HA_now[perm] if mode == "decoy" else HA_now
                h = transport(h[None, :], HA_cut, now[gid], Rm)[0]
            H[i] = h
        return np.maximum(H, 0.0), np.array(cs, dtype=ytr.dtype)

    with np.errstate(all="ignore"):
        for j, task in enumerate(R.tasks_of(K, per_task)):
            ii = np.where(np.isin(ytr, task))[0]; X, y = Xtr[ii], ytr[ii]
            for _ in range(EPOCHS):
                perm = rng.permutation(len(y))
                for t in range(0, len(perm), BS):
                    jj = perm[t:t + BS]; x, yy = X[jj], y[jj]
                    if len(anchors):
                        aa = anchors[brng.integers(0, len(anchors), ANCHOR_BS)]
                        x = np.concatenate([x, Xtr[aa]]); yy = np.concatenate([yy, ytr[aa]])
                    _, g = S.ce_loss_grad(net, x, yy)
                    if use_feat and gauss:
                        hp, yp = pseudo(PSEUDO_BS)
                        W1, b1, W2, b2 = net.p; z = hp @ W2 + b2; p = S.softmax(z); p[np.arange(len(yp)), yp] -= 1; p /= len(yp)
                        gh = np.concatenate([np.zeros(W1.size + b1.size), (hp.T @ p).ravel(), p.sum(0)])
                        g = (len(yy) * g + len(yp) * gh) / (len(yy) + len(yp))
                    net.set_flat(net.flat() - LR * g)
            # the cut: settle the task's classes
            if form == "1":
                if j == 0:
                    anchors = np.concatenate([arng.permutation(np.where(ytr == c)[0])[:m_first] for c in task])
            else:
                anchors = np.concatenate([anchors] + [arng.permutation(np.where(ytr == c)[0])[:m_acc] for c in task])
            idx = anchors.copy(); HA_cut = net.forward(Xtr[idx])[0]
            groups.append((idx, HA_cut, relation(HA_cut, beta), drng.permutation(len(idx))))
            for c in task:
                Z = net.forward(Xtr[ytr == c])[0]; gauss[c] = (Z.mean(0), Z.std(0), len(groups) - 1)
    acc = 100 * net.acc(Xte, yte)
    if return_mem:
        raw = len(anchors); nums = (2 * HID * len(gauss) + sum(2 * len(g[0]) * HID for g in groups)) if use_feat else 0
        return acc, raw, nums
    return acc
