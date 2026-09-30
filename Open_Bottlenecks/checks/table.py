"""OB1 stage 1 (Open_Bottlenecks/DECLARATION.md): the harvested bottleneck table from claims_h1-h4.py, with the open test
computed per the declaration's two parts: (1) the quotes are present (role a, b and c claims; computed) and (2) the c claim
shows the best result SHORT of the target (the harvesting agent's reading of the quoted numbers, its 'open' flag; printed).
A bottleneck with all three roles whose c claim shows the target reached is printed 'not shown open (target reached)'.
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
    print('OB1 stage 1: the harvested bottlenecks (DECLARATION.md); open = role a, b and c claims present (computed) and short of target (agent); '
          f'claims {len(claims)}; sources {len({c["url"] for c in claims})}')
    n_open = 0
    for f in FAMS:
        for b in mods[f].BOTTLENECKS:
            roles = collections.Counter(c['role'] for c in claims if c['bottleneck'] == b['id'])
            q = all(roles[r] for r in 'abc'); op = q and bool(b.get('open')); n_open += op
            lab = 'OPEN' if op else ('not shown open (target reached or no shortfall, per the agent)' if q else 'not shown open')
            print(f"\n{b['id']:7} {lab} | {b['name']}")
            print(f"        claims a {roles['a']}, b {roles['b']}, c {roles['c']}, d {roles['d']}; benchmark: {b.get('benchmark', '')}")
            print(f"        best {b.get('best', '')} against target {b.get('target', '')}; gap: {b.get('gap_note', '')}")
            print(f"        CPU-testable: {'yes' if b.get('cpu_testable') else 'no'} ({b.get('cpu_note', '')})")
            for a in b.get('assumptions', []):
                print(f"        assumes: {a}")
    print(f"\nopen bottlenecks: {n_open} of {sum(len(m.BOTTLENECKS) for m in mods.values())}")


if __name__ == '__main__':
    main()
