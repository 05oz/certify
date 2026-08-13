# FIXLOG — wedge v2 (Part K): the exact logical error probability

Build and verification log, 2026-08-12. Decisions and fixes recorded in the
order they were made.

## Verification battery (all PASS before staging)

1. **Identity re-derivation.** Both identities (Theorems 2.1, 2.2) re-derived
   from scratch (group-algebra character argument) rather than trusted from
   the scoping record, then verified in exact `Fraction` arithmetic against
   brute force over all 2^m subsets on six random small DEMs (n=5,6; m=9,10,12),
   including two with non-spanning masks (exercising the general reachable-set
   term that the shipped DEMs do not need). 6/6 exact matches for the full
   A_w spectrum AND the exact P_L. Ships as `identity_selftest.py`.
2. **Counts, d=3** (in-shell, instant): A_2=55, A_3=690, A_4=4078 match the
   Part H certificates; A_5=16467 matches the scoping dig's brute-force value;
   sum_w A_w = 2^22; A_23 = 1.
3. **Counts, d=5** (jobrunner, 84 s, <2500 MB): A_3, A_4, A_5 match the Part H
   certificates; A_6 = 67,711,204 matches the Part H WMAX=6 certificate;
   **A_7 = 832,441,445 matches the scoping dig**; sum_w A_w = 2^76 exactly;
   A_77 = 1; spectra at p=1/1000 and p=1/100 identical (p-independence).
4. **Exact P_L, d=3:** three fully independent exact routes agree
   digit-for-digit at both operating points: (a) class-binned character sum,
   (b) CRT reconstruction of the syndrome-space signed convolution over
   25-bit primes, (c) Gray-code full enumeration of all 2^23 configurations
   with incremental exact integer numerators. (b) and (c) share no code or
   method with (a) beyond the BFS decoder and the mechanism list.
5. **Exact P_L, d=5:** (a) checked against (b) modulo 24 distinct 25-bit
   primes (~600 bits of agreement), both operating points, jobrunner, ~110 s
   each. Full CRT reconstruction at d=5 was not run (≈195 primes ≈ 30+ min);
   the 24-prime residue check has false-match probability ~2^-600.
6. **Containment (the kill test for this release):** exact P_L lies strictly
   inside the Part H bracket at all four operating points (positions 0.515,
   0.515, 0.358, 0.370 of the width), inside the tighter WMAX=6 bracket at
   d=5, p=1/1000 (position 0.42), and inside both 10^7-shot MC 95% CIs at
   d=5. A failure at any point would have stopped the build (it would
   falsify Part H); none occurred.
7. **Checker (public artifact):** re-derives everything from the mechanism
   list; measured 0.15 s (d=3) and 129 s / 0.79-0.84 GB peak RSS (d=5) with
   `/usr/bin/time -l` under the jobrunner cap. CHECK PASS on all four
   certificates. Independent of the engine (array-module FWHTs, fused
   syndrome pass, two-level scaled product tables vs. numpy transforms and
   numpy binning in the engine).
8. **Tamper battery:** 8/8 corruption classes rejected, each by the gate it
   targets (count, hash, hashless probability, P_L digit, obs bit, distance,
   N_w, bracket containment). Baseline pristine pass re-confirmed.

## Decisions

- **Route (a) of the scoping record (CPOG weighted model counter) not
  pursued**, for the reason recorded there: it enlarges the trusted base
  (C checker + CNF encoding fidelity + from-source GMP toolchain) and breaks
  the CPython-only trust root. Route (b) is proven and shipped.
- **Full-BFS decoder in the checker** (not depth-truncated): the transform
  needs D on all syndromes; this also RETIRES Part H's depth-truncation
  soundness argument from the trusted base.
- **Certificate carries string-encoded integers** for all big counts and the
  P_L numerator/denominator (JSON number precision hazards).
- **The v1 bracket is embedded in the v2 certificate** (with DOI) so the
  checker can re-verify containment; it is data cited from Part H, not a
  re-derivation of Part H.
- **N_w spectrum added** (undetectable logical operators): re-derives the
  circuit-level distance via transform, replacing Part H's enumeration
  derivation, and adds the closed-form gate sum_w N_w = 2^{m-n-1}.
- **d=5 tamper battery not run** (would take ~20 min at 129 s/run × 9 runs);
  the battery is certificate-generic and demonstrated at d=3. The note says
  exactly this.
- **Framing:** supersession of our own Part H bracket, never of any external
  result; the character sum acknowledged as MacWilliams-type classical
  lineage (Jurrius–Pellikaan cited); "first"/"no prior" phrasing scoped to
  the intersection in SWEEP-RECORD-WEDGE2-2026-08-12.md and qualified as
  "no prior work found".
- **Honest limit stated in §6:** the C(m,w) wall is traded for a 2^n wall;
  d=7 one-round (n≈48) is out of reach on a laptop by this method. No claim
  that the method scales past d=5.

## Machine-safety record

All 2^24-scale compute (engine runs, CRT checks, checker timing runs) went
through `jobrunner.py --mem-mb 2500 --workers 1` on a dedicated queue
(`wedge2/queue_w2.jsonl`); in-shell work was limited to d=3/small-case smoke
tests (<10 s each). Peak checker RSS 836 MB, well under the cap. No job died
at the cap; no cap was raised.

## Post-release correction pass, 2026-08-12

Four claim-level corrections landed after release; recorded here because the Engine 2 referee
found only this file's title line changed while the paper had changed substantively.

**K-1. Part letter.** This file and `note.tex`'s header comment labelled the release "Part L".
wedge2 is **Part K**, v0.11.0, doi:10.5281/zenodo.21898343; Part L is the demagnetization-tensor
release, v0.12.0. Propagation grep (`Part L` in wedge2-*): 2 hits, both corrected.

**K-2. Strict containment.** The note asserted `L < P_L < U` "verified in exact rational
arithmetic by the checker". `check_wedge2.py:300` gates the non-strict `L <= P_L <= U`.
Strictness is true — re-verified in exact `Fraction` arithmetic — but is not what the shipped
checker establishes. Corrected to state what the checker does.

**K-3. Bracket positions.** The abstract gave the two d = 5 exact values as sitting at 0.36 and
0.51 of their bracket widths. Re-derived positions: 0.5151 and 0.5146 at d = 3, 0.3581 and
0.3698 at d = 5. The sentence is scoped to d = 5, so the correct pair is 0.36 and 0.37.

**K-4. Supersession pointer.** Part H's README section presented its bracket as current with no
pointer to this part. Noted for the README owner; not a wedge2-paper edit.
