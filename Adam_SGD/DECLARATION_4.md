# Declaration 4 — the mechanism check (committed and pushed before its first full run)

Owner request, prompt-log entry 107. The anchor is the push timestamp of the commit that adds this file. The script is
`Adam_SGD/checks/mechanism.py`. A smoke run on thinned grids checked that the code runs; its output was discarded unread.
The engine gained an optional weight log; its default outputs are unchanged, and `drift_battery.txt` still reproduces
byte for byte.

## Why

Declaration 3 (post hoc) opened the gate narrowly. The ratio rule won in the wandering-units world T0′ under SGD, momentum
and coupled Adam, within 1.002 of the oracle. Two details point to a mechanism that would make that win a coincidence of
the design:
- the win held only at Ω = 1 (FRAGILE: 6 of 8 cells flip);
- the rule landed on the oracle's weight in every drifting world.

**The suspected mechanism.** When training settles, the real parts of the two pulls cancel, so the unsmoothed ratio
|g_p|/|g_q| measures the ratio of the gradients' noise. The battery gave both gradients equal noise, which makes the rule's
effective weight 1, and 1 is exactly the right weight in those worlds. This would also explain why smoothing hurts:
smoothing removes the noise that was making the rule right.

## Tests and expectations

The world is T0′ under SGD, with the past gradient's noise set to r × the present noise, r ∈ {0.25, 0.5, 1, 2, 4}, plus a
noise-free past (r = 0). Every arm is retuned at each r, on the same seeds and grids as Declaration 3.

- **M1. The ratio rule's effective weight tracks 1/r,** within 25 % at every r > 0. Expected: holds.
- **M2. The ratio rule is AHEAD at r = 1 and not AHEAD at r = 0.25 or 4.** Expected: holds.
- **M3. A noise-free past.** Reported, with no prediction.

## What the outcomes mean

- **M1 and M2 hold.** The ratio rule's win in the drifting worlds is set by the noise ratio of the two gradients, not by
  their signal. The win holds only when the past and present gradients are equally noisy.
  - The equanimity principle ("equal pull") is then an accidental estimator of the right balance.
  - The drifting-world results must be read as conditional on equal noise.
  - A rule that would work generally has to compare signal, not noise. That is a new idea, to be declared and gated
    separately if the owner wants it pursued.
- **Either fails.** The noise explanation is not confirmed. The win in T0′ stands as post-hoc evidence of a real
  drifting-units niche, still FRAGILE in Ω.
