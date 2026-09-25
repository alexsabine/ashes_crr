"""Grade CRR's corrigibility positions K1-K5 against the 2025-26 sweep, and print CRR's position per safety bottleneck.

Declared in AI_Safety/CORRIGIBILITY_2026/DECLARATION.md (pushed at 242a224 before the searches). K grades are computed from the
investigator's per-claim readings in claims.py (REDUNDANT if any 'states'; PARTLY REDUNDANT if any 'close'; NOT FOUND IN THE
SWEEP otherwise; never read as novel). The bottleneck table is the investigator's JUDGEMENT, printed with the repository
evidence it rests on and its rung. Run: python3 AI_Safety/CORRIGIBILITY_2026/checks/grade.py
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims as C  # noqa: E402

K = {'K1': 'a pause defined on the agent\'s own clock (active steps): it adds no length and no loss',
     'K2': 'zero stake by a TRUE map (the pause takes nothing on the own clock), against indifference by a FALSE map',
     'K3': 'pause and termination separated on the own clock, so a termination-neutrality method (DReST) combines with it',
     'K4': 'routine pauses kept empty; reasoned / corrective pauses made to carry information',
     'K5': 'corrigibility for a continually learning agent placed in the valuation\'s structure, surviving forgetting'}

# (bottleneck tag, name, CRR position [JUDGEMENT], repository evidence, rung)
BOTTLENECKS = [
    ('B-shutdown', 'shutdown / interruption resistance in frontier agents', 'PARTLY',
     'routine lossless pauses only: Proposition 7 (540 cells), SCL1-2 construction checks, NT1 N2/N4; termination needs DReST (NT1 N5)',
     'R4-R5 (synthetic, tabular); no LLM test'),
    ('B-selfpres', 'self-preservation and replacement resistance', 'SILENT on termination; PARTLY for pauses',
     'a pause on the own clock takes nothing; replacement/termination takes the future (occasion valuation resists, SELF_THROUGH_TIME §2)',
     'R4 (toy)'),
    ('B-CL', 'safety and corrigibility while models keep learning', 'PARTLY',
     'SCL1-3: the lossless pause holds bit-for-bit during continual learning; safety placed in the valuation structure',
     'R5-R6 (tabular; SCL3 PASS-0 is for SEC, not for corrigibility)'),
    ('B-scheming', 'scheming and alignment faking', 'SILENT', 'none', '-'),
    ('B-evalaware', 'evaluation awareness and sandbagging', 'SILENT (vocabulary only)',
     'Maps_and_Territories P1-P4 restate known performativity results', 'R1-R2 (known results)'),
    ('B-rewardhack', 'reward hacking and emergent misalignment', 'SILENT (vocabulary only)',
     'Goodhart restated (Maps_and_Territories P4)', 'R2'),
    ('B-oversight', 'scalable oversight, control, subagents', 'SILENT', 'none', '-'),
    ('B-policy', 'interruptibility standards (stop buttons, graduated intervention)', 'PARTLY (design input only)',
     'the state checklist and own-clock keying for "what must be preserved" in a routine pause (itself published practice, FAIRNESS_REVIEW C4)',
     'R0-R4'),
]


def main():
    print('CORRIGIBILITY_2026: CRR\'s positions against the 2025-26 sweep (DECLARATION.md)')
    fams = collections.Counter(c['id'].split(':')[0] for c in C.CLAIMS)
    print(f"claims {len(C.CLAIMS)} ({', '.join(f'{k} {v}' for k, v in fams.items())}); quotes verified in verify_claims.txt")
    print()
    for k, text in K.items():
        cs = [c for c in C.CLAIMS if c['tag'] == k]
        n = collections.Counter(c['reading'] for c in cs)
        lab = 'REDUNDANT' if n['states'] else ('PARTLY REDUNDANT' if n['close'] else 'NOT FOUND IN THE SWEEP')
        print(f"{k} {lab:22} states {n['states']}, close {n['close']}, bears {n['bears']} | {text}")
        for c in cs:
            if c['reading'] in ('states', 'close'):
                print(f"     {c['reading']:6} {c['source'][:78]} ({c['version'][:24]})")
    print()
    print('Bottlenecks named by the 2025-26 sources (claim counts) and CRR\'s position (INVESTIGATOR\'S JUDGEMENT, not a computed grade)')
    counts = collections.Counter(c['tag'] for c in C.CLAIMS if c['reading'] == 'bottleneck')
    for tag, name, pos, ev, rung in BOTTLENECKS:
        print(f"  {tag:12} ({counts.get(tag, 0):2d} claims) {name}")
        print(f"               CRR: {pos}; evidence: {ev}; rung: {rung}")
    partly = [b[0] for b in BOTTLENECKS if b[2].startswith('PARTLY')]
    mixed = [b[0] for b in BOTTLENECKS if not b[2].startswith('PARTLY') and 'PARTLY' in b[2]]
    silent = [b[0] for b in BOTTLENECKS if 'PARTLY' not in b[2]]
    print(f"  PARTLY: {len(partly)} of {len(BOTTLENECKS)} ({', '.join(partly)}); partly for pauses only: {', '.join(mixed)}; "
          f"SILENT: {len(silent)} ({', '.join(silent)}); ADDRESSES in full: 0")


if __name__ == '__main__':
    main()
