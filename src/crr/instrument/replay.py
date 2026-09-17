"""Salience-weighted replay: the continual-learning operationalisation of the occasion-weight
law pi_m ∝ r_m · exp(lambda · S_m) (external spec [D9]/[H1]/[T5]; theory/CRR.md v3.1 [P2]
with beta fixed), with equal retention r_m = 1 by design.

One occasion = one task. Its surplus S_m is the model's own Fisher-path surplus on a fixed
probe set while it learned task m (D6: C = sum sqrt(2 KL_step), C* = sqrt(2 KL(start||end)),
S = C - C*, categorical predictives averaged over the probe; the per-update Fisher unit).
Replay draws a past task m with probability pi_m over the tasks present in the buffer, then a
uniform sample from that task's buffer entries; the loss is CE(present batch) + CE(replay
batch) (ER-sum, w = 1). lambda = 0 is uniform-over-tasks replay; lambda = 1 is the law's
prediction; negative lambda is the anti-salience control.

Every constant is a named argument. Deterministic given the seed (one generator, single
thread). The same function serves the surrogate gate (synthetic streams) and the study.
"""
from __future__ import annotations

import math

import numpy as np

from .core import kl_step, path_length


class _MLP:
    def __init__(self, rng, d, K, h):
        self.p = [rng.normal(0, math.sqrt(2 / d), (d, h)), np.zeros(h), rng.normal(0, math.sqrt(2 / h), (h, K)), np.zeros(K)]

    def forward(self, x):
        W1, b1, W2, b2 = self.p; hid = np.maximum(0, x @ W1 + b1); return hid, hid @ W2 + b2

    def grad(self, x, dz, hid):
        W1, b1, W2, b2 = self.p; dh = dz @ W2.T; dh[hid <= 0] = 0
        return [x.T @ dh, dh.sum(0), hid.T @ dz, dz.sum(0)]

    def step(self, g, lr):
        for a, gg in zip(self.p, g): a -= lr * gg

    def probs(self, x):
        z = self.forward(x)[1]; z = z - z.max(1, keepdims=True); e = np.exp(z); return e / e.sum(1, keepdims=True)

    def acc(self, x, y):
        with np.errstate(all="ignore"):
            z = self.forward(x)[1]
        if not np.all(np.isfinite(z)): return 0.0
        return float((z.argmax(1) == y).mean())


def _ce_grad(net, x, y):
    hid, z = net.forward(x); z = z - z.max(1, keepdims=True); p = np.exp(z); p /= p.sum(1, keepdims=True)
    dz = p; dz[np.arange(len(y)), y] -= 1; dz /= len(y)
    return net.grad(x, dz, hid)


def salience_replay(Xtr, ytr, Xte, yte, K, per_task, lam, seed, lr=0.05, bs=10, hid=256, epochs=3, buf=500,
                    replay_w=1.0, probe_n=200, snap_every=5, form="exp", grad_noise=None, probe_seed=12345,
                    surplus_mode="shadow"):
    """Run one salience-weighted-replay stream. Returns final class-IL accuracy (%), per-task
    surplus S, per-task C and C*, per-task forgetting (accuracy on the task's own classes right
    after it was learned minus at the end), the final replay weights, and diagnostics.

    surplus_mode 'shadow'  S_m is measured on a replay-free shadow pass over task m from the
              weights at the task's start (the occasion's own path, uncontaminated by replay of
              other tasks); the live pass with replay then follows from the same start weights.
              'stream'  S_m is measured on the live pass (replay included; carries a trend with m).
    form      'exp'  pi_m ∝ exp(lam * S_m)          (the law; lam = 1 is the prediction)
              'lin'  pi_m ∝ max(1 + lam * S_m, 0)   (the pre-specified alternative form, spec [F2])
    grad_noise  optional dict {task index: sd}: Gaussian noise added to the present gradient
              during those tasks (surrogate use only: inflates S without changing the task)."""
    rng = np.random.default_rng(seed); prng = np.random.default_rng(probe_seed)
    d = Xtr.shape[1]; net = _MLP(rng, d, K, hid)
    tasks = [tuple(range(i, i + per_task)) for i in range(0, K, per_task)]
    probe = prng.choice(len(ytr), min(probe_n, len(ytr)), replace=False); Xp = Xtr[probe]
    bufx = np.zeros((buf, d)); bufy = np.zeros(buf, int); buft = np.zeros(buf, int); nb = 0; seen = 0
    S, C, Cs, acc_after = [], [], [], []
    pi_log = []
    with np.errstate(all="ignore"):
        for ti, task in enumerate(tasks):
            ii_task = np.where(np.isin(ytr, task))[0]
            snaps = [net.probs(Xp)]; step = 0
            if surplus_mode == "shadow":                                     # replay-free shadow pass from the same start
                srng = np.random.default_rng(seed * 1000 + ti); shadow = _MLP.__new__(_MLP); shadow.p = [a.copy() for a in net.p]
                ssnaps = [shadow.probs(Xp)]; sstep = 0
                for _ in range(epochs):
                    perm = srng.permutation(ii_task)
                    for t in range(0, len(perm), bs):
                        ii = perm[t:t + bs]; g = _ce_grad(shadow, Xtr[ii], ytr[ii])
                        if grad_noise and ti in grad_noise:
                            g = [a + grad_noise[ti] * srng.standard_normal(a.shape) for a in g]
                        shadow.step(g, lr); sstep += 1
                        if sstep % snap_every == 0: ssnaps.append(shadow.probs(Xp))
                if sstep % snap_every: ssnaps.append(shadow.probs(Xp))
                spl = path_length(ssnaps, kl=kl_step)
            past = [m for m in range(ti) if np.any(buft[:nb] == m)]
            if past:
                Sv = np.array([S[m] for m in past])
                w = np.exp(lam * Sv) if form == "exp" else np.maximum(1 + lam * Sv, 0)
                if not np.all(np.isfinite(w)) or w.sum() <= 0: w = np.ones_like(Sv)
                pi = w / w.sum(); pi_log.append({m: float(p) for m, p in zip(past, pi)})
            for _ in range(epochs):
                perm = rng.permutation(ii_task)
                for t in range(0, len(perm), bs):
                    ii = perm[t:t + bs]; x, y = Xtr[ii], ytr[ii]
                    g = _ce_grad(net, x, y)
                    if grad_noise and ti in grad_noise:
                        g = [a + grad_noise[ti] * rng.standard_normal(a.shape) for a in g]
                    if past:
                        m = past[rng.choice(len(past), p=pi)]
                        pool = np.where(buft[:nb] == m)[0]; jj = pool[rng.integers(0, len(pool), len(y))]
                        gr = _ce_grad(net, bufx[jj], bufy[jj]); g = [a + replay_w * b for a, b in zip(g, gr)]
                    net.step(g, lr); step += 1
                    if step % snap_every == 0: snaps.append(net.probs(Xp))
                    for k in range(len(y)):                                   # reservoir buffer with task ids
                        seen += 1
                        if nb < buf: j = nb; nb += 1
                        else:
                            j = rng.integers(seen)
                            if j >= buf: continue
                        bufx[j] = x[k]; bufy[j] = y[k]; buft[j] = ti
            if step % snap_every: snaps.append(net.probs(Xp))
            pl = spl if surplus_mode == "shadow" else path_length(snaps, kl=kl_step)
            S.append(pl["S"]); C.append(pl["C"]); Cs.append(pl["Cstar"])
            m_te = np.isin(yte, task); acc_after.append(100 * net.acc(Xte[m_te], yte[m_te]))
        final_task = [100 * net.acc(Xte[np.isin(yte, task)], yte[np.isin(yte, task)]) for task in tasks]
    return dict(lam=lam, form=form, seed=seed, acc=100 * net.acc(Xte, yte), S=S, C=C, Cstar=Cs,
                forgetting=[a - b for a, b in zip(acc_after, final_task)], acc_after=acc_after, acc_final_task=final_task,
                pi_last=pi_log[-1] if pi_log else {}, finite=bool(all(np.all(np.isfinite(a)) for a in net.p)))
