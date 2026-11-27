#!/bin/bash
# P5 step 2 on the enumerated helix instances (needs the s1 JSON files).  Run times: 3 s, 25 s, 3 s, 24 s, ~5 min.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
for inst in "L6 H 0.60" "L8 H 0.60" "S4 H 0.70" "S5 H 0.70"; do python3 -B s2_signblind.py $inst 5 > /dev/null; done
python3 -B s2_signblind.py S6 H 0.70 5 --blk 3e7 > /dev/null
tail -n 1 logs/s2_*.log
