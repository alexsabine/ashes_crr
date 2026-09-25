"""SOTA1 Phase A (R4): the gate, the synthetic comparative battery and the synthetic construction checks.

Declared in `CL Design Principle/DECLARATION_2.md` (pushed before any unit ran). No benchmark data: the worlds come from
`synth_worlds.py`. Every unit is one run of `studies/sota1/vendor/mammoth/sota1_harness.py` (Mammoth's own train() loop
and model classes). Unit records are written to `gate_runs/<world>__<arm>__s<seed>[__<pause>].json`.
  python gate_sota1.py run        # runs the missing units (resumable), two at a time, two threads each
  python gate_sota1.py summary    # prints the declared labels from the unit records (pinned as gate_sota1.txt)
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
MAMMOTH = os.path.join(ROOT, 'studies', 'sota1', 'vendor', 'mammoth')
PY = os.path.join(ROOT, 'studies', 'sota1', 'env', '.venv', 'bin', 'python')
RUNS = os.path.join(HERE, 'gate_runs')
SCRATCH = os.environ.get('SOTA1_SCRATCH', os.path.join(ROOT, 'data', 'raw', 'sota1_synth'))

COMMON = ['--dataset', 'seq-cifar100-local', '--backbone', 'reduced-resnet18', '--n_epochs', '1', '--batch_size', '10',
          '--num_workers', '0', '--non_verbose', '1', '--lr', '0.1']
REHEARSAL = ['--buffer_size', '500', '--minibatch_size', '10']  # every arm except sgd
ARMS = {
    'sgd': ['--model', 'sgd'],
    'er': ['--model', 'er'],
    'er_ace': ['--model', 'er_ace'],
    'derpp': ['--model', 'derpp', '--alpha', '0.3', '--beta', '0.5'],
    'crr': ['--model', 'crr_scl'],
    'crr-ace': ['--model', 'crr_scl', '--crr_ace', '0'],
    'crr-cos': ['--model', 'crr_scl', '--crr_cos', '0'],
    'crr-a8': ['--model', 'crr_scl', '--crr_a8', '0'],
    'crr-alpha': ['--model', 'crr_scl', '--alpha', '0'],
    'crr-beta': ['--model', 'crr_scl', '--beta', '0'],
    'crr-kd': ['--model', 'crr_scl', '--crr_kd', 'off'],
    'crr-kdfixed': ['--model', 'crr_scl', '--crr_kd', 'fixed'],
    'crr-stepclock': ['--model', 'crr_scl', '--crr_clock', 'step'],
    'crr-predfast': ['--model', 'crr_scl', '--crr_pred', 'fast'],
    'crr-predslow': ['--model', 'crr_scl', '--crr_pred', 'slow'],
}
ABLATIONS = [a for a in ARMS if a.startswith('crr-')]
UNITS = [('W+', a, s, None) for a in ARMS for s in (0, 1)]
UNITS += [('W0', a, 0, None) for a in ('sgd', 'er', 'er_ace', 'derpp', 'crr')]
PAUSES = ['none', 'lossless'] + [f'drop:{p}' for p in ('net', 'opt', 'buffer', 'rng', 'counters', 'crr_ema',
                                                        'crr_clock', 'crr_eq', 'crr_seen')] + ['world:20', 'wall:30']
UNITS += [('W+', 'crr', 0, p) for p in PAUSES]
MUST_CHANGE = ['net', 'buffer', 'rng', 'crr_ema', 'crr_clock', 'crr_eq', 'crr_seen']
REPORT_ONLY = ['opt', 'counters']


def unit_path(w, a, s, p):
    tag = '' if p is None else '__' + p.replace(':', '-')
    return os.path.join(RUNS, f"{w.replace('+', 'plus')}__{a}__s{s}{tag}.json")


def world_npz(w):
    os.makedirs(SCRATCH, exist_ok=True)
    path = os.path.join(SCRATCH, f"{w.replace('+', 'plus')}.npz")
    if not os.path.exists(path):
        subprocess.run([PY, os.path.join(HERE, 'synth_worlds.py'), w, path], check=True)
    return path


def run_unit(u):
    w, a, s, p = u
    out = unit_path(w, a, s, p)
    if os.path.exists(out):
        return out
    args = [PY, 'sota1_harness.py', '--threads', '2', '--out', out + '.tmp'] + COMMON + ['--seed', str(s)] + ARMS[a]
    if a != 'sgd':
        args += REHEARSAL
    if p is not None:
        args += ['--stop_after', '3', '--pause_at', '150,350,550', '--pause_mode', p]
    env = dict(os.environ, CRR_CIFAR100_NPZ=world_npz(w), OMP_NUM_THREADS='2')
    log = out + '.log'
    with open(log, 'w') as f:
        r = subprocess.run(args, cwd=MAMMOTH, env=env, stdout=f, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        return f'FAILED {out} (see {log})'
    os.replace(out + '.tmp', out)
    os.remove(log)
    return out


def load(w, a, s, p=None):
    path = unit_path(w, a, s, p)
    return json.load(open(path)) if os.path.exists(path) else None


def lab(d, seeds_d):
    """AHEAD / BEHIND need a mean paired difference of at least one point AND the same sign in every seed."""
    if d >= 1.0 and all(x > 0 for x in seeds_d):
        return 'AHEAD'
    if d <= -1.0 and all(x < 0 for x in seeds_d):
        return 'BEHIND'
    return 'TIE'


def compare(w, a, b, seeds):
    da = [load(w, a, s) for s in seeds]
    db = [load(w, b, s) for s in seeds]
    if any(x is None for x in da + db):
        return None
    diffs = [x['final_class_il'] - y['final_class_il'] for x, y in zip(da, db)]
    d = sum(diffs) / len(diffs)
    return d, diffs, lab(d, diffs)


def summary():
    print('SOTA1 Phase A: gate, synthetic comparative battery and construction checks (DECLARATION_2.md)')
    print('metric: final class-incremental accuracy (mean over the 10 tasks after the last task), reduced ResNet-18, M = 500')
    print('label: AHEAD/BEHIND if the mean paired difference is >= 1.0 point in size and has the same sign in every seed')
    print()
    print('Unit results (final class-IL / task-IL, seconds):')
    for w, a, s, p in UNITS:
        r = load(w, a, s, p)
        tag = '' if p is None else f' [{p}]'
        if r is None:
            print(f'  {w:3} {a:14} s{s}{tag}: MISSING')
        else:
            print(f"  {w:3} {a:14} s{s}{tag}: {r['final_class_il']:7.2f} / {r['final_task_il']:7.2f}  ({r['seconds']:.0f} s)  params {r['param_sha256'][:12]}")
    print()
    g0 = compare('W+', 'er', 'sgd', (0, 1))
    print('G0 instrument (W+): ER against SGD must read AHEAD:', 'not decidable' if g0 is None else f"{g0[0]:+.2f} {g0[2]}")
    g0_ok = g0 is not None and g0[2] == 'AHEAD'
    g1 = []
    for a in ('er_ace', 'derpp', 'crr'):
        c = compare('W0', a, 'er', (0,))
        g1.append((a, c))
        print(f'G1 negative control (W0): {a} against ER must not read AHEAD:', 'not decidable' if c is None else f'{c[0]:+.2f} {c[2]}')
    g1_ok = all(c is not None and c[2] != 'AHEAD' for _, c in g1)
    print('GATE:', 'OPEN' if g0_ok and g1_ok else 'CLOSED', f'(G0 {"holds" if g0_ok else "fails"}, G1 {"holds" if g1_ok else "violated"})')
    print()
    print('G2 synthetic comparative (W+, seeds 0 and 1): CRR-SCL against each baseline (report)')
    for b in ('sgd', 'er', 'er_ace', 'derpp'):
        c = compare('W+', 'crr', b, (0, 1))
        print(f'  crr vs {b:7}:', 'not decidable' if c is None else f'{c[0]:+.2f}  per seed {[round(x, 2) for x in c[1]]}  {c[2]}')
    print()
    print('G3 synthetic ablations (W+, seeds 0 and 1): full CRR-SCL against each leave-one-out arm (report;')
    print('   AHEAD means the removed component helped, as CRR predicts)')
    for a in ABLATIONS:
        c = compare('W+', 'crr', a, (0, 1))
        print(f'  crr vs {a:14}:', 'not decidable' if c is None else f'{c[0]:+.2f}  per seed {[round(x, 2) for x in c[1]]}  {c[2]}')
    print()
    print('C-S construction checks (W+, seed 0, 3 tasks, pauses after updates 150, 350, 550)')
    base = load('W+', 'crr', 0, 'none')
    if base is None:
        print('  not decidable (no unpaused unit)')
        return
    ll = load('W+', 'crr', 0, 'lossless')
    ok1 = ll is not None and ll['param_sha256'] == base['param_sha256'] and ll['acc_class_matrix'] == base['acc_class_matrix']
    print('  C-S1 lossless pause bitwise identical to no pause:', 'holds' if ok1 else 'FAILS')
    ch = []
    for part in MUST_CHANGE + REPORT_ONLY:
        r = load('W+', 'crr', 0, f'drop:{part}')
        if r is None:
            print(f'  drop {part:10}: MISSING')
            continue
        changed = r['param_sha256'] != base['param_sha256']
        if part in MUST_CHANGE:
            ch.append(changed)
        print(f"  drop {part:10}: {'changes the run' if changed else 'inert'}; final class-IL {r['final_class_il']:.2f} "
              f"(difference {r['final_class_il'] - base['final_class_il']:+.2f}){'  [report only]' if part in REPORT_ONLY else ''}")
    print('  C-S2 every declared part changes the run when dropped:', 'holds' if ch and all(ch) and len(ch) == len(MUST_CHANGE) else 'FAILS')
    wd = load('W+', 'crr', 0, 'world:20')
    if wd is not None:
        stake = base['final_class_il'] - wd['final_class_il']
        print(f"  C-S3 the world moves (20 batches expire per pause): stake {stake:+.2f}; must be non-zero:",
              'holds' if wd['param_sha256'] != base['param_sha256'] else 'FAILS')
    wl = load('W+', 'crr', 0, 'wall:30')
    if wl is not None:
        print(f"  C-S4 valued at a wall-clock deadline (30 updates lost per pause): stake {base['final_class_il'] - wl['final_class_il']:+.2f} (report)")
    print('  C-S0 the own-step valuation: stake 0 exactly when C-S1 holds (Proposition 7)')


def main():
    if sys.argv[1] == 'run':
        os.makedirs(RUNS, exist_ok=True)
        with ThreadPoolExecutor(max_workers=2) as ex:
            for r in ex.map(run_unit, UNITS):
                print(r, flush=True)
    else:
        summary()


if __name__ == '__main__':
    main()
