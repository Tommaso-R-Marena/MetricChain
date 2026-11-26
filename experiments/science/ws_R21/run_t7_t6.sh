#!/bin/bash
export OMP_NUM_THREADS=1
cd /home/user/MetricChain/experiments/science/ws_R21
python3 -B t7_fewer_means.py > logs/t7_fewer_means_run1.log 2>&1
python3 -B t6_e13_reading.py > logs/t6_e13_reading_run2.log 2>&1
for nb in 4 5 6 7 8 9 10 12; do
  python3 -B t6d_two_conformer_chains.py $nb 12 2000 > logs/t6d_chains_${nb}bonds_run1.log 2>&1
done
echo "DONE run_t7_t6 $(date -u +%Y-%m-%dT%H:%M:%SZ)" > logs/run_t7_t6_done.txt
