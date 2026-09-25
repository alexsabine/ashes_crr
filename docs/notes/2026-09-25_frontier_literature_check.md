# Frontier literature check, 2026-09-25: plasticity, the Pareto reading of Ω = 1, and continual learning with AI safety

**Status.** A note to the auditor, not evidence (R8). Owner request: prompt-log entry 176. Nothing here is a ledger row.

**Sources.** Every external claim below comes from one of three dossiers, all fetched on 2026-09-25 and tagged per
source ([F] full text, [A] abstract, [S] search rendering only):
- `docs/citations/frontier_plasticity_2026-09-25.md`: 44 sources (23 [F], 21 [A]);
- `docs/citations/pareto_equanimity_2026-09-25.md`: 35 sources (26 [F], 8 [A], 1 code; one [S] item);
- `docs/citations/frontier_cl_safety_2026-09-25.md`: 55 sources (18 [F], 36 [A], 1 [title]).

**How the quotes were checked.** Every quoted string in the three dossiers was checked against the saved fetched text.
- Mismatches were one of three kinds: mathematics transliterated from LaTeX (marked in the dossiers), titles shortened
  with an ellipsis, or the one [S] item.
- One paraphrase had been written as a quotation (Aligned-MTL). It was corrected to the verbatim wording before commit.

**The repository's own numbers** come from `Continuous_Learning/checks/pareto_identities.txt`: a pinned, CI-checked
identity check, standard algebra with no verdict.

## 1. Ω = 1 against the Pareto literature

**What the pinned identities show** (`pareto_identities.txt`):
- **[1]–[3] The direction.** For two terms, the rule at Ω = 1 is ‖g_p‖(u_p + u_q): the bisector of the unit gradients.
  - That is MGDA's min-norm direction on normalised gradients, and IMTL-G's equal-projection direction for two tasks.
  - The largest deviation over 1000 random pairs is 5.164e-15.
- **[4] Where they stop.** On the Pareto curve of two quadratics, the rule at Ω = 1, MGDA (raw and normalised) and IMTL-G all
  vanish (at most 1.208e-14 of ‖g_p‖). The rule at Ω = 0.9 and 1.1 leaves 0.100000 of ‖g_p‖.
- **[5] The step length.** The rule's step length stays at ‖g_p‖ (1.087246 at every scale of the past term). MGDA's and
  IMTL-G's lengths move with that scale.

**What the literature adds** (`pareto_equanimity_2026-09-25.md`):
- **The continuum of equilibria is published.** For MGDA: Désidéri, "If ω = 0 ..., stop"; CAGrad, "MGDA and PCGrad
  converge to different Pareto-stationary points depending on θ_init". For the plain sum of normalised gradients: DiBS,
  NeurIPS 2025, Example 2, which converges "at x = x_0" from any start. This is the paper's one-dimensional knife edge
  (§4.1).
- **The direction is published.** Nash-MTL's two-task solution "is equivalent to independently normalizing each gradient
  and summing with equal weights".
  - MEGA-II (2019/2020) takes the bisector in continual learning, with the step fixed at ‖∇ℓ_t‖. That is a tighter form of
    the rule's step bound.
  - DB-MTL has the rule's EMA and normalisation.
- **Not found in what was read:**
  - that Ω ≠ 1 removes every interior equilibrium (a one-line consequence of the definition, so unlikely to be new);
  - that the stopping point depends on the smoothing lag.
- **Equanimity has one published counterpart: the symmetry axiom of Nash bargaining.** Symmetry fixes the direction, not
  the endpoint: symmetric methods still stop anywhere on the front.
- **The principles that do choose a point are not CRR's:**
  - distance to each objective's own optimum (DiBS);
  - Σ log ℓ (FAMO);
  - maximum likelihood (Kendall et al.);
  - sample counts, α_t = n_t/Σn_k (PMF-CL, May 2026).
- **PMF-CL's rule is the Bayes weight.** It is w_B = n_q/n_p of the paper's §4.3, and SCL3's SEC keeps it.
- **Xin et al.'s result is the published form of this repository's B5.** Properly chosen scalarisation cannot be beaten on
  convex problems, and coarse grids mislead.

**Reading (inference).** As a rule for choosing a trade-off, Ω = 1 fails before any data.
- The DiBS symmetric pair is a ready-made must-fail surrogate. Any rule that claims a selection principle must return the
  symmetric point from every start.
- The exact rule at Ω = 1 returns its start (§4.1 of the paper; identity [4]).
- H-EQ therefore reduces to normalised-gradient summation with the present step length. Its one property beyond the family
  is the asymmetric scale: invariant to the past term, linear in the present.

## 2. Plasticity, and the prior art for H-REG

**H-REG as proposed in chat on 2026-09-25 (prompt-log entry 175).** CRR's A6 ("never an accumulated count") and P3 (age
weights) as a learner:
- per-task Fisher penalties;
- normalised geometric weights, Σπ_k = 1;
- total strength of one task's Laplace term;
- anchored at the Fisher-weighted mean of past optima.

**What the literature says** (`frontier_plasticity_2026-09-25.md`):
- **The anchor is Kirkpatrick et al.'s separate-penalty EWC,** and it is disputed. Huszár calls it a double count, and the
  reply defends it on empirical grounds.
- **The weights are online EWC's (Schwarz et al. 2018) up to a factor** (1 − qⁿ)/(1 − q). That factor tends to a
  constant, which a tuned λ absorbs.
- **The normalised merge to the same point is published:** mode-IMM, Fisher merging, and CoFiMA, whose eq. 6 is
  Σ F_t θ_t / Σ F_t.
- **The uniform limit (q → 1) is Laplace divided by the task count, below Bayes.** CoMA warns that the uniform average
  "might result in suboptimal performances". GVCL reports tuned online-EWC weights far above Bayes.
- **"Accumulation makes the network rigid" is well documented:** Chaudhry's intransigence, Schwarz, MESU ("plasticity
  collapses"), MEAL, Kim 2026.
- **What remains of H-REG** is the small-T schedule of the normalisation. With one past task, H-REG, online EWC and Laplace
  coincide up to λ, and this repository's carriers have 2–5 tasks.

**Reading (inference).**
- H-REG is not a promising novelty candidate.
- As a test of the axiom A6 it is still meaningful. A6's direction, "past strength of one task", runs against the
  published finding that tuned weights sit above Bayes.
- A gate would need online EWC (γ tuned), separate-penalty EWC, EWC++, L2 Init and Shrink-and-Perturb as baselines. It
  would also need two ablations (anchor; normalisation), and long streams.
- If the gate cannot separate H-REG from online EWC, it reduces to online EWC with a λ schedule, and R12 applies.

## 3. Continual learning with AI safety

**Findings** (`frontier_cl_safety_2026-09-25.md`):
- **The zero-anchor degeneracy** that froze the Ω rule in RW2 is stated in print. "Two to Tango" (arXiv 2606.09866):
  "this KL gradient is zero at θ = θ₀". The published repairs are four:
  - a target instead of a ratio (Ziegler et al.);
  - a warm-up (Two to Tango; the VQGAN code);
  - ε, clamp and EMA (VQGAN; SAE-FD);
  - a constraint that vanishes at zero deviation (Qi et al. 2024).
- **No safety method read today sets an anchor weight from a gradient-norm ratio.**
- **The own-step objective as a route to zero stake in a pause** (Proposition 7) is **not stated in any source read today**.
  - The nearest are POST / Neutrality+, DReST and LNPO: training for trajectory-length neutrality, 40–71 % less shutdown
    resistance in gridworlds.
  - Orseau and Armstrong's warning applies to lossy pauses: "Removing interrupted histories ... is also likely to introduce
    a bias".
  - Mitra (arXiv 2609.22087) finds that resuming with the schedule indexed "in effective (active) time" matches
    uninterrupted training "exactly on a GPT-2/AdamW task". That is independent support for RW1.
  - Agent-framework papers (arXiv 2608.29381, 2608.03836) state the "world moved during the pause" failure (E3) in systems
    terms.
- **New empirical shutdown work:**
  - peer-shutdown sabotage at 38.3 % against an 8.4 % control, falling when shutdown is framed as routine (arXiv
    2609.28274);
  - ROGUE (arXiv 2606.00341);
  - a low-nudge benchmark at 5.1 % (arXiv 2605.06490).
- **The shared variable of forgetting, plasticity and safety** in the 2026 literature is distance from the base or aligned
  model: KL or drift (RL's Razor; Rejuvenation; FST).
  - That is an endpoint quantity. It agrees with this ledger's T1X2-1 (the endpoint predicts forgetting; the path does not
    beat it).
  - Every method that picks a safety–helpfulness trade-off does so with an external dial.

## 4. What this changes for the next step (inference; the owner decides)

1. **Ω = 1 is closed as a trade-off principle.** It is the two-task normalised-gradient direction (Nash-MTL, IMTL-G,
   normalised MGDA). Its continuum of equilibria is published, and it fails the DiBS symmetric must-fail surrogate by
   construction. Any further Ω study would have to register those methods as arms and would expect to reduce to them
   (R7).
2. **H-REG is mostly prior art.** It remains a meaningful test of A6, but not a novelty candidate. It is worth running only
   as the first data test of a CRR axiom, with the baselines of §2 and the expectation that it may reduce to online EWC.
3. **The one CRR construction without a published statement in this check is on the safety side:** the own-step objective
   giving zero stake in a lossless pause.
   - Its evidential weakness is that it holds by construction.
   - A comparison against published baselines would give it weight: the natural-time agent against DReST- and
     LNPO-trained agents in the same gridworlds, including the lossy pauses where Orseau and Armstrong warn of bias. That
     can run on this CPU if their environments can be reproduced.
   - It would need a declaration, a gate and the POST literature re-read in full. A named domain expert, not this check,
     would judge novelty (the SYNTHESIS/ADDS rule).
