#!/bin/bash
# P5 step 1 on Leu6, Leu8 (helix, tau 0.60) and Ser4, Ser5 (helix, tau 0.70).  Run times: 2 s, 12 s, 6 s, 70 s.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
for inst in "L6 H 0.60" "L8 H 0.60" "S4 H 0.70" "S5 H 0.70"; do python3 -B s1_cancel.py $inst 5 > /dev/null; done
tail -n 1 logs/s1_L6_H_0.60.log logs/s1_L8_H_0.60.log logs/s1_S4_H_0.70.log logs/s1_S5_H_0.70.log
