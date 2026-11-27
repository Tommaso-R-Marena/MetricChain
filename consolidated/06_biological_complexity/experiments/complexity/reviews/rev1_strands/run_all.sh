#!/bin/sh
# Referee's independent checks for docs/complexity/STRANDS_NN_HARDNESS.md (nothing here imports the author's code).
#   enum.cpp           brute force: all circular orderings x all non-crossing pair sets; faces; connectivity (faces + union-find);
#                      labelled / physical keys; rotational symmetry; structural tiling test; face-string signatures
#   dp.cpp             second, independent exact method (transfer matrix per ordering) for larger instances
#   lib.py             instances, packing / Til / L by brute force, face parser, loop-energy models
#   test_main.py       Theorem 1 + Theorem 3 on 134 instances x 14 models satisfying (H0)-(H2)     -> out_F.txt, out_PL.txt
#   test_dp.py         DP vs brute force (134 instances), then 867 larger/random instances          -> out_dp.txt, out_dp2.txt
#   fragility.py       synthetic violations of (H0)/(H2): coax, dangles, negative bulges             -> out_frag.txt
#   coax_grid.py       threshold for flush coaxial stacking vs bulge penalty
#   params.py, fragility_real.py   published parameter files (ViennaRNA .par, in ../review1_params)  -> out_frag_real.txt
set -e
cd "$(dirname "$0")"
g++ -O2 -std=c++17 -o enum enum.cpp
g++ -O2 -std=c++17 -o dp dp.cpp
python3 test_main.py F  > out_F.txt
python3 test_main.py PL > out_PL.txt
python3 test_dp.py      > out_dp_all.txt
python3 fragility.py    > out_frag.txt
python3 coax_grid.py    > out_coax_grid.txt
python3 fragility_real.py > out_frag_real.txt
