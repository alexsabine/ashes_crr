"""If the method held on large AI systems, how much energy would it save? (Compute_Savings/DECLARATION_2.md, prompt-log 198)

A scale model; no data opened, no training run. Run: python3 Compute_Savings/checks/scale_estimate.py
Pinned inputs read from the repository: Compute_Savings/checks/compute_savings.txt (the SCL3 sweep saving),
Alexander Plan/model/cl_patent.txt (P(adopted)), prereg/sota1/budget.txt (measured seconds per unit).
Published figures: docs/citations/compute_scale_2026-09-25.md (fetched 2026-09-25). Assumed bands: DECLARATION_2.
"""
import math
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

# published (docs/citations/compute_scale_2026-09-25.md)
DC_2024_TWH = 415.0          # IEA, all data centres, 2024
DC_2030_TWH = 945.0          # IEA base case, 2030
AI_SHARE_2024 = 0.15         # IEA: servers for AI, share of data-centre energy, 2024
AI_GROWTH = 0.30             # IEA: AI-server electricity growth per year (predominantly inference)
F_DEV = {'low': (0.30, 'Meta 10:20:70, experimentation + training'),
         'middle': (0.40, 'Google 2019-2021, training 2/5 of ML energy'),
         'high': (5.0 / 7.0, 'OpenAI 2024, R&D 5 of 7 of compute spend')}
HOME_KWH = 10791.0           # EIA, US residential customer, 2022
LLAMA3 = dict(total=466, planned=47, unexpected=419, effective_min=0.90)
MUP_TUNING_SHARE = 0.07      # Tensor Programs V: all-HP tuning cost / pretraining cost, with transfer

# assumed (DECLARATION_2)
F_SWEEP = {'low': 0.001, 'high': 0.02}
F_SWEEP_BEYOND = 0.05        # beyond the record: the calibration generalised to every penalty-like weight
CONFIRM, GRID = 3, 17


def pinned():
    t = open(os.path.join(ROOT, 'Compute_Savings/checks/compute_savings.txt')).read()
    m = re.search(r'C5 energy: .*? spends (\d+)/(\d+) = [\d.]+ .*?a saving of ([\d.]+); it is accepted without losing a step '
                  r'on (\d+)/(\d+)', t)
    n, sweep, saving, acc, N = int(m[1]), int(m[2]), float(m[3]), int(m[4]), int(m[5])
    p = open(os.path.join(ROOT, 'Alexander Plan/model/cl_patent.txt')).read()
    p_adopt = float(re.search(r'P\(adopted by 2029\) = [\d.]+ x [\d.]+ x [\d.]+ = ([\d.]+)', p)[1])
    b = open(os.path.join(ROOT, 'prereg/sota1/budget.txt')).read()
    secs = {k: float(v) for k, v in re.findall(r'^\s+(\S+)\s+(\d+)\s*$', b, re.M)}
    return dict(n=n, sweep=sweep, saving=saving, acc=acc, N=N, p_adopt=p_adopt, secs=secs)


def main():
    P = pinned()
    s_hi = 1 - P['n'] / P['sweep']
    assert abs(s_hi - P['saving']) < 5e-5, 'the pinned saving does not match its counts'
    s_lo = 1 - CONFIRM / GRID
    S = {'low': s_lo, 'middle': (s_lo + s_hi) / 2, 'high': s_hi}
    FS = {'low': F_SWEEP['low'], 'middle': math.sqrt(F_SWEEP['low'] * F_SWEEP['high']), 'high': F_SWEEP['high']}
    ai = {2024: DC_2024_TWH * AI_SHARE_2024}
    ai[2030] = ai[2024] * (1 + AI_GROWTH) ** 6
    dc = {2024: DC_2024_TWH, 2030: DC_2030_TWH}

    print('Compute_Savings scale estimate (DECLARATION_2): energy saved IF the method held on large AI systems')
    print('every figure is conditional on the method holding; SCL3-3 is PASS-0 (provisional, one study, fragile); no PASS-2 exists')
    print()
    print('[1] Inputs')
    print(f"  pinned   SEC sweep saving (SCL3, UNSEEN): {P['n']}/{P['sweep']} configurations -> s = {s_hi:.4f}; accepted on {P['acc']}/{P['N']}")
    print(f"  derived  s with {CONFIRM} confirming configurations of {GRID}: {s_lo:.4f}")
    print(f"  published data-centre electricity: 2024 {DC_2024_TWH:.0f} TWh, 2030 {DC_2030_TWH:.0f} TWh (IEA)")
    print(f"  published AI servers: {AI_SHARE_2024:.2f} of data-centre energy in 2024, growth {AI_GROWTH:.2f}/year (IEA)")
    print(f"  derived  E_AI: 2024 {ai[2024]:.2f} TWh; 2030 {ai[2030]:.2f} TWh ({ai[2030] / dc[2030]:.4f} of data-centre electricity)")
    for k, (v, lab) in F_DEV.items():
        print(f"  published f_dev {k:6}: {v:.4f} ({lab})")
    print(f"  ASSUMED  f_sweep: low {F_SWEEP['low']}, high {F_SWEEP['high']} (middle = geometric mean {FS['middle']:.5f}); "
          f"context: all-HP tuning with transfer = {MUP_TUNING_SHARE:.2f} of pretraining (Tensor Programs V)")
    print(f"  published a US home: {HOME_KWH:.0f} kWh/year (EIA)")
    print()
    print('[2] SEC: E_saved = E_AI x f_dev x f_sweep x s (conditional on the method holding)')
    print(f"  {'year':4} {'case':7} {'E_AI TWh':>9} {'f_dev':>7} {'f_sweep':>8} {'s':>7} {'saved TWh':>10} {'of DC elec':>11} "
          f"{'of AI elec':>11} {'US homes':>11}")
    res = {}
    for y in (2024, 2030):
        for k in ('low', 'middle', 'high'):
            e = ai[y] * F_DEV[k][0] * FS[k] * S[k]
            res[(y, k)] = e
            print(f"  {y} {k:7} {ai[y]:9.2f} {F_DEV[k][0]:7.4f} {FS[k]:8.5f} {S[k]:7.4f} {e:10.4f} {e / dc[y]:11.6f} "
                  f"{e / ai[y]:11.6f} {e * 1e9 / HOME_KWH:11,.0f}")
    e = ai[2030] * F_DEV['high'][0] * F_SWEEP_BEYOND * s_hi
    print(f"  beyond the record (f_sweep {F_SWEEP_BEYOND}, every penalty-like weight calibrated), 2030 high: {e:.4f} TWh "
          f"({e / dc[2030]:.6f} of DC electricity; {e * 1e9 / HOME_KWH:,.0f} US homes)")
    print(f"  unconditional mean with cl_patent's P(adopted) = {P['p_adopt']:.4f} (that model's assumption): 2030 middle "
          f"{res[(2030, 'middle')] * P['p_adopt']:.6f} TWh, 2030 high {res[(2030, 'high')] * P['p_adopt']:.6f} TWh")
    print()
    print('[3] What no method here touches, and the ceiling for any training-side method (2030)')
    for k in ('low', 'middle', 'high'):
        fd = F_DEV[k][0]
        print(f"  f_dev {k:6}: serving (inference) {ai[2030] * (1 - fd):7.2f} TWh untouched; ceiling for a training-side "
              f"method (all development) {ai[2030] * fd:7.2f} TWh")
    print()
    print('[4] The empty cut (a bound, not an estimate)')
    ps = LLAMA3['planned'] / LLAMA3['total']
    lost = 1 - LLAMA3['effective_min']
    print(f"  Llama 3 405B, 54 days: {LLAMA3['total']} interruptions, {LLAMA3['planned']} planned ({ps:.4f}), "
          f"{LLAMA3['unexpected']} unexpected; effective training time > {LLAMA3['effective_min']:.2f}")
    print(f"  a cut can be taken only before a planned stop; ceiling on time it could touch = lost ({lost:.2f}) x planned "
          f"share ({ps:.4f}) = {lost * ps:.4f} of pre-training time (ASSUMED: equal time lost per interruption)")
    print('  a checkpoint written before planned maintenance (standard practice) already recovers this: saving beyond good '
          'practice claimed = 0')
    print()
    print('[5] The CRR learner per run (measured seconds per CIFAR-100 unit, prereg/sota1/budget.txt; CPU, before the data step)')
    c = P['secs']['crr']
    for b in ('er', 'er_ace', 'derpp', 'xder'):
        r = c / P['secs'][b]
        print(f"  crr / {b:7}: {c:.0f} / {P['secs'][b]:.0f} s = {r:.4f} -> {'an energy COST per run' if r > 1 else 'cheaper per run'}")


if __name__ == '__main__':
    main()
