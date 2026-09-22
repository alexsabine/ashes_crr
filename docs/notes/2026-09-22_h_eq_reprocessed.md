# H-EQ reprocessed after the cross-verification, and the enhanced rule EQ-B (2026-09-22)

Owner request (prompt-log entry 74): process the CRR mathematics again with what the cross-verification taught, then
test the enhancement with the EQ3 approach. This note is a note (R8): every number is from a pinned output
(`theory/checks/omega_reprocessed.txt`, `runs/eq4_dev/summary.txt`, `prereg/eq4/gate_EQB.txt`, `prereg/eq4/gate_EQBM.txt`);
the held-out study is EQ4 (`prereg/eq4/PREREG.md`), whose data step is on a later calendar day (R3).

## 1. What the cross-verification taught, made checkable

`Continuous_Learning/CROSS_VERIFICATION.md` §4 left four statements about the rule. `theory/checks/omega_reprocessed.py`
turns each into a computation on the two-task quadratic of the mathematics check and prints its label from the numbers.

| statement | check | result |
|---|---|---|
| the rule is invariant to the scale of the past term | trajectories at F and 16F, same seed, past noise scaled with the term | identical to machine precision (0.000e+00); with the noise left at 0.5 the trajectories differ (4.252e+00): the invariance is to the term, not to a fixed-size noise added to it |
| and blind to its shape | F with its diagonal reversed | endpoint moves by 0.0412: the rule does not see shape; importance-estimate methods compose with it |
| the step bound is the mechanism | max of the smoothed ratio ‖ĝ_p + wĝ_q‖/‖ĝ_p‖ over 20 000 steps | 1.9778, never above 2: the bound holds on the smoothed pull; the raw ratio exceeds 2 on 0.89 % of steps (a small ‖g_p‖ in the denominator) |
| a set-valued past minimum (a constraint) breaks the rule's premise | F with two zero eigenvalues | **no**: the free directions relax to the present optimum and the median derived w is unchanged (0.5409 vs 0.5516); the quadratic model gives no mechanism for excluding constraint terms; the narrowing of H-EQ to losses on the past stays an empirical scope from EQ3-4 |
| the rule answers one extreme present batch by amplifying the past step | sweep: gradient × {10, 100, 1000, 10000} for {1, 5} steps | the rule's total exceeds twice its clean value at (100, 5) and it diverges at (1000, 5); the tuned fixed weight diverges at (1000, 5) too; the rule degrades before the fixed weight does |
| the Fisher-norm ratio of H-EQ as written changes the mechanism | endpoint's nearest Pareto λ under both norms | Euclidean 0.4926, Fisher 0.4763, both within 0.06 of the curve: the metric moves the stopping point along the curve, not the set |
| the property survives Adam | the rule upstream of Adam, F and 16F | every arm finite and within 2 % of the Adam-tuned fixed weight, the fixed weight included: under Adam the fixed weight is scale-robust too, so the scale claim is SGD-only |

## 2. The enhancement, EQ-B

The one failure the rule has that a fixed weight does not is the amplification: w ∝ ‖ĝ_p‖, so an extreme present batch
raises the past pull in proportion (max w 749 at ×10000 against 6.82 clean). EQ-B bounds the present gradient first:

$$\tilde g_p = g_p \cdot \min\!\left(1,\; \frac{\kappa \, \max_{\text{last } N \text{ kept}} \|g_p\|}{\|g_p\|}\right), \qquad w = \Omega \frac{\|\widehat{\tilde g}_p\|}{\|\hat g_q\|}, \qquad \theta \leftarrow \theta - \eta(\tilde g_p + w\,g_q),$$

with κ = 2, N = 50, no clip until 10 lengths are known, the history holding the **kept** (post-clip) lengths and restarting
at every task boundary. The reference is the window **maximum**, not the median: the first version of EQ-B used
κ × the running median, and on the softmax surrogate S-Y it clipped the informative batches, because the median
present-gradient length collapses toward zero as a task is learned while the information sits in the tail (AGENT_LOG 63;
the first version's dev run is kept in `runs/eq4_dev/v1_median/`). With the kept-length maximum, a run of extreme batches
can raise the bound by at most a factor κ per batch (a geometric leak bounded by κ^run), and a legitimate regime change
catches up at the same rate.

On the quadratic (`omega_reprocessed.txt` [4]): EQ-B's clean total equals the rule's (3.4789 vs 3.4789), and EQ-B
survives the whole poison sweep where the rule and the tuned fixed weight both diverge at (1000, 5) and the rule degrades
at (100, 5). On the S-Y gate rows (`prereg/eq4/gate_EQB.txt`, `gate_EQBM.txt`): EQ-B equals the rule on every clean
row (the bound idle) and is ahead of it on the poisoned row, the EQBM gate reading OPEN with the clean S-Y row as its
negative control. On the six seen EQ3 carriers (`runs/eq4_dev/summary.txt`, exploratory, no verdict): with κ = 2 the
clean EQ-B accuracy equals the rule's on every carrier (clip fraction ≤ 0.001), and under the poisoned regime EQ-B is
ahead of the rule on 6/6 carriers by 2.64 to 20.75 points and ahead of the fixed weight with the same clip on 5/6.

## 3. What changes in H-EQ (proposal for the v3.2 list; `theory/CRR.md` is not edited)

Printed by the check as [7], each line conditional on its numbers:

- (a) **scope**: the quadratic model gives no mechanism for excluding constraint terms; the narrowing to past terms that
  are losses on the past is an empirical scope from EQ3-4, and is stated as such;
- (b) **the bound is the mechanism**: the claim is "the past pull never exceeds (1 + Ω) × the present pull in the smoothed
  gradients", not "equal pull is optimal";
- (c) **the present pull must itself be bounded** for the bound to mean anything: EQ-B, with κ and N named;
- (d) **the metric is a stopping point**, not a mechanism; (e) **the optimiser is a registered parameter**, and under Adam
  the fixed weight is scale-robust too, so the scale claim is SGD-only.

## 4. The study that tests it

EQ4 (`prereg/eq4/PREREG.md`): six unseen PMLB carriers, the EQ3 design with EQ-B beside the registered rule, and a
poisoned regime whose R7 baseline is the fixed weight with the same clip. The rule that EQ4 tests (EQ-B) was defined
today after seeing EQ3's carriers and the synthetic battery; under R3 it is used on other carriers under a fresh prereg
on a later calendar day. The prereg is hashed and pushed today; the data are fetched on or after 2026-09-23.

> The remember-pull rule had one weak spot: if a single learning step was enormous, the rule made the remember-pull
> enormous too, and the whole thing could blow up. The fix is to cap each learning step at twice the biggest recent
> step before the rule looks at it. On clean data the cap never triggers and nothing changes; on data with a few
> poisoned steps, the capped rule keeps working where the plain rule and the plain fixed knob fall over. The first
> version of the cap used the *typical* step size instead of the *biggest*, and that was wrong: on these learners the
> typical step shrinks to almost nothing, so the cap was cutting the useful steps. The real test is on new data,
> tomorrow.
