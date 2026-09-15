# How a study runs, end to end

> Explanatory narration of CLAUDE.md §8 ("Command sequence for a study").
> **CLAUDE.md is normative**; on any conflict it wins. Rules cited as R#
> are explained in [rules.md](rules.md).

A study is a one-way street: hypothesis gate → prereg → hash → anchor →
tag → **only then** data → frozen run → ledger row → report. Each step
below states what it does, what it produces, and what is forbidden at
that point.

---

## Step 0 — Environment (R9)

```bash
uv sync && uv lock --check && uv run python -c "import numpy, scipy; print('ok')"
```

Pinned, locked, reproducible. Nothing runs on an unpinned tree.

*Forbidden:* proceeding with a dirty or unlocked environment; any `pip`
or bare `python` invocation.

## Step 1 — Phase A: instrument tests + surrogate gate (R4)

```bash
./scripts/check_all.sh                                     # tests + symbolic checks + all gates
uv run python -m crr.surrogates.gate <HYP> > prereg/<study>/gate_<HYP>.txt
```

Every hypothesis to be pre-registered gets its gate output computed and
committed into the prereg folder. The gate must read **GATE OPEN** — a
PASS on a negative control or a FAIL on a positive control closes the
gate (see [modules/surrogates.md](../modules/surrogates.md)).

*Forbidden:* entering a hypothesis into a prereg whose gate row reads
PASS on a "must fail" surrogate; proceeding while any gate reads GATE
CLOSED.

## Step 2 — Draft the prereg; freeze the scripts

```bash
mkdir -p prereg/<study> runs/<study>/frozen
cp src/crr/instrument/core.py prereg/<study>/<study>_score.py theory/CRR.md runs/<study>/frozen/
```

`PREREG.md` is written from [`prereg/PREREG_TEMPLATE.md`](../../prereg/PREREG_TEMPLATE.md):
hypotheses with ids matching `theory/CRR.md`, the data (exact record ids,
each confirmed absent from [`data/SEEN.md`](../../data/SEEN.md)), every
named instrument parameter, the baseline set (R7), the sensitivity table
plan, and the path of the frozen scoring script. The scoring script is
written into the prereg folder — it is covered by the hash — and
`runs/<study>/frozen/` holds byte-identical copies taken at freeze time.

*Forbidden:* naming a threshold that is not also swept in the planned
sensitivity table (R5); scoring "per study" where the prereg will say
per level/subject (R6).

## Step 3 — Hash + anchor + tag (R2) — BEFORE any data

```bash
( cd prereg/<study> && find . ../../runs/<study>/frozen -type f | sort | xargs sha256sum > HASH.txt )
uv run ots stamp prereg/<study>/HASH.txt          # produces HASH.txt.ots
git add -A && git commit -m "prereg <study>" && git tag -s prereg-<study>-$(date -I) -m "prereg"
git push --tags
```

The hash covers the prereg folder **and** the frozen scripts. The
OpenTimestamps proof is the evidence of "before"; the signed tag is the
commit boundary.

*Forbidden:* downloading or opening **any** data for the study before
this tag exists — not a byte, not a peek.

## Step 4 — Data (only now) (R11)

```bash
uv run python data/fetch_<dataset>.py --records <range> && uv run python data/manifest.py
```

Append opened records to `data/SEEN.md` **in the same commit** as the
download.

*Forbidden:* opening records not named in the prereg; reusing a record
already in SEEN.md as "held-out".

## Step 5 — Frozen run (R9)

```bash
uv run python runs/<study>/frozen/<study>_score.py > runs/<study>/stdout.txt
uv run python runs/<study>/frozen/<study>_score.py > runs/<study>/stdout_rerun.txt
cmp runs/<study>/stdout.txt runs/<study>/stdout_rerun.txt
```

The study runs the **frozen copy**, twice, byte-identical (`cmp`). A
non-byte-identical rerun must be documented why and downgraded to
tolerance-level reproduction.

*Forbidden:* editing anything under `runs/<study>/frozen/` (write-once
after the tag); reporting in-sample fits.

## Step 6 — Ledger row, then report (R8)

```bash
uv run python ledger/append.py runs/<study>/results.json
```

`ledger/LEDGER.md` gets one row per committed prediction, in prereg
order, linking the script and the log. `reports/<study>.md` is written
**after** its rows exist, contains no number absent from `runs/`,
includes the sensitivity table and the exclusion count, and ends with a
"What a surrogate would have done" paragraph pointing at the gate table.

*Forbidden:* editing or deleting a ledger row (rows are appended;
corrections are new rows referencing the old id); a report number that
no row contains.

---

## Stop conditions and voiding

- **R12:** if Phase A leaves no hypothesis standing, stop, write that in
  the ledger, and report. Do not invent a weaker hypothesis.
- **Voided study:** if a script must change after step 3's tag, the
  study is void — start a new study id with a fresh prereg.

## Helper scripts that do not exist yet

CLAUDE.md §8 references three helpers that the tree does not yet contain;
they must be written **before the first study reaches their step**:

| script | lifecycle step | status |
|---|---|---|
| `data/fetch_<dataset>.py` | step 4 | to be written |
| `data/manifest.py` | step 4 | to be written |
| `ledger/append.py` | step 6 | to be written |

Until they exist, the corresponding steps cannot be performed, which is
itself a stop condition: a study cannot reach step 4 without a fetch +
manifest path, and step 6 without a ledger append path.
