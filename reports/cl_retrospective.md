# Retrospective — the continual-learning results of 2026-09-14, and the way forward

Written 2026-09-15 at the owner's request (`notebook/PROMPT_LOG.md` entry 16).
Every number quoted here is printed in `audit/recompute_2026-09-14.txt`
(from the archived jsonl) or `runs/eqx/score.txt`; nothing is quoted from
the archive's own ledger text or from memory.

The bundle in question is `archive/cl_ledger_2026-09-14/` (a second upload
of the same zip on 2026-09-15 was byte-identical, sha256 `df200c50…`, and
was not re-imported). It is context, not evidence; this document explains
why it read as evidence at the time.

## 1. What it claimed, in one line each

- **Equanimity (Ω = 1)**: a sharp, learning-rate-invariant optimum on three
  datasets; matches 100 % replay at 40 % less compute.
- **T1**: forgetting tracks Fisher path length better than endpoint
  displacement (R² 0.89 vs 0.76).
- **T2**: equanimity competitive with the published KL-to-base recipe.
- The compute claim via EMA self-distillation and the "no free parameters"
  claim were already retracted in the bundle itself.

## 2. Why each appeared to work, and what the recompute found

| claim | why it looked right on the day | what the recompute shows |
|---|---|---|
| "Ω = 1 is the sharp optimum in 6/6 landscapes" | It is — the landscapes reproduce exactly (`audit/recompute_2026-09-14.txt` §3). | The Ω axis relabels the *effective replay weight*: median w at Ω = 1 was 0.7–2.2, and the fixed-w grid on KMNIST (w = 1: 61.42, 2: 60.79, 4: 52.51) traces the same curve. A sharp optimum in w is standard replay behaviour, not a theory value. |
| "Fixed w = 1 is within 1.0 of adaptive (61.4 vs 62.5) → adaptivity irrelevant" and, simultaneously, the rule being reported as a result | The two rounded numbers differ by 1.1; the full-precision gap is **1.0333**, per seed +1.00, +0.42, +1.68. | A verdict sitting on its own threshold, read both ways. §7's rule ("never rounded alone at a boundary") exists for this case. The cross-dataset fixed-w sweep that would have settled it (`results_adv2`) was lost to a container restart and never re-run. |
| "Estimator finalised post hoc on KMNIST seed 0; all else held out" | Honestly labelled. | Under the *first* estimator (`ratio=unbiased`) the optimum was Ω = 2, not 1; the estimator that put it at Ω = 1 was chosen after seeing that. The theory value moved with the estimator (R3). Q1–Q4 as pre-registered (r = 0.05) were never run at all. |
| "T1 PASS: R² 0.887 / 0.901 vs 0.756" | The numbers reproduce (log-log fits, `audit/…` §5 T1). | The endpoint on the **old** probe, listed as "near-tautological, reported not a candidate", gives R² **0.9935** on the same runs. The path did not beat the endpoint; it beat the wrong endpoint. The convex-learner lemma (`theory/checks/verify_scope_math.py`) shows E_old is a sufficient statistic for forgetting, so this had to happen. lr was also not controlled (five lrs, all monotone in C and F). |
| "T2: EQ dominates ER(0.25) and KL-to-base on the plasticity axis" | The Pareto reading is true of the means. | The pre-registered pass line (within 0.03 bpb of KLrep on D0) was missed by 0.063 and re-read as "off the frontier" — §10's "reinterpret a fail" case. The λ = 1/3 rows cannot be attributed from the log (the script never printed λ). |
| "40 % less compute at equal accuracy" | True on KMNIST and MNIST for EQ vs ER(1.0). | Also true for **fixed w = 1** (61.42 vs 61.14): the saving belongs to summing two batch means with a small replay batch — standard ER-sum — not to Ω. False on Fashion-MNIST (−7.85). |
| Every "prereg hash in the shell logs" | The preregs were written before the runs. | No `HASH.txt`, no `.ots`, no tag in the bundle; the ordering is asserted, not witnessed (R2). |

Three mechanisms, then, made the bundle read as positive: **a baseline that
could not win** (E_new instead of E_old; no cross-dataset fixed w), **a
boundary read in the favourable direction** (1.03 → "within 1.0"), and
**a criterion moved after the data** (the estimator; the T2 reinterpretation).
None was hidden — the bundle labels most of them — but labelling a defect is
not the same as scoring it.

## 3. What replaced it under the protocol (2026-09-15)

Study **EQX** (`prereg/eqx/`, `reports/eqx.md`): the same rule on three
datasets no CRR work had touched, hashed and pushed before download, with
the fixed-w grid *and* the constant the rule reduces to in the baseline set.
Result: Ω = 1 reduces to a fixed weight (median effective w 1.04–1.12) and is
**behind** the best constant on 3/3 datasets; never ahead of ER-sum by a
resolvable step; the Euclidean ratio beats the Fisher ratio. Rows EQX-1..5.

The path-length claim was not re-run: the recompute (row ARC-T1b) already
shows the fair baseline wins on the only runs ever made, and the surrogate
gate (`gate_T1`, S-H) shows why.

## 4. How to develop the continual-learning research from here

Under the protocol as it now stands (Daniel Friedman's restructure, CI, and
docs merged 2026-09-15; theory v3.1 signed), and with the owner's
decisions on #13, #15 and #17:

**T1x — the open question that still has content.** RL's Razor's own data
show forgetting collapsing onto endpoint KL; the prior-art map
(`archive/…/prior_art_map_2026-09.txt` Part 4) confirms no one has scored
*cumulative* Fisher length as the predictor. A fair T1x is: lr fixed, path
length varied ≥ 3× by schedule (constant, sawtooth, cosine-restart, noise,
loop), scored out-of-sample, against **E_new, E_old and the EWC
Fisher-weighted endpoint distance**. `gate_T1` (S-H must fail, S-H2 must
pass) is open. Under v3.1 [A8], T1x-4 — predict *final* forgetting from the
first-half path — becomes admissible once `gate_F` exists. If E_old wins
here too, the path-length idea is finished for learners; that is a
legitimate result.

**EQ-3 — the one line of the equanimity study still unscored.** Framework
baselines (ER-ACE, DER++, CLS-ER, MEGA-I from Mammoth, commit pinned) on
Split-CIFAR-100 / TinyImageNet / an LM stream, seeds 0–4, on Daniel's 3.14
environment. Given EQX-1, the arm under test is a *fixed* replay weight
near 1, not an adaptive rule; the honest framing is "does the ER-sum family
with a small replay batch hold its own against the published methods," and
the theory has no stake in the answer.

**What Daniel's protocol adds that the bundle lacked**, and what each new
study must therefore carry: OTS-anchored, signed preregs (his machine can
reach the calendars; this environment cannot); `runs/phaseA` gate tables
and the gate-contract tests, so a control verdict cannot drift silently; CI
on every push; the `PREREG_TEMPLATE` fields for aggregation, denominator,
sidedness and seeds; `sign_test_units` for cross-unit scoring; and the
amplitude control scored by CI, fixed before use. The R13 prompt log
records what was asked for — including, on 2026-09-15, a request to remove
the null results, and its refusal.

**What to stop doing**, from the audit rows: reporting a mean where the
prereg said per seed; letting a threshold sit on a rounded number; changing
an estimator after a landscape has been seen; and treating "the baseline is
near-tautological" as a reason to exclude it — that is precisely the
baseline that must be beaten.

## 5. One sentence

The 2026-09-14 results were not fabricated and not careless; they were what
a sound-looking pipeline produces when the baseline that can win is left
out and the boundary is read in the theory's favour — and the protocol that
now guards against both is the reason the next positive, if it comes, will
mean something.
