"""Could SEC, and the other recent successes, save compute and energy? (Compute_Savings/DECLARATION.md, prompt-log 196)

A re-analysis of pinned run records; no data opened, no training run. Run: python3 Compute_Savings/checks/compute_savings.py
Inputs: runs/scl3/results_*.jsonl (10 UNSEEN carriers, study SCL3) and runs/sec1/results_*.jsonl (12 SEEN carriers, SEC1).
Every arm of the SEC1/SCL3 learner makes the same gradient and Fisher passes (runs/scl3/frozen/sec1_score.py), so compute is
proportional to the number of configurations run (x 5 seeds x one run's cost); energy on one machine is proportional to it.
"""
import glob
import json
import math
import os
import statistics

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
FS = FE = 0.1  # the registered calibration windows (runs at other windows are SCL3/SEC1 sensitivity cells)


def load(pattern):
    data = {}
    for p in sorted(glob.glob(os.path.join(ROOT, pattern))):
        name, rows = None, []
        for line in open(p):
            if not line.startswith('{'):
                continue
            o = json.loads(line)
            if 'acc' in o:
                rows.append(o)
            elif 'dataset' in o:
                name = o['dataset']
        if name and rows:
            data[name] = rows
    return data


def arm(rows, mode, value=None):
    v = [r for r in rows if r['mode'] == mode and r.get('fs') == FS and r.get('fe') == FE and r.get('distort') is None
         and (value is None or abs(r['value'] - value) < 1e-6)]
    return [r['acc'] for r in sorted(v, key=lambda r: r['seed'])]


def step_of(tv):  # SCL3/SEC1: max(1, 2 * SE over seeds of the tuned raw-lambda arm)
    return max(1.0, 2 * statistics.stdev(tv) / math.sqrt(len(tv)))


def analyse(data, label):
    print('=' * 110)
    print(f'{label}: {len(data)} carriers')
    print('=' * 110)
    R = {}
    for name, rows in data.items():
        grid = sorted(set(round(r['value'], 6) for r in rows if r['mode'] == 'fixed' and r.get('fs') == FS
                          and r.get('fe') == FE and r.get('distort') is None))
        g = {w: arm(rows, 'fixed', w) for w in grid}
        tuned = max(g, key=lambda w: statistics.mean(g[w]))
        tv = g[tuned]
        R[name] = dict(grid=g, tuned=tuned, tv=tv, step=step_of(tv), G=len(grid),
                       sec=arm(rows, 'bayes_sec', 0.0), raw=arm(rows, 'bayes', 0.0), eq=arm(rows, 'eq', 1.0))
    names = list(R)
    # C3: the transferred default (leave one out), snapped in log distance to this carrier's grid
    for n in names:
        others = [R[m]['tuned'] for m in names if m != n]
        d = math.exp(statistics.mean(math.log(x) for x in others))
        snap = min(R[n]['grid'], key=lambda w: abs(math.log(w) - math.log(d)))
        R[n]['default'], R[n]['default_snap'] = d, snap
        R[n]['dflt'] = R[n]['grid'][snap]
    print('C1 the sweep and C2/C3 not behind the tuned lambda (mean over seeds 0-4; step = max(1, 2 SE of the tuned arm))')
    print(f"  {'carrier':22} {'G':>3} {'saved':>7} {'tuned':>9} {'step':>5} {'SEC-tuned':>10} {'raw-tuned':>10} {'rule-tuned':>11} "
          f"{'default':>9} {'dflt-tuned':>11}")
    nb = {k: {} for k in ('sec', 'raw', 'eq', 'dflt')}
    for n in names:
        r = R[n]
        tm = statistics.mean(r['tv'])
        diff = {k: statistics.mean(r[k]) - tm for k in ('sec', 'raw', 'eq', 'dflt')}
        for k in diff:
            nb[k][n] = diff[k] > -r['step']
        r['diff'] = diff
        print(f"  {n:22} {r['G']:3d} {1 - 1 / r['G']:7.4f} {r['tuned']:9g} {r['step']:5.2f} {diff['sec']:+10.4f} {diff['raw']:+10.4f} "
              f"{diff['eq']:+11.4f} {r['default_snap']:9g} {diff['dflt']:+11.4f}")
    N = len(names)
    counts = {k: sum(v.values()) for k, v in nb.items()}
    print(f"  not behind the tuned lambda: SEC {counts['sec']}/{N}, raw Bayes {counts['raw']}/{N}, the rule {counts['eq']}/{N}, "
          f"transferred default {counts['dflt']}/{N}")
    only_sec = [n for n in names if nb['sec'][n] and not nb['dflt'][n]]
    both = [n for n in names if nb['sec'][n] and nb['dflt'][n]]
    print(f"  C3 saving attributable to SEC (SEC not behind, default behind): {len(only_sec)}/{N} {only_sec}")
    print(f"     SEC and the default both not behind (the saving is a default's there): {len(both)}/{N} {both}")
    print()
    print('C4 policies: one configuration accepted without tuning, against the full sweep (compute = configurations x 5 seeds)')
    sweep = sum(R[n]['G'] for n in names)
    for k, lab in (('sec', 'SEC'), ('raw', 'raw Bayes'), ('eq', 'the rule Omega=1'), ('dflt', 'transferred default')):
        lost = {n: R[n]['diff'][k] for n in names if not nb[k][n]}
        ratio = N / sweep
        print(f"  {lab:20}: compute {N} configs against {sweep} ({ratio:.4f} of the sweep; saving {1 - ratio:.4f}); "
              f"accepted without losing a step on {counts[k]}/{N}; accuracy lost where behind: "
              + (', '.join(f'{n} {v:+.2f}' for n, v in lost.items()) if lost else 'none'))
    print()
    return R, counts, only_sec, sweep


def main():
    print('Compute_Savings: tuning compute saved by a tuning-free weight, from pinned run records (DECLARATION.md)')
    print('compute is proportional to configurations run: every arm makes the same gradient and Fisher passes per run')
    print()
    scl3 = load('runs/scl3/results_*.jsonl')
    R, counts, only_sec, sweep = analyse(scl3, 'SCL3 (UNSEEN OpenML-CC18 carriers; SCL3-3 is PASS-0)')
    pinned = {'sec': 9, 'raw': 4, 'eq': 7}
    ok = all(counts[k] == v for k, v in pinned.items())
    print(f"C2 check against the pinned SCL3-3 counts (SEC 9/10, raw Bayes 4/10, the rule 7/10): {'reproduced' if ok else 'NOT REPRODUCED'}")
    if not ok:
        print('the calculation does not reproduce the ledger: no saving is reported')
        return
    n = len(R)
    print(f"C5 energy: with equal passes per run, SEC used without tuning spends {n}/{sweep} = {n / sweep:.4f} of the tuning "
          f"sweep's compute and energy on these carriers, a saving of {1 - n / sweep:.4f}; it is accepted without losing a step "
          f"on {counts['sec']}/{n}; the saving attributable to SEC rather than to a transferred default holds on {len(only_sec)}/{n}")
    print('   this is a share of hyperparameter-sweep compute, not of training compute; no kWh figure (no per-run energy recorded)')
    print()
    sec1 = load('runs/sec1/results_*.jsonl')
    analyse(sec1, 'SEC1 (SEEN carriers of EQ3/EQ4; confirmatory, rung R5; context only)')
    print('C6 the empty cut: rework avoided (standard checkpointing arithmetic; the CRR content is the state checklist)')
    for T in (10,):
        per = 1 / (2 * T)
        for k in (1, 5, 20):
            print(f"  T = {T} tasks, checkpoint only at task boundaries, {k:2d} interruption(s) per run at uniformly random updates: "
                  f"expected rework {k * per:.2f} of a run; with a lossless mid-task cut: 0")


if __name__ == '__main__':
    main()
