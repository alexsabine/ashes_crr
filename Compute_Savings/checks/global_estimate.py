"""A year's global compute, energy and CO2 saving from a tuning-free forgetting weight (Compute_Savings/DECLARATION_3.md,
prompt-log entry 228).

A scale model; no data opened, no training run. Run: python3 Compute_Savings/checks/global_estimate.py
Pinned inputs read from the repository:
  runs/scl3/results_*.jsonl, runs/sec3/results_*.jsonl (unguarded SEC on 16 UNSEEN carriers, two families),
  runs/sec4/results_*.jsonl when they exist (the clipped SEC on a third UNSEEN family; before the data step: 'pending'),
  prereg/sec4/dev_SEC4.txt (the clipped SEC on SEEN carriers: development, printed, never used),
  Alexander Plan/model/cl_patent.txt (P(adopted)).
Published figures: docs/citations/global_estimate_2026-09-28.md (fetched 2026-09-28) and, for Declaration 2's factors,
docs/citations/compute_scale_2026-09-25.md. Assumed bands: DECLARATION_2 and DECLARATION_3.
"""
import glob
import json
import math
import os
import re
import statistics

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
FS = FE = 0.1
GRID, CHECK, DIV_FRAC = 17, 3, 0.5
THREE = (1.0, 30.0, 1000.0)

# Declaration 2's factors (docs/citations/compute_scale_2026-09-25.md), unchanged
DC_TWH = {2024: 415.0, 2030: 945.0}
AI_SHARE_2024 = 0.15
AI_GROWTH = 0.30
F_DEV = {'low': 0.30, 'middle': 0.40, 'high': 5.0 / 7.0}
F_SWEEP = {'low': 0.001, 'high': 0.02}
F_SWEEP_EWC_ONLY = 0.0001        # DECLARATION_3: EWC-style continual learning only (ASSUMED)
HOME_KWH = 10791.0

# DECLARATION_3's factors, quoted verbatim in docs/citations/global_estimate_2026-09-28.md (fetched 2026-09-28)
DC_CO2_MT_2024 = 180.0           # IEA Energy and AI (2025): data centres ~180 Mt indirect CO2 'today' (2024)
SRC = {
    'I_dc_iea': (DC_CO2_MT_2024 * 1e12 / (DC_TWH[2024] * 1e9), 'g CO2/kWh', 'derived'),   # 180 Mt / 415 TWh (IEA, 2024)
    'I_grid': (458.0, 'g CO2e/kWh', 'published'),      # Ember Global Electricity Review 2026: global average, 2025
    'I_dc_us': (548.0, 'g CO2e/kWh', 'published'),     # Guidi et al., arXiv 2411.09786 v1: US data centres, energy-weighted
    'P_board': (0.700, 'kW per GPU', 'published'),     # NVIDIA H100 SXM max TDP 700 W
    'P_dgx': (10.2, 'kW per 8-GPU system', 'published'),   # NVIDIA DGX H100 system max input power
    'PUE_avg': (1.54, '', 'published'),                # Uptime Institute Global Data Center Survey 2025
    'PUE_fleet': (1.09, '', 'published'),              # Google fleet, 2025 and trailing twelve months
    'BF16_dense': (989.4e12, 'FLOP/s', 'published'),   # NVIDIA H100 SXM5 dense BF16 Tensor Core peak (whitepaper)
    'MFU_low': (0.38, '', 'published'),                # Llama 3 405B BF16 MFU 38-43 % (arXiv 2407.21783 v3)
    'MFU_high': (0.43, '', 'published'),
    'CAR_T': (4.6, 't CO2 per car-year', 'published'),  # US EPA typical passenger vehicle
    'DC_CO2_MT': (DC_CO2_MT_2024, 'Mt CO2 (2024)', 'published'),
}


def load(pattern):
    data = {}
    for p in sorted(glob.glob(os.path.join(ROOT, pattern))):
        name, rows = None, []
        for line in open(p):
            if not line.startswith('{'):
                continue
            o = json.loads(line)
            if 'acc' in o and 'mode' in o:
                rows.append(o); name = o.get('dataset', name)
            elif 'dataset' in o:
                name = o['dataset']
        if name and rows:
            data[name] = rows
    return data


def arm(rows, mode, value=None):
    v = [r for r in rows if r.get('mode') == mode and r.get('fs') == FS and r.get('fe') == FE and r.get('distort') is None
         and (value is None or abs(r['value'] - value) <= 1e-6 * max(1.0, abs(value)))]
    return [r['acc'] for r in sorted(v, key=lambda r: r['seed'])]


def step_of(tv):
    return max(1.0, 2 * statistics.stdev(tv) / math.sqrt(len(tv)))


def carriers(data, mode):
    """Per carrier: tuned accuracy, step, the method's seeds, the best of the 3-point sweep."""
    R = {}
    for name, rows in data.items():
        grid = sorted(set(round(r['value'], 6) for r in rows if r.get('mode') == 'fixed' and r.get('fs') == FS
                          and r.get('fe') == FE and r.get('distort') is None))
        g = {w: arm(rows, 'fixed', w) for w in grid}
        tuned = max(g, key=lambda w: statistics.mean(g[w]))
        m = arm(rows, mode, 0.0 if mode == 'bayes_sec' else None)
        if not m:
            continue
        R[name] = dict(tacc=statistics.mean(g[tuned]), step=step_of(g[tuned]), m=m, G=len(grid),
                       best3=max(statistics.mean(g[w]) for w in THREE if w in g))
    return R


def protocols(R):
    """p_div, and per protocol: expected configurations c and the share of carriers behind the tuned lambda by a step."""
    N = len(R)
    div = [n for n, r in R.items() if any(a < DIV_FRAC * r['tacc'] for a in r['m'])]
    behind = lambda a, r: a - r['tacc'] <= -r['step']  # noqa: E731
    b_full = [n for n, r in R.items() if behind(statistics.mean(r['m']), r)]
    b_fb = [n for n in b_full if n not in div]                    # a diverged carrier gets the full sweep
    b_chk = [n for n, r in R.items() if behind(max(statistics.mean(r['m']), r['best3']), r)]
    p = len(div) / N
    return dict(N=N, div=div, p_div=p,
                P={'P-FULL': (1.0, b_full), 'P-FALLBACK': (1.0 + p * GRID, b_fb), 'P-CHECK': (1.0 + CHECK, b_chk)})


def gm(a, b): return math.sqrt(a * b)


def report(ai, FSW, S, p_adopt):
    """Energy (TWh, IT-level as E_AI), compute (H100-hours, FLOP), CO2 (Mt, on facility energy = IT x PUE)."""
    v = {k: x[0] for k, x in SRC.items()}
    I = {'low': v['I_dc_iea'], 'middle': v['I_grid'], 'high': v['I_dc_us']}
    P = {'low': v['P_dgx'] / 8, 'middle': gm(v['P_board'], v['P_dgx'] / 8), 'high': v['P_board']}      # kW per GPU; low output = high power
    PUE = {'low': v['PUE_avg'], 'middle': gm(v['PUE_avg'], v['PUE_fleet']), 'high': v['PUE_fleet']}
    MFU = {'low': v['MFU_low'], 'middle': (v['MFU_low'] + v['MFU_high']) / 2, 'high': v['MFU_high']}
    dc = {2024: DC_TWH[2024], 2026: DC_TWH[2024] * (DC_TWH[2030] / DC_TWH[2024]) ** (2 / 6), 2030: DC_TWH[2030]}

    def row(year, case, s, fsw=None):
        e = ai[year] * F_DEV[case] * (FSW[case] if fsw is None else fsw) * s          # TWh, IT level
        gpuh = e * 1e9 / P[case]                                                     # H100-hours (kWh / kW)
        flop = gpuh * 3600 * v['BF16_dense'] * MFU[case]
        fac = e * PUE[case]                                                          # TWh at the meter
        co2 = fac * 1e9 * I[case] / 1e12                                             # Mt (kWh x g/kWh -> g -> Mt)
        return e, gpuh, flop, fac, co2
    print()
    print('[3] One year, protocol P-FALLBACK (SEC; a full sweep where a seed diverges), conditional on the method holding')
    hdr = (f"  {'year':4} {'case':7} {'IT TWh':>8} {'meter TWh':>9} {'of DC':>9} {'H100-hours':>14} {'FLOP':>9} "
           f"{'CO2 kt':>9} {'US homes':>9} {'cars':>9}")
    print(hdr)
    out = {}
    for y in (2026, 2030):
        for c in ('low', 'middle', 'high'):
            e, g, f, fac, co2 = row(y, c, S['P-FALLBACK'])
            out[(y, c)] = (e, g, f, fac, co2)
            print(f"  {y} {c:7} {e:8.4f} {fac:9.4f} {fac / dc[y]:9.6f} {g:14,.0f} {f:9.2e} {co2 * 1e3:9.2f} "
                  f"{fac * 1e9 / HOME_KWH:9,.0f} {co2 * 1e6 / v['CAR_T']:9,.0f}")
    print(f"  (data-centre electricity {dc[2026]:.1f} TWh in 2026, interpolated geometrically between the IEA's 2024 and 2030 figures)")
    print()
    print('[4] 2026, middle case, by protocol (and what each saving is measured against)')
    for k, s in S.items():
        e, g, f, fac, co2 = row(2026, 'middle', s)
        print(f"  {k:10}: s = {s:.4f}; {e:.4f} TWh IT, {fac:.4f} TWh at the meter, {g:,.0f} H100-hours, {co2 * 1e3:.2f} kt CO2")
    s3 = S['P-FALLBACK'] - (1 - CHECK / GRID)
    e3 = ai[2026] * F_DEV['middle'] * FSW['middle'] * s3
    print(f"  against a 3-point sweep instead of the full sweep (P-FALLBACK): s3 = {s3:+.4f} -> {e3:+.4f} TWh IT "
          f"({'a saving' if s3 > 0 else 'no saving: a 3-point sweep is cheaper'})")
    print('  against a reused lambda (1 configuration): no compute saving under P-FULL; SEC\'s gain there is accuracy')
    print()
    print('[5] Bounds and sensitivity')
    e, g, f, fac, co2 = row(2026, 'middle', S['P-FALLBACK'], fsw=F_SWEEP_EWC_ONLY)
    print(f"  EWC-style continual learning only (f_sweep {F_SWEEP_EWC_ONLY}), 2026 middle: {e:.5f} TWh IT, {g:,.0f} H100-hours, "
          f"{co2 * 1e3:.3f} kt CO2")
    hi = ai[2030] * F_DEV['high'] * F_SWEEP['high'] * S['P-FULL']
    hi_co2 = hi * v['PUE_avg'] * 1e9 * I['high'] / 1e12
    print(f"  outer bound (2030, every factor at its high end, P-FULL, the highest PUE and intensity): {hi:.4f} TWh IT, "
          f"{hi * 1e9 / P['high']:,.0f} H100-hours, {hi_co2 * 1e3:.1f} kt CO2")
    for y in (2026, 2030):
        e, g, f, fac, co2 = out[(y, 'middle')]
        print(f"  unconditional, x cl_patent's P(adopted) = {p_adopt:.4f} (that model's assumption), {y} middle: "
              f"{e * p_adopt:.6f} TWh IT, {g * p_adopt:,.0f} H100-hours, {co2 * p_adopt * 1e3:.4f} kt CO2")
    dce = v['DC_CO2_MT']
    e, g, f, fac, co2 = out[(2026, 'middle')]
    print(f"  scale: data-centre emissions {dce:g} Mt CO2 (IEA); the 2026 middle saving is {co2 / dce:.2e} of it")
    print()
    print('[6] The investigator\'s expectations (DECLARATION_3, written before the sources and the script) against the printout')
    print('    "of the order of X or less" holds if observed <= 10^0.5 X; a stated range holds if observed is inside it')
    e, g, f, fac, co2 = out[(2026, 'middle')]
    ew = row(2026, 'middle', S['P-FALLBACK'], fsw=F_SWEEP_EWC_ONLY)[0]
    checks = [('energy, 2026 middle P-FALLBACK, TWh at the meter, <~ 0.1', fac, fac <= 0.1 * 10 ** 0.5),
              ('energy share of data-centre electricity < 0.001', fac / dc[2026], fac / dc[2026] < 0.001),
              ('CO2, 2026 middle, Mt, <~ 0.05', co2, co2 <= 0.05 * 10 ** 0.5),
              ('compute, 2030 high, H100-hours in 1e7..1e8', out[(2030, 'high')][1], 1e7 <= out[(2030, 'high')][1] <= 1e8),
              ('saving against a 3-point sweep <= 2/17 of the sweep', s3, s3 <= 2 / GRID),
              ('EWC-only row about 45x below the middle row (30..60)', e / ew, 30 <= e / ew <= 60)]
    for lab, val, ok in checks:
        print(f"  {lab:58}: {val:.4g} -> {'holds' if ok else 'MISSED'}")


def main():
    print('Compute_Savings global estimate (DECLARATION_3): compute, energy and CO2 saved in one year IF the method held')
    print('every figure is conditional (the SGD/numpy-MLP result transferring to large models; f_sweep ASSUMED; small samples);')
    print('no PASS-2 exists for SEC; not quotable outside the ledger (R8)')
    print()
    print('[1] The saving per sweep, from the pinned studies (s = 1 - c/17; c = expected configurations per carrier)')
    sets = []
    unguarded = {}
    unguarded.update(load('runs/scl3/results_*.jsonl')); unguarded.update(load('runs/sec3/results_*.jsonl'))
    sets.append(('unguarded SEC, SCL3 + SEC3 (16 UNSEEN carriers, two families)', carriers(unguarded, 'bayes_sec')))
    sec4 = load('runs/sec4/results_*.jsonl')
    if sec4:
        sets.append(('clipped SEC, SEC4 (UNSEEN, third family)', carriers(sec4, 'bayes_sec_clip')))
    else:
        print('  clipped SEC, SEC4 (UNSEEN, third family): pending (data step on or after 2026-09-29 00:00 UTC)')
    dev = open(os.path.join(ROOT, 'prereg/sec4/dev_SEC4.txt')).read()
    m = re.search(r'^clip : not behind (\d+)/(\d+).*?divergence carriers not behind (\d)/3', dev, re.M)
    print(f'  clipped SEC on SEEN carriers (development, not evidence; never used below): not behind {m[1]}/{m[2]}, '
          f'divergence carriers not behind {m[3]}/3')
    S = {}
    for label, R in sets:
        pr = protocols(R)
        print(f'  {label}: N = {pr["N"]}; carriers with a seed below {DIV_FRAC} x the tuned accuracy: {pr["div"]} '
              f'-> p_div = {pr["p_div"]:.4f}')
        for k, (c, b) in pr['P'].items():
            s = 1 - c / GRID; s3 = (CHECK - c) / GRID
            print(f'     {k:10}: c = {c:.4f}; saving against the full sweep s = {s:.4f}; against a 3-point sweep {s3:+.4f}; '
                  f'against a reused lambda {1 - c:+.4f} configurations; behind the tuned lambda by a step on {len(b)}/{pr["N"]} {b}')
        S = {k: 1 - c / GRID for k, (c, b) in pr['P'].items()}
        S_label = label
    print(f'  used below: the last evidence set ({S_label})')
    print()
    p = open(os.path.join(ROOT, 'Alexander Plan/model/cl_patent.txt')).read()
    p_adopt = float(re.search(r'P\(adopted by 2029\) = [\d.]+ x [\d.]+ x [\d.]+ = ([\d.]+)', p)[1])
    ai = {2024: DC_TWH[2024] * AI_SHARE_2024}
    ai[2026] = ai[2024] * (1 + AI_GROWTH) ** 2
    ai[2030] = ai[2024] * (1 + AI_GROWTH) ** 6
    FSW = {'low': F_SWEEP['low'], 'middle': math.sqrt(F_SWEEP['low'] * F_SWEEP['high']), 'high': F_SWEEP['high']}
    print('[2] Inputs')
    print(f"  published (Declaration 2) E_AI: 2024 {ai[2024]:.2f} TWh; derived 2026 {ai[2026]:.2f} TWh, 2030 {ai[2030]:.2f} TWh "
          f"(growth {AI_GROWTH:.2f}/year)")
    print(f"  published (Declaration 2) f_dev low/middle/high {F_DEV['low']:.4f}/{F_DEV['middle']:.4f}/{F_DEV['high']:.4f}")
    print(f"  ASSUMED  f_sweep low/middle/high {FSW['low']}/{FSW['middle']:.5f}/{FSW['high']}; EWC-only row {F_SWEEP_EWC_ONLY}")
    for k, (v, unit, lab) in SRC.items():
        print(f'  {lab:9} {k}: {v:g} {unit}')
    print(f"  derived   power per GPU in a DGX H100: {SRC['P_dgx'][0] / 8:.3f} kW; 1 TWh at {SRC['P_board'][0]} kW = "
          f"{1e9 / SRC['P_board'][0]:.3e} H100-hours")
    report(ai, FSW, S, p_adopt)


if __name__ == '__main__':
    main()
