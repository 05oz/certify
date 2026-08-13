# FIXLOG — adversarial pre-release review of note-mps-eigenstate

Reviewer pass: 2026-08-06. Ground truth = the shipped artifacts and the
verifier gate (`reverify.py` 20/20; `xcheck.py` printed cross-check, L=3..9).
Edits below only ever
*weaken* claims to what the gate supports; no claim was strengthened. The
hash-pinned artifacts (`reverify.py`, `xcheck.py`, `object.json`) were NOT
modified, so Table 1 remains valid.

## Verification performed (all passed)
- Reran printed replay verbatim from a clean shell: `python3 reverify.py` →
  ALL CHECKS PASS (20/20, exit 0); `python3 xcheck.py` → printed H@psi==0,
  ||psi||^2=4^L for L=3..9 (that script asserts nothing and exits 0
  unconditionally, so its exit status is not a gate; the values were read off
  its output); `shasum -a 256` matches Table 1 for all three files.
- Independent symbolic re-derivation (sympy, no shared code): h matrix, all 16
  certificate entries, det[I;A0;A1;A0A1] = -4, contiguous rank 4, odd/even rank
  2/4/8 at L=4,6,8 — all reproduced. Probed L=10,12: odd/even rank 16,32 and
  ||psi||^2=4^L continue the pattern (corroboration only; not shipped, not a proof).
- Telescoping proof (Prop 2.2) checked by hand including the wraparound bond
  (i=L) via trace cyclicity: rigorous and uniform in L. Certificate (u,v)=(0,0)
  worked numbers in the Lemma proof verified.
- All five citations verified against primary sources (arXiv/IOP), 2026-08-06:
  DEHP93 (DOI 10.1088/0305-4470/26/7/011, J.Phys.A 26 (1993) 1493); GE26
  2605.03020 (Eq.(6) general / Eq.(10) "hAA=EA-AE"; Model I = Rydberg+DM, S=1/2
  free complex param — matches note exactly); GRMSV26 2603.28349 (necessary &
  sufficient local eq.; XXZ quantum-group example); IM25 2503.16327 (PXP
  kinetically-constrained area-law eigenstates); PGCGB20 PRX 10, 021051 (2020)
  (non-thermal states exact "in the large-size limit").
- Forbidden-word scan: no "scar" self-description; "thermal"/"ergodicity"
  appear only inside explicit disclaimers and the PGCGB20 citation.
- No erratum component to this submission (checklist step 5 N/A); swept every
  numeric value (A0,A1,C0,C1,h,det,ranks,norms) for cross-passage consistency —
  all agree across abstract, Thm 1.1, §2, §3, and object.json. No stale value.

## MUST-FIX applied
- **M1 (overclaim: unbounded product-state complexity).** Abstract, Theorem 1.1,
  and §3 asserted |psi_L| "is not a sum of a bounded number of product states"
  / "no single k can present the whole family." This is an all-L (unbounded-rank)
  statement; the gate proves the odd/even Schmidt rank only at L=4,6,8 (2,4,8).
  Unbounded growth is an observed pattern (2^{L/2-1}), not in the trusted base.
  Rewrote all three passages to state exactly the supported fact: the odd/even
  Schmidt rank equals the minimal product-state count across that cut, so
  |psi_8| requires >=8 product states and the count grows over L=4,6,8; the
  2^{L/2-1} growth is recorded as observed, not established for all L, with no
  L-uniform complexity claim for the family. (note.tex + note.md.)

## SHOULD-FIX applied
- **S1 (verification-coverage overstatement).** Abstract said "Every quantitative
  claim ... independently, by a dense numpy build." xcheck.py only re-establishes
  the eigenvalue property (H@psi=0), the norm, and Hermiticity for L=3..9 — not
  the certificate, ranks, span, or rotation. Scoped the abstract to "the
  eigenvalue property is independently re-established by a dense numpy build."
  (§4 body was already correctly scoped; left as is.) (note.tex + note.md.)
- **S2 (citation traceability).** Added the verified full titles to the [GE26],
  [GRMSV26], [IM25] bibliography entries (previously arXiv-number-only) and the
  full PRX title to [PGCGB20]. Improves the prior-art record; no claim changed.
  (note.tex + note.md.)

## Flagged, NOT edited (rationale)
- **Widen the novelty sweep before formal submission.** Today's sweep surfaced
  adjacent work not among the four swept sources: Karle, Serbyn, Michailidis,
  "Area-law entangled eigenstates from nullspaces of local Hamiltonians"
  (arXiv:2102.13633, 2021; bond-dimension-2 exact zero-energy MPS eigenstates of
  two-local Hamiltonians) and crosscap-state eigenstates (arXiv:2503.15640).
  Neither contains the specific pair, and both differ (area-law regime; the
  present object has GROWING odd/even rank). The note's novelty claim is already
  bounded ("finite sweep ... cannot exclude an unexamined venue"), so no
  weakening is required. Not added as citations because they were read only at
  abstract level; LAW (1) bars citing a source not read in full.
- **Inert sign slip (not in the paper).** The informal density-density expansion
  in construct/NOTES.md and a comment in reverify.py reads
  "2 n_i X_{i+1} - 2 n_i + 4 n_i n_{i+1}"; the correct expansion is
  UHU^{-1} = 2 sum n_i X_{i+1} + 2 sum n_i - 4 sum n_i n_{i+1} (verified as 4x4
  matrices). The paper's Remark 3.2 makes only the qualitative "additional
  density-density term" claim (correct), and the executed P7 check verifies the
  compact form -2 sum P0_i (Z-X)_{i+1} directly, so the slip is inert. NOT edited:
  reverify.py is SHA-256-pinned in Table 1; touching a comment would break the
  pinned hash for no substantive gain.

## Addendum, 2026-08-12 (§14 retroactive sweep)

- **Printed verdict rescoped in `reverify.py`.** The final RESULT line asserted
  the object is "not a finite sum of product states," and the P4 rationale in
  the module docstring reasoned "growing rank => not a finite cat of product
  states." That is the unbounded-rank claim M1 above retracted from the note;
  read at any fixed L it is also false, every finite-dimensional state being a
  finite sum of product states. Both passages were rewritten to the gate's
  actual content: odd/even Schmidt rank 2, 4, 8 at L = 4, 6, 8, hence a minimal
  product-state count across that cut that grows over those three lengths, with
  the 2^(L/2-1) pattern recorded as observed and not established for all L. No
  check was altered; `python3 reverify.py` still reports ALL CHECKS PASS (20/20,
  exit 0).
- **Table 1 re-pinned.** That edit changes the file, so the digest recorded for
  `reverify.py` in note.tex and note.md was recomputed:
  eac86c33...7177ec4 -> e57a0aea...ff9179d9. `xcheck.py` and `object.json` are
  unchanged. The "hash-pinned artifacts were NOT modified, so Table 1 remains
  valid" statement in the header above, and the hash-pin rationale under
  "Inert sign slip," are records of the 2026-08-06 pass and no longer describe
  the shipped file; the sign-slip comment itself is still present in
  `reverify.py`.
- **Verification-coverage sentences scoped.** The abstract's "Every quantitative
  claim is re-established ... by a standard-library exact-arithmetic verifier"
  and the parallel sentence opening §4 were replaced by per-code coverage:
  `reverify.py` re-establishes the certificate, the eigenvalue property, the
  Schmidt ranks and the spanning property; `xcheck.py` recomputes the eigenvalue
  property and the norms ||psi_L||^2 = 4^L; the determinant -4 of Prop. 2.3 is
  computed by neither, the verifier establishing the equivalent rank-four
  statement (P5). Re-derived independently this pass: det[I;A0;A1;A0A1] = -4.
- **`xcheck.py` described as printing, not gating.** §4's "It confirms ..." now
  states that the script prints its booleans and the exact squared norm, makes
  no assertion, and exits 0 unconditionally, so the comparison with 4^L is made
  against its printed output. Re-executed 2026-08-12: all booleans True, norms
  64, 256, 1024, 4096, 16384, 65536, 262144 for L = 3..9, i.e. exactly 4^L.
  The same scoping was applied to SWEEP-RECORD-MPS-2026-08-06.md and to the
  replay bullet above.
- **Not fixed, out of scope for this pass.** `mps-certificates/object.json`
  attributes "coefficient determinant = -4" to `reverify.py` P5, which verifies
  rank == 4 and computes no determinant. The file is a certificate JSON and was
  left untouched.
