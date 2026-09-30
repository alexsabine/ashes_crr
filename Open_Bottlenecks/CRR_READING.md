# OB1 stage 2: where CRR agrees with the frontier, and where it disagrees (written before any stage-3 search)

**Input.** The 19 bottlenecks that `checks/table.txt` shows OPEN, and the frontier's assumptions recorded there (B-d).

**The rule** (`DECLARATION.md` stage 2):
- **DISAGREES:** CRR denies an assumption the frontier methods make, and predicts differently because of it.
- **RESTATES:** CRR agrees with the frontier's assumption or restates its fix.
- **SILENT:** no CRR ingredient bears on it.

The readings are the investigator's, written on 2026-09-30 after the harvest and before any targeted prior-art search.

## An honest prior (the record, before reading)

- CRR's one repeated point of disagreement with the field is **the clock**. CRR indexes an occasion by its own change (the
  arc, H-L5; the path, D6/H-T1), where the field indexes by steps, epochs, counts or calendar time.
- The record on that point is poor:
  - H-L5 failed on both real carriers tested (MEAS2 0/17; CARD 1/29);
  - H-T1 failed (T1X2-1, 5/5: the old-probe endpoint predicts forgetting and the path does not beat it).
- So the prior that "index by own change" beats "index by clock" is low. The readings below still name it where it applies,
  because the owner asked for the proper test, and because in a learner the arc per step jumps at a distribution shift.
  That is a different use from H-L5's regularity claim.

## The readings

| bottleneck | the frontier's assumption (quoted in the table) | CRR ingredient | reading |
|---|---|---|---|
| h1-B1 gap to joint, representation learned | consolidation anchored to the previous optimum, applied "every I steps"; boundaries given | D6/H-L5 (own clock), A3 (own cut) | **DISAGREES** on "every I steps" (same mechanism as C3) |
| h1-B2 cold-start exemplar-free gap | statistics remapped at supplied transitions; covariances fixed | A3 | RESTATES (tested in RQM/RRM; the transport is published) |
| h1-B3 drift of stored statistics | drift estimated from current data at transitions | A3 + A6 | RESTATES (RRM; HopDC arXiv 2602.00144) |
| h1-B4 online single-pass gap | fixed learning rate and batch; recalibrate hyperparameters under shift | H-EQ / D6 | RESTATES (Ω = 1 reduces to a constant, EQX to SEC5; recalibration without future data is the realistic-tuning line, h4-B2, which the sweep shows closed) |
| h1-B5 long sequences | one adapter per task at given boundaries; compensation cost grows | A1′ | SILENT (CRR fixes no capacity rule) |
| h1-B6 stability gap at switches | **optimiser timescales fixed on the step clock**; the fix adds a fast timescale driven by the loss at transitions | D6/H-L5 (own clock) | **DISAGREES**: candidate C1 |
| h2-B1 sequential editing | running normalisation indexed by cumulative edit count | D6 | DISAGREES in principle, but not CPU-testable at benchmark scale: set aside (named) |
| h2-B2 knowledge drift | calendar timestamps (retrieval); per-batch updates | A7, H-L5 | SILENT in practice (a retrieval reference; not CPU-testable) |
| h2-B3 TRACE | known boundaries; per-task epochs fixed in advance; tuned once | A3, A7 | RESTATES (boundaries, as h4-B1); not CPU-testable |
| h2-B4 multimodal instruction tuning | experts = tasks, fixed in advance | A3 | not CPU-testable; set aside |
| h2-B5 routing | routing as classification of a supplied task label | A3 | not CPU-testable; set aside |
| h2-B6 agent stages | stages supplied from outside, uniform merging | A3 | not CPU-testable; set aside |
| h3-B1 plasticity under switches | **resets on a fixed clock; the boundary supplied (Oracle)**; regulariser fixed because non-stationarity is not measured | A3 (own cut) + D6 (own change) | **DISAGREES**: candidate C2 |
| h3-B2 streaming RL | step size fixed in parameter units | D6 (step in own-change units) | RESTATES (a step fixed in output or KL units is Intentional Updates, arXiv 2604.19033, and the trust-region line) |
| h3-B3 AgarCL | hyperparameters from shorter horizons | A7 | not CPU-testable; set aside |
| h3-B4 warm-start gap | chunk boundaries given; fixed iterations per chunk | A6 (regeneration from the settled past) | RESTATES (warm-starting is A6; shrink-perturb and DASH are the field's fixes) |
| h4-B1 boundary-free streams | **shift detected over a fixed batch window or a fixed per-expert sample budget (count-indexed)** | A3 + D6 | **DISAGREES**: candidate C3 (same mechanism as h1-B1's consolidation trigger) |
| h4-B4 on-device configuration | threshold decaying with an experience index; decisions at boundaries | D6 | DISAGREES in principle; its benchmark is embedded GPU memory: set aside (named) |
| h4-B5 federated edge | compute counted in gradient steps per round | D6 | DISAGREES in principle; not CPU-testable (1000+ GPU-hours): set aside |

**Counts:**
- DISAGREES 7. C1, C2 and C3 are carried forward; h1-B1 is folded into C3; h2-B1, h4-B4 and h4-B5 are set aside as not
  CPU-testable.
- RESTATES 6 (h1-B2, h1-B3, h1-B4, h2-B3, h3-B2, h3-B4).
- SILENT 2 (h1-B5, h2-B2).
- Set aside as not CPU-testable, with no disagreement read: 4 (h2-B4, h2-B5, h2-B6, h3-B3).
- The declaration forecast "at most 3" DISAGREES. Counted in principle, that forecast is wrong (7). Counted as candidates
  carried forward, it holds (3). Both are printed.

## The three candidates carried to stage 3

All three are the same CRR point, applied in three places: **index the learner's timescale, trigger or budget by its own
accumulated change (the arc since the last cut), not by the step count.** The arc of a step is √(2·KL) between successive
predictive distributions on a fixed probe set, which the instrument implements as `path_length`.

**C1: arc-clocked optimiser timescales (h1-B6, the stability gap).**
- **Frontier:** momentum and Adam averages decay per step. NGM-SGD adds a fast timescale driven by the loss at
  transitions.
- **CRR:** decay per unit of the learner's own arc, β_t = β^(a_t / ā), where a_t is the step's arc and ā a running mean.
- **Prediction:** at a switch the arc per step jumps, so the stale averages are forgotten faster without being told of
  the switch.
  - On the named protocol, the dip (avg-SG) is smaller than with step-clock averages, and not larger than NGM-SGD's.
  - It is equal to step-clock averages on a stream without switches.
  - It is worse where arc spikes are uninformative (injected noise spikes).

**C2: arc-triggered refresh (h3-B1, plasticity under switches).**
- **Frontier:** resets on a fixed clock, or at a supplied boundary (the Oracle).
- **CRR:** refresh (reset or shrink-perturb) when the accumulated arc since the last refresh crosses a unit.
- **Prediction:** on a continual control chain, the arc-triggered refresh is closer to the Oracle's aggregate than a
  clock-scheduled refresh with the same number of refreshes, without boundary information.

**C3: arc-triggered consolidation in boundary-free streams (h4-B1, h1-B1).**
- **Frontier:** consolidation or freezing at supplied boundaries, "every I steps", or at shifts detected over a fixed
  batch window or sample budget.
- **CRR:** consolidate (freeze, snapshot or anchor) when the arc since the last consolidation crosses a unit.
- **Prediction:** on a boundary-free (Si-Blurry-type) stream, arc-triggered consolidation is closer to the
  clear-boundary result than count-triggered consolidation, at an equal number of consolidations.

## What stage 3 must search (the specific mechanisms)

- **C1:** optimiser moment decay or reset driven by the step's parameter or function change, KL, gradient norm or loss;
  "momentum reset at task switch"; "adaptive β"; "stability gap optimiser".
- **C2:** plasticity resets triggered by detected change, KL, drift or a divergence budget, rather than on a schedule.
- **C3:** task-free consolidation triggered by accumulated change: KL, Fisher, parameter distance or loss-surprise budgets.
  Leads already in the harvest: FiUni (Fisher-subspace self-detected boundaries); Seo et al. (Fisher-information compute
  allocation); Aljundi et al. 2019 (loss-plateau task-free).

**Forecast (from the declaration, unchanged):** at least one of the three is published. The most likely is C3: task-free
continual learning with self-detected shifts is a literature. C1 is the most likely to survive.

## Erratum (appended after stage 3; the readings above are unchanged)

- **C1's description of the frontier comparator is wrong.** It says NGM-SGD's fast timescale is "driven by the loss at
  transitions". The fetched v3 text (arXiv 2507.14056; `docs/citations/ob1_s3_c1_2026-09-30.md`) says the driver is the
  Shannon entropy of the readout. The candidate and its prediction are unchanged; the comparator is corrected in the
  stage-4 declaration.
- **The stage-3 grades** (`checks/grade_s3.txt`): C1, C2 and C3 are each PARTLY REDUNDANT, with 0 states. In each case the
  missing part is the learner's own accumulated change (the arc) as the index. That is the part CRR predicts, so all
  three may go on.
- **The declaration's forecasts.**
  - Forecast 3, "at least one published", is not held as REDUNDANT. It holds in substance: every component is published.
  - Forecast 4, "zero or one survives", is not held: three go on.
