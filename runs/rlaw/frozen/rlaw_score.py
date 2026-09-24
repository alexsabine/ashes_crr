"""RLAW scorer: the regeneration law (CRR 2.0) on five domains (prereg/rlaw/PREREG.md). Frozen at hash time.

    uv run python runs/rlaw/frozen/rlaw_score.py [--raw data/raw/rlaw] [--json runs/rlaw/results.json]

The law: a system that regenerates from its settled past weights its newest input by alpha* = K(v_own).
- v_own is the drift of the input the system receives, per occasion, in the system's own resolvable steps.
- alpha_hat is the partial-adjustment weight the system actually uses.

Both are measured per unit. The level test asks whether alpha_hat is within a factor of 2 of alpha*. Every verdict is
computed here from the numbers (R15). Nothing below reads a threshold from the data."""
import argparse
import itertools
import json
import math
import pathlib
import sys

import numpy as np
from scipy.stats import spearmanr

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from rlaw_lib import K, ml_v, mom_v, v_own, alpha_hat, fit_q2, arm_env, rate_table, table_rate, ALPHA_GRID  # noqa: E402
from rlaw_load import read_xlsx_sheet, fred_csv, uscrn_daily, kool_subjects  # noqa: E402

LOG2 = math.log(2.0)
N_BOOT, BOOT_SEED = 2000, 0
TRACK_MIN_RHO = 0.3
PRIMARY = dict(vest="ml", own=True, lag=0, alt=False)
SPF_VARS = {  # SPF root: (FRED series, kind, scale, delta in the forecast's units)
    "UNEMP": ("UNRATE", "level", 1.0, 0.1), "HOUSING": ("HOUST", "level", 1e-3, 0.01), "TBILL": ("TB3MS", "level", 1.0, 0.1),
    "TBOND": ("GS10", "level", 1.0, 0.1), "CPI": ("CPIAUCSL", "infl", 1.0, 0.1), "CORECPI": ("CPILFESL", "infl", 1.0, 0.1),
    "PCE": ("PCEPI", "infl", 1.0, 0.1), "COREPCE": ("PCEPILFE", "infl", 1.0, 0.1)}
IVOL_PAIRS = [("VIX", "VIXCLS", "SP500"), ("VXN", "VXNCLS", "NASDAQ100"), ("OVX", "OVXCLS", "DCOILWTICO"),
              ("EVZ", "EVZCLS", "DEXUSEU"), ("VXD", "VXDCLS", "DJIA")]
MICH_END, MICH_END_ALT = np.datetime64("2024-03-01"), np.datetime64("2019-12-01")
MIN_ROWS = dict(spf=40, mich=150, ivol=500, ivol_week=100, soil=300)
SOIL_DEPTHS = (5, 10, 20, 50, 100)


# ---------------------------------------------------------------- helpers
def month_index(d):
    d = np.asarray(d).astype("datetime64[M]"); return d.astype(int)  # months since 1970-01


def monthly(path):
    d, v = fred_csv(path); return dict(zip(month_index(d).tolist(), v.tolist()))


def quarter_avg(mon):
    """{(year, q): mean of the three months} for quarters with all three months present."""
    out = {}
    for m, v in mon.items():
        y, mm = 1970 + m // 12, m % 12; out.setdefault((y, mm // 3 + 1), []).append(v)
    return {k: float(np.mean(v)) for k, v in out.items() if len(v) == 3 and not np.any(np.isnan(v))}


def qshift(y, q, k):
    i = y * 4 + (q - 1) - k; return i // 4, i % 4 + 1


def thirds(n):
    a, b = int(round(n / 3)), int(round(2 * n / 3)); return [(0, a), (a, b), (b, n)]


# ---------------------------------------------------------------- builders: each unit is dict(domain, id, s, x, delta)
def build_spf(raw, cell):
    units = []; wb = raw / "spf_medianLevel.xlsx"
    for root, (series, kind, scale, delta) in SPF_VARS.items():
        rows = read_xlsx_sheet(wb, root); head = [str(h).upper() if h is not None else "" for h in rows[0]]
        iy, iq = head.index("YEAR"), head.index("QUARTER")
        hz = [head.index(f"{root}{h}") for h in ((6,) if cell["alt"] else (3, 4, 5, 6))]
        qa = quarter_avg(monthly(raw / "fred" / f"{series}.csv"))
        if kind == "infl":
            real = {k: 100.0 * ((qa[k] / qa[qshift(*k, 1)]) ** 4 - 1.0) for k in qa if qshift(*k, 1) in qa}
        else:
            real = {k: v * scale for k, v in qa.items()}
        S, X = [], []
        for r in rows[1:]:
            if len(r) <= max(hz + [iy, iq]) or r[iy] is None or r[iq] is None: continue
            vals = [r[j] for j in hz]; s = float(np.mean(vals)) if all(isinstance(v, float) for v in vals) else np.nan
            S.append(s); X.append(real.get(qshift(int(r[iy]), int(r[iq]), 1 + cell["lag"]), np.nan))
        S, X = np.array(S), np.array(X); ok = np.where(~np.isnan(S))[0]
        if ok.size == 0: continue
        sl = slice(ok[0], ok[-1] + 1)
        units.append(dict(domain="spf", id=root, s=S[sl], x=X[sl], delta=delta))
    return units


def build_mich(raw, cell):
    cpi = monthly(raw / "fred" / "CPIAUCSL.csv"); mich = monthly(raw / "fred" / "MICH.csv")
    end = int(month_index(MICH_END_ALT if cell["alt"] else MICH_END)); ms = sorted(m for m in mich if m <= end)
    yoy = {m: 100.0 * (cpi[m] / cpi[m - 12] - 1.0) for m in cpi if m - 12 in cpi}
    S = np.array([mich[m] for m in ms]); X = np.array([yoy.get(m - 1 - cell["lag"], np.nan) for m in ms])
    return [dict(domain="mich", id=f"third{i + 1}", s=S[a:b], x=X[a:b], delta=1.0) for i, (a, b) in enumerate(thirds(len(ms)))]


def build_ivol(raw, cell):
    units = []
    for name, iv, px in IVOL_PAIRS:
        di, vi = fred_csv(raw / "fred" / f"{iv}.csv"); dp, vp = fred_csv(raw / "fred" / f"{px}.csv")
        okp = ~np.isnan(vp); dp, vp = dp[okp], vp[okp]
        r = np.full(vp.size, np.nan)
        pos = (vp[1:] > 0) & (vp[:-1] > 0); r[1:][pos] = np.log(vp[1:][pos] / vp[:-1][pos])
        rmap = dict(zip(dp.tolist(), r.tolist())); keep = ~np.isnan(vi)
        dates = [d for d in di[keep].tolist() if d in rmap]; ivm = dict(zip(di[keep].tolist(), vi[keep].tolist()))
        s = np.array([ivm[d] ** 2 for d in dates]); x = np.array([252.0 * (100.0 * rmap[d]) ** 2 for d in dates])
        delta = 2.0 * float(np.median(np.sqrt(s))) * 0.01
        if cell["alt"]:
            nb = s.size // 5; s = s[:nb * 5].reshape(nb, 5)[:, -1]; xb = x[:nb * 5].reshape(nb, 5)
            x = np.where(np.isnan(xb).any(axis=1), np.nan, xb.mean(axis=1))
        if cell["lag"]: x = np.concatenate([[np.nan], x[:-1]])
        units.append(dict(domain="ivol", id=name, s=s, x=x, delta=delta))
    return units


def build_soil(raw, cell, deep):
    units = []
    for f in sorted((raw / "uscrn2025").glob("CRND0103-2025-*.txt")):
        d = uscrn_daily(f); st = f.stem.replace("CRND0103-2025-", "")
        pairs = [(SOIL_DEPTHS[i], f"soil{SOIL_DEPTHS[i - 1]}", f"soil{SOIL_DEPTHS[i]}") for i in range(1, 5)] if deep else \
                [(5, "t_mean" if cell["alt"] else "t_avg", "soil5")]
        for depth, xk, sk in pairs:
            x = d[xk].copy()
            if cell["lag"]: x = np.concatenate([[np.nan], x[:-1]])
            units.append(dict(domain="soil_deep" if deep else "soil5", id=f"{st}@{depth}cm", s=d[sk], x=x, delta=0.1))
    return units


def build_twostep(raw, cell):
    subs = kool_subjects(raw / "kool" / "data.mat", raw / "kool" / "subinfo.mat")
    return [dict(domain="twostep", id=s["id"], sub=s) for s in subs]


# ---------------------------------------------------------------- per-unit measurement
def measure(units, cell, table=None):
    """Adds alpha_hat, alpha_star, v, v_own, n, excluded (reason or None) to each unit."""
    out = []
    if units and units[0]["domain"] == "twostep":
        alphas = ALPHA_GRID if cell["vest"] == "ml" else np.exp(np.linspace(math.log(0.005), 0.0, 400))
        for u in units:
            s = u["sub"]; nv = int(np.sum(s["valid"])); rec = dict(domain="twostep", id=u["id"], n=nv, excluded=None)
            if nv < (0.9 * s["n"] if cell["alt"] else 100): rec["excluded"] = f"valid trials {nv} of {s['n']}"; out.append(rec); continue
            a, b, nll, edge = fit_q2(s["state2"], s["choice2"], s["win"], s["valid"], alphas=alphas,
                                     beta_bounds=(0.0, 20.0 if cell["lag"] else 50.0), q0=0.5 if not cell["own"] else 0.0)
            env = arm_env(s["ps"], s["state2"], s["choice2"], s["valid"])
            rec.update(alpha_hat=a, beta_hat=b, alpha_edge=edge, alpha_star=table_rate(env["mean_gap"], table), v=env["v"],
                       v_own=env["v"], k_muth=float(K(env["v"])), mean_gap=env["mean_gap"], sd_drift=env["sd_drift"])
            out.append(rec)
        return out
    minr = MIN_ROWS["ivol_week"] if (units and units[0]["domain"] == "ivol" and cell["alt"]) else \
        MIN_ROWS["soil"] if units and units[0]["domain"].startswith("soil") else MIN_ROWS[units[0]["domain"]] if units else 0
    fitted = []
    for u in units:
        s, x = u["s"], u["x"]; ah, c, n = alpha_hat(s, x); nx = int(np.sum(~np.isnan(x)))
        rec = dict(domain=u["domain"], id=u["id"], n=n, n_env=nx, delta=u["delta"], excluded=None)
        if n < minr or nx < minr: rec["excluded"] = f"rows {n}, input values {nx} (< {minr})"; out.append(rec); continue
        rec.update(alpha_hat=ah, intercept=c); out.append(rec); fitted.append((rec, x))
    if cell["vest"] == "ml" and fitted:
        L = max(x.size for _, x in fitted); Y = np.full((len(fitted), L), np.nan)
        for i, (_, x) in enumerate(fitted): Y[i, :x.size] = x
        fit = ml_v(Y)
        for i, (rec, _) in enumerate(fitted):
            rec.update(v=float(fit["v"][i]), s_eta2=float(fit["sigma_eta2"][i]), s_eps2=float(fit["sigma_eps2"][i]), v_edge=bool(fit["edge"][i]))
    else:
        for rec, x in fitted:
            v, e2, n2 = mom_v(x); rec.update(v=float(v), s_eta2=float(e2), s_eps2=float(n2), v_edge=False)
    for rec, _ in fitted:
        vo = float(v_own(rec["s_eta2"], rec["s_eps2"], rec["delta"])) if cell["own"] else rec["v"]
        rec.update(v_own=vo, alpha_star=float(K(vo)), k_muth=float(K(rec["v"])))
    return out


def logerr(a, b):
    return abs(math.log(a / b)) if (a is not None and b is not None and np.isfinite(a) and np.isfinite(b) and a > 0 and b > 0) else math.inf


# ---------------------------------------------------------------- verdicts
def level_threshold(domain, n):
    if domain == "twostep": return math.ceil(0.5 * n)
    return math.ceil(2 * n / 3) if n >= 6 else n


def verdicts(recs, domain, tracking):
    used = [r for r in recs if r["excluded"] is None]; n = len(used)
    for r in used: r["logerr"] = logerr(r["alpha_hat"], r["alpha_star"])
    k = sum(r["logerr"] <= LOG2 for r in used); th = level_threshold(domain, n)
    out = dict(n_units=n, n_excluded=len(recs) - n, within_x2=k, threshold=th, level="PASS" if n > 0 and k >= th else "FAIL")
    pos = [r["alpha_hat"] for r in used if np.isfinite(r["alpha_hat"]) and r["alpha_hat"] > 0]
    if n >= 2:
        base = []
        for r in used:
            others = [q["alpha_hat"] for q in used if q is not r and np.isfinite(q["alpha_hat"]) and q["alpha_hat"] > 0]
            base.append(logerr(r["alpha_hat"], float(np.median(others))) if others else math.inf)
        ml, mb = float(np.median([r["logerr"] for r in used])), float(np.median(base))
        out.update(law_median_logerr=ml, const_median_logerr=mb, const_within_x2=int(sum(b <= LOG2 for b in base)),
                   baseline="PASS" if ml < mb else "FAIL")
    else:
        out.update(baseline="NOT SCORED (one unit)")
    if tracking:
        a = np.array([r["alpha_hat"] for r in used]); p = np.array([r["alpha_star"] for r in used])
        rho = float(spearmanr(a, p).statistic) if n >= 3 else float("nan")
        rng = np.random.default_rng(BOOT_SEED); bs = []
        for _ in range(N_BOOT):
            i = rng.integers(0, n, n)
            if np.unique(a[i]).size > 1 and np.unique(p[i]).size > 1: bs.append(spearmanr(a[i], p[i]).statistic)
        lo, hi = (float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975))) if bs else (float("nan"), float("nan"))
        out.update(spearman=rho, spearman_ci=[lo, hi], tracking="PASS" if (rho >= TRACK_MIN_RHO and lo > 0) else "FAIL")
    # the domain's row (R7 folded in): the level test AND the law beats the leave-one-unit-out constant; in the two-step
    # domain the law's prediction is nearly the same for every subject (a constant itself), so the row is the level test
    base_ok = out["baseline"] == "PASS" or domain == "twostep"
    out["row"] = "PASS" if out["level"] == "PASS" and base_ok else "FAIL"
    out["median_alpha_hat"] = float(np.median(pos)) if pos else float("nan")
    out["median_alpha_star"] = float(np.median([r["alpha_star"] for r in used])) if used else float("nan")
    return out


DOMAINS = [("spf", build_spf, False), ("mich", build_mich, False), ("ivol", build_ivol, False),
           ("soil5", lambda raw, c: build_soil(raw, c, False), True), ("soil_deep", lambda raw, c: build_soil(raw, c, True), True),
           ("twostep", build_twostep, False)]
ROW = {"spf": "RLAW-1", "mich": "RLAW-2", "ivol": "RLAW-3", "soil5": "RLAW-4", "soil_deep": "RLAW-4D", "twostep": "RLAW-5"}
CELLS = [dict(vest=a, own=b, lag=c, alt=d) for a, b, c, d in itertools.product(("ml", "mom"), (True, False), (0, 1), (False, True))]


def fmt(x, nd=4):
    return "nan" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{nd}f}"


def cell_name(c):
    return f"v:{c['vest']} own:{'on' if c['own'] else 'off'} lag:+{c['lag']} alt:{'yes' if c['alt'] else 'no'}"


def run(raw, only=None):
    table = rate_table(); res = dict(rate_table=dict(gaps=table[0].tolist(), rates=table[1].tolist()), domains={})
    print("RLAW scorer: the regeneration law alpha* = K(v_own) on five domains (prereg/rlaw/PREREG.md)")
    print("two-step optimal constant rate by mean visit gap (M13 rule): " + ", ".join(f"{g:g}: {r:.3f}" for g, r in zip(*table)))
    for dom, builder, tracking in DOMAINS:
        if only and dom not in only: continue
        cells = {}
        for c in CELLS:
            recs = measure(builder(raw, c), c, table); v = verdicts(recs, dom, tracking); cells[cell_name(c)] = dict(verdict=v, units=recs if c == PRIMARY else None)
        prim = cells[cell_name(PRIMARY)]; pv = prim["verdict"]
        print(f"\n== {ROW[dom]} ({dom}), primary cell {cell_name(PRIMARY)}")
        print("   unit | n | alpha_hat | alpha* = K(v_own) | K(v) (Muth, instrument unit) | v_hat | v_own | log(alpha_hat/alpha*) | within x2")
        for r in prim["units"]:
            if r["excluded"]: print(f"   {r['id']} | EXCLUDED: {r['excluded']}"); continue
            le = logerr(r["alpha_hat"], r["alpha_star"]); sg = math.log(r["alpha_hat"] / r["alpha_star"]) if np.isfinite(le) else float("nan")
            print(f"   {r['id']} | {r['n']} | {fmt(r['alpha_hat'])} | {fmt(r['alpha_star'])} | {fmt(r['k_muth'])} | {fmt(r['v'])} | {fmt(r['v_own'])} | "
                  f"{fmt(sg, 3)} | {'yes' if le <= LOG2 else 'no'}")
        print(f"   level: {pv['within_x2']}/{pv['n_units']} units within x2 (threshold {pv['threshold']}; excluded {pv['n_excluded']}) -> {pv['level']}")
        if "law_median_logerr" in pv:
            print(f"   baseline (leave-one-unit-out constant): law median |log err| {pv['law_median_logerr']:.6f} ({pv['law_median_logerr']:.3f}) vs constant "
                  f"{pv['const_median_logerr']:.6f} ({pv['const_median_logerr']:.3f}); constant within x2 {pv['const_within_x2']}/{pv['n_units']} -> law beats constant: {pv['baseline']}")
        else:
            print(f"   baseline: {pv['baseline']}")
        if tracking:
            print(f"   tracking: Spearman(alpha_hat, alpha*) {pv['spearman']:.6f} ({pv['spearman']:.3f}), bootstrap 95% CI {pv['spearman_ci'][0]:.3f} to {pv['spearman_ci'][1]:.3f} "
                  f"(PASS needs >= {TRACK_MIN_RHO} and CI above 0) -> {pv['tracking']}")
        print(f"   row {ROW[dom]}: level {pv['level']} AND law beats constant {pv['baseline']}{' (not required in the two-step domain)' if dom == 'twostep' else ''} -> {pv['row']}")
        keys = ["row", "level", "baseline"] + (["tracking"] if tracking else [])
        print("   sensitivity (16 cells; for twostep the factors read: v -> alpha grid 200/400 (ml/mom), own -> Q0 0/0.5 (on/off), lag -> beta bound 50/20, alt -> exclusion >10% missed):")
        flips = {k: 0 for k in keys}
        for name, cv in cells.items():
            v = cv["verdict"]; line = "; ".join(f"{k} {v[k]}" for k in keys)
            for k in keys:
                if v[k] != pv[k]: flips[k] += 1
            print(f"      {name}: {v['within_x2']}/{v['n_units']} within x2; {line}")
        frag = {k: ("FRAGILE" if flips[k] > 1 else "not fragile") for k in keys}
        print("   flips against the primary: " + "; ".join(f"{k} {flips[k]} -> {frag[k]}" for k in keys))
        res["domains"][dom] = dict(row=ROW[dom], primary=pv, flips=flips, fragile=frag, units=prim["units"],
                                   cells={k: v["verdict"] for k, v in cells.items()})
    if not only:
        lv = {d: res["domains"][d]["primary"]["row"] for d in ("spf", "mich", "ivol", "soil5", "twostep")}
        npass = sum(v == "PASS" for v in lv.values())
        res["RLAW-U"] = dict(passes=npass, of=5, verdict="PASS" if npass >= 4 else "FAIL")
        s5 = res["domains"]["soil5"]["primary"]
        res["RLAW-C"] = dict(row=s5["row"], tracking=s5["tracking"], verdict="PASS" if s5["row"] == "PASS" and s5["tracking"] == "PASS" else "FAIL")
        print(f"\n== RLAW-U (universality): domain rows passed {npass}/5 ({', '.join(f'{d} {v}' for d, v in lv.items())}); PASS needs >= 4 -> {res['RLAW-U']['verdict']}")
        print(f"== RLAW-C (the CRR-only content, a non-inferring system): soil 5 cm row {s5['row']}, tracking {s5['tracking']} -> {res['RLAW-C']['verdict']}")
    return res


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--raw", default="data/raw/rlaw"); ap.add_argument("--json", default=None)
    ap.add_argument("--only", nargs="*", default=None); a = ap.parse_args()
    res = run(pathlib.Path(a.raw), a.only)
    if a.json: pathlib.Path(a.json).write_text(json.dumps(res, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
