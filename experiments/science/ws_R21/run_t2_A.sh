#!/bin/bash
# K = 2 on all GGR graphs
export OMP_NUM_THREADS=1
cd /home/user/MetricChain/experiments/science/ws_R21
for g in W5 K5-e K5 W6 K33+e; do
  python3 -B t2_chimera_search.py $g 2 10 30 > logs/t2_${g}_K2_run1.log 2>&1
done
python3 -B t2_chimera_search.py K6 2 3 30 0 2102 2000 > logs/t2_K6_K2_run1.log 2>&1
echo "DONE run_t2_A $(date -u +%Y-%m-%dT%H:%M:%SZ)" > logs/run_t2_A_done.txt
