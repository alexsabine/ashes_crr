# Report — study MEAS2: "change has its own clock" on measles epidemics

Written 2026-09-15 after ledger rows MEAS2-1 … MEAS2-3 (`ledger/LEDGER.md`).
Every number below is in `runs/meas2/score.txt`, printed by
`runs/meas2/frozen/meas2_score.py score` from `runs/meas2/results.jsonl`.
Study MEAS (same hypotheses) preceded it and was voided by its own format
rule before any case value was read; see ledger row MEAS-1..3 and
`prereg/meas2/PREREG.md` for the data-status statement.

## Verdict, as pre-registered

| line | claim | result |
|---|---|---|
| MEAS2-1 | H-L5, Poisson-rate metric (Fisher-native): per city, arc between epidemic onsets more regular than clock (CI < 0) **and** beyond amplitude (CI < 0); PASS if ≥ 80 % of cities | **FAIL — 0/17 cities.** The bare inequality cv_arc < cv_clock held in 5/17; no city's CI excluded 0 in the arc's favour on both criteria. |
| MEAS2-2 | same, identity metric (control ii) | **FAIL — 0/17.** Bare inequality in 1/17. |
| MEAS2-3 | control (iii): arc between onsets more regular than arc between `find_peaks` boundaries in ≥ 70 % | 12/17 = 0.706 → passes the line, which compares two boundary rules and says nothing about H-L5 (both fail). |
| sensitivity | 26 detector cells (rise_factor × floor_frac × min_gap), both metrics | verdict differs in **0/26** cells for each metric → not fragile. The best any cell reaches is 1/17. |

Exclusions (pre-registered, < 8 onsets): Halesworth (2), Lees (5), Mold (5)
— the three smallest towns, where measles faded out for long stretches. ρ was
computable in 12 of 17 scored cities (1.5–5.7 occasion extents per σ under the
Poisson metric; 1.2–3.6 under identity) and "n/a" in five with too few
occasions for the named detrender; ρ enters no threshold.

## What the data say
In most cities the **clock** is the regular quantity: cv_clock 0.20–0.48,
cv_arc 0.26–0.52 (Poisson). In Birmingham, Leeds, Dalton-in-Furness the CI on
(cv_arc − cv_clock) lies entirely *above* 0 — the arc is significantly *less*
regular than the clock. This is the signature of the S-A″/S-G class in the
gate table: a fixed period with variable excursion size. Measles in
pre-vaccination England is the textbook biennial oscillator; its epidemics
differ in size far more than in timing, and the arc — which integrates the
size — inherits that variability.

The Fisher metric changed the numbers (in 16 of 17 cities the Poisson-metric
cv_arc is below the identity-metric cv_arc, as the concavity of √ predicts;
Northwich is the exception) without changing a single verdict. Control (ii) was therefore not discriminating here, and
the concavity trap the gate identified did not produce a spurious pass —
the amplitude control did its job in every cell.

## Per-city distribution
All 17 scored cities are listed with cv_arc, cv_clock, cv_amp, both CIs,
the peak-cut control and ρ in `runs/meas2/score.txt` (primary cell); all 26
sensitivity cells give k/n, the plain-inequality count and the control (iii)
count. No city passed in any cell except one city in three of the
rise_factor = 3.0 cells (1/17).

## Anchoring caveat (R2)
Hash 6346305b… was pushed (`57b6302`, 21:24:30Z) before the run but the
OpenTimestamps anchor could not be created and the tag could not be pushed.
The data file had been downloaded under MEAS at 21:23:22Z; no value was read
before the MEAS2 hash. An auditor who rejects that distinction should read
these rows as confirmatory (seen). Since every line is a FAIL, the weakness
cuts against nothing the theory would want to claim.

## What a surrogate would have done
`prereg/meas2/gate_L5R.txt`: the S-P AM row (constant period, variable peak)
FAILs under both metrics with cv_arc 0.082 vs cv_clock 0.000 (Poisson). The
measles cities behave like that row with a jittered clock: variable peaks,
comparatively steady timing. The positive control (two-hump compensating,
arc constant while amplitude varies) shows the instrument would have seen an
arc-regular system had there been one. There was not.

## Open, not tested here
- The forecasting form (H-F, SCOPE.md §5) against the TSIR model, which is
  the published baseline for measles *timing*; it needs the A8′ decision.
- H-L5 on carriers with genuinely arc-regular events (stick-slip, cardiac —
  the planned L5x), which this result does not touch.
