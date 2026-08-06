# FIXLOG — note-tt3-packing (fix pass 2026-08-05)

Three review reports applied: Lens 1 (claims-vs-artifacts), Lens 2 (priority/citations),
Lens 3 (replay audit). Tally: 4 MUST-FIX, 6 SHOULD-FIX (two of them the same issue
reported by two lenses), 7 NITs. All MUST-FIX and SHOULD-FIX applied; all NITs applied.
Every reviewer/draft factual disagreement was re-settled against the primary artifact or
source during this pass (verdicts below). Fixes applied identically to note.tex and note.md.

## CLAIM-LEVEL DOWNGRADES (read first)

1. **n = 11 status.** The draft said the n=11 sweep "is in progress." The record
   (problem-2/q.jsonl: 40/40 jobs, none for n=11; no q11 queue; no running sweep process)
   shows it was never launched. Downgraded everywhere to: within reach, next target,
   **not started**.
2. **Provenance of primary-source reading.** The draft claimed both primary sources were
   "read in full." The record (NOTES.md) documents only KY08. Downgraded to: KY08 read in
   full from the archived copy; Yus04's concluding-remarks account checked verbatim
   against the arXiv text (math/0304180, fetched and archived with this note during this
   fix pass); Yus04 otherwise used as reported in KY08.
3. **Upper-bound credit reassigned KY08 → Yuster 2004.** Yus04 §4 proves the full integral
   upper bound f(n) ≤ ⌈n(n−1)/6 − n/3⌉ with the identical Turán-orientation argument
   ("Conjecture 1.1, if true, would be best possible. We show f(n) ≤ ..."); KY08 §2.4
   itself credits the tournaments to [14] and adds only the fractional strengthening.
   Abstract, §1.3, §1.4, §2.4, Remark 2.1, and Acknowledgments recredited accordingly.
4. **"Verified by computer for all n ≤ 8" narrowed.** Yus04 §4 (checked verbatim):
   n ≤ 7 by hand/direct argument; **only n = 8 by computer**. The draft had reproduced
   KY08's inaccurate secondary summary. All four occurrences fixed; "computer-verified
   range" → "verified range."

## Findings, verdicts, actions (one line each)

### Lens 1 — claims vs artifacts
- L1-1 (MUST): n=11 "in progress" — **reviewer right** (q.jsonl 40/40 done, no n=11 job, no live sweep) — downgraded in abstract and §5 (downgrade #1).
- L1-2 (MUST): "primary sources read in full" — **reviewer right** (NOTES.md names KY08 only; no Yus04 copy existed in the tree) — footnote, §1.1, comment block, and both bibliography entries rewritten (downgrade #2).
- L1-3 (SHOULD, = L3-S1): "all 32 released files" vs unpinned cited files — **reviewer right** (MD5SUMS.txt has exactly 32 entries; n10_chunk_counts.txt, smalln_table.txt, cand9.out, cand10.out, archived PDF unpinned) — §6 now defines the certified release as exactly the 32 pinned files, names the auxiliary files as unpinned, and notes the certified chain runs through pinned files only.
- L1-4 (SHOULD): "byte-identical fresh re-run" — **reviewer right** (RESULTS.md: "enumeration-set equality byte-for-byte", i.e. set equality) — §4 item 1 now says "fresh re-run ... equal to the shipped enumeration as a set of strings byte for byte."
- L1-5 (NIT): completion-immateriality over-attributed — **reviewer right** (KY08 §2.4 proves the upper bound for arbitrary completion; exact-value independence needs this note's computation) — reworded, now also citing Yus04 §4.
- L1-6 (NIT): Theorem 1.1 consequent hid the n ≤ 8 dependence — **reviewer right** — theorem now reads "together with the verified range n ≤ 8 ([Yus04], reproduced in §2.2)"; §2.2 given label ssec:packer.

### Lens 2 — priority and citations
- F1 (MUST): n ≤ 8 computer-verification scope — **reviewer right**, re-settled this pass against Yus04 arXiv text (quote matches reviewer verbatim) — fixed in abstract, §1.1, §1.2, §2.2 (downgrade #4).
- F2 (MUST): upper-bound credit — **reviewer right**, re-settled against Yus04 §4 (arXiv) and the archived KY08 §2.4 ("constructed in [14]" verified in the local PDF) — recredited throughout (downgrade #3).
- F3 (SHOULD): KY08 reference incomplete — **reviewer right**, confirmed via Crossref (Ann. Comb. 12 (2008), no. 3, 291–306, DOI 10.1007/s00026-008-0352-3; archived copy is a 17-pp author preprint) — reference completed; both the entry and the prior-art footnote now state section numbers follow the archived preprint.
- F4 (SHOULD): CaDiCaL uncited — **reviewer right**, confirmed via Crossref (Biere–Faller–Fazekas–Fleury–Froleyks–Pollitt, "CaDiCaL 2.0," CAV 2024, LNCS 14681, 133–152, DOI 10.1007/978-3-031-65627-9_7) — new [BFF+24] entry, cited at the point of use; solver line removed from [CFHKS17].
- F5 (SHOULD): Burnside numbers lacked a canonical source — **reviewer right**, confirmed via Crossref (R. L. Davis, "Structures of dominance relations" — note plural "Structures," Crossref — Bull. Math. Biophys. 16 (1954), 131–140) — new [Dav54] entry, cited in §1.3, §3.2, §4.
- F6 (NIT): OPG "dormant since 2008" — accepted on reviewer's live fetch (not re-fetched here; fix is a strict weakening) — now "records no progress beyond 2008" in §1.1.
- F7 (NIT): OEIS title gloss — accepted (oeis.org unreachable from this pass; gloss made plainly descriptive, not a quote) — "(the number of tournaments on n unlabeled nodes)."
- F8 (NIT): Sinz proof location — accepted on reviewer's verbatim quote — §4 item 2 notes the conference paper states the property and omits the proofs for space.

### Lens 3 — replay audit
- (MUST): none reported; all 32 hashes and all printed commands replayed clean.
- S1 (SHOULD): same as L1-3 — applied once, as above.
- N1 (NIT): replay block silent on redirection/per-slice line numbers — **reviewer right** — one bracketed paragraph added after the replay block in §6.
- N2 (NIT): "0.6 s" wall clock — **both partly right**: NOTES.md records BOTH 0.6 s (formal jobrunner run — the draft's source) and 0.83 s (interactive run); referee measured 0.9–1.2 s — weakened to "about a second."

## Files touched
- note.tex, note.md — all fixes above, kept as faithful twins; %% comment block updated to match.
- primary-source-yuster04-arxiv-math0304180.pdf — added (arXiv math/0304180 fetched 2026-08-05, backs the Yus04 verbatim checks).
- note.pdf — recompiled with tectonic after the fixes.
- No artifact in solve/problem-2/ was modified; no solver campaign was launched.
