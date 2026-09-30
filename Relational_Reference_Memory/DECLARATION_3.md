# Declaration 3: RRM where the features actually drift (POST HOC; pushed before T7 runs)

**Why (post hoc, stated).** T1 found that the SEC1 learner's hidden features barely move after each cut.
- On POS, the stale prototype's mean error against the true current mean is 0.1197 (FT) to 0.1926 (ER20), where the
  scrambled-anchor decoy's is about 6.7 (`checks/t1_diag.txt`).
- T3 found nearest-mean with **stale** prototypes level with the true current prototypes: 85.35 against 85.22 on POS
  (`checks/t3_ncm.txt`).
- So on this learner, forgetting lives in the head, not in drift. The mechanism the owner proposed (prompt-log entry 248)
  has almost nothing to correct.
- Repeated testing "in different ways" (prompt-log entry 250) therefore needs a regime in which features drift. This
  declaration is written after T1–T3 were seen. It is exploratory (rung R4 on the synthetic streams, R5 on SEEN data),
  report-only, with no gate and no ledger PASS. The Part W verdict (NOT WORTH PURSUING) stands; no unseen data will be
  opened.

## T7: the drift-rich regime (`checks/t7_drift.py`)

**The learners and their settings.**
- The same SEC1 MLP, learners and anchors as T1, T2 and T3, with the **epochs per task E ∈ {3, 15, 30}**.
- E = 3 reproduces T1 and T2. More epochs on each task moves the hidden layer further from each cut.
- Nothing else changes: lr 0.05, batch 10, 256 hidden units, β = 0.01, 20 first-task anchors, and HopDC's τ = 0.05 and
  k = min(400, M).

**What is reported per E, on POS, NEG2 and the 30 SEEN carriers (seeds 0–4).**
- **Relative drift:** mean over old classes of ‖μ_cut − μ_now‖ / ‖μ_now‖, for the FT, ANCH1 and ER20 learners.
- **Drift explained,** 1 − err / err_STALE, for RRM and for HOPDC.
- **NCM accuracy** on the ANCH1 learner, with STALE, RRM, HOPDC and ORACLE prototypes.
- **Learner accuracy** for STALE-1, RRM-1, HOPDC-1 and ER-20 (ER-20 via `t_lib.train`, with the same E).

**Forecasts (written now).**
1. Relative drift rises with E, on POS and on at least two thirds of the SEEN carriers.
2. RRM explains more drift than HOPDC at every E on POS and NEG2. T1 already showed this at E = 3 (RRM's error below
   HOPDC's on 5/5 seeds in every cell), so this forecast is not blind at E = 3.
3. RRM − STALE (learner accuracy) grows with E, but stays within one step of zero on POS at E = 15.
4. At E = 30, NCM-RRM is ahead of NCM-STALE by more than one step on POS. This is the only forecast that, if it held,
   would show the owner's mechanism doing real work.

No threshold here decides anything. The forecasts are scored by the script (held / not held), so the record shows how
often the investigator's expectations were right.
