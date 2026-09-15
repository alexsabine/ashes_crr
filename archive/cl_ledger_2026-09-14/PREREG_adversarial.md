# Pre-registration — adversarial tests of equanimity replay. 2026-09-14, before any run.
All on Split-KMNIST class-IL unless stated, repo pipeline, r = 0.2, seeds 0–2, standard stream.
A1 (fixed weight): replay weight fixed at w ∈ {1, 2, 4, 8} (no adaptation). Equanimity Ω=1 is vindicated as *adaptive*
   only if it beats the best fixed w by ≥ 1.0 pt. FAIL (adaptivity irrelevant) if some fixed w is within 1.0.
A2 (prior art): MEGA-I-style loss-ratio balancing, w = L_past/L_present, (a) per step as published, (b) with the same
   0.98 smoothing as equanimity. Equanimity is a distinct result only if it beats both by ≥ 1.0. FAIL if within 1.0.
A3 (unit-freeness): Ω sweep {0.5, 0.71, 1, 1.41, 2} at lr ∈ {0.0125, 0.2} (×¼, ×4) and batch ∈ {5, 20} (stream length
   fixed). PASS if the optimum stays at Ω=1 in all four; FAIL if it moves by ≥ √2 in any.
A4 (occasion timescale): task length ∈ {1000, 2000, 4000} samples (100/200/400 updates), smoothing window
   β ∈ {0.9, 0.95, 0.98, 0.99, 0.995} at Ω=1. Reported: does the best β track task length? Not scored.
