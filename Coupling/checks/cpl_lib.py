"""CPL1 learner and pause harness (Coupling/DECLARATION.md, pushed at 440e185 before any CPL1 code).

CL-X, THE COUPLED LEARNER. run_cpl() re-implements runs/sec5/frozen/sec4_score.run_guard(variant='clip') line for line (SEC1's
MLP and SGD, the calibrated Laplace importance, SEC4's clip at kappa 0.5), imported frozen and never modified, with the coupling
extras and the operator's pauses added around it:
  stored statistics  at each task end, the class means and one shared (pooled within-class) diagonal covariance of the hidden
                     features (the ReLU layer) of that task's training rows, for that task's classes; no raw rows are kept
  transport          at the end of every later task, every stored class mean is moved by rrm_lib.hopdc_transport, unchanged
                     (tau 0.05, k 400), with the anchors taken from the current task's training rows: their features under the
                     previous task end's weights (SEC's theta_star) and under the current weights; covariances are not moved
  readouts           (i) the network's own head (SEC1's net.acc); (ii) NCM on the stored statistics with a diagonal Gaussian
                     likelihood (ncm_gauss below)
  penalty            'sec' (the clipped SEC) or 'none' (fine-tuning: the same loop with the penalty term removed; the Fisher,
                     the secant and the guard are still computed as diagnostics, so the training rng is consumed exactly as in
                     the 'sec' arm)
None of the extras draws from the training rng or writes to the weights, so with no pause the 'sec' arm is run_guard('clip')
bit for bit whether the extras are on or off (the identity C0-ID, checked in cpl_phase_a.py).

THE PAUSE (SCL's construction; Proposition 7's empty cut). The operator pauses immediately before own-clock step k of a task
(k in 0..steps-1). Every piece of the learner's state lives in one dict; at a pause the dict is pickled to bytes, cleared (the
live learner is gone) and a fresh learner is rebuilt from the bytes (a new MLP object, a new Generator carrying the restored
bit-generator state, new arrays). The state: the weights; the accumulated importance (task-size-weighted calibrated Fisher) and
the current task's clipped importance; the anchor theta_star; the calibration accumulators (the secant windows' parameter and
gradient sums) with their counts; the stored statistics; the training rng's state; the step counters (the window counter k_step,
the global own-step count) and the data position (task, epoch, offset, the epoch's permutation); the logs (s_j, guard margins,
firings, fallbacks) and the L2 no-transport list. The operator's schedule is the operator's, not part of the learner's state.
Lossy variants (each restores everything else):
  L1  the four secant accumulators are zeros after the restore (the window counts, the divisors, are unchanged)
  L2  the task in which the pause fell gets no transport at its end
  L3  the windows are keyed to wall-clock time: the window counter k_step (SEC's only use of the step count) advances by the
      pause's duration, D = 50 ticks, at each pause; the pause schedule itself stays keyed to own steps
"""
from __future__ import annotations

import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")                    # as the frozen scorers, before numpy is imported
sys.dont_write_bytecode = True                        # nothing is written into the frozen or other folders

import hashlib  # noqa: E402
import math  # noqa: E402
import pickle  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "Replay_Quality_Memory" / "checks"))
sys.path.insert(0, str(ROOT / "Relational_Reference_Memory" / "checks"))
import rrm_lib as RL  # noqa: E402  (hopdc_transport, unchanged)
import t_lib as T  # noqa: E402  (the 30 SEEN carriers, their cache, the ER20 learner)
import phase_a as PA  # noqa: E402  (RQM's stream builder: POS is SEC1's synthetic stream)

R = RL.R                  # rqm_lib: it imports runs/sec5/frozen/sec5_score.py, unmodified
P5 = R.P5; P4 = P5.P4; S = R.S; LD = P5.L
assert Path(P4.__file__).resolve().parent == ROOT / "runs" / "sec5" / "frozen", P4.__file__

# ---------------------------------------------------------------- fixed by DECLARATION.md (and the CHOICES in cpl_phase_a.py)
KAPPA = P4.KAPPA                  # 0.5, SEC4's clip
TAU = RL.HOPDC_TAU; K_TOP = RL.HOPDC_K                     # 0.05, 400
ALPHA = R.ALPHA                   # 0.1: RQM's covariance shrinkage toward the mean variance, used by the NCM readout
N_PAUSE = 3                       # pauses per task
PAUSE_SEED = 70_000               # the operator's rng: default_rng([PAUSE_SEED, seed]), never the learner's
D_TICKS = 50                      # L3: a pause's duration in wall-clock ticks
ROT_SEED = 60_000                 # the rotated stream's rotations: default_rng(ROT_SEED), one per task in task order
ER_M = 20                         # ER-20: raw rows per class
SEEDS = S.SEEDS
VARIANTS = ("closure", "L1", "L2", "L3")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def step_of(v):
    """max(1, 2 SE over seeds), the record's resolvable step."""
    v = np.asarray(v, dtype=float)
    return max(1.0, 2 * float(np.std(v, ddof=1)) / math.sqrt(len(v)))


# ---------------------------------------------------------------- streams
def synthetic():
    """SEC1's synthetic stream as RQM's and RRM2's POS (S._synthetic, select_classes, SEC1's split and standardisation)."""
    data, K = PA.stream("POS")
    return data, K


def rotated():
    """POS with a seeded rotation of the input at each task: task j's training and test rows are multiplied by an orthogonal
    Q_j (QR of a standard normal matrix with the signs fixed, worlds.py's ROT construction), drawn in task order from
    default_rng(ROT_SEED), after SEC1's standardisation."""
    (Xtr, ytr, Xte, yte), K = PA.stream("POS")
    Xtr = Xtr.copy(); Xte = Xte.copy(); d = Xtr.shape[1]; rr = np.random.default_rng(ROT_SEED)
    for task in R.tasks_of(K, 2):
        F = rr.standard_normal((d, d)); Q, Rr = np.linalg.qr(F); Q = Q * np.sign(np.diag(Rr))
        mtr = np.isin(ytr, task); mte = np.isin(yte, task)
        Xtr[mtr] = Xtr[mtr] @ Q.T; Xte[mte] = Xte[mte] @ Q.T
    return (Xtr, ytr, Xte, yte), K


TABLES = {"scl3": dict(P5.P3.SCL3_DATASETS), "sec3": dict(P5.P3.DATASETS), "sec4": dict(P5.P4.DATASETS), "sec5": dict(P5.DATASETS)}


def pinned_header(study, did):
    import json
    with open(ROOT / "runs" / study / f"results_{did}.jsonl") as f:
        h = json.loads(f.readline())
    assert "mode" not in h
    return h


def seen(study, did):
    """A SEEN carrier through t_lib's cache (RQM's loader, SEC1's split); K from the loader, per_task from the frozen scorer's
    DATASETS table; checked against the pinned header. None if the loader excludes it."""
    d = T.load_seen_cached(study, did)
    if d is None:
        return None
    Xtr, ytr, Xte, yte, K, name = d; per_task = TABLES[study][did][2]
    h = pinned_header(study, did)
    assert (h["dataset"], h["K"], h["per_task"], h["n_train"], h["n_test"], h["d"]) == (name, K, per_task, len(ytr), len(yte), Xtr.shape[1]), \
        (study, did, name, K, per_task, len(ytr), len(yte), Xtr.shape[1])
    return (Xtr, ytr, Xte, yte), int(K), int(per_task), str(name)


# ---------------------------------------------------------------- the pause schedule (the operator's)
def task_steps(ytr, K, per_task, fs=S.FS, fe=S.FE, bs=S.BS, epochs=S.EPOCHS):
    out = []
    for task in R.tasks_of(K, per_task):
        n_task = int(np.isin(ytr, task).sum()); total = epochs * int(math.ceil(n_task / bs))
        out.append((total, max(1, int(math.ceil(fs * total))), max(1, int(math.ceil(fe * total)))))
    return out


def pause_schedule(seed, ytr, K, per_task):
    """Per task, N_PAUSE distinct own-step indices: the first uniformly from the secant-window steps (the first n_s and the last
    n_e steps of the task), the others uniformly without replacement from the task's remaining steps."""
    prng = np.random.default_rng([PAUSE_SEED, seed]); out = []
    for total, n_s, n_e in task_steps(ytr, K, per_task):
        win = sorted(set(range(n_s)) | set(range(total - n_e, total)))
        first = int(win[int(prng.integers(0, len(win)))])
        rest = np.array([k for k in range(total) if k != first])
        others = [int(x) for x in prng.choice(rest, N_PAUSE - 1, replace=False)]
        out.append(sorted([first] + others))
    return out


# ---------------------------------------------------------------- the state and the pause
_ACC = ("s_th", "s_g", "e_th", "e_g")


def _save(st):
    blob = {k: v for k, v in st.items() if k not in ("net", "rng")}
    blob["net_p"] = st["net"].p; blob["net_K"] = st["net"].K; blob["rng_state"] = st["rng"].bit_generator.state
    return pickle.dumps(blob, protocol=pickle.HIGHEST_PROTOCOL)


def _restore(b):
    blob = pickle.loads(b)
    net = S.MLP.__new__(S.MLP); net.p = blob.pop("net_p"); net.K = blob.pop("net_K")
    rng = np.random.default_rng(); rng.bit_generator.state = blob.pop("rng_state")
    blob["net"] = net; blob["rng"] = rng
    return blob


def pause(st, variant, d_ticks=D_TICKS):
    """The operator's pause: save the full state, drop the live learner, rebuild it from the bytes; a lossy variant loses or
    changes one thing on the way."""
    b = _save(st)
    st.clear()
    st = _restore(b)
    if variant == "L1":
        for k in _ACC:
            st[k] = np.zeros_like(st[k])
    elif variant == "L2":
        st["no_transport"].append(int(st["ti"]))
    elif variant == "L3":
        st["k_step"] += d_ticks
    else:
        assert variant == "closure", variant
    return st


# ---------------------------------------------------------------- readouts and records
def _features_at(theta, net, X):
    tmp = S.MLP.__new__(S.MLP); tmp.p = [np.empty_like(a) for a in net.p]; tmp.K = net.K; tmp.set_flat(theta)
    return tmp.forward(X)[0]


def ncm_gauss(Z, yte, stats, alpha=ALPHA):
    """NCM with a diagonal Gaussian likelihood, equal priors, over every stored class; each class uses its task's pooled diagonal
    covariance shrunk toward its mean variance (v' = (1 - alpha) v + alpha mean(v)). 0 if anything is non-finite."""
    cs = sorted(stats)
    if not np.all(np.isfinite(Z)) or not all(np.all(np.isfinite(stats[c][0])) and np.all(np.isfinite(stats[c][1])) for c in cs):
        return 0.0
    sc = np.empty((len(Z), len(cs)))
    for i, c in enumerate(cs):
        mu, v, _ = stats[c]; t = float(np.mean(v)); vv = (1 - alpha) * v + alpha * (t if t > 0 else 1.0)
        sc[:, i] = -0.5 * (((Z - mu) ** 2 / vv).sum(1) + float(np.log(vv).sum()))
    return 100 * float((np.array(cs)[sc.argmax(1)] == yte).mean())


def stats_sha(stats):
    h = hashlib.sha256()
    for c in sorted(stats):
        mu, v, j = stats[c]; h.update(np.asarray(mu, dtype=np.float64).tobytes()); h.update(np.asarray(v, dtype=np.float64).tobytes())
        h.update(str((int(c), int(j))).encode())
    return h.hexdigest()


# ---------------------------------------------------------------- CL-X
def run_cpl(seed, Xtr, ytr, Xte, yte, K, per_task, penalty="sec", transport=True, stats=True, pauses=None, variant="closure",
            fs=S.FS, fe=S.FE, kappa=KAPPA, d_ticks=D_TICKS, lr=S.LR, bs=S.BS, epochs=S.EPOCHS, hidden=S.HID, tau=TAU, k_top=K_TOP):
    """sec4_score.run_guard(variant='clip') line for line, every piece of state in one dict, with the coupling extras and the
    operator's pauses. penalty 'sec' | 'none'; pauses None or one sorted list of own-step indices per task."""
    assert penalty in ("sec", "none") and variant in VARIANTS
    rng = np.random.default_rng(seed)
    d = Xtr.shape[1]; net = S.MLP(rng, d, K, h=hidden); n = net.flat().size
    tasks = [tuple(range(i, i + per_task)) for i in range(0, K, per_task)]
    cap = kappa / (lr * S.BAYES_W)
    st = dict(rng=rng, net=net, imp_bayes=np.zeros(n), theta_star=None, stats={}, svals=[], margins=[], fired=0, n_fallback=0,
              no_transport=[], ti=0, own=0)
    n_paused = 0
    with np.errstate(all="ignore"):
        while st["ti"] < len(tasks):
            ti = st["ti"]; task = tasks[ti]
            ii_task = np.where(np.isin(ytr, task))[0]; n_task = len(ii_task)            # the data stream's, not the learner's
            imp_used = st["imp_bayes"] / n_task
            if st["theta_star"] is not None:                                              # SEC4's clip
                m = lr * S.BAYES_W * float(np.max(imp_used)); st["margins"].append(m)
                if not (m < kappa):
                    imp_used = np.minimum(imp_used, cap); st["fired"] += 1
            total = epochs * int(math.ceil(n_task / bs)); n_s = max(1, int(math.ceil(fs * total))); n_e = max(1, int(math.ceil(fe * total)))
            st.update(imp_used=imp_used, total=total, n_s=n_s, n_e=n_e, s_th=np.zeros(n), s_g=np.zeros(n), e_th=np.zeros(n),
                      e_g=np.zeros(n), k_step=0, ep=0, t=0, perm=None)
            P = pauses[ti] if pauses is not None else (); pi = 0; spe = int(math.ceil(n_task / bs))
            while st["ep"] < epochs:
                own = st["ep"] * spe + st["t"] // bs
                while pi < len(P) and P[pi] == own:                                       # the operator
                    st = pause(st, variant, d_ticks); pi += 1; n_paused += 1
                if st["t"] == 0:
                    st["perm"] = st["rng"].permutation(ii_task)
                net = st["net"]
                ii = st["perm"][st["t"]:st["t"] + bs]; x, y = Xtr[ii], ytr[ii]
                L_p, g_p = S.ce_loss_grad(net, x, y)
                theta_before = net.flat()
                if st["k_step"] < st["n_s"]: st["s_th"] += theta_before; st["s_g"] += g_p
                if st["k_step"] >= st["total"] - st["n_e"]: st["e_th"] += theta_before; st["e_g"] += g_p
                st["k_step"] += 1; st["own"] += 1
                st["t"] += bs
                if st["t"] >= n_task:
                    st["t"] = 0; st["ep"] += 1
                if st["theta_star"] is None or penalty == "none":
                    net.set_flat(theta_before - lr * g_p); continue
                dth = theta_before - st["theta_star"]; g_q = 2 * st["imp_used"] * dth
                w = S.BAYES_W
                net.set_flat(theta_before - lr * (g_p + w * g_q))
            assert pi == len(P), (ti, pi, P)
            net = st["net"]; rng_ = st["rng"]
            theta_now = net.flat().copy()
            f = np.zeros(n)
            for _ in range(S.N_FISHER):
                ii = ii_task[rng_.integers(0, len(ii_task), bs)]; f += S.ce_loss_grad(net, Xtr[ii], ytr[ii])[1] ** 2
            f_task = f / S.N_FISHER * bs
            n_s, n_e = st["n_s"], st["n_e"]
            dth = st["e_th"] / n_e - st["s_th"] / n_s; dg = st["e_g"] / n_e - st["s_g"] / n_s; nn = float(dth @ dth)
            c = float(dg @ dth) / nn if nn > S.DTH_FLOOR else float("nan"); rho = float((f_task * dth) @ dth) / nn if nn > S.DTH_FLOOR else float("nan")
            if nn > S.DTH_FLOOR and np.isfinite(c) and np.isfinite(rho) and c > 0 and rho > 0: s = c / rho
            else: s = 1.0; st["n_fallback"] += 1
            st["svals"].append(float(s))
            st["imp_bayes"] = st["imp_bayes"] + n_task * s * f_task
            if stats:                                                                     # the coupling extras (no rng)
                H_now = net.forward(Xtr[ii_task])[0]
                if transport and ti > 0 and ti not in st["no_transport"] and st["stats"]:
                    H_cut = _features_at(st["theta_star"], net, Xtr[ii_task])
                    cs = sorted(st["stats"]); M = np.stack([st["stats"][cc][0] for cc in cs])
                    M2 = RL.hopdc_transport(M, H_cut, H_now, tau=tau, k=k_top)
                    for i, cc in enumerate(cs):
                        st["stats"][cc] = (M2[i].copy(), st["stats"][cc][1], st["stats"][cc][2])
                yt = ytr[ii_task]; resid = np.empty_like(H_now); mus = {}
                for cc in task:
                    msk = yt == cc; mus[cc] = H_now[msk].mean(0); resid[msk] = H_now[msk] - mus[cc]
                v = (resid ** 2).mean(0)
                for cc in task:
                    st["stats"][cc] = (mus[cc], v.copy(), ti)
            st["theta_star"] = theta_now
            st["ti"] += 1
        net = st["net"]; theta = net.flat()
        Zte = net.forward(Xte)[0]
        rec = dict(penalty=penalty, transport=bool(transport and stats), stats=bool(stats), variant=variant if pauses is not None else "none",
                   seed=int(seed), acc_head=100 * net.acc(Xte, yte), acc_ncm=ncm_gauss(Zte, yte, st["stats"]) if stats else None,
                   s=st["svals"], guard_fired=int(st["fired"]), guard_margins=[round(x, 6) for x in st["margins"]],
                   n_fallback=int(st["n_fallback"]), n_paused=int(n_paused), own_steps=int(st["own"]),
                   theta_sha=hashlib.sha256(theta.tobytes()).hexdigest(), stats_sha=stats_sha(st["stats"]) if stats else None,
                   finite=bool(np.all(np.isfinite(theta))))
        if stats:                                                                         # report: stored means against the current ones
            last = set(tasks[-1]); rel = []
            for cc, (mu, _, j) in sorted(st["stats"].items()):
                if cc in last:
                    continue
                o = net.forward(Xtr[ytr == cc])[0].mean(0); no = float(np.linalg.norm(o))
                rel.append(float(np.linalg.norm(mu - o)) / max(no, 1e-12))
            rec["rel_err_old"] = float(np.mean(rel)) if rel and np.all(np.isfinite(rel)) else None
    return rec


def run_er20(seed, Xtr, ytr, Xte, yte, K, per_task):
    """ER-20: t_lib.train(..., 'ER20'), unchanged (20 raw training rows per class, replay batch = stream batch, SEC1's MLP and SGD)."""
    net = T.train(seed, Xtr, ytr, Xte, yte, K, "ER20", per_task=per_task, er_m=ER_M)[0]
    return 100 * net.acc(Xte, yte)


def compute_rows(ytr, K, per_task, epochs=S.EPOCHS, bs=S.BS):
    """Row counts per learner (forward+backward rows; forward-only rows), from the stream: the coupled learner's steps, its
    Fisher minibatches, its statistics and transport forwards; ER-20's stream and replay rows."""
    ns = [int(np.isin(ytr, t).sum()) for t in R.tasks_of(K, per_task)]
    stream = epochs * sum(ns)
    cpl_grad = stream + len(ns) * S.N_FISHER * bs
    cpl_fwd = sum(ns) + sum(ns[1:])
    er_grad = stream + epochs * sum(ns[1:])
    return dict(stream=stream, cpl_grad=cpl_grad, cpl_fwd=cpl_fwd, er_grad=er_grad)
