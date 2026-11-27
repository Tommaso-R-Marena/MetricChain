#!/bin/bash
# P5: Leu30 on the helix (1.07e9 assignments) at order 6 with site penalties, as four runs of < 20 min each:
# the ball of radius 5 (174 437 evaluations of a 582-atom energy, about 19 min in all) in two checkpointed halves,
# their merge into the pipeline's cache, then workstream P3's pipeline (floor_p3copy.py), which reads the ball back.
# usage: ./run_floor_L30.sh [first part to run: 0 (default) or 1]
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
first=${1:-0}
for k in 0 1; do
  if [ $k -ge $first ]; then python3 -B ball_precompute.py L30 H 0.60 5 $k 2 > /dev/null; fi
done
python3 -B ball_precompute.py L30 H 0.60 5 merge 2 > /dev/null
python3 -B floor_p3copy.py L30 H 0.60 6 --siteres --N 20000 > logs/floor_L30_H_m6_siteres.log 2>&1
tail -n 1 logs/floor_L30_H_m6_siteres.log
