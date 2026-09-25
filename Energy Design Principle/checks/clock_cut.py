"""Does a cut on content beat a cut on the clock? The own-clock (arc) cut against fixed budgets, confidence and stability.

Declared in `Energy Design Principle/DECLARATION_2.md` Part A (pushed at 4b3b995 before this script existed).
Synthetic, no data. Run: python3 "Energy Design Principle/checks/clock_cut.py"
"""
import math

import numpy as np

K, TMAX = 4, 256
MU = np.arange(K, dtype=float)
N_CAL = N_TEST = 4000
SEEDS = range(5)
DEFAULT_T = 16
W_REG, AMIN_REG = 4, 2 * math.acos(0.5) / 2          # 1.0472
C_GRID = [round(0.5 + 0.05 * i, 2) for i in range(10)] + [0.97, 0.98, 0.99, 0.995, 0.999, 0.9999]
THETA_GRID = list(np.logspace(-4, 0, 30))
WS_GRID = list(range(1, 65))
T_GRID = list(range(1, TMAX + 1))
SENS_W = [2, 4, 8]
SENS_AMIN = [0.0, 2 * math.acos(0.5) / 4, 2 * math.acos(0.5) / 2]


def world(name, n, rng):
    c = rng.integers(0, K, n)
    t = np.arange(1, TMAX + 1)
    if name == 'W0':
        sig = np.where(t < 32, 1e6, 0.05)[None, :].repeat(n, 0)
    elif name == 'W1':
        sig = np.full((n, TMAX), 2.0)
    else:
        s = np.exp(rng.uniform(math.log(0.5), math.log(4.0), n))
        sig = s[:, None].repeat(TMAX, 1)
    mean = MU[c][:, None].repeat(TMAX, 1)
    if name == 'W3':
        tau = rng.geometric(1 / 24, n)
        bad = (t[None, :] > tau[:, None]) & (rng.random((n, TMAX)) < 0.3)
        wrong = (c[:, None] + rng.integers(1, K, (n, TMAX))) % K
        mean = np.where(bad, MU[wrong], mean)
    x = mean + sig * rng.standard_normal((n, TMAX))
    ll = -np.cumsum((x[:, :, None] - MU[None, None, :]) ** 2 / (2 * sig[:, :, None] ** 2), axis=1)
    ll -= ll.max(axis=2, keepdims=True)
    p = np.exp(ll)
    p /= p.sum(axis=2, keepdims=True)
    return c, p


class Run:
    def __init__(self, c, p):
        self.n = len(c)
        self.p = p
        am = p.argmax(axis=2)
        self.correct = (am == c[:, None])
        self.maxp = p.max(axis=2)
        prev = np.concatenate([np.full((self.n, 1, K), 1.0 / K), p[:, :-1, :]], axis=1)
        bc = np.clip(np.sqrt(p * prev).sum(axis=2), 0.0, 1.0)
        self.d = 2 * np.arccos(bc)                       # Fisher-Rao step length (sqrt-probability sphere, radius 2)
        self.arc = np.cumsum(self.d, axis=1)
        r = np.ones_like(am)
        for t in range(1, TMAX):
            r[:, t] = np.where(am[:, t] == am[:, t - 1], r[:, t - 1] + 1, 1)
        self.run = r

    @staticmethod
    def first(mask):
        hit = mask.any(axis=1)
        return np.where(hit, mask.argmax(axis=1) + 1, TMAX)

    def stop(self, arm, par, w=W_REG, amin=AMIN_REG):
        if arm == 'S0':
            return np.full(self.n, TMAX)
        if arm in ('S1a', 'S1b'):
            return np.full(self.n, par)
        if arm == 'S2':
            return self.first(self.maxp >= par)
        if arm == 'S3':
            cs = np.cumsum(self.d < par, axis=1)
            lag = np.concatenate([np.zeros((self.n, w), dtype=cs.dtype), cs[:, :-w]], axis=1)
            full = (cs - lag == w) & (np.arange(1, TMAX + 1)[None, :] >= w)   # the last w steps all below theta
            return self.first(full & (self.arc >= amin))
        if arm == 'S4':
            return self.first(self.run >= par)
        raise ValueError(arm)

    def score(self, s):
        return self.correct[np.arange(self.n), s - 1], s


def tune(run, arm, target, **kw):
    grid = {'S1b': T_GRID, 'S2': C_GRID, 'S3': THETA_GRID, 'S4': WS_GRID}[arm]
    best, best_acc = None, None
    for g in grid:
        corr, s = run.score(run.stop(arm, g, **kw))
        acc, cost = 100 * corr.mean(), s.mean()
        if acc >= target and (best is None or cost < best[1]):
            best = (g, cost)
        if best_acc is None or acc > best_acc[1]:
            best_acc = (g, acc)
    return best[0] if best else best_acc[0]


def label(cx, sx, cy, sy):
    ratio = sx.mean() / sy.mean()
    dq = 100 * (cx.astype(float) - cy.astype(float))
    step = max(1.0, 2 * dq.std(ddof=1) / math.sqrt(len(dq)))
    q = dq.mean()
    cl = 'SAVES' if ratio <= 0.90 else ('COSTS' if ratio >= 1.10 else 'SAME')
    ql = 'AHEAD' if q >= step else ('BEHIND' if q <= -step else 'NB')
    if (cl == 'SAVES' and ql != 'BEHIND') or (cl != 'COSTS' and ql == 'AHEAD'):
        lab = 'BETTER'
    elif (cl == 'COSTS' and ql != 'AHEAD') or (cl != 'SAVES' and ql == 'BEHIND'):
        lab = 'WORSE'
    elif cl == 'SAVES' and ql == 'BEHIND' or cl == 'COSTS' and ql == 'AHEAD':
        lab = 'TRADE-OFF'
    else:
        lab = 'TIE'
    return lab, ratio, q, step


def across(labels):
    for lab in ('BETTER', 'WORSE', 'TRADE-OFF', 'TIE'):
        if labels.count(lab) >= 4:
            return lab
    return 'MIXED'


def run_world(name, w=W_REG, amin=AMIN_REG):
    res = []
    for seed in SEEDS:
        rng = np.random.default_rng(1000 * seed + {'W0': 0, 'W1': 1, 'W2': 2, 'W3': 3}[name])
        cal = Run(*world(name, N_CAL, rng))
        test = Run(*world(name, N_TEST, rng))
        target = 100 * cal.correct[:, -1].mean() - 1.0
        pars = {'S0': None, 'S1a': DEFAULT_T}
        for arm in ('S1b', 'S2', 'S3', 'S4'):
            pars[arm] = tune(cal, arm, target, **({'w': w, 'amin': amin} if arm == 'S3' else {}))
        out = {}
        for arm, par in pars.items():
            kw = {'w': w, 'amin': amin} if arm == 'S3' else {}
            out[arm] = test.score(test.stop(arm, par, **kw))
        res.append((pars, out))
    return res


def cmp(res, x, y):
    labs = [label(*o[x], *o[y]) for _, o in res]
    return across([l[0] for l in labs]), labs


def main():
    print('clock_cut: own-clock (arc) cut against step-clock budgets, confidence and stability (DECLARATION_2 Part A)')
    print(f'K={K}, T_max={TMAX}, items {N_CAL} calibration + {N_TEST} test per world and seed, seeds {list(SEEDS)}; '
          f'S3 registered w={W_REG}, a_min={AMIN_REG:.4f}')
    print('label: BETTER = (SAVES and not BEHIND) or (not COSTS and AHEAD); step = max(1.0 pt, 2 x paired SE); '
          'across seeds: the label in >= 4 of 5, else MIXED')
    print()
    R = {w: run_world(w) for w in ('W0', 'W1', 'W2', 'W3')}

    def show(tag, world, x, y, required=None):
        lab, labs = cmp(R[world], x, y)
        per = '; '.join(f'{l} {r:.4f} {q:+.2f}/{s:.2f}' for l, r, q, s in labs)
        ok = '' if required is None else ('  -> holds' if required(lab) else '  -> DOES NOT HOLD')
        print(f'  {tag:4} {world} {x:3} vs {y:3}: {lab:9} [per seed: label cost-ratio dQ/step: {per}]{ok}')
        return lab

    print('GATE (read first; nothing after it is a result if it closes)')
    g1 = [show('G1', w, 'S2', 'S1b', lambda l: l == 'BETTER') for w in ('W1', 'W2')]
    g2 = [show('G2', 'W0', a, 'S1b', lambda l: l != 'BETTER') for a in ('S2', 'S3', 'S4')]
    gate_open = all(l == 'BETTER' for l in g1) and all(l != 'BETTER' for l in g2)
    print(f"  GATE {'OPEN' if gate_open else 'CLOSED'}")
    print()
    if not gate_open:
        print('gate closed: stop (R12)')
        return
    print('Predictions and reports')
    show('G3', 'W2', 'S1a', 'S0', lambda l: l == 'TRADE-OFF')
    f1 = [show('F1', w, 'S3', 'S1b', lambda l: l == 'BETTER') for w in ('W1', 'W2', 'W3')]
    print(f"       F1 (content beats the clock): {'holds' if all(l == 'BETTER' for l in f1) else 'does not hold in every world'}"
          f" -> REDUNDANT-DOMAIN (Wald's sequential test) whatever the outcome")
    c1 = show('C1', 'W1', 'S3', 'S2', lambda l: l != 'BETTER')
    c2 = [show('C2', w, 'S3', 'S2') for w in ('W2', 'W3')]
    c3 = [show('C3', w, 'S3', 'S4') for w in ('W2', 'W3')]
    for w in ('W3',):
        for a in ('S2', 'S3', 'S4'):
            show('O1', w, a, 'S0')
    cand = c1 != 'BETTER' and c2[1] == 'BETTER'
    print(f"  C2 forecast was TIE: W2 {c2[0]}, W3 {c2[1]}; PROSPECTIVE CANDIDATE (S3 BETTER than S2 in W3, not in W1): "
          f"{'yes' if cand else 'no'}")
    print()
    print('Tuned parameters and test accuracy / mean steps, seed 0')
    for w in ('W0', 'W1', 'W2', 'W3'):
        pars, out = R[w][0]
        print(f'  {w}: ' + ', '.join(f"{a}[{(f'{pars[a]:.4g}' if isinstance(pars[a], float) else pars[a])}] "
                                   f"{100 * out[a][0].mean():.2f}% / {out[a][1].mean():.2f}" for a in out))
    print()
    print('Sensitivity of the S3 labels (W2, W3): w x a_min; registered cell marked *')
    flips = {}
    for w in ('W2', 'W3'):
        base = {y: cmp(R[w], 'S3', y)[0] for y in ('S1b', 'S2', 'S4')}
        for ww in SENS_W:
            for am in SENS_AMIN:
                reg = (ww == W_REG and abs(am - AMIN_REG) < 1e-9)
                rr = R[w] if reg else run_world(w, ww, am)
                labs = {y: cmp(rr, 'S3', y)[0] for y in ('S1b', 'S2', 'S4')}
                for y in labs:
                    flips.setdefault((w, y), 0)
                    flips[(w, y)] += labs[y] != base[y]
                print(f"  {w} w={ww} a_min={am:.4f}{'*' if reg else ' '}: " + ', '.join(f'S3 vs {y} {labs[y]}' for y in labs))
    print('  cells flipping from the registered label: ' + ', '.join(f'{w} S3 vs {y}: {n}' for (w, y), n in flips.items()))
    print('  FRAGILE (> 1 flip): ' + (', '.join(f'{w} S3 vs {y}' for (w, y), n in flips.items() if n > 1) or 'none'))


if __name__ == '__main__':
    main()
