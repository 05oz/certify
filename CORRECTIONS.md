# CORRECTIONS — v0.14.0 documentation-correction round

Dated 2026-08-13. Every corrected claim in the round, by part, with what it now says.
**No certificate file, checker, or certified value changed.** Every certificate and every
checker in the deposit is byte-identical to its released form; every checker passes as before
and every mathematical result of Parts A through M stands. Where a shipped certificate's own
prose was found inaccurate, the certificate was left untouched and the correction is stated in
the note. What follows is documentation.

## How these were found

Three passes, each catching what the one before could not:

1. A retroactive cross-examination of ~149 build-log decisions against the prose of their own
   papers. Found 55 defects. The class had never been checked: earlier audits verified metadata,
   links and labels, and treated each paper's own sentences as the reference.
2. A repair round, then a serial repair of the defects the repair itself introduced.
3. An independent referee — a session that did no editing — which re-executed each checkable
   sentence against its artifact rather than reading it, and returned 21 further findings,
   five of them written by the repair.

The procedure and the gates now standing between a claim and the public record are maintained
in the author's working tree and are not part of this deposit.

## Corrections by part

### Part A — Alpöge Keller (v0.1.x)

- `scripts/erratum-check/exhibit.py` queried the point (4/27, 1/3, 1) under a label naming (p,q)=(7/3,4/27). The file's own convention is (q, p−1, 1), so the point is (4/27, 4/3, 1) as its sibling `exhibit2.py` uses. As shipped the script printed three preimages over the locus Theorem D proves empty; it now prints `GB = [1]`, the empty fibre. The script contains no assertions and exits 0 regardless, so it was never a gate.
- The Section 7 artifact inventory listed `gen_ms.py`, which has never existed in the repository or its history.
- The claim that the mod-32003 reproductions ran independently in both msolve and SymPy is retracted: `min_verify.py` part II times out on both Branch-II leaves, and the longer attempt over ℚ times out too. Branch-II emptiness rests on the stored msolve certificates.
- `README.md`: the unknown counts for II-f0 and II-f1 were reversed (18 and 19, not 19 and 18).

### Part B — quantum code distances (v0.2.x)

- The quickstart carried a blanket `gunzip` over `*.lrat.gz` that would have destroyed the three shipped `*_prof_*.lrat.gz` archives, which `check_prof.py` requires gzipped. The hazard had been identified in a build log on 2026-08-06 and fixed only in the paper; the public README carried the command for six days.
- The replayable strength for [[360,12,≤24]] is `d_X ≥ 16` from the shipped artifacts; the previously advertised `16 ≤ d ≤ 24` additionally requires the ZX-duality lemma.
- A machine-specific dangling symlink had been committed into the release and is removed.
- Three `*_prof_*.lrat.gz` archives ship, not four.
- `manifest.py` hands only the largest `check_lower` replays to an external checker, not all checkers.

### Part C, D — tournament packing (v0.3.0), [[14,3,5]] exclusion (v0.4.0)

- Both notes claimed a primary source ships with the artifacts; neither does. The copies are retained in the author's working tree and are not redistributed.
- The Part D certificate directory holds 41 archived run outputs and 2 executable certificates, and the unarchived runs are itemized in Sections 3, 5 and 7.
- The [[14,3,5]] existence question is stated with its dated retrieval facts rather than an unsupported 'open since 2005'.

### Part E, F — Florentine rectangles (v0.5.0), MPS eigenstate (v0.6.0)

- The note claimed the verifier establishes 'the equivalent statement' to the determinant −4. Rank four is equivalent to the determinant being **nonzero**, which is what the proposition's argument requires; it is not equivalent to its value.
- `mps-certificates/object.json` attributed the determinant to `reverify.py` P5, which computes rank. Corrected, with the SHA-256 pin recomputed and propagated.
- The abstract's norm claim is scoped to the L = 3,…,9 range the numpy cross-check actually covers.
- The linearity classification is attributed to the pass that performed it, not to the shipped verifier, which contains no linearity check.

### Part G, J — k(3,4) = 21 (v0.7.0), extremal non-uniqueness (v0.10.0)

- Section 6 listed queue files, block-class representatives and audit records as shipped; none are. The deposit's contents and the private regeneration kit are now described separately.
- 'A skeptic can replay every shipped LRAT certificate' was vacuous: the LRAT corpus is a regenerable cache and is not shipped.
- The IRW preprint copy is in the author's working tree, not the deposit.
- Table 1's coarse fingerprint does **not** separate all thirteen witnesses — w₁ and w₅ agree in every column, as do w₂ and w₄, and the third column is determined by the second. Separation is established by the canonical forms and the richer invariant the checker computes.
- The largest {I₃,TT₄}-free tournament blow-up reaches 14 vertices; 15 is the derived Ramsey lower bound.
- Rigidity of thirteen witnesses does not exclude a fourteenth: the inference that no canonical 20-vertex extremal object exists is withdrawn.

### Part H, K — sub-threshold brackets (v0.8.0), exact P_L (v0.11.0)

- At d = 3 the uncorrectable fault sets **of weight at most 4** number 4823 (55 + 690 + 4078). The total is 2²² = 4,194,304.
- The checker description distinguished the two distances: at d = 3 the search runs to exhaustion over all 256 syndromes; the depth truncation applies at d = 5.
- The shipped checker verifies non-strict containment `L ≤ P_L ≤ U`. Strictness is true but is not what the checker establishes.
- The d = 5 exact values sit at 0.36 and 0.37 of their bracket widths; 0.51 is the d = 3 position.
- Part K is Part K, not Part L, in its own build log and note header.

### Part I — Kelmans 1984 (v0.9.0)

- The order-12 negative control's 253 strong-form failures split 4 + 8 + 106 + 135 across four types; only 135 are of (z8) type.
- `refcert.py` rejects all eight doctored-certificate classes; `verify_cert.py` rejects seven and accepts the non-canonical relabelling, having no membership gate.
- Count agreement holds with one published enumeration at every order and with the other at orders 10 through 20, its tables stopping there.
- The fix pass logged five must-fix entries, not two.
- A control artifact printed a total of 15692 against its own 15691.

### Part L, M — demagnetization tensors (v0.12.x), ZEFOZ (v0.13.0)

- The table carries no `Nyz` entries anywhere; for the rectangular cell on the body diagonal `Nyz` is nonzero and is not a relabelling of any carried component. Coverage is 862 entries: 850 across fifty geometry-and-component combinations away from the origin, plus twelve self-terms.
- The sixteen Maple gold values **agree** with the enclosure midpoints to ≥ 49.6 digits; they do not lie inside the enclosures, which are far tighter, and fifteen of the sixteen lie outside. (Released as the v0.12.1 erratum.)
- The relative enclosure width across the table reaches 1.7×10⁻⁴⁶, not the canonical far point's 2×10⁻⁵⁴, which is exceeded by over a hundred of the 862 entries.
- `demagcoef.cc`'s header carries 31 check rows, 24 of them nonzero; sixteen form the anchor.
- Four of the ten published zero-field transitions have certified positive-definite Hessians — local minima, not saddles.
- The twenty published points span 191 mT to 2.48 T, not 5.3 T.
- The both-sites completeness bound is 1.58×10⁶ laptop-hours.
- The narrowest Hessian bracket is 1.41×10⁻¹⁶ at site 1 (8,13); the highlighted site-2 pair ranks sixth of twenty.

### Part Repository-wide

- `PROVENANCE.md` cited two commit hashes unreachable from any ref, in the section written so a timestamp auditor could check the dates; corrected to `7992c21` and `229bf5e`. It also described four bodies of work against thirteen released parts.
- `INDEPENDENT-VERIFICATION.md`'s finding D2 (bb288 ships no duality certificate) was true when the third-party audit was written and was resolved in v0.2.1; it is annotated as resolved rather than rewritten.
- The Windows replay predates Parts G–M; Parts E and F were already released and were not included.
- The README header ladder and `CITATION.cff` now carry the same DOI set.


---

77 files changed in this round.
