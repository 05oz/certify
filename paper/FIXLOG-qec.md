# FIXLOG — adversarial pre-release review of the qec-d18 paper/update

Reviewer pass: 2026-08-06. Scope: `preprint-qec-distances.tex` (+ `.md` mirror,
`.pdf`) and the shipped certificate corpus behind the August-6 extension that
determines `d([[288,12,18]]) = 18` and adds the `[[360,12,<=24]]` lower bound.
Ground truth = the artifacts on disk (`qec-certificates/`, `qec-scripts/`) and
the on-machine replay results, never the prose. Rule observed: never strengthen
a claim; the artifacts are ground truth. A separate `FIXLOG.md` in this
directory belongs to the concurrent Part A (Dixmier–Poisson) erratum review and
was left untouched.

## Independent re-verification performed (all passed)

All replays used `/usr/bin/python3` (CPython 3.9.6) and the shipped
`qec-scripts/check_prof.py` (479 lines), reading the shipped certificate paths.

| certificate | result | regen CNF | lemmas | check |
|---|---|---|---|---|
| `bb288/bb288_prof_K14.json` | no wt<=14 → d_X>=15, +Lemma P → **d_X>=16** | 4939 vars, 27101 cl | 447,281 | matches paper §6.3 exactly |
| `bb288/bb288_prof_K16_exact.json` | no wt-exactly-16 → **d_X>=18** | 5249 vars, 31208 cl | 2,335,793 | matches paper §6.3 exactly |
| `bb360/bb360_prof_K12.json` | no wt<=12, +Lemma P → d_X>=14 | 13957 vars, 78648 cl | 184,403 | (corroboration) |
| `bb360/bb360_prof_K14.json` | no wt<=14, +Lemma P → **d_X>=16** | 14015 vars, 79397 cl | 428,498 | matches paper §6.4 exactly |

Also re-verified on this machine:
- `check_witness bb288/witness_X.json` → d_X<=18 (declared weight 18). ✓
- `check_duality bb288/duality.json` → d_X=d_Z (passes). ✓ (n=288 ships a duality cert)
- `check_duality bb144/duality.json`, `check_witness bb144/witness_X.json` → pass. ✓
- Lemma P hypothesis: `check_prof` exhibits `c` with `c^T H_Z = 1_n`, `|c|=72` at
  n=288 and `|c|=90` at n=360 — both match the paper. ✓
- Manifest: `verify_manifest.py` → `172 match, 0 mismatch, 10 absent (of 182)`,
  matching REGENERATE.md/§7. ✓
- Byte counts of the shipped prof proofs: 48,415,931 (K14), 43,367,744 (bb360 K14),
  14,725,981 (bb360 K12) — i.e. 48/43/14.7 MB, matching Table 1. ✓
- **bb360 ZX-duality independently confirmed in F₂**: for Π:(b,r,s)↦(1−b,−r,−s),
  rowsp(H_X·Π)=rowsp(H_Z) and rowsp(H_Z·Π)=rowsp(H_X) both hold (my own script,
  using the checker's rref). So the bb360 `d = d_X` step is mathematically true.

**Ladder verdict:** the full `d([[288,12,18]]) = 18` chain (K14 rung + Lemma P;
exact-K16 rung + Lemma P; weight-18 witness; shipped duality) reproduces
end-to-end on this machine with every published var/clause/lemma/|c| count exact.
The result is stated at defensible strength, and the single-encoding dependency
of the weight-16 rung is disclosed in the abstract, §1(B), §5, §6.3 and the
trusted base. No claim in the paper was found to exceed what the artifacts
support.

## Citations checked against primary source (title/authors/date/result)

- **Bravyi et al. [BCGMRY], arXiv:2308.07915, Table 3** (fetched): n=288 listed as
  distance "18" (no "≤"); n=360 as "≤24"; n=756 as "≤34"; caption "≤d indicates
  that only an upper bound … is known"; and "the upper bound d_circ ≤ 18 … is
  unlikely to be tight" refers to the **circuit-level** distance. This confirms
  Remark 5.1's correction verbatim. ✓
- **Okada–Kasai [OK26], arXiv:2607.14091** (fetched): title *Pair-Partition
  Constructions for CPM-Based Quantum LDPC Codes*, authors Okada & Kasai, Jul 2026
  — matches the bibliography. The Sec. V-A even-weight lemma could not be quoted
  from the abstract-only fetch, but the lemma itself is elementary and its
  hypothesis is machine-verified here (|c| exhibited). ✓ (attribution only)
- **Chen–Jafari–Lai [CJL26], arXiv:2606.12445** (fetched): title *SAT, MaxSAT, and
  SMT for QLDPC Distance Computation…*, authors Chen, Jafari, Lai, 29 May 2026 —
  matches. The specific "d≥11 at 7200 s for [[288,12,18]]" figure was not
  re-confirmable from the abstract; it is not load-bearing for any result here. ✓
- **Novelty sweep (today, 2026-08-06):** web search for a machine-checkable / LRAT
  distance certificate for [[288,12,18]] returned only the known sources (Bravyi,
  Tour de gross, BB-existence) — nothing that would pre-empt "first independently
  replayable determination." Consistent with the paper's hedge. ✓

## MUST-FIX (applied)

**M1 — the printed replay block (§8/§10 "Reproducibility") is not replayable as
printed.** Empirically confirmed from a clean shell:
- the `gunzip … bb288/*.lrat.gz … bb360/*.lrat.gz` line **removes the very
  `*_prof_*.lrat.gz` files the three `check_prof.py` certs name**, so every
  check_prof command then fails `FileNotFoundError` (check_prof reads its LRAT
  gzipped). Demonstrated in a scratch copy.
- `check_lower … bb144/lower_X_K11.json` and `…/lower_Z_K11.json` reference the
  868/672 MB symmetry-free proofs that do not ship (REGENERATE items 1, 2) —
  `FileNotFoundError` confirmed.
- `check_lower … bb288/lower_X_K13_sym.json` references `lower_X_K13_i0.lrat`
  (2.94 GB, REGENERATE item 4), which does not ship — `FileNotFoundError`
  confirmed. Only `_i1.lrat` is present.
- the section flagged **only** the K16-exact command as needing regeneration,
  understating what a fresh clone cannot run.

Fix (both .tex and .md): the block is split into **(i)** commands that run on a
fresh clone from shipped artifacts (validated on this machine: witness_X,
duality bb144, prof K14, prof bb360 K12/K14, duality bb288) and **(ii)** commands
that each require regenerating one large proof first (REGENERATE.md items 1, 2,
4, 5). The harmful blanket `gunzip` is replaced by an explicit caution not to
gunzip the prof `.lrat.gz`. Verbatim lines were shortened to remove the overfull
hboxes this introduced.

## SHOULD-FIX (applied)

**S1 — bb360 `d` (vs `d_X`) rests on an unshipped duality.** Unlike n=288, the
bb360 directory ships **no** `check_duality` certificate (and no `HX.txt/HZ.txt`),
and `check_prof.py` does not verify ZX-duality (it checks only the (1,0),(0,1)
translations and the parity combiner). The passage `d_X>=16 ⇒ d>=16` for bb360
therefore relies on a duality lemma that is *verified in exact arithmetic* (I
re-confirmed it, above) but **not shipped as a one-command replayable artifact**.
Several passages implied it was ("… each converted to a statement about d by the
shipped duality certificate"; Table 1 footnote §; trusted-base item 4; §6.4).
Fix: those passages now state the replayable bb360 strength as `d_X>=16`, with
`16<=d<=24` following from the duality lemma verified in F₂ but not shipped for
this code. No claim strengthened; this is a weakening/clarification. (Abstract
left as "we certify 16≤d≤24, the lower end by this method" — defensible because
the bound is true and its main rung is replayable, and the body now carries the
shipping nuance precisely.)

**S2 — trusted-base inventory omitted the totalizer.** §5 "Assumed" item 1 named
only the Sinz counter's completeness, but the prof certificates (behind d=18 at
n=288 and the n=360 bound) use a Bailleux–Boufkhad totalizer with per-row exact
counters and a lex-leader predicate (`tot`/`merge`/`lex_ge` in `check_prof.py`),
not Sinz. Fix: item 1 and the one-sentence summary now record the totalizer's
completeness (and the lex-leader's) as assumed on the same footing as Sinz.

## FLAGGED, not modified (artifact/release hygiene — outside "fix the draft")

**S3 — absolute-path symlink in the certificate tree.**
`qec-certificates/bb288/bb288_prof_K16_exact.lrat.gz` is a symlink to
`/Users/kirt/Documents/reserch math/algo/proofs/bb288_prof_K16_exact.lrat.gz`
(an absolute path outside the repo). It is currently **untracked** in git, so it
is not yet in the release; but if `git add`-ed it becomes a dangling,
machine-specific symlink on any clone — contradicting REGENERATE.md, which says
this 310 MB proof is not carried in git and must be regenerated. **Action for the
author before commit:** do not commit this symlink (leave the proof absent, as
REGENERATE.md item 5 already documents). Not deleted here: it is untracked (not
in the release), it is what enabled the local K16 replay above, and deleting
artifacts is outside a paper-text review.

*Outcome, recorded 2026-08-12.* The action was not carried out. The symlink was
staged and committed in `b3d00ba`, the v0.2.1 release commit reviewed above, and
it is present as mode `120000` in the tag trees v0.2.1 and v0.5.0 through
v0.13.0. Every clone of those trees received a dangling absolute symlink at the
path REGENERATE.md item 5 tells the reader to write the regenerated proof to, so
the documented `gzip bb288_prof_K16_exact.lrat` step, and any `gunzip
bb288/*.lrat.gz` loop, failed on a fresh clone. The paragraph above therefore
describes the state at review time only; its "currently untracked" was overtaken
by the release commit. The symlink has now been removed from the index, and
REGENERATE.md item 5 states plainly that the path is empty and that the
procedure is what fills it.

**Directory-name mismatch (observation).** The printed commands use
`certificates/…` and bare `check_witness.py`, describing a bundled `qec/`
layout; the dev repo uses `qec-certificates/` and `qec-scripts/`. Ensure the
shipped bundle matches the printed paths (or vice-versa). Not edited, because the
intended release layout is the author's to fix and the paper is internally
consistent in the `qec/` convention.

*Outcome, recorded 2026-08-12.* Resolved the other way round: no `qec/`-layout
bundle exists in the repository, so §10 of both twins now names the release
layout — checkers in `qec-scripts/`, certificates in `qec-certificates/`, every
command run from the repository root. The six group-(i) commands were
re-executed verbatim from that root on 2026-08-12 and all six pass. The two
remaining bare `certificates/` references (§1.3 in each twin) were corrected to
`qec-certificates/` in the same pass.

## Erratum check (task item 5)

The paper's own internal correction (Remark 5.1: the earlier draft misread
Bravyi's circuit-level `d_circ ≤ 18` "unlikely to be tight" as a hedge on the
code distance). Confirmed **correct** against the primary source (Table 3 lists
288 as exact 18; the "unlikely to be tight" line is about `d_circ`). Confirmed
**no propagation**: `grep` over `.tex`/`.md` finds "unlikely to be tight" only
inside the corrective passage and the header comment; no live statement retains a
heuristic/upper-bound-only reading of the 288 distance.

## Compile

`tectonic preprint-qec-distances.tex` → PDF written, **22 pages**, 235,598 bytes.
Final-pass log: **0 undefined references, 0 undefined citations, 0
multiply-defined labels, 0 overfull hboxes**; rendered PDF has 0 `??`
placeholders. New cross-reference `\ref{ssec:bb360}` resolves.

## Bottom line

The d=18 result and the n=360 lower bound are sound and reproduce end-to-end on
this machine with every published count exact; the three verifiable citations
match their primary sources; the internal erratum is correct with no propagation.
One MUST-FIX (a replay block that did not replay) and two SHOULD-FIX
(bb360-duality-not-shipped; totalizer absent from the trusted base) were applied
without strengthening any claim; one release-hygiene item (an absolute-path
symlink) is flagged for the author to remove before commit.
