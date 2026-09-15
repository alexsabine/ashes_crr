# Pre-registration — MEAS: "change has its own clock" on measles epidemics

Written: 2026-09-15T21:21Z (container clock). Hash of this folder and
`runs/meas/frozen/` in `HASH.txt`. Signed tag `prereg-meas-2026-09-15`.
**No data listed below has been opened. No file under `data/raw/measles/`
exists at hash time.**

## Anchoring
As for study EQX (`prereg/eqx/PREREG.md` §Anchoring): OpenTimestamps calendars
are unreachable from this environment and the remote refuses tag refs, so the
only external witness of "before" is the GitHub push timestamp of the commit
that carries `HASH.txt`. Rows from this study are labelled
`anchor: push-timestamp only`. A PASS here would be *held-out, weakly
anchored*, not an R2 held-out PASS; the human can strengthen it only by
re-running the study after stamping a fresh prereg.

## Hypothesis under test (theory/CRR.md [H-L5]; CLAUDE.md §4 template)
For a system with its own boundary events, the coherence C accumulated between
consecutive events is more regular than the clock time between them,
CV(C_m) < CV(Δt_m), **beyond** three controls: (i) amplitude of the excursion
alone, (ii) arc under the identity metric, (iii) arc between peak-detected
boundaries.

**Carrier and metric.** Reported measles cases per biweek are a Poisson-rate
carrier. Under the Poisson family the Fisher–Rao arc of the rate is exactly
the total variation of y = 2√λ (SCOPE.md P6 and P9, `verify_scope_math.py`;
`instrument.core.poisson_transform`). This is the first study in this repository
where "Fisher" is not decorative: the identity-metric arc (total variation of
the counts) is a genuinely different number, so control (ii) has content.

**Own events.** Epidemic onsets, `instrument.core.onset_events`: since the
last onset, M = max cases and m = min cases *after* that maximum; an onset fires
at the first biweek with cases ≥ rise_factor·m, m ≤ floor_frac·M, cases ≥
min_cases, and ≥ min_gap biweeks since the last onset. No smoothing, no peak
finder. Verified on the S-P surrogates to fire once per synthetic epidemic
(`instrument/tests/test_core.py::test_onset_detector_fires_once_per_epidemic`).

## Gate (R4) — `gate_L5R.txt`, committed here, covered by the hash
Rate-domain battery S-P (Poisson counts on synthetic epidemic curves; events
= true cycle starts). Under BOTH metrics: S-P AM (constant period, variable
peak) FAIL; S-P AM+FM (no CRR content) FAIL; S-P clock-regular two-hump FAIL;
S-P FM two-hump compensating (arc constant, amplitude variable by construction)
PASS. **GATE OPEN.** Two facts the gate established, which fix the scoring
rule below:

1. *The concavity trap.* Under the Poisson metric S-P AM+FM satisfies the bare
   inequality CV(arc) < CV(clock) with the bootstrap CI excluding 0
   (cv_arc 0.097 vs cv_clock 0.136): √ halves the CV of a variable peak. Only
   control (i), scored in the same metric by its paired-bootstrap CI, blocks
   it. Control (i) is therefore *decisive*, not decorative, and is scored by
   CI, never by a point comparison.
2. *Arc absorbs sampling noise.* On S-P FM (one hump, constant peak) the arc's
   CV (0.076) exceeds the amplitude's (0.032) because Poisson noise accumulates
   in the total variation; that row FAILs the "beyond amplitude" requirement
   although arc beats clock. A real-data PASS must overcome this.

## Data (absent from data/SEEN.md — confirmed)
`twentymeas` from the R package tsiR 0.4.2 (Becker, Morris, Bjørnstad;
source: Bryan Grenfell), GitHub `adbecker/tsiR`, `master`,
`data/twentymeas.RData`: "a list containing 20 dataframes with cases, births,
populations. Each dataframe is a 22 year time series at biweekly intervals"
(`man/twentymeas.Rd`, read before hashing; the data file was not). Fetched
after the tag by `data/fetch_measles.py`; sha256 in `data/manifests/meas.sha256`
and in the results header; appended to `data/SEEN.md` in the same commit.
Reader: `rdata` (pure Python) with `pyreadr` fallback; both pinned in
`uv.lock`. **Format void rule:** if neither reader yields 20 series each with a
`cases` column, the study is void for format reasons and the row says so; the
frozen script is not edited.

Units: the 20 cities. Quality gate (pre-registered): a city with any NaN in
`cases` is excluded; a city with fewer than **8 onsets** under a cell's detector
is excluded *in that cell*; every exclusion is counted and listed.

## Instrument parameters (all named; frozen in `runs/meas/frozen/meas_score.py`)
- Metrics: `poisson` (primary, MEAS-1) and `identity` (MEAS-2).
- Onset detector, primary cell: rise_factor 2.0, floor_frac 0.25,
  min_cases 20, min_gap 20 biweeks.
- Sensitivity table (required): rise_factor ∈ {1.5, 2.0, 3.0} × floor_frac ∈
  {0.15, 0.25, 0.5} × min_gap ∈ {12, 20, 30} = 26 non-primary cells, both
  metrics. A verdict that differs from the primary cell's in > 1 cell is
  reported as **fragile**.
- Regularity: `instrument.core.regularity`, paired bootstrap n = 2000,
  seed 0; cv = std(ddof=1)/mean.
- Amplitude (control i): peak-to-trough of y within each occasion, same metric.
- Control (iii): `peak_cuts` on the raw counts, prominence 0.3 × range,
  distance 20; arc of y between consecutive peak-detected boundaries.
- Unit and ρ (report only, never in a threshold): σ = `unit_sigma` of the
  per-occasion peak of y (savgol 9/2, MAD); ρ = mean occasion extent / σ;
  "n/a" where a city has too few occasions for the detrender.

## Baselines (R7)
Clock CV (the conventional quantity); amplitude CV (i); identity-metric arc
(ii, scored as MEAS-2 in full); peak-cut arc (iii). The published method
closest to this question is the TSIR model (Finkenstadt & Grenfell 2000; the
tsiR package itself), which predicts epidemic *timing* from susceptible
build-up. TSIR is a forecasting baseline, not a regularity baseline, and
belongs to the H-F form that theory v3 does not yet admit (SCOPE.md §0); it is
therefore **not** in this study and is named here as the baseline any future
forecasting study on this data must beat.

## Hypotheses (scored once by `meas_score.py score`)
Per city, in a given cell and metric, the city **passes** iff all three hold:
cv_arc < cv_clock; the paired 95 % CI of (cv_arc − cv_clock) lies below 0;
the paired 95 % CI of (cv_arc − cv_amp) lies below 0. Cross-city: k passing
of n scored, exact two-sided binomial p at 0.5.

- **MEAS-1 (primary; Poisson metric).** PASS if k/n ≥ 0.80 and p < 0.05.
  FAIL if k/n < 0.60. Otherwise INDETERMINATE, written as such.
- **MEAS-2 (identity metric).** Same rule. Reported in full alongside MEAS-1
  (control ii is "MEAS-1 passes and MEAS-2 does not" or vice versa; both are
  written as they fall).
- **MEAS-3 (control iii; A3 proxy).** Arc between onsets more regular than arc
  between peak-detected boundaries in ≥ 70 % of scored cities (Poisson metric,
  primary cell). Note: onsets are threshold events on the counts, not antipodal
  cuts; this line tests "own events vs extrema", not A3 itself.
- **Sensitivity.** For MEAS-1 and MEAS-2 the primary verdict is fragile if it
  differs in > 1 of the 26 cells.

Outcomes named in advance: MEAS-1 FAIL → H-L5 fails on its first Fisher-native
carrier; the ledger row says so; no re-parametrisation. MEAS-1 PASS with MEAS-2
FAIL → the Fisher metric is doing the work (the interesting case) — still
held-out-weakly-anchored only. Both PASS → the result is metric-independent and
control (ii) is not discriminating on this carrier. INDETERMINATE → written as
indeterminate; a follow-up needs a fresh prereg and different cities.

## Scoring script
`runs/meas/frozen/meas_score.py` (copy of `studies/meas/meas_score.py` at hash
time) with frozen copies of `instrument/core.py`, `surrogates/battery.py`,
`surrogates/gate.py`, `theory/CRR.md`; sha256 of each in `HASH.txt`. Two runs
must be byte-identical (`cmp`); single-threaded BLAS forced in the script.
