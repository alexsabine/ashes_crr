# Study EQ4 — the bounded rule EQ-B on six unseen PMLB streams: it fails on 2/6 clean, the clip does the work under poison, and the ER-sum control is violated

**EQ4-1 FAILS.** The bounded rule EQ-B at Ω = 1 is not behind the tuned EWC λ on 4 of 6 carriers. It is behind on
`segmentation` by 2.2727 (step 1.8625) and on `yeast` by 6.7857 (step 6.0415). The registered rule (EQ4-1r, EQ3-1's
criterion on fresh carriers) fails on the same two.

**Under poison, the clip is what helps, not the rule.** EQ4-3 FAILS: EQ-B is behind a fixed weight carrying the same clip
on `wine_quality_white` by 10.5520, against a step of 7.0062. Across carriers, adding the clip to the fixed weight moves it
by −16.2162 to +0.7857. EQ4-4 reads INERT: the rule without the clip trails EQ-B by a step on only 2 of 6 carriers.

**The controls.** The ER-sum control (EQ4-5) is violated on `sleep` and `satimage`. The sensitivity table flips in 16 of
96 cells, so the result is FRAGILE. The lr × batch array (EQ4-I) passes 5/5, on `satimage` alone.

**Where the numbers come from.** Every number is printed in:
- `runs/eq4/score.txt` (the frozen scorer; the reruns are byte-identical, `runs/eq4/rerun_*`);
- `runs/eq4/score_without_satimage.txt`;
- `runs/eq4/exclusions.txt`;
- `prereg/eq4/gate_EQB.txt` and `prereg/eq4/gate_EQBM.txt`.

**Anchoring and carriers.**
- Prereg hash `e634280e`; prereg commit a55be4d, 2026-09-22T05:39:00Z. OpenTimestamps was unreachable and the tag push
  was refused; both attempts are recorded in `runs/eq4/`.
- The data was fetched on 2026-09-23 from 04:45:13Z, a calendar day after the hash (R3). The study is **weakly
  anchored**, and every row carries `anchor: push-timestamp only`.
- Carriers (PMLB), all absent from `data/SEEN.md` at the hash (`data/manifests/eq4.sha256`):
  - `satimage` (36 features, K = 6);
  - `segmentation` (19, K = 6 of 7);
  - `yeast` (8, K = 6 of 9);
  - `wine_quality_white` (11, K = 4 of 7);
  - `sleep` (13, K = 4 of 5, subsample 105908 → 5000);
  - `page_blocks` (10, K = 4 of 5).
- The instrument is EQ3's (numpy MLP d-256-K, one head, tasks of 2 classes, 3 epochs per task, seeds 0–4), with EQ-B, the
  poisoned regime and the class floor of `prereg/eq4/PREREG.md`.
- The optimiser is plain SGD (lr 0.05, batch 10). This matters for reading the result beside the Adam checks
  (`Continuous_Learning/ADAM_AND_PRIOR_ART.md`).

## The data-side fact to weigh: `satimage`

The 6435 Landsat records of `satimage` were opened on 2026-09-22T16:23:30Z as `294_satellite_image` in study T1x. That was
after the EQ4 hash and before this data step. By R11's definition (absent from SEEN.md before the hash) the carrier is held
out, and it is scored as committed (R6). The frozen scorer was also run on the other five carriers. The verdicts of EQ4-1
to EQ4-6 are the same without `satimage`: EQ4-1 is 3/5, EQ4-3 is 4/5, EQ4-4 is INERT and EQ4-5 is VIOLATED on `sleep`.
EQ4-I, the invariance array, stands on `satimage` alone. AGENT_LOG 82 records this.

## Rows

| row | verdict | what it says |
|---|---|---|
| EQ4-0 | DECIDABLE | the tuned λ spans 100.00× across carriers (3 to 300) |
| EQ4-1 | **FAIL** (4/6) | EQ-B − tuned: −3.1832 / +4.0841 / −2.2727 / −0.4995 / −6.7304 / −6.7857 (page_blocks / satimage / segmentation / sleep / wine_quality_white / yeast); `wine_quality_white` is not behind by 0.0082 (−6.7304 against −6.7386) |
| EQ4-1r | **FAIL** (4/6) | the registered rule: −7.8278 / +4.8248 / −2.2727 / −0.4995 / −6.7304 / −6.7857 |
| EQ4-2 | IDLE | EQ-B equals the rule on four carriers and differs by +4.6446 and −0.7407 on the other two, each inside its step |
| EQ4-3 | **FAIL** (5/6) | poisoned, EQ-B − fixed+clip: −0.3604 / −0.1602 / −0.4040 / −5.0350 / −10.5520 / −0.7143 |
| EQ4-4 | INERT (2/6) | poisoned, rule − EQ-B: −20.2402 / −1.3814 / −31.2626 / −0.5794 / +0.1699 / +1.5714 |
| EQ4-5 | **VIOLATED** | on replay, EQ-B is ahead of the best fixed w by 2.5774 and of its reduction by 3.1568 on `sleep` (step 1.1153), and 1.6617 from its reduction on `satimage` (step 1.6183) |
| EQ4-6 | DOES NOT REDUCE | EQ-B − fixed@median: +6.9870 / +25.7057 / −1.4646 / +3.4366 / −3.0361 / −2.0714 |
| EQ4-7 | report | no published baseline dominates; A-GEM is ahead of EQ-B by a step on page_blocks and satimage, MEGA-I on page_blocks, satimage and segmentation |
| EQ4-S | FRAGILE | 16 flips in 96 cells |
| EQ4-P | report | plateau widths of EQ-B over the nine-point Ω grid: 7, 6, 5, 9, 9, 9 |
| EQ4-B | report | the Laplace weight is not behind the tuned λ on 4/6 |
| EQ4-D | report only | DER++, LwF, SI, MAS with EQ-B, per carrier in the log |
| EQ4-I | PASS (5/5, `satimage` only) | EQ-B not behind the tuned λ in every lr × batch cell |

## What the rows say together

1. **The clean-stream claim did not replicate as 6/6.**
   - EQ3-1 held on 5 of 6 carriers, and its one failure (`fars`) was a sampling defect. EQ4 has a class floor, so no
     carrier is degenerate, and the rule still fails on two of six.
   - On `segmentation` the tuned λ is 300 and the rule gives 70.9596 against 73.2323.
   - On `yeast` the tuned λ is 8.49. Its per-seed values are 37.14, 24.64, 25.36, 18.57 and 25.00, against the rule's
     15.71, 25.71, 22.50, 13.57 and 19.29.
   - On `wine_quality_white` the rule sits at 18.1741 in every sensitivity cell. The tuned λ reaches 24.9045 on the
     strength of two seeds (34.39 and 31.63; the other three are 18.68, 18.68 and 21.13).
   - The tuned λ is the best of 17 grid means, so it carries a selection advantage the rule does not have. The prereg
     defines it this way, and it is scored that way.
2. **The enhancement is the clip, and the rule adds nothing to it.**
   - In the poisoned regime the unclipped fixed weight falls below the same weight with the clip on five carriers
     (−16.2162, −17.8979, −32.3737, −4.5355, −4.2251), and is +0.7857 above it on `yeast`. So the clip is
     load-bearing.
   - EQ-B and the clipped fixed weight are within a step on five carriers. On the sixth, `wine_quality_white`, the fixed
     weight with the clip is 10.5520 ahead.
   - This is the outcome the prereg names as "the fixed weight with the same clip is enough, and the rule adds nothing
     under poison." The clip is prior art: adaptive clipping from a history of gradient norms (AutoClip, 2020;
     `docs/citations/continual_learning_2026-09-23.md`).
3. **The reduction premise fails again.** EQ4-5 is violated, as EQ3-3 was, so the mechanism statement "the rule is ER-sum
   in other units" is falsified on replay. At the same time, EQ4-6 shows EQ-B is not a constant. It is a
   normalised-gradient method whose outcomes range from a clear loss to a clear gain, carrier by carrier.
4. **Under plain SGD, where the synthetic mechanism says the rule has its only advantage, the real-data record is now:**
   - EQ2-1b PASS (fragile);
   - EQ3-1 5/6;
   - EQ4-1 4/6;
   - both controls violated in EQ3 and EQ4.

   No row has reached PASS-1.

## Sensitivity table (EQ-B Ω = 1 − tuned λ; `runs/eq4/score.txt`)

| carrier | cap 10: sm 0.8 / 0.9 / 0.98 | cap 100: sm 0.8 / 0.9 / 0.98 | cap 1e4: sm 0.8 / 0.98 | κ 1.5: N 20 / 50 / 200 | κ 2: N 20 / 200 | κ 4: N 20 / 50 / 200 |
|---|---|---|---|---|---|---|
| page_blocks | −10.93 / −10.81 / −10.81 | +4.16 / −0.48 / +0.62 | −1.22 / −11.43 | −2.80 / −3.06 / −7.31 | −3.18 / −7.55 | −8.19 / −7.83 / −7.83 |
| satimage | −0.54 / −0.54 / −0.54 | −0.76 / −0.76 / −0.78 | +3.60 / +2.62 | +2.66 / +3.26 / +5.11 | +3.26 / +4.78 | +3.38 / +5.11 / +4.82 |
| segmentation | −1.72 / −1.72 / −1.72 | −0.35 / −0.40 / −0.30 | −0.91 / +0.51 | −1.92 / −2.12 / −2.27 | −1.97 / −2.27 | −2.27 / −2.27 / −2.27 |
| sleep | −0.46 / −0.46 / −0.46 | −0.56 / −0.30 / −0.34 | −0.54 / −0.44 | −0.44 / −0.44 / −0.50 | −0.48 / −0.50 | −0.50 / −0.50 / −0.50 |
| wine_quality_white | −6.73 / −6.73 / −6.71 | −6.73 / −6.73 / −6.69 | −6.71 / −6.65 | −6.71 / −6.73 / −6.73 | −6.71 / −6.73 | −6.73 / −6.73 / −6.73 |
| yeast | −3.14 / −3.29 / −2.93 | −5.07 / −8.86 / −3.21 | −6.07 / +1.71 | −6.14 / −6.43 / −6.79 | −6.14 / −6.79 | −6.79 / −6.79 / −6.79 |

The main cell (cap 1e4, smooth 0.9, κ 2, N 50) is in the rows above. The scorer counts 16 flips of "not behind" in the 96
cells.

## Exclusions and quality gates (`runs/eq4/exclusions.txt`)

- **The class rule.** No carrier was excluded by the class-selection rule (K ≥ 4 after the floor of 40 rows on all six).
  `yeast` keeps one class under 50 rows (44).
- **No NaN rows.**
- **Non-finite runs.** There were 4050 runs, and 664 of them ended with non-finite parameters. They were kept and scored 0,
  as pre-registered. All 664 are fixed-weight, fixed+clip or reduction arms. No rule or EQ-B arm ended non-finite.
- **The exclusions command.** The pre-registered command ran the frozen copy, which resolves the repository root one level
  too high and read nothing. The hashed, byte-identical study copy was run instead (AGENT_LOG 82).

## What a surrogate would have done

`prereg/eq4/gate_EQB.txt` and `gate_EQBM.txt` both read GATE OPEN. On the softmax surrogate S-Y, EQ-B passed the 16×
Fisher-scale mismatch and the poisoned stream, and it was ahead of the registered rule only on the poisoned one. The real
carriers repeat the second half on two of six and not the first half on two of six.

The gate had no row in which a clipped fixed weight competes with EQ-B under poison, which is the comparison EQ4-3 made
and EQ-B lost. A future gate for any clip-based enhancement needs that row.

The synthetic checks run today (`Continuous_Learning/checks/adam_checks*.txt`) go further. The rule's SGD advantage there
comes from the scales at which a fixed weight crosses its stability edge. Without the rule's smoothing, the rule is the
VQGAN-style gradient ratio.
