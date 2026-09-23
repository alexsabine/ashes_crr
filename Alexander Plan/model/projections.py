"""Funding scenarios for the CRR research programme, 2026 Q4 to 2030 (Alexander Plan; owner request prompt-log entry 101).

What this is. A deterministic Monte Carlo model of the money that could flow to the programme (grants, fellowships) and to
its researcher (employment), under explicit technical scenarios. It is NOT a forecast of what will happen: every input is
either (i) an anchor computed from this repository's own record, (ii) a figure reported by a web-search summary on
2026-09-23 (listed with its URL in docs/citations/alexander_plan_2026-09-23.md; summaries, not fetched pages), or
(iii) an ASSUMPTION, named as such, with a sensitivity sweep. The lower / middle / upper bounds are the 10th, 50th and
90th percentiles of the simulated totals. Every number the dossier quotes is printed here (R1).

The scenario tree (technical milestones; each resolves at the end of a year):
    M1 end 2027  a held-out PASS-1 row (or an AI-safety construction shown on a learned model under a declared test)
    M2 end 2028  a replication under a fresh prereg (PASS-2), given M1
    M3 end 2029  uptake: a lab, a standard or a funder adopts the method, given M2
    S0 = no M1; S1 = M1 only; S2 = M1 and M2; S3 = M1, M2 and M3.
Anchors from the record (docs/notes/2026-09-22_epistemic_status.md §1; row ids checked against ledger/LEDGER.md below):
    held-out scored rows: PASS-0 EQ2-1b, EQ3-I; FAIL MEAS2-1, EQX-2, EQ3-1 -> 5 rows, 0 PASS-1
    replication attempts: 1 (EQ3-1 replicating EQ2-1b), successes 0
    p(PASS-1 per study) by Laplace's rule (k + 1) / (n + 2); Jeffreys (k + 1/2) / (n + 1) in the sensitivity table.
    uv run python "Alexander Plan/model/projections.py" > "Alexander Plan/model/projections.txt"
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SEED = 20260923; N_DRAW = 20000
YEARS = ("2026Q4", "2027", "2028", "2029", "2030"); YEAR_FRAC = (0.25, 1.0, 1.0, 1.0, 1.0)

# ---------------------------------------------------------------- (i) anchors from the repository's record
HELD_OUT = {"EQ2-1b": "PASS-0", "EQ3-I": "PASS-0", "MEAS2-1": "FAIL", "EQX-2": "FAIL", "EQ3-1": "FAIL"}
N_PASS1 = 0; REPL_ATTEMPTS = 1; REPL_SUCCESSES = 0
EQ3_OMEGA_GRID = 9                     # the Ω grid of CLAUDE.md §6 used in EQ3 (nine points)

# ---------------------------------------------------------------- (ii) reported figures (search summaries, 2026-09-23)
REPORTED = {
    "ltff_accept": (0.193, "Long-Term Future Fund acceptance rate, May 2023 - March 2024"),
    "nsf_rate": (0.19, "NSF funding rate, FY2025 (reported fall from an estimated 0.27)"),
    "crf_lo": (5000, "Corrigibility Research Fund, typical grant, low (USD)"),
    "crf_hi": (35000, "Corrigibility Research Fund, typical grant, high (USD)"),
    "crf_total": (200000, "Corrigibility Research Fund, 2026 total (USD)"),
    "aisi_lo_gbp": (50000, "UK AISI Alignment Project, grant low (GBP)"),
    "aisi_hi_gbp": (1000000, "UK AISI Alignment Project, grant high (GBP)"),
    "aisi_total_gbp": (27000000, "UK AISI Alignment Project, first round total (GBP)"),
    "aisi_projects": (60, "UK AISI Alignment Project, first round projects"),
    "fmf_total": (5000000, "Frontier Model Forum AI Safety Fund, Dec 2025 cohort, more than (USD)"),
    "fmf_grantees": (11, "Frontier Model Forum AI Safety Fund, Dec 2025 cohort, grantees"),
    "anth_week": (3850, "Anthropic Fellows stipend per week (USD)"),
    "mats_week": (1250, "MATS stipend per week (USD)"),
    "sal_lo": (97000, "AI safety researcher salary, US range low (USD)"),
    "sal_med": (141000, "AI safety researcher salary, US median (USD)"),
    "sal_hi": (187000, "AI safety researcher salary, US range high (USD)"),
    "frontier_lo": (600000, "frontier-lab senior individual contributor, total compensation low (USD)"),
    "frontier_hi": (900000, "frontier-lab senior individual contributor, total compensation high (USD)"),
    "mkt_2025": (3.61e9, "AI safety market 2025 (USD; Research and Markets)"),
    "mkt_2026": (4.9e9, "AI safety market 2026 (USD; Research and Markets)"),
    "mkt_2030": (16.56e9, "AI safety market 2030 forecast (USD; Research and Markets)"),
    "mkt_2030_alt": (13.4e9, "AI safety market 2030 forecast (USD; New Market Pitch)"),
    "eval_2025": (1.64e9, "AI safety evaluation market 2025 (USD; InsightAce)"),
    "uscis_i129": (1055, "USCIS Form I-129 fee for O petitions (USD)"),
    "uscis_asylum": (600, "USCIS Asylum Program Fee (USD)"),
    "uscis_premium": (2965, "USCIS premium processing, Form I-907 (USD)"),
    "o1_approval": (0.94, "O-1 approval rate FY2025 (share of adjudicated petitions)"),
    "o1_rfe": (0.187, "O-1 share receiving a Request for Evidence, FY2025 to date"),
}

# context figures quoted in the dossier but not used by the model (search summaries, 2026-09-23)
CONTEXT = (
    ("Palisade 2025 tests: share of trials in which Grok 4 resisted shutdown", "nearly 0.90"),
    ("Palisade 2025 tests: share for codex-mini", "about 0.40 to 0.50"),
    ("UK AISI Alignment Project: OpenAI's contribution", "GBP 5.6M"),
    ("UK AISI Alignment Project: AISI's initial funding", "GBP 15M"),
    ("Frontier Model Forum AI Safety Fund: established with", "over USD 10M"),
    ("Long-Term Future Fund: acceptance Jan 2022 - Apr 2023, including desk rejections", "0.374"),
    ("Anthropic Fellows: compute per fellow per month", "about USD 15k"),
    ("O-1: share approved after a Request for Evidence", "0.709"),
    ("O-1: regular processing, mid-2026", "up to about 12.5 months"),
    ("O-1: premium processing", "action within 15 business days"),
    ("O petitions completed, FY2025", "nearly 32,000"),
    ("O-1A: evidentiary criteria to meet (absent a major internationally recognised award)", "at least 3 of 8"),
    ("California Executive Order N-9-26 (18 Sept 2026): recommendations due", "16 Nov 2026"),
    ("EU AI Act, general-purpose models: enforcement powers from 2 Aug 2026; fines up to", "EUR 15M or 0.03 of global turnover, whichever is higher"),
)

# ---------------------------------------------------------------- (iii) assumptions (named; swept below)
ASSUME = {
    "fx_usd_per_gbp": (1.30, "USD per GBP, for the AISI grant range (not sourced)"),
    "anth_weeks": (16, "an Anthropic-Fellows-type fellowship counted as 16 weeks ('four months')"),
    "n_studies_2027": (3, "held-out studies scored by end 2027: EQ4 and T1x2 (pre-registered) and one AI-safety study"),
    "p_uptake": (0.30, "P(M3 uptake by end 2029 | M2): no anchor exists"),
    "small_apps": (2, "small-grant applications per year"),
    "medium_apps": (1, "medium-grant applications per year, from 2027"),
    "fellow_apps": (1, "fellowship applications per year"),
}
# success-rate multipliers on the reported base rates, by programme state (a proposal resting on toy results is weaker
# than one resting on a replicated result): ASSUMPTIONS
MULT = {"pre": 0.5, "S0": 0.25, "S1": 1.0, "S2": 1.5, "S3": 2.0}
FELLOW_P = {"pre": 0.05, "S0": 0.03, "S1": 0.10, "S2": 0.20, "S3": 0.30}          # ASSUMPTION: no published rate found
EMPLOY_P = {"pre": 0.5, "S0": 0.5, "S1": 0.7, "S2": 0.8, "S3": 0.9}               # ASSUMPTION: P(a paid research role that year, if not already in one)
FRONTIER_P_S3 = 0.5                                                               # ASSUMPTION: P(frontier-lab role | S3, employed)
RETAIN = 0.9                                                                      # ASSUMPTION: P(a paid role continues into the next year)


def check_anchors():
    led = (ROOT / "ledger" / "LEDGER.md").read_text()
    for rid in HELD_OUT:
        assert re.search(rf"^\| {re.escape(rid)} \|", led, re.M), rid
    note = (ROOT / "docs" / "notes" / "2026-09-22_epistemic_status.md").read_text()
    assert "No row is PASS-1" in note and "Two, both PASS-0" in note
    return len(HELD_OUT), sum(v.startswith("PASS") for v in HELD_OUT.values())


def tree(p_study, p_repl, p_up, n_studies):
    p1 = 1 - (1 - p_study) ** n_studies; p2 = p_repl; p3 = p_up
    return dict(p1=p1, p2=p2, p3=p3, S0=1 - p1, S1=p1 * (1 - p2), S2=p1 * p2 * (1 - p3), S3=p1 * p2 * p3)


def simulate(tr, rate_scale=1.0, seed=SEED, n=N_DRAW):
    R = {k: v[0] for k, v in REPORTED.items()}; A = {k: v[0] for k, v in ASSUME.items()}
    rng = np.random.default_rng(seed)
    m1 = rng.random(n) < tr["p1"]; m2 = m1 & (rng.random(n) < tr["p2"]); m3 = m2 & (rng.random(n) < tr["p3"])
    final = np.where(m3, 3, np.where(m2, 2, np.where(m1, 1, 0)))
    proj = np.zeros((n, len(YEARS))); pers = np.zeros((n, len(YEARS))); employed = np.zeros(n, bool)
    base_rate = 0.5 * (R["ltff_accept"] + R["nsf_rate"])
    for j, (y, f) in enumerate(zip(YEARS, YEAR_FRAC)):
        if y in ("2026Q4", "2027"): state = np.full(n, "pre", dtype=object)
        elif y == "2028": state = np.where(m1, "S1", "S0").astype(object)
        elif y == "2029": state = np.where(m2, "S2", np.where(m1, "S1", "S0")).astype(object)
        else: state = np.where(m3, "S3", np.where(m2, "S2", np.where(m1, "S1", "S0"))).astype(object)
        mult = np.array([MULT[s] for s in state]); fel = np.array([FELLOW_P[s] for s in state]); emp = np.array([EMPLOY_P[s] for s in state])
        for _ in range(1 if y == "2026Q4" else A["small_apps"]):
            win = rng.random(n) < np.minimum(1.0, base_rate * mult * rate_scale)
            proj[:, j] += win * rng.uniform(R["crf_lo"], R["crf_hi"], n)
        if y != "2026Q4":
            for _ in range(A["medium_apps"]):
                win = rng.random(n) < np.minimum(1.0, base_rate * mult * rate_scale)
                proj[:, j] += win * rng.uniform(R["aisi_lo_gbp"], R["aisi_hi_gbp"], n) * A["fx_usd_per_gbp"]
            for _ in range(A["fellow_apps"]):
                win = rng.random(n) < np.minimum(1.0, fel * rate_scale)
                proj[:, j] += win * R["anth_week"] * A["anth_weeks"]
        fresh = rng.random(n) < np.minimum(1.0, emp * rate_scale); kept = rng.random(n) < RETAIN
        employed = fresh if j == 0 else np.where(employed, kept | fresh, fresh)
        salary = rng.uniform(R["sal_lo"], R["sal_hi"], n)
        frontier = (state == "S3") & (rng.random(n) < FRONTIER_P_S3)
        salary = np.where(frontier, rng.uniform(R["frontier_lo"], R["frontier_hi"], n), salary)
        pers[:, j] = employed * salary * f
    return dict(final=final, proj=proj, pers=pers)


def pct(x): return np.percentile(x, [10, 50, 90])


def money(v): return f"${v:,.0f}"


def main():
    n_held, n_pass0 = check_anchors()
    print("Funding scenarios for the CRR programme, 2026 Q4 to 2030 (Alexander Plan/model/projections.py)")
    print(f"seed {SEED}, {N_DRAW} draws; bounds = 10th / 50th / 90th percentiles (lower / middle / upper)")
    print("[1] Anchors from the repository's record (row ids checked in ledger/LEDGER.md)")
    print(f"    held-out scored rows {n_held}: " + ", ".join(f"{k} {v}" for k, v in HELD_OUT.items()) + f"; PASS-0 {n_pass0}; PASS-1 {N_PASS1}")
    p_lap = (N_PASS1 + 1) / (n_held + 2); p_jef = (N_PASS1 + 0.5) / (n_held + 1); p0_lap = (n_pass0 + 1) / (n_held + 2)
    p_repl = (REPL_SUCCESSES + 1) / (REPL_ATTEMPTS + 2)
    print(f"    p(PASS-1 per study): Laplace {p_lap:.4f}, Jeffreys {p_jef:.4f}; p(PASS-0 per study), Laplace {p0_lap:.4f}")
    print(f"    p(replication | a PASS-1): Laplace on {REPL_SUCCESSES} of {REPL_ATTEMPTS} attempts {p_repl:.4f}")
    print("[2] Reported figures (search summaries 2026-09-23; see docs/citations/alexander_plan_2026-09-23.md)")
    for k, (v, d) in REPORTED.items(): print(f"    {k:15s} {v:>16,.3f}  {d}" if v < 10 else f"    {k:15s} {v:>16,.0f}  {d}")
    print("    context (quoted in the dossier, not used by the model):")
    for d, v in CONTEXT: print(f"        {d}: {v}")
    R = {k: v[0] for k, v in REPORTED.items()}; A = {k: v[0] for k, v in ASSUME.items()}
    print("    derived: AISI mean first-round grant " + money(R["aisi_total_gbp"] / R["aisi_projects"]).replace("$", "GBP ")
          + f"; FMF mean grant at least {money(R['fmf_total'] / R['fmf_grantees'])}; Anthropic-type fellowship {money(R['anth_week'] * A['anth_weeks'])}; "
          f"MATS 10 to 12 weeks {money(R['mats_week'] * 10)} to {money(R['mats_week'] * 12)}")
    cagr = (R["mkt_2030"] / R["mkt_2026"]) ** (1 / 4) - 1
    print(f"    derived: AI safety market implied growth 2026 -> 2030 {cagr:.4f} per year; path " + ", ".join(f"{2026 + t}: ${R['mkt_2026'] * (1 + cagr) ** t / 1e9:.2f}B" for t in range(5)))
    fee = R["uscis_i129"] + R["uscis_asylum"]
    print(f"    derived: O-1 USCIS fees {money(fee)} base, {money(fee + R['uscis_premium'])} with premium processing (attorney fees not included)")
    print("[3] Assumptions (named; swept in [6])")
    for k, (v, d) in ASSUME.items(): print(f"    {k:15s} {v:>8g}  {d}")
    print("    success-rate multiplier by state " + ", ".join(f"{k} {v:g}" for k, v in MULT.items()) + f" on the base rate {0.5 * (R['ltff_accept'] + R['nsf_rate']):.4f} (mean of LTFF and NSF)")
    print("    fellowship success by state " + ", ".join(f"{k} {v:g}" for k, v in FELLOW_P.items()) + "; employment by state " + ", ".join(f"{k} {v:g}" for k, v in EMPLOY_P.items())
          + f"; frontier-lab role given S3 and employed {FRONTIER_P_S3:g}; a role continues into the next year {RETAIN:g}")
    tr = tree(p_lap, p_repl, A["p_uptake"], A["n_studies_2027"])
    print("[4] Scenario tree (exact)")
    print(f"    p(M1 by end 2027) = 1 - (1 - {p_lap:.4f})^{A['n_studies_2027']} = {tr['p1']:.4f}; p(M2 | M1) = {tr['p2']:.4f}; p(M3 | M2) = {tr['p3']:.4f}")
    for s, name in (("S0", "no held-out result"), ("S1", "a result, not replicated"), ("S2", "replicated, no uptake"), ("S3", "replicated and taken up")):
        print(f"    {s} {name:26s} p = {tr[s]:.4f}")
    sim = simulate(tr)
    print("[5] Simulated money (USD), all scenarios together")
    print("    project funding (grants and fellowships) per year: lower | middle | upper | mean")
    for j, y in enumerate(YEARS):
        lo, md, hi = pct(sim["proj"][:, j]); print(f"    {y:7s} {money(lo):>12s} | {money(md):>12s} | {money(hi):>12s} | {money(sim['proj'][:, j].mean()):>12s}")
    cp = sim["proj"].sum(1); cs = sim["pers"].sum(1)
    lo, md, hi = pct(cp); print(f"    cumulative project funding 2026Q4-2030: lower {money(lo)} | middle {money(md)} | upper {money(hi)} | mean {money(cp.mean())} | P(zero) {np.mean(cp == 0):.4f}")
    print("    researcher compensation per year: lower | middle | upper | mean")
    for j, y in enumerate(YEARS):
        lo, md, hi = pct(sim["pers"][:, j]); print(f"    {y:7s} {money(lo):>12s} | {money(md):>12s} | {money(hi):>12s} | {money(sim['pers'][:, j].mean()):>12s}")
    lo, md, hi = pct(cs); print(f"    cumulative compensation 2026Q4-2030: lower {money(lo)} | middle {money(md)} | upper {money(hi)} | mean {money(cs.mean())}")
    print("    by final scenario: share of draws | cumulative project funding lower / middle / upper | cumulative compensation lower / middle / upper")
    for k in range(4):
        sel = sim["final"] == k; a = pct(cp[sel]); b = pct(cs[sel])
        print(f"    S{k} {sel.mean():.4f} | {money(a[0])} / {money(a[1])} / {money(a[2])} | {money(b[0])} / {money(b[1])} / {money(b[2])}")
    print("    mean project funding per year by final scenario: " + "; ".join(
        f"S{k} " + " ".join(f"{money(sim['proj'][sim['final'] == k, j].mean())}" for j in range(len(YEARS))) for k in range(4)))
    print("[6] Sensitivity (one change at a time): cumulative project funding middle | upper | P(S3)")
    cells = [("registered", dict(p=p_lap, up=A["p_uptake"], rs=1.0, ns=A["n_studies_2027"])),
             ("Jeffreys prior", dict(p=p_jef, up=A["p_uptake"], rs=1.0, ns=A["n_studies_2027"])),
             ("uptake 0.1", dict(p=p_lap, up=0.1, rs=1.0, ns=A["n_studies_2027"])),
             ("uptake 0.5", dict(p=p_lap, up=0.5, rs=1.0, ns=A["n_studies_2027"])),
             ("success rates x0.5", dict(p=p_lap, up=A["p_uptake"], rs=0.5, ns=A["n_studies_2027"])),
             ("success rates x2", dict(p=p_lap, up=A["p_uptake"], rs=2.0, ns=A["n_studies_2027"])),
             ("1 study in 2027", dict(p=p_lap, up=A["p_uptake"], rs=1.0, ns=1)),
             ("6 studies in 2027", dict(p=p_lap, up=A["p_uptake"], rs=1.0, ns=6))]
    for name, c in cells:
        t = tree(c["p"], p_repl, c["up"], c["ns"]); s = simulate(t, rate_scale=c["rs"]); x = s["proj"].sum(1)
        print(f"    {name:20s} middle {money(np.percentile(x, 50)):>12s} | upper {money(np.percentile(x, 90)):>12s} | P(S3) {t['S3']:.4f}")
    print("[7] Value at stake for the field (illustration, not an estimate): share of the 2030 AI safety market, only in S3")
    for share in (0.0001, 0.001, 0.01):
        v = share * R["mkt_2030"]; print(f"    share {share:g}: {money(v)} a year if S3; times P(S3) {tr['S3']:.4f} = {money(v * tr['S3'])} expected")
    print("[8] Continual learning: what a no-tuning rule would save, if it worked")
    save = 1 - 1 / EQ3_OMEGA_GRID
    print(f"    a {EQ3_OMEGA_GRID}-point weight grid replaced by one run saves {save:.4f} of that sweep's compute")
    for name, p in (("PASS-0 per study (Laplace)", p0_lap), ("PASS-1 per study (Laplace)", p_lap), ("replicated by end 2028 (tree)", tr["p1"] * tr["p2"])):
        print(f"    expected saving per unit of sweep compute, p(works) = {name} {p:.4f}: {save * p:.4f}")
    print("    status from the ledger: EQX the rule at Ω = 1 reduces to a fixed replay weight; EQ2-1b PASS-0, fragile; EQ3-1 FAIL on 1 of 6; EQ4 (the bounded rule) not yet run")


if __name__ == "__main__":
    main()
