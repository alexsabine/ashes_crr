# Attention algorithms, family F1: the ethics and objectives of recommender algorithms (sweep 2026-09-28)

- **Date:** 2026-09-28 (UTC); every fetch on this date.
- **Purpose:** `Attention_Algorithms/DECLARATION.md` (prompt-log 231), section 3, family F1. The declaration was pushed before any source was fetched.
- **Who:** agent-fetched (a literature sub-agent); readings are the agent's, per claim, in `Attention_Algorithms/checks/claims_f1.py`.
- **What it is:** a record of what the sources say. It does not judge novelty; "not found" is never read as novel (DECLARATION section 2). A note, not evidence (R8).

## Method

- **Window:** 2019-01-01 to 2026-09-28, plus canonical earlier work that in-window sources build on (Mittelstadt et al. 2016; Wu et al. 2017; Zhao et al. 2018).
- **arXiv:** `https://arxiv.org/search/?query=<q>&searchtype=all&order=-announced_date_first&size=50` via curl, one per declared query; every hit on the first page (newest 50) screened on title (and abstract where the title was ambiguous). Only Q1 exceeded 50 results (829): its first 50 (all dated March to September 2026) were screened and the remainder was not; the canonical Q1 works were reached through the WebSearch.
- **WebSearch:** one per declared query (11), every hit logged. Supplementary searches (S-a to S-i) were run for priority sources the declared queries did not hit and for the brief's item "objectives that do not reward the user's return, per-session value, or respecting the user's decision to stop"; they are logged separately.
- **Screening:** hits not fetched were excluded on title and snippet; the reason is given. Hits stating a position already carried by an included source (chiefly U1 retention RL papers from Kuaishou/Meta and U2 notification papers) were excluded as redundant at the 25-source cap; the cap bit on U1/U2 industry papers, not on U3/U5 candidates.
- **Fetching and text:** arXiv abstract page (for the current version and date, R10) plus the full-text PDF, extracted with pypdf 6.19; non-arXiv PDFs likewise; one HTML transcript converted to text. Raw texts are saved in the session scratchpad `attn/f1/<short>.txt` (not committed: third-party full texts), each with a header (source URL, HTTP status, version).
- **Blocked or failed fetches (R10):** SAGE (journals.sagepub.com) 403 to curl and WebFetch; Springer served a JavaScript bot challenge; PhilArchive served a Cloudflare challenge; web.archive.org is blocked by the session egress policy (403 "Blocked by egress policy"; not routed around). Both affected works (S01, S02) were fetched as versions of record from the Oxford repository ORA. Journal versions of S15, S19 and S20 were not fetched (arXiv versions used, noted per source). Russell's book (Human Compatible, 2019) was not fetched; his own words are taken from a published interview transcript (S14).
- **Quotes:** every quote in `claims_f1.py` is a verbatim substring of its saved raw text after html-unescape, removal of U+FFFE/U+00AD and of `-\n` joins, and whitespace collapse (PDF artefacts such as joined words, e.g. "termlow-regret", are kept as extracted). Check result: **78 of 78 quotes found in 41 claims** (run by the agent on 2026-09-28 with the same normalisation as `AI_Safety/CORRIGIBILITY_2026/checks/verify_claims.py`).

## Counts

- Hits screened: arXiv 134 (Q1 50, Q2 27, Q3 1, Q4 0, Q5 10, Q6 8, Q7 32, Q8 1, Q9 3, Q10 2, Q11 0); WebSearch 99 on the 11 declared queries; supplementary WebSearch 81 (54 screened as candidate sources, 27 used only to locate open copies of S01/S02). 314 hit entries in all, with duplicates across engines and queries.
- Sources included: **25** (cap 25). Claims: **41** (78 quotes).
- Claims by tag and reading: U1 states 5, close 1, bears 3; U2 states 4, close 1; U3 close 4, bears 2; U4 states 1, close 8, bears 2; U5 close 1; U6 mixed 1; U7 close 1; U8 addresses 2, bears 5.

## Readings nearest U3 and U5 (the agent's, for the grader; not a grade)

- **S22 Anwar, Dhillon, Schoenebeck 2025 (f1:36 U5 close, f1:37 U3 close).** Objective: the user's reflective value (enrichment from deliberate ratings) summed over choice rounds, no retention or return term; leaving the platform can be optimal. Difference from U5: the objective counts the off-platform option's enrichment (not indifferent to the stop: it can favour it), rounds are platform choice occasions over a fixed horizon rather than the user's own active steps, and no zero-stake/pause statement or notification analysis.
- **S25 RecoMind 2025 (f1:41 U3 close).** Session-episode valuation that terminates when the user exits: no term on the return. Difference: the reward is in-session engagement (session depth), so the in-session stop still removes represented value; not reflective value.
- **S11 Carroll et al. 2022 and S12 Krueger et al. 2020 (f1:15, f1:17 U3 close).** Myopic (gamma = 0) learners as a way to remove incentives to shape the user's future state (including driving users away). Difference: myopia removes the whole future including in-session value, is not indexed on the user's active steps, and the pause is not the object; Carroll et al. report myopic systems still induce shifts.
- The counter-position is stated by **S21 System-2 Recommenders (f1:34 U1 states)**: the user's return is taken as the evidence of reflective utility.
- No source in the F1 sweep states a valuation with no term on the user's return together with an explicit zero-stake treatment of the user's pause (the U3/U5 statement). This is "not found in the F1 sweep", not "novel".

## Search log

### arXiv (one search per declared query)

#### Q1. "ethics of algorithms"
- **arXiv search** (all fields, newest first, size 50): 829 results; 50 screened (first 50 of the newest; the rest not screened, see note).
  - 2609.30747 "Beyond the Last Truffula Tree: SustainAI - A Water-Aware, Closed-Loop Framework for Environmentally Accountable AI" (September 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2609.26507 "The Ethics of Artificial Intelligence in Military Operations" (September 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2609.24718 "A Federated Artificial Intelligence Framework for Optimizing Pancreatic Cancer Treatment - Strategy Update" (September 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2609.21643 "From Smarter to Hungrier: the Role of Energy Efficiency in Software-defined Vehicles" (September 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2609.16232 "Toward Governance-Aware Autonomous GIS: A Narrative Review of Ethical and Privacy Risks in LLM-Enabled GeoAI" (September 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2609.13187 "Algorithmic authority and the complexities of delegated decision-making: Case studies on ethical challenges for 21st-century leadership" (September 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2609.08982 "Embedded Human-Centered Data Science in a Graduate Programming Course: A Framework and Case Study" (September 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2608.13444 "Algorithmic Gender Prediction Is Illegitimate, But Gender Imputation Can Yield Valid Measurements" (August 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2608.10400 "Do Judges Behave Like Algorithms?" (August 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2608.09917 "WhichTok? Comparing Three TikTok Data Acquisition Tools" (August 2026) — excluded: TikTok data-acquisition tools; method comparison, no objective
  - 2608.07642 "Contextual Value Alignment via Multilayer Combinatorial Fusion" (August 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2608.02699 "Explainable AI for the EU Right to Explanation: A Systematic Review of the Law-XAI Translation Gap" (August 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2607.21547 "The Boundaries of Automation: A Theory of Persistent Human Participation" (July 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2607.19733 "AI-Increased Talent Retention Strategies: Fostering Long-Term Employee Engagement and Development in Talent Management" (July 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2607.14782 "Global Index on Responsible AI: 2026 Report" (July 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2607.13839 "AI-Augmented Human Resource Management? Insights from German companies" (July 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2607.02245 "Copewell: A Multi-Agent Swarm Architecture for Equitable Mental Wellness Support" (July 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2607.00854 "A field experiment of social influence and behavioral contagion with bots on Reddit" (July 2026) — excluded: social-bot field experiment on Reddit; not recommender objectives
  - 2606.20704 "Artificial Intelligence as Monism: Ontological, Organisational, and Methodological Implications" (June 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2606.18289 "Beyond the Algorithm: Professional Experiences and Perceptions of AI Bias" (June 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2606.17777 "On Response-Adaptive Targeting Strategies for Multi-Treatment Experiments" (June 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2606.12437 "Algorithmic Constitutionalism" (June 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2606.11214 "From Awareness to Action: Understanding and Overcoming the Research-Practice Gap in Algorithmic Fairness for Public Health" (June 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2606.09901 "On the Controllability-Fidelity Frontier in Diffusion Editing" (June 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2605.31143 "Extending the UXR Point of View Pyramid: A Generative AI-Augmented Methodology for Human-Centred AI Systems" (May 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2605.30099 "Evaluation of Conversational Agents: Understanding Culture, Context and Environment in Emotion Detection" (May 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2605.25258 "First, do no harm: Breaking suicidogenic echo chambers in media recommendation" (May 2026) — excluded: recommender harm (suicidogenic echo chambers); content safety, not the objective's stake in return
  - 2605.16296 "Artificial Intelligence in Lifelong Learning: Opportunities and Challenges in Adult Education Policy" (May 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2605.16041 "Explainable AI Isn't Enough! Rethinking Algorithmic Contestability" (May 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2605.10604 "Fairness vs Performance: Characterizing the Pareto Frontier of Algorithmic Decision Systems" (May 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2605.09393 "Prediction Model of Motivators and Demotivators of Integrating Large Language Models in Software Engineering Education: An Empirical Study" (May 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2605.06439 "From Review to Design: Ethical Multimodal Driver Monitoring Systems for Risk Mitigation, Incident Response, and Accountability in Automated Vehicles" (May 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2605.02773 "A Critical Pragmatism Approach for Algorithmic Fairness: Lessons from Urban Planning Theory" (May 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2605.02169 "Heterogeneous Model Fusion for Privacy-Aware Multi-Camera Surveillance via Synthetic Domain Adaptation" (May 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2605.00315 "Unbox Responsible GeoAI: Navigating Climate Extreme and Disaster Mapping" (May 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2604.27825 "Requirements Debt in AI-Enabled Perception Systems Development: An Industrial RE4AI Perspective" (April 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2604.15990 "From Vulnerable Data Subjects to Vulnerabilizing Data Practices: Navigating the Protection Paradox in AI-Based Analyses of Platformized Lives" (April 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2604.06219 "From experimentation to engagement: on the paradox of participatory AI and power in contexts of forced displacement and humanitarian crises" (April 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2604.03251 "The Algorithmic Blind Spot: Bias, Moral Status, and the Future of Robot Rights" (April 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2604.03250 "Ethical Implications of Training Deceptive AI" (April 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2604.01853 "Beyond Detection: Ethical Foundations for Automated Dyslexic Error Attribution" (April 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2603.28755 "Graphilosophy: Graph-Based Digital Humanities Computing with The Four Books" (March 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2603.27895 "Fairness Across Fields: Comparing Software Engineering and Human Sciences Perspectives" (March 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2603.24853 "Resisting Humanization: Ethical Front-End Design Choices in AI for Sensitive Contexts" (March 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2603.18633 "An Onto-Relational-Sophic Framework for Governing Synthetic Minds" (March 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2603.12511 "How Fair is Software Fairness Testing?" (March 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2603.12406 "Team Diversity Promotes Software Fairness: An Experiment on Fairness-Aware Requirements Prioritization" (March 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2603.05226 "Learning Optimal Individualized Decision Rules with Conditional Demographic Parity" (March 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2603.04595 "A Late-Fusion Multimodal AI Framework for Privacy-Preserving Deduplication in National Healthcare Data Environments" (March 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives
  - 2603.00161 "SKINOPATHY AI: Smartphone-Based Ophthalmic Screening and Longitudinal Tracking Using Lightweight Computer Vision" (March 2026) — excluded: general AI/algorithm ethics or unrelated domain; not recommender objectives

#### Q2. "recommender system long-term user engagement reinforcement learning"
- **arXiv search** (all fields, newest first, size 50): 27 results; 27 screened.
  - 2607.14192 "Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning" (July 2026) — excluded: long-term engagement via downstream reward learning (2026); same U1 position as included S03/S05, cap
  - 2603.19585 "SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search" (March 2026) — excluded: short-video search satisfaction fusion; in-query satisfaction, not return or pause
  - 2603.03820 "Fairness Begins with State: Purifying Latent Preferences for Hierarchical Reinforcement Learning in Interactive Recommendation" (March 2026) — excluded: fairness state purification in interactive RL recommenders; fairness, not engagement stake
  - 2603.03094 "Proactive Guiding Strategy for Item-side Fairness in Interactive Recommendation" (March 2026) — excluded: item-side fairness in interactive recommendation; out of scope
  - 2511.10573 "Towards Emotionally Intelligent and Responsible Reinforcement Learning" (November 2025) — excluded: emotionally intelligent RL (position); no recommender objective analysed
  - 2510.09167 "Hierarchical Semantic RL: Tackling the Problem of Dynamic Action Space for RL-based Recommendations" (October 2025) — excluded: RL action-space method; no objective discussion
  - 2507.16253 "Reinforce Lifelong Interaction Value of User-Author Pairs for Large-Scale Recommendation Systems" (July 2025) — excluded: lifelong user-author interaction value (Kuaishou); U1 again, redundant with S05, cap
  - 2504.05628 "Stratified Expert Cloning for Retention-Aware Recommendation at Scale" (April 2025) — excluded: retention-aware recommendation at scale (Kuaishou); U1 again, redundant with S05, cap
  - 2502.10158 "Combinatorial Reinforcement Learning with Preference Feedback" (February 2025) — excluded: combinatorial RL with preference feedback; theory, no engagement objective
  - 2412.10381 "Supervised Learning-enhanced Multi-Group Actor Critic for Live Stream Allocation in Feed" (December 2024) — excluded: live-stream allocation actor-critic; method
  - 2409.14872 "FedSlate:A Federated Deep Reinforcement Learning Recommender System" (September 2024) — excluded: federated deep RL recommender; method
  - 2408.08047 "An Efficient Continuous Control Perspective for Reinforcement-Learning-based Sequential Recommendation" (August 2024) — excluded: continuous-control RL for sequential recommendation; method
  - 2404.03637 "Sequential Recommendation for Optimizing Both Immediate Feedback and Long-term Retention" (April 2024) — excluded: immediate feedback + long-term retention (Kuaishou); U1 again, redundant with S05, cap
  - 2402.15164 "EasyRL4Rec: An Easy-to-use Library for Reinforcement Learning Based Recommender Systems" (February 2024) — excluded: RL recommender library; tooling
  - 2310.16566 "Model-enhanced Contrastive Reinforcement Learning for Sequential Recommendation" (October 2023) — excluded: model-enhanced contrastive RL; method
  - 2309.08622 "Representation Learning in Low-rank Slate-based Recommender Systems" (September 2023) — excluded: low-rank slate representation learning; theory/method
  - 2305.13747 "Optimizing Long-term Value for Auction-Based Recommender Systems via On-Policy Reinforcement Learning" (May 2023) — excluded: long-term value for auction recommenders (Meta); U1-type LTV, redundant, cap
  - 2305.04832 "Sim2Rec: A Simulator-based Decision-making Approach to Optimize Real-World Long-term User Engagement in Sequential Recommender Systems" (May 2023) — excluded: Sim2Rec simulator for long-term engagement; method, U1 redundant
  - 2301.08632 "Generative Slate Recommendation with Reinforcement Learning" (January 2023) — excluded: generative slate RL; method
  - 2212.02779 "PrefRec: Recommender Systems with Human Preferences for Reinforcing Long-term User Engagement" (December 2022) — excluded: PrefRec: human preferences to reinforce long-term engagement; preferences over trajectories used to raise engagement (U1), redundant, cap
  - 2202.08812 "Should I send this notification? Optimizing push notifications decision making by modeling the future" (February 2022) — **INCLUDED** as S09
  - 2202.03867 "Offline Reinforcement Learning for Mobile Notifications" (February 2022) — **INCLUDED** as S07
  - 2109.04083 "User Tampering in Reinforcement Learning Recommender Systems" (September 2021) — **INCLUDED** as S13
  - 2101.06286 "Reinforcement learning based recommender systems: A survey" (January 2021) — excluded: survey of RL recommenders; secondary
  - 2101.03584 "Towards Long-term Fairness in Recommendation" (January 2021) — excluded: long-term fairness in recommendation; fairness
  - 1905.12767 "Reinforcement Learning for Slate-based Recommender Systems: A Tractable Decomposition and Practical Methodology" (May 2019) — excluded: SlateQ (Google) slate decomposition; method; engagement reward noted but S04 covers YouTube
  - 1902.05570 "Reinforcement Learning to Optimize Long-term User Engagement in Recommender Systems" (February 2019) — **INCLUDED** as S03

#### Q3. "user retention return time recommender"
- **arXiv search** (all fields, newest first, size 50): 1 results; 1 screened.
  - 2511.18013 "Save, Revisit, Retain: A Scalable Framework for Enhancing User Retention in Large-Scale Recommender Systems" (November 2025) — excluded: Save, Revisit, Retain (Pinterest, 2025): retention framework; fetched (raw attn/f1/jiang2025.txt) and excluded at the 25 cap, U1 redundant with S05/S20

#### Q4. "notification volume optimization engagement"
- **arXiv search** (all fields, newest first, size 50): 0 results; 0 screened.

#### Q5. "induced preference shift recommender"
- **arXiv search** (all fields, newest first, size 50): 10 results; 10 screened.
  - 2609.00165 "Two-Sided State-Space Models for Sequential Recommendation with Non-Random Multimodal Review Feedback" (September 2026) — excluded: state-space sequential recommendation; method
  - 2608.03892 "Intertemporal Preference Steering in Qwen3 via Contrastive Activation Addition" (August 2026) — excluded: intertemporal preference steering in an LLM; not recommenders
  - 2608.03647 "Conditionally Identifiable Latent-Environment Modeling for Out-of-Distribution Recommendation" (August 2026) — excluded: OOD recommendation latent environments; method
  - 2607.25227 "Decision-Level Hijacking: Injecting Cognitive Bias into Large Language Models via Bit-Flip Attacks" (July 2026) — excluded: bit-flip attacks on LLM decisions; security
  - 2607.10915 "Normative Alignment of Recommender Systems via Internal Label Shift" (July 2026) — excluded: normative alignment via internal label shift (2026); editorial/normative diversity, not return or pause; judgement call, cap
  - 2606.14046 "When Recommendation Denoising Meets Popularity Bias: Understanding and Mitigating Their Interaction" (June 2026) — excluded: denoising and popularity bias; method
  - 2510.10978 "Does LLM Focus on the Right Words? Mitigating Context Bias in LLM-based Recommenders" (October 2025) — excluded: context bias in LLM recommenders; method
  - 2509.09689 "Personas within Parameters: Fine-Tuning Small Language Models with Low-Rank Adapters to Mimic User Behaviors" (September 2025) — excluded: persona LoRA user simulation; method
  - 2204.11966 "Estimating and Penalizing Induced Preference Shifts in Recommender Systems" (April 2022) — **INCLUDED** as S11
  - 2009.09153 "Hidden Incentives for Auto-Induced Distributional Shift" (September 2020) — **INCLUDED** as S12

#### Q6. "inconsistent preferences engagement optimization"
- **arXiv search** (all fields, newest first, size 50): 8 results; 8 screened.
  - 2606.10126 "Pareto-Guided Teacher Alignment for Fair Personalized Text Generation" (June 2026) — excluded: fair personalised text generation; not recommenders
  - 2601.02372 "Improving News Recommendations through Hybrid Sentiment Modelling and Reinforcement Learning" (January 2026) — excluded: news recommendation sentiment + RL; method
  - 2510.16368 "The Burden of Interactive Alignment with Inconsistent Preferences" (October 2025) — excluded: burden of interactive alignment with inconsistent preferences (Shirali 2025); theory of user effort to steer engagement-based learners, bears on U4; excluded at cap (KMR S15 covers)
  - 2509.21044 "Reinforcement Learning Fine-Tuning Enhances Activation Intensity and Diversity in the Internal Circuitry of LLMs" (September 2025) — excluded: RL fine-tuning LLM circuitry; not recommenders
  - 2508.10116 "Bridging Modality Gaps in e-Commerce Products via Vision-Language Alignment" (August 2025) — excluded: e-commerce vision-language alignment; not relevant
  - 2506.17682 "Reinforcing User Interest Evolution in Multi-Scenario Learning for recommender systems" (June 2025) — excluded: multi-scenario interest evolution; method
  - 2210.12384 "The Devil is in the Conflict: Disentangled Information Graph Neural Networks for Fraud Detection" (October 2022) — excluded: fraud detection GNN; not relevant
  - 2202.11776 "The Challenge of Understanding What Users Want: Inconsistent Preferences and Engagement Optimization" (February 2022) — **INCLUDED** as S15

#### Q7. "aligning recommender systems human values"
- **arXiv search** (all fields, newest first, size 50): 32 results; 32 screened.
  - 2609.17839 "Evaluating the Impact of Personalization in Conversational Cybersecurity Assistants" (September 2026) — excluded: not about recommender objectives or user value
  - 2608.18638 "Report on The 1st Workshop on Human-Centered Proactive and Personalized Agents for Interactive Information Access at CHIIR 2026" (August 2026) — excluded: not about recommender objectives or user value
  - 2607.02539 "Beyond Satisfaction: Learning Associations Between Content, Reviews, and Well-Being" (July 2026) — excluded: Beyond Satisfaction: content, reviews and well-being (2026); bears on U4/U6 but no objective about return/pause; cap
  - 2606.02741 "Greener Than Humans? Environmental Attitudes in Large Language Models" (June 2026) — excluded: not about recommender objectives or user value
  - 2605.25273 "LLM-as-a-Judge in Healthcare: A Scoping Analysis of Applications, Methods, and Human Alignment" (May 2026) — excluded: not about recommender objectives or user value
  - 2605.01507 "MILD: Mediator Agent System with Bidirectional Perception and Multi-Layered Alignment for Human-Vehicle Collaboration" (May 2026) — excluded: not about recommender objectives or user value
  - 2602.19368 "The Human Factor in Data Cleaning: Exploring Preferences and Biases" (February 2026) — excluded: not about recommender objectives or user value
  - 2602.13305 "WildfireVLM: AI-powered Analysis for Early Wildfire Detection and Risk Assessment Using Satellite Imagery" (February 2026) — excluded: not about recommender objectives or user value
  - 2601.09871 "Epistemology gives a Future to Complementarity in Human-AI Interactions" (January 2026) — excluded: not about recommender objectives or user value
  - 2511.23312 "From IR to RecSys: Evaluating LLM-based Judges in Cranfield-style Recommendation Collections" (November 2025) — excluded: not about recommender objectives or user value
  - 2511.19979 "The 2nd Workshop on Human-Centered Recommender Systems" (November 2025) — excluded: workshop proposal on human-centred recommenders; no primary content
  - 2510.16662 "Safire: Similarity Framework for Visualization Retrieval" (October 2025) — excluded: not about recommender objectives or user value
  - 2510.16380 "MoReBench: Evaluating Procedural and Pluralistic Moral Reasoning in Language Models, More than Outcomes" (October 2025) — excluded: not about recommender objectives or user value
  - 2510.14702 "Cognitive-Aligned Spatio-Temporal Large Language Models For Next Point-of-Interest Prediction" (October 2025) — excluded: not about recommender objectives or user value
  - 2508.07673 "Ethics2vec: aligning automatic agents and human preferences" (August 2025) — excluded: not about recommender objectives or user value
  - 2507.08108 "Mallows Model with Learned Distance Metrics: Sampling and Maximum Likelihood Estimation" (July 2025) — excluded: not about recommender objectives or user value
  - 2505.21596 "Learning optimal treatment strategies for intraoperative hypotension using deep reinforcement learning" (May 2025) — excluded: not about recommender objectives or user value
  - 2504.09137 "Can Large Language Models Become Policy Refinement Partners? Evidence from China's Social Security Studies" (April 2025) — excluded: not about recommender objectives or user value
  - 2503.10215 "Adaptive Preference Aggregation" (March 2025) — excluded: not about recommender objectives or user value
  - 2502.00055 "Towards Recommender Systems LLMs Playground (RecSysLLMsP): Exploring Polarization and Engagement in Simulated Social Networks" (February 2025) — excluded: LLM playground on polarisation and engagement; simulation of polarisation, not objectives
  - 2501.13333 "AgentRec: Agent Recommendation Using Sentence Embeddings Aligned to Human Feedback" (January 2025) — excluded: not about recommender objectives or user value
  - 2410.12519 "RosePO: Aligning LLM-based Recommenders with Human Values" (October 2024) — excluded: RosePO: aligning LLM recommenders with values (helpfulness/harmlessness); not engagement objective
  - 2407.12847 "Aligning Model Evaluations with Human Preferences: Mitigating Token Count Bias in Language Model Assessments" (July 2024) — excluded: not about recommender objectives or user value
  - 2406.09264 "Position: Towards Bidirectional Human-AI Alignment" (June 2024) — excluded: not about recommender objectives or user value
  - 2312.15241 "Measuring Value Alignment" (December 2023) — excluded: not about recommender objectives or user value
  - 2308.06233 "Help or Hinder? Evaluating the Impact of Fairness Metrics and Algorithms in Visualizations for Consensus Ranking" (August 2023) — excluded: not about recommender objectives or user value
  - 2204.13480 "The Value of Measuring Trust in AI - A Socio-Technical System Perspective" (April 2022) — excluded: not about recommender objectives or user value
  - 2202.13985 "The dangers in algorithms learning humans' values and irrationalities" (February 2022) — excluded: dangers of learning human values and irrationalities (Gorman & Armstrong); general, bears on U4; cap
  - 2108.06370 "Visual Arrangements of Bar Charts Influence Comparisons in Viewer Takeaways" (August 2021) — excluded: not about recommender objectives or user value
  - 2107.10939 "What are you optimizing for? Aligning Recommender Systems with Human Values" (July 2021) — **INCLUDED** as S16
  - 2104.00983 "STARdom: an architecture for trusted and secure human-centered manufacturing systems" (April 2021) — excluded: not about recommender objectives or user value
  - 2008.13404 "Beyond Our Behavior: The GDPR and Humanistic Personalization" (August 2020) — excluded: GDPR and humanistic personalisation; legal/normative, F2 territory

#### Q8. "stated preferences versus engagement recommender"
- **arXiv search** (all fields, newest first, size 50): 1 results; 1 screened.
  - 1912.13023 "A Hierarchical Self-Attentive Model for Recommending User-Generated Item Lists" (December 2019) — excluded: hierarchical self-attentive list recommendation; keyword collision

#### Q9. "user tampering recommender reinforcement learning"
- **arXiv search** (all fields, newest first, size 50): 3 results; 3 screened.
  - 2407.03210 "Combining AI Control Systems and Human Decision Support via Robustness and Criticality" (July 2024) — excluded: AI control systems + decision support; not recommenders
  - 2203.10629 "Explicit User Manipulation in Reinforcement Learning Based Recommender Systems" (March 2022) — excluded: explicit user manipulation in RL recommenders (thesis); same result as S13, redundant
  - 2109.04083 "User Tampering in Reinforcement Learning Recommender Systems" (September 2021) — **INCLUDED** as S13

#### Q10. "time well spent recommender objective"
- **arXiv search** (all fields, newest first, size 50): 2 results; 2 screened.
  - 2410.23019 "High Precision Astrometry Science in the Context of Space Mission Prospectives" (October 2024) — excluded: astrometry; keyword collision
  - 2008.11925 "Algorithmic Approaches to Reconfigurable Assembly Systems" (August 2020) — excluded: reconfigurable assembly; keyword collision

#### Q11. "session-based recommender stopping"
- **arXiv search** (all fields, newest first, size 50): 0 results; 0 screened.


### WebSearch (one per declared query)

Each hit is listed as returned (title, host). Duplicates of a source already screened are marked "dup".

**Q1 "ethics of algorithms"** (9 hits)
- Medium/Aisentica, "The Ethics of Algorithms: Responsibility in the Age of the Digital Unconscious" — excluded: blog essay, no primary content.
- Springer, Tsamados et al., "The ethics of algorithms: key problems and solutions" — **INCLUDED** as S02.
- ACM DL, same Tsamados et al. record — dup of S02.
- arXiv 2406.13140, "From decision aiding to the massive use of algorithms: where does the responsibility stand?" — excluded: responsibility in decision aiding; not recommender objectives.
- ResearchGate, Mittelstadt et al. 2016, "The ethics of algorithms: Mapping the debate" — **INCLUDED** as S01 (canonical; text from ORA).
- arXiv 1711.06035, "From Algorithmic Black Boxes to Adaptive White Boxes" — excluded: ethical programs as codes of ethics; not recommenders.
- ResearchGate, Tsamados et al. — dup of S02.
- arXiv 1801.01705, "Gatekeeping Algorithms with Human Ethical Bias" — excluded: archives/libraries; not engagement objectives.
- arXiv 2310.18979, "Methodology of Algorithm Engineering" — excluded: keyword collision.

**Q2 "recommender system long-term user engagement reinforcement learning"** (9 hits)
- ACM DL, Zou et al. KDD 2019 — **INCLUDED** as S03.
- arXiv 1902.05570 — dup of S03.
- Semantic Scholar, Zou et al. — dup of S03.
- arXiv 1812.07127, "Deep reinforcement learning for search, recommendation, and online advertising: a survey" — excluded: survey, secondary.
- ResearchGate, Zou et al. — dup of S03.
- arXiv 2212.02779, PrefRec — excluded: preferences over trajectories used to raise long-term engagement (U1 again), redundant with S03/S05; 25-source cap.
- arXiv 2305.13747, long-term value for auction-based recommenders — excluded: U1-type LTV, redundant; cap.
- ResearchGate, "Long-term user engagement in recommender systems: a review" — excluded: review behind ResearchGate; secondary.
- ScienceDirect, "Deep reinforcement learning in recommender systems: A survey and new perspectives" — excluded: survey, secondary.

**Q3 "user retention return time recommender"** (9 hits)
- ACM DL, "Interpretable User Retention Modeling in Recommendation" (RecSys 2023) — excluded: retention modelling (U1 again), redundant with S05; cap.
- arXiv 2302.01724, Cai et al. (Kuaishou) — **INCLUDED** as S05.
- NSF PAR 10066038, Wu et al. "Returning is Believing" (CIKM 2017) — **INCLUDED** as S06 (canonical).
- arXiv 2310.03984, AURO adaptive user-retention optimisation — excluded: U1 again (Kuaishou retention RL), redundant; cap.
- arXiv 2303.06347, retention-oriented recommendation with Decision Transformer — excluded: U1 again, redundant; cap.
- ResearchGate, "Interpretable User Retention Modeling" — dup.
- ResearchGate, "Save, Revisit, Retain" — dup of arXiv 2511.18013 (fetched, excluded at cap; see arXiv log Q3).
- awesomepapers.io listing of 2511.18013 — dup.
- lacuna.tiptreesystems.com, "Sustaining User Attention in Recommender Systems" — excluded: aggregator page, no primary content.

**Q4 "notification volume optimization engagement"** (9 hits; arXiv returned 0)
- Medium, "Paper Explained — Notification Volume Control ... at Pinterest" — excluded: secondary summary of S10.
- Pinterest Engineering blog, "User state-based notification volume optimization" — excluded: engineering blog; S10 is the primary paper (judgement; U2 already stated).
- ACM DL, Zhao et al. KDD 2018 (Pinterest) — **INCLUDED** as S10 (canonical; author PDF fetched).
- ResearchGate, same — dup of S10.
- ResearchGate, "Optimizing Email Volume For Sitewide Engagement" (LinkedIn, CIKM 2017) — excluded: email volume, U2 redundant with S07/S08/S10; cap.
- kdd.org, KDD 2018 accepted-paper page — dup of S10.
- wjaets.com, "User state-based notification volume optimization: A novel approach" — excluded: low-provenance journal restating the Pinterest blog.
- wjaets.com PDF of the same — dup.
- cdn-static.findly.com PDF of Zhao et al. — dup of S10 (the copy fetched).

**Q5 "induced preference shift recommender"** (9 hits)
- ResearchGate, Carroll et al. — dup of S11.
- arXiv HTML 2204.11966 — **INCLUDED** as S11.
- PMLR PDF, Carroll et al. — dup of S11.
- ACM DL, "Estimating and Penalizing Preference Shift in Recommender Systems" (RecSys 2021 late-breaking version) — excluded: earlier short version of S11.
- liner.com quick review — excluded: secondary.
- ACM DL PDF of the RecSys 2021 version — dup.
- OpenReview, Carroll et al. — dup of S11.
- arXiv PDF 2204.11966 — dup of S11.
- arXiv 2403.07571, "Proactive Recommendation with Iterative Preference Guidance" — excluded: proposes steering preferences on purpose (opposite direction); method, no objective analysis of return or pause.

**Q6 "inconsistent preferences engagement optimization"** (9 hits)
- AEA 2023 programme page — excluded: listing of S15.
- arXiv PDF 2202.11776 — **INCLUDED** as S15.
- arXiv abs 2202.11776 — dup of S15.
- ADS abstract — dup.
- INFORMS Management Science page — dup (journal version; not fetched, arXiv v3 used).
- Harvard EconCS event page — excluded: talk listing.
- ResearchGate — dup.
- Simons Institute talk page — excluded: talk listing.
- sendhil.org page — dup (author listing).

**Q7 "aligning recommender systems human values"** (9 hits)
- arXiv PDF 2107.10939, Stray et al. 2021 — **INCLUDED** as S16.
- arXiv abs 2107.10939 — dup.
- arXiv PDF 2207.10192, Stray et al., "Building Human Values into Recommender Systems" — **INCLUDED** as S17.
- ACM DL TORS version of 2207.10192 — dup of S17.
- ResearchGate, Stray 2021 — dup.
- Google Research page for 2207.10192 — dup.
- Partnership on AI, "Beyond Engagement: Aligning Algorithmic Recommendations With Prosocial Goals" — excluded: industry-programme page; the same authors' papers (S17, S20) carry the content; cap.
- Facebook post (arXiv ML feed) — excluded: social-media repost.
- participatoryml.github.io PDF of Stray 2021 — dup of S16.

**Q8 "stated preferences versus engagement recommender"** (9 hits)
- arXiv 2412.10595, "Recommendation and Temptation" — **INCLUDED** as S22.
- ACM DL RecSys 2025 version — dup of S22.
- PMC, "Engagement, user satisfaction, and the amplification of divisive content on social media" (PNAS Nexus) — **INCLUDED** as S19 (arXiv 2305.16941 v6 fetched).
- arXiv 2209.11801, Ashton & Franklin — **INCLUDED** as S23.
- arXiv HTML 2406.01611v1, "System-2 Recommenders" — **INCLUDED** as S21.
- arXiv HTML 2604.11517v1, "Understanding the Gap Between Stated and Revealed Preferences in News Curation: A Study of Young Adult Social Media Users" — excluded: user study of the stated/revealed gap in news, bears on U4 only; cap (S19 carries the stated-preference test).
- Medium (Understanding Recommenders), Thorburn, "What Does it Mean to Give Someone What They Want?" — excluded: blog essay; the same group's papers (S17, S20) carry the content.
- arXiv 2212.02779, PrefRec — dup (excluded under Q2).
- arXiv 2506.04525, "Can Users Fix Algorithms? A Game-Theoretic Analysis of Collective Content Amplification" — excluded: collective user strategy, not the objective.

**Q9 "user tampering recommender reinforcement learning"** (9 hits)
- arXiv abs 2109.04083 — **INCLUDED** as S13.
- Edinburgh Research Explorer — dup of S13.
- ACM DL AIES 2023 — dup of S13.
- ResearchGate — dup.
- Edinburgh PDF — dup.
- arXiv 2203.10629, "Explicit User Manipulation in RL Based Recommender Systems" (Sparr) — excluded: replicates S13's result; redundant.
- awesomepapers.io listings (3) — dup.

**Q10 "time well spent recommender objective"** (9 hits)
- arXiv 2512.13726, "Time-constrained recommendations: reinforcement ..." — excluded on title/snippet (not fetched): a user time budget as a constraint on recommendation (method); judgement, cap. Not read, so not graded either way.
- Recombee blog, "Modern Recommender Systems - Part 3: Objectives" — excluded: vendor blog.
- Medium, "Time Well Spent and New Metrics in Tech" — excluded: essay.
- LinkedIn advice page on metrics — excluded: non-scholarly.
- ludwig.guru usage page — excluded: keyword collision.
- participatoryml.github.io PDF of Stray 2021 — dup of S16.
- stonemantel.co blog — excluded: keyword collision.
- arXiv 1708.08447, "It's Time to Consider 'Time' when Evaluating Recommender-System Algorithms" — excluded: temporal evaluation protocol, not objectives.
- pith.science citation listing of Stray 2021 — dup.

**Q11 "session-based recommender stopping"** (9 hits; arXiv returned 0)
- arXiv 2002.02890, session-based recommenders for GUI test generation — excluded: keyword collision.
- NVIDIA Merlin session-based recommenders — excluded: product page.
- arXiv 1902.04864, "A Survey on Session-based Recommender Systems" — excluded: survey of next-item prediction; no stopping/objective content.
- Jannach, session-based recommender handbook chapter — excluded: next-item prediction, no stopping.
- arXiv 2211.06394, STAR session-based time-aware recommender — excluded: method.
- fastforwardlabs session-based recommenders report — excluded: tutorial.
- GitHub rn5l/session-rec — excluded: code framework.
- Medium, micro-behaviours session-based recommendation — excluded: blog.
- MDPI, flexible session-based recommender for e-commerce — excluded: method.
The declared query found nothing on a recommender that respects the user's decision to stop; the supplementary search S-c below was run for that brief item.

### Supplementary searches (priority sources and the brief's last item; logged, not declared queries)

- **S-a "Top-K Off-Policy Correction for a REINFORCE Recommender System" YouTube** (9 hits): arXiv 1812.02353 — **INCLUDED** as S04 (+ 3 dups: arXiv PDF, Google Research, Semantic Scholar); arXiv 2211.06365 (inductive/incremental updates) excluded: method; arXiv 2308.07857 (impression-aware survey) excluded: survey; arXiv 2304.02572 (online bandit exploration) excluded: method; arXiv 2508.00201 RecoMind — **INCLUDED** as S25; arXiv 2603.08956 (survey of RL for economics) excluded: survey.
- **S-b LinkedIn notification volume optimization multi-objective (Gao/Yuan)** (9 hits): arXiv 2207.03029 — **INCLUDED** as S08; arXiv 2509.02458 (generative sequential notification optimisation via multi-objective decision transformers, LinkedIn) excluded: U2 redundant with S07/S08, cap (+ PDF dup); ResearchGate/ACM "Optimizing Email Volume For Sitewide Engagement" excluded (see Q4); LinkedIn engineering blog "Less Is More" parts 1-2 excluded: blog, U2 redundant; vinija.ai notes excluded: secondary; USPTO patent 10977096 excluded: patent, U2 redundant. No paper with Gao as first author on LinkedIn notification volume was found; the search result's "Gao Yan" appears only as an acknowledged reviewer.
- **S-c recommender objective respect user's decision to stop session end / well-being** (9 hits): ACM DL / arXiv 2412.09950 "Hesitation and Tolerance" — **INCLUDED** as S24 (+ 1 dup); Recombee blog excluded; ACM RecSys 2025 "How Do Users Perceive Recommender Systems' Objectives?" excluded: perception survey, bears on U4 only, cap; Carroll et al. dup of S11; System-2 dup of S21; arXiv 2001.00846 (multi-gradient descent multi-objective) excluded: method; MDPI recommendation messages excluded: UX of messages; PMC survey of multi-objective recommenders excluded: survey.
- **S-d Stuart Russell recommender algorithms manipulate preferences** (9 hits): 80,000 Hours transcript — **INCLUDED** as S14; Goodreads quotes excluded: secondary; EA Forum post and zachfreitasgroff blog "Is there evidence that recommender systems are changing users' preferences?" excluded: blog reviews; Medium essay excluded; arXiv 2001.07118 (incentives for responsiveness, instrumental control) excluded: general causal-incentive theory, not recommenders; Carroll et al. (3) dup of S11.
- **S-e Milli, Belli, Hardt "From optimizing engagement to measuring value"** (9 hits): arXiv 2008.12623 — **INCLUDED** as S18 (+ Semantic Scholar, ResearchGate x2, ADS, ACM, v1 dups); arXiv HTML 2405.03948v1 (untitled "1 Introduction" page) excluded: not identifiable from the hit, not fetched.
- **S-f "non-engagement signals" content ranking** (9 hits): arXiv 2402.06831 — **INCLUDED** as S20 (+ ADS, Wiley NYAS x2, jonathanstray.com PDF, awesomepapers dups); arXiv HTML 2305.16941v6 and PMC — dup of S19; arXiv 2405.03948v1 — as S-e.
- **S-g/S-h/S-i locating open copies of S01 and S02** (27 hits): repository and aggregator listings only (VUB, PhilArchive, SSRN, ORA, ResearchGate, Semantic Scholar, Academia.edu, Scribd, OUCI, Goodreads, eBay, arXiv 2110.10980 and 2403.06910); used only to find the ORA copies; none screened as sources.


## Sources (25 included)

### S01. Mittelstadt, Allo, Taddeo, Wachter, Floridi, "The ethics of algorithms: Mapping the debate"
- Venue: Big Data & Society 3(2) (canonical, pre-window; Tsamados et al. 2022 is its update)
- Version/date: published Dec 2016; version of record (CC BY-NC). URL: https://doi.org/10.1177/2053951716679679
- Fetch (2026-09-28): SAGE HTML and PDF returned 403 to curl and WebFetch; Wayback blocked by egress policy (403 "Blocked by egress policy"); version of record fetched from ORA (https://ora.ox.ac.uk/objects/uuid:684a91dd-faff-411a-8739-39d57734cab4, file HTTP 200, 21 pp., pypdf). Raw text: `attn/f1/mittelstadt2016.txt`
- Hit by: Q1 WebSearch (ResearchGate listing); copy located by a supplementary search
- Claim `f1:1` [U4, bears]: BEARS: canonical framing of personalisation as a threat to autonomy (the user pushed toward the institution's preferred action). No objective, no treatment of the session end or return.
  > "Value-laden decisions made by algorithms can also pose a threat to the autonomy of data subjects. The reviewed literature in particular connects personalisation algorithms to these threats."
  > "institutionally preferred action rather than their own preference"

### S02. Tsamados, Aggarwal, Cowls, Morley, Roberts, Taddeo, Floridi, "The ethics of algorithms: key problems and solutions"
- Venue: AI & Society 37:215-230 (2022)
- Version/date: received 27 Jul 2020, accepted 22 Jan 2021, published online 20 Feb 2021; version of record (CC BY). URL: https://doi.org/10.1007/s00146-021-01154-8
- Fetch (2026-09-28): Springer pages served a JavaScript bot challenge to curl (3 KB page) and a cookie redirect to WebFetch; PhilArchive behind a Cloudflare challenge; version of record fetched from ORA (https://ora.ox.ac.uk/objects/uuid:6e15650c-6bb2-40c1-8617-20b82aabd815, file HTTP 200, pypdf). Raw text: `attn/f1/tsamados2022.txt`
- Hit by: Q1 WebSearch (Springer, ACM DL)
- Claim `f1:2` [U4, bears]: BEARS: autonomy loss through recommenders shaping choices; the remedy discussed is user control over information and participation in design, not an objective that leaves the stop to the user.
  > "Considering that recommender systems contribute to the dynamic construction of individuals’ identities by intervening in their choices, a lack of control over one’s information translates in a loss of autonomy."
  > "The risks that algorithmic systems may hinder human autonomy by shaping users’ choices has been widely reported in the literature"

### S03. Zou, Xia, Ding, Song, Liu, Yin, "Reinforcement Learning to Optimize Long-term User Engagement in Recommender Systems"
- Venue: KDD 2019
- Version/date: arXiv:1902.05570 v4, Thu, 11 Jul 2019 08:28:08 UTC. URL: https://arxiv.org/abs/1902.05570
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/zou2019.txt`
- Hit by: Q2 arXiv and WebSearch
- Claim `f1:4` [U1, states]: STATES U1: long-term engagement ("stickiness") includes revisit / return time; staying and scrolling is rewarded, so leaving ends the reward stream.
  > "a good recommender system should pay more attention to user stickiness, which is far beyond classical instant metrics"
  > "delayed feedback~(e.g. dwell time, revisit)"
  > "the system should reward this feed if the user remained in the system and scrolled down"
- Claim `f1:5` [U2, close]: CLOSE form of U2: the feed without a natural stop is named as the setting the stickiness objective is optimised in. Difference: the paper does not say the objective produces the never-ending feed (the causal direction U2 asserts).
  > "The feed streaming setting provides users the interactive manner of recommendation in never-ending feeds."

### S04. Chen, Beutel, Covington, Jain, Belletti, Chi, "Top-K Off-Policy Correction for a REINFORCE Recommender System" (YouTube)
- Venue: WSDM 2019
- Version/date: arXiv:1812.02353 v3, Wed, 15 Dec 2021 02:23:41 UTC. URL: https://arxiv.org/abs/1812.02353
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/chen2019.txt`
- Hit by: supplementary WebSearch (priority source; not hit by a declared query)
- Claim `f1:7` [U1, close]: CLOSE: a long-horizon reward aggregated over a wall-clock window (4-10 hours) of user activity, deployed on YouTube. Difference: return time is not named as the reward; the stake in the stop is implicit (activity outside the session within the window counts).
  > "Here we explore framing recommendation as building RL agents to maximize each user’s long term satisfaction with the system."
  > "The long term reward𝑅 is aggregated over a time horizon of 4–10 hours."

### S05. Cai, Liu, Wang, Zuo, Xie, Yang, Zheng, Jiang, Gai, "Reinforcing User Retention in a Billion Scale Short Video Recommender System" (Kuaishou)
- Venue: The Web Conference 2023, Industry Track
- Version/date: arXiv:2302.01724 v3, Sun, 12 Feb 2023 07:02:19 UTC. URL: https://arxiv.org/abs/2302.01724
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/cai2023.txt`
- Hit by: Q3 WebSearch
- Claim `f1:3` [U1, states]: STATES U1 exactly: the reward is the wall-clock gap between sessions (the user's time away), to be minimised; deployed in the Kuaishou app. In CRR terms the pause has maximal content: every hour away is the loss the objective counts.
  > "our objective is to minimize the accumulated time interval of multiple sessions, which is equal to improving the app open frequency and user retention"
  > "The session ends when the user leaves the app, the next session starts when the user opens the app again and the process repeats. Our objective is to minimize the cumulative returning time (defined as the time gap between the last request of the session and the first request of the next session)"

### S06. Wu, Wang, Hong, Shi, "Returning is Believing: Optimizing Long-term User Engagement in Recommender Systems"
- Venue: CIKM 2017 (canonical, pre-window; the return-time objective S03/S05 build on)
- Version/date: CIKM Nov 2017; NSF PAR accepted manuscript as served 2026-09-28. URL: https://par.nsf.gov/servlets/purl/10066038
- Fetch (2026-09-28): NSF PAR PDF HTTP 200 (pypdf). Raw text: `attn/f1/wu2017.txt`
- Hit by: Q3 WebSearch
- Claim `f1:6` [U1, states]: STATES U1 (canonical, pre-window; Zou 2019 and Cai 2023 build on the return-time objective): clicks per calendar period, with return behaviour modelled so the policy can raise it.
  > "maximizing cumulative clicks from a population of users in a given period of time, while a linear regret is inevitable if a user’s temporal return behavior is not considered when making the recommendations"
  > "users’ re-visitations and return time intervals"

### S07. Yuan, Muralidharan, Nandy, Cheng, Prabhakar, "Offline Reinforcement Learning for Mobile Notifications" (LinkedIn)
- Venue: arXiv preprint (comments: "submitted")
- Version/date: arXiv:2202.03867 v1, Fri, 4 Feb 2022 22:22:22 UTC. URL: https://arxiv.org/abs/2202.03867
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/yuan2022.txt`
- Hit by: Q2 arXiv
- Claim `f1:10` [U2, states]: STATES U2: an RL notification policy optimised for engagement, measured in sessions (each return after 30 idle minutes counts).
  > "Mobile notification systems have taken a major role in driving and maintaining user engagement for online platforms."
  > "We propose an offline reinforcement learning framework to optimize sequential notification decisions for driving user engagement."
  > "A session is a collection of full-page views made by a single user on the same device type. Two sessions are separated by 30 minutes of zero activity."

### S08. Prabhakar, Yuan, Yang, Sun, Muralidharan, "Multi-objective Optimization of Notifications Using Offline Reinforcement Learning" (LinkedIn)
- Venue: KDD 2022
- Version/date: arXiv:2207.03029 v1, Thu, 7 Jul 2022 00:53:08 UTC. URL: https://arxiv.org/abs/2207.03029
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/prabhakar2022.txt`
- Hit by: supplementary WebSearch (LinkedIn notification volume; priority source)
- Claim `f1:11` [U2, states]: STATES U2: notifications as an engagement lever, with user visits as the site-engagement reward (multi-objective with disables as a cost).
  > "Notifications play an important role for mobile applications to keep users informed and engaged."
  > "Through this, notifications also help increase user engagements with the platform."
  > "site engagement responses (e.g., user visits, notification disables)"

### S09. O'Brien, Wu, Zhai, Guo, Shi, Hunt, "Should I send this notification? Optimizing push notifications decision making by modeling the future" (Twitter)
- Venue: arXiv preprint
- Version/date: arXiv:2202.08812 v1, Thu, 17 Feb 2022 18:27:17 UTC. URL: https://arxiv.org/abs/2202.08812
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/obrien2022.txt`
- Hit by: Q2 arXiv
- Claim `f1:12` [U2, states]: STATES U2 (and U1): push decisions optimised for long-term value with DAU a key metric; opening a notification makes the user active that day.
  > "Daily active users (DAU), the number of users who choose to login to Twitter daily, is one key metric (this is typically correlated with the number of notifications a user “opens” since when a user opens a notification they become an active user that day)."
  > "there is significant interest in recommender systems that optimize directly for long-term value (LTV)"
- Claim `f1:13` [U8, bears]: BEARS on U8: fewer notifications at equal engagement is reported as a win, i.e. volume can fall without an engagement cost; the objective (engagement) is unchanged.
  > "we are able to send less notifications and obtain a higher open rate than the baseline system, while generating the same level of user engagement on the platform as the existing, heuristic-based, system"

### S10. Zhao, Narita, Orten, Egan, "Notification Volume Control and Optimization System at Pinterest"
- Venue: KDD 2018 (canonical, pre-window; LinkedIn S07/S08 cite this line of work)
- Version/date: KDD Aug 2018; author PDF as served 2026-09-28. URL: https://doi.org/10.1145/3219819.3219906
- Fetch (2026-09-28): author PDF (cdn-static.findly.com) HTTP 200 (pypdf). Raw text: `attn/f1/pinterest2018.txt`
- Hit by: Q4 WebSearch
- Claim `f1:8` [U2, states]: STATES U2 (canonical, pre-window): notification volume is chosen per user to maximise site engagement (DAU/MAU), i.e. to bring the user back; the model splits organic from notification-triggered visits (the f_notif mechanism of the declaration).
  > "we propose a novel machine learning approach to decide notification volume for each user such that long term user engagement is optimized"
  > "In most companies, the more important metric we want to improve is the overall site engagement metric, such as daily active users (DAU), monthly active users (MAU), etc."
  > "We know that users could either come to the site organically, or they receive a notification and come to the site by clicking the notification."
- Claim `f1:9` [U8, bears]: BEARS on U8: the choice of target metric is justified by revenue; the incentive behind the return objective is stated, not treated as a problem.
  > "which is not desirable since active users contribute more on revenue"

### S11. Carroll, Dragan, Russell, Hadfield-Menell, "Estimating and Penalizing Induced Preference Shifts in Recommender Systems"
- Venue: ICML 2022, PMLR 162:2686-2708
- Version/date: arXiv:2204.11966 v2, Thu, 14 Jul 2022 20:41:04 UTC. URL: https://arxiv.org/abs/2204.11966
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/carroll2022.txt`
- Hit by: Q5 arXiv and WebSearch
- Claim `f1:14` [U1, bears]: BEARS: the long-horizon (LTV) valuation creates a stake in the user's future internal state. Same mechanism as CRR's content argument, applied to preferences, not to the pause.
  > "systems trained via long-horizon optimization will have direct incentives to manipulate users: in this work, we focus on the incentive to shift user preferences so they are easier to satisfy"
  > "these non-myopic policies are commonly referred to as longterm value, or LTV , systems. However, these policies will have incentives to manipulate users as a side-effect"
- Claim `f1:15` [U3, close]: CLOSE form of U3: a myopic valuation (gamma = 0) has no term on any future state, so none on the user's return. Difference: myopia removes the whole future, including in-session value; it is not indexed on the user's own active steps and the pause is not named; Carroll et al. report that myopic systems still induce shifts.
  > "While it has been proposed to prevent the RS from reasoning about manipulation pathways (e.g., by keeping it myopic)"
  > "For training our myopic policies, we use the same exact infrastructure as above, but setγ = 0"
- Claim `f1:16` [U4, close]: CLOSE form of U4: the user's own (natural) evolution is the reference the system must respect. Difference: engagement stays the objective, with a penalty on induced preference shift; no statement about the session end or return.
  > "we use the notion of "safe shifts", that define a trust region within which behavior is safe: for instance, the natural way in which users would shift without interference from the system could be deemed "safe""
  > "recommenders that optimize for staying in the trust region can avoid manipulative behaviors while still generating engagement"

### S12. Krueger, Maharaj, Leike, "Hidden Incentives for Auto-Induced Distributional Shift"
- Venue: arXiv preprint
- Version/date: arXiv:2009.09153 v1, Sat, 19 Sep 2020 03:31:27 UTC. URL: https://arxiv.org/abs/2009.09153
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/krueger2020.txt`
- Hit by: Q5 arXiv
- Claim `f1:17` [U3, close]: CLOSE form of U3: the design goal is a learner with no (revealed) incentive to change who arrives or stays (the user being driven away is one channel). Difference: the remedy is myopia plus a mitigation for meta-learning (context swapping), not a valuation indexed on the user's active steps; the user's pause is not the object.
  > "the (choice of) content displayed can change users' perceptions and preferences, or even drive them away, causing a shift in the distribution of users"
  > "Our goal is to ensure that machine learning systems do not leverage ADS to increase performance when doing so could be undesirable."
  > "(b) Myopic RL: Incentives for ADS are present and pursuing them is undesirable"

### S13. Evans, Kasirzadeh, "User Tampering in Reinforcement Learning Recommender Systems"
- Venue: AIES 2023
- Version/date: arXiv:2109.04083 v3, Mon, 24 Jul 2023 14:19:55 UTC. URL: https://arxiv.org/abs/2109.04083
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/evans2021.txt`
- Hit by: Q2 and Q9 arXiv; Q9 WebSearch
- Claim `f1:18` [U1, bears]: BEARS: the long-term engagement valuation produces an instrumental incentive on the user's state (opinions); the pause is not discussed.
  > "User tampering is a situation where an RL-based recommender system may manipulate a media user's opinions through its suggestions as part of a policy to maximize long-term user engagement."
- Claim `f1:19` [U3, bears]: BEARS: calls for a different objective design because existing mitigations fail; proposes none of the U3 kind.
  > "achieving such safety would require a fundamental shift in the design away from the approaches we have seen in the recent literature"

### S14. Russell (interviewed by Wiblin), "Stuart Russell on the flaws that make today's AI architecture unsafe, and a new approach that could fix them"
- Venue: 80,000 Hours podcast transcript; the book form (Human Compatible, 2019) was not fetched
- Version/date: published 22 Jun 2020; page modified 13 Oct 2025. URL: https://80000hours.org/podcast/episodes/stuart-russell-human-compatible-ai/
- Fetch (2026-09-28): HTML HTTP 200, converted to text. Raw text: `attn/f1/russell2020.txt`
- Hit by: supplementary WebSearch (Russell, preference manipulation)
- Claim `f1:20` [U1, bears]: BEARS: Russell's preference-manipulation argument in his own words (stated as hypothetical: he says he has not seen the platforms' code). The stake is in the user's future predictability, not in the pause.
  > "if you imagine a simple reinforcement learning algorithm whose goal is to optimize click-through or engagement or whatever metric the company platform would like to optimize, then what a reinforcement learning algorithm is going to do is to figure out how to manipulate you, your personality, your interests, your views in order to make you a more predictable consumer of content."

### S15. Kleinberg, Mullainathan, Raghavan, "The Challenge of Understanding What Users Want: Inconsistent Preferences and Engagement Optimization"
- Venue: Management Science (per WebSearch; journal version not fetched)
- Version/date: arXiv:2202.11776 v3, Mon, 23 Oct 2023 12:21:18 UTC. URL: https://arxiv.org/abs/2202.11776
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/kmr2022.txt`
- Hit by: Q6 arXiv and WebSearch
- Claim `f1:21` [U4, close]: CLOSE form of U4: the platform's target is the user's reflective (system-2) utility and engagement is shown to mislead it. Difference: a model of the gap, not a proposed objective; no treatment of the return or the pause.
  > "We consider a platform which simply wants to maximize user utility, but only observes user engagement."
  > "we often make choices in the moment that are inconsistent with what we actually want"
  > "These phenomena include users who have long sessions on a platform but derive very little utility from it, and platform changes that steadily raise user engagement before abruptly causing users to go “cold turkey” and quit."
- Claim `f1:22` [U3, bears]: BEARS: the user's reflective self ends the session on its own clock (per item) and utility is counted per session; this is a user model, not a platform valuation, and no zero-stake claim is made.
  > "there is a probability q after each item that system 2 wants to continue, and a complementary probability 1−q that system 2 views itself as “done” and derives no further utility"
- Claim `f1:23` [U8, bears]: BEARS on U8: names the incentive explanation and sets it aside (the problem persists even for a welfare-maximising platform); does not treat how incentives would be changed.
  > "One possible explanation is misaligned incentives: platforms are not optimizing for user happiness. We suggest the problem runs deeper, transcending the specific incentives of any particular platform"

### S16. Stray, Vendrov, Nixon, Adler, Hadfield-Menell, "What are you optimizing for? Aligning Recommender Systems with Human Values"
- Venue: ICML 2020 Participatory Approaches to ML workshop
- Version/date: arXiv:2107.10939 v1, Thu, 22 Jul 2021 21:52:43 UTC. URL: https://arxiv.org/abs/2107.10939
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/stray2021.txt`
- Hit by: Q7 arXiv and WebSearch; Q10 WebSearch
- Claim `f1:24` [U4, states]: STATES the U4 objective: optimise the user's informed, retrospective value rather than immediate behaviour ("time well spent"). Nothing on the pause or return.
  > "informed, deliberative, and perhaps retrospective evaluations are of a higher quality than immediate judgements"
  > "Many people report that they watch more TV than they retrospectively endorse"
  > "We describe cases where real recommender systems were modified in the service of various human values such as diversity, fairness, well-being, time well spent, and factual accuracy."

### S17. Stray, Halevy, Assar, Hadfield-Menell, Boutilier, Ashar, Beattie, Ekstrand, Leibowicz, et al., "Building Human Values into Recommender Systems: An Interdisciplinary Synthesis and Open Problems"
- Venue: ACM Trans. Recomm. Syst. 2(3) Article 20 (Sep 2024)
- Version/date: arXiv:2207.10192 v1, Wed, 20 Jul 2022 20:59:06 UTC. URL: https://arxiv.org/abs/2207.10192
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/stray2022.txt`
- Hit by: Q7 WebSearch
- Claim `f1:25` [U4, close]: CLOSE form of U4 (and a U1 description: product teams optimise retention). Difference: a research agenda naming values-relevant outcomes, not a valuation construction.
  > "Similarly, if social media recommenders should not optimize for engagement, then what should they optimize for?"
  > "While today these teams are typically optimizing for purchases, subscriptions or user retention, recommender systems could also be managed on values-relevant outcomes."
- Claim `f1:26` [U8, addresses]: ADDRESSES U8: the commercial pull toward retention and the role of external regulation are both treated.
  > "For example, subscription services must maximize user retention, while current recommender designs struggle with long-term outcomes."
  > "The challenge for policy-makers or regulators is to be both precise and general about how harms are to be assessed and values are to be enacted in recommender systems."
- Claim `f1:27` [U6, mixed]: MIXED (as summarised by a 2022 review, not primary evidence; F3 carries the primary studies).
  > "In the context of social media recommendation there has been mixed evidence regarding both positive and negative effects on adolescent well-being"
  > "it is currently not clear if social media contributes to depression or if depressed people spend more time on social media, or both"

### S18. Milli, Belli, Hardt, "From Optimizing Engagement to Measuring Value"
- Venue: FAccT 2021
- Version/date: arXiv:2008.12623 v2, Mon, 19 Jul 2021 16:32:49 UTC. URL: https://arxiv.org/abs/2008.12623
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/milli2021.txt`
- Hit by: supplementary WebSearch (priority: Milli et al.)
- Claim `f1:28` [U4, close]: CLOSE form of U4: optimise a measured notion of value instead of engagement (deployed at Twitter). Difference: value is a latent construct inferred from behavioural signals, not the user's stated/reflective judgement; nothing on the pause.
  > "there is potentially a large gap between engagement signals and a desired notion of "value" that is worth optimizing for"
  > "provide a general latent variable model approach that can be used to operationalize the target construct and directly optimize for it"

### S19. Milli, Carroll, Wang, Pandey, Zhao, Dragan, "Engagement, User Satisfaction, and the Amplification of Divisive Content on Social Media"
- Venue: PNAS Nexus 2025 (per the PMC listing in Q8; journal version not fetched)
- Version/date: arXiv:2305.16941 v6, Sat, 7 Dec 2024 14:53:35 UTC. URL: https://arxiv.org/abs/2305.16941
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/milli2023.txt`
- Hit by: Q8 WebSearch (PMC listing)
- Claim `f1:29` [U4, close]: CLOSE form of U4: ranking by stated preferences, tested against the engagement ranker in a pre-registered audit. Difference: per-item ranking, no treatment of the return or pause; the authors call for a balance of engagement and stated preferences.
  > "suggesting that the engagement-based algorithm underperforms in satisfying users' stated preferences"
  > "we explore the implications of an alternative approach that ranks content based on users' stated preferences"
- Claim `f1:30` [U8, bears]: BEARS on U8: the engagement ranker buys time on platform, which is what a switch away from it would cost.
  > "randomized experiments at Twitter have shown that it increases the amount of time users spend on the platform compared to the reverse-chronological timeline"

### S20. Cunningham, Pandey, Sigerson, Stray, Allen, Barrilleaux, Iyer, Milli, Kothari, Rezaei, "What We Know About Using Non-Engagement Signals in Content Ranking"
- Venue: arXiv; peer-reviewed form in Annals of the New York Academy of Sciences 2025 (per WebSearch; not fetched)
- Version/date: arXiv:2402.06831 v1, Fri, 9 Feb 2024 23:42:13 UTC. URL: https://arxiv.org/abs/2402.06831
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/cunningham2024.txt`
- Hit by: supplementary WebSearch
- Claim `f1:31` [U1, states]: STATES U1 as industry practice (workshop with platform staff): ranking weights are tuned to maximise long-term retention.
  > "Platforms often wish to estimate the set of weights that would maximize long-term retention"
  > "There is strong evidence that ranking by predicted engagement is effective in increasing user retention."
- Claim `f1:32` [U8, addresses]: ADDRESSES U8: the engagement/retention cost of dropping engagement ranking is quantified, and the incentive-compatible route (non-engagement signals that also raise retention) is argued. Note the route keeps retention as the judge.
  > "Multiple platforms reported maintaining long-term experiments which assigned users to a chronologically-ranked feed. Those users had substantially lower time-spent and retention, with the effects remaining over months or years."
  > "However retention can be further increased by incorporating other signals, including item "quality" proxies and asking users what they want to see with "item-level" surveys."
- Claim `f1:33` [U7, close]: CLOSE form of U7: opt-in user controls are rarely used and ranking changes rarely show measurable well-being effects. Difference: about ranking controls, not break reminders / time limits; F2 carries the company countermeasures.
  > "User controls over ranking often have low usage rates, but when used they do correlate well with quality and item-level surveys."
  > "Ranking changes can alter the prevalence of self-reported experiences of various kinds (e.g. harassment) but seldom have large enough effects on attitude measures like user satisfaction, well-being, polarization etc. to be measured in typical experiments."

### S21. Agarwal, Usunier, Lazaric, Nickel, "System-2 Recommenders: Disentangling Utility and Engagement in Recommendation Systems via Temporal Point-Processes"
- Venue: FAccT 2024
- Version/date: arXiv:2406.01611 v1, Wed, 29 May 2024 18:19:37 UTC. URL: https://arxiv.org/abs/2406.01611
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/system2.txt`
- Hit by: Q8 WebSearch
- Claim `f1:34` [U1, states]: STATES U1 in its welfare-motivated form, and is the direct counter-position to U3/U5: the user's return (arrival rate) is taken as the evidence of reflective utility, so the return is valued.
  > "In this paper we explore a new approach to recommender systems where we infer user utility based on their return probability to the platform rather than engagement signals."
  > "Our intuition is that users tend to return to a platform in the long run if it creates utility for them"
- Claim `f1:35` [U4, close]: CLOSE form of U4: optimise reflective (System-2) utility, separated from impulse. Difference: utility is read off returns (a wall-clock quantity), the opposite of the empty pause.
  > "The System-2 arrival intensity depends on the utility and has a long lasting effect, while the System-1 intensity depends on the instantaneous gratification and tends to vanish rapidly."

### S22. Anwar, Dhillon, Schoenebeck, "Recommendation and Temptation"
- Venue: RecSys 2025
- Version/date: arXiv:2412.10595 v2, Wed, 23 Jul 2025 07:15:21 UTC. URL: https://arxiv.org/abs/2412.10595
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/temptation.txt`
- Hit by: Q8 WebSearch
- Claim `f1:36` [U5, close]: CLOSEST to U5 in F1: the objective is the user's reflective value (enrichment, estimated from deliberate ratings) summed over choice rounds, with no retention or return term, and leaving the platform can be optimal. Differences: (i) the objective counts the enrichment of the off-platform option, so it is not indifferent to the stop (it can favour it); (ii) rounds are platform choice occasions over a fixed horizon T, not the user's own active steps; (iii) no zero-stake / pause statement and no notifications.
  > "We aim to design a recommendation system that ensures as much enrichment from consumption as possible."
  > "In the second case, where any platform content is likely less enriching than studying, maximizing enrichment requires helping the user avoid the platform altogether by recommending minimally tempting content or no recommendations at all."
  > "rating an item typically involves more deliberate reflection from a user compared to the often more impulsive act of choosing what to consume"
- Claim `f1:37` [U3, close]: CLOSE form of U3: the optimal policy is locally greedy (per-round value, no future term, hence no term on return). Difference: per-round enrichment, not engagement or pause content; the greedy optimality is a theorem of their model, not a design choice to remove a stake.
  > "It chooses what to recommend by maximizing the expected enrichment in a single round from an item."
- Claim `f1:38` [U8, bears]: BEARS on U8: an industry example of the value-vs-retention trade-off; no incentive analysis.
  > "He acknowledges navigating a tradeoff between the educational value of Duolingo and its ability to retain users."

### S23. Ashton, Franklin, "Solutions to preference manipulation in recommender systems require knowledge of meta-preferences"
- Venue: RecSys 2022 FAccTRec workshop
- Version/date: arXiv:2209.11801 v1, Wed, 14 Sep 2022 15:01:13 UTC. URL: https://arxiv.org/abs/2209.11801
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/ashton2022.txt`
- Hit by: Q8 WebSearch
- Claim `f1:39` [U4, close]: CLOSE form of U4 (meta-preferences as the user's reflective standard). The second quote reports Everitt et al. 2021: a counterfactual valuation removes the incentive, the same logical shape as Proposition 7 applied to preferences, not to the pause.
  > "solutions to preference manipulation in recommender systems must take into account certain meta-preferences (preferences over another preference) in order to respect the autonomy of the user and not be manipulative"
  > "a recommender serving content to a user using a preference set based on the counterfactual world where the user had not interacted with the system removes the preference manipulative incentive"

### S24. Zou, Sun, Ji, Zhang, Wang, Zhang, Jiang, "Hesitation and Tolerance in Recommender Systems"
- Venue: CHI 2026
- Version/date: arXiv:2412.09950 v2, Sun, 15 Feb 2026 13:16:13 UTC. URL: https://arxiv.org/abs/2412.09950
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/hesitation.txt`
- Hit by: supplementary WebSearch (objectives respecting the stop)
- Claim `f1:40` [U4, close]: CLOSE form of U4 (respect for the user's time; low-regret value). Difference: success is still validated on next-day retention, so the return keeps its place in the objective.
  > "Instead, recommender systems should be optimized for what we termlow-regret satisfaction: interactions that respect users’ time, reduce unnecessary effort, and deliver value that feels meaningful."
  > "even lightweight strategies treating tolerance as distinct from interest can improve retention while reducing wasted effort"

### S25. Ben Ayed, Feng, Adams, Singh, Anand, Xu, "RecoMind: A Reinforcement Learning Framework for Optimizing In-Session User Satisfaction in Recommendation Systems" (Pinterest)
- Venue: arXiv preprint
- Version/date: arXiv:2508.00201 v1, Thu, 31 Jul 2025 23:01:14 UTC. URL: https://arxiv.org/abs/2508.00201
- Fetch (2026-09-28): arXiv abstract page HTTP 200; full-text PDF HTTP 200 (pypdf 6.19). Raw text: `attn/f1/recomind.txt`
- Hit by: supplementary WebSearch (Chen 2019 query)
- Claim `f1:41` [U3, close]: CLOSE form of U3: a session-episode valuation has no term on the return (the episode ends at exit). Difference: the reward is in-session engagement (session depth), so the user's in-session stop still removes represented value (non-zero content at the stop); not reflective value; no zero-stake statement.
  > "Each episode involves a fixed user and terminates when the user exits the platform."
  > "our goal is to optimize long-term user engagement at the session level"

