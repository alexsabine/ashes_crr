"""ROB1 stage 1b, family R3 (Robotics/DECLARATION.md): the double check of the drone bottlenecks r3-B1 ... r3-B7.

Written by a second agent that did not harvest family R3. For every bottleneck in `claims_r3.BOTTLENECKS` (including
r3-B4, which the harvester read as not shown open) it searched independently (different queries and sources from the
harvester's; log in /tmp/claude-0/rob_src/r3x/search/queries.txt) for the strongest contrary evidence: a 2025-26 source
reporting the target reached on the named metric, a deployed system that does it, or a source arguing that the bottleneck
is misframed. It also re-read the harvester's quotes and numbers against the harvester's raw texts
(/tmp/claude-0/rob_src/r3/txt/); a scratch copy of Open_Bottlenecks/checks/verify.py pointed at claims_r3.py read "quotes
found verbatim: 150 of 150 (claims 60; raw files 22, missing 0)" (r3x/verify_r3_recheck.txt), and the ByteTrack table of
arXiv 2607.05467 (r3:20) was parsed in full to confirm the harvester's per-video best values.

Every source was fetched on 2026-09-30 through the session proxy with curl (TLS verification on). arXiv: the abstract page
(for the current version and its history) and the PDF of that version. Text was extracted with the harvester's own
extractors (copied to r3x/): PDFs by pymupdf 1.28.2 (`page.get_text()`, pages joined by newlines); HTML by BeautifulSoup 4
(`get_text('\\n')` after removing script/style/noscript/svg, runs of spaces and blank lines collapsed). Raw files live outside
the repository under /tmp/claude-0/rob_src/ (`raw_file` is relative to that root; the fetched originals are in r3x/src/);
their sha256 is in /tmp/claude-0/rob_src/r3x/SHA256SUMS.txt and in the dossier docs/citations/rob1_r3_2026-09-30.md
(section "Stage 1b double check"). Claims that re-check the harvester's own sources point at the harvester's raw texts under
r3/txt/. Hosts that refused curl (403, or a JavaScript challenge) are listed in the dossier and are not used. A scratch copy
of Open_Bottlenecks/checks/verify.py (r3x/verify_r3x_scratch.py) pointed at this file read "quotes found verbatim: 72 of 72
(claims 24; raw files 22, missing 0)"; with one number altered (99.99% -> 99.95% in r3x:15) it read 71 of 72, as it should
(r3x/verify_r3x_negative_control.txt).

Fields. role = 'x' (a double-check claim). `refutes` = the bottleneck the claim bears on. `contrary` = True when the claim
is contrary evidence (the target reached, a deployed system that does it, or a misframing argument); False when it is a
re-check or a corroboration of the harvester's reading (a number or a framing the harvester got wrong, overstated, or got
right), which bears on the bottleneck's B-c but is not evidence that the bottleneck is closed. `shows_target_reached` = True
only if the verified quote shows the target reached on the named metric of that bottleneck (the named metric as the
harvester's BOTTLENECKS entry states it: the quantity and the target, not necessarily the same paper's protocol; every True
says in its note how the protocol differs, and whether the source is 2025-26). `agent_note` is the double-checker's reading,
fair to both sides; it is not the source's words. Company statements, university news releases, state media and vendor
white papers are recorded as such; a company's claim about its own product is not an independent measurement.

CHECKS: one entry per bottleneck: what was searched, what was found, and `harvester_errors` (quotes or numbers the
harvester got wrong or overstated; an empty list when none was found). Every harvester quote was found verbatim; the
errors listed are readings, framings and a source statement passed through unchecked against its own table, not misquotes.
"""

R = 'r3x/txt/'
H = 'r3/txt/'  # the harvester's raw texts, re-read

CLAIMS = [
    # ---------------- r3-B1: endurance and energy of small battery-electric multirotors
    {'id': 'r3x:1', 'bottleneck': 'r3-B1', 'role': 'x', 'refutes': 'r3-B1', 'contrary': True, 'shows_target_reached': True,
     'source': 'DJI Enterprise, Matrice 400 specifications (manufacturer statement)',
     'version': 'live product specification page fetched 2026-09-30 (no date shown)',
     'url': 'https://enterprise.dji.com/matrice-400/specs',
     'quote': ['Max Payload 6 kg',
               'Max Flight Time (no wind) 59 minutes*',
               'Measured with the aircraft flying forward at a constant speed of 10 m/s in a windless environment at sea level, '
               'carrying only the H30T (total weight 10,670 g), until a forced landing due to battery depletion.',
               'Max Flight Distance (no wind) 49 km Measured by the aircraft flying forward at a constant speed of 17 m/s in a '
               'windless environment at sea level, carrying only the H30T (total weight 10,670 g), and from 100% battery level '
               'until 0%.'],
     'raw_file': R + 'dji_matrice-400_specs.txt',
     'agent_note': 'A deployed battery-electric multirotor with a useful payload. The harvester\'s named quantity for r3-B1 is '
                   'range on one battery against the 9 km SPRIN-D course: this manufacturer figure is 49 km on one battery with '
                   'the H30T camera payload (10.67 kg total), 5.4x the 9 km course; 59 min flight time. So the quantity as named '
                   'is reached by a commercial battery-electric multirotor. How the protocol differs: a manufacturer\'s own '
                   'figure (not independently measured), windless sea level, constant 17 m/s, flown to 0% with no reserve, a '
                   'camera payload rather than a LiDAR + onboard-computer autonomy payload, and no GNSS-denied autonomy. Fair '
                   'to the harvester: at the SPRIN-D winner\'s average speed (1371 m / 977 s = 1.40 m/s, limited by its '
                   'local-map size, r3x:4) 59 min covers about 4.96 km, still short of 9 km; and 59 min is still "tens of '
                   'minutes", so the duration half of the problem statement stands. What this refutes is the reading of the '
                   'SPRIN-D 15% (1371/9000) as the battery-electric frontier: it reflects that team\'s platform and speed.'},
    {'id': 'r3x:2', 'bottleneck': 'r3-B1', 'role': 'x', 'refutes': 'r3-B1', 'contrary': True, 'shows_target_reached': False,
     'source': 'Xinhua via China Daily, Chinese hydrogen-powered drone sets longest distance flight record (state media; the same '
               'Xinhua text is on english.scio.gov.cn, saved as r3x/txt/scio_2025-12-12_tianmushan.txt)',
     'version': 'article dated 12 Dec 2025 (page shows "Updated: 2025-12-12 09:52")',
     'url': 'https://global.chinadaily.com.cn/a/202512/12/WS693b757aa310d6866eb2e48f.html',
     'quote': ['A Chinese drone has accomplished the longest distance flight of a hydrogen-powered multirotor/drone by 188.605 km, '
               'the Guinness World Records announced on Thursday at the 7th Zhejiang International Intelligent Transportation '
               'Industry Expo in Hangzhou',
               'The drone, Tianmushan-1, completed this flight in more than four hours on Nov 16 in Hangzhou, according to '
               'Beihang University.',
               'Featuring a 1,600 mm wheelbase and a 19 kg empty weight, the zero-emission drone can carry up to 6 kg of '
               'payload. It is also capable of delivering an ultra-long 240-minute unloaded endurance'],
     'raw_file': R + 'chinadaily_2025-12-12_tianmushan.txt',
     'agent_note': 'This is the 2025 hydrogen distance record that the harvester found only in a trade-press header (fuelcellsworks, '
                   'body not served). Here it is from state media reporting the Guinness announcement; the Guinness record page '
                   'itself was not found. A multirotor flew 188.605 km (21x the 9 km course) in more than four hours on one '
                   'fuelling (Nov 2025). The payload carried on the record flight is not stated (capacity 6 kg). It does not show '
                   'the target reached on the named metric, because the bottleneck is scoped to battery-electric multirotors and '
                   'the named metric is range per battery. It strengthens the harvester\'s CONTESTED note: for multirotors as '
                   'such, endurance is an energy-carrier choice, not a limit.'},
    {'id': 'r3x:3', 'bottleneck': 'r3-B1', 'role': 'x', 'refutes': 'r3-B1', 'contrary': True, 'shows_target_reached': False,
     'source': 'Amprius Technologies, Amprius Introduces SiCore 500 High-Energy-Density Cells for Unmanned Aviation (press release)',
     'version': 'press release dated 2 Sep 2026 (company statement with forward-looking statements)',
     'url': 'https://ir.amprius.com/news-events/press-releases/detail/174/amprius-introduces-sicore500-high-energy-density-cells-for-unmanned-aviation',
     'quote': ['The cell delivers 500 Wh/kg at a 1C continuous discharge rate and can be produced on conventional lithium-ion '
               'battery manufacturing equipment.',
               'The new SiCore cell is optimized for the sustained, low-rate discharge profiles required for High-Altitude '
               'Platform Stations (HAPS), fixed-wing drones, and other long-endurance applications.',
               'Amprius currently expects commercial availability in Q4 2026, with cells built in customer-specific formats and '
               'in the standard small uncrewed aircraft systems (sUAS) pouch format defined by SAE JA1016.'],
     'raw_file': R + 'amprius_sicore500_pr174.txt',
     'agent_note': 'A misframing argument against the harvester\'s specific-energy target. The 200 Wh/kg lithium-ion reference '
                   '(Williamson et al.) is not a fixed ceiling: silicon-anode lithium-ion cells are claimed at 500 Wh/kg (2.5x). '
                   'It does not show the target reached on the named metric: the target is parity of an alternative (non-lithium) '
                   'power source with lithium-ion, and this cell is itself lithium-ion. It is also a cell-level company figure '
                   '(no pack, no flight), optimised for low-rate discharge (fixed wing, HAPS), not for multirotor hover power, '
                   'and commercial availability is only expected in Q4 2026.'},
    {'id': 'r3x:4', 'bottleneck': 'r3-B1', 'role': 'x', 'refutes': 'r3-B1', 'contrary': False, 'shows_target_reached': False,
     'source': 'Werner et al., SPRIN-D winning system (Table I; Sec. IV-A; Lessons learned) - the harvester\'s source, re-read',
     'version': 'arXiv v2, 25 May 2026', 'url': 'https://arxiv.org/abs/2510.01348v2',
     'quote': ['Each team had 2 hours to demonstrate the capability of their system and visit as many waypoints as possible.',
               'Flight ID Length [m] Time [s] RMSEodom [m] RMSEmethod [m] Waypoints detected Area Termination',
               '206† 1023 621 27 6 2/2 urban SW issue',
               '232† 1256 1021 53 7 1/2 forest failsafe - HW issue',
               '239† 1371 977 8 9 4/4 forest low battery',
               'In our case, the limited size of the local map restricted flight speed, which in turn capped the effective '
               'mission range despite accurate localization.'],
     'raw_file': H + '2510.01348v2.txt',
     'agent_note': 'Re-check of the harvester\'s B-c (r3:3). (1) The source\'s sentence "Flights exceeding 1 km were consistently '
                   'terminated due to battery constraints", quoted by the harvester, is contradicted by the source\'s own Table I: '
                   'of the three competition flights over 1 km, 206 (1023 m) ended on a software issue, 232 (1256 m) on a hardware '
                   'failsafe, and only 239 (1371 m) on low battery. The low-battery flights are 872, 939 and 1371 m. (2) The '
                   'programme gave a 2 h slot to visit as many waypoints as possible; it did not ask for the 9 km on one battery, '
                   'so "range per battery against 9 km" is the harvester\'s construction, not the programme\'s target. (3) The '
                   'source names the speed limit set by its local map as what capped range; at 1.40 m/s a flight of 977 s '
                   '(16.3 min, inside the typical 10-30 min) covers 1.37 km. The endurance figure is typical, not a frontier.'},

    # ---------------- r3-B2: GNSS-denied long-range navigation at low altitude
    {'id': 'r3x:5', 'bottleneck': 'r3-B2', 'role': 'x', 'refutes': 'r3-B2', 'contrary': True, 'shows_target_reached': False,
     'source': 'Werner et al., SPRIN-D winning system (Table I; Sec. IV-B) - the harvester\'s source, re-read for the termination causes',
     'version': 'arXiv v2, 25 May 2026', 'url': 'https://arxiv.org/abs/2510.01348v2',
     'quote': ['205† 939 622 31 10 1/1 urban test finished',
               '208† 872 500 14 11 1/1 urban/open field low battery',
               '242† 939 622 9 11 2/3 urban/open field low battery',
               'our method managed to correct the position estimate when the UAV observed the trees and in the end reduced its '
               'error to approx. 4 m'],
     'raw_file': H + '2510.01348v2.txt',
     'agent_note': 'A misframing argument from the harvester\'s own benchmark. Across the six competition flights in Table I the '
                   'terminations are: test finished 1, software issue 1, hardware failsafe 1, low battery 3, localization drift 0; '
                   'the method\'s RMSE stays 6-11 m against odometry RMSE 8-53 m, and a 32 m initialisation error was corrected '
                   'to about 4 m. So the gap to the 9 km course (15%) is not a navigation-drift gap: it is energy, speed and '
                   'hardware reliability. It does not show the target reached (no flight or sequence covers the 9 km course), '
                   'and the competition ground truth is approximate (0-5 m).'},
    {'id': 'r3x:6', 'bottleneck': 'r3-B2', 'role': 'x', 'refutes': 'r3-B2', 'contrary': True, 'shows_target_reached': False,
     'source': 'University of Klagenfurt news, Team from the University of Klagenfurt wins European drone competition '
               '"Fully Autonomous Flight 2.0" (university release about its own team)',
     'version': 'news item dated 11 Sep 2026',
     'url': 'https://www.aau.at/en/blog/team-der-universitaet-klagenfurt-gewinnt-europaeischen-drohnen-wettbewerb-fully-autonomous-flight-2-0/',
     'quote': ['The final, held from 24 to 27 August 2026, consisted of two missions, each comprising a static and a dynamic task. '
               'Teams only saw the operational area when it was their turn to compete: they had 30 minutes to prepare, followed '
               'by 60 minutes of mission time.',
               'This victory is the result of years of fundamental research into robust state estimation and navigation without '
               'GPS, and it demonstrates that this research is ready for the real world.',
               'As the drone is a research system rather than a finished product, it was not protected against rain.'],
     'raw_file': R + 'aau_hermes_fully_autonomous_flight_2.0.txt',
     'agent_note': 'The 2025-26 edition of the harvester\'s programme (SPRIND Fully Autonomous Flight 2.0) ended with a GNSS-free, '
                   'pilot-free winner, and the winning group states its GNSS-free navigation is "ready for the real world". '
                   'The final\'s missions were 60-minute tasks in an area (find a house number, search and rescue, follow a person), '
                   'not a 9 km course: the programme itself moved from long-range traversal to semantic missions. No distance, '
                   'error or waypoint score is published, so this does not show the target reached; it is a claim by the winner '
                   'about its own work, and the same text says the drone was not weather-protected.'},
    {'id': 'r3x:7', 'bottleneck': 'r3-B2', 'role': 'x', 'refutes': 'r3-B2', 'contrary': True, 'shows_target_reached': False,
     'source': 'CTU Department of Cybernetics news, MRS CTU & F4F success in Germany\'s SPRIND Fully Autonomous Flight 2.0 competition',
     'version': 'news item dated 11 Sep 2026',
     'url': 'https://cyber.felk.cvut.cz/news/mrs-ctu-f4f-succeess-in-germanys-sprind-fully-autonomous-flight-2-0-competition/',
     'quote': ['has successfully demonstrated a drone capable of understanding natural-language instructions, planning its own '
               'mission and executing it fully autonomously — without GPS or pilot intervention.',
               'The developed system combines four cameras, a 3D LiDAR and onboard computing with autonomous localisation and '
               'mapping, object and situation recognition, and mission planning based on natural-language instructions.',
               'Further details about the system will be presented in upcoming research publications.'],
     'raw_file': R + 'ctu_sprind_fully_autonomous_flight_2.0.txt',
     'agent_note': 'The 2024 winner (Fly4Future/CTU, the harvester\'s B-c source) competed again in 2026 and reports GNSS-free, '
                   'pilot-free missions from natural-language instructions. Contrary in direction (the frontier has moved on '
                   'from pure traversal), but no metric is published and details are deferred to future papers.'},
    {'id': 'r3x:8', 'bottleneck': 'r3-B2', 'role': 'x', 'refutes': 'r3-B2', 'contrary': True, 'shows_target_reached': False,
     'source': 'Northrop Grumman news release, Northrop Grumman\'s Lumberjack proves quantum-enabled flight capabilities',
     'version': 'news release dated 9 Sep 2026 (company statement)',
     'url': 'https://news.northropgrumman.com/autonomous-systems/northrop-grumman-lumberjack-quantum-enabled-flight-capabilities-advance-warfighter-missions',
     'quote': ['collaborated with SandboxAQ to demonstrate quantum sensing magnetic navigation on',
               'a Group 3 uncrewed aircraft system (UAS), just one month after establishing an objective to fly this capability '
               'on this type of platform.',
               'The quantum-based navigation system resisted jamming and operated reliably in GPS-denied environments, including '
               'over open water.'],
     'raw_file': R + 'northropgrumman_lumberjack_quantum_2026.txt',
     'agent_note': 'A fielded-direction item for the programme-listed magnetic-navigation family (r3:16): magnetic anomaly '
                   'navigation flown on a Group 3 UAS, including over open water, where terrain or visual matching has no '
                   'structure (the harvester\'s open-field failure case). It does not show the target reached: no distance, '
                   'error or altitude is published, it is a company statement, and a Group 3 aircraft is not a small multirotor '
                   'below 25 m AGL.'},
    {'id': 'r3x:9', 'bottleneck': 'r3-B2', 'role': 'x', 'refutes': 'r3-B2', 'contrary': True, 'shows_target_reached': False,
     'source': 'Ye et al., Exploring the best way for UAV visual localization under Low-altitude Multi-view Observation '
               'Condition: a Benchmark (AnyVisLoc)',
     'version': 'arXiv v2, 13 Apr 2026 (v1 12 Mar 2025)', 'url': 'https://arxiv.org/abs/2503.10692v2',
     'quote': ['This baseline achieved a 74.1% localization accuracy within 5m under low-altitude, multi-view conditions.',
               'AnyVisLoc (Ours) 2026 Real-scenes 7 ✓ Aerial & Satellite ✓ 30m to 300m'],
     'raw_file': R + '2503.10692v2.txt',
     'agent_note': 'Bears on the harvester\'s B-d reading (r3:14) that satellite-image matching is "highly unreliable at such low '
                   'altitudes": on real low-altitude oblique imagery (30-300 m, seven scenes) the best absolute visual '
                   'localization baseline places 74.1% of images within 5 m of truth against aerial or satellite maps. It does '
                   'not show the target reached: it is per-image localization on a dataset, not a flown course, the altitudes '
                   'start at 30 m (SPRIN-D required below 25 m), and 25.9% of images are outside 5 m.'},

    # ---------------- r3-B3: perception in fog and haze
    {'id': 'r3x:10', 'bottleneck': 'r3-B3', 'role': 'x', 'refutes': 'r3-B3', 'contrary': False, 'shows_target_reached': False,
     'source': 'Pouladi et al., synthetic fog (Table 3, Video 10 rows; Sec. 5) - the harvester\'s source, re-read',
     'version': 'arXiv v1, 6 Jul 2026', 'url': 'https://arxiv.org/abs/2607.05467v1',
     'quote': ['10 11n clean 0.245 0.200 0.299 0.194 0.302 0.205 0.107 0.095 0.246 0.182 0.000 0.000 0.003 0.005',
               '11s 50% foggy 0.303 0.195 0.368 0.240 0.332 0.194 0.347 0.204 0.319 0.188 0.157 0.147 0.154 0.123',
               'Video 10 is consistently the most challenging sequence for both ByteTrack and BoT-SORT. This suggests that the main '
               'limitation is the combined difficulty of small-target detection, sequence content, and severe visibility loss, '
               'rather than the tracker choice alone.'],
     'raw_file': H + '2607.05467v1.txt',
     'agent_note': 'Re-check of r3:20 (the whole ByteTrack table was parsed: the harvester\'s per-video best values are right: '
                   'best clean 1.000 / 0.980 / 0.995 / 0.321 and best at beta = 3.6 0.771 / 0.940 / 0.960 / 0.179 for videos '
                   '02 / 03 / 06 / 10). On Video 10 the clean oracle is itself only 0.321, and light fog does not lower it (0.368 '
                   'at beta = 0.4 for 11s 50% foggy; 0.359 at beta = 1.6 for 11s 100% foggy): the sequence is hard without fog. '
                   'The heavy-fog drop on V10 (0.179 vs 0.321) is still real, so the harvester\'s "open on the worst sequences" '
                   'stands, but the low absolute level of V10 is not a fog effect.'},
    {'id': 'r3x:11', 'bottleneck': 'r3-B3', 'role': 'x', 'refutes': 'r3-B3', 'contrary': False, 'shows_target_reached': False,
     'source': 'Pouladi et al., synthetic fog (Sec. 5, scope) - the harvester\'s source, re-read',
     'version': 'arXiv v1, 6 Jul 2026', 'url': 'https://arxiv.org/abs/2607.05467v1',
     'quote': ['The results provide a systematic analysis of relative robustness under physically motivated degradation, but they '
               'do not by themselves establish performance under real fog. Validation on real adverse-weather anti-UAV data '
               'remains an important direction for future work.'],
     'raw_file': H + '2607.05467v1.txt',
     'agent_note': 'The source limits its own reach: the B-c gap is a synthetic-fog gap. This cuts both ways (the harvester '
                   'noted "synthetic fog"): the real-fog gap could be larger or smaller; neither a closure nor a real-fog gap is '
                   'measured.'},
    {'id': 'r3x:12', 'bottleneck': 'r3-B3', 'role': 'x', 'refutes': 'r3-B3', 'contrary': False, 'shows_target_reached': False,
     'source': 'Lenhard et al., Beyond Clear Skies: Synthetic Seasonal and Weather Variations for Real-World Drone Detection (SDV-W)',
     'version': 'arXiv v1, 17 Aug 2026 (only version)', 'url': 'https://arxiv.org/abs/2608.16191v1',
     'quote': ['Snow and fog are most disruptive, reducing mAP@0.25 by 8.2/6.2 percentage points (pp) and raising FNR by 15.8/12.7 '
               'pp, respectively.',
               'we show that SDV-W improves detector reliability under adverse appearance shifts, reduces missed detections and '
               'false alarms, and is most effective as a complement to general-purpose synthetic drone-detection data.',
               'A key limitation remains the lack of real-world data capturing genuine and diverse adverse-weather for evaluation.'],
     'raw_file': R + '2608.16191v1.txt',
     'agent_note': 'An independent 2026 drone-detection source found while searching for a closure; it corroborates the problem '
                   'instead. On matched clean/adverse synthetic scenes, fog lowers mAP@0.25 by 6.2 pp and raises the miss rate '
                   'by 12.7 pp averaged over YOLO models; synthetic weather training helps but is not shown to close the gap, and '
                   'the authors again name the lack of real adverse-weather evaluation data. No contrary evidence.'},

    # ---------------- r3-B4: agile flight against human pilots (the harvester read it as not shown open)
    {'id': 'r3x:13', 'bottleneck': 'r3-B4', 'role': 'x', 'refutes': 'r3-B4', 'contrary': True, 'shows_target_reached': True,
     'source': 'De Wagter et al. (TU Delft MAVLab), MonoRace: Winning Champion-Level Drone Racing with Robust Monocular AI',
     'version': 'arXiv v1, 21 Jan 2026 (only version)', 'url': 'https://arxiv.org/abs/2601.15222v1',
     'quote': ['The proposed approach won the 2025 Abu Dhabi Autonomous Drone Racing Competition (A2RL), outperforming all '
               'competing AI teams and three human world champion pilots in a direct knockout tournament.',
               'Our controller achieved the fastest completion time of 16.56 s, outperforming three world champion-level FPV '
               'pilots.',
               'Second, the vision pipeline heavily relies on the rectangular shape of the gates for both the corner detection '
               'and the localization relative to the gate. In contrast, humans can easily adapt to different gate shapes, with '
               'no training necessary.'],
     'raw_file': R + '2601.15222v1.txt',
     'agent_note': 'The paper behind the harvester\'s news release (r3:26), with the numbers the release lacked: fastest '
                   'completion time 16.56 s against three world-champion-level pilots (organiser RF timing in its Fig. 1). The '
                   'target (human champions) is reached on the named metric (the A2RL 2025 AI-vs-human knockout), confirming the '
                   'harvester. Same event and protocol; an author paper, not independent. The paper itself names the residual '
                   'generality limit (rectangular gates; no detection of other drones, which cost it a crash in the multi-drone '
                   'race).'},
    {'id': 'r3x:14', 'bottleneck': 'r3-B4', 'role': 'x', 'refutes': 'r3-B4', 'contrary': False, 'shows_target_reached': False,
     'source': 'A2RL (ASPIRE / ATRC, the organiser), A2RL Drone Championship Sets the Pace for AI in Autonomous Flight',
     'version': 'organiser news release dated 23 Jan 2026',
     'url': 'https://a2rl.io/news/45/A2RL-Drone-Championship-Sets-the-Pace-for-AI-in-Autonomous-Flight',
     'quote': ['Human FPV pilot Mincham Kim narrowly defeated AI competitor in a decisive Human vs AI finale, in a down-to-the-wire '
               'showdown',
               'World FPV Champion, Minchan Kim, faced TII Racing in a best-of-nine showdown that remained tied at four wins apiece.',
               'In the final run, Kim maintained his lead as the autonomous drone struck a gate and was unable to recover, '
               'securing victory for the human pilot.',
               'recording a benchmark lap time of 12.032 seconds, the quickest achieved across all competitors. MAVLAB followed '
               'closely with a time of 12.832 seconds'],
     'raw_file': R + 'a2rl_news45_drone_championship_2026.txt',
     'agent_note': 'Found while checking whether the 2025 result held. At the next A2RL championship (21-22 Jan 2026) a human '
                   'world champion beat the AI (TII Racing) 5-4 in a best-of-nine, the deciding race lost when the AI struck a '
                   'gate. This does not reopen the bottleneck as scoped (the 2025 target was reached), but it shows parity, '
                   'not dominance: the AI is at the human level in speed (12.032 s AI lap) and still loses on robustness. '
                   '"Mincham" and "Minchan" are the source\'s two spellings.'},

    # ---------------- r3-B5: C2 link reliability and lost-link behaviour
    {'id': 'r3x:15', 'bottleneck': 'r3-B5', 'role': 'x', 'refutes': 'r3-B5', 'contrary': True, 'shows_target_reached': True,
     'source': 'Nokia, Controlling drones over cellular networks (white paper; vendor statement)',
     'version': 'white paper, (c) 2023 Nokia (PDF dated 27 Feb 2023); pre-2025',
     'url': 'https://www.nokia.com/asset/f/210537/',
     'quote': ['This can be seen from figure 2, which shows the results from measurements taken of a drone flying in an urban '
               'environment during busy hour at 40 m height while being connected to two live LTE networks. The reliability '
               'measure shown is based on the number of packets in uplink and downlink that are received correctly within the '
               '50 ms delay budget at the application layer.',
               'It can be seen that the LTE networks (operator 1 and operator 2), although not optimized for devices in the air, '
               'can deliver high reliabilities (88.5% and 98.5%). While not fulfilling the 3GPP Release 15 requirement of 99.9%, a '
               'simple enhancement can achieve this standard. By simultaneously connecting to both networks and sending the data '
               'packets over each of them, 99.99% reliability is achieved'],
     'raw_file': R + 'nokia_controlling-drones-over-cellular-networks.txt',
     'agent_note': 'On the harvester\'s named metric (C2 packet reliability over commercial networks against 99.9% within a '
                   'latency bound), a flying drone reached 99.99% of packets within 50 ms (a stricter bound than the sub-100 ms '
                   'target) by packet duplication over two live LTE operators; each single operator missed (88.5%, 98.5%), as the '
                   'harvester\'s 2026 single-link measurements do. How it differs: a vendor white paper (2023, before the 2025-26 '
                   'window the declaration prefers), one urban flight at 40 m, details only in a video, the flight date not given. '
                   'It is the redundancy family the harvester lists in B-d ("assumes the links do not fail together"), and here '
                   'they did not. The jammed-spectrum half of r3-B5 is untouched by it.'},
    {'id': 'r3x:16', 'bottleneck': 'r3-B5', 'role': 'x', 'refutes': 'r3-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'Baltaci, Meer, Ozger, Cavdar & Schupke (KTH, Aalborg, Airbus), Multi-Connectivity for UAVs: A Measurement Study '
               'of Integrating Cellular, Aerial Mesh, and LEO Satellite Links',
     'version': 'arXiv v1, 30 Apr 2026 (only version); accepted at IEEE EuCNC', 'url': 'https://arxiv.org/abs/2604.27640v1',
     'quote': ['we find that aggregation can preserve end-to-end connectivity under severe link outages. However, large round-trip '
               'time (RTT) heterogeneity amplifies packet reordering, leading to substantial receiver-side buffering and bursty '
               'delivery.',
               'These effects cause real-time streaming to violate delay constraints, including cases where aggregate capacity is '
               'sufficient.'],
     'raw_file': R + '2604.27640v1.txt',
     'agent_note': 'A 2026 flight measurement that partly contradicts and partly supports the harvester. Against: multi-link '
                   'aggregation (cellular + aerial mesh + LEO) kept end-to-end connectivity through severe single-link outages, '
                   'so link loss as such is addressable by redundancy. For: with lossless in-order multipath (MPTCP) the latency '
                   'bound was violated. Its reframing (connectivity continuity is not service continuity) is a misframing '
                   'argument about the harvester\'s packet-delivery metric, but no number against 99.9% is given.'},
    {'id': 'r3x:17', 'bottleneck': 'r3-B5', 'role': 'x', 'refutes': 'r3-B5', 'contrary': True, 'shows_target_reached': False,
     'source': 'FAA and TSA, Part 108 NPRM (C2 assessment) - the harvester\'s source, re-read',
     'version': '90 FR 38212, 7 Aug 2025 (proposed rule)', 'url': 'https://www.govinfo.gov/content/pkg/FR-2025-08-07/pdf/2025-14992.pdf',
     'quote': ['Based on current research and operational approvals of BVLOS operations, FAA has seen C2 metrics that include, but '
               'are not limited to, link accessibility, latency of link, and operational processes in the event of lost link. FAA '
               'expects that work performed by industry consensus standards bodies will refine the key metrics for C2 over time.',
               'As such, the operator would need to do an assessment of how link latency and intermittent lost link may impact '
               'the safety of their operation and produce mitigation protocols in these instances to maintain a low-risk '
               'operation.'],
     'raw_file': H + 'FR-2025-14992.txt',
     'agent_note': 'A misframing argument from the harvester\'s own regulator source. The US proposal sets no numeric C2 '
                   'reliability requirement: it expects intermittent lost link and asks for an assessment and mitigations (with '
                   'a predetermined action on timeout, r3:34). The 99.9% / sub-100 ms target the harvester uses is a 3GPP service '
                   'figure quoted through a paper, not a BVLOS rule, and the FAA ties the C2 assessment to "operational approvals '
                   'of BVLOS operations" that already exist. It does not show the target reached; it questions whether it is the '
                   'target that gates BVLOS.'},
    {'id': 'r3x:18', 'bottleneck': 'r3-B5', 'role': 'x', 'refutes': 'r3-B5', 'contrary': False, 'shows_target_reached': False,
     'source': 'Chintareddy et al., UAV connectivity (Sec. 5.1) - the harvester\'s source, re-read',
     'version': 'arXiv v2, 28 May 2026', 'url': 'https://arxiv.org/abs/2605.27755v2',
     'quote': ['with approximately 80% of measurement data falling under the 150 ms threshold.',
               'The cellular network, while exhibiting higher latency, maintains competitive packet delivery reliability (99.66%)'],
     'raw_file': H + '2605.27755v2.txt',
     'agent_note': 'Re-check of r3:33. (1) The source is internally inconsistent: Table 1 gives cellular delivery 99.44% '
                   '(5130/5159), the dual-connectivity paragraph gives 99.66%; the harvester used the table value without noting '
                   'the other. Either is below 99.9%, so the reading holds. (2) The source says "approximately 80%" of LTE RTTs '
                   'fall under 150 ms; the harvester\'s "at least 20% of LTE RTTs exceed 150 ms" turns an approximation into a '
                   'bound. (3) The counts are small (29 and 25 lost packets), so the loss rates carry wide uncertainty; the '
                   'gap to 0.1% is still several-fold.'},

    # ---------------- r3-B6: BVLOS detect-and-avoid of non-cooperative aircraft
    {'id': 'r3x:19', 'bottleneck': 'r3-B6', 'role': 'x', 'refutes': 'r3-B6', 'contrary': True, 'shows_target_reached': False,
     'source': 'Amazon, Amazon drones: Prime Air expands drone deliveries after FAA approval (company statement)',
     'version': 'article dated 30 May 2024 (pre-2025)',
     'url': 'https://www.aboutamazon.com/news/transportation/amazon-drone-prime-air-expanded-delivery-faa-approval',
     'quote': ['To obtain this permission, we developed a BVLOS strategy, including an onboard detect-and-avoid technology.',
               'We then conducted flight demonstrations in the presence of FAA inspectors to show our system works in real-world '
               'scenarios—we flew in the presence of real planes, helicopters, and a hot air balloon to demonstrate how the drone '
               'safely navigated away from each of them.',
               'After reviewing this information and observing the technology in action at our test site, the FAA provided Amazon '
               'Prime Air with BVLOS approval.'],
     'raw_file': R + 'amazon_prime-air_faa-approval.txt',
     'agent_note': 'A deployed onboard DAA for a small UAS, approved by the FAA for BVLOS after flight demonstrations against '
                   'real non-cooperative traffic (a hot air balloon among them). It contradicts the harvester\'s B-b reading (DLR, '
                   'r3:41) that no small-UAS approach has passed "from prototype experiments to robust, safe, standardized, and '
                   'secure subsystems" in its strong form: at least one onboard system is operationally approved. It does not '
                   'show the target reached: no risk ratio is published, the approval is an operator-specific FAA decision (not a '
                   'standard), and the statement is the company\'s.'},
    {'id': 'r3x:20', 'bottleneck': 'r3-B6', 'role': 'x', 'refutes': 'r3-B6', 'contrary': True, 'shows_target_reached': False,
     'source': 'Amazon, Amazon pushes for safe and expanded drone delivery with enhanced standards in FAA\'s proposed regulations '
               '(company statement on its Part 108 comments)',
     'version': 'article dated 9 Dec 2025',
     'url': 'https://www.aboutamazon.com/news/policy-news-views/amazon-drone-regulation-comments',
     'quote': ['At Amazon Prime Air, we meet this requirement through our sophisticated onboard computer vision system, which has '
               'been proven to detect all types of aircraft—from planes and helicopters to balloons and paragliders.',
               'As long as these approaches can be demonstrated to be more effective than a human at detecting aircraft, they '
               'should be evaluated and approved and put into service.',
               'We’ve asked FAA to close a critical safety gap by requiring all crewed aircraft that operate at low altitude '
               '(below 500 feet above ground level) to be electronically conspicuous'],
     'raw_file': R + 'amazon_drone-regulation-comments.txt',
     'agent_note': 'A 2025 operator statement that its onboard non-cooperative DAA is in service and "proven to detect all types '
                   'of aircraft", and a proposed yardstick ("more effective than a human") that ViSafe\'s E1-E3 risk ratios already '
                   'beat against the modelled human own-only baseline (r3:46/r3:47, cross-document). Also the same reframing as '
                   'r3:52 (make every low-altitude aircraft electronically conspicuous). It does not show the target reached: '
                   '"proven to detect" is a company claim with no risk ratio, detection is not avoidance, and no NMAC RR <= 0.3 is '
                   'shown.'},
    {'id': 'r3x:21', 'bottleneck': 'r3-B6', 'role': 'x', 'refutes': 'r3-B6', 'contrary': False, 'shows_target_reached': False,
     'source': 'Air Line Pilots Association (ALPA), comment on Zipline petition to amend Exemption No. 19111C, Docket FAA-2020-0499 '
               '(regulations.gov FAA-2020-0499-0043, attachment 1)',
     'version': 'letter dated 12 Aug 2024 (pre-2025)',
     'url': 'https://downloads.regulations.gov/FAA-2020-0499-0043/attachment_1.pdf',
     'quote': ['Zipline has proposed operating its Unmanned Aircraft System (UAS) using a proprietary Automatic Dependent '
               'Surveillance-Broadcast (ADS-B) and an acoustic Detect And Avoid (DAA) system to scan for aircraft and initiate an '
               'avoidance maneuver as needed.',
               'Without adequate knowledge of Zipline Inc.’s acoustic and ADS-B In DAA systems, it is hard to evaluate this '
               'system by NAS stakeholders thoroughly.',
               'The PE does not state information confirming the application of an FAA-approved DAA/ACAS standard'],
     'raw_file': R + 'regulations_FAA-2020-0499-0043_att1.txt',
     'agent_note': 'The other side of r3x:19-20: deployed onboard DAA systems (Zipline\'s acoustic DAA here) are proprietary, and '
                   'their performance evidence is not public; the airline pilots\' union says it cannot evaluate them and that no '
                   'FAA-approved DAA/ACAS standard is shown. So "deployed" does not mean "shown to meet the risk-ratio target", '
                   'which supports the harvester\'s reading that public evidence against the target is missing.'},
    {'id': 'r3x:22', 'bottleneck': 'r3-B6', 'role': 'x', 'refutes': 'r3-B6', 'contrary': True, 'shows_target_reached': False,
     'source': 'UK CAA, CAP 3015 v2 (Ch. 9; references) - the harvester\'s source, re-read',
     'version': 'Second edition September 2026', 'url': 'https://www.caa.co.uk/publication/download/22551',
     'quote': ['While existing standards such as RTCA DO-396, EUROCAE ED-330, ASTM F3442-25, and RTCA DO-365 provide important '
               'verification of DAA system performance, their primary focus is on demonstrating compliance with minimum '
               'equipment performance requirements.',
               'However, compliance with equipment standards alone does not necessarily demonstrate that a DAA capability '
               'performs safely within a specific operational concept',
               'FAA TCAS Programme Office, Airborne Collision Avoidance System sXu Operational Validation Report, '
               'ACAS_RPS_22_016_V4R2-DO-396, Sept 1st, 2022'],
     'raw_file': H + 'caa_CAP3015_v2.txt',
     'agent_note': 'The regulator lists published DAA standards for small UAS (ASTM F3442-25) and a standardised avoidance logic '
                   '(ACAS sXu, RTCA DO-396, with an FAA operational validation report of 2022), which weakens the strong form of '
                   'the DLR statement (r3:41) that nothing small-UAS is standardised. The regulator also says equipment compliance '
                   'is not enough for an operation, so the open part is the operational demonstration of a whole system '
                   '(sensor + logic) against the logic risk ratio, not the existence of standards. No risk ratio is shown here.'},

    # ---------------- r3-B7: counter-UAS tracking and non-destructive interception
    {'id': 'r3x:23', 'bottleneck': 'r3-B7', 'role': 'x', 'refutes': 'r3-B7', 'contrary': True, 'shows_target_reached': False,
     'source': 'Fortem Technologies, Fortem\'s AI-powered SkyDome Neutralizes Drone Swarm With Zero Collateral Damage (press '
               'release)',
     'version': 'press release dated 4 Feb 2026 (company statement)',
     'url': 'https://fortemtech.com/press-releases/2026-02-04-fortem-s-ai-powered-skydome-neutralizes-drone-swarm-with-zero-collateral-damage/',
     'quote': ['today announced it has completed what it believes is the first autonomous 5-vs-5 drone intercept with safe capture '
               'of every target',
               'intercepted and safely captured five incoming drones, each flying an autonomous, pre-programmed attack mission. '
               'SkyDome autonomously planned, sequenced, and coordinated all five intercepts, with no human involvement.',
               'That maturity was underscored last month when the Pentagon’s counter-UAS task force selected DroneHunter as its '
               'first operational purchase under the Replicator-2 initiative',
               'Fortem is the only company authorized to deploy a drone-on-drone kinetic interceptor in U.S. airspace'],
     'raw_file': R + 'fortem_pr_2026-02-04_skydome_swarm.txt',
     'agent_note': 'A deployed system in the family SPRIND itself seeks ("guided interception ... safe retrieval", r3:59): '
                   'autonomous, radar-guided net capture with no human involvement, 5 of 5 targets captured in a live test, and a '
                   'US DoD operational purchase (Jan 2026). It does not show the SPRIND target reached: the target speed and mass '
                   '(200 km/h, 25 kg) are not stated for the test, the result is the company\'s own, and Fortem calls its '
                   'interceptor "kinetic", whereas SPRIND specifies "without kinetic means".'},
    {'id': 'r3x:24', 'bottleneck': 'r3-B7', 'role': 'x', 'refutes': 'r3-B7', 'contrary': True, 'shows_target_reached': False,
     'source': 'Fortem Technologies, DroneHunter F700 product page (company statement)',
     'version': 'live product page fetched 2026-09-30 (no date shown)', 'url': 'https://fortemtech.com/products/dronehunter-f700/',
     'quote': ['With more than 4,500 drone captures, the DroneHunter® F700 is a counter-UAS weapon with real field success.',
               'It capably mitigates both Group-1 and large Group-2 drones.',
               'Statistically, only 15% of target drones evade the first shot… and a second shot is usually ready to follow.'],
     'raw_file': R + 'fortem_dronehunter-f700.txt',
     'agent_note': 'Company claims for the same fielded system: more than 4,500 captures, Group-1 and large Group-2 targets (the '
                   'US Group 2 class reaches about 25 kg, SPRIND\'s mass limit; the class definition is not in this source), and an '
                   '85% first-shot capture rate. Against the SPRIND specification ("consistently, reproducibly, and in line with '
                   'the specifications"; 200 km/h) it is not shown: no speed envelope, no independent test, and the captures\' '
                   'conditions are not described. It is contrary evidence that autonomous non-destructive capture is deployed, '
                   'not that the specification is met. It does not bear on the CST tracking metric.'},
]

CHECKS = [
    {'bottleneck': 'r3-B1',
     'searched': ['WebSearch: hydrogen multirotor drone world record 188 km non-stop flight November 2025',
                  'WebSearch: guinnessworldrecords.com "hydrogen-powered multirotor" longest distance flight Tianmushan (no Guinness '
                  'page found; state-media copies fetched)',
                  'WebSearch: Amprius SiCore 450 Wh/kg cells UAS drone flight time 2025 press release',
                  'WebSearch: DJI Matrice 400 max flight time 59 minutes specs payload',
                  'Fetched: China Daily and english.scio.gov.cn (Xinhua, 12 Dec 2025), Amprius press release (2 Sep 2026), DJI '
                  'Matrice 400 specification page',
                  'Harvester raw texts re-read: 2510.01348v2 (Table I, Sec. IV-A, Lessons learned), 2503.16587v1 (Results, '
                  'Conclusions)'],
     'finding': 'NOT OPEN by the table rule on the range-per-battery metric, CONTESTED in substance. A commercial battery-electric '
                'multirotor is specified at 49 km on one battery with a 10.67 kg camera-payload configuration (DJI Matrice 400, '
                'manufacturer figure, 17 m/s, windless, to 0%), 5.4x the 9 km course; a hydrogen multirotor flew 188.605 km in more '
                'than four hours (Nov 2025, state media reporting Guinness); silicon-anode lithium-ion cells are claimed at 500 '
                'Wh/kg (company, availability Q4 2026). What stays open: flight duration of battery multirotors is still tens of '
                'minutes (59 min at best here), no non-lithium drop-in beats lithium on specific power for hover, and at the '
                'SPRIN-D winner\'s localization-limited 1.40 m/s even 59 min covers only about 5 km. The SPRIN-D 15% is that '
                'team\'s platform and speed, not the frontier of battery endurance.',
     'harvester_errors': ['r3:3 passes through the source\'s sentence "Flights exceeding 1 km were consistently terminated due to '
                          'battery constraints" although the source\'s own Table I shows that of the three competition flights over '
                          '1 km only one (239, 1371 m) ended on low battery; 206 (1023 m) ended on a software issue and 232 (1256 m) '
                          'on a hardware failsafe. The harvester\'s own count ("3 of the 6 competition flights ended on low '
                          'battery") is right; the quoted generalisation is overstated.',
                          'The target "9 km course on one battery" (range per flight / course = 15%, "about 6.6 battery-limited '
                          'flights per course") is the harvester\'s construction: the programme gave a 2 h slot to "visit as many '
                          'waypoints as possible", with no one-battery requirement.',
                          'Range per battery is attributed to energy although the source names speed, capped by its local-map size, '
                          'as what limited range; the 977 s flight (16.3 min) is ordinary endurance for the class. The harvester '
                          'notes this under r3-B2 but not under r3-B1.']},
    {'bottleneck': 'r3-B2',
     'searched': ['WebSearch: SPRIND Fully Autonomous Flight 2.0 winner HERMES Klagenfurt GNSS-denied arXiv 2026',
                  'WebSearch: University of Klagenfurt HERMES SPRIND Fully Autonomous Flight 2.0 final August 2026',
                  'WebSearch: arXiv 2026 GNSS-denied UAV long-range flight test tens of kilometers visual localization error drift',
                  'WebSearch: visual navigation GNSS-denied drone flight test 2025 kilometers position error percent of distance',
                  'WebSearch: arXiv 2025 2026 UAV absolute visual localization satellite imagery low altitude ... real-world onboard',
                  'WebSearch: arXiv 2026 multirotor GNSS-denied navigation real flight over 5 km low altitude onboard map matching',
                  'WebSearch: Satellite Navigation 2025 GNSS-denied UAV navigation review; NaviLoc (Drones 2026; MDPI not fetched)',
                  'WebSearch: drone flew without GPS ... 2025 2026 announcement; Northrop Grumman Lumberjack SandboxAQ AQNav',
                  'Fetched: AAU news (11 Sep 2026), CTU news (11 Sep 2026), Northrop Grumman release (9 Sep 2026), arXiv '
                  '2503.10692v2 (AnyVisLoc) PDF; abstracts of 2603.22153v3, 2609.28225v1 screened',
                  'Not reached: UAV Navigation-Grupo Oesia VNS01 pages (JavaScript challenge), GPS World article (403 to curl; '
                  'read by WebFetch only, not used)',
                  'Harvester raw text re-read: 2510.01348v2 (Table I terminations; Sec. IV-B)'],
     'finding': 'CONTESTED (misframing), not shown closed. No 2025-26 source reports a GNSS-free small drone completing a 9 km '
                'low-altitude course, and the 2025-26 SPRIND edition published no metrics. Against the reading: in the harvester\'s '
                'own benchmark no competition flight ended on localization drift (terminations: test finished, software, hardware '
                'failsafe, low battery), with method RMSE 6-11 m; the programme\'s 2026 final set 60-minute area missions, not a '
                'traverse, and its winner calls its GNSS-free navigation "ready for the real world" (no numbers); magnetic '
                'navigation flew on a Group 3 UAS (no numbers); low-altitude (30-300 m) absolute visual localization reaches 74.1% '
                'within 5 m on real imagery. What stays open: a published, measured kilometre-scale GNSS-free flight below 25 m '
                'AGL over unseen terrain, especially over structureless ground.',
     'harvester_errors': ['r3-B2 gap_note repeats "flights over 1 km ended on battery, not drift"; Table I shows one of three flights '
                          'over 1 km ended on battery (see r3-B1). The correct and stronger statement is that no flight ended on '
                          'drift.',
                          'The harvester counts the 2025-26 SPRIND edition only as "no metrics published"; it did not record that '
                          'the edition changed the task from a 9 km traverse to 60-minute area missions, which bears on whether '
                          'the 9 km course is still the programme\'s target.']},
    {'bottleneck': 'r3-B3',
     'searched': ['WebSearch: arXiv 2025 2026 UAV detection adverse weather fog real data benchmark robust detector matches '
                  'clear-weather accuracy',
                  'WebSearch: radar detect and avoid drone fog rain all-weather detection range unaffected 2025 flight test',
                  'WebSearch: arXiv 2025 camera radar fusion drone detection adverse weather fog thermal infrared anti-UAV',
                  'Fetched: arXiv 2608.16191v1 (SDV-W) PDF; abstract of 2605.12608v3 (Clear2Fog, road scenes) screened',
                  'Harvester raw text re-read: 2607.05467v1 (Table 3 parsed in full; Sec. 5-6)'],
     'finding': 'OPEN (double-checked): no contrary claim found. No 2025-26 source reports drone-view or anti-UAV detection or '
                'tracking in real fog at clear-weather performance; a 2026 drone-detection paper corroborates the problem (fog '
                'lowers mAP@0.25 by 6.2 pp and raises misses by 12.7 pp on matched synthetic scenes) and again names the lack of '
                'real adverse-weather evaluation data. Radar or acoustic sensing as a fog-proof alternative (a possible misframing '
                'argument) appears only in vendor blogs and trade press, with no primary 2025-26 measurement found. The '
                'harvester\'s numbers are right; the V10 residual is partly sequence difficulty (clean oracle 0.321), not fog.',
     'harvester_errors': ['None in the numbers (Table 3 parsed in full; the per-video best values match). Framing only: Video 10\'s '
                          'low absolute MOTA is not fog-caused (clean 0.321, light fog up to 0.368), so "open on the worst '
                          'sequences" is carried by the heavy-fog relative drop (V02 0.229; V10 0.179 vs 0.321), not by V10\'s level.']},
    {'bottleneck': 'r3-B4',
     'searched': ['WebSearch: A2RL drone racing season 2 2026 AI versus human pilots results autonomous drone',
                  'WebSearch: arXiv MAVLab A2RL 2025 champion-level monocular drone racing guidance and control network paper',
                  'Fetched: arXiv 2601.15222v1 (MonoRace) PDF; A2RL organiser release (23 Jan 2026); ADNEC pre-event release '
                  'screened and dropped',
                  'Harvester raw texts re-read: tudelft_2025 release, 2510.14783v1 (SkyDreamer)'],
     'finding': 'NOT OPEN, as the harvester read it. The team\'s own paper confirms the 2025 A2RL result with numbers: the AI beat '
                'three world-champion-level pilots, fastest completion 16.56 s, onboard monocular camera + IMU, speeds up to 100 '
                'km/h. For fairness: at the next A2RL championship (Jan 2026) a human world champion beat the AI 5-4 in a '
                'best-of-nine after the AI struck a gate, so the state is parity, not dominance; and generality (gate shapes, '
                'other drones, unstructured settings) stays open with no metric against a target.',
     'harvester_errors': []},
    {'bottleneck': 'r3-B5',
     'searched': ['WebSearch: drone command and control link LTE 5G flight measurement 2025 reliability 99.9% achieved',
                  'WebSearch: arXiv 2025 2026 multi-link UAV C2 redundancy cellular satellite measured availability 99.99 BVLOS',
                  'WebSearch: UAV flight measurement multi-operator packet duplication cellular C2 reliability 99.9% within 50 ms',
                  'WebSearch: uAvionix SkyLine multi-link C2 BVLOS trial Wales December 2025 (company page 403 to curl)',
                  'WebSearch: Zipline OR Wing 2026 deliveries milestone BVLOS',
                  'Fetched: Nokia white paper (2023), arXiv 2604.27640v1 PDF; screened and dropped: arXiv 1907.12307 (2019 lab '
                  'setup), 2111.07637v3 (2021 simulation), 2604.04044v1 (2026 requirements survey)',
                  'Harvester raw texts re-read: 2605.27755v2 (Sec. 5.1, Table 1), FR-2025-14992 (C2 assessment, § 108.815)'],
     'finding': 'NOT OPEN by the table rule on the civil C2 metric, CONTESTED in substance. A vendor measurement on a flying drone '
                'reached 99.99% of packets within 50 ms by duplicating over two live LTE operators (Nokia, 2023; pre-2025, one '
                'urban flight at 40 m), meeting the 99.9% / sub-100 ms target that single links miss; a 2026 KTH/Airbus flight '
                'study shows multi-link aggregation keeps connectivity through severe outages but can break latency bounds; and the '
                'FAA NPRM sets no numeric C2 reliability and expects intermittent lost link to be mitigated, so the 99.9% target '
                'is a 3GPP service figure, not the BVLOS gate. What stays open: single commercial links (99.3-99.4% in 2026), '
                'latency under multipath, and the jammed-spectrum half, which none of these sources touches.',
     'harvester_errors': ['r3:33 note: "at least 20% of LTE RTTs exceed 150 ms" turns the source\'s "approximately 80% ... under the '
                          '150 ms threshold" into a bound; "about 20%" is what the source supports. Minor.',
                          'The source gives cellular packet delivery as 99.44% (Table 1) and as 99.66% (dual-connectivity '
                          'paragraph); the harvester used 99.44% without noting the inconsistency. Either is below 99.9%. Minor.',
                          'The problem statement ("a command-and-control link that commercial networks do not deliver at the '
                          'required reliability") treats 99.9% as required; the harvester\'s own regulator source (FAA NPRM) sets '
                          'no numeric C2 requirement. Framing.']},
    {'bottleneck': 'r3-B6',
     'searched': ['WebSearch: onboard detect and avoid small UAS meets ASTM F3442 risk ratio non-cooperative 2025 2026 flight test',
                  'WebSearch: Amazon Prime Air MK30 detect and avoid system FAA approval beyond visual line of sight statement',
                  'WebSearch: UK CAA 2026 approves BVLOS operation detect and avoid onboard non-cooperative first authorisation',
                  'WebSearch: Zipline acoustic detect and avoid aircraft detection range FAA approval onboard DAA statement',
                  'WebSearch: ACAS sXu risk ratio NMAC non-cooperative intruder simulation results small UAS 2025',
                  'WebSearch: arXiv 2025 2026 detect and avoid small UAS radar risk ratio encounter simulation meets 0.3',
                  'Fetched: Amazon statements (30 May 2024; 9 Dec 2025), ALPA comment in FAA-2020-0499 (12 Aug 2024); DTIC '
                  'AD1197090 returned an HTML interstitial (dropped)',
                  'Harvester raw texts re-read: caa_CAP3015_v2 (Ch. 9, references), A65 report (Table 16 context: modelled GA '
                  'pilot see-and-avoid, confirmed)'],
     'finding': 'CONTESTED. Deployed onboard DAA exists: Amazon Prime Air received FAA BVLOS approval in 2024 after flight '
                'demonstrations against real planes, helicopters and a balloon, and in Dec 2025 states its onboard vision DAA is '
                'in service; Zipline flies an acoustic DAA under FAA exemption; standards for small-UAS DAA (ASTM F3442-25) and a '
                'standardised logic (ACAS sXu, DO-396, validated 2022) exist. None of these shows the named target: no deployed '
                'system publishes a non-cooperative NMAC risk ratio <= 0.3, ALPA says Zipline\'s DAA performance evidence is not '
                'available to stakeholders, and the UK regulator says equipment standards alone do not demonstrate operational '
                'safety. The open part is public evidence that a whole small-UAS DAA meets the risk ratio, not the existence of '
                'systems.',
     'harvester_errors': ['The problem text ("no small-UAS approach has passed from prototype to a standardised subsystem") and B-b '
                          '(DLR, r3:41) are read without the FAA-approved onboard DAA in service since 2024 (Amazon) and 2023 '
                          '(Zipline), or ACAS sXu (DO-396) and ASTM F3442-25; "standardised" is defensible, "prototype" is '
                          'overstated. Omission, not a misquote.']},
    {'bottleneck': 'r3-B7',
     'searched': ['WebSearch: "CST Anti-UAV" tracker 2026 state accuracy mSA new state of the art',
                  'WebSearch: 4th Anti-UAV challenge 2025 results tracking accuracy winning team (CVPR 2025 workshop)',
                  'WebSearch: arXiv 2026 thermal infrared tiny UAV tracking CST Anti-UAV benchmark results outperform GlobalTrack',
                  'WebSearch: Fortem DroneHunter F700 autonomous net capture 2025 2026 deployed',
                  'Fetched: Fortem press release (4 Feb 2026) and product page; CST Anti-UAV GitHub README (no leaderboard); '
                  'abstracts of 2607.26511v1, 2605.20667v1 screened',
                  'Not reached: JIATF-401 2026 C-sUAS Quick Reference Guide (media.defense.gov, 403)',
                  'Harvester raw text re-read: 2507.23473v2 (Table 3)'],
     'finding': 'CONTESTED on the interception half; OPEN on the tracking half. A fielded autonomous, radar-guided, non-destructive '
                '(net-capture) interceptor exists and was bought by the US DoD counter-UAS task force (Fortem DroneHunter F700: '
                'more than 4,500 captures, an autonomous 5-vs-5 swarm capture in Feb 2026, Group-1 and large Group-2 targets; '
                'company statements). It is not shown to meet SPRIND\'s specification (200 km/h, 25 kg, "without kinetic means", '
                'reproducibly; Fortem calls its interceptor kinetic). On CST Anti-UAV no later tracker result above 35.92 mSA was '
                'found. Misframing note: fielded counter-UAS guides by radar, so a thermal single-object tracking score is a '
                'proxy, not the operational metric.',
     'harvester_errors': ['The "oracle SA 100" target and the 64.08-point gap are the harvester\'s construction, not a programme, '
                          'regulatory or human target; the meaningful same-paper reference is the 67.69 reached on Anti-UAV410, '
                          'which the harvester also reports. Framing.',
                          'The problem text ("no autonomous civilian soft-kill system has met a public specification") is right '
                          'for SPRIND\'s specification but omits a fielded autonomous net-capture system (Fortem). Omission.']},
]
