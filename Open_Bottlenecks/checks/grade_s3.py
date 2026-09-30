"""OB1 stage 3 (Open_Bottlenecks/DECLARATION.md): grade each DISAGREES candidate C1-C3 (CRR_READING.md) against its targeted
prior-art sweep (dossiers docs/citations/ob1_s3_c{1,2,3}_2026-09-30.md; claims_s3_c*.py; quotes checked in verify_s3.txt):
REDUNDANT if any 'states'; else PARTLY REDUNDANT if any 'close'; else NOT FOUND IN THE SWEEP. The declared rule for going on:
NOT FOUND goes on; PARTLY REDUNDANT goes on only if the missing part is the part CRR predicts (the investigator's reading,
printed per candidate from MISSING below, fixed before this script ran). Deterministic, stdlib only; no raw texts read.
Run: python3 Open_Bottlenecks/checks/grade_s3.py
"""
import collections
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CANDS = [
    ('c1', 'C1 arc-clocked optimiser moments (stability gap, h1-B6)'),
    ('c2', 'C2 arc-triggered refresh (plasticity under switches, h3-B1)'),
    ('c3', 'C3 arc-triggered consolidation (boundary-free streams, h4-B1, h1-B1)'),
]
# the investigator's reading of what the close sources leave out, and whether it is the part CRR predicts (from the dossiers'
# 'Is the mechanism published?' sections and the agents' reports; fixed before this script ran)
MISSING = {
    'c1': ("the index is the learner's own step (probe-set KL, the arc) and the object is the optimiser moments in the "
           "stability-gap setting; published: KL-gated decay of BatchNorm statistics (MECTA), gradient-norm-gated beta2 "
           "(Kourkoutas-beta), velocity-gated momentum (iKFAD), alignment-triggered restarts", True),
    'c2': ("accumulation of own change to a unit since the last refresh, for plasticity under task switches; published: resets "
           "on a spike of own predictive KL against a running average (RDumb++), on per-step label flips (ABR), on accumulated "
           "reward-prediction error (SeRe)", True),
    'c3': ("the own accumulated change as the consolidation trigger; published: the same trigger for communication (Kamp et "
           "al.; event-triggered FL) and loss-plateau-triggered consolidation (Aljundi et al. 2019; Online-LoRA); TIDE not "
           "reached", True),
}


def grade(n):
    if n['states']:
        return 'REDUNDANT'
    if n['close']:
        return 'PARTLY REDUNDANT'
    return 'NOT FOUND IN THE SWEEP'


def main():
    print('OB1 stage 3: targeted prior art per candidate (DECLARATION.md stage 3; CRR_READING.md)')
    print('rule: REDUNDANT if states; else PARTLY REDUNDANT if close; else NOT FOUND IN THE SWEEP; not found is never novel')
    goes = []
    for cid, name in CANDS:
        cl = importlib.import_module(f'claims_s3_{cid}').CLAIMS
        n = collections.Counter(c['reading'] for c in cl)
        g = grade(n); miss, crr_part = MISSING[cid]
        on = g == 'NOT FOUND IN THE SWEEP' or (g == 'PARTLY REDUNDANT' and crr_part)
        goes.append((cid, on))
        print(f"\n{name}")
        print(f"   claims {len(cl)}, sources {len({c['url'] for c in cl})}: states {n['states']}, close {n['close']}, "
              f"bears {n['bears']}, contradicts {n['contradicts']} -> {g}")
        print(f"   missing (investigator): {miss}; the part CRR predicts: {'yes' if crr_part else 'no'}")
        print(f"   goes on to a stage-4 declaration: {'yes' if on else 'no'}")
    print(f"\ncandidates going on: {', '.join(c for c, o in goes if o) or 'none'}")
    print('caution: in each case the missing part is a choice of signal within a published family; a gate must include the '
          'published signals as baselines')


if __name__ == '__main__':
    main()
