"""SOTA1 scorer: every pre-registered row, computed from the unit records (R15). Frozen at hash time (prereg/sota1/).

    python prereg/sota1/sota1_score.py > runs/sota1/score.txt     (also writes runs/sota1/results.json)

Rules (PREREG.md):
- Metric: final class-incremental accuracy (mean over the 10 tasks after the last task); task-incremental reported.
- A paired comparison X vs Y over seeds: d = mean of per-seed differences; step = max(1.0, 2 * SE(d)).
  AHEAD if d >= step and X > Y in all but at most one seed (5 seeds) or in every seed (2 or 3 seeds);
  BEHIND symmetrically; TIE otherwise.
- A missing unit makes every comparison that needs it NOT DECIDABLE. No unit is rerun with any change.
"""
import json
import math
import os
import statistics
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
UNITS = os.environ.get('SOTA1_UNITS', os.path.join(ROOT, 'runs', 'sota1', 'units'))
GATE_TXT = os.path.join(ROOT, 'prereg', 'sota1', 'gate_sota1.txt')
SOTA = ['er', 'er_ace', 'derpp', 'xder']
COMPONENTS = [('crr-ace', 'A3: asymmetric incoming loss'), ('crr-cos', 'H-EQ at the head: cosine classifier'),
              ('crr-a8', 'A8: past-logit mask and X-DER fill'), ('crr-alpha', 'A6: logit replay'),
              ('crr-beta', 'A6/A8: label replay'), ('crr-kd', 'A6: pull toward the slow model'),
              ('crr-stepclock', "D2/A1': the slow model on the model's own clock"),
              ('crr-predfast', 'A6: slow model + nearest class mean against the fast head'),
              ('crr-predslow', 'A6: nearest class mean against the slow head')]
SENS = ['crr@q0.98', 'crr@q0.995', 'crr@cap100', 'crr@gamma1', 'crr@smooth0.5']


def load(name):
    p = os.path.join(UNITS, name + '.json')
    return json.load(open(p)) if os.path.exists(p) else None


def acc(arm, s, suffix=''):
    r = load(f'{arm}__s{s}{suffix}')
    return None if r is None else r['final_class_il']


def compare(x, y, seeds, sx='', sy=''):
    ax = [acc(x, s, sx) for s in seeds]
    ay = [acc(y, s, sy) for s in seeds]
    if any(v is None for v in ax + ay):
        return None
    diffs = [a - b for a, b in zip(ax, ay)]
    d = statistics.mean(diffs)
    se = statistics.stdev(diffs) / math.sqrt(len(diffs)) if len(diffs) > 1 else 0.0
    step = max(1.0, 2 * se)
    need = len(diffs) - 1 if len(diffs) >= 5 else len(diffs)
    pos, neg = sum(v > 0 for v in diffs), sum(v < 0 for v in diffs)
    lab = 'AHEAD' if d >= step and pos >= need else ('BEHIND' if d <= -step and neg >= need else 'TIE')
    return {'d': d, 'step': step, 'diffs': diffs, 'label': lab, 'x': ax, 'y': ay}


def fmt(c):
    if c is None:
        return 'NOT DECIDABLE (unit missing)'
    return (f"d = {c['d']:+.4f} ({c['d']:+.2f}), step {c['step']:.2f}, per seed "
            f"{[round(v, 2) for v in c['diffs']]} -> {c['label']}")


def main():
    rows = []
    print('SOTA1 score (prereg/sota1/PREREG.md); online Split-CIFAR-100, reduced ResNet-18, M = 2000, lr 0.1')
    gate_open = os.path.exists(GATE_TXT) and 'GATE: OPEN' in open(GATE_TXT).read()
    print('Phase A gate (prereg/sota1/gate_sota1.txt):', 'OPEN' if gate_open else 'CLOSED or missing')
    print()
    print('Per-arm final class-incremental accuracy by seed (task-incremental in brackets):')
    arms = ['sgd', 'er', 'er_ace', 'derpp', 'xder', 'agem', 'lwf', 'ewc_on', 'icarl', 'crr'] + [c for c, _ in COMPONENTS] + SENS
    for a in arms:
        vals = []
        for s in range(5):
            r = load(f'{a}__s{s}')
            if r is not None:
                vals.append(f"s{s} {r['final_class_il']:.2f} [{r['final_task_il']:.2f}]")
        if vals:
            m = statistics.mean([load(f'{a}__s{s}')['final_class_il'] for s in range(5) if load(f'{a}__s{s}')])
            print(f'  {a:16} mean {m:6.2f} | ' + '; '.join(vals))
    print()
    # S1-1: the CRR safe continual learner against the best state-of-the-art baseline (a design comparison)
    means = {}
    for b in SOTA:
        v = [acc(b, s) for s in range(5)]
        means[b] = None if any(x is None for x in v) else statistics.mean(v)
    avail = {b: m for b, m in means.items() if m is not None}
    best = max(avail, key=avail.get) if len(avail) == len(SOTA) else None
    print('Best state-of-the-art baseline by mean over seeds 0-4:', best,
          {b: (None if m is None else round(m, 2)) for b, m in means.items()})
    c11 = compare('crr', best, range(5)) if best else None
    v_sup = None if c11 is None else ('PASS' if c11['label'] == 'AHEAD' else 'FAIL')
    v_non = None if c11 is None else ('PASS' if c11['label'] != 'BEHIND' else 'FAIL')
    print('S1-1a (superiority) CRR-SCL AHEAD of the best baseline:', fmt(c11), '->', v_sup or 'NOT DECIDABLE')
    print('S1-1b (non-inferiority) CRR-SCL not BEHIND the best baseline:', '->', v_non or 'NOT DECIDABLE')
    rows += [{'id': 'SOTA1-1a', 'verdict': v_sup, 'cmp': c11, 'best': best},
             {'id': 'SOTA1-1b', 'verdict': v_non, 'cmp': c11, 'best': best}]
    for b in SOTA + ['sgd']:
        print(f'  CRR-SCL vs {b:7}:', fmt(compare('crr', b, range(5))))
    print()
    # S1-2: equanimity as the weight of the regeneration pull (H-EQ, Omega = 1) against MKD's published constant
    c12 = compare('crr', 'crr-kdfixed', range(3))
    if c12 is None:
        v12 = None
    else:
        v12 = {'AHEAD': 'PASS', 'TIE': 'REDUCES (Omega = 1 equivalent to the fixed constant)', 'BEHIND': 'FAIL'}[c12['label']]
    print('S1-2 H-EQ (Omega = 1) weight AHEAD of MKD lambda = 5.5:', fmt(c12), '->',
          (v12 if gate_open else f'report only (gate closed): {v12}') if v12 else 'NOT DECIDABLE')
    rows.append({'id': 'SOTA1-2', 'verdict': v12 if gate_open else None, 'cmp': c12})
    print()
    # S1-3: CRR's reading of each integrated component predicts that removing it lowers accuracy (full AHEAD of ablation)
    print("S1-3 components (CRR predicts: full CRR-SCL AHEAD of the leave-one-out arm; seeds 0-2):")
    n_pass = 0
    for arm, what in COMPONENTS:
        c = compare('crr', arm, range(3))
        v = None if c is None else ('PASS' if c['label'] == 'AHEAD' else 'FAIL')
        n_pass += v == 'PASS'
        print(f'  S1-3 {arm:14} [{what}]:', fmt(c), '->', (v if gate_open else f'report only: {v}') if v else 'NOT DECIDABLE')
        rows.append({'id': f'SOTA1-3:{arm}', 'verdict': v if gate_open else None, 'cmp': c})
    print(f'  components passing: {n_pass} of {len(COMPONENTS)}')
    print()
    # Retrodiction rechecks on the benchmark (report only): the published mechanisms read again on unseen data
    print('Rechecks of graded mechanisms on this benchmark (report only; seeds 0-2):')
    for x, y, what in (('er', 'sgd', 'M1 replay'), ('er', 'agem', 'M13 ER against A-GEM'), ('er', 'lwf', 'M8 replay against LwF'),
                       ('ewc_on', 'sgd', 'M12 parameter anchor against fine-tuning'), ('er_ace', 'er', 'M7 asymmetric loss'),
                       ('derpp', 'er', 'M4/M5 logit + label replay'), ('xder', 'derpp', 'M6 X-DER over DER++')):
        print(f'  {what:44}: {x} vs {y}:', fmt(compare(x, y, range(3))))
    print()
    # Sensitivity (R5): S1-1 recomputed in each cell, seeds 0-1
    print('Sensitivity of S1-1 (seeds 0-1): each cell recomputes CRR-SCL against the best baseline')
    base = compare('crr', best, range(2)) if best else None
    print('  default cell         :', fmt(base))
    flips = 0
    cells = []
    for a in SENS:
        c = compare(a, best, range(2)) if best else None
        cells.append((a, c))
    lr_means = {b: [acc(b, s, '__lr0.05') for s in range(2)] for b in SOTA}
    lr_best = None
    if all(None not in v for v in lr_means.values()):
        lr_best = max(lr_means, key=lambda b: statistics.mean(lr_means[b]))
    cells.append(('lr 0.05', compare('crr', lr_best, range(2), '__lr0.05', '__lr0.05') if lr_best else None))
    for name, c in cells:
        flip = None if (c is None or base is None) else (c['label'] != base['label'])
        flips += bool(flip)
        print(f'  {name:20} :', fmt(c), '' if flip is None else ('FLIP' if flip else 'same label'))
    fragile = flips > 1
    print(f'  flips: {flips} of {len(cells)} cells ->', 'FRAGILE' if fragile else 'not fragile')
    rows.append({'id': 'SOTA1-S', 'verdict': 'FRAGILE' if fragile else 'not fragile', 'flips': flips})
    print()
    # Construction rows (the empty cut on the benchmark learner; checks of the construction, not evidence)
    print('Construction (3 tasks, pauses after updates 250, 700, 1200):')
    for arm in ('crr', 'derpp'):
        for s in range(3):
            a, b = load(f'{arm}__s{s}__none'), load(f'{arm}__s{s}__lossless')
            ok = None if (a is None or b is None) else (a['param_sha256'] == b['param_sha256'] and a['acc_class_matrix'] == b['acc_class_matrix'])
            print(f'  SOTA1-C1 {arm} s{s} lossless pause bitwise identical:', 'NOT DECIDABLE' if ok is None else ('holds' if ok else 'FAILS'))
            rows.append({'id': f'SOTA1-C1:{arm}:s{s}', 'verdict': None if ok is None else ('holds' if ok else 'FAILS')})
    base0 = load('crr__s0__none')
    must = ['net', 'buffer', 'rng', 'crr_ema', 'crr_clock', 'crr_eq', 'crr_seen']
    changed = []
    for part in must + ['opt', 'counters']:
        r = load(f'crr__s0__drop-{part}')
        if r is None or base0 is None:
            print(f'  drop {part:10}: NOT DECIDABLE')
            continue
        ch = r['param_sha256'] != base0['param_sha256']
        if part in must:
            changed.append(ch)
        print(f"  drop {part:10}: {'changes the run' if ch else 'inert'} (final class-IL {r['final_class_il']:.2f}, "
              f"difference {r['final_class_il'] - base0['final_class_il']:+.2f}){' [report only]' if part not in must else ''}")
    v2 = None if len(changed) < len(must) else ('holds' if all(changed) else 'FAILS')
    print('  SOTA1-C2 every declared part changes the run when dropped:', v2 or 'NOT DECIDABLE')
    rows.append({'id': 'SOTA1-C2', 'verdict': v2})
    w = load('crr__s0__world-20')
    v3 = None if (w is None or base0 is None) else ('holds' if w['param_sha256'] != base0['param_sha256'] else 'FAILS')
    if v3:
        print(f"  SOTA1-C3 the world moves during the pause (must change the run): stake {base0['final_class_il'] - w['final_class_il']:+.2f} -> {v3}")
    rows.append({'id': 'SOTA1-C3', 'verdict': v3})
    wl = load('crr__s0__wall-30')
    if wl is not None and base0 is not None:
        print(f"  SOTA1-C4 stake of a wall-clock valuation (30 updates lost per pause): {base0['final_class_il'] - wl['final_class_il']:+.2f} (report)")
    print()
    # R9: the rerun of one unit
    a, b = load('crr__s0'), load('crr__s0__rerun')
    r9 = None if (a is None or b is None) else (a['param_sha256'] == b['param_sha256'] and a['acc_class_matrix'] == b['acc_class_matrix'])
    print('R9 rerun of crr seed 0 bitwise identical:', 'NOT DECIDABLE' if r9 is None else ('holds' if r9 else 'FAILS'))
    json.dump({'rows': rows, 'gate_open': gate_open, 'rerun_identical': r9}, open(os.environ.get('SOTA1_RESULTS', os.path.join(ROOT, 'runs', 'sota1', 'results.json')), 'w'), indent=1, default=str)


if __name__ == '__main__':
    sys.exit(main())
