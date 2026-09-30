# A11: is SEC explained by CRR, Bayes, optimisation or information geometry? (a code reading)

**The question.** Analysis A11 of `DECLARATION.md` (pushed at 5f64b5f; prompt-log entry 257), with forecast F11.

**Status.**
- This is a post hoc reading of code and of records already opened. It adds no ledger row, and no word here is a PASS.
- Every number below is printed by one of these pinned outputs:
  - `checks/a11_grade.txt`, from `checks/a11_grade.py`;
  - `checks/verify_a11.txt`, from `checks/verify_a11.py`;
  - `theory/checks/cramer_rao_reading.txt`, where it is named.
- Every HOLDS, FAILS, REDUNDANT and "load-bearing" is computed by `a11_grade.py` from those numbers (R15).
- **The sources** were fetched on 2026-09-30, and their versions are listed in `checks/claims_a11.py` (R10).
  - `verify_a11.txt`: 47 of 47 quotes found verbatim, from 26 claims across 11 sources.
  - The extracted texts are kept outside the repository, under `/tmp/claude-0/sec_an_src/`. `verify_a11.txt` ends with
    each file's sha256.
- **Barzilai & Borwein 1988 was not read.** The DOI (10.1093/imanum/8.1.141) redirects to academic.oup.com, which returned
  HTTP 403 behind a Cloudflare challenge.
  - Crossref's record confirms the title, journal and pages (claim a11:16).
  - The BB step formula is quoted instead from Tan, Ma, Dai & Qian 2016 (arXiv 1605.04131 v2), which is freely readable
    and cites Barzilai & Borwein as its reference [3] (a11:13, a11:15).

## The answer, as printed

- **F11: PENDING.** Its deciding clause is the one CRR-guided variant, M4 (the arc secant), which needs `checks/m_checks.json`.
  That file has not been written yet.
- **The static part holds.** SEC's code path performs **0 of the 8** CRR-proper clauses (CLAUDE.md §7). **None of its 9**
  ingredients (0 of 9) is CRR-proper.
- **Parts (a)–(e) of the forecast all hold:**
  - (a) the weight 1/2 is the Laplace weight;
  - (b) the calibration is a Barzilai–Borwein secant that fixes the empirical Fisher's known scale error;
  - (c) the secant is a chord between window means, not an arc;
  - (d) the clip is AR1's;
  - (e) A1′ supplies only the name "units".
- **Where the ingredients come from** (`a11_grade.txt` [7]):

  | field | ingredients |
  |---|---|
  | Bayes | 2 |
  | information geometry | 3 |
  | optimisation | 2 |
  | optimisation + information geometry | 1 |
  | protocol | 1 |
  | CRR | 0 |

- **Every ingredient but one is REDUNDANT** (a verified source states it). The exception is the calibration itself, S,
  which is PARTLY REDUNDANT: no source found states it.
- **So SEC's explanation is Bayes, optimisation and information geometry.** CRR supplies a word ("units") and, in the
  context of discovery, a route to the idea (§4 below). No CRR operation does work in the code.
- If M4 is ahead of the clipped SEC by more than a step on at least 3 carriers, the printed word becomes F11 FAILS. §5
  says what that would and would not mean.

## 1. What the code does, line by line

**What was read.**
- `runs/sec4/frozen/sec1_score.py` `run()` (lines 169–230). This file is byte-identical in the frozen folders of SEC1,
  SCL3, SEC3, SEC4 and SEC5: one distinct sha256 (`a11_grade.txt` [1]).
- `runs/sec4/frozen/sec4_score.py` `run_guard()` (lines 58–114). This file is identical in SEC4 and SEC5.
- `a11_grade.py` finds each statement quoted below verbatim in the frozen text: 35 of 35.
- **Not read:** SEC3's own guard (`sec3_score.py`, mode `bayes_sec_g`, a raw-Laplace fallback). It is not one of the two
  functions A11 names.

**The ingredients.**

| id | ingredient | the code (sec1_score.py / sec4_score.py) | what it is | published source (verified) | grade |
|---|---|---|---|---|---|
| W | the weight 1/2 | `w = BAYES_W` (197) with `g_q = 2 * imp_used * dth` (195), step `lr * (g_p + w * g_q)` (205); `w = S.BAYES_W` (94) | the penalty is w·Δθᵀ imp Δθ; at w = 1/2 it is the Laplace quadratic ½ Δθᵀ H Δθ | Huszár eq. (6); Ritter: the multiplier's "natural value of 1" | REDUNDANT |
| N | task-size weighting, one penalty | `imp_bayes = imp_bayes + n_task * sc * f_task` (223), used as `imp_bayes / n_task` (181); `theta_star = theta_now` (224) | the Laplace recursion: task curvature = sample count × per-sample Fisher, summed, anchored at the latest task end; ÷ n_task puts it on the scale of the mean mini-batch loss | Huszár eq. (5), (11); Ritter eq. (7); online EWC (P&C, with a decay γ < 1: close) | REDUNDANT |
| F | per-sample empirical Fisher | `f += ce_loss_grad(net, Xtr[ii], ytr[ii])[1] ** 2` over 50 mini-batches, `f_task = f / N_FISHER * bs` (208–210) | squared gradients at the **training** labels: the empirical Fisher (EF). Squaring mini-batch means and multiplying by bs gives the gradient variance plus bs × the squared mean gradient (a mini-batch variant of Kunstner eq. 18) | Martens §11; Kunstner et al. | REDUNDANT |
| E | premise: the EF's scale error | none (a premise) | where the task is fit, the EF understates the curvature | Kunstner: "the EF goes to zero while the Fisher (and the corresponding GGN) approaches the Hessian"; Martens: the EF "doesn’t have the right “scale”" | REDUNDANT |
| C | the secant c_j | window sums (183, 190–191); `dth = e_th / n_e - s_th / n_s; dg = e_g / n_e - s_g / n_s` (217); `c = float(dg @ dth) / nn` (218) | 1/η of the BB step η = ‖s‖²/sᵀy, with s = Δθ and y = Δg taken between START- and END-window means | Tan et al. eq. (2.4) (the BB step); SGD-BB forms it from epoch-averaged stochastic gradients (close); SI (close) | REDUNDANT |
| R | ρ_j | `rho = float((f_task * dth) @ dth) / nn` (218) | the Rayleigh quotient of the diagonal EF along the same Δθ: the curvature the Fisher claims | RWalk: DKL ≈ ½ Δθᵀ F Δθ with the empirical Fisher | REDUNDANT |
| S | the calibration s_j = c_j/ρ_j | `s = c / rho`, else `s = 1.0` (219–220); applied as `sc` (222–223) | one scalar per task rescales that task's Fisher to the secant curvature, keeping the Fisher's shape | close: Ritter (one tuned multiplier, the same on every task's curvature term in the recursion); Martens (combining the EF with another curvature estimate to fix its scale); RWalk (observed over Fisher-predicted, then normalised to [0, 1], losing the scale); SI | **PARTLY REDUNDANT** |
| K | the clip | `cap = kappa / (lr * S.BAYES_W)` (67); `imp_used = np.minimum(imp_used, cap)` (77) | bounds lr·w·imp at κ = 0.5 | AR1: "if … the product η · λ · Fk is greater than 1 … we overshoot"; the λ bound 1/(η · maxF) | REDUNDANT |
| T | the task boundary | `tasks = [tuple(range(i, i + per_task)) …]` (175; 64) | the Fisher, the secant and the anchor are all taken at the stream's task switches | EWC: "we compute the Fisher information matrix at each task switch" | REDUNDANT |

**The chord, from the code.** `a11_grade.py` parses the training step loop and lists every quantity summed in it. The list
is `e_g, e_th, k_step, s_g, s_th` in both functions ([2]).
- **The path enters the calibration only through two window means.** These are the START window (first ⌈0.1 × steps⌉) and
  the END window (last ⌈0.1 × steps⌉). FS + FE = 0.20, so the middle 0.80 of the task's path is never read.
- **Δθ and Δg are differences of those means, so c_j is a chord quantity.** No per-step length is summed, so it is not
  D2's arc and not D6's Σ√(2·KL_t).
- **Its metric is Euclidean** (`dth @ dth`), so it is not D3's Fisher–Rao chord either. It is a Barzilai–Borwein secant.

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

Each clause's defining sentence is found verbatim in `theory/CRR.md`, and `a11_grade.py` tests the code for its operation
([3]). None is performed.

| clause | what it requires | what SEC's code does | performed |
|---|---|---|---|
| A3/D5 | a cut at the antipode of an intrinsic phase | boundaries are the label schedule; no call to `antipodal_cuts` or `intrinsic_phase` | no |
| A6 | the next state seeded from a Fisher–Rao Fréchet mean of past occasion contents under MaxEnt weights, at bounded strength, "never an accumulated count" | the anchor is the last task's end state; the importance **is** an accumulated count (`imp_bayes += n_task * s * f_task`), bounded afterwards by AR1's clip | no |
| P2/P3 | occasion weights ∝ exp(βS_m) or q^k | task weights n_j·s_j (data count × calibration) | no |
| A1′/D1 | σ = 1.4826·MAD of one occasion statistic; ρ = half-turn extent / σ | no σ, no MAD, and 0 calls into `src/crr/instrument/core.py` (17 functions). The code's `rho` is the Fisher's Rayleigh quotient, not D1's resolution; only the letter is shared | no |
| H-L5 | CV of arc against CV of clock between events | nothing of the kind | no |
| D6/H-T1 | an arc: a per-step length summed along the path | only the START and END window sums (above) | no |
| H-EQ | w = Ω‖ḡ_present‖/‖ḡ_past‖ | SEC's weight is the constant 1/2; the norm ratio exists only under run()'s mode `eq`, a comparison arm | no |
| A7/A8 | prohibitions | the window sums reset at each task start, so the calibration uses only the task's own steps, as every online learner does | nothing to perform |

**Two name collisions to keep apart.**
- The code's `rho_j` is not D1's ρ.
- SEC4's κ (a step-size margin) is not A6's κ (a regeneration strength).

**One tension with A6, stated plainly.** SEC works with an accumulated count, which is Bayes: the posterior sharpens task by
task.
- **Where the count comes from.** The SEC1 pre-registration names "keeping the task count" as one of the tuned λ's three
  jobs.
- **Where it clashes with A6.** A6's letter forbids an accumulated count. SEC keeps it and bounds it with AR1's clip.
- **What SEC honours.** It keeps the spirit of A6's "bounded strength". It does not keep the form of A6.

## 3. Is each ingredient load-bearing? (the evidence that exists now)

**The rule used.** From the pinned records ([5]), an ingredient is LOAD-BEARING when the arm without it is not behind on at
least 2 fewer carriers than the arm with it. This reads the declaration's "at most 1 carrier fewer" tolerance in reverse. It
is a report rule and decides nothing.

- **S, the calibration, is load-bearing.**
  - SEC is not behind on 29/42 carriers, raw Laplace (s = 1) on 20/42. SEC rescues 11 carriers and loses 2.
  - Per study, SEC against raw: SEC1 9–6, SCL3 9–4, SEC3 4–5, SEC4 3–1, SEC5 4–4.
- **Per-task factors are load-bearing.** One factor for all tasks (`bayes_s1`, M3) is not behind on 18/42.
- **K, the clip, is load-bearing on SEC4 + SEC5.**
  - Clipped 10/14 against unclipped 7/14 (rescued 3, lost 0).
  - Divergence: 5/14 unclipped against 2/14 clipped. The clip fired on 5/14 carriers.
- **W, the value 1/2, sits where it should.** SEC is within a step of the best calibrated multiplier λ\*_sec on 31/42
  (A1's location cost).
- **E, the premise, points the way the literature predicts.**
  - The geometric-mean s exceeds 1 on 41/42 carriers.
  - The median over carriers of the per-carrier median s is 25.51 (range 0.8691 to 5.97e+04).
  - That is the direction Kunstner et al. give: the EF understates the curvature once the task is fit.
- **N, the task-size weights,** is not tested. No recorded arm removes it alone.
- **The mechanism checks will add the rest** (`m_checks.json`; pending):
  - **M1** (true-Fisher Laplace) tests whether the known fix, "use the Fisher, not the EF" (Kunstner; the Fisher equals the
    GGN for softmax cross-entropy, a11:23), does the calibration's job.
  - **M2** (endpoint curvature) tests whether the secant's path averaging matters, or only the curvature's size.
  - **M4** (arc secant) is the CRR-guided variant.
  - **M5 and M6** (Amendment 2: freeze the capped coordinates only; freeze everything) test whether the clip's freeze,
    rather than the importance, does the work. `a11_grade.py` prints them when `m_checks.json` carries them.

## 4. Where CRR does real work, and where it does not (a fair account)

**Inside SEC: nowhere.** No CRR operation is performed (§2), so none can be load-bearing.

**Beside SEC: the H-EQ rule does real work of its own, as a different rule.**
- **Its count.** The same `run()` carries mode `eq`, the CRR-proper equanimity rule at Ω = 1. Over the 42 carriers it is
  not behind on 29/42, SEC's own count. The two differ on 5 carriers each way. Per study, SEC against the rule: SEC1 9–8,
  SCL3 9–7, SEC3 4–5, SEC4 3–5, SEC5 4–4 ([5]).
- **It shares one property with SEC.** A gradient-norm ratio makes the penalty invariant to the Fisher's scale (up to the rule's
  cap), and so does SEC's calibration.
- **It is still not SEC's explanation:**
  - it is not an ingredient of SEC;
  - its norm ratio sets the size of the past pull to the present gradient's, however many tasks the importance has
    accumulated, so it drops the task count that SEC keeps;
  - the record finds it reduces to a fixed replay weight (EQX-1);
  - the record finds it is the VQGAN adaptive weight without smoothing (`Continuous_Learning/ADAM_AND_PRIOR_ART.md`).
- **What the tie shows.** On these seen carriers, the one CRR-proper weight rule in the same code is not behind as often as
  SEC.

**In the context of discovery: a route, not a mechanism.**
- **The questions that led to SEC were put in CRR's terms.** Prompt-log entry 111 asks "what determines a learning unit".
  Entry 118 reads "Bayes λ = 1 simply assumes F is already right" and "The Ω = 1 rule corrects the units at every step."
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
- **Summary.** CRR named the defect ("units") and pointed at it. The repair is a BB secant on the EF inside the Laplace
  recursion, all published, plus AR1's clip.

## 5. What M4 can and cannot decide

- **What M4 is.** The declared arc secant: c_arc = Σ_k ⟨Δg_k, Δθ_k⟩ / Σ_k ‖Δθ_k‖² over five segments. It is SEC's
  secant with more points.
- **It is still BB's least-squares secant.** `a11_grade.py` checks that c_arc is the least-squares solution of BB's secant
  equation (1/η)·Δθ_k = Δg_k stacked over the five segment pairs ([2]; seeded instance, equal to 1e-12). This is Tan et
  al.'s residual minimisation (a11:13) applied to several pairs.
- **It is not an arc length either.** It reads the path's intermediate window means, but it sums squared segment
  displacements, not segment lengths.
- **What the declared rule then says.**
  - **M4 ahead of the clipped SEC by more than a step on at least 3 carriers:**
    - the declared rule counts it as load-bearing and prints F11 FAILS;
    - M4 becomes the one place where reading the path, the CRR-guided idea, did measurable work;
    - SEC6 may carry it as a two-sided candidate (DECLARATION.md, "What the results may change");
    - its arithmetic would still be BB's.
  - **M4 ahead on fewer than 3 carriers:** F11 HOLDS and part (f), "rung R1 (inherited) at best", holds with it.

## 6. Sources (fetched 2026-09-30; versions in `checks/claims_a11.py`)

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
  `/tmp/claude-0/sec_an_src/`.
- `uv run python SEC_Analysis/checks/a11_grade.py > SEC_Analysis/checks/a11_grade.txt` needs only the repository.
- Both reran byte-identical under `cmp`.
- Once `checks/m_checks.json` exists, rerun `a11_grade.py` and re-pin its output. F11's headline word is then printed by
  the script.
