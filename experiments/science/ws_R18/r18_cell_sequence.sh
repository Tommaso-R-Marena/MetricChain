#!/bin/bash
# R18: r18_cell.py on the six cells in which their searched bound exceeds their searched product worst case by more than 0.001 n a
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1
ulimit -v 2097152
for cell in "2 250 0.85" "2 350 0.85" "0.5 250 0.5" "0.5 350 0.5" "0.5 350 0.55" "0.5 500 0.35"; do
  set -- $cell
  log="logs/cell_v2_u$1_n$2_phi$3.log"
  if [ -e "$log" ]; then echo "skip $cell"; continue; fi
  python3 -I -B r18_cell.py $1 $2 $3 > "$log" 2>&1
  tail -1 "$log" | cut -c1-150
done
echo "cells finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
