# Declaration — the smoothing follow-up to the Adam checks (committed and pushed before its first full run)

Owner request, prompt-log entry 104. The anchor is the push timestamp of the commit that adds this file. The script is
`Continuous_Learning/checks/adam_checks_2.py`, and its docstring holds the design. A 50-step smoke run checked that the
code runs; its output was discarded unread.

## Why this follow-up exists

`adam_checks.txt` (pinned in the previous commit, run after `DECLARATION_ADAM.md` was pushed) returned three results that
the declaration did not expect or left open:
- **A4 fails.** Under SGD the rule is ahead of the tuned fixed weight at c = 16 (total ratio 0.660) and behind it at
  c = 256 (1.235).
- **A7: the VQGAN-style ratio beat the rule at both mismatched scales.** The ratios were 0.526 against 0.660 at c = 16,
  and 0.847 against 1.235 at c = 256.
- **A8: under momentum the rule is finite but behind the tuned fixed weight at every scale.** The ratios were 1.015,
  1.077, 1.796 and 4.788.

The VQGAN-style ratio and the rule differ in two ways: the rule smooths the gradients with an EMA (0.9), and the VQGAN
ratio adds δ = 1e-4 to its denominator. This follow-up asks which of the two made the difference, and what the smoothing
buys.

## Tests and expectations

- **B1. Smoothing ablation under SGD.** The rule is run at smoothing s ∈ {0, 0.5, 0.9, 0.98} at every scale.
  - Declared criterion: the rule at s = 0 is within 10 % of the VQGAN-style ratio at c = 16 and c = 256.
  - Expected: holds. The δ is negligible against these gradient norms, so without smoothing the two rules nearly coincide.
  - If it holds: the gap in A7 is the smoothing, and the registered smoothing (0.9, frozen since EQ2) costs the rule on
    this model.
  - If it fails: something other than the smoothing separates the rule from the prior-art ratio, and the write-up must
    say so.
- **B2. What the smoothing buys.** At c = 16, the rule at s = 0.9 is run against s = 0 at noise 0.1, 0.5 and 1.0.
  - Expected: smoothing helps more as the noise grows, because an EMA averages noise out of the ratio. The result is
    reported per noise level, with no verdict.
- **B3. The derived weight itself.** The median of w over the last 1000 steps, for s = 0 and s = 0.9, at c = 16 and
  c = 256, is printed beside the SGD-tuned λ and the edge.
  - This is report only. It shows whether the rule under-weights the past relative to what the total loss asks for.

## What the results change

Nothing registered changes. The rule's smoothing is frozen in the registered estimator (R3). A different smoothing is a
new rule, and it would need a fresh prereg before any real carrier. The write-up (`ADAM_AND_PRIOR_ART.md`) reports B1–B3
as they fall, beside A1–A8.
