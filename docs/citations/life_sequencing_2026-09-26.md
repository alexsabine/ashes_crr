# Life sciences dossier: DNA sequencing and germline mutation (2026-09-26)

For `Life_Sciences/DECLARATION_1.md` Part 3 (DS-1 to DS-5), fetched on the day under R10.

A note, not evidence (R8). Quotes are verbatim substrings of the saved texts.

- Raw texts are in the session scratchpad at `life/seq/*.txt`. PMC articles were fetched as JATS XML through NCBI efetch and
  flattened to text (title, abstract, body paragraphs). Code and docs come from shallow clones at the commits named below.
- The machine-readable claims are in `life/seq_claims.json`: 27 claims and 84 quotes. Each quote was checked with Python to be
  a substring of its saved text after collapsing whitespace. Result: **84/84 verified**.
- Code quotes are shown with their whitespace collapsed.
- Nothing here claims novelty for CRR.

Corrections to the brief, all found on the day:

- Squigulator was published in *Genome Research* 34:778 (2024), not *Nat Methods*.
- Wang & Obbard 2023 was published in *Evolution Letters* 7:216, not *Heredity*.
- DECLARATION_1 DS-2 calls the two-window t-statistic "the segmentation used by Scrappie and Tombo-style tools". That holds
  for Scrappie, Nanopolish, f5c, Uncalled4 and the older MinKNOW. It does **not** hold for Tombo on DNA. Tombo's DNA default
  is a running difference of neighbouring-window means, and it uses a t-test only for RNA (see A.2).

---

## A. Nanopore raw-signal segmentation (DS-2, DS-3)

### A.1 Scrappie (ONT): the two-window t-statistic detector

- **Version:** nanoporetech/scrappie `master` @ `5ccddbc1fded55772ca2d62617e7262b12fd4ca9` (commit 2022-01-13).
- **URL:** https://github.com/nanoporetech/scrappie (`src/event_detection.{c,h}`).
- **Fetch status:** fetched via raw.githubusercontent.com and a git clone. The GitHub REST API refused the request (the
  repository is not enabled for this session's API), so the commit was read by `git ls-remote` and the clone.
- **Raw files:** `life/seq/scrappie_event_detection.h.txt`, `life/seq/scrappie_event_detection.c.txt`.

> static detector_param const event_detection_defaults = { .window_length1 = 3, .window_length2 = 6, .threshold1 = 1.4f, .threshold2 = 9.0f, .peak_height = 0.2f }; [DS-2]

> Compute windowed t-statistic from summary information [DS-2]

> //t-stat //  Formula is a simplified version of Student's t-statistic for the //  special case where there are two samples of equal size with //  differing variance [DS-2]

> tstat[i] = fabs(delta_mean) / sqrt(combined_var / w_lengthf); [DS-2]

> float *tstat1 = compute_tstat(sums, sumsqs, nsample, edparam.window_length1); float *tstat2 = compute_tstat(sums, sumsqs, nsample, edparam.window_length2); [DS-2]

> //Dominate other tstat signals if we're going to fire at some point [DS-2]

> //Have we convinced ourselves we've seen a peak if (detector->peak_value - current_value > peak_height && detector->peak_value > detector->threshold) { detector->valid_peak = true; } [DS-2]

> //Finally, check the distance if this is a good peak if (detector->valid_peak && (i - detector->peak_pos) > detector->window_length / 2) { [DS-2]

**Bears on DS-2.** This is the domain's detector T, as the code implements it. It runs two t-statistics:

- a short one with windows of w = 3 samples each side and threshold 1.4;
- a long one with windows of w = 6 and threshold 9.0.

Each statistic is |mean₂ − mean₁| / √(combined_var / w). A local maximum becomes a boundary when three things hold:

- it exceeds the threshold;
- the statistic then falls from the peak by more than peak_height = 0.2;
- more than w/2 samples have passed.

The short detector masks the long one. DS-2's "T" is a single-window version of this (w ∈ {3, 5, 7}, tuned threshold, minimum
spacing 2).

### A.2 Tombo (ONT): running neighbouring-window difference for DNA, t-test for RNA

- **Version:** nanoporetech/tombo `master` @ `f5ea43fec759f1523097ed7aa68e80b7901c3046` (commit 2023-05-03).
- **URL:** https://github.com/nanoporetech/tombo (`docs/resquiggle.rst`, `tombo/_default_parameters.py`,
  `tombo/tombo_helper.py`, `tombo/resquiggle.py`).
- **Fetch status:** fetched by git clone.
- **Raw files:** `life/seq/tombo_resquiggle.rst.txt`, `life/seq/tombo_default_parameters.py.txt`, `life/seq/tombo_helper.py.txt`,
  `life/seq/tombo_resquiggle.py.txt`.

> Events are determined by identifying large shifts in current level, by taking the running difference between neighboring windows of raw signal (explicitly set this parameter with the ``--segmentation-parameters`` option). The largest jumps (or most significant via a t-test for RNA) are chosen as the breakpoints between events. [DS-2]

> # table containing default segmentation parameters for different sample types # 1) running neighboring window width for segmentation scoring # 2) minimum observations per genomic base # 3) raw re-squiggle minimum observations per genomic base # 4) mean number of observations per event during segmentation SEG_PARAMS_TABLE = { RNA_SAMP_TYPE:(12, 6, 2, 15), DNA_SAMP_TYPE:(5, 3, 1, 5), } [DS-2]

> use_t_test_seg (bool): use t-test segmentation criterion (default: raw neighboring window difference) [DS-2]

> # RNA bases show consistent variable spread so use t-test segmentation [DS-2]

> For RNA samples, stalled bases are detected using a moving window mean approach and event boundaries located within a stalled base are removed from downstream processing. [DS-3]

**Bears on DS-2.** Tombo's DNA segmentation is a running neighbouring-window mean difference with window 5 and a minimum of 3
observations per base. It keeps the largest jumps, and the number of events is set by mean observations per event (5), not by a
threshold. It is not a t-statistic. DS-2's T therefore represents Scrappie-lineage tools, and Tombo DNA only loosely.

**Bears on DS-3.** Tombo treats stalls explicitly, for RNA only.

### A.3 Nanopolish and f5c (eventalign): Scrappie's detector, vendored

- **Nanopolish:** jts/nanopolish `master` @ `28e774088b4a780b86066571896348e790f4113c` (commit 2023-08-05),
  `src/thirdparty/scrappie/event_detection.h`. Fetched by git clone. Raw file: `life/seq/nanopolish_event_detection.h.txt`.
  (nanoporetech/nanopolish, a fork, is at `f1de746…` from 2018-09-12. Not used.)
- **f5c:** hasindu2008/f5c `master` @ `08441cd9dbc7e48f4a5a977da3a739625f612f12` (commit 2026-08-21), `src/events.c`. Fetched by
  git clone. Raw file: `life/seq/f5c_events.c.txt`.

> static detector_param const event_detection_rna = { .window_length1 = 7, .window_length2 = 14, .threshold1 = 2.5f, .threshold2 = 9.0f, .peak_height = 1.0f }; [DS-2] (Nanopolish; the DNA default is byte-identical to Scrappie's line in A.1)

> static detector_param const event_detection_defaults = {.window_length1 = 3, .window_length2 = 6, .threshold1 = 1.4f, .threshold2 = 9.0f, .peak_height = 0.2f}; [DS-2] (f5c)

> tstat[i] = fabs(delta_mean) / sqrt(combined_var / w_lengthf); [DS-2] (f5c)

**Bears on DS-2.** The same detector and the same DNA parameters (3/6, 1.4/9.0, 0.2) are used across the eventalign lineage.

### A.4 Uncalled4 (Kovaka et al. 2025)

- **Paper:** Kovaka S. et al., "Uncalled4 improves nanopore DNA and RNA modification detection via fast and accurate signal
  alignment", *Nat Methods* 22:681. PMC11978507.1, epub 2025-03-28, doi 10.1038/s41592-025-02631-4.
- **Paper URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC11978507/. Fetched (PMC XML). Raw file: `life/seq/uncalled4_2025.txt`.
  The bioRxiv preprint (doi 10.1101/2024.03.05.583511, PMC10942365) was located but not fetched.
- **Code:** skovaka/uncalled4 `main` @ `b3993fab379e8e534947ce80fe97ecd008ef6f83` (commit 2024-09-27),
  `src/cpp/event_detector.cpp`. Raw file: `life/seq/uncalled4_event_detector.cpp.txt`.

> First, the individual sensor readings (raw samples) are segmented into ‘events’ using the same algorithm as UNCALLED8, which uses rolling t-tests to group samples with similar current levels. [DS-2]

> This groups signal representing the same nucleotides, although variable sequencing speeds result in frequent ‘stays’ (consecutive events representing the same k-mer, roughly 50% of events) and fewer frequent ‘skips’ (an event representing multiple k-mers, ~1–5% of events). [DS-2] [DS-3]

> Event detection parameters are chosen depending on the sequencing chemistry, where RNA uses longer t-test window lengths than DNA to adjust for the slower sequencing speed. [DS-2]

> EventDetector::PRMS_450BPS = { window_length1 : 3, window_length2 : 6, threshold1 : 1.4, threshold2 : 9.0, peak_height : 0.2, [DS-2]

> EventDetector::PRMS_70BPS = { window_length1 : 7, window_length2 : 12, threshold1 : 2.8, threshold2 : 18.0, peak_height : 0.2, [DS-2]

> EventDetector::PRMS_130BPS = { window_length1 : 5, window_length2 : 10, threshold1 : 2.1, threshold2 : 13.5, peak_height : 0.2, [DS-2]

**Bears on DS-2.** Window lengths and thresholds are tuned to the translocation speed (samples per base), which is a clock-side
choice.

**Bears on DS-3.** Even the domain's detector over-segments. About 50% of events are "stays", and 1–5% are "skips" (missed
boundaries).

### A.5 ONT's own event-detection description (via Rang et al. 2018)

- **Paper:** Rang F.J., Kloosterman W.P., de Ridder J., "From squiggle to basepair: computational approaches for improving
  nanopore sequencing read accuracy", *Genome Biol* 19:90. PMC6045860.1, epub 2018-07-13, doi 10.1186/s13059-018-1462-9.
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6045860/. Fetched. Raw file: `life/seq/rang2018.txt`.
- ONT's community pages were not fetched because they need a login. Rang et al. cite ONT (their ref. [19]).

> According to ONT, MinKNOW (up to v1.9) performed segmentation by calculating t statistics over two pairs of adjacent sliding windows in the raw signal [19]. These statistics were then combined to determine event boundaries. For each event, the mean, standard deviation, and duration of the raw signal were reported and used for further base calling. [DS-2]

> To deal with the oversampling, the initial MinION base callers required segmentation of the raw signals into discrete events before base identification. [DS-2]

**Bears on DS-2.** ONT's own segmentation, MinKNOW up to v1.9, was the two-pair adjacent-window t-statistic.

### A.6 Sampling: samples per base (R9.4.1 and R10.4.1)

- **Sources:**
  - Rang et al. 2018, as in A.5.
  - Squigulator code, hasindu2008/squigulator `master` @ `6f59e70df1149103e7612274747c0a851f805322` (commit 2026-02-26),
    `src/sim.c` and `docs/man.md`.
  - Uncalled4 paper, as in A.4.
  - Delahaye & Nicolas 2021, as in A.7.
- **Raw files:** `life/seq/rang2018.txt`, `life/seq/squigulator_sim.c.txt`, `life/seq/squigulator_man.txt`,
  `life/seq/uncalled4_2025.txt`, `life/seq/delahaye2021.txt`.

> For the current MinION chemistry, ONT reports that single DNA strands are pulled through the pore at an average speed of 450 bp/s, while the electric current is sampled at a frequency of 4 kHz [34]. This means that there are on average nine discrete measurements per k-mer, although the number varies because of the fluctuating translocation speed of the motor protein. [DS-2] (Rang 2018)

> profile_t prom_r9_dna_prof = { .digitisation = 2048, .sample_rate = 4000, .bps = 450, [DS-2] (Squigulator)

> .dwell_mean=9.0, //this must be sample_rate/bps for now .dwell_std=4.0 }; profile_t minion_r9_rna_prof [DS-2] (Squigulator, R9 DNA)

> profile_t prom_r10_dna_prof = { .digitisation = 2048, .sample_rate = 5000, .bps = 400, [DS-2] (Squigulator)

> .dwell_mean=13.0, //this must be sample_rate/bps for now .dwell_std=4.0 }; profile_t minion_r10_dna_prof [DS-2] (Squigulator, R10 DNA)

> pore version (for example, r9.4.1, r10.4.1), sequencing speed (for example, 400 bases per second (bps)) [DS-2] (Uncalled4)

> r10.4.1 MinION flow cells (ONT, FLO-MIN114) using either 260 or 400 bases per second mode [DS-2] (Uncalled4)

> Knowing the rate at which the electrical is sampled, 4.000 samples per second according to ONT [DS-2] (Delahaye 2021)

**Bears on DS-2.**

- R9.4.1 DNA runs at 4 kHz and 450 bases/s, about 9 samples per base. DS-2's dwell mean of 9 samples matches this.
- R10.4.1 DNA runs at 5 kHz and 400 bases/s. Squigulator's R10 profile uses a dwell mean of 13 samples.

### A.7 Known error modes (DS-3)

- **Wang Y. et al. 2021**, "Nanopore sequencing technology, bioinformatics and applications", *Nat Biotechnol* 39:1348.
  PMC8988251.1 (author manuscript), epub 2021-11-08, doi 10.1038/s41587-021-01108-x. Fetched. Raw file:
  `life/seq/wang2021_natbiotech.txt`.
- **Delahaye C., Nicolas J. 2021**, "Sequencing DNA with nanopores: Troubles and biases", *PLoS ONE* 16:e0257521.
  PMC8486125.1, epub 2021-10-01, doi 10.1371/journal.pone.0257521. Fetched. Raw file: `life/seq/delahaye2021.txt`.
- **Rang et al. 2018**, as in A.5.

> (i) the structural similarity of the nucleotides; (ii) the simultaneous influence of multiple nucleotides on the signal [23]; (iii) the nonuniform speed at which nucleotides pass through the pore [24–26]; and (iv) the fact that the signal does not change within homopolymers [26] (Fig. 2). [DS-3] (Rang 2018)

> The detection of homopolymers with nanopores is more challenging because consecutive k-mers are identical. As the segmentation step often resulted in more events than actual bases, initial base callers assumed that identical signals were the result of stalling in the pore rather than signals originating from a homopolymer. [DS-3] (Rang 2018)

> However, the R9.4 and R9.5 have difficulty sequencing very long homopolymer runs because the current signal of CsgG is determined by approximately five consecutive nucleotides. [DS-3] (Wang 2021)

> The raw current measurement can be segmented based on current shift to capture individual signals from each k-mer. Each current segment contains multiple measurements, and the corresponding mean, variance and duration of the current measurements together make up the event’ data. [DS-2] (Wang 2021)

> In the context of homopolymers, this results into (1) an usually well segmented signal, both in terms of duration and value, for homopolymers of length ≤ 5 bases long, thus being mostly well sequenced, unlike (2) longer homopolymers for which the current is far less influenced by surrounding bases, which results in a harder to segment signal, making it harder to correctly assess the homopolymer length. [DS-3] (Delahaye 2021)

> Since the DNA translocation speed is not constant, this results in difficulties determining the exact length of homopolymers. [DS-3] (Delahaye 2021)

> An analysis of raw electrical signal associated to deletion of at least 5 bases showed that the translocation rate was at least twice as fast on deleted parts (median ≃ 1,220 bases per second) than right before (median ≃ 460 bases per second) or right after (median ≃ 520 bases per second) these errors. [DS-3] (Delahaye 2021)

> a higher translocation speed lead to a dramatic increase of error rate (above 20% for speeds over 650 bases per second) [DS-3] (Delahaye 2021)

**Bears on DS-3.** Three error modes are named by the domain itself:

- level changes too small to see: similar nucleotides, and identical k-mers in homopolymers;
- short dwells: fast translocation co-locates with deletions;
- variable speed.

This fits the reading that detectability depends on |Δμ| and dwell length n. The domain states it without CRR, so it is at
most REDUNDANT-DOMAIN, as the declaration expects.

### A.8 Squigulator (Gamaarachchi et al. 2024)

- **Paper:** Gamaarachchi H. et al., "Simulation of nanopore sequencing signal data with tunable parameters", *Genome Res*
  34:778. PMC11216307.1, ppub 2024-05, doi 10.1101/gr.278730.123.
- **Paper URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC11216307/. Fetched. Raw file: `life/seq/squigulator2024.txt`.
- **Code:** as in A.6. Raw files: `life/seq/squigulator_gensig.c.txt`, `life/seq/squigulator_man.txt`,
  `life/seq/squigulator_sim.c.txt`.

> Normal distributions are used for modeling noise along amplitude domains of the signal, where the mean and standard deviation of each k-mer in the pore-model form a random number generator. Normal distributions are also used for generating noise along the time domain (dwell), and other signal metadata such as offset and median_before. Read length variability is modeled using a gamma distribution. [DS-2]

> sps = round(nrng(core->rand_time[tid])); sps = sps < 1 ? -sps + 1 : sps; [DS-2] (gensig.c: dwell per k-mer)

> s=nrng(core->kmer_gen[tid][kmer_rank]); [DS-2] (gensig.c: each sample)

> `--dwell-mean FLOAT`: Mean of number of signal samples per k-mer/base. This is usually the sampling rate (4000Hz for DNA and 3000Hz for RNA) divided by translocation speed in bases per second (450 for R9.4.1 pore for DNA and 70 for RNA). [default: 9.0] [DS-2]

> `--dwell-std FLOAT`: Standard deviation of number of signal samples per k-mer/base. Increasing this will increase time-domain noise. Setting this to 0 is same as `--ideal-time`. [DS-2]

> `--amp-noise FLOAT`: The amplitude noise factor. This factor is multiplied with level standard deviation values in the pore-model. [DS-2]

> In fact, basecalling was much more sensitive to dwell-time noise (i.e., standard deviation) than to fixed changes in the dwell-time mean (Supplemental Fig. S3B,C). [DS-3]

> default value is ‐‐dwell-std = 4 [DS-2]

> (e.g., 450 nt/sec and 400 kHz for DNA sequencing on R9.4.1 flow cells) [DS-2]

The paper's "400 kHz" contradicts the tool's own 4000 Hz profile (A.6) and man page. It is quoted verbatim and read as a typo
for 4 kHz.

**Bears on DS-2.**

- Squigulator draws each k-mer's dwell from a rounded **normal** with mean 9 and sd 4 samples (R9 DNA), reflected to ≥ 1.
- It draws each sample from a normal with the k-mer's pore-model level mean and sd.
- DS-2 declares Gamma(shape 2, mean 9) dwells, minimum 2. The mean is the same, but the shape is different: Gamma(2) has
  sd ≈ 6.4 against Squigulator's 4. This is a declared choice and is recorded here only for comparison.

---

## B. Illumina sequencing by synthesis (DS-5)

- **Kircher M., Stenzel U., Kelso J. 2009**, "Improved base calling for the Illumina Genome Analyzer using machine learning
  strategies", *Genome Biol* 10:R83. PMC2745764.1, epub 2009-08-14, doi 10.1186/gb-2009-10-8-r83.
  URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC2745764/. Fetched. Raw file: `life/seq/kircher2009.txt`.
- **Bentley D.R. et al. 2008**, "Accurate whole human genome sequencing using reversible terminator chemistry", *Nature*
  456:53. PMC2581791.1 (author manuscript), doi 10.1038/nature07517.
  URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC2581791/. Fetched. Raw file: `life/seq/bentley2008.txt`.

> Base incorporation ceases after the addition of a single base due to the 3' termination of the incorporated nucleotides. [DS-5] (Kircher 2009)

> Phasing and pre-phasing are caused by incomplete removal of the 3' terminators and fluorophores, sequences in the cluster missing an incorporation cycle, as well as by the incorporation of nucleotides without effective 3' terminators. [DS-5] (Kircher 2009)

> As the number of cycles increases, the fraction of sequences per cluster affected by phasing increases, hampering the identification of the correct [DS-5] (Kircher 2009)

> reduced the phasing rates determined by Bustard from, on average, 0.8% per cycle to 0.5%, and pre-phasing from 0.6% to 0.4% per cycle. [DS-5] (Kircher 2009)

> The sequencing error, measured as the mismatch rate, increases with cycle number. [DS-5] (Kircher 2009)

> We sequenced DNA templates by repeated cycles of polymerase-directed single base extension. To ensure base-by-base nucleotide incorporation in a stepwise manner, we used a set of four reversible terminators [DS-5] (Bentley 2008)

> After each cycle of incorporation, we determined the identity of the inserted base by laser-induced excitation of the fluorophores and imaging. [DS-5] (Bentley 2008)

**Bears on DS-5.** The chemistry imposes one base per cycle, so the clock and the base count coincide by design. The error
that exists is the loss of that coincidence within a cluster (phasing and pre-phasing), and it grows with cycle number. This
supports the SILENT reading. No test follows.

---

## C. Germline mutation rate per generation and per year (DS-4)

### C.1 Bergeron et al. 2023

- **Paper:** Bergeron L.A. et al., "Evolution of the germline mutation rate across vertebrates", *Nature* 615:285.
  PMC9995274.1, epub 2023-03-01, doi 10.1038/s41586-023-05752-y.
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC9995274/. Fetched (full text). Raw file: `life/seq/bergeron2023.txt`.

> Here we quantify germline mutation rates across vertebrates by sequencing and comparing the high-coverage genomes of 151 parent–offspring trios from 68 species of mammals, fishes, birds and reptiles. We show that the per-generation mutation rate varies among species by a factor of 40 [DS-4]

> Overall, µgeneration varies by a factor of 40 across all species. [DS-4]

> The average pedigree-based mutation rates per generation for each species, which are represented by the squares, show 40-fold variation among species. [DS-4]

> The estimated average µyearly_modelled varies more than 120-fold among species (Supplementary Note 1 and Supplementary Table 9), with the highest µyearly_modelled estimated for the Texas banded gecko at 1.96 × 10−8 mutations per site per year [DS-4]

> whereas the lowest µyearly_modelled estimates were obtained for two bird species, the griffon vulture and the snowy owl, both with less than 0.18 × 10−9 mutations per site per year [DS-4]

> This large amount of interspecific variation is remarkable given that pedigree-based GMR estimates of individual species assessed by previous separate studies only show an approximately 16-fold variation in yearly GMRs34,51. [DS-4]

> Within primates, we observed a twofold variation across species [DS-4] (the context is µyearly_modelled)

> When sample sizes are small, yearly rates are commonly inferred by dividing the per-generation rate by the average age of the parents (or the generation time if parental age is unknown)49–51. [DS-4]

> Bearing this in mind, we decided to use µyearly_modelled for the current analysis as we believe that this measure is more representative of the yearly rate at the generation time for each species (estimated yearly rates are provided in Supplementary Table 9 for comparison). [DS-4]

> Unfortunately, small per-species sample sizes in our dataset precluded modelling the effects of parental age separately for each species. However, we observed very similar intercepts and slopes across taxonomic groups, allowing us to fit a joint model for all species. [DS-4]

> In total there are 55 species with modelled per-generation rates, including 32 mammalian and 15 avian species. [DS-4]

> The generation time, age at maturity and species-level fecundity are the key life-history traits affecting this variation among species. [DS-4]

> The exceptionally high yearly mutation rates of domesticated animals, which have been continually selected on fecundity traits including shorter generation times, further support the importance of generation time in the evolution of mutation rates. [DS-4]

> For the 105 trios for which parental age was known at reproduction, we found a significant positive association between µgeneration and the average parental age at reproduction (linear regression adjusted r2 = 0.14, P = 3.9 × 10−5; Fig. 1b). [DS-4]

> Our results (Fig. 1b), as well as previous studies of mice, humans and cats20,34, imply that parents always carry a minimum number of mutations in their gametes regardless of their age. [DS-4]

> all three of these regressions have similar positive y-intercept values on the order of approximately 0.59 × 10−8 mutations per site per generation. [DS-4]

**Bears on DS-4.** This is the one study that states both spreads, and it uses one pipeline. The two spreads are not on the
same statistic:

- the per-generation figure is the raw µgeneration over all 68 species;
- the per-year figure is the modelled µyearly_modelled, from a joint Poisson model in parental age with an intercept at birth.

The text does not state the species count behind the 120-fold figure. The paired same-footing quantities (µgeneration_modelled
and µyearly_modelled per species) are in **Supplementary Table 9**, which was not downloaded, as instructed.

### C.2 Wang & Obbard 2023 (cross-eukaryote meta-analysis)

- **Paper:** Wang Y., Obbard D.J., "Experimental estimates of germline mutation rate in eukaryotes: a phylogenetic
  meta-analysis", *Evolution Letters* 7:216. PMC10355183.1, epub 2023-06-19, doi 10.1093/evlett/qrad027.
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC10355183/. Fetched. Raw file: `life/seq/wang_obbard2023.txt`.

> a ciliate (Tetrahymena thermophila) had the lowest mutation rate, estimated at 0.01 × 10−9 per generation per base pair, while a fungus (Marasmius oreades) had the highest rate, estimated at 55.58 × 10−9—a difference of over 5,000-fold. [DS-4]

> We found a significant positive relationship with generation time (Bayesian PGLMM MCMC p < .0001; Figure 3A), such that a longer generation time predicted a higher per-site mutation rate per generation. [DS-4]

> In humans, there are around 401 cell divisions per 30-year generation in males and 31 in females (Drost & Lee, 1995; Ohno, 2019), but in mice, it is 62 per 9-month generation in males and 25 in females. [DS-4]

**Bears on DS-4.** This source gives a per-generation spread across eukaryotes (over 5,000-fold, including unicellular species)
and states no per-year spread. It cannot grade DS-4 on its own. Its positive association of per-generation rate with generation
time is quoted as stated; no slope on the log scale is given in the text.

### C.3 Human paternal and parental age (within-species)

- **Kong A. et al. 2012**, "Rate of de novo mutations, father’s age, and disease risk" (the PMC manuscript title), *Nature*
  488:471. PMC3548427.1, doi 10.1038/nature11396. Fetched. Raw file: `life/seq/kong2012.txt`.
- **Jónsson H. et al. 2017**, "Parental influence on human germline de novo mutations in 1,548 trios from Iceland", *Nature*
  549:519. PMID 28959963, doi 10.1038/nature24018. The abstract only was fetched (NCBI efetch); the paper is not in PMC. Raw
  file: `life/seq/jonsson2017_pubmed_abstract.txt`.
- **Gao Z. et al. 2019**, "Overlooked roles of DNA damage and maternal age in generating human germline mutations", *PNAS*
  116:9491. PMC6511033.1, epub 2019-04-24, doi 10.1073/pnas.1901259116. Fetched. Raw file: `life/seq/gao2019.txt`.

> with an average father’s age of 29.7, the average de novo mutation rate is 1.20×10−8 per nucleotide per generation. [DS-4] (Kong 2012)

> The number of mutations increases with father’s age (P = 3.6×10−19) with an estimated effect of 2.01 mutations per year (standard error (SE) = 0.17). [DS-4] (Kong 2012)

> the rate of paternal mutations is estimated to increase by 4.28% per year, which corresponds to doubling every 16.5 years and increasing by 8 fold in 50 years. [DS-4] (Kong 2012)

> The number of de novo mutations from mothers increases by 0.37 per year of age (95% CI 0.32-0.43), a quarter of the 1.51 per year from fathers (95% CI 1.45-1.57). [DS-4] (Jónsson 2017)

> Notably, despite the drastic increase in the ratio of male to female germ cell divisions after the onset of spermatogenesis, even young fathers contribute three times more mutations than young mothers, and this ratio barely increases with parental age. This surprising finding points to a substantial contribution of damage-induced mutations. [DS-4] (Gao 2019)

> Thus, results from pedigree and phylogenetic studies could be reconciled if humans and chimpanzees long had shorter generation times than at present. [DS-4] (Gao 2019)

**Bears on DS-4.** Within humans, the per-generation count grows with parental age in years. The data therefore support neither
a constant per-generation rate nor a constant per-year rate: there is an intercept at birth plus a slope in years (see also
Bergeron's intercept of about 0.59 × 10⁻⁸ per generation). Gao et al. argue for a substantial time-driven, damage-induced
component, which is the direction the declaration's investigator flagged as "cuts the other way". None of these sources is
cross-species.

### C.4 DS-4 structured summary

| item | as quoted |
|---|---|
| Per-generation spread | "the per-generation mutation rate varies among species by a factor of 40"; "µgeneration varies by a factor of 40 across all species" (Bergeron 2023; raw µgeneration, species means, 68 vertebrate species) |
| Per-year spread | "The estimated average µyearly_modelled varies more than 120-fold among species" (Bergeron 2023; modelled yearly rate; highest 1.96 × 10−8, lowest < 0.18 × 10−9 per site per year) |
| Other spreads (context) | "approximately 16-fold variation in yearly GMRs" (earlier separate studies, as cited by Bergeron); "a difference of over 5,000-fold" per generation across eukaryotes (Wang & Obbard 2023; no per-year figure) |
| Same footing (same species set and same statistic)? | **No.** Same study and pipeline, but the per-generation figure is raw µgeneration over all 68 species, while the per-year figure is the model-based µyearly_modelled (joint parental-age model). The species count behind the 120-fold figure is not stated in the text, and modelled rates exist for 55 species. The paired same-footing values (µgeneration_modelled, µyearly_modelled) are in Bergeron 2023 Supplementary Table 9 (not downloaded). |

The grading itself (AGREES, DISAGREES or SILENT) is left to `Life_Sciences/checks/grade_origin.py` under the declaration's
rule. This dossier records only what the sources state.
