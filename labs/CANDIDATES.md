# First shortlist of labs (investigator's judgement, 2026-09-26)

**What this is.**
- **The source.** Drawn from `checks/bank.txt`, the Life Sciences record (`Life_Sciences/LIFE_SCIENCES.md`) and the
  standing study designs in `CLAUDE.md` §4.
- **Every entry is judgement.** The entry rule is applied by reading, not computed. The data class is provisional until the
  sources are checked on the day of each lab's declaration.
- **Numbers.** Every number is quoted from a pinned output, named beside it.
- **This is a note, not evidence** (R8).

## Ready: the entry rule is met, a gate exists or is designed, and the data are public

| lab | rows | H1 (CRR) | H0 (domain) | gate | data | forecast |
|---|---|---|---|---|---|---|
| **L01 replication initiation at the antipode** | Life_Sciences CD-3 | initiation where the growth–division phase has advanced by π since division (H-CUT, A3) | the initiation adder, and a fitted constant cycle fraction | G-CD3 **OPEN** (`Life_Sciences/checks/phase_a.txt`) | **D2**: Witz et al. 2019 per-cell tables with per-frame lengths (2019 pandas pickles; loader risk; VOID rule required) | FAIL: the domain rule's own-world error is 0.0312–0.0631 of a cycle |
| **L02 the grandmother term** | `synthesis` row 8 (PROPOSES) | birth size carries a positive lag-2 partial autocorrelation with geometric (A6/P3) weights | the plain adder, AR(1) with coefficient 1/2 and lag-2 zero; any AR(2) | to design: the row's weakness says any AR(2) gives a lag-2 term, so the gate must score the **sign and geometric shape**, not a non-zero lag-2 | **D2**: the same lineages as L01 | uncertain |
| **L03 H-L5 in the arterial pulse (L5x)** | `CLAUDE.md` §4; measles FAIL (ledger MEAS2-*) as the other class | arc from the dicrotic notch to the next onset is more regular than clock time | clock CV, amplitude CV, identity-metric arc, peak-cut arc | the standing `gate_L5` (OPEN, `runs/phaseA/gate_L5.txt`); a study gate still to write | **D1**: PhysioNet Autonomic Aging 1.0.0, records 0061–0120 (unseen per `data/SEEN.md`) | uncertain |

**Why L01 and L02 go together.** They share data, and R3 allows one pre-registration per dataset. So they must be declared
and hashed **together**, in one pre-registration.

## Needs a sharper H1 before a lab can open

- **L04: which clock does interference keep?**
  - **The row.** `batch_16` row 1, REDUNDANT-DOMAIN.
  - **The edge, quoted.** "which of the two a memory sees is the empirical question the source row said no row has opened".
  - **What separates the two readings.** In the row's model, the Jost ratio is 1.0000 on the environment-time carrier and
    0.0769 on the trace-time carrier. Data can tell those two readings apart.
  - **Why it cannot open yet.** CRR does not choose which clock is "own", because ρ is a fit (O1). The trace-time reading
    is the Wickelgren power law the domain already has.
  - **What a lab needs first.** A reading of A1′ that fixes the clock before the data. Otherwise it only re-measures
    Jost's law.
  - **Data.** D1 is likely: public spaced-repetition logs with timestamps. To verify.
- **L05: the shape of a remembered state.**
  - **The rows.** `batch_17` row 1 (Bass diffusion), `batch_31` rows 2–4 (SIR with distancing, car following, Samuelson),
    `batch_28` row 4. All ADDS, "direction known" by the literature check.
  - **The edge.** The direction is known, so a lab could only test the **kernel shape**: geometric q^k (P3) against a fixed
    delay or a power law.
  - **The risk.** CRR does not fix q, and exponential kernels are standard. The lab may reduce to "an exponential moving
    average fits".
  - **Data.** D1 is likely: public vehicle-trajectory and product-adoption data. To verify.
- **L06: mutation per generation against per year.**
  - **The row.** Life_Sciences DS-4, SILENT.
  - **The edge.** The matched pair is in Bergeron et al. 2023, Supplementary Table 9 (D1, not opened).
  - **Why it cannot open yet.** CRR does not say which process is the own event, so the generation is an added assumption.
  - **Not blind.** The quoted spreads (40-fold per generation, more than 120-fold per year, not on one footing) already
    hint at the direction.

## No lab: CRR equals the domain (from the readings of prompt-log entries 218–219 and the bank)

| row | why no lab |
|---|---|
| `batch_04` row 1, aftershocks in natural time | the time-rescaling theorem; CRR renames Ogata's residual analysis |
| `batch_04` row 3, Kepler half-orbits | the antipode and the extremum coincide; the equal arcs are the ellipse's symmetry |
| `batch_05` row 1, two-level system and negative temperature | Ramsey's β = 0 boundary; CRR fixes no temperature scale |
| `batch_13` row 1, the adder | P1: the arc is the added size; H-L5's control can never be beaten (Life_Sciences CD-1) |
| `batch_13` row 3, circadian half-turns | the domain's phase equation gives both durations (13.1276 h and 10.8724 h) |
| `batch_12` row 2, cardiac alternans with memory | REDUNDANT-DOMAIN by the literature check |
| Life_Sciences OL-2, Eigen's threshold with memory | REDUNDANT-IG: μ_c 0.045007 at every q |
| Life_Sciences G-DS2, nanopore segmentation | gate CLOSED |

## D3 and D∅ (a new experiment, or no empirical access)

- **D3, H-CUT on a tabletop physics system.**
  - **The candidate.** An asymmetric relaxation oscillator whose own events and antipodes differ, such as a driven
    stick-slip bench or an electronic relaxation circuit.
  - **The condition.** A lab only if no public record exists; the Marone-lab stick-slip data (`CLAUDE.md` §4) are D1 and
    come first.
  - **What this repository can do.** Write the protocol and the gate. Running it needs equipment and a collaborator.
- **D∅, the loop-quantum-cosmology bounce** (`batch_25` row 3).
  - **What the row shows.** The arc-clock rate is 0.0000 at the bounce, against the scalar clock's 0.9055.
  - **Why only a thought-lab.** There is no empirical access. It stays a thought-lab, never a ledger row.

## Suggested order

1. **L03.** D1 data, a standing gate, and the study fully specified in `CLAUDE.md` §4.
2. **L01 + L02, in one pre-registration.** First a loader VOID rule and an owner decision on the D2 risk.
3. **L04, L05 and L06.** Only after each has an H1 that is fixed before the data and separates from the domain's model on a
   synthetic gate.
