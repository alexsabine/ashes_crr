"""Claims for Grid_Demand_Response/DECLARATION.md section 1 (positions G1-G9), transcribed from the five verified dossiers
docs/citations/dr1_f1..f5_2026-09-29.md (fetched 2026-09-29/30; raw extracted texts under /tmp/claude-0/dr1_src/F1..F5/, outside
the repository: third-party full texts).

One dict per claim. 'quote' holds verbatim blockquotes copied from the dossier ("[...]" marks the dossier's own omissions);
verify.py checks every fragment against 'raw_file'. 'reading' (states / close / bears / contradicts) is the grading agent's,
decided from the quote against the declared position, for the investigator's review ('reading_by'); 'proposed_reading' is the
reading the literature family proposed for the same claim, kept so that grade.py can print the grades under both. Where the two
differ, 'agent_note' says why. G4 claims carry 'part' ('extension' or 'tiers'), because the declaration gives G4 two expected
grades. Tags 'DEF-*' are definition claims, not G positions; grade.py lists them but does not grade them.
Data only: no computation happens here.
"""

CLAIMS = [{'id': 'F1:0',
  'family': 'F1',
  'tag': 'G1',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': "Google blog, Terrell, 'A new milestone for smart, affordable electricity growth'",
  'title': 'Google, "A new milestone for smart, affordable electricity growth" (Terrell, 2026)',
  'version': 'blog post by Michael Terrell, dated Mar 19, 2026 (datePublished 2026-03-19), fetched 2026-09-29.',
  'url': 'https://blog.google/innovation-and-ai/infrastructure-and-cloud/global-network/demand-response-data-center-milestone/',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['We’ve now integrated a total of 1 gigawatt (GW) of demand response capacity into our long-term energy '
            'contracts with multiple utilities across the U.S.',
            'Google’s demand response capability allows us to limit or shift a portion of machine learning (ML) workloads '
            'running in our data centers. This reduces the overall data center power demand, helping to stabilize the grid '
            'during certain hours or times of the year.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/google_1gw_2026.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('states')."},
 {'id': 'F1:1',
  'family': 'F1',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Google blog, Terrell 2026',
  'title': 'Google, "A new milestone for smart, affordable electricity growth" (Terrell, 2026)',
  'version': 'blog post by Michael Terrell, dated Mar 19, 2026 (datePublished 2026-03-19), fetched 2026-09-29.',
  'url': 'https://blog.google/innovation-and-ai/infrastructure-and-cloud/global-network/demand-response-data-center-milestone/',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['Since announcing initial agreements with Indiana Michigan Power (I&M) and Tennessee Valley Authority (TVA) '
            'last year, we’ve signed contracts with Entergy Arkansas, Minnesota Power and DTE Energy that incorporate '
            'demand response as a key resource for new data centers to connect more rapidly to local grids.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/google_1gw_2026.html.txt',
  'agent_note': "Faster connection is called 'a key resource' for new data centres; the post does not rank it above event "
                'payments or call it the main value, so the named difference is the ranking G8 asserts. Family proposal '
                "'states' lowered to 'close' (the dossier's re-verified reading agrees)."},
 {'id': 'F1:2',
  'family': 'F1',
  'tag': 'G1',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': "Google blog, Terrell, 'How we're making data centers more flexible to benefit power grids'",
  'title': 'Google, "How we\'re making data centers more flexible to benefit power grids" (Terrell, 2025)',
  'version': 'blog post by Michael Terrell (Head of Advanced Energy), page metadata datePublished 2025-08-04, dateModified '
             '2026-01-07. Requested at which redirects to fetched ...',
  'url': 'https://blog.google/inside-google/infrastructure/how-were-making-data-centers-more-flexible-to-benefit-power-grids/',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['These agreements represent the first time we’re delivering data center demand response by targeting machine '
            'learning (ML) workloads. This builds on our successful demonstration with Omaha Public Power District (OPPD) '
            'where we reduced the power demand associated with ML workloads during three grid events last year'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/google_terrell_2025.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('states')."},
 {'id': 'F1:3',
  'family': 'F1',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Google blog, Terrell 2025',
  'title': 'Google, "How we\'re making data centers more flexible to benefit power grids" (Terrell, 2025)',
  'version': 'blog post by Michael Terrell (Head of Advanced Energy), page metadata datePublished 2025-08-04, dateModified '
             '2026-01-07. Requested at which redirects to fetched ...',
  'url': 'https://blog.google/inside-google/infrastructure/how-were-making-data-centers-more-flexible-to-benefit-power-grids/',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['These capabilities, often referred to as demand response, have several advantages, especially as we continue '
            'to see electricity growth in the US and elsewhere. It allows large electricity loads like data centers to be '
            'interconnected more quickly, helps reduce the need to build new transmission and power plants, and helps grid '
            'operators more effectively and efficiently manage power grids.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/google_terrell_2025.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('close')."},
 {'id': 'F1:4',
  'family': 'F1',
  'tag': 'G3',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': "Google Cloud blog, Mehra & Hasegawa, 'Supporting power grids with demand response at Google data centers'",
  'title': 'Google Cloud, "Supporting power grids with demand response at Google data centers" (Mehra & Hasegawa, 2023)',
  'version': 'Google Cloud Blog, October 3, 2023, fetched 2026-09-29.',
  'url': 'https://cloud.google.com/blog/products/infrastructure/using-demand-response-to-reduce-data-center-power-consumption',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['This alert activates an algorithm that generates hour-by-hour instructions for specified data centers to limit '
            'non-urgent compute tasks for the duration of the grid event, and allows them to be rescheduled after the grid '
            'event has passed.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/google_cloud_2023.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F1:5',
  'family': 'F1',
  'tag': 'G4',
  'part': 'tiers',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Radovanovic et al., Carbon-Aware Computing for Datacenters (Google)',
  'title': 'Radovanović et al., "Carbon-Aware Computing for Datacenters" (Google)',
  'version': 'arXiv:2106.11750 v1 (Fri, 11 Jun 2021)',
  'url': 'https://arxiv.org/abs/2106.11750',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['VCCs impose hourly limits on resources available to temporally ﬂexible workloads while preserving overall '
            'daily capacity, enabling all such workloads to complete within a day.',
            'the system harnesses the temporal ﬂexibility of a signiﬁcant fraction of Google’s internal workloads that '
            'tolerate delays as long as their work gets completed within 24 hours. Typical examples of such workloads are '
            'data compaction, machine learning, simulation, and data processing (e.g., video processing) pipelines'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/radovanovic_2106.11750v1.pdf.txt',
  'agent_note': "Read against G4's tiers clause: a fixed 24-hour completion window for flexible work (ML included) is a "
                'pre-agreed bound on the time axis, close to a tier (named difference: a time window, not a '
                'throughput-reduction tier). It does not move with the delay imposed, so it is not the extension.'},
 {'id': 'F1:6',
  'family': 'F1',
  'tag': 'G2',
  'reading': 'bears',
  'proposed_reading': 'contradicts',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'IURC Cause No. 46276, CAC Exhibit 1 (Mellinger testimony, public redacted)',
  'title': 'IURC Cause No. 46276: direct testimony of Dan Mellinger for the Citizens Action Coalition (public, redacted)',
  'version': '"CAC Exhibit 1 (Redacted)", Cause No. 46276 (I&M petition for a customer-specific Clean Capacity Arrangement '
             'and Demand Response contract), IURC online portal, (file ...',
  'url': 'https://iurc.portal.in.gov/_entity/sharepointdocumentlocation/92daa416-4ab0-f011-bbd3-001dd80846ac/bb9c6bba-fd52-45ad-8e64-a444aef13c39?file=CN+46276--+CAC+PUBLIC+Exhibit+1--10-23-25FINAL.pdf',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['For each event failure, I&M will assess an event failure charge of % of the annual [...] Interruptible Demand '
            'Credit for the failed events, [...] or % of the total Demand Credit.',
            'This exposure grows as the PJM capacity prices increase, since [...] the DRPS credits (and thus the associated '
            'penalty) are calculated using the',
            'The DRPS mechanism allows the Customer to curtail up to MW, which can [...] help manage peaks. However, this '
            'amount equates to only % of the total contracted load, [...] which may not be sufficient to materially reduce '
            'system stress during extreme events.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/iurc_46276_cac_ex1.pdf.txt',
  'agent_note': 'The contract pays a capacity-type interruptible demand credit with event-failure charges; the amounts are '
                'redacted. G2 is about the payment a job needs (its reservation price); a capacity credit neither states '
                "nor makes that fail, so 'contradicts' (family proposal) is lowered to 'bears' (the dossier's re-verified "
                'reading agrees).'},
 {'id': 'F1:7',
  'family': 'F1',
  'tag': 'G2',
  'reading': 'bears',
  'proposed_reading': 'contradicts',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'IURC Cause No. 46276, OUCC exceptions with I&M proposed-order text',
  'title': "IURC Cause No. 46276: OUCC's exceptions to I&M's proposed order (with the proposed-order text)",
  'version': '"OUCC\'s Exceptions to Indiana Michigan Power Company Proposed Order", filed December 17, 2025 (Exhibit A: '
             'redline of the proposed order; Exhibit B: clean OUCC proposed ...',
  'url': 'https://iurc.portal.in.gov/_entity/sharepointdocumentlocation/e2e5b537-85db-f011-8544-001dd803db57/bb9c6bba-fd52-45ad-8e64-a444aef13c39?file=46276+OUCC+Exceptions+to+Proposed+Order+12.17.2025.doc.pdf',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['He explained Google will provide specified interruptible capacity beginning with the designated PJM Delivery '
            'Year, subject to annual review and qualification requirements.',
            'Mr. Loveman testified that credits provided to Google for demand response participation will be recovered '
            'through the Resource Adequacy Rider because such commitments reduce I&M’s capacity and transmission service '
            'costs for all Indiana retail customers.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/iurc_46276_oucc_exceptions.pdf.txt',
  'agent_note': 'Interruptible capacity paid by credits (proposed order, not the final order); the quotes do not say how '
                'the credit is set and do not rule out opportunity-cost pricing, so G2 does not fail as written. Family '
                "proposal 'contradicts' lowered to 'bears'."},
 {'id': 'F1:8',
  'family': 'F1',
  'tag': 'G1',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Colangelo et al., Turning AI Data Centers into Grid-Interactive Assets (Phoenix)',
  'title': 'Colangelo et al., "Turning AI Data Centers into Grid-Interactive Assets: Results from a Field Demonstration in '
           'Phoenix, Arizona"',
  'version': 'arXiv:2507.00909 v1 (Tue, 1 Jul 2025)',
  'url': 'https://arxiv.org/abs/2507.00909',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['the trial achieved a 25% reduction in cluster power usage for three hours during peak grid events while '
            'maintaining AI quality of service (QoS) guarantees.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/colangelo_v1.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('states')."},
 {'id': 'F1:9',
  'family': 'F1',
  'tag': 'G4',
  'part': 'tiers',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Colangelo et al., Phoenix field demonstration',
  'title': 'Colangelo et al., "Turning AI Data Centers into Grid-Interactive Assets: Results from a Field Demonstration in '
           'Phoenix, Arizona"',
  'version': 'arXiv:2507.00909 v1 (Tue, 1 Jul 2025)',
  'url': 'https://arxiv.org/abs/2507.00909',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['Our workload tagging schema classifies jobs into flexibility tiers based on user tolerance for runtime or '
            'throughput deviations.',
            'For example, using feedback and guidance from our industry partners, we identified the following flexible SLAs '
            'for representative AI workloads: (a) Flex 0: no performance reduction (strict SLA); (b) Flex 1: up to 10% '
            'performance (average throughput) reduction allowed over a 3-6 hour period; (c) Flex 2: up to 25% allowed; (d) '
            'Flex 3: up to 50% allowed.',
            'In addition, the industry’s incentives and SLAs will need to evolve, encouraging users to opt into flexibility '
            'tiers in exchange for cost or compute availability benefits'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/colangelo_v1.pdf.txt',
  'agent_note': "States G4's tiers clause: pre-agreed throughput-reduction tiers Flex 0-3 (0/10/25/50 % over 3-6 h). No "
                'tier extends a deadline by the curtailed time, so it bears on the extension only as an absence.'},
 {'id': 'F1:10',
  'family': 'F1',
  'tag': 'G3',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Colangelo et al., Phoenix field demonstration',
  'title': 'Colangelo et al., "Turning AI Data Centers into Grid-Interactive Assets: Results from a Field Demonstration in '
           'Phoenix, Arizona"',
  'version': 'arXiv:2507.00909 v1 (Tue, 1 Jul 2025)',
  'url': 'https://arxiv.org/abs/2507.00909',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['Both pausing and re-allocating resources for running jobs require checkpointing for training jobs to ensure '
            'forward progress and minimize the overhead associated with these knobs. Although prior work offers methods to '
            'optimize for long-term objectives where changes to control state incur a cost [15], we are able to treat '
            'checkpointing overhead as negligible for our relatively infrequent demand response events since training jobs '
            'often run for days (or even weeks) at a time.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/colangelo_v1.pdf.txt',
  'agent_note': 'Pausing needs a checkpoint and the overhead is treated as negligible for infrequent events on long jobs. '
                'Named difference: an assumption, not a measurement, and the cost is not identified with the restart '
                'overhead.'},
 {'id': 'F1:11',
  'family': 'F1',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Colangelo et al., Phoenix field demonstration',
  'title': 'Colangelo et al., "Turning AI Data Centers into Grid-Interactive Assets: Results from a Field Demonstration in '
           'Phoenix, Arizona"',
  'version': 'arXiv:2507.00909 v1 (Tue, 1 Jul 2025)',
  'url': 'https://arxiv.org/abs/2507.00909',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['Although utilities offer financial incentives for power flexibility, other adoption costs–such as impacts on '
            'workload performance and delays in deploying new data centers–can limit participation [10], especially amid '
            'rapid AI growth. Utilities and system operators can further prioritize flexible AI data centers for '
            'accelerated interconnection and offer them lower tariffs and flexibility payments, recognizing their benefits '
            'to system reliability and ability to utilize existing system headroom, estimated at 100GW in the United States '
            '[11].'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/colangelo_v1.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('close')."},
 {'id': 'F1:12',
  'family': 'F1',
  'tag': 'G5',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Colangelo et al., Phoenix field demonstration',
  'title': 'Colangelo et al., "Turning AI Data Centers into Grid-Interactive Assets: Results from a Field Demonstration in '
           'Phoenix, Arizona"',
  'version': 'arXiv:2507.00909 v1 (Tue, 1 Jul 2025)',
  'url': 'https://arxiv.org/abs/2507.00909',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['Each event required the cluster to reduce power by 25% with respect to the average base load during the peak '
            'demand period, sustain the reduction for 3 hours, and ramp down and up gracefully over 15 minutes, avoiding '
            'so-called “snap back” at the conclusion of the event by staying below the pre-event baseline.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/colangelo_v1.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F1:13',
  'family': 'F1',
  'tag': 'G1',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Williams et al., Power-Flexible AI Data Centers',
  'title': 'Williams et al., "Power-Flexible AI Data Centers: A New Paradigm for Grid-Responsive Compute"',
  'version': 'arXiv:2606.25098 v1 (Tue, 23 Jun 2026)',
  'url': 'https://arxiv.org/abs/2606.25098',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['To evaluate sustained flexibility, grid partners requested power reductions between 10% and 40% for durations '
            'ranging from two to ten hours. The controller delayed flexible jobs to off-peak periods while critical jobs '
            'continued operating.',
            'UK Grid Compliance. Achieved 100% compliance across 200+ distinct National Grid power events on a 130 kW AI '
            'cluster of NVIDIA Blackwell Ultra GPUs.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/arx_2606.25098v1.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('states')."},
 {'id': 'F1:14',
  'family': 'F1',
  'tag': 'G3',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Williams et al., Power-Flexible AI Data Centers',
  'title': 'Williams et al., "Power-Flexible AI Data Centers: A New Paradigm for Grid-Responsive Compute"',
  'version': 'arXiv:2606.25098 v1 (Tue, 23 Jun 2026)',
  'url': 'https://arxiv.org/abs/2606.25098',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['Training jobs often consist of long iterative processes with natural pause points such as checkpoint '
            'intervals, creating opportunities to temporarily slow down or suspend jobs without compromising correctness, '
            'since distributed training systems support checkpointing and preemption that allow jobs to resume from saved '
            'states [9].'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/arx_2606.25098v1.pdf.txt',
  'agent_note': 'Checkpointing and preemption let jobs resume from saved states without compromising correctness: the '
                'lossless-pause premise. Named difference: no cost of the pause is given.'},
 {'id': 'F1:15',
  'family': 'F1',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Williams et al., Power-Flexible AI Data Centers',
  'title': 'Williams et al., "Power-Flexible AI Data Centers: A New Paradigm for Grid-Responsive Compute"',
  'version': 'arXiv:2606.25098 v1 (Tue, 23 Jun 2026)',
  'url': 'https://arxiv.org/abs/2606.25098',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['If data centers can reliably reduce power consumption during stressed grid operating conditions, operators may '
            'instead allow them to connect under alternative or non-firm agreements that [...] permit temporary curtailment '
            'during periods of system stress. [...] Because such arrangements reduce or defer the need for infrastructure '
            'upgrades identified for extreme conditions and system contingencies, they can shorten interconnection '
            'timelines and result in lower system costs.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/arx_2606.25098v1.pdf.txt',
  'agent_note': "Non-firm agreements permitting curtailment 'can shorten interconnection timelines'; the paper names the "
                "interconnection benefit but does not rank it above event payments. Family proposal 'states' lowered to "
                "'close'."},
 {'id': 'F1:16',
  'family': 'F1',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Williams et al., Power-Flexible AI Data Centers',
  'title': 'Williams et al., "Power-Flexible AI Data Centers: A New Paradigm for Grid-Responsive Compute"',
  'version': 'arXiv:2606.25098 v1 (Tue, 23 Jun 2026)',
  'url': 'https://arxiv.org/abs/2606.25098',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['The cluster reduced its power consumption by approximately 30% within 40 seconds',
            'In additional experiments, the cluster achieved 40% load reduction within approximately a minute while '
            'maintaining performance guarantees for critical jobs.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/arx_2606.25098v1.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F1:17',
  'family': 'F1',
  'tag': 'G4',
  'part': 'tiers',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Emerald AI, Sivaram, strategic expansion round post',
  'title': 'Emerald AI, "Sharing our Strategic Expansion Round: Emerald AI Raises $25 Million …" (Sivaram, 2026)',
  'version': 'company blog post by Varun Sivaram, dated March 31, 2026 (page metadata datePublished 2026-04-02, '
             'dateModified 2026-03-31), fetched 2026-09-29.',
  'url': 'https://www.emeraldai.co/blog/sharing-our-strategic-expansion-round-emerald-ai-raises-25-million-to-transform-ai-data-centers-into-flexible-power-grid-assets',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['Temporal Flexibility: Slowing or pausing AI workloads such as fine-tuning runs that have some '
            'customer-designated flexibility on completion time.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/emerald_expansion_round_2026.html.txt',
  'agent_note': "The nearest statement to the extension in the sweep: jobs with 'customer-designated flexibility on "
                "completion time' are slowed or paused. The grading agent reads the difference (a slack designated in "
                'advance, not stated to grow with the curtailed time) as the defining feature of the extension, so the '
                "claim is read against the tiers clause (a time-axis tier). For the investigator's review: read as 'close' "
                'to the extension, it would turn the extension grade to PARTLY REDUNDANT.'},
 {'id': 'F1:18',
  'family': 'F1',
  'tag': 'G8',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': "Utility Dive, Trabish, 'Data centers are ready to negotiate flexibility for speed'",
  'title': 'Utility Dive, "Data centers are ready to negotiate flexibility for speed" (Trabish, 2026)',
  'version': 'Deep Dive article by Herman K. Trabish, published June 26, 2026 (datePublished 2026-06-26), fetched '
             '2026-09-29.',
  'url': 'https://www.utilitydive.com/news/data-centers-flexibility-utilities-speed-to-power/822588/',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['But traditional bill credit incentives are too small to guarantee AI data centers will reduce their lucrative '
            'workloads when the utility sends a signal through Emerald AI, he added.',
            'An interconnection agreement offering the right incentive structure will, however, “unlock the next wave of '
            'flexibility technologies,” Barrow said.',
            '“A hyperscaler’s primary incentive is getting the interconnection to scale the business, and if it is not '
            'willing to work with the utility or system operator, a competitor will,” Kacergis said.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/utilitydive_flex_for_speed.html.txt',
  'agent_note': "Trade press quoting named industry voices: the hyperscaler's 'primary incentive is getting the "
                "interconnection' (Kacergis) and bill credits too small (Barrow, reported speech)."},
 {'id': 'F1:19',
  'family': 'F1',
  'tag': 'G4',
  'part': 'tiers',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Utility Dive, Trabish 2026',
  'title': 'Utility Dive, "Data centers are ready to negotiate flexibility for speed" (Trabish, 2026)',
  'version': 'Deep Dive article by Herman K. Trabish, published June 26, 2026 (datePublished 2026-06-26), fetched '
             '2026-09-29.',
  'url': 'https://www.utilitydive.com/news/data-centers-flexibility-utilities-speed-to-power/822588/',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['Every utility-data center interaction “is governed by operational parameters agreed upon by both parties in '
            'advance,” Shah said.',
            'The utility defines the parameters of an event requiring flexibility, including “maximum magnitude, minimum '
            'notice period, frequency limits, and event duration,” Shah continued.',
            'But data centers set the “hard floors that protect critical workloads and infrastructure under all '
            'circumstances,” she said.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/utilitydive_flex_for_speed.html.txt',
  'agent_note': "Event parameters (magnitude, notice, frequency, duration) and the data centre's 'hard floors' are fixed in "
                'advance: a bounded, pre-agreed form. Named difference: they are event parameters, not named as slowdown '
                "tiers. Family proposal 'states' lowered to 'close'."},
 {'id': 'F1:20',
  'family': 'F1',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Norris et al., Rethinking Load Growth (Duke Nicholas Institute)',
  'title': 'Norris, Profeta, Patino-Echeverri & Cowie-Haskell, "Rethinking Load Growth" (Duke Nicholas Institute, 2025)',
  'version': 'Nicholas Institute report, February 2025 (PDF created 2025-02-10), 43 pages as filed. Fetched copy: the copy '
             'filed as "JNGO Ex. 2.08" in Illinois Commerce Commission ...',
  'url': 'https://www.icc.illinois.gov/docket/P2025-0679/documents/371138/files/650737.pdf',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['Load flexibility similarly offers a practical solution to accelerating the interconnection of large demand '
            'loads',
            'These options resemble interconnection services available to large generators that forgo capacity '
            'compensation, and potentially higher curtailment risk, in exchange for expedited lower-cost grid access '
            '(Norris 2023).'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/duke_rlg_icc.pdf.txt',
  'agent_note': 'Flexibility accelerates interconnection, and flexible-interconnection options are likened to generator '
                'services that forgo capacity compensation for expedited access. Named difference: an analogy for a '
                'programme design; the report does not say interconnection is the main commercial value of flexible AI '
                "load. Family proposal 'states' lowered to 'close'."},
 {'id': 'F1:21',
  'family': 'F1',
  'tag': 'G2',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Norris et al., Rethinking Load Growth (Duke)',
  'title': 'Norris, Profeta, Patino-Echeverri & Cowie-Haskell, "Rethinking Load Growth" (Duke Nicholas Institute, 2025)',
  'version': 'Nicholas Institute report, February 2025 (PDF created 2025-02-10), 43 pages as filed. Fetched copy: the copy '
             'filed as "JNGO Ex. 2.08" in Illinois Commerce Commission ...',
  'url': 'https://www.icc.illinois.gov/docket/P2025-0679/documents/371138/files/650737.pdf',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['At the same time, financial incentives provided by most demand response programs have historically been modest '
            'and insufficient to offset the expenses and opportunity costs associated with curtailed operations.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/duke_rlg_icc.pdf.txt',
  'agent_note': 'Names opportunity cost as what a DR payment must offset; named difference: data centres generally, not '
                'decomposed into lost work, restart and deadline pressure.'},
 {'id': 'F1:22',
  'family': 'F1',
  'tag': 'G4',
  'part': 'tiers',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Chen & Zheng, To Defer or To Shift?',
  'title': 'Chen & Zheng, "To Defer or To Shift? The Role of AI Data Center Flexibility on Grid Interconnection"',
  'version': 'arXiv:2604.05376 v1 (Tue, 7 Apr 2026)',
  'url': 'https://arxiv.org/abs/2604.05376',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['For many AI training and inference jobs, they have a flexible window so that users could opt for later '
            'completion time. In practice, it is possible to determine the delay window size based on user tolerance for '
            'runtime or throughput deviations.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/arx_2604.05376v1.pdf.txt',
  'agent_note': 'A fixed delay window per job class chosen from user tolerance: a time-axis tier, not an extension by the '
                'curtailed time.'},
 {'id': 'F1:23',
  'family': 'F1',
  'tag': 'G2',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Ji, Crozier & Liska, Quantifying and Attributing Power Flexibility from GPU-Heavy Data Centers',
  'title': 'Ji, Crozier & Liska, "Quantifying and Attributing Power Flexibility from GPU-Heavy Data Centers"',
  'version': 'arXiv:2603.27831 v2 (Tue, 30 Jun 2026)',
  'url': 'https://arxiv.org/abs/2603.27831',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['cooling shifting can reliably reduce demand for short periods at relatively low incentive ($30/MWh), and '
            'movement of backfilled jobs can often reduce demand at similar prices ($30-300/MWh). Further reduction is '
            'possible through reordering or delaying jobs, but due to lost profits these actions come at higher prices '
            '(starting at $600/MWh, more significantly above $3000/MWh).',
            'Job reordering likely leads to introduced latency (unless there happens to be a 1:1 swap of two jobs whose '
            'only difference is in GPU utilization) and so both mechanisms are likely trading off against the job revenue. '
            'The exact price at which this flexibility is deployed will depend heavily on the assumed revenue per GPU-hour; '
            'here we considered a relatively high value consistent with a commercial machine, however in-house private '
            'AI-training machines (whose profit isn’t directly linked to jobs) may provide these mechanisms at a lower '
            'price point.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/arx_2603.27831v2.pdf.txt',
  'agent_note': 'The price at which delay flexibility appears is set by lost job revenue (opportunity-cost pricing, in a '
                "model). Named difference: the operator's lost revenue from delayed starts, not a training job's lost work, "
                "restart and deadline pressure. Family proposal 'states' lowered to 'close'."},
 {'id': 'F1:24',
  'family': 'F1',
  'tag': 'G3',
  'reading': 'bears',
  'proposed_reading': 'contradicts',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Ji, Crozier & Liska',
  'title': 'Ji, Crozier & Liska, "Quantifying and Attributing Power Flexibility from GPU-Heavy Data Centers"',
  'version': 'arXiv:2603.27831 v2 (Tue, 30 Jun 2026)',
  'url': 'https://arxiv.org/abs/2603.27831',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['cooling shifting can reliably reduce demand for short periods at relatively low incentive ($30/MWh), and '
            'movement of backfilled jobs can often reduce demand at similar prices ($30-300/MWh). Further reduction is '
            'possible through reordering or delaying jobs, but due to lost profits these actions come at higher prices '
            '(starting at $600/MWh, more significantly above $3000/MWh).',
            'Constraint (3) ensures that each job should start within the maximum waiting time twait after its arrival.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/arx_2603.27831v2.pdf.txt',
  'agent_note': 'The model has no pause (jobs are delayed or reordered before they start), so it says nothing about a '
                "lossless pause's cost; its delay cost is a revenue-bound operator's lost profit. A qualifier "
                "(fleet-level), not a statement that makes G3's job-level claim fail. Family proposal 'contradicts' lowered "
                "to 'bears'."},
 {'id': 'F1:25',
  'family': 'F1',
  'tag': 'G3',
  'reading': 'bears',
  'proposed_reading': 'contradicts',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Li, Beyond Scalar Flexibility: From Eligible AI Workloads to Dependable Load Relief',
  'title': 'Li, "Beyond Scalar Flexibility: From Eligible AI Workloads to Dependable Load Relief"',
  'version': 'arXiv:2609.05406 v1 (Fri, 4 Sep 2026)',
  'url': 'https://arxiv.org/abs/2609.05406',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['If every deferred megawatt-hour rebounds and the expected lost work equals half of a one-hour checkpoint '
            'interval, net energy change after a four-hour call is −12.5% of gross curtailed energy.',
            'Low-priority status shows that an operator already accepts preemption semantics, yet the trace does not reveal '
            'checkpoint completion, service-level violations, restart energy, network bottlenecks, or the control latency '
            'required by a grid product.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/arx_2609.05406v1.pdf.txt',
  'agent_note': "Lost work of half a checkpoint interval is a conditional scenario ('If ...'), and the paper says the trace "
                'does not reveal checkpoint completion: an assumption of a lossy pause, not evidence that a lossless pause '
                "costs more than the restart. Family proposal 'contradicts' lowered to 'bears'."},
 {'id': 'F1:26',
  'family': 'F1',
  'tag': 'G1',
  'reading': 'bears',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Li, Beyond Scalar Flexibility',
  'title': 'Li, "Beyond Scalar Flexibility: From Eligible AI Workloads to Dependable Load Relief"',
  'version': 'arXiv:2609.05406 v1 (Fri, 4 Sep 2026)',
  'url': 'https://arxiv.org/abs/2609.05406',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['Immediate eligible curtailment averages 3.55 MW, or 12.1% of workload power but only 6.35% of median facility '
            'power',
            'The production scheduler exposes almost no additional delay-based capacity: newly deferrable arrivals average '
            '0.008 MW and have zero 95%-available capacity.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/arx_2609.05406v1.pdf.txt',
  'agent_note': 'A trace analysis of eligible curtailment (small: 6.35 % of median facility power); it does not report DR '
                "use in the field. Read 'bears' (a qualifier on scale), not 'close'."},
 {'id': 'F1:27',
  'family': 'F1',
  'tag': 'G4',
  'part': 'extension',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Li, Beyond Scalar Flexibility',
  'title': 'Li, "Beyond Scalar Flexibility: From Eligible AI Workloads to Dependable Load Relief"',
  'version': 'arXiv:2609.05406 v1 (Fri, 4 Sep 2026)',
  'url': 'https://arxiv.org/abs/2609.05406',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['Flexibility contracts should therefore specify an eligible-power boundary, duration, reliability, portfolio, '
            'response realization, recovery, and recalibration rule rather than one percentage of site load.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/arx_2609.05406v1.pdf.txt',
  'agent_note': 'The proposed contract terms have no job-deadline term: bears on the extension as an absence.'},
 {'id': 'F1:28',
  'family': 'F1',
  'tag': 'G4',
  'part': 'tiers',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Acun et al., Investigating Power Consumption Flexibility of AI Data Centers for DR Participation (E-Energy '
            "'26)",
  'title': 'Acun et al., "Investigating Power Consumption Flexibility of AI Data Centers for Demand Response Participation" '
           "(e-Energy '26)",
  'version': "The 17th ACM International Conference on Future and Sustainable Energy Systems (E-Energy '26), June 22–25, "
             '2026, Banff; doi 10.1145/3744255.3798112; Boston University. ...',
  'url': 'https://www.bu.edu/peaclab/files/2026/03/FlexDC_Sim_ACM_E_Energy26.pdf',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['Although training workloads may appear to have stricter QoS constraints in Table 2, they effectively have more '
            'relaxed deadlines under our relative execution-time–based QoS definition in Eq. (8).',
            'is the sojourn time, representing the total time for queuing and execution.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/bu_flexdc_sim_eenergy26.pdf.txt',
  'agent_note': 'A relative-deadline QoS threshold fixed in advance (proportional to job length, not extended by the '
                'curtailed time): a time-axis tier.'},
 {'id': 'F1:29',
  'family': 'F1',
  'tag': 'G3',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Gao et al., Deep Learning Workload Scheduling in GPU Datacenters: Taxonomy, Challenges and Vision',
  'title': 'Gao et al., "Deep Learning Workload Scheduling in GPU Datacenters: Taxonomy, Challenges and Vision"',
  'version': 'arXiv:2205.11913 v3 (Wed, 1 Jun 2022)',
  'url': 'https://arxiv.org/abs/2205.11913',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['C4: Preemption overhead. DL frameworks usually provide functions to pause/resume the training jobs at any time '
            'for better fault-tolerance. The overhead of such processes primarily depends upon the job scale, which ranges '
            'from seconds to minutes. In this paper, the preemption overhead is considered as the addition of the costs of '
            'pausing and resuming the job. For time-consuming jobs, the preemption overhead is relatively small with the '
            'benefit of higher scheduling [...] flexibility. But for short jobs, the preemption overhead is non-negligible, '
            'and frequent preemption will delay their progress.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/arx_2205.11913v3.pdf.txt',
  'agent_note': 'Pause/resume overhead of seconds to minutes, small for long jobs. Named difference: a survey statement '
                'about scheduling preemption, not a curtailment cost.'},
 {'id': 'F1:30',
  'family': 'F1',
  'tag': 'G4',
  'part': 'extension',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Lechowicz et al., The Online Pause and Resume Problem',
  'title': 'Lechowicz et al., "The Online Pause and Resume Problem"',
  'version': 'arXiv:2303.17551 v1 (Thu, 30 Mar 2023)',
  'url': 'https://arxiv.org/abs/2303.17551',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['In carbon-aware temporal workload shifting, an interruptible and deferrable workload may be paused during '
            'periods of high carbon intensity and resumed during periods of low carbon intensity. The workload needs to be '
            'running for k units of time to complete and must be ﬁnished before its deadline T. However, pausing and '
            'resuming the workload typically comes with overheads such as storing the state in memory and checkpointing; '
            'hence frequent pausing and resuming is undesirable.',
            'The player is required to complete this transaction for all k units by some point in time T. Both k and T are '
            'known in advance.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/lechowicz_v1.pdf.txt',
  'agent_note': "The domain model's deadline T is fixed and known in advance (the WALL arm); bears on the extension as an "
                'absence.'},
 {'id': 'F1:31',
  'family': 'F1',
  'tag': 'G2',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': "Ren & Islam, Colocation Demand Response: Why Do I Turn Off My Servers? (ICAC '14)",
  'title': 'Ren & Islam, "Colocation Demand Response: Why Do I Turn Off My Servers?" (ICAC \'14)',
  'version': "Proceedings of the 11th International Conference on Autonomic Computing (ICAC '14), June 18–20, 2014, "
             'Philadelphia, USENIX, (PDF created 2014-06-11), fetched 2026-09-29.',
  'url': 'https://www.usenix.org/system/files/conference/icac14/icac14-paper-ren.pdf',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['Tenant cost. Turning off some servers will result in “costs”. As an example, we consider switching cost and '
            'delay cost [25], while other costs (e.g., management costs) can also be factored in.',
            'Below, we denote tenant i’s requested payment for turning off mi servers by [...] where wi ≥1 is referred to '
            'as greediness of tenant i, and βi ≥0 converts delay cost to monetary values'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/ren_islam_icac14.pdf.txt',
  'agent_note': "A tenant's requested payment is its switching cost plus delay cost (times a markup): G2's structure. Named "
                'difference: queue-served colocation workloads with latency, not training jobs with deadlines.'},
 {'id': 'F1:32',
  'family': 'F1',
  'tag': 'G2',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Wierman, Liu, Liu & Mohsenian-Rad, Opportunities and Challenges for Data Center Demand Response (IGCC 2014)',
  'title': 'Wierman, Liu, Liu & Mohsenian-Rad, "Opportunities and Challenges for Data Center Demand Response" (IGCC 2014)',
  'version': 'Proc. IGCC 2014 (doi 10.1109/IGCC.2014.7039172 per dblp search result; not independently fetched). Author PDF '
             'at (PDF created 2014-05-06), fetched 2026-09-29. The Stony ...',
  'url': 'https://smart.caltech.edu/papers/dcdrsurvey.pdf',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['The ﬁrst payment is the “capacity payment”, which is made simply for being available. The second payment is '
            'the “operation payment”, which is made only if the service was actually called.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/wierman_dcdr_survey_caltech.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F1:33',
  'family': 'F1',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'EPRI, DCFlex Flex MOSAIC Framework brief',
  'title': 'EPRI, "DCFlex Flex MOSAIC™ Framework" (two-page brief)',
  'version': 'EPRI public attachment 97236, "© 2026" (PDF created 2026-03-24), (linked from Utility Dive and from page '
             'sha256 ...',
  'url': 'https://restservice.epri.com/publicattachment/97236',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['The goal of introducing Flex MOSAIC™ is to increase transparency and predictability around ﬂexibility '
            'capabilities to operationalize ﬂexibility and facilitate large load interconnection processes.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/epri_publicattachment_97236.pdf.txt',
  'agent_note': 'A stated purpose of the classification is to facilitate interconnection; it is not a statement that '
                "interconnection is flexible load's main commercial value. Family proposal 'states' lowered to 'close'."},
 {'id': 'F1:34',
  'family': 'F1',
  'tag': 'G1',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'EPRI via PR Newswire, DCFlex expands to nine demonstration sites',
  'title': 'EPRI via PR Newswire, "EPRI\'s DCFlex Initiative Expands to Nine Demonstration Sites Across U.S., Europe"',
  'version': 'press release, Feb 02, 2026 (San Diego, DTECH), fetched 2026-09-29. (The same release on epri.com rendered '
             'only by JavaScript and returned no text; see NOT REACHED.)',
  'url': 'https://www.prnewswire.com/news-releases/epris-dcflex-initiative-expands-to-nine-demonstration-sites-across-us-europe-302676241.html',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['London, UK : Testing involves AI compute load flexibility, with the data center reacting to direct utility '
            'interaction using day-ahead, hour-ahead, and real-time curtailment requests.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/prn_dcflex_nine_sites.html.txt',
  'agent_note': 'A demonstration site where AI compute load reacts to utility curtailment requests: field use '
                '(demonstration scale).'},
 {'id': 'F1:35',
  'family': 'F1',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NVIDIA blog, Parker, How Power-Flexible AI Factories Can Stabilize the Global Energy Grid',
  'title': 'NVIDIA, "How Power-Flexible AI Factories Can Stabilize the Global Energy Grid" (Parker, 2026)',
  'version': 'NVIDIA Blog, datePublished 2026-03-25, fetched 2026-09-29.',
  'url': 'https://blogs.nvidia.com/blog/power-flexible-ai-factories-energy-grid/',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['For AI factories, proven load flexibility could support faster utility and interconnectiodn conversations by '
            'showing that sites can temporarily reduce withdrawals during grid stress, rather than requiring the grid to '
            'plan only for worst-case firm demand.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/nvidia_blog_power_flexible_factories.html.txt',
  'agent_note': "Proven flexibility 'could support' faster interconnection conversations; not ranked against payments. "
                "Family proposal 'states' lowered to 'close'."},
 {'id': 'F1:36',
  'family': 'F1',
  'tag': 'G1',
  'reading': 'bears',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NVIDIA blog, How AI Factories Can Help Relieve Grid Stress',
  'title': 'NVIDIA, "How AI Factories Can Help Relieve Grid Stress" (2025)',
  'version': 'NVIDIA Blog, datePublished 2025-07-01, fetched 2026-09-29.',
  'url': 'https://blogs.nvidia.com/blog/ai-factories-flexible-power-use/',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['Some jobs can be paused or slowed, like the training or fine-tuning of a large language model for academic '
            'research.',
            'AI factory users can label their workloads to guide Emerald’s software on which jobs can be slowed, paused or '
            'rescheduled — or, Emerald’s AI agents can make these predictions automatically.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/nvidia_blog_ai_factories.html.txt',
  'agent_note': "The quotes say training 'can be paused or slowed' and that workloads can be labelled; they do not by "
                "themselves say this is done for DR in the field. Family proposal 'states' lowered to 'bears'."},
 {'id': 'F1:37',
  'family': 'F1',
  'tag': 'G1',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Indiana Michigan Power news release 10359',
  'title': 'Indiana Michigan Power, "I&M, Google Filing to Support Reliability Through Demand Response Structure"',
  'version': 'I&M (AEP) news release, August 4, 2025, fetched 2026-09-29.',
  'url': 'https://www.indianamichiganpower.com/company/news/view?releaseID=10359',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['The contract filed with the Indiana Utilities Regulatory Commission (IURC) on July 30 outlines a custom Demand '
            'Response structure, aligning with Google’s operating capabilities.',
            'By participating in this program, Google will leverage new capabilities that allow it to reduce or shift '
            'electricity demand to carry out non-urgent tasks during hours when the electric grid is under less stress.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/im_release_10359.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('states')."},
 {'id': 'F1:38',
  'family': 'F1',
  'tag': 'G2',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'POWER magazine, Patel, Google-I&M deal',
  'title': 'POWER magazine, "Google, I&M Strike Landmark Deal to Share Clean Capacity and Flex AI Load" (trade press)',
  'version': 'article by Sonal Patel, datePublished 2025-08-06, fetched 2026-09-29.',
  'url': 'https://www.powermag.com/google-im-strike-landmark-deal-to-share-clean-capacity-and-flex-ai-load/',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['According Loveman, the arrangement includes two separate demand response offerings—one that is tailored to '
            'Google’s offerings and another that qualifies under PJM’s Emergency Demand Response Program.',
            'The structure, which includes defined curtailment schedules, compliance testing, and performance penalties, '
            'will “benefit I&M, and all of its customers, by reducing the cost of providing service through lower capacity '
            'and transmission costs,” he said.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/powermag_google_im.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F1:39',
  'family': 'F1',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Energy Innovation, Data Center Demand Flexibility (one-page brief)',
  'title': 'Energy Innovation, "Data Center Demand Flexibility" (one-page brief)',
  'version': 'undated one-page PDF (PDF created 2025-07-07), fetched 2026-09-29.',
  'url': 'https://energyinnovation.org/wp-content/uploads/Data-Center-Demand-Flexibility.pdf',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['Flexible data centers may be able to connect to the grid faster and reduce ratepayer costs by avoiding the '
            'need for new infrastructure.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/energyinnovation_dc_flex.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('close')."},
 {'id': 'F1:40',
  'family': 'F1',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Data Center Frontier, Google Partners With Utilities to Ease AI Data Center Grid Strain',
  'title': 'Data Center Frontier, "Google Partners With Utilities to Ease AI Data Center Grid Strain" (trade press)',
  'version': 'article, datePublished 2025-09-15, fetched 2026-09-29.',
  'url': 'https://www.datacenterfrontier.com/energy/article/55316600/google-partners-with-utilities-to-ease-ai-data-center-grid-strain',
  'dossier': 'docs/citations/dr1_f1_2026-09-29.md',
  'quote': ['By agreeing to curtail loads during peak demand, data centers can be granted faster interconnection approvals '
            'since they present less risk to overall system stability.'],
  'raw_file': '/tmp/claude-0/dr1_src/F1/dcf_google_utilities.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('close')."},
 {'id': 'F2:0',
  'family': 'F2',
  'tag': 'G2',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'PJM Manual 11: Energy & Ancillary Services Market Operations',
  'title': 'PJM Manual 11: Energy & Ancillary Services Market Operations, Revision 137 (effective July 28, 2026)',
  'version': '("Revision: 137 Effective Date: July 28, 2026"); fetched 2026-09-29.',
  'url': 'https://www.pjm.com/-/media/DotCom/documents/manuals/m11.pdf',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['Shut down costs, for each period are defaulted to zero if not submitted. Shutdown costs are expressed in '
            'dollars, and represent the fixed cost associated with committing a Load Response resource.',
            'The end-use customer’s incremental costs shall include the quantifiable cost incurred for not consuming '
            'electricity when dispatched by PJM, such as wages paid without production, lost sales, damaged products that '
            'cannot be sold, or other incremental costs as approved by PJM.',
            'CSPs are eligible to be paid full LMP for the Registration’s or Dispatch Group’s reductions, provided that the '
            'LMP at the pricing point is at or above the Net Benefits Price'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/pjm_m11.pdf.txt',
  'agent_note': "Economic DR offers are validated against the customer's incremental cost of not consuming (lost "
                "production, lost sales) plus a fixed shutdown cost per commitment: near G2's decomposition. Named "
                'differences: deadline pressure is not named, and the payment when dispatched is the LMP, not the validated '
                "cost. Family proposal 'states' lowered to 'close'."},
 {'id': 'F2:1',
  'family': 'F2',
  'tag': 'G3',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'PJM Manual 11',
  'title': 'PJM Manual 11: Energy & Ancillary Services Market Operations, Revision 137 (effective July 28, 2026)',
  'version': '("Revision: 137 Effective Date: July 28, 2026"); fetched 2026-09-29.',
  'url': 'https://www.pjm.com/-/media/DotCom/documents/manuals/m11.pdf',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['Shut down costs, for each period are defaulted to zero if not submitted. Shutdown costs are expressed in '
            'dollars, and represent the fixed cost associated with committing a Load Response resource.',
            'Incremental costs may not include shutdown costs.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/pjm_m11.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F2:2',
  'family': 'F2',
  'tag': 'G2',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NESO DFS Pricing Pro-Forma',
  'title': 'NESO, DFS Pricing Pro-Forma (July 2024)',
  'version': '("DFS Pricing Pro-Forma July 2024", listed 31 Jul 2024; PDF created 2024-07-26); fetched 2026-09-29 (served '
             'without a file extension; saved as `.pdf`).',
  'url': 'https://www.neso.energy/document/322181/download',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['This would risk participants aiming to beat a marginal cost of other actions rather than submitting their own '
            'marginal cost, removing the benefits of pay-as-clear.',
            'Pay as Bid (PAB) therefore continues to be the chosen payment mechanism as it is more efficient for this '
            'market.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/neso_dfs_pricing_proforma_2024.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('close')."},
 {'id': 'F2:3',
  'family': 'F2',
  'tag': 'G2',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NESO DFS Procurement Rules',
  'title': 'NESO, DFS Procurement Rules, Version 5.0 (effective and published 18 May 2026)',
  'version': '(linked as "Procurement Rules", published 18 May 2026, on the DFS page); front cover "Version: 5.0 Effective '
             'From: 18 May 2026 Date Published: 18 May 2026"; fetched ...',
  'url': 'https://www.neso.energy/document/379391/download',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['11.5.6 a Utilisation Price (in £/MWh, where the applicable pound and pence figures shall each be an integer); '
            'and 11.5.7 the offered Service Volume (in MW)',
            '12.2 All valid DFS Submissions shall be ranked, for each relevant Event ID, by price (from lowest to highest) '
            'and (subject to paragraph 12.3) accepted until NESO has secured its required aggregate volume for the relevant '
            'Settlement Period and Event ID and without exceeding the Zonal Caps'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/neso_dfs_procurement_rules_2026.pdf.txt',
  'agent_note': "The price is the provider's own bid, ranked lowest first; a job could bid its own curtailment cost. Named "
                "difference: the rules do not say what the bid should reflect, and acceptance is NESO's."},
 {'id': 'F2:4',
  'family': 'F2',
  'tag': 'G2',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NESO DFS Market Guidance',
  'title': 'NESO, Demand Flexibility Service Market Guidance (2026; PDF created 16 February 2026)',
  'version': '("DFS Market Guidance report"); fetched 2026-09-29.',
  'url': 'https://www.neso.energy/document/377071/download',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['It is worth noting that BM prices can be changed up until gate closure, and this means that NESO could decline '
            'DFS based on BM prices at the time, and then BM prices increase closer to real time. This means that DFS, as a '
            'longer notice service, cannot react to close to real-time price spikes, and providers should be aware of this '
            'when analysing any post event data.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/neso_dfs_market_guidance_2026.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F2:5',
  'family': 'F2',
  'tag': 'G2',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'ERCOT, Load Resource Participation in the ERCOT Markets',
  'title': 'ERCOT, "Load Resource Participation in the ERCOT Markets" (programme page)',
  'version': '(undated page); fetched 2026-09-29.',
  'url': 'https://www.ercot.com/services/programs/load/laar',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['In the ERCOT markets, the value of an LR’s Load reduction is equal to that of an increase in generation by a '
            'generating plant. LRs in SCED submit bids to buy power up to their specified level and are instructed by ERCOT '
            'to reduce Load if wholesale market prices equal or exceed that level. LRs that are scheduled or selected in '
            'the ERCOT Day-Ahead AS Market are eligible to receive a capacity payment regardless of whether they are '
            'dispatched in Real-Time.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/ercot_clr_page.html.txt',
  'agent_note': 'A Load Resource is curtailed when prices reach the level it chose (a load-side reservation price). Named '
                "difference: ERCOT does not say how the level is chosen or that it is the job's opportunity cost. Family "
                "proposal 'states' lowered to 'close'."},
 {'id': 'F2:6',
  'family': 'F2',
  'tag': 'G2',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'ERCOT Nodal Protocols Section 6',
  'title': 'ERCOT Nodal Protocols, Section 6 (Adjustment Period and Real-Time Operations), August 28, 2026',
  'version': '(linked as "Section 6"); document date "August 28, 2026"; fetched 2026-09-29.',
  'url': 'https://www.ercot.com/files/docs/2024/06/28/06-082826_Nodal.docx',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['(1) An RTM Energy Bid represents the willingness to buy energy at or below a certain price, not to exceed the '
            'effective Value of Lost Load (VOLL), for the Demand response capability of a Controllable Load Resource (CLR) '
            'in the RTM.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/ercot_nodal_s06.docx.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('close')."},
 {'id': 'F2:7',
  'family': 'F2',
  'tag': 'G2',
  'reading': 'bears',
  'proposed_reading': 'contradicts',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'ERCOT ERS Technical Requirements & Scope of Work',
  'title': 'ERCOT, ERS Technical Requirements & Scope of Work, December 1, 2026 through March 31, 2027 (posted Sep 18, '
           '2026)',
  'version': 'fetched 2026-09-29. The file carries tracked changes from the June–September 2026 version; text is taken with '
             'the changes accepted.',
  'url': 'https://www.ercot.com/files/docs/2026/09/18/ERS-Technical-Requirements_DecMar27.docx',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['If a QSE’s offer is selected by the Emergency Response Service Procurement Methodology, ERCOT will pay the QSE '
            'a capacity payment in exchange for making ERS Resources available for deployment upon ERCOT’s instruction.',
            'Offers must be for a single price, MW capacity and maximum base Load for any specific Time Period, although '
            'those values may vary across Time Periods.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/ercot_ers_techreq_DecMar27.docx.txt',
  'agent_note': "ERS pays for availability at the offered or clearing price; an offer can embed the load's expected cost, "
                "so G2 (the job's cost sets the payment it needs) does not fail as written. Family proposal 'contradicts' "
                "lowered to 'bears'."},
 {'id': 'F2:8',
  'family': 'F2',
  'tag': 'G2',
  'reading': 'bears',
  'proposed_reading': 'contradicts',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'CPUC, Emergency Load Reduction Program',
  'title': 'CPUC, "Emergency Load Reduction Program" (web page)',
  'version': '(undated; refers to decision D.23-12-005, December 2023); fetched 2026-09-29.',
  'url': 'https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/electric-costs/demand-response-dr/emergency-load-reduction-program',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['Non-residential participants are compensated after-the-fact at a prefixed compensation rate of '
            '$2/kilowatt-hour for every kilowatt-hour of electricity consumption the customer reduces voluntarily during an '
            'ELRP event.',
            'There are no penalties for not reducing energy consumption, or for increasing consumption, during an ELRP '
            'event.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/cpuc_elrp.html.txt',
  'agent_note': "A posted uniform price with no penalty: the job's cost still decides whether the posted payment is enough, "
                "which is G2's claim; ELRP qualifies how the payment is set rather than making G2 fail. Family proposal "
                "'contradicts' lowered to 'bears'."},
 {'id': 'F2:9',
  'family': 'F2',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NESO DFS winter 2024/25 report',
  'title': 'NESO, "Demand Flexibility Service (DFS)" winter 2024/25 report (published 3 July 2025)',
  'version': '(linked as "The DFS Winter 2024/2025 Overview Report"); front page "Published: 3 July 2025"; fetched '
             '2026-09-29.',
  'url': 'https://www.neso.energy/document/363911/download',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['Overall, the average accepted bid price across all accepted bids was £210/MWh. The lowest accepted bid price '
            'was £59 on 27 December 2024 for 1MW covering 1 SP. The 5 highest prices cleared over separate winter days were '
            '£1,290, £750, £740, £575 and £572 per MWh.',
            'Number of SPs 306 112 40 High (based on Breakpoints) £ 33,560* £ 12,477 £ 13,726 High (based on highest '
            'accepted Bid) £ 25,609* £ 10,166 £ 12,337 Average (based on mean accepted bid) £ 21,009 £ 7,558 Low (lowest '
            'accepted bid) £ 17,918 £3,142'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/neso_dfs_winter2425_report.pdf.txt',
  'agent_note': 'Revenue scenarios per MW and accepted prices; the source says nothing about compute cost, so it cannot '
                "state G7. Family proposal 'states' lowered to 'bears'."},
 {'id': 'F2:10',
  'family': 'F2',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NESO DFS winter 2022/23 review',
  'title': 'NESO (as ESO), DFS winter 2022/23 review (published 30 August 2023)',
  'version': '("Download the DFS winter review", entry "DFS winter review 22/23 – 30 August 2023"; PDF created 2023-08-17); '
             'fetched 2026-09-29.',
  'url': 'https://www.neso.energy/document/287006/download',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['The average price paid for tests events was £3,000/MWh. For live events, the average price paid was '
            '£4,559/MWh.',
            'The combined spend was around £11.1 million split up into £8.0 million for tests events and £3.1 million for '
            'live events. In total, the demand reduction achieved was around 3,300 MWh.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/neso_dfs_winter2223_review.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F2:11',
  'family': 'F2',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NESO DFS Market Information Report',
  'title': 'NESO, DFS Market Information Report, August 2026 (published 11 August 2026)',
  'version': '("DFS Market Information Report August 2026"); fetched 2026-09-29.',
  'url': 'https://www.neso.energy/document/385526/download',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['Each downward (demand turn down) test will carry a GAP of £500/MWh.',
            'The GAPs have been set to be in line with the high end of attainable revenue, informed by actual scenarios '
            'observed this year.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/neso_dfs_market_info_aug2026.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F2:12',
  'family': 'F2',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'contradicts',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'PJM 2027/2028 Base Residual Auction Report',
  'title': 'PJM, 2027/2028 Base Residual Auction Report (December 17, 2025)',
  'version': '(dated December 17, 2025; PDF created 2026-01-05); fetched 2026-09-29.',
  'url': 'https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2027-2028/2027-2028-bra-report.pdf',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['For the 2027/2028 BRA, all prices cleared at the cap ($333.44). In the 2026/2027 BRA, the RTO cleared at the '
            'price cap of $329.17.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/pjm_bra_2027_2028_report.pdf.txt',
  'agent_note': 'The capacity price ($333.44/MW-day) is a large per-MW availability payment, but the source does not '
                "compare it with compute cost; whether it is small against a training fleet's compute cost is the model "
                "check's arithmetic, not the source's statement. Family proposal 'contradicts' lowered to 'bears'."},
 {'id': 'F2:13',
  'family': 'F2',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'ERCOT ERS Procurement Results, ERS-30 Oct-Nov 2026',
  'title': 'ERCOT, ERS Procurement Results: Non-Weather-Sensitive ERS-30, October 1 – November 30, 2026 (posted 2026-09-29)',
  'version': 'ERCOT MIS report type 11465 ("ERS Procurement Results", EMIL NP3-144-M, public), document "30M ERS '
             'Procurement OctNov26", DocID 1280391409, published ...',
  'url': 'https://www.ercot.com/misdownload/servlets/mirDownload?doclookupId=1280391409',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['Time Period 1 HE 0600 through 0900, Monday thru Friday except ERCOT Holidays; 164 hours MW Procured or Self '
            'Arranged 2,400.916 Clearing Price $5.15 Number of ERS Resources Procured 339 Projected cost $2,027,813.65',
            'Time Period 5 HE 2000 through 2200, Monday thru Friday except ERCOT Holidays; 123 hours MW Procured or Self '
            'Arranged 2,288.654 Clearing Price $15.03 Number of ERS Resources Procured 325 Projected cost $4,231,011.76'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/ercot_ers_proc_30M_OctNov26.docx.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F2:14',
  'family': 'F2',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'PUCT Substantive Rule 25.507',
  'title': 'PUCT Substantive Rule §25.507, ERCOT Emergency Response Service (effective 08/04/2022)',
  'version': '(header "§25.507--1 effective date 08/04/2022 (P 53493)"); fetched 2026-09-29. The link printed on ERCOT\'s '
             'page ( redirects to the PUCT home page (sha256 ...',
  'url': 'https://ftp.puc.texas.gov/public/puct-info/agency/rulesnlaws/subrules/electric/25.507/25.507.pdf',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['(2) ERCOT may spend a maximum of $75 million in a 12-month period on ERS, unless otherwise determined by the '
            'commission. During that 12-month period, ERCOT may exceed the $75 million maximum by up to an additional $25 '
            'million for ERS contract renewals'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/puct_25507.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F2:15',
  'family': 'F2',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'CPUC, Emergency Load Reduction Program',
  'title': 'CPUC, "Emergency Load Reduction Program" (web page)',
  'version': '(undated; refers to decision D.23-12-005, December 2023); fetched 2026-09-29.',
  'url': 'https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/electric-costs/demand-response-dr/emergency-load-reduction-program',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['Non-residential participants are compensated after-the-fact at a prefixed compensation rate of '
            '$2/kilowatt-hour for every kilowatt-hour of electricity consumption the customer reduces voluntarily during an '
            'ELRP event.',
            'Event Duration 1-hour minimum; 5-hour maximum Annual Dispatch Limit Program can be called up to 60 hours in a '
            'single year'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/cpuc_elrp.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F2:16',
  'family': 'F2',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'ERCOT Nodal Protocols Section 2 (Definitions)',
  'title': 'ERCOT Nodal Protocols, Section 2 (Definitions and Acronyms)',
  'version': '(linked as "Section 2"); fetched 2026-09-29.',
  'url': 'https://www.ercot.com/files/docs/2024/06/28/02-080126_Nodal.docx',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['Sustained Response Period The period of time beginning ten minutes after the deployment time instructed within '
            'the ERCOT Extensible Markup Language (XML) message deploying Emergency Response Service (ERS)-10 or 30 minutes '
            'after the deployment time instructed within the ERCOT XML message deploying ERS-30, and ending with the recall '
            'time instructed within the ERCOT XML message recalling ERS Resources from the deployment.',
            'Fast Frequency Response (FFR) The automatic self-deployment and provision by a Resource of their obligated '
            'response within 15 cycles after frequency meets or drops below a preset threshold, or a deployment in response '
            'to an ERCOT Extensible Markup Language (XML) messaging instruction within ten minutes.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/ercot_nodal_s02.docx.txt',
  'agent_note': 'Gives product response times (FFR within 15 cycles or ten minutes); says nothing about checkpoint saves, '
                "so it bears on G6 rather than stating it. Family proposal 'states' lowered to 'bears'."},
 {'id': 'F2:17',
  'family': 'F2',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'ERCOT Nodal Protocols Section 3',
  'title': 'ERCOT Nodal Protocols, Section 3 (Management Activities for the ERCOT System), August 1, 2026',
  'version': '(linked from as "Section 3"); document date "August 1, 2026"; fetched 2026-09-29.',
  'url': 'https://www.ercot.com/files/docs/2025/09/01/03-080126_Nodal.docx',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['(b) An ERS Resource participating in ERS-10 must be capable of meeting its event performance obligations '
            'relevant to its assigned performance evaluation methodology within ten minutes of an ERCOT Dispatch '
            'Instruction to its QSE, and must be able to maintain such performance for the entire Sustained Response '
            'Period. An ERS Resource participating in ERS-30 must be capable of meeting its event performance obligations '
            'relevant to its assigned performance evaluation methodology within 30 minutes of an ERCOT Dispatch Instruction '
            'to its QSE, and must be able to maintain such performance for the entire Sustained Response Period.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/ercot_nodal_s03.docx.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F2:18',
  'family': 'F2',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'PJM Manual 18: PJM Capacity Market',
  'title': 'PJM Manual 18: PJM Capacity Market, Revision 63 (effective September 24, 2026)',
  'version': '("Revision: 63 Effective Date: September 24, 2026"); fetched 2026-09-29.',
  'url': 'https://www.pjm.com/-/media/DotCom/documents/manuals/m18.pdf',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['Load management must be able to be implemented within two hours of notification to the resource provider of a '
            'PJM-initiated load management event. Load management is required to fully respond within 30 minutes of '
            'notification unless an exception request for 60 or 120 minutes notification time is approved by PJM.',
            '30 Minute Lead Time – Load management which must be fully implemented in 30 minutes or less from the time the '
            'PJM dispatcher notifies the market operations center of a curtailment event.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/pjm_m18.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F2:19',
  'family': 'F2',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NESO DFS Participation Guidance v18',
  'title': 'NESO, DFS Participation Guidance document v18 (2026; PDF created 10 August 2026)',
  'version': '("DFS Participation Guidance document v18 2026", listed 10 Aug 2026; PDF creation date 2026-08-10); fetched '
             '2026-09-29.',
  'url': 'https://www.neso.energy/document/346011/download',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['2. DFS units must be able to respond for a minimum of 30 minutes.',
            'In line with the existing derogation, the service can be procured at any time in a day, up to a maximum of '
            'twenty four hours ahead of the start of any Service Requirement window. The requirement windows for the '
            'positive margin (demand turn down) aspect of the service are unlikely to change and will continue to '
            'predominantly be within the evening peak period, between 4pm and 11pm.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/neso_dfs_participation_guidance_v18.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F2:20',
  'family': 'F2',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'CAISO, Overview of Reliability Demand Response Resource',
  'title': 'CAISO, "Overview of Reliability Demand Response Resource" (training presentation, May 8, 2014)',
  'version': '(dated May 8, 2014; still listed on the current CAISO page); fetched 2026-09-29. Dated: the RDRR rules may '
             'have changed since 2014; this document is not a current tariff.',
  'url': 'https://www.caiso.com/documents/reliabilitydemandresponseresourceparticipationoverview.pdf',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['Minimum load curtailment ≥ 500kW per RDRR Must be capable of delivering reliability energy in real-time, '
            'reaching full curtailment within 40 minutes Cannot have a minimum run time of greater than one (1) hour Must '
            'have sustained response period or maximum run time of at least four (4) hours'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/caiso_rdrr_overview.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F2:21',
  'family': 'F2',
  'tag': 'G4',
  'part': 'extension',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'PJM Manual 18: PJM Capacity Market',
  'title': 'PJM Manual 18: PJM Capacity Market, Revision 63 (effective September 24, 2026)',
  'version': '("Revision: 63 Effective Date: September 24, 2026"); fetched 2026-09-29.',
  'url': 'https://www.pjm.com/-/media/DotCom/documents/manuals/m18.pdf',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['Capacity Performance DR is available for an unlimited number of interruptions during the Delivery Year, and '
            'will be capable of maintaining each such interruption (i) for all hours of the Delivery Year beginning with '
            'the 2027/ 2028 Delivery Year unless there is an Office of the Interconnection approved maintenance outage '
            'during October through April'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/pjm_m18.pdf.txt',
  'agent_note': 'Capacity Performance DR: unlimited interruptions, each maintainable for all hours of the Delivery Year; no '
                "term extends any deadline of the load's. Bears on the extension as an absence."},
 {'id': 'F2:22',
  'family': 'F2',
  'tag': 'G5',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NESO DFS Procurement Rules',
  'title': 'NESO, DFS Procurement Rules, Version 5.0 (effective and published 18 May 2026)',
  'version': '(linked as "Procurement Rules", published 18 May 2026, on the DFS page); front cover "Version: 5.0 Effective '
             'From: 18 May 2026 Date Published: 18 May 2026"; fetched ...',
  'url': 'https://www.neso.energy/document/379391/download',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['10.4.2 in order to ensure that step changes in aggregate delivery of DFS over a DFS Service Window do not '
            'exceed operational limits, for each DFS Service Window comprising two or more consecutive Settlement Periods '
            'NESO may determine an allocation of one or more of such Settlement Periods to each Registered DFS Participant'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/neso_dfs_procurement_rules_2026.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F2:23',
  'family': 'F2',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'ERCOT Trending Topics: New Batch Connection Process for Large Electricity Users',
  'title': 'ERCOT, "ERCOT\'s New Batch Connection Process for Large Electricity Users" (Trending Topics, June 18, 2026)',
  'version': '(dated June 18, 2026; PDF created 2026-07-20); found by web search on ercot.com; fetched 2026-09-29.',
  'url': 'https://www.ercot.com/files/docs/2026/06/18/Trending-Topics-ERCOT-s-New-Batch-Connection-Process-for-Large-Electricity-Users-v2.pdf',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['PCLR is for large customers that are willing to let ERCOT reduce their power consumption during periods of '
            'localized stress on the grid. The customers agree to embed the controllable load into ERCOT’s dispatching '
            'system and let ERCOT curtail their power use when transmission constraints arise in their area. In exchange, '
            'the customers can access a portion of the grid ahead of a full transmission buildout.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/ercot_trending_batch_v2.pdf.txt',
  'agent_note': 'Curtailability is exchanged for earlier grid access under PCLR; the explainer does not rank access above '
                "event payments and PCLR is not specific to AI load. Family proposal 'states' lowered to 'close'."},
 {'id': 'F2:24',
  'family': 'F2',
  'tag': 'G3',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NESO DFS Procurement Rules',
  'title': 'NESO, DFS Procurement Rules, Version 5.0 (effective and published 18 May 2026)',
  'version': '(linked as "Procurement Rules", published 18 May 2026, on the DFS page); front cover "Version: 5.0 Effective '
             'From: 18 May 2026 Date Published: 18 May 2026"; fetched ...',
  'url': 'https://www.neso.energy/document/379391/download',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['6.4.3 to act (and where it is not the owner and/or occupier of Premises which are Metered by Unit Meter '
            'Point(s) allocated to a DFS Unit procure that such owner and/or occupier acts) in good faith to implement the '
            'DFS Initiation Measures and deliver DFS in accordance with the DFS Service Terms including by preventing the '
            'deliberate displacement of any Demand or Generation represented by the DFS Operational Baseline to one or more '
            'other Meter Points.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/neso_dfs_procurement_rules_2026.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F2:25',
  'family': 'F2',
  'tag': 'DEF-reservation-price',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': "PJM Manual 18 / Wikipedia 'Reservation price' (PJM Manual 18 part)",
  'title': 'PJM Manual 18: PJM Capacity Market, Revision 63 (effective September 24, 2026)',
  'version': '("Revision: 63 Effective Date: September 24, 2026"); fetched 2026-09-29.',
  'url': 'https://www.pjm.com/-/media/DotCom/documents/manuals/m18.pdf',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['A PRD Provider that is nominating PRD for an RPM Auction must also submit a PRD election (indicating the '
            'Sub-zonal/Zonal Nominal PRD Value to be provided at different reservation prices) in the Capacity Exchange '
            'system by January 15, prior to the Base Residual Auction or Third Incremental Auction for the relevant '
            'Delivery Year.',
            'The curve will be shifted leftward in this manner only for those portions of the curve that are at or above '
            'the PRD Reservation Price, since the PRD load can be excluded only if the auction clears at or above that '
            'price.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/pjm_m18.pdf.txt',
  'agent_note': "Definition claim (not a G position): PJM's Price Responsive Demand uses a load-side reservation price in "
                '$/MW-day.'},
 {'id': 'F2:26',
  'family': 'F2',
  'tag': 'DEF-reservation-price',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': "PJM Manual 18 / Wikipedia 'Reservation price' (Wikipedia part)",
  'title': 'Wikipedia, "Reservation price" (revision 1375744881, 2026-09-19T20:02:49Z)',
  'version': 'revision id and timestamp from the MediaWiki API (first API request HTTP 429, retried once: sha256 '
             '1a324bcff36672df3c61f8f6ceae73b7db06397ee2e3444120ebe0aa5cc8c2f1); ...',
  'url': 'https://en.wikipedia.org/w/index.php?title=Reservation_price&action=render',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['In economics, a reservation (or reserve) price is a limit on the price of a good or a service. On the demand '
            'side, it is the highest price that a buyer is willing to pay; on the supply side, it is the lowest price a '
            'seller is willing to accept for a good or service.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/wikipedia_reservation_price.html.txt',
  'agent_note': 'Definition claim (not a G position); tertiary source for the generic definition.'},
 {'id': 'F2:27',
  'family': 'F2',
  'tag': 'DEF-VoLL',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'DESNZ, Exploring Reliability Standard Metrics / London Economics VoLL (DESNZ part)',
  'title': 'DESNZ, "Exploring Reliability Standard Metrics in a Net Zero Transition" (research paper 2023/050, November '
           '2023)',
  'version': '(November 2023; PDF created 2024-03-01); found by web search; fetched 2026-09-29.',
  'url': 'https://assets.publishing.service.gov.uk/media/65e3a3323f694514a3035fbe/5-exploring-reliability-standard-metrics-in-net-zero-transition.pdf',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['The willingness to pay can be measured by the Value of Lost Load (VoLL). This represents the value that '
            'customers place on reliability, or their own cost of interruption.'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/desnz_reliability_metrics_2023.pdf.txt',
  'agent_note': "Definition claim (not a G position): VoLL as the customer's own cost of interruption."},
 {'id': 'F2:28',
  'family': 'F2',
  'tag': 'DEF-VoLL',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'DESNZ, Exploring Reliability Standard Metrics / London Economics VoLL (London Economics part)',
  'title': 'London Economics, "The Value of Lost Load (VoLL) for Electricity in Great Britain", final report for Ofgem and '
           'DECC (July 2013)',
  'version': 'requested at redirected to (July 2013; PDF created 2013-07-18); found by web search; fetched 2026-09-29.',
  'url': 'https://ofgem.gov.uk/ofgem-publications/82293/london-economics-value-lost-load-electricity-gbpdf',
  'dossier': 'docs/citations/dr1_f2_2026-09-29.md',
  'quote': ['Doing these calculations yields a headline weighted-average VoLL figure of £16,940/MWh for peak winter '
            'workdays in GB.',
            'Overall, the VoLLs for I&C customers are about £1,400/MWh taking the simple arithmetic mean of the figures '
            'above (at a sector level, as detailed in Annex 13, the average I&C VoLLs show a broader range; however, the '
            'vast majority are around £6,000/MWh or lower).'],
  'raw_file': '/tmp/claude-0/dr1_src/F2/le_voll_gb_2013.pdf.txt',
  'agent_note': 'Definition claim (not a G position): GB study values of VoLL.'},
 {'id': 'F3:0',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NERC Incident Review: Considering Simultaneous Voltage-Sensitive Load Reductions',
  'title': 'NERC, "Incident Review: Considering Simultaneous Voltage-Sensitive Load Reductions" (January 2025)',
  'version': 'NERC Event Analysis incident review, "Date of Publication: January 8, 2025" (PDF creation 2025-01-08), '
             'fetched 2026-09-29.',
  'url': 'https://www.nerc.com/globalassets/our-work/reports/event-reports/incident_review_large_load_loss.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['A 230 kV transmission line fault led to customer-initiated simultaneous loss of approximately 1,500 MW of '
            'voltage-sensitive load that was not anticipated by the BES operators. The electric grid has not historically '
            'experienced simultaneous load losses of this magnitude in response to a fault on the system, which has '
            'historically been planned for large generation losses but not for such significant simultaneous load losses.',
            'While this incident did not present any significant issues with the reconnection of the large loads, the '
            'potential exists for issues in future incidents if the load is not reconnected in a controlled manner. '
            'Significant amounts of load being reconnected to the system present challenges to Balancing Authorities (BA) '
            'and Transmission Operators (TOP). Ramp rates for load connection are just as critical to system operations as '
            'generation ramping.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/nerc_incident_review_large_load_loss.pdf.txt',
  'agent_note': 'Simultaneous loss of ~1,500 MW of data-centre load and reconnection ramp rates as a challenge. Named '
                'differences: an involuntary, fault-triggered transfer to backup, not flexible load; not identified as AI '
                "training; the reconnection risk stated as potential. Family proposal 'states' lowered to 'close'."},
 {'id': 'F3:1',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NERC LLTF White Paper: Characteristics and Risks of Emerging Large Loads',
  'title': 'NERC Large Loads Task Force, "White Paper: Characteristics and Risks of Emerging Large Loads" (July 2025)',
  'version': 'NERC LLTF white paper dated July 2025 (PDF creation 2025-07-22), fetched 2026-09-29.',
  'url': 'https://www.nerc.com/globalassets/who-we-are/standing-committees/rstc/whitepaper-characteristics-and-risks-of-emerging-large-loads.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['Generally, AI training executed in large clusters has rapid fluctuations during training periods and while '
            'saving checkpoint [...] progress. Additionally, the transition from training to saving checkpoint progress (or '
            'vice versa) may happen in under one second.',
            'For example, Figure 3.1 shows a North American data center ramping down from about 450 MW to about 40 MW '
            'within 36 seconds around hour 6. The load’s demand is constant (around 7 MW) for approximately 4 hours. After '
            'hour 10, the data center ramps back up to 450 MW over the course of a few minutes.',
            'In addition to the loss of load, the sudden restoration of a large load could exhaust available balancing '
            'reserves, ultimately leading to decreased system frequency and potential frequency instability.',
            'For example, AI model training at the xAI Colossus Supercomputer in Memphis, Tennessee—currently the world’s '
            'largest AI training cluster [...] —can change the loading 35–70 MW or more within a minute as the model starts '
            'and stops. That change may not be an issue for a single facility, but the aggregate effect across multiple '
            'facilities may negatively impact ACE control.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/nerc_whitepaper_large_loads.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('states')."},
 {'id': 'F3:2',
  'family': 'F3',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NERC LLTF White Paper: Characteristics and Risks of Emerging Large Loads',
  'title': 'NERC Large Loads Task Force, "White Paper: Characteristics and Risks of Emerging Large Loads" (July 2025)',
  'version': 'NERC LLTF white paper dated July 2025 (PDF creation 2025-07-22), fetched 2026-09-29.',
  'url': 'https://www.nerc.com/globalassets/who-we-are/standing-committees/rstc/whitepaper-characteristics-and-risks-of-emerging-large-loads.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['Generally, AI training executed in large clusters has rapid fluctuations during training periods and while '
            'saving checkpoint [...] progress. Additionally, the transition from training to saving checkpoint progress (or '
            'vice versa) may happen in under one second.',
            'Data center industry experts note that power delivery systems for HPC loads (AI data centers) commonly exclude '
            'UPS protection systems for the IT equipment. Instead, they employ a checkpoint process where checkpoints are '
            'saved at regular intervals. If there is an interruption to the IT equipment’s power, the checkpoint may be '
            'restored after the power interruption ends.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/nerc_whitepaper_large_loads.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F3:3',
  'family': 'F3',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NERC LLTF White Paper: Characteristics and Risks of Emerging Large Loads',
  'title': 'NERC Large Loads Task Force, "White Paper: Characteristics and Risks of Emerging Large Loads" (July 2025)',
  'version': 'NERC LLTF white paper dated July 2025 (PDF creation 2025-07-22), fetched 2026-09-29.',
  'url': 'https://www.nerc.com/globalassets/who-we-are/standing-committees/rstc/whitepaper-characteristics-and-risks-of-emerging-large-loads.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['Concepts have been explored [...] in some areas around mandatory load curtailments by the ISO or utility '
            'during stressful grid conditions, which might allow for TPs to assume a lower peak demand for the load and '
            'potentially reduce the transmission buildout exclusively needed to support the load.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/nerc_whitepaper_large_loads.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('close')."},
 {'id': 'F3:4',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NERC LLWG White Paper: Assessment of Gaps',
  'title': 'NERC Large Loads Working Group, "White Paper: Assessment of Gaps in Existing Practices, Requirements, and '
           'Reliability Standards for Emerging Large Loads" (March 2026)',
  'version': 'NERC LLWG white paper dated March 2026 (PDF creation 2026-03-11), fetched 2026-09-29.',
  'url': 'https://www.nerc.com/globalassets/our-work/guidelines/reliability/white-paper---assessment-of-gaps.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['However, as noted above, multiple large loads in a region could collectively reduce or increase their '
            'consumption by unknown amounts, which are not events currently considered in operations or operations '
            'planning. These events could lead to reliability issues including thermal violations/exceedances, unacceptable '
            'voltage levels and voltage instability, and transient instability of the system.',
            'Currently, planning (TPL-001, FAC-002, FAC-01156), operations planning (TOP-002, IRO-00857), and operations '
            '(TOP-001, IRO-008) related Reliability Standards do not consider the impacts of large-scale ramping, '
            'disconnection, and reconnection events.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/nerc_wp_gaps.pdf.txt',
  'agent_note': "Collective ramps, disconnection and reconnection of large loads named as reliability risks outside today's "
                'standards; stated for the emerging-large-load class (computational loads), not AI training by name.'},
 {'id': 'F3:5',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NERC Reliability Guideline: Risk Mitigation for Emerging Large Loads',
  'title': 'NERC, "Reliability Guideline: Risk Mitigation for Emerging Large Loads" (May 2026)',
  'version': 'NERC LLWG Reliability Guideline, "Final", dated May 2026 (PDF creation 2026-05-01), fetched 2026-09-29. The '
             'guideline is voluntary and non-binding (NERC FAQ, below).',
  'url': 'https://www.nerc.com/globalassets/our-work/guidelines/reliability/RG_Risk-Mitigation-For-Emerging-Large-Loads.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['A newly identified driver of CILR involves distributed computing workloads shared across geographically or '
            'electrically disparate data centers. When a transmission fault causes a low-voltage condition at a single '
            'facility, the interruption of the shared process triggers a synchronized demand reduction across all '
            'participating data centers, including those completely unaffected by the fault and low voltage condition. This '
            'cause of CILR is not well documented.',
            'TOs should coordinate with RCs and TOPs to define restoration sequences that avoid simultaneous reconnection '
            'of large blocks of load.',
            'At a minimum, this should include the establishment of operational load ramp rate limits (e.g., MW/min) for '
            'large loads in normal and post-disturbance scenarios'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/nerc_rg_risk_mitigation.pdf.txt',
  'agent_note': 'A synchronized demand reduction across data centres sharing a distributed computing workload, and '
                'restoration that avoids simultaneous reconnection of large load blocks (stated for disturbance recovery).'},
 {'id': 'F3:6',
  'family': 'F3',
  'tag': 'G1',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NERC Reliability Guideline: Risk Mitigation for Emerging Large Loads',
  'title': 'NERC, "Reliability Guideline: Risk Mitigation for Emerging Large Loads" (May 2026)',
  'version': 'NERC LLWG Reliability Guideline, "Final", dated May 2026 (PDF creation 2026-05-01), fetched 2026-09-29. The '
             'guideline is voluntary and non-binding (NERC FAQ, below).',
  'url': 'https://www.nerc.com/globalassets/our-work/guidelines/reliability/RG_Risk-Mitigation-For-Emerging-Large-Loads.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['Require large load curtailment participation by establishing programs for voluntary or automated demand '
            'modulation from large loads during regulation scarcity'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/nerc_rg_risk_mitigation.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F3:7',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NERC Aggregated Report on Level 2 Industry Recommendation: Large Load Interconnection',
  'title': 'NERC, "Aggregated Report on NERC Level 2 Industry Recommendation: Large Load Interconnection, Study, '
           'Commissioning, and Operations"',
  'version': 'NERC aggregated report on the Level 2 alert of September 9, 2025 (PDF creation 2026-03-17), fetched '
             '2026-09-29.',
  'url': 'https://www.nerc.com/globalassets/programs/bpsa/alerts/2025/aggregated-report-level-2-large-load-interconnection-study-commissioning-and-operations.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['Many still left this blank or indicated that no operational ramp is established. This is not a normal '
            'requirement for load, but the fast-ramping nature of computational loads may necessitate this for large loads. '
            'The entities that did respond varied between 8 MW/min to 300 MW/min. Many responses that did include a load '
            'ramp limit largely fell between 10 MW/min and 30 MW/min.',
            'The entities that responded to Question 11 typically repeated the same value for Question 10. There does not '
            'seem to be a consistent requirement concerning the recovery of load in a post-disturbance state.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/nerc_level2_aggregated.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('states')."},
 {'id': 'F3:8',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'bears',
  'proposed_reading': 'contradicts',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NERC Incident Review: Voltage-Sensitive Crypto Load Reductions',
  'title': 'NERC, "Incident Review: Voltage-Sensitive Crypto Load Reductions" (January 2026)',
  'version': 'NERC Event Analysis incident review (PDF creation 2026-01-13), fetched 2026-09-29.',
  'url': 'https://www.nerc.com/globalassets/our-work/reports/event-reports/incident_review_considering_voltage-sensitive_crypto_load_reductions.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['Unlike traditional data centers, crypto-mining facilities do not return to full load almost immediately; '
            'instead, their ramp-up process is gradual and predictable, reducing the chances of rapid spikes in demand on '
            'the grid.',
            'In no recorded instance has a crypto facility’s power draw surged instantaneously—such as within a few cycles '
            'or seconds—because recovery occurs through a restarting process, not from instantaneous transfer via UPS as '
            'seen in traditional data centers.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/nerc_ir_crypto_2026.pdf.txt',
  'agent_note': "Crypto facilities ramp back gradually after trips (a hardware restart); 'traditional data centers' return "
                'almost immediately. It concerns crypto, not AI training, so it does not make G5 fail as written; it names '
                "restart speed as the variable. Family proposal 'contradicts' lowered to 'bears'."},
 {'id': 'F3:9',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NERC Level 3 Essential Action alert: Computational Load',
  'title': 'NERC, "Essential Action to Industry: Computational Load Modeling, Studies, Instrumentation, Commissioning, '
           'Operations, Protection, and Control" (Level 3 Alert, May 2026)',
  'version': 'NERC Level 3 alert, "Initial Distribution: May 4, 2026", fetched 2026-09-29.',
  'url': 'https://www.nerc.com/globalassets/programs/bpsa/alerts/level-3-computational-load-alert.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['d. Expected Ramp Rate – Expected maximum ramp rate (MW/min) in down-ramp and up-ramp.',
            'This Level 3 NERC Alert is not the same as a Reliability Standard, and it does not create a mandatory '
            'obligation to take the Essential Actions.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/nerc_level3_alert.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F3:10',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NERC Large Loads FAQ',
  'title': 'NERC, "Large Loads Frequently Asked Questions" (August 2026)',
  'version': 'NERC FAQ page dated August 2026 (PDF creation 2026-08-21), fetched 2026-09-29.',
  'url': 'https://www.nerc.com/globalassets/initiatives/large-loads-action-plan/large-loads-faqs.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['In addition to these rapid timelines, some emerging large loads introduce new challenges to grid operators '
            'like rapid demand ﬂuctuations and increased voltage sensitivity.',
            'This paper also provides recommendations for ride-through and post-fault active power recovery requirements,'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/nerc_large_loads_faq.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('states')."},
 {'id': 'F3:11',
  'family': 'F3',
  'tag': 'G1',
  'reading': 'bears',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NERC 2025 Long-Term Reliability Assessment',
  'title': 'NERC, "2025 Long-Term Reliability Assessment" (January 2026)',
  'version': 'NERC LTRA, cover dated January 2026 (PDF modified 2026-02-24), fetched 2026-09-29.',
  'url': 'https://www.nerc.com/globalassets/our-work/assessments/nerc_ltra_2025.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['Understand and manage reliability risks accompanying large-load growth and leverage potential capabilities in '
            'new types of loads to provide flexibility to operators during times of grid stress.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/nerc_ltra_2025.pdf.txt',
  'agent_note': "Flexibility of new loads is a 'potential capability', not reported field practice. Family proposal 'close' "
                "lowered to 'bears'."},
 {'id': 'F3:12',
  'family': 'F3',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'ERCOT Ancillary Services Study (final white paper)',
  'title': 'ERCOT, "ERCOT Ancillary Services Study" (final white paper, September 2024)',
  'version': 'ERCOT public report, "September 2024" (PDF creation 2024-10-07), fetched 2026-09-29.',
  'url': 'https://www.ercot.com/files/docs/2024/10/07/ERCOT-Ancillary-Services-Study-Final-White-Paper.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['RRS-FFR is (full) response when frequency is below 59.85 Hz within 250 ms',
            'ECRS is capacity that can respond in 10 minutes',
            'c. Load Resources that are not Controllable Load Resources and are qualified for deployment by the operator '
            'using the Ancillary Service Deployment Manager and capable of: i. Reducing consumption based on an ERCOT '
            'Extensible Markup Language (XML) instruction within 30 minutes; and ii. Maintaining that deployment until '
            'recalled.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/ercot_as_study_2024.pdf.txt',
  'agent_note': "States product timescales (250 ms to 30 minutes), not the position that a pause's save limits the "
                "products; the link to the save time is the investigator's. Family proposal 'states' lowered to 'bears'."},
 {'id': 'F3:13',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'bears',
  'proposed_reading': 'contradicts',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'ERCOT Ancillary Services Study (final white paper)',
  'title': 'ERCOT, "ERCOT Ancillary Services Study" (final white paper, September 2024)',
  'version': 'ERCOT public report, "September 2024" (PDF creation 2024-10-07), fetched 2026-09-29.',
  'url': 'https://www.ercot.com/files/docs/2024/10/07/ERCOT-Ancillary-Services-Study-Final-White-Paper.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['Some Large Loads, for example crypto-mining data centers, can quickly change consumption based on changes in '
            'ERCOT wholesale prices. If many Large Loads change their consumption at the same time and in a manner not '
            'coordinated with ERCOT, it could cause a significant imbalance between load and generation, which could cause '
            'frequency instability on the ERCOT system.',
            'However, through mid-2024, ERCOT has not observed reliability problems due to Large Load consumption ramps. '
            'Based on this, ERCOT is not planning to make any related changes but will continue to monitor the issue.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/ercot_as_study_2024.pdf.txt',
  'agent_note': 'GRADE-DECIDING READING. The same passage names the risk (uncoordinated simultaneous changes by many large '
                'loads could cause frequency instability) and reports no observed reliability problem from large-load ramps '
                'through mid-2024. G5 says flexible AI load carries grid-safety risks; a report that the risk had not been '
                'realised as harm by mid-2024 qualifies it but does not make it fail as written. Family proposal '
                "'contradicts' read as 'bears'; for the investigator's review, 'contradicts' would make G5 MIXED."},
 {'id': 'F3:14',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'ERCOT staff, Ancillary Services and Large Loads in ERCOT',
  'title': 'ERCOT staff, "Ancillary Services and Large Loads in ERCOT" (May 6, 2024)',
  'version': 'ERCOT staff presentation, Large Load Integration, May 6, 2024, fetched 2026-09-29.',
  'url': 'https://www.ercot.com/files/docs/2024/05/05/Large%20Loads%20and%20Ancillary%20Services.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['Both triggers are more likely to occur during intervals of elevated system prices, which ERCOT has observed is '
            'also when many Large Loads independently curtail (totaling over 2 GW).'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/ercot_large_loads_as_2024.pdf.txt',
  'agent_note': 'Many large loads curtail independently (over 2 GW) in the same high-price intervals as ECRS triggers. '
                'Named difference: the grid consequence is in unquoted bullets and the loads are not AI-specific. Family '
                "proposal 'states' lowered to 'close'."},
 {'id': 'F3:15',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'ERCOT (Springer), Large Loads in ERCOT, NERC LMWG meeting package',
  'title': 'ERCOT (Springer), "Large Loads in ERCOT – Observations and Risks to Reliability" (NERC LMWG, September 17, '
           '2024)',
  'version': 'ERCOT presentation in the NERC Load Modeling Working Group meeting package of September 17, 2024 (PDF '
             'creation 2024-09-20), fetched 2026-09-29.',
  'url': 'https://www.nerc.com/globalassets/who-we-are/standing-committees/rstc/lmwg/lmwg_meeting_presentations_september_17_2024.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['A growing number of Large Loads can change their MW consumption rapidly enough to exhaust available Regulation '
            'service.',
            'In the 12 months ending February 2024, – ERCOT experienced 255 five-minute SCED intervals where the change in '
            'Large Load consumption has exceeded the amount of procured Regulation for that interval.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/nerc_lmwg_sep2024.pdf.txt',
  'agent_note': 'Large-load consumption changes exceeded procured regulation in 255 five-minute intervals: the ramp risk '
                "measured on ERCOT's flexible large loads (not AI-specific in the quote)."},
 {'id': 'F3:16',
  'family': 'F3',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'ERCOT, Overview of Demand Response in ERCOT',
  'title': 'ERCOT (Ögelman), "Overview of Demand Response in ERCOT" (April 2023)',
  'version': 'ERCOT presentation, April 2023 (PDF creation 2023-05-19), fetched 2026-09-29.',
  'url': 'https://www.ercot.com/files/docs/2023/05/19/ERCOT_Demand_Response__Summary_Spring_2023-update.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['Non-Controllable Load Resources – Blocky loads with both a 10-minute ramp capability for manual deployments '
            'and automatic deployment through Under Frequency Relay',
            'Four ERS service types: • Non-Weather Sensitive in 10 and 30 minute ramps'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/ercot_dr_overview_2023.pdf.txt',
  'agent_note': "States ERS and load-resource ramp times, not the position. Family proposal 'states' lowered to 'bears'."},
 {'id': 'F3:17',
  'family': 'F3',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'ERCOT, Overview of Demand Response in ERCOT',
  'title': 'ERCOT (Ögelman), "Overview of Demand Response in ERCOT" (April 2023)',
  'version': 'ERCOT presentation, April 2023 (PDF creation 2023-05-19), fetched 2026-09-29.',
  'url': 'https://www.ercot.com/files/docs/2023/05/19/ERCOT_Demand_Response__Summary_Spring_2023-update.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['$75M per year spend limit, with addition $25M for renewals in case of exhaustion • Exhaustion occurs when '
            'deployment exceeds a total of 24 hours in the December-March SCT and 12 hours in all other SCTs',
            'Current estimated value of 1 MW 4CP load Reduction for a Transmission connected IDR customer on Oncor’s system '
            '~$38,000'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/ercot_dr_overview_2023.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F3:18',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'ERCOT NOGRR282 Large Computational Load Ride-Through Requirements (board item 6.2; PUCT report)',
  'title': 'ERCOT, NOGRR 282 "Large Computational Load Ride-Through Requirements" (approved July 9, 2026; effective August '
           '1, 2026)',
  'version': '(a) ERCOT Board item 6.2, December 8–9, 2025 (PDF modified 2025-12-01), (b) NOGRR282 issue page, ("Status '
             'Approved on 07/09/2026", "Effective Dates 08/01/2026"); (c) ...',
  'url': 'https://www.ercot.com/files/docs/2025/12/01/6.2-NOGRR282-Large-Electronic-Load-Ride-Through-Requirements-and-NPRR1308.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['ERCOT has identified 26 LEL ride-through events since the beginning of 2023.',
            'When loads trip due to voltage excursions (also referred to as failing to “ride through”), this can result in '
            'sudden changes to the frequency that can cause other loads and generators to trip offline, potentially '
            'resulting in cascading outages.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/ercot_nogrr282_item6.2.pdf.txt',
  'agent_note': 'Large computational load trips during voltage excursions can cause sudden frequency changes and cascading '
                'outages. Named difference: involuntary trips, not flexible or scheduled curtailment. Family proposal '
                "'states' lowered to 'close'. Quotes from the board-item PDF only."},
 {'id': 'F3:19',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'ERCOT NPRR1191 (withdrawn), Galaxy comments',
  'title': 'ERCOT, NPRR1191 "Registration, Interconnection, and Operation of Customers with Large Loads" (withdrawn) and '
           'Galaxy comments (August 2023)',
  'version': 'NPRR1191 issue page, ("Status: Withdrawn"; posted Aug 1, 2023); Galaxy Digital comments on 1191NPRR (PDF '
             'creation 2023-08-30), fetched 2026-09-29.',
  'url': 'https://www.ercot.com/mktrules/issues/NPRR1191',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['1. What is the rationale for the proposed ramp rate limitations of 20% per minute of registered peak demand '
            'for Controllable Load Resources (CLRs)?',
            'b) Proposed ramp rate limitations (lesser of 5% of peak demand or 20 MW per minute ramp down, lesser of 2% of '
            'peak demand or 8 MW per minute ramp up)'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/ercot_galaxy_1191nprr.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('close')."},
 {'id': 'F3:20',
  'family': 'F3',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'contradicts',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Texas SB 6, 89(R), enrolled',
  'title': 'Texas Senate Bill 6, 89th Legislature (Regular Session), enrolled version (2025)',
  'version': '"89(R) SB 6 - Enrolled version" (PDF creation 2025-05-30), fetched 2026-09-29. (The House Research '
             'Organization bill analysis, sha256 ...',
  'url': 'https://capitol.texas.gov/tlodocs/89R/billtext/pdf/SB00006F.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['ensure that the independent organization provides at least a 24-hour notice to large load customers and '
            'requires each large load to remain curtailed for the duration of the energy emergency alert event or until the '
            'load can be recalled safely; and'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/tx_sb6_enrolled.pdf.txt',
  'agent_note': "A product with at least 24 hours' notice is outside G6's limit, which is consistent with G6 ('limits the "
                "products it can meet'), not a contradiction. Family proposal 'contradicts' lowered to 'bears'."},
 {'id': 'F3:21',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'WECC (Elevate), Assessment of Large Load Interconnection Risks in the Western Interconnection',
  'title': 'WECC (Elevate Energy Consulting: Quint, Zhao, Thomas), "An Assessment of Large Load Interconnection Risks in '
           'the Western Interconnection" (February 2025)',
  'version': 'WECC technical report dated February 2025 (PDF creation 2025-02-27), page headers marked '
             '"<Limited-Disclosure>" although the file is served publicly at fetched ...',
  'url': 'https://www.wecc.org/sites/default/files/documents/products/2025/Report_WECC%20Large%20Loads%20Risk%20Assessment%204.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['Large flexible loads may be price sensitive or respond to other signals. When understood, modeled, studied, '
            'and/or controlled, this is a service and asset to the grid. Yet when these fluctuations cause increased '
            'variability and uncertainty for real-time operations, they are a detriment.',
            'Without requirements on ramping (e.g., ramp rate limits), the BPS may be challenged to manage operating '
            'conditions within acceptable limits, particularly for very large load customers.',
            'ERCOT observed that large load consumption ramps quickly up and down when the price curve surpasses the '
            'estimated average strike price, as shown in Figure 2.7 [26].'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/wecc_large_loads_risk.pdf.txt',
  'agent_note': 'Uncontrolled fluctuations of large flexible loads are a detriment and ramp limits the remedy (large loads '
                'generally).'},
 {'id': 'F3:22',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Choukse et al., Power Stabilization for AI Training Datacenters',
  'title': 'Choukse et al. (Microsoft, OpenAI, NVIDIA), "Power Stabilization for AI Training Datacenters"',
  'version': 'arXiv:2508.14318 v2 (21 Aug 2025)',
  'url': 'https://arxiv.org/abs/2508.14318',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['Given the synchronous nature of these jobs, during every iteration there is a computation-heavy phase, where '
            'each GPU works on the local data, and a communication-heavy phase where all the GPUs synchronize on the data. '
            'Because compute-heavy phases require much more power than communication phases, large power swings occur.',
            'An even bigger challenge arises from the frequency spectrum of these power swings which, if harmonized with '
            'critical frequencies of utilities, can cause physical damage to the power grid infrastructure.',
            'Utility operators may impose time-domain constraints on how quickly a load may change its power draw. These '
            'constraints include: • Ramp-Up Rate: The maximum permitted rate of increase in power demand, typically '
            'expressed in megawatts per second (MW/s). • Ramp-Down Rate: The maximum permitted decrease in power '
            'consumption over time.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/arx_2508.14318v2.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('states')."},
 {'id': 'F3:23',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Google Cloud, Balance of power: power and thermal fluctuations in ML infrastructure',
  'title': 'Google Cloud (Gan & Ranganathan), "Balance of power: A full-stack approach to power and thermal fluctuations in '
           'ML infrastructure" (February 12, 2025)',
  'version': 'Google Cloud blog, February 12, 2025, fetched 2026-09-29 (cited by the NERC white paper above as its footnote '
             '16).',
  'url': 'https://cloud.google.com/blog/topics/systems/mitigating-power-and-thermal-fluctuations-in-ml-infrastructure',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['You can observe these power fluctuations when a workload launches or finishes, or when it is halted, then '
            'resumed or rescheduled.',
            'In fact, in our latest batch-synchronous ML workloads running on dedicated ML clusters, we observed power '
            'fluctuations in the tens of megawatts (MW), as shown in Fig.1. And compared to a traditional load variation '
            'profile, the ramp speed could be almost instantaneous, repeat as frequently as every few seconds, and last for '
            'weeks… or even months!'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/google_balance_of_power.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('states')."},
 {'id': 'F3:24',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Jensen et al., EasyRider',
  'title': 'Jensen et al. (Stanford), "EasyRider: Mitigating Power Transients in Datacenter-Scale Training Workloads"',
  'version': 'arXiv:2604.15522 v2 (11 Sep 2026)',
  'url': 'https://arxiv.org/abs/2604.15522',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['During synchronous communication, start-up, shut-down, and checkpointing, GPU power consumption can swing from '
            'peak to idle within milliseconds.',
            'These are not rare events—they occur every few seconds at the end of a training iteration, and (often '
            'unpredictably) every few minutes during checkpointing, restart, or a fault or collective stall.',
            'Cloud-computing datacenters run tens or hundreds of millions of different jobs, each of which is a tiny load; '
            'control planes such as Kubernetes [34] or Borg [63] stagger job starts over seconds, and the aggregate power '
            'use changes slowly over minutes or hours.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/arx_2604.15522v2.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('states')."},
 {'id': 'F3:25',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Chen et al., Electricity Demand and Grid Impacts of AI Data Centers',
  'title': 'Chen et al., "Electricity Demand and Grid Impacts of AI Data Centers: Challenges and Prospects"',
  'version': 'arXiv:2509.07218 v6 (4 Aug 2026)',
  'url': 'https://arxiv.org/abs/2509.07218',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['For instance, inference or training tasks deferred in response to high electricity prices may be rescheduled '
            'simultaneously once prices fall, leading to secondary demand peaks or rebound effects that stress the grid.',
            'In addition, tasks such as checkpointing, intermediate result saving, and large-scale data transfers between '
            'nodes can cause brief but pronounced spikes in electricity consumption; additional transient surges may occur '
            'when training is paused and resumed [12], [44].'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/arx_2509.07218v6.pdf.txt',
  'agent_note': 'States both clauses for AI load: deferred tasks rescheduled simultaneously cause secondary peaks '
                "(rebound), and surges when training is paused and resumed (a review's assertion with citations)."},
 {'id': 'F3:26',
  'family': 'F3',
  'tag': 'G2',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Chen et al., Electricity Demand and Grid Impacts of AI Data Centers',
  'title': 'Chen et al., "Electricity Demand and Grid Impacts of AI Data Centers: Challenges and Prospects"',
  'version': 'arXiv:2509.07218 v6 (4 Aug 2026)',
  'url': 'https://arxiv.org/abs/2509.07218',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['Moreover, AI data center operators can be relatively insensitive to electricity prices. As noted in [125], '
            'these facilities have high sunk capital costs, and the workloads they run are highly lucrative. As a result, '
            'the opportunity cost of deferring training or inference tasks can outweigh potential savings from energy '
            'arbitrage.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/arx_2509.07218v6.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('close')."},
 {'id': 'F3:27',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'bears',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Li, Beyond Scalar Flexibility',
  'title': 'Li, "Beyond Scalar Flexibility: From Eligible AI Workloads to Dependable Load Relief"',
  'version': 'arXiv:2609.05406 v1 (4 Sep 2026)',
  'url': 'https://arxiv.org/abs/2609.05406',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['Load relief is a power service rather than an energy saving. If every deferred megawatt-hour rebounds and the '
            'expected lost work equals half of a one-hour checkpoint interval, net energy change after a four-hour call is '
            '−12.5% of gross curtailed energy. For the full-realization 2.32 MW offer, that rebound contains 10.44 MWh. The '
            'mean noneligible workload power, defined as the floor plus shift layers, is 23.264 MW; absorbing the rebound '
            'at 10% of that level takes 4.49 hours. This rule implies 8.49 hours between four-hour calls and at most 19.8 '
            'calls per week.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/arx_2609.05406v1.pdf.txt',
  'agent_note': "The rebound is an accounting assumption ('If every deferred megawatt-hour rebounds'), energy to be "
                "absorbed rather than a stated risk. Family proposal 'states' lowered to 'bears'."},
 {'id': 'F3:28',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Mueller & Jansen, Large-Scale Demonstration of Precise Demand Response Provided by Residential Heating Systems',
  'title': 'Müller & Jansen, "Large-Scale Demonstration of Precise Demand Response Provided by Residential Heating Systems"',
  'version': 'arXiv:1806.07670 v1 (20 Jun 2018)',
  'url': 'https://arxiv.org/abs/1806.07670',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['In the experiment shown in the top plot, the throttling signals are released simultaneously at 12.00 h, i.e., '
            '∆T = 0, which results in a sharp load ramp and a peak rebound of 64.8 kW. In the second experiment, shown in '
            'the bottom plot, ∆T = 45 min was used to spread the individual release times (29). The rebound is reduced to '
            'values below 32.6 kW, which amounts to a peak rebound damping of 50%.',
            'Predicting the peak rebound power is challenging because it heavily depends on the degree of synchronization '
            'among the HPs when resuming operation.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/arx_1806.07670v1.pdf.txt',
  'agent_note': 'A measured rebound peak on synchronized release, halved by a staggered release. Named difference: heat '
                "pumps, not AI load. Family proposal 'states' lowered to 'close'."},
 {'id': 'F3:29',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'bears',
  'proposed_reading': 'contradicts',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Michaels Energy for Minnesota Dept. of Commerce, Demand Response Impact Study',
  'title': 'Michaels Energy for the Minnesota Department of Commerce, "Demand Response Impact Study" (May 1, 2013)',
  'version': 'report dated May 1, 2013 (PDF modified 2021-12-04), fetched 2026-09-29.',
  'url': 'https://michaelsenergy.com/wp-content/uploads/2021/12/DR-Snapback-Report.pdf',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['Snapback is the increase in energy and demand in the hours immediately following a demand response event.',
            'The technologies used for demand response that exhibit snapback are: air conditioner cycling, water heater '
            'curtailment, and electric heating cycling. Other technologies that are often used do not have snapback effects '
            'due to the nature of their operations. These include ice storage, electric heating thermal storage, and '
            'on-site generation.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/michaels_dr_snapback.pdf.txt',
  'agent_note': 'Snapback is found for thermal loads and not for storage or on-site generation; compute loads are not '
                "discussed, so G5 does not fail as written. Family proposal 'contradicts' lowered to 'bears'."},
 {'id': 'F3:30',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Chaudhary et al., Correlated AI Data-Center Load Episodes',
  'title': 'Chaudhary et al. (Michigan State), "Real-Time Edge-based Detection of Correlated AI Data-Center Load Episodes"',
  'version': 'arXiv:2608.22719 v1 (24 Aug 2026)',
  'url': 'https://arxiv.org/abs/2608.22719',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['When several facilities synchronize their training cycles, these load variations become spatially correlated '
            'and amplify the aggregate disturbance on the grid.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/arx_2608.22719v1.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('states')."},
 {'id': 'F3:31',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Zahedi et al. (Quanta), Best Practices for Large Load Interconnections',
  'title': 'Zahedi, Zamani & Anilkumar (Quanta Technology), "Best Practices for Large Load Interconnections: A North '
           'American Perspective on Data Centers"',
  'version': 'arXiv:2601.12686 v1 (19 Jan 2026)',
  'url': 'https://arxiv.org/abs/2601.12686',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['As shown in Table 1, Southern Company is the only company that enforces a numeric cap of ≤ 20 MW/min for load '
            'ramping under normal operation.',
            'while noting gaps in ride-through specifications, load-variation management, and post-disturbance recovery '
            'targets.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/arx_2601.12686v1.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F3:32',
  'family': 'F3',
  'tag': 'G5',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Mohammadi et al., Grid Integration of AI Data Centers: energy storage review',
  'title': 'Mohammadi et al., "Grid Integration of AI Data Centers: A Critical Review of Energy Storage Solutions"',
  'version': 'arXiv:2603.00415 v2 (5 May 2026)',
  'url': 'https://arxiv.org/abs/2603.00415',
  'dossier': 'docs/citations/dr1_f3_2026-09-29.md',
  'quote': ['At hyperscale, uncontrolled simultaneous recharge can create step increases in aggregate load that trip '
            'upstream protection.'],
  'raw_file': '/tmp/claude-0/dr1_src/F3/arx_2603.00415v2.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('close')."},
 {'id': 'F4:0',
  'family': 'F4',
  'tag': 'G3',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Kokolis et al., Revisiting Reliability in Large-Scale Machine Learning Research Clusters (HPCA 2025)',
  'title': 'Kokolis et al., "Revisiting Reliability in Large-Scale Machine Learning Research Clusters" (HPCA 2025)',
  'version': 'arXiv:2410.21680 v2 (6 Feb 2025)',
  'url': 'https://arxiv.org/abs/2410.21680',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['we consider three sources of unproductive scheduled time: 1) Catching up from last saved checkpoint: '
            'Re-training between the most recent checkpoint and a job interruption. 2) Restart overhead: all initialization '
            'tasks that need to be performed after a restart that wouldn’t otherwise be needed. 3) Checkpoint overhead: The '
            'time checkpointing adds to job runtime. All of these are highly job dependent, and we currently lack a '
            'reliable way for tracking either at scale with confidence.',
            'assuming Daly-Young optimal checkpointing with 5 minute restart overhead and 5 minute checkpoint write '
            'overhead.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2410.21680v2.pdf.txt',
  'agent_note': 'The interruption cost splits into lost work, restart overhead and checkpoint overhead; for a planned pause '
                'with a save the first term is zero, leaving about R plus the save. Named difference: the paper is about '
                "failures, and the zero lost-work step is the grader's. Family proposal 'states' lowered to 'close'."},
 {'id': 'F4:1',
  'family': 'F4',
  'tag': 'G2',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Kokolis et al. (HPCA 2025)',
  'title': 'Kokolis et al., "Revisiting Reliability in Large-Scale Machine Learning Research Clusters" (HPCA 2025)',
  'version': 'arXiv:2410.21680 v2 (6 Feb 2025)',
  'url': 'https://arxiv.org/abs/2410.21680',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['we assume that all jobs checkpoint hourly (we find this is a typical checkpoint interval for larger jobs on '
            'the RSC clusters), giving an average of half an hour of lost work.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2410.21680v2.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:2',
  'family': 'F4',
  'tag': 'G3',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': "Wang et al., GEMINI: Fast Failure Recovery in Distributed Training with In-Memory Checkpoints (SOSP '23)",
  'title': 'Wang et al., "GEMINI: Fast Failure Recovery in Distributed Training with In-Memory Checkpoints" (SOSP \'23)',
  'version': "SOSP '23, October 23–26, 2023, Koblenz, Germany (Rice University and Amazon Web Services); author copy at "
             'fetched 2026-09-29.',
  'url': 'https://www.cs.rice.edu/~eugeneng/papers/SOSP23.pdf',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['We define wasted time as the sum of the time spent on the lost training process before a failure and the time '
            'for retrieving the latest checkpoint during a failure recovery.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/gemini_sosp23.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('close')."},
 {'id': 'F4:3',
  'family': 'F4',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': "Wang et al., GEMINI (SOSP '23)",
  'title': 'Wang et al., "GEMINI: Fast Failure Recovery in Distributed Training with In-Memory Checkpoints" (SOSP \'23)',
  'version': "SOSP '23, October 23–26, 2023, Koblenz, Germany (Rice University and Amazon Web Services); author copy at "
             'fetched 2026-09-29.',
  'url': 'https://www.cs.rice.edu/~eugeneng/papers/SOSP23.pdf',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['However, existing solutions are restricted by the low bandwidth to remote persistent storage, resulting in '
            'significant failure recovery costs, i.e., taking up to tens of minutes to retrieve the checkpoint captured a '
            'few hours ago to resume the training.',
            'For example, it takes 42 minutes to checkpoint the model states of MT-NLG [68] to the remote persistent '
            'storage when the bandwidth is 20Gbps.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/gemini_sosp23.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:4',
  'family': 'F4',
  'tag': 'G3',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': "Jiang et al., MegaScale (NSDI '24)",
  'title': 'Jiang et al., "MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs" (NSDI \'24)',
  'version': 'arXiv:2402.15627 v1 (23 Feb 2024)',
  'url': 'https://www.usenix.org/system/files/nsdi24-jiang-ziheng.pdf',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['We conduct experiments on the same AI cluster in §6 and our empirical measurement indicates that the '
            'initialization time for Megatron-LM on 2,048 NVIDIA Ampere GPUs is approximately 1047 seconds. While this may '
            'appear relatively small compared to the training duration, it imposes a significant hurdle to routine testing '
            'and iterative development (e.g., minor code adjustments in hyperparameter tuning and debugging). It also '
            'hampers the implementation of fast restart-and-recovery mechanisms.',
            'The initialization time is reduced to under 5 seconds on 2048 GPUs, and to under 30 seconds on more than '
            '10,000 GPUs with those optimizations.',
            'Moreover, the system can catch up to the training progress prior to the crash within 15 minutes from the '
            'latest checkpoints, maintaining over 90% effective training time rate'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/megascale_nsdi24.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:5',
  'family': 'F4',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'contradicts',
  'reading_by': "grading agent; for the investigator's review",
  'source': "Jiang et al., MegaScale (NSDI '24)",
  'title': 'Jiang et al., "MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs" (NSDI \'24)',
  'version': 'arXiv:2402.15627 v1 (23 Feb 2024)',
  'url': 'https://www.usenix.org/system/files/nsdi24-jiang-ziheng.pdf',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['In the first stage, each GPU worker writes its on-chip states to the host memory, and then continues the '
            'training process. After the optimization of Pytorch’s serialization mechanism and the use of pinned memory, '
            'this process can be reduced to several seconds thanks to the high PCIe bandwidth, thereby minimally '
            'interrupting the ongoing training process. In the second stage, a background process takes over, '
            'asynchronously transferring the state from the host memory to a distributed file system'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/megascale_nsdi24.pdf.txt',
  'agent_note': 'The GPU part of a two-stage save takes seconds and the persist runs in the background: this narrows G6 (if '
                "hosts stay powered) without making it fail as written. Family proposal 'contradicts' lowered to 'bears'."},
 {'id': 'F4:6',
  'family': 'F4',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': "Wan et al., ByteCheckpoint (NSDI '25)",
  'title': 'Wan et al., "ByteCheckpoint: A Unified Checkpointing System for Large Foundation Model Development" (NSDI \'25)',
  'version': 'arXiv:2407.20143 v4 (2 Apr 2025)',
  'url': 'https://arxiv.org/abs/2407.20143',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['By analyzing our previous LFM training jobs, we observe that the average end-to-end time required to save '
            'checkpoints of a GPT 175B model, trained on 4096 GPUs, to HDFS can be 200 seconds. This duration substantially '
            'exceeds the time required for a single training iteration.',
            'ByteCheckpoint consistently maintained average checkpoint stalls under 600ms, even at the largest scale with '
            '8,960 GPUs.',
            'Table 8: I/O performance of ByteCheckpoint in large-scale LFM training. Model and Framework #GPUs Parallelism '
            'TBlock (s) TSave (s) TLoad (s) Vision Transformer 7B FSDP 1488 ZeRO-2 0.34 20.13 265.73 Text Transformer 405B '
            'Megatron-LM 8960 TP=8, DP=70, PP=16 0.59 51.06 129.49'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2407.20143v4.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:7',
  'family': 'F4',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'PyTorch blog (Meta, IBM Research), Reducing Model Checkpointing Times by Over 10x with PyTorch Distributed '
            'Asynchronous Checkpointing',
  'title': 'PyTorch blog (Meta and IBM Research), "Reducing Model Checkpointing Times by Over 10x with PyTorch Distributed '
           'Asynchronous Checkpointing"',
  'version': 'blog post by Lucas Pasqualin, Less Wright, Iris Zhang, Chien-Chin Huang (Meta) and Swaminathan Sundararaman, '
             'Saransh Gupta, Raghu Ganti (IBM Research). The page shows ...',
  'url': 'https://pytorch.org/blog/reducing-checkpointing-times/',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['Example: 7B model ‘down time’ for a checkpoint goes from an average of 148.8 seconds to 6.3 seconds, or 23.62x '
            'faster.',
            'As IBM Research had noted, torch.save could take up to 30 minutes to checkpoint a single 11B model (PyTorch '
            '1.13). With advancements in distributed checkpointing, checkpoints could be done in under 4 minutes for up to '
            '30B model sizes. With asynchronous checkpointing, the training time lost due to checkpointing now moves to '
            'under 30 seconds, and often as short as 6 seconds.',
            'The first phase copies the data from each gpu/rank from GPU to CPU. This is the visible downtime to the user '
            'and can take from 6 – 14 seconds for 7B-13B model sizes. The second phase asynchronously copies the data from '
            'CPU memory to disk to persist the checkpoint. Once data is copied to CPU in the first phase, the GPU is free '
            'to immediately resume training.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pytorch_async_dcp_blog.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:8',
  'family': 'F4',
  'tag': 'G3',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Llama Team, The Llama 3 Herd of Models',
  'title': 'Llama Team, AI @ Meta, "The Llama 3 Herd of Models"',
  'version': 'arXiv:2407.21783 v3 (23 Nov 2024)',
  'url': 'https://arxiv.org/abs/2407.21783',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['Moreover, the synchronous nature of training makes it less fault-tolerant—a single GPU failure may require a '
            'restart of the entire job. Despite these challenges, for Llama 3, we achieved higher than 90% effective '
            'training time while supporting automated cluster maintenance, such as firmware and Linux kernel upgrades '
            '(Vigraham and Leonhardi, 2024), which resulted in at least one training interruption daily.',
            'During a 54-day snapshot period of pre-training, we experienced a total of 466 job interruptions. Of these, 47 '
            'were planned interruptions due to automated maintenance operations such as firmware upgrades or operator- '
            'initiated operations like configuration or dataset updates.',
            'To increase the effective training time, we reduced job startup and checkpointing time, and developed tools '
            'for fast diagnosis and problem resolution.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2407.21783v3.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:9',
  'family': 'F4',
  'tag': 'G5',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Llama Team, The Llama 3 Herd of Models',
  'title': 'Llama Team, AI @ Meta, "The Llama 3 Herd of Models"',
  'version': 'arXiv:2407.21783 v3 (23 Nov 2024)',
  'url': 'https://arxiv.org/abs/2407.21783',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['During training, tens of thousands of GPUs may increase or decrease power consumption at the same time, for '
            'example, due to all GPUs waiting for checkpointing or collective communications to finish, or the startup or '
            'shutdown of the entire training job. When this happens, it can result in instant fluctuations of power '
            'consumption across the data center on the order of tens of megawatts, stretching the limits of the power '
            'grid.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2407.21783v3.pdf.txt',
  'agent_note': "States G5's swings clause (whole-job start-up or shutdown swings tens of MW); not the rebound clause."},
 {'id': 'F4:10',
  'family': 'F4',
  'tag': 'G3',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Gemini Team, Gemini: A Family of Highly Capable Multimodal Models',
  'title': 'Gemini Team, Google, "Gemini: A Family of Highly Capable Multimodal Models"',
  'version': 'arXiv:2312.11805 v5 (9 May 2025)',
  'url': 'https://arxiv.org/abs/2312.11805',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['Maintaining a high goodput2 at this scale would have been impossible using the conventional approach of '
            'periodic checkpointing of weights to persistent cluster storage. For Gemini models, we instead made use of '
            'redundant in-memory copies of the model state, and on any unplanned hardware failures, we rapidly recover '
            'directly from an intact model replica. Compared to both PaLM and PaLM-2 (Anil et al., 2023), this provided a '
            'substantial speedup in recovery time, despite the significantly larger training resources being used. As a '
            'result, the overall goodput for the largest-scale training job increased from 85% to 97%.',
            'We define goodput as the time spent computing useful new steps over the elapsed time of the training job.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2312.11805v5.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:11',
  'family': 'F4',
  'tag': 'G3',
  'reading': 'bears',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': "Mohan et al., CheckFreq (FAST '21)",
  'title': 'Mohan, Phanishayee & Chidambaram, "CheckFreq: Frequent, Fine-Grained DNN Checkpointing" (FAST \'21)',
  'version': '19th USENIX Conference on File and Storage Technologies, February 23–25, 2021, fetched 2026-09-29.',
  'url': 'https://www.usenix.org/system/files/fast21-mohan.pdf',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['Since model weights are constantly updated between iterations, checkpointing requires the training to brieﬂy '
            'pause to capture the model weights accurately. We term this overhead (i.e, the time GPU is idle, waiting for '
            'the checkpoint to complete) as the checkpoint stall.',
            'Our evaluation across a variety of models, GPUs, and storage types conﬁrms that CheckFreq reduces the wasted '
            'GPU time from order of hours to just under a minute, while incurring less than 3.5% runtime overhead, as '
            'compared to the existing epoch-based checkpointing schemes.',
            'Violating the data invariant during training can affect model accuracy. Each epoch performs a full pass over '
            'the dataset, in a random order and holds the invariant that each data item is seen exactly once per epoch.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/checkfreq_fast21.pdf.txt',
  'agent_note': 'Names what a lossless pause needs (consistent snapshot, restorable data iterator) but does not say the '
                "curtailment cost is about the restart overhead. Family proposal 'close' lowered to 'bears'."},
 {'id': 'F4:12',
  'family': 'F4',
  'tag': 'G3',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Gupta et al., Just-In-Time Checkpointing (EuroSys 2024), MSR publication page',
  'title': 'Gupta et al., "Just-In-Time Checkpointing: Low Cost Error Recovery from Deep Learning Training Failures" '
           '(EuroSys 2024)',
  'version': 'Microsoft Research publication page (European Conference on Computer Systems, April 2024), fetched 2026-09-30 '
             '00:00 UTC. The full paper was NOT REACHED: - redirected to ...',
  'url': 'https://www.microsoft.com/en-us/research/publication/just-in-time-checkpointing-low-cost-error-recovery-from-deep-learning-training-failures/',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['In this paper, we present a novel approach of just-in-time checkpointing when failures happen, which enables '
            'recovery from failures with just a single minibatch iteration of work replayed by all GPUs. This reduces the '
            'cost of error recovery from several minutes to a few seconds per GPU, with nearly zero steady state overhead.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/jit_msr_page.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('close')."},
 {'id': 'F4:13',
  'family': 'F4',
  'tag': 'G3',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': "Wan et al., Robust LLM Training Infrastructure at ByteDance (SOSP '25)",
  'title': 'Wan et al., "Robust LLM Training Infrastructure at ByteDance" (ByteRobust; SOSP \'25)',
  'version': 'arXiv:2509.16293 v4 (20 Oct 2025)',
  'url': 'https://arxiv.org/abs/2509.16293',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['We observed that the time cost of failover operations is often more than 10 minutes for the large model '
            'training at the scale of 10,000 GPUs.',
            'Fig. 2 shows the training loss and Model FLOPs Utilization (MFU) when training an LLM in a 1000-GPU cluster '
            'over a 10-day training span, during which a total of 28 runs were conducted (each run corresponds to a restart '
            'of the model training).'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2509.16293v4.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:14',
  'family': 'F4',
  'tag': 'G6',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': "Thorpe et al., Bamboo (NSDI '23)",
  'title': 'Thorpe et al., "Bamboo: Making Preemptible Instances Resilient for Affordable Training of Large DNNs" (NSDI '
           "'23)",
  'version': 'arXiv:2204.12013 v1 (26 Apr 2022)',
  'url': 'https://arxiv.org/abs/2204.12013',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['First, grace periods vary from cloud to cloud. While AWS spot instances have 2 minutes before preemption, GCP '
            'and Azure provide only 30 seconds, with GCP not even guaranteeing such a warning. For large models, this can '
            'be too short of a warning and may not leave sufﬁcient time to save model updates into a checkpoint.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2204.12013v1.pdf.txt',
  'agent_note': "G6's mechanism for cloud pre-emption: a 30 s to 2 min warning 'may not leave sufficient time to save model "
                "updates into a checkpoint'. Named difference: a pre-emption notice, not a DR dispatch."},
 {'id': 'F4:15',
  'family': 'F4',
  'tag': 'G3',
  'reading': 'bears',
  'proposed_reading': 'contradicts',
  'reading_by': "grading agent; for the investigator's review",
  'source': "Thorpe et al., Bamboo (NSDI '23)",
  'title': 'Thorpe et al., "Bamboo: Making Preemptible Instances Resilient for Affordable Training of Large DNNs" (NSDI '
           "'23)",
  'version': 'arXiv:2204.12013 v1 (26 Apr 2022)',
  'url': 'https://arxiv.org/abs/2204.12013',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['As shown, although checkpointing itself can be done efﬁciently, the restarting overheads (i.e., for adapting '
            'existing checkpoints to new pipeline conﬁgurations) and the wasted computations take 77% of the training '
            'time.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2204.12013v1.pdf.txt',
  'agent_note': '77 % of training time lost to restarts and wasted work under frequent bulk pre-emption with pipeline '
                "re-planning; the wasted work is unsaved work, which a lossless pause does not have. Does not make G3's "
                "per-event claim fail. Family proposal 'contradicts' lowered to 'bears'."},
 {'id': 'F4:16',
  'family': 'F4',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'AWS EC2 User Guide, Spot Instance interruption notices',
  'title': 'Amazon EC2 User Guide, "Spot Instance interruption notices"',
  'version': 'AWS documentation page (undated), fetched 2026-09-30 00:08 UTC.',
  'url': 'https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-instance-termination-notices.html',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['A Spot Instance interruption notice is a warning that is issued two minutes before Amazon EC2 stops or '
            'terminates your Spot Instance. If you specify hibernation as the interruption behavior, you receive an '
            'interruption notice, but you do not receive a two-minute warning because the hibernation process begins '
            'immediately.',
            'Interruption notices are emitted on a best effort basis.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/aws_spot_interruption_notices.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:17',
  'family': 'F4',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Google Cloud Compute Engine documentation, Spot VMs',
  'title': 'Google Cloud Compute Engine documentation, "Spot VMs" (and "Preemptible VM instances")',
  'version': 'Google Cloud documentation pages, "Last updated 2026-09-28 UTC"; requested at (redirected to and (redirected '
             'likewise); fetched 2026-09-30 00:08 UTC.',
  'url': 'https://cloud.google.com/compute/docs/instances/spot',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['120 seconds ( Preview ) : We recommend setting the preemption notice duration to 120 seconds for any workloads '
            'that need a dedicated duration or longer than 30 seconds to handle preemption. 0 seconds (default) : If the '
            "preemption notice duration for a Spot VM isn't specified or is set to 0, then there is no dedicated delay "
            'between detecting preemption in metadata and the ACPI G2 Soft Off signal.',
            'The shutdown period for Spot VMs is best effort and up to 30 seconds, which is shorter than the shutdown '
            'period for other instances .'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/gcp_spot_vms.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:18',
  'family': 'F4',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Kubernetes documentation, Pod Lifecycle',
  'title': 'Kubernetes documentation, "Pod Lifecycle"',
  'version': 'kubernetes.io documentation, page footer "Last modified July 27, 2026", fetched 2026-09-30 00:09 UTC.',
  'url': 'https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['The default terminationGracePeriodSeconds setting is 30 seconds. If the preStop hook is still running after '
            'the grace period expires, the kubelet requests a small, one-off grace period extension of 2 seconds.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/k8s_pod_lifecycle.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:19',
  'family': 'F4',
  'tag': 'G9',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Colangelo et al., Turning AI Data Centers into Grid-Interactive Assets (Phoenix field demonstration)',
  'title': 'Colangelo et al., "Turning AI Data Centers into Grid-Interactive Assets: Results from a Field Demonstration in '
           'Phoenix, Arizona"',
  'version': 'arXiv:2507.00909 v1 (1 Jul 2025)',
  'url': 'https://arxiv.org/abs/2507.00909',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['Our demonstration explored several control knobs to regulate power consumption: (a) power capping via the '
            'NVIDIA-System Management Interface (SMI), which primarily uses dynamic voltage frequency scaling (DVFS) to '
            'effectively reduce power with minor throughput impacts for many workloads [14] (Fig. 6); (b) job pausing '
            '(de-prioritization), which temporarily pauses running jobs for steep reductions in power, and (c) changing the '
            'allocated resources for jobs, which reduces the number of allocated GPUs to reduce power while allowing job '
            'progress.',
            'In particular, MPT pre-training jobs were notably [...] more sensitive in the mid-range of power caps, showing '
            'greater performance drops compared to fine-tuning and inference tasks. Control overhead of power capping is '
            'negligible, making real-time responsiveness feasible even in busy clusters.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2507.00909v1.pdf.txt',
  'agent_note': 'GRADE-DECIDING READING. In a field DR trial, power capping (minor throughput impact) and job pausing '
                '(steep reductions) are used side by side: the alternative and a different grid effect are stated. The '
                "energy clause of G9 ('different energy ... effects') is not in the quotes. Read strictly, a source that "
                "states part of the position is 'close'; the family proposal 'states' is lowered to 'close'. For the "
                "investigator's review: read as 'states', G9 would be REDUNDANT."},
 {'id': 'F4:20',
  'family': 'F4',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'contradicts',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Colangelo et al. (Phoenix field demonstration)',
  'title': 'Colangelo et al., "Turning AI Data Centers into Grid-Interactive Assets: Results from a Field Demonstration in '
           'Phoenix, Arizona"',
  'version': 'arXiv:2507.00909 v1 (1 Jul 2025)',
  'url': 'https://arxiv.org/abs/2507.00909',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['Both pausing and re-allocating resources for running jobs require checkpointing for training jobs to ensure '
            'forward progress and minimize the overhead associated with these knobs. Although prior work offers methods to '
            'optimize for long-term objectives where changes to control state incur a cost [15], we are able to treat '
            'checkpointing overhead as negligible for our relatively infrequent demand response events since training jobs '
            'often run for days (or even weeks) at a time.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2507.00909v1.pdf.txt',
  'agent_note': 'The trial treats checkpoint overhead as negligible for a cost reason (infrequent events, long jobs), not a '
                "timing one; it says nothing about the save against a response time. Family proposal 'contradicts' lowered "
                "to 'bears'."},
 {'id': 'F4:21',
  'family': 'F4',
  'tag': 'G9',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'McDonald et al., Great Power, Great Responsibility: Recommendations for Reducing Energy for Training Language '
            'Models',
  'title': 'McDonald et al., "Great Power, Great Responsibility: Recommendations for Reducing Energy for Training Language '
           'Models"',
  'version': 'arXiv:2205.09646 v1 (19 May 2022)',
  'url': 'https://arxiv.org/abs/2205.09646',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['For example, power-capping, which limits the maximum power a GPU can consume, can enable a 15% decrease in '
            'energy usage with marginal increase in overall computation time when training a transformer-based language '
            'model.',
            'Averaging across each choice of conﬁguration, a 150W bound on power utilization led to an average 13.7% '
            'decrease in energy usage and 6.8% increase in training time compared to the default maximum. Note from Figure '
            '2 that the 100W setting has signiﬁcantly longer training times (31.4% longer on average). A 200W limit '
            'corresponds with almost the same training time as a 250W limit but more modest energy savings than a 150W '
            'limit.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2205.09646v1.pdf.txt',
  'agent_note': 'Power capping trades a little time for energy, measured; named difference: the alternative is to full '
                "power, not to pausing. Family proposal 'states' lowered to 'close'."},
 {'id': 'F4:22',
  'family': 'F4',
  'tag': 'G9',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'You, Chung & Chowdhury, Zeus (NSDI 2023)',
  'title': 'You, Chung & Chowdhury, "Zeus: Understanding and Optimizing GPU Energy Consumption of DNN Training" (NSDI \'23)',
  'version': 'arXiv:2208.06102 v2 (29 Sep 2022)',
  'url': 'https://arxiv.org/abs/2208.06102',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['Setting a GPU’s power limit will have the device internally trigger dynamic voltage and frequency scaling '
            '(DVFS) such that its power draw does not exceed the power limit [69].',
            'We found that the optimal energy consumption (Power Limit Opt. in Figure 1) may happen at a lower power limit '
            'than the maximum and can reduce energy consumption by 3.0%–31.5%.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2208.06102v2.pdf.txt',
  'agent_note': "The energy side of throttling for single GPUs; no comparison with pausing. Family proposal 'states' "
                "lowered to 'close'."},
 {'id': 'F4:23',
  'family': 'F4',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': "Chung et al., Reducing Energy Bloat in Large Model Training (Perseus, SOSP '24)",
  'title': 'Chung et al., "Reducing Energy Bloat in Large Model Training" (Perseus; SOSP \'24)',
  'version': 'arXiv:2312.06902 v3 (23 Sep 2024)',
  'url': 'https://arxiv.org/abs/2312.06902',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['The SM frequency of NVIDIA GPUs can be set via NVML [4] in around 10 ms, which is much shorter than typical '
            'large model computation latencies.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2312.06902v3.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:24',
  'family': 'F4',
  'tag': 'G9',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': "Chung et al., Perseus (SOSP '24)",
  'title': 'Chung et al., "Reducing Energy Bloat in Large Model Training" (Perseus; SOSP \'24)',
  'version': 'arXiv:2312.06902 v3 (23 Sep 2024)',
  'url': 'https://arxiv.org/abs/2312.06902',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['Evaluation on large models, including GPT-3 and Bloom, shows that Perseus reduces the energy consumption of '
            'large model training by up to 30% without any throughput loss or hardware modification.',
            'This is typically not the lowest frequency, because computations running with very low frequencies incur more '
            'latency increase than power reduction, resulting in higher energy consumption.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2312.06902v3.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:25',
  'family': 'F4',
  'tag': 'G9',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Patel et al., POLCA: Power Oversubscription in LLM Cloud Providers',
  'title': 'Patel et al., "POLCA: Power Oversubscription in LLM Cloud Providers" (Microsoft)',
  'version': 'arXiv:2308.12908 v1 (24 Aug 2023)',
  'url': 'https://arxiv.org/abs/2308.12908',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['For Flan-T5 and GPT- NeoX, frequency capping reduces the peak server power by 22% while only impacting the '
            'performance by 10%.',
            'Frequency capping is more effective in reclaiming larger amount of peak power, and power capping introduces '
            'more performance variability with less control over computation.',
            'Parameter Value Number of servers 40 Server type DGX-A100 Power telemetry delay 2s Power brake latency 5s OOB '
            'commands latency 40s Table 1: Default row-level parameters for our study.',
            '(3) Power brake, which is a fast lever (Table 1) to bring the GPU down to almost a halt, stopping all '
            'progress.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2308.12908v1.pdf.txt',
  'agent_note': 'Frequency capping (22 % peak power for 10 % performance) beside a power brake that stops all progress; '
                "power-oversubscription levers, not grid events, and no energy comparison. Family proposal 'states' lowered "
                "to 'close'."},
 {'id': 'F4:26',
  'family': 'F4',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Patel et al., POLCA',
  'title': 'Patel et al., "POLCA: Power Oversubscription in LLM Cloud Providers" (Microsoft)',
  'version': 'arXiv:2308.12908 v1 (24 Aug 2023)',
  'url': 'https://arxiv.org/abs/2308.12908',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['Parameter Value Number of servers 40 Server type DGX-A100 Power telemetry delay 2s Power brake latency 5s OOB '
            'commands latency 40s Table 1: Default row-level parameters for our study.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2308.12908v1.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:27',
  'family': 'F4',
  'tag': 'G6',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Choukse et al., Power Stabilization for AI Training Datacenters',
  'title': 'Choukse et al., "Power Stabilization for AI Training Datacenters" (Microsoft, OpenAI, NVIDIA)',
  'version': 'arXiv:2508.14318 v2 (21 Aug 2025)',
  'url': 'https://arxiv.org/abs/2508.14318',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['The challenge with a useful job is that the job’s state would need to be saved and restored, causing '
            'additional delay in power smoothing, and performance impact to the primary workload. An artificial workload '
            'would avoid such challenges, with the downside of wasted energy.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2508.14318v2.pdf.txt',
  'agent_note': "The state save and restore delay is named as a reason not to swap useful jobs for power control: G6's "
                'mechanism in a power-smoothing setting, not DR.'},
 {'id': 'F4:28',
  'family': 'F4',
  'tag': 'G9',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NVIDIA nvidia-smi documentation',
  'title': 'NVIDIA, "nvidia-smi" documentation (NVIDIA System Management Interface)',
  'version': 'NVIDIA documentation page (copyright 2011–2026; its change log begins "Changes between nvidia-smi v610 Update '
             'and v595"), fetched 2026-09-29.',
  'url': 'https://docs.nvidia.com/deploy/nvidia-smi/index.html',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['-pl, --power-limit=POWER_LIMIT Specifies maximum power limit in watts. Accepts integer and floating point '
            'numbers. it takes an optional argument --scope. Only on supported devices from Kepler family. Value needs to '
            'be between Min and Max Power Limit as reported by nvidia-smi. Requires root.',
            'SW Power Cap SW Power Scaling algorithm is reducing the clocks below requested clocks because the GPU is '
            'consuming too much power. E.g. SW power cap limit can be changed with nvidia-smi --power-limit=<Power Limit '
            'Value in W>'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/nvidia_smi_docs.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:29',
  'family': 'F4',
  'tag': 'G9',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NVIDIA Technical Blog, How New GB300 NVL72 Features Provide Steady Power for AI',
  'title': 'NVIDIA Technical Blog, "How New GB300 NVL72 Features Provide Steady Power for AI"',
  'version': 'NVIDIA Developer blog, datePublished 2025-07-28, dateModified 2025-08-27 (page metadata), fetched 2026-09-29.',
  'url': 'https://developer.nvidia.com/blog/how-new-gb300-nvl72-features-provide-steady-power-for-ai/',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['With the new power cap feature, GPU power draw at the start of a workload is capped by the power controller. '
            'New maximum power levels are sent to the GPUs and gradually increased, aligning with the ramp rates the grid '
            'can tolerate.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/nvidia_gb300_power_blog.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:30',
  'family': 'F4',
  'tag': 'G5',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NVIDIA Technical Blog, GB300 NVL72 steady power',
  'title': 'NVIDIA Technical Blog, "How New GB300 NVL72 Features Provide Steady Power for AI"',
  'version': 'NVIDIA Developer blog, datePublished 2025-07-28, dateModified 2025-08-27 (page metadata), fetched 2026-09-29.',
  'url': 'https://developer.nvidia.com/blog/how-new-gb300-nvl72-features-provide-steady-power-for-ai/',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['If power demand suddenly ramps up, it can take one minute to 90 minutes for generation resources to respond '
            'because of physical limitations in their ramp rates.',
            'The burner keeps using constant power as it waits for the workload to resume; if the workload doesn’t resume, '
            'the burner smoothly reduces the power consumption.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/nvidia_gb300_power_blog.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:31',
  'family': 'F4',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Eisenman et al., Check-N-Run',
  'title': 'Eisenman et al., "Check-N-Run: A Checkpointing System for Training Deep Learning Recommendation Models"',
  'version': 'arXiv:2010.08679 v2 (4 May 2021)',
  'url': 'https://arxiv.org/abs/2010.08679',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['For instance, creating a snapshot (in CPU DRAM) of a typical model residing in the GPU memory and partitioned '
            'across 16 nodes, each with 8 GPUs (total of 128 GPUs), would stall training in our system for less than 7 '
            'seconds. When check- [...] pointing every 30 minutes (our default), stall time would be a negligible fraction '
            '(< 0.4%).'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2010.08679v2.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:32',
  'family': 'F4',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': "Maurya et al., DataStates-LLM (HPDC '24)",
  'title': 'Maurya et al., "DataStates-LLM: Lazy Asynchronous Checkpointing for Large Language Models" (HPDC \'24)',
  'version': 'arXiv:2406.10707 v1 (15 Jun 2024)',
  'url': 'https://arxiv.org/abs/2406.10707',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['For example, Gemini [43] reports 3.13 GB/s checkpointing throughput (9.4 GB shard of GPT-100B takes about 3 '
            'seconds for checkpointing). REFT [42] reports 38% PCIe bandwidth utilization at 6 GB/s, while TRANSOM’s '
            'checkpointing engine (TCE) [45] reports achieving a throughput of ∼1.2 GB/s. Nebula [23], which is Microsoft’s '
            'DeepSpeed closed-source implementation of asynchronous checkpointing and is only available on the Azure cloud, '
            'reports achieving 1-4 GB/s (GPT2-XL checkpoint of 20.6 GB takes 5 seconds to checkpoint).'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2406.10707v1.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:33',
  'family': 'F4',
  'tag': 'G3',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Wang et al., FastPersist',
  'title': 'Wang, Ruwase, Xie & He, "FastPersist: Accelerating Model Checkpointing in Deep Learning"',
  'version': 'arXiv:2406.13768 v1 (19 Jun 2024)',
  'url': 'https://arxiv.org/abs/2406.13768',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['In practice, users reduce checkpointing frequency (e.g., every 10s/100s iterations) in order to limit the '
            'performance impact on training (e.g., 10% of training time is widely accepted as a reasonably low overhead '
            '[50]). However, this approach also increases the amount of computation and time lost to training '
            'interruptions.',
            'Our evaluation using real world dense and sparse DL models shows that FastPersist creates checkpoints in '
            'persistent storage up to 116x faster than baseline, and enables per-iteration checkpointing with negligible '
            'overhead.'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2406.13768v1.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F4:34',
  'family': 'F4',
  'tag': 'G3',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Liang et al., TorchTitan',
  'title': 'Liang et al., "TorchTitan: One-stop PyTorch native solution for production ready LLM pre-training"',
  'version': 'arXiv:2410.06511 v3 (7 Jun 2025)',
  'url': 'https://arxiv.org/abs/2410.06511',
  'dossier': 'docs/citations/dr1_f4_2026-09-29.md',
  'quote': ['TorchTitan utilizes DCP’s asynchronous checkpointing to reduce the checkpointing overhead by 5-15x compared to '
            'synchronous distributed checkpointing for the Llama 3.1 8B model (PyTorch Team, 2024b).'],
  'raw_file': '/tmp/claude-0/dr1_src/F4/pdf_2410.06511v3.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:0',
  'family': 'F5',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'FERC order accepting SPP CHILLS (ER26-1323)',
  'title': "FERC, order accepting SPP's Conditional High Impact Large Load Service (CHILLS), Docket ER26-1323",
  'version': '195 FERC ¶ 61,196, "Order Accepting Tariff Revisions, Subject to Condition", issued June 5, 2026, Docket Nos. '
             'ER26-1323-000/-001 (Document Accession #20260605-3090), as ...',
  'url': 'https://spp.org/documents/76880/20260605_order%20-%20revisions%20to%20add%20the%20conditional%20high%20impact%20large%20load%20service_er26-1323.pdf',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['Southwest Power Pool, Inc. (SPP) submitted proposed revisions to its Open Access Transmission Tariff (Tariff) '
            'to add a new type of non-firm transmission service called Conditional High Impact Large Load Service (CHILLS).',
            'According to SPP, depending on the size, scope, and availability of materials, completing network upgrades '
            'often requires six years or more.',
            'SPP states that CHILLS is subject to curtailment and interruption on a non-discriminatory basis when the '
            'transmission system is constrained or under emergency or other unforeseen conditions.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/spp_chills_order.pdf.txt',
  'agent_note': 'A FERC-accepted tariff trades curtailability for transmission service now, on spare capacity; it '
                'establishes the trade for one product but does not say access is the main commercial value or compare it '
                "with event payments. Family proposal 'states' lowered to 'close'."},
 {'id': 'F5:1',
  'family': 'F5',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'FERC order accepting SPP CHILLS (ER26-1323)',
  'title': "FERC, order accepting SPP's Conditional High Impact Large Load Service (CHILLS), Docket ER26-1323",
  'version': '195 FERC ¶ 61,196, "Order Accepting Tariff Revisions, Subject to Condition", issued June 5, 2026, Docket Nos. '
             'ER26-1323-000/-001 (Document Accession #20260605-3090), as ...',
  'url': 'https://spp.org/documents/76880/20260605_order%20-%20revisions%20to%20add%20the%20conditional%20high%20impact%20large%20load%20service_er26-1323.pdf',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['(3) not register as a demand response resource; (4) not be a demand response load; (5) not be a critical load;',
            'For the third and fourth requirements, SPP states that transmission customers receiving CHILLS should not be '
            'eligible to participate in the market for demand response because they are receiving a reduced level of '
            'transmission service with a different rate structure and a different curtailment priority.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/spp_chills_order.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:2',
  'family': 'F5',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'PJM Board decisional letter, CIFP large load additions',
  'title': 'PJM Board, decisional letter on the Critical Issue Fast Path for large load additions',
  'version': 'letter from the PJM Board of Managers (David Mills, Interim President & CEO) to stakeholders, dated January '
             '16, 2026, fetched 2026-09-29.',
  'url': 'https://www.pjm.com/-/media/DotCom/about-pjm/who-we-are/public-disclosures/2026/20260116-pjm-board-letter-re-results-of-the-cifp-process-large-load-additions.pdf',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['Under this framework, the incremental demand associated with such load growth would be subject to curtailment '
            'prior to the deployment of pre-emergency Demand Response. This will help to preserve Demand Response as a '
            'valuable reliability tool by not disrupting its business model through a dramatic increase in its use and will '
            'provide an incentive for new load to secure capacity or provide flexibility.',
            'the Board encourages voluntary “Bring Your Own New Generation” (BYONG) and directs the PJM staff to implement '
            'its proposal and associated matrix components related to the Expedited Interconnection Track5 that will serve '
            'as an alternate path for any entity seeking to mitigate curtailment risk by bringing their own new generation '
            'to the system on an accelerated basis.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/pjm_board_letter_20260116.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('close')."},
 {'id': 'F5:3',
  'family': 'F5',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'FERC order instituting proceeding, PJM (EL26-67)',
  'title': 'FERC, order instituting proceeding under FPA section 206, PJM (Docket EL26-67)',
  'version': '195 FERC ¶ 61,211, issued June 18, 2026 (file name dated 20260618), Docket No. EL26-67-000, as posted by PJM '
             'at fetched 2026-09-29.',
  'url': 'https://www.pjm.com/-/media/DotCom/documents/ferc/orders/2026/20260618-el26-67-000.pdf',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['(c) transmission services that reflect Eligible Customers taking transmission service on behalf of flexible '
            'large loads that are willing and able to limit their use of the transmission system under certain conditions;',
            '“[D]ata centers have characteristics unlike more traditional loads [including] size, strong desire for faster '
            'interconnection, and potential flexibility.”',
            '“[t]his willingness to curtail would potentially allow them to obtain service more quickly”'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/pjm_el26-67_order.pdf.txt',
  'agent_note': "Willingness to curtail 'would potentially allow them to obtain service more quickly' and data centres' "
                "'strong desire for faster interconnection': the trade, not a ranking above event payments. Family proposal "
                "'states' lowered to 'close'."},
 {'id': 'F5:4',
  'family': 'F5',
  'tag': 'G8',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Texas SB 6 (89R), enrolled',
  'title': 'Texas Senate Bill 6 (89th Legislature, Regular Session), enrolled version',
  'version': '"89(R) SB 6 - Enrolled version - Bill Text", fetched 2026-09-30. The signing date is not on the fetched page '
             '(Relae, below, gives June 20, 2025; not checked against the ...',
  'url': 'https://capitol.texas.gov/tlodocs/89R/billtext/html/SB00006F.htm',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['develops a protocol, including the installation of any necessary equipment or technology before the customer '
            'is interconnected, to allow the load to be curtailed during firm load shed.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/tx_sb6_enrolled.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:5',
  'family': 'F5',
  'tag': 'G6',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Texas SB 6 (89R), enrolled',
  'title': 'Texas Senate Bill 6 (89th Legislature, Regular Session), enrolled version',
  'version': '"89(R) SB 6 - Enrolled version - Bill Text", fetched 2026-09-30. The signing date is not on the fetched page '
             '(Relae, below, gives June 20, 2025; not checked against the ...',
  'url': 'https://capitol.texas.gov/tlodocs/89R/billtext/html/SB00006F.htm',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['(2) ensure that the independent organization provides at least a 24-hour notice to large load customers and '
            'requires each large load to remain curtailed for the duration of the energy emergency alert event or until the '
            'load can be recalled safely; and (3) prohibit participation by any large load customer that curtails in '
            'response to the wholesale price of electricity'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/tx_sb6_enrolled.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:6',
  'family': 'F5',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'PG&E Currents, Why Grid Flexibility Is Now Essential',
  'title': 'PG&E Currents, "Why Grid Flexibility Is Now Essential — and How PG&E Is Delivering It"',
  'version': 'PG&E newsroom article by Rachel Sarah, dated May 06, 2026, fetched 2026-09-30.',
  'url': 'https://www.pge.com/en/newsroom/currents/future-of-energy/why-grid-flexibility-is-now-essential---and-how-pg-e-is-deliveri.html',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['This solution allows a site to connect sooner, while PG&E completes necessary long-term infrastructure '
            'upgrades in the area. In many cases, it helped projects move ahead by 18–24 months.',
            'T-Flex would allow large, flexible loads like data centers to connect sooner by adjusting usage during rare '
            'grid constraints, instead of waiting years for upgrades.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/pge_flex_newsroom.html.txt',
  'agent_note': 'Flex Connect moved projects ahead 18-24 months and T-Flex proposes the trade for data centres; not ranked '
                "above event payments. Family proposal 'states' lowered to 'close'."},
 {'id': 'F5:7',
  'family': 'F5',
  'tag': 'G5',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'PG&E Currents, Why Grid Flexibility Is Now Essential',
  'title': 'PG&E Currents, "Why Grid Flexibility Is Now Essential — and How PG&E Is Delivering It"',
  'version': 'PG&E newsroom article by Rachel Sarah, dated May 06, 2026, fetched 2026-09-30.',
  'url': 'https://www.pge.com/en/newsroom/currents/future-of-energy/why-grid-flexibility-is-now-essential---and-how-pg-e-is-deliveri.html',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['Large data centers can change their load quickly—and at huge scale. If those shifts happen without visibility '
            'or planning, they can affect voltage and frequency and increase reliability risk.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/pge_flex_newsroom.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:8',
  'family': 'F5',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Utility Dive, PG&E Flex Connect pilot (Martucci)',
  'title': 'Utility Dive, "PG&E sees rising interest in \'customer-driven\' flexible interconnection pilot" (Martucci, '
           '2026)',
  'version': 'Dive Brief published Sept. 2, 2026, fetched 2026-09-30.',
  'url': 'https://www.utilitydive.com/news/pge-sees-rising-interest-in-customer-driven-flexible-interconnection-pil/829447/',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['The Flex Connect program allows larger distribution-connected loads to energize in months instead of waiting '
            '“several years” for firm interconnection, the Northern California utility says.',
            'Active Flex Connect participants have seen operational loads impacted less than 1% of the time during “the '
            'rare confluence of events” when the local grid is constrained and their demand remains high',
            'Most active and potential Flex Connect sites range from 2 MW to 5 MW, though some data center and '
            'manufacturing prospects push 10 MW, he said.',
            'Collins said two Flex Connect customers have so far “graduated” out of the pilot after an average wait of '
            'about 18 months.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/utilitydive_pge_flex.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('close')."},
 {'id': 'F5:9',
  'family': 'F5',
  'tag': 'G8',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Ofgem, Proposed data centre connection reforms',
  'title': 'Ofgem, "Proposed data centre connection reforms" (consultation)',
  'version': 'Ofgem consultation page, publication date 29 July 2026, closed 17 September 2026 (status "Closed (awaiting '
             'decision)"), fetched 2026-09-30.',
  'url': 'https://www.ofgem.gov.uk/consultation/proposed-data-centre-connection-reforms',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['We are consulting on proposals to reduce the number of non-viable projects in the connections queue. These two '
            'proposals are to introduce a new data centre commitment fee and data centre queue management milestones.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/ofgem_dc_reforms.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:10',
  'family': 'F5',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Norris et al., Rethinking Load Growth (Duke Nicholas Institute)',
  'title': 'Norris, Profeta, Patino-Echeverri & Cowie-Haskell, "Rethinking Load Growth" (Duke Nicholas Institute, 2025)',
  'version': 'Nicholas Institute report, February 2025. Fetched copy: the copy filed as "JNGO Ex. 2.08" in Illinois '
             'Commerce Commission Docket Nos. 25-0677/25-0679 (consol.), fetched ...',
  'url': 'https://www.icc.illinois.gov/docket/P2025-0679/documents/371138/files/650737.pdf',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['The most time-intensive and costly infrastructure upgrades required for new interconnections are often '
            'associated with expanding the transmission system to deliver electricity during the most stressed grid '
            'conditions (Gorman et al. 2024).',
            'For loads that pay for firm interconnection service, any period requiring occasional curtailment would be '
            'temporary, ending once necessary network upgrades are completed.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/duke_rlg_icc.pdf.txt',
  'agent_note': 'Costly upgrades are tied to stressed conditions and curtailment for firm-service loads ends when upgrades '
                "are done; the report does not rank faster connection above event payments. Family proposal 'states' "
                "lowered to 'close'."},
 {'id': 'F5:11',
  'family': 'F5',
  'tag': 'G7',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Norris et al., Rethinking Load Growth (Duke Nicholas Institute)',
  'title': 'Norris, Profeta, Patino-Echeverri & Cowie-Haskell, "Rethinking Load Growth" (Duke Nicholas Institute, 2025)',
  'version': 'Nicholas Institute report, February 2025. Fetched copy: the copy filed as "JNGO Ex. 2.08" in Illinois '
             'Commerce Commission Docket Nos. 25-0677/25-0679 (consol.), fetched ...',
  'url': 'https://www.icc.illinois.gov/docket/P2025-0679/documents/371138/files/650737.pdf',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['At the same time, financial incentives provided by most demand response programs have historically been modest '
            'and insufficient to offset the expenses and opportunity costs associated with curtailed operations. For '
            'operators focused on maintaining high utilization rates and controlling costs, the economic proposition of '
            'demand response participation may be unattractive.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/duke_rlg_icc.pdf.txt',
  'agent_note': "DR incentives 'modest and insufficient to offset the expenses and opportunity costs associated with "
                "curtailed operations'; for data centres generally."},
 {'id': 'F5:12',
  'family': 'F5',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'contradicts',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Norris et al., Rethinking Load Growth (Duke Nicholas Institute)',
  'title': 'Norris, Profeta, Patino-Echeverri & Cowie-Haskell, "Rethinking Load Growth" (Duke Nicholas Institute, 2025)',
  'version': 'Nicholas Institute report, February 2025. Fetched copy: the copy filed as "JNGO Ex. 2.08" in Illinois '
             'Commerce Commission Docket Nos. 25-0677/25-0679 (consol.), fetched ...',
  'url': 'https://www.icc.illinois.gov/docket/P2025-0679/documents/371138/files/650737.pdf',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['A company generated more revenue from its demand response participation in ERCOT than from Bitcoin mining in '
            'one month, at times accommodating a 95% load reduction during peak demands (Riot Platforms 2023).'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/duke_rlg_icc.pdf.txt',
  'agent_note': 'GRADE-DECIDING READING. A bitcoin miner earned more from ERCOT DR than from mining in one month: a '
                'scarcity-month exception for a load whose product earns far less per MWh than AI compute. G7 is about '
                'payments against the compute cost of a training fleet; this case does not make that fail as written. '
                "Family proposal 'contradicts' read as 'bears'; for the investigator's review, 'contradicts' would make "
                "G7's answer MIXED."},
 {'id': 'F5:13',
  'family': 'F5',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Camus, encoord & Princeton ZERO Lab, Flexible Data Centers (blog + executive summary)',
  'title': 'Camus, encoord & Princeton ZERO Lab, "Flexible Data Centers: A Faster, More Affordable Path to Power" (2025)',
  'version': '(a) encoord blog post dated 2025-12-04, fetched 2026-09-29; (b) the executive summary PDF, December 2025, '
             'fetched 2026-09-29. The study was funded by Google, which ...',
  'url': 'https://www.encoord.com/resources/blog/flexible-data-centers-study',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['New research from Camus, encoord, and Princeton ZERO Lab, funded by Google, shows how flexible grid '
            'connections and bring-your-own capacity (BYOC) can accelerate data center interconnection by 3–5 years while '
            'maintaining reliability and protecting ratepayers.',
            'Data centers across the United States face 3–7-year delays connecting to the electric grid—far longer than the '
            '18-24 months required to build new facilities.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/encoord_blog.html.txt',
  'agent_note': 'The value of flexibility is stated in years of earlier operation; no event payment is compared '
                "(Google-funded). Family proposal 'states' lowered to 'close'. Quotes from the blog copy only."},
 {'id': 'F5:14',
  'family': 'F5',
  'tag': 'G7',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Cox, Schwartz & Stenclik (GridLab/Telos), NV Energy data-centre flexibility case study',
  'title': 'Cox, Schwartz & Stenclik (GridLab / Telos Energy), "Bringing Data Center Flexibility into Resource Adequacy '
           'Planning: A Case Study of NV Energy"',
  'version': 'slide report dated September 2025, (linked from datePublished 2025-09-23, dateModified 2026-09-23), fetched '
             '2026-09-30.',
  'url': 'https://gridlab.org/wp-content/uploads/2025/09/GridLab_Telos_Data-Center-Flexibility_Final_Update1_ReducedSize.pdf',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['Market prices or traditional demand response programs are unlikely to be sufficient to incentivize data center '
            'flexibility due to high willingness to pay for electricity.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/gridlab_telos_nve_report.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('states')."},
 {'id': 'F5:15',
  'family': 'F5',
  'tag': 'G8',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Cox, Schwartz & Stenclik (GridLab/Telos), NV Energy data-centre flexibility case study',
  'title': 'Cox, Schwartz & Stenclik (GridLab / Telos Energy), "Bringing Data Center Flexibility into Resource Adequacy '
           'Planning: A Case Study of NV Energy"',
  'version': 'slide report dated September 2025, (linked from datePublished 2025-09-23, dateModified 2026-09-23), fetched '
             '2026-09-30.',
  'url': 'https://gridlab.org/wp-content/uploads/2025/09/GridLab_Telos_Data-Center-Flexibility_Final_Update1_ReducedSize.pdf',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['Market prices or traditional demand response programs are unlikely to be sufficient to incentivize data center '
            'flexibility due to high willingness to pay for electricity.',
            'Instead, flexibility should be incentivized in terms of avoided capital ($/MW) and accelerated '
            'interconnection, before interconnecting the data center to the grid.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/gridlab_telos_nve_report.pdf.txt',
  'agent_note': 'Sets avoided capital and accelerated interconnection against market prices and traditional DR programmes '
                "as the incentive: a planners' recommendation from one utility's case study."},
 {'id': 'F5:16',
  'family': 'F5',
  'tag': 'G2',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Khanal et al., Shift or curtail?',
  'title': 'Khanal et al., "Shift or curtail? How much data-center flexibility is worth depends on the host power grid"',
  'version': 'arXiv:2608.19622 v1 (20 Aug 2026)',
  'url': 'https://arxiv.org/abs/2608.19622',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['Fully interruptible load is the lowest-cost option in both systems, but its value depreciates when reliability '
            'limits, event-shape constraints and the opportunity cost of forgone compute are introduced.',
            'Flexibility adders represent the value of compute displaced in time or space rather than lost.',
            'The flexible tier carries an adder for compute shifted in time and a smaller one for compute shifted in space. '
            'Interruption carries none, since the interruptible tier is constrained instead by its annual energy budget.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/arx_2608.19622v1.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:17',
  'family': 'F5',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Khanal et al., Shift or curtail?',
  'title': 'Khanal et al., "Shift or curtail? How much data-center flexibility is worth depends on the host power grid"',
  'version': 'arXiv:2608.19622 v1 (20 Aug 2026)',
  'url': 'https://arxiv.org/abs/2608.19622',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['Utilities, grid operators and regulators are developing mechanisms to capture one or multiple flexibility '
            'tiers, allowing data centers to trade operational flexibility for faster or more favorable interconnection '
            'terms [7, 10].'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/arx_2608.19622v1.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('close')."},
 {'id': 'F5:18',
  'family': 'F5',
  'tag': 'G8',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Lu & Xu, Grid Integration of Gigawatt-Scale AI Data Centers under Connect-and-Manage',
  'title': 'Lu & Xu, "Grid Integration of Gigawatt-Scale AI Data Centers under Connect-and-Manage" (abstract only)',
  'version': 'arXiv:2605.14109 v1 (13 May 2026)',
  'url': 'https://arxiv.org/abs/2605.14109',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['Emerging connect-and-manage interconnection practices allow gigawatt-scale artificial intelligence data '
            'centers (AIDCs) to connect to the transmission network without prior network upgrades, at the cost of '
            'real-time curtailment during grid stress.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/abs_2605.14109.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('close')."},
 {'id': 'F5:19',
  'family': 'F5',
  'tag': 'G7',
  'reading': 'states',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Relae (ex Carbon Direct), The $5.5 Billion-Dollar Case for Enabling Data Center Load Flexibility',
  'title': 'Relae (formerly Carbon Direct Inc., per the page), "The $5.5 Billion-Dollar Case for Enabling Data Center Load '
           'Flexibility"',
  'version': 'article by Jonathan Goldberg, Douglas Bryan and Liam Kilroy, "Published March 20, 2026 \\ Last Updated '
             'September 21, 2026"; requested at which redirects to fetched ...',
  'url': 'https://carbon-direct.com/insights/the-billion-dollar-case-for-enabling-data-center-load-flexibility',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['In an AI compute arms race, the value of uninterrupted compute time far exceeds any available curtailment '
            'payment, such as via PJM’s capacity market mechanisms.',
            'Innovators like Emerald AI have demonstrated a 25% power reduction across a 256-GPU cluster over three hours '
            'during an Arizona grid stress event, while preserving compute service quality, helping to bridge the valuation '
            'asymmetry between energy and compute.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/carbondirect_5p5bn.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('states')."},
 {'id': 'F5:20',
  'family': 'F5',
  'tag': 'G8',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Relae/Carbon Direct Capital page (passage of uncertain article attribution)',
  'title': 'Relae (formerly Carbon Direct Inc., per the page), "The $5.5 Billion-Dollar Case for Enabling Data Center Load '
           'Flexibility"',
  'version': 'article by Jonathan Goldberg, Douglas Bryan and Liam Kilroy, "Published March 20, 2026 \\ Last Updated '
             'September 21, 2026"; requested at which redirects to fetched ...',
  'url': 'https://carbon-direct.com/insights/the-billion-dollar-case-for-enabling-data-center-load-flexibility',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['Electricity is slightly over 10% of total costs in our model: a 50% increase in power price reduces '
            'equity-level returns by less than 2%. Access to power, speed of interconnection, and equipment availability '
            'matter more.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/carbondirect_5p5bn.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:21',
  'family': 'F5',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Giga Energy, How to earn $60-80k per MW per year (Holliday)',
  'title': 'Giga Energy, "Maximizing data center profit margins: How to earn $60-80k per MW per year" (Holliday, 2026)',
  'version': 'vendor blog post by Clay Holliday dated 1.12.2026 (page metadata "Jan 12"; modified "May 13"), fetched '
             '2026-09-30.',
  'url': 'https://www.gigaenergy.com/blog/data-center-profit-margin',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['Flexible load data centers can earn $60-80k per MW annually through participation in energy markets. When grid '
            'prices spike above compute economics, the grid will pay you to curtail.',
            'The economics are simple: when the grid values your megawatt hours more than the bitcoin network does, you '
            'should sell power instead of consuming it.',
            'that same facility can generate approximately $3.25 million in additional gross annual revenue (calculated at '
            'an average of $65,000 per MW).'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/gigaenergy_profit.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:22',
  'family': 'F5',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'contradicts',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Riot Platforms, August 2023 Production and Operations Updates',
  'title': 'Riot Platforms, "Riot Announces August 2023 Production and Operations Updates"',
  'version': 'press release dated Sep 6, 2023, fetched 2026-09-30. This is the "Riot Platforms 2023" source that the Duke '
             'report cites.',
  'url': 'https://www.riotplatforms.com/riot-announces-august-2023-production-and-operations-updates/',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['Bitcoin Produced 333 410 374',
            'Average Net Price per Bitcoin Sold $28,617',
            'Riot achieved a new monthly record for Power and Demand Response Credits, totaling $31.7 million in August, '
            'which surpassed the total amount of all Credits received in 2022.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/riot_aug2023.html.txt',
  'agent_note': 'GRADE-DECIDING READING. $31.7 million of credits in an ERCOT scarcity month (mostly resale of contracted '
                "power; $7.4 million DR credits) against 333 bitcoin produced: large against a bitcoin miner's product, but "
                'the source says nothing about AI compute, and bitcoin mining earns far less per MWh than a training '
                "fleet's compute. Does not make G7 fail as written. Family proposal 'contradicts' read as 'bears'."},
 {'id': 'F5:23',
  'family': 'F5',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'PJM 2027/2028 Base Residual Auction Report',
  'title': 'PJM, "2027/2028 Base Residual Auction Report"',
  'version': 'PJM report dated December 17, 2025 (PDF created 2026-01-05), fetched 2026-09-30.',
  'url': 'https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2027-2028/2027-2028-bra-report.pdf',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['Table 1 summarizes the prices ($/MW-day UCAP) from the previous BRA and this BRA. For the 2027/2028 BRA, all '
            'prices cleared at the cap ($333.44). In the 2026/2027 BRA, the RTO cleared at the price cap of $329.17.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/pjm_bra_2027_2028_report.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:24',
  'family': 'F5',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'PUCT 16 TAC 25.509, Scarcity Pricing Mechanism (ERCOT)',
  'title': 'Public Utility Commission of Texas, Substantive Rule §25.509, Scarcity Pricing Mechanism (ERCOT)',
  'version': '16 TAC §25.509, the version "effective 12/20/23 (P 54585)" as served at (PDF created 2023-12-11), fetched '
             '2026-09-30. The rule provides for commission review beginning ...',
  'url': 'https://ftp.puc.texas.gov/public/puct-info/agency/rulesnlaws/subrules/electric/25.509/25.509.pdf',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['(B) The high system-wide offer cap (HCAP) will be $5,000 per MWh for energy offers and $5,000 per MW per hour '
            'for ancillary service offers.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/puct_25.509.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:25',
  'family': 'F5',
  'tag': 'G2',
  'reading': 'close',
  'proposed_reading': 'close',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Jahanshahi et al., Coordinating GPU Data Centers and Power Grid Regulation Service',
  'title': 'Jahanshahi, Rashidi Golrouye, Anderson, Yu & Wong, "Coordinating GPU Data Centers and Power Grid Regulation '
           'Service for Exogenous Carbon Benefits"',
  'version': 'arXiv:2601.22487 v3 (24 Jun 2026)',
  'url': 'https://arxiv.org/abs/2601.22487',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['Since regulation service modulates BE workloads, we capture this lost throughput as opportunity cost. We model '
            'opportunity cost using the GPU hours lost and the hourly cost of a cloud GPU instance.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/arx_2601.22487v3.pdf.txt',
  'agent_note': "Prices a GPU data centre's grid service at GPU-hours lost times the cloud price: G2's form of the cost, "
                'for best-effort work in a regulation service, not a deadline-bound training job.'},
 {'id': 'F5:26',
  'family': 'F5',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'EY, Demand response and data center growth',
  'title': 'EY, "Demand response and data center growth"',
  'version': 'EY insights article, datePublished 2026-04-06, fetched 2026-09-29.',
  'url': 'https://www.ey.com/en_us/insights/power-utilities/demand-response-and-data-center-growth',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['At the same time, data centers remain highly risk-averse to load curtailment due to strict service-level '
            'agreements (SLAs) and uptime requirements, where even brief disruptions can carry financial and reputational '
            'consequences.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/ey_dr_dc.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:27',
  'family': 'F5',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'AWS EC2 on-demand price list JSON (US East, Linux) + AWS P5 page (price list part)',
  'title': 'Amazon Web Services, EC2 on-demand price list (US East, N. Virginia, Linux), public JSON',
  'version': 'AWS price-list file manifest "hawkFilePublicationDate" 2026-09-25T17:45:21Z; fetched 2026-09-29. The file is '
             'served gzip-compressed; the quoted text is the decompressed ...',
  'url': 'https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/US%20East%20(N.%20Virginia',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['"hawkFilePublicationDate":"2026-09-25T17:45:21Z"',
            '"price":"55.0400000000","Location":"US East (N. Virginia)","Instance Family":"GPU '
            'instance","vCPU":"192","Instance Type":"p5.48xlarge"'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/aws_ondemand_useast1_linux.json.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:28',
  'family': 'F5',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'AWS EC2 on-demand price list JSON (US East, Linux) + AWS P5 page (P5 page part)',
  'title': 'Amazon Web Services, "Amazon EC2 P5 Instances" product page',
  'version': 'product page, undated, fetched 2026-09-29.',
  'url': 'https://aws.amazon.com/ec2/instance-types/p5/',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['p5.48xlarge 192 2 TiB 8 H100 640 GB HBM3 3200 Gbps EFA Yes 900 GB/s NVSwitch 8 x 3.84 NVMe SSD 80'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/aws_p5.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:29',
  'family': 'F5',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Bandi & Su, (Early) AI Compute Asset Pricing',
  'title': 'Bandi & Su, "(Early) AI Compute Asset Pricing"',
  'version': 'arXiv:2607.12156 v3 (10 Sep 2026)',
  'url': 'https://arxiv.org/abs/2607.12156',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['AWS: on-demand instance p5.48xlarge (AWS name for an H100 server) Linux in us-east-1 (N. Virginia), priced at '
            '$55.04 per instance-hour, bundling 8 H100 GPUs, 640 GB HBM3 GPU memory, 192 vCPUs, 2,048 GiB system memory, '
            'and 3,200 Gigabit networking. Translating to 6.88 dollars per GPU-hour.',
            'H100 NEO SDH100RT 595 2024-09-01 2026-04-18 2.500',
            'H100 HS 595 2024-09-01 2026-04-18 7.430'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/arx_2607.12156v3.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:30',
  'family': 'F5',
  'tag': 'G3',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Bandi & Su, (Early) AI Compute Asset Pricing',
  'title': 'Bandi & Su, "(Early) AI Compute Asset Pricing"',
  'version': 'arXiv:2607.12156 v3 (10 Sep 2026)',
  'url': 'https://arxiv.org/abs/2607.12156',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['direct no-arbitrage links between futures prices and current spot prices fail due to the non-storable nature '
            'of compute'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/arx_2607.12156v3.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:31',
  'family': 'F5',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NVIDIA DGX H100 datasheet; NVIDIA H100 product page (datasheet part)',
  'title': 'NVIDIA, "NVIDIA DGX H100" datasheet',
  'version': 'datasheet PDF, undated, fetched 2026-09-29.',
  'url': 'https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/nvidia-dgx-h100-datasheet.pdf',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['GPU 8x NVIDIA H100 Tensor Core GPUs GPU memory 640GB total Performance 32 petaFLOPS FP8 NVIDIA® NVSwitch™ 4x '
            'System power usage ~10.2kW max'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/nvidia_dgx_h100_datasheet.pdf.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:32',
  'family': 'F5',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'NVIDIA DGX H100 datasheet; NVIDIA H100 product page (product page part)',
  'title': 'NVIDIA, H100 product page',
  'version': 'product page, undated, fetched 2026-09-29.',
  'url': 'https://www.nvidia.com/en-us/data-center/h100/',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['Max Thermal Design Power (TDP) Up to 700W (configurable) 350-400W (configurable)'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/nvidia_h100.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:33',
  'family': 'F5',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'bears',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'US EIA Electric Power Monthly Table 5.6.A',
  'title': 'US EIA, Electric Power Monthly, Table 5.6.A (average price of electricity by sector and state)',
  'version': 'Electric Power Monthly, data for July 2026, "Release Date: September 24, 2026", fetched 2026-09-29.',
  'url': 'https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['Table 5.6.A. Average Price of Electricity to Ultimate Customers by End-Use Sector, by State, July 2026 and '
            '2025 (Cents per Kilowatthour)',
            'U.S. Total 18.31 17.45 14.53 14.05 9.77 9.33 14.97 14.27 14.99 14.36'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/eia_epm_5_6_a.html.txt',
  'agent_note': "Grading agent's reading of the quote(s) agrees with the family's proposed reading ('bears')."},
 {'id': 'F5:34',
  'family': 'F5',
  'tag': 'G7',
  'reading': 'bears',
  'proposed_reading': 'states',
  'reading_by': "grading agent; for the investigator's review",
  'source': 'Cottier et al., The rising costs of training frontier AI models',
  'title': 'Cottier, Rahman, Fattorini, Maslej, Besiroglu & Owen, "The rising costs of training frontier AI models"',
  'version': 'arXiv:2405.21015 v2 (7 Feb 2025)',
  'url': 'https://arxiv.org/pdf/2405.21015',
  'dossier': 'docs/citations/dr1_f5_2026-09-29.md',
  'quote': ['On the compute side, we find that amortized hardware cost makes up 47–64% of the full model development cost, '
            'while energy comprises only 2–6%.',
            'Note that while energy consumption is a small fraction of total cost, this doesn’t entail that power '
            'requirements are not a challenge in frontier AI development. Regulatory and logistical hurdles to secure power '
            'supplies may cause bottlenecks in the coming years, but we leave that topic to future work.'],
  'raw_file': '/tmp/claude-0/dr1_src/F5/arx_2405.21015.pdf.txt',
  'agent_note': "Energy is 2-6 % of frontier development cost: G7's premise, not the position (the step to 'DR payments are "
                "small' is the grader's). Family proposal 'states' lowered to 'bears'."}]
