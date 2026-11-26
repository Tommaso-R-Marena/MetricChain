#!/bin/bash
# P5 step 1 for Leu12 on the helix (4 096 states, 240 atoms), orders 3..6, in two runs of < 10 min each:
# (1) exact constants (phase A, checkpointed in out/tmp/), (2) the rest; P3's bound subset by subset up to order 5 only.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python3 -B s1_cancel.py L12 H 0.60 6 --gg residue,rigid,peptide --rows 0:240 > /dev/null
python3 -B s1_cancel.py L12 H 0.60 6 --gg residue,rigid,peptide --merge --p3max 5 > /dev/null && rm -f out/tmp/s1_L12_H_0.60_rows*.npz
tail -n 1 logs/s1_L12_H_0.60_rows0-240.log logs/s1_L12_H_0.60.log
