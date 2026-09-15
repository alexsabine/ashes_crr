"""Study CARD — H-L5 and the A3 proxy (L5x-3) on a cardiac carrier.
PhysioNet "Autonomic Aging: a dataset to quantify changes of cardiovascular autonomic
function during healthy aging" 1.0.0, records 0061-0090 (records 0001-0060 are SEEN).
Unit = record (subject). Signals: ECG and continuous non-invasive blood pressure (NIBP),
WFDB format. PhysioNet is unreachable from the execution environment, so the files are
supplied by the human after the prereg hash (see PREREG.md); their sha256s go in the
manifest.

    uv run python studies/card/card_score.py run   [data_dir]   # all records, all cells -> JSON lines
    uv run python studies/card/card_score.py score <results.jsonl>
    uv run python studies/card/card_score.py smoke               # synthetic ECG+BP, no data

Own events: R-peaks from a Pan-Tompkins-style detector with PUBLISHED constants
(band-pass 5-15 Hz, derivative, squaring, 150 ms moving integration, adaptive
threshold, 200 ms refractory). No constant is learned on any data in this repository.

Occasions = R-to-R. Per record and per cell:
  CARD-1  quantity = arc of the BP trace over each beat (identity metric: total
          variation in mmHg, sigma-scaled per record; P9 disclosure), vs the RR clock.
          Control (i): pulse amplitude (peak-to-trough of BP within the beat).
  CARD-2  same with the ECG trace's own arc (expected to tie its QRS amplitude).
  CARD-3  DIAGNOSTIC ONLY (not a hypothesis): arc of BP between ANTIPODAL cuts on the
          intrinsic phase of BP vs arc between PEAK-detected cuts. gate_A3 showed this
          comparison passes on jittered asymmetric surrogates with no CRR content (S-C,
          S-E) because find_peaks segments them inconsistently; under R4 it cannot enter
          the prereg as a test of A3. Reported per record, never scored.
Per-record criterion for CARD-1/2: cv_arc < cv_clock, paired 95% CI of (cv_arc - cv_clock)
below 0, paired 95% CI of (cv_arc - cv_amp) below 0. Cross-record: fraction and exact
binomial p. Sensitivity: band-pass edges x refractory x integration window (detector),
and the analytic-signal detrend flag for CARD-3.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402
from scipy.signal import butter, filtfilt  # noqa: E402
from scipy.stats import binomtest  # noqa: E402

HERE = Path(__file__).resolve().parent
if (HERE / "core.py").exists():
    sys.path.insert(0, str(HERE))
    from core import (antipodal_cuts, arc_length, cv, intrinsic_phase, peak_cuts,  # noqa: E402
                      regularity, unit_sigma)
    ROOT = HERE.parents[1]
else:
    ROOT = HERE.parents[1]
    sys.path.insert(0, str(ROOT))
    from instrument.core import (antipodal_cuts, arc_length, cv, intrinsic_phase, peak_cuts,  # noqa: E402
                                 regularity, unit_sigma)

DATA = ROOT / "data" / "raw" / "autonomic_aging"
RECORDS = [f"{i:04d}" for i in range(61, 91)]          # 0061-0090, pre-registered
MIN_BEATS = 200                                         # a record needs >= 200 detected beats
MAX_SECONDS = 600.0                                     # first 10 min of each record (fixed)
N_BOOT = 2000; BOOT_SEED = 0
PRIMARY = dict(low=5.0, high=15.0, integ_ms=150, refractory_ms=200)
SENSITIVITY = dict(low=(4.0, 5.0, 8.0), high=(12.0, 15.0, 20.0), refractory_ms=(200, 250, 300))
PEAK_DISTANCE_MS = 300; PEAK_PROMINENCE_FRAC = 0.3      # control (iii) / CARD-3 peak cuts on BP
PASS_FRAC, FAIL_FRAC, ALPHA = 0.80, 0.60, 0.05
RHO_FLOOR = 3.0                                         # quality gate: exclude records with rho < 3 (reported)


# ---------------------------------------------------------------- data
def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_record(rec: str, data_dir: Path):
    import wfdb
    r = wfdb.rdrecord(str(data_dir / rec))
    names = [s.lower() for s in r.sig_name]
    def pick(keys):
        for k in keys:
            for i, n in enumerate(names):
                if k in n:
                    return i
        return None
    ie = pick(("ecg",)); ib = pick(("nibp", "bp", "pressure", "abp"))
    if ie is None or ib is None:
        raise ValueError(f"{rec}: need ECG and BP channels, have {r.sig_name}")
    n = int(min(len(r.p_signal), MAX_SECONDS * r.fs))
    return r.p_signal[:n, ie].astype(float), r.p_signal[:n, ib].astype(float), float(r.fs), r.sig_name


# ---------------------------------------------------------------- R-peak detector (published constants)
def rpeaks(ecg: np.ndarray, fs: float, low=5.0, high=15.0, integ_ms=150, refractory_ms=200) -> np.ndarray:
    x = np.asarray(ecg, float); x = x - np.mean(x)
    b, a = butter(2, [low / (fs / 2), high / (fs / 2)], btype="band")
    f = filtfilt(b, a, x)
    d = np.gradient(f); s = d * d
    w = max(1, int(integ_ms / 1000 * fs)); integ = np.convolve(s, np.ones(w) / w, mode="same")
    refr = int(refractory_ms / 1000 * fs)
    thr = 0.5 * np.mean(integ[: int(2 * fs)]) + 0.5 * np.max(integ[: int(2 * fs)]) * 0.25
    peaks = []; last = -refr; spk = np.max(integ[: int(2 * fs)]); npk = np.mean(integ[: int(2 * fs)])
    i = 1
    while i < len(integ) - 1:
        if integ[i] > thr and integ[i] >= integ[i - 1] and integ[i] >= integ[i + 1] and i - last >= refr:
            # locate the R wave as the max of |filtered| within +-100 ms of the integrator peak
            lo, hi = max(0, i - int(0.1 * fs)), min(len(f), i + int(0.1 * fs))
            j = lo + int(np.argmax(np.abs(f[lo:hi])))
            peaks.append(j); last = i
            spk = 0.125 * integ[i] + 0.875 * spk
        else:
            npk = 0.125 * integ[i] + 0.875 * npk if integ[i] < thr else npk
        thr = npk + 0.25 * (spk - npk)
        i += 1
    return np.asarray(sorted(set(peaks)), int)


# ---------------------------------------------------------------- one record, one cell
def score_record(ecg, bp, fs, det: dict, detrend_phase: bool = True):
    if np.isnan(ecg).any() or np.isnan(bp).any():
        return dict(excluded=f"NaN samples: ecg {int(np.isnan(ecg).sum())}, bp {int(np.isnan(bp).sum())}")
    if np.ptp(bp) == 0 or np.ptp(ecg) == 0:
        return dict(excluded="flat channel")
    ev = rpeaks(ecg, fs, **det)
    if len(ev) < MIN_BEATS:
        return dict(excluded=f"{len(ev)} beats < {MIN_BEATS}", n_events=int(len(ev)))
    out = dict(n_events=int(len(ev)), mean_rr_s=float(np.mean(np.diff(ev)) / fs))
    for name, x in (("bp", bp), ("ecg", ecg)):
        # unit (A1'): sigma from the per-beat peak-to-trough statistic on the first half of beats
        amp = np.array([np.ptp(x[a:b + 1]) for a, b in zip(ev[:-1], ev[1:])])
        try:
            sig = unit_sigma(amp[: len(amp) // 2])
        except ValueError as e:
            out[name] = dict(excluded=f"unit: {e}"); continue
        rho = float(np.mean(amp) / sig)
        r = regularity(x, ev, sigma=sig, dt=1.0 / fs, n_boot=N_BOOT, seed=BOOT_SEED)
        passes = bool((r["cv_arc"] < r["cv_clock"]) and (r["ci95"][1] < 0) and (r["ci95_amp"][1] < 0))
        out[name] = dict(sigma=float(sig), rho=rho, cv_arc=r["cv_arc"], cv_clock=r["cv_clock"], cv_amp=r["cv_amp"],
                         ci95=r["ci95"], ci95_amp=r["ci95_amp"], passes=passes, rho_ok=bool(rho >= RHO_FLOOR))
    # CARD-3: antipodal cuts on the intrinsic phase of BP vs peak cuts on BP; arc of BP between cuts
    ph = intrinsic_phase(bp, detrend=detrend_phase)
    pk = peak_cuts(bp, prominence=PEAK_PROMINENCE_FRAC * np.ptp(bp), distance=max(2, int(PEAK_DISTANCE_MS / 1000 * fs)))
    ant = antipodal_cuts(ph, start=int(pk[1]) if len(pk) > 1 else 0)
    sig_bp = out["bp"]["sigma"] if "sigma" in out.get("bp", {}) else 1.0
    def arcs(cuts):
        return np.array([arc_length(bp[a:b + 1], sigma=sig_bp) for a, b in zip(cuts[:-1], cuts[1:]) if b > a])
    if len(ant) >= MIN_BEATS and len(pk) >= MIN_BEATS:
        Ca, Cp = arcs(ant), arcs(pk)
        # paired bootstrap on cv(antipodal) - cv(peak) over occasions (independent resamples of each set)
        rng = np.random.default_rng(BOOT_SEED); diffs = []
        for _ in range(N_BOOT):
            diffs.append(cv(Ca[rng.integers(0, len(Ca), len(Ca))]) - cv(Cp[rng.integers(0, len(Cp), len(Cp))]))
        lo, hi = np.percentile(diffs, [2.5, 97.5])
        d = np.array([np.min(np.abs(pk - c)) for c in ant[1:]]) / fs
        out["card3"] = dict(n_antipodal=int(len(ant)), n_peak=int(len(pk)), cv_arc_antipodal=cv(Ca), cv_arc_peakcut=cv(Cp),
                            ci95=(float(lo), float(hi)), passes=bool(cv(Ca) < cv(Cp) and hi < 0),
                            median_antipode_extremum_s=float(np.median(d)))
    else:
        out["card3"] = dict(excluded=f"antipodal {len(ant)} / peak {len(pk)} cuts < {MIN_BEATS}")
    return out


def cells():
    yield ("primary", dict(PRIMARY))
    for lo in SENSITIVITY["low"]:
        for hi in SENSITIVITY["high"]:
            for rf in SENSITIVITY["refractory_ms"]:
                d = dict(PRIMARY, low=lo, high=hi, refractory_ms=rf)
                if d != PRIMARY:
                    yield (f"lo{lo}_hi{hi}_rf{rf}", d)


def run_all(data_dir: Path):
    man = {}
    for rec in RECORDS:
        for ext in ("hea", "dat"):
            p = data_dir / f"{rec}.{ext}"
            man[f"{rec}.{ext}"] = sha256(p) if p.exists() else None
    print(json.dumps(dict(dataset="PhysioNet autonomic-aging-cardiovascular 1.0.0", records=RECORDS, files=man,
                          params=dict(MIN_BEATS=MIN_BEATS, MAX_SECONDS=MAX_SECONDS, N_BOOT=N_BOOT, BOOT_SEED=BOOT_SEED,
                                      PRIMARY=PRIMARY, SENSITIVITY=SENSITIVITY, PEAK_DISTANCE_MS=PEAK_DISTANCE_MS,
                                      PEAK_PROMINENCE_FRAC=PEAK_PROMINENCE_FRAC, RHO_FLOOR=RHO_FLOOR))), flush=True)
    loaded = {}
    for rec in RECORDS:
        try:
            loaded[rec] = load_record(rec, data_dir)
        except Exception as e:  # noqa: BLE001
            loaded[rec] = e
    for cell, det in cells():
        for detrend in ((True, False) if cell == "primary" else (True,)):
            for rec in RECORDS:
                L = loaded[rec]
                if isinstance(L, Exception):
                    o = dict(excluded=f"not loadable: {type(L).__name__}: {L}")
                else:
                    ecg, bp, fs, names = L
                    o = score_record(ecg, bp, fs, det, detrend_phase=detrend); o["fs"] = fs; o["sig_name"] = names
                print(json.dumps(dict(cell=cell, detrend_phase=detrend, record=rec, det=det, **o)), flush=True)


# ---------------------------------------------------------------- scoring
def verdict(frac, p):
    if frac >= PASS_FRAC and p < ALPHA:
        return "PASS"
    if frac < FAIL_FRAC:
        return "FAIL"
    return "INDETERMINATE"


def score(path):
    rows = [json.loads(l) for l in open(path) if l.startswith("{") and '"cell"' in l]
    cellnames = []
    for r in rows:
        if r["cell"] not in cellnames: cellnames.append(r["cell"])
    print("=" * 110); print("CARD scoring — thresholds from prereg/card/PREREG.md; per-record values for the primary cell"); print("=" * 110)
    res = {}
    for cell in cellnames:
        v = [r for r in rows if r["cell"] == cell and r["detrend_phase"] is True]
        for key, label in (("bp", "CARD-1 BP arc vs RR"), ("ecg", "CARD-2 ECG arc vs RR")):
            scored = [r for r in v if "excluded" not in r and key in r and "excluded" not in r[key] and r[key]["rho_ok"]]
            excl = [r for r in v if "excluded" in r or key not in r or "excluded" in r[key] or not r[key]["rho_ok"]]
            k = sum(r[key]["passes"] for r in scored); n = len(scored)
            frac = k / n if n else float("nan"); p = float(binomtest(k, n, 0.5).pvalue) if n else float("nan")
            plain = sum(r[key]["cv_arc"] < r[key]["cv_clock"] for r in scored)
            res[(cell, key)] = dict(k=k, n=n, frac=frac, p=p, v=verdict(frac, p), excl=len(excl), plain=plain)
            if cell == "primary":
                print(f"\n[{label}, primary cell]")
                for r in sorted(scored, key=lambda r: r["record"]):
                    q = r[key]
                    print(f"  {r['record']} beats={r['n_events']:4d} rho={q['rho']:5.1f} cv_arc={q['cv_arc']:.3f} cv_clock={q['cv_clock']:.3f} cv_amp={q['cv_amp']:.3f} "
                          f"ci=({q['ci95'][0]:+.3f},{q['ci95'][1]:+.3f}) ci_amp=({q['ci95_amp'][0]:+.3f},{q['ci95_amp'][1]:+.3f}) -> {'PASS' if q['passes'] else 'FAIL'}")
                for r in excl:
                    why = r.get("excluded") or (r.get(key, {}).get("excluded")) or (f"rho {r[key]['rho']:.2f} < {RHO_FLOOR}" if key in r else "no channel")
                    print(f"  {r['record']} EXCLUDED: {why}")
                print(f"  PASS {k}/{n} = {frac:.3f}, p = {p:.4f}; plain cv_arc<cv_clock {plain}/{n}; excluded {len(excl)} -> {verdict(frac, p)}")
        # CARD-3
        c3 = [r for r in v if "card3" in r and "excluded" not in r["card3"]]
        k3 = sum(r["card3"]["passes"] for r in c3); n3 = len(c3)
        res[(cell, "card3")] = dict(k=k3, n=n3, frac=k3 / n3 if n3 else float("nan"))
        if cell == "primary":
            print("\n[CARD-3 antipodal-cut arc vs peak-cut arc on BP, primary cell]")
            for r in sorted(c3, key=lambda r: r["record"]):
                q = r["card3"]
                print(f"  {r['record']} ant={q['n_antipodal']:4d} pk={q['n_peak']:4d} cv_ant={q['cv_arc_antipodal']:.3f} cv_pk={q['cv_arc_peakcut']:.3f} "
                      f"ci=({q['ci95'][0]:+.3f},{q['ci95'][1]:+.3f}) |antipode-extremum| median {q['median_antipode_extremum_s']:.3f}s -> {'PASS' if q['passes'] else 'FAIL'}")
            print(f"  antipodal more regular than peak-cut in {k3}/{n3} records (DIAGNOSTIC, not scored — see prereg)")
            # detrend sensitivity for CARD-3
            v2 = [r for r in rows if r["cell"] == cell and r["detrend_phase"] is False and "card3" in r and "excluded" not in r["card3"]]
            print(f"  (detrend_phase=False: {sum(r['card3']['passes'] for r in v2)}/{len(v2)})")
    print("\n" + "-" * 110)
    for key, hid in (("bp", "CARD-1"), ("ecg", "CARD-2")):
        t = res[("primary", key)]
        flips = sum(1 for c in cellnames if c != "primary" and res[(c, key)]["v"] != t["v"])
        print(f"{hid}: {t['k']}/{t['n']} (frac {t['frac']:.3f}, p {t['p']:.4f}) -> {t['v']}; sensitivity flips {flips}/{len(cellnames)-1} -> {'FRAGILE' if flips > 1 else 'not fragile'}")
        for c in cellnames:
            tt = res[(c, key)]
            print(f"   {c:22s} {tt['k']:2d}/{tt['n']:2d} plain {tt['plain']:2d}/{tt['n']:2d} excl {tt['excl']:2d} {tt['v']}")
    t = res[("primary", "card3")]
    print(f"CARD-3 (diagnostic, not scored): antipodal-cut arc more regular than peak-cut arc in {t['k']}/{t['n']} records")


# ---------------------------------------------------------------- synthetic smoke (no data)
def synth(fs=1000.0, seconds=200.0, seed=0):
    rng = np.random.default_rng(seed)
    n_beats = int(seconds / 0.8) + 2
    rr = 0.8 * rng.normal(1, 0.06, n_beats); rr = np.clip(rr, 0.5, 1.2)
    t_beats = np.cumsum(rr); t = np.arange(0, seconds, 1 / fs)
    ecg = np.zeros_like(t); bp = np.zeros_like(t) + 80.0
    for tb, r in zip(t_beats, rr):
        ecg += 1.0 * np.exp(-((t - tb) / 0.012) ** 2) - 0.15 * np.exp(-((t - tb + 0.03) / 0.02) ** 2) + 0.25 * np.exp(-((t - tb - 0.25) / 0.05) ** 2)
        a = 40.0 * rng.normal(1, 0.08)
        u = np.clip((t - tb - 0.15) / r, 0.0, 1.0)
        bp += a * np.where(u < 1, np.exp(-u / 0.35) * (1 - np.exp(-u / 0.03)) * (1 + 0.15 * np.exp(-((u - 0.35) / 0.04) ** 2)), 0.0)
    ecg += 0.02 * rng.standard_normal(len(t)); bp += 0.3 * rng.standard_normal(len(t))
    return ecg, bp, fs


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "smoke":
        ecg, bp, fs = synth()
        ev = rpeaks(ecg, fs, **PRIMARY); print("detected beats:", len(ev), "mean RR s:", round(float(np.mean(np.diff(ev)) / fs), 3))
        o = score_record(ecg, bp, fs, PRIMARY); print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk in ('cv_arc', 'cv_clock', 'cv_amp', 'passes', 'rho', 'cv_arc_antipodal', 'cv_arc_peakcut')}) for k, v in o.items()}))
    elif cmd == "run":
        run_all(Path(sys.argv[2]) if len(sys.argv) > 2 else DATA)
    elif cmd == "score":
        score(sys.argv[2])
    else:
        raise SystemExit(__doc__)
