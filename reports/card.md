# CARD: "change has its own clock" on the cardiac pulse (lab L03)

**How the study ran.**
- **Pre-registration.** `prereg/card/PREREG.md`, signed tag `prereg-card-2026-09-15` at 0c8fe04. Anchor: push-timestamp only,
  as registered. The hash was verified OK on 2026-09-26.
- **Why it ran now.** It was run as lab L03 (`labs/L03_pulse/LAB.md`; prompt-log entry 221; AGENT_LOG 164–165).
- **Data.** PhysioNet Autonomic Aging 1.0.0, records 0061–0090, first 600 s. Fetched after decision commit aaf7acd; the
  manifest is `data/manifests/card.sha256`.
- **Scoring.** The frozen scorer `runs/card/frozen/card_score.py`, as committed. Output in `runs/card/score.txt`, from
  `runs/card/results.jsonl`, rerun check in `runs/card/rerun_cmp.txt`.

This report is written after the ledger rows CARD-1..3 and quotes them.

## Result

| row | prediction | observed | verdict |
|---|---|---|---|
| CARD-1 | H-L5 on blood pressure: per record, the arc per beat is more regular than the RR interval, beyond the amplitude control | 1/29 records pass (0.034, binomial p 0.0000); plain cv_arc < cv_clock in 8/29; 1 excluded (0065, flat channel) | **FAIL**, not fragile (0/26 sensitivity cells differ) |
| CARD-2 | the same on the ECG trace | 5/29 records pass (0.172, p 0.0005); plain cv_arc < cv_clock in 19/29 | **FAIL**, not fragile (0/26) |
| CARD-3 | diagnostic only: antipodal-cut arc against peak-cut arc | 5/28 records | no verdict (not a hypothesis: gate_A3) |

**H-L5 fails on its second real carrier**, as it did on measles (MEAS2-1: 0/17 cities).
- **On blood pressure the RR clock is the regular quantity.** In the primary cell, the bare inequality cv_arc < cv_clock
  holds in only 8/29 records. Where it holds, the pulse amplitude usually ties or beats the arc, so control (i) fails.
- **The one passing record is 0070:** cv_arc 0.051, cv_clock 0.072, cv_amp 0.064, with both CIs below 0.
- **ECG.** The bare inequality holds more often (19/29), but the QRS amplitude is as regular in most of those records, as
  the pre-registration expected.

## Sensitivity and exclusions

**The detector grid.** Low edge ∈ {4, 5, 8} Hz × high edge ∈ {12, 15, 20} Hz × refractory ∈ {200, 250, 300} ms, which
gives 26 non-primary cells. The per-cell table is in `runs/card/score.txt`.
- CARD-1 reads FAIL in every cell: between 0/28 and 1/29 records pass.
- CARD-2 reads FAIL in every cell: between 0/28 and 6/29.

**Exclusions.**
- 0065 is the primary cell's only exclusion (flat channel).
- The cells with a 12 Hz high edge exclude 2 records (28 scored); the per-cell counts are in the score table.

**A carrier-admissibility observation (reported, not acted on; R6).**
- **What was seen.** Three records' BP channels, 0069, 0085 and 0088, have ρ of 670.9, 619.6 and 316.9, an amplitude CV of
  0.004–0.006, and about 60,000 antipodal cuts in 600 s (CARD-3 lines). A fast oscillation dominates their analytic
  phase. The pre-registered quality gate, flat channel or ρ < 3, does not catch this.
- **Why it doesn't matter to the verdict.** None of the three is the passing record 0070. Removing any or all of them
  cannot raise the pass fraction toward 0.60, so the verdict cannot change.
- **What happens next.** A replication must name an admissibility rule for this before its hash.

## What this means for H-L5 and for the labs

- **The heartbeat is clock-regular.** The autonomic control of the RR interval keeps the interval more regular than the
  pressure excursion per beat. So H-L5's claim that "change has its own clock" is false for this system under this
  carrier and metric.
- **Two carriers, two failures.** With measles, H-L5 has now failed on both real carriers tested, neither fragile. Its only
  "arc-regular" case on the record is the adder, where the arc is the amplitude by P1 (Life_Sciences CD-1), so H-L5 there
  says nothing beyond its control.
- **No PASS-0 or PASS-1 was possible.** The anchor is push-timestamp only. The pre-registration's replication clause
  (OTS-anchored, records 0091–0120) was written for a PASS and is not triggered by a FAIL. Running it would be a new
  pre-registration, justified only by a changed carrier or unit decided before the data (R3), never by the hope of a
  different answer.

## What a surrogate would have done

`prereg/card/gate_L5.txt` (hashed 2026-09-15) reads GATE OPEN:
- the clock-regular surrogates (the AM sine and S-G) FAIL;
- the arc-regular surrogates (the FM sine and S-G2) PASS.

So the instrument separates the two classes. On these 29 records it places the cardiac pulse in the clock-regular class,
beside S-G and the measles cycle.
