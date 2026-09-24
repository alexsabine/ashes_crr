# Declaration 1 — the mathematics of the regeneration law (CRR 2.0), checked before any study is registered

- **Written and pushed:** 2026-09-24 (prompt-log entry 137), before `Regeneration_Law/checks/math_checks.py` exists.
- **The owner's instruction:** "Ensure the mathematics is internally sound first."
- **No data is involved.** Every check below runs on formulas or synthetic series.

## The law as stated by the owner

**The law.** For any system that regenerates from its settled past, the memory depth is **q = 1 − K(v)**.
- K(v) = (v/2)(√(v² + 4) − v) is P4's steady-state Kalman gain.
- **v** is the environment's drift per occasion, in the system's own resolvable steps (A1′).
- The system's weight on its newest input is **α = K(v)**, and its P3 memory weights are q^k.

## The checks, each with its expected result (declared before the run)

| id | check | expected |
|---|---|---|
| M1 | K(v) is the steady-state Kalman gain of a random walk (drift variance σ_η²) observed in white noise (σ_ε²) with v = σ_η/σ_ε: sympy solves the prior-variance Riccati fixed point and simplifies K = P/(P + σ_ε²) | holds (identity) |
| M2 | K(1) = 1/φ = (√5 − 1)/2 | holds |
| M3 | Muth 1960: among exponential smoothers with weight α, the stationary one-step prediction error of the local level is minimised at α = K(v). Check on a grid of v ∈ {0.05, 0.2, 1, 3} by the closed-form stationary variance | holds (argmin within 1e-3 of K(v)) |
| M4 | **the own unit is load-bearing.** With a reporting quantum δ (the resolution of the system's own reports), σ_own² = σ_ε² + δ²/12 and v_own = σ_η/σ_own. The predicted α changes when δ is comparable to σ_ε. Printed for δ/σ_ε ∈ {0, 0.5, 1, 2} | α*(v_own) < α*(v_ε) whenever δ > 0 (numbers printed); the own unit makes the law differ from Muth's |
| M5 | limits and A6. As v → 0, K → 0 and q → 1, the accumulated count A6 forbids. As v → ∞, K → 1 (no memory) | for every v > 0, q < 1, consistent with A6; at v = 0 exactly the law and A6's "never an accumulated count" conflict. This is stated as a boundary of the law's scope |
| M6 | P3 consistency: the geometric weights of an exponential smoother with weight K have mean age (1 − K)/K = q/(1 − q) | holds |
| M7 | **the law is not H-EQ.** The update m' = (1 − K)m + K·y pulls with weights 1 − K (the settled past) and K (the new datum). Equal pull (Ω = 1) holds only at K = 1/2, i.e. v = 1/√2 | holds: equal pull at v = 0.7071 only. O1's phrase "at Ω = 1" cannot be kept; CRR 2.0 replaces equanimity with the Kalman balance |
| M8 | scope: the law is derived for a random-walk environment. For an AR(1) environment (φ = 0.7, a mean-reverting drift, as daily air-temperature anomalies are) plus white noise, the optimal steady-state gain is computed from its own Riccati and compared with K(v̂), where v̂ comes from fitting a local-level model to that environment | they differ (the size is printed); the study must fit the local-level model and state the approximation as part of the operationalisation |
| M9 | estimator recovery. On synthetic series of the study's lengths (170, 500, 2500, 200 occasions; seeds fixed): the local-level ML estimate of v, and the least-squares estimate of α for a system that smooths the environment with α, have bias and SE (printed) | the bias of α̂ is below 10 % for n ≥ 500. For n = 170 and 200 the SE may be large: a power limitation to be stated in the prereg |
| M10 | unit invariance: rescaling the environment and the system by a constant leaves v̂ and α̂ unchanged | holds |

**What failure of a check means.** If any M1–M3, M6 or M10 fails, the implementation is wrong and is fixed before
anything else. A different magnitude in M4, M8 or M9 is not a failure; it is information the prereg must use.
