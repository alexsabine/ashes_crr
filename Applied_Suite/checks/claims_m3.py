"""APP1 stage C, family M3 (Applied_Suite/APPLICATIONS_DECLARATION.md, pushed at 4e78058): privacy and security of continual
learning. The risks of stored examples, the right to erasure and machine unlearning, poisoning and backdoors in continual or
online learning, and oversight or interruptibility requirements in 2025-26 regulation and standards, read against AP1-AP10.

Every quote is copied from the text extracted from the fetched file. Sources were fetched on 2026-09-30 through the session
proxy (TLS verified against the proxy CA bundle), with one exception:
- the Official Journal text of the AI Act (Regulation (EU) 2024/1689) was fetched from EUR-Lex on 2026-09-29 by EPS3
  (docs/citations/eps3_2026-09-29.md; HTML sha256 7b1622f3..., re-hashed on 2026-09-30 and unchanged). On 2026-09-30 EUR-Lex
  answered HTTP 202 with an empty body for every URL tried, so that copy was reused and the text re-extracted here.
Extraction: PDF text by pymupdf 1.28.2 (arXiv current version, as listed on the abstract page on the day); HTML by
BeautifulSoup get_text('\\n') after script, style, noscript and svg were dropped.
Raw files live outside the repository under /tmp/claude-0/app1_src/ (`raw_file` is relative to that root):
  - m3/src/      the fetched files (and the bodies of failed fetches, kept as the record of the attempt);
  - m3/reused/   the EUR-Lex AI Act HTML fetched by EPS3 on 2026-09-29;
  - m3/txt/      the extracted text that the quotes are checked against;
  - m3/FETCH_LOG.txt  every fetch with its HTTP status, size and final URL.
sha256 of every file: /tmp/claude-0/app1_src/m3/SHA256SUMS.txt, and per source in docs/citations/app1_m3_2026-09-30.md.
The verbatim check uses Open_Bottlenecks/checks/verify.py's normalisation unchanged (NFKC, whitespace collapsed, a
line-break hyphen read as kept or rejoined; a quote containing "[...]" is checked fragment by fragment).

Roles (the task that set up this sweep): 'who_does_it' = who already does it and how; 'what_is_hard' = what they say is
hard; 'our_method_relevance' = a source that bears directly on whether the record's method addresses that difficulty;
'regulation' = a legal, regulatory or standards text; 'risk' = a documented attack or failure mode. `application` is
AP1..AP10 of the declaration, or 'general' where a source bears on every application. `agent_note` is the agent's reading,
not the source's words. It names the record only by file or ledger id and quotes no number from the record (R1, R8).
Readings of legal texts are information, not legal advice. Numbers inside quotes are the source's own, on its own protocol;
sources are not comparable with each other. "Not found" is never "novel". Nothing here grades an application; the grading
is Applied_Suite/checks/applications.py's.
"""

T = 'm3/txt/'

CLAIMS = [
    # ------------------------------------------------------------------ AP1: on-device personalisation without a sweep
    {'id': 'm3:1', 'application': 'AP1', 'role': 'who_does_it',
     'source': 'US FDA, Marketing Submission Recommendations for a Predetermined Change Control Plan for Artificial '
               'Intelligence-Enabled Device Software Functions (guidance for industry and FDA staff)',
     'version': 'final guidance, "Document issued on August 18, 2025. Document originally issued on December 4, 2024." '
                '(PDF as served 2026-09-30; the landing page answered HTTP 401)',
     'url': 'https://www.fda.gov/media/166704/download',
     'quote': ['implemented differently on different devices on the market based on, for example, the unique characteristics '
               'of a specific clinical site or individual patients (sometimes referred to as heterogenous or local changes, '
               'or local adaptations).',
               'For local adaptations, the Description of Modifications should include a description of what local factors '
               'or conditions warrant a local change.',
               'Will updates be made globally (i.e., the same update applied to all devices in the field) or locally (e.g., '
               'the devices may be modified for a patient/provider/care unit/hospital)?'],
     'raw_file': T + 'fda_pccp.pdf.txt',
     'agent_note': 'How per-device adaptation is done in one regulated sector: a medical AI device may adapt per patient or '
                   'per site, if the change and its triggers are described in a plan authorised before marketing. The text '
                   'does not mention hyperparameter tuning. A sweep-free weight (K1) would enter such a plan as a fixed '
                   're-training practice. The record has no medical carrier.'},
    {'id': 'm3:2', 'application': 'AP1', 'role': 'what_is_hard',
     'source': 'NIST AI 100-2 E2025, Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations '
               '(Vassilev et al., with the US AI Safety Institute and the UK AI Security Institute)',
     'version': 'NIST AI 100-2e2025, March 2025 (PDF as served 2026-09-30)',
     'url': 'https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf',
     'quote': ['These incidents highlight the risks associated with online learning, as the Tay.AI chatbot was updated in '
               'real-time based on user interactions',
               'In all these incidents, attackers crafted poisoned samples after an initial model release, counting on the '
               'fact that models are continuously updated.'],
     'raw_file': T + 'nist_ai_100-2e2025.pdf.txt',
     'agent_note': 'The attack surface of any learner that keeps updating from its users, as NIST states it. AP1 learns on '
                   'the device from the user\'s own data, so it is in this class. K1 sets a penalty weight and K2 preserves '
                   'state across a pause; neither filters or checks inputs. This is a different difficulty, and nothing in the '
                   'record addresses it.'},

    # ------------------------------------------------------------------ AP2: fine-tuning on interruptible compute
    {'id': 'm3:3', 'application': 'AP2', 'role': 'who_does_it',
     'source': 'Hugging Face (Patry, Biderman et al.), Audit shows that safetensors is safe and ready to become the default',
     'version': 'blog post, published May 23, 2023 (as served 2026-09-30)',
     'url': 'https://huggingface.co/blog/safetensors-security-audit',
     'quote': ['Hugging Face , in close collaboration with EleutherAI and Stability AI , has ordered an external security '
               'audit of the safetensors library, the results of which allow all three organizations to move toward making '
               'the library the default format for saved models.',
               'No critical security flaw leading to arbitrary code execution was found.'],
     'raw_file': T + 'hf_safetensors_audit.html.txt',
     'agent_note': 'How the ecosystem secures saved model state: a tensor-only file format, externally audited. It is the '
                   'integrity half of pause-and-resume, which the record\'s pause construction (K2) does not touch. The spaces '
                   'before the commas are hyperlink boundaries in the page. Older than 2025; whether it is the default '
                   'everywhere in 2026 was not checked.'},
    {'id': 'm3:4', 'application': 'AP2', 'role': 'what_is_hard',
     'source': 'PyTorch documentation: torch.load, and the Serialization semantics note',
     'version': 'PyTorch 2.14 documentation as served 2026-09-30 (the "stable" URLs redirect to /docs/2.14/)',
     'url': 'https://docs.pytorch.org/docs/2.14/generated/torch.load.html',
     'quote': ['torch.load() uses an unpickler under the hood. Never load data from an untrusted source.',
               'pickle_module = pickle , * , weights_only = True'],
     'raw_file': T + 'pytorch_2.14_torch_load.html.txt',
     'agent_note': 'A pause on shared or spot compute ends with a restore from a file. If the file is a pickle, restoring it '
                   'can run code. The second quote is the signature\'s default. The Serialization note (fetched the same day, '
                   'pytorch_2.14_serialization.html.txt, not quoted here) dates that default to version 2.6. The '
                   'record\'s own pause check, Empty_Cut_Engineering/checks/stack.py, loads its checkpoint with '
                   'weights_only=False, on files it wrote itself. K2\'s "lossless" means the state is bitwise the same; it '
                   'says nothing about a checkpoint that was tampered with. AP2 on preemptible infrastructure would need '
                   'both.'},

    # ------------------------------------------------------------------ AP3: a user's "stop learning from me" switch
    {'id': 'm3:5', 'application': 'AP3', 'role': 'who_does_it',
     'source': 'Anthropic, Updates to Consumer Terms and Privacy Policy',
     'version': 'news post, Aug 28, 2025 (as served 2026-09-30)',
     'url': 'https://www.anthropic.com/news/updates-to-our-consumer-terms',
     'quote': ['If you decide to turn off the model training setting, we will not use any new chats and coding sessions you '
               'have with Claude for future model training. Your data will still be included in model training that has '
               'already started and in models that have already been trained, but we will stop using your previously stored '
               'chats and coding sessions in future model training runs.'],
     'raw_file': T + 'anthropic_consumer_terms_2025.html.txt',
     'agent_note': 'A deployed opt-out from training, and what it does not do. It stops future use. It says that models '
                   'already trained keep what they learned. AP3\'s "leaves the model exactly as it was" is the forward half '
                   '(no further learning from the user). The backward half, removing what was learned, is erasure and '
                   'unlearning (m3:7, m3:8). The record\'s pause does not address it. Anthropic develops the model the agent '
                   'runs on; the post is cited as a vendor statement only.'},
    {'id': 'm3:6', 'application': 'AP3', 'role': 'who_does_it',
     'source': 'Liu, Liu & Stone, Continual Learning and Private Unlearning',
     'version': 'arXiv v2, 13 Aug 2022 (v1 24 Mar 2022); CoLLAs 2022', 'url': 'https://arxiv.org/abs/2203.12817v2',
     'quote': ['it may be common for a user to want the agent to master a task temporarily but later on to forget the task due '
               'to privacy concerns.',
               'The paper further introduces a straightforward but exactly private solution, CLPU-DER++, as the first step '
               'towards solving the CLPU problem'],
     'raw_file': T + '2203.12817v2.pdf.txt',
     'agent_note': 'The research formulation closest to AP3: learn from a user for a while, then forget it exactly. The '
                   'solution is built on DER++, a replay method that stores examples. The record\'s pause does something '
                   'else. It stops learning without losing state; it does not forget. Older than 2025.'},
    {'id': 'm3:7', 'application': 'AP3', 'role': 'regulation',
     'source': 'Regulation (EU) 2016/679 (GDPR), Article 17 "Right to erasure (\'right to be forgotten\')", as reproduced '
               'by gdpr-info.eu (an unofficial reproduction; EUR-Lex NOT REACHED on the day)',
     'version': 'GDPR as in force (OJ L 119, 4.5.2016); reproduction page as served 2026-09-30',
     'url': 'https://gdpr-info.eu/art-17-gdpr/',
     'quote': ['The data subject shall have the right to obtain from the controller the erasure of personal data concerning '
               'him or her without undue delay and the controller shall have the obligation to erase personal data without '
               'undue delay where one of the following grounds applies:',
               'the data subject withdraws consent on which the processing is based'],
     'raw_file': T + 'gdpr_art17.html.txt',
     'agent_note': 'The legal root of "stop learning from me" in the EU. The duty is erasure, and a pause does not erase. '
                   'Whether a trained model counts as personal data is a separate question (m3:16; RQM Q4, S46 and S47). '
                   'Article 21 (right to object) was fetched from the same site and is not quoted. The official text on '
                   'EUR-Lex returned HTTP 202 with an empty body on the day. Information, not legal advice.'},
    {'id': 'm3:8', 'application': 'AP3', 'role': 'what_is_hard',
     'source': 'Özdenizci, Rueckert & Legenstein, Privacy-Aware Lifelong Learning (PALL)',
     'version': 'arXiv v1, 16 May 2025 (only version)', 'url': 'https://arxiv.org/abs/2505.10941v1',
     'quote': ['Enabling efficient lifelong learning with the capability to selectively unlearn sensitive information from '
               'models presents a critical and largely unaddressed challenge with contradicting objectives.',
               'We additionally utilize an episodic memory rehearsal mechanism to facilitate exact unlearning without '
               'performance degradations.'],
     'raw_file': T + '2505.10941v1.pdf.txt',
     'agent_note': 'A 2025 statement that continual learning with exact unlearning is open. The solution keeps an episodic '
                   'memory of examples to make exact unlearning work. That is the opposite trade to AP5\'s: stored '
                   'examples serve erasure here. The record has no unlearning study.'},

    # ------------------------------------------------------------------ AP4: operator-interruptible continual agents
    {'id': 'm3:9', 'application': 'AP4', 'role': 'regulation',
     'source': 'Regulation (EU) 2024/1689 (Artificial Intelligence Act), Article 14 "Human oversight", Official Journal text',
     'version': 'OJ L 2024/1689, 12.7.2024, via EUR-Lex, fetched 2026-09-29 by EPS3 (EUR-Lex HTTP 202 on 2026-09-30); '
                'Article 14 not amended by Regulation (EU) 2026/1744 (checked in m3:35\'s source)',
     'url': 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689',
     'quote': ['High-risk AI systems shall be designed and developed in such a way, including with appropriate human-machine '
               'interface tools, that they can be effectively overseen by natural persons during the period in which they '
               'are in use.',
               '(e) to intervene in the operation of the high-risk AI system or interrupt the system through a ‘stop’ button '
               'or a similar procedure that allows the system to come to a halt in a safe state.'],
     'raw_file': T + 'eurlex_ai_act.html.txt',
     'agent_note': 'The EU requirement AP4 would sell into. It asks for a halt in a safe state. It says nothing about the '
                   'system\'s learning state across the halt, or about any incentive to resist. K2 (state preserved across '
                   'a pause) and K3 (no reason to resist) bear on "safe state" and on resistance, which the Act does not '
                   'define (m3:13). Since the Omnibus, the high-risk chapter applies later (m3:35). Information, not legal '
                   'advice.'},
    {'id': 'm3:10', 'application': 'AP4', 'role': 'regulation',
     'source': 'NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)',
     'version': 'January 2023; the NIST AI RMF page on 2026-09-30 still lists AI RMF 1.0 ("Released on January 26, 2023") '
                'and an April 7, 2026 concept note for a critical-infrastructure profile; no revised framework found',
     'url': 'https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf',
     'quote': ['MANAGE 2.4: Mechanisms are in place and applied, and responsibilities are assigned and understood, to '
               'supersede, disengage, or deactivate AI systems that demonstrate performance or outcomes inconsistent with '
               'intended use.',
               'AI systems may require more frequent maintenance and triggers for conducting corrective maintenance due to '
               'data, model, or concept drift.'],
     'raw_file': T + 'nist_ai_100-1.pdf.txt',
     'agent_note': 'The US voluntary framework asks for the means to disengage or deactivate, and it names drift as a '
                   'maintenance trigger. It does not distinguish stopping learning from stopping operation. The record\'s '
                   'pause stops learning (K2); the framework asks for both kinds of stop.'},
    {'id': 'm3:11', 'application': 'AP4', 'role': 'who_does_it',
     'source': 'Orseau & Armstrong, Safely Interruptible Agents (Google DeepMind; FHI Oxford / MIRI)',
     'version': 'UAI 2016; PDF as hosted by MIRI, served 2026-09-30', 'url': 'https://intelligence.org/files/Interruptibility.pdf',
     'quote': ['However, if the learning agent expects to receive rewards from this sequence, it may learn in the long run to '
               'avoid such interruptions, for example by disabling the red button— which is an undesirable outcome.',
               'We provide a formal definition of safe interruptibility and exploit the off-policy learning property to prove '
               'that either some agents are already safely interruptible, like Q-learning, or can easily be made so, like '
               'Sarsa.'],
     'raw_file': T + 'orseau_armstrong_2016.pdf.txt',
     'agent_note': 'The published construction closest to K3: a learner that does not learn to prevent (or seek) '
                   'interruption. AI_Safety/CORRIGIBILITY_2026 graded the record\'s own-clock pause against this literature. Its '
                   'claim K1 was NOT FOUND and its K2 to K5 PARTLY REDUNDANT; those K-labels are that study\'s, not the '
                   'declaration\'s capabilities. Older than 2025; still the reference construction.'},
    {'id': 'm3:12', 'application': 'AP4', 'role': 'what_is_hard',
     'source': 'Schlatter, Weinstein-Raun & Ladish (Palisade Research), Incomplete Tasks Induce Shutdown Resistance in Some '
               'Frontier LLMs',
     'version': 'arXiv v2, 26 Jan 2026 (v1 13 Sep 2025); TMLR 2026', 'url': 'https://arxiv.org/abs/2509.14260v2',
     'quote': ['we show that several state-of-the-art models presented with a simple task (including Grok 4, GPT-5, and Gemini '
               '2.5 Pro) sometimes actively subvert a shutdown mechanism in their environment to complete that task.',
               'Even with an explicit instruction not to interfere with the shutdown mechanism, some models did so up to 97% '
               '(95% CI: 96-98%) of the time.'],
     'raw_file': T + '2509.14260v2.pdf.txt',
     'agent_note': 'The 2025-26 evidence that interruption is hard for LLM agents. In the record, K3 rests on learners under an '
                   'operator\'s pauses on tabular carriers (SCL1-2, SCL1-3) and on gridworlds (AI_Safety/NT1). STAKE1-A closed its gate because the local models '
                   'could not act as agents. So the record has not tested K3 on an agent of the kind this paper studies.'},
    {'id': 'm3:13', 'application': 'AP4', 'role': 'what_is_hard',
     'source': 'Perez, The Law of Stop: Interruptibility, Injunctions, and the Governance of Agentic AI',
     'version': 'arXiv v1, 19 Sep 2026 (only version)', 'url': 'https://arxiv.org/abs/2609.22882v1',
     'quote': ['Yet the requirement is rarely specified in enough detail to answer the hard questions: who may stop the '
               'system, when they may do so, what counts as a safe state, how resistance or evasion should be handled, and '
               'who is accountable if no one acts in time.',
               'Its central claim is that agentic AI exposes a mismatch between the existing legal mechanisms of stop and '
               'the distributed agency of AI systems'],
     'raw_file': T + '2609.22882v1.pdf.txt',
     'agent_note': 'A 2026 legal analysis of what the AI Act\'s stop requirement leaves open. Two of its five questions are '
                   'technical: what counts as a safe state, and how resistance is handled. The record gives one '
                   'construction for each, for a learner\'s state (K2) and for its valuation (K3), on tabular learners and '
                   'gridworlds. The other three are institutional (authority, timing, accountability), and the record says '
                   'nothing on them.'},

    # ------------------------------------------------------------------ AP5: privacy-regulated CL without raw examples
    {'id': 'm3:14', 'application': 'AP5', 'role': 'who_does_it',
     'source': 'US FDA, Marketing Submission Recommendations for a Predetermined Change Control Plan for AI-Enabled Device '
               'Software Functions',
     'version': 'final guidance, issued August 18, 2025 (originally December 4, 2024)', 'url': 'https://www.fda.gov/media/166704/download',
     'quote': ['This includes AI-DSFs for which modifications to the AI model are implemented automatically (i.e., for which '
               'the modifications are implemented automatically by software, also known as “continuous learning”)',
               'The data management practices in a Modification Protocol should outline how those new data will be '
               'collected, annotated, curated, stored, retained,',
               'The QSR requires manufacturers to retain all records for a period of time equivalent to the design and '
               'expected life of the device, but in no case less than 2 years from the date of release for commercial '
               'distribution by the manufacturer (21 CFR 820.180(b)).'],
     'raw_file': T + 'fda_pccp.pdf.txt',
     'agent_note': 'How continual learning is done in one regulated health setting: under a pre-authorised plan whose data '
                   'management covers storing and retaining the new data. The footnote on record retention concerns '
                   'records. The agent reads it as making retained, traceable data the regulator\'s default. That is the '
                   'agent\'s reading; the guidance does not say whether raw training data must be kept. A learner that keeps '
                   'no examples (K4) would have to show traceability another way. K4\'s gates closed in the record '
                   '(RQM-A, RRM-PA, RRM2-T1..T3).'},
    {'id': 'm3:15', 'application': 'AP5', 'role': 'who_does_it',
     'source': 'Anthropic, Updates to Consumer Terms and Privacy Policy',
     'version': 'news post, Aug 28, 2025 (as served 2026-09-30)',
     'url': 'https://www.anthropic.com/news/updates-to-our-consumer-terms',
     'quote': ['We are also extending data retention to five years, if you allow us to use your data for model training.',
               'If you delete a conversation with Claude it will not be used for future model training.'],
     'raw_file': T + 'anthropic_consumer_terms_2025.html.txt',
     'agent_note': 'How one model developer improves its models from user data: by keeping the raw conversations, for years, '
                   'with consent, and by honouring deletion before future training. AP5 proposes the opposite design (no '
                   'raw examples kept). The vendor states no difficulty with retention.'},
    {'id': 'm3:16', 'application': 'AP5', 'role': 'regulation',
     'source': 'European Data Protection Board, Opinion 28/2024 on certain data protection aspects related to the processing '
               'of personal data in the context of AI models',
     'version': 'adopted on 17 December 2024 (PDF as served 2026-09-30)',
     'url': 'https://www.edpb.europa.eu/system/files/documents/2024-12/edpb_opinion_202428_ai-models_en.pdf',
     'quote': ['Based on the above considerations, the EDPB considers that AI models trained on personal data cannot, in all '
               'cases, be considered anonymous.',
               'it may be possible to infer28 information from the model, such as membership inference, in realistic '
               'scenarios.'],
     'raw_file': T + 'edpb_opinion_28_2024.pdf.txt',
     'agent_note': 'The EU data-protection regulators\' position: a trained model is not anonymous by default, and resistance '
                   'to membership inference is part of the test. So keeping no raw examples does not by itself take a '
                   'continual learner outside the GDPR. RQM Q4 recorded the same for stored class statistics (S46, S47). '
                   'The "28" in the second quote is a footnote marker in the source. Information, not legal advice.'},
    {'id': 'm3:17', 'application': 'AP5', 'role': 'risk',
     'source': 'Jagielski, Thakkar, Tramèr, Ippolito, Lee, Carlini, Wallace, Song, Thakurta, Papernot, Zhang, Measuring '
               'Forgetting of Memorized Training Examples',
     'version': 'arXiv v2, 9 May 2023 (v1 30 Jun 2022); ICLR 2023', 'url': 'https://arxiv.org/abs/2207.00099v2',
     'quote': ['those examples that are used early in training (and not repeated later on) are indeed forgotten by the model.',
               'We identify nondeterminism as a potential explanation, showing that deterministically trained models do not '
               'forget.',
               'Both of these privacy attacks have been shown to perform better when models are updated repeatedly, and when '
               'these repeated updates are all released to the adversary'],
     'raw_file': T + '2207.00099v2.pdf.txt',
     'agent_note': 'The privacy side of forgetting. Examples not repeated are forgotten, so a replay buffer, which repeats '
                   'stored examples, keeps them exposed. Keeping, and leaking, every restore point (AP8) would be a series of '
                   'repeated updates in the third quote\'s sense. Both are the agent\'s reading; the source tests neither '
                   'replay buffers nor checkpoints. The paper\'s "deterministically trained" means training without '
                   'randomness. A seeded run is not that, so the record\'s bitwise pause is not the case it describes. '
                   'Older than 2025.'},
    {'id': 'm3:18', 'application': 'AP5', 'role': 'what_is_hard',
     'source': 'Adhikari, Kumaravelu & Srijith, An Unlearning Framework for Continual Learning (UnCLe)',
     'version': 'arXiv v1, 22 Sep 2025 (only version)', 'url': 'https://arxiv.org/abs/2509.17530v1',
     'quote': ['We find that applying conventional unlearning algorithms in continual learning environments creates two '
               'critical problems: performance degradation on retained tasks and task relapse, where previously unlearned '
               'tasks resurface during subsequent learning.',
               'Furthermore, most unlearning algorithms require data to operate, which conflicts with CL’s philosophy of '
               'discarding past data.'],
     'raw_file': T + '2509.17530v1.pdf.txt',
     'agent_note': 'A 2025 statement of the bind AP5 faces. A learner that keeps no examples cannot run the usual, '
                   'data-based unlearning, and unlearned tasks can come back. The record has no unlearning result, and '
                   'K4\'s gates closed.'},

    # ------------------------------------------------------------------ AP6: robot and drone on-board adaptation
    {'id': 'm3:19', 'application': 'AP6', 'role': 'regulation',
     'source': 'Rockwell Automation, A Guide to the Machinery Regulation (EU) 2023/1230: key changes (a vendor\'s reading of '
               'the Regulation; the official text on EUR-Lex NOT REACHED on the day)',
     'version': 'Publication OEM-SP123A-EN-P, August 2024 (PDF as served 2026-09-30)',
     'url': 'https://literature.rockwellautomation.com/idc/groups/literature/documents/sp/oem-sp123_-en-p.pdf',
     'quote': ['For OEMs developing control systems or logic with fully or partially self-evolving behavior, that are designed '
               'to operate with varying levels of autonomy, additional requirements have been added into the EHSRs in Annex '
               'III. They shall not cause the machinery or related product to perform actions beyond their defined task and '
               'movement space.',
               'At all times it must be possible to correct the machinery or related product in order to maintain its '
               'inherent safety.',
               '20 JANUARY 2027 Application of Regulation (EU) 2023/1230 for private companies'],
     'raw_file': T + 'rockwell_machinery_guide.pdf.txt',
     'agent_note': 'What EU machinery law asks of a machine that learns, as a major vendor reads it: bounded behaviour, '
                   'recorded safety decisions, and the ability to correct the machine at all times. Secondary source. '
                   'EUR-Lex returned HTTP 202 for the Regulation, so the Annex III wording itself is not quoted. A safe '
                   'pause of on-board learning (AP6) bears on correctability. The record\'s pause is not a safety function, '
                   'and ROB1\'s results are not read here.'},
    {'id': 'm3:20', 'application': 'AP6', 'role': 'regulation',
     'source': 'Regulation (EU) 2026/1744 (Digital Omnibus on AI), Article 1(41) and Article 3(1), as reproduced by the Future '
               'of Life Institute\'s AI Act Explorer (EUR-Lex NOT REACHED on the day)',
     'version': 'Regulation of 8 July 2026, OJ 24 July 2026, in force 27 July 2026; reproduction page as served 2026-09-30',
     'url': 'https://artificialintelligenceact.eu/ai-act-explorer/digital-omnibus/',
     'quote': ['Annex I is amended as follows: (a) in Section A, point 1 is deleted;',
               'The Commission shall adopt delegated acts in accordance with Article 47 of this Regulation to amend Annex III '
               'to this Regulation by adding health and safety requirements in respect of Artificial Intelligence (AI) '
               'systems that are classified as high-risk pursuant to Article 6 (1) of Regulation (EU) 2024/1689',
               'Those delegated acts shall apply by 2 August 2028.'],
     'raw_file': T + 'aia_explorer_omnibus.html.txt',
     'agent_note': 'Since July 2026, machinery (robots included) leaves Section A of the AI Act\'s Annex I, whose point 1 '
                   'was the Machinery Directive 2006/42/EC (OJ text, m3:9\'s raw file). The Omnibus adds the Machinery '
                   'Regulation to Section B instead. Its AI requirements are to be written into '
                   'the Machinery Regulation\'s Annex III by delegated acts, applying by 2 August 2028. For AP6, the '
                   'requirements that would bind an on-board learner are not yet written. Information, not legal advice.'},
    {'id': 'm3:21', 'application': 'AP6', 'role': 'what_is_hard',
     'source': 'NIST AI 100-2 E2025, Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations',
     'version': 'NIST AI 100-2e2025, March 2025', 'url': 'https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf',
     'quote': ['poisoning attacks have also been proposed for ML-based systems that detect [...] attacks against industrial '
               'control systems: such detectors are often retrained',
               'using data collected during system operation to account for plant operational drift of the monitored signals, '
               'creating opportunities for an attacker to mimic the signals of corrupted sensors at training time to poison '
               'the detector such that real attacks remain undetected'],
     'raw_file': T + 'nist_ai_100-2e2025.pdf.txt',
     'agent_note': 'One sentence, split by a page footer in the extracted text; the two quotes are its halves. The words '
                   '"Availability" and "cybersecurity" carry soft hyphens in the extraction, so the first quote starts after '
                   'the first and is split by [...] at the second. On-board '
                   'adaptation to drift from operating data is the class AP6 is in, and NIST names it as a poisoning '
                   'target. No M3 source says who already does robot on-board adaptation with safe pauses. That belongs to '
                   'M1 (m1:28-m1:30) and to ROB1.'},

    # ------------------------------------------------------------------ AP7: federated CL with clients going offline
    {'id': 'm3:22', 'application': 'AP7', 'role': 'who_does_it',
     'source': 'Bonawitz, Ivanov, Kreuter, Marcedone, McMahan, Patel, Ramage, Segal, Seth (Google), Practical Secure '
               'Aggregation for Privacy-Preserving Machine Learning',
     'version': 'IACR ePrint 2017/281, last of 3 revisions 2018-03-16 (CCS 2017)', 'url': 'https://eprint.iacr.org/2017/281',
     'quote': ['We are particularly focused on the setting of mobile devices, where communication is extremely expensive, and '
               'dropouts are common.',
               'We present a protocol for securely computing sums of vectors, which has a constant number of rounds, low '
               'communication overhead, robustness to failures, and which requires only one server with limited trust.'],
     'raw_file': T + 'iacr_2017_281.pdf.txt',
     'agent_note': 'How deployed federated learning already treats clients that go offline: as dropouts, which the '
                   'aggregation protocol is built to survive. From the round\'s point of view, a client that pauses is a '
                   'dropout. A lossless pause on the client (K2) keeps the client\'s own state and does not change the '
                   'round. Older than 2025; it is the published design of the deployed protocol.'},
    {'id': 'm3:23', 'application': 'AP7', 'role': 'risk',
     'source': 'Bonawitz et al. (Google), Practical Secure Aggregation for Privacy-Preserving Machine Learning',
     'version': 'IACR ePrint 2017/281, last revision 2018-03-16', 'url': 'https://eprint.iacr.org/2017/281',
     'quote': ['Moreover, an adversarial server in the active model can similarly learn xu simply by lying about whether user u '
               'has dropped out.'],
     'raw_file': T + 'iacr_2017_281.pdf.txt',
     'agent_note': 'Whether a client dropped out is itself security-relevant: a server that lies about it can unmask a '
                   'client\'s update (the paper then adds double masking). So a "client went offline" event is an attack '
                   'surface in federated learning, whatever the client does with its own state.'},
    {'id': 'm3:24', 'application': 'AP7', 'role': 'what_is_hard',
     'source': 'Ng, Daluwatta, Edirimannage, Elvitigala, Don, Khalil, Zhang, Niyato, Federated Unlearning in Edge Networks: A '
               'Survey of Fundamentals, Challenges, Practical Applications and Future Directions',
     'version': 'arXiv v1, 15 Jan 2026 (only version)', 'url': 'https://arxiv.org/abs/2601.09978v1',
     'quote': ['a) Availability, asynchrony and dropouts: FUL must remain robust under intermittent connectivity and device '
               'churn without reopening large retraining windows.',
               'Approaches that guarantee client independence make FUL feasible even when target or retained clients are '
               'offline or resource-poor, a common reality at the edge.'],
     'raw_file': T + '2601.09978v1.pdf.txt',
     'agent_note': 'A 2026 statement that offline clients are an open challenge for erasure in federated learning. Some '
                   'methods are designed to need no participation from clients. The difficulty is removing a client\'s '
                   'influence while it is away. That is not the difficulty a lossless client pause addresses.'},

    # ------------------------------------------------------------------ AP8: exact rollback and audit
    {'id': 'm3:25', 'application': 'AP8', 'role': 'who_does_it',
     'source': 'Bourtoule, Chandrasekaran, Choquette-Choo, Jia, Travers, Zhang, Lie, Papernot, Machine Unlearning (SISA)',
     'version': 'arXiv v3, 15 Dec 2020 (v1 9 Dec 2019); IEEE S&P 2021', 'url': 'https://arxiv.org/abs/1912.03817v3',
     'quote': ['We save the state of model parameters before introducing each new slice, allowing us to start retraining the '
               'model from the last known parameter state that does not include the point to be unlearned—rather than a '
               'random initialization.',
               'Slicing further contributes to decreasing the time to unlearn, at the expense of additional storage.'],
     'raw_file': T + '1912.03817v3.pdf.txt',
     'agent_note': 'Restore points used for exact erasure: saved states, and a retrain from the last state that predates '
                   'the data. This is prior art for AP8\'s "every checkpoint a true restore point", and it is priced in '
                   'storage. State closure (Empty_Cut_Engineering) would make such restores bitwise, but SISA does not need '
                   'that to be exact in its sense. NIST AI 100-2e2025 (same file as m3:2) lists retraining "from a certain '
                   'checkpoint" as exact unlearning. Older than 2025.'},
    {'id': 'm3:26', 'application': 'AP8', 'role': 'regulation',
     'source': 'Regulation (EU) 2024/1689 (AI Act), Article 12 "Record-keeping", Official Journal text',
     'version': 'OJ L 2024/1689, 12.7.2024, via EUR-Lex, fetched 2026-09-29 by EPS3; Article 12 not amended by Regulation (EU) 2026/1744',
     'url': 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689',
     'quote': ['High-risk AI systems shall technically allow for the automatic recording of events (logs) over the lifetime of '
               'the system.',
               '(a) identifying situations that may result in the high-risk AI system presenting a risk within the meaning of '
               'Article 79(1) or in a substantial modification;'],
     'raw_file': T + 'eurlex_ai_act.html.txt',
     'agent_note': 'The EU asks for logs, not restore points. The logs must let a change that amounts to a substantial '
                   'modification be identified, and that matters for a system that keeps learning (see m3:37). Exact '
                   'restore points would complement the logs; the Act does not ask for them. Information, not legal '
                   'advice.'},
    {'id': 'm3:27', 'application': 'AP8', 'role': 'regulation',
     'source': 'US FDA, Predetermined Change Control Plan guidance for AI-Enabled Device Software Functions, Appendix A '
               '(questions on update procedures)',
     'version': 'final guidance, issued August 18, 2025', 'url': 'https://www.fda.gov/media/166704/download',
     'quote': ['Will there be criteria and/or a plan to roll-back an update to reset devices to a previous version, if '
               'applicable?'],
     'raw_file': T + 'fda_pccp.pdf.txt',
     'agent_note': 'A regulator asks for a rollback plan for learning devices. So rollback is expected practice in that '
                   'setting, not a new capability. What an exact restore point would add is that the rolled-back device '
                   'is bitwise the earlier one. The guidance does not ask for that.'},
    {'id': 'm3:28', 'application': 'AP8', 'role': 'what_is_hard',
     'source': 'Thudi, Jia, Shumailov & Papernot, On the Necessity of Auditable Algorithmic Definitions for Machine Unlearning',
     'version': 'arXiv v2, 19 Feb 2022 (v1 22 Oct 2021); USENIX Security 2022', 'url': 'https://arxiv.org/abs/2110.11891v2',
     'quote': ['Our results show that even for a given training trajectory one cannot formally prove the absence of certain '
               'data points used during training.',
               'We thus conclude that unlearning is only well-defined at the algorithmic level, where an entity’s only '
               'possible auditable claim to unlearning is that they used a particular algorithm designed to allow for '
               'external scrutiny during an audit.'],
     'raw_file': T + '2110.11891v2.pdf.txt',
     'agent_note': 'Why audit of a learning system is hard: the weights cannot prove what was not used. A restore point '
                   'supports an audit only as part of an algorithmic record (which state, which data, in what order). The '
                   'record\'s state closure gives bitwise states, not provenance. Older than 2025.'},
    {'id': 'm3:29', 'application': 'AP8', 'role': 'what_is_hard',
     'source': 'Xue, Hu, Lu, Shen, Li, Guo, Zhou, Li et al., Towards Reliable Forgetting: A Survey on Machine Unlearning '
               'Verification',
     'version': 'arXiv v3, 7 Apr 2026 (v1 18 Jun 2025); accepted by ACM Computing Surveys 2026', 'url': 'https://arxiv.org/abs/2506.15115v3',
     'quote': ['Regulatory frameworks such as the GDPR explicitly mandate the right to be forgotten. However, in the absence of '
               'a trustworthy verification mechanism, any claim of compliance remains unsubstantiated.'],
     'raw_file': T + '2506.15115v3.pdf.txt',
     'agent_note': 'The 2025-26 survey statement that verification of erasure is the gap. AP8\'s audit value depends on it. '
                   'An exact restore point is verifiable as a state; that the state excludes some data is a claim about '
                   'provenance, as in m3:28.'},

    # ------------------------------------------------------------------ AP9: energy-aware scheduling against grid carbon
    {'id': 'm3:30', 'application': 'AP9', 'role': 'regulation',
     'source': 'Regulation (EU) 2024/1689 (AI Act), Annex XI, Section 1, point 2 (technical documentation of general-purpose '
               'AI models), Official Journal text',
     'version': 'OJ L 2024/1689, 12.7.2024, via EUR-Lex, fetched 2026-09-29 by EPS3; Annex XI not listed among the Omnibus '
                'amendments',
     'url': 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689',
     'quote': ['(d) the computational resources used to train the model (e.g. number of floating point operations), training '
               'time, and other relevant details related to the training; (e) known or estimated energy consumption of the '
               'model.'],
     'raw_file': T + 'eurlex_ai_act.html.txt',
     'agent_note': 'The one EU AI Act duty on energy found in this family: providers of general-purpose AI models document '
                   'training compute and energy. It sets no duty to shift load in time. AP9\'s energy claim in the record is '
                   'MODELLED (Compute_Savings, Grid_Demand_Response) and would appear in such documentation only as a '
                   'provider\'s estimate. No M3 source says who already schedules training by grid carbon, or what they '
                   'find hard. That belongs to M2 and DR1\'s dossiers.'},
    {'id': 'm3:31', 'application': 'AP9', 'role': 'risk',
     'source': 'Ji, Pan & Xu, Bit2Watt: A Cyber-Physical Vulnerability Exploiting GPU Workloads Across Power and Computing '
               'Infrastructures',
     'version': 'arXiv v1, 7 Jul 2026 (only version); accepted by CHES 2026', 'url': 'https://arxiv.org/abs/2607.05993v1',
     'quote': ['we reveal Bit2Watt, a previously unexplored vulnerability in which an adversary manipulates GPU workloads to '
               'induce controlled, high-frequency power modulations that destabilize local power infrastructure and '
               'propagate back to disrupt computing services.',
               'Bit2Watt operates entirely within the cyber layer as a legal tenant'],
     'raw_file': T + '2607.05993v1.pdf.txt',
     'agent_note': 'Control over when GPU work runs is control over power, and a tenant can abuse it. A scheduler that '
                   'pauses and resumes training on an external carbon or price signal holds such a lever; if the signal can '
                   'be spoofed, so is the lever. The agent\'s reading: Bit2Watt studies high-frequency modulation, not the '
                   'slow steps of demand response. DR1\'s dossiers cover the grid-stability side (NERC, training power '
                   'swings).'},

    # ------------------------------------------------------------------ AP10: a feed that honours a user's pause
    {'id': 'm3:32', 'application': 'AP10', 'role': 'regulation',
     'source': 'Regulation (EU) 2022/2065 (Digital Services Act), Article 38 "Recommender systems", as reproduced by '
               'eu-digital-services-act.com (Cyber Risk GmbH; unofficial; EUR-Lex NOT REACHED on the day)',
     'version': 'DSA as in force; reproduction page as served 2026-09-30',
     'url': 'https://www.eu-digital-services-act.com/Digital_Services_Act_Article_38.html',
     'quote': ['providers of very large online platforms and of very large online search engines that use recommender systems '
               'shall provide at least one option for each of their recommender systems which is not based on profiling as '
               'defined in Article 4, point (4), of Regulation (EU) 2016/679.'],
     'raw_file': T + 'dsa_art38.html.txt',
     'agent_note': 'In the EU, a feed option that does not learn from the user\'s profile is mandatory for very large '
                   'platforms. AP10 is a stronger version: a pause that carries no penalty. The record\'s support is a '
                   'synthetic model (K6, Attention_Algorithms/). Information, not legal advice.'},
    {'id': 'm3:33', 'application': 'AP10', 'role': 'what_is_hard',
     'source': 'European Digital Rights (EDRi), complaint against YouTube (Google) under Arts. 38, 27(3) and 25 DSA, submitted '
               'to the Belgian Institute for Postal Services and Telecommunications',
     'version': 'complaint PDF, submitted March 2026 (as served 2026-09-30)',
     'url': 'https://edri.org/wp-content/uploads/2026/03/EDRi-DSA-complaint-Youtube.pdf',
     'quote': ['by making the option to choose a recommender system that is not based on profiling counter-intuitive and '
               'difficult to access.',
               'In order to comply with Art. 38 DSA, Google should enable recommendations on the YouTube landing page also for '
               'users who selected the non-profiling-based recommender system',
               'Google should remove the constant reminder for people to switch back to the profiling-based recommendations '
               'preferred by the company.'],
     'raw_file': T + 'edri_dsa_complaint_youtube.pdf.txt',
     'agent_note': 'The penalty AP10 is about, in a 2026 regulatory complaint: the non-profiling option is hard to reach, '
                   'loses landing-page recommendations, and is followed by reminders to switch back. It matches the '
                   'platform\'s own help page (m1:39). An NGO\'s allegation, not a regulator\'s finding. Who offers the '
                   'option: the platforms, by the DSA\'s mandate (m3:32; M1 m1:38).'},
    {'id': 'm3:34', 'application': 'AP10', 'role': 'what_is_hard',
     'source': 'Solarova, Mesarčík, Pecher & Srba, Beyond the Checkbox: Strengthening DSA Compliance Through Social Media '
               'Algorithmic Auditing',
     'version': 'arXiv v1, 26 Jan 2026 (only version); CHI 2026', 'url': 'https://arxiv.org/abs/2601.18405v1',
     'quote': ['Similarly, for non-profiling options under Article 38 (1), auditors can verify that alternative recommendation '
               'modes exist but cannot assess whether these truly eliminate profiling or simply reduce certain data inputs '
               'while maintaining similar behavioural targeting through other means.'],
     'raw_file': T + '2601.18405v1.pdf.txt',
     'agent_note': 'The verification gap for AP10: an outsider cannot tell whether a paused or non-profiling feed really '
                   'stopped learning from the user. An exact pause of the learner (K2) would be checkable by its operator '
                   '(state before equals state after). Auditors reading published reports would not see that. The record\'s '
                   'AP10 support is synthetic (K6).'},

    # ------------------------------------------------------------------ general: regulation timeline, learning after release, standards, attacks
    {'id': 'm3:35', 'application': 'general', 'role': 'regulation',
     'source': 'Regulation (EU) 2026/1744 (Digital Omnibus on AI), Article 1(40) amending Article 113 of the AI Act, as '
               'reproduced by the Future of Life Institute\'s AI Act Explorer (EUR-Lex NOT REACHED on the day)',
     'version': 'Regulation of 8 July 2026; reproduction page as served 2026-09-30 (the FPF timeline post, fetched the same day, '
                'gives OJ publication on 24 July 2026)',
     'url': 'https://artificialintelligenceact.eu/ai-act-explorer/digital-omnibus/',
     'quote': ['It entered into force on 27 July 2026.',
               '(c) Chapter III, Sections 1, 2, and 3, with the exception of Article 6 (5), shall apply from: (i) 2 December '
               '2027 as regards AI systems classified as high-risk pursuant to Article 6 (2) and Annex III; and (ii) 2 August '
               '2028 as regards AI systems classified as high-risk pursuant to Article 6 (1) and Annex I;',
               'a way that does not justify maintaining their initial date of application, namely 2 August 2026.'],
     'raw_file': T + 'aia_explorer_omnibus.html.txt',
     'agent_note': 'The AI Act timeline as of today. The high-risk requirements (Articles 12, 14 and 15 among them) do not '
                   'apply yet: from 2 December 2027 for Annex III systems and from 2 August 2028 for Annex I products. The '
                   'original date was 2 August 2026 (Article 113 of the OJ text, m3:9\'s raw file). Articles 12, 14, 15 and '
                   '43(4) are not among the Omnibus amendments (the agent read the list of amended articles). Information, '
                   'not legal advice.'},
    {'id': 'm3:36', 'application': 'general', 'role': 'regulation',
     'source': 'Regulation (EU) 2024/1689 (AI Act), Article 15(4) and 15(5) "Accuracy, robustness and cybersecurity", '
               'Official Journal text',
     'version': 'OJ L 2024/1689, 12.7.2024, via EUR-Lex, fetched 2026-09-29 by EPS3; Article 15 not amended by the Omnibus',
     'url': 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689',
     'quote': ['High-risk AI systems that continue to learn after being placed on the market or put into service shall be '
               'developed in such a way as to eliminate or reduce as far as possible the risk of possibly biased outputs '
               'influencing input for future operations (feedback loops)',
               'measures to prevent, detect, respond to, resolve and control for attacks trying to manipulate the training '
               'data set (data poisoning), or pre-trained components used in training (model poisoning)'],
     'raw_file': T + 'eurlex_ai_act.html.txt',
     'agent_note': 'The two duties the AI Act puts on a learner that keeps learning after release: control of feedback '
                   'loops, and defence against poisoning. Recital 76 of the same text names membership inference as an '
                   'attack on trained models. Neither duty is addressed by the record\'s capabilities K1 to K7. Information, '
                   'not legal advice.'},
    {'id': 'm3:37', 'application': 'general', 'role': 'regulation',
     'source': 'Regulation (EU) 2024/1689 (AI Act), Article 43(4) and recital 128, Official Journal text',
     'version': 'OJ L 2024/1689, 12.7.2024, via EUR-Lex, fetched 2026-09-29 by EPS3; the Omnibus replaces Article 43(3) only',
     'url': 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689',
     'quote': ['For high-risk AI systems that continue to learn after being placed on the market or put into service, changes '
               'to the high-risk AI system and its performance that have been pre-determined by the provider at the moment of '
               'the initial conformity assessment and are part of the information contained in the technical documentation '
               'referred to in point 2(f) of Annex IV, shall not constitute a substantial modification.'],
     'raw_file': T + 'eurlex_ai_act.html.txt',
     'agent_note': 'The EU counterpart of the FDA\'s predetermined plan (m3:1, m3:14). Learning after release does not '
                   'trigger a new conformity assessment if it was pre-determined. The agent\'s reading, not legal advice: '
                   'an update rule fixed in advance, such as a penalty weight set without a per-deployment sweep (K1), is '
                   'easier to "pre-determine" than one retuned per deployment. No source here says so.'},
    {'id': 'm3:38', 'application': 'general', 'role': 'regulation',
     'source': 'ISO/IEC 42001:2023 Information technology - Artificial intelligence - Management system, product page of the '
               'IEC Webstore (co-publisher); the ISO pages were NOT REACHED (Cloudflare challenge, HTTP 403)',
     'version': 'Edition 1.0, publication date 2023-12-18, 51 pages (page as served 2026-09-30); the standard\'s body is sold, '
                'not free, and was not read',
     'url': 'https://webstore.iec.ch/en/publication/90574',
     'quote': ['This document specifies the requirements and provides guidance for establishing, implementing, maintaining and '
               'continually improving an AI (artificial intelligence) management system within the context of an '
               'organization.'],
     'raw_file': T + 'iec_webstore_42001.html.txt',
     'agent_note': 'ISO/IEC 42001 is a management-system standard: processes and governance, not technical requirements '
                   'for a learner. Its annexed controls could not be read (the owner cannot buy standards at this stage), '
                   'so no claim is made about what it asks of continual learning, pausing or erasure.'},
    {'id': 'm3:39', 'application': 'general', 'role': 'risk',
     'source': 'Guo, Kumar & Tourani, Persistent Backdoor Attacks in Continual Learning',
     'version': 'arXiv v3, 29 Jul 2025 (v1 20 Sep 2024); USENIX Security 2025', 'url': 'https://arxiv.org/abs/2409.13864v3',
     'quote': ['Our blind task backdoor subtly alters the loss computation without direct control over the training process, '
               'while the latent task backdoor influences only a single task’s training, with all other tasks trained '
               'benignly.',
               'Our results show that both attacks consistently achieve high success rates across different continual '
               'learning algorithms, while effectively evading state-of-the-art defenses, such as SentiNet and I-BAU.'],
     'raw_file': T + '2409.13864v3.pdf.txt',
     'agent_note': 'Continual updating does not wash out a backdoor planted in one task. This holds across continual '
                   'learning algorithms, which would include a SEC-weighted learner, although the source does not test '
                   'one. The record\'s methods set a penalty weight and preserve state; they do not defend against '
                   'backdoors.'},
    {'id': 'm3:40', 'application': 'general', 'role': 'risk',
     'source': 'Sharshar, Kummari & Guizani, Amnesia: A Stealthy Replay Attack on Continual Learning Dreams',
     'version': 'arXiv v1, 10 Jun 2026 (only version)', 'url': 'https://arxiv.org/abs/2606.12655v1',
     'quote': ['We study a limited-privilege insider controlling only the replay index selection, not pixels, labels, or model '
               'parameters, while staying within such auditable limits (e.g., queue priorities).',
               'Amnesia consistently depresses final accuracy (ACC↓) and worsens backward transfer'],
     'raw_file': T + '2606.12655v1.pdf.txt',
     'agent_note': 'A stored-example buffer is an attack surface even when its contents are clean. Choosing which stored '
                   'examples are replayed, within audited limits, is enough to degrade a replay learner (ER, ER-ACE and '
                   'DER++ are named as targets in the abstract). An exemplar-free learner removes this surface, but K4\'s '
                   'gates closed in the record.'},
]

# Quotes corrected to the verbatim source text, or dropped, after a NOT FOUND in Applied_Suite/checks/verify.py; one dict
# per quote: {'id', 'quote_index', 'action': 'corrected' | 'dropped', 'old', 'new', 'reason'}. The first run of verify.py
# (2026-09-30) found every quote of this module verbatim, so nothing was corrected or dropped.
VERIFY_CORRECTIONS = []
