"""RLAW loaders: FRED csv, the SPF median workbook (a stdlib xlsx reader: no openpyxl in the locked environment), USCRN
daily01 fixed-width files and the Kool et al. (2016) two-step .mat files. Every format rule below comes from the sources'
documentation (docs/citations/rlaw_data_availability_2026-09-24.md), not from the data."""
import re
import zipfile
import xml.etree.ElementTree as ET

import numpy as np

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "pr": "http://schemas.openxmlformats.org/package/2006/relationships"}


def _col_index(ref):
    letters = re.match(r"([A-Z]+)", ref).group(1); n = 0
    for ch in letters: n = n * 26 + (ord(ch) - 64)
    return n - 1


def read_xlsx_sheet(path, sheet):
    """Rows of one worksheet as lists (None for empty cells). Numbers -> float, shared/inline strings -> str,
    error cells (t="e", e.g. #N/A, the SPF missing code) -> None."""
    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml")); rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        rid = None
        for s in wb.find("m:sheets", NS):
            if (s.get("name") or "").upper() == sheet.upper(): rid = s.get("{%s}id" % NS["r"])
        if rid is None: raise KeyError(f"sheet {sheet!r} not in {path}")
        target = [r.get("Target") for r in rels if r.get("Id") == rid][0]
        target = target.lstrip("/"); target = target if target.startswith("xl/") else "xl/" + target
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
                shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
        ws = ET.fromstring(z.read(target)); rows = []
        for row in ws.find("m:sheetData", NS).findall("m:row", NS):
            cells = {}
            for c in row.findall("m:c", NS):
                t = c.get("t"); v = c.find("m:v", NS); j = _col_index(c.get("r"))
                if t == "s": cells[j] = shared[int(v.text)]
                elif t == "inlineStr": cells[j] = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                elif t == "e" or v is None: cells[j] = None
                elif t == "str": cells[j] = v.text
                else:
                    try: cells[j] = float(v.text)
                    except ValueError: cells[j] = None
            if cells: rows.append([cells.get(j) for j in range(max(cells) + 1)])
            else: rows.append([])
        return rows


def fred_csv(path):
    """(dates as datetime64[D], values float with NaN for '.' or empty). FRED csv: a header line, then date,value."""
    d, v = [], []
    with open(path) as f:
        head = f.readline()
        if "," not in head: raise ValueError(f"{path}: not a FRED csv header: {head[:80]!r}")
        for line in f:
            line = line.strip()
            if not line: continue
            a, b = line.split(",")[:2]; d.append(np.datetime64(a, "D"))
            try: v.append(float(b))
            except ValueError: v.append(np.nan)
    return np.array(d), np.array(v, float)


USCRN_FIELDS = {"date": 1, "t_mean": 7, "t_avg": 8, "soil5": 23, "soil10": 24, "soil20": 25, "soil50": 26, "soil100": 27}


def uscrn_daily(path):
    """USCRN daily01 (format version 03): 28 whitespace-separated fields; missing = -9999.0 (7-char one-decimal fields)."""
    out = {k: [] for k in USCRN_FIELDS}
    with open(path) as f:
        for line in f:
            p = line.split()
            if len(p) < 28: continue
            for k, i in USCRN_FIELDS.items():
                if k == "date": out[k].append(np.datetime64(f"{p[i][:4]}-{p[i][4:6]}-{p[i][6:8]}", "D"))
                else:
                    x = float(p[i]); out[k].append(np.nan if x <= -9990.0 else x)
    return {k: (np.array(v) if k == "date" else np.array(v, float)) for k, v in out.items()}


def _scalar(x):
    a = np.asarray(x)
    if a.dtype.kind in "OU": a = a.ravel()
    while a.dtype.kind == "O" and a.size: a = np.asarray(a.ravel()[0])
    return a.ravel()[0] if a.size else None


def kool_subjects(data_mat, subinfo_mat, nrtrials_full=150):
    """Kool, Cushman & Gershman (2016), Daw paradigm, as make_raw_data.m builds it: subjects listed in subinfo with exactly
    150 rows in data; practice trials (column 13 == 1) dropped. Column map (1-based, after the id): 1 stim_1_left, 3 rt1,
    4 choice1, 7 rt2, 8 choice2, 9 win, 10 state2, 13 practice, 14-17 ps1a1 ps1a2 ps2a1 ps2a2, 18 trial."""
    from scipy.io import loadmat
    data = loadmat(data_mat)["data"]; sub = loadmat(subinfo_mat)["subinfo"]
    ids = np.array([str(_scalar(data[i, 0])) for i in range(data.shape[0])])
    out = []
    for i in range(sub.shape[0]):
        sid = str(_scalar(sub[i, 0])); rows = np.where(ids == sid)[0]
        if rows.size != nrtrials_full: continue
        M = np.array([[float(_scalar(data[r, j])) for j in range(1, 19)] for r in rows])
        M = M[M[:, 12] != 1]
        missed = (M[:, 2] == -1) | (M[:, 6] == -1) | (M[:, 3] == -1) | (M[:, 7] == -1)
        out.append(dict(id=sid, state2=(M[:, 9] - 1).astype(int), choice2=(M[:, 7] - 1).astype(int), win=(M[:, 8] > 0).astype(float),
                        valid=~missed, ps=M[:, 13:17], n=int(M.shape[0])))
    return out
