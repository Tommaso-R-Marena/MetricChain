#!/bin/bash
# usage: bash run_batch.sh LISTFILE LOG     (lines: SEQ BB TAU m [extra options])
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cd "$(dirname "$0")"
while read -r line; do
  [ -z "$line" ] && continue
  timeout 1150 python3 -B run_floor.py $line >> "$2" 2>&1 || echo "FAILED/TIMEOUT: $line" >> "$2"
done < "$1"
echo "BATCH DONE $1" >> "$2"
