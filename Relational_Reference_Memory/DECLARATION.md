# Declaration: RRM, relational reference memory (pushed before any source, code or data)

**Status.**
- **The request.**
  - Prompt-log entry 248 (2026-09-30) is the owner's reading of the RQM bottleneck. Quoted in part: "the relationality
    between the schematic representations is what matters? Mapping the difference from one thing to the next ... every
    face/representational map they experience in the field of reality is measured as a difference between those
    structural resolutions ... each object (person) is a different reflection of the first object".
  - Prompt-log entry 249: "Okay, run the tests please".
- **Follows** RQM (`Replay_Quality_Memory/`, ledger RQM-A: Phase A GATE CLOSED twice, because its criterion could not
  fail) and the answer to entry 248.
- **Rung.** The sweep, the synthetic worlds and the development stage are notes (R8). Only a pre-registered study on
  unseen carriers can produce ledger rows.

## 1. The idea, translated (fixed now)

**The owner's reading, in CRR terms.**
- A class's content settles at its cut (A3).
- The drift bottleneck (RQM B1) is that content written in the learner's own coordinates goes stale when those
  coordinates change.
- The reading: store each settled content **as a relation to a kept reference** (the "first object"), not as absolute
  coordinates. When the learner changes, the reference is seen again through the learner as it is now, and the content
  is rebuilt from its stored relation.
- Differences taken against a shared reference cancel whatever change they share. The mechanism can work only where the
  change is shared: here, linear on the span of the reference's features.

**The machine translation (the candidate, RRM).**
- **Anchors.** A few raw training rows are kept as the reference.
- **At each class's cut, three things are stored:**
  - the class's hidden-layer feature distribution: a diagonal Gaussian over the 256 hidden units;
  - the anchors' hidden features at that cut, H_A(cut);
  - the relation map R = (H_A H_Aᵀ + β̄ I)⁻¹ H_A, where β̄ = β · tr(H_A H_Aᵀ) / M. R gives each feature vector its
    coordinates relative to the anchors.
- **At replay,** a pseudo-feature h is drawn from the stored Gaussian and **transported by the anchors' measured movement**:
  - h′ = h + (H_A(now) − H_A(cut))ᵀ R h;
  - h′ is clipped at 0 (the ReLU range) and replayed into the head, as FGR in RQM.
- **Exactness.** If the features change by any linear map L (h ↦ L h) and h lies in the anchors' span, then as β → 0,
  h′ = L h exactly. Outside the span, the orthogonal part is carried stale.
- **Anchor replay.** The anchors themselves are also replayed through the whole network, as experience replay on the
  anchor rows. They are kept anyway.

**The relaxation, stated.** RQM's target forbade stored raw rows. RRM keeps **M raw rows in total** (the anchors), far
fewer than a replay buffer, plus aggregates. The privacy claim is therefore weaker than RQM's, and the write-up must say so.

**Two forms (named now).**

| form | the reference | M |
|---|---|---|
| **RRM-1** (the owner's "first object") | 10 rows per class of the **first task**, kept for the whole stream; every later class relates to them | 20 |
| **RRM-A** (accumulating) | 2 rows per class are added at each cut; a class's relation uses the anchors kept at its own cut | 2 per class seen |

**Named constants.** β = 0.01. Replay batch: 10 pseudo-features plus 10 anchor rows per step, beside the current batch
of 10.

## 2. Arms (all on SEC1's learner, as RQM; `checks/rrm_lib.py`)

**The candidate and its controls.**

| arm | what it is | role |
|---|---|---|
| **RRM-1, RRM-A** | as §1 | the candidate |
| **STALE-1, STALE-A** | the same anchors (replayed as ER) and the same feature Gaussians, **without transport** | the relational ablation: RRM − STALE is the effect of the owner's idea |
| **DECOY-1, DECOY-A** | as RRM, but H_A(now) is row-permuted against H_A(cut) by a fixed seeded permutation (wrong correspondences) | the must-fail control |

**Baselines.**

| arm | role |
|---|---|
| **ANCH-ER** | ER on the anchor rows alone (no feature Gaussians) |
| **ER-20** | ER with 20 raw rows per class: a realistic buffer, the primary comparator |
| **IGR-F** | RQM's input-space Gaussian replay |
| **RFR** | RQM's frontier exemplar-free baseline |
| **FT, JOINT** | lower and upper bounds |

**Memory.** Every arm's stored raw rows and stored numbers are printed. They are not gated; the primary comparator ER-20
stores more raw rows than any RRM form.

## 3. Phase A, part 1: the mechanism in controlled drift worlds (`checks/worlds.py`; no learner)

**The world.**
- K = 10 Gaussian classes in d = 20 (SEC1's synthetic generator), 2 classes per task.
- A fixed feature map f₀(x) = ReLU(W₀x + b₀), 256 hidden units, seeded.
- Anchors and relations are taken at each class's cut, with the map changing by T = 20 increments per task.
- **Score:** nearest-class-mean accuracy (%) of the current features of held-out rows of all classes, using the
  prototype each method supplies. Seeds 0–4. Step = max(1, 2 × SE over seeds).

**The three drift regimes.**
- **SHARED:** f_t = L_t f₀ with L_t = Π(I + εG_s), G_s i.i.d. N(0, 1/256), ε = 0.05 (a linear, shared change).
- **ROT:** as SHARED, with each factor orthogonalised (an angle-preserving change).
- **UNSHARED:** at every increment W and b are redrawn independently. The map at the end shares nothing with the map
  at the cut.

**The methods.**
- ORACLE: the true current class means.
- STALE: the means at the cut.
- RRM-1 and RRM-A: means transported as §1.
- DECOY: RRM with permuted anchors.

**The gate. All must hold for both forms.**
- **G-SHARED:** on SHARED and on ROT, RRM is ahead of STALE by more than a step, and ORACLE − RRM ≤ a step.
- **G-UNSHARED:** on UNSHARED, ORACLE is ahead of RRM by more than a step. The mechanism must fail where the change is not
  shared.
- **G-DECOY:** on SHARED, RRM is ahead of DECOY by more than a step.

## 4. Phase A, part 2: in the real learner (`checks/phase_a.py`; RQM's POS and NEG2 streams; seeds 0–4)

**The gate. All must hold.**
- **G-REL:** on POS, at least one RRM form is ahead of its STALE by more than a step. The owner's mechanism must do
  something in a learner whose features actually drift.
- **G-CANFAIL:** on POS and on NEG2, both DECOY forms are behind ER-20 by more than a step. This shows the primary
  criterion (not behind ER-20) can fail; RQM's criterion could not.
- **G-FT:** FT is behind ER-20 by more than a step on both streams.
- **G-ID:** with transport forced off, RRM equals STALE bit for bit (20/20).

**Reported beside the gate:** RRM − JOINT, RRM − IGR-F, RRM − RFR, RRM − ANCH-ER, and memory.

**If either part's gate closes,** RRM stops (R12). The reason is recorded in the ledger as row RRM-A, and nothing is
pre-registered.

## 5. Development stage (SEEN carriers only; only if both parts open)

**The carriers:** the 30 SEEN carriers of RQM's DEV_DECLARATION.

**The selection rule.**
- For each form, count the carriers where it is not behind ER-20 by a step.
- The larger count is chosen; a tie goes to RRM-1 (the owner's form).

**D-GATE.**
- **D-COUNT:** the chosen form is not behind ER-20 on at least ⌈0.75 N_dev⌉ carriers.
- **D-REL:** the chosen form is ahead of its STALE by a step on at least one third of the carriers. Otherwise the row
  must say "reduces to anchor replay plus stale feature replay" (R7), and the gate closes: the owner's mechanism would not
  be what passed.

**If it opens:** a pre-registration.
- **Primary row:** the chosen form is not behind ER-20 by a step on at least ⌈0.75 N⌉ unseen carriers; NOT DECIDABLE if
  N < 4.
- **Registered rows:** RRM − STALE (ahead count), RRM − JOINT, RRM against RFR, and no collapse (no seed below half of
  ER-20's mean).
- **Sensitivity:** β ∈ {0.001, 0.1}; anchors M ∈ {10, 40} for RRM-1, or {1, 4} per class for RRM-A. More than one flip
  is FRAGILE.
- **Unseen carriers and data step:** as RQM's DEV_DECLARATION (study 454, then 445, then study 293's unused eligible;
  `default_rng(20261001)`). The data step is not before 2026-10-01 00:00 UTC (R3).

## 6. Literature sweep (one dossier, `docs/citations/rrm_2026-09-30.md`; rule as RQM)

**Positions graded, with the investigator's forecast written now:**

| id | position | forecast |
|---|---|---|
| N1 | correcting stored prototypes or statistics for feature drift by measuring how reference points move is published | REDUNDANT |
| N2 | estimating that drift from kept old-class exemplars or anchors, rather than from current-task data, is published | PARTLY REDUNDANT |
| N3 | representations relative to a set of anchors are invariant to angle-preserving changes of the latent space | REDUNDANT |
| N4 | preserving relations between samples (relational distillation) reduces forgetting | REDUNDANT |
| N5 | storing old-class feature distributions in coordinates relative to a few kept anchors, and transporting them with the anchors' current features (RRM) | PARTLY REDUNDANT |
| N6 | developmental or object-relations framings (a first reference object, increasing resolution) used to design continual learners | PARTLY REDUNDANT |

"Not found" is never read as novel.

## 7. Forecasts (written now)

1. Part 1 opens. The mechanism is exact by construction on SHARED and ROT, and it must fail on UNSHARED.
2. **Part 2 is more likely than not to close at G-REL.**
   - The MLP's drift is not linear on a span of 20 anchors.
   - Anchor replay alone already slows drift.
   - So transport may add less than a step.
3. If Part 2 opens, the development stage is uncertain. A PASS would be recorded as "an anchor-based drift-transport
   method suggested by the object-relations reading of CRR; not a CRR rule" (R8).
