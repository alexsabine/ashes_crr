"""SOTA1 planning: CPU compute budget for an online split-image benchmark (synthetic tensors only; no data opened).

Times one SGD step of a reduced ResNet-18 (nf = 20, the continual-learning literature's small ResNet) on random
tensors, at the batch sizes the planned arms use, and converts it to minutes per single-pass run. Timings depend on
the machine, so this output is a planning estimate, not a result, and is not byte-identical on rerun (R9 does not
apply: nothing here is scored). Run: uv run --group realsys python studies/sota1/checks/compute_budget.py
"""
import os
import platform
import time

import torch
import torch.nn as nn
import torch.nn.functional as F

THREADS = 4
REPEATS = 20
WARMUP = 3
STREAM_BATCH = 10  # online continual learning: 10 new samples per step
# (label, images per step, image side, stream size per pass, classes)
CASES = [
    ("CIFAR-100 online, ER / ER-ACE / CRR arms (10 stream + 10 replay)", 20, 32, 50000, 100),
    ("CIFAR-100 online, DER++ (10 stream + 2 x 10 replay)", 30, 32, 50000, 100),
    ("TinyImageNet online, ER / CRR arms (10 stream + 10 replay)", 20, 64, 100000, 200),
]


class Block(nn.Module):
    def __init__(self, cin, cout, stride):
        super().__init__()
        self.c1 = nn.Conv2d(cin, cout, 3, stride, 1, bias=False)
        self.b1 = nn.BatchNorm2d(cout)
        self.c2 = nn.Conv2d(cout, cout, 3, 1, 1, bias=False)
        self.b2 = nn.BatchNorm2d(cout)
        self.short = nn.Sequential()
        if stride != 1 or cin != cout:
            self.short = nn.Sequential(nn.Conv2d(cin, cout, 1, stride, bias=False), nn.BatchNorm2d(cout))

    def forward(self, x):
        return F.relu(self.b2(self.c2(F.relu(self.b1(self.c1(x))))) + self.short(x))


class ReducedResNet18(nn.Module):
    def __init__(self, nf=20, classes=100):
        super().__init__()
        self.conv = nn.Conv2d(3, nf, 3, 1, 1, bias=False)
        self.bn = nn.BatchNorm2d(nf)
        plan = [(nf, 1), (nf, 1), (2 * nf, 2), (2 * nf, 1), (4 * nf, 2), (4 * nf, 1), (8 * nf, 2), (8 * nf, 1)]
        layers, cin = [], nf
        for cout, stride in plan:
            layers.append(Block(cin, cout, stride))
            cin = cout
        self.layers = nn.Sequential(*layers)
        self.fc = nn.Linear(8 * nf, classes)

    def forward(self, x):
        x = self.layers(F.relu(self.bn(self.conv(x))))
        return self.fc(F.adaptive_avg_pool2d(x, 1).flatten(1))


def main():
    torch.manual_seed(0)
    torch.set_num_threads(THREADS)
    print(f"machine: {platform.machine()}, os.cpu_count() = {os.cpu_count()}, torch {torch.__version__}, threads {THREADS}")
    for label, batch, side, stream, classes in CASES:
        model = ReducedResNet18(classes=classes)
        opt = torch.optim.SGD(model.parameters(), lr=0.1)
        x = torch.randn(batch, 3, side, side)
        y = torch.randint(0, classes, (batch,))
        for _ in range(WARMUP):
            opt.zero_grad()
            F.cross_entropy(model(x), y).backward()
            opt.step()
        t0 = time.perf_counter()
        for _ in range(REPEATS):
            opt.zero_grad()
            F.cross_entropy(model(x), y).backward()
            opt.step()
        sec = (time.perf_counter() - t0) / REPEATS
        steps = stream // STREAM_BATCH
        params = sum(p.numel() for p in model.parameters())
        print(f"{label}: params {params}, {sec:.4f} s/step, {steps} steps per pass, "
              f"{steps * sec / 60:.1f} min of training per run (evaluation not included)")


if __name__ == "__main__":
    main()
