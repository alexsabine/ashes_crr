# OB1-C1 Phase A: the result (GATE CLOSED; C1 stops)

**What was tested** (`C1_DECLARATION.md`, 39e86ce). Adam's moment averages decaying per unit of the learner's own change
(ARC). The comparisons were:
- step-clock Adam (STEP);
- a timing decoy (SHUF): ARC's own decays, shuffled in time;
- the published signals: the gradient norm (KOURK) and hidden-statistics KL (MECTA-M);
- a misalignment restart (ALIGN);
- a reset at the supplied switch (ORACLE).

Output: `checks/c1_phase_a.txt`, pinned; the rerun is byte-identical.

## The gate

| condition | result |
|---|---|
| G-POS: ARC reduces the dip vs STEP | S1 holds (−61.4949, step 2.4106); S2 holds (−3.6288, step 1.0000) |
| G-TIME: ARC beats its own decays shuffled in time | S1 holds (−44.7388, step 3.2672); **S2 FAILS** (−0.8528, step 1.0000) |
| G-DISC: ARC beats both published signals on at least one stream | holds on S2 (KOURK −4.0970, MECTA-M −7.1405); on S1, MECTA-M is ahead of ARC (+8.4452) |
| G-HARM: no harm without switches (S0) | holds (+0.5351) |
| G-FAIL: moment resets move the dip at all | holds (ORACLE − STEP −58.1425 on S1) |

**C1 GATE CLOSED** on G-TIME for S2. C1 stops (R12). Ledger row OB1-C1-A.

## What it shows (synthetic, rung R4; not evidence)

**On S2** (domain-incremental; the cleaner stability-gap setting, since every task has all classes):
- ARC removes the small dip: STEP's avg-SG is 3.06, ARC's −0.57. It beats both published signals.
- But its own decays shuffled in time do nearly as well (0.28).
- So the gain comes from the **distribution** of ARC's decays, not from their **timing**. ARC's median r is below 1,
  so on most steps it keeps longer memory. The timing by own change, which is the CRR-specific part, is not what did the
  work.

**On S1** (class-incremental, no replay), timing matters a great deal: ARC 8.70 against SHUF 53.44 and STEP 70.20.
- But the published hidden-statistics signal does better: MECTA-M 0.26, with final accuracy 43.96 against ARC's 27.35.
- And S1's metric is a design defect of the declaration. Without replay, old-class accuracy never recovers, so the
  30-step minimum measures how fast forgetting begins, not a transient stability gap. The literature's stability gap
  (h1-B6) is measured under joint training, with replay of all past data.
- A corrected S1 would be a new declaration. It could not reopen this gate, because G-TIME fails on S2, which the
  correction would not change.

## What it means for CRR

- **The published signal won where timing mattered.** Indexing the optimiser by the learner's own change did move the
  dip, and in S1 its timing mattered. But there, a published signal (MECTA-style statistics) did better.
- **Timing added nothing where the setting was cleanest.** In S2 the timing added nothing beyond the average change in
  memory length.
- **On this test,** CRR's point of disagreement (own change, not the step clock) does not beat the frontier's signals.
