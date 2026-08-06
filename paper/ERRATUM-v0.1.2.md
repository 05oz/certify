# Erratum v0.1.2 — Part A (Alpöge Keller map)

**Note:** *Degree minimality in the equivariant class of the Alpöge Keller map, and the moment-map structure of its cotangent lift* (`paper/preprint-dixmier-poisson.{tex,md,pdf}`).
**Affected releases:** v0.1.0, v0.1.1.
**This release:** v0.1.2, 2026-08-06.
**Scope:** one geometric value in Theorem D (the fiber count over `{Δ₂ = 0}`). Two sentences. No other claim in the note depended on it.

This erratum supersedes v0.1.0 and v0.1.1 **on this point only**. Every other statement in those releases stands unchanged.

---

## 1. What was wrong, and where

Theorem D reported that the set-theoretic fiber of the map `F : ℂ³ → ℂ³` drops to **two** points over the pullback of `{Δ₂ = 0}`. It does not. The fiber there has **three distinct** points.

The error occurred in two places, both in Theorem D (statement and proof).

**(A) Theorem D, statement** — `preprint-dixmier-poisson.tex` (v0.1.1) around l. 302; `preprint-dixmier-poisson.md` l. 74. Verbatim:

> "Generic fibers of F have three points; the count drops **(generically) to two over the pullback of {∆₂ = 0}** and to one over the pullback of {∆₁ = 0} — two sheets escaping to infinity — and to zero exactly on Γ, where all three sheets have escaped."

**(B) Theorem D, proof, "Fiber counts"** — `preprint-dixmier-poisson.tex` (v0.1.1) around l. 1035; `preprint-dixmier-poisson.md` l. 242. Verbatim:

> "Fiber counts. Generic fibers have three points. **Over {∆₂ = 0} (with ∆₁ ≠ 0) two sheets merge;** over {∆₁ = 0} \ {(7/3, 4/27)} the cubic drops degree and exactly one preimage remains — two sheets escape to infinity; at (7/3, 4/27), i.e. over Γ, all three sheets have escaped and the fiber is empty."

The false content is the phrase "drops (generically) to two over the pullback of `{Δ₂ = 0}`" / "two sheets merge." Note that the paper's own adjacent *Priority* note already recorded the correct triple **3/1/0** (`.tex` l. 309, `.md` l. 76: "The fiber counts 3/1/0 …"), so the document was internally inconsistent, and the correct value was already present one paragraph away.

---

## 2. The correct statement

Over the pullback of `{Δ₂ = 0}` (with `Δ₁ ≠ 0`) the fiber of `F` has **three distinct points**. `{Δ₂ = 0}` is an *apparent* branch locus: the invariant `u = 1 + xy` fails to separate two of the three unramified sheets, which is exactly why `Δ₂` occurs **squared** in the discriminant identity `disc = −4·Δ₁·Δ₂²` (Proposition 5.3(ii) of the note, in §5.3; the same proposition is numbered 5.2 in the Markdown edition). The count drops to **one** over `{Δ₁ = 0} \ {(7/3, 4/27)}`, where the cubic drops degree `3 → 1` (its `u²` term is absent by the trace identity, so two sheets escape to infinity at once), and to **zero** exactly over `(7/3, 4/27)`, i.e. on `Γ`, where all three sheets have escaped.

**The achievable set-theoretic fiber sizes are exactly `{3, 1, 0}`. The value `2` never occurs.**

---

## 3. Independent re-verification

The check was written from scratch from the raw map `F` (note §1.2, the displayed map, eq. (2)), reusing no existing script. Exact arithmetic throughout (SymPy over ℚ). The scripts ship in the repository under `scripts/erratum-check/`:

```
scripts/erratum-check/fibre_check.py    direct fiber counts across all four strata
scripts/erratum-check/exhibit2.py       exact elimination polynomials + explicit preimages
scripts/erratum-check/structural.py     structural certificate that size 2 is unreachable
scripts/erratum-check/exhibit.py        (slower radsimp variant of exhibit2.py; same conclusion)
```

**Method.** `F₁, F₂, F₃` are each linear in `z` (leading `z`-coefficients `(1+xy)³`, `3x(1+xy)²`, `−x³`). Eliminating `z` by exact polynomial combinations gives `h₁, h₂ ∈ ℚ[x,y]`. For any target with `t ≠ 0` one has `h₁(0,y) = −t ≠ 0`, so no fiber point has `x = 0`; the distinct fiber size then equals the degree of the squarefree part of the elimination polynomial in a separating coordinate, cross-checked against the scheme length (Gröbner staircase).

### 3.1 Direct fiber counts — `fibre_check.py` (decisive lines)

```
det JF = -2 (expected -2)
resultant cubic / paper cubic = 1 (should be u-free constant in QQ(p,q))
disc + 4*Delta1*Delta2^2 = 0 (should be 0)

=== DIRECT set-theoretic fibre counts over raw F (t=1) ===
[generic]
  generic (p,q)=(2,5): target=(5,1,1)   distinct_points=3  length_w_mult=3
[Delta_2 = 0, Delta_1 != 0  -- DISPUTED stratum]
    check: Delta2(-11,4)=0, Delta1=-512
  Delta2=0 (p,q)=(-11,4):  target=(4,-12,1)   distinct_points=3  length_w_mult=3   # NOT 2
    check: Delta2(-11,-8)=0, Delta1=-2000
  Delta2=0 (p,q)=(-11,-8): target=(-8,-12,1)  distinct_points=3  length_w_mult=3   # NOT 2
[Delta_1 = 0 rational points (scan), excluding Gamma (7/3,4/27)]
  Delta1=0 (p,q)=(-6,2) [Delta2=125]: target=(2,-7,1)   distinct_points=1  length_w_mult=1
  Delta1=0 (p,q)=(-3,-4) [Delta2=512]: target=(-4,-4,1) distinct_points=1  length_w_mult=1
  (… all Delta_1=0 rational points scanned give distinct_points = 1 …)
[Gamma point (7/3, 4/27) -- expect EMPTY]
  Gamma (p,q)=(7/3,4/27): target=(4/27,4/3,1)  distinct_points=0  length_w_mult=None
```

The first three lines reproduce, from the raw map, `det JF = −2`, the paper's cover cubic, and the discriminant identity `disc = −4·Δ₁·Δ₂²` (`disc + 4·Δ₁·Δ₂² = 0`). Every point tested on the disputed stratum `{Δ₂ = 0, Δ₁ ≠ 0}` returns **3**, not 2.

### 3.2 Exact preimages on the disputed stratum — `exhibit2.py`

```
Delta2=0 (p,q)=(-11,4): target=(4, -12, 1)
  elim poly in x = (4*x - 1)*(64*x**2 + 16*x - 1)/256
  degree=3  distinct x-roots=3  squarefree=yes

Delta2=0 (p,q)=(-11,-8): target=(-8, -12, 1)
  elim poly in x = (10*x - 1)*(100*x**2 + 10*x - 1)/1000
  degree=3  distinct x-roots=3  squarefree=yes

generic (p,q)=(2,5): target=(5, 1, 1)
  elim poly in x = (665*x**3 + x - 2)/665
  degree=3  distinct x-roots=3  squarefree=yes

Delta1=0 (p,q)=(-6,2): target=(2, -7, 1)
  elim poly in x = (25*x - 2)/25
  degree=1  distinct x-roots=1  squarefree=yes

Gamma (p,q)=(7/3,4/27): target=(4/27, 4/3, 1)
  reduced GB = [1] -> UNIT (empty fibre)

Exact single preimage over Delta1=0 target (2,-7,1):
   {x: 2/25, y: -17/2, z: -10575/8}  F= (2, -7, 1)
Gamma target (4/27,4/3,1) [(p,q)=(7/3,4/27)]: solving F=target -> []
```

Over the disputed target `(4, −12, 1)`, i.e. `(p,q) = (−11, 4)` on `{Δ₂ = 0}` with `Δ₁ = −512 ≠ 0`, the elimination polynomial in `x` is squarefree of degree 3 with **three distinct roots** — three genuine, reduced preimages. The discriminant vanishes on `{Δ₂ = 0}` only because the invariant `u` fails to separate two unramified sheets: on this fiber the `u`-cubic factors as `−16·(2u+1)·(4u−1)²` (double root `u = 1/4` carrying two distinct fiber points `x = (−1 ± √2)/8`, plus the simple root `u = −1/2`). That is an apparent branch, not a genuine one.

### 3.3 Structural certificate that `2` is unreachable — `structural.py`

```
(a) det J_G - 2*C^2 = 0  (should be 0)
    det J_G = 2*(s + 3*u - 5)**2
(b) G|_{C=0} = ( 1 , 0 )  (should be (1,0))
(c) cubic in u = ...   u^2 coefficient = 0  (should be 0)

u-cubic factorization on Delta_2=0 samples (double root = u NOT separating):
   (p,q)=(-11,4):  -16*(2*u + 1)*(4*u - 1)**2
   (p,q)=(-11,-8): -16*(5*u - 2)*(5*u + 1)**2

(d) fibre over contraction pt (p,q)=(1,0), target (0,0,1): [{x: 1/2, y: 0, z: 0}]   -> size 1

Broad sweep on {Delta_2=0}, Delta_1!=0 (distinct fibre size over each):
  tested 113 points on Delta_2=0;  all distinct==3 ? True
```

This is a proof, not a sample. A genuine 2-point fiber would require either

- exactly **one** sheet to escape to infinity — impossible, because the elimination cubic has no `u²` term (line (c)), so when the leading coefficient `Δ₁` vanishes the degree drops `3 → 1`, escaping two sheets at once, never one; or
- two of three finite sheets to **genuinely merge** — impossible off `{C = 0}`, since `det J_G = 2C²` (line (a)) makes `{C = 0}` the entire ramification locus of the downstairs `3:1` cover `G`, and `G` contracts `{C = 0}` to the single point `(1,0)` (line (b)), whose fiber is `1` (line (d)).

Hence the distinct fiber size lies in `{3, 1, 0}` everywhere; `2` is unreachable. A broad sweep of 113 rational points on `{Δ₂ = 0}` with `Δ₁ ≠ 0` returns 3 at every point.

---

## 4. Nothing else depended on the erroneous value

Checked claim by claim; the wrong "2" / "two sheets merge" is isolated and non-load-bearing.

| Downstream item | What it uses | Status |
|---|---|---|
| Generic degree 3 / "generically 3:1" (Thm B; Thm D; the `3:1` cover) | the **generic** count 3 only | correct, untouched |
| Image theorem `im F = ℂ³ ∖ Γ` (Thm D) | fiber nonempty ⇔ off `Γ`; over `{Δ₂ = 0}` it is 3 (nonempty either way) | correct, untouched |
| Discriminant / `S₃` monodromy (Prop. 5.3(ii), §5.3; 5.2 in the .md edition) | the identity `disc = −4·Δ₁·Δ₂²` and squarefreeness of `Δ₁` | correct (re-derived: `disc + 4·Δ₁·Δ₂² = 0`); the corrected reading — `Δ₂` squared = apparent branch — is **more** consistent with the `S₃` statement, not less |
| Theorems A, B, C, E | do not reference the `{Δ₂ = 0}` fiber count at all | untouched |

The correction replaces the `{Δ₂ = 0} → 2` / "two sheets merge" description with `{Δ₂ = 0} → 3` (apparent branch). The surviving mathematics — generic degree 3, image `ℂ³ ∖ Γ`, `S₃` monodromy — is unaffected. This was a genuine geometric mischaracterization (not a typo), but its blast radius is two sentences with no propagation.

---

## 5. Changes made in v0.1.2

- `paper/preprint-dixmier-poisson.tex` — Theorem D statement and the "Fiber counts" paragraph of its proof corrected; a dated `CHANGELOG` block added to the file header; an erratum footnote attached to the Theorem D statement; the erratum release noted in the title footnote.
- `paper/preprint-dixmier-poisson.md` — same two passages corrected; a dated erratum blockquote added below the title.
- `paper/preprint-dixmier-poisson.pdf` — recompiled from the corrected source (tectonic).
- `README.md`, `CITATION.cff` — note that v0.1.2 supersedes v0.1.x on this point.

**Reproduce this erratum:**

```sh
python3 scripts/erratum-check/fibre_check.py
python3 scripts/erratum-check/exhibit2.py
python3 scripts/erratum-check/structural.py
```

Each terminates with all assertions passing. (SymPy over ℚ; no OS-specific calls.) `exhibit.py` prints the same radical preimages as `exhibit2.py` but uses `radsimp` and runs slowly; it is included for completeness only.
