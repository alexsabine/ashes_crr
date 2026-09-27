# Frontier domains, life sciences (F2, F7, F12): bottlenecks, proposals and CRR's declared directions — sources fetched 2026-09-27

A note, not evidence (R8). Quotes are verbatim substrings of the saved texts.

- **Declaration.** `labs/frontier/DECLARATION.md`. It was pushed before this fetch. The grading rule and CRR's directions are fixed there.
- **What this dossier does.** It supplies the source quotes only. It assigns no COMPATIBLE-P / RESTATES / GUIDES label; that is `labs/frontier/checks/grade.py`'s job.
- **What this dossier does not do.** It never claims novelty. "Not found in the fetched texts" is not "novel".
- **Raw texts.** In the session scratchpad at `/tmp/claude-0/-home-user-ashes-crr/77fb7a2b-ce3d-5c52-a1a6-710031fa20e9/scratchpad/frontier/life/`:
  - PMC JATS XML, fetched through NCBI E-utilities `efetch`, with the plain text extracted beside it;
  - PubMed abstracts where the full text is paywalled;
  - arXiv HTML or PDF text (pypdf 6.19.0).
- **Machine-readable claims.** `/tmp/claude-0/-home-user-ashes-crr/77fb7a2b-ce3d-5c52-a1a6-710031fa20e9/scratchpad/frontier/life_claims.json`.
- **Quote check.** 33 claims hold 61 quote strings. Each was checked in Python to be a substring of its saved text after whitespace collapse: **61/61 verified**.
- **Fetch status.** Every fetch in the tables returned HTTP 200. One transient HTTP 429 from E-utilities was retried and then succeeded.
- **Articles outside the window.** Research articles and older items reached by the targeted direction searches are marked as such in the tables. They are not bottleneck reviews.

## F2 — Bacterial and eukaryotic cell-cycle control (replication initiation and division; is the adder mechanistic)

Declaration's CRR direction (fixed before the fetch): initiation at a fixed phase of the growth–division rotor (CD-3; gate G-CD3 OPEN); a lag-2 "grandmother" memory in birth size.

### Sources

| source | version / date / DOI | URL | fetch | raw file |
|---|---|---|---|---|
| Chadha, Khurana, Schmoller, 'Eukaryotic cell size regulation and its implications for cellular function and dysfunction', Physiol Rev 104:1679 | epub 2024-06-20; issue 2024-10-01; DOI 10.1152/physrev.00046.2023; PMC11495193 | https://pmc.ncbi.nlm.nih.gov/articles/PMC11495193/ | HTTP 200, full text | `frontier/life/F2_physiolrev2024_eukaryotic_size.txt` |
| Serbanescu, Ojkic, Banerjee, 'Cellular resource allocation strategies for cell size and shape control in bacteria', FEBS J 289:7891 | epub 2021-10-30; issue 2022-12; DOI 10.1111/febs.16234; PMC9016100 | https://pmc.ncbi.nlm.nih.gov/articles/PMC9016100/ | HTTP 200, full text | `frontier/life/F2_febsj2022_resource_allocation.txt` |
| Herrick, 'DNA/Cell Mass Homeostasis: Coordinating DNA Replication and Cell Size with Central Carbon Metabolism During Bacterial Growth', Genes 17:695 | epub 2026-06-15; DOI 10.3390/genes17060695; PMC13300287 | https://pmc.ncbi.nlm.nih.gov/articles/PMC13300287/ | HTTP 200, full text | `frontier/life/F2_genes2026_dna_mass.txt` |
| Torres, Carrasco, Ayora, Alonso, 'Mechanisms of chromosomal DNA replication in Escherichia coli and Bacillus subtilis', FEMS Microbiol Rev 50:fuag021 | epub 2026-05-14; DOI 10.1093/femsre/fuag021; PMC13220808 | https://pmc.ncbi.nlm.nih.gov/articles/PMC13220808/ | HTTP 200, full text | `frontier/life/F2_femsmr2026_replication.txt` |
| Witz, van Nimwegen, Julou, 'Initiation of chromosome replication controls both division and replication cycles in E. coli through a double-adder mechanism', eLife 8:e48063 (research article; targeted search) | pub 2019-11-11; DOI 10.7554/eLife.48063; PMC6890467 | https://pmc.ncbi.nlm.nih.gov/articles/PMC6890467/ | HTTP 200, full text | `frontier/life/F2_elife2019_double_adder.txt` |
| Zhang, Fei, Dunkel, 'Nonlinear memory in cell-division dynamics across species', PNAS 122:e2417416122 (research article; targeted search) | pub 2025-09-03; DOI 10.1073/pnas.2417416122; PMC12435308 | https://pmc.ncbi.nlm.nih.gov/articles/PMC12435308/ | HTTP 200, full text | `frontier/life/F2_pnas2025_nonlinear_memory.txt` |
| ElGamel, Vashistha, Salman, Mugler, 'Multigenerational memory in bacterial size control', arXiv:2206.05340 (Phys Rev E 108, L032401) (research letter; targeted search) | arXiv v2, 2023-05-24 (v1 2022-06-10) | https://arxiv.org/pdf/2206.05340v2 | HTTP 200, full text | `frontier/life/F2_arxiv2206.05340v2.txt` |

### Quotes

- [BOTTLENECK] *Eukaryotic cell size regulation and its implications for cellular function and dysfunction* (epub 2024-06-20).
  - **Note.** eukaryotic: the size-sensing signal behind adder/sizer phenomenology
  - "For size to be controlled by a sizer- or an adder-like mechanism, a molecular signal that measures cell size is required."
  - "The size reporter property for the commitment decision, however, remains elusive."
- [PROPOSAL] *Eukaryotic cell size regulation and its implications for cellular function and dysfunction* (epub 2024-06-20).
  - **Note.** titration / reporter-vs-constant size sensing; adder as emergent from phase-specific controls
  - "One way for a cell to sense its size is by comparison of two biochemical properties: one that changes with cell size (a “reporter” property) and one that stays constant as cell size changes (a “constant” property), similar to a titration."
  - "in budding yeast, the G1 phase exhibits a weak sizer and the S/G2/M phase exhibits a timer, but an approximate adder emerges when the entire cell cycle is considered"
- [BOTTLENECK] *Cellular resource allocation strategies for cell size and shape control in bacteria* (epub 2021-10-30).
  - **Note.** is the adder mechanistic; origin of the invariant initiation mass
  - "the adder model does not readily reveal a molecular basis for cell size control nor any connections between cell size and growth physiology."
  - "The invariance of initiation mass with elongation rate and birth size is consistent with the threshold initiation model, but its mechanistic origin remains unknown."
- [PROPOSAL] *Cellular resource allocation strategies for cell size and shape control in bacteria* (epub 2021-10-30).
  - **Note.** replication-initiation-centric (C+D timer), double adder, independent adders, threshold accumulation (FtsZ)
  - "In this model, cell divides after a fixed time interval (C + D period) since the initiation of chromosome replication."
  - "Recently, a replication double adder model has been proposed [72], where cells grow by a fixed volume per replication origin between two consecutive initiation cycles, and cell divides after elongation by a constant volume per origin of replication."
  - "the chromosome replication initiation and cellular division have been shown to be controlled independently"
  - "a recent study has identified the protein FtsZ as the key size sensor molecule that reaches a threshold abundance at the time of cell division"
- [BOTTLENECK] *DNA/Cell Mass Homeostasis: Coordinating DNA Replication and Cell Size with Central Carbon Metabolism During Bacterial Growth* (epub 2026-06-15).
  - **Note.** what sets the initiation mass
  - "Why and how cell size varies with DNA content remains an unresolved question of both evolutionary and physiological interest."
  - "might have the yet-unrealized potential to explain, at least in part, the long-standing mystery of the multiple mechanisms that determine the initiation mass in bacteria."
- [PROPOSAL] *DNA/Cell Mass Homeostasis: Coordinating DNA Replication and Cell Size with Central Carbon Metabolism During Bacterial Growth* (epub 2026-06-15).
  - **Note.** DnaA-RNR homeostatic pair (single-author review; the author flags it as open)
  - "the hypothesis that DnaA and RNR form a homeostatic pair that sets the Mi"
  - "DnaA, it seems, serves mainly as a licensing factor at oriC (similar to the eukaryote Origin Recognition Complex) and not as a timer in initiation control."
  - "This, however, remains an open question."
- [PROPOSAL] *Mechanisms of chromosomal DNA replication in Escherichia coli and Bacillus subtilis* (epub 2026-05-14).
  - **Note.** the standard framing: initiation at a fixed cell mass (not a fixed phase)
  - "which initiate replication at a fixed cell mass"
- [BOTTLENECK] *Initiation of chromosome replication controls both division and replication cycles in E. coli through a double-adder mechanism* (pub 2019-11-11).
  - **Note.** 2019 research article (older than the window); the coupling question as posed
  - "It remains unclear how bacteria such as Escherichia coli tightly coordinate those two cycles across a wide range of growth conditions."
- [PROPOSAL] *Initiation of chromosome replication controls both division and replication cycles in E. coli through a double-adder mechanism* (pub 2019-11-11).
  - **Note.** initiation-to-initiation double adder
  - "the cell cycle is driven from one initiation event to the next rather than from birth to division and is controlled by two adder mechanisms: the added volume since the last initiation event determines the timing of both the next division and replication initiation events."
- [DIRECTION-NAMED] *Nonlinear memory in cell-division dynamics across species* (pub 2025-09-03).
  - **Note.** DIRECTION-NAMED (lag-2 / grandmother memory): named and tested; for E. coli the grandmother term did not improve BIC
  - "However, despite such major progress, there still exist fundamental open questions regarding the nonlinear and multigenerational memory (28) effects that are not captured by some of the currently prevailing standard models of cell-size homeostasis."
  - "one with two-generation memory λt=λ(st,st∗,st∗∗), where the current size st, the mother size st∗, and the grandmother size st∗∗ represent progressively higher orders of memory in the cell-division rate λ"
  - "Perhaps surprisingly, adding memory of the grandmother size st∗∗ does not further improve the BIC score of the model"
- [DIRECTION-NAMED] *Multigenerational memory in bacterial size control* (arXiv v2, 2023-05-24 (v1 2022-06-10)).
  - **Note.** DIRECTION-NAMED (multigenerational memory; phase depends on previous generation's phase = lag-2 structure in birth size)
  - "However, recent evidence from comparing sister lineages suggests that correlations in size fluctuations can persist for many generations."
  - "In particular, it is still unclear whether deviations from the average size dissipate over one or many generations"
  - "which accounts for the generational dependence of the phase"
- [DIRECTION-NAMED, PARTIAL] *Multigenerational memory in bacterial size control* (arXiv v2, 2023-05-24 (v1 2022-06-10)).
  - **Note.** PARTIAL: a growth 'phase' (ln-size advanced) is used for division control; initiation at a fixed phase of the growth-division cycle not found named in fetched texts
  - "consider a cell born with size xn that grows exponentially for an elapsed phase ϕn, the product of the growth rate and cell cycle time"

### Directions not found or not covered

- **[DIRECTION-NOT-FOUND-IN-FETCHED] Initiation at a fixed *phase* of the growth–division cycle.** Searched all seven F2 saved texts with the regex `initiat\w*.{0,80}\b(phase|cell age|age)\b` and its reverse, plus one targeted web search ("replication initiation" E. coli single cell "cell age" OR "phase of the cell cycle" ... fixed fraction of generation time). No fetched text names initiation at a fixed phase (fraction of the cycle or fixed ln-size advance). The fetched framings are initiation at a fixed cell mass / volume per origin (FEMS 2026, Genes 2026, FEBS J 2022), an initiation-to-initiation adder (eLife 2019), and a C+D timer from initiation (FEBS J 2022). The nearest item is ElGamel et al.'s growth "phase" ϕn used for *division* control (quoted above as PARTIAL). Not found is not novel: the search covered seven texts and one web query.

## F7 — Memory consolidation and forgetting (power law, spacing, sleep, interference)

Declaration's CRR direction: forgetting in natural time (interference events), with Jost's law arising only if interference keys to the trace's own age; the "which clock" test (time-based decay vs interference).

### Sources

| source | version / date / DOI | URL | fetch | raw file |
|---|---|---|---|---|
| Berry, Guhle, Davis, 'Active forgetting and neuropsychiatric diseases', Mol Psychiatry 29:2810 | 2024-09; DOI 10.1038/s41380-024-02521-9; PMC11420092 | https://pmc.ncbi.nlm.nih.gov/articles/PMC11420092/ | HTTP 200, full text | `frontier/life/F7_molpsych2024_active_forgetting.txt` |
| de Snoo, Frankland, 'Neurobiological mechanisms of forgetting across timescales', Curr Opin Neurobiol 90:102972 | epub 2025-01-31; DOI 10.1016/j.conb.2025.102972; PMID 39892316 (abstract only) | https://pubmed.ncbi.nlm.nih.gov/39892316/ | HTTP 200, abstract only (PubMed efetch) | `frontier/life/F7_conb2025_forgetting_timescales_abs.txt` |
| Autore, Drew, Ryan, 'The cost of remembering: engram competition as a flexible mechanism of forgetting', Trends Neurosci 48:728-738 | epub 2025-08-14; DOI 10.1016/j.tins.2025.07.011; PMID 40813160 (abstract only) | https://pubmed.ncbi.nlm.nih.gov/40813160/ | HTTP 200, abstract only (PubMed efetch) | `frontier/life/F7_tins2025_engram_competition_abs.txt` |
| Brodt, Inostroza, Niethard, Born, 'Sleep - A brain-state serving systems memory consolidation', Neuron 111:1050-1075 | 2023-04-05; DOI 10.1016/j.neuron.2023.03.005; PMID 37023710 (abstract only) | https://pubmed.ncbi.nlm.nih.gov/37023710/ | HTTP 200, abstract only (PubMed efetch) | `frontier/life/F7_neuron2023_sleep_consolidation_abs.txt` |
| Georgiou, Katkov, Tsodyks, 'Retroactive interference model of forgetting', J Math Neurosci 11:4 (research article; targeted search) | epub 2021-01-23; DOI 10.1186/s13408-021-00102-6; PMC7826326 | https://pmc.ncbi.nlm.nih.gov/articles/PMC7826326/ | HTTP 200, full text | `frontier/life/F7_jmathneuro2021_retroactive_interference.txt` |
| Wixted, 'On Common Ground: Jost's (1897) Law of Forgetting and Ribot's (1881) Law of Retrograde Amnesia', Psychol Rev 111(4):864-879 (targeted search; older than the window) | 2004; DOI 10.1037/0033-295X.111.4.864; author PDF | http://wixtedlab.ucsd.edu/publications/wixted/Jost_Law.pdf | HTTP 200, full text | `frontier/life/F7_wixted2004_jost.txt` |
| Ray Barman, Starenky, Bodnar, Narasimhan, Gopinath, 'The Geometry of Forgetting', arXiv:2604.06222 (preprint; targeted search) | arXiv v1, 2026-03-27 | https://arxiv.org/html/2604.06222 | HTTP 200, full text | `frontier/life/F7_arxiv2604.06222v1.txt` |

### Quotes

- [BOTTLENECK] *Active forgetting and neuropsychiatric diseases* (2024-09).
  - **Note.** mechanism of forgetting; sleep
  - "Mechanistic studies of forgetting began only about one decade ago, so there remains much more to be discovered."
  - "The underlying mechanisms of sleep-dependent memory enhancement are still being defined and are diverse."
- [PROPOSAL] *Active forgetting and neuropsychiatric diseases* (2024-09).
  - **Note.** active (dopamine/Rac1) forgetting; sleep protects from interference; synaptic downscaling
  - "Thus, DAn driven active forgetting mechanisms provide a biological explanation for interference-based forgetting."
  - "Another possible mechanism, not mutually exclusive with the first, is that sleep and rest inhibit active forgetting of labile memory, potentially protecting nascent memory traces from interference so they can be consolidated [113, 124]."
  - "First, sleep leads to synaptic downscaling that broadly reduces synapse strength and thus theoretically could degrade engrams [127–129]."
- [BOTTLENECK] *Neurobiological mechanisms of forgetting across timescales* (epub 2025-01-31).
  - **Note.** forgetting across timescales
  - "However, changes in accessibility emerge on vastly different timescales."
- [PROPOSAL] *Neurobiological mechanisms of forgetting across timescales* (epub 2025-01-31).
  - **Note.** engram accessibility
  - "Viewed this way, forgetting encompasses a family of plasticity mechanisms that modulate engram accessibility, perhaps in order to prioritize those memories that are most timely or relevant to the situation at hand."
- [PROPOSAL] *The cost of remembering: engram competition as a flexible mechanism of forgetting* (epub 2025-08-14).
  - **Note.** engram competition (an interference account)
  - "One explanation for the forgetting of particular memories is active competition between memory engrams for expression in the brain."
- [BOTTLENECK] *Sleep - A brain-state serving systems memory consolidation* (2023-04-05).
  - **Note.** sleep vs wake consolidation
  - "Although long-term memory consolidation is supported by sleep, it is unclear how it differs from that during wakefulness."
- [PROPOSAL] *Sleep - A brain-state serving systems memory consolidation* (2023-04-05).
  - **Note.** replay
  - "identifies the repeated replay of neuronal firing patterns as a basic mechanism triggering consolidation during sleep and wakefulness."
- [DIRECTION-NAMED] *Retroactive interference model of forgetting* (epub 2021-01-23).
  - **Note.** DIRECTION-NAMED (forgetting counted in interfering events, i.e. an event clock)
  - "One such mechanism proposed in previous studies is retrograde interference, stating that a memory can be erased due to subsequently acquired memories."
  - "For simplicity, we assume that memories are acquired at a constant rate (one new memory per time step)."
  - "consider a memory acquired at time 0 followed by t other memories."
- [DIRECTION-NAMED] *Retroactive interference model of forgetting* (epub 2021-01-23).
  - **Note.** DIRECTION-NAMED (forgetting rate decreasing with age from interference; here via valence selection, not age-keyed vulnerability)
  - "Therefore the probability that a unit will be forgotten at the next time step is a strictly decaying function of its age"
- [DIRECTION-NAMED] *On Common Ground: Jost's (1897) Law of Forgetting and Ribot's (1881) Law of Retrograde Amnesia* (2004).
  - **Note.** DIRECTION-NAMED (Jost's law from interference whose force decays with the trace's age)
  - "One reason why memories might decay less rapidly with age is because they become less vulnerable to the forces of retroactive interference (RI) as a result of consolidation."
  - "If it is true that memory traces become less vulnerable to the effects of subsequent memory formation as a result of the process of consolidation, then forgetting functions would be expected to exhibit an ever-decreasing rate of decay"
- [DIRECTION-NAMED] *The Geometry of Forgetting* (arXiv v1, 2026-03-27).
  - **Note.** DIRECTION-NAMED ('which clock': time-based decay vs number of competitors); math symbols stripped in saved text
  - "Decay theories say memory traces fade with time."
  - "The critical test: does the forgetting exponent depend on the decay function or on the number of competing memories?"
  - "Power-law forgetting ( , human ) arises from interference among competing memories, not from decay."
- [DIRECTION-NAMED] *Retroactive interference model of forgetting* (epub 2021-01-23).
  - **Note.** DIRECTION-NAMED (decay vs interference framing)
  - "Mechanisms that are usually considered in relation to forgetting are passive decay of memories, interference, and consolidation"

### Directions not found or not covered

- **Spacing effect.** No dedicated 2022–2026 spacing-effect review with full text was found in the PubMed search tried (`"spacing effect" OR "spaced training" OR "distributed practice"` AND mechanism/theory AND review). Spacing appears in the fetched texts only as a secondary result of the arXiv 2604.06222 preprint. This dossier states no spacing bottleneck.

## F12 — Circadian medicine and chronotherapy (phase-dependent dosing; entrainment in shift work)

Declaration's CRR direction: half-turn asymmetry of entrained days follows from the phase-response integral; no new direction.

### Sources

| source | version / date / DOI | URL | fetch | raw file |
|---|---|---|---|---|
| Boivin, Boudreau, Kosmadopoulos, 'Disturbance of the Circadian System in Shift Work and Its Health Impact', J Biol Rhythms 37:3 | epub 2021-12-30; issue 2022-02; DOI 10.1177/07487304211064218; PMC8832572 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8832572/ | HTTP 200, full text | `frontier/life/F12_jbr2022_shiftwork.txt` |
| Easton, Gupta, Vincent, Ferguson, 'Move the night way: how can physical activity facilitate adaptation to shift work?', Commun Biol 7:259 | epub 2024-03-02; DOI 10.1038/s42003-024-05962-8; PMC10908783 | https://pmc.ncbi.nlm.nih.gov/articles/PMC10908783/ | HTTP 200, full text | `frontier/life/F12_commbio2024_shiftwork_activity.txt` |
| Lee, Field, Sehgal, 'Circadian Rhythms, Disease and Chronotherapy', J Biol Rhythms 36:503 | epub 2021-09-22; issue 2021-12; DOI 10.1177/07487304211044301; PMC9197224 | https://pmc.ncbi.nlm.nih.gov/articles/PMC9197224/ | HTTP 200, full text | `frontier/life/F12_jbr2021_chronotherapy.txt` |
| Gong, Ren, Xiong, Wu et al., 'Toward adaptive therapeutic timing: integration of mechanistic pharmacology and artificial intelligence in precision dosing', Front Pharmacol 17:1890846 | pub 2026-09-03; DOI 10.3389/fphar.2026.1890846; PMC13582453 | https://pmc.ncbi.nlm.nih.gov/articles/PMC13582453/ | HTTP 200, full text | `frontier/life/F12_frontpharm2026_adaptive_timing.txt` |
| Uriu, Tei, 'Complementary phase responses via functional differentiation of dual negative feedback loops', PLoS Comput Biol 17:e1008774 (research article; targeted search) | 2021; DOI 10.1371/journal.pcbi.1008774; PMC7971863 | https://pmc.ncbi.nlm.nih.gov/articles/PMC7971863/ | HTTP 200, full text | `frontier/life/F12_ploscb2021_complementary_prc.txt` |

### Quotes

- [BOTTLENECK] *Disturbance of the Circadian System in Shift Work and Its Health Impact* (epub 2021-12-30).
  - **Note.** entrainment resistance in shift work; internal desynchrony
  - "Simulated night-shift experiments and field-based studies with shift workers both indicate that the circadian system is resistant to adaptation from a day- to a night-oriented schedule, as determined by a lack of substantial phase shifts over multiple days in centrally controlled rhythms, such as those of melatonin and cortisol."
  - "The size effects, in real working environments, of specific factors mediating the health impacts of atypical shifts remain unclear."
- [PROPOSAL] *Disturbance of the Circadian System in Shift Work and Its Health Impact* (epub 2021-12-30).
  - **Note.** light scheduling
  - "Light attenuation with goggles or sunglasses during the morning commute after night shifts has been shown to facilitate phase shifting"
  - "Three cycles of 8-h bright light exposure at night induced significant phase delays of ~7 to 9 h for central and peripheral markers"
- [BOTTLENECK] *Move the night way: how can physical activity facilitate adaptation to shift work?* (epub 2024-03-02).
  - **Note.** none
  - "However, evidence of real-world circadian adaptation is found primarily in occupations where light exposure is readily controlled."
  - "Despite this, non-photic adaptation to shift work remains under researched."
- [PROPOSAL] *Move the night way: how can physical activity facilitate adaptation to shift work?* (epub 2024-03-02).
  - **Note.** exercise as zeitgeber; light timing by advance/delay direction
  - "We also propose that physical activity might be an accessible and cost-effective countermeasure that could influence multiple markers of adaptation across three timeframes (Within Shift, Within Block, Within Work-span)."
  - "Light exposure during the early morning hours of a night shift will naturally advance circadian rhythms64, thereby working against the desired delay."
- [BOTTLENECK] *Circadian Rhythms, Disease and Chronotherapy* (epub 2021-09-22).
  - **Note.** individual internal time
  - "(3) How generalizable is the application of circadian medicine? Individual variability in circadian rhythms, caused by genetics or environmental factors (e.g. chronotype, lifestyle, illness, age), could have significant effects on treatment, suggesting chronotherapy may need to be individualized for patients."
- [PROPOSAL] *Circadian Rhythms, Disease and Chronotherapy* (epub 2021-09-22).
  - **Note.** none
  - "(1) Clocks as targets; non-pharmaceutical or pharmacological interventions to manipulate circadian rhythms or circadian components; (2) Clocks as modulators: timing of medicine to the endogenous rhythm established by clocks in order to improve efficacy and reduce side effects."
- [BOTTLENECK] *Toward adaptive therapeutic timing: integration of mechanistic pharmacology and artificial intelligence in precision dosing* (pub 2026-09-03).
  - **Note.** estimating internal phase
  - "Strong circadian biomarkers such as melatonin and cortisol can also require invasive or specialized testing, which limits routine use."
  - "These shortcomings make it harder for models to estimate the circadian state reliably in everyday care."
- [PROPOSAL] *Toward adaptive therapeutic timing: integration of mechanistic pharmacology and artificial intelligence in precision dosing* (pub 2026-09-03).
  - **Note.** none
  - "AI-enabled chronotherapy is moving toward closed-loop, sensor-based, and adaptive treatment."
- [DIRECTION-NAMED] *Complementary phase responses via functional differentiation of dual negative feedback loops* (2021).
  - **Note.** DIRECTION-NAMED (advance/delay PRC areas set entrainment and its phase)
  - "To quantify the shape of a PRC, we measure the unsigned areas of its advance (Δϕ ≥ 0) and delay (Δϕ < 0) zones, which we refer to A and D (A ≥ 0, D ≥ 0), respectively."
  - "the ratio of light-induced transcription rates between Per1 and Per2 determines the proportion of phase advance and delay zones in a PRC, and thereby determines the entrainability of a circadian clock to a 24-hour LD cycle."
  - "Thus, as our simulations suggested, the administration of such compounds may adjust the phase of entrainment to be more desirable for daily life."

### Directions not found or not covered

- **Direction in the fetched *reviews*: not named.** The four F12 reviews (JBR 2022, JBR 2021, Commun Biol 2024, Front Pharmacol 2026) were searched for `phase[- ]response|PRC|phase angle|asymmetr|advance.{0,60}delay`. None names the phase-response curve or its integrals. Only Commun Biol 2024 uses the advance-versus-delay direction of light timing (quoted above as a proposal). One targeted web search (phase of entrainment determined by phase response curve advance delay region asymmetry ...) found Uriu & Tei 2021, which names it (quoted as DIRECTION-NAMED). The classical entrainment literature (Pittendrigh, Daan) that the search summary alludes to was not fetched.

## Summary of the direction check (source quotes only; no label)

- **F2, lag-2 / grandmother memory.** NAMED.
  - Zhang, Fei & Dunkel (PNAS 2025) test a two-generation (grandmother) memory model. It did not improve BIC for E. coli.
  - ElGamel et al. (arXiv v2 2023 / PRE) name multigenerational memory, with a phase that depends on the previous generation.
- **F2, initiation at a fixed phase.** NOT FOUND in the fetched texts. The literature frames initiation as occurring at a fixed mass or volume per origin, or as an adder between initiations.
- **F7, forgetting counted in interfering events.** NAMED (Georgiou, Katkov & Tsodyks 2021).
- **F7, Jost's law from interference that weakens with the trace's age.** NAMED (Wixted 2004, consolidation reading of Jost's law).
- **F7, the which-clock question (decay vs interference).** NAMED (arXiv 2604.06222 v1, 2026; Georgiou et al. 2021).
- **F12, advance/delay PRC areas set entrainment.** NAMED in a 2021 research article (Uriu & Tei). Not named in the four fetched reviews.
