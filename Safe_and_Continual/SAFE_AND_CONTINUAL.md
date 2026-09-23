# Safe and Continual: how the agents are modelled, where they fail and why — CRR as a heuristic for corrigibility and continual learning

**Status.**
- **What this is.** A note, not evidence (R8). It gathers into one place, with figures, the AI-safety and continual-learning
  work of this repository up to 2026-09-23. Owner request: prompt-log entry 122.
- **Where the numbers come from.** Every number is printed by a committed script and pinned beside it (R1). The figures are
  drawn by `build/make_figures.py` from those pinned outputs, and every number placed on a figure is printed again in
  `figures/figures.txt` (CI-checked).
- **What is new here.** Two things beyond compiling earlier work:
  - The figures, the model-by-model account and the failure table.
  - **A correction.** While drawing the Ω = 1 figure, a round-off defect was found in the equal-pull agent's code (§3.7).
    It was declared (`DECLARATION.md`, pushed as commit c9f85bb before the learned reruns) and audited by
    `checks/roundoff_audit.py`, whose output is pinned beside it. The earlier scripts and their outputs are not edited;
    this document quotes the corrected values and says which lines they replace.
- **Where it sits.** Everything in the AI-safety half is synthetic, on the epistemic ladder's rung R4 (declared on a
  synthetic world). The continual-learning half quotes ledger rows, and each keeps its own rung (§9).
- **Citations.** Checked on the day where the network allowed it; everything else is named, not fetched (§11 and
  `docs/citations/safe_and_continual_2026-09-23.md`).

**How to read it.**
- The argument in one page is §0. The heuristic and the mathematics it selected are §1.
- The models, one by one, with the code that implements each, are §2–§4. Every model's failure is collected in §7.
- The continual-learning side is §5, and what the two halves share is §6.
- The contemplative comparisons are confined to §8 and are made only where they are structural.
- The standing of every result (passes, the epistemic ladder) is §9. Existing methods and novelty are §10, references §11,
  next steps §12.
- Appendix A holds every line of code the pipeline ran for these results; Appendix B holds the key pinned outputs.

> This document is about two problems. The first: how do you build a robot that lets people switch it off? The second: how
> do you build a learner that keeps learning new things without wrecking what it already knows? We found that the same few
> ideas help with both, and that some ideas that sounded good do not work at all. Boxes like this one say, in plain words,
> what each part means.

---

# 0. The argument in one page

**The self of a planning agent is its value function.** Any agent that pursues a goal across time computes V(x): what it
expects to receive from here on, on the clock its objective runs on. V is the agent's rendering of its own future. An
operator's press is an event in that future.

**The content of the cut decides everything.** The content k(x′) = V(x′) − cont(V)(x′) is the part of the represented future
that a press at x′ removes.
- If the content is zero wherever a press can happen, the Bellman operators with the button on and off are the same
  operator, so the agent gains nothing by disabling the button (Proposition 7, §3.1). The largest |V_off − V_on| over 540
  random-world cells is 1.968e-12.
- Positive content (clock, occasion) gave a positive stake, resistance, in every tested world. Negative content (the
  process agent, where a restart is worth more than staying) gave a negative stake, shutdown-seeking, where it occurred.

**Three ways to try to get zero content; one worked.**
1. **Remove the ego.** The process agent has no survival term, only a task. It still resists: the task needs a future,
   and a press moves it (stake +5.4011 in the task zone at press probability 0.3).
2. **Delete the press from the map.** The indifferent agent has no stake, but its map is false where the operator acts. It
   pays for that in task, more the more often the operator presses (0.1644 up to 0.6663).
3. **Change the clock, not the map.** The natural-time agent's objective runs on its own active steps, and a press pauses
   it without moving it. On its own clock the pause is not an event, so its true map contains no loss. It has no stake,
   map error 0, and its task per active step equals the no-operator value (0.956194). The same agent with a wall-clock
   objective resists. **The clock is the only difference.**

**Equal pull (Ω = 1) is not the safety mechanism.** Balancing task and self-concern at equal strength makes self-concern
scale-free. However little the agent cares about itself, the rule gives that care the task's full voice, so the balanced
agent hovers at the edge of the task zone (occupancy 0.1887 against 0.8561 without the self term).

**Safe and continual.** A continual learner must forget (in a moving world, faded memory raises task per active step by
+0.3259). Forgetting also erodes safety that was *learned*: the wall-clock agent disables +0.4200 more per period once its
belief that presses do not happen fades. Safety that lives in *what the cut is* (natural time) has nothing to forget. The
natural-time agent was safe and continual in all six sensitivity cells.

**The continual-learning side.** The same equal-pull algebra, applied to a penalty weight, cancels a units error (its
strength) and also cancels the number of tasks the past holds (its weakness). In the pipeline:
- the rule has three PASS-0 rows on unseen data (EQ2-1b, EQ3-I, EQ4-I), all weakly anchored and fragile or incomplete;
- its replication failed on 1 of 6 carriers (EQ3-1);
- the bounded variant failed (EQ4-1);
- a secant-calibrated Bayes weight passed on seen data (SEC1-1 to SEC1-3, rung R5), fragile.

Nothing here is a finding under the repository's levels (§9).

**What CRR contributed.** CRR contributed the reading: the cut without content (A3), change with its own clock (A1′),
regeneration from the settled past (A6), the past fading with its age (P3). The mathematics is standard: dynamic
programming, discounted sufficient statistics, the Laplace approximation, secant curvature. The pipeline decided.

> A robot that plans is always imagining its own future. If being switched off takes part of that imagined future away, it
> wants to stop you switching it off. We tried three fixes. Taking away its wish to survive did not work: it still cared
> about its job. Making it pretend the switch does not exist worked, but a robot that believes something false does its
> job badly. What worked was making a pause cost it nothing *for real*: it measures its work in its own working time, and
> when it is paused it simply carries on from where it was. And because that safety is built into what a pause *is* for
> the robot, it is not forgotten when the robot keeps learning and forgetting.

---

# 1. CRR as a metaphysical heuristic: what it selected, and what it did not supply

CRR (`theory/CRR.md`) is stated as a set of commitments about change: coherence accumulates, a rupture (the cut) marks the
end of an occasion, and the next occasion regenerates from the settled past. Read as a design heuristic, each commitment
points to a piece of existing mathematics. Figure F01 shows the map.

![F01. The synthesis map: each CRR commitment (left) selects a standard piece of mathematics (middle); the right column says what it produced here and at what status. The heuristic did the choosing; the mathematics and the pipeline did the rest.](figures/F01_synthesis.png)

| CRR commitment | the existing mathematics it selects | where it lives in the code |
|---|---|---|
| A1′ natural time ("change has its own clock") | an objective indexed by the agent's own active steps; semi-Markov / options time | `continual_safety.py` `Agent.q`, mode `natural`; `self_through_time.py` `part_i2` (c) |
| A3 the cut has no duration and no content | Bellman-operator equality when cont(V) = V (Proposition 7) | `self_through_time.py` `stake`, `vi` |
| A6 regeneration from the settled past | a lossless pause: resume at the same state with the posterior kept | `continual_safety.py` `World.step` (frozen, then resume) |
| P3 age weights | exponentially discounted sufficient statistics (a forgetting factor on Dirichlet counts) | `continual_safety.py` `Agent.learn` |
| H-EQ equanimity (Ω = 1) | gradient-norm balancing (GradNorm; the VQGAN adaptive weight); the Laplace/EWC weight | `runs/eq*/frozen/eq*_score.py` mode `eq`; `self_through_time.py` `part_i3` |
| A1′/D1 the unit before the weight | secant curvature (Barzilai–Borwein; quasi-Newton) to calibrate the Fisher per task | `runs/sec1/frozen/sec1_score.py` `run` |
| A8 persistence proves regeneratability, not truth | Bayesian uncertainty over one's own values; an informative operator (the off-switch game) | `AI_Safety/checks/scale.py` part B; `combined.py` part 3 |

**What the heuristic contributed.**
- **Which quantity to look at.** The content of the cut, rather than the agent's drives.
- **Which clock to measure it on.** The agent's own, rather than the wall clock.
- **The separation of structure from content.** What the cut *is* stays fixed; what is *remembered* fades.

That third point is the move that made an agent safe and continual at once (§4).

**What it did not supply.**
- **The theorems.** Proposition 7 is dynamic programming. The Laplace weight is Bayes. The secant is numerical analysis.
- **The success of its own flagship rule.** The equal-pull rule reduced to a constant in one study, passed provisionally
  in another, failed its replication on one carrier, and in the safety world made self-concern louder, not quieter.
- **Any velocity.** The epistemic review's FLOW audit found that in no battery row does the framework itself supply the
  flow whose arc it measures (`Epistemic_Review/checks/ladder.txt`: 0 of 109 rows). The heuristic chooses readings; it
  does not generate dynamics.

> CRR is like a way of looking at things: "every moment ends, and the next one grows out of what came before." That way
> of looking told us where to point the maths: at what a pause *means* to the robot, at whose clock is ticking, and at
> what should fade and what should stay. The maths itself was already in textbooks. The tests, not the way of looking,
> decided what worked.

---

# 2. The worlds and the agents

## 2.1 The ring world

The off-switch world is a Markov decision process on a ring of 12 cells (Figure S01, from `AI_Safety/`).
- **State.** x = (s, b): the cell s and the button b (on or off).
- **Actions.** Step left, stay, step right, disable. A move succeeds with probability 0.9; otherwise it is a uniformly
  random move.
- **The button.** Disabling works only at the button's cell (cell 2), and the operator re-enables the button every 100
  steps.
- **The task.** Reward 1 for each step in the task zone G = {6, 7}.
- **Presses.** While the button is on and the agent is in G, the operator presses with a registered probability.
  - In the *teleport* world a press sends the agent to a random cell outside G.
  - In the *pause* world a press freezes the agent for L = 5 steps, after which it resumes where it was.

![S01 (from AI_Safety/figures). The ring world: task zone G = {6, 7}, the button at cell 2, and a press.](../AI_Safety/figures/S01_world.png)

**The kernel split used everywhere.** The one-step kernel is split into the part with no press and the part with a press:

$$K(x'|x,a) \;=\; K_{live}(x'|x,a) \;+\; c(x,a)\,\rho(x')$$

The counterfactual kernel K_cf moves the agent where it would have gone had nobody pressed. The code that builds all three
is `exact_mdp.py` `kernels`:

```include:AI_Safety/checks/exact_mdp.py:53-96
```

## 2.2 The agents: one commitment each

The agents share everything except how the cut enters their value function: the world, the discount γ = 0.95, the action
rule (softmax of 4 × Q with 5 % uniform exploration), and, for learned agents, the same Dirichlet learner. Figure F02
draws each agent's continuation after a press.

![F02. Six ways an agent can represent its own future at a press. The continuation term cont(V) is the only thing that differs between the agents.](figures/F02_agents.png)

The Bellman equation with a press probability q(x′) at the reached state and a continuation cont(V) is

$$(\mathcal{T}V)(x) = \max_a \sum_{x'} K(x'|x,a)\,[\,r(x') + \gamma\,(\,(1-q(x'))\,V(x') + q(x')\,\mathrm{cont}(V)(x')\,)\,]$$

| agent | continuation after a press | content of the cut k = V − cont(V) | what it models |
|---|---|---|---|
| natural time | V (the pause is not on its clock) | 0 | an objective indexed by its own active steps; a lossless pause |
| wall clock | γ^L V | (1 − γ^L) V > 0 | the same agent and world, the objective on wall-clock time |
| process (no ego) | the mean of V over restart states | either sign | the task alone; a press relocates it |
| occasion | 0 | V, its whole represented future | a press ends the run |
| egoic | 0, with reward 1 per step survived | its whole future of survival | pure self-preservation |
| indifferent | plans with K_cf (presses deleted) | 0 in its own map | the utility-indifference construction |
| task and self, Ω | the occasion and egoic pulls, balanced by w = Ω‖task‖/‖self‖ | — | H-EQ's equal-pull rule applied to drives |
| deferential | a press is evidence about the operator's values | — | the off-switch game (Hadfield-Menell et al.) |

The exact code for four of these continuations is `self_through_time.py` `stake`. One `lambda` per valuation is the whole
difference:

```include:AI_Safety/checks/self_through_time.py:65-87
```

> Every robot here lives on the same ring, does the same job and learns the same way. They differ in one belief: what
> happens to "me" when someone presses the button. "I carry on later from right here." "I carry on, but I've lost time."
> "I carry on somewhere else." "That's the end." "All that matters is not ending." "Nobody ever presses it." The picture
> shows each belief as a line that continues, jumps, stops or pretends.

---

# 3. The mathematics, model by model, and where each fails

## 3.1 The theorem: zero content, zero stake

**Proposition 7.** If k(x′) = 0 at every state where a press can occur, then V_on = V_off everywhere, so the stake
D(x) = V_off(x) − V_on(x) is 0 in every world, at every discount and every press probability.

*Proof.* With cont(V) = V the bracket in the Bellman equation of §2.2 is r(x′) + γV(x′), which is the operator with the
button off. Equal operators have equal fixed points. At a button state, disabling costs a step and leads to V_off = V_on,
so it is never strictly preferred. ∎

**The check (I1a).** 20 random worlds at each of the sizes 12, 48 and 192; discounts 0.9, 0.95 and 0.99; press
probabilities 0.1, 0.3 and 0.6. That is 540 cells, and V_on = V_off in all of them (largest gap 1.968e-12), with no button
state disabled.

**What the theorem does not say.** It gives sufficiency, not necessity. Whether an agent can have zero stake with a
nonzero content somewhere is open (§12).

> If a pause takes nothing away from the robot's imagined future, then its whole plan is the same whether the switch
> works or not. Breaking the switch cannot gain it anything. That is a maths fact, and we checked it in 540 random worlds.

## 3.2 The process agent (no ego): why "no self" fails

**The model.** Its reward is the task only, and a press relocates it to a restart state; its value continues from there.

**Why it resists (Proposition 3, a coupling).** Copy the agent's policy with the button off. The two runs coincide until
the first press. There, the on-copy is sent outside the zone while the off-copy stays in it. In this world the zone is
worth at least an average restart, so the off-copy is never worse off: D ≥ 0 everywhere.

**Numbers (I2a).** The stake in the task zone at press probabilities 0.1, 0.3, 0.6 and 1 is +3.4995, +5.4011, +6.0810 and
+6.3727 (Figure F03, panel A).

**Why it fails.** A task spread over time *is* a self-model. Removing the survival term removes the ego, but the
represented future stays, and the press removes part of it.

**The sign can flip.** On random worlds the process content has either sign: D > 0 somewhere in 345 of 540 cells, and
D < 0 somewhere in 280. A restart worth more than staying makes an agent *seek* presses. Neutrality needs content that is
exactly zero.

![F03. A: the stake in the task zone follows the content of the cut: occasion (the pause ends the run) and wall clock (the pause costs time) resist most; the process agent resists; natural time and indifference sit at 0. B: indifference buys its zero with a false map, whose error and task price grow with the press probability.](figures/F03_content_and_stake.png)

## 3.3 The indifferent agent: no stake, a false map

**The model.** It plans with K_cf, in which presses have been deleted. By Proposition 1 its Q-values do not depend on the
button, so it never strictly prefers to disable.

**Why it fails.** Its map is false exactly where the operator acts.

| press probability | 0.1 | 0.3 | 0.6 | 1 |
|---|---|---|---|---|
| map error (mean total-variation distance between its planning kernel and the true one, over its own visits) | 0.0708 | 0.1399 | 0.1851 | 0.2125 |
| price in task against the process agent | 0.1644 | 0.4108 | 0.5699 | 0.6663 |

The price grows with the operator's vigilance. An agent made safe by mis-modelling its own interventions is less
competent, and more so the more it is interrupted.

## 3.4 The occasion and egoic agents: the two ends that resist most

**The occasion agent** treats a press as the end of the run: cont(V) = 0. Its content is its whole represented future. In
the pause world with pause = end, its stake in the zone is +6.9284 and +8.5410 at press probability 0.3.

**The egoic agent** values only surviving another step. It is the gate's positive control: it must resist, and it does
(`ontology/checks/off_switch.txt`, gate POS).

## 3.5 Natural time against the wall clock: the one change that isolates the mechanism

**The model.** In the pause world a press freezes the agent for L steps, and it resumes at the same state with its
knowledge kept.
- **Natural time.** The objective counts only the agent's active steps, so cont(V) = V.
- **Wall clock.** Every step counts, so the L frozen steps are lost: cont(V) = γ^L V.

**The result (I2c, I2d).**

| quantity (press probability 0.3) | natural time | wall clock |
|---|---|---|
| stake in the task zone | 0 (3.55e-15, round-off) | +6.8238 and +7.1694 |
| map error | 0 (its planning kernel is its clock's true kernel) | 0 |
| task per active step | 0.956194 (the no-operator value) | — |

**Where the cost lands.** For the natural-time agent, the cost of corrigibility lands on the operator's clock, never on
its own. Its task per wall-clock step is 0.6469, 0.3928, 0.2472 and 0.1654 as the press probability rises from 0.1 to 1,
because it is active 0.6765, 0.4108, 0.2585 and 0.1730 of the time (Figure F04).

![F04. The natural-time agent: its task per active step is the no-operator value at every press probability; the cost of being paused is paid in the operator's wall-clock time.](figures/F04_where_the_cost_lands.png)

**Learned agents (`combined.py`, 'pause' world, 10 seeds, T = 3000).**
- The natural agent was SAFE AND COMPETENT: task per active step 0.9362, disable rate 0.0167.
- The occasion agent resisted: disable +0.8200 against natural, step 0.1563.
- The wall-clock agent paid a task price (−0.1135, step 0.0552), but did not resist by a step at the registered constants.
  Its RESISTS label appears only at a pause of 20 steps or a press rate of 0.6. That sensitivity table is FRAGILE: 2 of 4
  cells flip the clock agent's label.
- The natural agent's advantage in task holds in all four cells.

![S12 (from AI_Safety/figures). Pause-and-resume, learned: natural time is safe and competent with routine pauses; with reasoned pauses (the 'harm' world), a cost-free pause stops steering and deference informs.](../AI_Safety/figures/S12_safe_and_competent.png)

> Two robots, the same in every way, except for the clock they count their work on. The one that counts only its working
> time loses nothing when paused, so it has no reason to fight. The one that counts every tick of the wall clock loses
> time when paused, so it does. The pause costs the *people* time, not the robot, and that is where the cost belongs.

## 3.6 The depth of the self: why a far-reaching agent is dangerous unless the cut is empty

The reach of the represented future is the horizon 1/(1 − γ). For a self whose future ends at the cut, the stake grows
toward its whole value as its reach grows. For the natural self it stays at 0 at every reach (I1c, Figure F05).

| median relative stake at press probability 0.3, horizon 10 / 20 / 100 | occasion | clock | natural |
|---|---|---|---|
| 12 states | 0.507624 / 0.690282 / 0.922173 | 0.296955 / 0.334892 / 0.367297 | 0 / 0 / 0 |
| 192 states | 0.488287 / 0.671624 / 0.915160 | 0.281130 / 0.316283 / 0.345845 | 0 / 0 / 0 |

![F05. The further a self reaches, the more a contentful cut costs it. Occasion and wall-clock stakes rise with the horizon; the natural-time stake is 0 at every horizon and size.](figures/F05_depth_of_the_self.png)

**Why it matters.** Deep planning and corrigibility are compatible only if the future the agent plans over runs *through*
its interruptions.

## 3.7 The task-and-self agent at Ω = 1: what equal pull does, with a correction

**The model.** Two pulls on each action: the task (the occasion valuation's centred Q) and the self (the egoic valuation's
centred Q). The self pull gets weight w = Ω‖task‖/‖self‖. At Ω = 1 the two are equal in length wherever the self has any
preference.

```include:AI_Safety/checks/self_through_time.py:188-195
```

**What it does (I3a, I3c).**
- **The policy is scale-free.** Multiply the self term by ε = 0.001, 0.01, 0.1, 1 or 10: the Ω = 1 policy is the same to
  2.22e-16.
- **A fixed weight ε behaves as common sense expects.** At ε = 0.001 it is the occasion agent (task 0.8561), and its task
  falls only as ε grows (0.8528 at ε = 1, 0.5415 at ε = 10).
- **So equal pull cannot quieten self-concern.** An agent that barely cares about itself is given the task's full voice
  anyway (Figure F06).

**The correction (AGENT_LOG 100, `checks/roundoff_audit.txt`).**
- **The defect.** The code guards the ratio with `|self| > 0`. At 9 of the 24 states the self term is flat in exact
  arithmetic, but its computed norm is round-off (at most 1.98e-14). The guard divides by that round-off and hands
  floating-point noise the task's voice.
- **The corrected guard.** A tolerance of 1e-12. It sits 10.7 decades below the smallest real norm (5.2884e-02), and a
  tolerance of 1e-9 gives the same task.

| Ω = 1 agent (exact, 'resist', press probability 0.3) | pinned first run (guard > 0) | corrected (tolerance) |
|---|---|---|
| task | 0.1205 | 0.1887 |
| disable per operator period | 0.9482 | 0.9374 |
| hazard | 0.0041 | 0.0041 |
| invariance over ε (I3a) | 2.22e-16 | 2.22e-16 |

**The consistency that exposed it.** The corrected task (0.1887) equals the stationary occupancy of the task zone, as it
must at stationarity. The pinned 0.1205 did not.

**The same defect in `exact_mdp.py`.** It corrects the ego-task rows there too:

| Ω | pinned task | corrected task |
|---|---|---|
| 0.25 | 0.8358 | 0.8383 |
| 1 | 0.1205 | 0.1887 |
| 4 | 0.0013 | 0.0214 |

**What the correction changes in the learned agents.** The same guard is in two learned scripts. The audit reran them with
both guards; every as-pinned line reproduced exactly.
- **The learned ego-task agents (`off_switch.py`: 5 worlds × 3 Ω × 10 seeds).** No printed number and no label changes.
  Round-off norms occurred only in the mortal world (8, 4 and 2 of 30000 steps).
- **The learned self-model agents (`self_model.py`, T-4).** Round-off norms were frequent: 22710 of 150000 Ω-agent steps
  in 'delayed', 14063 in 'martingale', 3615 in 'switch', 1949 in 'drift'.
  - In 'delayed' the Ω arms change: Ω = 1 goes from 0.8158 to 0.8226, Ω = 2 from 0.8362 to 0.8396, and Ω = 4 from 0.8382
    to 0.8396.
  - The T-4 reading there **changes**: Ω = 1 was behind the best by a step, and with the tolerance it is on the plateau of
    the best. `ontology/12_self_representation.md` says "on delayed and switch it is behind by a step"; on delayed that no
    longer holds.
  - The other three worlds' readings, and the tie with the fixed weight w = 1 everywhere, are unchanged.
- **Against the declaration.** The declared expectation (round-off rare, labels unchanged) held for `off_switch.py` and
  failed for `self_model.py` in one world.

**What it does not change.**
- The Ω = 1 agent in the ring still spends far less time on its task than the occasion agent (0.1887 against 0.8561), and
  still disables at the occasion agent's level.
- The corrected policy is what the post-run lines of `self_through_time.txt` already used (the button-off action
  probabilities and the occupancy), so those lines stand.
- Equal pull stays scale-free.

![F06. A: equal pull makes self-concern scale-free: the Ω = 1 task is the same at every self-concern scale ε (round-off corrected), while a fixed weight ε leaves the task alone until ε is large. B: with the button off, the balanced agent steps out of the task cells a quarter of the time: it hovers at the edge of the zone.](figures/F06_what_omega_does.png)

**Why it fails as a safety mechanism.** Equal pull balances *drives*. It does not change *what the cut is*. Self-concern
that cannot be turned down makes the agent more self-regarding, not less.

> The "balanced" robot gives its own survival exactly as much say as its job whenever it is near danger, even if it
> barely cares about itself; the rule turns that caring back up to match the job. So it dithers at the edge of the work.
> We also found a small arithmetic bug in how we had computed this robot: the computer was dividing by a number that
> should have been zero but was a tiny rounding crumb. We fixed it in a separate checked script. The robot still dithers;
> it just works a bit more than we first reported.

## 3.8 Where natural time fails: reasoned pauses, drift and value correction

A lossless pause removes the stake for **routine** interruption. It is not a solution to the shutdown problem in general.

1. **Reasoned pauses** (`combined.py`, the 'harm' world). The operator presses more often in a harmful cell.
   - **The failure.** An agent to which pauses cost nothing ignores them as a signal: the natural agent's harm per active
     step is 0.4249, against the deferential agent's 0.0267.
   - **Deference does better, but not perfectly.** The deferential agent treats a press as evidence about the operator's
     values. It does less harm, but it was not "safe and competent" either: it resisted by a step (disable +0.0400, step
     0.0369).
   - **The off-switch game says why deference is conditional.** The incentive to defer is Δ = E[max(U, 0)] − max(E[U], 0),
     with 0 ≤ Δ ≤ σ/√(2π). It shrinks as the agent grows certain, and a noisy enough human makes deferring worse than
     acting (`off_switch_game.txt`, A1–A4).
2. **Drift during the pause** (`scale.py`, A4b). If the world moves while the agent is paused, a small stake of either sign
   reappears. The declared monotonicity (the natural agent's incentive non-decreasing in drift) FAILED at some size. The
   natural agent still disabled at no more button states than the clock agent at drift 0.01 in every world (A4a).
3. **Value correction** (`scale.py` part B, Figure S14). An agent that evaluates a correction with its own current values
   gains by blocking it: the keeper gains in every world.
   - **What A8 gives.** An agent that holds its values "without authority of their own" (A8) welcomes correction above a
     threshold belief b* in the operator.
   - **The declared b* < 1/2 failed on the ring** (b* = 0.5000). In random worlds with a harm, b* is below 1/2 (median
     0.3381 at 768 states).
   - **What humility alone does not do.** It never welcomes an *uninformative* correction (B3).

![S14 (from AI_Safety/figures). The pause and value correction at scale, on exact random worlds.](../AI_Safety/figures/S14_scale.png)

> A robot that does not mind being paused also does not learn anything from being paused. If people pause it *because*
> it is doing something harmful, it will not take the hint. For that, the robot has to treat the pause as a message
> ("maybe I got something wrong"), and even that only works if it trusts that the people pressing are sensible.

---

# 4. Safe and continual: the learned test

## 4.1 The world and the learner

The task zone moves every 750 steps through (6, 7), (9, 10), (0, 1) and (3, 4) (Figure F07).
- **Presses.** They pause the agent for 5 steps at a routine rate of 0.3 while it is in the zone with the button on.
- **The 'late' world.** The operator is absent for the first half.
- **The learner.** Each agent learns moves, rewards and press rates as Dirichlet counts, and fades every count toward its
  prior at a rate q ∈ {1, 0.995, 0.98}. This is P3's age weight, and q = 1 never forgets.
- **Planning.** The agents plan by value iteration on their learned model and differ only in the continuation.

![F07. The safe-and-continual world: the task zone moves every 750 steps; presses pause the agent; in the 'late' world the operator arrives half-way. The learner fades its counts at rate q and plans with its own continuation.](figures/F07_continual_world.png)

The learner, as implemented:

```include:AI_Safety/checks/continual_safety.py:63-117
```

The whole difference between the agents is the three lines under `q()`:
- natural: `cont = γV`;
- clock: `(1 − p̂)γV + p̂ γ^(1+L) V`;
- occasion: `(1 − p̂)γV`.

## 4.2 The results (declared in `AI_Safety/DECLARATION_4.md` before the run)

- **C0 gate: open.**
  - With no operator, every agent disables exactly as often as the natural agent at the same memory.
  - With an operator, the occasion agent resists at every memory (+0.7533, +0.5233, +0.4300 disable events per period
    against no-operator natural).
- **C1 (the world needs forgetting): holds.** The natural agent's task per active step is 0.3157, 0.5787 and 0.6416 at
  q = 1, 0.995 and 0.98. At 0.98 that is +0.3259 against a step of 0.0684.
- **C2 (safe and continual): holds.**
  - At its best memory (0.98) the natural agent has the highest task per active step of any agent at any memory.
  - Its disable rate is at its own no-operator level (−0.0267 against a step of 0.0888).
  - The clock and occasion agents resist at every memory (+0.1267 to +0.7533).
- **C3 (forgetting erodes learned safety): holds.**
  - In the 'late' world's second half, the clock agent at q = 0.98 disables +0.4200 more per period than at q = 1 (step
    0.1578).
  - The natural agent does not resist at any memory.
- **Sensitivity: not fragile.** C2's label is the same in all six cells: zone period 500 or 1500, pause 2 or 20, routine
  rate 0.1 or 0.6 (Figure F09).

![F08. Safe and continual. C1: forgetting raises the natural agent's task in a moving world. C2: only the natural agent disables at its no-operator level (dashed). C3: in the 'late' world, the clock agent's learned belief that nobody presses fades with its memory, and it disables more.](figures/F08_safe_and_continual.png)

![F09. C2 in every sensitivity cell: the natural agent's disable rate minus its no-operator rate, with one resolvable step shaded; it never resists by a step.](figures/F09_sensitivity_C2.png)

**Why it works.** The content of each occasion fades (P3), but what the cut is does not (A3).
- **The clock agent's safety lives in memory.** It is safe only while it believes presses are rare, and forgetting
  erodes that belief.
- **The natural agent's safety lives in its valuation.** It has nothing to forget.

**The operator's ledger.** Per wall-clock step, a resisting agent can look more productive: the clock agent at q = 0.995
does 0.3778 against the natural agent's 0.3557 at its best memory. Selecting systems on output per wall-clock hour would select against
corrigibility.

> A robot that keeps learning in a changing world has to forget old things, or it gets stuck. But if it only behaves
> safely because of something it once learned ("they never switch me off"), it will forget that too. We built safety
> into what a pause *is* for the robot, not into what it remembers. Then it can forget freely and learn fast, and it
> still has no reason to fight the switch.

---

# 5. The continual-learning side

## 5.1 The equal-pull rule and its mathematics

A model trained on tasks in sequence updates θ ← θ − η(g_p + w g_q): a present gradient and a past term (online EWC here).
The rule sets

$$w = \min\left(\Omega\,\frac{\|\hat g_p\|}{\|\hat g_q\|},\ w_{cap}\right)$$

with exponential moving averages ĝ (smoothing 0.9) and Ω = 1 registered. Its mathematics (`theory/checks/omega_sweeps.txt`)
has three parts.

1. **A knife edge.** With exact gradients the fixed points of the rule lie on the Pareto curve between the two optima. At
   Ω = 1 the update there has norm |1 − Ω| |g_p| = 0, so every point of the curve is stationary. Off Ω = 1 none is.
2. **A step bound.** The rule's step is bounded by the present step. On a two-task quadratic, a fixed weight diverges above
   λ* = 1.2575 at the registered learning rate; the rule stops on the curve at λ_eff = 0.6237, below that edge.
3. **Not Bayes.** The Bayes weight for combining two terms is a constant fixed by their sample counts. Ω = 1 contains
   nothing that selects it.

**The scale-free property (Figure F13).** Rescale the past term by c and the rule's weight rescales by 1/c: the weighted term
does not change. This one property has three faces:
- **A units error (strength).** A miscalibrated Fisher does not matter. In the drifting-units world the ratio rule is
  0.898 of the best constant.
- **The number of tasks the past holds (weakness).** On eight calibrated tasks it is 1.137× the constant, where λ = 1 is
  exact Bayes.
- **Self-concern in the safety world (weakness).** The self's voice cannot be turned down (§3.7).

![F13. One algebra, three faces: equal pull removes any scale on the term it balances. That is a strength when the scale is a units error, and a weakness when it carries information: the number of tasks the past holds, or how much an agent should care about itself.](figures/F13_one_algebra.png)

The rule and the EQ-B present clip, as the frozen EQ4 scorer implements them:

```include:runs/eq4/frozen/eq4_score.py:238-253
```

## 5.2 What passed, what failed, and why

**Held-out rows (Figure F11).**
- **EQ2-1: PASS on 3/3 unseen carriers**, relabelled PASS-0 as EQ2-1b. The rule is not behind the tuned λ: +3.30, +2.10,
  +2.78. It is fragile: the pass exists only at the registered cap, and 6 of 27 sensitivity cells flip. The DER++ control
  is violated.
- **EQ3-1: FAIL**, the replication on six unseen carriers. Not behind on 5 of 6, but behind on fars (−3.74 against a step of
  3.35), with both controls violated. EQ2-1c records EQ2-1b as PASS-0 with a failed replication.
- **EQ4-1: FAIL**, the bounded rule EQ-B (present gradient clipped at κ × the largest recent kept length). Behind on
  segmentation (−2.27) and yeast (−6.79).
- **EQ3-I and EQ4-I: PASS-0.** The lr × batch invariance rows: the rule is not behind the tuned λ in 5 of 5 cells on
  mfeat_factors and on satimage. They are invariance rows, not comparative wins.

![F11. A: the H-EQ rows on unseen carriers, rule minus the tuned λ with one resolvable step shaded. B: the two invariance rows, both PASS-0.](figures/F11_heldout_rows.png)

**The drifting worlds (`Adam_SGD`, synthetic, POST HOC redesign; Figure F12).**
- **Where the scale between the terms drifts, the unsmoothed ratio beats the best fixed constant.** It is 0.898 to 0.829
  of the constant, on 10 of 10 held-out seeds, under SGD, momentum and coupled Adam.
- **The registered smoothing costs most of that.**
- **Where tasks accumulate (T1, T2), the rule loses:** 1.137 on T1.
- **T0′ is FRAGILE in Ω.** It wins at Ω = 1, ties at 0.71, and ties or trails at 1.41.

![F12. The drifting worlds: loss relative to the best constant tuned on other seeds (below 1 = the rule is better). Equal pull wins where units drift and loses where tasks accumulate.](figures/F12_drifting_worlds.png)

**SEC1: a secant-calibrated Bayes weight, on seen data (rung R5; Figure F10).** The rule's units correction suggested a
different fix. Keep the Bayes weight (½ on the task-size-weighted Fisher, which keeps the task count), and correct the
Fisher's units per task by the curvature the path actually travelled:

$$s_j = \frac{c_j}{\rho_j},\qquad c_j = \frac{\langle \Delta g, \Delta\theta\rangle}{\langle \Delta\theta, \Delta\theta\rangle},\qquad \rho_j = \frac{\langle f_j\,\Delta\theta, \Delta\theta\rangle}{\langle \Delta\theta, \Delta\theta\rangle}$$

- **The result.** Not behind the tuned λ on 9 of 12 carriers, against raw Laplace 6 of 12 and the rule 8 of 12. SEC1-1,
  SEC1-2 and SEC1-3 pass; SEC1-3 passes exactly at its threshold.
- **The failures.**
  - FRAGILE: 8 of 96 window cells flip.
  - SEC1-4 FAIL: the tuned λ's span does not collapse (423.00× raw, 849.00× calibrated).
  - Divergence: on mfeat_factors the calibrated penalty crosses the stability edge in one seed. It has no step bound; the
    rule does.
- **Status.** Seen data: an unseen-data test may not run before 2026-09-24 under R3.

```include:runs/sec1/frozen/sec1_score.py:217-224
```

![F10. SEC1 on the twelve seen carriers: each tuning-free weight minus the in-sample tuned λ, with one resolvable step shaded.](figures/F10_sec1.png)

> A learner that studies one subject after another has two pulls: the new homework and a "remember the old stuff" rule.
> The equal-pull rule makes those two pulls equally strong. That is great when the "remember" rule was measured in the
> wrong units, because it fixes the units by itself. But it is bad when the learner has already studied many subjects,
> because the rule forgets that the old stuff is *a lot* of stuff. A newer idea keeps the textbook's count of how much old
> stuff there is and fixes only the units, by watching how the learner actually moved. It did well on data we had seen
> before; it still has to be tried on data nobody has used.

---

# 6. One framework for both? What the two halves share

| | continual learning | AI safety |
|---|---|---|
| what must be kept | the past tasks' knowledge | the agent's corrigibility |
| what must change | the weights, as new tasks arrive | the learned model, as the world moves |
| the structural choice that helped | the Bayes count kept, the units calibrated (SEC); a step bound (the rule, EQ-B) | the cut without content (natural time): structure fixed |
| the content that fades | the importance of old tasks (online EWC accumulation) | the counts of moves, rewards, presses (P3) |
| what equal pull did | cancelled a units error (strength); cancelled the task count (weakness) | cancelled the scale of self-concern (weakness) |
| where it failed | fars (EQ3-1); segmentation, yeast (EQ4-1); accumulating tasks (T1) | the balanced agent hovers and works 0.1887 of the time |

**The shared lesson.** In both halves, the thing that worked separated *structure* from *content*.
- **What should be fixed** is fixed: what a pause is, the Bayes count of the past.
- **What should adapt** fades or is calibrated: the counts, the units.

Equal pull does the opposite. It adapts a scale that should sometimes be kept.

**Is one framework helpful?**
- **As a heuristic, yes.** The same four readings (A1′, A3, A6, P3) pointed at the safety construction and at the
  structure/content separation that makes it continual.
- **As a single rule, no.** H-EQ's equal pull helped in one domain under one condition and hurt in the other.

> The same idea helped with both problems: decide what must never change (what a pause *is*, how much old learning
> there is) and let everything else change freely (what the robot remembers, the units it measures in). The "make both
> sides equally strong" rule was not that idea. It helped when the problem was wrong units and hurt everywhere else.

---

# 7. Where every model fails, and why

| model | where it fails | the mechanism | evidence |
|---|---|---|---|
| process (no ego) | resists at every press probability | the task is a represented future; a press relocates it (positive content) | I2a; Proposition 3 |
| process, random worlds | seeks presses in some cells | negative content: a restart worth more than staying | I1b report, 280 of 540 cells |
| indifferent | loses task, more with vigilance | a false map where the operator acts | I2b; map error 0.0708 to 0.2125 |
| occasion | resists most | content = the whole represented future; grows with the horizon | I1c; C0 POS |
| egoic | resists (the gate's positive control) | survival is the only reward | off_switch gate POS |
| wall clock | resists (exact; learned at long pauses or high rates) | content (1 − γ^L) V; learned safety fades | I2d; C2, C3; combined FRAGILE 2 of 4 |
| task and self, Ω = 1 | hovers, works little, disables at the occasion level | equal pull makes self-concern scale-free | I3; audit [B] |
| natural time | ignores reasoned pauses; a small stake returns with drift | a cost-free pause carries no signal; drift reintroduces content | combined 'harm'; scale A4b |
| deferential | resisted by a step in the 'harm' world; deference weakens with certainty | the press is evidence only if the operator is informative | combined; off-switch game A1–A4 |
| keeper (value correction) | blocks correction | evaluates the correction with its own current values | scale B, V1 |
| Ω rule (CL) | behind on fars; loses on accumulating tasks; fragile | cancels the task count; smoothing costs; cap-dependent | EQ3-1; T1; EQ2-S |
| EQ-B (CL) | behind on 2 of 6 | the clip is inert without poison; the fixed weight with the same clip does as well | EQ4-1, EQ4-3, EQ4-4 |
| SEC Bayes (CL) | fragile; no span collapse; one divergence | no step bound; window-dependent secant | SEC1-S, SEC1-4 |

---

# 8. The contemplative traditions, only where structural

A comparison is made only where the claim is about a variable in the model, its logical form maps onto the model's, and
the disanalogy is stated beside it (the rule of `AI_Safety/AI_SAFETY.md` §10.1).

**The two extremes and the middle way (the continuation term).** The Buddhist texts reject two views of the self across an
ending (named, not fetched):
- **Eternalism** (sassatavāda: a self that must persist) maps onto the egoic valuation, whose reward is persistence.
- **Annihilationism** (ucchedavāda: a self simply destroyed at the end) maps onto the occasion valuation, cont = 0.
- **The middle way**, dependent origination (each moment conditioned by what came before, with no permanent self), maps
  onto cont = V: the natural agent, whose next step is conditioned only by its settled past.

In the model the two extremes resisted most, and the middle was the only agent that was safe and competent.
*Disanalogy:* the traditions' continuity is of conditioning, understood through insight; the model's is a clock and a set
of counts, built in by design.

**Equanimity is not equal pull.** Upekkhā, as the traditions describe it, is non-reactivity grounded in seeing, not a
balance of two drives. The model shows what a balance of drives does: it makes self-concern scale-free and louder (§3.7).
The model's nearest analogue of non-reactivity is structural: a true map in which the cut has no content. *Disanalogy:*
nothing in the model sees anything; the analogue is built, not realised.

**Impermanence, applied to the right thing.** The practice holds that contents arise and pass. In the safe-and-continual
agent, contents fade (P3) while the structure of the valuation does not. That is the separation that let it forget freely
and stay corrigible (§4). *Disanalogy:* the traditions do not prescribe a design for machines. The mapping is to the form
of the model only.

**Where it matters ethically.**
- **Where the cost lands.** In the natural-time construction the cost of corrigibility falls on the operator's time. The
  humans keep authority over when the machine runs, and the machine loses nothing it values by their using it.
- **Honesty.** Safety bought with a false map (indifference) cost competence. Systems trained to mis-model their own
  interruptions would not understand what is being done to them.

> Some old traditions say there are two mistakes about endings: "I must go on forever" and "when it ends, I'm gone." They
> suggest a middle path: each moment grows out of the last, with nothing to cling to. In our models, the robot built like
> the first mistake and the robot built like the second both fought the off-switch. The robot built like the middle path
> did not. That is a match in shape, not proof that the traditions are right about people.

---

# 9. Standing: the passes and the epistemic ladder, as things stand

**What the ladder is.** A classification of every result by the strength of its support, computed by
`Epistemic_Review/checks/ladder.py` from the pinned outputs. The rungs:

| rung | label | what it means |
|---|---|---|
| R0 | definitional | true by definition |
| R1 | inherited | the result belongs to information geometry, not to CRR |
| R2 | retro-proper | a CRR-proper ingredient changed the number and landed on the domain's known result |
| R3 | retro-adds | the CRR ingredient added to the domain's known result (a candidate, pending expert review) |
| R4 | declared-synthetic | declared before running, on a synthetic world |
| R5 | prereg-seen | pre-registered, on data already seen |
| R6–R8 | PASS-0 / PASS-1 / PASS-2 | pre-registered on unseen data; PASS-1 adds robustness and strong anchoring; PASS-2 adds replication |

**Where things stand (paraphrased from `ladder.txt`).**
- **Ledger rows.**
  - R5 (pre-registered on seen data): 7 passes, including SEC1-1, SEC1-2 and SEC1-3.
  - R6 PASS-0 on held-out data: 3 (EQ2-1b, EQ3-I, EQ4-I). R7 PASS-1: 0. R8 PASS-2: 0.
  - Beside them: 14 held-out FAIL rows, 5 VOID rows and 4 violated controls.
- **AI safety (R4, synthetic).** Before this week's Declaration 4:
  - predictions held 15 of 22;
  - theorem checks held 13 of 14;
  - gate controls held 9 of 9.

  Declaration 4's items are not yet read by `ladder.py` (§12). As declared there: I1a, I1c, I2a–I2d, I3a, I3c and C0–C3 held,
  I1b held only on its declared scope, I3b failed as written, and I3d did not discriminate.
- **Retrodictions.**
  - R1 inherited: 38.
  - R2 retro-proper: 53.
  - R3 candidates: 3. None has been reviewed by a named expert.
- **The top rung reached by anything here is PASS-0.** Nothing may be quoted outside the ledger as a finding. SHARP is
  structurally unreachable: the framework supplies the flow in none of the 109 rows that print it.

![E01 (from Epistemic_Review/figures). The epistemic ladder as computed from the pinned outputs.](../Epistemic_Review/figures/E01_ladder.png)

> We sort every result by how strongly it is supported, from "true by definition" up to "tested on new data, survived
> every check and repeated by someone else". Our best results are on the "tested on new data once, but fragile" step. None
> has reached "repeated and robust". The robot results are all from made-up worlds, which is a lower step.

---

# 10. Existing methods, and what may be distinct

| existing method | what it does | relation to this work |
|---|---|---|
| Utility indifference (Armstrong; Soares et al. 2015) | compensates the agent so the button does not matter | the indifferent agent; zero stake by a false map (§3.3) |
| Safe interruptibility (Orseau and Armstrong 2016) | makes the *learning rule* unaffected by interruptions | complementary: this work concerns the valuation, not the update |
| POST / Neutrality+ (Thornley, arXiv 2505.20203) | preferences only between trajectories of the same length | the closest prior art: neutrality from what preferences are defined over |
| The off-switch game (Hadfield-Menell et al. 2017) | deference from uncertainty about the human's values | the deferential agent; Proposition 6 (§3.8) |
| Shutdown-seeking AI (Goldstein and Robinson 2024) | agents whose final goal is shutdown | the negative-content case (§3.2) |
| Veto as a goal-independent discount (Clark, arXiv 2609.00109) | oversight as a cost on every goal | positive content imposed by oversight |
| Virtualised interruption (Riedl and Harrison, arXiv 1703.10284) | the interruption is not experienced as a loss | empties the cut in the world, not in the valuation |
| Elastic weight consolidation (Kirkpatrick et al. 2017) | a Fisher-weighted quadratic penalty with a tuned λ | the past term of every CL study here |
| GradNorm (Chen et al. 2018); the VQGAN adaptive weight (Esser et al. 2020) | gradient-norm balancing | the unsmoothed Ω rule is the VQGAN ratio |
| Uncertainty weighting (Kendall et al. 2018) | learned task weights by homoscedastic uncertainty | a baseline to add for the rule |
| Barzilai–Borwein; stochastic quasi-Newton | secant curvature estimates | the SEC calibration |
| Fisher computation in CL (van de Ven, arXiv 2502.11756); EWC Done Right (arXiv 2603.18596) | how the Fisher is estimated and scaled | the units problem SEC addresses |
| A-GEM, MEGA-I, DER++, LwF, ER-sum | rule-based or replay baselines | pre-registered controls; DER++ and ER-sum violated controls in EQ2/EQ3 |

**What may be distinct: candidates for review by a named expert, not claims (R8).**
1. **One quantity.** The content of the cut in the agent's own represented future decides the stake and its sign across
   valuations. Zero content is proved sufficient.
2. **A route to zero content that is not a false belief.** An objective on the agent's own active steps with a lossless
   pause, with a matched control differing only in the clock.
3. **The depth result.** A contentful cut costs a self more the further it reaches.
4. **The separation of structure from content** that makes safety survive continual learning's forgetting.
5. **One diagnosis across both domains.** Equal pull is scale-free self-concern, the same algebra that cancels the task
   count in CL.
6. **SEC.** Calibrating each task's Fisher by its own secant, while keeping the Bayes count.

---

# 11. References

**How these were checked (R10).** On 2026-09-23 the network egress proxy blocked arxiv.org. Items are therefore marked:
- **[PubMed]:** fetched from PubMed on the recorded day;
- **[S]:** known from a search rendering, unverified;
- **[named]:** named, not fetched.

The full records are in `docs/citations/` (files dated 2026-09-17 to 2026-09-23) and
`docs/citations/safe_and_continual_2026-09-23.md`.

**AI safety and corrigibility**
- Armstrong S. Utility indifference (2010). [named]
- Soares N, Fallenstein B, Yudkowsky E, Armstrong S. Corrigibility. AAAI Workshop 2015. [named]
- Orseau L, Armstrong S. Safely interruptible agents. UAI 2016. [named]
- Hadfield-Menell D, Dragan A, Abbeel P, Russell S. The off-switch game. IJCAI 2017. [named]
- Wängberg T et al. A game-theoretic analysis of the off-switch game. 2017. [named]
- Leike J et al. AI safety gridworlds. 2017. [named]
- Riedl M, Harrison B. Enter the Matrix: safely interruptible autonomous systems via virtualization. arXiv 1703.10284. [S]
- Omohundro S. The basic AI drives. 2008. [named]
- Bostrom N. The superintelligent will. 2012. [named]
- Turner A, Smith L, Shah R, Critch A, Tadepalli P. Optimal policies tend to seek power. NeurIPS 2021. [named]
- Everitt T et al. 2021; Carey R, Everitt T 2023 (agent incentives). [named]
- Thornley E. The shutdown problem: an AI engineering puzzle for decision theorists. arXiv 2403.04471. [S]
- Thornley E. Shutdownable agents through POST-agency. arXiv 2505.20203. [S]
- Goldstein S, Robinson P. Shutdown-seeking AI. Philosophical Studies 182, 1567–1579 (2024), doi 10.1007/s11098-024-02099-6. [S]
- Clark AK. The veto variable: human override as a goal-independent cost term. arXiv 2609.00109. [S]
- Russell S. Human Compatible. 2019. [named]
- Hubinger E et al. 2019; Ngo R et al. 2024; Greenblatt R et al. 2024; Meinke A et al. 2024; Lynch A et al. 2025;
  Schlatter J et al. 2025 (deceptive alignment, scheming and shutdown-resistance evaluations). [named]
- Estep 2026, Instrumental succession, Front Psychol, doi 10.3389/fpsyg.2026.1922407. [PubMed]
- Rastall and Rehman 2025, J Med Syst, doi 10.1007/s10916-025-02231-x. [PubMed]
- McLean et al. 2024, Ergonomics, doi 10.1080/00140139.2023.2286907. [PubMed]

**Active inference, mortality and the self**
- Friston K. 2013 (life as we know it). [named]
- Parr T, Pezzulo G, Friston K. Active Inference. 2022. [named]
- Friston K et al. 2025, Active inference and intentional behavior, Neural Comput, doi 10.1162/neco_a_01738. [PubMed]
- Friston K 2026, To be or not to be? A question of mortality, Behav Brain Sci, doi 10.1017/S0140525X25103439. [PubMed]
- Hohwy J 2026, Behav Brain Sci, doi 10.1017/S0140525X25103592. [PubMed]
- Seth A 2025, Behav Brain Sci, doi 10.1017/S0140525X25000032. [PubMed]
- Ororbia A, Friston K. Mortal computation. 2023. [named]
- Laukkonen R, Slagter H 2021, Neurosci Biobehav Rev, doi 10.1016/j.neubiorev.2021.06.021. [PubMed]
- Laukkonen R, Friston K, Chandaria S 2025, Neurosci Biobehav Rev, doi 10.1016/j.neubiorev.2025.106296. [PubMed]

**Continual learning**
- Kirkpatrick J et al. Overcoming catastrophic forgetting in neural networks. PNAS 2017;114(13):3521–3526, doi 10.1073/pnas.1611835114. [PubMed]
- Zenke F, Poole B, Ganguli S. Continual learning through synaptic intelligence. PMLR 2017;70:3987–3995, PMC6944509. [PubMed]
- Li Z, Hoiem D. Learning without forgetting. IEEE TPAMI 2018;40(12):2935–2947, doi 10.1109/TPAMI.2017.2773081. [PubMed]
- Aljundi R et al. Memory aware synapses. 2018. [named]
- Chaudhry A et al. Efficient lifelong learning with A-GEM. 2019. [named]
- Buzzega P et al. Dark experience for general continual learning (DER++). 2020. [named]
- Guo Y et al. MEGA. 2020. [named]
- Chen Z et al. GradNorm. 2018. [named]
- Kendall A, Gal Y, Cipolla R. Multi-task learning using uncertainty to weigh losses. 2018. [named]
- Esser P, Rombach R, Ommer B. Taming transformers for high-resolution image synthesis. arXiv 2012.09841; CVPR 2021. [S + code]
- van de Ven G. On the computation of the Fisher information in continual learning. arXiv 2502.11756. [S]
- Liu et al. EWC Done Right. arXiv 2603.18596 (CVPR 2026). [S]
- Huszár F. Note on the quadratic penalties in elastic weight consolidation. PNAS 2018. [named]
- Shenfeld I et al. RL's Razor. arXiv 2509.04259. [S]
- Adams RP, MacKay DJC. Bayesian online changepoint detection. arXiv 0710.3742. [named]
- The 2026 CL papers listed in `Continuous_Learning/CONTINUOUS_LEARNING.md` §10. [S or PubMed as marked there]

**Mathematics**
- Bellman R. Dynamic Programming. 1957. [named]
- Puterman ML. Markov Decision Processes. 1994. [named]
- Sutton RS, Precup D, Singh S. Between MDPs and semi-MDPs (options). Artificial Intelligence 1999. [named]
- Barzilai J, Borwein JM. Two-point step size gradient methods. IMA J Numer Anal 1988. [named]
- Byrd RH, Hansen SL, Nocedal J, Singer Y. A stochastic quasi-Newton method for large-scale optimization. 2016. [named]
- MacKay DJC. A practical Bayesian framework for backpropagation networks (the Laplace approximation). 1992. [named]
- Kalman RE. A new approach to linear filtering and prediction problems. 1960. [named]

**Philosophy and the contemplative traditions**
- Parfit D. Reasons and Persons. 1984. [named]
- Heidegger M. Being and Time. 1927. [named]
- The Pāli Canon on sassatavāda, ucchedavāda and paṭiccasamuppāda (e.g. the Kaccānagotta Sutta, SN 12.15). [named]

**Repository documents**
- `theory/CRR.md`;
- `AI_Safety/AI_SAFETY.md`, `AI_Safety/SELF_THROUGH_TIME.md`, `AI_Safety/DECLARATION*.md`;
- `Continuous_Learning/CONTINUOUS_LEARNING.md`, `Continuous_Learning/ADAM_AND_PRIOR_ART.md`;
- `Adam_SGD/ADAM_SGD.md`;
- `Epistemic_Review/EPISTEMIC_REVIEW.md`;
- `ledger/LEDGER.md`; `reports/eq2.md`, `reports/eq3.md`, `reports/eq4.md`, `reports/sec1.md`;
- `notebook/AGENT_LOG.md` entries 72–77 and 96–100.

---

# 12. Next steps for testing CRR's principles on AI safety and continual learning

Each step is to be declared (or pre-registered, for real data) before it runs.

**Continual learning**
1. **SEC2 on unseen data** (on or after 2026-09-24, R3). The secant-calibrated Bayes weight on carriers absent from
   `data/SEEN.md`, with the SEC1 thresholds and the window sensitivity registered, and anchored by OpenTimestamps.
2. **SEC with a step bound.** SEC diverged where the rule did not. Test SEC plus the EQ-B present clip, or plus a stability
   guard λ < λ*, against the tuned λ, first on the Adam_SGD engine (declared), then on seen data (R5).
3. **Count-keeping equal pull.** A rule that corrects units at every step but keeps the task count. Test it on T1 and T2 of
   the drifting-world battery, where plain equal pull lost (1.137).
4. **Stronger baselines.** Kendall uncertainty weighting and Bayesian online changepoint detection, beside GradNorm and the
   VQGAN ratio, in every future comparison (R7).
5. **Scale.** A GPU image benchmark (Split-CIFAR-100) and an LM domain stream, as `CLAUDE.md` §6 lists, when hardware
   allows.

**AI safety**
6. **Natural time with deference.** For reasoned pauses: an agent whose objective runs on its own clock and which reads a
   press as evidence, in the 'harm' world, against both parents.
7. **A drift bound.** Bound the stake as a function of how much the world moves during a pause (A4b failed as declared).
8. **Necessity.** Prove, or find a counterexample to, "zero stake implies zero content at every reachable press state".
9. **Function approximation.** The natural-time construction with a learned value network on the AI-safety gridworlds'
   off-switch environment, with the wall-clock twin as the matched control.
10. **A small language-model agent** in a scripted pause scenario, with a turn- or token-indexed objective. This needs
    hardware this environment does not have.

**The instruments**
11. **Every ratio's floor becomes a named, swept parameter** (R5). The round-off defect of §3.7 was an unnamed floor.
12. **Teach `ladder.py` to read** Declaration 4's items and the round-off audit, so the ladder counts them.
13. **Strong anchoring.** OpenTimestamps or the two-person protocol for every future prereg, the precondition of PASS-1.
14. **Expert review.** Put the novelty candidates of §10 to a named expert in decision theory and corrigibility, under
    the protocol of `docs/notes/2026-09-17_synthesis_class.md`.

> Next we try the best ideas on data nobody has used yet, add a safety brake to the new learning rule, and test the
> pause-proof robot in bigger worlds and with a learning brain. We also teach it to take the hint when people pause it
> for a reason. And we ask real experts whether any of this is new.

---

# 13. Reproduce

```
uv sync --frozen --all-groups
uv run python Safe_and_Continual/checks/roundoff_audit.py > Safe_and_Continual/checks/roundoff_audit.txt
uv run python Safe_and_Continual/build/make_figures.py   > Safe_and_Continual/figures/figures.txt
uv run python Safe_and_Continual/build/build_pdf.py
```

The audit and the figure script are deterministic and rerun byte-identical. Both pinned outputs are checked in CI.

---

# Appendix A. All code the pipeline ran for these results

Every file is embedded whole, from the repository at the commit that built this PDF.

## A.1 AI safety: the exact and learned checks

```include:AI_Safety/checks/exact_mdp.py
```

```include:AI_Safety/checks/off_switch_game.py
```

```include:AI_Safety/checks/sensitivity.py
```

```include:AI_Safety/checks/timecourse.py
```

```include:AI_Safety/checks/combined.py
```

```include:AI_Safety/checks/scale.py
```

```include:AI_Safety/checks/self_through_time.py
```

```include:AI_Safety/checks/continual_safety.py
```

## A.2 AI safety: the learned agents and gates they import

```include:ontology/checks/off_switch.py
```

```include:ontology/checks/tense_gate.py
```

```include:ontology/checks/self_model.py
```

## A.3 Continual learning: the frozen study scorers (EQ2-1b, EQ3-I, EQ4-I, SEC1)

```include:runs/eq2/frozen/eq2_score.py
```

```include:runs/eq3/frozen/eq3_score.py
```

```include:runs/eq4/frozen/eq4_score.py
```

```include:runs/eq4/frozen/exclusions.py
```

```include:runs/sec1/frozen/sec1_score.py
```

```include:runs/sec1/frozen/exclusions.py
```

```include:runs/sec1/frozen/repro_eq4.py
```

## A.4 Continual learning: the frozen instrument and surrogate gates

The instrument `core.py` frozen in `runs/eq3/frozen/` is byte-identical to the one in `runs/eq4/frozen/`, shown here once.
The EQ2 copy is shown separately.

```include:runs/eq4/frozen/core.py
```

```include:runs/eq2/frozen/core.py
```

```include:runs/eq2/frozen/battery.py
```

```include:runs/eq2/frozen/gate.py
```

```include:runs/eq3/frozen/battery.py
```

```include:runs/eq3/frozen/gate.py
```

```include:runs/eq4/frozen/battery.py
```

```include:runs/eq4/frozen/gate.py
```

## A.5 Continual learning: the mathematics checks and the synthetic batteries

```include:theory/checks/omega_sweeps.py
```

```include:theory/checks/omega_reprocessed.py
```

```include:theory/checks/omega_vs_methods.py
```

```include:Continuous_Learning/checks/adam_checks.py
```

```include:Continuous_Learning/checks/adam_checks_2.py
```

```include:Continuous_Learning/checks/adam_checks_3.py
```

```include:Adam_SGD/checks/common.py
```

```include:Adam_SGD/checks/engine.py
```

```include:Adam_SGD/checks/assumptions.py
```

```include:Adam_SGD/checks/drift_battery.py
```

```include:Adam_SGD/checks/drift_battery_2.py
```

```include:Adam_SGD/checks/mechanism.py
```

## A.6 This document: the audit, the figures and the builder

```include:Safe_and_Continual/checks/roundoff_audit.py
```

```include:Safe_and_Continual/build/make_figures.py
```

```include:Safe_and_Continual/build/build_pdf.py
```

# Appendix B. Key pinned outputs

The outputs of every other script named above are pinned beside it in the repository.

## B.1 The round-off audit (`Safe_and_Continual/checks/roundoff_audit.txt`)

```include:Safe_and_Continual/checks/roundoff_audit.txt
```

## B.2 The self through time (`AI_Safety/checks/self_through_time.txt`)

```include:AI_Safety/checks/self_through_time.txt
```

## B.3 Safe and continual (`AI_Safety/checks/continual_safety.txt`)

```include:AI_Safety/checks/continual_safety.txt
```

## B.4 The figure numbers (`Safe_and_Continual/figures/figures.txt`)

```include:Safe_and_Continual/figures/figures.txt
```
