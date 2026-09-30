"""ROB1 stage 1b, family R5 (Robotics/DECLARATION.md): the double check of the news-and-industry bottlenecks r5-B1 ... r5-B8.

Written by a second agent that did not harvest family R5. For every bottleneck in `claims_r5.BOTTLENECKS` it searched
independently for the strongest contrary evidence: a 2025-26 source reporting the target reached on the named metric, a
deployed system that does it, or a source arguing that the bottleneck is misframed. It used queries and sources different
from the harvester's: 16 WebSearch queries (the session's WebSearch budget then ran out; queries 17-18 were not run), then
the arXiv API, company and regulator pages fetched by URL, the Federal Register API and the Federal Reserve H.10 release
(log in /tmp/claude-0/rob_src/r5x/search/queries.txt; every fetch with its HTTP status in r5x/search/fetch_log.txt). It also
re-read the harvester's quotes and numbers against the harvester's raw texts (/tmp/claude-0/rob_src/r5/txt/); a scratch copy
of Open_Bottlenecks/checks/verify.py pointed at claims_r5.py read "quotes found verbatim: 144 of 144 (claims 74; raw files
32, missing 0)" (r5x/verify_r5_recheck.txt).

Every source was fetched on 2026-09-30 through the session proxy with curl (TLS verification on). Text was extracted with the
harvester's own extractors (copied to r5x/): PDFs by pymupdf (`page.get_text()`, pages joined by newlines); HTML by
BeautifulSoup 4 (`get_text('\\n')` after removing script/style/noscript/svg, runs of spaces and blank lines collapsed). X
(Twitter) posts were read through publish.twitter.com oEmbed (the post text as the JSON's HTML gives it, which truncates
long posts with an ellipsis) and a YouTube video's title through youtube.com oEmbed; the Federal Register API response
(JSON) was written to a text file as one line per document (date, type, number, title). Raw files live outside the
repository under /tmp/claude-0/rob_src/ (`raw_file` is relative to that root; the fetched originals are in r5x/src/);
their sha256 is in /tmp/claude-0/rob_src/r5x/SHA256SUMS.txt and in the dossier docs/citations/rob1_r5_2026-09-30.md (section
"Stage 1b double check"). Four harvester PDFs were re-fetched into r5x/ and are byte-identical to the harvester's copies
(2505.04572v1, 2609.18051v1, 2606.14089v1 and the Unitree SSE reply); the Figure BMW page was re-fetched and extracts to
identical text. SEC EDGAR refused this agent's User-Agent (HTTP 403), so the two SEC filings quoted here (Agility S-4, Serve
10-K) are the harvester's fetched copies, copied into r5x/ unchanged and marked as such in `version`. Where an extractor
split a sentence across lines at a hyphen that starts a line ("24\\n-hour"), or split a label from its value, the quote is
cut with "[...]" at that point or keeps the extractor's space ("Success Rate : Over 99.9%"), as stated in the note.

Fields. role = 'x' (a double-check claim). `refutes` = the bottleneck the claim bears on. `contrary` = True when the claim is
contrary evidence (the target reached, a deployed system that does it, or a misframing argument); False when it is a
re-check of the harvester's reading (a number, a "best" or a target the harvester got wrong, overstated or left out) or
evidence that supports the harvester, which bears on B-c but is not evidence that the bottleneck is closed.
`shows_target_reached` = True only if the verified quote shows the target reached on the named metric of that bottleneck.
`agent_note` is the double-checker's reading, fair to both sides; it is not the source's words. Company statements, CEO
posts and press releases are the company's own claims, not independent measurements, and are recorded as such. Currency
conversions in notes use the Federal Reserve H.10 noon buying rate for 25 Sep 2026 (6.7110 yuan per US dollar, r5x:17),
today's rate, not the rate on the transaction dates; they are indicative only (agent's arithmetic).

CHECKS: one entry per bottleneck: what was searched, what was found, and `harvester_errors` (quotes or numbers the harvester
got wrong, overstated or left out; an empty list when none was found).
"""

R = 'r5x/txt/'

CLAIMS = [
    # ---------------- r5-B1: humanoid battery runtime against a working shift and a 24-hour day
    {'id': 'r5x:1', 'bottleneck': 'r5-B1', 'role': 'x', 'refutes': 'r5-B1', 'contrary': True, 'shows_target_reached': False,
     'source': 'Shanghai Kepler Robotics Co., Ltd, press release "World\'s First Commercially Available Hybrid-Architecture '
               'Humanoid Robot Moves into Mass Production" (PR Newswire)',
     'version': 'published 26 Sep 2025 (PR Newswire dateline)',
     'url': 'https://www.prnewswire.com/news-releases/worlds-first-commercially-available-hybrid-architecture-humanoid-robot-moves-into-mass-production-kepler-marks-the-start-of-a-new-industrial-era-302568138.html',
     'quote': ['Purpose-built for industrial integration, the K2 "Bumblebee" achieves up to 81.3% energy efficiency with its hybrid '
               'architecture, allowing for up to eight hours of operation on a single charge.',
               'has announced the start of mass production for its K2 "Bumblebee" model, confirming through a recently released '
               'video that the world\'s first commercially available hybrid-architecture humanoid robot has begun shipping to customers.'],
     'raw_file': R + 'prn_kepler_k2_mass_production.txt',
     'agent_note': 'Contrary on the per-cycle metric: a humanoid in mass production and shipping since Sep 2025 is specified at up '
                   'to 8 h per charge, twice the 4 h the harvester gave as the best deployed. Against the IFR\'s unnumbered '
                   '"full working day" read as an 8-hour shift, the company claims the target; against the 10-hour BMW shift the '
                   'harvester used, 8/10 = 80%, still short. Not counted as the target reached: a maker\'s specification ("up '
                   'to"), no hours measured at a customer, and the named target is the 10-hour shift.'},
    {'id': 'r5x:2', 'bottleneck': 'r5-B1', 'role': 'x', 'refutes': 'r5-B1', 'contrary': True, 'shows_target_reached': False,
     'source': 'Kepler Robotics, press release "Kepler\'s Forerunner K2 \'Bumblebee\' Robot Completes 8-Hour Livestream at WAIC 2025" '
               '(PR Newswire)',
     'version': 'published 1 Aug 2025 (PR Newswire dateline); the livestream was on 27 Jul 2025',
     'url': 'https://www.prnewswire.com/news-releases/keplers-forerunner-k2-bumblebee-robot-completes-8-hour-livestream-at-waic-2025-signaling-major-step-toward-real-world-deployment-of-embodied-ai-in-industrial-settings-302520070.html',
     'quote': ['first 8-hour nonstop livestream by a bipedal humanoid robot. From 9 AM to 5 PM [...] the K2 demonstrated its '
               'groundbreaking "1-hour charge, 8-hour operation" capability',
               'The 8-hour endurance benchmark was strategically selected to meet real-world industrial demands, balancing '
               'technical feasibility with operational requirements.'],
     'raw_file': R + 'prn_kepler_k2_8h_livestream.txt',
     'agent_note': 'A public 8-hour run on one charge (9 AM to 5 PM) at an exhibition, stated by the maker. It supports r5x:1\'s '
                   'specification with a demonstration, but at a trade show, not a customer shift, and the tasks and load are '
                   'not given. The "[...]" skips an extractor line break before a comma.'},
    {'id': 'r5x:3', 'bottleneck': 'r5-B1', 'role': 'x', 'refutes': 'r5-B1', 'contrary': False, 'shows_target_reached': False,
     'source': 'Figure AI, "F.03 Battery Development"', 'version': 'published 17 Jul 2025 (page date)',
     'url': 'https://www.figure.ai/news/f-03-battery-development',
     'quote': ['Run Time: 2.3 kWh enables 5 hours of run time at peak performance'],
     'raw_file': R + 'figure_f-03-battery-development.txt',
     'agent_note': 'Re-check of the harvester\'s "best deployed runtime per charge: up to 4 h". Figure 03, which Figure says it '
                   'has delivered in the hundreds (r5x:15) and which arrived at BMW in Jun 2026 (harvester\'s screened page), is '
                   'specified at 5 h per charge at peak performance: 5/10 = 50% of the BMW shift, not 40%. A company '
                   'specification; the gap stays open on the per-cycle metric.'},
    {'id': 'r5x:4', 'bottleneck': 'r5-B1', 'role': 'x', 'refutes': 'r5-B1', 'contrary': True, 'shows_target_reached': False,
     'source': 'Brett Adcock (Figure AI founder and CEO), posts on X about the F.03 livestream; Figure\'s YouTube livestream title',
     'version': 'posts dated 20 May 2026 and 22 May 2026 (read through publish.twitter.com oEmbed, text truncated by oEmbed); '
                'YouTube video JeeJJ42TKQU (oEmbed title)',
     'url': 'https://x.com/adcock_brett/status/2057145678355460126',
     'quote': ['F.03 has been working fully autonomously, non-stop for a full week'],
     'raw_file': R + 'x_adcock_2057145678355460126.txt',
     'agent_note': 'Contrary at the day level (multi-shift use in a 24-hour day): a humanoid work cell ran around the clock for '
                   'days, per the company\'s CEO and its livestream ("F.03 Livestream: Day 9 (Hour 192-200)", r5x:8). A single '
                   'Figure 03 is specified at 5 h per charge (r5x:3), so continuity must have come from more than one robot or '
                   'from charging breaks; press reports (not primary, not used) describe robots rotating to the charger. The '
                   'posts give no per-robot productive hours. A demonstration at a company site, not a customer deployment, so '
                   'not the target reached on the named metric.'},
    {'id': 'r5x:5', 'bottleneck': 'r5-B1', 'role': 'x', 'refutes': 'r5-B1', 'contrary': False, 'shows_target_reached': False,
     'source': 'Churchill Capital Corp XI and Agility Robotics, Form S-4, Business of Agility (Digit v4 and v5 descriptions)',
     'version': 'filed with the SEC 4 Sep 2026 (accession 0001213900-26-097764); the harvester\'s fetched copy (sha256 e5313a60...), '
                'copied unchanged: SEC EDGAR refused this agent\'s User-Agent (HTTP 403)',
     'url': 'https://www.sec.gov/Archives/edgar/data/2074973/000121390026097764/ea0297114-04.htm',
     'quote': ['Approximately 20 hours of operation within a 24 [...] hour period through an industry [...] leading 10:1 charge '
               'ratio, significantly increasing robot utilization across multiple shifts.',
               'carrying capacity, four [...] hour runtime with autonomous charging'],
     'raw_file': R + 'sec_agility_s4_ea0297114-04.txt',
     'agent_note': 'Re-check of r5:5. The press release (15 Sep 2026) says "more than 20 hours of productive work in a 24-hour '
                   'day"; the company\'s own securities filing eleven days earlier says "Approximately 20 hours of operation". '
                   'The harvester quoted only the stronger wording and wrote "at least 83%"; about 83% (20/24) is what the '
                   'filing supports. The filing also confirms Digit v4\'s four-hour runtime. The "[...]" marks hyphens that the '
                   'extractor put at the start of a line ("24\\n-hour").'},
    {'id': 'r5x:6', 'bottleneck': 'r5-B1', 'role': 'x', 'refutes': 'r5-B1', 'contrary': False, 'shows_target_reached': False,
     'source': 'UBTECH Robotics Corp Ltd, Interim results announcement for the six months ended June 30, 2026 (Future Plans)',
     'version': 'dated 28 Aug 2026 (PDF created 28 Aug 2026); fetched from the company\'s announcements page (HKEX filing copy)',
     'url': 'https://owebsite-cdn.ubtrobot.com/resources/file/2026/09/02/844614814105669.pdf',
     'quote': ['on-device intelligence, autonomous battery swapping, and industrial-grade safety, thereby enhancing overall system '
               'integration, system stability, single-unit autonomy, swarm collaboration, and continuous operation capabilities.'],
     'raw_file': R + 'ubtech_interim_results_2026H1.txt',
     'agent_note': 'Supports the harvester\'s caution on r5:8: five months after claiming "24-hour continuous operation" by '
                   'swapping, UBTech lists autonomous battery swapping and continuous operation among capabilities it will '
                   'advance, and gives no measured hours worked per day at a customer. Not evidence that the claim is false.'},

    # ---------------- r5-B2: humanoid functional reliability in production
    {'id': 'r5x:7', 'bottleneck': 'r5-B2', 'role': 'x', 'refutes': 'r5-B2', 'contrary': True, 'shows_target_reached': False,
     'source': 'AGIBOT and Longcheer Technology, press release "AGIBOT and Longcheer Technology Achieve World\'s First Embodied AI '
               'Deployment in Consumer Electronics Precision Manufacturing Mass Production Line" (PR Newswire)',
     'version': 'published 15 Apr 2026 (PR Newswire dateline); the same text is on agibot.com/article/231/detail/60.html',
     'url': 'https://www.prnewswire.com/news-releases/agibot-and-longcheer-technology-achieve-worlds-first-embodied-ai-deployment-in-consumer-electronics-precision-manufacturing-mass-production-line-302742853.html',
     'quote': ['Multiple AGIBOT G2 robots have been officially integrated into Longcheer\'s tablet production lines, working '
               'alongside human operators in real manufacturing environments.',
               'Success Rate : Over 99.9% in continuous operation',
               'Operational Stability : Supports 24/7 autonomous operation with minimal human intervention, over 140 hours of '
               'cumulative continuous operation, with downtime loss below 4%',
               'In just four months, the AGIBOT G2 was integrated into Longcheer\'s mass production line, delivering stable, '
               'continuous operation and meeting all key targets.'],
     'raw_file': R + 'prn_agibot_longcheer_2026-04-15.txt',
     'agent_note': 'The strongest contrary claim found for r5-B2. On a customer\'s mass-production line (tablet loading and '
                   'unloading at test stations), the maker and the customer claim over 99.9% success, above the >99% per-shift '
                   'target the harvester took from BMW (cross-source and cross-task, as the harvester\'s own gap was), and the '
                   'customer\'s robotics head says all key targets were met. Not counted as the target reached: the second half '
                   'of the named target (zero interventions per shift) is "minimal human intervention", not zero; success is "in '
                   'continuous operation", not per shift; the G2 is a wheeled humanoid; the figures are company claims without '
                   'counts or definitions. The extractor split each label from its value; the space before the colon is its.'},
    {'id': 'r5x:8', 'bottleneck': 'r5-B2', 'role': 'x', 'refutes': 'r5-B2', 'contrary': True, 'shows_target_reached': False,
     'source': 'Brett Adcock (Figure AI CEO), posts on X about the F.03 package-sorting livestream; Figure YouTube livestream title',
     'version': 'posts dated 14 May 2026 and 22 May 2026 (publish.twitter.com oEmbed; text truncated by oEmbed); YouTube video '
                'JeeJJ42TKQU',
     'url': 'https://x.com/adcock_brett/status/2057651077928145235',
     'quote': ['We just wrapped what began as an 8-hour challenge - and it ran for 200 hours without a failure'],
     'raw_file': R + 'x_adcock_2057651077928145235.txt',
     'agent_note': 'Contrary on interventions: the CEO states 200 hours (25 eight-hour shifts) without a failure on a package-'
                   'sorting cell run by Helix-02, with a public livestream (r5x:9). If "failure" includes human pauses and resets, '
                   'this is the "zero interventions per shift" half of the BMW target. Not counted as the target reached: a '
                   'demonstration at the company\'s own site, "failure" is not defined, and no per-package success rate is '
                   'given, so the ">99% success per shift" half is not shown. CEO posts are company statements.'},
    {'id': 'r5x:9', 'bottleneck': 'r5-B2', 'role': 'x', 'refutes': 'r5-B2', 'contrary': True, 'shows_target_reached': False,
     'source': 'Brett Adcock (Figure AI CEO), post on X, 14 May 2026; YouTube oEmbed of Figure\'s livestream',
     'version': 'post dated 14 May 2026 (oEmbed text, truncated); YouTube video JeeJJ42TKQU title as served by oEmbed',
     'url': 'https://x.com/adcock_brett/status/2054973511572271172',
     'quote': ['Our original goal was an 8-hour run. After zero failures yesterday, we decided to keep going. We’re now over 24 '
               'hours of continuous autonomous operation without a failure.'],
     'raw_file': R + 'x_adcock_2054973511572271172.txt',
     'agent_note': 'Same event as r5x:8, at the 24-hour mark; the YouTube title of the last segment reads "F.03 Livestream: Day '
                   '9 (Hour 192-200)" (youtube_oembed_JeeJJ42TKQU.txt). Recorded so the claim has two dated statements.'},
    {'id': 'r5x:10', 'bottleneck': 'r5-B2', 'role': 'x', 'refutes': 'r5-B2', 'contrary': False, 'shows_target_reached': False,
     'source': 'Figure AI, "F.02 Contributed to the Production of 30,000 Cars at BMW" (Hardware Reliability and Learnings)',
     'version': 'published 19 Nov 2025; re-fetched, text identical to the harvester\'s copy',
     'url': 'https://www.figure.ai/news/production-at-bmw',
     'quote': ['Across 1,250+ operational hours, Figure 02 recorded minimal hardware failures while generating critical data that '
               'informed the build procedures, component architecture, and mechanical design of Figure 03.'],
     'raw_file': R + 'figure_production-at-bmw.txt',
     'agent_note': 'Re-check of r5:15. The harvester quoted the forearm as the "top hardware failure point" but not the sentence '
                   'before it, in which the same page says hardware failures were minimal over 1,250+ hours. Neither sentence '
                   'gives a count or a rate, so the reliability gap stays unmeasured; the harvester\'s selection was one-sided.'},
    {'id': 'r5x:11', 'bottleneck': 'r5-B2', 'role': 'x', 'refutes': 'r5-B2', 'contrary': False, 'shows_target_reached': False,
     'source': 'Figure AI, "Ramping Figure 03 Production" (Ramping Robot Operations)', 'version': 'published 29 Apr 2026 (page date)',
     'url': 'https://www.figure.ai/news/ramping-figure-03-production',
     'quote': ['Having already addressed the high-frequency hardware and software issues, our focus has shifted to the "long tail" '
               'of edge-case failures - a stage of maturity that only comes with significant fleet hours.'],
     'raw_file': R + 'figure_ramping-figure-03-production.txt',
     'agent_note': 'A company statement of progress on fleet reliability, with no metric. Recorded as context for both sides: it '
                   'claims the frequent failures are fixed, and it concedes a long tail of failures remains.'},
    {'id': 'r5x:12', 'bottleneck': 'r5-B2', 'role': 'x', 'refutes': 'r5-B2', 'contrary': False, 'shows_target_reached': False,
     'source': 'UBTECH Robotics, Interim results announcement for the six months ended June 30, 2026 (Business Review)',
     'version': 'dated 28 Aug 2026',
     'url': 'https://owebsite-cdn.ubtrobot.com/resources/file/2026/09/02/844614814105669.pdf',
     'quote': ['Key industrial scenarios have been continuously expanded, driving robots from technical verification to practical '
               'applications. We have carried out solution validation for typical industrial scenarios such as material '
               'handling, sheet metal parts loading and unloading, express sorting, seeding wall sorting, depalletizing and '
               'palletizing.'],
     'raw_file': R + 'ubtech_interim_results_2026H1.txt',
     'agent_note': 'Supports the harvester: a listed maker that sold 921 full-size humanoids in H1 2026 (r5x:16) describes its '
                   'industrial work as solution validation, not production at stated reliability.'},

    # ---------------- r5-B3: unit cost and business case of humanoids for productive work
    {'id': 'r5x:13', 'bottleneck': 'r5-B3', 'role': 'x', 'refutes': 'r5-B3', 'contrary': True, 'shows_target_reached': False,
     'source': 'Unitree Robotics and CITIC Securities, reply to the SSE second-round inquiry letter (2025 results and orders)',
     'version': 'SSE disclosure dated 20 Mar 2026; re-fetched PDF byte-identical to the harvester\'s copy (sha256 3a481485...)',
     'url': 'https://static.sse.com.cn/stock/disclosure/announcement/c/202603/002178_20260320_BLK4.pdf',
     'quote': ['2025 年，公司预计的营业收入和扣非归母净利润分别为17.08 亿元和6.00 亿元，分别同比增长3.35 倍和6.74 倍。',
               '2025 年12 月末，公司在手订单金额为2.82 亿元，同比增长93.15%'],
     'raw_file': R + 'sse_unitree_prospectus_20260320_BLK4.txt',
     'agent_note': 'Agent\'s translation: "In 2025 the company expects revenue of RMB 1.708 billion and net profit attributable '
                   '(excluding non-recurring items) of RMB 600 million, up 3.35x and 6.74x"; "at end-Dec 2025 orders in hand were '
                   'RMB 282 million, up 93.15%". The largest humanoid shipper is profitable, with humanoids its largest product '
                   'line (51.80% of main revenue in H1 2025, harvester\'s file). Cost: from the harvester\'s r5:27 figures, cost '
                   'of sales per humanoid is about RMB 167,600 x (1 - 0.6291) = RMB 62,164, about US$9,260 at 6.7110 (agent\'s '
                   'arithmetic), below Agility\'s US$30,000 BOM target at 10,000 per year. Not the target reached: the named '
                   'target is Agility\'s own BOM trajectory and "an economically viable business case" for productive work; '
                   'Unitree\'s buyers are mostly research and education (r5:27), and a maker\'s profit is not a buyer\'s case.'},
    {'id': 'r5x:14', 'bottleneck': 'r5-B3', 'role': 'x', 'refutes': 'r5-B3', 'contrary': True, 'shows_target_reached': False,
     'source': 'Kepler Robotics, press release on K2 mass production (PR Newswire)', 'version': 'published 26 Sep 2025',
     'url': 'https://www.prnewswire.com/news-releases/worlds-first-commercially-available-hybrid-architecture-humanoid-robot-moves-into-mass-production-kepler-marks-the-start-of-a-new-industrial-era-302568138.html',
     'quote': ['is priced at RMB 248,000 per unit, breaking through the million-yuan threshold of prototype humanoid robots and '
               'significantly lowering barriers for large-scale adoption.',
               'To date, Kepler Robotics has signed framework agreements covering several thousand units, with total contract '
               'value in the hundreds of millions of yuan.',
               'Ready for immediate deployment, the K2 "Bumblebee" is designed for logistics, manufacturing, R&D, government '
               'exhibitions, and specialized operations, delivering clear operational benefits.'],
     'raw_file': R + 'prn_kepler_k2_mass_production.txt',
     'agent_note': 'Contrary on the harvester\'s generalisation that "industrial humanoids cost several times their makers\' own '
                   'volume targets" (a statement resting on one maker, Agility). An industrial humanoid (30 kg payload, 8 h per '
                   'charge) is listed at RMB 248,000, about US$36,950 at 6.7110 (agent\'s arithmetic, today\'s rate), a sale '
                   'price near Agility\'s US$30,000 BOM target. Not the target reached: a price, not a BOM; framework agreements, '
                   'not deliveries; customers include "data operations" and exhibitions, so the productive-work case is not shown.'},
    {'id': 'r5x:15', 'bottleneck': 'r5-B3', 'role': 'x', 'refutes': 'r5-B3', 'contrary': False, 'shows_target_reached': False,
     'source': 'Figure AI, "Ramping Figure 03 Production"; "F.03 Battery Development"',
     'version': 'pages dated 29 Apr 2026 and 17 Jul 2025',
     'url': 'https://www.figure.ai/news/ramping-figure-03-production',
     'quote': ['delivering over 350 of our third generation humanoid robots and increasing our production rate from 1 Figure 03 per '
               'day to 1 per hour - a 24x throughput improvement in under 120 days.',
               'our end of line first pass yield is now over 80% and improving weekly'],
     'raw_file': R + 'figure_ramping-figure-03-production.txt',
     'agent_note': 'Volume progress (the harvester\'s "volume cost-down" family) with no unit cost: 350+ delivered and a one-per-'
                   'hour line; the battery page claims a "78% reduction in cost over F.02" for the pack alone. Evidence that the '
                   'cost curve is being ridden, not that a cost target is met.'},
    {'id': 'r5x:16', 'bottleneck': 'r5-B3', 'role': 'x', 'refutes': 'r5-B3', 'contrary': True, 'shows_target_reached': False,
     'source': 'UBTECH Robotics, Interim results announcement for the six months ended June 30, 2026 (Business Review; MD&A)',
     'version': 'dated 28 Aug 2026',
     'url': 'https://owebsite-cdn.ubtrobot.com/resources/file/2026/09/02/844614814105669.pdf',
     'quote': ['For the first half of 2026, full-size embodied intelligent humanoid robot products and services for all scenarios '
               'achieved revenue of RMB590.3 million, representing a year-on-year increase of 1,445.0%; achieved sales volume of '
               '921 units',
               'with an increased proportion of revenue generated from our full-size embodied smart humanoid robot products and '
               'services, which have a higher gross profit margin.',
               'Loss for the period decreased by 23.0% year-on-year to RMB338.8 million'],
     'raw_file': R + 'ubtech_interim_results_2026H1.txt',
     'agent_note': 'Contrary in part: full-size humanoids sell in volume (921 units in six months, about RMB 641,000 each, about '
                   'US$95,500 at 6.7110; agent\'s arithmetic) and at a higher margin than the rest of the business (company '
                   'gross margin 44.7%). Against it: the company still lost RMB 338.8M in the half, and its industrial work is at '
                   'solution validation (r5x:12). Buyers\' returns are not given, so the productive-work business case is not shown.'},
    {'id': 'r5x:17', 'bottleneck': 'r5-B3', 'role': 'x', 'refutes': 'r5-B3', 'contrary': False, 'shows_target_reached': False,
     'source': 'Board of Governors of the Federal Reserve System, Foreign Exchange Rates H.10 (weekly)',
     'version': 'release dated 28 Sep 2026 (rates for 21-25 Sep 2026)', 'url': 'https://www.federalreserve.gov/releases/h10/current/',
     'quote': ['Rates in currency units per U.S. dollar except as noted by an asterisk',
               'Sep. 21 Sep. 22 Sep. 23 Sep. 24 Sep. 25',
               'CHINA, P.R. YUAN 6.6947 6.6996 6.7111 6.7128 6.7110'],
     'raw_file': R + 'fed_h10_current.txt',
     'agent_note': 'The rate used for the indicative conversions in r5x:13, r5x:14 and r5x:16 (6.7110 yuan per dollar, 25 Sep '
                   '2026). The harvester made no conversions; with them, the cheapest humanoids sold (Unitree, cost of sales '
                   'about US$9,260 per unit) are below Agility\'s US$30,000 target, while the industrial ones sold (Kepler list '
                   'price about US$36,950; UBTech about US$95,500 including services) are near or above it.'},
    {'id': 'r5x:18', 'bottleneck': 'r5-B3', 'role': 'x', 'refutes': 'r5-B3', 'contrary': False, 'shows_target_reached': False,
     'source': 'Churchill Capital Corp XI and Agility Robotics, Form S-4, Agility MD&A and statements of operations',
     'version': 'filed 4 Sep 2026; the harvester\'s fetched copy, copied unchanged (SEC refused this agent\'s User-Agent)',
     'url': 'https://www.sec.gov/Archives/edgar/data/2074973/000121390026097764/ea0297114-04.htm',
     'quote': ['The increase was primarily driven by sales of Digit robots to one investor during 2025.',
               'Total net sales 1,781,967 310,301 Cost of goods sold 4,473,234 462,555 Gross loss (2,691,267'],
     'raw_file': R + 'sec_agility_s4_ea0297114-04.txt',
     'agent_note': 'Checks r5:26: total net sales $1,781,967 and cost of goods sold $4,473,234 in 2025, a ratio of 2.51 and a '
                   'gross margin of -151% (agent\'s arithmetic), as the harvester computed from rounded figures. It adds that '
                   '$1.1M of the $1.78M (about 63%) came from Digit sales to one investor, a related party; this strengthens the '
                   'harvester\'s reading that the business case is unproven.'},

    # ---------------- r5-B4: warehouse robotic stow and pick
    {'id': 'r5x:19', 'bottleneck': 'r5-B4', 'role': 'x', 'refutes': 'r5-B4', 'contrary': True, 'shows_target_reached': False,
     'source': 'Hudson et al. (Amazon Robotics), Stow: Robotic Packing of Items into Fabric Pods (Sec. IX-B, Table III)',
     'version': 'arXiv v1, 7 May 2025 (only version at fetch); re-fetched PDF byte-identical to the harvester\'s copy',
     'url': 'https://arxiv.org/abs/2505.04572v1',
     'quote': ['A Algfreq 695 307.6 (313,302) B Alglearned 227 326 (336,316) TABLE III: A/B test where we randomized the '
               'treatments over the pods that arrive to a single workcell.',
               'A/B testing, outside of the 100,000 stow attempts, was used to show that stow rates are improved by approximately '
               '7% using the learned risk models from Section VIII-B.'],
     'raw_file': R + '2505.04572v1.txt',
     'agent_note': 'Contrary on the rate part of the target, from the harvester\'s own source: in the A/B test on one workcell '
                   'the mean rate per pod was 307.6 UPH (frequentist, the algorithm used in production) and 326 UPH (learned '
                   'risk), both above the 300 UPH design rate. The harvester reported only the floor\'s monthly average (224 '
                   'UPH) and the 7% gain. The two measures differ (UPH per pod presented at one workcell against a month\'s '
                   'average across the floor), so the 300 UPH target is met on one measure and missed on the other. Not the '
                   'target reached: the design target also requires 80% of items, more than 20 h a day, no interruptions, and '
                   'the unproductive-stow aim (3%) is not met.'},
    {'id': 'r5x:20', 'bottleneck': 'r5-B4', 'role': 'x', 'refutes': 'r5-B4', 'contrary': True, 'shows_target_reached': False,
     'source': 'Hudson et al. (Amazon Robotics), Stow (Sec. IX-B stow rate)', 'version': 'arXiv v1, 7 May 2025',
     'url': 'https://arxiv.org/abs/2505.04572v1',
     'quote': ['The stow robot rate is comparable to that of a human.',
               'It is estimated that using the robot stow system to populate only top rows of pods would increase human stow rates '
               'by 4.5% overall and would avoid the use of step ladders.'],
     'raw_file': R + '2505.04572v1.txt',
     'agent_note': 'Misframing argument in part, by the operator: the authors read 224 against 243 UPH as "comparable", and they '
                   'value the robot for the rows humans do worst (top rows, ladders), where it raises total throughput. The '
                   'bottleneck as framed (robot alone against the full design target) is not the operator\'s deployment case; '
                   'the unproductive and defect rates remain the paper\'s own open targets.'},
    {'id': 'r5x:21', 'bottleneck': 'r5-B4', 'role': 'x', 'refutes': 'r5-B4', 'contrary': True, 'shows_target_reached': False,
     'source': 'Amazon Science, "How Amazon\'s Vulcan robots use touch to plan and execute motions"',
     'version': 'published 9 May 2025 (page metadata; not modified since)',
     'url': 'https://www.amazon.science/blog/how-amazons-vulcan-robots-use-touch-to-plan-and-execute-motions',
     'quote': ['The plan is for the Vulcan robots to handle the majority of stow and pick operations on the highest and lowest '
               'shelves, while humans will focus on the middle shelves and on more challenging operations involving densely '
               'packed bins or items, such as fluid containers, that require careful handling.',
               'The Vulcan pilot involved six Vulcan Stow robots in an FC in Spokane, Washington; the beta trial will involve '
               'another 30 robots in the same facility'],
     'raw_file': R + 'amazon_science_vulcan_touch.txt',
     'agent_note': 'Misframing argument: the operator\'s design target is a split of the pod between robot (top and bottom '
                   'shelves) and human (middle shelves, hard items), so the items "tagged to a human" (r5:35) are part of the '
                   'design, not only a shortfall. It also shows the scale in 2025: a pilot of six stow robots, a beta of 30.'},
    {'id': 'r5x:22', 'bottleneck': 'r5-B4', 'role': 'x', 'refutes': 'r5-B4', 'contrary': True, 'shows_target_reached': False,
     'source': 'Amazon, "Amazon robotics: Meet the robots inside fulfillment centers" (aboutamazon.com)',
     'version': 'published 9 Oct 2024, modified 4 Jun 2026 (page metadata)',
     'url': 'https://www.aboutamazon.com/news/operations/amazon-robotics-robots-fulfillment-center',
     'quote': ['Vulcan works alongside our employees, and the combination is better than either on their own.'],
     'raw_file': R + 'amazon_meet_robots.txt',
     'agent_note': 'The operator\'s 2026 framing of the same point as r5x:21. A company statement without numbers.'},

    # ---------------- r5-B5: field harvesting robots against human pickers
    {'id': 'r5x:23', 'bottleneck': 'r5-B5', 'role': 'x', 'refutes': 'r5-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'Dogtooth Technologies, home page and robots page', 'version': 'live pages fetched 2026-09-30 (footer "2025 ©")',
     'url': 'https://www.dogtooth.tech/',
     'quote': ['Our robots have been harvesting commercially on 10 customer sites over 10 seasons',
               'Our fifth generation robots are available to buy now.'],
     'raw_file': R + 'dogtooth_home.txt',
     'agent_note': 'A deployed system: selective strawberry-harvesting robots working commercially in UK and Australian table-top '
                   'crops (company statement). Contrary to "harvesting for the fresh market remains almost entirely manual" as a '
                   'general statement, though not for blueberries or apples. No rate against a human picker is given; see r5x:24.'},
    {'id': 'r5x:24', 'bottleneck': 'r5-B5', 'role': 'x', 'refutes': 'r5-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'Dogtooth Technologies, robots page', 'version': 'live page fetched 2026-09-30', 'url': 'https://dogtooth.tech/robots/',
     'quote': ['Fifth generation robots pick 200kg per day'],
     'raw_file': R + 'dogtooth_robots.txt',
     'agent_note': 'Misframing argument in part: the maker states output per day, not per minute, which credits hours a human does '
                   'not work. No human baseline on the same crop or metric is given, and the hours per day are not stated, so '
                   'no gap can be computed. Company claim.'},
    {'id': 'r5x:25', 'bottleneck': 'r5-B5', 'role': 'x', 'refutes': 'r5-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'Tevel Aerobotics Technologies, home page', 'version': 'live page fetched 2026-09-30 (no date shown)',
     'url': 'https://www.tevel-tech.com/',
     'quote': ['Our pioneering Flying Autonomous Robots™ are at the forefront of solving agricultural labor shortages.',
               'Harvest 24/7'],
     'raw_file': R + 'tevel_home.txt',
     'agent_note': 'The same reframing as r5x:24 (round-the-clock harvesting, so per-minute parity with a human is not the '
                   'binding metric) from a tree-fruit harvester that says it works in orchards in several countries. A marketing '
                   'claim without numbers.'},
    {'id': 'r5x:26', 'bottleneck': 'r5-B5', 'role': 'x', 'refutes': 'r5-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'Fieldwork Robotics, home page', 'version': 'live page fetched 2026-09-30 (no date shown)',
     'url': 'https://fieldworkrobotics.com/',
     'quote': ['Using AI-enhanced 3D cameras, sensors, and machine learning, our robots are designed to pick fruits at the same '
               'speed and quality as human pickers, ensuring efficiency and precision.'],
     'raw_file': R + 'fieldwork_home.txt',
     'agent_note': 'A maker of raspberry-harvesting robots claims its robots are designed for human speed and quality. "Designed '
                   'to" is an aim, not a measurement; the linked Fieldworker 1 announcement returned a JavaScript challenge and '
                   'was not read. Weak contrary evidence, recorded for completeness.'},
    {'id': 'r5x:27', 'bottleneck': 'r5-B5', 'role': 'x', 'refutes': 'r5-B5', 'contrary': False, 'shows_target_reached': False,
     'source': 'Xia et al., CLASP (Sec. VII firmness; Sec. VIII)',
     'version': 'arXiv v1, 16 Sep 2026 (only version); re-fetched PDF byte-identical to the harvester\'s copy',
     'url': 'https://arxiv.org/abs/2609.18051v1',
     'quote': ['the observed 15 % difference represents an upper bound on the reduction attributable to the harvesting mechanism '
               'itself.',
               'the observed reduction compares favorably with the 16 % to 26 % severe bruising rates reported for mechanical '
               'harvesters in Section I.'],
     'raw_file': R + '2609.18051v1.txt',
     'agent_note': 'Re-check of r5:45. The harvester scored firmness as a 15% gap against hand-picked fruit. The authors call '
                   '15% an upper bound, confounded by a longer interval before measurement, and favourable against mechanical '
                   'harvesters. The rate gap (58% of the human rate with manual alignment) stands.'},
    {'id': 'r5x:28', 'bottleneck': 'r5-B5', 'role': 'x', 'refutes': 'r5-B5', 'contrary': False, 'shows_target_reached': False,
     'source': 'Zhu et al., A Modular Dual-Arm Apple Harvesting Robot (Sec. 4 field results)',
     'version': 'arXiv v1, 12 Jun 2026 (only version); re-fetched PDF byte-identical to the harvester\'s copy',
     'url': 'https://arxiv.org/abs/2606.14089v1',
     'quote': ['the per-attempt metric does not credit retries, the 80.0% success rate reported here represents a conservative '
               'lower bound on the effective per-apple harvesting rate.'],
     'raw_file': R + '2606.14089v1.txt',
     'agent_note': 'Re-check of r5:46: the harvester wrote "20% of attempts fail" (true per attempt) without the authors\' '
                   'statement that 80.0% is a conservative lower bound per apple, since failed attempts can be retried. The '
                   'paper still gives no human baseline, so it remains supporting only.'},

    # ---------------- r5-B6: remote human help per robot (not shown open by the harvester)
    {'id': 'r5x:29', 'bottleneck': 'r5-B6', 'role': 'x', 'refutes': 'r5-B6', 'contrary': True, 'shows_target_reached': False,
     'source': 'Starship Technologies, press release "Autonomous Delivery Moves Into the Mainstream as Starship Technologies '
               'Passes 10 Million Deliveries"',
     'version': 'published 28 Apr 2026, modified 29 Apr 2026 (page metadata)',
     'url': 'https://www.starship.xyz/press/autonomous-delivery-moves-into-the-mainstream-as-starship-technologies-passes-10-million-deliveries/',
     'quote': ['Starship’s robots now complete over 125,000 road crossings every day (roughly two per second) operating fully '
               'autonomously at Level 4 without active human supervision, in dense urban environments and across all weather '
               'conditions.',
               'Starship’s fleet of more than 3,000 autonomous robots, operating across around'],
     'raw_file': R + 'starship_10m_deliveries.txt',
     'agent_note': 'The strongest contrary claim for sidewalk robots, newer than the harvester\'s Starship FAQ (r5:58): a fleet '
                   'of more than 3,000 robots operating at Level 4 "without active human supervision" (vendor claim). No ratio of '
                   'humans to robots and no intervention rate are given, so the claim cannot be scored; the harvester\'s "not '
                   'shown open" stands, and this vendor reads it as largely solved for its class.'},
    {'id': 'r5x:30', 'bottleneck': 'r5-B6', 'role': 'x', 'refutes': 'r5-B6', 'contrary': True, 'shows_target_reached': False,
     'source': 'Serve Robotics Inc., Form 10-K for FY2025, Business (Level 4 Autonomy)',
     'version': 'signed 12 Mar 2026 (accession 0001832483-26-000010); the harvester\'s fetched copy, copied unchanged (SEC refused '
                'this agent\'s User-Agent)',
     'url': 'https://www.sec.gov/Archives/edgar/data/1832483/000183248326000010/patr-20251231.htm',
     'quote': ['Specifically, our robots are capable of driving autonomously in certain environments without a remote human '
               'supervisor having to oversee their movement.',
               'because it enables a single remote supervisor to oversee multiple deliveries simultaneously.'],
     'raw_file': R + 'sec_serve_10k_fy2025.txt',
     'agent_note': 'In the harvester\'s own raw file but not quoted: Serve states Level 4 operation in certain environments and '
                   'one supervisor overseeing several deliveries. The same filing says robots still need remote supervision at '
                   'times (r5:52) and ties growth to an unstated human-to-robot ratio (r5:59), so both sides are in one document.'},
    {'id': 'r5x:31', 'bottleneck': 'r5-B6', 'role': 'x', 'refutes': 'r5-B6', 'contrary': True, 'shows_target_reached': False,
     'source': 'Brett Adcock (Figure AI CEO), post on X', 'version': 'dated 14 May 2026 (publish.twitter.com oEmbed)',
     'url': 'https://x.com/adcock_brett/status/2054729581391962353',
     'quote': ['Figure just live-streamed 8 hours of fully autonomous, unsupervised work'],
     'raw_file': R + 'x_adcock_2054729581391962353.txt',
     'agent_note': 'For humanoids: a public demonstration of unsupervised work (later 200 h, r5x:8), against the S-4\'s claim '
                   '(r5:49) that many humanoid makers rely on teleoperation. A demonstration, not a deployment; no ratio.'},
    {'id': 'r5x:32', 'bottleneck': 'r5-B6', 'role': 'x', 'refutes': 'r5-B6', 'contrary': False, 'shows_target_reached': False,
     'source': 'UBTECH Robotics, Interim results announcement for the six months ended June 30, 2026 (Business Review)',
     'version': 'dated 28 Aug 2026', 'url': 'https://owebsite-cdn.ubtrobot.com/resources/file/2026/09/02/844614814105669.pdf',
     'quote': ['covering demand assessment, solution design, teleoperation validation, data acquisition and model training',
               'We have also explored the combined application of teleoperation, VLA, end-to-end and other technical solutions '
               'based on the characteristics of different industrial tasks.'],
     'raw_file': R + 'ubtech_interim_results_2026H1.txt',
     'agent_note': 'Supports the harvester for humanoids: a leading industrial-humanoid maker builds teleoperation into its '
                   'deployment pipeline in 2026.'},
    {'id': 'r5x:33', 'bottleneck': 'r5-B6', 'role': 'x', 'refutes': 'r5-B6', 'contrary': False, 'shows_target_reached': False,
     'source': 'Federal Register API: FAA documents matching "Beyond Visual Line of Sight" published since 1 Aug 2025',
     'version': 'API response fetched 2026-09-30 (9 documents)',
     'url': 'https://www.federalregister.gov/api/v1/documents.json?conditions%5Bterm%5D=%22Beyond+Visual+Line+of+Sight%22&conditions%5Bagencies%5D%5B%5D=federal-aviation-administration&conditions%5Bpublication_date%5D%5Bgte%5D=2025-08-01&order=newest&per_page=40',
     'quote': ['2026-01-28 | Proposed Rule | 2026-01644 | Normalizing Unmanned Aircraft Systems Beyond Visual Line of Sight '
               'Operations; Reopening of Comment Period',
               '2026-02-10 | Proposed Rule | 2026-02649 | Normalizing Unmanned Aircraft Systems Beyond Visual Line of Sight '
               'Operations; Reopening of Comment Period; Denial of Extension'],
     'raw_file': R + 'fedreg_bvlos_since_2025-08.txt',
     'agent_note': 'Confirms the harvester: no final Part 108 rule has been published; the latest documents reopen the NPRM\'s '
                   'comment period (Jan-Feb 2026). The proposed 1:1 default (r5:51) is still a proposal, and no numeric 1:many '
                   'target has been set.'},

    # ---------------- r5-B7: delivery-drone collisions (not shown open by the harvester)
    {'id': 'r5x:34', 'bottleneck': 'r5-B7', 'role': 'x', 'refutes': 'r5-B7', 'contrary': True, 'shows_target_reached': False,
     'source': 'Zipline, "Safety Facts" (Zipline safety fact sheet)', 'version': 'published 6 Nov 2025 (page date)',
     'url': 'https://www.zipline.com/about/zipline-safety-fact-sheet',
     'quote': ['Flown more than 135 million commercial autonomous miles since we started, the same as driving on every road in '
               'America more than 32 times, without injury.',
               'Each aircraft has a Detect-and-Avoid system onboard to avoid other aircraft.'],
     'raw_file': R + 'zipline_safety_fact_sheet.txt',
     'agent_note': 'Misframing argument: incidents should be read against exposure. Zipline, which describes itself as operating '
                   'the world\'s largest autonomous delivery system, claims 135 million autonomous miles without injury (a '
                   'company claim; collisions with property or obstacles are not counted in it). '
                   'The NTSB reports the harvester cited are single events without a denominator, so they do not establish a '
                   'rate either way.'},
    {'id': 'r5x:35', 'bottleneck': 'r5-B7', 'role': 'x', 'refutes': 'r5-B7', 'contrary': True, 'shows_target_reached': False,
     'source': 'Wing, "Safety" page (wing.com/safety)', 'version': 'live page fetched 2026-09-30 (no date shown)',
     'url': 'https://wing.com/safety',
     'quote': ['One of our safety objectives is to maintain a lower risk to the public than conventional ground transportation.',
               'To date, Wing has safely completed well over one million on-demand deliveries.'],
     'raw_file': R + 'wing_safety.txt',
     'agent_note': 'The same framing as r5x:34 from a second operator (Alphabet\'s Wing): a comparative risk target (lower than '
                   'ground transport) and a record of over a million deliveries, without an incident rate. Company claims.'},

    # ---------------- r5-B8: cost of collecting robot training data (not shown open by the harvester)
    {'id': 'r5x:36', 'bottleneck': 'r5-B8', 'role': 'x', 'refutes': 'r5-B8', 'contrary': True, 'shows_target_reached': False,
     'source': 'Generalist AI, "GEN-0: Embodied Foundation Models That Scale with Physical Interaction" (company blog)',
     'version': 'published 4 Nov 2025 (page date)', 'url': 'https://generalistai.com/blog/gen-0',
     'quote': ['is pretrained on our in-house robotics dataset, which includes over 270,000 hours of real-world diverse '
               'manipulation data, growing at a rate of 10,000 hours a week and accelerating.',
               'This is all powered by a global network of hardware and 1,000s of data collection devices and robots.'],
     'raw_file': R + 'generalist_gen-0.txt',
     'agent_note': 'Contrary on scale: one company\'s private corpus (270,000 h in Nov 2025) is about 13x the whole public '
                   'supply HumanScale counts (about 2 x 10^4 h, r5:68), and it grew by 10,000 h a week. No cost per hour is given. '
                   'HumanScale\'s figure is about public data and stays correct as stated.'},
    {'id': 'r5x:37', 'bottleneck': 'r5-B8', 'role': 'x', 'refutes': 'r5-B8', 'contrary': True, 'shows_target_reached': False,
     'source': 'Generalist AI, "GEN-1: Scaling Embodied Foundation Models to Mastery" (company blog)',
     'version': 'published 2 Apr 2026 (page date)', 'url': 'https://generalistai.com/blog/gen-1',
     'quote': ['Previous general models in robotics that surpass 90% success have depended on enormous teleoperation datasets that '
               'are expensive and difficult to scale.',
               'the base foundation model is trained without any robot data—it instead uses data from low-cost wearable devices '
               'on humans doing millions of activities, and provides an existence proof that this pretraining can lead to high '
               'levels of mastery without requiring large teleoperation or simulation datasets.',
               'on our dataset of now half a million hours of real-world data.'],
     'raw_file': R + 'generalist_gen-1.txt',
     'agent_note': 'Misframing argument: the cost of teleoperated data (the harvester\'s B-a, B-b) binds only if teleoperation is '
                   'the data source; this company states it pretrains without robot data, from low-cost wearables on humans, and '
                   'reports half a million hours. It concedes the premise ("expensive and difficult to scale") for teleoperation. '
                   'A company claim; no cost figure.'},
    {'id': 'r5x:38', 'bottleneck': 'r5-B8', 'role': 'x', 'refutes': 'r5-B8', 'contrary': True, 'shows_target_reached': False,
     'source': 'Figure AI, "Introducing Index: Building The World\'s Largest and Most Diverse Physical Dataset"',
     'version': 'published 25 Aug 2026 (page date)', 'url': 'https://www.figure.ai/news/introducing-index',
     'quote': ['The app is processing 30 minutes of video uploads every second; 4.9 years of human work every day uploaded',
               'Prior to this we tried buying data. Vendors couldn\'t hit the throughput, diversity, or quality bar Helix requires, '
               'so we built the pipeline ourselves',
               'We are now on a path to 100x, and are committed to spend over $1B the next 12 months on data and compute'],
     'raw_file': R + 'figure_introducing-index.txt',
     'agent_note': 'Both sides in one source. Contrary: human video is collected at about 43,000 h a day (4.9 years x 8,760 h; '
                   'agent\'s arithmetic), from paid contributors rather than teleoperation, and Helix 2.5 was pretrained on it '
                   '(Figure, 17 Sep 2026). Supporting: the company says vendors could not supply the data and commits over $1B in '
                   'a year to data and compute, so data remains a large cost. No cost per hour is stated.'},
]

CHECKS = [
    {'bottleneck': 'r5-B1',
     'searched': ['WebSearch: humanoid robot autonomous battery swap continuous operation 2026 Atlas Boston Dynamics Hyundai factory',
                  'WebSearch: humanoid robot 8-hour battery life full shift specification 2026 official',
                  'WebSearch: Figure 03 Helix continuous operation hours uninterrupted logistics 2026 figure.ai',
                  'WebSearch: Kepler K2 Bumblebee humanoid 8 hours battery; prnewswire Kepler K2 mass production 8 hours battery 2025',
                  'Fetched: figure.ai/news index and posts (F.03 battery development, Helix 2.5, Ramping Figure 03 Production); '
                  'X posts of Figure\'s CEO (oEmbed); YouTube oEmbed of the F.03 livestream',
                  'Fetched: Kepler K2 press releases (PR Newswire, Aug and Sep 2025); UBTECH 2026 interim results (company CDN)',
                  'Tried: bostondynamics.com Atlas product page and CES 2026 blog post, hyundainews.com release 4664 (JavaScript '
                  'challenge or empty shell; not readable, not used); automate.org (HTTP 403)',
                  'Re-read: Agility S-4 Digit v4/v5 descriptions in the harvester\'s copy'],
     'finding': 'CONTESTED, not NOT OPEN. Per cycle, a humanoid in mass production (Kepler K2, shipping since Sep 2025) is '
                'specified at up to 8 h per charge and ran an 8-hour exhibition livestream on one charge, and Figure 03 is specified '
                'at 5 h; both exceed the harvester\'s "best deployed 4 h", but neither reaches the 10-hour BMW shift, and both are '
                'makers\' specifications. At the day level, Figure\'s CEO reports a humanoid package-sorting cell running non-stop '
                'for about 200 hours at Figure\'s site (more than one robot, since one is specified at 5 h a charge), and UBTech '
                'claims 24-hour operation by '
                'swapping; neither gives productive hours per robot at a customer. Boston Dynamics\' Atlas (4 h, autonomous swap) '
                'was seen only in press and could not be read at the source.',
     'harvester_errors': ['B-c "best deployed runtime per charge: up to 4 h" is not the best reported: Figure 03 (delivered in the '
                          'hundreds by Apr 2026, at BMW from Jun 2026) is specified at 5 h, and Kepler\'s K2 (in mass production, '
                          'shipping) at up to 8 h per charge; the per-cycle gap to a 10-hour shift is 20-50% on company specs, '
                          'not 60%.',
                          'r5:5: the harvester quoted Agility\'s press release ("more than 20 hours ... in a 24-hour day") and wrote '
                          '"at least 83%"; Agility\'s SEC filing of 4 Sep 2026 says "Approximately 20 hours of operation within a '
                          '24-hour period", so about 83% is what the company states under securities law.']},
    {'bottleneck': 'r5-B2',
     'searched': ['WebSearch: humanoid robot deployment 2026 success rate 99% interventions per shift production line results '
                  'company announcement',
                  'WebSearch: Agility Robotics GXO Digit 2026 uptime interventions "per shift" OR "99%" results',
                  'WebSearch: AgiBot G2 Longcheer production line 99.9% success rate continuous hours; the release title on '
                  'prnewswire',
                  'WebSearch: Brett Adcock livestream F.03 packages hours zero failures (pointer to the CEO\'s X posts)',
                  'Fetched: AgiBot-Longcheer release (PR Newswire, agibot.com, roboticstomorrow.com copy), AgiBot 15,000th-robot '
                  'release; Figure CEO posts via oEmbed; Figure BMW page (re-fetched) and Ramping page; UBTECH 2026 interim results',
                  'Screened: press summaries claiming Figure "hit >99% placement success per shift" at BMW; the Figure BMW page '
                  'states >99% as the target and reports no achieved value, so the press claim was not used'],
     'finding': 'CONTESTED, not NOT OPEN. AgiBot and its customer Longcheer claim over 99.9% success "in continuous operation" '
                'on a tablet mass-production line with 24/7 operation, "minimal human intervention" and downtime below 4% (Apr '
                '2026), above the >99% per-shift success target; Figure\'s CEO claims 200 hours "without a failure" in a public '
                'package-sorting livestream (May 2026). Neither reaches both halves of the target (>99% per shift AND zero '
                'interventions) in one verified statement: AgiBot\'s interventions are "minimal", Figure gives no success rate and '
                'ran at its own site. All are company claims without counts. The IFR (Sep 2026) still says reliability is unproven, '
                'and UBTech describes its industrial work as solution validation.',
     'harvester_errors': ['B-c "best: about 98% operational accuracy ... interventions per shift not disclosed by any source" '
                          'omits AgiBot/Longcheer\'s claimed >99.9% success on a production line (15 Apr 2026) and Figure\'s CEO\'s '
                          'claim of 200 hours without a failure (22 May 2026); the gap "failure share ~2% against <1%" is not '
                          'computed from the best reported value.',
                          'r5:15 quotes the forearm as the "top hardware failure point" but not the preceding sentence on the same '
                          'page, "Across 1,250+ operational hours, Figure 02 recorded minimal hardware failures"; one-sided '
                          'selection (minor).']},
    {'bottleneck': 'r5-B3',
     'searched': ['WebSearch: UBTECH interim results 2026 humanoid Walker S2 revenue gross margin orders; hkexnews 9880 interim '
                  'results 2026 pdf',
                  'WebSearch: prnewswire Kepler Robotics K2 mass production (price)',
                  'Fetched: UBTECH 2026 interim results (company announcements page and CDN); Kepler K2 mass-production release; '
                  'Figure Ramping and battery pages; Federal Reserve H.10 (exchange rate)',
                  'Re-read: Unitree SSE reply (re-fetched, byte-identical) for 2025 profit and orders; Agility S-4 statements of '
                  'operations (harvester\'s copy)'],
     'finding': 'CONTESTED, not NOT OPEN. On cost and price, makers other than Agility are near or below Agility\'s own targets: '
                'Unitree\'s humanoid cost of sales is about US$9,260 per unit and the company expects a 2025 net profit of RMB '
                '600M; Kepler lists an industrial humanoid at RMB 248,000 (about US$36,950); UBTech sold 921 full-size humanoids in '
                'H1 2026 at a higher-than-average margin (conversions at the 25 Sep 2026 H.10 rate, indicative). The productive-work '
                'business case is not shown by any source: Unitree\'s buyers are mostly research and education, UBTech still lost '
                'RMB 338.8M in the half and its industrial work is at solution validation, Kepler\'s orders are framework '
                'agreements, Agility\'s 2025 sales were 63% to one investor, and the IFR (Sep 2026) says the business case is lacking.',
     'harvester_errors': ['The problem statement "Industrial humanoids cost several times their makers\' own volume targets" '
                          'generalises from one maker\'s filing (Agility); an industrial humanoid in mass production (Kepler K2) '
                          'lists at RMB 248,000, about US$36,950 at the Fed H.10 rate, near Agility\'s US$30,000 BOM target; the '
                          'harvester made no currency conversions, so this comparison was not visible.']},
    {'bottleneck': 'r5-B4',
     'searched': ['WebSearch: Amazon Vulcan 2026 update deployed fulfillment centers stowed picked million items robotic stow rate',
                  'WebSearch: arXiv 2025 2026 robotic picking warehouse production deployment pick success rate 99% picks per '
                  'hour each picking real-world fleet (pointers: Amazon Robin and multi-suction picking papers; package '
                  'singulation, not pod stow)',
                  'Fetched: Amazon Science Vulcan blog (May 2025); aboutamazon "Meet the robots" (modified Jun 2026); the Stow paper '
                  're-fetched (byte-identical) and its abs page (still v1)',
                  'Re-read in full: the Stow paper Sec. IX (Table II, Table III, stow rate, amnesty)'],
     'finding': 'CONTESTED, not NOT OPEN. The harvester\'s own source reports, in an A/B test on one workcell, 307.6 UPH '
                '(the production algorithm) and 326 UPH (learned risk) per pod, above the 300 UPH design rate; the floor\'s '
                'monthly average (224 UPH) is a different measure and stays below it. The operator also frames the target '
                'differently: robots take the top and bottom shelves and humans the middle and hard items ("the combination is '
                'better than either on their own"), so items handed to humans are partly by design. The unproductive-stow aim (3% '
                'against 9.31%), the 80% item coverage and the 20 h/day requirement are not shown met by any source; Vulcan was at '
                '6 robots (pilot) and 30 (beta) in 2025.',
     'harvester_errors': ['B-c reports 224 UPH (monthly floor average) and "74.7% of the design rate" but omits Table III of the '
                          'same paper: 307.6 and 326 UPH per pod on a single workcell, above the 300 UPH design target; the note '
                          'mentions only the 7% relative gain.',
                          'The problem statement ("covers most but not all item types; the rest goes to humans") omits that the '
                          'operator designs the split: the paper values robot stowing of the top rows (+4.5% human stow rate, no '
                          'ladders) and Amazon plans robots for the highest and lowest shelves with humans on the middle ones.']},
    {'bottleneck': 'r5-B5',
     'searched': ['WebSearch (not run, budget exhausted): arXiv 2026 harvesting robot field trial speed vs human; commercial '
                  'robotic harvesting 2026 deployed rate per hour',
                  'arXiv API (export.arxiv.org): harvesting AND robot AND human/manual AND picker/labor; harvesting AND robot AND '
                  'field AND throughput; harvesting AND robot AND commercial; strawberry AND harvesting AND robot (2025-26 hits '
                  'screened by abstract: 2603.13987 VADER bell pepper >60% success, <100 s per fruit; 2605.23863 strawberry 84.3% '
                  'overall in greenhouse; 2607.14708 strawberry 82.0% real-world; none compares with a human picker)',
                  'Fetched company pages: Tevel, Dogtooth (home, robots, products), Fieldwork Robotics (home; the Fieldworker 1 '
                  'announcement returned a JavaScript challenge), Harvest CROO, Four Growers (no rate text); Advanced Farm '
                  '(connection reset)',
                  'Re-read: CLASP and the apple paper (both re-fetched, byte-identical) for caveats'],
     'finding': 'CONTESTED, not NOT OPEN. Commercial selective harvesters exist (Dogtooth: strawberries on 10 customer sites over '
                '10 seasons, 200 kg per day; Tevel: tree fruit in several countries), and makers reframe the metric as output per '
                'day with round-the-clock work; Fieldwork says its robots are designed for human speed. No source reports a '
                'robot rate at or above a human picker\'s on the same crop and metric; the 2025-26 arXiv field results found '
                'report 60-92% success and multi-second cycles without human baselines. The CLASP rate gap (58% of the human '
                'rate) stands; its firmness gap is an upper bound per its authors.',
     'harvester_errors': ['r5:45 and the BOTTLENECKS target use hand-picked firmness (195.59 g/mm) as a target and report a 15% '
                          'shortfall; the authors state that 15% is an upper bound confounded by a longer interval before '
                          'measurement and compares favourably with 16-26% severe bruising for mechanical harvesters.',
                          'r5:46 "20% of attempts fail" omits the authors\' statement that the 80.0% per-attempt success is a '
                          'conservative lower bound per apple (retries not credited); minor.']},
    {'bottleneck': 'r5-B6',
     'searched': ['Fetched: Starship press releases of 28 Apr 2026 (10 million deliveries) and 4 Jun 2026 (grocery focus), found '
                  'from the harvester\'s pointer page; UBTECH 2026 interim results; Figure CEO posts (oEmbed)',
                  'Federal Register API: FAA documents on "Beyond Visual Line of Sight" since 1 Aug 2025 (no final Part 108 rule; '
                  'comment period reopened Jan-Feb 2026)',
                  'Re-read: Serve 10-K (harvester\'s copy) for Level 4 statements; Waymo and Markey figures in the harvester\'s files'],
     'finding': 'Not shown open, as the harvester found; vendors claim it largely solved for their own classes. Starship (Apr 2026) '
                'says its 3,000+ robots cross roads at Level 4 "without active human supervision"; Serve\'s 10-K says Level 4 in '
                'certain environments lets one supervisor oversee several deliveries; Figure\'s CEO reports unsupervised humanoid '
                'work in a demonstration. No source gives a humans-to-robots ratio against a target or an intervention rate for '
                'sidewalk robots or humanoids; UBTech builds teleoperation into its 2026 deployment pipeline; the FAA\'s 1:1 default '
                'is still a proposal.',
     'harvester_errors': []},
    {'bottleneck': 'r5-B7',
     'searched': ['Fetched: Zipline safety page and safety fact sheet (6 Nov 2025); Zipline home; Wing safety page',
                  'Checked: the harvester\'s NTSB reports are still the current versions it fetched (preliminary for the Oct 2025 '
                  'crane strikes)'],
     'finding': 'Not shown open, as the harvester found; the operators frame it as a rate problem they meet: Zipline claims 135 '
                'million autonomous miles without injury and compares that exposure with road crashes; Wing states a target of '
                'lower public risk than ground transport and over a million deliveries. Neither gives a collision rate with '
                'obstacles or aircraft, so neither answers the incident record the harvester cited; no target exists to score.',
     'harvester_errors': []},
    {'bottleneck': 'r5-B8',
     'searched': ['Fetched: Generalist AI blog index and posts GEN-0 (Nov 2025), GEN-1 (Apr 2026), GEN-1.5 (Aug 2026), "Towards '
                  'Machines with a Thousand Hands" (Jul 2026); Figure "Introducing Index" (Aug 2026) and Helix 2.5 (Sep 2026)',
                  'Screened: vendor blogs on teleoperation cost per hour (not primary, not fetched), as the harvester did'],
     'finding': 'Not shown open, as the harvester found, and partly misframed: companies now collect manipulation data at scales '
                'far above the public supply HumanScale counts (Generalist: 270,000 h in Nov 2025, over half a million by 2026, '
                '10,000 h a week; Figure Index: about 43,000 h of human video a day) and pretrain without teleoperation (low-cost '
                'wearables, phone video). Cost remains large (Figure commits over $1B in a year to data and compute; Generalist '
                'says teleoperation data is expensive), and no source gives a cost per hour against a target.',
     'harvester_errors': ['B-c/best "about 2 x 10^4 public robot hours in aggregate" is correct as HumanScale\'s count of public '
                          'data, but the harvester did not record that single companies report private corpora an order of '
                          'magnitude larger (270,000-500,000+ h), which bears on whether the data volume is the binding '
                          'constraint; an omission, not a misquote.']},
]
