# Declaration 2: is RRM worth pursuing? The frontier sweep, and the overnight tests (pushed before any search or run)

**The request.** Prompt-log entry 250 (2026-09-30T03:46Z): "I'd like to run a full literature sweep first please ...
Please check contemporary frontier literature to verify that this is worth pursuing, before we continue. I am going to
bed now so please keep working overnight on testing the idea repeatedly in different ways."

**What "this" is.** Replay-quality memory without keeping the data, pursued through RRM-1:
- the owner's first-object form of relational reference memory (`DECLARATION.md`);
- part 1 passed all of its conditions (`PHASE_A.md`); the declared gate closed on the other form.

**Order.** The sweep runs first, and its verdict is computed and pushed before any learner test runs. The synthetic and
SEEN-data tests below run either way (the owner asked for repeated testing), but **no unseen data is opened unless the
verdict is WORTH PURSUING** and the development gate opens.

## Part W: the frontier sweep (2025–2026 first; older only as needed)

**Three dossiers:** `docs/citations/rrm2_f{1,2,3}_2026-09-30.md`.
- **Sources.** arXiv search, and where reachable, CVF open access, OpenReview and the proceedings of CVPR, ICCV and
  ECCV 2025, NeurIPS 2025 and ICLR 2026. Every quote is verified against its fetched text, and current versions are
  noted (R10). Claims go in `checks/claims_w{1,2,3}.py`; quotes are checked by `checks/verify_w.py` and graded by
  `checks/grade_w.py`. Reading policy and grade rule as RQM.
- **The families.**
  - **F1:** the state of the art in exemplar-free and small-memory class-IL, and the remaining gap to replay (P1, P2).
  - **F2:** hybrids of a few exemplars with class statistics, drift transport, and linear drift maps; a deeper search
    for P5 (P3, P5, P7).
  - **F3:** anchors and relative representations inside one continual learner, and on-device or privacy-constrained
    settings (P4, P6).

**Positions graded, with the investigator's forecast (written now).**

| id | position | forecast |
|---|---|---|
| P1 | 2025–26 papers still name the drift of stored class statistics as a main limitation of exemplar-free or small-memory class-IL trained from scratch | REDUNDANT |
| P2 | a 2025–26 exemplar-free method trained from scratch reports class-IL accuracy level with or ahead of replay at a realistic buffer, on the same protocol (the gap is closed) | MIXED |
| P3 | hybrids that keep a few exemplars **and** class statistics, and use the kept exemplars to correct the stored statistics, are published | PARTLY REDUNDANT |
| P4 | anchor-relative or relative representations are used inside one continual learner to keep old representations valid | PARTLY REDUNDANT |
| P5 | transporting stored old-class statistics by the measured feature movement of a few **kept** anchors (RRM's transport) is published | PARTLY REDUNDANT |
| P6 | on-device or privacy-constrained continual learning is named as a setting where a small store of raw rows is acceptable and a full replay buffer is not | REDUNDANT |
| P7 | the feature drift of a class-IL learner is reported to be approximately linear, or well corrected by a linear map | MIXED |

**The worth rule (computed by `grade_w.py`).** The verdict is **WORTH PURSUING** if all four hold:
- P1 is REDUNDANT or MIXED (the problem is live);
- P2 is not REDUNDANT (the gap is not closed);
- P3 is not REDUNDANT (the niche is not already filled);
- P5 is not REDUNDANT (the transport is not published).

Otherwise the verdict is **NOT WORTH PURSUING**, and the failing position is named. P4, P6 and P7 are reported, not
gating.

**Forecast:** WORTH PURSUING, narrowly. "Not found" is never "novel". A WORTH verdict means only that a test is not
redundant before it runs.

## Part T: the overnight tests (synthetic and SEEN data only; seeds 0–4; step = max(1, 2 × SE over seeds))

Every script prints its gate words (R15). Outputs are pinned, and reruns are checked byte-identical. A closed gate stops
only the chain that depends on it.

**T1 DIAG: does transport track the real learner's drift?** (`checks/t1_diag.py`)
- **The learners.** The SEC1 MLP is trained as three learners, each with a different drift regime:
  - FT;
  - ANCH-1 (replay of the 20 first-task anchors only);
  - ER-20.
- **The measurement.** At the end of the stream, for each class of the first four tasks:
  - the prototype error ‖p − μ_now‖ against the class's true current feature mean, for p = STALE (the mean at the cut),
    RRM (transported by the 20 first-task anchors, β = 0.01) and DECOY (permuted anchors);
  - the drift explained, 1 − err_RRM / err_STALE.
  - Nearest-class-mean accuracy over all classes with each set of prototypes, plus ORACLE (true current means).
- **The streams:** POS, NEG2 and the 30 SEEN carriers.
- **Gate T1**, on POS and NEG2 for each learner:
  - RRM's error is below STALE's on at least 4 of 5 seeds;
  - DECOY's error is above STALE's on at least 4 of 5 seeds.
  - The SEEN carriers are report-only: per carrier, the mean drift explained and NCM RRM − STALE.

**T2: the learner gate for RRM-1 alone** (`checks/t2_learner.py`; DECLARATION.md §4, RRM-1 only)
- **Disclosure:** part 1 is not blind for this form. Its result is known.
- **G-REL:** on POS, RRM-1 is ahead of STALE-1 by more than a step.
- **G-CANFAIL:** DECOY-1 is behind ER-20 by more than a step on POS and on NEG2.
- **G-FT** and **G-ID** as declared.
- Reported: RRM-1 − ANCH-1, − ER-20, − JOINT, − IGR-F and − RFR.

**T3: relational NCM, SDC-style classification without replay** (`checks/t3_ncm.py`)
- **The learner:** ANCH-1.
- **At the end:** classify by the nearest prototype in feature space, with prototypes STALE, RRM, DECOY or ORACLE.
  This is the use SDC makes of drift compensation, with kept anchors instead of current-task data.
- **Gate T3:** on POS, NCM-RRM is ahead of NCM-STALE by more than a step, and NCM-DECOY is behind NCM-STALE by more
  than a step.
- **Reported:** NCM-RRM against ANCH-1's own softmax head, and on the 30 SEEN carriers.

**T4: sensitivity** (`checks/t4_sens.py`; report only; drift worlds of DECLARATION.md §3, and T1 DIAG on POS)
- anchors per first-task class ∈ {2, 5, 10, 20};
- β ∈ {0.001, 0.01, 0.1};
- anchor source ∈ {first task only; 20 anchors spread evenly over all tasks, which uses future data and is marked as an
  oracle design};
- the drift rate ε ∈ {0.02, 0.05, 0.1} in the worlds.

**T5: development on the 30 SEEN carriers** (only if T2's gate opens; `checks/t5_dev.py`)
- DECLARATION.md §5 for RRM-1 alone (no selection).
- **D-COUNT:** not behind ER-20 on at least ⌈0.75 N_dev⌉ carriers.
- **D-REL:** ahead of STALE-1 on at least one third of the carriers.

**T6: pre-registration** (only if the Part W verdict is WORTH PURSUING **and** T5's D-GATE opens)
- `prereg/rrm2/`, with the shape of DECLARATION.md §5, hashed and OTS-stamped.
- The data step is not before 2026-10-01 00:00 UTC (R3).

**Forecasts (written now):**
- T1 holds on POS for the anchor learner. Its drift explained is well below 1, because the MLP's drift is not linear.
- T2 closes at G-REL (DECLARATION.md §7's forecast, unchanged).
- T3 holds.
- T5 is not reached.

## Amendment 1 (2026-09-30, after the sweep and before any Part T run; AGENT_LOG 198)

**The verdict.** Part W's verdict (`checks/grade_w.txt`, pinned) is **NOT WORTH PURSUING; failing: P5 (the transport is
published)**.
- **The deciding source** is HopDC (Rao et al., arXiv 2602.00144 v1, 29 Jan 2026).
  - It keeps a fixed anchor set for the whole stream and stores the anchors' features.
  - It measures the anchors' drift and moves pseudo-features sampled from each stored class Gaussian by a
    similarity-weighted average of that drift.
- **The reading.** The grading agent read it "close"; the investigator reads it "states" on P5's declared predicates.
  - Anchor provenance and the relation's form are not predicates of P5.
  - Under the agent's reading, P5 is PARTLY REDUNDANT and the verdict is WORTH PURSUING. That output is pinned as
    `checks/grade_w_run1.txt`: a script error ran the grade once before the review was applied.
- **Consequence.** As declared, T6 (pre-registration) is off. No unseen data will be opened for RRM.

**The addition (R7: the closest published method).** A **HOPDC** arm is added as a reported baseline, never gating, to
T1 (prototypes), T2 (a learner arm HOPDC-1) and T3 (NCM-HOPDC).
- **The anchors:** the same kept anchors as RRM-1.
- **The relation:** HopDC's transport. The query and the anchors' cut features are ℓ2-normalised; weights are a top-k
  softmax of cosine similarity over τ, with τ = 0.05 and k = min(400, M), HopDC's published values. The query moves by
  the weighted average of the anchors' drift, H_A(now) − H_A(cut).
- **The comparison it answers.** RRM − HOPDC is the one difference left to RRM: a linear ridge relation on the stream's
  own kept rows against HopDC's kernel relation on the same rows.
- **Nothing else changes:** the gates, the thresholds and T1–T5.
