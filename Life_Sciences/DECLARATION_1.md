# Declaration 1: CRR's predictions for cell division, the origin of life and DNA sequencing

**Status.**
- **The request.** Owner request: prompt-log entry 217. Written on 2026-09-26.
- **When it was pushed.** Before any source dossier (`docs/citations/life_*_2026-09-26.md`) exists. Also before any
  Phase A script is written, and before any data set is located or opened.
- **What it is.** A declaration of predictions, gates and grading rules, in the pipeline's order:
  1. predictions, pushed first;
  2. sources, fetched on the day;
  3. a Phase A synthetic gate that can close;
  4. a pre-registration hashed and anchored with OpenTimestamps, only if a gate opens;
  5. a data step on a later calendar day (R3), no earlier than 2026-09-27;
  6. rows scored as committed.

  Everything before step 4 is a note, not evidence (R8).
- **How labels are computed.** Every label is computed by a committed script from its numbers (R15). The investigator's
  expectation is written beside each prediction so that a surprise is visible.

**Honesty clause.**
- **The predictions cannot be blind.** The investigator's training exposure includes the textbook results in all three
  fields. Examples: the adder, the Cooper–Helmstetter model, Eigen's error threshold, nanopore segmentation.
- **What the declaration can fix.** It fixes:
  - the CRR reading, named by axiom;
  - the direction CRR implies;
  - the rule that grades it;
  - the gate conditions.
- **What is already on the record** in this area:
  - **Synthesis batch 13, row 1 (the adder).** On a monotone volume carrier the arc equals the added volume (P1).
    CV(arc) 0.0749 against CV(clock) 0.3319. OUTCOME REDUNDANT-IG, and the domain's adder agrees.
  - **Batch 13, row 2 (ion-channel gating with A6).** WRONG.
  - **Batch 12, row 4 (Wright–Fisher with A6 memory).** The domain's seed-bank theorem.
  - **`theory/retrodictions/synthesis.py`, row 8.** Already made the A6/P3 lag-2 mother–daughter proposition. It is not
    repeated.
  - **Ledger rows MEAS2-*.** H-L5 FAILs on measles, 0/17 cities: the clock-regular class.

  This declaration does not re-grade any of them.

## The CRR ingredients used

The ingredients are those of `theory/CRR.md` v3.1:
- **A1′ and D1**, the resolvable step and the resolution ρ.
- **D2 and D3**, arc and chord.
- **P1**, arc equals chord if and only if the traversal is monotone.
- **A3**, the antipodal cut on an intrinsic phase. It needs a rotor.
- **O3**, the cut without a rotor. Nothing sets L.
- **H-CUT**, own events against the antipode against the extremum.
- **A6 and P3**, regeneration from the settled past with geometric age weights q^k. q is not fixed by CRR.
- **H-L5**, arc against clock between own events.
- **Proposition 7**, the empty cut.

The Fisher–Rao metric, arc, chord and surplus belong to information geometry, not to CRR.

---

## Part 1. Cell division and biological systems

### CD-1: H-L5 on the cell-size carrier

- **Kind.** INHERITED (P1).
- **CRR reading.** Division is the cell's own event. H-L5 says the arc accumulated between divisions is more regular than the
  interdivision time.
- **Prediction.** H-L5 cannot pass here as a CRR claim.
  - On a monotone growth trace the arc between divisions equals the added size. So cv_arc − cv_amp = 0 identically, and
    H-L5's control (i), the amplitude of the excursion, can never be beaten.
  - "Change has its own clock" on this carrier is the adder, which is the domain's result.
- **Graded by.** `Life_Sciences/checks/phase_a.py`, on three synthetic lineage worlds (adder, sizer, timer). The prediction
  holds if the amplitude-control difference is exactly 0 (to round-off) in all three worlds. It fails otherwise.
- **Investigator's expectation.** Holds (this is P1).

### CD-2: which size rule, adder, sizer or timer

- **Kind.** SILENT.
- **Reading.** CRR does not choose among them. The choice of carrier and unit decides which quantity is "regular", and CRR
  fixes neither for a cell.
- **What this means.** No test. It is recorded so that the adder is never quoted as a CRR prediction.

### CD-3: H-CUT on DNA replication initiation (the risky prediction)

**CRR reading.**
- The growth–division cycle of a bacterial lineage is a rotor. Its intrinsic phase is the analytic-signal phase of the
  detrended log-volume trace (`intrinsic_phase`, the one implemented phase).
- Replication initiation is an own event of the cell. It is distinct from the volume extremum, which is the division
  itself.
- H-CUT says own events align with the antipode.

**Prediction (CRR).**
- Initiation occurs at the A3 antipode of the last division: the first time after a division t_d at which
  φ(t) − φ(t_d) = π.
- It sits there more closely than two alternatives, each fitted on the first half of the unit's occasions and scored on the
  second half:
  1. **The strongest simple alternative:** a constant cycle fraction f̂, with initiation at t_d + f̂·τ.
  2. **The domain's rule:** the initiation adder. A constant volume per origin, Δ̂_i, is added between consecutive
     initiations (Si et al. 2019; Witz et al. 2019).
- The H-CUT extremum baseline is degenerate on this carrier. The volume extremum is the division, so initiation cannot align
  with it. The two alternatives replace it (R7).

**Per-unit score.**
- **The error.** For each rule, the error is e = |t_init − t_rule| / τ, where τ is the cycle's interdivision time. A unit's
  error for a rule is the median e over its scored occasions.
- **When a unit passes.** Its CRR error is below the smaller of the two baselines' errors by at least a step.
- **The step.** max(the imaging frame interval / the unit's median τ, twice the bootstrap SE of the paired difference). On
  synthetic data the "frame" is the grid step.
- **The verdict.** PASS if at least 80 % of units pass. FAIL if fewer than 60 % pass. Otherwise NOT DECIDED.

**The Phase A gate G-CD3.** It runs on synthetic lineages only.

- **The domain world W−.** The initiation adder with Cooper–Helmstetter division.
  - Per-origin volume u grows at the cycle's rate λ. It halves at initiation. The next initiation fires when u has added
    Δ_i(1 + 0.1ξ).
  - Division follows each initiation after (C+D)(1 + 0.1ξ), with C+D = 70 min.
  - The volume halves at division. λ is redrawn at each division as (ln 2/τ̄)(1 + 0.1ξ).
  - Three conditions: τ̄ ∈ {100, 50, 25} min, spanning non-overlapping to overlapping replication cycles.
  - Grid step 0.5 min. 10 lineages of 150 division cycles per condition. The first 20 cycles are dropped as burn-in.
- **The positive world W+.** The same volume traces as W−, with each initiation moved to the antipode of the preceding
  division plus Gaussian jitter of 0.05 τ.
- **Conditions for the gate to open.**
  - The standing `runs/phaseA/gate_CUT.txt` reads OPEN (the instrument check).
  - At all three conditions, W+ reads PASS: at least 80 % of units pass.
  - At all three conditions, W− reads FAIL: fewer than 60 % of units pass.
- **Conditions for the gate to close.** Anything else closes it. In particular:
  - If the antipode and the fitted constant fraction agree within a step on W+, the label is **REDUCES (to a fixed cycle
    fraction)**. The gate closes, because on this carrier A3 cannot be separated from the simplest alternative.
- **If the gate closes.** No pre-registration is written and no data are opened (R12).
- **If the gate opens.** A pre-registration LIFE1 is written for real mother-machine lineages with measured initiation
  times, from a source to be verified on the day. It is hashed and OTS-anchored, and its data step falls on or after
  2026-09-27.

**Investigator's expectation.**
- In the textbook model, the initiation cycle fraction moves with growth rate (Cooper–Helmstetter), while the antipode is a
  fixed phase.
- So on real data the fitted constant fraction and the initiation adder should beat the antipode. Expected: **FAIL**, if the
  gate opens.
- Whether the gate opens at all is uncertain. The Hilbert phase of a noisy exponential sawtooth may be nearly linear in
  time. In that case the antipode reduces to a fixed fraction and the gate closes.

### CD-4: mother–daughter memory (A6/P3)

- **Kind.** Already made (`synthesis.py`, row 8).
- **What this means.** Not repeated. No test.

### BS-1: other biological rotors

- **Candidates.** The segmentation clock and somite boundaries, the circadian clock, and cardiac cycles are candidates for
  H-CUT and H-L5.
- **Arterial pressure is already designed.** H-L5 on arterial pressure has a design in `CLAUDE.md` §4 (L5x, Autonomic Aging
  records 0061–0120). It has not been run.
- **What this declaration does.** It names these candidates and does not declare them. Each needs its own declaration and
  gate. Declaring them here would widen the request past what can be gated today.

---

## Part 2. Origin of life

### OL-1: a comparison of existing theories against CRR's ingredients

- **Kind.** A comparison, graded from quotes.
- **The theories.** At least these, with sources fetched on the day:
  - RNA world;
  - metabolism-first (iron–sulfur world, the reverse citric acid cycle);
  - autocatalytic sets (RAF: Kauffman; Hordijk and Steel);
  - the hypercycle (Eigen and Schuster);
  - the chemoton (Gánti);
  - compartment-first or lipid world;
  - assembly theory (Cronin, Walker);
  - dissipative adaptation (England);
  - the free-energy principle applied to life (Friston 2013);
  - autopoiesis (Maturana and Varela);
  - dynamic kinetic stability (Pross).
- **The ingredients.**
  - **I1 (A3 with O3).** A cut needs a rotor, so the first cut needs the first self-sustaining cycle.
  - **I2 (A6).** The next occasion is seeded from the settled past at bounded strength (heredity without accumulation).
  - **I3 (H-L5).** The system's own events set its clock.
  - **I4 (D2 against D3, surplus S = C − C*).** The travelled path against the shortest path.
  - **I5 (Proposition 7 / A8).** The cut has no content, and nothing is fed by a future.
- **The cells.** For each theory T and ingredient I, the claims file records one of:
  - **CONTAINS:** T already states I; a verbatim quote is required.
  - **CONFLICTS:** T states something incompatible with I; a verbatim quote is required.
  - **SILENT:** neither.
- **The label per cell.**
  - REDUNDANT if CONTAINS;
  - CONFLICTS if CONFLICTS;
  - SILENT otherwise.
- **The label per ingredient.** DISCRIMINATES if at least one theory CONTAINS it and at least one CONFLICTS. Otherwise it
  is NON-DISCRIMINATING. Computed by `Life_Sciences/checks/grade_origin.py`.
- **Investigator's expectation.** Every ingredient is NON-DISCRIMINATING.
  - I1 and I2 are CONTAINED by every theory that posits a cycle and heredity, which is most of them.
  - I4 maps onto assembly theory's minimal construction path, which is a chord (D3), not an arc. That is a reading, not a
    prediction.
  - So CRR does not choose between origin-of-life theories. It restates what they share.

### OL-2: A6 memory and Eigen's error threshold

- **Kind.** A SYNTHESIS row, graded by the harness.
- **Q.** Regenerating templates from the settled past with A6/P3 geometric age weights moves Eigen's error threshold μ_c.
  In this reading, offspring are copied from templates of age k with weight (1 − q)q^k.
- **The world.**
  - Single-peak landscape: master fitness σ = 10, mutants 1, length L = 50, no back mutation.
  - Q_copy = (1 − μ)^L.
  - q ∈ {0 (the null, Eigen's discrete generations), 0.5, 0.9}.
- **How μ_c is found.**
  1. By iterating the population dynamics (the numerical check).
  2. From the characteristic equation Σ_k w_k σ Q_copy / λ^{k+1} = 1 against the mutant class's λ = 1.
- **The tests.**
  - **T-G:** μ_c at q = 0.9 against q = 0.
  - **T-N:** Eigen's μ_c = 1 − σ^{−1/L} (the renewal or Euler–Lotka argument: a positive delay kernel moves the growth rate,
    not the sign of λ − 1).
  - **T-C:** the numerical threshold.
- **Investigator's expectation.** The threshold does not move. **REDUNDANT-IG** on the threshold. The stationary master
  fraction and the approach rate do change; they are printed as secondary numbers.

### OL-3: the protocell division cut

- **Kind.** PROPOSES.
- **CRR reading.** A protocell's growth–division cycle is a rotor. A3 then places its first internal own event (template
  copying) at the antipode of division.
- **What this means.** The prediction is structurally the same as CD-3 on an unevolved system. It has no data and no
  test here.
- **Two consequences for grading.**
  - If CD-3's gate closes or CD-3 fails, OL-3 loses its only testable analogue. It is then recorded as untestable.
  - On a bare protocell size sawtooth, the division is the extremum, so H-CUT's own-event comparison is empty. Phase A
    prints the fraction of divisions within one grid step of a volume extremum, expected 1.0.

---

## Part 3. DNA sequencing

### DS-1: nanopore translocation and the cut

- **Kind.** A reading (O3).
- **The reading.** Strand translocation through a pore is not cyclic. There is no rotor, so A3 does not apply and the cut
  is undefined. The base steps form a point process, and natural time gives its unit (one base) but not the cut.
- **What this means.** Any "CRR segmentation" of a squiggle uses the scalar condition "cut when the arc since the last cut
  reaches θ". `CRR.md` §2 says this coincides with A3 only on monotone traversals, and "It is not the axiom". So DS-2 tests
  a CRR-inspired rule, not A3.

### DS-2: arc-threshold segmentation against the domain's detector

- **Kind.** A gate that can close.
- **The synthetic squiggles.**
  - Current levels μ_j ~ N(0, s²) per base step, with s ∈ {1, 2, 4} in noise units (σ = 1).
  - Dwell per base: Gamma(shape 2, mean 9 samples), rounded, minimum 2.
  - With probability 0.05 a step repeats its level (a homopolymer-like, undetectable boundary; kept in the truth set).
  - 200 training reads and 200 test reads of 400 bases per level. Fixed seeds.
- **The detectors.** Each threshold (and window) is tuned on the training reads to the best F1 over a declared grid.
  - **A-raw (CRR):** arc = Σ|x_{t+1} − x_t| / σ̂ on the raw samples, with σ̂ the MAD of first differences divided by √2.
    Cut when the arc since the last cut reaches θ.
  - **A-smooth (CRR):** the same on a moving average of window w ∈ {3, 5, 7}.
  - **T (the domain's):** a two-window t-statistic with window w ∈ {3, 5, 7}. Local maxima above a threshold, with a
    minimum spacing of 2 samples. This is the segmentation used by Scrappie and Tombo-style tools; the sources are to be
    verified on the day.
  - **CL (a clock):** cut every k samples.
- **Score.** Boundary F1 on the test reads, with a tolerance of ±2 samples and greedy one-to-one matching.
- **Conditions for the gate G-DS2 to open.** Both must hold at all three levels:
  - the better arc detector's F1 ≥ T's F1 + a step;
  - it also beats CL by a step.
  - The step is max(0.02, twice the paired bootstrap SE over reads).
- **Also printed.** Whether A-raw is within a step of CL. If so, the label is **REDUCES (to a clock)**: under noise alone,
  E|Δx|/σ = 2/√π per sample, so a raw arc advances like a clock.
- **If the gate closes.** No real-data study (R12). Real squiggles have no ground-truth boundaries except model-based
  resquiggling, which would make the test circular.
- **Investigator's expectation.** **CLOSED.** A-raw reduces to a clock, and A-smooth is at or below T.

### DS-3: the A1′ unit and where segmentation fails

- **Kind.** A reading computed on DS-2's squiggles; expected to be the domain's own statistics.
- **The reading.** A1′ says a transition is resolvable in one dwell of n samples only if |Δμ|·√n / σ ≥ 1 (one Cramér–Rao
  step, as in `theory/checks/cramer_rao_reading.py`).
- **Prediction.** The domain detector T misses boundaries below one step at least twice as often as boundaries above it.
- **Graded by.** `phase_a.py`, which prints the miss rates by bin:
  - HOLDS if the ratio is ≥ 2;
  - FAILS otherwise.
- **Investigator's expectation.** Holds. The label is still REDUNDANT-DOMAIN: detection power as a function of
  |Δμ|√n/σ is the t-test's own power function.

### DS-4: mutation accumulation, generations against years

- **Kind.** A retrodiction, graded from quoted numbers.
- **The reading, with an added assumption.** CRR does not say which physical process counts as the own event. Taking the
  generation (germline transmission) as the own event, H-L5's "change has its own clock" reads: across species, the
  germline mutation rate per generation varies less than the rate per year.
- **Graded by.** `Life_Sciences/checks/grade_origin.py`, from quoted fold-ranges or spreads in the fetched sources
  (preferably a cross-species pedigree study such as Bergeron et al. 2023; the version is to be verified).
  - **AGREES:** per-generation spread < per-year spread.
  - **DISAGREES:** per-generation spread > per-year spread.
  - **SILENT:** the sources do not state both on one footing.
- **Investigator's expectation.** Uncertain. The investigator does not recall the direction reliably. A replication-driven
  view favours AGREES; the paternal-age and damage-driven evidence cuts the other way.

### DS-5: sequencing by synthesis (Illumina)

- **Kind.** SILENT.
- **The reading.** Each chemistry cycle is imposed on the clock, and one cycle is one base. The own event and the clock
  coincide by design, so H-L5 has nothing to test.
- **What this means.** No test.

---

## What is run, in order

1. **Sources.** Three dossiers are fetched on the day, with versions (R10):
   - `docs/citations/life_cell_2026-09-26.md`;
   - `docs/citations/life_origin_2026-09-26.md`;
   - `docs/citations/life_sequencing_2026-09-26.md`.

   Data sets are located, and their links and licences recorded, but no data file is opened.
2. **Phase A.** `Life_Sciences/checks/phase_a.py`, pinned to `phase_a.txt`. It covers CD-1, G-CD3 (with the OL-3
   extremum print), OL-2 through the synthesis harness, G-DS2 and DS-3. It is deterministic, and a rerun must be
   byte-identical.
3. **Grading.** `Life_Sciences/checks/claims_origin.py` records quotes and readings, and `grade_origin.py` (pinned to its
   `.txt`) labels OL-1 and DS-4.
4. **Pre-registration.** Only if G-CD3 or G-DS2 opens: a pre-registration in `prereg/life1/`, hashed, OTS-anchored and
   tagged, with the data step on or after 2026-09-27.
5. **Write-up.** `Life_Sciences/LIFE_SCIENCES.md` quotes the pinned outputs and nothing else.

## Amendment policy

- **What an amendment may do.** Anything changed after this push is an amendment, appended here and pushed before the
  script it affects runs.
- **What it may not do.** No gate condition, threshold or world parameter above may be changed after its script has run.
  A changed gate is a new declaration.
