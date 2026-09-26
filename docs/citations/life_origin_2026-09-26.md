# Sources checked on the day (R10): origin-of-life theories against CRR ingredients I1–I5, for Life_Sciences/DECLARATION_1.md Part 2 (OL-1; context for OL-2, OL-3), 2026-09-26

A note, not evidence (R8). Quotes are verbatim substrings of the saved texts. Readings are proposals for the investigator.

- **Saved texts.** Every raw text is in the session scratchpad,
  `/tmp/claude-0/-home-user-ashes-crr/77fb7a2b-ce3d-5c52-a1a6-710031fa20e9/scratchpad/life/origin/`. The per-endpoint HTTP
  log is `FETCH_LOG.txt` and the sha256 list is `../origin_sha256.txt`. The scratchpad is not committed. A reader who needs
  the texts must re-fetch them from the URLs given here.
- **Machine-readable claims.** `scratchpad/life/origin_claims.json` has one record per (theory, ingredient, source) plus
  PRED rows, with every SILENT cell listed. Its `raw_file` paths are relative to the scratchpad.
- **How the texts were made.**
  - JATS XML (Europe PMC `fullTextXML`, or NCBI efetch for PMC6517266) was flattened to plain text: title, abstract, then
    body paragraphs, titles, formulas and captions. Nested captions can appear twice.
  - PubMed abstracts are the NCBI efetch `rettype=abstract` text.
  - arXiv PDFs were converted with pypdfium2. PDF artefacts (soft hyphens, broken superscripts) are kept verbatim inside
    quotes.
  - HTML pages were tag-stripped.
- **Access limits, which shape the evidence base.**
  - Several canonical primaries could not be read on the day: Gilbert 1986, Eigen 1971, Eigen & Schuster 1977, Varela,
    Maturana & Uribe 1974, Wächtershäuser 1988/1992, Kauffman 1986 full text, Gánti's book, and the full texts of Robertson
    & Joyce 2012 and England 2013 (journal).
  - The reasons: paywalls, Cloudflare 403s at PNAS, CSH Perspectives and the Royal Society, a reCAPTCHA wall at
    pmc.ncbi.nlm.nih.gov, a 403 at pubs.aip.org, no PubMed abstract for the 1970s papers, and the book not being fetched.
  - These theories are therefore quoted from PubMed abstracts, from the arXiv version, or from open-access reviews by the
    theory's own school (Szathmáry group for hypercycle and chemoton, Hordijk & Steel, Luisi, Pross & Pascal). Each quote
    names its actual source.
  - The SEP has no "Autopoiesis" entry (HTTP 404). The SEP "Life" entry (first published 2021-11-30, substantive revision
    2026-01-23) was fetched but names none of the eleven frameworks except in passing (Wächtershäuser 1988; Eigen &
    Schuster 1977). It is not quoted.
- **How quotes were checked.** A quote was counted as verified if, after every run of whitespace was collapsed to one space,
  it was a substring of its saved text. Result: **71/71** quotes in the claims file verified. A further 18/18 short
  quoted fragments inside notes were verified against the union of saved texts. Script: `scratchpad/life/verify_quotes.py`.
- **Grading rule used here.** A cell reads CONTAINS or CONFLICTS only when a quote clearly supports it. Otherwise it reads
  SILENT. Weak readings are flagged in the note, and the investigator may downgrade them. PRED rows record each theory's
  signature testable claim and its stated empirical status. They are not graded. No novelty is claimed for CRR anywhere
  in this note.

**Source keys used in notes.** RJ12 = Robertson MP, Joyce GF (pubmed_robertson_joyce2012.txt); RW26 = Vázquez-Salazar A (rnaworld_life2026.txt); W90 = Wächtershäuser G (pubmed_wachtershauser1990.txt); MO00 = Morowitz HJ, Kostelnik JD, Yang J, Cody GD (pubmed_morowitz2000.txt); MU17 = Muchowska KB, Varma SJ, Chevallot-Beroux E, Lethuillier-Karl L, Li G, Moran J (muchowska2017_revkrebs.txt); MU19 = Muchowska KB, Varma SJ, Moran J (muchowska2019_iron.txt); K86 = Kauffman SA (pubmed_kauffman1986.txt); HS04 = Hordijk W, Steel M (pubmed_hordijk_steel2004.txt); HKS11 = Hordijk W, Kauffman SA, Steel M (hordijk_kauffman_steel2011.txt); HS18 = Hordijk W, Steel M (hordijk_steel2018_life.txt); SZ17 = Szilágyi A, Zachar I, Scheuring I, Kun Á, Könnyű B, Czárán T (szilagyi2017_rnaworld.txt); VE24 = Velten H, Pinheiro CF, Castro e Silva A (velten2024_arxiv.txt); BE05 = Biebricher CK, Eigen M (pubmed_biebricher_eigen2005.txt); TH12 = Takeuchi N, Hogeweg P (pubmed_takeuchi_hogeweg2012.txt); ZA11 = Zachar I, Fedor A, Szathmáry E (zachar2011_chemoton.txt); TR23 = Tran QP, Yi R, Fahrenbach AC (tran2023_chemoton.txt); SE01 = Segré D, Ben-Eli D, Deamer DW, Lancet D (pubmed_segre2001.txt); LA19 = Lancet D, Segrè D, Kahana A (lancet2019_lipidworld.txt); CH04 = Chen IA, Roberts RW, Szostak JW (pubmed_chen2004.txt); ZS09 = Zhu TF, Szostak JW (zhu_szostak2009.txt); SH23 = Sharma A, Czégel D, Lachmann M, Kempes CP, Walker SI, Cronin L (sharma2023_assembly.txt); SH23a = Sharma A, et al (sharma_abs.txt); MA21 = Marshall SM, et al (marshall2021_assembly_ms.txt); EN13 = England JL (england2013_arxiv.txt); EN15 = England JL (pubmed_england2015.txt); HE17 = Horowitz JM, England JL (pubmed_horowitz_england2017.txt); FR13 = Friston K (friston2013_life.txt); LU03 = Luisi PL (pubmed_luisi2003.txt); LU14 = Luisi PL (pubmed_luisi2014.txt); BL04 = Bitbol M, Luisi PL (pubmed_bitbol_luisi2004.txt); PPS13 = Pascal R, Pross A, Sutherland JD (pascal_pross_sutherland2013.txt); PR17 = Pross A, Pascal R (pross2017_beilstein.txt); PR23 = Pross A, Pascal R (pross2023_life.txt); PRE20 = Preiner M, et al (preiner2020_review.txt).

## Summary of proposed readings (theory × ingredient)

| theory | I1 | I2 | I3 | I4 | I5 |
|---|---|---|---|---|---|
| T1 RNA world | SILENT | CONTAINS | SILENT | SILENT | CONTAINS |
| T2 Metabolism-first (iron-sulfur world / reverse Krebs) | CONTAINS | SILENT | SILENT | SILENT | SILENT |
| T3 Autocatalytic sets (Kauffman; RAF, Hordijk & Steel) | CONTAINS | SILENT | SILENT | SILENT | SILENT |
| T4 Hypercycle and error threshold (Eigen; Eigen & Schuster) | CONTAINS | CONTAINS | SILENT | SILENT | SILENT |
| T5 Chemoton (Gánti) | CONTAINS | CONTAINS | CONTAINS | SILENT | SILENT |
| T6 Compartment-first / Lipid world (GARD; Szostak protocells) | CONTAINS | CONTAINS | SILENT | SILENT | SILENT |
| T7 Assembly theory (Cronin, Walker et al.) | SILENT | SILENT | CONTAINS | CONTAINS | CONTAINS |
| T8 Dissipative adaptation (England) | SILENT | SILENT | SILENT | SILENT | SILENT |
| T9 Free-energy principle applied to life (Friston 2013) | SILENT | SILENT | SILENT | SILENT | CONFLICTS |
| T10 Autopoiesis (Maturana & Varela) | CONTAINS | SILENT | SILENT | SILENT | SILENT |
| T11 Dynamic kinetic stability (Pross) | CONTAINS | CONTAINS | SILENT | SILENT | SILENT |

| ingredient | CONTAINS | CONFLICTS | SILENT |
|---|---|---|---|
| I1 | 7 | 0 | 4 |
| I2 | 5 | 0 | 6 |
| I3 | 2 | 0 | 9 |
| I4 | 1 | 0 | 10 |
| I5 | 2 | 1 | 8 |

**For the investigator.** These are counts of proposed readings, not the output of `Life_Sciences/checks/grade_origin.py`.

- Under OL-1's rule (DISCRIMINATES if at least one CONTAINS and at least one CONFLICTS), these readings would make I5 the
  only discriminating ingredient.
- That outcome rests on one reading: T9 (FEP) as CONFLICTS. Friston 2013 gives internal states content ("encoding
  posterior beliefs") and shows anticipation. It does not claim that anything is fed by a future. So the conflict is with
  I5's "no content at the cut" half only.
- It also rests on the weak T1 CONTAINS, a review's disclaimer of directedness. T7 (assembly theory) CONTAINS is stated
  directly by the source.
- If the investigator reads T9-I5 as SILENT, every ingredient is NON-DISCRIMINATING, as the declaration expected.
- I4 is CONTAINED only by assembly theory. There the assembly index is a shortest path, the analogue of the chord C* (D3),
  not the arc C (D2). No theory states the surplus S = C − C*.

---

## T1. RNA world

**Sources.**

- Robertson MP, Joyce GF. The origins of the RNA world. Cold Spring Harb Perspect Biol 4(5):a003608.
  - Version and date: 2012-05-01; PubMed abstract (PMID 20739415); full text not retrievable (see access notes).
  - URL: https://doi.org/10.1101/cshperspect.a003608.
  - Fetch: HTTP 200.
  - Raw file: `pubmed_robertson_joyce2012.txt`.
- Vázquez-Salazar A. Complex and Messy Prebiotic Chemistry: Obstacles and Opportunities for an RNA World. Life (Basel) 16(2):240.
  - Version and date: 2026-02-02; PMC12942124 (Europe PMC full-text XML).
  - URL: https://doi.org/10.3390/life16020240.
  - Fetch: HTTP 200.
  - Raw file: `rnaworld_life2026.txt`.
- Lancet D, Segrè D, Kahana A. Twenty years of 'Lipid World': a fertile partnership with David Deamer. Life (Basel) 9(4):77.
  - Version and date: 2019-09-20; PMC6958426 (Europe PMC full-text XML).
  - URL: https://doi.org/10.3390/life9040077.
  - Fetch: HTTP 200.
  - Raw file: `lancet2019_lipidworld.txt`.

**I1 (A3 with O3): a self-sustaining cycle — proposed reading: SILENT.**

- *Note:* The fetched texts posit RNA replication but do not state a self-sustaining cycle as a requirement. The cycles they name are environmental drives (wet-dry, freeze-thaw), external to the system, e.g. RW26: 'repeated wet-dry and freeze–thaw cycles acted on exposed environments'. Gilbert 1986 (the original) is paywalled; no text read.

**I2 (A6): heredity from the settled past, bounded — proposed reading: CONTAINS.**

> genetic continuity was assured by the replication of RNA [I2]

— Robertson MP, Joyce GF; `pubmed_robertson_joyce2012.txt`

- *Note:* Heredity by template replication. The bounded-strength part of I2 is the error threshold (see T4); the fetched RNA-world texts quoted here do not state it themselves.

> Within a local compartment, a heritable RNA sequence can undergo imperfect templated copying [I2]

— Vázquez-Salazar A; `rnaworld_life2026.txt`

- *Note:* Imperfect templated copying: heredity seeded by the past template, with error.

**I3 (H-L5): own events set the clock — proposed reading: SILENT.**

- *Note:* No statement found that replication events rather than clock time set the system's timescale.

**I4 (D2 vs D3): travelled path vs shortest path — proposed reading: SILENT.**

- *Note:* No path-length or minimal-path statement found.

**I5 (Prop. 7 / A8): no content at the cut; nothing fed by a future — proposed reading: CONTAINS.**

> without implying that complex mixtures are intrinsically directed toward specific outcomes [I5]

— Vázquez-Salazar A; `rnaworld_life2026.txt`

> without assuming that any specific outcome was predetermined [I5]

— Vázquez-Salazar A; `rnaworld_life2026.txt`

- *Note:* Weak: a methodological disclaimer of directedness in a 2026 review, not a core axiom of the RNA-world hypothesis. The investigator may prefer SILENT.

**Signature prediction and status [PRED].**

> There is now strong evidence indicating that an RNA World did indeed exist before DNA- and protein-based life. However, arguments regarding whether life on Earth began with RNA are more tenuous. [PRED]

— Robertson MP, Joyce GF; `pubmed_robertson_joyce2012.txt`

- *Note:* Status as stated by Robertson & Joyce 2012.

> in vitro evolution has produced RNA replicases capable of extending templates and, in recent work, sustaining adaptive evolution in RNA-only systems [PRED]

— Vázquez-Salazar A; `rnaworld_life2026.txt`

- *Note:* Experimental status, 2026 review.

> Our findings falsify the existence of an ancient RNA world [PRED]

— Lancet D, Segrè D, Kahana A; `lancet2019_lipidworld.txt`

- *Note:* A contrary claim by other authors, quoted inside Lancet et al. 2019; recorded as a sign that the status is contested, not as a verdict.

---

## T2. Metabolism-first (iron-sulfur world / reverse Krebs)

**Sources.**

- Wächtershäuser G. Evolution of the first metabolic cycles. PNAS 87(1):200-204.
  - Version and date: 1990-01; PubMed abstract (PMID 2296579).
  - URL: https://doi.org/10.1073/pnas.87.1.200.
  - Fetch: HTTP 200.
  - Raw file: `pubmed_wachtershauser1990.txt`.
- Morowitz HJ, Kostelnik JD, Yang J, Cody GD. The origin of intermediary metabolism. PNAS 97(14):7704-7708.
  - Version and date: 2000-07-05; PubMed abstract (PMID 10859347).
  - URL: https://doi.org/10.1073/pnas.110153997.
  - Fetch: HTTP 200.
  - Raw file: `pubmed_morowitz2000.txt`.
- Muchowska KB, Varma SJ, Chevallot-Beroux E, Lethuillier-Karl L, Li G, Moran J. Metals promote sequences of the reverse Krebs cycle. Nat Ecol Evol 1:1716-1721.
  - Version and date: 2017; PMC5659384 (Europe PMC full-text XML, author manuscript).
  - URL: https://doi.org/10.1038/s41559-017-0311-7.
  - Fetch: HTTP 200.
  - Raw file: `muchowska2017_revkrebs.txt`.
- Muchowska KB, Varma SJ, Moran J. Synthesis and breakdown of universal metabolic precursors promoted by iron. Nature 569:104-107.
  - Version and date: 2019; PMC6517266 (NCBI efetch PMC XML, author manuscript).
  - URL: https://doi.org/10.1038/s41586-019-1151-1.
  - Fetch: HTTP 200.
  - Raw file: `muchowska2019_iron.txt`.

**I1 (A3 with O3): a self-sustaining cycle — proposed reading: CONTAINS.**

> I here propose the hypothesis that this process is an autocatalytic cycle [I1]

— Wächtershäuser G; `pubmed_wachtershauser1990.txt`

> The cycle is catalytic for pyrite formation and autocatalytic for its own multiplication. [I1]

— Wächtershäuser G; `pubmed_wachtershauser1990.txt`

> the reductive citric acid cycle is an engine of synthesis, taking in CO(2) and synthesizing the molecules of the cycle [I1]

— Morowitz HJ, Kostelnik JD, Yang J, Cody GD; `pubmed_morowitz2000.txt`

**I2 (A6): heredity from the settled past, bounded — proposed reading: SILENT.**

- *Note:* Metabolism-first sources do not state template heredity. MU19 concedes the limit: 'Although the ability of simple reaction networks to evolve is limited in the absence of a genetic mechanism'. PRE20 names the link as open: 'A cell-like energy-coupling system could only be persistent over time if it can be inherited'. Neither states an incompatible claim, so SILENT rather than CONFLICTS.

**I3 (H-L5): own events set the clock — proposed reading: SILENT.**

- *Note:* No own-clock statement found.

**I4 (D2 vs D3): travelled path vs shortest path — proposed reading: SILENT.**

- *Note:* No path-length statement. W90's 'retrodictively constructed' refers to inferring the ancestral cycle from the extant one, not to a path metric.

**I5 (Prop. 7 / A8): no content at the cut; nothing fed by a future — proposed reading: SILENT.**

- *Note:* No statement on teleology or anticipation found.

**Signature prediction and status [PRED].**

> an autocatalytic cycle that can be retrodictively constructed from the extant reductive citric acid cycle by replacing thioesters by thioacids and by assuming that the required reducing power is obtained from the oxidative formation of pyrite (FeS2) [PRED]

— Wächtershäuser G; `pubmed_wachtershauser1990.txt`

> the postulated cycle cannot exist as a single isolated cycle but must be a member of a network of concatenated homologous cycles [PRED]

— Wächtershäuser G; `pubmed_wachtershauser1990.txt`

- *Note:* Signature claims (1990).

> Here we report non-enzymatic promotion of multiple reactions of the rTCA cycle in consecutive sequence, whereby 6 of its 11 reactions are promoted by Zn2+, Cr3+ and Fe0 in an acidic aqueous solution. [PRED]

— Muchowska KB, Varma SJ, Chevallot-Beroux E, Lethuillier-Karl L, Li G, Moran J; `muchowska2017_revkrebs.txt`

> A notable criticism by Orgel concerning the hypothesis of a prebiotic complete rTCA cycle is the difficulty for simple non-enzymatic catalysts to promote the reactions of the cycle over parasitic reactions with sufficient selectivity to achieve the theoretical 50% efficiency threshold such that autocatalysis could self-sustain or self-amplify. [PRED]

— Muchowska KB, Varma SJ, Chevallot-Beroux E, Lethuillier-Karl L, Li G, Moran J; `muchowska2017_revkrebs.txt`

- *Note:* Partial support plus the standing criticism.

> build up nine of the eleven Krebs (tricarboxylic acid, TCA) cycle intermediates, including all five universal metabolic precursors [PRED]

— Muchowska KB, Varma SJ, Moran J; `muchowska2019_iron.txt`

- *Note:* Status 2019. The source's numbers are transcribed, not recomputed (R1).

---

## T3. Autocatalytic sets (Kauffman; RAF, Hordijk & Steel)

**Sources.**

- Hordijk W, Steel M. Autocatalytic networks at the basis of life's origin and organization. Life (Basel) 8(4):62.
  - Version and date: 2018-12; PMC6315399 (Europe PMC full-text XML).
  - URL: https://doi.org/10.3390/life8040062.
  - Fetch: HTTP 200.
  - Raw file: `hordijk_steel2018_life.txt`.
- Hordijk W, Kauffman SA, Steel M. Required levels of catalysis for emergence of autocatalytic sets in models of chemical reaction systems. Int J Mol Sci 12(5):3085-3101.
  - Version and date: 2011; PMC3116177 (Europe PMC full-text XML).
  - URL: https://doi.org/10.3390/ijms12053085.
  - Fetch: HTTP 200.
  - Raw file: `hordijk_kauffman_steel2011.txt`.
- Kauffman SA. Autocatalytic sets of proteins. J Theor Biol 119(1):1-24.
  - Version and date: 1986-03-07; PubMed abstract (PMID 3713221).
  - URL: https://doi.org/10.1016/s0022-5193(86)80047-9.
  - Fetch: HTTP 200.
  - Raw file: `pubmed_kauffman1986.txt`.

**I1 (A3 with O3): a self-sustaining cycle — proposed reading: CONTAINS.**

> An autocatalytic set thus forms a catalytically closed (RA) and self-sustaining (F) reaction network (or RAF). [I1]

— Hordijk W, Steel M; `hordijk_steel2018_life.txt`

- *Note:* Catalytic closure is the cycle in network form. It is a closed loop of catalysis, not necessarily a single cyclic pathway.

> The formation of a self-sustaining autocatalytic chemical network is a necessary but not sufficient condition for the origin of life. [I1]

— Hordijk W, Kauffman SA, Steel M; `hordijk_kauffman_steel2011.txt`

> the emergence of reflexively autocatalytic sets of peptides and polypeptides may be an essentially inevitable collective property of any sufficiently complex set of polypeptides [I1]

— Kauffman SA; `pubmed_kauffman1986.txt`

**I2 (A6): heredity from the settled past, bounded — proposed reading: SILENT.**

- *Note:* No template heredity is stated. HS18 speaks of evolvability, not heredity: 'This property provides one of the necessary conditions for autocatalytic sets to be potentially evolvable'.

**I3 (H-L5): own events set the clock — proposed reading: SILENT.**

- *Note:* No own-clock statement found.

**I4 (D2 vs D3): travelled path vs shortest path — proposed reading: SILENT.**

- *Note:* No path-length statement found.

**I5 (Prop. 7 / A8): no content at the cut; nothing fed by a future — proposed reading: SILENT.**

- *Note:* No statement on teleology or anticipation found.

**Signature prediction and status [PRED].**

> a linear growth rate in the level of catalysis (with increasing length n of the largest molecules in the system) is sufficient for autocatalytic sets to arise spontaneously [PRED]

— Hordijk W, Kauffman SA, Steel M; `hordijk_kauffman_steel2011.txt`

- *Note:* Signature quantitative claim of the RAF programme.

> contrary to most of the other models, various experimental chemical examples of autocatalytic sets do exist [PRED]

— Hordijk W, Steel M; `hordijk_steel2018_life.txt`

- *Note:* Empirical status as stated by the authors.

> Recombinant DNA procedures, cloning random DNA coding sequences into expression vectors, afford a direct avenue to test the distribution of catalytic capacities in peptide space [PRED]

— Kauffman SA; `pubmed_kauffman1986.txt`

- *Note:* Kauffman's proposed test (1986).

---

## T4. Hypercycle and error threshold (Eigen; Eigen & Schuster)

**Sources.**

- Hordijk W, Steel M. Autocatalytic networks at the basis of life's origin and organization. Life (Basel) 8(4):62.
  - Version and date: 2018-12; PMC6315399 (Europe PMC full-text XML).
  - URL: https://doi.org/10.3390/life8040062.
  - Fetch: HTTP 200.
  - Raw file: `hordijk_steel2018_life.txt`.
- Szilágyi A, Zachar I, Scheuring I, Kun Á, Könnyű B, Czárán T. Ecology and evolution in the RNA world: dynamics and stability of prebiotic replicator systems. Life (Basel) 7(4):48.
  - Version and date: 2017; PMC5745561 (Europe PMC full-text XML).
  - URL: https://doi.org/10.3390/life7040048.
  - Fetch: HTTP 200.
  - Raw file: `szilagyi2017_rnaworld.txt`.
- Velten H, Pinheiro CF, Castro e Silva A. Extended error threshold mechanism in quasispecies theory via population dynamics. arXiv:2406.14516.
  - Version and date: arXiv v1, submitted 2024-06-20 (only version); PDF text extracted with pypdfium2.
  - URL: https://arxiv.org/abs/2406.14516.
  - Fetch: HTTP 200.
  - Raw file: `velten2024_arxiv.txt`.
- Biebricher CK, Eigen M. The error threshold. Virus Res 107(2):117-127.
  - Version and date: 2005-02; PubMed abstract (PMID 15649558).
  - URL: https://doi.org/10.1016/j.virusres.2004.11.002.
  - Fetch: HTTP 200.
  - Raw file: `pubmed_biebricher_eigen2005.txt`.

**I1 (A3 with O3): a self-sustaining cycle — proposed reading: CONTAINS.**

> They consist of a cyclic arrangement of catalytic polymers, each one catalyzing both its own replication as well as that of the next one in the cycle. [I1]

— Hordijk W, Steel M; `hordijk_steel2018_life.txt`

- *Note:* The primary sources (Eigen 1971; Eigen & Schuster 1977) are paywalled with no PubMed abstract. The definition is quoted from reviews.

> R3 catalyses the replication of R1 and closes the hypercycle [I1]

— Szilágyi A, Zachar I, Scheuring I, Kun Á, Könnyű B, Czárán T; `szilagyi2017_rnaworld.txt`

**I2 (A6): heredity from the settled past, bounded — proposed reading: CONTAINS.**

> The hypercycle was proposed by Eigen and Schuster [22,41,42,43] as a solution to the error threshold [1], a severe limit to the information content of primordial biological sequences. [I2]

— Szilágyi A, Zachar I, Scheuring I, Kun Á, Könnyű B, Czárán T; `szilagyi2017_rnaworld.txt`

> the inequality of the error threshold setting an upper limit to reliably replicable sequence lengths: (6)L<ln(AW/Am)μ [I2]

— Szilágyi A, Zachar I, Scheuring I, Kun Á, Könnyű B, Czárán T; `szilagyi2017_rnaworld.txt`

- *Note:* Bounded heredity. The error threshold caps the information that copying from the past can carry. This is the closest existing statement to I2's 'bounded strength'; OL-2 tests it. Equation (6) as extracted reads L < ln(A_W/A_m)/μ.

> p ≪ 1, ln(1 − p) ≈ −p one arrives at the conclusion (1) i.e., pL < ln σ. [I2]

— Velten H, Pinheiro CF, Castro e Silva A; `velten2024_arxiv.txt`

- *Note:* A secondary derivation of the Eigen condition, per replication step: pL < ln σ, equivalently Q = (1-p)^L > 1/σ. This matches OL-2's T-N form μ_c = 1 − σ^(−1/L).

**I3 (H-L5): own events set the clock — proposed reading: SILENT.**

- *Note:* The error rate is stated per replication (per copying event), which is an own-event unit. No statement was found that own events rather than clock time set the timescale, so SILENT.

**I4 (D2 vs D3): travelled path vs shortest path — proposed reading: SILENT.**

- *Note:* No path-length statement found.

**I5 (Prop. 7 / A8): no content at the cut; nothing fed by a future — proposed reading: SILENT.**

- *Note:* No statement on teleology or anticipation found.

**Signature prediction and status [PRED].**

> as far as we are aware, there are no published experimental chemical examples of hypercycles [PRED]

— Hordijk W, Steel M; `hordijk_steel2018_life.txt`

- *Note:* Empirical status (2018).

> the hypercycle, is probably the worst performer in almost all of these respects [PRED]

— Szilágyi A, Zachar I, Scheuring I, Kun Á, Könnyű B, Czárán T; `szilagyi2017_rnaworld.txt`

- *Note:* A theoretical assessment (2017).

> A consequence of quasispecies is the existence of an error threshold for selective competence. [PRED]

— Biebricher CK, Eigen M; `pubmed_biebricher_eigen2005.txt`

- *Note:* The error threshold is the signature prediction. Its empirical status in RNA viruses is covered by Biebricher & Eigen 2005 (abstract only).

---

## T5. Chemoton (Gánti)

**Sources.**

- Zachar I, Fedor A, Szathmáry E. Two different template replicators coexisting in the same protocell: stochastic simulation of an extended chemoton model. PLoS One 6(7):e21380.
  - Version and date: 2011; PMC3139576 (Europe PMC full-text XML).
  - URL: https://doi.org/10.1371/journal.pone.0021380.
  - Fetch: HTTP 200.
  - Raw file: `zachar2011_chemoton.txt`.
- Tran QP, Yi R, Fahrenbach AC. Towards a prebiotic chemoton - nucleotide precursor synthesis driven by the autocatalytic formose reaction. Chem Sci 14:9589.
  - Version and date: 2023-09-13; PMC10498504 (Europe PMC full-text XML).
  - URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC10498504/.
  - Fetch: HTTP 200.
  - Raw file: `tran2023_chemoton.txt`.
- Hordijk W, Steel M. Autocatalytic networks at the basis of life's origin and organization. Life (Basel) 8(4):62.
  - Version and date: 2018-12; PMC6315399 (Europe PMC full-text XML).
  - URL: https://doi.org/10.3390/life8040062.
  - Fetch: HTTP 200.
  - Raw file: `hordijk_steel2018_life.txt`.

**I1 (A3 with O3): a self-sustaining cycle — proposed reading: CONTAINS.**

> It consists of three autocatalytic subsystems: a metabolic subsystem (self-reproducing chemical cycle), an informational subsystem (template polymerization cycle) and a boundary subsystem surrounding the former two (membrane). [I1]

— Zachar I, Fedor A, Szathmáry E; `zachar2011_chemoton.txt`

- *Note:* Gánti's book (2003) was not fetched. The three subsystems are quoted from Zachar et al. 2011.

> At the heart of the chemoton is a self-sustaining autocatalytic system capable of providing the substrates for the other two required autocatalytic cycles [I1]

— Tran QP, Yi R, Fahrenbach AC; `tran2023_chemoton.txt`

**I2 (A6): heredity from the settled past, bounded — proposed reading: CONTAINS.**

> By the introduction of an information carrier template molecule, at least limited heredity [10] can be achieved: when the chemoton reaches a certain size, it splits into daughter spheres, thus it is able to pass on changes in the template molecules to offspring. [I2]

— Zachar I, Fedor A, Szathmáry E; `zachar2011_chemoton.txt`

- *Note:* Explicitly 'limited heredity'.

**I3 (H-L5): own events set the clock — proposed reading: CONTAINS.**

> The chemical reactions of the three subsystems are coupled stoichiometrically, which coordinates the growth and division of the cell [I3]

— Zachar I, Fedor A, Szathmáry E; `zachar2011_chemoton.txt`

> when the chemoton reaches a certain size, it splits into daughter spheres [I3]

— Zachar I, Fedor A, Szathmáry E; `zachar2011_chemoton.txt`

- *Note:* Reading: division is triggered by the own state of the system (size, reached through stoichiometric coupling), not by an external clock. This is weaker than H-L5's arc-versus-clock claim. The investigator may prefer SILENT.

**I4 (D2 vs D3): travelled path vs shortest path — proposed reading: SILENT.**

- *Note:* No path-length statement found.

**I5 (Prop. 7 / A8): no content at the cut; nothing fed by a future — proposed reading: SILENT.**

- *Note:* No statement on teleology or anticipation found in the fetched texts. Ginsburg 2015, titled “The teleological transitions in evolution: A Gántian view” (PMID 25890032), was found by title only in a PubMed search and not read.

**Signature prediction and status [PRED].**

> there appear to be no published experimental chemical examples of chemotons [PRED]

— Hordijk W, Steel M; `hordijk_steel2018_life.txt`

- *Note:* Empirical status (2018).

> The synthesis of nucleotide precursors fuelled by the formose reaction, one of the most plausible forms of autocatalysis on the early Earth, is demonstrated, and the relevance to the chemoton model is discussed. [PRED]

— Tran QP, Yi R, Fahrenbach AC; `tran2023_chemoton.txt`

- *Note:* Partial experimental step (2023).

---

## T6. Compartment-first / Lipid world (GARD; Szostak protocells)

**Sources.**

- Zhu TF, Szostak JW. Coupled growth and division of model protocell membranes. J Am Chem Soc 131(15):5705-5713.
  - Version and date: 2009; PMC2669828 (Europe PMC full-text XML, author manuscript).
  - URL: https://doi.org/10.1021/ja900919c.
  - Fetch: HTTP 200.
  - Raw file: `zhu_szostak2009.txt`.
- Lancet D, Segrè D, Kahana A. Twenty years of 'Lipid World': a fertile partnership with David Deamer. Life (Basel) 9(4):77.
  - Version and date: 2019-09-20; PMC6958426 (Europe PMC full-text XML).
  - URL: https://doi.org/10.3390/life9040077.
  - Fetch: HTTP 200.
  - Raw file: `lancet2019_lipidworld.txt`.
- Chen IA, Roberts RW, Szostak JW. The emergence of competition between model protocells. Science 305(5689):1474-1476.
  - Version and date: 2004-09-03; PubMed abstract (PMID 15353806).
  - URL: https://doi.org/10.1126/science.1100757.
  - Fetch: HTTP 200.
  - Raw file: `pubmed_chen2004.txt`.
- Segré D, Ben-Eli D, Deamer DW, Lancet D. The lipid world. Orig Life Evol Biosph 31(1-2):119-145.
  - Version and date: 2001; PubMed abstract (PMID 11296516).
  - URL: https://doi.org/10.1023/a:1006746807104.
  - Fetch: HTTP 200.
  - Raw file: `pubmed_segre2001.txt`.

**I1 (A3 with O3): a self-sustaining cycle — proposed reading: CONTAINS.**

> We show that model protocells can proceed through multiple cycles of reproduction. [I1]

— Zhu TF, Szostak JW; `zhu_szostak2009.txt`

> It is the ensuing non-trivial concentration-preserving (homeostatic) growth, followed by random fission, that marks true lipid reproduction [I1]

— Lancet D, Segrè D, Kahana A; `lancet2019_lipidworld.txt`

- *Note:* A growth–fission cycle.

**I2 (A6): heredity from the settled past, bounded — proposed reading: CONTAINS.**

> lipid mixed assemblies that grow and split can transmit molecular information from one generation to another [I2]

— Lancet D, Segrè D, Kahana A; `lancet2019_lipidworld.txt`

- *Note:* Compositional inheritance. On its bound: 'GARD was technically contested in [48] due to poor evolvability' (same source).

> Encapsulated RNA molecules, representing a primitive genome, are distributed to the daughter vesicles. [I2]

— Zhu TF, Szostak JW; `zhu_szostak2009.txt`

**I3 (H-L5): own events set the clock — proposed reading: SILENT.**

- *Note:* In ZS09 division is set off by an external event (gentle shear): 'Modest shear forces are then sufficient to cause the thread-like vesicles to divide'. The theory states no own-clock claim, so SILENT. The investigator may note that this division cut is environmental (relevant to OL-3).

**I4 (D2 vs D3): travelled path vs shortest path — proposed reading: SILENT.**

- *Note:* No path-length statement found.

**I5 (Prop. 7 / A8): no content at the cut; nothing fed by a future — proposed reading: SILENT.**

- *Note:* No statement on teleology or anticipation found.

**Signature prediction and status [PRED].**

> more efficient RNA replication could cause faster cell growth, leading to the emergence of Darwinian evolution at the cellular level [PRED]

— Chen IA, Roberts RW, Szostak JW; `pubmed_chen2004.txt`

> Twenty years later, experimental verification is still hard to attain. [PRED]

— Lancet D, Segrè D, Kahana A; `lancet2019_lipidworld.txt`

- *Note:* Status of compositional inheritance (GARD), as stated by its authors.

> these concepts provide a theoretical framework, and suggest experimental tests for a Lipid World model for the origin of life [PRED]

— Segré D, Ben-Eli D, Deamer DW, Lancet D; `pubmed_segre2001.txt`

---

## T7. Assembly theory (Cronin, Walker et al.)

**Sources.**

- Sharma A, Czégel D, Lachmann M, Kempes CP, Walker SI, Cronin L. Assembly theory explains and quantifies selection and evolution. Nature 622:321-328.
  - Version and date: 2023; PMC10567559 (Europe PMC full-text XML); arXiv:2206.02279 v3 (2023-03-12).
  - URL: https://doi.org/10.1038/s41586-023-06600-9.
  - Fetch: HTTP 200.
  - Raw file: `sharma2023_assembly.txt`.
- Sharma A, et al. Assembly theory explains and quantifies selection and evolution. arXiv:2206.02279 abstract page.
  - Version and date: arXiv v3, last revised 2023-03-12 (v1 2022-06-05).
  - URL: https://arxiv.org/abs/2206.02279.
  - Fetch: HTTP 200.
  - Raw file: `sharma_abs.txt`.
- Marshall SM, et al. Identifying molecules as biosignatures with assembly theory and mass spectrometry. Nat Commun 12:3033.
  - Version and date: 2021; PMC8144626 (Europe PMC full-text XML).
  - URL: https://doi.org/10.1038/s41467-021-23258-x.
  - Fetch: HTTP 200.
  - Raw file: `marshall2021_assembly_ms.txt`.

**I1 (A3 with O3): a self-sustaining cycle — proposed reading: SILENT.**

- *Note:* AT does not require a cycle; no statement found.

**I2 (A6): heredity from the settled past, bounded — proposed reading: SILENT.**

- *Note:* No heredity statement as such. Related: 'the minimal number of operations necessary to construct an observed object based on objects that could have existed in its past' (SH23) is construction from past objects, not templated inheritance. Left SILENT.

**I3 (H-L5): own events set the clock — proposed reading: CONTAINS.**

> It introduces an ‘assembly time’ that ticks at each object being made: assembly physics includes an explicit arrow of time intrinsic to the structure of objects. [I3]

— Sharma A, Czégel D, Lachmann M, Kempes CP, Walker SI, Cronin L; `sharma2023_assembly.txt`

- *Note:* An event-counted clock ('ticks at each object being made'). SH23 also defines clock-rate timescales τd and τp, so AT uses both kinds of time.

**I4 (D2 vs D3): travelled path vs shortest path — proposed reading: CONTAINS.**

> For each object, the most important feature is the assembly index ai, which corresponds to the shortest number of steps required to generate the object from basic building blocks. [I4]

— Sharma A, Czégel D, Lachmann M, Kempes CP, Walker SI, Cronin L; `sharma2023_assembly.txt`

> This can be quantified as the length of the shortest assembly pathway that can generate the object (Fig. 1). [I4]

— Sharma A, Czégel D, Lachmann M, Kempes CP, Walker SI, Cronin L; `sharma2023_assembly.txt`

- *Note:* The assembly index is a minimal path: the analogue of the chord C* (D3), not the arc C (D2). AT contrasts it with the paths actually taken, e.g. 'a vast separation in scales separating the number of objects that could have been explored versus those that are actually constructed following a particular path'. AT has no surplus S = C − C* as a quantity. That is a reading, not a finding (declaration OL-1).

> defined as the minimal number of steps needed to construct the object from basic building blocks [I4]

— Sharma A, et al; `sharma_abs.txt`

- *Note:* arXiv abstract wording (v3).

**I5 (Prop. 7 / A8): no content at the cut; nothing fed by a future — proposed reading: CONTAINS.**

> Historical contingency is introduced by assuming that only the knowledge or constraints built on a given path can be used in the future [I5]

— Sharma A, Czégel D, Lachmann M, Kempes CP, Walker SI, Cronin L; `sharma2023_assembly.txt`

- *Note:* Only the past path feeds the future.

> To understand how open-ended forms can emerge in a forward-process from physics that does not include their design [I5]

— Sharma A, et al; `sharma_abs.txt`

- *Note:* No design: no teleology.

**Signature prediction and status [PRED].**

> This suggests that selectivity in an unknown physical process can be explained by experimentally detecting the number of objects, their assembly index and copy number as a function of time. [PRED]

— Sharma A, Czégel D, Lachmann M, Kempes CP, Walker SI, Cronin L; `sharma2023_assembly.txt`

> only biologically produced samples produce MA above a certain threshold [PRED]

— Marshall SM, et al; `marshall2021_assembly_ms.txt`

> Importantly this measurement does not imply that samples with a maximum MA below 15 are non-living [PRED]

— Marshall SM, et al; `marshall2021_assembly_ms.txt`

- *Note:* The signature biosignature prediction (a molecular assembly threshold of about 15, per the source). Published critiques exist but were not fetched here.

---

## T8. Dissipative adaptation (England)

**Sources.**

- England JL. Statistical physics of self-replication. J Chem Phys 139:121923 (2013).
  - Version and date: arXiv:1209.1179 v1 (2012-09-06, only version); journal version 2013-08-21 not retrievable (pubs.aip.org 403); PDF text extracted with pypdfium2.
  - URL: https://arxiv.org/abs/1209.1179.
  - Fetch: HTTP 200.
  - Raw file: `england2013_arxiv.txt`.
- England JL. Dissipative adaptation in driven self-assembly. Nat Nanotechnol 10(11):919-923.
  - Version and date: 2015-11; PubMed abstract (PMID 26530021).
  - URL: https://doi.org/10.1038/nnano.2015.250.
  - Fetch: HTTP 200.
  - Raw file: `pubmed_england2015.txt`.
- Horowitz JM, England JL. Spontaneous fine-tuning to environment in many-species chemical reaction networks. PNAS 114(29):7565-7570.
  - Version and date: 2017-07-18; PubMed abstract (PMID 28674005).
  - URL: https://doi.org/10.1073/pnas.1700617114.
  - Fetch: HTTP 200.
  - Raw file: `pubmed_horowitz_england2017.txt`.

**I1 (A3 with O3): a self-sustaining cycle — proposed reading: SILENT.**

- *Note:* Self-replication is assumed, not a self-sustaining cycle required for origin. The 'division cycle' appears only as the E. coli example.

**I2 (A6): heredity from the settled past, bounded — proposed reading: SILENT.**

- *Note:* No heredity statement; 'durability' is the replicator's lifetime, not inheritance.

**I3 (H-L5): own events set the clock — proposed reading: SILENT.**

- *Note:* The heat bound is written over one division interval: 'it again after a time interval of τdiv, the typical duration of a single round of growth and cell division' (EN13). This is the analyst's choice of window, not a claim that own events set the clock, so SILENT.

**I4 (D2 vs D3): travelled path vs shortest path — proposed reading: SILENT.**

- *Note:* No path-length statement found.

**I5 (Prop. 7 / A8): no content at the cut; nothing fed by a future — proposed reading: SILENT.**

- *Note:* No statement on teleology or anticipation found. Adaptation is attributed to the history of work absorption (EN15, HE17) with no forward-looking term. Left SILENT because this is not stated as a principle.

**Signature prediction and status [PRED].**

> we will derive a lower bound on the heat output of a self-replicator in terms of its size, growth rate, entropy, and durability [PRED]

— England JL; `england2013_arxiv.txt`

> these calculations also establish that the E. coli bacterium produces an amount of heat less than three times as large as the absolute physical lower bound dictated by its growth rate, internal entropy production, and durability [PRED]

— England JL; `england2013_arxiv.txt`

> I propose that they imply a general thermodynamic mechanism for self-organization via dissipation of absorbed work that may be applicable in a broad class of driven many-body systems [PRED]

— England JL; `pubmed_england2015.txt`

> We find that the long-time dynamics of such systems are biased toward states that exhibit a fine-tuned extremization of environmental forcing. [PRED]

— Horowitz JM, England JL; `pubmed_horowitz_england2017.txt`

- *Note:* An in-silico result (2017).

---

## T9. Free-energy principle applied to life (Friston 2013)

**Sources.**

- Friston K. Life as we know it. J R Soc Interface 10(86):20130475.
  - Version and date: 2013; PMC3730701 (Europe PMC full-text XML).
  - URL: https://doi.org/10.1098/rsif.2013.0475.
  - Fetch: HTTP 200.
  - Raw file: `friston2013_life.txt`.

**I1 (A3 with O3): a self-sustaining cycle — proposed reading: SILENT.**

- *Note:* The paper names a circular causality ('reminiscent of the action–perception cycle') and a random global attractor, but not a self-sustaining cycle as an origin requirement. SILENT.

**I2 (A6): heredity from the settled past, bounded — proposed reading: SILENT.**

- *Note:* No heredity statement.

**I3 (H-L5): own events set the clock — proposed reading: SILENT.**

- *Note:* No own-clock statement. The analysis uses ergodic time averages over clock time.

**I4 (D2 vs D3): travelled path vs shortest path — proposed reading: SILENT.**

- *Note:* No path-length statement found.

**I5 (Prop. 7 / A8): no content at the cut; nothing fed by a future — proposed reading: CONFLICTS.**

> the internal states will appear to have solved the problem of Bayesian inference by encoding posterior beliefs about hidden (external) states [I5]

— Friston K; `friston2013_life.txt`

> The internal dynamics that predict this event appear to emerge in their fluctuations before the event itself (figure 4)—as would be anticipated if internal events are modelling external events. [I5]

— Friston K; `friston2013_life.txt`

- *Note:* Reading: the internal states carry content (beliefs about external states) and anticipate events. This sits against I5's 'the cut has no content'. No causation from the future is claimed: prediction is built from past data. So the conflict is with the no-content half of I5, not the no-future half. The investigator should confirm.

**Signature prediction and status [PRED].**

> any system that exists will appear to minimize free energy and therefore engage in active inference [PRED]

— Friston K; `friston2013_life.txt`

> The final section uses simulations to provide a proof of principle [PRED]

— Friston K; `friston2013_life.txt`

- *Note:* Status: the paper's evidence is a simulation (proof of principle).

---

## T10. Autopoiesis (Maturana & Varela)

**Sources.**

- Luisi PL. The minimal autopoietic unit. Orig Life Evol Biosph 44(4):335-338.
  - Version and date: 2014-12; PubMed abstract (PMID 25585801).
  - URL: https://doi.org/10.1007/s11084-014-9388-z.
  - Fetch: HTTP 200.
  - Raw file: `pubmed_luisi2014.txt`.
- Hordijk W, Steel M. Autocatalytic networks at the basis of life's origin and organization. Life (Basel) 8(4):62.
  - Version and date: 2018-12; PMC6315399 (Europe PMC full-text XML).
  - URL: https://doi.org/10.3390/life8040062.
  - Fetch: HTTP 200.
  - Raw file: `hordijk_steel2018_life.txt`.
- Luisi PL. Autopoiesis: a review and a reappraisal. Naturwissenschaften 90(2):49-59.
  - Version and date: 2003-02; PubMed abstract (PMID 12590297).
  - URL: https://doi.org/10.1007/s00114-002-0389-9.
  - Fetch: HTTP 200.
  - Raw file: `pubmed_luisi2003.txt`.

**I1 (A3 with O3): a self-sustaining cycle — proposed reading: CONTAINS.**

> a living cell is an open system capable of self-maintenance, due to a process of internal self-regeneration of the components, all within a boundary which is itself product from within [I1]

— Luisi PL; `pubmed_luisi2014.txt`

- *Note:* Reading: closed self-production is the cycle. Luisi paraphrases Varela et al. 1974, which is paywalled (linkinghub/ScienceDirect 403) with no PubMed abstract. Scope caveat from LU03: autopoiesis is 'not a theory about the origin of life'.

**I2 (A6): heredity from the settled past, bounded — proposed reading: SILENT.**

- *Note:* LU14: 'In this definition (or better operational description) there is no mention of DNA or genetic code.' This is silence about genetic heredity, not a denial of continuity, so SILENT rather than CONFLICTS.

**I3 (H-L5): own events set the clock — proposed reading: SILENT.**

- *Note:* No own-clock statement found.

**I4 (D2 vs D3): travelled path vs shortest path — proposed reading: SILENT.**

- *Note:* No path-length statement found.

**I5 (Prop. 7 / A8): no content at the cut; nothing fed by a future — proposed reading: SILENT.**

- *Note:* No teleology statement found. BL04 frames cognition 'in contradistinction to the representationalistic point of view', which could bear on I5's 'no content'. Left SILENT because it is not a claim about the future or about empty content.

**Signature prediction and status [PRED].**

> there are preliminary experimental data supporting the possible existence of this primitive form of cell activity [PRED]

— Luisi PL; `pubmed_luisi2014.txt`

> some simple autopoietic chemical systems have been constructed experimentally [PRED]

— Hordijk W, Steel M; `hordijk_steel2018_life.txt`

> not an abstract theory, not a concept of artificial life, not a theory about the origin of life-but rather a pragmatic blueprint of life based on cellular life [PRED]

— Luisi PL; `pubmed_luisi2003.txt`

- *Note:* Scope: by Luisi's reading, autopoiesis makes no origin-of-life prediction.

---

## T11. Dynamic kinetic stability (Pross)

**Sources.**

- Pascal R, Pross A, Sutherland JD. Towards an evolutionary theory of the origin of life based on kinetics and thermodynamics. Open Biol 3:130156.
  - Version and date: 2013; PMC3843823 (Europe PMC full-text XML).
  - URL: https://doi.org/10.1098/rsob.130156.
  - Fetch: HTTP 200.
  - Raw file: `pascal_pross_sutherland2013.txt`.
- Pross A, Pascal R. How and why kinetics, thermodynamics, and chemistry induce the logic of biological evolution. Beilstein J Org Chem 13:665-674.
  - Version and date: 2017; PMC5389199 (Europe PMC full-text XML).
  - URL: https://doi.org/10.3762/bjoc.13.66.
  - Fetch: HTTP 200.
  - Raw file: `pross2017_beilstein.txt`.
- Pross A, Pascal R. On the Emergence of Autonomous Chemical Systems through Dissipation Kinetics. Life (Basel) 13(11):2171.
  - Version and date: 2023-11-06; PMC10672272 (Europe PMC full-text XML).
  - URL: https://doi.org/10.3390/life13112171.
  - Fetch: HTTP 200.
  - Raw file: `pross2023_life.txt`.

**I1 (A3 with O3): a self-sustaining cycle — proposed reading: CONTAINS.**

> This means that any autocatalytic cycle or other replication process must proceed unidirectionally to display DKS [3]. [I1]

— Pascal R, Pross A, Sutherland JD; `pascal_pross_sutherland2013.txt`

> the process can be represented as a reaction cycle in which the autocatalytic species is recycled and reproduced (Scheme 3) [I1]

— Pascal R, Pross A, Sutherland JD; `pascal_pross_sutherland2013.txt`

**I2 (A6): heredity from the settled past, bounded — proposed reading: CONTAINS.**

> The storage of genetic information as a sequence in a polymer associated with template replication through base-pairing constitutes an efficient system to ensure evolvability. [I2]

— Pross A, Pascal R; `pross2017_beilstein.txt`

- *Note:* Weak: DKS itself is defined on persistent replicators; template heredity enters as an efficient means, not as part of the definition.

**I3 (H-L5): own events set the clock — proposed reading: SILENT.**

- *Note:* Candidate, not graded: PR23 ties irreversibility to the ratio of the own generation time of the system to the transition-state lifetime: 'the constraint on the kinetic barrier ΔGr≠ is rather related to time (the ratio of the duration of two events, namely transition state lifetime and reproduction timescale) than to thermodynamics'. Generation time is still measured in clock time ('generation times spanning from 1 s to 1 century'), so SILENT under the conservative rule.

**I4 (D2 vs D3): travelled path vs shortest path — proposed reading: SILENT.**

- *Note:* No path-length statement found.

**I5 (Prop. 7 / A8): no content at the cut; nothing fed by a future — proposed reading: SILENT.**

- *Note:* Candidate, not graded: PPS13 states contingency ('evolution towards subsequent states cannot generally be predicted by any extrapolation of the present behaviour'). That concerns unpredictability, not future causation, so SILENT.

**Signature prediction and status [PRED].**

> Another direction of potential interest could be to seek the emergence of autocatalytic cycles in combinatorial mixtures of prebiotically plausible reactants and activated reagents or energy sources. [PRED]

— Pascal R, Pross A, Sutherland JD; `pascal_pross_sutherland2013.txt`

> A universal scale of DKS seems therefore unattainable from a kinetic point of view [PRED]

— Pascal R, Pross A, Sutherland JD; `pascal_pross_sutherland2013.txt`

- *Note:* The proposed research direction, and the stated limit on quantifying DKS.

> Numerically this treatment leads to kinetic barriers ΔGr≠ exceeding values of 73 and 127 kJ mol−1 at 25 °C considering generation times spanning from 1 s to 1 century, respectively. [PRED]

— Pross A, Pascal R; `pross2023_life.txt`

- *Note:* A semi-quantitative model prediction (the source's numbers, transcribed).

---

## REV. Preiner et al. 2020 review

**Sources.**

- Preiner M, et al. The future of origin of life research: bridging decades-old divisions. Life (Basel) 10(3):20.
  - Version and date: 2020-02-26; PMC7151616 (Europe PMC full-text XML).
  - URL: https://doi.org/10.3390/life10030020.
  - Fetch: HTTP 200.
  - Raw file: `preiner2020_review.txt`.

**Signature prediction and status [PRED].**

> even though classical approaches and theories—e.g., bottom-up and top-down, RNA world vs. metabolism-first—have been prevalent in origin of life research, they are ceasing to be mutually exclusive [PRED]

— Preiner M, et al; `preiner2020_review.txt`

- *Note:* A comparative review; context for OL-1's expectation that CRR restates what the theories share.

---

## Checks and limits

- **Quote check.** 71 quotes. Each was verified as a whitespace-collapsed substring of its saved text, 71/71. The script
  `verify_quotes.py` in `scratchpad/life/` prints the counts and the per-ingredient tallies.
- **Primaries not read, and what that means.**
  - Gilbert 1986 (Nature 319:618; nature.com preview only). Eigen 1971 (Naturwissenschaften 58:465, DOI
    10.1007/BF00623322). Eigen & Schuster 1977 (DOI 10.1007/BF00450633). Varela, Maturana & Uribe 1974 (BioSystems
    5:187–196, per Crossref). Wächtershäuser 1988 (Microbiol Rev 52:452) and 1992 (Prog Biophys Mol Biol). Kauffman 1986
    (abstract only). Gánti 2003 (book). England 2013 journal version (J Chem Phys 139:121923, published 2013-08-21 per
    Crossref; the arXiv v1 was read instead).
  - Readings for T1, T4, T5 and T10 therefore rest on reviews or abstracts. A SILENT cell there means "silent in the
    fetched texts", not "silent in the theory".
- **Numbers.** Numbers inside quotes are the sources' own, transcribed. None was recomputed here, and none may enter a
  ledger row (R1).

