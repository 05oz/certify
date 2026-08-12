# Dated novelty and verification sweeps — Kelmans' 1984 problem note (Part I)

Target: Kelmans' Problem 1.10 (1984), "if G is a 3-connected cubic graph then
λ(G) = ⌊v(G)/3⌋"; equivalently, at orders divisible by 3, the Akiyama–Kano P₃-factor
conjecture. Open Problem Garden OPG-46613; West REGS "Factors in regular graphs",
Conjecture 1.

* **2026-08-05 (selection).** Primary source read in full before any attack: Kelmans,
  *Packing 3-vertex paths in cubic 3-connected graphs*, arXiv:0910.2766v2 (29 pp.); Problem
  1.10, Theorem 3.1 (the equivalence theorem), remarks (r1)–(r8), §6 (the R_s construction).
  Open Problem Garden page fetched live — open, posted 2013-03-04, never updated with a
  solution. West's REGS page fetched — Conjecture 1 stated, no resolution, no computational
  verification mentioned. Web sweeps for 2024–2026 work: nearest is 3-star packing in
  claw-free cubic graphs (different problem). No exhaustive verification of the problem at
  any order found anywhere.
* **2026-08-06 (adversarial referee, n ≤ 20).** Verdict signed: `kelmans-certificates/
  verdict-n04-20.md`. Independent pipeline (`refcheck.c` + `refcert.py`, no code shared
  with the search side), independent recount of all 429,865 3-connected cubic graphs on
  ≤ 20 vertices, counts cross-checked against OEIS A002851, OEIS A204198 and McKay–Royle's
  published connectivity tables, negative controls on both failure paths.
* **2026-08-11 (pre-draft, independent).** All of the above re-run by the drafting agent
  immediately before the note was written: the arXiv API (abstracts mentioning P₃-factors
  or 3-vertex paths; *Kelmans* in math.CO; *Akiyama–Kano*), the citing literature of
  arXiv:0910.2766 through OpenAlex and Semantic Scholar, the Open Problem Garden entry and
  West's REGS page fetched live, plus general web sweeps. Clean.
* **2026-08-11 (three-lens review, blocking).** Claims-vs-artifacts, replay-and-tamper, and
  priority-and-citations, each by a separate agent. The primary source was re-read in full
  at every cited passage; the citing literature of arXiv:0910.2766 was re-checked
  (Semantic Scholar `citationCount: 0`, no OpenAlex record, no Crossref published version);
  eight fresh arXiv API queries returned nothing relevant in the last 24 months; the Open
  Problem Garden entry and West's REGS page were fetched live again. Novelty component:
  CLEAN. Two must-fix defects found, both about the source and not about the computation
  (the smallest member of Kelmans' R_s family is cyclically 5-connected, not 6-connected;
  the page range of the Kostochka–Stodolsky reference, inherited from Kelmans'
  bibliography, is wrong).
* **2026-08-11 (fix pass, this release).** Every review finding re-settled against the
  primary artifact or the archived primary source before any edit; decision log ships as
  `kelmans-paper/FIXLOG.md`. Re-verified here, first-hand: West's REGS page fetched live
  (HTTP 200) and Conjecture 1 quoted verbatim; the Kostochka–Stodolsky, Hell–Kirkpatrick,
  Kosowski–Małafiejski–Żyliński and Kelmans (Discrete Appl. Math. 2011) references checked
  against Crossref by DOI; the Kosowski–Żyliński reference against DBLP; the McKay–Royle
  author copy fetched (HTTP 200). The arXiv API did not respond during this pass, so the
  arXiv-side novelty queries of the same day were not repeated a fourth time; they are
  recorded above from the two agents that ran them.

**Verification summary.** All 6,339,157 3-connected cubic graphs on at most 22 vertices
decided for the base claim and for the applicable strong forms of Kelmans' Theorem 3.1, by
two pipelines sharing no code, with zero failures; generated and filtered counts equal to
the published enumerations at every order (A002851 / Brinkmann–Goedgebeur–McKay; A204198 /
McKay–Royle). 53,356 Λ-factor certificates ship — all 43,580 through order 22 and 9,776 at
order 24 — every one re-verified from the graph6 string alone by both standard-library
checkers in this release, 0 rejected. Order 24 is search-side complete (98,101,019 graphs,
zero failures) with **no independent recount**, and is claimed at exactly that strength and
no higher.
