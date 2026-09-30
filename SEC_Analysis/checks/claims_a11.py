"""SEC_Analysis A11 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; prompt-log entry 257): the published sources for each
load-bearing ingredient of SEC's code (runs/sec4/frozen/sec1_score.py run(), runs/sec4/frozen/sec4_score.py run_guard()).

Every quote is copied from the text that pymupdf 1.28.2 extracted from the fetched PDF (arXiv current version), fetched
2026-09-30 through the session proxy. Raw files live outside the repository under /tmp/claude-0/sec_an_src/ (`raw_file` is
relative to that root); their sha256 is in /tmp/claude-0/sec_an_src/SHA256SUMS.txt and the fetch record (URL, version,
date, HTTP status) in /tmp/claude-0/sec_an_src/FETCH_LOG.txt. Formulae are quoted as the extractor emitted them, symbol by
symbol in reading order (a fraction a/b comes out as "a b", a sum as "X" or "P"). Checked by SEC_Analysis/checks/verify_a11.py.

Barzilai & Borwein 1988 (IMA J. Numer. Anal. 8(1):141-148, doi 10.1093/imanum/8.1.141) was NOT read: doi.org redirects to
academic.oup.com, which returned HTTP 403 with a Cloudflare challenge page on 2026-09-30. Its bibliographic record is
quoted from Crossref's metadata (api.crossref.org, HTTP 200). The BB step formula is quoted from Tan, Ma, Dai & Qian 2016
(arXiv 1605.04131 v2), a freely readable source that states it and cites Barzilai & Borwein as its reference [3].

Fields: id; ingredient (the code ingredient the claim bears on, SEC_Analysis/checks/a11_grade.py INGREDIENTS: W the weight
1/2, N the task-size weighting and single accumulated penalty, F the per-sample empirical Fisher, E the empirical Fisher's
scale error (the premise the calibration corrects), C the secant c_j, R rho_j, S the calibration s_j = c_j / rho_j, K the
clip, T the task boundary where the Fisher is taken); role (how the source reads against the ingredient: 'states' = the
source states the ingredient as SEC's code uses it; 'close' = it states something near it that differs in a named way;
'bears' = context or attribution, not the ingredient itself; 'contradicts'); source; version; url; quote (list); raw_file;
agent_note (the agent's reading, not the source's words).
"""

R = 'src/'
EWC = ('Kirkpatrick et al., Overcoming catastrophic forgetting in neural networks (EWC)', 'arXiv v2, 25 Jan 2017',
       'https://arxiv.org/abs/1612.00796v2', R + 'pdf_1612.00796v2.txt')
HUS = ('Huszar, On Quadratic Penalties in Elastic Weight Consolidation', 'arXiv v1, 11 Dec 2017 (only version)',
       'https://arxiv.org/abs/1712.03847v1', R + 'pdf_1712.03847v1.txt')
RIT = ('Ritter, Botev & Barber, Online Structured Laplace Approximations For Overcoming Catastrophic Forgetting',
       'arXiv v1, 20 May 2018 (only version)', 'https://arxiv.org/abs/1805.07810v1', R + 'pdf_1805.07810v1.txt')
KUN = ('Kunstner, Balles & Hennig, Limitations of the Empirical Fisher Approximation for Natural Gradient Descent',
       'arXiv v3, 8 Jun 2020 (v1 29 May 2019)', 'https://arxiv.org/abs/1905.12558v3', R + 'pdf_1905.12558v3.txt')
MAR = ('Martens, New insights and perspectives on the natural gradient method', 'arXiv v11, 19 Sep 2020 (official JMLR version)',
       'https://arxiv.org/abs/1412.1193v11', R + 'pdf_1412.1193v11.txt')
TAN = ('Tan, Ma, Dai & Qian, Barzilai-Borwein Step Size for Stochastic Gradient Descent', 'arXiv v2, 23 May 2016',
       'https://arxiv.org/abs/1605.04131v2', R + 'pdf_1605.04131v2.txt')
BBX = ('Barzilai & Borwein, Two-Point Step Size Gradient Methods, IMA J. Numer. Anal. 8(1):141-148 (1988): Crossref record only',
       'Crossref metadata fetched 2026-09-30 (the article itself: HTTP 403 at academic.oup.com)',
       'https://api.crossref.org/works/10.1093/imanum/8.1.141', R + 'bb_crossref.json')
AR1 = ('Maltoni & Lomonaco, Continuous Learning in Single-Incremental-Task Scenarios (AR1)', 'arXiv v3, 22 Jan 2019',
       'https://arxiv.org/abs/1806.08568v3', R + 'pdf_1806.08568v3.txt')
SI = ('Zenke, Poole & Ganguli, Continual Learning Through Synaptic Intelligence', 'arXiv v3, 12 Jun 2017 (ICML 2017)',
      'https://arxiv.org/abs/1703.04200v3', R + 'pdf_1703.04200v3.txt')
PC = ('Schwarz et al., Progress & Compress: A scalable framework for continual learning (online EWC)', 'arXiv v2, 2 Jul 2018 (ICML 2018)',
      'https://arxiv.org/abs/1805.06370v2', R + 'pdf_1805.06370v2.txt')
RW = ('Chaudhry et al., Riemannian Walk for Incremental Learning: Understanding Forgetting and Intransigence (RWalk)',
      'arXiv v3, 14 Aug 2018', 'https://arxiv.org/abs/1801.10112v3', R + 'pdf_1801.10112v3.txt')


def _c(cid, ingredient, role, src, quote, note):
    return {'id': cid, 'ingredient': ingredient, 'role': role, 'source': src[0], 'version': src[1], 'url': src[2],
            'quote': quote, 'raw_file': src[3], 'agent_note': note}


CLAIMS = [
    # ---------------- W: the weight 1/2 (w = BAYES_W = 0.5 on w * dth' imp dth, i.e. the Laplace penalty 1/2 dth' H dth)
    _c('a11:1', 'W', 'states', HUS,
       ['log p(θ|DA, DB) ≈log p(DB|θ) −1 2 X i (NAFA,i + λprior) (θi −θ∗ A,i)2 + constant. (6)',
        'The above method of replacing a log posterior by a second order Taylor approximation around its maximum is known as '
        'Laplace’s method'],
       "Huszar's eq. (6): the Laplace approximation of the log posterior carries the factor 1/2 on the quadratic with the "
       "task's total curvature N_A F_A. SEC's penalty w * dth' imp dth with w = 1/2 (g_q = 2 * imp_used * dth) is this "
       "form with lambda_prior = 0."),
    _c('a11:2', 'W', 'states', RIT,
       ['its optimal value can inform us about the quality of our approximation: if it strongly deviates from its natural '
        'value of 1, our approximation is a poor one and over- or underestimates the uncertainty about the parameters.'],
       'The multiplier on each task\'s curvature has the natural (Bayes) value 1; in SEC\'s parametrisation w * dth\' imp dth '
       'that is w = 1/2.'),
    _c('a11:3', 'W', 'bears', EWC,
       ['L(θ) = LB(θ) + X i λ 2 Fi(θi −θ∗ A,i)2 (3) where LB(θ) is the loss for task B only, λ sets how important the old '
        'task is compared to the new one and i labels each parameter.',
        'with weights given by the Fisher information matrix times a scaling factor λ which was optimized by '
        'hyperparameter search.'],
       'EWC writes the penalty with lambda/2 and tunes lambda; it does not name lambda = 1 as the Bayes value (Huszar and '
       'Ritter do). Context for the tuned-lambda baseline SEC is scored against.'),
    # ---------------- N: task-size weighting imp_bayes = sum_j n_j s_j f_j, used as imp_bayes / n_task; one penalty at the last anchor
    _c('a11:4', 'N', 'states', HUS,
       ['H(θ∗ A) ≈NA · F(θ∗ A) + Hprior(θ∗ A), (5) where NA is the number of i. i. d. observations in DA,',
        'our derivation suggests that only a single penalty should be maintained, and it should be anchored at θ∗ S, where '
        'S is the latest task learned.',
        'can be updated as a moving sum, without saving the value of Ft,i for each task t.'],
       "The task's curvature is its sample count times the per-sample Fisher; the recursion keeps one penalty with the "
       'summed curvature, anchored at the latest task end. SEC: imp_bayes = imp_bayes + n_task * s * f_task; theta_star = '
       'theta_now; the division by n_task puts the penalty on the per-sample scale of the mean mini-batch loss.'),
    _c('a11:5', 'N', 'states', RIT,
       ['the precision matrix as the product of the number of data points and the average precision.',
        'Λt+1 = Ht+1(μt+1) + Λt (7)'],
       'The online Laplace recursion: the precision is data count times average precision, accumulated task by task.'),
    _c('a11:6', 'N', 'close', PC,
       ['where γ < 1 is a hyperparameter associated with removing the approximation term associated with the previous',
        'the overall Fisher is then updated as F ∗ i = γF ∗ i−1 + Fi (9)'],
       'Online EWC: one running Fisher at the latest anchor, with a decay gamma < 1. SEC is the gamma = 1 case with task-size '
       'weights (Huszar).'),
    # ---------------- F: the per-sample empirical Fisher f_task (true labels; bs x mean of 50 squared mini-batch gradients)
    _c('a11:7', 'F', 'states', MAR,
       ['An approximation of the Fisher known as the “empirical Fisher” (Schraudolph, 2002), which we denote by',
        'is commonly used in practical natural gradient methods. It is obtained by taking the inner expectation of eqn. 3 '
        'over the target distribution'],
       'Martens section 11 defines the empirical Fisher (expectation over the training targets). SEC\'s f_task uses the '
       'training labels ytr in ce_loss_grad.'),
    _c('a11:8', 'F', 'states', KUN,
       ['However, yn is a training label and not a sample from the model’s predictive distribution pθ(y|xn).',
        'Therefore, and contrary to what its name suggests, the empirical Fisher is not an empirical (i.e. Monte Carlo) '
        'estimate of the Fisher.'],
       'f_task is the EF in this sense: squared gradients of the loss at the TRAINING labels.'),
    _c('a11:9', 'F', 'bears', KUN,
       ['The empirical Fisher, as a sum of outer products of individual gradients, coincides with the non-central second '
        'moment of this estimate and can be written as N eF(θ) = Σ(θ) + ∇L(θ) ∇L(θ)⊤, Σ(θ) := cov[g(θ)]. (18)'],
       "SEC squares MINI-BATCH mean gradients (bs = 10) and multiplies by bs: per coordinate that is the gradient variance "
       "(the EF's centred part) plus bs times the squared mean gradient, a mini-batch variant of eq. (18). At a task's end "
       'the mean gradient is small, so f_task is close to the per-sample EF diagonal. The variant is an implementation '
       'detail; no source found states it for continual learning.'),
    _c('a11:10', 'F', 'bears', EWC,
       ['(b) it can be computed from first-order derivatives alone and is thus easy to calculate even for large models,'],
       "EWC's reason for the (diagonal) Fisher: first-order derivatives only. SEC keeps EQ4's estimator unchanged."),
    # ---------------- E: the premise: the EF's scale is wrong where the model fits (it understates the curvature)
    _c('a11:11', 'E', 'states', KUN,
       ['In such cases, the EF goes to zero while the Fisher (and the corresponding GGN) approaches the Hessian (Prop. 2).',
        'The EF is a good approximation of the Fisher at the minimum if this assumption is fulfilled (left panel), but can '
        'be arbitrarily wrong if the assumption is violated, even at the minimum and with large N.',
        'the empirical Fisher—unlike the Fisher—does not generally capture second-order information.'],
       "The known error: where the training samples are fit, the EF shrinks while the curvature does not. At a task's end "
       'the learner has fit the task, so the EF understates the curvature: the direction SEC\'s s_j > 1 corrects.'),
    _c('a11:12', 'E', 'states', MAR,
       ['The empirical Fisher differs from the usual Fisher in subtle but important ways, which as we show in Section 11.1, '
        'make it considerably less useful as an approximation to the Fisher, or as a curvature matrix to be used in 2nd-order '
        'methods.',
        'in order to correct for how the empirical Fisher doesn’t have the right “scale” (which is ultimately the reason why '
        'it does poorly in the example given at the end of Section 11.1).'],
       'Martens names the EF\'s scale as its defect as a curvature matrix.'),
    _c('a11:26', 'E', 'bears', HUS,
       ['Assuming that θ∗ A achieves near-perfect predictions on task A, we can approximate H as',
        'F(θ∗ A) is the empirical Fisher information matrix on task A [see e. g. section 11 of Martens, 2014]'],
       "The Laplace derivation SEC's weight comes from replaces the task's Hessian by N_A times the EMPIRICAL Fisher, under "
       'near-perfect predictions: the regime where, per Kunstner et al. (a11:11), the EF goes to zero while the Hessian does '
       'not. The scale error sits inside the derivation of the weight 1/2 itself.'),
    # ---------------- C: the secant c_j = <dg, dth> / <dth, dth>, dth and dg differences of END- and START-window means
    _c('a11:13', 'C', 'states', TAN,
       ['The most important feature of Bt is that it must satisfy the so-called secant equation: Btst = yt, (2.3) where '
        'st = xt −xt−1 and yt = ∇f(xt) −∇f(xt−1) for t ≥1.',
        'Instead, one can find ηt such that the residual of the secant equation is minimized, i.e.,',
        'which leads to the following choice of ηt: ηt = ∥st∥2 2 s⊤ t yt . (2.4)'],
       "The BB step eta = ||s||^2 / s'y. SEC's c_j = <dg, dth> / <dth, dth> is 1 / eta with s = dth, y = dg: the "
       "curvature along the displacement that the BB secant assigns. SEC uses it to rescale a Fisher, not as a step size."),
    _c('a11:14', 'C', 'close', TAN,
       ['SGD-BB takes the average of the stochastic gradients in one epoch as an estimation of the full gradient.'],
       "SGD-BB forms the secant from EPOCH-AVERAGED stochastic gradients and epoch-end iterates. SEC averages both the "
       "stochastic gradients and the iterates over a START and an END window of the task (ceil(0.1 x steps) each): the "
       'same device on two windows of one task.'),
    _c('a11:15', 'C', 'bears', TAN,
       ['[3] J. Barzilai and J. M. Borwein. Two-point step size gradient methods. IMA Journal of Numerical Analysis, '
        '8(1):141–148, 1988.'],
       "Tan et al. attribute the BB method to Barzilai & Borwein 1988, the reference the declaration names."),
    _c('a11:16', 'C', 'bears', BBX,
       ['Two-Point Step Size Gradient Methods', 'IMA Journal of Numerical Analysis', '141-148'],
       'The bibliographic record of the original (title, journal, pages) from Crossref. The article text was not reached '
       '(HTTP 403, Cloudflare challenge at academic.oup.com); the formula is quoted from Tan et al. (a11:13).'),
    _c('a11:17', 'C', 'close', SI,
       ['The quadratic surrogate loss (green) is chosen to precisely match 3 aspects of the descent dynamics on the original '
        'loss function: the total drop in the loss function',
        'ensures that the regularization term carries the same units as the loss L.'],
       "SI fits a quadratic to the task's own descent (loss drop over the squared net motion, per parameter) and uses it IN "
       'PLACE OF the Fisher. SEC fits one scalar curvature to the task\'s own descent (gradient change over the displacement) '
       'and uses it to RESCALE the Fisher. Both are path-fitted curvatures in the loss\'s units.'),
    # ---------------- R: rho_j = <f dth, dth> / <dth, dth>, the curvature the Fisher claims along the same displacement
    _c('a11:18', 'R', 'states', RW,
       ['DKL(pθ∥pθ+∆θ) ≈ 1 2∆θ⊤Fθ∆θ = 1 2∥∆θ∥2 Fθ 2, where Fθ, known as the empirical Fisher Information Matrix [1,18] at θ, '
        'is defined as:'],
       "The Fisher quadratic form along a displacement is (twice) the KL it predicts. rho_j is that form along dth over "
       "||dth||^2: the Rayleigh quotient of the diagonal EF along the chord. The code's name rho is NOT D1's rho (resolution "
       "= half-turn extent / sigma); only the letter is shared."),
    # ---------------- S: the calibration s_j = c_j / rho_j (fallback s_j = 1), applied to task j's Fisher in the recursion
    _c('a11:19', 'S', 'close', RIT,
       ['we instead place the multiplier on the Hessian of each log likelihood and update the precision as: Λt+1 = '
        'λHt+1(μt+1) + Λt (11)'],
       "A multiplier on each task's curvature term inside the Laplace recursion, where SEC puts s_j. Ritter tunes ONE lambda "
       'for all tasks by validation; SEC fits a separate s_j per task from the task\'s own path, with no validation data.'),
    _c('a11:20', 'S', 'close', MAR,
       ['with other quantities (such as an approximation of the diagonal of the Gauss-Newton/Fisher in the case of Schaul et '
        'al. (2013)) in order to correct for how the empirical Fisher doesn’t have the right “scale”'],
       'Combining the EF diagonal with another curvature estimate to fix its scale, in an optimiser preconditioner. SEC does '
       'this with a secant curvature, for a continual-learning penalty.'),
    _c('a11:21', 'S', 'close', RW,
       ['we define parameter importance as the ratio of the change in the loss to its influence in DKL(pθ(t)∥pθ(t+1)).',
        'This can be ensured by individually normalizing them to be in the interval [0, 1].'],
       "RWalk takes an observed-over-Fisher-predicted ratio along the path (per parameter, per step, accumulated), then "
       "normalises it to [0, 1] and ADDS it to the Fisher, discarding the scale. SEC's ratio is one scalar per task that "
       'MULTIPLIES the Fisher and keeps its scale (SPA1 graded this position S2 PARTLY REDUNDANT).'),
    _c('a11:22', 'S', 'close', SI,
       ['If the path integral (Eq. 3) is evaluated precisely, c = 1 would correspond to an equal weighting of old and new '
        'memories.'],
       "SI's path-fitted importance carries the loss's units, so its strength has a natural value 1 (then tuned below 1 in "
       'practice); SEC\'s calibrated Fisher carries the loss\'s curvature units, so the Laplace value 1/2 applies.'),
    _c('a11:23', 'S', 'bears', KUN,
       ['an unbiased estimate of the true Fisher can be obtained at the same computational cost as the empirical Fisher by '
        'replacing the expectation in Eq. (2) with a single sample',
        'the Fisher coincides with a generalized Gauss-Newton [Schraudolph, 2002] approximation of the Hessian for the '
        'problems presented here.'],
       'The known alternative fix for the EF\'s error: the (true) Fisher from labels sampled from the model, equal to the GGN '
       'for softmax cross-entropy. Mechanism check M1 runs exactly this in place of the calibration.'),
    # ---------------- K: the clip imp_used = min(imp_used, kappa / (lr w)), kappa = 0.5
    _c('a11:24', 'K', 'states', AR1,
       ['In the above equation if, for some k, the product η · λ · Fk is greater than 1, the weight correction toward θ∗ k '
        'is excessive and we overshoot the desired value.',
        'where clip sets the matrix values exceeding maxF to the constant maxF .',
        'Given maxF and η we can easily determine the maximum value for λ as 1/(η · maxF ).'],
       "AR1 clips the Fisher at maxF so that eta * lambda * F <= 1. SEC's update is lr * (g_p + w * 2 * imp_used * dth), so "
       "AR1's lambda * F is SEC's 2 w imp; the cap imp <= kappa / (lr w) with kappa = 0.5 gives lr * 2 w * imp <= 1: AR1's "
       'bound exactly (a11_grade.py prints the arithmetic from the frozen constants).'),
    # ---------------- T: the Fisher is taken, and the anchor set, at each task boundary (the label schedule)
    _c('a11:25', 'T', 'states', EWC,
       ['In order to apply EWC, we compute the Fisher information matrix at each task switch.'],
       "SEC's boundaries are the stream's task switches: tasks = consecutive groups of per_task class labels. The Fisher, "
       'the secant and the anchor are all taken there.'),
]
