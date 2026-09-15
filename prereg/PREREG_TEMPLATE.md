# Pre-registration — <study id>

Written: <ISO datetime>. Hash and OpenTimestamps proof in HASH.txt / HASH.txt.ots.
Signed tag: prereg-<study>-<date>. **No data listed below has been opened.**

## Hypotheses (from theory/CRR.md; ids must match)
| id | statement | PASS if | FAIL if | scored per | gate table |
|---|---|---|---|---|---|
| H-… | … | … | … | level / subject / seed | gate_<id>.txt (committed here) |

For each hypothesis (R4): which surrogates must fail it and BY HOW MUCH —
the must-fail surrogate, the margin it fails by in the gate table, and the
margin the study requires on real data.

## Analysis conventions (stated per hypothesis; R6)
- Aggregation: what is pooled, what is not; the denominator of every
  fraction (who is counted, who is excluded and where they are listed).
- Strict vs non-strict: every threshold says whether equality passes.
- Sidedness: two-sided unless the prereg justifies one side, per test.

## Seeds and determinism (R9)
- Every stochastic step names its seed / seed rule (generator, draws).
- Determinism statement: which steps must reproduce byte-identically
  (two reruns, `cmp`), which are only tolerance-level reproducible and why.

## Data
Dataset, version, exact record ids, download source, sha256 manifest path.
Confirm each id is absent from data/SEEN.md.

## Instrument parameters (all named)
unit statistic; detrender + window; MAD/std; instrument quantisation step;
phase method; ρ floor; minimum cycles; NaN rule; exclusion rules.

## Baselines
List every control arm and the published method it corresponds to.

## Sensitivity table (required in the report)
Parameters swept and the rule for calling a verdict "fragile".

## Scoring script
Path of the frozen script; its sha256 is inside HASH.txt.
