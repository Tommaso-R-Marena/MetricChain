#!/bin/bash
# K = 3
export OMP_NUM_THREADS=1
cd /home/user/MetricChain/experiments/science/ws_R21
python3 -B t2_chimera_search.py W5 3 3 10 > logs/t2_W5_K3_run1.log 2>&1
python3 -B t2_chimera_search.py K5-e 3 2 10 > logs/t2_K5-e_K3_run1.log 2>&1
python3 -B t2_chimera_search.py K5 3 2 10 > logs/t2_K5_K3_run1.log 2>&1
python3 -B t2_chimera_search.py W6 3 2 10 > logs/t2_W6_K3_run1.log 2>&1
python3 -B t2_chimera_search.py K33+e 3 2 10 > logs/t2_K33+e_K3_run1.log 2>&1
echo "DONE run_t2_B $(date -u +%Y-%m-%dT%H:%M:%SZ)" > logs/run_t2_B_done.txt
