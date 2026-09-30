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


# ---------------------------------------------------------------- the arms of DEV_DECLARATION.md (written after it was pushed)
ALPHA = 0.1          # IGR-F / FGR-F covariance shrinkage toward (tr/d) I
REPLAY_BS = 10       # pseudo-samples per step, as ER's replay batch
RFR_WIDTH = 512; RFR_LAMBDA = 1.0; RFR_SEED = 0


def run_er_pc(seed, Xtr, ytr, Xte, yte, K, m, per_task=2):
    """ER with m raw rows per seen class (matched memory): run_er with M = m x classes seen at every cut."""
    rng = np.random.default_rng(seed); net = S.MLP(rng, Xtr.shape[1], K, h=HID)
    bufX = np.zeros((0, Xtr.shape[1])); bufy = np.zeros(0, dtype=ytr.dtype)
    brng = np.random.default_rng(10_000 + seed)

    def extra(net, rng, x, yy):
        if len(bufy) == 0:
            return x, yy
        jj = brng.integers(0, len(bufy), len(yy))
        return np.concatenate([x, bufX[jj]]), np.concatenate([yy, bufy[jj]])

    with np.errstate(all="ignore"):
        for task in tasks_of(K, per_task):
            ii = np.where(np.isin(ytr, task))[0]; sgd_steps(net, rng, Xtr[ii], ytr[ii], extra=extra)
            for c in task:
                cc = np.where(ytr == c)[0]; pick = brng.permutation(cc)[:m]
                bufX = np.concatenate([bufX, Xtr[pick]]); bufy = np.concatenate([bufy, ytr[pick]])
    return 100 * net.acc(Xte, yte)


def _fit_gauss(Z, form, alpha):
    mu = Z.mean(0)
    if form == "D":
        return mu, np.sqrt(np.maximum(Z.var(0), 0.0)), "D"
    C = np.cov(Z, rowvar=False) if len(Z) > 1 else np.zeros((Z.shape[1], Z.shape[1]))
    C = np.atleast_2d(C); d = C.shape[0]; t = float(np.trace(C)) / d
    C = (1 - alpha) * C + alpha * (t if t > 0 else 1.0) * np.eye(d)
    return mu, np.linalg.cholesky(C + 1e-10 * np.eye(d)), "F"


def _draw(g, prng, n):
    mu, Lc, form = g; z = prng.standard_normal((n, len(mu)))
    return mu + (z * Lc if form == "D" else z @ Lc.T)


def run_igr(seed, Xtr, ytr, Xte, yte, K, form="F", alpha=ALPHA, replay_bs=REPLAY_BS, force_empty=False, per_task=2, space="input"):
    """IGR (space='input'): per-class Gaussians of the INPUT fitted at the class's cut, never refitted, replayed class-balanced
    (a seeded rotation over old classes) as pseudo-inputs concatenated to each batch. FGR (space='feature'): the Gaussians are
    of the hidden activations at the cut, replayed at the head only (clipped at 0, the ReLU range)."""
    rng = np.random.default_rng(seed); net = S.MLP(rng, Xtr.shape[1], K, h=HID)
    prng = np.random.default_rng(20_000 + seed); gauss = {}; rot = [0]

    def classes_for(n):
        old = sorted(gauss); out = [old[(rot[0] + i) % len(old)] for i in range(n)]; rot[0] = (rot[0] + n) % len(old); return out

    def pseudo(n):
        cs = classes_for(n); xs = np.concatenate([_draw(gauss[c], prng, 1) for c in cs]); return xs, np.array(cs, dtype=ytr.dtype)

    with np.errstate(all="ignore"):
        for task in tasks_of(K, per_task):
            ii = np.where(np.isin(ytr, task))[0]; X, y = Xtr[ii], ytr[ii]
            for _ in range(EPOCHS):
                perm = rng.permutation(len(y))
                for t in range(0, len(perm), BS):
                    jj = perm[t:t + BS]; x, yy = X[jj], y[jj]
                    if force_empty or not gauss or replay_bs == 0:
                        _, g = S.ce_loss_grad(net, x, yy)
                    elif space == "input":
                        xp, yp = pseudo(replay_bs); _, g = S.ce_loss_grad(net, np.concatenate([x, xp]), np.concatenate([yy, yp]))
                    else:
                        hp, yp = pseudo(replay_bs); hp = np.maximum(hp, 0.0)
                        _, gc = S.ce_loss_grad(net, x, yy)
                        W1, b1, W2, b2 = net.p; z = hp @ W2 + b2; p = S.softmax(z); p[np.arange(len(yp)), yp] -= 1; p /= len(yp)
                        gh = np.concatenate([np.zeros(W1.size + b1.size), (hp.T @ p).ravel(), p.sum(0)])
                        g = (len(yy) * gc + len(yp) * gh) / (len(yy) + len(yp))
                    net.set_flat(net.flat() - LR * g)
            for c in task:
                Z = Xtr[ytr == c] if space == "input" else net.forward(Xtr[ytr == c])[0]
                gauss[c] = _fit_gauss(Z, form, alpha)
    return 100 * net.acc(Xte, yte)


def mem_rows_per_class(form, d):
    """Matched ER rows per class for an IGR form (memory in numbers / d, rounded up)."""
    return int(math.ceil((d + d * (d + 1) / 2) / d)) if form == "F" else 2


def run_rfr(Xtr, ytr, Xte, yte, K, per_task=2, width=RFR_WIDTH, lam=RFR_LAMBDA, seed=RFR_SEED):
    """Random ReLU features (fixed, seed 0) + streaming ridge: G += H'H, C += H'Y per task; W = (G + lam I)^-1 C. Exact against
    joint ridge on the same features; no stored example."""
    r = np.random.default_rng(seed); d = Xtr.shape[1]
    Wr = r.normal(0, 1 / math.sqrt(d), (d, width)); br = r.normal(0, 1, width)
    phi = lambda X: np.maximum(0.0, X @ Wr + br)  # noqa: E731
    G = np.zeros((width, width)); C = np.zeros((width, K))
    for task in tasks_of(K, per_task):
        ii = np.where(np.isin(ytr, task))[0]; H = phi(Xtr[ii]); Y = np.zeros((len(ii), K)); Y[np.arange(len(ii)), ytr[ii]] = 1
        G += H.T @ H; C += H.T @ Y
    W = np.linalg.solve(G + lam * np.eye(width), C)
    return 100 * float((np.argmax(phi(Xte) @ W, 1) == yte).mean())


def run_sec_clip(seed, Xtr, ytr, Xte, yte, K, per_task=2):
    return P5.P4.run_guard(seed, Xtr, ytr, Xte, yte, K, per_task, "clip")["acc"]
