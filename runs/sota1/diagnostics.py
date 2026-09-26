"""SOTA1 post hoc diagnostics (prompt-log entry 208): descriptive reads of the unit records, NO verdict, no ledger row.

Written after the scoring (runs/sota1/score.txt); nothing here was pre-registered, so nothing here may be used on this or
another dataset without a fresh prereg on a later day (R3). Reads runs/sota1/units/*.json only.
    python3 runs/sota1/diagnostics.py > runs/sota1/diagnostics.txt
[D1] the pull weight each arm actually applied, against its final class-incremental accuracy (a dose-response read);
[D2] plasticity: the fast head's class-incremental accuracy on the task just learned, averaged over tasks 2-10, and on
     task 1 at the end (a stalemate reads as ~0 on the newest task with the oldest task intact);
[D3] how much nearest class mean adds over the fast head, per arm.
"""
import glob
import json
import os
import statistics as st

U = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'units')
FIXED_EFFECTIVE = 0.5 * 5.5   # crr-kdfixed: loss_p + 0.5 * lambda * KD, lambda = 5.5 (models/crr_scl.py, frozen)


def recs(arm, seeds):
    out = []
    for s in seeds:
        p = os.path.join(U, f'{arm}__s{s}.json')
        if os.path.exists(p):
            out.append(json.load(open(p)))
    return out


def weight(r, arm):
    if arm == 'crr-kd':
        return 0.0
    if arm == 'crr-kdfixed':
        return FIXED_EFFECTIVE
    w = [x for x in r['eq_w_samples'] if x is not None]
    return st.median(w) if w else None


def newest(m):
    # class-IL accuracy on task t right after learning task t, for t = 2..10
    return st.mean(m[t][t] for t in range(1, len(m)))


def main():
    arms = [('crr-kd', range(3)), ('crr-kdfixed', range(3)), ('crr', range(3)), ('crr@cap100', range(2)),
            ('crr-cos', range(3)), ('crr-beta', range(3)), ('crr-a8', range(3))]
    print('SOTA1 post hoc diagnostics (descriptive; no verdict; prompt-log entry 208)')
    print()
    print('[D1] pull weight applied (H-EQ: median of the recorded samples, tasks 2-10) against final class-IL (seeds shown)')
    for arm, seeds in arms:
        rs = recs(arm, seeds)
        ws = [weight(r, arm) for r in rs]
        ws_all = [x for r in rs for x in (r['eq_w_samples'] or []) if x is not None] if arm not in ('crr-kd', 'crr-kdfixed') else []
        capped = (f'; samples at the cap 10: {sum(abs(x - 10.0) < 1e-9 for x in ws_all)}/{len(ws_all)}' if ws_all else '')
        print(f"  {arm:12} weight {st.mean(ws):6.3f} (per seed {', '.join(f'{w:.3f}' for w in ws)}){capped}; "
              f"final class-IL {st.mean(r['final_class_il'] for r in rs):6.2f}")
    print()
    print('[D2] plasticity of the fast head: class-IL accuracy on the task just learned (mean over tasks 2-10) and on task 1 at the end')
    for arm, seeds in arms:
        rs = recs(arm, seeds)
        nw = [newest(r['alt_pred']['fast']['acc_class_matrix']) for r in rs]
        t1 = [r['alt_pred']['fast']['acc_class_matrix'][-1][0] for r in rs]
        last = [r['alt_pred']['fast']['acc_class_matrix'][-1][-1] for r in rs]
        print(f'  {arm:12} newest task {st.mean(nw):6.2f}; task 1 at the end {st.mean(t1):6.2f}; task 10 at the end {st.mean(last):6.2f}')
    print()
    print('[D3] nearest class mean (the scored prediction) minus the fast head, final class-IL')
    for arm, seeds in arms:
        rs = recs(arm, seeds)
        d = [r['final_class_il'] - r['alt_pred']['fast']['final_class_il'] for r in rs]
        print(f"  {arm:12} {st.mean(d):+6.2f} (per seed {', '.join(f'{x:+.2f}' for x in d)})")


if __name__ == '__main__':
    main()
