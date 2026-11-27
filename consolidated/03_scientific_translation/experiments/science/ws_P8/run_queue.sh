#!/bin/bash
# P8: run the commands of a list file one after the other (one process at a time per queue).
# usage: ./run_queue.sh LISTFILE     -- each line: arguments after "python3 -B"; '#' lines are skipped
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")"
while IFS= read -r line; do
  case "$line" in ''|'#'*) continue;; esac
  echo "[$(date -u +%H:%M:%S)] START python3 -B $line"
  python3 -B $line > /dev/null 2>&1
  echo "[$(date -u +%H:%M:%S)] END   (exit $?) $line"
done < "$1"
echo "[$(date -u +%H:%M:%S)] QUEUE DONE $1"
