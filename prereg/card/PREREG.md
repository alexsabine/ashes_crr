# Pre-registration — CARD: "change has its own clock" on a cardiac carrier

Written: 2026-09-15T21:46Z (container clock). Hash of this folder and
`runs/card/frozen/` in `HASH.txt`. Signed tag `prereg-card-2026-09-15`.
**No data listed below has been opened. No file under `data/raw/autonomic_aging/`
exists at hash time, and none can be fetched from this environment.**

## Anchoring and the data path
As for EQX and MEAS2: OTS calendars and tag refs are blocked; the push
timestamp of the commit carrying `HASH.txt` is the only external witness.
Rows will be labelled `anchor: push-timestamp only`.

PhysioNet is unreachable from this environment (403 at the proxy). The
records must therefore be **supplied by the human after this hash**, as an
upload of the WFDB files. This is stated here so the audit can see the
order: hash → push → human supplies files → manifest → run. The human is
asked to supply the files without inspecting them; if they were inspected,
the ledger row must say `seen: Y`.

## Hypothesis under test (theory/CRR.md [H-L5]; CLAUDE.md §4 L5x)
For a system with its own boundary events, the coherence accumulated between
consecutive events is more regular than the clock time between them, beyond
the amplitude, identity-metric and peak-cut controls.

**Carrier.** Continuous non-invasive blood pressure (BP, mmHg) and ECG
(mV) at the record's sampling rate; the first 600 s of each record (fixed).
**Metric: identity.** Neither trace has a statistical family, so the arc is
the total variation of the trace in units of σ (SCOPE.md P9 disclosure:
*the Fisher metric plays no role in this study*). Control (ii) is therefore
void here and is not scored.
**Own events.** R-peaks from a Pan–Tompkins-style detector with published
constants (band-pass 5–15 Hz, derivative, squaring, 150 ms integration,
adaptive threshold, 200 ms refractory). No constant was learned on any data
in this repository; the detector was checked only on synthetic ECG
(`card_score.py smoke`).
**Unit (A1′).** σ = `unit_sigma` of the per-beat peak-to-trough statistic of
the trace, computed on the first half of the beats (savgol 9/2, MAD, no
floor); ρ = mean per-beat extent / σ, reported. **Quality gate:** records
with NaN, a flat channel, fewer than 200 detected beats, or ρ < 3 are
excluded and counted (ρ is a pre-registered quality floor here, not a
criterion input).

## Gates (R4) — committed here, covered by the hash
- `gate_L5.txt` (identity-metric L5 gate): GATE OPEN.
- `gate_CUT.txt`: GATE OPEN.
- `gate_A3.txt`: the L5x-3 comparison (arc between antipodal cuts vs arc
  between peak cuts) reads GATE OPEN on its registered negative controls but
  **PASSes on S-C (λ = 1) and S-E** — jittered asymmetric waveforms with no
  CRR content — because `find_peaks` segments them inconsistently while the
  phase antipode does not. Under R4 that comparison is therefore *not about
  CRR* and **does not enter this prereg as a hypothesis**. It is computed and
  reported per record as a diagnostic (CARD-3) and never scored. The A3 test
  proper (H-CUT: own events align with the antipode rather than the extremum)
  is left for a study with a gate of its own.

## Data (absent from data/SEEN.md — confirmed: only 0001–0060 are listed)
PhysioNet *Autonomic Aging: a dataset to quantify changes of cardiovascular
autonomic function during healthy aging* v1.0.0, records **0061–0090**
(30 records; 0061–0120 are named in CLAUDE.md §4, the first 30 are taken
to keep the upload tractable). Expected channels: an ECG lead and a
continuous NIBP channel, WFDB `.hea/.dat`. The script picks the first
channel whose name contains "ecg" and the first containing "nibp"/"bp"/
"pressure"/"abp"; a record lacking either is excluded and counted. A record
missing from the upload is an exclusion, counted. sha256 of every supplied
file goes in `data/manifests/card.sha256` and in the results header; the
records are appended to `data/SEEN.md` in the same commit as the run.
**Format void rule:** if fewer than 10 records load and yield ≥ 200 beats
under the primary cell, the study is void for format reasons and the row
says so; the frozen script is not edited.

## Instrument parameters (all named; frozen in `runs/card/frozen/card_score.py`)
Primary detector cell: low 5 Hz, high 15 Hz, integration 150 ms, refractory
200 ms. Sensitivity table: low ∈ {4, 5, 8} × high ∈ {12, 15, 20} ×
refractory ∈ {200, 250, 300} ms = 26 non-primary cells. Regularity: paired
bootstrap n = 2000, seed 0; CVs with ddof = 1. Amplitude (control i):
per-beat peak-to-trough of the same trace. Peak cuts (diagnostic):
prominence 0.3 × range, distance 300 ms. Intrinsic phase: analytic signal,
mean-detrended (primary) and raw (sensitivity, diagnostic only).

## Baselines (R7)
Clock CV (the RR interval — the conventional quantity, and the object of the
entire HRV literature); amplitude CV (pulse pressure; QRS amplitude). The
published quantities this study is nearest to are the HRV time-domain
indices (SDNN/RMSSD) on the clock side and pulse-pressure variability on
the amplitude side; both are computed here implicitly as the CVs.

## Hypotheses (scored once by `card_score.py score`; per record; primary cell)
A record **passes** iff cv_arc < cv_clock, the paired 95 % CI of
(cv_arc − cv_clock) lies below 0, and the paired 95 % CI of
(cv_arc − cv_amp) lies below 0. k passing of n scored; exact two-sided
binomial p at 0.5.
- **CARD-1 (primary): BP arc per beat vs RR.** PASS if k/n ≥ 0.80 and
  p < 0.05; FAIL if k/n < 0.60; otherwise INDETERMINATE.
- **CARD-2: ECG arc per beat vs RR.** Same rule. (Expected to tie its QRS
  amplitude and fail control (i); scored anyway.)
- **CARD-3: diagnostic only**, see Gates.
- **Sensitivity.** A CARD-1/2 verdict that differs from the primary cell's
  in > 1 of 26 cells is fragile.

Outcomes named in advance: CARD-1 FAIL → H-L5 fails on its second real
carrier and on the physiological system it was written for; the ledger says
so. CARD-1 PASS → the first held-out-weakly-anchored positive row in the
ledger; it would need OTS-anchored replication on 0091–0120 before it is
called a result. INDETERMINATE → written as such.

## Scoring script
`runs/card/frozen/card_score.py` (copy of `studies/card/card_score.py` at
hash time) with frozen `core.py`, `battery.py`, `gate.py`, `CRR.md`; sha256
in `HASH.txt`. Two runs must be byte-identical (`cmp`); single-threaded
BLAS forced in the script. `wfdb` 4.3.1 pinned in `uv.lock` for reading.
