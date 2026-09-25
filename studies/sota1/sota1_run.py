"""SOTA1 runner: every unit of the pre-registered design, resumable, two units at a time with two threads each.

Frozen at hash time into runs/sota1/frozen/ together with the vendored Mammoth; the run uses the frozen copies:
    python runs/sota1/frozen/sota1_run.py run [tier ...]    # missing units only, in the declared priority order
    python runs/sota1/frozen/sota1_run.py list              # the units and the count per tier
Each unit is one call of the frozen `mammoth/sota1_harness.py` (Mammoth's own train() and model classes) on
data/raw/cifar100/cifar100.npz; its record goes to runs/sota1/units/<arm>__s<seed>[__<pause>].json.
"""
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

FROZEN = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(FROZEN, '..', '..', '..'))
MAMMOTH = os.path.join(FROZEN, 'mammoth')
PY = os.path.join(ROOT, 'studies', 'sota1', 'env', '.venv', 'bin', 'python')
UNITS_DIR = os.path.join(ROOT, 'runs', 'sota1', 'units')
NPZ = os.path.join(ROOT, 'data', 'raw', 'cifar100', 'cifar100.npz')
THREADS = 2
WORKERS = 2

COMMON = ['--dataset', 'seq-cifar100-local', '--backbone', 'reduced-resnet18', '--n_epochs', '1', '--batch_size', '10',
          '--num_workers', '0', '--non_verbose', '1']
REHEARSAL = ['--buffer_size', '2000', '--minibatch_size', '10']
LR = ['--lr', '0.1']
ARMS = {
    # SOTA baselines (Mammoth reference implementations)
    'sgd': ['--model', 'sgd'],
    'er': ['--model', 'er'],
    'er_ace': ['--model', 'er_ace'],
    'derpp': ['--model', 'derpp', '--alpha', '0.3', '--beta', '0.5'],
    'xder': ['--model', 'xder', '--alpha', '0.3', '--beta', '0.8'],
    # context baselines
    'agem': ['--model', 'agem'],
    'lwf': ['--model', 'lwf'],
    'ewc_on': ['--model', 'ewc_on', '--e_lambda', '10', '--gamma', '1'],
    'icarl': ['--model', 'icarl'],
    # the CRR safe continual learner and its leave-one-out ablations
    'crr': ['--model', 'crr_scl'],
    'crr-ace': ['--model', 'crr_scl', '--crr_ace', '0'],
    'crr-cos': ['--model', 'crr_scl', '--crr_cos', '0'],
    'crr-a8': ['--model', 'crr_scl', '--crr_a8', '0'],
    'crr-alpha': ['--model', 'crr_scl', '--alpha', '0'],
    'crr-beta': ['--model', 'crr_scl', '--beta', '0'],
    'crr-kd': ['--model', 'crr_scl', '--crr_kd', 'off'],
    'crr-kdfixed': ['--model', 'crr_scl', '--crr_kd', 'fixed'],
    'crr-stepclock': ['--model', 'crr_scl', '--crr_clock', 'step'],
    # the prediction-rule ablations (fast head, slow head) are read inside every `crr` unit (alt_pred): the training is
    # identical, so a separate unit would repeat it (Phase A: identical parameter hashes)
    # sensitivity cells (named constants swept)
    'crr@q0.98': ['--model', 'crr_scl', '--crr_ema_q', '0.98'],
    'crr@q0.995': ['--model', 'crr_scl', '--crr_ema_q', '0.995'],
    'crr@cap100': ['--model', 'crr_scl', '--crr_eq_cap', '100'],
    'crr@gamma1': ['--model', 'crr_scl', '--crr_gamma', '1.0'],
    'crr@smooth0.5': ['--model', 'crr_scl', '--crr_eq_smooth', '0.5'],
}
LR_CELL = ['crr', 'er', 'er_ace', 'derpp', 'xder']  # the learning-rate cell: these arms at lr 0.05
PAUSE = ['--stop_after', '3', '--pause_at', '250,700,1200']  # 3 tasks = 1500 updates
PAUSE_MODES = ['none', 'lossless'] + [f'drop:{p}' for p in ('net', 'opt', 'buffer', 'rng', 'counters', 'crr_ema',
                                                             'crr_clock', 'crr_eq', 'crr_seen')] + ['world:20', 'wall:30']

TIERS = {
    'A': [(a, s, None, None) for s in range(5) for a in ('crr', 'er', 'er_ace', 'derpp', 'xder', 'sgd')],
    'C': [(a, s, None, None) for s in range(3) for a in ARMS if a.startswith('crr-')],
    'S': [('crr', s, m, None) for s in range(3) for m in ('none', 'lossless')]
         + [('derpp', s, m, None) for s in range(3) for m in ('none', 'lossless')]
         + [('crr', 0, m, None) for m in PAUSE_MODES[2:]],
    'B': [(a, s, None, None) for s in range(3) for a in ('agem', 'lwf', 'ewc_on', 'icarl')],
    'D': [(a, s, None, None) for s in range(2) for a in ARMS if '@' in a]
         + [(a, s, None, '0.05') for s in range(2) for a in LR_CELL],
    'R': [('crr', 0, None, 'rerun')],
}
ORDER = ['A', 'C', 'S', 'B', 'D', 'R']


def unit_name(a, s, pause, lr):
    tag = '' if pause is None else '__' + pause.replace(':', '-')
    if lr == 'rerun':
        tag += '__rerun'
    elif lr is not None:
        tag += f'__lr{lr}'
    return f'{a}__s{s}{tag}'


def run_unit(u):
    a, s, pause, lr = u
    out = os.path.join(UNITS_DIR, unit_name(*u) + '.json')
    if os.path.exists(out):
        return f'exists {out}'
    lr_args = ['--lr', lr] if lr not in (None, 'rerun') else LR
    args = [PY, 'sota1_harness.py', '--threads', str(THREADS), '--out', out + '.tmp'] + COMMON + lr_args
    args += ['--seed', str(s)] + ARMS[a] + ([] if a == 'sgd' else REHEARSAL)
    if pause is not None:
        args += PAUSE + ['--pause_mode', pause]
    env = dict(os.environ, CRR_CIFAR100_NPZ=NPZ, OMP_NUM_THREADS=str(THREADS))
    log = out + '.log'
    with open(log, 'w') as f:
        r = subprocess.run(args, cwd=MAMMOTH, env=env, stdout=f, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        return f'FAILED {out} (log kept)'
    os.replace(out + '.tmp', out)
    os.remove(log)
    return f'done {out}'


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'list'
    tiers = sys.argv[2:] or ORDER
    if cmd == 'list':
        for t in ORDER:
            print(t, len(TIERS[t]), [unit_name(*u) for u in TIERS[t]][:3], '...')
        print('total units', sum(len(TIERS[t]) for t in ORDER))
        return
    os.makedirs(UNITS_DIR, exist_ok=True)
    assert os.path.exists(NPZ), 'run data/fetch_cifar100.py first (after the hash, not before 2026-09-26 00:00 UTC)'
    units = [u for t in tiers for u in TIERS[t]]
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for r in ex.map(run_unit, units):
            print(r, flush=True)


if __name__ == '__main__':
    main()
