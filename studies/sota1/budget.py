"""SOTA1 compute budget, printed before the hash from measured unit timings (a planning estimate, not a result).

Inputs, all measured on this machine and committed:
- the Phase A gate units (`CL Design Principle/checks/gate_runs/*.json`): W+ has 200 training images per class, so a full
  10-task unit sees 20,000 images; CIFAR-100 has 50,000, so a CIFAR-100 unit is scaled by 50000 / 20000 = 2.5;
- arms absent from the gate are costed relative to ER from the one-task timings in `prereg/sota1/timing/` (four threads,
  one unit at a time, the same synthetic stream for both).
Units run two at a time with two threads each, so wall time = total unit time / 2.
"""
import glob
import json
import os
import statistics
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'studies', 'sota1'))
import sota1_run as R  # noqa: E402

GATE = os.path.join(ROOT, 'CL Design Principle', 'checks', 'gate_runs')
TIMING = os.path.join(ROOT, 'prereg', 'sota1', 'timing')
SCALE = 50000 / 20000


def gate_seconds(arm):
    v = [json.load(open(f))['seconds'] for f in glob.glob(os.path.join(GATE, f'Wplus__{arm}__s*.json')) if '__s0__' not in f and f.count('__') == 2]
    return statistics.mean(v) if v else None


def main():
    base = {}
    for a in ('sgd', 'er', 'er_ace', 'derpp', 'crr', 'crr-ace', 'crr-cos', 'crr-a8', 'crr-alpha', 'crr-beta', 'crr-kd',
              'crr-kdfixed', 'crr-stepclock', 'crr-predfast', 'crr-predslow'):
        s = gate_seconds(a)
        if s is not None:
            base[a] = s * SCALE
    t = {os.path.basename(f)[:-5]: json.load(open(f))['seconds'] for f in glob.glob(os.path.join(TIMING, '*.json'))}
    for a in ('xder', 'agem', 'lwf', 'ewc_on', 'icarl'):
        if a in t and 'er' in t and 'er' in base:
            base[a] = base['er'] * t[a] / t['er']
    for a in R.ARMS:
        if '@' in a:
            base[a] = base.get('crr')
    print('Estimated seconds per full CIFAR-100 unit (two threads, two units at a time):')
    for a, s in sorted(base.items()):
        print(f'  {a:16} {s:8.0f}' if s else f'  {a:16} unknown')
    total = 0.0
    for tier in R.ORDER:
        sec = 0.0
        for a, s, pause, lr in R.TIERS[tier]:
            u = base.get(a)
            if u is None:
                continue
            sec += u * (0.3 if pause is not None else 1.0)
        total += sec
        print(f'tier {tier}: {len(R.TIERS[tier]):3d} units, {sec / 3600:6.2f} unit-hours')
    print(f'total {total / 3600:.2f} unit-hours; wall time with two units at a time {total / 7200:.2f} hours')


if __name__ == '__main__':
    main()
