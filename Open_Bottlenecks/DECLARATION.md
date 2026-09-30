# Declaration: OB1, the open bottlenecks of continual learning, and where CRR disagrees with the frontier (pushed before any search)

**The request.** Prompt-log entry 252 (2026-09-30T05:02Z): "I need you to find the actual big bottlenecks so we can put crr
to the proper test on things that are not currently possible".

## Why the process changes

**The previous rounds had the same shape.** In RQM and RRM, the investigator:
1. read the bottlenecks;
2. derived a design from CRR (or from the owner's reading of it);
3. searched for prior art **after** building it.

**The design was published each time.** RQM's reading selected Gaussian Mixture Replay (arXiv 2104.09240). RRM's transport
is HopDC's (arXiv 2602.00144). The CRR readings were RESTATES in every case (RQM `CRR_READING.md`: 6 RESTATES, 4 SILENT;
RRM2 Part W: NOT WORTH PURSUING).

**The process is changed in three ways.**
1. **Open first.** A bottleneck enters only if the sources show it is open: a 2025–26 source says it is unsolved, **and**
   the best reported result on a named benchmark falls short of a stated target.
2. **Disagreement, not restatement.** A CRR reading counts only if it names a **point of disagreement**: an assumption that
   the frontier methods for that bottleneck make and CRR denies, with a prediction that differs because of it. If CRR
   agrees with the frontier's assumption, the reading is RESTATES, however apt the words.
3. **Prior art before code.** Every candidate gets a targeted prior-art search of its **specific mechanism** before any
   code is written. Only a candidate NOT FOUND after that search goes on to a synthetic gate. "Not found" is still never
   "novel". It only licenses a test.

## Stage 1: the bottleneck harvest (four families, 2025–2026 sources first)

**The families** (one dossier each, `docs/citations/ob1_h{1..4}_2026-09-30.md`, every quote verified against its fetched
text by `Open_Bottlenecks/checks/verify.py`):
- **H1:** class-incremental, exemplar-free and online continual learning (surveys, benchmarks, position papers).
- **H2:** continual learning of large models: continual pre-training and fine-tuning of language models, forgetting under
  fine-tuning, and knowledge editing at scale (sequential edits).
- **H3:** loss of plasticity, long-horizon streams, continual reinforcement learning, non-stationary optimisation.
- **H4:** deployment constraints: task-free or boundary-free streams, choosing hyperparameters without future data
  (tuning-free), compute-budgeted continual learning, and on-device learning.

**For each bottleneck, the dossier records:**
- **B-a:** a quote stating the problem;
- **B-b:** a 2025–26 quote stating it is open, unsolved or a main challenge;
- **B-c:** the best result the sources report on a named benchmark, against the target (joint training, an oracle, or a
  stated goal), with the numbers quoted;
- **B-d:** the method families tried, and the assumption each makes about time, boundaries, memory or tuning;
- **B-e:** CPU-testability on this machine (yes or no, and why).

## Stage 2: the CRR reading (the investigator; `Open_Bottlenecks/CRR_READING.md`; before any stage-3 search)

**For each open bottleneck:**
- **the CRR ingredient**, from `theory/CRR.md` only: A1′, A3/D5, A6, P2/P3, H-L5, D6/H-T1, H-EQ, A7/A8, Proposition 7;
- **the frontier's assumption** (from B-d) and whether CRR **agrees**, **denies** or is **silent**;
- if it denies, **the prediction**: what a method built on CRR's side of the disagreement does that the frontier's does not,
  as a direction or an inequality on the B-c benchmark.

**Labels:** DISAGREES (a candidate), RESTATES or SILENT.

**The ranking of candidates:** the size of the B-c gap; CPU-testability; and whether the prediction can fail on a
synthetic stream.

## Stage 3: targeted prior art (agents; before any code)

- **The search.** One search per DISAGREES candidate, for its specific mechanism, on arXiv, CVF and OpenReview where
  reachable, 2023–2026, with verified quotes.
- **The grade:** REDUNDANT (the mechanism is published), PARTLY REDUNDANT, or NOT FOUND IN THE SWEEP.
- **Only NOT FOUND goes on.** A PARTLY REDUNDANT candidate goes on only if the missing part is the part CRR predicts.

## Stage 4: the test (only for survivors; each declared separately before code)

- **The Phase A gate.** A synthetic gate that can close. The frontier method is the baseline, and a must-fail control is
  included, as in DECLARATION_2 of RRM.
- **Then:** development on SEEN carriers; then a pre-registration with a data step on a later day (R3).

## Stop conditions (R12)

- **After stage 2:** if no bottleneck reads DISAGREES, OB1 stops. The finding is recorded: "on the open bottlenecks found,
  CRR has no point of disagreement with the frontier".
- **After stage 3:** if no candidate is NOT FOUND, OB1 stops, and the same is recorded with the prior art named.

## Forecasts (written now)

1. Stage 1 finds at least 8 open bottlenecks with B-a, B-b and B-c all quoted.
2. Stage 2 reads **at most 3** as DISAGREES. The most likely points of disagreement:
   - boundaries supplied from outside the learner, where CRR's cut is the system's own event (A3);
   - hyperparameters indexed by clock time or step count, where CRR indexes by the learner's own change (H-L5, D6);
   - tuning on the full stream, which uses future data (A7).
3. Stage 3 finds **at least one** of those mechanisms published: task-free continual learning with self-detected
   boundaries is an existing literature.
4. The most likely final outcome is **zero or one** candidate surviving to a gate.
