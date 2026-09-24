# Note: ten pre-registered predictions in the classes where CRR works (synthesis batches 31–32), 2026-09-24

**Status of this note**
- **Scope.** Owner request (prompt-log entry 131). A note to the auditor, not evidence (R8).
- **The rows.** The declarations are in `theory/retrodictions/synthesis_batches/DECLARATION_31_32.md`. Its sha256 begins
  86cfb0eb. It was stamped with OpenTimestamps on four calendars and pushed in commit 1232815, before `batch_31.py` or
  `batch_32.py` existed, and no prototype was run.
- **The outputs** are pinned in `batch_31.txt` and `batch_32.txt`, and both rerun byte-identical. The first-run outputs
  are kept in the scratchpad. The only changes after the first run are in AGENT_LOG 109: two computed text lines and one
  post-hoc diagnostic. No parameter, criterion or outcome changed.

## What "a pre-registered prediction in a working class" can mean on the ladder

**The classes.** The map of prompt-log entry 129 sorted CRR's retrodictions by kind of system. CRR's commitments landed
where the domain is known to be in four classes:
- MEMORY, bounded fading memory: 16/23;
- CYCLE, the cut on a rotor phase: 7/8;
- EVENT, own-event trains: 11/13;
- EQ-IG, static information geometry: 18/19.

**What the ladder allows** (`Epistemic_Review/checks/ladder.py`).
- **The rung of every row here.** Each prediction here is declared before a run on a model world built by the same
  author, so it sits at **R4**. Its synthesis outcome places it further.
- **REDUNDANT-DOMAIN is R2.** It means "a CRR-proper ingredient changed the number and landed on the domain's known
  result; it adds nothing the domain lacked". In a working class that is the expected outcome and an honest one.
- **ADDS is R3,** a candidate until a named expert answers the class note's three questions.
- **The limit.** None of these rows can be a ledger PASS. PASS-0 (R6) and above need a hashed prediction scored on real
  data that has never been opened.
- **The bridge.** The ladder's bridge from here to there is the **PROSPECTIVE CANDIDATE** label
  (`docs/notes/2026-09-18_sharp_regime_review.md` §3.2). It needs a comparative claim with a baseline that can win, an
  open gate, a named unseen real carrier, a threshold fixed before the data, and a fixed reading convention.

**The design rule** (stated in the declaration before any run): in a working class a row can only add something if its
proposition is not already the domain's theorem. So every proposition was built so that the domain's standard model
(the null) and the CRR variant give different numbers.

## The ten rows

| row | system (class) | CRR ingredient | outcome | rung | the number |
|---|---|---|---|---|---|
| 31-1 | Ricker stock–recruitment with remembered density (MEMORY) | A6 + P3 | ADDS | R3 candidate | first instability moves from r = 2.000 to 6.000 (a flip); Beverton–Holt surrogate stable, as required |
| 31-2 | SIR with distancing on remembered prevalence (MEMORY) | A6 + P3 | ADDS | R3 candidate | peak prevalence 0.041501 against 0.031357 (ratio 1.3235); the k = 0 surrogate shows no effect, as required |
| 31-3 | optimal-velocity traffic with remembered headway (MEMORY) | A6 + P3 | ADDS | R3 candidate | string-stability threshold V'_c 0.3335 against Bando's 0.5005 (scan) |
| 31-4 | Samuelson multiplier–accelerator with permanent income (MEMORY) | A6 + P3 | ADDS | R3 candidate | critical accelerator 2.500 against 1.250; a closed form, 1/((1 − q)c) |
| 31-5 | continuous logistic with remembered density (MEMORY) | A6 + P3 | REDUNDANT-DOMAIN | R2 | never destabilised; the weak-kernel theorem (MacDonald 1978) says so. Hutchinson's delay destabilises at 1.5800 (π/2 on the grid) |
| 32-1 | Brusselator under a slow drift of B (EVENT/CYCLE) | H-L5 on the Poisson carrier | **WRONG** | retrodictive fail | clock-regular: CV(period) 0.0424 against CV(Fisher arc) 0.1261, over 627 cycles |
| 32-2 | FitzHugh–Nagumo recovery event (CYCLE) | A3 via H-CUT | ADDS by the harness; **forced** | not a candidate in substance | nearer the antipodal cut on 1.0000 of 502 events; the post-hoc surrogate with no dynamics reaches 0.6667, the declared threshold |
| 32-3 | Lotka–Volterra with predators on remembered prey (MEMORY on a rotor) | A6 + P3 | ADDS | R3 candidate | the centre becomes an unstable spiral, leading eigenvalue +0.14858 ± 0.60281i |
| 32-4 | seasonally forced SIR (EVENT) | H-L5 | REDUNDANT-IG (degenerate) | R1 | the declared tuple is locked to the year (every interval 1.000); nothing varies, so H-L5 has nothing to test |
| 32-5 | event counting between two Poisson rates (EQ-IG) | A1′ | REDUNDANT-DOMAIN | R2 | 10.0000 resolvable steps; Anscombe's square-root transform gives 10.0037; the Gaussian unit gives 12.5000 |

**Tally:** 6 ADDS (one forced), 2 REDUNDANT-DOMAIN, 1 REDUNDANT-IG, 1 WRONG. On the whole ladder the retrodictive hit
rate is now 69 of 97 = 0.7113 (Wilson 95 % interval 0.6145 to 0.7921).

## What the ten rows say, read plainly

1. **The candidates are one mechanism, not five discoveries.** The five substantive ADDS all come from the MEMORY class
   (31-1 to 31-4, 32-3). All of them insert A6, a bounded exponential memory of the settled past, into a classic
   threshold model. What moves the threshold is the model's type:
   - in discrete maps with a period-2 instability (Ricker, and cardiac alternans before it) memory damps the alternation
     and pushes the flip out;
   - in continuous feedback loops (traffic, predator–prey, behavioural epidemics) memory is a distributed delay and
     destabilises or overshoots;
   - in the continuous logistic equation it is the weak kernel, and the domain already proved it harmless (31-5).

   These are applications of one lemma family. Each domain has a literature on memory or delay kernels: fisheries
   harvest rules on averaged indices, reaction delays in car-following, adaptive expectations in macroeconomics,
   information-dependent contact rates in epidemiology, delayed Lotka–Volterra. None of it was fetched here. **The
   decisive next step is a literature check per row. Several will probably turn out REDUNDANT-DOMAIN once the domain's
   memory-kernel papers are cited.** Until then each stays a candidate, and their count must not be read as five
   independent confirmations.
2. **The EVENT class failed its one real test (32-1).** H-L5's arc-regular claim, on a two-dimensional chemical
   oscillator with a proper (Poisson) Fisher carrier, where the arc is not simply the amplitude, came out clock-regular.
   This agrees with the ledger's measles result (MEAS2) and with the earlier finding that H-L5 wins mainly on monotone
   one-dimensional carriers, where it is its own amplitude control (REDUNDANT-IG).
3. **The CYCLE row taught an instrument lesson (32-2).**
   - **Why the result is forced.** The analytic signal writes x = A·cos φ exactly, so the zero crossings of a signal sit
     half a turn apart on its own Hilbert phase. An event defined as a zero crossing lands on the antipodal cut by the
     estimator's arithmetic. The declared surrogate (van der Pol, "nothing to test") could not show this.
   - **What caught it.** A post-hoc surrogate with no dynamics reached the declared 2/3.
   - **The consequence.** Under R4 this operationalisation of H-CUT is deleted. A future H-CUT row must define events
     independently of the phase estimator: a Poincaré-section phase, or an event variable other than the phased signal.
     That is itself a declaration to write before any further H-CUT row.
4. **The EQ-IG row (32-5) and the logistic row (31-5)** are what "redundant in paradigm" looks like. CRR's own unit gives
   the variance-stabilised distance statisticians already use, and CRR's regeneration is the stabilising distributed
   delay ecologists already proved. They add nothing. They do confirm that the ingredients land where the paradigm says
   they should.
5. **The seasonal SIR row (32-4)** did not test anything. The declared parameters locked the epidemic to the calendar
   year. A biennial measles-like row needs a new declaration with a tuple checked to be biennial. Checking the tuple
   first, on the model alone, is a design step, not a result, and it would have to be stated.

## Which rows could become real-data pre-registrations

**None earns PROSPECTIVE CANDIDATE yet.** Each would need a gate: a synthetic positive and negative control for the
comparative claim on the real carrier.

| row | unseen real carrier (to check against `data/SEEN.md`) | comparative claim and the baseline that can win | what is missing |
|---|---|---|---|
| 31-3 traffic | NGSIM vehicle trajectories (US-101, I-80) | drivers' acceleration is predicted better by an exponentially remembered headway (A6) than by the instantaneous headway, or by a pure reaction delay (the domain's standard), per driver, out of sample | a gate with synthetic drivers with and without memory; the kernel family fixed in advance. **The closest to a candidate** |
| 31-2 epidemics | mobility or contact indices beside case counts for regions not yet opened | the contact index tracks remembered prevalence (A6) better than current prevalence, or a pure lag | the domain literature check first; a gate; confounding by policy |
| 31-1 fisheries | a stock–recruitment database (RAM Legacy) | recruitment residuals are better predicted by remembered spawner abundance than by current abundance, per stock | a gate; the data licence and version recorded under R10/R11 |
| 32-3 predator–prey | long predator–prey series not opened before | the predator's response lags prey by a distributed rather than a discrete kernel | series length; a gate |
| 31-4 macroeconomics | none proposed | the closed form makes the row an exercise, not a test | — |

**The recommended next step.** Commission the literature check for rows 31-1 to 31-4 and 32-3; the dossier method used
for prompt-log entry 130 would do. Then write one real-data pre-registration, for 31-3 on NGSIM, with its gate. Under R3
the data step would fall on a later day than the rule's definition.
