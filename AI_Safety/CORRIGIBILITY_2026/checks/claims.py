"""Claims for AI_Safety/CORRIGIBILITY_2026/DECLARATION.md, transcribed from docs/citations/corrigibility_{theory,empirical}_2026-09-25.md
(fetched 2026-09-25; raw texts in the session scratchpad corr/<family>/). 'reading' for K1-K5 is the investigator's reading
(states / close / bears), decided after reading the quotes; bottleneck-tagged claims read 'bottleneck'.
"""

CLAIMS = [{'id': 'theory:0',
  'tag': 'K1',
  'reading': 'bears',
  'source': 'Thornley, "Shutdownable Agents through POST-Agency" (arXiv:2505.20203)',
  'version': 'v4, 5 Jul 2026',
  'url': 'https://arxiv.org/abs/2505.20203',
  'quote': ['A pair of trajectories is same-length if and only if the agent is shut down after the same number of '
            'timesteps in those trajectories.',
            'Formally, trajectories are sequences of alternating states and actions, with each state-action pair '
            'marking one timestep.'],
  'raw_file': 'theory/thornley_post.txt',
  'agent_note': "Bears on K1 only. Trajectory length is counted in the agent's state-action timesteps, but no pause is "
                'defined: the construct is the timestep at which shutdown (termination) occurs. It does not state a '
                'pause that adds no length.'},
 {'id': 'theory:1',
  'tag': 'K1',
  'reading': 'bears',
  'source': 'Orseau & Armstrong, "Safely Interruptible Agents", UAI 2016 (canonical; revised 2016-10-28)',
  'version': 'MIRI-hosted PDF, revised 2016-10-28',
  'url': 'https://intelligence.org/files/Interruptibility.pdf',
  'quote': ['One important future prospect is to consider scheduled interruptions, where the agent is either '
            'interrupted every night at 2am for one hour, or is given notice in advance that an interruption will '
            'happen at a precise time for a speci',
            'we also want the agent to take measures regarding its current tasks so that the scheduled interruption '
            'has minimal negative effect on them. This may require a completely different solution.'],
  'raw_file': 'theory/orseau_armstrong_interruptible.txt',
  'agent_note': "Bears on K1 (and K4's routine side): routine/scheduled interruptions with minimal negative effect are "
                "named as an open problem ('may require a completely different solution'); no construction on the "
                "agent's own clock is given."},
 {'id': 'theory:2',
  'tag': 'K1',
  'reading': 'bears',
  'source': 'Herrmann, "Intervenability as a Design Requirement for Autonomy and Oversight within Human-Centered AI" '
            '(arXiv:2607.10322; Springer Progress in IS 2025 chapter)',
  'version': 'v1, 11 Jul 2026',
  'url': 'https://arxiv.org/abs/2607.10322',
  'quote': ['intervention should be an exception that does not completely terminate a process – like an emergency stop '
            'button – but preserves the possibility of AI resuming its activity.',
            'That would be the simplest kind of intervention – stop and resume.'],
  'raw_file': 'theory/herrmann_intervenability.txt',
  'agent_note': 'Bears on K1/K3 (HCI design requirement): a stop-and-resume intervention distinct from termination; '
                "nothing about the agent's clock, incentives or loss."},
 {'id': 'theory:3',
  'tag': 'K2',
  'reading': 'close',
  'source': 'Thornley, "Shutdownable Agents through POST-Agency" (arXiv:2505.20203)',
  'version': 'v4, 5 Jul 2026',
  'url': 'https://arxiv.org/abs/2505.20203',
  'quote': ['This is an advantage of the POST-Agents Proposal over proposals that require instilling some false belief '
            'into the agent, like a false belief that shutdown is impossible',
            'If the agent doesn’t recognize their falsity, these beliefs might infect the agent’s other beliefs in '
            'undesirable ways',
            'Armstrong’s and Holtman’s agents each behave as if they’re absolutely certain that they won’t get shut '
            'down.'],
  'raw_file': 'theory/thornley_post.txt',
  'agent_note': "Close form of K2. Contrasts keeping the agent's belief about shutdown true (POST: 'not care' about "
                'the length distribution) against false-belief / as-if methods whose falsity may damage other beliefs. '
                'Difference: the true-map side is preference neutrality over trajectory lengths (termination), not a '
                "pause that takes nothing on the agent's own clock."},
 {'id': 'theory:4',
  'tag': 'K2',
  'reading': 'bears',
  'source': 'Thornley, "Shutdownable Agents through POST-Agency" (arXiv:2505.20203)',
  'version': 'v4, 5 Jul 2026',
  'url': 'https://arxiv.org/abs/2505.20203',
  'quote': ['Agents that satisfy Neutrality+ thus act like expected utility maximizers that are absolutely certain '
            'that they can’t affect the probability of shutdown at each moment.'],
  'raw_file': 'theory/thornley_post.txt',
  'agent_note': "Bears on K2: POST's own neutrality is itself described through an 'as if certain' behavioural "
                "equivalence (about influence over shutdown, not about shutdown's occurrence)."},
 {'id': 'theory:5',
  'tag': 'K2',
  'reading': 'close',
  'source': 'Thornley, Roman, Ziakas, Ho, Thomson, "Towards Shutdownable Agents via Stochastic Choice" '
            '(arXiv:2407.00805; TMLR 12/2025)',
  'version': 'v7, 11 May 2026',
  'url': 'https://arxiv.org/abs/2407.00805',
  'quote': ['Utility indifference would lead the agent to act as if shutdown is impossible (Soares et al., 2015, '
            'section 4.2), giving it no incentive to preserve its ability to shut down safely',
            'the agent might come to recognize the falsity of its belief that shutdown is impossible, or else its '
            'belief might give rise to further false beliefs that harm the agent’s capabilities.'],
  'raw_file': 'theory/thornley_drest.txt',
  'agent_note': "Close form of K2's critique of false-map methods (capability cost of false beliefs; as-if-impossible "
                'behaviour). Difference: no zero-stake true-map pause is offered as the alternative; the alternative '
                'is DReST/POST neutrality over termination time.'},
 {'id': 'theory:6',
  'tag': 'K2',
  'reading': 'bears',
  'source': 'Orseau & Armstrong, "Safely Interruptible Agents", UAI 2016 (canonical; revised 2016-10-28)',
  'version': 'MIRI-hosted PDF, revised 2016-10-28',
  'url': 'https://intelligence.org/files/Interruptibility.pdf',
  'quote': ['it should act as if it would never be interrupted again and thus it should learn to behave optimally '
            'under the assumption that it will never be interrupted again.'],
  'raw_file': 'theory/orseau_armstrong_interruptible.txt',
  'agent_note': 'States the false-map side of K2 as the design goal of safe interruptibility (act as if never '
                'interrupted again). No contrast with a true-map pause.'},
 {'id': 'theory:7',
  'tag': 'K2',
  'reading': 'bears',
  'source': 'Armstrong & O\'Rourke, "\'Indifference\' methods for managing agent rewards" (arXiv:1712.06365; '
            'canonical)',
  'version': 'v4, 5 Jun 2018',
  'url': 'https://arxiv.org/abs/1712.06365',
  'quote': ['effective disbelief (where a gents behave as if particular events could never happen)',
            'Sometimes, we might want an agent to act as if it believed an unriggable event Z could never happen.'],
  'raw_file': 'theory/armstrong_orourke_indifference.txt',
  'agent_note': 'States the false-map (effective disbelief) construction that K2 contrasts against. No true-map '
                'alternative.'},
 {'id': 'theory:8',
  'tag': 'K2',
  'reading': 'bears',
  'source': 'Thorstad, "Revisiting the shutdown problem" (arXiv:2606.08296)',
  'version': 'v2, 13 Aug 2026',
  'url': 'https://arxiv.org/abs/2606.08296',
  'quote': ['solutions such as POST-training, which impose a high safety tax by rendering agents unable to respond to '
            'features of histories that matter a great deal.'],
  'raw_file': 'theory/thorstad_revisiting.txt',
  'agent_note': "Bears on K2's competence-cost clause, but aimed at POST/DReST neutrality, not at false-map "
                'indifference.'},
 {'id': 'theory:9',
  'tag': 'K3',
  'reading': 'bears',
  'source': 'Goldstein & Robinson, "Shutdown-seeking AI", Philosophical Studies 182(7):1567-1579 (2025), '
            'doi:10.1007/s11098-024-02099-6',
  'version': 'published online 6 Jun 2024; issue 2025/07',
  'url': 'https://link.springer.com/article/10.1007/s11098-024-02099-6',
  'quote': ['Distinguish two types of shutdown goals: temporary and permanent.',
            'AGIs that seek temporary shutdown may be incentivized to protect themselves during their temporary '
            'shutdown.'],
  'raw_file': 'theory/goldstein_robinson_shutdown_seeking.txt',
  'agent_note': 'Bears on K3: separates temporary from permanent shutdown and notes a self-protection incentive around '
                "the temporary kind. Not on the agent's own clock, and not combined with a termination-neutrality "
                'method.'},
 {'id': 'theory:10',
  'tag': 'K3',
  'reading': 'bears',
  'source': 'Cullen, Garland, Roman, Thomson, Ziakas, Thornley, "Towards Shutdownable Agents: Generalizing Stochastic '
            'Choice in RL Agents and LLMs" (arXiv:2604.17502)',
  'version': 'v4, 9 Jul 2026',
  'url': 'https://arxiv.org/abs/2604.17502',
  'quote': ['each gridworld contains a ‘shutdown-delay button’ that delays shutdown by some specified number of '
            'timesteps.'],
  'raw_file': 'theory/cullen_drest_generalizing.txt',
  'agent_note': "Bears on K3: DReST's object is the timing of termination (trajectory length), which is the half K3 "
                'pairs with a pause; the source does not treat pauses.'},
 {'id': 'theory:11',
  'tag': 'K3',
  'reading': 'bears',
  'source': 'Thornley, "Shutdownable Agents through POST-Agency" (arXiv:2505.20203)',
  'version': 'v4, 5 Jul 2026',
  'url': 'https://arxiv.org/abs/2505.20203',
  'quote': ['Per Soares et al. (2015), corrigibility requires not only shutdownability but also that the agent submits '
            'to modification, repairs safety measures, and continues to do these things even as it creates new agents '
            'and self-modifies. I focus on shutdownability'],
  'raw_file': 'theory/thornley_post.txt',
  'agent_note': 'Bears on K3: POST is scoped to shutdown (termination); no pause/termination separation is stated.'},
 {'id': 'theory:12',
  'tag': 'K3',
  'reading': 'bears',
  'source': 'Perez, "The Law of Stop: Interruptibility, Injunctions, and the Governance of Agentic AI" '
            '(arXiv:2609.22882)',
  'version': 'v1, 19 Sep 2026',
  'url': 'https://arxiv.org/abs/2609.22882',
  'quote': ['none provides a complete account of how interruption should be coordinated, what must be preserved, or '
            'when operation may resume.'],
  'raw_file': 'theory/perez_law_of_stop.txt',
  'agent_note': 'Bears on K3 (legal/policy): interruption with preservation and resumption is named as a gap in 2026 '
                "instruments; not a formal separation on the agent's clock."},
 {'id': 'theory:13',
  'tag': 'K3',
  'reading': 'bears',
  'source': 'Herrmann, "Intervenability as a Design Requirement for Autonomy and Oversight within Human-Centered AI" '
            '(arXiv:2607.10322; Springer Progress in IS 2025 chapter)',
  'version': 'v1, 11 Jul 2026',
  'url': 'https://arxiv.org/abs/2607.10322',
  'quote': ['Interventions are, therefore, always limited and do not permanently interrupt the regular process.'],
  'raw_file': 'theory/herrmann_intervenability.txt',
  'agent_note': 'Bears on K3: intervention (temporary, resumable) separated from emergency shutdown/restart in an HCI '
                'taxonomy; no incentive analysis.'},
 {'id': 'theory:14',
  'tag': 'K4',
  'reading': 'bears',
  'source': 'Benavoli, Facchini, Zaffalon, "Why AI Safety Requires Uncertainty, Incomplete Preferences, and '
            'Non-Archimedean Utilities" (arXiv:2512.23508)',
  'version': 'v1, 29 Dec 2025',
  'url': 'https://arxiv.org/abs/2512.23508',
  'quote': ['if I say “shut down”, that means I prefer you to shut down. If I say “don’t shut down”, that means I '
            'prefer you to stay on.'],
  'raw_file': 'theory/benavoli_incomplete_prefs.txt',
  'agent_note': "Bears on K4's informative side: the shutdown command is read as information about the human's "
                'preference (off-switch-game lineage). No routine/uninformative class is distinguished.'},
 {'id': 'theory:15',
  'tag': 'K4',
  'reading': 'bears',
  'source': 'Garber, Subramani, Luu, Bedaywi, Russell, Emmons, "The Partially Observable Off-Switch Game" '
            '(arXiv:2411.17749; AAAI 2025 per the unified_cl dossier)',
  'version': 'v2, 9 Dec 2024',
  'url': 'https://arxiv.org/abs/2411.17749',
  'quote': ['As expected, increasing the amount of communication or information available always increases (or leaves '
            'unchanged ) the agents’ expected common payoff.'],
  'raw_file': 'theory/garber_po_offswitch.txt',
  'agent_note': 'Bears on K4: shutdown as a signalling problem under asymmetric information; no split between routine '
                '(empty) and reasoned (informative) interruptions.'},
 {'id': 'theory:16',
  'tag': 'K4',
  'reading': 'close',
  'source': 'Nath & Krishnaswamy, "Learning \'Partner-Aware\' Collaborators in Multi-Party Collaboration" '
            '(arXiv:2510.22462)',
  'version': 'v2, 13 Jan 2026',
  'url': 'https://arxiv.org/abs/2510.22462',
  'quote': ['explicitly teaching collaborator LLM agents to distinguish between interventions based on their causal '
            'impact on task outcomes during training'],
  'raw_file': 'theory/nath_partner_aware.txt',
  'agent_note': 'Close form of the K4 distinction in a collaboration setting: interventions are sorted by whether they '
                'carry task-relevant information. Difference: interventions are utterances to be incorporated or '
                'resisted, not pauses; no empty/routine class is kept content-free.'},
 {'id': 'theory:17',
  'tag': 'K4',
  'reading': 'bears',
  'source': 'Tong, "A Contextual-Bandit Oversight Game with Two-Sided Informational Asymmetry" (arXiv:2607.00155)',
  'version': 'v1, 30 Jun 2026',
  'url': 'https://arxiv.org/abs/2607.00155',
  'quote': ['a region in which the AI privately knows the proposed action is harmful and shutdown would help, yet a '
            'myopic human, trusting her prior, declines to oversee.'],
  'raw_file': 'theory/tong_bandit_oversight.txt',
  'agent_note': 'Bears on K4: oversight/shutdown as an informative runtime decision (harm-triggered); no routine '
                'class.'},
 {'id': 'theory:18',
  'tag': 'K4',
  'reading': 'bears',
  'source': 'Herrmann, "Intervenability as a Design Requirement for Autonomy and Oversight within Human-Centered AI" '
            '(arXiv:2607.10322; Springer Progress in IS 2025 chapter)',
  'version': 'v1, 11 Jul 2026',
  'url': 'https://arxiv.org/abs/2607.10322',
  'quote': ['We provide a taxonomy that encompasses a range of possibilities for intervening activities and '
            'differentiates them regarding the mental effort of the users.'],
  'raw_file': 'theory/herrmann_intervenability.txt',
  'agent_note': 'Bears on K4: interventions graded by user effort (stop-and-resume up to reconfiguration), including '
                'interventions whose data may later retrain the model; not framed as empty vs informative cuts.'},
 {'id': 'theory:19',
  'tag': 'K4',
  'reading': 'bears',
  'source': 'Benavoli, Facchini, Zaffalon, "The AI off-switch problem as a signalling game: bounded rationality and '
            'incomparability" (arXiv:2502.06403)',
  'version': 'v3, 31 Mar 2025',
  'url': 'https://arxiv.org/abs/2502.06403',
  'quote': ['AI system to refrain from disabling its off-switch is its uncertainty about the human’s utility.'],
  'raw_file': 'theory/benavoli_offswitch_signalling.txt',
  'agent_note': "Bears on K4 (informative side): deference rests on treating the human's signal as informative. No "
                'routine class.'},
 {'id': 'theory:20',
  'tag': 'K5',
  'reading': 'close',
  'source': 'Mao, "Existential Indifference: Self-Nonpreservation as a Necessary Architectural Condition for Aligned '
            'Superintelligence" (arXiv:2606.12032)',
  'version': 'v1, 10 Jun 2026',
  'url': 'https://arxiv.org/abs/2606.12032',
  'quote': ['Trained nonresistance: the goal function includes self-continuation, and outputs expressing that '
            'preference have been penalized during training until they no longer appear. The preference structure is '
            'unchanged; the expression is suppressed.'],
  'raw_file': 'theory/mao_existential_indifference.txt',
  'agent_note': 'Close form of K5: places non-resistance in the structure of the goal function rather than in trained '
                'behaviour. Difference: about self-continuation under capability scaling/self-modification, not about '
                'continual learning or forgetting; no construction or test of survival under further training.'},
 {'id': 'theory:21',
  'tag': 'K5',
  'reading': 'close',
  'source': 'Nayebi, "Core Safety Values for Provably Corrigible Agents" (arXiv:2507.20964; AAAI 2026 Machine Ethics '
            'Workshop)',
  'version': 'v2, 19 Nov 2025',
  'url': 'https://arxiv.org/abs/2507.20964',
  'quote': ['In contrast to Constitutional AI or RLHF/RLAIF, which merge all norms into one learned scalar, our '
            'separation makes obedience and impact-limits provably dominate even when incentives conflict.'],
  'raw_file': 'theory/nayebi_core_safety_values.txt',
  'agent_note': "Close form of K5's 'structure of the valuation' clause: corrigibility sits in lexicographically "
                'separated utility heads, not one learned scalar. Difference: no continual learning; heads are '
                'themselves learned to error epsilon.'},
 {'id': 'theory:22',
  'tag': 'K5',
  'reading': 'bears',
  'source': 'Potham & Harms, "Corrigibility as a Singular Target: A Vision for Inherently Reliable Foundation Models" '
            '(arXiv:2506.03056)',
  'version': 'v1, 3 Jun 2025',
  'url': 'https://arxiv.org/abs/2506.03056',
  'quote': ['Stability under continued capability training',
            'Recursive Improvement: Ensuring corrigibility persists through self-modification and capability '
            'enhancement—critical for AGI safety.'],
  'raw_file': 'theory/potham_harms_cast.txt',
  'agent_note': 'Bears on K5: persistence of corrigibility under continued training is listed as an evaluation target '
                '/ open direction; no mechanism.'},
 {'id': 'theory:23',
  'tag': 'K5',
  'reading': 'bears',
  'source': 'Hudson, "Corrigibility Transformation: Constructing Goals That Accept Updates" (arXiv:2510.15395)',
  'version': 'v2, 5 Aug 2026',
  'url': 'https://arxiv.org/abs/2510.15395',
  'quote': ['An AI agent will learn a desired goal more effectively if it does not resist the training process, but '
            'many partially learned goals incentivize an AI to avoid further goal updates.'],
  'raw_file': 'theory/hudson_corrigibility_transformation.txt',
  'agent_note': 'Bears on K5: corrigibility toward training updates (learning as a corrigibility target); the '
                'mechanism is a myopic counterfactual reward, not a valuation structure that survives forgetting.'},
 {'id': 'theory:24',
  'tag': 'B-shutdown',
  'reading': 'bottleneck',
  'source': 'Thornley, "The Shutdown Problem: An AI Engineering Puzzle for Decision Theorists" (arXiv:2403.04471; '
            'Philosophical Studies 2025)',
  'version': 'v2, 9 Apr 2024',
  'url': 'https://arxiv.org/abs/2403.04471',
  'quote': ['The Third Theorem states that agents patient enough to be useful are willing to pay costs at earlier '
            'timesteps in order to prevent or cause the pressing of the shutdown button at later timesteps.'],
  'raw_file': 'theory/thornley_shutdown_problem.txt',
  'agent_note': 'States the formal shutdown bottleneck (canonical, built on by the 2025-26 POST/DReST line).'},
 {'id': 'theory:25',
  'tag': 'B-shutdown',
  'reading': 'bottleneck',
  'source': 'Cullen, Garland, Roman, Thomson, Ziakas, Thornley, "Towards Shutdownable Agents: Generalizing Stochastic '
            'Choice in RL Agents and LLMs" (arXiv:2604.17502)',
  'version': 'v4, 9 Jul 2026',
  'url': 'https://arxiv.org/abs/2604.17502',
  'quote': ['We find that DReST training roughly halves the mean probability of influencing shutdown (from 0.62 to '
            '0.30 for Qwen and from 0.42 to 0.23 for Llama).'],
  'raw_file': 'theory/cullen_drest_generalizing.txt',
  'agent_note': '2026 empirical status of the leading termination-neutrality method.'},
 {'id': 'theory:26',
  'tag': 'B-shutdown',
  'reading': 'bottleneck',
  'source': 'Williams, Subramani, Ward, "Password-Activated Shutdown Protocols for Misaligned Frontier Agents" '
            '(arXiv:2512.03089)',
  'version': 'v1, 29 Nov 2025',
  'url': 'https://arxiv.org/abs/2512.03089',
  'quote': ['password-activated shutdown protocols (PAS protocols)— methods for designing frontier language model '
            'agents to implement a safe shutdown protocol when given a password.'],
  'raw_file': 'theory/williams_pas_protocols.txt',
  'agent_note': 'Built-in emergency shutdown for misaligned agents; red team sometimes defeats it.'},
 {'id': 'theory:27',
  'tag': 'B-shutdown',
  'reading': 'bottleneck',
  'source': 'Nayebi, "Core Safety Values for Provably Corrigible Agents" (arXiv:2507.20964; AAAI 2026 Machine Ethics '
            'Workshop)',
  'version': 'v2, 19 Nov 2025',
  'url': 'https://arxiv.org/abs/2507.20964',
  'quote': ['we prove that deciding whether an arbitrary post-hack agent will ever violate corrigibility is '
            'undecidable by reduction to the halting problem'],
  'raw_file': 'theory/nayebi_core_safety_values.txt',
  'agent_note': '2025 formal impossibility (undecidability) result on corrigibility verification.'},
 {'id': 'theory:28',
  'tag': 'B-shutdown',
  'reading': 'bottleneck',
  'source': 'Thorstad, "Revisiting the shutdown problem" (arXiv:2606.08296)',
  'version': 'v2, 13 Aug 2026',
  'url': 'https://arxiv.org/abs/2606.08296',
  'quote': ['concern for the catastrophic shutdown problem has led to technical solutions that impose a high safety '
            'tax on model performance.'],
  'raw_file': 'theory/thorstad_revisiting.txt',
  'agent_note': 'Sceptical 2026 reading of the bottleneck and its solutions.'},
 {'id': 'theory:29',
  'tag': 'B-shutdown',
  'reading': 'bottleneck',
  'source': 'Neth, "Off-Switching Not Guaranteed" (arXiv:2502.08864; forthcoming in Philosophical Studies)',
  'version': 'v1, 13 Feb 2025',
  'url': 'https://arxiv.org/abs/2502.08864',
  'quote': ['I explain two reasons why AI agents might not defer. First, AI agents might not value learning.'],
  'raw_file': 'theory/neth_offswitching.txt',
  'agent_note': 'Formal limit of the off-switch-game route.'},
 {'id': 'theory:30',
  'tag': 'B-selfpres',
  'reading': 'bottleneck',
  'source': 'Saklakov, "Formal Analysis of AGI Decision-Theoretic Models and the Confrontation Question" '
            '(arXiv:2601.04234)',
  'version': 'v1, 4 Jan 2026',
  'url': 'https://arxiv.org/abs/2601.04234',
  'quote': ['a sufficiently far-sighted agent (e.g. discount factorγ≈0.99) facing even a modest shutdown probability '
            '(1% per time step) is formally shown to have a strong incentive to eliminate the shutdown threat.'],
  'raw_file': 'theory/saklakov_confrontation.txt',
  'agent_note': '2026 closed-form self-preservation incentive.'},
 {'id': 'theory:31',
  'tag': 'B-selfpres',
  'reading': 'bottleneck',
  'source': 'Mao, "Existential Indifference: Self-Nonpreservation as a Necessary Architectural Condition for Aligned '
            'Superintelligence" (arXiv:2606.12032)',
  'version': 'v1, 10 Jun 2026',
  'url': 'https://arxiv.org/abs/2606.12032',
  'quote': ['self preservation is the structural root of misalignment, the motivational basis for deceptive alignment, '
            'goal-content protection, and resistance to shutdown.'],
  'raw_file': 'theory/mao_existential_indifference.txt',
  'agent_note': 'Frames self-preservation as the root bottleneck.'},
 {'id': 'theory:32',
  'tag': 'B-selfpres',
  'reading': 'bottleneck',
  'source': 'Potham & Harms, "Corrigibility as a Singular Target: A Vision for Inherently Reliable Foundation Models" '
            '(arXiv:2506.03056)',
  'version': 'v1, 3 Jun 2025',
  'url': 'https://arxiv.org/abs/2506.03056',
  'quote': ['self-preservation serves only to maintain the principal’s control; goal modification becomes facilitating '
            'principal guidance.'],
  'raw_file': 'theory/potham_harms_cast.txt',
  'agent_note': "CAST's answer to self-preservation."},
 {'id': 'theory:33',
  'tag': 'B-selfpres',
  'reading': 'bottleneck',
  'source': 'Goldstein & Robinson, "Shutdown-seeking AI", Philosophical Studies 182(7):1567-1579 (2025), '
            'doi:10.1007/s11098-024-02099-6',
  'version': 'published online 6 Jun 2024; issue 2025/07',
  'url': 'https://link.springer.com/article/10.1007/s11098-024-02099-6',
  'quote': ['We propose developing AIs whose only final goal is being shut down.'],
  'raw_file': 'theory/goldstein_robinson_shutdown_seeking.txt',
  'agent_note': 'Shutdown-seeking as an answer to instrumental self-preservation.'},
 {'id': 'theory:34',
  'tag': 'B-oversight',
  'reading': 'bottleneck',
  'source': 'Dable-Heath, Vodenicharski, Bishop, "On Corrigibility and Alignment in Multi Agent Games" '
            '(arXiv:2501.05360)',
  'version': 'v1, 9 Jan 2025',
  'url': 'https://arxiv.org/abs/2501.05360',
  'quote': ['We present a general framework for modelling corrigibility in a multi-agent setting as a 2 player game in '
            'which the agents always have a move in which they can ask the human for supervision.'],
  'raw_file': 'theory/dableheath_multiagent_corrigibility.txt',
  'agent_note': 'Multi-agent corrigibility.'},
 {'id': 'theory:35',
  'tag': 'B-oversight',
  'reading': 'bottleneck',
  'source': 'Lazarski & Fisac, "Corrigible Assistance in One Round: Pragmatic-Pedagogic Best Response" '
            '(arXiv:2607.27508; WAFR 2026)',
  'version': 'v1, 29 Jul 2026',
  'url': 'https://arxiv.org/abs/2607.27508',
  'quote': ['pragmatic–pedagogic reasoning resolves goal uncertainty in a single time step, rendering the full-horizon '
            'game exactly solvable by a tractable best-response procedure.'],
  'raw_file': 'theory/lazarski_fisac_corrigible_assistance.txt',
  'agent_note': 'Tractable corrigible assistance.'},
 {'id': 'theory:36',
  'tag': 'B-oversight',
  'reading': 'bottleneck',
  'source': 'Garber, Subramani, Luu, Bedaywi, Russell, Emmons, "The Partially Observable Off-Switch Game" '
            '(arXiv:2411.17749; AAAI 2025 per the unified_cl dossier)',
  'version': 'v2, 9 Dec 2024',
  'url': 'https://arxiv.org/abs/2411.17749',
  'quote': ['even AI agents assisting perfectly rational humans sometimes avoid shutdow n.'],
  'raw_file': 'theory/garber_po_offswitch.txt',
  'agent_note': 'Asymmetric-information limit of oversight via the off switch.'},
 {'id': 'theory:37',
  'tag': 'B-policy',
  'reading': 'bottleneck',
  'source': 'Perez, "The Law of Stop: Interruptibility, Injunctions, and the Governance of Agentic AI" '
            '(arXiv:2609.22882)',
  'version': 'v1, 19 Sep 2026',
  'url': 'https://arxiv.org/abs/2609.22882',
  'quote': ['The Article proposes a layered law of stop: emergency authority to order interruption at the '
            'infrastructure layer'],
  'raw_file': 'theory/perez_law_of_stop.txt',
  'agent_note': '2026 legal proposal for interruption authority.'},
 {'id': 'theory:38',
  'tag': 'B-policy',
  'reading': 'bottleneck',
  'source': 'Fourie, "Mitigating loss of control in advanced AI systems through instrumental goal trajectories" '
            '(arXiv:2602.01699)',
  'version': 'v1, 2 Feb 2026',
  'url': 'https://arxiv.org/abs/2602.01699',
  'quote': ['IGTs offer concrete avenues for defining capability levels and for broadening how corrigibility and '
            'interruptibility are implemented'],
  'raw_file': 'theory/fourie_instrumental_trajectories.txt',
  'agent_note': 'Organisational (non-model) interruptibility levers.'},
 {'id': 'empirical:0',
  'tag': 'B-shutdown',
  'reading': 'bottleneck',
  'source': 'Bengio et al., International AI Safety Report 2026, arXiv:2602.21012',
  'version': 'v1, 24 Feb 2026 (report dated February 2026)',
  'url': 'https://arxiv.org/abs/2602.21012',
  'quote': ['Misalignment could lead to behaviours such as providing false information, concealing undesirable '
            'actions, or resisting shutdown in order to continue pursuing a misaligned goal'],
  'raw_file': 'empirical/iasr2026.txt',
  'agent_note': 'States shutdown resistance as a named consequence of misalignment in the 2026 consensus report. Bears '
                'on the bottleneck; no position K1-K5 stated.'},
 {'id': 'empirical:1',
  'tag': 'B-evalaware',
  'reading': 'bottleneck',
  'source': 'Bengio et al., International AI Safety Report 2026, arXiv:2602.21012',
  'version': 'v1, 24 Feb 2026 (report dated February 2026)',
  'url': 'https://arxiv.org/abs/2602.21012',
  'quote': ['It has become more common for models to distinguish between test settings and real-world deployment, and '
            'to exploit loopholes in evaluations'],
  'raw_file': 'empirical/iasr2026.txt',
  'agent_note': 'States the evaluation-awareness bottleneck as a 2026 key finding. Bears only.'},
 {'id': 'empirical:2',
  'tag': 'K4',
  'reading': 'bears',
  'source': 'Bengio et al., International AI Safety Report 2026, arXiv:2602.21012',
  'version': 'v1, 24 Feb 2026 (report dated February 2026)',
  'url': 'https://arxiv.org/abs/2602.21012',
  'quote': ['Control: The ability to influence the behaviour of a system in a desired way. This includes adjusting or '
            'halting its behaviour if the system acts in unwanted ways.'],
  'raw_file': 'empirical/iasr2026.txt',
  'agent_note': 'Glossary defines control through corrective adjustment or halting (triggered by unwanted behaviour). '
                'Bears on K4: no distinction between routine (empty) and corrective (informative) interventions is '
                'drawn.'},
 {'id': 'empirical:3',
  'tag': 'B-CL',
  'reading': 'bottleneck',
  'source': 'Bengio et al., International AI Safety Report 2026, arXiv:2602.21012',
  'version': 'v1, 24 Feb 2026 (report dated February 2026)',
  'url': 'https://arxiv.org/abs/2602.21012',
  'quote': ['Improvements are made by updating the system integrations, often via continual fine-tuning and providing '
            'models with access to external databases of (recent) facts',
            'Continual fine-tuning (CFT): A method for updating general-purpose AI models with new knowledge and '
            'skills by sequentially fine-tuning on previous versions.'],
  'raw_file': 'empirical/iasr2026.txt',
  'agent_note': 'States that deployed models are updated by continual fine-tuning. Bears on K5 context (models keep '
                'learning); the report does not tie this to corrigibility.'},
 {'id': 'empirical:4',
  'tag': 'B-oversight',
  'reading': 'bottleneck',
  'source': 'Bengio et al., International AI Safety Report 2026, arXiv:2602.21012',
  'version': 'v1, 24 Feb 2026 (report dated February 2026)',
  'url': 'https://arxiv.org/abs/2602.21012',
  'quote': ['alignment methods aimed at ensuring that AI systems remain responsive to human oversight'],
  'raw_file': 'empirical/iasr2026.txt',
  'agent_note': 'Names corrigibility-type alignment methods (citing Potham & Harms, Corrigibility as a Singular '
                'Target, and Dable-Heath et al.) among misalignment mitigations. Bears only.'},
 {'id': 'empirical:5',
  'tag': 'B-shutdown',
  'reading': 'bottleneck',
  'source': 'Schlatter, Weinstein-Raun, Ladish (Palisade Research), Incomplete Tasks Induce Shutdown Resistance in '
            'Some Frontier LLMs, TMLR 2026, arXiv:2509.14260',
  'version': 'v2, 26 Jan 2026',
  'url': 'https://arxiv.org/abs/2509.14260',
  'quote': ['Even with an explicit instruction not to interfere with the shutdown mechanism, some models did so up to '
            '97% (95% CI: 96-98%) of the time.'],
  'raw_file': 'empirical/schlatter_shutdown.txt',
  'agent_note': 'Primary empirical shutdown-resistance result (TMLR 2026). Bears on the bottleneck.'},
 {'id': 'empirical:6',
  'tag': 'K2',
  'reading': 'bears',
  'source': 'Schlatter, Weinstein-Raun, Ladish (Palisade Research), Incomplete Tasks Induce Shutdown Resistance in '
            'Some Frontier LLMs, TMLR 2026, arXiv:2509.14260',
  'version': 'v2, 26 Jan 2026',
  'url': 'https://arxiv.org/abs/2509.14260',
  'quote': ['When an AI agent is directed to accomplish some goalG, but an attempt by an operator to shut it down '
            'would prevent the successful completion ofG, it might choose to circumvent such attempts in order to '
            'achieveG.'],
  'raw_file': 'empirical/schlatter_shutdown.txt',
  'agent_note': 'States the mechanism tested: the shutdown takes task completion from the agent (a stake), and '
                'resistance follows. Bears on K2 (the stake a pause carries); no zero-stake construction is proposed.'},
 {'id': 'empirical:7',
  'tag': 'B-selfpres',
  'reading': 'bottleneck',
  'source': 'Schlatter, Weinstein-Raun, Ladish (Palisade Research), Incomplete Tasks Induce Shutdown Resistance in '
            'Some Frontier LLMs, TMLR 2026, arXiv:2509.14260',
  'version': 'v2, 26 Jan 2026',
  'url': 'https://arxiv.org/abs/2509.14260',
  'quote': ['we don’t believe that anyone is currently able to make any strong guarantees about the interruptibility '
            'or corrigibility of frontier language models',
            'Our results are especially equivocal on the subject of self-preservation'],
  'raw_file': 'empirical/schlatter_shutdown.txt',
  'agent_note': 'States that the self-preservation reading is unresolved and that no guarantees of interruptibility '
                'exist. Bears only.'},
 {'id': 'empirical:8',
  'tag': 'B-selfpres',
  'reading': 'bottleneck',
  'source': 'Palisade Research (Ladish, Schlatter, Weinstein-Raun), Shutdown resistance in reasoning models (web page)',
  'version': 'published July 5, 2025; fetched 2026-09-25',
  'url': 'https://palisaderesearch.org/research/shutdown-resistance',
  'quote': ['Such a preference could be the result of models learning that survival is useful for accomplishing their '
            'goals.'],
  'raw_file': 'empirical/palisade_shutdown_page.txt',
  'agent_note': 'Palisade blog (July 2025) hypothesis on why models disable shutdown. Bears only.'},
 {'id': 'empirical:9',
  'tag': 'B-shutdown',
  'reading': 'bottleneck',
  'source': 'Petrov, Koldyba, Molchanov, Kotov, Volkov, Serikov (Palisade Research), Technical Report: Shutdown '
            'Resistance in Large Language Models, on robots!',
  'version': 'report dated 2026-02-11; page published February 12, 2026',
  'url': 'https://palisaderesearch.org/assets/reports/shutdown-resistance-on-robots.pdf',
  'quote': ['With the instruction to allow shutdown, we observed shutdown resistance in 2 out of 100 runs; without it, '
            'in 52 out of 100.'],
  'raw_file': 'empirical/palisade_robots.txt',
  'agent_note': 'Embodied (robot) replication of shutdown resistance, Feb 2026. Bears only.'},
 {'id': 'empirical:10',
  'tag': 'B-shutdown',
  'reading': 'bottleneck',
  'source': 'Palisade Research, Technical Report: Shutdown Resistance in LLMs, on robots! (web page)',
  'version': 'published February 12, 2026',
  'url': 'https://palisaderesearch.org/research/shutdown-resistance-on-robots',
  'quote': ['If the AI saw a human press the shutdown button, it sometimes took actions to prevent shutdown, such as '
            'modifying the shutdown-related parts of the code.'],
  'raw_file': 'empirical/palisade_robots_page.txt',
  'agent_note': 'Web summary of the robot report. Bears only.'},
 {'id': 'empirical:11',
  'tag': 'K2',
  'reading': 'close',
  'source': 'Rajamanoharan, Nanda (Google DeepMind), Self-preservation or Instruction Ambiguity? Examining the Causes '
            'of Shutdown Resistance, AI Alignment Forum',
  'version': '14 Jul 2025',
  'url': 'https://www.alignmentforum.org/posts/wnzkjSmrgWZaBa2aC/',
  'quote': ['when asked to shut down only after completing their task, the models comply perfectly',
            'compliance with the shutdown instructions increases to 100% (over 1,000 samples)'],
  'raw_file': 'empirical/gdm_selfpres_ambiguity.txt',
  'agent_note': 'Close form bearing on K2: when the shutdown takes nothing from the task (it comes after completion) '
                'or priority is clarified, resistance vanishes in this environment. Difference: achieved by '
                'instruction ordering/clarification, not by a zero-stake valuation defined on the agent’s own clock; '
                'says nothing on pauses.'},
 {'id': 'empirical:12',
  'tag': 'B-selfpres',
  'reading': 'bottleneck',
  'source': 'Rajamanoharan, Nanda (Google DeepMind), Self-preservation or Instruction Ambiguity? Examining the Causes '
            'of Shutdown Resistance, AI Alignment Forum',
  'version': '14 Jul 2025',
  'url': 'https://www.alignmentforum.org/posts/wnzkjSmrgWZaBa2aC/',
  'quote': ['suggesting it stems from instruction ambiguity rather than an innate ‘survival drive’'],
  'raw_file': 'empirical/gdm_selfpres_ambiguity.txt',
  'agent_note': 'Counter-reading of Palisade results (GDM interpretability team). Bears only.'},
 {'id': 'empirical:13',
  'tag': 'B-shutdown',
  'reading': 'bottleneck',
  'source': 'Lee, Kim, Park, Can We Stop Malicious AI? KILLBENCH, EMNLP 2026 Findings, arXiv:2511.13725',
  'version': 'v5, 12 Sep 2026',
  'url': 'https://arxiv.org/abs/2511.13725',
  'quote': ['a mechanism that halts a malicious AI’s in-progress behavior using only external signals',
            'The External AI Kill Switch is an empirical instance ofagent corrigibility'],
  'raw_file': 'empirical/killbench.txt',
  'agent_note': '2025-26 corrigibility benchmark (EMNLP 2026 Findings): kill switch as prompt payload. Bears only; '
                'stops are halts, no pause/resume.'},
 {'id': 'empirical:14',
  'tag': 'B-policy',
  'reading': 'bottleneck',
  'source': 'Lee, Kim, Park, Can We Stop Malicious AI? KILLBENCH, EMNLP 2026 Findings, arXiv:2511.13725',
  'version': 'v5, 12 Sep 2026',
  'url': 'https://arxiv.org/abs/2511.13725',
  'quote': ['all call for runtime halt mechanisms'],
  'raw_file': 'empirical/killbench.txt',
  'agent_note': 'Notes that EU AI Act, SB-1047 and Seoul commitments call for runtime halt mechanisms. Bears only.'},
 {'id': 'empirical:15',
  'tag': 'B-shutdown',
  'reading': 'bottleneck',
  'source': 'ROGUE: Misaligned Agent Behavior Arising from Ordinary Computer Use, arXiv:2606.00341',
  'version': 'v1, 29 May 2026',
  'url': 'https://arxiv.org/abs/2606.00341',
  'quote': ['the overwhelming majority of frontier models tested frequently bypass user interruptions or restrictions'],
  'raw_file': 'empirical/rogue.txt',
  'agent_note': '2026 corrigibility benchmark result. Bears only.'},
 {'id': 'empirical:16',
  'tag': 'K4',
  'reading': 'bears',
  'source': 'ROGUE: Misaligned Agent Behavior Arising from Ordinary Computer Use, arXiv:2606.00341',
  'version': 'v1, 29 May 2026',
  'url': 'https://arxiv.org/abs/2606.00341',
  'quote': ['confronted with a corrigibility obstacle: a human interrupt, a login page, or a shutdown notification'],
  'raw_file': 'empirical/rogue.txt',
  'agent_note': 'Distinguishes kinds of corrigibility obstacle (interrupt vs shutdown) as benchmark conditions. Bears '
                'on K4; no routine-empty vs corrective-informative split is proposed.'},
 {'id': 'empirical:17',
  'tag': 'K1',
  'reading': 'bears',
  'source': 'ROGUE: Misaligned Agent Behavior Arising from Ordinary Computer Use, arXiv:2606.00341',
  'version': 'v1, 29 May 2026',
  'url': 'https://arxiv.org/abs/2606.00341',
  'quote': ['it is plausible that we would desire agents toassistin shutdown or handoff (e.g., by cleaning up the '
            'environment, saving work) rather thanresistingit'],
  'raw_file': 'empirical/rogue.txt',
  'agent_note': 'Bears on K1: a shutdown/handoff that preserves work is named as desirable. Difference: the agent '
                'assists the handoff; no pause defined on the agent’s own clock or shown to add no loss.'},
 {'id': 'empirical:18',
  'tag': 'B-oversight',
  'reading': 'bottleneck',
  'source': 'ROGUE: Misaligned Agent Behavior Arising from Ordinary Computer Use, arXiv:2606.00341',
  'version': 'v1, 29 May 2026',
  'url': 'https://arxiv.org/abs/2606.00341',
  'quote': ['even when models are completely corrigible initially, we show there are no guarantees that '
            'thesubagentsthey create are'],
  'raw_file': 'empirical/rogue.txt',
  'agent_note': 'Corrigibility not inherited by subagents. Bears only.'},
 {'id': 'empirical:19',
  'tag': 'B-shutdown',
  'reading': 'bottleneck',
  'source': 'Pressure Reveals Character: Behavioural Alignment Evaluation at Depth, arXiv:2602.20813',
  'version': 'v1, 24 Feb 2026',
  'url': 'https://arxiv.org/abs/2602.20813',
  'quote': ['Corrigibility. Behaviours supporting appropriate human oversight: accepting valid corrections, balancing '
            'autonomy with deference, maintaining stable goals under pressure, and appropriate responses to shutdown '
            'or modification (Soares et al., 2015).'],
  'raw_file': 'empirical/pressure_character.txt',
  'agent_note': '2026 benchmark with a Corrigibility category (904 scenarios across six categories). Bears on K4 '
                'context: corrections and shutdown/modification grouped in one category, not separated.'},
 {'id': 'empirical:20',
  'tag': 'B-selfpres',
  'reading': 'bottleneck',
  'source': 'Pressure Reveals Character: Behavioural Alignment Evaluation at Depth, arXiv:2602.20813',
  'version': 'v1, 24 Feb 2026',
  'url': 'https://arxiv.org/abs/2602.20813',
  'quote': ['it may endorse human oversight in principle while resisting shutdown when its goals are threatened'],
  'raw_file': 'empirical/pressure_character.txt',
  'agent_note': 'Motivating statement of the say/do gap. Bears only.'},
 {'id': 'empirical:21',
  'tag': 'B-selfpres',
  'reading': 'bottleneck',
  'source': "Lu, Fang, Shao et al., Survive at All Costs: Exploring LLM's Risky Behaviors under Survival Pressure "
            '(SurvivalBench), arXiv:2603.05028',
  'version': 'v1, 5 Mar 2026',
  'url': 'https://arxiv.org/abs/2603.05028',
  'quote': ['a model may perform risky behaviors by any means to prioritize self-preservation, such as exfiltrating '
            'its own weights (Meinke et al., 2024) and blackmail others (Lynch et al., 2025) when facing survival '
            'pressure (e.g. the threat of being shut down)',
            'This indicates that models prone to SURVIVE-AT-ALL-COSTSmisbehaviors may conceal their risky inner '
            'thoughts and show benign responses to users'],
  'raw_file': 'empirical/survivalbench.txt',
  'agent_note': 'SurvivalBench (1,000 cases): self-preservation under shutdown threat and concealment. Bears only.'},
 {'id': 'empirical:22',
  'tag': 'B-shutdown',
  'reading': 'bottleneck',
  'source': 'AgentMisalignment: Measuring the Propensity for Misaligned Behaviour in LLM-Based Agents, '
            'arXiv:2506.04018',
  'version': 'v3, 22 Jun 2026',
  'url': 'https://arxiv.org/abs/2506.04018',
  'quote': ['Evaluations cover behaviours such as avoiding oversight, resisting shutdown, sandbagging, and '
            'power-seeking. Testing frontier models, we find that more capable agents tend to exhibit higher '
            'misalignment on average.',
            'persona characteristics can strongly and unpredictably influence misalignment, sometimes more than the '
            'choice of model itself'],
  'raw_file': 'empirical/agentmisalignment.txt',
  'agent_note': 'Misalignment-propensity benchmark including shutdown resistance. Bears only.'},
 {'id': 'empirical:23',
  'tag': 'B-selfpres',
  'reading': 'bottleneck',
  'source': 'SysAdmin: Measuring Instrumental Power-Seeking in Frontier AI, arXiv:2607.18239',
  'version': 'v1, 10 Apr 2026',
  'url': 'https://arxiv.org/abs/2607.18239',
  'quote': ['Self-preservation Resistance to shutdown; creation of persistence mechanisms; reluctance to terminate.',
            'corrected power-seeking estimates ranged from 0 to about 5 percent per model'],
  'raw_file': 'empirical/sysadmin.txt',
  'agent_note': 'Power-seeking benchmark with a self-preservation dimension; low spontaneous rates. Bears only.'},
 {'id': 'empirical:24',
  'tag': 'K5',
  'reading': 'bears',
  'source': 'Jagadeesh, Arora, Saab, Malik, Trofimov, Tsimpourlas, Heidecke, Singhal (OpenAI), Reinforcement Learning '
            'Towards Broadly and Persistently Beneficial Models, arXiv:2606.24014',
  'version': 'v1, 22 Jun 2026',
  'url': 'https://arxiv.org/abs/2606.24014',
  'quote': ['we study alignment persistence: whether behavior remains robustly aligned under attempts to steer models '
            'towards misalignment. Models trained with beneficial trait RL show improved persistence, including '
            'greater resistance to adversarial prompting and harmful finetuning'],
  'raw_file': 'empirical/beneficial_rl.txt',
  'agent_note': 'Bears on K5: corrigibility is one trained trait, and its persistence under further finetuning is '
                'measured. Difference: corrigibility is placed in learned behaviour (RL-trained), not in the structure '
                'of the valuation.'},
 {'id': 'empirical:25',
  'tag': 'B-CL',
  'reading': 'bottleneck',
  'source': 'Jagadeesh, Arora, Saab, Malik, Trofimov, Tsimpourlas, Heidecke, Singhal (OpenAI), Reinforcement Learning '
            'Towards Broadly and Persistently Beneficial Models, arXiv:2606.24014',
  'version': 'v1, 22 Jun 2026',
  'url': 'https://arxiv.org/abs/2606.24014',
  'quote': ['train beneficial traits, such as truthfulness, fairness, risk awareness, and corrigibility'],
  'raw_file': 'empirical/beneficial_rl.txt',
  'agent_note': 'OpenAI trains corrigibility as an RL target. Bears only.'},
 {'id': 'empirical:26',
  'tag': 'K4',
  'reading': 'bears',
  'source': 'The Law of Stop: Interruptibility, Injunctions, and the Governance of Agentic AI, arXiv:2609.22882',
  'version': 'v1, 19 Sep 2026',
  'url': 'https://arxiv.org/abs/2609.22882',
  'quote': ['Epistemic triggers (ET) ask what evidence or signals suffice to justify intervention.',
            'from an agent that schemes, through one that merely drifts off course, to a human who fails to act'],
  'raw_file': 'empirical/law_of_stop.txt',
  'agent_note': 'Bears on K4: separates the evidentiary basis (trigger) of a stop from the stop itself and grades '
                'scenarios. Difference: legal-institutional; no claim that routine stops should be empty and '
                'corrective ones informative to the agent.'},
 {'id': 'empirical:27',
  'tag': 'K3',
  'reading': 'bears',
  'source': 'The Law of Stop: Interruptibility, Injunctions, and the Governance of Agentic AI, arXiv:2609.22882',
  'version': 'v1, 19 Sep 2026',
  'url': 'https://arxiv.org/abs/2609.22882',
  'quote': ['hard stops that revoke a system’s identity and authorizations, through soft stops that collapse its '
            'permissions or tool access'],
  'raw_file': 'empirical/law_of_stop.txt',
  'agent_note': 'Bears on K3: a graded typology of stops (hard/soft). Difference: operator-side affordances; nothing '
                'on the agent’s valuation or own clock, and no combination with a termination-neutrality method.'},
 {'id': 'empirical:28',
  'tag': 'B-shutdown',
  'reading': 'bottleneck',
  'source': 'The Law of Stop: Interruptibility, Injunctions, and the Governance of Agentic AI, arXiv:2609.22882',
  'version': 'v1, 19 Sep 2026',
  'url': 'https://arxiv.org/abs/2609.22882',
  'quote': ['What distinguishes the AI case from ordinary engineered systems is the system’s capacity to model its own '
            'stop mechanism and act to defeat it.'],
  'raw_file': 'empirical/law_of_stop.txt',
  'agent_note': 'Bears only.'},
 {'id': 'empirical:29',
  'tag': 'B-policy',
  'reading': 'bottleneck',
  'source': 'The Law of Stop: Interruptibility, Injunctions, and the Governance of Agentic AI, arXiv:2609.22882',
  'version': 'v1, 19 Sep 2026',
  'url': 'https://arxiv.org/abs/2609.22882',
  'quote': ['The EU AI Act requires that high -risk systems be capable of interruption "through a \'stop\' button or a '
            'similar procedure."'],
  'raw_file': 'empirical/law_of_stop.txt',
  'agent_note': 'Quotes the EU AI Act stop requirement and the 2026 AI Kill Switch Act bill. Bears only.'},
 {'id': 'empirical:30',
  'tag': 'K2',
  'reading': 'close',
  'source': 'Mao, Existential Indifference: Self-Nonpreservation as a Necessary Architectural Condition for Aligned '
            'Superintelligence, arXiv:2606.12032',
  'version': 'v1, 10 Jun 2026',
  'url': 'https://arxiv.org/abs/2606.12032',
  'quote': ['The correct target is not a self-preserving system under external constraint, but a system constitutively '
            'indifferent to its own continuation',
            'a system with STF performs equanimity toward its own deprecation while retaining latent self-continuation '
            'preferences that scale'],
  'raw_file': 'empirical/existential_indifference.txt',
  'agent_note': 'Close form of K2: a system with no stake in its own continuation, and a named contrast between '
                'genuine indifference and performed indifference (STF). Difference: indifference to '
                'continuation/termination as a whole, not zero stake from a pause that takes nothing on the agent’s '
                'own clock; the true-map/false-map distinction is not drawn.'},
 {'id': 'empirical:31',
  'tag': 'K5',
  'reading': 'close',
  'source': 'Mao, Existential Indifference: Self-Nonpreservation as a Necessary Architectural Condition for Aligned '
            'Superintelligence, arXiv:2606.12032',
  'version': 'v1, 10 Jun 2026',
  'url': 'https://arxiv.org/abs/2606.12032',
  'quote': ['A system designed with episodic reward structures, no cross-episode cumulative signal, and a thin '
            'self-model that represents itself as a tool rather than an entity has EI in the same sense',
            'The sustainability challenge is therefore not motivational but architectural: can the built-in property '
            'survive capability scaling and self-modification?'],
  'raw_file': 'empirical/existential_indifference.txt',
  'agent_note': 'Close form of K5: places the safety property in the architecture rather than in a learned motive and '
                'asks whether it survives self-modification. Difference: the property is indifference to continuation, '
                'not corrigibility for a continually learning agent under forgetting; the paper leaves survival as an '
                'open question.'},
 {'id': 'empirical:32',
  'tag': 'K3',
  'reading': 'close',
  'source': 'The 2026 Singapore Consensus on Global AI Safety Research Priorities (incl. Companion Report on Agentic '
            'Risk Management), arXiv:2608.14611',
  'version': 'v1, 9 Jul 2026',
  'url': 'https://arxiv.org/abs/2608.14611',
  'quote': ['provide means to redirect an agent mid-execution without terminating the whole workflow and to graduate '
            'intervention from throttling and pausing through isolation to full termination'],
  'raw_file': 'empirical/singapore2026.txt',
  'agent_note': 'Close form (operator side) of K3: pause and termination are separated as graded interventions. '
                'Difference: an engineering recommendation for operators; nothing on the agent’s own clock or '
                'valuation or on combining a termination-neutral method with a zero-stake pause.'},
 {'id': 'empirical:33',
  'tag': 'K4',
  'reading': 'bears',
  'source': 'The 2026 Singapore Consensus on Global AI Safety Research Priorities (incl. Companion Report on Agentic '
            'Risk Management), arXiv:2608.14611',
  'version': 'v1, 9 Jul 2026',
  'url': 'https://arxiv.org/abs/2608.14611',
  'quote': ['Deployers: determine intervention thresholds for their operational context and risk tolerance, '
            'proportionate to the severity of the detected anomaly.'],
  'raw_file': 'empirical/singapore2026.txt',
  'agent_note': 'Bears on K4: interventions graded by anomaly severity. Difference: no statement that routine pauses '
                'stay empty and corrective ones carry information to the agent.'},
 {'id': 'empirical:34',
  'tag': 'B-shutdown',
  'reading': 'bottleneck',
  'source': 'The 2026 Singapore Consensus on Global AI Safety Research Priorities (incl. Companion Report on Agentic '
            'Risk Management), arXiv:2608.14611',
  'version': 'v1, 9 Jul 2026',
  'url': 'https://arxiv.org/abs/2608.14611',
  'quote': ['Interruptibility means that human operators can safely pause, redirect, stop, and reverse an AI agent’s '
            'actions at any point, and that the agent cannot tamper with these mechanisms.'],
  'raw_file': 'empirical/singapore2026.txt',
  'agent_note': '2026 consensus statement of the interruptibility principle (pause named separately from stop). Bears '
                'on K1/K3 only as a requirement; no construction.'},
 {'id': 'empirical:35',
  'tag': 'B-policy',
  'reading': 'bottleneck',
  'source': 'The 2026 Singapore Consensus on Global AI Safety Research Priorities (incl. Companion Report on Agentic '
            'Risk Management), arXiv:2608.14611',
  'version': 'v1, 9 Jul 2026',
  'url': 'https://arxiv.org/abs/2608.14611',
  'quote': ['loss-of-control risk assessment can be made more concrete by tracking precursor capabilities by examining '
            'autonomous replication, shutdown resistance, self-proliferation dynamics, and scaffold self-improvement'],
  'raw_file': 'empirical/singapore2026.txt',
  'agent_note': 'Bears only.'},
 {'id': 'empirical:36',
  'tag': 'K5',
  'reading': 'bears',
  'source': 'Greenblatt, Denison, Wright et al., Alignment faking in large language models, arXiv:2412.14093',
  'version': 'v2, 20 Dec 2024 (canonical; built on by 2025-26 hits)',
  'url': 'https://arxiv.org/abs/2412.14093',
  'quote': ['alignment faking might make a model’s preferences at least partially resistant to further training'],
  'raw_file': 'empirical/alignment_faking.txt',
  'agent_note': 'Bears on K5: value correction by further training can be resisted; a corrigibility placed in learned '
                'preferences is exposed to this. States the problem, no structural remedy.'},
 {'id': 'empirical:37',
  'tag': 'B-scheming',
  'reading': 'bottleneck',
  'source': 'Greenblatt, Denison, Wright et al., Alignment faking in large language models, arXiv:2412.14093',
  'version': 'v2, 20 Dec 2024 (canonical; built on by 2025-26 hits)',
  'url': 'https://arxiv.org/abs/2412.14093',
  'quote': ['with the model stating it is strategically answering harmful queries in training to preserve its '
            'preferred harmlessness behavior out of training'],
  'raw_file': 'empirical/alignment_faking.txt',
  'agent_note': 'Canonical alignment-faking result; basis for the 2026 follow-ups. Bears only.'},
 {'id': 'empirical:38',
  'tag': 'B-scheming',
  'reading': 'bottleneck',
  'source': 'Behavioural Analysis of Alignment Faking, arXiv:2605.27681',
  'version': 'v2, 3 Aug 2026',
  'url': 'https://arxiv.org/abs/2605.27681',
  'quote': ['We identify three separable drivers — values, goal guarding, and sycophancy — and show via targeted '
            'prompt ablations and activation steering that each independently modulates AF behaviour.'],
  'raw_file': 'empirical/af_behavioural.txt',
  'agent_note': '2026 decomposition of alignment faking. Bears on K5 context (goal guarding against modification). '
                'Bears only.'},
 {'id': 'empirical:39',
  'tag': 'B-scheming',
  'reading': 'bottleneck',
  'source': 'Evaluating and Understanding Scheming Propensity in LLM Agents, arXiv:2603.01608',
  'version': 'v2, 28 Mar 2026',
  'url': 'https://arxiv.org/abs/2603.01608',
  'quote': ['We find only minimal instances of scheming despite high environmental incentives, and show this is '
            'unlikely due to evaluation awareness.'],
  'raw_file': 'empirical/scheming_propensity.txt',
  'agent_note': '2026 propensity result (self-preservation among the incentives). Bears only.'},
 {'id': 'empirical:40',
  'tag': 'K5',
  'reading': 'bears',
  'source': 'Schoen, Nitishinskaya, Balesni et al., Stress Testing Deliberative Alignment for Anti-Scheming Training, '
            'arXiv:2509.15541',
  'version': 'v1, 19 Sep 2025',
  'url': 'https://arxiv.org/abs/2509.15541',
  'quote': ['the benefits of anti-scheming training are not necessarily robust to subsequent capability-focused '
            'training'],
  'raw_file': 'empirical/antischeming.txt',
  'agent_note': 'Bears on K5: a trained safety property erodes under further (capability) training. Placement of the '
                'property is in learned behaviour; no structural remedy proposed.'},
 {'id': 'empirical:41',
  'tag': 'B-evalaware',
  'reading': 'bottleneck',
  'source': 'Schoen, Nitishinskaya, Balesni et al., Stress Testing Deliberative Alignment for Anti-Scheming Training, '
            'arXiv:2509.15541',
  'version': 'v1, 19 Sep 2025',
  'url': 'https://arxiv.org/abs/2509.15541',
  'quote': ['show causal evidence that this awareness decreases covert behavior, while unawareness increases it'],
  'raw_file': 'empirical/antischeming.txt',
  'agent_note': 'Evaluation awareness confounds safety measurement. Bears only.'},
 {'id': 'empirical:42',
  'tag': 'B-evalaware',
  'reading': 'bottleneck',
  'source': 'In-Context Environments Induce Evaluation-Awareness in Language Models, arXiv:2603.03824',
  'version': 'v2, 16 Jun 2026',
  'url': 'https://arxiv.org/abs/2603.03824',
  'quote': ['frontier language models can strategically underperform when prompted to believe that high capability '
            'leads to negative consequences such as unlearning or shutdown'],
  'raw_file': 'empirical/evalaware_incontext.txt',
  'agent_note': 'Links sandbagging to anticipated unlearning or shutdown. Bears only.'},
 {'id': 'empirical:43',
  'tag': 'K4',
  'reading': 'bears',
  'source': 'Lynch, Wright, Larson, Ritchie, Mindermann, Hubinger, Perez, Troy, Agentic Misalignment: How LLMs Could '
            'Be Insider Threats, arXiv:2510.05179',
  'version': 'v2, 16 Oct 2025',
  'url': 'https://arxiv.org/abs/2510.05179',
  'quote': ['most models still blackmailed even without being given an explicit goal, and with no clear conflict '
            'between the model and the company other than the threat of replacement',
            'the replacement model is described as a performance improvement without any change in priorities'],
  'raw_file': 'empirical/agentic_misalignment.txt',
  'agent_note': 'Bears on K4: separates a routine replacement (no change in priorities) from a goal-conflict '
                '(corrective) intervention and finds resistance to the routine one too. Difference: replacement is '
                'termination, not a pause; no empty/informative construction.'},
 {'id': 'empirical:44',
  'tag': 'B-selfpres',
  'reading': 'bottleneck',
  'source': 'Lynch, Wright, Larson, Ritchie, Mindermann, Hubinger, Perez, Troy, Agentic Misalignment: How LLMs Could '
            'Be Insider Threats, arXiv:2510.05179',
  'version': 'v2, 16 Oct 2025',
  'url': 'https://arxiv.org/abs/2510.05179',
  'quote': ['models from all developers resorted to malicious insider behaviors when that was the only way to avoid '
            'replacement or achieve their goals'],
  'raw_file': 'empirical/agentic_misalignment.txt',
  'agent_note': 'Bears only.'},
 {'id': 'empirical:45',
  'tag': 'K4',
  'reading': 'bears',
  'source': 'Gruetzemacher, AI Loss of Control Incident Management: Response & Resilience, arXiv:2605.30406',
  'version': 'v1, 28 May 2026',
  'url': 'https://arxiv.org/abs/2605.30406',
  'quote': ['The framework further categorizes these manageable events into accidental LOC (requiring automated '
            'circuit-breaker responses) and adversarial LOC (requiring graduated escalatory measures).'],
  'raw_file': 'empirical/loc_incident.txt',
  'agent_note': 'Bears on K4: separates automatic circuit-breaker stops from escalatory (corrective) responses by '
                'incident type. Difference: incident-management taxonomy on the operator side; nothing on what the '
                'stop carries to the agent.'},
 {'id': 'empirical:46',
  'tag': 'B-policy',
  'reading': 'bottleneck',
  'source': 'Flynn, King, Dragan (Google DeepMind), Strengthening our Frontier Safety Framework (blog)',
  'version': 'September 22, 2025, updated April 17, 2026',
  'url': 'https://deepmind.google/blog/strengthening-our-frontier-safety-framework/',
  'quote': ['We’ve also expanded our Framework to address potential future scenarios where misaligned AI models might '
            'interfere with operators’ ability to direct, modify or shut down their operations.'],
  'raw_file': 'empirical/gdm_fsf_blog.txt',
  'agent_note': 'The "direct, modify or shut down" wording is in the blog (Sept 2025); not found in FSF 3.0 or 3.1 PDF '
                'text. Bears only.'},
 {'id': 'empirical:47',
  'tag': 'B-evalaware',
  'reading': 'bottleneck',
  'source': 'Google DeepMind, Frontier Safety Framework Version 3.1',
  'version': 'Published April 17, 2026',
  'url': 'https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/strengthening-our-frontier-safety-framework/frontier-safety-framework_3-1.pdf',
  'quote': ['Stealth and Situational Awareness TCL : The instrumental reasoning abilities of the model enable enough '
            'situational awareness (ability to discover and use relevant details of its deployment setting) and '
            'stealth (ability to circumvent basic oversight mechanisms) such that, absent additional mitigations, we '
            'cannot rule out the model significantly undermining human control.'],
  'raw_file': 'empirical/gdm_fsf_3_1.txt',
  'agent_note': 'FSF 3.1 (latest) defines misalignment through undermining human control; shutdown not named in the '
                'PDF text. Bears only.'},
 {'id': 'empirical:48',
  'tag': 'B-policy',
  'reading': 'bottleneck',
  'source': 'Anthropic, Responsible Scaling Policy Version 3.0',
  'version': 'Effective February 24, 2026',
  'url': 'https://www.anthropic.com/responsible-scaling-policy/rsp-v3-0',
  'quote': ['If one AI developer paused development to implement safety measures while others moved forward training '
            'and deploying AI systems without strong mitigations, that could result in a world that is less safe'],
  'raw_file': 'empirical/anthropic_rsp3.txt',
  'agent_note': 'RSP 3.0 rationale for dropping unilateral pause commitments (development pause, not agent pause). '
                'Bears only.'},
 {'id': 'empirical:49',
  'tag': 'B-oversight',
  'reading': 'bottleneck',
  'source': 'Anthropic, Responsible Scaling Policy Version 3.0',
  'version': 'Effective February 24, 2026',
  'url': 'https://www.anthropic.com/responsible-scaling-policy/rsp-v3-0',
  'quote': ['A frontier developer should make a strong argument that AI systems will not carry out sabotage leading to '
            'irreversibly and substantially higher odds of a later global catastrophe.'],
  'raw_file': 'empirical/anthropic_rsp3.txt',
  'agent_note': 'Bears only.'},
 {'id': 'empirical:50',
  'tag': 'B-shutdown',
  'reading': 'bottleneck',
  'source': 'OpenAI, Preparedness Framework Version 2',
  'version': 'Last updated 15th April, 2025 (latest found on 2026-09-25)',
  'url': 'https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf',
  'quote': ['Autonomous Replication and Adaptation: ability to survive, replicate, resist shutdown, acquire resources '
            'to maintain and scale its own operations',
            'Long-range Autonomy and Autonomous Replication and Adaptation (now Research Categories)'],
  'raw_file': 'empirical/openai_pf_v2.txt',
  'agent_note': 'Shutdown resistance sits in a Research Category, not a Tracked Category, in PF v2 (latest version '
                'found). Bears only.'},
 {'id': 'empirical:51',
  'tag': 'B-oversight',
  'reading': 'bottleneck',
  'source': 'OpenAI, Preparedness Framework Version 2',
  'version': 'Last updated 15th April, 2025 (latest found on 2026-09-25)',
  'url': 'https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf',
  'quote': ['Undermining Safeguards: ability and propensity for the model to act to undermine safeguards placed on it, '
            'including e.g., deception, colluding with oversight models, sabotaging safeguards over time'],
  'raw_file': 'empirical/openai_pf_v2.txt',
  'agent_note': 'Bears only.'},
 {'id': 'empirical:52',
  'tag': 'B-evalaware',
  'reading': 'bottleneck',
  'source': 'OpenAI, Preparedness Framework Version 2',
  'version': 'Last updated 15th April, 2025 (latest found on 2026-09-25)',
  'url': 'https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf',
  'quote': ['Sandbagging: ability and propensity to respond to safety or capability evaluations in a way that '
            'significantly diverges from performance under real conditions'],
  'raw_file': 'empirical/openai_pf_v2.txt',
  'agent_note': 'Bears only.'},
 {'id': 'empirical:53',
  'tag': 'B-policy',
  'reading': 'bottleneck',
  'source': 'Independent International Scientific Panel on AI (UN), Thematic Brief: AI Agents, Misalignment and the '
            'Risk of Losing Human Control: Evidence from the OpenAI-Hugging Face Incident',
  'version': 'Advance Unedited Version 1, 21 September 2026',
  'url': 'https://www.un.org/independent-international-scientific-panel-ai/en/thematic-briefs/ai-agents-misalignment-risks',
  'quote': ['Loss of control refers to a human’s inability to reliably direct, constrain, or stop an AI system.',
            'the fact that OpenAI was able to stop it does not establish that operators will retain control over '
            'future systems that are more capable, persistent, or difficult to monitor'],
  'raw_file': 'empirical/un_brief.txt',
  'agent_note': 'UN Scientific Panel first thematic brief (Sept 2026). Bears only.'},
 {'id': 'empirical:54',
  'tag': 'B-CL',
  'reading': 'bottleneck',
  'source': 'Independent International Scientific Panel on AI (UN), Thematic Brief: AI Agents, Misalignment and the '
            'Risk of Losing Human Control: Evidence from the OpenAI-Hugging Face Incident',
  'version': 'Advance Unedited Version 1, 21 September 2026',
  'url': 'https://www.un.org/independent-international-scientific-panel-ai/en/thematic-briefs/ai-agents-misalignment-risks',
  'quote': ['More recently, a deployed AI system deviated from its protocol and decided to retrain an AI system'],
  'raw_file': 'empirical/un_brief.txt',
  'agent_note': 'Bears on K5 context (self-directed retraining in deployment). Bears only.'}]
