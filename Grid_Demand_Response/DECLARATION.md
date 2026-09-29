# Declaration: DR1, full checks of the empty-pause contract for grid demand response (pushed before any source, code or data)

**Status.**
- **The request.** Owner request, prompt-log entry 241 (2026-09-29): "Please run full checks on grid demand response."
- **Where it comes from.** EPS2 T1 (`Empty_Pause_Systems/EMPTY_PAUSE_SYSTEMS.md` §6). In a synthetic model, a training job
  whose deadline runs on its own clock (a lossless pause, the empty true map, ETM) sells every curtailment hour at its
  restart cost (0.025 per curtailed hour at R = 0.1 h, H = 4 h). The other arms needed 6.12–15.73, and the job finished
  68.1 h late. The EPS2 sources qualified this:
  - industry contracts use pre-agreed slowdown tiers;
  - no source prices a curtailment at the job's opportunity cost;
  - the Phoenix field trial treats checkpoint overhead as negligible.
- **What "full checks" means here (the investigator's reading, fixed now).** Four parts: a systematic literature and
  industry sweep graded against declared positions (§1); eight synthetic model checks, each with a declared prediction and
  forecast (§2); a real-data application on public demand-response event data, with its protocol fixed now (§3); and an
  adversarial verification of every finding, plus a completeness critic (§4).
- **Rung and status.** The model checks are R4. The data part is an application calculation on public data, not a test of
  a CRR hypothesis: no ledger row. A note, not evidence (R8). "Not found" is never "novel". CRR supplies only the condition
  (zero content at the pause); the economics, the grid engineering and the contracts are the fields'.

## 1. The literature and industry sweep (positions graded; rule as in `AI_Safety/CORRIGIBILITY_2026`)

**The grading rule.** Each position is graded from claims with verbatim quotes, fetched on the day:
- REDUNDANT if a source states it;
- PARTLY REDUNDANT if a source is close;
- NOT FOUND IN THE SWEEP otherwise;
- MIXED where sources disagree;
- ADDRESSED where the position is a question the sources answer.

The per-claim reading (states / close / bears / contradicts) is the investigator's, printed with the quote.

| id | position | expected grade |
|---|---|---|
| G1 | AI training and data-centre load is already used for demand response in the field | REDUNDANT |
| G2 | a training job's cost of a curtailment is its lost work plus restart plus deadline pressure (its opportunity cost), and this sets the payment it needs | PARTLY REDUNDANT |
| G3 | a lossless pause (checkpoint and resume, nothing lost) makes the job's curtailment cost about the restart overhead | PARTLY REDUNDANT |
| G4 | a contract that extends the job's deadline by the curtailed time (stop-the-clock) elicits full participation at the restart cost; industry instead uses slowdown tiers | NOT FOUND IN THE SWEEP (the extension); REDUNDANT (the tiers) |
| G5 | flexible AI load carries grid-safety risks: synchronized ramps and power swings, and a rebound peak when paused jobs resume together | REDUNDANT |
| G6 | a lossless pause needs a checkpoint save before the power drops, which limits the demand-response products it can meet (response-time requirements) | PARTLY REDUNDANT |
| G7 | demand-response payments are small against the compute cost of a training fleet | MIXED (expected: small, with exceptions in scarcity events) |
| G8 | the main commercial value of flexible AI load is faster or larger grid interconnection, not event payments | REDUNDANT |
| G9 | power capping or throttling (running slower) is an alternative to pausing, with different energy and grid effects | REDUNDANT |

**The sweep's families** (each a separate dossier `docs/citations/dr1_<family>_2026-09-29.md`, every quote verified
against its fetched text by a script, and every unreached source marked NOT REACHED):
- F1: data centres and AI training as flexible load: industry announcements, field trials, research;
- F2: demand-response programme design and prices, in at least two markets with public rules (for example GB NESO's
  Demand Flexibility Service and a US ISO/RTO programme);
- F3: grid-reliability sources on large flexible loads, ramps, rebound and response times (for example NERC, ERCOT,
  EPRI);
- F4: the engineering of pausing training (checkpoint save and restore times at scale; power capping);
- F5: the economics (interconnection value, flexible-connection offers, compute cost per MWh).

## 2. The model checks (synthetic; `checks/dr_h1.py` … `dr_h8.py`, each pinned with its `.txt`, run twice and compared with `cmp`)

**Common setting.**
- **Units.** EPS2 T1's units unless a check says otherwise: W = 1000 compute-hours, value 1 per compute-hour at
  completion, restart R, event length H.
- **Arms.**
  - **WALL:** value on the wall clock, with the wall-clock deadline;
  - **OWN:** value on its own steps, with the wall-clock deadline;
  - **ETM:** a lossless pause with the deadline counted in own steps (the stop-the-clock contract);
  - **TIER:** the industry slowdown-tier contract, a pre-agreed maximum performance reduction over a window;
  - **H0:** an interruptible-load contract priced at the job's opportunity cost.
- **Computed per check.** Every verdict word is computed. Every choice is printed as CHOICE; every input number is
  sourced (from the dossiers) or marked ASSUMED.

| id | check | declared prediction (Q) | forecast |
|---|---|---|---|
| H1 | online offers: events arrive as a Poisson process of unknown count; each arm decides per offer | ETM's minimum acceptable payment is R/H at every offer; OWN's and WALL's rise as the slack falls | Q holds |
| H2 | ETM (deadline extension) against TIER contracts (maximum slowdown 10, 25 or 50 % over a 3–6 h window), at matched job delay | at matched delay, ETM and the best tier supply the same curtailed energy within 1 % (ETM is an unbounded tier) | Q holds (REDUNDANT in substance) |
| H3 | a portfolio of 100 jobs with a spread of deadline slack: the fleet's supply curve (curtailable MW against payment) | ETM's curve is flat at R/H; OWN's and WALL's are rising; the gap is largest for tight-slack jobs | Q holds |
| H4 | realistic restart and save overheads (from the F4 dossier, else ASSUMED ranges), event lengths 0.5–4 h | ETM's minimum payment stays below OWN's at every overhead and length; the ratio shrinks as overheads grow | Q holds |
| H5 | rebound: N jobs resume together at the event's end | a lossless pause resumes at full power at once, so the rebound peak equals the curtailed load; a staggered resume removes it at a cost; the cost of staggering is printed | Q holds (REDUNDANT: rebound is known) |
| H6 | response time: a lossless pause must save before the power drops; demand-response products need response within T | where the save time S exceeds T, ETM cannot meet the product without losing work; the feasible product set is printed | Q holds |
| H7 | power capping (a throttle) against a full pause, with a declared performance–power curve | a throttle also has zero content on the own clock; its energy per step is lower; the curtailed MW per unit of delay is compared | Q holds |
| H8 | the value to the grid: curtailable MW-hours per season under each arm's minimum payment, at a price grid | at every payment above R/H, ETM supplies all the flexibility; OWN supplies it only while slack lasts | Q holds |

**The gate (all eight).**
- **G-ZERO:** ETM's stake beyond R is exactly 0 in every cell.
- **G-POS:** OWN or WALL declines offers ETM accepts in at least one cell of H1.
- **G-NEG:** with no events offered, ETM is not ahead of WALL on any outcome by more than 1 %.

If the gate closes, the checks are printed and read as "no stake to remove".

## 3. The real-data application (protocol fixed now; data fetched only after this file is pushed)

**The data.** Public demand-response event records with times and prices, from the first reachable of:
1. GB NESO's Demand Flexibility Service: the utilisation or event reports for its seasons (dates, windows, guaranteed
   acceptance prices, volumes);
2. a US ISO/RTO demand-response event history with prices (for example ERCOT or PJM);
3. any other system operator's published event list with prices.

Each file gets a version, a URL, a download date and a sha256 in `Grid_Demand_Response/data/MANIFEST.md`. These records
have never been opened in CRR work (they are not model carriers).

**The calculation** (`checks/dr_data.py`, pinned).
- **The fleet.** A hypothetical AI training fleet of 100 MW (ASSUMED), running jobs of the H3 portfolio.
- **Participation.** At each real event with its real window and price:
  - ETM participates whenever the price covers R/H;
  - OWN participates while slack lasts;
  - TIER participates within its tier;
  - WALL participates when the price exceeds its wall-clock loss.
- **Printed:**
  - events joined, curtailed MWh and revenue per arm;
  - revenue as a share of the fleet's compute cost over the same period (the compute cost per MWh from F5, else ASSUMED);
  - the job delay ETM accepts.

**Declared expectations.**
- ETM joins every event.
- Its revenue is below 1 % of the fleet's compute cost in an ordinary season (G7).
- The commercial value, if any, lies in interconnection (G8), not in event payments.

## 4. Verification and completeness

- **Adversarial verification.** Every model check and the data calculation are reviewed by independent skeptic agents
  prompted to refute them (code against this declaration, arithmetic, choices that decide a verdict). A finding survives
  only if a majority of its skeptics fail to refute it. Refuted findings are reported as refuted, not deleted.
- **Completeness critic.** A critic lists what is missing (a market not covered, a claim unverified, a source unread).
  One follow-up round addresses what can be done on the day; the rest is listed.
- **Every decision is logged** (AGENT_LOG), and every post-first-run change is listed with its reason.

## Outputs

- `Grid_Demand_Response/DECLARATION.md` (this file);
- `docs/citations/dr1_f{1..5}_2026-09-29.md`;
- `checks/claims.py`, `grade.py` and `grade.txt` (the G grades);
- `checks/dr_h1.py` … `dr_h8.py` and their `.txt`;
- `data/MANIFEST.md`, `checks/dr_data.py` and `dr_data.txt`;
- `checks/verification.md` (the skeptics' verdicts);
- `GRID_DEMAND_RESPONSE.md`, written last, quoting the pinned outputs.
