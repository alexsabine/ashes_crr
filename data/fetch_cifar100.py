"""Download CIFAR-100 (python version) for SOTA1 and write a sha256 manifest and the local .npz the harness reads.
Run ONLY after the SOTA1 prereg hash is pushed (CLAUDE.md R2) and not before 2026-09-26 00:00 UTC (R3).

    python data/fetch_cifar100.py

- Source: https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz (Krizhevsky 2009), the URL torchvision uses.
- Integrity: the archive's md5 is checked against torchvision 0.29.0's constant (eb9058c3a382ffc7106e4002c42a8d85), and
  the members `train` and `test` against torchvision's member md5s.
- Output: data/raw/cifar100/cifar-100-python.tar.gz; data/raw/cifar100/cifar100.npz with x_train (50000,32,32,3) uint8,
  y_train (fine labels), x_test (10000,32,32,3), y_test, in the archive's record order; data/manifests/sota1.sha256.
Transport is curl, as in the other fetchers (the proxy CA bundle is accepted by curl).
"""
import datetime as dt
import hashlib
import pickle
import subprocess
import tarfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "cifar100"
URL = "https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz"
TGZ_MD5 = "eb9058c3a382ffc7106e4002c42a8d85"
MEMBER_MD5 = {"cifar-100-python/train": "16019d7e3df5f24257cddd939b257f8d",
              "cifar-100-python/test": "f0ef6b0ae62326f3e7ffdfab6717acfc"}
MAN = ROOT / "data" / "manifests" / "sota1.sha256"


def digest(b, algo):
    h = hashlib.new(algo)
    h.update(b)
    return h.hexdigest()


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    tgz = RAW / "cifar-100-python.tar.gz"
    when = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if not tgz.exists():
        subprocess.run(["curl", "-sSfL", "--retry", "3", "--max-time", "1800", "-o", str(tgz), URL], check=True)
    blob = tgz.read_bytes()
    assert digest(blob, "md5") == TGZ_MD5, "archive md5 does not match torchvision's constant"
    out = {}
    with tarfile.open(tgz) as tf:
        for name, md5 in MEMBER_MD5.items():
            raw = tf.extractfile(name).read()
            assert digest(raw, "md5") == md5, f"{name} md5 does not match torchvision's constant"
            d = pickle.loads(raw, encoding="latin1")
            x = np.asarray(d["data"], dtype=np.uint8).reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)
            y = np.asarray(d["fine_labels"], dtype=np.int64)
            split = name.split("/")[-1]
            out[f"x_{split}"], out[f"y_{split}"] = x, y
    npz = RAW / "cifar100.npz"
    np.savez(npz, **out)
    lines = [f"{digest(blob, 'sha256')}  data/raw/cifar100/cifar-100-python.tar.gz  url={URL} md5={TGZ_MD5} fetched={when}",
             f"{digest(npz.read_bytes(), 'sha256')}  data/raw/cifar100/cifar100.npz  derived by data/fetch_cifar100.py"]
    for k in ("x_train", "y_train", "x_test", "y_test"):
        lines.append(f"# {k} shape {out[k].shape} dtype {out[k].dtype}")
    MAN.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
