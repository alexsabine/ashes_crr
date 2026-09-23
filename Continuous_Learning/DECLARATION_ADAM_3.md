# Declaration — is the rule's SGD advantage a tuning-grid artefact? (committed and pushed before the first full run)

Owner request, prompt-log entry 104. The anchor is the push timestamp of the commit that adds this file. The script is
`Continuous_Learning/checks/adam_checks_3.py`.

## Why this follow-up exists

`adam_checks_2.txt` [B3] shows the rule's weight settling between two values. At c = 16 the median derived w is 0.0480
without smoothing and 0.0446 with it. Below that sits the grid-tuned λ (0.03 at c = 16), and above it the edge (0.0786).
The tuning grid used everywhere in these checks has no point between 0.03 and 0.1. So the rule's "advantage" over the
tuned fixed weight at c = 16 (A4, B1) may be the rule finding a weight that the coarse grid could not represent.

## Tests and expectations

- **B4. The reduction test** (CLAUDE.md §6, the logic of EQ-1). A fixed weight equal to the rule's median derived w is
  run and compared with the rule.
  - Criterion: the label is REDUCES if the two totals are within 10 %.
  - Expected: REDUCES at every scale. On a stationary quadratic the rule's weight settles, and a settled weight is a
    constant.
- **B5. A fine tuning grid.** 60 log-spaced weights from 1e-4 to 3 are run, and the rule's total is divided by the best
  of them.
  - Labels: AHEAD below 0.9; TIES within 10 %; BEHIND above 1.1.
  - Expected: TIES or BEHIND at every scale for smoothing 0.9, and TIES for smoothing 0.

## What the outcomes mean

- **If B4 reduces and B5 is not AHEAD anywhere,** the rule does not beat a well-tuned fixed weight on this model under
  any optimiser tested. Its value is then a tuning-free property:
  - it finds a stable weight without a search;
  - that weight lies below the edge at any scale.

  That is the claim the write-up may make, and nothing stronger. It is also what a patent's technical effect would have
  to rest on: a reduced tuning cost, not better accuracy.
- **If B5 reads AHEAD somewhere,** the rule does something that no single constant does on this model, and the write-up
  says where.
