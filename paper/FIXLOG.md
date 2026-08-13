# FIXLOG — adversarial pre-release review of Part A erratum v0.1.2

Reviewer pass: 2026-08-06. Scope: the v0.1.2 erratum (Theorem D fiber count over
`{Δ₂ = 0}`) and its shipped artifacts. Ground truth = `preprint-dixmier-poisson.tex`
+ the `scripts/erratum-check/` output. Rule observed: never strengthen a claim;
the artifacts/scripts are ground truth.

## Verification performed (all passed)

1. **Replay commands, verbatim from a clean shell at repo root** (the three in the
   erratum "Reproduce" block and the Theorem D footnote):
   - `python3 scripts/erratum-check/fibre_check.py` — all asserts pass;
     `det JF = -2`; `resultant cubic / paper cubic = 1`; `disc + 4·Δ₁·Δ₂² = 0`;
     `{Δ₂=0, Δ₁≠0}` → distinct 3 (length 3) at every tested point; `{Δ₁=0}` → 1;
     Γ → 0. SymPy 1.14.0.
   - `python3 scripts/erratum-check/exhibit2.py` — `(4,−12,1)` elim poly
     `(4x−1)(64x²+16x−1)/256`, squarefree, 3 distinct roots; `{Δ₁=0}` degree-1;
     Γ = unit ideal (empty). Matches the erratum's quoted output verbatim.
   - `python3 scripts/erratum-check/structural.py` — `det J_G = 2(s+3u−5)²`;
     `G|_{C=0} = (1,0)`; u²-coefficient = 0; contraction-point fiber size 1;
     113-point sweep on `{Δ₂=0}` all distinct = 3. Matches quoted output.
2. **Independent re-derivation of the map/discriminant.** The raw map in all three
   scripts equals `eq:themap` (the displayed map, PDF eq. (2)) character-for-character;
   `Δ₁, Δ₂` are re-derived by resultant inside `fibre_check.py` (ratio to the paper
   cubic = 1) rather than copied. Confirms genuine independence.
3. **Correction is mathematically correct.** Fiber over `{Δ₂=0}` (Δ₁≠0) is three
   distinct reduced points; `{Δ₂=0}` is an apparent branch (u fails to separate two
   unramified sheets; Δ₂ enters squared). Achievable sizes `{3,1,0}`, never 2.
   The cleanest proof is even shorter than the shipped one and is already in the note:
   `det JF ≡ −2 ≠ 0` makes F étale, so every finite fiber is reduced (distinct =
   length); the trace-free cubic (no u² term) forces length ∈ {3,1,0}. The shipped
   `structural.py` route (det J_G = 2C², contraction to (1,0)) is equivalent and also
   verified. "This is a proof, not a sample" is therefore defensible — kept as-is.
4. **No-propagation, repo-wide.** `grep` over `*.tex *.md *.txt *.json *.py` for
   "two sheets merge" / "drops … to two" / "generically … two": the only hits are
   inside erratum quotations. Every live statement reads three distinct / {3,1,0}.
   PROVENANCE.md, README.md, CITATION.cff, .zenodo.json all use 3/1/0.
5. **Compile.** `tectonic -X compile preprint-dixmier-poisson.tex` → exit 0,
   **20 pages**, 251.60 KiB (= 257,635 B, byte-size-identical to the PDF shipped
   at v0.1.2; the 2026-08-12 documentation pass rebuilt it to 21 pages / 259,293 B),
   only pre-existing cosmetic under/overfull-hbox warnings. Corrected text renders
   ("three distinct points" ×4); wrong phrases survive only in the footnote quote.
6. **Novelty sweep (today).** The underlying fiber-count/image result is public
   (ulam.ai Thm 4.2, 2026-07-20; Shaska arXiv:2607.20210; Mayner §4.3; Speyer/SBS).
   The note credits these (Priority note; PROVENANCE). The corrected value 3/1/0
   agrees with the public 3/1/0 counts, so the erratum asserts no new priority.

## MUST-FIX

None. The correction is correct, internally consistent, no live passage retains the
wrong value, and nothing downstream depended on it.

## SHOULD-FIX (applied)

| # | File | Was | Now | Rationale |
|---|---|---|---|---|
| 1 | `ERRATUM-v0.1.2.md` §2 | "Proposition 5.2/5.3(ii)" | "Proposition 5.3(ii) … §5.3; numbered 5.2 in the Markdown edition" | The 3:1-cover proposition is **5.3** in the canonical PDF/.tex and **5.2** in the .md (the .md does not number remarks). "5.2/5.3" reads as uncertainty; disambiguated to the canonical number + section + edition note. |
| 2 | `ERRATUM-v0.1.2.md` §4 table | "(Prop. 5.2/5.3(ii))" | "(Prop. 5.3(ii), §5.3; 5.2 in the .md edition)" | Same. |
| 3 | `ERRATUM-v0.1.2.md` §3 | "note eq. 1.2" | "note §1.2, the displayed map, eq. (2)" | The map is **eq. (2)** inside **§1.2** ("The map"); "eq. 1.2" conflates the subsection number with an equation number. |
| 4 | `scripts/erratum-check/fibre_check.py` docstring | "preprint eq. 1.2" | "preprint sec. 1.2, displayed map eq. (2)" | Same conflation, in a shipped comment. Comment only — no effect on output (which the erratum quotes). Re-ran: still passes. |
| 5 | `scripts/erratum-check/structural.py` docstring | "broad sweep: 40 rational points" | "113 rational points" | Stale docstring; the code and the actual output (and the erratum text) say 113. Comment only — output unchanged; re-ran to confirm "tested 113 … True". |

## Noted, deliberately NOT changed (out of erratum scope)

- **Pre-existing tex/.md proposition-number divergence (5.3 vs 5.2).** The .tex numbers
  the cover proposition 5.3 (Remark 5.2 "the parked square" consumes 5.2); the .md,
  which leaves remarks unnumbered, numbers it 5.2. This predates the erratum and lies
  outside its two-sentence scope; renumbering the .md would be a separate edit with its
  own error surface. Fix #1/#2 make the erratum's citation correct against the canonical
  PDF and unambiguous for both editions instead.
- **`exhibit.py`** (the slow radsimp variant) was **not** executed: it is excluded from
  the replay set, flagged as slow, and redundant with `exhibit2.py`, which was run and
  passes. Not verified here.
- **`structural.py` module docstring** still describes the sweep prose loosely ("40" →
  "113" fixed; the surrounding proof sketch is accurate). No further change.

## Bottom line

Erratum accepted. Correction verified independently in exact arithmetic; no MUST-FIX;
five citation/precision SHOULD-FIXes applied to supporting docs and script comments
(no live claim touched, PDF unchanged at that time, still 20 pages, scripts still
pass; superseded 2026-08-12 by the documentation pass, which rebuilt the PDF to
21 pages after correcting the Section 7 artifact inventory).
