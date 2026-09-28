# Declaration 3: a year's global compute, energy and CO₂ saving from a tuning-free forgetting weight

**Status.**
- **The request.** Owner request, prompt-log entry 228: "make a calculation regarding how much compute would be saved over
  the course of a year globally. Calculate estimated compute saving, energy saving and co2 emission saving."
- **What it is.** An extension of Declaration 2's scale model (`checks/scale_estimate.py`) to three outputs (compute, energy,
  CO₂) for one calendar year, with the saving per sweep now read from **every** pinned SEC study (SCL3, SEC3, and SEC4 once
  scored), not only SCL3. It opens no data and runs no training. It is not a ledger study and it is a note, not evidence (R8).
- **When it was pushed.** Written and pushed before `checks/global_estimate.py` exists and before any source for the new
  factors is fetched. The model, the protocols, the bands and the investigator's expectation are fixed here. The script
  computes every figure from them (R15). Sources are fetched on the day into `docs/citations/global_estimate_2026-09-28.md`
  (R10); a figure the fetch cannot confirm is printed as "unconfirmed" and its row carries the fallback named below.

## The year

- **Main answer: calendar year 2026**, the current year. E_AI(2026) = E_AI(2024) × (1 + g)², with g the IEA's growth rate
  of AI-server electricity (Declaration 2's derivation, two years instead of six).
- **Projection: 2030**, as in Declaration 2. A projection, not a forecast.

## The three outputs

For one year and one scenario:

1. **Energy saved** E = E_AI × f_dev × f_sweep × s (TWh). E_AI, f_dev and f_sweep are Declaration 2's factors, unchanged
   (f_sweep ASSUMED 0.001 to 0.02). One new sensitivity row, **f_sweep = 0.0001**, is labelled "EWC-style continual learning
   only": SEC's weight is an anchor penalty of the online-EWC kind, and that practice is a niche of 2026 development compute.
2. **Compute saved**, in H100-equivalent GPU-hours: GPU-h = E / (P_gpu × PUE), where P_gpu is the all-in server power per
   GPU (kW; a band from the H100's 0.7 kW board power to the DGX H100 system power per GPU) and PUE the facility overhead
   (a band from a hyperscaler fleet figure to the industry average). Also printed in FLOP: GPU-h × 3600 × the H100's dense
   BF16 peak × MFU, with MFU a published band from large-run reports (fallback, if unconfirmed: ASSUMED 0.3 to 0.45). And as
   a share of global AI compute, taken equal to the energy share E / E_AI (named assumption: saved sweep compute is as
   energy-intensive per FLOP as the average AI workload).
3. **CO₂ saved**, Mt: E × I, with I the carbon intensity of the electricity (g CO₂/kWh, location-based). Three values:
   low = data-centre emissions / data-centre electricity (IEA), middle = the global grid average (Ember), high = a measured
   data-centre intensity (US data centres, published). Market-based accounting (certificates) would print lower and is not
   used, because it does not change what is burned.

## The saving per sweep, s, from the pinned studies (not assumed)

**The unit.** One carrier (a task stream) needing a forgetting weight. The conventional practice in the record is SEC1's
two-stage sweep, 17 configurations. Each protocol's expected configurations c per carrier gives s = 1 − c / 17.

| protocol | what a user does | c (expected configurations) |
|---|---|---|
| P-FULL | SEC accepted as it stands | 1 |
| P-FALLBACK | run SEC; if any seed diverges (below half of the best seen accuracy, which a user can see without a sweep, approximated by the tuned accuracy in the record), run the full sweep | 1 + p_div × 17 |
| P-CHECK | run SEC and a 3-point check {1, 30, 1000}; keep the best | 4 |

- **p_div** and the accuracy cost are read per study from the pinned score files: `runs/scl3/score*.txt` or `results_*.jsonl`,
  `runs/sec3/score.txt` and `runs/sec4/score.txt` once it exists (before that the SEC4 line prints "pending").
  - **Unguarded SEC:** pooled SCL3 + SEC3 carriers (the carriers where a seed diverged, over the carriers scored).
  - **Clipped SEC:** SEC4's unseen carriers only. The development result on SEEN carriers is printed beside it and labelled
    "development, not evidence"; it never enters s.
- **The accuracy cost** (not compute): the share of carriers where the method is behind the tuned λ by a step, printed per
  protocol. A compute saving that costs accuracy on a quarter of streams is printed with that quarter beside it.

**What the saving is against (fairness).** The record shows two cheaper alternatives to the full sweep:
- a 3-point mini-sweep (3 configurations; SEC3-P: SEC matched it on 5 of 6);
- a λ reused from other carriers (1 configuration; SEC3-T: it was not behind on 3 of 6).

So three savings are printed: against the full sweep (s above), against a 3-point sweep (s₃ = (3 − c) / 17 of the full
sweep's compute, zero or negative when c ≥ 3), and against a reused λ (zero compute saving at c = 1: both are one
configuration; SEC's gain there is accuracy on the carriers where the reused λ fails). **The headline is the saving against
the full sweep, and the other two are printed on the same line.**

## Scenarios

- **low / middle / high** as in Declaration 2 (low ends, geometric-mean middle, high ends), crossed with the three
  protocols, for 2026 and 2030.
- **The CO₂ and compute bands** are matched to the scenario (low energy with low intensity, and so on), and the full cross
  of the extremes is printed once as the outer bound.
- **Unconditional**: × cl_patent's P(adopted) = 0.0150, printed once, labelled as that model's assumption.
- **Everyday units**: US homes (EIA 10,791 kWh a year; Declaration 2) and, for CO₂, cars (a published tonnes-per-car-year
  figure, if the fetch confirms one; otherwise not printed).

## What is conditional, and on what

Every figure assumes:
1. the result on small numpy MLPs trained by SGD transfers to the models that use most compute (Adam_SGD found the rule's
   scale advantage to be an SGD property; nothing in the record tests an AdamW-trained large model);
2. f_sweep, which is assumed and dominates the band;
3. the pinned p_div, from 16 unguarded carriers and SEC4's carriers: small samples.

No PASS-2 exists for SEC. The printout says so in its header. The figures are not quotable outside the ledger (R8).

## The investigator's expectation (written before the sources and the script)

- **Energy, 2026, middle, P-FALLBACK:** of the order of 0.1 TWh or less, under 0.1 % of data-centre electricity.
- **CO₂, 2026, middle:** of the order of 0.05 Mt or less, against data-centre emissions of the order of 10² Mt.
- **Compute:** of the order of 10⁷–10⁸ H100-hours in the high 2030 case; far less in the middle 2026 case.
- **Against a 3-point sweep**, the saving attributable to SEC is small (at most 2/17 of the sweep) and near zero under
  P-FALLBACK if p_div is as large as in SEC3.
- **The EWC-only row (f_sweep 0.0001)**, the investigator's best guess at today's real use, is about 45 times below the
  middle row.

If the printed figures fall outside these orders, the script is checked before the text is written (R15).

## Sources to fetch on the day

1. Global average grid carbon intensity, latest year (Ember, Global Electricity Review).
2. Data-centre electricity and emissions (IEA, *Energy and AI*), and the 2024 and 2030 electricity figures, re-checked.
3. A measured data-centre carbon intensity (a published US data-centre figure).
4. NVIDIA H100 SXM board power and dense BF16 peak; DGX H100 system power.
5. PUE: an industry-average survey (Uptime Institute) and one hyperscaler fleet figure.
6. MFU of a published large training run.
7. Tonnes of CO₂ per passenger car per year (a public-agency figure).
