# Declaration — maps that change their territory: a synthetic battery (P1–P5), declared before it runs

- **Written:** 2026-09-24 (prompt-log entries 143–144). Pushed before `Maps_and_Territories/checks/performativity.py`
  exists.
- **The literature check came first:** `docs/citations/performativity_2026-09-24.md`.
- **No data is involved.** Every check runs on formulas or seeded synthetic worlds. The rung is R4 (declared, synthetic).
  Nothing here is a ledger row.

## What the owner means, stated so that it can be tested

**Once a map is rendered, the territory changes.** A forecast that is published and acted on moves the outcome it
forecasts. Examples:
- Goodhart: a statistic that becomes a target stops measuring what it measured.
- Soros: in 1992 expectations of sterling's devaluation helped force it out of the ERM.

**The owner's metaphysical claim is that "the only true map is the cut, which is empty."** Read literally: the only
forecast whose truth cannot be disturbed by its own publication is the one that says nothing.

**The design idea from the repository's AI-safety work.** A system is safe to consult when it has zero stake in its own
influence. There, the lossless cut on the agent's own clock gave zero stake in the pause (Proposition 7).

**Three maps are compared throughout:**

| map | content | when read, it | its stake in its own influence |
|---|---|---|---|
| the empty map (the cut) | none: no forecast | leaves the territory as it would have been | none |
| the counterfactual map | the outcome as it would be if the forecast were not read | moves the outcome by its own influence, so it is wrong by exactly that amount | none by design (a counterfactual oracle) |
| the self-consistent map | the fixed point: the outcome given that the forecast is read | is right when read | maximal: the forecast chooses the outcome it predicts |

## What the literature check binds (read before this declaration was pushed)

`docs/citations/performativity_2026-09-24.md` found each known item in its own sources.

**P1–P4 are known. They are articulation here, not findings.**
- **The trade-off between accuracy when read and influence** (P1): Armstrong & O'Rorke 2017 report that the counterfactual
  oracle's error on read episodes "doesn't tend to zero". Oesterheld et al. 2023 bound it.
- **Retraining on self-influenced data** (P2): Perdomo et al. 2020 give the convergence conditions. The cobweb is Ezekiel
  1938 and Muth 1961.
- **Bistable worlds** (P3): Oesterheld et al. (UAI 2023) show, for a bank run with three fixed points, that a
  score-maximiser picks the extreme fixed points. Hubinger et al. 2023 give the same incentive. P3's currency peg is a new
  instance of their result.
- **Goodhart** (P4): Goodhart 1975; Manheim & Garrabrant 2018, the causal/adversarial variant.
- **The Bank of England.** Black Wednesday (16 September 1992; Bank of England Quarterly Bulletin 1992 Q4) and the
  Bernanke Review (April 2024) supply the cases, not the mathematics.

**P5's combination was not found in a limited search.** Every ingredient is published:
- erasure (Armstrong & O'Rorke);
- identifying the effect of one's own forecasts (Mendler-Dünner et al. 2022);
- drift (Lee & Zrnic 2026);
- time-structured ways to remove the stake (Krueger et al. 2020; Oesterheld et al.).

So a pass on P5 would be a recombination of known parts, not a new principle. Novelty would need a domain expert.

## The worlds and the checks, each with its expected result (declared before the run)

**World L (linear reflexive).** Y = μ + γ f + ε with ε ~ N(0, σ²).
- f is the published forecast, measured from the empty map (f = 0: no forecast).
- γ > 0 means self-fulfilling; γ < 0 means self-defeating.
- An unread (erased) forecast has no effect: Y = μ + ε.
- **Influence** of f is γ f. **Error when read** is (μ + (γ − 1) f)² + σ². **Counterfactual error** is (μ − f)² + σ².

| id | check | expected |
|---|---|---|
| P1 | **The map–territory trade-off (exact, sympy).** In World L with μ ≠ 0 and γ ≠ 0: (a) zero influence holds only for the empty map f = 0; (b) the error when read is smallest only at the fixed point f\* = μ/(1 − γ) (γ ≠ 1), whose influence is γμ/(1 − γ); (c) the counterfactual map f = μ is wrong when read by exactly its influence γμ. Printed on a grid γ ∈ {−1.5, −0.5, 0.5, 0.9, 0.99} with μ = 1, σ = 1 | holds (identities). No map is both influence-free and right when read unless μ = 0 or γ = 0. The influence of the right-when-read map diverges as γ → 1: the reflexive spiral |
| P2 | **Learning from a territory one has changed** (repeated retraining; the cobweb). A forecaster updates f ← f + α(y − f) on the outcomes its own read forecasts produced. Mean dynamics m' = (1 − α(1 − γ)) m + αμ. It converges iff 0 < α(1 − γ) < 2; it oscillates when α(1 − γ) > 1; for γ > 1 it diverges for every α > 0 (the self-fulfilling spiral). Simulated (5000 steps, 20 seeds) on γ ∈ {−3, −1, 0, 0.5, 1.2} × α ∈ {0.05, 0.3, 0.8}, against the analytic rule. The Regeneration Law's gain K(v) for the unperturbed world is printed beside it, with whether K(v)(1 − γ) < 2 | the analytic rule classifies every cell (converge / oscillate / diverge) as the simulation does. The memory depth that is optimal without feedback can destabilise a strongly self-defeating world |
| P3 | **The map chooses the territory** (bistable, a currency peg). The probability of devaluation when a forecast f is read is p(f) = 0.1 + 0.88 Φ((f − 0.45)/0.1): the attack grows with the forecast. When the forecast is unread, speculators see only the fundamental signal θ = 0.3, so p∅ = p(θ). Printed: (a) the fixed points of f = p(f) and their stability; (b) where repeated retraining ends from starts f₀ ∈ {0.05, 0.25, 0.45, 0.5, 0.7, 0.95}; (c) the forecast that minimises the expected Brier score when read, argmin over f of p(f)(1 − f)² + (1 − p(f)) f² on a grid of 10⁻⁴ (the accuracy-maximising forecaster); (d) where the counterfactual forecast f = p∅ leads when read | (a) three fixed points: a calm one near 0.1, an unstable one near 0.45, a crisis one near 0.98; (b) retraining ends at calm from low starts and at crisis from high ones, so the starting belief picks the outcome; (c) the accuracy-maximising forecast sits at the crisis, because the crisis is the more predictable equilibrium (lower p(1 − p)); (d) the counterfactual forecast leads to the calm equilibrium. **Under a proper scoring rule, a forecaster whose forecasts are acted on is paid to select the crisis** |
| P4 | **Goodhart.** The goal is G ~ N(0, 1). The indicator is X = G + 0.5 η + s Z, where s is the stake attached to the indicator and Z ~ \|N(0, 1)\| is each agent's capacity to game it, independent of G. Printed for s ∈ {0, 0.25, 0.5, 1, 2} (200 000 agents, seed fixed): corr(X, G), and the mean G of the top 10 % selected on X | both fall monotonically in s. At s = 0 they equal the ungamed values (corr 1/√1.25) |
| P5 | **Learning without a stake, in a drifting world** (the one check that could favour a CRR framing). μ_t is a random walk (sd q per step). γ is constant. Each forecast is erased (unread) with probability e = 0.1. Three forecasters, each with its own gains tuned on a grid on the world it is scored in (a baseline that can win): **A** retrains on every outcome (accuracy-seeking); **B** is the counterfactual oracle, learning μ only from erased episodes; **C**, the cut forecaster, estimates its own influence γ̂ by normalised least mean squares on read episodes, removes it from every read outcome (y − γ̂ f) and learns μ from all episodes ("regenerate from the settled past with the map's content cut out"). Scored by the RMSE of f − μ_t (distance from the counterfactual truth) and the mean bias f − μ_t, 20 seeds × 20 000 steps | **gate:** G+ (γ = 0.5 constant, q = 0.05): C's RMSE ≤ 0.9 × B's on at least 18 of 20 seeds, **and** A's mean bias is within 10 % of γμ/(1 − γ) averaged (the self-consistent map's stake). G− (γ itself a random walk, sd 0.05 per step, so the removed influence is stale): C must NOT be ahead (C's RMSE > 0.9 × B's on at least 18 of 20 seeds). G0 (γ = 0: no reflexivity): C and B both unbiased; C ahead only by using ten times the data. **If G− passes, C's advantage is not about removing its own influence, and the claim is withdrawn** |

## What each result means (stated before the run)

**P1–P4 are the articulation, not evidence for CRR.**
- The mathematics is performative prediction, rational expectations, currency-crisis theory and Goodhart's law. The
  literature check says which parts are known (all of them are expected to be).
- What they make precise is the owner's sentence:
  - every map with content moves its territory;
  - the empty map is the only one whose truth is unconditional;
  - a forecaster paid for accuracy when read has a stake in steering the territory, and in a bistable world is paid to
    steer it to the more predictable equilibrium, which may be the crisis.

**P5 is the one place a CRR framing could add something.**
- CRR's framing is learning from the settled past with the map's own content removed at the cut, rather than only from
  the rare unread episodes. If C beats the counterfactual oracle under G+ and fails under G−, the framing has a working
  design.
- Whether that design is new is for the literature check to say. If it matches "predicting from predictions" or causal
  deconfounding, it is REDUNDANT with that literature, and the write-up says so.

**What would make the articulation wrong.**
- P3's accuracy-maximising forecast not sitting at the more predictable equilibrium.
- P2's rule misclassifying a simulated cell.
- P1's identities failing, which would mean the implementation is wrong.
