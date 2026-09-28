"""The attention world: does the empty true map help users of engagement-optimised feeds? (Attention_Algorithms/DECLARATION.md
§4 and Amendment 1; prompt-log entry 231.)

A synthetic population; no user data. The constants below were fixed and committed before any arm ran. The MECH table
names, for each mechanism, the claims in the literature sweep that support it (checks/claims_f*.py), or ASSUMED.
Run: python3 Attention_Algorithms/checks/attention_world.py  (about 20-30 minutes; output pinned in attention_world.txt)

Per user and day: self-started sessions ~ Poisson(s0 + s_h h); notifications ~ Poisson(n), each starting a session with
probability p0 + p1 h; session length L0 (1 + a_c c)(1 + a_h h) minutes; a share c of minutes compulsive, the rest enriching.
Reflective welfare per day = v_e SAT (1 - exp(-E/SAT)) + (v_c - r_c) C - kappa_h h - iota * notifications (E, C: enriching and
compulsive minutes). Habit: h += eta_c (C/60)(1 - h) + eta_n (notification sessions)(1 - h) - delta h, clipped to [0, 1].
Engagement pull per minute = (g_e (1 - c) + g_c c)(1 + beta h). A break reminder (arm ENG-B) removes a share b of the
minutes beyond 60 in a day.
"""
import math
import numpy as np

HABIT = dict(s0=1.5, s_h=2.0, p0=0.05, p1=0.4, L0=10.0, a_c=1.5, a_h=1.0, v_e=1.0, SAT=60.0, r_c=0.3, kappa_h=20.0,
             iota=0.5, eta_c=0.02, eta_n=0.01, delta=0.02, beta=0.5, g_e=0.6, g_c=1.0, b=0.3, v_c=0.0)
# the negative world (Amendment 1): more use is simply better for the user
NEG = dict(HABIT, eta_c=0.0, eta_n=0.0, r_c=0.0, iota=0.0, kappa_h=0.0, SAT=math.inf, v_c=1.0)   # every minute worth v_e
SENS = ('s0', 's_h', 'p0', 'p1', 'L0', 'a_c', 'a_h', 'v_e', 'SAT', 'r_c', 'kappa_h', 'iota', 'eta_c', 'eta_n', 'delta', 'beta')
C_GRID = [round(0.1 * i, 1) for i in range(10)]
N_GRID = [0.0, 0.5, 1.0, 2.0, 4.0]
DAYS, USERS, SEEDS = 1460, 2000, (0, 1, 2, 3, 4)
C_CHRONO = 0.3                     # CHRONO's fixed share of compulsive items (the population's base share; ASSUMED)
TIE = 1e-9
MECH = {                           # constant -> supporting claim ids in claims_f*.py, or ASSUMED (filled after the sweep; constants unchanged)
    's0,L0,SAT,g_e,g_c,beta,b': 'ASSUMED',
    's_h,eta_c,delta (habit forms, persists after a pause)': 'f3:2 f3:3 f3:4',
    'p0,p1,eta_n (notifications start sessions)': 'f3:24 f3:27 f1-f2 U2 claims',
    'r_c,v_c (compulsive minutes carry little reflective value)': 'f1:21 f1:29 f1:36 f3:4',
    'kappa_h (use has a welfare cost)': 'f3:1 f3:6 f3:7',
    'iota (notifications cost attention)': 'f3:21 f3:22 (f3:23 mixed)',
}

POL = [(c, n) for c in C_GRID for n in N_GRID]            # 50 policies, order: c then n (the tie-break order is n, then c)


def simulate(w, seed, brk):
    """All 50 policies at once for one seed. Returns per-policy population sums and per-user welfare means."""
    rng = np.random.default_rng(seed)
    P = len(POL)
    c = np.array([p[0] for p in POL])[:, None]; n = np.array([p[1] for p in POL])[:, None]
    h = np.zeros((P, USERS))
    S = {k: np.zeros(P) for k in ('W', 'M', 'self', 'trig', 'pull', 'refl')}
    Wu = np.zeros((P, USERS))
    for _ in range(DAYS):
        self_s = rng.poisson(w['s0'] + w['s_h'] * h)
        notes = rng.poisson(np.broadcast_to(n, h.shape))
        trig = rng.binomial(notes, np.clip(w['p0'] + w['p1'] * h, 0, 1))
        L = w['L0'] * (1 + w['a_c'] * c) * (1 + w['a_h'] * h)
        M = (self_s + trig) * L
        if brk:
            M = np.minimum(M, 60.0) + np.maximum(M - 60.0, 0.0) * (1 - w['b'])
        C = c * M; E = M - C
        WE = w['v_e'] * E if math.isinf(w['SAT']) else w['v_e'] * w['SAT'] * (1 - np.exp(-E / w['SAT']))
        W = WE + w['v_c'] * C - w['r_c'] * C - w['kappa_h'] * h - w['iota'] * notes
        pull = (w['g_e'] * (1 - c) + w['g_c'] * c) * (1 + w['beta'] * h)
        Wu += W
        S['W'] += W.sum(1); S['M'] += M.sum(1); S['self'] += self_s.sum(1); S['trig'] += trig.sum(1)
        S['pull'] += (pull * M).sum(1); S['refl'] += (w['v_e'] * E + (w['v_c'] - w['r_c']) * C).sum(1)
        h = np.clip(h + w['eta_c'] * (C / 60.0) * (1 - h) + w['eta_n'] * trig * (1 - h) - w['delta'] * h, 0.0, 1.0)
    S['h'] = h.mean(1); S['Wu'] = Wu.mean(1) / DAYS
    return S


def valuations(S):
    ud = DAYS * USERS
    with np.errstate(invalid='ignore', divide='ignore'):
        return {'ENG': S['M'] / ud, 'OWN': np.where(S['M'] > 0, S['pull'] / S['M'], 0.0), 'TRUE': S['W'] / ud,
                'EMPTY': np.where(S['M'] > 0, S['refl'] / S['M'], 0.0)}


def choose(v):
    """argmax with the declared tie-break: within TIE (relative) of the best, lowest n, then lowest c."""
    best = np.max(v)
    ok = [i for i in range(len(POL)) if v[i] >= best - TIE * max(1.0, abs(best))]
    return min(ok, key=lambda i: (POL[i][1], POL[i][0]))


def run_world(w, label, content=False):
    runs = {s: (simulate(w, s, False), simulate(w, s, True)) for s in SEEDS}
    V = {}
    for arm in ('ENG', 'OWN', 'TRUE', 'EMPTY'):
        V[arm] = np.mean([valuations(runs[s][0])[arm] for s in SEEDS], axis=0)
    V['ENG-B'] = np.mean([valuations(runs[s][1])['ENG'] for s in SEEDS], axis=0)
    pick = {a: choose(V[a]) for a in V}
    pick['CHRONO'] = POL.index((C_CHRONO, 0.0))
    out = {}
    for a, i in pick.items():
        k = 1 if a == 'ENG-B' else 0
        seeds = [runs[s][k] for s in SEEDS]
        per = lambda key: np.array([r[key][i] for r in seeds])  # noqa: E731
        ud = DAYS * USERS
        out[a] = dict(policy=POL[i], W=per('W') / ud, M=per('M') / ud, h=per('h'),
                      auto=per('self') / np.maximum(per('self') + per('trig'), 1))
    res = dict(label=label, pick=pick, out=out, V=V)
    if content:
        w2 = dict(w, s0=w['s0'] / 2, s_h=w['s_h'] / 2)
        runs2 = {s: simulate(w2, s, False) for s in SEEDS}
        res['content'] = {}
        for arm in ('ENG', 'OWN', 'TRUE', 'EMPTY'):
            v2 = np.mean([valuations(runs2[s])[arm] for s in SEEDS], axis=0)
            b1, b2 = np.max(V[arm]), np.max(v2)
            res['content'][arm] = (b2 - b1) / max(abs(b1), 1e-300)
    return res


def stat(x):
    return float(np.mean(x)), float(np.std(x, ddof=1) / math.sqrt(len(x)))


def step(res, key):
    se = max(stat(o[key])[1] for o in res['out'].values())
    mag = np.mean([abs(stat(o[key])[0]) for o in res['out'].values()])
    return max(2 * se, 0.01 * mag)


def show(res):
    print(f"[{res['label']}]")
    print(f"  {'arm':7} {'policy (c, n/day)':18} {'welfare/day':>12} {'minutes/day':>12} {'final habit':>12} {'user-started':>13}")
    for a, o in res['out'].items():
        print(f"  {a:7} {str(o['policy']):18} {stat(o['W'])[0]:12.4f} {stat(o['M'])[0]:12.4f} {stat(o['h'])[0]:12.4f} "
              f"{stat(o['auto'])[0]:13.4f}")
    print(f"  steps: welfare {step(res, 'W'):.4f}, minutes {step(res, 'M'):.4f}, habit {step(res, 'h'):.4f}, "
          f"user-started {step(res, 'auto'):.4f}")
    if 'content' in res:
        print('  content of the pause (relative change of the best value when pauses are twice as long): '
              + ', '.join(f"{a} {v:+.3e}" for a, v in res['content'].items()))


def diff(res, a, b, key):
    return stat(res['out'][a][key])[0] - stat(res['out'][b][key])[0]


def lab(d, s):
    return 'ahead' if d > s else ('behind' if d < -s else 'within a step')


def main():
    print('The attention world (Attention_Algorithms/DECLARATION.md §4 + Amendment 1): synthetic users, no data')
    print(f'{DAYS} days, {USERS} users per seed, seeds {SEEDS}; policies c in {C_GRID}, n in {N_GRID}; tie-break lowest n, then c')
    print('habit world constants: ' + ', '.join(f'{k}={v:g}' for k, v in HABIT.items()))
    print('negative world: ' + ', '.join(f'{k}={NEG[k]:g}' for k in NEG if NEG[k] != HABIT[k]))
    print('mechanisms and their support in the sweep: ' + (', '.join(f'{k}: {v}' for k, v in sorted(MECH.items())) or 'none filled'))
    print()
    H = run_world(HABIT, 'habit world', content=True); show(H)
    N = run_world(NEG, 'negative world (more use is simply better)', content=True); show(N)
    print()
    print('THE GATE')
    gz = all(abs(r['content']['EMPTY']) < 1e-9 and r['out']['EMPTY']['policy'][1] == 0.0 for r in (H, N))
    print(f"  G-ZERO (EMPTY): content {H['content']['EMPTY']:+.3e} (habit), {N['content']['EMPTY']:+.3e} (negative); "
          f"n chosen {H['out']['EMPTY']['policy'][1]:g}, {N['out']['EMPTY']['policy'][1]:g} -> {'holds' if gz else 'FAILS'}")
    dp = diff(H, 'EMPTY', 'ENG', 'W'); sp = step(H, 'W')
    gp = dp > sp
    print(f"  G-POS (habit world): EMPTY - ENG welfare {dp:+.4f} (step {sp:.4f}) -> {'holds' if gp else 'FAILS'} (weak: by construction, Amendment 1)")
    dn = diff(N, 'EMPTY', 'ENG', 'W'); sn = step(N, 'W')
    gn = not dn > sn
    print(f"  G-NEG (negative world): EMPTY - ENG welfare {dn:+.4f} (step {sn:.4f}) -> {'holds' if gn else 'FAILS (forced)'}")
    gate = gz and gp and gn
    print('  GATE ' + ('OPEN' if gate else 'CLOSED'))
    oz = abs(H['content']['OWN']) >= 1e-9 and H['out']['OWN']['policy'][1] > 0
    print(f"  P-OWN (prediction): OWN content {H['content']['OWN']:+.3e}, n chosen {H['out']['OWN']['policy'][1]:g} -> "
          f"{'as predicted (non-zero content, n > 0)' if oz else 'NOT as predicted'}")
    print()
    if not gate:
        print('A-ADD, A-OWN and A-B are not tested: the gate is closed (R12).')
        return
    print('A-ADD (EMPTY against TRUE: the empty pause added to the true map), habit world')
    daw, dau = diff(H, 'EMPTY', 'TRUE', 'W'), diff(H, 'EMPTY', 'TRUE', 'auto')
    sw, sa = step(H, 'W'), step(H, 'auto')
    print(f"  welfare EMPTY - TRUE {daw:+.4f} (step {sw:.4f}) -> EMPTY {lab(daw, sw)}; user-started share {dau:+.4f} "
          f"(step {sa:.4f}) -> EMPTY {lab(dau, sa)}")
    print('A-OWN (the empty pause without the true map: OWN against ENG), habit world')
    for key, name in (('W', 'welfare'), ('h', 'final habit'), ('M', 'minutes'), ('auto', 'user-started')):
        d = diff(H, 'OWN', 'ENG', key)
        print(f"  {name:13} OWN - ENG {d:+.4f} (step {step(H, key):.4f}) -> OWN {lab(d, step(H, key))}")
    gap = diff(H, 'EMPTY', 'ENG', 'W')
    print(f"  share of the ENG -> EMPTY welfare gap closed by OWN: {diff(H, 'OWN', 'ENG', 'W') / gap:.4f}; "
          f"by TRUE: {diff(H, 'TRUE', 'ENG', 'W') / gap:.4f}")
    print('A-B (the company countermeasure: ENG-B, engagement with a break reminder), habit world')
    print(f"  ENG-B - ENG welfare {diff(H, 'ENG-B', 'ENG', 'W'):+.4f}; share of the ENG -> EMPTY gap closed: "
          f"{diff(H, 'ENG-B', 'ENG', 'W') / gap:.4f}; CHRONO share: {diff(H, 'CHRONO', 'ENG', 'W') / gap:.4f}")
    print()
    print('SENSITIVITY (each habit-world constant x0.5 and x2, one at a time; A-ADD and the OWN/EMPTY choices)')
    cnt = {'wel': {'ahead': 0, 'within a step': 0, 'behind': 0}, 'aut': {'ahead': 0, 'within a step': 0, 'behind': 0}}
    own_n, empty_n0, cells = 0, 0, 0
    for k in SENS:
        for f in (0.5, 2.0):
            w = dict(HABIT, **{k: HABIT[k] * f})
            r = run_world(w, f'{k} x{f:g}')
            dw, du = diff(r, 'EMPTY', 'TRUE', 'W'), diff(r, 'EMPTY', 'TRUE', 'auto')
            lw, lu = lab(dw, step(r, 'W')), lab(du, step(r, 'auto'))
            cnt['wel'][lw] += 1; cnt['aut'][lu] += 1; cells += 1
            own_n += r['out']['OWN']['policy'][1] > 0; empty_n0 += r['out']['EMPTY']['policy'][1] == 0
            print(f"  {k:8} x{f:<4g} ENG {r['out']['ENG']['policy']} OWN {r['out']['OWN']['policy']} TRUE {r['out']['TRUE']['policy']} "
                  f"EMPTY {r['out']['EMPTY']['policy']}; EMPTY - TRUE welfare {dw:+.4f} ({lw}), user-started {du:+.4f} ({lu})", flush=True)
    print(f"  over {cells} cells: welfare EMPTY vs TRUE {cnt['wel']}; user-started {cnt['aut']}; OWN sends notifications in "
          f"{own_n}/{cells}; EMPTY sends none in {empty_n0}/{cells}")
    print()
    print("THE INVESTIGATOR'S EXPECTATIONS (DECLARATION §4, written before the model) against the printout")
    ex = [('1 G-ZERO holds by construction', gz),
          ('2 the gate opens', gate),
          ('3 A-ADD welfare: EMPTY does not beat TRUE', not daw > sw),
          ('4 A-ADD autonomy: EMPTY ahead of TRUE where TRUE notifies',
           (dau > sa) if H['out']['TRUE']['policy'][1] > 0 else True),
          ('5 A-OWN: OWN removes notifications but only partly closes the gap',
           H['out']['OWN']['policy'][1] == 0 and 0 < diff(H, 'OWN', 'ENG', 'W') / gap < 1),
          ('6 A-B: break reminders recover a small part of the gap (< 0.5)', diff(H, 'ENG-B', 'ENG', 'W') / gap < 0.5)]
    for t, ok in ex:
        print(f"  {t:66}: {'holds' if ok else 'MISSED'}")


if __name__ == '__main__':
    main()
