# SEC6: the second replication of SEC4-1 — NOT DECIDABLE (no carrier could be read)

**How it was run.**
- **The request.** Prompt-log entry 257 ("We should then run more tests on sec4"; P2 of `Applied_Suite/PROGRAMME.md`).
- **The development.** `prereg/sec6/DEV_DECLARATION.md` with Amendments 1–3, on SEEN carriers before any SEC6 data.
- **The pre-registration.** `prereg/sec6/PREREG.md`, HASH.txt sha256 69c37965…, prereg commit 1bb1870 pushed
  2026-09-30T09:51:54Z. The signed tag was created; its push was refused, as for SEC3–SEC5 (`runs/sec6/tag_attempt.txt`).
- **The anchor.** OpenTimestamps is complete in Bitcoin blocks 969292, 969296 and 969327 (`runs/sec6/ots_upgrade.txt`).
- **The data step.** 2026-10-01 (R3).
  - The hash was unchanged: 141/141 files OK (`runs/sec6/hash_check_datastep.txt`).
  - The first fetch was cut by a proxy reset during DBPedia (`runs/sec6/fetch_attempt1.txt`). The registered command
    was re-run unchanged from 00:18:10Z (`runs/sec6/fetch.txt`).
  - All 24 raw files matched the manifest, and the d = 0 self-test held (`runs/sec6/data_check.txt`).
- **The runs.** The frozen scorer ran on all twelve carriers (`runs/sec6/exits.txt`). Two of the first runs were
  interrupted by the operator's own kill. Both were re-run from scratch, and each re-run is byte-identical to the first
  output, which had in fact finished (`runs/sec6/interrupted/`). The R9 rerun of air-quality is byte-identical
  (`runs/sec6/rerun_cmp.txt`).
- **The scoring.** `runs/sec6/score.txt`, printed by the frozen scorer.

This report is written after ledger rows SEC6-G … SEC6-K and quotes them.

## The answer

**SEC6 could not test anything. All twelve carriers were excluded by the registered loader, so 0 carriers were scored.
As the pre-registration requires for N < 4, SEC6-1, SEC6-1F, SEC6-B and SEC6-C are NOT DECIDABLE. SEC4-1 is neither
replicated nor contradicted here. Its replication on record remains SEC5-1, which FAILS.**

| row | question | observed | verdict |
|---|---|---|---|
| SEC6-G | is the criterion failed by a learner frozen after task 1? | 0/0; the scorer prints CLOSED at 0/0 | report (vacuous; no level) |
| SEC6-1 | is the clipped SEC within a step of the tuned λ (the replication of SEC4-1)? | 0/0 | NOT DECIDABLE |
| SEC6-1F | the same, on carriers that are not floor-bound | N_F = 0 | NOT DECIDABLE |
| SEC6-C | the same, against the tuned λ given the same clip | 0/0 | NOT DECIDABLE |
| SEC6-B | does the clipped SEC beat SI-1, SI-1C, SI-0.1, AR1-P, AR1-B and raw Laplace? | every arm 0/0 | NOT DECIDABLE |
| SEC6-T | is the saving SEC's (carriers where a transferred λ is behind)? | \|B\| = 0 | NOT DECIDABLE |
| SEC6-2 | no divergence | 0 carriers; the scorer prints PASS | report (vacuous; not PASS-0) |
| SEC6-P | the clipped SEC against the 3-point mini-sweep | 0/0; the scorer prints PASS | report (vacuous; not PASS-0) |
| SEC6-S | sensitivity over 5 cells | 0 cells; the scorer prints "not fragile" | report (vacuous) |
| SEC6-K | compute and guard firings | no run | report |

**The vacuous lines.** The frozen scorer computes its gate, divergence, mini-sweep and sensitivity lines whatever N is.
On 0 carriers it prints CLOSED, PASS, PASS and "not fragile". None of these says anything about the method. The ledger
records the printed word inside a "report (vacuous …)" verdict, so the ladder counts no level for them (AGENT_LOG 241).

## Why every carrier was excluded

`runs/sec6/diagnose_targets.txt` is printed by `studies/sec6/diagnose_targets.py`. It is post hoc and decides nothing.
It imports the frozen reader and parser; it does not copy or edit them.
- **Every carrier declares its class column as an ARFF STRING attribute** (12/12). The suites used by SCL3–SEC5 declared
  nominal targets.
- **The frozen parser (SCL3's, unchanged since SCL3) reads a STRING target as a number.** A class name such as
  "Moderate" raises an error, and the row is dropped. So every row of every carrier was dropped:
  - 666 of 666 on Student_Performance_on_an_Entrance_Examination;
  - 855514 of 855514 on Wikipedia_Talk_Labels;
  - and so for all twelve.
- **The features were not the cause.** Read alone, they would have dropped every row on one carrier
  (regensburg_pediatric_appendicitis, 782 of 782) and some rows on two more (HCV_data 26 of 615, wine_reviews 5578 of
  84123). Three carriers have no usable feature at all and were also excluded by the d = 0 rule (Amendment 1):
  Student_Performance_on_an_Entrance_Examination, WBCAtt and Mental_Health_Dataset.
- **Why the selection did not catch it.** The selection script (`studies/sec6/select_carriers.py`, metadata only) counts
  classes from OpenML's dataset qualities, which do not depend on the ARFF attribute type. Nothing in the development
  stage read a suite-454 file, because development ran on SEEN carriers of the earlier suites.

**What this means.** The frozen scorer did not crash. It ran as registered, and the registered outcome for N < 4 is NOT
DECIDABLE. Reading STRING targets would change the loader, and a scorer changed after the hash makes a study void
(CLAUDE.md §8). So any further test of SEC4-1 needs a fresh pre-registration with a loader that reads STRING targets,
validated on a SEEN carrier before the hash. The twelve SEC6 carriers are now SEEN (`data/SEEN.md`) and cannot be used
in it.

## The SEC family's record after SEC6

- SEC4-1: PASS-1 as scored, on one family.
- SEC5-1: FAIL, the declared replication (4/8, need 6).
- SEC6-1: NOT DECIDABLE (N = 0).
- SEC4-1-G: post hoc, SEC6's own instrument rule would print SEC4-1 UNINFORMATIVE. A learner frozen after task 1 meets
  its criterion on 5 of its 6 carriers.

No PASS-2 exists.

## What a surrogate would have done

No surrogate or synthetic carrier entered the scoring. The synthetic self-tests in `runs/sec6/data_check.txt` passed:
- the d = 0 rule excluded the d = 0 stream and kept the d = 1 stream;
- every SEC6 arm ran on the d = 1 stream.

These self-tests generate numeric streams in memory, so they could not expose a STRING target either. The
instrument-gate logic SEC6-G was built for (P1's frozen learner meeting the criterion) is in
`SEC_Analysis/checks/gate_posthoc.txt`. It was never exercised on SEC6's own carriers, because none was read.
