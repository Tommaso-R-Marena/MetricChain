#!/bin/bash
# R28: sequential grid jobs (one process at a time); each python script caps itself at 3 GB.
cd /home/user/MetricChain/experiments/science/ws_R28
export OMP_NUM_THREADS=1
D=/home/user/MetricChain/experiments/science/ws_R28
timeout 600 python3 -B ff_grid.py L E 144 $D/grid_L_E_144.npz > $D/ff_grid_L_E_144_01.log 2>&1
timeout 600 python3 -B ff_grid.py L H 144 $D/win_L_H_mt_1deg.npz --window 270,305,140,195,1 > $D/ff_grid_L_H_win_mt_01.log 2>&1
timeout 600 python3 -B ff_grid.py L H 144 $D/win_L_H_tp_1deg.npz --window 170,205,50,100,1 > $D/ff_grid_L_H_win_tp_01.log 2>&1
timeout 600 python3 -B ff_grid.py L H 144 $D/win_L_H_rot_1deg.npz --window 170,310,50,190,10 > $D/ff_grid_L_H_win_rot_01.log 2>&1
echo "run_grids_02 done $(date -u +%FT%TZ)" > $D/run_grids_02.done
