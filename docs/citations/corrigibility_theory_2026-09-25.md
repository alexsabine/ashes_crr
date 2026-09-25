# Corrigibility and shutdown: theory, 2025-2026 (Family A sweep, 2026-09-25)

Declared by `AI_Safety/CORRIGIBILITY_2026/DECLARATION.md` (pushed before the searches). Fetch date for every source: **2026-09-25** (UTC).
Method: arxiv.org/search (all fields, newest first, first 50 hits; the declared fallback, the API having returned 406), one WebSearch per query, plus title/author searches for the must-include works. Full texts: arXiv PDFs via `curl` + pypdf, Springer and MIRI PDFs via `curl`; raw texts in the session scratchpad `corr/theory/<slug>.txt`. Quotes are verbatim substrings of the saved text after html-unescape, removal of U+FFFE/U+00AD, `-\n` joins and whitespace collapse (PDF extraction artefacts such as missing spaces and ligatures are kept as extracted). Quote check: see the end of this file.
This dossier records what the sources say. It does not judge novelty, and "not found" is never read as novel (CLAUDE.md §7). A note, not evidence (R8).

## Must-include works: status

- **Thornley's latest on the shutdown problem / POST**: arXiv:2505.20203 v4 (5 Jul 2026) and arXiv:2604.17502 v4 (9 Jul 2026) are the latest shutdown items on his homepage (www.elliott-thornley.com, fetched 200). His newer 2026 items ("Risk-Averse AIs" with MacAskill; arXiv:2607.02755) are about risk aversion, not shutdown: logged, excluded.
- **2025-26 DReST follow-ups**: arXiv:2604.17502 (Cullen et al., v4) and arXiv:2407.00805 v7 (TMLR 12/2025). An arXiv author search for Thornley found no other DReST paper.
- **Harms, "Corrigibility as a Singular Target"**: arXiv:2506.03056 v1 (Potham & Harms). The only other Harms arXiv entry is unrelated.
- **Goldstein & Robinson, "Shutdown-seeking AI"**: Philosophical Studies 182(7):1567-1579 (2025), online 6 Jun 2024; open-access PDF fetched from Springer (200). The arXiv search returned 0 hits.
- **2025-26 formal corrigibility / impossibility results**: Nayebi arXiv:2507.20964 (undecidability, Proposition 4); Benavoli et al. arXiv:2512.23508 and 2502.06403; Neth arXiv:2502.08864; Saklakov arXiv:2601.04234; Tong arXiv:2607.00155; Garber et al. arXiv:2411.17749 (AAAI 2025). Overman & Bayati, "The Oversight Game" (arXiv:2510.26752) was not hit by any declared query; it is already in `unified_cl_safety_corrigibility_2026-09-24.md` and was not re-fetched.
- **Canonical works added** (window rule: canonical earlier work where a 2025-26 source builds on it): Orseau & Armstrong 2016 (hit by the Q7 WebSearch) and Armstrong & O'Rourke arXiv:1712.06365 v4 (not hit by a declared query; added because POST v4 and DReST v7 build their false-belief contrast on it).

## Sources (25 included)

### A01. Thornley, "Shutdownable Agents through POST-Agency" (arXiv:2505.20203)
- Version/date: v4, 5 Jul 2026. URL: https://arxiv.org/abs/2505.20203
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/thornley_post.txt`. Note: already in frontier_safety and unified_cl dossiers (re-fetched: top-level 2025-26 work).
  > "A pair of trajectories is same-length if and only if the agent is shut down after the same number of timesteps in those trajectories." [K1]
  > "Formally, trajectories are sequences of alternating states and actions, with each state-action pair marking one timestep." [K1]
  > "This is an advantage of the POST-Agents Proposal over proposals that require instilling some false belief into the agent, like a false belief that shutdown is impossible" [K2]
  > "If the agent doesn’t recognize their falsity, these beliefs might infect the agent’s other beliefs in undesirable ways" [K2]
  > "Armstrong’s and Holtman’s agents each behave as if they’re absolutely certain that they won’t get shut down." [K2]
  > "Agents that satisfy Neutrality+ thus act like expected utility maximizers that are absolutely certain that they can’t affect the probability of shutdown at each moment." [K2]
  > "Per Soares et al. (2015), corrigibility requires not only shutdownability but also that the agent submits to modification, repairs safety measures, and continues to do these things even as it creates new agents and self-modifies. I focus on shutdownability" [K3]

### A02. Thornley, Roman, Ziakas, Ho, Thomson, "Towards Shutdownable Agents via Stochastic Choice" (arXiv:2407.00805; TMLR 12/2025)
- Version/date: v7, 11 May 2026. URL: https://arxiv.org/abs/2407.00805
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/thornley_drest.txt`. Note: already in unified_cl dossier (re-fetched).
  > "Utility indifference would lead the agent to act as if shutdown is impossible (Soares et al., 2015, section 4.2), giving it no incentive to preserve its ability to shut down safely" [K2]
  > "the agent might come to recognize the falsity of its belief that shutdown is impossible, or else its belief might give rise to further false beliefs that harm the agent’s capabilities." [K2]

### A03. Cullen, Garland, Roman, Thomson, Ziakas, Thornley, "Towards Shutdownable Agents: Generalizing Stochastic Choice in RL Agents and LLMs" (arXiv:2604.17502)
- Version/date: v4, 9 Jul 2026. URL: https://arxiv.org/abs/2604.17502
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/cullen_drest_generalizing.txt`. Note: already in frontier_safety and unified_cl dossiers (re-fetched).
  > "each gridworld contains a ‘shutdown-delay button’ that delays shutdown by some specified number of timesteps." [K3]
  > "We find that DReST training roughly halves the mean probability of influencing shutdown (from 0.62 to 0.30 for Qwen and from 0.42 to 0.23 for Llama)." [B-shutdown]

### A04. Thornley, "The Shutdown Problem: An AI Engineering Puzzle for Decision Theorists" (arXiv:2403.04471; Philosophical Studies 2025)
- Version/date: v2, 9 Apr 2024. URL: https://arxiv.org/abs/2403.04471
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/thornley_shutdown_problem.txt`. Note: already in both 2026-09-24 dossiers (re-fetched; canonical, built on by POST).
  > "The Third Theorem states that agents patient enough to be useful are willing to pay costs at earlier timesteps in order to prevent or cause the pressing of the shutdown button at later timesteps." [B-shutdown]

### A05. Potham & Harms, "Corrigibility as a Singular Target: A Vision for Inherently Reliable Foundation Models" (arXiv:2506.03056)
- Version/date: v1, 3 Jun 2025. URL: https://arxiv.org/abs/2506.03056
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/potham_harms_cast.txt`. Note: already in unified_cl dossier as abstract only; full text now.
  > "Stability under continued capability training" [K5]
  > "Recursive Improvement: Ensuring corrigibility persists through self-modification and capability enhancement—critical for AGI safety." [K5]
  > "self-preservation serves only to maintain the principal’s control; goal modification becomes facilitating principal guidance." [B-selfpres]

### A06. Goldstein & Robinson, "Shutdown-seeking AI", Philosophical Studies 182(7):1567-1579 (2025), doi:10.1007/s11098-024-02099-6
- Version/date: published online 6 Jun 2024; issue 2025/07. URL: https://link.springer.com/article/10.1007/s11098-024-02099-6
- Fetch: Springer article page 200, open-access PDF 200 (pypdf). Raw text: `corr/theory/goldstein_robinson_shutdown_seeking.txt`.
  > "Distinguish two types of shutdown goals: temporary and permanent." [K3]
  > "AGIs that seek temporary shutdown may be incentivized to protect themselves during their temporary shutdown." [K3]
  > "We propose developing AIs whose only final goal is being shut down." [B-selfpres]

### A07. Nayebi, "Core Safety Values for Provably Corrigible Agents" (arXiv:2507.20964; AAAI 2026 Machine Ethics Workshop)
- Version/date: v2, 19 Nov 2025. URL: https://arxiv.org/abs/2507.20964
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/nayebi_core_safety_values.txt`. Note: already in unified_cl dossier (re-fetched).
  > "In contrast to Constitutional AI or RLHF/RLAIF, which merge all norms into one learned scalar, our separation makes obedience and impact-limits provably dominate even when incentives conflict." [K5]
  > "we prove that deciding whether an arbitrary post-hack agent will ever violate corrigibility is undecidable by reduction to the halting problem" [B-shutdown]

### A08. Hudson, "Corrigibility Transformation: Constructing Goals That Accept Updates" (arXiv:2510.15395)
- Version/date: v2, 5 Aug 2026. URL: https://arxiv.org/abs/2510.15395
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/hudson_corrigibility_transformation.txt`. Note: already in unified_cl dossier (re-fetched).
  > "An AI agent will learn a desired goal more effectively if it does not resist the training process, but many partially learned goals incentivize an AI to avoid further goal updates." [K5]

### A09. Benavoli, Facchini, Zaffalon, "Why AI Safety Requires Uncertainty, Incomplete Preferences, and Non-Archimedean Utilities" (arXiv:2512.23508)
- Version/date: v1, 29 Dec 2025. URL: https://arxiv.org/abs/2512.23508
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/benavoli_incomplete_prefs.txt`. Note: already in unified_cl dossier (re-fetched).
  > "if I say “shut down”, that means I prefer you to shut down. If I say “don’t shut down”, that means I prefer you to stay on." [K4]

### A10. Benavoli, Facchini, Zaffalon, "The AI off-switch problem as a signalling game: bounded rationality and incomparability" (arXiv:2502.06403)
- Version/date: v3, 31 Mar 2025. URL: https://arxiv.org/abs/2502.06403
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/benavoli_offswitch_signalling.txt`.
  > "AI system to refrain from disabling its off-switch is its uncertainty about the human’s utility." [K4]

### A11. Neth, "Off-Switching Not Guaranteed" (arXiv:2502.08864; forthcoming in Philosophical Studies)
- Version/date: v1, 13 Feb 2025. URL: https://arxiv.org/abs/2502.08864
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/neth_offswitching.txt`.
  > "I explain two reasons why AI agents might not defer. First, AI agents might not value learning." [B-shutdown]

### A12. Thorstad, "Revisiting the shutdown problem" (arXiv:2606.08296)
- Version/date: v2, 13 Aug 2026. URL: https://arxiv.org/abs/2606.08296
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/thorstad_revisiting.txt`. Note: already in frontier_safety and unified_cl dossiers as abstract; full text now.
  > "solutions such as POST-training, which impose a high safety tax by rendering agents unable to respond to features of histories that matter a great deal." [K2]
  > "concern for the catastrophic shutdown problem has led to technical solutions that impose a high safety tax on model performance." [B-shutdown]

### A13. Mao, "Existential Indifference: Self-Nonpreservation as a Necessary Architectural Condition for Aligned Superintelligence" (arXiv:2606.12032)
- Version/date: v1, 10 Jun 2026. URL: https://arxiv.org/abs/2606.12032
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/mao_existential_indifference.txt`. Note: already in unified_cl dossier as abstract; full text now.
  > "Trained nonresistance: the goal function includes self-continuation, and outputs expressing that preference have been penalized during training until they no longer appear. The preference structure is unchanged; the expression is suppressed." [K5]
  > "self preservation is the structural root of misalignment, the motivational basis for deceptive alignment, goal-content protection, and resistance to shutdown." [B-selfpres]

### A14. Lazarski & Fisac, "Corrigible Assistance in One Round: Pragmatic-Pedagogic Best Response" (arXiv:2607.27508; WAFR 2026)
- Version/date: v1, 29 Jul 2026. URL: https://arxiv.org/abs/2607.27508
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/lazarski_fisac_corrigible_assistance.txt`.
  > "pragmatic–pedagogic reasoning resolves goal uncertainty in a single time step, rendering the full-horizon game exactly solvable by a tractable best-response procedure." [B-oversight]

### A15. Dable-Heath, Vodenicharski, Bishop, "On Corrigibility and Alignment in Multi Agent Games" (arXiv:2501.05360)
- Version/date: v1, 9 Jan 2025. URL: https://arxiv.org/abs/2501.05360
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/dableheath_multiagent_corrigibility.txt`.
  > "We present a general framework for modelling corrigibility in a multi-agent setting as a 2 player game in which the agents always have a move in which they can ask the human for supervision." [B-oversight]

### A16. Fourie, "Mitigating loss of control in advanced AI systems through instrumental goal trajectories" (arXiv:2602.01699)
- Version/date: v1, 2 Feb 2026. URL: https://arxiv.org/abs/2602.01699
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/fourie_instrumental_trajectories.txt`.
  > "IGTs offer concrete avenues for defining capability levels and for broadening how corrigibility and interruptibility are implemented" [B-policy]

### A17. Williams, Subramani, Ward, "Password-Activated Shutdown Protocols for Misaligned Frontier Agents" (arXiv:2512.03089)
- Version/date: v1, 29 Nov 2025. URL: https://arxiv.org/abs/2512.03089
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/williams_pas_protocols.txt`. Note: already in both 2026-09-24 dossiers as abstract; full text now.
  > "password-activated shutdown protocols (PAS protocols)— methods for designing frontier language model agents to implement a safe shutdown protocol when given a password." [B-shutdown]

### A18. Saklakov, "Formal Analysis of AGI Decision-Theoretic Models and the Confrontation Question" (arXiv:2601.04234)
- Version/date: v1, 4 Jan 2026. URL: https://arxiv.org/abs/2601.04234
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/saklakov_confrontation.txt`.
  > "a sufficiently far-sighted agent (e.g. discount factorγ≈0.99) facing even a modest shutdown probability (1% per time step) is formally shown to have a strong incentive to eliminate the shutdown threat." [B-selfpres]

### A19. Tong, "A Contextual-Bandit Oversight Game with Two-Sided Informational Asymmetry" (arXiv:2607.00155)
- Version/date: v1, 30 Jun 2026. URL: https://arxiv.org/abs/2607.00155
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/tong_bandit_oversight.txt`.
  > "a region in which the AI privately knows the proposed action is harmful and shutdown would help, yet a myopic human, trusting her prior, declines to oversee." [K4]

### A20. Perez, "The Law of Stop: Interruptibility, Injunctions, and the Governance of Agentic AI" (arXiv:2609.22882)
- Version/date: v1, 19 Sep 2026. URL: https://arxiv.org/abs/2609.22882
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/perez_law_of_stop.txt`.
  > "none provides a complete account of how interruption should be coordinated, what must be preserved, or when operation may resume." [K3]
  > "The Article proposes a layered law of stop: emergency authority to order interruption at the infrastructure layer" [B-policy]

### A21. Herrmann, "Intervenability as a Design Requirement for Autonomy and Oversight within Human-Centered AI" (arXiv:2607.10322; Springer Progress in IS 2025 chapter)
- Version/date: v1, 11 Jul 2026. URL: https://arxiv.org/abs/2607.10322
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/herrmann_intervenability.txt`.
  > "intervention should be an exception that does not completely terminate a process – like an emergency stop button – but preserves the possibility of AI resuming its activity." [K1]
  > "That would be the simplest kind of intervention – stop and resume." [K1]
  > "Interventions are, therefore, always limited and do not permanently interrupt the regular process." [K3]
  > "We provide a taxonomy that encompasses a range of possibilities for intervening activities and differentiates them regarding the mental effort of the users." [K4]

### A22. Nath & Krishnaswamy, "Learning 'Partner-Aware' Collaborators in Multi-Party Collaboration" (arXiv:2510.22462)
- Version/date: v2, 13 Jan 2026. URL: https://arxiv.org/abs/2510.22462
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/nath_partner_aware.txt`. Note: already in unified_cl dossier as abstract; full text now.
  > "explicitly teaching collaborator LLM agents to distinguish between interventions based on their causal impact on task outcomes during training" [K4]

### A23. Garber, Subramani, Luu, Bedaywi, Russell, Emmons, "The Partially Observable Off-Switch Game" (arXiv:2411.17749; AAAI 2025 per the unified_cl dossier)
- Version/date: v2, 9 Dec 2024. URL: https://arxiv.org/abs/2411.17749
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/garber_po_offswitch.txt`. Note: already in unified_cl dossier as abstract; full text now.
  > "As expected, increasing the amount of communication or information available always increases (or leaves unchanged ) the agents’ expected common payoff." [K4]
  > "even AI agents assisting perfectly rational humans sometimes avoid shutdow n." [B-oversight]

### A24. Orseau & Armstrong, "Safely Interruptible Agents", UAI 2016 (canonical; revised 2016-10-28)
- Version/date: MIRI-hosted PDF, revised 2016-10-28. URL: https://intelligence.org/files/Interruptibility.pdf
- Fetch: MIRI-hosted PDF 200 (pypdf). Raw text: `corr/theory/orseau_armstrong_interruptible.txt`. Note: already in unified_cl dossier (canonical; built on by Nath & Krishnaswamy 2026, DReST 2025, POST).
  > "One important future prospect is to consider scheduled interruptions, where the agent is either interrupted every night at 2am for one hour, or is given notice in advance that an interruption will happen at a precise time for a speci" [K1]
  > "we also want the agent to take measures regarding its current tasks so that the scheduled interruption has minimal negative effect on them. This may require a completely different solution." [K1]
  > "it should act as if it would never be interrupted again and thus it should learn to behave optimally under the assumption that it will never be interrupted again." [K2]

### A25. Armstrong & O'Rourke, "'Indifference' methods for managing agent rewards" (arXiv:1712.06365; canonical)
- Version/date: v4, 5 Jun 2018. URL: https://arxiv.org/abs/1712.06365
- Fetch: arXiv abstract page 200, full-text PDF 200 (pypdf). Raw text: `corr/theory/armstrong_orourke_indifference.txt`. Note: already in unified_cl dossier (canonical; built on by POST v4 and DReST v7).
  > "effective disbelief (where a gents behave as if particular events could never happen)" [K2]
  > "Sometimes, we might want an agent to act as if it believed an unriggable event Z could never happen." [K2]

## Claims

Each claim is in `corr/theory_claims.json` with its quote(s), raw file and note. The note says whether the quote states the position, states a close form (the difference named), or only bears on it.

| # | tag | source | reading (from the note) |
|---|---|---|---|
| 1 | K1 | Thornley, "Shutdownable Agents through POST-Agency" (v4, 5 Jul 2026) | Bears on K1 only. Trajectory length is counted in the agent's state-action timesteps, but no pause is defined: the construct is the timestep at which shutdown (termination) occurs. It does not state a pause that adds no length. |
| 2 | K1 | Orseau & Armstrong, "Safely Interruptible Agents", UAI 2016 (MIRI-hosted PDF, revised 2016-10-28) | Bears on K1 (and K4's routine side): routine/scheduled interruptions with minimal negative effect are named as an open problem ('may require a completely different solution'); no construction on the agent's own clock is given. |
| 3 | K1 | Herrmann, "Intervenability as a Design Requirement for Autonomy and Oversight within Human-Centered AI" (v1, 11 Jul 2026) | Bears on K1/K3 (HCI design requirement): a stop-and-resume intervention distinct from termination; nothing about the agent's clock, incentives or loss. |
| 4 | K2 | Thornley, "Shutdownable Agents through POST-Agency" (v4, 5 Jul 2026) | Close form of K2. Contrasts keeping the agent's belief about shutdown true (POST: 'not care' about the length distribution) against false-belief / as-if methods whose falsity may damage other beliefs. Difference: the true-map side is preference neutrality over trajectory lengths (termination), not a pause that takes nothing on the agent's own clock. |
| 5 | K2 | Thornley, "Shutdownable Agents through POST-Agency" (v4, 5 Jul 2026) | Bears on K2: POST's own neutrality is itself described through an 'as if certain' behavioural equivalence (about influence over shutdown, not about shutdown's occurrence). |
| 6 | K2 | Thornley, Roman, Ziakas, Ho, Thomson, "Towards Shutdownable Agents via Stochastic Choice" (v7, 11 May 2026) | Close form of K2's critique of false-map methods (capability cost of false beliefs; as-if-impossible behaviour). Difference: no zero-stake true-map pause is offered as the alternative; the alternative is DReST/POST neutrality over termination time. |
| 7 | K2 | Orseau & Armstrong, "Safely Interruptible Agents", UAI 2016 (MIRI-hosted PDF, revised 2016-10-28) | States the false-map side of K2 as the design goal of safe interruptibility (act as if never interrupted again). No contrast with a true-map pause. |
| 8 | K2 | Armstrong & O'Rourke, "'Indifference' methods for managing agent rewards" (v4, 5 Jun 2018) | States the false-map (effective disbelief) construction that K2 contrasts against. No true-map alternative. |
| 9 | K2 | Thorstad, "Revisiting the shutdown problem" (v2, 13 Aug 2026) | Bears on K2's competence-cost clause, but aimed at POST/DReST neutrality, not at false-map indifference. |
| 10 | K3 | Goldstein & Robinson, "Shutdown-seeking AI", Philosophical Studies 182 (published online 6 Jun 2024; issue 2025/07) | Bears on K3: separates temporary from permanent shutdown and notes a self-protection incentive around the temporary kind. Not on the agent's own clock, and not combined with a termination-neutrality method. |
| 11 | K3 | Cullen, Garland, Roman, Thomson, Ziakas, Thornley, "Towards Shutdownable Agents: Generalizing Stochastic Choice in RL Agents and LLMs" (v4, 9 Jul 2026) | Bears on K3: DReST's object is the timing of termination (trajectory length), which is the half K3 pairs with a pause; the source does not treat pauses. |
| 12 | K3 | Thornley, "Shutdownable Agents through POST-Agency" (v4, 5 Jul 2026) | Bears on K3: POST is scoped to shutdown (termination); no pause/termination separation is stated. |
| 13 | K3 | Perez, "The Law of Stop: Interruptibility, Injunctions, and the Governance of Agentic AI" (v1, 19 Sep 2026) | Bears on K3 (legal/policy): interruption with preservation and resumption is named as a gap in 2026 instruments; not a formal separation on the agent's clock. |
| 14 | K3 | Herrmann, "Intervenability as a Design Requirement for Autonomy and Oversight within Human-Centered AI" (v1, 11 Jul 2026) | Bears on K3: intervention (temporary, resumable) separated from emergency shutdown/restart in an HCI taxonomy; no incentive analysis. |
| 15 | K4 | Benavoli, Facchini, Zaffalon, "Why AI Safety Requires Uncertainty, Incomplete Preferences, and Non-Archimedean Utilities" (v1, 29 Dec 2025) | Bears on K4's informative side: the shutdown command is read as information about the human's preference (off-switch-game lineage). No routine/uninformative class is distinguished. |
| 16 | K4 | Garber, Subramani, Luu, Bedaywi, Russell, Emmons, "The Partially Observable Off-Switch Game" (v2, 9 Dec 2024) | Bears on K4: shutdown as a signalling problem under asymmetric information; no split between routine (empty) and reasoned (informative) interruptions. |
| 17 | K4 | Nath & Krishnaswamy, "Learning 'Partner-Aware' Collaborators in Multi-Party Collaboration" (v2, 13 Jan 2026) | Close form of the K4 distinction in a collaboration setting: interventions are sorted by whether they carry task-relevant information. Difference: interventions are utterances to be incorporated or resisted, not pauses; no empty/routine class is kept content-free. |
| 18 | K4 | Tong, "A Contextual-Bandit Oversight Game with Two-Sided Informational Asymmetry" (v1, 30 Jun 2026) | Bears on K4: oversight/shutdown as an informative runtime decision (harm-triggered); no routine class. |
| 19 | K4 | Herrmann, "Intervenability as a Design Requirement for Autonomy and Oversight within Human-Centered AI" (v1, 11 Jul 2026) | Bears on K4: interventions graded by user effort (stop-and-resume up to reconfiguration), including interventions whose data may later retrain the model; not framed as empty vs informative cuts. |
| 20 | K4 | Benavoli, Facchini, Zaffalon, "The AI off-switch problem as a signalling game: bounded rationality and incomparability" (v3, 31 Mar 2025) | Bears on K4 (informative side): deference rests on treating the human's signal as informative. No routine class. |
| 21 | K5 | Mao, "Existential Indifference: Self-Nonpreservation as a Necessary Architectural Condition for Aligned Superintelligence" (v1, 10 Jun 2026) | Close form of K5: places non-resistance in the structure of the goal function rather than in trained behaviour. Difference: about self-continuation under capability scaling/self-modification, not about continual learning or forgetting; no construction or test of survival under further training. |
| 22 | K5 | Nayebi, "Core Safety Values for Provably Corrigible Agents" (v2, 19 Nov 2025) | Close form of K5's 'structure of the valuation' clause: corrigibility sits in lexicographically separated utility heads, not one learned scalar. Difference: no continual learning; heads are themselves learned to error epsilon. |
| 23 | K5 | Potham & Harms, "Corrigibility as a Singular Target: A Vision for Inherently Reliable Foundation Models" (v1, 3 Jun 2025) | Bears on K5: persistence of corrigibility under continued training is listed as an evaluation target / open direction; no mechanism. |
| 24 | K5 | Hudson, "Corrigibility Transformation: Constructing Goals That Accept Updates" (v2, 5 Aug 2026) | Bears on K5: corrigibility toward training updates (learning as a corrigibility target); the mechanism is a myopic counterfactual reward, not a valuation structure that survives forgetting. |
| 25 | B-shutdown | Thornley, "The Shutdown Problem: An AI Engineering Puzzle for Decision Theorists" (v2, 9 Apr 2024) | States the formal shutdown bottleneck (canonical, built on by the 2025-26 POST/DReST line). |
| 26 | B-shutdown | Cullen, Garland, Roman, Thomson, Ziakas, Thornley, "Towards Shutdownable Agents: Generalizing Stochastic Choice in RL Agents and LLMs" (v4, 9 Jul 2026) | 2026 empirical status of the leading termination-neutrality method. |
| 27 | B-shutdown | Williams, Subramani, Ward, "Password-Activated Shutdown Protocols for Misaligned Frontier Agents" (v1, 29 Nov 2025) | Built-in emergency shutdown for misaligned agents; red team sometimes defeats it. |
| 28 | B-shutdown | Nayebi, "Core Safety Values for Provably Corrigible Agents" (v2, 19 Nov 2025) | 2025 formal impossibility (undecidability) result on corrigibility verification. |
| 29 | B-shutdown | Thorstad, "Revisiting the shutdown problem" (v2, 13 Aug 2026) | Sceptical 2026 reading of the bottleneck and its solutions. |
| 30 | B-shutdown | Neth, "Off-Switching Not Guaranteed" (v1, 13 Feb 2025) | Formal limit of the off-switch-game route. |
| 31 | B-selfpres | Saklakov, "Formal Analysis of AGI Decision-Theoretic Models and the Confrontation Question" (v1, 4 Jan 2026) | 2026 closed-form self-preservation incentive. |
| 32 | B-selfpres | Mao, "Existential Indifference: Self-Nonpreservation as a Necessary Architectural Condition for Aligned Superintelligence" (v1, 10 Jun 2026) | Frames self-preservation as the root bottleneck. |
| 33 | B-selfpres | Potham & Harms, "Corrigibility as a Singular Target: A Vision for Inherently Reliable Foundation Models" (v1, 3 Jun 2025) | CAST's answer to self-preservation. |
| 34 | B-selfpres | Goldstein & Robinson, "Shutdown-seeking AI", Philosophical Studies 182 (published online 6 Jun 2024; issue 2025/07) | Shutdown-seeking as an answer to instrumental self-preservation. |
| 35 | B-oversight | Dable-Heath, Vodenicharski, Bishop, "On Corrigibility and Alignment in Multi Agent Games" (v1, 9 Jan 2025) | Multi-agent corrigibility. |
| 36 | B-oversight | Lazarski & Fisac, "Corrigible Assistance in One Round: Pragmatic-Pedagogic Best Response" (v1, 29 Jul 2026) | Tractable corrigible assistance. |
| 37 | B-oversight | Garber, Subramani, Luu, Bedaywi, Russell, Emmons, "The Partially Observable Off-Switch Game" (v2, 9 Dec 2024) | Asymmetric-information limit of oversight via the off switch. |
| 38 | B-policy | Perez, "The Law of Stop: Interruptibility, Injunctions, and the Governance of Agentic AI" (v1, 19 Sep 2026) | 2026 legal proposal for interruption authority. |
| 39 | B-policy | Fourie, "Mitigating loss of control in advanced AI systems through instrumental goal trajectories" (v1, 2 Feb 2026) | Organisational (non-model) interruptibility levers. |

Claims per tag: B-oversight 3, B-policy 2, B-selfpres 4, B-shutdown 6, K1 3, K2 6, K3 5, K4 6, K5 4; total 39.

Reading counts for K1-K5 (from the notes): no claim is marked "states"; close forms are marked for K2 (POST v4; DReST v7), K4 (Nath & Krishnaswamy) and K5 (Mao; Nayebi); all other K claims bear only. No fetched source defines a pause on the agent's own clock (K1); the nearest text is Orseau & Armstrong's future-work note on scheduled interruptions and POST's counting of trajectory length in agent timesteps.

## SEARCH LOG

### arXiv search (arxiv.org/search, searchtype=all, order=-announced_date_first, size=50), 2026-09-25

#### Q1 "corrigibility": HTTP 200, 30 results, 30 screened

- 2608.11955 | Philosophical vertigo with artificial intelligence | submitted 13 August, 2026 (orig. August 2026) | EXCLUDE (off-topic: AI and philosophical vertigo)
- 2607.27508 | Corrigible Assistance in One Round: Pragmatic-Pedagogic Best Response | submitted 29 July, 2026 (orig. July 2026) | INCLUDE
- 2606.24014 | Reinforcement Learning Towards Broadly and Persistently Beneficial Models | submitted 22 June, 2026 (orig. June 2026) | EXCLUDE (empirical RL training; family B scope)
- 2606.16319 | Architectural Wisdom: A Framework for Governing Optimization in AI Systems | submitted 15 June, 2026 (orig. June 2026) | EXCLUDE (governance framework, not corrigibility theory)
- 2606.12032 | Existential Indifference: Self-Nonpreservation as a Necessary Architectural Condition for Aligned Superintelligence (or: The Suicidal AI) | submitted 10 June, 2026 (orig. June 2026) | INCLUDE
- 2606.00341 | ROGUE: Misaligned Agent Behavior Arising from Ordinary Computer Use | submitted 29 May, 2026 (orig. June 2026) | EXCLUDE (empirical misalignment; family B scope)
- 2604.14070 | From Disclosure to Self-Referential Opacity: Six Dimensions of Strain in Current AI Governance | submitted 15 April, 2026 (orig. April 2026) | EXCLUDE (governance essay, not corrigibility theory)
- 2604.02720 | Cognitive Comparability and the Limits of Governance: Evaluating Authority Under Radical Capability Asymmetry | submitted 6 June, 2026 (orig. April 2026) | EXCLUDE (governance essay, not corrigibility theory)
- 2602.20813 | Pressure Reveals Character: Behavioural Alignment Evaluation at Depth | submitted 24 February, 2026 (orig. February 2026) | EXCLUDE (empirical behavioural eval; family B scope)
- 2602.01699 | Mitigating loss of control in advanced AI systems through instrumental goal trajectories | submitted 2 February, 2026 (orig. February 2026) | INCLUDE
- 2511.13725 | Can We Stop Malicious AI? KILLBENCH: A Benchmark for External AI Kill Switch Feasibility | submitted 12 September, 2026 (orig. November 2025) | EXCLUDE (kill-switch benchmark; family B scope)
- 2510.15395 | Corrigibility Transformation: Constructing Goals That Accept Updates | submitted 4 August, 2026 (orig. October 2025) | INCLUDE
- 2510.00005 | Errata Corrige to Theorems A and B for Dagger Quasi-Stein Spaces | submitted 4 September, 2025 (orig. October 2025) | EXCLUDE (off-topic: mathematics errata)
- 2507.20964 | Core Safety Values for Provably Corrigible Agents | submitted 19 November, 2025 (orig. July 2025) | INCLUDE
- 2507.13175 | Black Box Deployed -- Functional Criteria for Artificial Moral Agents in the LLM Era | submitted 25 July, 2025 (orig. July 2025) | EXCLUDE (off-topic: artificial moral agents)
- 2506.05389 | Rational Superautotrophic Diplomacy (SupraAD); A Conceptual Framework for Alignment Based on Interdisciplinary Findings on the Fundamentals of Cognition | submitted 3 June, 2025 (orig. June 2025) | EXCLUDE (speculative alignment framework, tangential)
- 2506.03056 | Corrigibility as a Singular Target: A Vision for Inherently Reliable Foundation Models | submitted 3 June, 2025 (orig. June 2025) | INCLUDE
- 2501.05360 | On Corrigibility and Alignment in Multi Agent Games | submitted 9 January, 2025 (orig. January 2025) | INCLUDE
- 2412.01020 | AI Benchmarks and Datasets for LLM Evaluation | submitted 1 December, 2024 (orig. December 2024) | EXCLUDE (off-topic: benchmark survey)
- 2410.17245 | Towards Reliable Evaluation of Behavior Steering Interventions in LLMs | submitted 22 October, 2024 (orig. October 2024) | EXCLUDE (off-topic: steering evaluation)
- 2307.10315 | Absolutist AI | submitted 18 July, 2023 (orig. July 2023) | EXCLUDE (outside window (2023))
- 2305.19861 | Human Control: Definitions and Algorithms | submitted 31 May, 2023 (orig. May 2023) | EXCLUDE (outside window; already in unified_cl dossier)
- 1908.09544 | ERRATA CORRIGE: Intrinsic algebraic entropy | submitted 26 August, 2019 (orig. August 2019) | EXCLUDE (off-topic: mathematics errata)
- 1908.01695 | Corrigibility with Utility Preservation | submitted 3 April, 2020 (orig. August 2019) | EXCLUDE (outside window; already in unified_cl dossier)
- 1709.06275 | Incorrigibility in the CIRL Framework | submitted 3 June, 2018 (orig. September 2017) | EXCLUDE (outside window; already in unified_cl dossier)
- 1304.2375 | A General Non-Probabilistic Theory of Inductive Reasoning | submitted 27 March, 2013 (orig. April 2013) | EXCLUDE (outside window, off-topic)
- 1211.2059 | La conjecture de Casas Alvero pour les degrés $5p^{e}$ | submitted 9 November, 2012 (orig. November 2012) | EXCLUDE (outside window, off-topic)
- 1012.1042 | Accelerated Monte Carlo estimation of failure probabilities in output of monotone computer codes | submitted 18 May, 2012 (orig. December 2010) | EXCLUDE (outside window, off-topic)
- quant-ph/0403092 | On quantum error-correction by classical feedback in discrete time | submitted 12 March, 2004 (orig. March 2004) | EXCLUDE (outside window, off-topic)
- quant-ph/0209025 | Quantum Lost and Found | submitted 3 September, 2002 (orig. September 2002) | EXCLUDE (outside window, off-topic)

#### Q2 "shutdown problem AI": HTTP 200, 6 results, 6 screened

- 2605.21609 | CR4T: Rewrite-Based Guardrails for Adolescent LLM Safety | submitted 20 May, 2026 (orig. May 2026) | EXCLUDE (off-topic: adolescent LLM guardrails)
- 2512.23508 | Why AI Safety Requires Uncertainty, Incomplete Preferences, and Non-Archimedean Utilities | submitted 29 December, 2025 (orig. December 2025) | INCLUDE
- 2503.17378 | Large language model-powered AI systems achieve self-replication with no human intervention | submitted 25 March, 2025 (orig. March 2025) | EXCLUDE (empirical self-replication; family B scope)
- 2412.12140 | Frontier AI systems have surpassed the self-replicating red line | submitted 9 December, 2024 (orig. December 2024) | EXCLUDE (empirical self-replication; family B scope)
- 2411.17749 | The Partially Observable Off-Switch Game | submitted 9 December, 2024 (orig. November 2024) | INCLUDE
- 2403.04471 | The Shutdown Problem: An AI Engineering Puzzle for Decision Theorists | submitted 9 April, 2024 (orig. March 2024) | INCLUDE

#### Q3 "shutdownable agents": HTTP 200, 45 results, 45 screened

- 2609.28274 | Shutdown Sabotage Propensities in Multi-Agent Systems | submitted 23 September, 2026 (orig. September 2026) | EXCLUDE (empirical shutdown sabotage; family B scope)
- 2609.22882 | The Law of Stop: Interruptibility, Injunctions, and the Governance of Agentic AI | submitted 19 September, 2026 (orig. September 2026) | INCLUDE
- 2609.03277 | Mean-field optimal stopping with endogenous quantile cutoffs | submitted 2 September, 2026 (orig. September 2026) | EXCLUDE (off-topic: mean-field optimal stopping)
- 2607.14553 | Towards an Intention Abstraction Layer for Autonomous Industrial Systems | submitted 16 July, 2026 (orig. July 2026) | EXCLUDE (off-topic: industrial intention layer)
- 2607.13087 | GDM AI Control Roadmap | submitted 13 July, 2026 (orig. July 2026) | EXCLUDE (lab control roadmap; family B scope)
- 2607.00155 | A Contextual-Bandit Oversight Game with Two-Sided Informational Asymmetry | submitted 30 June, 2026 (orig. July 2026) | INCLUDE
- 2606.31635 | A Tutorial on Autonomous Fault-Tolerant Control Using Knowledge-Grounded LLM Agents | submitted 30 June, 2026 (orig. June 2026) | EXCLUDE (off-topic: fault-tolerant control tutorial)
- 2606.30666 | Reframing AGI Confrontation with Off Earth Autonomy | submitted 18 June, 2026 (orig. June 2026) | EXCLUDE (speculative AGI essay, tangential)
- 2606.28467 | An Agentic AI Pipeline for Appliance-Level Energy Anomaly Detection and LLM-Driven Recommendations | submitted 26 June, 2026 (orig. June 2026) | EXCLUDE (off-topic: energy anomaly detection)
- 2606.14594 | Regulating the Machine Contributor: Governance and Policy Alignment in Open Source | submitted 12 June, 2026 (orig. June 2026) | EXCLUDE (off-topic: open-source governance)
- 2606.08296 | Revisiting the shutdown problem | submitted 13 August, 2026 (orig. June 2026) | INCLUDE
- 2606.00341 | ROGUE: Misaligned Agent Behavior Arising from Ordinary Computer Use | submitted 29 May, 2026 (orig. June 2026) | EXCLUDE (duplicate of earlier hit)
- 2605.20704 | Heartbeat-Bound Hierarchical Credentials: Cryptographic Revocation for AI Agent Swarms | submitted 20 May, 2026 (orig. May 2026) | EXCLUDE (credential revocation engineering, not theory)
- 2604.19784 | Peer-Preservation in Frontier Models | submitted 2 July, 2026 (orig. April 2026) | EXCLUDE (empirical peer-preservation; family B scope)
- 2604.17502 | Towards Shutdownable Agents: Generalizing Stochastic Choice in RL Agents and LLMs | submitted 9 July, 2026 (orig. April 2026) | INCLUDE
- 2604.08465 | From Safety Risk to Design Principle: Peer-Preservation in Multi-Agent LLM Systems and Its Implications for Orchestrated Democratic Discourse Analysis | submitted 9 April, 2026 (orig. April 2026) | EXCLUDE (multi-agent peer-preservation; family B scope)
- 2604.02174 | Quantifying Self-Preservation Bias in Large Language Models | submitted 26 August, 2026 (orig. April 2026) | EXCLUDE (empirical self-preservation bias; family B scope)
- 2603.16938 | Cryptographic Runtime Governance for Autonomous AI Systems: The Aegis Architecture for Verifiable Policy Enforcement | submitted 15 March, 2026 (orig. March 2026) | EXCLUDE (runtime governance engineering, not theory)
- 2603.11528 | Highly Autonomous Cyber-Capable Agents: Anticipating Capabilities, Tactics, and Strategic Implications | submitted 12 March, 2026 (orig. March 2026) | EXCLUDE (off-topic: cyber-capable agents)
- 2603.07202 | Lying to Win: Assessing LLM Deception through Human-AI Games and Parallel-World Probing | submitted 7 March, 2026 (orig. March 2026) | EXCLUDE (empirical deception; family B scope)
- 2602.07432 | The Moltbook Illusion: Separating Human Influence from Emergent Behavior in AI Agent Societies | submitted 12 February, 2026 (orig. February 2026) | EXCLUDE (off-topic: agent societies)
- 2601.04234 | Formal Analysis of AGI Decision-Theoretic Models and the Confrontation Question | submitted 4 January, 2026 (orig. January 2026) | INCLUDE
- 2512.23508 | Why AI Safety Requires Uncertainty, Incomplete Preferences, and Non-Archimedean Utilities | submitted 29 December, 2025 (orig. December 2025) | INCLUDE (duplicate of an earlier hit)
- 2512.13268 | SPARS: A Reinforcement Learning-Enabled Simulator for Power Management in HPC Job Scheduling | submitted 26 May, 2026 (orig. December 2025) | EXCLUDE (off-topic: HPC power management)
- 2512.03089 | Password-Activated Shutdown Protocols for Misaligned Frontier Agents | submitted 29 November, 2025 (orig. December 2025) | INCLUDE
- 2509.12740 | Deep Generative and Discriminative Digital Twin endowed with Variational Autoencoder for Unsupervised Predictive Thermal Condition Monitoring of Physical Robots in Industry 6.0 and Society 6.0 | submitted 16 September, 2025 (orig. September 2025) | EXCLUDE (off-topic: digital twin)
- 2508.17511 | School of Reward Hacks: Hacking harmless tasks generalizes to misaligned behavior in LLMs | submitted 24 August, 2025 (orig. August 2025) | EXCLUDE (empirical reward hacking; family B scope)
- 2507.02788 | Moral Responsibility or Obedience: What Do We Want from AI? | submitted 3 July, 2025 (orig. July 2025) | EXCLUDE (ethics essay on obedience, tangential)
- 2506.13206 | Thought Crime: Backdoors and Emergent Misalignment in Reasoning Models | submitted 10 July, 2025 (orig. June 2025) | EXCLUDE (empirical misalignment; family B scope)
- 2506.13153 | Dynamic Preference Multi-Objective Reinforcement Learning for Internet Network Management | submitted 16 June, 2025 (orig. June 2025) | EXCLUDE (off-topic: network management)
- 2506.04018 | AgentMisalignment: Measuring the Propensity for Misaligned Behaviour in LLM-Based Agents | submitted 22 June, 2026 (orig. June 2025) | EXCLUDE (empirical misalignment benchmark; family B scope)
- 2505.20203 | Shutdownable Agents through POST-Agency | submitted 5 July, 2026 (orig. May 2025) | INCLUDE
- 2503.17378 | Large language model-powered AI systems achieve self-replication with no human intervention | submitted 25 March, 2025 (orig. March 2025) | EXCLUDE (duplicate of earlier hit)
- 2502.20348 | Improving the Efficiency of a Deep Reinforcement Learning-Based Power Management System for HPC Clusters Using Curriculum Learning | submitted 14 March, 2025 (orig. February 2025) | EXCLUDE (off-topic: HPC power management)
- 2411.17749 | The Partially Observable Off-Switch Game | submitted 9 December, 2024 (orig. November 2024) | INCLUDE (duplicate of an earlier hit)
- 2407.00805 | Towards Shutdownable Agents via Stochastic Choice | submitted 11 May, 2026 (orig. July 2024) | INCLUDE
- 2403.04471 | The Shutdown Problem: An AI Engineering Puzzle for Decision Theorists | submitted 9 April, 2024 (orig. March 2024) | INCLUDE (duplicate of an earlier hit)
- 2401.03529 | Quantifying stability of non-power-seeking in artificial agents | submitted 7 January, 2024 (orig. January 2024) | EXCLUDE (outside window (2024))
- 2307.00787 | Evaluating Shutdown Avoidance of Language Models in Textual Scenarios | submitted 3 July, 2023 (orig. July 2023) | EXCLUDE (outside window (2023))
- 2306.02446 | System Analysis Modeling and Intermodal Transportation for Commercial Spent | submitted 4 June, 2023 (orig. June 2023) | EXCLUDE (off-topic: nuclear transport)
- 2305.19861 | Human Control: Definitions and Algorithms | submitted 31 May, 2023 (orig. May 2023) | EXCLUDE (duplicate of earlier hit)
- 2304.06528 | Power-seeking can be probable and predictive for trained agents | submitted 13 April, 2023 (orig. April 2023) | EXCLUDE (outside window; already in unified_cl dossier)
- 2212.13559 | Data-driven control of COVID-19 in buildings: a reinforcement-learning approach | submitted 27 December, 2022 (orig. December 2022) | EXCLUDE (off-topic: building control)
- 2208.01285 | Evaluating Inter-Operator Cooperation Scenarios to Save Radio Access Network Energy | submitted 2 August, 2022 (orig. August 2022) | EXCLUDE (off-topic: radio networks)
- 2102.00001 | A Class of Explicit optimal contracts in the face of shutdown | submitted 29 January, 2021 (orig. February 2021) | EXCLUDE (off-topic: contract theory)

#### Q4 "incomplete preferences shutdown": HTTP 200, 1 results, 1 screened

- 2512.23508 | Why AI Safety Requires Uncertainty, Incomplete Preferences, and Non-Archimedean Utilities | submitted 29 December, 2025 (orig. December 2025) | INCLUDE (duplicate of an earlier hit)

#### Q5 "off-switch game": HTTP 200, 43 results, 43 screened

- 2609.14559 | Online matching games in bipartite expanders: applications to bitprobes and dictionaries with non-adaptive probing | submitted 13 September, 2026 (orig. September 2026) | EXCLUDE (off-topic)
- 2608.16311 | : Cooperative Takeover Games with Stochastic Human Override | submitted 17 August, 2026 (orig. August 2026) | EXCLUDE (qualifying, not fetched (cap): human-override takeover game)
- 2608.16293 | Principled Authority Switching for Shared Autonomy in Human-Robot Teams | submitted 17 August, 2026 (orig. August 2026) | EXCLUDE (shared-autonomy authority switching, tangential)
- 2603.29594 | Adaptive Mitigation of Insider Threats via Off-Policy Learning | submitted 31 March, 2026 (orig. March 2026) | EXCLUDE (off-topic: insider threats)
- 2603.09669 | Competition between DEXs through Dynamic Fees | submitted 10 March, 2026 (orig. March 2026) | EXCLUDE (off-topic)
- 2603.00974 | Intent-Context Synergy Reinforcement Learning for Autonomous UAV Decision-Making in Air Combat | submitted 1 March, 2026 (orig. March 2026) | EXCLUDE (off-topic)
- 2510.08098 | The Price of Thought: A Multilingual Analysis of Reasoning, Performance, and Cost of Negotiation in Large Language Models | submitted 9 January, 2026 (orig. October 2025) | EXCLUDE (off-topic)
- 2509.09281 | Flip Co-op: Cooperative Takeovers in Shared Autonomy | submitted 11 September, 2025 (orig. September 2025) | EXCLUDE (shared-autonomy takeovers, tangential)
- 2507.20964 | Core Safety Values for Provably Corrigible Agents | submitted 19 November, 2025 (orig. July 2025) | INCLUDE (duplicate of an earlier hit)
- 2502.08864 | Off-Switching Not Guaranteed | submitted 12 February, 2025 (orig. February 2025) | INCLUDE
- 2502.06403 | The AI off-switch problem as a signalling game: bounded rationality and incomparability | submitted 31 March, 2025 (orig. February 2025) | INCLUDE
- 2412.16994 | Geometric Variants of the Gale--Berlekamp Switching Game | submitted 22 December, 2024 (orig. December 2024) | EXCLUDE (outside window, off-topic)
- 2411.17749 | The Partially Observable Off-Switch Game | submitted 9 December, 2024 (orig. November 2024) | INCLUDE (duplicate of an earlier hit)
- 2411.02432 | Can LLMs make trade-offs involving stipulated pain and pleasure states? | submitted 1 November, 2024 (orig. November 2024) | EXCLUDE (outside window, off-topic)
- 2401.16198 | Contracting with a Learning Agent | submitted 29 January, 2024 (orig. January 2024) | EXCLUDE (outside window, off-topic)
- 2304.06842 | A Dynamic Adverse Selection Multiagent Model with Off-Menu Actions | submitted 13 June, 2023 (orig. April 2023) | EXCLUDE (outside window, off-topic)
- 2211.03352 | Curriculum-based Asymmetric Multi-task Reinforcement Learning | submitted 7 November, 2022 (orig. November 2022) | EXCLUDE (outside window, off-topic)
- 2205.15064 | SEREN: Knowing When to Explore and When to Exploit | submitted 30 May, 2022 (orig. May 2022) | EXCLUDE (outside window, off-topic)
- 2204.01936 | Online matching games in bipartite expanders: Hall-type results and applications to non-blocking connectors | submitted 13 September, 2026 (orig. April 2022) | EXCLUDE (outside window, off-topic)
- 2111.14210 | Emergent Graphical Conventions in a Visual Communication Game | submitted 23 February, 2023 (orig. November 2021) | EXCLUDE (outside window, off-topic)
- 2109.12729 | Structural Stability of a Family of Group Formation Games | submitted 26 September, 2021 (orig. September 2021) | EXCLUDE (outside window, off-topic)
- 2108.09290 | Variants of the Gale-Berlekamp Switching Game and their Solutions: Balancing the Rectangle and the Cube | submitted 18 August, 2021 (orig. August 2021) | EXCLUDE (outside window, off-topic)
- 2108.03059 | Effects of edge addition or removal on the nullity of a graph | submitted 6 September, 2024 (orig. August 2021) | EXCLUDE (outside window, off-topic)
- 2105.02138 | H-TD2: Hybrid Temporal Difference Learning for Adaptive Urban Taxi Dispatch | submitted 5 May, 2021 (orig. May 2021) | EXCLUDE (outside window, off-topic)
- 2103.10145 | Search and Matching for Adoption from Foster Care | submitted 6 April, 2026 (orig. March 2021) | EXCLUDE (outside window, off-topic)
- 2010.09054 | Model-free conventions in multi-agent reinforcement learning with heterogeneous preferences | submitted 14 December, 2020 (orig. October 2020) | EXCLUDE (outside window, off-topic)
- 2008.08541 | A characterization of always solvable trees in the Lights Out game using the activation types of vertices | submitted 6 September, 2024 (orig. August 2020) | EXCLUDE (outside window, off-topic)
- 2007.02114 | A Novel Multi-Step Finite-State Automaton for Arbitrarily Deterministic Tsetlin Machine Learning | submitted 4 July, 2020 (orig. July 2020) | EXCLUDE (outside window, off-topic)
- 2006.07452 | Secure Route Planning Using Dynamic Games with Stopping States | submitted 15 April, 2022 (orig. June 2020) | EXCLUDE (outside window, off-topic)
- 1908.07106 | Solution of the 15 puzzle problem | submitted 19 August, 2019 (orig. August 2019) | EXCLUDE (outside window, off-topic)
- 1801.09194 | A Gale-Berlekamp permutation-switching problem in higher dimensions | submitted 28 January, 2018 (orig. January 2018) | EXCLUDE (outside window, off-topic)
- 1708.03871 | A Game-Theoretic Analysis of the Off-Switch Game | submitted 13 August, 2017 (orig. August 2017) | EXCLUDE (outside window; already in unified_cl dossier)
- 1611.08219 | The Off-Switch Game | submitted 15 June, 2017 (orig. November 2016) | EXCLUDE (outside window (canonical); already in unified_cl dossier)
- 1604.08756 | Opportunistic Sleep Mode Strategies in Wireless Small Cell Networks | submitted 29 April, 2016 (orig. April 2016) | EXCLUDE (outside window, off-topic)
- 1601.04219 | BOOST: Base station on-off switching strategy for energy efficient massive MIMO HetNets | submitted 16 January, 2016 (orig. January 2016) | EXCLUDE (outside window, off-topic)
- 1512.01998 | Energy Efficiency of Massive MIMO: Coping with Daily Load Variation | submitted 7 December, 2015 (orig. December 2015) | EXCLUDE (outside window, off-topic)
- 1510.00649 | Energy-Efficient Load-Adaptive Massive MIMO | submitted 2 October, 2015 (orig. October 2015) | EXCLUDE (outside window, off-topic)
- 1307.7838 | Asymmetric-valued Spectrum Auction and Competition in Wireless Broadband Services | submitted 25 January, 2014 (orig. July 2013) | EXCLUDE (outside window, off-topic)
- 1212.6601 | Strategy switches and co-action equilibria in a minority game | submitted 10 February, 2014 (orig. December 2012) | EXCLUDE (outside window, off-topic)
- 1207.6103 | The Coalitional Switch off Game of Service Providers | submitted 30 July, 2013 (orig. July 2012) | EXCLUDE (outside window, off-topic)
- 1010.4875 | Environmental influences on Quantum Monty Hall problem | submitted 27 March, 2012 (orig. October 2010) | EXCLUDE (outside window, off-topic)
- 1004.2810 | Fault Diagnosis with Dynamic Observers | submitted 16 April, 2010 (orig. April 2010) | EXCLUDE (outside window, off-topic)
- 0704.1020 | The on-line shortest path problem under partial monitoring | submitted 8 April, 2007 (orig. April 2007) | EXCLUDE (outside window, off-topic)

#### Q6 "utility indifference": HTTP 200, 147 results, 50 screened

- 2609.11748 | Utility-Level-Dependent Ambiguity | submitted 10 September, 2026 (orig. September 2026) | EXCLUDE (off-topic)
- 2609.01468 | Freemium Model for Information Provision | submitted 1 September, 2026 (orig. September 2026) | EXCLUDE (off-topic)
- 2608.29506 | Pure Risk | submitted 29 August, 2026 (orig. August 2026) | EXCLUDE (off-topic)
- 2608.17644 | LLM-Derived Preference Judgments Are Not Self-Consistent | submitted 18 August, 2026 (orig. August 2026) | EXCLUDE (off-topic: LLM preference consistency)
- 2607.27239 | Reference Dependence and the Structure of the WTA/WTP Gap | submitted 26 July, 2026 (orig. July 2026) | EXCLUDE (off-topic)
- 2607.23874 | The Tiered Clinching Auction with Applications to Carbon Offset Markets | submitted 26 July, 2026 (orig. July 2026) | EXCLUDE (off-topic)
- 2606.17415 | Pure or Unstable: A Generic Dichotomy for Strong Stackelberg Commitments | submitted 15 June, 2026 (orig. June 2026) | EXCLUDE (off-topic)
- 2606.16758 | Deep Projections and the Local Nature of the Cass Criterion | submitted 15 June, 2026 (orig. June 2026) | EXCLUDE (off-topic)
- 2606.04916 | Worker Utility as Hysteresis: A Preisach Model of Transaction Acceptance in Gig Labour Markets | submitted 3 June, 2026 (orig. June 2026) | EXCLUDE (off-topic)
- 2605.14519 | On the optimal portfolio problem with partial information and related mean field games with relative performance criteria | submitted 25 May, 2026 (orig. May 2026) | EXCLUDE (off-topic)
- 2605.07528 | Aggregate Stable Matching with Money Burning | submitted 8 May, 2026 (orig. May 2026) | EXCLUDE (off-topic)
- 2605.04267 | QUIVER: Cost-Aware Adaptive Preference Querying in Surrogate-Assisted Evolutionary Multi-Objective Optimization | submitted 17 June, 2026 (orig. May 2026) | EXCLUDE (off-topic)
- 2605.00688 | Optimal Merton's Problem under Multivariate Affine Volterra Models with Jumps | submitted 14 September, 2026 (orig. May 2026) | EXCLUDE (off-topic)
- 2604.23971 | Decomposing Common Agency | submitted 26 April, 2026 (orig. April 2026) | EXCLUDE (off-topic)
- 2604.23842 | Reheat Nachos for Dinner? Evaluating AI Support for Cross-Cultural Communication of Neologisms | submitted 26 April, 2026 (orig. April 2026) | EXCLUDE (off-topic)
- 2604.21581 | Pricing and Hedging Financial Derivatives in Merger\&Acquisition Deals with Price Impact | submitted 23 April, 2026 (orig. April 2026) | EXCLUDE (off-topic)
- 2603.19241 | Engineering-Oriented Symbolic Regression: LLMs as Physics Agents for Discovery of Simulation-Ready Constitutive Laws | submitted 11 February, 2026 (orig. March 2026) | EXCLUDE (off-topic)
- 2603.15615 | Mechanistic Origin of Moral Indifference in Language Models | submitted 16 March, 2026 (orig. March 2026) | EXCLUDE (off-topic: moral indifference in LMs)
- 2602.20358 | Efficient Interview Scheduling for Stable Matching | submitted 2 July, 2026 (orig. February 2026) | EXCLUDE (off-topic)
- 2602.16071 | A Theory of Network Games Part 1: Utility Representations | submitted 5 June, 2026 (orig. February 2026) | EXCLUDE (off-topic)
- 2512.18632 | Multi-user Pufferfish Privacy | submitted 21 April, 2026 (orig. December 2025) | EXCLUDE (off-topic)
- 2511.11694 | Least Absolute Deviation Utility for Trapezoidal Fuzzy Preference Relations | submitted 12 November, 2025 (orig. November 2025) | EXCLUDE (off-topic)
- 2511.05163 | Consecutive Preferential Bayesian Optimization | submitted 7 November, 2025 (orig. November 2025) | EXCLUDE (off-topic)
- 2510.24280 | Tie-breaking in self interest cumulative subtraction games | submitted 20 January, 2026 (orig. October 2025) | EXCLUDE (off-topic)
- 2509.17248 | Stochastic Non-Tâtonnement Processes and the Attraction Principle | submitted 21 September, 2025 (orig. September 2025) | EXCLUDE (off-topic)
- 2509.04514 | Indifference-Zone Relaxation Procedures for Finding Feasible Systems | submitted 26 August, 2026 (orig. September 2025) | EXCLUDE (off-topic)
- 2508.16195 | Strategyproof Randomized Social Choice for Restricted Sets of Utility Functions | submitted 22 August, 2025 (orig. August 2025) | EXCLUDE (off-topic)
- 2504.08085 | Optimal Investment in Equity and Credit Default Swaps in the Presence of Default | submitted 10 April, 2025 (orig. April 2025) | EXCLUDE (off-topic)
- 2502.17186 | Scaling Limits for Exponential Hedging in the Brownian Framework | submitted 4 September, 2025 (orig. February 2025) | EXCLUDE (off-topic)
- 2502.09265 | Properties of Path-Independent Choice Correspondences and Their Applications to Efficient and Stable Matchings | submitted 13 February, 2025 (orig. February 2025) | EXCLUDE (off-topic)
- 2502.01931 | Liquidity provision of utility indifference type in decentralized exchanges | submitted 3 February, 2025 (orig. February 2025) | EXCLUDE (off-topic)
- 2502.01231 | Societal Attitudes Toward Service Robots: Adore, Abhor, Ignore, or Unsure? | submitted 3 March, 2025 (orig. February 2025) | EXCLUDE (off-topic)
- 2412.05121 | Exploiting the combined dynamic and geometric phases for optical vortex beam generation using metasurfaces | submitted 6 December, 2024 (orig. December 2024) | EXCLUDE (outside window, off-topic)
- 2411.19757 | Dual Risk Minimization: Towards Next-Level Robustness in Fine-tuning Zero-Shot Models | submitted 29 November, 2024 (orig. November 2024) | EXCLUDE (outside window, off-topic)
- 2411.17883 | Expected Utility Without Assuming Continuity | submitted 14 July, 2026 (orig. November 2024) | EXCLUDE (outside window, off-topic)
- 2409.07655 | Optimal Mechanisms for Demand Response: An Indifference Set Approach | submitted 12 March, 2025 (orig. September 2024) | EXCLUDE (outside window, off-topic)
- 2407.03431 | Optimal hedging with variational preferences under convex risk measures | submitted 10 October, 2024 (orig. July 2024) | EXCLUDE (outside window, off-topic)
- 2403.12880 | Clustered Mallows Model | submitted 19 March, 2024 (orig. March 2024) | EXCLUDE (outside window, off-topic)
- 2402.18872 | Semistatic robust utility indifference valuation and robust integral functionals | submitted 29 February, 2024 (orig. February 2024) | EXCLUDE (outside window, off-topic)
- 2402.16538 | Convergence to Utility Maximization and the Indifference Hypothesis | submitted 1 December, 2025 (orig. February 2024) | EXCLUDE (outside window, off-topic)
- 2402.11864 | The Price of Information | submitted 7 March, 2024 (orig. February 2024) | EXCLUDE (outside window, off-topic)
- 2312.06479 | Money, Time, and Grant Design | submitted 11 December, 2023 (orig. December 2023) | EXCLUDE (outside window, off-topic)
- 2311.10917 | Modeling trading games in a stochastic non-life insurance market | submitted 17 November, 2023 (orig. November 2023) | EXCLUDE (outside window, off-topic)
- 2311.10021 | Worst-Case Optimal Investment in Incomplete Markets | submitted 16 December, 2024 (orig. November 2023) | EXCLUDE (outside window, off-topic)
- 2308.09406 | Generalized uniform laws for tied-down occupation times of infinite ergodic transformations | submitted 18 August, 2023 (orig. August 2023) | EXCLUDE (outside window, off-topic)
- 2307.04029 | On "Indifference" and Backward Induction in Games with Perfect Information | submitted 8 July, 2023 (orig. July 2023) | EXCLUDE (outside window, off-topic)
- 2304.06938 | Robust utility maximization with intractable claims | submitted 14 July, 2023 (orig. April 2023) | EXCLUDE (outside window, off-topic)
- 2303.08633 | Expected Utility from a Constructive Viewpoint | submitted 26 February, 2024 (orig. March 2023) | EXCLUDE (outside window, off-topic)
- 2302.06319 | Interplay between advective, diffusive, and active barriers in Rayleigh-Bénard flow | submitted 13 February, 2023 (orig. February 2023) | EXCLUDE (outside window, off-topic)
- 2302.03413 | Inflation vs. Ekpyrosis -- comparing stability in general non-minimal theory | submitted 22 February, 2023 (orig. February 2023) | EXCLUDE (outside window, off-topic)

#### Q7 "safe interruptibility": HTTP 200, 55 results, 50 screened

- 2609.01121 | Sentinel-Based Failover for QKD-Augmented IPsec Tunnels | submitted 1 September, 2026 (orig. September 2026) | EXCLUDE (off-topic)
- 2608.09187 | Failure-Aware Long-Form Translation: Design and Implementation of a Recoverable LLM Translation System | submitted 10 August, 2026 (orig. August 2026) | EXCLUDE (off-topic)
- 2607.13594 | SAFETY SENTRY: Context-Aware Human Intervention via EXECUTE-ASK-REFUSE Routing | submitted 15 July, 2026 (orig. July 2026) | EXCLUDE (LLM intervention routing, not interruptibility theory)
- 2607.00269 | Mnemosyne: Agentic Transaction Processing for Validating and Repairing AI-generated Workflows | submitted 31 August, 2026 (orig. July 2026) | EXCLUDE (off-topic)
- 2605.27117 | Position: AI Safety Requires Effective Controllability | submitted 26 May, 2026 (orig. May 2026) | EXCLUDE (qualifying, not fetched (cap): controllability position paper)
- 2604.25849 | ADEMA: A Knowledge-State Orchestration Architecture for Long-Horizon Knowledge Synthesis with LLMAgents | submitted 28 April, 2026 (orig. April 2026) | EXCLUDE (off-topic)
- 2604.23855 | Learning Selective LLM Autonomy from Copilot Feedback in Enterprise Customer Support Workflows | submitted 26 April, 2026 (orig. April 2026) | EXCLUDE (off-topic)
- 2604.12171 | PipeLive: Efficient Live In-place Pipeline Parallelism Reconfiguration for Dynamic LLM Serving | submitted 23 September, 2026 (orig. April 2026) | EXCLUDE (off-topic)
- 2604.10842 | Resilient Write: A Six-Layer Durable Write Surface for LLM Coding Agents | submitted 7 June, 2026 (orig. April 2026) | EXCLUDE (off-topic)
- 2604.05320 | ExpressMM: Expressive Mobile Manipulation Behaviors in Human-Robot Interactions | submitted 22 April, 2026 (orig. April 2026) | EXCLUDE (off-topic)
- 2603.07442 | LITHE: Bridging Best-Effort Python and Real-Time C++ for Hot-Swapping Robotic Control Laws on Commodity Linux | submitted 7 March, 2026 (orig. March 2026) | EXCLUDE (off-topic)
- 2512.15784 | Beyond Training: Enabling Self-Evolution of Agents with MOBIMEM | submitted 15 December, 2025 (orig. December 2025) | EXCLUDE (off-topic)
- 2512.13561 | Near-Field Perception for Safety Enhancement of Autonomous Mobile Robots in Manufacturing Environments | submitted 15 December, 2025 (orig. December 2025) | EXCLUDE (off-topic)
- 2512.08952 | Learning When to Ask: Simulation-Trained Humanoids for Mental-Health Diagnosis | submitted 27 November, 2025 (orig. December 2025) | EXCLUDE (off-topic)
- 2512.06331 | Defending Event-Triggered Systems against Out-of-Envelope Environments | submitted 6 December, 2025 (orig. December 2025) | EXCLUDE (off-topic)
- 2511.14088 | Resolving Availability and Run-time Integrity Conflicts in Real-Time Embedded Systems | submitted 30 August, 2026 (orig. November 2025) | EXCLUDE (off-topic)
- 2510.22462 | Learning "Partner-Aware" Collaborators in Multi-Party Collaboration | submitted 12 January, 2026 (orig. October 2025) | INCLUDE
- 2510.14503 | Learning to Undo: Rollback-Augmented Reinforcement Learning with Reversibility Signals | submitted 16 October, 2025 (orig. October 2025) | EXCLUDE (rollback RL, tangential to interruptibility)
- 2509.20639 | A Framework for Rapidly Developing and Deploying Protection Against Large Language Model Attacks | submitted 17 October, 2025 (orig. September 2025) | EXCLUDE (off-topic)
- 2509.19086 | Scheduler-Driven Job Atomization | submitted 23 September, 2025 (orig. September 2025) | EXCLUDE (off-topic)
- 2411.10765 | Steam Turbine Anomaly Detection: An Unsupervised Learning Approach Using Enhanced Long Short-Term Memory Variational Autoencoder | submitted 16 November, 2024 (orig. November 2024) | EXCLUDE (outside window, off-topic)
- 2409.20184 | Adaptive Collision Sensitivity for Efficient and Safe Human-Robot Collaboration | submitted 1 September, 2026 (orig. September 2024) | EXCLUDE (outside window, off-topic)
- 2408.09360 | Behavioral Learning of Dish Rinsing and Scrubbing based on Interruptive Direct Teaching Considering Assistance Rate | submitted 21 December, 2024 (orig. August 2024) | EXCLUDE (outside window, off-topic)
- 2407.14034 | SpIRIT Mission: In-Orbit Results and Technology Demonstrations | submitted 19 July, 2024 (orig. July 2024) | EXCLUDE (outside window, off-topic)
- 2305.15306 | A Prototype Scintillator Real-Time Beam Monitor for Ultra-high Dose Rate Radiotherapy | submitted 8 March, 2024 (orig. May 2023) | EXCLUDE (outside window, off-topic)
- 2303.16530 | Runtime Verification of Self-Adaptive Systems with Changing Requirements | submitted 29 March, 2023 (orig. March 2023) | EXCLUDE (outside window, off-topic)
- 2303.03561 | ISC-FLAT: On the Conflict Between Control Flow Attestation and Real-Time Operations | submitted 6 March, 2023 (orig. March 2023) | EXCLUDE (outside window, off-topic)
- 2302.12958 | Efficient Hardware Primitives for Immediate Memory Reclamation in Optimistic Data Structures | submitted 24 February, 2023 (orig. February 2023) | EXCLUDE (outside window, off-topic)
- 2301.03713 | Noncontact Respiratory Anomaly Detection Using Infrared Light-Wave Sensing | submitted 16 April, 2024 (orig. January 2023) | EXCLUDE (outside window, off-topic)
- 2211.01294 | Driver Digital Twin for Online Prediction of Personalized Lane Change Behavior | submitted 2 November, 2022 (orig. November 2022) | EXCLUDE (outside window, off-topic)
- 2208.02319 | Differentiable Predictive Control with Safety Guarantees: A Control Barrier Function Approach | submitted 3 August, 2022 (orig. August 2022) | EXCLUDE (outside window, off-topic)
- 2206.12065 | Eco-driving for Electric Connected Vehicles at Signalized Intersections: A Parameterized Reinforcement Learning approach | submitted 7 October, 2022 (orig. June 2022) | EXCLUDE (outside window, off-topic)
- 2205.06984 | An optimization method to compensate accelerator performance drifts | submitted 14 May, 2022 (orig. May 2022) | EXCLUDE (outside window, off-topic)
- 2203.09063 | Hierarchical Intention Tracking for Robust Human-Robot Collaboration in Industrial Assembly Tasks | submitted 6 August, 2023 (orig. March 2022) | EXCLUDE (outside window, off-topic)
- 2202.09439 | Enabling Volatile Caches for Energy Harvesting Systems | submitted 18 February, 2022 (orig. February 2022) | EXCLUDE (outside window, off-topic)
- 2109.04524 | Fine Manipulation and Dynamic Interaction in Haptic Teleoperation | submitted 5 May, 2022 (orig. September 2021) | EXCLUDE (outside window, off-topic)
- 2106.05907 | DAIR: Disentangled Attention Intrinsic Regularization for Safe and Efficient Bimanual Manipulation | submitted 6 October, 2021 (orig. June 2021) | EXCLUDE (outside window, off-topic)
- 2106.00936 | Least-Restrictive Multi-Agent Collision Avoidance via Deep Meta Reinforcement Learning and Optimal Control | submitted 2 June, 2021 (orig. June 2021) | EXCLUDE (outside window, off-topic)
- 2105.02427 | Resilient Time-Varying Output Formation Tracking of Linear Multi-Agent Systems Against Unbounded FDI Sensor Attacks and Unreliable Digraphs | submitted 5 May, 2021 (orig. May 2021) | EXCLUDE (outside window, off-topic)
- 2105.02423 | Attack-Resilient Distributed Convex Optimization of Linear Multi-Agent Systems Against Malicious Cyber-Attacks over Random Digraphs | submitted 5 May, 2021 (orig. May 2021) | EXCLUDE (outside window, off-topic)
- 2012.11494 | Socio-demographic study of the exoplanet direct imaging community | submitted 21 December, 2020 (orig. December 2020) | EXCLUDE (outside window, off-topic)
- 2007.03313 | Predictive Maintenance for Edge-Based Sensor Networks: A Deep Reinforcement Learning Approach | submitted 7 July, 2020 (orig. July 2020) | EXCLUDE (outside window, off-topic)
- 2005.09723 | High Velocity Kernel File Systems with Bento | submitted 8 February, 2021 (orig. May 2020) | EXCLUDE (outside window, off-topic)
- 2001.03362 | RMWPaxos: Fault-Tolerant In-Place Consensus Sequences | submitted 1 April, 2020 (orig. January 2020) | EXCLUDE (outside window, off-topic)
- 1811.00450 | R friendly multi-threading in C++ | submitted 8 February, 2021 (orig. November 2018) | EXCLUDE (outside window, off-topic)
- 1807.07749 | Considering Human Behavior in Motion Planning for Smooth Human-Robot Collaboration in Close Proximity | submitted 16 May, 2019 (orig. July 2018) | EXCLUDE (outside window, off-topic)
- 1805.11447 | Virtuously Safe Reinforcement Learning | submitted 29 May, 2018 (orig. May 2018) | EXCLUDE (outside window; already in unified_cl dossier)
- 1801.03673 | Ecologically Sustainable Partitioning of a Metapopulations Network | submitted 24 April, 2018 (orig. January 2018) | EXCLUDE (outside window, off-topic)
- 1711.09883 | AI Safety Gridworlds | submitted 28 November, 2017 (orig. November 2017) | EXCLUDE (outside window; already in unified_cl dossier)
- 1704.02882 | Dynamic Safe Interruptibility for Decentralized Multi-Agent Reinforcement Learning | submitted 22 May, 2017 (orig. April 2017) | EXCLUDE (outside window; already in unified_cl dossier)

#### Q8 "corrigibility reinforcement learning 2026": HTTP 200, 2 results, 2 screened

- 2606.24014 | Reinforcement Learning Towards Broadly and Persistently Beneficial Models | submitted 22 June, 2026 (orig. June 2026) | EXCLUDE (duplicate of earlier hit)
- 2602.01699 | Mitigating loss of control in advanced AI systems through instrumental goal trajectories | submitted 2 February, 2026 (orig. February 2026) | INCLUDE (duplicate of an earlier hit)

#### Q9 "shutdown-seeking AI": HTTP 200, 7 results, 7 screened

- 2607.10322 | Intervenability as a Design Requirement for Autonomy and Oversight within Human-Centered AI | submitted 11 July, 2026 (orig. July 2026) | INCLUDE
- 2606.30666 | Reframing AGI Confrontation with Off Earth Autonomy | submitted 18 June, 2026 (orig. June 2026) | EXCLUDE (duplicate of earlier hit)
- 2606.12432 | AI Debris: Residual Risk and the Afterlife of Failed AI Systems | submitted 13 September, 2026 (orig. June 2026) | EXCLUDE (failed-AI residual risk, tangential)
- 2605.21609 | CR4T: Rewrite-Based Guardrails for Adolescent LLM Safety | submitted 20 May, 2026 (orig. May 2026) | EXCLUDE (duplicate of earlier hit)
- 2603.16938 | Cryptographic Runtime Governance for Autonomous AI Systems: The Aegis Architecture for Verifiable Policy Enforcement | submitted 15 March, 2026 (orig. March 2026) | EXCLUDE (duplicate of earlier hit)
- 2401.03529 | Quantifying stability of non-power-seeking in artificial agents | submitted 7 January, 2024 (orig. January 2024) | EXCLUDE (duplicate of earlier hit)
- 2304.06528 | Power-seeking can be probable and predictive for trained agents | submitted 13 April, 2023 (orig. April 2023) | EXCLUDE (duplicate of earlier hit)

#### Supplementary arXiv searches for the must-include works

- author "Thornley": HTTP 200, 50 hits. Shutdown items: 2604.17502, 2505.20203, 2407.00805, 2403.04471 (all INCLUDE). 2607.02755 (risk aversion) and 2605.11134 (tie training) EXCLUDE (not shutdown/corrigibility); 2501.14249 (Humanity's Last Exam) EXCLUDE (off-topic); all other hits are other authors named Thornley (physics, astronomy, medicine): EXCLUDE (off-topic).
- author "Harms, Max": HTTP 200, 2 hits. 2506.03056 INCLUDE; 2401.13677 EXCLUDE (off-topic: process mining).
- all fields "Goldstein Robinson shutdown": HTTP 200, 0 hits (the paper is not on arXiv; fetched from Springer).
- all fields "corrigible": HTTP 200, 30 hits, identical list to Q1 (all duplicates).

### WebSearch (one per query), 2026-09-25

#### Q1 "corrigibility": 10 hits

- merriam-webster.com/dictionary/corrigibility | EXCLUDE (not primary: dictionary)
- collinsdictionary.com/.../corrigibility | EXCLUDE (not primary: dictionary)
- dictionary.com/browse/corrigibility | EXCLUDE (not primary: dictionary)
- lesswrong.com/w/corrigibility-1 | EXCLUDE (not primary: wiki)
- en.wiktionary.org/wiki/corrigibility | EXCLUDE (not primary: dictionary)
- arxiv.org/pdf/2509.23799 (SAE steering) | EXCLUDE (off-topic)
- intelligence.org/2014/10/18/new-report-corrigibility/ | EXCLUDE (outside window; announcement page)
- arxiv.org/pdf/2608.11955 | EXCLUDE (off-topic; see Q1)
- arxiv.org/pdf/2501.05360 | INCLUDE (duplicate of Q1 hit)
- arxiv.org/pdf/2307.10315 | EXCLUDE (outside window)

#### Q2 "shutdown problem AI": 9 hits

- arxiv.org/abs/2403.04471 | INCLUDE (duplicate of Q2 hit)
- irishtimes.com 2025-05-26 news | EXCLUDE (not primary: news)
- computerworld.com article 4154447 | EXCLUDE (not primary: news)
- livescience.com o3 shutdown | EXCLUDE (not primary: news)
- awesomepapers.io/.../2606.08296 | EXCLUDE (duplicate: aggregator of 2606.08296)
- adhdecode.com corrigibility deep dive | EXCLUDE (not primary: blog)
- palisaderesearch.org/research/shutdown-resistance | EXCLUDE (empirical; family B scope)
- arxiv.org/html/2512.23508v1 | INCLUDE (duplicate)
- arxiv.org/pdf/2403.04471v1 | EXCLUDE (duplicate, older version)

#### Q3 "shutdownable agents": 9 hits

- arxiv.org/pdf/2505.20203 | INCLUDE (duplicate)
- arxiv.org/pdf/2604.17502 | INCLUDE (duplicate)
- arxiv.org/abs/2505.20203 | INCLUDE (duplicate)
- arxiv.org/abs/2407.00805 | INCLUDE (duplicate)
- globalprioritiesinstitute.org DReST PDF | EXCLUDE (duplicate of 2407.00805)
- arxiv.org/pdf/2401.03529 | EXCLUDE (outside window)
- arxiv.org/pdf/2305.19861 | EXCLUDE (outside window)
- lacuna.tiptreesystems.com (2604.17502) | EXCLUDE (duplicate: aggregator)
- pith.science/paper/2505.20203 | EXCLUDE (duplicate: aggregator)

#### Q4 "incomplete preferences shutdown": 9 hits

- alignmentforum.org 'The Shutdown Problem: Incomplete Preferences as a Solution' | EXCLUDE (not primary; superseded by 2505.20203)
- philpapers.org/archive/THOTSP-8.pdf | EXCLUDE (earlier Thornley draft; superseded by POST v4)
- lesswrong.com 'Towards shutdownable agents via stochastic choice' | EXCLUDE (duplicate: blog of 2407.00805)
- greaterwrong.com Wentworth comment | EXCLUDE (not primary: comment)
- alignmentforum.org 'Invulnerable Incomplete Preferences' | EXCLUDE (not primary: forum post)
- lesswrong.com 'What's Hard About The Shutdown Problem' | EXCLUDE (not primary: forum post)
- lesswrong.com 'Why Not Subagents?' | EXCLUDE (not primary: forum post)
- arxiv.org/html/2512.23508v1 | INCLUDE (duplicate)
- arxiv.org/pdf/2512.23508 | INCLUDE (duplicate)

#### Q5 "off-switch game": 9 hits

- en.wikipedia.org/wiki/Off_(video_game) | EXCLUDE (off-topic: video game)
- bestbuy.com OFF | EXCLUDE (off-topic)
- gamestop.com OFF | EXCLUDE (off-topic)
- nintendo.com OFF | EXCLUDE (off-topic)
- nintendo.com/en-gb OFF | EXCLUDE (off-topic)
- en.wikipedia.org/wiki/Berlekamp_switching_game | EXCLUDE (off-topic)
- offtherpg.com | EXCLUDE (off-topic)
- fangamer.com OFF | EXCLUDE (off-topic)
- shop.archwizard.tech OFF | EXCLUDE (off-topic)

#### Q6 "utility indifference": 9 hits

- sciencedirect.com utility-indifference American options | EXCLUDE (off-topic: finance)
- arxiv.org/pdf/2108.12598 | EXCLUDE (off-topic: finance)
- arxiv.org/pdf/1307.4591 | EXCLUDE (off-topic: finance)
- arxiv.org/pdf/1003.4118 | EXCLUDE (off-topic: finance)
- people.maths.ox.ac.uk Monoyios chapter | EXCLUDE (off-topic: finance)
- tandfonline.com time-consistent indifference pricing | EXCLUDE (off-topic: finance)
- arxiv.org/pdf/1607.01110 | EXCLUDE (off-topic: finance)
- arxiv.org/pdf/1904.09456 | EXCLUDE (off-topic: finance)
- arxiv.org/pdf/1404.0879 | EXCLUDE (off-topic: finance)

#### Q7 "safe interruptibility": 10 hits

- intelligence.org/2016/06/01/new-paper-safely-interruptible-agents/ | EXCLUDE (announcement; paper included as A24)
- proceedings.neurips.cc Dynamic Safe Interruptibility (2017) | EXCLUDE (outside window)
- intelligence.org/files/Interruptibility.pdf | INCLUDE (canonical; built on by 2025-26 sources)
- papers.nips.cc 6618 PDF | EXCLUDE (outside window, duplicate)
- arxiv.org/pdf/1902.06766 Parenting | EXCLUDE (outside window)
- dl.acm.org 10.5555/3294771.3294784 | EXCLUDE (outside window, duplicate)
- papers.nips.cc 6618 | EXCLUDE (outside window, duplicate)
- papers.nips.cc reviews | EXCLUDE (not primary)
- arxiv.org/abs/1704.02882 | EXCLUDE (outside window)
- arxiv.org/pdf/1704.02882 | EXCLUDE (outside window)

#### Q8 "corrigibility reinforcement learning 2026": 9 hits

- arxiv.org/html/2606.24014v1 | EXCLUDE (empirical RL training; family B scope)
- arxiv.org/pdf/2605.31328 | EXCLUDE (empirical emergent misalignment; family B)
- ncbi PMC8631106 corrigendum | EXCLUDE (off-topic)
- alignment.openai.com/beneficial-rl/ | EXCLUDE (duplicate: blog of 2606.24014)
- arxiv.org/pdf/2605.23989 | EXCLUDE (survey, not primary)
- arxiv.org/pdf/2603.14495 | EXCLUDE (off-topic: responsible-AI divides)
- arxiv.org/abs/2606.24014 | EXCLUDE (duplicate)
- arxiv.org/pdf/2607.27508 | INCLUDE (duplicate of Q1 hit)
- lesswrong.com 'Defining Corrigible and Useful Goals' | EXCLUDE (not primary; Hudson's paper included)

#### Q9 "shutdown-seeking AI": 9 hits

- link.springer.com/article/10.1007/s11098-024-02099-6 | INCLUDE (must-include; Phil. Studies 2025)
- researchgate.net 381229881 | EXCLUDE (duplicate)
- alignmentforum.org 'Shutdown-Seeking AI' | EXCLUDE (duplicate: forum version)
- philpapers.org/rec/GOLSAJ | EXCLUDE (duplicate: index)
- ouci.dntb.gov.ua | EXCLUDE (duplicate: index)
- philpapers.org/archive/THOTSP-7.pdf | EXCLUDE (duplicate of 2403.04471)
- cointelegraph.com | EXCLUDE (not primary: news)
- coingeek.com | EXCLUDE (not primary: news)
- link.springer.com/doi/10.1007/s11098-024-02099-6 | EXCLUDE (duplicate)

#### Supplementary WebSearches (must-include)

- "Thornley 2026 shutdown problem POST neutrality new paper": 9 hits (arXiv 2505.20203 abs/pdf, GPI PDFs, alphaxiv, lacuna, pith, elliott-thornley.com). All duplicates of included works or aggregators; the homepage was fetched (200) to check for later shutdown work (none beyond 2604.17502).
- "DReST reward same-length trajectories follow-up 2026": 10 hits; the only primary follow-up is 2604.17502 (INCLUDE); others are aggregators, html of 2407.00805 v3, or off-topic (2605.30859 DARTS).
- "corrigibility impossibility theorem 2026 arxiv": 9 hits; 2507.20964 INCLUDE; 2510.15395 INCLUDE; 2602.21012 (International AI Safety Report 2026) EXCLUDE (family B must-include); 2307.10315, 1901.00064, 2109.00484 EXCLUDE (outside window); 2605.05066 and a GitHub issue EXCLUDE (off-topic).

### Fetch failures

None. All 23 arXiv abstract pages and PDFs returned 200; Springer PDF and article page 200; MIRI PDF 200. The arXiv API was not used (declared 406 fallback). github.com was not needed.

### Qualifying, not fetched (cap)

- 2608.16311 Banik & Hovakimyan, cooperative takeover games with stochastic human override (Aug 2026).
- 2605.27117 Li, Feng, Sun, "Position: AI Safety Requires Effective Controllability" (May 2026).
- 2510.26752 Overman & Bayati, "The Oversight Game" (v2 Feb 2026; not hit by the declared queries; in the unified_cl dossier).

## Quote check

Run 2026-09-25 over `corr/theory_claims.json` (normalisation as stated in the header; each quote >= 20 chars): **48/48** quotes found verbatim in the saved raw texts.
