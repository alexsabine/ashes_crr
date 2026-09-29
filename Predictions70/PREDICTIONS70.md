# PRED70: CRR's predictions on 70 new systems

**Status.**
- **The request.** Owner request, prompt-log entry 234 (2026-09-29).
- **The order of work.**
  1. `DECLARATION.md` and `declared.py` were pushed at 8397478 before any model existed. They fixed, for each of 70
     systems not in the retrodictive bank: CRR's prediction Q, the ingredient, the null, the domain's own model (H0) and the
     investigator's forecast.
  2. Seven research agents wrote the 14 batches (`batches/pred_01.py` … `pred_14.py`) from that file. Every batch was run
     twice and was byte-identical (`cmp`).
  3. `checks/tally.py` was written before any batch output existed. Its output is `checks/tally.txt`.
- **What it is.** Tests in each domain's own mathematics, on standard synthetic models. That is rung R4, not real data.
  It is a note, not evidence (R8).

## The result (`checks/tally.txt`)

| | count (of 70) |
|---|---|
| CRR's prediction Q held in the domain's own model | 35 |
| Q failed | 33 |
| Q not computable | 2 |

**By outcome (the harness label, computed from the numbers):**

| outcome | computed | forecast |
|---|---|---|
| ADDS | 14 | 9 |
| REDUNDANT-IG | 19 | 5 |
| REDUNDANT-DOMAIN | 16 | 34 |
| WRONG | 18 | 18 |
| INTERNAL | 2 | 3 |
| UNSTATED | 1 | 0 |
| PROPOSES | 0 | 1 |

**The forecast.** The investigator's forecast of the outcome was right on 33 of 70 (0.4714). The declared expectation
("fewer than a third hold AND carry CRR content") holds: 14 < 23.33.

**What held was mostly redundant.** Of the 35 predictions that held, 20 were redundant: either the null does as well
(REDUNDANT-IG) or the domain already has the result (REDUNDANT-DOMAIN).

## The ADDS rows, read strictly

**The 7 H-L5 ADDS rows** are "the arc between the system's own events is more regular than the clock":
- P01-1 Hodgkin-Huxley; P01-2 Morris-Lecar; P01-3 Stuart-Landau; P01-5 Lorenz;
- P02-3 dripping faucet; P07-5 Dupont calcium; P11-5 the menstrual-cycle model.

**None of them survives H-L5's own amplitude control.**
- **The control.** `theory/CRR.md`'s H-L5 and the instrument's `regularity()` carry a control: the arc must also be more
  regular than the amplitude of each cycle.
- **The error.** `declared.py` wrote Q as the bare arc-against-clock inequality and left the control out. That is the
  investigator's error in the declaration.
- **What the rows show.** The printed rows show the amplitude at least as regular as the arc in all 7 (the tally's
  post hoc "amp" column: FAIL on 7 of 7).
- **The cause.** Where a spike or cycle has a nearly fixed height, the arc per cycle is nearly fixed by arithmetic. It is
  the waveform's regularity, not a clock of its own.
- **Across all H-L5 rows.** Of the 16, the column reads FAIL on 11 (the 7 ADDS rows and 4 others), OPEN on 1, and is
  absent on 4.

**The 7 A6 ADDS rows survive the strict reading:**

| row | system | what the remembered state changed |
|---|---|---|
| P03-4 | SIS epidemic, contacts on remembered prevalence | damped oscillations appear (a complex leading eigenvalue) |
| P08-1 | Rosenzweig-MacArthur | the paradox-of-enrichment Hopf point falls (K_H 2.3333 → 1.8750) |
| P09-2 | Kaldor business cycle | the limit cycle shrinks away (cycle amplitude 0.6544 → about 0) |
| P10-1 | DeGroot opinion averaging | consensus reached 54.8 % slower, same value |
| P10-5 | Daley-Kendall rumour | the never-hearing fraction falls from 0.2032 to 0.1495 |
| P14-3 | recommender filter bubble | topic diversity collapses more slowly (halving time ratio 1.1613) |
| P14-4 | federated averaging with stragglers | lower final loss than FedAvg (0.101337 vs 0.122854) |

**Their standing.**
- **P14-4 depends on the form of FedAvgM.** It is ADDS against FedAvgM at the paper's fixed server rate
  (`docs/citations/pred70_2026-09-29.md`: Hsu et al. v1, quoted). The A6 server is FedAvgM at a smaller effective rate,
  inside the family the paper tunes.
- **The bank's lesson applies.** In the retrodictive bank, 6 of the 7 A6 ADDS candidates checked in the literature
  turned out "direction known": memory kernels shifting a threshold is standard in each field.
- **So these seven are candidates.** They are not claims until a literature check of each one is done (the protocol of
  `theory/retrodictions/synthesis_batches/literature_check.py`).

## Where the predictions failed (WRONG 18)

- **The antipodal cut against a domain's own trigger** (A3 and H-CUT: WRONG 6).
  - These were the thermostat, sleep onset, the thermohaline collapse, the circadian phase-response crossover, the
    Brownian ratchet and SGD restarts.
  - In each the domain's own trigger (a threshold, a saddle-node, a response curve) sets the event, not half a turn of a
    phase.
- **H-L5 on clock-regular carriers** (WRONG 4: Red Queen, breathing, glacial cycles, the two-block slider).
- **A6 memory in the wrong direction or against a better model** (WRONG 7).
  - P03-5: Goodwin's cycle is destabilised, not stabilised.
  - P05-5: the Kalman filter is better.
  - P10-2: A6 is not the Hawkes intensity.
  - P10-4: traffic capacity falls.
  - P11-1: the glucose nadir moves.
  - P11-4: A6 is not the pharmacokinetic accumulation.
  - P14-1: the bandit's regret is worse.
- **Path against endpoint on a convex learner** (P05-1: the endpoint is exact, as the SCOPE lemma says).

## What the 70 add to the picture

- **The pattern repeats the bank's.** CRR's ingredients mostly restate the domain (35 redundant) or fail where the
  domain has a specific mechanism (18 WRONG).
- **Only the remembered-state ingredient (A6) produces surviving candidates.** Its candidates have the same shape as the
  bank's: a bounded memory shifts a stability threshold or a speed.
- **H-L5 did not survive its own control on any of the 70.** The antipodal cut did not beat a domain's trigger on any
  system where the two could be told apart.

**Model choices that decided a label.** Each is printed in its row, and the tally flags 22 deviations. Among the labels
that turn on a model detail:
- P01-3 (the kind of noise);
- P02-1 (whether the slip is the cut);
- P02-4 (the recharge noise);
- P02-5 (which clock midpoint);
- P03-2 (P/δ);
- P04-2 (the integration step);
- P05-4 (patience and horizon);
- P11-1 (the occasion length);
- P11-4 (the dosing interval);
- P12-1 (quasi-static against finite ramps);
- P12-5 (the flood rate);
- P14-4 (the FedAvgM form).

These rows are fragile by construction and are read as such.

**Next, if wanted:**
- the literature check of the seven A6 ADDS candidates;
- for any that survive, a lab under `labs/README.md`'s entry rule, with real data.
