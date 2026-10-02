"""PRE-PHOENIX INTERPRETIVE AUDIT — NO VERDICTS ALTERED.

Label-leak scan of every OpenML ARFF in data/raw/openml (all SEEN; nothing held-out is opened). Prompted by Embers'
report that SEC4-1's carrier cardiotocography (OpenML 1466) carries one-hot copies of its class
([Embers@de6c05a] audits/sec5/README.md:52-61; Pre_Phoenix_Audit/notes/EMBERS_ADDENDUM_de6c05a.md §1.6 item 3).

For each carrier: the target is the declared default_target_attribute (sidecar .json), else the last attribute. For each
other attribute whose non-missing values are all in {0, 1}, the agreement of (value == 1) with (target == c) is computed
for every class c, and the best is kept. A column with agreement >= 0.999 for some class is printed as a leak candidate.
This is a reading of SEEN raw files; it re-scores nothing and changes no verdict.

    uv run python Pre_Phoenix_Audit/checks/label_leak.py > Pre_Phoenix_Audit/checks/label_leak.txt   (needs data/raw; rerun by hand)
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "openml"
THRESH = 0.999


def parse(path):
    attrs, rows, in_data = [], [], False
    for line in path.read_text(errors="replace").splitlines():
        t = line.strip()
        if not t or t.startswith("%"):
            continue
        if in_data:
            if t.startswith("{"):
                return attrs, None  # sparse ARFF: not scanned
            rows.append([x.strip().strip("'\"") for x in t.split(",")])
            continue
        low = t.lower()
        if low.startswith("@attribute"):
            rest = t[len("@attribute"):].strip()
            name = rest[1:rest.index(rest[0], 1)] if rest[0] in "'\"" else rest.split()[0]
            attrs.append(name)
        elif low.startswith("@data"):
            in_data = True
    return attrs, rows


def target_of(path, attrs):
    js = path.with_suffix(".json")
    if js.exists():
        try:
            t = json.loads(js.read_text())["data_set_description"].get("default_target_attribute")
            if t in attrs:
                return t
        except (KeyError, ValueError, TypeError):
            pass
    return attrs[-1]


def main():
    print("PRE-PHOENIX INTERPRETIVE AUDIT — NO VERDICTS ALTERED: label-leak scan of SEEN OpenML raw files")
    print(f"rule: a {{0,1}} column whose (value == 1) agrees with (target == c) on >= {THRESH} of rows with both present")
    files = sorted(RAW.glob("*.arff"))
    print(f"files scanned: {len(files)} in data/raw/openml\n")
    flagged = 0
    for f in files:
        attrs, rows = parse(f)
        sha = hashlib.sha256(f.read_bytes()).hexdigest()[:16]
        if rows is None or not attrs:
            print(f"{f.name}: sparse or unreadable, not scanned (sha256 {sha}…)")
            continue
        rows = [r for r in rows if len(r) == len(attrs)]
        tgt = target_of(f, attrs); ti = attrs.index(tgt)
        y = [r[ti] for r in rows]
        classes = sorted({v for v in y if v not in ("?", "")})
        hits = []
        for j, a in enumerate(attrs):
            if j == ti:
                continue
            col = [r[j] for r in rows]
            present = [i for i, v in enumerate(col) if v not in ("?", "") and y[i] not in ("?", "")]
            if not present or not {col[i] for i in present} <= {"0", "1", "0.0", "1.0"}:
                continue
            best_c, best = None, 0.0
            for c in classes:
                agree = sum((col[i] in ("1", "1.0")) == (y[i] == c) for i in present) / len(present)
                if agree > best:
                    best_c, best = c, agree
            if best >= THRESH:
                hits.append(f"{a}->class {best_c} {best:.6f}")
        if hits:
            flagged += 1
            print(f"{f.name}: target '{tgt}', rows {len(rows)}, classes {len(classes)}; LEAK CANDIDATES {len(hits)}: " + "; ".join(hits))
    print(f"\ncarriers with at least one leak candidate: {flagged} of {len(files)}")


if __name__ == "__main__":
    main()
