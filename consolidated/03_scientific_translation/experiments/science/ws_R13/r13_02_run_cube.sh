#!/bin/bash
# R13: production runs of the own cube recursion (one process at a time, OMP_NUM_THREADS=1)
export OMP_NUM_THREADS=1
cd /home/user/MetricChain/experiments/science/ws_R13
for u in 0.5 1.0 2.0; do
  python3 r13_01_cube_recursion.py $u 60 1.01 out/cube_u${u}_k60_r1.01.json > out/cube_u${u}_k60_r1.01.log 2>&1
done
for u in 0.5 1.0 2.0; do
  python3 r13_01_cube_recursion.py $u 60 1.003 out/cube_u${u}_k60_r1.003.json > out/cube_u${u}_k60_r1.003.log 2>&1
done
echo ALL_DONE > out/cube_runs.done
