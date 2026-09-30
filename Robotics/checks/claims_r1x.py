"""ROB1 stage 1b, family R1 (Robotics/DECLARATION.md): the double check of the programme bottlenecks r1-B1 ... r1-B7.

Written by a second agent that did not harvest family R1. For every bottleneck in `claims_r1.BOTTLENECKS` it searched
independently (different queries and sources from the harvester's; log in /tmp/claude-0/rob_src/r1x/search/queries.txt)
for the strongest contrary evidence: a 2025-26 source reporting the target reached on the named metric, a deployed system
that does it, or a source arguing that the bottleneck is misframed. It also re-read the harvester's quotes and numbers
against the harvester's raw texts (/tmp/claude-0/rob_src/r1/txt/); a scratch copy of Open_Bottlenecks/checks/verify.py
pointed at claims_r1.py read "quotes found verbatim: 114 of 114 (claims 49; raw files 26, missing 0)".

Every source was fetched on 2026-09-30 through the session proxy with curl (TLS verification on). Text was extracted with
the harvester's own extractors (copied to r1x/): PDFs by pymupdf (`page.get_text()`, pages joined by newlines); HTML by
BeautifulSoup 4 (`get_text('\n')` after removing script/style/noscript/svg, runs of spaces and blank lines collapsed); the
two Markdown READMEs are used as fetched. Raw files live outside the repository under /tmp/claude-0/rob_src/ (`raw_file`
is relative to that root; the fetched originals are in r1x/src/); their sha256 is in /tmp/claude-0/rob_src/r1x/SHA256SUMS.txt
and in the dossier docs/citations/rob1_r1_2026-09-30.md (section "Stage 1b double check"). Four re-fetched files (the
Robothon README, the ARIA EAP call, the DARPA Lift page, the DARPA SubT page) are byte-identical to the harvester's copies.

Fields. role = 'x' (a double-check claim). `refutes` = the bottleneck the claim bears on. `contrary` = True when the claim
is contrary evidence (the target reached, a deployed system that does it, or a misframing argument); False when it is a
re-check of the harvester's reading (a number or a target the harvester got wrong or overstated), which bears on the
bottleneck's B-c but is not evidence that the bottleneck is closed. `shows_target_reached` = True only if the verified
quote shows the target reached on the named metric of that bottleneck. `agent_note` is the double-checker's reading, fair
to both sides; it is not the source's words. Company statements and trade press are recorded as such.

CHECKS: one entry per bottleneck: what was searched, what was found, and `harvester_errors` (quotes or numbers the
harvester got wrong or overstated; an empty list when none was found).
"""

R = 'r1x/txt/'

CLAIMS = [
    # ---------------- r1-B1: dexterous manipulation, speed and generality against a human
    {'id': 'r1x:1', 'bottleneck': 'r1-B1', 'role': 'x', 'refutes': 'r1-B1', 'contrary': True, 'shows_target_reached': False,
     'source': 'Rivière & Denain (Epoch AI), Where Autonomy Works: Evaluating Robot Capabilities in 2026 (report, key takeaways)',
     'version': 'published 10 Feb 2026 (no later update shown; fetched 2026-09-30)',
     'url': 'https://epoch.ai/publications/where-autonomy-works-evaluating-robot-capabilities-in-2026',
     'quote': ['Speed is not solved, but is not the main bottleneck to deployment.',
               'Robots are typically 3–10× slower than humans. But a robot working 20 hours a day compensates for being slower '
               'per task',
               'This is the main bottleneck: most demonstrations show robots fine-tuned on specific tasks in specific settings.'],
     'raw_file': R + 'epoch_where_autonomy_works_2026.txt',
     'agent_note': 'A 2026 independent assessment arguing the speed framing is partly misframed: speed is "not the main '
                   'bottleneck to deployment" (duty cycle compensates) and transfer is. It does not show the target reached: it '
                   'confirms robots are 3-10x slower than humans, consistent with the harvester\'s 6.4x on the Robothon board. '
                   'The generality half of r1-B1 is supported, not contested, by this source.'},
    {'id': 'r1x:2', 'bottleneck': 'r1-B1', 'role': 'x', 'refutes': 'r1-B1', 'contrary': True, 'shows_target_reached': False,
     'source': 'Rivière & Denain (Epoch AI), Where Autonomy Works (task sections: pick and place; connector insertion; packages)',
     'version': 'published 10 Feb 2026',
     'url': 'https://epoch.ai/publications/where-autonomy-works-evaluating-robot-capabilities-in-2026',
     'quote': ['Vulcan’s speed is close to human on each operation, which means faster over longer periods since the robot does '
               'not need breaks.',
               'CATL has deployed humanoid robots to insert connectors into battery packs, claiming 99% reliability and human speed.',
               'Speed remains far from human: over the hour-long demo, the robot was roughly four times slower than an average '
               'worker.'],
     'raw_file': R + 'epoch_where_autonomy_works_2026.txt',
     'agent_note': 'Deployed systems at about human speed exist in 2025-26, but each on one narrow, engineered task (Amazon '
                   'stowing in fixed pods; CATL connector insertion, a company claim relayed by Epoch). The same report finds a '
                   'general humanoid package-handling demo 4x slower than a worker. Contests "cannot achieve the speed of human '
                   'manipulation" for single deployed tasks; does not reach human speed across a varied protocol, which is the '
                   'named metric (the Robothon task board).'},
    {'id': 'r1x:3', 'bottleneck': 'r1-B1', 'role': 'x', 'refutes': 'r1-B1', 'contrary': True, 'shows_target_reached': False,
     'source': 'Amazon (company statement), Introducing Vulcan: Amazon\'s first robot with a sense of touch (A. Davies)',
     'version': 'published 7 May 2025, modified 4 Jun 2026 (page metadata)',
     'url': 'https://www.aboutamazon.com/news/operations/amazon-vulcan-robot-pick-stow-touch',
     'quote': ['With the ability to pick and stow approximately 75% of all various types of items we store at our fulfillment '
               'centers, and at speeds comparable to that our front-line employees, Vulcan represents a step change in how '
               'automation and AI can assist our employees in their everyday tasks.',
               'It also has the smarts to identify when it can’t move a specific item, and can ask a human partner to tag in'],
     'raw_file': R + 'aboutamazon_vulcan.txt',
     'agent_note': 'Primary company statement behind r1x:2: a deployed manipulator at human-comparable speed on stow/pick, on '
                   'about 75% of items, with a human fallback for the rest. It is one task in one engineered setting, with no '
                   'timed human baseline published, so it contests the speed claim for that task only; the named metric is not '
                   'reached.'},
    {'id': 'r1x:4', 'bottleneck': 'r1-B1', 'role': 'x', 'refutes': 'r1-B1', 'contrary': True, 'shows_target_reached': False,
     'source': 'Lei, Li et al., RL-100: Performant Robotic Manipulation with Real-World Reinforcement Learning (abstract)',
     'version': 'arXiv v4, 10 Mar 2026 (v1 16 Oct 2025, v2 3 Nov 2025, v3 19 Nov 2025)', 'url': 'https://arxiv.org/abs/2510.14830v4',
     'quote': ['RL-100 attains 100 percent success across evaluated trials, for a total of 1000 out of 1000 episodes, including '
               'up to 250 out of 250 consecutive trials on one task.',
               'It matches or surpasses expert teleoperators in time to completion.',
               'our juicing robot served random customers continuously for about seven hours without failure when deployed '
               'zero-shot in a shopping mall.'],
     'raw_file': R + 'arxiv_2510.14830_abs.txt',
     'agent_note': 'Learned policies at or above the speed of expert teleoperators on eight trained tasks, with long failure-free '
                   'runs. The baseline is a human teleoperating the robot, not a human hand, and each task is trained, so this '
                   'is not the human-hand baseline of r1-B1 (a teleoperator is itself much slower than a bare human hand). '
                   'Contrary on reliability, not on the named speed metric.'},
    {'id': 'r1x:5', 'bottleneck': 'r1-B1', 'role': 'x', 'refutes': 'r1-B1', 'contrary': False, 'shows_target_reached': False,
     'source': 'Robothon Grand Challenge results repository (organiser P. So), README, Robothon 2022 section',
     'version': 'GitHub peterso/robothon-grand-challenge, main branch, re-fetched raw 2026-09-30 (byte-identical to the '
                'harvester\'s copy); the 2022 scorecard PDF (created 15 Jan 2024) is image-only and was read by eye',
     'url': 'https://github.com/peterso/robothon-grand-challenge',
     'quote': ['TBv2022 "Rigid Design" [Protocol](/Assets/TBv2021_Test_Protocol.pdf)',
               '25 Applications, 20 Selected Teams, 6 Finishers, Best Time 31 seconds.',
               '| 3 | RoboTechX MDX | AE | 190 | 31 |'],
     'raw_file': R + 'github_robothon-grand-challenge_README.txt',
     'agent_note': 'Re-check of the harvester\'s B-c. The organiser\'s own record gives a 31 s best full trial in 2022 (RoboTechX '
                   'MDX; the image-only scorecard ticks all six tasks T1-T6 for this team) on the 2021 six-task protocol that '
                   'DR.J Table 6 also covers, where the harvester used DR.J\'s 52 s. On 31 s the robot runs at 8.1/31 = 0.26 of '
                   'the best human (3.8x slower, not 6.4x) and is still 1.6x slower than the human mean 18.9 s. The two records '
                   'from the same organiser disagree (board-measured vs submitted time is a guess, not checked; the team\'s repo '
                   'README was 404). The gap narrows but stays open.'},

    # ---------------- r1-B2: legged locomotion range, endurance and robustness outside prepared ground
    {'id': 'r1x:6', 'bottleneck': 'r1-B2', 'role': 'x', 'refutes': 'r1-B2', 'contrary': True, 'shows_target_reached': True,
     'source': 'Lee, Youm, Park, ... Hwangbo (KAIST), A quadruped robot designed to complete a marathon on a single battery '
               'charge, Nature (abstract and article metadata)',
     'version': 'Nature, published 23 Sep 2026 (received 16 Feb 2025, accepted 28 Aug 2026), doi 10.1038/s41586-026-11102-5; '
                'abstract reachable, full text behind the subscription wall',
     'url': 'https://www.nature.com/articles/s41586-026-11102-5',
     'quote': ['However, practical deployment is hindered by the limited travel range per battery charge',
               'RAIBO2 completed a full marathon in 4 hours, 19 minutes and 52 seconds on a single battery charge',
               'achieving a total cost of transport of 0.25: surpassing the human benchmark of 0.37.',
               'Compared with existing quadrupeds, RAIBO2 offers more than three times the travel range per battery charge.'],
     'raw_file': R + 'nature_raibo2_s41586-026-11102-5.txt',
     'agent_note': 'The strongest contrary evidence found. On one of r1-B2\'s two named metrics, cost of transport, the target '
                   'is reached: 0.25 is inside the human range 0.2-0.47 that the harvester set as the target, below the paper\'s '
                   'human benchmark 0.37, and far below the harvester\'s "best robot 0.52". It is a peer-reviewed 2026 paper, on a '
                   'public marathon course. The other named metric, range on one charge, is NOT reached: 42.195 km is below '
                   'Ranger\'s 65 km and far below the "hundreds of kilometers" of the human baseline. So r1-B2 is reached on CoT and open on range; the text of '
                   'the Nature abstract itself still names limited range per charge as the obstacle for quadrupeds in general.'},
    {'id': 'r1x:7', 'bottleneck': 'r1-B2', 'role': 'x', 'refutes': 'r1-B2', 'contrary': True, 'shows_target_reached': False,
     'source': 'KAIST PR Office, KAIST\'s RAIBO2 becomes the World\'s First Robo-dog to Successfully Complete a Full-course Marathon',
     'version': 'press release dated 17 Nov 2024 (fetched 2026-09-30)',
     'url': 'https://news.kaist.ac.kr/newsen/html/news/?mode=V&mng_no=41590',
     'quote': ['completed the full-course race (42.195 km) with a time of 4 hours 19 minutes and 52 seconds.',
               'is known for its challenging course featuring two 50 m elevation climbs, each at the 14 km and 28 km marks',
               'In follow-up research, we will add autonomous navigation functions to RAIBO'],
     'raw_file': R + 'kaist_news_41590.txt',
     'agent_note': 'Primary institutional statement for the event behind r1x:6: more than four hours in an official road race '
                   'among runners, with climbs, i.e. outside a lab or warehouse floor. Contests "cannot yet operate reliably for '
                   'long periods beyond controlled environments" for one paved course. Fair to the harvester: it is paved road '
                   'not rough terrain, no load was carried, and the release says autonomous navigation is still to be added.'},
    {'id': 'r1x:8', 'bottleneck': 'r1-B2', 'role': 'x', 'refutes': 'r1-B2', 'contrary': True, 'shows_target_reached': False,
     'source': 'Cornell Chronicle, Robot walks a 40.5-mile ultramarathon without recharge (Cornell Ranger)',
     'version': 'published 10 May 2011', 'url': 'https://news.cornell.edu/stories/2011/05/ranger-robot-walks-marathon-and-then-some',
     'quote': ['At 16 watts total, the specific cost of transport (COT, energy per unit weight per unit distance) was a relatively '
               'stingy 0.28 joules per newton-meter.',
               'Ranger still isn\'t as efficient as a typical human, who walks with a COT of about 0.2.',
               'with students, faculty and staff taking shifts to steer.'],
     'raw_file': R + 'cornell_ranger_2011.txt',
     'agent_note': 'Re-check of the harvester\'s "best robot CoT 0.52 (MIT Cheetah)". Riener et al.\'s "closest of all robots" '
                   'covers only the robots in their table; Ranger, the robot the harvester cites for range, had a CoT of 0.28 '
                   'in 2011, already inside the human range 0.2-0.47. By the source\'s own comparison (a walking human at 0.2) '
                   'it had not reached the human, so shows_target_reached is False, but the harvester\'s CoT gap "1.1x-2.6x" '
                   'was wrong long before 2026 (0.28 is 0.6x-1.4x of the range ends). Old source (2011), used only to test the '
                   'harvester\'s number.'},
    {'id': 'r1x:9', 'bottleneck': 'r1-B2', 'role': 'x', 'refutes': 'r1-B2', 'contrary': True, 'shows_target_reached': False,
     'source': 'Guinness World Records, Longest journey walked by a humanoid robot (AgiBot A2)',
     'version': 'record page fetched 2026-09-30 (record set 10-13 Nov 2025)',
     'url': 'https://www.guinnessworldrecords.com/world-records/780227-longest-journey-walked-by-a-humanoid-robot',
     'quote': ['The longest journey walked by a humanoid robot is 106.286 km (348,707 ft 4.322 in) and was achieved by Agibot '
               'Innovation (Shanghai) Technology Co., Ltd. (China) in Shanghai, China, from 10 to 13 November 2025.'],
     'raw_file': R + 'guinness_780227.txt',
     'agent_note': 'A certified multi-day legged journey above 100 km (the floor the harvester used for "hundreds of '
                   'kilometers"). It is not range on one charge (the Guinness text does not say whether batteries were swapped; '
                   'press reports say they were, not verified here), it is on paved urban routes, and 106 km is not "hundreds". '
                   'Contrary on multi-day endurance only; the target is not reached.'},

    # ---------------- r1-B3: persistent stratospheric platforms at low cost and high recovery
    {'id': 'r1x:10', 'bottleneck': 'r1-B3', 'role': 'x', 'refutes': 'r1-B3', 'contrary': True, 'shows_target_reached': False,
     'source': 'Sceye (company statement), Sceye\'s Stratospheric Platform Re-enters United States After Record-Breaking '
               'Roundtrip Stratospheric Flight Between U.S. and Japan',
     'version': 'press release dated 9 Sep 2026', 'url': 'https://sceye.com/press-releases/sceye-completes-record-us-japan-stratospheric-flight/',
     'quote': ['The journey, which lasted 30 days and traversed nearly 30,000 km, included operating for a week in the '
               'stratosphere over Japan.',
               'Remained continuously within its target location on the coast of Japan for an extended period, achieving a '
               'station-seeking radius as low as 5 km',
               'where Sceye completed additional vehicle testing and a planned termination and descent.',
               'This mission proved not only that our technology, vehicle systems, payload, and operational infrastructure are '
               'ready for connectivity services'],
     'raw_file': R + 'sceye_pr_us_japan_2026.txt',
     'agent_note': 'A 2026 lighter-than-air HAPS that carried a cell-tower payload, worked about a week over Japan and claims '
                   'readiness for service: this contests ARIA\'s "remain too limited to deliver a commercially scalable solution" '
                   '(a company claim against a programme claim). It does not reach the named metrics: no payload power is '
                   'stated (so 300 W for a week is not shown), the station-keeping period is "extended", not a stated week, no '
                   'cost per hour is given, and the flight ended in "a planned termination", which is not a recovery for reuse '
                   '(Rredeployment). Latitude about 35 N, not the UK.'},
    {'id': 'r1x:11', 'bottleneck': 'r1-B3', 'role': 'x', 'refutes': 'r1-B3', 'contrary': True, 'shows_target_reached': False,
     'source': 'Sceye (company statement), Sceye Completes Historic 12-Day, 6,400 Mile Stratospheric Flight (SE2 Endurance Program)',
     'version': 'press release dated 13 Apr 2026',
     'url': 'https://sceye.com/press-releases/sceye-completes-historic-12-day-6400-mile-stratospheric-flight-advancing-a-new-layer-of-infrastructure-for-humanity/',
     'quote': ['Closed the power loop, maintaining power, position, and altitude during each day and night cycle.',
               'Spent over 88 hours across several selected locations during the 6,400-mile flight maintaining position and '
               'altitude, achieving a station seeking radius as low as 1 km.',
               'before completing a planned and controlled flight termination.'],
     'raw_file': R + 'sceye_pr_se2_12day_2026.txt',
     'agent_note': 'Station-keeping with the power loop closed through day and night, but 88 hours on station in total across '
                   'several locations (under ARIA\'s one-week TWR), no payload power figure, and again a planned termination. '
                   'Weak contrary evidence; target not reached.'},
    {'id': 'r1x:12', 'bottleneck': 'r1-B3', 'role': 'x', 'refutes': 'r1-B3', 'contrary': True, 'shows_target_reached': False,
     'source': 'FlightGlobal (trade press), AALTO ready to accelerate Zephyr testing after 13-day debut over Kenya (standfirst)',
     'version': 'published 6 Feb 2025; headline and standfirst reachable, body behind the subscription wall',
     'url': 'https://www.flightglobal.com/aerospace/aalto-ready-to-accelerate-zephyr-testing-after-13-day-debut-over-kenya/161695.article',
     'quote': ['Ultra-long-endurance aircraft landed after spending more than 13 days airborne over Kenya'],
     'raw_file': R + 'flightglobal_aalto_13day.txt',
     'agent_note': 'A solar HALE flight of more than a week that ended with the aircraft landed (recovered), in early 2025, '
                   'beside the two record flights that ended with the aircraft lost (harvester r1:20). One recovery does not '
                   'show a recovery rate above 0.95, and nothing here bears on cost per hour. AALTO\'s own release was HTTP 403. '
                   'Weak contrary evidence on recovery only.'},
    {'id': 'r1x:13', 'bottleneck': 'r1-B3', 'role': 'x', 'refutes': 'r1-B3', 'contrary': False, 'shows_target_reached': False,
     'source': 'ARIA, Enduring Atmospheric Platforms, call for proposals, Section 3 (technical metrics)',
     'version': 'V.2, 11 Dec 2025 (re-fetched 2026-09-30, byte-identical to the harvester\'s copy)',
     'url': 'https://aria.org.uk/media/noffgx5z/programme-solicitation-enduring-atmospheric-platforms.pdf',
     'quote': ['Applicants to the central programme effort (TA2) must present a plan to continuously do so for a full week, while '
               'maintaining station within line of sight of a fixed point on the ground.',
               'Maximises endurance within range TWR.',
               'Programme Target TWR > 1 week'],
     'raw_file': R + 'programme-solicitation-enduring-atmospheric-platforms.txt',
     'agent_note': 'Re-check of the harvester\'s "endurance target exceeded by 67 days". TWR is endurance within range of the '
                   'region of interest (station-keeping), and the primary metric needs a week within line of sight of a fixed '
                   'point. The quoted Amprius release (r1:22) states 67 days in the stratosphere, not 67 days within range of a '
                   'fixed point, so "target exceeded" is plausible but not shown by the harvester\'s source.'},

    # ---------------- r1-B4: heavy-lift drones, payload-to-weight ratio
    {'id': 'r1x:14', 'bottleneck': 'r1-B4', 'role': 'x', 'refutes': 'r1-B4', 'contrary': True, 'shows_target_reached': False,
     'source': 'DARPA, Lift Challenge scoreboard (2026 Competition Results)',
     'version': 'live page fetched 2026-09-30 ("All flight runs are complete")',
     'url': 'https://www.darpa.mil/research/challenges/lift/scoreboard',
     'quote': ['Teams that met or exceeded the challenge goal of a 4:1 ratio would earn the full prize purse. The following teams '
               'came in under the target and earned half the prize purse for each place.',
               'All flight runs are complete. Results are grouped by official scored runs and attempted runs, ranked in order '
               'by payload-to-weight ratio.',
               'Teams who continued to push the limits of heavy lift aviation as they attempted but did not receive an official '
               'score:',
               'DefendTex 12 lb. 112 lb. 9.63:1',
               'AVIDrone, Inc. | Columbia, Md. Aircraft weight Payload weight Ratio Prize 29 lb. 112 lb. 3.84:1 $1,250,000'],
     'raw_file': R + 'darpa_lift_scoreboard.txt',
     'agent_note': 'The programme owner\'s own table. A 12 lb aircraft lifted 112 lb (9.63:1, the weights are rounded) in an '
                   'attempted run that did not receive an official score; the best scored run is 3.84:1 and no scored run met '
                   '4:1 (all scored places earned half purses). The named metric is the scored 5-nmi circuit, so the target is '
                   'not reached on it; the unscored lift shows the ratio is physically attainable at this scale. CONTESTED, as '
                   'the harvester expected. No 2025-26 source outside DARPA reporting a completed flight above 4:1 was found.'},
    {'id': 'r1x:15', 'bottleneck': 'r1-B4', 'role': 'x', 'refutes': 'r1-B4', 'contrary': False, 'shows_target_reached': False,
     'source': 'DARPA, Lift Challenge programme page (DLC-2 plans)',
     'version': 'live page re-fetched 2026-09-30 (byte-identical to the harvester\'s copy)',
     'url': 'https://www.darpa.mil/research/challenges/lift',
     'quote': ['Aircraft will continue to be 55 lbs. or less', 'Minimum payload is 220 lbs., not 110 lbs',
               'A new course design will double in length to 10 nautical miles (8 loaded, 2 unloaded)'],
     'raw_file': R + 'darpa_research_challenges_lift.txt',
     'agent_note': 'Re-check of the harvester\'s r1:31 note ("raises the course length for DLC-2"): the same page also doubles '
                   'the minimum payload to 220 lb with the aircraft still at most 55 lb, so 4:1 becomes the entry floor at the '
                   'maximum weight in 2028. The programme treats 4:1 as within reach; this supports CONTESTED, not NOT OPEN.'},

    # ---------------- r1-B5: autonomous search in unknown, communication-denied environments
    {'id': 'r1x:16', 'bottleneck': 'r1-B5', 'role': 'x', 'refutes': 'r1-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'Emesent (company statement), C. Skinner, Transforming underground surveying: Fully autonomous stope mapping (blog)',
     'version': 'dated 11 Jul 2025 (URL path); page copyright 2026',
     'url': 'https://www.emesent.com/blog/2025/07/11/transforming-underground-surveying-fully-autonomous-stope-mapping',
     'quote': ['Already trusted by over 200 hard rock mines globally, Hovermap delivers breakthrough autonomy, data quality, and '
               'ease of use.',
               'no pilot, no line of sight, and no guesswork.',
               'Set your virtual bounding box and Hovermap handles the rest, autonomously flying and scanning every corner — even '
               'beyond communications range.'],
     'raw_file': R + 'emesent_blog_2025-07-11_stope.txt',
     'agent_note': 'A deployed commercial system (a company claim of use at over 200 mines) that explores and maps underground '
                   'voids autonomously beyond communications range. This contests "autonomous exploration in comm-denied '
                   'underground spaces is open" for single-drone mapping of a bounded void. It is not the SubT task (a '
                   'multi-robot search for 40 objects in 60 minutes across tunnel, urban and cave sections), so the named metric '
                   'is untouched.'},
    {'id': 'r1x:17', 'bottleneck': 'r1-B5', 'role': 'x', 'refutes': 'r1-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'Emesent (company statement), Autonomy product page (Hovermap, Emesent Cortex)',
     'version': 'live page fetched 2026-09-30 (copyright 2026; no date shown)', 'url': 'https://www.emesent.com/autonomy',
     'quote': ['enables fully autonomous missions beyond visual line of sight and communication range.',
               'Advanced failsafes and behaviors deal with challenging conditions such as dust, thin wires, and communication '
               'loss. Smart Return-to-Home finds the quickest way for the drone to return home.'],
     'raw_file': R + 'emesent_autonomy.txt',
     'agent_note': 'The lost-link behaviour of a commercial product: communication loss is handled on board with a '
                   'return-to-home. It is the same family as CERBERUS\'s homing and backtracking (harvester r1:40), now sold as '
                   'a product; no metric against a target is given.'},
    {'id': 'r1x:18', 'bottleneck': 'r1-B5', 'role': 'x', 'refutes': 'r1-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'Exyn Technologies (company statement), Underground Drone Mapping: High-Precision 3D Modeling For Mines',
     'version': 'live page fetched 2026-09-30 (undated)', 'url': 'https://www.exyn.com/underground-drone-mapping',
     'quote': ['ExynAI allows flight beyond visual line-of-sight, wireless communications, or GPS.',
               'our SLAM pipeline enables the robot to autonomously navigate in many extreme field conditions, including GPS- and '
               'comms-denied environments with little to no light.'],
     'raw_file': R + 'exyn_underground_drone_mapping.txt',
     'agent_note': 'A second vendor claiming comms-denied autonomous flight in mines. Undated marketing page; no numbers. Same '
                   'reading as r1x:16.'},
    {'id': 'r1x:19', 'bottleneck': 'r1-B5', 'role': 'x', 'refutes': 'r1-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'Rivière & Denain (Epoch AI), Where Autonomy Works (navigation section and key takeaways)',
     'version': 'published 10 Feb 2026',
     'url': 'https://epoch.ai/publications/where-autonomy-works-evaluating-robot-capabilities-in-2026',
     'quote': ['Navigation is deployed commercially, while most industrial and household tasks are not.',
               'is a collision-tolerant drone that can autonomously inspect spaces inaccessible or dangerous to humans: boiler '
               'interiors, cooling towers, mine shafts, and cave systems. It captures 3D scans and video while navigating '
               'environments with no GPS and limited visibility.'],
     'raw_file': R + 'epoch_where_autonomy_works_2026.txt',
     'agent_note': 'An independent 2026 assessment placing GPS-denied inspection navigation (Flyability Elios 3 in mine shafts '
                   'and caves) among commercially deployed capabilities. Contrary on single-robot navigation; silent on '
                   'multi-robot search under intermittent links and on the SubT artifact score.'},
    {'id': 'r1x:20', 'bottleneck': 'r1-B5', 'role': 'x', 'refutes': 'r1-B5', 'contrary': False, 'shows_target_reached': False,
     'source': 'Hudson, Talbot, ... Kottege et al. (CSIRO Data61), Heterogeneous robot teams with unified perception and autonomy: '
               'How Team CSIRO Data61 tied for the top score at the DARPA Subterranean Challenge',
     'version': 'arXiv v1, 26 Feb 2023 (the only version)', 'url': 'https://arxiv.org/abs/2302.13230v1',
     'quote': ['A total of 23 objects were successfully detected. Another four objects were detected but not reported.',
               'With time running out, the human supervisor relied heavily on teleoperation for faster traversal'],
     'raw_file': R + '2302.13230v1.txt',
     'agent_note': 'Re-check of the harvester\'s B-c. In the tied 23-point prize run the robots detected 27 of 40 (67.5%) but '
                   'reported 23, and the final part of the run relied heavily on teleoperation by the one human supervisor. So '
                   'the benchmark\'s best score is neither the robots\' detection limit nor a fully autonomous result; it cuts '
                   'both ways and does not close the bottleneck.'},
    {'id': 'r1x:21', 'bottleneck': 'r1-B5', 'role': 'x', 'refutes': 'r1-B5', 'contrary': False, 'shows_target_reached': False,
     'source': 'DARPA, Subterranean (SubT) Challenge programme page',
     'version': 'page re-fetched 2026-09-30, byte-identical to the harvester\'s copy (covers the Final Event of 21-24 Sep 2021)',
     'url': 'https://www.darpa.mil/research/challenges/subterranean',
     'quote': ['Teams earn points by correctly identifying artifacts placed within those environments.'],
     'raw_file': R + 'darpa_research_challenges_subterranean.txt',
     'agent_note': 'Re-check of the harvester\'s target "40 of 40 artifacts in 60 minutes". DARPA set no target score; teams '
                   'earn points per artifact. 40/40 is the course ceiling (an oracle), which the declaration allows as a '
                   'target, but it is not a programme goal and should be labelled as the ceiling.'},

    # ---------------- r1-B6: off-road ground autonomy at human-driver speed (harvester: not shown open)
    {'id': 'r1x:22', 'bottleneck': 'r1-B6', 'role': 'x', 'refutes': 'r1-B6', 'contrary': True, 'shows_target_reached': False,
     'source': 'Overland AI (company statement; a RACER performer), Completing RACER: What It Took to Clear the Highest Bar in '
               'Ground Autonomy',
     'version': 'dated 17 Dec 2025 in the company\'s newsroom listing (fetched 2026-09-30)',
     'url': 'https://www.overland.ai/news/completing-racer-what-it-took-to-clear-the-highest-bar-in-ground-autonomy',
     'quote': ['We have proven our autonomy on fleet vehicles, heavy platforms, and most recently on ULTRA, our own fully '
               'autonomous tactical vehicle built in-house and in production today.',
               'But we also accelerated the moment autonomy became operationally fielded'],
     'raw_file': R + 'overland_completing_racer.txt',
     'agent_note': 'A RACER performer reports its stack in production and fielded, which agrees with DARPA\'s completion claim '
                   '(harvester r1:45). No speed is compared with a human driver, so the programme target ("on par with a human '
                   'driver") is neither shown reached nor shown missed. Supports the harvester\'s "not shown open".'},

    # ---------------- r1-B7: modularity and interoperability (harvester: not shown open)
    {'id': 'r1x:23', 'bottleneck': 'r1-B7', 'role': 'x', 'refutes': 'r1-B7', 'contrary': True, 'shows_target_reached': False,
     'source': 'Mobile Industrial Robots (MiR; company statement), MiR Supports interoperability with new VDA5050 Adapter',
     'version': 'release dated 11 Mar 2025 in the text (page metadata published 20 Apr 2026, modified 24 Apr 2026)',
     'url': 'https://mobile-industrial-robots.com/news-center/mir-supports-interoperability-with-vda5050',
     'quote': ['By simplifying integration to third-party systems, this new software adapter enables interoperability for '
               'warehouses, distribution centers and manufacturing facilities seeking a standardized approach to managing '
               'diverse heritage robot fleets, reducing integration complexities, and improving operational efficiency.'],
     'raw_file': R + 'mir_vda5050_adapter.txt',
     'agent_note': 'Multi-vendor interoperability is shipping at the fleet-control level for mobile robots (VDA 5050). This '
                   'contests "rarely interoperable" for AMR fleets. It says nothing about the hardware and low-level module '
                   'modularity that ARIA TA3 and euROBIN name, and no metric exists, so no target can be reached.'},
    {'id': 'r1x:24', 'bottleneck': 'r1-B7', 'role': 'x', 'refutes': 'r1-B7', 'contrary': True, 'shows_target_reached': False,
     'source': 'VDA / VDMA / KIT-IFL, VDA5050 repository README',
     'version': 'GitHub VDA5050/VDA5050, main branch, fetched raw 2026-09-30 (states version 3.0.0; release date not reachable, '
                'github.com HTML returned 403)',
     'url': 'https://github.com/VDA5050/VDA5050',
     'quote': ['An open standard for communication between mobile robot fleets and a central fleet control.',
               'The *main* branch contains the latest published version of VDA 5050 (currently version 3.0.0).'],
     'raw_file': R + 'github_VDA5050_README.txt',
     'agent_note': 'The standard behind r1x:23, maintained and at version 3.0.0 by 2026. Partial solution in one sub-domain '
                   '(fleet control of mobile robots); no metric.'},
]

CHECKS = [
    {'bottleneck': 'r1-B1',
     'searched': ['WebSearch: robot manipulation "human speed" 2026 benchmark throughput robot matches human',
                  'WebSearch: aboutamazon.com Vulcan robot sense of touch stow speed human',
                  'WebSearch: RL-100 real-world reinforcement learning manipulation surpasses human teleoperation efficiency cycle time',
                  'WebSearch: Robothon 2026 grand challenge results task board best time',
                  'WebSearch: NIST assembly task board robot completion time human baseline 2025 competition results faster than human',
                  'WebSearch: Science Robotics 2025 robot hand dexterity matches human speed benchmark in-hand manipulation human-level',
                  'Epoch AI report (10 Feb 2026); Amazon Vulcan release (2025); arXiv 2510.14830v4 (RL-100); arXiv 2604.09294 '
                  '(POMDAR benchmark, abstract: no numbers, screened only)',
                  'Robothon README re-read in full and the 2022 scorecard PDF (image-only, read by eye)'],
     'finding': 'CONTESTED at most, not NOT OPEN. Deployed manipulators work at about human speed on single engineered tasks '
                '(Amazon Vulcan stow/pick, on about 75% of items; CATL connector insertion as relayed by Epoch), and learned '
                'policies match or beat expert teleoperators on trained tasks (RL-100). A 2026 independent assessment (Epoch) '
                'argues speed is "not the main bottleneck to deployment" (transfer is), a partial misframing argument, while '
                'confirming robots are typically 3-10x slower than humans. No 2025-26 source reports a robot at or above the '
                'human time on the Robothon task board or on any varied manipulation protocol with a timed human baseline; no '
                'Robothon 2026 result was found. The generality half of the bottleneck is supported by every source found.',
     'harvester_errors': ['Best robot time: the harvester used DR.J Table 6\'s 52 s, but the organiser\'s own README (which the '
                          'harvester quoted for 2023 and 2025) gives "Best Time 31 seconds" for 2022 (RoboTechX MDX, all six '
                          'tasks ticked on the scorecard) on the same 2021 six-task protocol; on 31 s the gap is 3.8x (0.26 of '
                          'the best human), not 6.4x (0.156). The two records from the same organiser disagree; the harvester '
                          'reported only the larger gap.',
                          '"also the best any-robot composite": the AnyRobot row\'s per-subtask best times (11, 5.8, 5.1, 12, 0.2, '
                          '1.9) sum to 36.0 s although the table\'s trial column reads 52; the per-subtask historical limit is '
                          '4.4x the best human, not 6.4x. Minor; the quote itself is verbatim.']},
    {'bottleneck': 'r1-B2',
     'searched': ['WebSearch: humanoid robot longest distance walked Guinness record 2025 km',
                  'WebSearch: quadruped robot marathon single charge 42 km completed',
                  'WebSearch: KAIST RAIBO2 marathon Nature 2026 cost of transport 0.25 press release',
                  'WebSearch: Cornell Ranger total cost of transport 0.19 65 km single charge',
                  'Nature s41586-026-11102-5 (abstract; full text paywalled); KAIST release 17 Nov 2024; Guinness record '
                  '780227; AgiBot record page (screened); Cornell Chronicle 10 May 2011',
                  'Harvester raw texts re-read: Burden et al. (no robot CoT figure) and Riener et al. (robots sampled in its table)'],
     'finding': 'Split by metric. Cost of transport: the target is reached. RAIBO2 (Nature, 23 Sep 2026) ran a full marathon on '
                'one charge with a total CoT of 0.25, "surpassing the human benchmark of 0.37" and inside the harvester\'s human '
                'range 0.2-0.47; even Ranger was at 0.28 in 2011. Range on one charge: not reached (RAIBO2 42.195 km; Ranger 65 km; '
                'the human baseline is "hundreds of kilometers" over days). Multi-day endurance with battery swaps reached 106.286 '
                'km (AgiBot A2, Guinness, Nov 2025) on paved routes. Robustness outside prepared ground: a four-hour public road '
                'race with climbs was completed (KAIST), but not rough terrain and not with loads, so the bottleneck as ARIA '
                'frames it (a shift carrying loads over uneven terrain) is still open. Because one of the two named metrics shows '
                'the target reached (r1x:6), the table rule reads NOT OPEN; the fair summary is "closed on CoT, open on range and '
                'rough-terrain duty".',
     'harvester_errors': ['"best robot CoT 0.52 (MIT Cheetah)" and "CoT 1.1x-2.6x the human value for the best robot": Riener et '
                          'al.\'s "closest of all robots" is limited to the robots in its own table. Ranger, which the harvester '
                          'cites for range, had a CoT of 0.28 in 2011 (Cornell Chronicle), inside the human range the harvester '
                          'used as the target; RAIBO2 reports 0.25 (Nature 2026). The CoT gap was already 0.6x-1.4x in 2011 and is '
                          'now below the human benchmark.',
                          '"range at least 1.5x (taking 100 km as the floor of \'hundreds\')": "hundreds of kilometers" implies at '
                          'least 200 km, so on the harvester\'s own reading the range gap is at least 3.1x (65 km); the floor of '
                          '100 km understated it. The comparison also mixes one battery charge (robot) with multi-day refuelled '
                          'running (athletes); the harvester flagged the second point only in part.']},
    {'bottleneck': 'r1-B3',
     'searched': ['WebSearch: AALTO Zephyr 2026 flight landed recovered commercial service stratosphere',
                  'WebSearch: HAPS 2026 stratospheric airship payload power kW record flight Sceye',
                  'WebSearch: Sceye ST1 30-day flight Japan landed recovered payload power watts press release 2026',
                  'WebSearch: aaltohaps.com news 2026 Zephyr flight Japan entry into service recovered landing',
                  'Sceye releases of 13 Apr 2026 (SE2) and 9 Sep 2026 (ST1); FlightGlobal 6 Feb 2025 (standfirst only, '
                  'paywall); AALTO\'s own Kenya release and its PDF (HTTP 403, not reached)',
                  'ARIA EAP call re-fetched and re-read (Section 3 metrics)'],
     'finding': 'CONTESTED weakly. In 2026 a lighter-than-air HAPS (Sceye ST1) carried a cell-tower payload, worked about a '
                'week over Japan within a 5 km station radius at best, and its maker claims readiness for service; a solar HALE '
                '(Zephyr) landed after a 13-day flight in 2025. None shows the named targets: no payload power figure (300 W '
                'for a week), no cost per hour (below GBP 500/hr), and no recovery rate (above 0.95); Sceye\'s flights ended in '
                'planned terminations, not recovery for reuse, and at about 35 N, not UK latitudes. Nothing found argues the '
                'bottleneck is misframed.',
     'harvester_errors': ['"endurance (> 1 week) already exceeded by 67 days ... so it is not the open part": ARIA\'s TWR is '
                          '"endurance within range" (station-keeping for the region of interest; the primary metric needs a week '
                          'within line of sight of a fixed point). The quoted Amprius release states 67 days in the '
                          'stratosphere, not 67 days within range of a fixed point, so "target exceeded" is plausible but not '
                          'shown by the harvester\'s source.']},
    {'bottleneck': 'r1-B4',
     'searched': ['WebSearch: DARPA Lift Challenge 2026 results DefendTex 9.63 payload ratio scored run',
                  'WebSearch: drone carries payload more than four times its own weight flight test 2025 2026 record',
                  'DARPA Lift scoreboard page; DARPA Lift programme page re-fetched (DLC-2 rules)',
                  'Search results from trade press (DroneXL, Defense News, UAS Weekly) screened by snippet only; none adds a '
                  'completed flight above 4:1'],
     'finding': 'CONTESTED, as the harvester expected. DARPA\'s scoreboard lists DefendTex lifting 112 lb on a 12 lb aircraft '
                '(9.63:1) in an attempted run that received no official score; the best scored run is 3.84:1 and no scored run '
                'met 4:1. DARPA reads 4:1 as possible and sets it as the entry floor for DLC-2 (220 lb minimum payload, 55 lb '
                'maximum aircraft). The target '
                'is not reached on the named (scored-circuit) metric; no other 2025-26 source reporting a completed circuit '
                'above 4:1 was found.',
     'harvester_errors': ['Omission, not a misquote: the harvester\'s r1:31 note says DLC-2 "raises the course length", but the '
                          'same page also doubles the minimum payload to 220 lb with the aircraft still at most 55 lb, making 4:1 '
                          'the floor at maximum weight in 2028.']},
    {'bottleneck': 'r1-B5',
     'searched': ['WebSearch: autonomous drone underground mine exploration beyond communication range deployed 2025 GPS-denied '
                  'commercial',
                  'WebSearch: Emesent Hovermap autonomy beyond communication range underground mine exploration return home',
                  'WebSearch: CSIRO Data61 SubT final event artifacts detected but not reported "of the 40 artifacts" lessons',
                  'WebSearch: arXiv 2025 2026 autonomous subterranean exploration field deployment mine multi-robot results after '
                  'DARPA SubT communication-denied',
                  'WebSearch: "How Team CSIRO Data61 Tied for the Top Score at the DARPA Subterranean Challenge" arXiv',
                  'Emesent blog (11 Jul 2025) and autonomy page; Exyn mining page; Epoch AI report (2026); arXiv 2302.13230v1 '
                  '(CSIRO); arXiv 2212.05626v1 (human-robot vs full autonomy, 2022, screened); arXiv 2501.10262v1 (aerial '
                  'multi-agent mine deployment, 2025, screened: a Wi-Fi mesh supports the agents, no score against a target)',
                  'DARPA SubT page re-fetched (scoring rule)'],
     'finding': 'CONTESTED for the capability, open on the benchmark. Commercial drones map underground voids autonomously '
                'beyond communications range with on-board lost-link handling (Emesent Hovermap, claimed in use at over 200 '
                'mines, 2025; Exyn), and a 2026 independent assessment lists GPS-denied inspection in mine shafts and caves '
                'among deployed capabilities. These are single-robot mapping missions in bounded voids, not multi-robot search '
                'for objects under intermittent links. SubT has not been re-run and no newer score on it or on a comparable '
                'artifact-search benchmark was found; the 23/40 of 2021 remains the best number.',
     'harvester_errors': ['"target: 40 of 40 artifacts in 60 minutes": DARPA stated no target score ("Teams earn points by '
                          'correctly identifying artifacts"); 40/40 is the course ceiling (an oracle), which should be labelled '
                          'as such rather than as the programme target.',
                          'The benchmark result is presented as autonomous search, but CSIRO\'s tied 23-point run ended with the '
                          'human supervisor relying "heavily on teleoperation", and its robots detected 27 of 40 (four detected but '
                          'not reported). The score is neither fully autonomous nor the detection limit.']},
    {'bottleneck': 'r1-B6',
     'searched': ['WebSearch: DARPA RACER autonomous vehicle speed compared human driver 2025 results off-road',
                  'WebSearch: Overland AI OverDrive off-road autonomy speed "human" driver RACER 2025',
                  'WebSearch: RACER program 2025 final experiment autonomous vehicles "human-driven" speed comparison average mph',
                  'Harvester raw texts re-read (RACER page, 2023, 2024 and 2026 releases, the 2025 profile): no human-driver '
                  'speed anywhere',
                  'Overland AI homepage and its RACER article; JPL RACER Experiment 5 news (15 Jul 2024; screened, no numbers); '
                  'GeekWire article on Overland ULTRA (HTTP 403)'],
     'finding': 'Agrees with the harvester\'s "not shown open". A RACER performer (Overland AI, Dec 2025) reports its stack in '
                'production and operationally fielded, matching DARPA\'s January 2026 completion claim. No source found '
                'publishes a human-driver speed on the RACER courses, so the target "on par with a human driver" can be shown '
                'neither reached nor missed.',
     'harvester_errors': []},
    {'bottleneck': 'r1-B7',
     'searched': ['WebSearch: robot interoperability standard 2025 adopted VDA 5050 MassRobotics ISO 22166 modularity service robots',
                  'VDA5050 GitHub README (raw); MiR VDA 5050 adapter release (Mar 2025); MassRobotics interoperability page '
                  '(2023, screened: version 1.0 of 2021, version 2.0 in progress); ISO 22166-1 page (HTTP 403)'],
     'finding': 'Partial solutions ship in one sub-domain: fleet-level interoperability of mobile robots through VDA 5050 '
                '(version 3.0.0 by 2026) with vendor adapters (MiR, 2025). Nothing found addresses the hardware and low-level '
                'module modularity that ARIA TA3 and euROBIN name, and no metric with a target exists, so the harvester\'s "not '
                'shown open" stands; the contrary evidence is partial.',
     'harvester_errors': []},
]
