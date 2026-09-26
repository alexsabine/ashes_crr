"""SOTA1 ledger rows, printed from the frozen scorer's results.json and the unit records (R1, R15).

The verdicts are the scorer's (prereg/sota1/sota1_score.py, frozen); this script only formats them into the ledger's
columns and adds the PASS level and the per-unit distributions. Run after the scorer:
    python3 runs/sota1/ledger_rows.py > runs/sota1/ledger_rows.txt
"""
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
RES = json.load(open(os.path.join(ROOT, 'runs', 'sota1', 'results.json')))
UNITS = os.path.join(ROOT, 'runs', 'sota1', 'units')

ANCHOR = ('4986bbee (anchor: OpenTimestamps complete, Bitcoin blocks 968549/968554/968555/968581, earliest '
          '2026-09-25T13:06:00Z, runs/sota1/ots_upgrade.txt; prereg commit de95c63, 2026-09-25T11:51:16Z; every hashed '
          'file unchanged after the run, runs/sota1/hash_check.txt; data fetched 2026-09-26T00:07:26Z)')
DATA = ('CIFAR-100 (Krizhevsky 2009) as online Split-CIFAR-100, 10 tasks of 10 classes, natural order; reduced '
        'ResNet-18, M = 2000, lr 0.1, one epoch, batch 10 (Y)')
SCRIPT = 'prereg/sota1/sota1_score.py (frozen); runs/sota1/ledger_rows.py'
LOG = 'runs/sota1/score.txt; runs/sota1/results.json; runs/sota1/units/'
WHAT = {
    'SOTA1-1a': ('CRR-SCL AHEAD of the best of {ER, ER-ACE, DER++, X-DER} (highest mean over seeds 0-4)', 'AHEAD over seeds 0-4'),
    'SOTA1-1b': ('CRR-SCL not BEHIND that best baseline', 'not BEHIND'),
    'SOTA1-2': ('H-EQ (Omega = 1) as the KD weight AHEAD of MKD\'s published lambda = 5.5 (crr-kdfixed)',
                'AHEAD = PASS; TIE = REDUCES; BEHIND = FAIL'),
    'SOTA1-3:crr-ace': ('A3 reading: full CRR-SCL AHEAD of the arm without the asymmetric incoming loss', 'AHEAD over seeds 0-2'),
    'SOTA1-3:crr-cos': ('H-EQ at the head: full AHEAD of the arm without the cosine classifier', 'AHEAD over seeds 0-2'),
    'SOTA1-3:crr-a8': ('A8 reading: full AHEAD of the arm without the past-logit mask and X-DER fill', 'AHEAD over seeds 0-2'),
    'SOTA1-3:crr-alpha': ('A6 reading: full AHEAD of the arm without logit replay', 'AHEAD over seeds 0-2'),
    'SOTA1-3:crr-beta': ('A6/A8 reading: full AHEAD of the arm without label replay', 'AHEAD over seeds 0-2'),
    'SOTA1-3:crr-kd': ('A6 reading: full AHEAD of the arm without the pull toward the slow model', 'AHEAD over seeds 0-2'),
    'SOTA1-3:crr-stepclock': ("D2/A1' reading: full AHEAD of the arm whose slow model runs on the step clock", 'AHEAD over seeds 0-2'),
    'SOTA1-3:pred-fast': ('nearest class mean on the slow model against the fast head (same units)', 'report only (AHEAD on the R4 surrogate)'),
    'SOTA1-3:pred-slow': ('nearest class mean against the slow head (same units)', 'report only (AHEAD on the R4 surrogate)'),
}


def num(v):
    return f'{v:+.6f} ({v:+.2f})'


def cmp_text(c):
    return (f"d = {num(c['d'])}, step {c['step']:.4f}; per seed " + ' / '.join(f'{x:+.2f}' for x in c['diffs'])
            + f" -> {c['label']}")


def frac(c, ahead=True):
    n = sum((v > 0) if ahead else (v < 0) for v in c['diffs'])
    return f"{n}/{len(c['diffs'])} seeds {'ahead' if ahead else 'behind'}"


def row(*cells):
    print('| ' + ' | '.join(cells) + ' |')


def main():
    rows = {r['id']: r for r in RES['rows']}
    for rid in WHAT:
        r = rows[rid]
        pred, thr = WHAT[rid]
        c = r.get('cmp')
        v = r.get('verdict')
        if rid == 'SOTA1-1a':
            obs = f"best baseline {r['best']}; " + cmp_text(c)
        else:
            obs = cmp_text(c)
        if v == 'PASS':
            verdict = ('**PASS-0** (unseen, strongly anchored; not PASS-1 until the SOTA1-S table covers it and a second '
                       'carrier replicates; the component is DER++\'s label term, M4/M5)')
        elif v == 'FAIL':
            verdict = '**FAIL**'
        else:
            verdict = 'report (no verdict)'
        row(rid, ANCHOR, DATA, pred, thr, obs, frac(c, c['d'] >= 0), verdict, SCRIPT, LOG)
    s = rows['SOTA1-S']
    row('SOTA1-S', ANCHOR, DATA, 'sensitivity of SOTA1-1: the label recomputed in 6 cells (q 0.98, q 0.995, cap 100, gamma 1, '
        'smoothing 0.5, lr 0.05; seeds 0-1)', 'FRAGILE if it flips in more than one cell',
        f"{s['flips']} of 6 cells flip (every cell BEHIND, as the default)", f"{6 - s['flips']}/6 cells same label",
        f"**{s['verdict']}** (the SOTA1-1 FAIL is robust)", SCRIPT, LOG)
    c1 = [r for k, r in rows.items() if k.startswith('SOTA1-C1')]
    held = sum(r['verdict'] == 'holds' for r in c1)
    row('SOTA1-C1', ANCHOR, DATA, 'a lossless pause leaves the run bitwise identical (crr and derpp, seeds 0-2; 3 tasks, pauses '
        'after updates 250, 700, 1200)', 'holds in every unit', f'holds in {held} of {len(c1)} units',
        f'{held}/{len(c1)}', f"**{'holds' if held == len(c1) else 'FAILS'}** (construction, Proposition 7; not evidence for CRR)",
        SCRIPT, LOG)
    base = json.load(open(os.path.join(UNITS, 'crr__s0__none.json')))['final_class_il']
    parts = ('net', 'buffer', 'rng', 'crr_ema', 'crr_clock', 'crr_eq')
    diffs = {p: json.load(open(os.path.join(UNITS, f'crr__s0__drop-{p}.json')))['final_class_il'] - base for p in parts}
    inert = ('crr_seen', 'opt', 'counters')
    h0 = json.load(open(os.path.join(UNITS, 'crr__s0__none.json')))['param_sha256']
    changed = {p: json.load(open(os.path.join(UNITS, f'crr__s0__drop-{p}.json')))['param_sha256'] != h0 for p in parts}
    idiffs = {p: json.load(open(os.path.join(UNITS, f'crr__s0__drop-{p}.json')))['final_class_il'] - base for p in inert}
    row('SOTA1-C2', ANCHOR, DATA, 'dropping any declared part of the pause state (net, buffer, random streams, slow model, own clock, '
        'H-EQ state) changes the run (crr seed 0)', 'holds / FAILS',
        'final class-IL change: ' + ', '.join(f'{p} {v:+.2f}' for p, v in diffs.items())
        + '; reported only: ' + ', '.join(f'{p} {v:+.2f}' for p, v in idiffs.items()),
        f"{sum(changed.values())}/6 parts change the final parameters (sha256)",
        f"**{rows['SOTA1-C2']['verdict']}** (construction)", SCRIPT, LOG)
    w = json.load(open(os.path.join(UNITS, 'crr__s0__world-20.json')))['final_class_il']
    wl = json.load(open(os.path.join(UNITS, 'crr__s0__wall-30.json')))['final_class_il']
    row('SOTA1-C3', ANCHOR, DATA, 'the world moving during the pause (20 batches expire per pause) changes the run: a must-fail '
        'control for the construction', 'holds / FAILS', f'stake {num(base - w)} class-IL points', '1/1',
        f"**{rows['SOTA1-C3']['verdict']}** (construction)", SCRIPT, LOG)
    row('SOTA1-C4', ANCHOR, DATA, 'the stake of a wall-clock valuation (30 updates lost per pause)', 'report',
        f'stake {num(base - wl)} class-IL points', '—', 'report (no verdict)', SCRIPT, LOG)
    row('SOTA1-R9', ANCHOR, DATA, 'the rerun of crr seed 0 is bitwise identical (parameter sha256 and accuracy matrix)',
        'holds / FAILS', 'holds' if RES['rerun_identical'] else 'FAILS', '1/1',
        f"**{'holds' if RES['rerun_identical'] else 'FAILS'}**", SCRIPT, LOG)
    row('SOTA1-ND', ANCHOR, DATA, 'context baselines lwf and ewc_on (seeds 0-2; mechanism rechecks M8, M12, report only)',
        'report', 'NOT DECIDABLE: the frozen runner passed rehearsal flags to non-buffer arms; the units failed at argument '
        'parsing before training (AGENT_LOG 153)', '0/6 units', 'NOT DECIDABLE (no registered verdict needs them)', SCRIPT, LOG)


if __name__ == '__main__':
    main()
