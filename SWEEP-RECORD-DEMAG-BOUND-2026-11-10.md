# Sweep record: the Part L addendum (v0.17.0), 2026-11-10

What was searched: whether an explicit bound on the truncation error of the asymptotic
expansion of the Newell demagnetization tensor, valid for every rectangular cell, component and
separation larger than the cell diagonal, is already published; and what OOMMF itself does.
Searches used generic terms only (for example "demagnetization tensor asymptotic expansion
error bound", "far-field approximation demagnetizing field truncation error", "multipole
expansion error bound cuboid", "norm of derivatives of 1/r symmetric multilinear form"), about
20 queries across a web search engine and the arXiv, OpenAlex and Crossref interfaces, plus
direct reading of the sources below. The search was run by an agent that did not write the
bound, and repeated in part by a second.

## What was found

* **OOMMF source** (`app/oxs/ext/demagcoef.cc`, `demag.cc`, `demagcoef.h`), read on the public
  mirror `github.com/fangohr/oommf` at 1.2a5bis (commit 17ef69411f6c), 1.2a6 (commit
  2a310acc9bd7) and the tags for 1.2b0, 2.0a0, 2.0a1, 2.0a2, 2.0a3, 2.0b0 and 2.1a0. The asymptotic form carries the terms 1/R^3 to 1/R^9 (error of order
  1/R^11). From 2.0a2 the order is selectable (5, 7, 9, 11; default 11) and `FindKnotSchedule`
  sets the switching radii from error and speed models that a comment calls assumptions; the
  base asymptotic error model is V R^2 hmax^(n-3) / (5 (R^2 - hmax^2) R^n), with hmax the
  longest edge. No version read states a
  proven bound. The current release (2.1a3, 2026) ships as an archive only and was not read.
* **M. J. Donahue, "Accurate computation of the demagnetization tensor"**, talk at HMM-2007,
  Naples, 4 June 2007 (slides at math.nist.gov/~MDonahue): the series to all orders in operator
  form. His MMM 2019 poster with D. G. Porter (ET-01, Las Vegas, 7 November 2019) shows the same model,
  written as V R^2 / (5 hmax^3 (R^2 - hmax^2)) (hmax/R)^(n+2), with its order index two below the
  code's; his MMM 2020 talk
  counts the terms of the 1/R^9 and 1/R^11 coefficients (150 and 315).
* **Buchheit, Busse, Kessler and Rybakov**, J. Comput. Phys. 559 (2026) 114885
  (arXiv:2509.26274), Theorem 2.3 and Corollary 2.5: the same cuboid moment series for general
  power-law kernels, with a rigorous remainder bound by Cauchy estimates. The constant is not
  explicit, and the bound needs a separation larger than a multiple of the cell size.
* **Lebecki, Donahue and Gutowski**, J. Phys. D 41 (2008) 175005: dipole approximation only,
  with fitted error laws. **Chernyshenko and Fangohr** (arXiv:1403.1978): numerical error curves.
  **Liang and Yan** (arXiv:2407.16793): explicit 1/r^7 terms for cubes, order estimates.
  Classical multipole truncation bounds (Greengard and Rokhlin; Wala and Klöckner,
  arXiv:2008.00653; Baczewski and Shanker, arXiv:1107.3069) concern point sources; the
  cell-averaged second-derivative tensor is outside their scope.
* **The norm identity** used in the proof (the m-th derivative of 1/|x| has norm exactly
  m!/|x|^(m+1) as a symmetric multilinear form) was not found stated; it follows from Banach's
  theorem on symmetric forms in Hilbert space (Studia Math. 7 (1938) 36-44, Satz I, p. 38, read on
  the journal's scan during the release gate; in finite dimensions it also follows, by induction
  on the degree, from the gradient bound of Kellogg, Math. Z. 27 (1928) 55-64, Theorem IV) and the
  Legendre generating function.

## Verdict

The series is known (Donahue). A rigorous remainder estimate exists in a different form with a
non-explicit constant (Buchheit et al.). No bound of the explicit form of Theorem 8.1 was found.
The search does not rule out a bound of this form elsewhere.

## Not read

Seberino and Bertram 2001 (abstract only); the archives of OOMMF 2.1a1 to 2.1a3. (Banach 1938
was first listed here as not read; its statement had been taken from two later papers that cite
it. It was read on the journal's scan on 2026-11-10, during the release gate.)
