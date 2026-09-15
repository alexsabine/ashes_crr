# Scope review — where the CRR mathematics can be tested under the audit protocol

Written 2026-09-15 in answer to prompt 2 (`notebook/PROMPT_LOG.md`).
Status: **a planning document.** Nothing here is a result, a prediction, or a
change to `theory/CRR.md`. Where it proposes a change to the theory it says
so and leaves the canonical file untouched until the human approves. Closed
forms it relies on are proved in `theory/checks/verify_scope_math.py` and
labelled *proposed* P6–P9 until merged into CRR.md.

---

## 0. The forecasting question, settled before anything else

`theory/CRR.md` §0 and [A8] say CRR "cannot forecast content or timing" and
that "any test against the future is not a test of CRR". Prompt 2 says the
past includes a system's historical data, so forecasting is possible,
provided it is acknowledged that the future has no content and a forecast
never reaches certainty.

These are compatible, and the reconciliation is already latent in H-L5.
If arc-to-next-event is more regular than clock-to-next-event, then "the
next event arrives when the arc since the last one reaches its typical
value" is a *better predictor* than "when the clock reaches its typical
value". That is a forecast built entirely from settled occasions, scored
comparatively, with an error distribution — exactly what a growing-block
reading permits and what [A8] actually forbids is something narrower: a
claim that the *content* or *clock time* of a future occasion is fixed.

Proposed amendment, **not applied** (a theory change must precede any prereg
that uses it and be covered by that prereg's hash):

> **[A8′] No valence, no certainty.** Persistence proves regeneratability,
> not truth. CRR makes no claim about the content or clock time of a future
> occasion. It permits *conditional, comparative* forecasts computed from
> settled occasions ("the next boundary is expected when C reaches its past
> typical value"), scored against the conventional forecast (clock) on
> held-out occasions and reported with their error distribution. Such a
> forecast is a prediction about the record, never knowledge of the future.

Under A8′ every forecasting test in this document takes one form, **H-F**
("quota forecaster"), defined in §5. Nothing in this document proposes a
point forecast of content.

---

## 1. What a domain must supply

CRR's mathematics is small: a unit (A1′), an arc on a statistical manifold
(D2), a cut at the phase antipode (A3) or at the system's own event (D5/[M]),
and a comparison (§4, §5). A domain can be tested only if it supplies all of:

| # | requirement | why | where it fails |
|---|---|---|---|
| 1 | **A carrier with intrinsic phase, or a point process with its own events** | otherwise the cut is undefined ([O3]) | trends, one-shot processes, "narratives" |
| 2 | **Events the system itself produces**, distinct from waveform extrema | H-CUT and H-L5 are scored on them; extrema are the instrument's, not the system's | smooth cycles with no discrete event (pure oscillators) |
| 3 | **A statistical family for the state**, so g is the Fisher metric of *something* | otherwise "Fisher" is a label on the identity metric (§2) | raw voltage / price traces with no model |
| 4 | **One occasion statistic** to set σ before data | A1′ | records where no single statistic is defensible |
| 5 | **A conventional quantity to beat** (clock, endpoint, published method) | R7; CRR is comparative | domains with no established baseline |
| 6 | **Enough units** for per-unit scoring (≥ 10 levels / subjects / seeds) | R6 forbids medians over a handful | n < 10 series (business cycles, solar polarity reversals) |
| 7 | **Public, versioned, unseen data** with record ids | R2, R11 | proprietary streams, already-SEEN sets |
| 8 | **A surrogate that must fail** | R4 | any claim a generic smooth signal also satisfies |

A domain missing 1 or 2 is out of scope. Missing 3 is admissible only with
the disclosure in §2.

---

## 2. The metric question: where "Fisher" is real and where it is decorative

This is the single most important scoping fact and the old work never
stated it.

**On a 1-D trace, the Fisher–Rao arc is a total variation after a fixed
reparametrisation** (proposed **P9**, verified): with metric g(x) > 0,
arc = ∫√g |dx| = TV(y), y = ∫√g. With the identity metric it is plain TV.
So for ECG, PPG, shear stress, an index — anything scalar with no
statistical model of what the value *is* — control (ii) of H-L5 ("arc with
identity metric") is not a control, it is the same number. The instrument's
`arc_length(metric=None)` on a 1-D trace is TV(x)/σ and must be called that.

"Fisher" carries content only where the state is a distribution or its
parameter. Closed forms for the families each domain needs
(`verify_scope_math.py`):

| family | state | FR distance | note |
|---|---|---|---|
| categorical (K classes) | p on the simplex | 2·arccos Σ√(p_i q_i) (**P7**) | learners' predictive distributions; epidemic compartments |
| Poisson rate | λ | 2·\|√λ₂ − √λ₁\| (**P6**) | spike trains, event catalogues, case counts; arc = TV(2√λ) — **not** proportional to TV(λ) |
| fixed-variance Gaussian | μ | \|Δμ\|/σ, and √(2KL) is *exact* (**P8**) | regression learners; S-H |
| general | θ | √(2KL) to second order (D6) | D6 as written |

Consequence for each hypothesis:

- **H-T1, H-EQ** (learners): Fisher is native. The metric claim is real.
- **H-L5 on point processes** (spikes, slips, cases): Fisher is native if
  the carrier is the *rate* — arc = TV(2√λ̂(t)) between events, which is
  a different quantity from TV(λ̂) (P9 check). Control (ii) then means
  something.
- **H-L5 / H-CUT on a scalar physiological or mechanical trace**: the arc
  is TV/σ. Admissible — "change has its own clock" is still a falsifiable
  comparative claim — but the report must say **"arc = total variation of
  the trace in units of σ; the Fisher metric plays no role in this study"**.
  Anything else is the decoration the audit caught.

---

## 3. Domain review

Scored against §1. "Fisher" column: **native** / **rate** (Poisson on an
event rate) / **TV** (decorative, must be disclosed). n = units for
per-unit scoring. Data sources are named from memory and **must be fetched
and versioned on the day (R10) before any of them enters a prereg**; none
has been fetched for this document.

| domain | carrier / own events | Fisher | unit statistic (one) | baseline to beat (R7) | must-fail surrogate | n | data (unverified) | verdict |
|---|---|---|---|---|---|---|---|---|
| **Continual learning: fine-tuning** | predictive distribution on a probe; "cut" = task switch (imposed) | native | per-step √(2KL) residual | E_old, E_new, EWC Fisher-weighted ‖θ_T−θ_0‖, lr | S-H (convex) | 60+ runs/model | own runs; Pythia/OLMo checkpoints; RL's Razor logs | **Tier 1** |
| **Continual learning: replay weighting (EQ)** | same | native | — | ER-sum, fixed w, MEGA-I, ER-ACE, DER++ | convex replay learner (gate_EQ, to write) | 5 seeds × 4 datasets | Split-CIFAR-100, TinyImageNet, LM stream | **Tier 1**, reduction test first |
| **Lab friction (stick-slip)** | shear stress cycle; slips | TV | per-occasion stress drop residual | clock CV, amplitude CV, peak-cut arc | S-A, S-A″, S-G | levels × experiments | PSU Marone-lab repository, experiments ≠ p4581 | **Tier 1** (planned L5x) |
| **Cardiovascular pressure / ECG** | pulse cycle; upstroke onset / R-peak | TV | per-beat amplitude residual | clock CV (RR interval), amplitude, peak-cut | S-B, S-C, S-D noise | 60 subjects | PhysioNet Autonomic Aging 0061–0120; MIT-BIH (unseen) | **Tier 1** (planned L5x); H-CUT on ECG asymmetry |
| **Epidemic waves (measles, pre-vaccine)** | (S, I, R) fractions on the simplex; own events = outbreak onset / fade-out | **native** (P7) | per-wave peak incidence residual | clock CV of inter-epidemic interval; TSIR model | S-A‴ AM+FM | 40+ cities | Project Tycho / UK weekly notifications (E&W 1944–66) | **Tier 2**, best non-learner Fisher-native case |
| **Spike trains + LFP** | LFP phase; own events = spikes / bursts | rate (P6) | ISI residual | ISI CV; standard phase-locking (Hilbert) | S-D noise | 100s of units | Allen Neuropixels, DANDI (versioned) | **Tier 2**; H-CUT competes with phase-precession literature |
| **Abrupt climate events (D–O)** | δ¹⁸O sawtooth; own events = abrupt warmings | TV | per-event warming amplitude residual | clock CV (GICC05 age), amplitude | S-G (clock-regular relaxation) | ~25 events, 1–3 cores | NGRIP/GRIP on GICC05 | **Tier 2**, single-unit only; bootstrap not per-unit |
| **ENSO / solar cycle** | Niño3.4 or sunspot number; own events = El Niño onsets / polar reversals | TV | per-cycle amplitude residual | clock CV | S-A‴ | 20–25 events, 1–2 units | NOAA ERSST; SILSO; WSO polar field | **Tier 3**: n fails §1.6 for per-unit scoring; exploratory only |
| **Slow-slip / tremor catalogues** | natural time = events | rate | inter-event count residual | clock CV; ETAS | Poisson surrogate | 10+ segments | PNSN tremor, Cascadia SSE catalogues | **Tier 2** (named as optional in CLAUDE.md §4) |
| **Market microstructure** | trades = natural time | rate | per-bar volume residual | **volume clock / volume bars** (Easley, López de Prado — a published "own clock" already) | Poisson surrogate | many symbols | tick data (mostly proprietary) | **Tier 3**: strong existing baseline, high false-positive culture, SPY is SEEN |
| **Sleep architecture** | NREM/REM cycle; own events = REM onsets | TV | per-cycle duration residual | clock CV | S-A′ | 150+ nights | PhysioNet Sleep-EDF (unseen) | **Tier 2**, cheap |
| **Aftershock / retention fits** | events | rate | — | Omori p | — | — | — | **Out**: [P5] says a fitted p tells you nothing about CRR |
| **Business cycles, solar polarity (n < 10)** | — | — | — | — | — | < 10 | — | **Out** by §1.6 |
| **Language / discourse boundaries** | next-token distribution path; own events = discourse boundaries? | native | — | — | — | — | — | **[O]**: no intrinsic phase; needs a cut criterion first ([O3]) |

**Why measles is the standout non-learner case.** Its state (fractions in
compartments) is a point on the simplex, so P7 gives a genuine Fisher
arc; its own events (onsets, fade-outs in small towns) are not waveform
extrema; there is a strong published baseline (TSIR); the data are public,
versioned and unseen; and n is large (cities). It is the one domain outside
machine learning where every §1 requirement is met with a *native* metric.

---

## 4. Continual-learning programme (the focus)

### 4.1 What the surrogate already taught us (today)

Building S-H produced a lemma (verified in `verify_scope_math.py`): for a
linear model at its task-A optimum, **forgetting is exactly 2σ²·E_old** —
the endpoint KL on the *old* probe is a sufficient statistic. Path length
can only lose to it. The gate table shows it:

```
S-H  convex learner   R2(C)=0.09  R2(E_new)=0.98  R2(E_old)=0.997   -> FAIL (correct)
S-H2 wear learner     R2(C)=0.45  R2(E_new)=0.17  R2(E_old)=0.22    -> PASS (instrument sees path-dependence)
```
(emitting output committed at runs/phaseA/gate_T1.txt)

Two consequences for Study T1x as written in CLAUDE.md §5:

1. **T1x-1 must compare against E_old as well as E_new.** As written it
   compares C against E_new only, so a "win" could mean "old probe beats
   new probe", not "path beats endpoint". `gate_T1` scores the best path
   predictor against the best endpoint predictor. (CLAUDE.md §5 amended
   accordingly in this commit — a strengthening of the baseline, allowed
   before any prereg.)
2. **The Fisher-weighted endpoint distance of EWC**
   (‖θ_T − θ_0‖ in the old-task Fisher norm, Kirkpatrick et al. 2017 —
   fetch and version per R10) is the published method closest to E_old and
   is a required R7 baseline for T1x on neural nets.

### 4.2 T1x hypotheses (unchanged in substance, baseline strengthened)

- **T1x-1** held-out R²(best of C_new, C_old) ≥ R²(best of E_new, E_old,
  EWC-distance) + 0.05, lr controlled. FAIL if any endpoint predictor wins
  by ≥ 0.05.
- **T1x-2** fixed-lr arm: Spearman(C, F) ≥ 0.6 and Spearman(best E, F) <
  Spearman(C, F) − 0.2.
- **T1x-3** on S-H: R²(C) − R²(E) ≤ 0.02 (gate, in-prereg). Currently −0.90.
- **T1x-4 (new, forecasting form, needs A8′)**: from the path accumulated
  in the **first half** of fine-tuning, predict *final* forgetting; compare
  with the endpoint displacement at the same half-way point. Scored on
  held-out runs. This is the CL instance of H-F (§5): a prediction from
  settled occasions about the record's future, never certain.

### 4.3 EQ: what gate_EQ must be before the study can be pre-registered

- A convex learner with replay (S-H plus a task-A replay buffer) on which
  the Ω = 1 rule and every fixed w converge to the same joint optimum:
  "no forgetting to trade off". H-EQ must **FAIL** there (tie with fixed w).
- A positive control where balancing the two gradients' Fisher norms
  provably beats summing the losses: a two-task problem with grossly
  mismatched gradient scales (task B loss scaled ×100), where ER-sum is
  dominated by B and any norm-balanced rule recovers A. H-EQ must **PASS**.
- Both controls implemented against the ER-sum baseline *summed, not
  averaged* (the defect CLAUDE.md §6 identified).
Not written today; EQ cannot enter a prereg until it exists (R4).

### 4.4 Data for T1x on real models (all to be fetched and versioned on the day)

- Own byte-level LM and GPT-2-small class runs (CLAUDE.md §5) — the only
  arm where lr and schedule are fully controlled.
- Public checkpoint series with per-step logs (Pythia, OLMo): natural time
  = tokens; single-stream pretraining, so *not* a task-switch — usable for
  D6 path/endpoint reporting only, not for T1x-1.
- RL's Razor (Shenfeld et al. 2025): its claim is an **endpoint-KL** claim
  (RL stays closer to the base distribution); T1 says path beats endpoint.
  This is the sharpest external comparison available. Usable only if
  per-step checkpoints or KL logs are public; otherwise the ledger row says
  "not scoreable: no per-step data".

---

## 5. H-F — the one admissible forecasting form ("quota forecaster")

For any domain with own events and a CRR quantity Q accumulated between
them (arc, or path length in learners):

- From the settled occasions 1..m, the **quota forecast** of event m+1 is
  the first sample at which Q since event m reaches the median of
  Q_1..Q_m. The **clock forecast** is t_m + median(Δt_1..Δt_m).
- Score: absolute error in samples, per unit, on occasions never used to
  set the quota (rolling origin, no look-ahead). Paired sign test across
  units; bootstrap CI on the median error ratio.
- **PASS** if the quota forecast has lower median error in ≥ 80 % of units
  and the CI excludes 1. **FAIL** if < 60 %.
- Must FAIL on: S-A″ (AM sine, clock-regular), S-G. Must PASS on: S-A′,
  S-G2. `gate_F` to be added to `surrogates/gate.py` before use.
- Report the full error distribution, and the fraction of forecasts whose
  error exceeds one full occasion (a forecast that is worse than "no
  forecast").

H-F is H-L5 re-expressed as an out-of-sample prediction and is stronger:
CV comparison can be won by a quantity that is regular but unpredictable
in advance (e.g. via look-ahead in σ); the quota forecast cannot.
It does not enter any prereg until A8′ is adopted into CRR.md.

---

## 6. Prioritised programme

| order | study | prerequisites before its prereg hash | status |
|---|---|---|---|
| 1 | **T1x** (own LM + GPT-2 class) | gate_T1 (done); EWC baseline coded; `lm_bench.py` frozen; A8′ only if T1x-4 is included | ready to draft prereg |
| 2 | **L5x** (stick-slip ≠ p4581; Autonomic Aging 0061–0120) | gate L5 + CUT (done); TV disclosure (§2) in the prereg; fetch scripts + manifests | ready to draft prereg |
| 3 | **EQ** | gate_EQ (§4.3); Mammoth commit pinned; S-H replay variant | blocked on gate_EQ |
| 4 | **MEAS** (measles, Fisher-native) | simplex arc in `instrument/core.py` (P7); TSIR baseline; gate on S-A‴; Tycho fetch + version | needs instrument extension |
| 5 | **SPK** (Neuropixels) | rate-metric arc (P6) in instrument; phase-locking baseline; DANDI fetch | needs instrument extension |
| 6 | **SLP** (Sleep-EDF) | none beyond L5 gate | cheap, low novelty |
| — | ENSO / solar / D–O | single-unit; report only, never a ledger PASS | exploratory |
| — | markets, aftershock p | out | — |

Instrument extensions implied: `arc_length(metric="simplex")` (P7, exact
geodesic on the sphere map p ↦ √p) and `metric="poisson"` (P6). Both are
closed forms, no fitting.

---

## 7. What this review changes in existing plans (log for the audit)

1. **E_old is a required baseline for T1** (§4.1). CLAUDE.md §5 T1x-1
   amended in this commit; theory §5 [H-T1] wording ("than by E on the new
   task") should be tightened to "than by E on either probe" in v3.1 —
   proposed, not applied.
2. **1-D arc = TV disclosure** (§2) is mandatory in every L5/CUT report;
   control (ii) of H-L5 is void in 1-D and must be replaced by the P6/P7
   metric where a family exists, or dropped with the disclosure.
3. **A8′** (§0) is proposed to permit comparative forecasts (H-F). Not
   applied.
4. **The CUT gate's S-D row** (noise-only "PASS" at 0.136 half-turns) is
   the reason H-CUT is scored on own events; a study report must show the
   noise-only disagreement for its ρ as a reference line.
5. **gate_EQ does not exist**; EQ is blocked (R4).
