# Pre-registration — <study id>

Written: <ISO datetime>. Hash and OpenTimestamps proof in HASH.txt / HASH.txt.ots.
Signed tag: prereg-<study>-<date>. **No data listed below has been opened.**

## Hypotheses (from theory/CRR.md; ids must match)
| id | statement | PASS if | FAIL if | scored per | gate table |
|---|---|---|---|---|---|
| H-… | … | … | … | level / subject / seed | gate_<id>.txt (committed here) |

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
