# How much distance does the Kishony–Fowler colour-code circuit lose at its boundary? A proof-carrying answer up to d = 15

**Daniel Kirtchakov**
Independent researcher (`05oz`); no institutional affiliation — daniel@halfounce.io — halfounce.io — ORCID [0009-0009-5213-4098](https://orcid.org/0009-0009-5213-4098)

*Part N of Certify (v0.16.0). Version of October 29, 2026.*

> **Computation and authorship.** The derivations, the code, the checks and this note were
> produced by **Claude** (Anthropic), directed by the author, on one Apple laptop. Every value
> and every machine check stated below is carried by Python-standard-library scripts in the
> repository. Those scripts re-derive the fault mechanisms from the circuit text and replay the
> proofs independently, but the checker shares its formula specification with the encoder that
> produced the solved formulas, so a passing check is not an independent re-implementation of the
> encoding. The guards on that layer are a tamper battery, agreement with the authors' own
> integer program on six instances, and, at d = 15, a second LRAT checker. The repository README
> gives the measured code overlap and the full trust base.

## 1. The question

The circuit-level distance d_circ of a syndrome-extraction circuit is the least number of
circuit faults that flip a logical observable without flipping any detector. It sets the leading
order of the logical failure rate, and a circuit can have d_circ < d even when its code has
distance d. Kishony and Fowler proposed a colour-code syndrome-extraction circuit with **one
auxiliary qubit per plaquette** and colour-dependent CNOT orders. They state that it avoids all
malign hook errors in the bulk, and that apart from the corners no single hook error alone
reduces its distance [KF, abstract and §II]. Issa and Martonosi give counterexamples: on every
non-corner plaquette, bulk included, the schedule has a weight-2 "junction" hook error which,
with d − 2 data-qubit errors, forms an undetected logical error of d − 1 faults. They verified
this at d = 7, 9 and 11, and note that these sets leave the distance the authors report
unchanged [IM]. At the boundary the circuit loses more. The authors identify the
mechanism: three weight-2 hook errors and two data-qubit errors near the boundary are equivalent
to six data-qubit errors along it, and from this they conclude that the circuit-level distance
along the boundaries is "asymptotically reduced by a factor of 5/6" [KF, §II]. They then report:

> "Indeed, we verify numerically that, up to d=13, the circuit-level distance is given by
> d_circ = d − ⌊(d+3)/6⌋." [KF, §II]

The formula is the finite-d form of that argument: d − ⌊(d+3)/6⌋ grows like 5d/6. The loss term
⌊(d+3)/6⌋ is 1 at d = 3, 5, 7, 2 at d = 9, 11, 13 and 3 at d = 15. Over the range the authors
verified numerically, the loss takes only the values 1 and 2, so that range cannot tell a loss
that keeps growing like d/6, as their argument predicts, from one that stops at 2. Every
single-auxiliary schedule obeys the corner bound d_circ ≤ d − 1 [qsim-lab, theory-colour.md:11].
At d = 15 that bound allows any value up to 14. The formula predicts 12, and a loss that stopped
growing at 2 would give 13.

**Question.** What is d_circ of this circuit at d = 15, the first distance beyond the authors'
numerical range and the first at which their formula predicts a loss of 3? A value there tests
the asymptotic argument, not only the formula. And can the values at smaller d be given in a form
that a reader can check without trusting any solver?

**Answer.** d_circ = 12 at d = 15, so the loss reaches 3. Every value from d = 3 to 15 equals
d − ⌊(d+3)/6⌋, and each comes with an explicit fault set (upper bound) and an LRAT refutation
(lower bound). Both kinds of certificate are replayed by a standard-library checker that rebuilds
the fault list from the circuit text. At d = 15 the refutation was also accepted by drat-trim's
`lrat-check`.

## 2. The object

**Circuit.** C(d, r) is the Stim circuit returned by `build_parallel_circuit(d, r, p, S₀)` of
the paper's companion code [KFcode].
- **Schedule.** S₀ is the schedule its benchmark driver loads by default, row 1 of
  `results/zero_collision_schedules.csv`: R = [1,3,2,5,4,6], G = [5,1,4,3,6,2],
  B = [1,5,3,6,2,4]. A referee pass matched it against the paper's Fig. 1(b).
- **Rounds.** In each round the Z checks use CNOT steps 1–6 (data → auxiliary). The X checks
  then use steps 7–12 (auxiliary → data) on the same auxiliary.
- **Noise.** Two-qubit depolarising noise (`DEPOLARIZE2`) follows every CNOT, and nothing else
  is noisy. This is the driver's default `depolarize2_after_cnot` model.
- **Memory experiment.** Z-basis memory; the observable is the Z-parity of the top row of data
  qubits.

The authors' functions were executed verbatim. The only change to their package is one
`from __future__ import annotations` line per module, so that it runs under Python 3.9. That was
seven modules in the first build and eight in a rebuild; the rebuild reproduced byte for byte the
three earlier circuit texts it was compared with. Every circuit text is hash-pinned.

**Fault mechanisms.** M(d, r) is the set of distinct (detector set, observable bit) signatures
of the detector error model of C(d, r). One fault is one two-qubit Pauli after one CNOT, so

  d_circ(d, r) = min { |F| : F ⊆ M(d, r), ⊕_{f∈F} dets(f) = ∅, ⊕_{f∈F} obs(f) = 1 }.

At d = 15 and r = 15, C has 253 qubits, 13,860 CNOTs, 2,520 detectors and 87,901 mechanisms.

**Extended code.** Strikis, Browne and Beverland attach to a single-auxiliary CNOT circuit an
*extended code* [SBB]. Its rows are the checks, and its columns are the data qubits plus one
*residual* column per suffix {i_l, …, i_w} (l = 2, …, w) of each check's CNOT order. Their
Theorem "Circuit distance bounds" gives d_ext ≤ d_circ for every such circuit, with equality when
the circuit is non-interleaved. C(d, r) is non-interleaved. At d = 15 the X-sector extended code
has 84 rows and 547 columns, of which 379 are distinct.

## 3. Why the certificates prove the values

**Upper bounds.** Each upper bound is an explicit set of mechanisms of M(d, d). The checker
XORs the set against the list and confirms that it flips no detector and flips the observable.
At d = 11, 13 and 15 the set was obtained by lifting an extended-code witness: each column is
realised by one mechanism living in a single round. The lifting program is untrusted, because
the checker tests only its output.

**Lower bounds.** Each lower bound is an LRAT refutation of the canonical CNF "some set of at most
K mechanisms flips no detector and flips the observable". This CNF is a parity chain per detector,
a parity chain for the observable and a sequential at-most-K counter. The checker regenerates the
CNF from the mechanism list and matches its SHA-256 against the certificate before replaying the
proof. Three routes are used; the third reaches d = 15.

1. **Direct.** The refutation is on M(d, r) itself and uses no lemma.
2. **X-part sub-list.** M_Z is the sub-list of mechanisms that touch only Z-type detectors. Take
   *Hypothesis A*: every mechanism, restricted to the Z-type detectors and the observable, is
   empty or lies in M_Z. Then restricting each member of an undetected logical fault set, and
   cancelling repeats, gives an undetected logical subset of M_Z that is no larger. Hence
   d_circ(M) = d_circ(M_Z).
3. **Extended code.** Project each mechanism of M_Z to its per-check parity over all rounds,
   together with its observable bit. Take *Hypothesis B*: every such projection is zero or a
   column of the extended code. Parity is additive, so the projections of an undetected logical
   subset of M_Z cancel, after removing repeats, to an undetected logical set of columns that is
   no larger. Hence d_circ(M_Z) ≥ d_ext. A refutation of the extended code's CNF at K therefore
   gives d_circ(d, r) ≥ K + 1.

Hypotheses A and B are finite statements about the explicit lists, and a standard-library script
checks them on every object (d = 3, …, 15; r = 1 and r = d). With them, route 3 needs only the two
paragraphs above. It needs neither the proof of [SBB]'s theorem nor any claim that the theorem
applies to this noise model. [SBB]'s contribution is the construction itself, and the equality
predicted by their theorem is what makes the bound tight.

Hypothesis B is not a new device. For IBM's bivariate-bicycle cycles, [Kornstein] checks that
every fault's data footprint modulo stabilisers is 0 or a column of the extended code, and proves
that the footprints of an undetected logical fault set sum to an extended-code logical
[Kornstein, depth8_cycle/DERIVATION.md, §3b]. Hypothesis B is the same check, made on the explicit
fault list of one colour-code circuit. The checks found no exception: every mechanism satisfied
both hypotheses. Two earlier scripts give a second derivation:
- for Hypothesis B, a build-session script that reads detector coordinates through Stim rather
  than from the circuit text gave identical output on all fourteen objects;
- for Hypothesis A, the build session's sub-list builder gave the same sub-list sizes at
  d = 5, 7, 9.

## 4. Results

**Table 1.** d_circ of C(d, r), Z-basis memory, DEPOLARIZE2 after every CNOT. Every cell is
two-sided: a checked fault set and a checked refutation. The last column names the lower-bound
routes for r = d.

| d | ⌊(d+3)/6⌋ | d − ⌊(d+3)/6⌋ | d_circ, r = 1 | d_circ, r = d | lower-bound routes at r = d |
|---|---|---|---|---|---|
| 3 | 1 | 2 | 2 | 2 | direct; extended code |
| 5 | 1 | 4 | 4 | 4 | direct; X-part; extended code |
| 7 | 1 | 6 | 6 | 6 | X-part; extended code |
| 9 | 2 | 7 | 7 | 7 | X-part; extended code |
| 11 | 2 | 9 | 9 | 9 | extended code |
| 13 | 2 | 11 | 11 | 11 | extended code |
| **15** | **3** | **12** | **12** | **12** | extended code (two LRAT checkers) |

At r = 1 the lower bounds are direct for d ≤ 9 and through the extended code for d = 11, 13, 15.

**At d = 15**, the refutation of the extended code at K = 11 has 53,140,862 lemmas; the proof is
14.1 GB in CaDiCaL's binary format. Two checkers accepted the same proof text:
- drat-trim's `lrat-check`, in 1,168 s, reading a streamed conversion of the binary proof;
- the standard-library checker, which regenerated the formula itself, in 6,167 s, reading the
  stored text proof.

The two inputs were compared afterwards and are byte-identical.

The weight-12 fault set lies in M(15, 15), and the checker verifies it against the list it
re-derives from the circuit text.

**At d = 9**, where the loss first becomes 2, the value 7 is certified at r = d by both the X-part
and the extended-code routes, and at r = 1 by a direct, lemma-free refutation. The direct
refutation at r = d was not obtained.

**Anchors.**
- The authors' own OR-Tools integer program, run verbatim, returned status OPTIMAL with the same
  value on six instances: (3,1), (3,3), (5,1), (7,1), (9,1) and (5,5).
- On (7,7), with a 1,500 s limit, it returned FEASIBLE with incumbent 7 and bound 3. A weight-6
  fault set ships for that instance.

The repository README gives solver costs and proof sizes for the larger refutations, and for the
direct d-round refutations at d = 7 and 9, which were not obtained.

## 5. What is certified, and what is trusted

**Machine-checked:**
- every cell of Table 1;
- the identity of each mechanism list with the one re-derived from its circuit text, without Stim;
- Hypotheses A and B on each list;
- the binding of every certificate to its object and formula by SHA-256.

**Trusted:**
1. That the hash-pinned circuit text is the authors' construction. It was produced by running
   their code, and the 863 other schedules in their table are not covered.
2. The fault model.
   - Uniform-depolarising and SI1000 models add fault locations, which can only lower d_circ.
   - An internal referee pass found the signature sets of the CNOT-only model and a
     location-based uniform model identical at d ≤ 5, and gave a location-by-location argument
     for equality in general. That argument is not certified here.
3. The two short arguments of §3, and CPython.

**Availability.** Five proofs are too large for git: the refutations at d = 13 and 15, and three
of the d-round refutations at d = 5, 7 and 9. A reader checks them by regenerating them with the
procedure in the repository, or by obtaining the originals, whose SHA-256 are listed there. The
checker accepts a regenerated proof on its own merits. Without them, the shipped proofs cover
every value up to d = 11.

**Not claimed:**
- X-basis memory. Its extended code coincides with the Z-memory one (identical hashes at every
  d ≤ 15), so [SBB]'s theorem would give the same values, but no X-memory circuit was checked.
- Round counts other than 1 and d.
- The paper's Monte Carlo results.
- Other schedules, and other colour-code circuits.

## 6. Credit and context

The circuit, its schedule and the formula are Kishony and Fowler's [KF, KFcode]. The extended
code and the theorem that predicts its tightness are Strikis, Browne and Beverland's [SBB]. The
detector error models were generated with Stim [Stim] and re-derived independently.

**Earlier values for this circuit.** The earliest independent values for this circuit found in
the sources read, as of 2026-10-29, are in the qsim-lab repository [qsim-lab,
research/qec/qec-r4.md §2.3]. They are exact minimum weights from
a branch-and-bound search, checked by lifting to the full detector error model, and at most points
cross-checked with MaxSAT or ILP.
- **Rounds = d:** d = 3, 5, 7, 9.
- **One round:** d = 5, 7, 9, 11.

Our values at those points agree with these and are reproductions of them. qsim-lab also proved
the corner bound and published DRAT-checked statements that no schedule in a given design space
reaches a given distance. Those are upper bounds over schedules, not lower bounds for this
circuit.

Two later results concern the same CNOT schedule:
- [Crocker] applies the authors' colour rule on his own lattice and circuit builder, with uniform
  depolarising noise, in Z and X memory. He finds extended-code distances 2, 4, 6, 7 at
  d = 3, 5, 7, 9 by exhaustive search, and, through Stim's detector error model, circuit
  distance 7 at d = 9 for one and three rounds.
- [IM] give the undetected logical errors of d − 1 faults described in §1, at d = 7, 9 and 11, in
  the authors' circuits. These are upper bounds.

Neither ships a proof object for a lower bound on this schedule.

**Other colour-code circuits.** Exact circuit distances have been reported for other circuits:
- the superdense circuit at d ≤ 7, by MaxSAT [Lacroix];
- morphing circuits at d ≤ 9, by Gurobi [ST];
- a 4.8.8 circuit with shared auxiliaries at d = 3, 7, 11, 15, from matching upper and lower
  bounds whose lower-bound method is not named [Shutty];
- another single-auxiliary schedule of the authors' family, C9, at d = 9: circuit distance
  8 = d − 1 in Crocker's construction, in Z and X memory [Crocker].

Of these, [Crocker] has a checkable proof object for the extended-code step of its lower bound:
a DRAT proof, from kissat and checked by drat-trim, that no 7 of the 127 extended-code columns of
C9 sum to a logical operator, so d_ext ≥ 8. The record ships the formula, not the proof: its
script regenerates the proof, checks it and deletes it. The step from the extended code to the
circuit is a check, through Stim's detector error model, that every single fault acts as one of
those columns, made at 1–5, 9 and 25 rounds; the step to every number of rounds is a hand lemma
in a companion note that is not in the record [Crocker, README.md and check_full.py]. The other
three ship no checkable proof (an LRAT, DRAT or formal proof object) of their lower bounds. The
bundle accompanying [Shutty] ships a re-runnable, Stim-based exhaustive check that reproduces
that paper's small-instance lower bounds, triangular d = 3 and torus d = 4 [ShuttyData,
distance/README.md]; it trusts Stim and is not a proof object.

**Other proof-carrying certificates.** Proof-carrying certificates of circuit-level or fault
distance exist for other settings:
- kernel-checked code distances, and phenomenological or timelike fault distances
  [LeanQEC, QECCert, AnYang];
- a DRAT-checked circuit distance for IBM's depth-8 syndrome cycle of the [[72,12,6]]
  bivariate-bicycle code, and circuit distances for larger bivariate-bicycle codes whose DRAT-checked
  steps rest in part on enumerators [Kornstein, depth8_cycle/DERIVATION.md §5];
- for the gross and [[90,8,10]] bivariate-bicycle codes, circuits of period 11 with circuit
  distance 12 and 10, whose extended-code distances and logical-list completeness carry VeriPB
  proofs and whose lift steps carry DRAT proofs checked by drat-trim and `cake_lpr`; and, for
  IBM's depth-8 gross-code cycle, VeriPB-checked lower bounds of 10 for every number of rounds
  up to 12 [Pan].

**What was not found elsewhere.** The following were not found in the sources read, as of
2026-10-29; this note gives each of them:
- a circuit-level distance for this circuit at d = 15, or any test there of the authors' formula,
  whose loss term reaches 3 at d = 15;
- an independent computation, or a checkable proof, of this circuit's distance at d = 13, where
  the authors state that the formula holds [KF, §II] but give no per-d value, round count or
  method;
- a checkable proof (an LRAT, DRAT or formal proof object) of a lower bound on the circuit
  distance of any circuit with the authors' schedule, at any d, or of any colour-code
  syndrome-extraction circuit at d ≥ 11.

The dated record, with the as-of time and the list of sources read in full, is in
`colorcode-dcirc-paper/PROVENANCE.md` and `SWEEP-RECORD-COLORCODE-DCIRC-2026-10-20.md`.

## 7. Questions

**7.1.** The certified loss is ⌊(d+3)/6⌋ at every odd d ≤ 15. Is there a boundary-loss argument
that proves d_circ = d − ⌊(d+3)/6⌋ for all d? Is the minimum fault set always built from the
boundary mechanism the authors describe? The shipped minimum fault sets are the data such an
argument would have to explain.

**7.2.** Here, as in [Kornstein]'s projection check for bivariate-bicycle cycles, a theorem about
a class of circuits was replaced by a few lines of algebra plus a finite check on one circuit.
Which other distance theorems can be made instance-checkable in this way, so that a certificate
never has to cite a proof?

**7.3.** qsim-lab reports a schedule in the authors' design space with circuit distance 8 at
d = 9, one more than the authors' schedule [qsim-lab, research/qec/colour-global.md:18 and §4].
It also conjectures an optimum of d − 2 for d ≥ 11 [qsim-lab, theory-colour.md:274]. Both
concern other schedules.
Certificates of the kind used here would make such comparisons checkable. Do the optimal
schedules lose a bounded amount at the boundary, while this one loses an amount that grows
with d?

**7.4.** The refutation at d = 15 is 14 GB. What reduction would keep proof size polynomial in d?
Examples are a symmetry of the boundary, a decomposition into independent boundary segments, or
cubes that can be checked separately.

## Acknowledgments

The circuit is Kishony and Fowler's, built by their own released code; the extended code is
Strikis, Browne and Beverland's; the detector error models were produced with Stim (Craig
Gidney), used as an untrusted generator and re-derived independently. The note's shape follows
the program's standing constraint: open with the question, cite the computation once, close with
the questions it opens.

## References

- **[KF]** G. Kishony and A. Fowler, *Color code off-the-hook: avoiding hook errors with a single auxiliary per plaquette*, arXiv:2603.28852v1 (2026).
- **[KFcode]** Classiq/classiq-library, `algorithms/error_correction/syndrome_extraction_optimization/`, commit a43d3bd4 (2026-09-01), github.com/Classiq/classiq-library.
- **[SBB]** A. Strikis, D. E. Browne and M. E. Beverland, *High-performance syndrome extraction circuits for quantum codes*, arXiv:2603.05481 (v1 2026-03-05; v2 2026-09-14, theorem statement unchanged).
- **[IM]** S. Issa and M. Martonosi, *Junction Hook Errors in the Color Code*, arXiv:2610.33347v1 (2026).
- **[qsim-lab]** github.com/dylanneve1/qsim-lab (MIT), colour-code files as of commit b5f4b289 (2026-10-07; unchanged at 682845a, 2026-10-11): research/qec/qec-r4.md, research/qec/colour-global.md, research/theory/theory-colour.md.
- **[Shutty]** N. Shutty, *Denser Planar Color Codes*, arXiv:2609.21376v3 (2026).
- **[ShuttyData]** N. Shutty, *Denser Planar Color Codes: source code, circuits, and simulation statistics*, v1.0.0, Zenodo, doi:10.5281/zenodo.22820614; `distance/README.md`.
- **[Lacroix]** N. Lacroix et al., *Scaling and logic in the color code on a superconducting quantum processor*, Nature 645, 614 (2025); arXiv:2412.14256.
- **[ST]** M. H. Shaw and B. M. Terhal, *Optimising quantum error correction using morphing circuits*, arXiv:2604.09797v2 (2026).
- **[Crocker]** C. Crocker, *A d = 9 single-auxiliary colour-code schedule with circuit distance d − 1: reproducibility package*, v1.0, Zenodo, doi:10.5281/zenodo.23633600 (2026-10-25); `README.md`, `check_full.py`, `check_kf.py`.
- **[LeanQEC]** M. Ehatamm, Y. Lee, X. Wu and R. Tao, *End-to-end formalization of quantum error correction*, arXiv:2605.16523 (2026).
- **[QECCert]** QCL-SUAT/QECCertificates, v0.3.0, doi:10.5281/zenodo.23056679.
- **[AnYang]** S. An and F. Yang, *Quantum error-correcting code parameters, checkable by a certificate of provable size*, arXiv:2610.03214v2 (2026).
- **[Kornstein]** M. Kornstein, *Data and code for "The gross code's depth-8 syndrome cycle has circuit distance 10"*, Zenodo, doi:10.5281/zenodo.23394575 (2026-10-15); `depth8_cycle/DERIVATION.md` and `depth8_cycle_independent_checks/REVIEW.md`.
- **[Pan]** G. Pan, *Interleaving recovers the full circuit distance of the gross and [[90,8,10]] bivariate-bicycle codes*, github.com/GavinNull/gross-code-distance-12, release v2.0 (2026-10-24; it supersedes v1.0 of 2026-10-20), and the journal of experiment E-037, `research/journal/2026-10-25-E-037-ibm-cert.md` (2026-10-25), as of commit 1f9757458f (2026-10-27).

*Tool references.* The following are cited only as the software that was run. Their papers were not read in full for this note, and no statement here rests on their contents.

- **[Stim]** C. Gidney, *Stim: a fast stabilizer circuit simulator*, Quantum 5, 497 (2021). Used as an untrusted generator.
- **[CaDiCaL]** A. Biere et al., CaDiCaL 3.0.1. Used as an untrusted solver.
- **[LRAT]** L. Cruz-Filipe, M. J. H. Heule, W. A. Hunt, M. Kaufmann and P. Schneider-Kamp, *Efficient certified RAT verification*, CADE 2017. Cited for the proof format.
- **[drat-trim]** M. J. H. Heule et al., drat-trim and its `lrat-check`, github.com/marijnheule/drat-trim, build of commit 2e3b2dc. Used as the second checker at d = 15.
