# L03: H-L5 on the cardiac pulse (L5x), run as the frozen study CARD

**Status.**
- **The request.** Owner request: prompt-log entry 221 (2026-09-26).
- **What L03 is.** The first lab from `labs/CANDIDATES.md`.
- **What this file is.** A pointer, not a new design.

**Why L03 is CARD.**
- **The study already exists.** H-L5 on the Autonomic Aging records was pre-registered on 2026-09-15 as study **CARD**
  (`prereg/card/PREREG.md`), with signed tag `prereg-card-2026-09-15` at commit 0c8fe04.
- **What it covers.** Records 0061–0090, a frozen scorer, and gates L5, CUT and A3 in the hashed folder.
- **Why it never ran.** PhysioNet returned 403 to the environment, and no files were ever supplied.
- **The hash still holds.** On 2026-09-26 `sha256sum -c prereg/card/HASH.txt` gives OK for all 9 files, so the
  pre-registration is intact.
- **No new pre-registration.** Writing one on the same records would be choosing rules after the fact, and R3 allows one
  pre-registration per dataset. L03 therefore runs CARD **as committed**.

**The lab fields.**
1. **Rows.** H-L5 (`theory/CRR.md` §4). Its other real carrier failed: measles, ledger MEAS2-*, 0/17 cities, the
   clock-regular class. On cell size it is empty (Life_Sciences CD-1).
2. **The edge.** Whether the heartbeat is arc-regular or clock-regular is an open empirical question. The field's clock
   quantity (RR intervals, heart-rate variability) and CRR's arc per beat separate on the standing gate (`gate_L5`: OPEN).
3. **The hypotheses.**
   - **H1 (CARD-1):** per record, the blood-pressure arc per beat is more regular than the RR interval, beyond the
     amplitude control.
   - **H0:** the RR clock, the object of the heart-rate-variability literature, is as regular or more so.
   - **The scoring rule:** as in the pre-registration.
4. **The gate.** `prereg/card/gate_L5.txt`, `gate_CUT.txt` and `gate_A3.txt`, hashed on 2026-09-15.
5. **The data.** D1: PhysioNet Autonomic Aging 1.0.0, records 0061–0090, absent from `data/SEEN.md`.
6. **The forecast.** CARD-1 FAIL. The investigator expects the pulse to belong to the clock-regular class, as measles did.
   A heartbeat's pressure excursion (its arc) varies with breathing and with vascular tone while RR is held by autonomic
   control, and the amplitude control (pulse pressure) will likely tie the arc. This is a guess, written before the data.
7. **Stop rules.** The format VOID rule of the pre-registration: fewer than 10 records load with ≥ 200 beats.

**Deviations, decided before any data were fetched (AGENT_LOG 164).**
- **The data route.** The pre-registration expected the human to upload the WFDB files because PhysioNet was unreachable.
  It is reachable now, so the files are fetched directly by `data/fetch_autonomic_aging.py`, with sha256s in
  `data/manifests/card.sha256`. The frozen scorer and its thresholds are unchanged.
- **Anchoring.** It stays as registered: "push-timestamp only". So a PASS here could be PASS-0 at most, never PASS-1
  (strong anchoring is required), and it would need an OTS-anchored replication on 0091–0120, as the pre-registration
  itself says.

## Result (2026-09-27; ledger rows CARD-1..3; `reports/card.md`)

| row | observed | verdict |
|---|---|---|
| CARD-1 | 1/29 records pass (0.034, binomial p 0.0000); plain cv_arc < cv_clock in 8/29; 1 excluded (0065) | **FAIL**, not fragile (0/26 cells differ) |
| CARD-2 | 5/29 records pass (0.172, p 0.0005); plain in 19/29 | **FAIL**, not fragile (0/26) |
| CARD-3 | 5/28 records (diagnostic only) | no verdict |

**The forecast held.** The cardiac pulse is in the clock-regular class. H-L5 has now failed on both real carriers tested:
measles (MEAS2-1) and the pulse (CARD-1).
