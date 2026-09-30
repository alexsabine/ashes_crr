"""DR1 summary (Grid_Demand_Response/DECLARATION.md, pushed at e67e8ee): reads the pinned outputs dr_h1.txt ... dr_h8.txt and
dr_data.txt, parses each 'RESULT <id>: ...' line, and prints one row per check: the verdict on Q, the investigator's forecast
(parsed from the declaration's table for H1-H8; for DATA from its 'Declared expectations'), hit or miss (computed), G-ZERO,
G-NEG, and H1's G-POS. Then the battery gate and the counts. Every word printed is parsed or computed; nothing is typed in.
Run: cd /home/user/ashes_crr && uv run python Grid_Demand_Response/checks/dr_summary.py
"""
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CHECKS = os.path.join(ROOT, 'Grid_Demand_Response', 'checks')
DECL = os.path.join(ROOT, 'Grid_Demand_Response', 'DECLARATION.md')
IDS = [f'H{i}' for i in range(1, 9)] + ['DATA']
FILES = {i: (f'dr_{i.lower()}.txt' if i != 'DATA' else 'dr_data.txt') for i in IDS}
MODEL = [f'H{i}' for i in range(1, 9)]


def word(pattern, text):
    m = re.search(pattern, text)
    return m.group(1).lower() if m else None


def forecasts():
    txt = open(DECL, encoding='utf-8').read()
    out = {}
    for hid, fc in re.findall(r'^\| (H\d) \|.*\| (Q (?:holds|fails)[^|]*?) \|\s*$', txt, re.M):
        out[hid] = (word(r'^Q (holds|fails)', fc), fc.strip())
    # DATA: the declaration fixes 'Declared expectations' (ETM joins every event; revenue below 1 % in an ordinary season).
    # Read as a forecast that the scored Q (those expectations) holds, when the section exists.
    m = re.search(r'\*\*Declared expectations\.\*\*\n((?:- .*\n)+)', txt)
    if m:
        out['DATA'] = ('holds', 'declared expectations: ' + ' | '.join(l[2:].strip() for l in m.group(1).splitlines()))
    return out


def own_forecast_word(text):
    """The check's own computed statement on the forecast, where it prints one ('... is right' / '... is wrong')."""
    m = re.findall(r"forecast[^\n]*? is (right|wrong)", text)
    return m[-1] if m else None


def main():
    fc = forecasts()
    print("DR1 summary: the eight model checks and the data application (Grid_Demand_Response/DECLARATION.md, e67e8ee)")
    print("Source of every row: the last 'RESULT <id>:' line of the pinned output named; forecasts parsed from DECLARATION.md.")
    print("CHOICE: DATA's forecast is read from the declaration's 'Declared expectations' (ETM joins every event; revenue below")
    print("  1 % in an ordinary season) as 'Q holds'; G8's interconnection expectation is not scored by dr_data.py.")
    print("CHOICE: hit = the parsed Q word equals the forecast's Q word. 'own' = the check's own printed statement on its forecast")
    print("  (right/wrong), shown as a cross-check; '-' where the check prints none.")
    print()
    rows = {}
    missing = []
    for i in IDS:
        path = os.path.join(CHECKS, FILES[i])
        if not os.path.exists(path):
            missing.append(FILES[i]); continue
        text = open(path, encoding='utf-8').read()
        lines = re.findall(rf'^RESULT {i}: (.*)$', text, re.M)
        if not lines:
            missing.append(FILES[i] + ' (no RESULT line)'); continue
        r = lines[-1]
        rows[i] = dict(q=word(r'^Q (holds|fails|not computable)', r), zero=word(r'G-ZERO (holds|fails)', r),
                       neg=word(r'G-NEG (holds|fails)', r), pos=word(r'G-POS (holds|fails)', r),
                       own=own_forecast_word(text), line=r)
    if missing:
        print(f"missing or unparsed: {missing}")
    hdr = f"  {'check':6} {'Q':15} {'forecast':9} {'hit':5} {'own':6} {'G-ZERO':7} {'G-NEG':7} {'G-POS':7} file"
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    for i in IDS:
        if i not in rows:
            print(f"  {i:6} (no RESULT line)"); continue
        r = rows[i]
        f = fc.get(i, (None, ''))[0]
        r['hit'] = None if (f is None or r['q'] is None) else (r['q'] == f)
        hit = '-' if r['hit'] is None else ('hit' if r['hit'] else 'miss')
        own_ok = '-' if r['own'] is None else r['own']
        pos = r['pos'] if (i == 'H1' and r['pos']) else ('(none)' if i == 'H1' else '-')
        print(f"  {i:6} {str(r['q']):15} {'Q ' + str(f):9} {hit:5} {own_ok:6} {str(r['zero']):7} {str(r['neg']):7} {pos:7} {FILES[i]}")
    print()
    print("Forecasts as declared:")
    for i in IDS:
        if i in fc:
            print(f"  {i}: {fc[i][1]}")
    print()
    # consistency of the computed hit with each check's own printed statement
    incons = [i for i in rows if rows[i]['own'] is not None and rows[i]['hit'] is not None
              and (rows[i]['own'] == 'right') != rows[i]['hit']]
    n_own = sum(rows[i]['own'] is not None for i in rows)
    print(f"cross-check: the computed hit/miss agrees with the check's own right/wrong statement in {n_own - len(incons)} of {n_own} "
          f"checks that print one" + (f"; disagreements: {incons}" if incons else ''))
    print()

    def gate(ids):
        present = [i for i in ids if i in rows]
        z = [i for i in present if rows[i]['zero'] == 'holds']
        n = [i for i in present if rows[i]['neg'] == 'holds']
        p = 'H1' in rows and rows['H1']['pos'] == 'holds'
        ok = len(present) == len(ids) and len(z) == len(ids) and len(n) == len(ids) and p
        return present, z, n, p, ok

    pres, z, n, p, ok = gate(IDS)
    print("BATTERY GATE (rule: G-ZERO holds in all, G-POS holds in H1, G-NEG holds in all -> OPEN, else CLOSED)")
    print(f"  over all {len(IDS)} (H1-H8 and DATA): G-ZERO holds in {len(z)} of {len(IDS)}; G-NEG holds in {len(n)} of {len(IDS)}; "
          f"G-POS in H1: {'holds' if p else 'does not hold'} -> {'OPEN' if ok else 'CLOSED'}")
    pres8, z8, n8, p8, ok8 = gate(MODEL)
    print(f"  over the declaration's eight model checks alone: G-ZERO {len(z8)} of 8; G-NEG {len(n8)} of 8; "
          f"G-POS in H1: {'holds' if p8 else 'does not hold'} -> {'OPEN' if ok8 else 'CLOSED'}")
    print()
    q = [rows[i]['q'] for i in IDS if i in rows]
    qm = [rows[i]['q'] for i in MODEL if i in rows]
    hits = [i for i in IDS if i in rows and rows[i].get('hit')]
    hits8 = [i for i in MODEL if i in rows and rows[i].get('hit')]
    print("COUNTS")
    print(f"  model checks H1-H8: Q holds {qm.count('holds')} of {len(MODEL)} {[i for i in MODEL if i in rows and rows[i]['q'] == 'holds']}; "
          f"fails {qm.count('fails')} {[i for i in MODEL if i in rows and rows[i]['q'] == 'fails']}; "
          f"not computable {qm.count('not computable')}")
    print(f"  forecast hits H1-H8: {len(hits8)} of {len(MODEL)}; misses {[i for i in MODEL if i in rows and rows[i].get('hit') is False]}")
    print(f"  with DATA (9 rows): Q holds {q.count('holds')}, fails {q.count('fails')}; forecast hits {len(hits)} of {len(IDS)}")
    print(f"  gate: {'OPEN' if ok else 'CLOSED'} (all nine), {'OPEN' if ok8 else 'CLOSED'} (the eight)")
    print()
    print("RESULT lines as parsed:")
    for i in IDS:
        if i in rows:
            print(f"  RESULT {i}: {rows[i]['line']}")


if __name__ == '__main__':
    main()
