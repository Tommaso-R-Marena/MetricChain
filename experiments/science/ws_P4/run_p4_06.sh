#!/bin/bash
# P4 item 4: batch of p4_06_p3pair.py (P3's certified constants, re-run of P3's code; grids of P2).
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cd "$(dirname "$0")"
for spec in "V6 E 0.70 3" "V6 E 0.70 4" "S6 E 0.70 3" "S6 E 0.70 4" "S6 H 0.70 3" "L8 H 0.60 3" "K4 H 0.70 3" "F4 E 0.60 3" "V8 P2 0.70 3" "V8 P2 0.70 4" "S4 E 0.70 3"; do
  set -- $spec
  log=logs/p4_06_$1_$2_$3_m$4.log
  timeout 900 python3 -B p4_06_p3pair.py $1 $2 $3 $4 2 > $log 2>&1; echo "exit $?" >> $log
done
echo "DONE run_p4_06" > logs/p4_06_batch.done
