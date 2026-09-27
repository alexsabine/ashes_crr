# Sources checked on the day (R10): frontier domains F8–F11 (earthquake forecasting, quantum metrology, stochastic thermodynamics, active inference), for labs/frontier/DECLARATION.md, 2026-09-27

A note, not evidence (R8). Quotes are verbatim substrings of the saved texts.

- **The request.** Prompt-log entry 226, through `labs/frontier/DECLARATION.md`, which was pushed before any fetch. This dossier covers F8–F11 only. F1 (continual learning) reuses the existing dossiers of 2026-09-23 and 2026-09-25, and nothing was fetched for it here.
- **Saved texts.** The raw texts are in the session scratchpad, `/tmp/claude-0/-home-user-ashes-crr/77fb7a2b-ce3d-5c52-a1a6-710031fa20e9/scratchpad/frontier/phys/`. The per-URL HTTP log is `FETCH_LOG.txt` in the same folder. The claims file is `frontier/phys_claims.json`, with one record per quoted group. The scratchpad is not committed. A reader who needs the texts must re-fetch them from the URLs given here.
- **How the texts were made.** arXiv HTML and Europe PMC JATS XML were converted to plain text with a small tag-stripping script (`frontier/html2txt.py`). That script replaces LaTeXML math with its `alttext`. PDFs were converted with `pypdfium2`. PDF artefacts are kept verbatim inside quotes, for example U+2010 hyphens in the Mizrahi PDF.
- **How quotes were checked.** A quote was counted as verified if, after every run of whitespace was collapsed to one space, it was a substring of its saved text. The check is `frontier/build_phys_claims.py`. Result: 71 of 71 quotes verified, in 35 claim records.
- **The tags.** [BOTTLENECK] is a stated open question or bottleneck. [PROPOSAL] is a leading approach the source names. [DIRECTION-NAMED] means the declaration's "CRR's suggested direction" is already named in the source. [DIRECTION-NOT-FOUND-IN-FETCHED] records what was searched and not found.
- **What this note does not do.** It assigns no COMPATIBLE-P, CONFLICT-W or OUTSIDE reading and no label: `labs/frontier/checks/grade.py` does that. It states no novelty. "Not found in the fetched texts" is never read as "novel" (the declaration's rule).

---

## F8. Earthquake and aftershock forecasting (beyond ETAS, ML catalogues, natural time)

**The declaration's direction for F8.** natural time (event-count or compensator time) and time-rescaling residual analysis (Ogata; Varotsos natural time).

### Sources

- **Zhuang & Sornette, How to quantify earthquake predictability? Advances in earthquake forecasting and predictability limits**
  - Version: arXiv:2607.26918v1 (29 Jul 2026)
  - URL: https://arxiv.org/html/2607.26918v1
  - Fetch: HTTP 200 (arXiv HTML)
  - Raw file: `f8_sornette2026_predictability_arXiv2607.26918v1.txt`
- **Stockman et al., EarthquakeNPP: A Benchmark for Earthquake Forecasting with Neural Point Processes**
  - Version: arXiv:2410.08226v3 (10 Mar 2026)
  - URL: https://arxiv.org/html/2410.08226v3
  - Fetch: HTTP 200 (arXiv HTML)
  - Raw file: `f8_stockman_earthquakeNPP_arXiv2410.08226v3.txt`
- **Mizrahi et al., Developing, Testing, and Communicating Earthquake Forecasts: Current Practices and Future Directions, Rev. Geophys. 62(3) (2024), DOI 10.1029/2023RG000823**
  - Version: published version, author-hosted PDF (downloaded 13/08/2024 per PDF footer)
  - URL: http://wpage.unina.it/iuniervo/papers/Mizrahi_et_al_Reviews_of_Geophysics_2024.pdf
  - Fetch: HTTP 200 (author-hosted PDF, converted with pypdfium2); Wiley full text returned 403
  - Raw file: `f8_mizrahi2024_revgeophys_unina.txt`
- **Wen et al., Integrating Artificial Intelligence and Geophysical Insights for Earthquake Forecasting: A Cross-Disciplinary Review**
  - Version: arXiv:2502.12161v1 (10 Feb 2025)
  - URL: https://arxiv.org/html/2502.12161v1
  - Fetch: HTTP 200 (arXiv HTML)
  - Raw file: `f8_wen2025_ai_eq_review_arXiv2502.12161v1.txt`
- **Rundle, Baughman, Donnellan, Grant, Fox, From Local Earthquake Nowcasting to Natural Time Forecasting: A Simple Do-It-Yourself (DIY) Method (targeted search; research article, not a review)**
  - Version: arXiv:2510.02467v2 (16 Oct 2025)
  - URL: https://arxiv.org/pdf/2510.02467v2
  - Fetch: HTTP 200 (arXiv PDF, pypdfium2); arXiv HTML returned 404
  - Raw file: `f8_rundle2025_natural_time_DIY_arXiv2510.02467v2.txt`

### Quotes

[BOTTLENECK] **Zhuang & Sornette (arXiv:2607.26918v1).** Open question: how much predictability exists, and whether model skill is bounded by it.

> However, it remains unclear whether the forecasting performance of a model, quantified by the likelihood ratio against a model of complete randomness, is necessarily bounded by the intrinsic predictability capacity of the forecasting model itself.

> Taken together, these considerations indicate that earthquake forecasting remains an active and scientifically challenging field in which both progress and fundamental limitations must be carefully assessed.

[BOTTLENECK] **Stockman et al. (arXiv:2410.08226v3).** Bottleneck: ML (neural point processes) does not yet beat ETAS; catalogue incompleteness.

> Benchmarking experiments, using both log-likelihood and generative evaluation metrics widely recognised in seismology, show that none of the five NPPs tested outperform ETAS.

> Data missingness, referred to in seismology as catalog (in)completeness, is the primary challenge faced with earthquake catalogs.

[BOTTLENECK] **Mizrahi et al. (published version, author-hosted PDF).** Bottlenecks: no standard ETAS benchmark; short-term incompleteness after large events.

> Because no two implementations of the model are identical, the earthquake forecasting community faces the challenge that a truly standardized benchmark version of the ETAS model is currently lacking.

> Incompleteness entailed by strong events is also not automatically corrected in the current version of the system; so far, corrections for incompleteness are applied by hand only immediately after a large earthquake.

[BOTTLENECK] **Wen et al. (arXiv:2502.12161v1).** Bottleneck: skill short of societal use; evaluation practice in ML papers.

> Despite decades of research, earthquake forecasting remains in an exploratory stage, with current methods still falling short of achieving performance levels that would provide meaningful benefits for society.

> Due to a lack of understanding of specialized knowledge in earthquake forecasting, researchers often focus solely on high scores from evaluation metrics and hastily claim the success of their models, overlooking the deeper principles of seismology and the challenges present in practical applications.

[PROPOSAL] **Zhuang & Sornette (arXiv:2607.26918v1).** Proposals: entropy-gap predictability; ETAS variants (gV-ETAS); utility-aware evaluation.

> This paper develops a unified information-theoretic framework to quantify predictability.

> Particularly, pseudo-prospective forecasting experiments have suggested that gV-ETAS models incorporating magnitude-dependent triggering may outperform the standard ETAS formulation

> Future work should therefore integrate information-theoretic measures of predictability with explicit utility or loss functions that reflect societal, economic, and safety priorities.

[PROPOSAL] **Stockman et al. (arXiv:2410.08226v3).** Proposal: neural point processes with large-magnitude triggering.

> Current NPP architectures struggle most in mainshock dominated regimes but show clear promise in modelling spatially complex background seismicity and swarm driven activity, motivating future work on incorporating large magnitude triggering while preserving this flexibility.

[PROPOSAL] **Mizrahi et al. (published version, author-hosted PDF).** Proposals: more physics; ML / neural point processes.

> (c) continued research on the development of superior forecasting models by including more information on earthquake physics, or by exploring alternative or complementary models for earthquake forecasting using machine learning (ML) techniques.

> Another noteworthy advantage of neural point process models is that they are extremely adaptive to nonstationarities in earthquake catalogs.

[PROPOSAL] **Wen et al. (arXiv:2502.12161v1).** Proposals: multi-source data; strong baselines.

> To overcome these limitations, there is a growing recognition of the need to integrate non-seismic and non-mechanical information into earthquake forecasting models.

> When we want to demonstrate that a newly developed model surpasses existing limitations, we should compare our model with the best current models, including both the best AI models and the most advanced geophysical or statistical seismological models.

[DIRECTION-NAMED] **Mizrahi et al. (published version, author-hosted PDF).** DIRECTION-NAMED: time-rescaling / residual analysis (transform to homogeneous Poisson = compensator time) is named as an existing test method, not yet routine in CSEP. Ogata (1988) residual analysis is cited in the reference lists of Mizrahi, Stockman, Zhuang-Sornette and Wen.

> Clements et al. (2011) also describe a series of residual analysis for point‐process methods, which consist of transforming the points of a simulated/observed catalog (e.g., by rescaling, thinning, superpositioning), such that the resulting transformed process should be homogeneous‐Poisson if the original model were consistent with the observations.

> Additional tests have been proposed in the literature, which do not depend on (pseudo‐) likelihood functions or have not been yet implemented in routine CSEP experiments.

[DIRECTION-NAMED] **Rundle (arXiv:2510.02467v2).** DIRECTION-NAMED (targeted search): event-count natural time is an existing forecasting method (Rundle et al. nowcasting line).

> We work in natural time, which is defined as the count of small earthquakes between large earthquakes.

> The probability is conditioned on the number of small earthquakes n(t) that have occurred since the last large earthquake.

### The direction search

The fetched texts were searched for: natural time, residual analys, transformed time, time rescal, rescaled time, compensator, random time change, Varotsos. Targeted web search: "natural time aftershock forecasting nowcasting Rundle 2024 2025 review event count time".

- [DIRECTION-NOT-FOUND-IN-FETCHED] **Varotsos natural time in the four reviews.** It is not named in Zhuang & Sornette, Mizrahi et al., Stockman et al. or Wen et al. Wen et al. cite Varotsos only for a geoelectric search engine (RASE). The only "rescaled time" in Wen et al. is the nearest-neighbour rescaled interval used for declustering, which is not natural time. The targeted search found event-count natural time named in Rundle et al. 2025 (quoted above).
- [DIRECTION-NOT-FOUND-IN-FETCHED] **The word "compensator".** It does not appear in any fetched F8 text. Ogata (1988), "Statistical models for earthquake occurrences and residual analysis for point processes", appears only in the reference lists of all four reviews. The rescaling or thinning residual method itself is named in Mizrahi et al. (quoted above).

---

## F9. Quantum metrology and sensing (Heisenberg scaling under noise)

**The declaration's direction for F9.** quantum Fisher information as the figure of merit, and the Cramér–Rao bound in the probe's own units.

### Sources

- **Montenegro et al., Review: Quantum Metrology and Sensing with Many-Body Systems, Phys. Rep. (2025), DOI 10.1016/j.physrep.2025.05.005**
  - Version: arXiv:2408.15323v3 (7 Jun 2025)
  - URL: https://arxiv.org/html/2408.15323v3
  - Fetch: HTTP 200 (arXiv HTML)
  - Raw file: `f9_montenegro_manybody_review_arXiv2408.15323v3.txt`
- **Konar et al., Journey in quantum metrology and sensing from foundations to applications: a review**
  - Version: arXiv:2605.21702v2 (25 May 2026)
  - URL: https://arxiv.org/html/2605.21702v2
  - Fetch: HTTP 200 (arXiv HTML)
  - Raw file: `f9_konar2026_journey_review_arXiv2605.21702v2.txt`

### Quotes

[BOTTLENECK] **Montenegro et al. (arXiv:2408.15323v3).** Bottlenecks: decoherence; robustness undefined; multiparameter CR bound not tight.

> Another problem which requires further investigation is the performance of quantum sensors under imperfect situations, such as the presence of decoherence

> the notion of robustness has not yet been formulated quantitatively for quantum sensors.

> Furthermore, a general issue for quantum sensors arise in the multi-parameter Cramér-Rao inequality as the bounds are not tight and thus saturating them may not be achievable

[BOTTLENECK] **Konar et al. (arXiv:2605.21702v2).** Bottleneck: Heisenberg scaling lost under noise; resources for optimal precision unclear.

> In particular, we have limited understanding as yet of the resources necessary for attaining the best precision allowed by quantum mechanics.

> Noisy environments also pose a significant challenges, both with respect to modeling the relevant environment for a given physical platform and for finding the optimal sensing strategy under realistic noisy condition.

> While ideal noiseless quantum metrology predicts Heisenberg limit for suitably entangled probes of size N , decoherence typically degrades this enhancement and restores the standard quantum limit

[PROPOSAL] **Montenegro et al. (arXiv:2408.15323v3).** Proposals: error-correction codes; control theory; (also criticality and non-equilibrium probes, in the same outlook).

> A related approach is the use of error-correction codes for quantum sensing

> Developing tighter bounds and strategies towards achieving them in many-body sensors require closer connections between quantum metrology and control theory.

[PROPOSAL] **Konar et al. (arXiv:2605.21702v2).** Proposal: QEC / adaptive protocols under the HNLS condition.

> Heisenberg-limited scaling can still be restored using quantum error correction or adaptive protocols

> known as HNLS (Hamiltonian-not-in-Lindblad span) condition

[DIRECTION-NAMED] **Montenegro et al. (arXiv:2408.15323v3).** DIRECTION-NAMED: QFI / quantum Cramér-Rao bound is the standard figure of merit; the review also names its non-asymptotic limitation (Ziv-Zakai, Bayesian alternatives).

> Gauging the precision of parameter estimation through the quantum Cramér-Rao bound is undoubtedly the most popular approach in the literature, thanks to its geometrical properties and its utility as a signature of multipartite entanglement.

> Firstly, although this bound is asymptotically tight for single parameter estimation, it may perform quite poorly in the non-asymptotic regime and especially if the likelihood function is highly non-Gaussian.

[DIRECTION-NAMED] **Konar et al. (arXiv:2605.21702v2).** DIRECTION-NAMED: QFI as distinguishability of neighbouring states (the probe's own resolvable step) and the QCRB as the bound.

> The QFI quantifies how rapidly a quantum state changes under an infinitesimal variation of an encoded parameter and hence it measures the distinguishability between neighboring quantum states and its inverse determines the ultimate precision bound for a parameter encoded in a quantum system.

> We then systematically describe the quantum Cramér-Rao bound across various encoding processes, including unitary evolution, quantum channels, and indefinite causal order of maps.

### The direction search

The fetched texts were searched for: quantum Fisher information, Cramér-Rao, statistical distance, distinguishab, Bures, own units, natural units, error correction, HNLS, Heisenberg. Targeted web search: "quantum Fisher information figure of merit noisy quantum metrology review 2025 Heisenberg scaling error correction perspective". It found no further source beyond the two reviews, and none was fetched.

- [DIRECTION-NOT-FOUND-IN-FETCHED] **The phrase "own units" or "natural units".** Neither phrase occurs in either F9 text. The idea is named in the reviews' own terms: the QFI as the distinguishability of neighbouring states, whose inverse sets the precision bound (Konar et al., quoted above).

---

## F10. Stochastic thermodynamics and optimal finite-time control (minimal dissipation beyond linear response)

**The declaration's direction for F10.** which metric governs minimal dissipation (the friction tensor or thermodynamic metric against the Fisher information metric); geodesic protocols; beyond linear response.

### Sources

- **Korbel, Kolchinsky, Loos et al., Quo vadis, stochastic thermodynamics? (Perspective), DOI 10.1515/jnet-2026-0051**
  - Version: arXiv:2604.26601v2 (4 Sep 2026)
  - URL: https://arxiv.org/html/2604.26601v2
  - Fetch: HTTP 200 (arXiv HTML)
  - Raw file: `f10_quovadis_stochthermo_arXiv2604.26601v2.txt`
- **Blaber & Sivak, Optimal Control in Stochastic Thermodynamics (review), J. Phys. Commun. (2023), DOI 10.1088/2399-6528/acbf04**
  - Version: arXiv:2212.00706v2 (11 Apr 2023)
  - URL: https://arxiv.org/html/2212.00706v2
  - Fetch: HTTP 200 (arXiv HTML)
  - Raw file: `f10_blaber_sivak_optimalcontrol_arXiv2212.00706v2.txt`
- **Zhong & DeWeese, Beyond Linear Response: Equivalence between Thermodynamic Geometry and Optimal Transport, PRL 133, 057102 (2024), DOI 10.1103/PhysRevLett.133.057102**
  - Version: arXiv:2404.01286v4 (26 Apr 2024)
  - URL: https://arxiv.org/html/2404.01286v4
  - Fetch: HTTP 200 (arXiv HTML)
  - Raw file: `f10_zhong_deweese_beyondLR_arXiv2404.01286v4.txt`
- **Sivak & Crooks, Thermodynamic metrics and optimal paths, PRL 108, 190602 (2012), DOI 10.1103/PhysRevLett.108.190602 (targeted search; pre-2024 original)**
  - Version: arXiv:1201.4166v2 (8 May 2012)
  - URL: https://arxiv.org/pdf/1201.4166
  - Fetch: HTTP 200 (arXiv PDF, pypdfium2)
  - Raw file: `f10_sivak_crooks2012_thermo_metrics_arXiv1201.4166.txt`

### Quotes

[BOTTLENECK] **Korbel (arXiv:2604.26601v2).** Bottleneck: which geometry governs dissipation beyond idealised (overdamped, linear-response) settings.

> In particular, it remains unclear how to construct geometric frameworks that faithfully capture realistic optimal control problems beyond idealized settings.

> More broadly, these efforts point toward a deeper question: to what extent is dissipation fundamentally geometric?

> Extensions to the aforementioned non-Markovian dynamics and mixed conservative–dissipative systems also remain largely unexplored.

[BOTTLENECK] **Blaber & Sivak (arXiv:2212.00706v2).** Bottleneck: choice of control parameters.

> Beyond simply the number of control parameters, it remains an open question as to which control parameters are the most important when designing protocols to minimize dissipation.

[BOTTLENECK] **Zhong & DeWeese (arXiv:2404.01286v4).** Bottleneck: friction-tensor geodesics fail far from linear response.

> While this geometric framework is both mathematically elegant and computationally tractable, geodesic protocols are fundamentally approximate; their performance often degrades for sufficiently small protocol times, in some cases performing even worse than a linear interpolation protocol

[PROPOSAL] **Korbel (arXiv:2604.26601v2).** Proposals: Onsager-operator W2 generalisations; W1 activity geometries; large deviations / Schrödinger bridge.

> The first generalizes the Wasserstein-2 structure by introducing Onsager-type operators that relate thermodynamic forces to fluxes

> However, it typically assumes fixed linear-response structures that may not be realistic far from equilibrium.

> The second approach abandons the strict Riemannian structure and instead defines generalized Wasserstein-1 geometries based on constraints on dynamical activity or related quantities

> Connections to large deviation theory and classical problems such as the Schrödinger bridge are expected to play an important role in this direction.

[PROPOSAL] **Blaber & Sivak (arXiv:2212.00706v2).** Proposals: interpolate slow/fast and weak/strong approximations.

> A promising area of future study would be to explore if extensions and generalizations can be made to strong and fast control.

> For fast driving, the minimum-dissipation protocols determined from linear-response theory have jumps at the start and end of the protocol.

[DIRECTION-NAMED] **Korbel (arXiv:2604.26601v2).** DIRECTION-NAMED: the dissipation metric is Wasserstein-2 (optimal transport) / thermodynamic length; the Fisher metric is not named as the dissipation metric here.

> For overdamped Langevin systems with constant diffusivity, the entropy produced along a stochastic trajectory coincides with the optimal transport cost of redistribution

> This geometric picture extends to the linear-response regime, where thermodynamic length quantifies dissipation during slow transformations, and geodesics prescribe optimal protocols

[DIRECTION-NAMED] **Blaber & Sivak (arXiv:2212.00706v2).** DIRECTION-NAMED: the metric is the friction tensor.

> The generalized friction tensor endows the space of thermodynamic states with a Riemannian metric where minimum-dissipation protocols correspond to geodesics of the friction tensor.

[DIRECTION-NAMED] **Zhong & DeWeese (arXiv:2404.01286v4).** DIRECTION-NAMED: beyond linear response, the geodesic is of the friction tensor (= OT geometry); the Fisher information metric enters only the counterdiabatic term.

> We show that obtaining optimal protocols past the slow-driving or linear response regime is computationally tractable as the sum of a friction tensor geodesic and a counterdiabatic term related to the Fisher information metric.

> Here we derive an even stronger result, that thermodynamic geometry is in fact equivalent to optimal transport geometry, in the sense that the friction tensor and the Benamou-Brenier problem restricted to equilibrium distributions parameterized by \lambda have identical geodesics and geodesic distances.

[DIRECTION-NAMED] **Sivak & Crooks (arXiv:1201.4166v2).** DIRECTION-NAMED (targeted search): friction tensor = relaxation time x Fisher information; equals the Fisher metric only when relaxation time is constant.

> we derive a friction tensor that induces a Riemannian manifold on the space of thermodynamic

> When the relaxation time does not vary with the control parameter, the Riemannian metric reduces to the Fisher information metric [26]

### The direction search

The fetched texts were searched for: Fisher, friction tensor, friction matrix, geodesic, thermodynamic length, beyond linear response, linear-response, open question, remains unclear. Targeted web search: "Fisher information metric versus friction tensor thermodynamic length minimal dissipation which metric 2024 2025 arXiv". It led to Sivak & Crooks 2012, which was fetched.

- [DIRECTION-NOT-FOUND-IN-FETCHED] **The Fisher information metric as the dissipation metric.** No fetched source proposes it. The friction tensor (equivalently, optimal-transport geometry) is named as the metric. The Fisher metric appears in two roles only. It is the special case with a constant relaxation time (Sivak & Crooks 2012). It is the counterdiabatic correction beyond linear response (Zhong & DeWeese 2024). The Quo vadis perspective does not mention "Fisher" at all.

---

## F11. Active inference and the free-energy principle as a theory of cognition (precision, timescales)

**The declaration's direction for F11.** statements on precision, timescales, or the "clock" of belief updating as open problems; statements that equate precision with attention.

### Sources

- **Hodson, Mehta, Smith, The empirical status of predictive coding and active inference, Neurosci. Biobehav. Rev. (2024), DOI 10.1016/j.neubiorev.2023.105473**
  - Version: abstract only (Europe PMC, PMID 38030100; full text 403/paywalled)
  - URL: https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:38030100%20AND%20SRC:MED&format=json&resultType=core
  - Fetch: HTTP 200 (Europe PMC abstract); no open full text found
  - Raw file: `f11_hodson2024_empirical_status_abstract_PMID38030100.txt`
- **Lageman, Fahrenfort, Slagter, Prediction in action: Toward an empirical science of active inference, Neurosci. Biobehav. Rev. (2026), DOI 10.1016/j.neubiorev.2026.106817**
  - Version: abstract only (Europe PMC, PMID 42285188, first published 2026-06-13; ScienceDirect 403)
  - URL: https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:42285188%20AND%20SRC:MED&format=json&resultType=core
  - Fetch: HTTP 200 (Europe PMC abstract); ScienceDirect 403
  - Raw file: `f11_lageman2026_prediction_in_action_abstract_PMID42285188.txt`
- **Badcock & Davey, Active Inference in Psychology and Psychiatry: Progress to Date?, Entropy 26(10):833 (2024), DOI 10.3390/e26100833**
  - Version: PMC11507080 (first published 2024-09-30)
  - URL: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11507080/fullTextXML
  - Fetch: HTTP 200 (Europe PMC fullTextXML)
  - Raw file: `f11_badcock_davey2024_actinf_psychiatry_PMC11507080.txt`
- **Pezzulo, Parr, Friston, Active inference as a theory of sentient behavior, Biol. Psychol. (2024), DOI 10.1016/j.biopsycho.2023.108741**
  - Version: abstract only (Europe PMC, PMID 38182015; CC BY but ScienceDirect returned 403)
  - URL: https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:38182015%20AND%20SRC:MED&format=json&resultType=core
  - Fetch: HTTP 200 (Europe PMC abstract); ScienceDirect 403, Elsevier API 400, Crossref says CC BY
  - Raw file: `f11_pezzulo2024_sentient_abstract_PMID38182015.txt`
- **Proietti, Parr, Tessari, Friston, Pezzulo, Active inference and cognitive control: Balancing deliberation and habits through precision optimization (Review), Phys. Life Rev. (2025), DOI 10.1016/j.plrev.2025.05.008**
  - Version: published version PDF, institutional repository (available online 16 May 2025)
  - URL: https://cris.unibo.it/retrieve/4f0ef4b4-b5f4-462d-8fe3-6e4fd3b7104b/Physic%20of%20life%20reviews%202025.pdf
  - Fetch: HTTP 200 (institutional-repository PDF, pypdfium2)
  - Raw file: `f11_pezzulo2025_plr_cognitive_control_unibo.txt`
- **Klar, Stein, Paterson, Williamson, Gollee, Murray-Smith, Intermittent Active Inference, Entropy 28(3):269 (2026), DOI 10.3390/e28030269 (targeted search; research article)**
  - Version: PMC13024937 (first published 2026-02-28)
  - URL: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13024937/fullTextXML
  - Fetch: HTTP 200 (Europe PMC fullTextXML)
  - Raw file: `f11_intermittent_actinf2026_PMC13024937.txt`
- **Harris & Arthur, Hidden State Inference or Continuous Belief Updating during a Dynamic Visuomotor Skill, J. Neurosci. 46 (2026), DOI 10.1523/JNEUROSCI.1285-25.2025 (targeted search; research article)**
  - Version: PMC12873645 (first published 2026-02-04)
  - URL: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12873645/fullTextXML
  - Fetch: HTTP 200 (Europe PMC fullTextXML)
  - Raw file: `f11_belief_updating_visuomotor_PMC12873645.txt`

### Quotes

[BOTTLENECK] **Hodson (abstract only).** Bottleneck: empirical validity untested against alternatives.

> While Active Inference models tend to explain behavioral data reasonably well, there has not been a focus on testing empirical validity of active inference theory per se, which would require formal comparison to other models (e.g., non-Bayesian or model-free reinforcement learning models).

[BOTTLENECK] **Lageman (abstract only).** Bottleneck: distinct testable predictions.

> Despite its growing prominence, the framework is often criticized for the difficulty of extracting qualitatively distinct, testable predictions and its limited empirical grounding.

> We highlight areas where evidence is promising, while emphasizing the need for theory-driven experiments that can adjudicate between accounts.

[BOTTLENECK] **Badcock & Davey (PMC11507080).** Bottleneck: whether active inference adds to existing accounts.

> Meanwhile, the main outstanding question is whether this theory will make a positive difference through applications in clinical psychology, and its sister discipline of psychiatry.

> Despite its unique explanatory promise, without further empirical progress in this area, the extent to which active inference adds meaningfully to what we already know about depression remains to be seen.

[BOTTLENECK] **Proietti (published version PDF, institutional repository).** Bottleneck: context-sensitivity of precision control; reconciling neurobiological proposals.

> Our simulations show that a standard active inference model can form adaptive habits; i.e., can pass from deliberative to habitual control when the context is stable, but generally fails to revert to deliberative control, when the context changes.

> Reconciling these and other alternative proposals is an open objective for future studies.

[PROPOSAL] **Lageman (abstract only).** Proposal: named testable predictions in decision-making and motor control.

> In the domain of decision-making, we identify predictions that agents behave more stochastically when they are uncertain about outcome predictions; that they explore to resolve uncertainty about hidden states and model parameters; and that preferences can be learned through accumulated experience.

[PROPOSAL] **Pezzulo (abstract only).** Proposals (abstract only): aberrant precision control; temporally deep hierarchical models.

> Active inference has been used to account for aspects of anatomy and neurophysiology, to offer theories of psychopathology in terms of aberrant precision control, and to unify extant psychological theories.

> Key steps in this development include the formulation of predictive coding models and related theories of neuronal message passing, the use of sequential models for planning and policy optimization, and the importance of hierarchical (temporally) deep internal (i.e., generative or world) models.

[DIRECTION-NAMED] **Badcock & Davey (PMC11507080).** DIRECTION-NAMED: precision equated with attention (selective attention / attentional selection) and a timescale (seconds to hours) for precision learning; stated as the framework's account, not as an open problem.

> Prediction errors are also weighted by their precision , which relates to the reliability afforded to various beliefs or sources of sensory evidence, and involves neuromodulatory mechanisms (e.g., affecting attentional selection) that determine the relative influence of ascending (error) vs. descending (representation) signals on belief-updating

> This will occur according to the degree of confidence in one’s generative models, and corresponds psychologically to the selective attention or sensory attenuation of evidence for one’s Bayesian beliefs.

> The second process, which relates to learning and attention , optimises synaptic strength and efficiency over seconds to hours to encode the precision of prediction errors and the causal structure of the environment in the sensorium.

[DIRECTION-NAMED] **Proietti (published version PDF, institutional repository).** DIRECTION-NAMED: precision as control signal and attentional resource (proposal, 2025 review).

> The theory proposes that cognitive control amounts to optimising a precision parameter, which acts as a control signal and balances the contributions of deliberative and habitual components of action selection.

> This novel expected (indicated by bold) precision parameter γ’ plays the role of a control signal [140] and of attentional resources [31,138] and its main role is to prioritize deliberative components of action selection, when useful.

[DIRECTION-NAMED] **Klar (PMC13024937).** DIRECTION-NAMED (targeted search): the clock of belief updating (continuous vs event-triggered) is posed and an event-triggered variant proposed.

> Whilst standard formulations assume continuous inference and control, empirical evidence indicates that humans update their control strategies intermittently, which reduces computational demands and mitigates propagation of correlated noise in closed feedback loops.

> This paper investigates intermittent planning, where IAIF agents follow their current plan and only re-plan when the prediction error exceeds a predefined threshold or the Expected Free Energy associated with the current plan surpasses prior estimates.

[DIRECTION-NAMED] **Harris & Arthur (PMC12873645).** DIRECTION-NAMED (targeted search): continuous vs discrete belief updating tested empirically (continuous won in that task).

> Here, we test whether behavior in a naturalistic interception task is better explained by continuous belief updating or by more abrupt shifts driven by state inference, consistent with hierarchical Bayesian learning.

> However, the neurocomputational mechanisms through which higher-level beliefs shape moment-to-moment perception and action behaviors remains unclear.

### The direction search

The fetched texts were searched for: attention, precision, timescale, time scale, continuous updating, intermittent, discrete time, open question, remains unclear, remains to be, limitation. Targeted web search: "active inference precision attention open question timescale of belief updating review 2025 PMC". It led to Proietti et al. 2025, Harris & Arthur 2026 and (from an earlier search) Klar et al. 2026, which were fetched.

- [DIRECTION-NOT-FOUND-IN-FETCHED] **Precision or its timescale as an open problem, in the four reviews.** None of the four reviews poses it as an open problem. Badcock & Davey state precision as attention, and a seconds-to-hours timescale for precision learning, as settled parts of the account. Proietti et al. present precision as the attentional control signal as their proposal. The clock of belief updating (continuous against event-triggered or discrete) is posed as an open question only in the two targeted research articles (Klar et al. 2026; Harris & Arthur 2026).
- Three full texts were not reachable: Hodson et al. 2024, Lageman et al. 2026 and Pezzulo, Parr & Friston 2024. Their quotes come from the abstracts alone.

---

## Summary of the direction search

Each line records only whether the declaration's direction was found named. It is not a label.

- **F8.** Named. Time-rescaling residual analysis (transform to homogeneous Poisson) is named in Mizrahi et al. 2024, as an existing test not yet routine in CSEP. Event-count natural time is named in Rundle et al. 2025. Neither is named in the other three reviews.
- **F9.** Named. The QFI and the quantum Cramér–Rao bound are the standard figure of merit (Montenegro et al.), and the QFI is read as the distinguishability of neighbouring states (Konar et al.).
- **F10.** Named. The friction tensor (equivalently, optimal-transport or Wasserstein-2 geometry) is the metric whose geodesics minimise dissipation. The Fisher information metric enters only as the constant-relaxation-time special case or as the counterdiabatic term beyond linear response.
- **F11.** Precision is equated with attention in Badcock & Davey 2024 and Proietti et al. 2025. The clock of belief updating (continuous against event-triggered or discrete) is posed in Klar et al. 2026 and Harris & Arthur 2026. None of the four reviews poses precision or timescales as the open problem. Their stated bottleneck is empirical: distinct testable predictions and comparison with alternative models.
