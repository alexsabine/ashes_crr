# RQM prior-art check for the candidate the CRR reading selects (2026-09-30; R10)

The candidate the CRR reading selects is: per-class distributions stored in input space, fitted at the task boundary and
never refit, replayed as pseudo-samples while a network keeps learning. See `Replay_Quality_Memory/CRR_READING.md`.

**How the sources were found.** An arXiv search on the day (arxiv.org/search) for "Gaussian mixture replay continual",
"pseudo-rehearsal gaussian class incremental" and "generative replay tabular continual learning" returned the three
sources below. Abstract pages were fetched with curl; their sha256 is given. The quotes are copied from the abstracts'
extracted text.

## Pfülb & Gepperth, "Continual Learning with Fully Probabilistic Models"

- **Identifier:** arXiv:2104.09240, current version **v1** (Mon, 19 Apr 2021), fetched 2026-09-30.
- **Integrity:** abstract page sha256 3d5796e24eb07e8d563a53c0feedc771b91ea43578ab4e266a53aba9dfaa4211.

> As a concrete realization of generative continual learning, we propose Gaussian Mixture Replay (GMR). GMR is a pseudo-rehearsal approach using a Gaussian Mixture Model (GMM) instance for both generator and classifier functionalities.

> Lastly, we verify that GMR, despite its simple structure, achieves state-of-the-art performance on common class-incremental learning problems at very competitive time and memory complexity.

**Reading.**
- **The candidate's core is published.** Pseudo-rehearsal from Gaussian mixture models fitted in input space (the
  benchmarks are MNIST, FashionMNIST and Devanagari) for class-incremental learning.
- **The difference from GMR.** In GMR the GMM is also the classifier; the candidate uses the Gaussians only as the
  generator, for a separate network that keeps learning. That is the deep generative replay design (DGR, Shin et al.
  2017; `rqm_q2_2026-09-30.md`) with a Gaussian generator. It is not new.

## "Study of Class-Incremental Radio Frequency Fingerprint Recognition Without Storing Exemplars"

- **Identifier:** arXiv:2601.03063, current version **v1** (Tue, 6 Jan 2026), fetched 2026-09-30.
- **Integrity:** abstract page sha256 5bbf4bb2ae2db153b8ead48788a2bfdd5a96499969d02da882d011ce3cd4a812.

> For each class we fit a diagonal Gaussian Mixture Model (GMM) to the backbone features and sample pseudo-features from these fitted distributions to rehearse past classes without storing raw signals.

**Reading.**
- **Feature-space, not input-space.** The per-class GMMs are fitted to the features of a frozen pretrained backbone.
- **Bears on:** the storage form and on privacy as motivation ("without storing raw signals").

## "Distribution-Level Memory Recall for Continual Learning: Preserving Knowledge and Avoiding Confusion"

- **Identifier:** arXiv:2408.02695, current version **v1** (Sun, 4 Aug 2024), fetched 2026-09-30.
- **Integrity:** abstract page sha256 1440d442b584d7fcf65c8816d0c737a37673c8482c7726587edd0d90c1d509d1.

> we propose the Distribution-Level Memory Recall (DMR) method, which uses a Gaussian mixture model to precisely fit the feature distribution of old knowledge at the distribution level and generate pseudo features in the next stage.

**Reading.** Feature-space GMM replay. It supports the Q1 point that single Gaussians are too crude in feature space.

## Conclusion for the candidate

The candidate is the GMR / DGR family with a Gaussian generator in input space. No part of it is new. A pre-registered
test of it would be a test of a known method on new carriers, in the repository's learner, at matched memory. The ledger
would record it as such, "not a CRR rule; GMR/DGR family".
