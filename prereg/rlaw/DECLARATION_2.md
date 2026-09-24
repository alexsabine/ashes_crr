# Declaration 2 — the operational mathematics of the regeneration-law study (RLAW), checked before the prereg

- **Written and pushed:** 2026-09-24 (prompt-log entry 137). It is pushed before
  `Regeneration_Law/checks/operational_checks.py` exists and before any data of the study is fetched or opened.
- **Why a second declaration.** Declaration 1 checked the law itself (M1–M10). The literature check
  (`docs/citations/rlaw_literature_2026-09-24.md`) and the data check (`docs/citations/rlaw_data_availability_2026-09-24.md`)
  raise four questions about how the law is *measured* in the five domains. They must be settled on synthetic series
  before the study is registered.
- **No data is involved.** Every check below runs on formulas or synthetic series, with fixed seeds.

## What the literature check binds (read before this declaration was written)

**(L1) The formula and (L2) its optimality for an inferring system are published.** They are Muth 1960, Kalman 1960 and
Harvey 1989 (FOUND). A pass on an inferring system therefore tests only whether that system is Muth-optimal. The law
itself is not CRR's there.

**(L3) Real agents at the optimal level is untested.**
- The literature tests only the direction (forecasters: Coibion & Gorodnichenko 2015; learners: Behrens 2007 and its
  successors).
- Where levels were estimated, they are often far from optimal. The two-step task's second-stage learning rate is about
  0.42 against an optimal gain of about 0.05 (the literature agent's own computation from Daw 2011).

**(L4) Universality, including non-inferring systems, is NOT FOUND.**
- It is the CRR-only content.
- The physics literature states the contrary for heat conduction. Memory there is set by diffusivity and depth, not by
  the variability of the forcing (FOUND as a counter-statement).

**One consequence for the study.** The soil domain is the only one where a pass would be CRR's alone. There, the
foreseeable result from physics is a FAIL. The prereg must say so in advance.

## The checks, each with its expected result (declared before the run)

| id | check | expected |
|---|---|---|
| M11 | **LTI independence.** A fixed first-order filter (α₀ = 0.3) and a fixed two-stage filter (two first-order stages in series, each 0.5, a crude diffusion analogue) are each driven by local-level environments with v ∈ {0.05, 0.3, 1, 3} (n = 5000). For each, print the fitted partial-adjustment α̂ and K(v). | First-order: α̂ = 0.30 ± 0.01 at every v, while K(v) runs from 0.05 to 0.91. A linear time-invariant system meets the law at one v at most, by coincidence. It cannot track v across environments unless its physical constant co-varies with v. Two-stage: α̂ moves with v (misspecified fit), and the size of the movement is printed. |
| M12 | **Estimator recovery at the unit lengths the study will use** (n = 60, 185, 365, 840). Environment: local level with v ∈ {0.1, 0.3, 1}. System: exponential smoother with α = K(v), an offset c = 0.5 σ_ε, report noise 0.05 σ_ε and a reporting quantum 0.1 σ_ε. Estimators: v̂ by the ML local-level fit (Declaration 1, M9); α̂ by partial-adjustment least squares **with intercept**. 100 seeds each. | Print the fraction of units whose α̂/K(v̂) lies within a factor of 2, and within a factor of 1.5. Expected at least 0.9 within a factor of 2 for n ≥ 185. At n = 60 it is unknown. If it is below 0.8 there, units of that length are not used, and whole-sample units replace them. |
| M13 | **The bandit arm (the two-step domain).** One arm's reward probability follows a Gaussian random walk (sd 0.025 per trial, reflecting at 0.25 and 0.75) and is observed as a Bernoulli outcome only on visits, with visit gaps geometric of mean ḡ ∈ {1, 2, 4, 8}. Find the constant delta-rule rate minimising the mean squared error of the estimate, by grid over α, 200 seeds × 2000 visits. Compare it with K(v), where v = 0.025 √ḡ / σ_ε and σ_ε = √(mean p(1 − p)). | Within 25 % of K(v) at every ḡ. The argmin and the ratio are printed. If the ratio is off by more than 25 % at some ḡ, the prereg uses the numerically optimal rate as the law's prediction for that domain, and says so. |
| M14 | **Learning-rate recovery in the two-step second stage.** Simulated Q-learners (α ∈ {0.05, 0.1, 0.3, 0.6}, inverse temperature β = 5, 125 trials, the Kool environment) are fitted by per-subject ML over (α, β), with a deterministic grid in α (200 log-spaced points on [0.005, 1]) and a bounded scalar β fit. 100 simulated subjects per α. | Print the fraction of α̂ within a factor of 2 of the true α. Expected poor recovery at α = 0.05 (125 trials carry little information about a slow rate). The number is printed and sets the attainable ceiling for that domain's per-subject criterion in the prereg. |

**What failure of a check means.**
- If M11's first-order α̂ is not 0.3 ± 0.01, the estimator is wrong, and it is fixed before anything else.
- M12–M14 are calibrations. Their numbers set unit lengths and attainable ceilings in the prereg. They are not verdicts
  on the law.

## The gate (R4), declared here and built after these checks

The gate is `Regeneration_Law/checks/gate_rlaw.py`. Each domain gets synthetic units with that domain's lengths, noise
levels and reporting quanta. Every registered hypothesis is scored on them by the same scorer the study will use.

| gate row | the synthetic system | expected |
|---|---|---|
| G+ | α = K(v_own) for each unit: the law holds | PASS on every registered hypothesis (positive control) |
| G−over | α = min(0.95, 3 K(v_own)): an over-reactor | FAIL |
| G−under | α = K(v_own)/3: a sluggish system | FAIL |
| G−free | α drawn log-uniform on [0.02, 0.9], independent of v | FAIL |
| G−LTI | one fixed α per domain, set at the domain's median K(v) of G+, units with different v (an LTI system, M11) | FAILS the tracking hypothesis wherever the domain's v varies. It may pass the level test, and that is why the level test alone is not the law. |

**A registered hypothesis that passes on G−over, G−under or G−free is not about the law. It is deleted before the prereg
is hashed.**
