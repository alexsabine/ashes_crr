"""The global arithmetic, 2026 to 2030 (Attention_Algorithms/DECLARATION.md §5, pushed at 0273a1c before any source).

Time returned per year = users x minutes per day x 365 x f_notif x f_avoid: the hours users would get back IF every feed
held an empty pause (no re-engagement pushes). Conditional on adoption by every platform; not a forecast; not quotable
outside the ledger (R8). Figures are read from the sweep's claims (claims_f3.py, tag 'G', quotes verified in verify.txt).
Run: python3 Attention_Algorithms/checks/global_attention.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims_f3  # noqa: E402

G = {c['id']: c for c in claims_f3.CLAIMS if c['tag'] == 'G'}
F_AVOID = {'low': 0.2, 'high': 0.6}          # ASSUMED (DECLARATION §5): share of notification sessions the user would not have started
F_NOTIF_ASSUMED = {'low': 0.1, 'high': 0.3}  # the declared fallback band, printed as a sensitivity only (a published value was found)


def main():
    users = {2026: G['f3:29'], 2030: G['f3:33']}
    mins_week = G['f3:30']['value']; mpd = mins_week / 7
    fn = G['f3:24']['value']
    fa = {'low': F_AVOID['low'], 'middle': math.sqrt(F_AVOID['low'] * F_AVOID['high']), 'high': F_AVOID['high']}
    print('Attention algorithms: time returned to users if every feed held an empty pause (DECLARATION §5; conditional)')
    print()
    print('[1] Inputs (from the sweep, claims_f3.py)')
    for y, c in users.items():
        print(f"  published users {y}: {c['value']:.4g} ({c['unit']}) | {c['source'][:80]}")
    print('  caution: 2026 counts user identities (not unique people); the 2030 projection counts unique users and is secondary')
    print(f"  published minutes per week per user: {mins_week:g} -> derived minutes per day {mpd:.4f} | {G['f3:30']['source'][:70]}")
    chk = users[2026]['value'] * mpd / 60
    print(f"  cross-check: users x minutes = {chk:.4g} hours/day; published world total {G['f3:31']['value']:.4g} hours/day "
          f"(ratio {chk / G['f3:31']['value']:.4f})")
    print(f"  published f_notif (share of sessions started by a notification): {fn:g} | {G['f3:24']['source'][:80]} (one small study, all apps)")
    print(f"  ASSUMED f_avoid: low {fa['low']}, middle {fa['middle']:.4f} (geometric mean), high {fa['high']}")
    print()
    print('[2] Time returned (conditional on every platform adopting the empty pause)')
    print(f"  {'year':4} {'case':7} {'min/user/day':>13} {'hours/year (world)':>20} {'share of social-media time':>27}")
    for y in (2026, 2030):
        for k in ('low', 'middle', 'high'):
            m = mpd * fn * fa[k]
            hy = users[y]['value'] * m / 60 * 365
            print(f"  {y} {k:7} {m:13.4f} {hy:20.4g} {fn * fa[k]:27.4f}")
    print('  (2030 holds minutes per user at the 2026 figure: no published forecast of time per user was found)')
    print()
    print('[3] Sensitivity: the declared fallback band for f_notif (not the headline)')
    for k in ('low', 'high'):
        m = mpd * F_NOTIF_ASSUMED[k] * fa['middle']
        print(f"  f_notif {F_NOTIF_ASSUMED[k]}: {m:.4f} min/user/day, 2026 {users[2026]['value'] * m / 60 * 365:.4g} hours/year")
    print()
    print('[4] Context from the sweep (not used in the arithmetic)')
    for cid in ('f3:26', 'f3:27', 'f3:10'):
        if cid in G:
            print(f"  {G[cid]['value']:g} {G[cid]['unit']} ({G[cid]['year']}) | {G[cid]['source'][:70]}")


if __name__ == '__main__':
    main()
