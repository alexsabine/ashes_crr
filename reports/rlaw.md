# Study RLAW: The Regeneration Law (CRR 2.0) on five domains where it can fail

- **Written:** 2026-09-25, after the ledger rows RLAW-1 … RLAW-C existed. Every number here is in those rows or in
  `runs/rlaw/score.txt`, `runs/rlaw/summary.txt`, `runs/rlaw/diag_kinf.txt` or `runs/rlaw/rerun_check.txt`.
- **Pre-registration:** `prereg/rlaw/PREREG.md`.
  - The sha256 of HASH.txt starts dc8a7101 (prereg commit be82a3f, 2026-09-24T05:50:35Z). All 16 covered files were
    verified at the data step (`runs/rlaw/hash_check.txt`).
  - **Anchor: strong.** The OpenTimestamps proof is complete in Bitcoin block 968363 and later
    (`runs/rlaw/ots_upgrade.txt`).
  - The data step started 2026-09-25T00:40:40Z, after 00:00 UTC as R3 requires. 182 files, sha256 in
    `data/manifests/rlaw.sha256`.
- **Owner request:** prompt-log entries 137, 139 and 140. The owner named CRR 2.0 "The Regeneration Law".
- **Ladder:** at the owner's request (prompt-log entry 139), RLAW rows stay out of the epistemic ladder.

> **Read this first.** Every admissible row FAILs, and no failure is fragile.
>
> - **The law is refuted in its universal form (RLAW-U, 0 of 5 domains).** In four domains (forecasters, households,
>   option markets, soil) the systems keep a much longer memory than α\* = K(v_own) says. Humans in the two-step task
>   keep a much shorter one.
> - **The CRR-only claim fails (RLAW-C).** Soil at 5 cm, a system that does no inference, does not set its memory by its
>   input's drift: 0 of 112 units within a factor of 2, and no rank tracking (Spearman −0.065). The prereg said this is
>   what physics expects. CRR stays a grammar on this route (R12).
> - **The law also loses to a plain constant in every domain.** The strongest simple alternative (the median memory of
>   the domain's other units) is closer than the law everywhere.
> - The one pass as computed, deeper-soil tracking (RLAW-4DT, Spearman 0.523), is FRAGILE: it flips in 8 of 15 cells.

## 1. The question

The Regeneration Law says that a system which regenerates from its settled past weights its newest input by
α\* = K(v_own), where K(v) = (v/2)(√(v² + 4) − v). Here v_own is the drift of the input per occasion, measured in the
system's own resolvable steps.

For inferring systems, K is Muth's steady Kalman gain, so passes there would show only the known neighbour. The row
that is CRR's own is soil (RLAW-C): a system with no inference, whose memory the law says should still follow the
drift.

## 2. Instrument checks

- **Data.** All 182 raw files are in the manifest with their sha256, URL and download time. Every source was absent from
  `data/SEEN.md` before the hash, and all of them are SEEN now.
- **R9.** A second full run of the frozen scorer is byte-identical to the first (`runs/rlaw/rerun_check.txt`).
- **Exclusions**, applied by the frozen scorer before scoring and listed per unit in `score.txt`:
  - SPF, Michigan and implied vol: none.
  - Soil 5 cm: 47 of 159 station files (fewer than 300 rows or input values).
  - Deeper soil: 267 of 636 station × depth units (missing probes, or fewer than 300 rows or inputs).
  - Two-step: 9 of 206 subjects (fewer than 100 valid trials).
- **α̂ ≤ 0** was kept and counted outside every band, as registered: UNEMP and TBILL (SPF), OVX (implied vol).
- **A v fit at the grid edge** was flagged and kept, as registered: SPF 3/8, Michigan 3/3, soil 5 cm 64/112, deeper
  soil 366/369.

### A scorer defect in the sensitivity cells, and why it changes nothing

- **The defect.** The frozen moments estimator returns v = ∞ when the lag-1 autocovariance of the first differences is
  non-negative (no measurement noise). K(∞) should be its limit, 1. The frozen K instead evaluates ∞·(∞ − ∞) = NaN, and
  the scorer then counts the unit outside every band. This is the RuntimeWarning in `runs/rlaw/score_err.txt`.
- **Where it matters.** Only where α\* is taken on the instrument unit with the moments estimator (the four
  `v:mom own:off` cells). With the own unit switched on, v_own stays finite.
- **What was done.** The frozen files were not changed. A post-hoc diagnostic (`runs/rlaw/diag_kinf.py`) imports the
  frozen scorer unchanged and re-scores the moments cells with K(∞) = 1.
- **Result (`runs/rlaw/diag_kinf.txt`): no verdict changes in any cell of any domain.**
  - The largest effect is on deeper soil at `v:mom own:off lag:+0`: 1 → 140 units within ×2. That is still below 246,
    and the row still FAILs.
  - The same diagnostic shows that the moments estimator finds no noise component at all on 366 of 369 deeper-soil
    units, and on 50 to 67 of 112 soil 5 cm units.
- **Logged** as AGENT_LOG 129.

## 3. Results (ledger rows)

| row | criterion | observed | verdict |
|---|---|---|---|
| RLAW-1 (SPF) | ≥ 6 of 8 within ×2, and beats the constant | 1/8; law median \|log err\| 2.662 vs constant 0.682 | **FAIL** |
| RLAW-2 (Michigan) | all 3 within ×2, and beats the constant | 0/3; law 2.913 vs constant 1.210 | FAIL as computed; no counted verdict (not admissible) |
| RLAW-3 (implied vol) | all 5 within ×2, and beats the constant | 1/5; law 1.761 vs constant 0.285 | **FAIL** |
| RLAW-4 (soil 5 cm) | ≥ 75 of 112 within ×2, and beats the constant | 0/112; law 1.580 vs constant 0.392 | **FAIL** |
| RLAW-4T | Spearman ≥ 0.3, CI above 0 | −0.065 (CI −0.248 to 0.134) | **FAIL** |
| RLAW-4D (soil 10–100 cm) | ≥ 246 of 369 within ×2, and beats the constant | 140/369; law 0.891 vs constant 0.481 | **FAIL** |
| RLAW-4DT | Spearman ≥ 0.3, CI above 0 | 0.523 (CI 0.439 to 0.600) | PASS as computed, **FRAGILE** (8 of 15 flip) |
| RLAW-5 (two-step) | ≥ 99 of 197 within ×2 | 6/197 | **FAIL** |
| RLAW-U | ≥ 4 of 5 domain rows | 0/5 | **FAIL** |
| RLAW-C | RLAW-4 and RLAW-4T | both FAIL | **FAIL** |

## 4. The per-unit distributions (primary cell; `runs/rlaw/summary.txt`)

Every unit's α̂, α\*, Muth's K(v), v̂, v_own and signed log ratio is printed in `runs/rlaw/score.txt`. Here, log(α̂/α\*)
by domain (finite units only):

| domain | units | min | q25 | median | q75 | max | α̂ below α\* / above | within ×2 |
|---|---|---|---|---|---|---|---|---|
| SPF | 8 (2 with α̂ ≤ 0) | −2.881 | −2.747 | −2.261 | −2.025 | −0.377 | 6 / 0 | 1 |
| Michigan | 3 | −4.311 | −3.612 | −2.913 | −2.518 | −2.123 | 3 / 0 | 0 |
| implied vol | 5 (1 with α̂ ≤ 0) | −2.314 | −1.899 | −1.688 | −1.320 | −0.435 | 4 / 0 | 1 |
| soil 5 cm | 112 | −3.512 | −1.973 | −1.580 | −1.242 | −0.701 | 112 / 0 | 0 |
| soil 10–100 cm | 369 | −6.966 | −1.657 | −0.891 | −0.535 | 0.010 | 358 / 11 | 140 |
| two-step | 197 | −2.128 | 1.386 | 2.238 | 2.797 | 3.170 | 21 / 176 | 6 |

**The failure has a direction.**
- **Forecasters, households, option markets and soil** use far less of the newest input than the law says.
  - Median α̂ against median α\*: SPF 0.0583 vs 0.7478; soil 5 cm 0.1901 vs 0.9997; deeper soil 0.3978 vs 0.9982.
  - In the gate's vocabulary these systems look like G-under, the sluggish surrogate, which the gate showed fails the
    domain row.
- **Human learners in the two-step task** use far more: median α̂ 0.3938 against the optimal constant rate 0.0420. That
  is the over-reactor, G-over.

**Soil is the clearest case.**
- The ML fit puts v at the top of the grid for 64 of 112 soil 5 cm units. Air temperature looks like an almost noiseless
  random walk at the day scale, so the law predicts α\* ≈ 1, almost no memory.
- Soil at 5 cm keeps a memory of several days (median α̂ 0.19), set by its thermal diffusivity and depth, not by the
  statistics of the air temperature.
- That is what the prereg said physics expects. Soil's memory comes from its own dynamics, not from an inference-optimal
  weighting of its input.

## 5. Sensitivity (16 cells per row; `runs/rlaw/score.txt`)

| row | alternative cells whose verdict flips | fragile? |
|---|---|---|
| RLAW-1, 2, 3, 4, 4D, 5 (row, level, baseline) | 0 of 15 each | no |
| RLAW-4T | 0 of 15 | no |
| RLAW-4DT | 8 of 15 (every own:off cell reads FAIL) | **yes** |

- **Deeper-soil tracking holds only with the own unit.** In every cell where α\* is taken on the instrument unit
  (own:off), tracking fails. Even so, the level test fails there too: at most 140 of 369 units within ×2 in any cell.
- **The own unit does not rescue any domain row.** In the two-step domain, switching the factor (there it is Q₀) moves
  the level from 6 to 13–15 subjects out of 192–197.

## 6. What the results mean, and what they do not

1. **The universal form of the Regeneration Law is refuted on unseen data**, under a strongly anchored prereg, with no
   fragile failure. That is a clean negative result, and the ledger records it as such.
2. **The CRR-only content failed.** A system that does no inference does not set its memory by its environment's drift.
   On this route CRR stays a grammar (R12). No weaker hypothesis is written to replace it.
3. **The inferring domains did not reproduce Muth's law either.** RLAW-1 and RLAW-3 fail both the level and the
   constant comparison.
   - That is not a refutation of Kalman filtering. Nothing guarantees that SPF medians, the Michigan median or
     option-implied variance behave as Muth's optimal forecaster in the local-level model. This study cites no source
     on why they do not, so it gives no reason.
   - What fails here is the claim that K(v_own) predicts their memory.
4. **What it is not.** It does not bear on H-L5, H-T1, H-EQ or H-CUT, or on the empty-cut construction. Those are
   separate rows. RLAW rows stay out of the epistemic ladder, as the owner asked.

## What a surrogate would have done

The gate (`prereg/rlaw/gate_RLAW.txt`) ran the frozen scorer on synthetic domains before the hash:

- **G+ passed every admissible row** in 0.875 to 1.000 of replicates.
- **Every must-fail surrogate passed at most 0.05 of the time**: G-over (3 × K\*), G-under (K\*/3), G-free (memory
  independent of drift) and G-LTI (one memory per domain).
- So a law-obeying system would have passed, and the rows are not forced to FAIL by the arithmetic.

The real systems failed the way the must-fail surrogates do:
- the forecasters, markets and soil like G-under;
- the two-step learners like G-over;
- soil 5 cm, with no rank tracking, also like G-free.
