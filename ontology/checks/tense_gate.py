"""The tense test (ontology/10_fep_and_crr.md section 6; owner request prompt-log entry 91). Synthetic, no data.

What it can and cannot test. Every agent here is a program: whatever 'future' it carries (a forward model, preferences
over outcomes) is computed now from the settled past and from constants fixed before the run. So no run can show that
the future has content, and A7 holds for every agent by construction. What CAN fail is the operational shadow of A8: an
agent built only from CRR's regeneration clause (A6: the next occasion seeded from the settled past at bounded strength;
no preference, no forward model) against an agent that has both (an active-inference planner choosing by expected free
energy). If the regenerator ties the planner, A8's empty future costs nothing on that world; if it loses by a resolvable
step, the cost of A8 is measured; if it wins, the planner's future content was a liability there.

World. A ring of N states; the viable arc V. Each step s' = s + a_(t-k) + w (mod N), a in {-1, 0, +1}, k the action delay,
w the world's push. Leaving V is a cut (the occasion ends); the next step restarts in a random state of V. Score: the
fraction of scored steps spent in V (persistence), per seed; the restart step after a cut is not scored (it is
the world's move, not the agent's); mean and paired differences over seeds.
    drift     w = +1 with probability P_WIND, else 0 (one-step structure; a delay k = 0)
    delayed   drift with k = 2 (the agent must act two steps ahead; both agents see (s, last two actions))
    switch    drift whose push flips sign at T/2 (non-stationary)
    martingale s' uniform on the ring whatever the action (nothing to exploit: the negative control)
Agents (all see the same context x: the state, plus pending actions when k > 0):
    planner   active inference: Dirichlet counts over P(x'|x,a) (prior ALPHA0, accumulated), log-preference 0 on V and
              -PREF_COST off V, policies = all action sequences of length H, G = sum over the horizon of KL(Q || C~)
              (risk; states are observed, so ambiguity is zero), action drawn from the first-action marginal of
              softmax(-GAMMA G). The FEP's future content: preferred outcomes and predicted outcomes over a horizon.
    planner-v the same with volatile counts (multiplied by DECAY each step): the stronger baseline on 'switch' (R7).
    R-dur     A6 regenerator: at each cut the next occasion's policy is the Fisher-Rao (sphere) weighted mean of past
              occasions' action distributions per context, weights MaxEnt under a mean-DURATION constraint,
              pi_m ~ exp(beta tau_m), beta = BETA_REL / mean tau (persistence; CRR names no duration constraint: O2 names
              surplus and age only; this is A8's 'persistence proves regeneratability' read as the one constraint);
              exploration: a uniform action with probability EPS. No preference, no model, nothing about outcomes.
    R-age     the same with CRR's P3 age weights pi ~ Q_AGE^age (CRR-named; no selection by persistence).
    random    uniform actions (the floor).
Labels (computed, R15): a paired difference d (agent minus planner, per seed) is TIE if |mean d| < step, else the
sign names who is ahead; step = max(STEP_MIN, 2 x the standard error of the paired differences).
Gate: planner vs random must TIE on 'martingale' (NEG) and planner must be AHEAD of random on 'drift' (POS).
A world is DECIDABLE only where the planner is a step above random; elsewhere the reading is NOT DECIDABLE (a tie there
is two agents at the floor). On 'martingale' this holds by construction: the world's draws ignore the actions.
    uv run python ontology/checks/tense_gate.py > ontology/checks/tense_gate.txt
"""
from __future__ import annotations

import itertools
import os
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

# ---------------------------------------------------------------- registered constants
N = 12; V = (4, 5, 6, 7); P_WIND = 0.6; T = 3000; DELAY = 2; SEEDS = tuple(range(10))
ALPHA0 = 0.1; PREF_COST = 4.0; H = 3; GAMMA = 4.0; DECAY = 0.99
BETA_REL = 1.0; Q_AGE = 0.9; EPS = 0.1
STEP_MIN = 0.01
ACTIONS = (-1, 0, 1)
ENVS = ("drift", "delayed", "switch", "martingale")
SENS = dict(beta_rel=(0.5, 1.0, 2.0), eps=(0.05, 0.1, 0.2))
VIABLE = np.zeros(N, bool); VIABLE[list(V)] = True


class World:
    def __init__(self, kind, seed):
        self.kind = kind; self.rng = np.random.default_rng([seed, 7]); self.k = DELAY if kind == "delayed" else 0
        self.t = 0; self.s = int(self.rng.choice(V)); self.pend = [1] * self.k   # pending action indices (1 = 'stay')
    def n_ctx(self): return N * 3 ** self.k
    def ctx(self):
        x = self.s
        for a in self.pend: x = x * 3 + a
        return x
    def step(self, a_idx):
        if not VIABLE[self.s]:                                             # after a cut: restart in V
            self.s = int(self.rng.choice(V)); self.pend = [1] * self.k; self.t += 1
            return True, True                                               # (restarted, viable)
        if self.k: eff = self.pend[-1]; self.pend = [a_idx] + self.pend[:-1]
        else: eff = a_idx
        if self.kind == "martingale":
            self.s = int(self.rng.integers(N))
        else:
            push = 1 if self.rng.random() < P_WIND else 0
            if self.kind == "switch" and self.t >= T // 2: push = -push
            self.s = (self.s + ACTIONS[eff] + push) % N
        self.t += 1
        return False, bool(VIABLE[self.s])


def state_of(x, k): return x // 3 ** k


class Planner:
    def __init__(self, n_ctx, k, rng, decay=1.0):
        self.A = np.full((n_ctx, 3, n_ctx), ALPHA0); self.k = k; self.rng = rng; self.decay = decay
        pref = np.where(VIABLE[state_of(np.arange(n_ctx), k)], 0.0, -PREF_COST)
        self.lnC = pref - np.log(np.exp(pref).sum())
        self.seqs = np.array(list(itertools.product(range(3), repeat=H)))
    def act(self, x, _t):
        T_ = self.A / self.A.sum(-1, keepdims=True)
        Q = T_[x]                                                           # (3, X): after the first action
        def risk(q): return (q * (np.log(np.maximum(q, 1e-300)) - self.lnC)).sum(-1)
        G = risk(Q)                                                         # (3,)
        Qs, Gs = Q, G
        for _ in range(1, H):
            Qs = np.einsum("...x,xby->...by", Qs, T_)                      # add one action axis
            Gs = Gs[..., None] + risk(Qs)
        g = Gs.reshape(-1)
        p = np.exp(-GAMMA * (g - g.min())); p /= p.sum()
        first = p.reshape(3, -1).sum(1)
        return int(self.rng.choice(3, p=first))
    def learn(self, x, a, x2):
        if self.decay < 1.0: self.A = ALPHA0 + (self.A - ALPHA0) * self.decay
        self.A[x, a, x2] += 1.0
    def cut(self): pass


class Regenerator:
    def __init__(self, n_ctx, rng, weights="dur", beta_rel=BETA_REL, eps=EPS):
        self.n = n_ctx; self.rng = rng; self.weights = weights; self.beta_rel = beta_rel; self.eps = eps
        self.past = []; self.cur = np.zeros((n_ctx, 3)); self.tau = 0
        self.pol = np.full((n_ctx, 3), 1 / 3)
    def act(self, x, _t):
        if self.rng.random() < self.eps: return int(self.rng.integers(3))
        return int(self.rng.choice(3, p=self.pol[x]))
    def learn(self, x, a, _x2): self.cur[x, a] += 1.0; self.tau += 1
    def cut(self):
        """The occasion ends: it joins the settled past, and the next one is seeded from it (A6)."""
        if self.tau == 0: return
        self.past.append((self.cur.copy(), self.tau)); self.cur[:] = 0; self.tau = 0
        taus = np.array([t for _, t in self.past], float); M = len(taus)
        if self.weights == "dur":
            lw = self.beta_rel / taus.mean() * taus
        else:
            lw = (M - 1 - np.arange(M)) * np.log(Q_AGE)
        w = np.exp(lw - lw.max())
        C = np.stack([c for c, _ in self.past])                             # (M, X, 3)
        tot = C.sum(-1)                                                     # (M, X)
        vis = tot > 0
        P = np.where(vis[..., None], C / np.maximum(tot, 1)[..., None], 0.0)
        W = w[:, None] * vis                                                # weight only occasions that visited x
        Wn = W / np.maximum(W.sum(0, keepdims=True), 1e-300)
        m = np.einsum("mx,mxa->xa", Wn, np.sqrt(P)) ** 2                   # sphere (Fisher-Rao) weighted mean
        s = m.sum(-1, keepdims=True)
        self.pol = np.where(s > 0, m / np.maximum(s, 1e-300), 1 / 3)


class Random:
    def __init__(self, rng): self.rng = rng
    def act(self, x, _t): return int(self.rng.integers(3))
    def learn(self, *a): pass
    def cut(self): pass


def run(env, agent_name, seed, **kw):
    w = World(env, seed); rng = np.random.default_rng([seed, 11]); X = w.n_ctx()
    ag = {"planner": lambda: Planner(X, w.k, rng), "planner-v": lambda: Planner(X, w.k, rng, decay=DECAY),
          "R-dur": lambda: Regenerator(X, rng, "dur", **kw), "R-age": lambda: Regenerator(X, rng, "age", **kw),
          "random": lambda: Random(rng)}[agent_name]()
    viable = 0; scored = 0; cuts = 0
    for t in range(T):
        x = w.ctx(); a = ag.act(x, t)
        restarted, ok = w.step(a)
        if restarted:
            ag.cut(); continue                                              # the restart is the world's move: not scored
        ag.learn(x, a, w.ctx()); scored += 1; viable += int(ok); cuts += int(not ok)
    return viable / scored, cuts


_CACHE = {}


def score(env, agent, seed, **kw):
    key = (env, agent, seed, tuple(sorted(kw.items())))
    if key not in _CACHE: _CACHE[key] = run(env, agent, seed, **kw)[0]
    return _CACHE[key]


def compare(env, a, b="planner", **kw):
    fa = np.array([score(env, a, s, **kw) for s in SEEDS]); fb = np.array([score(env, b, s) for s in SEEDS])
    d = fa - fb; step = max(STEP_MIN, 2 * d.std(ddof=1) / np.sqrt(len(d)))
    lab = "TIE" if abs(d.mean()) < step else (f"{a} AHEAD" if d.mean() > 0 else f"{b} AHEAD")
    return fa, fb, d, step, lab


def main():
    print("Tense test (ontology/checks/tense_gate.py): synthetic; score = fraction of steps in the viable arc; "
          f"{len(SEEDS)} seeds, T = {T}, ring N = {N}, V = {V}, push probability {P_WIND}, delay {DELAY} on 'delayed'")
    print("[1] Gate")
    _, fb, d, step, lab = compare("martingale", "random")
    neg_ok = lab == "TIE"
    print(f"    NEG martingale: random {np.mean(fb + d):.4f} vs planner {fb.mean():.4f}; d {d.mean():+.4f}, step {step:.4f} -> {lab} (must TIE: {'ok' if neg_ok else 'VIOLATION'})")
    _, fb, d, step, lab = compare("drift", "random")
    pos_ok = lab == "planner AHEAD"
    print(f"    POS drift: random {np.mean(fb + d):.4f} vs planner {fb.mean():.4f}; d {d.mean():+.4f}, step {step:.4f} -> {lab} (must be planner AHEAD: {'ok' if pos_ok else 'VIOLATION'})")
    print("    " + ("GATE OPEN" if neg_ok and pos_ok else "GATE CLOSED"))
    print("[2] The test: each regenerator against the planner (and against the volatile planner), per world")
    table = {}
    for env in ENVS:
        for reg in ("R-dur", "R-age"):
            for base in ("planner", "planner-v"):
                fa, fb, d, step, lab = compare(env, reg, base)
                table[(env, reg, base)] = lab
                print(f"    {env:10s} {reg} {fa.mean():.4f} vs {base} {fb.mean():.4f}: d {d.mean():+.4f} (step {step:.4f}; seeds ahead {int((d > 0).sum())}/{len(d)}) -> {lab}")
    print("[2b] The floor: planner against random per world (where the planner is not a step above random, the world decides nothing)")
    decidable = {}
    for env in ENVS:
        fa, fb, d, step, lab = compare(env, "planner", "random")
        decidable[env] = lab == "planner AHEAD"
        print(f"    {env:10s} planner {fa.mean():.4f} vs random {fb.mean():.4f}: d {d.mean():+.4f} (step {step:.4f}) -> {lab}; decidable {decidable[env]}")
    print("[3] Sensitivity of R-dur against the planner (beta_rel x eps) on the structured worlds")
    flips = 0; cells = 0
    for env in ("drift", "delayed", "switch"):
        base_lab = table[(env, "R-dur", "planner")]
        row = []
        for br in SENS["beta_rel"]:
            for ep in SENS["eps"]:
                *_, lab = compare(env, "R-dur", "planner", beta_rel=br, eps=ep)
                cells += 1; flips += int(lab != base_lab); row.append(f"({br},{ep}):{lab.split()[0]}")
        print(f"    {env:10s} registered {base_lab}: " + " ".join(row))
    print(f"    labels differing from the registered cell: {flips} of {cells}")
    print("[4] Reading (computed)")
    for env in ENVS:
        lab = table[(env, "R-dur", "planner")]
        if not decidable[env]:
            cost = "NOT DECIDABLE: the planner is not a step above random here, so a tie is two agents at the floor"
        else:
            cost = "A8's empty future costs nothing here" if lab == "TIE" else ("the cost of A8 is measured here" if lab == "planner AHEAD" else "the planner's future content was a liability here")
        print(f"    {env:10s}: R-dur vs planner {lab} -> {cost}")


if __name__ == "__main__":
    main()
