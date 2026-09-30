"""ROB1 stage 1, family R5 (Robotics/DECLARATION.md): news and industry feeds. Deployment bottlenecks reported in 2025-26
for humanoids, warehouse and logistics robots, field robots and delivery drones: battery life, reliability, cost,
dependence on remote human help, the cost of training data, and safety incidents.

News (IEEE Spectrum, The Robot Report, Reuters, trade sites) was used as a pointer only. A claim enters only with a primary
source, and every quote is copied from that primary source: company statements and filings (SEC Forms S-4 and 10-K via
EDGAR; an HKEX annual results announcement; a reply filed with the Shanghai Stock Exchange; company pages and press
releases), the International Federation of Robotics (IFR: position-paper infographic, World Robotics 2025 and 2026 press
conference slides), a regulator (FAA: the Part 108 NPRM in the Federal Register, a Part 107 certificate of waiver), an
investigator (NTSB: final and preliminary reports), a US Senator's published investigation, and papers (arXiv current
version).

Every source was fetched on 2026-09-30 through the session proxy. Quotes are copied from the text extracted from the fetched
file: PDFs by pymupdf 1.28.2 (`page.get_text()`, pages joined by newlines); HTML pages by BeautifulSoup 4 (`get_text('\\n')`
after removing script/style/noscript/svg, runs of spaces and blank lines collapsed). Raw files live outside the repository
under /tmp/claude-0/rob_src/ (`raw_file` is relative to that root; the fetched originals are in r5/src/); their sha256 is in
/tmp/claude-0/rob_src/r5/SHA256SUMS.txt and in the dossier docs/citations/rob1_r5_2026-09-30.md. Table rows and slide text
are quoted as the extractor emitted them, cell by cell or line by line in reading order. Where a quote bridges a line break
that the extractor turned into a space inside Chinese text, or a slide bullet glyph (U+F0A7), the quote is split with
"[...]" at that point (r5:13, r5:24, r5:27, r5:31, r5:32). To be checked by Robotics/checks/verify.py; at harvest time a
scratch copy of Open_Bottlenecks/checks/verify.py pointed at this file and this root read "quotes found verbatim: 144 of
144 (claims 74; raw files 32, missing 0)".

Roles (DECLARATION.md stage 1): a = the problem stated; b = a 2025-26 statement that it is open, unsolved or a main challenge;
c = the best reported result on a named benchmark or metric against the target (numbers quoted; the gap is computed in
`agent_note` and in BOTTLENECKS); d = the method families tried and the assumption each makes (about time, clocks,
boundaries, interruptions, memory or tuning). `agent_note` is the agent's reading, not the source's words. Numbers from
different sources are not comparable unless a note says the protocol is shared; where a target and a best result come from
different documents, the note says so. Company statements and filings state the company's own figures, targets and
forward-looking plans; they are not independent measurements, and a filing's projections are management estimates.
Where a company's number contradicts the bottleneck (a claimed target reached), the claim is kept and marked CONTRARY in its
note, for the double check. Currency conversions are not made (no exchange rate was quoted).
"""

R = 'r5/txt/'

CLAIMS = [
    # ---------------- r5-B1: humanoid battery runtime against a working shift / a 24-hour day
    {'id': 'r5:1', 'bottleneck': 'r5-B1', 'role': 'a',
     'source': 'International Federation of Robotics (IFR), Humanoid Robots - Vision and Reality, infographic accompanying the position paper',
     'version': 'PDF created 21 Jul 2025 (no version number); the full position paper requires registration and was not fetched',
     'url': 'https://ifr.org/downloads/press_docs/Humanoids_Position_Infograph_2025.pdf',
     'quote': ['Battery power is a fundamental challenge for humanoid robots.'],
     'raw_file': R + 'ifr_Humanoids_Position_Infograph_2025.txt',
     'agent_note': 'The problem stated by the robot industry federation.'},
    {'id': 'r5:2', 'bottleneck': 'r5-B1', 'role': 'b',
     'source': 'IFR, Humanoid Robots - Vision and Reality, infographic', 'version': 'PDF created 21 Jul 2025',
     'url': 'https://ifr.org/downloads/press_docs/Humanoids_Position_Infograph_2025.pdf',
     'quote': ['So far, a battery cycle does not last a full working day.'],
     'raw_file': R + 'ifr_Humanoids_Position_Infograph_2025.txt',
     'agent_note': '2025 statement that one battery cycle falls short of a working day. The IFR gives no hours for "a full '
                   'working day"; the shift lengths used as targets below come from deployments (r5:7) and a filing (r5:3).'},
    {'id': 'r5:3', 'bottleneck': 'r5-B1', 'role': 'b',
     'source': 'Churchill Capital Corp XI and Agility Robotics, Inc., Form S-4 registration statement (proxy statement/prospectus), '
               'Business of Agility',
     'version': 'Form S-4 filed with the SEC 4 Sep 2026 (accession 0001213900-26-097764; earlier S-4 7 Aug 2026 and S-4/A 21 Aug 2026 '
                'are listed in EDGAR full-text search and were not fetched)',
     'url': 'https://www.sec.gov/Archives/edgar/data/2074973/000121390026097764/ea0297114-04.htm',
     'quote': ['Customer deployments consistently reinforced four priorities for broader commercial adoption: the ability to '
               'operate safely alongside people, maximize utilization across multiple shifts, handle heavier payloads and '
               'perform a broader range of workflows within a facility.'],
     'raw_file': R + 'sec_agility_s4_ea0297114-04.txt',
     'agent_note': '2026 filing: multi-shift utilisation is a customer priority that Digit v5 "was engineered to address" (the '
                   'next sentence of the filing), i.e., in the agent\'s reading, not yet met to customers\' satisfaction by the '
                   'deployed Digit v4. The target implied is operation across shifts in a 24-hour day.'},
    {'id': 'r5:4', 'bottleneck': 'r5-B1', 'role': 'c',
     'source': 'Agility Robotics, press release "Agility Robotics Announces New Innovations for Market-Leading Humanoid Robot Digit"',
     'version': 'published 31 Mar 2025 (page date)',
     'url': 'https://www.agilityrobotics.com/content/agility-robotics-announces-new-innovations-for-market-leading-humanoid-robot-digit',
     'quote': ['Expanded battery capabilities which run more efficiently and last up to four hours',
               'Autonomous docking onto charging station'],
     'raw_file': R + 'agility_digit_innovations.txt',
     'agent_note': 'Best deployed runtime per charge found for an industrial humanoid in commercial service (Digit v4, the model '
                   'with 65,000+ operating hours, r5:16): up to 4 h. Against the 10-hour shift of r5:7 this is 4/10 = 40% of a '
                   'shift per charge (cross-source: the shift is BMW\'s, the runtime Agility\'s).'},
    {'id': 'r5:5', 'bottleneck': 'r5-B1', 'role': 'c',
     'source': 'Agility Robotics, press release "Agility Unveils Digit 5 Humanoid Robot Built for Cooperatively Safe Work at Scale"',
     'version': 'published 15 Sep 2026 (page date; also on PR Newswire the same day)',
     'url': 'https://www.agilityrobotics.com/content/agility-unveils-digit-5-humanoid-robot-built-for-cooperatively-safe-work-at-scale',
     'quote': ['A new 90-minute runtime battery system charges in just 9 minutes, giving Digit 5 a 10:1 run-to-charge ratio (up '
               'from Digit 4’s 2:1), enabling more than 20 hours of productive work in a 24-hour day.',
               'Early access to Digit 5 is expected to begin in the first half of 2027'],
     'raw_file': R + 'agility_digit5.txt',
     'agent_note': 'Day-level metric (productive hours per 24 h). Deployed Digit 4 at 2:1 run-to-charge gives at most 24 x 2/3 = '
                   '16 h of 24 (67%); the announced Digit 5 claims more than 20 h (at least 83%), a company specification for a '
                   'robot not yet shipped (early access H1 2027). Note the trade: runtime per charge falls from up to 4 h '
                   '(r5:4) to 90 min; the day-level target is approached by charging more often, not by a longer cycle.'},
    {'id': 'r5:6', 'bottleneck': 'r5-B1', 'role': 'c',
     'source': '1X Technologies, NEO product page (specifications)',
     'version': 'live page fetched 2026-09-30 (no date shown; copyright 2026)', 'url': 'https://www.1x.tech/neo',
     'quote': ['Run-time 4h Quick charge 6min per hour runtime'],
     'raw_file': R + '1x_neo.txt',
     'agent_note': 'Home humanoid: 4 h per charge, a specification. 6 min of charge per hour of runtime is a 10:1 ratio, like '
                   'Digit 5\'s.'},
    {'id': 'r5:7', 'bottleneck': 'r5-B1', 'role': 'c',
     'source': 'Figure AI, "F.02 Contributed to the Production of 30,000 Cars at BMW"',
     'version': 'published 19 Nov 2025 (page date)', 'url': 'https://www.figure.ai/news/production-at-bmw',
     'quote': ['Ran 10-hour shift Monday-Friday', '1,250+ hours of runtime'],
     'raw_file': R + 'figure_production-at-bmw.txt',
     'agent_note': 'The shift length a deployed humanoid had to cover at a customer (10 h), used as the per-shift target. Figure '
                   'does not say how the 10-hour shift was covered (charging, swaps or several robots); 1,250 h over the '
                   'deployment is consistent with about 25 weeks of 50 h, and gives no runtime per charge.'},
    {'id': 'r5:8', 'bottleneck': 'r5-B1', 'role': 'c',
     'source': 'UBTECH Robotics Corp Ltd, Annual results announcement for the year ended 31 December 2025 (HKEX, stock code 9880)',
     'version': 'HKEX filing dated 31 Mar 2026 (PDF created 31 Mar 2026)',
     'url': 'https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0331/2026033102607.pdf',
     'quote': ['its 3-minute autonomous battery swap and 24-hour continuous operation capabilities',
               'The 1,000-unit-level small-scale mass production and delivery of the Walker S2'],
     'raw_file': R + 'hkex_ubtech_2025_annual_results_2026033102607.txt',
     'agent_note': 'CONTRARY at the day level: the company claims 24-hour continuous operation by autonomous battery swapping, '
                   'on a robot it says it delivered at the 1,000-unit level in 2025. A company claim in a results '
                   'announcement; no measured availability (hours per day actually worked at a customer) is given. It does not '
                   'change the per-cycle reading (IFR, r5:2).'},
    {'id': 'r5:9', 'bottleneck': 'r5-B1', 'role': 'd',
     'source': 'UBTECH, Walker S2 product page', 'version': 'live page fetched 2026-09-30 (no date shown)',
     'url': 'https://www.ubtrobot.com/en/humanoid/products/walker-s2',
     'quote': ['With its dual-battery dynamic balancing and dual-arm coordinated precision battery swapping technologies,Walker S2 '
               'is able to swap battery autonomously within 3 minutes.',
               'By integrating the real-time battery monitoring management with battery swap stations, Walker S2 can autonomously '
               'choose battery swap or charge mode according to the task priorities'],
     'raw_file': R + 'ubtech_walker_s2.txt',
     'agent_note': 'Hot-swap family: the energy boundary is triggered by the battery state and by task priority (state-indexed), '
                   'and it needs swap stations and a spare-battery inventory in the workcell.'},
    {'id': 'r5:10', 'bottleneck': 'r5-B1', 'role': 'd',
     'source': 'Figure AI, "Introducing Figure 03"', 'version': 'published 9 Oct 2025 (page date)',
     'url': 'https://www.figure.ai/news/introducing-figure-03',
     'quote': ['Charging coils in the robot’s feet allow it to simply step onto a wireless stand and charge at 2 kW.',
               'Thanks to inductive charging, Figure 03 is capable of near-continuous operation as long as it can step onto a '
               'charging mat for a certain period of time during the use case.',
               'the robot can offload seamlessly during shift breaks just by returning to the dock.'],
     'raw_file': R + 'figure_introducing-figure-03.txt',
     'agent_note': 'Opportunity-charging family: continuity assumes the task leaves time windows at a dock ("a certain period of '
                   'time during the use case", "shift breaks"), i.e. charging slots set by the workflow\'s clock.'},
    {'id': 'r5:11', 'bottleneck': 'r5-B1', 'role': 'd',
     'source': '1X Technologies, NEO product page', 'version': 'live page fetched 2026-09-30', 'url': 'https://www.1x.tech/neo',
     'quote': ['NEO manages it’s own battery life so you don\'t have to. When NEO needs a charge—it plugs itself in.'],
     'raw_file': R + '1x_neo.txt',
     'agent_note': 'Self-docking on need (state-triggered charging), in a home where idle time is plentiful.'},

    # ---------------- r5-B2: humanoid functional reliability in production (task accuracy, interventions, hardware failures)
    {'id': 'r5:12', 'bottleneck': 'r5-B2', 'role': 'a',
     'source': 'IFR, Humanoid Robots - Vision and Reality, infographic', 'version': 'PDF created 21 Jul 2025',
     'url': 'https://ifr.org/downloads/press_docs/Humanoids_Position_Infograph_2025.pdf',
     'quote': ['Humanoids will not compete with traditional industrial robots in terms of speed, precision, reliability and '
               'repeatability.'],
     'raw_file': R + 'ifr_Humanoids_Position_Infograph_2025.txt',
     'agent_note': 'The problem stated (and framed: the IFR does not expect humanoids to match fixed industrial robots).'},
    {'id': 'r5:13', 'bottleneck': 'r5-B2', 'role': 'b',
     'source': 'IFR, World Robotics 2026 press conference, market presentation (slides)',
     'version': 'slides dated 24 Sep 2026 (PDF created 23 Sep 2026)',
     'url': 'https://ifr.org/downloads/press_docs/Market_Presentation_WR_Press_Conference_2026.pdf',
     'quote': ['Humanoids as Innovation Drivers [...] Technology yet to prove reliability and efficiency',
               'Major challenges: [...] Safety and functional reliability'],
     'raw_file': R + 'ifr_Market_Presentation_WR_Press_Conference_2026.txt',
     'agent_note': '2026 statement by the federation that publishes World Robotics: reliability not yet proven. Each "[...]" '
                   'skips a slide bullet glyph (U+F0A7) that the extractor emitted.'},
    {'id': 'r5:14', 'bottleneck': 'r5-B2', 'role': 'b',
     'source': 'Churchill Capital Corp XI and Agility Robotics, Form S-4, Risk Factors', 'version': 'filed 4 Sep 2026',
     'url': 'https://www.sec.gov/Archives/edgar/data/2074973/000121390026097764/ea0297114-04.htm',
     'quote': ['Returns under the model depend on factors that remain unproven, including the useful life and durability of Digit '
               'units in warehouse, logistics and manufacturing environments',
               'Agility has no experience maintaining or servicing its products at large scale.'],
     'raw_file': R + 'sec_agility_s4_ea0297114-04.txt',
     'agent_note': '2026 filing by the humanoid maker with the longest commercial tenure: durability and service at scale are '
                   'unproven.'},
    {'id': 'r5:15', 'bottleneck': 'r5-B2', 'role': 'b',
     'source': 'Figure AI, "F.02 Contributed to the Production of 30,000 Cars at BMW"', 'version': 'published 19 Nov 2025',
     'url': 'https://www.figure.ai/news/production-at-bmw',
     'quote': ['One learning that informed Figure 03 design was the robot’s forearm, our top hardware failure point at BMW.'],
     'raw_file': R + 'figure_production-at-bmw.txt',
     'agent_note': '2025: a named hardware failure mode from an 11-month deployment; failure counts and rates are not given.'},
    {'id': 'r5:16', 'bottleneck': 'r5-B2', 'role': 'c',
     'source': 'Churchill Capital Corp XI and Agility Robotics, Form S-4, Business of Agility', 'version': 'filed 4 Sep 2026',
     'url': 'https://www.sec.gov/Archives/edgar/data/2074973/000121390026097764/ea0297114-04.htm',
     'quote': ['At Schaeffler, Digit v4 has been deployed across multiple facilities supporting material handling and logistics '
               'workflows, achieving approximately 98% operational accuracy while moving approximately 25,000 totes.',
               'At GXO, Digit has automated tote fulfillment and handling workflows, moving more than 100,000 totes with '
               'approximately 98% operational accuracy.',
               'As of May 2026, Digit v4 had accumulated more than 65,000 hours of commercial operation across nine committed '
               'customer facility deployments'],
     'raw_file': R + 'sec_agility_s4_ea0297114-04.txt',
     'agent_note': 'Best reported task reliability of a humanoid in commercial service found: about 98% "operational accuracy" '
                   '(term not defined in the filing) on tote handling, i.e. about 2% of operations not accurate (about 2,000 of '
                   '100,000 totes at GXO). No interventions per shift, uptime or MTBF is disclosed.'},
    {'id': 'r5:17', 'bottleneck': 'r5-B2', 'role': 'c',
     'source': 'Figure AI, "F.02 Contributed to the Production of 30,000 Cars at BMW" (the three KPIs)',
     'version': 'published 19 Nov 2025', 'url': 'https://www.figure.ai/news/production-at-bmw',
     'quote': ['The requirement was 84 seconds total, 37 seconds load time.',
               'Percentage of cycles where all three sheet-metal parts are correctly loaded. Our target was > 99% success per shift.',
               'Number of times a human must pause or reset the robot. The goal was zero per shift.',
               'Every hour on BMW’s line, every part loaded, and every intervention logged, shaped how we designed, validated, and built.'],
     'raw_file': R + 'figure_production-at-bmw.txt',
     'agent_note': 'The production targets a customer line set for a humanoid: more than 99% success per shift, zero '
                   'interventions per shift, 84 s cycle. Figure reports that interventions were logged but reports no achieved '
                   'value for any of the three KPIs. Gap (CROSS-SOURCE, different task and company): Agility\'s ~98% (r5:16) '
                   'against >99% is a failure share of ~2% against <1%, at least twice the target\'s; interventions per shift '
                   'are disclosed by neither company.'},
    {'id': 'r5:18', 'bottleneck': 'r5-B2', 'role': 'd',
     'source': 'Figure AI, "F.02 Contributed to the Production of 30,000 Cars at BMW"', 'version': 'published 19 Nov 2025',
     'url': 'https://www.figure.ai/news/production-at-bmw',
     'quote': ['We also developed advanced hand-eye coordination algorithms and built field-calibration tools for consistent '
               'cross-robot performance.',
               'For Figure 03, we completely re-architected the wrist electronics to eliminate both the distribution board and '
               'dynamic cabling.'],
     'raw_file': R + 'figure_production-at-bmw.txt',
     'agent_note': 'Families: field calibration (periodic, per robot) and redesign between hardware generations (the fix lands '
                   'at a product boundary, here the retirement of a whole fleet).'},
    {'id': 'r5:19', 'bottleneck': 'r5-B2', 'role': 'd',
     'source': 'Agility Robotics, Digit 5 press release; Form S-4 Risk Factors',
     'version': 'press release 15 Sep 2026; S-4 filed 4 Sep 2026',
     'url': 'https://www.agilityrobotics.com/content/agility-unveils-digit-5-humanoid-robot-built-for-cooperatively-safe-work-at-scale',
     'quote': ['Arc gives operational visibility into fleet KPIs such as uptime, throughput and Mean Time Between Incidents'],
     'raw_file': R + 'agility_digit5.txt',
     'agent_note': 'Fleet monitoring family: reliability tracked as time-based fleet KPIs (uptime, MTBI) by the vendor, which in '
                   'the RaaS model keeps ownership and servicing (r5:14); the values are not published.'},

    # ---------------- r5-B3: unit cost and business case of humanoids for productive work
    {'id': 'r5:20', 'bottleneck': 'r5-B3', 'role': 'a',
     'source': 'IFR, Humanoid Robots - Vision and Reality, infographic', 'version': 'PDF created 21 Jul 2025',
     'url': 'https://ifr.org/downloads/press_docs/Humanoids_Position_Infograph_2025.pdf',
     'quote': ['Humanoids are so far only produced in small numbers. There is not yet a mass production reaching economies of '
               'scale regarding costs.'],
     'raw_file': R + 'ifr_Humanoids_Position_Infograph_2025.txt', 'agent_note': 'The problem stated.'},
    {'id': 'r5:21', 'bottleneck': 'r5-B3', 'role': 'b',
     'source': 'IFR, World Robotics 2026 press conference, market presentation (slide "Focus: Humanoids")',
     'version': 'slides dated 24 Sep 2026',
     'url': 'https://ifr.org/downloads/press_docs/Market_Presentation_WR_Press_Conference_2026.pdf',
     'quote': ['Nearly 7,000 humanoid robots* were sold worldwide in 2025.',
               'Humanoid robots are still on the verge of making the leap from laboratories to pilots – let alone real deployments.',
               'Lack of economic viable business case',
               '* Full-size humanoids, height above 140cm'],
     'raw_file': R + 'ifr_Market_Presentation_WR_Press_Conference_2026.txt',
     'agent_note': '2026: no economically viable business case yet; about 7,000 full-size humanoids sold in 2025. The IFR '
                   'count excludes robots below 140 cm; Unitree alone reports more than 5,500 humanoids shipped in 2025 (r5:27), '
                   'so the two counts differ in scope and are not added or compared.'},
    {'id': 'r5:22', 'bottleneck': 'r5-B3', 'role': 'b',
     'source': 'Tesla, Inc., Annual Report on Form 10-K for the fiscal year ended 31 Dec 2025, Risk Factors',
     'version': 'filed with the SEC 29 Jan 2026 (accession 0001628280-26-003952; a 10-K/A of 30 Apr 2026 was not fetched)',
     'url': 'https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm',
     'quote': ['We have yet to commercialize Bots and cannot predict how demand for Bots will develop, either from commercial or '
               'consumer applications.',
               'the product’s cost-effectiveness, utility and competitive positioning relative to market alternatives'],
     'raw_file': R + 'sec_tesla_10k_fy2025.txt',
     'agent_note': '2026 filing: Optimus not commercialised; cost-effectiveness named as a condition of success.'},
    {'id': 'r5:23', 'bottleneck': 'r5-B3', 'role': 'b',
     'source': 'Churchill Capital Corp XI and Agility Robotics, Form S-4 (Risk Factors; MD&A of Agility)', 'version': 'filed 4 Sep 2026',
     'url': 'https://www.sec.gov/Archives/edgar/data/2074973/000121390026097764/ea0297114-04.htm',
     'quote': ['Agility’s RaaS model has not yet demonstrated profitability at scale.',
               'Gross margins remained negative as the Company continues to operate at an early stage of commercialization and is '
               'continuing to scale manufacturing operations and production efficiencies.'],
     'raw_file': R + 'sec_agility_s4_ea0297114-04.txt', 'agent_note': '2026 filing.'},
    {'id': 'r5:24', 'bottleneck': 'r5-B3', 'role': 'b',
     'source': 'Unitree Robotics (宇树科技股份有限公司) and CITIC Securities, reply to the Shanghai Stock Exchange second-round '
               'inquiry letter on the STAR Market IPO application (预先审阅申请文件的第二轮问询函的回复)',
     'version': 'SSE disclosure dated 20 Mar 2026 (PDF created 20 Mar 2026); the prospectus itself was not fetched',
     'url': 'https://static.sse.com.cn/stock/disclosure/announcement/c/202603/002178_20260320_BLK4.pdf',
     'quote': ['全球范围内，人形机器人行业正处于快速发展初期，在工业场景尚未形成规 [...] 模化应用。公司于2023 年与2024 年先后发布了全尺寸人形机器人H1 与中型'],
     'raw_file': R + 'sse_unitree_prospectus_20260320_BLK4.txt',
     'agent_note': 'Agent\'s translation: "Globally, the humanoid robot industry is at an early stage of rapid development and has '
                   'not yet formed scaled application in industrial scenarios." The largest humanoid shipper (by its own count) '
                   'states in a 2026 exchange filing that industrial use is not yet at scale. The "[...]" bridges a line break '
                   'that the extractor turned into a space inside the word 规模化.'},
    {'id': 'r5:25', 'bottleneck': 'r5-B3', 'role': 'c',
     'source': 'Churchill Capital Corp XI and Agility Robotics, Form S-4, RaaS (Robots-as-a-Service) Model Illustrative Unit Economics',
     'version': 'filed 4 Sep 2026; "Unaudited Prospective Unit Economics Information" (management estimates)',
     'url': 'https://www.sec.gov/Archives/edgar/data/2074973/000121390026097764/ea0297114-04.htm',
     'quote': ['The cost to build a robot will be approximately $150,000 at commercial launch.',
               'At the annual production of 1,000 robots, Agility targets a robot BOM of approximately $75,000.',
               'At the annual production of 10,000 robots, Agility targets a robot BOM of approximately $30,000.'],
     'raw_file': R + 'sec_agility_s4_ea0297114-04.txt',
     'agent_note': 'Bill of materials of an industrial humanoid (Digit v5) at launch against the maker\'s own cost targets: '
                   '$150,000 / $75,000 = 2.0x the 1,000-per-year target; $150,000 / $30,000 = 5.0x the 10,000-per-year target. '
                   'Same document, so comparable. For scale: Digit v4 is in nine facilities (r5:16).'},
    {'id': 'r5:26', 'bottleneck': 'r5-B3', 'role': 'c',
     'source': 'Churchill Capital Corp XI and Agility Robotics, Form S-4, Agility MD&A (years ended 31 Dec 2025 and 2024)',
     'version': 'filed 4 Sep 2026',
     'url': 'https://www.sec.gov/Archives/edgar/data/2074973/000121390026097764/ea0297114-04.htm',
     'quote': ['Net sales — trade increased by $0.4 million, or 136%, to $0.7 million for the year ended December 31, 2025',
               'Net sales to related parties increased by $1.1 million, or 3,229%, to $1.1 million for the year ended December 31, 2025',
               'Cost of goods sold increased by $4.0 million, or 866%, to $4.5 million for the year ended December 31, 2025'],
     'raw_file': R + 'sec_agility_s4_ea0297114-04.txt',
     'agent_note': '2025: cost of goods sold $4.5M against net sales $0.7M + $1.1M = $1.8M, i.e. 2.5x sales (gross margin about '
                   '-150%; agent\'s arithmetic on rounded figures). Target: positive gross margin (the filing\'s own "path toward '
                   'product gross margins in excess of 70%" is a projection).'},
    {'id': 'r5:27', 'bottleneck': 'r5-B3', 'role': 'c',
     'source': 'Unitree Robotics and CITIC Securities, reply to the SSE second-round inquiry letter (humanoid margin, unit price, '
               'revenue by application)',
     'version': 'SSE disclosure dated 20 Mar 2026',
     'url': 'https://static.sse.com.cn/stock/disclosure/announcement/c/202603/002178_20260320_BLK4.pdf',
     'quote': ['公司2025 年人形机器人出货量超过 [...] 5,500 台，保持行业第一',
               '2024 年与2025 年1-9 月，公司人形机器人的毛利率分别为68.44%、62.91%， [...] 单位价格分别为26.07 万元/台、16.76 万元/台',
               '科研教育 43,806.74 73.60%',
               '行业应用 5,360.36 9.01%',
               '人形机器人用于智能制造、智能巡 [...] 检、物流配送等明确场景的销售收入合计为1,570.20 万元，占行业应用的收入'],
     'raw_file': R + 'sse_unitree_prospectus_20260320_BLK4.txt',
     'agent_note': 'CONTRARY on price, not on productive use. Unitree sold humanoids at RMB 167,600 per unit (Jan-Sep 2025) with '
                   '62.91% gross margin: low cost and profitable. But by revenue (Jan-Sep 2025, RMB 10,000s) 73.60% went to '
                   'research and education and 9.01% to industry applications, of which only RMB 15.702M was for explicit '
                   'productive scenes (manufacturing, inspection, logistics): 1,570.20 / 59,518.79 = 2.64% of humanoid revenue '
                   '(agent\'s arithmetic; 59,518.79 is the table total). So the cheap humanoid is not yet the productive one. The '
                   'shipment figure (more than 5,500 in 2025) is the exchange\'s question quoting the application; it counts all '
                   'sizes.'},
    {'id': 'r5:28', 'bottleneck': 'r5-B3', 'role': 'c',
     'source': 'UBTECH Robotics, Annual results announcement 2025 (HKEX)', 'version': 'dated 31 Mar 2026',
     'url': 'https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0331/2026033102607.pdf',
     'quote': ['In 2025, full-size embodied intelligent humanoid robot products and services for all scenarios achieved revenue of '
               'approximately RMB820 million, representing a year-on-year increase of approximately 2,203.7%; and achieved sales '
               'volume of 1,079 units',
               'as high-margin full-size embodied intelligent humanoid robot products and services became our largest source of '
               'revenue.'],
     'raw_file': R + 'hkex_ubtech_2025_annual_results_2026033102607.txt',
     'agent_note': 'Industrial full-size humanoids: RMB 820M / 1,079 units = about RMB 760,000 per unit including services '
                   '(agent\'s arithmetic), sold at a high margin (segment margin not given). Price to the buyer, not cost; about '
                   '4.5x Unitree\'s unit price (r5:27).'},
    {'id': 'r5:29', 'bottleneck': 'r5-B3', 'role': 'd',
     'source': 'Churchill Capital Corp XI and Agility Robotics, Form S-4 (RaaS assumptions; Business of Agility)',
     'version': 'filed 4 Sep 2026',
     'url': 'https://www.sec.gov/Archives/edgar/data/2074973/000121390026097764/ea0297114-04.htm',
     'quote': ['A deployed robot will generate a recurring monthly fee of $8,500 that includes access to software and maintenance '
               'services.',
               'subscription pricing is generally structured at a discount to a customer’s fully burdened labor cost',
               'Based on our current planning assumptions, Digit v5 is expected to achieve customer breakeven in approximately 1.1 years.'],
     'raw_file': R + 'sec_agility_s4_ea0297114-04.txt',
     'agent_note': 'Robots-as-a-Service family: price set against the hourly labour it replaces, on a calendar subscription '
                   '(monthly fee, 5-year assumed life); the vendor carries durability risk (r5:14). Payback is a planning '
                   'assumption, not a measurement.'},
    {'id': 'r5:30', 'bottleneck': 'r5-B3', 'role': 'd',
     'source': 'Figure AI, "Introducing Figure 03"', 'version': 'published 9 Oct 2025',
     'url': 'https://www.figure.ai/news/introducing-figure-03',
     'quote': ['each Figure 03 unit now costs dramatically less to build, with the economics improving as volumes grow.',
               'BotQ’s first-generation manufacturing line will initially be capable of producing up to 12,000 humanoid robots per '
               'year, with the goal of producing a total of 100,000 robots over the next four years.'],
     'raw_file': R + 'figure_introducing-figure-03.txt',
     'agent_note': 'Volume cost-down family (design for tooling, in-house line): assumes demand for the volume. No unit cost '
                   'stated. The 100,000-in-four-years goal is about 3.6x per year the ~7,000 full-size humanoids the IFR counts '
                   'as sold worldwide in 2025 (r5:21; cross-source, agent\'s arithmetic 25,000/7,000).'},
    {'id': 'r5:31', 'bottleneck': 'r5-B3', 'role': 'd',
     'source': 'Unitree Robotics and CITIC Securities, reply to the SSE second-round inquiry letter', 'version': 'dated 20 Mar 2026',
     'url': 'https://static.sse.com.cn/stock/disclosure/announcement/c/202603/002178_20260320_BLK4.pdf',
     'quote': ['中型人形机器人的推出并非以更高的销售毛利率为目标， [...] 而是以更具竞争力的产品定位、性价比优势带动人形机器人销售规模的大幅提升'],
     'raw_file': R + 'sse_unitree_prospectus_20260320_BLK4.txt',
     'agent_note': 'Agent\'s translation: "The launch of the mid-size humanoid did not aim at a higher gross margin, but at driving '
                   'a large increase in humanoid sales volume through more competitive positioning and value for money." Low-price '
                   'volume family; the buyers are mostly research and education (r5:27).'},
    {'id': 'r5:32', 'bottleneck': 'r5-B3', 'role': 'd',
     'source': 'IFR, World Robotics 2025 - Service Robots, press conference presentation (slides)',
     'version': 'slides dated September 2025 (PDF created 29 Sep 2025)',
     'url': 'https://ifr.org/downloads/press_docs/Press_Conference_2025_SR.pdf',
     'quote': ['Major challenges: [...] High upfront investment costs', 'RaaS business models lower adoption barriers considerably',
               'There is no massive use today but serial production in preparation'],
     'raw_file': R + 'ifr_Press_Conference_2025_SR.txt',
     'agent_note': 'For transport and logistics service robots (not humanoids), the IFR names upfront cost as a major challenge '
                   'and RaaS as the family that lowers it; for humanoids, "no massive use today". The "[...]" skips a slide bullet '
                   'glyph (U+F0A7).'},

    # ---------------- r5-B4: warehouse robotic stow/pick: item coverage, rate and defects against the production target
    {'id': 'r5:33', 'bottleneck': 'r5-B4', 'role': 'a',
     'source': 'Hudson, Hooks, Warrier, ... Parness (Amazon Robotics), Stow: Robotic Packing of Items into Fabric Pods',
     'version': 'arXiv v1, 7 May 2025 (only version)', 'url': 'https://arxiv.org/abs/2505.04572v1',
     'quote': ['The wide diversity of items and strict business requirements for high producing rates and low defect generation '
               'have prohibited warehouse robotics from performing this task.',
               'The task is currently performed manually more than 14 billion times per year.'],
     'raw_file': R + '2505.04572v1.txt', 'agent_note': 'The problem stated by the operator itself.'},
    {'id': 'r5:34', 'bottleneck': 'r5-B4', 'role': 'b',
     'source': 'Hudson et al. (Amazon Robotics), Stow (Sec. IX)', 'version': 'arXiv v1, 7 May 2025',
     'url': 'https://arxiv.org/abs/2505.04572v1',
     'quote': ['Unproductive stows are thus expected even in more mature versions of this robotic system, but will aim for much '
               'lower rates (i.e. 3% vs. 9%).',
               'This behavior needs to be changed as the system scales'],
     'raw_file': R + '2505.04572v1.txt', 'agent_note': '2025: the deployed system is below its own target on unproductive cycles.'},
    {'id': 'r5:35', 'bottleneck': 'r5-B4', 'role': 'b',
     'source': 'Amazon, "Introducing Vulcan: Amazon’s first robot with a sense of touch" (aboutamazon.com)',
     'version': 'published 7 May 2025, modified 4 Jun 2026 (page metadata)',
     'url': 'https://www.aboutamazon.com/news/operations/amazon-vulcan-robot-pick-stow-touch',
     'quote': ['It also has the smarts to identify when it can’t move a specific item, and can ask a human partner to tag in'],
     'raw_file': R + 'amazon_vulcan.txt',
     'agent_note': '2025-26: items the robot cannot handle go to a human; the robot does not cover the item range alone.'},
    {'id': 'r5:36', 'bottleneck': 'r5-B4', 'role': 'c',
     'source': 'Hudson et al. (Amazon Robotics), Stow (Sec. I design targets; Sec. IX-B stow rate; Table II outcomes over 100,000 attempts)',
     'version': 'arXiv v1, 7 May 2025', 'url': 'https://arxiv.org/abs/2505.04572v1',
     'quote': ['The robotic solution described here is designed to stow 80% of items in the warehouse at a rate of 300 units per hour.',
               'it must be capable of operating more than 20 hr per day and 7 days per week.',
               'Over the month of March 2025, humans stowed at an average rate of 243 units per hour (UPH) while the robotic '
               'systems stowed at 224 UPH.',
               'All Successful 85,859 85.86% – Unproductive 9,311 9.31% – Defect 4,830 4.83%'],
     'raw_file': R + '2505.04572v1.txt',
     'agent_note': 'Same paper, same deployment. Rate: 224 UPH against the human 243 UPH on the same floor (92.2%) and against '
                   'the 300 UPH design target (74.7%). Unproductive cycles 9.31% against the 3% aim (3.1x). Success 85.86%, '
                   'defects 4.83%. Hours per day actually achieved and interventions per day are not reported, so the 20 h / 7 d '
                   'requirement is not scored. (The 7% learned-model gain was measured outside the 100,000 attempts.)'},
    {'id': 'r5:37', 'bottleneck': 'r5-B4', 'role': 'c',
     'source': 'Amazon, "Introducing Vulcan" (aboutamazon.com)', 'version': 'published 7 May 2025, modified 4 Jun 2026',
     'url': 'https://www.aboutamazon.com/news/operations/amazon-vulcan-robot-pick-stow-touch',
     'quote': ['With the ability to pick and stow approximately 75% of all various types of items we store at our fulfillment '
               'centers, and at speeds comparable to that our front-line employees'],
     'raw_file': R + 'amazon_vulcan.txt',
     'agent_note': 'Item coverage ~75% of item types against the 80% design target of the stow system (r5:36): 5 points short '
                   '(company page vs company paper; "item types" and "items" may not be the same denominator).'},
    {'id': 'r5:38', 'bottleneck': 'r5-B4', 'role': 'c',
     'source': 'Ocado Group plc, Full Year Results 2025 (52 weeks to 30 Nov 2025), results page',
     'version': 'live page fetched 2026-09-30 (no date shown; it cites CFC closures of Jan and Feb 2026)',
     'url': 'https://www.ocadogroup.com/investors/results-and-presentations/ocado-group-full-year-results-2025',
     'quote': ['OGRP rolled out in 10 CFCs with most advanced CFC now picking c.50% volumes robotically'],
     'raw_file': R + 'ocado_fy2025_results.txt',
     'agent_note': 'Supporting number only (grocery each-picking, a different task): the best site picks about half its volume '
                   'robotically; Ocado states no target, so no gap is computed from it.'},
    {'id': 'r5:39', 'bottleneck': 'r5-B4', 'role': 'd',
     'source': 'Hudson et al. (Amazon Robotics), Stow (Fig. 2; Sec. III)', 'version': 'arXiv v1, 7 May 2025',
     'url': 'https://arxiv.org/abs/2505.04572v1',
     'quote': ['Fig. 2: In the Robotic Stow Process, a human checks inbound items for quality and feeds three robotic workcells.',
               'Finally, the system must run autonomously without interruptions that require human intervention (e.g. to clear a '
               'jam, restart a subsystem, or jog a robot)'],
     'raw_file': R + '2505.04572v1.txt',
     'agent_note': 'Human-in-the-loop decomposition: a human inducts and screens items (one human per three cells); robots take '
                   'the rest; interruptions are the named failure mode.'},
    {'id': 'r5:40', 'bottleneck': 'r5-B4', 'role': 'd',
     'source': 'Hudson et al. (Amazon Robotics), Stow (Sec. VIII-B learned risk; Sec. IX-A)', 'version': 'arXiv v1, 7 May 2025',
     'url': 'https://arxiv.org/abs/2505.04572v1',
     'quote': ['up to 5% of the time, the system relaxes margins and/or randomly chooses a behavior',
               'but it does come with a cost of needing to continually recollect training data as development evolves and behaviors change.',
               'Exploring, which executes riskier stows, will continue to be critical for continual learning and maintaining robust models.'],
     'raw_file': R + '2505.04572v1.txt',
     'agent_note': 'Learned-risk family: a fixed exploration rate (up to 5%, epsilon-greedy) and retraining when behaviours '
                   'change (a development boundary triggers data recollection); continual learning named as the maintenance mode.'},
    {'id': 'r5:41', 'bottleneck': 'r5-B4', 'role': 'd',
     'source': 'Amazon, "Introducing Vulcan" (aboutamazon.com)', 'version': 'published 7 May 2025, modified 4 Jun 2026',
     'url': 'https://www.aboutamazon.com/news/operations/amazon-vulcan-robot-pick-stow-touch',
     'quote': ['we couldn’t just teach Vulcan with computer simulations, but trained its AI on physical data that incorporates touch '
               'and force feedback.'],
     'raw_file': R + 'amazon_vulcan.txt', 'agent_note': 'Real-robot data family (simulation judged insufficient).'},

    # ---------------- r5-B5: field harvesting robots: throughput and success against human pickers
    {'id': 'r5:42', 'bottleneck': 'r5-B5', 'role': 'a',
     'source': 'Zhu, Lammers, Arunachalam, Zhang, Lu & Li (Michigan State University; USDA-ARS), A Modular Dual-Arm Apple '
               'Harvesting Robot with Enhanced Field Performance',
     'version': 'arXiv v1, 12 Jun 2026 (only version)', 'url': 'https://arxiv.org/abs/2606.14089v1',
     'quote': ['Robotic apple harvesting offers a promising solution to growing labor shortages in commercial orchards, but low '
               'throughput and poor performance in challenging orchard environments hinder its commercial adoption.'],
     'raw_file': R + '2606.14089v1.txt', 'agent_note': 'The problem stated.'},
    {'id': 'r5:43', 'bottleneck': 'r5-B5', 'role': 'b',
     'source': 'Xia, Cai, Espinoza, Li, Rubio Ames, Zhang & Chen, CLASP: A Cluster-Level Autonomous Selective Picking Robot with a '
               'Soft Rolling-Band Gripper for Fresh-Market Blueberry Harvesting',
     'version': 'arXiv v1, 16 Sep 2026 (only version)', 'url': 'https://arxiv.org/abs/2609.18051v1',
     'quote': ['Yet harvesting for the fresh market remains almost entirely manual'],
     'raw_file': R + '2609.18051v1.txt', 'agent_note': '2026 statement.'},
    {'id': 'r5:44', 'bottleneck': 'r5-B5', 'role': 'b',
     'source': 'Zhu et al., Advancement and Field Evaluation of a Dual-arm Apple Harvesting Robot',
     'version': 'arXiv v1, 6 Jun 2025 (only version)', 'url': 'https://arxiv.org/abs/2506.05714v1',
     'quote': ['the evaluations of the robots in commercial orchards remain limited, and current systems still fall short of the '
               'speed and accuracy required for practical deployment.'],
     'raw_file': R + '2506.05714v1.txt', 'agent_note': '2025 statement.'},
    {'id': 'r5:45', 'bottleneck': 'r5-B5', 'role': 'c',
     'source': 'Xia et al., CLASP (Sec. VII field results)', 'version': 'arXiv v1, 16 Sep 2026', 'url': 'https://arxiv.org/abs/2609.18051v1',
     'quote': ['The gripper achieved 32 berries per minute against 55 for a human picker.',
               'the gripper itself achieves 58 % of the manual harvesting rate.',
               'Of 25 harvesting attempts, 23 succeeded and 2 failed, giving a success rate of 92 %.',
               'should not be interpreted as a comprehensive reliability estimate.',
               '166.22 g mm−1 against 195.59 g mm−1 for the hand-picked reference, corresponding to a 15 % reduction.'],
     'raw_file': R + '2609.18051v1.txt',
     'agent_note': 'Same paper, same field, human baseline measured: 32 vs 55 berries/min = 58% of the human rate, and that with '
                   'the gripper MANUALLY aligned (the autonomous pipeline is slower; its rate is not reported). Autonomous success '
                   '23/25 = 92% (n = 25, flagged by the authors). Fruit firmness 15% below hand-picked. Gap: 42% of the human '
                   'rate at best.'},
    {'id': 'r5:46', 'bottleneck': 'r5-B5', 'role': 'c',
     'source': 'Zhu et al., A Modular Dual-Arm Apple Harvesting Robot (abstract; 2025 season field trials)',
     'version': 'arXiv v1, 12 Jun 2026', 'url': 'https://arxiv.org/abs/2606.14089v1',
     'quote': ['Across the 1,738 arm cycles collected in these field trials, the system achieved an 80.0% per-attempt success rate '
               'and a mean per-arm cycle time of 7.53 s.'],
     'raw_file': R + '2606.14089v1.txt',
     'agent_note': 'Supporting number only: the paper reports no human baseline, so no gap is computed from it. 20% of attempts '
                   'fail.'},
    {'id': 'r5:47', 'bottleneck': 'r5-B5', 'role': 'd',
     'source': 'Zhu et al., A Modular Dual-Arm Apple Harvesting Robot (Sec. 2; Sec. 5 limitations)', 'version': 'arXiv v1, 12 Jun 2026',
     'url': 'https://arxiv.org/abs/2606.14089v1',
     'quote': ['following a stop-and-go harvesting pattern under human operator control.',
               'In the current deployment, a human operator drives the tractor and performs platform adjustments at each '
               'harvesting stop.',
               'Replacing the tractor-trailer with an autonomous ground vehicle would enable continuous low-speed traversal of '
               'orchard rows, with the platform repositioning dynamically according to fruit distribution rather than halting '
               'at fixed intervals.'],
     'raw_file': R + '2606.14089v1.txt',
     'agent_note': 'Stop-and-go family: the work is cut into stops at fixed intervals set by a human operator; the authors\' '
                   'proposed next step indexes repositioning by the fruit distribution instead (state-indexed).'},
    {'id': 'r5:48', 'bottleneck': 'r5-B5', 'role': 'd',
     'source': 'Xia et al., CLASP (Sec. VII-1 field test setup)', 'version': 'arXiv v1, 16 Sep 2026',
     'url': 'https://arxiv.org/abs/2609.18051v1',
     'quote': ['The robot was mounted on a mobile platform (Rover Robotics MAX) for teleoperated in-field transport.',
               'Autonomous harvesting tests were then conducted at several fixed locations',
               'Only 40.3 % (29 of 72 analyzed clusters) of the clusters surveyed lay within the field of view of the global camera'],
     'raw_file': R + '2609.18051v1.txt',
     'agent_note': 'Teleoperated transport between fixed test locations; autonomy only at the stop; perception from a fixed '
                   'viewpoint sees 40.3% of clusters.'},

    # ---------------- r5-B6 (not shown open): remote human help per robot (teleoperation dependence), no numeric target
    {'id': 'r5:49', 'bottleneck': 'r5-B6', 'role': 'a',
     'source': 'Churchill Capital Corp XI and Agility Robotics, Form S-4, Business of Agility (competition)', 'version': 'filed 4 Sep 2026',
     'url': 'https://www.sec.gov/Archives/edgar/data/2074973/000121390026097764/ea0297114-04.htm',
     'quote': ['Many companies in the humanoid robotics industry have not yet achieved autonomous commercial deployment, relying '
               'instead on teleoperation, demonstrations or prototype systems.'],
     'raw_file': R + 'sec_agility_s4_ea0297114-04.txt',
     'agent_note': 'The problem stated for humanoids, by a competitor in a securities filing (self-interested).'},
    {'id': 'r5:50', 'bottleneck': 'r5-B6', 'role': 'a',
     'source': 'FAA and TSA, Normalizing Unmanned Aircraft Systems Beyond Visual Line of Sight Operations, NPRM '
               '(Federal Register Vol. 90 No. 150), Sec. VI.M Operation of multiple UA',
     'version': 'published 7 Aug 2025 (proposed rule; no final rule listed in docket FAA-2025-1908 on 2026-09-30 per family R3)',
     'url': 'https://www.govinfo.gov/content/pkg/FR-2025-08-07/pdf/2025-14992.pdf',
     'quote': ['The technological ability for one individual person to manipulate multiple aircraft simultaneously is unique to '
               'the UAS environment.',
               'FAA recognizes that broader applicability of controlling or monitoring multiple UA per person, or groups of '
               'persons, is an important consideration in scaling UAS operations'],
     'raw_file': R + 'FR-2025-14992.txt', 'agent_note': 'The problem stated for delivery and other BVLOS drones.'},
    {'id': 'r5:51', 'bottleneck': 'r5-B6', 'role': 'b',
     'source': 'FAA and TSA, Part 108 NPRM, Sec. VI.M (proposed § 108.210)', 'version': 'published 7 Aug 2025',
     'url': 'https://www.govinfo.gov/content/pkg/FR-2025-08-07/pdf/2025-14992.pdf',
     'quote': ['only be able to conduct operations at a UA to flight coordinator ratio of 1:1, except in accordance with a method '
               'acceptable to the Administrator.',
               'FAA recognizes that there is significant interest in the industry in being able to operate 1:many at scale to '
               'facilitate further UAS integration. However, at this time there is limited industry standardization'],
     'raw_file': R + 'FR-2025-14992.txt',
     'agent_note': '2025 regulator statement: 1:many at scale is wanted but not standardised; the proposed default is 1:1. No '
                   'numeric target ratio is set (the NPRM leaves it to consensus standards and case-by-case review).'},
    {'id': 'r5:52', 'bottleneck': 'r5-B6', 'role': 'b',
     'source': 'Serve Robotics Inc., Annual Report on Form 10-K for the fiscal year ended 31 Dec 2025, Business',
     'version': 'signed 12 Mar 2026 (accession 0001832483-26-000010)',
     'url': 'https://www.sec.gov/Archives/edgar/data/1832483/000183248326000010/patr-20251231.htm',
     'quote': ['While all automated delivery robots still require a certain amount of human involvement (e.g., loading and '
               'unloading, maintenance, remote supervision)',
               'Creating fully autonomous machines that are safe and reliable without any human intervention requires '
               'substantially more time and capital investment than creating machines that are mostly automated but can rely on '
               'occasional human support'],
     'raw_file': R + 'sec_serve_10k_fy2025.txt', 'agent_note': '2026 filing by a sidewalk-delivery-robot operator.'},
    {'id': 'r5:53', 'bottleneck': 'r5-B6', 'role': 'b',
     'source': 'Office of Senator Edward J. Markey, press release on the report "Remote Backseat Operators" (remote assistance '
               'operators of autonomous vehicles)',
     'version': 'published 31 Mar 2026 (page date); the report PDF itself was not fetched',
     'url': 'https://www.markey.senate.gov/news/press-releases/markey-investigation-into-autonomous-vehicle-companies-use-of-remote-assistance-operators-reveals-serious-safety-gaps-lack-of-transparency',
     'quote': ['Every AV company refused to disclose how frequently their RAOs intervene to help their self-driving cars.'],
     'raw_file': R + 'markey_ra_investigation.txt',
     'agent_note': 'COMPARATOR outside the family\'s robot classes (road vehicles, seven companies): the intervention frequency, '
                   'the natural metric for this bottleneck, is withheld by every company asked in 2026.'},
    {'id': 'r5:54', 'bottleneck': 'r5-B6', 'role': 'b',
     'source': '1X Technologies, "1X NEO Home Robot" launch announcement; NEO product page',
     'version': 'announcement dated 28 Oct 2025; product page fetched 2026-09-30',
     'url': 'https://www.1x.tech/discover/neo-home-robot',
     'quote': ['For any chore that NEO doesn\'t yet know, owners can schedule a 1X Expert to guide it through unknown tasks'],
     'raw_file': R + '1x_neo_home_robot.txt',
     'agent_note': '2025: a consumer humanoid shipped with scheduled remote human operation for tasks it cannot do; the share of '
                   'tasks done this way is not published.'},
    {'id': 'r5:55', 'bottleneck': 'r5-B6', 'role': 'd',
     'source': '1X Technologies, NEO product page', 'version': 'live page fetched 2026-09-30', 'url': 'https://www.1x.tech/neo',
     'quote': ['For complex tasks NEO doesn’t know, an Expert from 1X can remotely supervise its actions at scheduled times to help '
               'it learn new abilities and get the job done.'],
     'raw_file': R + '1x_neo.txt',
     'agent_note': 'Scheduled teleoperation that doubles as data collection: the human session is booked on the clock (a '
                   'calendar slot), not triggered by the robot\'s state.'},
    {'id': 'r5:56', 'bottleneck': 'r5-B6', 'role': 'd',
     'source': 'FAA, Certificate of Waiver 107W-2024-04627 issued to Zipline (Delivery OPS), special provisions',
     'version': 'signed 16 Jan 2025; effective 13 Jan 2025 to 30 Sep 2028',
     'url': 'https://www.faa.gov/media/90041',
     'quote': ['The remote PIC may conduct operations of up to 6 sUA, equipped with redundant flight control and transmission '
               'systems',
               'A remote PIC may not be responsible for more than one Operational Volume at a time'],
     'raw_file': R + 'faa_media_90041.txt',
     'agent_note': 'Waiver family: the ratio is raised case by case (here 1:6, against the 1:1 default of r5:51), with redundancy '
                   'and one operational volume per pilot. A number, but not against a stated target, so not B-c.'},
    {'id': 'r5:57', 'bottleneck': 'r5-B6', 'role': 'd',
     'source': 'Waymo LLC, response to Senator Markey on remote assistance', 'version': 'letter dated 17 Feb 2026',
     'url': 'https://assets.ctfassets.net/7ijaobx36mtm/7E5uOzS5F7Z1yuFoz27BIc/680a27f89a3aae48977db655a5f45005/Sen._Markey_RA_Letter_Waymo__Response.pdf',
     'quote': ['At any given time, there are approximately 70 Remote Assistance agents on duty worldwide.',
               'We operate a fleet of over 3,000 vehicles across six major U.S. cities.',
               'reaches out to Remote Assistance when the vehicle encounters an ambiguous situation'],
     'raw_file': R + 'waymo_markey_RA_response_2026-02-17.txt',
     'agent_note': 'COMPARATOR (road vehicles): event-driven remote assistance, requested by the vehicle, not continuous '
                   'monitoring; about 70 agents on duty for over 3,000 vehicles, about 1 per 43 vehicles (agent\'s arithmetic; '
                   'fleet in service at one time not stated). The request frequency is withheld (r5:53).'},
    {'id': 'r5:58', 'bottleneck': 'r5-B6', 'role': 'd',
     'source': 'Starship Technologies, FAQ page', 'version': 'published 23 May 2024, modified 4 Sep 2025 (page metadata)',
     'url': 'https://www.starship.xyz/faq/',
     'quote': ['Currently, Starship operates at over 99% autonomy, whilst some robots are now making multiple deliveries in a row, '
               '100% autonomously.',
               'For safety reasons, we also make sure to have human remote assistants on standby, in case they’re called upon to support.'],
     'raw_file': R + 'starship_faq.txt',
     'agent_note': 'CONTRARY (vendor claim) for sidewalk robots: "over 99% autonomy", metric undefined (share of time, distance or '
                   'deliveries is not said); the family is remote assistants on standby, called on demand.'},
    {'id': 'r5:59', 'bottleneck': 'r5-B6', 'role': 'd',
     'source': 'Serve Robotics, Form 10-K FY2025 (Business; Risk Factors; Key Metrics)', 'version': 'signed 12 Mar 2026',
     'url': 'https://www.sec.gov/Archives/edgar/data/1832483/000183248326000010/patr-20251231.htm',
     'quote': ['The fleet is monitored through mobile connectivity and video streaming by remote human supervisors who can assist '
               'robots when necessary, such as at intersection crossings or when robots are unable to navigate certain conditions.',
               'certain of our remote piloting services are currently provided by third-party vendors, including service centers '
               'outside of the United States.',
               'We closely monitor and strive to efficiently increase our daily active robots as we improve our autonomy and '
               'resultant human-to-robot ratios',
               'Daily Active Robots 547 57 273 52',
               'with approximately 2,000 sidewalk delivery robots deployed across multiple geographic markets'],
     'raw_file': R + 'sec_serve_10k_fy2025.txt',
     'agent_note': 'Continuous remote monitoring family with situation-triggered assists (intersections). Daily active robots '
                   '547 in Q4 2025 (273 for 2025; columns Q4 2025, Q4 2024, FY 2025, FY 2024) against about 2,000 robots '
                   'deployed: 27% (agent\'s '
                   'arithmetic); the filing ties the growth of this number to the human-to-robot ratio, which it does not state.'},

    {'id': 'r5:74', 'bottleneck': 'r5-B6', 'role': 'd',
     'source': 'Wing (Alphabet), "How Wing\'s Drone Delivery Technology Works" (wing.com/technology)',
     'version': 'live page fetched 2026-09-30 (no date shown)', 'url': 'https://wing.com/technology',
     'quote': ['Pilots oversee multiple flights from a central location, monitoring weather and air traffic to ensure safety. '
               'Individual flights don’t require human control. Instead, pilots oversee the whole system.',
               'With approvals for one pilot to oversee several drones at any point, our system is designed to scale.'],
     'raw_file': R + 'wing_technology.txt',
     'agent_note': 'Supervisory (1:many) family for delivery drones: the pilot monitors the system, not each flight; the ratio '
                   '("several") is not stated. Id out of sequence: added after r5:73.'},

    # ---------------- r5-B7 (not shown open): delivery-drone collisions with obstacles and other aircraft (incident record)
    {'id': 'r5:60', 'bottleneck': 'r5-B7', 'role': 'a',
     'source': 'NTSB, Aviation Investigation Preliminary Report WPR26LA001 (Amazon MK30 N579PA, Tolleson, AZ, 1 Oct 2025)',
     'version': 'preliminary report ("subject to change"), current version fetched 2026-09-30; no final report yet',
     'url': 'https://data.ntsb.gov/carol-repgen/api/Aviation/ReportMain/GenerateNewestReport/201774/pdf',
     'quote': ['crane arrived at the jobsite at 0530 and was erected between 0730 and 0800. At 0949, the crane operator felt '
               'something impact the erected crane that turned out to be a UAS.',
               'operator terminated operations and was evaluating the UAS strike when a second UAS impacted the stationary crane.',
               'The planned route of flight was at an altitude of about 200 ft agl.'],
     'raw_file': R + 'ntsb_newest_201774.txt',
     'agent_note': 'Two commercial Part 135 delivery drones struck the same temporary obstacle 9 minutes apart (0949 here, 0958 '
                   'in r5:73), about 2 h after it was erected. An incident, not a rate.'},
    {'id': 'r5:61', 'bottleneck': 'r5-B7', 'role': 'd',
     'source': 'NTSB, Preliminary Report WPR26LA001', 'version': 'preliminary, fetched 2026-09-30',
     'url': 'https://data.ntsb.gov/carol-repgen/api/Aviation/ReportMain/GenerateNewestReport/201774/pdf',
     'quote': ['Ground Surveillance Crews (GSC) to conduct rooftop scans of the surrounding area twice per day, once in the morning '
               'and again about midday. On the day of the incident, GSC’s conducted their scans about 0658 and did not identify '
               'any obstructions that would have interrupted normal operations.'],
     'raw_file': R + 'ntsb_newest_201774.txt',
     'agent_note': 'Obstacle survey on a fixed clock (twice a day): the crane appeared between the 0658 scan and the midday one. '
                   'The assumption is that the obstacle map changes slowly relative to the survey interval.'},
    {'id': 'r5:62', 'bottleneck': 'r5-B7', 'role': 'a',
     'source': 'NTSB, Aviation Investigation Final Report WPR25LA103 (Amazon MK30 N265PA, Pendleton, OR, 21 Feb 2025, flight test)',
     'version': 'final report, original publish date 9 May 2025', 'url': 'https://data.ntsb.gov/carol-repgen/api/Aviation/ReportMain/GenerateNewestReport/199746/pdf',
     'quote': ['The unmanned aircraft system’s failure to maintain clearance from an obstacle, which resulted in a loss of control and '
               'impact with terrain.'],
     'raw_file': R + 'ntsb_newest_199746.txt', 'agent_note': 'Probable cause of a test-flight accident with a placed obstacle.'},
    {'id': 'r5:63', 'bottleneck': 'r5-B7', 'role': 'a',
     'source': 'NTSB, Aviation Investigation Final Report WPR24LA302 (two Amazon MK30, Pendleton, OR, 6 Sep 2024, flight test)',
     'version': 'final report, original publish date 13 Mar 2025', 'url': 'https://data.ntsb.gov/carol-repgen/api/Aviation/ReportMain/GenerateNewestReport/195091/pdf',
     'quote': ['The operator’s failure to maintain separation between two drones during dual simulated engine out recoveries, which '
               'resulted in a midair collision.',
               'The same fault was applied to N282PA as it was departing, which then diverted the UAS to the same alternate landing '
               'pad and into the flight path of N213PA, resulting in a mid-air collision.'],
     'raw_file': R + 'ntsb_newest_195091.txt',
     'agent_note': 'Two drones diverted by the same contingency logic to the same alternate pad (a shared boundary rule).'},
    {'id': 'r5:64', 'bottleneck': 'r5-B7', 'role': 'd',
     'source': 'FAA and TSA, Part 108 NPRM, Sec. VI.D (proposed § 108.165(e))', 'version': 'published 7 Aug 2025',
     'url': 'https://www.govinfo.gov/content/pkg/FR-2025-08-07/pdf/2025-14992.pdf',
     'quote': ['Before beginning operations in a new area, FAA proposes in § 108.165(e) that the operator would need to ensure that '
               'the planned operations minimize risk to persons and property on the ground',
               'The operator would be required to verify the maximum height of obstructions.'],
     'raw_file': R + 'FR-2025-14992.txt',
     'agent_note': 'Proposed rule: obstacles assessed before operations begin in a new area (a one-time boundary), no required '
                   'refresh interval.'},
    {'id': 'r5:65', 'bottleneck': 'r5-B7', 'role': 'd',
     'source': 'FAA, Certificate of Waiver 107W-2024-04627 (Zipline), special provision 12', 'version': 'signed 16 Jan 2025',
     'url': 'https://www.faa.gov/media/90041',
     'quote': ['Prior to conducting operations under this Waiver, the RPIC must perform a documented site survey to:',
               '1) Identify flight operational area obstacles and boundaries so as to avoid collision with, or damage to property;'],
     'raw_file': R + 'faa_media_90041.txt',
     'agent_note': 'Survey before operations (a boundary at the start of operations), as in the NPRM.'},

    {'id': 'r5:73', 'bottleneck': 'r5-B7', 'role': 'a',
     'source': 'NTSB, Aviation Investigation Preliminary Report WPR26LA002 (Amazon MK30 N791PA, Tolleson, AZ, 1 Oct 2025)',
     'version': 'preliminary report ("subject to change"), current version fetched 2026-09-30; no final report yet',
     'url': 'https://data.ntsb.gov/carol-repgen/api/Aviation/ReportMain/GenerateNewestReport/201773/pdf',
     'quote': ['On October 1, 2025, about 0958 mountain standard time, an Amazon.Com Services LLC, MK30,'],
     'raw_file': R + 'ntsb_newest_201773.txt',
     'agent_note': 'The second aircraft of r5:60, nine minutes after the first. Id out of sequence: added after r5:72.'},

    # ---------------- r5-B8 (not shown open here; size gap is r2-B6): cost of collecting robot training data
    {'id': 'r5:66', 'bottleneck': 'r5-B8', 'role': 'a',
     'source': 'IFR, World Robotics 2026 press conference, market presentation (slide "Focus: Humanoids")',
     'version': 'slides dated 24 Sep 2026',
     'url': 'https://ifr.org/downloads/press_docs/Market_Presentation_WR_Press_Conference_2026.pdf',
     'quote': ['Lack of training data'],
     'raw_file': R + 'ifr_Market_Presentation_WR_Press_Conference_2026.txt',
     'agent_note': 'Listed by the IFR among the three major challenges for humanoids in 2026 (with safety/reliability, r5:13, '
                   'and the business case, r5:21).'},
    {'id': 'r5:67', 'bottleneck': 'r5-B8', 'role': 'b',
     'source': 'Ma, Bi, ... Zhou (PKU, NUS, MIT, UCSB, NVIDIA), HumanScale: Egocentric Human Video Can Outperform Real-Robot Data '
               'for Embodied Pretraining',
     'version': 'arXiv v1, 18 Jun 2026 (only version)', 'url': 'https://arxiv.org/abs/2606.20521v1',
     'quote': ['Teleoperated real-robot trajectories remain the dominant pretraining source due to their precise action supervision '
               'and embodiment alignment, yet their scalability is limited by high collection cost, acquisition difficulty, and '
               'low behavioral and environmental diversity.'],
     'raw_file': R + '2606.20521v1.txt', 'agent_note': '2026 statement.'},
    {'id': 'r5:68', 'bottleneck': 'r5-B8', 'role': 'a',
     'source': 'Ma et al., HumanScale (Sec. 2.1-2.2)', 'version': 'arXiv v1, 18 Jun 2026', 'url': 'https://arxiv.org/abs/2606.20521v1',
     'quote': ['even the most generous aggregations of the entire public supply total only ∼2 × 104 hours',
               'even the low-cost ALOHA platform costs ∼$20k per station'],
     'raw_file': R + '2606.20521v1.txt',
     'agent_note': 'Quantitative statement, no target: "104" is 10^4 with the superscript lost in extraction (about 20,000 public '
                   'robot hours). Hardware per station about $20k; no cost per hour of data is given. The size gap against a '
                   'target is family R2\'s r2-B6 and is not counted again here.'},
    {'id': 'r5:69', 'bottleneck': 'r5-B8', 'role': 'd',
     'source': 'Ma et al., HumanScale (abstract; Sec. 4)', 'version': 'arXiv v1, 18 Jun 2026', 'url': 'https://arxiv.org/abs/2606.20521v1',
     'quote': ['pretrain on egocentric human video to learn diverse world representations, then adapt with a small amount of '
               'labeled real-robot data for action-space alignment.',
               'In our 100-hour recipe, for instance, the egocentric data comprises roughly 45,000 trajectories, whereas the '
               'real-robot data contains only about 8,000'],
     'raw_file': R + '2606.20521v1.txt',
     'agent_note': 'Human-video pretraining family; the paper also counts data by hours (the clock) and notes an hour of '
                   'teleoperation carries fewer trajectories (idle time), i.e. hours are the wrong unit.'},
    {'id': 'r5:70', 'bottleneck': 'r5-B8', 'role': 'd',
     'source': 'Churchill Capital Corp XI and Agility Robotics, Form S-4, Business of Agility (physical AI)', 'version': 'filed 4 Sep 2026',
     'url': 'https://www.sec.gov/Archives/edgar/data/2074973/000121390026097764/ea0297114-04.htm',
     'quote': ['Agility combines learning from demonstration — including teleoperation, motion capture and simulated examples — with '
               'reinforcement learning, allowing Digit to refine behaviors through repeated practice in simulation before '
               'deployment into customer environments.',
               'Over time, these capabilities are expected to continue improving through learning across fleets of deployed robots.'],
     'raw_file': R + 'sec_agility_s4_ea0297114-04.txt',
     'agent_note': 'Demonstration + simulation RL before deployment (a train/deploy boundary), then fleet learning after it.'},
    {'id': 'r5:71', 'bottleneck': 'r5-B8', 'role': 'd',
     'source': 'Figure AI, "Introducing Figure 03"',
     'version': 'Figure page 9 Oct 2025', 'url': 'https://www.figure.ai/news/introducing-figure-03',
     'quote': ['Figure 03 also includes 10 Gbps mmWave data offload capability, allowing the entire fleet to upload terabytes of data '
               'for continuous learning and improvement.'],
     'raw_file': R + 'figure_introducing-figure-03.txt',
     'agent_note': 'Fleet data offload family; with r5:10, offload happens at the dock during shift breaks (clock-bound windows).'},
    {'id': 'r5:72', 'bottleneck': 'r5-B8', 'role': 'd',
     'source': 'UBTECH Robotics, Annual results announcement 2025 (HKEX)', 'version': 'dated 31 Mar 2026',
     'url': 'https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0331/2026033102607.pdf',
     'quote': ['We are building and operating humanoid robot data collection and testing centers in multiple locations, and '
               'establishing a one-stop embodied intelligence data collection platform.'],
     'raw_file': R + 'hkex_ubtech_2025_annual_results_2026033102607.txt',
     'agent_note': 'Dedicated data-collection centres (staged collection, separate from deployment); cost not disclosed.'},
]

BOTTLENECKS = [
    {'id': 'r5-B1', 'name': 'Humanoid battery runtime against a working shift and a 24-hour day',
     'problem': 'One battery cycle of a humanoid lasts a few hours; a shift is 8-10 h and customers want multi-shift use. '
                'Makers bridge it by docking, fast charging or hot-swapping, whose day-level performance is claimed, not measured.',
     'open': True,
     'benchmark': 'runtime per charge (h) against the customer shift (10 h at BMW); productive hours per 24 h',
     'best': 'deployed: up to 4 h per charge (Digit v4, Agility 2025; NEO spec 4 h), Digit 4 at 2:1 run-to-charge (at most 16 of '
             '24 h); announced: Digit 5 90-min battery, 10:1, "more than 20 hours of productive work in a 24-hour day" (early '
             'access H1 2027); claimed: UBTech Walker S2 "3-minute autonomous battery swap and 24-hour continuous operation"',
     'target': 'a full working day (IFR 2025: "a battery cycle does not last a full working day"); a 10-hour shift (Figure at '
               'BMW); multi-shift use in a 24-hour day (Agility S-4)',
     'gap_note': 'Per cycle: 4 h of a 10-hour shift = 40% (cross-source: Agility runtime, BMW shift). Per day: deployed Digit 4 at '
                 'most 16/24 h = 67%; announced Digit 5 at least 20/24 = 83% (a specification, not delivered). CONTRARY at the '
                 'day level: UBTech claims 24-hour operation by swapping on a robot delivered at the 1,000-unit level in 2025 '
                 '(a results-announcement claim; no measured hours worked per day). The double check may read this CONTESTED; '
                 'the per-cycle reading stands.',
     'assumptions': ['opportunity charging at a dock or mat: continuity assumes the workflow leaves charging windows ("shift '
                     'breaks", "a certain period of time during the use case") - charging slots set by the task\'s clock',
                     'fast charging (10:1): shorter cycles, more boundaries per day (runtime per charge falls from 4 h to 90 min)',
                     'autonomous hot-swap: the energy boundary is triggered by battery state and task priority; needs swap '
                     'stations and spare packs in the cell',
                     'self-docking on need in the home (state-triggered), where idle time is plentiful'],
     'cpu_testable': False,
     'cpu_note': 'runtime and availability are measured on hardware in service; a CPU duty-cycle model (charge/swap scheduling) '
                 'can be simulated but would test scheduling, not battery capacity'},
    {'id': 'r5-B2', 'name': 'Humanoid functional reliability in production (task accuracy, interventions, hardware failures)',
     'problem': 'Humanoids in commercial work report task accuracy near 98% and name hardware failure points, while customer '
                'lines set targets above 99% per shift and zero interventions; interventions, uptime and MTBF go undisclosed.',
     'open': True,
     'benchmark': 'task accuracy / success per shift; interventions per shift (Figure\'s BMW KPIs); operational accuracy on tote '
                  'handling (Agility S-4)',
     'best': 'about 98% operational accuracy (Digit v4 at Schaeffler, ~25,000 totes; at GXO, >100,000 totes); interventions per '
             'shift not disclosed by any source',
     'target': '> 99% success per shift and zero interventions per shift, 84 s cycle (the BMW line\'s KPIs for Figure 02)',
     'gap_note': 'CROSS-SOURCE (Agility\'s number, Figure\'s target; different tasks): failure share ~2% against <1%, at least 2x '
                 'the target\'s. Figure reports no achieved KPI values; neither company reports interventions per shift. The IFR '
                 '(2025, 2026) says humanoids have yet to prove reliability. Gap direction robust, size uncertain.',
     'assumptions': ['field calibration per robot (periodic, clock- or event-scheduled by staff)',
                     'reliability fixed by redesign at hardware-generation boundaries (a whole fleet retired and replaced)',
                     'vendor-owned fleets (RaaS) with time-based KPIs (uptime, Mean Time Between Incidents) tracked centrally; '
                     'values not published',
                     'human reset/pause as the recovery path (interventions counted per shift)'],
     'cpu_testable': False,
     'cpu_note': 'the metric is measured on physical robots in customer plants; no CPU benchmark reproduces it'},
    {'id': 'r5-B3', 'name': 'Unit cost and business case of humanoids for productive work',
     'problem': 'Industrial humanoids cost several times their makers\' own volume targets and sell at negative or unknown '
                'margins; the cheap, profitable humanoids sell mostly to research and education, not to productive work.',
     'open': True,
     'benchmark': 'bill of materials per robot at commercial launch against the maker\'s volume cost targets (Agility S-4); gross '
                  'margin; share of humanoid revenue from productive industrial scenes',
     'best': 'BOM about $150,000 at launch (Digit v5); 2025 cost of goods sold $4.5M against net sales $1.8M (Agility); Unitree '
             'unit price RMB 167,600 at 62.91% gross margin, but industry applications 9.01% of humanoid revenue and explicit '
             'productive scenes 2.64% (Jan-Sep 2025); UBTech ~RMB 760,000 per unit (1,079 units, RMB 820M)',
     'target': 'BOM about $75,000 at 1,000 robots per year and about $30,000 at 10,000 per year (Agility\'s own targets); an '
               'economically viable business case (IFR 2026: lacking)',
     'gap_note': 'BOM 2.0x the 1,000/yr target and 5.0x the 10,000/yr target (same document). Agility COGS 2.5x sales in 2025. '
                 'CONTRARY on price: Unitree sells humanoids cheaply and profitably, but its own filing says industrial use is not '
                 'yet at scale and only 2.64% of its humanoid revenue came from explicit productive scenes. The double check may '
                 'read the price part CONTESTED; the productive-work business case stays open on the IFR\'s 2026 statement.',
     'assumptions': ['volume cost-down: cost falls with cumulative production (tooling, in-house lines); assumes the demand '
                     'arrives (Figure: 100,000 in four years; IFR: ~7,000 full-size sold worldwide in 2025)',
                     'RaaS: a calendar subscription priced below the fully burdened labour it replaces; assumes a 5-year life and '
                     'vendor-borne maintenance (durability unproven)',
                     'low-price volume strategy (Unitree G1): margin traded for adoption; buyers mostly research and education',
                     'payback computed from planning assumptions, not measured deployments'],
     'cpu_testable': False,
     'cpu_note': 'cost and margins are business data; nothing to run on a CPU beyond arithmetic'},
    {'id': 'r5-B4', 'name': 'Warehouse robotic stow and pick: item coverage, rate and defects against the production target',
     'problem': 'Robotic stowing into dense fabric pods runs in production below its own rate and quality targets and below the '
                'human rate, and covers most but not all item types; the rest goes to humans.',
     'open': True,
     'benchmark': 'Amazon robotic stow: units per hour (UPH), share of items handled, outcomes over 100,000 attempts (Stow paper, '
                  'Table II); Vulcan item coverage',
     'best': '224 UPH (March 2025); 85.86% success, 9.31% unproductive, 4.83% defects; ~75% of item types (Vulcan)',
     'target': 'design: 80% of items at 300 UPH, more than 20 h/day, 7 days/week, no interruptions needing human intervention; '
               'unproductive-stow aim 3%; human stowers 243 UPH on the same floor',
     'gap_note': 'Same paper: 224/243 = 92.2% of the human rate, 224/300 = 74.7% of the design rate; unproductive 9.31% vs 3% '
                 '(3.1x). Coverage 75% vs 80% (company page vs paper, denominators may differ). Hours per day and interventions '
                 'not reported. Ocado\'s best site picks c.50% of volume robotically (different task, no target; supporting only).',
     'assumptions': ['human-in-the-loop decomposition: a human inducts and screens items, robots take the rest; unhandled items '
                     'tagged to humans',
                     'learned risk model with a fixed exploration rate (up to 5%, epsilon-greedy) and retraining when behaviours '
                     'change (data recollected at development boundaries)',
                     'real-robot training data (simulation judged insufficient for touch and deformation)',
                     'dedicated hardware per sub-task (band separator, plank, conveyor paddles)'],
     'cpu_testable': False,
     'cpu_note': 'the benchmark is a production warehouse; only a toy bin-packing or risk-model proxy would run on CPU'},
    {'id': 'r5-B5', 'name': 'Field harvesting robots: throughput and success against human pickers',
     'problem': 'Selective fruit-harvesting robots pick at a fraction of the human rate, fail a fifth of attempts in orchards, and '
                'still need a human to move the platform between stops.',
     'open': True,
     'benchmark': 'berries per minute against a human picker in the same field (CLASP); per-attempt success and cycle time over '
                  '1,738 apple arm cycles (2025 season)',
     'best': '32 berries/min with the gripper manually aligned (autonomous rate not reported), 92% autonomous success (23/25); '
             'apple: 80.0% per-attempt success, 7.53 s per arm cycle',
     'target': 'human picker 55 berries/min (same paper); hand-picked firmness 195.59 g/mm',
     'gap_note': '58% of the human rate at best (42% short), and that with manual alignment; firmness 15% lower. The apple paper '
                 'gives no human baseline (supporting only). n = 25 for CLASP\'s success rate, flagged by its authors.',
     'assumptions': ['stop-and-go harvesting: the row is cut into stops at fixed intervals chosen by a human operator driving the '
                     'tractor (clock/boundary set outside the robot); the authors propose repositioning by fruit distribution '
                     'instead',
                     'teleoperated transport between fixed test locations; autonomy only at the stop',
                     'perception from fixed viewpoints (40.3% of clusters visible to the global camera in CLASP)'],
     'cpu_testable': False,
     'cpu_note': 'field throughput needs orchards and hardware; a CPU simulation of stop scheduling would not be the benchmark'},
    {'id': 'r5-B6', 'name': 'Remote human help per robot (teleoperation dependence)',
     'problem': 'Humanoids, sidewalk robots, delivery drones (and robotaxis) rely on remote humans; the ratio of humans to robots '
                'and the frequency of interventions are rarely disclosed.',
     'open': False,
     'benchmark': 'robots per remote human; interventions per robot-hour (not published by any source found)',
     'best': 'delivery drones: up to 6 sUA per remote pilot by FAA waiver (Zipline, 2025); robotaxi comparator: ~70 remote-'
             'assistance agents on duty for over 3,000 vehicles (Waymo 2026); Starship claims "over 99% autonomy" (undefined)',
     'target': 'none numeric: the FAA NPRM proposes a 1:1 default and says "1:many at scale" is wanted but not standardised',
     'gap_note': 'not shown open: B-a and B-b are quoted (Agility, FAA 2025, Serve 2026, 1X 2025, Markey 2026), but no source '
                 'states a numeric target, and every AV company refused to disclose intervention frequency; one vendor '
                 '(Starship) claims the problem largely solved for sidewalk robots. No B-c is recorded.',
     'assumptions': ['scheduled teleoperation sessions booked on the calendar (1X Expert Mode), doubling as data collection',
                     'continuous remote monitoring with situation-triggered assists (Serve), partly offshore',
                     'event-driven remote assistance requested by the robot (Waymo, Starship "on standby")',
                     'ratio raised case by case by waiver with redundancy and one operational volume per pilot (FAA/Zipline)',
                     'system-level supervision: pilots monitor the whole system, not each flight (Wing; ratio not stated)'],
     'cpu_testable': True,
     'cpu_note': 'a queueing/fleet model of robot-initiated help requests against scheduled or continuous monitoring runs on CPU '
                 'in minutes; no public intervention data exist to calibrate it'},
    {'id': 'r5-B7', 'name': 'Delivery-drone collisions with obstacles and other aircraft (incident record)',
     'problem': 'Commercial and test delivery drones have struck temporary obstacles and each other; obstacle surveys run on a '
                'fixed schedule or once before operations.',
     'open': False,
     'benchmark': 'NTSB reports (incidents), no rate against a target',
     'best': 'not applicable (incident reports: two MK30 struck a crane erected about 2 h earlier, Oct 2025; test accidents 2024-25)',
     'target': 'none numeric found (the Part 108 NPRM sets no obstacle-data refresh interval)',
     'gap_note': 'not shown open: only B-a and B-d quotes; no 2025-26 source states the problem as open with a rate against a '
                 'target. Recorded because the scope names safety incidents and because the survey assumption is explicit.',
     'assumptions': ['obstacle survey on a fixed clock (Amazon: rooftop scans twice per day) - assumes the obstacle map changes '
                     'slowly relative to the interval',
                     'obstacle assessment once before operations in a new area (NPRM; Zipline waiver site survey)',
                     'shared contingency rules (divert to the same alternate pad) across drones'],
     'cpu_testable': True,
     'cpu_note': 'a CPU simulation of obstacle arrival against scan schedules is cheap; no public incident-rate data to calibrate it'},
    {'id': 'r5-B8', 'name': 'Cost of collecting robot training data',
     'problem': 'Teleoperated robot data is costly and slow to collect; the IFR lists lack of training data as a major challenge '
                'for humanoids.',
     'open': False,
     'benchmark': 'hours of public robot data; hardware cost per collection station (no primary source gives cost per hour)',
     'best': 'about 2 x 10^4 public robot hours in aggregate; ALOHA about $20k per station (HumanScale 2026)',
     'target': 'none numeric here; the size target (Goldberg\'s LLM-equivalent) is family R2\'s r2-B6',
     'gap_note': 'not shown open in this family: B-a and B-b are quoted (IFR 2026, HumanScale 2026) but no 2025-26 primary source '
                 'reports a data-collection cost against a target; per-hour cost figures seen were vendor blogs (not used). The '
                 'size gap is r2-B6 and is not double-counted.',
     'assumptions': ['teleoperated collection in staged scenes, counted in hours (the clock), though an hour of teleoperation '
                     'carries fewer trajectories than an hour of human video',
                     'pretrain on human video, adapt on a small robot set (a pretrain/post-train boundary)',
                     'demonstration + simulation RL before deployment, fleet learning after (a train/deploy boundary)',
                     'fleet data offload at docks during shift breaks; dedicated data-collection centres'],
     'cpu_testable': False,
     'cpu_note': 'data cost is an operational figure; CPU experiments would not measure it'},
]
