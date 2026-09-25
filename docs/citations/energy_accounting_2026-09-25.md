# Energy of AI systems: measurement, accounting and three mechanism families (fetched 2026-09-25)

Family: **accounting**. Literature dossier made on the day (R10). Every quote below is a verbatim substring of the raw text
saved at `<scratchpad>/energy_lit/accounting/<file>.txt` after html-unescape, removal of soft hyphens and "-\n" joins, and
whitespace collapse (pypdf ligatures such as "ﬁ" and missing spaces are kept as extracted). The check script
`<scratchpad>/energy_lit/accounting/check_quotes.py` (rows) and `check_dossier.py` (this file) re-verify them.
Rows: `<scratchpad>/energy_lit/accounting_rows.json` (21 rows: E13 × 7, I10 × 7, I11 × 7).

This is a note, not evidence (R8). The dossier only extracts what the sources print. It does not grade them and does not
interpret them in terms of CRR.

Fetch failures on the day:
- iea.org returned **403** for every page tried: `/reports/energy-and-ai`, `/reports/energy-and-ai/executive-summary`, the
  2025 press release, `/reports/key-questions-on-energy-and-ai/executive-summary` (April 2026) and the 2026 news release.
  WebFetch was also refused with 403. A guessed blob-storage PDF URL returned 404. The IEA figures below are therefore quoted
  from secondary reports, named in each case.
- de Vries 2023 (Joule, "The growing energy footprint of artificial intelligence"): cell.com and sciencedirect.com returned
  **403**. It is not quoted directly. Its 3 Wh per-query figure appears below only as Epoch AI reports it.
- ACM DL PDF of GEMINI (SOSP 2023) returned **403**. The authors' PDF from rice.edu was fetched instead.
- LBNL report: the `eta-publications.lbl.gov/.../lbnl-2024-...-report.pdf` link and escholarship returned **403**. The
  `..._1.pdf` variant returned 200 and was used. The "2025 Update" (escholarship item 33m6w3x0) returned **403** and was not read.
- datacenterdynamics.com, enlit.world and cnbc.com returned 403, and euronews.com returned 406. None of these is quoted.

---

## A. Accounting figures

### A1. IEA, "Energy and AI" (April 2025), as reported by Carbon Brief and Brookings
- Primary: https://www.iea.org/reports/energy-and-ai returned **403** (proxy and WebFetch).
- Secondary 1: Carbon Brief, "AI: Five charts that put data-centre energy use – and emissions – into context", datePublished
  2025-09-15. URL https://www.carbonbrief.org/ai-five-charts-that-put-data-centre-energy-use-and-emissions-into-context (200).
  Raw text: `accounting/carbonbrief_iea_2025.txt`
> "Under the IEA’s central scenario for data-centre growth, the sector’s global electricity consumption would more than double between 2024 and 2030, reaching 945 terawatt-hours (TWh) by the end of the decade."

> "As it stands, AI has been responsible for around 5-15% of data-centre power use in recent years, but this could increase to 35-50% by 2030, according to another report prepared for the IEA."

> "data centres are currently responsible for just over 1% of global electricity demand and 0.5% of CO2 emissions, according to IEA data."

- Secondary 2: Brookings, "Global energy demands within the AI regulatory landscape", datePublished 2026-04-10.
  URL https://www.brookings.edu/articles/global-energy-demands-within-the-ai-regulatory-landscape/ (200).
  Raw text: `accounting/brookings.txt`
> "The IEA, in its base case scenario, projects that global data center electricity consumption could reach 945 TWh by 2030, climbing further to 1,200 TWh by 2035."

### A2. IEA, "Key Questions on Energy and AI" (April 2026): no reputable secondary source could be fetched
- Primary: 403. Search-engine snippets (not fetched text, so not quoted here) attribute to it the following: data-centre
  electricity demand grew 17% in 2025 to about 485 TWh, AI-focused data centres grew about 50%, and demand is projected to
  reach about 950 TWh in 2030. The only page that could be fetched with these figures is a vendor blog (Sardina Systems,
  datePublished 2026-04-30,
  https://www.sardinasystems.com/news/ais-electricity-problem-or-what-the-latest-data-actually-shows/). It is not an
  independent source, and it gives 15% where the snippets give 17%. It is quoted only to show what was retrievable.
  Raw text: `accounting/sardina.txt`
> "In 2025, global data centre electricity consumption grew by 15%. AI-focused facilities grew faster still — up 50% in a single year. The IEA’s latest report, Key Questions on Energy and AI (April 2026) , puts the updated trajectory plainly: consumption will roughly double and reach almost 500 TWh in 2025 to 950 TWh by 2030"

### A3. Elsworth et al. (Google) 2025, "Measuring the environmental impact of delivering AI at Google Scale"
- arXiv 2508.15734, current **v1** (Thu, 21 Aug 2025). URL https://arxiv.org/pdf/2508.15734 (200). Raw text: `accounting/2508.15734.txt`
> "we find the median Gemini Apps text prompt consumes 0.24 Wh of energy—a figure substantially lower than many public estimates."

> "the primary energy draw originates from the active AI Accelerator power (0.14 Wh, 58% of total) and the necessary host CPU & DRAM power (0.06 Wh, 25%). The energy consumed by provisioned idle machines and the data center overhead (PUE) each contribute 0.02 Wh (10% and 8% respectively)."

> "The results for the median Gemini Apps text prompt presented in this paper vary from a more narrowly defined Existing Approach (10,000 prompts per kWh) to the more complete Comprehensive Approach (4,167 prompts per kWh) proposed."

> "Google’s software efficiency efforts and clean energy procurement have driven a 33x reduction in energy consumption and a 44x reduction in carbon footprint for the median Gemini Apps text prompt over one year."

> "a median Gemini Apps text prompt generates 0.03 gCO2e and consumes 0.26 mL of water when measured comprehensively."

### A4. Morrison et al. 2025, "Holistically Evaluating the Environmental Impact of Creating Language Models" (ICLR 2025): the development share
- arXiv 2503.05804, current **v1** (Mon, 3 Mar 2025). URL https://arxiv.org/pdf/2503.05804 (200). Raw text: `accounting/2503.05804.txt`
- **The key figure.** Model development (hyperparameter tuning, ablations and experiments before the final runs) used
  **459 MWh**. The final training runs used **913 MWh**. So development was about 50% of final training (the paper: "∼50%").
> "we find that model development, the impact of which is generally not disclosed by most model developers, amounted to∼50% of that of training."

> "early model development (e.g., hyperparameter tuning and experiments before the final training run), training of the main model, and inference."

> "GPU Hours Total MWh # Runs Carbon Emissions (tCO2eq) Equivalent to... (energy usage, 1 home, U.S.) Water Consumption (kL) Equivalent to... (water usage, 1 person) <1B 29k 19 20 6 1 yr, 4 mo 24 3 mo 7B 269k 196 375 65 13 yrs, 6 mo 252 2 yrs, 7 mo 13B 191k 116 156 46 9 yrs, 7 mo 402 3 yrs, 7 mo MoE 27k 19 35 6 1 yr, 4 mo 24 3 mo Total 680k 459 813 159 33 yrs, 1 mo 843 7 yrs, 5 mo"

> "Total (Ours) 913 312 65 years 1,921 17 yrs, 1 mo"

> "we find that our development runs led to 159 tCO 2eq emitted and 843 kL of water consumed."

> "In summary, we find that our training runs led to 312 tCO2eq emitted and 1,921 kL of water consumed."

> "In total, our series of models led to at least 493 tCO2eq emitted."

> "power usage throughout training is not consistent, fluctuating between ∼15% and∼85% of our hardware’s maximum power draw"

> "When actively training, the average GPU power is over 600W, over 85% of an H100’s maximum power draw of 700W, and during checkpointing, power usage drops to just over 100W, or about 15% maximum."

> "We find that for most models tested, the number of inferences required to outweigh training costs is in the hundreds of millions to tens of billions, except for the most over-trained models."

> "As we only measure GPU power consumption, our estimates should be viewed as a lower bound on the true amount of power consumed during development and training."

### A5. Luccioni, Viguier, Ligozat 2022, "Estimating the Carbon Footprint of BLOOM, a 176B Parameter Language Model" (JMLR 2023)
- arXiv 2211.02001, current **v1** (Thu, 3 Nov 2022). URL https://arxiv.org/pdf/2211.02001 (200). Raw text: `accounting/2211.02001.txt`
- The final BLOOM run used 433,196 kWh of the project's 1,163,088 kWh of dynamic energy (Table 5). That is 37.24% of the
  dynamic emissions.
> "176B BLOOM Model 433,196 24.69 37.24% 104B Model 266,522 15.19 22.92% 1B Model 158,972 9.06 13.68% 13B Model 87,210 4.97 7.49% Other Models 64,257 3.66 5.53% Miscellaneous Processes 57,961 3.3 4.98% 6B Model 51,686 2.95 4.45% Model Evaluation 43,172 2.46 3.71% Total 1,163,088 66.29 100.00% Table 5: Breakdown of dynamic energy consumption and CO2 emissions of different parts of the BigScience project"

> "if we consider the totality of experiments run by members of the BigScience project, they add up to a total of 3.46 million GPU hours (2.2 million hours of which used V100 GPUs and 1.24 million hours used A100 GPUs), which represents an electrical consumption of 1,163,032 kWh of electricity and approximately 66.29 tonnes of CO2eq emitted via dynamic power consumption."

> "It is interesting to note that experimenting with intermediate models (such as the 104B, 13B and 1B models) add up to a total of 35.8 tonnes of CO2eq, which is more than the training of the ﬁnal model."

> "the authors of the OPT paper, who stated that the total carbon footprint of their model is roughly 2 times higher due to experimentation, baselines and ablations [ 37]."

> "we believe it is worth noting the high proportion of energy dedicated to maintaining a LLM like BLOOM in memory (approximately 75% of the total energy consumed by the instance)"

- Note: the text prints 1,163,032 kWh and Table 5 prints 1,163,088 kWh. Both are kept as printed.

### A6. Luccioni, Jernite, Strubell 2024, "Power Hungry Processing: Watts Driving the Cost of AI Deployment?" (FAccT 2024)
- arXiv 2311.16863, current **v3** (Tue, 15 Oct 2024). URL https://arxiv.org/pdf/2311.16863 (200). Raw text: `accounting/2311.16863.txt`
> "classification tasks for both images and text are on the lower end of the spectrum in terms of emissions (ranging between 0.002 and 0.007 kWh for 1,000 inferences)"

> "generative tasks such as text generation and summarization use, on average, over 10 times more energy for the same number of inferences (around 0.05 kWh for 1,000 inferences), and multimodal tasks such as image captioning and image generation are on the highest end of the spectrum (0.06-2.9 kWh for 1,000 inferences)."

> "Training energy (kWh) 51,686 25,634 17,052 10,505 Finetuning energy (kWh) 7,571 3,242 1,081 543 Inference energy (kWh) 1.0 × 10−4 7.3 × 10−5 6.2 × 10−5 5.4 × 10−5 Cost parity (# inferences) 592,570,000 395,602,740 292,467,741 204,592,592"

> "from around 200 million inferences for the smallest model, BLOOMz-560M, to over 590 million inferences for the biggest model, BLOOMz-7B."

### A7. Patterson et al. 2021, "Carbon Emissions and Large Neural Network Training"
- arXiv 2104.10350, current **v3** (Fri, 23 Apr 2021). URL https://arxiv.org/pdf/2104.10350 (200). Raw text: `accounting/2104.10350.txt`
> "Energy Consumption (MWh) 7.5 85.7 232 24.1 179 1,287"

> "For example, NVIDIA estimated that 80–90% of the ML workload is inference processing [Leo19]. Similarly, Amazon Web services claimed that 90% of the ML demand in the cloud is for inference [Bar19]."

> "Remarkably, the choice of DNN, datacenter, and processor can reduce the carbon footprint up to ~100-1000X."

- The six energy columns of that table are T5, Meena, GShard-600B, Switch Transformer, GPT-3 and (the last) GPT-3 at 1,287 MWh.
  The column header is garbled in the extraction. The dossier relies only on the paper's own statement "GPT-3 ... 1,287 MWh",
  which also appears in the BLOOM paper's Table 4 (`2211.02001.txt`: "9 gCO2eq/kWh 1,287 MWh 502 tonnes 552 tonnes").

### A8. Patterson et al. 2022, "The Carbon Footprint of Machine Learning Training Will Plateau, Then Shrink"
- arXiv 2204.05149, current **v1** (Mon, 11 Apr 2022). URL https://arxiv.org/pdf/2204.05149 (200). Raw text: `accounting/2204.05149.txt`
> "Each time the ML portion was 10% to 15% of Google's total energy consumption for that week despite ML representing 70%-80% of the FLOPS at Google"

> "Across all three years, about ⅗ of ML energy use is for inference and ⅖ for training. These measurements include all ML energy usage: research, development, testing, and production."

### A9. Wu et al. 2022, "Sustainable AI: Environmental Implications, Challenges and Opportunities" (MLSys 2022)
- arXiv 2111.00364, current **v2** (Sun, 9 Jan 2022). URL https://arxiv.org/pdf/2111.00364 (200). Raw text: `accounting/2111.00364.txt`
> "At Facebook, we observe a rough power capacity breakdown of 10:20:70 for AI infrastructures devoted to the three key phases — Experimentation, Training, and Inference"

> "the energy footprint of RM1 is roughly 31:29:40 over Data, Experimentation/Training, and Inference"

> "For recommendation use cases, we ﬁnd the carbon footprint is split evenly between training and inference. On the other hand, the carbon footprint of LM is dominated by the inference phase, using much higher inference resources (65%) as compared to training (35%)."

### A10. Strubell, Ganesh, McCallum 2019, "Energy and Policy Considerations for Deep Learning in NLP" (ACL 2019)
- arXiv 1906.02243, current **v1** (Wed, 5 Jun 2019). URL https://arxiv.org/pdf/1906.02243 (200). Raw text: `accounting/1906.02243.txt`
> "Transformer (big) 192 w/ neural architecture search 626,155"

> "During that time 123 small hyperparameter grid searches were performed, resulting in 4789 jobs in total."

> "The sum GPU time required for the project totaled 9998 days (27 years)."

> "Research and development of new models multiplies these costs by thousands of times by requiring retraining to experiment with model architectures and hyperparameters."

### A11. Samsi et al. 2023, "From Words to Watts: Benchmarking the Energy Costs of Large Language Model Inference" (IEEE HPEC 2023)
- arXiv 2310.03003, current **v1** (Wed, 4 Oct 2023). URL https://arxiv.org/pdf/2310.03003 (200). Raw text: `accounting/2310.03003.txt`
> "with length 512, we see that it takes about 3-4 Joules for a output token"

> "For a 30% reduction in power from 250W to 175W, the inference time increases by an average of 6.7% for a corresponding average reduction in total energy by 23.21%."

### A12. Chung et al. 2025, "The ML.ENERGY Benchmark: Toward Automated Inference Energy Measurement and Optimization" (NeurIPS 2025 D&B)
- arXiv 2505.06371, current **v2** (Thu, 16 Oct 2025). URL https://arxiv.org/pdf/2505.06371 (200). Raw text: `accounting/2505.06371.txt`
> "automated optimization recommendations can lead to significant (sometimes more than 40%) energy savings without changing what is being computed by the model."

> "The early 2025 iteration of the benchmark and leaderboard presents energy measurements across 40 models and 6 tasks"

- The leaderboard itself (https://ml.energy/leaderboard) was not fetched. The paper is cited in its place.

### A13. Jegham et al. 2025, "How Hungry is AI? Benchmarking Energy, Water, and Carbon Footprint of LLM Inference"
- arXiv 2505.09598, current **v6** (Mon, 24 Nov 2025). URL https://arxiv.org/pdf/2505.09598 (200). Raw text: `accounting/2505.09598.txt`
> "Results show the most energy-intensive models exceed 29 Wh per long prompt, over 65 × the most efficient systems."

> "Our framework estimates 0.42 Wh ( ±0.13 Wh) for a short GPT-4o prompt (0.37 Wh without datacenter overhead), within 19% of Altman’s figure."

> "In June 2025, OpenAI CEO Sam Altman reported that the default ChatGPT model consumed approximately 0.34 Wh per query [68]."

### A14. You (Epoch AI) 2025, "How much energy does ChatGPT use?" (Gradient Updates)
- Page date 7 Feb 2025 (pagefind:date meta). URL https://epoch.ai/gradient-updates/how-much-energy-does-chatgpt-use (200).
  Raw text: `accounting/epoch_chatgpt_energy.txt`
> "We find that typical ChatGPT queries using GPT-4o likely consume roughly 0.3 watt-hours, which is ten times less than the older estimate."

> "The original three watt-hour estimate, which has been widely cited by many different researchers and media outlets, comes from Alex de Vries (2023) ."

> "The training runs for current generation models that are comparable to GPT-4o 13 consumed around 20-25 megawatts of power each, lasting around three months."

> "using our 0.3 Wh estimate, this suggests that overall ChatGPT inference requires ~12.5 MW of power. This is comparable to the power (temporarily) required to train GPT-4o, but language models are typically used for longer than they are trained"

### A15. Shehabi et al. 2024, "2024 United States Data Center Energy Usage Report" (LBNL)
- URL https://eta-publications.lbl.gov/sites/default/files/2024-12/lbnl-2024-united-states-data-center-energy-usage-report_1.pdf (200). The version without "_1" returned 403.
  Raw text: `accounting/lbnl2024.txt`
> "U.S. data center energy use has continued to grow at an increasing rate, reaching 176 TWh by 2023, representing 4.4% of total U.S. electricity consumption."

> "the scenario variations provide a range of total data center energy estimates, with the low and high end of roughly 325 and 580 TWh in 2028"

> "This annual energy use also represents 6.7% to 12.0% of total U.S. electricity consumption forecasted for 2028."

> "A crucial distinction exists between training and inference workloads."

### A16. Oviedo et al. (Microsoft) 2025/2026, "Energy Use of AI Inference, Efficiency Pathways, and Test-Time Scaling" (Joule 2026)
- arXiv 2509.20241, current **v2** (Tue, 9 Jun 2026). URL https://arxiv.org/pdf/2509.20241 (200). The Joule version on cell.com
  was not fetched (the domain returns 403). Raw text: `accounting/2509.20241.txt`
> "For frontier-scale models (>200B parameters) on H100 nodes, we estimate a median energy of 0.31 Wh/query (IQR 0.16– 0.60), indicating widely cited estimates are overstated by 4–20×."

> "In test-time scaling scenarios 15× longer than typical queries, the median energy rises 13× to 3.91 Wh (IQR 2.15–7.05)."

> "The greatest strain on power grids from new AI workloads is not from inference energy use, but from training loads, the rapid rate of AI adoption, and concentrated capacity build-up"

### A17. 2024-2026 statements on the training-vs-inference share
None of the fetched 2024-2026 papers makes a new measured estimate of the global training/inference split. The figures
they cite trace back to Patterson 2022 (Google, about 3/5 inference) and Wu 2022 (Meta, 10:20:70).
- Yang, Adamek, Armour 2024, "Double-Exponential Increases in Inference Energy", arXiv 2412.09731 **v1** (Thu, 12 Dec 2024).
  Raw text: `accounting/2412.09731.txt`
> "Google reported that the energy consumption of machine learning (ML) workloads constituted 10–15% of its total energy usage from 2019 to 2021, with training accounting for 40% and inference for 60% [1]. Similarly, Meta observed a power capacity distribution of 10:20:70 among experimentation, training, and inference in their AI infrastructure [2]."

- Tchakoute and Tadonki 2026, "Energy-Aware Computing in the Year 2026" (survey), arXiv 2605.24569 **v1** (Sat, 23 May 2026).
  It gives no number. Raw text: `accounting/2605.24569.txt`
> "hyperscaler telemetry from 2024–2026 indicates thatInferencenow accounts for the vast majority of the overall AI energy footprint."

---

## B. Mechanism sources

### E13: frequent, fast, in-memory or asynchronous checkpointing and fault tolerance

**Mohan, Phanishayee, Chidambaram 2021, "CheckFreq: Frequent, Fine-Grained DNN Checkpointing" (USENIX FAST 2021).**
URL https://www.usenix.org/system/files/fast21-mohan.pdf (200); no arXiv version. Raw text: `accounting/checkfreq_fast21.txt`
> "CheckFreq can reduce the recovery time from hours to seconds while bounding the runtime overhead within 3.5%."

> "CheckFreq reduces the end-to-end training time by 2× when training a ResNet50 job on a 1080Ti GPU, and by 1.6 × for a ResNext101 job on a V100 GPU, when the job is interrupted every 5 hours in both cases."

**Wang et al. 2023, "Gemini: Fast Failure Recovery in Distributed Training with In-Memory Checkpoints" (SOSP 2023).**
The ACM DL returned 403. Authors' PDF: https://www.cs.rice.edu/~eugeneng/papers/SOSP23.pdf (200). Raw text: `accounting/gemini_sosp23.txt`
> "Gemini reduces the checkpoint retrieval time by up to 250× and improves the checkpoint frequency by up to 8×. As a result, Gemini achieves a faster failure recovery by more than 13× without incurring overhead on training throughput."

**Llama Team (Grattafiori, Dubey et al.) 2024, "The Llama 3 Herd of Models".** arXiv 2407.21783, current **v3** (Sat, 23 Nov 2024). Raw text: `accounting/2407.21783.txt`
> "for Llama 3, we achieved higher than 90% effective training time while supporting automated cluster maintenance"

> "During a 54-day snapshot period of pre-training, we experienced a total of 466 job interruptions. Of these, 47 were planned interruptions"

> "We aim to minimize GPU pause time during checkpointing and increase checkpoint frequency to reduce the amount of lost work after a recovery."

> "it can result in instant fluctuations of power consumption across the data center on the order of tens of megawatts, stretching the limits of the power grid."

**Jiang et al. 2024, "MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs" (NSDI 2024).** arXiv 2402.15627, current **v1** (Fri, 23 Feb 2024). Raw text: `accounting/2402.15627.txt`
> "the system can catch up to the training progress prior to the crash within 15 minutes from the latest checkpoints, maintaining over 90% effective training time rate"

> "This require us to increase the frequency of checkpointing during training."

**Wan et al. 2024/2025, "ByteCheckpoint: A Unified Checkpointing System for Large Foundation Model Development" (NSDI 2025).** arXiv 2407.20143, current **v4** (Wed, 2 Apr 2025). Raw text: `accounting/2407.20143.txt`
> "Compared to the baselines, ByteCheckpoint achieves improvements ranging from 12.13× to 161.50× in terms of checkpoint stalls reduction, making the end-to-end checkpoint saving and loading procedures 6.05× and 3.88× faster on average, respectively."

**Kokolis et al. 2025, "Revisiting Reliability in Large-Scale Machine Learning Research Clusters" (HPCA 2025).** arXiv 2410.21680, current **v2** (Thu, 6 Feb 2025). Raw text: `accounting/2410.21680.txt`
> "To obtain a good ETTR (≳ 0.9) for a job of this size, RSC-1 failure rate either needs to improve from 6.50 to ∼1 or checkpoint write overhead needs to be under a minute O(10s), achievable with asynchronous checkpoint writing"

**Wan et al. 2025, "Robust LLM Training Infrastructure at ByteDance" (ByteRobust).** arXiv 2509.16293, current **v4** (Mon, 20 Oct 2025). Raw text: `accounting/2509.16293.txt`
> "ByteRobust is deployed on a production GPU platform and advances the state of the art in training robustness by achieving 97% ETTR for a three-month training job on 9,600 GPUs."

> "As Table 8 shows, ByteRobust save cuts blocking time by 99.69% and 95.10% versusMegatron saveandMemory save."

**Zhao et al. 2025, "FFTrainer: Fast Failover in Large-Language Model Training with Almost-Free State Management".** arXiv 2512.03644, current **v1** (Wed, 3 Dec 2025). Raw text: `accounting/2512.03644.txt`
> "Compared with prior checkpointing approaches, FFTrainer reduces recovery time by up to 98% and mitigates GPU utilization loss by up to 68% without hindering normal training."

### I10: GPU power capping and frequency scaling
**You, Chung, Chowdhury 2023, "Zeus: Understanding and Optimizing GPU Energy Consumption of DNN Training" (NSDI 2023).**
arXiv 2208.06102, current **v2** (Thu, 29 Sep 2022). The NSDI PDF https://www.usenix.org/system/files/nsdi23-you.pdf (200) was used. Raw text: `accounting/zeus_nsdi23.txt`
> "We found that the optimal energy consumption (Power Limit Opt. in Figure 1) may happen at a lower power limit than the maximum and can reduce energy consumption by 3.0%–31.5%."

> "Zeus reduces energy consumption by 15.3%–75.8% and training time by 60.6% w.r.t. simply selecting the maximum batch size and maximum GPU power limit."

**Chung et al. 2024, "Reducing Energy Bloat in Large Model Training" (Perseus, SOSP 2024).** arXiv 2312.06902, current **v3** (Mon, 23 Sep 2024). Raw text: `accounting/2312.06902.txt`
> "Perseus reduces the energy consumption of large model training by up to 30% without any throughput loss or hardware modification."

**McDonald et al. 2022, "Great Power, Great Responsibility: Recommendations for Reducing Energy for Training Language Models" (NAACL Findings 2022).** arXiv 2205.09646, current **v1** (Thu, 19 May 2022). Raw text: `accounting/2205.09646.txt`
> "a 150W bound on power utilization led to an average 13.7% decrease in energy usage and 6.8% increase in training time compared to the default maximum."

> "Compared to 250W, a 100W setting required double the inference time (a 114% increase) and consumed 11.0% less energy, 150W required 22.7% more time and saved 24.2% the energy, and 200W required 8.2% more time with 12.0% less energy."

**Samsi et al. 2023** (A11 above), Table III: power caps of 175W and 150W on LLaMA 65B inference.

**Stojkovic et al. 2024, "Towards Greener LLMs: Bringing Energy-Efficiency to the Forefront of LLM Inference".** arXiv 2403.20306, current **v1** (Fri, 29 Mar 2024). Raw text: `accounting/2403.20306.txt`
> "For most batch sizes, running the GPUs at 1.6GHz instead of 2GHz yields about the same throughput at less than 80% of the energy."

**Stojkovic et al. 2024/2025, "DynamoLLM: Designing LLM Inference Clusters for Performance and Energy Efficiency" (HPCA 2025).** arXiv 2408.00741, current **v1** (Thu, 1 Aug 2024). Raw text: `accounting/2408.00741.txt`
> "DynamoLLM conserves 53% energy and 38% operational carbon emissions, and reduces 61% cost to the customer, while meeting the latency SLOs."

- DynamoLLM reconfigures instance count, parallelism and frequency together. It is not a frequency-only comparison, so it has no row.

**Liu et al. 2025, "GreenLLM: SLO-Aware Dynamic Frequency Scaling for Energy-Efficient LLM Serving".** arXiv 2508.16449, current **v1** (Fri, 22 Aug 2025). Raw text: `accounting/2508.16449.txt`
> "GreenLLM achieves up to 34% reduction in total energy consumption compared to the default DVFS baseline in Alibaba/Azure trace replays, with no loss of throughput and only less than 3.5% SLO violations increase"

**Ma et al. 2026, "The Illusion of Power Capping in LLM Decode".** arXiv 2605.11999, current **v1** (Tue, 12 May 2026). Raw text: `accounting/2605.11999.txt`
> "decode draws only 137–300 W on a 700 W GPU; no cap ever triggers, because memory-bound decode saturates HBM bandwidth rather than compute and leaves power headroom untouched."

> "clock locking Pareto-dominates power capping universally, recovering up to 32% of decode energy at minimal throughput loss."

**Braga et al. 2026, "A principled approach for energy-efficient training via phase-aware GPU frequency tuning" (Paft).** arXiv 2609.24205, current **v1** (Mon, 21 Sep 2026). Raw text: `accounting/2609.24205.txt`
> "Experiments conducted on twelve widely used models show thatPaftconsistently outperforms all baselines, achieving energy savings of up to 46% with an average overhead of 4%."

### I11: carbon- or price-aware shifting and pausing of training jobs
**Dodge et al. 2022, "Measuring the Carbon Intensity of AI in Cloud Instances" (FAccT 2022).** arXiv 2206.05229, current **v1** (Fri, 10 Jun 2022). Raw text: `accounting/2206.05229.txt`
> "for very long runs like training a 6 billion parameter language model for 8 days (b), changing the start time by up to 24 hours leads to less than 1.5% reduction at best in any region."

> "short experiments like DenseNet 201 only see emissions reductions smaller than 10%, while the 6 billion transformer training run (our experiment with the largest carbon intensity) actually sees the largest decrease in emissions."

> "FS 7.0% 4.1% 2.6% 1.8% 2.5% 2.7% 5.0% 4.8% 3.9% 3.3% 3.0% P&R 9.5% 11.0% 11.4% 2.0% 2.8% 3.1% 11.0% 11.0% 10.8% 11.4% 11.3%"

**Wiesner et al. 2021, "Let's Wait Awhile: How Temporal Workload Shifting Can Reduce Carbon Emissions in the Cloud" (Middleware 2021).** arXiv 2110.13234, current **v1** (Mon, 25 Oct 2021). Raw text: `accounting/2110.13234.txt`
> "When considering the Next Workday constraint, the Non-Interrupting scheduling managed to reduced the project’s carbon emissions by 2.5 % to 6.3 %, while the Interrupting scheduling achieved reductions of 5.7 % to 8.5 %."

> "For the Semi-Weekly constraint, Non-Interrupting scheduling saved 6.1 % to 14.4 % and Interrupting scheduling 13.3 % to 18.9 % of CO2 emissions."

**Hanafy et al. 2023, "CarbonScaler: Leveraging Cloud Workload Elasticity for Optimizing Carbon-Efficiency" (SIGMETRICS / POMACS 7(3), Dec 2023).** arXiv 2302.08681, current **v2** (Thu, 19 Oct 2023). Raw text: `accounting/2302.08681.txt`
> "show that it can yield i) 51% carbon savings over carbon-agnostic execution; ii) 37% over a state-of-the-art suspend-resume policy; and iii) 8% over the best static scaling policy."

**Hanafy et al. 2025, "CarbonFlex: Enabling Carbon-aware Provisioning and Scheduling for Cloud Clusters".** arXiv 2505.18357, current **v1** (Fri, 23 May 2025). Raw text: `accounting/2505.18357.txt`
> "CarbonFlex decreases carbon emissions by ∼57% compared to a carbon-agnostic baseline and performs within 2.1% of an oracle scheduler with perfect knowledge of future carbon intensity and job length."

**Wiesner et al. 2026, "Distributed LLM Pretraining During Renewable Curtailment Windows: A Feasibility Study" (technical report).** arXiv 2602.22760, current **v1** (Thu, 26 Feb 2026). Raw text: `accounting/2602.22760.txt`
> "Preliminary results show that curtailment-aware scheduling preserves training quality while reducing operational emissions to 5–12% of single-site baselines."

> "Single-region executions emit between 11.4 and 27.1 kgCO2, depending on regional grid conditions, whereas our curtailment-aware execution emits only 1.38 kgCO2."

**McDonald et al. 2022** (above), on scheduling by PUE. Raw text: `accounting/2205.09646.txt`
> "moving a shortrunning job from daytime to nighttime may provide a roughly 10% reduction, and moving a longer, expensive job (e.g. a language model taking weeks to"

---

## Rows by mechanism

Rows are in `<scratchpad>/energy_lit/accounting_rows.json`. Each row's numbers appear in its own quotes. Relative figures
(for example "up to 30%") are stored as x_cost, and cost_metric says so. Lower or upper bounds are flagged in `note`.

| mech | source | x vs y | quality (x / y) | cost (x / y) |
|---|---|---|---|---|
| E13 | CheckFreq (FAST 2021) | iteration-level checkpointing vs epoch-based | not reported | end-to-end time 2× lower (1.6× ResNext101) |
| E13 | GEMINI (SOSP 2023) | in-memory checkpoints vs remote storage | "without overhead" | recovery >13× faster |
| E13 | ByteRobust 2509.16293v4, Table 8 | ByteRobust save vs Megatron save (70B, 128×16) | MFU 99.23 / 39.84 % | blocking 0.04 / 6.77 s |
| E13 | ByteRobust 2509.16293v4, Table 8 | Memory save (Gemini-style) vs Megatron save | MFU 70.05 / 39.84 % | blocking 1.84 / 6.77 s |
| E13 | Llama 3 2407.21783v3 §3.3.4 | fast checkpoint and restart, no reference | effective time >90 % | 466 interruptions in 54 days |
| E13 | MegaScale 2402.15627v1 | two-stage async checkpoint, no reference | effective time >90 % | catch-up within 15 min |
| E13 | Kokolis 2410.21680v2 | ~10 s write (12k GPUs) vs 5 min (2-4k GPUs), model | ETTR 0.9 / 0.9 | 10 s / — |
| I10 | Zeus (NSDI 2023) | optimal power limit vs maximum | same target accuracy | energy −3.0 to −31.5 % |
| I10 | McDonald 2205.09646v1 | 150W vs 250W (training) | — | energy −13.7 %, time +6.8 % |
| I10 | Samsi 2310.03003v1, Table III | 175W vs 250W (LLaMA 65B inference) | token rate −6.11 % | energy −23.95 % |
| I10 | Perseus 2312.06902v3 | frequency planning vs default | no throughput loss | energy up to −30 % |
| I10 | Paft 2609.24205v1 | phase-aware frequency vs baselines | overhead 4 % (avg) | energy up to −46 % |
| I10 | Ma 2605.11999v1 | clock locking vs power capping (decode) | "minimal throughput loss" | up to 32 % decode energy |
| I10 | Stojkovic 2403.20306v1 | 1.6 GHz vs 2 GHz (inference) | ~same throughput | <80 % of energy |
| I11 | Dodge 2206.05229v1, Table 4 | P&R vs none, 6B LM, +24 h | same job | emissions −2.5 % |
| I11 | Dodge 2206.05229v1, Table 5 | P&R vs none, 6B LM, +100 % | same job | emissions −11.4 % |
| I11 | Wiesner 2110.13234v1 | interrupting vs non-interrupting (simulated) | same jobs | −13.3 to −18.9 % vs −6.1 to −14.4 % |
| I11 | CarbonScaler 2302.08681v2 | carbon scaling vs suspend-resume | same job | −37 % |
| I11 | CarbonFlex 2505.18357v1 | carbon-aware vs agnostic | same jobs | ~−57 % |
| I11 | Wiesner 2602.22760v1 | curtailment-aware vs single-site | ppl 15.1 / 14.8 | 1.38 / 11.4–27.1 kgCO2 |
| I11 | McDonald 2205.09646v1 | night vs day (PUE) | same job | energy ~−10 % |
