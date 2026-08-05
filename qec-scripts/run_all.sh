#!/bin/zsh
# run_all.sh -- full reproduction of every certificate in certificates/.
# Requires: python (numpy), /opt/homebrew/bin/cadical (>= 3.0, --lrat),
# and tools-drat-trim/lrat-check (cc -O2 -o lrat-check lrat-check.c).
# Wall-clock on an Apple M4 (10 cores, jobs below run sequentially): ~45 min.
set -e
PY=${PY:-python3}

# sanity tier
$PY certify.py init steane
$PY certify.py upper steane X 3 && $PY certify.py upper steane Z 3
$PY certify.py lower steane X 2 && $PY certify.py lower steane Z 2
$PY certify.py five_qubit

# scaling tier: rotated surface codes
for d in 3 5 7; do
  $PY certify.py init surface$d
  $PY certify.py upper surface$d X $d && $PY certify.py upper surface$d Z $d
  $PY certify.py lower surface$d X $((d-1)) && $PY certify.py lower surface$d Z $((d-1))
done

# Golay [[23,1,7]]
$PY certify.py init golay
$PY certify.py upper golay X 7 && $PY certify.py upper golay Z 7
$PY certify.py lower golay X 6 && $PY certify.py lower golay Z 6

# IBM bivariate bicycle codes (Bravyi et al., Nature 627, 2024)
$PY certify.py init bb72
$PY certify.py upper bb72 X 6 && $PY certify.py upper bb72 Z 6
$PY certify.py lower bb72 X 5 && $PY certify.py lower bb72 Z 5

$PY certify.py init bb90
$PY certify.py upper bb90 X 10 && $PY certify.py upper bb90 Z 10
$PY certify.py lower bb90 X 9 && $PY certify.py lower bb90 Z 9

$PY certify.py init bb108
$PY certify.py upper bb108 X 10 && $PY certify.py upper bb108 Z 10
$PY certify.py lower bb108 X 9 && $PY certify.py lower bb108 Z 9

# gross code [[144,12,12]]
$PY certify.py init bb144
$PY certify.py upper bb144 X 12 && $PY certify.py upper bb144 Z 12
$PY certify.py lower bb144 X 11 sym          # 45 s
$PY certify.py lower bb144 X 11              # ~19 min, symmetry-free
$PY certify.py lower bb144 Z 11              # ~13 min, symmetry-free

# [[288,12,18]]: certified lower-bound ladder (the value d = 18 is Bravyi et al.'s,
# asserted there by ILP; these rungs are the machine-checkable part)
$PY certify.py init bb288
$PY certify.py upper bb288 X 18
$PY certify.py lower bb288 X 9 sym               # 11 s
$PY certify.py lower bb288 X 11 sym              # 86 s
$PY certify.py lower bb288 X 13 sym              # 513 s, 2.94 GB proof

# ZX-duality certificates
$PY gen_duality.py

# hash + re-check everything
$PY manifest.py
