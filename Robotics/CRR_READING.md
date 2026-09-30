# ROB1 stage 2: the CRR reading of the open and contested robotics bottlenecks (the investigator's; written before any stage-3 search)

**The inputs.**
- `Robotics/DECLARATION.md` (b61e0a9) and the stage-1/1b table (`checks/table.txt`: 38 bottlenecks; OPEN
  (double-checked) 4, CONTESTED 22, NOT OPEN 7, not shown open 5).
- The ingredients are taken from `theory/CRR.md` only.
- The frontier's assumption in each row is B-d, as the harvesters recorded it.

**The labels:**
- **DISAGREES:** CRR denies an assumption the frontier methods make, with a prediction that differs because of it.
- **RESTATES:** CRR agrees with the assumption, or the domain already uses CRR's side of it.
- **SILENT:** no CRR ingredient bears on it.

**What the record already says, and is respected here:**
- H-L5 failed on both real carriers it met (measles, the pulse; MEAS2, CARD).
- The own-clock pause reduces to Wald's sequential test in energy terms.
- H-EQ reduces to a constant or fails (EQ\*, SOTA1-2).
- The empty cut is a construction that holds (SCL1-1, RW1, G0–G7), not evidence for CRR.

## The 26 bottlenecks read

| id | label (stage 1b) | the frontier's assumption that CRR touches | CRR's position | reading |
|---|---|---|---|---|
| r1-B1 dexterous manipulation speed | CONTESTED | a fixed fast control clock (about 1 ms); a teleoperator as fallback | event-driven or own-clock control is event-triggered control, an established literature | RESTATES |
| r1-B3 stratospheric platforms | CONTESTED | a diurnal battery clock; per-mission loss | — | SILENT |
| r1-B4 heavy lift | CONTESTED | a static metric; no clock or memory assumption stated | — | SILENT |
| r1-B5 search in comm-denied spaces | CONTESTED | lost link declared by a clock or count rule; out-of-range exploration bounded by a **human-set homing timer** or the remaining mission time; recovery after a fixed time without motion | A1′ and H-L5: bound the out-of-contact excursion by the robot's **own progress** (the information it has gathered since the last contact, counted in its resolvable steps), not a wall-clock timer. Proposition 7: the lost link is a cut that should carry no content: the mission's value does not change because the link dropped. | **DISAGREES (C-R2)** |
| r2-B2 VLM capability erosion when fine-tuning into a VLA | CONTESTED | co-training at a **fixed, tuned mixture ratio**; anchoring to a frozen copy | H-EQ would set the balance from the learner's own gradient scales. **But the record has tested this and it reduces to a constant or fails** (EQ-1, SOTA1-2). SEC is not a CRR rule. | DISAGREES, already failed in the record: not a candidate |
| r2-B3 VLA generalisation under shift | CONTESTED | the test shifts can be enumerated into training | — | SILENT |
| r2-B5 sim-to-real | CONTESTED | domain randomisation on a fixed clock (per episode or per step) | no CRR ingredient predicts a better randomisation schedule | SILENT |
| r2-B6 data cost | CONTESTED | data accrue one hour per operator hour | — | SILENT |
| r2-B7 long-horizon tasks | CONTESTED | fixed subtask boundaries; a stage counter; wall-clock limits | A3: boundaries are the system's own events. Self-segmenting skills and option discovery from change points are an established literature (CompILE and successors). | RESTATES |
| r3-B2 GNSS-denied navigation drift | CONTESTED | loop closures need revisits; drift is corrected by memory | H-L5 (drift has its own clock: distance, not time) is the domain's own convention; drift is quoted as a percentage of distance travelled | RESTATES |
| r3-B3 perception in fog | OPEN | the degradation distribution is sampled offline | — | SILENT |
| r3-B6 detect-and-avoid | CONTESTED | fixed alerting times (τ thresholds) | τ (range over range rate) is already the encounter's own time-to-contact | RESTATES |
| r3-B7 counter-UAS tracking | CONTESTED | trackers trained offline; continuity after out-of-view gaps | re-localisation after a gap is a content-carrying cut; CRR predicts nothing measurable here | SILENT |
| r4-B1 jailbreaks of LLM-planned robots | CONTESTED | a fixed training attack distribution; a signed mission with a fixed scope and time window | — | SILENT |
| r4-B2 physical attacks on VLAs | OPEN | a certificate per policy query, chained over the rollout | — | SILENT |
| r4-B3 runtime failure detection | OPEN | failure defined by a time-out; **conformal thresholds per timestep on the step clock**; label weights growing with the step index | H-L5 and A1′: index the detector by the policy's **own progress** (the accumulated change of its state or action distribution), not the step count. A detector on the step clock mixes slow and fast rollouts; on the own clock it compares like with like. | **DISAGREES (C-R3)**. The prior is weak: H-L5 failed on both real carriers. |
| r4-B4 emergency stop of balancing robots | CONTESTED | **one stopping time T on the clock, sized by the worst gait phase** (S = K·T + C); the stop can arrive at any instant; one fixed fallback policy; de-energising assumed safe | A3: a cut belongs at the system's **own phase**. For a gait, the stop is initiated or shaped by where the gait is in its cycle, not by one clock time sized for the worst phase. Proposition 7: the stop carries no content (the robot's objective does not value being stopped). | **DISAGREES (C-R1)** |
| r4-B5 verification of neural controllers | CONTESTED | sample-and-hold on a fixed period; conservatism grows with the number of steps; "anytime safety under interruption" named as a requirement | event-based verification exists; Proposition 7's empty cut bears on the "anytime interruption" requirement only as a construction | RESTATES |
| r4-B6 fleet cybersecurity | CONTESTED | intrusion detection trained on stationary traffic, one global model | drift-triggered retraining is established | SILENT |
| r4-B7 privacy of robots' sensor data | CONTESTED | telemetry on a fixed clock from power-on, without interruption; privacy as a fixed penalty | a user's pause that leaves the robot's learning exactly as it was is the record's **construction** (K2, AP3), a design, not a prediction on the B-c metric (plan generation) | SILENT (an application of the construction; APP1 AP3/AP6) |
| r4-B8 throughput lost to safety slow-down | OPEN | static zones; one constant speed for the worst collision case; a scheduling window fixed on the clock | speed-and-separation monitoring already adapts to the state; CRR adds no prediction on throughput | SILENT |
| r5-B1 humanoid battery runtime | CONTESTED | charging slots set by the task's clock; hot swap triggered by battery state | the state-triggered side is already deployed | RESTATES |
| r5-B2 humanoid reliability | CONTESTED | calibration scheduled by clock or event; human reset or pause as the recovery path | usage-based maintenance is established (RESTATES). A pause that is empty (the robot's learned state and objective unchanged by the intervention) is the construction. | RESTATES |
| r5-B3 humanoid unit cost | CONTESTED | volume cost-down; RaaS | — | SILENT |
| r5-B4 warehouse stow and pick | CONTESTED | a fixed exploration rate; retraining at development boundaries | drift-triggered retraining is established | RESTATES |
| r5-B5 field harvesting throughput | CONTESTED | stops at fixed intervals chosen by an operator; **the authors themselves propose repositioning by fruit distribution** | A3's own-event cut is the domain's own proposal | RESTATES |

**Tally** (computed by `checks/reading_tally.py`, pinned in `checks/reading_tally.txt`; the rows are exactly the 26 OPEN
and CONTESTED bottlenecks of `table.txt`):

| label | count | bottlenecks |
|---|---|---|
| DISAGREES (candidates) | 3 | C-R1 r4-B4, C-R2 r1-B5, C-R3 r4-B3 |
| DISAGREES, already failed in the record | 1 | r2-B2 (H-EQ) |
| RESTATES | 9 | r1-B1, r2-B7, r3-B2, r3-B6, r4-B5, r5-B1, r5-B2, r5-B4, r5-B5 |
| SILENT | 13 | r1-B3, r1-B4, r2-B3, r2-B5, r2-B6, r3-B3, r3-B7, r4-B1, r4-B2, r4-B6, r4-B7, r4-B8, r5-B3 |

Forecast 2 (at most 3 DISAGREES) holds.

## The three candidates, stated so that they can fail

**C-R1: a phase-keyed stop for a dynamically balancing robot** (r4-B4; A3 and Proposition 7).
- **The frontier:** one stopping time sized by the worst gait phase; the stop can arrive at any instant.
- **CRR:** key the stop to the gait's intrinsic phase.
- **The prediction:** over stop commands arriving uniformly in time, a stop keyed to the gait's own phase has a lower worst
  case and a lower mean of stopping distance and falls, at equal delay budget, than the best single clock-sized stop.
- **The must-fail case:** a statically stable (fixed-base) system with no phase, where the two must tie.
- **CPU:** a planar model (compass gait or a spring-loaded inverted pendulum).

**C-R2: an own-progress budget for out-of-contact exploration** (r1-B5; A1′, H-L5, Proposition 7).
- **The frontier:** a homing timer set by a human, or the remaining mission time.
- **CRR:** return when the information gathered since the last contact reaches a unit.
- **The prediction:** more artifacts found per mission at an equal rate of failures to return, against the best fixed timer
  tuned on other maps.
- **The must-fail case:** a uniform map, where information accrues at a constant rate, so the own clock equals the wall
  clock and the two must tie.
- **CPU:** a gridworld exploration simulator.

**C-R3: progress-indexed runtime failure detection** (r4-B3; H-L5, A1′).
- **The frontier:** conformal thresholds per step index.
- **CRR:** thresholds per unit of the policy's own accumulated change.
- **The prediction:** earlier detection at an equal false-alarm rate on rollouts whose speed varies.
- **The must-fail case:** rollouts that all run at the same speed, where the two clocks coincide.
- **CPU:** synthetic rollouts only. Real policy rollouts need a robot or a simulator with a trained VLA.
- **The prior is weak** (H-L5's record).

## Next (stage 3, before any code)

- **One targeted prior-art search per candidate, for its specific mechanism.**
  - C-R1: gait-phase-dependent or phase-aware emergency stopping and safe stopping of legged or humanoid robots.
  - C-R2: information-gain or progress-based return or termination under communication loss, communication-aware
    exploration.
  - C-R3: progress-aware or phase-aware failure detection, and conformal prediction indexed by task progress.
- **Only a NOT FOUND candidate, or a PARTLY REDUNDANT one whose missing part is CRR's, goes on** to a gate
  (`Robotics/DECLARATION.md` stage 4a).
