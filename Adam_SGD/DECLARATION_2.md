# Declaration 2 — the drifting-world battery (committed and pushed before its first full run)

Owner request, prompt-log entry 107. The anchor is the push timestamp of the commit that adds this file. The files are:
- `Adam_SGD/checks/drift_battery.py`, the battery;
- `Adam_SGD/checks/engine.py`, the batched engine;
- `Adam_SGD/checks/common.py`, shared code.

The docstrings hold every constant.

**What was seen before this commit.** Three things, stated for the auditor:
- A 2-seed check during development that the engine reproduces `common.run`. The final objectives agreed to 1e-15; this
  repeats as [E0].
- A timing check.
- A smoke run on thinned grids (two seeds), whose output was discarded unread.

## What the assumption audit changed (`checks/assumptions.txt`, pinned before this design)

1. **The earlier verdict depended on one reading of the scale.** "A finely tuned constant beats the rule wherever the
   scales differ" (`adam_checks_3.txt`) held under the 'imp' reading (the scale is true importance) and at a fixed
   learning rate.
   - Under a pure units error (AS3), the rule is exactly invariant: spread 0.000e+00 across scales.
   - Unsmoothed, the rule ties a constant retuned at every scale: 1.014 to 1.022.
   - A constant not retuned diverges at c ≥ 16.
   - With the learning rate tuned (AS5), the rule and the in-principle weight λ = 1 tie exactly under 'imp': 3.4346
     against 3.4347 at c = 16.
2. **The registered smoothing (EMA 0.9) is the rule's weak point.** It costs 1.368 to 1.379 against the retuned constant
   under a pure units error (AS3).
3. **Ratio rules fail when the past gradient is mostly noise.** They are 3.046 to 3.779 behind at c = 1/16 with unscaled
   noise (AS3b).
4. **Five seeds are too few.** The registered rule scored 3.4789 on seeds 0–4 and 4.6284 on seeds 5–9 (AS4).

So this battery does the following:
- reads the scale as a units error, with the noise scaled with the units, except in one declared low-signal world;
- tunes the learning rate for every arm;
- tunes on 10 seeds and scores on 10 held-out seeds;
- uses a weight grid from 1e-5 to 1e3 (the audit's grid stopped at 10, below the right weight 16 at c = 1/16);
- reports the registered rule and the unsmoothed ratio rule separately.

## Why this is the fair test

On a stationary problem an adaptive weight settles to a constant, so it can at best tie a well-tuned one (`adam_checks_3.txt`
B4; AS3). The rule's claim is about worlds where the right weight moves. The battery builds two worlds for the gate, and
then four worlds where the weight moves for the reasons continual learning actually faces.

| world | what moves | expected | why |
|---|---|---|---|
| G-STAT | nothing (c = 16) | ratio rule TIE, registered BEHIND; neither AHEAD (**gate: must not read AHEAD**) | AS3 |
| G-DRIFT | the units drift 4096-fold over the run | ratio rule AHEAD (**gate: must read AHEAD**); registered open | a constant is right at one moment only; the rule is invariant |
| T0 | the units wander (log-OU, sd 1.5) | open; AHEAD if the wander is large enough | the same mechanism, not monotone |
| T1 | eight tasks, calibrated Fishers, so importance accumulates | **BEHIND** | λ = 1 is exact Bayes here; equal pull ignores that the past now holds several tasks |
| T2 | eight tasks, each Fisher miscalibrated by a factor in [1/16, 16] | open | drifting units favour the rule; accumulating importance favours the constant |
| T3 | T0 with a low-signal past gradient | **BEHIND** | AS3b's failure mode |

**Optimisers.**
- Plain SGD runs everywhere.
- On T0 and T2 three more optimisers run: heavy-ball momentum, coupled Adam, and decoupled Adam (past pull outside the
  preconditioner).
- Expected under coupled Adam: open. Adam normalises the whole step, not each term, so a drift in one term's units still
  changes the balance.
- Expected under momentum and decoupled Adam: as SGD.

**The oracle.** An oracle that knows the units (λ/c_t, or the calibrated Fishers) is printed as the ceiling for SGD.

**The gate.** Both the ratio and the registered rule must not read AHEAD on G-STAT, and the ratio rule must read AHEAD on
G-DRIFT. Otherwise the gate is closed: the rule has no niche even by construction, and by R12 nothing further is run on
this operationalisation.

**Sensitivity.** On T0 and T2 under SGD the grid is Ω ∈ {0.71, 1, 1.41} × noise ∈ {0.1, 0.5, 1.0}, with everything
retuned in each cell. A label that flips in more than one of the 8 non-main cells is FRAGILE.

## What the outcomes mean

- **Gate open; T0 or T2 AHEAD under SGD, momentum or decoupled Adam; T1 and T3 BEHIND.** Then the rule has a specific,
  honest niche: continual training where the penalty's units drift or are miscalibrated, under SGD-family or decoupled
  optimisers, with an adequate signal in the past gradient. It does not help where the penalty is calibrated and
  importance accumulates.
  - If only the ratio rule (smoothing 0) wins, the advantage belongs to the gradient-ratio family, which includes prior
    art. The registered smoothing then needs replacing in any later prereg (a new rule, R3).
  - Real data would come next, on a later day: carriers with deliberately miscalibrated or drifting Fisher scales, under a
    fresh prereg and a gate.
- **Gate open, but every test TIE or BEHIND.** The niche exists only by construction, and the realistic worlds do not
  supply it.
- **Gate closed.** The equanimity rule has no advantage even where the right weight moves by construction, and the ledger
  and write-up say so.

In every case the result is reported as it falls, with per-seed win counts beside every mean (R6).
