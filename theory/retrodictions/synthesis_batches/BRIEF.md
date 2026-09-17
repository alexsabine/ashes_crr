# Brief for writing one synthesis batch (five rows)

You are re-reading five existing retrodiction rows (graded CONSIST or DESCR) under the SYNTHESIS class.
Read, in this order, before writing anything: `CLAUDE.md` §1 (R1, R5, R6, R14, R15) and §7,
`docs/notes/2026-09-17_synthesis_class.md` (the class), `src/crr/synthesis/harness.py` (the API),
`theory/retrodictions/synthesis.py` (a worked battery of eleven rows), the five source rows in their
pinned battery output (the queue names the file and row id), and the clauses of `theory/CRR.md` the
source rows cite.

## The question each row answers

Not "does CRR agree with the domain?" (the source row answered that) but: **taking CRR whole and
integrating it with this domain's own mathematics, is there one proposition Q, in the domain's own
terms, built with a CRR-proper ingredient, that the domain does not already contain?**

CRR-proper ingredients: A3 antipodal cut / D5 occasions; A6 regeneration by a bounded Fréchet mean
("never an accumulated count"); P2/P3 occasion weights; A1′/D1 the system's own unit and ρ; H-L5's class
claim; D6/H-T1 path vs endpoint; H-EQ; A7/A8 tense. NOT proper (information geometry's): A1 the metric,
D2 arc, D3 chord, D4 surplus, P1. A Q built only from non-proper ingredients reads REDUNDANT-IG by
construction (see synthesis.py row 6); write such a row when the source row's content is exactly that,
and say so.

## What the script must do (R15: numbers before words)

For each row, compute in code:
- `crr`: the decisive quantity with the ingredient; `null`: the same with its replacement (T-G);
- `domain`: the domain's own theorem's value for the same target, or `None` if none is cited (T-N);
- `check`: True / False / None (T-C, checked in the domain's own mathematics; None only when the check
  needs data or an unmeasured quantity — then name the data and say it is absent from `data/SEEN.md`);
- pass them to `outcome(...)`; pass `internal=True` when two readings of the ingredient disagree
  (say which, with both numbers), `unstated=True` when no Q could be formed (print what was tried).
Every verdict word in the printed text ("differ"/"agree", "holds"/"fails", the outcome) is computed from
the numbers, never typed. A number that appears in a sentence is an f-string of the computed value.
Reuse the source row's model where it is reproducible from its script (import nothing from
`theory/retrodictions/*.py` — they run on import; re-implement compactly); keep every run deterministic
(fixed seeds, fixed grids, explicit RK4 or fixed-grid RK45), under ~60 s total, no data files (R2).

## Elegance record (prompt-log entry 61)

Do not get side-tracked by it; notice it and record it. When a row shows something elegant — a
statement a child could carry, a picture, a rule with no knobs — fill `elegance=` (one or two
sentences: what is elegant and why it helps teach the principle to children, families and
communities) and `child=` (a fifth-grader explanation, plain words, no numbers unless the row prints
them). Leave both empty when there is nothing; an empty record is a correct record. Elegance never
changes an outcome.

## File format

`theory/retrodictions/synthesis_batches/batch_NN.py`:

```python
"""Synthesis batch NN: rows <first>-<last> of QUEUE.md (prompt-log entry 61). <one line per row: source, topic>."""
import math, sys
import numpy as np
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch
from crr.instrument.core import ...   # what you use

def r1():   # one function per row, returns make_row(...)
    ...
    return make_row("cls", "system", source="<battery file> [<row id>] (<old grade>)", Q=..., ingredient=..., null=..., domain=...,
                    numbers=..., tg=..., tn=..., tc=..., out=out, reading=..., weakness=..., elegance=..., child=...)

def main():
    return run_batch("Synthesis batch NN: rows <first>-<last> (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])

if __name__ == "__main__":
    sys.exit(main())
```

Run `uv run python theory/retrodictions/synthesis_batches/batch_NN.py > theory/retrodictions/synthesis_batches/batch_NN.txt`,
then run it again and `cmp` (must be byte-identical), then read the output as an auditor: does every
sentence match its numbers? If the first run's numbers contradict a row's text, fix the model or the
estimator and regenerate the text (never edit the text to fit) and report what you changed and why in
your final message (it becomes an AGENT_LOG entry). Do not edit any other file. Do not commit.

## Final message

Return: the batch tally line; one line per row (source, Q in ten words, outcome); the list of
model/estimator corrections made after the first run (observed issue → decision → alternative
rejected); and which rows carry an elegance record.
