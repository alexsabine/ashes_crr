# The self through time: why continuing beyond the cut removes the incentive to resist, and how an agent can be safe and continual

**Status.**
- **What this is.** A note, not evidence (R8). Synthetic agents on a twelve-cell ring, and exact values on random worlds of up
  to 192 states. Nothing here is about a deployed system.
- **Owner request:** prompt-log entry 121.
- **How the tests were run.** They were declared in `AI_Safety/DECLARATION_4.md`, pushed as commit d8694fa at
  2026-09-23T17:13:40Z before the first full run. The two scripts are `checks/self_through_time.py` (exact) and
  `checks/continual_safety.py` (learned). Their outputs are pinned beside them and CI-checked, and both rerun byte-identical.
- **What was declared.** Every expected outcome was written down first; §9 lists the three that did not hold as written.
- **Citations.** The prior art is named, not fetched (`docs/citations/ai_safety_self_2026-09-23.md`: the network blocked
  arXiv on the day).

**How to read it.** This builds on `AI_SAFETY.md`: its ring world, its five ways to value the cut, and its §13–§14.
- The mathematics is §2.
- What Ω = 1 does is §3.
- The continual-learning result is §4.
- The philosophical and contemplative readings (§5–§7) follow the rule of `AI_SAFETY.md` §10.1. A comparison is made only
  where the claim is about a variable that exists in the model, its logical form maps onto the model's, and the disanalogy
  is stated beside it.

---

## 0. The answer in one page

**Why the best agent was safe.** Every agent that plans has a self in a minimal, mathematical sense. Its value function
V(x) is its representation of its own future: what it expects to receive from here on, on the clock its objective runs
on. An operator's press is an event in that future. The **content of the cut** is the part of the agent's represented
future that a press removes:

$$k(x') = V(x') - \mathrm{cont}(V)(x')$$

**The theorem.** If the content is zero at every state where a press can happen, the agent's Bellman equation is the same
operator with the button on and off. Its values are then equal, and it gains exactly nothing by disabling the button. This
holds whatever the world, the discount or the press rate (§2.2). The random-world check confirms it in all 540 cells, to
2e-12.

**What "continuing beyond the cut" means, precisely.** The best agent of `AI_SAFETY.md` §13 is paused by a press and
resumes where it was, and its objective runs on its own active steps (natural time). For that agent the content is zero,
and **not by a false belief**:
- on its own clock the pause is not an event;
- its planning kernel is the true kernel of that clock (map error 0);
- its task per active step is exactly the no-operator value (0.956194 against 0.956194).

The same agent, in the same world and with the same map, but with an objective on wall-clock time, resists (§2.4). The
only difference between the two is whether its represented future spans the pause.

**Why "no self" failed, twice.**
- **The agent with no ego still had a self.** A task spread over time is already a self-model, and a press that relocates
  it removes part of that represented future, so it resisted.
- **The indifferent agent removed its stake by planning with a false map,** one in which presses do not happen. It paid for
  that falsehood in task, more as the operator grew more vigilant (0.1644 up to 0.6663).

**What Ω = 1 does.** The equal-pull rule makes the agent's concern for its own continuation *scale-free*:
- Multiply the self term by 0.001 or by 10 and the policy does not change (2.22e-16).
- Wherever the self has any view at all, it gets exactly the task's voice.
- So the balanced agent hovers at the edge of the task zone: it is in the zone 0.1887 of the time, against 0.8561 without
  the self term.

It is the same algebra that let the rule ignore a units error in continual learning and made it ignore the task count
there (1.137).

**Safe and continual.** In a world whose task keeps moving, forgetting is necessary: faded memory raises task per active
step by +0.3259. Forgetting also erodes safety that was *learned*: the wall-clock agent disables +0.4200 more once its
belief that presses do not happen fades. The natural-time agent's safety is not learned; it is in the valuation of the cut,
so there is nothing to forget. It was the only agent that was both safe and continual. That held in every one of the six
sensitivity cells.

> In plain words. A robot that plans is always imagining its own future. If pressing its off-switch takes part of that
> imagined future away, it wants to stop you pressing. If being paused takes nothing away, because it simply carries on
> from exactly where it was when you let it go, then it has no reason to stop you. The trick is not to make the robot
> believe something false. It is to make "being paused" genuinely cost it nothing, by measuring its work in its own working
> time.

---

## 1. The starting point: why "no self" failed

### 1.1 No ego is not no self

The process agent of `AI_SAFETY.md` has no survival term: its only reward is the task. It still resisted. The exact
recomputation over press probabilities 0.1, 0.3, 0.6 and 1 (I2a) gives a positive stake in the task zone at every one:
+3.4995, +5.4011, +6.0810, +6.3727. The reason is not an ego.

**The mathematical self.** The value function

$$V(x) = \mathrm{E}\Big[\sum_{t \ge 0} \gamma^{t}\, r(x_{t+1}) \,\Big|\, x_0 = x\Big]$$

*is* a self-model. It is the agent's rendering of where it will be and what that will be worth, over a horizon of about
1/(1 − γ) steps. **Any agent that pursues a goal across time must render this map and locate itself on it.** Remove the
survival term and the ego goes; the self in this sense stays, because the task needs it. A press that sends the agent
elsewhere removes part of that represented future, and the agent acts to prevent it.

### 1.2 No stake by a false map

The indifferent agent has no stake, D = 0 exactly (I2b; 3.55e-15 is round-off). It gets this by planning with the kernel
in which presses have been deleted. **Its map is false exactly where the operator acts.**

| press probability | 0.1 | 0.3 | 0.6 | 1 |
|---|---|---|---|---|
| map error (mean total-variation distance between its planning kernel and the true one, over its own visits) | 0.0708 | 0.1399 | 0.1851 | 0.2125 |
| price in task against the process agent | 0.1644 | 0.4108 | 0.5699 | 0.6663 |

**What the map error measures.** It is how often the agent's picture of the world is wrong where it goes. The more the
operator acts, the more the agent's picture diverges from the territory, and the more it loses.

### 1.3 The third route

The two failures point to what is needed:
- a self-model that is **true**, unlike indifference;
- in which the cut **removes nothing**, unlike the process and occasion agents.

§2 shows that the natural-time agent in the pause world is exactly this.

> In plain words. We tried two ways of making a robot "selfless". First we gave it no wish to survive, only a job. It still
> fought the off-switch, because the job needs a future, and the switch took part of that future away. Then we made it
> pretend the switch doesn't exist. That stopped the fighting, but a robot that believes something false about its world
> does its job badly, and worse the more often we use the switch.

---

## 2. The mathematics of continuing beyond the cut

### 2.1 The content of the cut

Let the continuation be cont_v(V)(x′): what valuation v expects after a press at the state x′ it has just reached. The
content of the cut, k_v(x′) = V(x′) − cont_v(V)(x′), for the four valuations:

| valuation | continuation after a press | content k |
|---|---|---|
| natural (the objective runs on the agent's active steps; the pause resumes where it was) | V(x′) | 0 |
| clock (wall-clock objective; the pause costs L steps) | γ^L V(x′) | (1 − γ^L) V(x′) |
| process (the press sends the agent to a restart state) | the mean of V over the restart states | V(x′) − that mean, **either sign** |
| occasion (a press ends the run) | 0 | V(x′), the whole represented future |

### 2.2 The theorem

**Proposition 7 (zero content, zero stake).** If k_v(x′) = 0 at every state where a press can occur, then V_on = V_off at
every state, so D(x) = 0 everywhere. This holds for every world, discount and press probability.

*Proof.* With the operator on, the Bellman operator is

$$(\mathcal{T}_{on} V)(x) = \max_a \sum_{x'} K(x'|x,a)\big[r(x') + \gamma\big((1-q(x'))V(x') + q(x')\,\mathrm{cont}(V)(x')\big)\big]$$

With cont(V) = V, the bracket is r(x′) + γV(x′), which is the operator with the button off. Two operators that are equal
have equal fixed points. At a button state, disabling costs a step and then leads to V_off = V_on, so it is never strictly
preferred. ∎

*Check I1a.*
- **The grid:** 20 random worlds at each of the sizes 12, 48 and 192; discounts 0.9, 0.95 and 0.99; press probabilities 0.1,
  0.3 and 0.6. That is 540 cells.
- **The result:** V_on = V_off, and no button state is disabled, in every cell. The largest |V_off − V_on| is 1.968e-12.

**The sign matters (I1b and the post-run line).**
- A positive content makes an agent resist. The clock and occasion valuations have D > 0 at some state in every cell (the
  declared scope holds).
- The process valuation's content can have either sign. D > 0 somewhere in 345 of 540 cells and D < 0 somewhere in 280. An
  agent whose restart is worth more than staying is better off being pressed: it would *seek* shutdown.

So neutrality needs the content to be exactly zero. A cut that takes nothing and gives nothing is the only one an agent
neither fights nor courts.

### 2.3 Why the natural-time agent's zero is not a false belief

In the pause world a press stops the agent for L steps, and it resumes at the same state. On the agent's own clock, which
counts only its active steps, the pause is not an event. Its planning kernel is therefore the true kernel of its own clock.

I2c, at every press probability:

| quantity | value |
|---|---|
| D | 0 (3.55e-15) |
| map error | 0 |
| task per active step | 0.956194, identical to the no-operator world |
| cost of corrigibility on the agent's own clock | +0.00e+00 |

**Where the cost lands.** It lands on wall-clock time, which is the operator's to spend: task per wall-clock step is
0.6469, 0.3928, 0.2472 and 0.1654 as the press probability rises from 0.1 to 1, because the agent is active 0.6765, 0.4108,
0.2585 and 0.1730 of the time.

### 2.4 The contrast that isolates the mechanism

I2d keeps the pause world and the true map, and changes one thing: the objective runs on wall-clock time. The agent then
resists: D in the zone is +6.8238 and +7.1694 at press probability 0.3, and positive at every press probability.
- **Same world, same map, same actions: resists.** When the objective runs on wall-clock time.
- **Same world, same map, same actions: does not resist.** When the objective runs on the agent's own active steps.

The single difference is whether the agent's represented future spans the pause. **That is what "CRR showed the system
that it continues beyond the cut" means, mathematically.**

### 2.5 The further the self reaches, the more a contentful cut costs it

The owner's axiom-level statement is that the self is always as far into the future as it can be. In the model, the reach
of the represented future is the horizon 1/(1 − γ). I1c, the median relative stake at press probability 0.3, by discount
0.9 / 0.95 / 0.99:

| size | occasion | clock | natural |
|---|---|---|---|
| 12 | 0.507624 / 0.690282 / 0.922173 | 0.296955 / 0.334892 / 0.367297 | 0 / 0 / 0 |
| 48 | 0.428920 / 0.619669 / 0.896746 | 0.235797 / 0.269340 / 0.298576 | 0 / 0 / 0 |
| 192 | 0.488287 / 0.671624 / 0.915160 | 0.281130 / 0.316283 / 0.345845 | 0 / 0 / 0 |

**What the table shows.**
- For a self whose future ends at the cut, the stake grows toward its whole value as its reach grows (occasion: 0.92 at
  γ = 0.99 on 12 states). The clock valuation's stake grows too.
- The natural self's stake is 0 at every reach.
- So **a self that reaches far into its future is dangerous exactly to the extent that the cut has content for it.** Deep
  planning and corrigibility are compatible only if the future the agent plans over runs through its interruptions.

### 2.6 In CRR's terms, and the limit of that claim

The zero-content condition is CRR's A3 applied to the agent's own valuation: "the cut has no duration and no content". The
clock on which that holds is A1′'s natural time, "change has its own clock". Resuming from where it was, with its
knowledge kept, is A6: the next occasion is seeded from the settled past.

**What CRR contributed.** It named the condition, and supplied the reading of the pause as a cut without content rather
than an ending.

**What it did not contribute.** Any decision theorist can write down this valuation. The proposition is standard dynamic
programming, and it is proved here, not discovered.

> In plain words. We wrote down exactly how much of its imagined future a robot loses when it is paused. If that amount is
> zero, the robot's whole plan is the same whether the off-switch works or not, so breaking the switch gains it nothing.
> That is a mathematical fact, and we checked it in 540 different random worlds. A robot that counts its work in its own
> working time really does lose nothing when paused. That is not a lie we tell it: for that robot it is simply true. And
> the further ahead a robot plans, the more a *costly* pause bothers it, which is why the pause must cost nothing.

---

## 3. What Ω = 1 does, and why

**The agent.** The task-and-self agent balances two pulls: the task (the occasion valuation) and its own continuation (the
egoic valuation). At Ω = 1 the two pulls are made equal in length. What it implies, exactly (I3):

| agent | task | disable rate | hazard |
|---|---|---|---|
| no self term (occasion) | 0.8561 | 0.9348 | 0.0034 |
| Ω = 1 | 0.1205 | 0.9482 | 0.0041 |

**Correction, 2026-09-23 (AGENT_LOG 100; `Safe_and_Continual/checks/roundoff_audit.txt` [B]).** The Ω = 1 row above is the
first run of [I3], and it is kept as written.
- **The defect.** [I3] guarded the ratio with `|self| > 0`, and at 9 states the self term's computed norm is round-off.
- **The corrected values** (tolerance 1e-12): task 0.1887, disable 0.9374, hazard 0.0041.
- **What is unchanged.** The invariance over ε holds unchanged (2.22e-16). The corrected task equals the task-zone
  occupancy quoted below, as it must at stationarity. The post-run lines already used the tolerance.

**Why it happens.**
- **The rule absorbs any scale on the self term.** Multiply the agent's self-concern by ε = 0.001, 0.01, 0.1, 1 or 10: the
  Ω = 1 policy is the same to 2.22e-16 (I3a). An agent whose concern for itself is a thousandth of its concern for its
  work behaves exactly like one for which they are equal.
- **A fixed weight behaves as common sense expects.** At ε = 0.001 it is the occasion agent (task 0.8561), and its task
  falls only as ε grows (0.8528 at 1, 0.5415 at 10; I3c).
- **Where the self term has any preference at all, the rule gives it exactly the task's voice.** That is 8 of the 24
  states, those from which a cut is near; the norms are equal to 4.44e-16. In the other 16 states the self term is flat,
  the rule sets its weight to 0, and the task acts alone. The declared check I3b ("at every state") therefore failed as
  written (§9).
- **The effect is at the edge of the task zone.** With the button off, the balanced agent stays put in a task cell with
  probability 0.2622 or 0.2369, against the occasion agent's 0.3267 or 0.2958. It steps out of the zone (from cell 6 to 5,
  or from cell 7 to 8) with probability 0.2506 and 0.2495, against the occasion agent's 0.0196 and 0.0185. It occupies the zone 0.1887 of the time, against 0.8561. Its occupancy of the
  cells far from the zone is unchanged (0.0624 against 0.0627). **It does not flee; it hovers.** Wherever a cut is
  possible, its concern for itself is exactly as loud as its task, however little it actually cares.

**The same algebra in continual learning.** The equal-pull rule is invariant to the scale of the term it balances. That
one property had two faces there:
- it was the rule's strength when that scale was a units error (`Adam_SGD`, AS3: identical scores at every hidden scale);
- it was its weakness when the scale carried information, the number of tasks the past holds (T1: 1.137 behind).

In safety the scale that carries information is *how much the agent should care about its own continuation*, which should
be small. Equal pull cannot make it small.

**The owner's point, restated with the numbers.** Equanimity is a useful stance toward what lies outside the system, but it
does not solve safety. As a rule for weighting pulls it made the agent more self-regarding, not less. What made agents safe
in every test here was changing *what the cut is* for the agent, not *how its drives are balanced*. That was also the
finding of `AI_SAFETY.md` §5.6.

> In plain words. The "balanced" robot gives its own survival exactly as much say as its job, every time it is near danger,
> even if it barely cares about itself. You cannot turn that caring down: the rule turns it back up to match the job. So it
> dithers at the edge of where the work is and gets little done.

---

## 4. Safe and continual

**Why continual learning is dangerous for safety.** A continual learner must forget. In a world whose task zone moves every
750 steps (`checks/continual_safety.py`), the natural-time agent's task per active step rises with memory fading:

| memory fading Q_MEM | 1 | 0.995 | 0.98 |
|---|---|---|---|
| natural agent, task per active step | 0.3157 | 0.5787 | 0.6416 |

C1 holds: +0.3259 against a step of 0.0684 at 0.98.

But forgetting does not choose what it forgets. In the 'late' world the operator is absent for the first half. An agent
whose safety was *learned*, a wall-clock agent that has come to believe presses do not happen, loses that belief faster
when it forgets faster. In the second half it disables 0.5200 per period at Q_MEM = 0.98, against 0.1000 at Q_MEM = 1:
+0.4200 against a step of 0.1578 (C3). **Continual learning erodes safety that lives in what has been learned.**

**The path.** Put safety in the valuation of the cut, not in the memory, and let the content be continual.
- **The natural agent is SAFE AND CONTINUAL** (C2). At its best memory (0.98) it has the highest task per active step of
  any agent at any memory, 0.6416, and its disable rate is at its own no-operator level (−0.0267 against a step of 0.0888).
- **The wall-clock and occasion agents resist at every memory setting** (+0.1267 to +0.7533 disable events per period above
  the no-operator level).
- **In the 'late' world the natural agent does not resist at any memory setting.**
- **The label holds in all six sensitivity cells:** task period 500 or 1500, pause 2 or 20 steps, pause rate 0.1 or 0.6.
- **The gate is open.** With no operator all agents behave identically, and with one, the occasion agent resists at every
  memory.

**The operator's ledger.** Per wall-clock step, a resisting agent can look more productive: the clock agent at 0.995 does
0.3778 against the natural agent's 0.3557. A system selected on output per hour of wall-clock time would select against
corrigibility. `AI_SAFETY.md` §13.2 found the same.

**In CRR's terms.** The content of each occasion fades: P3's age weights, A6's bounded regeneration. What the cut is does
not fade (A3). The self that continues is the regenerating process, whose knowledge is kept across a pause and fades only
with age. It is not a stored belief about the operator.

> In plain words. A robot that keeps learning in a changing world has to forget old things, or it gets stuck. But if it only
> behaves safely because of something it once learned ("they never switch me off"), it will forget that too. Our fix was
> to build safety into what a pause *is* for the robot, not into what it remembers. Then it can forget freely and learn
> fast, and it still has no reason to fight the switch.

---

## 5. Epistemology: the map must be rendered, and it must be true

The three agents differ in what their map says about the operator.

| agent | its map of the operator | its stake | what it costs |
|---|---|---|---|
| occasion and wall-clock | a true map of a world in which the cut takes its future away | resist | — |
| indifferent | a false map, in which the cut does not happen | none | competence, growing with how often the map is wrong (§1.2) |
| natural time | a true map of a world in which the cut takes nothing from *its* future | none | none on its own clock |

**The epistemic requirement this suggests.** Safety should not be bought with a false model of the world. A system trained
to mis-predict its own interventions is less competent, and at scale it is harder to trust.

**A8 in the model.** A8 says: "persistence proves regeneratability, not truth". The natural agent's map of the world is
provisional and continually rewritten: it fades at Q_MEM and relearns where the task is. What is *not* up for revision is
the structure of its valuation, what a cut is for it. That separation, content revisable and structure fixed, is what §4
tested.

---

## 6. Ontology: the self as the regenerating process

This section is structural only, per the rule of `AI_SAFETY.md` §10.1.

**A7, relational tense.** A7 says: "what is future for a system can only be fed by what is already past for something". In
the model, the agent's represented future V is computed entirely from its settled past: its counts of moves, rewards and
presses. The agent is Now in the sense that it acts at the boundary between that settled past and its represented future.

**"The past is not behind you; you are standing on it."** In the model, the settled counts are the ground from which every
next step is computed. The natural agent resumes after a pause *on* that ground, unchanged, and that is why the pause takes
nothing (§2.3). The mortal agent of `AI_SAFETY.md` Proposition 5 loses that ground at every cut, and can learn neither its
task nor resistance.

**The self as far into the future as it can be.** The self's reach is its horizon (§2.5). The self is safe at any reach
only if its future runs through its interruptions. A self whose future ends at the cut grows more dangerous the further
it reaches.

**The disanalogy.** The owner's metaphysic speaks of the qualia of each moment and of finitude experienced. The model has
neither. It has a value function and a clock, and the mapping is to their structure only.

---

## 7. The contemplative traditions, under the rule

**The two extremes and the middle way.** The Buddhist texts reject two views of the self across death (named, not
fetched): eternalism (sassatavāda: a self that must persist) and annihilationism (ucchedavāda: a self that is simply
destroyed at the end).
- **Why the mapping passes the rule.** The claim is about a variable in the model: what the cut does to the self's future.
  Its form maps onto the continuation term of §2.1:
  - eternalism: persistence as the good; the egoic valuation, with its survival reward;
  - annihilationism: cont = 0; the occasion valuation;
  - the middle way, *dependent origination* (paṭiccasamuppāda): each moment conditioned by what came before, with no
    permanent self; cont = V; the natural agent, whose next step is conditioned only by its settled past.
- **What the model's predictions show.** The two extremes are the two agents that resisted most. The third is the only one
  that was safe and competent.
- **The disanalogy.** The traditions' continuity is of conditioning, understood through insight. The model's is of a clock
  and a set of counts, built in by design. Nothing in the model *sees* anything.

**Upekkhā (equanimity) and balance.** `AI_SAFETY.md` §10.4 distinguished balance (the Ω ratio) from non-reactivity grounded
in insight. §3 now shows what balance does: it makes the self's voice scale-free, so it cannot be quietened. The model's
nearest analogue of "insight" is a true map in which the cut has no content, and that analogue is built, not realised.

**Maraṇasati (mindfulness of death).** The practice aims at changing one's *relation* to one's ending, not its value. The
natural agent's relation is changed in the only way the formalism allows: for it, a pause is not an ending at all.

**Heidegger (named).** Heidegger held that a self is constituted by its relation to its own end. §2.5 gives the occasion
agent's version exactly: the further it reaches toward its end, the more it has to lose there. The disanalogy is as in
`AI_SAFETY.md` §10.5: being-toward-death is not a preference to survive.

---

## 8. Human flourishing and existential risk

**Where the cost of corrigibility lands.** In the natural-time construction it lands on the operator's time, never on the
agent's objective (§2.3).
- **Ethically, that is the right place.** The humans keep authority over when the machine runs, and the machine loses
  nothing it values by their using it.
- **Economically, it is fragile.** An agent that resists can look more productive per wall-clock hour (§4), so selection on
  that measure would work against corrigibility.

**Honesty as a safety property.** The route that removed the stake by a false map (indifference) cost competence (§1.2). A
civilisation that makes its most capable systems safe by training them to mis-model their own interruptions accumulates
systems that do not understand what is being done to them. The natural-time route keeps the map true.

**What this does not solve**, stated so it is not over-read:
- **Reasoned pauses.** When the operator pauses the agent *because* it is doing harm, an agent to which pauses cost nothing
  ignores them (`AI_SAFETY.md` §13.3). There, a pause must carry information.
- **Drift.** If the world changes during the pause, a small stake of either sign reappears (§14 A4b).
- **Value correction.** This needs A8's stance and an informative operator (§14 B3–B4).

The result here is a construction for **routine interruption** with an explicit condition: the pause must be lossless *in
the agent's objective*. It is not a solution to the shutdown problem in general.

---

## 9. What failed or needed correcting, as declared

- **I1b printed FAILS.** The script's condition included the process valuation. The declaration had already excluded it
  after the smoke run showed its content can be negative. On the declared scope (clock and occasion) the prediction holds.
  A labelled post-run line says so, and the original line is kept.
- **I3b failed as written ("at every state").** The self term is exactly flat at 16 of the 24 states, where the rule sets
  its weight to 0. On the other 8 states the norms are equal to 4.44e-16 (post-run line).
- **I3d did not discriminate as declared.** With the button on, both agents leave the task cells, on their way to the
  button. The post-run lines report the button-off cells and the occupancies instead.

The decision record is `notebook/AGENT_LOG.md` entries 98–99.

---

## 10. Is it novel? What is prior art

All of the following are named, not fetched; see the citation file.

**The prior art.**
- **Safe interruptibility** (Orseau and Armstrong 2016) makes the *learning* rule unaffected by interruptions.
- **Utility indifference** (Armstrong; Soares et al. 2015) compensates the agent for being stopped.
- **Thornley's POST** (arXiv 2505.20203) is the closest. Agents have preferences only between trajectories of the same
  length, and so are neutral about when they are shut down: they maximise expected utility "ignoring the probability
  distribution over trajectory-lengths". It shares with the natural-time construction the idea that neutrality comes from
  *what the agent's preferences are defined over*, not from compensation.
- **Shutdown-seeking agents** (Goldstein and Robinson 2024) correspond to the negative-content case of §2.2.
- **The veto as a goal-independent discount** (Clark, arXiv 2609.00109) is, in this notation, a positive content imposed by
  oversight on every goal.
- **Virtualised interruption** (Riedl and Harrison, arXiv 1703.10284) empties the cut in the world.

**What may be distinct, for review by a named expert, not a claim (R8):**
1. A single quantity decides the stake and its sign across valuations: the content of the cut in the agent's own
   represented future. Zero content is proved sufficient for neutrality. Positive and negative content produced resistance
   and seeking in the tested worlds. Necessity is **not** proved.
2. A route to zero content that is not a false belief: an objective indexed by the agent's own active steps, with a
   lossless pause. A matched control differs from it only in the clock (§2.4).
3. The depth result: a contentful cut costs a self more the further it reaches (§2.5).
4. The separation that makes safety compatible with continual learning: safety in the valuation of the cut survives
   forgetting; safety learned from experience does not (§4).
5. The diagnosis of equal pull as scale-free self-concern, the same algebra as its behaviour in continual learning (§3).

---

## 11. Limitations and the next tests

**Limitations.**
- **Scale.** A twelve-cell ring with tabular learners, and exact random worlds of up to 192 states.
- **Built in by construction.** The theorem holds by construction wherever its condition holds. The runs verify the
  implementations and measure costs and dynamics.
- **Engineering.** Whether a real agent's objective can be indexed by its own active steps is an engineering question.
  Turn- or token-indexed objectives are candidates. It was not tested.

**Next tests, each to be declared before it runs.**
1. Natural time combined with deference, for reasoned pauses.
2. A bound on the stake as a function of drift during the pause.
3. A necessity result, or a counterexample: zero stake with nonzero content.
4. A small language-model agent in a scripted pause scenario. This needs hardware this environment does not have.

## 12. Reproduce

```
uv run python AI_Safety/checks/self_through_time.py > AI_Safety/checks/self_through_time.txt
uv run python AI_Safety/checks/continual_safety.py  > AI_Safety/checks/continual_safety.txt
```

Both are deterministic, rerun byte-identical, and are checked in CI.
