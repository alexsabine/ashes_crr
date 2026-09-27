# Declaration: which 2026 frontier domains CRR's retrodictive record is compatible with

**Status.**
- **The request.** Owner request: prompt-log entry 226 (2026-09-27).
- **When it was pushed.** Before any source is fetched.
- **What it is.** A note, not evidence (R8).
- **Grading.** The rule and the predictions below are fixed now. `labs/frontier/checks/grade.py` grades them from quoted
  sources after the fetch.

## What "where the retrodictive passes sit" means (from pinned outputs only)

**The redundant rows.** `labs/checks/redundant.txt` has 98 redundant rows. They land on five known principles:
1. **(P-IG)** information geometry and the Cramér–Rao bound (arc, unit);
2. **(P-TR)** time-rescaling and conservation-at-threshold (the own clock);
3. **(P-SYM)** symmetry points (the antipodal cut);
4. **(P-EWMA)** exponential smoothing (A6 with P3 weights);
5. **(P-PHASE)** phase reduction on true rotors.

**The ADDS rows.** `labs/checks/themes.txt` holds 11. After the literature check, 6 keep "direction known". All of them are
**remembered-state** models (P-MEM): an agent or population responds to a geometrically smoothed memory of its own past.
The domains are ecology, epidemics, traffic, economics, contingency tracking and cosmological natural selection.

**The WRONG rows** (29) mark where CRR must not be proposed:
- **(W-CLOCK)** H-L5 on driven or controlled oscillators;
- **(W-MEM)** bounded memory where the true rule accumulates or is memoryless;
- **(W-METRIC)** Fisher as the dissipation metric;
- **(W-PATH)** path length as the damage functional;
- **(W-CUT)** the antipode as a physical threshold;
- **(W-FEP)** the Ω and precision readings of the FEP.

The prospective ledger agrees with W-CLOCK (MEAS2-1, CARD-1), W-PATH (T1X2-1) and the H-EQ reductions (EQX, SOTA1).

## The grading rule (fixed before the sources)

**Units.** For each frontier domain, the sources on the day supply one to three **bottleneck questions**. Each is a
verbatim quoted sentence from a 2024–2026 review, perspective or roadmap, with its version.

**Readings.** The investigator reads each bottleneck against the principles above, as one of:
- **COMPATIBLE-P:** the bottleneck is posed in the terms of a principle where CRR's rows landed (P-IG, P-TR, P-SYM,
  P-EWMA, P-PHASE, P-MEM);
- **CONFLICT-W:** it is posed where CRR has WRONG rows (W-*);
- **OUTSIDE:** neither.

**Labels.** For each COMPATIBLE-P bottleneck, the investigator writes CRR's suggested direction here, before the fetch
(below). The label is then computed from the source's own quoted proposals:
- **RESTATES:** the source already names that direction as a proposal or current approach. This is the expected label,
  because CRR's passes are redundant.
- **GUIDES:** the source does not name it, and CRR's direction yields an H1 that differs from the domain's leading H0 in a
  measurable quantity. This makes it a **lab candidate**. It is not a claim of help or novelty, and it still needs the
  labs entry rule: a synthetic gate that can close.
- **SILENT:** CRR's reading gives no direction for that bottleneck.

A CONFLICT-W bottleneck is labelled **AVOID**: CRR's defaults are known to fail there. "Not found in the sources" is never
read as "novel".

## The domains and CRR's directions (written before the fetch)

| # | frontier domain (2026) | expected bottleneck | principle | CRR's suggested direction (fixed now) | expected label |
|---|---|---|---|---|---|
| F1 | continual learning and loss of plasticity in AI (already surveyed: `Continuous_Learning/FRONTIER_BOTTLENECKS.md`) | stability–plasticity; how big each step should be forever | P-IG, P-EWMA | step size set in the model's own Fisher units; the anchor as a geometrically smoothed past (SEC, the one PASS-0 line, is not a CRR rule) | RESTATES (natural gradient, EMA teachers, EWC) |
| F2 | bacterial and eukaryotic cell-cycle control | what couples replication initiation to division; is the initiation adder mechanistic | P-TR, P-MEM | initiation at a fixed phase of the growth–division rotor (CD-3; gate G-CD3 OPEN); a lag-2 "grandmother" memory in birth size | GUIDES (lab L01/L02 candidate) |
| F3 | epidemic forecasting with behavioural feedback | how behaviour responds to perceived risk; waves and plateaus | P-MEM | distancing responds to geometrically remembered prevalence, not current prevalence; predicts oscillation onset set by the memory's mean age | RESTATES (memory kernels in behaviour-epidemic models) |
| F4 | macroeconomic expectations (inflation expectations, de-anchoring) | how households form expectations; when they de-anchor | P-EWMA, P-MEM | expectations as a geometric memory of experienced inflation (experience-weighted learning) | RESTATES (Malmendier–Nagel experience effects, adaptive learning) |
| F5 | traffic flow and automated-vehicle string stability | stability of mixed traffic with human memory and delays | P-MEM | remembered headway destabilises at a mean memory age set by the linear-stability boundary | RESTATES (delay/memory car-following literature) |
| F6 | early-warning signals of critical transitions (ecology, climate) | reliability of EWS; false alarms; what to measure | P-IG, P-TR | measure the approach in the system's own Fisher units (distinguishable steps to the tipping point), not in clock time | GUIDES or RESTATES (Fisher-information EWS exists; the investigator does not know how central) |
| F7 | memory consolidation and forgetting (cognitive neuroscience) | why forgetting follows a power law; spacing; sleep | P-TR, P-MEM | forgetting in natural time (interference events), with Jost's law arising only if interference keys to the trace's own age (lab L04's edge) | GUIDES (a which-clock test) or RESTATES |
| F8 | earthquake forecasting (aftershocks, ML catalogues) | forecasting beyond ETAS; the role of natural time | P-TR | natural time as the compensator is Ogata's residual analysis; no new direction | RESTATES |
| F9 | quantum metrology and sensing | reaching Heisenberg scaling under noise | P-IG | quantum Fisher information in the probe's own units; no new direction | RESTATES |
| F10 | stochastic thermodynamics and optimal finite-time control | minimal-dissipation protocols beyond linear response | W-METRIC | (CRR's Fisher geodesic is WRONG here) | AVOID |
| F11 | active inference and the FEP as a theory of cognition | precision, attention, the clock of belief updating | W-FEP, W-CLOCK | (CRR's readings are WRONG here) | AVOID |
| F12 | circadian medicine and chronotherapy | phase-dependent dosing; entrainment in shift work | P-PHASE | half-turn asymmetry of entrained days follows from the phase-response integral; no new direction | RESTATES |

**What the investigator expects overall.** Most compatible bottlenecks will read RESTATES. GUIDES candidates are expected
only at F2 (cell-cycle, where a gate is already open) and possibly F6 and F7. F10 and F11 are AVOID.

## Sources

Three research agents fetch one to three 2024–2026 reviews or roadmaps per domain, with versions and verbatim quotes of:
- the bottleneck questions;
- the leading proposals.

Raw texts go in the session scratchpad. Dossiers go in `docs/citations/frontier_domains_2026-09-27_*.md`.
F1 reuses the existing dossiers of 2026-09-23 and 2026-09-25.
