# labs/: from the edge of the retrodictive bank to deductive tests

**Status.**
- **Where it comes from.** Owner request, prompt-log entry 220 (2026-09-26).
- **What this folder is.** A charter and an index, not evidence (R8).
- **How a lab becomes a result.** Only through a pre-registration in `prereg/<study>/` and a ledger row.

## What a lab is

A lab takes one row, or a group of rows, from the retrodictive bank, `checks/bank.txt`. That file holds every SYNTHESIS row
as pinned: 166 rows, of which 98 read REDUNDANT, 29 WRONG and 11 ADDS. From those rows a lab turns CRR's reading into one
deductive test.

**Most rows cannot make a lab.**
- A REDUNDANT row is one where CRR's reading and the domain's own theory give the same number. Data cannot separate them,
  so the redundant part of a row can never become a lab.
- A lab starts at the row's **edge**: the place where the row's own weakness line, or the domain's open question, leaves
  CRR and the domain predicting different things.

## The entry rule: CRR against the domain, not against nothing

A lab file is opened only if all four hold:

1. **H1** names the quantity CRR predicts, from a named ingredient (A1′, A3, A6/P3, H-L5, H-CUT, D6/H-T1, H-EQ,
   Proposition 7).
2. **H0** is the domain's best model: its own theorem, its fitted rule, or the strongest simple alternative (R7). It is not
   "no effect".
3. **The two separate on a synthetic world.** In a world built from the domain's model, H1 and H0 differ by more than one
   resolvable step in the quantity scored.
4. **A synthetic gate can close:**
   - a world where H1 is true by construction reads PASS;
   - the domain's world reads FAIL.

If the gate closes, the lab stops and says so (R12). If H1 and H0 cannot be separated, the file records **"no lab: CRR =
domain"**. That is a finding about CRR, not a gap to fill with a weaker hypothesis.

## Induction, then deduction

- **Induction happens in the bank.** The bank is where hypotheses are **induced**. Its rows are retrodictions on known
  results, the investigator knows the literature, and nothing in it is blind.
- **Deduction needs unseen data.** A deductive test needs data absent from `data/SEEN.md`, the rule fixed and hashed before
  the data are opened (R2), and a data step on a later calendar day than any change to the rule (R3).
- **Rows count on both sides.** A row's WRONG is as useful as its ADDS: it marks where CRR's reading has already failed and
  must not be re-proposed.
- **ADDS is not novelty.** The literature check (`theory/retrodictions/synthesis_batches/literature_check.txt`) found, for
  the 10 ADDS rows it checked:
  - 3 already REDUNDANT-DOMAIN in the literature;
  - 6 whose direction is already known;
  - 1 artefact.

## Where the data come from

| class | meaning | what this repository can do |
|---|---|---|
| **D1** | public, analysis-ready (tables, catalogues, PhysioNet-style records) | the whole pipeline, on CPU, at no cost |
| **D2** | public but needing processing or a loader whose format cannot be checked without opening it | the pipeline, with a written VOID rule; a blind loader voided EQ2R and T1x |
| **D3** | no suitable data exist; a new wet-lab or physics experiment is needed | the protocol, the synthetic gate and a power analysis; running it needs a collaborator and money (the owner's constraint: no spend at this stage) |
| **D∅** | no empirical access (e.g. a cosmological bounce) | a thought-lab only; never a ledger row |

**Checking the data.**
- Availability, version, licence, record IDs and file sizes are checked on the day (R10, R11), from landing pages and
  metadata only.
- No data file is opened before the hash.

## The lab file (one per lab: `labs/Lxx_<name>/LAB.md`)

Each lab file has these fields:
1. **Rows.** Which bank rows the lab comes from (file and row), and their outcomes.
2. **The edge.** The weakness line or open question that leaves H1 ≠ H0, quoted from the row.
3. **The hypotheses.**
   - H1, CRR's prediction, with its ingredient;
   - H0, the domain's model;
   - the scored quantity;
   - the resolvable step.
4. **The synthetic gate.** Its worlds, its pass rule, and its output, pinned.
5. **The data.** The class (D1, D2, D3 or D∅), with candidate sources verified on the day. For D3, the experiment, the
   sample size from the gate's effect size, and what would be needed to run it.
6. **The forecast.** The investigator's expected outcome, with a reason, so that a surprise is visible.
7. **Stop rules.** What closes the lab.

## Order of work

1. `checks/bank.py` → `checks/bank.txt` (CI-checked): the index.
2. `CANDIDATES.md`: the investigator's first shortlist, sorted by the entry rule and the data class. It is judgement,
   labelled as such.
3. **One lab at a time.** For each:
   1. a declaration pushed first;
   2. the synthetic gate;
   3. sources and data availability on the day;
   4. a pre-registration, hashed and anchored, if the gate opens;
   5. the data step on a later day;
   6. the ledger row and the report.
