# Data that has EVER been opened in CRR work (any version, any repo)

Records listed here are NOT held-out. A study may use them only as
"confirmatory (seen)" and must say so in its ledger row. Append to this
file in the same commit as any data download.

| dataset | version | records / scope | first opened |
|---|---|---|---|
| PhysioNet BIDMC PPG & Respiration | 1.0.0 | all 53 records | 2026-09-11 |
| PhysioNet Fantasia | 1.0.0 | all 40 records (ECG, RESP) | 2026-09-11 |
| PhysioNet Autonomic Aging | 1.0.0 | records 0001–0060 | 2026-09-12 (0001–0030); 2026-09-15 audit (0031–0060) |
| Marone lab stick-slip p4581 | as downloaded 2026-09-12 | whole run | 2026-09-12 |
| USGS Ridgecrest 2019 catalogue | ComCat export, M≥2.5 | whole export | 2026-09-12 |
| SPY daily prices | 2010–2026 | whole series | 2026-09-12 |
| Split-MNIST, Split-Fashion-MNIST, Split-KMNIST | standard | all | 2026-09-08 to 09-14 |
| Split-CIFAR-10 | standard | all | 2026-09-12 |
| PMLB `optdigits` (GitHub mirror, master) | sha256 in data/manifests/eqx.sha256 | all rows | 2026-09-15 (study EQX, after tag prereg-eqx-2026-09-15) |
| PMLB `pendigits` (GitHub mirror, master) | sha256 in data/manifests/eqx.sha256 | all rows | 2026-09-15 (study EQX) |
| PMLB `letter` (GitHub mirror, master) | sha256 in data/manifests/eqx.sha256 | all rows | 2026-09-15 (study EQX) |
| tsiR `twentymeas` (Grenfell; E&W measles, 20 cities, biweekly, 22 y) | tsiR 0.4.2, GitHub master; sha256 in data/manifests/meas.sha256 | all 20 cities | 2026-09-15 (study MEAS, after commit 3869ba2) |
| PMLB `mfeat_fourier` (GitHub mirror, master) | sha256 in data/manifests/eq2.sha256 | all rows | 2026-09-17 (study EQ2, after tag prereg-eq2-2026-09-17 at commit 4ba6035) |
| PMLB `mfeat_pixel` (GitHub mirror, master) | sha256 in data/manifests/eq2.sha256 | all rows | 2026-09-17 (study EQ2) |
| PMLB `texture` (GitHub mirror, master) | sha256 in data/manifests/eq2.sha256 | all rows (classes beyond the first ten dropped by the script) | 2026-09-17 (study EQ2) |
| PMLB `mfeat_karhunen` (GitHub mirror, master) | sha256 in data/manifests/eq2r.sha256 | all rows | 2026-09-21 (study EQ2R, after prereg commit 231cb26 (PR #40, 2026-09-17T20:59Z) and EQ2R-CC prereg commit 708e9b1 (PR #41); fetched after the R3 hold of AGENT_LOG 25) |
| PMLB `mfeat_zernike` (GitHub mirror, master) | sha256 in data/manifests/eq2r.sha256 | all rows | 2026-09-21 (study EQ2R) |
| PMLB `vowel` (GitHub mirror, master) | sha256 in data/manifests/eq2r.sha256 | all rows | 2026-09-21 (study EQ2R) |
| PMLB `mfeat_factors` (GitHub mirror, master) | sha256 in data/manifests/eq3.sha256 | all rows | 2026-09-22 (study EQ3, after prereg commit daf50e7 pushed 2026-09-22T01:22:03Z; fetched 2026-09-22T01:22:03Z) |
| PMLB `mfeat_morphological` (GitHub mirror, master) | sha256 in data/manifests/eq3.sha256 | all rows | 2026-09-22 (study EQ3, after prereg commit daf50e7 pushed 2026-09-22T01:22:03Z; fetched 2026-09-22T01:22:03Z) |
| PMLB `led7` (GitHub mirror, master) | sha256 in data/manifests/eq3.sha256 | all rows | 2026-09-22 (study EQ3, after prereg commit daf50e7 pushed 2026-09-22T01:22:03Z; fetched 2026-09-22T01:22:03Z) |
| PMLB `led24` (GitHub mirror, master) | sha256 in data/manifests/eq3.sha256 | all rows | 2026-09-22 (study EQ3, after prereg commit daf50e7 pushed 2026-09-22T01:22:03Z; fetched 2026-09-22T01:22:03Z) |
| PMLB `krkopt` (GitHub mirror, master) | sha256 in data/manifests/eq3.sha256 | all rows (first 10 classes in remapped label order used; stratified subsample to 5000 rows, seed 777) | 2026-09-22 (study EQ3, after prereg commit daf50e7 pushed 2026-09-22T01:22:03Z; fetched 2026-09-22T01:22:03Z) |
| PMLB `fars` (GitHub mirror, master) | sha256 in data/manifests/eq3.sha256 | all rows (8 classes; stratified subsample to 5000 rows, seed 777) | 2026-09-22 (study EQ3, after prereg commit daf50e7 pushed 2026-09-22T01:22:03Z; fetched 2026-09-22T01:22:03Z) |

Unseen and available: Autonomic Aging 0061–1121; other Marone-lab
experiments; Split-CIFAR-100; Split-TinyImageNet; any LM domain stream;
PMLB `satimage`, `usps` (not mirrored), other PMLB classification sets (no unseen 10-class set with >= 900 rows remains on the mirror except poker and kddcup).
