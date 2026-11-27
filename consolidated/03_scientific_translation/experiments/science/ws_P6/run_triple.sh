#!/bin/bash
# usage: bash run_triple.sh LISTFILE    (lines: arguments of p6_09_triple.py); one log per run
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cd "$(dirname "$0")"
LIST="$1"
while read -r line; do
  [ -z "$line" ] && continue
  set -- $line
  tag="$(echo "$1" | tr ':' 'c')_$2_t$3"
  timeout 1150 python3 -B p6_09_triple.py $line > "logs/p6_09_triple_${tag}.log" 2>&1 || echo "FAILED/TIMEOUT: $line" >> "logs/p6_09_triple_${tag}.log"
done < "$LIST"
echo "BATCH DONE $LIST $(date)" > "logs/$(basename "$LIST" .txt).done"
