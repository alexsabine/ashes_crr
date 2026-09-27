# CRR's retrodictive record against 2026 frontier bottlenecks

**Status.**
- **The request.** Owner request: prompt-log entry 226 (2026-09-27).
- **The order of work.**
  1. The declaration (`DECLARATION.md`, 289a79d) fixed the domains, CRR's directions and the grading rule before any
     source was fetched.
  2. The sources came from three dossiers fetched on the day: `docs/citations/frontier_domains_2026-09-27_{life,complex,physics}.md`.
     F1 reuses the dossier of 2026-09-25.
  3. `checks/verify.txt` found 204 of 204 quotes verbatim.
  4. The labels are computed by `checks/grade.py` (`grade.txt`, CI-checked) from the investigator's readings.
- **What this is.** A note, not evidence (R8). "Not found in the fetched sources" is never read as novel.

## The short answer

| # | frontier domain | CRR principle | CRR's direction named by the field? | label |
|---|---|---|---|---|
| F1 | continual learning, loss of plasticity | information geometry, exponential smoothing | yes (EWC's Fisher-weighted anchor; online EWC's geometric decay) | RESTATES |
| F2a | cell cycle: replication initiation at a fixed phase | own clock, phase | **no** (the field frames it as a fixed mass per origin) | **GUIDES**: a lab candidate (L01) |
| F2b | cell cycle: grandmother memory in birth size | remembered state | yes, and tested: it did not improve the E. coli fit | RESTATES |
| F3 | epidemics with behavioural feedback | remembered state | yes (exponential-decay memory of prevalence; wave period set by the kernel) | RESTATES |
| F4 | inflation expectations | exponential smoothing, remembered state | yes (experience-weighted averages, constant-gain learning) | RESTATES |
| F5 | traffic and automated-vehicle string stability | remembered state | yes (distributed-delay driver memory; IDM with memory) | RESTATES |
| F6 | early warnings of tipping points | information geometry | yes (Fisher information as an indicator since 2008) | RESTATES |
| F7 | forgetting and consolidation | own clock, remembered state | yes (interference-event clocks; Jost's law from interference; decay against competitors) | RESTATES |
| F8 | earthquake forecasting | own clock | yes (time-rescaling residuals; event-count natural time) | RESTATES |
| F9 | quantum metrology | information geometry | yes (quantum Cramér–Rao bound, quantum Fisher information) | RESTATES |
| F10 | stochastic thermodynamics, minimal dissipation | (CRR WRONG: Fisher as the dissipation metric) | the field names the friction tensor | **AVOID** |
| F11 | active inference and the FEP | (CRR WRONG: Ω and precision readings) | the field poses precision and the update clock itself | **AVOID** |
| F12 | circadian medicine | phase | yes (advance/delay areas of the phase-response curve) | RESTATES |

**Tally:** RESTATES 10, GUIDES 1, AVOID 2. The declared expectations were met on 12 of 13. The miss is F2b: the grandmother
term was expected to GUIDE but is already named and tested.

## What this says

**1. Where CRR's passes sit is where frontier fields already work.**
- **The same tools are already in use.** The redundant rows landed on information geometry, time-rescaling, exponential
  smoothing and phase reduction. The frontier fields that use those tools already hold CRR's direction as their own
  current approach:
  - online EWC's geometric Fisher decay (F1);
  - an exponential-decay memory of prevalence fitted to epidemic data (F3);
  - Malmendier–Nagel's time-discounted experience (F4);
  - distributed-delay driver memory (F5);
  - Fisher-information early warnings (F6);
  - interference clocks for forgetting (F7);
  - residual analysis for aftershocks (F8);
  - the quantum Cramér–Rao bound (F9);
  - phase-response areas (F12).
- **Compatibility is real but redundant.** CRR speaks the same language as these fields because the language is theirs.

**2. The open bottlenecks are mostly ones CRR's ingredients do not address.** The quoted bottlenecks ask about:
- molecular mechanisms (what sets the initiation mass, and why forgetting is active);
- identifiability and calibration (how strong the memory is in epidemic behaviour, and how far back consumers look);
- data and benchmarks (neural point processes do not beat ETAS; warnings in real systems);
- noise and robustness (Heisenberg scaling under decoherence);
- individual variation (internal circadian time).

CRR supplies none of these. It supplies a way of writing a memory or a clock, which these fields already write.

**3. In two fields the frontier has moved past CRR's direction.**
- **F4.** The 2021–23 de-anchoring of inflation expectations is posed *against* a simple experience-weighted memory.
  Selective recall by similarity is proposed instead.
- **F2b.** The grandmother term was tested and did not improve the E. coli fit.

In both, CRR's geometric memory is the baseline being improved on, not the answer.

**4. One direction is not in the fetched literature and can be tested: F2a.**
- **The claim.** CRR places replication initiation at the antipode of the growth–division phase.
- **The field's framing.** Initiation at a fixed mass per origin, or the initiation-to-initiation double adder.
- **Why it can be tested.** The two separate on the synthetic gate G-CD3, which is OPEN (`Life_Sciences/checks/phase_a.txt`).
- **What the label means.** "GUIDES" means a lab candidate, not help. The investigator's written forecast on real lineages
  is FAIL, because the field's rule predicts initiation to within a few hundredths of a cycle in its own world.
- **Why it could still matter.** It is the only place in these twelve fields where CRR makes a claim the field does not
  already make, and a decisive test is possible on public data (Witz et al. 2019; lab L01 + L02).

**5. Two frontiers are places to stay out of.**
- **F10.** Minimal-dissipation control uses the friction tensor, and Wasserstein-type geometry beyond linear response.
  CRR's Fisher geodesic was WRONG on three trap rows.
- **F11.** Active inference already poses precision-as-attention and continuous-versus-event belief updating. CRR's
  readings there were WRONG.

## Can CRR guide these fields toward resolutions?

On this evidence, mostly no.
- **Why not.** CRR's compatible ingredients are the fields' existing tools. Its distinctive defaults (a universal clock,
  bounded memory, the Fisher metric, the antipode as a threshold) are the ones that fail where fields have specific
  mechanisms.
- **The useful role it has.** It gives one vocabulary across these fields, and it can show where a result in one field
  already exists in another. For example, the wave period set by a memory kernel in epidemics is the same object as
  distributed-delay string stability in traffic and constant-gain learning in expectations. That cross-field mapping is
  teaching and translation, not resolution.
- **The one test.** F2a (lab L01) is the one place where a CRR claim could be decided against a field's H0 on existing
  data.

## Sources and limits

- **Sources.** Each domain has one to four reviews, perspectives or roadmaps, most from 2024–2026, plus targeted searches
  for CRR's directions. Versions and fetch status are in the three dossiers.
- **Paywalled or blocked.** Some primaries were blocked, and some were quoted from abstracts only:
  - three active-inference reviews;
  - one earthquake-forecasting paper, read from an author PDF;
  - some PMC pages and publisher PDFs.
- **Readings.** The readings are the investigator's. For F2, the declaration's single direction was split into F2a and F2b
  after reading, because the sources treat the two claims separately (AGENT_LOG 166). The declared expectation for both
  halves is kept.
