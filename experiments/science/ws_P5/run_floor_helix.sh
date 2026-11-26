#!/bin/bash
# P5: workstream P3's own pipeline (floor_p3copy.py = verbatim copy of ws_P3/run_floor.py) in a regime P3 did not run:
# Leu on the helix with the floor as a FUNCTION (site penalties), truncation orders 5 and 6.
# usage: ./run_floor_helix.sh SEQ m [extra options]      e.g.  ./run_floor_helix.sh L16 6 --N 20000
# log: logs/floor_<SEQ>_H_m<m>_siteres.log (complete when its last line is "[...s] -> out/floor_....json")
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
seq=$1; m=$2; shift; shift
python3 -B floor_p3copy.py $seq H 0.60 $m --siteres "$@" > logs/floor_${seq}_H_m${m}_siteres.log 2>&1
tail -n 1 logs/floor_${seq}_H_m${m}_siteres.log
