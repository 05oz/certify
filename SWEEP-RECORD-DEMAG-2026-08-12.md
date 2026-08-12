# Dated novelty and verification sweep — certified Newell demagnetization-tensor reference table (Part L)

Searches run 2026-08-11 and 2026-08-12 (arXiv + web). This record is the
priority-and-replay provenance for the demag note and the released Part L
artifacts (`demag-paper/`, `demag-certificates/`, `demag-scripts/`), v0.12.0.

## Primary sources, read at the relevant sections and quoted verbatim

* **Newell, Williams, Dunlop**, "A generalization of the demagnetizing tensor
  for nonuniform magnetization," J. Geophys. Res. Solid Earth 98(B6) 9551-9555
  (1993). The analytic tensor. Formula (16): `Hx = -Nxx Mx`. CONFIRMED as the
  formula base of OOMMF.
* **OOMMF `app/oxs/ext/demagcoef.cc`** (Donahue/Porter, NIST; revision by
  Donahue 2018-01-25), pulled from the `fangohr/oommf` mirror at commit on
  `master`. The functions `Oxs_Newell_f`, `Oxs_Newell_g`, `Oxs_SelfDemagNx`,
  `Oxs_CalculateNxx/Nxy` are implemented here line for line. The header carries
  16 Maple-computed 50-digit check values for Nxx and Nxy; all 16 lie inside our
  certified enclosures and agree with their midpoints to >= 49.6 digits (our
  independent numerical anchor).
* **Chernyshenko & Fangohr**, JMMM 381 (2015) 440-445; arXiv:1403.1978. The
  pathology, quoted verbatim in the note (S II.B): relative error "is of the
  order 10^-15 r^6," so "for cell separations greater than 10^(15/6) ~ 300 the
  analytical computation will contain no significant digits at all." OOMMF
  "counteracts this ... utilizing an asymptotic expansion ... in terms of powers
  of 1/r up to 6th order." Their reference value is MPFR floating point
  (S II.B, III.G), NOT a certified enclosure; their output is accuracy plots,
  not a table.
* **Bjork & d'Aquino**, "Accuracy of the analytical demagnetization tensor for
  various geometries," JMMM 587 (2023) 171235 (S0304885323008958); open poster
  version read in full. Error of the analytic tensor vs the dipolar field over
  prism/tetrahedron/cylinder tiles, single and double precision, out to 10^4
  tile radii (Fig. 1). Reference is "exact (to machine precision)" floating
  point; deliverable is plots, no certified table, no interval enclosures, no
  checker. Cites CF2015 [6] for the far-field inaccuracy.
* **OOMMF asymptotic expansion**: the `DemagNxxAsymptotic` powers-of-1/r
  expansion (through 1/r^6), taken from Fangohr's `ovf2mfm/demagderiv.pdf`
  reverse-engineering of the OOMMF code (`nXXfunNoncubic`). Reproduced (with mu0
  dropped) for the crossover analysis; validated against our enclosure at large
  r (leading term matches to sign and magnitude: on-axis cube n=100 gives
  -1/(2 pi 10^6) = -1.5915e-7).

## Novelty verdict

Searches (2026-08-11/12): "certified/interval demagnetization tensor," "rigorous
enclosure demag tensor micromagnetics," "arbitrary precision demag tensor
verified 2024/2025/2026." No certified or interval-arithmetic demagnetization-
tensor table exists. The literature is:
  - the analytic formula (Newell 1993; Maicas 1998; Schabes-Aharoni 1987, both
    flagged by OOMMF as having errors),
  - the accuracy studies (CF2015; Bjork-d'Aquino 2023; Donahue MMM2020 talk) --
    all floating-point, all uncertified, all producing plots or internal
    reference values,
  - the numerical-integration alternative (CF2015) and the newer codes
    (mumax+, MagneX, magnum.np, MagTense) which inherit the same kernels.

The intersection the note occupies -- a rigorous TWO-SIDED enclosure of the
Newell entries across the simulation regime, a rigorous measurement of the
double-precision and asymptotic failures against those enclosures, and
independent stdlib re-verification -- is unoccupied. **Verdict:
PRIORITY-CLEAN / NOVEL as a certified object.** The Newell FORMULAS and the
pathology are not ours and are cited to their sources; what is new is the
certification and the certified pathology map.

## Verification summary

* All 4 quick-grid + full-grid demag certificates: `CHECK PASS` under the shipped
  stdlib checker (`check_demag.py`), Python 3, standard library only.
* Independent numerical anchor: 16 OOMMF/Maple 50-digit values all inside the
  enclosures (>= 49.6-digit agreement); an independent 220-digit mpmath
  evaluation of the same Newell formulas inside every enclosure of the table
  (0 containment failures); trace `Nxx+Nyy+Nzz` encloses 0 at mutual points.
* Tamper battery (6 controls): enclosure narrowed to exclude truth, enclosure
  shifted off truth, enclosure grossly widened, corrupted naive double, altered
  digit-loss claim, falsified hash -- each rejected nonzero, at the hash layer
  and (hash recomputed to match) at the mathematical re-derivation layer.
* KILL CONDITION (pre-registered): "if certified enclosures cannot be made
  tighter than double precision anywhere in the regime of interest, DEAD." Not
  triggered. Enclosures are tighter than double precision EVERYWHERE in the
  regime; at the worst point (cube on-axis Nxx, n=10^4) the relative enclosure
  width is ~2e-54 where the double-precision analytic formula has zero (indeed
  negative) correct digits. **Verdict: LIVE.**

## IP boundary

Public unit = certificate JSON + stdlib checker (`check_demag.py`) only.
The generator (`gen_demag.py`), the shared interval library used to build the
certificate (`civ.py`, `newell.py`), and the grid-selection search remain
PRIVATE (method repo). Note: F2 is infrastructure, so the shipped checker is by
design close to a full independent reimplementation -- there is little hidden
engine here, and that is the point (maximal reproducibility for a substrate
object). The checker shares NO code with the generator.
