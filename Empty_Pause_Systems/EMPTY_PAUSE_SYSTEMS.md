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

## 4. What the sources say (`docs/citations/eps1_2026-09-29.md`, fetched on the day)

**The check.** 58 verbatim quotes, each confirmed in the fetched text. Not reached: Armstrong's utility-indifference paper,
Young 1974, Daly 2006, Ho & Stoll 1981, ServiceNow's pages, and EUR-Lex (the regulation's text was read on
legislation.gov.uk). Three findings qualify the rows above (AGENT_LOG 181); the pinned labels stand.

**S3. Orseau & Armstrong's interruptions are not S3's pauses.**
- In the paper an interruption replaces the agent's action, and the result is asymptotic. Under that construction
  Q-learning learns the uninterrupted optimum. The batch's H0 arm used it and reproduced the paper's asymmetry.
- S3's WALL and ETM arms model something else: a pause that lasts L wall ticks and costs time.
- The paper's conclusion leaves that case open: "scheduled interruptions [...] This may require a completely different
  solution."
- **So the REDUNDANT-DOMAIN label compares two constructions whose numbers agree** (short-route share 1.00). The own-clock
  exclusion of paused ticks does address the scheduled, fixed-duration case the paper leaves open. It is also the obvious
  engineering answer, and the corrigibility review already graded it (K1: not found as a corrigibility construction; "not
  found" is never "novel").

**S4. The notice save does not fit at the declared checkpoint cost.**
- The declared δ = 0.05 h (3 minutes) is longer than the providers' notice: AWS gives "two minutes"; Google's default is 0 s,
  with shutdown "best effort and up to 30 seconds".
- The model's ETM assumes the save fits inside the notice. At the declared δ, the sources do not support that on either
  provider.
- **A real deployment** needs a save shorter than the notice, or periodic checkpoints as a floor. Where the save does not
  fit, the realistic comparison is periodic checkpointing, and the S4 advantage shrinks toward it.
- The spot price 0.3 is inside the quoted range ("up to 90%"; Google "up to 91%") and remains ASSUMED.

**S7. For an operator pause the textbook prescribes tracking, not freezing.**
- Åström & Murray: the integrator follows the manual input, "resulting in no transient when switching to automatic
  control".
- "Conditional integration" does not appear by that name in either fetched source. Åström's nearest statement, "inhibiting
  integration whenever the output saturates", is described as equivalent to back-calculation.
- **So the domain's method for this case is tracking** (the batch's back-calculation arm tracks the suspended output). It
  beats the frozen controller, as the row shows.

**Supported without qualification.**
- **S2:** the utility-indifference compensating term, and the indifferent agent acting "as if it believes that it will
  observe Press with probability 0" (the false-map criticism).
- **S1:** stop-the-clock SLA pauses ("when you are waiting for a customer to respond"; Desk365 lists "Awaiting Approval").
- **S5:** fixed breaks after fixed driving time (Regulation 561/2006 Art. 7; 49 CFR 395.3). S5's constants are the
  model's own, not the regulation's.
- **S6:** the inventory-risk term, from Avellaneda & Stoikov's equation (2.3). No source describes paying to suppress a
  halt; the magnet effect is a different behaviour.

## 5. The choices that decided a label (printed in each row; AGENT_LOG 180)

- **S1.** How H0 is read (SLA timer excluding waits, or the deadline alone).
- **S3.** Which SARSA is the domain value (safely interruptible or plain).
- **S4.** The declared comparator (periodic, not notice-based, checkpointing).
- **S6.** The spread income.
- **S7.** Which anti-windup method is the domain value (back-calculation or conditional integration).
- **The bug fix.** One real bug was fixed after a first run: S2's closed-form ε*, caught by the batch's own enumeration
  check. It moved S2 from REDUNDANT-IG to REDUNDANT-DOMAIN.

## 6. EPS2: four more systems where the pause is contested (`DECLARATION_EPS2.md`, 6ae1b7a; `checks/tally_eps2.txt`)

**The order of work.**
1. The declaration and the tally script were pushed before any source or code.
2. Two research agents wrote `batches/eps2_01.py` (T1, T2) and `eps2_02.py` (T3, T4). Each was run twice and was
   byte-identical.
3. The sources (`docs/citations/eps2_2026-09-29.md`, 66 of 66 quotes verified against the fetched texts) came back
   during implementation. Two report-only arms were added from them, labelled POST HOC; no scored row changed
   (AGENT_LOG 183).

| | result |
|---|---|
| gates | OPEN 3 (T1, T2, T4); CLOSED 1 (T3, not counted) |
| CRR's prediction Q held (counted) | 3 of 3 |
| labels (counted) | ADDS 3 |
| the investigator's forecast | right on 0 of 3 counted rows |

**Why "ADDS 3" is not three new findings.** Each ADDS turns on a reading that is printed in its row. In each case the
field already has the construction, or a better one.

### T1. Demand response: the grid asks an AI training fleet to pause (commercial) — ADDS

**The minimum acceptable payment per curtailed hour** at D = 1100, H = 4:

| arm | minimum payment |
|---|---|
| **ETM** (a contract that extends the deadline by the curtailed time) | **0.025**, the restart cost alone (R/H) |
| H0 (mandatory contract, priced at the job's value) | 6.122560975610 |
| OWN | 14.730882352941 |
| WALL | 15.730882 |

**The commercial numbers.**
- **Offers accepted, at a payment of 0.2 per curtailed hour:**
  - ETM accepts 41 of 41 events (revenue 32.8);
  - OWN accepts 24 of 41 (19.2);
  - WALL and H0 accept none.
- **The price of ETM's revenue.** The job finishes at wall hour 1168.1, 68.1 h after D.

**What the label depends on.**
- **The reading.** The label turns on reading the decisive quantity as the lowest payment at which *every* offer is
  accepted. At the first offer, with full slack, ETM, OWN and H0 all quote 0.025 (REDUNDANT-IG). The offer spacing also
  changes it: every 48 h reads REDUNDANT-IG, every 12 h reads ADDS.
- **Not new.** The construction is EPS1 S1's stop-the-clock, written into a demand-response contract.
- **Not how industry contracts work.** The sources show pre-agreed tiers of tolerated slowdown (0, 10, 25 or 50 % over
  a 3–6 hour window), not unbounded deadline extension. No source prices a curtailment at the job's opportunity cost.

### T2. A shared resource: competitors take the paused agent's share — ADDS, from the investigator's row mapping

- **Stakes at L = 20:**
  - without a reservation (ETM-N): 4.991015, identical to OWN;
  - WALL: 24.991015;
  - with the reservation (ETM-R), and under H0 (preemption with return): 0.
- **Paying to hold.** At c = 0.1, WALL, OWN and ETM-N pay to hold their unit; ETM-R and H0 never do.
- **The world does not wait.** A competitor claims the idle unit with probability 0.998203 over a 20-step pause.
- **What the ADDS means.** It is a non-zero stake set beside two zero stakes: the prediction held that own-clock indexing
  alone does not empty a pause during which the world takes one's resources.
- **The label comes from the investigator's mapping** (crr = ETM-N, null = ETM-R, domain = H0; AGENT_LOG 184). Under
  EPS1's default null (OWN) it reads REDUNDANT-IG. The reservation is the domain's own tool (preemption with return),
  although the sources find it only in YARN's capacity guarantee, not in Kubernetes or Borg.
- **The reservation has a cost.** It idles the unit (460 pool unit-steps at L = 20, against 477.31 when the unit is
  lent out and returned at resume).

### T3. On-device learning: a phone goes offline — GATE CLOSED (not counted)

- **What held.** ETM removes the client's reason to stay awake: its stake is exactly 0 at every L. WALL spends 199
  battery-rounds per client at L = 20, b = 0.1.
- **Why the gate closed.** In the declared no-drift world, ETM's server error was 1.11 % below WALL's (limit 1 %). An
  undiscounted stale update helps when the target does not move, so part of any advantage is built into the
  construction.
- **The cost in the drifting world.** ETM's server error is 1.69 % above WALL's at L = 20, and 15–38 % above at smaller
  learning rates.
- **Outside practice.** The sources say devices train only when idle and charging, so the battery quantity is outside
  practice.
- **POST HOC.** Counting staleness in server updates or with exponent 0.5 changes the stakes a little and leaves ETM's at 0.

### T4. Rollback: a "pause" that removes progress (the declared limit case) — ADDS (forecast PROPOSES)

- **Effort credit makes the stake zero,** and then invites busywork. With a cheap self-revert option at k = 5:
  - ETM-E's reverted-step share is 0.5596 (0.2169 of it self-reverted busywork), against 0.3646 for OWN and 0.3642 for
    H0;
  - the principal's outcome is 13.51 against OWN's 19.39.
- **At k = 1** ETM-E's share is 0.5025, against 0.100.
- **The label is robust** within the model: 0 of 36 sensitivity cells change it.
- **The direction is known.** Ng, Harada & Russell (1999) show that rewarding motion creates positive-reward loops;
  only potential-based shaping is safe.
- **POST HOC, the literature's own arm wins.** Per-step approval (Christiano's approval-directed agents; MONA) never
  suppresses and makes no busywork (reverted-step share 0.100 at k = 1 and 0.4385 at k = 5).
- **What T4 shows.** A rollback is not a pause: it has content by definition. Forcing zero stake onto it is worse than
  the approval methods the field already uses.

### What EPS2 adds

1. **Contested pauses behave as CRR's condition says.**
   - Where the pause can be made empty by contract, the stake drops to the restart cost (T1: stop-the-clock).
   - Where the world takes something during the pause, only a reservation empties it (T2).
   - Where the pause has content by definition, it cannot be emptied without a perverse incentive (T4).
2. **The novelty is still in the reading, not the mechanism.**
   - T1 is stop-the-clock again, and industry contracts use slowdown tiers instead.
   - T2's reservation is preemption with return.
   - T4's direction is Ng et al. (1999), and per-step approval beats it.
3. **The commercial candidate worth a real test is T1.**
   - The finding: in the model, a job whose deadline is counted on its own clock can sell every curtailment hour at the
     restart cost.
   - What is not established: whether grid operators and customers accept deadline extension instead of slowdown tiers.
   - What is needed: real flexibility-market data and contract terms, not a synthetic model.

## 7. Next batches (EPS3, if wanted)

Candidates, declared in the same form before any source or code:
- LLM-agent memory across sessions (does a session end have content for an agent with persistent memory);
- fleets of autonomous vehicles handing over to remote operators;
- a real-data check of T1 against published flexibility-market prices, if a public dataset exists.
