# Declaration — synthesis batches 31 and 32: ten new systems in the classes where CRR works (declared blind)

- **Written:** 2026-09-24 (prompt-log entry 131).
- **Anchored before any code:** this file is hashed, stamped with OpenTimestamps and pushed before `batch_31.py` and
  `batch_32.py` exist, and before any of the ten systems is computed. **No prototype was run for any row.** This
  differs from DECLARATION_29_30, where prototypes were seen.
- **Outcome rule:** the SYNTHESIS class (`docs/notes/2026-09-17_synthesis_class.md`), with outcomes computed by
  `crr.synthesis.harness.outcome` (R15).

## What these rows can and cannot be (the ladder, `Epistemic_Review/checks/ladder.py`)

The owner asked for new pre-registered predictions in the classes where CRR has been consistent, descriptive or
redundant (prompt-log entry 131). The map of prompt-log entry 129 gives those classes and their hit rates:
- MEMORY, bounded fading memory: 16/23;
- CYCLE, the cut on a rotor phase: 7/8;
- EVENT, own-event trains: 11/13;
- EQ-IG, static information geometry: 18/19.

**What the ladder allows.** Each row is declared and pushed before a run on a model world built by the same author, so
it sits at rung R4 (DECLARED-SYNTHETIC). Its synthesis outcome places it further:
- REDUNDANT-IG is R1;
- REDUNDANT-DOMAIN is R2: CRR landed on the domain's known result, "it adds nothing the domain lacked";
- ADDS is R3, a candidate until a named expert answers the class note's three questions;
- WRONG is a retrodictive fail;
- PROPOSES is a prospective candidate.

**What none of them can be:**
- **A ledger PASS.** Nothing here reaches R6 (PASS-0) or above, because no real, unseen data is used.
- **A PROSPECTIVE CANDIDATE by itself.** A row earns that label (`docs/notes/2026-09-18_sharp_regime_review.md` §3.2)
  only if it also names a real carrier absent from `data/SEEN.md`, has an open gate, and has a baseline that can win.
  The last column below says, per row, what that would take. The assessment is made after the runs and changes no
  outcome.

**Design rule.** A row in a working class can only add something if its proposition is not already the domain's
theorem. Each proposition below is therefore built so that the null (the domain's standard model) and the CRR variant
give different numbers. Where the domain has a theorem for the CRR variant, it is named, and the row is then expected to
read REDUNDANT-DOMAIN. That is an honest outcome in a working class, not a failure of the row.

## Common conventions

**A6 in continuous time and in maps.** The remembered quantity is the P3 age-weighted mean of the settled past:
- in maps, M_n = (1 − q)·z_n + q·M_{n−1};
- in continuous time, dM/dt = (z − M)/T_m, the exponential kernel with mean age T_m.

This is A6 with P3's weights at bounded strength ("never an accumulated count"). On these one-dimensional carriers
the Fisher–Rao Fréchet mean is replaced by the arithmetic weighted mean. That replacement is stated as a modelling
step here, and it is the same one batch 12 row 2 and batch 17 row 1 made.

**Thresholds.** A number "differs" or "exceeds" by more than 1 % relative, which is TOL_G and TOL_N of the harness.
Integrators are explicit fixed-step RK4. Every random stream is seeded. Every batch must rerun byte-identical.

**Surrogate.** Every row carries a must-fail or sanity surrogate, printed beside it. A surrogate that behaves otherwise
is reported as a violation in the row's weakness line. It does not change the outcome, which the harness computes.

## Batch 31: MEMORY (A6 with P3 weights) in five classic threshold models

**31-1. Ricker stock–recruitment with remembered density.**
- **Model.** x_{n+1} = x_n·exp(r(1 − M_n)), with M_n = (1 − q)x_n + q M_{n−1} and q = 0.5. The equilibrium is
  (x, M) = (1, 1).
- **Q.** The equilibrium first loses stability at r_c > 2·1.01: memory stabilises the Ricker map, as it raised the
  cardiac-alternans threshold in batch 12 row 2.
- **How r_c is found.** A scan of r over (0, 20] in steps of 0.001, taking the first r at which the spectral radius of
  the 2×2 Jacobian reaches 1. The row reports whether that eigenvalue is −1 (a flip) or a complex pair (a
  Neimark–Sacker bifurcation).
- **Null.** q = 0, which gives r_c = 2.
- **Domain.** Ricker's flip at r = 2, which is the null's value. No theorem is cited for the memory variant, so the
  domain value for Q is none.
- **Check.** The computed r_c(0.5) > 2.02.
- **Surrogate.** Beverton–Holt, x' = r x/(1 + (r − 1)M), at q = 0 has no loss of stability on (1, 20]; the domain says
  it is globally stable.
- **My prior:** uncertain. Averaging damps a period-2 flip but adds lag.

**31-2. SIR with behavioural distancing driven by remembered prevalence.**
- **Model.** β(P) = β₀/(1 + kP), with β₀ = 0.3/day, γ = 0.1/day (R₀ = 3), k = 50, I₀ = 1e-4, S₀ = 1 − I₀. RK4 with
  dt 0.01 over 400 days.
- **Q.** When P is the A6-remembered prevalence (dP/dt = (I − P)/T_m, T_m = 10 days), the epidemic's peak prevalence is
  higher than when P = I, by more than 1 %: a lagged response overshoots.
- **Null.** Instantaneous P = I.
- **Domain.** None for the memory variant.
- **Check.** The computed peak ratio exceeds 1.01.
- **Surrogate.** At k = 0 the two peaks must agree within 1e-9 relative, since memory cannot matter without a response.
- **My prior:** holds.

**31-3. Optimal-velocity traffic with a remembered headway.**
- **Model.** Bando et al.: dv_n/dt = a(V(h̃_n) − v_n), with a = 1, and h̃_n the A6-remembered headway
  (dh̃_n/dt = (h_n − h̃_n)/T_m, T_m = 0.5).
- **Q.** The linear string-stability threshold V'_c on V'(h*) is below Bando's a/2 = 0.5 by more than 1 %: memory
  destabilises the platoon.
- **How V'_c is found.** Per wavenumber k ∈ (0, π], take the largest real part of the eigenvalues of the 3×3 system in
  (x, v, h̃). V'_c is the smallest V' at which the maximum over k of that real part exceeds 1e-9, scanned in steps of
  0.0005.
- **Null.** T_m = 0, which gives 0.5.
- **Domain.** Bando et al. 1995, V'_c = a/2 for the null. None for the memory variant.
- **Check.** V'_c < 0.495.
- **Surrogate.** At T_m = 0 the scan must return 0.5 within one scan step.
- **My prior:** holds.

**31-4. Samuelson's multiplier–accelerator with permanent-income consumption.**
- **Model.** Y_t = C_t + I_t + G, C_t = c·P_{t−1}, P_t = (1 − q)Y_t + q P_{t−1}, I_t = v(C_t − C_{t−1}), with c = 0.8 and
  q = 0.5.
- **Q.** The critical accelerator v_c at which the equilibrium loses stability exceeds Samuelson's 1/c = 1.25 by more
  than 1 %: permanent income stabilises the cycle.
- **How v_c is found.** A scan of v over (0, 10] in steps of 0.001, using the companion matrix's spectral radius.
- **Null.** q = 0, Samuelson's model, with v_c = 1/c.
- **Domain.** Samuelson 1939, cv = 1, for the null. None for the memory variant (Friedman 1957 supplies the consumption
  function, not this threshold).
- **Check.** v_c > 1.2625.
- **Surrogate.** At q = 0 the scan returns 1.25 within one step.
- **My prior:** uncertain.

**31-5. The continuous logistic equation with remembered density.**
- **Model.** dN/dt = rN(1 − M/K), dM/dt = (N − M)/T.
- **Q.** The equilibrium never loses stability: there is no Hopf bifurcation for r·T in (0, 1000].
- **Encoding.** "No loss of stability on the scan" is encoded as the number 1000.0, so that the harness can compare it.
- **Null.** Hutchinson's discrete delay τ = T, which has a Hopf bifurcation at rτ = π/2.
- **Domain.** The weak (exponential) distributed-delay kernel is always stable (MacDonald 1978; Cushing 1977), encoded
  as 1000.0.
- **Check.** The eigenvalues' real parts are negative on the whole scan (rT over the grid (0, 1000] in steps of 0.01).
- **Surrogate.** Hutchinson's delay equation, whose characteristic equation λ = −r e^{−λτ} is solved on the same scan,
  must lose stability within 1 % of π/2.
- **My prior:** REDUNDANT-DOMAIN.

## Batch 32: CYCLE, EVENT, MEMORY on a rotor, EQ-IG

**32-1. The Brusselator under a slow drift of B, with H-L5's class on a Poisson carrier (EVENT/CYCLE).**
- **Model.** dx/dt = A − (B + 1)x + x²y, dy/dt = Bx − x²y, with A = 1 and B(t) = 3 + 0.3 sin(2πt/500). RK4 with dt 0.002
  over t ∈ [0, 5000], discarding the first 500.
- **Own events.** Upward crossings of x = 1.
- **The arc per cycle.** The Fisher arc on the Poisson (concentration) carrier, ∫√(ẋ²/x + ẏ²/y) dt.
- **Q.** CV(Fisher arc per cycle) < CV(period), and CV(Fisher arc) < CV(peak-to-trough amplitude of x). That is
  H-L5's arc-regular class beyond control (i).
- **Null.** The arc with the identity metric (control ii).
- **Domain.** None.
- **Check.** Both inequalities hold.
- **Surrogate.** None beyond the standing gate (`runs/phaseA/gate_L5.txt`, OPEN).
- **My prior:** uncertain.

**32-2. FitzHugh–Nagumo: H-CUT on the recovery event (CYCLE).**
- **Model.** dv/dt = v − v³/3 − w + I(t), dw/dt = ε(v + a − bw), with ε = 0.08, a = 0.7, b = 0.8 and
  I(t) = 0.5 + 0.1 sin(2πt/2000). RK4 with dt 0.01 over t ∈ [0, 20000].
- **Own events.** The recovery event is the downward crossing of v = 0.
- **The cuts.** `crr.instrument.core.antipodal_cuts` on `intrinsic_phase(v)`, started at the first upstroke (upward
  crossing of v = 0).
- **The competitor.** The nearest waveform extremum, from `peak_cuts(v, prominence=0.5, distance=100)`.
- **Q.** On at least 2/3 of recovery events, the event is nearer an antipodal cut than it is to the nearest extremum.
- **Null.** Chance, 0.5.
- **Domain.** None.
- **Check.** The fraction is at least 2/3.
- **Surrogate.** The symmetric van der Pol oscillator (μ = 5), where antipode and extremum coincide up to sampling:
  "nothing to test". The median absolute difference of the two distances must be at most 2 samples.
- **My prior:** uncertain.

**32-3. Lotka–Volterra with predators responding to remembered prey (MEMORY on a rotor).**
- **Model.** dx/dt = x(α − βy), dy/dt = y(δM − γ), dM/dt = (x − M)/T_m, with α = 1, β = 0.5, γ = 0.5, δ = 0.25 and
  T_m = 1.
- **Q.** The neutral centre becomes an unstable spiral: the largest real part of the Jacobian's eigenvalues at the
  equilibrium is above +0.01·(the imaginary part). Memory destabilises the cycle.
- **Null.** T_m → 0, the classical centre with real part 0.
- **Domain.** None.
- **Check.** The real part exceeds 0.01·|Im|.
- **Surrogate.** At T_m = 1e-6 the real part is within 1e-4 of 0.
- **My prior:** holds.

**32-4. The seasonally forced SIR in the biennial regime: H-L5's class (EVENT).**
- **Model.** β(t) = β₀(1 + 0.25 cos 2πt), with β₀ = 1250/yr, γ = 365/14 per yr, births and deaths μ = 0.02/yr, and
  the tuple chosen to sit in the measles-like biennial regime. RK4 with dt 1e-4 yr over 200 years, the first 100
  discarded.
- **Own events.** The upward crossing of I through its mean.
- **The arc.** The Fisher arc on the Poisson carrier of (S, I) between events.
- **Q.** H-L5 fails here: CV(clock) < CV(arc), i.e. the model is clock-regular. That agrees with the ledger rows
  MEAS2-1 and MEAS2-2 (measles, 0/17).
- **The decisive quantity.** The class index CV(clock)/CV(arc).
- **Null.** The identity-metric arc.
- **Domain.** Phase-locking to the annual forcing: inter-epidemic intervals are integer years. The domain value is the
  class index when the clock's CV is that of exact integer-year intervals, computed on the same run.
- **Check.** The index is below 1.
- **Surrogate.** None beyond the standing gate.
- **My prior:** REDUNDANT-DOMAIN or REDUNDANT-IG.

**32-5. Photon or event counting: the number of resolvable steps between two Poisson rates (EQ-IG, A1′).**
- **The unit (A1′).** The unit is the system's own resolvable step: one event is one step, observed over a window T.
- **Q.** The number of resolvable steps between rates λ₁ = 4 and λ₂ = 9 events per unit, in a window T = 25, is
  2√T(√λ₂ − √λ₁) = 10, the Fisher arc of the Poisson family in its own unit.
- **Null.** The number of clock-noise steps, (λ₂ − λ₁)T/√(λ₁T), which uses the Gaussian unit at λ₁.
- **Domain.** Anscombe's variance-stabilising transform: the difference of 2√(counts) in units of its standard
  deviation 1. The domain value is computed from 200 000 simulated windows at each rate (seed 325), as the mean
  difference of 2√N.
- **Check.** Not needed if the domain agrees.
- **Surrogate.** None.
- **My prior:** REDUNDANT-DOMAIN.

## Discipline and what follows

- **Fixed now:** the parameters, grids, criteria and surrogates above. The code implements them as written.
- **If a first run shows an implementation error** (a bug, not an unwelcome number), the fix is reported in AGENT_LOG
  with the first run's output kept in the scratchpad. The row's text is regenerated from the corrected numbers, never
  edited to fit (R15).
- **The declared propositions are not changed** after any run.
- **After the runs, one table:** per row, the outcome, its rung, and what a real-data prereg would need to earn
  PROSPECTIVE CANDIDATE: an unseen carrier, a gate, a baseline that can win, and a threshold. It is written in
  `docs/notes/2026-09-24_in_paradigm_predictions.md`.
