# Declaration: PRED70, predictive tests of CRR on 70 new systems

**Status.**
- **The request.** Owner request, prompt-log entry 234 (2026-09-29): "Run new predictive tests on 70 new systems please".
- **When it was pushed.** This file and `declared.py` are pushed before any model for these systems exists.
- **What is fixed.** For each of the 70 systems:
  - CRR's prediction Q (its decisive quantity and threshold);
  - the CRR ingredient;
  - the null replacement;
  - the domain's own model or theorem (H0);
  - the investigator's forecast of the outcome.
- **What it is.** Tests in each domain's own mathematics, on standard synthetic models with the parameters named in
  `declared.py`. They sit at rung R4 (declared before a synthetic run). There is no real data and no ledger row, so this
  is a note, not evidence (R8).
- **The route to real data.** A row that comes out ADDS becomes a candidate for a real-data lab (`labs/README.md`, the
  entry rule), under its own pre-registration.

## The systems

The 70 systems are not in the retrodictive bank (`labs/checks/bank.txt`, 166 rows). They come in 14 batches of five:

| batch | systems |
|---|---|
| P01 | oscillators with their own events |
| P02 | stick-slip and relaxation |
| P03 | remembered state and stability thresholds |
| P04 | learning and cognition |
| P05 | continual learning and optimisation |
| P06 | physics |
| P07 | chemistry and cell biology |
| P08 | ecology and evolution |
| P09 | economics and finance |
| P10 | social systems |
| P11 | physiology |
| P12 | climate and earth |
| P13 | engineering and control |
| P14 | agents, AI and information |

## How each prediction is scored

Each row runs through the SYNTHESIS harness (`src/crr/synthesis/harness.py`). The label is computed from the numbers,
never written (R15):
- **T-G:** the ingredient against its null;
- **T-N:** against the domain's theorem;
- **T-C:** the check of Q in the domain's own mathematics.

Two things are read off each row:

1. **Did CRR's prediction hold?** The T-C check is True: Q held in the domain's own model, whatever its novelty. It fails
   when the check is False. The redundant labels are included: a Q that the domain already contains, or that the null
   also meets, still held.
2. **Was the investigator's forecast of the outcome right?** The forecasts are in `declared.py`, written now.

**Fixed CRR knobs.** P3 is not fixed by CRR, so the declaration fixes it:
- A6's memory weight is q = 0.5 per occasion. The grid q ∈ {0.25, 0.5, 0.75} is printed as a sensitivity and never
  chooses the verdict.
- H-L5 margins use the instrument's paired bootstrap (n_boot 2000, seed 0).
- "More than 1 %" is the harness's TOL_G.

**Rules for the implementation.** Each batch is written by a research agent from this file.
- **Fixed:** the implementer may choose model details that `declared.py` leaves open (step sizes, horizons, seeds). It
  must NOT change Q, the null, H0, the direction, a threshold or a parameter that `declared.py` names.
- **If a Q cannot be computed as written,** the row is UNSTATED and says what was tried. A Q is never rephrased so that it
  can be computed.
- **Every deviation is printed in the row and logged** (AGENT_LOG).
- **Runs are deterministic,** each batch under about two minutes, and every batch is run twice and compared with `cmp`.

**The harness gate.** `theory/retrodictions/synthesis.txt` rows 1 and 2 must read ADDS and WRONG. They are read by the
tally, not re-run.

## The investigator's forecast (written now, from the bank's lessons)

| outcome | forecast count |
|---|---|
| REDUNDANT-DOMAIN | 34 |
| WRONG | 18 |
| ADDS | 9 |
| REDUNDANT-IG | 5 |
| INTERNAL | 3 |
| PROPOSES | 1 |

These counts are those of `declared.py` (printed by `python3 -c "import declared"` in the tally).

**The reasons, from the bank's lessons:**
- H-L5 on clock-regular carriers fails.
- A6 memory is mostly an exponential moving average that the domain already has.
- Threshold shifts from memory have a known direction.
- The antipodal cut rarely beats a domain's own trigger.

**A pre-written expectation.** Fewer than a third of the predictions will hold AND carry CRR content (ADDS). Most that
hold will be redundant.

## Outputs

- `Predictions70/batches/pred_NN.py` and a pinned `.txt` for NN = 01…14;
- `Predictions70/checks/tally.py` and `tally.txt`: per row, the outcome, whether Q held, and the forecast hit; the totals;
  a comparison with the bank;
- `Predictions70/PREDICTIONS70.md`, written after the tally, quoting it.
