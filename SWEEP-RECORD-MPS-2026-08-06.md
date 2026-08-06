# Dated novelty and verification sweep — exact eigenstate note (Part F), 2026-08-06

Gate and adversarial review both ran on 2026-08-06, primary sources read directly with decisive
passages quoted in the review log (mps-paper/FIXLOG.md):
* Object re-verified in exact integer arithmetic by two independent scripts (reverify.py: 20/20
  checks; xcheck.py: H|psi> = 0 and ||psi||^2 = 4^L for L = 3..9); the sixteen-equation
  telescoping certificate re-derived by hand including the periodic wraparound bond.
* Method precedent credited: DEHP 1993 (DOI 10.1088/0305-4470/26/7/011); Gehrmann–Essler
  arXiv:2605.03020 Eq. (10); Garre Rubio–Molnár–Schuch–Verstraete arXiv:2603.28349 (necessity
  and sufficiency of the local equation). Object absence checked against Ivanov–Motrunich
  arXiv:2503.16327 (constrained-subspace models only) and Pancotti et al., PRX 10, 021051
  (exact only in the large-size limit).
* The note makes no claim about the remainder of the spectrum and does not use the term "scar"
  (host-chain level statistics were not verified).
Claim at defensible strength: the bond-dimension-2 matrix-product state with the stated integer
transfer matrices is an exact zero-energy eigenstate of the periodic chain
H = -sum_i (I+X_i)(X_{i+1}+Z_{i+1}) at every length L, established by an integer telescoping
certificate and independent exact-arithmetic verification.
