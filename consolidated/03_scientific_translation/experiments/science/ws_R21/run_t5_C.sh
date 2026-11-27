#!/bin/bash
export OMP_NUM_THREADS=1
cd /home/user/MetricChain/experiments/science/ws_R21
for K in 2 3 4 5 6; do python3 -B t5_gap_scaling.py K4 $K 8 12 > logs/t5_K4_K${K}_run1.log 2>&1; done
for K in 2 3 4; do python3 -B t5_gap_scaling.py W5 $K 8 12 > logs/t5_W5_K${K}_run1.log 2>&1; done
for K in 2 3 4; do python3 -B t5_gap_scaling.py K5-e $K 8 12 > logs/t5_K5-e_K${K}_run1.log 2>&1; done
echo "DONE run_t5_C $(date -u +%Y-%m-%dT%H:%M:%SZ)" > logs/run_t5_C_done.txt
