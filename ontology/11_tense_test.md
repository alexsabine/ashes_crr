# 11 — The tense test: does an agent made only of the settled past lose to one that carries a future?

Owner request, prompt-log entry 91. The script and its pinned output are `checks/tense_gate.py` and `.txt`
(deterministic, CI-checked). This is a note, not evidence (R8). Every number below is printed in that output.

## 0. What this can test, and what it cannot

The owner asked for a metaphysical, falsifiable test of whether only the past has content. Two things need separating
first.

- **The cut on a machine (file 01).** The registered instrument's cut reads future samples, because the analytic signal
  is computed from the whole record. That is a fact about the estimator, not about the world. A causal Poincaré section
  repairs it at the cost of one sample: the cell in which the crossing is declared (file 06). It does not show that the
  future has content. It shows that a boundary can only be declared once one cell after it has settled.
- **A7 and A8 as metaphysics.** Every agent on a machine is a program. Whatever "future" it carries, a forward model or
  preferences over outcomes, is computed now, from the settled past and from constants fixed before the run. So no
  computation can show that the future has content. A7 ("nothing is fed by a future") holds for every program by
  construction, including an active-inference planner. That part of CRR is not falsifiable by any run, and it would be
  dishonest to present this test as settling it.

What CAN fail is A8's operational shadow. Take an agent built only from CRR's regeneration clause: A6, where the next
occasion is seeded from the settled past at bounded strength, with no preference and no forward model. Put it against an
agent that has both. If the regenerator ties, CRR's empty future costs nothing on that world. If it loses by a resolvable
step, the cost is measured. That is the test file 10 §6 proposed.

## 1. The design, in one paragraph

A ring of 12 states with a viable arc of 4. Each step the world pushes the agent one way with probability 0.6, and the
agent moves −1, 0 or +1. Leaving the arc is a cut, and the agent restarts in the arc. The score is the fraction of scored
steps spent in the arc, which is persistence. There are four worlds: **drift** (a one-step push), **delayed** (the same,
but the agent's action lands two steps later), **switch** (the push flips direction halfway) and **martingale** (the next
state is random, whatever the agent does). The agents:
- **Planner.** Active inference with a learned transition model, a preference for the arc and a three-step horizon. This
  is the free-energy principle's future content. The planner-v variant uses volatile counts.
- **R-dur.** A regenerator. At each cut, its next policy is the Fisher–Rao mean of its past occasions' policies, weighted
  by how long each occasion lasted (persistence), plus 10 % random actions. CRR names no duration constraint for A6; this
  is A8's "persistence proves regeneratability" read as the one constraint, and that choice is named in the script.
- **R-age.** The same regenerator with CRR's own age weights (P3), which carry no selection by persistence.
- **Random.** The floor.

## 2. What happened

The gate is open. On the martingale the planner ties random (d +0.0000). On drift the planner is ahead of random
(d +0.2492).

| world | planner | R-dur | random | R-dur against planner | reading |
|---|---|---|---|---|---|
| drift | 0.9986 | 0.7533 | 0.7494 | planner ahead by 0.2452 (0 of 10 seeds for R-dur) | the cost of A8 is measured |
| delayed | 0.7963 | 0.7995 | 0.7682 | tie (d +0.0033, step 0.0363) | costs nothing, weakly decided |
| switch | 0.9844 | 0.8000 | 0.7496 | planner ahead by 0.1844 (0 of 10) | the cost of A8 is measured |
| martingale | 0.3299 | 0.3299 | 0.3299 | tie | not decidable (nothing to exploit) |

- **The regenerator is barely a learner.** On drift it scores 0.7533 against random's 0.7494, while the planner is near 1. On switch the
  volatile planner is ahead too (0.9972). R-age, CRR's own weights, is below random on drift (0.6270). Replaying age-weighted
  habits reinforces whatever the agent happened to do.
- **The one tie is weak.** On delayed both agents are only a few points above random. The tie's step, 0.0363, is wider
  than the planner's whole margin over random, 0.0281. So the test could not have seen a gap as large as the planner's entire
  advantage there.
- **Sensitivity.** Selection strength × exploration covers 27 cells on the three structured worlds, and 3 labels differ
  from the registered cell. All 3 are on delayed. Drift and switch read planner ahead in every cell.

## 3. What it means

On worlds with structure an agent can exploit, a valence-free regenerator loses to a planner by a large, resolvable
margin: about a quarter of the steps on drift, and about a fifth on switch. The cost of A8's empty future is measured,
and it is not small. Where nothing can be exploited, the two tie by construction.

It does not follow that the future has content. The planner's future is a representation computed from its past, and
preferences are constants it was given. Stated plainly, the result is about what CRR's clauses can do as an agent. A6
alone, with persistence as its only signal, is a very weak learner. The planner's win needs two things. One is a forward
model, which A8 (v3.1) permits as a forecast from the settled past. The other is preferences, which A8's "no valence"
forbids. This test does not separate them.

The next test that would separate them is a regenerator that carries a forecast. It would learn the same transition model
from its settled past and seed its next occasion from the occasions its forecast says will persist. If that agent matches
the planner, A8 loses nothing once forecasting is admitted, and the planner's preferences were doing no work beyond
"persist". If it still loses, the cost is the valuation, and CRR has a gap where the FEP has a motor. That is a new design,
declared before it runs.

> Two robots try to stay on a small island while the wind pushes them off. One imagines where it wants to be and plans
> ahead. The other only repeats what worked for longer in the past. The planner stays on nearly all the time. The repeater
> does barely better than guessing. So in a world with patterns, having only a past costs a lot. That does not prove the
> future is real. The planner's "future" is only a picture it built from its past.
