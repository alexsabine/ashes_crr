# Declaration: the Cramér–Rao reading of C·Ω = 1 (prompt-log entry 207)

Pushed before `theory/checks/cramer_rao_reading.py` exists. A mathematical check on synthetic families; no data, no
study, no ledger row (R8). Nothing it prints can change a verdict; it can only say whether the reading is already in the
record and where it would have bitten.

**The owner's reading.** On a monotone segment, C·Ω = 1 is the Cramér–Rao limit.

**Our reading of the reading, fixed before the script.** On a monotone segment C = C* (P1). If the unit σ is the
Cramér–Rao length 1/√(nI) (A1′ as the retrodictions already name it: `crr_retrodictions.py` row d2, synthesis batches 01,
02, 06, 23, 26), then C counts Cramér–Rao standard errors travelled, and C·Ω = 1 at Ω = 1 says "cut when the change first
reaches one resolvable standard error". As a cut rule this is the spec's removed strong form (§XI.1; `verify_spec_math`
[XI.1]): it coincides with A3 only where the half-turn is one unit, ρ = 1/Ω.

**Checks and predictions (each printed with a computed HOLDS / FAILS).**

- **CR1, the unit.** Gaussian location family N(θ, s²), n data, I_n = n/s². On a monotone path of displacement Δ,
  `arc_length` with σ = 1/√I_n equals |Δ|√I_n (the count of Cramér–Rao standard errors), to 1e-12. Doubling n multiplies
  the count by √2 (Fisher additivity).
- **CR2, a varying information.** Bernoulli family, monotone path p: 0.1 → 0.9. The sum of local Cramér–Rao steps
  Σ|Δp|/√(p(1−p)) converges to the Fisher–Rao length 2(arcsin√0.9 − arcsin√0.1) as the grid refines. On a non-monotone
  path 0.1 → 0.9 → 0.5 the step count exceeds the chord (P1), so "C counts resolvable steps from the start" holds only on
  the monotone segment.
- **CR3, what one step means.** Two equal-variance Gaussians at Fisher distance d: KL = d²/2 and the equal-prior Bayes
  error is Φ(−d/2). At d = 1: KL 0.5, error 0.3085. One Cramér–Rao step is a change barely resolvable from the data the
  unit was defined on; it is a detection threshold, not a limit on how far the system may travel.
- **CR4, the scalar rule on a half-turn.** A sampled half-turn of extent ρ units (ρ ∈ {1, 2, 4.54}), Ω ∈ {0.5, 1, 2}.
  Noise-free (monotone): the rule "cut when C reaches 1/Ω" fires ⌊ρΩ⌋ times per half-turn (to within one cut) and falls on
  the antipode only where ρΩ = 1. With added noise the count rises with the arc, ≈ Ω·C per half-turn with C = C* + S.
- **CR5, where the Cramér–Rao reading does live in the continual-learning work: the Laplace weight.** Gaussian linear
  model with known noise, task A then task B. The penalty ½(θ − θ_A)ᵀF_A(θ − θ_A) with F_A the true Fisher is half the
  squared distance in task-A Cramér–Rao units, and weight λ = 1 gives the exact sequential-Bayes posterior mode (to 1e-10).
  With a mis-scaled Fisher c·F_A (c ∈ {0.1, 10}), the λ on a fine grid that best recovers the Bayes mode is 1/c, not 1:
  λ = 1 is right only when the unit is right, which is what SEC calibrates.
- **CR6, the H-EQ rule is not that weight.** The same model, the Ω = 1 gradient-ratio rule w = ‖g_B‖/‖g_past‖ (past term
  the true-Fisher penalty), full-batch gradient descent from θ_A. Prediction: it stops on the Pareto set but not at the
  Bayes mode; its distance from the mode, in task-(A+B) Cramér–Rao units, is printed. The Cramér–Rao reading gives Ω = 1 no
  meaning in H-EQ.

**Outcome rule.** If CR1–CR5 hold and CR6 lands off the Bayes mode, the reading is (i) correct as a statement about
units, (ii) already in the record as A1′'s Cramér–Rao unit (definitional, R0) and as the removed rupture law (FAILS),
and (iii) present in the continual-learning work only through the Laplace weight, not through H-EQ. Any other outcome is
reported as printed.
