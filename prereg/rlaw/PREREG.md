# Pre-registration — RLAW: the regeneration law (CRR 2.0) on five domains where it can fail

- **Study id:** `rlaw`.
- **Written:** 2026-09-24 (prompt-log entry 137; AGENT_LOG 113, 114).
- **Timing.** Hashed, anchored and pushed on 2026-09-24. **No source below is fetched or opened before
  2026-09-25 00:00 UTC** (R3):
  - every estimator, unit and threshold here was defined on 2026-09-24;
  - SCL2's data step had already opened a dataset that day.
  - The fetch timestamps go into `data/manifests/rlaw.sha256`.
- **Author:** the agent, under CLAUDE.md §1.
- **Status of this file: DRAFT, not yet hashed.**
  - The gate (`gate_RLAW.txt`) is still running, and the admissibility list below is filled from it.
  - The file is merged to `main` at the owner's request (prompt-log entry 139) before the hash.
  - The hash, the OpenTimestamps proof and the tag follow in a later commit. Only the hashed version binds.
- **Outside the epistemic ladder.** CRR 2.0 is a different form of CRR, not in this repository's initial conditions.
  - By the owner's instruction (prompt-log entry 139), its RLAW rows go to the ledger and to `reports/rlaw.md`, but not
    into the epistemic ladder, its tables or its figures.
  - `Epistemic_Review/checks/ladder.py` skips rows whose id starts with RLAW.

## The law under test

**The law.** A system that regenerates from its settled past weights its newest input by

  **α\* = K(v_own)**, where K(v) = (v/2)(√(v² + 4) − v) (`theory/CRR.md` P4). Its memory depth is q\* = 1 − α\*.

- **v_own** is the drift of the input the system receives, per occasion. It is counted in the system's own resolvable
  steps (A1′): v_own = σ_η / √(σ_ε² + δ²/12).
  - σ_η² and σ_ε² are the drift and noise variances of a local-level (random walk plus noise) model of the input.
  - δ is the system's reporting quantum.
- **It has no free parameter.**
- **It amends O1.** `theory/CRR.md` O1 asks whether memory depth follows from the system's own state model "at Ω = 1".
  Declaration 1 (M7) shows that the Kalman balance gives equal pull only at v = 1/√2, so the law is not H-EQ. CRR 2.0
  drops "at Ω = 1".

**What the mathematics established first** (`Regeneration_Law/`; both outputs are pinned and copied here, covered by
the hash).
- `math_checks.txt` (Declaration 1). Three things hold:
  - K is the steady Kalman gain;
  - Muth's EWMA optimality;
  - the P3 mean age and unit invariance.

  The own unit lowers α\* when δ is comparable to σ_ε (M4). For an AR(1) input the local-level approximation is 2 % off
  the optimal gain (M8). ML is the estimator of v (M9).
- `operational_checks.txt` (Declaration 2).
  - **M11.** A linear time-invariant filter keeps its weight at every v. It meets the law at one v at most.
  - **M12.** Recovery at the unit lengths used here: 60-occasion units are not used.
  - **M13.** The two-step arm is mean-reverting, so the prediction there is the numerically optimal constant rate.
  - **M14.** The two-step recovery ceiling is 0.63 at α 0.05.

**What the literature check binds** (`docs/citations/rlaw_literature_2026-09-24.md`, read before this prereg).
- **The formula and its optimality for inferring systems are published** (Muth 1960; Kalman 1960; Harvey 1989).
  Domains 1, 2, 3 and 5 below test only whether those systems are Muth-optimal. **A pass there is not CRR's.**
- **Universality, including systems that do no inference, is not in the literature.** Domain 4 (soil temperature) is
  therefore **the only CRR-only test**.
- **Heat conduction is linear.** Its memory is set by diffusivity and depth, not by the variability of the forcing
  (FOUND as a counter-statement; M11). **The foreseeable result of domain 4 is FAIL, above all of its tracking row.**
- **Two-step learners: the foreseeable result is also FAIL.** In the two-step task, fitted second-stage learning rates
  (median about 0.42 in Daw 2011) sit far above the optimal gain. The ratio of about 8 is the literature agent's own
  computation.
- **These expectations are stated so that a pass is surprising and a fail is not over-read.** They do not enter any
  threshold.

## The five domains (all sources are absent from `data/SEEN.md` before this hash)

| row | domain | system (what regenerates) | its input x_t (what it receives at occasion t) | occasion | units | δ (own quantum) |
|---|---|---|---|---|---|---|
| RLAW-1 | professional forecasters | SPF median forecast, the mean of horizons 3–6 of each variable (`medianLevel.xlsx`) | the realised value of the quarter before the survey (FRED: UNRATE, HOUST/1000, TB3MS, GS10; annualised q/q inflation of CPIAUCSL, CPILFESL, PCEPI, PCEPILFE; quarterly averages of monthly values) | survey quarter | 8 variables: UNEMP, HOUSING, TBILL, TBOND, CPI, CORECPI, PCE, COREPCE, each from its first survey to 2026Q3 | 0.1 (0.01 for HOUSING, millions); an assumption, because the SPF does not document its precision |
| RLAW-2 | households | Michigan median expected inflation, MICH | year-on-year CPI inflation (CPIAUCSL) of the month before | month, 1978-01 to 2024-03 (before the 2024-04 web mode, which accepts decimals) | 3 contiguous thirds (185 months each) | 1 pp (the survey codes whole percents; Curtin 1996) |
| RLAW-3 | option markets | implied variance IV² (VIXCLS, VXNCLS, OVXCLS, EVZCLS, VXDCLS) | 252 × (100 r_t)², r_t the close-to-close log return of the underlying (SP500, NASDAQ100, DCOILWTICO, DEXUSEU, DJIA) | trading day | 5 index pairs, each over its FRED window (listed in `data/fetch_rlaw.py`) | 2 × median(IV) × 0.01 (IV is quoted to 0.01) |
| RLAW-4 | soil (no inference) | daily soil temperature at 5 cm (USCRN daily01 2025, field 24) | daily air temperature T_DAILY_AVG (field 9) | day | every 2025 station file | 0.1 °C |
| RLAW-4D | soil, deeper layers | soil temperature at 10, 20, 50, 100 cm | soil temperature at the layer above | day | every station × depth | 0.1 °C |
| RLAW-5 | human learners | the second-stage learning rate of the two-step task (Kool, Cushman & Gershman 2016, Daw paradigm, `data.mat` at wkool/tradeoffs commit 6f849e1) | the reward on each visit of a second-stage option | visit | subjects retained by the authors' own rule (exactly 150 rows, practice dropped) | none |

**The two measurements per unit, independent of each other.**
- **The memory actually used, α̂.** Partial adjustment with intercept: s_t − s_{t−1} = α̂ (x_t − s_{t−1}) + c, by least
  squares on every row where s_t, s_{t−1} and x_t are all present.
  - The intercept absorbs a constant bias, such as a variance risk premium, a soil–air offset, or a forecaster bias.
  - In RLAW-5, α̂ is the per-subject ML learning rate of a delta-rule learner on second-stage choices: α on a
    200-point log grid over [0.005, 1], β bounded in [0, 50], Q₀ = 0, as in Kool's code.
- **The prediction, α\*.**
  - RLAW-1 to 4D: K(v_own). σ_η² and σ_ε² come from the ML local-level fit on the input series x over the unit's
    occasions: 1001-point log grid on v over [10⁻³, 10²], parabolic refinement, missing values skipped by the filter.
  - RLAW-5: the numerically optimal constant rate at the subject's mean gap between visits of the same option. The table
    is computed by the frozen scorer (M13 rule: reflecting walk, sd 0.025, bounds 0.25/0.75, geometric gaps; 200
    seeds × 2000 visits). Muth's K(v) is printed beside it.

**Quality and exclusions (applied before scoring, counted and listed).**
- A unit is excluded below a minimum number of usable rows:
  - SPF: 40 rows;
  - Michigan: 150;
  - implied vol: 500 daily, 100 weekly;
  - soil: 300 rows and 300 input values.
- A subject is excluded with fewer than 100 valid trials.
- Soil stations with only 5/10 cm probes have no deeper units: their missing depths are excluded and counted.
- An α̂ ≤ 0 is kept and counted as outside every band. A v fit at the grid edge is flagged and kept.

## Hypotheses (verdicts computed by `rlaw_score.py`, R15)

| id | what is tested | PASS if | scored per |
|---|---|---|---|
| **RLAW-d** (d = 1, 2, 3, 4, 4D, 5): the domain row | (i) **level:** α̂ within a factor of 2 of α\*, i.e. \|log(α̂/α\*)\| ≤ log 2 (non-strict, two-sided); AND (ii) **R7:** the law beats the strongest simple alternative, a leave-one-unit-out constant (the median α̂ of the domain's other units) | (i) at least ⌈2N/3⌉ of N units if N ≥ 6, all N units if N < 6, ⌈N/2⌉ subjects in RLAW-5 (the M14 ceiling is 0.63); AND (ii) the law's median \|log error\| < the constant's (strict). In RLAW-5, (ii) is printed and not required: the law predicts nearly the same rate for every subject, so it is itself a constant there | unit |
| **RLAW-4T, RLAW-4DT** (tracking) | across units, α̂ rises with α\*: memory moves with the drift | Spearman ≥ 0.3 and the bootstrap 95 % CI (2000 resamples of units, seed 0) above 0 | unit |
| **RLAW-U** (universality) | the domain rows 1, 2, 3, 4 and 5 | at least 4 of 5 PASS | domain |
| **RLAW-C** (CRR-only) | a system that does no inference obeys the law | RLAW-4 AND RLAW-4T both PASS | — |

**Why (i) and (ii) are one row.** The gate shows that each half alone passes on a system that is not the law.
- "Beats a constant" alone passes on the over-reactor, the sluggish system and random memory, because the law's error is
  uniform there while the units' memories spread.
- The level test alone passes on a one-constant LTI system when the drifts are similar.

Together they fail on all four. **Tracking** tests only that memory moves with drift, so its must-fail surrogates are the
two that cut that link (random memory, one constant). It says nothing about the level.

**Admissibility (R4) is decided by `gate_RLAW.txt`, computed before this hash.**
- A row is admissible if the law-obeying synthetic system G+ passes it in at least 0.8 of replicates, and every must-fail
  surrogate passes it in at most 0.05.
- **A row the gate marks NOT ADMISSIBLE is computed and reported, with no verdict counted.** It is still printed with
  PASS or FAIL, labelled as not admissible.
- RLAW-U and RLAW-C take the domain rows as computed.

ADMISSIBILITY_PLACEHOLDER

**Every per-unit value is printed (R6):** α̂, α\*, Muth's K(v) in the instrument unit, v̂, v_own and the signed log ratio.
There is no median-only verdict. The medians in RLAW-dB are the pre-registered comparison statistic, and every unit's
error is printed beside them.

## Sensitivity table (required; 16 cells per row)

| factor | primary | alternative |
|---|---|---|
| v estimator | ML local level | moments on first differences (Declaration 1, M9) |
| own unit | δ on | δ off (Muth, the instrument's unit) |
| lag | the input as defined above | one occasion older |
| domain-specific | SPF: horizons 3–6; Michigan: to 2024-03; implied vol: daily; soil: T_DAILY_AVG | SPF: horizon 6 only; Michigan: to 2019-12; implied vol: weekly (5 aligned days; IV² at the block end, the mean of the input); soil 5 cm: T_DAILY_MEAN |

- RLAW-5 has its own factors, in the same positions:
  - α grid of 200 or 400 points;
  - Q₀ of 0 or 0.5;
  - β bound of 50 or 20;
  - exclusion of subjects with fewer than 100 valid trials, or with more than 10 % missed.
- **A verdict that flips in more than 1 of the 15 alternative cells is FRAGILE.**

## Seeds and determinism (R9)

- The two-step table uses NumPy default_rng seeds 1300 + round(100 ḡ). The bootstrap uses seed 0.
- Nothing else is random.
- Two runs of the scorer must be byte-identical (`cmp` on stdout).

## Anchoring

- **The hash:** one sha256 list over `prereg/rlaw/` and `runs/rlaw/frozen/` (HASH.txt, whose own line is excluded from
  its list).
- **The timestamp:** `ots stamp` (HASH.txt.ots), upgraded after Bitcoin confirmation.
- **The tag:** a signed tag `prereg-rlaw-2026-09-24` is attempted. If the tag push is refused, the push time of the hash
  commit is the git-side witness.

## What each outcome means (stated before the data)

- **RLAW-1, 2, 3, 5 PASS.** Those systems are Muth-optimal in level. That is the known neighbour, and it is not CRR's.
- **RLAW-4 and RLAW-4T PASS (RLAW-C).** A system that does no inference sets its memory by its environment's drift in
  its own unit. That is the CRR-only claim, and its first support. Only PASS-0 on unseen data; PASS-2 needs a replication
  on a later day.
- **RLAW-C FAILs, as physics expects.** The universal form of the law is refuted where it is CRR's own. What survives is
  Muth's law for inferring systems, if 1, 2, 3 and 5 pass. CRR then stays a grammar on this route (R12), and the ledger
  says so.
- **RLAW-dB FAILs while RLAW-d passes.** The law does no better than one constant in that domain: it reduces to the
  constant there (R7).

## Reproduction (on or after 2026-09-25 00:00 UTC)

```
sha256sum -c prereg/rlaw/HASH.txt   # every line but HASH.txt's own
uv run python runs/rlaw/frozen/fetch_rlaw.py
uv run python runs/rlaw/frozen/rlaw_score.py --json runs/rlaw/results.json > runs/rlaw/score.txt
uv run python runs/rlaw/frozen/rlaw_score.py > runs/rlaw/score_rerun.txt && cmp runs/rlaw/score.txt runs/rlaw/score_rerun.txt
```

`data/SEEN.md` gains every source in the same commit as the data step.
