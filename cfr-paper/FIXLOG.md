# FIXLOG — adversarial pre-release review of note-cfr525

Reviewer pass: 2026-08-06. Ground truth treated as authoritative: the object
`CFR_5_25.json`, the shipped verifier `verify_cfr525.py`, the second verifier
`/Users/kirt/Documents/reserch math/construct/florentine/verify_cfr.py`, and the
primary source (Handbook of Combinatorial Designs, 2nd ed., chapter VI.62,
fetched and read directly this pass). No claim was strengthened; only accuracy
and precision were adjusted. The verifier and the object file were NOT touched,
so both pinned SHA-256 values remain valid.

## Verifications that PASSED unchanged (no edit)

- Object is a valid CFR(5,25). Shipped verifier `verify_cfr525.py` exits 0;
  all 3000 ordered distance events distinct by methods A and B; second verifier
  `verify_cfr.py` returns `OVERALL: OBJECT IS A VALID CFR(5,25): True`. Both
  re-run this pass.
- SHA-256(CFR_5_25.json) = 9e2d9b33...779ffdcc — matches note and recorded value.
- SHA-256(verify_cfr525.py) = 9d7363d0...37dd0bb — matches note.
- `verify_cfr525.py` is 173 lines (matches the note's "173 lines").
- Primary source, verified verbatim against chapter VI.62 PDF this pass:
  * Def 62.1 (p.673) defines circular tuscan-k / florentine (= tuscan-(n-1))
    rectangles — attribution correct.
  * Def 62.26 (p.677): "Let F_c(n) denote the maximum integer F_c such that an
    F_c x n circular florentine rectangle exists." — note's quote is exact,
    including lowercase "florentine".
  * Construction 62.22(1) (p.676): smallest prime factor p gives a (p-1) x n
    circular florentine rectangle — matches.
  * Table 62.27 (p.677), n=25 row reads "4 ...... 24" — matches note exactly.
  * Chapter authors Wensong Chu, Solomon W. Golomb, Hong-Yeop Song; pp.673-678
    — matches.
- Song 2000 citation: Comput. Math. Appl. 39 (2000), no. 11, pp. 31-35,
  DOI 10.1016/S0898-1221(00)00104-8 — page range confirmed [31--35] via the
  Utah TeX bibliography TOC; DOI PII (S0898122100001048) matches. NOTE: the
  internal working file construct/florentine/NOTES.md has an inconsistent
  "31-36"; the SHIPPED note is correct at 31-35. (No shipped-file change.)
- CPro1 open instances (6,21),(5,25),(5,27),(4,33) — confirmed against on-disk
  cpro1/circular-florentine-rectangle.py (OPEN_INSTANCES).
- Negative control: every within-row transposition (all 1500 tested) drops the
  distinct-event count below 3000; a concrete corrupted copy gives
  `[sha256] match = False`, `[meth A] ... 2984/3000`, `FAILED`, exit 1 — the
  note's negative-control sentence is accurate.
- Clean-shell replay of both printed commands (`python3 verify_cfr525.py` and
  `python3 verify_cfr525.py PATH`) passes from a fresh directory.
- Novelty sweep re-run 2026-08-06: no surveyed source asserts F_c(25) >= 5;
  recent literature quotes only the basic bounds p-1 <= F_c(N) <= N-1; Song's
  own 2006 Handbook table records 4 for n=25. song2000.pdf on disk is an
  Elsevier interstitial, not the paper — "not read / no priority claimed" honest.
- Erratum / wrong-value scan: no passage asserts F_c(25) = 4 as truth or gives a
  wrong upper bound; every mention of 4 is qualified as the *recorded* lower
  bound, and the upper bound is stated as 24 = n-1 throughout. Consistent.

## SHOULD-FIX applied

1. Verifier-output block was labeled "verbatim in its final lines" but omitted
   two lines the verifier actually prints in that tail:
   `[shape ] r=5, n=25, 5 rows of length n: True` and
   `[cross ] disk rows == independent transcription: True`.
   FIX (note.tex and note.md): inserted the two omitted lines so the block is a
   faithful contiguous tail; replaced "verbatim in its final lines" with
   "in its final lines (the long verdict line soft-wrapped ... to fit)" so no
   character-exact claim is made about the soft-wrapped verdict line. This does
   not change any result; it makes a reproducibility display honest.

2. "The two linear rows t->t and t->7t are of the form the multiplier
   construction [62.22(1)] produces" could be read as claiming 62.22(1) outputs
   the c=7 row; for p=5 that construction outputs multipliers c in {1,2,3,4},
   so c=7 is not literally among its rows. FIX (note.tex and note.md): reworded
   to "are multiplier rows of the form t->ct that underlies the multiplier
   construction [62.22(1)]" — precise, non-load-bearing, not a strengthening.

## Observed, NOT changed (out of trusted base; flagged for author)

- The authorship footnote describes the search space as "the K-equivariant
  orthomorphisms of Z_25," but row 0 is the identity t->t, whose difference map
  t->0 is not a permutation, so the identity is not an orthomorphism. This is a
  provenance detail, explicitly excluded from the trusted base (the object is
  independently verified), so it was left unchanged pending the author's own
  check of the search-space description. It does not affect Theorem 2.1.

## Result strength — unchanged

Theorem 2.1 remains stated at exactly its defensible strength: an explicit,
independently verified 5 x 25 circular Florentine rectangle establishes
F_c(25) >= 5, one more than the *recorded* lower bound of 4 (Table 62.27,
p.677); no priority over Song 2000 (unread) is claimed.
