# Life Sciences: CRR on cell division, the origin of life and DNA sequencing

**Status.**
- **The request.** Owner request: prompt-log entry 217 (2026-09-26).
- **The order of work, as the pipeline requires:**
  1. The predictions were declared first, in `DECLARATION_1.md`, pushed at ed4b04a before any source, script or data.
  2. The Phase A script was pushed before its first run.
  3. Sources were fetched on the day.
  4. Labels were computed by scripts.
- **What this is.** A note, not evidence (R8). No ledger row is added: no pre-registered study ran, and a synthetic gate
  that opens or closes is not a result about cells.
- **What every number comes from.** Three pinned outputs:
  - `checks/phase_a.txt` (rerun byte-identical);
  - `checks/grade_origin.txt` (CI-checked);
  - `checks/verify_origin.txt` (87 of 87 quotes found verbatim).
- **The first Phase A output is kept.** It is `checks/phase_a_run1.txt`. Two repairs were made after it (AGENT_LOG 162):
  - a reading whose words contradicted its own numbers;
  - a broken domain baseline.

  Neither changed a gate verdict.

## The short answer

| id | what CRR says | kind | result | label |
|---|---|---|---|---|
| CD-1 | H-L5 on cell size: the arc between divisions beats the clock | INHERITED (P1) | CV(arc) − CV(amplitude) = 0 exactly in the adder, sizer and timer worlds | control (i) can never be beaten: **HOLDS** as predicted; H-L5 is empty here |
| CD-2 | which size rule (adder, sizer, timer) | SILENT | no test | CRR does not choose |
| CD-3 | replication initiation sits at the A3 antipode of the division cycle | H-CUT, risky | the synthetic gate G-CD3 **OPENS** (positive control PASS, domain world FAIL, at all three growth rates) | a real-data test is possible; not yet pre-registered (below) |
| CD-4 | mother–daughter memory (A6/P3) | already made | not repeated | — |
| OL-1 | CRR's five ingredients against eleven origin-of-life theories | comparison | 0 of 5 ingredients discriminate (1 of 5 under the agent's proposed readings) | CRR restates what the theories share |
| OL-2 | A6 memory moves Eigen's error threshold | SYNTHESIS | μ_c 0.045007 at q = 0, 0.5 and 0.9; Eigen's 0.045007 | **REDUNDANT-IG** |
| OL-3 | a protocell's first internal event sits at the antipode | PROPOSES | on a bare size sawtooth the division is the extremum (199/199) | untestable until CD-3 is tested |
| DS-1 | the cut on a nanopore squiggle | reading (O3) | no rotor, so A3 does not apply | — |
| DS-2 | arc-threshold segmentation beats the domain's detector | gate | the gate G-DS2 **CLOSES** at all three levels | no real-data study (R12) |
| DS-3 | the A1′ step predicts where segmentation fails | reading | misses below one step are 2.05, 2.55 and 3.16 times those above | **HOLDS**; it is the t-test's own power function (REDUNDANT-DOMAIN) |
| DS-4 | mutations per generation vary less across species than per year | retrodiction | 40-fold against more than 120-fold, not on one footing | **SILENT** by the declared rule |
| DS-5 | sequencing by synthesis | SILENT | one base per imposed cycle | nothing to test |

**In plain words.**
- **Mostly not new.** Across three fields, CRR mostly says what each field already says, in different words:
  - The regularity of bacterial size is the adder.
  - Memory in replication does not move Eigen's error threshold.
  - Origin-of-life theories that share cycles and heredity are not told apart by CRR.
  - A nanopore squiggle has no cycle to cut.
- **One claim that can fail.** CRR says replication starts half a turn after division, measured on the cell's own
  growth–division phase. In a synthetic check this claim is **separable** from the domain's rule. When it is false, the
  check says false; when it is true, the check says true. So it can be tested on real cells.
- **What the investigator expects.** It will fail on real cells, because the domain's initiation adder predicts initiation
  to within 0.0312–0.0631 of a cycle in its own world. That expectation is not a result.

---

## Part 1. Cell division

### CD-1: "change has its own clock" on cell size is the adder

**What was run.** In three synthetic lineage worlds (adder, sizer, timer; 279 occasions each), H-L5's amplitude control
equals the arc to the last digit, as P1 says it must:
- **adder:** CV(arc) 0.095141, CV(amplitude) 0.095141, CV(clock) 0.227981;
- **sizer:** 0.212194 each, against a clock of 0.278827;
- **timer:** 1.077200 each, against a clock of 0.094674.

**Which class each world falls in.**
- The adder and sizer worlds are arc-regular (clock minus arc CIs [−0.1559, −0.1090] and [−0.0925, −0.0425]).
- The timer world is clock-regular ([+0.9059, +1.0460]).
- So the instrument separates the classes.
- But on this carrier the "arc" is the added size, and H-L5's claim beyond its control is empty. This agrees with synthesis
  batch 13, row 1 (REDUNDANT-IG).

### CD-3: H-CUT on DNA replication initiation

**The domain's picture** (quoted in `docs/citations/life_cell_2026-09-26.md`):
- Donachie 1968: "ROUNDS of DNA replication are initiated in Escherichia coli at different stages in the cell cycle of
  bacteria growing at different rates".
- Wang & Levin 2009: "rapidly growing cells initiate new rounds of chromosome replication before completing the previous
  round".

**CRR's prediction.** A3 says the cell's own event sits at the antipode. Initiation happens when the intrinsic
(analytic-signal) phase of the log-volume trace has advanced by π from the last division.

**The baselines** (R7):
- a constant cycle fraction fitted on the training half;
- the initiation adder (Si et al. 2019; Witz et al. 2019), with its per-origin add fitted on the training half.

**The gate G-CD3** (`checks/phase_a.txt`). Ten synthetic lineages of 150 cycles per growth rate, C + D = 70 min, 3
growth rates.

| τ̄ (min) | W− (the domain's world) pass fraction | W+ (initiation at the antipode) pass fraction | label |
|---|---|---|---|
| 100 | 0.00 → FAIL | 0.90 → PASS | as required |
| 50 | 0.00 → FAIL | 1.00 → PASS | as required |
| 25 | 0.00 → FAIL | 1.00 → PASS | as required |

The standing `gate_CUT` reads OPEN. **G-CD3 OPEN.**

**Two features of the per-unit output matter for a real test.**
- **The domain rule is sharp in its own world.** Its per-unit median error lies between 0.0312 and 0.0631 of a cycle across
  the 30 W− units. The per-unit lines print it next to the antipode's error, after the repair recorded in AGENT_LOG 162.
- **The antipode is not far off at intermediate growth.** At τ̄ = 50 min the W− units initiate at median cycle fractions of
  0.564–0.623. There the antipode's errors (0.0809–0.1155) are far smaller than at 100 min (0.2127–0.2866) or 25 min
  (0.3599–0.4693).

A real test therefore turns on the initiation adder, not on the fitted fraction.

**What is needed to run it.** The only public data located on the day with per-frame lengths and measured initiation
times are Witz et al. 2019:
- 3-min frames;
- doubling times of 89, 53 and 41 min;
- CC-BY;
- MoMA outputs on Zenodo 10.5281/zenodo.3149097, 9.6 GB, and the authors' processed per-cell tables in their replication
  repository.

**Why no pre-registration was written today.** The processed tables are 2019 pandas pickles. Their schema is known from
the authors' code (`length` per frame, `born`, `mother_id`, `Ti`, `full_cellcycle`), but loading them cannot be checked
without opening them, and R2 forbids opening before the hash. A blind loader voided EQ2R and T1x, and a void would make the
one suitable data set SEEN.

**The next step (LIFE1).** It is fixed now, so nothing is chosen after the data:
- **Carrier:** each mother-machine lineage traced through `mother_id`, following the daughter with a complete cycle.
- **Phase:** the intrinsic phase of its log-length trace.
- **Events:** initiations at `born + Ti`.
- **Scoring:** the three rules exactly as in `phase_a.py`, and the step includes the 3-min frame.
- **Verdict:** PASS at ≥ 80 % of lineages, FAIL below 60 %.
- **VOID rule:** the scorer is VOID if the loader raises, which is written into the pre-registration.
- **Timing:** hashed and OTS-anchored before any byte of the tables is read, with the data step on or after 2026-09-27
  (R3).
- **Forecast:** FAIL, against the initiation adder.

### CD-2, CD-4

- **CD-2** is SILENT: CRR does not choose among adder, sizer and timer.
- **CD-4** (the A6/P3 mother–daughter lag term) is `synthesis.py` row 8 and is not repeated.

---

## Part 2. The origin of life

### OL-1: eleven theories against CRR's five ingredients

**What was graded.**
- **The sources.** 71 quotes from on-the-day sources for eleven theories: RNA world, metabolism-first, RAF autocatalytic
  sets, hypercycle and error threshold, chemoton, compartment-first, assembly theory, dissipative adaptation, the FEP
  applied to life, autopoiesis, and dynamic kinetic stability. Details are in `docs/citations/life_origin_2026-09-26.md`.
- **The readings.** Each theory gets one reading per ingredient.
- **The grading.** `checks/grade_origin.txt` computes it:

| ingredient | CONTAINS (REDUNDANT) | CONFLICTS | label |
|---|---|---|---|
| I1 A3 + O3: the first cut needs the first self-sustaining cycle | 7 (metabolism-first, RAF, hypercycle, chemoton, compartment-first, autopoiesis, DKS) | 0 | NON-DISCRIMINATING |
| I2 A6: heredity from the settled past at bounded strength | 5 (RNA world, hypercycle, chemoton, compartment-first, DKS) | 0 | NON-DISCRIMINATING |
| I3 H-L5: own events set the clock | 1 (assembly theory: "an 'assembly time' that ticks at each object being made") | 0 | NON-DISCRIMINATING |
| I4 arc against chord | 1 (assembly theory: "the shortest number of steps required to generate the object") | 0 | NON-DISCRIMINATING |
| I5 the empty cut; nothing fed by a future | 1 (assembly theory) | 0 | NON-DISCRIMINATING |

**The result.** **0 of 5** ingredients discriminate between the theories, as the declaration expected.

**What decides the 0.** The investigator changed three of the source agent's proposed readings to SILENT (listed in the
output with reasons). One of them decides the result: the agent read the FEP as CONFLICTING with I5, because the FEP's
internal states "encod[e] posterior beliefs" and anticipate events.
- The investigator reads that as a different claim:
  - content in internal states is not content at the cut;
  - prediction built from past data is not being fed by a future.
- Under the agent's readings, I5 **would discriminate**, 1 of 5.
- Both gradings are printed, and the reader can judge the one cell that decides it.

**One reading worth keeping, which is not a prediction.** Assembly theory's assembly index is a shortest path, which is
CRR's chord C* (D3), not its arc C (D2). No fetched theory states the surplus S = C − C* between the path a system took
and the shortest one that would have built it.

**What SILENT means here.** Several primary texts were paywalled and are quoted from reviews by the theory's own school
(dossier, "Checks and limits"). So SILENT means "silent in the fetched texts", not "silent in the theory".

### OL-2: memory does not move the error threshold

**The row.** The SYNTHESIS row regenerates templates from the settled past with geometric age weights (A6/P3).

**What it moves and what it doesn't.**
- It moves the master's growth factor per generation: 3.2045 at q = 0, 2.1022 at q = 0.5, 1.2204 at q = 0.9.
- It leaves the stationary master fraction unchanged at 0.2449, which is Eigen's (σQ − 1)/(σ − 1).
- It leaves the threshold unchanged: μ_c = 0.045007 at every q. The characteristic equation and the iterated dynamics
  agree, and both equal Eigen's 1 − σ^(−1/L).

**Outcome REDUNDANT-IG.** The threshold is where σQ crosses 1, whatever the weights. This is the renewal-equation fact
familiar from epidemiology: a delay kernel changes the rate, not the threshold.

**A wrong expectation.** The declared expectation that the stationary fraction would change was wrong. In a linear
renewal system the kernel cancels from the composition too.

### OL-3

- On a bare protocell size sawtooth, the division is the volume maximum in 199 of 199 cycles. H-CUT's own-event comparison
  is therefore empty there.
- CRR's protocell claim (a first internal event at the antipode) has CD-3 as its only testable analogue.

---

## Part 3. DNA sequencing

### DS-1

Strand translocation is not cyclic, so there is no rotor and no A3 cut (O3). What CRR offers for a squiggle is the scalar
arc-threshold rule. `CRR.md` §2 says this "is not the axiom".

### DS-2: the gate closes

**The domain's detector.** Scrappie, the domain's reference detector, computes `tstat[i] = fabs(delta_mean) /
sqrt(combined_var / w_lengthf)` over two window pairs, with defaults `.window_length1 = 3, .window_length2 = 6`
(`docs/citations/life_sequencing_2026-09-26.md`).

**What the gate compared.** A tuned single-window t-test (T) as the stand-in, the arc-threshold rules on raw and smoothed
samples, and a clock. All were tuned on 200 training reads and scored on 200 test reads per level.

| level spread | A-raw | A-smooth | T | CL (clock) | better arc vs T (step) |
|---|---|---|---|---|---|
| 1 σ | 0.5866 | 0.6122 | 0.5997 | 0.6324 | +0.0125 (0.0200): not ahead |
| 2 σ | 0.6114 | 0.6330 | 0.6694 | 0.6317 | −0.0363 (0.0200): not ahead |
| 4 σ | 0.6538 | 0.6662 | 0.7507 | 0.6323 | −0.0844 (0.0200): not ahead |

**G-DS2 CLOSED.** No real-data study follows (R12).

**Three things to note.**
- **The clock led at the smallest spread.** A clock tuned to the mean dwell was the best detector at 1 σ, ahead of every
  rule that reads the signal.
- **A-raw did not reduce to a clock.** It was within a step of the clock at none of the three levels (behind at 1 and 2 σ,
  ahead at 4 σ).
- **T is a weaker stand-in than the tools.**
  - Tombo segments DNA by a running window difference, not a t-test.
  - Scrappie uses two t-test detectors.
  - Squigulator's dwell is a rounded normal (mean 9, sd 4 samples).

  The arc rule was not ahead of even this weaker stand-in, so the gate was not rerun.

### DS-3: the A1′ step, and misses

**What was measured.** The t-test detector's miss rate on boundaries below one A1′ step, |Δμ|√n/σ < 1, against boundaries
at or above it.

| level spread | miss rate below one step | at or above | ratio |
|---|---|---|---|
| 1 σ | 0.4529 | 0.2206 | 2.05 |
| 2 σ | 0.6953 | 0.2730 | 2.55 |
| 4 σ | 0.7977 | 0.2527 | 3.16 |

**The result.** The prediction **HOLDS** at every level. It is still the t-test's own power function stated in CRR's unit,
so it is REDUNDANT-DOMAIN. The domain states the error modes itself; homopolymers and similar k-mer levels are quoted in
the dossier.

### DS-4, DS-5

**DS-4.** Bergeron et al. 2023 give two spreads:
- **per generation:** "varies by a factor of 40 across all species" (pedigree rates, 68 species);
- **per year:** "varies more than 120-fold among species" (modelled; the species count is not stated).

These are not on one footing, so DS-4 is **SILENT** by the declared rule.

- **Report only, not a grade.** Under an accepted footing, the per-generation spread would be the narrower.
- **Where a real test could run.** The matched pair is in their Supplementary Table 9. A test on it would be a
  pre-registration with a later-day data step.
- **CRR's own limit.** CRR does not say which process is the "own event" (generations, germline divisions, or damage
  accumulating in time). The human parental-age evidence (Kong et al. 2012; Jónsson et al. 2017; Gao et al. 2019) points
  to clock-time damage as a real contributor.

**DS-5.** Illumina chemistry adds one base per imposed cycle, so the own event and the clock coincide by design.

---

## What a surrogate would have done

**G-CD3.** Its surrogate pair is built to separate the two outcomes:
- W+ is a world where CRR is true by construction; it reads PASS.
- W− is the domain's world; it reads FAIL.
- The standing `gate_CUT` checks the instrument on sine, van der Pol and asymmetric harmonics.

A real-data PASS would therefore have to come from the cells, not from the arithmetic of the phase.

**G-DS2.** Its clock detector is the surrogate. The arc rule was not ahead of it by a step at any level. So no real
squiggle is needed to see that the rule has nothing to win.

## Sources

Each source was fetched on 2026-09-26, with its version and URL, in:
- `docs/citations/life_cell_2026-09-26.md` (68 quotes verified by the agent);
- `docs/citations/life_origin_2026-09-26.md` (71 quotes);
- `docs/citations/life_sequencing_2026-09-26.md` (81 blockquotes).

The claims graded here are re-verified in `checks/verify_origin.txt`.
