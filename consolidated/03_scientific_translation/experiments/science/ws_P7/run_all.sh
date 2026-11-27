#!/bin/bash
# Workstream P7: re-run every script that produces cited numbers (no Lean), one process at a time, each under
# the memory poller (cap 3.5 GB anonymous).  Logs: logs/<script>.log, each ending with "DONE <script>", the
# poller's line and "exit 0".   usage: ./run_all.sh      (about 7 minutes on one core)
set -u
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
for s in p7_01_five p7_00_models p7_02_branch p7_02b_exact p7_03_triplet p7_03b_multi p7_04_survey p7_04b_tables p7_05_domains p7_06_check p7_08_synth p7_11_normalform; do
  date -u +"%H:%M:%S UTC  start $s"
  python3 -B run_capped.py 3500 1500 0 -- python3 -B $s.py > logs/$s.log 2> logs/$s.err
  echo "exit $?" >> logs/$s.log
done
date -u +"%H:%M:%S UTC  all done"
