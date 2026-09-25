"""Grade CRR's candidate offers C1-C5 against the systematic sweep (Lossless_Pause/DECLARATION_2.md). Labels computed here (R15).

REDUNDANT: at least one fetched source states the candidate; PARTLY REDUNDANT: none states it, at least one states a close
form (the difference is in the claim's note); NOT FOUND IN THE SWEEP: neither. 'Not found' is never read as novel.
Also prints the new energy figures beside the old inputs (they replace nothing) and a counterfactual sensitivity for SEC.
Run: python3 Lossless_Pause/checks/grade_sweep.py
"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
import sweep_claims as S  # noqa: E402

CANDS = {'C1': 'state-digest audit of a pause/resume (hash the saved and restored state, not the outputs)',
         'C2': 'zero-stake pause (no incentive to resist a lossless pause, valuation on own steps)',
         'C3': 'SEC: a tuning-free calibrated penalty weight replacing a sweep',
         'C4': 'the empty-cut checklist (full state, own-clock keying, the world\'s content)',
         'C5': 'the own-clock cut (stop computing when the belief has settled)'}


def quote_num(claim_src, pattern):
    for c in S.CLAIMS:
        if c['source'].startswith(claim_src):
            m = re.search(pattern, ' '.join(c['quote']))
            if m:
                return m
    raise KeyError((claim_src, pattern))


def main():
    print('Systematic sweep of 2026-09-25 (DECLARATION_2): CRR\'s candidate offers against prior art')
    fams = collections.Counter(c['id'].split(':')[0] for c in S.CLAIMS)
    print(f"claims {len(S.CLAIMS)} ({', '.join(f'{k} {v}' for k, v in fams.items())}); quotes verified in verify_sweep_claims.txt")
    print()
    for k, text in CANDS.items():
        cs = [c for c in S.CLAIMS if c['tag'] == k]
        n = collections.Counter(c['reading'] for c in cs)
        lab = 'REDUNDANT' if n['states'] else ('PARTLY REDUNDANT' if n['close'] else 'NOT FOUND IN THE SWEEP')
        print(f"{k} {lab:22} states {n['states']}, close {n['close']}, bears {n['bears']} | {text}")
        for c in cs:
            if c['reading'] in ('states', 'close'):
                print(f"     {c['reading']:6} {c['source'][:70]} ({c['version'][:24]})")
    print()
    print('Topic claims (reported beside the earlier dossiers; they replace nothing):')
    topics = collections.Counter(c['tag'] for c in S.CLAIMS if c['reading'] == 'topic')
    print('  ' + ', '.join(f'{k} {v}' for k, v in sorted(topics.items())))
    m = quote_num('Morrison, Smith, Strubell 2026', r'Development accounts for ([\d.]+)% of total GPU hours .*? and ([\d.]+)% of total GPU energy')
    cons = open(os.path.join(ROOT, 'Energy Design Principle/checks/consolidated_estimate.txt')).read()
    ff = float(re.search(r'to ([\d.]+) \(Morrison: 913 of 1,372 MWh\)', cons)[1])
    print(f'  development share of a model project\'s energy: Olmo 3 (Morrison et al. 2026) {m[2]}% of GPU energy ({m[1]}% of GPU hours); '
          f'OLMo 2 (Morrison et al. 2025, used in the scenario) {1 - ff:.4f} of development + final-run energy')
    r = quote_num('Hugging Face (Luccioni et al.), AI Energy Score v2: Ref', r'use, on average, (\d+) times more energy')
    p = quote_num('Morrison, Smith, Strubell 2026', r'Think uses (\d+) × more datacenter energy than Instruct')
    print(f'  reasoning: {r[1]}x more inference energy on average (AI Energy Score v2); {p[1]}x more post-training energy (Olmo 3 Think vs Instruct)')
    i = quote_num('Niu, Zhang, Li et al. 2025', r'accounts for more than (\d+)% of total power consumption')
    print(f'  inference share: "more than {i[1]}%" of power (industry reports, as cited by TokenPowerBench; secondhand) against the '
          f'scenario\'s 1 - f_dev of 0.60 middle')
    print('  rebound: stated by Luccioni, Strubell & Crawford 2025 and found empirically for training by Morand et al. 2026 (quotes in the dossier)')
    print()
    print('SEC counterfactual sensitivity (C3 PARTLY REDUNDANT; not dominated: no quoted method sets a CL penalty weight)')
    o = quote_num('Karpukhin, Savchenko', r'approximately (\d+)% above a single training run')
    cost_alt = 1 + int(o[1]) / 100
    sweep = 17
    t1 = float(re.search(r'T1  SEC on penalty-weight sweeps\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', cons)[2])
    se = open(os.path.join(ROOT, 'Compute_Savings/checks/scale_estimate.txt')).read()
    s_mid = float(re.search(r'^\s+2030 middle\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+([\d.]+)', se, re.M)[1])
    frac_vs_sweep = 1 - 1 / sweep
    frac_vs_alt = (cost_alt - 1) / sweep
    print(f'  against a {sweep}-configuration sweep SEC saves {frac_vs_sweep:.4f} of the sweep; against an online weighting method at '
          f'{cost_alt:.2f} runs (2605.07756, pretraining losses) it saves {frac_vs_alt:.4f} of the sweep-equivalent')
    print(f'  T1 middle {t1:.4f} TWh assumes the sweep as the counterfactual; if such a method transferred to CL penalty weights (not shown), '
          f'T1 middle would scale by {frac_vs_alt / s_mid:.4f} to {t1 * frac_vs_alt / s_mid:.4f} TWh ({s_mid:.4f} = the middle s, scale_estimate.txt)')


if __name__ == '__main__':
    main()
