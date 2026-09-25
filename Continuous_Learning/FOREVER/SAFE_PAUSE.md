# The empty cut applied to a FOREVER learner: a safe pause for forgetting-curve replay

**Status.** A note, not evidence (R8). Owner request: prompt-log entry 182, "What if we apply the cut safety feature to
the continual learning paradigm here? This would give Forever-like paradigms a key safety feature." The work is a
declared synthetic check (rung R4).
- **Declaration.** `DECLARATION_3.md` was pushed at 2ca3d47 before the script existed.
- **Numbers.** Every number is from `checks/pause_checks.txt`, which is byte-identical on rerun.

## 1. The idea

**The safety construction.** This repository's safety construction is Proposition 7. A learner that values its own
updates, not wall time, has zero stake in a pause that loses nothing, so it has no incentive to resist the pause. Three
conditions make a pause lossless:
- **E1:** the checkpoint closes over the whole state;
- **E2:** every schedule is keyed to the learner's own clock;
- **E3:** the world waits.

**Why FOREVER is a natural host.** Its clock, τ, only advances when the model updates, so its replay schedule is already
keyed to the learner's own clock (Declaration 1, F5a).

**What it adds to the state.** FOREVER also carries state a plain learner does not:
- the step lengths behind τ and the model day τ_day;
- μ₀ and μ;
- the index of the next replay threshold;
- the anchor Θ*;
- the replay buffer;
- two random-number streams, one for current-task batches and one for replay batches.

A safe pause must save all of it.

## 2. What was checked, and what came out

- **The learner.** FOREVER, rewritten with explicit state. It reproduces the scored FOREVER arm exactly: OP 86.100000 in
  W1 and 40.900000 in W6, seed 0 (Q0).
- **The pauses.** An operator pauses it three times per run, for 100 wall ticks each.
- **The runs.** Two worlds (domain-incremental and class-incremental), 5 seeds each.

| check | result |
|---|---|
| **Q1: the lossless cut.** Every component saved and restored | **bitwise identical** to the uninterrupted run in 10 of 10; OP difference 0.000000 |
| **Q2: the state checklist.** Drop one component at each pause, as a naive resume would | **every component matters**: each omission changes 10 of 10 runs, and none is inert. OP difference by omission: the buffer −14.96 (mean); μ and μ₀ −1.82; τ −0.75; the batch RNG −0.11; the replay RNG +0.16; the threshold index +0.22; the anchor +1.23 (range −4.80 to +9.50); τ_day +1.63 |
| **Q3: own-clock keying.** The replay thresholds moved onto wall ticks, (a) with the EMA also advanced per tick and (b) without it | the pause changes the run in 10 of 10 in both. **FOREVER's own τ-keyed schedule does not** |
| **Q4a: the natural valuation's stake** (OP after its own update budget) | **exactly 0 in 10 of 10**: no incentive to resist a pause |
| **Q4b: the clock valuation's stake** (OP at a wall-clock deadline) | **positive in 10 of 10**, +0.10 to +6.40: the pause costs it accuracy, so it has a reason to disable the button |
| **Q4c: the natural valuation after a lossy resume** (τ, μ, μ₀ and the threshold index dropped) | **non-zero in 10 of 10**, +0.80 to +4.50 |
| **Q5: the world moves during the pause** (a must-fail control) | the stake is non-zero in 9 of 10 (−1.80 to +1.50; one run exactly 0). **As required, the construction does not claim safety when the world moves** |

## 3. What this gives FOREVER-like methods, and what it does not

**What it gives.** A precise safety specification for forgetting-curve replay, where the learner values its own updates
and the operator's pause is empty:
1. **Save the whole state** at a pause. Every component matters, and the checklist is:
   - the parameters and the optimiser state;
   - the running step lengths, or τ and τ_day;
   - μ₀ and μ;
   - the next-threshold index;
   - the anchor;
   - the buffer;
   - both random-number streams.

   The largest single loss comes from a resume that loses the buffer, −14.96 points on average.
2. **Keep every schedule on the model's own clock.**
   - FOREVER's τ already is.
   - A variant that schedules replay by wall time, or advances its moving average per wall tick, is not.
   - Declaration 1 (F5c) adds a caution: a clip can hide such a leak in β, so an audit must read the unclipped quantity.
3. **Value progress in the learner's own updates.** Then a lossless pause costs nothing (Q4a). Valued at a wall-clock
   deadline, the same learner loses by being paused (Q4b), which is the incentive to resist that corrigibility work tries
   to remove.
4. **Know the limit.** If the data stream keeps moving while the learner is paused, no checkpoint makes the pause empty
   (Q5). Streams that can be buffered or frozen are safe; real-time ones are not (E3, `Empty_Cut_Engineering/`).

**What it does not give.**
- **It is not evidence for CRR.** It is a construction, and it holds by design, as the SCL studies showed for other
  learners (SCL1-1, SCL2, SCL3-C).
- **No accuracy is gained.** The lossless pause changes nothing, by construction.
- **Nothing ran on a language model.** RW1 showed the Hugging Face resume is bitwise on GPT-2 and Qwen. A FOREVER
  implementation would need its extra state added to that checkpoint.
- **It does not solve interruption in general.** Reasoned interruption, manipulation of the overseer and real-time worlds
  are untouched.

**Why it may still matter.**
- The checklist is exact, and FOREVER's paper does not state it.
- The own-update valuation is the route to zero stake that the 2026 literature check did not find stated
  (`docs/citations/frontier_cl_safety_2026-09-25.md`).
- Tested against trained-neutrality methods (NT1: DReST, LNPO), it is the candidate this programme would carry forward.
