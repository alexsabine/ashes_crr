# The surrogate battery and the gate — `src/crr/surrogates/`

> Explanatory reference. Sources of truth:
> [`src/crr/surrogates/battery.py`](../../src/crr/surrogates/battery.py),
> [`src/crr/surrogates/gate.py`](../../src/crr/surrogates/gate.py), and
> CLAUDE.md §3.2–§3.3. On any conflict, source and CLAUDE.md win.

Rule R4 in executable form: **every hypothesis must fail on a surrogate
before it may enter a pre-registration.** The battery is a catalogue of
deterministic synthetic signals (generators are deterministic given
`seed`) with **no CRR content**, each returning `(x, events, meta)` —
`events` being the sample indices of the signal's own boundary events,
or `None`. The learner surrogates instead return `(runs, None, meta)`
where each run carries per-step probe predictions and the forgetting `F`
it produced.

## How to run

```bash
uv run python -m crr.surrogates.gate L5
uv run python -m crr.surrogates.gate CUT
uv run python -m crr.surrogates.gate T1
```

Committed outputs live in [`runs/phaseA/`](../../runs/phaseA/) —
`gate_L5.txt`, `gate_CUT.txt`, `gate_T1.txt` — and are the emitting
evidence for every gate statistic quoted anywhere (R1; audit finding #9's
remedy). If you change the instrument, re-run the gate and commit the new
output.

## Battery catalogue

Control roles are exactly the `MUST_FAIL` / `MUST_PASS` maps registered
in `gate.py`; rows not listed there are informational.

| id | generator | parameters | role |
|---|---|---|---|
| S-A | `S_A_sine` | `n=60`, `period=100` | L5 MUST_FAIL, CUT MUST_FAIL — a pure sine: nothing varies |
| S-A′ | `S_A1_fm_sine` | `jitter=0.2` | L5 MUST_PASS — FM sine, constant amplitude: arc-regular by construction |
| S-A″ | `S_A2_am_sine` | `jitter=0.3` | L5 MUST_FAIL — AM sine, constant period: clock is the regular one |
| S-A‴ | `S_A3_amfm_sine` | `jitter` (period 80–120, amp 0.7–1.3) | informational |
| S-B | `S_B_sine_bump` | `bump=0.15` | informational — the "dicrotic" surrogate |
| S-C | `S_C_lobed_ramp` | `lam` ∈ {0.0, 0.25, 0.5, 1.0} | informational — the "ECG" surrogate; λ sweep (audit #5) |
| S-D | `S_D_noisy_sine` | `rho` ∈ {5.0, 10.0, 20.0, 40.0, 80.0} | CUT **reference line** — noise alone displaces extrema from antipodes; studies report the noise-only disagreement for their ρ (SCOPE.md §7.4). ρ sweep (audit #5) |
| S-E | `S_E_asymmetric` | — | CUT MUST_PASS — asymmetric multi-harmonic |
| S-F | `S_F_vanderpol` | `mu=5.0`, `T=400`, `dt=0.05`; registered μ=1.0 variant row | CUT MUST_FAIL (μ=5) — symmetric limit cycle; the μ=1 row is informational |
| S-F | `S_F_roessler` | `T=1200`, `dt=0.05` (a=0.2, b=0.2, c=5.7) | informational — implemented by the restructure PR (audit #5) |
| S-F | `S_F_duffing` | `T=1000`, `dt=0.05` (δ=0.15, γ=0.3, ω=1) | informational — forced double-well; implemented by the restructure PR (audit #5) |
| S-G | `S_G_relaxation` | `thresh_cv=0.15` | L5 MUST_FAIL — clock-regular by construction (fixed firing time, varying threshold) |
| S-G2 | `S_G2_relaxation_arc_regular` | `rate_cv=0.15` | L5 MUST_PASS — arc-regular by construction (fixed threshold, varying charging rate) |
| S-H | `S_H_convex_learner` | `n_runs=60` | T1 MUST_FAIL — forgetting is a function of the endpoint alone (lemma) |
| S-H2 | `S_H2_wear_learner` | `n_runs=60`, `gamma=0.5` | T1 MUST_PASS — path-dependent damage by construction; the instrument must see it |

Sweeps and parameter variants are registered as rows via
`functools.partial` with named parameters; row names encode the
parameter, e.g. "S-C lobed ramp (lambda=0.25)", "S-D sine + white noise
(rho~20.0)", "S-F van der Pol mu=1.0".

The two learners (in `LEARNER_BATTERY`) fine-tune a linear model from a
task-A optimum on task B under schedules `constant / sawtooth /
cosine_restarts / grad_noise / loop`, an lr grid, and a fixed-variance
Gaussian predictive family N(x·θ, 1); each run records `pred_old`,
`pred_new`, `F`, `schedule`, `lr`, `seed`. An unstable lr grid is a hard
error (`RuntimeError`), not a clipped result.

## Gate semantics

Each gate prints one row per surrogate — the statistic, PASS/FAIL under
the candidate criterion — and flags a **VIOLATION** in exactly two cases:

- **PASS on a negative control** (a `MUST_FAIL` row): the "hypothesis"
  holds on a signal with no CRR content — it is not about CRR and may
  not enter a prereg.
- **FAIL on a positive control** (a `MUST_PASS` row): the instrument
  cannot see an effect that is true by construction.

Rows can also read `n/a` — not scoreable (e.g. too few events/cuts/runs
for the statistic to mean anything).

**GATE OPEN** = zero violations. **GATE CLOSED (n violations)** = the
hypothesis must be restated or a control added before anything proceeds
([lifecycle step 1](../protocol/study-lifecycle.md)).

### What each gate tests

- **L5** — the H-L5 shape (CRR.md §4): arc-CV beats clock-CV with the
  paired-bootstrap CI of the difference excluding 0 on the negative
  side, and the amplitude control scored the same way — by its own CI
  (`ci95_amp`), not by strict point CVs, which tie at floating-point
  precision on constant-period carriers. L5 rows in the committed
  tables carry `ci_amp=lo,hi`.
- **CUT** — *testability* of A3, not a prediction: on a symmetric cycle
  (sine, van der Pol) antipodes and extrema coincide — nothing to test,
  gate reads FAIL; on an asymmetric waveform (S-E) they disagree. The
  gate measures the median antipode–extremum distance as a fraction of a
  half-turn. H-CUT itself is scored on the system's **own events**,
  never on this noise-sensitive disagreement (CRR.md §2).
- **T1** — H-T1 in the T1x-1 form (CLAUDE.md §5): held-out R² of the
  best PATH predictor (C_new, C_old) beats the best ENDPOINT predictor
  (E_new, **E_old**) by the preregistered margin; even seeds fit, odd
  seeds score (never in-sample). E_old is required: on a convex learner
  it is a sufficient statistic for forgetting (the verified lemma). The
  restructure PR adds the lr-controlled reporting T1x-1 requires
  (audit #6). A PASS on S-H or FAIL on S-H2 is a violation.

The gate layer was corrected against A1′/R5 and its verdicts pinned by
tests in the restructure PR (audit #2, #3); EQ has **no gate yet** —
`gate_EQ` (SCOPE.md §4.3) is finding #12, and EQ cannot enter a prereg
until it exists.
