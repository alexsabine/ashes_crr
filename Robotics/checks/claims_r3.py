"""ROB1 stage 1, family R3 (Robotics/DECLARATION.md): drones. Endurance and energy, GNSS-denied state estimation and drift,
perception in adverse conditions, agile flight, command-and-control (C2) link loss and lost-link behaviour (including
jamming), beyond-visual-line-of-sight (BVLOS) detect-and-avoid (FAA Part 108 NPRM, EASA SORA 2.5, UK CAA CAP 3015), and
counter-UAS.

Every source was fetched on 2026-09-30 through the session proxy with curl (TLS verification on). Quotes are copied from the
text extracted from the fetched file: PDFs by pymupdf 1.28.2 (`page.get_text()`, pages joined by newlines); HTML pages by
BeautifulSoup 4 (`get_text('\n')` after removing script/style/noscript/svg, runs of spaces and blank lines collapsed); the one
JSON file (the Federal Register API listing of docket FAA-2025-1908) is used as fetched. Raw files live outside the
repository under /tmp/claude-0/rob_src/ (`raw_file` is relative to that root; the fetched originals are in r3/src/); their
sha256 is in /tmp/claude-0/rob_src/r3/SHA256SUMS.txt and in the dossier docs/citations/rob1_r3_2026-09-30.md. Table rows are
quoted as the extractor emitted them, cell by cell in reading order; a quote containing "[...]" skips a page header that the
extractor placed inside the sentence. To be checked by Robotics/checks/verify.py; at harvest time a scratch copy of
Open_Bottlenecks/checks/verify.py pointed at this file and this root read "quotes found verbatim: 150 of 150 (claims 60; raw
files 22, missing 0)"; with one number altered (99.44% -> 99.54% in r3:33) it read 149 of 150, as it should.

Roles (DECLARATION.md stage 1): a = the problem stated; b = a 2025-26 statement that it is open, unsolved or a main challenge;
c = the best reported result on a named benchmark or metric against the target (numbers quoted; the gap is computed in
`agent_note` and in BOTTLENECKS); d = the method families tried and the assumption each makes (about time, clocks,
boundaries, interruptions, memory or tuning). `agent_note` is the agent's reading, not the source's words. Numbers from
different sources are not comparable unless a note says the protocol is shared; where a target and a best result come from
different documents, the note says so. Regulator texts state requirements or proposals, not measurements; an NPRM is a
proposal, not a rule (no final Part 108 rule was listed in docket FAA-2025-1908 on 2026-09-30). One source (RUSI) is a
think-tank field study of a war; it is used only for what it states about link jamming and its workarounds.
"""

R = 'r3/txt/'

CLAIMS = [
    # ---------------- r3-B1: endurance and energy of small battery-electric multirotors
    {'id': 'r3:1', 'bottleneck': 'r3-B1', 'role': 'a',
     'source': 'Williamson, Rao, Segura, Wylie & Hall, Prospects for endurance augmentation of small unmanned systems using '
               'butane-fueled thermoelectric generation',
     'version': 'arXiv v1, 20 Mar 2025 (only version)', 'url': 'https://arxiv.org/abs/2503.16587v1',
     'quote': ['One particularly vexing weakness of small drones (especially multicopters) happens to be their limited '
               'endurance. In general, a high performing small multicopter drone able to carry a minimally useful payload is '
               'able to stay aloft for around 10-30 minutes.'],
     'raw_file': R + '2503.16587v1.txt',
     'agent_note': 'The problem stated, with the typical figure (10-30 min aloft with a useful payload).'},
    {'id': 'r3:2', 'bottleneck': 'r3-B1', 'role': 'b',
     'source': 'Williamson et al., butane-fueled thermoelectric generation (abstract)',
     'version': 'arXiv v1, 20 Mar 2025', 'url': 'https://arxiv.org/abs/2503.16587v1',
     'quote': ['The combination of the prototype performance and modeling suggests that endurance augmentation remains a '
               'difficult technical challenge with no clear immediate remedy despite many expectant alternatives.'],
     'raw_file': R + '2503.16587v1.txt',
     'agent_note': '2025 statement that endurance augmentation of small drones is open.'},
    {'id': 'r3:3', 'bottleneck': 'r3-B1', 'role': 'c',
     'source': 'Werner, Capek, Musil, Franek, Baca & Saska, Kilometer-Scale GNSS-Denied UAV Navigation via Heightmap Gradients: '
               'A Winning System from the SPRIN-D Challenge (Sec. IV, Table I)',
     'version': 'arXiv v2, 25 May 2026 (v1 1 Oct 2025)', 'url': 'https://arxiv.org/abs/2510.01348v2',
     'quote': ['On the final day of the competition, a 9 km course was defined by a sequence of waypoints distributed across '
               'all three environments (printed on a paper map distributed 30 minutes prior the mission). Each team had 2 '
               'hours to demonstrate the capability of their system and visit as many waypoints as possible.',
               'Flights exceeding 1 km were consistently terminated due to battery constraints, rather than localization '
               'drift, indicating hardware limitations as the primary bottleneck.',
               'Flight ID Length [m] Time [s] RMSEodom [m] RMSEmethod [m] Waypoints detected Area Termination',
               '239† 1371 977 8 9 4/4 forest low battery',
               '242† 939 622 9 11 2/3 urban/open field low battery',
               '208† 872 500 14 11 1/1 urban/open field low battery'],
     'raw_file': R + '2510.01348v2.txt',
     'agent_note': 'Programme task (SPRIN-D Funke 2024): a 9 km course within 2 h. The winning team\'s longest competition flight '
                   'was 1371 m (header order: length 1371 m, time 977 s; the caption lists time before length, the header '
                   'length before time) and ended on low battery; 3 of the 6 competition flights in Table I ended on low '
                   'battery. Longest flight / course = 1371/9000 = 0.152, i.e. about 6.6 flights (battery changes) per course. '
                   'The platform carried LiDAR, cameras and an onboard computer (total mass below 25 kg), so this is endurance '
                   'with an autonomy payload, not a bare airframe.'},
    {'id': 'r3:4', 'bottleneck': 'r3-B1', 'role': 'c',
     'source': 'Williamson et al., butane-fueled thermoelectric generation (abstract; Sec. 2; Results)',
     'version': 'arXiv v1, 20 Mar 2025', 'url': 'https://arxiv.org/abs/2503.16587v1',
     'quote': ['from their current maximum values of 12%, thermoelectric (TE) generator module efficiencies must increase by '
               'over two times to achieve endurance parity with lithium batteries for VTOL multicopters.',
               'Typical values for the specific energies for each are: 150 Wh/kg and 200 Wh/kg, respectively.',
               'Overall, tests demonstrate the prototype generator (at 1.8% device efficiency) possesses specific energy and '
               'power of 30 Wh/kg and 6 W/kg, respectively.'],
     'raw_file': R + '2503.16587v1.txt',
     'agent_note': 'Metric: specific energy of the power source. Target: parity with lithium-ion (200 Wh/kg; lithium-polymer 150 '
                   'Wh/kg). Best measured alternative in this paper: 30 Wh/kg (prototype, 1.8% efficiency) = 0.15 of '
                   'lithium-ion; modelled best module (12%) reaches only parity, and endurance parity for VTOL multicopters '
                   'needs more than 2x the best module efficiency (> 24%). Same paper.'},
    {'id': 'r3:5', 'bottleneck': 'r3-B1', 'role': 'c',
     'source': 'Guinness World Records, Longest remote-controlled (RC) model multirotor/drone flight (duration)',
     'version': 'live record page fetched 2026-09-30 (record set 3 Apr 2019; the page says records are not immediately '
                'published online)',
     'url': 'https://www.guinnessworldrecords.com/world-records/longest-rc-model-multicopter-flight-duration',
     'quote': ['The longest duration RC multicopter flight is 12 hr 7 min 5 sec and was achieved by Metavista Inc. (South Korea) '
               'in Yuseong-gu, Daejeon, South Korea, on 3 April 2019. Metavista Inc. (South Korea) is a liquid hydrogen '
               'specialist.'],
     'raw_file': R + 'gwr_longest-rc-model-multicopter-flight-duration.txt',
     'agent_note': 'CONTRARY evidence recorded for fairness: with liquid hydrogen, a multirotor has flown 12 h 7 min 5 s (2019, '
                   'no payload or mission stated). Duration is therefore not bounded for every energy carrier; the bottleneck '
                   'as scoped here is battery-electric small multirotors carrying a useful or autonomy payload. Trade-press '
                   'reports of a 2025 hydrogen multirotor distance record (188.6 km) were found but the article body was not '
                   'served (see dossier), so they are not used.'},
    {'id': 'r3:6', 'bottleneck': 'r3-B1', 'role': 'd',
     'source': 'Williamson et al., butane-fueled thermoelectric generation (Introduction; Discussion)',
     'version': 'arXiv v1, 20 Mar 2025', 'url': 'https://arxiv.org/abs/2503.16587v1',
     'quote': ['To some extent the endurance weakness may be alleviated by employing fixed wing small drones instead, however, '
               'often at the cost of sacrificing hovering maneuverability and the flexibility associated with takeoff and '
               'landing that a VTOL capability affords.',
               'High voltage tethering could be an attractive alternative providing practically endless endurance, but '
               'sacrifices much of its mobility as well as swarming capability due to high voltage line tangling complications.',
               'Inductive charging along powerlines is a strategy that may avoid these limitations, but would require a '
               'peace-time-like infrastructure operation environment typically not reliably assumed during battlefield '
               'operations.'],
     'raw_file': R + '2503.16587v1.txt',
     'agent_note': 'Families: fixed wing (gives up hover), tethering (continuous supply, gives up mobility), power beaming / '
                   'powerline charging (assumes fixed infrastructure that is always there), hydrocarbon or fuel-cell hybrids '
                   '(the paper\'s own route). Each assumes either a fixed mission clock sized to one charge or an uninterrupted '
                   'external supply.'},
    {'id': 'r3:7', 'bottleneck': 'r3-B1', 'role': 'd',
     'source': 'Verraest, Bahnam, Ferede, de Croon & De Wagter, SkyDreamer: Interpretable End-to-End Vision-Based Drone Racing '
               'with Model-Based Reinforcement Learning (abstract)',
     'version': 'arXiv v1, 16 Oct 2025 (only version)', 'url': 'https://arxiv.org/abs/2510.14783v1',
     'quote': ['exhibits robustness to battery depletion by accurately estimating the maximum attainable motor RPM and adjusting '
               'its flight path in real-time.'],
     'raw_file': R + '2510.14783v1.txt',
     'agent_note': 'A control-side family: adapt the flight to the battery\'s state as estimated online (state-indexed), rather '
                   'than plan the flight to a fixed endurance clock. It does not add energy.'},

    # ---------------- r3-B2: GNSS-denied long-range navigation and drift
    {'id': 'r3:8', 'bottleneck': 'r3-B2', 'role': 'a',
     'source': 'Werner et al., SPRIN-D winning system (Introduction)', 'version': 'arXiv v2, 25 May 2026',
     'url': 'https://arxiv.org/abs/2510.01348v2',
     'quote': ['Without GNSS, UAVs typically rely on visual–inertial or LiDAR odometry to navigate a previously unseen '
               'environment. These methods are consistent locally, but accumulate unbounded drift in previously unvisited '
               'areas, where loop closures cannot be used. When flying over kilometer-scale trajectories, this leads to '
               'position errors too large for waypoint-based navigation.'],
     'raw_file': R + '2510.01348v2.txt', 'agent_note': 'The problem stated.'},
    {'id': 'r3:9', 'bottleneck': 'r3-B2', 'role': 'b',
     'source': 'Werner et al., SPRIN-D winning system (Introduction)', 'version': 'arXiv v2, 25 May 2026 (v1 1 Oct 2025)',
     'url': 'https://arxiv.org/abs/2510.01348v2',
     'quote': ['Fully onboard systems that scale to kilometer ranges in diverse unseen environments remain rare, since outdoor '
               'geodata-based drift correction that is both lightweight and robust has not been solved.'],
     'raw_file': R + '2510.01348v2.txt', 'agent_note': '2025-26 statement that the problem is open.'},
    {'id': 'r3:10', 'bottleneck': 'r3-B2', 'role': 'b',
     'source': 'SPRIND (German Federal Agency for Breakthrough Innovation), Funke Fully Autonomous Flight 2.0 page',
     'version': 'live page fetched 2026-09-30 (marked "Funke completed"; no last-updated date)',
     'url': 'https://www.sprind.org/en/actions/challenges/funke-fully-autonomous-flight-2.0',
     'quote': ['The dream of fully autonomous flight is not yet a reality. What is missing are robust systems that can safely '
               'navigate complex environments without GNSS or human intervention.',
               'The challenge: To develop an autonomous flight system that can operate safely without GNSS support or human '
               'control – validated through two clearly defined missions under real-world conditions.'],
     'raw_file': R + 'sprind_funke_fully_autonomous_flight_2.0.txt',
     'agent_note': 'Programme statement of the open problem. The challenge text probably dates from the 2025 call; the page now '
                   'says "Funke completed" and names HERMES (University of Klagenfurt) as winner, with no metrics published. '
                   'The final article (r3:11) is dated 2 Sep 2026.'},
    {'id': 'r3:11', 'bottleneck': 'r3-B2', 'role': 'b',
     'source': 'SPRIND magazine, Final of the SPRIND Funken "Fully Autonomous Flight 2.0" (Decisions from the air)',
     'version': 'magazine article dated 2 Sep 2026 (page shows 9/2/2026)',
     'url': 'https://www.sprind.org/en/words/magazine/fully-autonomous-flight-final',
     'quote': ['At the same time, the finale demonstrated just how difficult it is to make a complex combination of hardware and '
               'software perform reliably on precisely the day it matters.',
               'Conditions during the final week ranged from 17°C and rain to 29°C and intense sunshine. For humans, these are '
               'simply different weather conditions. For a drone, they mean changing thermal conditions, varying visibility, '
               'and different stresses on sensitive electronics.'],
     'raw_file': R + 'sprind_mag_fully-autonomous-flight-final.txt',
     'agent_note': '2026 programme statement on reliability at the final of the second edition; no numbers are published.'},
    {'id': 'r3:12', 'bottleneck': 'r3-B2', 'role': 'c',
     'source': 'Werner et al., SPRIN-D winning system (abstract; Sec. IV-B, IV-C; Table I)', 'version': 'arXiv v2, 25 May 2026',
     'url': 'https://arxiv.org/abs/2510.01348v2',
     'quote': ['which required 9 km long-range waypoint navigation below 25 m AGL (Above Ground Level) without GNSS or prior dense '
               'mapping.',
               'During the actual competition, our system was able to autonomously perform multiple kilometer-scale flights '
               'with overall localization RMSE below 11 m while the compass-aligned odometry had RMSE of up to 53 m.',
               '232† 1256 1021 53 7 1/2 forest failsafe - HW issue',
               'As a result, only us and 2 other teams managed to realize autonomous flights under these demanding conditions '
               'for more than 100 m. The two other teams accumulated critical drift and were not able to reach more than 2 '
               'waypoints.'],
     'raw_file': R + '2510.01348v2.txt',
     'agent_note': 'Benchmark: SPRIN-D Funke Fully Autonomous Flight (Erding, Sep 2024), 9 km GNSS-denied waypoint course below 25 '
                   'm AGL. Best (the winner): longest flight 1371 m (r3:3), localization RMSE below 11 m against odometry up to '
                   '53 m (flight 232: 7 m vs 53 m; ground truth approximate, reconstructed from footage to 0-5 m). Target: the '
                   '9 km course; no flight in Table I exceeds 1.371 km (15% of the course) and the paper does not report the '
                   'course completed. Only 3 of 9 teams flew more than 100 m autonomously. The second edition (2025-26) '
                   'published no metrics.'},
    {'id': 'r3:13', 'bottleneck': 'r3-B2', 'role': 'c',
     'source': 'SPRIND magazine, Pioneers of the sky: SPRIND FUNKE Winners Lead the Way on Fully Autonomous Flight',
     'version': 'magazine article dated 24 Sep 2024 (page shows 9/24/2024)',
     'url': 'https://www.sprind.org/en/words/magazine/fully-autonomous-flight',
     'quote': ['From September 16 to 19, 2024, these teams gathered at the air base in Erding, Bavaria, where they were competing '
               'to demonstrate a system capable of flying fully autonomously over a 9km track without using GPS or manual '
               'control.',
               'Additionally, the drones had to deal with various disruptive factors such as smoke, fog and rain. 27 waypoints '
               'guided the drones through their journey – at the last one, they needed to identify and pick up a package.',
               'The standout winner was Fly4Future, a team spun off from the Technical University of Prague.'],
     'raw_file': R + 'sprind_mag_fully-autonomous-flight.txt',
     'agent_note': 'The programme\'s own statement of the target (9 km track, 27 waypoints, package pick-up at the last, smoke, '
                   'fog and rain) and of the winner, the team whose paper gives the best result in r3:12. Pre-2025 source used '
                   'for the target only.'},
    {'id': 'r3:14', 'bottleneck': 'r3-B2', 'role': 'd',
     'source': 'Werner et al., SPRIN-D winning system (Introduction; Related work; Sec. IV-C)', 'version': 'arXiv v2, 25 May 2026',
     'url': 'https://arxiv.org/abs/2510.01348v2',
     'quote': ['Odometry methods such as VIO and LIO provide local motion estimates, yet accumulate drift that is usually '
               'corrected through loop closures. In real-world missions, e.g. search and rescue, UAVs operate in previously '
               'unseen environments where revisits are rare and loop closures cannot be relied upon.',
               'We tested state-of-the-art visual Simultaneous Localization And Mapping (SLAM) systems such as RTAB-Map [1] and '
               'ORB-SLAM3 [2] in a high-fidelity simulator [3], and found that both performance degraded significantly in a '
               'long-range scenario (beyond 1 km), as their memory and compute demands grow with the size of the environment.',
               'deep-learning geolocalization achieves high accuracy but is too computationally heavy to run in real-time on '
               'embedded platforms, while odometry-only systems based on Visual-Inertial Odometry (VIO) or Lidar-Inertial '
               'Odometry (LIO) are efficient but accumulate excessive drift.',
               'Some teams used RGB satellite image-based matching, but this has proved to be highly unreliable at such low '
               'altitudes.'],
     'raw_file': R + '2510.01348v2.txt',
     'agent_note': 'Families and assumptions: odometry + loop closure (assumes revisits: a memory of places that long unseen '
                   'routes do not provide); SLAM (memory and compute grow with the map); learned geolocalization (compute); '
                   'satellite-image matching (assumes a viewpoint close to the map\'s, which fails at low altitude).'},
    {'id': 'r3:15', 'bottleneck': 'r3-B2', 'role': 'd',
     'source': 'Werner et al., SPRIN-D winning system (abstract; Sec. II-A; Lessons learned)', 'version': 'arXiv v2, 25 May 2026',
     'url': 'https://arxiv.org/abs/2510.01348v2',
     'quote': ['matches LiDAR-derived local heightmaps to a prior geodata heightmap via gradient-template matching and fuses the '
               'evidence with odometry in a clustered particle filter.',
               'In our case, the limited size of the local map restricted flight speed, which in turn capped the effective '
               'mission range despite accurate localization.',
               'Deployed during the competition, the system executed kilometer-scale flights across urban, forest, and '
               'open-field terrain and reduced drift substantially relative to raw odometry, while running in real time on '
               'CPU-only hardware.'],
     'raw_file': R + '2510.01348v2.txt',
     'agent_note': 'The winning family: map-matching against prior geodata (assumes a prior map that matches the present '
                   'terrain, and enough structure; in open fields the system "mostly relied on the odometry"), a bounded local '
                   'map (memory bound traded against speed and range), and CPU-only onboard execution.'},
    {'id': 'r3:16', 'bottleneck': 'r3-B2', 'role': 'd',
     'source': 'SPRIND, Funke Fully Autonomous Flight 2.0 page', 'version': 'live page fetched 2026-09-30',
     'url': 'https://www.sprind.org/en/actions/challenges/funke-fully-autonomous-flight-2.0',
     'quote': ['Examples include approaches based on multimodal technologies – such as combining one or more cameras with other '
               'sensors like inertial measurement units – as well as alternative technologies like ultra-wideband or '
               'leveraging the Earth’s magnetic field.'],
     'raw_file': R + 'sprind_funke_fully_autonomous_flight_2.0.txt',
     'agent_note': 'The programme\'s list of families: visual-inertial fusion, ultra-wideband (assumes installed beacons), '
                   'magnetic-field navigation (assumes a magnetic map).'},

    # ---------------- r3-B3: perception in adverse conditions (fog, haze)
    {'id': 'r3:17', 'bottleneck': 'r3-B3', 'role': 'a',
     'source': 'Pouladi, Ahsani, Li, Najjaran & Suleman, A Task-Driven Evaluation of UAV Detection and Tracking under Synthetic '
               'Fog (abstract)',
     'version': 'arXiv v1, 6 Jul 2026 (only version)', 'url': 'https://arxiv.org/abs/2607.05467v1',
     'quote': ['Fog severely degrades the visibility of small unmanned aerial vehicles (UAVs) in sky-dominant, long-range imagery, '
               'reducing the reliability of downstream detection and tracking.'],
     'raw_file': R + '2607.05467v1.txt', 'agent_note': 'The problem stated (airborne detection of small UAVs, for sense-and-avoid).'},
    {'id': 'r3:18', 'bottleneck': 'r3-B3', 'role': 'b',
     'source': 'Pouladi et al., synthetic fog (Sec. 2.1)', 'version': 'arXiv v1, 6 Jul 2026',
     'url': 'https://arxiv.org/abs/2607.05467v1',
     'quote': ['However, recent reviews of UAV perception under adversity still indicate that fog-robust airborne perception '
               'remains underdeveloped relative to road-scene perception, especially for safety-critical onboard obstacle or '
               'aircraft detection [19].'],
     'raw_file': R + '2607.05467v1.txt', 'agent_note': '2026 statement that the problem is open (citing a review, [19], not fetched).'},
    {'id': 'r3:19', 'bottleneck': 'r3-B3', 'role': 'b',
     'source': 'Feng, Chen, Li, Wang, Yang, Cheng, Dai & Fu, HazyDet: Open-Source Benchmark for Drone-View Object Detection with '
               'Depth-Cues in Hazy Scenes',
     'version': 'arXiv v2, 26 May 2025 (v1 30 Sep 2024); PDF dated May 25, 2025', 'url': 'https://arxiv.org/abs/2409.19833v2',
     'quote': ['Despite promising progress in recent years, ensuring reliable perception in challenging real-world conditions '
               'remains a significant hurdle. Among various factors, adverse atmospheric effects, particularly haze, present a '
               'persistent obstacle that greatly undermines the robustness of drone-based detection systems.',
               'Despite these advances, the question of how adverse weather conditions fundamentally influence the detection '
               'capabilities of UAVs remains largely unresolved.'],
     'raw_file': R + '2409.19833v2.txt', 'agent_note': '2025 statement that drone-view perception in haze is open.'},
    {'id': 'r3:20', 'bottleneck': 'r3-B3', 'role': 'c',
     'source': 'Pouladi et al., synthetic fog (Table 3, ByteTrack on DUT Anti-UAV sample videos)', 'version': 'arXiv v1, 6 Jul 2026',
     'url': 'https://arxiv.org/abs/2607.05467v1',
     'quote': ['Table 3: ByteTrack tracking performance on DUT Anti-UAV sample videos under clean, fog-degraded, and restored '
               'conditions.',
               'Video YOLO Trained model Clean β = 0.4 β = 1.6 β = 3.6 Foggy Restored Foggy Restored Foggy Restored MOTA IDF1 '
               'MOTA IDF1 MOTA IDF1 MOTA IDF1 MOTA IDF1 MOTA IDF1 MOTA IDF1',
               '02 11n clean 1.000 1.000 0.976 0.988 0.988 0.994 0.265 0.419 0.988 0.994 0.000 0.000 0.277 0.434',
               '11s 100% foggy 1.000 1.000 0.988 0.994 0.988 0.994 0.988 0.994 0.988 0.994 0.771 0.871 0.759 0.863',
               '11s 100% foggy 0.960 0.980 0.970 0.985 0.970 0.985 0.970 0.985 0.940 0.969 0.940 0.969 0.760 0.864',
               '11m 50% foggy 0.980 0.990 0.980 0.990 0.980 0.990 0.970 0.985 0.960 0.980 0.920 0.958 0.890 0.942',
               '11s 100% foggy 0.980 0.990 0.975 0.987 0.980 0.990 0.950 0.974 0.985 0.992 0.960 0.980 0.645 0.580',
               '11m clean 0.995 0.997 0.995 0.997 0.995 0.997 0.995 0.997 0.995 0.997 0.220 0.361 0.790 0.883',
               '11n 100% foggy 0.321 0.210 0.336 0.342 0.332 0.341 0.325 0.209 0.312 0.208 0.078 0.062 0.050 0.066',
               '11s 100% foggy 0.291 0.188 0.316 0.189 0.298 0.187 0.359 0.182 0.301 0.189 0.168 0.119 0.179 0.141',
               'Video 06 is comparatively stable across most detector and tracker settings, whereas Video 10 is consistently '
               'the most challenging sequence for both ByteTrack and BoT-SORT.'],
     'raw_file': R + '2607.05467v1.txt',
     'agent_note': 'Metric: MOTA of YOLO11 + ByteTrack at the heaviest synthetic fog (beta = 3.6), best over detector size '
                   '(n/s/m), training regime (clean, 50% foggy, 100% foggy) and input (foggy or restored). Target (oracle): the '
                   'best clean-condition MOTA on the same video. Rows in order: Video 02 (11n clean; 11s 100% foggy), Video 03 '
                   '(11s 100% foggy; 11m 50% foggy), Video 06 (11s 100% foggy; 11m clean), Video 10 (11n 100% foggy; 11s 100% '
                   'foggy). Best fog vs best clean: V02 0.771 vs 1.000 (gap 0.229); V03 0.940 vs 0.980 (0.040); V06 0.960 vs '
                   '0.995 (0.035); V10 0.179 (restored) vs 0.321 (0.142, 56% retained). Clean-trained detectors collapse at '
                   'beta = 3.6 (e.g. V02 11n clean 0.000). Fog-inclusive training nearly closes the gap on 2 of 4 videos; '
                   'fog is synthetic (depth-aware scattering model), 4 sample videos, one tracker quoted. Same paper, same '
                   'protocol.'},
    {'id': 'r3:21', 'bottleneck': 'r3-B3', 'role': 'c',
     'source': 'Feng et al., HazyDet (Table 3 and Sec. 5.2)', 'version': 'arXiv v2, 26 May 2025',
     'url': 'https://arxiv.org/abs/2409.19833v2',
     'quote': ['Type Model Epoch FPS Para (M) GFLOPs AP on Synthetic Test-Set AP on Real-World Test-Set mAP Car Truck Bus mAP Car '
               'Truck Bus',
               '⋆DeCoDet (Ours) 12 59.7 34.62 225.37 52.0 60.5 34.0 61.9 38.7 55.0 21.9 39.2',
               'Our DeCoDet method outperforms all competitors with model achieving 52.0% mAP on simulated data and 38.7% on '
               'real-world data, while maintaining higher speed (59.7 FPS) and efficiency (34.62M parameters), making it ideal '
               'for deployment in challenging foggy environments.'],
     'raw_file': R + '2409.19833v2.txt',
     'agent_note': 'Best reported real-haze drone-view detection: 38.7 mAP (DeCoDet), against 52.0 on synthetic haze. The paper '
                   'gives no clear-weather or human reference, so no gap to a target is computed from this claim; it is '
                   'recorded as the best real-haze number only.'},
    {'id': 'r3:22', 'bottleneck': 'r3-B3', 'role': 'd',
     'source': 'Pouladi et al., synthetic fog (abstract)', 'version': 'arXiv v1, 6 Jul 2026',
     'url': 'https://arxiv.org/abs/2607.05467v1',
     'quote': ['Given the practical difficulty of collecting and annotating foggy UAV scenes, synthetic fog is generated from real '
               'clear-weather outdoor images containing UAV targets using monocular depth estimation and the atmospheric '
               'scattering model.',
               'The results show that fog substantially degrades both detection and tracking, primarily through increased '
               'missed detections. Fog-inclusive training provides the most consistent improvement in robustness, whereas '
               'test-time restoration is most beneficial when the detector has been trained only on clean imagery.'],
     'raw_file': R + '2607.05467v1.txt',
     'agent_note': 'Families: test-time restoration (dehazing; assumes the degradation model is known), fog-inclusive training '
                   '(assumes the test-time fog distribution was sampled offline at training time), synthetic data generation '
                   '(assumes the scattering model is right). The tracker is tracking-by-detection: a missed detection is not '
                   'recovered.'},
    {'id': 'r3:23', 'bottleneck': 'r3-B3', 'role': 'd',
     'source': 'Feng et al., HazyDet (Sec. 2; Sec. 4.2)', 'version': 'arXiv v2, 26 May 2025',
     'url': 'https://arxiv.org/abs/2409.19833v2',
     'quote': ['Separate paradigms first employ restoration algorithms to enhance image quality before detection; however, this '
               'often yields insufficient impr',
               'While fine-tuning on synthetic data may not generalize well to real-world scenarios, training solely on limited '
               'real-world hazy data often leads to overfitting. To bridge the synthetic-to-real domain gap, we propose a '
               'Progressive Domain Fine-Tuning (PDFT)'],
     'raw_file': R + '2409.19833v2.txt',
     'agent_note': 'Families: restoration-then-detect; joint restoration-detection; depth-conditioned detection with a staged '
                   'fine-tuning schedule (clear -> synthetic haze -> real haze; the stage boundaries are fixed by the designer).'},

    # ---------------- r3-B4: agile flight against human pilots (autonomous drone racing)
    {'id': 'r3:24', 'bottleneck': 'r3-B4', 'role': 'a',
     'source': 'TU Delft news, Autonomous drone from TU Delft defeats human champions in historic racing first',
     'version': 'news release dated 15 April 2025',
     'url': 'https://www.tudelft.nl/en/2025/lr/autonomous-drone-from-tu-delft-defeats-human-champions-in-historic-racing-first',
     'quote': ['The goal of the 2025 A2RL Drone Championship in Abu Dhabi was to push the frontier of physical AI, by stimulating '
               'research on robotic AI under extreme time pressure and with very limited computational and sensory resources. '
               'The drone had access to just one forward-looking camera, a major difference from previous autonomous drone '
               'races.'],
     'raw_file': R + 'tudelft_2025_autonomous-drone-defeats-human-champions.txt',
     'agent_note': 'The problem (agile autonomous flight with minimal sensing and compute) as the competition states it. A '
                   'university release about its own team: a primary source for the result, not an independent one.'},
    {'id': 'r3:25', 'bottleneck': 'r3-B4', 'role': 'b',
     'source': 'Verraest et al., SkyDreamer (abstract; Introduction)', 'version': 'arXiv v1, 16 Oct 2025',
     'url': 'https://arxiv.org/abs/2510.14783v1',
     'quote': ['Autonomous drone racing (ADR) systems have recently achieved champion-level performance, yet remain highly '
               'specific to drone racing. While end-to-end vision-based methods promise broader applicability, no system to '
               'date simultaneously achieves full sim-to-real transfer, onboard execution, and champion-level performance.',
               'In contrast, humans fly with remarkable adaptability – handling unseen tracks, different drones, and even '
               'unstructured environments with minimal task-specific training [3]. This gap underscores the inherent '
               'limitations in today’s champion-level ADR systems.'],
     'raw_file': R + '2510.14783v1.txt',
     'agent_note': '2025 statement: speed against humans is reached, generality is not. The generality gap is stated without a '
                   'number against a target.'},
    {'id': 'r3:26', 'bottleneck': 'r3-B4', 'role': 'c',
     'source': 'TU Delft news, A2RL 2025', 'version': 'news release dated 15 April 2025',
     'url': 'https://www.tudelft.nl/en/2025/lr/autonomous-drone-from-tu-delft-defeats-human-champions-in-historic-racing-first',
     'quote': ['The AI drone developed by TU Delft first won the A2RL Grand Challenge. It then went on to win the knockout '
               'tournament against human pilots, beating three former DCL world champions and reaching flight speeds up to '
               '95.8 km/h on the very winding track.',
               'However, that impressive achievement occurred in a flight lab environment, where conditions, hardware, and the '
               'track were still controlled by the researchers – a very different situation from this world championship, '
               'where the hardware and track were fully designed and managed by the competition organisers.'],
     'raw_file': R + 'tudelft_2025_autonomous-drone-defeats-human-champions.txt',
     'agent_note': 'Benchmark: the A2RL x DCL 2025 AI-vs-human knockout on an organiser-designed drone and track. Target: human '
                   'champion pilots. Best: the AI won against three former DCL world champions (up to 95.8 km/h). The target '
                   'is reached on this metric (second sentence: the 2023 Zurich win was in a lab setting). No lap times are '
                   'given in the release.'},
    {'id': 'r3:27', 'bottleneck': 'r3-B4', 'role': 'd',
     'source': 'TU Delft news, A2RL 2025', 'version': 'news release dated 15 April 2025',
     'url': 'https://www.tudelft.nl/en/2025/lr/autonomous-drone-from-tu-delft-defeats-human-champions-in-historic-racing-first',
     'quote': ['One of the core new elements of the drone’s AI is the use of a deep neural network that doesn’t send control '
               'commands to a traditional human controller, but directly to the motors.',
               'We now train the deep neural networks with reinforcement learning, a form of learning by trial and error.',
               'Robot AI is limited by the required computational and energy resources.'],
     'raw_file': R + 'tudelft_2025_autonomous-drone-defeats-human-champions.txt',
     'agent_note': 'Family: end-to-end neural guidance-and-control trained by RL in simulation for a known track and a known '
                   'drone (task given in advance; tuning offline).'},
    {'id': 'r3:28', 'bottleneck': 'r3-B4', 'role': 'd',
     'source': 'Verraest et al., SkyDreamer (Introduction; Conclusion)', 'version': 'arXiv v1, 16 Oct 2025',
     'url': 'https://arxiv.org/abs/2510.14783v1',
     'quote': ['Such pipelines cannot generalize beyond the highly structured settings they were designed for.',
               'Despite these promising results, several limitations remain. Parameter estimates tend to drift over time, and '
               'their quality varies across training runs.'],
     'raw_file': R + '2510.14783v1.txt',
     'agent_note': 'Modular racing pipelines assume a structured, known setting; the end-to-end world-model family estimates '
                   'parameters online, and those estimates drift over time.'},

    # ---------------- r3-B5: C2 link reliability and lost-link behaviour (civil BVLOS and jammed environments)
    {'id': 'r3:29', 'bottleneck': 'r3-B5', 'role': 'a',
     'source': 'FAA and TSA, Normalizing Unmanned Aircraft Systems Beyond Visual Line of Sight Operations, NPRM, 90 FR 38212, '
               'Docket FAA-2025-1908',
     'version': 'Federal Register Vol. 90 No. 150, 7 Aug 2025 (govinfo PDF, 180 pages); proposed rule, not final',
     'url': 'https://www.govinfo.gov/content/pkg/FR-2025-08-07/pdf/2025-14992.pdf',
     'quote': ['As discussed in section XI.D of this preamble, a lost link or loss of control of the UA pose significant risks to '
               'aviation safety.',
               'The operator would not be able to commence a UAS operation if a control link is working improperly, whether due '
               'to a result of radio interference or for some other reason.',
               'In addition, FAA expects that BVLOS flights could at times experience intermittent lost link.'],
     'raw_file': R + 'FR-2025-14992.txt', 'agent_note': 'The problem stated by the regulator (2025).'},
    {'id': 'r3:30', 'bottleneck': 'r3-B5', 'role': 'a',
     'source': 'Watling & Reynolds, Tactical Developments During the Third Year of the Russo-Ukrainian War, RUSI',
     'version': 'report, February 2025 (PDF created 14 Feb 2025)',
     'url': 'https://static.rusi.org/tactical-developments-third-year-russo-ukrainian-war-february-2205.pdf',
     'quote': ['Between 60 and 80% of Ukrainian FPVs fail to reach their target, depending on the part of the front and the skill '
               'of the operators.',
               'Furthermore, there are long periods where either EW or the weather significantly degrades UAV operations.'],
     'raw_file': R + 'rusi_tactical-developments-third-year-russo-ukrainian-war-february-2025.txt',
     'agent_note': 'The contested-spectrum form of the problem: radio-piloted drones lose their link under electronic warfare '
                   '(EW). The 60-80% figure is the authors\' field estimate and mixes link loss with other causes; it is not a '
                   'C2 metric and is not used for the gap.'},
    {'id': 'r3:31', 'bottleneck': 'r3-B5', 'role': 'b',
     'source': 'Chintareddy, Abdullah, Clough, Frost, Keshmiri & Hashemi, A Vertical Look at UAV Connectivity in the Wild: '
               'Cellular vs. Starlink, 3D Characterization, and Performance Prediction (Introduction)',
     'version': 'arXiv v2, 28 May 2026 (v1 26 May 2026)', 'url': 'https://arxiv.org/abs/2605.27755v2',
     'quote': ['Practical field evaluations further highlight the difficulty of meeting stringent reliability and latency '
               'requirements, such as 99.9% C2 reliability and sub-100 ms one-way delay under complex aerial propagation '
               'conditions and dynamic network loading [13].'],
     'raw_file': R + '2605.27755v2.txt',
     'agent_note': '2026 statement that meeting C2 requirements over commercial networks is hard; also states the requirement '
                   'used as target in r3:33 (the paper cites [13]; the 3GPP study itself was not fetched).'},
    {'id': 'r3:32', 'bottleneck': 'r3-B5', 'role': 'b',
     'source': 'Watling & Reynolds, RUSI (Fires: Attrition in Depth; Electronic protection)', 'version': 'report, February 2025',
     'url': 'https://static.rusi.org/tactical-developments-third-year-russo-ukrainian-war-february-2205.pdf',
     'quote': ['at present, navigational jamming is ubiquitous throughout the combat area. Jamming of command frequences is also '
               'widespread.'],
     'raw_file': R + 'rusi_tactical-developments-third-year-russo-ukrainian-war-february-2025.txt',
     'agent_note': '2025 statement that GNSS and command-link denial is the normal condition in that theatre ("frequences" is the '
                   'source\'s spelling).'},
    {'id': 'r3:33', 'bottleneck': 'r3-B5', 'role': 'c',
     'source': 'Chintareddy et al., UAV connectivity (abstract; Sec. 5.1, Table 1)', 'version': 'arXiv v2, 28 May 2026',
     'url': 'https://arxiv.org/abs/2605.27755v2',
     'quote': ['Through an extensive flight campaign with more than 10 flight tests, 4.5+ hours of flight time resulting in more '
               'than 18K samples',
               'the LEO satellite link achieves superior latency performance with 95% of Round-Trip Time (RTT) measurements '
               'below 50 ms compared to 80% under 150 ms for cellular',
               '53.5% of handovers improve RTT, but worst-case degradation (275 ms) is 2 × larger than best-case improvement '
               '(137 ms).',
               'the cellular connection achieved a packet delivery rate of 99.44% (5130 out of 5159 packets delivered), while '
               'the Starlink connection maintained a 99.31% delivery rate (3602 of 3627 packets delivered).',
               'These minimal packet loss rates (0.56% for cellular and 0.69% for Starlink) validate the robustness of both '
               'links for UAV operations and indicate sufficient reliability for data transfers.'],
     'raw_file': R + '2605.27755v2.txt',
     'agent_note': 'Benchmark: in-flight packet delivery and RTT over commercial LTE (Verizon) and Starlink, rural Kansas. Target '
                   '(r3:31, same paper): 99.9% C2 reliability, sub-100 ms one-way delay. Delivery 99.44% (LTE) and 99.31% '
                   '(Starlink): loss 0.56% and 0.69% against 0.1% allowed, i.e. 5.6x and 6.9x the allowed loss. Latency: at '
                   'least 20% of LTE RTTs exceed 150 ms (above 75 ms one-way if the path is symmetric; the share above 100 ms '
                   'one-way is not reported); Starlink meets 50 ms RTT for 95% of samples, and its 99.9th percentile is not '
                   'reported. Worst handover RTT increase 275 ms. The authors call the delivery rates "sufficient reliability '
                   'for data transfers"; the comparison with the C2 requirement is the agent\'s. The traffic was test packets '
                   '(Nping/iPerf3), not a C2 protocol.'},
    {'id': 'r3:34', 'bottleneck': 'r3-B5', 'role': 'd',
     'source': 'FAA and TSA, Part 108 NPRM (Sec. XI, design requirements)', 'version': '90 FR 38212, 7 Aug 2025',
     'url': 'https://www.govinfo.gov/content/pkg/FR-2025-08-07/pdf/2025-14992.pdf',
     'quote': ['Proposed § 108.815(b) would require the UAS design to execute a safe predetermined action in the event of a link '
               'timeout.',
               'FAA expects industry to define and standardize safe predetermined actions such as return to home, loiter, '
               'continue flight, etc. a UA could execute during a link timeout event.',
               'Further, FAA also expects industry to define the link timeout metric as part of any proposed MOC'],
     'raw_file': R + 'FR-2025-14992.txt',
     'agent_note': 'The regulatory family: link loss is declared by a timeout (a clock), and the response is a predetermined '
                   'action chosen before flight (return to home, loiter, continue). The timeout value is left to industry '
                   'standards.'},
    {'id': 'r3:35', 'bottleneck': 'r3-B5', 'role': 'd',
     'source': 'EASA, AMC & GM to Regulation (EU) 2019/947, Issue 1, Amendment 3 (Annex to ED Decision 2025/018/R; SORA 2.5)',
     'version': 'PDF dated 29 Sep 2025 (204 pages); renamed Amendment 4 by the Corrigendum of 12 Dec 2025',
     'url': 'https://www.easa.europa.eu/en/downloads/142980/en',
     'quote': ['Note 2: The main parameters associated with the performance of a C2 link (RLP) and the performance parameters for '
               'other communication links (e.g. RCP for communication with ATC) include, but are not limited to, the '
               'following: (i) the transaction expiration time; (ii) the availability; (iii) the continuity; and (iv) the '
               'integrity.',
               'definition and upload of lost link contingency automatic procedures',
               'Emergency recovery capability A UAS safety feature (e.g. return-to-home) that provides for the cessation of the '
               'UA operation in a manner that minimises the risk to persons on the ground, other airspace users and critical '
               'infrastructure.',
               'For operations requesting only a low level of integrity for this OSO, this could be achieved by monitoring the '
               'C2 link signal strength and receiving an alert from the UAS HMI if the signal strength becomes too low.'],
     'raw_file': R + 'easa_download_142980.txt',
     'agent_note': 'EU family: C2 performance specified by a transaction expiration time (clock), availability, continuity and '
                   'integrity; lost-link contingencies uploaded as automatic procedures before flight; emergency recovery such '
                   'as return-to-home; at low integrity, a signal-strength alert to the remote pilot.'},
    {'id': 'r3:36', 'bottleneck': 'r3-B5', 'role': 'd',
     'source': 'Chintareddy et al., UAV connectivity (Related work)', 'version': 'arXiv v2, 28 May 2026',
     'url': 'https://arxiv.org/abs/2605.27755v2',
     'quote': ['Dual connectivity, in which UAVs simultaneously utilize commercial LTE and LEO satellite links, offers a promising '
               'path toward resilient and flexible communication architectures, enabling failover, load balancing, and '
               'application-aware traffic steering across heterogeneous networks [31].',
               'while higher altitudes (e.g., 330+ m above the sea level) improve signal power by 15 −20 dB via line-of-sight '
               '(LOS) propagation, it causes a 3 −4 × increase in handover rates, which is due to excessive multi-cell '
               'visibility rather than signal degradation.'],
     'raw_file': R + '2605.27755v2.txt',
     'agent_note': 'Family: link redundancy (dual LTE + LEO with failover; assumes both links are not lost together). Cellular '
                   'handover triggers are threshold rules designed for ground users; at altitude they fire 3-4x more often.'},
    {'id': 'r3:37', 'bottleneck': 'r3-B5', 'role': 'd',
     'source': 'Watling & Reynolds, RUSI (Fires; Protection of Territory)', 'version': 'report, February 2025',
     'url': 'https://static.rusi.org/tactical-developments-third-year-russo-ukrainian-war-february-2205.pdf',
     'quote': ['FPVs have been improved with autonomous terminal guidance and wire spools, which render them impervious to '
               'electronic disruption.',
               'including degraded flight performance, a comparatively limited range of approximately 10 km and running the '
               'risk of entanglement with obstacles',
               'These gaps can be induced through the suppression of enemy electronic warfare (EW) using artillery, or through '
               'planned pauses in friendly jamming to enable strike systems to get airborne.',
               'EW is effective in significantly reducing the reliability of UAVs and disrupting the accurate fixing of targets '
               'to cue strikes. However, it is also causing widespread issues with deconfliction and fratricide causes friendly '
               'UAV operations to be periodic rather than continuous.'],
     'raw_file': R + 'rusi_tactical-developments-third-year-russo-ukrainian-war-february-2025.txt',
     'agent_note': 'Families under jamming: remove the radio link (fibre-optic spools: about 10 km range, entanglement), or '
                   'remove the need for it at the end (autonomous terminal guidance), or schedule operations into planned '
                   'windows (pauses in friendly jamming), which makes operations "periodic rather than continuous".'},
    {'id': 'r3:38', 'bottleneck': 'r3-B5', 'role': 'd',
     'source': 'FAA and TSA, Part 108 NPRM (maintenance; proposed § 108.930 testing)', 'version': '90 FR 38212, 7 Aug 2025',
     'url': 'https://www.govinfo.gov/content/pkg/FR-2025-08-07/pdf/2025-14992.pdf',
     'quote': ['must perform at least 150 flight hours without experiencing any failure leading to— (1) Loss of flight, (2) Loss '
               'of control,',
               'Inspection criteria typically include a schedule for performing maintenance and inspections, expressed in time '
               'in service, calendar time, number of system operations, or any combination thereof.'],
     'raw_file': R + 'FR-2025-14992.txt',
     'agent_note': 'Fail-safe reliability is demonstrated on a clock (150 flight hours without a failure leading to loss of '
                   'flight or control, among other outcomes) and maintained on clocks or counts (time in service, calendar '
                   'time, cycles).'},

    # ---------------- r3-B6: BVLOS detect-and-avoid of non-cooperative aircraft
    {'id': 'r3:39', 'bottleneck': 'r3-B6', 'role': 'a',
     'source': 'UK CAA, CAP 3015 Detect and Avoid Policy Concept v2 (Ch. 1)',
     'version': 'Second edition September 2026 (first published July 2024; version date 22 Sep 2026; PDF created 23 Sep 2026)',
     'url': 'https://www.caa.co.uk/publication/download/22551',
     'quote': ['Perhaps the most significant barrier to the growth of this sector is the mid-air collision risk associated with '
               'Beyond Visual Line of Sight (BVLOS) operations.',
               'However, it is recognised that visual detection of ‘smaller’ UA from the cockpit of manned aircraft may be '
               'limited, and EC-in detection of the UA by the manned is not currently expected to be mandated, hence UA are to '
               'resolve any conflicts at range.'],
     'raw_file': R + 'caa_CAP3015_v2.txt', 'agent_note': 'The problem stated by the UK regulator (2026).'},
    {'id': 'r3:40', 'bottleneck': 'r3-B6', 'role': 'a',
     'source': 'FAA and TSA, Part 108 NPRM', 'version': '90 FR 38212, 7 Aug 2025',
     'url': 'https://www.govinfo.gov/content/pkg/FR-2025-08-07/pdf/2025-14992.pdf',
     'quote': ['Research conducted by MITRE for FAA found that in Class G airspace, a drone with no mitigations could be expected '
               'to collide with manned aircraft between once every 10,000 flight hours in the most heavily used Class G '
               'airspace, to once every 1 million flight hours in the least used Class G airspace.',
               'FAA also proposes to require UA operating in Class B or C airspace to detect and avoid manned aircraft that are '
               'not broadcasting their position via ADS–B or an electric conspicuity device.'],
     'raw_file': R + 'FR-2025-14992.txt',
     'agent_note': 'The problem with a quantified unmitigated risk (1e-4 to 1e-6 collisions per flight hour in Class G), and the '
                   'proposed non-cooperative DAA requirement ("electric" is the source\'s word).'},
    {'id': 'r3:41', 'bottleneck': 'r3-B6', 'role': 'b',
     'source': 'Riedel (DLR), A Review of Detect and Avoid Standards for Unmanned Aircraft Systems, Aerospace 12(4):344',
     'version': 'published 15 April 2025 (CC BY; DLR elib copy of the publisher PDF)',
     'url': 'https://elib.dlr.de/213723/1/aerospace-12-00344.pdf',
     'quote': ['Smaller UASs, especially when operating in VLL, are facing major challenges like detecting manned traffic in '
               'regions with high clutter. Furthermore, smaller UAS-to-UAS DAA concepts are still under development. Detection '
               'of small UASs, encounter models for VLL, and maneuver coordination for smaller UASs are some of the main aspects '
               'that still require suitable solutions. While there is plenty of research carried out within these areas, none '
               'of these approaches have undergone the transition from prototype experiments to robust, safe, standardized, and '
               'secure subsystems.',
               'Moreover, there is currently no standard available that applies to smaller UASs, which are not capable of '
               'hovering.'],
     'raw_file': R + 'aerospace-12-00344.txt', 'agent_note': '2025 statement that small-UAS DAA is open.'},
    {'id': 'r3:42', 'bottleneck': 'r3-B6', 'role': 'b',
     'source': 'FAA, Part 108 NPRM, Reopening of Comment Period, 91 FR 3695 (Notice No. 25-07B)',
     'version': 'Federal Register Vol. 91 No. 18, 28 Jan 2026 (govinfo PDF)',
     'url': 'https://www.govinfo.gov/content/pkg/FR-2026-01-28/pdf/2026-01644.pdf',
     'quote': ['Other commenters expressed concern that the proposed detect-and-avoid provisions would require prohibitively '
               'expensive technology that has not been adequately proven for safety value.',
               'Noting the substantial interest in, and comment on, FAA’s proposed policies for ADS–B Out, EC, and '
               'detect-and-avoid, FAA is reopening the NPRM for comment on the limited topics discussed herein.'],
     'raw_file': R + 'FR-2026-01644.txt',
     'agent_note': '2026 regulator record that non-cooperative DAA is unsettled (commenters\' view, reported by FAA; the rule '
                   'reopened). No final Part 108 rule appears in docket FAA-2025-1908 on 2026-09-30 (Federal Register API '
                   'listing saved as a raw file).'},
    {'id': 'r3:43', 'bottleneck': 'r3-B6', 'role': 'b',
     'source': 'Kapoor, Higgins, Keetha, Patrikar et al., Demonstrating ViSafe: Vision-enabled Safety for High-speed Detect and '
               'Avoid (Introduction)',
     'version': 'arXiv v2, 8 May 2025 (v1 6 May 2025)', 'url': 'https://arxiv.org/abs/2505.03694v2',
     'quote': ['Addressing threats posed by cooperative as well as non-cooperative aerial entities like balloons and rogue drones '
               'while respecting SWaP-C resource constraints remains an ongoing challenge. As a result, current regulations '
               'impose strict line-of-sight requirements on human operators, significantly restricting the utility and '
               'scalability of UASs.'],
     'raw_file': R + '2505.03694v2.txt', 'agent_note': '2025 statement that small-UAS DAA is open.'},
    {'id': 'r3:44', 'bottleneck': 'r3-B6', 'role': 'b',
     'source': 'UK CAA, Detect and Avoid policy programme page', 'version': 'live page fetched 2026-09-30 (no last-updated date)',
     'url': 'https://www.caa.co.uk/drones/regulations-consultations-and-policy-programmes/policy-programmes/detect-and-avoid/',
     'quote': ['DAA Policy Concept v2 is a live policy concept that may be used to support operational authorisations during the '
               'policy concept test phase.',
               'Its use remains controlled and operation-specific while the CAA and industry build experience and test the '
               'completeness and suitability of the framework before any transition to business-as-usual arrangements.'],
     'raw_file': R + 'caa_detect-and-avoid_page.txt',
     'agent_note': '2026 regulator status: DAA-enabled BVLOS is authorised case by case in a test phase, not routine.'},
    {'id': 'r3:45', 'bottleneck': 'r3-B6', 'role': 'c',
     'source': 'UK CAA, CAP 3015 v2 (DAA02 requirement; guidance DAA02.GM1)', 'version': 'Second edition September 2026',
     'url': 'https://www.caa.co.uk/publication/download/22551',
     'quote': ['DAA02 ARC-b & ARC-c The nominal DAA capability shall meet the following Logic RR performance requirements: '
               'Cooperative with coordinating manoeuvre: NMAC RR ≤ 0.04, LWC RR ≤ 0.4 Cooperative: NMAC RR ≤ 0.18, LWC RR ≤ '
               '0.4 Non-cooperative: NMAC RR ≤ 0.3, LWC RR ≤ 0.5',
               'The NMAC volume is defined as 500 ft horizontally and +/-100 ft vertically around the ownship, and Well Clear '
               'Volume is defined as 2000 ft horizontally and +/-250 ft vertically around the ownship.',
               'A smaller value denotes improved performance, e.g., a RR of 0.1 indicates that 90% of events have successfully '
               'been mitigated.'],
     'raw_file': R + 'caa_CAP3015_v2.txt',
     'agent_note': 'The regulatory target (UK, 2026): against non-cooperative intruders, logic risk ratio NMAC <= 0.3 and LWC <= '
                   '0.5, with NMAC defined as 500 ft horizontal / +/-100 ft vertical.'},
    {'id': 'r3:46', 'bottleneck': 'r3-B6', 'role': 'c',
     'source': 'ASSURE (FAA Center of Excellence), A65 Detect and Avoid Risk Ratio Validation, Final Report (Executive Summary; '
               'Table 16)',
     'version': 'Final Report 7/31/2024, updated 16 Oct 2025 ("Third party research. Pending FAA review.")',
     'url': 'https://assureuas.org/wp-content/uploads/2022/02/A65-Final-Report-Updated-16-Oct-2025.pdf',
     'quote': ['found that the Risk Ratio values presented in this report are in line with the currently accepted ASTM '
               'non-cooperative LoWC Risk Ratio of 0.5 and NMAC Risk Ratio of 0.3for most of the beta ranges.',
               'Table 16. Encounter simulation results for β=2859. Turn Rate(x standard) Delay (s) Risk Ratio, Well-Clear (Own '
               'Only) Risk Ratio, NMAC (Own Only) Risk Ratio, Well-Clear (Both) Risk Ratio, NMAC (Both) Cessna Intruder 1 3 '
               '0.746 0.625 0.596 0.331'],
     'raw_file': R + 'A65-Final-Report-Updated-16-Oct-2025.txt',
     'agent_note': 'Corroborates the target (ASTM non-cooperative NMAC RR 0.3, LoWC RR 0.5; "0.3for" is the source\'s spacing) '
                   'and gives the human baseline: modelled general-aviation pilot see-and-avoid at standard turn rate and 3 s '
                   'delay, NMAC RR 0.625 when only the ownship avoids and 0.331 when both avoid (beta = 2859, Cessna intruder).'},
    {'id': 'r3:47', 'bottleneck': 'r3-B6', 'role': 'c',
     'source': 'Kapoor et al., ViSafe (Sec. V, Tables II and III; Sec. VI-B)', 'version': 'arXiv v2, 8 May 2025',
     'url': 'https://arxiv.org/abs/2505.03694v2',
     'quote': ['TABLE II DIGITAL TWIN & HARDWARE-IN-THE-LOOP BENCHMARKING Separation Minima (m) ↑ P(NMAC) ↓ Risk Ratio ↓ Number '
               'of violations ↓ Scenario Nominal ViSafe Nominal ViSafe Nominal ViSafe Nominal ViSafe',
               'E1 19.9 ± 2.15 35.55 ± 14.00 1.0 0.55 1.0 0.55 4000 2213 E2 22.72 ± 2.63 27.635 ± 6.27 1.0 0.439 1.0 0.439 4000 '
               '1759 E3 49.14 ± 0.7 59.04 ± 11.37 1.0 0.5248 1.0 0.5248 4000 2099',
               'Above Horizon - E1, E2, E3 30.58 ± 3.02 50.90 ± 4.72 1.0 0.1 1.0 0.1 6000 605 Below Horizon - E1, E2, E3 28.6 ± '
               '2.73 30.46 ± 3.26 1.0 0.91 1.0 0.91 6000 5466',
               'TABLE III REAL WORLD BENCHMARKING',
               'Below Horizon - E1, E2, E3 44.59 ± 2.73 60.23 ± 18.76 1.0 0.667 1.0 0.667 6 4',
               '1) Probability of Near Mid Air Collision P(NMAC): This metric measures the probability that two agents come '
               'within a predefined unsafe distance.',
               'Across our wide array of simulation and real-world tests, we find that our current system struggles when the '
               'intruder is below the horizon.'],
     'raw_file': R + '2505.03694v2.txt',
     'agent_note': 'Best reported vision-only small-UAS DAA with a risk ratio: digital-twin HIL, 4000-6000 encounters per row; '
                   'RR 0.55 (E1 head-on), 0.439 (E2 overtake), 0.5248 (E3 crossing), 0.1 above the horizon, 0.91 below it; '
                   'real world 0.667 below the horizon (6 encounters). Against the non-cooperative target NMAC RR <= 0.3 (r3:45, '
                   'r3:46): E1-E3 are 1.46-1.83x the allowed ratio, below-horizon 3.0x; above-horizon meets it. CROSS-DOCUMENT '
                   'and not the same protocol: ViSafe\'s NMAC is its own "predefined unsafe distance" between small drones '
                   '(intruders a hexarotor and a VTOL at up to 144 km/h closure), not CAP 3015\'s 500 ft volume around manned '
                   'aircraft, so the comparison is indicative only. E1-E3 are better than the modelled human own-only baseline '
                   '(0.625, r3:46).'},
    {'id': 'r3:48', 'bottleneck': 'r3-B6', 'role': 'd',
     'source': 'UK CAA, CAP 3015 v2 (Ch. 8-9, qualification by simulation; DAA18)', 'version': 'Second edition September 2026',
     'url': 'https://www.caa.co.uk/publication/download/22551',
     'quote': ['On the order of 10,000–200,000 encounter-geometry simulations should be conducted.',
               'The total number of simulations, as well as the percentage allocated to each split, should be determined by '
               'convergence of the Risk Ratio, Loss of Well Clear ratio, and unnecessary manoeuvre rate (including induced '
               'NMACs/LWC) to within 5% of a stable value (see Figure 1).',
               'A deterministic simulation framework may be used, providing quick results without requiring extensive '
               'computational resources.',
               'In addition to the usual Mandatory Occurrence Reporting (MOR) the competent authority will conduct an enhanced '
               'monitoring programme on any approved DAA enabled operations.'],
     'raw_file': R + 'caa_CAP3015_v2.txt',
     'agent_note': 'Qualification family: fast-time encounter simulation (10^4-2x10^5 encounters, stopped when the risk ratio '
                   'converges within 5%), then enhanced in-service monitoring. Assumes the encounter model represents the '
                   'traffic the system will meet.'},
    {'id': 'r3:49', 'bottleneck': 'r3-B6', 'role': 'd',
     'source': 'Riedel (DLR), DAA standards review', 'version': 'published 15 April 2025',
     'url': 'https://elib.dlr.de/213723/1/aerospace-12-00344.pdf',
     'quote': ['These models are based on data acquired by long-term observations of different airspace classes.',
               'These volumes and alerting times are usually determined by running millions of fast-time simulations using '
               'encounter models and the DAA system to check if the required risk ratios are achieved.',
               'Many research papers on detect and avoid introduce new algorithms for surveillance, conflict detection, and '
               'avoidance, but do not provide evidence that these algorithms are capable of mitigating collisions by reducing '
               'the risk ratio or complying with standards which have proven that their requirements support the system to '
               'achieve that.'],
     'raw_file': R + 'aerospace-12-00344.txt',
     'agent_note': 'Standards family: fixed protection volumes and alerting times (tau thresholds on the clock) tuned by millions '
                   'of simulations on encounter models built from long-term historical traffic (assumes stationary traffic '
                   'statistics). Research family: new algorithms, often without risk-ratio evidence.'},
    {'id': 'r3:50', 'bottleneck': 'r3-B6', 'role': 'd',
     'source': 'Kapoor et al., ViSafe (Sec. IV; Sec. VI-B)', 'version': 'arXiv v2, 8 May 2025',
     'url': 'https://arxiv.org/abs/2505.03694v2',
     'quote': ['Lastly, for the design of our CBF, we make the following assumptions: the intruder has a constant velocity '
               'vector, the action space of the ownship is constrained to a 2D plane parallel to the ground plane, and the '
               'intruder doesn’t react to the ownship’s actions.',
               'We use the following tuned hyperparameters for the final formulation of Eq. (12) and 13: k = 0.2, c = 0.01, n = '
               '0.3, and λ = 0.2.',
               'For our real-world intruder platforms (shown in Fig. 1), the reliable maximum distance comes out as dHexarotor '
               'max = 287m and dVTOL max = 525m. Thus, for real-world Head-on scenarios, the maximum available reaction time for '
               'the M600 intruder is 14.35s, and for the VTOL intruder, it is 13.12s.'],
     'raw_file': R + '2505.03694v2.txt',
     'agent_note': 'Learned-perception + control-barrier-function family: assumes a constant-velocity, non-reacting intruder and '
                   'planar manoeuvres; hyperparameters hand-tuned for one ownship; the reaction window is bounded by the '
                   'detection range (287 m / 525 m -> 14.35 s / 13.12 s).'},
    {'id': 'r3:51', 'bottleneck': 'r3-B6', 'role': 'd',
     'source': 'FAA and TSA, Part 108 NPRM (strategic deconfliction; right-of-way)',
     'version': '90 FR 38212, 7 Aug 2025',
     'url': 'https://www.govinfo.gov/content/pkg/FR-2025-08-07/pdf/2025-14992.pdf',
     'quote': ['In total, the Applied Physics Laboratory conducted more than 450,000 airspace simulations representing nearly 94 '
               'million UAS flight hours, the research showed midair collisions between UAS were about 100 times less likely to '
               'occur when strategic deconfliction was used by all UAS, compared with simulations in which UAS did not use '
               'strategic deconfliction.',
               'FAA acknowledges that ADS–B Out systems may occasionally fail to meet the performance requirements of § 91.227. '
               'Therefore, FAA expects DAA standards would include performance requirements for the UAS so that the system can '
               'avoid aircraft when ADS–B Out equipment exhibits performance deficiencies.'],
     'raw_file': R + 'FR-2025-14992.txt',
     'agent_note': 'Strategic family: deconfliction of shared operational intent before flight (assumes every UAS participates; '
                   'about 100x fewer UAS-UAS midair collisions in simulation). Cooperative family: yield to ADS-B Out '
                   'broadcasters (assumes the intruder equips and its equipment works).'},
    {'id': 'r3:52', 'bottleneck': 'r3-B6', 'role': 'd',
     'source': 'FAA, Reopening of Comment Period (Comments Received)', 'version': '91 FR 3695, 28 Jan 2026',
     'url': 'https://www.govinfo.gov/content/pkg/FR-2026-01-28/pdf/2026-01644.pdf',
     'quote': ['Some commenters identified mandatory ADS–B or alternate EC for [...] manned operators in low-altitude airspace as '
               'the preferred, and only viable, collision risk mitigation strategy.'],
     'raw_file': R + 'FR-2026-01644.txt',
     'agent_note': 'A reframing on the record (commenters, reported by FAA): make every aircraft cooperative (electronic '
                   'conspicuity mandate) rather than detect non-cooperative ones. The "[...]" skips a page header.'},
    {'id': 'r3:53', 'bottleneck': 'r3-B6', 'role': 'd',
     'source': 'EASA, AMC & GM to Regulation (EU) 2019/947 (SORA 2.5, Step #6 TMPR levels)',
     'version': 'Annex to ED Decision 2025/018/R, PDF dated 29 Sep 2025', 'url': 'https://www.easa.europa.eu/en/downloads/142980/en',
     'quote': ['If operations in this airspace are conducted more routinely, the competent authority is expected to require the '
               'operator to comply with the recognised DAA system standards (e.g. those developed by RTCA SC-228 and/or EUROCAE '
               'WG-105).',
               'Operations with a medium TMPR will likely be supported by systems currently used in aviation to aid the remote '
               'pilot in detecting other manned aircraft or by systems which are designed to support aviation and which are '
               'built to a corresponding level of robustness.',
               'For example, for operations below 500 ft AGL, the traffic avoidance manoeuvres are expected to mostly be based '
               'on a rapid descent to an altitude where manned aircraft are not expected to ever operate.'],
     'raw_file': R + 'easa_download_142980.txt',
     'agent_note': 'EU family (SORA 2.5): tactical mitigation scaled to the air-risk class; at low TMPR a fixed avoidance '
                   'manoeuvre (rapid descent); for routine high-risk operations, the RTCA/EUROCAE DAA standards. No numeric '
                   'risk-ratio targets appear in the fetched AMC text.'},

    # ---------------- r3-B7: counter-UAS detection, tracking and non-destructive interception
    {'id': 'r3:54', 'bottleneck': 'r3-B7', 'role': 'a',
     'source': 'SPRIND, Funke Anti-Drone Response 2.0 page (with Vinnova)',
     'version': 'live page fetched 2026-09-30 ("2nd stage"; the Funke started 1 Mar 2026)',
     'url': 'https://www.sprind.org/en/actions/challenges/funke-anti-drone-response-2.0',
     'quote': ['Small and micro drones have rapidly evolved into a significant security challenge – whether in urban '
               'environments, at airports, during major events, or around critical infrastructure. They are inexpensive, '
               'readily available, adaptable, and increasingly equipped with autonomous capabilities. Existing countermeasures '
               'are overwhelmed by the speed, diversity, and agility of these systems.'],
     'raw_file': R + 'sprind_funke_anti_drone_response_2.0.txt', 'agent_note': 'The problem stated by the programme.'},
    {'id': 'r3:55', 'bottleneck': 'r3-B7', 'role': 'b',
     'source': 'SPRIND, Funke Anti-Drone Response 2.0 page', 'version': 'live page fetched 2026-09-30 (Funke started 1 Mar 2026)',
     'url': 'https://www.sprind.org/en/actions/challenges/funke-anti-drone-response-2.0',
     'quote': ['Key components such as reliable detection and classification, robust decision-making logic, and reversible '
               'intervention mechanism were not yet integrated into a cohesive system. The core challenge therefore remains '
               'unresolved.',
               'The SPRIND Funke starts on March 1, 2026, and runs for a total duration of 15 months across three stages.'],
     'raw_file': R + 'sprind_funke_anti_drone_response_2.0.txt',
     'agent_note': '2026 programme statement that the problem is open (after the first edition).'},
    {'id': 'r3:56', 'bottleneck': 'r3-B7', 'role': 'b',
     'source': 'Xie, Zhang, Wang, Liu, Lu, Chen & Hu, CST Anti-UAV: A Thermal Infrared Benchmark for Tiny UAV Tracking in Complex '
               'Scenes (abstract)',
     'version': 'arXiv v2, 19 Nov 2025 (v1 31 Jul 2025)', 'url': 'https://arxiv.org/abs/2507.23473v2',
     'quote': ['Experimental results demonstrate that tracking tiny UAVs in complex environments remains a challenge, as the '
               'state-of-the-art method achieves only 35.92% state accuracy, much lower than the 67.69% observed on the '
               'Anti-UAV410 dataset.'],
     'raw_file': R + '2507.23473v2.txt', 'agent_note': '2025 statement that counter-UAS tracking is open.'},
    {'id': 'r3:57', 'bottleneck': 'r3-B7', 'role': 'c',
     'source': 'Xie et al., CST Anti-UAV (Sec. 1; Table 3)', 'version': 'arXiv v2, 19 Nov 2025',
     'url': 'https://arxiv.org/abs/2507.23473v2',
     'quote': ['It contains 220 video sequences with over 240k high-quality bounding box annotations',
               'Methods Source Trained with 410 and test on 410 Trained with CST and test on CST mSA P(AUC) S(AUC) mSA P(AUC) '
               'S(AUC) GlobalTrack [27] AAAI20 66.42 85.25 65.11 35.92 58.72 35.38',
               'For example, SiamDT’s [26] State Accuracy (SA) performance drops from 67.69% on Anti-UAV410 to 35.84% on CST '
               'Anti-UAV, while GlobalTrack [27] declines from 66.42% to 35.92%'],
     'raw_file': R + '2507.23473v2.txt',
     'agent_note': 'Benchmark: CST Anti-UAV (thermal infrared, tiny UAVs, complex scenes), mean state accuracy (mSA; SA scores '
                   'IoU when the target is visible and correct absence prediction when not). Best: 35.92 (GlobalTrack, trained '
                   'and tested on CST). Target: the oracle (SA 100); reference: 67.69 by the same class of trackers on '
                   'Anti-UAV410. Gap: 64.08 points to the oracle. The best score drops from 67.69 (SiamDT, Anti-UAV410) to '
                   '35.92 (GlobalTrack, CST), 31.77 points; per tracker, GlobalTrack loses 30.50 and SiamDT 31.85 (about half '
                   'their accuracy). Same paper, same protocol.'},
    {'id': 'r3:58', 'bottleneck': 'r3-B7', 'role': 'c',
     'source': 'SPRIND, Funke Anti-Drone Response 2.0 page', 'version': 'live page fetched 2026-09-30',
     'url': 'https://www.sprind.org/en/actions/challenges/funke-anti-drone-response-2.0',
     'quote': ['The first SPRIND Funke Anti-Drone Response demonstrated that, despite strong and diverse technological '
               'approaches, no team was able to deliver an autonomous, civilian-compatible soft-kill system capable of reacting '
               'consistently, reproducibly, and in line with the specifications.',
               'The challenge: to develop a fully autonomous system capable of neutralizing small and micro UAVs (Unmanned '
               'Aerial Vehicles) of up to 25 kg and 200 km/h autonomously, precisely, and non-destructively in real '
               'time—without explosives, without kinetic means, and without collateral damage.'],
     'raw_file': R + 'sprind_funke_anti_drone_response_2.0.txt',
     'agent_note': 'Programme target: autonomous, non-destructive neutralisation of UAVs up to 25 kg and 200 km/h. Best reported '
                   'from the first edition: no team met the specification (the number of teams and their scores are not '
                   'published on the page). A count of zero, not a measured gap.'},
    {'id': 'r3:59', 'bottleneck': 'r3-B7', 'role': 'd',
     'source': 'SPRIND, Funke Anti-Drone Response 2.0 page', 'version': 'live page fetched 2026-09-30',
     'url': 'https://www.sprind.org/en/actions/challenges/funke-anti-drone-response-2.0',
     'quote': ['We are seeking adaptive solutions that can reliably detect and clearly classify threats and respond with '
               'situation-appropriate, reversible measures such as guided interception, controlled redirection, blocking, or '
               'safe retrieval.',
               'Reversible interception mechanisms can reliably halt unauthorized UAVs or safely recover fly-aways.'],
     'raw_file': R + 'sprind_funke_anti_drone_response_2.0.txt',
     'agent_note': 'Families sought: detect-classify-respond pipelines with reversible (soft-kill) effectors: guided '
                   'interception, redirection, blocking, capture.'},
    {'id': 'r3:60', 'bottleneck': 'r3-B7', 'role': 'd',
     'source': 'Xie et al., CST Anti-UAV (Introduction; Sec. 4.3)', 'version': 'arXiv v2, 19 Nov 2025',
     'url': 'https://arxiv.org/abs/2507.23473v2',
     'quote': ['Most existing SOT datasets [33, 45, 50, 51] are based on visible light images, leading to unreliable tracking '
               'results in low-light or foggy conditions.',
               'Among these, the OV attribute exhibits a pronounced bimodal distribution in performance, with peak performance '
               'at 65.77% and minimum performance dropping to 14.53%. This highlights the critical importance of re-localizing '
               'the target when it reappears.',
               'Occluded objects do not experience significant positional changes when reappearing, making them easier to '
               'locate than out-of-view ones.',
               'We conducted all experiments on a server equipped with 8 NVIDIA A100-PCIE-40GB GPUs'],
     'raw_file': R + '2507.23473v2.txt',
     'agent_note': 'Families: thermal-infrared sensing (for low light and fog); single-object trackers (transformer, Siamese, '
                   'global re-detection) trained offline per dataset. Assumption about interruptions: trackers do well when the '
                   'target reappears where it vanished (occlusion) and poorly after out-of-view gaps (OV), where re-localization '
                   'is needed. Retraining 20 trackers used 8 A100 GPUs.'},
]

BOTTLENECKS = [
    {'id': 'r3-B1', 'name': 'Endurance and energy of small battery-electric multirotors',
     'problem': 'Small multirotors carrying a useful or autonomy payload stay aloft for tens of minutes; missions longer than one '
                'battery need landings and swaps, and drop-in alternatives do not yet beat lithium on specific energy.',
     'open': True,
     'benchmark': 'mission range on one battery in the SPRIN-D Funke Fully Autonomous Flight (9 km course, 2 h slot; Werner et al. '
                  'Table I); specific energy of the power source against lithium-ion (Williamson et al.)',
     'best': 'longest competition flight 1371 m (977 s), ended on low battery; thermoelectric prototype 30 Wh/kg at 1.8% '
             'efficiency; best TE module 12% (modelled parity only)',
     'target': 'the 9 km course (programme task); lithium-ion 200 Wh/kg (parity); TE efficiency more than 2x 12% for VTOL '
               'multicopter endurance parity',
     'gap_note': 'range per flight 1371/9000 = 15% of the course (about 6.6 battery-limited flights per course); the prototype '
                 'reaches 30/200 = 15% of lithium-ion specific energy. CONTESTED for other carriers: a liquid-hydrogen '
                 'multirotor flew 12 h 7 min 5 s (Guinness, 2019, payload not stated), so the bottleneck holds for '
                 'battery-electric small multirotors with payload, not for multirotors as such. The two c-claims are from '
                 'different papers and are not combined.',
     'assumptions': ['flight planned to one battery\'s clock (10-30 min); a longer mission is cut into flights at battery '
                     'boundaries (land, swap, relaunch) - clock and boundaries',
                     'tethering or power beaming: an uninterrupted external supply from fixed infrastructure that is assumed '
                     'always present - interruptions',
                     'hybrid hydrocarbon or fuel-cell generation with a battery buffer for transients; fixed conversion '
                     'efficiency',
                     'fixed wing instead of rotor: gives up hover',
                     'online adaptation to battery depletion (estimate maximum motor RPM in real time and re-plan): '
                     'state-indexed rather than clock-indexed, adds no energy'],
     'cpu_testable': False,
     'cpu_note': 'energy storage and flight endurance are hardware properties measured in flight; an energy-budget simulation of '
                 'battery swaps against a mission could run on CPU in minutes but would not be the benchmark'},
    {'id': 'r3-B2', 'name': 'GNSS-denied long-range navigation (drift over kilometres at low altitude)',
     'problem': 'Without GNSS, odometry drifts without bound over unseen kilometre-scale routes at low altitude, where loop '
                'closures and satellite-image matching are not available or not reliable.',
     'open': True,
     'benchmark': 'SPRIN-D Funke Fully Autonomous Flight (Sep 2024): 9 km waypoint course below 25 m AGL without GNSS or prior '
                  'dense mapping; localization RMSE and waypoints reached (Werner et al. Table I)',
     'best': 'winner: longest flight 1371 m with 4/4 waypoints, localization RMSE below 11 m (7 m against 53 m for odometry on '
             'flight 232); only 3 of 9 teams flew more than 100 m autonomously',
     'target': 'the 9 km track with 27 waypoints and a package pick-up at the last (programme task, SPRIND 2024); SPRIND 2.0 '
               '(2025-26): safe navigation without GNSS or human intervention',
     'gap_note': 'longest flight 1.371 km = 15% of the 9 km course; the paper does not report the course completed; flights over '
                 '1 km ended on battery, not drift, so range is jointly limited by energy (r3-B1) and by the local map size '
                 'that capped speed. The 2025-26 second edition published no metrics. Ground truth in competition is '
                 'approximate (0-5 m).',
     'assumptions': ['odometry corrected by loop closures: assumes revisits, i.e. a memory of places, absent on long unseen '
                     'routes - memory',
                     'SLAM: memory and compute grow with the environment - memory',
                     'satellite-image matching: assumes a viewpoint close to the map\'s (fails below 25 m)',
                     'prior-geodata heightmap matching with a particle filter: assumes the prior map matches the present terrain '
                     'and has structure; in open fields it falls back to odometry',
                     'bounded local map traded against flight speed and range; compass alignment with slowly drifting bias',
                     'programme-listed alternatives: ultra-wideband (installed beacons), magnetic-field navigation (a magnetic '
                     'map)'],
     'cpu_testable': False,
     'cpu_note': 'the benchmark is a field course flown by real drones; the winning localization itself runs on CPU-only onboard '
                 'hardware, so a replay on recorded flight data could run on CPU if the data are public (supplementary site '
                 'named in the paper, not checked)'},
    {'id': 'r3-B3', 'name': 'Perception in adverse conditions (fog and haze) for airborne detection and tracking',
     'problem': 'Fog and haze remove the contrast that small, distant airborne targets need; detection and tracking lose '
                'targets, mostly by missed detections, and real adverse-weather drone data are scarce.',
     'open': True,
     'benchmark': 'DUT Anti-UAV sample videos with depth-aware synthetic fog (beta up to 3.6), YOLO11 + ByteTrack MOTA '
                  '(Pouladi et al. Table 3); HazyDet real-haze mAP (Feng et al.)',
     'best': 'MOTA at beta = 3.6 (best over detector, training regime, foggy or restored input): V02 0.771, V03 0.940, V06 '
             '0.960, V10 0.179; HazyDet real-haze best mAP 38.7 (no clear-weather reference)',
     'target': 'oracle: the best clean-condition MOTA on the same video: V02 1.000, V03 0.980, V06 0.995, V10 0.321',
     'gap_note': 'gaps 0.229 (V02), 0.040 (V03), 0.035 (V06), 0.142 (V10; 56% retained). Clean-trained detectors collapse at '
                 'beta = 3.6 (MOTA 0.000-0.250 on V02, V03, V06). Fog-inclusive training nearly closes the gap on 2 of 4 '
                 'videos, so the reading is open on the worst sequences only; synthetic fog, 4 sample videos, one tracker. The '
                 'double check may read it CONTESTED.',
     'assumptions': ['fog-inclusive training: the test-time degradation distribution is sampled offline at training time - '
                     'tuning, boundaries of the training set',
                     'test-time restoration (dehazing): the degradation model is known and stationary',
                     'synthetic data from a scattering model because real foggy data are hard to collect',
                     'staged fine-tuning (clear -> synthetic haze -> real haze) with designer-set stage boundaries',
                     'tracking-by-detection: a target lost by the detector is not recovered by the tracker'],
     'cpu_testable': False,
     'cpu_note': 'the named benchmark retrains three YOLO11 sizes under three regimes for 100 epochs (GPU-scale); synthetic fog '
                 'generation and inference with a pretrained YOLO11n on the four public DUT Anti-UAV videos could run on CPU '
                 'in hours as a proxy'},
    {'id': 'r3-B4', 'name': 'Agile flight against human pilots (autonomous drone racing)',
     'problem': 'Whether autonomous drones can fly agile, high-speed courses as well as expert human pilots with onboard sensing '
                'and compute only.',
     'open': False,
     'benchmark': 'A2RL x DCL 2025 AI-vs-human knockout (organiser-designed drone and track, one forward camera)',
     'best': 'TU Delft AI won the knockout against three former DCL world champions, up to 95.8 km/h',
     'target': 'human champion pilots',
     'gap_note': 'not shown open: the source states the target reached on this metric (15 Apr 2025, in an externally organised '
                 'race). The residual problem the 2025 sources state - generality to unseen tracks, drones and unstructured '
                 'environments, where humans adapt - carries no number against a target in the sources found.',
     'assumptions': ['known track and drone; policy trained in simulation by RL for that task - boundaries given, tuning offline',
                     'end-to-end neural control directly to the motors under tight compute and energy budgets',
                     'modular pipelines assume the structured setting they were designed for',
                     'online parameter estimation whose estimates drift over time'],
     'cpu_testable': False,
     'cpu_note': 'the benchmark is a physical race against human pilots; a simulated racing proxy could run on CPU but would not '
                 'be the benchmark or its human baseline'},
    {'id': 'r3-B5', 'name': 'C2 link reliability and lost-link behaviour for BVLOS (commercial networks; jammed spectrum)',
     'problem': 'BVLOS drones depend on a command-and-control link that commercial networks do not deliver at the required '
                'reliability and latency, and that jamming removes; the response to link loss is a timeout and a '
                'predetermined action.',
     'open': True,
     'benchmark': 'in-flight packet delivery and RTT over commercial LTE and Starlink (rural Kansas, >10 flights, 4.5+ h, 18K '
                  'samples; Chintareddy et al.)',
     'best': 'packet delivery 99.44% (LTE), 99.31% (Starlink); RTT: Starlink 95% < 50 ms, LTE 80% < 150 ms; worst handover RTT '
             'increase 275 ms',
     'target': '99.9% C2 reliability and sub-100 ms one-way delay (as stated in the same paper, citing field evaluations)',
     'gap_note': 'loss 0.56% (LTE) and 0.69% (Starlink) against 0.1% allowed: 5.6x and 6.9x; at least 20% of LTE RTTs exceed 150 '
                 'ms, and neither link\'s 99.9th-percentile latency is reported. The authors judge the rates sufficient for '
                 'data transfer; the C2 comparison is the agent\'s. Test traffic, not a C2 protocol; one rural area, one '
                 'carrier. Contested-spectrum context (RUSI, 2025): jamming of command and navigation links is ubiquitous; not '
                 'quantified as a C2 metric.',
     'assumptions': ['link loss declared by a timeout on the clock; response a predetermined action (return to home, loiter, '
                     'continue) fixed before flight; timeout value left to industry standards - clock, interruptions',
                     'C2 performance specified by transaction expiration time, availability, continuity, integrity (EASA) - '
                     'clock',
                     'redundancy by dual links (LTE + LEO) with failover: assumes the links do not fail together',
                     'cellular handover triggers (fixed dB thresholds) designed for ground users fire 3-4x more at altitude',
                     'under jamming: remove the radio link (fibre spool, about 10 km), autonomous terminal guidance, or planned '
                     'windows (pauses in friendly jamming) that make operations periodic rather than continuous - '
                     'interruptions scheduled',
                     'reliability shown by 150 clocked flight hours without failure; maintenance by time in service, calendar '
                     'time or cycles - clock'],
     'cpu_testable': False,
     'cpu_note': 'the benchmark is an in-flight radio measurement; a lost-link simulation (timeout policies against a link model) '
                 'could run on CPU in minutes, but it would not be the measured link'},
    {'id': 'r3-B6', 'name': 'BVLOS detect-and-avoid of non-cooperative aircraft by small UAS',
     'problem': 'Routine BVLOS needs small drones to detect and avoid aircraft that do not broadcast their position; mid-air '
                'collision risk is named by the UK regulator as the most significant barrier, and no small-UAS approach has '
                'passed from prototype to a standardised subsystem.',
     'open': True,
     'benchmark': 'logic NMAC risk ratio of a vision-only DAA (ViSafe) in digital-twin hardware-in-the-loop encounter sets '
                  '(4000-6000 encounters per scenario; Kapoor et al. Table II)',
     'best': 'NMAC RR 0.439 (overtake), 0.5248 (crossing), 0.55 (head-on); 0.1 above the horizon, 0.91 below it; real world '
             '0.667 below the horizon (6 encounters)',
     'target': 'UK CAA CAP 3015 v2 DAA02: non-cooperative NMAC RR <= 0.3, LWC RR <= 0.5 (NMAC 500 ft / +/-100 ft); ASTM '
               'non-cooperative NMAC RR 0.3, LoWC 0.5 (ASSURE A65); human baseline: modelled GA pilot see-and-avoid NMAC RR '
               '0.625 (ownship only) / 0.331 (both)',
     'gap_note': 'head-on/overtake/crossing RRs are 1.46-1.83x the allowed 0.3; below the horizon 3.0x; above the horizon '
                 'meets it. CROSS-DOCUMENT and protocol-different: ViSafe\'s NMAC is its own unsafe distance between small '
                 'drones, not the regulatory 500 ft volume around manned aircraft, so the gap is indicative. ViSafe beats the '
                 'modelled human own-only baseline (0.625). No final FAA Part 108 rule on 2026-09-30; UK DAA-enabled BVLOS is '
                 'in a policy test phase.',
     'assumptions': ['qualification by fast-time encounter simulation on encounter models built from long-term historical '
                     'traffic; simulation count set by convergence of the risk ratio within 5% - stationarity of traffic',
                     'fixed protection volumes and alerting times (tau thresholds) - clock',
                     'control barrier function avoidance: constant-velocity, non-reacting intruder, planar manoeuvres, '
                     'hand-tuned hyperparameters - tuning',
                     'reaction window bounded by detection range (287 m / 525 m -> 14.35 s / 13.12 s)',
                     'strategic deconfliction of shared intent before flight: assumes all UAS participate',
                     'cooperative route: make every aircraft broadcast (electronic conspicuity mandate), assumes universal '
                     'equipage; low-risk airspace: a fixed avoidance manoeuvre (rapid descent)'],
     'cpu_testable': True,
     'cpu_note': 'the regulatory metric is itself a fast-time simulation: CAP 3015 allows a deterministic framework "without '
                 'requiring extensive computational resources" and gives an example non-cooperative EO sensor model, so a '
                 'logic risk ratio for a given avoidance logic over 10^4-10^5 encounters is CPU work of minutes to hours; '
                 'ViSafe\'s learned perception and Isaac Sim digital twin are not'},
    {'id': 'r3-B7', 'name': 'Counter-UAS: tracking tiny drones in complex scenes and non-destructive interception',
     'problem': 'Small drones are cheap, fast and increasingly autonomous; trackers lose tiny targets in complex scenes, and no '
                'autonomous civilian soft-kill system has met a public specification.',
     'open': True,
     'benchmark': 'CST Anti-UAV thermal-infrared single-object tracking, mean state accuracy (Xie et al. Table 3); SPRIND Funke '
                  'Anti-Drone Response specification',
     'best': 'mSA 35.92 (GlobalTrack, trained and tested on CST); first SPRIND Funke: no team met the specification',
     'target': 'oracle SA 100 (reference: 67.69 on Anti-UAV410); SPRIND: autonomous non-destructive neutralisation of UAVs up to '
               '25 kg and 200 km/h',
     'gap_note': '64.08 points below the oracle; the best score falls 31.77 points from Anti-UAV410 to CST (GlobalTrack loses '
                 '30.50, SiamDT 31.85; same paper, same metric); SPRIND gives a count of zero teams meeting the specification, not a measured gap (number of '
                 'teams not published).',
     'assumptions': ['single-object trackers trained offline per dataset; accuracy about halves on a harder distribution - '
                     'tuning, boundaries',
                     'continuity after interruptions: targets reappearing where they vanished (occlusion) are easy, out-of-view '
                     'gaps need re-localization and score as low as 14.53% - interruptions',
                     'thermal-infrared sensing to survive low light and fog',
                     'detect-classify-respond pipelines with reversible effectors (guided interception, redirection, blocking, '
                     'capture)'],
     'cpu_testable': False,
     'cpu_note': 'the named results retrain 20 trackers on 8 A100 GPUs; evaluating one pretrained tracker on the public 240k-frame '
                 'CST test data could run on CPU in hours as a proxy; interception is a field trial'},
]
