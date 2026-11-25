#!/bin/bash
# workstream R6: all simulated-oracle campaigns (2 processes).  Outputs: data/*.jsonl, logs/*.log
export OMP_NUM_THREADS=1
cd "$(dirname "$0")"
mkdir -p logs data
run() { timeout 1500 python3 campaign.py "$1" "$2" "$3" 2 > "logs/$1_$3.log" 2>&1; echo "$1 $3 exit $?" >> logs/progress.txt; }
run A_small 1600 11
run A_ties 500 12
run A_medium 500 13
run B_reducedK 900 14
run B_invalid 700 15
run D_2L 400 16
run D_2L_off 500 17
echo ALLDONE >> logs/progress.txt
