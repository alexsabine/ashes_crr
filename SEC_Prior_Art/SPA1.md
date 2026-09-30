# SPA1: is SEC4's method already known? (the result)

**The request.** Prompt-log entry 254. The declaration (`DECLARATION.md`, 512ad74) was pushed before any search.
- **Three families:** the Fisher's scale in continual learning; curvature calibration; tuning-free and stable
  regularisation.
- **The sweep:** 110 claims from 53 sources. `checks/verify.txt`: 249 of 249 quotes verbatim.
- **The grades** (`checks/grade.txt`) are pinned and CI-checked.

## The verdict (the declared rule, computed): **KNOWN**

The rule gives KNOWN because S3 is REDUNDANT (Synaptic Intelligence) and S4 is REDUNDANT (tuning-free weights are
published). Part by part:

| SEC4's part | position | grade | the nearest sources |
|---|---|---|---|
| a penalty with curvature fitted along the optimisation path | S3 | **REDUNDANT** | Synaptic Intelligence (Zenke, Poole & Ganguli, arXiv 1703.04200 v3): a per-parameter path-fitted importance, loss drop over squared motion, "carries the same units as the loss L". It **replaces** the Fisher rather than calibrating it, and its strength was tuned in practice |
| **rescaling the Fisher by the observed-over-claimed curvature ratio** (SEC's calibration itself) | S2 | **PARTLY REDUNDANT** (no source states it) | RWalk (arXiv 1801.10112 v3) takes the same observed-over-predicted ratio along the path, but **adds** it and normalises to [0, 1], discarding the scale. Self-scaled quasi-Newton methods apply the secant ratio to an optimiser's matrix, not a Fisher. Layers Matter (arXiv 2608.15901 v1) and CSQN (arXiv 2503.19939 v1) are close |
| the stability clip at the step-size edge | S5 | **REDUNDANT** | AR1 (Maltoni & Lomonaco, arXiv 1806.08568 v3): if η·λ·F > 1 the correction overshoots, so F is clipped at maxF and λ ≤ 1/(η·maxF). Kutalev & Lapina (arXiv 2109.10021 v3) derive the same edge and soft-bound the importance |
| a tuning-free, principled weight in continual learning | S4 | **REDUNDANT** | VCL ("does not have free parameters that need to be tuned on a validation set"); Laplace Redux (the evidence framework "alleviating the need for a validation set"); Zhao et al., ICML 2024 (the optimal penalty derived in continual linear regression) |
| the Fisher's scale makes λ need tuning | S1 | MIXED | stated by Ritter et al., van de Ven, and Progress & Compress; contradicted in a pre-trained LoRA setting by EWC-LoRA (one λ = 10^7 across its datasets) |
| a tuning-free Laplace weight matches a tuned λ across many datasets | S6 | PARTLY REDUNDANT | no source states it. Close: MAS ("no tuning of λ was performed") and VCL. Several report the raw weight behind a tuned λ (Ritter; GVCL) |

**Forecasts:** 2 of 6 hit. The forecast PARTLY KNOWN is wrong. S3 and S5 were forecast PARTLY REDUNDANT and are
REDUNDANT; S6 was forecast NOT FOUND and is PARTLY REDUNDANT; S1 is MIXED.

## What this means for the record

- **SEC4's stability clip is AR1's clip (2019),** with κ = 0.5 in place of 1. It is not new.
- **A path-fitted curvature as the continual-learning penalty is Synaptic Intelligence's idea (2017).**
- **Tuning-free principled weights are published.**
- **What no source states** is SEC's specific step: one secant scalar per task that fixes the **units** of the Fisher
  while keeping its **shape**, used with the Laplace weight w = 1/2. The nearest (RWalk) takes the same ratio and then
  discards its scale. A one-day keyword sweep cannot show that it is new.
- **SEC4-1's PASS-1 stands as scored.** Its test is unchanged. But the method it passed is a **combination of known
  parts, with one unpublished-in-this-sweep step**: SI-style path curvature, used to calibrate an EWC/Laplace Fisher, at
  the textbook weight, with AR1's clip. SEC5 did not replicate it (SEC5-1 FAIL), so there is no PASS-2.
- **Any external description of SEC** must name these sources: SI, RWalk, AR1, Kutalev & Lapina, VCL and Laplace Redux.
  It must not present the clip or tuning-free weighting as new (R8, R10).

## Not reached (from the dossiers)

- OpenReview PDFs (HTTP 403 challenges). Among them: "Full Elastic Weight Consolidation via the Surrogate Hessian-Vector
  Product" (a withdrawn ICLR 2024 submission), the most likely unread S2/S3 source.
- NL2SOL (the ACM Digital Library returned 403).
- The textbook self-scaling sources (Oren & Luenberger 1974; Nocedal & Wright 2006).
- Conference title lists and code links.

## Follow-up (2026-09-30, prompt-log entry 256)

`COMPARISON.md` sets SEC's held-out **results** against what the sources report. The verdict KNOWN is about the method's
parts. The finding that the calibrated weight is not behind a tuned λ across many held-out carriers is not stated by any
source found:
- pooled 23/30 against the raw weight's 14/30 (`checks/compare.txt`);
- the published sources report the raw weight failing.

The finding did not replicate in SEC5.
