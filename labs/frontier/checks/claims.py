"""Claims and readings for labs/frontier/DECLARATION.md (pushed at 289a79d before any source), transcribed from
docs/citations/frontier_domains_2026-09-27_{life,complex,physics}.md (fetched 2026-09-27; raw texts in the session scratchpad
frontier/{life,cx,phys}/) and, for F1, from docs/citations/frontier_plasticity_2026-09-25.md (raw texts lit0925/plasticity/).
READINGS are the investigator's, decided after reading the quotes. F2 was split into F2a and F2b after reading (AGENT_LOG 166):
the declaration's F2 direction joined two claims that the sources treat separately.
"""

CLAIMS = [{'domain': 'F1',
  'kind': 'BOTTLENECK',
  'source': 'Dohare, Hernandez-Garcia, Lan, Rahman, Mahmood, Sutton, "Loss of plasticity in deep continual learning" '
            '(abstract)',
  'version': 'arXiv 2306.13812 v3, 2024-04-09 (Nature 632, 2024); fetched 2026-09-25',
  'url': 'https://arxiv.org/abs/2306.13812',
  'quote': ['More fundamental, but less well known, is that they may also lose their ability to learn on new examples, '
            'a phenomenon called loss of plasticity.'],
  'raw_file': 'lit0925/plasticity/abs_2306.13812.txt',
  'note': 'reused from docs/citations/frontier_plasticity_2026-09-25.md',
  'id': 'f1:0'},
 {'domain': 'F1',
  'kind': 'DIRECTION',
  'source': 'Kirkpatrick et al., "Overcoming catastrophic forgetting in neural networks" (EWC; abstract)',
  'version': 'arXiv 1612.00796; fetched 2026-09-25',
  'url': 'https://arxiv.org/abs/1612.00796',
  'quote': ['Our approach remembers old tasks by selectively slowing down learning on the weights important for those '
            'tasks.'],
  'raw_file': 'lit0925/plasticity/abs_1612.00796.txt',
  'note': 'a Fisher-weighted anchor to the past (P-IG)',
  'id': 'f1:1'},
 {'domain': 'F1',
  'kind': 'DIRECTION',
  'source': 'Schwarz et al., "Progress & Compress" (online EWC; full text)',
  'version': 'arXiv 1805.06370 (ar5iv); fetched 2026-09-25',
  'url': 'https://arxiv.org/abs/1805.06370',
  'quote': ['where $\\gamma<1$ is a hyperparameter associated with removing the approximation term associated with the '
            'previous presentation of task $i$'],
  'raw_file': 'lit0925/plasticity/ft_1805.06370.txt',
  'note': 'the geometric (gamma) decay of the past Fisher penalty (P-EWMA)',
  'id': 'f1:2'},
 {'domain': 'F2',
  'kind': 'BOTTLENECK',
  'source': "Chadha, Khurana, Schmoller, 'Eukaryotic cell size regulation and its implications for cellular function "
            "and dysfunction', Physiol Rev 104:1679",
  'version': 'epub 2024-06-20; issue 2024-10-01; DOI 10.1152/physrev.00046.2023; PMC11495193',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11495193/',
  'quote': ['For size to be controlled by a sizer- or an adder-like mechanism, a molecular signal that measures cell '
            'size is required.',
            'The size reporter property for the commitment decision, however, remains elusive.'],
  'raw_file': 'frontier/life/F2_physiolrev2024_eukaryotic_size.txt',
  'note': 'eukaryotic: the size-sensing signal behind adder/sizer phenomenology',
  'id': 'life:0'},
 {'domain': 'F2',
  'kind': 'PROPOSAL',
  'source': "Chadha, Khurana, Schmoller, 'Eukaryotic cell size regulation and its implications for cellular function "
            "and dysfunction', Physiol Rev 104:1679",
  'version': 'epub 2024-06-20; issue 2024-10-01; DOI 10.1152/physrev.00046.2023; PMC11495193',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11495193/',
  'quote': ['One way for a cell to sense its size is by comparison of two biochemical properties: one that changes '
            'with cell size (a “reporter” property) and one that stays constant as cell size changes (a “constant” '
            'property), similar to a titration.',
            'in budding yeast, the G1 phase exhibits a weak sizer and the S/G2/M phase exhibits a timer, but an '
            'approximate adder emerges when the entire cell cycle is considered'],
  'raw_file': 'frontier/life/F2_physiolrev2024_eukaryotic_size.txt',
  'note': 'titration / reporter-vs-constant size sensing; adder as emergent from phase-specific controls',
  'id': 'life:1'},
 {'domain': 'F2',
  'kind': 'BOTTLENECK',
  'source': "Serbanescu, Ojkic, Banerjee, 'Cellular resource allocation strategies for cell size and shape control in "
            "bacteria', FEBS J 289:7891",
  'version': 'epub 2021-10-30; issue 2022-12; DOI 10.1111/febs.16234; PMC9016100',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9016100/',
  'quote': ['the adder model does not readily reveal a molecular basis for cell size control nor any connections '
            'between cell size and growth physiology.',
            'The invariance of initiation mass with elongation rate and birth size is consistent with the threshold '
            'initiation model, but its mechanistic origin remains unknown.'],
  'raw_file': 'frontier/life/F2_febsj2022_resource_allocation.txt',
  'note': 'is the adder mechanistic; origin of the invariant initiation mass',
  'id': 'life:2'},
 {'domain': 'F2',
  'kind': 'PROPOSAL',
  'source': "Serbanescu, Ojkic, Banerjee, 'Cellular resource allocation strategies for cell size and shape control in "
            "bacteria', FEBS J 289:7891",
  'version': 'epub 2021-10-30; issue 2022-12; DOI 10.1111/febs.16234; PMC9016100',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9016100/',
  'quote': ['In this model, cell divides after a fixed time interval (C + D period) since the initiation of chromosome '
            'replication.',
            'Recently, a replication double adder model has been proposed [72], where cells grow by a fixed volume per '
            'replication origin between two consecutive initiation cycles, and cell divides after elongation by a '
            'constant volume per origin of replication.',
            'the chromosome replication initiation and cellular division have been shown to be controlled '
            'independently',
            'a recent study has identified the protein FtsZ as the key size sensor molecule that reaches a threshold '
            'abundance at the time of cell division'],
  'raw_file': 'frontier/life/F2_febsj2022_resource_allocation.txt',
  'note': 'replication-initiation-centric (C+D timer), double adder, independent adders, threshold accumulation (FtsZ)',
  'id': 'life:3'},
 {'domain': 'F2',
  'kind': 'BOTTLENECK',
  'source': "Herrick, 'DNA/Cell Mass Homeostasis: Coordinating DNA Replication and Cell Size with Central Carbon "
            "Metabolism During Bacterial Growth', Genes 17:695",
  'version': 'epub 2026-06-15; DOI 10.3390/genes17060695; PMC13300287',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC13300287/',
  'quote': ['Why and how cell size varies with DNA content remains an unresolved question of both evolutionary and '
            'physiological interest.',
            'might have the yet-unrealized potential to explain, at least in part, the long-standing mystery of the '
            'multiple mechanisms that determine the initiation mass in bacteria.'],
  'raw_file': 'frontier/life/F2_genes2026_dna_mass.txt',
  'note': 'what sets the initiation mass',
  'id': 'life:4'},
 {'domain': 'F2',
  'kind': 'PROPOSAL',
  'source': "Herrick, 'DNA/Cell Mass Homeostasis: Coordinating DNA Replication and Cell Size with Central Carbon "
            "Metabolism During Bacterial Growth', Genes 17:695",
  'version': 'epub 2026-06-15; DOI 10.3390/genes17060695; PMC13300287',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC13300287/',
  'quote': ['the hypothesis that DnaA and RNR form a homeostatic pair that sets the Mi',
            'DnaA, it seems, serves mainly as a licensing factor at oriC (similar to the eukaryote Origin Recognition '
            'Complex) and not as a timer in initiation control.',
            'This, however, remains an open question.'],
  'raw_file': 'frontier/life/F2_genes2026_dna_mass.txt',
  'note': 'DnaA-RNR homeostatic pair (single-author review; the author flags it as open)',
  'id': 'life:5'},
 {'domain': 'F2',
  'kind': 'PROPOSAL',
  'source': "Torres, Carrasco, Ayora, Alonso, 'Mechanisms of chromosomal DNA replication in Escherichia coli and "
            "Bacillus subtilis', FEMS Microbiol Rev 50:fuag021",
  'version': 'epub 2026-05-14; DOI 10.1093/femsre/fuag021; PMC13220808',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC13220808/',
  'quote': ['which initiate replication at a fixed cell mass'],
  'raw_file': 'frontier/life/F2_femsmr2026_replication.txt',
  'note': 'the standard framing: initiation at a fixed cell mass (not a fixed phase)',
  'id': 'life:6'},
 {'domain': 'F2',
  'kind': 'BOTTLENECK',
  'source': "Witz, van Nimwegen, Julou, 'Initiation of chromosome replication controls both division and replication "
            "cycles in E. coli through a double-adder mechanism', eLife 8:e48063 (research article; targeted search)",
  'version': 'pub 2019-11-11; DOI 10.7554/eLife.48063; PMC6890467',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6890467/',
  'quote': ['It remains unclear how bacteria such as Escherichia coli tightly coordinate those two cycles across a '
            'wide range of growth conditions.'],
  'raw_file': 'frontier/life/F2_elife2019_double_adder.txt',
  'note': '2019 research article (older than the window); the coupling question as posed',
  'id': 'life:7'},
 {'domain': 'F2',
  'kind': 'PROPOSAL',
  'source': "Witz, van Nimwegen, Julou, 'Initiation of chromosome replication controls both division and replication "
            "cycles in E. coli through a double-adder mechanism', eLife 8:e48063 (research article; targeted search)",
  'version': 'pub 2019-11-11; DOI 10.7554/eLife.48063; PMC6890467',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6890467/',
  'quote': ['the cell cycle is driven from one initiation event to the next rather than from birth to division and is '
            'controlled by two adder mechanisms: the added volume since the last initiation event determines the '
            'timing of both the next division and replication initiation events.'],
  'raw_file': 'frontier/life/F2_elife2019_double_adder.txt',
  'note': 'initiation-to-initiation double adder',
  'id': 'life:8'},
 {'domain': 'F2',
  'kind': 'DIRECTION',
  'source': "Zhang, Fei, Dunkel, 'Nonlinear memory in cell-division dynamics across species', PNAS 122:e2417416122 "
            '(research article; targeted search)',
  'version': 'pub 2025-09-03; DOI 10.1073/pnas.2417416122; PMC12435308',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12435308/',
  'quote': ['However, despite such major progress, there still exist fundamental open questions regarding the '
            'nonlinear and multigenerational memory (28) effects that are not captured by some of the currently '
            'prevailing standard models of cell-size homeostasis.',
            'one with two-generation memory λt=λ(st,st∗,st∗∗), where the current size st, the mother size st∗, and the '
            'grandmother size st∗∗ represent progressively higher orders of memory in the cell-division rate λ',
            'Perhaps surprisingly, adding memory of the grandmother size st∗∗ does not further improve the BIC score '
            'of the model'],
  'raw_file': 'frontier/life/F2_pnas2025_nonlinear_memory.txt',
  'note': 'DIRECTION-NAMED (lag-2 / grandmother memory): named and tested; for E. coli the grandmother term did not '
          'improve BIC',
  'id': 'life:9'},
 {'domain': 'F2',
  'kind': 'DIRECTION',
  'source': "ElGamel, Vashistha, Salman, Mugler, 'Multigenerational memory in bacterial size control', "
            'arXiv:2206.05340 (Phys Rev E 108, L032401) (research letter; targeted search)',
  'version': 'arXiv v2, 2023-05-24 (v1 2022-06-10)',
  'url': 'https://arxiv.org/pdf/2206.05340v2',
  'quote': ['However, recent evidence from comparing sister lineages suggests that correlations in size fluctuations '
            'can persist for many generations.',
            'In particular, it is still unclear whether deviations from the average size dissipate over one or many '
            'generations',
            'which accounts for the generational dependence of the phase'],
  'raw_file': 'frontier/life/F2_arxiv2206.05340v2.txt',
  'note': "DIRECTION-NAMED (multigenerational memory; phase depends on previous generation's phase = lag-2 structure "
          'in birth size)',
  'id': 'life:10'},
 {'domain': 'F2',
  'kind': 'DIRECTION',
  'source': "ElGamel, Vashistha, Salman, Mugler, 'Multigenerational memory in bacterial size control', "
            'arXiv:2206.05340 (Phys Rev E 108, L032401) (research letter; targeted search)',
  'version': 'arXiv v2, 2023-05-24 (v1 2022-06-10)',
  'url': 'https://arxiv.org/pdf/2206.05340v2',
  'quote': ['consider a cell born with size xn that grows exponentially for an elapsed phase ϕn, the product of the '
            'growth rate and cell cycle time'],
  'raw_file': 'frontier/life/F2_arxiv2206.05340v2.txt',
  'note': "PARTIAL: a growth 'phase' (ln-size advanced) is used for division control; initiation at a fixed phase of "
          'the growth-division cycle not found named in fetched texts',
  'id': 'life:11'},
 {'domain': 'F7',
  'kind': 'BOTTLENECK',
  'source': "Berry, Guhle, Davis, 'Active forgetting and neuropsychiatric diseases', Mol Psychiatry 29:2810",
  'version': '2024-09; DOI 10.1038/s41380-024-02521-9; PMC11420092',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11420092/',
  'quote': ['Mechanistic studies of forgetting began only about one decade ago, so there remains much more to be '
            'discovered.',
            'The underlying mechanisms of sleep-dependent memory enhancement are still being defined and are diverse.'],
  'raw_file': 'frontier/life/F7_molpsych2024_active_forgetting.txt',
  'note': 'mechanism of forgetting; sleep',
  'id': 'life:12'},
 {'domain': 'F7',
  'kind': 'PROPOSAL',
  'source': "Berry, Guhle, Davis, 'Active forgetting and neuropsychiatric diseases', Mol Psychiatry 29:2810",
  'version': '2024-09; DOI 10.1038/s41380-024-02521-9; PMC11420092',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11420092/',
  'quote': ['Thus, DAn driven active forgetting mechanisms provide a biological explanation for interference-based '
            'forgetting.',
            'Another possible mechanism, not mutually exclusive with the first, is that sleep and rest inhibit active '
            'forgetting of labile memory, potentially protecting nascent memory traces from interference so they can '
            'be consolidated [113, 124].',
            'First, sleep leads to synaptic downscaling that broadly reduces synapse strength and thus theoretically '
            'could degrade engrams [127–129].'],
  'raw_file': 'frontier/life/F7_molpsych2024_active_forgetting.txt',
  'note': 'active (dopamine/Rac1) forgetting; sleep protects from interference; synaptic downscaling',
  'id': 'life:13'},
 {'domain': 'F7',
  'kind': 'BOTTLENECK',
  'source': "de Snoo, Frankland, 'Neurobiological mechanisms of forgetting across timescales', Curr Opin Neurobiol "
            '90:102972',
  'version': 'epub 2025-01-31; DOI 10.1016/j.conb.2025.102972; PMID 39892316 (abstract only)',
  'url': 'https://pubmed.ncbi.nlm.nih.gov/39892316/',
  'quote': ['However, changes in accessibility emerge on vastly different timescales.'],
  'raw_file': 'frontier/life/F7_conb2025_forgetting_timescales_abs.txt',
  'note': 'forgetting across timescales',
  'id': 'life:14'},
 {'domain': 'F7',
  'kind': 'PROPOSAL',
  'source': "de Snoo, Frankland, 'Neurobiological mechanisms of forgetting across timescales', Curr Opin Neurobiol "
            '90:102972',
  'version': 'epub 2025-01-31; DOI 10.1016/j.conb.2025.102972; PMID 39892316 (abstract only)',
  'url': 'https://pubmed.ncbi.nlm.nih.gov/39892316/',
  'quote': ['Viewed this way, forgetting encompasses a family of plasticity mechanisms that modulate engram '
            'accessibility, perhaps in order to prioritize those memories that are most timely or relevant to the '
            'situation at hand.'],
  'raw_file': 'frontier/life/F7_conb2025_forgetting_timescales_abs.txt',
  'note': 'engram accessibility',
  'id': 'life:15'},
 {'domain': 'F7',
  'kind': 'PROPOSAL',
  'source': "Autore, Drew, Ryan, 'The cost of remembering: engram competition as a flexible mechanism of forgetting', "
            'Trends Neurosci 48:728-738',
  'version': 'epub 2025-08-14; DOI 10.1016/j.tins.2025.07.011; PMID 40813160 (abstract only)',
  'url': 'https://pubmed.ncbi.nlm.nih.gov/40813160/',
  'quote': ['One explanation for the forgetting of particular memories is active competition between memory engrams '
            'for expression in the brain.'],
  'raw_file': 'frontier/life/F7_tins2025_engram_competition_abs.txt',
  'note': 'engram competition (an interference account)',
  'id': 'life:16'},
 {'domain': 'F7',
  'kind': 'BOTTLENECK',
  'source': "Brodt, Inostroza, Niethard, Born, 'Sleep - A brain-state serving systems memory consolidation', Neuron "
            '111:1050-1075',
  'version': '2023-04-05; DOI 10.1016/j.neuron.2023.03.005; PMID 37023710 (abstract only)',
  'url': 'https://pubmed.ncbi.nlm.nih.gov/37023710/',
  'quote': ['Although long-term memory consolidation is supported by sleep, it is unclear how it differs from that '
            'during wakefulness.'],
  'raw_file': 'frontier/life/F7_neuron2023_sleep_consolidation_abs.txt',
  'note': 'sleep vs wake consolidation',
  'id': 'life:17'},
 {'domain': 'F7',
  'kind': 'PROPOSAL',
  'source': "Brodt, Inostroza, Niethard, Born, 'Sleep - A brain-state serving systems memory consolidation', Neuron "
            '111:1050-1075',
  'version': '2023-04-05; DOI 10.1016/j.neuron.2023.03.005; PMID 37023710 (abstract only)',
  'url': 'https://pubmed.ncbi.nlm.nih.gov/37023710/',
  'quote': ['identifies the repeated replay of neuronal firing patterns as a basic mechanism triggering consolidation '
            'during sleep and wakefulness.'],
  'raw_file': 'frontier/life/F7_neuron2023_sleep_consolidation_abs.txt',
  'note': 'replay',
  'id': 'life:18'},
 {'domain': 'F7',
  'kind': 'DIRECTION',
  'source': "Georgiou, Katkov, Tsodyks, 'Retroactive interference model of forgetting', J Math Neurosci 11:4 (research "
            'article; targeted search)',
  'version': 'epub 2021-01-23; DOI 10.1186/s13408-021-00102-6; PMC7826326',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7826326/',
  'quote': ['One such mechanism proposed in previous studies is retrograde interference, stating that a memory can be '
            'erased due to subsequently acquired memories.',
            'For simplicity, we assume that memories are acquired at a constant rate (one new memory per time step).',
            'consider a memory acquired at time 0 followed by t other memories.'],
  'raw_file': 'frontier/life/F7_jmathneuro2021_retroactive_interference.txt',
  'note': 'DIRECTION-NAMED (forgetting counted in interfering events, i.e. an event clock)',
  'id': 'life:19'},
 {'domain': 'F7',
  'kind': 'DIRECTION',
  'source': "Georgiou, Katkov, Tsodyks, 'Retroactive interference model of forgetting', J Math Neurosci 11:4 (research "
            'article; targeted search)',
  'version': 'epub 2021-01-23; DOI 10.1186/s13408-021-00102-6; PMC7826326',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7826326/',
  'quote': ['Therefore the probability that a unit will be forgotten at the next time step is a strictly decaying '
            'function of its age'],
  'raw_file': 'frontier/life/F7_jmathneuro2021_retroactive_interference.txt',
  'note': 'DIRECTION-NAMED (forgetting rate decreasing with age from interference; here via valence selection, not '
          'age-keyed vulnerability)',
  'id': 'life:20'},
 {'domain': 'F7',
  'kind': 'DIRECTION',
  'source': "Wixted, 'On Common Ground: Jost's (1897) Law of Forgetting and Ribot's (1881) Law of Retrograde Amnesia', "
            'Psychol Rev 111(4):864-879 (targeted search; older than the window)',
  'version': '2004; DOI 10.1037/0033-295X.111.4.864; author PDF',
  'url': 'http://wixtedlab.ucsd.edu/publications/wixted/Jost_Law.pdf',
  'quote': ['One reason why memories might decay less rapidly with age is because they become less vulnerable to the '
            'forces of retroactive interference (RI) as a result of consolidation.',
            'If it is true that memory traces become less vulnerable to the effects of subsequent memory formation as '
            'a result of the process of consolidation, then forgetting functions would be expected to exhibit an '
            'ever-decreasing rate of decay'],
  'raw_file': 'frontier/life/F7_wixted2004_jost.txt',
  'note': "DIRECTION-NAMED (Jost's law from interference whose force decays with the trace's age)",
  'id': 'life:21'},
 {'domain': 'F7',
  'kind': 'DIRECTION',
  'source': "Ray Barman, Starenky, Bodnar, Narasimhan, Gopinath, 'The Geometry of Forgetting', arXiv:2604.06222 "
            '(preprint; targeted search)',
  'version': 'arXiv v1, 2026-03-27',
  'url': 'https://arxiv.org/html/2604.06222',
  'quote': ['Decay theories say memory traces fade with time.',
            'The critical test: does the forgetting exponent depend on the decay function or on the number of '
            'competing memories?',
            'Power-law forgetting ( , human ) arises from interference among competing memories, not from decay.'],
  'raw_file': 'frontier/life/F7_arxiv2604.06222v1.txt',
  'note': "DIRECTION-NAMED ('which clock': time-based decay vs number of competitors); math symbols stripped in saved "
          'text',
  'id': 'life:22'},
 {'domain': 'F7',
  'kind': 'DIRECTION',
  'source': "Georgiou, Katkov, Tsodyks, 'Retroactive interference model of forgetting', J Math Neurosci 11:4 (research "
            'article; targeted search)',
  'version': 'epub 2021-01-23; DOI 10.1186/s13408-021-00102-6; PMC7826326',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7826326/',
  'quote': ['Mechanisms that are usually considered in relation to forgetting are passive decay of memories, '
            'interference, and consolidation'],
  'raw_file': 'frontier/life/F7_jmathneuro2021_retroactive_interference.txt',
  'note': 'DIRECTION-NAMED (decay vs interference framing)',
  'id': 'life:23'},
 {'domain': 'F12',
  'kind': 'BOTTLENECK',
  'source': "Boivin, Boudreau, Kosmadopoulos, 'Disturbance of the Circadian System in Shift Work and Its Health "
            "Impact', J Biol Rhythms 37:3",
  'version': 'epub 2021-12-30; issue 2022-02; DOI 10.1177/07487304211064218; PMC8832572',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8832572/',
  'quote': ['Simulated night-shift experiments and field-based studies with shift workers both indicate that the '
            'circadian system is resistant to adaptation from a day- to a night-oriented schedule, as determined by a '
            'lack of substantial phase shifts over multiple days in centrally controlled rhythms, such as those of '
            'melatonin and cortisol.',
            'The size effects, in real working environments, of specific factors mediating the health impacts of '
            'atypical shifts remain unclear.'],
  'raw_file': 'frontier/life/F12_jbr2022_shiftwork.txt',
  'note': 'entrainment resistance in shift work; internal desynchrony',
  'id': 'life:24'},
 {'domain': 'F12',
  'kind': 'PROPOSAL',
  'source': "Boivin, Boudreau, Kosmadopoulos, 'Disturbance of the Circadian System in Shift Work and Its Health "
            "Impact', J Biol Rhythms 37:3",
  'version': 'epub 2021-12-30; issue 2022-02; DOI 10.1177/07487304211064218; PMC8832572',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8832572/',
  'quote': ['Light attenuation with goggles or sunglasses during the morning commute after night shifts has been shown '
            'to facilitate phase shifting',
            'Three cycles of 8-h bright light exposure at night induced significant phase delays of ~7 to 9 h for '
            'central and peripheral markers'],
  'raw_file': 'frontier/life/F12_jbr2022_shiftwork.txt',
  'note': 'light scheduling',
  'id': 'life:25'},
 {'domain': 'F12',
  'kind': 'BOTTLENECK',
  'source': "Easton, Gupta, Vincent, Ferguson, 'Move the night way: how can physical activity facilitate adaptation to "
            "shift work?', Commun Biol 7:259",
  'version': 'epub 2024-03-02; DOI 10.1038/s42003-024-05962-8; PMC10908783',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10908783/',
  'quote': ['However, evidence of real-world circadian adaptation is found primarily in occupations where light '
            'exposure is readily controlled.',
            'Despite this, non-photic adaptation to shift work remains under researched.'],
  'raw_file': 'frontier/life/F12_commbio2024_shiftwork_activity.txt',
  'note': '',
  'id': 'life:26'},
 {'domain': 'F12',
  'kind': 'PROPOSAL',
  'source': "Easton, Gupta, Vincent, Ferguson, 'Move the night way: how can physical activity facilitate adaptation to "
            "shift work?', Commun Biol 7:259",
  'version': 'epub 2024-03-02; DOI 10.1038/s42003-024-05962-8; PMC10908783',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10908783/',
  'quote': ['We also propose that physical activity might be an accessible and cost-effective countermeasure that '
            'could influence multiple markers of adaptation across three timeframes (Within Shift, Within Block, '
            'Within Work-span).',
            'Light exposure during the early morning hours of a night shift will naturally advance circadian '
            'rhythms64, thereby working against the desired delay.'],
  'raw_file': 'frontier/life/F12_commbio2024_shiftwork_activity.txt',
  'note': 'exercise as zeitgeber; light timing by advance/delay direction',
  'id': 'life:27'},
 {'domain': 'F12',
  'kind': 'BOTTLENECK',
  'source': "Lee, Field, Sehgal, 'Circadian Rhythms, Disease and Chronotherapy', J Biol Rhythms 36:503",
  'version': 'epub 2021-09-22; issue 2021-12; DOI 10.1177/07487304211044301; PMC9197224',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9197224/',
  'quote': ['(3) How generalizable is the application of circadian medicine? Individual variability in circadian '
            'rhythms, caused by genetics or environmental factors (e.g. chronotype, lifestyle, illness, age), could '
            'have significant effects on treatment, suggesting chronotherapy may need to be individualized for '
            'patients.'],
  'raw_file': 'frontier/life/F12_jbr2021_chronotherapy.txt',
  'note': 'individual internal time',
  'id': 'life:28'},
 {'domain': 'F12',
  'kind': 'PROPOSAL',
  'source': "Lee, Field, Sehgal, 'Circadian Rhythms, Disease and Chronotherapy', J Biol Rhythms 36:503",
  'version': 'epub 2021-09-22; issue 2021-12; DOI 10.1177/07487304211044301; PMC9197224',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9197224/',
  'quote': ['(1) Clocks as targets; non-pharmaceutical or pharmacological interventions to manipulate circadian '
            'rhythms or circadian components; (2) Clocks as modulators: timing of medicine to the endogenous rhythm '
            'established by clocks in order to improve efficacy and reduce side effects.'],
  'raw_file': 'frontier/life/F12_jbr2021_chronotherapy.txt',
  'note': '',
  'id': 'life:29'},
 {'domain': 'F12',
  'kind': 'BOTTLENECK',
  'source': "Gong, Ren, Xiong, Wu et al., 'Toward adaptive therapeutic timing: integration of mechanistic pharmacology "
            "and artificial intelligence in precision dosing', Front Pharmacol 17:1890846",
  'version': 'pub 2026-09-03; DOI 10.3389/fphar.2026.1890846; PMC13582453',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC13582453/',
  'quote': ['Strong circadian biomarkers such as melatonin and cortisol can also require invasive or specialized '
            'testing, which limits routine use.',
            'These shortcomings make it harder for models to estimate the circadian state reliably in everyday care.'],
  'raw_file': 'frontier/life/F12_frontpharm2026_adaptive_timing.txt',
  'note': 'estimating internal phase',
  'id': 'life:30'},
 {'domain': 'F12',
  'kind': 'PROPOSAL',
  'source': "Gong, Ren, Xiong, Wu et al., 'Toward adaptive therapeutic timing: integration of mechanistic pharmacology "
            "and artificial intelligence in precision dosing', Front Pharmacol 17:1890846",
  'version': 'pub 2026-09-03; DOI 10.3389/fphar.2026.1890846; PMC13582453',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC13582453/',
  'quote': ['AI-enabled chronotherapy is moving toward closed-loop, sensor-based, and adaptive treatment.'],
  'raw_file': 'frontier/life/F12_frontpharm2026_adaptive_timing.txt',
  'note': '',
  'id': 'life:31'},
 {'domain': 'F12',
  'kind': 'DIRECTION',
  'source': "Uriu, Tei, 'Complementary phase responses via functional differentiation of dual negative feedback "
            "loops', PLoS Comput Biol 17:e1008774 (research article; targeted search)",
  'version': '2021; DOI 10.1371/journal.pcbi.1008774; PMC7971863',
  'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7971863/',
  'quote': ['To quantify the shape of a PRC, we measure the unsigned areas of its advance (Δϕ ≥ 0) and delay (Δϕ < 0) '
            'zones, which we refer to A and D (A ≥ 0, D ≥ 0), respectively.',
            'the ratio of light-induced transcription rates between Per1 and Per2 determines the proportion of phase '
            'advance and delay zones in a PRC, and thereby determines the entrainability of a circadian clock to a '
            '24-hour LD cycle.',
            'Thus, as our simulations suggested, the administration of such compounds may adjust the phase of '
            'entrainment to be more desirable for daily life.'],
  'raw_file': 'frontier/life/F12_ploscb2021_complementary_prc.txt',
  'note': 'DIRECTION-NAMED (advance/delay PRC areas set entrainment and its phase)',
  'id': 'life:32'},
 {'domain': 'F3',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Gozzi, Perra, Vespignani, 'Comparative evaluation of behavioral epidemic models using COVID-19 data', "
            'PNAS 122(24) e2421993122 (2025), doi:10.1073/pnas.2421993122, PMC12184516',
  'version': 'published 2025-06-17 (received 2024-10-24, accepted 2025-05-08); full text via Europe PMC fullTextXML',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12184516/fullTextXML',
  'fetch_status': '200 (the PMC HTML page https://pmc.ncbi.nlm.nih.gov/articles/PMC12184516/ returned a reCAPTCHA '
                  'page, not used)',
  'quote': ['Characterizing the feedback linking human behavior and the transmission of infectious diseases (i.e., '
            'behavioral changes) remains a significant challenge in computational and mathematical epidemiology.'],
  'raw_file': 'frontier/cx/F3_pnas_comparative_behavioral.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:0'},
 {'domain': 'F3',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Gozzi, Perra, Vespignani, 'Comparative evaluation of behavioral epidemic models using COVID-19 data', "
            'PNAS 122(24) e2421993122 (2025), doi:10.1073/pnas.2421993122, PMC12184516',
  'version': 'published 2025-06-17 (received 2024-10-24, accepted 2025-05-08); full text via Europe PMC fullTextXML',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12184516/fullTextXML',
  'fetch_status': '200 (the PMC HTML page https://pmc.ncbi.nlm.nih.gov/articles/PMC12184516/ returned a reCAPTCHA '
                  'page, not used)',
  'quote': ['Existing behavioral epidemic models often lack real-world data calibration and cross-model performance '
            'evaluation in both retrospective analysis and forecasting.'],
  'raw_file': 'frontier/cx/F3_pnas_comparative_behavioral.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:1'},
 {'domain': 'F3',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Gozzi, Perra, Vespignani, 'Comparative evaluation of behavioral epidemic models using COVID-19 data', "
            'PNAS 122(24) e2421993122 (2025), doi:10.1073/pnas.2421993122, PMC12184516',
  'version': 'published 2025-06-17 (received 2024-10-24, accepted 2025-05-08); full text via Europe PMC fullTextXML',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12184516/fullTextXML',
  'fetch_status': '200 (the PMC HTML page https://pmc.ncbi.nlm.nih.gov/articles/PMC12184516/ returned a reCAPTCHA '
                  'page, not used)',
  'quote': ['Furthermore, translating mobility changes into contact reductions remains an open challenge.'],
  'raw_file': 'frontier/cx/F3_pnas_comparative_behavioral.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:2'},
 {'domain': 'F3',
  'kind': 'PROPOSAL',
  'tag': 'PROPOSAL',
  'source': "Gozzi, Perra, Vespignani, 'Comparative evaluation of behavioral epidemic models using COVID-19 data', "
            'PNAS 122(24) e2421993122 (2025), doi:10.1073/pnas.2421993122, PMC12184516',
  'version': 'published 2025-06-17 (received 2024-10-24, accepted 2025-05-08); full text via Europe PMC fullTextXML',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12184516/fullTextXML',
  'fetch_status': '200 (the PMC HTML page https://pmc.ncbi.nlm.nih.gov/articles/PMC12184516/ returned a reCAPTCHA '
                  'page, not used)',
  'quote': ['Specifically, we investigate three mechanistic models: i) the Data-Driven Behavioral Model exemplifies '
            'data-driven approaches, leveraging mobility data to estimate effective changes in contact patterns; ii) '
            'the Compartmental Behavioral Feedback Model simulates the feedback loop by explicitly representing '
            'different behavioral classes within the population; iii) the Effective Force of Infection Behavioral '
            'Feedback Model employs an effective nonlinear forcing to adjust the infection rate based on the '
            'epidemic’s progression and the resulting behavioral changes.'],
  'raw_file': 'frontier/cx/F3_pnas_comparative_behavioral.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:3'},
 {'domain': 'F3',
  'kind': 'PROPOSAL',
  'tag': 'PROPOSAL',
  'source': "Gozzi, Perra, Vespignani, 'Comparative evaluation of behavioral epidemic models using COVID-19 data', "
            'PNAS 122(24) e2421993122 (2025), doi:10.1073/pnas.2421993122, PMC12184516',
  'version': 'published 2025-06-17 (received 2024-10-24, accepted 2025-05-08); full text via Europe PMC fullTextXML',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12184516/fullTextXML',
  'fetch_status': '200 (the PMC HTML page https://pmc.ncbi.nlm.nih.gov/articles/PMC12184516/ returned a reCAPTCHA '
                  'page, not used)',
  'quote': ['our findings show that approaches explicitly modeling behavioral feedback mechanisms often outperform '
            'data-driven approaches, even when considering data quality and the increased numbers of free parameters '
            'of these models.'],
  'raw_file': 'frontier/cx/F3_pnas_comparative_behavioral.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:4'},
 {'domain': 'F3',
  'kind': 'PROPOSAL',
  'tag': 'PROPOSAL',
  'source': "Gozzi, Perra, Vespignani, 'Comparative evaluation of behavioral epidemic models using COVID-19 data', "
            'PNAS 122(24) e2421993122 (2025), doi:10.1073/pnas.2421993122, PMC12184516',
  'version': 'published 2025-06-17 (received 2024-10-24, accepted 2025-05-08); full text via Europe PMC fullTextXML',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12184516/fullTextXML',
  'fetch_status': '200 (the PMC HTML page https://pmc.ncbi.nlm.nih.gov/articles/PMC12184516/ returned a reCAPTCHA '
                  'page, not used)',
  'quote': ['f(Drep) is a nonlinear function of the number of reported deaths that modulates the force of infection in '
            'the Effective Force of Infection Behavioral Feedback model.'],
  'raw_file': 'frontier/cx/F3_pnas_comparative_behavioral.txt',
  'note': 'The feedback here is on reported deaths (with reporting delay compartments), not on an explicitly weighted '
          'memory of prevalence.',
  'verified_substring': True,
  'id': 'cx:5'},
 {'domain': 'F3',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Diekmann, Inaba, Thieme, 'Mathematical epidemiology of infectious diseases: an ongoing challenge', "
            'arXiv:2505.01621 (perspective with a Challenges/Open Problems section)',
  'version': 'arXiv v2, 2025-08-05 (latest on the day)',
  'url': 'https://arxiv.org/pdf/2505.01621',
  'fetch_status': '200',
  'quote': ['Human behaviour adapts to perceived risk, either spontaneously or on the instruction of the govern- ment '
            '[43].'],
  'raw_file': 'frontier/cx/F3_math_epi_challenge.txt',
  'note': "Opens Section 5 'Challenges / Open Problems'; PDF hyphenation kept.",
  'verified_substring': True,
  'id': 'cx:6'},
 {'domain': 'F3',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Diekmann, Inaba, Thieme, 'Mathematical epidemiology of infectious diseases: an ongoing challenge', "
            'arXiv:2505.01621 (perspective with a Challenges/Open Problems section)',
  'version': 'arXiv v2, 2025-08-05 (latest on the day)',
  'url': 'https://arxiv.org/pdf/2505.01621',
  'fetch_status': '200',
  'quote': ['Even though it is clear that outbreak dynamics is influenced by all of these mech- anisms, it is '
            'virtually impossible to quantitatively disentangle their effect on the basis of data.'],
  'raw_file': 'frontier/cx/F3_math_epi_challenge.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:7'},
 {'domain': 'F3',
  'kind': 'PROPOSAL',
  'tag': 'PROPOSAL',
  'source': "Diekmann, Inaba, Thieme, 'Mathematical epidemiology of infectious diseases: an ongoing challenge', "
            'arXiv:2505.01621 (perspective with a Challenges/Open Problems section)',
  'version': 'arXiv v2, 2025-08-05 (latest on the day)',
  'url': 'https://arxiv.org/pdf/2505.01621',
  'fetch_status': '200',
  'quote': ['By allowing this parameter to vary dynamically in response (possibly with some delay) to the prevail- ing '
            'incidence or prevalence, one obtains a simple representation of contact reduction triggered by '
            'awareness.'],
  'raw_file': 'frontier/cx/F3_math_epi_challenge.txt',
  'note': 'Names delayed response to prevalence (a delay, not a geometric memory).',
  'verified_substring': True,
  'id': 'cx:8'},
 {'domain': 'F3',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Diekmann, Inaba, Thieme, 'Mathematical epidemiology of infectious diseases: an ongoing challenge', "
            'arXiv:2505.01621 (perspective with a Challenges/Open Problems section)',
  'version': 'arXiv v2, 2025-08-05 (latest on the day)',
  'url': 'https://arxiv.org/pdf/2505.01621',
  'fetch_status': '200',
  'quote': ['It would be an interesting challenge to incorporate behavioural feedback in such more complicated '
            'models.'],
  'raw_file': 'frontier/cx/F3_math_epi_challenge.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:9'},
 {'domain': 'F3',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Mao, Deardon, Deeth, 'Memory mechanisms for behavioural change in Bayesian individual-level spatial "
            "epidemic models', Infectious Disease Modelling (2026), doi:10.1016/j.idm.2026.05.008, PMC13276345",
  'version': '2026 (accepted 2026-05; CC BY); full text via Europe PMC fullTextXML',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13276345/fullTextXML',
  'fetch_status': '200 (PMC HTML page returned a reCAPTCHA page, not used)',
  'quote': ['While recently developed behavioural change epidemic models attempt to acknowledge such dynamics, the '
            'role of memory in shaping perceived risk has been treated in an ad hoc fashion.'],
  'raw_file': 'frontier/cx/F3_memory_mechanisms.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:10'},
 {'domain': 'F3',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Mao, Deardon, Deeth, 'Memory mechanisms for behavioural change in Bayesian individual-level spatial "
            "epidemic models', Infectious Disease Modelling (2026), doi:10.1016/j.idm.2026.05.008, PMC13276345",
  'version': '2026 (accepted 2026-05; CC BY); full text via Europe PMC fullTextXML',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13276345/fullTextXML',
  'fetch_status': '200 (PMC HTML page returned a reCAPTCHA page, not used)',
  'quote': ['Many existing approaches either base individual responses solely on current information, without '
            'explicitly considering accumulated historical knowledge, or rely on ad hoc assumptions about how memory '
            'shapes behaviour, thereby imposing a rigid evolution of responses.'],
  'raw_file': 'frontier/cx/F3_memory_mechanisms.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:11'},
 {'domain': 'F3',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Mao, Deardon, Deeth, 'Memory mechanisms for behavioural change in Bayesian individual-level spatial "
            "epidemic models', Infectious Disease Modelling (2026), doi:10.1016/j.idm.2026.05.008, PMC13276345",
  'version': '2026 (accepted 2026-05; CC BY); full text via Europe PMC fullTextXML',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13276345/fullTextXML',
  'fetch_status': '200 (PMC HTML page returned a reCAPTCHA page, not used)',
  'quote': ['In this study, we propose four alternative memory mechanisms and incorporate them into the BC-ILM '
            'framework.'],
  'raw_file': 'frontier/cx/F3_memory_mechanisms.txt',
  'note': 'Memoryless, sliding window, power-law decay and exponential decay.',
  'verified_substring': True,
  'id': 'cx:12'},
 {'domain': 'F3',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Mao, Deardon, Deeth, 'Memory mechanisms for behavioural change in Bayesian individual-level spatial "
            "epidemic models', Infectious Disease Modelling (2026), doi:10.1016/j.idm.2026.05.008, PMC13276345",
  'version': '2026 (accepted 2026-05; CC BY); full text via Europe PMC fullTextXML',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13276345/fullTextXML',
  'fetch_status': '200 (PMC HTML page returned a reCAPTCHA page, not used)',
  'quote': ['Similarly, we introduce an exponential decay memory model, in which past prevalence values are discounted '
            'exponentially over time:'],
  'raw_file': 'frontier/cx/F3_memory_mechanisms.txt',
  'note': 'The geometrically weighted memory of prevalence is named and fitted.',
  'verified_substring': True,
  'id': 'cx:13'},
 {'domain': 'F3',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Mao, Deardon, Deeth, 'Memory mechanisms for behavioural change in Bayesian individual-level spatial "
            "epidemic models', Infectious Disease Modelling (2026), doi:10.1016/j.idm.2026.05.008, PMC13276345",
  'version': '2026 (accepted 2026-05; CC BY); full text via Europe PMC fullTextXML',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13276345/fullTextXML',
  'fetch_status': '200 (PMC HTML page returned a reCAPTCHA page, not used)',
  'quote': ['Across all three MEBC-ILMs, we observe a consistent underestimation of memory strength.'],
  'raw_file': 'frontier/cx/F3_memory_mechanisms.txt',
  'note': 'Identifiability of the memory parameter is itself an open problem.',
  'verified_substring': True,
  'id': 'cx:14'},
 {'domain': 'F3',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "'Behavior-induced oscillations in epidemic outbreaks with distributed memory: Beyond the linear chain "
            "trick using numerical methods', Mathematical Biosciences and Engineering 23(1):76-96 (2026), "
            'doi:10.3934/mbe.2026004 (targeted direction search)',
  'version': 'published 2025-11-28 (received 2025-07-29); abstract page',
  'url': 'https://www.aimspress.com/article/doi/10.3934/mbe.2026004',
  'fetch_status': '200',
  'quote': ['In line with the information index approach, we supposed that individuals react to past information '
            'according to a memory kernel that is continuously distributed in the past.'],
  'raw_file': 'frontier/cx/F3_dist_memory_oscillations.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:15'},
 {'domain': 'F3',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "'Behavior-induced oscillations in epidemic outbreaks with distributed memory: Beyond the linear chain "
            "trick using numerical methods', Mathematical Biosciences and Engineering 23(1):76-96 (2026), "
            'doi:10.3934/mbe.2026004 (targeted direction search)',
  'version': 'published 2025-11-28 (received 2025-07-29); abstract page',
  'url': 'https://www.aimspress.com/article/doi/10.3934/mbe.2026004',
  'fetch_status': '200',
  'quote': ['In agreement with previous studies, we showed that behavior adaptation alone can cause sustained waves of '
            'infections even in an outbreak scenario, and notably in the absence of other processes like demographic '
            'turnover, seasonality, or waning immunity.'],
  'raw_file': 'frontier/cx/F3_dist_memory_oscillations.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:16'},
 {'domain': 'F3',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "'Behavior-induced oscillations in epidemic outbreaks with distributed memory: Beyond the linear chain "
            "trick using numerical methods', Mathematical Biosciences and Engineering 23(1):76-96 (2026), "
            'doi:10.3934/mbe.2026004 (targeted direction search)',
  'version': 'published 2025-11-28 (received 2025-07-29); abstract page',
  'url': 'https://www.aimspress.com/article/doi/10.3934/mbe.2026004',
  'fetch_status': '200',
  'quote': ['Our analysis gives a more general insight into how the period and peak of epidemic waves depend on the '
            'shape of the memory kernel and how the level of minimal contact impacts the stability of the '
            'behavior-induced positive equilibrium.'],
  'raw_file': 'frontier/cx/F3_dist_memory_oscillations.txt',
  'note': 'Oscillation period set by the memory kernel: named.',
  'verified_substring': True,
  'id': 'cx:17'},
 {'domain': 'F3',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "'Behavior-induced oscillations in epidemic outbreaks with distributed memory: Beyond the linear chain "
            "trick using numerical methods', Mathematical Biosciences and Engineering 23(1):76-96 (2026), "
            'doi:10.3934/mbe.2026004 (targeted direction search)',
  'version': 'published 2025-11-28 (received 2025-07-29); abstract page',
  'url': 'https://www.aimspress.com/article/doi/10.3934/mbe.2026004',
  'fetch_status': '200',
  'quote': ['Information-related changes in contact patterns may trigger oscillations in the endemic prevalence of '
            'infectious diseases'],
  'raw_file': 'frontier/cx/F3_dist_memory_oscillations.txt',
  'note': "Title of d'Onofrio & Manfredi (2009) in the reference list: the information-index (memory) route to "
          'oscillations predates this work.',
  'verified_substring': True,
  'id': 'cx:18'},
 {'domain': 'F3',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Mohammed, Alsammani, 'Long-term Coexistence of Epidemics and Risk Awareness: Impacts of Adaptive Human "
            "Response and Fatigue', arXiv:2607.18301 (abstract page; found by the targeted direction search)",
  'version': 'arXiv v3, 2026-09-20',
  'url': 'https://arxiv.org/abs/2607.18301',
  'fetch_status': '200',
  'quote': ['Human behavior shapes epidemic dynamics, yet most models represent it by rescaling transmission, '
            'conflating behavior with biology and removing the memory carried by sustained protective behavior.'],
  'raw_file': 'frontier/cx/F3_fatigue_abs.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:19'},
 {'domain': 'F3',
  'kind': 'PROPOSAL',
  'tag': 'PROPOSAL',
  'source': "Mohammed, Alsammani, 'Long-term Coexistence of Epidemics and Risk Awareness: Impacts of Adaptive Human "
            "Response and Fatigue', arXiv:2607.18301 (abstract page; found by the targeted direction search)",
  'version': 'arXiv v3, 2026-09-20',
  'url': 'https://arxiv.org/abs/2607.18301',
  'fetch_status': '200',
  'quote': ['At finite relaxation rates, however, numerical stability and bifurcation analyses reveal a Hopf '
            'transition and self-sustained epidemic cycles without an imposed delay.'],
  'raw_file': 'frontier/cx/F3_fatigue_abs.txt',
  'note': 'A counterpoint: cycles without an imposed memory kernel.',
  'verified_substring': True,
  'id': 'cx:20'},
 {'domain': 'F4',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "D'Acunto, Charalambakis, Georgarakos, Kenny, Meyer, Weber, 'Household Inflation Expectations: An Overview "
            "of Recent Insights for Monetary Policy', NBER Working Paper 32488 (also ECB Discussion Paper 24)",
  'version': 'NBER WP 32488, May 2024',
  'url': 'https://www.nber.org/system/files/working_papers/w32488/w32488.pdf',
  'fetch_status': '200',
  'quote': ['Understanding how consumers make such temporal comparisons, i.e., how far back consumers look to form '
            'price change perceptions , represents an important subject for future research.'],
  'raw_file': 'frontier/cx/F4_dacunto_household_overview.txt',
  'note': 'The memory horizon is named as open. Stray space before the comma is in the extracted text.',
  'verified_substring': True,
  'id': 'cx:21'},
 {'domain': 'F4',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "D'Acunto, Charalambakis, Georgarakos, Kenny, Meyer, Weber, 'Household Inflation Expectations: An Overview "
            "of Recent Insights for Monetary Policy', NBER Working Paper 32488 (also ECB Discussion Paper 24)",
  'version': 'NBER WP 32488, May 2024',
  'url': 'https://www.nber.org/system/files/working_papers/w32488/w32488.pdf',
  'fetch_status': '200',
  'quote': ['the highly dispersed, extrapolative, and idiosyncratic nature of consumer inflation expectations poses '
            'important questions and challenges for what monetary policy can - or should - expect to achieve in terms '
            'of influencing consumers’ inflation expectations'],
  'raw_file': 'frontier/cx/F4_dacunto_household_overview.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:22'},
 {'domain': 'F4',
  'kind': 'PROPOSAL',
  'tag': 'PROPOSAL',
  'source': "D'Acunto, Charalambakis, Georgarakos, Kenny, Meyer, Weber, 'Household Inflation Expectations: An Overview "
            "of Recent Insights for Monetary Policy', NBER Working Paper 32488 (also ECB Discussion Paper 24)",
  'version': 'NBER WP 32488, May 2024',
  'url': 'https://www.nber.org/system/files/working_papers/w32488/w32488.pdf',
  'fetch_status': '200',
  'quote': ['D’Acunto and Weber (2022) recently put forward a memory framework in which consumers rely on selective '
            'recall of received price signals for specific goods when forming beliefs and often underestimate past '
            'prices.'],
  'raw_file': 'frontier/cx/F4_dacunto_household_overview.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:23'},
 {'domain': 'F4',
  'kind': 'PROPOSAL',
  'tag': 'PROPOSAL',
  'source': "D'Acunto, Charalambakis, Georgarakos, Kenny, Meyer, Weber, 'Household Inflation Expectations: An Overview "
            "of Recent Insights for Monetary Policy', NBER Working Paper 32488 (also ECB Discussion Paper 24)",
  'version': 'NBER WP 32488, May 2024',
  'url': 'https://www.nber.org/system/files/working_papers/w32488/w32488.pdf',
  'fetch_status': '200',
  'quote': ['the recent experience also highlights the importance of looking at measures of the cross-sectional '
            'distribution, such as the skewness of expectations, as an early-warning indicator of possible future '
            'de-anchoring.'],
  'raw_file': 'frontier/cx/F4_dacunto_household_overview.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:24'},
 {'domain': 'F4',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "D'Acunto, Charalambakis, Georgarakos, Kenny, Meyer, Weber, 'Household Inflation Expectations: An Overview "
            "of Recent Insights for Monetary Policy', NBER Working Paper 32488 (also ECB Discussion Paper 24)",
  'version': 'NBER WP 32488, May 2024',
  'url': 'https://www.nber.org/system/files/working_papers/w32488/w32488.pdf',
  'fetch_status': '200',
  'quote': ['and Nagel (2016) find that consumers overweight their own previous lifetime experience of inflation when '
            'thinking about future price changes.'],
  'raw_file': 'frontier/cx/F4_dacunto_household_overview.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:25'},
 {'domain': 'F4',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "D'Acunto, Charalambakis, Georgarakos, Kenny, Meyer, Weber, 'Household Inflation Expectations: An Overview "
            "of Recent Insights for Monetary Policy', NBER Working Paper 32488 (also ECB Discussion Paper 24)",
  'version': 'NBER WP 32488, May 2024',
  'url': 'https://www.nber.org/system/files/working_papers/w32488/w32488.pdf',
  'fetch_status': '200',
  'quote': ['Their model also implies that the inflation expectations of younger consumers, given their shorter '
            'lifetime inflation history, should react more strongly to the same shocks relative to older consumers'],
  'raw_file': 'frontier/cx/F4_dacunto_household_overview.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:26'},
 {'domain': 'F4',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Gennaioli, Leva, Schoenle, Shleifer, 'How Inflation Expectations De-Anchor: The Role of Selective Memory "
            "Cues', NBER Working Paper 32633",
  'version': 'NBER WP 32633, June 2024',
  'url': 'https://www.nber.org/system/files/working_papers/w32633/w32633.pdf',
  'fetch_status': '200',
  'quote': ['Malmendier and Nagel (2011, 2016, 2021) show that such expectations depend on a time-discounted average '
            'of lifetime inflation experiences, which of course only gradually adjusts to recent events.'],
  'raw_file': 'frontier/cx/F4_how_deanchor.txt',
  'note': 'The geometric/experience-weighted memory is the stated conventional wisdom.',
  'verified_substring': True,
  'id': 'cx:27'},
 {'domain': 'F4',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Gennaioli, Leva, Schoenle, Shleifer, 'How Inflation Expectations De-Anchor: The Role of Selective Memory "
            "Cues', NBER Working Paper 32633",
  'version': 'NBER WP 32633, June 2024',
  'url': 'https://www.nber.org/system/files/working_papers/w32633/w32633.pdf',
  'fetch_status': '200',
  'quote': ['Yet the evidence from the recent inflation surge does not support stickiness, nor does it align with a '
            'simple effect of past or recent experiences.'],
  'raw_file': 'frontier/cx/F4_how_deanchor.txt',
  'note': 'A bottleneck posed AGAINST the experience-weighted-memory direction.',
  'verified_substring': True,
  'id': 'cx:28'},
 {'domain': 'F4',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Gennaioli, Leva, Schoenle, Shleifer, 'How Inflation Expectations De-Anchor: The Role of Selective Memory "
            "Cues', NBER Working Paper 32633",
  'version': 'NBER WP 32633, June 2024',
  'url': 'https://www.nber.org/system/files/working_papers/w32633/w32633.pdf',
  'fetch_status': '200',
  'quote': ['Recency effects cannot explain all of: i) the stability of expectations in the pre-2021 period, ii) their '
            'sharp rise in April 2021, and iii) the strong de-anchoring by the elderly.'],
  'raw_file': 'frontier/cx/F4_how_deanchor.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:29'},
 {'domain': 'F4',
  'kind': 'PROPOSAL',
  'tag': 'PROPOSAL',
  'source': "Gennaioli, Leva, Schoenle, Shleifer, 'How Inflation Expectations De-Anchor: The Role of Selective Memory "
            "Cues', NBER Working Paper 32633",
  'version': 'NBER WP 32633, June 2024',
  'url': 'https://www.nber.org/system/files/working_papers/w32633/w32633.pdf',
  'fetch_status': '200',
  'quote': ['In a model of memory and selective recall, household inflation expectations remain rigid when inflation '
            'is anchored but exhibit sharp instability during inflation surges, as similarity prompts retrieval of '
            'forgotten high-inflation experiences.'],
  'raw_file': 'frontier/cx/F4_how_deanchor.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:30'},
 {'domain': 'F4',
  'kind': 'PROPOSAL',
  'tag': 'PROPOSAL',
  'source': "Gennaioli, Leva, Schoenle, Shleifer, 'How Inflation Expectations De-Anchor: The Role of Selective Memory "
            "Cues', NBER Working Paper 32633",
  'version': 'NBER WP 32633, June 2024',
  'url': 'https://www.nber.org/system/files/working_papers/w32633/w32633.pdf',
  'fetch_status': '200',
  'quote': ['Numerical similarity yields state-dependence, and hence memory based de-anchoring: as people see a jump '
            'in inflation, say from 2% to 10%, they start selectively recalling inflation levels around 10%.'],
  'raw_file': 'frontier/cx/F4_how_deanchor.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:31'},
 {'domain': 'F4',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Coibion, Gorodnichenko, 'Inflation, Expectations and Monetary Policy: What Have We Learned and to What "
            "End?', IZA Discussion Paper 17919",
  'version': 'IZA DP 17919, May 2025',
  'url': 'https://docs.iza.org/dp17919.pdf',
  'fetch_status': '200',
  'quote': ['First, how has the recent experience altered our views about the formation of inflation expectations by '
            'economic agents and their consequences?'],
  'raw_file': 'frontier/cx/F4_iza_inflation_expectations.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:32'},
 {'domain': 'F4',
  'kind': 'PROPOSAL',
  'tag': 'PROPOSAL',
  'source': "Coibion, Gorodnichenko, 'Inflation, Expectations and Monetary Policy: What Have We Learned and to What "
            "End?', IZA Discussion Paper 17919",
  'version': 'IZA DP 17919, May 2025',
  'url': 'https://docs.iza.org/dp17919.pdf',
  'fetch_status': '200',
  'quote': ['But if learning primarily takes place when inflation is high relative to the target, then it is natural '
            'that inflation expectations will appear to be systematically unanchored, both during the bad times when '
            'people are attentive (which is when central banks appear to be failing) as well as during the good times '
            'when people are inattentive and their expectations are shaped by their prior experiences.'],
  'raw_file': 'frontier/cx/F4_iza_inflation_expectations.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:33'},
 {'domain': 'F4',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Coibion, Gorodnichenko, 'Inflation, Expectations and Monetary Policy: What Have We Learned and to What "
            "End?', IZA Discussion Paper 17919",
  'version': 'IZA DP 17919, May 2025',
  'url': 'https://docs.iza.org/dp17919.pdf',
  'fetch_status': '200',
  'quote': ['consistent with a wide body of evidence that studies how large macroeconomic events like the Great '
            'Depression or hyperinflations can have persistent effects on beliefs'],
  'raw_file': 'frontier/cx/F4_iza_inflation_expectations.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:34'},
 {'domain': 'F4',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Christoffel, Farkas, 'Managing the risks of inflation expectation de-anchoring', ECB Working Paper 3082, "
            'doi:10.2866/7698288',
  'version': 'ECB WP 3082, (c) ECB 2025',
  'url': 'https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp3082~273898d46f.en.pdf',
  'fetch_status': '200',
  'quote': ['However, in times of high inflation or prolonged low inflation, there is a risk that inflation '
            'expectations may stray from the central bank’s target—a phenomenon known as de-anchoring.'],
  'raw_file': 'frontier/cx/F4_ecb_wp3082_deanchoring_risks.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:35'},
 {'domain': 'F4',
  'kind': 'PROPOSAL',
  'tag': 'PROPOSAL',
  'source': "Christoffel, Farkas, 'Managing the risks of inflation expectation de-anchoring', ECB Working Paper 3082, "
            'doi:10.2866/7698288',
  'version': 'ECB WP 3082, (c) ECB 2025',
  'url': 'https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp3082~273898d46f.en.pdf',
  'fetch_status': '200',
  'quote': ['We propose a monetary policy framework in which the central bank accounts for de-anchoring risks using a '
            'regime-switching model.'],
  'raw_file': 'frontier/cx/F4_ecb_wp3082_deanchoring_risks.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:36'},
 {'domain': 'F4',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Christoffel, Farkas, 'Managing the risks of inflation expectation de-anchoring', ECB Working Paper 3082, "
            'doi:10.2866/7698288',
  'version': 'ECB WP 3082, (c) ECB 2025',
  'url': 'https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp3082~273898d46f.en.pdf',
  'fetch_status': '200',
  'quote': ['Future research could provide a more comprehensive evaluation of various policy alternatives with respect '
            'to the implied risks of a de-anchoring of inflation expectations.'],
  'raw_file': 'frontier/cx/F4_ecb_wp3082_deanchoring_risks.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:37'},
 {'domain': 'F4',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Gati, 'Monetary policy & anchored expectations: an endogenous gain learning model', ECB Working Paper "
            '2685 (targeted direction search; older than the 2024-2026 window)',
  'version': 'ECB WP 2685, July 2022',
  'url': 'https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp2685~95e6d7b379.en.pdf',
  'fetch_status': '200',
  'quote': ['Thus, one can interpret the gain as the sensitivity of the expectations process to short-run surprises.'],
  'raw_file': 'frontier/cx/F4_ecb_wp2685_endogenous_gain.txt',
  'note': 'Adaptive learning with a gain; constant gain = geometric memory.',
  'verified_substring': True,
  'id': 'cx:38'},
 {'domain': 'F4',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Gati, 'Monetary policy & anchored expectations: an endogenous gain learning model', ECB Working Paper "
            '2685 (targeted direction search; older than the 2024-2026 window)',
  'version': 'ECB WP 2685, July 2022',
  'url': 'https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp2685~95e6d7b379.en.pdf',
  'fetch_status': '200',
  'quote': ['endogenous gain learning models can match time-varying volatility in the data, a feature that constant '
            'gain learning or rational expectations models cannot account for.'],
  'raw_file': 'frontier/cx/F4_ecb_wp2685_endogenous_gain.txt',
  'note': 'Constant-gain learning is named as the baseline that an endogenous gain improves on.',
  'verified_substring': True,
  'id': 'cx:39'},
 {'domain': 'F4',
  'kind': 'PROPOSAL',
  'tag': 'PROPOSAL',
  'source': "Gati, 'Monetary policy & anchored expectations: an endogenous gain learning model', ECB Working Paper "
            '2685 (targeted direction search; older than the 2024-2026 window)',
  'version': 'ECB WP 2685, July 2022',
  'url': 'https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp2685~95e6d7b379.en.pdf',
  'fetch_status': '200',
  'quote': ['The endogenous gain can thus be interpreted as a metric of the varying degrees of unanchoring.'],
  'raw_file': 'frontier/cx/F4_ecb_wp2685_endogenous_gain.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:40'},
 {'domain': 'F5',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Zhou, Zheng, Tian, Jiang, Zhang, 'Twenty-Five Years of the Intelligent Driver Model: Foundations, "
            "Extensions, Applications, and Future Directions', arXiv:2506.05909",
  'version': 'arXiv v2, 2025-11-23 (latest on the day)',
  'url': 'https://arxiv.org/pdf/2506.05909',
  'fetch_status': '200 (PDF text extraction lost many inter-word spaces; quotes keep the extracted form)',
  'quote': ['Yet, much of this literature remains confined to linearized scenarios, externally imposed uncertainties, '
            'and idealized driver behaviors, limiting its explanatory power in real-world complexity.'],
  'raw_file': 'frontier/cx/F5_idm_25years.txt',
  'note': 'About the traffic-stability literature.',
  'verified_substring': True,
  'id': 'cx:41'},
 {'domain': 'F5',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Zhou, Zheng, Tian, Jiang, Zhang, 'Twenty-Five Years of the Intelligent Driver Model: Foundations, "
            "Extensions, Applications, and Future Directions', arXiv:2506.05909",
  'version': 'arXiv v2, 2025-11-23 (latest on the day)',
  'url': 'https://arxiv.org/pdf/2506.05909',
  'fetch_status': '200 (PDF text extraction lost many inter-word spaces; quotes keep the extracted form)',
  'quote': ['With its lack of mechanisms for cooperative driving or information-sharing, IDM is less effective in '
            'modeling connected and autonomous vehicle (CAV) interactions, as well as mixed traffic environments.'],
  'raw_file': 'frontier/cx/F5_idm_25years.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:42'},
 {'domain': 'F5',
  'kind': 'PROPOSAL',
  'tag': 'PROPOSAL',
  'source': "Zhou, Zheng, Tian, Jiang, Zhang, 'Twenty-Five Years of the Intelligent Driver Model: Foundations, "
            "Extensions, Applications, and Future Directions', arXiv:2506.05909",
  'version': 'arXiv v2, 2025-11-23 (latest on the day)',
  'url': 'https://arxiv.org/pdf/2506.05909',
  'fetch_status': '200 (PDF text extraction lost many inter-word spaces; quotes keep the extracted form)',
  'quote': ['Future directions include integrating stochastic elements, human behavioral insights, and hybrid modeling '
            'approaches that combine physics-based structures with data-driven methodologies.'],
  'raw_file': 'frontier/cx/F5_idm_25years.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:43'},
 {'domain': 'F5',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Zhou, Zheng, Tian, Jiang, Zhang, 'Twenty-Five Years of the Intelligent Driver Model: Foundations, "
            "Extensions, Applications, and Future Directions', arXiv:2506.05909",
  'version': 'arXiv v2, 2025-11-23 (latest on the day)',
  'url': 'https://arxiv.org/pdf/2506.05909',
  'fetch_status': '200 (PDF text extraction lost many inter-word spaces; quotes keep the extracted form)',
  'quote': ['IDMM (IDM with memory), which incorporates driver adaptation to traffic states.'],
  'raw_file': 'frontier/cx/F5_idm_25years.txt',
  'note': 'Memory of traffic state (level of service), not headway history.',
  'verified_substring': True,
  'id': 'cx:44'},
 {'domain': 'F5',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Zhou, Zheng, Tian, Jiang, Zhang, 'Twenty-Five Years of the Intelligent Driver Model: Foundations, "
            "Extensions, Applications, and Future Directions', arXiv:2506.05909",
  'version': 'arXiv v2, 2025-11-23 (latest on the day)',
  'url': 'https://arxiv.org/pdf/2506.05909',
  'fetch_status': '200 (PDF text extraction lost many inter-word spaces; quotes keep the extracted form)',
  'quote': ['While IDM does not directly account for reaction time, it can be extended to include factors such as '
            'reaction delays, estimation errors, and multi-vehicle anticipation.'],
  'raw_file': 'frontier/cx/F5_idm_25years.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:45'},
 {'domain': 'F5',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Zhou, Zheng, Tian, Jiang, Zhang, 'Twenty-Five Years of the Intelligent Driver Model: Foundations, "
            "Extensions, Applications, and Future Directions', arXiv:2506.05909",
  'version': 'arXiv v2, 2025-11-23 (latest on the day)',
  'url': 'https://arxiv.org/pdf/2506.05909',
  'fetch_status': '200 (PDF text extraction lost many inter-word spaces; quotes keep the extracted form)',
  'quote': ['Their analysis of CF behaviorin a '
            '25-carplatoonexperimentshowsthatreactiondelayhasanegligibleeffectonfluctuationgrowth'],
  'raw_file': 'frontier/cx/F5_idm_25years.txt',
  'note': 'Extraction lost spaces. Counter-evidence: a platoon experiment finds reaction delay negligible for '
          'oscillation growth, against a delay/memory-driven account.',
  'verified_substring': True,
  'id': 'cx:46'},
 {'domain': 'F5',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Zhang et al., 'Car-Following Models: A Multidisciplinary Review', arXiv:2304.07143",
  'version': 'arXiv v4, 2024-03-05 (HTML); a v5 of 2025-02-16 exists and was NOT fetched',
  'url': 'https://arxiv.org/html/2304.07143v4',
  'fetch_status': '200',
  'quote': ['By introducing an internal dynamical variable to represent the subjective level of service, Treiber and '
            'Helbing[80] build the IDMM (intelligent driver model with memory) to incorporate memory effects in '
            'microscopic traffic models.'],
  'raw_file': 'frontier/cx/F5_carfollowing_review.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:47'},
 {'domain': 'F5',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Zhang et al., 'Car-Following Models: A Multidisciplinary Review', arXiv:2304.07143",
  'version': 'arXiv v4, 2024-03-05 (HTML); a v5 of 2025-02-16 exists and was NOT fetched',
  'url': 'https://arxiv.org/html/2304.07143v4',
  'fetch_status': '200',
  'quote': ['analyzed the long-term memory effect in the car-following model using a deep learning model by taking '
            'various time-horizon historical information as inputs.'],
  'raw_file': 'frontier/cx/F5_carfollowing_review.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:48'},
 {'domain': 'F5',
  'kind': 'PROPOSAL',
  'tag': 'PROPOSAL',
  'source': "Zhang et al., 'Car-Following Models: A Multidisciplinary Review', arXiv:2304.07143",
  'version': 'arXiv v4, 2024-03-05 (HTML); a v5 of 2025-02-16 exists and was NOT fetched',
  'url': 'https://arxiv.org/html/2304.07143v4',
  'fetch_status': '200',
  'quote': ['A serial distributed model predictive control (MPC) [141] is developed for connected automated vehicles '
            '(CAVs), ensuring local stability and multi-criteria string stability by formulating future state '
            'constraints and tuning weight matrices, with mathematical proofs and simulations demonstrating its '
            'superiority over traditional MPC methods in maintaining stability.'],
  'raw_file': 'frontier/cx/F5_carfollowing_review.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:49'},
 {'domain': 'F5',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Zhang et al., 'Car-Following Models: A Multidisciplinary Review', arXiv:2304.07143",
  'version': 'arXiv v4, 2024-03-05 (HTML); a v5 of 2025-02-16 exists and was NOT fetched',
  'url': 'https://arxiv.org/html/2304.07143v4',
  'fetch_status': '200',
  'quote': ['The future direction of driver behavior models, particularly in the context of integrating Artificial '
            'General Intelligent (AGI) capabilities and learning efficiencies into car following models, presents a '
            'fascinating and complex challenge.'],
  'raw_file': 'frontier/cx/F5_carfollowing_review.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:50'},
 {'domain': 'F5',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Ehrhardt, Tordeux, 'Stability of heterogeneous linear and nonlinear car-following models', "
            'arXiv:2408.07549 (preprint submitted to Franklin Open)',
  'version': 'arXiv v1, 2024-08-14',
  'url': 'https://arxiv.org/pdf/2408.07549',
  'fetch_status': '200',
  'quote': ['Despite the large number of studies, understanding and controlling stop-and-go in road traffic flow '
            'remains challenging and still nowadays an active area of research.'],
  'raw_file': 'frontier/cx/F5_heterogeneous_stability.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:51'},
 {'domain': 'F5',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Ehrhardt, Tordeux, 'Stability of heterogeneous linear and nonlinear car-following models', "
            'arXiv:2408.07549 (preprint submitted to Franklin Open)',
  'version': 'arXiv v1, 2024-08-14',
  'url': 'https://arxiv.org/pdf/2408.07549',
  'fetch_status': '200',
  'quote': ['In particular, the role of heterogeneity and non-linearity in the shape of the model remains poorly '
            'understood.'],
  'raw_file': 'frontier/cx/F5_heterogeneous_stability.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:52'},
 {'domain': 'F5',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Sipahi, Niculescu, 'Stability of car following with human memory effects and automatic headway "
            "compensation', Phil. Trans. R. Soc. A 368:4563-4583 (2010), doi:10.1098/rsta.2010.0127, PMID 20819822 "
            '(targeted direction search; abstract only, via Europe PMC; older than the window)',
  'version': '2010-10 (abstract record)',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:20819822%20AND%20SRC:MED&resultType=core&format=xml',
  'fetch_status': '200',
  'quote': ['More precisely, the delayed action/decision of human drivers is represented using distributed delays with '
            'a gap and the considered automated controller is of proportional derivative type.'],
  'raw_file': 'frontier/cx/F5_sipahi_memory_headway_epmc.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:53'},
 {'domain': 'F5',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Sipahi, Niculescu, 'Stability of car following with human memory effects and automatic headway "
            "compensation', Phil. Trans. R. Soc. A 368:4563-4583 (2010), doi:10.1098/rsta.2010.0127, PMID 20819822 "
            '(targeted direction search; abstract only, via Europe PMC; older than the window)',
  'version': '2010-10 (abstract record)',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:20819822%20AND%20SRC:MED&resultType=core&format=xml',
  'fetch_status': '200',
  'quote': ['Surprisingly, large delays and/or gains improve stability for the corresponding closed-loop schemes.'],
  'raw_file': 'frontier/cx/F5_sipahi_memory_headway_epmc.txt',
  'note': 'Stability as a function of memory (distributed delay) is analysed; the sign here is stabilising in the '
          'closed loop.',
  'verified_substring': True,
  'id': 'cx:54'},
 {'domain': 'F6',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Dakos et al., 'Tipping point detection and early warnings in climate, ecological, and human systems', "
            'Earth System Dynamics 15:1117-1135 (2024), doi:10.5194/esd-15-1117-2024',
  'version': 'published 2024-08-19 (received 2023-08-01, revised 2024-03-26)',
  'url': 'https://esd.copernicus.org/articles/15/1117/2024/esd-15-1117-2024.pdf',
  'fetch_status': '200',
  'quote': ['Whatever the term used, while early warnings are well grounded in theory, the challenge remains to apply '
            'them to real-world systems.'],
  'raw_file': 'frontier/cx/F6_dakos_esd2024.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:55'},
 {'domain': 'F6',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Dakos et al., 'Tipping point detection and early warnings in climate, ecological, and human systems', "
            'Earth System Dynamics 15:1117-1135 (2024), doi:10.5194/esd-15-1117-2024',
  'version': 'published 2024-08-19 (received 2023-08-01, revised 2024-03-26)',
  'url': 'https://esd.copernicus.org/articles/15/1117/2024/esd-15-1117-2024.pdf',
  'fetch_status': '200',
  'quote': ['The detection of early warnings relies on the assumption that the system is approaching a transition '
            'gradually.'],
  'raw_file': 'frontier/cx/F6_dakos_esd2024.txt',
  'note': "Opens 4.2.1 'Fast changes, slow responses, stochasticity, multiple drivers, and limited data challenge "
          "early warning performance'.",
  'verified_substring': True,
  'id': 'cx:56'},
 {'domain': 'F6',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Dakos et al., 'Tipping point detection and early warnings in climate, ecological, and human systems', "
            'Earth System Dynamics 15:1117-1135 (2024), doi:10.5194/esd-15-1117-2024',
  'version': 'published 2024-08-19 (received 2023-08-01, revised 2024-03-26)',
  'url': 'https://esd.copernicus.org/articles/15/1117/2024/esd-15-1117-2024.pdf',
  'fetch_status': '200',
  'quote': ['we simply do not know what similar information early warnings provide.'],
  'raw_file': 'frontier/cx/F6_dakos_esd2024.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:57'},
 {'domain': 'F6',
  'kind': 'PROPOSAL',
  'tag': 'PROPOSAL',
  'source': "Dakos et al., 'Tipping point detection and early warnings in climate, ecological, and human systems', "
            'Earth System Dynamics 15:1117-1135 (2024), doi:10.5194/esd-15-1117-2024',
  'version': 'published 2024-08-19 (received 2023-08-01, revised 2024-03-26)',
  'url': 'https://esd.copernicus.org/articles/15/1117/2024/esd-15-1117-2024.pdf',
  'fetch_status': '200',
  'quote': ['The next step is to develop meaningful ways to best combine them for detecting tipping points.'],
  'raw_file': 'frontier/cx/F6_dakos_esd2024.txt',
  'note': 'Composite metrics (4.3.1).',
  'verified_substring': True,
  'id': 'cx:58'},
 {'domain': 'F6',
  'kind': 'PROPOSAL',
  'tag': 'PROPOSAL',
  'source': "Dakos et al., 'Tipping point detection and early warnings in climate, ecological, and human systems', "
            'Earth System Dynamics 15:1117-1135 (2024), doi:10.5194/esd-15-1117-2024',
  'version': 'published 2024-08-19 (received 2023-08-01, revised 2024-03-26)',
  'url': 'https://esd.copernicus.org/articles/15/1117/2024/esd-15-1117-2024.pdf',
  'fetch_status': '200',
  'quote': ['Deep learning models which combine convolutional lay- ers have been shown to outperform methods using '
            'statisti- cal CSD-based warnings (e.g. variance, AR(1)) in a variety of both real and simulated case '
            'studies (Bury et al., 2021; Deb et al., 2022).'],
  'raw_file': 'frontier/cx/F6_dakos_esd2024.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:59'},
 {'domain': 'F6',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Dakos et al., 'Tipping point detection and early warnings in climate, ecological, and human systems', "
            'Earth System Dynamics 15:1117-1135 (2024), doi:10.5194/esd-15-1117-2024',
  'version': 'published 2024-08-19 (received 2023-08-01, revised 2024-03-26)',
  'url': 'https://esd.copernicus.org/articles/15/1117/2024/esd-15-1117-2024.pdf',
  'fetch_status': '200',
  'quote': ['Fisher information (temporal)'],
  'raw_file': 'frontier/cx/F6_dakos_esd2024.txt',
  'note': "Fisher information appears in the review's list of early-warning indicators used in empirical studies.",
  'verified_substring': True,
  'id': 'cx:60'},
 {'domain': 'F6',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Dakos et al., 'Tipping point detection and early warnings in climate, ecological, and human systems', "
            'Earth System Dynamics 15:1117-1135 (2024), doi:10.5194/esd-15-1117-2024',
  'version': 'published 2024-08-19 (received 2023-08-01, revised 2024-03-26)',
  'url': 'https://esd.copernicus.org/articles/15/1117/2024/esd-15-1117-2024.pdf',
  'fetch_status': '200',
  'quote': ['Other ML techniques can also tell us something about how far systems are from tipping.'],
  'raw_file': 'frontier/cx/F6_dakos_esd2024.txt',
  'note': 'Distance-to-tipping is posed, but via ML, not in Fisher (distinguishable-step) units.',
  'verified_substring': True,
  'id': 'cx:61'},
 {'domain': 'F6',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Diekert, Heyen, Nesje, Shayegh, 'Do early warning signals of tipping points lead to better decisions?', "
            'J. R. Soc. Interface 22(225) 20240864 (2025), doi:10.1098/rsif.2024.0864, PMC11978447 (abstract only)',
  'version': '2025-04 (Europe PMC core record)',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1098/rsif.2024.0864&resultType=core&format=xml',
  'fetch_status': '200 (PMC HTML: reCAPTCHA; Europe PMC fullTextXML: 500; publisher PDF: 403)',
  'quote': ['Despite notable progress in identifying statistical indicators that can provide early warning signals '
            '(EWS) of tipping points, they have yet to find direct application in management.'],
  'raw_file': 'frontier/cx/F6_ews_decisions_epmc.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:62'},
 {'domain': 'F6',
  'kind': 'BOTTLENECK',
  'tag': 'BOTTLENECK',
  'source': "Diekert, Heyen, Nesje, Shayegh, 'Do early warning signals of tipping points lead to better decisions?', "
            'J. R. Soc. Interface 22(225) 20240864 (2025), doi:10.1098/rsif.2024.0864, PMC11978447 (abstract only)',
  'version': '2025-04 (Europe PMC core record)',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1098/rsif.2024.0864&resultType=core&format=xml',
  'fetch_status': '200 (PMC HTML: reCAPTCHA; Europe PMC fullTextXML: 500; publisher PDF: 403)',
  'quote': ['We demonstrate that although EWSys can help balance the risk of tipping by providing information to '
            'update the belief about the location of the tipping point, it may also result in more risky behaviour in '
            'the case that no EWS is received.'],
  'raw_file': 'frontier/cx/F6_ews_decisions_epmc.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:63'},
 {'domain': 'F6',
  'kind': 'PROPOSAL',
  'tag': 'PROPOSAL',
  'source': "Diekert, Heyen, Nesje, Shayegh, 'Do early warning signals of tipping points lead to better decisions?', "
            'J. R. Soc. Interface 22(225) 20240864 (2025), doi:10.1098/rsif.2024.0864, PMC11978447 (abstract only)',
  'version': '2025-04 (Europe PMC core record)',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1098/rsif.2024.0864&resultType=core&format=xml',
  'fetch_status': '200 (PMC HTML: reCAPTCHA; Europe PMC fullTextXML: 500; publisher PDF: 403)',
  'quote': ['Here, we develop a theoretical model of an early warning system (EWSys) that integrates EWS information '
            'into a simple decision-making process.'],
  'raw_file': 'frontier/cx/F6_ews_decisions_epmc.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:64'},
 {'domain': 'F6',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Karunanithi, Cabezas, Frieden, Pawlowski, 'Detection and Assessment of Ecosystem Regime Shifts from "
            "Fisher Information', Ecology and Society 13(1):22 (2008), doi:10.5751/ES-02318-130122 (targeted direction "
            'search; older than the window)',
  'version': 'published 2008-05-13',
  'url': 'https://www.ecologyandsociety.org/vol13/iss1/art22/main.html',
  'fetch_status': '200',
  'quote': ['Here we propose the use of Fisher information as a means of: (1) detecting dynamic regime shifts in '
            'ecosystems, and (2) assessing the quality of the shift in terms of intensity and pervasiveness.'],
  'raw_file': 'frontier/cx/F6_karunanithi_fisher_2008.txt',
  'note': "Fisher information as a regime-shift indicator, named since 2008 (the Frieden 'dynamic order' form over "
          'states, not the parameter-space Fisher metric).',
  'verified_substring': True,
  'id': 'cx:65'},
 {'domain': 'F6',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Karunanithi, Cabezas, Frieden, Pawlowski, 'Detection and Assessment of Ecosystem Regime Shifts from "
            "Fisher Information', Ecology and Society 13(1):22 (2008), doi:10.5751/ES-02318-130122 (targeted direction "
            'search; older than the window)',
  'version': 'published 2008-05-13',
  'url': 'https://www.ecologyandsociety.org/vol13/iss1/art22/main.html',
  'fetch_status': '200',
  'quote': ['There is a great need for indicators of regime shifts, particularly methods that are applicable to data '
            'from real systems.'],
  'raw_file': 'frontier/cx/F6_karunanithi_fisher_2008.txt',
  'note': '',
  'verified_substring': True,
  'id': 'cx:66'},
 {'domain': 'F6',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Karunanithi, Cabezas, Frieden, Pawlowski, 'Detection and Assessment of Ecosystem Regime Shifts from "
            "Fisher Information', Ecology and Society 13(1):22 (2008), doi:10.5751/ES-02318-130122 (targeted direction "
            'search; older than the window)',
  'version': 'published 2008-05-13',
  'url': 'https://www.ecologyandsociety.org/vol13/iss1/art22/main.html',
  'fetch_status': '200',
  'quote': ['are indistinguishable from each other if'],
  'raw_file': 'frontier/cx/F6_karunanithi_fisher_2008.txt',
  'note': 'States are binned by measurement uncertainty (distinguishability) before Fisher information is computed: a '
          "partial overlap with 'distinguishable steps'.",
  'verified_substring': True,
  'id': 'cx:67'},
 {'domain': 'F6',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NAMED',
  'source': "Da Silva, Vieira, Leonel, 'The Geometric Bifurcation Theory', chapter 4 of 'Geometric Bifurcation Theory' "
            '(Springer, Nonlinear Physical Science), doi:10.1007/978-981-95-8291-4_4 (preview page only; found by the '
            'targeted direction search). The companion review in Physics Reports (2026), '
            'doi:10.1016/j.physrep.2026.01.004, returned 403 (captcha) at ScienceDirect; Crossref carries no abstract; '
            'not quoted',
  'version': 'published 2026-06-03 (chapter preview)',
  'url': 'https://link.springer.com/chapter/10.1007/978-981-95-8291-4_4',
  'fetch_status': '200 (preview; body behind subscription)',
  'quote': ['This includes the construction of Riemannian manifolds from dynamical systems, the Fisher information '
            'metric, and the role of scalar curvature in detecting bifurcations, local structural stability, and the '
            'character of phase–space trajectories.'],
  'raw_file': 'frontier/cx/F6_gbt_springer_chapter.txt',
  'note': 'Fisher metric on parameter space used to detect bifurcations (curvature), not an arc-length distance to '
          'tipping.',
  'verified_substring': True,
  'id': 'cx:68'},
 {'domain': 'F6',
  'kind': 'DIRECTION',
  'tag': 'DIRECTION-NOT-FOUND-IN-FETCHED',
  'source': 'all F6 texts fetched (F6_dakos_esd2024, F6_ews_decisions_epmc, F6_karunanithi_fisher_2008, '
            'F6_gbt_springer_chapter, F6_geometric_separatrix_abs)',
  'version': '2026-09-27 fetch',
  'url': '',
  'fetch_status': '',
  'quote': [],
  'raw_file': 'frontier/cx/F6_*.txt',
  'note': 'Second half of the F6 direction: measuring the distance to a tipping point as a count of statistically '
          'distinguishable steps (a Fisher-metric arc length) instead of clock time. Searched the saved texts '
          "(case-insensitive) for 'distance', 'distinguish', 'proximity', 'how far', 'time to', 'clock', 'Fisher'; "
          "plus web searches 'information geometry early warning bifurcation Fisher information metric distance to "
          "tipping point statistical distinguishability' and 'Fisher information regime shift indicator ecosystem "
          "review 2024 2025'. Nearest hits: Dakos 2024 poses 'how far systems are from tipping' via ML; Karunanithi "
          '2008 bins states by distinguishability before computing Fisher information; the Geometric Bifurcation '
          "Theory chapter uses the Fisher metric's curvature to detect bifurcations. None of the fetched texts states "
          'the Fisher arc length to the tipping point as the measure. This is a statement about the fetched texts '
          "only; it is NOT a claim of novelty (declaration: 'Not found in the sources' is never read as 'novel').",
  'id': 'cx:69'},
 {'domain': 'F8',
  'kind': 'BOTTLENECK',
  'source': 'Zhuang & Sornette, How to quantify earthquake predictability? Advances in earthquake forecasting and '
            'predictability limits',
  'version': 'arXiv:2607.26918v1 (29 Jul 2026)',
  'url': 'https://arxiv.org/html/2607.26918v1',
  'quote': ['However, it remains unclear whether the forecasting performance of a model, quantified by the likelihood '
            'ratio against a model of complete randomness, is necessarily bounded by the intrinsic predictability '
            'capacity of the forecasting model itself.',
            'Taken together, these considerations indicate that earthquake forecasting remains an active and '
            'scientifically challenging field in which both progress and fundamental limitations must be carefully '
            'assessed.'],
  'raw_file': 'frontier/phys/f8_sornette2026_predictability_arXiv2607.26918v1.txt',
  'note': 'Open question: how much predictability exists, and whether model skill is bounded by it.',
  'id': 'phys:0'},
 {'domain': 'F8',
  'kind': 'PROPOSAL',
  'source': 'Zhuang & Sornette, How to quantify earthquake predictability? Advances in earthquake forecasting and '
            'predictability limits',
  'version': 'arXiv:2607.26918v1 (29 Jul 2026)',
  'url': 'https://arxiv.org/html/2607.26918v1',
  'quote': ['This paper develops a unified information-theoretic framework to quantify predictability.',
            'Particularly, pseudo-prospective forecasting experiments have suggested that gV-ETAS models incorporating '
            'magnitude-dependent triggering may outperform the standard ETAS formulation',
            'Future work should therefore integrate information-theoretic measures of predictability with explicit '
            'utility or loss functions that reflect societal, economic, and safety priorities.'],
  'raw_file': 'frontier/phys/f8_sornette2026_predictability_arXiv2607.26918v1.txt',
  'note': 'Proposals: entropy-gap predictability; ETAS variants (gV-ETAS); utility-aware evaluation.',
  'id': 'phys:1'},
 {'domain': 'F8',
  'kind': 'BOTTLENECK',
  'source': 'Stockman et al., EarthquakeNPP: A Benchmark for Earthquake Forecasting with Neural Point Processes',
  'version': 'arXiv:2410.08226v3 (10 Mar 2026)',
  'url': 'https://arxiv.org/html/2410.08226v3',
  'quote': ['Benchmarking experiments, using both log-likelihood and generative evaluation metrics widely recognised '
            'in seismology, show that none of the five NPPs tested outperform ETAS.',
            'Data missingness, referred to in seismology as catalog (in)completeness, is the primary challenge faced '
            'with earthquake catalogs.'],
  'raw_file': 'frontier/phys/f8_stockman_earthquakeNPP_arXiv2410.08226v3.txt',
  'note': 'Bottleneck: ML (neural point processes) does not yet beat ETAS; catalogue incompleteness.',
  'id': 'phys:2'},
 {'domain': 'F8',
  'kind': 'PROPOSAL',
  'source': 'Stockman et al., EarthquakeNPP: A Benchmark for Earthquake Forecasting with Neural Point Processes',
  'version': 'arXiv:2410.08226v3 (10 Mar 2026)',
  'url': 'https://arxiv.org/html/2410.08226v3',
  'quote': ['Current NPP architectures struggle most in mainshock dominated regimes but show clear promise in '
            'modelling spatially complex background seismicity and swarm driven activity, motivating future work on '
            'incorporating large magnitude triggering while preserving this flexibility.'],
  'raw_file': 'frontier/phys/f8_stockman_earthquakeNPP_arXiv2410.08226v3.txt',
  'note': 'Proposal: neural point processes with large-magnitude triggering.',
  'id': 'phys:3'},
 {'domain': 'F8',
  'kind': 'BOTTLENECK',
  'source': 'Mizrahi et al., Developing, Testing, and Communicating Earthquake Forecasts: Current Practices and Future '
            'Directions, Rev. Geophys. 62(3) (2024), DOI 10.1029/2023RG000823',
  'version': 'published version, author-hosted PDF (downloaded 13/08/2024 per PDF footer)',
  'url': 'http://wpage.unina.it/iuniervo/papers/Mizrahi_et_al_Reviews_of_Geophysics_2024.pdf',
  'quote': ['Because no two implementations of the model are identical, the earthquake forecasting community faces the '
            'challenge that a truly standardized benchmark version of the ETAS model is currently lacking.',
            'Incompleteness entailed by strong events is also not automatically corrected in the current version of '
            'the system; so far, corrections for incompleteness are applied by hand only immediately after a large '
            'earthquake.'],
  'raw_file': 'frontier/phys/f8_mizrahi2024_revgeophys_unina.txt',
  'note': 'Bottlenecks: no standard ETAS benchmark; short-term incompleteness after large events.',
  'id': 'phys:4'},
 {'domain': 'F8',
  'kind': 'PROPOSAL',
  'source': 'Mizrahi et al., Developing, Testing, and Communicating Earthquake Forecasts: Current Practices and Future '
            'Directions, Rev. Geophys. 62(3) (2024), DOI 10.1029/2023RG000823',
  'version': 'published version, author-hosted PDF (downloaded 13/08/2024 per PDF footer)',
  'url': 'http://wpage.unina.it/iuniervo/papers/Mizrahi_et_al_Reviews_of_Geophysics_2024.pdf',
  'quote': ['(c) continued research on the development of superior forecasting models by including more information on '
            'earthquake physics, or by exploring alternative or complementary models for earthquake forecasting using '
            'machine learning (ML) techniques.',
            'Another noteworthy advantage of neural point process models is that they are extremely adaptive to '
            'nonstationarities in earthquake catalogs.'],
  'raw_file': 'frontier/phys/f8_mizrahi2024_revgeophys_unina.txt',
  'note': 'Proposals: more physics; ML / neural point processes.',
  'id': 'phys:5'},
 {'domain': 'F8',
  'kind': 'DIRECTION',
  'source': 'Mizrahi et al., Developing, Testing, and Communicating Earthquake Forecasts: Current Practices and Future '
            'Directions, Rev. Geophys. 62(3) (2024), DOI 10.1029/2023RG000823',
  'version': 'published version, author-hosted PDF (downloaded 13/08/2024 per PDF footer)',
  'url': 'http://wpage.unina.it/iuniervo/papers/Mizrahi_et_al_Reviews_of_Geophysics_2024.pdf',
  'quote': ['Clements et al. (2011) also describe a series of residual analysis for point‐process methods, which '
            'consist of transforming the points of a simulated/observed catalog (e.g., by rescaling, thinning, '
            'superpositioning), such that the resulting transformed process should be homogeneous‐Poisson if the '
            'original model were consistent with the observations.',
            'Additional tests have been proposed in the literature, which do not depend on (pseudo‐) likelihood '
            'functions or have not been yet implemented in routine CSEP experiments.'],
  'raw_file': 'frontier/phys/f8_mizrahi2024_revgeophys_unina.txt',
  'note': 'DIRECTION-NAMED: time-rescaling / residual analysis (transform to homogeneous Poisson = compensator time) '
          'is named as an existing test method, not yet routine in CSEP. Ogata (1988) residual analysis is cited in '
          'the reference lists of Mizrahi, Stockman, Zhuang-Sornette and Wen.',
  'id': 'phys:6'},
 {'domain': 'F8',
  'kind': 'BOTTLENECK',
  'source': 'Wen et al., Integrating Artificial Intelligence and Geophysical Insights for Earthquake Forecasting: A '
            'Cross-Disciplinary Review',
  'version': 'arXiv:2502.12161v1 (10 Feb 2025)',
  'url': 'https://arxiv.org/html/2502.12161v1',
  'quote': ['Despite decades of research, earthquake forecasting remains in an exploratory stage, with current methods '
            'still falling short of achieving performance levels that would provide meaningful benefits for society.',
            'Due to a lack of understanding of specialized knowledge in earthquake forecasting, researchers often '
            'focus solely on high scores from evaluation metrics and hastily claim the success of their models, '
            'overlooking the deeper principles of seismology and the challenges present in practical applications.'],
  'raw_file': 'frontier/phys/f8_wen2025_ai_eq_review_arXiv2502.12161v1.txt',
  'note': 'Bottleneck: skill short of societal use; evaluation practice in ML papers.',
  'id': 'phys:7'},
 {'domain': 'F8',
  'kind': 'PROPOSAL',
  'source': 'Wen et al., Integrating Artificial Intelligence and Geophysical Insights for Earthquake Forecasting: A '
            'Cross-Disciplinary Review',
  'version': 'arXiv:2502.12161v1 (10 Feb 2025)',
  'url': 'https://arxiv.org/html/2502.12161v1',
  'quote': ['To overcome these limitations, there is a growing recognition of the need to integrate non-seismic and '
            'non-mechanical information into earthquake forecasting models.',
            'When we want to demonstrate that a newly developed model surpasses existing limitations, we should '
            'compare our model with the best current models, including both the best AI models and the most advanced '
            'geophysical or statistical seismological models.'],
  'raw_file': 'frontier/phys/f8_wen2025_ai_eq_review_arXiv2502.12161v1.txt',
  'note': 'Proposals: multi-source data; strong baselines.',
  'id': 'phys:8'},
 {'domain': 'F8',
  'kind': 'DIRECTION',
  'source': 'Rundle, Baughman, Donnellan, Grant, Fox, From Local Earthquake Nowcasting to Natural Time Forecasting: A '
            'Simple Do-It-Yourself (DIY) Method (targeted search; research article, not a review)',
  'version': 'arXiv:2510.02467v2 (16 Oct 2025)',
  'url': 'https://arxiv.org/pdf/2510.02467v2',
  'quote': ['We work in natural time, which is defined as the count of small earthquakes between large earthquakes.',
            'The probability is conditioned on the number of small earthquakes n(t) that have occurred since the last '
            'large earthquake.'],
  'raw_file': 'frontier/phys/f8_rundle2025_natural_time_DIY_arXiv2510.02467v2.txt',
  'note': 'DIRECTION-NAMED (targeted search): event-count natural time is an existing forecasting method (Rundle et '
          'al. nowcasting line).',
  'id': 'phys:9'},
 {'domain': 'F9',
  'kind': 'BOTTLENECK',
  'source': 'Montenegro et al., Review: Quantum Metrology and Sensing with Many-Body Systems, Phys. Rep. (2025), DOI '
            '10.1016/j.physrep.2025.05.005',
  'version': 'arXiv:2408.15323v3 (7 Jun 2025)',
  'url': 'https://arxiv.org/html/2408.15323v3',
  'quote': ['Another problem which requires further investigation is the performance of quantum sensors under '
            'imperfect situations, such as the presence of decoherence',
            'the notion of robustness has not yet been formulated quantitatively for quantum sensors.',
            'Furthermore, a general issue for quantum sensors arise in the multi-parameter Cramér-Rao inequality as '
            'the bounds are not tight and thus saturating them may not be achievable'],
  'raw_file': 'frontier/phys/f9_montenegro_manybody_review_arXiv2408.15323v3.txt',
  'note': 'Bottlenecks: decoherence; robustness undefined; multiparameter CR bound not tight.',
  'id': 'phys:10'},
 {'domain': 'F9',
  'kind': 'PROPOSAL',
  'source': 'Montenegro et al., Review: Quantum Metrology and Sensing with Many-Body Systems, Phys. Rep. (2025), DOI '
            '10.1016/j.physrep.2025.05.005',
  'version': 'arXiv:2408.15323v3 (7 Jun 2025)',
  'url': 'https://arxiv.org/html/2408.15323v3',
  'quote': ['A related approach is the use of error-correction codes for quantum sensing',
            'Developing tighter bounds and strategies towards achieving them in many-body sensors require closer '
            'connections between quantum metrology and control theory.'],
  'raw_file': 'frontier/phys/f9_montenegro_manybody_review_arXiv2408.15323v3.txt',
  'note': 'Proposals: error-correction codes; control theory; (also criticality and non-equilibrium probes, in the '
          'same outlook).',
  'id': 'phys:11'},
 {'domain': 'F9',
  'kind': 'DIRECTION',
  'source': 'Montenegro et al., Review: Quantum Metrology and Sensing with Many-Body Systems, Phys. Rep. (2025), DOI '
            '10.1016/j.physrep.2025.05.005',
  'version': 'arXiv:2408.15323v3 (7 Jun 2025)',
  'url': 'https://arxiv.org/html/2408.15323v3',
  'quote': ['Gauging the precision of parameter estimation through the quantum Cramér-Rao bound is undoubtedly the '
            'most popular approach in the literature, thanks to its geometrical properties and its utility as a '
            'signature of multipartite entanglement.',
            'Firstly, although this bound is asymptotically tight for single parameter estimation, it may perform '
            'quite poorly in the non-asymptotic regime and especially if the likelihood function is highly '
            'non-Gaussian.'],
  'raw_file': 'frontier/phys/f9_montenegro_manybody_review_arXiv2408.15323v3.txt',
  'note': 'DIRECTION-NAMED: QFI / quantum Cramér-Rao bound is the standard figure of merit; the review also names its '
          'non-asymptotic limitation (Ziv-Zakai, Bayesian alternatives).',
  'id': 'phys:12'},
 {'domain': 'F9',
  'kind': 'BOTTLENECK',
  'source': 'Konar et al., Journey in quantum metrology and sensing from foundations to applications: a review',
  'version': 'arXiv:2605.21702v2 (25 May 2026)',
  'url': 'https://arxiv.org/html/2605.21702v2',
  'quote': ['In particular, we have limited understanding as yet of the resources necessary for attaining the best '
            'precision allowed by quantum mechanics.',
            'Noisy environments also pose a significant challenges, both with respect to modeling the relevant '
            'environment for a given physical platform and for finding the optimal sensing strategy under realistic '
            'noisy condition.',
            'While ideal noiseless quantum metrology predicts Heisenberg limit for suitably entangled probes of size N '
            ', decoherence typically degrades this enhancement and restores the standard quantum limit'],
  'raw_file': 'frontier/phys/f9_konar2026_journey_review_arXiv2605.21702v2.txt',
  'note': 'Bottleneck: Heisenberg scaling lost under noise; resources for optimal precision unclear.',
  'id': 'phys:13'},
 {'domain': 'F9',
  'kind': 'PROPOSAL',
  'source': 'Konar et al., Journey in quantum metrology and sensing from foundations to applications: a review',
  'version': 'arXiv:2605.21702v2 (25 May 2026)',
  'url': 'https://arxiv.org/html/2605.21702v2',
  'quote': ['Heisenberg-limited scaling can still be restored using quantum error correction or adaptive protocols',
            'known as HNLS (Hamiltonian-not-in-Lindblad span) condition'],
  'raw_file': 'frontier/phys/f9_konar2026_journey_review_arXiv2605.21702v2.txt',
  'note': 'Proposal: QEC / adaptive protocols under the HNLS condition.',
  'id': 'phys:14'},
 {'domain': 'F9',
  'kind': 'DIRECTION',
  'source': 'Konar et al., Journey in quantum metrology and sensing from foundations to applications: a review',
  'version': 'arXiv:2605.21702v2 (25 May 2026)',
  'url': 'https://arxiv.org/html/2605.21702v2',
  'quote': ['The QFI quantifies how rapidly a quantum state changes under an infinitesimal variation of an encoded '
            'parameter and hence it measures the distinguishability between neighboring quantum states and its inverse '
            'determines the ultimate precision bound for a parameter encoded in a quantum system.',
            'We then systematically describe the quantum Cramér-Rao bound across various encoding processes, including '
            'unitary evolution, quantum channels, and indefinite causal order of maps.'],
  'raw_file': 'frontier/phys/f9_konar2026_journey_review_arXiv2605.21702v2.txt',
  'note': "DIRECTION-NAMED: QFI as distinguishability of neighbouring states (the probe's own resolvable step) and the "
          'QCRB as the bound.',
  'id': 'phys:15'},
 {'domain': 'F10',
  'kind': 'BOTTLENECK',
  'source': 'Korbel, Kolchinsky, Loos et al., Quo vadis, stochastic thermodynamics? (Perspective), DOI '
            '10.1515/jnet-2026-0051',
  'version': 'arXiv:2604.26601v2 (4 Sep 2026)',
  'url': 'https://arxiv.org/html/2604.26601v2',
  'quote': ['In particular, it remains unclear how to construct geometric frameworks that faithfully capture realistic '
            'optimal control problems beyond idealized settings.',
            'More broadly, these efforts point toward a deeper question: to what extent is dissipation fundamentally '
            'geometric?',
            'Extensions to the aforementioned non-Markovian dynamics and mixed conservative–dissipative systems also '
            'remain largely unexplored.'],
  'raw_file': 'frontier/phys/f10_quovadis_stochthermo_arXiv2604.26601v2.txt',
  'note': 'Bottleneck: which geometry governs dissipation beyond idealised (overdamped, linear-response) settings.',
  'id': 'phys:16'},
 {'domain': 'F10',
  'kind': 'PROPOSAL',
  'source': 'Korbel, Kolchinsky, Loos et al., Quo vadis, stochastic thermodynamics? (Perspective), DOI '
            '10.1515/jnet-2026-0051',
  'version': 'arXiv:2604.26601v2 (4 Sep 2026)',
  'url': 'https://arxiv.org/html/2604.26601v2',
  'quote': ['The first generalizes the Wasserstein-2 structure by introducing Onsager-type operators that relate '
            'thermodynamic forces to fluxes',
            'However, it typically assumes fixed linear-response structures that may not be realistic far from '
            'equilibrium.',
            'The second approach abandons the strict Riemannian structure and instead defines generalized '
            'Wasserstein-1 geometries based on constraints on dynamical activity or related quantities',
            'Connections to large deviation theory and classical problems such as the Schrödinger bridge are expected '
            'to play an important role in this direction.'],
  'raw_file': 'frontier/phys/f10_quovadis_stochthermo_arXiv2604.26601v2.txt',
  'note': 'Proposals: Onsager-operator W2 generalisations; W1 activity geometries; large deviations / Schrödinger '
          'bridge.',
  'id': 'phys:17'},
 {'domain': 'F10',
  'kind': 'DIRECTION',
  'source': 'Korbel, Kolchinsky, Loos et al., Quo vadis, stochastic thermodynamics? (Perspective), DOI '
            '10.1515/jnet-2026-0051',
  'version': 'arXiv:2604.26601v2 (4 Sep 2026)',
  'url': 'https://arxiv.org/html/2604.26601v2',
  'quote': ['For overdamped Langevin systems with constant diffusivity, the entropy produced along a stochastic '
            'trajectory coincides with the optimal transport cost of redistribution',
            'This geometric picture extends to the linear-response regime, where thermodynamic length quantifies '
            'dissipation during slow transformations, and geodesics prescribe optimal protocols'],
  'raw_file': 'frontier/phys/f10_quovadis_stochthermo_arXiv2604.26601v2.txt',
  'note': 'DIRECTION-NAMED: the dissipation metric is Wasserstein-2 (optimal transport) / thermodynamic length; the '
          'Fisher metric is not named as the dissipation metric here.',
  'id': 'phys:18'},
 {'domain': 'F10',
  'kind': 'BOTTLENECK',
  'source': 'Blaber & Sivak, Optimal Control in Stochastic Thermodynamics (review), J. Phys. Commun. (2023), DOI '
            '10.1088/2399-6528/acbf04',
  'version': 'arXiv:2212.00706v2 (11 Apr 2023)',
  'url': 'https://arxiv.org/html/2212.00706v2',
  'quote': ['Beyond simply the number of control parameters, it remains an open question as to which control '
            'parameters are the most important when designing protocols to minimize dissipation.'],
  'raw_file': 'frontier/phys/f10_blaber_sivak_optimalcontrol_arXiv2212.00706v2.txt',
  'note': 'Bottleneck: choice of control parameters.',
  'id': 'phys:19'},
 {'domain': 'F10',
  'kind': 'PROPOSAL',
  'source': 'Blaber & Sivak, Optimal Control in Stochastic Thermodynamics (review), J. Phys. Commun. (2023), DOI '
            '10.1088/2399-6528/acbf04',
  'version': 'arXiv:2212.00706v2 (11 Apr 2023)',
  'url': 'https://arxiv.org/html/2212.00706v2',
  'quote': ['A promising area of future study would be to explore if extensions and generalizations can be made to '
            'strong and fast control.',
            'For fast driving, the minimum-dissipation protocols determined from linear-response theory have jumps at '
            'the start and end of the protocol.'],
  'raw_file': 'frontier/phys/f10_blaber_sivak_optimalcontrol_arXiv2212.00706v2.txt',
  'note': 'Proposals: interpolate slow/fast and weak/strong approximations.',
  'id': 'phys:20'},
 {'domain': 'F10',
  'kind': 'DIRECTION',
  'source': 'Blaber & Sivak, Optimal Control in Stochastic Thermodynamics (review), J. Phys. Commun. (2023), DOI '
            '10.1088/2399-6528/acbf04',
  'version': 'arXiv:2212.00706v2 (11 Apr 2023)',
  'url': 'https://arxiv.org/html/2212.00706v2',
  'quote': ['The generalized friction tensor endows the space of thermodynamic states with a Riemannian metric where '
            'minimum-dissipation protocols correspond to geodesics of the friction tensor.'],
  'raw_file': 'frontier/phys/f10_blaber_sivak_optimalcontrol_arXiv2212.00706v2.txt',
  'note': 'DIRECTION-NAMED: the metric is the friction tensor.',
  'id': 'phys:21'},
 {'domain': 'F10',
  'kind': 'BOTTLENECK',
  'source': 'Zhong & DeWeese, Beyond Linear Response: Equivalence between Thermodynamic Geometry and Optimal '
            'Transport, PRL 133, 057102 (2024), DOI 10.1103/PhysRevLett.133.057102',
  'version': 'arXiv:2404.01286v4 (26 Apr 2024)',
  'url': 'https://arxiv.org/html/2404.01286v4',
  'quote': ['While this geometric framework is both mathematically elegant and computationally tractable, geodesic '
            'protocols are fundamentally approximate; their performance often degrades for sufficiently small protocol '
            'times, in some cases performing even worse than a linear interpolation protocol'],
  'raw_file': 'frontier/phys/f10_zhong_deweese_beyondLR_arXiv2404.01286v4.txt',
  'note': 'Bottleneck: friction-tensor geodesics fail far from linear response.',
  'id': 'phys:22'},
 {'domain': 'F10',
  'kind': 'DIRECTION',
  'source': 'Zhong & DeWeese, Beyond Linear Response: Equivalence between Thermodynamic Geometry and Optimal '
            'Transport, PRL 133, 057102 (2024), DOI 10.1103/PhysRevLett.133.057102',
  'version': 'arXiv:2404.01286v4 (26 Apr 2024)',
  'url': 'https://arxiv.org/html/2404.01286v4',
  'quote': ['We show that obtaining optimal protocols past the slow-driving or linear response regime is '
            'computationally tractable as the sum of a friction tensor geodesic and a counterdiabatic term related to '
            'the Fisher information metric.',
            'Here we derive an even stronger result, that thermodynamic geometry is in fact equivalent to optimal '
            'transport geometry, in the sense that the friction tensor and the Benamou-Brenier problem restricted to '
            'equilibrium distributions parameterized by \\lambda have identical geodesics and geodesic distances.'],
  'raw_file': 'frontier/phys/f10_zhong_deweese_beyondLR_arXiv2404.01286v4.txt',
  'note': 'DIRECTION-NAMED: beyond linear response, the geodesic is of the friction tensor (= OT geometry); the Fisher '
          'information metric enters only the counterdiabatic term.',
  'id': 'phys:23'},
 {'domain': 'F10',
  'kind': 'DIRECTION',
  'source': 'Sivak & Crooks, Thermodynamic metrics and optimal paths, PRL 108, 190602 (2012), DOI '
            '10.1103/PhysRevLett.108.190602 (targeted search; pre-2024 original)',
  'version': 'arXiv:1201.4166v2 (8 May 2012)',
  'url': 'https://arxiv.org/pdf/1201.4166',
  'quote': ['we derive a friction tensor that induces a Riemannian manifold on the space of thermodynamic',
            'When the relaxation time does not vary with the control parameter, the Riemannian metric reduces to the '
            'Fisher information metric [26]'],
  'raw_file': 'frontier/phys/f10_sivak_crooks2012_thermo_metrics_arXiv1201.4166.txt',
  'note': 'DIRECTION-NAMED (targeted search): friction tensor = relaxation time x Fisher information; equals the '
          'Fisher metric only when relaxation time is constant.',
  'id': 'phys:24'},
 {'domain': 'F11',
  'kind': 'BOTTLENECK',
  'source': 'Hodson, Mehta, Smith, The empirical status of predictive coding and active inference, Neurosci. Biobehav. '
            'Rev. (2024), DOI 10.1016/j.neubiorev.2023.105473',
  'version': 'abstract only (Europe PMC, PMID 38030100; full text 403/paywalled)',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:38030100%20AND%20SRC:MED&format=json&resultType=core',
  'quote': ['While Active Inference models tend to explain behavioral data reasonably well, there has not been a focus '
            'on testing empirical validity of active inference theory per se, which would require formal comparison to '
            'other models (e.g., non-Bayesian or model-free reinforcement learning models).'],
  'raw_file': 'frontier/phys/f11_hodson2024_empirical_status_abstract_PMID38030100.txt',
  'note': 'Bottleneck: empirical validity untested against alternatives.',
  'id': 'phys:25'},
 {'domain': 'F11',
  'kind': 'BOTTLENECK',
  'source': 'Lageman, Fahrenfort, Slagter, Prediction in action: Toward an empirical science of active inference, '
            'Neurosci. Biobehav. Rev. (2026), DOI 10.1016/j.neubiorev.2026.106817',
  'version': 'abstract only (Europe PMC, PMID 42285188, first published 2026-06-13; ScienceDirect 403)',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:42285188%20AND%20SRC:MED&format=json&resultType=core',
  'quote': ['Despite its growing prominence, the framework is often criticized for the difficulty of extracting '
            'qualitatively distinct, testable predictions and its limited empirical grounding.',
            'We highlight areas where evidence is promising, while emphasizing the need for theory-driven experiments '
            'that can adjudicate between accounts.'],
  'raw_file': 'frontier/phys/f11_lageman2026_prediction_in_action_abstract_PMID42285188.txt',
  'note': 'Bottleneck: distinct testable predictions.',
  'id': 'phys:26'},
 {'domain': 'F11',
  'kind': 'PROPOSAL',
  'source': 'Lageman, Fahrenfort, Slagter, Prediction in action: Toward an empirical science of active inference, '
            'Neurosci. Biobehav. Rev. (2026), DOI 10.1016/j.neubiorev.2026.106817',
  'version': 'abstract only (Europe PMC, PMID 42285188, first published 2026-06-13; ScienceDirect 403)',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:42285188%20AND%20SRC:MED&format=json&resultType=core',
  'quote': ['In the domain of decision-making, we identify predictions that agents behave more stochastically when '
            'they are uncertain about outcome predictions; that they explore to resolve uncertainty about hidden '
            'states and model parameters; and that preferences can be learned through accumulated experience.'],
  'raw_file': 'frontier/phys/f11_lageman2026_prediction_in_action_abstract_PMID42285188.txt',
  'note': 'Proposal: named testable predictions in decision-making and motor control.',
  'id': 'phys:27'},
 {'domain': 'F11',
  'kind': 'BOTTLENECK',
  'source': 'Badcock & Davey, Active Inference in Psychology and Psychiatry: Progress to Date?, Entropy 26(10):833 '
            '(2024), DOI 10.3390/e26100833',
  'version': 'PMC11507080 (first published 2024-09-30)',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11507080/fullTextXML',
  'quote': ['Meanwhile, the main outstanding question is whether this theory will make a positive difference through '
            'applications in clinical psychology, and its sister discipline of psychiatry.',
            'Despite its unique explanatory promise, without further empirical progress in this area, the extent to '
            'which active inference adds meaningfully to what we already know about depression remains to be seen.'],
  'raw_file': 'frontier/phys/f11_badcock_davey2024_actinf_psychiatry_PMC11507080.txt',
  'note': 'Bottleneck: whether active inference adds to existing accounts.',
  'id': 'phys:28'},
 {'domain': 'F11',
  'kind': 'DIRECTION',
  'source': 'Badcock & Davey, Active Inference in Psychology and Psychiatry: Progress to Date?, Entropy 26(10):833 '
            '(2024), DOI 10.3390/e26100833',
  'version': 'PMC11507080 (first published 2024-09-30)',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11507080/fullTextXML',
  'quote': ['Prediction errors are also weighted by their precision , which relates to the reliability afforded to '
            'various beliefs or sources of sensory evidence, and involves neuromodulatory mechanisms (e.g., affecting '
            'attentional selection) that determine the relative influence of ascending (error) vs. descending '
            '(representation) signals on belief-updating',
            'This will occur according to the degree of confidence in one’s generative models, and corresponds '
            'psychologically to the selective attention or sensory attenuation of evidence for one’s Bayesian beliefs.',
            'The second process, which relates to learning and attention , optimises synaptic strength and efficiency '
            'over seconds to hours to encode the precision of prediction errors and the causal structure of the '
            'environment in the sensorium.'],
  'raw_file': 'frontier/phys/f11_badcock_davey2024_actinf_psychiatry_PMC11507080.txt',
  'note': 'DIRECTION-NAMED: precision equated with attention (selective attention / attentional selection) and a '
          "timescale (seconds to hours) for precision learning; stated as the framework's account, not as an open "
          'problem.',
  'id': 'phys:29'},
 {'domain': 'F11',
  'kind': 'PROPOSAL',
  'source': 'Pezzulo, Parr, Friston, Active inference as a theory of sentient behavior, Biol. Psychol. (2024), DOI '
            '10.1016/j.biopsycho.2023.108741',
  'version': 'abstract only (Europe PMC, PMID 38182015; CC BY but ScienceDirect returned 403)',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:38182015%20AND%20SRC:MED&format=json&resultType=core',
  'quote': ['Active inference has been used to account for aspects of anatomy and neurophysiology, to offer theories '
            'of psychopathology in terms of aberrant precision control, and to unify extant psychological theories.',
            'Key steps in this development include the formulation of predictive coding models and related theories of '
            'neuronal message passing, the use of sequential models for planning and policy optimization, and the '
            'importance of hierarchical (temporally) deep internal (i.e., generative or world) models.'],
  'raw_file': 'frontier/phys/f11_pezzulo2024_sentient_abstract_PMID38182015.txt',
  'note': 'Proposals (abstract only): aberrant precision control; temporally deep hierarchical models.',
  'id': 'phys:30'},
 {'domain': 'F11',
  'kind': 'DIRECTION',
  'source': 'Proietti, Parr, Tessari, Friston, Pezzulo, Active inference and cognitive control: Balancing deliberation '
            'and habits through precision optimization (Review), Phys. Life Rev. (2025), DOI '
            '10.1016/j.plrev.2025.05.008',
  'version': 'published version PDF, institutional repository (available online 16 May 2025)',
  'url': 'https://cris.unibo.it/retrieve/4f0ef4b4-b5f4-462d-8fe3-6e4fd3b7104b/Physic%20of%20life%20reviews%202025.pdf',
  'quote': ['The theory proposes that cognitive control amounts to optimising a precision parameter, which acts as a '
            'control signal and balances the contributions of deliberative and habitual components of action '
            'selection.',
            'This novel expected (indicated by bold) precision parameter γ’ plays the role of a control signal [140] '
            'and of attentional resources [31,138] and its main role is to prioritize deliberative components of '
            'action selection, when useful.'],
  'raw_file': 'frontier/phys/f11_pezzulo2025_plr_cognitive_control_unibo.txt',
  'note': 'DIRECTION-NAMED: precision as control signal and attentional resource (proposal, 2025 review).',
  'id': 'phys:31'},
 {'domain': 'F11',
  'kind': 'BOTTLENECK',
  'source': 'Proietti, Parr, Tessari, Friston, Pezzulo, Active inference and cognitive control: Balancing deliberation '
            'and habits through precision optimization (Review), Phys. Life Rev. (2025), DOI '
            '10.1016/j.plrev.2025.05.008',
  'version': 'published version PDF, institutional repository (available online 16 May 2025)',
  'url': 'https://cris.unibo.it/retrieve/4f0ef4b4-b5f4-462d-8fe3-6e4fd3b7104b/Physic%20of%20life%20reviews%202025.pdf',
  'quote': ['Our simulations show that a standard active inference model can form adaptive habits; i.e., can pass from '
            'deliberative to habitual control when the context is stable, but generally fails to revert to '
            'deliberative control, when the context changes.',
            'Reconciling these and other alternative proposals is an open objective for future studies.'],
  'raw_file': 'frontier/phys/f11_pezzulo2025_plr_cognitive_control_unibo.txt',
  'note': 'Bottleneck: context-sensitivity of precision control; reconciling neurobiological proposals.',
  'id': 'phys:32'},
 {'domain': 'F11',
  'kind': 'DIRECTION',
  'source': 'Klar, Stein, Paterson, Williamson, Gollee, Murray-Smith, Intermittent Active Inference, Entropy 28(3):269 '
            '(2026), DOI 10.3390/e28030269 (targeted search; research article)',
  'version': 'PMC13024937 (first published 2026-02-28)',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13024937/fullTextXML',
  'quote': ['Whilst standard formulations assume continuous inference and control, empirical evidence indicates that '
            'humans update their control strategies intermittently, which reduces computational demands and mitigates '
            'propagation of correlated noise in closed feedback loops.',
            'This paper investigates intermittent planning, where IAIF agents follow their current plan and only '
            're-plan when the prediction error exceeds a predefined threshold or the Expected Free Energy associated '
            'with the current plan surpasses prior estimates.'],
  'raw_file': 'frontier/phys/f11_intermittent_actinf2026_PMC13024937.txt',
  'note': 'DIRECTION-NAMED (targeted search): the clock of belief updating (continuous vs event-triggered) is posed '
          'and an event-triggered variant proposed.',
  'id': 'phys:33'},
 {'domain': 'F11',
  'kind': 'DIRECTION',
  'source': 'Harris & Arthur, Hidden State Inference or Continuous Belief Updating during a Dynamic Visuomotor Skill, '
            'J. Neurosci. 46 (2026), DOI 10.1523/JNEUROSCI.1285-25.2025 (targeted search; research article)',
  'version': 'PMC12873645 (first published 2026-02-04)',
  'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12873645/fullTextXML',
  'quote': ['Here, we test whether behavior in a naturalistic interception task is better explained by continuous '
            'belief updating or by more abrupt shifts driven by state inference, consistent with hierarchical Bayesian '
            'learning.',
            'However, the neurocomputational mechanisms through which higher-level beliefs shape moment-to-moment '
            'perception and action behaviors remains unclear.'],
  'raw_file': 'frontier/phys/f11_belief_updating_visuomotor_PMC12873645.txt',
  'note': 'DIRECTION-NAMED (targeted search): continuous vs discrete belief updating tested empirically (continuous '
          'won in that task).',
  'id': 'phys:34'}]

READINGS = [{'domain': 'F1',
  'name': 'continual learning and loss of plasticity in AI',
  'reading': 'COMPATIBLE-P',
  'principle': 'P-IG, P-EWMA',
  'direction_named': True,
  'measurable_h1': False,
  'bottleneck_claims': ['f1:0'],
  'direction_claims': ['f1:1', 'f1:2'],
  'note': "the Fisher-weighted anchor (EWC) and its geometric decay (online EWC) are the field's own; SEC, the one "
          'PASS-0 line (SCL3), is not a CRR rule',
  'h0_claims': []},
 {'domain': 'F2a',
  'name': 'cell cycle: replication initiation at a fixed phase of the growth-division rotor',
  'reading': 'COMPATIBLE-P',
  'principle': 'P-TR, P-PHASE',
  'direction_named': False,
  'measurable_h1': True,
  'bottleneck_claims': ['life:2', 'life:4', 'life:7'],
  'direction_claims': [],
  'note': 'not named in 7 fetched texts plus one search; the field frames initiation at a fixed mass per origin '
          '(quoted); H1 (antipode) separates from H0 (initiation adder) on the open gate G-CD3; the investigator '
          'forecasts FAIL on real lineages (Life_Sciences); GUIDES means a lab candidate (L01), not help',
  'h0_claims': ['life:6', 'life:8']},
 {'domain': 'F2b',
  'name': 'cell cycle: a lag-2 (grandmother) memory in birth size',
  'reading': 'COMPATIBLE-P',
  'principle': 'P-MEM',
  'direction_named': True,
  'measurable_h1': False,
  'bottleneck_claims': ['life:0'],
  'direction_claims': ['life:9', 'life:10'],
  'note': 'named and tested (Zhang, Fei & Dunkel 2025): for E. coli the grandmother term did not improve the fit, so '
          'the direction is named and currently disfavoured',
  'h0_claims': []},
 {'domain': 'F3',
  'name': 'epidemic forecasting with behavioural feedback',
  'reading': 'COMPATIBLE-P',
  'principle': 'P-MEM',
  'direction_named': True,
  'measurable_h1': False,
  'bottleneck_claims': ['cx:10', 'cx:0'],
  'direction_claims': ['cx:13', 'cx:17'],
  'note': 'exponential-decay memory of prevalence is fitted (Mao et al. 2026) and wave period set by the memory kernel '
          'is shown; counterpoint: cycles without an imposed kernel (cx:20); open: identifiability of the memory '
          'strength (cx:14)',
  'h0_claims': []},
 {'domain': 'F4',
  'name': 'macroeconomic inflation expectations',
  'reading': 'COMPATIBLE-P',
  'principle': 'P-EWMA, P-MEM',
  'direction_named': True,
  'measurable_h1': False,
  'bottleneck_claims': ['cx:21', 'cx:28'],
  'direction_claims': ['cx:27', 'cx:38'],
  'note': 'the time-discounted experience average and constant-gain learning are the stated conventional wisdom; the '
          '2021-23 de-anchoring is posed AGAINST them (cx:28), with selective recall by similarity proposed instead: '
          "the frontier has moved past CRR's direction",
  'h0_claims': []},
 {'domain': 'F5',
  'name': 'traffic flow and automated-vehicle string stability',
  'reading': 'COMPATIBLE-P',
  'principle': 'P-MEM',
  'direction_named': True,
  'measurable_h1': False,
  'bottleneck_claims': ['cx:41', 'cx:51'],
  'direction_claims': ['cx:53', 'cx:44'],
  'note': 'distributed-delay driver memory (Sipahi & Niculescu) and IDM with memory are named; a 25-car platoon '
          'experiment found reaction delay negligible for fluctuation growth (cx:46)',
  'h0_claims': []},
 {'domain': 'F6',
  'name': 'early-warning signals of critical transitions',
  'reading': 'COMPATIBLE-P',
  'principle': 'P-IG',
  'direction_named': True,
  'measurable_h1': False,
  'bottleneck_claims': ['cx:55', 'cx:56'],
  'direction_claims': ['cx:65', 'cx:60'],
  'note': 'Fisher information as a regime-shift indicator is named since 2008 and listed in the 2024 review; the '
          'second half (distance to tipping in distinguishable steps) was not found (cx:69) but needs the unknown '
          'tipping point, so it gives no H1 separable from Fisher-information EWS',
  'h0_claims': []},
 {'domain': 'F7',
  'name': 'memory consolidation and forgetting',
  'reading': 'COMPATIBLE-P',
  'principle': 'P-TR, P-MEM',
  'direction_named': True,
  'measurable_h1': False,
  'bottleneck_claims': ['life:12', 'life:14'],
  'direction_claims': ['life:19', 'life:21', 'life:22'],
  'note': "forgetting counted in interfering events (Georgiou, Katkov & Tsodyks), Jost's law from interference "
          "weakening with age (Wixted 2004) and the decay-vs-competitors question (2026) are all named: lab L04's edge "
          "is the field's own question",
  'h0_claims': []},
 {'domain': 'F8',
  'name': 'earthquake and aftershock forecasting',
  'reading': 'COMPATIBLE-P',
  'principle': 'P-TR',
  'direction_named': True,
  'measurable_h1': False,
  'bottleneck_claims': ['phys:2', 'phys:4'],
  'direction_claims': ['phys:6', 'phys:9'],
  'note': 'time-rescaling residual analysis and event-count natural time are named; the bottleneck (neural point '
          'processes do not beat ETAS) is outside what CRR supplies',
  'h0_claims': []},
 {'domain': 'F9',
  'name': 'quantum metrology and sensing',
  'reading': 'COMPATIBLE-P',
  'principle': 'P-IG',
  'direction_named': True,
  'measurable_h1': False,
  'bottleneck_claims': ['phys:10', 'phys:13'],
  'direction_claims': ['phys:12', 'phys:15'],
  'note': "the quantum Cramer-Rao bound and QFI as distinguishability are the field's standard; the bottlenecks "
          '(noise, robustness, multiparameter bounds) get no direction from CRR',
  'h0_claims': []},
 {'domain': 'F10',
  'name': 'stochastic thermodynamics: minimal-dissipation protocols',
  'reading': 'CONFLICT-W',
  'principle': 'W-METRIC',
  'direction_named': True,
  'measurable_h1': False,
  'bottleneck_claims': ['phys:16', 'phys:22'],
  'direction_claims': ['phys:21', 'phys:24'],
  'note': 'the dissipation metric is the friction tensor (Wasserstein-type beyond), not Fisher at one global scale; '
          "CRR's three WRONG trap rows are the same finding",
  'h0_claims': []},
 {'domain': 'F11',
  'name': 'active inference and the FEP as a theory of cognition',
  'reading': 'CONFLICT-W',
  'principle': 'W-FEP, W-CLOCK',
  'direction_named': True,
  'measurable_h1': False,
  'bottleneck_claims': ['phys:25', 'phys:26'],
  'direction_claims': ['phys:29', 'phys:31', 'phys:33'],
  'note': 'precision as attention and the continuous-vs-event clock of belief updating are posed by the field itself; '
          "CRR's readings here were WRONG in batches 27-28",
  'h0_claims': []},
 {'domain': 'F12',
  'name': 'circadian medicine and chronotherapy',
  'reading': 'COMPATIBLE-P',
  'principle': 'P-PHASE',
  'direction_named': True,
  'measurable_h1': False,
  'bottleneck_claims': ['life:24', 'life:28'],
  'direction_claims': ['life:32'],
  'note': 'advance/delay PRC areas setting entrainment are named (Uriu & Tei 2021); the bottlenecks (shift-work '
          'resistance, individual internal time, phase estimation) get no direction from CRR',
  'h0_claims': []}]
