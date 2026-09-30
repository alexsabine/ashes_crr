# RRM Phase A: the result (part 1 GATE CLOSED; part 2 not run)

**What was tested.** The owner's object-relations reading (prompt-log entry 248), translated in `DECLARATION.md` (3a740f1).
Each class's settled content is stored as a relation to kept anchors. When the learner changes, the content is rebuilt
from the anchors' current features.

**Part 1:** controlled drift worlds, with no learner (`checks/worlds.py`, output `checks/worlds.txt`, pinned; the rerun
is byte-identical). The transport was also checked on its own before pinning: the relative error falls from 0.0034 at
β = 0.01 to 3.5e-09 at β = 1e-8 for a feature in the anchors' span, under a linear change. That check was printed in the
session, not pinned.

## The gate, as declared (all conditions, both forms)

| condition | RRM-1 (the owner's "first object") | RRM-A (accumulating anchors) |
|---|---|---|
| G-SHARED on SHARED: ahead of STALE, within a step of ORACLE | holds: +3.0769 over STALE; ORACLE − RRM +0.9365 (step 1.6736) | holds: +2.9431; +1.0702 |
| G-SHARED on ROT | holds: +4.0803; ORACLE − RRM +1.0702 (step 1.1072) | **FAILS**: +3.3445 over STALE, but ORACLE − RRM +1.8060 (step 1.1072) |
| G-UNSHARED: ORACLE ahead by more than a step | holds: +32.8428 | holds: +33.5786 |
| G-DECOY: ahead of permuted anchors | holds: +48.4281 | holds: +37.7258 |

**PART 1 GATE CLOSED** on one of eight conditions. RRM stops at Phase A (R12). Part 2 (the learner), the development
stage and any pre-registration were not run. Ledger row **RRM-PA**.

## What part 1 does show (synthetic, rung R4; not evidence)

- **The owner's form cleared every condition.**
  - Anchors are taken from the first task only; every later class is stored relative to them.
  - Under shared change it recovered most of the drift: within 0.94 of the oracle under a linear change and 1.07 under a
    rotation, against the stale memory's shortfall.
  - It failed where it must fail: the change is not shared (UNSHARED), and the anchors are scrambled (DECOY).
- **The accumulating form fell short of the oracle by more than a step under rotation.** It was still ahead of the stale
  memory (+3.3445).
  - A likely reason, not tested: at the first cut it holds only 4 anchors (2 per class), so the earliest classes are
    related to a 4-dimensional span, and the rest of each feature is carried stale.
  - The owner's form holds 20 anchors from the start. In the owner's terms, a rich first object served better than a thin
    reference that grows. This is a reading of one synthetic run.
- **Relations carry information even when nothing is shared.** Under UNSHARED, where the map is redrawn completely, the
  stale memory fell to chance (10.84), yet the relational memory kept 52.64 (RRM-1) and 51.91 (RRM-A).
  - The transported prototype is partly re-expressed as a combination of the anchors' new features. So the relation
    survives some change that is not a shared linear map.
  - This was not declared as a claim, and it is reported only.

## What would be needed to go on (not run; the owner's decision)

- **A new declared study (RRM2) with RRM-1 only.**
  - RRM2's part 1 would not be blind: its result is already known from this run and must be disclosed.
  - The declared learner gate (G-REL, G-CANFAIL, G-FT, G-ID) would then decide whether the mechanism does anything in a
    learner whose features actually drift.
  - The forecast in DECLARATION.md §7 was that it probably would not.
- **Rejected here:** dropping the failed form and continuing under this declaration. That would change a declared gate
  after its result (CLAUDE.md §10).

## The literature grade of N1–N6 (DECLARATION.md §6; `checks/grade.txt`, pinned, CI-checked)

**The sweep:** 37 claims from 27 sources (`docs/citations/rrm_2026-09-30.md`). `checks/verify.py` found 58 of 58 quotes
verbatim in the fetched texts. No source contradicts any position.

| | position | grade | forecast | |
|---|---|---|---|---|
| N1 | drift correction of stored statistics by measuring how reference points move | REDUNDANT | REDUNDANT | hit |
| N2 | that drift estimated from kept old-class rows rather than current data | PARTLY REDUNDANT | PARTLY REDUNDANT | hit |
| N3 | anchor-relative representations are invariant to angle-preserving change | REDUNDANT | REDUNDANT | hit |
| N4 | preserving relations between samples reduces forgetting | REDUNDANT | REDUNDANT | hit |
| N5 | the RRM transport itself | PARTLY REDUNDANT | PARTLY REDUNDANT | hit |
| N6 | developmental framings used to design continual learners | REDUNDANT | PARTLY REDUNDANT | miss |

**The judgement calls** (the grading agent's, kept as pinned, R15):
- **N5 was not found published**; each part exists separately. The nearest:
  - **GATF** (arXiv 2606.25347 v2) carries stored class Gaussians by a ridge-regularised linear map fitted on
    **current-task** features, not on kept anchors.
  - **MPT** (arXiv 2609.12771 v1, federated) splits a class prototype into an in-span part, expressed by its relation to
    other classes' live prototypes, and a residual. That is the nearest form of the owner's reading, but its references
    are not kept anchors.
  - **Maiorca et al.** (arXiv 2311.00664 v2) fit the transport between two separate models.
  - A one-day arXiv keyword sweep is not a novelty search. "Not found" is never "novel".
- **N6** is graded REDUNDANT on the developmental framing alone: Parisi et al.'s review (arXiv 1802.07569 v4) presents
  critical periods and coarse-to-fine staging as design sources. If N6 needs the owner's specific framing (a first
  reference object, rising resolution), nothing states it, and it would be PARTLY REDUNDANT. No source applying
  psychoanalytic object-relations theory to machine learning was found.
