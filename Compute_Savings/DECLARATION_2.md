# Declaration 2: if the method held on large AI systems, how much energy would it save?

**Status.**
- **The request.** Owner request: prompt-log entry 198.
- **What it is.** A scale model built on the pinned `checks/compute_savings.txt` and on published figures. It opens no data
  and runs no training. It is not a ledger study, and it is a note, not evidence (R8).
- **When it was pushed.** Written and pushed before `checks/scale_estimate.py` exists. The model, the factors and every
  assumed band are fixed here. The script prints the figures and computes each band from them (R15).
- **Sources.** Fetched on 2026-09-25 and quoted in `docs/citations/compute_scale_2026-09-25.md` (R10). The IEA's own pages
  refused the session proxy (HTTP 403), so the IEA figures are quoted from two articles that report them. That is stated
  beside each figure.

## What "the method" means here

There are three candidates in the record. The model treats them separately, because they touch different compute.

1. **SEC, a tuning-free penalty weight.** SCL3-3 is PASS-0: provisional, one study, fragile. It replaces a sweep over one
   weight with a single run. It saves **tuning** compute. It does not make any training run or any inference cheaper.
2. **The empty cut, a lossless pause.** It saves rework only when a run is stopped at a moment of the operator's choosing
   and the checkpoint would otherwise have been incomplete.
3. **The CRR safe continual learner (CRR-SCL, SOTA1).** It has not been run on real data; SOTA1's data step is on
   2026-09-26. Per run it costs more than plain replay. A continual learner could save energy only if it replaced
   retraining. Nothing in the record shows that.

## The model for SEC (the only term with a pinned saving)

**E_saved = E_AI × f_dev × f_sweep × s**

| factor | meaning | value or band | source |
|---|---|---|---|
| E_AI | electricity of servers for AI, per year | 2024: 0.15 × 415 TWh. 2030: the 2024 figure grown at 30 % a year for six years (derived; the IEA base case) | IEA *Energy and AI* (2025), as reported |
| f_dev | the share of AI electricity spent developing models (experiments + training), not serving them | low 0.30 (Meta, power capacity 10:20:70). Middle 0.40 (Google 2019–2021, training ⅖ of ML energy, research included). High 0.7143 (OpenAI 2024, R&D 5 of 7 of compute spend; one frontier lab, spend not energy) | Wu et al. 2022 v2; Patterson et al. 2022 v1; Epoch AI (already in `alexander_plan_2026-09-23.md`) |
| f_sweep | the share of development compute spent sweeping penalty, anchor, replay or KL weights of the kind SEC sets | **ASSUMED** low 0.001, high 0.02 (the band of `Alexander Plan/model/cl_patent.py`). One sensitivity row, 0.05, is labelled "beyond the record": it assumes the calibration generalised to every penalty-like weight | assumption. Context: μTransfer puts **all** hyperparameter tuning at 7 % of pretraining cost |
| s | the share of such a sweep saved | 1 − 3/17 = 0.8235 (a lab keeps 3 confirming configurations) to 0.9412 (SEC accepted as it stands; pinned SCL3) | `checks/compute_savings.txt`, `cl_patent.txt` |

**Printed for 2024 and 2030, at low, middle and high.**
- The low case multiplies the low ends of every factor, and the high case the high ends.
- The middle case uses the middle f_dev, the geometric mean of the f_sweep band, and the mean of s.
- The result is given in TWh, as a share of all data-centre electricity, and in US homes. A US home uses 10,791 kWh a year
  (EIA, 2022). That is a unit for the public, not a claim.
- **Conditional, not a forecast.** Every figure assumes the method holds. The unconditional expectation needs a probability
  that it holds and is adopted. That probability is `cl_patent.txt`'s 0.0150, printed once as a product, labelled as that
  model's assumption.

## The other two terms (bounds, not estimates)

- **The empty cut.** Llama 3 405B had 466 interruptions in 54 days. 47 were planned and 419 unexpected, with more than 90 %
  effective training time.
  - A cut can be taken only before a planned stop. Before an unexpected failure, no cut can be taken.
  - The printed ceiling is the lost time (at most 1 − 0.90) × the planned share (47/466). It assumes that each interruption
    loses equal time, which is a named assumption.
  - Standard practice (a checkpoint written before planned maintenance) already recovers most of this. So **no saving
    beyond good practice is claimed.** The empty cut's contribution is that nothing is silently lost: RNG streams, optimiser
    state, the slow model and the own clock. That affects correctness, not kWh.
- **The CRR learner.** Its cost per run relative to ER, DER++ and X-DER comes from `prereg/sota1/budget.txt`'s measured
  seconds per unit. A cost ratio above 1 is an energy **cost** per run.
- **The ceiling for any training-side method** is E_AI × f_dev: everything spent on development. It is printed as a
  ceiling, not an estimate. Nothing in the record reaches it.
- **What no method here touches** is E_AI × (1 − f_dev): inference, or serving the models. The IEA describes the growth to
  2030 as predominantly inference.

## What would change the answer

- **A measured f_sweep** from a real lab would replace the assumption, which dominates the band.
- **A PASS-2 for SEC.**
- **A PASS on an AdamW-trained large model.** Adam_SGD found the rule's scale advantage to be an SGD property.
- **Evidence that a continual learner can replace retraining.**
