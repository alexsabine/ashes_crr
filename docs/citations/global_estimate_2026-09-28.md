# Sources for Compute_Savings/DECLARATION_3 (fetched 2026-09-28, R10)

- **Date fetched:** 2026-09-28 (UTC; fetches between about 04:05Z and 04:17Z).
- **Purpose:** Compute_Savings DECLARATION_3, prompt-log entry 228 (the factors listed under "Sources to fetch on the day").
- **Fetched by:** a research agent (Claude Code subagent), with `curl` through the session proxy and web search to locate URLs.
  No figure below comes from a search-result summary; every quoted figure was read in the fetched page or PDF.
- **Quoting rule.** Quotes are verbatim from the fetched text. HTML was converted to text (tags removed, whitespace collapsed).
  For PDFs, text was extracted with `pypdf`; the extractor inserts stray spaces inside some words (e.g. "Ac celerated",
  "Lift- Off") and before punctuation. Those stray spaces are removed in the quotes below, and nothing else is changed.
  Table cells are shown with `|` between cells, as extracted.
- **PDF hashes** (sha256 of the files as downloaded on the day, for re-checking):
  - IEA *Energy and AI* (2025): `f9b90069ca5c014b67066998b0869735e399d8eb5b9fc64b5f9b215adc09cbbf`
  - IEA *Key Questions on Energy and AI* (2026): `a3a47f07b35420e74b243878f631192b04788110db3c75275feb0fbdee7f4858`
  - NVIDIA H100 architecture whitepaper: `3641614979809a027a8aabdc2e77639efb8fcd0f8dc7873a22ba2125489f5a27`
  - Uptime Institute Global Data Center Survey 2025: `b4e1075cb8ee6a72a287a9faeb91736e270e28cd8f35b0965303f41b17ed2c7f`
  - Llama 3 paper, arXiv 2407.21783v3: `481f1599468f95a07d05e97fafe55bbe786dc1624c6f881bcb4c7d14c933d083`

---

## 1. Global average electricity-grid carbon intensity (Ember)

**Primary source.** Ember, *Global Electricity Review 2026*. Published 21 Apr 2026 (page metadata `datePublished`
2026-04-21, `dateModified` 2026-06-22). Chapter pages:
- https://ember-energy.org/latest-insights/global-electricity-review-2026/2025-in-review (status **OK**, HTTP 200)
- https://ember-energy.org/latest-insights/global-electricity-review-2026/electricity-demand-and-supply-trends (status **OK**)
- https://ember-energy.org/latest-insights/global-electricity-review-2026/major-countries-and-regions (status **OK**)

> In 2025, the average kilowatt hour produced globally resulted in emissions of 458 gCO2e, 2.7% less than in 2024 (471 gCO2e) and down 16% from two deca[des …]

(2025-in-review chapter; the page text breaks off at the end of the extracted window, the figure is complete.)

> The emissions intensity of electricity has dropped 14% over the last decade, from 533 grams of CO2 equivalent per kWh (gCO2e/kWh) in 2015 to 458 gCO2e/kWh in 2025.

(electricity-demand-and-supply-trends chapter.)

> Despite similar fossil shares, US carbon intensity in 2025 (384 gCO2e/kWh) was below the global average (458 gCO2e/kWh)

(major-countries-and-regions chapter; the US figure is given for context only.)

**Previous edition, for the record.** Ember, *Global Electricity Review 2025* (published 8 Apr 2025, `dateModified`
2026-04-13), https://ember-energy.org/latest-insights/global-electricity-review-2025/major-countries-and-regions (status **OK**):

> The carbon intensity of US electricity generation was 384 gCO2/kWh – below the global average of 473 gCO2/kWh.

Note: the 2025 edition gives the 2024 global average as 473 gCO2/kWh; the 2026 edition gives 2024 as 471 gCO2e. Ember
revised the 2024 value between editions. The latest year available on the day is **2025: 458 gCO2e/kWh** (CO2-equivalent,
generation-based, location-based).

---

## 2. IEA, *Energy and AI* (2025) and its 2026 update

**Status of the IEA website.** Every iea.org page tried returned **HTTP 403** to the session proxy (curl and WebFetch):
`/reports/energy-and-ai`, `/reports/energy-and-ai/executive-summary`, `/reports/energy-and-ai/energy-demand-from-ai`,
the April 2025 press release, and the 2026 news release
`/news/data-centre-electricity-use-surged-in-2025-even-with-tightening-bottlenecks-driving-a-scramble-for-solutions`.
The IEA's own PDF host (iea.blob.core.windows.net) was **reachable**, so the quotes below come from the IEA's PDFs
directly, not from reporting.

### 2a. *Energy and AI* (World Energy Outlook Special Report, April 2025)

Source: https://iea.blob.core.windows.net/assets/34eac603-ecf1-464f-b813-2ecceb8f81c2/EnergyandAI.pdf (status **OK**;
304 pages; colophon "Typeset in France by IEA - April 2025"; PDF ModDate 2025-04-30, the latest of three copies found on
the IEA host, the other two dated 2025-04-09 and 2025-04-10). Page numbers are PDF page indices.

Data-centre electricity 2024 and 2030 (p. 63):

> Global electricity consumption by data centres is projected to reach around 945 TWh by 2030 in the Base Case, representing just under 3% of total global electricity consumption in 2030. This is more than double the estimated approximately 415 TWh for 2024 (Figure 2.10), which accounted for around 1.5% of today's global electricity demand.

Share of AI / accelerated servers (p. 56):

> As a second-best approach, estimates often rely on the electricity consumption of accelerated servers as a proxy for the share of AI in total electricity consumption from data centres. Accelerated servers accounted for 24% of server electricity demand and 15% of total data centre demand in 2024.

Growth of accelerated servers (p. 63):

> Electricity consumption in accelerated servers, which is mainly driven by AI technology adoption (Box 2.1), is projected to grow by 30% annually in the Base Case, while conventional server electricity consumption growth is slower at 9% per year.

Data-centre CO2 emissions, today and projected (p. 18, executive summary):

> Emissions from electricity use by data centres grows from 180 million tonnes (Mt) today to 300 Mt in the Base Case by 2035, and up to 500 Mt in the Lift-Off Case. While these emissions remain below 1.5% of the total energy sector emissions in this period, data centres are among the fastest growing sources of emissions.

"Today" is 2024 (p. 246, §5.8.1):

> Global fuel combustion CO2 emissions are estimated to reach 35 000 million tonnes (Mt) in 2024. Data centres account for around 180 Mt of indirect CO2 emissions today from the consumption of electricity, not including any emissions from backup power generation. This includes all workloads by data centres, of which AI is a subset.

2030 emissions (p. 87):

> Consequently, CO2 emissions from electricity generation for data centres peak at around 320 Mt CO2 by 2030, before entering a shallow decline to around 300 Mt CO2 by 2035.

Note for DECLARATION_3's "low" intensity (data-centre emissions / data-centre electricity): the IEA does not publish this
ratio as a figure. It must be computed by the script from the two quoted figures (180 Mt, 415 TWh, both 2024); it is not
quoted here.

### 2b. *Key Questions on Energy and AI* (World Energy Outlook Special Report, April 2026): the IEA's update

Source: https://iea.blob.core.windows.net/assets/3179f7f8-01f6-4dd6-bffa-c9f7b73f1dc9/KeyQuestionsonEnergyandAI.pdf
(status **OK**; 138 pages; colophon "Typeset in France by IEA - April 2026").

2025 and 2030 (p. 10, executive summary):

> Our updated projections see electricity consumption from data centres roughly doubling from 485 TWh in 2025 to 950 TWh in 2030, accounting for around 3% of global electricity demand by that date. Electricity consumption from AI-focused data centres grows much faster than overall data centre electricity consumption, tripling in this period.

2024 re-stated, 2030 revised from 945 to around 950 (p. 24):

> Now updated for this report, our Base Case still sees data centre electricity consumption growing from around 415 TWh in 2024 to around 950 TWh in 2030 (Figure 1.4).

AI-focused data centres in 2030 (p. 26):

> In the Base Case, the electricity consumption of these AI-focused data centres increases by more than threefold to 2030, reaching around 465 TWh by 2030 (Figure 1.5).

Emissions in 2035 (p. 13):

> The emissions associated with data centres double in IEA projections, reaching around 350 million tonnes in 2035, but still make up about 2% of global electricity sector emissions by that date.

Notes. (i) The 2026 update measures AI by "AI-focused data centres", the 2025 report by "accelerated servers"; the two
are different definitions and should not be mixed in one growth rate. (ii) No 2025 emissions figure ("today") was found
in the 2026 PDF by text search; the 2024 figure of 180 Mt (2a) is the latest confirmed "today" value. (iii) A 2030 AI-share
for 2026 would need the 2025 AI-focused consumption, which the text gives only as "more than threefold" growth to ~465 TWh;
no 2025 AI-focused TWh figure was confirmed verbatim.

### 2c. Reporting cross-checks (not used for figures)

- Carbon Brief, "AI: Five charts that put data-centre energy use – and emissions – into context", 15 Sep 2025,
  https://www.carbonbrief.org/ai-five-charts-that-put-data-centre-energy-use-and-emissions-into-context/ (status **OK**):
  > Under the IEA's central scenario for data-centre growth, the sector's global electricity consumption would more than double between 2024 and 2030, reaching 945 terawatt-hours (TWh) by the end of the decade.
- arXiv 2509.07218v3 (a review citing the IEA), https://arxiv.org/html/2509.07218v3 (status **OK**):
  > According to the IEA report [8], carbon emissions from the electricity use of global data centers reached 180 million tonnes (Mt) in 2024 and are projected to rise to 300 Mt by 2035
- **Caution:** carboncredits.com, "AI's Energy Hunger: Data Centers Set to Use Power Equal to Japan's by 2035" (status OK)
  prints figures that disagree with the IEA PDF ("emissions from data centers grow from 220 million tonnes (Mt) in 2024 to
  300-320 Mt by 2035"; "reaching about 1,050 TWh" by 2030). Not used; the IEA PDF governs.
- datacenterdynamics.com, nsenergybusiness.com, reglobal.org, eandt.theiet.org: HTTP **403**.

---

## 3. A measured data-centre carbon intensity (US)

Source: Guidi G., Dominici F., Gilmour J., Butler K., Bell E., Delaney S., Bargagli-Stoffi F. J., *Environmental Burden of
United States Data Centers in the Artificial Intelligence Era*, arXiv:2411.09786 [cs.CY], **v1** (submitted Thu, 14 Nov 2024;
v1 is the only version on the day). Abstract https://arxiv.org/abs/2411.09786 (status **OK**); full text
https://arxiv.org/html/2411.09786v1 (status **OK**).

> The average carbon intensity of the US data centers in our study (weighted by the energy they consumed) was 548 grams of CO2e per kilowatt hour (kWh), approximately 48% higher than the US national average of 369 gCO2e/kWh [26].

(HTML full text; the subscript in "CO 2 e" is rendered "CO2e" here.)

> Data centers' carbon intensity - the amount of CO$_{2}$e emitted per unit of electricity consumed - exceeded the US average by 48%.

(abstract.) Context from the paper's Limitations: "the uptime, or capacity utilization rate, is assumed to be 0.75 for all
data centers" (quoted verbatim); the 548 figure is an attributional, location-based estimate for the US in the paper's
study year ("2.18% of US emissions in 2023", abstract).

---

## 4. NVIDIA H100 SXM and DGX H100

### 4a. H100 product page

Source: NVIDIA, "NVIDIA H100 Tensor Core GPU", https://www.nvidia.com/en-us/data-center/h100/ (status **OK**; no version
date on the spec table; the page's FAQ cites benchmarks "as of April 2026"). Specification table, columns
`H100 SXM | H100 NVL`:

> BFLOAT16 Tensor Core | * | 1,979 teraFLOPS | 1,671 teraFLOPS

> Max Thermal Design Power (TDP) | Up to 700W (configurable) | 350-400W (configurable)

> \* With sparsity

So the product page shows only the **sparse** BF16 figure (1,979 TFLOPS, asterisked). The dense figure is not on this page.

### 4b. H100 architecture whitepaper (dense BF16)

Source: NVIDIA, *NVIDIA H100 Tensor Core GPU Architecture* whitepaper, on NVIDIA's asset host
https://nvdam.widen.net/s/95bdhpsgrs/nvidia_h100_tensor_core_gpu_architecture_whitepaper_v1.03 (status **OK**; the file is
named "…Whitepaper_V1.03.pdf" but its cover reads "V1.04", "Includes final GPU / memory clocks and final TFLOPS performance
specs."; 71 pages).

Table 1, "NVIDIA H100 Tensor Core GPU Performance Specs" (p. 20), columns `NVIDIA H100 SXM5 | NVIDIA H100 PCIe`:

> Peak BF16 Tensor Core 989.4 TFLOPS | 1978.9 TFLOPS1 756 TFLOPS | 1513 TFLOPS

> 1. Effective TFLOPS / TOPS using the Sparsity feature

Table 3, "Comparison of NVIDIA A100 and H100 Data Center GPUs" (pp. 39–40), columns `A100 | H100 SXM5 | H100 PCIe`:

> Peak BF16 Tensor TFLOPS with FP32 Accumulate 312/624 | 989.4/1978.9 | 756/1513

(the extracted cells run the footnote marker "1" into each number, e.g. "989.4/1978.91"; the footnote is "1. Effective
TOPS / TFLOPS using the Sparsity feature".)

> TDP | 400 Watts | 700 Watts | 350 Watts

(extracted as "TDP1 400 Watts 700 Watts 350 Watts".)

So: **dense BF16 Tensor Core peak, H100 SXM5 = 989.4 TFLOPS**; 1,978.9 (≈ 1,979) TFLOPS is **with sparsity**.
**TDP = 700 W** (product page: "Up to 700W (configurable)").

Independent confirmation of 700 W in a large run: Llama 3 paper (item 6), p. 9:
> Llama 3 405B is trained on up to 16K H100 GPUs, each running at 700W TDP with 80GB HBM3, using Meta's Grand Teton AI server platform (Matt Bowman, 2022).

### 4c. DGX H100 system power

Source: NVIDIA DGX H100/H200 User Guide, "Introduction to the NVIDIA DGX H100/H200 System",
https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html (status **OK**; "Last updated on Jan 26, 2026").

> The DGX H100/H200 systems are built on eight NVIDIA H100 Tensor Core GPUs or eight NVIDIA H200 Tensor Core GPUs.

> Table 3. Power Specifications | Input | Specification for Each Power Supply | 200-240 volts AC | 10.2 kW max. | 3300 W @ 200-240 V, 16 A, 50-60 Hz

> Power supply | 6 x 3.3 kW

The "10.2 kW max." cell is the system input maximum (the per-supply specification is 3,300 W; six supplies in 4+2
redundancy). The NVIDIA DGX H100 marketing page (https://www.nvidia.com/en-us/data-center/dgx-h100/, status OK) carried no
power figure in its static HTML.

---

## 5. PUE

### 5a. Industry average: Uptime Institute Global Data Center Survey 2025

Source: Uptime Institute, *Uptime Institute Global Data Center Survey 2025*, UII Keynote Report 180, July 2025 (PDF creation
date 2025-08-06), https://datacenter.uptimeinstitute.com/rs/711-RIA-145/images/2025.Annual.Survey.Report.pdf (status **OK**;
31 pages). The Uptime landing pages for the 2025 and 2024 survey results (uptimeinstitute.com/resources/research-and-reports/…)
returned 200 but carry no figures (the summary is behind a form).

> In 2025, respondents' annual PUE had a weighted average of 1.54 (see Figure 2), marking the sixth consecutive year that this headline figure has virtually stood still.

(p. 7.) Also (p. 8):

> Facilities commissioned within five years of the survey (from around early 2020) achieved an average PUE of 1.48. Notably, larger data centers (20 MW and above) averaged a PUE of 1.44 globally

The 2024 survey's figure (~1.56) was **not fetched** and is UNCONFIRMED; the 2025 figure is the latest and is used.

### 5b. Hyperscaler fleet: Google

Source: Google Data Centers, "Power usage effectiveness", https://datacenters.google/efficiency/ (status **OK**; the old URL
https://www.google.com/about/datacenters/efficiency/ serves the same page).

> In 2025, the average annual power usage effectiveness for our global fleet of data centers was 1.09.

> We report a comprehensive trailing twelve-month (TTM) PUE of 1.09 across all our large-scale data centers (once they reach stable operations), in all seasons, including all sources of overhead.

> According to the Uptime Institute's 2025 Global Data Center Survey, the global average PUE of respondents' data centers was 1.54.

The page's "2026 PUE Yearly Report" table, fleet row, reads "Fleet | 1.08 | 1.09" under "Quarterly PUE | Trailing
twelve-month (TTM) PUE" (2026 Q1: quarterly 1.08, TTM 1.09).

---

## 6. Model FLOPs utilisation of a published large run

Source: Llama Team, AI @ Meta, *The Llama 3 Herd of Models*, arXiv:2407.21783, **v3** (Sat, 23 Nov 2024; the current version
on the day; v1 31 Jul 2024, v2 15 Aug 2024). Abstract https://arxiv.org/abs/2407.21783 (status **OK**); PDF
https://arxiv.org/pdf/2407.21783v3 (status **OK**). §3.3.2, p. 10:

> Through careful tuning of the parallelism configuration, hardware, and software, we achieve an overall BF16 Model FLOPs Utilization (MFU; Chowdhery et al. (2023)) of 38-43% for the configurations shown in Table 4.

Table 4 ("Scaling configurations and MFU for each stage of Llama 3 405B pre-training"), columns
`GPUs | TP | CP | PP | DP | Seq. Len. | Batch size/DP | Tokens/Batch | TFLOPs/GPU | BF16 MFU`:

> 8,192 | 8 | 1 | 16 | 64 | 8,192 | 32 | 16M | 430 | 43%
> 16,384 | 8 | 1 | 16 | 128 | 8,192 | 16 | 16M | 400 | 41%
> 16,384 | 8 | 16 | 16 | 8 | 131,072 | 16 | 16M | 380 | 38%

MFU band confirmed: **0.38 to 0.43** (so DECLARATION_3's fallback "ASSUMED 0.3 to 0.45" is not needed).

---

## 7. Tonnes of CO2 per typical passenger vehicle per year

Source: US EPA, Green Vehicle Guide, "Greenhouse Gas Emissions from a Typical Passenger Vehicle",
https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle (status **OK**; "Last updated on June 3, 2026").

> A typical passenger vehicle emits about 4.6 metric tons of carbon dioxide per year. This number can vary based on a vehicle's fuel, fuel economy, and the number of miles driven per year.

> A typical passenger vehicle emits about 4.6 metric tons of CO2 per year. This assumes the average gasoline vehicle on the road today has a fuel economy of about 22.2 miles per gallon and drives around 11,500 miles per year.

(US tailpipe CO2 only; a US-specific figure.)

---

## Summary

| item | figure | unit | confirmed verbatim | source |
|---|---|---|---|---|
| 1. global grid carbon intensity, 2025 | 458 | gCO2e/kWh | yes | Ember, Global Electricity Review 2026 (21 Apr 2026) |
| 1. global grid carbon intensity, 2024 (revised) | 471 (GER 2026); 473 (GER 2025) | gCO2e/kWh; gCO2/kWh | yes | Ember GER 2026; GER 2025 |
| 2. data-centre electricity, 2024 | ~415 | TWh | yes | IEA, Energy and AI (Apr 2025) PDF p. 63; re-stated in Key Questions (Apr 2026) p. 24 |
| 2. data-centre electricity, 2030 Base Case | ~945 (2025 report); ~950 (2026 update) | TWh | yes | IEA Energy and AI p. 63; Key Questions p. 10, 24 |
| 2. data-centre electricity, 2025 | 485 | TWh | yes | IEA, Key Questions on Energy and AI (Apr 2026) p. 10 |
| 2. accelerated servers' share, 2024 | 24 of server demand; 15 of total data-centre demand | % | yes | IEA Energy and AI p. 56 |
| 2. accelerated-server electricity growth, Base Case | 30 | % per year | yes | IEA Energy and AI p. 63 |
| 2. AI-focused data-centre electricity, 2030 | ~465 ("more than threefold" from 2025) | TWh | yes | IEA Key Questions p. 26 |
| 2. data-centre CO2, 2024 ("today") | ~180 | Mt CO2 | yes | IEA Energy and AI p. 18, p. 246 |
| 2. data-centre CO2, 2030 | ~320 (peak) | Mt CO2 | yes | IEA Energy and AI p. 87 |
| 2. data-centre CO2, 2035 | ~300 (Base); up to 500 (Lift-Off); ~350 (2026 update) | Mt CO2 | yes | IEA Energy and AI p. 18; Key Questions p. 13 |
| 2. data-centre CO2, 2025 | — | Mt CO2 | no (UNCONFIRMED; not found) | — |
| 3. measured US data-centre carbon intensity | 548 | gCO2e/kWh | yes | Guidi et al., arXiv 2411.09786v1 |
| 3. US national average (same paper) | 369 | gCO2e/kWh | yes | Guidi et al., arXiv 2411.09786v1 |
| 4. H100 SXM max TDP | 700 | W | yes | NVIDIA H100 product page; H100 whitepaper Table 3 |
| 4. H100 SXM5 BF16 Tensor Core peak, dense | 989.4 | TFLOPS | yes | NVIDIA H100 architecture whitepaper (V1.04), Tables 1 and 3 |
| 4. H100 SXM BF16 Tensor Core peak, with sparsity | 1,979 (page); 1978.9 (whitepaper) | TFLOPS | yes | NVIDIA H100 product page; whitepaper |
| 4. DGX H100 system max input power (8 GPUs) | 10.2 | kW | yes | NVIDIA DGX H100/H200 User Guide, Table 3 (updated 26 Jan 2026) |
| 5. industry-average PUE, 2025 | 1.54 | ratio | yes | Uptime Institute Global Data Center Survey 2025 (UII Report 180) p. 7 |
| 5. industry-average PUE, 2024 | ~1.56 | ratio | no (UNCONFIRMED; not fetched) | — |
| 5. Google fleet PUE, 2025 / TTM | 1.09 | ratio | yes | Google, datacenters.google/efficiency |
| 6. Llama 3 405B BF16 MFU | 38–43 | % | yes | Llama 3 paper, arXiv 2407.21783v3, §3.3.2 and Table 4 |
| 7. typical US passenger vehicle | 4.6 | metric t CO2 per year | yes | US EPA (updated 3 Jun 2026) |

Unconfirmed: the IEA's 2025 data-centre CO2 figure (not found in the 2026 update's text) and Uptime's 2024 PUE (not
fetched; the 2025 value is confirmed and is the latest). The ratio 180 Mt / 415 TWh (DECLARATION_3's "low" intensity) is
not a published figure and is left for the script to compute.
