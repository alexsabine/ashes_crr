"""ROB1 stages 1 and 1b (Robotics/DECLARATION.md): the harvested bottleneck table from claims_r1-r5.py, with the double
check from claims_r1x-r5x.py, and the label COMPUTED by the declaration's rule from the two agents' VERIFIED claims.

A claim counts only if it is verified: it has at least one quote and every one of its quotes is FOUND by
Robotics/checks/verify.py (its matcher is imported, not copied; the raw texts under /tmp/claude-0/rob_src/ are read).
A role-x claim is CONTRARY to a bottleneck when its `refutes` names that bottleneck and its `contrary` flag is true; a
role-x claim with `contrary` false is a re-check of the harvester's reading and bears on B-c only (the x modules'
docstrings), so it is counted and listed but never changes a label.

The label, applied in this order (the first that applies):
  'not shown open'       a verified role a, b or c claim is missing;
  NOT OPEN               a verified contrary role-x claim has shows_target_reached true, or the harvester's `open` flag is false;
  CONTESTED              at least one verified contrary role-x claim exists (none shows the target reached);
  OPEN (double-checked)  role a, b and c claims verified, the harvester's `open` flag true, and no verified contrary role-x claim.
`open` is the harvesting agent's reading of the quoted numbers (best short of target); shows_target_reached is the
double-checking agent's reading of its quote against the named metric; both are printed with the ids they rest on.
Deterministic, stdlib only. Run: python3 Robotics/checks/table.py [raw-root]
"""
import collections
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify  # noqa: E402

FAMS = ('r1', 'r2', 'r3', 'r4', 'r5')
LABELS = ('OPEN (double-checked)', 'CONTESTED', 'NOT OPEN', 'not shown open')


def label(roles, open_flag, contrary, reached):
    if not all(roles[r] for r in 'abc'):
        return 'not shown open', 'role ' + ', '.join(r for r in 'abc' if not roles[r]) + ' missing'
    if reached:
        return 'NOT OPEN', 'verified contrary claim shows the target reached: ' + ', '.join(reached)
    if not open_flag:
        return 'NOT OPEN', "harvester's open flag false"
    if contrary:
        return 'CONTESTED', 'verified contrary claims, none shows the target reached: ' + ', '.join(contrary)
    return 'OPEN (double-checked)', 'no verified contrary claim'


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else verify.ROOT
    hmods = {f: importlib.import_module(f'claims_{f}') for f in FAMS}
    xmods = {f: importlib.import_module(f'claims_{f}x') for f in FAMS}
    claims = verify.load_claims()
    status, _ = verify.claim_status(claims, root)
    ok = {cid: bool(st) and all(s == 'FOUND' for s in st) for cid, st in status.items()}
    n_q = sum(len(st) for st in status.values())
    n_qf = sum(s == 'FOUND' for st in status.values() for s in st)
    print('ROB1 stages 1 and 1b: the harvested bottlenecks and the double check (DECLARATION.md); label computed from '
          'verified claims only')
    print(f'root: {root}')
    print(f'claims {len(claims)} (verified {sum(ok.values())}); quotes {n_q} (found {n_qf}); '
          f'sources {len({c["url"] for c in claims})}')
    tally = collections.Counter()
    fam_tally = {f: collections.Counter() for f in FAMS}
    for f in FAMS:
        checks = {ch['bottleneck']: ch for ch in xmods[f].CHECKS}
        print(f'\n==== family {f.upper()} ({len(hmods[f].BOTTLENECKS)} bottlenecks; claims_{f}.py, claims_{f}x.py)')
        for b in hmods[f].BOTTLENECKS:
            own = [c for c in claims if c['bottleneck'] == b['id'] and c['role'] != 'x']
            xs = [c for c in claims if c['role'] == 'x' and c['refutes'] == b['id']]
            roles = collections.Counter(c['role'] for c in own if ok[c['id']])
            unver = [c['id'] for c in own + xs if not ok[c['id']]]
            contrary = [c['id'] for c in xs if ok[c['id']] and c['contrary']]
            reached = [c['id'] for c in xs if ok[c['id']] and c['contrary'] and c['shows_target_reached']]
            recheck = [c['id'] for c in xs if ok[c['id']] and not c['contrary']]
            lab, why = label(roles, bool(b.get('open')), contrary, reached)
            tally[lab] += 1
            fam_tally[f][lab] += 1
            print(f"\n{b['id']:6} {lab} | {b['name']}")
            print(f'       why: {why}')
            print(f"       roles (verified claims): a {roles['a']}, b {roles['b']}, c {roles['c']}, d {roles['d']}; "
                  f"x {sum(ok[c['id']] for c in xs)} (contrary {len(contrary)}, target reached {len(reached)}, "
                  f"re-check {len(recheck)}); unverified {len(unver)}{' ' + ', '.join(unver) if unver else ''}")
            print(f"       harvester open flag: {bool(b.get('open'))}")
            print(f"       benchmark: {b.get('benchmark', '')}")
            print(f"       best: {b.get('best', '')}")
            print(f"       target: {b.get('target', '')}")
            print(f"       gap: {b.get('gap_note', '')}")
            print(f"       CPU-testable: {'yes' if b.get('cpu_testable') else 'no'} ({b.get('cpu_note', '')})")
            for a in b.get('assumptions', []):
                print(f'       assumes: {a}')
            ch = checks.get(b['id'])
            if ch is None:
                print('       double check: NONE RECORDED')
                continue
            print(f"       double check ({len(ch.get('searched', []))} searches listed): {ch.get('finding', '')}")
            print(f"       contrary: {', '.join(contrary) or 'none'}; re-checks: {', '.join(recheck) or 'none'}")
            errs = ch.get('harvester_errors', [])
            print(f'       harvester errors found by the double check: {len(errs)}')
            for e in errs:
                print(f'         - {e}')
    print('\nlabels per family:')
    print('  family ' + ' | '.join(LABELS) + ' | total')
    for f in FAMS:
        print(f'  {f.upper():6} ' + ' | '.join(str(fam_tally[f][lab]) for lab in LABELS) +
              f' | {sum(fam_tally[f].values())}')
    print(f'  {"all":6} ' + ' | '.join(str(tally[lab]) for lab in LABELS) + f' | {sum(tally.values())}')
    print('\nlabel totals: ' + '; '.join(f'{lab} {tally[lab]}' for lab in LABELS) +
          f'; bottlenecks {sum(tally.values())}')


if __name__ == '__main__':
    main()
