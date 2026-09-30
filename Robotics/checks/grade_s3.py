"""ROB1 stage 3 (Robotics/DECLARATION.md): grade each DISAGREES candidate C-R1..C-R3 (Robotics/CRR_READING.md) against its
targeted prior-art sweeps (two independent searchers per candidate: claims_s3_r{1,2,3}a.py, searcher A, and
claims_s3_r{1,2,3}b.py, searcher B, whose READING_CHECKS check each of A's readings; dossiers
docs/citations/rob1_s3_r{1,2,3}{a,b}_2026-09-30.md; quotes checked in verify_s3.txt).

A claim counts only if it is verified: it has at least one quote and every one of its quotes is found by
Robotics/checks/verify_s3.py (its matcher is imported, not copied; the raw texts under /tmp/claude-0/rob_s3/ are read).
The effective reading of a claim is its searcher's reading, except that a 'states' reading of searcher A which searcher B's
READING_CHECKS does not agree with counts as 'close'. A disagreement with any other reading is printed and changes nothing
(the rule names 'states' only).

The grade per candidate and position (P1, P2, P3, as each claims module's docstring states them), OB1's rule
(Open_Bottlenecks/checks/grade_s3.py) with a MIXED grade added, applied in this order (the first that applies):
  MIXED                    a verified claim reads 'states' and another reads 'contradicts';
  REDUNDANT                a verified claim reads 'states';
  PARTLY REDUNDANT         a verified claim reads 'close';
  NOT FOUND IN THE SWEEP   otherwise ('bears' and a lone 'contradicts' do not lift a position above this).
The candidate's grade (the rule fixed by the caller before this script ran):
  REDUNDANT                P1 is REDUNDANT;
  PARTLY REDUNDANT         P1 is PARTLY REDUNDANT, or P1 is NOT FOUND IN THE SWEEP and P2 or P3 is close (graded REDUNDANT,
                           PARTLY REDUNDANT or MIXED: a verified 'states' or 'close' claim exists there);
  NOT FOUND IN THE SWEEP   otherwise;
  a MIXED P1 is outside the rule and is printed as such, for the investigator.
Going on to a stage-4a declaration (Robotics/DECLARATION.md stage 3): NOT FOUND IN THE SWEEP goes on; PARTLY REDUNDANT goes on
only if the missing part is the part CRR predicts; the script names the missing part (the positions short of REDUNDANT and the
closest claims) and prints 'investigator to decide'; REDUNDANT does not go on. 'Not found' is never 'novel'.
Printed beside each grade (information, never a change to it): the grade from each searcher's claims alone, and whether it
survives leaving out any one source (by url).
Deterministic, stdlib only. Run: python3 Robotics/checks/grade_s3.py [raw-root]
"""
import collections
import importlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_s3  # noqa: E402

CANDS = [
    ('r1', 'C-R1 a phase-keyed stop for a dynamically balancing robot (r4-B4; A3, Proposition 7)', {
        'P1': 'phase-dependent timing or shaping of a stop for a legged or humanoid robot is published',
        'P2': 'it is shown to reduce worst-case or mean stopping distance, time or falls against a phase-independent stop',
        'P3': 'it appears in a standard, a standards proposal or an industrial safety function'}),
    ('r2', 'C-R2 an own-progress budget for out-of-contact exploration (r1-B5; A1\', H-L5, Proposition 7)', {
        'P1': 'a return or rendezvous decision triggered by information or progress accumulated since the last contact is '
              'published',
        'P2': 'it is compared with a fixed time budget and shown better (more coverage, information delivered or artifacts, at '
              'equal loss or return failure where modelled)',
        'P3': 'it is used in a fielded system (DARPA SubT teams, mine-mapping drones, field deployments)'}),
    ('r3', 'C-R3 progress-indexed runtime failure detection (r4-B3; H-L5, A1\')', {
        'P1': 'progress- or phase-indexed failure detection or conformal calibration for robot policies is published',
        'P2': 'it is shown to detect earlier or more accurately than step-indexed thresholds',
        'P3': 'the step-index mismatch (rollouts of different speed) is named as a problem'}),
]
POSITIONS = ('P1', 'P2', 'P3')
READINGS = ('states', 'close', 'bears', 'contradicts')
ORDER = ('NOT FOUND IN THE SWEEP', 'PARTLY REDUNDANT', 'REDUNDANT', 'MIXED')


def grade_position(readings):
    n = collections.Counter(readings)
    if n['states'] and n['contradicts']:
        return 'MIXED'
    if n['states']:
        return 'REDUNDANT'
    if n['close']:
        return 'PARTLY REDUNDANT'
    return 'NOT FOUND IN THE SWEEP'


def grade_candidate(g):
    if g['P1'] == 'MIXED':
        return 'MIXED at P1 (outside the rule)'
    if g['P1'] == 'REDUNDANT':
        return 'REDUNDANT'
    if g['P1'] == 'PARTLY REDUNDANT':
        return 'PARTLY REDUNDANT'
    if any(g[p] in ('REDUNDANT', 'PARTLY REDUNDANT', 'MIXED') for p in ('P2', 'P3')):
        return 'PARTLY REDUNDANT'
    return 'NOT FOUND IN THE SWEEP'


def short(c):
    m = re.match(r'^(.*?"[^"]*")', c['source'])
    s = m.group(1) if m else c['source']
    return s if len(s) <= 150 else s[:147] + '...'


def version_head(v):
    """The version string up to its first ' (' or ';' outside parentheses (the full string is in the claims module)."""
    depth = 0
    for i, ch in enumerate(v):
        if ch == '(' and depth == 0 and i > 0 and v[i - 1] == ' ':
            return v[:i - 1]
        if ch == ';' and depth == 0:
            return v[:i]
        depth += (ch == '(') - (ch == ')')
    return v


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else verify_s3.ROOT
    mods = verify_s3.load()
    claims = [c for f in verify_s3.MODULES for c in mods[f].CLAIMS]
    status, _ = verify_s3.claim_status(claims, root)
    ok = {cid: bool(st) and all(s == 'PASS' for s in st) for cid, st in status.items()}
    n_q = sum(len(st) for st in status.values())
    n_qf = sum(s == 'PASS' for st in status.values() for s in st)
    print('ROB1 stage 3: targeted prior art per candidate (Robotics/DECLARATION.md stage 3; Robotics/CRR_READING.md); '
          'grades computed from verified claims only')
    print(f'root: {root}')
    print(f'claims {len(claims)} (verified {sum(ok.values())}); quotes {n_q} (found {n_qf}); '
          f'sources {len({c["url"] for c in claims})}')
    print('position rule: MIXED if a verified claim states and another contradicts; else REDUNDANT if any states; else PARTLY '
          'REDUNDANT if any close; else NOT FOUND IN THE SWEEP')
    print("effective reading: A's 'states' that B's READING_CHECKS does not agree with counts as 'close'")
    print('candidate rule: REDUNDANT if P1 REDUNDANT; PARTLY REDUNDANT if P1 PARTLY REDUNDANT, or P1 NOT FOUND and P2 or P3 '
          'close; else NOT FOUND IN THE SWEEP')
    print("not found is never novel")
    summary = []
    for cid, name, pos_text in CANDS:
        a, b = mods[cid + 'a'], mods[cid + 'b']
        cl = [c for c in a.CLAIMS + b.CLAIMS]
        checks = {r['claim_id']: r for r in getattr(b, 'READING_CHECKS', [])}
        eff, why = {}, {}
        for c in cl:
            r = c['reading']
            chk = checks.get(c['id'])
            if chk is not None and not chk['agree'] and r == 'states':
                eff[c['id']] = 'close'
                why[c['id']] = "A 'states', B disagrees -> close"
            else:
                eff[c['id']] = r
                if chk is None:
                    why[c['id']] = ("searcher B's claim; not cross-checked" if c['id'].startswith(cid + 'b')
                                    else "searcher A's claim; no check by B")
                else:
                    why[c['id']] = 'B agrees' if chk['agree'] else f"B disagrees with '{r}' (rule names states only; kept)"
        a_ids = [c['id'] for c in a.CLAIMS]
        n_chk = sum(i in checks for i in a_ids)
        dis = [i for i in a_ids if i in checks and not checks[i]['agree']]
        unver = [c['id'] for c in cl if not ok[c['id']]]
        print(f'\n==== {name}')
        print(f"   claims: A {len(a.CLAIMS)}, B {len(b.CLAIMS)} (verified {sum(ok[c['id']] for c in cl)}; unverified "
              f"{len(unver)}{' ' + ', '.join(unver) if unver else ''}); sources {len({c['url'] for c in cl})}")
        print(f"   B's READING_CHECKS: {n_chk} of A's {len(a_ids)} claims checked; agree {n_chk - len(dis)}; disagree "
              f"{len(dis)}" + (': ' + '; '.join(f"{i} (A {next(c['reading'] for c in a.CLAIMS if c['id'] == i)} -> "
                                                   f"counted {eff[i]})" for i in dis) if dis else ''))
        g = {}
        for p in POSITIONS:
            vc = [c for c in cl if c['position'] == p and ok[c['id']]]
            n = collections.Counter(eff[c['id']] for c in vc)
            g[p] = grade_position([eff[c['id']] for c in vc])
            print(f'\n   {p} {pos_text[p]}')
            print(f"      verified claims {len(vc)} (A {sum(c['id'].startswith(cid + 'a') for c in vc)}, "
                  f"B {sum(c['id'].startswith(cid + 'b') for c in vc)}): "
                  + ', '.join(f'{r} {n[r]}' for r in READINGS) + f' -> {g[p]}')
            for r in READINGS:
                ids = [c['id'] for c in vc if eff[c['id']] == r]
                if ids:
                    print(f"      {r:11} {', '.join(ids)}")
            decisive = {'MIXED': ('states', 'contradicts'), 'REDUNDANT': ('states',),
                        'PARTLY REDUNDANT': ('close',)}.get(g[p], ())
            if decisive:
                print(f"      decisive ({' and '.join(decisive)}):")
            for c in vc:
                if eff[c['id']] in decisive:
                    print(f"        {c['id']:7} {eff[c['id']]:11} {short(c)}; {version_head(c['version'])} "
                          f"[{why[c['id']]}]")
                    if c['id'] in checks:
                        print(f"                B's check: {checks[c['id']]['note']}")
            alone = {s: grade_position([eff[c['id']] for c in vc if c['id'].startswith(cid + s)]) for s in 'ab'}
            urls = sorted({c['url'] for c in vc})
            loso = {}
            for u in urls:
                gu = grade_position([eff[c['id']] for c in vc if c['url'] != u])
                if gu != g[p]:
                    loso[u] = gu
            print(f"      searcher A's claims alone (B's checks applied): {alone['a']}; searcher B's alone: {alone['b']}")
            if not loso:
                print(f'      leave-one-source-out ({len(urls)} sources): the grade holds for every source left out')
            else:
                for u, gu in sorted(loso.items()):
                    hid = ', '.join(c['id'] for c in vc if c['url'] == u)
                    print(f'      leave-one-source-out: without {hid} ({u}) the grade is {gu}')
        cg = grade_candidate(g)
        short_of = [f'{p} {g[p]}' for p in POSITIONS if g[p] != 'REDUNDANT']
        print(f"\n   candidate grade: {cg} (P1 {g['P1']}, P2 {g['P2']}, P3 {g['P3']})")
        if cg == 'NOT FOUND IN THE SWEEP':
            on = 'yes (NOT FOUND IN THE SWEEP goes on)'
        elif cg == 'PARTLY REDUNDANT':
            closest = [c['id'] for c in cl if ok[c['id']] and c['position'] == 'P1' and eff[c['id']] == 'close']
            print(f"   missing part: {'; '.join(short_of)}; P1 is not stated by any verified claim"
                  + (f" (closest P1 claims: {', '.join(closest)})" if closest else ' (no close P1 claim)')
                  + '; whether the missing part is the part CRR predicts: investigator to decide')
            on = 'investigator to decide (PARTLY REDUNDANT; goes on only if the missing part is the part CRR predicts)'
        elif cg == 'REDUNDANT':
            if short_of:
                print(f"   positions short of REDUNDANT (information; the candidate's grade rests on P1): {'; '.join(short_of)}")
            on = 'no (P1 REDUNDANT: the mechanism is published)'
        else:
            on = 'investigator to decide (MIXED at P1 is outside the rule)'
        print(f'   goes on to a stage-4a declaration: {on}')
        summary.append((name.split(' ')[0], cg, g, on))
    print('\nsummary')
    for n, cg, g, on in summary:
        print(f"   {n}: {cg} (P1 {g['P1']}; P2 {g['P2']}; P3 {g['P3']}); goes on: {on.split(' (')[0]}")
    going = [n for n, cg, g, on in summary if on.startswith('yes')]
    decide = [n for n, cg, g, on in summary if on.startswith('investigator')]
    print(f"candidates going on: {', '.join(going) or 'none'}; for the investigator to decide: {', '.join(decide) or 'none'}")
    if not going and not decide:
        print('stop condition (Robotics/DECLARATION.md, R12): every candidate published; stage 4a does not run; the prior art '
              'is named in the decisive claims above')


if __name__ == '__main__':
    main()
