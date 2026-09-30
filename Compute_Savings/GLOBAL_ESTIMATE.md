# A year's global saving from a tuning-free forgetting weight: compute, energy and CO₂

**Status.**
- **The request.** Prompt-log entry 228 (2026-09-28).
- **How it was built.**
  - The model, the protocols, the bands and the investigator's expectations were fixed in `DECLARATION_3.md` (638620b)
    before any source was fetched and before the script existed.
  - The sources were fetched on the day and quoted verbatim in `docs/citations/global_estimate_2026-09-28.md`.
  - Every number below is printed by `checks/global_estimate.py`, output pinned in `checks/global_estimate.txt`, CI-checked.
- **What it is.** A note, not evidence (R8). It is not quotable outside the ledger. No PASS-2 exists for SEC.
- **Updating.**
  - **Re-pinned 2026-09-29** on SEC4's evidence: the clipped SEC on a third unseen family, ledger SEC4-1 PASS-1.
  - The first version (2026-09-28) used unguarded SEC's record: p_div 3/16, P-FALLBACK s = 0.7537. Its figures are kept in
    git history (commit b427e2e), and the unguarded lines are still printed in section [1].

## The short answer (2026, the middle case; if the method held)

| | saved in one year |
|---|---|
| compute | 187,485,635 H100-hours (about 2.70e+26 FLOP) |
| energy | 0.1771 TWh at the servers, 0.2295 TWh at the meter: 0.000420 of all data-centre electricity |
| CO₂ | 105.10 kt, 5.84e-04 of data-centres' 180 Mt |
| in everyday units | the electricity of 21,266 US homes; the CO₂ of 22,848 cars |

**The range, 2026.**
- Energy: 0.0457 TWh (low) to 1.5418 TWh (high) at the meter.
- Compute: 23,297,439 to 2,020,696,279 H100-hours.
- CO₂: 19.84 kt to 844.90 kt.

**2030 (a projection).**
- Middle: 0.6554 TWh, 535,477,723 H100-hours, 300.18 kt.
- High: 4.4035 TWh, 5,771,310,641 H100-hours, 2413.12 kt.

**Weighted by the chance of holding and being adopted** (`cl_patent`'s assumed 0.0150): 2026 middle is 2,812,285
H100-hours, 0.002657 TWh and 1.5765 kt CO₂.

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

**The realistic protocol (P-FALLBACK):** run SEC, and run the full sweep only where a seed diverges.

**The clipped SEC, SEC4 (6 unseen carriers of a third family; used for the figures above):**
- No seed diverged (p_div = 0.0000).
- P-FALLBACK therefore costs 1 of 17 configurations: s = 0.9412, with 0 of 6 carriers behind the tuned λ.

**Unguarded SEC, SCL3 + SEC3 (16 unseen carriers; the first version):**
- A seed diverged on 3 of 16 (cnae-9, dionis, fabert), so p_div = 0.1875.
- P-FALLBACK costs 4.1875 configurations: s = 0.7537.

**The fair comparison is not only the full sweep.**
- **Against a 3-point mini-sweep:**
  - the clipped SEC under P-FALLBACK saves 0.1176 of a full sweep (2 configurations of 17);
  - unguarded SEC saved nothing (−0.0699).
- **Against reusing a λ from other datasets**, SEC saves no compute at all (both are one configuration). Its gain there is
  accuracy on the streams where the reused λ fails.

So the headline figures are the saving **against the full 17-point sweep**, the conventional practice in the record. A
lab that already uses a small sweep or a reused default saves little or nothing in compute by switching.

## What it depends on

1. **That the result transfers.** It was measured on small numpy networks trained by SGD. Nothing in the record tests an
   AdamW-trained large model, where most compute goes. Adam_SGD found the rule's scale advantage to be an SGD property.
2. **f_sweep**, which is assumed. If SEC applies only to EWC-style continual learning (f_sweep 0.0001, the investigator's
   best guess at today's real use), the 2026 middle figure is 44.72 times smaller: 4,192,306 H100-hours, 0.00396 TWh,
   2.350 kt CO₂.
3. **The clipped SEC's record is one family.**
   - SEC4-1 is PASS-1 on 6 carriers, after 3 exclusions. PASS-2 needs a replication on a fourth unseen family.
   - If divergence reappears there, s falls back toward the unguarded 0.7537.

## The expectations, checked (section [6] of the printout)

- **Five of six held:**
  - energy and CO₂ of the order declared;
  - the share of data-centre electricity under 0.001;
  - a saving against a 3-point sweep of at most 2/17;
  - the EWC-only ratio near 45.
- **One was missed:** the compute expectation. The investigator expected 10⁷–10⁸ H100-hours in the high 2030 case, and the
  printout is 5.771e+09.
  - **The arithmetic was checked:** one TWh is 1.429e+09 H100-hours at 0.7 kW. The expectation was mis-scaled.
  - The miss is recorded (AGENT_LOG 170), not edited away.

## Sources

`docs/citations/global_estimate_2026-09-28.md`: Ember Global Electricity Review 2026; IEA *Energy and AI* (2025) and *Key
Questions on Energy and AI* (2026); Guidi et al. arXiv 2411.09786 v1; the NVIDIA H100 page, the architecture whitepaper
and the DGX H100 user guide; the Uptime Institute 2025 survey; Google's efficiency page; the Llama 3 paper
(arXiv 2407.21783 v3); US EPA.

The IEA revised its 2030 data-centre figure from ~945 to ~950 TWh in April 2026. The model keeps Declaration 2's factors
unchanged, as declared.

## Addendum 2026-09-30: the premise after SEC5 and SEC4-1-G (figures not re-pinned)

The figures above are unchanged; they quote their own pinned output. Since they were pinned, the ledger shows three
things that weaken the premise they rest on.

1. **SEC4-1 did not replicate.** SEC5-1 (the replication on a fourth unseen family) FAILS: the clipped SEC is not behind
   the tuned λ on 4/8, need 6. SEC5-2 FAILS too. SEC4-1 therefore stays a single-family PASS-1, and no PASS-2 exists.
2. **The criterion could not fail on SEC4's carriers.** SEC4-1-G is a post hoc report, not a re-score. It applies SEC6's
   later instrument rule. A learner frozen after task 1 is not behind the tuned λ on 5 of SEC4's 6 carriers (need 5), so
   under that rule SEC4-1 would be printed UNINFORMATIVE.
   - Across the 30 held-out carriers of SCL3, SEC3, SEC4 and SEC5, the frozen learner is not behind on 24/30
     (`SEC_Analysis/checks/m_checks.txt`).
   - The cause is traced in `SEC_Analysis/WHY_SEC4_WORKED.md`: the loader ranks classes by count, and task 1 holds the two
     largest.
3. **A random class order with balanced accuracy does not repair it** (SEC7-A, GATE CLOSED). The frozen learner is behind
   the tuned λ on only 13/30 of the SEEN carriers.

**What this means for this note.** The saving per sweep, s = 0.9412, assumes that one SEC configuration replaces the
17-point sweep without loss. The only evidence for "without loss" is the criterion "not behind the tuned λ". On these
streams that criterion does not separate SEC from a learner that stops learning after task 1. So the record does not
currently support the premise, and the figures above are an arithmetic on an unsupported premise, not an estimate of a
saving.

Following AGENT_LOG 188, the script is not re-pinned. A re-estimate needs its own declaration and a criterion that can
fail. SEC6 (data step 2026-10-01) carries that check as its instrument gate SEC6-G.
