# Dated novelty and verification sweeps — k(3,4) = 21 note (Part G)

* 2026-08-05 (selection): erdosproblems.com/112 live — OPEN, 0 comments, 0 claimed proofs, no
  exact values recorded; literature established the published state: k(3,3)=9 (Bermond 1974),
  k(4,3)=15, k(5,3)=23 and k(3,4) in [9,25] (Ihringer–Rajendraprasad–Weinert, read in full).
  [Correction, 2026-11-17: the version read was arXiv v3. The first arXiv version, v1 of 29 July
  2017, states r(I_3,L_4) <= 24, with a proof by an integer program, and remarks that the largest
  {I_3,L_4}-free Cayley graph has 20 vertices, which implies k(3,4) >= 21; neither is in v2 or v3.
  The reviewers at erdosproblemaday.com pointed out the remark on 2026-11-16. See the note, §1.1.]
* 2026-08-11 (final referee): live #112 unchanged; teorth/erdosproblems "open"/"unformalized";
  arXiv: the only r(I_m,L_n) paper remains IRW (nothing May–Aug 2026); IRW's citing literature
  (1 citation, off-target) and the authors' recent output checked. Clean.
* 2026-08-11 (pre-draft, independent): all of the above re-run by the drafting agent. Clean.
* 2026-08-11 (three-lens review): IRW arXiv:1707.09556v3 re-read in full at every cited passage
  (archived, SHA-256 pinned); every attribution verified; the k(6,3) lower bound separately
  refereed (REFEREE-k63.md in k34-paper/): novelty supported, strongest prior lower bound the
  trivial R(3,6)=18.
  [Correction, 2026-11-17: 18 is the only bound the literature stated, but one-line assemblies of
  IRW's graphs give more: their 22-vertex circulant with a disjoint directed 3-cycle has 25
  vertices, no I_6 and no TT_3, so k(6,3) >= 26. See the note, §5.2.]
Verification summary: 445 certificates, ~1.02e9 checked proof steps, every certificate replayed
by an independently written stdlib checker, twelve re-checked by a second unrelated checker,
eleven of eleven regeneration attempts bit-identical, completeness audited at clause-multiset
level against two independent re-derivations of the case decomposition.
[Correction, 2026-11-17: the second checker, also ours, ran on ten of the 445 certificates and on
the two small certificates of Lemma 3.2, which are not ledger entries; and nine regeneration
attempts are on record, on eight distinct certificates, all bit-identical. See the note, §6 and §7,
and k34-paper/FIXLOG.md, decisions G-9 and G-11.]
