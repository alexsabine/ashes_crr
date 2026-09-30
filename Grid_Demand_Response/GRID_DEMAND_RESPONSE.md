# DR1: the empty-pause contract for grid demand response — what the full checks found

**What this is.**
- Owner request, prompt-log entry 241: "Please run full checks on grid demand response."
- The declaration (`DECLARATION.md`, e67e8ee) was pushed before any source, code or data.
- Status: a note, not evidence (R8). The model checks are synthetic (rung R4). The data part is an application calculation
  on public GB records, not a test of a CRR hypothesis, so it has no ledger row.
- CRR supplies only the condition: zero content at the pause, meaning a lossless pause whose deadline runs on the job's own
  clock (ETM, the stop-the-clock contract). The economics, grid engineering and contracts are the fields' own.
- Every number below is from a pinned output named beside it.

## 1. What the sources say (`checks/grade.txt`; 173 claims, 296 quotes, `checks/verify.txt`)

| id | position | grade | declared | |
|---|---|---|---|---|
| G1 | AI and data-centre load is already used for demand response | REDUNDANT | REDUNDANT | hit |
| G2 | a job's curtailment cost is its opportunity cost, which sets the payment it needs | PARTLY REDUNDANT | PARTLY REDUNDANT | hit |
| G3 | a lossless pause makes that cost about the restart overhead | PARTLY REDUNDANT | PARTLY REDUNDANT | hit |
| G4 | a deadline-extension (stop-the-clock) contract; industry uses slowdown tiers | extension NOT FOUND IN THE SWEEP; tiers REDUNDANT | same | hit, hit |
| G5 | flexible AI load carries grid-safety risks (ramps, swings, rebound) | REDUNDANT | REDUNDANT | hit |
| G6 | a lossless pause needs a save first, which limits the products it can meet | PARTLY REDUNDANT | PARTLY REDUNDANT | hit |
| G7 | demand-response payments are small against a training fleet's compute cost | ADDRESSED (answer: REDUNDANT) | MIXED | miss |
| G8 | the main commercial value is faster grid interconnection, not event payments | ADDRESSED (answer: REDUNDANT) | REDUNDANT | hit |
| G9 | power capping is an alternative to pausing, with different effects | PARTLY REDUNDANT | REDUNDANT | miss |

**8 of 10 grades hit** the declared expectation.

**The grades are one grading agent's readings, not yet reviewed by the investigator.**
- Under the families' proposed readings the same rule gives 6 of 10 (the sensitivity block of `grade.txt`).
- The completeness critic counted 17 single readings that would each flip a grade (item 20, below).
- "G4 extension NOT FOUND" means only that no source reached in one day's sweep states it. It is not a finding of novelty.

## 2. The eight model checks and the data application (`checks/dr_summary.txt`)

**The battery gate is OPEN**, but only under the scripts' reading:
- G-ZERO holds in 9 of 9 with the stake counted beyond R + S (the restart plus the save).
- G-NEG holds in 9 of 9, but it cannot fail in these models: with no events, every arm is identical.
- G-POS holds in H1.
- Read literally ("beyond R"), G-ZERO fails wherever the save S > 0 (critic item 16).

| check | declared prediction | Q | forecast |
|---|---|---|---|
| H1 | ETM's minimum payment is R/H at every offer; OWN's and WALL's rise as slack falls | holds | hit |
| H2 | ETM and the best slowdown tier supply the same curtailed energy within 1 % | fails: 0 of 8 cells within 1 % (max gap 0.016393 to 0.090909) | miss |
| H3 | ETM's supply curve is flat at R/H; the others rise | holds | hit |
| H4 | ETM's minimum payment stays below OWN's at every overhead and length | fails: strictly below in 300 of 1400 cells, equal in 1100, never above | miss |
| H5 | a simultaneous resume makes a rebound peak equal to the curtailed load; staggering removes it | holds (9 of 9; 63 of 63) | hit |
| H6 | where the save time exceeds the product's response time, ETM cannot meet it without losing work | holds | hit |
| H7 | a throttle also has zero content; it uses less energy per step | holds as pinned; **fragile** (below) | hit as pinned |
| H8 | above R/H ETM supplies all the flexibility; OWN only while slack lasts | fails: OWN supplies beyond its slack above a payment of 27.127027 (H = 1) and 8.366667 (H = 3) | miss |
| DATA | on GB NESO Demand Flexibility Service events, ETM joins every event, and its revenue is below 1 % of compute cost in an ordinary season | fails: part (a) joins every event in 2 of 6 seasons | miss |

**Model checks:** Q holds 5 of 8; forecasts hit 5 of 8.

**Adversarial verification** (`checks/verification.md`): every finding survived its three skeptics. Only H7 drew a major
refutation, from one skeptic of three.

## 3. The follow-up round (POST HOC, not declared; each labelled so in its output)

- **H7 (`checks/followup_1.txt`).** The pinned verdict treats the GPU power ratio as the whole fleet's.
  - At the node-level GPU share from sourced figures, g = 0.549020, **Q fails**. Q holds only for g > 0.879507.
  - The verdict flips at 4 of 5 values of g: **H7 is FRAGILE**.
- **The restart overhead R (`checks/followup_2.txt`).** One assumed value, R = 0.1 h, decides three verdicts. Over the
  sourced range of 5 s to 1200 s:
  - H2 holds only at R ≤ 36.36 s (2 of 9 sourced values);
  - H3 holds only at R ≤ 439.02 s (6 of 9);
  - DATA holds only at R ≤ 99.14 s (2 of 9).
  - With fast, MegaScale-class restarts (5 s or 30 s), H2's and DATA's fails reverse.
- **DATA's scarcity exclusion (`checks/followup_3.txt`).** Leaving out only the scarcity (live) events, as the sources
  describe them, rather than the whole 2022/23 season, **part (b) fails**: W2022/23's share is 1.36917 %. Q still fails,
  on part (a).
- **DATA's margins (`checks/followup_4.txt`).** Part (b) holds at **0 of 6 sourced PUE values**. The break-even compute
  cost for W2023/24 is 1435.62 GBP/MWh, a 1.158 % fall from the scored cost.

## 4. What this adds up to

**The construction works as designed, and that is by construction.**
- In every model, the stop-the-clock job's entry price is its restart and save overhead (G-ZERO).
- It joins every event that pays that overhead and has no stake beyond it.
- That follows from counting the deadline in the job's own steps. It is EPS2's result with more detail, not an
  empirical finding.

**Where it met reality:**
- **The literature** already has AI load in demand response (G1), the grid risks (G5) and slowdown tiers (G4). Nobody
  was found selling a stop-the-clock extension, but that is a one-day sweep.
- **The money is small, and that result is fragile.** On six seasons of real GB event prices, a 100 MW fleet's revenue is
  around 1 % of its compute cost.
  - The pinned run gives 0.19217 % to 1.52265 % per season (`followup_2.txt`, at the assumed R).
  - Whether it stays below 1 % depends on the PUE, the exchange rate and the GPU price (follow-ups 3 and 4).
- **The main commercial case the sources make is faster interconnection (G8).** No source reached puts a money value on
  it (critic item 26).
- **The delay does not disappear.** ETM's zero stake holds because the extension moves the delay (68.1 h late in EPS2
  T1) onto whoever grants it. No check models that party (critic item 6). This is the same point as every EPS system:
  the empty pause buys participation by relocating a cost, not by removing it.
- **The grid-safety side is only partly checked.** The rebound on resume is modelled (H5). The ramp-down at event start,
  fleet loss during faults, oscillations and herding across many fleets with the same entry price are not (critic items
  11–15).

## 5. What the critic listed and the follow-up round did not address

26 items; follow-ups 1–4 addressed items 1–4. Still open:
- 5: DATA's revenue is gross, not net of rent paid while paused.
- 6: nobody bears the deferred delay in the model.
- 7–8: only GB DFS was applied; MISO, NYISO, ISO-NE, SPP, AEMO and Ireland were not swept.
- 9–10: DFS is pay-as-bid, and the main US products are committed, not voluntary per offer.
- 11–15: grid safety beyond the rebound.
- 16–19: the gate's non-literal reading, and the readings behind H1, H3 and H4–H6.
- 20–21: the grades are unreviewed, and the G4 search was thin.
- 22–23: some sources were not reached, and the quote verification depends on fetched texts outside the repository.
- 24–26: record-keeping, author slips, and G8 has no money figure.

The full list is in the workflow record (AGENT_LOG 200).

## 6. Files

- **Declaration:** `DECLARATION.md`.
- **Sources:** dossiers `docs/citations/dr1_f{1..5}_2026-09-29.md` and `dr1_followup{1,3,4}_2026-09-29.md`.
- **Grades:** `checks/claims.py`, `grade.py/.txt`, `verify.py/.txt`.
- **Model and data checks:** `checks/drlib.py` (selftest 31/31), `dr_h1…h8.py/.txt`, `dr_data.py/.txt`, `dr_summary.py/.txt`.
- **Verification and follow-ups:** `checks/verification.md`, `checks/followup_1…4.py/.txt`.
- **Data:** `data/MANIFEST.md`, `data/fetch_dfs.py`, `data/raw/` (GB NESO DFS, sha256 in the manifest).
