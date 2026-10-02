# PRE-PHOENIX INTERPRETIVE AUDIT — NO VERDICTS ALTERED; ADDENDUM: Embers unmerged branch claude/eager-allen-5rjiem read at de6c05a (post hoc to the declaration, which named 7082f23)

**Status.** Reader notes, not evidence (R8). They change no verdict, ledger row or log in either repository. They extend
`notes/EMBERS_CROSS_AUDIT.md`, which read Embers only at `main` 7082f23. This reading is **post hoc to the declaration**:
`Pre_Phoenix_Audit/DECLARATION.md:23` names "a shallow clone of commit 7082f23 (2026-09-28)". The later branch was found
after the cross-audit was written.

**Conventions.**
- **[Embers@de6c05a]** is `/home/user/embers_branch`, a read-only checkout of `claude/eager-allen-5rjiem` at de6c05a
  (2026-10-02T00:01:54Z). **[Embers@7082f23]** is `/home/user/embers_crr`. **[Ashes]** is `/home/user/ashes_crr` on
  2026-10-02. Nothing in either Embers checkout was modified or run; only `git log`, `git show`, `git cat-file`,
  `git merge-base`, `grep`, `sed` and `ls` were used.
- Each repository's verdicts are quoted in its own words and labelled. No Embers verdict is restated as applying to an
  Ashes row, and no Ashes verdict as applying to an Embers row.
- **Auditor's count (derived)** and **auditor's reading** mark anything I computed or interpreted. The method is stated.
- **Line numbers in `PRE_PHOENIX_AUDIT.md`** are as read on 2026-10-02 (§9 at lines 633–764). The file was being edited
  while I read it (an earlier read put §9 at 611–742), so §9 statements are also identified by quoted text.
- Salvage classes A–G are those of prompt-log entry 260 ([Ashes] `notebook/PROMPT_LOG.md:1928-1985`).

---

## 0 Summary

1. **What exists.** `git log 7082f23..HEAD` on the branch lists 72 commits, from d853f0d (2026-09-29T00:12:44Z) to
   de6c05a (2026-10-02T00:01:54Z) (auditor's count, derived: `git log --oneline 7082f23..HEAD | wc -l`). The branch
   merges `main` 7082f23 (279cb1d), so it contains everything the cross-audit read. `main` does not contain the branch.
2. **Ledger.** 10 new rows: STK2-1/S/C and ESEC2-1/2/3/K/K2/D/S. The total is 22 (auditor's count, derived: `grep -c` of
   row lines in [Embers@de6c05a] `ledger/LEDGER.md`). STK2-1 is "**VOID**". ESEC2-1 is "criterion met; **no rung**";
   ESEC2-2 and ESEC2-3 are "FAIL, FRAGILE". No row carries a PASS-0/1/2 rung. One secondary row, ESEC2-D, reads
   "PASS (secondary)" ([Embers@de6c05a] `ledger/LEDGER.md:40,45-51`).
3. **Baseline CRR.** No new Embers ledger row tests a hypothesis stated in [Ashes] `theory/CRR.md`. STK2 is VOID, and
   ESEC2 tests the frozen SEC4 rule, "not a CRR rule" (`ledger/LEDGER.md:44`). Cross-audit statement (a) stands. Its
   wording should now cite STK2 as VOID instead of "pending".
4. **The SEC criterion: independent convergence under a blind.** On 2026-09-30, about 3 minutes apart, both repositories
   found that SEC4-1's "not behind the tuned λ" criterion is met by a constant or a learner frozen after task 1:
   - [Embers@de6c05a] ESEC1 closed on CP1, d11c9db at 09:41:14Z;
   - [Ashes] FM6 FAILS, 34b4765 at 09:38:11Z.

   Both traced the cause to the class-ordered loader. Both then registered a constant or frozen-learner arm before
   held-out data, and on held-out data it met the criterion: [Embers] ESEC2-K 8/10 and ESEC2-K2 10/10; [Ashes] SEC6R-G
   "edge not behind on 8/9". The records show no read across the blind; §4.1 gives the limits of that independence.
5. **Kalman / Ω = 1: the same conclusion, but primed.** Stage K agrees with Ashes L-EQ: Ω = 1 does not select a weight,
   K(1) = 1/φ is textbook, and the rest is adaptive filtering. But its input was another chat's re-reading of Ashes'
   own Ω = 1 material (AGENT_LOG 88), so the agreement is inherited. Embers adds three things:
   - whiteness, not NIS, selects the gain;
   - "speed matching" is lag-1 whiteness in 1-D and fails as a full-matrix criterion in 2-D;
   - the scoring target decides more than drift does.
6. **Pause and robotics.** These are new, independent and convergent with Ashes. Both find:
   - no CRR candidate in robotics;
   - no support for coupling SEC with HopDC-type transport and the pause;
   - a pause can be empty only if the world is held still.

   Embers adds a sharper textual point: the *literal* A3 cut text ("settles … resets C") is a pause **breaker** (new
   disagreement D12).
7. **New record defects.**
   - Embers' tag-signing key file is empty. It was already empty at 7082f23, and the cross-audit missed it.
   - AGENT_LOG entries 57–61 and prompt-log entries 25–26 exist in two different versions, on this branch and on
     unmerged `claude/pensive-johnson-2c76xr`.
   - Embers reports a label leak in an Ashes SEC4-1 carrier (cardiotocography). Ashes' record does not mention it.
   - Records Embers opened (PSU p5156 and p5565, the ESEC2 carriers) are absent from [Ashes] `data/SEEN.md`.

---

## 1 Everything new after 7082f23

### 1.1 Branches seen

| branch / ref | head | relation to de6c05a | what bears on verdicts |
|---|---|---|---|
| `claude/eager-allen-5rjiem` | de6c05a | read here | everything below |
| `main` | 7082f23 | ancestor (merged at 279cb1d) | already in the cross-audit |
| `claude/pensive-johnson-2c76xr` (PR #13) | 80811db, 2026-09-29T01:47:09Z | **not an ancestor** (`git merge-base --is-ancestor 80811db HEAD` false; also e8fcd05 false). It contains d853f0d..6586466 (stk2 VOID), and those are in de6c05a | No new verdict. It carries a **different** AGENT_LOG 57–61 and prompt-log 25–26 (§1.6) |
| `audit/detector-nonanticipation-gate` (PR #12) | 1450037, docxology, 2026-09-28T17:23:33-07:00 | not an ancestor | It finds the frozen h1card detectors "DETECTED" as leaking post-cutoff content (commit message). Embers' review: "The verdict is right; the printed evidence hides it … None of this affects a registered result (every H1 study is FAIL or NOT DECIDABLE)" ([Embers@de6c05a] `notebook/AGENT_LOG.md:71`, entry 58) |
| `audit/readability-fixes` | not read | — | not read; no verdict expected |

### 1.2 New ledger rows, verbatim (columns: id | observed | per-unit | verdict)

From [Embers@de6c05a] `ledger/LEDGER.md:39-51`. Anchors are given once per study; the full cells are in the file.

**Study stk2** (`:39`): "registered 2026-09-28, m = 1; successor of stk1; S2 occasion-counted ageing, laboratory
stick-slip, unit p5565". Anchor: "OTS Bitcoin anchor 2026-09-28T05:11:26+00:00, block 968945, verified
2026-09-29T00:12:43Z before data".

| id | observed | per-unit | verdict |
|---|---|---|---|
| STK2-1 (`:40`) | "unit VOID: npz "missing columns ['time', 'shear_stress', 'lp_disp'] in ['allow_pickle', 'arr_0']" (one unnamed array); csv fallback "0 header lines carry the required column names (need exactly 1)"" | "0/1 units loadable" | "**VOID**" |
| STK2-S (`:41`) | "0 of 8 cells differ (all VOID)" | — | "sensitivity: not informative (all VOID)" |
| STK2-C (`:42`) | "SHUF VOID" | — | "control not evaluable" |

**Study esec2** (`:44`): "registered 2026-09-30, frozen 18:41Z; successor of ESEC1, which closed at its controls gate
before data; the frozen SEC4 rule, unchanged, run by this machine; not a CRR rule". Anchor: "OTS Bitcoin anchor
2026-09-30T19:46:27+00:00, block 969342, verified 2026-10-01T01:22Z before data …; signed tag prereg-esec2-2026-09-30 NOT
VERIFIED in this container …; beacon block 969374; data step after the R3 embargo". Dataset: "10 admissible fresh OpenML
carriers, beacon-drawn from ESEC1's 41-id pool (18 opened …)".

| id | prediction (abridged) | observed | per-unit | verdict |
|---|---|---|---|---|
| ESEC2-1 (`:45`) | "frozen SEC4 (clipped SEC) not behind SEC4-1's explicit tuned λ sweep (V0g) by one resolvable step"; threshold "≥ ⌈0.75 N⌉ = 8 of 10" | "9/10 (ahead/tie/behind 2/7/1)" | "9/10" | "criterion met; **no rung**: tag signature not verified; and the constants V5s (8/10) and ISO (10/10) also meet this criterion, so the row cannot be PASS-1; its family partner ESEC2-2 FAILs" |
| ESEC2-2 (`:46`) | "frozen SEC4 not behind a capacity-matched stabilised λ sweep (V5g, clip, same 17-configuration search)" | "5/10 (0/5/5)" | "5/10" | "FAIL, FRAGILE (4 flips in the PASS-1 table)" |
| ESEC2-3 (`:47`) | "the secant: frozen SEC4 ahead of raw Laplace + clip (V3) by V3's own step" | "4/10 (4/6/0)" | "4/10" | "FAIL, FRAGILE (3 flips)" |
| ESEC2-K (`:48`) | "constant reduction: the saturated clip V5s under ESEC2-1's criterion" | "8/10 (7/1/2)" | "8/10" | "MEETS (a single constant configuration meets row 1's criterion)" |
| ESEC2-K2 (`:49`) | "constant reduction: ESEC1's isotropic cap (s = 1e6) under ESEC2-1's criterion" | "10/10 (8/2/0)" | "10/10" | "MEETS (a single constant configuration meets row 1's criterion)" |
| ESEC2-D (`:50`) | "no frozen-SEC4 seed below half the tuned accuracy" | "none" | "10/10" | "PASS (secondary)" |
| ESEC2-S (`:51`) | "SEC4's window cells (fragility)" | "0 of 30 flips" | — | "not fragile (secondary)" |

The scorer's own printout reads "ESEC2-1 … 9/10 (need 8) -> PASS" and "RUNG ESEC2-1: no rung (tag signature not verified
…)" ([Embers@de6c05a] `runs/esec2/score.txt:332,345`). The ledger cell carries the rung text.

Report-only lines beside the verdicts:
- "balanced per-task accuracy …: row 1 version 10/10 -> MEETS the criterion; row 2 version 7/10 -> does not meet the
  criterion; ESEC2-K version 4/10 -> does not meet the criterion" (`runs/esec2/score.txt:344`).
- The walk "39 ids walked, 18 opened (SEEN), 10 admissible" (`:11`). Auditor's count (derived, `:12-50`): of the 18
  opened, 8 were excluded after opening: 2 "leak-flagged", 3 "not learnable", 3 by the "class rule".

### 1.3 Prompts 25–42 ([Embers@de6c05a] `notebook/PROMPT_LOG.md:172-441`)

| entry | time ("no later than") | gist, quoted where short | directed work |
|---|---|---|---|
| 25 (`:172`) | 2026-09-29T01:23:47Z | "check the Issues folder again" | issues #7–#11, PR #12 review (AGENT_LOG 57–58) |
| 26 (`:176`) | 2026-09-29T03:0xZ | "Please advise accordingly." | none |
| 27 (`:182`) | 2026-09-29T02:3xZ | post in Issues and tag Daniel | AGENT_LOG 60 |
| 28 (`:186`) | 2026-09-29T02:4xZ | "run 100 new pre-registered predictions on new systems" | battery R4 |
| 29 (`:190`) | 2026-09-29T15:03:28Z | "how wrong is that" | none |
| 30 (`:196-235`) | 2026-09-29T15:28:00Z | "From gpt6": R4 as an "applicability map"; "Predicting a label for a system selected because its law is already known is prospective classification of known mathematics, not a held-out prediction of nature" (`:222`) | none (assessment in chat) |
| 31 (`:237-239`) | 2026-09-29T19:44:11Z | "more checks on the SEC finding" in ashes_crr | `audits/sec4/` (AGENT_LOG 63) |
| 32 (`:241-243`) | 2026-09-29T22:19:10Z | more checks on the "Empty True Map" pause | EP1–EP5 (AGENT_LOG 64–69) |
| 33 (`:245-247`) | 2026-09-30T00:54:04Z | verify ashes SEC5 | `audits/sec5/` (AGENT_LOG 70) |
| 34–35 (`:249-264`) | 2026-09-30T01:05–01:13Z | "What has worked with SEC4"; "5–7 % of the sweep's CPU" | none |
| 36 (`:266-286`) | 2026-09-30T01:48:16Z | SEC4 PASS-1 write-up, "brochure style", "commercial case", "Highlight that one *metaphysical* heuristic has enabled this finding" (`:284`) | `Findings/SEC4_PASS1/` (AGENT_LOG 71) |
| 37–38 (`:288-302`) | 2026-09-30T02:59–05:28Z | link; "check ashes for the latest updates" | read of 64 ashes commits (snapshot 989e4d8) |
| 39 (`:304-330`) | 2026-09-30T07:17:16Z | the week programme, identical to [Ashes] prompt-log 257 except for an added blind clause: "At the end of the week we will compare the two sets of findings (don't look until then)" (`:326`) | stages A–I; `BLIND_COMPARISON.md` (AGENT_LOG 72) |
| 40 (`:332-336`) | 2026-10-01T14:46:41Z | short update | none |
| 41 (`:338-390`) | 2026-10-01T21:15:49Z | a "fresh Claude 5.1 chat" analysis of ashes' Ω = 1 / Kalman material; "calibrated surprise" | stage K (AGENT_LOG 88) |
| 42 (`:392-441`) | 2026-10-01T21:40:08Z | "speed matching" and a "budget of change" | stage K strands k5/k6 (AGENT_LOG 89) |

**Note on the blind's asymmetry.** [Ashes] prompt-log 257 (`notebook/PROMPT_LOG.md:1787-1807`, 2026-09-30T07:11:08Z) has
the same programme text, with no "don't look" clause. So Ashes was under no recorded blind. The only evidence that Ashes
did not read Embers is an absence: an auditor's `grep -i embers` of [Ashes] `notebook/AGENT_LOG.md` and
`notebook/PROMPT_LOG.md` finds no Embers mention before entry 260.

### 1.4 AGENT_LOG entries 55–91 ([Embers@de6c05a] `notebook/AGENT_LOG.md:68-104`; entry n at line n + 13)

| entry | date | substance (quoted or closely paraphrased) |
|---|---|---|
| 55 | 09-29 | stk2 anchor verified "Bitcoin block 968945 … before the fetch" |
| 56 | 09-29 | stk2 VOID; "No column guessing or loader change after exposure"; "All verified multi-velocity PSU candidates (p5156, p5363, p5565) are now SEEN; S2 remains untested" |
| 57 | 09-29 | issues #7–#11; #10: the h1card/h1gait fetch logs were "recovered originals, not reconstructions" |
| 58 | 09-29 | PR #12 review: "in which the frozen detectors lose all pre-cutoff fiducials (39 → 0 on each of 3 seeds …)" |
| 59 | 09-29 | H2 gate run 2: "**GATE OPEN**, 21/21"; but `parity_free` "ties crr in every POS unit (0/0/12 on all seeds …)"; "CRR's advantage over a parity-aware linear model is worth about one fitted parameter. The minimum detectable κ rises from 0.4 to 0.6" |
| 60 | 09-29 | issue comments, PR to main (not merged as of `main` 7082f23) |
| 61–62 | 09-29 | battery R4 declared, anchored (block 969093), run once; "Tally: 51 REDUNDANT-DOMAIN, 46 WRONG, 3 REDUNDANT-IG"; commit 206be3b's message "is wrong, and this entry corrects it" |
| 63 | 09-29 | `audits/sec4`, read at ashes 9fd07d5: "SEC4-1 reproduces exactly (6/6)"; "four arms reach it (clip 6/6, G-SCALE 6/6, G-RAW 5/6, CRR rule Omega=1 5/6); no fixed lambda or fixed calibrated weight in the files reaches 5/6" |
| 64–69 | 09-29 | EP1–EP5 (pause stakes). EP1 B1 "expectation missed"; EP2 C1 missed at declared settings; EP3 and EP3b "closed" on failed controls; EP4 and EP5 "All expectations held" |
| 70 | 09-30 | `audits/sec5`: "SEC5-1 4/8 FAIL reproduced exactly"; "(a) on 6 of 8 SEC5 carriers no arm learns above the majority share"; "(b) SEC4's cardiotocography carrier leaks its label (V26-V35 one-hot encode Class; agreement 1.000000 …)" |
| 71 | 09-30 | Findings/SEC4_PASS1: "Tension recorded: … only a PASS-2 may be quoted outside the ledger as a finding, and SEC4-1's replication SEC5-1 FAILED" |
| 72 | 09-30 | the blind: last ashes state read "origin/main 45cd4af; branch snapshot 989e4d8, committed 05:25:10Z; last fetch 05:27:08Z; all before the prompt" |
| 73 | 09-30 | ESEC1 CLOSED: "The registered must-pass control CP1 FAILED"; "SEC4-1's criterion cannot tell calibrated SEC from a constant penalty at the stability limit on that stream" |
| 74, 76 | 09-30 | stage A: PR1–PR7 frozen at 08:34:11Z; the "amendment's text was finished after results had begun to appear"; synthesis findings "MEASURED-SEEN, post hoc; no PASS possible"; entry 76 "supersedes AGENT_LOG 73's description of that arm" |
| 75 | 09-30 | stage E: "a register of 77 bottlenecks"; "694 of 700 quotes were found verbatim again" |
| 77, 79 | 09-30 | stage C: designs, then checks; "None of the six declared SIMULATED checks met its declared expectation"; "The literal CRR cut … broke pause identity in 100/100 runs"; "The declared run order was breached … The order breach is the lead's error" |
| 78, 80 | 09-30 | ESEC2 design: "ESEC2-K … if it also meets it, a PASS of ESEC2-1 is recorded as 'constant reduction NOT excluded'"; "**no PASS rung can be printed in this container**" (tag unverifiable) |
| 81 | 09-30 | stage D: "Every CRR-proper learning rule failed held-out, reduced to a known rule, or closed at its gate"; the brochure's "17" safety constructions should read "5" |
| 82 | 09-30 | stage F: "SILENT 60, TRANSLATES 13, RESTATES 3, DISAGREES 1 (RB-31 …), CANDIDATE 0" |
| 83 | 10-01 | ESEC2 anchor verified; a registered `machine_record.py` step "was not run" at the freeze; written at 01:22Z and "labelled late" |
| 84 | 10-01 | ESEC2 scored: "'tuning-free' holds only against a divergence-limited comparator" |
| 85–86 | 10-01 | stage G declared, then "The harness gate EG0 CLOSED, so EG1–EG5 did not run"; "The defects are the declaration's (one impossible control, an unstable learner)" |
| 87 | 10-01 | stage H: "**The committed key files are empty, although AGENT_LOG 25 says the key was committed, and the remote holds 0 tags.**" Corrected by this entry, "which supersedes AGENT_LOG 25's claim" |
| 88 | 10-01 | the blind note on prompt 41 (§4.2) |
| 89–91 | 10-01/02 | stage K strands; EKS declaration hash recorded before any run; "EKS1 CLOSED"; EKS2 ran "with a flag: its CPU-gate rule was changed after development timing but before the scored run" |

### 1.5 Stages B–K at a glance ([Embers@de6c05a] `Applied_Suite/README.md:52-63`)

| stage | rung (Embers' own label) | outcome quoted |
|---|---|---|
| A (why SEC4 worked) | "MEASURED-SEEN … exploratory, post hoc, never held-out evidence" (`A_sec4_why/REPORT.md:3-5`) | "the secant carried SEC4; the clip only guarded stability; SEC4-1's comparator could diverge; a constant also meets its count (by staying on task 1); SEC5's failure has three confounded accounts; no CRR-specific ingredient" (`README.md:54`) |
| B (ESEC1, ESEC2) | ESEC1 closed before data; ESEC2 held-out | ledger rows above |
| C (SEC × HopDC × pause) | SIMULATED | "no simulated support for coupling SEC or HopDC; the product baseline T0 uses neither; the pause contract and its breakers are the usable output" (`README.md:56`) |
| D (CL applications) | analysis note | "every CRR-proper rule failed or reduced; the product core (T0) uses no CRR ingredient" (`:57`) |
| E (robotics bottlenecks) | literature | "77 robotics and drone bottlenecks, each with at least two independent verified sources" (`:58`) |
| F (CRR readings) | classification | "SILENT 60, TRANSLATES 13, RESTATES 3, DISAGREES 1 …, CANDIDATE 0" (`:59`) |
| G (drone checks) | SIMULATED | "harness gate EG0 CLOSED (declared learner unstable; one must-fail control impossible); EG1–EG5 not run" (`:60`) |
| H (trust and security) | analysis | "audits do not stop poisoning; rollback and spoofed press unaddressed … empty key files, single author, local-history append-only check; CRR vocabulary only" (`:61`) |
| K (Kalman / Ω = 1) | DERIVED / SIMULATED / LITERATURE | "whiteness is what selects the gain; textbook (adaptive filtering), not CRR; EKS1 closed, EKS2: calibrated surprise helps only for fast drift on the latest-task target and loses to plain counting on the all-tasks target" (`:62`) |
| I (suite) | — | "not started" (`:63`) |

### 1.6 Record defects and other material items

1. **The tag-key defect** ([Embers@de6c05a] `notebook/AGENT_LOG.md:100`, entry 87; `Applied_Suite/H_trust_security/REPORT.md:74-81`).
   - `docs/keys/tag_signer_ssh.pub` is 0 bytes. AGENT_LOG 25 says "Committed the SSH public key"
     (`notebook/AGENT_LOG.md:38`).
   - Signatures are "valid for the key embedded in the signature, all from one key", which is "the platform's generic
     commit-signing key" (`H_trust_security/REPORT.md:74`). "The remote has 0 tags" (`:81`).
   - Auditor's check: `ls -la /home/user/embers_crr/docs/keys/` shows `tag_signer_ssh.pub` at 0 bytes at 7082f23 too,
     last touched by c5af86b (2026-09-27T05:23:16Z). **The cross-audit missed this** (its §5.1 "Signed tags" row).
   - The STK1-1 and STK2-1 ledger cells name signed tags without a "not verified" note (`ledger/LEDGER.md:35,40`). Auditor's reading: after entry 87 those tags are equally unverifiable against a
     registered key. Embers' strong anchor, the verified OTS proof, is unaffected.
2. **Divergent append-only logs across branches.** On 80811db (PR #13), AGENT_LOG 57–61 record the issue #7 decisions,
   and prompt-log 25–26 are "Please can you check the latest Issues folder…" (≤ 2026-09-28T23:43:04Z) and "Please can you
   make sure the neccessary fixes are made?" (`git show 80811db:notebook/PROMPT_LOG.md`, entries 25–26). On de6c05a the
   same numbers carry different entries (§1.3, §1.4). Embers foresaw this hazard: "merging such a branch into `main`
   fails `scripts/check_append_only.py` whichever way the conflict is resolved" (`notebook/AGENT_LOG.md:67`, entry 54).
   Auditor's reading: until one line is merged, each log is complete only on its own branch.
3. **A label leak in an Ashes SEC4-1 carrier, as Embers reports it.** "OpenML 1466 (cardiotocography, a SEC4 held-out
   carrier) contains ten binary columns, V26–V35. Each equals the indicator of one of the ten classes in 100 % of the
   2126 rows (agreement 1.000000)"; "Without the carrier, SEC4-1 is 5/5 (need 4)"; "it is an admissibility defect"
   ([Embers@de6c05a] `audits/sec5/README.md:52-61`).
   - Auditor's search: `grep -rni` of [Ashes] `*.md`/`*.txt` for "label leak", "leaks its label" and "one-hot encode"
     finds no Ashes record of this.
   - [Ashes] P1's frozen learner M6 is behind the tuned λ only on cardiotocography (−44.0566;
     `SEC_Analysis/WHY_SEC4_WORKED.md:41-42`).
   - Auditor's reading (derived from those two quoted lines): without the leaky carrier, [Ashes] SEC4-1-G's "M6 not
     behind the tuned λ on 5/6 (need 5)" becomes 5/5 against a need of 4, so the gate would still close. This is not a
     re-score; it is for Phoenix to verify.
4. **Exposures absent from Ashes' SEEN.** p5156 and p5565 were opened by STK1 and STK2. The ESEC2 walk opened 18 OpenML
   ids, and stage A downloaded 30 ([Embers@de6c05a] `data/SEEN.md:117,119,124-125`). An auditor's `grep -c` of
   [Ashes] `data/SEEN.md` returns 0 for p5156, p5363, p5565 and each ESEC2 carrier name. Ashes R11 defines held-out
   against records opened "in any prior CRR work". Auditor's reading: Phoenix must treat these as SEEN.
5. **Stale "not committed" text in committed reports.**
   - [Embers@de6c05a] `Applied_Suite/K_kalman_equanimity/REPORT.md:12,263` say that the EKS scripts and outputs are
     "untracked". `git show --stat de6c05a` lists them as committed in that same commit.
   - `Applied_Suite/G_robotics_tests/REPORT.md:7` and `Applied_Suite/F_robotics_crr/REPORT.md:10` say "Nothing was
     committed or pushed". Both files are committed (093f3e8; 37d5d7a).
   - Both are information-level defects.
6. **Declared-check closures traced to the declarations themselves.**
   - EKS1: "That was computable from the declared text before the run" (`K_kalman_equanimity/REPORT.md:159`).
   - EG0: "F0-3 … could not have been" met, "derived and logged before the run" (`notebook/AGENT_LOG.md:99`).
   - ESEC1 CP1: "The outcome was knowable before CP1 was chosen" (`prereg/esec1/CLOSED.md:21`).
   - EKS2: "flag F1": the CPU rule was changed after development timing; under the original rule it would have been
     "NOT RUN" (`K_kalman_equanimity/REPORT.md:197-201`).

---

## 2 New lines of inquiry: four layers, salvage class, bearing on baseline CRR

Stable IDs continue the cross-audit's (`EMBERS_CROSS_AUDIT.md:202-208`). New IDs: **E-SEC**, **E-PAUSE**, **E-KAL**,
**E-ROB** (with stages D, E, F and H).

### 2.1 E-S2 update: stk2 VOID

| (1) observed | (2) rotor/CRR interpretation | (3) ordinary explanation | (4) what would distinguish |
|---|---|---|---|
| STK2-1 "**VOID**": one unnamed npz array; csv without the required header (`ledger/LEDGER.md:40`). "S2 remains untested" (`docs/TRANSFER_CANDIDATES.md:256`) | none | file format; "The metadata read before the freeze … could not show whether the files had column labels" (`runs/stk2/RESULT.md:18-20`) | "a stick-slip dataset with documented column names or a data dictionary, checked from its documentation before the freeze; at least two loading rates at least 5× apart; at least 300 events per rate" (`runs/stk2/RESULT.md:25-29`) |

- **Class:** **D** (data access). Propagation level: none.
- **Bears on:** potentially baseline A6/P3 (occasion-indexed ageing) and A1′ (natural time), had it run. As run, nothing.
- Every verified multi-velocity PSU run is now consumed: "All three PSU runs are now SEEN" (`TRANSFER_CANDIDATES.md:260`).

### 2.2 E-SEC: audits/sec4, audits/sec5, stage A, ESEC1, ESEC2, Findings

| observation | (1) observed | (2) CRR interpretation | (3) ordinary explanation | (4) what would distinguish |
|---|---|---|---|---|
| audits/sec4 (pre-blind) | "The SEC4-1 threshold is not specific to the clip … the registered CRR rule Ω = 1, 5/6"; "no fixed λ on the coarse grid … reaches it (best: λ = 30, 4/6)" (`audits/sec4/README.md:29-41`) | — | a lenient non-inferiority bar | a constant outside those files (found later: V5s) |
| stage A (SEEN, post hoc) | "On these carriers the secant carried SEC4; the clip only guarded stability" (`A_sec4_why/REPORT.md:47`); the constant V5s "meets SEC4-1's count on P1 (5/6), P2 (7/8) and P3 (12/16) … by predicting mostly task-1 classes and giving up the last task" (`:57-59`) | "SEC4's arm contains no CRR-specific quantity" (`:72`) | the Laplace weight plus a units rescale plus a stability guard; a class-ordered loader rewards staying on task 1 (`:213-217`) | a stream and metric on which a must-fail constant fails |
| ESEC1 | "CP1, must-pass: FAILED"; "the criterion SEC4-1 used cannot tell calibrated SEC from a constant penalty set at the stability limit" (`prereg/esec1/CLOSED.md:18,39-40`) | — | a control chosen without checking SEC4's own development output (`:21-23`) | — (closed before data) |
| ESEC2 (held-out) | rows 1 "9/10" no rung, 2 "5/10" FAIL, 3 "4/10" FAIL; K "8/10" and K2 "10/10" MEETS (§1.2) | "not a CRR rule" (`ledger/LEDGER.md:44`) | "'tuning-free' holds only against a divergence-limited comparator" (`notebook/AGENT_LOG.md:97`) | ESEC2-3's secant comparison on a criterion constants cannot meet. Balanced accuracy is a candidate: V5s "4/10" there (`runs/esec2/score.txt:344`), a report, not a verdict |
| Findings/SEC4_PASS1 | brochure at the owner's request; standing "a single-family PASS-1 that did not replicate, not a finding" (`notebook/AGENT_LOG.md:84`); stage D correction "Read that PDF sentence as '5 of 17'" (`Findings/SEC4_PASS1/README.md:42`) | "CRR was the heuristic that led to it" (`:20-21`) | — | — |

- **Class:**
  - **C** for SEC as a method: "textbook mechanism" (`Applied_Suite/README.md:57`).
  - **A (method level)** for ESEC2-2 and ESEC2-3 against SEC's held-out "tuning-free" and secant claims.
  - **D/E (instrument)** for ESEC2-1, since constants meet its criterion.
  - **F (weak)** for the secant on SEEN data: 6/0/0 against raw Laplace + clip (`A_sec4_why/REPORT.md:127`). It did not
    replicate held-out (ESEC2-3 4/10).
- **Bears on:** nothing in [Ashes] `theory/CRR.md`. Stage A's CRR predictions PR1 and PR6 were "FALSIFIED"
  (`A_sec4_why/REPORT.md:304-307`). These are readings frozen at 08:34:11Z on SEEN data, not CRR.md hypotheses.

### 2.3 E-PAUSE: EP1–EP5, stage C, stage G, RB-31

| observation | (1) observed | (2) CRR interpretation | (3) ordinary explanation | (4) what would distinguish |
|---|---|---|---|---|
| EP1 | bound "held in 200 of 200 random MDPs"; B1 queue "**−0.53 to −0.22 at backlog 0–3**" (seeks the pause); B1f buffered "0 in 21/21" (`audits/empty_pause/README.md:21,32-33`) | the empty cut needs zero content | "Zero content is a property of the whole system, not of the agent" (`:51`); "standard dynamic programming" (`:8`) | — (exact value iteration; "The labels are forced; the numbers are the information", `:58`) |
| EP3, EP3b | "closed": in moving worlds "value-estimation noise exceeds the 0.05 disable cost, so agents with no stake still disable" (`notebook/AGENT_LOG.md:80`) | — | learning noise | a declaration that sets the disable cost against a measured error bound first (same entry) |
| stage C, SPLIT | "A3's cut 'partitions the history …; settles the occasion just completed …; resets C to zero'. For this learner, that is consolidation, which is breaker (a)"; T1-SPLIT differed "in 100 of 100 runs" (`C_coupling/REPORT.md:204-206`) | a literal-A3 learner breaks the pause | a commit at the press is ordinary state mutation | — (a construction check; "It says nothing about CRR as physics", `:206`) |
| stage F, RB-31 | "RESTATES to DISAGREES … The '100 of 100' in stage C reduces to 5 distinct runs per tier"; "The conflict holds only if an interruption is modelled as a cut" (`F_robotics_crr/REPORT.md:25-28`) | — | — | — |
| stage G, EG0 | P0-5 in config M "4.691–4.901, **0/10 → NOT met**" (`G_robotics_tests/REPORT.md:89`) | — | a declared RLS learner that diverges | the successor EG-b, "no earlier than 2026-10-02" (`notebook/AGENT_LOG.md:99`); not run at de6c05a |

- **Class:**
  - **C** (construction, known dynamic programming) for EP1, EP2, EP4, EP5 and the pause contract.
  - **D** for EP3, EP3b and EG0, closed on controls or harness.
  - **F (R4, not CRR-specific):** the stake sizes and the lease sizing rule, "the lease … covers the tail, not the mean"
    (`notebook/AGENT_LOG.md:81`).
- **Bears on:** not on any CRR.md hypothesis. On wording, SPLIT and RB-31 bear on whether the empty pause is a reading
  of A3 at all (D12 below).

### 2.4 E-KAL: stage K (Kalman / Ω = 1)

| observation | (1) observed | (2) CRR interpretation | (3) ordinary explanation | (4) what would distinguish |
|---|---|---|---|---|
| fixed Ω gains | "K = 1/φ is optimal only at v = 1 and K = 1/2 only at v = 1/√2 … unbounded on both sides" (`K_kalman_equanimity/REPORT.md:21`) | Ω = 1 as "Fisher speed 1" or "equal pull" | steady-state Riccati (P4 labelled textbook in CRR.md) | — (DERIVED) |
| equal pull | "The precision-weighted pulls cancel at every optimal Kalman update … Unweighted equal pull picks a constant: K = 1/2, or λ = 1" (`:22`) | equanimity as balance | the first-order condition at any minimiser | — |
| what selects | "whiteness, not NIS"; NIS = 1 family member "7.39× worse" (`:23-24`); speed matching "In two or more dimensions … rotated gains … 213× worse at 85°" (`:26`) | "calibrated surprise" | Mehra; Myers–Tapley; Mohamed–Schwarz; Titsias 2023; Galashov 2024 (`:27`) | a CL setting where the textbook does not already predict the outcome; "k4 found none" (`:252`) |
| EKS2 | EKS2-1 "HOLDS" at v = 3, 10; EKS2-2 "FAILS. R = 1.542"; EKS2-4 behind LAPLACE "D = 1.636, 1.822 and 1.826"; every row flagged F1 (`:177-185,197-201`) | — | the scoring target: "When every seen task is scored … the Bayes answer is plain counting (q = 0)" (`:29`) | — (SIMULATED) |

- **Class:**
  - **C** dominant (textbook adaptive filtering).
  - **E** for "which Ω = 1".
  - **D** for EKS1, closed on a control infeasible by its own text.
- **Bears on:** baseline P4 (already "Standard", [Ashes] `theory/CRR.md:265-266`, as quoted in L-EQ) and the theory's
  undecided reading of equanimity. k4 labels: (i) "**DISAGREES**" with the A8 step; (ii) "**MOTIVATED** by CRR.md §6,
  P3, O1 … **DISAGREES** with H-EQ as registered"; (iii) "**TRANSLATES** … **SILENT** on whiteness"
  (`REPORT.md:137-139`). "CANDIDATE count 0" (`:141`).

### 2.5 E-RETRO update: battery R4

| (1) observed | (2) interpretation | (3) ordinary explanation | (4) what would distinguish |
|---|---|---|---|
| "51 REDUNDANT-DOMAIN, 46 WRONG, 3 REDUNDANT-IG" (`retro/REPORT_R4.md:133`); 0 ADDS (`:152`). Cumulative over 200 systems: "125 \| 15 \| 55 \| 2 \| 1 \| 1 \| 1" (`:160-162`) | "a map of CRR's structural commitments" (`:241-242`) | "In F3, F5, F6, F8 and F10 the Embers value is fixed by the family's algebra … These rows cover 64 of the 100 systems" (`:166-168`) | "A prospective real-data study under the full R1–R15 protocol" (`:247`) |

The structural results that bear on shared questions:
- **F3/F4, the Fisher cut on total-variation carriers.** "The Fisher half-turn … is the peak of every single-peaked
  cycle that returns to its start (F3: 10/10 …). It misses the global peak of every cycle with more than one hump (F4:
  8/8, by 6.3–31.7 %)" (`:169-173`).
- **F5, sensor laws.** On π-symmetric laws the Fisher antipode is π exactly. On lopsided laws it is "3.855139, 2.909588,
  4.150397 and 3.962920 rad" (`:174-178`).
- **F6, S2 algebra.** It "always gives a half-life ratio of 0.5 when the event rate doubles", and it matches the 12
  per-event domains (`:179-183`).
- **F7/F8, A6.** It "fails every multi-timescale decay tried: 7/7" and "cannot represent the 6 accumulating stocks"
  (`:184-186,201-202`).
- **F10, the oriented cut.** It "counts nearly none of the events in reversing motion" (`:187-190`).

Classification:
- **Class:** **C** dominant; **A at R4** for the WRONG rows as model-domain limits; **E** for F5, which marks where S1
  could be discriminated.
- **Bears on:** baseline A6 at R4 (F7/F8, as before). Baseline A3's *oriented* cut, as an event counter, at R4 (F10);
  Ashes implements the cut "oriented" ([Ashes] `CLAUDE.md` §3.1 item 3).
- The rotor's S1 and S2 are mapped, not tested.

### 2.6 E-H2H3 update: H2 gate run 2

- **Observed.** "GATE OPEN" (`results/gate_h2_run2.txt:266`). But `parity_free` "ties crr in every POS unit"; "the
  minimum detectable κ rises from 0.4 to 0.6" (`notebook/AGENT_LOG.md:72`).
- **Class:** R4 only, **C-risk confirmed**: the advantage is "worth about one fitted parameter" (same entry).
- **Bears on:** the rotor only.

### 2.7 E-ROB: stages D, E, F, H

- **Observed:**
  - stage D: "Every CRR-proper learning rule failed held-out, reduced to a known rule, or closed at its gate"; "The
    candidate product core (T0) uses no CRR ingredient" (`notebook/AGENT_LOG.md:94`);
  - stage F: "CANDIDATE 0" of 77 (`F_robotics_crr/REPORT.md:12-19`);
  - stage H: "CRR's role: vocabulary only (one TRANSLATES, two DISAGREES)" (`notebook/AGENT_LOG.md:100`).
- **Class:** **C** (classification against known work). There is no A–F empirical content.
- **Bears on:** nothing in CRR.md.

### 2.8 E-H1 instrument note (PR #12)

- PR #12's gate finds the frozen h1card R-peak and ABP-foot detectors leak post-cutoff content (1450037 message).
  Embers' review confirms the leak and says it changes no registered result (`notebook/AGENT_LOG.md:71`).
- Auditor's reading: this adds a **D** (instrument) caveat to H1CARD-1's FAIL. It does not reverse the direction, since
  look-ahead could only have helped the tested arm or neither. It does not change the cross-audit's class A for H1 in
  that class.

---

## 3 Effects on the cross-audit

**(a) "No Embers failure reaches a hypothesis stated in Ashes CRR.md."** **Unchanged.**
- STK2-1 is VOID.
- ESEC2-2 and ESEC2-3 FAIL on the frozen SEC4 rule, which Embers labels "not a CRR rule" (`ledger/LEDGER.md:44`).
- The new synthetic WRONG rows (R4 F7, F8, F10) reach A6 and the oriented cut only at R4, as before.
- Stage C's SPLIT reaches a *reading* of A3 (D12), not a CRR.md hypothesis.

**(b) Shared live leads.**
- **Stick-slip / S2.**
  - Still untested on both sides, now VOID twice in Embers. "Neither ran a test that scored" stays true.
  - Every verified multi-velocity PSU run is now SEEN in Embers (§2.1). They are absent from Ashes' SEEN (§1.6 item 4).
  - The lead survives as an idea, but it now needs a new dataset with documented columns. The cross-audit's
    "VOID or pending" should read "VOID twice (stk1, stk2)".
- **Own-event indexing.** No new real-data evidence. R4 F6 maps where per-event updating holds (12 domains) and where
  clock decay holds (10) (`retro/REPORT_R4.md:179-183`). That map is fixed by algebra and is not evidence.
- **Identifiability of the cut.** Strengthened as the shared gating problem:
  - R4 F3 shows that on total-variation carriers the Fisher half-turn coincides with the peak of single-peaked
    returning cycles. Auditor's reading: on such carriers, antipode and extremum are not separable, so H-CUT is not
    decidable there. This bears on D2/D3.
  - R4 F5 lists real sensor laws where S1 is discriminable, the head-direction cell among them.
  - PR #12 adds an event-detector causality caveat.

**(c) Shared dead ends.** Five new ones:
1. **The "not behind the tuned λ" criterion for SEC.** Reached independently, as far as the records show (§4.1).
2. **No CRR-proper ingredient in SEC.** [Embers] "no CRR-specific quantity" (`A_sec4_why/REPORT.md:72`); [Ashes] F11
   (`PRE_PHOENIX_AUDIT.md` §5, SEC row at line 255).
3. **Coupling SEC + transport + pause.** [Embers] "no simulated support" (`Applied_Suite/README.md:56`); [Ashes]
   ledger CPL1-A "GATE CLOSED (the coupling stops, R12)".
4. **Robotics.** [Embers] "CANDIDATE 0"; [Ashes] ROB1 stage 3 "C-R1: REDUNDANT ... C-R2: REDUNDANT ... C-R3:
   REDUNDANT" (as quoted in `notes/L-RETRO-ONT-APP.md:655`).
5. **Ω = 1 / Kalman as textbook.** Agreed, but **primed** (§4.2), so it belongs with the inherited agreements.

**(d) Disagreements D1–D11.** None is resolved. Two are touched, and three new ones are recorded:

| # | topic | Ashes reading | Embers reading | what would decide |
|---|---|---|---|---|
| D2/D3 (touched) | the antipode against the extremum | unchanged | R4 F3: on TV carriers the Fisher half-turn *is* the single-peaked extremum; F4: it misses multi-hump peaks | carriers where the two differ (F4/F5 types), with an independent event channel |
| D5 (touched) | laws of motion | unchanged | H2's edge over a parity-aware model ≈ one parameter (`AGENT_LOG.md:72`) | an S2/H2 transfer test on real data |
| **D12 (new)** | is the empty pause an instance of A3? | "A3 read as natural time: press = pause that resumes in place" ([Ashes] `notes/L-PAUSE.md:64`, O3); the press-as-cut is a modelling step, not CRR.md (`:28-30`) | A3 read literally ("settles … resets C") is "the first pause-breaker for a consolidating learner, so that CRR text DISAGREES with a safe pause" (`notebook/AGENT_LOG.md:90`); RB-31 DISAGREES | textual. Both agree the pause is not CRR evidence. Whether A3 "settles" means commit or freeze is undecided in CRR.md; Embers' F notes "can be read as freezing a model just as easily" (`F_robotics_crr/REPORT.md`, RB-56 bullet) |
| **D13 (new)** | what carried SEC4 on its own carriers | "Both the calibration and the clip added carriers in SEC4. On SEEN data the calibration is replaceable" (AR1-B 27/30, SI-1C 28/30) ([Ashes] `SEC_Analysis/WHY_SEC4_WORKED.md:48-56`) | "the secant carried SEC4; the clip only guarded stability"; paired by seed the clip is "a tie on all 5 non-leaky carriers" (`A_sec4_why/REPORT.md:47-50,146-149`) | the same numbers read two ways. Ashes counts under the frozen unpaired rule; Embers pairs by seed. Both find the clip rescues diverged seeds. On held-out data, ESEC2-3 (secant ahead of raw Laplace + clip) "4/10" FAIL and [Ashes] SEC6R-B raw Laplace "6/9" against clipped SEC "7/9" point the same way: the calibration's held-out margin is small |
| **D14 (new)** | does balanced accuracy repair the criterion? | SEC7-A: with random class order and balanced accuracy, edge is "behind … on 13/30 (need more than 15)", GATE CLOSED ([Ashes] ledger SEC7-A, SEEN) | ESEC2 report: under balanced accuracy V5s is "4/10" and "does not meet the criterion" (`runs/esec2/score.txt:344`, held-out, report only) | different arms (edge vs V5s), different carriers, a report vs a gate. A registered must-fail on balanced accuracy with both arms would decide it |

**(e) Question 10 for Embers after 7082f23.** Mixed, and the record shifted away from "too confirmatory too early" on SEC:
- **Exploration on SEEN data before held-out data was used as designed.** Stage A was declared "exploratory on SEEN data
  (no PASS possible)" (`Applied_Suite/README.md:26`). ESEC1 closed before data. ESEC2 was redesigned from stage A's
  lessons, with a beacon draw, constants as rivals and a next-day data step (`notebook/AGENT_LOG.md:91`, entry 78).
  Auditor's count (derived): prompt 39 (≤ 07:17:16Z) → ESEC2 freeze 04de875 (18:41:31Z) ≈ 11 h 24 min; → beacon
  draw 88cc2c3 (2026-10-01T02:14:42Z) ≈ 18 h 57 min. This is the "pre-hash maturity stage" the cross-audit asked for.
- **Still too fast in places.**
  - stk2 consumed p5565 (≈ 855 MB; auditor's sum of 106762542 + 748597115 bytes, `runs/stk2/RESULT.md:11-12`) for a
    plumbing VOID.
  - ESEC2 opened 8 carriers it then excluded (§1.2).
  - Declared synthetic checks closed on defects in their own declarations: EKS1, EG0, ESEC1 CP1 (§1.6 item 6); EP3 and
    EP3b on controls; ECC3–5 "CLOSED on their controls" (`notebook/AGENT_LOG.md:92`).
  - Prompt 41 (≤ 21:15:49Z) → EKS declaration f20423e (23:19:12Z) ≈ 2 h 03 min; → EKS run committed (00:01:54Z)
    ≈ 2 h 46 min (auditor's count, derived). A short dry run of each control would have caught several of these closures
    before the declaration. Auditor's reading: that is the *suppressive* face of declare-first applied to cheap
    synthetic checks.
- **Promotional pressure, contained.** Prompt 36 asked for a brochure. Embers labelled it "not a finding"
  (`notebook/AGENT_LOG.md:84`) and later corrected a factual overstatement ("5 of 17", `Findings/SEC4_PASS1/README.md:42`).

**(f) Machinery.**
- **Stronger than the cross-audit recorded:**
  - carriers drawn by a public beacon after the anchor;
  - constant-reduction rows registered before data (ESEC2-K/K2);
  - a scorer that refuses to print a rung without a verified tag (`runs/esec2/score.txt:345`);
  - control-feasibility as a stated lesson (`K_kalman_equanimity/REPORT.md:245`).
- **Weaker than the cross-audit recorded:**
  - the signing key was empty from the start (§1.6 item 1), so cross-audit §9.4 item 1 holds for the OTS anchor only;
  - the research line sits on an unmerged branch with a divergent twin (§1.6 item 2);
  - subagent reports were saved by the lead, with stale text (§1.6 item 5);
  - a commit message was wrong (AGENT_LOG 62);
  - a registered machine record ran late (AGENT_LOG 83);
  - ESEC1's "selection rule was revised twice after its earlier draws' metadata had been seen" (`notebook/AGENT_LOG.md:86`).

---

## 4 Comparisons with Ashes' own conclusions

### 4.1 E-SEC against [Ashes] L-SEC

| point | [Ashes] | [Embers@de6c05a] | same? |
|---|---|---|---|
| SEC4-1 standing | ledger SEC4-1 PASS-1 (`ledger/LEDGER.md:186`) | quoted as an ashes row; "SEC4-1 reproduces exactly (6/6)" (`notebook/AGENT_LOG.md:76`) | same row, reproduced |
| the criterion met by a must-fail arm | FM6: "a learner frozen after task 1 … not behind the tuned λ on 24/30" (`SEC_Analysis/WHY_SEC4_WORKED.md:35-36`); ledger SEC4-1-G: "M6 not behind the tuned lambda on 5/6 (need 5)", "gate CLOSED" (`ledger/LEDGER.md:211`) | V5s "meets SEC4-1's count on P1 (5/6), P2 (7/8) and P3 (12/16)" (`A_sec4_why/REPORT.md:57`); ESEC1 CP1 FAILED (`prereg/esec1/CLOSED.md:18`) | **same conclusion**. Ashes' M6 ("EDGE, a uniform cap after task 1 with no Fisher", [Ashes] `notebook/AGENT_LOG.md:235`) and Embers' V5s ("every coordinate with any importance anchored at strength κ/lr", `A_sec4_why/REPORT.md:32-33`) are, on the auditor's reading, near-identical arms |
| the cause | "select_classes ranks classes by count … task 1 always holds the two most frequent classes" ([Ashes] `notebook/AGENT_LOG.md:235`) | "tasks run from the most to the least frequent classes under one softmax head" (`A_sec4_why/REPORT.md:63-64`) | **same** |
| on held-out data | SEC6R-G: "edge not behind on 8/9 (closes at 7)"; SEC6R-1 "PASS-0 UNINFORMATIVE" ([Ashes] `ledger/LEDGER.md:234-235`) | ESEC2-K "8/10", ESEC2-K2 "10/10" MEETS; ESEC2-1 "no rung" | **same pattern** on disjoint carriers (auditor's comparison of the two carrier lists) |
| SEC5-1 | FAIL 4/8 | "reproduced exactly"; three confounded accounts (`A_sec4_why/REPORT.md:61-69`) | same row; Embers adds the learnability and edge accounts |
| a stabilised or clipped tuned λ | SEC6R-C "7/9 (need 7)", "PASS-0 (UNINFORMATIVE: SEC6R-GC CLOSED)" (`ledger/LEDGER.md:238`) | ESEC2-2 "5/10 … FAIL, FRAGILE" | different outcomes on similar comparators; not a contradiction (different carriers, different gate state) |
| the calibration | SEC6R-B: AR1-B and SI-1C "8/9" against clipped SEC "7/9" (`ledger/LEDGER.md:239`) | ESEC2-3 "4/10" FAIL | the same direction: no held-out advantage for the calibration |

**Independence.**
- **Timeline:**
  - [Embers] ESEC1 CP1: d11c9db, 2026-09-30T09:41:14Z.
  - [Ashes] FM6: 34b4765, 09:38:11Z.
  - [Embers] V5s added in A2's "09:41Z–09:58Z fix round" (`A_sec4_why/REPORT.md:316`).
  - [Ashes] SEC4-1-G: bc9ec3e, 12:25:43Z.
  - Both came after the blind began (Embers prompt 39 ≤ 07:17:16Z; [Ashes] P1 declaration 5f64b5f at 07:19:45Z).
- **Before the blind, Embers had not reached it.** Its pre-blind audit said "The result does not reduce to a constant in
  these files" (`audits/sec4/README.md:38`).
- **Before the blind, Ashes had not reached it either.** M5 and M6 entered P1 in "Amendment 2 … after SEC6's development
  runs" ([Ashes] `SEC_Analysis/WHY_SEC4_WORKED.md:8`), after 5f64b5f.
- **Shared inputs (limits):**
  - the same prompt text;
  - the same pre-blind Ashes records: SEC4 and SEC5 outputs and the frozen SEC4 code, copied from 45cd4af
    (`runs/esec2/score.txt:3`);
  - the same model family. `BLIND_COMPARISON.md:41-45` says so itself: "Agreement is weaker evidence than two people or
    two labs agreeing".
  - Ashes was not under a recorded blind (§1.3).
- **Auditor's reading:** independent within one model family and a shared baseline. That is stronger than Embers
  reading Ashes, and weaker than two labs.

### 4.2 E-KAL against [Ashes] L-EQ

| point | [Ashes] L-EQ | [Embers@de6c05a] stage K | same? |
|---|---|---|---|
| Ω = 1 as a value | "**A** (empirical) **+ C** (analytic, MGDA-known)"; the equal-magnitude reading is "analytically non-selecting" (`notes/L-EQ.md:422,563`) | "'Equal pull' cannot choose a weight" (`REPORT.md:22`) | same |
| K(1) = 1/φ | "Standard mathematics … at one Fisher speed" (`notes/L-EQ.md:431`) | "K = 1/φ is optimal only at v = 1" (`REPORT.md:21`); claim 1b CONFIRMED (`:54`) | same |
| the equal-precision reading | "never chosen or tested as such … Its natural home is inverse-variance (Bayes) weighting" (`notes/L-EQ.md:465-470`) | K = 1/2 = "the *unweighted* equal pull" (P⁻ = r); "the precision-weighted pulls are equal at every optimal update" (`k1_maths.md`, claim 2 and 5 rows) | **compatible, different cut.** Embers makes both the weighted and the unweighted versions non-selecting (an identity, or a fixed gain). Ashes leaves (b) as "selecting, but standard". Neither tests it on data |
| what would select | not addressed beyond Bayes/Kalman | "whiteness, not NIS" (`REPORT.md:23`) | **Embers only** (textbook) |
| the scoring target | not addressed | "The scoring target decides more than drift does" (`REPORT.md:28-31`) | **Embers only** |
| drifting units | "Drifting-units niche: F (rung R4, post hoc, fragile) + C (VQGAN)" (`notes/L-EQ.md:433`) | EKS2 drifting *optima*: calibrated surprise helps "only for fast drift on the latest-task target" | different regimes; not comparable |

**Independence: primed, recorded as such.**
- The pasted analysis (prompt 41) cites `Continuous_Learning/CONTINUOUS_LEARNING.md`,
  `docs/notes/2026-09-22_omega_sweeps.md` and CRR.md, and it "recomputed the Kalman table"
  (`notebook/PROMPT_LOG.md:342`).
- AGENT_LOG 88 says ([Embers@de6c05a] `notebook/AGENT_LOG.md:101`):
  - "Blind question: the other chat 'cloned the repository', so it may have seen ashes_crr's current state";
  - "Every file the pasted text cites … exists at ashes_crr 45cd4af, the pre-prompt baseline … The text refers to
    nothing dated after 2026-09-22";
  - "Treated as owner input about baseline material, not as a breach; recorded here so Daniel can judge".
- AGENT_LOG 89 adds that a verifier "ran one `ls /home/user/alexsabine` with output to /dev/null; nothing was seen".
- Embers' own mapping: "Claims 1–6 are already in the record, mostly verbatim" (`K_kalman_equanimity/REPORT.md:107`).
- **Auditor's reading:** the agreement on non-selection, 1/φ and VQGAN is Ashes' own L-EQ content, returned through a
  third party. It is not independent. Whiteness, the 2-D failure of speed matching and the scoring-target point are new
  and textbook. None of it is CRR-specific (k4 "CANDIDATE count 0").

### 4.3 Stages C, G, EP and F against [Ashes] L-PAUSE (constructions; ROB1)

| point | [Ashes] | [Embers@de6c05a] | same? |
|---|---|---|---|
| what the pause is | "Construction" (`notes/L-PAUSE.md:15`); C class (`PRE_PHOENIX_AUDIT.md` §5, line 260) | "standard dynamic programming", "not a CRR result" (`audits/empty_pause/README.md:8,60`) | same (EP is pre-blind and read Ashes at 9fd07d5) |
| the world must stand still | an assumption of O3: "the world does not move during the pause" (`notes/L-PAUSE.md:64`) | measured stakes when it moves, with both signs; "freezing the world restores zero content" (`README.md:32-33,51-57`) | **same condition**. Embers sizes it: the lease must "cover the tail, not the mean" (AGENT_LOG 68) |
| A3 and the pause | A3 *read as* natural time (O3) | the literal A3 text is a breaker (SPLIT 100/100) | **D12** |
| coupling with SEC and transport | CPL1-A GATE CLOSED | stage C: no support | same, independent (post-blind) |
| robotics | ROB1: "DISAGREES (candidate) 3 … RESTATES 9 … SILENT 13"; C-R1..3 REDUNDANT (`notes/L-RETRO-ONT-APP.md:654-659`) | 77 bottlenecks: "SILENT 60, TRANSLATES 13, RESTATES 3, DISAGREES 1 …, CANDIDATE 0" | same direction on different registers, independent (post-blind) |
| drone or robot application checks | ROB1 stage 4b: "ADDS 0, PROPOSES 0, … REDUNDANT-DOMAIN 6, WRONG 2" (as quoted in `notes/L-RETRO-ONT-APP.md:656-657`) | EG0 CLOSED, no result | not comparable (Embers has no result) |

---

## 5 Phoenix inheritance rows for the new or updated Embers lineages

| Lineage ID | Core CRR idea | Operationalisation(s) tried | Strongest supporting observation | Strongest negative evidence | Failure level | Current epistemic status | Mundane explanation | CRR-specific possibility | What Phoenix may explore | What Phoenix must never claim |
|---|---|---|---|---|---|---|---|---|---|---|
| E-S2 (updated) | A6/P3 age counted in occasions; A1′ natural time | q^(n−j) memory, transferred across loading rates; stk1, stk2 | s2_transfer_gate DECIDABLE (R4); R4 F6: per-event domains give ratio 0.5 (algebra) | STK1-1 and STK2-1 "**VOID**" | none reached (D) | untested; every verified PSU multi-velocity run consumed | clock-time healing; no memory | memory half-life scales inversely with event rate | a stick-slip dataset with a published data dictionary read before the freeze; schema validation that does not count as exposure | anything about S2 from stk1/stk2; that p5156/p5363/p5565 are held-out |
| E-SEC (new) | none (SEC is "not a CRR rule"); CRR as heuristic route | frozen SEC4 on 30 SEEN carriers with 21 variants (stage A); ESEC1 (closed); ESEC2 on 10 beacon-drawn held-out carriers | ESEC2-1 "9/10" (no rung); secant 6/0/0 over raw Laplace + clip on SEEN P1 | ESEC2-2 "5/10" FAIL, ESEC2-3 "4/10" FAIL; ESEC2-K/K2 MEETS (constants) | method level (A); instrument (D/E) for row 1 | no rung; criterion uninformative where constants meet it | Laplace weight + units rescale + stability guard; class-ordered loader | none | metrics that constants fail (balanced accuracy, random class order) as registered must-fail gates; the cardiotocography leak check on Ashes' SEC4-1 | "tuning-free" without a must-fail constant; any SEC row as CRR evidence; ESEC2-1 as a replication PASS |
| E-PAUSE (new) | the empty cut (A3 transposed); Proposition 7 | EP1–EP5 exact MDPs; stage C pause contract; stage G drone (EG0) | EP1 bound 200/200; B1f 0 in 21/21; the pause contract's breaker catalogue | EP3/EP3b closed; EG0 CLOSED; SPLIT: literal A3 breaks the pause in 100/100 (5 distinct runs per tier) | construction (C); D for the closed checks | R4 / SIMULATED; no status | checkpoint/resume plus holding the world | none shown | lease sizing under heavy-tailed pauses; EG-b with a stable learner and feasible controls; a theory decision on whether A3 "settles" means commit or freeze | that the pause is CRR evidence; that the empty cut works in a moving world without holding it |
| E-KAL (new) | Ω = 1 / equanimity; P4 | scalar Kalman derivations; EKS1 (closed); EKS2 continual-regression bridge | EKS2-1 HOLDS at fast drift (R = 1.0077, 1.0005) | EKS2-2 "R = 1.542", EKS2-4 behind LAPLACE; every EKS2 row flagged F1 | C (textbook); E (which Ω = 1) | SIMULATED, no status; primed by Ashes material | Mehra-type adaptive filtering; predictive likelihood (Titsias, Galashov) | none (k4 CANDIDATE 0) | a registered whiteness-tuned consolidation weight against the rival list in `REPORT.md:229-237`, with the target declared | that "speed matching" or "calibrated surprise" is CRR's; that Embers' agreement with Ashes L-EQ is independent |
| E-RETRO R4 (new battery) | A3/A6/S1/S2 commitments across domains | 100 declared synthetic systems in families F1–F10 | 51 RD, 3 RIG; F3 10/10 | 46 WRONG; 0 ADDS; 64 labels fixed by algebra | R4 | redescription and map | first passage, total variation, exponential smoothing, sensor symmetry | F5 sensors where S1 is discriminable | real-data tests on F5-type sensors (head-direction cells) and F6-type per-event domains | any R4 count as support; "pre-registered" as meaning real data were predicted |
| E-ROB (new) | CRR readings of robotics, drones, trust | registers of 77 bottlenecks; readings; threat model | — | CANDIDATE 0 | classification | none | known robotics and security engineering | none | — | that CRR addresses a robotics bottleneck |

---

## 6 Statements in `PRE_PHOENIX_AUDIT.md` §9 (and related) that need changing

Line numbers are as read (§9 at 633–764).

1. **§9 intro, "What was read" (`:636-637`):** "A `git ls-remote` on 2026-10-02 returned the same HEAD, so this is
   Embers' current published state."
   - Change to: `main` is at 7082f23, but Embers' work continued on the unmerged branch `claude/eager-allen-5rjiem`, to
     de6c05a (2026-10-02T00:01:54Z), 72 commits later. That branch was read post hoc in this addendum.
   - Also name PR #13 (80811db, a divergent twin) and PR #12 (1450037).
2. **§9.1 (`:644-646`):** "built in about 45 hours"; "Its ledger has 12 rows and no PASS of any level"; and the primary
   rows list.
   - Change to: 22 rows at de6c05a. STK2-1 "**VOID**". ESEC2-1 "criterion met; **no rung**". ESEC2-2 and ESEC2-3 "FAIL,
     FRAGILE". No PASS-0/1/2 rung; ESEC2-D reads "PASS (secondary)".
   - Activity spans 2026-09-27 to 2026-10-02.
3. **§9.1 timing caveat (`:655`):** "SEC4–SEC6R postdate it."
   - Change to: Embers later read Ashes at 9fd07d5 (SEC4 audit), 25940a1 (SEC5 audit) and 45cd4af/989e4d8 (the blind
     baseline). It did not read SEC6, SEC6R or Ashes P1, by its recorded blind.
4. **§9.3 (`:678-679`):** "Its successor stk2 is hashed but not run at 7082f23."
   - Change to: STK2-1 is VOID (no declared column names). S2 is untested. Every verified multi-velocity PSU run is now
     SEEN.
   - Add one line that ESEC2's FAILs bear on SEC, which Embers itself labels "not a CRR rule". The headline sentence at
     `:674` (and §1 item 7, `:79`) stands.
5. **§9.4 item 1 (`:688`):** keep the anchor statement, and add: the tag-signing key file is empty (since c5af86b;
   AGENT_LOG 87 supersedes AGENT_LOG 25), so Embers' signed tags were never verifiable against a registered key.
   - Add as strengths: beacon-drawn carriers; constant-reduction rows registered before data; a scorer that refuses a
     rung without a verified tag.
6. **§9.5 (`:698-710`).**
   - Item 2's count becomes: four of six real-data data steps ended without a hypothesis verdict (H1GAIT, H1RESP, STK1,
     STK2; auditor's count, derived). ESEC2 scored, but it tests SEC.
   - Add a balancing item: after 7082f23, Embers inserted a declared exploratory SEEN-data stage (A) and a closed
     pre-data gate (ESEC1) before its held-out successor.
   - Add the opposite cost: several declared synthetic checks closed on defects in their own declarations (EKS1, EG0,
     ESEC1 CP1, EP3/EP3b, ECC3–5).
7. **§9.6 live leads (`:715-719`).**
   - "VOID or pending" → "VOID twice (stk1, stk2)".
   - Add that the PSU multi-velocity runs are consumed (and absent from [Ashes] `data/SEEN.md`).
   - Add R4 F3/F5 to the identifiability lead.
8. **§9.6 dead ends (`:721-729`).**
   - Add, as independent under the blind (with the §4.1 limits): "not behind the tuned λ" is met by a constant or frozen
     learner on class-ordered streams; SEC has no CRR-proper ingredient; the SEC + transport + pause coupling has no
     support; robotics yields no CRR candidate.
   - Add to the *inherited* list: Ω = 1 / Kalman is textbook, primed through prompt 41 (AGENT_LOG 88).
9. **§9.7:** add D12 (A3 and the pause), D13 (what carried SEC4) and D14 (balanced accuracy). Note that R4 F3 bears on
   D2/D3: the Fisher half-turn equals the extremum on single-peaked TV carriers.
10. **§9.8 (`:763-764`):** strengthen the loader point with STK2. Quote Embers' rule: "read that documentation (never
    the data) before freezing" (`docs/TRANSFER_CANDIDATES.md:258-259`).
11. **Outside §9, for the owner.**
    - §13 (record-keeping) could add the cardiotocography label leak that Embers reports (§1.6 item 3).
    - It could also add the missing Embers exposures in [Ashes] `data/SEEN.md` (§1.6 item 4).
    - `notes/EMBERS_CROSS_AUDIT.md` §1, §4.2, §5.1 and §8.1 carry the same stale items (prompt-log entries 24,
      agent-log entries 54, 12 ledger rows, "stk2 pending", "Signed tags … tag objects committed").
