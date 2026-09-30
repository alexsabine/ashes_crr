"""OB1 stage 1 (Open_Bottlenecks/DECLARATION.md): the harvested bottleneck table from claims_h1-h4.py, with the open test
computed (open iff the bottleneck has role a, b and c claims), per-role claim counts and the frontier's assumptions.
Deterministic, stdlib only; does not read the raw source texts. Run: python3 Open_Bottlenecks/checks/table.py
"""
import collections
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
FAMS = ('h1', 'h2', 'h3', 'h4')


def main():
    mods = {f: importlib.import_module(f'claims_{f}') for f in FAMS}
    claims = [c for m in mods.values() for c in m.CLAIMS]
    print('OB1 stage 1: the harvested bottlenecks (DECLARATION.md); open = role a, b and c claims present (computed); '
          f'claims {len(claims)}; sources {len({c["url"] for c in claims})}')
    n_open = 0
    for f in FAMS:
        for b in mods[f].BOTTLENECKS:
            roles = collections.Counter(c['role'] for c in claims if c['bottleneck'] == b['id'])
            op = all(roles[r] for r in 'abc'); n_open += op
            flag = '' if op == bool(b.get('open')) else f"  (agent's flag {b.get('open')} differs from the computed test)"
            print(f"\n{b['id']:7} {'OPEN' if op else 'not shown open':15} {b['name']}{flag}")
            print(f"        claims a {roles['a']}, b {roles['b']}, c {roles['c']}, d {roles['d']}; benchmark: {b.get('benchmark', '')}")
            print(f"        best {b.get('best', '')} against target {b.get('target', '')}; gap: {b.get('gap_note', '')}")
            print(f"        CPU-testable: {'yes' if b.get('cpu_testable') else 'no'} ({b.get('cpu_note', '')})")
            for a in b.get('assumptions', []):
                print(f"        assumes: {a}")
    print(f"\nopen bottlenecks: {n_open} of {sum(len(m.BOTTLENECKS) for m in mods.values())}")


if __name__ == '__main__':
    main()
