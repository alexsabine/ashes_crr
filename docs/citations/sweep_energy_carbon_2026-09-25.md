# Systematic sweep, family E: energy and carbon (2026-09-25)

Declared by `Lossless_Pause/DECLARATION_2.md` (family 3, E). A note, not evidence (R8). Quotes are verbatim substrings of the saved full text (after html-unescape, removal of U+FFFE/U+00AD, `-\n` joins and whitespace collapse); PDF extraction glitches (missing spaces, ligatures such as U+FB01) are kept as extracted. New figures are reported beside the old dossiers' figures (`energy_accounting_2026-09-25.md`, `energy_inference_2026-09-25.md`, `energy_training_2026-09-25.md`); they replace nothing. This dossier does not judge novelty and does not grade C1-C5; the grading is computed by `checks/grade_sweep.py` from the claims file.

## Deviations and failures (recorded)

- **arXiv API refused.** `http://export.arxiv.org/api/query?...` returns HTTP 301 to https; `https://export.arxiv.org/api/query?...` returns **HTTP 406** through the session proxy, with or without Accept/User-Agent headers. Each of the 8 queries was tried twice (the protocol's retry); all 16 attempts failed. `https://arxiv.org/api/query` redirects to the same endpoint (302 then 406).
- **Fallback used:** arXiv's own search page, `https://arxiv.org/search/?query=<q>&searchtype=all&abstracts=show&order=&size=25` (all fields, `order=` empty = relevance, first 25). Its matching differs from the API: every term must match, so some queries return fewer than 25 hits (listed below). The date shown is the arXiv 'Submitted' date of the latest version as displayed on the search page.
- **WebSearch** returned 8-10 links per query; the full link list is logged. github.com is refused by the proxy (not attempted). No other fetch failed: every included arXiv abs page and PDF returned HTTP 200.
- **Window:** 2024-01-01 to 2026-09-25. Hits before 2024 are excluded as 'outside window'. Sources already fetched in the 2026-09-25 energy dossiers are excluded as 'duplicate of prior dossier'.

## Sources (24 included; cap 25)

### S1. Morrison, Smith, Strubell 2026, The Hidden Cost of Thinking: Energy Use and Environmental Impact of LMs Beyond Pretraining

- Authors: Morrison, Jacob; Smith, Noah A.; Strubell, Emma
- Venue/comments: arXiv preprint
- Id and current version: 2605.01158v1 (versions on abs page: v1 Fri, 1 May 2026 23:24:23 UTC)
- URL: https://arxiv.org/abs/2605.01158v1
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/hidden_cost_thinking.txt`
- Tags: C3, E-reasoning

> "Within 32B post-training, Think uses 17 × more datacenter energy than Instruct, with 87% of that energy spent on RLVR rollout generation"

> "In total, we estimate our model development process consumed ∼12.3 GWhof datacenter energy"

> "Development accounts for 82.2% of total GPU hours (6.85M of 8.34M) and 80.9% of total GPU energy, excluding data generation."

> "Each stage (midtraining, SFT, DPO, RLVR) introduces its own hyperparameters, data choices, and design decisions that require iteration."

### S2. Hugging Face (Luccioni et al.), AI Energy Score v2: Refreshed Leaderboard, now with Reasoning

- Version: HF community blog, published December 4, 2025 (fetched 2026-09-25)
- URL: https://huggingface.co/blog/sasha/ai-energy-score-v2
- Fetch status: HTML 200 (curl, tags stripped); saved `<scratchpad>/sweep/energy_carbon/ai_energy_score_v2.txt`
- Tags: E-measure, E-reasoning

> "According to our analysis, reasoning models use, on average, 30 times more energy than models with no reasoning capabilities (or with reasoning turned off)."

> "models with reasoning enabled use between 300 and 800 times more tokens than their base equivalents"

> "Under the hood, we are still using Code Carbon and the same datasets that we initially developed for the first version of the leaderboard"

### S3. Manya, Thorpe, Zhang et al. 2026, From Caveman to Expert Analyst: Energy Consumption of Variable LLM Tasks

- Authors: Manya, Diego; Thorpe, Ethan I.; Zhang, Ji; Shirk, Myranda; He, Jiamian; Hsu, Angel; Vandenbergh, Michael P.
- Venue/comments: arXiv preprint
- Id and current version: 2608.12350v1 (versions on abs page: v1 Thu, 2 Jul 2026 22:25:37 UTC)
- URL: https://arxiv.org/abs/2608.12350v1
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/caveman_expert_analyst.txt`
- Tags: E-reasoning

> "The research concludes that nonreasoning models provide sufficient quality while consuming close to one-twentieth of energy compared to reasoning models"

### S4. Ellis-Mohr, Hartman, Varshney 2026, Energy-Aware Routing to Large Reasoning Models

- Authors: Ellis-Mohr, Austin R.; Hartman, Max; Varshney, Lav R.
- Venue/comments: arXiv preprint
- Id and current version: 2601.00823v2 (versions on abs page: v2 Sun, 26 Apr 2026 18:34:17 UTC)
- URL: https://arxiv.org/abs/2601.00823v2
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/energy_aware_routing_lrm.txt`
- Tags: E-reasoning

> "Large reasoning models (LRMs) have heterogeneous inference energy costs based on which model is used and how much it reasons."

### S5. Siddiqui, Rojas, Yang et al. 2026, Measured Joules, Learned Routes

- Authors: Siddiqui, Muhammad Abdur Rab; Rojas, Daniela; Yang, Chen; Cui, Wenqi; Shi, Yuanyuan; Chen, Yize
- Venue/comments: 16 pages, 10 figures, in submission
- Id and current version: 2609.23085v1 (versions on abs page: v1 Sat, 19 Sep 2026 15:44:09 UTC)
- URL: https://arxiv.org/abs/2609.23085v1
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/measured_joules_learned_routes.txt`
- Tags: E-reasoning

> "The candidate models are first profiled through an offline tournament that records their correctness, latency, power, and GPU energy for each query."

> "we also observe a sharp accuracy–energy phase transition among routers"

### S6. Amin, Afroz, Nikolopoulos 2026, CAI-DLLM: Convergence Aware Inference for Diffusion Language Models

- Authors: Amin, Farhana; Afroz, Sabiha; Nikolopoulos, Dimitrios S.
- Venue/comments: arXiv preprint
- Id and current version: 2608.22646v1 (versions on abs page: v1 Sun, 23 Aug 2026 23:03:59 UTC)
- URL: https://arxiv.org/abs/2608.22646v1
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/cai_dllm.txt`
- Tags: C5

> "introduce a low yield detector that stops denoising when newly committed tokens remain scarce forKconsecutive steps"

> "We define a token as stable when its top prediction remains unchanged for three consecutive steps."

> "while energy consumption is reduced by up to 95.3%"

### S7. Pham, Katevas, Shamsabadi, Haddadi 2026, AgentStop: Terminating Local AI Agents Early to Save Energy in Consumer Devices (ACM CAIS '26)

- Authors: Pham, Dzung; Katevas, Kleomenis; Shamsabadi, Ali Shahin; Haddadi, Hamed
- Venue/comments: ACM CAIS '26
- Id and current version: 2605.15206v1 (versions on abs page: v1 Fri, 1 May 2026 14:45:37 UTC)
- URL: https://arxiv.org/abs/2605.15206v1
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/agentstop.txt`
- Tags: C5

> "we introduce AgentStop, a lightweight efficiency supervisor that predicts and preemptively terminates trajectories unlikely to succeed"

> "AgentStopcan reduce wasted energy by 15-20% with minimal impact on task performance (<5% utility drop)"

> "in real-world deployment, it is important to calibrate the prediction threshold to avoid these negative trade-offs"

### S8. Tschand et al. 2025, MLPerf Power: Benchmarking the Energy Efficiency of ML Systems from Microwatts to Megawatts (HPCA 2025)

- Authors: Tschand, Arya; Rajan, Arun Tejusve Raghunath; Idgunji, Sachin; Ghosh, Anirban; Holleman, Jeremy; Kiraly, Csaba; Ambalkar, Pawan; Borkar, Ritika; Chukka, Ramesh; Cockrell, Trevor; Curtis, Oliver; Fursin, Grigori; Hodak, Miro; Kassa, Hiwot; Lokhmotov, Anton; Miskovic, Dejan; Pan, Yuechao; Manmathan, Manu Prasad; Raymond, Liz; John, Tom St.; Suresh, Arjun; Taubitz, Rowan; Zhan, Sean; Wasson, Scott; Kanter, David; Reddi, Vijay Janapa
- Venue/comments: 16 pages, 11 figures, 1 table
- Id and current version: 2410.12032v2 (versions on abs page: v2 Thu, 6 Feb 2025 04:16:22 UTC)
- URL: https://arxiv.org/abs/2410.12032v2
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/mlperf_power.txt`
- Tags: E-measure

> "We use representative workloads from the MLPerf benchmark suite to collect 1,841 reproducible measurements from 60 systems across the entire range of ML deployment scales."

> "For multi-node training, this includes the compute nodes, interconnect fabric, and any cooling infrastructure."

> "Measuring power consumption from cooling remains future work."

### S9. Niu, Zhang, Li et al. 2025, TokenPowerBench: Benchmarking the Power Consumption of LLM Inference (AAAI'26)

- Authors: Niu, Chenxu; Zhang, Wei; Li, Jie; Zhao, Yongjian; Wang, Tongyang; Wang, Xi; Chen, Yong
- Venue/comments: Accepted by the AAAI'26 Conference Main Track
- Id and current version: 2512.03024v1 (versions on abs page: v1 Tue, 2 Dec 2025 18:50:17 UTC)
- URL: https://arxiv.org/abs/2512.03024v1
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/tokenpowerbench.txt`
- Tags: E-measure

> "industry reports show that inference, not training, accounts for more than 90% of total power consumption"

> "a phase-aligned metrics pipeline that attributes energy to the prefill and decode stages of every request"

### S10. Vartziotis et al. 2026, From Tokens to Watt-hours: Analytical Energy Estimation for LLM Inference on Modern GPUs

- Authors: Vartziotis, Tina; Kosteli, Rodopi; Vartziotis, Elli; Dasoulas, George; Keckeisen, Michael; Skianis, Konstantinos; Kotsopoulos, Sotirios; Dominici, Francesca
- Venue/comments: 20 pages, 3 figures, 6 tables. Accepted for oral presentation at the GREEN-AI Workshop, co-located with ECML-PKDD 2026
- Id and current version: 2607.26571v1 (versions on abs page: v1 Wed, 29 Jul 2026 07:50:55 UTC)
- URL: https://arxiv.org/abs/2607.26571v1
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/tokens_to_watthours.txt`
- Tags: E-measure

> "The resulting estimates are not intended to replace physical power measurements; rather, they provide transparent, reproducible, and assumption-explicit approximations"

### S11. Vadari 2026, The Model Parking Tax: Quantifying the Hidden Energy Cost of Always-On GPU Model Deployment

- Authors: Vadari, Sai Sathvik
- Venue/comments: 7 pages, 3 figures, 5 tables
- Id and current version: 2605.23918v1 (versions on abs page: v1 Wed, 15 Apr 2026 09:01:24 UTC)
- URL: https://arxiv.org/abs/2605.23918v1
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/model_parking_tax.txt`
- Tags: E-measure

> "The AI inference industry keeps models loaded in GPU memory around the clock to avoid cold-start latency, implicitly treating idle power as a fixed cost of readiness."

> "the CUDA context forces a discrete DVFS transition consuming +26–66W over bare idle"

> "We derive a coldstart breakeven model showing energy-optimal behavior depends on request arrival rate and loading latency—not model size—with breakeven intervals of 1–5 minutes."

### S12. Panigrahy, Tyagi 2026, Energy per Successful Goal: Goal-Level Energy Accounting for Agentic AI Systems

- Authors: Panigrahy, Deepak; Tyagi, Aakash
- Venue/comments: 34 pages, 16 figures, 10 tables
- Id and current version: 2605.22883v1 (versions on abs page: v1 Wed, 20 May 2026 22:55:19 UTC)
- URL: https://arxiv.org/abs/2605.22883v1
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/energy_per_successful_goal.txt`
- Tags: E-measure

> "EpGaggregates total workflow energy across all execution attempts, including failures and retries, normalized by successfully completed goals."

### S13. Vercellino, Willard, Campos et al. 2026, Measurement of Generative AI Workload Power Profiles for Whole-Facility Data Center Infrastructure Planning

- Authors: Vercellino, Roberto; Willard, Jared; Campos, Gustavo; Pereira, Weslley da Silva; Hull, Olivia; Selensky, Matthew; Mueller, Juliane
- Venue/comments: The data associated with this publication can be found at this http URL
- Id and current version: 2604.07345v1 (versions on abs page: v1 Wed, 8 Apr 2026 17:56:41 UTC)
- URL: https://arxiv.org/abs/2604.07345v1
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/genai_power_profiles.txt`
- Tags: E-measure

> "we measure power consumption of AI workloads at 0.1-second resolution for AI training, fine-tuning and inference jobs"

> "The dataset of power consumption profiles is made publicly available."

### S14. Luccioni, Strubell, Crawford 2025, From Efficiency Gains to Rebound Effects: The Problem of Jevons' Paradox in AI's Polarized Environmental Debate (FAccT 2025)

- Authors: Luccioni, Alexandra Sasha; Strubell, Emma; Crawford, Kate
- Venue/comments: arXiv preprint
- Id and current version: 2501.16548v2 (versions on abs page: v2 Fri, 13 Jun 2025 15:59:59 UTC)
- URL: https://arxiv.org/abs/2501.16548v2
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/luccioni_rebound_jevons.txt`
- Tags: E-rebound

> "Rebound effects undermine the assumption that improved technical efficiency alone will ensure net reductions in environmental harm."

> "Cost savings achieved by more efficient AI hardware, for example, can spur increased demand for new AI functionalities, which in turn drive further hardware upgrades and increase costs."

> "the model requires much more inference-time computation and energy than previous approaches due to its reasoning abilities"

### S15. Morand, Ligozat, Névéol 2026, The Environmental Impacts of Language Model Training Keep Rising: Now is the Time to Catch Impacts on the Rebound

- Authors: Morand, Clément; Ligozat, Anne-Laure; Névéol, Aurélie
- Venue/comments: arXiv preprint
- Id and current version: 2510.09022v2 (versions on abs page: v2 Thu, 17 Sep 2026 12:29:23 UTC)
- URL: https://arxiv.org/abs/2510.09022v2
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/morand_rebound_training.txt`
- Tags: E-rebound

> "We find that energy use and environmental impacts associated with training ML models have increased exponentially, even when considering impact reduction strategies such as using less carbon intensive electricity mixes or more efficient hardware."

> "Optimization strategies do not mitigate the impacts induced by model training, suggesting rebound effect."

### S16. Schön, Hoffmann, Becker (Gesellschaft für Informatik) 2025, Expert Assessment: The Systemic Environmental Risks of Artificial Intelligence

- Authors: Schön, Julian; Hoffmann, Lena; Becker, Nikolas
- Venue/comments: arXiv preprint
- Id and current version: 2512.11863v1 (versions on abs page: v1 Fri, 5 Dec 2025 10:15:06 UTC)
- URL: https://arxiv.org/abs/2512.11863v1
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/systemic_env_risks.txt`
- Tags: E-rebound

> "Thus, rebound effects describe instances where efﬁciency gains lead to a rise in demand and consumption, thereby exacerbating the environmental impact."

> "Direct Rebound Effects occur when increased efﬁciency of an AI system leads to more frequent or extensive use of that system"

### S17. Mhlanga 2025, AI beyond efficiency, navigating the rebound effect in AI-driven sustainable development (Front. Energy Res. 13)

- Version: Frontiers review article, 25 June 2025, doi:10.3389/fenrg.2025.1460586
- URL: https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2025.1460586/full
- Fetch status: HTML 200 (curl, tags stripped); saved `<scratchpad>/sweep/energy_carbon/frontiers_rebound.txt`
- Tags: E-rebound

> "The findings reveal that while AI-driven advancements reduce energy use per unit, they often lead to higher overall consumption, potentially negating environmental benefits"

### S18. Li, Hu, Choukse et al. 2025, EcoServe: Designing Carbon-Aware AI Inference Systems

- Authors: Li, Yueying; Hu, Zhanqiu; Choukse, Esha; Fonseca, Rodrigo; Suh, G. Edward; Gupta, Udit
- Venue/comments: arXiv preprint
- Id and current version: 2502.05043v2 (versions on abs page: v2 Sat, 15 Mar 2025 19:26:40 UTC)
- URL: https://arxiv.org/abs/2502.05043v2
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/ecoserve.txt`
- Tags: E-carbon

> "First, while GPUs dominate operational carbon, host processing systems (e.g., CPUs, memory, storage) dominate embodied carbon."

> "we demonstrate that EcoServe can lower carbon emissions by up to 47%, compared to performance, energy, and cost-optimized design points"

### S19. Bernhard, Yardimci 2026, Routing LLM Inference to the Cleanest Grid in Real Time

- Authors: Bernhard, Aleks; Yardimci, Arif Baran
- Venue/comments: 18 pages, 4 figures. Live multi-region GPU validation plus a one-year historical marginal-emissions replay
- Id and current version: 2608.06188v1 (versions on abs page: v1 Thu, 6 Aug 2026 15:46:18 UTC)
- URL: https://arxiv.org/abs/2608.06188v1
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/cleanest_grid_routing.txt`
- Tags: E-carbon

> "The central result is one of feasibility: a MOER signal can steer live inference workloads across a multi-region GPU testbed, with no observed dispatch failures, as a strict and reversible overlay on the existing production router."

### S20. Wiesner, Grinwald, Weiß et al., Carbon-Aware Quality Adaptation for Energy-Intensive Services (e-Energy'25, extended)

- Authors: Wiesner, Philipp; Grinwald, Dennis; Weiß, Philipp; Wilhelm, Patrick; Khalili, Ramin; Kao, Odej
- Venue/comments: Extended version of our paper published at e-Energy'25. Compared to the published version, we (i) add a time-based vs. utilization-based power attribution perspective together with a proof that both yield equivalent provisioning decisions under mild assumptions and (ii) extend the online approach with an automatic quality adaptation to meet a fixed annual carbon budget
- Id and current version: 2411.19058v4 (versions on abs page: v4 Wed, 4 Mar 2026 14:09:36 UTC)
- URL: https://arxiv.org/abs/2411.19058v4
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/carbon_aware_quality_adaptation.txt`
- Tags: E-carbon

> "We show that adapting this quality of responses with respect to grid carbon intensity can lead to additional carbon savings beyond resource and energy efficiency."

> "Our approach can reduce the emissions of large-scale LLM services, which we estimate at multiple 10,000 tons of CO2 annually, by up to 10 %."

### S21. Moore, Qi, Hogade et al. 2025, Sustainable Carbon-Aware and Water-Efficient LLM Scheduling in Geo-Distributed Cloud Datacenters (GLSVLSI 2025)

- Authors: Moore, Hayden; Qi, Sirui; Hogade, Ninad; Milojicic, Dejan; Bash, Cullen; Pasricha, Sudeep
- Venue/comments: arXiv preprint
- Id and current version: 2505.23554v1 (versions on abs page: v1 Thu, 29 May 2025 15:31:28 UTC)
- URL: https://arxiv.org/abs/2505.23554v1
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/carbon_water_llm_scheduling.txt`
- Tags: E-carbon

> "we propose a novel framework called SLIT to co -optimize LLM quality of service (time -to-first token), carbon emissions, water usage, and energy costs"

### S22. Yan, Li, Liu 2026, AgentDecarbonizer: Carbon-Aware Execution for AI Agents

- Authors: Yan, Leyi; Li, Shuangning; Liu, Sihang
- Venue/comments: arXiv preprint
- Id and current version: 2608.20566v1 (versions on abs page: v1 Thu, 20 Aug 2026 21:05:51 UTC)
- URL: https://arxiv.org/abs/2608.20566v1
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/agentdecarbonizer.txt`
- Tags: C4, E-carbon

> "Our characterization identifies deadline flexibility as an opportunity for carbon-aware execution: agent tasks can wait for lower-carbon-intensity periods or shift to lower-carbon grids."

> "AgentDecarbonizer reduces carbon emissions by up to 57.9 % compared with a carbon-agnostic baseline"

> "pauses between execution intervals when the plan calls for waiting, resumes from the saved execution state, and performs location shifting when the planner selects a different region"

> "while accounting for cache recomputation overhead during spatial shifting"

### S23. Hewage, Ilager, Read et al. 2025, Aging-aware CPU Core Management for Embodied Carbon Amortization in Cloud LLM Inference (ACM e-Energy '25)

- Authors: Hewage, Tharindu B.; Ilager, Shashikant; Read, Maria Rodriguez; Buyya, Rajkumar
- Venue/comments: arXiv preprint
- Id and current version: 2501.15829v1 (versions on abs page: v1 Mon, 27 Jan 2025 07:29:08 UTC)
- URL: https://arxiv.org/abs/2501.15829v1
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/aging_aware_cpu_embodied.txt`
- Tags: E-embodied

> "leading to accumulation of embodied carbon−the emissions from manufacturing and supplying IT assets−that mostly concentrate on inference server CPU"

> "an estimated 37.67% reduction in yearly embodied carbon emissions"

### S24. Panteleaki, Balaskas, Zervakis et al. 2025, Carbon-Efficient 3D DNN Acceleration: Optimizing Performance and Sustainability (ISVLSI 2025)

- Authors: Panteleaki, Aikaterini Maria; Balaskas, Konstantinos; Zervakis, Georgios; Amrouch, Hussam; Anagnostopoulos, Iraklis
- Venue/comments: IEEE Computer Society Annual Symposium on VLSI (ISVLSI) 2025
- Id and current version: 2504.09851v2 (versions on abs page: v2 Thu, 29 May 2025 16:57:22 UTC)
- URL: https://arxiv.org/abs/2504.09851v2
- Fetch status: abs 200, PDF 200 (pypdf text); saved `<scratchpad>/sweep/energy_carbon/carbon_efficient_3d_dnn.txt`
- Tags: E-embodied

> "Experimental evaluations across three technology nodes (45nm, 14nm, and 7nm) show that our method reduces embodied carbon by up to 30% with negligible accuracy drop."

## Claims

One row per claim in `<scratchpad>/sweep/energy_carbon_claims.json` (quotes in the file and above). Reading: states / close form / bears on.

| # | tag | source | reading (from the claim's note) |
|---|---|---|---|
| 1 | E-reasoning | Morrison (arXiv 2605.01158v1) | A 2025-2026 reasoning-energy measurement (training side: post-training of Olmo 3 Think vs Instruct). New figure; reported beside the old ones, replaces nothing. |
| 2 | C3 | Morrison (arXiv 2605.01158v1) | Only bears on C3: measures the development share (hyperparameter searches, failed runs, ablations) that a tuning-free weight would act on; does not state a tuning-free penalty weight. |
| 3 | E-reasoning | Hugging Face (Luccioni et al.) (HF community blog, published December 4, 2025) | A 2025 reasoning-energy measurement (inference side, AI Energy Score benchmark). New figure; reported beside the old ones. |
| 4 | E-measure | Hugging Face (Luccioni et al.) (HF community blog, published December 4, 2025) | AI Energy Score measurement method (CodeCarbon, fixed datasets); bears on how energy per model is measured. |
| 5 | E-reasoning | Manya (arXiv 2608.12350v1) | Reasoning vs non-reasoning inference energy ratio (~20x) from user-behaviour tests. |
| 6 | E-reasoning | Ellis-Mohr (arXiv 2601.00823v2) | Theory of energy-aware dispatch among reasoning models; bears on reasoning-energy allocation, no new measurement. |
| 7 | E-reasoning | Siddiqui (arXiv 2609.23085v1) | Measured-energy routing across an LLM pool; bears on routing/cascade energy (prior dossier mechanism I8). |
| 8 | C5 | Amin (arXiv 2608.22646v1) | States a close form of C5 (stop computing when the output has settled). Difference: the stop rule is a heuristic count of newly committed tokens below a threshold for K=4 steps inside diffusion decoding, not a stop on a settled belief/sequential test; energy is E = mean GPU power x time. |
| 9 | C5 | Pham (arXiv 2605.15206v1) | Bears on C5 (energy-saving early stop of agent computation). Difference from C5: stops on a learned classifier's prediction of failure (log-prob features, tuned threshold), not on the settling of the agent's own belief. |
| 10 | E-measure | Tschand et al. 2025 (arXiv 2410.12032v2) | Must-include MLPerf Power; the industry standard for measured system power; cooling for liquid-cooled systems not yet attributed. |
| 11 | E-measure | Niu (arXiv 2512.03024v1) | Inference share (>90%, as reported by industry) and a per-phase measurement pipeline. |
| 12 | E-measure | Vartziotis et al. 2026 (arXiv 2607.26571v1) | Analytical (non-measured) inference-energy estimator; bears on estimate vs measurement. |
| 13 | E-measure | Vadari 2026 (arXiv 2605.23918v1) | Idle (resident-state) energy vs cold-start reload; bears on the energy side of pausing/unloading a served model. |
| 14 | E-measure | Panigrahy (arXiv 2605.22883v1) | Unit of accounting for agentic workloads (energy per successful goal). |
| 15 | E-measure | Vercellino (arXiv 2604.07345v1) | High-resolution measured power profiles (H100) scaled to facility level. |
| 16 | E-rebound | Luccioni (arXiv 2501.16548v2) | Must-include Luccioni et al. 2025 on rebound effects. Bears on any energy-saving claim (a per-unit saving need not reduce total use). |
| 17 | E-rebound | Morand (arXiv 2510.09022v2) | Empirical rebound evidence on training (Epoch AI database). |
| 18 | E-rebound | Schön (arXiv 2512.11863v1) | Expert report; definition of direct rebound for AI. |
| 19 | E-rebound | Mhlanga 2025 (Frontiers review article, 25 June 2025, doi:10.3389/fenrg.2025.1460586) | Systematic review (150 articles, 41 in detail) on rebound from AI-driven efficiency in other sectors (AI-for-efficiency, not AI's own energy). |
| 20 | E-carbon | Li (arXiv 2502.05043v2) | Carbon-aware provisioning for LLM serving; also bears on E-embodied. |
| 21 | E-carbon | Bernhard (arXiv 2608.06188v1) | Live carbon-aware spatial routing of inference. |
| 22 | E-carbon | Wiesner (arXiv 2411.19058v4) | Carbon-aware quality tiers for always-on LLM services. |
| 23 | E-carbon | Moore (arXiv 2505.23554v1) | Geo-distributed carbon/water-aware LLM scheduling. |
| 24 | E-carbon | Yan (arXiv 2608.20566v1) | Carbon-aware temporal/spatial shifting of agent runs. |
| 25 | C4 | Yan (arXiv 2608.20566v1) | Only bears on C4: an agent paused and resumed from saved execution state for carbon reasons; it does not state a full-state / own-clock / world-content checklist, and moving regions recomputes the cached context rather than restoring it. |
| 26 | E-embodied | Hewage (arXiv 2501.15829v1) | Embodied carbon of inference servers (host CPU) and lifetime extension. |
| 27 | E-embodied | Panteleaki (arXiv 2504.09851v2) | Accelerator-design embodied-carbon reduction (approximate multipliers). |

Claims per tag: C3 1, C4 1, C5 2, E-carbon 5, E-embodied 2, E-measure 7, E-reasoning 5, E-rebound 4; total 27.

Candidate notes: no fetched source states C3 (a tuning-free calibrated penalty weight); the C3 row only measures the development share a tuning-free weight would act on. C5: CAI-DLLM states a close form (a stop rule on settled output inside diffusion decoding); AgentStop only bears on it (stop on predicted failure). C4 (outside this family's brief but found): AgentDecarbonizer pauses and resumes agents from saved execution state; it only bears on C4.

## SEARCH LOG

### E-Q1: "energy consumption reasoning models"

- arXiv API: `http://export.arxiv.org/api/query?search_query=all:energy%20consumption%20reasoning%20models&start=0&max_results=25&sortBy=relevance`: FAILED twice (HTTP 406 via https redirect); 0 hits parsed.
- arXiv search fallback: `https://arxiv.org/search/?query=energy+consumption+reasoning+models&searchtype=all&abstracts=show&order=&size=25`: 25 hits.

| arXiv id | title | submitted (latest) | decision |
|---|---|---|---|
| 2609.02729 | BuildOcc: A Large Language Model Occupant Agent Platform for Building Energy Research | 2 September, 2026 | EXCLUDE: off-topic |
| 2609.25415 | Cloud, Edge, or Split? Profiling Onboard and Split Vision-Language Model Deployment for Drone AI | 21 September, 2026 | EXCLUDE: edge VLM deployment, not reasoning energy |
| 2609.23085 | Measured Joules, Learned Routes: Learning to Route for Energy-Efficient LLM Serving | 19 September, 2026 | INCLUDE |
| 2608.22646 | CAI-DLLM: Convergence Aware Inference for Diffusion Language Models | 23 August, 2026 | INCLUDE |
| 2608.12350 | From Caveman to Expert Analyst: Energy Consumption of Variable LLM Tasks | 2 July, 2026 | INCLUDE |
| 2608.30527 | Developer Attitudes and Practices Towards Optimizing Software Energy Consumption | 31 August, 2026 | EXCLUDE: off-topic |
| 2607.19901 | StrokeSeg2: Stroke Lesion Segmentation in Clinical Research Workflows | 22 July, 2026 | EXCLUDE: off-topic |
| 2607.24904 | Mage-VL: An Efficient Codec-Native Streaming Multimodal Foundation Model | 27 July, 2026 | EXCLUDE: off-topic |
| 2607.26602 | Harnessing Large Language Models for Intelligent Resource Allocation in the Internet of Everything | 29 July, 2026 | EXCLUDE: off-topic |
| 2607.19054 | Probabilistic Physics-Aware Machine Learning Predictions of Electric Truck Energy Consumption with Field Data | 23 July, 2026 | EXCLUDE: off-topic |
| 2607.20806 | Profiling Lightweight Large Language Models | 22 July, 2026 | EXCLUDE: qualifying, not fetched (cap) |
| 2607.17317 | TAPAS: Throughput-adaptive Perception for Autonomous Systems | 19 July, 2026 | EXCLUDE: off-topic |
| 2607.06124 | Static Metrics Are Insufficient: Predicting Java Method Energy Usage with Execution Time | 7 July, 2026 | EXCLUDE: off-topic |
| 2607.24256 | ML-based Predictive Models for Power Consumption in Virtualised O-RANs | 27 July, 2026 | EXCLUDE: off-topic |
| 2607.16089 | SQUIRO: A Framework for Security-Aware Quantum-Classical Scheduling on Kubernetes | 17 July, 2026 | EXCLUDE: off-topic |
| 2607.04569 | LLMs for Agentic Home Energy Management | 27 July, 2026 | EXCLUDE: off-topic |
| 2606.27807 | SpikeVLA: Vision-Language-Action Models with Spiking Neural Networks | 26 June, 2026 | EXCLUDE: off-topic |
| 2606.28467 | An Agentic AI Pipeline for Appliance-Level Energy Anomaly Detection and LLM-Driven Recommendations | 26 June, 2026 | EXCLUDE: off-topic |
| 2605.00504 | EnCoDe: Energy Estimation of Source Code At Design-Time | 1 May, 2026 | EXCLUDE: off-topic |
| 2605.15206 | AgentStop: Terminating Local AI Agents Early to Save Energy in Consumer Devices | 1 May, 2026 | INCLUDE |
| 2605.18872 | EUPHORIA: Efficient Universal Planning via Hybrid Optimization for Robust Industrial Robotic Assembly | 15 May, 2026 | EXCLUDE: off-topic |
| 2605.01158 | The Hidden Cost of Thinking: Energy Use and Environmental Impact of LMs Beyond Pretraining | 1 May, 2026 | INCLUDE |
| 2605.03302 | Height Control and Optimal Torque Planning for Jumping With Wheeled-Bipedal Robots | 4 May, 2026 | EXCLUDE: off-topic |
| 2605.22883 | Energy per Successful Goal: Goal-Level Energy Accounting for Agentic AI Systems | 20 May, 2026 | INCLUDE |
| 2605.13338 | Inducing Overthink: Hierarchical Genetic Algorithm-based DoS Attack on Black-Box Large Language Reasoning Models | 14 May, 2026 | EXCLUDE: security attack; energy is secondary |

- WebSearch "energy consumption reasoning models": 10 links.

| URL | title | date | decision |
|---|---|---|---|
| https://arxiv.org/pdf/2606.13111 | MÖVE: A Holistic LLM Benchmark for the German Public Sector | 2026-06 | EXCLUDE: off-topic |
| https://arxiv.org/pdf/2510.24509 | Quantum Combinatorial Reasoning for Large Language Models | 2025-10 | EXCLUDE: off-topic |
| https://arxiv.org/html/2601.00823 | Energy-Aware Routing to Large Reasoning Models | 2026-01 (v2 2026-04-26) | INCLUDE |
| https://arxiv.org/pdf/2601.22076 | Where Do the Joules Go? Diagnosing Inference Energy Consumption | 2026-01 | EXCLUDE: duplicate of prior dossier (energy_inference) |
| https://www.insurancejournal.com/news/national/2025/12/05/850005.htm | The Rise of AI Reasoning Models Comes With a Big Energy Tradeoff | 2025-12-05 | EXCLUDE: not primary (news on AI Energy Score v2; primary included) |
| https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9357769/ | Explanatory Optimization of the Prediction Model for Building Energy Consumption | not shown | EXCLUDE: off-topic |
| https://fortune.com/2025/12/05/ai-reasoning-energy-problem-data-centers-30-times-more-power/ | The rise of AI reasoning models comes with a big energy tradeoff | 2025-12-05 | EXCLUDE: not primary (news) |
| https://www.bloomberg.com/news/articles/2025-12-04/the-rise-of-ai-reasoning-models-comes-with-a-big-energy-tradeoff | The Rise of AI Reasoning Models Comes With A Big Energy Tradeoff | 2025-12-04 | EXCLUDE: not primary (news) |
| https://www.sciencedirect.com/science/article/pii/S2542435126001145 | Energy use of AI inference, efficiency pathways, and test-time scaling (Joule) | 2026 | EXCLUDE: duplicate of prior dossier (energy_accounting A16, 2509.20241) |
| https://singularityhub.com/2025/12/15/hugging-face-says-ai-models-with-reasoning-use-100x-more-energy-than-those-without/ | Hugging Face Says AI Models With Reasoning Use 30x More Energy on Average | 2025-12-15 | EXCLUDE: not primary (news) |

### E-Q2: "AI inference energy measurement 2026"

- arXiv API: `http://export.arxiv.org/api/query?search_query=all:AI%20inference%20energy%20measurement%202026&start=0&max_results=25&sortBy=relevance`: FAILED twice (HTTP 406 via https redirect); 0 hits parsed.
- arXiv search fallback: `https://arxiv.org/search/?query=AI+inference+energy+measurement+2026&searchtype=all&abstracts=show&order=&size=25`: 25 hits.

| arXiv id | title | submitted (latest) | decision |
|---|---|---|---|
| 2609.10550 | Optimizing AI Inference Across the Deployment Stack | 1 July, 2026 | EXCLUDE: survey-style overview, not primary measurement |
| 2609.15241 | A 25-$μ$s/inf Event-driven Graph Neural Network Processor with Spatiotemporal Caching and Spline Convolution for Ultra-low-latency AI at the Edge | 14 September, 2026 | EXCLUDE: off-topic |
| 2609.01918 | Grounded, Compute-Efficient LLM Policy Agents for Energy-Poverty Equity in Physically-Constrained Peer-to-Peer Energy Markets | 1 September, 2026 | EXCLUDE: off-topic |
| 2609.11940 | The Battery Price of edge AI: A study of the Environmental Impact of LLM Inference on Mobile Devices | 10 July, 2026 | EXCLUDE: qualifying, not fetched (cap) |
| 2609.16705 | The Robot Data Factory | 15 September, 2026 | EXCLUDE: off-topic |
| 2609.23085 | Measured Joules, Learned Routes: Learning to Route for Energy-Efficient LLM Serving | 19 September, 2026 | EXCLUDE: duplicate (included under earlier query) |
| 2609.15583 | Generalized Parton Distributions: Phenomenology, Extraction, and Hadron Imaging | 14 September, 2026 | EXCLUDE: off-topic |
| 2608.12915 | InFactPlanner: Planning Sustainable Geo-Distributed LLM Data Centers | 13 August, 2026 | EXCLUDE: qualifying, not fetched (cap) |
| 2608.28667 | GreenBench: Benchmarking Energy Efficiency and Carbon Footprint of Open-Source LLM Inference on Apple Silicon | 24 August, 2026 | EXCLUDE: qualifying, not fetched (cap) |
| 2608.07427 | A Picture is Worth a Thousand Tokens: How Vision Language Models Cut AI Energy Costs While Improving Accuracy | 7 August, 2026 | EXCLUDE: qualifying, not fetched (cap) |
| 2607.22792 | Reducing Instruction-Fetch Energy in RISC-V for Embedded AI Processing via Dynamic and Static Loop Caching | 24 July, 2026 | EXCLUDE: off-topic |
| 2607.09520 | Seeing is Free, Speaking is Not: Uncovering the True Energy Bottleneck in Edge VLM Inference | 18 August, 2026 | EXCLUDE: qualifying, not fetched (cap) |
| 2607.26571 | From Tokens to Watt-hours: Analytical Energy Estimation for LLM Inference on Modern GPUs | 29 July, 2026 | INCLUDE |
| 2606.21833 | Inference as Flexibility: Ramp Management for Transmission-Connected AI Data Centres | 19 June, 2026 | EXCLUDE: qualifying, not fetched (cap) |
| 2606.24861 | First-Order Recoverability Collapse in Self-Referential Information Decoders: The Operating Loop of an AI System as a Driven Nonequilibrium Steady State | 16 August, 2026 | EXCLUDE: off-topic |
| 2605.22883 | Energy per Successful Goal: Goal-Level Energy Accounting for Agentic AI Systems | 20 May, 2026 | EXCLUDE: duplicate (included under earlier query) |
| 2605.23918 | The Model Parking Tax: Quantifying the Hidden Energy Cost of Always-On GPU Model Deployment | 15 April, 2026 | INCLUDE |
| 2605.00300 | Token Arena: A Continuous Benchmark Unifying Energy and Cognition in AI Inference | 30 April, 2026 | EXCLUDE: qualifying, not fetched (cap) |
| 2604.02776 | Evaluating the Environmental Impact of using SLMs and Prompt Engineering for Code Generation | 3 April, 2026 | EXCLUDE: qualifying, not fetched (cap) |
| 2604.10852 | The xPU-athalon: Quantifying the Competition of AI Acceleration | 12 April, 2026 | EXCLUDE: qualifying, not fetched (cap) |
| 2604.23554 | Adaptive Swin Transformer Partitioning over AI-RAN Networks | 26 April, 2026 | EXCLUDE: off-topic |
| 2604.03524 | Structural Rigidity and the 57-Token Predictive Window: A Physical Framework for Inference-Layer Governability in Large Language Models | 3 April, 2026 | EXCLUDE: off-topic |
| 2604.07345 | Measurement of Generative AI Workload Power Profiles for Whole-Facility Data Center Infrastructure Planning | 8 April, 2026 | INCLUDE |
| 2604.27911 | Physical Foundation Models: Fixed hardware implementations of large-scale neural networks | 30 April, 2026 | EXCLUDE: off-topic |
| 2603.14091 | Evaluating Four FPGA-accelerated Space Use Cases based on Neural Network Algorithms for On-board Inference | 14 March, 2026 | EXCLUDE: off-topic |

- WebSearch "AI inference energy measurement 2026": 10 links.

| URL | title | date | decision |
|---|---|---|---|
| https://intuitionlabs.ai/articles/ai-inference-energy-joules-per-task | Energy Use per AI Inference Task: Joules and Watt-Hours | not shown | EXCLUDE: not primary (secondary article) |
| https://arxiv.org/pdf/2605.24569 | Energy-Aware Computing in the Year 2026 | 2026-05 | EXCLUDE: duplicate of prior dossier |
| https://arxiv.org/abs/2509.20241 | Energy Use of AI Inference, Efficiency Pathways, and Test-Time Scaling | 2025-09 | EXCLUDE: duplicate of prior dossier (A16) |
| https://arxiv.org/pdf/2605.22883 | Energy per Successful Goal: Goal-Level Energy Accounting for Agentic AI Systems | 2026-05 | EXCLUDE: duplicate (included in this sweep) |
| https://davidmytton.blog/energy-use-of-ai-inference-estimates-and-efficiency-opportunities/ | Energy use of AI inference - estimates and efficiency opportunities | not shown | EXCLUDE: not primary (blog) |
| https://arxiv.org/pdf/2604.16682 | KAIROS: Stateful, Context-Aware Power-Efficient Agentic Inference Serving | 2026-04 | EXCLUDE: qualifying, not fetched (cap) |
| https://www.cell.com/joule/fulltext/S2542-4351(26)00114-5 | Energy use of AI inference, efficiency pathways, and test-time scaling: Joule | 2026 | EXCLUDE: duplicate of prior dossier (A16) |
| https://arxiv.org/pdf/2510.01889 | Small is Sufficient: Reducing the World AI Energy Consumption Through Model Selection | 2025-10 | EXCLUDE: qualifying, not fetched (cap) |
| https://arxiv.org/pdf/2601.22076 | Where Do the Joules Go? Diagnosing Inference Energy Consumption | 2026-01 | EXCLUDE: duplicate of prior dossier |
| https://aimultiple.com/ai-energy-consumption | AI Energy Consumption Statistics | not shown | EXCLUDE: not primary (statistics compilation) |

### E-Q3: "rebound effect AI energy efficiency"

- arXiv API: `http://export.arxiv.org/api/query?search_query=all:rebound%20effect%20AI%20energy%20efficiency&start=0&max_results=25&sortBy=relevance`: FAILED twice (HTTP 406 via https redirect); 0 hits parsed.
- arXiv search fallback: `https://arxiv.org/search/?query=rebound+effect+AI+energy+efficiency&searchtype=all&abstracts=show&order=&size=25`: 3 hits.

| arXiv id | title | submitted (latest) | decision |
|---|---|---|---|
| 2510.09022 | The Environmental Impacts of Language Model Training Keep Rising Now is the Time to Catch Impacts on the Rebound | 17 September, 2026 | INCLUDE |
| 2501.16548 | From Efficiency Gains to Rebound Effects: The Problem of Jevons' Paradox in AI's Polarized Environmental Debate | 13 June, 2025 | INCLUDE |
| 2412.17376 | How Green Can AI Be? A Study of Trends in Machine Learning Environmental Impacts | 23 December, 2024 | EXCLUDE: qualifying, not fetched (cap); same authors 2510.09022 fetched |

- WebSearch "rebound effect AI energy efficiency": 9 links.

| URL | title | date | decision |
|---|---|---|---|
| https://planet-a.medium.com/the-rebound-effect-ais-silent-backfire-e92c1aa8b90f | The Rebound Effect: AI's Silent Backfire | not shown | EXCLUDE: not primary (blog) |
| https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2025.1460586/full | AI beyond efficiency, navigating the rebound effect in AI-driven sustainable development | 2025-06-25 | INCLUDE |
| https://sustain.algorithmwatch.org/en/the-rebound-effect/ | The Rebound Effect – sustAIn | not shown | EXCLUDE: not primary (explainer) |
| https://arxiv.org/pdf/2512.11863 | Expert Assessment: The Systemic Environmental Risks of Artficial Intelligence | 2025-12-05 | INCLUDE |
| https://sciintl.scione.com/cms/fulltext.php?id=341 | Rebound Effects of AI on Sustainability: Economic and Policy Perspectives | not shown | EXCLUDE: qualifying, not fetched (cap) |
| https://arxiv.org/html/2501.16548v1 | From Efficiency Gains to Rebound Effects: The Problem of Jevons' Paradox in AI's Polarized Environmental Debate | 2025-01 (v2 2025-06-13) | EXCLUDE: duplicate (included in this sweep) (fetched as v2) |
| https://arxiv.org/pdf/2603.23075 | Good for the Planet, Bad for Me? Intended and Unintended Consequences of AI Energy Consumption Disclosure | 2026-03-24 | EXCLUDE: qualifying, not fetched (cap) |
| https://arxiv.org/pdf/2602.24091 | The impacts of artificial intelligence on environmental sustainability and human well-being | 2026-02 | EXCLUDE: qualifying, not fetched (cap) |
| https://en.wikipedia.org/wiki/Rebound_effect_(conservation) | Rebound effect (conservation) | not shown | EXCLUDE: not primary (encyclopedia) |

### E-Q4: "carbon-aware LLM inference serving"

- arXiv API: `http://export.arxiv.org/api/query?search_query=all:carbon-aware%20LLM%20inference%20serving&start=0&max_results=25&sortBy=relevance`: FAILED twice (HTTP 406 via https redirect); 0 hits parsed.
- arXiv search fallback: `https://arxiv.org/search/?query=carbon-aware+LLM+inference+serving&searchtype=all&abstracts=show&order=&size=25`: 6 hits.

| arXiv id | title | submitted (latest) | decision |
|---|---|---|---|
| 2609.15230 | ETCInfer: An Energy-efficient Thermal-aware Cooling-joint Scheduler for LLM Inference in AI Datacenters | 14 September, 2026 | EXCLUDE: qualifying, not fetched (cap) |
| 2608.12915 | InFactPlanner: Planning Sustainable Geo-Distributed LLM Data Centers | 13 August, 2026 | EXCLUDE: duplicate (listed under earlier query) |
| 2606.04550 | Trading Engagement for Sustainability: Carbon-Aware Re-ranking for E-commerce Recommendations | 3 June, 2026 | EXCLUDE: recommender re-ranking, not LLM serving |
| 2603.23668 | Energy Efficient Software Hardware CoDesign for Machine Learning: From TinyML to Large Language Models | 24 March, 2026 | EXCLUDE: survey, not primary |
| 2502.05043 | EcoServe: Designing Carbon-Aware AI Inference Systems | 15 March, 2025 | INCLUDE |
| 2410.14740 | Harnessing Your DRAM and SSD for Sustainable and Accessible LLM Inference with Mixed-Precision and Multi-level Caching | 22 October, 2024 | EXCLUDE: qualifying, not fetched (cap) |

- WebSearch "carbon-aware LLM inference serving": 9 links.

| URL | title | date | decision |
|---|---|---|---|
| https://doi.org/10.3390/su172310473 | A Deployment-Aware Framework for Carbon- and Water- Efficient LLM Serving | 2025 | EXCLUDE: qualifying, not fetched (cap) |
| https://www.themoonlight.io/en/review/ecoserve-designing-carbon-aware-ai-inference-systems | [Literature Review] EcoServe | not shown | EXCLUDE: not primary (review of 2502.05043) |
| https://arxiv.org/pdf/2608.06188 | Routing LLM Inference to the Cleanest Grid in Real Time | 2026-08-06 | INCLUDE |
| https://arxiv.org/pdf/2411.19058 | Carbon-Aware Quality Adaptation for Energy-Intensive Services | 2024-11 (v4 2026-03-04) | INCLUDE |
| https://arxiv.org/pdf/2609.05565 | Toward Sustainable Distributed LLM Inference: A Systems Synthesis and Research Agenda ... llm-d Control Plane | 2026-09-03 | EXCLUDE: not primary (synthesis; no new measurements, per its comments) |
| https://github.com/RavaniRoshan/carbonserve | CarbonServe (GitHub repository) | not shown | EXCLUDE: inaccessible (github.com refused by proxy); not a paper |
| https://arxiv.org/pdf/2507.11417 | Quantifying the Energy Consumption and Carbon Emissions of LLM Inference via Simulations | 2025-07-15 | EXCLUDE: qualifying, not fetched (cap) |
| https://bytez.com/docs/arxiv/2502.05043/paper | Bytez mirror of EcoServe | not shown | EXCLUDE: duplicate (included in this sweep) (mirror of 2502.05043) |
| https://pith.science/paper/2502.05043 | EcoServe · Pith Review | not shown | EXCLUDE: duplicate (included in this sweep) (mirror/review of 2502.05043) |

### E-Q5: "carbon-aware training scheduling 2025"

- arXiv API: `http://export.arxiv.org/api/query?search_query=all:carbon-aware%20training%20scheduling%202025&start=0&max_results=25&sortBy=relevance`: FAILED twice (HTTP 406 via https redirect); 0 hits parsed.
- arXiv search fallback: `https://arxiv.org/search/?query=carbon-aware+training+scheduling+2025&searchtype=all&abstracts=show&order=&size=25`: 3 hits.

| arXiv id | title | submitted (latest) | decision |
|---|---|---|---|
| 2509.08980 | Green Federated Learning via Carbon-Aware Client and Time Slot Scheduling | 10 September, 2025 | EXCLUDE: qualifying, not fetched (cap) |
| 2508.05949 | A Survey on Task Scheduling in Carbon-Aware Container Orchestration | 7 August, 2025 | EXCLUDE: survey, not primary |
| 2505.23554 | Sustainable Carbon-Aware and Water-Efficient LLM Scheduling in Geo-Distributed Cloud Datacenters | 29 May, 2025 | INCLUDE |

- WebSearch "carbon-aware training scheduling 2025": 9 links.

| URL | title | date | decision |
|---|---|---|---|
| https://link.springer.com/article/10.1007/s44163-026-02022-4 | A carbon aware job scheduling framework for data center sustainability using deep learning training | 2026 | EXCLUDE: qualifying, not fetched (cap) |
| https://par.nsf.gov/servlets/purl/10655792 | Carbon- and Precedence-Aware Scheduling for Data Processing Clusters | not shown | EXCLUDE: qualifying, not fetched (cap) |
| https://www.researchgate.net/publication/400558379_Carbon-Aware_Training_Schedules_for_Machine_Learning_Models_An_Energy-Efficient_Green_AI_Approach | Carbon-Aware Training Schedules for Machine Learning Models | not shown | EXCLUDE: inaccessible (ResearchGate) |
| https://dl.acm.org/doi/10.1145/3716368.3735301 | Sustainable Carbon-Aware and Water-Efficient LLM Scheduling in Geo-Distributed Cloud Datacenters (GLSVLSI 2025) | 2025 | EXCLUDE: duplicate (included in this sweep) (arXiv 2505.23554) |
| https://link.springer.com/article/10.1557/s43581-025-00146-1 | Federated carbon intelligence for sustainable AI | 2025 | EXCLUDE: qualifying, not fetched (cap) |
| https://arxiv.org/pdf/2609.13355 | LOCO 2026 Lightning Talk Abstracts | 2026-09-11 | EXCLUDE: not primary (abstract collection) |
| https://arxiv.org/pdf/2505.18357 | CarbonFlex: Enabling Carbon-aware Provisioning and Scheduling for Cloud Clusters | 2025-05 | EXCLUDE: duplicate of prior dossier (energy_accounting I11) |
| https://arxiv.org/pdf/2608.20566 | AgentDecarbonizer: Carbon-Aware Execution for AI Agents | 2026-08-20 | INCLUDE |
| https://dev.to/nilofer_tweets/carbon-aware-model-training-scheduling-gpu-workloads-around-electricity-carbon-intensity-b4b | Carbon-Aware Model Training (DEV Community) | not shown | EXCLUDE: not primary (blog) |

### E-Q6: "embodied carbon GPU AI accelerators"

- arXiv API: `http://export.arxiv.org/api/query?search_query=all:embodied%20carbon%20GPU%20AI%20accelerators&start=0&max_results=25&sortBy=relevance`: FAILED twice (HTTP 406 via https redirect); 0 hits parsed.
- arXiv search fallback: `https://arxiv.org/search/?query=embodied+carbon+GPU+AI+accelerators&searchtype=all&abstracts=show&order=&size=25`: 2 hits.

| arXiv id | title | submitted (latest) | decision |
|---|---|---|---|
| 2605.05615 | LLMSpace: Carbon Footprint Modeling for Large Language Model Inference on LEO Satellites | 7 May, 2026 | EXCLUDE: qualifying, not fetched (cap) |
| 2207.01209 | Sustainable AI Processing at the Edge | 4 July, 2022 | EXCLUDE: outside window (2022) |

- WebSearch "embodied carbon GPU AI accelerators": 9 links.

| URL | title | date | decision |
|---|---|---|---|
| https://arxiv.org/html/2501.15829v1 | Aging-aware CPU Core Management for Embodied Carbon Amortization in Cloud LLM Inference | 2025-01-27 | INCLUDE |
| https://dl.acm.org/doi/10.1145/3679240.3734608 | Same paper, ACM e-Energy '25 | 2025 | EXCLUDE: duplicate (included in this sweep) |
| https://introl.com/blog/carbon-accounting-ai-workloads-gpu-emissions-tracking-2025 | Carbon Accounting for AI Workloads (Introl Blog) | not shown | EXCLUDE: not primary (blog) |
| https://digitalcommons.morris.umn.edu/cgi/viewcontent.cgi?article=1004&context=urs_2025 | The Hidden Carbon Footprint of AI Models: GPU-Aware ... | 2025 | EXCLUDE: qualifying, not fetched (cap) (student symposium paper) |
| https://www.techinsights.com/blog/ai-carbon-challenge-why-your-next-gpus-memory-stack-new-emissions-hotspot | The AI Carbon Challenge: ... Memory Stack Is the New Emissions Hotspot | not shown | EXCLUDE: not primary (industry blog; projections not traceable to a fetched primary) |
| https://www.arxiv.org/pdf/2502.05043 | EcoServe (www.arxiv.org) | 2025 | EXCLUDE: duplicate (included in this sweep) |
| https://arxiv.org/pdf/2504.09851v1 | Carbon-Efficient 3D DNN Acceleration (v1) | 2025-04 | INCLUDE (fetched as v2) |
| https://arxiv.org/pdf/2502.05043v1 | EcoServe v1 | 2025-02 | EXCLUDE: duplicate (included in this sweep) |
| https://arxiv.org/html/2504.09851v2 | Carbon-Efficient 3D DNN Acceleration (v2) | 2025-05-29 | EXCLUDE: duplicate (included in this sweep) |

### E-Q7: "MLPerf power"

- arXiv API: `http://export.arxiv.org/api/query?search_query=all:MLPerf%20power&start=0&max_results=25&sortBy=relevance`: FAILED twice (HTTP 406 via https redirect); 0 hits parsed.
- arXiv search fallback: `https://arxiv.org/search/?query=MLPerf+power&searchtype=all&abstracts=show&order=&size=25`: 9 hits.

| arXiv id | title | submitted (latest) | decision |
|---|---|---|---|
| 2606.27704 | AdvScan: Black-Box Adversarial Example Detection at Runtime through Power Analysis | 26 June, 2026 | EXCLUDE: off-topic (adversarial detection) |
| 2410.12032 | MLPerf Power: Benchmarking the Energy Efficiency of Machine Learning Systems from Microwatts to Megawatts for Sustainable AI | 5 February, 2025 | INCLUDE |
| 2406.16791 | Enabling more efficient and cost-effective AI/ML systems with Collective Mind, virtualized MLOps, MLPerf, Collective Knowledge Playground and reproducible optimization tournaments | 1 December, 2024 | EXCLUDE: off-topic (MLOps tooling) |
| 2310.07217 | Enhancing Neural Architecture Search with Multiple Hardware Constraints for Deep Learning Model Deployment on Tiny IoT Devices | 11 October, 2023 | EXCLUDE: outside window (2023) |
| 2206.00302 | Multi-Complexity-Loss DNAS for Energy-Efficient and Memory-Constrained Deep Neural Networks | 1 June, 2022 | EXCLUDE: outside window (2022) |
| 2106.07597 | MLPerf Tiny Benchmark | 24 August, 2021 | EXCLUDE: outside window (2021) |
| 2105.09187 | High performance and energy efficient inference for deep learning on ARM processors | 19 May, 2021 | EXCLUDE: outside window (2021) |
| 2008.07141 | AIPerf: Automated machine learning as an AI-HPC benchmark | 14 March, 2021 | EXCLUDE: outside window (2020) |
| 1911.02549 | MLPerf Inference Benchmark | 9 May, 2020 | EXCLUDE: outside window (2019) |

- WebSearch "MLPerf power": 9 links.

| URL | title | date | decision |
|---|---|---|---|
| https://arxiv.org/abs/2410.12032 | MLPerf Power: Benchmarking the Energy Efficiency of ML Systems from Microwatts to Megawatts | 2024-10 (v2 2025-02-06) | INCLUDE |
| https://ieeexplore.ieee.org/abstract/document/10946778/ | MLPerf Power (IEEE HPCA 2025) | 2025 | EXCLUDE: duplicate (included in this sweep) |
| https://arxiv.org/pdf/2410.12032 | MLPerf Power (PDF) | 2025 | EXCLUDE: duplicate (included in this sweep) |
| https://github.com/aryatschand/MLPerf-Power-HPCA-2025 | GitHub - MLPerf-Power-HPCA-2025 | not shown | EXCLUDE: inaccessible (github.com refused by proxy) |
| https://www.researchgate.net/publication/384974304_MLPerf_Power_Benchmarking_the_Energy_Efficiency_of_Machine_Learning_Systems_from_muWatts_to_MWatts_for_Sustainable_AI | MLPerf Power (ResearchGate) | not shown | EXCLUDE: duplicate (included in this sweep) |
| https://arxiv.org/pdf/2512.03024 | TokenPowerBench: Benchmarking the Power Consumption of LLM Inference | 2025-12-02 | INCLUDE |
| https://mlcommons.org/2025/03/ml-commons-power-hpca/ | MLCommons Power Working Group Presents MLPerf Power benchmark at IEEE HPCA | 2025-03 | EXCLUDE: not primary (announcement) |
| https://mlcommons.org/benchmarks/inference-datacenter/ | Benchmark MLPerf Inference: Datacenter | MLCommons V6.1 | not shown | EXCLUDE: not primary (results portal; no text claim needed) |
| https://mlcommons.org/working-groups/benchmarks/power/ | Power - MLCommons | not shown | EXCLUDE: not primary (working-group page) |

### E-Q8: "AI Energy Score"

- arXiv API: `http://export.arxiv.org/api/query?search_query=all:AI%20Energy%20Score&start=0&max_results=25&sortBy=relevance`: FAILED twice (HTTP 406 via https redirect); 0 hits parsed.
- arXiv search fallback: `https://arxiv.org/search/?query=AI+Energy+Score&searchtype=all&abstracts=show&order=&size=25`: 25 hits.

| arXiv id | title | submitted (latest) | decision |
|---|---|---|---|
| 2609.03716 | Artificial Intelligence for Energy Optimization in Data Centers | 3 September, 2026 | EXCLUDE: off-topic (AI for data-centre energy) |
| 2609.00665 | Triple-Bottom-Line Sustainability of Language Models for Edge AI: A Comparison Between SLMs and Quantized LLMs | 31 August, 2026 | EXCLUDE: qualifying, not fetched (cap) |
| 2608.08954 | Do AI Forecast Ensembles Sample the Correct Conditional Distribution? | 9 August, 2026 | EXCLUDE: off-topic |
| 2608.11830 | Quantifying the Relationship Between Clinical Safety and Environmental Impact in Therapeutic LLMs | 12 August, 2026 | EXCLUDE: qualifying, not fetched (cap) |
| 2608.20540 | GOES-East full-disk AI nowcasting of cloud evolution in observation space | 20 August, 2026 | EXCLUDE: off-topic |
| 2608.29403 | Kac's Walk on Rotation Matrices Mixes in $\boldsymbol{Θ(n^2)}$ Steps: A Proof Discovered with AI | 1 September, 2026 | EXCLUDE: off-topic |
| 2608.01377 | CraftAlign: Feature-Grounded Evaluation and Revision Guidance for AI Stories | 2 August, 2026 | EXCLUDE: off-topic |
| 2608.11545 | DLESyM-Ocean: A Deep Learning Probabilistic Global Model for Simulating Present-Day Upper Ocean and Sea Ice | 11 August, 2026 | EXCLUDE: off-topic |
| 2608.07427 | A Picture is Worth a Thousand Tokens: How Vision Language Models Cut AI Energy Costs While Improving Accuracy | 7 August, 2026 | EXCLUDE: duplicate (listed under earlier query) |
| 2608.17270 | Do LLMs Know a Good Hypothesis When They See One? Logit-Based Energy Scoring Outperforms Prompted LLM-as-Judge for Scientific Hypothesis Ranking | 17 August, 2026 | EXCLUDE: off-topic |
| 2607.22604 | The Fallacy of Sustainable Generative AI: Limitations in EU Environmental Regulation of Data Centres and Paths Forward | 13 June, 2026 | EXCLUDE: qualifying, not fetched (cap) (policy) |
| 2607.09737 | Q-Score: A Quantum-Native Scoring Function for Molecular Docking | 2 July, 2026 | EXCLUDE: off-topic |
| 2607.04374 | An End-to-End Explainable AI Framework with Automated LLM-Based Natural Language Explanation Generation for Energy Systems | 5 July, 2026 | EXCLUDE: off-topic |
| 2607.05100 | AIFS-SUBS: Extending Data-Driven Forecasting to Sub-Seasonal Timescales | 6 July, 2026 | EXCLUDE: off-topic |
| 2607.26324 | Planning Waste-to-Energy-Coupled AI Data Centers Through Grade-Matched Cooling and Corridor Screening | 28 July, 2026 | EXCLUDE: off-topic |
| 2607.10942 | Edge Physical AI Deployment of Vision Transformers on Heterogeneous Edge GPU Targeting Autonomous Vehicles | 12 July, 2026 | EXCLUDE: off-topic |
| 2607.13930 | NNStar: An end-to-end AI agent for nuclear matter and neutron star physics | 15 July, 2026 | EXCLUDE: off-topic |
| 2606.05710 | Explainable AI-Driven Cyber Risk Analytics and Model Reliability Assessment for Intelligent Governance of U.S. Critical Infrastructure: An XGBoost and SHAP-Based Intrusion Detection Framework | 4 June, 2026 | EXCLUDE: off-topic |
| 2606.13754 | D2H-AD: A Hybrid Model Utilizing Hyperdimensional Computing for Advanced Anomaly Detection | 11 June, 2026 | EXCLUDE: off-topic |
| 2606.19427 | Physics-guided discovery of dynamical dark-energy equations of state through iterative AI reasoning | 17 June, 2026 | EXCLUDE: off-topic |
| 2606.09576 | Characterizing Stellar Streams with Error-Aware Machine Learning | 8 June, 2026 | EXCLUDE: off-topic |
| 2606.07455 | A 65 nm Trustworthy Hypoglycemia Forecasting Engine Achieving 11.3 nJ per Inference | 14 June, 2026 | EXCLUDE: off-topic |
| 2606.14707 | Green AI Carbon Optimizer: Carbon-Efficient Training Location Recommendation and Global AI Energy Demand Forecasting | 6 April, 2026 | EXCLUDE: qualifying, not fetched (cap) |
| 2606.09537 | STEPS: Semantic Contract-Guided Scheduling for LLM-Assisted Natural Language-Driven Edge AI Services | 15 June, 2026 | EXCLUDE: off-topic |
| 2606.29981 | Hephaestus: Toward a Cybersecurity AI Scientist | 29 June, 2026 | EXCLUDE: off-topic |

- WebSearch "AI Energy Score": 9 links.

| URL | title | date | decision |
|---|---|---|---|
| https://oecd.ai/en/catalogue/tools/ai-energy-score | AI Energy Score - OECD.AI | not shown | EXCLUDE: not primary (catalogue entry) |
| https://www.salesforce.com/news/stories/ai-energy-score/ | Salesforce Joins ... to Unveil AI Energy Score | not shown | EXCLUDE: not primary (press release) |
| https://huggingface.co/blog/sasha/ai-energy-score-v2 | AI Energy Score v2: Refreshed Leaderboard, now with Reasoning | 2025-12-04 | INCLUDE |
| https://huggingface.co/blog/sasha/announcing-ai-energy-score | Announcing AI Energy Score Ratings | 2025-02 | EXCLUDE: qualifying, not fetched (cap) (v2 supersedes) |
| https://github.com/huggingface/AIEnergyScore | GitHub - huggingface/AIEnergyScore | not shown | EXCLUDE: inaccessible (github.com refused by proxy) |
| https://www.sustainableaicoalition.org/ai-energy-score-a-standardized-approach-to-evaluating-ai-model-energy-efficiency/ | AI Energy Score - Coalition for Sustainable AI | not shown | EXCLUDE: not primary |
| https://huggingface.co/AIEnergyScore | AIEnergyScore (HF organisation page) | not shown | EXCLUDE: not primary |
| https://huggingface.github.io/AIEnergyScore/ | AI Energy Score documentation site | not shown | EXCLUDE: qualifying, not fetched (cap) (documentation) |
| https://aitransparencyinstitute.com/ai-energy-score-ratings/ | AI Energy Score Ratings - AI Transparency Institute | not shown | EXCLUDE: not primary |

### Must-include works

- Luccioni et al. 2025 on rebound effects: found by E-Q3 (arXiv search and WebSearch): 2501.16548v2, included (S-rebound).
- MLPerf Power: found by E-Q7: 2410.12032v2, included.
- A 2025-2026 reasoning-energy measurement: found by E-Q1 and E-Q8: AI Energy Score v2 (HF, 2025-12-04; inference) and Morrison, Smith, Strubell 2026 (2605.01158v1; post-training), both included; also 2608.12350v1 (reasoning vs non-reasoning inference). Oviedo et al. (Joule 2026, 2509.20241) and 2601.22076 were hit but are already in the prior energy dossiers.

### Qualifying, not fetched (cap)

arXiv: 2410.14740, 2412.17376, 2509.08980, 2604.02776, 2604.10852, 2605.00300, 2605.05615, 2606.14707, 2606.21833, 2607.09520, 2607.20806, 2607.22604, 2608.07427, 2608.11830, 2608.12915, 2608.28667, 2609.00665, 2609.11940, 2609.15230. Web: https://arxiv.org/pdf/2507.11417, https://arxiv.org/pdf/2510.01889, https://arxiv.org/pdf/2602.24091, https://arxiv.org/pdf/2603.23075, https://arxiv.org/pdf/2604.16682, https://digitalcommons.morris.umn.edu/cgi/viewcontent.cgi?article=1004&context=urs_2025, https://doi.org/10.3390/su172310473, https://huggingface.co/blog/sasha/announcing-ai-energy-score, https://huggingface.github.io/AIEnergyScore/, https://link.springer.com/article/10.1007/s44163-026-02022-4, https://link.springer.com/article/10.1557/s43581-025-00146-1, https://par.nsf.gov/servlets/purl/10655792, https://sciintl.scione.com/cms/fulltext.php?id=341.

