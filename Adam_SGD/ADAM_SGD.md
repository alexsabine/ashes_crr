# The equanimity rule under SGD and Adam: the assumptions re-checked, and the test where the right weight moves

**Status.** This is a note, not evidence (R8). It was written on 2026-09-23 at the owner's request (prompt-log entry 107):
"Make a new folder for Adam/SGD and ensure our synthetic data checks build on lessons learned so far. Double check any
prior assumptions regarding the value of a fixed parameter before proceeding."

**Sources.** Every number below is printed by a pinned script in `Adam_SGD/checks/`:
- `assumptions.txt` (Declaration 1);
- `drift_battery.txt` (Declaration 2);
- `drift_battery_2.txt` (Declaration 3, **post hoc**);
- `mechanism.txt` (Declaration 4).

Each declaration was pushed before its run. Everything here is synthetic: rung R4, not a ledger row.

> In plain words. We went back and checked the rules of the game we had been using to judge the balancing rule. Two of
> them were unfair. Then we gave the rule the test it was built for: a world where the right balance keeps changing. In
> that world, if the old and new lessons are about equally "noisy", the rule does as well as a cheat who knows the answer,
> and beats every fixed setting. When lots of old lessons pile up, it does worse than a fixed setting. And part of why it
> works turned out to be luck about the noise.

## 1. The assumptions, re-checked (Declaration 1)

The earlier Adam checks concluded that "a finely tuned constant beats the rule wherever the scales differ". That
conclusion rested on four choices, now tested.

1. **The objective depends on what the scale c means.**
   - If c is the old task's true importance (the 'imp' reading), the right fixed weight is λ = 1.
   - If c is a units error the learner cannot see (the 'unit' reading), for example a miscalibrated Fisher estimate, the
     right weight is 1/c.
   - Both hold exactly: AS1 found the argmin at 0.9966 and at 1/c within 0.4 %.
   - The earlier checks used the 'imp' reading (AS2 reproduces them exactly: 9.7260174112 both ways). Units errors are
     real in this repository's own data: the tuned EWC λ spans 100.00× across the EQ4 carriers and 1410.00× across the
     EQ3 carriers (EQ4-0, EQ3-0).
2. **Under a pure units error the rule is exactly invariant.**
   - Its score was identical at every scale; the relative spread was 0.000e+00 (AS3).
   - Without smoothing it tied a constant retuned at every scale (1.014 to 1.022).
   - A constant tuned at one scale and used at another diverged at c ≥ 16.
   - The registered smoothing (EMA 0.9) cost 1.368 to 1.379.
3. **The step size is a fixed parameter too.** With the learning rate tuned for every arm, the rule and λ = 1 tied exactly:
   3.4346 against 3.4347 at c = 16 (AS5). The earlier "behind" verdict came from a learning rate too large for the
   stiffer term, not from the weight.
4. **Two warnings.**
   - When the old task's gradient is mostly noise, ratio rules fail: 3.046 to 3.779 behind (AS3b).
   - Five seeds are too few: the registered rule scored 3.4789 on one seed set and 4.6284 on another (AS4).

> In plain words. We had been judging the rule by the wrong scoreboard, with a stopwatch set too fast. When the "scale"
> is just a mistake in units, the rule copes perfectly without being told; a fixed setting has to be re-chosen by hand
> every time. And once everyone may pick their own speed, the rule and the best fixed setting come out level.

## 2. The drifting worlds (Declarations 2 and 3)

**Declaration 2** (declared in advance) closed its gate, but on an instrument defect.
- In the must-win world, even the oracle that knows the units was only 0.977 of the best constant. The constant scored
  3.3545 against the oracle's 3.2775, so no method could clear the 0.9 threshold.
- The ratio rule (smoothing 0) equalled the oracle (1.000) and beat the constant on 10 of 10 held-out seeds, but it could
  not read AHEAD.

**Declaration 3** (a post-hoc redesign) made two changes, both stated in advance of its run: a headroom precondition, and
grids widened in both directions with edge flags. Its results:

| world | what moves | ratio rule (smoothing 0) / best constant | registered rule (0.9) | seeds ahead | note |
|---|---|---|---|---|---|
| G-STAT2 | nothing | 1.000 TIE | 1.036 TIE | 3/10 | stationary: the rule reduces to a constant |
| G-DRIFT2 (gate) | units drift 4096-fold | **0.898 AHEAD** | 1.008 TIE | 10/10 | headroom 0.896; GATE OPEN, narrowly, post hoc |
| T0′, SGD | units wander | **0.862 AHEAD** | 0.916 TIE | 10/10 | ratio / oracle 1.002 |
| T0′, momentum | same | **0.860 AHEAD** | 0.907 TIE | 10/10 | |
| T0′, coupled Adam | same | **0.829 AHEAD** | 0.897 AHEAD | 10/10 | Adam does not remove a drift between two terms |
| T0′, decoupled Adam | same | 0.902 TIE | 0.916 TIE | 10/10 | |
| T1, SGD | eight calibrated tasks | 1.137 BEHIND | 1.123 BEHIND | 0/10 | λ = 1 is exact Bayes; equal pull ignores the accumulated past |
| T2, SGD | eight miscalibrated tasks | 1.056 TIE | 1.108 BEHIND | 1/10 | the oracle's headroom is only 0.928 |
| T3′, SGD | low-signal past | 0.966 TIE | 0.996 TIE | 6/10 | headroom 0.882; the rule fails to take it |

**Sensitivity.** T0′ is FRAGILE: the ratio rule's label flips in 6 of 8 cells. It wins at Ω = 1, ties at Ω = 0.71, and ties
or trails at Ω = 1.41. T2 is FRAGILE too. Several of the rule's chosen learning rates on T2 sit at the top of the grid.

> In plain words. We built a world where the right balance keeps moving, and made sure there was room to win. The rule
> without its smoothing matched the cheat who knows the answer and beat the best fixed setting every time. That held for
> plain training, training with momentum, and Adam. But it only worked with the dial at exactly 1. And in the more
> realistic setting, where the machine learns eight subjects one after another, the rule was worse than a fixed setting.

## 3. Why it wins, and the limit on that (Declaration 4)

At the balance point the real pulls from the two tasks cancel. What is left is noise, so the unsmoothed ratio partly
measures how noisy each gradient is.

When the past gradient was made r times noisier than the present one:
- **The rule's effective weight moved with r.**

  | r | 0.25 | 0.5 | 1 | 2 | 4 |
  |---|---|---|---|---|---|
  | effective weight | 2.238 | 1.738 | 0.970 | 0.637 | 0.428 |

  The declared test M1, "tracks 1/r within 25 %", **fails**: the weight moves in the predicted direction, but less than
  in proportion.
- **The rule read AHEAD only at equal noise** (M2 holds). At r = 0.5 and 2 it still beat the constant on 10 of 10 seeds,
  but by 0.936 and 0.927, which read TIE.
- **With a noise-free past it tied** (1.024).

So the rule's best case needs the two gradients to be about equally noisy. Its advantage fades as they differ. It fades
gradually, not all at once.

> In plain words. Part of the trick is luck. The rule balances the "wobble" of the two lessons as well as their real
> pull. When both lessons wobble equally, balancing the wobble happens to give the right answer. When one wobbles more,
> the rule leans the wrong way, though it still does a bit better than a fixed setting.

## 4. What this means for the equanimity idea

**It is not dead.** On synthetic worlds where the old term's units drift during training, the rule without its smoothing
does two things:
- it matches an oracle that knows the units;
- it beats the best tuned fixed weight on every held-out seed under SGD, momentum and coupled Adam.

A fixed weight cannot do that without being re-tuned by hand as the units move.

**Its niche is narrow, and the record now says where.**
1. **Drop the registered smoothing.** Smoothing 0.9 trailed the unsmoothed rule in every world except T1, and missed the gate (1.008). It read AHEAD only once, under coupled Adam in T0′ (0.897). A different smoothing is a new rule,
   and any real-data study would need a fresh prereg (R3).
2. **It works for balancing two terms whose units drift.** It does not work for many accumulating tasks. With eight
   calibrated tasks, equal pull loses to λ = 1 (T1), because equal pull ignores that the past now holds several tasks.
3. **Its balance is partly set by noise.** It is best when the present and past gradients are about equally noisy, and
   weaker as they differ (Declaration 4).
4. **The evidence is post hoc and fragile.** The gate opened on a redesign, by 0.898 against a 0.9 threshold, and T0′
   flips in 6 of 8 sensitivity cells.

**Two possible next steps, neither run here.** Both are new hypotheses in CRR terms, to be declared and gated separately if
the owner chooses.
- **Scale Ω with the number of settled occasions.** For many tasks, the past's weight would grow with the tasks it holds
  (T1's lesson).
- **Balance the signal, not the noise.** Compare denoised pulls away from the balance point, which is Declaration 4's
  lesson.

## 5. Corrections to earlier notes

`Continuous_Learning/ADAM_AND_PRIOR_ART.md` and `FRONTIER_BOTTLENECKS.md` said that a finely tuned constant beats the rule
"wherever the scales differ". That holds only in a narrow setting: the 'imp' reading, at a fixed learning rate, with a
constant tuned on the seeds it was scored on.
- Under a units error, the unsmoothed rule ties a constant retuned at every scale, without retuning.
- In a world whose units drift, it beats every fixed constant (post hoc, fragile).

Those notes now carry a dated addendum pointing here. Their pinned outputs are unchanged.

## 6. Reproduce

```
uv run python Adam_SGD/checks/assumptions.py   > Adam_SGD/checks/assumptions.txt
uv run python Adam_SGD/checks/drift_battery.py > Adam_SGD/checks/drift_battery.txt
uv run python Adam_SGD/checks/drift_battery_2.py > Adam_SGD/checks/drift_battery_2.txt
uv run python Adam_SGD/checks/mechanism.py     > Adam_SGD/checks/mechanism.txt
```
All four scripts are deterministic and CI-checked.

## Addendum (prompt-log entry 109): the "let Ω grow" idea, corrected against the paper's own mathematics

§4 named "scale Ω with the number of settled occasions" as a possible next step. Read against
`Continuous_Learning/CONTINUOUS_LEARNING.md` §4.1–4.2, that idea is wrong as stated.
- **The knife edge.** With exact gradients, the rule's update on the Pareto curve is (1 − Ω)·g_p. At Ω = 1 every point of
  the curve is a resting point. At any Ω > 1 no point is: the learner slides all the way to the old optimum b.
- **So Ω = 2, 3, … does not give the past two or three votes.** It gives the past every vote, and the present task stops
  being learned.
- **Why noise hides this, and why that is not a fix.** With noise and smoothing the edge blurs into a plateau (§4.5), and
  there Ω acts roughly like a multiplier on the effective weight (`checks/drift_battery_2.txt`: T0′ at Ω = 1.41 trails or
  ties). A growing Ω would then work only in a noise-dominated regime. That is the fragility the record already warns
  about.

**Where the problem actually sits.** In online EWC the penalty's Fisher is a running sum, F ← F + F_t (paper §2.2). So its
size carries two things at once: the units of the Fisher estimate, and how many tasks the past holds. The rule divides by
‖ĝ_q‖, so it cancels both. Cancelling the units is its real strength (`checks/assumptions.txt` AS3). Cancelling the count
is its weakness: T1, where λ = 1 on the accumulated sum is exact Bayes (paper §4.3), put the rule behind (1.137).

**A coherent version, for the owner's decision; untested, and it would need its own declaration and gate.**
- Apply the equal-pull normalisation to each task's Fisher once, at its boundary, to strip that task's units.
- Accumulate the unit-free contributions with CRR's age weights (P3), q^age, so the sum is bounded as A6 requires.
- Keep a fixed weight on the result.

In short: equanimity within each task (units) and counting across tasks (Bayes, bounded). With q = 0 the method keeps only
the latest task; with q → 1 it counts every task, as Bayes does.
