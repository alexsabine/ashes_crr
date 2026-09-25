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

## At scale: if the method held on large AI systems (DECLARATION_2, prompt-log entry 198)

**How it was done.** `DECLARATION_2.md` was pushed (536a85e) before `checks/scale_estimate.py`. Every number below is from
`checks/scale_estimate.txt`, which is byte-identical on rerun and CI-checked. The published figures were fetched on the day
and are quoted in `docs/citations/compute_scale_2026-09-25.md`. The IEA's own pages refused the proxy, so its figures are
quoted as reported by Scientific American and Brookings.

**The model.** Energy saved = AI-server electricity × the share spent developing models × the share of that spent sweeping
penalty-like weights × the share of such a sweep SEC removes.
- **AI-server electricity.** 62.25 TWh in 2024; 300.47 TWh in 2030, derived from the IEA's 30 % a year.
- **The share spent developing models:**
  - 0.30 at Meta;
  - 0.40 at Google;
  - 0.7143 in OpenAI's 2024 spend.
- **The share of development spent sweeping penalty-like weights.** ASSUMED, 0.001 to 0.02. No lab publishes it. For
  context, all hyperparameter tuning with μTransfer costs 0.07 of pretraining.
- **The share of such a sweep SEC removes.** 0.8235 to 0.9412, from the pinned SCL3 sweep.

| 2030, conditional on the method holding | saved | share of all data-centre electricity | US homes' yearly use |
|---|---|---|---|
| low | 0.0742 TWh | 0.000079 | 6,879 |
| middle | 0.4743 TWh | 0.000502 | 43,950 |
| high | 4.0399 TWh | 0.004275 | 374,378 |
| beyond the record (every penalty-like weight calibrated, sweep share 0.05) | 10.0998 TWh | 0.010688 | 935,946 |

**What it says.**
1. **Even if SEC holds at scale, it saves a few tenths of a TWh a year in 2030.** The middle case is 0.4743 TWh, or 0.05 % of
   data-centre electricity. The high case is 4.0399 TWh, or 0.43 %.
   - **Why the fraction is small, although SEC removes 94 % of a sweep:** the sweep it removes is a small part of
     development, and development is a minority of AI electricity.
   - **Why the band is wide:** the unmeasured sweep share spans a factor of 20 and dominates it.
2. **Serving the models is untouched.** That is 180.28 TWh of the 300.47 in the middle case, and the IEA describes the
   growth to 2030 as predominantly inference. No method in this repository makes a served answer cheaper.
3. **The empty cut saves no energy beyond good practice.** Llama 3's planned stops were 47 of 466. That bounds what a cut
   taken before a stop could touch at 0.0101 of pre-training time, and a checkpoint before maintenance already recovers it.
   The cut's value is that nothing is silently lost, and that a run can be paused whenever the grid is cleanest. That moves
   energy in time; it does not reduce it.
4. **The CRR learner costs energy per run.**
   - It costs 1.8466 × ER, 1.5012 × DER++ and 0.6330 × X-DER, measured before SOTA1.
   - It could save energy only by replacing retraining, which nothing in the record shows.
   - The ceiling for any training-side method is all development: 120.19 TWh in the middle case. It is a ceiling, not a
     prospect.
5. **Weighted by the chance of holding and being adopted**, taking `cl_patent`'s assumed 0.0150, the middle case is 0.007114
   TWh.
