# SOTA1 addition (not upstream Mammoth): the CRR safe continual learner (CRR-SCL), prompt-log entry 191.
# Built from Mammoth's own DER++ (models/derpp.py) and ER-ACE (models/er_ace.py) code at commit e75a491, plus the
# X-DER memory update (Boschini et al., arXiv 2201.00766 v2) and momentum distillation (MKD, Michel et al., arXiv
# 2309.02870 v2), chosen by the retrodictive grading in `CL Design Principle/checks/retro_sota.txt` and set out in
# `CL Design Principle/DESIGN.md`. Every component is switchable so each can be ablated:
#   --crr_ace   A3: the incoming batch competes only among present (and not-yet-seen) classes (ER-ACE's mask)
#   --crr_cos   H-EQ at the head: cosine classifier, every class weight at equal norm (ER-ACE's CustomLinear)
#   --alpha     A6: distil the stored logits of the settled past (DER)
#   --beta      A6/A7: replay the stored labels, the settled outcome (DER++)
#   --crr_a8    A8: distil only logits that were past at storage; at each cut, fill the new past classes' logits
#               (X-DER's memory update, gamma-attenuated)
#   --crr_ema   A6 + P3: a slow model, the geometric-age-weighted mean of the parameter history
#   --crr_clock D2/A1': the slow model's decay runs on the model's own clock (update length / its running mean)
#   --crr_kd    A6 at bounded strength: the present is pulled toward the slow model's prediction (MKD's KD term);
#               'eq' weights the pull by H-EQ (Omega = 1, equal gradient pull with the present), 'fixed' uses MKD's
#               published lambda, 'off' removes it
#   --crr_pred  prediction by nearest class mean on the slow model's features ('ncm', A6 Frechet mean), by the slow
#               model's head ('slow') or by the fast model's head ('fast')
# The empty cut (Proposition 7) is not a loss term: `crr_state()` / `crr_load_state()` expose every piece of state the
# learner adds, and the SOTA1 pause harness checks that a pause and resume leaves the run bitwise unchanged.
import copy

import torch
import torch.nn.functional as F

from models.er_ace import CustomLinear
from models.utils.continual_model import ContinualModel
from utils import binary_to_boolean_type
from utils.args import add_rehearsal_args, ArgumentParser
from utils.buffer import Buffer


class CrrScl(ContinualModel):
    """CRR safe continual learner."""
    NAME = 'crr_scl'
    COMPATIBILITY = ['class-il', 'task-il']

    @staticmethod
    def get_parser(parser) -> ArgumentParser:
        add_rehearsal_args(parser)
        parser.add_argument('--alpha', type=float, default=0.3, help='DER logit-distillation weight (A6).')
        parser.add_argument('--beta', type=float, default=0.5, help='Buffer label-replay weight (A6/A7).')
        parser.add_argument('--crr_ace', type=binary_to_boolean_type, default=True, help='Asymmetric incoming loss (A3).')
        parser.add_argument('--crr_cos', type=binary_to_boolean_type, default=True, help='Cosine head (H-EQ at the head).')
        parser.add_argument('--crr_a8', type=binary_to_boolean_type, default=True, help='A8 mask and X-DER memory update.')
        parser.add_argument('--crr_gamma', type=float, default=0.75, help='X-DER attenuation of filled logits.')
        parser.add_argument('--crr_ema', type=binary_to_boolean_type, default=True, help='Slow model (A6 + P3).')
        parser.add_argument('--crr_ema_q', type=float, default=0.99, help='Slow-model decay per own-clock unit.')
        parser.add_argument('--crr_clock', type=str, default='model', choices=['model', 'step'], help='Slow-model clock.')
        parser.add_argument('--crr_clock_lambda', type=float, default=0.05, help='EMA rate of the running mean update length.')
        parser.add_argument('--crr_kd', type=str, default='eq', choices=['eq', 'fixed', 'off'], help='Pull toward the slow model.')
        parser.add_argument('--crr_kd_lambda', type=float, default=5.5, help="MKD's published lambda (fixed mode).")
        parser.add_argument('--crr_kd_tau', type=float, default=4.0, help='KD temperature (MKD).')
        parser.add_argument('--crr_eq_omega', type=float, default=1.0, help='Omega for the H-EQ weight.')
        parser.add_argument('--crr_eq_smooth', type=float, default=0.9, help='EMA smoothing of the gradient norms (H-EQ).')
        parser.add_argument('--crr_eq_cap', type=float, default=10.0, help='Cap on the H-EQ weight.')
        parser.add_argument('--crr_pred', type=str, default='ncm', choices=['ncm', 'slow', 'fast'], help='Prediction rule.')
        return parser

    def __init__(self, backbone, loss, args, transform, dataset=None):
        if args.crr_cos:
            assert hasattr(backbone, 'classifier'), 'The backbone must have a classifier layer.'
            backbone.classifier = CustomLinear(backbone.classifier.in_features, backbone.classifier.out_features)
        super().__init__(backbone, loss, args, transform, dataset=dataset)
        assert args.crr_ema or (args.crr_kd == 'off' and args.crr_pred == 'fast'), 'KD and slow prediction need the slow model'
        self.buffer = Buffer(self.args.buffer_size)
        self.seen_so_far = torch.tensor([]).long().to(self.device)
        self.ema_net = copy.deepcopy(self.net).to(self.device) if args.crr_ema else None
        if self.ema_net is not None:
            for p in self.ema_net.parameters():
                p.requires_grad_(False)
        self.ema_updates = 0
        self.clock_mu = None       # running mean update length (the own unit)
        self.clock_tau = 0.0       # model time elapsed, in own units
        self.eq_norm_p = None      # smoothed present-gradient norm (H-EQ)
        self.eq_norm_k = None      # smoothed regeneration-gradient norm (H-EQ)
        self.eq_last_w = float('nan')

    # ---- the empty cut: every piece of state this learner adds beyond net, optimiser, buffer and RNGs ----
    def crr_state(self):
        return {'seen_so_far': self.seen_so_far.clone(), 'ema_updates': self.ema_updates, 'clock_mu': self.clock_mu,
                'clock_tau': self.clock_tau, 'eq_norm_p': self.eq_norm_p, 'eq_norm_k': self.eq_norm_k,
                'eq_last_w': self.eq_last_w,
                'ema_net': None if self.ema_net is None else copy.deepcopy(self.ema_net.state_dict())}

    def crr_load_state(self, st):
        self.seen_so_far = st['seen_so_far'].clone()
        self.ema_updates, self.clock_mu, self.clock_tau = st['ema_updates'], st['clock_mu'], st['clock_tau']
        self.eq_norm_p, self.eq_norm_k, self.eq_last_w = st['eq_norm_p'], st['eq_norm_k'], st['eq_last_w']
        if self.ema_net is not None:
            self.ema_net.load_state_dict(st['ema_net'])

    # ---- prediction ----
    def forward(self, x):
        if self.net.training or self.args.crr_pred == 'fast':
            return self.net(x)
        net = self.ema_net
        net.eval()
        if self.args.crr_pred == 'slow' or self.buffer.is_empty():
            return net(x)
        feats = F.normalize(net(x, returnt='features'), dim=1)
        key = (self.task_iteration, self.current_task, self.buffer.num_seen_examples, self.ema_updates)
        if getattr(self, '_proto_key', None) != key:
            self._proto_cache, self._proto_key = self._prototypes(net), key
        classes, protos = self._proto_cache
        out = torch.full((x.shape[0], self.num_classes), -1e9, device=x.device)
        out[:, classes] = feats @ protos.T
        return out

    @torch.no_grad()
    def _prototypes(self, net):
        n = min(self.buffer.num_seen_examples, self.buffer.examples.shape[0])
        ex, lab = self.buffer.examples[:n], self.buffer.labels[:n]
        norm = self.dataset.get_normalization_transform()
        feats = torch.cat([F.normalize(net(norm(ex[i:i + 256]).to(self.device), returnt='features'), dim=1)
                           for i in range(0, n, 256)])
        classes = lab.unique()
        protos = torch.stack([F.normalize(feats[lab == c].mean(0), dim=0) for c in classes])
        return classes.to(self.device), protos

    # ---- learning ----
    def _masked(self, logits, labels):
        present = labels.unique()
        self.seen_so_far = torch.cat([self.seen_so_far, present]).unique()
        if not self.args.crr_ace or self.current_task == 0:
            return logits
        mask = torch.zeros_like(logits)
        mask[:, present] = 1
        mask[:, self.seen_so_far.max():] = 1
        return logits.masked_fill(mask == 0, -1e9)

    def _present_loss(self, inputs, labels):
        raw = self.net(inputs)
        loss = self.loss(self._masked(raw, labels), labels)
        kd_inputs, kd_outputs = [inputs], [raw]
        if not self.buffer.is_empty():
            if self.args.alpha > 0:
                b_in, _, b_logits, b_tl = self.buffer.get_data(self.args.minibatch_size, transform=self.transform, device=self.device)
                b_out = self.net(b_in)
                if self.args.crr_a8:
                    n_known = (b_tl + 1) * self.cpt  # logits that were past or present at storage (or filled since)
                    cols = torch.arange(b_out.shape[1], device=self.device)[None, :]
                    m = (cols < n_known[:, None]).float()
                    loss = loss + self.args.alpha * (((b_out - b_logits) ** 2) * m).sum() / m.sum()
                else:
                    loss = loss + self.args.alpha * F.mse_loss(b_out, b_logits)
            if self.args.beta > 0:
                b_in, b_lab, _, _ = self.buffer.get_data(self.args.minibatch_size, transform=self.transform, device=self.device)
                b_out = self.net(b_in)
                loss = loss + self.args.beta * self.loss(b_out, b_lab)
                kd_inputs.append(b_in)
                kd_outputs.append(b_out)
        return loss, raw, torch.cat(kd_inputs), torch.cat(kd_outputs)

    def _kd_loss(self, x, out):
        # the student's logits are the ones already computed for the present loss (same inputs, same forward pass)
        t = self.args.crr_kd_tau
        with torch.no_grad():
            self.ema_net.eval()
            teacher = F.softmax(self.ema_net(x)[:, :self.n_seen_classes] / t, dim=1)
        student = F.log_softmax(out[:, :self.n_seen_classes] / t, dim=1)
        return F.kl_div(student, teacher, reduction='batchmean') * t * t

    def observe(self, inputs, labels, not_aug_inputs, epoch=None):
        self.opt.zero_grad()
        loss_p, raw, kd_x, kd_out = self._present_loss(inputs, labels)
        use_kd = self.args.crr_kd != 'off' and self.ema_updates > 0 and self.current_task > 0
        if not use_kd:
            loss = loss_p
            loss.backward()
        elif self.args.crr_kd == 'fixed':
            loss = loss_p + 0.5 * self.args.crr_kd_lambda * self._kd_loss(kd_x, kd_out)
            loss.backward()
        else:
            loss_k = self._kd_loss(kd_x, kd_out)
            params = [p for p in self.net.parameters() if p.requires_grad]
            gp = torch.autograd.grad(loss_p, params, retain_graph=True, allow_unused=True)
            gk = torch.autograd.grad(loss_k, params, allow_unused=True)
            npn = torch.sqrt(sum((g ** 2).sum() for g in gp if g is not None)).item()
            nk = torch.sqrt(sum((g ** 2).sum() for g in gk if g is not None)).item()
            s = self.args.crr_eq_smooth
            self.eq_norm_p = npn if self.eq_norm_p is None else s * self.eq_norm_p + (1 - s) * npn
            self.eq_norm_k = nk if self.eq_norm_k is None else s * self.eq_norm_k + (1 - s) * nk
            w = min(self.args.crr_eq_cap, self.args.crr_eq_omega * self.eq_norm_p / self.eq_norm_k) if self.eq_norm_k > 1e-12 else 0.0
            self.eq_last_w = w
            for p, a, b in zip(params, gp, gk):
                if a is None and b is None:
                    continue
                g = torch.zeros_like(p) if a is None else a.clone()
                if b is not None:
                    g.add_(b, alpha=w)
                p.grad = g
            loss = loss_p + w * loss_k.detach()
        prev = None
        if self.ema_net is not None and self.args.crr_clock == 'model':
            prev = [p.detach().clone() for p in self.net.parameters()]
        self.opt.step()
        if self.ema_net is not None:
            self._update_ema(prev)
        tl = torch.full_like(labels, self.current_task)
        self.buffer.add_data(examples=not_aug_inputs, labels=labels, logits=raw.data, task_labels=tl)
        return loss.item()

    @torch.no_grad()
    def _update_ema(self, prev):
        if self.args.crr_clock == 'model':
            d = torch.sqrt(sum(((p - p0) ** 2).sum() for p, p0 in zip(self.net.parameters(), prev))).item()
            lam = self.args.crr_clock_lambda
            self.clock_mu = d if self.clock_mu is None else (1 - lam) * self.clock_mu + lam * d
            u = d / self.clock_mu if self.clock_mu > 0 else 0.0
        else:
            u = 1.0
        self.clock_tau += u
        # A6: regeneration averages settled occasions only; the untrained initialisation is not one, so the slow model
        # starts at the first update.
        decay = 0.0 if self.ema_updates == 0 else self.args.crr_ema_q ** u
        self.ema_updates += 1
        for pe, p in zip(self.ema_net.parameters(), self.net.parameters()):
            pe.mul_(decay).add_(p.detach(), alpha=1 - decay)
        for be, b in zip(self.ema_net.buffers(), self.net.buffers()):
            if be.dtype.is_floating_point:
                be.mul_(decay).add_(b, alpha=1 - decay)
            else:
                be.copy_(b)

    # ---- the cut at a task boundary: X-DER's memory update (A8) ----
    @torch.no_grad()
    def end_task(self, dataset):
        if not self.args.crr_a8 or self.buffer.is_empty():
            return
        t_end = self.current_task
        n = min(self.buffer.num_seen_examples, self.buffer.examples.shape[0])
        norm = self.dataset.get_normalization_transform()
        was = self.net.training
        self.net.eval()
        hi = (t_end + 1) * self.cpt
        for i in range(0, n, 256):
            idx = torch.arange(i, min(i + 256, n))
            tl = self.buffer.task_labels[idx]
            old = tl < t_end
            if not old.any():
                continue
            idx, tl = idx[old], tl[old]
            cur = self.net(norm(self.buffer.examples[idx]).to(self.device))
            stored = self.buffer.logits[idx].clone()
            lab = self.buffer.labels[idx]
            gt = stored[torch.arange(len(idx)), lab]
            for j in range(len(idx)):
                lo = int((tl[j] + 1) * self.cpt)
                new = cur[j, lo:hi]
                fpmax = new.max()
                factor = 1.0
                if fpmax > 0 and gt[j] > 0:
                    factor = min(float(self.args.crr_gamma * gt[j] / fpmax), 1.0)
                elif fpmax > 0 >= gt[j]:
                    factor = 0.0
                stored[j, lo:hi] = new * factor
            self.buffer.logits[idx] = stored
            self.buffer.task_labels[idx] = t_end
        self.net.train(was)
