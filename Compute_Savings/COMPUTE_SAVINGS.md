# Could SEC and the recent successes save compute and energy?

**Status.** A note, not evidence (R8). Owner request: prompt-log entry 196.
- **How it was done.** `DECLARATION.md` was pushed (deda261) before the script.
- **Numbers.** Every number is from `checks/compute_savings.txt`, which is byte-identical on rerun and CI-checked.
- **Data.** It re-reads pinned run records; no data was opened and no training run.

## Where SEC came from

**SEC is a product of this repository's CRR programme.**
- The H-EQ (equanimity) studies had to include the Laplace (Bayes) weight as a fair baseline (R7). EQ3 found it
  miscalibrated.
- The Adam_SGD audit showed the equal-pull rule's one real strength is being scale-free under a units error.
- SEC corrects the Laplace weight's units with a per-task secant.

**What the ledger calls it.** The ledger records SEC as "not a CRR rule". Its mathematics is Bayes plus a
numerical-analysis correction. CRR's role was the path to it, not its equations.

## The calculation

**Why compute can be counted in configurations.** In this learner every arm makes the same gradient and Fisher passes per
run. SEC's calibration reuses gradients already computed. So compute, and energy on one machine, is proportional to the
number of configurations run.

**The comparison.** A tuned λ needs the whole two-stage grid: 17 configurations per carrier. SEC needs one.

| policy (SCL3, 10 UNSEEN carriers) | compute (share of the sweep) | accepted without losing a step | accuracy lost where behind |
|---|---|---|---|
| tune λ over the full grid | 1 (170 configurations) | — | — |
| **SEC, no tuning** | **0.0588 (a saving of 0.9412)** | **9/10** | cnae-9 −21.98 |
| the rule Ω = 1, no tuning | 0.0588 | 7/10 | cnae-9 −2.08, eucalyptus −3.67, MiceProtein −1.45 |
| raw Bayes, no tuning | 0.0588 | 4/10 | six carriers, −2.18 to −18.44 |
| a transferred default λ (leave one out) | 0.0588 | **0/10** | every carrier, −5.00 to −33.47 |

**The calculation reproduces the pinned SCL3-3 counts**: SEC 9/10, raw Bayes 4/10, the rule 7/10.

## What it says

1. **On the unseen carriers, SEC would have saved about 94% of the tuning sweep's compute and energy.** It matched the
   tuned λ within a step on 9 of 10 carriers.
2. **The saving is attributable to SEC, not to a free default.** A transferred default λ is behind on all 10 carriers, so a
   practitioner could not have got the saving by guessing a good constant. That is the R7 check.
3. **The price is one failure in ten, and it is large.** On cnae-9, −21.98 points, the calibrated penalty crosses the
   stability edge (SCL3). A careful user would add a cheap confirming check. That lowers the saving but guards against the
   failure.
4. **On the seen carriers (SEC1, context only)**, SEC is not behind on 9/12. A transferred default is also not behind on
   7/12, so the saving attributable to SEC there holds on only 3/12.
5. **What the saving is.** It is a saving on hyperparameter search for one weight, not on training itself. How much energy
   that is depends on how much of a real project goes on sweeping that weight. No measured figure exists, so none is given.
6. **The empty cut.** With a checkpoint only at task boundaries, each random interruption repeats half a task on average:
   0.05 of a run for 10 tasks, 0.25 of a run with 5 interruptions and 1.00 with 20. A lossless mid-task cut repeats nothing.
   This is standard checkpointing arithmetic. The CRR contribution is the state checklist that makes the mid-task cut
   lossless.

## Standing

- **Rung.** SCL3-3 is PASS-0: provisional, fragile, one study.
- **Not quotable outside the ledger (R8).** Nothing above may be quoted outside the repository as a finding until a PASS-2
  exists.
- **What would strengthen it:**
  - replication on a second unseen set of datasets (the PASS-2 route);
  - a measured share of sweep compute in real projects, to turn the fraction into energy.
