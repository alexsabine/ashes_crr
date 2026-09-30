"""RQM harness (Replay_Quality_Memory/DECLARATION.md): the class-incremental stream and the candidate-independent baselines on
SEC1's learner (runs/sec5/frozen/sec1_score.py: one hidden layer of 256 ReLU units, a single softmax head over all K classes,
SGD lr 0.05, batch 10, 3 epochs per task, 2 classes per task, EQ4's fixed 80/20 split). Written before any candidate code.

Baselines here:
  ft     fine-tuning: train on each task in turn, nothing kept (the lower bound)
  joint  all tasks' data at once, the same number of epochs over the union (the upper bound)
  er     experience replay: a class-balanced buffer of M raw training examples (the memory budget M is a parameter);
         each step concatenates the current batch with a replay batch of the same size drawn from the buffer (standard ER)
Every function is deterministic in its seed. Accuracy is class-IL: argmax over all K outputs on the test set of all classes.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "runs" / "sec5" / "frozen"))
import sec5_score as P5  # noqa: E402  (loads SEC4's scorer, SCL3's loader and SEC1's learner, unchanged)

S = P5.S; L = P5.L
LR, BS, EPOCHS, HID = S.LR, S.BS, S.EPOCHS, S.HID


def tasks_of(K, per_task=2):
    return [tuple(range(i, i + per_task)) for i in range(0, K, per_task)]


def sgd_steps(net, rng, X, y, epochs=EPOCHS, bs=BS, lr=LR, extra=None):
    """Plain SGD over (X, y) for `epochs`. `extra(net, rng, x, y) -> (x2, y2)` may append rows to each batch (ER)."""
    for _ in range(epochs):
        perm = rng.permutation(len(y))
        for t in range(0, len(perm), bs):
            ii = perm[t:t + bs]; x, yy = X[ii], y[ii]
            if extra is not None:
                x, yy = extra(net, rng, x, yy)
            _, g = S.ce_loss_grad(net, x, yy)
            net.set_flat(net.flat() - lr * g)


def run_ft(seed, Xtr, ytr, Xte, yte, K, per_task=2):
    rng = np.random.default_rng(seed); net = S.MLP(rng, Xtr.shape[1], K, h=HID)
    with np.errstate(all="ignore"):
        for task in tasks_of(K, per_task):
            ii = np.where(np.isin(ytr, task))[0]; sgd_steps(net, rng, Xtr[ii], ytr[ii])
    return 100 * net.acc(Xte, yte)


def run_joint(seed, Xtr, ytr, Xte, yte, K, per_task=2):
    rng = np.random.default_rng(seed); net = S.MLP(rng, Xtr.shape[1], K, h=HID)
    with np.errstate(all="ignore"):
        sgd_steps(net, rng, Xtr, ytr)
    return 100 * net.acc(Xte, yte)


def run_er(seed, Xtr, ytr, Xte, yte, K, M, per_task=2):
    """ER with a class-balanced buffer of at most M raw examples, filled at each task end (a cut) with a random draw per class,
    re-balanced to floor(M / classes seen) per class. The buffer is the stored raw data the candidates must do without."""
    rng = np.random.default_rng(seed); net = S.MLP(rng, Xtr.shape[1], K, h=HID)
    bufX = np.zeros((0, Xtr.shape[1])); bufy = np.zeros(0, dtype=ytr.dtype); seen = []
    brng = np.random.default_rng(10_000 + seed)

    def extra(net, rng, x, yy):
        if len(bufy) == 0:
            return x, yy
        jj = brng.integers(0, len(bufy), len(yy))
        return np.concatenate([x, bufX[jj]]), np.concatenate([yy, bufy[jj]])

    with np.errstate(all="ignore"):
        for task in tasks_of(K, per_task):
            ii = np.where(np.isin(ytr, task))[0]; sgd_steps(net, rng, Xtr[ii], ytr[ii], extra=extra)
            seen += list(task); per = max(1, M // len(seen))
            keepX, keepy = [], []
            for c in seen:
                if c in task:
                    cc = np.where(ytr == c)[0]; pick = brng.permutation(cc)[:per]; keepX.append(Xtr[pick]); keepy.append(ytr[pick])
                else:
                    cc = np.where(bufy == c)[0][:per]; keepX.append(bufX[cc]); keepy.append(bufy[cc])
            bufX = np.concatenate(keepX); bufy = np.concatenate(keepy)
    return 100 * net.acc(Xte, yte), int(len(bufy))


def load_seen(did, study):
    """A SEEN carrier from a pinned table (development only): study in {'scl3', 'sec3', 'sec4', 'sec5'}."""
    tables = {"scl3": dict(P5.P3.SCL3_DATASETS), "sec3": dict(P5.P3.DATASETS), "sec4": dict(P5.P4.DATASETS), "sec5": dict(P5.DATASETS)}
    L.DATASETS = tables[study]
    Xs, ys, meta = L.load_openml(did)
    if meta["excluded"]:
        return None
    K = meta["classes_used"]
    return (*S.split_standardise(Xs, ys, K), K, tables[study][did][0])


if __name__ == "__main__":
    X, y = S._synthetic(); Xs, ys, meta = L.select_classes(X, y, 10); K = meta["classes_used"]; data = S.split_standardise(Xs, ys, K)
    for seed in range(3):
        print(f"seed {seed}: ft {run_ft(seed, *data, K):.2f}  joint {run_joint(seed, *data, K):.2f}  "
              f"er M=50 {run_er(seed, *data, K, 50)[0]:.2f}  er M=200 {run_er(seed, *data, K, 200)[0]:.2f}")
