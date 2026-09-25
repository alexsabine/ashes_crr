"""A consolidated estimate: what a CRR-informed economy of continual learning, AI safety and compute could save in energy.

Declared in `Energy Design Principle/DECLARATION_2.md` Parts B and C (pushed at 4b3b995 before this script existed).
A scenario model, conditional on the methods holding; no data opened. Run: python3 "Energy Design Principle/checks/consolidated_estimate.py"
Inputs read from pinned files: Compute_Savings/checks/scale_estimate.txt, Alexander Plan/model/cl_patent.txt,
Energy Design Principle/checks/energy_rows.py (quoted rows) and checks/clock_cut.txt.
"""
import itertools
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
import energy_rows as ER  # noqa: E402
import retro_energy as RE  # noqa: E402

# assumed bands (DECLARATION_2 Part B)
F_REFRESH = (0.1, 0.5)
F_REASON = (0.1, 0.5)
F_SCALING = (0.01, 0.1)
# fair forecasts (DECLARATION_2 Part C): the investigator's probabilities, recorded before ENERGY1 and SOTA1
FORECASTS = [
    ('P1', 'SEC vs the tuned sweep on SOTA1\'s learner: accepted without losing a step, saving >= 80 % of the sweep', 0.45),
    ('P2', 'a continual learner reaches >= 95 % of retrain-from-scratch accuracy at <= 0.5 of its compute (online Split-CIFAR-100)', 0.10),
    ('P3', 'a horizon-free schedule is not behind cosine in the stream', 0.60),
    ('P4', 'shrink-and-perturb at task boundaries saves >= 10 % of work to a target', 0.30),
    ('P5', 'the arc cut is BETTER than the confidence cut on real data', 0.10),
    ('P6', 'the empty cut changes energy by 0 and leaves the run bitwise identical', 0.95),
    ('P7', 'SOTA1-1a: CRR-SCL is AHEAD of the best baseline', 0.35),
    ('P8', 'SEC\'s saving survives at LLM scale under AdamW', 0.15),
]


def read(p):
    return open(os.path.join(ROOT, p), encoding='utf-8').read()


def row(src_start, x_start):
    rs = [r for r in ER.ROWS if r['source'].startswith(src_start) and r['x_label'].startswith(x_start)]
    assert len(rs) >= 1, (src_start, x_start)
    return rs[0]


def main():
    se = read('Compute_Savings/checks/scale_estimate.txt')
    m = re.findall(r'^\s+2030 (low|middle|high)\s+([\d.]+)\s+([\d.]+)\s+[\d.]+\s+[\d.]+\s+([\d.]+)', se, re.M)
    t1 = {case: float(saved) for case, _, _, saved in m}
    e_ai = float(m[0][1])
    fdev = {case: float(fd) for case, _, fd, _ in m}
    dc2030 = float(re.search(r'2030 (\d+) TWh \(IEA\)', se)[1])
    home = float(re.search(r'a US home: (\d+) kWh/year', se)[1])
    cp = read('Alexander Plan/model/cl_patent.txt')
    final_runs = float(re.search(r'openai_final_runs_2024\s+([\d,]+)', cp)[1].replace(',', ''))
    rnd = float(re.search(r'openai_rnd_2024\s+([\d,]+)', cp)[1].replace(',', ''))
    p_adopt = float(re.search(r'P\(adopted by 2029\) = [\d.]+ x [\d.]+ x [\d.]+ = ([\d.]+)', cp)[1])
    acc = {a['source'].split(',')[0]: a for a in ER.ACCOUNTING}
    mq = ' '.join(acc['Morrison et al. 2025']['quote'])
    assert '913' in mq and '459' in mq
    f_final = (final_runs / rnd, 913 / (913 + 459))
    # quoted cost ratios (checks/energy_rows.py), recomputed by the grader's own functions
    r_cl = [RE.cost_ratio(r) for r in ER.ROWS if r['mech'] == 'E5' and r['source'].startswith('Ibrahim')]
    assert all(abs(x - 0.5) < 1e-9 for x in r_cl)
    r_stop = (RE.cost_ratio(row('Chen et al. 2024/2025', 'SimPO with First-Correct')),
              RE.cost_ratio(row('Muennighoff et al. 2025', 'budget forcing')))
    r_wsd = RE.cost_ratio(row('Hagele et al. 2024', 'constant LR + cooldowns'))
    carbon = row('Wiesner et al. 2026', 'curtailment-aware')
    cc = read('Energy Design Principle/checks/clock_cut.txt')
    cand = re.search(r'PROSPECTIVE CANDIDATE .*?: (yes|no)', cc)[1] == 'yes'
    gate = re.search(r'GATE (OPEN|CLOSED)', cc)[1]
    s_stop = (1 - r_stop[0], 1 - r_stop[1])

    print('Consolidated estimate (DECLARATION_2 Parts B-C): CRR-informed continual learning + AI safety + compute, 2030')
    print('A SCENARIO conditional on the methods holding at scale; not a forecast of net energy (no overlap or rebound)')
    print()
    print('[1] Inputs')
    print(f'  pinned   E_AI(2030) {e_ai:.2f} TWh; data centres {dc2030:.0f} TWh; f_dev low/middle/high '
          f"{fdev['low']:.4f}/{fdev['middle']:.4f}/{fdev['high']:.4f} (scale_estimate.txt)")
    print(f"  pinned   T1 SEC term 2030: low {t1['low']:.4f}, middle {t1['middle']:.4f}, high {t1['high']:.4f} TWh (scale_estimate.txt)")
    print(f'  sourced  f_final: {f_final[0]:.4f} (Epoch: final runs {final_runs:,.0f} of R&D {rnd:,.0f}) to {f_final[1]:.4f} '
          f'(Morrison: 913 of 1,372 MWh)')
    print(f'  quoted   s_cl = 1 - {r_cl[0]:.4f} (continual pre-training, Ibrahim et al., 3 rows); s_stop = 1 - {r_stop[0]:.4f} '
          f'to 1 - {r_stop[1]:.4f} (not-behind I7 rows); s_wsd = 1 - {r_wsd:.4f} (Hagele et al.)')
    cq = re.search(r'emit between ([\d.]+) and ([\d.]+) kgCO2.*?emits only ([\d.]+) kgCO2', ' '.join(carbon['quote']))
    print(f'  quoted   carbon (not energy) of curtailment-aware pause/resume training: {cq[3]} kgCO2 against {cq[1]} to {cq[2]} '
          f'kgCO2 for single-region runs (Wiesner et al. 2026); T4 counts it as energy moved, not saved')
    print(f'  ASSUMED  f_refresh {F_REFRESH}, f_reason {F_REASON}, f_scaling {F_SCALING}')
    print(f'  clock_cut.txt: gate {gate}; arc cut BETTER than confidence in W3 but not W1 (a PROSPECTIVE CANDIDATE): '
          f"{'yes' if cand else 'no'}")
    print()

    def gm(b):
        return math.sqrt(b[0] * b[1])

    def am(b):
        return (b[0] + b[1]) / 2

    fdev_band = (fdev['low'], fdev['high'])
    terms = {}
    # T2: E_AI x f_dev x f_final x f_refresh x s_cl
    f2 = lambda fd, ff, fr: e_ai * fd * ff * fr * (1 - r_cl[0])
    c2 = [f2(*x) for x in itertools.product(fdev_band, f_final, F_REFRESH)]
    terms['T2'] = (min(c2), f2(fdev['middle'], am(f_final), gm(F_REFRESH)), max(c2))
    # T3: E_AI x (1 - f_dev) x f_reason x s_stop
    f3 = lambda fd, fr, s: e_ai * (1 - fd) * fr * s
    c3 = [f3(*x) for x in itertools.product(fdev_band, F_REASON, s_stop)]
    terms['T3'] = (min(c3), f3(fdev['middle'], gm(F_REASON), am(s_stop)), max(c3))
    # T5: E_AI x f_dev x f_scaling x s_wsd
    f5 = lambda fd, fs: e_ai * fd * fs * (1 - r_wsd)
    c5 = [f5(*x) for x in itertools.product(fdev_band, F_SCALING)]
    terms['T5'] = (min(c5), f5(fdev['middle'], gm(F_SCALING)), max(c5))
    terms['T1'] = (t1['low'], t1['middle'], t1['high'])
    terms['T4'] = (0.0, 0.0, 0.0)
    attrib = {'T1': 'the CRR programme (SEC; the ledger: not a CRR rule)', 'T2': 'none (continual pre-training is published)',
              'T3': 'CRR' if cand else 'none (the arc cut did not beat the confidence cut; Wald)',
              'T4': 'none (energy moved, not saved)', 'T5': 'none (WSD is published)'}
    names = {'T1': 'SEC on penalty-weight sweeps', 'T2': 'continual updating instead of periodic retraining',
             'T3': 'content-based stopping of reasoning', 'T4': 'the safe pause (empty cut)',
             'T5': 'horizon-free schedules for multi-horizon sweeps'}
    print('[2] Terms, 2030, TWh (low = min and high = max over the band ends; middle = middle f_dev, arithmetic mean of sourced '
          'bands, geometric mean of assumed bands)')
    print(f"  {'term':3} {'':52} {'low':>9} {'middle':>9} {'high':>9}  attributable to")
    for k in ('T1', 'T2', 'T3', 'T4', 'T5'):
        lo, mi, hi = terms[k]
        print(f'  {k:3} {names[k]:52} {lo:9.4f} {mi:9.4f} {hi:9.4f}  {attrib[k]}')
    tot = [sum(terms[k][i] for k in terms) for i in range(3)]
    crr = [terms['T1'][i] + (terms['T3'][i] if cand else 0.0) for i in range(3)]
    print()
    print('[3] Totals, 2030 (conditional on holding; an upper bound on the sum of terms, no overlap or rebound)')
    for lab, v in (('technical potential of the mechanisms the lens endorses', tot),
                   ('attributable to CRR or its programme', crr)):
        print(f'  {lab:58} low {v[0]:9.4f}  middle {v[1]:9.4f}  high {v[2]:9.4f} TWh')
        print(f"  {'':58} share of data-centre electricity: {v[0] / dc2030:.6f} / {v[1] / dc2030:.6f} / {v[2] / dc2030:.6f}; "
              f'of AI-server electricity: {v[0] / e_ai:.6f} / {v[1] / e_ai:.6f} / {v[2] / e_ai:.6f}; '
              f'US homes: {v[0] * 1e9 / home:,.0f} / {v[1] * 1e9 / home:,.0f} / {v[2] * 1e9 / home:,.0f}')
    print(f"  attributable share of the technical potential: {crr[0] / tot[0]:.4f} / {crr[1] / tot[1]:.4f} / {crr[2] / tot[2]:.4f}")
    print(f"  probability-weighted attributable (x cl_patent's P(adopted) {p_adopt:.4f}, that model's assumption): "
          f"middle {crr[1] * p_adopt:.6f}, high {crr[2] * p_adopt:.6f} TWh")
    print()
    print('[4] Fair forecasts, recorded before ENERGY1 and SOTA1 (the investigator\'s probabilities; to be scored later)')
    for i, ev, p in FORECASTS:
        print(f'  {i}: P = {p:.2f}  {ev}')
    print(f"  expected number of the eight events that occur: {sum(p for _, _, p in FORECASTS):.2f}")


if __name__ == '__main__':
    main()
