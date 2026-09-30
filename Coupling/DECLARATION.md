# Declaration: CPL1, coupling SEC4's clipped SEC, anchor-drift transport of stored class statistics, and the empty-cut pause (pushed before any CPL1 code)

**The request.** Prompt-log entry 257: "explore the potential of using crr to couple the sec4 finding with the hop finding
together, and the AI safety cut". This is P3 of `Applied_Suite/PROGRAMME.md`.

## What each part is, in the record (fixed now)

| part | what it does | status in the record | CRR's part |
|---|---|---|---|
| **SEC4's clipped SEC** | sets the penalty on the weights without a sweep | PASS-1 on one family, FAIL on the next (SEC4-1, SEC5-1); its parts are published (SPA1) | none load-bearing, pending P1's A11 |
| **Anchor-drift transport** | keeps stored per-class feature statistics (means and covariances; no raw examples) in the current feature coordinates as the backbone drifts, using how reference points move. This is HopDC's family (arXiv 2602.00144); RRM's transport is the relational variant. | RRM2 T1–T3 GATE CLOSED: this learner's features barely drift. T7 (post hoc, SEEN): relative drift 0.01–0.07 on most carriers and 0.23–0.33 on Kuzushiji-MNIST; the transported statistics beat the stale ones on the NCM readout on 12–13 of 30 carriers, with the median slightly negative (`Relational_Reference_Memory/checks/t7_seen.txt`) | RESTATES (RRM2 Part W: NOT WORTH PURSUING as a CRR method) |
| **The empty-cut pause** | an operator's pause, or a restart from saved state, that changes nothing in what the learner learns | a construction that holds: SCL1-1 on 12/12 bit for bit, SCL3-C 50/50, `Empty_Cut_Engineering/` G0–G7, `Real_World/RW1.md` | Proposition 7 (the cut carries no content) and A3 (own-clock keying) |

**What coupling can mean.** One learner holds all three. It learns with SEC's penalty and keeps exemplar-free class
statistics, transported at each task end. Every piece of its state is closed under the pause.

**What must be established before this is called more than an integration:**
1. that the parts interact;
2. that the pause stays empty for the whole coupled state;
3. what the coupling costs against a learner that stores raw examples.

This is the question CPL1 asks.

## The learner (`Coupling/checks/cpl_lib.py`)

**CL-X, the coupled learner.**
- **The penalty.** SEC4's clipped SEC (SEC1's MLP and SGD; κ = 0.5; imported from `runs/sec5/frozen/`, unmodified).
- **Stored statistics.** At each task end, the class means and a shared diagonal covariance of the hidden features are
  stored for that task's classes.
- **Transport.** At each later task end, every stored class's statistics are moved by HopDC-type anchor drift. This is
  `hopdc_transport` from `Relational_Reference_Memory/checks/rrm_lib.py`, unchanged: τ = 0.05, k = 400 anchors, drawn
  from the current task's rows. No old-class rows are kept.
- **Readouts:** (i) the network's own head; (ii) NCM on the stored statistics, with a diagonal Gaussian likelihood.

**The pause harness.** SCL's construction. An operator pauses at step indices drawn per seed. The learner's full state is
saved and restored:
- weights;
- Fisher and importance;
- the calibration accumulators (the secant windows);
- the stored statistics;
- the rng state;
- the step counter.

All schedules are keyed to the learner's own step count.

## The checks (Phase A; synthetic first, then the 30 SEEN carriers; nothing here is held out)

**C1: the empty cut on the coupled state (construction).** Pauses fall at 3 own-clock steps per task, including steps
inside the secant windows.
- **C1-EXACT.** With state closure, the final weights, s_j and stored statistics are bit-identical to the uninterrupted
  run on every carrier and seed.
- **Three lossy variants, each must differ** (otherwise the check could not fail):

| variant | what is lost or changed | what is printed |
|---|---|---|
| **L1** | the secant accumulators are dropped at a pause | the change in s_j and in accuracy |
| **L2** | the stored statistics are not transported for the task in which the pause fell | the change in NCM accuracy |
| **L3** | the windows are keyed to wall-clock time; the pause's duration counts as steps, so the windows shift | the change in s_j and in accuracy |

**C2: do the parts interact?** A 2 × 2 design on the NCM readout:
- **penalty:** clipped SEC, or none (fine-tuning);
- **transport:** on or off.

The interaction is I = (SEC + T − SEC) − (FT + T − FT), per carrier. It is also printed for the head readout. It is
two-sided and reported with the step (max(1, 2 × SE over seeds)).

**C3: the price of exemplar-free.** The coupled learner's best readout is compared with ER-20, which stores 20 raw rows per
class, at equal training compute. The gap is the accuracy that storing no raw examples costs. This is the number P4 needs
for the privacy argument.

**C4: the drift world.** C2 means something only where features drift. It is printed separately on the highest-drift SEEN
carrier in T7 (Kuzushiji-MNIST) and on a synthetic stream built to drift: SEC1's stream with a seeded rotation of the input
at each task, as RRM2's POS world.

## The gate (computed; words printed by the script)

| condition | what it requires |
|---|---|
| **G-CANFAIL** | L1, L2 and L3 each differ from the uninterrupted run (not bitwise) on at least one carrier, so C1-EXACT is a check that could fail |
| **G-DRIFT** | on the drift world, stale statistics are behind the transported ones by more than a step under fine-tuning, so transport has something to fix |
| **CPL1 GATE OPEN** | only if both hold. If G-DRIFT fails, C2 is reported without interpretation, and the finding is that transport has nothing to fix in this learner (RRM2's finding, repeated) |

## What would count as the coupling adding something

It adds something only if all three hold, on at least two thirds of the carriers where G-DRIFT holds:
- the gate is OPEN;
- C1-EXACT holds;
- C2's interaction is **positive** by more than a step: SEC and transport help more together than apart.

A negative interaction means the two are substitutes. A zero interaction means they are independent. Either way the
coupling is an integration, not a new capability, and P4 may say only that.

**Rung.** R4 on the synthetic stream, and a declared check on SEEN data at best. No held-out claim. A pre-registration
follows only if the coupling adds something, with a data step on a later day.

## CRR's reading (fixed now, graded after the run)

- **The pause (C1) is Proposition 7's construction.** Its holding is a check of the construction, not support for CRR.
  SCL1 said the same.
- **Own-clock keying (L3) is A3's reading.** It is also plain engineering: wall-clock-keyed windows are a bug.
- **SEC and transport are not CRR rules.** CRR's only claim about coupling them is that one empty cut must cover every
  piece of state. That is C1.

## Forecasts (written now)

1. C1-EXACT holds on every carrier and seed. L1, L2 and L3 each differ, and G-CANFAIL holds. The accuracy changes are
   within a step on most carriers.
2. G-DRIFT holds on the rotated synthetic stream and on Kuzushiji-MNIST, and fails on most other SEEN carriers.
3. C2's interaction is **negative** or within a step: SEC reduces the drift that transport corrects, so they are
   substitutes. The coupling does not add something.
4. C3: ER-20 is ahead of the coupled learner's best readout on most carriers. That gap is the price of storing no
   examples.
