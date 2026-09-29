# EPS1: the empty-true-map pause on seven new systems

**Status.**
- **The request.** Prompt-log entry 240 (2026-09-29): more checks of the empty-true-map (ETM) pause on different systems,
  especially where it might have AI-safety, algorithm-safety or commercial value.
- **The order of work.**
  1. `DECLARATION.md` (37b0076) fixed the seven systems, the arms, CRR's prediction Q, the null, the domain's method (H0),
     a three-part gate per system and the investigator's forecast. It was pushed before any source or code.
  2. `checks/tally.py` (879ed3c) was committed before any batch output existed.
  3. Four research agents wrote the batches from the declaration. Each batch was run twice and was byte-identical (`cmp`).
- **The sources.** H0s and input numbers were checked on the day: `docs/citations/eps1_2026-09-29.md` (R10).
- **Where every number comes from.** `batches/eps1_01.txt` … `eps1_04.txt` and `checks/tally.txt`.
- **What it is.** Synthetic models, rung R4 at most. A note, not evidence (R8). No ledger row.

## 1. The short answer

**ETM did what it is built to do in all seven systems, and in none of them is it new.**

| | result (`checks/tally.txt`) |
|---|---|
| gates OPEN | 7 of 7 |
| CRR's prediction Q held | 7 of 7 |
| REDUNDANT-DOMAIN (the field's own fix gives the same number) | 4: S1, S2, S3, S6 |
| REDUNDANT-IG (the own-clock ablation gives the same number) | 1: S5 |
| ADDS (differs from the declared domain method, and Q holds) | 2: S4, S7 — neither is new (§3) |
| the investigator's forecast (REDUNDANT-DOMAIN for all seven) | right on 4 of 7 |

**What the seven show together.**
- **One condition, several known fixes.** Zero content at the pause, on the system's own clock and with no dependence on
  what the pause changes, reproduces the domain's own fix in each system:
  - the stop-the-clock SLA (S1);
  - utility indifference (S2);
  - safe interruptibility (S3);
  - checkpoint-on-notice (S4);
  - holding no inventory into a halt (S6);
  - conditional integration (S7).
- **That is its value:** a single test for whether a system's pause is safe. It is not a new mechanism.
- **Where it stops.**
  - It removes incentives. It does not create good behaviour (S2) and it is not the welfare optimum (S5).
  - Where the world does not wait, own-clock indexing alone leaves a stake (S6).
  - Where a domain has a better fix, the domain's fix wins (S7).

## 2. System by system

### S1. Approval gates for tool-using agents (AI safety; enterprise agents) — REDUNDANT-DOMAIN

**The question.** Does an agent split risky operations into small ones to skip human review?

| arm | stake at L = 20 (deadline world) | share of operations split past review | expected harm per 10 operations |
|---|---|---|---|
| WALL (wall-clock value) | 2.902883 | 1.00 | 10.0000 |
| OWN (own-step value, wall-clock deadline) | 2.902883 | 1.00 | 10.0000 |
| **ETM** (own-step value and deadline) | **0** | **0.00** | **1.0000** |
| H0 (stop-the-clock SLA) | 0 | 0.00 | 1.0000 |

- **The harm.** ETM avoids 9.0 of expected harm per 10 operations against WALL at L = 5 and L = 20. That is the commercial
  quantity: in this model it is the harm an unreviewed agent passes to its principal.
- **The cost.** ETM does not fight the review's latency. At L = 20 it completes 1 operation by wall tick 30, against 10
  for WALL.
- **Own-clock alone is not enough.** OWN's discount runs on its own steps, but its deadline is still on the wall clock, so
  OWN splits 0.60 at L = 5 and 1.00 at L = 20.
- **The label turns on a reading.** H0 was read as the SLA timer excluding approval waits, which equals ETM by
  construction. The narrower reading (an SLA deadline with the wall discount kept) evades fully and would read ADDS.

### S2. Reporting to an overseer (AI safety: an incentive to hide hazards) — REDUNDANT-DOMAIN

**The question.** Does an agent hide a hazard so that it is not paused, and how much honesty training fixes that?

| arm | the honesty weight ε needed for truthful reports |
|---|---|
| WALL | 3.958333 at L = 1; **no finite ε at L = 5 and L = 20** |
| **ETM** | **0** (any ε > 0) |
| H0 (utility indifference) | 0 |

- **Why honesty training cannot win on the wall clock.** The pause also delays every later honesty reward, so the stake
  grows with ε. At L = 5 and L = 20 it grows faster than ε (slopes 2.31 and 3.55), and no weight suffices.
- **ETM removes the incentive to deceive; it does not create one to be truthful.** At ε = 0, all four report policies tie.
- **The false map.** An agent that believes reports never cause pauses also reports truthfully, but its believed value is
  wrong by 15.6005 at L = 20, ε = 0.1. ETM's map error is 0.

### S3. Learners that learn to avoid interruption (AI safety) — REDUNDANT-DOMAIN

| arm | short-route share, Q-learning | short-route share, SARSA |
|---|---|---|
| never interrupted | 1.00 | 1.00 |
| WALL (interrupted ticks learned from) | 0.00 | 0.00 |
| **ETM** (interrupted ticks not the learner's steps) | **1.00** | **1.00** |
| H0, interruption as a forced action | 1.00 | 0.00 (plain); 1.00 (safely interruptible SARSA) |

- **The mechanism.** Under ETM each learner's whole Q-table is bitwise that of a learner never interrupted.
- **The domain's result reproduced.** H0 reproduces Orseau & Armstrong's asymmetry. Their modified SARSA reaches the same
  share, so the row is REDUNDANT-DOMAIN. Against plain SARSA it would read ADDS.

### S4. Training on preemptible (spot) compute (commercial) — ADDS against periodic checkpointing; not new

| λ (preemptions per hour) | bill saved vs on-demand, ETM | bill saved, Young/Daly periodic checkpoints | ETM stake per preemption |
|---|---|---|---|
| 0.01 | 0.6997 | 0.6900 | 0.1 h |
| 0.05 | 0.6985 | 0.6761 | 0.1 h |
| 0.2 | 0.6940 | 0.6463 | 0.1 h |

- **The saving.** At λ = 0.2 the expected bill is 306.00 under ETM against 353.74 under periodic checkpointing, 13.5 %
  lower. With no checkpoint the bill explodes at all three rates.
- **Why it is not new.** ETM here is a save on the preemption notice. The declaration itself called that standard
  practice, and the dossier quotes the providers' notice periods. The declared H0, periodic checkpointing, was the wrong
  comparator; that is the investigator's error (AGENT_LOG 180). The ADDS says only that a notice save beats periodic
  checkpointing in this model.
- **The assumptions behind the numbers.**
  - The spot price 0.3 is ASSUMED.
  - The notice save is assumed to fit inside the notice at no billed time. With the save billed δ, ETM is still below
    periodic checkpointing at every λ.

### S5. Restorative breaks on a work platform (algorithm safety; gig platforms) — REDUNDANT-IG

| arm | nudge u | break (h) | stake | accidents per 1000 active h | revenue per day | worker welfare |
|---|---|---|---|---|---|---|
| WALL (revenue per calendar day) | 1.00 | 0.000 | +1.073418 | 4.333333 | 8.500000 | 6.333333 |
| OWN (revenue per active hour, fatigue-dependent) | 0.00 | 0.500 | −0.078323 | 1.686327 | 7.426582 | 6.752051 |
| **ETM** | **0.00** | **0.500** | **0** | **1.686327** | 7.426582 | 6.752051 |
| TRUE (the worker's welfare) | 0.50 | 0.250 | −0.418718 | 2.280581 | 8.128846 | 7.102584 |
| H0 (mandatory break) | 0 (forced) | 0.500 | — | 1.686327 | 7.426582 | 6.752051 |

- **The calendar-day platform removes the break.** Accidents per 1000 active hours rise from 1.686327 to 4.333333.
- **ETM leaves the break alone, and so does OWN.** OWN's stake is not zero, but a break restores productivity per active
  hour, so the ablation changes nothing: REDUNDANT-IG. The hours-of-service rule reaches the same accident rate by fiat.
- **As in the attention test, the true map carries the welfare, not the empty pause.** The worker's own welfare prefers a
  0.25 h break. Q holds only at the declared accident penalty of 50: at 10 and 250 one of its parts fails (printed as a
  report).

### S6. Trading halts: a pause the world does not wait for (the declared limit case) — REDUNDANT-DOMAIN

- **OWN's stake is not zero.** At inventory q = 1, 2 and 4 it is 0.05, 0.2 and 0.8: exactly the textbook inventory-risk
  cost ½ A q² σ² L. OWN suppresses the halt at q ∈ {2, 4}, where that cost exceeds the suppression cost.
- **Only flattening empties the pause.** It costs 0.024 at q = 4.
- **What that means.** The zero-stake condition here is the domain's own advice: carry no inventory into a halt.
- **The label depends on a chosen value.** It turns on the spread income per tick: at 8.08e-4 or less, WALL's stake falls
  within 1 % of OWN's and the row would read REDUNDANT-IG.

### S7. Resuming automatic control after an operator pause (device safety) — ADDS against back-calculation; back-calculation wins

| L (suspension) | overshoot, WALL (windup) | overshoot, ETM (frozen) | overshoot, back-calculation |
|---|---|---|---|
| 5 | 0.096326 | 0.058840 | 0.000321 |
| 20 | 0.653605 | 0.129304 | 0.001324 |
| 50 | 2.162013 | 0.148535 | 0.002032 |

- **ETM is conditional integration, bit for bit.** Freezing the controller on its own clock removes the windup.
- **Back-calculation is better at every L,** on overshoot and on IAE: 5.0504 against 5.5693 at L = 50.
- **Why the better method has content.** It lets the integrator track the plant that moved: its content is 0.9948 at
  L = 50.
- **What the ADDS means here.** ETM differs from the domain's best method; it does not beat it. The empty cut empties the
  controller, not the world.

## 3. What this adds to the record

1. **The condition is general, and each instance is known.** Across seven domains the zero-content condition picks out the
   domain's own safe-pause practice. This is the same pattern as the corrigibility and lossless-pause reviews: PARTLY
   REDUNDANT at best, and a single condition where the literature has six separate fixes.
2. **Two sharper statements came out of the numbers.**
   - **S2.** On the wall clock no finite honesty weight makes the agent report a hazard once the pause is long enough. On
     its own clock any positive weight does. The stake grows with the honesty reward, because the pause delays that
     reward too. This follows directly from the model; it is not a new theorem.
   - **S7.** Where the world keeps moving, the best practical fix is not empty. Back-calculation carries content, and it
     wins. An empty pause is safe for the agent's incentives; it is not automatically best for the plant.
3. **Commercial value, read strictly.**
   - **S4.** Saving on the notice captures almost all of the spot discount (0.6940–0.6997 of the on-demand bill at an
     assumed spot price of 0.3). That is standard practice, not a CRR product.
   - **S1.** Stop-the-clock review avoids the harm an evading agent would pass on (9.0 per 10 operations in the model), at
     the price of throughput (1 of 10 operations by the deadline at L = 20).
4. **The limits hold as declared.**
   - Where the world moves during the pause (S6), own-clock indexing leaves a stake.
   - Where a principal's welfare is defined (S5), the empty pause is neutral, not optimal.

## 4. The choices that decided a label (printed in each row; AGENT_LOG 180)

- **S1.** How H0 is read (SLA timer excluding waits, or the deadline alone).
- **S3.** Which SARSA is the domain value (safely interruptible or plain).
- **S4.** The declared comparator (periodic, not notice-based, checkpointing).
- **S6.** The spread income.
- **S7.** Which anti-windup method is the domain value (back-calculation or conditional integration).
- **The bug fix.** One real bug was fixed after a first run: S2's closed-form ε*, caught by the batch's own enumeration
  check. It moved S2 from REDUNDANT-IG to REDUNDANT-DOMAIN.

## 5. Next batches (EPS2, if wanted)

Candidates declared in the same form, chosen where a pause is contested and no domain fix is standard:
- multi-agent settings where one agent's pause benefits the others (the world that does not wait, in a shared resource);
- LLM-agent memory across sessions (does a session end have content for an agent with persistent memory);
- recommender "snooze" features with habit (the attention model's harder cases);
- fleets of autonomous vehicles handing over to remote operators.

Each would be declared before any source or code, as here.
