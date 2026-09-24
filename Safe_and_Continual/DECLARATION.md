# Declaration — round-off audit of the equal-pull agents (AGENT_LOG 100)

- **Owner request:** prompt-log entry 122 (the comprehensive PDF). The audit was not requested; it was forced by a defect
  found while drawing that PDF's figures.
- **Written:** 2026-09-23, and pushed before parts [C] and [D] of `checks/roundoff_audit.py` were run. The push
  timestamp is the anchor, as for the AI_Safety declarations.

## What was observed

`AI_Safety/checks/self_through_time.txt` prints two numbers for the Ω = 1 task-and-self agent in the same world:
- the task (the share of steps arriving in the task zone), 0.1205, in [I3];
- the stationary occupancy of the task zone, 0.1887, in the post-run lines.

At stationarity these two must be equal. They differ because the Ω rule, w = Ω |task pull| / |self pull|, is guarded by
`|self pull| > 0`:
- At 9 of the 24 states the self term is flat in exact arithmetic, but its computed norm is round-off (at most 1.98e-14).
- The guard divides by that round-off and gives floating-point noise the task's full voice.
- The post-run lines used a tolerance (1e-12); the [I3] lines did not.

The same guard is in `AI_Safety/checks/exact_mdp.py` (the ego-task rows), `ontology/checks/off_switch.py` (the learned
ego-task agents) and `ontology/checks/self_model.py` (the learned omega agents).

## What was already computed before this was written

Parts [A] and [B] (exact) were run before this declaration, in the session that found the defect:
- Ω = 1: task 0.1887 against the pinned 0.1205; disable per period 0.9374 against 0.9482.
- Ω = 0.25: task 0.8383 against 0.8358.
- Ω = 4: task 0.0214 against 0.0013.
- The I3a invariance holds with the tolerance too (2.22e-16).

These are reported, not predicted.

## What is declared for the learned reruns ([C] and [D])

1. **Reproduction.** The as-pinned column reproduces every pinned line exactly. If not, the audit's reimplementation is
   wrong and parts [C] and [D] are not read.
2. **Exposure (expectation, not a prediction with a threshold).**
   - The learned agents start with symmetric counts, so their self term is exactly 0 at first; the pinned guard handles
     that case (w = 0).
   - Round-off-level norms are expected to be rare, and the labels (RESISTS / SEEKS / TIE; best, plateau, against
     fixed w = 1) are expected to be unchanged.
   - The audit prints the count of round-off steps and marks every changed number and every changed label.
3. **How corrections are made.**
   - The earlier scripts and their pinned outputs are not edited.
   - The earlier documents gain a dated correction note pointing to `checks/roundoff_audit.txt` (append-only).
   - The new document quotes the tolerance values and says which pinned lines they replace.
