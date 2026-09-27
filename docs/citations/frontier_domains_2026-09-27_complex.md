# Frontier domains F3-F6: bottlenecks, proposals, and whether CRR's direction is already named (2026-09-27)

A note, not evidence (R8). Quotes are verbatim substrings of the saved texts.

- **Request:** the declaration `labs/frontier/DECLARATION.md` (prompt-log entry 226), domains F3, F4, F5 and F6. It was pushed before any source was fetched.
- **Where the texts are:** raw texts saved in the session scratchpad under `frontier/cx/*.txt` (never committed).
- **How the text was extracted:** PDF text by pypdf 6.19.0; HTML/XML with tags stripped. Each file begins with its URL, the fetch time (UTC) and the HTTP status.
- **Machine-readable claims:** `frontier/cx_claims.json`.
- **Verification.** 69 quotes. Each one was checked in Python to be a substring of its saved text after whitespace is collapsed: 69/69 hold. Hyphenation and lost spaces from PDF extraction are kept as extracted.
- **What this dossier does not do.** It assigns no COMPATIBLE-P, CONFLICT-W or OUTSIDE reading and no RESTATES, GUIDES or SILENT label. Those belong to the investigator and `labs/frontier/checks/grade.py`. Nothing here claims novelty. 'Not found in the fetched texts' means only that.

## F3: Epidemic forecasting with behavioural feedback

**CRR's suggested direction (from the declaration):** distancing responds to a remembered / exponentially weighted / delayed memory of prevalence, not current prevalence; oscillations set by the memory length.

**Direction search, summary:** **Named.** Mao et al. (2026) name and fit an exponential-decay memory of past prevalence, alongside sliding-window and power-law memories. The MBE (2026) paper names a memory kernel distributed over the past and states that the period and peak of the waves depend on the kernel's shape. Its reference list carries d'Onofrio & Manfredi (2009) on information-driven oscillations. Diekmann et al. (2025) name a response 'possibly with some delay'. Counterpoint (arXiv 2607.18301v3): cycles can arise at finite behavioural relaxation rates with no imposed delay.

### Sources

| key | source | version / date | URL | fetch status | raw file | sha256 (first 16) |
|---|---|---|---|---|---|---|
| F3_pnas | Gozzi, Perra, Vespignani, 'Comparative evaluation of behavioral epidemic models using COVID-19 data', PNAS 122(24) e2421993122 (2025), doi:10.1073/pnas.2421993122, PMC12184516 | published 2025-06-17 (received 2024-10-24, accepted 2025-05-08); full text via Europe PMC fullTextXML | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12184516/fullTextXML | 200 (the PMC HTML page https://pmc.ncbi.nlm.nih.gov/articles/PMC12184516/ returned a reCAPTCHA page, not used) | `frontier/cx/F3_pnas_comparative_behavioral.txt` | `617124cd2d7083f9` |
| F3_diekmann | Diekmann, Inaba, Thieme, 'Mathematical epidemiology of infectious diseases: an ongoing challenge', arXiv:2505.01621 (perspective with a Challenges/Open Problems section) | arXiv v2, 2025-08-05 (latest on the day) | https://arxiv.org/pdf/2505.01621 | 200 | `frontier/cx/F3_math_epi_challenge.txt` | `efb7ab7bd09fae47` |
| F3_mao | Mao, Deardon, Deeth, 'Memory mechanisms for behavioural change in Bayesian individual-level spatial epidemic models', Infectious Disease Modelling (2026), doi:10.1016/j.idm.2026.05.008, PMC13276345 | 2026 (accepted 2026-05; CC BY); full text via Europe PMC fullTextXML | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13276345/fullTextXML | 200 (PMC HTML page returned a reCAPTCHA page, not used) | `frontier/cx/F3_memory_mechanisms.txt` | `5965c4af6b3be581` |
| F3_mbe | 'Behavior-induced oscillations in epidemic outbreaks with distributed memory: Beyond the linear chain trick using numerical methods', Mathematical Biosciences and Engineering 23(1):76-96 (2026), doi:10.3934/mbe.2026004 (targeted direction search) | published 2025-11-28 (received 2025-07-29); abstract page | https://www.aimspress.com/article/doi/10.3934/mbe.2026004 | 200 | `frontier/cx/F3_dist_memory_oscillations.txt` | `a5707cd524333611` |
| F3_fatigue | Mohammed, Alsammani, 'Long-term Coexistence of Epidemics and Risk Awareness: Impacts of Adaptive Human Response and Fatigue', arXiv:2607.18301 (abstract page; found by the targeted direction search) | arXiv v3, 2026-09-20 | https://arxiv.org/abs/2607.18301 | 200 | `frontier/cx/F3_fatigue_abs.txt` | `4eef18d9a0ae089e` |

### Quotes

**F3_pnas**

- [BOTTLENECK] "Characterizing the feedback linking human behavior and the transmission of infectious diseases (i.e., behavioral changes) remains a significant challenge in computational and mathematical epidemiology."
- [BOTTLENECK] "Existing behavioral epidemic models often lack real-world data calibration and cross-model performance evaluation in both retrospective analysis and forecasting."
- [BOTTLENECK] "Furthermore, translating mobility changes into contact reductions remains an open challenge."
- [PROPOSAL] "Specifically, we investigate three mechanistic models: i) the Data-Driven Behavioral Model exemplifies data-driven approaches, leveraging mobility data to estimate effective changes in contact patterns; ii) the Compartmental Behavioral Feedback Model simulates the feedback loop by explicitly representing different behavioral classes within the population; iii) the Effective Force of Infection Behavioral Feedback Model employs an effective nonlinear forcing to adjust the infection rate based on the epidemic’s progression and the resulting behavioral changes."
- [PROPOSAL] "our findings show that approaches explicitly modeling behavioral feedback mechanisms often outperform data-driven approaches, even when considering data quality and the increased numbers of free parameters of these models."
- [PROPOSAL] "f(Drep) is a nonlinear function of the number of reported deaths that modulates the force of infection in the Effective Force of Infection Behavioral Feedback model." *(The feedback here is on reported deaths (with reporting delay compartments), not on an explicitly weighted memory of prevalence.)*

**F3_diekmann**

- [BOTTLENECK] "Human behaviour adapts to perceived risk, either spontaneously or on the instruction of the govern- ment [43]." *(Opens Section 5 'Challenges / Open Problems'; PDF hyphenation kept.)*
- [BOTTLENECK] "Even though it is clear that outbreak dynamics is influenced by all of these mech- anisms, it is virtually impossible to quantitatively disentangle their effect on the basis of data."
- [PROPOSAL] "By allowing this parameter to vary dynamically in response (possibly with some delay) to the prevail- ing incidence or prevalence, one obtains a simple representation of contact reduction triggered by awareness." *(Names delayed response to prevalence (a delay, not a geometric memory).)*
- [BOTTLENECK] "It would be an interesting challenge to incorporate behavioural feedback in such more complicated models."

**F3_mao**

- [BOTTLENECK] "While recently developed behavioural change epidemic models attempt to acknowledge such dynamics, the role of memory in shaping perceived risk has been treated in an ad hoc fashion."
- [BOTTLENECK] "Many existing approaches either base individual responses solely on current information, without explicitly considering accumulated historical knowledge, or rely on ad hoc assumptions about how memory shapes behaviour, thereby imposing a rigid evolution of responses."
- [DIRECTION-NAMED] "In this study, we propose four alternative memory mechanisms and incorporate them into the BC-ILM framework." *(Memoryless, sliding window, power-law decay and exponential decay.)*
- [DIRECTION-NAMED] "Similarly, we introduce an exponential decay memory model, in which past prevalence values are discounted exponentially over time:" *(The geometrically weighted memory of prevalence is named and fitted.)*
- [BOTTLENECK] "Across all three MEBC-ILMs, we observe a consistent underestimation of memory strength." *(Identifiability of the memory parameter is itself an open problem.)*

**F3_mbe**

- [DIRECTION-NAMED] "In line with the information index approach, we supposed that individuals react to past information according to a memory kernel that is continuously distributed in the past."
- [DIRECTION-NAMED] "In agreement with previous studies, we showed that behavior adaptation alone can cause sustained waves of infections even in an outbreak scenario, and notably in the absence of other processes like demographic turnover, seasonality, or waning immunity."
- [DIRECTION-NAMED] "Our analysis gives a more general insight into how the period and peak of epidemic waves depend on the shape of the memory kernel and how the level of minimal contact impacts the stability of the behavior-induced positive equilibrium." *(Oscillation period set by the memory kernel: named.)*
- [DIRECTION-NAMED] "Information-related changes in contact patterns may trigger oscillations in the endemic prevalence of infectious diseases" *(Title of d'Onofrio & Manfredi (2009) in the reference list: the information-index (memory) route to oscillations predates this work.)*

**F3_fatigue**

- [BOTTLENECK] "Human behavior shapes epidemic dynamics, yet most models represent it by rescaling transmission, conflating behavior with biology and removing the memory carried by sustained protective behavior."
- [PROPOSAL] "At finite relaxation rates, however, numerical stability and bifurcation analyses reveal a Hopf transition and self-sustained epidemic cycles without an imposed delay." *(A counterpoint: cycles without an imposed memory kernel.)*

## F4: Macroeconomic expectations: inflation-expectation formation and de-anchoring

**CRR's suggested direction (from the declaration):** expectations as an experience-weighted / geometrically decaying memory of past inflation (Malmendier-Nagel experience effects; adaptive learning with constant gain).

**Direction search, summary:** **Named.** D'Acunto et al. (2024) and Gennaioli et al. (2024) both name Malmendier-Nagel experience effects: a time-discounted average of lifetime inflation experiences. Gati (ECB WP 2685, 2022; older than the window) names constant-gain learning as the baseline. Counterpoint: Gennaioli et al. write that the 2021 de-anchoring 'does not ... align with a simple effect of past or recent experiences', and they propose similarity-cued selective recall instead. D'Acunto et al. list 'how far back consumers look' as open.

### Sources

| key | source | version / date | URL | fetch status | raw file | sha256 (first 16) |
|---|---|---|---|---|---|---|
| F4_dacunto | D'Acunto, Charalambakis, Georgarakos, Kenny, Meyer, Weber, 'Household Inflation Expectations: An Overview of Recent Insights for Monetary Policy', NBER Working Paper 32488 (also ECB Discussion Paper 24) | NBER WP 32488, May 2024 | https://www.nber.org/system/files/working_papers/w32488/w32488.pdf | 200 | `frontier/cx/F4_dacunto_household_overview.txt` | `f6161ac24265229f` |
| F4_gennaioli | Gennaioli, Leva, Schoenle, Shleifer, 'How Inflation Expectations De-Anchor: The Role of Selective Memory Cues', NBER Working Paper 32633 | NBER WP 32633, June 2024 | https://www.nber.org/system/files/working_papers/w32633/w32633.pdf | 200 | `frontier/cx/F4_how_deanchor.txt` | `de0c1229f2eedea1` |
| F4_coibion | Coibion, Gorodnichenko, 'Inflation, Expectations and Monetary Policy: What Have We Learned and to What End?', IZA Discussion Paper 17919 | IZA DP 17919, May 2025 | https://docs.iza.org/dp17919.pdf | 200 | `frontier/cx/F4_iza_inflation_expectations.txt` | `09c4652490225074` |
| F4_ecb3082 | Christoffel, Farkas, 'Managing the risks of inflation expectation de-anchoring', ECB Working Paper 3082, doi:10.2866/7698288 | ECB WP 3082, (c) ECB 2025 | https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp3082~273898d46f.en.pdf | 200 | `frontier/cx/F4_ecb_wp3082_deanchoring_risks.txt` | `2f198ddb974a4157` |
| F4_gati | Gati, 'Monetary policy & anchored expectations: an endogenous gain learning model', ECB Working Paper 2685 (targeted direction search; older than the 2024-2026 window) | ECB WP 2685, July 2022 | https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp2685~95e6d7b379.en.pdf | 200 | `frontier/cx/F4_ecb_wp2685_endogenous_gain.txt` | `449cc9844ec374e3` |

### Quotes

**F4_dacunto**

- [BOTTLENECK] "Understanding how consumers make such temporal comparisons, i.e., how far back consumers look to form price change perceptions , represents an important subject for future research." *(The memory horizon is named as open. Stray space before the comma is in the extracted text.)*
- [BOTTLENECK] "the highly dispersed, extrapolative, and idiosyncratic nature of consumer inflation expectations poses important questions and challenges for what monetary policy can - or should - expect to achieve in terms of influencing consumers’ inflation expectations"
- [PROPOSAL] "D’Acunto and Weber (2022) recently put forward a memory framework in which consumers rely on selective recall of received price signals for specific goods when forming beliefs and often underestimate past prices."
- [PROPOSAL] "the recent experience also highlights the importance of looking at measures of the cross-sectional distribution, such as the skewness of expectations, as an early-warning indicator of possible future de-anchoring."
- [DIRECTION-NAMED] "and Nagel (2016) find that consumers overweight their own previous lifetime experience of inflation when thinking about future price changes."
- [DIRECTION-NAMED] "Their model also implies that the inflation expectations of younger consumers, given their shorter lifetime inflation history, should react more strongly to the same shocks relative to older consumers"

**F4_gennaioli**

- [DIRECTION-NAMED] "Malmendier and Nagel (2011, 2016, 2021) show that such expectations depend on a time-discounted average of lifetime inflation experiences, which of course only gradually adjusts to recent events." *(The geometric/experience-weighted memory is the stated conventional wisdom.)*
- [BOTTLENECK] "Yet the evidence from the recent inflation surge does not support stickiness, nor does it align with a simple effect of past or recent experiences." *(A bottleneck posed AGAINST the experience-weighted-memory direction.)*
- [BOTTLENECK] "Recency effects cannot explain all of: i) the stability of expectations in the pre-2021 period, ii) their sharp rise in April 2021, and iii) the strong de-anchoring by the elderly."
- [PROPOSAL] "In a model of memory and selective recall, household inflation expectations remain rigid when inflation is anchored but exhibit sharp instability during inflation surges, as similarity prompts retrieval of forgotten high-inflation experiences."
- [PROPOSAL] "Numerical similarity yields state-dependence, and hence memory based de-anchoring: as people see a jump in inflation, say from 2% to 10%, they start selectively recalling inflation levels around 10%."

**F4_coibion**

- [BOTTLENECK] "First, how has the recent experience altered our views about the formation of inflation expectations by economic agents and their consequences?"
- [PROPOSAL] "But if learning primarily takes place when inflation is high relative to the target, then it is natural that inflation expectations will appear to be systematically unanchored, both during the bad times when people are attentive (which is when central banks appear to be failing) as well as during the good times when people are inattentive and their expectations are shaped by their prior experiences."
- [DIRECTION-NAMED] "consistent with a wide body of evidence that studies how large macroeconomic events like the Great Depression or hyperinflations can have persistent effects on beliefs"

**F4_ecb3082**

- [BOTTLENECK] "However, in times of high inflation or prolonged low inflation, there is a risk that inflation expectations may stray from the central bank’s target—a phenomenon known as de-anchoring."
- [PROPOSAL] "We propose a monetary policy framework in which the central bank accounts for de-anchoring risks using a regime-switching model."
- [BOTTLENECK] "Future research could provide a more comprehensive evaluation of various policy alternatives with respect to the implied risks of a de-anchoring of inflation expectations."

**F4_gati**

- [DIRECTION-NAMED] "Thus, one can interpret the gain as the sensitivity of the expectations process to short-run surprises." *(Adaptive learning with a gain; constant gain = geometric memory.)*
- [DIRECTION-NAMED] "endogenous gain learning models can match time-varying volatility in the data, a feature that constant gain learning or rational expectations models cannot account for." *(Constant-gain learning is named as the baseline that an endogenous gain improves on.)*
- [PROPOSAL] "The endogenous gain can thus be interpreted as a metric of the varying degrees of unanchoring."

## F5: Traffic flow and automated-vehicle string stability with human memory/delay

**CRR's suggested direction (from the declaration):** car-following with a memory of past headways / distributed delays, and its effect on string stability.

**Direction search, summary:** **Named.** Sipahi & Niculescu (2010; older than the window) model human memory as distributed delays and analyse the stability of the closed loop with headway control. Both the IDM review (2025) and the car-following review (2024) name IDMM (IDM with memory) and deep-learning long-memory models. Counterpoint: the IDM review cites a 25-car platoon experiment in which reaction delay had a negligible effect on fluctuation growth. None of the fetched texts derives an explicit 'memory age at the string-stability boundary' result; the targeted search's search-engine summary pointed to 'gamma-distributed memory' car-following work, but it was not fetched and is not quoted.

### Sources

| key | source | version / date | URL | fetch status | raw file | sha256 (first 16) |
|---|---|---|---|---|---|---|
| F5_idm | Zhou, Zheng, Tian, Jiang, Zhang, 'Twenty-Five Years of the Intelligent Driver Model: Foundations, Extensions, Applications, and Future Directions', arXiv:2506.05909 | arXiv v2, 2025-11-23 (latest on the day) | https://arxiv.org/pdf/2506.05909 | 200 (PDF text extraction lost many inter-word spaces; quotes keep the extracted form) | `frontier/cx/F5_idm_25years.txt` | `8b3748fc42b794b9` |
| F5_cfreview | Zhang et al., 'Car-Following Models: A Multidisciplinary Review', arXiv:2304.07143 | arXiv v4, 2024-03-05 (HTML); a v5 of 2025-02-16 exists and was NOT fetched | https://arxiv.org/html/2304.07143v4 | 200 | `frontier/cx/F5_carfollowing_review.txt` | `56e5388539ac5a15` |
| F5_ehrhardt | Ehrhardt, Tordeux, 'Stability of heterogeneous linear and nonlinear car-following models', arXiv:2408.07549 (preprint submitted to Franklin Open) | arXiv v1, 2024-08-14 | https://arxiv.org/pdf/2408.07549 | 200 | `frontier/cx/F5_heterogeneous_stability.txt` | `b3cb5bba4a02ab5a` |
| F5_sipahi | Sipahi, Niculescu, 'Stability of car following with human memory effects and automatic headway compensation', Phil. Trans. R. Soc. A 368:4563-4583 (2010), doi:10.1098/rsta.2010.0127, PMID 20819822 (targeted direction search; abstract only, via Europe PMC; older than the window) | 2010-10 (abstract record) | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:20819822%20AND%20SRC:MED&resultType=core&format=xml | 200 | `frontier/cx/F5_sipahi_memory_headway_epmc.txt` | `f2cc2cd5765f019c` |

### Quotes

**F5_idm**

- [BOTTLENECK] "Yet, much of this literature remains confined to linearized scenarios, externally imposed uncertainties, and idealized driver behaviors, limiting its explanatory power in real-world complexity." *(About the traffic-stability literature.)*
- [BOTTLENECK] "With its lack of mechanisms for cooperative driving or information-sharing, IDM is less effective in modeling connected and autonomous vehicle (CAV) interactions, as well as mixed traffic environments."
- [PROPOSAL] "Future directions include integrating stochastic elements, human behavioral insights, and hybrid modeling approaches that combine physics-based structures with data-driven methodologies."
- [DIRECTION-NAMED] "IDMM (IDM with memory), which incorporates driver adaptation to traffic states." *(Memory of traffic state (level of service), not headway history.)*
- [DIRECTION-NAMED] "While IDM does not directly account for reaction time, it can be extended to include factors such as reaction delays, estimation errors, and multi-vehicle anticipation."
- [BOTTLENECK] "Their analysis of CF behaviorin a 25-carplatoonexperimentshowsthatreactiondelayhasanegligibleeffectonfluctuationgrowth" *(Extraction lost spaces. Counter-evidence: a platoon experiment finds reaction delay negligible for oscillation growth, against a delay/memory-driven account.)*

**F5_cfreview**

- [DIRECTION-NAMED] "By introducing an internal dynamical variable to represent the subjective level of service, Treiber and Helbing[80] build the IDMM (intelligent driver model with memory) to incorporate memory effects in microscopic traffic models."
- [DIRECTION-NAMED] "analyzed the long-term memory effect in the car-following model using a deep learning model by taking various time-horizon historical information as inputs."
- [PROPOSAL] "A serial distributed model predictive control (MPC) [141] is developed for connected automated vehicles (CAVs), ensuring local stability and multi-criteria string stability by formulating future state constraints and tuning weight matrices, with mathematical proofs and simulations demonstrating its superiority over traditional MPC methods in maintaining stability."
- [BOTTLENECK] "The future direction of driver behavior models, particularly in the context of integrating Artificial General Intelligent (AGI) capabilities and learning efficiencies into car following models, presents a fascinating and complex challenge."

**F5_ehrhardt**

- [BOTTLENECK] "Despite the large number of studies, understanding and controlling stop-and-go in road traffic flow remains challenging and still nowadays an active area of research."
- [BOTTLENECK] "In particular, the role of heterogeneity and non-linearity in the shape of the model remains poorly understood."

**F5_sipahi**

- [DIRECTION-NAMED] "More precisely, the delayed action/decision of human drivers is represented using distributed delays with a gap and the considered automated controller is of proportional derivative type."
- [DIRECTION-NAMED] "Surprisingly, large delays and/or gains improve stability for the corresponding closed-loop schemes." *(Stability as a function of memory (distributed delay) is analysed; the sign here is stabilising in the closed loop.)*

## F6: Early-warning signals of critical transitions (ecology/climate)

**CRR's suggested direction (from the declaration):** Fisher information as an early-warning indicator; the distance to a tipping point measured in statistically distinguishable steps rather than clock time.

**Direction search, summary:** **Partly named.** Fisher information as a regime-shift indicator is named: Karunanithi et al. (2008) propose it, Dakos et al. (2024) list 'Fisher information (temporal)' among the indicators used empirically, and Da Silva et al. (2026) use the Fisher metric's curvature to detect bifurcations. The distance-in-distinguishable-steps reading was **not found in the fetched texts**. That is a statement about these texts only, not a claim of novelty.

### Sources

| key | source | version / date | URL | fetch status | raw file | sha256 (first 16) |
|---|---|---|---|---|---|---|
| F6_dakos | Dakos et al., 'Tipping point detection and early warnings in climate, ecological, and human systems', Earth System Dynamics 15:1117-1135 (2024), doi:10.5194/esd-15-1117-2024 | published 2024-08-19 (received 2023-08-01, revised 2024-03-26) | https://esd.copernicus.org/articles/15/1117/2024/esd-15-1117-2024.pdf | 200 | `frontier/cx/F6_dakos_esd2024.txt` | `b86b371e62cbb687` |
| F6_diekert | Diekert, Heyen, Nesje, Shayegh, 'Do early warning signals of tipping points lead to better decisions?', J. R. Soc. Interface 22(225) 20240864 (2025), doi:10.1098/rsif.2024.0864, PMC11978447 (abstract only) | 2025-04 (Europe PMC core record) | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1098/rsif.2024.0864&resultType=core&format=xml | 200 (PMC HTML: reCAPTCHA; Europe PMC fullTextXML: 500; publisher PDF: 403) | `frontier/cx/F6_ews_decisions_epmc.txt` | `e5a178a99c2c4757` |
| F6_karunanithi | Karunanithi, Cabezas, Frieden, Pawlowski, 'Detection and Assessment of Ecosystem Regime Shifts from Fisher Information', Ecology and Society 13(1):22 (2008), doi:10.5751/ES-02318-130122 (targeted direction search; older than the window) | published 2008-05-13 | https://www.ecologyandsociety.org/vol13/iss1/art22/main.html | 200 | `frontier/cx/F6_karunanithi_fisher_2008.txt` | `b3e01ea131fc0123` |
| F6_gbt | Da Silva, Vieira, Leonel, 'The Geometric Bifurcation Theory', chapter 4 of 'Geometric Bifurcation Theory' (Springer, Nonlinear Physical Science), doi:10.1007/978-981-95-8291-4_4 (preview page only; found by the targeted direction search). The companion review in Physics Reports (2026), doi:10.1016/j.physrep.2026.01.004, returned 403 (captcha) at ScienceDirect; Crossref carries no abstract; not quoted | published 2026-06-03 (chapter preview) | https://link.springer.com/chapter/10.1007/978-981-95-8291-4_4 | 200 (preview; body behind subscription) | `frontier/cx/F6_gbt_springer_chapter.txt` | `4e4980ca85c43c77` |
| (not quoted) | Shi, Serdukova, Zheng, Petrovskii, Lucarini, 'Geometric early warning indicator from stochastic separatrix structure in a random two-state ecosystem model', arXiv:2603.08861 (committor-based geometric indicator, not Fisher) | arXiv v2, 2026-04-04 | https://arxiv.org/abs/2603.08861 | 200 | `frontier/cx/F6_geometric_separatrix_abs.txt` | `1b10cfd0ca38d473` |

### Quotes

**F6_dakos**

- [BOTTLENECK] "Whatever the term used, while early warnings are well grounded in theory, the challenge remains to apply them to real-world systems."
- [BOTTLENECK] "The detection of early warnings relies on the assumption that the system is approaching a transition gradually." *(Opens 4.2.1 'Fast changes, slow responses, stochasticity, multiple drivers, and limited data challenge early warning performance'.)*
- [BOTTLENECK] "we simply do not know what similar information early warnings provide."
- [PROPOSAL] "The next step is to develop meaningful ways to best combine them for detecting tipping points." *(Composite metrics (4.3.1).)*
- [PROPOSAL] "Deep learning models which combine convolutional lay- ers have been shown to outperform methods using statisti- cal CSD-based warnings (e.g. variance, AR(1)) in a variety of both real and simulated case studies (Bury et al., 2021; Deb et al., 2022)."
- [DIRECTION-NAMED] "Fisher information (temporal)" *(Fisher information appears in the review's list of early-warning indicators used in empirical studies.)*
- [DIRECTION-NAMED] "Other ML techniques can also tell us something about how far systems are from tipping." *(Distance-to-tipping is posed, but via ML, not in Fisher (distinguishable-step) units.)*

**F6_diekert**

- [BOTTLENECK] "Despite notable progress in identifying statistical indicators that can provide early warning signals (EWS) of tipping points, they have yet to find direct application in management."
- [BOTTLENECK] "We demonstrate that although EWSys can help balance the risk of tipping by providing information to update the belief about the location of the tipping point, it may also result in more risky behaviour in the case that no EWS is received."
- [PROPOSAL] "Here, we develop a theoretical model of an early warning system (EWSys) that integrates EWS information into a simple decision-making process."

**F6_karunanithi**

- [DIRECTION-NAMED] "Here we propose the use of Fisher information as a means of: (1) detecting dynamic regime shifts in ecosystems, and (2) assessing the quality of the shift in terms of intensity and pervasiveness." *(Fisher information as a regime-shift indicator, named since 2008 (the Frieden 'dynamic order' form over states, not the parameter-space Fisher metric).)*
- [DIRECTION-NAMED] "There is a great need for indicators of regime shifts, particularly methods that are applicable to data from real systems."
- [DIRECTION-NAMED] "are indistinguishable from each other if" *(States are binned by measurement uncertainty (distinguishability) before Fisher information is computed: a partial overlap with 'distinguishable steps'.)*

**F6_gbt**

- [DIRECTION-NAMED] "This includes the construction of Riemannian manifolds from dynamical systems, the Fisher information metric, and the role of scalar curvature in detecting bifurcations, local structural stability, and the character of phase–space trajectories." *(Fisher metric on parameter space used to detect bifurcations (curvature), not an arc-length distance to tipping.)*

- [DIRECTION-NOT-FOUND-IN-FETCHED] Second half of the F6 direction: measuring the distance to a tipping point as a count of statistically distinguishable steps (a Fisher-metric arc length) instead of clock time. Searched the saved texts (case-insensitive) for 'distance', 'distinguish', 'proximity', 'how far', 'time to', 'clock', 'Fisher'; plus web searches 'information geometry early warning bifurcation Fisher information metric distance to tipping point statistical distinguishability' and 'Fisher information regime shift indicator ecosystem review 2024 2025'. Nearest hits: Dakos 2024 poses 'how far systems are from tipping' via ML; Karunanithi 2008 bins states by distinguishability before computing Fisher information; the Geometric Bifurcation Theory chapter uses the Fisher metric's curvature to detect bifurcations. None of the fetched texts states the Fisher arc length to the tipping point as the measure. This is a statement about the fetched texts only; it is NOT a claim of novelty (declaration: 'Not found in the sources' is never read as 'novel').

## Fetch failures and substitutions (recorded, R10)

- pmc.ncbi.nlm.nih.gov article pages returned a reCAPTCHA page for all three PMC articles. Two were then fetched as Europe PMC `fullTextXML` (200). The third, PMC11978447, returned 500 from Europe PMC, and its publisher PDF (royalsocietypublishing.org) returned 403. The abstract was taken from the Europe PMC core record.
- The ScienceDirect page for Physics Reports doi:10.1016/j.physrep.2026.01.004 returned 403 (captcha). Crossref carries no abstract for it. The Semantic Scholar record returned `abstract: null`. It is not quoted.
- www.jorsc.shu.edu.cn ('Stability Analysis of a Car-Following Model with Effect of Driver's Memory Delay in Connected Vehicle Environment', doi:10.1007/s40305-023-00508-x): the connection was reset, so nothing was saved and nothing is quoted.
- arXiv:2304.07143 was fetched at v4 (2024-03-05). A v5 (2025-02-16) exists and was not fetched.
