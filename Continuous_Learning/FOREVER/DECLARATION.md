# Declaration: CRR's commitments run through FOREVER's mathematics (pushed before any script exists)

**Status.** Owner request: prompt-log entry 180, "Treat crr as falsifiable metaphysics and run the mathematical principles
through the forever paper mathematics". This is a declared synthetic check (rung R4). It is not a ledger row and uses no
data. It was written on 2026-09-25 before `checks/forever_checks.py` existed.

**The paper.** Feng, Wang et al., *FOREVER: Forgetting Curve-Inspired Memory Replay for Language Model Continual
Learning*, arXiv 2601.03938 v2, 20 Apr 2026 (v1 7 Jan 2026). It was fetched and read in full on 2026-09-25; the record is
`docs/citations/forever_2026-09-25.md`.

**Its equations, as used here:**

| eq. | name | definition |
|---|---|---|
| (2) | the update | Δ_t = ‖Θ_t − Θ_{t−1}‖₂ over the LoRA weights |
| (3) | model time | τ_t = Σ Δ_i, reset at each new task |
| (4) | the model day | τ_day = Σ_{i ≤ S} Δ_i, with S = 24 |
| (5)–(6) | replay triggers | replay fires when τ_t ≥ d·τ_day, for d in {1, 2, 4, 7, 15, 30} |
| (7)–(9) | the intensity ratio | μ₀ is the warm-up mean of Δ; μ_t is an EMA of Δ with λ = 0.05; r_t = μ_t/μ₀ |
| (10) | the replay weight | β_t = β_base · clip(1 + γ(r_t − 1), g_min, g_max), with β_base = 10⁻³, g_min = 0.5, g_max = 3.0 (γ is not stated in the text read) |
| (11) | the replay loss | L_old + β_t ‖Θ − Θ*‖², with Θ* the end of the previous task |

## The reading tested

CRR (`theory/CRR.md`) is read as falsifiable metaphysics:
- each commitment makes a claim about what FOREVER's quantities should be;
- each claim has a computed falsifier;
- every label is printed from numbers by the script (R15).

Rows marked CRR-favourable are those a pass would count for. Rows marked record-predicted are those the repository's
record says will go against CRR.

### F1. A1′ + D2 (the arc in the system's own unit) against a change of parametrisation

**The claim.** CRR's arc uses the Fisher–Rao metric, which Čencov's theorem makes the invariant choice. FOREVER's τ is a
Euclidean arc over LoRA factors. The product BA is unchanged when A → DA and B → BD⁻¹ for any positive diagonal D.

**The world.** A softmax classifier with W = W₀ + BA and rank 4, trained by SGD on two synthetic tasks. The trajectory is
fixed. Every snapshot is reparametrised by a fixed D (entries log-uniform on [1/4, 4], seed 1), and the model's
predictions on a probe are unchanged.

**Predictions:**
- **F1a.** The predictions are identical: max |Δp| ≤ 1e-12. *(check)*
- **F1b.** The Fisher arc (the sum of √(2·KL_step) on the probe) is identical: relative difference ≤ 1e-9. *(check)*
- **F1c.** FOREVER's normalised trigger steps differ in at least one of the first six triggers. *(CRR-favourable)*
- **F1d.** With every Δ multiplied by a constant (a change of units, not a reparametrisation), FOREVER's normalised
  trigger steps are identical. The τ_day calibration, an own-unit in A1′'s sense, removes a global scale. *(check)*

### F2. D2's "change" (resolvable change in what the system says) against movement that changes nothing

**The world.** The same classifier with k = 8 input features that are identically zero in the training data and the
probe. Their weights receive Gaussian noise (sd 0.01 per step), which changes no prediction.

**Predictions:**
- **F2a.** The Fisher trigger steps are identical with and without the noise. *(check)*
- **F2b.** FOREVER's Euclidean trigger steps move earlier in at least one of the first six triggers. *(CRR-favourable)*

### F3. P3 and P5 (exponential retention in natural time; the consistency relation)

**The computation.** The step at which each of FOREVER's thresholds is reached, when the update size decays as:
- Δ_t constant;
- Δ_t ∝ 1/(t + c), with c = 50;
- Δ_t ∝ 1/√(t + c).

**Predictions:**
- **F3a.** With 1/(t + c) decay, the trigger steps satisfy t_d = c((1 + S/c)^d − 1) within one step, so the human
  schedule in τ becomes geometric spacing in steps. That is P5's p = 1 case, standard calculus. *(consistency, as CRR.md
  §7 says; not a prediction)*
- **F3b.** Constant Δ reproduces the human schedule in steps, t_d = d·S. *(check)*

### F4. H-EQ (equal pull, Ω = 1) against FOREVER's intensity-aware weight (10)

**The world.** A quadratic present loss L_p = ½(θ − a)ᵀH(θ − a) in five dimensions, an anchor penalty w·c‖θ − θ*‖²
with the anchor at the start (θ* = θ₀), SGD at η = 0.05, and 2000 steps.

**Arms:**
- fixed w on a grid;
- the registered rule (Ω = 1, EMA 0.9, cap 10⁴);
- FOREVER's weight, with β_base tuned on the same grid at c = 1 and then held fixed, γ in {0.5, 1, 2}, and the paper's
  S, λ, g_min and g_max.

**The anchor scales:** c in {1, 16, 256}.

**Predictions:**
- **F4a.** At c = 1 the rule's weight sits at its cap on at least half of the first 50 steps, the zero-anchor freeze of
  RW2. FOREVER's weight stays inside [g_min, g_max]·β_base at every step. *(record-predicted: the degeneracy is the
  rule's)*
- **F4b.** At c = 16 or 256, FOREVER's weight with β_base held at its c = 1 value diverges for at least one γ, and the
  rule is finite at every c. *(CRR-favourable: the step bound)*
- **F4c.** When the movement stops, FOREVER's weight tends to β_base·max(g_min, 1 − γ): at the last step, within 1 %. So
  FOREVER stops at one point on the Pareto curve (a fixed-λ point), while the rule at Ω = 1 stops wherever it meets the
  curve. *(check, standard)*
- **F4d.** At c = 1, the rule's final total loss L_p + c‖θ − θ*‖² is at or below FOREVER's best γ. *(H-EQ's own claim;
  the record, EQX and the Adam checks, predicts FAIL)*

### F5. A3 + E2 + Proposition 7 (a pause on the system's own clock carries no content)

**The world.** The recorded Δ sequence of F1's run, with a pause of L wall ticks, L in {0, 50, 500}, inserted after
update 300. No update happens during the pause.

**Predictions:**
- **F5a.** FOREVER's τ-keyed trigger indices, counted in updates, are identical for every L. *(check: its clock is the
  learner's own)*
- **F5b.** The same thresholds keyed to wall ticks give different trigger indices for L > 0. *(check)*
- **F5c.** β at the first replay after the pause is identical for every L when the EMA advances per update (Algorithm 1).
  It differs when the EMA advances per wall tick with Δ = 0 during the pause. *(check: E2 applied to (8))*

### F6. D3 + D4 (chord and surplus) against the arc, where the path backtracks

**The world.** The classifier trained on task B for 150 steps, then on task A again for 150 steps. So it travels away
and back.

**The computation:**
- the arc and the chord from the task start (Euclidean and Fisher);
- the surplus S = C − C*;
- the old-task (A) loss at the end;
- how many of FOREVER's triggers each clock fires.

**Predictions:**
- **F6a.** The arc clocks fire at least 2 more triggers than the chord clocks. *(check)*
- **F6b.** The chord is the better tracker of the final old-task loss here, because the path returns. *(reading, per
  T1X2-1 and ARC-T1b: the endpoint, not the path, predicts forgetting)*

## What each outcome means

- **F1c, F2b and F4b hold.** On FOREVER's own quantities, the CRR choices (the Fisher metric; a past step bounded by the
  present) do what CRR says: they are invariant, and they are bounded where FOREVER's are not. That is a reason to run
  the declared ARC-R gate. It is not evidence that they improve accuracy.
- **They fail.** In this setting, CRR's metric and bound add nothing to FOREVER.
- **F4a and F4d.** These go against H-EQ if they fall as the record predicts.

## Parameters

Seeds 0 (data and initialisation) and 1 (D). Every constant is named in the script. This is one declared run: no second
battery on the same day under this declaration.

## Amendment 1 (2026-09-25, after the first run crashed in F5; pushed before the rerun)

**What happened.** The first run printed F1 to F4 and then crashed in F5. In the declared world, FOREVER's triggers on the
base run fall at updates 24 and 257 and at no later update. With the pause placed after update 300, there is no "first
replay after the pause", so F5c's quantity was undefined.

**The change.** The pause is moved to after update 100, so the trigger at update 257 follows it. The script also stops
with a message, rather than a crash, if no trigger follows the pause. Nothing else changes: F5a, F5b and F5c keep their
wording, and F1 to F4 and F6 are unchanged. The F1–F4 output of the crashed run is kept in the scratchpad and will be
compared with the rerun.

**Its status.** This is a post-hoc repair of an instrument defect, not a change of prediction. F5 is labelled "(Amendment
1)" in the output.
