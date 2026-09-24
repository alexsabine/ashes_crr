# Data availability check (metadata only), 2026-09-24

Method: `curl -sI` HEAD requests on data URLs; documentation pages, README files, file listings and
API metadata read in full. **No data file was downloaded or opened.** The exceptions, all of them
documentation or code, are listed here: FRED series HTML pages (only the title, units, frequency and notes
were extracted; observation values were not printed), FRED `graph/api/series` JSON (only the
date-range and units keys were grepped), Michigan survey questionnaires and technical PDFs, the SPF
documentation PDF and release-dates text file, the USCRN README/HEADERS and sensor-description PDFs,
the README/`.m`/`.js` code files of wkool/tradeoffs (a blobless, no-checkout clone was used, so the `.mat`
data blobs were never fetched), and the Gillan OSF `readme.rtf`. `data/SEEN.md` has no entry for any of
these four sources: grep for SPF/FRED/CPIAUCSL/MICH/VIX/SP500/USCRN/two-step/Kool/Gillan/Decker/OSF
returned nothing.

---

## 1. Survey of Professional Forecasters (Philadelphia Fed), median CPI inflation forecasts

**Fetch URLs**
- Median levels workbook (contains the `CPI` worksheet):
  `https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/survey-of-professional-forecasters/historical-data/medianLevel.xlsx`
  HEAD: 200, `application/vnd...spreadsheetml.sheet`, content-length 554444, no Last-Modified header.
  The landing page says "509 KB; last update: August 14, 2026".
  (The page link also carries `?sc_lang=en&hash=E52F5DEF4551C3EBD24031A04CE6E98A`. The bare URL also returns 200.)
- Median growth workbook: `.../historical-data/medianGrowth.xlsx`: 200, 144611 bytes. The documentation says it does
  **not** contain CPI, because CPI enters the survey in growth-rate form already. Use medianLevel.xlsx.
- Documentation PDF: `.../survey-of-professional-forecasters/spf-documentation.pdf`: 200, 731389 bytes, 62 pp,
  "last update: August 14, 2026".
- Data sources PDF: `.../spf-data-sources.pdf`: 200, 260426 bytes.
- Deadline/release dates: `.../spf-release-dates.txt`: 200.
- Landing page: https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/median-forecasts
- Trap: guessed names such as `Median_CPI_Level.xlsx` return **HTTP 200 with text/html** (a soft 404). A fetch
  script must check the content-type, not just the status.

**Documented format (spf-documentation.pdf)**
- The workbook has one worksheet per variable. The first two columns are YEAR and QUARTER (the survey date).
  The remaining columns are horizons, named with root + suffix: `CPI1` = the quarter before the survey
  quarter (already known to forecasters), `CPI2` = the current quarter (nowcast), `CPI3`–`CPI6` = the next
  four quarters. `CPIA`, `CPIB`, `CPIC` = Q4/Q4 annual inflation for the current year and the next two
  (`CPIC` since 2005:Q3).
- Definition (verbatim): "CPI — Forecasts for the headline CPI inflation rate. Seasonally adjusted, annual
  rate, percentage points. Quarterly forecasts are annualized quarter-over-quarter percent changes of the
  quarterly average price index level. Annual forecasts are fourth-quarter over fourth-quarter percent
  changes. ... First survey to include this variable: 1981:Q3."
- "the survey's median and mean projections for CPI and PCE inflation are means and medians of a growth
  rate (inflation), not growth rates of the mean and median projection for the level".
- Q/Q growth formula: g = 100[(X_t/X_{t-1})^4 − 1], discrete compounding.
- Missing value code: `#N/A`.
- **Reporting precision: not stated.** A grep of the 62-page documentation for decimal/precision/round/digit finds
  only "sum to 100 (up to a rounding error)" for the density probabilities. The documentation does not give the
  number of decimals panelists report in. A prereg cannot cite a documented resolution for SPF CPI and
  would have to name one as an assumption.
- Survey timing: true deadline dates are known only from 1990:Q2 (spf-release-dates.txt: "True deadline and
  news release dates for surveys prior to 1990:Q2 are not known").
- Licence/terms: public on the Philadelphia Fed website. The documentation carries no explicit licence. Note from the
  landing page: "The historical values of Moody's Aaa and Baa rates are proprietary" (not relevant to CPI).

**Usable:** yes. One xlsx fetch (needs openpyxl), sheet `CPI`, columns `CPI1..CPI6, CPIA..CPIC`.

---

## 2. FRED series (fredgraph.csv) + Michigan survey documentation

**Fetch URL pattern:** `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIES>`
(HEAD returns `content-disposition: attachment; filename="<SERIES>.csv"`, `application/csv`)

| series | HEAD | content-length (HEAD) | Last-Modified | units / freq (series page) | coverage (graph API min_date–max_date) |
|---|---|---|---|---|---|
| CPIAUCSL | 200 | 17744 | Fri, 11 Sep 2026 13:37:49 GMT | Index 1982-1984=100, Seasonally Adjusted, Monthly; source BLS | 1947-01-01 – 2026-08-01 |
| MICH | 200 | 0 (HEAD reports 0; see note) | Fri, 28 Aug 2026 15:03:30 GMT | Percent, Not Seasonally Adjusted, Monthly; source University of Michigan Surveys of Consumers | 1978-01-01 – 2026-07-01 |
| VIXCLS | 200 | 0 (HEAD reports 0) | Wed, 23 Sep 2026 13:37:36 GMT | Index, NSA, Daily, Close; source CBOE | 1990-01-02 – 2026-09-22 |
| SP500 | 200 | 48903 | Thu, 24 Sep 2026 00:01:41 GMT | Index, NSA, Daily, Close; source S&P Dow Jones Indices | 2016-09-26 – 2026-09-23 |

Notes and quirks from the documentation pages (https://fred.stlouisfed.org/series/<SERIES>):
- A content-length of 0 on HEAD for MICH/VIXCLS is a HEAD artefact (the body is generated on GET). It does not
  mean the file is empty. A fetch script should record the sha256 of the GET body, not the HEAD length.
- The graph API default window (`cosd`) for VIXCLS and SP500 is 2021 onwards (cosd=2021-09-22 / 2021-09-23).
  A fetch script should pass explicit `&cosd=YYYY-MM-DD&coed=YYYY-MM-DD` so the downloaded range is pinned and
  does not depend on a server default. Adding `&vintage_date` or recording Last-Modified is also advisable,
  because FRED series are revised (CPIAUCSL SA factors are revised each year).
- MICH notes (verbatim): "Median expected price change next 12 months, Surveys of Consumers. **The most
  recent value is not shown due to an agreement with the source.**" Citation required; "Copyright, 2016,
  Surveys of Consumers, University of Michigan. Reprinted with permission."
- SP500 notes (verbatim): "FRED and its associated services will include 10 years of daily history for
  Standard & Poors and Dow Jones Averages series." It is a price index without dividends. The copyright notice
  says "Reproduction of S&P 500 in any form is prohibited except with the prior written permission of S&P
  Dow Jones Indices LLC". Do not commit the raw SP500 file to the repo; commit only its sha256.
- VIXCLS: "Copyright, 2016, Chicago Board Options Exchange, Inc. Reprinted with permission."
- CPIAUCSL: BLS, public domain (US government).
- Missing values in fredgraph.csv are "." (FRED convention, e.g. market holidays in daily series). This is not
  stated on these pages and should be verified from the header on first fetch, which is itself a data open.

**Michigan survey documentation on the reporting resolution of individual expectations**
(https://data.sca.isr.umich.edu/survey-info.php and technical-docs.php. The main site sca.isr.umich.edu returned 502 today. data.sca.isr.umich.edu works.)
- *Procedure to Estimate Price Expectations* (R. Curtin, Jan 1996), `https://data.sca.isr.umich.edu/fetchdoc.php?docid=75433`:
  "All responses are coded in an open-ended format, with any answers outside of the range -95% to +95%
  truncated to ±95% prior to coding." Also: "The problem with point estimates is magnified by **the survey practice
  to only code integer values**, as well as rounding the imputed point estimates to integer values." Footnote:
  "All range responses (for example, 1% to 3%) are initially probed ... If the respondent could not narrow
  the range, the midpoint is coded (rounded to the nearest odd number if necessary)." The published median is
  obtained by **interpolation between adjacent integer codes**, so MICH itself is not integer-valued, while individual
  responses are whole percent in the phone era.
- Phone questionnaire (`fetchdoc.php?docid=24776`, 233907 bytes; also docid=75441): A12b "By about what percent do
  you expect prices to go (up/down) on the average, during the next 12 months?" `____ PERCENT`. It has a
  cents-on-the-dollar probe for DK, and a confirmation probe if the answer is greater than 5%.
- **Resolution change, April 2024:** the web questionnaire (`fetchdoc.php?docid=75445` / 75440, 2024) Q13a (PX1Q2W) says
  "(Please report a number from 0.1 to 100)", which means **decimals to 0.1 are accepted**. Mode table
  (docid=75436): "Jan 2015 – Jun 2024 Cell (RDD) Computer-assisted telephone interviewing"; "Apr 2024 – Address
  Based Sampling Web interviewing"; "Methodological Improvements Begin with April 2024 Preliminary Release"
  (Apr–Jun 2024 mixed mode). A prereg that uses whole-percent resolution must restrict the Michigan
  data to before 2024-04, or treat the mode transition as a registered break.
- Revision note (docid=80741): "A small number of historical values of PX1Q2 and PX5Q2 from between 202404 and
  202511 have been revised to correctly reflect internal editing, topcoding, and bottomcoding. Note that
  historical aggregate estimates are unaffected".
- Usage (faq.php): "Any data, tables, or charts available to the public on our main website can be used without
  permission ... cite our data as 'University of Michigan, Survey Research Center, Surveys of Consumers.'"

**Usable:** yes for CPIAUCSL, MICH and VIXCLS (VIX from 1990). SP500 via FRED covers only 2016-09-26 onwards (10 years),
with restrictive reproduction terms.

---

## 3. NOAA USCRN daily01

**Directory:** https://www.ncei.noaa.gov/pub/data/uscrn/products/daily01/
- Year folders 2000 … 2026, plus `snapshots/`, `updates/`, `.archive`, `.awips`, and README.txt / readme.txt /
  HEADERS.txt / headers.txt.
- Per-station yearly file: `.../daily01/<YYYY>/CRND0103-<YYYY>-<ST_Name_dist_dir>.txt`. 159 station files in
  2025, 159 in 2026 and 45 in 2003.
- HEAD `.../2025/CRND0103-2025-NC_Asheville_8_SSW.txt`: 200, text/plain, Content-Length 79205,
  Last-Modified Thu, 01 Jan 2026 15:56:53 GMT. HEAD `.../2025/CRND0103-2025-AK_Fairbanks_11_NE.txt`: 200,
  79205 bytes, Last-Modified Tue, 25 Aug 2026 15:41:33 GMT. Files change after the year ends, so record
  Last-Modified and sha256. 79205 = 365 lines × 217 bytes, which fits the fixed-width format.
- Whole-archive snapshots (weekly): `.../daily01/snapshots/CRND0103-YYYYMMDDHHmm.zip`. The latest is
  `CRND0103-202609210850.zip` (previous: 202609140850, 202609070850). A snapshot is the best way to pin a version.

**Example station file names (2025, names only):**
CRND0103-2025-AK_Aleknagik_1_NNE.txt, CRND0103-2025-AK_Bethel_87_WNW.txt, CRND0103-2025-AK_Cordova_14_ESE.txt,
CRND0103-2025-AK_Deadhorse_3_S.txt, CRND0103-2025-AK_Denali_27_N.txt, CRND0103-2025-AK_Fairbanks_11_NE.txt,
CRND0103-2025-AK_Toolik_Lake_5_ENE.txt, CRND0103-2025-AL_Brewton_3_NNE.txt, CRND0103-2025-AL_Gainesville_2_NE.txt,
CRND0103-2025-AL_Scottsboro_2_NE.txt, CRND0103-2025-CA_Bodega_6_WSW.txt, CRND0103-2025-CA_Yosemite_Village_12_W.txt,
CRND0103-2025-CO_Nunn_7_NNE.txt, CRND0103-2025-GA_Newton_8_W.txt, CRND0103-2025-ID_Murphy_10_W.txt,
CRND0103-2025-KY_Bowling_Green_21_NNE.txt, CRND0103-2025-ME_Old_Town_2_W.txt, CRND0103-2025-MO_Joplin_24_N.txt,
CRND0103-2025-NC_Asheville_8_SSW.txt, CRND0103-2025-ND_Jamestown_38_WSW.txt, CRND0103-2025-NE_Whitman_5_ENE.txt,
CRND0103-2025-OR_Corvallis_10_SSW.txt, CRND0103-2025-TN_Crossville_7_NW.txt
(The full 159-name list was saved to scratchpad `rlaw/crn_2025_names.txt`.)

**Documented format (README.txt, updated 2017-07-06; HEADERS.txt)**: fixed width, one day per line, 28 fields,
whitespace-separated, computed over the station's 24-h LST day. Format version `03` (since 2013-01-07).
- F1 WBANNO, F2 LST_DATE (YYYYMMDD), F3 CRX_VN (string), F4 LONGITUDE, F5 LATITUDE
- F6 T_DAILY_MAX, F7 T_DAILY_MIN (°C)
- **F8 T_DAILY_MEAN** (°C) = (max+min)/2, "the typical historical approach", cols 55–61
- **F9 T_DAILY_AVG** (°C) = average air temperature (from 5-minute values), cols 63–69
- F10 P_DAILY_CALC (mm), F11 SOLARAD_DAILY (MJ/m²), F12 SUR_TEMP_DAILY_TYPE (R/C/U), F13–15 surface IR temperature (°C),
  F16–18 RH (%)
- F19–23 SOIL_MOISTURE_{5,10,20,50,100}_DAILY (m³/m³)
- **F24 SOIL_TEMP_5_DAILY (cols 178–184), F25 SOIL_TEMP_10_DAILY (186–192), F26 SOIL_TEMP_20_DAILY (194–200),
  F27 SOIL_TEMP_50_DAILY (202–208), F28 SOIL_TEMP_100_DAILY (210–216)**, all °C, "an average of the day's hourly soil
  measurements which are calculated from the multiple independent measurements"
- **Missing code:** "the lowest possible integer for a given column format, such as **-9999.0** for 7-character fields
  with one decimal place or **-99.000** for 7-character fields with three decimal places" (soil moisture fields
  therefore use -99.000). "There are no quality flags ... When the raw data are flagged as erroneous, these
  derived values are not calculated, and are instead reported as missing."
- **Reporting resolution:** temperatures are written in 7-character fields with **one decimal place (0.1 °C)**. Soil
  moisture has three decimals.
- **Sensor resolution/accuracy (sensor description PDFs, documentation/site/sensors/...):**
  - Air: 3 independent Thermometrics PT1000 PRTs in aspirated shields. "Platinum 1000 ohm ± 0.04% at 0°C
    (per IEC-751, Class A accuracy)", "Repeatability and Stability: Better than ± 0.01°C per year", "Accuracy:
    ±0.04% over full range", time constant 13 s (`AirTemp_ThermometricsPT1000PRT.pdf`).
  - Soil: Stevens Hydra Probe II SDI-12 with a built-in thermistor, 3 probe sets at 5/10/20/50/100 cm. "Soil
    dielectric and temperature measurements are sampled **hourly at the four lower depths and every 5 minutes
    at the 5 cm depth**". "Stations with soils that are not compatible with deep installations ... have only
    5 cm and 10 cm probes installed" (so 20/50/100 cm are missing at those stations). The description gives no
    thermistor resolution. The 2019 NOAA soil tech memo reports Hydra−Acclima soil-temperature differences of
    about −0.3 °C (2017), growing to about −4.0 °C when only two Hydras worked, and a Hydra failure rate of 337 of
    1383 probes over 2009–2015. Soil probes date from 2009, so soil series start in or after 2009.
- Other quirks: USRCRN stations (discontinued 2014-06-01) carry missing values for solar, surface, RH and soil. Precipitation
  algorithm versions changed (OAP 1.0 → 2.0 in 2015, 2.1 in 2016, 2.1.1 in 2017) and were applied retroactively.
  NDST rounding advice (documentation/program/NDST_Rounding_Advice.pdf) recommends "round half up asymmetric".
- Licence: NOAA/NCEI US-government data, public domain. The README states no restrictions.

**Usable:** yes. Pin a version by fetching one snapshot zip, or per-station yearly files with sha256 + Last-Modified.

---

## 4. Human two-step task, trial-level data with Gaussian-random-walk reward drift

### 4a. Kool, Cushman & Gershman 2016 (PLoS Comput Biol 12(8): e1005090), github.com/wkool/tradeoffs (**most usable**)
- Repo HEAD commit `6f849e13a8fe32c0b62ad768d3578068b93ee69e` (2017-10-17). No LICENSE file in the tree.
  (github.com web and api.github.com return 403 through this session's proxy. Anonymous git reads work.)
- Clone: `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/wkool/tradeoffs`, or raw files:
  `https://raw.githubusercontent.com/wkool/tradeoffs/6f849e13a8fe32c0b62ad768d3578068b93ee69e/data/daw%20paradigm/data.mat`
- Data files (HEAD content-length on raw.githubusercontent):
  - `data/daw paradigm/`: data.mat 1894663, subinfo.mat 3159, groupdata.mat 1691041, results.mat 419219, plus
    MB_MF_daw_rllik.m, groupanalysis.m, make_raw_data.m, mfit_wrapper.m, set_opts.m
  - `data/novel paradigm/`: data.mat 862030, subinfo.mat 3282, groupdata.mat 387715, results.mat 390728, plus the same .m files
  - `simulations/*.m` (incl. generate_rewards.m), `tasks/space_daw_task`, `tasks/space_novel_task` (jsPsych code)
- READMEs: root "Code, data, and tasks for 'When does model-based control pay off?'". data/README.md: "These
  directories contain all the raw data for both two-step paradigms, and the functions that are used to analyze
  them." **The READMEs do not document columns.** Columns are documented in code: `data/daw paradigm/make_raw_data.m`
  maps data.mat (a MATLAB cell array; column 1 = subject id, then 18 numeric columns) to stim_1_left, stim_1_right,
  rt1, choice1, stim_2_left, stim_2_right, rt2, choice2, win, state2, common, score, practice, **ps1a1, ps1a2,
  ps2a1, ps2a2 (the per-trial reward probabilities)**, trial. It keeps only subjects with exactly 150 rows
  (25 practice + 125 real) and marks a timeout as rt = −1.
- **Drift parameters are documented:** the task code (`tasks/space_daw_task/index.html`) has `var max = 0.75; var min = 0.25;
  var sd = 0.025;`, reflecting bounds, and initial values drawn from {0.25/0.75, 0.4/0.6} pairs. The paper says "Gaussian random walk
  (mean = 0, σ = 0.025) ... the same parameters used by Daw and colleagues". **Quirk:** increments are sampled with
  replacement from a pre-drawn pool of 1000 N(0, 0.025) values, not freshly drawn each trial. The novel paradigm
  uses reward points, not probabilities: σ = 2, bounds −4..+5, integer-rounded (`Math.round`). It is not the 0.025 drift.
- Participants (paper): 406 recruited on MTurk; **207 did the Daw-structure task** (125 trials), 199 did the novel task.
  The number of complete datasets retained by make_raw_data is not documented outside the data.
- Format blocker: `.mat` files need scipy.io.loadmat. The MAT version (v5 vs v7.3/HDF5) cannot be known without opening the file.

### 4b. Gillan, Kosinski, Whelan, Phelps & Daw 2016 (eLife 5:e11305), OSF https://osf.io/usdgt/
- Title "Characterizing a psychiatric symptom dimension related to deficits in goal-directed control". Public,
  created 2019-05-18, modified 2021-06-09. **No licence set** (node_license None).
- Files (OSF API `https://api.osf.io/v2/nodes/usdgt/files/osfstorage/`; use `page[size]=100&sort=name`, because default
  pagination returned duplicate entries):
  - `Experiment 1/twostep_data_study1/`: **649** per-subject CSVs (19228–39844 bytes), folder API
    `https://api.osf.io/v2/nodes/usdgt/files/osfstorage/5d30a113251f0e00190530ab/`
  - `Experiment 2/twostep_data_study2/`: **1712** per-subject CSVs (18661–19824 bytes), folder API
    `https://api.osf.io/v2/nodes/usdgt/files/osfstorage/5d30a139a667db0018f7b8a4/`
  - Exp 1: readme.rtf (1674 B, https://osf.io/download/gf69e/), self_report_study1.csv (34455 B, https://osf.io/download/fe9x3/)
  - Exp 2: readme.rtf (identical), self_report_study2.csv (189079), individual_items_study2.csv (666094), weights.csv (9308)
  - root: "Error in adminstration of one SDS Depression Item.rtf" (4827)
  - Downloads are `https://osf.io/download/<id>/`, which 302-redirects to application/octet-stream with Content-Length and
    Last-Modified. Example: Exp1 subject file 5fcdfcb6aa60b8035b893cf4 is 19988 B, Last-Modified 2020-12-07.
- readme.rtf (Nov 2019) columns: "Task data starts the row after the one that lists 'twostep_instruct_9' in column C",
  with a variable number of preamble rows. A = trial_num, **B–E = drift 1–4 (probability of reward after second stage option 1–4)**,
  F stage-1 response, G stage-1 stimulus, H stage-1 RT, I transition (common TRUE / rare FALSE), J stage-2 response,
  K stage-2 stimulus, L stage-2 state (2/3), M stage-2 RT, N reward (1/0), O constant 1.
- Drift: the paper documents "Gaussian Random Walks for 200 trials with ... boundaries at 0.25 and 0.75". **σ = 0.025
  is not stated** in the paper text found by grep, or in the readme. The per-trial drift columns would let it be
  estimated, but only after opening the data.
- Participants: Exp1 N = 548 analysed (646 submitted, 98 excluded); Exp2 N = 1413 analysed (1671 submitted, 258 excluded).
  The OSF counts (649 / 1712) exceed "submitted" slightly, so a prereg exclusion rule is needed. Exclusion criteria are in
  the paper (more than 10% missed trials, more than 95% same key, fast RTs, catch/IQ questions).

### 4c. Decker, Otto, Daw & Hartley 2016 (Psychol Sci 27(6):848–858), OSF https://osf.io/gq7z2
- The node metadata endpoint returns "Not found", but the file listing works: `Archive of OSF Storage/Decker_choices_for_RL.csv`
  (273786 B, https://osf.io/download/dnxwr/), `Decker_choices_for_MEregression.csv` (435188 B, https://osf.io/download/3tk9d/),
  `Data/Decker_subject_list.csv` (469 B, https://osf.io/download/ed2vy/). **No README**, so the columns and whether
  reward probabilities are included are undocumented. Not usable without opening the data.

### 4d. Daw et al. 2011 (Neuron)
- No public trial-level repository was found (search 2026-09-24). Its drift parameters (σ = 0.025, reflecting 0.25/0.75)
  are cited by Kool 2016. Other candidates surfaced by search, not inspected: github.com/carolfs/muddled_models
  (Feher da Silva & Hare 2020), osf.io/3stp9 (Lockwood et al.), github.com/ClaireSmid/Model-based_Model-free_Developmental.

**Pick: Kool 2016, Daw paradigm** (`data/daw paradigm/data.mat`). It has trial-level per-trial reward probabilities
(ps1a1..ps2a2) and a drift of σ = 0.025 with reflecting bounds of 0.25/0.75, documented in its own task code; the dataset is a single
1.9 MB file. Caveats: .mat format, no licence file, and increments drawn from a 1000-value pool. **Runner-up: Gillan 2016 Exp1/Exp2**
(far larger N, drift columns documented in readme.rtf, bounds documented). But σ is not documented, there is no licence,
there are 649 + 1712 separate files, and it has variable preamble rows.

---

Sources (fetched 2026-09-24): philadelphiafed.org median-forecasts page + spf-documentation.pdf; fred.stlouisfed.org/series/{CPIAUCSL,MICH,VIXCLS,SP500};
data.sca.isr.umich.edu docids 24776, 75445, 75433, 75436, 75437, 80741, faq.php; ncei.noaa.gov daily01 README/HEADERS and
documentation/site/sensors; github.com/wkool/tradeoffs; journals.plos.org (doi 10.1371/journal.pcbi.1005090);
osf.io/usdgt; elifesciences.org/articles/11305; osf.io/gq7z2; doi.org/10.1177/0956797616639301.
