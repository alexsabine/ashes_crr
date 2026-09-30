"""Grade the declared positions G1-G9 of Grid_Demand_Response/DECLARATION.md section 1 against the DR1 sweep.

Declared in Grid_Demand_Response/DECLARATION.md (pushed at e67e8ee before any source, code or data). The claims, their quotes and
the per-claim readings (states / close / bears / contradicts, the grading agent's, for the investigator's review) are in
claims.py; the quotes are checked verbatim against the fetched texts by verify.py (verify.txt).

The rule (declaration section 1, as instructed for this script):
  MIXED                  if any claim 'states' and any claim 'contradicts';
  REDUNDANT              otherwise, if any claim 'states';
  PARTLY REDUNDANT       otherwise, if any claim is 'close';
  NOT FOUND IN THE SWEEP otherwise.
  ADDRESSED              for the positions that are questions the sources answer (G7, G8); the answer is the rule's grade.
Every grade word and every hit/miss below is computed from the claim counts. "Not found" is never read as "novel".
Deterministic; stdlib only. Run: cd /home/user/ashes_crr && uv run python Grid_Demand_Response/checks/grade.py
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims as C  # noqa: E402

READINGS = ('states', 'close', 'bears', 'contradicts')

# The declaration's table (section 1), verbatim, with its expected grades.
POSITIONS = [
    ('G1', None, 'AI training and data-centre load is already used for demand response in the field', 'REDUNDANT'),
    ('G2', None, "a training job's cost of a curtailment is its lost work plus restart plus deadline pressure (its opportunity "
                 "cost), and this sets the payment it needs", 'PARTLY REDUNDANT'),
    ('G3', None, "a lossless pause (checkpoint and resume, nothing lost) makes the job's curtailment cost about the restart "
                 "overhead", 'PARTLY REDUNDANT'),
    ('G4', 'extension', "a contract that extends the job's deadline by the curtailed time (stop-the-clock) elicits full "
                        "participation at the restart cost", 'NOT FOUND IN THE SWEEP'),
    ('G4', 'tiers', 'industry instead uses slowdown tiers', 'REDUNDANT'),
    ('G5', None, 'flexible AI load carries grid-safety risks: synchronized ramps and power swings, and a rebound peak when '
                 'paused jobs resume together', 'REDUNDANT'),
    ('G6', None, 'a lossless pause needs a checkpoint save before the power drops, which limits the demand-response products '
                 'it can meet (response-time requirements)', 'PARTLY REDUNDANT'),
    ('G7', None, 'demand-response payments are small against the compute cost of a training fleet', 'MIXED'),
    ('G8', None, 'the main commercial value of flexible AI load is faster or larger grid interconnection, not event payments',
     'REDUNDANT'),
    ('G9', None, 'power capping or throttling (running slower) is an alternative to pausing, with different energy and grid '
                 'effects', 'REDUNDANT'),
]
EXPECTED_NOTE = {'G7': 'expected: small, with exceptions in scarcity events'}
ADDRESSED = ('G7', 'G8')  # positions that are questions the sources answer (as instructed)


def rule(n):
    """The declared rule on reading counts n (a Counter)."""
    if n['states'] and n['contradicts']:
        return 'MIXED'
    if n['states']:
        return 'REDUNDANT'
    if n['close']:
        return 'PARTLY REDUNDANT'
    return 'NOT FOUND IN THE SWEEP'


def select(tag, part, key='reading'):
    cs = [c for c in C.CLAIMS if c['tag'] == tag and (part is None or c.get('part') == part)]
    return cs, collections.Counter(c[key] for c in cs)


def label(tag, part):
    return tag if part is None else f'{tag}-{part}'


def grade_all(key):
    out = []
    for tag, part, text, expected in POSITIONS:
        cs, n = select(tag, part, key)
        answer = rule(n)
        grade = 'ADDRESSED' if tag in ADDRESSED else answer
        out.append((tag, part, text, expected, cs, n, answer, grade, answer == expected))
    return out


def main():
    print('DR1 section 1: positions G1-G9 graded against the sweep (Grid_Demand_Response/DECLARATION.md, pushed at e67e8ee)')
    fam = collections.Counter(c['family'] for c in C.CLAIMS)
    rd = collections.Counter(c['reading'] for c in C.CLAIMS)
    n_q = sum(len(c['quote']) for c in C.CLAIMS)
    print(f"claims {len(C.CLAIMS)} ({', '.join(f'{k} {fam[k]}' for k in sorted(fam))}); quotes {n_q}; "
          f"readings {', '.join(f'{r} {rd[r]}' for r in READINGS)}; quotes checked in verify.txt")
    print("readings by: grading agent, for the investigator's review; the families' proposed readings are graded in the "
          "sensitivity block below")
    print('CHOICE: rule order MIXED (states and contradicts) > REDUNDANT (states) > PARTLY REDUNDANT (close) > NOT FOUND IN THE '
          'SWEEP; close + contradicts without states is not MIXED under this rule (the contradicting count is printed)')
    print('CHOICE: G4 is graded in two parts (the extension; the tiers) because the declaration gives it two expected grades; '
          'each G4 claim carries its part')
    print('CHOICE: G7 and G8 are positions that are questions the sources answer; their grade is ADDRESSED, the answer is the '
          "rule's grade, and hit/miss compares the answer with the declared expected grade")
    g4_bad = [c['id'] for c in C.CLAIMS if c['tag'] == 'G4' and c.get('part') not in ('extension', 'tiers')]
    print(f"G4 claims without a part: {len(g4_bad)}{' (' + ', '.join(g4_bad) + ')' if g4_bad else ''}")
    print('CHOICE: hit = the computed grade (for G7, G8 the answer) equals the declared expected grade string exactly')
    print()

    rows = grade_all('reading')
    for tag, part, text, expected, cs, n, answer, grade, hit in rows:
        g = f'ADDRESSED (answer: {answer})' if tag in ADDRESSED else grade
        exp = expected + (f' ({EXPECTED_NOTE[tag]})' if tag in EXPECTED_NOTE else '')
        print(f"{label(tag, part):12} {g}")
        print(f"{'':12} position: {text}")
        print(f"{'':12} claims {len(cs)}: states {n['states']}, close {n['close']}, bears {n['bears']}, "
              f"contradicts {n['contradicts']}")
        print(f"{'':12} expected (declaration): {exp}; {'hit' if hit else 'miss'}")
        for c in cs:
            if c['reading'] != 'bears':
                print(f"{'':14}{c['reading']:11} {c['id']:6} {c['source'][:80]} [{c['version'][:40]}]")
        bears = [c['id'] for c in cs if c['reading'] == 'bears']
        if bears:
            print(f"{'':14}{'bears':11} {', '.join(bears)}")
        print()

    pooled_cs, pooled_n = select('G4', None)
    print(f"G4 pooled (both parts as one position, for comparison only): {rule(pooled_n)} "
          f"(states {pooled_n['states']}, close {pooled_n['close']}, bears {pooled_n['bears']}, "
          f"contradicts {pooled_n['contradicts']})")
    hits = sum(r[8] for r in rows)
    print(f'hits against the declared expected grades: {hits} of {len(rows)} '
          f"(misses: {', '.join(label(r[0], r[1]) for r in rows if not r[8]) or 'none'})")
    print('never read as novel: NOT FOUND IN THE SWEEP means only that no source reached in this sweep states the position '
          'or comes close to it; it is not a finding of novelty (declaration, Status)')
    print()

    print("Sensitivity: the same rule on the families' proposed readings ('proposed_reading')")
    prow = grade_all('proposed_reading')
    for (tag, part, _, expected, _, n, answer, grade, hit), mine in zip(prow, rows):
        g = f'ADDRESSED (answer: {answer})' if tag in ADDRESSED else grade
        same = 'same as above' if answer == mine[6] else f'differs from above ({mine[6]})'
        print(f"  {label(tag, part):12} {g:40} states {n['states']:2}, close {n['close']:2}, bears {n['bears']:2}, "
              f"contradicts {n['contradicts']:2}; {'hit' if hit else 'miss'}; {same}")
    phits = sum(r[8] for r in prow)
    print(f'  hits on the proposed readings: {phits} of {len(prow)}')
    moved = collections.Counter((c['proposed_reading'], c['reading']) for c in C.CLAIMS
                                if c['proposed_reading'] != c['reading'])
    print(f'  readings changed by the grading agent: {sum(moved.values())} of {len(C.CLAIMS)} '
          f"({', '.join(f'{a} -> {b} {k}' for (a, b), k in sorted(moved.items()))})")
    base = {(r[0], r[1]): r[6] for r in rows}
    flips = []
    for c in C.CLAIMS:
        if c['proposed_reading'] == c['reading'] or not c['tag'].startswith('G'):
            continue
        part = c.get('part')
        cs, _ = select(c['tag'], part)
        n = collections.Counter(c['proposed_reading'] if x is c else x['reading'] for x in cs)
        if rule(n) != base[(c['tag'], part)]:
            flips.append(f"{c['id']} ({label(c['tag'], part)}: {c['reading']} -> {c['proposed_reading']} gives {rule(n)})")
    print(f'  single-claim sensitivity: changed readings whose proposed reading, substituted alone, changes the grade: '
          f'{len(flips)}')
    for f in flips:
        print(f'    {f}')
    print()

    defs = [c for c in C.CLAIMS if c['tag'].startswith('DEF-')]
    print(f'Definition claims (not graded): {len(defs)}')
    for c in defs:
        print(f"  {c['tag']:22} {c['id']:6} {c['source'][:90]}")
    other = sorted({c['tag'] for c in C.CLAIMS} - {p[0] for p in POSITIONS} - {c['tag'] for c in defs})
    print(f"tags outside G1-G9 and DEF-*: {', '.join(other) if other else 'none'}")


if __name__ == '__main__':
    main()
