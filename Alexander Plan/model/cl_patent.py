"""The continual-learning method and the EPO application in money terms, 2026 Q4 to 2030 (Alexander Plan §11; owner request,
prompt-log entry 103). A model, not a forecast. Separate from projections.py, so the numbers already quoted from that model
do not move.

What it does.
  [1] Re-reads the continual-learning record from the pinned outputs: the per-carrier results of the two held-out studies on
      the EWC arm (runs/eq2/score.txt, runs/eq3/score.txt), the fars defect (runs/eq3/exclusions.txt class counts), and the ledger
      rows the pipeline recorded as failures, sorted into the four kinds of Continuous_Learning/CONTINUOUS_LEARNING.md §7.5.
      It prints the strict (as registered) reading and a pipeline-adjusted reading that sets aside the one carrier on which
      the whole EWC family sat at chance. The adjusted reading is NOT a ledger verdict; it is what a fresh prereg with a class
      floor (study EQ4 carries one) would test.
  [2] Prints the properties that carry commercial value, each from its pinned output: the tuning-inclusive compute ratio
      (runs/eq2r_cc/dryrun_on_eq2_seen.txt, seen data), learning-rate x batch invariance (ledger EQ3-I), scale robustness
      under SGD (theory/checks/omega_vs_methods.txt), the Adam caution (theory/checks/omega_reprocessed.txt), the Omega plateau
      (ledger EQ3-P) and the bounded rule on poisoned batches (runs/eq4_dev/summary.txt, seen data, exploratory).
  [3] Simulates the value the rule would create at GPU/LLM scale if it transferred, and what an owner of a patent covering it
      could capture, under a technical tree whose first branch is anchored on the rule's own held-out record.
  [4] Sensitivity, one assumption at a time.
  [5] The patent calendar that bears on an applied use case (dates only; information, not legal advice).
Inputs are (i) parsed from pinned repository outputs, (ii) figures reported by web-search summaries on 2026-09-23 (URLs in
docs/citations/alexander_plan_2026-09-23.md; summaries, not fetched pages), or (iii) ASSUMPTIONS, named and swept.
    uv run python "Alexander Plan/model/cl_patent.py" > "Alexander Plan/model/cl_patent.txt"
"""
from __future__ import annotations

import datetime as dt
import math
import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SEED = 20260923; N_DRAW = 20000

# ---------------------------------------------------------------- (ii) reported figures (search summaries, 2026-09-23)
REPORTED = {
    "openai_compute_2024": (7.0e9, "OpenAI cloud compute spend, 2024 (Epoch AI)"),
    "openai_rnd_2024": (5.0e9, "of which R&D compute, 2024 (Epoch AI)"),
    "openai_experiments_2024": (4.5e9, "of which research, experiments and unreleased models, 2024 (Epoch AI)"),
    "openai_final_runs_2024": (0.5e9, "of which final training runs of released models, about, 2024 (Epoch AI)"),
    "lab_compute_2026": (50e9, "compute spend per frontier lab, 2026, OpenAI and Anthropic each, about (press summaries; sources differ)"),
    "openai_training_2026": (25e9, "OpenAI training cost projection, 2026 (press summary)"),
    "openai_training_2028": (121e9, "OpenAI training cost projection, 2028 (press summary)"),
    "epo_renewals_to_y7_eur": (5250, "EPO renewal fees for one application through year 7, 2026 rates (EUR)"),
}
CONTEXT = (
    ("RL post-training share of DeepSeek-R1's compute", "about 0.05 (Epoch AI summary)"),
    ("a single RL ablation run", "10,000 to 100,000 GPU hours (search summary)"),
    ("hyperscaler capital expenditure, 2026", "USD 660B to 690B (Futurum summary)"),
    ("EPO official fees", "most up about 0.05 from 1 April 2026"),
    ("European SME patents commercially exploited", "up to two thirds (EPO Patent Commercialisation Scoreboard)"),
    ("European universities' and public research organisations' inventions brought to market", "more than a third (EPO scoreboard)"),
    ("EPO Guidelines G-II 3.3", "a mathematical method contributes technical character by application to a specific field of technology "
     "and/or adaptation to a specific technical implementation; 'controlling a technical system' in general is not enough"),
    ("EPC Article 54 / 55", "no general grace period: the applicant's own earlier publication is prior art (Art. 55: six-month "
     "exceptions for evident abuse and recognised exhibitions only)"),
    ("EPC Article 123(2)", "an application may not be amended to contain subject matter extending beyond the content as filed"),
    ("35 U.S.C. 102(b)(1)(A)", "a US one-year grace period for the inventor's own disclosures"),
)

# ---------------------------------------------------------------- (iii) assumptions (named; swept in [4])
ASSUME = {
    "p_llm_given_gpu": (0.20, "P(the rule's advantage survives AdamW-trained LLM regimes | a GPU PASS-1): the repository's own check says the "
                              "scale advantage is an SGD property"),
    "p_adopt_given_llm": (0.30, "P(labs adopt | an LLM-scale pass)"),
    "s_reg_lo": (0.001, "share of experiment compute spent sweeping penalty / KL / anchor weights, low"),
    "s_reg_hi": (0.02, "share of experiment compute spent sweeping penalty / KL / anchor weights, high"),
    "confirm_configs": (3, "configurations a lab would still run to confirm the rule (of the instrument's 17)"),
    "rnd_share_2026": (5.0 / 7.0, "R&D share of 2026 lab compute, taken from the 2024 OpenAI split"),
    "n_labs_hi": (2, "frontier labs in the high end of the spend range"),
    "p_use_case_ok": (0.5, "P(an applied use case exists in the EPO application as filed and satisfies Art. 123(2))"),
    "p_grant_given_use": (0.7, "P(grant | such a use case; owner's statement: claims agreed in principle)"),
    "p_cover": (0.10, "P(granted claims cover an implementation a lab actually uses)"),
    "roy_lo": (0.005, "share of the value created a patent holder captures, low"),
    "roy_hi": (0.05, "share of the value created a patent holder captures, high"),
}
YEARS_VALUE = (2029, 2030)   # GPU study 2027, LLM test 2028, adoption 2029-2030 (timeline assumption)


def parse_carriers(path, row):
    line = next(l for l in path.read_text().splitlines() if l.startswith(row + " "))
    return [(c, float(d), float(s), int(a), int(b)) for c, d, s, a, b in
            re.findall(r"(\w+):([+\-]\d+\.\d+) \(step (\d+\.\d+); seeds not behind (\d)/(\d)\)", line)]


def laplace(k, n): return (k + 1) / (n + 2)


def usd(v): return f"${v:,.0f}"


def evidence():
    print("[1] The continual-learning record, re-read (EWC arm, the two held-out studies)")
    eq2 = parse_carriers(ROOT / "runs/eq2/score.txt", "EQ2-1"); eq3 = parse_carriers(ROOT / "runs/eq3/score.txt", "EQ3-1")
    rows = [("EQ2", *r) for r in eq2] + [("EQ3", *r) for r in eq3]
    for st, c, d, s, a, b in rows:
        print(f"    {st} {c:20s} rule - tuned {d:+.4f} (step {s:.2f}; seeds not behind {a}/{b}) -> {'not behind' if d > -s else 'BEHIND'}")
    counts = re.search(r"fars: .*?class counts \[([\d, ]+)\]", (ROOT / "runs/eq3/exclusions.txt").read_text())[1]
    empty = [int(x) for x in counts.split(",")].count(0)
    print(f"    fars class counts after the pre-registered subsample: [{counts}] -> {empty} empty class; the first task had one class and every "
          "EWC-family arm sat at chance there (CONTINUOUS_LEARNING.md §7.4)")
    nb = sum(d > -s for _, _, d, s, _, _ in rows); n = len(rows)
    print(f"    strict (as registered): not behind on {nb} of {n} carriers; study verdicts EQ2-1 PASS (PASS-0, fragile), EQ3-1 FAIL")
    print(f"    pipeline-adjusted (fars set aside as uninformative; NOT a ledger verdict): not behind on {nb} of {n - 1} informative carriers")
    print(f"    per-carrier Laplace: strict {laplace(nb, n):.4f}, adjusted {laplace(nb, n - 1):.4f}; per-study PASS-1 (0 of 2) {laplace(0, 2):.4f}, "
          f"PASS-0-level (1 of 2) {laplace(1, 2):.4f}")
    kinds = {"a pre-registered 'every carrier / every cell' criterion missed on one unit": ["EQX-2", "EQ3-1", "EQ3-C", "EQ3-A"],
             "a pre-registered control did not hold (the mechanism statement, not the measurement)": ["EQ2-4", "EQ3-3", "EQ3-4"],
             "the theory value Omega = 1 did not appear (a plateau instead)": ["EQX-2", "EQ2-6", "EQ3-6"],
             "a pipeline defect or a reduction to a constant": ["EQ2R-VOID", "EQX-1"]}
    led = (ROOT / "ledger/LEDGER.md").read_text()
    print("    what the pipeline recorded as failures, by kind (CONTINUOUS_LEARNING.md §7.5; ids checked in the ledger):")
    for k, ids in kinds.items():
        for i in ids: assert re.search(rf"^\| {re.escape(i)} \|", led, re.M), i
        print(f"        {len(ids)}  {k}: {', '.join(ids)}")
    return laplace(0, 2), laplace(1, 2)


def properties():
    print("[2] The properties that carry commercial value (pinned outputs)")
    dr = (ROOT / "runs/eq2r_cc/dryrun_on_eq2_seen.txt").read_text()
    m = re.search(r"tuned lambda ([\d.e+]+) over (\d+) configs, rule ([\d.e+]+) over 1 config, ratio ([\d.]+)", dr)
    ratio = float(m[4]); nconf = int(m[2])
    print(f"    tuning-inclusive compute (seen data, dry run): rule {m[3]} sample passes against the tuned weight's {m[1]} over {nconf} configurations, "
          f"ratio {ratio:.4f} -> saving {1 - ratio:.4f} of that sweep")
    led = (ROOT / "ledger/LEDGER.md").read_text()
    ei = re.search(r"^\| EQ3-I \|(?:[^|]*\|){4}([^|]*)\|", led, re.M)[1].strip()
    print(f"    learning-rate x batch invariance (EQ3-I, PASS-0): {ei[:150]}")
    ov = (ROOT / "theory/checks/omega_vs_methods.txt").read_text()
    om = re.search(r"^omega\s+\S+\s+[\d.]+\s+[\d.]+\s+([\d.]+)\s+([\d.]+) \|\s+([\d.]+)\s+([\d.]+)", ov, re.M)
    print(f"    scale robustness under SGD (synthetic): the rule's total {om[1]} ({om[2]} of the tuned weight) at F; {om[3]} ({om[4]} of the "
          f"re-tuned weight) at 16F; scale-robust methods {re.search(r'scale-robust methods [^:]*: (.*)', ov)[1]}")
    orp = (ROOT / "theory/checks/omega_reprocessed.txt").read_text()
    print("    the Adam caution (synthetic): " + re.search(r"computed: (the fixed weight is scale-robust under Adam too[^\n]*)", orp)[1])
    ep = re.search(r"^\| EQ3-P \|(?:[^|]*\|){4}([^|]*)\|", led, re.M)[1].strip()
    print(f"    Omega plateau (EQ3-P): {ep} grid points within a step of the best, per carrier")
    dev = (ROOT / "runs/eq4_dev/summary.txt").read_text()
    d = [float(x) for x in re.findall(r"POISON:.*?EQ-B k=2: [\d.]+ \(rule − EQ-B ([+\-][\d.]+); clip", dev)]
    print(f"    bounded rule EQ-B (registered kappa 2) under poisoned batches (seen data, exploratory, no verdict): rule - EQ-B on {len(d)} carriers "
          + ", ".join(f"{x:+.2f}" for x in d) + f" -> EQ-B ahead on {sum(x < 0 for x in d)} of {len(d)}; study EQ4 (held-out) not yet run")
    return ratio, nconf


def simulate(p_gpu, A, ratio, nconf, rng, p_llm=None, s_lo=None, s_hi=None, p_cover=None, n=N_DRAW):
    R = {k: v[0] for k, v in REPORTED.items()}
    p_llm = A["p_llm_given_gpu"] if p_llm is None else p_llm; s_lo = A["s_reg_lo"] if s_lo is None else s_lo
    s_hi = A["s_reg_hi"] if s_hi is None else s_hi; p_cover = A["p_cover"] if p_cover is None else p_cover
    ok = (rng.random(n) < p_gpu) & (rng.random(n) < p_llm) & (rng.random(n) < A["p_adopt_given_llm"])
    e_lo = R["openai_experiments_2024"]; e_hi = A["n_labs_hi"] * R["lab_compute_2026"] * A["rnd_share_2026"]
    e26 = np.exp(rng.uniform(math.log(e_lo), math.log(e_hi), n))
    g = np.exp(rng.uniform(0.0, 0.5 * math.log(R["openai_training_2028"] / R["openai_training_2026"]), n))
    s = np.exp(rng.uniform(math.log(s_lo), math.log(s_hi), n))
    f = rng.uniform(1 - A["confirm_configs"] / nconf, 1 - ratio, n)
    vals = {y: e26 * g ** (y - 2026) * s * f for y in YEARS_VALUE}           # value created in the field if adopted
    created = sum(vals.values()) * ok
    pat = (rng.random(n) < A["p_use_case_ok"]) & (rng.random(n) < A["p_grant_given_use"]) & (rng.random(n) < p_cover)
    roy = np.exp(rng.uniform(math.log(A["roy_lo"]), math.log(A["roy_hi"]), n))
    owner = created * pat * roy
    return dict(ok=ok, vals=vals, created=created, owner=owner, pat=pat)


def pct(x): return np.percentile(x, [10, 50, 90])


def main():
    print("The continual-learning method and the EPO application in money terms (Alexander Plan/model/cl_patent.py)")
    print(f"seed {SEED}, {N_DRAW} draws; lower / middle / upper = 10th / 50th / 90th percentiles")
    p_pass1, p_pass0 = evidence(); ratio, nconf = properties()
    print("[3a] Inputs")
    for k, (v, d) in REPORTED.items(): print(f"    reported {k:24s} {v:>18,.0f}  {d}")
    for d, v in CONTEXT: print(f"    context  {d}: {v}")
    A = {k: v[0] for k, v in ASSUME.items()}
    for k, (v, d) in ASSUME.items(): print(f"    ASSUMED  {k:18s} {v:>8.4g}  {d}")
    e_hi = A["n_labs_hi"] * REPORTED["lab_compute_2026"][0] * A["rnd_share_2026"]
    print(f"    derived: experiment compute of adopting labs in 2026, log-uniform from {usd(REPORTED['openai_experiments_2024'][0])} to {usd(e_hi)}; "
          f"yearly growth up to {math.sqrt(REPORTED['openai_training_2028'][0] / REPORTED['openai_training_2026'][0]):.4f}; share of a sweep saved "
          f"{1 - A['confirm_configs'] / nconf:.4f} to {1 - ratio:.4f}")
    print(f"    derived: P(GPU PASS-1) = Laplace on the rule's held-out studies, 0 PASS-1 of 2 = {p_pass1:.4f}")
    p_tech = p_pass1 * A["p_llm_given_gpu"] * A["p_adopt_given_llm"]
    p_pat = A["p_use_case_ok"] * A["p_grant_given_use"] * A["p_cover"]
    print(f"    derived: P(adopted by 2029) = {p_pass1:.4f} x {A['p_llm_given_gpu']:.2f} x {A['p_adopt_given_llm']:.2f} = {p_tech:.4f}; "
          f"P(a granted patent covers the used implementation) = {A['p_use_case_ok']:.2f} x {A['p_grant_given_use']:.2f} x {A['p_cover']:.2f} = {p_pat:.4f}")
    rng = np.random.default_rng(SEED); sim = simulate(p_pass1, A, ratio, nconf, rng)
    ok = sim["ok"]
    print("[3b] Value the rule would create in the field (saved sweep compute), USD")
    for y in YEARS_VALUE:
        lo, md, hi = pct(sim["vals"][y]); print(f"    {y}, if adopted:            lower {usd(lo)} | middle {usd(md)} | upper {usd(hi)} | mean {usd(sim['vals'][y].mean())}")
    lo, md, hi = pct(sim["created"])
    print(f"    2029-2030 cumulative, all futures: lower {usd(lo)} | middle {usd(md)} | upper {usd(hi)} | mean {usd(sim['created'].mean())} | "
          f"share of futures with any value {ok.mean():.4f}")
    lo, md, hi = pct(sim["created"][ok]); print(f"    2029-2030 cumulative, adopted futures only: lower {usd(lo)} | middle {usd(md)} | upper {usd(hi)}")
    print("[3c] What a patent holder could capture, USD (2029-2030)")
    lo, md, hi = pct(sim["owner"])
    print(f"    all futures: lower {usd(lo)} | middle {usd(md)} | upper {usd(hi)} | mean {usd(sim['owner'].mean())} | share of futures with any income "
          f"{(sim['owner'] > 0).mean():.4f}")
    sel = sim["owner"] > 0
    if sel.any():
        lo, md, hi = pct(sim["owner"][sel]); print(f"    futures with income only: lower {usd(lo)} | middle {usd(md)} | upper {usd(hi)}")
    print(f"    cost side: EPO renewal fees through year 7 for one application EUR {REPORTED['epo_renewals_to_y7_eur'][0]:,.0f} (attorney, validation and "
          "national fees not included)")
    print("[4] Sensitivity (one change at a time): mean value created 2029-2030 | mean patent-holder capture | P(adopted)")
    cells = [("registered", {}), ("GPU pass at the PASS-0 level (1 of 2)", dict(p_gpu=p_pass0)),
             ("LLM transfer 0.05 (Adam removes the advantage)", dict(p_llm=0.05)), ("LLM transfer 0.5", dict(p_llm=0.5)),
             ("sweep share 0.0005 to 0.005", dict(s_lo=0.0005, s_hi=0.005)), ("sweep share 0.005 to 0.05", dict(s_lo=0.005, s_hi=0.05)),
             ("patent covers 0.02", dict(p_cover=0.02)), ("patent covers 0.3", dict(p_cover=0.3))]
    for name, kw in cells:
        pg = kw.pop("p_gpu", p_pass1); r = simulate(pg, A, ratio, nconf, np.random.default_rng(SEED), **kw)
        pt = pg * kw.get("p_llm", A["p_llm_given_gpu"]) * A["p_adopt_given_llm"]
        print(f"    {name:46s} {usd(r['created'].mean()):>16s} | {usd(r['owner'].mean()):>12s} | {pt:.4f}")
    print("[5] The patent calendar that bears on an applied use case (dates; information, not legal advice)")
    filed = dt.date(2025, 8, 1); public = dt.date(2026, 9, 15)
    print(f"    EPO application filed August 2025 (owner's statement; day not given, the 1st used for arithmetic): {filed.isoformat()[:7]}")
    print(f"    Paris Convention priority year for filings elsewhere claiming it: ended {dt.date(2026, 8, 1).isoformat()[:7]}")
    print(f"    repository public since {public.isoformat()} (GitHub API: created_at 2026-09-15T04:06:50Z, visibility public)")
    print(f"    EPO: anything first published in the repository is prior art for any NEW European filing (no grace period); the pending "
          "application can only be amended within its content as filed (Art. 123(2))")
    print(f"    US: a filing on repository-disclosed matter would have to be made within one year of its first disclosure, i.e. no later than "
          f"{dt.date(2027, 9, 15).isoformat()} for matter first published on {public.isoformat()}")
    print(f"    a European patent's term runs 20 years from filing: to {dt.date(2045, 8, 1).isoformat()[:7]}")


if __name__ == "__main__":
    main()
