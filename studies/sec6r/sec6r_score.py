"""Study SEC6R — SEC6 run in full with ONE change: SCL3's loader reads an ARFF STRING target as a class label.

Owner request: prompt-log entry 259 ("Yes, please run full SEC6 checks"); prereg/sec6r/DECLARATION.md (pushed at 3d9502c before
this file) fixes everything below.

WHAT THIS FILE DOES. It imports SEC6's frozen scorer by path (runs/sec6/frozen/sec6_score.py, which loads SEC5's, SEC4's, SCL3's
and SEC1's frozen copies beside it) and replaces only SCL3's row parser `_parse_rows` with `_parse_rows_r`:
  if the target attribute is declared `string`, it is re-declared nominal with values = its distinct non-missing field strings in
  sorted order, and the FROZEN parser is called on that; for every other target kind the frozen parser is called unchanged.
Nothing else is touched: SEC6's arms, seeds, grid, clip, baselines, `edge`, gates and scorer run byte for byte.

    uv run python studies/sec6r/sec6r_score.py devid_r  > prereg/sec6r/devid_r.txt   # D-ID-R: identity, STRING self-test, smoke
    uv run python studies/sec6r/sec6r_score.py check --part B                        # Part B raw files against data/manifests/sec6r.sha256
    uv run python studies/sec6r/sec6r_score.py all <OpenML id> --part A|B --out F [--times F]
    uv run python studies/sec6r/sec6r_score.py score <results.jsonl ...>
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve()
FROZEN = _HERE.parent.name == "frozen"
ROOT = _HERE.parents[3] if FROZEN else _HERE.parents[2]
_SEC6 = (_HERE.parent if FROZEN else ROOT / "runs" / "sec6r" / "frozen") / "sec6_score.py"
if not _SEC6.exists():                                              # before the freeze: SEC6's own frozen copy
    _SEC6 = ROOT / "runs" / "sec6" / "frozen" / "sec6_score.py"
_spec = importlib.util.spec_from_file_location("sec6_score", _SEC6)
M = importlib.util.module_from_spec(_spec); sys.modules["sec6_score"] = M; _spec.loader.exec_module(M)
L = M.L; S = M.S; np = M.np

_parse_rows_frozen = L._parse_rows


def _parse_rows_r(attrs, rows, target, drop):
    """SCL3's _parse_rows, with a STRING target re-declared nominal (sorted distinct non-missing values); else unchanged."""
    names = [a[0] for a in attrs]; ti = names.index(target)
    if attrs[ti][1] != "string":
        return _parse_rows_frozen(attrs, rows, target, drop)
    vals = sorted({r[ti] for r in rows if len(r) == len(attrs) and r[ti] not in ("?", "")})
    attrs = list(attrs); attrs[ti] = (attrs[ti][0], "nominal", vals)
    return _parse_rows_frozen(attrs, rows, target, drop)


L._parse_rows = _parse_rows_r

PART_A = dict(M.DATASETS)                                           # SEC6's twelve (SEEN since 2026-10-01): post hoc
PART_B = {183: ('abalone', 10, 2), 279: ('meta_stream_intervals.arff', 10, 2), 1534: ('volcanoes-b4', 4, 2), 1538: ('volcanoes-d1', 4, 2),
          1542: ('volcanoes-e1', 4, 2), 1552: ('autoUniv-au7-1100', 4, 2), 40985: ('tamilnadu-electricity', 10, 2),
          46608: ('drug_reviews_druglib_com', 10, 2), 46684: ('HolisticBias', 4, 2), 46709: ('SOCC', 10, 2),
          46745: ('Advanced_IoT_Dataset', 6, 2), 46761: ('mental_health_detection', 10, 2)}   # SEC7's metadata-only draw


def _part_b_from_selection():
    """PART_B must equal the DATASETS line of SEC7's pinned selection (copied to prereg/sec6r/carrier_selection_sec7.txt)."""
    sel = (ROOT / "prereg" / "sec6r" / "carrier_selection_sec7.txt").read_text().splitlines()
    line = [x for x in sel if x.startswith("DATASETS = ")][0]
    return eval(line[len("DATASETS = "):], {})                    # a literal dict printed by studies/sec7/select_carriers.py


# ---------------------------------------------------------------- D-ID-R (prereg/sec6r/DECLARATION.md)
def devid_r():
    ok_all = True
    print("SEC6R D-ID-R (prereg/sec6r/DECLARATION.md): the patched loader against SEC6's frozen loader")
    tb = _part_b_from_selection(); same = tb == PART_B
    print(f"[0] PART_B equals the DATASETS line of prereg/sec6r/carrier_selection_sec7.txt: {same}"); ok_all &= same
    print("[1] identity on every SEEN nominal-target carrier of SCL3, SEC3, SEC4 and SEC5 (matrices, labels, header):")
    n = k = 0
    for study, table in M.DEV_TABLES:
        for did in sorted(table):
            L.DATASETS = table
            L._parse_rows = _parse_rows_frozen; Xa, ya, ma = L.load_openml(did)
            L._parse_rows = _parse_rows_r; Xb, yb, mb = L.load_openml(did)
            names = [a[0] for a in L.read_arff(L.RAW / f"{did}_{table[did][0]}.arff")[0]]
            eq = Xa.shape == Xb.shape and bool(np.array_equal(Xa, Xb)) and bool(np.array_equal(ya, yb)) and ma == mb
            n += 1; k += eq
            print(f"   {study:5} {did:6d} {table[did][0][:34]:34} n {ma['n']:6d} d {ma['d']:4d} -> {'identical' if eq else 'DIFFERENT'}")
            del names
    print(f"   identical on {k}/{n}"); ok_all &= (k == n)
    print("[2] a STRING target is read (synthetic ARFF in a temporary folder, never the repository):")
    raw0 = L.RAW
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp); L.RAW = tmp
        try:
            classes = ("alpha", "beta", "gamma", "delta"); did = 990011; name = "selftest_string_target"
            lines = ["@relation selftest", "@attribute x numeric", "@attribute z numeric", "@attribute label string", "@data"]
            for i in range(240):
                c = i % 4; lines.append(f"{c + ((i * 37) % 11) / 10},{(i * 13) % 7},'{classes[c]}'")
            (tmp / f"{did}_{name}.arff").write_text("\n".join(lines) + "\n")
            (tmp / f"{did}_{name}.json").write_text(json.dumps({"data_set_description": {"default_target_attribute": "label", "version": "1"}}))
            table = {did: (name, 4, 2)}; L.DATASETS = table
            L._parse_rows = _parse_rows_frozen; _, _, mf = L.load_openml(did)
            L._parse_rows = _parse_rows_r; _, yr, mr = L.load_openml(did)
        finally:
            L.RAW = raw0; L._parse_rows = _parse_rows_r
    okf = mf["n_file"] == 0 and mf["rows_dropped_nan"] == 240
    okr = mr["n_file"] == 240 and mr["rows_dropped_nan"] == 0 and mr["classes_used"] == 4 and sorted(mr["class_counts"]) == [60, 60, 60, 60]
    print(f"   frozen loader: rows kept {mf['n_file']}, dropped {mf['rows_dropped_nan']} -> {'drops every row, as SEC6 found' if okf else 'NOT as expected'}")
    print(f"   patched loader: rows kept {mr['n_file']}, dropped {mr['rows_dropped_nan']}, classes used {mr['classes_used']}, counts {mr['class_counts']} "
          f"-> {'reads the STRING target' if okr else 'NOT as required'}")
    ok_all &= okf and okr
    print("[3] SEC6's smokefull through this wrapper against prereg/sec6/smokefull.txt (the CPU-seconds line excluded: timing is not deterministic):")
    buf = io.StringIO()
    with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(buf):
        outp = str(Path(tmp) / "results_sec6r_smoke.jsonl")
        M.d0_selftest()
        with open(outp, "w") as out, open(outp.replace("results_", "times_"), "w") as tout:
            M.run_carrier(0, out, tout, synthetic=True)
        M.score([outp])
    new = buf.getvalue().splitlines(); old = (ROOT / "prereg" / "sec6" / "smokefull.txt").read_text().splitlines()
    cpu = lambda ls: [x for x in ls if "CPU s full" not in x]  # noqa: E731
    diff = [i for i, (a, b) in enumerate(zip(cpu(new), cpu(old))) if a != b]
    oks = len(cpu(new)) == len(cpu(old)) and not diff
    print(f"   lines {len(new)} (pinned {len(old)}); identical outside the CPU line: {oks}" + ("" if oks else f"; first differing line {diff[:1]}"))
    ok_all &= oks
    print(f"D-ID-R -> {'holds' if ok_all else 'FAILS: SEC6R stops before the hash'}")
    return ok_all


def data_check_b():
    man = {}
    for line in open(ROOT / "data" / "manifests" / "sec6r.sha256"):
        if line.strip(): h_, pth = line.split()[:2]; man[pth] = h_
    bad = []
    for did, (name, _, _) in PART_B.items():
        for ext in ("arff", "json"):
            pth = f"data/raw/openml/{did}_{name}.{ext}"; got = S.sha256(ROOT / pth) if (ROOT / pth).exists() else None
            print(f"{did} {name} .{ext}: sha256 {got} manifest {man.get(pth)} -> {'ok' if got and got == man.get(pth) else 'MISMATCH'}")
            if not got or got != man.get(pth): bad.append(f"{name}.{ext}")
    print("data check: " + (f"all {2 * len(PART_B)} raw files match data/manifests/sec6r.sha256" if not bad else f"MISMATCH {bad}: the study stops"))
    return not bad


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "devid_r":
        sys.exit(0 if devid_r() else 1)
    elif cmd == "check":
        ok = data_check_b(); ok = M.d0_selftest() and ok
        sys.exit(0 if ok else 1)
    elif cmd == "all":
        did = int(sys.argv[2]); part = sys.argv[sys.argv.index("--part") + 1]
        table = {"A": PART_A, "B": PART_B}[part]
        if did not in table: raise SystemExit(f"{did} is not a Part {part} carrier")
        outp = sys.argv[sys.argv.index("--out") + 1]
        tp = sys.argv[sys.argv.index("--times") + 1] if "--times" in sys.argv else outp.replace("results_", "times_")
        with open(outp, "w") as out, open(tp, "w") as tout: M.run_carrier(did, out, tout, table=table)
    elif cmd == "score": M.score(sys.argv[2:])
    else: raise SystemExit(__doc__)
