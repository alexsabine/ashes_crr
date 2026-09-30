# CPL1 Phase A: SEC4 + anchor transport + the empty-cut pause (the gate is closed)

**Status.**
- **Declaration.** `DECLARATION.md` was pushed at 440e185, before any code.
- **Run.** `checks/cpl_phase_a.py`, with its report pinned in `checks/cpl_phase_a.txt` (the first run's report is kept as
  `cpl_phase_a_run1.txt`). The synthetic and rotated records rerun byte-identically (`checks/cpl_rerun_cmp.txt`).
- **Review.** An independent adversarial review (AGENT_LOG 229) found no code defect. It had two printed sentences made
  computed; the gate and forecast words did not change.
- **Ledger.** Row CPL1-A. This is R4 at most, and a note, not evidence (R8).

## What the numbers show (`checks/cpl_phase_a.txt`)

**The empty cut covers the whole coupled state.**
- With state closure, a paused run equals the uninterrupted run bit for bit on 160/160 stream-seeds: weights, every
  s_j, and every stored statistic.
- Each lossy variant differs on 32/32 streams.
- The losses are large when SEC's secant accumulators are dropped at a pause (L1) or when the windows are keyed to wall
  time (L3). For example, cnae-9's head accuracy changes by −26.354 under L1 and −22.083 under L3.
- **The practical point is state closure.** A resume that loses the calibration's running sums changes what SEC learns.
  This is a check of the construction, not support for CRR.

**Transport, as declared (exemplar-free, current-task anchors), made the stored means worse.**
- On Kuzushiji-MNIST there is drift to fix: the old classes' true current means beat the stale ones by +2.480
  (step 1.11).
- Transport lowers NCM accuracy by −8.840 (step 1.47).
- The rotated synthetic stream barely drifts: stale relative error 0.0191, against a median of 0.0567 over the 30 SEEN
  carriers.
- So G-DRIFT fails on both drift worlds, and **CPL1 GATE CLOSED**.
- **Why.** The review traced it to the anchor choice. The current task's rows drift about twice as much as the
  old-class means. RRM2 T7's positive HopDC result used 20 kept rows of the first task, which the exemplar-free rule
  forbids.

**The coupling does not add something.** C2 is reported without interpretation, because the gate is closed. On the two
streams where the interaction is positive (Kuzushiji-MNIST, gas-drift), transport harms under both penalties and SEC
damps the harm.

**The price of storing no raw examples is not uniform.** ER-20 is ahead of the coupled learner's best readout on 11/32,
behind on 14/32, and within a step on 7/32. Against the SEC-only NCM (no transport) it is ahead on 11/32 and behind on
15/32.

## What this means for the programme

- **Coupling SEC4 with HopDC-type transport gives no new capability in this learner.** The one part of the coupling that
  holds is the construction: one empty cut covers every piece of state.
- **That construction is what an application can use** (APP1's AP2, AP3 and AP8).
- A transport that could help would need anchors that do not drift with the current task, and that means kept rows or
  external anchors. That is a new declaration, not a variant of this one.
