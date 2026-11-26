# Dated novelty and verification sweep — CFR(5,25) note (Part E), 2026-08-06

Gate and adversarial review both ran on 2026-08-06, primary sources read directly:
* Object re-verified twice with independent standard-library checkers (all 3000 ordered-pair/
  distance events distinct — the maximum possible); SHA-256 of object and verifier pinned in the
  note and unchanged through review.
  [Correction, 2026-11-17: the two checkers are not code-disjoint; v0.15.0 measured 26 of the
  shipped checker's 104 executable lines in the second. See the note, §3, and CORRECTIONS.md.]
* Recorded value: Handbook of Combinatorial Designs, 2nd ed. (2006), §VI.62 (Chu–Golomb–Song),
  Table 62.27, p. 677: F_c(25) = 4. Read directly from the chapter PDF.
  [Correction, 2026-11-17: the table entry is the range "4 ⋯ 24", lower bound 4, as the note
  quotes it; it does not give F_c(25) = 4.]
* H.-Y. Song (2000, Comput. Math. Appl. 39, no. 11, 31–35; DOI 10.1016/S0898-1221(00)00104-8)
  remained inaccessible after repeated attempts;
  the note therefore claims F_c(25) ≥ 5 against the RECORDED Handbook value only and explicitly
  claims no priority over the unread 2000 paper. This limitation is stated in the note itself.
  [Correction, 2026-11-17: the paper has since been read in full (author's copy). Its Table 1
  gives n = 25 as "4, ..., 24", the basic lower bound, so F_c(25) ≥ 5 exceeds it too. The
  Handbook's Table 62.27 is out of date at n = 33, 35 and 39, so exceeding it is not by itself
  novelty; see the note, §5.]
* Full-text searches on "circular Florentine rectangle", "Tuscan square", and F_c(25): no other
  competing value found as of 2026-08-06.
Claim at defensible strength: the explicit 5×25 array establishes F_c(25) ≥ 5, exceeding the
recorded lower bound of 4.
