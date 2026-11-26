#!/bin/bash
# usage: bash run_batch.sh LISTFILE     (lines: SEQ BB TAU --m ORDERS [--kind K] [--bands ...]); one log per run
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cd "$(dirname "$0")"
LIST="$1"
mkdir -p logs out
while read -r line; do
  [ -z "$line" ] && continue
  set -- $line
  tag="$(echo "$1" | tr ':' 'c')_$2_t$3"
  case "$line" in *obc2*) tag="${tag}_obc2";; esac
  timeout 1150 python3 -B p6_02_sandwich.py $line > "logs/p6_02_sandwich_${tag}.log" 2>&1 || echo "FAILED/TIMEOUT: $line" >> "logs/p6_02_sandwich_${tag}.log"
done < "$LIST"
echo "BATCH DONE $LIST $(date)" >> "logs/batch_$(basename "$LIST" .txt).done"
