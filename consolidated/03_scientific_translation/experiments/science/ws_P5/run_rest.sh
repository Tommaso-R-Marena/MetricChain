#!/bin/bash
# P5: the short runs, one after the other (about 10 min in all): step 1 on the four small instances, Proposition 11,
# the explicit family, step 2 on the five instances of orders 3-5.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
./run_s1_small.sh
python3 -B s4_refbound.py > /dev/null
python3 -B s2_family.py > /dev/null
./run_s2_all.sh
tail -n 1 logs/s4_refbound.log logs/s2_family.log
