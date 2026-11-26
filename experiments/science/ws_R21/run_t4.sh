#!/bin/bash
export OMP_NUM_THREADS=1
cd /home/user/MetricChain/experiments/science/ws_R21
for g in K4 W5; do for K in 1 2 3; do
  python3 -B t4_certificate.py $g $K 2104 3 > logs/t4_${g}_K${K}_run1.log 2>&1
done; done
echo "DONE run_t4 $(date -u +%Y-%m-%dT%H:%M:%SZ)" > logs/run_t4_done.txt
