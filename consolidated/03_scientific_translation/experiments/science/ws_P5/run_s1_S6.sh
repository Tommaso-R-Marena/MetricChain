#!/bin/bash
# P5 step 1 for Ser6 on the helix (104 976 states, 78 atoms): two half-runs over the atom rows in parallel
# (each < 20 min, < 3 GB), then the merge.  Partial files go to out/tmp/ and are removed after the merge.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python3 -B s1_cancel.py S6 H 0.70 5 --blk 3e7 --gg residue,rigid,peptide --rows 0:39 > /dev/null &
python3 -B s1_cancel.py S6 H 0.70 5 --blk 3e7 --gg residue,rigid,peptide --rows 39:78 > /dev/null &
wait
python3 -B s1_cancel.py S6 H 0.70 5 --blk 3e7 --gg residue,rigid,peptide --merge > /dev/null && rm -f out/tmp/s1_S6_H_0.70_rows*.npz
tail -1 logs/s1_S6_H_0.70.log
