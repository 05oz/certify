#!/bin/sh
# Reproduce and verify the d(3,3) >= 6 certificate (Erdos #1111), plus tamper controls.
# Requires: python3 (stdlib only for all checkers); CaDiCaL only to REGENERATE proofs (optional).
set -u
D=$(cd "$(dirname "$0")" && pwd)
LRAT=${LRAT_CHECK:-$D/../k34-scripts/lrat_check.py}
cd "$D"
ok=0
expect() {  # expect <0|nonzero> <label> <cmd...>
  want=$1; shift; label=$1; shift
  out=$("$@" 2>&1); rc=$?
  if [ "$want" = 0 ] && [ $rc -eq 0 ]; then echo "[ok]   $label: $(echo "$out" | tail -1)";
  elif [ "$want" != 0 ] && [ $rc -ne 0 ]; then echo "[ok]   $label (rejected as expected): $(echo "$out" | tail -1)";
  else echo "[BAD]  $label rc=$rc"; echo "$out" | tail -5; ok=1; fi
}
echo "== positive checks: G = graphs/mmc5.edges (Mycielskian of the Groetzsch graph)"
expect 0 "check_P (triangle-free, Criterion A, Criterion B)" python3 check_P.py graphs/mmc5.edges
expect 0 "check_P --pruned" python3 check_P.py graphs/mmc5.edges --pruned
expect 0 "is M(M(C5)) (construction check)" python3 check_construction.py mmc5 graphs/mmc5.edges
expect 0 "audit 4-colouring CNF" python3 audit_cnf.py col graphs/mmc5.edges 4 cnf/mmc5_col4.cnf
expect 0 "LRAT: not 4-colourable" python3 "$LRAT" cnf/mmc5_col4.cnf proofs/mmc5_col4.lrat
expect 0 "audit anticomplete-pair CNF" python3 audit_cnf.py pair graphs/mmc5.edges cnf/mmc5_pair.cnf
expect 0 "LRAT: no two disjoint anticomplete odd cycles (Criterion C)" python3 "$LRAT" cnf/mmc5_pair.cnf proofs/mmc5_pair.lrat
echo "== extra 5-chromatic witnesses (same checks)"
for g in mchvatal mclebsch circ29; do
  expect 0 "$g check_P" python3 check_P.py graphs/$g.edges
  expect 0 "$g audit 4-col CNF" python3 audit_cnf.py col graphs/$g.edges 4 cnf/${g}_col4.cnf
  expect 0 "$g LRAT not 4-colourable" python3 "$LRAT" cnf/${g}_col4.cnf proofs/${g}_col4.lrat
  expect 0 "$g audit pair CNF" python3 audit_cnf.py pair graphs/$g.edges cnf/${g}_pair.cnf
  expect 0 "$g LRAT no anticomplete odd-cycle pair" python3 "$LRAT" cnf/${g}_pair.cnf proofs/${g}_pair.lrat
done
expect 0 "circ29 is Cay(Z_29,{+-2,+-5,+-6,+-14})" python3 check_construction.py circ 29 2,5,6,14 graphs/circ29.edges
expect 0 "Lemma 4 colourings of Cay(Z_2k+1,{1,3})" python3 check_lemma_colourings.py 300
echo "== tamper controls (each must be REJECTED)"
T=$(mktemp -d)
expect 1 "check_P on M(M(M(C5)))" python3 check_P.py graphs/mmmc5.edges
expect 1 "check_P on M(M(Chvatal))" python3 check_P.py graphs/m_mchvatal.edges
# add an edge creating a triangle: 0-1 and 1-2 are edges of the C5, add 0-2
{ read n m; echo "$n $((m+1))"; cat; echo "0 2"; } < graphs/mmc5.edges > $T/tri.edges
expect 1 "check_P with added triangle edge" python3 check_P.py $T/tri.edges
{ read n m; echo "$n $((m+1))"; cat; echo "0 1"; } < graphs/mmc5.edges > $T/dup.edges
expect 1 "check_P with repeated edge" python3 check_P.py $T/dup.edges
# hand-made graph: two disjoint C5s (anticomplete pair) -> must fail
printf '10 10\n0 1\n1 2\n2 3\n3 4\n0 4\n5 6\n6 7\n7 8\n8 9\n5 9\n' > $T/twoc5.edges
expect 1 "check_P on two disjoint C5" python3 check_P.py $T/twoc5.edges
expect 1 "check_P --pruned on two disjoint C5" python3 check_P.py $T/twoc5.edges --pruned
cp cnf/mmc5_col4.cnf $T/a.cnf; echo "9 0" >> $T/a.cnf   # unit x(2,0): 2nd unit with colour 0
expect 1 "audit CNF with extra unit" python3 audit_cnf.py col graphs/mmc5.edges 4 $T/a.cnf
sed '2d' cnf/mmc5_col4.cnf > $T/b.cnf; echo "3 0" >> $T/b.cnf  # replace a clause by a foreign unit
expect 1 "audit CNF with foreign unit" python3 audit_cnf.py col graphs/mmc5.edges 4 $T/b.cnf
python3 gen_cnf.py col graphs/grotzsch.edges 4 0 1 > $T/g4.cnf
expect 1 "LRAT proof replayed against 4-col CNF of Groetzsch (satisfiable)" python3 "$LRAT" $T/g4.cnf proofs/mmc5_col4.lrat
python3 gen_cnf.py col graphs/mmc5.edges 5 0 1 > $T/m5.cnf
expect 1 "LRAT proof replayed against 5-col CNF of M(M(C5))" python3 "$LRAT" $T/m5.cnf proofs/mmc5_col4.lrat
awk 'NR==5{ $NF=""; $(NF-1)=""; } {print}' proofs/mmc5_col4.lrat > $T/c.lrat   # drop a hint from step 5
expect 1 "LRAT proof with a dropped hint (step 5)" python3 "$LRAT" cnf/mmc5_col4.cnf $T/c.lrat
python3 gen_cnf.py pair graphs/mmmc5.edges > $T/p.cnf
expect 1 "pair-LRAT replayed against pair CNF of M(M(M(C5)))" python3 "$LRAT" $T/p.cnf proofs/mmc5_pair.lrat
expect 1 "construction check: M(M(C5)) file vs Groetzsch" python3 check_construction.py mmc5 graphs/grotzsch.edges
expect 1 "construction check: circ29 with wrong generator" python3 check_construction.py circ 29 2,5,6,13 graphs/circ29.edges
rm -rf $T
[ $ok -eq 0 ] && echo "ALL EXPECTATIONS MET" || echo "SOME EXPECTATION FAILED"
exit $ok
