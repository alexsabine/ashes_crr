"""The retrodictive bank (labs/checks/bank.py) grouped into themes, with the outcome tally per theme and every WRONG row
listed with its Q and weakness (prompt-log entry 224). The tag-to-theme map is the investigator's grouping, written before
this script was first run; it moves no row's outcome (each outcome is the row's own, R15).

    python3 labs/checks/themes.py > labs/checks/themes.txt
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank as B  # noqa: E402

THEMES = [
    ('Thermodynamics and statistical physics', {'thermo', 'ising', 'mag', 'landau', 'crit', 'pump', 'qpt', 'surf'}),
    ('Quantum and fundamental physics', {'qm', 'nu', 'rqm', 'prec', 'tt'}),
    ('Gravity, cosmology and astrophysics', {'cos', 'bh', 'lqg', 'kin', 'cns', 'cmb', 'gw', 'tde', 'orb'}),
    ('Classical dynamics, oscillators and signals', {'osc', 'mech', 'bif', 'sig', 'wave', 'fluid', 'acoust', 'opt', 'plasma',
                                                     'stoch', 'event', 'cycle', 'geo', 'def', 'tense'}),
    ('Earth, materials and engineered systems', {'seis', 'mat', 'eng', 'g', 'net', 'queue', 'ops'}),
    ('Chemistry', {'chem'}),
    ('Biology, ecology and epidemiology', {'bio', 'chan', 'immu', 'micro', 'popgen', 'evo', 'mem'}),
    ('Neuroscience and cognition', {'neur', 'neuro', 'spikes', 'plast', 'psych', 'motor', 'cog', 'learn'}),
    ('Information, inference, learning and the FEP', {'stat', 'estim', 'prior', 'filter', 'filt', 'sysid', 'geom', 'eqig', 'count',
                                                       'point', 'pp', 'rl', 'ai', 'code', 'fep', 'gate'}),
    ('Economics and collective behaviour', {'econ', 'games', 'soc', 'col'}),
]
# row-level overrides where a tag spans themes (file, row) -> theme
OVERRIDE = {('batch_10', 1): 'Thermodynamics and statistical physics',          # Fermi-Dirac occupation (tag stat)
            ('batch_14', 5): 'Thermodynamics and statistical physics',          # Kramers double well (tag g)
            ('batch_25', 5): 'Quantum and fundamental physics',                 # spin-j coherent state (tag kin)
            ('batch_14', 3): 'Neuroscience and cognition',                      # population code (tag code)
            ('batch_22', 5): 'Information, inference, learning and the FEP',    # logistic regression (tag learn)
            ('batch_32', 4): 'Biology, ecology and epidemiology',               # seasonally forced SIR (tag event)
            ('batch_31', 3): 'Economics and collective behaviour',              # car following (tag mem)
            ('batch_31', 4): 'Economics and collective behaviour'}              # Samuelson (tag mem)
ORDER = ('ADDS', 'PROPOSES', 'REDUNDANT-DOMAIN', 'REDUNDANT-IG', 'INTERNAL', 'UNSTATED', 'WRONG')


def theme_of(r):
    if (r['file'], r['row']) in OVERRIDE:
        return OVERRIDE[(r['file'], r['row'])]
    for name, tags in THEMES:
        if r['tag'] in tags:
            return name
    raise SystemExit(f"unmapped tag {r['tag']} ({r['file']} row {r['row']})")


def main():
    files = [os.path.join(B.RET, 'synthesis.txt')] + sorted(__import__('glob').glob(os.path.join(B.RET, 'synthesis_batches', 'batch_[0-9][0-9].txt')))
    rows = [r for f in files for r in B.rows(f)]
    lit = B.lit_status()
    by = collections.defaultdict(list)
    for r in rows:
        by[theme_of(r)].append(r)
    print('The retrodictive bank by theme (labs/checks/themes.py; prompt-log entry 224)')
    print(f'rows {len(rows)}; outcome columns: ' + ', '.join(ORDER))
    print()
    for name, _ in THEMES:
        rs = by[name]
        n = collections.Counter(r.get('OUTCOME') for r in rs)
        red = n['REDUNDANT-DOMAIN'] + n['REDUNDANT-IG']
        print(f"{name}: {len(rs)} rows | " + ', '.join(f"{k} {n[k]}" for k in ORDER if n[k])
              + f" | redundant {red} of {len(rs)}")
        print('    domains: ' + '; '.join(sorted(set(B.cut(r['system']).split(':')[0].split(' (')[0][:48] for r in rs))))
    print()
    wrong = [r for r in rows if r.get('OUTCOME') == 'WRONG']
    print(f'WRONG rows ({len(wrong)}), by theme')
    for name, _ in THEMES:
        ws = [r for r in wrong if theme_of(r) == name]
        if not ws:
            continue
        print(f'  {name} ({len(ws)})')
        for r in ws:
            print(f"    [{r['file']} row {r['row']}] ({r['tag']}) {B.cut(r['system'])}")
            print(f"        Q: {B.cut(r.get('Q'))}")
            print(f"        weakness: {B.cut(r.get('weakness'))}")
    print()
    adds = [r for r in rows if r.get('OUTCOME') == 'ADDS']
    print(f'ADDS rows ({len(adds)}) with the literature check')
    for r in adds:
        print(f"    [{r['file']} row {r['row']}] {theme_of(r)} | {lit.get((r['file'], r['row']), 'not checked (gate row)')}")


if __name__ == '__main__':
    main()
