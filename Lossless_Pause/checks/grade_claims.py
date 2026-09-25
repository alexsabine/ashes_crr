"""Grade Lossless_Pause/DECLARATION.md predictions D1-D8 against the quoted claims (claims.py). Labels computed here (R15).

FOUND: at least one quote states the prediction and none states the opposite; CONTRADICTED: the reverse; MIXED: both;
NOT FOUND: neither (only 'bears' or no claim). Run: python3 Lossless_Pause/checks/grade_claims.py
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims as C  # noqa: E402

PREDS = {
    'D1': 'bitwise-identical GPU training needs deterministic algorithms; same hardware/software/parallel layout only; '
          'changing GPU count or type breaks it',
    'D2': 'non-determinism sources include atomics, cuDNN algorithm selection, NCCL reduction order',
    'D3': 'LLM inference differences come mainly from batch composition; batch-invariant kernels remove them at a cost',
    'D4': 'serving preempts by swapping the KV cache or dropping and recomputing it; recompute costs compute, swap transfer/memory',
    'D5': 'instruction-level compute preemption on NVIDIA GPUs from Pascal on, with context save/restore',
    'D6': 'transparent checkpoint/restore of a running GPU process exists (cuda-checkpoint + CRIU)',
    'D7': 'an idle but allocated GPU draws a substantial fraction of active power',
    'D8': 'checkpointing large-model training has measurable overhead; asynchronous / in-memory checkpoints reduce it',
}


def main():
    print('Grading of Lossless_Pause/DECLARATION.md D1-D8 against quoted claims (claims.py; quotes verified in verify_claims.txt)')
    print(f'claims: {len(C.CLAIMS)} ({sum(1 for c in C.CLAIMS if c["pred"] == "context")} context)')
    print()
    for d, text in PREDS.items():
        cs = [c for c in C.CLAIMS if c['pred'] == d]
        n = collections.Counter(c['reading'] for c in cs)
        lab = ('MIXED' if n['states'] and n['opposite'] else 'FOUND' if n['states'] else 'CONTRADICTED' if n['opposite']
               else 'NOT FOUND')
        print(f"{d} {lab:12} states {n['states']:2d}, opposite {n['opposite']:2d}, bears {n['bears']:2d}  | {text}")
        for c in cs:
            if c['reading'] in ('states', 'opposite'):
                print(f"     {c['reading']:8} {c['id']:12} {c['source'][:60]} ({c['version'][:30]})")


if __name__ == '__main__':
    main()
