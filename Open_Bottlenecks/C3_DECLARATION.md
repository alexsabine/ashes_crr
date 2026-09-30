# OB1-C3 declaration: when to consolidate in a boundary-free stream: the arc (CRR) against the chord (TIDE) (pushed before any C3 code)

**The request.** Prompt-log entry 254: "We should run a consolidation".

**Where this comes from.**
- `CRR_READING.md` C3 (h4-B1, h1-B1).
- `checks/grade_s3.txt`: PARTLY REDUNDANT. The nearest source is TIDE, claim c3:24 (AGENT_LOG 206).

**The question.**
- In a stream with no task boundaries, a learner must decide **when** to consolidate: fix an anchor and an importance
  estimate for a quadratic penalty.
- **CRR's reading:** consolidate when the learner's own **accumulated path (the arc)** since the last consolidation reaches
  a unit.
- **TIDE's family:** act on the **Fisher-weighted displacement (the chord)** from the last settled point.
- **The repository's own record** (T1X2-1: the endpoint predicts forgetting and the path does not beat it) predicts the
  chord.
- **The contest is two-sided.** CRR predicts ARC ahead of CHORD, the record predicts CHORD ahead of ARC, and a tie is
  possible.

**Rung.** Phase A is synthetic (R4). A pre-registration follows only if the gate opens **and** ARC is ahead of CHORD. Its
data step would be on a later day (R3).

## The stream and the learner (`checks/c3_lib.py`)

**The domains.** SEC1's synthetic 10-class problem (d = 20, 1500 rows, the fixed 80/20 split). There are 5 domains, each
with a fixed seeded random rotation of the input (as C1's S2). Each domain has its own disjoint fifth of the training rows,
and the whole rotated test set.

**The streams.**
- **BLURRY (primary).** 360 batches of 10. At normalised time τ = step/360, each sample's domain is drawn with weights
  w_k(τ) ∝ exp(−(τ − c_k)² / (2σ²)), where c_k = (k + 0.5)/5 and σ = 0.06. The row is then drawn from that domain's rows.
- **ABRUPT (secondary).** The same, with σ → 0: domain k occupies τ ∈ [k/5, (k+1)/5).

**The learner.**
- SEC1's MLP (256 hidden units), SGD with lr 0.05, batch 10. Seeds 0–4 are scored; seed 100 is for calibration only.
- **Penalty:** λ/2 · Σ_i Ω_i (θ_i − θ*_i)², online-EWC style.
- **At each consolidation:**
  - θ* ← θ;
  - Ω ← Ω + F, where F is the diagonal empirical Fisher over a sliding window of the last 200 inputs seen (a short-term
    window, not long-term replay).
- **The stability clip.** Ω is clipped at κ/(lr·λ) with κ = 0.5, SEC4's clip, so no arm diverges.

## The triggers (each fires online; none sees the domains except ORACLE)

| arm | fires when | role |
|---|---|---|
| NONE | never | lower bound |
| ORACLE | at τ = 1/5, 2/5, 3/5, 4/5 (the dominant-domain switches) | upper reference: 4 consolidations |
| COUNT | every 72 steps | clock |
| RAND | at 4 seeded random steps | timing control |
| **ARC** | Σ a_t since the last consolidation ≥ U_arc, where a_t = √(2·KL) of each update on its batch (C1's arc) | **CRR** |
| **CHORD** | D_t = Σ_i M_i (θ_i − θ*_i)² ≥ U_chord, where M is the last consolidation's F, or the window Fisher at step 20 before the first | **TIDE's quantity** (a unit threshold, not TIDE's significance test) |
| LOSS | the CUSUM Σ max(0, ℓ_t − ℓ̄_t) since the last consolidation ≥ U_loss, with ℓ̄ the loss's running mean at ρ = 0.01 | published loss-surprise family (SeRe; Aljundi-type) |

**Calibration** (seed 100, BLURRY stream, fixed before scoring):
- λ is chosen from {0.1, 1, 10, 100} by ORACLE's final accuracy.
- Each threshold U is set by bisection, so that the trigger fires 4 times on the calibration run.
- The same λ and thresholds are used on the scored seeds and on ABRUPT. The number of consolidations per run is printed.

## The metric

- Final average accuracy over the 5 domains' test sets.
- Also printed: average forgetting (each domain's best accuracy over the run minus its final accuracy) and the
  consolidation times.

## Phase A gate (`checks/c3_phase_a.py`; both must hold on BLURRY)

The step is max(1, 2 × SE over seeds) of the comparator.
- **G-MATTER:** ORACLE ahead of NONE by more than a step. Consolidation helps in this stream at all.
- **G-TIMING:** ORACLE ahead of RAND by more than a step. **When** to consolidate matters. Without it, no trigger
  comparison means anything.

**If the gate closes,** C3 stops (R12): ledger row OB1-C3-A.

## The result, scored only if the gate opens (the two-sided contest; printed words computed)

- **ARC − CHORD on BLURRY:**
  - CRR-WIN if above +step;
  - RECORD-WIN if below −step;
  - TIE otherwise.
- **Reported beside it:** ARC − COUNT, ARC − LOSS, ARC − ORACLE, and the same on ABRUPT.
- **If CRR-WIN:** a development declaration on SEEN tabular carriers (blurry streams built from them) is written next.
  **If RECORD-WIN or TIE:** C3 stops. The finding is recorded: the arc is not a better consolidation clock than the chord
  here.

## Forecasts (written now)

1. The gate opens: ORACLE ahead of NONE and of RAND.
2. **RECORD-WIN or TIE.** The chord (TIDE's quantity) is at least as good as the arc, as T1X2 found for forgetting.
3. LOSS is close to ARC. The loss surprise and the arc both spike at a shift.
