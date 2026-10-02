# PRE-PHOENIX INTERPRETIVE AUDIT — NO VERDICTS ALTERED; Embers read only at commit 7082f23

**Embers cross-audit (reader notes).** These notes are not evidence (R8). They change no verdict in either repository.
They follow the declaration's method, step 5 ([Ashes] `Pre_Phoenix_Audit/DECLARATION.md:60-65`). The requested questions
are in prompt-log entry 260, §6 ([Ashes] `notebook/PROMPT_LOG.md:2047-2068`). The coordinator's addition asks for items
(a)–(d); they are answered in §5.4, §5.5, §6.3 and §6.4.

**Conventions.**
- Path prefixes:
  - **[Embers]** is `/home/user/embers_crr`, a read-only clone at 7082f23.
  - **[Ashes]** is `/home/user/ashes_crr` as it stands on 2026-10-02.
- Ledger rows are cited by id and repository, e.g. "Embers ledger row H1CARD-1", "Ashes ledger row CARD-1".
- Each repository's verdicts are quoted in its own words. No Embers verdict is restated as applying to an Ashes row, and no
  Ashes verdict as applying to an Embers row.
- **Auditor's count (derived)** and **auditor's reading** mark anything I computed or interpreted myself. The method is
  stated each time.
- **Dates in Embers.** `git log` in the clone returns a single commit:
  - `7082f23 2026-09-28 23:52:33 +0000` (`git log --oneline | wc -l` → 1);
  - the clone is shallow, so per-commit dates are not available.
  
  Every other Embers date comes from the times Embers records itself, in `notebook/PROMPT_LOG.md`, `notebook/AGENT_LOG.md`
  and the ANCHOR/fetch logs.
- **Edit scope.** Nothing in Embers was modified or executed. Only this file was written in Ashes.

**Corrections after independent verification (2026-10-02; the text below is otherwise as written).**
1. **The record is not limited to 7082f23.** That is the HEAD of Embers `main` only. Embers' work continued on the unmerged
   branch `claude/eager-allen-5rjiem`, now at de6c05a, 72 commits later. That branch is read in
   `notes/EMBERS_ADDENDUM_de6c05a.md`. Statements below about stk2 being "pending", about 12 ledger rows, and about "four
   scored real-data studies" are as of 7082f23. At de6c05a:
   - STK2-1 is VOID;
   - the ledger has 22 rows;
   - four of six real-data studies have no hypothesis verdict.
2. **§6.4, "same, reached on disjoint system sets"** (A6 accumulation; antipode against extremum). The systems are disjoint,
   but Embers had adopted both Ashes lessons before its batteries ([Embers] `CRR_Ashes/README.md:208-212`), and rows were
   declared expecting WRONG ([Embers] `retro/DECLARATION_R2.md:157`). Read these as replicated on new systems, primed, not
   independent.
3. **§5.1, "Signed tags".** Embers' `docs/keys/tag_signer_ssh.pub` is 0 bytes, already at 7082f23 (Embers AGENT_LOG 87 on the
   branch).
4. **§5.4 item 3.** Ashes' SEC instrument gates were registered in SEC6 and SEC6R, computed on held-out units at scoring, and
   applied post hoc to SCL3, SEC3, SEC4 and SEC5.
5. **§5.5 item 2.**
   - "Chosen by a channel-count rule" should read "≥ 2 physical channels and an expected asymmetric waveform (odd
     harmonics)" ([Embers] `notebook/AGENT_LOG.md:33`).
   - Two of the plumbing risks (H1GAIT's side labels, p5156's format) were flagged before the freeze.
   - The phrase "no peek before the anchor" is a paraphrase, not a quotation.

---

## 0 Summary

1. **What Embers is.** Embers is "a restricted, unvalidated rotor extension of `ashes_crr`" ([Embers] `CLAUDE.md:6`). It
   was built in about 45 hours: auditor's count (derived), from prompt 1 at "no later than 2026-09-27T02:53:43Z"
   ([Embers] `notebook/PROMPT_LOG.md:22`) to commit 7082f23 at 2026-09-28T23:52:33Z.
   - It pins Ashes at 0edbc37 for theory and rules ([Embers] `README.md:68-69`; `docs/SOURCES.md:9-10`, as numbered in that
     file).
   - It adds equations of motion, a Fisher-arc first-passage cut, a seed separate from the phase, and three hypotheses
     (H1/H2/H3). Ashes' CRR.md says it has none of the first: "It has no equations of motion" ([Ashes] `theory/CRR.md:31-32`).
2. **Ledger.** 12 Embers ledger rows: auditor's count (derived), from `ledger/LEDGER.md:24-37`. Four of them are primary
   hypothesis rows:
   - H1CARD-1 "FAIL";
   - H1RESP-1 and H1GAIT-1 "NOT DECIDABLE";
   - STK1-1 "**VOID**".

   No PASS of any level.
3. **Inheritance.**
   - **Rules:** a verbatim snapshot of Ashes CLAUDE.md, enforced by script.
   - **Code:** the synthesis harness, "ported verbatim in logic".
   - **Data status:** Ashes SEEN, copied verbatim.
   - **Verdicts:** Embers treated the Ashes verdicts as settled lessons and priors ([Embers] `CRR_Ashes/README.md:202-222`;
     `docs/DOMAIN_PORTFOLIO.md:166-182`). Most of those lessons match what the Ashes lineage notes conclude. They diverge on
     the cut (A3/H-CUT), and partly on how far a single FAIL propagates (H-L5, H-T1, RLAW).
4. **Which failures bear on baseline CRR.** None of the Embers ledger failures bears on a CRR.md v3.1 hypothesis as stated:
   - H1CARD-1 tests the rotor extension's H1 (Fisher-arc antipode against angular antipode), not H-CUT (antipode against
     extremum).
   - The two NOT DECIDABLE rows and the VOID row are bridge or infrastructure outcomes.

   Embers' *synthetic* battery WRONG rows do bear on baseline A6. They fall where a domain accumulates or needs several
   timescales, which CRR.md itself excludes ("never an accumulated count", [Ashes] `theory/CRR.md:151-153`). Maths_Repair
   MR-003 is a scope note on baseline P3's formula.
5. **Machinery.**
   - **Where Embers is stricter:**
     - a Bitcoin-verified anchor before every data step, including the retrodiction declarations;
     - blame tables and honest priors fixed before data;
     - Bonferroni correction within a same-day batch;
     - calibration-only decidability, settled on training units before held-out units are opened.
   - **Where it is no better:**
     - tags were not pushed;
     - there is no second person;
     - metadata-only data scouting consumed held-out records without a verdict.

   **It has no explicitly exploratory environment.** Exploration was synthetic (gates, retrodiction batteries) and fast.
   There was essentially no exploratory contact with real data before confirmatory hashing.
6. **Question 10 for Embers.** Prompt 1 to the first held-out data step took about 3 h 38 min: auditor's count (derived),
   02:53:43Z → 06:32Z ([Embers] `notebook/AGENT_LOG.md:43`).
   - Three of the four scored real-data studies ended without a hypothesis verdict for data-plumbing reasons that
     metadata-only scouting could not see (auditor's count, derived: H1GAIT, H1RESP, STK1).
   - The one FAIL (H1CARD) was run on a carrier chosen by an admissibility rule, with a recorded prior of "FAIL
     (P ≈ 0.80)" ([Embers] `prereg/h1card/PREREG.md:194`).

   This is the same pattern the Ashes process notes record: request-to-hash in minutes, and infrastructure consuming
   held-out data ([Ashes] `Pre_Phoenix_Audit/notes/PROCESS.md:628-637`).

---

## 1 Embers at a glance

| item | value | source |
|---|---|---|
| Commit read | 7082f23, 2026-09-28T23:52:33Z, "Restore the archive manifest; bring stale status lines up to date (issue #7)". The only commit in the shallow clone | `git log` in [Embers] |
| Origin | An uploaded archive, `CRR_Embers_review_draft (1).zip`, extracted after `sha256sum -c MANIFEST.sha256` passed on all 18 files | [Embers] `notebook/AGENT_LOG.md:15` (entry 2) |
| Pinned Ashes source | `ashes_crr` at 0edbc37f2c96… | [Embers] `README.md:68`; `docs/EPISTEMIC_GUARDRAILS.md:7-9` |
| First prompt | "received no later than 2026-09-27T02:53:43Z" | [Embers] `notebook/PROMPT_LOG.md:22` |
| Last prompt logged | entry 24, "no later than 2026-09-28T21:12:38Z" | [Embers] `notebook/PROMPT_LOG.md:166` |
| Size | 342 files outside `.git` (28M on disk including `.git`; 19M without it, per the verifier) | auditor's count (derived): `find . -type f -not -path './.git/*' \| wc -l`; `du -sh .` |
| Prompt-log entries | 24 | [Embers] `notebook/PROMPT_LOG.md:22-170` (entries 1–24) |
| Agent-log entries | 54 | [Embers] `notebook/AGENT_LOG.md:14-67` (entries 1–54) |
| Ledger rows | 12: batch 1 has 9 (H1GAIT-A, H1GAIT-1, H1RESP-A, H1RESP-1, H1CARD-A/-1/-S/-C/-X); stk1 has 3 (STK1-1/-S/-C) | auditor's count (derived), [Embers] `ledger/LEDGER.md:24-37` |
| Primary hypothesis rows | 4: FAIL 1 (H1CARD-1), NOT DECIDABLE 2 (H1GAIT-1, H1RESP-1), VOID 1 (STK1-1) | auditor's count (derived), same lines |
| PASS rows (any level) | 0 | [Embers] `ledger/LEDGER.md:24-37` |
| Preregistrations | Hashed and scored: h1card, h1resp, h1gait, stk1. Hashed and OTS-stamped, data step "not before 2026-09-29T00:00:00Z", not run at 7082f23: stk2. Closed before freeze: fire1 | [Embers] `prereg/*/`; `prereg/stk2/PREREG.md:22`; `prereg/fire1/CLOSED.md:1-4` |
| Retrodiction batteries | R1 14, R2 36 (+ correction row C1), R3 50 systems. Cumulative: "REDUNDANT-DOMAIN 74, REDUNDANT-IG 12, WRONG 9, PROPOSES 2, UNSTATED 1, ADDS(PARTIAL) 1, ARTEFACT 1" | [Embers] `retro/REPORT_R3.md:88-92`; `notebook/AGENT_LOG.md:52` (entry 39) |
| Synthetic gates | H1 GATE OPEN (run 1 CLOSED, kept); H2 GATE OPEN; H3 v1 CLOSED, v2 OPEN, fresh seeds OPEN; A7 GATE OPEN; fire1 CLOSED | [Embers] `results/gate_h1.txt`, `gate_h1_run1_CLOSED.txt`, `gate_h2.txt`, `gate_h3*.txt`, `gate_a7.txt` (last lines); `prereg/fire1/CLOSED.md` |
| Adversarial self-audit | "TALLY: HOLDS 34 DEFECT 0 WEAK 9 NOTE 4" (after the repairs; first pin had DEFECT 11) | [Embers] `results/adversarial.txt:54`; `notebook/AGENT_LOG.md:26` (entry 13) |
| Ashes for comparison | 235 ledger rows; held-out PASS-1 1 (SEC4-1); held-out PASS-0 15 by `ladder.py` | [Ashes] `Pre_Phoenix_Audit/checks/outcome_classes.txt:48`; `derived_counts.txt:20-25` |

**Timing caveat.** Embers read Ashes at 0edbc37. Ashes' CRR.md has not changed since then: the last commit touching
`theory/CRR.md` is 455780b, 2026-09-17 (`git log -- theory/CRR.md` in [Ashes]).

Ashes' ledger and studies have moved on. At 0edbc37 the Ashes ledger had 165 rows ([Embers] `CRR_Ashes/README.md:12`) and
no PASS-1 ([Embers] `CRR_Ashes/README.md:196`). SEC4-1 PASS-1 and the SEC5–SEC6R rows came later
([Ashes] `Pre_Phoenix_Audit/checks/outcome_classes.txt:226-279`, ledger order).

So Embers' account of the Ashes record is a snapshot. That is a timing difference, not a disagreement.

---

## 2 Inheritance (question 1)

### 2.1 What was inherited

| kind | what | how it is used in Embers | citation |
|---|---|---|---|
| Theory text | CRR.md v3.1. "A1/A1′/A3/A6/A7/A8, D2/D3/D4, P1/P2/P3" are the "audited starting point" | Tagged `BASE` in `docs/MATHEMATICS.md`. "The original repo's A1/A3/A6/A7/A8 and D2/D3/D4 motivate this draft" | [Embers] `docs/SOURCES.md:9` (file line); `docs/MATHEMATICS.md:3-13`; `README.md:69` |
| Rules | Ashes CLAUDE.md R1–R15 and the PASS ladder, snapshotted verbatim as `docs/source_protocol/ashes_CLAUDE_0edbc37.md`. "The source's R1–R15, R0–R8 ladder, PASS-0/1/2 criteria and closure rules govern a study even where this summary is shorter" | Enforced by `scripts/check_all.sh`, which verifies the snapshot and the append-only logs | [Embers] `docs/EPISTEMIC_GUARDRAILS.md:10-13`; `CLAUDE.md:94-107` |
| Rungs | R0–R8 "unchanged from the source" | Taxonomy axis A | [Embers] `docs/EPISTEMIC_TAXONOMY.md:70-72` |
| Code | The synthesis-class outcome rule: "ported verbatim in logic from ashes `src/crr/synthesis/harness.py` @ 0edbc37", TOL_G = TOL_N = 1 % | `retro/harness.py` decides every R1–R3 label | [Embers] `retro/harness.py:1-9` |
| Data status | Ashes `data/SEEN.md` copied verbatim as Part B. "records previously used in `ashes_crr` are seen for the same inquiry" | Every Ashes dataset is excluded from held-out | [Embers] `data/SEEN.md:22-27`; `docs/EPISTEMIC_GUARDRAILS.md:64-67` |
| Retrodiction class | The SYNTHESIS class: T-G / T-N / T-C; REDUNDANT-IG = R1, REDUNDANT-DOMAIN = R2, ADDS = R3 | Applied to the Embers formalism | [Embers] `retro/DECLARATION_R1.md:14-31` |
| Verdicts and lessons | An audit of Ashes at 0edbc37, fact-checked: 687 claims checked by hand, 649 confirmed, 38 discrepancies (4 material) | `CRR_Ashes/`, labelled "historical content ... confers no status" | [Embers] `notebook/AGENT_LOG.md:34` (entry 21); `CLAUDE.md:109-110` |

### 2.2 Did Embers treat Ashes verdicts as settled? Yes, as priors and lessons, not as Embers rows

Embers states that Ashes rows "are **not** rows of this ledger and confer no status on CRR_Embers"
([Embers] `ledger/LEDGER.md:9-10`). Ashes verdicts nonetheless enter Embers as settled premises in four places.

1. **"What CRR_Embers inherits from this record"**, nine numbered lessons ([Embers] `CRR_Ashes/README.md:202-222`). Among
   them:
   - item 4, "H-L5 fails on clock-regular systems ... Test clock-regularity before choosing a carrier";
   - item 5, "Domain events sit at extrema, not antipodes, and the registered cut needs the future";
   - item 7, "Every CRR-specific part of H-EQ failed or reduced";
   - item 8, "No corroborated novel fact".
2. **Priors for every natural-data row.** "For every natural row below, the honest default is FAIL or NOT DECIDABLE"
   ([Embers] `docs/DOMAIN_PORTFOLIO.md:182-183`). The stated basis is the Ashes pattern: "A6 fails where the domain
   accumulates. The antipode fails where the domain's event is an extremum. H-L5 fails where the system is clock-regular ...
   Path-over-endpoint fails where the state is Markov or an endpoint" (`:168-173`).
3. **The taxonomy's §8 places the Ashes rows on its axes.** For MEAS2, CARD, T1X2 and RLAW it reads: "FAIL: empirical
   readings of H-L5, D6/H-T1 and the regeneration law retracted for those classes" ([Embers]
   `docs/EPISTEMIC_TAXONOMY.md:198`). It concludes: "CRR entered CRR_Embers with **no corroborated novel fact**" (`:201-203`).
4. **H1 instrument design.** A7 compliance makes the causal phase primary ([Embers] `crr_embers/h1.py:15-18`), which answers
   the Ashes finding that "the registered cut needs the future". Measles and CARD records may serve only "as stress tests,
   not new holdouts" (`docs/EPISTEMIC_GUARDRAILS.md:65-67`).

**Auditor's reading.**
- Items 1–3 use Ashes verdicts as premises for Embers' design choices and priors. That is a legitimate use: a prior is
  not a verdict. Embers labels each premise with its Ashes source path.
- Two of the premises are stated more strongly than the cited Ashes evidence supports at the level Ashes' own lineage
  notes assign. This is a disagreement over interpretation, not a factual error, and §6 states both sides:
  - "Domain events sit at extrema, not antipodes" (see §6, D2);
  - "retracted for those classes" for H-T1 and RLAW (see §6, D8–D9).
- **One possible R3 tension, recorded, not adjudicated.**
  - Embers AGENT_LOG entry 14 set a fairness condition: "A design that would use a lesson from those results (for example,
    redesigning a cardiac H-L5 test after CARD) is held to 2026-09-28 under R3" ([Embers] `notebook/AGENT_LOG.md:27`).
  - H1CARD, a cardiac study, was hashed on 2026-09-27. Its prereg discloses the Ashes CARD study as "a **design exposure**
    to this physiological class ..., not to these records" ([Embers] `prereg/h1card/PREREG.md:26-30`).
  - Embers judged H1 on mghdb not to be a redesign of the Ashes H-L5 test. Whether the disclosure suffices under the
    Ashes R3 wording ([Ashes] `CLAUDE.md`, R3) is for a reviewer. It changes no verdict.

---

## 3 The rotor extension (question 2)

### 3.1 What it adds to CRR.md v3.1, clause by clause

| Embers item ([Embers] `docs/MATHEMATICS.md`) | Status in Embers | Nearest CRR.md v3.1 clause ([Ashes] `theory/CRR.md`) | What changes |
|---|---|---|---|
| **R1, carrier.** An identifiable embedded circle of positive distributions p(z\|θ). Fisher arc s(θ) = ∫√g, circumference ℓ, a = ℓ/2. The *intrinsic* circle distance is d = min(r, ℓ−r) (`:15-27`) | ASSUMPTION | A1 (`:50-53`); D3, the chord as "the geodesic distance" d_FR (`:85-86`); A3's rotor "u ∈ ℝ/Lℤ (intrinsic phase, a circle of circumference L)" (`:101-103`) | It **chooses** the Fisher arc coordinate as the rotor phase, and the intrinsic, not ambient, chord. It shows that the ambient chord gives a monotone half-turn positive surplus (`:28-39`). The README calls these "**additional modelling commitments**" (`README.md:70-73`) |
| **σ in Fisher-length units** (`:41-51`) | ASSUMPTION / clarification | A1′: σ = 1.4826·MAD of an occasion statistic's residual in raw units (`:61-67`) | Flags that a raw-amplitude σ "cannot directly divide a Fisher arc", because detectability varies with the state (Bernoulli example 0.03263 against 0.02000) |
| **R2, cut.** The first forward passage of the unwrapped s through s_last + ℓ/2. A counting process N_t with unit clock-time atoms, and the Jacobian conditions for the phase delta (`:55-82`) | ASSUMPTION | A3, δ(Now) = δ(u(t) − u(t_n) − L/2) (`:101-106`) | It makes "half a turn" mean **half the Fisher circumference** and defines the event measure. Ashes' implemented cut is half a turn of the analytic-signal phase ([Ashes] `src/crr/instrument/core.py:89-114`) |
| **R3, surplus.** S_n = 2B_n/σ on the 1-D intrinsic circle; monotone ⇒ S = 0 (`:86-103`) | RESULT ("standard path-length arithmetic") | D4, P1 (`:88-95`) | Exact form of D4 on the circle; restricted to the intrinsic chord |
| **R4, laws of motion.** ζ(s,m) ds/dt = τ − ∂U/∂s + η, with physical friction ζ separate from g; inertial form with a connection term; optional OU drive (`:105-174`) | ASSUMPTION ("constitutive additions") | None. "It has no equations of motion" (`:31-32`) | **New.** Embers itself states it "does not claim a universal law of motion" (`README.md:7-8`). Its battery reports: "The Embers equations are the washboard/Adler law, first-passage theory and a normalised exponential memory" (`retro/REPORT_R2.md:78-80`) |
| **R5, regeneration.** A seed m_{n+1} ∈ argmin Σ q^(n−j) d_Y(y, Φ_j)²; flat closure m ← qm + (1−q)Φ. "There is no universal value of `q`". Circle-mean non-uniqueness (`:176-213`) | ASSUMPTION | A6: "The successor state is the Fisher–Rao Fréchet mean of past occasion contents" (`:144-153`); P3 (`:159-160`) | "**The seed `m` is distinct from continuous phase `s`: that is an explicit revision**" of A6 (`:215-218`) |
| **R6, cost.** Q_n T_n ≥ ζ_min(a + 2B_n)²; W_cut at potential switches (`:220-245`) | RESULT ("existing thermodynamic-length mathematics") | None | New conditional bound; "not a new thermodynamic result" (`:244-245`) |
| **VII, ontology** (`:247-261`) | ONTOLOGY / OPEN | A7, A8 (`:291-302`) | "Objective openness requires a separate commitment" (`:253-254`) |
| **Hypotheses H1, H2, H3** ([Embers] `docs/EMPIRICAL_PROTOCOL.md:61-79`; `docs/EPISTEMIC_GUARDRAILS.md:156-196`) | HYPOTHESIS | §9's H-CUT, H-L5, H-T1, H-EQ (`:306-313`) | **H1:** an independently measured event lies nearer the Fisher antipode than the angular antipode and the best fitted baseline. **H2:** memory-coupled flow beats κ = 0 and a matched conventional feedback model. **H3:** a cost check. "The H1/H2 names below belong to this *new rotor extension* and do not retroactively validate the source repo's H-CUT/H-L5/H-T1/H-EQ" (`EMPIRICAL_PROTOCOL.md:9-10`) |
| **Structural conditions found in Embers** | Maths_Repair, transfer audit | — | **MR-002:** "The Fisher antipode is a property of the pair (rotor, observation law)". **MR-004:** the two antipodes "differ **only through the odd harmonics of √g**" ([Embers] `Maths_Repair/README.md:14,16`). **S1** (Fisher half-turn ½) and **S2** (occasion-counted ageing q^(n−j)) are "Exactly two structural commitments" ([Embers] `docs/TRANSFER_CANDIDATES.md:77-100`) |

### 3.2 What was tested

| target | test | outcome, quoted | rung |
|---|---|---|---|
| H1 (S1) | h1card, h1resp, h1gait (batch 1, m = 3, α = 0.05/3) | H1CARD-1 "FAIL" (vs angular: FISHER 0, OTHER 19, TIE 0, p 3.8147e-06; vs best fitted baseline the same). H1RESP-1 and H1GAIT-1 "NOT DECIDABLE" | held-out, strongly anchored ([Embers] `ledger/LEDGER.md:24-32`) |
| S2 (occasion-counted ageing, MATHEMATICS §V) | stk1 on Marone-lab runs p5156, p5363, p5565 | STK1-1 "**VOID**": p5156 "Unknown mat file type"; p5363 HTTP 404; p5565 not fetched | held-out registration, nothing scored ([Embers] `ledger/LEDGER.md:35`) |
| S2 (successor) | stk2, p5565 only | not run at 7082f23 | — ([Embers] `notebook/AGENT_LOG.md:61-62`, entries 48–49) |
| R1-12 (inverse-Gaussian fire intervals) | fire1 surrogate gate | "CLOSED before exposure (not a result about fire, and not a FAIL of CRR)" | R4 ([Embers] `prereg/fire1/CLOSED.md:18-21`) |
| R1-10 (paleoseismic memory) | power analysis | "NOT DECIDABLE by design" (n_required = 11231) | R4 ([Embers] `retro/followup/R1_10_FEASIBILITY.md:20,32`) |
| H2, H3, A7 | synthetic gates | GATE OPEN (H2, with a binding parity-comparator requirement; H3 v2; A7) | R4 ([Embers] `notebook/AGENT_LOG.md:39-41`, entries 26–28) |
| Laws of motion, cut, memory, on 100 systems | retrodiction batteries R1–R3 | "74 \| 12 \| 9 \| 2 \| 1 \| 1 \| 1" (RD, RIG, WRONG, PROPOSES, UNSTATED, ADDS(PARTIAL), ARTEFACT) | R1–R4 ([Embers] `retro/REPORT_R3.md:88-92`) |
| Mathematics | 35 unittest cases, independent checks, adversarial audit | "Ran 35 tests"; "HOLDS 34 DEFECT 0 WEAK 9 NOTE 4" | R0/R1 ([Embers] `results/tests.txt`; `results/adversarial.txt:54`) |

---

## 4 Embers lineages (questions 3 and 6)

Stable IDs for Embers lineages, chosen by the auditor:
- **E-H1:** the Fisher cut against the angular cut, S1.
- **E-S2:** occasion-counted memory and the transfer programme.
- **E-H2H3:** memory-coupled flow and cost.
- **E-RETRO:** the batteries R1–R3, fire1 and R1-10.
- **E-MATH:** Maths_Repair, the adversarial audit and Elegance.
- **E-INH:** the CRR_Ashes audit and its lessons.

### 4.0 Which Embers failures bear on baseline CRR and which only on the rotor (question 3)

| Embers outcome (quoted) | target | bears on baseline CRR.md v3.1? | highest level it legitimately reaches (auditor's reading, from Embers' own blame tables where they exist) |
|---|---|---|---|
| H1CARD-1 "FAIL"; H1CARD-S "0 of 17 cells differ"; H1CARD-C "control holds" | H1 (rotor R1 + R2 + bridge) | **No CRR.md hypothesis.** H-CUT compares the antipode with the *extremum* on the system's own events ([Ashes] `theory/CRR.md:123-131`). H1 compares the *Fisher* antipode with the *angular* antipode and a fitted lag, against an event on another channel ([Embers] `docs/EMPIRICAL_PROTOCOL.md:63-67`). It bears on A3 only under Embers' reading that A3's half-turn is half the Fisher arc (§6, D1) | Embers' blame table: "H1 for this (system, observation law) class: a 2-lead raw-ECG Gaussian Fourier carrier ..., ART foot → dicrotic notch events, ... 360 Hz; and so the L1 commitment's empirical reading under this bridge" ([Embers] `prereg/h1card/PREREG.md:187`). **Class A for H1 in that class.** It does not reach S1 in other carriers, by Embers' own rule: retraction needs FAILs "on two independent admissible studies in that class" ([Embers] `docs/EPISTEMIC_TAXONOMY.md:162-164`) |
| H1GAIT-A/-1 "NOT DECIDABLE" (force headers carry no side labels) | bridge | No | **D** (loader/bridge). "this refutes only 'this dataset under these label rules can test H1', not H1" ([Embers] `notebook/AGENT_LOG.md:42`) |
| H1RESP-A/-1 "NOT DECIDABLE" (separation 0.316920 s < 2δ 0.500000 s; 8 Hz airflow) | bridge | No | **E** (resolution). Decidable with "A finer event channel" (`notebook/AGENT_LOG.md:43`) |
| STK1-1 "**VOID**" | S2 | **Potentially yes, had it run.** S2 is A6's weights indexed by occasion, q^(n−j) ([Embers] `prereg/stk1/PREREG.md:19`). CRR.md's P3 also weights by age over occasions ([Ashes] `theory/CRR.md:159-160`), and A1′ makes natural time the event count (`:59-60`) | **D**. "This says nothing about S2, friction or CRR" ([Embers] `runs/stk1/RESULT.md:1`) |
| fire1 "CLOSED before exposure" | first-passage IG interval law (rotor R2 + R4) | No | **E** (power): "IG ... wins the per-site comparison against lognormal in 0.500125 of 24000 sites" ([Embers] `prereg/fire1/CLOSED.md:14-15`) |
| R1-10 "NOT DECIDABLE by design" | bounded memory at cuts (rotor R5) | No | **E** |
| R2-01, R2-03, R2-21, R3-10 WRONG (oriented cut counts records; half-turn at the turning point; 2-D Fisher half-turn marks no extremum; unfinished decline) | the Embers Fisher/first-passage cut | Through A3 only under Embers' cut reading | **A at R4 (synthetic)** for the cut as Embers defines it, in those model systems. "recorded as limits of A3/A6, not repaired" ([Embers] `retro/REPORT_R2.md:81-88`) |
| R2-27, R2-32, R2-C1, R3-22, R3-48 WRONG (one kernel, no accumulation, no hyperbolic discounting) | A6 normalised geometric kernel | **Yes, A6, at R4.** These are domains outside A6's stated design: "regeneration returns a reweighted content, never an accumulated count" ([Ashes] `theory/CRR.md:151-153`) | **A at R4** for "A6 is a model of these domains". Embers: "A6 averages with one timescale and cannot accumulate, hold several scales, or discount hyperbolically" ([Embers] `retro/REPORT_R3.md:115-116`) |
| R3-49 WRONG (Lindy) | first-passage lifetime | No (rotor R2) | **A at R4** |
| MR-003 | P3's ⟨k⟩ = q/(1−q) | **Yes, a scope note on baseline P3.** "The ashes P3 formula ⟨k⟩ = q/(1−q) holds only on infinite support (q=0.5 on 0..7 gives 0.968627, not 1)" ([Embers] `Maths_Repair/README.md:15`) | Mathematical wording only (OPEN) |
| MR-002 / MR-004 | the cut's carrier dependence; odd harmonics | Bears on A3/A1 identifiability for any Fisher-arc reading of the cut | **E** (identifiability). "Until a principle picks the carrier, every H1 prereg must fix the observation law before exposure" ([Embers] `Maths_Repair/README.md:14`) |

### 4.1 E-H1: the Fisher cut against the angular cut (S1)

**Four-layer table.**

| observation | (1) observed | (2) rotor interpretation | (3) ordinary explanation | (4) what would distinguish |
|---|---|---|---|---|
| H1CARD-1 | In 19/19 admissible held-out units the dicrotic notch is nearer the angular antipode and the fitted lag than the Fisher antipode; p 3.8147e-06 ([Embers] `ledger/LEDGER.md:29`). Auditor's count (derived, from `runs/h1card/summary.txt:6-24`): in 19/19 units the per-unit stat_angular equals −separation to within 0.00101 s, and stat_best < stat_angular. On my reading, in the median occasion the notch sits at or before the earlier (angular) antipode in every unit, which is consistent with the prereg's prior | H1 refuted for this (carrier, bridge) class ([Embers] `reports/batch1.md:15`) | "The dicrotic notch marks aortic-valve closure. It follows the foot by the left-ventricular ejection time" ([Embers] `prereg/h1card/PREREG.md:198-201`). It is a mechanical interval, not a half-turn of any phase | A carrier where MR-004's odd harmonics are large and the event has no mechanical-lag explanation. Embers names "neurons with von Mises tuning, strongly skewed waveforms, and multi-sensor encoders" ([Embers] `docs/TRANSFER_CANDIDATES.md:164`) |
| H1RESP | Separation 0.316920 s; 2δ 0.500000 s; odd-harmonic amplitude 0.3686 ([Embers] `notebook/AGENT_LOG.md:43`) | The cuts differ but are unresolvable | An 8 Hz thermistor channel | A higher-rate event channel |
| H1GAIT | All 26 training units excluded: headers carry no side labels (`notebook/AGENT_LOG.md:42`) | None | Dataset format | A documented plate→side mapping, in a new study |
| MR-004 / s1_discriminability | Symmetric laws give an identical Fisher cut and angular antipode; lopsided laws separate them by 0.0079–0.1667 of the cycle (`docs/TRANSFER_CANDIDATES.md:142-159`) | S1 is "empty" on symmetric instruments | Fourier symmetry of √g | Not an empirical question: it is a design constraint |

- **Salvage class.** **A** for H1 in the class tested. **E** for MR-002 (the carrier choice is unfixed by theory). **D/E**
  for the two NOT DECIDABLE studies.
  - **Chain:** core principle (cut at half a turn, A3) → rotor operationalisation (half the intrinsic Fisher arc of a fitted
    Gaussian Fourier ECG law, causal R–R phase) → test (notch timing on mghdb) → FAIL.
  - **Highest level actually challenged:** H1 under that bridge ([Embers] `prereg/h1card/PREREG.md:187`). The prereg says it
    does not reach "L0; other carriers ...; other event pairs ...; other populations".
- **Extinguished-lead check.**
  - Embers' transfer audit says of S1: "the cross-domain parameter-free candidate exists, has already been tested, and has
    not survived" ([Embers] `docs/TRANSFER_CANDIDATES.md:89`). That sentence is stronger than three things in Embers' own
    record:
    - its blame table (one class);
    - its retraction rule (two FAILs per class; `docs/EPISTEMIC_TAXONOMY.md:162-164`);
    - its addendum, which lists the S1 domains still untested (`:161-166`).
  - **Auditor's reading.** S1 was tested once, on a carrier the prereg expected to fail (`prereg/h1card/PREREG.md:194`) and
    whose PASS "cannot validate the rotor-specific cut theorem" ([Embers] `docs/DOMAIN_PORTFOLIO.md:361-363`). Calling S1
    "not survived" risks extinguishing it at a level above the evidence. The ledger row itself is correctly scoped.

### 4.2 E-S2: occasion-counted memory and the transfer programme

| observation | (1) observed | (2) rotor/CRR interpretation | (3) ordinary explanation | (4) what would distinguish |
|---|---|---|---|---|
| Transfer audit | "CRR has no universal constants"; only S1 and S2 are class S ([Embers] `docs/TRANSFER_CANDIDATES.md:58-63,77`) | S2: the memory half-life in clock time scales inversely with the event rate (ratio 0.500 vs 1.000) (`:90-100`) | Clock-time memory, e.g. frictional healing growing with hold time (`:98-99`) | The registered stk test (fit at rate 1, predict at rate 2) |
| s2_power_gate | κ = 0 control: "the classifier says 'occasion' in 70 % (N = 1000) and 64 % (N = 3000)" (`:194-195`) | — | A built-in false positive of the estimator | Calibrated margin; a precondition that κ > 0 |
| s2_transfer_gate v2 | "DECIDABLE at κ = 0.2 for N ≥ 300 events per rate"; no-memory false wins 0.14–0.15 (`notebook/AGENT_LOG.md:56`) | The design can see S2 if present | — | stk1/stk2 on real data |
| STK1-1 | VOID: a format mismatch and a 404 | None | Infrastructure | stk2 (p5565) |

- **Salvage class.**
  - **D** for stk1.
  - **F-pending:** an untested but gated design, the one Embers line that could bear on a *baseline* commitment (A6/P3
    indexed in occasions; A1′ natural time).
  - **No A, B or C yet.**
- **Extinguished-lead check.**
  - Not extinguished. stk2 was frozen with a data step "not before 2026-09-29T00:00:00Z" ([Embers] `prereg/stk2/PREREG.md:22`).
  - Its outcome is not in the clone read.
  - Phoenix should read Embers after 7082f23 before stating S2's status.

### 4.3 E-H2H3: memory-coupled flow and cost

| observation | (1) observed | (2) interpretation | (3) ordinary explanation | (4) distinguishing evidence |
|---|---|---|---|---|
| gate_h2 OPEN, 21/21 | POS beats κ = 0 and the best conventional model ([Embers] `notebook/AGENT_LOG.md:40`) | The instrument can see memory-coupled flow | "POS beats the conventional models only because memory acts with **opposite signs on the two half-turns**, and a parity-aware linear model would probably tie it" (same entry) | Gate run 2 with a parity-aware comparator, which Embers made binding before any H2 prereg |
| gate_h3 v2 OPEN | Bound identity holds; "B comparison REDUCES in 15/15" ([Embers] `results/gate_h3.txt`, last lines) | Conditional mechanics | "The bound is a theorem" (`notebook/AGENT_LOG.md:41`) | Measured friction and dissipation on a real rotor |

- **Salvage class.** **C** for H3: a theorem, which Embers also says reduces. **R4 only** for H2, with an acknowledged
  probable reduction (C-risk).
- **Extinguished lead:** none. No real-data test exists.

### 4.4 E-RETRO: batteries R1–R3, fire1, R1-10

| observation | (1) observed | (2) interpretation | (3) ordinary explanation | (4) distinguishing evidence |
|---|---|---|---|---|
| 74 RD / 12 RIG of 100 | Consistency to 6–12 digits in many rows ([Embers] `retro/REPORT_R3.md:96-103`) | The Embers law, cut and memory are internally consistent with many domains | "The consistency is inherited from first-passage theory, stochastic energetics and exponential smoothing" (`:149-150`). "About half the rows are marked re-expressions" (`:101`) | A row where the Embers value differs from the domain's and the domain is wrong: an ADDS that survives the literature check. There are none |
| 9 WRONG | Boundaries of A3/A6 ([Embers] `retro/REPORT_R3.md:104-116`; `retro/REPORT_R2.md:81-88`) | Limits of the formalism | Accumulating or multi-scale memory; extremum events | Already decided at R4 |
| R2-28 | ADDS → PARTIAL: "direction = published exponential-tail theorem for integrable ageing, for a close variant" ([Embers] `notebook/AGENT_LOG.md:48`) | Ageing caps hubs | Known for trees; "the m ≥ 2 case stated as an open problem" (entry 37) | A proof or published result for m ≥ 2; a named expert |
| fire1 | Gate closed (power) | — | Eight intervals per site cannot separate IG from lognormal | A pooled likelihood with a site bootstrap, under a new gate ([Embers] `prereg/fire1/CLOSED.md:19-21`) |

- **Salvage class.**
  - **C** (dominant).
  - **A at R4** for the nine WRONG rows.
  - **E** for fire1 and R1-10.
  - **F (weak)** for R2-28, which Embers says "cannot become CRR-specific (A6 = integrable ageing)"
    ([Embers] `notebook/AGENT_LOG.md:50`, entry 37).
- **Extinguished-lead check.** No lead was killed above its level:
  - fire1 is explicitly "not a FAIL of CRR";
  - R1-10 is "NOT DECIDABLE by design";
  - the weak passes are listed, not relabelled ([Embers] `retro/REPORT_R3.md:119-133`).

### 4.5 E-MATH: Maths_Repair, the adversarial audit, Elegance

| observation | (1) observed | (2) interpretation | (3) ordinary explanation | (4) distinguishing evidence |
|---|---|---|---|---|
| MR-001 | "a NaN `now` let `gated_age_memory` admit **future** marks" ([Embers] `Maths_Repair/README.md:13`) | An A7 breach in code | Missing input guards | Repaired; regression tests |
| MR-002 | Fisher antipode 3.637349473 / 3.573190331 / 3.648726599 for ε = 0.6 / 0.2 / 0.95, against an angular 3.541592654 (`:14`) | The cut is relative to the observation law | Čencov fixes the metric only up to sufficient statistics | A principle that picks the carrier. None exists |
| MR-003 | q = 1.521380 needed for mean age 2.0 on 0..3 (`:15`) | Scope of P3 | Finite-support MaxEnt | Wording |
| MR-004 | 0.000000 rad separation for half-turn-periodic √g (`:16`) | H1 admissibility | Fourier symmetry | Design constraint |
| Elegance EL-001..013 | "**never evidence**" ([Embers] `Elegance/README.md:3-5`) | Interpretive notes | Mostly inherited mathematics ("inherited from" column) | — |

- **Salvage class.**
  - **D** for MR-001.
  - **E** for MR-002 and MR-004.
  - Wording only for MR-003.
  - Elegance entries are outside A–G: not evidence, as Embers states.
- **Extinguished lead:** none.

### 4.6 E-INH: the CRR_Ashes audit

- **Observed.** A fact-checked historical audit, labelled "historical content ... confers no status"
  ([Embers] `CLAUDE.md:109-110`).
- **Salvage class.** Not applicable: it is an account of Ashes, not a test.
- **Extinguished-lead check.** Two lessons are stated above the level of their evidence: the antipode lesson (§6, D2)
  and the propagation of single FAILs (§6, D8). Both enter Embers as priors, not as verdicts.

---

## 5 Epistemic machinery compared (question 4)

### 5.1 Side by side

| element | Ashes | Embers |
|---|---|---|
| PASS levels | PASS-0/1/2 ([Ashes] `CLAUDE.md` §7) | The same, verbatim: "These levels reproduce the source's PASS definitions" ([Embers] `docs/EPISTEMIC_GUARDRAILS.md:200-211`) |
| Ladder | R0–R8, computed by `Epistemic_Review/checks/ladder.py` ([Ashes] `CLAUDE.md` §7) | R0–R8 "unchanged", plus five more axes: layer, novelty N0–N3, specificity S0–S3, robustness, scope ([Embers] `docs/EPISTEMIC_TAXONOMY.md:65-104`) |
| Layers | The theory tags [A]/[D]/[P]/[M]/[H]/[O] ([Ashes] `theory/CRR.md:8-15`) | L0 ontology … L4 hypotheses ([Embers] `docs/EPISTEMIC_TAXONOMY.md:55-63`), and five claim types ([Embers] `docs/EPISTEMIC_GUARDRAILS.md:38-46`) |
| Blame before data | Not required by [Ashes] `CLAUDE.md` or `prereg/PREREG_TEMPLATE.md`. Auditor's check: `grep -i blame` finds no match in either file or in `prereg/*/PREREG.md` | A required table in every prereg: "each study states which conjunct a FAIL refutes" ([Embers] `docs/EPISTEMIC_TAXONOMY.md:31-32,122-137`; e.g. `prereg/h1card/PREREG.md:179-190`) |
| Honest prior | Investigator forecasts in labs and PRED70 (e.g. "CARD-1 FAIL", [Ashes] `labs/L03_pulse/LAB.md:30-32`, per `Pre_Phoenix_Audit/notes/L-HYP.md:37`) | In every prereg (e.g. "Expected label: FAIL (P ≈ 0.80)", [Embers] `prereg/h1card/PREREG.md:194`) |
| Multiplicity | No family-wise rule. Auditor's check: `grep -i "bonferroni\|multiplicity\|family-wise"` finds nothing in [Ashes] `CLAUDE.md`, `prereg/PREREG_TEMPLATE.md` or `prereg/*/PREREG.md` | "α per study = 0.05 / m for m simultaneously registered studies" ([Embers] `docs/EPISTEMIC_TAXONOMY.md:179-181`); batch 1 m = 3 ([Embers] `reports/batch1.md:5`) |
| Anchoring | R2: OTS + signed tag ([Ashes] `CLAUDE.md` R2). At 0edbc37, "3 of 18 hashed preregistrations have OpenTimestamps proofs" ([Embers] `CRR_Ashes/README.md:183`). Later Ashes studies are OTS-complete (e.g. SEC4–SEC6R, [Ashes] `CLAUDE.md` §0) | A Bitcoin block verified *before* any data step by `scripts/verify_anchor.py`. "A pending calendar receipt alone is not a pre-exposure anchor" ([Embers] `notebook/AGENT_LOG.md:27,29`, entries 14, 16). Retrodiction declarations are also anchored before code ([Embers] `retro/DECLARATION_R1.md:4-6`) |
| Hash recipe | One sha256 over the folders ([Ashes] `CLAUDE.md` §8). [Ashes] `prereg/scl3/HASH.txt:7` lists `./HASH.txt` itself | `scripts/freeze.py`: a manifest excluding HASH/MANIFEST/*.ots, "without the self-listing flaw ashes had" ([Embers] `notebook/AGENT_LOG.md:29`) |
| Signed tags | Pushes refused (per Embers' reading of `runs/scl3/tag_attempt.txt`) | Pushes refused too (HTTP 403); tag objects committed ([Embers] `notebook/AGENT_LOG.md:38`, entry 25) |
| R3 | Literal same-day rule ([Ashes] `CLAUDE.md` R3) | First read as a universal next-day hold, then corrected: "Entry 11 overstated R3" ([Embers] `notebook/AGENT_LOG.md:27`). The practice adopted is the Ashes one: hold only after a rule change |
| Decidability | Preconditions (EQ2-0 etc.). Instrument gates computed after scoring produce UNINFORMATIVE rows ([Ashes] `Pre_Phoenix_Audit/checks/outcome_classes.txt:274-279`, SEC6R) | Calibration-only separation ≥ 2δ, decided on training units before held-out units are opened ([Embers] `notebook/AGENT_LOG.md:28`, entry 15) |
| Append-only enforcement | Rule text (R8, R13, R14) | Also a script: `scripts/check_append_only.py` in `check_all.sh` and CI ([Embers] `CLAUDE.md:94-107`) |
| Post hoc | Post hoc lines are labelled; FAILs are not rescued ([Ashes] `Pre_Phoenix_Audit/notes/PROCESS.md:611-626`) | "Post-hoc adjustments" are a counted quantity on the scorecard ([Embers] `docs/EPISTEMIC_TAXONOMY.md:158-161`). Declined explicitly: "no side-label mapping for the gait data, and no δ change for the respiration data" ([Embers] `reports/batch1.md:18`) |
| Retrodictive class | The SYNTHESIS harness. Embers reads the Ashes synthesis rows as "N1 (Q not preregistered)" ([Embers] `docs/EPISTEMIC_TAXONOMY.md:194`). Ashes declared later banks first (`DECLARATION_31_32.md`; PRED70 "pushed at 8397478", [Ashes] `CLAUDE.md` layout) | The same harness; every battery declared blind, Bitcoin-anchored before code, with a literature-check rule declared in advance. Rows are marked "[re-expression]" and weak passes are listed ([Embers] `retro/DECLARATION_R3.md:30`; `retro/REPORT_R3.md:119-133`) |
| Self-audit of code | Tests; CI checks of pinned outputs | `checks/adversarial.py`, pinned *before* fixes: "so the defects remain on the record" ([Embers] `notebook/AGENT_LOG.md:22`, entry 9) |
| Exploratory zone | None declared. Exploration "kept off the record (AL 3)" ([Ashes] `Pre_Phoenix_Audit/notes/PROCESS.md:628-629`). Large retrodictive and declared-synthetic banks | None declared; see §5.2 |
| Second person | "No frozen script has been run by a second person" (Embers quoting Ashes, [Embers] `CRR_Ashes/README.md:221-222`) | None. Daniel Friedman raised GitHub issues #1–#3 and #5, which led to code and text fixes, no re-run ([Embers] `notebook/AGENT_LOG.md:64-65`, entries 51–52) |

### 5.2 Does Embers have an explicitly exploratory environment? How did it work in practice?

**No dedicated environment.** What it has is the following:
- **A contract clause in each prereg:** "anything beyond this contract ... is exploratory, gets no rung"
  ([Embers] `prereg/stk1/PREREG.md:258-259`; `prereg/stk2/PREREG.md:224`).
- **Two owner-requested folders that are never evidence:**
  - Maths_Repair, for errors;
  - Elegance, for "noted for future reference, not pursued" ([Embers] `Elegance/README.md:1-5`; `notebook/PROMPT_LOG.md:50`).
- **Synthetic design gates,** run the same day: S1 discriminability, the S2 power gate and the S2 transfer gate
  ([Embers] `notebook/AGENT_LOG.md:54-56`, entries 41–43).
- **Retrodiction batteries.** These were the de facto exploratory layer, but Embers declared and anchored them like
  confirmatory studies (`retro/DECLARATION_R1.md:4-6`).

**In practice.**
- Exploration happened only in synthetic worlds, and quickly. It was productive:
  - MR-004 and the S1 odd-harmonic table;
  - the S2 false-positive rate;
  - the leak caught in `s2_transfer_gate.py` v1 ([Embers] `notebook/AGENT_LOG.md:56`, entry 43).
- There was **almost no exploratory contact with real data**. The only exception: SEEN run p4581 was "re-opened for
  development: file-format and column parsing only" (entry 44, line 57).
- The protocol's "no peek before the anchor" stance meant that file formats and links were checked by metadata only. The
  drafting agent had flagged p5156's format "as an open risk: 'matlab format' on the page, 'v7.3 → VOID'"
  ([Embers] `runs/stk1/RESULT.md:18-19`). That is the failure that occurred.

### 5.3 Post hoc and retrodictive handling: summary

Both repositories keep first outputs, label post hoc work and refuse relabelling.

Embers adds three things:
- it counts post hoc adjustments explicitly;
- it binds a pre-data blame table to every prereg;
- it anchors its retrodiction declarations.

Both reach the same verdict on what the retrodictive class licenses:
- Embers: "It licenses nothing about CRR being true, predictive or specific" ([Embers] `retro/REPORT_R3.md:149`).
- Ashes: "broad expressive coverage, which is redescription. It does not establish unique prediction"
  ([Ashes] `Pre_Phoenix_Audit/notes/L-RETRO-ONT-APP.md:19-20`).

### 5.4 (a) Where Embers' machinery looks stronger, cleaner or fairer than Ashes'

1. **Pre-exposure anchoring is verified, not assumed.** A Bitcoin block is checked before data, with must-fail controls on
   the verifier itself ([Embers] `notebook/AGENT_LOG.md:29`, entry 16). It also covers the retrodiction declarations.
2. **The blame is fixed before the data.** A pre-data blame table, with "does not refute" columns, in each prereg
   ([Embers] `prereg/h1card/PREREG.md:179-190`). This makes the level a FAIL reaches explicit in advance. It is the very
   thing the Ashes self-audit had to reconstruct after the fact (e.g. [Ashes] `Pre_Phoenix_Audit/notes/L-HYP.md:127-142`).
3. **Decidability is settled before the held-out data are opened.** The H1 calibration gate refused to score held-out
   units when the cuts were unresolvable (H1RESP-A).

   Contrast: Ashes' SEC instrument gates were computed after scoring, which produced UNINFORMATIVE rows
   ([Ashes] `Pre_Phoenix_Audit/checks/outcome_classes.txt:274-279`).
4. **Multiplicity** within a same-day batch (Bonferroni, m declared before the hash).
5. **The adversarial code audit was pinned with its defects**, before the repairs ([Embers] `notebook/AGENT_LOG.md:22,25-26`).
6. **The retrodiction design lessons were enforced in the next declaration.** Those lessons were: nulls checked
   analytically, no exact-zero targets, and one decisive number per row ([Embers] `notebook/AGENT_LOG.md:47,49`,
   entries 34, 36). The result was "No lesson-1 coincidences" in R3 ([Embers] `retro/REPORT_R3.md:141-142`).
7. **The theory-level gap is stated as a gap.** MR-002 says the cut is relative to the observation law, and that every H1
   prereg must fix the law before exposure.

   Contrast: Ashes' v3.2 decision list was "never adopted" ([Ashes] `Pre_Phoenix_Audit/notes/L-HYP.md:547-548`).

### 5.5 (b) Where Embers may have become too confirmatory too early

1. **Tempo.**
   - Batch 1 was hashed about 2.5 h after prompt 1: auditor's count (derived), prompt 1 ≤ 02:53:43Z and "Hashed 2026-09-27
     ~05:22Z" ([Embers] `reports/batch1.md:5`).
   - Held-out data were opened from 06:32Z ([Embers] `notebook/AGENT_LOG.md:43`).
   - The owner's request was "at least 50 domains tested by 9am Pacific Time" ([Embers] `notebook/PROMPT_LOG.md:42`).
     Embers declined it as a test deadline (`:46`), then accepted a same-day first batch under conditions (`:56`;
     AGENT_LOG entry 14).
2. **A carrier chosen by admissibility, with a recorded expectation of failure.**
   - The batch-1 candidates were chosen by a "≥ 2 physical channels" rule ([Embers] `notebook/AGENT_LOG.md:33`, entry 20),
     not by any prior plausibility that the Fisher antipode marks the event.
   - h1card's prior was "FAIL (P ≈ 0.80)".
   - Embers' own portfolio says that, on such carriers, "Even a PASS-0 there cannot validate the rotor-specific cut theorem"
     ([Embers] `docs/DOMAIN_PORTFOLIO.md:361-363`).
   - **Auditor's reading.** The first held-out test of S1 was spent where neither outcome could support S1. The FAIL then
     informed a sentence that S1 "has not survived" ([Embers] `docs/TRANSFER_CANDIDATES.md:89`).
3. **Held-out records were consumed without a verdict.**
   - H1GAIT: "the whole zip was downloaded" (entry 29).
   - H1RESP: "The 13 held-out units were never scored (their files were downloaded, so they are SEEN)" (entry 30).
   - stk1: p5156 is now SEEN (entry 47).
   - Auditor's count (derived): of the four scored real-data studies, three ended without a hypothesis verdict.
4. **Power statements were written, but the tests went ahead anyway.**
   - The H1 smoke test showed "FRAGILE: 3 of 17 cells flip" at a true effect of about 2 % of the period.
   - The recorded consequence was that "a real effect near 2% can at best be PASS-0 and FRAGILE"
     ([Embers] `notebook/AGENT_LOG.md:30`, entry 17).
   - This was honest. It also shows the confirmatory step ran before any exploratory estimate of the effect size on
     SEEN data.
5. **Lessons imported as priors at generalisation strength.** See §2.2 and §6 D2/D8.

---

## 6 ASHES ↔ EMBERS CROSS-AUDIT (question 5)

### 6.1 Disagreements table

| # | topic | Ashes interpretation | Embers interpretation | evidence that would decide |
|---|---|---|---|---|
| D1 | What "half a turn" in A3 is measured in | A3 cuts on "intrinsic phase, a circle of circumference L" ([Ashes] `theory/CRR.md:101-106`). It is implemented as the analytic-signal phase + π ([Ashes] `src/crr/instrument/core.py:89-114`). The phase "has at least four readings" ([Ashes] `ontology/02_commitments.md:61-63`), and the choice is open ([Ashes] `Pre_Phoenix_Audit/notes/L-HYP.md:486-488`) | Half of the **intrinsic Fisher arc** of an identifiable statistical circle (`docs/MATHEMATICS.md:55-59`). The ordinary angular antipode is the *ablation* (`crr_embers/h1.py:285`). This is labelled an "additional modelling commitment" (`README.md:70-73`) | Not decidable by data alone: it is a theory decision (Ashes v3.2 item 1; Embers MR-002). Data can show which reading, if any, predicts events. That needs one study scoring the own event against the Fisher antipode, the angular antipode, the extremum and a fitted lag, on a carrier with large odd harmonics (MR-004) |
| D2 | Status of the antipodal cut after the record | "**No ledger row tests H-CUT**" ([Ashes] `L-HYP.md:457`). "H-CUT. Not extinguished. It was never brought to a test" (`:530`). Dominant class E (`:486`). Synthetic WRONG rows reach H-CUT only "as applied to those model systems" (`:500-504`). Note: Ashes' own ontology summary is more negative: "found undecided and, where decided, wrong" ([Ashes] `ontology/02_commitments.md:149`) | "Domain events sit at extrema, not antipodes" ([Embers] `CRR_Ashes/README.md:212`). "The antipode fails where the domain's event is an extremum" (`docs/DOMAIN_PORTFOLIO.md:170`). After H1CARD, S1 "has not survived" (`docs/TRANSFER_CANDIDATES.md:89`) | A held-out H-CUT test on own events with its own gate and positive control. Ashes names G-CD3/LIFE1 as the ready design ([Ashes] `L-HYP.md:511-512`); Embers names odd-harmonic-rich carriers (`TRANSFER_CANDIDATES.md:164`). Neither has been run |
| D3 | What a fair cut test needs | The *system's own event* on the carrier (slip, firing, R-peak), scored against the extremum. Noise-induced disagreement is never scored ([Ashes] `theory/CRR.md:123-131`) | An *independent* event channel. "Never derive the tested event from the phase used to predict it" ([Embers] `CLAUDE.md:35-36`; `EMPIRICAL_PROTOCOL.md:29-34`) | Whether same-channel own events create circular alignment. Ashes' gate_A3 shows peak-cut comparisons pass on content-free surrogates ([Ashes] `prereg/card/PREREG.md:45-54`, per `L-HYP.md:415`). A gate that runs both designs on the same surrogates would decide which is necessary |
| D4 | The successor state in A6 | "The successor state is the Fisher–Rao Fréchet mean" ([Ashes] `theory/CRR.md:144-149`); the cut "resets C to zero" (`:110`) | "The seed `m` is distinct from continuous phase `s`: that is an **explicit revision**" ([Embers] `docs/MATHEMATICS.md:215-218`) | Not empirical. It is a definitional choice, which Embers flags for owner review (`README.md:72-73`). A domain where the phase does not jump at the cut would make literal A6 an extra impulse with its own energy budget (`MATHEMATICS.md:217-218`) |
| D5 | Laws of motion | "It has no equations of motion" ([Ashes] `theory/CRR.md:31-32`). The FLOW audit: the framework supplies the velocity in "0 of 109" rows ([Ashes] `Pre_Phoenix_Audit/notes/L-RETRO-ONT-APP.md:21`) | Adds constitutive laws, but "does not claim a universal law of motion" (`README.md:7-8`). Domain physics is "supplied by the domain, never by CRR" (`docs/EPISTEMIC_TAXONOMY.md:62`). The owner's prompt read it otherwise: "the ashes crr had no laws of motion" (`notebook/PROMPT_LOG.md:78`) | Both repositories' documents agree that the flow is not CRR's. The difference is with the owner's framing, not between the repositories. A test where the Embers law's parameters, fitted in one condition, predict another (S2's design) would show whether the law carries content |
| D6 | The chord in D3/P1 | D3: the chord is "the geodesic distance" d_FR on the manifold. P1: equality "in one dimension: iff the segment is monotone" ([Ashes] `theory/CRR.md:85-91`) | "`S=0 iff monotone` requires the *intrinsic* carrier". The ambient simplex chord gives a monotone half-turn positive surplus: 1.397009 against 0.880169 ([Embers] `docs/MATHEMATICS.md:28-39`) | Mathematical. Embers' worked example is reproducible from its pinned checks ([Embers] `docs/AUDIT.md:14`, file line). Ashes' text does not say which geodesic is meant for an embedded circle. A v3.2 wording decision would settle it. I found no Ashes text that addresses it (auditor's search: `grep -i ambient` in `theory/`, `ontology/`, `docs/notes/` returned nothing) |
| D7 | The unit σ | σ = 1.4826·MAD of a raw occasion statistic ([Ashes] `theory/CRR.md:61-67`). "renaming a constant unit as Cramér–Rao cannot move an H-L5 verdict. Only a unit that varies along the record could, and the carrier metrics already test that" ([Ashes] `docs/notes/2026-09-25_cramer_rao_reading.md:73-75`). The instrument returns "0.8629 of the Cramér–Rao unit" (`:46-48`) | σ must be a Fisher length. A raw residual "cannot directly divide a Fisher arc", because detectability is state-dependent (Bernoulli: 0.03263 against 0.02000) ([Embers] `docs/MATHEMATICS.md:41-51`) | A preregistered rerun of one SEEN study, scoring the verdict under both units on a carrier whose metric varies along the record. Both texts agree that only a state-dependent unit could matter |
| D8 | How far a single held-out FAIL propagates | H-L5: **A** at the universal-claim level; it "does not reach the existential reading" ([Ashes] `L-HYP.md:127-139`). H-T1: **A**, plus **C** for the v3.1 comparator, which "reduces the test to 'is F an endpoint function'" (`:337-344`) | "FAIL: empirical readings of H-L5, D6/H-T1 and the regeneration law retracted for those classes" ([Embers] `docs/EPISTEMIC_TAXONOMY.md:198`). "Path-over-endpoint fails where the state is Markov or an endpoint" (`docs/DOMAIN_PORTFOLIO.md:172`). Embers' own retraction rule asks for two FAILs per class (`docs/EPISTEMIC_TAXONOMY.md:162-164`) | For H-T1, the Ashes data already bear on the comparator point. On T1X2 the best path is behind E_new by ≤ −0.05 on 5/5 and behind EWC on 5/5 ([Ashes] `Pre_Phoenix_Audit/checks/derived_counts.txt:33-39`). So the FAIL does not depend only on the near-definitional E_old (a reading of Ashes numbers, no verdict changed). For H-L5, a test on a carrier with a prior of arc-regularity (stick-slip) would decide whether the existential reading survives. For the retraction semantics, a rule adopted before data in whichever repository applies it |
| D9 | What RLAW's failure reaches | "a genuine falsification, but of a conjecture added on top of CRR.md". It reaches "the stated law"; "Nor does it reach A6/P3, since 'CRR does not fix q'" ([Ashes] `L-RETRO-ONT-APP.md:14,149-154`) | Lists RLAW under lesson 3, "A6 fails where domains accumulate ... On real data the systems kept far longer memory than α* (RLAW-U 0/5)" ([Embers] `CRR_Ashes/README.md:208-209`). The taxonomy has "the regeneration law retracted" (`docs/EPISTEMIC_TAXONOMY.md:198`) | Textual. CRR.md says "CRR does not fix q" (`theory/CRR.md:160`) and "no retention law is claimed" (`:268-271`). That supports the Ashes reading that RLAW does not reach A6 as stated. Embers does not state that A6 entails RLAW; it juxtaposes them. A reader of Embers' lesson 3 could infer more than the text of CRR.md licenses. Not a factual error on either side |
| D10 | Where RLAW is counted | Excluded from the ladder at the owner's request (prompt-log entry 139). Kept as a separate column in the audit tally ([Ashes] `Pre_Phoenix_Audit/checks/outcome_classes.txt:7-9,287`) | "the ladder omits the cleanest negative in the record" ([Embers] `CRR_Ashes/README.md:178-180`) | Not an evidential disagreement: both call the rows FAIL. It is a reporting choice |
| D11 | What the empty-cut safety work is | A construction: "neither the positive nor the negative evidence in this lineage can propagate to a principle stated in CRR.md" ([Ashes] `L-PAUSE.md:29-30`) | "Every real-data 'holds' is a construction check ... R0 in substance"; "a correct construction at R4, with prior art" ([Embers] `CRR_Ashes/README.md:62-70`) | **No disagreement of substance.** It differs only in the rung label (R0 against construction/R4) |

### 6.2 Per-item notes

- **D1–D3 form one cluster.** Both repositories identify the same identifiability problem: which phase, which carrier,
  which event. They answer it differently:
  - **Ashes** leaves the phase open. Its pre-Phoenix notes classify H-CUT as E.
  - **Embers** fixes one answer (the Fisher arc on a chosen observation law) and tests it, then finds MR-002: that answer
    is itself relative to the instrument.

  Neither side's position is a factual error. Ashes' implemented cut (analytic phase + π) is structurally closer to
  Embers' *ablation* (the angular antipode) than to Embers' hypothesis.

  Auditor's reading: in H1CARD the angular cut and a fitted lag both beat the Fisher cut. The Embers ledger registers no
  comparison of angular cut against lag ([Embers] `ledger/LEDGER.md:29`), so H1CARD gives no verdict on the angular
  reading either.
- **D2 is the sharpest divergence in meaning.**
  - Embers' lesson ("Domain events sit at extrema, not antipodes") cites Ashes `ontology/01_the_cut.md`
    ([Embers] `CRR_Ashes/README.md:212`). Its stated basis is Ashes synthesis rows (b14 r2, b19 r1) and the Rupture gate
    ([Embers] `docs/DOMAIN_PORTFOLIO.md:42`). [Verifier correction, 2026-10-02: an earlier draft listed PRED70 here, but
    PRED70 postdates both 0edbc37 and 7082f23.] Ashes' own ontology summary reaches a similar reading: "found undecided and,
    where decided, wrong" ([Ashes] `ontology/02_commitments.md:149`).
  - The Ashes pre-Phoenix notes read the same rows as reaching H-CUT only on model systems.
  - So the disagreement is partly *inside* Ashes (ontology summary against lineage audit), and Embers inherited the
    ontology's version.
- **D8.** Both repositories record the same FAIL rows. They differ on the vocabulary of propagation ("retracted for those
  classes" against "A at the stated level, not the existential reading"). Embers' taxonomy states its retraction counts
  are "a proposal for the owner to adopt or amend before the first CRR_Embers ledger row exists"
  ([Embers] `docs/EPISTEMIC_TAXONOMY.md:171-173`). Applying "retracted" to single Ashes FAILs is therefore a historical
  gloss, not an Embers verdict.

### 6.3 (c) Live leads: do they identify the same ones independently?

| Ashes lead (salvage class F unless stated) | citation | Embers lead | citation | same idea? |
|---|---|---|---|---|
| H-L5 "Stick-slip at several normal stresses as the intended arc-regular class" (may explore) | [Ashes] `L-HYP.md:222` | stk1/stk2: S2 on Marone stick-slip runs at several loading rates | [Embers] `prereg/stk1/PREREG.md:19`; `prereg/stk2/PREREG.md:22` | **Same carrier class, different hypothesis.** Both converge on laboratory stick-slip as the right next carrier. Neither ran a test that scored |
| A1′ natural-time / own-clock: "A1′ robust unit lead"; held-out own-clock row SOTA1-3:crr-stepclock FAIL (TIE) | [Ashes] `L-MEM-CLK.md:511,516` | S2: memory indexed by occasion, q^(n−j); "untested, CRR-specific" | [Embers] `docs/TRANSFER_CANDIDATES.md:90-100` | **Related.** Both concern indexing by the system's own events. Ashes' single held-out learner test tied. Embers' physical test is VOID/pending |
| H-CUT via G-CD3/LIFE1 (DNA replication initiation at the antipode) | [Ashes] `L-HYP.md:511-512`; `L-RETRO-ONT-APP.md:413-414` | H1 on "neurons with von Mises tuning, strongly skewed waveforms, and multi-sensor encoders" | [Embers] `docs/TRANSFER_CANDIDATES.md:164` | **Same principle (A3), different operationalisations.** Neither was run |
| Bounded exponential memory moves thresholds (distributed-delay effect); 7 PRED70 A6 candidates | [Ashes] `L-RETRO-ONT-APP.md:386-391,414-415` | R2-28 ageing preferential attachment (PARTIAL); R1-10 paleoseismic memory (NOT DECIDABLE by design) | [Embers] `retro/REPORT_R2.md:45`; `retro/followup/R1_10_FEASIBILITY.md:32` | **Same family** (A6 as a delay kernel). Both judge it largely known |
| Secant units calibration (SEC); discriminating-subset tendency | [Ashes] `L-SEC.md:27-29,319,327` | — (SEC4 onward postdates 0edbc37; Embers read SCL3 as "a pass for a textbook method") | [Embers] `docs/EPISTEMIC_TAXONOMY.md:196` | Not shared |
| Normalised penalty step on online EWC; drifting-units niche | [Ashes] `L-EQ.md:423,433` | — (Embers: "S2 at most ... provisional pass for a normaliser") | [Embers] `docs/EPISTEMIC_TAXONOMY.md:195` | Not shared; same reading of reduction |
| Memory transport (O-MEM-5), Maps P5, reasoned-pause band | [Ashes] `L-MEM-CLK.md:227`; `L-PAUSE.md:245-246` | — | — | Not shared |
| — | — | H2 memory-coupled flow (gate OPEN; parity comparator binding) | [Embers] `notebook/AGENT_LOG.md:40` | Embers only (rotor) |
| — | — | First-passage IG interval law (R1-12), redesign as pooled likelihood | [Embers] `prereg/fire1/CLOSED.md:19-21` | Embers only (rotor) |

**Auditor's reading.**
- The independent convergence is on three things:
  - **the carrier class** (stick-slip);
  - **own-event indexing** (natural time / occasion-counted memory);
  - **the identifiability of the cut** (which phase or carrier), as the gating problem for A3.
- Neither repository has a G.

### 6.4 (d) Dead ends: do they identify the same ones independently?

| dead end | Ashes | Embers | agreement |
|---|---|---|---|
| Retrodictive consistency as evidence | "broad expressive coverage, which is redescription" ([Ashes] `L-RETRO-ONT-APP.md:19-20`) | "Consistency, which is not evidence" ([Embers] `retro/REPORT_R3.md:96`) | **Same**, reached on disjoint system sets: Embers' R1 declaration excludes systems already in Ashes' outputs (`retro/DECLARATION_R1.md:8-12`) |
| A6 where a domain accumulates or needs several timescales | "A6 is wrong wherever a domain accumulates" ([Ashes] `L-RETRO-ONT-APP.md:394`) | "A normalised A6 memory can average but never accumulate"; "one timescale" ([Embers] `retro/REPORT_R2.md:86-87`; `retro/REPORT_R3.md:115-116`) | **Same**, found independently on different systems |
| Antipode against domain trigger or extremum | "A3's antipode loses to domain triggers wherever the two differ" (R4) ([Ashes] `L-RETRO-ONT-APP.md:392`) | R2-03, R2-21 and R3-10 WRONG; "an extremum only under symmetric return" ([Embers] `retro/REPORT_R3.md:116`) | **Same at R4.** They diverge on what this implies for A3/H-CUT (D2) |
| CRR-specific parts of H-EQ | **A + C**; "No G" ([Ashes] `L-EQ.md:36-41,438`) | "Every CRR-specific part of H-EQ failed or reduced" ([Embers] `CRR_Ashes/README.md:216-217`) | **Same** (Embers reading Ashes) |
| H-L5 on measles and the pulse | **A** at the universal level ([Ashes] `L-HYP.md:127-136`) | "H-L5 fails on clock-regular systems" ([Embers] `CRR_Ashes/README.md:210-211`) | **Same** on the rows; they differ on propagation (D8) |
| Empty cut as CRR evidence | Construction; does not propagate ([Ashes] `L-PAUSE.md:29-30`) | "R0 in substance"; prior art ([Embers] `CRR_Ashes/README.md:62-70`) | **Same** |
| Universal constants and cross-domain transfer of σ, q, κ | — (RLAW tested one zero-parameter law and failed: [Ashes] `L-RETRO-ONT-APP.md:149-154`) | "CRR has no universal constants" ([Embers] `docs/TRANSFER_CANDIDATES.md:58-63`) | **Compatible.** Ashes found it by test (RLAW), Embers by audit of the axioms |
| The golden ratio / 1/φ | Kalman K(1) = 1/φ is "Standard mathematics" ([Ashes] `L-EQ.md:431`) | "a coincidence of the quadratic x² + x − 1, **not** a prediction" ([Embers] `Elegance/README.md:13`) | **Same** |
| Phase-defined event as circular | The Hilbert phase is non-causal and doubles on ECG-like beats ([Ashes] `L-HYP.md:427-436`) | MR-004; "Never derive the tested event from the phase" ([Embers] `CLAUDE.md:35-36`) | **Convergent** instrument lessons |

**Auditor's reading.** On dead ends the two repositories largely agree. The agreement is partly *independent*, where it
rests on disjoint retrodiction systems (A6, the antipode against extrema). It is partly *inherited*, where Embers is
reading Ashes rows (H-EQ, H-L5, the pause). The inherited agreements are not independent confirmations.

---

## 7 Question-10 evidence from Embers

| item | evidence | citation |
|---|---|---|
| Prompt → first held-out data | ≈ 3 h 38 min. Auditor's count (derived): 02:53:43Z → 06:32Z | [Embers] `notebook/PROMPT_LOG.md:22`; `notebook/AGENT_LOG.md:43` |
| Hash → data (batch 1) | ≈ 1 h 10 min. Auditor's count (derived): "~05:22Z" → 06:32Z; the anchor's earliest attestation was 05:35:13Z | [Embers] `reports/batch1.md:5`; `notebook/AGENT_LOG.md:37,43` |
| Idea → data (S2) | ≥ 5 h 12 min. Auditor's count (derived): prompt 16 "no later than 2026-09-27T19:1xZ" → stk1 data step 2026-09-28T00:31Z | [Embers] `notebook/PROMPT_LOG.md:130`; `runs/stk1/RESULT.md:7` |
| Gates closed before data | gate_h1 run 1 CLOSED, redesigned "by a rule on the TRUE generating law ... never on instrument output", run kept (entry 15). gate_h3 v1 CLOSED, replaced by a *more severe* v2 with a fresh-seed confirmation (entry 28). fire1 CLOSED on power (entry 38). R1-10 NOT DECIDABLE by design (entry 37) | [Embers] `notebook/AGENT_LOG.md:28,41,50-51` |
| Gate-required redesign not yet done | H2: "gate run 2 must first add a parity-aware linear comparator ... If POS then REDUCES, the gate is recorded as CLOSED" | [Embers] `notebook/AGENT_LOG.md:40` |
| Exploratory moves refused | Side-label mapping; a δ change after seeing 8 Hz; an xlook parser with re-scoring under stk1; guessing p5363's file name; pooling paleoseismic faults; relabelling retrodiction rows | [Embers] `reports/batch1.md:18`; `notebook/AGENT_LOG.md:43,59-60,50,47` |
| Exploration permitted | Unlimited same-day synthetic gates; three retrodiction batteries (100 systems) on 2026-09-27; Maths_Repair and Elegance; development on SEEN p4581 for loader parsing only | [Embers] `notebook/AGENT_LOG.md:45-57`; `retro/REPORT_R3.md:88-92` |
| Held-out data consumed without a hypothesis verdict | H1GAIT (whole zip), H1RESP (13 held-out units), stk1 (p5156). Auditor's count (derived): 3 of 4 scored real-data studies | [Embers] `notebook/AGENT_LOG.md:42-43,60` |
| The one FAIL's design maturity | Carrier chosen by a channel-count rule; prior "FAIL (P ≈ 0.80)"; Embers' own text says a PASS there could not validate the cut theorem | [Embers] `notebook/AGENT_LOG.md:33`; `prereg/h1card/PREREG.md:194`; `docs/DOMAIN_PORTFOLIO.md:361-363` |
| Rule that stopped more same-day tests | "no further primary claims are hashed on 2026-09-27" (batch m fixed at 3) | [Embers] `notebook/AGENT_LOG.md:39` (entry 26) |

**Reading (auditor's, both sides).**
- **Appropriately merciless.**
  - No FAIL, NOT DECIDABLE or VOID was rescued. Every rejected rescue is logged.
  - Gate redesigns made the instruments more severe, not less (H3 v2). They were declared before re-running.
  - The calibration gate protected held-out units in H1RESP from being scored on an unresolvable comparison.
- **Suppressive of exploration, in a specific sense.** The protocol did not stop ideas being explored synthetically: that
  was fast and productive (MR-004, the S2 power gates). What it stopped was **exploratory contact with real data before
  the hash**, since "no peek" covers file formats and schemas. The cost was paid in held-out records and in two
  plumbing-defined NOT DECIDABLE/VOID outcomes.

  Ashes shows the same structure:
  - "a header-only peek (opening data before the hash)" was rejected for LIFE1 ([Ashes] `L-HYP.md:544-545`);
  - "Infrastructure consumed held-out data" ([Ashes] `PROCESS.md:635-637`).
- **Too confirmatory too early, in one case.** H1's first real-data test came within hours of the rotor's adoption, on a
  carrier picked by admissibility. That mirrors Ashes' H-L5 history: carrier choice "followed availability and metric
  nativeness ... not prior plausibility" ([Ashes] `L-HYP.md:210-211`).

---

## 8 For Phoenix

### 8.1 Embers inheritance table (columns as the request names them)

| Lineage ID | Core CRR idea | Operationalisation(s) tried | Strongest supporting observation | Strongest negative evidence | Failure level | Current epistemic status | Mundane explanation | CRR-specific possibility | What Phoenix may explore | What Phoenix must never claim |
|---|---|---|---|---|---|---|---|---|---|---|
| E-H1 | A3: the cut at half a turn | Half the intrinsic Fisher arc of a fitted Gaussian Fourier law; causal phase; an independent event channel | gate_h1 OPEN (R4); MR-004 shows where the cuts can differ | Embers ledger row H1CARD-1 "FAIL" 0/19, not fragile, control holds | H1 for one (carrier, bridge) class (Embers blame table) | Held-out FAIL in one class; two NOT DECIDABLE (bridge) | The ejection-time lag sets the notch | The Fisher antipode marks an independently measured event on odd-harmonic-rich carriers | Carrier-selection rules (MR-002); exploratory checks on SEEN data of whether any Fisher antipode tracks any event before a hash; von Mises / skewed-waveform carriers | That H1 holds anywhere; that H1CARD refutes S1 universally; that H1RESP/H1GAIT bear on H1 |
| E-S2 | A6/P3 age counted in occasions; A1′ natural time | q^(n−j) memory; transfer across loading rates | s2_transfer_gate "DECIDABLE at κ = 0.2 for N ≥ 300" (R4) | Built-in false positive 64–70 % at κ = 0 (power gate); STK1-1 VOID | None reached (VOID) | Untested; stk2 pending at 7082f23 | Clock-time healing; no memory | Memory half-life scales inversely with event rate | Read Embers after 7082f23 for stk2; loader validation that does not count as exposure | Anything about S2 from stk1 |
| E-H2H3 | Memory-coupled flow; cost of detours | Driven rotor with κ tanh(m); bound Q·T ≥ ζ_min(a+2B)² | Gates OPEN (R4) | "a parity-aware linear model would probably tie it"; H3 "REDUCES 15/15" | R4 only | Synthetic | Ordinary feedback; thermodynamic length | None shown | The parity-comparator gate | That the bound or the gate is CRR evidence |
| E-RETRO | Embers laws, cut and memory across domains | Three declared batteries, 100 systems | 74 RD, 12 RIG | 9 WRONG; 0 clean ADDS (R2-28 PARTIAL, R2-16 ARTEFACT) | R4 (WRONG rows reach A3-as-Fisher-cut and A6 as domain models) | Redescription | Washboard/Adler, first passage, exponential smoothing | None shown | R2-28 for m ≥ 2 with an expert; a pooled fire design under its own gate | Any count from the batteries as support; "consistent with 74 of 100" as evidence |
| E-MATH | Coherence of the formalism | Tests, independent checks, an adversarial audit | 35 tests; DEFECT 11 → 0 | MR-002 (carrier relativity), MR-003 (P3 scope) | Mathematical | Gaps OPEN | — | — | A principle that fixes the carrier; P3 wording | Elegance entries as evidence; 1/φ as a constant |
| E-INH | Lessons from Ashes | — | Fact-checked audit | — | — | Priors, not verdicts | — | — | Re-read the Ashes rows at Phoenix's own levels | Any Embers row as Ashes evidence, or any Ashes row as Embers evidence |

### 8.2 Open questions Phoenix inherits from Embers

1. **Which observation law defines the cut?** (MR-002, OPEN.) Until it is fixed, every Fisher-arc cut claim is relative to
   an instrument. This is the same identifiability gap Ashes records for the phase (D1, D2).
2. **Intrinsic or ambient chord** for D3 and P1 (D6). It changes whether a monotone occasion has zero surplus.
3. **Is the seed separate from the phase?** (D4.) An owner decision, flagged by Embers as "Any change to the original
   axioms must be reviewed explicitly" ([Embers] `README.md:72-73`).
4. **σ in Fisher-length units** (D7). One SEEN-data rerun under both units would show whether it matters.
5. **S2's real-data outcome** (stk2), if Embers ran it after 7082f23.

### 8.3 Must never claim (from the Embers record)

- That any Embers row is a PASS, or that the Embers ledger confers status on any Ashes row or the reverse
  ([Embers] `ledger/LEDGER.md:9-10`).
- That the rotor's laws of motion are a CRR prediction. Embers calls them constitutive and inherited
  ([Embers] `README.md:7-8`; `retro/REPORT_R2.md:78-80`).
- That retrodictive consistency (Ashes or Embers) is evidence. Both repositories say it is not.
- That "the antipode is refuted" or "domain events sit at extrema" as a general finding. In either repository, that rests
  on R4 rows and one held-out FAIL of a *different* hypothesis (H1).
- That NOT DECIDABLE or VOID rows bear on any hypothesis.
