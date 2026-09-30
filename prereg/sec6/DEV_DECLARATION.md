# SEC6 development declaration: SEC4's clipped SEC on a fifth unseen family, against the published tuning-free baselines (pushed before any SEC6 code)

**The request.** Prompt-log entry 257: "We should then run more tests on sec4". This is P2 of `Applied_Suite/PROGRAMME.md`.

**Where SEC stands.**
- SEC4-1 is PASS-1 on the third unseen family (6/6).
- SEC5-1 FAILs on the fourth family (4/8).
- SPA1 finds the method's parts published. The two nearest published rules are:
  - **Synaptic Intelligence (SI).** It is a path-fitted, per-parameter importance "with the same units as the loss", at a
    strength c for which it states a principled value: "If the path integral (Eq. 3) is evaluated precisely, c = 1 would
    correspond to an equal weighting of old and new memories". Source: arXiv 1703.04200 v3, fetched in SPA1.
  - **AR1.** It bounds the EWC strength by the step size: "Given maxF and η we can easily determine the maximum value for
    λ as 1/(η · maxF )". Source: arXiv 1806.08568 v3, SPA1 claim f3:0.
- Neither was run against SEC on held-out carriers. SEC6 does both. R7 asks for the published method closest to the rule
  under test.

## What SEC6 tests (fixed now; the pre-registration adds only the carriers, the P1-conditional arms and the hash)

**1. The replication (primary): SEC4's clipped SEC, unchanged.**
- It is `run_guard(variant="clip")` with κ = 0.5, imported from byte copies of `runs/sec5/frozen/`, which are themselves
  byte copies of SEC4's.
- It runs on a fifth unseen family.

**2. The published tuning-free baselines** (new arms; each maps its paper's penalty onto SEC1's learner exactly):

| arm | the published rule | in SEC1's parametrisation (penalty gradient w · 2 · imp · (θ − θ\*)) |
|---|---|---|
| **SI-1** | SI with c = 1, ξ = 10⁻³ (the split-MNIST damping, reported with the same 2 × 256 MLP family). The per-task ω_k = −Σ_t g_k(t) Δθ_k(t) uses the clean present-task gradient, as SI's reference implementation does. Ω_k = Σ_ν ω_k^ν / ((Δ_k^ν)² + ξ). | w = c = 1; imp = Ω (summed over past tasks); anchor θ̃ = the parameters at the previous task's end |
| **SI-0.1** | SI with c = 0.1 and ξ = 0.1, the values the paper reports for permuted MNIST ("the value for c = 0.1 was determined via a coarse grid search"). This is a published default carried across. | w = 0.1; imp = Ω with ξ = 0.1 |
| **AR1-P** | AR1 as published: the Fisher averaged over past tasks and clipped at maxF = 0.001 ("Fk values are averaged and clipped to 0.001"), and λ = 1/(η · maxF) | imp = min(mean_j f_j, 0.001); λ = 2w, so w = 1/(2 · lr · 0.001) = 10,000 |
| **AR1-B** | AR1's bound used as the strength, with no maxF constant: λ = 1/(η · max_k F_k) on the accumulated raw Fisher at each task start (an adaptation: AR1's inequality, SEC's units-free direction) | w = 1/(2 · lr · max_k imp_k), recomputed at each task start; imp = the raw accumulated Fisher (the `fixed` arm's) |

- **None of these baselines is clipped by SEC4's guard.** They are run as published. A divergence is reported (SEC6-2's
  rule, applied to each).
- **raw Laplace** (`bayes`), unguarded SEC (`bayes_sec`), the one-factor SEC (`bayes_s1`) and Ω = 1 (`eq`) are SEC1's arms,
  unchanged.

**3. The P1-conditional arms** (the rule is fixed in `SEC_Analysis/DECLARATION.md` before any P1 run):
- **M1** (the model-Fisher Laplace) and **M2** (endpoint-curvature SEC) are carried if P1's pinned `m_checks.json` shows
  them not behind the tuned λ on at least (the clipped SEC's count − 1) of the 30 SEEN carriers.
- **M4** (the arc secant) is carried if it is ahead of the clipped SEC by more than a step on at least 3 of them.
- The pre-registration states which were carried, quoting `m_checks.json`.

## The development stage (SEEN data only; output `prereg/sec6/dev_SEC6.txt`, covered by the hash)

1. **D-ID.** The clipped SEC run through SEC6's harness equals SEC4's pinned `bayes_sec_clip` accuracy bit for bit, on
   seed 0 of every SEC4 and SEC5 carrier (14). The same identity holds for `bayes_sec` against SEC1's pinned records on 2
   SEC1 carriers.
2. **D-MAP.** Each baseline's mapping is checked on SEC1's synthetic stream:
   - SI-1 with c forced to 0 equals the fine-tuning run (`fixed` at w = 0 through the same harness) bit for bit.
   - AR1-B's w is printed per task, with max_k(lr · 2w · imp_k) = 1.0 to 10⁻¹².
   - AR1-P's imp never exceeds 0.001.
3. **D-RUN.** Every arm runs on the 30 SEEN carriers of SCL3, SEC3, SEC4 and SEC5 at seeds 0–4.
   - The count not behind the tuned λ is printed per arm, with divergences.
   - **Nothing is chosen from D-RUN.** Every baseline's constants come from its paper. D-RUN only shows that the arms run,
     and what they do on seen data.
   - D-RUN is not evidence and adds no ledger row. A baseline that does badly on SEEN data is still carried (R7: baselines
     that can win are not removed for losing).

## The fifth family (carrier selection from metadata only; `studies/sec6/select_carriers.py`)

**The rule.** SEC5's selection script with the suite order changed and nothing else:
- **Suites:** OpenML study 454 (New_OpenML_Suite_2025_classification), then study 445 (IRT Diverse Dataset Benchmark).
  Suites are pooled in this order until at least 8 datasets are eligible.
- **Eligibility:** SEC4's rule, unchanged. At least 4 classes; 400 to 1,000,000 rows; at most 1001 features; not SEEN by id,
  name or alias.
- **The records considered SEEN** include the twelve SEC5 carriers and everything else in `data/SEEN.md` on the day of the
  hash.
- **Draw:** at most 12, by `default_rng(20261001)` over the sorted eligible ids.
- **Metadata:** the study records and data lists are re-fetched today and saved in `prereg/sec6/`.

**If fewer than 8 are eligible across both suites,** SEC6 is declared NOT RUNNABLE on this family and stops (R12).

## Hypotheses to be registered (the pre-registration fixes them; stated now)

Here N is the number of scored carriers and need = ⌈0.75 N⌉.

| id | criterion |
|---|---|
| **SEC6-1** | the replication: clipped SEC − tuned λ > −step on at least need carriers |
| **SEC6-2** | no seed of the clipped SEC below 0.5 × the tuned λ's mean |
| **SEC6-B** | against the published baselines: the clipped SEC is not behind the tuned λ on **strictly more** carriers than each of SI-1, SI-0.1, AR1-P, AR1-B, raw Laplace, and each carried P1 arm. PASS only if it beats every one. |
| **SEC6-T, SEC6-P, SEC6-S** | as SEC5: the transferred λ, the 3-point sweep, and the sensitivity over the 3 window cells and κ ∈ {0.25, 1.0}. More than 1 flip is FRAGILE. |
| **SEC6-K, SEC6-E** | compute and firings, reported |

**PASS levels.**
- **PASS-0 and PASS-1** are as in SEC5.
- **If SEC6-1 is PASS-1,** it replicates SEC4-1 on a later day under a fresh pre-registration with the same frozen code,
  which is **PASS-2 by the letter of CLAUDE.md §7**. The row must print beside it that SEC5-1 FAILED on the fourth family,
  so the clipped SEC's family record is 2 of 3. The ladder prints both.

**Timing.** The pre-registration, the development output, the selection and the frozen scorer are hashed, OTS-stamped and
pushed on 2026-09-30. **No carrier is fetched before 2026-10-01T00:00Z** (R3).

## Forecasts (written now)

1. **SEC6-1:** FAIL is as likely as PASS. Two families of three were close to the edge, and SEC5 failed on the cap and on
   noisy seeds.
2. **SEC6-B:** SI-1 is the strongest baseline. Its per-parameter path secant is the nearest published relative of SEC's
   calibration. It is behind SEC on fewer carriers than raw Laplace.
3. **AR1-P** is behind the tuned λ on most carriers: its maxF constant does not transfer across networks.

## Amendment 1 (2026-09-30, after D-ID, D-MAP and D-RUN on SEEN carriers; before any SEC6 carrier is fetched; pushed before the changes are coded)

**What D-RUN showed** (`prereg/sec6/dev_SEC6.txt`, 30 SEEN carriers; not evidence, nothing chosen by count):

| arm | not behind the tuned λ | carriers with a divergent seed |
|---|---|---|
| SI-1 | 0/30 | 29 |
| SI-0.1 | 21/30 | 2 |
| AR1-P | 25/30 | 3 |
| AR1-B | 27/30 | 2 |
| clipped SEC (pinned records) | 26/30 | 2 |

- **SI-1 runs away.** At c = 1 under this learner's SGD, lr · 2c · Ω runs from about 8 to 10⁵⁹, and Ω has negative
  entries. The negatives come from minibatch noise in ω = −Σ g Δθ; SI's formula has no floor.
- **AR1-B is the strongest arm on SEEN data.** It is one carrier ahead of the clipped SEC. Its strength puts lr · w · max
  imp at 0.5 = κ, so it is SEC4's `scale` guard applied at every task start to the raw Fisher. It is a baseline that can
  win, and it stays exactly as declared.
- **Forecast 2 is wrong on SEEN data** ("SI-1 is the strongest baseline"). The forecast is recorded as written, not
  changed.

**The changes, each named with the data it was learned on** (R3: the 30 SEEN carriers, today; used on the fifth family
only on or after 2026-10-01):

1. **SI-1C is added** (SI-1 is kept as published). It is SI with c = 1 and ξ = 10⁻³, with Ω floored at 0 and clipped at
   κ / (lr · w), SEC4's clip with κ = 0.5 and w = c = 1.
   - **Why:** SEC itself is non-negative by construction (squared gradients), and it passes only with the clip (unguarded
     SEC diverged on 8 of 30). A comparison of the two calibrations that gives SEC its guard and denies SI the same guard
     would not be a baseline that can win (R7).
   - **Where it enters:** SEC6-B's "strictly more than every baseline" includes SI-1C.
   - **Its check:** SI-1C is run through D-RUN on the same 30 SEEN carriers before the hash, only to show it runs. Nothing
     is chosen from its count.
2. **An exclusion for carriers with no usable feature.** The metadata shows carriers whose features may all be string or
   text columns, which SCL3's loader drops (Student_Performance, WBCAtt, Mental_Health; DBPedia keeps 1).
   - **The rule:** a carrier with no usable feature after SCL3's loader (d = 0) is excluded and counted before any run,
     like the class rule. Otherwise the frozen scorer would divide by zero (SEC3 and T1x were voided by scorer crashes).
   - **d = 1 is not excluded.**
3. **SEC6-B is NOT DECIDABLE if N < 4,** as SEC6-1 is.
4. **Freezing.** The selection script is frozen as `sec6_select_carriers.py`, because `select_carriers.py` in the frozen
   folder is SEC4's.

**For P1, stated now:** AR1-B's strength rule uses no calibration. It only puts the Fisher's largest coordinate at half the
stability edge. It is recorded here as a candidate explanation to be read beside P1's M checks. It adds no row.

## Amendment 2 (2026-09-30, after SI-1C's D-RUN on SEEN carriers; before any SEC6 carrier is fetched; pushed before it is coded)

**What prompted it.**
- On the 30 SEEN carriers SI-1C is not behind the tuned λ on 28/30. Its margins over the tuned λ are often +10 to +30.
  The pinned clipped SEC reaches 26/30, and AR1-B 27/30.
- **The reference had no clip.** The tuned λ that SEC4-1 and SEC5-1 measure against is SEC1's two-stage grid on the raw
  Fisher **without** the clip. At large λ its largest coordinates cross the stability edge, so a strong but stable penalty
  is out of its reach. Every clipped arm has that reach.
- **So part of any clipped arm's margin over that reference may be the clip's, not the importance measure's.** A tuning-free
  claim should also be measured against a tuned λ that is given the same clip.

**The change** (learned on the 30 SEEN carriers today; used on the fifth family only on or after 2026-10-01):

1. **A new arm, `fixed_clip`, the tuned λ with SEC4's clip.**
   - It is SEC1's `fixed` arm (the raw Fisher at weight λ) on SEC1's same two-stage grid (the coarse grid, then the
     refinement rule), 5 seeds.
   - Every importance coordinate is clipped at κ / (lr · λ), with κ = 0.5, at each task start, exactly as SEC4's clip
     does at w = λ.
   - The best seed-mean is the **tuned clipped λ**, and its step is max(1, 2 × SE).
2. **A new registered hypothesis, SEC6-C:** clipped SEC − tuned clipped λ > −step_c on at least need carriers.
   - PASS or FAIL, and NOT DECIDABLE if N < 4.
   - It is not the replication. **SEC6-1 stays SEC4-1's criterion, unchanged,** so the replication is exact.
   - SEC6-C asks whether the clipped SEC is tuning-free against a reference with the same stability guard.
   - **SEC6-C is the stronger claim.** If SEC6-1 passes and SEC6-C fails, the report says the pass rests on the clip.
3. **The development check.** `fixed_clip` is run through D-RUN on the 30 SEEN carriers before the hash, only to show it
   runs and what it gives. Nothing is chosen from it.
4. **Beside SEC6-C (report):** SI-1C, AR1-B and every other baseline against the tuned clipped λ.

## Amendment 3 (2026-09-30, after P1's mechanism checks on the 30 SEEN carriers; before any SEC6 carrier is fetched; pushed before it is coded)

**What prompted it** (`SEC_Analysis/checks/m_checks.txt`, pinned).
- M6 (EDGE: every coordinate at SEC4's cap after task 1, no Fisher; the learner stays within one step of task 1's end) is
  **not behind the tuned λ on 24/30** SEEN carriers. The clipped SEC reaches 26/30.
- The frozen loader relabels classes by descending count, and SEC1's tasks are consecutive label pairs, so task 1 always
  holds the two most frequent classes (`SEC_Analysis/DECLARATION.md`, Amendment 3).
- **Consequence.** On these streams the family's criterion ("not behind the tuned λ") is met on most carriers by a learner
  that stops learning after task 1. A criterion that a must-fail control meets cannot, on its own, show that a method is
  tuning-free (R4's rule, applied to the instrument).

**The changes** (learned on the 30 SEEN carriers today; used on the fifth family only on or after 2026-10-01):

1. **A new arm, `edge`, P1's M6 exactly.**
   - After task 1, the importance is κ / (lr · w) on every coordinate, with κ = 0.5 and w = 1/2, and the anchor is updated
     at each task's end as for every arm.
   - Its implementation is checked against P1's pinned M6 records (`SEC_Analysis/checks/m_runs/`) on at least 3 SEEN
     carriers, bit for bit (D-ID-EDGE).
2. **A new registered instrument gate, SEC6-G.**
   - **The rule:** `edge` − tuned λ > −step is counted per carrier.
   - **If `edge` is not behind on at least need carriers,** the gate is CLOSED: the criterion of SEC6-1 cannot fail on this
     family. SEC6-1, SEC6-B and SEC6-P are then printed with "UNINFORMATIVE (a learner frozen after task 1 meets the same
     criterion; SEC6-G)". No PASS level above PASS-0 may be claimed for them.
   - The same gate is computed against the tuned clipped λ for SEC6-C (SEC6-GC).
   - **The gates' counts are printed whether open or closed.**
3. **A new registered secondary, SEC6-1F.** SEC6-1's criterion on the carriers that are not floor-bound (Amendment 1 of
   `SEC_Analysis/DECLARATION.md`: tuned λ mean − majority-class share × 100 ≥ 3 steps). NOT DECIDABLE if fewer than 4 such
   carriers.
4. **A report.** The task-1 share per carrier ((count of the two most frequent used classes) / n × 100), with `edge`'s and
   the clipped SEC's accuracies beside it.
