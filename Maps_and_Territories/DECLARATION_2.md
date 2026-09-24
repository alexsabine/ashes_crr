# Declaration 2 (POST HOC) — P5 re-tested with the corrected bias target, on fresh seeds

- **Written:** 2026-09-24, after `checks/performativity.txt` (Declaration 1) was pinned. Pushed before
  `checks/performativity_2.py` exists.
- **This declaration is post hoc.** It follows a result that read GATE CLOSED (AGENT_LOG 117). It is labelled post hoc
  wherever it is quoted, as the Adam_SGD redesign was.

## The one change

**Declaration 1's G+ condition on the accuracy-seeking forecaster A** was "mean bias within 10 % of γμ/(1 − γ)". That is
the fixed point when every forecast is read. With erasure probability e, only a fraction 1 − e of forecasts move the
outcome, so the fixed point is

  f\* = μ / (1 − (1 − e)γ), and the bias f\* − μ = (1 − e)γ μ / (1 − (1 − e)γ).

At γ = 0.5 and e = 0.1 that is 0.8182 μ, not 1.0 μ. The corrected condition is: A's pooled mean bias lies within 10 % of
(1 − e)γμ/(1 − (1 − e)γ).

**Nothing else changes.**
- The same worlds, forecasters, gain grids, metrics and thresholds as Declaration 1.
- C must beat B (RMSE ≤ 0.9 × B's) on at least 18 of 20 seeds under G+.
- C must NOT be ahead on at least 18 of 20 seeds under G−.

## Fresh seeds

**Seeds 20–39**, where Declaration 1 used 0–19. The world generator's seed is 5000 + seed + 1000 × world, as before. The
gains are re-tuned on the new seeds, by the same rule.

## Expected (declared before the run)

- **G+:** C ahead on ≥ 18/20. A's bias ratio to the corrected target within [0.9, 1.1].
- **G−:** C not ahead on ≥ 18/20.
- The gate reads OPEN.

**If it reads CLOSED on fresh seeds, the P5 result is not robust, and the write-up says so.**
