# C·Ω = 1 on a monotone segment as the Cramér–Rao step: does it help, and is it already in the record?

Owner's question: prompt-log entry 207. This is a note to the auditor, not evidence (R8).
- **Declaration.** `docs/notes/2026-09-25_cramer_rao_declaration.md`, pushed at 052c2fc before the script existed.
- **Check.** `theory/checks/cramer_rao_reading.py`, with its output pinned in `.txt`, a byte-identical rerun, and a CI
  check at tolerance. All six items (CR1–CR6) print HOLDS.
- **Other numbers.** Every other number below is quoted from a ledger row or a pinned output named beside it.

## 1. Does it make sense? Yes, as a statement about the unit

**The chain of reasoning.**
- **P1.** On a monotone segment the arc equals the chord, C = C*.
- **A1′.** Count in the unit σ that is the system's own resolvable step. For a parametric family that step is the
  Cramér–Rao length 1/√(nI): one standard error of the best unbiased estimate from the occasion's n data.
- **So C counts standard errors.** C is the number of standard errors the state has moved (CR1: 1.5, 2.1213 and 3.0 steps
  at n = 1, 2 and 4, to 0 difference; the count grows as √n, which is Fisher additivity).
- **Where the information varies,** the arc is the sum of local Cramér–Rao steps. It converges to the Fisher–Rao length:
  on the Bernoulli family, 1.8545904281 against 1.8545904360 at 10,000 steps (CR2).
- **Off the monotone segment,** the step count exceeds the distance from the start. On the path 0.1 → 0.9 → 0.5 it is
  2.781886 steps against a chord of 0.927295 (CR2). **The owner's qualifier "on a monotone regime" is therefore
  essential.**

**What C·Ω = 1 then says.** At Ω = 1, cut when the change first reaches one Cramér–Rao standard error. At other Ω, cut
at 1/Ω standard errors.

**What one step means (CR3).** Two states one Fisher unit apart differ by KL = 0.5 nat. An observer holding the data
that defines the unit confuses them with probability 0.3085, against 0.5 for a coin. One step is the threshold where a
change becomes resolvable.

**A correction in wording: "unit" or "resolution threshold", not "limit".** The Cramér–Rao bound limits the variance
of an estimator. It places no limit on how far a system may travel before it cuts. Four further qualifications:
- the bound is local;
- it scales with the data counted (per datum or per window, a carrier fact the axioms do not fix, row d2's weakness);
- it is attained only by an efficient estimator;
- it is mis-specified when the model is wrong.

## 2. Is it already in the record? Yes, in three places

1. **A1′'s unit is named as the Cramér–Rao length throughout the retrodictions.**
   - Where: `crr_retrodictions.py` row d2 ("Cramer-Rao unit 1/sqrt(I)"), battery row 14, and synthesis batches 01, 02,
     06, 08, 10, 23 and 26.
   - Grades: row d2 is definitional ("A1′ *names* the Cramer-Rao length as the unit — standard mathematics declared, not
     derived"). The synthesis rows that use it land on the domain's own theorem: "Cramér–Rao counts" is one of the named
     groups among the fifty REDUNDANT-DOMAIN rows in `theory/retrodictions/README.md`. Batch 23 is Clarke–Barron's
     theorem restated in D1's names.
   - One instrument fact (batch 06, AGENT_LOG 30): `unit_sigma` returns 0.8629 of the Cramér–Rao unit on white
     residuals. The ρ the studies report is therefore inflated by 1.1589 relative to a true Cramér–Rao count. So "C in
     instrument units" is not exactly "C in Cramér–Rao steps".
2. **The rule C·Ω = 1 was removed, then tested, and failed.**
   - The external specification removed it (§XI.1): "a monotone cut occurs at C=H, not generally C=1. The old formula
     agrees only in the special normalization H=1". `theory/checks/verify_spec_math.txt` [XI.1] proves that
     equivalence.
   - Retrodiction row 12 ran the rule and graded it FAILS. On the noisy Wilson–Cowan rhythm (σ = 0.0333, ρ = 4.54) it
     cuts 9.29 times per antipodal half-turn at Ω = 1. On the balanced LIF neuron the C = 1 cut fires at 4 % of the
     interspike interval.
   - CR4 shows why, in the Cramér–Rao reading. The rule is a counter of Cramér–Rao steps.
     - On a monotone half-turn it fires about ⌊ρΩ⌋ times: 4 cuts at ρ = 4.54 and Ω = 1.
     - It lands on the antipode only where ρΩ = 1.
     - With noise it fires about Ω·C = Ω(C* + S) times (6 cuts on a noisy half-turn with C = 6.1724, C* = 4.5639).
   - **So in this reading, "C·Ω = 1 at the cut" means ρ = 1/Ω.** At Ω = 1 that is a system whose whole half-turn is
     exactly one standard error. Such a system barely resolves its own cycle, and that, not the cut, is what the
     Cramér–Rao limit describes.
   - D1 says ρ is measured, never predicted. Measured values are not 1: ρ = 4.54 on Wilson–Cowan is a half-turn of
     10.3 nats, confused with its start with probability 0.0116 (CR3's d = 4.54 line).
   - **Where the reading is exactly right.** In row 12 the neuron's own event is a chord condition, C* = 1, with σ the
     threshold gap. On a noise-free (monotone) rise C = C*, so the rule and the event coincide there. With noise they
     separate: the rise arc is 10.77 σ against a chord of 1.117.
3. **Fisher–Rao path length is already counted in Cramér–Rao units wherever the studies used a Fisher metric.**
   - T1x2's path Σ√(2·KL_step) is a Fisher–Rao length, exact on the Gaussian (SCOPE P8). It FAILS on 5/5 carriers
     (T1X2-1).
   - The measles study scored H-L5 on a Poisson-rate carrier, whose Fisher metric counts Cramér–Rao steps. It FAILS on
     0/17 cities under both metrics (MEAS2).
   - H-L5 is a coefficient of variation, and a CV does not change when the unit is rescaled by a constant. So renaming a
     constant unit as Cramér–Rao cannot move an H-L5 verdict. Only a unit that varies along the record could, and the
     carrier metrics already test that.

## 3. Would it have helped the continual-learning work?

**Not for H-EQ.** In v3.1 and in the specification, Ω is the regeneration weight, a gradient-norm ratio. It is not a
cut scale, and §XI.1 separated the two for exactly that reason. CR6 runs the Ω = 1 rule on a Gaussian linear model where
the Bayes answer is known:
- it stops on the Pareto set (cos(g_B, g_past) = −1.000000);
- it is 6.1688 Cramér–Rao units from the sequential-Bayes mode.

The rule balances the two gradients' *norms*. That condition holds anywhere on the Pareto set, so nothing in it picks
the point one standard error would single out. This matches the record:
- the rule is 5.2082–18.1162 standard deviations from the exact posterior on six carriers (BAYES1-B1);
- it reduces to a fixed replay weight (EQX-1).

**Yes, implicitly, through the Laplace weight, where the reading is exactly right (CR5).**
- **With the true Fisher.** A penalty ½(θ − θ_A)ᵀF_A(θ − θ_A) is half the squared distance in task-A Cramér–Rao units.
  At weight 1 it gives the exact sequential-Bayes mode (distance 0.00e+00).
- **With a mis-scaled Fisher c·F_A.** The right weight is 1/c: 10.0000 at c = 0.1 and 0.1000 at c = 10. Weight 1 then
  misses the mode by 10.3668 and 5.3654 Cramér–Rao units.
- **So weight 1 is correct exactly when the unit is correct.** That is the record's continual-learning story:

| where | the Laplace weight on the estimated Fisher | after the secant calibration of the unit (SEC) |
|---|---|---|
| EQ3-B (seen) | not behind the tuned weight on 3/6 | — |
| SEC1-3 (seen, R5) | not behind on 6/12 | 9/12 (PASS on seen data, at the threshold, FRAGILE) |
| SCL3-3 (unseen) | not behind on 4/10 | 9/10 (**PASS-0**; not PASS-1, SCL3-S FRAGILE) |

- **SEC is a repair of the Cramér–Rao unit.** It rescales the Fisher so that the quadratic matches the curvature the loss
  actually showed along the path travelled. An SGD endpoint is not an efficient estimator, and an estimated Fisher is not
  the learner's Cramér–Rao information.
- **The repair is partial.** SEC1-4 FAILS: the calibrated tuned weight does not collapse (span 849.00×; 8 of 12 optima
  in 0.423–1.41).

## 4. Answer

- **Does it make sense?** Yes. On a monotone segment, and with σ the Cramér–Rao length, C·Ω = 1 at Ω = 1 means "the
  change has reached one resolvable standard error". Call it the Cramér–Rao *unit* or *resolution threshold*, not a
  limit.
- **Is it already implicit?** Yes. It is A1′ with the unit named, which the retrodictions do throughout (definitional,
  or the domain's own theorem). As a cut law it is the removed strong form, equivalent to ρ = 1/Ω, and it FAILS where
  tested (row 12).
- **Would it have helped?**
  - It would have predicted row 12's failure in advance: a step counter cannot find a half-turn of ρ ≠ 1 steps. It would
    not have rescued the rule.
  - It changes no H-L5 or T1 verdict (the CV is unit-free; the Fisher-metric runs already count Cramér–Rao steps).
  - It gives H-EQ's Ω = 1 no meaning (CR6).
  - Where it does apply, the Laplace weight, the programme reached the same point by another route: raw Laplace was a
    required baseline, and SEC calibrates the unit. That is where the only strongly anchored held-out passes (SCL3,
    PASS-0) come from.
  - Stated in advance, it might have pointed at unit calibration sooner. That is hindsight, and it is not counted as a
    prediction (R3, R15).
- **Rung.** The reading is R0–R2: Fisher, Cramér and Rao's mathematics, correctly placed inside A1′.
