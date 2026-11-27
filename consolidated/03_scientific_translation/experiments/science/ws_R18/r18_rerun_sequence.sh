#!/bin/bash
# R18: the re-run of the engineering division's two checks, their Python reference only, one chunk after the
# other in ONE process at a time.  Each chunk writes logs/<script>_<key>.log (+ .json, their --out file).
# A chunk whose log does not end with "R18-RUNNER done ... exit=0" is moved to not_cited/ by hand afterwards.
# usage: bash r18_rerun_sequence.sh <list of "script:job:key"> ...
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1
for item in "$@"; do
  IFS=: read script job key <<< "$item"
  log="logs/${script}_${key}.log"
  if [ -e "$log" ]; then echo "skip $item (log exists)"; continue; fi
  python3 -I -B r18_run_chunk.py "$script" "$job" "$key" > "$log" 2>&1
  tail -1 "$log" | cut -c1-200
done
echo "R18 sequence finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
