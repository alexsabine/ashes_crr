# Declaration 1 — the assumption audit (committed and pushed before its first full run)

Owner request, prompt-log entry 107: "Double check any prior assumptions regarding the value of a fixed parameter before
proceeding." The anchor is the push timestamp of the commit that adds this file. The script is
`Adam_SGD/checks/assumptions.py`, with its shared code in `Adam_SGD/checks/common.py`. A 40-step smoke run on thinned grids
checked that the code runs; its output was discarded unread.

## Why this comes first

Every earlier verdict on the Ω rule against a fixed weight rests on four choices that were never tested. Before designing
the drifting-world battery (Declaration 2, to follow), each choice is checked.

1. **The objective (the reading of the scale c).** The earlier checks scored the total L_p + c·L_q. That is right if c is
   the past term's true importance (the 'imp' reading). It is wrong if c is a units error the learner cannot see (the
   'unit' reading), such as a miscalibrated Fisher estimate, a temperature, or a loss scale. In that case the objective is
   L_p + L_q, and the weight that is right in principle is 1/c, not 1.
   - The repository has direct evidence that units errors are real. The tuned EWC λ spans 100.00× across the six EQ4
     carriers (EQ4-0) and 1410.00× across the six EQ3 carriers (EQ3-0).
2. **The noise under a change of units.** The earlier checks multiplied the past term's curvature by c but not its noise.
   So they did not test a pure change of units.
3. **Selection bias.** The tuned constant was chosen and scored on the same five seeds. The rule has no knob, so it had no
   such advantage.
4. **The step size is a fixed parameter too.** The fixed weight was tuned at a fixed learning rate of 0.05, where its
   in-principle value (λ = 1 under 'imp') diverges beyond the stability edge. A fixed weight with its learning rate tuned
   is the stronger baseline, and so is the rule with its learning rate tuned.

## Tests, expectations and meanings

- **AS1. The fixed weight that is right in principle.**
  - The check: the noise-free equilibrium of a fixed weight, on a fine grid of λ.
  - Expected: holds. The argmin is λ = 1 under 'imp' and λ = 1/c under 'unit'. This is algebra, so a failure is a bug.
- **AS2. Which reading and noise the earlier checks used.**
  - The check: this code, run in the 'imp' reading with unscaled noise, reproduces `adam_checks.ev` exactly.
  - Expected: holds.
  - Meaning: every earlier "behind wherever the scales differ" verdict (B5, A4, A8) is a statement under the 'imp'
    reading.
- **AS3. The earlier comparison re-scored under the 'unit' reading with a pure change of units.**
  - Expected: the rule is invariant across c (spread ≤ 1e-6), because its weight scales as 1/c.
  - Expected: a constant tuned at each c ties the rule, since λ/c reproduces λ's trajectory.
  - Expected: a constant tuned at c = 1 and deployed unchanged at c ≠ 1 is much worse or diverges.
  - If so: the earlier verdicts depend on the reading. Under 'unit', the rule's value is that it never needs retuning; it
    does not beat a constant retuned in hindsight.
- **AS3b.** The same under unscaled noise. Open.
- **AS4. Selection bias.**
  - Expected: the held-out score of the tuned constant is no better than its tuning-seed score, and the rule's two scores
    are close.
  - Meaning: if the bias is large, every in-sample comparison here understated the rule.
- **AS5. Tuning the learning rate.** Open.
  - If the fixed weight λ = 1 with a tuned learning rate beats the rule with a tuned learning rate by more than 10 %
    (under 'imp'), then the rule's earlier advantage at lr 0.05 was a step-size effect. That is the preconditioning Adam
    supplies, and the fixed baseline must be tuned jointly with the learning rate in every later check.
  - If it does not, the rule keeps an advantage that the step size alone does not give.
- **AS6. Tuning cost in trajectories.** Report only.

## The lessons carried forward into Declaration 2 (the drifting worlds)

These come from the record so far and bind the next battery.
- Compare against a **finely** tuned constant, not a coarse grid (`adam_checks_3.txt` B5).
- Tune constants on one set of seeds and score on another (AS4).
- Include the VQGAN-style ratio (the rule without smoothing) as the prior-art family member (B1).
- Run plain SGD, heavy-ball momentum, and Adam both coupled and decoupled (A1–A8).
- Tune the learning rate for every arm, or state why not (AS5).
- State the reading of the scale ('imp', 'unit' or both) and scale the noise with the units (AS1–AS3).
- On a stationary problem an adaptive weight settles to a constant (B4). The rule can only win where the right weight
  moves, so the must-win control must be a world in which it moves by construction. The must-lose control is a
  stationary world.
- The clip that EQ-B adds is prior art (AutoClip). Under poison, the comparator is a fixed weight with the same clip
  (EQ4-3).
- Every label is computed, and a sensitivity table is required. A label that flips in more than one cell is FRAGILE.
