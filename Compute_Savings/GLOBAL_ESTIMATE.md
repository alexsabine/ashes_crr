# A year's global saving from a tuning-free forgetting weight: compute, energy and CO₂

**Status.**
- **The request.** Prompt-log entry 228 (2026-09-28).
- **How it was built.**
  - The model, the protocols, the bands and the investigator's expectations were fixed in `DECLARATION_3.md` (638620b)
    before any source was fetched and before the script existed.
  - The sources were fetched on the day and quoted verbatim in `docs/citations/global_estimate_2026-09-28.md`.
  - Every number below is printed by `checks/global_estimate.py`, output pinned in `checks/global_estimate.txt`, CI-checked.
- **What it is.** A note, not evidence (R8). It is not quotable outside the ledger. No PASS-2 exists for SEC.
- **Updating.** The script will be re-run and re-pinned when SEC4 (the clipped SEC on a third unseen family) is scored on
  or after 2026-09-29. Until then it uses unguarded SEC's record.

## The short answer (2026, the middle case; if the method held)

| | saved in one year |
|---|---|
| compute | 150,134,981 H100-hours (about 2.17e+26 FLOP) |
| energy | 0.1418 TWh at the servers, 0.1838 TWh at the meter: 0.000337 of all data-centre electricity |
| CO₂ | 84.16 kt, 4.68e-04 of data-centres' 180 Mt |
| in everyday units | the electricity of 17,029 US homes; the CO₂ of 18,296 cars |

**The range, 2026.**
- Energy: 0.0366 TWh (low) to 1.2346 TWh (high) at the meter.
- Compute: 18,656,153 to 1,618,135,692 H100-hours.
- CO₂: 15.89 kt to 676.58 kt.

**2030 (a projection).**
- Middle: 0.5248 TWh, 428,800,520 H100-hours, 240.38 kt.
- High: 3.5262 TWh, 4,621,557,349 H100-hours, 1932.38 kt.

**Weighted by the chance of holding and being adopted** (`cl_patent`'s assumed 0.0150): 2026 middle is 2,252,025
H100-hours, 0.002128 TWh and 1.2625 kt CO₂.

## How it is calculated

**Energy saved** = E_AI × f_dev × f_sweep × s.
- **E_AI**, the electricity of AI (accelerated) servers: 105.20 TWh in 2026, derived from the IEA's 2024 figure grown at
  its 30 % a year.
- **f_dev**, the share spent developing rather than serving models: 0.30 / 0.40 / 0.7143.
- **f_sweep**, the share of development spent sweeping penalty-like weights: **assumed**, 0.001 / 0.00447 / 0.02. No lab
  publishes it, and it dominates the range.
- **s**, the share of each sweep saved. It is not assumed: it is read from the pinned SEC studies (below).

**Compute and CO₂ from energy.**
- The IEA's AI figure is server electricity. Saved server energy ÷ power per H100 (0.7 kW board to 1.275 kW, a DGX H100's
  10.2 kW over 8 GPUs) gives H100-hours.
- × the dense BF16 peak (989.4 TFLOPS) × Llama 3's measured utilisation (38–43 %) gives FLOP.
- × PUE (Google's fleet 1.09 to the industry's 1.54) gives electricity at the meter.
- × carbon intensity gives CO₂. Three values:
  - 433.735 g/kWh: the IEA's data-centre emissions over data-centre electricity, 2024;
  - 458 g/kWh: the global grid average in 2025 (Ember);
  - 548 g/kWh: US data centres, measured (Guidi et al.).

## What the saving per sweep is, and against what

**From 16 unseen carriers** (SCL3 and SEC3; unguarded SEC):
- A seed diverged on 3 of 16 (cnae-9, dionis, fabert), so p_div = 0.1875.
- The realistic protocol (**P-FALLBACK**: run SEC, and run the full sweep where a seed diverges) costs 4.1875 of 17
  configurations: s = 0.7537, with no carrier left behind the tuned λ.
- Accepting SEC as it stands (P-FULL) saves s = 0.9412 but leaves 3 of 16 carriers behind.

**The fair comparison is not only the full sweep.**
- **Against a 3-point mini-sweep**, SEC under P-FALLBACK saves nothing (−0.0699 of a sweep: the mini-sweep is cheaper).
- **Against reusing a λ from other datasets**, SEC saves no compute at all (both are one configuration). Its gain there is
  accuracy on the streams where the reused λ fails.

So the headline figures are the saving **against the full 17-point sweep**, the conventional practice in the record. A
lab that already uses a small sweep or a reused default saves little or nothing in compute by switching.

## What it depends on

1. **That the result transfers.** It was measured on small numpy networks trained by SGD. Nothing in the record tests an
   AdamW-trained large model, where most compute goes. Adam_SGD found the rule's scale advantage to be an SGD property.
2. **f_sweep**, which is assumed. If SEC applies only to EWC-style continual learning (f_sweep 0.0001, the investigator's
   best guess at today's real use), the 2026 middle figure is 44.72 times smaller: 3,357,120 H100-hours, 0.00317 TWh,
   1.882 kt CO₂.
3. **SEC4.** If the clipped SEC removes the divergence on a third unseen family, P-FALLBACK's fallback cost falls toward
   P-FULL's (s up to 0.9412). If it fails, the unguarded figures stand.

## The expectations, checked (section [6] of the printout)

- **Five of six held:**
  - energy and CO₂ of the order declared;
  - the share of data-centre electricity under 0.001;
  - no saving against a 3-point sweep;
  - the EWC-only ratio near 45.
- **One was missed:** the compute expectation. The investigator expected 10⁷–10⁸ H100-hours in the high 2030 case, and the
  printout is 4.622e+09.
  - **The arithmetic was checked:** one TWh is 1.429e+09 H100-hours at 0.7 kW. The expectation was mis-scaled.
  - The miss is recorded (AGENT_LOG 170), not edited away.

## Sources

`docs/citations/global_estimate_2026-09-28.md`: Ember Global Electricity Review 2026; IEA *Energy and AI* (2025) and *Key
Questions on Energy and AI* (2026); Guidi et al. arXiv 2411.09786 v1; the NVIDIA H100 page, the architecture whitepaper
and the DGX H100 user guide; the Uptime Institute 2025 survey; Google's efficiency page; the Llama 3 paper
(arXiv 2407.21783 v3); US EPA.

The IEA revised its 2030 data-centre figure from ~945 to ~950 TWh in April 2026. The model keeps Declaration 2's factors
unchanged, as declared.
