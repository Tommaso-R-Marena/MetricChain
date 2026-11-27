#!/bin/bash
# usage: bash run_sampler.sh LISTFILE    (lines: arguments of p6_04_sampler.py); one log per run
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cd "$(dirname "$0")"
LIST="$1"
mkdir -p logs out
while read -r line; do
  [ -z "$line" ] && continue
  set -- $line
  mode="V"; case "$line" in *enumcheck*) mode="enum";; esac
  timeout 1150 python3 -B p6_04_sampler.py $line > "logs/p6_04_sampler_${mode}_$1_$2_m$4_$5_w$6.log" 2>&1 || echo "FAILED/TIMEOUT: $line" >> "logs/p6_04_sampler_${mode}_$1_$2_m$4_$5_w$6.log"
done < "$LIST"
echo "BATCH DONE $LIST $(date)" >> "logs/batch_$(basename "$LIST" .txt).done"
