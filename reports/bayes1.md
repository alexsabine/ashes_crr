# Study BAYES-1 — the normalised penalty step against the exact sequential Bayes posterior (2026-09-22)

Ledger rows BAYES1-B0 … BS (`ledger/LEDGER.md`); every number below is in a row or in `runs/bayes1/score.txt`.
Prereg `prereg/bayes1/PREREG.md`, hash `ff037a7b`, anchor push-timestamp only (prereg commit 49072aa pushed
2026-09-22T15:52:37Z; data fetched 15:52:56Z); frozen scorer `runs/bayes1/frozen/bayes1_score.py`. Six unseen PMLB
regression streams, a whitened random-feature readout (D = 31), the exact sequential posterior as the referee, the score
being an arm's distance from the final posterior mean in posterior standard deviations per dimension.

## 1. The verdict

**B0, the precondition, is NOT DECIDABLE on 6/6.** The Bayes arm (the fixed weight λ = 1 on the exact curvature, run by the
same optimiser as every other arm) ended 0.18 to 0.89 posterior standard deviations from the exact posterior on the six
carriers, against the committed tolerance of 0.1 that it met on the synthetic gate (0.0650). By the prereg, rows B1–B3
are therefore reported without verdict. The optimiser, not the rule, was being measured at that tolerance, and the
tolerance was set on a surrogate that converged faster than the carriers.

What the report can say, from the rows, without a verdict:

| row | predicted | the script's line | margin |
|---|---|---|---|
| B1 the rule is not Bayes | PASS | PASS 6/6 | the rule sits 5.2 to 18.1 posterior sd from the posterior; the Bayes arm's own error is 0.18 to 0.89 |
| B2 the rule beats a 16×-miscalibrated Bayes | FAIL (surrogate) | FAIL 6/6 at c = 16 and at c = 1/16 | miscalibrated Bayes is closer by 1.7 to 9.7 sd |
| B3 the rule's invariance to the curvature scale | FAIL (surrogate) | FAIL 6/6 | +0.12 to +0.55 at c = 16, −0.25 to −3.86 at c = 1/16 |
| B4 the tuned λ is the Bayes weight | — | 6/6 | λ = 1 on every carrier, d(tuned) = d(Bayes) |
| BS sensitivity of B1 | — | 0 flips in 48 cells | not fragile |

Every prediction the prereg made from the surrogate came out the same way on the carriers. None of them is a ledger
verdict, because the precondition failed.

## 2. What the numbers say about the rule

The rule at Ω = 1 held a median derived weight of 51 to 108 on the six carriers, with the cap of 10⁴ binding on 6 to 15 %
of its steps. On a whitened model with unit noise and batches of ten, the present batch gradient is mostly noise, while the
past gradient near the previous endpoint is small; their length ratio is therefore a noise ratio, and the rule read it as
an instruction to hold the past fifty to a hundred times harder than Bayes does. The consequences are in B5: the rule's
held-out mean squared error was 1.5 to 4.2 times the Bayes arm's on every carrier, and in B7: the fixed weight at the
rule's own median w diverged on three carriers, so the rule survived at that weight only because its step is bounded. The
cross-verification's finding, that the rule's one distinct property is the bound, holds here in its unflattering form:
the bound kept a bad point.

The Ω plateau of every classification study is absent in the posterior metric (B6: exactly one grid point within a
step of the best, and the best Ω below 1 on every carrier). The exact model behaves as a model should (B4: the tuned λ
is 1, the Bayes arm's held-out error matches the exact posterior predictive to the third decimal).

## 3. Sensitivity table

B1 (the rule at Ω = 1, c = 1, against the Bayes arm) over cap ∈ {10, 100, 1e4} × smooth ∈ {0.8, 0.9, 0.98}, eight cells per
carrier: 0 flips in 48 (`runs/bayes1/score.txt`, the "sensitivity" line per carrier). Not fragile.

## 4. Exclusions and reproducibility

No rows dropped for NaN on any carrier; four carriers subsampled to 5000 rows (seed 777) as pre-registered. Fifteen
non-finite runs per carrier, all of them fixed weights λ ∈ {4, 8, 16} at c = 16 (the stability edge, scored d = ∞ and
counted). One arm per carrier rerun twice through the frozen scorer: byte-identical on 6/6 (`runs/bayes1/rerun_check.txt`);
the score reproduces byte for byte.

## 5. What a surrogate would have done

The gate (`prereg/bayes1/gate_BAYES.txt`) predicted the outcome of every row before the data: the Bayes decoy does not
fire the B1 statistic and a non-Bayes weight does; the rule sits far from the posterior (7.17); miscalibrated Bayes is
closer than the rule in both directions; the invariance does not survive mini-batch noise. The carriers repeated the
pattern with larger margins. What the surrogate did not predict is the precondition's failure: the synthetic stream
converged to 0.0650 under the same optimiser budget, and the carriers did not. A BAYES-1b would set the epoch budget from
the measured convergence of the Bayes arm on each carrier, before scoring, as a registered rule; it is a new prereg on a
later day, and it would carry EQ-B beside the rule.
