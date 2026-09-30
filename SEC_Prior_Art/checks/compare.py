"""SPA1 follow-up (prompt-log entry 256): SEC's held-out results set against what the published sources report about
tuning-free EWC/Laplace weights. Reads the pinned ledger rows (ledger/LEDGER.md) and the verified claims (claims_f1-f3.py);
prints, per held-out SEC study, the calibrated (or clipped) arm's and the raw Laplace weight's 'not behind the tuned lambda'
counts, a pooled count (report only: pooled across different families and arms, not a registered test), and the published
statements on the tuning-free weight (positions S1, S4, S6). Deterministic, stdlib only. Run: python3 SEC_Prior_Art/checks/compare.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import claims_f1, claims_f2, claims_f3  # noqa: E402

LEDGER = os.path.join(HERE, '..', '..', 'ledger', 'LEDGER.md')
# (row id, arm name, regex for the arm's count in 'observed', regex for raw Laplace's count)
ROWS = [
    ('SCL3-3', 'calibrated SEC (no clip)', r'\|\s*(\d+)/(\d+)\s*\|\s*\*\*PASS-0', r'raw Bayes not behind on (\d+)/(\d+)'),
    ('SEC3-3', 'calibrated SEC (no clip)', r'\|\s*(\d+)/(\d+):', r'raw Laplace (\d+)/(\d+)'),
    ('SEC4-1', 'clipped SEC (kappa 0.5)', r'\|\s*(\d+)/(\d+):', r'raw Laplace (\d+)/(\d+)'),
    ('SEC5-1', 'clipped SEC (kappa 0.5)', r'\|\s*(\d+)/(\d+):', r'raw Laplace (\d+)/(\d+)'),
]


def main():
    text = open(LEDGER, encoding='utf-8').read().splitlines()
    rows = {ln.split('|')[1].strip(): ln for ln in text if ln.startswith('| ')}
    print('SEC against the published tuning-free weight (SPA1 follow-up, prompt-log entry 256)')
    print('held-out studies: count of carriers where the arm is not behind the tuned lambda by a step (from the pinned ledger rows)')
    tot = [0, 0, 0, 0]
    for rid, arm, rx_arm, rx_raw in ROWS:
        ln = rows[rid]; a = re.search(rx_arm, ln); r = re.search(rx_raw, ln)
        na, da, nr, dr = int(a.group(1)), int(a.group(2)), int(r.group(1)), int(r.group(2))
        assert da == dr, rid
        tot[0] += na; tot[1] += da; tot[2] += nr; tot[3] += dr
        print(f'   {rid:7} {arm:26} {na}/{da}   raw Laplace (textbook w = 1/2, uncalibrated) {nr}/{dr}')
    print(f'   pooled (report only; different families and arms): SEC arm {tot[0]}/{tot[1]}, raw Laplace {tot[2]}/{tot[3]}')
    print('\npublished statements on the tuning-free (natural, lambda = 1 or Bayes) weight, verified quotes (verify.txt):')
    C = claims_f1.CLAIMS + claims_f2.CLAIMS + claims_f3.CLAIMS; seen = set()
    for c in C:
        if c['tag'] not in ('S1', 'S4', 'S6') or c['reading'] not in ('states', 'close', 'bears', 'contradicts'):
            continue
        key = (c['url'], c['tag'])
        if key in seen:
            continue
        seen.add(key)
        print(f"   [{c['tag']} {c['reading']}] {c['source'][:100]} ({c['version'][:24]})")
        print(f"      \"{c['quote'][-1][:230]}\"")


if __name__ == '__main__':
    main()
