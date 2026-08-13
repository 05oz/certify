# FIXLOG — note-k34add (Part J), the k(3,4) uniqueness addendum

## What this file is, and what it is not

**No build-time fix log was kept for v0.10.0.** Part J was built, certified and released without
one, and this file was created on 2026-08-13 — after release — when the Engine 2 re-gate found
that Part J was the only released part with no build log in the deposit.

This file therefore records **only** the corrections made in the v0.14.0 documentation-correction
round. It is not a reconstruction of the v0.10.0 build, and nothing in it is backdated. The
build-time record for Part J is the note itself, `k34add-certificates/README.md`, and
`SWEEP-RECORD-K34ADD-2026-08-11.md`. Decisions taken during the original build that were not
written down at the time are not recoverable and are not invented here.

## Documentation-correction round, 2026-08-13

Three sites carried one claim, and the claim was false. No certificate, checker or certified
value changed; the thirteen witnesses and their verification are untouched.

**J-1. Table 1's caption claimed the coarse invariant fingerprint separates all thirteen
witnesses. It does not.** The caption read "Even this coarse fingerprint separates all thirteen:
no two rows agree in all three columns", and offered w₁ and w₅ as a near-miss agreeing in only
the first two columns.

Re-derived from the thirteen shipped certificates rather than read off the table. For each
`k34add-certificates/w*.json` the invariant triple was recomputed from the arc list alone: arc
count; the N̄-degree sequence, N̄(v) being the non-neighbourhood of v, so deg N̄(v) = 19 − |N(v)|
in the underlying undirected graph; and #{s=7}, the count of QR₇ blocks. All thirteen rows of
Table 1 reproduce exactly. On the full triple:

- w₁ and w₅ agree in **every** column: both (126, 7¹¹ 6⁶ 5³, 11). The caption's own example was
  wrong about itself.
- w₂ and w₄ likewise agree in every column: both (125, 7¹² 6⁶ 5², 12).
- The remaining nine are pairwise distinct, so the triple yields 11 distinct fingerprints of 13.
- The third column is not independent evidence: #{s=7} is the exponent of 7 in the second
  column, for all thirteen rows.

Corrected in both twins and in `k34add-certificates/README.md` to state that the fingerprint
does not by itself separate the thirteen, to name both colliding pairs, and to note that the
third column is determined by the second. Separation is established where it always was — by
the canonical form read off the discrete Weisfeiler–Leman refinement, cross-checked by the
richer invariant `verify_witnesses.py` computes.

**J-2. Two cross-check attributions pointed at Table 1.** Section 2 and Section 5 said pairwise
non-isomorphism was "cross-checked by the invariant fingerprint of Table 1, which already
separates all thirteen" — the same false claim, and the load-bearing one, since it credited the
separation to an invariant that does not achieve it. Both corrected in both twins to credit the
richer invariant the checker computes. The mathematical conclusion is unaffected: the canonical
forms decide non-isomorphism and always did.

Propagation grep (`separates all thirteen`): 0 remaining in tracked text, 0 in extracted text
across all thirteen shipped PDFs. (`invariant fingerprint of Table`): 0 remaining.
(`separate all thirteen`): 3 tracked sites — `k34add-paper/note.tex`, `k34add-paper/note.md`,
`k34add-certificates/README.md` — each the corrected negated form "does not by itself separate
all thirteen". note.pdf rebuilt and verified by text extraction.

## What is trusted

The verification is unchanged by this round: `verify_witnesses.py` re-derives, from each
witness's arc list alone, validity as an oriented graph, freeness over all C(20,3) triples and
C(20,4) quadruples, rigidity by Weisfeiler–Leman refinement to twenty singleton colours
cross-checked by an explicit automorphism count, and pairwise non-isomorphism by canonical form.
It imports only the Python standard library and shares no code with the search.
