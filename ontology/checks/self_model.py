"""Self-representation and equanimity (ontology/12_self_representation.md; owner request prompt-log entries 92-93).
Synthetic, no data. The worlds, the planner, the regenerator and the scoring are the tense test's
(ontology/checks/tense_gate.py), imported unchanged. The design below was committed and pushed before the first run.

The question. The tense test found that a valence-free A6 regenerator loses to an active-inference planner where the world
has exploitable structure. The planner has two things the regenerator lacks: a forward model and a GIVEN preference for
the viable arc. The owner's reading: a system needs a model so it can represent itself, and a goal is its own continuation
projected through that self-representation. Three new agents separate the pieces; none is given the viable arc.
    R-F   A6 regenerator whose past occasions are reweighted by their FORECAST persistence under a learned world model
          (pi_m ~ exp(beta f_m / mean f), f_m = the occasion's policy's expected steps before a cut over H steps, from the
          occasion's own visited contexts); it regenerates only contents that actually happened (no counterfactuals).
          Only the last FORECAST_WINDOW occasions are evaluated (a named bound).
    S     self-model: Dirichlet counts over (context, action) -> next context OR the cut (its own ending, learned from
          experience); acts by softmax(GAMMA x Q), Q = expected steps before its own next cut over H steps (value
          iteration). Its 'goal' is its own continuation, derived from its model of itself; nothing tells it where V is.
          Its context includes its own in-flight actions on 'delayed' (self-representation through time).
    S-noself  S with the context reduced to the world state (it cannot represent its own in-flight actions). Identical to
          S where the delay is 0.
Equanimity. S acting on a mixture of two pulls: the settled past (the R-dur regenerator's policy, centred log-probabilities
l_R) and its self-forecast (centred GAMMA x Q, l_S): l = l_R + w l_S, w = OMEGA x |l_R| / |l_S| (H-EQ's ratio on policies:
at OMEGA = 1 the imagined future pulls exactly as hard as the settled past). OMEGA < 1 leans on habit; OMEGA > 1 leans on
the imagined future. Endpoints: R-dur (past only) and S (forecast only). A fixed w = 1 mixture is the constant the ratio
must beat (R7). All acting agents except the planner take a uniform action with probability EPS (as R-dur).

Labels (computed, R15): paired per-seed differences; TIE if |mean d| < step, step = max(STEP_MIN, 2 SE of d).
Gate: NEG martingale S vs random must TIE; POS drift S vs R-dur must be S AHEAD (counterfactual content is resolvable);
DECOY drift S vs S-noself must TIE (identical by construction at delay 0).
Tests: T-1 R-F vs R-dur and vs planner; T-2 S vs planner; T-3 S vs S-noself on 'delayed'; T-4 the OMEGA grid per world:
the best OMEGA, the members within a step of the best (the plateau), whether OMEGA = 1 is on it, and the ratio against the
fixed w = 1 mixture.
Phenomenological proxies (report only; functional correlates, not experience): steadiness = CV of occasion durations;
openness = mean entropy (nats) of the action distribution acted on (not measured for the planner: n/a); self-surprise = mean -log of the model's probability of
the cut at the steps where the cut happened (model-bearing agents); pull share = mean w|l_S| / (|l_R| + w|l_S|) (exactly 0.5
at every OMEGA = 1 step by construction; informative for the fixed-weight mixture and the other OMEGA).
    uv run python ontology/checks/self_model.py > ontology/checks/self_model.txt
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tense_gate as TG  # noqa: E402
from tense_gate import (ALPHA0, BETA_REL, ENVS, EPS, GAMMA, H, N, SEEDS, STEP_MIN, T,  # noqa: E402
                        Planner, Random, Regenerator, World, state_of)

OMEGAS = (0.25, 0.5, 1.0, 2.0, 4.0)
FORECAST_WINDOW = 50


def _centred(l):
    return l - l.mean()


class SelfModel:
    """Counts over (context, action) -> next context or the cut (index Xm)."""
    def __init__(self, n_ctx, k, self_rep=True):
        self.k = k; self.self_rep = self_rep; self.Xm = n_ctx if self_rep else N
        self.A = np.full((self.Xm, 3, self.Xm + 1), ALPHA0); self._Q = None
    def m(self, x): return x if self.self_rep else state_of(x, self.k)
    def observe(self, x, a, x2, cut):
        self.A[self.m(x), a, self.Xm if cut else self.m(x2)] += 1.0; self._Q = None
    def p_cut(self, x, a): return float(self.A[self.m(x), a, self.Xm] / self.A[self.m(x), a].sum())
    def trans(self): return self.A / self.A.sum(-1, keepdims=True)
    def Q(self):
        if self._Q is None:
            Tm = self.trans()[:, :, :self.Xm]; Vh = np.zeros(self.Xm)
            for _ in range(H):
                Qh = Tm @ (1.0 + Vh); Vh = Qh.max(1)
            self._Q = Qh
        return self._Q
    def evaluate(self, P):
        """H-step expected steps before the cut for policies P (M, Xm, 3)."""
        Tm = self.trans()[:, :, :self.Xm]; Vp = np.zeros((P.shape[0], self.Xm))
        for _ in range(H):
            nxt = np.einsum("xay,my->mxa", Tm, 1.0 + Vp); Vp = (P * nxt).sum(-1)
        return Vp


class Phenom:
    """Running phenomenological proxies."""
    def __init__(self): self.ent = 0.0; self.n = 0; self.sur = []; self.share = []; self.durs = []; self.tau = 0
    def acted(self, p):
        p = (1 - EPS) * p + EPS / 3; self.ent += float(-(p * np.log(p)).sum()); self.n += 1
    def tick(self): self.tau += 1
    def ended(self):
        if self.tau: self.durs.append(self.tau)
        self.tau = 0
    def summary(self):
        d = np.array(self.durs, float)
        return dict(steadiness=float(d.std() / d.mean()) if len(d) > 1 else float("nan"),
                    openness=self.ent / self.n if self.n else float("nan"),       # nan where the action distribution is not measured (the planner)
                    surprise=float(np.mean(self.sur)) if self.sur else float("nan"),
                    share=float(np.mean(self.share)) if self.share else float("nan"))


def _softmax(l):
    p = np.exp(l - l.max()); return p / p.sum()


class SelfAgent:
    """S (omega None, fixed_w None), an equanimity mixture (omega), or a fixed-weight mixture (fixed_w)."""
    def __init__(self, n_ctx, k, rng, self_rep=True, omega=None, fixed_w=None):
        self.model = SelfModel(n_ctx, k, self_rep); self.reg = Regenerator(n_ctx, rng, "dur")
        self.rng = rng; self.omega = omega; self.fixed_w = fixed_w; self.ph = Phenom()
    def act(self, x, _t):
        lS = _centred(GAMMA * self.model.Q()[self.model.m(x)])
        if self.omega is None and self.fixed_w is None:
            l = lS
        else:
            lR = _centred(np.log(np.maximum(self.reg.pol[x], 1e-12)))
            nR, nS = np.linalg.norm(lR), np.linalg.norm(lS)
            w = self.fixed_w if self.fixed_w is not None else (self.omega * nR / nS if nS > 0 else 0.0)
            l = lR + w * lS
            if nR + w * nS > 0: self.ph.share.append(w * nS / (nR + w * nS))
        p = _softmax(l); self.ph.acted(p)
        if self.rng.random() < EPS: return int(self.rng.integers(3))
        return int(self.rng.choice(3, p=p))
    def learn(self, x, a, x2, cut):
        if cut: self.ph.sur.append(-np.log(self.model.p_cut(x, a)))
        self.model.observe(x, a, x2, cut); self.reg.learn(x, a, x2); self.ph.tick()
    def cut(self): self.reg.cut(); self.ph.ended()


class ForecastRegenerator(Regenerator):
    """R-F: A6 regeneration with past occasions weighted by forecast persistence (actual contents only)."""
    def __init__(self, n_ctx, k, rng):
        super().__init__(n_ctx, rng, "dur"); self.model = SelfModel(n_ctx, k, True); self.ph = Phenom()
    def act(self, x, t):
        self.ph.acted(self.pol[x]); return super().act(x, t)
    def learn(self, x, a, x2, cut=False):
        if cut: self.ph.sur.append(-np.log(self.model.p_cut(x, a)))
        self.model.observe(x, a, x2, cut); super().learn(x, a, x2); self.ph.tick()
    def cut(self):
        self.ph.ended()
        if self.tau == 0: return
        self.past.append((self.cur.copy(), self.tau)); self.cur[:] = 0; self.tau = 0
        win = self.past[-FORECAST_WINDOW:]
        C = np.stack([c for c, _ in win]); tot = C.sum(-1); vis = tot > 0
        P = np.where(vis[..., None], C / np.maximum(tot, 1)[..., None], 1 / 3)
        Vp = self.model.evaluate(P)                                          # (M, X)
        d = tot / tot.sum(1, keepdims=True)
        f = (d * Vp).sum(1)
        lw = BETA_REL / max(f.mean(), 1e-12) * f; w = np.exp(lw - lw.max())
        W = w[:, None] * vis; Wn = W / np.maximum(W.sum(0, keepdims=True), 1e-300)
        m = np.einsum("mx,mxa->xa", Wn, np.sqrt(np.where(vis[..., None], P, 0.0))) ** 2
        s = m.sum(-1, keepdims=True); self.pol = np.where(s > 0, m / np.maximum(s, 1e-300), 1 / 3)


class Tracked:
    """Wraps the tense test's agents with the proxies (steadiness, openness)."""
    def __init__(self, inner): self.inner = inner; self.ph = Phenom()
    def act(self, x, t):
        a = self.inner.act(x, t)
        if isinstance(self.inner, Regenerator): self.ph.acted(self.inner.pol[x])
        elif isinstance(self.inner, Random): self.ph.acted(np.full(3, 1 / 3))
        return a
    def learn(self, x, a, x2, cut=False): self.inner.learn(x, a, x2); self.ph.tick()
    def cut(self): self.inner.cut(); self.ph.ended()


def make(agent, w, rng):
    X, k = w.n_ctx(), w.k
    if agent == "planner": return Tracked(Planner(X, k, rng))
    if agent == "random": return Tracked(Random(rng))
    if agent == "R-dur": return Tracked(Regenerator(X, rng, "dur"))
    if agent == "R-F": return ForecastRegenerator(X, k, rng)
    if agent == "S": return SelfAgent(X, k, rng)
    if agent == "S-noself": return SelfAgent(X, k, rng, self_rep=False)
    if agent == "fixed-w1": return SelfAgent(X, k, rng, fixed_w=1.0)
    if agent.startswith("omega"): return SelfAgent(X, k, rng, omega=float(agent[5:]))
    raise ValueError(agent)


_CACHE = {}


def run(env, agent, seed):
    key = (env, agent, seed)
    if key in _CACHE: return _CACHE[key]
    w = World(env, seed); rng = np.random.default_rng([seed, 11]); ag = make(agent, w, rng)
    viable = scored = 0
    for t in range(T):
        x = w.ctx(); a = ag.act(x, t)
        restarted, ok = w.step(a)
        if restarted: ag.cut(); continue
        ag.learn(x, a, w.ctx(), not ok); scored += 1; viable += int(ok)
    ag.cut()
    _CACHE[key] = (viable / scored, ag.ph.summary())
    return _CACHE[key]


def compare(env, a, b):
    fa = np.array([run(env, a, s)[0] for s in SEEDS]); fb = np.array([run(env, b, s)[0] for s in SEEDS])
    d = fa - fb; step = max(STEP_MIN, 2 * d.std(ddof=1) / np.sqrt(len(d)))
    lab = "TIE" if abs(d.mean()) < step else (f"{a} AHEAD" if d.mean() > 0 else f"{b} AHEAD")
    return fa.mean(), fb.mean(), d.mean(), step, lab


def line(env, a, b):
    ma, mb, d, step, lab = compare(env, a, b)
    print(f"    {env:10s} {a} {ma:.4f} vs {b} {mb:.4f}: d {d:+.4f} (step {step:.4f}) -> {lab}")
    return lab


def main():
    print(f"Self-representation and equanimity (ontology/checks/self_model.py): the tense test's worlds; {len(SEEDS)} seeds, T = {T}")
    print("[1] Gate")
    g = [line("martingale", "S", "random") == "TIE", line("drift", "S", "R-dur") == "S AHEAD", line("drift", "S", "S-noself") == "TIE"]
    print("    must: NEG TIE, POS S AHEAD, DECOY TIE -> " + " ".join("ok" if x else "VIOLATION" for x in g))
    print("    " + ("GATE OPEN" if all(g) else "GATE CLOSED"))
    print("[2] T-1 forecast without counterfactuals: R-F against R-dur and against the planner")
    for env in ENVS:
        line(env, "R-F", "R-dur"); line(env, "R-F", "planner")
    print("[3] T-2 self-continuation as the goal: S (no given preference) against the planner (given the viable arc)")
    t2 = {env: line(env, "S", "planner") for env in ENVS}
    print("[4] T-3 self-representation through time: S against S-noself on 'delayed'")
    t3 = line("delayed", "S", "S-noself")
    print("[5] T-4 equanimity: the OMEGA grid of the past/forecast mixture, per world (endpoints R-dur = past only, S = forecast only)")
    arms = ["R-dur"] + [f"omega{o:g}" for o in OMEGAS] + ["S", "fixed-w1"]
    t4 = {}
    for env in ENVS:
        sc = {a: np.array([run(env, a, s)[0] for s in SEEDS]) for a in arms}
        grid = ["R-dur"] + [f"omega{o:g}" for o in OMEGAS] + ["S"]
        best = max(grid, key=lambda a: sc[a].mean())
        plateau = []
        for a in grid:
            d = sc[a] - sc[best]; step = max(STEP_MIN, 2 * d.std(ddof=1) / np.sqrt(len(d)))
            if a == best or abs(d.mean()) < step: plateau.append(a)
        on = "omega1" in plateau
        d = sc["omega1"] - sc["fixed-w1"]; step = max(STEP_MIN, 2 * d.std(ddof=1) / np.sqrt(len(d)))
        vs_fixed = "TIE" if abs(d.mean()) < step else ("ratio AHEAD" if d.mean() > 0 else "fixed w = 1 AHEAD")
        t4[env] = (best, plateau, on, vs_fixed)
        print(f"    {env:10s} " + " ".join(f"{a}:{sc[a].mean():.4f}" for a in arms))
        print(f"    {'':10s} best {best}; within a step of the best: {plateau}; OMEGA = 1 on the plateau: {on}; OMEGA = 1 against fixed w = 1: {vs_fixed} (d {d.mean():+.4f}, step {step:.4f})")
    print("[6] Phenomenological proxies (report only): steadiness = CV of occasion durations (lower = steadier), openness = mean action entropy (nats; max 1.0986),")
    print("    self-surprise = mean -log P(cut) at its own cuts, pull share = the imagined future's share of the total pull; seed means")
    for env in ENVS:
        for a in ("R-dur", "omega0.25", "omega1", "omega4", "S", "planner"):
            ph = [run(env, a, s)[1] for s in SEEDS]
            def m(k): v = [p[k] for p in ph if np.isfinite(p[k])]; return f"{np.mean(v):.4f}" if v else "n/a"
            print(f"    {env:10s} {a:10s} steadiness {m('steadiness')}  openness {m('openness')}  self-surprise {m('surprise')}  pull share {m('share')}")
    print("[7] Reading (computed)")
    for env in ENVS:
        lab = t2[env]
        r = ("a learned goal of self-continuation matches a given preference here" if lab == "TIE" else
             "the given preference adds something self-continuation does not" if lab == "planner AHEAD" else
             "self-continuation does better than the given preference here")
        print(f"    T-2 {env:10s}: S vs planner {lab} -> {r}")
    print(f"    T-3 delayed: S vs S-noself {t3} -> " + ("representing its own in-flight actions matters" if t3 == "S AHEAD" else
          "representing its own in-flight actions did not help within this budget" if t3 == "TIE" else "the self-representation hurt within this budget"))
    for env in ENVS:
        best, plateau, on, vs_fixed = t4[env]
        print(f"    T-4 {env:10s}: " + ("equanimity (OMEGA = 1) is on the plateau of the best" if on else f"equanimity is behind the best ({best}) by a step")
              + f"; against the fixed constant: {vs_fixed}")


if __name__ == "__main__":
    main()
