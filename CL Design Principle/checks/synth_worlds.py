"""Synthetic Split-CIFAR-100-shaped surrogate streams for the SOTA1 gate (no benchmark data).

100 classes, each a low-frequency colour template (4x4 blocks upsampled to 32x32) plus a template shared by all classes,
Gaussian pixel noise and random circular shifts; uint8 images like CIFAR's. Declared in DECLARATION_2.md:
  W+ (headroom): seed 11, noise 1.6, signal 0.30, 200 train / 50 test per class (ER ends at 66.8, calibration run)
  W0 (near ceiling): seed 21, noise 1.6, signal 1.00, 200 train / 50 test per class
Usage: python synth_worlds.py <world> <out.npz>
"""
import sys

import numpy as np

WORLDS = {'W+': (11, 1.6, 0.30, 200, 50), 'W0': (21, 1.6, 1.00, 200, 50)}


def gen(path, seed, noise, sig, ntr, nte):
    rng = np.random.default_rng(seed)
    K = 100
    base = rng.normal(0, 1, (K, 4, 4, 3))
    common = rng.normal(0, 1, (4, 4, 3))
    tmpl = np.kron(sig * base + common[None], np.ones((1, 8, 8, 1)))

    def draw(n):
        xs, ys = [], []
        for k in range(K):
            x = tmpl[k][None] + noise * rng.normal(0, 1, (n, 32, 32, 3))
            sh = rng.integers(-4, 5, (n, 2))
            x = np.stack([np.roll(np.roll(x[i], sh[i, 0], 0), sh[i, 1], 1) for i in range(n)])
            xs.append(x)
            ys.append(np.full(n, k))
        x = np.concatenate(xs)
        y = np.concatenate(ys)
        return np.clip(128 + 40 * x, 0, 255).astype(np.uint8), y

    xtr, ytr = draw(ntr)
    xte, yte = draw(nte)
    np.savez(path, x_train=xtr, y_train=ytr, x_test=xte, y_test=yte)


if __name__ == '__main__':
    gen(sys.argv[2], *WORLDS[sys.argv[1]])
