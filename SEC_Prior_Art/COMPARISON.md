# SEC's results against what the published sources report (SPA1 follow-up, prompt-log entry 256)

**Why this note exists.** SPA1 (`SPA1.md`) graded SEC4's **method** KNOWN by its declared rule: the clip, the path-fitted
penalty and tuning-free weighting are each published. The owner asked a different question: do SEC4's **findings** say
something the published results do not? Numbers are from `checks/compare.txt` (read from the pinned ledger rows) and
from the verified claims (`checks/verify.txt`).

## What the published sources report about the tuning-free weight

The claims are listed in full in `checks/compare.txt`.
- **The textbook (natural, λ = 1) weight is reported to fail, or to be far from the tuned value:**
  - Ritter et al. (arXiv 1805.07810 v1): "For the natural choice of λ = 1 … the network's performance decays for the
    first task".
  - NCL (arXiv 2106.08085 v2): "NCL, OWM, and DOWM outperformed KFAC with λ = 1", and KFAC needed λ ∈ [100, 1000].
  - GVCL (arXiv 2011.12328 v1): the derivation gives λ = 1, and the methods "perform best when λ > 1, typically
    10 − 1000".
  - van de Ven (arXiv 2502.11756 v1): EWC's best λ moves by "orders of magnitude" with how the Fisher is computed.
  - EWC-DR (arXiv 2603.18596 v3): the peak is around λ = 10,000–20,000.
- **Where a single λ works across datasets, it is still found by a sweep once.** Examples: EWC-LoRA's λ = 10^7 on a
  pre-trained LoRA model; normalising the Fisher to [0, 1] and tuning one λ (Progress & Compress; Josifovski et al.).
- **Truly tuning-free methods exist, but they are other methods** (VCL; Laplace Redux by marginal likelihood; MAS with
  λ = 1 and no tuned comparison). None reports a Laplace/EWC weight matching a tuned λ across many datasets (S6: not
  stated by any source).
- **Realistic tuning protocols** (Cha & Cho, TMLR 2025; Lee et al. 2025) say in-scenario tuning of λ is unrealistic, and
  that most methods' reported performance does not survive it.

## What SEC's held-out studies found (the ledger rows)

| study | SEC arm | not behind the tuned λ | raw textbook weight (uncalibrated) |
|---|---|---|---|
| SCL3-3 | calibrated, no clip | 9/10 | 4/10 |
| SEC3-3 | calibrated, no clip | 4/6 | 5/6 |
| SEC4-1 | calibrated + clip | 6/6 (PASS-1) | 1/6 |
| SEC5-1 | calibrated + clip | 4/8 (FAIL) | 4/8 |
| pooled (report only) | | **23/30** | **14/30** |

Also from the ledger:
- **The tuned λ's spread across carriers collapsed after calibration:** 18866.67× raw against 500.00× calibrated (SCL3-4).
- **SEC used one configuration of 17** (SEC3-K, SEC4-K).

## The comparison

1. **The raw textbook weight behaves here as the literature says.** It was not behind the tuned λ on only 14 of 30
   held-out carriers (1 of 6 in SEC4). This agrees with Ritter, NCL, GVCL and van de Ven, and is an independent check
   that the harness reproduces the known failure.
2. **The step SPA1 did not find is the one that changes this.** The secant calibration of the Fisher's units raised the
   pooled count to 23 of 30, and in SEC4 from 1 of 6 to 6 of 6. It collapsed the tuned λ's spread from 18866.67× to
   500.00× (SCL3). No published source found reports a tuning-free Laplace/EWC weight doing this across many datasets.
   So **the method's parts are known, but this finding is not in the sources found.** SPA1's "KNOWN" is about the
   parts, not the result.
3. **The finding is not established.**
   - SEC5, the declared replication, failed: 4/8, the same as the raw weight on those carriers. So on the fourth family
     the calibration added nothing.
   - SEC3 also failed (4/6, below the raw weight's 5/6).
   - The pooled 23/30 mixes arms and families. It is a report, not a registered test.
   - Only SEC4 reached PASS-1, and there is no PASS-2.
   - All of it is on one small MLP with tabular carriers and 5 two-class tasks. None of it is on the published
     benchmarks where the λ failures were reported.
4. **The energy estimate follows from the finding, not from the method's parts.** The saving is the sweep avoided (one
   configuration of 17). It exists only where the calibrated weight holds, which is 23 of 30 pooled and not replicated
   in SEC5. `Compute_Savings/GLOBAL_ESTIMATE.md` was built on SEC3 and SCL3. It is conditional on the finding, and SEC5
   weakens that condition.

## The test that would decide it (not run; a proposal)

The published λ failures give a sharp, external target. On the benchmarks and models where Ritter, NCL, GVCL and
van de Ven report the tuned λ (λ = 3; 100–1000; 10–1000; orders of magnitude):
- does SEC's per-task calibration factor land the effective weight on their tuned value?
- and is the calibrated weight not behind their tuned λ?

That is a replication against published numbers, not our own sweep. The benchmarks are MNIST-family and CIFAR, which
are SEEN in this repository, so it would be confirmatory on seen data (rung R5) unless an unseen benchmark with a
published tuned λ is found first.
