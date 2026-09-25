# Declaration: could SEC, and the other recent successes, save compute and energy?

**Status.**
- **The request.** Owner request: prompt-log entry 196.
- **What it is.** A re-analysis of pinned run records. It opens no data and runs no training. It is not a ledger study.
- **When it was pushed.** Written and pushed before `checks/compute_savings.py` exists. Every quantity below is fixed now,
  and the labels are computed by the script (R15).

## Where SEC came from (the record)

SEC came out of the equanimity-rule programme.
- **The Laplace (Bayes) weight was a required baseline** (R7) in the H-EQ studies. EQ3 found it was the tuned λ on only 2
  of 6 carriers.
- **The Adam_SGD audit** showed the equal-pull rule's one real strength is scale-freeness under a units error.
- **SEC corrects the Laplace weight's units** with a per-task secant (SEC1, AGENT_LOG 96).
- **What the ledger labels it.** SCL3's pre-registration records SEC as "the textbook Laplace weight plus a units
  calibration", not a CRR rule. It is a product of the CRR programme; its mathematics is Bayes plus numerical analysis.

## Why compute is proportional to the number of configurations run

In the SEC1 and SCL3 learner (`runs/scl3/frozen/sec1_score.py`), every arm makes the same gradient passes per step and the
same Fisher passes per task:
- a fixed λ;
- the raw Laplace weight;
- SEC, whose calibration reuses the present gradients and parameters the step already computed;
- the rule Ω = 1, which adds two vector norms.

The difference between arms is vector arithmetic. **So the compute of a tuning policy is the number of configurations it
runs, times 5 seeds, times one run's cost. Energy on the same machine is proportional to it.**

## Quantities (from `runs/scl3/results_*.jsonl`: 10 UNSEEN carriers; `runs/sec1/results_*.jsonl`: 12 SEEN carriers, labelled seen)

- **C1, the sweep.**
  - G_c is the number of raw-Fisher λ configurations in carrier c's two-stage grid, counted from the records.
  - A tuned λ costs G_c configurations. SEC, raw Bayes and the rule each cost 1.
  - The share of the sweep saved is 1 − 1/G_c.
- **C2, not behind the tuned λ.** For SEC, raw Bayes and the rule on each carrier: the mean over seeds minus the tuned λ's
  mean, against SCL3's step, max(1, 2 × SE of the tuned arm). The script must reproduce the pinned SCL3-3 counts (SEC 9/10,
  raw Bayes 4/10, the rule 7/10). If it does not, the calculation is wrong and no saving is printed.
- **C3, the R7 alternative: a transferred default λ that costs nothing to find.**
  - For each carrier, the default is the geometric mean of the tuned raw λ on the other carriers (leave one out).
  - It is snapped, in log distance, to the nearest value in this carrier's grid, and that value's recorded accuracy is used.
  - **The saving attributable to SEC** is the set of carriers where SEC is not behind **and** the default is behind. Where
    the default is also not behind, the saving belongs to a default, not to SEC.
- **C4, the policies.** "Run SEC once and accept it" against "run the full sweep":
  - the compute ratio;
  - the number of carriers accepted without an accuracy loss of a step;
  - the accuracy lost on the others (printed per carrier).

  The same is printed for the transferred default and for the rule.
- **C5, the energy statement.** Only as a share of the tuning sweep's compute. No kWh or cost figure is given: the records
  carry no per-run energy, and a figure without a measurement would break R1.
- **C6, the empty cut: rework avoided (report).**
  - With T tasks and a checkpoint only at task boundaries, an interruption at a uniformly random update repeats half a task
    on average: 1/(2T) of a run.
  - A lossless mid-task cut repeats nothing.
  - This is standard checkpointing arithmetic, not a CRR result. The CRR content is the state checklist that makes the
    mid-task cut lossless.
  - Printed for T = 10 (SOTA1's Split-CIFAR-100) and for interruption counts of 1, 5 and 20 per run, as named assumptions.

## What would change the reading

- **If C3 finds the transferred default is not behind wherever SEC is not behind,** the saving is real but belongs to a
  default λ. The report says so.
- **The number printed is a share of hyperparameter-sweep compute, not of training compute.** It is not quoted outside
  the repository (R8): SCL3-3 is PASS-0, not PASS-2.
