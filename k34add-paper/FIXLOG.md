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
It imports only the Python standard library and shares only boilerplate with the SAT
search. It is NOT code-independent of the private structure-mining dig: 30 of its 174
executable lines are verbatim from it, including the backtrackers inside `aut_count` and
`iso` and the predicate `adj`; `i3_free` and `tt4_free` are the private predicates modulo
a parameter list and the order of two operands. The Weisfeiler–Leman refinement, the
canonical form and the invariant fingerprint are written here — `wl_colours` shares none
of its 17 executable lines with the dig — and rigidity follows from the refinement being
discrete alone.


## 2026-08-14 — independence-claim round (Part J, v0.15.0)

The four "share no code with the search / written from scratch" sentences were
replaced by measured statements. Against the SAT search the three checkers share
only boilerplate (25, 32 and 11 lines of 115, 174 and 51). They are not
code-independent of the private structure-mining dig in `hunt-structure/`: 24, 30
and 9 lines are verbatim from it, and `tour_iso` (with all eighteen identifiers
preserved), `qr7`, `adj` and the backtrackers inside `aut_count` and `iso` are the
same routines. The uniqueness conclusion is shown not to need the shared
isomorphism test, by orbit-stabilizer. The drafted correction also claimed two
from-scratch re-implementations reproducing the tournament and witness facts; no
such script is in the deposit or anywhere on disk, so that claim was dropped rather
than published. No count, witness or certificate changed.

**Engine 2 / §11 relocation, same day.** The disclosure above had been written into
the front-matter `\thanks` and had grown to 1,010 words in a five-page paper, breaking
across a page and a half. PROTOCOL §11 rule 1 puts file-by-file inventories, script
names and per-file counts in the repository, not the paper. The footnote is now one
187-word paragraph and the measurement text moved verbatim to
`k34add-certificates/README.md`. Every load-bearing statement survives — stdlib-only;
NOT code-independent of `hunt-structure/`, naming `tour_iso` and its backtracker,
`qr7`, `adj` and the backtrackers inside `aut_count` and `iso`; what a passing check
may therefore not be read as; and the orbit-stabilizer argument. Nothing was softened.
The paper is still 5 pages and both `\thanks` blocks now close on page 1.

Re-derived rather than transcribed, before and after the move: the checkers are 115,
174 and 51 executable lines and share 25, 32 and 11 with the 24 Python files of the
SAT search and 24, 30 and 9 with the six of the dig; `wl_colours` is 17 lines and
shares none; `tour_iso` and `adj` are AST-identical to their private counterparts
after alpha-renaming, `qr7` is the private `qr7_canon` under two renamings, and the
backtrackers inside `aut_count` and `iso` are identical to `aut_and_nesting.py:bt` and
`validate_alts.py:bt`. `verify_qr7_lemma.py` was re-executed (`PYTHONDONTWRITEBYTECODE=1`,
no bytecode written): PASS, exit 0, |Aut(QR_7)| = 21, 240 labelled TT_4-free tournaments
on 7 vertices, 7!/21 = 240, 0 on 8 vertices.

One nuance surfaced by that re-derivation and recorded in `CORRECTIONS.md` rather than
changed here: the two run figures in the moved passage are spans of consecutive
*executable* lines matched contiguously in both files (three against the SAT search, two
against the dig — on physical lines both are two), whereas the other seven parts measure
runs on physical lines. The `blowup_bound.py` "one further run" sub-clause is contiguous
in the checker but not in the search corpus, so it is one-sided; the three lines are
boilerplate and the passage's conclusion is unaffected.

`drafts/note-k34-addendum/` was found carrying a **pre-v0.14.0 claim that v0.14.0 had
already corrected** — that the coarse invariant fingerprint "separates all thirteen",
which it does not, `w1`/`w5` and `w2`/`w4` agreeing in all three columns. It also still
had `\par` where the deposit has `\endgraf` and so would not have compiled. Both working
copies were reconciled to the deposit and their PDF rebuilt. All four copies now match.
