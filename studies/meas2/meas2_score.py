"""Study MEAS2 — re-run of MEAS after its loader voided it (see ledger row MEAS-1..3). H-L5 ("change has its own clock") on measles epidemics, 20 English
cities, biweekly, 22 years (tsiR `twentymeas`, Grenfell). Unit = city.

    uv run python studies/meas2/meas2_score.py run                # all cities, all cells -> JSON lines
    uv run python studies/meas2/meas2_score.py score <results.jsonl>
    uv run python studies/meas2/meas2_score.py smoke              # synthetic, no data

Carrier: reported cases per biweek, a Poisson-rate carrier. Under the Poisson
metric the Fisher-Rao arc of the rate is the total variation of y = 2*sqrt(cases)
(SCOPE.md P6/P9, instrument.core.poisson_transform); the identity metric gives
the total variation of the counts. Both are scored; the prereg names Poisson
as primary (MEAS-1) and identity as MEAS-2.

Own events: epidemic ONSETS from instrument.core.onset_events (a threshold rule
on the raw counts: no smoothing, no peak finder). Every constant is a named
parameter and the sensitivity table sweeps them.

Per city: occasions = onset-to-onset. C_m = arc of y over occasion m; dt_m =
biweeks; A_m = peak-to-trough of y over the occasion (control i, same metric).
Control (iii): arc between find_peaks boundaries (peak_cuts on the counts).
Criterion per city (all three): cv_arc < cv_clock; paired-bootstrap 95% CI of
(cv_arc - cv_clock) below 0; paired 95% CI of (cv_arc - cv_amp) below 0.
Cross-city: fraction of qualifying cities passing, exact two-sided binomial p.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402
from scipy.stats import binomtest  # noqa: E402

HERE = Path(__file__).resolve().parent
if (HERE / "core.py").exists():
    # frozen copy under runs/<study>/frozen/: use the frozen instrument beside it; the repo's
    # data/ is reached through the runs/data symlink (see runs/eqx/RUNLOG.md)
    sys.path.insert(0, str(HERE))
    from core import (arc_length, cv, onset_events, peak_cuts, poisson_transform,  # noqa: E402
                      regularity, unit_sigma)
    ROOT = HERE.parents[1]
else:
    ROOT = HERE.parents[1]
    sys.path.insert(0, str(ROOT))
    from instrument.core import (arc_length, cv, onset_events, peak_cuts, poisson_transform,  # noqa: E402
                                 regularity, unit_sigma)

RAW = ROOT / "data" / "raw" / "measles" / "twentymeas.RData"

# ---------------------------------------------------------------- frozen parameters
MIN_EVENTS = 8            # a city needs >= 8 onsets (>= 7 occasions) to be scored
N_BOOT = 2000; BOOT_SEED = 0
PRIMARY = dict(rise_factor=2.0, floor_frac=0.25, min_cases=20.0, min_gap=20)   # onset detector, primary cell
SENSITIVITY = dict(rise_factor=(1.5, 2.0, 3.0), floor_frac=(0.15, 0.25, 0.5), min_gap=(12, 20, 30))
PEAK_PROMINENCE_FRAC = 0.3; PEAK_DISTANCE = 20   # control (iii) peak_cuts on the counts
METRICS = ("poisson", "identity")
PASS_FRAC, FAIL_FRAC, ALPHA = 0.80, 0.60, 0.05


# ---------------------------------------------------------------- data
def sha256(p: Path) -> str:
    h = hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()


def load_twentymeas(path: Path = RAW):
    """Returns {city: cases (T,) float}, meta. Tries the pure-python `rdata` reader
    (supports R lists), then pyreadr. The Rd says: a list of 20 data frames with
    cases, births, populations, biweekly, 22 years. Column named 'cases' is required."""
    series = {}
    import rdata
    obj = rdata.read_rda(path)
    top = obj[list(obj.keys())[0]] if isinstance(obj, dict) else obj
    skipped = []
    for city, df in dict(top).items():
        # the R list carries one unnamed, empty element before the 20 data frames (the
        # structure MEAS's loader tripped on); only data frames with a 'cases' column count
        if hasattr(df, "columns") and "cases" in list(df.columns):
            series[str(city)] = np.asarray(df["cases"], float)
        else:
            skipped.append(repr(city))
    reader = f"rdata (skipped non-dataframe entries: {skipped})"
    if len(series) != 20:
        raise SystemExit(f"FORMAT VOID: expected 20 city series with a 'cases' column, got {len(series)}")
    meta = dict(file=str(path.relative_to(ROOT)), sha256=sha256(path), reader=reader, n_cities=len(series),
                lengths={k: int(len(v)) for k, v in series.items()})
    return series, meta


# ---------------------------------------------------------------- one city, one cell
def score_city(cases: np.ndarray, metric: str, det: dict):
    c = np.asarray(cases, float)
    nan = int(np.isnan(c).sum())
    if nan:
        return dict(excluded=f"{nan} NaN samples")
    ev = onset_events(c, **det)
    if len(ev) < MIN_EVENTS:
        return dict(excluded=f"{len(ev)} onsets < {MIN_EVENTS}", n_events=int(len(ev)))
    y = poisson_transform(c) if metric == "poisson" else c
    r = regularity(y, ev, sigma=1.0, n_boot=N_BOOT, seed=BOOT_SEED)
    # control (iii): arc between peak-detected boundaries, same metric
    pk = peak_cuts(c, prominence=PEAK_PROMINENCE_FRAC * np.ptp(c), distance=PEAK_DISTANCE)
    cv_arc_peakcut = None
    if len(pk) >= MIN_EVENTS:
        Cp = [arc_length(y[a:b + 1]) for a, b in zip(pk[:-1], pk[1:])]
        cv_arc_peakcut = cv(np.asarray(Cp))
    # unit (A1') and rho, for reporting: sigma from the per-occasion peak statistic of y
    peaks = np.array([np.max(y[a:b + 1]) for a, b in zip(ev[:-1], ev[1:])])
    try:
        sig = unit_sigma(peaks); rho = float(np.mean([np.ptp(y[a:b + 1]) for a, b in zip(ev[:-1], ev[1:])]) / sig)
    except ValueError as e:
        sig, rho = None, f"n/a ({e})"
    passes = bool((r["cv_arc"] < r["cv_clock"]) and (r["ci95"][1] < 0) and (r["ci95_amp"][1] < 0))
    return dict(n_events=int(len(ev)), n_occasions=int(r["n"]), cv_arc=r["cv_arc"], cv_clock=r["cv_clock"],
                cv_amp=r["cv_amp"], ci95=r["ci95"], ci95_amp=r["ci95_amp"], cv_arc_peakcut=cv_arc_peakcut,
                sigma=sig, rho=rho, passes=passes, mean_dt=float(np.mean(np.diff(ev))))


def cells():
    yield ("primary", dict(PRIMARY))
    for rf in SENSITIVITY["rise_factor"]:
        for ff in SENSITIVITY["floor_frac"]:
            for mg in SENSITIVITY["min_gap"]:
                d = dict(PRIMARY, rise_factor=rf, floor_frac=ff, min_gap=mg)
                if d != PRIMARY:
                    yield (f"rf{rf}_ff{ff}_mg{mg}", d)


def run_all(series, meta):
    print(json.dumps(dict(dataset="tsiR twentymeas", **meta, params=dict(MIN_EVENTS=MIN_EVENTS, N_BOOT=N_BOOT,
                          BOOT_SEED=BOOT_SEED, PRIMARY=PRIMARY, SENSITIVITY=SENSITIVITY,
                          PEAK_PROMINENCE_FRAC=PEAK_PROMINENCE_FRAC, PEAK_DISTANCE=PEAK_DISTANCE))), flush=True)
    for cell, det in cells():
        for metric in METRICS:
            for city, c in series.items():
                o = score_city(c, metric, det)
                print(json.dumps(dict(cell=cell, metric=metric, city=city, det=det, **o)), flush=True)


# ---------------------------------------------------------------- scoring (MEAS-1..3, as in PREREG.md)
def verdict(frac, p):
    if frac >= PASS_FRAC and p < ALPHA:
        return "PASS"
    if frac < FAIL_FRAC:
        return "FAIL"
    return "INDETERMINATE (between 60% and 80%, or p >= 0.05)"


def score(path):
    rows = [json.loads(l) for l in open(path) if l.startswith("{") and '"cell"' in l]
    cellnames = []
    for r in rows:
        if r["cell"] not in cellnames: cellnames.append(r["cell"])
    print("=" * 110); print("MEAS scoring — thresholds from prereg/meas2/PREREG.md; per-city values shown for the primary cell"); print("=" * 110)
    table = {}
    for cell in cellnames:
        for metric in METRICS:
            v = [r for r in rows if r["cell"] == cell and r["metric"] == metric]
            scored = [r for r in v if "excluded" not in r]
            excl = [r for r in v if "excluded" in r]
            k = sum(r["passes"] for r in scored); n = len(scored)
            frac = k / n if n else float("nan")
            p = float(binomtest(k, n, 0.5, alternative="two-sided").pvalue) if n else float("nan")
            wins_plain = sum(r["cv_arc"] < r["cv_clock"] for r in scored)
            iii = [r for r in scored if r["cv_arc_peakcut"] is not None]
            k3 = sum(r["cv_arc"] < r["cv_arc_peakcut"] for r in iii)
            table[(cell, metric)] = dict(k=k, n=n, frac=frac, p=p, verdict=verdict(frac, p), excluded=len(excl),
                                         wins_plain=wins_plain, k3=k3, n3=len(iii))
            if cell == "primary":
                print(f"\n[primary cell, metric={metric}]  detector {v[0]['det']}")
                for r in sorted(scored, key=lambda r: r["city"]):
                    pc = "n/a" if r["cv_arc_peakcut"] is None else f"{r['cv_arc_peakcut']:.3f}"
                    rho = r["rho"] if isinstance(r["rho"], str) else f"{r['rho']:.1f}"
                    print(f"  {r['city']:14s} onsets={r['n_events']:2d} cv_arc={r['cv_arc']:.3f} cv_clock={r['cv_clock']:.3f} "
                          f"cv_amp={r['cv_amp']:.3f} ci=({r['ci95'][0]:+.3f},{r['ci95'][1]:+.3f}) "
                          f"ci_amp=({r['ci95_amp'][0]:+.3f},{r['ci95_amp'][1]:+.3f}) cv_arc_peakcut={pc} rho={rho}"
                          f"  -> {'PASS' if r['passes'] else 'FAIL'}")
                for r in excl:
                    print(f"  {r['city']:14s} EXCLUDED: {r['excluded']}")
                print(f"  per-city PASS {k}/{n} = {frac:.3f}, binomial p = {p:.4f}; plain cv_arc<cv_clock in {wins_plain}/{n}; "
                      f"control (iii) arc-between-onsets beats arc-between-peaks in {k3}/{len(iii)}; excluded {len(excl)}")
    print("\n" + "-" * 110)
    for metric, hid in (("poisson", "MEAS-1 (Poisson metric, primary)"), ("identity", "MEAS-2 (identity metric)")):
        t = table[("primary", metric)]
        print(f"{hid}: {t['k']}/{t['n']} cities pass (frac {t['frac']:.3f}, p {t['p']:.4f}) -> {t['verdict']}")
        flips = sum(1 for cell in cellnames if cell != "primary" and table[(cell, metric)]["verdict"].split()[0] != t["verdict"].split()[0])
        print(f"   sensitivity: verdict differs from primary in {flips}/{len(cellnames)-1} cells -> {'FRAGILE' if flips > 1 else 'not fragile'}")
        for cell in cellnames:
            tt = table[(cell, metric)]
            print(f"     {cell:18s} {tt['k']:2d}/{tt['n']:2d} pass  p={tt['p']:.3f}  plain {tt['wins_plain']:2d}/{tt['n']:2d}  (iii) {tt['k3']:2d}/{tt['n3']:2d}  excl {tt['excluded']}  {tt['verdict'].split()[0]}")
    t = table[("primary", "poisson")]
    print(f"MEAS-3 (control iii, Poisson): onset-arc more regular than peak-cut arc in {t['k3']}/{t['n3']} cities -> "
          f"{'PASS' if t['n3'] and t['k3']/t['n3'] >= 0.70 else 'FAIL'} (needs >= 70%)")


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "smoke":
        if (HERE / "battery.py").exists():
            from battery import S_P_amfm, S_P_fm_compensating
        else:
            from surrogates.battery import S_P_amfm, S_P_fm_compensating
        for gen in (S_P_amfm, S_P_fm_compensating):
            x, ev, meta = gen(n=12)
            print(meta["name"], json.dumps(score_city(x, "poisson", PRIMARY)))
    elif cmd == "run":
        series, meta = load_twentymeas()
        run_all(series, meta)
    elif cmd == "score":
        score(sys.argv[2])
    else:
        raise SystemExit(__doc__)
