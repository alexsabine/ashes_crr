# Declaration: SPA1, is SEC4's method already known? A full prior-art sweep (pushed before any search)

**The request.** Prompt-log entry 254 (2026-09-30T06:02Z): "Look at SEC 4 again. Do a deep dive online search for
whether this is already known in the field or not. Full literature sweep."

**Why it is needed.**
- The record flagged the gap on 2026-09-30 (the answer to prompt-log entry 242): the secant-calibration prior-art search
  had never been done.
- The only SEC citations so far are SEC5's, on Progress & Compress (`docs/citations/sec5_2026-09-29.md`).
- SEC4-1 is the record's only PASS-1 (`reports/sec4.md`). It did not replicate in SEC5.

## What SEC4's method is (from `prereg/sec4/PREREG.md` and `reports/sec1.md`, fixed now)

1. **A Laplace (EWC-type) quadratic penalty** on the past tasks, at the textbook weight w = 1/2, on the task-size-weighted
   diagonal empirical Fisher.
2. **The units calibration (SEC).**
   - At each task's end, the task's Fisher is rescaled by s_j = c_j / ρ_j.
   - c_j is the loss's **secant curvature** along the path the learner travelled during the task: the change of the mean
     clean gradient between the first and last 10 % of steps, projected on the change of the mean parameters, divided by
     the squared length of that change.
   - ρ_j is the curvature the Fisher claims along the same direction.
3. **The stability clip.** Each coordinate of the calibrated importance is clipped at κ / (lr · w), with κ = 0.5. This
   keeps the penalty's explicit step at half the gradient-descent stability edge.
4. **The claim:** with 1–3, no per-dataset tuning of the penalty strength λ is needed (not behind a tuned λ).

## The positions graded (rule as RQM/RRM: MIXED if states and contradicts; else REDUNDANT if states; else PARTLY REDUNDANT if close; else NOT FOUND)

| id | position | forecast |
|---|---|---|
| S1 | the EWC/Laplace penalty strength λ must be tuned per dataset because the (empirical) Fisher's scale is wrong or arbitrary, stated in continual learning or Bayesian deep learning | REDUNDANT |
| S2 | rescaling a Fisher or Laplace precision by a factor fitted to the loss's observed curvature (a secant, finite difference, line-search or Hessian-vector check) is published | PARTLY REDUNDANT |
| S3 | a curvature scale fitted along the optimisation path (quasi-Newton or secant style) is used to set a continual-learning penalty or an online Laplace posterior | PARTLY REDUNDANT |
| S4 | setting the penalty or prior precision without tuning, by a principled rule (Bayes weight, marginal likelihood, evidence, or calibration), is published for continual learning | REDUNDANT |
| S5 | clipping or bounding the penalty curvature by the step size (the stability edge, lr·λ·F < 2) to prevent divergence is published for regularisation-based continual learning | PARTLY REDUNDANT |
| S6 | a tuning-free Laplace or EWC weight is reported to match a tuned λ across many datasets | NOT FOUND IN THE SWEEP |

**The families** (one agent each; dossiers `docs/citations/spa1_f{1,2,3}_2026-09-30.md`, claims `checks/claims_f{1,2,3}.py`,
quotes verified by `checks/verify.py`, graded by `checks/grade.py`):
- **F1:** the scale of the Fisher in continual learning and Bayesian online learning. EWC and online EWC; the empirical
  against the true Fisher; K-FAC Laplace and online Laplace; VCL; tempered and cold posteriors; λ sensitivity studies
  (S1, S6).
- **F2:** calibrating curvature. Secant and quasi-Newton scaling; GGN and Fisher scale checks; Laplace Redux and
  prior-precision selection by marginal likelihood; Hessian-vector calibration of diagonal approximations (S2, S3).
- **F3:** tuning-free and stable regularisation. Hyperparameter-free continual learning; principled λ; stability-edge and
  step-size-aware penalties; clipping importance weights; divergence of EWC at large λ (S4, S5, S6).

**The verdict rule (computed by `grade.py`):**
- **KNOWN** if S2 or S3 is REDUNDANT **and** S4 is REDUNDANT (the calibration is published, and so is tuning-free use in
  continual learning);
- **PARTLY KNOWN** if any of S2–S5 is REDUNDANT or PARTLY REDUNDANT;
- **NOT FOUND IN THE SWEEP** otherwise.

"Not found" is never "novel". A KNOWN verdict would mean SEC4-1's PASS-1 is a replication of a published method on new
carriers, and the ledger's wording and the Compute_Savings premises would have to say so.

## Forecast (written now)

**PARTLY KNOWN.**
- The Fisher's scale problem (S1) and principled prior precisions (S4, by marginal likelihood) are known.
- A secant calibration of the Fisher used to make the Laplace weight tuning-free in continual learning (S2 and S3 as
  states) is probably not published in this exact form.
- The stability clip (S5) is a standard step-size safeguard.
