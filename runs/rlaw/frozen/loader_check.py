"""RLAW loader check: synthetic files written in each source's documented format (FRED csv, the SPF xlsx with shared
strings and #N/A error cells, USCRN daily01 fixed-width with -9999.0, Kool's MATLAB cell arrays) are read back by the
frozen loaders and builders, and the units they build are compared with the arrays that generated them. No real data.

    uv run python studies/rlaw/loader_check.py > prereg/rlaw/loader_check.txt"""
import math
import pathlib
import sys
import tempfile
import zipfile

import numpy as np
from scipy.io import savemat

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rlaw_score as S  # noqa: E402
from rlaw_lib import K  # noqa: E402


def colname(j):
    s = ""; j += 1
    while j: j, r = divmod(j - 1, 26); s = chr(65 + r) + s
    return s


def write_xlsx(path, sheets):
    """sheets: {name: rows}; strings go to sharedStrings, None to an #N/A error cell, floats to numbers."""
    shared = []; idx = {}
    def sid(t):
        if t not in idx: idx[t] = len(shared); shared.append(t)
        return idx[t]
    wsx = []
    for name, rows in sheets.items():
        out = []
        for i, row in enumerate(rows):
            cs = []
            for j, v in enumerate(row):
                ref = f"{colname(j)}{i + 1}"
                if v is None: cs.append(f'<c r="{ref}" t="e"><v>#N/A</v></c>')
                elif isinstance(v, str): cs.append(f'<c r="{ref}" t="s"><v>{sid(v)}</v></c>')
                else: cs.append(f'<c r="{ref}"><v>{repr(float(v))}</v></c>')
            out.append(f'<row r="{i + 1}">{"".join(cs)}</row>')
        wsx.append('<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                   f'<sheetData>{"".join(out)}</sheetData></worksheet>')
    M = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"; R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    wb = f'<?xml version="1.0"?><workbook xmlns="{M}" xmlns:r="{R}"><sheets>' + "".join(
        f'<sheet name="{n}" sheetId="{i + 1}" r:id="rId{i + 1}"/>' for i, n in enumerate(sheets)) + "</sheets></workbook>"
    rels = '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(
        f'<Relationship Id="rId{i + 1}" Type="{R}/worksheet" Target="worksheets/sheet{i + 1}.xml"/>' for i in range(len(sheets))) + "</Relationships>"
    ss = f'<?xml version="1.0"?><sst xmlns="{M}">' + "".join(f"<si><t>{t}</t></si>" for t in shared) + "</sst>"
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("xl/workbook.xml", wb); z.writestr("xl/_rels/workbook.xml.rels", rels); z.writestr("xl/sharedStrings.xml", ss)
        for i, x in enumerate(wsx): z.writestr(f"xl/worksheets/sheet{i + 1}.xml", x)


def smooth(y, a):
    s = np.empty_like(y); s[0] = y[0]
    for t in range(1, y.size): s[t] = s[t - 1] + a * (y[t] - s[t - 1])
    return s


def main():
    rng = np.random.default_rng(777); tmp = pathlib.Path(tempfile.mkdtemp()); raw = tmp / "rlaw"; (raw / "fred").mkdir(parents=True)
    ok = True
    def fred(name, dates, vals):
        with open(raw / "fred" / f"{name}.csv", "w") as f:
            f.write(f"observation_date,{name}\n")
            for d, v in zip(dates, vals): f.write(f"{d},{'.' if not np.isfinite(v) else repr(float(v))}\n")
    # monthly series 1967-01 .. 2026-08
    months = np.arange(np.datetime64("1967-01"), np.datetime64("2026-09"), dtype="datetime64[M]"); nm = months.size
    for name in ("CPIAUCSL", "CPILFESL", "PCEPI", "PCEPILFE"):
        fred(name, [f"{m}-01" for m in months], 100 * np.exp(np.cumsum(0.003 + 0.002 * rng.normal(size=nm))))
    for name in ("UNRATE", "TB3MS", "GS10"):
        fred(name, [f"{m}-01" for m in months], 5 + np.cumsum(0.1 * rng.normal(size=nm)))
    fred("HOUST", [f"{m}-01" for m in months], 1500 + np.cumsum(30 * rng.normal(size=nm)))
    mi = np.arange(np.datetime64("1978-01"), np.datetime64("2024-04"), dtype="datetime64[M]")
    fred("MICH", [f"{m}-01" for m in mi], 3 + np.cumsum(0.1 * rng.normal(size=mi.size)))
    # SPF workbook: rows 1981Q3..2026Q3, CPI with an #N/A cell
    sheets = {}
    for root in S.SPF_VARS:
        rows = [["YEAR", "QUARTER"] + [f"{root}{h}" for h in range(1, 7)]]
        for y in range(1981, 2027):
            for q in range(1, 5):
                if (y, q) < (1981, 3) or (y, q) > (2026, 3): continue
                rows.append([float(y), float(q)] + [float(2 + 0.1 * rng.normal()) for _ in range(6)])
        if root == "CPI": rows[10][5] = None
        sheets[root] = rows
    write_xlsx(raw / "spf_medianLevel.xlsx", sheets)
    # daily pairs
    days = np.arange(np.datetime64("2001-02-01"), np.datetime64("2026-09-23"), dtype="datetime64[D]")
    wk = days[(days.astype("datetime64[D]").view("int64") + 3) % 7 < 5]
    for _, iv, px in S.IVOL_PAIRS:
        p = 100 * np.exp(np.cumsum(0.01 * rng.normal(size=wk.size))); v = 15 + np.abs(np.cumsum(0.2 * rng.normal(size=wk.size)))
        p[5] = np.nan; v[7] = np.nan
        fred(iv, [str(d) for d in wk], v); fred(px, [str(d) for d in wk], p)
    # USCRN: two stations, one with only 5/10 cm
    (raw / "uscrn2025").mkdir(); gen = {}
    for st, deep in (("XX_Test_1_N", True), ("YY_Test_2_S", False)):
        n = 365; air = 10 + np.cumsum(0.6 * rng.normal(size=n)) + 2 * rng.normal(size=n)
        s5 = smooth(air, float(K(0.3))); s10 = smooth(s5, 0.3); s20 = smooth(s10, 0.2); s50 = smooth(s20, 0.1); s100 = smooth(s50, 0.05)
        air[40] = -9999.0; gen[st] = (air.copy(), s5, s10)
        with open(raw / "uscrn2025" / f"CRND0103-2025-{st}.txt", "w") as f:
            for t in range(n):
                d = np.datetime64("2025-01-01") + np.timedelta64(t, "D"); ds = str(d).replace("-", "")
                soil = [s5[t], s10[t]] + ([s20[t], s50[t], s100[t]] if deep else [-9999.0] * 3)
                fields = ["99999", ds, "2.622", "-80.00", "35.00", "20.0", "0.0", f"{air[t] + 0.3:.1f}", f"{air[t]:.1f}", "0.0", "10.00", "C",
                          "20.0", "0.0", "10.0", "80.0", "40.0", "60.0", "-99.000", "-99.000", "-99.000", "-99.000", "-99.000"] + [f"{x:.1f}" for x in soil]
                f.write(" ".join(fields) + "\n")
    # Kool .mat: 3 subjects in subinfo, one with 149 rows (dropped), practice rows 25
    (raw / "kool").mkdir(); rows = []; ids = ["A1", "B2", "C3"]
    for k, sid in enumerate(ids):
        nr = 149 if sid == "C3" else 150
        for t in range(nr):
            prac = 1.0 if t < 25 else 0.0; st2 = float(1 + (t % 2)); ch2 = float(1 + ((t // 2) % 2)); win = float(t % 3 == 0)
            miss = (t == 60 and sid == "A1")
            r = [sid, 1.0, 2.0, -1.0 if miss else 500.0, -1.0 if miss else 1.0, 1.0, 2.0, 400.0, -1.0 if miss else ch2, win, st2, 1.0, 0.0, prac,
                 0.3, 0.4, 0.6, 0.7, float(t + 1)]
            rows.append(r)
    data = np.empty((len(rows), 19), dtype=object)
    for i, r in enumerate(rows):
        for j, v in enumerate(r): data[i, j] = v
    sub = np.empty((3, 1), dtype=object)
    for i, sid in enumerate(ids): sub[i, 0] = sid
    savemat(raw / "kool" / "data.mat", {"data": data}); savemat(raw / "kool" / "subinfo.mat", {"subinfo": sub})

    c = S.PRIMARY
    u = S.build_spf(raw, c); cpi = [x for x in u if x["id"] == "CPI"][0]
    print(f"SPF: {len(u)} units ({', '.join(x['id'] for x in u)}); CPI rows {cpi['s'].size}, NaN forecasts {int(np.isnan(cpi['s']).sum())} (one #N/A planted), first x finite {np.isfinite(cpi['x'][0])}")
    ok &= len(u) == 8 and int(np.isnan(cpi["s"]).sum()) == 1 and cpi["s"].size == 181
    u = S.build_mich(raw, c); print(f"Michigan: {len(u)} units of {[x['s'].size for x in u]} months (555 planted), delta {u[0]['delta']}")
    ok &= [x["s"].size for x in u] == [185, 185, 185]
    u = S.build_ivol(raw, c); print(f"implied vol: {len(u)} units, rows {[x['s'].size for x in u]}, NaN x {[int(np.isnan(x['x']).sum()) for x in u]} (the first return only: a missing price day is dropped and the next return spans two days; a missing index day is dropped)")
    ok &= all(int(np.isnan(x["x"]).sum()) == 1 and x["s"].size == wk.size - 2 for x in u)
    u5 = S.build_soil(raw, c, False); ud = S.build_soil(raw, c, True)
    a0, s5, _ = gen["XX_Test_1_N"]; x0 = [x for x in u5 if x["id"].startswith("XX")][0]
    same = np.allclose(np.round(np.where(a0 <= -9990, np.nan, a0), 1), x0["x"], equal_nan=True, atol=0.051)
    print(f"USCRN: 5 cm units {len(u5)}, deep units {len(ud)}; air read back (0.1 degC rounding) {same}; missing day read as NaN {bool(np.isnan(x0['x'][40]))}; "
          f"deep units of the 5/10-only station all-NaN soil20.. {all(np.isnan(x['s']).all() for x in ud if x['id'].startswith('YY') and not x['id'].endswith('@10cm'))}")
    ok &= same and bool(np.isnan(x0["x"][40])) and len(u5) == 2 and len(ud) == 8
    subs = S.build_twostep(raw, c); s0 = subs[0]["sub"]
    print(f"Kool: {len(subs)} subjects kept (C3 with 149 rows dropped); trials after practice {s0['n']}; missed {int((~s0['valid']).sum())}; "
          f"state2 values {sorted(set(s0['state2'][s0['valid']].tolist()))}; choice2 values {sorted(set(s0['choice2'][s0['valid']].tolist()))}; ps shape {s0['ps'].shape}")
    ok &= len(subs) == 2 and s0["n"] == 125 and int((~s0["valid"]).sum()) == 1 and s0["ps"].shape == (125, 4)
    m = S.measure(u5, c); r0 = [r for r in m if r["id"].startswith("XX")][0]
    print(f"soil 5 cm synthetic unit (air: drift sd 0.6, noise sd 2, v = 0.3; soil alpha = K(0.3) = {float(K(0.3)):.4f} by construction; reports rounded to 0.1): alpha_hat {r0['alpha_hat']:.4f}, v_hat {r0['v']:.4f}")
    print(f"summary: loader check {'PASSES' if ok else 'FAILS'}")
    if "--smoke" in sys.argv: S.run(raw)   # the whole scorer on the synthetic files (not part of the pinned output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
