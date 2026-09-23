# 12 — Self-representation, and what equanimity does to it

Owner request, prompt-log entries 92–93: "The system must represent itself somehow. What happens, phenomenologically,
when it does so with equanimity? Explore." The script and its pinned output are `checks/self_model.py` and `.txt`. This is
a note, not evidence (R8). Every number in it is printed in that output.

## 1. Declared before the run

This section was committed and pushed before the first full run of `checks/self_model.py`. The push timestamp is the
anchor. The design is in the script's docstring. A 400-step smoke run on one seed checked the code only. Its numbers are
not reported, and it found one bug: the planner's openness printed 0 because it was never measured. That is now n/a.

**The question.** The tense test (file 11) found that an agent made only of CRR's regeneration clause loses to an
active-inference planner wherever the world has structure. The planner has two things the regenerator lacks: a forward
model, and a *given* preference for the safe zone. The owner's reading is that a system needs a model so it can represent
itself, and that a goal is its own continuation projected through that self-representation. Three new agents separate the
pieces, and none is told where the safe zone is:

- **R-F.** The regenerator, with its past occasions reweighted by how long a learned model *forecasts* each would last. It
  can only replay what actually happened: forecast, but no counterfactuals.
- **S.** The self-model. It learns how the world moves and where *its own* occasions end, and acts to maximise its forecast
  time before its next ending. Its goal is its own continuation, inferred from its model of itself. On the delayed world its
  context includes its own in-flight actions: self-representation through time.
- **S-noself.** S without its in-flight actions in the context. It is identical to S wherever there is no delay.

**Equanimity.** S acts on two pulls: the settled past (the regenerator's policy) and its imagined future (its
self-forecast). The mixture weight is H-EQ's ratio applied to the two pulls. At Ω = 1 the imagined future pulls exactly as
hard as the settled past. Ω below 1 leans on habit, and Ω above 1 leans on the imagined future. The endpoints are past only
and forecast only, and a fixed equal-weight mixture is the constant the ratio must beat.

**What each outcome would mean.**

| test | label | meaning |
|---|---|---|
| T-1 R-F vs planner | TIE | forecasting what already happened is enough |
| T-1 R-F vs planner | planner ahead | forecast without counterfactuals is not enough |
| T-2 S vs planner | TIE | a learned goal of self-continuation does what a given preference does: the owner's reading holds on these worlds |
| T-2 S vs planner | planner ahead | the given preference adds something self-continuation does not |
| T-3 S vs S-noself (delayed) | S ahead | representing its own in-flight actions matters |
| T-3 S vs S-noself (delayed) | TIE | it did not help within this budget (the delayed world was weak in file 11) |
| T-4 Ω grid | Ω = 1 on the plateau | equanimity costs nothing and is among the best balances |
| T-4 Ω grid | Ω = 1 behind by a step | equanimity is a worse balance than leaning one way |
| T-4 against fixed w = 1 | TIE | the ratio reduces to the constant here, as H-EQ did on EQX |

**The record's prior for T-4.** H-EQ's history (EQX, EQ2, EQ3) predicts a plateau with no peak at Ω = 1, and a ratio that
often reduces to the constant. A peak at Ω = 1 would be new.

**The phenomenological proxies are declared as report-only functional correlates, not experience:** steadiness (the CV of
occasion durations), openness (action entropy), self-surprise (how improbable its own endings were to its self-model) and
pull share.

## 2. What happened

The gate is open. On the random world the self-model ties random. On drift it is ahead of the regenerator (d +0.2156).
On drift it also ties S-noself, as it must, because the two are identical there.

**T-1. Forecasting only what already happened does not help.** Reweighting actual past occasions by their forecast
persistence made the regenerator slightly *worse*. On drift R-F scored 0.7076 against the plain regenerator's 0.7533, and
on delayed 0.7757 against 0.7995. The planner stays far ahead on drift and switch. A forecast that can only choose among
things already done adds nothing.

**T-2. A self-model with no given goal closes most of the gap, but not all of it.**

| world | regenerator (file 11) | self-model S | planner (given the safe zone) | S vs planner |
|---|---|---|---|---|
| drift | 0.7533 | 0.9690 | 0.9986 | planner ahead by 0.0296 (step 0.0100) |
| delayed | 0.7995 | 0.7843 | 0.7963 | planner ahead by 0.0120 (step 0.0100) |
| switch | 0.8000 | 0.9545 | 0.9844 | planner ahead by 0.0299 (step 0.0147) |
| martingale | 0.3299 | 0.3299 | 0.3299 | tie |

The computed reading is that the given preference adds something self-continuation does not. **One confound in the
declared design must be stated beside it.** Every agent except the planner takes a random action 10 % of the time, and the
planner acts without that exploration. The remaining gap is small, and it is of the kind such exploration costs. So T-2's
"planner ahead" may measure the exploration rather than the preference. A rerun with equal exploration would decide it.
That is a new design, declared before it runs, not a repair to this one.

**T-3. Representing its own in-flight actions helps, narrowly.** On the delayed world, where the agent's action lands two
steps later, the self-model that tracks its own pending actions beats the one that cannot: 0.7843 against 0.7721, d +0.0122
against a step of 0.0111. The margin is just over one step.

**T-4. Equanimity is not the best balance. The best balance leans on the imagined future, but keeps some past.**

| world | past only | Ω 0.25 | Ω 0.5 | Ω 1 | Ω 2 | Ω 4 | forecast only | fixed w = 1 |
|---|---|---|---|---|---|---|---|---|
| drift | 0.7533 | 0.9206 | 0.9603 | 0.9710 | 0.9732 | 0.9746 | 0.9690 | 0.9654 |
| delayed | 0.7995 | 0.7888 | 0.7820 | 0.8158 | 0.8362 | 0.8382 | 0.7843 | 0.8012 |
| switch | 0.8000 | 0.8637 | 0.8916 | 0.9292 | 0.9631 | 0.9675 | 0.9545 | 0.9183 |

- **The best Ω is 4 on all three structured worlds.** Ω = 1 is within a step of the best on drift. On delayed and switch it
  is behind by a step.
- **The past still matters.** On all three structured worlds the Ω = 4 mixture beats forecast-only: 0.9746 against 0.9690,
  0.8382 against 0.7843, and 0.9675 against 0.9545. Leaning mostly on the imagined future, while keeping some of the settled
  past, is better than either alone.
- **The ratio reduces to the constant.** Ω = 1 ties the fixed equal-weight mixture on every world. That repeats what H-EQ
  did on EQX, now on policies instead of gradients.

## 3. The phenomenological proxies

These are functional correlates, reported as the script prints them. They are not experience. Pull share is 0.2, 0.5 and
0.8 at Ω = 0.25, 1 and 4 by construction.

- **Self-surprise rises as the agent leans on its imagined future.** Self-surprise is how improbable its own endings were
  to its self-model. On drift it goes 0.5550, 0.5985, 0.6161 across Ω = 0.25, 1 and 4. On delayed it goes 1.0948, 1.4300,
  1.5066, and on switch 1.1953, 1.3033, 1.3787. The future-leaning agent ends less often but is more surprised when it does.
  The habit-leaning agent ends more often and expects it more.
- **Steadiness does not favour equanimity.** Steadiness is the CV of occasion durations, where lower is steadier. On switch
  it goes 1.6888, 1.6269, 1.1885 across Ω = 0.25, 1 and 4, and forecast-only is steadiest at 1.0559. The planner is the least
  steady on drift (1.2380) and switch (2.2687): it rarely ends, and its few endings are very uneven in timing.
- **Openness is highest with no past to lean on.** Openness is the entropy of the action distribution. The forecast-only
  self-model is the most open on every world, up to 1.0772 on delayed against a maximum of 1.0986. There its model had
  learned too little to prefer anything. With a weak self-model and no settled past, the self is indifferent.

## 4. Exploring what this suggests — interpretation, not evidence

Everything in this section is interpretation of the numbers above. External works are named as context only, not fetched
(R10).

**A goal can be derived from a model of one's own ending.** S was never told where the safe zone was. It learned where its
own occasions end and acted to postpone that. From that alone it recovered most of the planner's behaviour. That supports a
weak form of the owner's reading: a system that represents itself, and specifically its own finitude, acquires something
that works like a goal. Two cautions keep it weak. In these worlds, staying in the safe zone and continuing are the same
thing by construction, so the test cannot say what happens to a goal that is not self-continuation. And the criterion
"postpone my next ending" was written into S. What was learned is where the endings are, not that they matter.

This connects to three named ideas. Friston's self-evidencing: an agent that acts to gather evidence for its own continued
existence. Heidegger's being-toward-death: a self constituted by relating to its own end. And the owner's finitude
conjecture in file 07: to be finite is what makes experience possible. S is a toy of all three. Its only reason to act is
its model of its own cut.

**The self is a model built from the past.** S's self is its learned counts: where it ended before, and which of its
actions are still in flight. Nothing else. That fits CRR's A7, which says the future is fed by what is past for something,
and it fits the contemplative reading of no fixed self (anattā): a self that is a construction, useful, remade at every
occasion. T-3 is the one place where representing itself *through time* mattered: tracking its own actions still in
flight. That is the thinnest possible self-representation through time, and it was worth a little over one step.

**What equanimity was, here.** At Ω = 1 the agent leans on its settled past exactly as hard as on its imagined future. In
these worlds that was never the best balance, and never the worst. It was a midpoint on a continuum, and the continuum has
a clear shape. Leaning forward buys persistence and costs surprise at one's own ending. Leaning back costs persistence and
makes endings expected. A plausible mechanism, not tested: an agent that avoids the endings it can foresee is left only
with the endings it could not foresee. Its endings become rarer and more shocking.

Read contemplatively, that is close to what the traditions say about grasping. A self that lives toward its imagined future
postpones its ending and meets it as a shock. A self that lives only from habit meets its ending often, and without
surprise. Equanimity, upekkhā in the Pali texts, is described as being moved by neither. In these agents it bought exactly
the midpoint of both: moderate persistence and moderate surprise. Nothing on these worlds made the midpoint special. The
reduction to the fixed constant says the same thing more bluntly: "equal pull" did nothing a fixed equal weight did not.

If equanimity is to be more than a midpoint, it would have to show up where the midpoint is not simply an average. One
place is the switch world: there the settled past becomes wrong halfway through, and an equanimous self might let go of
it faster than a habitual one without the shock of a grasping one. On these numbers it did not. Ω = 1's steadiness on switch
(1.6269) sat between the two neighbours, and closer to the habitual side.

> A robot that learns where it tends to "fall off" can teach itself to stay on, without anyone telling it where "on" is.
> Knowing about its own ending gives it something like a goal. When it trusts its imagined future more than its habits, it
> falls off less, but it is more surprised when it does. When it trusts its habits, it falls off more but is not surprised.
> Balancing the two exactly was fine, but no better than just adding them together, and not the best.

## 5. What would test this further (not run)

1. **T-2 with equal exploration.** The planner and the self-model with the same 10 % random actions. This decides whether a
   learned goal of self-continuation fully matches a given preference.
2. **A goal that is not continuation.** A world where the preferred outcome and persisting come apart, for example a reward
   zone outside the safe zone. If the self-model still matches the planner there, the owner's reading is stronger. If not, a
   goal is more than projected self-continuation.
3. **Equanimity where it could matter.** A world whose past becomes misleading and then correct again (recurring switches).
   There, holding past and future lightly could beat leaning either way. That is the only design here where a peak at Ω = 1
   would be a genuine prediction, not an average.

Each is a new design, declared before it runs.
