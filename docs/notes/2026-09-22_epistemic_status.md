# Epistemic status of the pipeline (2026-09-22, prompt-log entries 82–83)

A note to the auditor and the owner. It quotes the ledger and the pinned outputs and nothing else (R8, R1). Its purpose
is to state, once and in one place, what the repository's record does and does not establish, and why a framework that
has been refuted in parts stands in a better epistemic position than one that cannot be refuted at all.

## 1. What the record holds

**Registered, held-out rows with a PASS.** Two, both PASS-0 (provisional), both on one kind of system (tabular
class-incremental learning) and one rule (the normalised penalty step at Ω = 1 on an online-EWC past term):

| row | what it says | why it is PASS-0 and not more |
|---|---|---|
| EQ2-1b | the rule at Ω = 1 is not behind the tuned λ by a resolvable step on three unseen carriers, and no single λ transfers | fragile (flips in 6 of 27 sensitivity cells); a pre-registered control violated (DER++ on 2/3 carriers); push-timestamp anchor only; the replication EQ3 failed on 1 of 6 carriers (row EQ2-1c) |
| EQ3-I | learning-rate × batch invariance on one carrier: not behind in 5 of 5 cells | an invariance row, not a comparative win: ahead by a step in 1 of 5 cells; weakly anchored |

Every other PASS in the ledger is on seen data (ARC-A2, ARC-A3, ARC-T1: in-sample, learning rate not controlled) or
on a control line (MEAS2-3, a comparison of two boundary rules on a carrier where H-L5 itself fails on both). The
held-out rows scored with a threshold in other domains failed: MEAS2-1, H-L5 at 0/17 cities; EQX-2, the replay rule's
Ω = 1 not the best grid point; EQ3-1, the replication, FAIL on 1/6 with both controls violated. No row is PASS-1. No row
is PASS-2. Nothing may be quoted outside the ledger as a finding.

**Retrodictions.** 197 rows across some fifty fields: 41 CONSIST, 86 DESCR, 20 FAILS, 9 TENSION, 41 OPEN; no SHARP,
and SHARP retired for retrodictions because every coherence integral has a system-supplied velocity and every unit is
the system's own (`ontology/03_review_of_findings.md` §3). Each CONSIST row prints what produced its number, and the
line reads: the Fisher metric of the Bernoulli family, Fubini–Study, thermodynamic length, the Riccati equation, the
Omori law, normal-form scaling.

**Synthesis re-reads.** 138 runs before the FEP batches: 2 ADDS (candidates), 34 REDUNDANT-IG, 50 REDUNDANT-DOMAIN,
17 WRONG, 21 INTERNAL, 3 UNSTATED; the ten FEP rows add 1 ADDS, 1 PROPOSES, 2 REDUNDANT-IG, 1 REDUNDANT-DOMAIN, 5 WRONG.
Three ADDS candidates in 148 runs, none yet judged by a named expert.

## 2. The technical statement

**2.1 Compatibility is inherited, not earned.** CRR's computable core is the Fisher–Rao geometry: the metric (A1),
the arc (D2), the chord (D3), the surplus (D4). Those are information geometry's, not CRR's (CLAUDE.md §7 says so, and
the synthesis class was built on that line). A retrodiction that reproduces the two-level thermodynamic length π/2, the
Kalman steady state or the Hopf amplitude reproduces it because CRR's arc *is* Weinhold's and Crooks's length and CRR's
chord *is* Wootters's distance. Agreement across fifty fields is therefore the consistency of a borrowed geometry with
the domains that already use it. It is a real property of the equation set (a wrong geometry would have failed), and it
is not evidence for anything CRR adds to the geometry.

**2.2 The proper content is what can be wrong.** CRR's own contributions are the cut and the occasion (A3/D5),
regeneration by a bounded mean (A6), tense (A7/A8), and the four hypotheses that turn them into predictions (H-CUT,
H-L5, H-T1, H-EQ). The synthesis class asked, row by row, whether a proper ingredient did the work of a CONSIST row,
and in 84 of 127 cases it did not. Where a proper ingredient was load-bearing, the record is the 20 FAILS and 17 WRONG,
the held-out failures of H-L5 and the reductions of H-EQ, and three ADDS candidates. In Popper's terms this is the
framework's empirical content: the set of observations it forbids. The forbidden observations have been observed, and
the ledger records them as rows. A framework whose content has been tested and found wanting in most places, and
standing in a few, is in the normal condition of a scientific hypothesis under audit.

**2.3 The comparison with the free-energy principle.** The FEP's core, that a system which persists can be described
as minimising a variational free energy under some generative model, forbids no observation: any persisting system
admits such a description, which is why its authors call it a principle rather than a theory. Under this repository's
protocol that core would not be refuted; it would be removed at the gate (R4), because a hypothesis that holds on a
surrogate with no content is deleted as not being about the theory, exactly as the salience hypothesis SAL was removed
on 2026-09-17. What the FEP has that CRR lacks is a large, tested shell of process theories (predictive coding, active
inference models of particular tasks, precision as attention), built by many groups. What CRR has that the FEP's core
lacks is a core that can fail, and has. Under R7 the FEP's process theories would meet the same reduction test that
caught the replay rule: an active-inference model with a per-domain generative model is a tuned weight in another form,
and where it ties the matched Bayesian decision-theoretic model with information gain added, the ledger row would read
"reduces to Bayesian decision theory", as batch 28 row 5 already reads the epistemic term as a chord. Neither framework
has a PASS-1 in this repository, and the repository has not tested the FEP's shell. The claim of this note is narrower:
a framework that has been refuted in parts has demonstrated content; a framework that cannot be refuted has not, and
the second condition is not the safer one.

**2.4 The limits of the pipeline itself.** Stated so that the auditor does not have to find them:

- Anchoring is push-timestamp only. OpenTimestamps calendars are unreachable from the execution environment and tag
  pushes are refused; every attempt is recorded. No row can rise above PASS-0 until the two-person protocol or a
  re-run on a second machine (`docs/ROADMAP_2026-Q4.md` §1.2).
- One operator wrote the hypotheses, the surrogates, the gates, the tolerances and the tests. The harness tolerances
  (1 % for T-G and T-N) and the surrogate battery are choices, named but not independently justified.
- No frozen script has been run by a second person. The ADDS candidates await a named expert who has not been named.
- The in-sample tuned baselines favour the baseline by design (R7); the resolvable step is max(1 point, 2 SE) on five
  seeds, which is coarse; the sensitivity tables are the only guard against a pass that lives in one cell, and two of
  the three EQ passes were fragile by that guard.
- The agent's own corrections are logged (65 entries) because first runs contradicted drafted text repeatedly. That
  is the protocol working, and it is also evidence of how easily a drafted sentence outruns its numbers.

**2.5 The standing summary.** Internally consistent, reproducible byte for byte, adversarially self-checked,
externally unverified, weakly anchored. Compatible with information geometry everywhere; refuted where its own
content was load-bearing, except for three candidates and one provisional, fragile, once-failed-to-replicate pass.

## 3. The same thing for a fifth grader

We had a small set of rules and we checked them against about two hundred things scientists already know. The rules
agreed with the textbooks a lot. Then we asked a harder question: was it *our* rules that got the answer right, or was
it the ordinary mathematics inside them that everybody already uses? Most of the time it was the ordinary mathematics.
When it was really our own rules doing the work, they were usually wrong, and a few times they might be right, and
those few are waiting for an expert to look.

We also made real predictions ahead of time, sealed them, and then looked at new data. Most of those predictions
failed. One of them held, but only just: it wobbles if you change a setting, one of its safety checks failed, and
when we tried it again on new data it failed on one dataset out of six. So we call it "provisional", which means
"maybe, not yet".

Here is the important part. Being wrong a lot is not the worst thing a set of rules can be. The worst thing is to be
a set of rules that *cannot* be wrong, because then it is not saying anything. The other big theory we compared ours
with, the free-energy principle, is built so that no experiment can ever catch it out; its own inventors say so. Our
rules can be caught out, and they were, in writing, with the numbers kept. That is what makes them worth testing
further. A rule that can lose is a rule that can also win; a rule that can never lose can never win either.

And one more honest thing: the people checking the rules were the same people who wrote them, and the seals we put on
our predictions are the weakest kind. Until someone else runs the same scripts on their own computer, everything here
is "we say so, and here is how you can check".
