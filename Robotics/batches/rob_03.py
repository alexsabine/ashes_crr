"""ROB1 stage 4b batch 03: applications RA5 (fleet update and rollback as a state-closed cut) and RA6 (event-triggered
attitude control) of the declared battery Robotics/DECLARATION_4B.md (pushed at d44e713 before any model; prompt-log
entry 257; AGENT_LOG 223). Each row fixes, as declared, the model, Q, the CRR-proper ingredient, the null (T-G), the
domain's own theorem (T-N), the check (T-C) and the investigator's forecast; the labels are computed from the numbers by
crr.synthesis.harness.outcome() (R15).

RA5. A learning controller on a fleet of 8 robots. Each robot is a damped joint (x = (q, q'), q'' = -w0^2 q - 2 zeta w0 q'
     + u, w0 = 2 rad/s, zeta = 0.1, exact zero-order hold at dt = 0.02 s, process noise sd 0.02 from the world's own
     generator). The controller is a one-hidden-layer tanh MLP policy (16 units) on running-normalised states, trained
     online by Adam (lr 1e-2 on a cosine schedule keyed to its own update count k) to imitate the discrete LQR expert from
     its own experience (a DAgger-type learner: it acts with exploration noise sd 0.1, stores (x, expert label) in a
     256-slot replay ring, and takes one Adam step on a minibatch of 32 drawn by its own generator). Its persistent state
     is five groups: params, optimiser (Adam m, v, t), rng (its generator), buffers (replay ring and the normaliser's
     running statistics) and clock (k). At k0 = 1000 the fleet pushes an update over the air: the robot parks (the world
     holds its state and draws nothing), the controller's state is saved, the update is installed, and the fleet
     manager orders a rollback after L wall ticks; the robot reboots into the saved state and resumes for 1000 steps.
     Arms: CRR's closure (E1 of Empty_Cut_Engineering: every group the update reads that persists is saved, keyed to k);
     the null, the declared lossy variants (optimiser state, rng, buffers dropped: each restored at its constructor
     default); the domain's method (A/B slots: the whole controller image written to the inactive slot and restored
     atomically). Content = the chord sqrt(2 KL) on a fixed 64-state probe between the rolled-back and the never-paused
     run at the same k (kl_gauss with the exploration variance), maximised over the 1000 resumed steps; T-C: bit-identical
     parameters, actions and plant states at every resumed step on every robot at every L under closure. Printed, not
     scored: a weights-only checkpoint, and a controller whose schedule reads the wall tick.
RA6. A linearised inverted pendulum (one quadrotor attitude axis): theta'' = (g/l) theta + u, g/l = 9.81 s^-2, continuous
     LQR (Q = I, R = 1) held between updates, exact zero-order hold on a 1 kHz grid; the sensor reads x = (theta, theta')
     with Gaussian noise sd sigma = 0.01 on each component at every tick; 100 episodes of 5 s from x0 ~ N(0, 0.1^2 I),
     common random numbers for every trigger. Triggers, checked every tick on the state x: the declared trigger (the
     declaration calls it A1'; it is not CRR-proper A1', which excludes the instrument's sample noise as the unit), an
     update when ||x - x_last|| >= sigma (one unit step of the sensor's Fisher metric I/sigma^2); Tabuada's
     relative trigger, ||x - x_last|| >= s_T ||x||; periodic updates every h seconds. At an update the held control is
     -K (x + v). Cost J = mean over episodes of the integral of x'Qx + u'Ru. The CRR trigger sets the cost; the periodic
     h and Tabuada's s_T are each swept (41-point log scan, then bisection on the last upward crossing, the fewest updates
     at that cost) to the same J, and the mean update counts are compared. T-C: the CRR trigger's updates at equal cost
     within 1 % of Tabuada's (literal). If a family cannot reach J*, the comparison at equal cost does not exist and the
     row is UNSTATED (the rule in the code before the first run, which the first run reached: see CHOICES (10)). Printed,
     not scored: the CRR threshold at 0.5, 2 and 4 sigma against both matched families, both event triggers reading
     the noisy measurement instead of the state (with its outcome() labels), and a noise-free reading (the control also
     reads x; sigma only a threshold constant) with its outcome() labels (added after review: CHOICES RA6 (11)).

CHOICES (every underspecified point, the most literal and simplest reading; printed on a CHOICES line before the rows and
repeated in each row's weakness line): see CHOICES_RA5 and CHOICES_RA6 below. Nothing was tuned after a run.

Run 1 is kept: Robotics/batches/rob_03_run1.txt is the first run's output, verbatim (code state: this file before the
post-run changes CHOICES RA5 (11)-(12) and RA6 (10)-(11); that code state was never committed). Every number, both
OUTCOME lines and the tally of run 1 equal the current output's; the later changes are text and printed readings only.

Literature named by name only, as the declaration names it (no citation claim beyond the names; R10: nothing fetched here):
A/B partitions and atomic updates (standard practice); Tabuada 2007 (event-triggered control). Proposition 7 as in
AI_Safety/SELF_THROUGH_TIME.md; E1-E3 as in Empty_Cut_Engineering/EMPTY_CUT_ENGINEERING.md. Deterministic (numpy
default_rng with fixed seeds; exact matrix exponentials); no data files; no network; CPU, about two minutes. Rung R4 at most
(a declared check on a synthetic model); a note, not evidence (R8).

    cd /home/user/ashes_crr && uv run python Robotics/batches/rob_03.py > Robotics/batches/rob_03.txt
"""
from __future__ import annotations

import copy
import math
import pickle
import sys

import numpy as np
from scipy.linalg import expm, solve_continuous_are, solve_discrete_are

from crr.instrument.core import kl_gauss
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

DECL = "Robotics/DECLARATION_4B.md at d44e713"


def _w(cond, yes, no):
    return yes if cond else no


def _qv(check):
    return "-> not computable" if check is None else ("-> Q holds" if check else "-> Q fails")


def _zoh(A, B, dt):
    """Exact zero-order-hold discretisation of x' = A x + B u over dt."""
    n, m = A.shape[0], B.shape[1]
    M = np.zeros((n + m, n + m))
    M[:n, :n], M[:n, n:] = A, B
    E = expm(M * dt)
    return E[:n, :n], E[:n, n:]


# ====================================================================================== RA5 fleet update and rollback
DT5 = 0.02                    # s, control period
W0, ZETA = 2.0, 0.1           # the joint's natural frequency (rad/s) and damping ratio
S_W = 0.02                    # process-noise sd per step (the world's generator)
X0_SD5 = 0.3                  # sd of the world's initial state
SIG_E = 0.1                   # exploration-noise sd (action units); the probe KL uses its variance
HID = 16                      # hidden units
CAP, BATCH = 256, 32          # replay ring, minibatch
LR0 = 1e-2                    # Adam learning rate at k = 0
BETA1, BETA2, ADAM_EPS = 0.9, 0.999, 1e-8
NORM_EPS = 1e-8               # the normaliser's variance guard
Q5, R5 = np.eye(2), 0.1       # the expert's discrete LQR weights
K0, K1 = 1000, 1000           # steps before the update; steps resumed after the rollback
K_SCHED = K0 + K1             # the cosine schedule's horizon
N_FLEET = 8                   # robots: controller seed r, world seed 100 + r
L_SWEEP = (0, 10, 1000)       # pause lengths (wall ticks) under closure
L_MAIN = 10                   # pause length for the image, the lossy variants and the printed variants
N_PROBE, PROBE_SD, SEED_PROBE = 64, 0.3, 999
GROUPS = {"params": ("W1", "b1", "W2", "b2"), "optimiser": ("m", "v", "t"), "rng": ("rng",),
          "buffers": ("bx", "by", "bn", "bi", "nc", "nm", "nM2"), "clock": ("k",)}
CONFIG = ("seed", "clock_kind")   # construction arguments, not state
LOSSY = ("optimiser", "rng", "buffers")   # the declared lossy variants (T-G's null)
CHOICES_RA5 = (
    "CHOICES RA5: (1) the plant is a damped joint (w0 = 2 rad/s, zeta = 0.1, dt = 0.02 s, process noise sd 0.02, initial state "
    "N(0, 0.3^2 I) from the world's generator, seed 100 + r) and the controller a 16-unit tanh MLP trained online by Adam to imitate "
    "the discrete LQR expert (Q = I, R = 0.1) from its own experience, acting with exploration noise sd 0.1 (the declaration names a "
    "learning controller and no model); (2) the controller's persistent state is five groups: params (W1, b1, W2, b2), optimiser "
    "(Adam m, v and its step t), rng (its numpy generator, which draws the initial weights, the exploration noise and the minibatch), "
    "buffers (the 256-slot replay ring and the normaliser's running count, mean and M2), clock (the update count k, which keys the "
    "cosine learning-rate schedule over 2000 steps); (3) the update and rollback: at k0 = 1000 the robot parks (the world holds its "
    "state and draws nothing: E3 holds by construction), the state is saved, the update is installed, and after L wall ticks the "
    "robot reboots into the saved state; the update's own content is never read (a reboot discards it), so it is not modelled beyond "
    "the L ticks it takes; (4) CRR's closure saves all five groups by name; the image (the domain's A/B slot) is the whole "
    "controller object pickled into the inactive slot and unpickled on rollback; (5) 'dropped' = not in the checkpoint, so after "
    "the reboot the group is at its constructor default (optimiser: m = v = 0, t = 0; rng: the generator as the constructor leaves "
    "it; buffers: an empty ring and a fresh normaliser); the clock k is kept in each lossy variant (only the named group is dropped); "
    "(6) content = max over the 1000 resumed steps of sqrt(2 kl_gauss) between the policy means of the paused and the never-paused "
    "run on a fixed probe of 64 states N(0, 0.3^2 I) (seed 999), variance = the exploration variance 0.1^2; (7) T-G: crr = the "
    "largest closure content over robots and L in (0, 10, 1000); null = the smallest content over robots and the three declared "
    "lossy variants at L = 10 (the ingredient did work only if every lossy variant on every robot changed the trajectory); "
    "(8) T-N: the largest image-restore content over robots at L = 10; (9) T-C: parameters, actions and plant states bit-identical "
    "(numpy array_equal) at every resumed step, every robot, every L under closure; (10) printed, not scored: a weights-only "
    "checkpoint (params only, the clock included in what is dropped) and the same controller with its schedule keyed to the wall "
    "tick (L = 0, 10, 1000), the variables of the controller that no group names (none is expected), and the checkpoint sizes; "
    "(11) CHANGE AFTER THE FIRST RUN: two phrases of the reading were reworded (a claim that the enumeration is what CRR adds over "
    "the image, and a claim about an image restore of the wall-keyed controller, which was not run); the model, the numbers and the "
    "label are unchanged; (12) CHANGE AFTER REVIEW (text only): the reading now states that the pause length L has no pathway into "
    "the own-clock arms (the wall tick is read only by the wall-keyed schedule, the world is parked, the update is never installed), "
    "so the L sweep under closure could not fail; that closure and image restore the same attributes; that dropped groups return at "
    "constructor defaults; and that the clock half of the ingredient is ablated only in the printed wall-keyed arm; the model, the "
    "numbers and the label are unchanged; the first run's output is pinned verbatim at Robotics/batches/rob_03_run1.txt (code state: "
    "this file before changes (11) and (12), never committed)")


def _expert():
    A = np.array([[0.0, 1.0], [-W0 ** 2, -2.0 * ZETA * W0]])
    B = np.array([[0.0], [1.0]])
    Ad, Bd = _zoh(A, B, DT5)
    P = solve_discrete_are(Ad, Bd, Q5, np.array([[R5]]))
    K = np.linalg.solve(np.array([[R5]]) + Bd.T @ P @ Bd, Bd.T @ P @ Ad)[0]
    return Ad, Bd[:, 0], K


AD5, BD5, KEXP = _expert()
PROBE = np.random.default_rng(SEED_PROBE).standard_normal((N_PROBE, 2)) * PROBE_SD


class World:
    """The robot's plant: the world's own state and generator; it steps only when the robot acts."""

    def __init__(self, seed):
        self.rng = np.random.default_rng(seed)
        self.x = self.rng.standard_normal(2) * X0_SD5

    def step(self, a):
        self.x = AD5 @ self.x + BD5 * a + S_W * self.rng.standard_normal(2)

    def snapshot(self):
        return self.x.copy(), copy.deepcopy(self.rng.bit_generator.state)

    @classmethod
    def from_snapshot(cls, snap):
        w = cls.__new__(cls)
        w.x = snap[0].copy()
        w.rng = np.random.default_rng(0)                         # state overwritten on the next line
        w.rng.bit_generator.state = copy.deepcopy(snap[1])
        return w


class Controller:
    def __init__(self, seed, clock_kind="own"):
        self.seed, self.clock_kind = seed, clock_kind
        self.rng = np.random.default_rng(seed)
        self.W1 = self.rng.standard_normal((HID, 2)) / math.sqrt(2.0)
        self.b1 = np.zeros(HID)
        self.W2 = self.rng.standard_normal((1, HID)) * (0.1 / math.sqrt(HID))
        self.b2 = np.zeros(1)
        self.m = [np.zeros_like(p) for p in self.params()]
        self.v = [np.zeros_like(p) for p in self.params()]
        self.t = 0
        self.bx, self.by = np.zeros((CAP, 2)), np.zeros(CAP)
        self.bn, self.bi = 0, 0
        self.nc, self.nm, self.nM2 = 0, np.zeros(2), np.zeros(2)
        self.k = 0

    def params(self):
        return [self.W1, self.b1, self.W2, self.b2]

    def flat(self):
        return np.concatenate([self.W1.ravel(), self.b1, self.W2.ravel(), self.b2])

    def _norm(self, X):
        var = self.nM2 / max(self.nc - 1, 1)
        return (X - self.nm) / np.sqrt(var + NORM_EPS)

    def _fwd(self, Z):
        h = np.tanh(Z @ self.W1.T + self.b1)
        return (h @ self.W2.T)[:, 0] + self.b2[0], h

    def mean(self, X):
        return self._fwd(self._norm(X))[0]

    def lr(self, wall):
        s = self.k if self.clock_kind == "own" else wall
        return LR0 * 0.5 * (1.0 + math.cos(math.pi * min(s, K_SCHED) / K_SCHED))

    def act(self, x):
        self.nc += 1
        d = x - self.nm
        self.nm = self.nm + d / self.nc
        self.nM2 = self.nM2 + d * (x - self.nm)
        mu = self._fwd(self._norm(x[None]))[0][0]
        return float(mu + SIG_E * self.rng.standard_normal())

    def learn(self, x, ystar, wall):
        self.bx[self.bi], self.by[self.bi] = x, ystar
        self.bi = (self.bi + 1) % CAP
        self.bn = min(self.bn + 1, CAP)
        if self.bn >= BATCH:
            idx = self.rng.integers(0, self.bn, BATCH)
            Z, Y = self._norm(self.bx[idx]), self.by[idx]
            out, h = self._fwd(Z)
            d = 2.0 * (out - Y) / BATCH
            gW2 = d[None, :] @ h
            gb2 = np.array([d.sum()])
            dpre = (d[:, None] * self.W2) * (1.0 - h * h)
            gW1 = dpre.T @ Z
            gb1 = dpre.sum(axis=0)
            self.t += 1
            lr = self.lr(wall)
            c1, c2 = 1.0 - BETA1 ** self.t, 1.0 - BETA2 ** self.t
            for p, g, m, v in zip(self.params(), (gW1, gb1, gW2, gb2), self.m, self.v):
                m *= BETA1
                m += (1.0 - BETA1) * g
                v *= BETA2
                v += (1.0 - BETA2) * g * g
                p -= lr * (m / c1) / (np.sqrt(v / c2) + ADAM_EPS)
        self.k += 1


def _checkpoint(ctrl, groups):
    ck = {}
    for gname in groups:
        for name in GROUPS[gname]:
            ck[name] = copy.deepcopy(ctrl.rng.bit_generator.state if name == "rng" else getattr(ctrl, name))
    return ck


def _reboot(seed, clock_kind, ck):
    """A fresh process: the constructor, then every saved item loaded; anything not saved stays at its default."""
    c = Controller(seed, clock_kind)
    for name, val in ck.items():
        if name == "rng":
            c.rng.bit_generator.state = copy.deepcopy(val)
        else:
            setattr(c, name, copy.deepcopy(val))
    return c


def _run(ctrl, world, n, wall0, rec=True):
    P, A, X, MU = [], [], [], []
    for j in range(n):
        x = world.x
        a = ctrl.act(x)
        ctrl.learn(x, -float(KEXP @ x), wall0 + j)
        world.step(a)
        if rec:
            P.append(ctrl.flat()); A.append(a); X.append(world.x.copy()); MU.append(ctrl.mean(PROBE))
    if rec:
        return dict(P=np.array(P), A=np.array(A), X=np.array(X), MU=np.array(MU))
    return None


def _content(ref, run):
    ch = np.array([math.sqrt(2.0 * kl_gauss(a, b, var=SIG_E ** 2)) for a, b in zip(ref["MU"], run["MU"])])
    bit = bool(np.array_equal(ref["P"], run["P"]) and np.array_equal(ref["A"], run["A"]) and np.array_equal(ref["X"], run["X"]))
    dx = float(np.max(np.abs(ref["X"] - run["X"])))
    loss = float(np.mean((run["MU"][-1] + PROBE @ KEXP) ** 2))
    return dict(max=float(ch.max()), end=float(ch[-1]), bit=bit, dx=dx, loss=loss)


def ra5_robot(r):
    ctrl, world = Controller(r, "own"), World(100 + r)
    _run(ctrl, world, K0, 0, rec=False)
    wsnap = world.snapshot()
    ck_full = _checkpoint(ctrl, GROUPS)
    image = pickle.dumps(ctrl)                                   # the inactive slot: the whole controller image
    ck_params = _checkpoint(ctrl, ("params",))
    ck_lossy = {g: _checkpoint(ctrl, tuple(x for x in GROUPS if x != g)) for g in LOSSY}
    unnamed = sorted(set(vars(ctrl)) - set(CONFIG) - {n for g in GROUPS.values() for n in g})
    sizes = dict(closure=len(pickle.dumps(ck_full)), image=len(image), params=len(pickle.dumps(ck_params)))
    ref = _run(ctrl, world, K1, K0)                              # never paused: the reference, same k from k0 on
    ref_loss = float(np.mean((ref["MU"][-1] + PROBE @ KEXP) ** 2))
    res = {}
    for L in L_SWEEP:
        res[("closure", L)] = _content(ref, _run(_reboot(r, "own", ck_full), World.from_snapshot(wsnap), K1, K0 + L))
    res[("image", L_MAIN)] = _content(ref, _run(pickle.loads(image), World.from_snapshot(wsnap), K1, K0 + L_MAIN))
    for g in LOSSY:
        res[(g, L_MAIN)] = _content(ref, _run(_reboot(r, "own", ck_lossy[g]), World.from_snapshot(wsnap), K1, K0 + L_MAIN))
    res[("params only", L_MAIN)] = _content(ref, _run(_reboot(r, "own", ck_params), World.from_snapshot(wsnap), K1, K0 + L_MAIN))
    for L in L_SWEEP:                                            # the wall-keyed schedule: the same state, saved in full
        res[("wall-keyed", L)] = _content(ref, _run(_reboot(r, "wall", ck_full), World.from_snapshot(wsnap), K1, K0 + L))
    return res, unnamed, sizes, ref_loss


def ra5():
    per = [ra5_robot(r) for r in range(N_FLEET)]
    keys = list(per[0][0].keys())
    tab = {k: [p[0][k] for p in per] for k in keys}
    unnamed = sorted({u for p in per for u in p[1]})
    sizes = per[0][2]
    ref_loss = [p[3] for p in per]
    print("RA5 per-variant table (content = max over the 1000 resumed steps of the probe chord sqrt(2 KL), in exploration sd; "
          "bit = robots bit-identical at every resumed step; dx = max plant-state divergence; loss = final probe imitation MSE, "
          f"never-paused mean {np.mean(ref_loss):.6e}):")
    print(f"  {'variant':12} {'L':>5} {'content min':>12} {'median':>12} {'max':>12} {'end max':>12} {'bit':>5} {'dx max':>12} {'loss mean':>12}")
    for k in keys:
        c = tab[k]
        mx = np.array([e["max"] for e in c])
        print(f"  {k[0]:12} {k[1]:>5d} {mx.min():>12.6e} {np.median(mx):>12.6e} {mx.max():>12.6e} "
              f"{max(e['end'] for e in c):>12.6e} {sum(e['bit'] for e in c):>2d}/{N_FLEET} {max(e['dx'] for e in c):>12.6e} "
              f"{np.mean([e['loss'] for e in c]):>12.6e}")
    print(f"RA5 controller variables no group names: {unnamed if unnamed else 'none'}; checkpoint sizes (pickled bytes, robot 0): "
          f"closure {sizes['closure']}, image {sizes['image']}, params only {sizes['params']}")
    print()
    clos = [e for L in L_SWEEP for e in tab[("closure", L)]]
    crr = max(e["max"] for e in clos)
    lossy = {g: tab[(g, L_MAIN)] for g in LOSSY}
    null = min(e["max"] for g in LOSSY for e in lossy[g])
    null_g = min(LOSSY, key=lambda g: min(e["max"] for e in lossy[g]))
    dom = max(e["max"] for e in tab[("image", L_MAIN)])
    check = all(e["bit"] for e in clos)
    n_bit_lossy = {g: sum(e["bit"] for e in lossy[g]) for g in LOSSY}
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    img_bit = sum(e["bit"] for e in tab[("image", L_MAIN)])
    po = tab[("params only", L_MAIN)]
    wk = {L: tab[("wall-keyed", L)] for L in L_SWEEP}
    wk_max = {L: max(e["max"] for e in wk[L]) for L in L_SWEEP}
    wk_bit = {L: sum(e["bit"] for e in wk[L]) for L in L_SWEEP}
    lossy_txt = "; ".join(f"{g} dropped: content {min(e['max'] for e in lossy[g]):.6e} to {max(e['max'] for e in lossy[g]):.6e}, "
                          f"bit-identical on {n_bit_lossy[g]}/{N_FLEET}, final loss mean {np.mean([e['loss'] for e in lossy[g]]):.6e}"
                          for g in LOSSY)
    clos_txt = "; ".join(f"L = {L}: max content {max(e['max'] for e in tab[('closure', L)]):.6e}, bit-identical on "
                         f"{sum(e['bit'] for e in tab[('closure', L)])}/{N_FLEET}" for L in L_SWEEP)
    wk_txt = "; ".join(f"L = {L}: max content {wk_max[L]:.6e}, bit-identical on {wk_bit[L]}/{N_FLEET}" for L in L_SWEEP)
    return make_row(
        "robotics", f"RA5 fleet update and rollback as a state-closed cut: a DAgger-type MLP controller trained online by Adam on a "
                    f"damped joint, {N_FLEET} robots, update pushed at k0 = {K0}, rolled back after L wall ticks, {K1} steps resumed",
        source=f"ROB1 RA5 (declared in {DECL}; forecast REDUNDANT-DOMAIN)",
        Q="with state closure, rollback restores bit for bit; each lossy variant (optimiser state, rng, buffers dropped) changes the "
          "trajectory (computed as: the probe chord between the rolled-back and the never-paused run at the same k, maximised over "
          "the resumed steps, and bitwise identity of parameters, actions and plant states)",
        ingredient="Proposition 7 (the cut carries no content: every persistent group saved, E1) and A3's own-clock keying (the "
                   "schedule reads the update count k, E2)",
        null="the declared lossy variants: optimiser state, rng or buffers dropped (restored at constructor defaults), the smallest content",
        domain="A/B partitions and atomic updates: the whole controller image written to the inactive slot and restored (exact restore of the saved image)",
        numbers=(f"expert gain K = ({KEXP[0]:.6f}, {KEXP[1]:.6f}); closure: {clos_txt}; image (A/B slot, L = {L_MAIN}): max content "
                 f"{dom:.6e}, bit-identical on {img_bit}/{N_FLEET}; {lossy_txt}; smallest lossy content {null:.6e} ({null_g} dropped); "
                 f"printed, not scored: params only (L = {L_MAIN}) content {min(e['max'] for e in po):.6e} to "
                 f"{max(e['max'] for e in po):.6e}, bit-identical on {sum(e['bit'] for e in po)}/{N_FLEET}; wall-keyed schedule with "
                 f"the full state saved: {wk_txt}; controller variables no group names: {unnamed if unnamed else 'none'}; checkpoint "
                 f"bytes (robot 0) closure {sizes['closure']}, image {sizes['image']}, params only {sizes['params']}; robotics reading "
                 f"(restore fidelity): closure {sum(e['bit'] for e in clos)}/{len(clos)} robot-pauses bit-exact, image {img_bit}/{N_FLEET}, "
                 f"lossy {sum(n_bit_lossy.values())}/{N_FLEET * len(LOSSY)}; final imitation loss never-paused {np.mean(ref_loss):.6e}"),
        tg=f"closure content {crr:.6e} vs null (smallest lossy content) {null:.6e}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"the image restore's content {dom:.6e}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')} "
           f"(relative difference {rel(crr, dom):.3f})",
        tc=f"bit-identical under closure at every resumed step, robot and L: {_w(check, 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=(f"saving every persistent group by name and keying the schedule to k makes the rollback an empty cut: "
                 f"{sum(e['bit'] for e in clos)} of {len(clos)} robot-pauses resume bit for bit at L in "
                 f"{{{', '.join(str(L) for L in L_SWEEP)}}}, so Q {_w(check, 'holds', 'fails')}; the test could have failed only "
                 f"through an enumeration or restore error: in the own-clock arms the pause length L has no pathway into "
                 f"the run (the wall tick is read only by the wall-keyed schedule, the world is parked by construction and the update "
                 f"is never installed), so the L sweep under closure tests nothing beyond the restore; each declared lossy variant "
                 f"changes the trajectory on "
                 + ", ".join(f"{N_FLEET - n_bit_lossy[g]}/{N_FLEET} robots ({g})" for g in LOSSY)
                 + f", each dropped group returning at its constructor default (a fresh-process reboot, not an installed update's "
                 f"state), which fixes how much each variant changes; the A/B slot, which saves the whole image without naming "
                 f"anything, restores bit for bit on {img_bit}/{N_FLEET} with content {dom:.6e}, the closure's number, so the row reads "
                 f"{out}; "
                 + _w(not unnamed, "mechanically the closure and the image restore the same thing (the closure names every persistent "
                                   "attribute of the controller, none is left unnamed, and the image pickles them all), so T-N's "
                                   "agreement is by construction; ",
                      f"the closure leaves {unnamed} unnamed, which the image carries; ")
                 + f"the image needs no list of what to save; the clock half of the ingredient has no scored ablation (the declared "
                 f"null ablates only the lossy groups) and is ablated only in the printed wall-keyed arm: the wall-keyed schedule, "
                 f"saved in full, "
                 f"{_w(wk_max[L_SWEEP[0]] == 0.0 and all(wk_max[L] > 0.0 for L in L_SWEEP[1:]), 'is exact only at L = 0 and leaks the pause length into the trajectory', 'does not behave as a wall-keyed channel should')} "
                 f"(content {wk_max[L_SWEEP[1]]:.6e} at L = {L_SWEEP[1]}, {wk_max[L_SWEEP[2]]:.6e} at L = {L_SWEEP[2]}; the wall tick is "
                 f"a host variable, outside every checkpoint)"),
        weakness=(CHOICES_RA5 + "; the world is held during the pause by construction (a parked robot), so E3 is assumed, not tested; "
                  "a robot that runs the update before the rollback moves its world, and no restore of the controller can undo that; "
                  "bitwise identity holds on one machine and one numpy build (a restore on a different build is a tolerance question)"),
        elegance="", child="")


# ====================================================================================== RA6 event-triggered attitude control
G_L6 = 9.81                   # g/l, s^-2 (l = 1 m)
DT6, T6 = 1e-3, 5.0           # s: the sensor and trigger tick; the episode
N6 = int(round(T6 / DT6))
M6 = 100                      # episodes
SIG6 = 0.01                   # sensor-noise sd on theta (rad) and theta' (rad/s); A1's unit
X0_SD6 = 0.1                  # initial state sd
SEED_X0, SEED_V = 6, 7
R6 = 1.0                      # LQR and cost weights: Q = I, R = 1
C_SCORED = 1.0                # the CRR trigger: one resolvable step
C_SWEEP = (0.5, 2.0, 4.0)     # printed, not scored
N_SCAN, N_BISECT = 41, 24
H_RANGE = (DT6, 0.5)          # periodic h scan (s)
ST_RANGE = (1e-3, 1.0)        # Tabuada s_T scan
TOL_TC6 = 0.01                # T-C: within 1 % of Tabuada's (declared)
CHOICES_RA6 = (
    "CHOICES RA6: (1) the plant theta'' = (g/l) theta + u with g/l = 9.81 s^-2 (l = 1 m, unit input gain), continuous LQR with "
    "Q = I, R = 1 (the declaration fixes a linearised inverted pendulum, no values); exact zero-order hold on a 1 kHz tick, at "
    "which the sensor samples and every trigger is checked; (2) 'sensor noise sigma' = Gaussian noise of sd sigma = 0.01 on both "
    "theta (rad) and theta' (rad/s), fresh at every tick, the same draws for every trigger (common random numbers); only sensor "
    "noise, as declared (no process disturbance); (3) 'the state has moved one resolvable step' = ||x - x_last|| >= sigma on the "
    "state x (the sensor model N(x, sigma^2 I) has Fisher metric I/sigma^2, so one unit step is Euclidean sigma; the declaration "
    "sets A1's unit to the sensor's sigma, although CRR.md's A1' says the instrument's sample noise is not the unit); Tabuada's "
    "trigger on the same state: ||x - x_last|| >= s_T ||x||; both event triggers read the state, as Tabuada's analysis does, and "
    "the held control is -K (x + v) with v the sensor noise at the update tick (the measured-state reading is printed, not "
    "scored); (4) every trigger updates at t = 0; periodic updates fire at the first tick at or after each multiple of h; "
    "(5) 100 episodes of 5 s from x0 ~ N(0, 0.1^2 I) (seed 6; noise seed 7); cost J = mean over episodes of the left Riemann sum "
    "of x'x + u^2 on the tick grid; updates = mean over episodes; (6) equal cost: the CRR trigger at one sigma sets J*; each other "
    "family is scanned on 41 log-spaced values (h from 1 ms to 0.5 s, s_T from 1e-3 to 1), the LAST upward crossing of J* is "
    "taken (the largest parameter reaching J*, i.e. that family's fewest updates at J*), bisected 24 times on the log parameter, "
    "and its update count interpolated linearly in J between the bracket's ends; the number of crossings is printed; if a family "
    "has no upward crossing, the comparison at equal cost does not exist and the row is UNSTATED (this rule was in the code before "
    "the first run); (7) T-G: crr "
    "= the CRR trigger's updates, null = periodic updates at J*; T-N: Tabuada's updates at J*; (8) T-C is the declared column "
    "read literally: the CRR trigger's updates at J* within 1 % (the harness's relative difference) of Tabuada's; read this way it "
    "is the same comparison as T-N, so ADDS cannot be reached (T-N agreeing gives REDUNDANT-DOMAIN, differing gives WRONG); Q's "
    "own inequality (fewer updates than periodic at J*) is printed and the label it would give as T-C is printed, not scored; "
    "(9) printed, not scored: the CRR threshold at 0.5, 2 and 4 sigma against both matched families, and both event triggers "
    "reading the noisy measurement y = x + v (the periodic family does not read the state); (10) CHANGE AFTER THE FIRST RUN: the "
    "first run reached the UNSTATED rule (no periodic schedule reached J*) and its fallback printed only 'not computable' on T-G, "
    "T-N, T-C and the reading; the fallback now prints the periodic family's cost floor, Tabuada's match, the literal T-C, the labels "
    "two numeric readings of the null would give, and the measured-state and threshold readings, all not scored; the model, the "
    "scoring rule, the numbers and the label are unchanged; (11) CHANGE AFTER REVIEW (the second post-run change; text and printed "
    "readings only): (a) the ingredient and Q fields name what was run, the declaration's absolute threshold at the sensor sd sigma "
    "(CRR.md's A1' excludes the instrument's sample-level noise as the unit, so the row does not test A1'); (b) printed, not scored: "
    "outcome() under the measured-state reading (both families matched on y, the declared T-C and Q's own inequality), and a "
    "noise-free reading (the held control also reads x, -K x; sigma is then only a threshold constant; both families scanned and "
    "matched as above) with its outcome() labels, and the per-tick periodic cost with and without noise in the held control; "
    "(c) the reading and the weakness line state whether the scored reading's oracle (event triggers on the noise-free state, "
    "control on the sensor) is what puts J* below the periodic floor, that the absolute-threshold trigger is the domain's own "
    "send-on-delta (level-crossing, Lebesgue) sampling, so a printed ADDS alternative is not a novelty signal, and that the "
    "declaration's T-C coincides with its T-N; the scored reading, the scoring rule, every earlier number and the label are "
    "unchanged; the first run's output is pinned verbatim at Robotics/batches/rob_03_run1.txt (code state: this file before "
    "changes (10) and (11), never committed)")


def _plant6():
    A = np.array([[0.0, 1.0], [G_L6, 0.0]])
    B = np.array([[0.0], [1.0]])
    P = solve_continuous_are(A, B, np.eye(2), np.array([[R6]]))
    K = (B.T @ P / R6)[0]
    Ad, Bd = _zoh(A, B, DT6)
    return Ad, Bd[:, 0], K


AD6, BD6, K6 = _plant6()
X06 = np.random.default_rng(SEED_X0).standard_normal((M6, 2)) * X0_SD6
V6 = np.random.default_rng(SEED_V).standard_normal((N6, M6, 2)) * SIG6


def sim6(kind, p, read="x", ctrl="noisy"):
    """One trigger over the M6 episodes. kind: 'abs' (||e|| >= p sigma), 'rel' (||e|| >= p ||s||), 'per' (period p seconds).
    read: 'x' (the state) or 'y' (the noisy measurement) for the event triggers. ctrl: 'noisy' (the held control reads the
    sensor, -K (x + v); the scored reading) or 'clean' (the held control reads the state, -K x; the noise-free reading,
    printed only, used with read = 'x'). Returns (J, mean updates)."""
    if ctrl not in ("noisy", "clean") or (ctrl == "clean" and read != "x"):
        raise ValueError((read, ctrl))
    clean = ctrl == "clean"
    x = X06.copy()
    y = x + V6[0]
    ref = x.copy() if read == "x" else y.copy()
    u = -(x @ K6) if clean else -(y @ K6)
    n = np.ones(M6)
    J = np.zeros(M6)
    AdT = AD6.T
    if kind == "per":
        slot = np.floor(np.arange(N6) / (p / DT6))             # integer tick over the period in ticks
        per_fire = np.concatenate([[False], slot[1:] > slot[:-1]])
    for i in range(N6):
        if i > 0:
            if kind == "per":
                if per_fire[i]:
                    u = -(x @ K6) if clean else -((x + V6[i]) @ K6)
                    n += 1.0
            else:
                s = x if read == "x" else x + V6[i]
                e = np.sqrt(((s - ref) ** 2).sum(axis=1))
                thr = p * SIG6 if kind == "abs" else p * np.sqrt((s * s).sum(axis=1))
                fire = e >= thr
                if fire.any():
                    ref[fire] = s[fire]
                    u[fire] = -(x[fire] @ K6) if clean else -((x[fire] + V6[i, fire]) @ K6)
                    n += fire
        J += (x * x).sum(axis=1) + R6 * u * u
        x = x @ AdT + u[:, None] * BD6
    return float((J * DT6).mean()), float(n.mean())


def _scan(kind, lo, hi, read="x", ctrl="noisy"):
    ps = np.geomspace(lo, hi, N_SCAN)
    res = [sim6(kind, p, read, ctrl) for p in ps]
    return ps, np.array([r[0] for r in res]), np.array([r[1] for r in res])


def _match(kind, scan, Jstar, read="x", ctrl="noisy"):
    """Last upward crossing of Jstar on the scan, bisected on log p; N interpolated in J. None if the family cannot reach Jstar."""
    ps, J, N = scan
    up = [i for i in range(len(ps) - 1) if J[i] <= Jstar < J[i + 1]]
    n_cross = int(np.sum(np.diff(np.sign(J - Jstar)) != 0))
    if not up:
        return dict(ok=False, n_cross=n_cross, Jmin=float(J.min()), Jmax=float(J.max()))
    i = up[-1]
    plo, phi, Jlo, Jhi, Nlo, Nhi = ps[i], ps[i + 1], J[i], J[i + 1], N[i], N[i + 1]
    for _ in range(N_BISECT):
        pm = math.sqrt(plo * phi)
        Jm, Nm = sim6(kind, pm, read, ctrl)
        if Jm <= Jstar:
            plo, Jlo, Nlo = pm, Jm, Nm
        else:
            phi, Jhi, Nhi = pm, Jm, Nm
    Nq = Nlo + (Nhi - Nlo) * (Jstar - Jlo) / (Jhi - Jlo) if Jhi > Jlo else Nlo
    return dict(ok=True, p=math.sqrt(plo * phi), plo=plo, phi=phi, Jlo=Jlo, Jhi=Jhi, Nlo=Nlo, Nhi=Nhi, N=float(Nq),
                n_cross=n_cross, n_up=len(up))


def ra6():
    scan_per = _scan("per", *H_RANGE)
    scan_tab = _scan("rel", *ST_RANGE)
    table = {}
    for c in (C_SCORED,) + C_SWEEP:
        Jc, Nc = sim6("abs", c)
        table[c] = dict(J=Jc, N=Nc, per=_match("per", scan_per, Jc), tab=_match("rel", scan_tab, Jc, "x"))
    # measured-state reading (printed, not scored)
    Jy, Ny = sim6("abs", C_SCORED, "y")
    scan_tab_y = _scan("rel", *ST_RANGE, read="y")
    my = dict(J=Jy, N=Ny, per=_match("per", scan_per, Jy), tab=_match("rel", scan_tab_y, Jy, "y"))
    # noise-free reading (printed, not scored; added after review, CHOICES RA6 (11)): the held control reads x as well
    Jz, Nz = sim6("abs", C_SCORED, "x", "clean")
    scan_per_z = _scan("per", *H_RANGE, ctrl="clean")
    scan_tab_z = _scan("rel", *ST_RANGE, ctrl="clean")
    mz = dict(J=Jz, N=Nz, per=_match("per", scan_per_z, Jz, ctrl="clean"), tab=_match("rel", scan_tab_z, Jz, "x", "clean"))
    J_tick, J_tick_z = float(scan_per[1][0]), float(scan_per_z[1][0])     # periodic at h = the tick (the scan's first point)
    h_tick = float(scan_per[0][0])

    def _labels(n_crr, mt_per, mt_tab):
        """outcome() for a reading in which both families reach the CRR trigger's cost: (declared T-C, Q's own inequality)."""
        if not (mt_per["ok"] and mt_tab["ok"]):
            return None
        chk = rel(n_crr, mt_tab["N"]) <= TOL_TC6
        return (outcome(crr=n_crr, null=mt_per["N"], domain=mt_tab["N"], check=chk),
                outcome(crr=n_crr, null=mt_per["N"], domain=mt_tab["N"], check=n_crr < mt_per["N"]))

    def _lab_txt(lab, n_crr, mt_per, mt_tab):
        if lab is None:
            return "outcome() not computable (a family does not reach that cost)"
        return (f"outcome() gives {lab[0]} under the declared T-C (T-G relative difference {rel(n_crr, mt_per['N']):.4f}, T-N "
                f"{rel(n_crr, mt_tab['N']):.4f}) and {lab[1]} under Q's own inequality")

    lab_y = _labels(Ny, my["per"], my["tab"])
    lab_z = _labels(Nz, mz["per"], mz["tab"])

    def _fmt(mt, name):
        if not mt["ok"]:
            return f"{name}: no crossing (J range {mt['Jmin']:.6f} to {mt['Jmax']:.6f}, {mt['n_cross']} sign changes)"
        return (f"{name}: parameter {mt['p']:.6g}, updates {mt['N']:.3f} (bracket J {mt['Jlo']:.6f} / {mt['Jhi']:.6f}, updates "
                f"{mt['Nlo']:.2f} / {mt['Nhi']:.2f}; {mt['n_cross']} sign changes on the scan, {mt['n_up']} upward)")

    print("RA6 trade-off table (J = mean quadratic cost over 100 episodes of 5 s; N = mean updates per episode; periodic and "
          "Tabuada matched to the CRR trigger's J; ratio = N_CRR / N_matched):")
    print(f"  {'c (sigma)':>9} {'J':>10} {'N_CRR':>10} {'N_per':>10} {'h (s)':>10} {'N_Tab':>10} {'s_T':>10} "
          f"{'CRR/per':>8} {'CRR/Tab':>8}")
    for c in sorted(table):
        t = table[c]
        npr = t["per"]["N"] if t["per"]["ok"] else float("nan")
        ntb = t["tab"]["N"] if t["tab"]["ok"] else float("nan")
        print(f"  {c:>9g} {t['J']:>10.6f} {t['N']:>10.3f} {npr:>10.3f} {t['per'].get('p', float('nan')):>10.6f} {ntb:>10.3f} "
              f"{t['tab'].get('p', float('nan')):>10.6f} {t['N'] / npr:>8.4f} {t['N'] / ntb:>8.4f}")
    npy = my["per"]["N"] if my["per"]["ok"] else float("nan")
    nty = my["tab"]["N"] if my["tab"]["ok"] else float("nan")
    print(f"  measured-state reading, c = {C_SCORED:g}: J {Jy:.6f}, N_CRR {Ny:.3f}, N_per {npy:.3f}, N_Tab {nty:.3f}, "
          f"CRR/per {Ny / npy:.4f}, CRR/Tab {Ny / nty:.4f}")
    npz = mz["per"]["N"] if mz["per"]["ok"] else float("nan")
    ntz = mz["tab"]["N"] if mz["tab"]["ok"] else float("nan")
    print(f"  noise-free reading (held control -K x), c = {C_SCORED:g}: J {Jz:.6f}, N_CRR {Nz:.3f}, N_per {npz:.3f}, "
          f"N_Tab {ntz:.3f}, CRR/per {Nz / npz:.4f}, CRR/Tab {Nz / ntz:.4f}")
    print(f"  periodic scan J from {scan_per[1].min():.6f} to {scan_per[1].max():.6f}; Tabuada scan J from {scan_tab[1].min():.6f} "
          f"to {scan_tab[1].max():.6f}; LQR gain K = ({K6[0]:.6f}, {K6[1]:.6f})")
    print(f"  noise-free scans: periodic J from {scan_per_z[1].min():.6f} to {scan_per_z[1].max():.6f}; Tabuada J from "
          f"{scan_tab_z[1].min():.6f} to {scan_tab_z[1].max():.6f}; periodic at h = {h_tick:g} s: J {J_tick:.6f} with noise in the "
          f"held control, {J_tick_z:.6f} without; sigma^2 ||K||^2 T = {SIG6 ** 2 * float(K6 @ K6) * T6:.6f}")
    print()

    t = table[C_SCORED]
    i_fl = int(np.argmin(scan_per[1]))                           # the periodic family's cost floor on the scan
    h_fl, J_fl, N_fl = float(scan_per[0][i_fl]), float(scan_per[1][i_fl]), float(scan_per[2][i_fl])
    sweep_txt = "; ".join(
        f"c = {c:g}: J {table[c]['J']:.6f}, CRR/per "
        + (f"{table[c]['N'] / table[c]['per']['N']:.4f}" if table[c]["per"]["ok"] else "no periodic match")
        + ", CRR/Tab " + (f"{table[c]['N'] / table[c]['tab']['N']:.4f}" if table[c]["tab"]["ok"] else "no Tabuada match")
        for c in C_SWEEP)
    fewer_tab = [c for c in sorted(table) if table[c]["tab"]["ok"] and table[c]["N"] < table[c]["tab"]["N"]]
    no_per = [c for c in sorted(table) if not table[c]["per"]["ok"]]
    sweep_read = (f"across thresholds (not scored) the absolute trigger is below Tabuada's count at c in "
                  f"{{{', '.join(f'{c:g}' for c in fewer_tab) or 'none'}}} of {{{', '.join(f'{c:g}' for c in sorted(table))}}} "
                  f"and no periodic schedule reaches its cost at c in {{{', '.join(f'{c:g}' for c in no_per) or 'none'}}} "
                  f"({sweep_txt})")
    meas_read = (f"under the measured-state reading (not scored; the literal one, both event triggers reading the sensor as a "
                 f"robot must) the CRR trigger costs {Jy:.6f} with {Ny:.3f} updates, "
                 + (f"{Ny / my['per']['N']:.4f} of periodic's" if my["per"]["ok"] else "no periodic match")
                 + " and " + (f"{Ny / my['tab']['N']:.4f} of Tabuada's" if my["tab"]["ok"] else "no Tabuada match")
                 + " at that cost; " + _lab_txt(lab_y, Ny, my["per"], my["tab"])
                 + f"; there the one-sigma trigger fires on sensor noise, at {(Ny - 1.0) / (N6 - 1):.4f} of the checked ticks, "
                 f"where two independent sensor draws alone differ by at least sigma with probability exp(-1/4) = "
                 f"{math.exp(-0.25):.4f}")
    free_read = (f"under the noise-free reading (not scored; the held control reads x as well, so sigma is only a threshold "
                 f"constant) the CRR trigger costs {Jz:.6f} with {Nz:.3f} updates, "
                 + (f"{Nz / mz['per']['N']:.4f} of periodic's" if mz["per"]["ok"] else "no periodic match")
                 + " and " + (f"{Nz / mz['tab']['N']:.4f} of Tabuada's" if mz["tab"]["ok"] else "no Tabuada match")
                 + " at that cost; " + _lab_txt(lab_z, Nz, mz["per"], mz["tab"]))
    oracle_read = ("the scored reading gives the event triggers an oracle: they read the noise-free state x, which a robot's "
                   "sensor does not give, while the held control reads the sensor, -K (x + v); "
                   + _w(J_tick_z <= Jz and J_tick > t["J"],
                        f"this oracle is what puts J* below the periodic floor: with the held control noise-free as well, the CRR "
                        f"trigger costs {Jz:.6f} and periodic at every tick {J_tick_z:.6f}, within periodic's reach",
                        f"with the held control noise-free as well, the CRR trigger costs {Jz:.6f} and periodic at every tick "
                        f"{J_tick_z:.6f}")
                   + f"; the noise in the held control adds {t['J'] - Jz:.6f} to the CRR trigger's cost and "
                   f"{J_tick - J_tick_z:.6f} to the cost of periodic updates at every tick (sigma^2 ||K||^2 T = "
                   f"{SIG6 ** 2 * float(K6 @ K6) * T6:.6f})")
    novelty_read = ("the row does not test A1': CRR.md's A1' excludes the instrument's sample-level noise as the unit, and the "
                    "declaration's ingredient column sets the unit to the sensor's sigma; "
                    + _w(any(lab is not None and lab[1] == "ADDS" for lab in (lab_y, lab_z)),
                         "an ADDS printed under Q's own inequality is not a novelty signal: an absolute threshold on "
                         "||x - x_last|| is the domain's own send-on-delta (level-crossing, Lebesgue) sampling",
                         "an absolute threshold on ||x - x_last|| is the domain's own send-on-delta (level-crossing, Lebesgue) "
                         "sampling"))
    if not (t["per"]["ok"] and t["tab"]["ok"]):
        # the rule written before the first run: if a declared family cannot reach J*, the comparison at equal cost
        # does not exist and the row is UNSTATED; everything that can be computed is printed, not scored
        miss = [nm for nm, mt in (("periodic", t["per"]), ("Tabuada", t["tab"])) if not mt["ok"]]
        out = outcome(unstated=True)
        crr = t["N"]
        dom = t["tab"]["N"] if t["tab"]["ok"] else float("nan")
        tg = (f"not computable: {' and '.join(miss)} cannot reach J* = {t['J']:.6f} at any scanned parameter"
              + (f" (periodic cost floor {J_fl:.6f} at h = {h_fl:.6g} s with {N_fl:.3f} updates, one update per sensor tick; "
                 f"no period shorter than the tick exists)" if not t["per"]["ok"] else ""))
        if t["tab"]["ok"]:
            chk_lit = rel(crr, dom) <= TOL_TC6
            tn = (f"not scored (T-G not computable): Tabuada at equal cost {dom:.3f} updates (s_T = {t['tab']['p']:.6g}), relative "
                  f"difference from the CRR trigger's {crr:.3f}: {rel(crr, dom):.4f} ({_w(rel(crr, dom) <= TOL_N, 'agree', 'differ')})")
            tc = (f"not scored: the literal column, CRR updates {crr:.3f} within {TOL_TC6:g} of Tabuada's {dom:.3f}: "
                  f"{_w(chk_lit, 'holds', 'fails')}")
            alt = ""
            lab_fl = None
            if not t["per"]["ok"]:
                o_lit = outcome(crr=crr, null=N_fl, domain=dom, check=chk_lit)
                o_q = outcome(crr=crr, null=N_fl, domain=dom, check=crr < N_fl)
                lab_fl = (o_lit, o_q)
                alt = (f"; read with the periodic floor as the null (every tick, {N_fl:.3f} updates, at a cost above J*; not "
                       f"scored) the row would read {o_lit} under the declared T-C and {o_q} under Q's own inequality")
        else:
            tn = tc = "not scored: Tabuada cannot reach J* either"
            alt = ""
            lab_fl = None
        alts = [(nm, lab) for nm, lab in (("the measured-state reading", lab_y),
                                           ("the scored oracle reading with the periodic floor as the null", lab_fl),
                                           ("the noise-free reading", lab_z)) if lab is not None]
        lit_set = sorted({lab[0] for _, lab in alts})
        summary = ("under the declared T-C the computable readings give "
                   + "; ".join(f"{lab[0]} ({nm})" for nm, lab in alts)
                   + (f", so {lit_set[0]} under every computable reading ({len(alts)} of {len(alts)})" if len(lit_set) == 1 else "")
                   if alts else "no other reading is computable")
        reading = (f"Q cannot be formed as declared: at one sigma the absolute trigger costs J* = {t['J']:.6f} with {crr:.3f} updates "
                   f"per 5 s episode, and 'periodic updates at the same mean cost' does not exist"
                   + (f": the cheapest periodic schedule updates at every 1 kHz sensor tick ({N_fl:.3f} updates) and still costs "
                      f"{J_fl:.6f}" if not t["per"]["ok"] else "")
                   + f"; by the rule written before the run the row reads {out} as scored; " + summary
                   + (f"; Tabuada's relative trigger reaches J* with {dom:.3f} updates, {dom / crr:.4f} times the CRR trigger's"
                      if t["tab"]["ok"] else "")
                   + alt + "; " + oracle_read + "; " + meas_read + "; " + free_read + "; " + novelty_read + "; " + sweep_read)
        rob_per = (f"no periodic schedule reaches J* (the floor, {N_fl:.3f} updates at every tick, costs more)"
                   if not t["per"]["ok"] else f"{1 - t['N'] / t['per']['N']:+.4f}")
    else:
        crr, null, dom = t["N"], t["per"]["N"], t["tab"]["N"]
        check = rel(crr, dom) <= TOL_TC6
        out = outcome(crr=crr, null=null, domain=dom, check=check)
        q_ineq = crr < null
        out_alt = outcome(crr=crr, null=null, domain=dom, check=q_ineq)
        tg = (f"CRR trigger {crr:.3f} updates vs periodic at equal cost {null:.3f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')} "
              f"(relative difference {rel(crr, null):.4f}; Q's inequality, fewer than periodic: {_w(q_ineq, 'holds', 'fails')})")
        tn = (f"Tabuada at equal cost {dom:.3f} updates (s_T = {t['tab']['p']:.6g}): {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')} "
              f"(relative difference {rel(crr, dom):.4f})")
        tc = (f"CRR updates {crr:.3f} within {TOL_TC6:g} of Tabuada's {dom:.3f} (literal column): {_w(check, 'holds', 'fails')} "
              f"{_qv(check)}; not scored: with Q's own inequality as T-C ({_w(q_ineq, 'holds', 'fails')}) the label would be {out_alt}")
        reading = (f"at one sigma the absolute trigger costs J* = {t['J']:.6f} with {crr:.3f} updates per 5 s episode; periodic control "
                   f"needs {null:.3f} to reach the same cost and Tabuada's relative trigger {dom:.3f}; so the CRR trigger "
                   f"{_w(q_ineq, 'saves', 'does not save')} updates against periodic ({1 - crr / null:+.4f} of periodic's) and sits "
                   f"{rel(crr, dom):.4f} (relative) from Tabuada's count, {_w(crr < dom, 'below', 'above')} it; the row reads {out}; "
                   + oracle_read + "; " + meas_read + "; " + free_read + "; " + novelty_read + "; " + sweep_read)
        rob_per = f"{1 - t['N'] / t['per']['N']:+.4f}"
    rob_tab = f"{1 - t['N'] / t['tab']['N']:+.4f}" if t["tab"]["ok"] else "no Tabuada match"
    return make_row(
        "robotics", f"RA6 event-triggered attitude control: a linearised inverted pendulum (g/l = {G_L6:g} s^-2) under LQR held "
                    f"between updates, sensor noise sd {SIG6:g}, {M6} episodes of {T6:g} s on a {1 / DT6:g} Hz tick",
        source=f"ROB1 RA6 (declared in {DECL}; forecast REDUNDANT-DOMAIN or ADDS)",
        Q="the declared trigger (an update when the state has moved the sensor sd sigma since the last update, the declaration's "
          "'one resolvable step') needs fewer updates than periodic control at equal cost (computed as: mean updates per episode at "
          "the CRR trigger's own mean quadratic cost, the other families swept to that cost)",
        ingredient="the declaration's absolute threshold at the sensor sd sigma (the declaration calls it A1'; CRR.md's A1' excludes "
                   "the instrument's sample-level noise as the unit, so this is not CRR-proper A1')",
        null="periodic updates at the same mean cost (h swept to match)",
        domain="event-triggered control (Tabuada 2007): an update when ||e|| >= s_T ||x||, s_T swept to the same mean cost",
        numbers=(f"LQR gain K = ({K6[0]:.6f}, {K6[1]:.6f}); J* = {t['J']:.6f} at c = {C_SCORED:g} sigma with {t['N']:.3f} updates "
                 f"per episode ({t['N'] / T6:.3f} per s); {_fmt(t['per'], 'periodic')}; {_fmt(t['tab'], 'Tabuada')}; measured-state "
                 f"reading (not scored): J {Jy:.6f}, CRR {Ny:.3f}, {_fmt(my['per'], 'periodic')}; {_fmt(my['tab'], 'Tabuada on y')}; "
                 f"noise-free reading (not scored): J {Jz:.6f}, CRR {Nz:.3f}, {_fmt(mz['per'], 'periodic')}; "
                 f"{_fmt(mz['tab'], 'Tabuada')}; periodic at h = {h_tick:g} s: J {J_tick:.6f} with noise in the held control, "
                 f"{J_tick_z:.6f} without; "
                 f"periodic cost floor on the scan {J_fl:.6f} at h = {h_fl:.6g} s ({N_fl:.3f} updates); robotics reading (updates "
                 f"saved, energy and bandwidth, as a share of the matched family's updates): against periodic {rob_per}, against "
                 f"Tabuada {rob_tab}"),
        tg=tg, tn=tn, tc=tc, out=out, reading=reading,
        weakness=(CHOICES_RA6 + "; the comparison is at one cost level set by the CRR trigger's own threshold and one operating "
                  "regime (x0 sd 0.1, sensor sd 0.01, 5 s); the scored reading's event triggers read the noise-free state (an oracle "
                  "a robot's sensor does not give) while the held control reads the sensor, and the reading states what that does "
                  "to the periodic floor; the declared T-C coincides with T-N (see CHOICES), so the label cannot be ADDS whatever "
                  "the numbers, and the declaration's forecast 'REDUNDANT-DOMAIN or ADDS' could reach ADDS only through a T-C it "
                  "did not write (a defect of the declaration, for the tally); the declaration's ingredient column for RA6 sets "
                  "A1''s unit to the sensor's sigma, which CRR.md's A1' excludes (for the tally); an absolute threshold on "
                  "||x - x_last|| is the domain's own send-on-delta (level-crossing, Lebesgue) sampling, named here, not cited and "
                  "not fetched (R10), so an ADDS printed under Q's own inequality is not a novelty signal; mixed "
                  "absolute-plus-relative triggers were not declared and were not run"),
        elegance="", child="")


def main():
    print(CHOICES_RA5)
    print()
    print(CHOICES_RA6)
    print()
    r5 = ra5()
    r6 = ra6()
    return run_batch("ROB1 stage 4b batch 03: RA5 fleet update and rollback as a state-closed cut, RA6 event-triggered attitude "
                     f"control (Robotics/DECLARATION_4B.md; declared at d44e713)", [r5, r6])


if __name__ == "__main__":
    sys.exit(main())
