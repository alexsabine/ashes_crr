# A11: is SEC explained by CRR, Bayes, optimisation or information geometry? (a code reading)

**The question.** Analysis A11 of `DECLARATION.md` (pushed at 5f64b5f; prompt-log entry 257), with forecast F11.

**Status.**
- This is a post hoc reading of code and of records already opened. It adds no ledger row, and no word here is a PASS.
- Every result number below is printed by one of these pinned outputs:
  - `checks/a11_grade.txt`, from `checks/a11_grade.py`;
  - `checks/verify_a11.txt`, from `checks/verify_a11.py`;
  - `theory/checks/cramer_rao_reading.txt`, where it is named.
- Frozen-code line numbers are printed by `a11_grade.py` ([1]). Dates are those of the named files and studies.
- Every HOLDS, FAILS, REDUNDANT and "load-bearing" is computed by `a11_grade.py` from those numbers (R15). Two columns
  are the agent's classification and are labelled so in [7]: an ingredient's field and its nearest CRR clause.
- **The sources** were fetched on 2026-09-30, and their versions are listed in `checks/claims_a11.py` (R10).
  - `verify_a11.txt`: 47 of 47 quotes found verbatim, from 26 claims across 11 sources.
  - The fetch record is committed in `sources/`: `FETCH_LOG.txt` (URL, version, date, HTTP status), `SHA256SUMS.txt`
    (every fetched file, PDFs included) and `fetch.py`.
  - The extracted third-party texts stay outside the repository, under `/tmp/claude-0/sec_an_src/`. The raw-text hashes
    that `verify_a11.txt` prints equal `sources/SHA256SUMS.txt` on 11 of 11 (`a11_grade.txt` [4]).
- **Barzilai & Borwein 1988 was not read.** The DOI (10.1093/imanum/8.1.141) redirects to academic.oup.com, which returned
  HTTP 403 behind a Cloudflare challenge (`sources/FETCH_LOG.txt`).
  - Crossref's record confirms the title, journal and pages (claim a11:16).
  - The BB step formula is quoted instead from Tan, Ma, Dai & Qian 2016 (arXiv 1605.04131 v2), which is freely readable
    and cites Barzilai & Borwein as its reference [3] (a11:13, a11:15).

## The answer, as printed

- **F11: HOLDS.** F11 is a conjunction of sentences. `a11_grade.py` computes each one, and F11 holds only if all of them
  hold ([8]).
  - **The headline, "no CRR-proper ingredient is load-bearing", holds on the static reading.** SEC's code path performs
    **0 of the 7** operational CRR-proper clauses (CLAUDE.md §7). An operation that is not performed cannot bear load.
  - **A7/A8 are prohibitions.** They have nothing to perform, so they are listed apart and not counted.
  - **None of the 9 ingredients is CRR-proper** (0 of 9: 8 in the code, 1 premise).
- **Parts (a)–(f) all hold:**
  - (a) the weight 1/2 is the Laplace weight;
  - (b) the calibration is built from a Barzilai–Borwein secant, is aimed at the empirical Fisher's published scale error,
    and moves the EF in that error's direction (s > 1) on 41/42 carriers. How (b) is read is set out below the list;
  - (c) the secant is a chord between window means, not an arc;
  - (d) the clip is AR1's bound, met with equality;
  - (e) A1′ supplies the name "units" and no CRR unit is computed;
  - (f) CRR's rung for the explanation is at most R1. The ladder's R2 needs "a CRR-proper ingredient changed the number",
    and none is performed.
- **How (b) is read.** The declaration does not say how "fixing" is meant, and the script names this ambiguity.
  - It reads "fixing" as purpose and direction, which a code reading can decide.
  - The mechanism reading is that SEC works because the EF's error is removed. That is not A11's question. M1 (the true
    Fisher) and M2 (endpoint curvature) test it, under FM1 and FM2 in `m_checks.txt`.
  - **Beside (b):** the calibration as a combination, S, is **PARTLY REDUNDANT**. No verified source states it. (b) names
    its parts and does not claim that the combination is published.
- **M4 does not enter F11.**
  - A11 is a code reading of SEC's `run()` and `run_guard()`. M4 is not SEC's code.
  - As implemented, M4 sums no segment length ([2]), so no M4 result could make a CRR-proper ingredient load-bearing.
  - M4 has its own declared forecast, FM4, and its own consequence, the SEC6 carry rule. Both are decided in
    `m_checks.txt`; [6] reports them once `m_checks.json` exists.
- **Where the ingredients come from.** The field column is **the agent's classification, not computed** (`a11_grade.txt`
  [7]). Each ingredient's stating sources are listed in [4].

  | field (agent's classification) | ingredients |
  |---|---|
  | Bayes | 2 (W, N) |
  | information geometry | 2 (F, R) |
  | optimisation | 2 (C, K) |
  | optimisation + information geometry | 2 (E, S) |
  | protocol | 1 (T) |
  | CRR | 0 (computed: 0 of 9 CRR-proper) |

- **Every ingredient but one is REDUNDANT** (a verified source states it). The exception is the calibration itself, S,
  which is PARTLY REDUNDANT: no source found states it.
- **So SEC's explanation is Bayes, optimisation and information geometry.** CRR supplies a word ("units") and, in the
  context of discovery, a route to the idea (§4 below). No CRR operation does work in the code.

## 1. What the code does, line by line

**What was read.**
- `runs/sec4/frozen/sec1_score.py` `run()` (lines 169–230). This file is byte-identical in the frozen folders of SEC1,
  SCL3, SEC3, SEC4 and SEC5: one distinct sha256 (`a11_grade.txt` [1]).
- `runs/sec4/frozen/sec4_score.py` `run_guard()` (lines 58–114). This file is identical in SEC4 and SEC5.
- `a11_grade.py` finds each statement quoted below verbatim in the frozen text, 35 of 35, and prints the line numbers used
  here ([1]).
- **SEC's code path.** The clause tests in §2 read only the statements SEC executes. These are `run()` with mode
  `bayes_sec` and no distortion, and `run_guard()` with variant `clip`. The branches these settings decide are pruned
  from a copy of the syntax tree and listed with their lines ([1]). They include `run()`'s gate-only distortion branch
  (lines 212–216, which call `exp`), its `eq` branch (the H-EQ comparison arm) and `run_guard()`'s `raw` and `scale`
  variants.
- **Not read:** SEC3's own guard (`sec3_score.py`, mode `bayes_sec_g`, a raw-Laplace fallback). It is not one of the two
  functions A11 names.

**The ingredients.**

| id | ingredient | the code (sec1_score.py / sec4_score.py) | what it is | published source (verified) | grade |
|---|---|---|---|---|---|
| W | the weight 1/2 | `w = BAYES_W` (197) with `g_q = 2 * imp_used * dth` (195), step `lr * (g_p + w * g_q)` (205); `w = S.BAYES_W` (94) | the penalty is w·Δθᵀ imp Δθ; at w = 1/2 it is the Laplace quadratic ½ Δθᵀ H Δθ | Huszár eq. (6); Ritter: the multiplier's "natural value of 1" | REDUNDANT |
| N | task-size weighting, one penalty | `imp_bayes = imp_bayes + n_task * sc * f_task` (223), used as `imp_bayes / n_task` (181); `theta_star = theta_now` (224) | the Laplace recursion: task curvature = sample count × per-sample Fisher, summed, anchored at the latest task end; ÷ n_task puts it on the scale of the mean mini-batch loss | Huszár eq. (5), (11); Ritter eq. (7); online EWC (P&C, with a decay γ < 1: close) | REDUNDANT |
| F | per-sample empirical Fisher | `f += ce_loss_grad(net, Xtr[ii], ytr[ii])[1] ** 2` over 50 mini-batches, `f_task = f / N_FISHER * bs` (209–210) | squared gradients at the **training** labels: the empirical Fisher (EF). Squaring mini-batch means and multiplying by bs gives the gradient variance plus bs × the squared mean gradient (a mini-batch variant of Kunstner eq. 18) | Martens §11; Kunstner et al. | REDUNDANT |
| E | premise: the EF's scale error | none (a premise) | where the task is fit, the EF understates the curvature | Kunstner: "the EF goes to zero while the Fisher (and the corresponding GGN) approaches the Hessian"; Martens: the EF "doesn’t have the right “scale”" | REDUNDANT |
| C | the secant c_j | window sums (183, 190–191); `dth = e_th / n_e - s_th / n_s; dg = e_g / n_e - s_g / n_s` (217); `c = float(dg @ dth) / nn` (218) | 1/η of the BB step η = ‖s‖²/sᵀy, with s = Δθ and y = Δg taken between START- and END-window means | Tan et al. eq. (2.4) (the BB step); SGD-BB forms it from epoch-averaged stochastic gradients (close); SI (close) | REDUNDANT |
| R | ρ_j | `rho = float((f_task * dth) @ dth) / nn` (218) | the Rayleigh quotient of the diagonal EF along the same Δθ: the curvature the Fisher claims | RWalk: DKL ≈ ½ Δθᵀ F Δθ with the empirical Fisher | REDUNDANT |
| S | the calibration s_j = c_j/ρ_j | `s = c / rho`, else `s = 1.0` (219–220); applied as `sc` (222–223) | one scalar per task rescales that task's Fisher to the secant curvature, keeping the Fisher's shape | close: Ritter (one tuned multiplier, the same on every task's curvature term in the recursion); Martens (combining the EF with another curvature estimate to fix its scale); RWalk (observed over Fisher-predicted, then normalised to [0, 1], losing the scale); SI | **PARTLY REDUNDANT** |
| K | the clip | `cap = kappa / (lr * S.BAYES_W)` (67); `imp_used = np.minimum(imp_used, cap)` (77) | bounds lr·w·imp at κ = 0.5 | AR1: "if … the product η · λ · Fk is greater than 1 … we overshoot"; the λ bound 1/(η · maxF) | REDUNDANT |
| T | the task boundary | `tasks = [tuple(range(i, i + per_task)) …]` (175; 64) | the Fisher, the secant and the anchor are all taken at the stream's task switches | EWC: "we compute the Fisher information matrix at each task switch" | REDUNDANT |

The C row's "states" tag rests on Tan et al.'s eq. (2.4). That equation is formed from consecutive iterates. SEC instead
differences START- and END-window means across a whole task, which is the SGD-BB device (averaging), tagged close (a11:14).

**The chord, from the code.** `a11_grade.py` parses the training step loop on SEC's path and lists every quantity summed
in it. The list is `e_g, e_th, k_step, s_g, s_th` in both functions ([2]).
- **The path enters the calibration only through two window means.** These are the START window and the END window, each
  of max(1, ⌈0.1 × steps⌉) steps.
  - FS + FE is 0.20 nominally. The ceiling makes the windows read a little more ([2], computed from each carrier's header):
    above 0.20 on 124 of the 149 tasks of the 42 carriers, median 0.2037, and at most 0.25 (sec1:yeast, a task of 24 steps
    with windows of 3).
  - The steps between the windows, at least 0.75 of every task's path, are never read.
- **Δθ and Δg are differences of those means, so c_j is a chord quantity.** No per-step length is summed, so it is not
  D2's arc and not D6's Σ√(2·KL_t).
- **Its metric is Euclidean.** c's expression holds no `f_task`, and `nn = dth @ dth`, so it is not D3's Fisher–Rao chord
  either. It is a Barzilai–Borwein secant.

**The clip is AR1's bound itself, not a stricter one.**
- **SEC's step.** The code's penalty gradient is w·g_q = 2w·imp·Δθ. So AR1's "η · λ · F" is, in SEC's code, lr·2w·imp.
- **At the cap** (20 with LR 0.05, w 0.5, κ 0.5), lr·2w·imp = 1. That is exactly AR1's overshoot edge ([2], "equal True").
  Explicit Euler diverges at imp = 40, where lr·w·imp = 1.
- **So two descriptions name the same bound.** SEC4's docstring ("half the explicit-Euler stability edge") and AR1's
  "η · λ · F ≤ 1" describe it from two sides.
- **At equality the clip freezes.** On a capped coordinate the penalty step multiplies the offset from the anchor by
  1 − lr·2w·cap = 0 ([2]). Each step therefore resets the offset to −lr·g_p alone. This is the "freeze" of
  DECLARATION.md Amendment 2, which M5 and M6 test. It too is AR1's bound, met exactly: optimisation, not CRR.
- **A correction to SPA1.** `SEC_Prior_Art/SPA1.md` read the clip as AR1's "with κ = 0.5 in place of 1". Once the factor 2
  in `g_q` is counted, κ = 0.5 is AR1's own bound. This refines that wording; it changes no grade (S5 was REDUNDANT
  either way).

## 2. The CRR-proper clauses against the code

Each clause's defining sentence is found verbatim in `theory/CRR.md`. `a11_grade.py` tests SEC's code path in both
functions for the clause's operation ([3]). None of the 7 operational clauses is performed.

| clause | what it requires | what SEC's code path does | performed |
|---|---|---|---|
| A3/D5 | a cut at the antipode of an intrinsic phase | boundaries are the label schedule; no call to `antipodal_cuts` or `intrinsic_phase` | no |
| A6 | the next state seeded from a Fisher–Rao Fréchet mean of past occasion contents under MaxEnt weights, at bounded strength, "never an accumulated count" | the anchor is only ever assigned the last task's end state (`None`, then `theta_now`); the importance **is** an accumulated count (`imp_bayes = imp_bayes + …`, in both functions) | no |
| P2/P3 | occasion weights ∝ exp(βS_m) or q^k | task weights n_j·s_j (data count × calibration); no `exp` or `power` call and no power with a variable exponent on SEC's path. The only `exp` calls in `run()` (lines 213 and 215) sit in the pruned distortion branch | no |
| A1′/D1 | σ = 1.4826·MAD of one occasion statistic; ρ = half-turn extent / σ | no σ, no MAD, and 0 calls into `src/crr/instrument/core.py` (17 functions). The code's `rho` is the Fisher's Rayleigh quotient, not D1's resolution; only the letter is shared | no |
| H-L5 | CV of arc against CV of clock between events | no call to `regularity` or `cv` | no |
| D6/H-T1 | an arc: a per-step length summed along the path | only the START and END window sums (above); no `sqrt`, `path_length`, `arc_length` or `kl_step` | no |
| H-EQ | w = Ω‖ḡ_present‖/‖ḡ_past‖ | the weight is only ever assigned `BAYES_W`; both `norm` calls of `run()` sit inside its `mode == "eq"` branch, a comparison arm pruned from SEC's path | no |
| A7/A8 | prohibitions | nothing to perform (not counted). The one code fact that bears on A7: the window sums are reset before each task's step loop and read after it, so the calibration reads only steps already taken | — |

**Two name collisions to keep apart.**
- The code's `rho_j` is not D1's ρ.
- SEC4's κ (a step-size margin) is not A6's κ (a regeneration strength).

**One tension with A6, stated plainly.** SEC works with an accumulated count, which is Bayes: the posterior sharpens task by
task.
- **Where the count comes from.** The SEC1 pre-registration names "keeping the task count" as one of the tuned λ's three
  jobs.
- **Where it clashes with A6.** A6's letter forbids an accumulated count. The unclipped SEC keeps the count unbounded. The
  clipped SEC keeps it and bounds it with AR1's clip.
- **What the clipped SEC honours.** It keeps the spirit of A6's "bounded strength". It does not keep the form of A6.

## 3. Is each ingredient load-bearing? (the evidence that exists now)

**The rule used.** This is a report rule, not a declared one, and it decides nothing ([5]). From the pinned records, an
ingredient is marked LOAD-BEARING when the arm without it is not behind on at least 2 fewer carriers than the arm with
it. The rule reads the declaration's "at most 1 carrier fewer" tolerance in reverse.

- **S, the calibration, is load-bearing.**
  - SEC is not behind on 29/42 carriers, raw Laplace (s = 1) on 20/42. SEC rescues 11 carriers and loses 2.
  - Per study, SEC against raw: SEC1 9–6, SCL3 9–4, SEC3 4–5, SEC4 3–1, SEC5 4–4.
- **Per-task factors are load-bearing.** One factor for all tasks (`bayes_s1`, M3) is not behind on 18/42. Its declared
  forecast, FM3, is decided in `m_checks.txt`.
- **K, the clip, is load-bearing on SEC4 + SEC5.**
  - Clipped 10/14 against unclipped 7/14 (rescued 3, lost 0).
  - Divergence: 5/14 unclipped against 2/14 clipped. The clip fired on 5/14 carriers.
- **W, the value 1/2.** SEC is within a step of the best calibrated multiplier λ\*_sec on 31/42 carriers. This is A1's
  location cost, and F1 decides it in `a1_a3.txt`.
- **E, the premise.**
  - The geometric-mean s exceeds 1 on 41/42 carriers.
  - The median over carriers of the per-carrier median s is 25.51 (range 0.8691 to 5.97e+04).
  - s > 1 is the direction Kunstner et al.'s error calls for: the EF understates the curvature once the task is fit.
  - **The direction does not single out that error.** s > 1 would also come from a larger curvature on the task's early
    path than at its end, which is M2's question (FM2). It would also come from a gap between diagonal and full curvature.
    M1, which uses the true Fisher (the known fix for the EF), bears on it too.
- **N, the task-size weights,** is not tested. No recorded arm removes it alone.
- **The mechanism checks will add the rest** (`m_checks.json`; pending):
  - **M1** (true-Fisher Laplace) tests whether the known fix, "use the Fisher, not the EF" (Kunstner; the Fisher equals the
    GGN for softmax cross-entropy, a11:23), does the calibration's job.
  - **M2** (endpoint curvature) tests whether the secant's path averaging matters, or only the curvature's size. It also
    bears on E.
  - **M4** (arc secant) is the CRR-guided variant. It is reported under FM4 and does not enter F11 (§5).
  - **M5 and M6** (Amendment 2: freeze the capped coordinates only; freeze everything) test whether the clip's freeze,
    rather than the importance, does the work. `a11_grade.py` prints them when `m_checks.json` carries them.

## 4. CRR inside SEC, beside it, and in the context of discovery

**Inside SEC: nowhere.** No CRR operation is performed (§2), so none can be load-bearing.

**Beside SEC: the H-EQ rule, as an undeclared report that decides nothing** (`a11_grade.txt` [5], marked REPORT).
- **What it is.** The same `run()` carries mode `eq`, the CRR-proper equanimity rule at Ω = 1. It is a comparison arm,
  not an ingredient of SEC.
- **The counts depend on which SEC arm it is set against.** Not behind the tuned λ:
  - against the unclipped SEC, over the 42 carriers: rule 29/42, SEC 29/42. They differ on 5 carriers each way. Per
    study, SEC against the rule: SEC1 9–8, SCL3 9–7, SEC3 4–5, SEC4 3–5, SEC5 4–4;
  - against the SEC arm each study scored (the clipped SEC on SEC4 and SEC5, the unclipped SEC elsewhere): rule 29/42,
    SEC 32/42;
  - on SEC4 + SEC5 alone: rule 9/14, clipped SEC 10/14, unclipped SEC 7/14.
- **Why the arm matters.** The unclipped SEC diverged on 5 of these 14 carriers. The rule's norm ratio sizes the past
  pull to the present gradient, so it bounds itself (up to the rule's cap).
- **Why it is not SEC's explanation:**
  - it is not an ingredient of SEC;
  - its norm ratio sets the size of the past pull whatever the number of tasks the importance has accumulated, so it drops
    the task count that SEC keeps;
  - the record finds it reduces to a fixed replay weight (EQX-1);
  - the record finds it is the VQGAN adaptive weight without smoothing (`Continuous_Learning/ADAM_AND_PRIOR_ART.md`).

**In the context of discovery: a route, not a mechanism.**
- **The questions that led to SEC were put in CRR's terms.** Prompt-log entry 111 asks "what determines a learning unit".
  Entry 118 reads "Bayes λ = 1 simply assumes F is already right" and "The Ω = 1 rule corrects the units at every step"
  (the second found verbatim by `a11_grade.py`, part (e)).
- **The pre-registration names three jobs.** `prereg/sec1/PREREG.md` split the tuned λ's job into "fixing the Fisher's
  units", "keeping the task count" and "staying below the stability edge". Those are S, N and K above.
- **The Cramér–Rao reading makes the same point in A1′'s words** (`docs/notes/2026-09-25_cramer_rao_reading.md`, CR5).
  - With the true Fisher, weight 1 in Cramér–Rao units is exact sequential Bayes.
  - With the Fisher scaled by c = 0.1, the right weight is 1/c: "best lambda 10.0000 (1/c = 10.0000)". Weight 1 then
    misses the mode by 10.3668 Cramér–Rao units (`theory/checks/cramer_rao_reading.txt`).
- **But the content is Laplace's.** The note grades itself R0–R2, and it post-dates SEC1 (2026-09-25 against
  2026-09-23).
- **A1′'s operational unit is absent from SEC's code.** CRR.md defines it as σ = 1.4826·MAD of an occasion statistic, and
  SEC computes none of it (§2).
- **Summary.** CRR named the defect ("units") and pointed at it.
  - **Each part of the repair is published:** the BB secant, the empirical Fisher and its scale error, the Laplace
    recursion and AR1's clip.
  - **Their combination was not found stated in any source.** That combination is the per-task secant calibration S,
    graded PARTLY REDUNDANT; the nearest sources are Ritter, Martens, RWalk and SI.

## 5. M4: why it does not decide F11

- **What M4 is.** The declared arc secant: c_arc = Σ_k ⟨Δg_k, Δθ_k⟩ / Σ_k ‖Δθ_k‖² over five segments. It is SEC's
  secant with more points.
- **It is still BB's least-squares secant.** `a11_grade.py` checks that c_arc is the least-squares solution of BB's secant
  equation (1/η)·Δθ_k = Δg_k stacked over the five segment pairs ([2]; seeded instance, equal to 1e-12). This is Tan et
  al.'s residual minimisation (a11:13) applied to several pairs.
- **It is not an arc length either.** As implemented in `m_checks.py`, it calls no `sqrt`, `norm`, `path_length`,
  `arc_length` or `kl_step` ([2]). It reads the path's intermediate window means, but it sums squared segment
  displacements, not segment lengths.
- **So it does not enter F11.**
  - F11 is about SEC's code, and M4 is not SEC's code.
  - By the same D6/H-T1 test that [3] applies to SEC, M4 performs no CRR-proper operation. A win by M4 could not make a
    CRR-proper ingredient load-bearing.
- **Where M4 is decided.**
  - Its declared forecast is FM4: within a step of the clipped SEC on at least 80 % of carriers, a TIE.
  - Its declared consequence is the SEC6 carry rule: it may be carried as a two-sided candidate if it is ahead by more
    than a step on at least 3 carriers.
  - `m_checks.txt` decides both. `a11_grade.txt` [6] repeats them as a REPORT once `m_checks.json` exists.
  - If M4 were carried, the one place where reading more of the path did measurable work would be a least-squares BB
    secant: optimisation's arithmetic.

## 6. Sources (fetched 2026-09-30; versions in `checks/claims_a11.py`; fetch record in `sources/`)

| source | version | ingredients |
|---|---|---|
| Kunstner, Balles & Hennig, *Limitations of the Empirical Fisher Approximation for Natural Gradient Descent* | arXiv 1905.12558 v3 | F, E, S |
| Martens, *New insights and perspectives on the natural gradient method* | arXiv 1412.1193 v11 (JMLR version) | F, E, S |
| Kirkpatrick et al., *Overcoming catastrophic forgetting in neural networks* (EWC) | arXiv 1612.00796 v2 | W, F, T |
| Huszár, *On Quadratic Penalties in Elastic Weight Consolidation* | arXiv 1712.03847 v1 | W, N, E |
| Ritter, Botev & Barber, *Online Structured Laplace Approximations for Overcoming Catastrophic Forgetting* | arXiv 1805.07810 v1 | W, N, S |
| Barzilai & Borwein, *Two-Point Step Size Gradient Methods*, IMA J. Numer. Anal. 8(1):141–148 | Crossref record only (article HTTP 403) | C |
| Tan, Ma, Dai & Qian, *Barzilai-Borwein Step Size for Stochastic Gradient Descent* (the BB formula, freely readable) | arXiv 1605.04131 v2 | C |
| Maltoni & Lomonaco, *Continuous Learning in Single-Incremental-Task Scenarios* (AR1) | arXiv 1806.08568 v3 | K |
| Zenke, Poole & Ganguli, *Continual Learning Through Synaptic Intelligence* | arXiv 1703.04200 v3 | C, S |
| Schwarz et al., *Progress & Compress* (online EWC) | arXiv 1805.06370 v2 | N |
| Chaudhry et al., *Riemannian Walk for Incremental Learning* (RWalk) | arXiv 1801.10112 v3 | R, S |

**How to rerun.**
- `uv run python SEC_Analysis/checks/verify_a11.py > SEC_Analysis/checks/verify_a11.txt` needs the raw texts under
  `/tmp/claude-0/sec_an_src/`. They can be refetched with `sources/fetch.py` and checked against `sources/SHA256SUMS.txt`.
- `uv run python SEC_Analysis/checks/a11_grade.py > SEC_Analysis/checks/a11_grade.txt` needs only the repository.
- Both reran byte-identical under `cmp`.
- Rerun `a11_grade.py` and re-pin its output once `checks/m_checks.json` exists, or whenever `m_checks.py` changes. This
  fills [6] and the M lines of [7]. F11's word does not depend on either file.
