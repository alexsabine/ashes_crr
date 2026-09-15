# Pre-registration — learner unit test (Phase 0.5). Written 2026-09-14 before any run.

## Question
Does the CRR-CLS Ω-landscape depend on the Fisher-speed *estimator*, and does an estimator-free
unit collapse the four benchmark landscapes (MNIST, Fashion-MNIST, KMNIST, CIFAR-10) onto one optimum?

## Two units, same pipeline (Clean_CRR crr_cl_bench.py logic; CIFAR = faithful PyTorch port), nothing else changed
- **diag** (the repo's): v = sqrt(Δθᵀ F̂ Δθ), F̂ = running EMA of (n·ḡ)² (batch-mean gradient, n=batch size). Ledger values.
- **kl** (estimator-free): v = sqrt(2 · mean_probe KL(p_θ_old(y|x) ‖ p_θ_new(y|x))) over a fixed probe set of
  512 held-out inputs (test indices 5000–5511, disjoint from the 5000 scoring images), one extra forward pass per update.
  This is the exact Fisher–Rao length of the update on the model's own predictive family to second order, in nats^½,
  averaged *per input*: no diagonal approximation, no batch factor, no dependence on parameterisation.
  It still scales with learning rate, as the system's real travel does.
Both feed the unchanged schedule α_fast = K(v̂/Ω), α_slow = K(v̂/(Ω·e)), v̂ = 0.9 v̂ + 0.1 v.

## Runs
Standard stream, seeds 0–2, d = e fixed, Ω ∈ {0.25, 0.5, 1, 2, 4}, unit ∈ {kl} on all four datasets
(diag landscapes taken from the ledger; diag re-run at Ω=1 once per dataset as a pipeline check).

## Hypotheses (scored once)
- **U0 (pipeline check):** diag Ω=1 re-run within 1.0 pt of the ledger value on each dataset. If not, all below is void.
- **U1 (collapse):** under kl, the best grid Ω is the same point on all four datasets, or every dataset's best is
  within 0.5 pt of the accuracy at one common Ω. FAIL if any pair of datasets has best-Ω differing by ≥ 4× with
  the loser trailing by > 1.0 pt at the other's optimum.
- **U2 (theory value):** the common optimum under U1 is Ω = 1. FAIL if Ω=1 trails the best grid point by > 1.0 pt
  on ≥ 2 datasets.
- **U3 (usefulness):** CRR-CLS(kl) at Ω=1 ≥ best tuned CLS-ER (ledger) − 0.5 on ≥ 3 of 4 datasets.
- **U4 (the estimator was the scale):** median v_F under kl and diag differ by a dataset-dependent factor
  (predicted: ratio kl/diag larger on CIFAR than on MNIST). Reported, not scored.

## Outcomes named in advance
(a) U1 ∧ U2 pass → the learner has a unit; Ω=1 is a claim again; Phase 1 tests a zero-parameter schedule.
(b) U1 pass, U2 fail → one universal calibrated constant; Phase 1 tests *that* constant.
(c) U1 fail → the schedule is architecture-dependent; Phase 1 must be framed as a one-scale adaptive EMA vs tuned fixed EMA.
