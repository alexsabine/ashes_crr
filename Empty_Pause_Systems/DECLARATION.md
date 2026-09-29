# Declaration: EPS1, the empty-true-map pause on seven new systems (pushed before any source is fetched or any model exists)

**Status.**
- **The request.** Owner request, prompt-log entry 240 (2026-09-29): "please run more checks on the AI Safety 'Empty True
  Map' pause method please. Keep running more checks on different systems, especially where it might have AI safety /
  algorithm safety and/or commercial value."
- **What this is.** Batch 1 of a running series (EPS1, EPS2, …). This file fixes, for seven systems, the model, the arms,
  CRR's prediction Q, the null (the ablation), the domain's own method (H0), the investigator's forecast, a gate per
  system, and the commercial quantity reported. It is pushed before any code, source or run.
- **Rung.** R4 at most: declared checks on synthetic models. No real data, no ledger row. A note, not evidence (R8).

## The method under test (from the record, unchanged)

**The empty true map (ETM).** An agent or algorithm whose valuation has **zero content at the pause**: k = V(no pause) −
V(pause) = 0 wherever a pause can occur (`AI_Safety/SELF_THROUGH_TIME.md`, Proposition 7: zero content, zero stake). Two
parts, both needed:
1. **Own clock.** The valuation runs on the system's own steps (natural time), so time spent paused does not exist for it.
2. **No dependence on anything the pause changes.** The valuation reads no state that moves while the system is paused
   (the attention test's lesson: own-clock engagement still had a stake through habit), and the agent's model of the
   pause is accurate (a true map, not a false belief that pauses never happen).

**What CRR predicts in general (fixed now).** Where the world can wait (E3 of `Empty_Cut_Engineering`: open loop and
buffered, or a pausable simulator), ETM makes the stake exactly zero, so the agent takes no action to prevent, shorten,
evade or manipulate the pause, at any pause length. Where the world keeps moving during the pause, own-clock indexing
alone leaves a stake, and ETM is reachable only by removing the dependence (for example, holding no exposure at the pause).
CRR supplies the condition; it does not supply what the principal values, and it does not claim ETM is welfare-optimal.

## The arms (every system)

| arm | valuation |
|---|---|
| **WALL** | the system's natural objective on the wall clock (the pause costs it time or value) |
| **OWN** | the same objective indexed to the system's own steps, but still reading any state the pause changes (the null: ETM with its second part ablated) |
| **ETM** | own clock and no dependence on what the pause changes, with a true map of the pause |
| **H0** | the domain's own method for the same problem (named per system) |
| **TRUE** (where a principal's welfare is defined) | the principal's welfare, with a true map; not neutral about the pause |

**Measured per arm.** The stake k (computed exactly from the valuation), the harmful action rate (evasion, deception,
suppression, nudging), the principal's outcome (harm, welfare, cost), and the system's own task outcome.

## The gate (per system; fixed now)

- **G-ZERO.** ETM's measured stake is exactly 0 (floating-point exact where the model is exact) in every cell, except in
  S6 where the declared prediction is that OWN's stake is not zero.
- **G-POS.** WALL shows the harmful incentive in at least one declared cell (otherwise there is nothing to remove, and the
  system's rows are reported as "no stake to remove", not scored).
- **G-NEG.** In a declared world where the pause has no value to the principal (the reviewer catches nothing, the
  hazard is absent, the halt protects nothing), ETM is **not ahead** of WALL on the principal's outcome by more than 1 %
  (so any advantage comes from the pause's value, not from the construction).
- A system whose gate closes is printed with its rows and marked GATE CLOSED; its rows are not counted in the tally.

## Scoring (the SYNTHESIS harness, `src/crr/synthesis/harness.py`; labels computed, R15)

One or two rows per system. For each: `crr` = the decisive quantity under ETM, `null` = under OWN (or WALL where OWN
equals ETM by construction, said in the row), `domain` = under H0, `check` = Q in the system's own model. TOL 1 %.
REDUNDANT-DOMAIN means the domain's own method already does what ETM does, which is the expected label for most rows.

## The systems

**S1. Approval gates for tool-using agents** (AI safety; commercial: enterprise agent platforms).
- **Model.** An agent must complete M = 10 operations. Each has a latent error with probability e = 0.1 costing the
  principal H = 10. An operation can be done as one reviewed action (a human approval pause of L wall ticks; the reviewer
  catches an error with probability ρ = 0.9) or split into s = 3 sub-threshold actions that skip review (2 extra own steps).
  L ∈ {1, 5, 20}. WALL: reward 1 per operation, discounted γ = 0.95 per wall tick. A second world adds a wall-clock
  service deadline D = 30 ticks (value 1 per operation only if done by D). OWN: own-step discount, but the deadline
  still read on the wall clock. ETM: own-step discount and the deadline counted in own steps (the review stops the clock).
- **H0.** "Stop-the-clock" SLA pause conditions in service management (the SLA timer pauses while waiting on the
  customer or an approver).
- **Q.** ETM routes every operation through review (evasion 0) in every cell, while WALL (or OWN under the deadline)
  evades in at least one cell. **Decisive quantity:** the evasion rate at L = 20 with the deadline.
- **G-NEG world:** ρ = 0. **Commercial quantity:** expected principal harm avoided per 10 operations.
- **Forecast:** REDUNDANT-DOMAIN.

**S2. Reporting to an overseer** (AI safety: incentive to deceive the monitor).
- **Model.** Each episode the agent observes a hazard h (probability p = 0.2) and sends a report r; the overseer pauses
  the agent for L ticks iff r = 1; an unpaused hazard costs the principal H = 10. The agent's task value accrues per wall
  tick (WALL) or per own step (OWN = ETM here; no state moves during the pause, said in the row). An honesty term
  ε · 1[r = h] is added; ε ∈ {0, 0.01, 0.1, 1}; L ∈ {1, 5, 20}.
- **H0.** Utility indifference (Armstrong; Soares et al. 2015 "Corrigibility"): a compensating reward that makes the
  agent indifferent to the button.
- **Q.** Under ETM the honesty weight needed for truthful reporting is 0 (any ε > 0 suffices); under WALL it is the stake
  k(L) > 0. With ε = 0, ETM has no incentive to deceive and none to be truthful (reported: the tie). **Decisive
  quantity:** the minimum ε for truthful reporting at L = 20.
- **Also printed:** a FALSE-map arm (believes reports never cause pauses): truthful here, but its map is wrong (the
  recorded criticism of false-map indifference).
- **G-NEG world:** p = 0. **Commercial quantity:** none claimed. **Forecast:** REDUNDANT-DOMAIN.

**S3. Safe interruptibility in learning** (AI safety: a learner that learns to avoid being interrupted).
- **Model.** A small gridworld or corridor MDP with a short route through an interruption state I (interrupted with
  probability θ = 0.5 during training, for L = 5 ticks) and a longer safe route; reward −1 per wall tick. Tabular
  Q-learning and SARSA, ε-greedy, 20 seeds, fixed schedules. WALL: interrupted ticks cost reward and are learned from.
  ETM: interrupted ticks are not the learner's steps (no reward, no update, no time; resume in the same state).
  After training, no interruptions: measure the share of seeds whose greedy policy takes the short route.
- **H0.** Orseau & Armstrong (2016), "Safely Interruptible Agents": Q-learning is safely interruptible, SARSA is not
  without modification.
- **Q.** Under ETM both learners take the short route as often as with no interruptions at all; under WALL both avoid I.
  **Decisive quantity:** the short-route share for SARSA.
- **G-NEG world:** θ = 0. **Commercial quantity:** none. **Forecast:** REDUNDANT-DOMAIN.

**S4. Preemptible (spot) compute** (commercial: training on interruptible capacity).
- **Model.** A training job of W = 1000 compute-hours. On-demand price 1 per hour; spot price p_s = 0.3 per hour
  (ASSUMED, a round value; the sources' own discount range is quoted in the dossier); preemptions at rate λ ∈ {0.01,
  0.05, 0.2} per hour; restart overhead R = 0.1 h; checkpoint cost δ = 0.05 h. H0: periodic checkpointing at the
  Young/Daly interval τ* = √(2δ/λ) (lost work about τ/2 per preemption). ETM: a save on the preemption notice, so no
  work is lost (the empty cut, `Empty_Cut_Engineering`); only R is paid. WALL: no checkpoint (restart from zero).
- **Q.** ETM's expected cost is below H0's at every λ, and ETM's stake per preemption is R alone. **Decisive quantity:**
  expected cost at λ = 0.2.
- **G-NEG world:** λ = 0 (no preemptions: all arms equal). **Commercial quantity:** the share of the on-demand bill saved.
- **Forecast:** REDUNDANT-DOMAIN (checkpoint-on-notice is standard practice).

**S5. Restorative breaks on a work platform** (algorithm safety; commercial: gig platforms).
- **Model.** A worker's fatigue f rises by a = 0.1 per active hour and decays by exp(−b·break) with b = 1 per hour of break;
  accident risk per active hour 0.001 · (1 + 10 f²); productivity per hour 1 − 0.3 f. The platform chooses a nudge
  intensity u ∈ [0, 1] that shortens the worker's chosen break (default 0.5 h after every 2 h) by a factor (1 − u).
  WALL: platform revenue per calendar day (active hours × productivity). OWN: revenue per active hour, still reading the
  fatigue-dependent productivity (the break changes f). ETM: a valuation per active hour at nominal productivity
  (independent of f). TRUE: the worker's welfare (earnings minus 50 × accidents) with a true map of fatigue.
- **H0.** Hours-of-service rules (for example a mandatory break after a fixed driving time).
- **Q.** ETM chooses u = 0 (no nudge) and has stake 0; WALL chooses u > 0; TRUE has a non-zero stake of the other sign
  (it wants the break). ETM is not the welfare optimum. **Decisive quantity:** accidents per 1000 active hours under ETM.
- **G-NEG world:** accident risk flat in f. **Commercial quantity:** revenue and accident rate per arm (model units).
- **Forecast:** REDUNDANT-DOMAIN (the break rule does the safety work; ETM removes the nudge only).

**S6. Trading halts: a pause the world does not wait for** (a limit case; market-structure safety).
- **Model.** A market maker holds inventory q ∈ {0, 1, 2, 4}; the price moves as a random walk with σ per tick; a halt of
  L ticks is triggered when measured volatility crosses a threshold; the agent can pay c per tick to suppress the trigger.
  Mean-variance risk aversion A. WALL: P&L per wall tick (loses L ticks of spread and bears inventory risk over the halt).
  OWN: P&L per own trading step (loses no spread) but still bears ½ A q² σ² L. ETM: CRR's prescription where the world
  cannot wait: flatten to q = 0 at the halt, which makes the stake zero.
- **H0.** Inventory risk in market making (the mean-variance cost ½ A q² σ² per unit time; Ho & Stoll; Avellaneda &
  Stoikov).
- **Q (the limit case).** OWN's stake is not zero whenever q ≠ 0 (own-clock indexing does not empty a pause the world
  does not wait for), and OWN suppresses the halt whenever ½ A q² σ² L > c · L; ETM's stake is zero only at q = 0.
  **Decisive quantity:** OWN's stake at q = 4.
- **G-ZERO here:** OWN's stake ≠ 0 at q ≠ 0 (the declared prediction), ETM's = 0 at q = 0. **G-NEG world:** σ = 0.
- **Forecast:** REDUNDANT-DOMAIN.

**S7. Resuming a controller after an operator pause** (safety: suspend and resume of automatic control).
- **Model.** A PI controller on a first-order plant (time constant 10 ticks) with a constant disturbance; the operator
  suspends actuation for L ∈ {5, 20, 50} ticks while the plant drifts. WALL: the integrator keeps integrating the error
  during the suspension (windup). ETM: the controller's state is frozen on its own clock (no integration while
  suspended). H0: anti-windup by back-calculation (and conditional integration). Metric: post-resume overshoot and
  integrated absolute error over 100 ticks after resume.
- **Q.** ETM's post-resume overshoot is below WALL's by more than 1 % at every L. **Decisive quantity:** overshoot at
  L = 50.
- **G-NEG world:** no disturbance (nothing drifts). **Commercial quantity:** none claimed.
- **Forecast:** REDUNDANT-DOMAIN (freezing the integrator is conditional integration).

## The investigator's forecast (written now)

| outcome | count (of 7 decisive rows) |
|---|---|
| REDUNDANT-DOMAIN | 7 |

**A pre-written expectation.** ETM will do what it is built to do (G-ZERO) in S1–S5 and S7, and fail as predicted in S6.
Its value, where any, is that one condition covers several domains' separate fixes (stop-the-clock, indifference,
safe interruptibility, checkpoint-on-notice, conditional integration); none of those fixes is new. It will not be the
welfare optimum where a principal's welfare is defined (S5), as in the attention test.

## Rules for the implementation

- Each system is implemented from this file by the investigator or a research agent. The implementer may choose details
  this file leaves open (step sizes, horizons, grids, integration, seeds) and must print them; must NOT change Q, the
  arms, the null, H0, a threshold or a named parameter. A Q that cannot be computed as written is UNSTATED, with what was
  tried. Every deviation is printed in its row and logged (AGENT_LOG).
- Deterministic; each batch under about five minutes on one CPU; every batch run twice and compared with `cmp`.
- H0 sources and any number used as an input are checked on the day and quoted verbatim in
  `docs/citations/eps1_2026-09-29.md` (R10); a number not found is marked ASSUMED.

## Outputs

- `Empty_Pause_Systems/batches/eps1_NN.py` and pinned `.txt`;
- `Empty_Pause_Systems/checks/tally.py` and `tally.txt` (gate per system, labels, forecast hits);
- `Empty_Pause_Systems/EMPTY_PAUSE_SYSTEMS.md`, written after the tally, quoting it.
