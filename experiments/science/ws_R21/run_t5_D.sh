#!/bin/bash
export OMP_NUM_THREADS=1
cd /home/user/MetricChain/experiments/science/ws_R21
for K in 2 3 4; do python3 -B t5_gap_scaling.py K5 $K 8 12 > logs/t5_K5_K${K}_run1.log 2>&1; done
for K in 2 3; do python3 -B t5_gap_scaling.py W6 $K 6 12 > logs/t5_W6_K${K}_run1.log 2>&1; done
for K in 2 3; do python3 -B t5_gap_scaling.py K6 $K 6 12 > logs/t5_K6_K${K}_run1.log 2>&1; done
echo "DONE run_t5_D $(date -u +%Y-%m-%dT%H:%M:%SZ)" > logs/run_t5_D_done.txt
