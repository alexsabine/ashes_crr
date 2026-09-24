# The rule for the literature check of every ADDS row (prompt-log entry 132), fixed before any finding is read

- **Written and pushed:** 2026-09-24, while three research subagents search. No finding has been read.
- **Scope:** every real-domain synthesis row whose pinned OUTCOME is ADDS. The gate's positive control, `synthesis.txt`
  row 1, is excluded as the ladder already excludes it. The rows are:

| row | system |
|---|---|
| batch_12 row 2 | cardiac alternans with memory |
| batch_17 row 1 | Bass diffusion with fading word of mouth |
| batch_28 row 4 | switching contingency: bounded mean against accumulated counts |
| batch_30 row 2 | CNS with lineage-memory inheritance |
| batch_31 rows 1–4 | Ricker, SIR with remembered prevalence, OV traffic, Samuelson with permanent income |
| batch_32 row 2 | FitzHugh–Nagumo H-CUT: forced, AGENT_LOG 109 |
| batch_32 row 3 | Lotka–Volterra with remembered prey |

## What a literature finding does to a row

The pinned batch outputs are **not edited**. The check is a separate pinned script, `literature_check.py`. It prints,
per row, the citation, the finding's class, the domain's value where a formula exists (computed by the script at the
row's parameters), and the row's status after the check. The ladder reads that output and prints R3 "after the literature
check" beside the mechanical R3 count, never in place of it.

| finding | condition | status after the check | rung |
|---|---|---|---|
| **FOUND-EXACT** | a published work states the same model and a formula or theorem that, evaluated by the script at the row's parameters, gives the row's decisive number within 1 % (TOL_N) | REDUNDANT-DOMAIN (literature) | R2 |
| **FOUND-THEOREM** | a published general theorem directly implies the row's claim, e.g. its sign or its threshold, though no paper evaluates this model | REDUNDANT-DOMAIN (literature, by theorem) | R2 |
| **PARTIAL** | the direction, or a close variant (another kernel, another model in the same family), is published, but neither this model's number nor a theorem that yields it | ADDS, direction known | R3, marked |
| **NOT FOUND** | none of the above after the recorded searches | ADDS, candidate | R3, pending a named expert |
| **ARTEFACT** | the row's pass is produced by the estimator or the construction, whatever the literature says (batch_32 row 2, AGENT_LOG 109) | not a candidate | removed from R3 after the check |

## What the check can and cannot do

- **Evidence of absence is weak.** A NOT FOUND is weak evidence of novelty. It records the searches, and the class
  note's rule stands: novelty is judged only by a named domain expert.
- **Unread sources.** Where a source could not be read in full (paywall, JavaScript challenge), the finding says so, and
  the script uses FOUND-EXACT only if the formula itself was read. A formula seen only in an abstract counts as PARTIAL.
- **No rescue.** The check never raises a row. It can only confirm, mark or remove the candidate status.
