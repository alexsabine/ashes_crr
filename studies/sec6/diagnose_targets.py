"""Why the frozen SEC6 loader excluded every carrier (POST HOC diagnostic after the data step; decides nothing, re-scores nothing).

For each SEC6 carrier, with the FROZEN reader (runs/sec6/frozen/scl3_score.py: read_arff, _attr, _parse_rows, imported, not
copied or edited): the target attribute's declared ARFF kind; the number of distinct non-missing target values; the rows the
frozen _parse_rows drops (its own count); and, to separate the two causes, the rows that would be dropped for a missing or
unreadable FEATURE value alone (the target ignored). A carrier whose target is declared STRING loses every row in the frozen
parser (float() of a class name raises), whatever its features.

Run: uv run python studies/sec6/diagnose_targets.py > runs/sec6/diagnose_targets.txt
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "runs" / "sec6" / "frozen"))
import scl3_score as L  # noqa: E402

IDS = [46584, 46593, 46597, 46603, 46652, 46653, 46676, 46686, 46708, 46721, 46737, 46762]
RAW = ROOT / "data" / "raw" / "openml"


def main():
    print("SEC6 carriers: the target's declared ARFF kind and where the frozen loader's rows go (POST HOC; no verdict)")
    print(f"{'id':>6} {'dataset':40} {'target':24} {'kind':8} {'distinct':>8} {'rows':>7} {'dropped (frozen)':>16} {'dropped by features alone':>25} {'features used':>13}")
    kinds = {}
    for did in IDS:
        stem = next(p.stem for p in RAW.glob(f"{did}_*.arff"))
        desc = json.loads((RAW / f"{stem}.json").read_text())["data_set_description"]
        target = desc["default_target_attribute"]
        drop = set()
        for key in ("row_id_attribute", "ignore_attribute"):
            v = desc.get(key)
            if v: drop |= set(v if isinstance(v, list) else [v])
        attrs, rows = L.read_arff(RAW / f"{stem}.arff")
        names = [a[0] for a in attrs]; ti = names.index(target); kind = attrs[ti][1]
        _, _, dropped, used = L._parse_rows(attrs, rows, target, drop)
        cols = [j for j, (nm, k, _) in enumerate(attrs) if j != ti and nm not in drop and k in ("numeric", "nominal")]
        maps = {j: {v: i for i, v in enumerate(attrs[j][2])} for j in cols if attrs[j][1] == "nominal"}
        feat_drop = 0; tv = set()
        for r in rows:
            if len(r) == len(attrs) and r[ti] not in ("?", ""): tv.add(r[ti])
            try:
                if len(r) != len(attrs): raise ValueError
                for j in cols:
                    v = r[j]
                    if v in ("?", ""): raise ValueError
                    x = float(maps[j][v]) if j in maps else float(v)
                    if not math.isfinite(x): raise ValueError
            except (ValueError, KeyError):
                feat_drop += 1
        kinds[kind] = kinds.get(kind, 0) + 1
        print(f"{did:6d} {stem.split('_', 1)[1][:40]:40} {target[:24]:24} {kind:8} {len(tv):8d} {len(rows):7d} {dropped:16d} {feat_drop:25d} {len(used):13d}")
    print("\ntarget kinds over the 12: " + ", ".join(f"{k} {n}" for k, n in sorted(kinds.items())))
    print("a carrier whose 'dropped (frozen)' equals its rows while 'dropped by features alone' is smaller lost its rows to the target, not to its features")


if __name__ == "__main__":
    main()
