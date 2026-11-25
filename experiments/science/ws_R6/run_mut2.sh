#!/bin/bash
# workstream R6: second pass of the five negative controls (corrected sampler), same seed 7.
export OMP_NUM_THREADS=1
cd "$(dirname "$0")"
run() { timeout 400 python3 campaign.py "MUT_$1" 48 7 2 > "logs/MUT_$1_7.log" 2>&1; echo "mut2 $1 exit $? ($(wc -l < data/MUT_$1_7.jsonl) runs)" >> logs/progress.txt; }
( run neg_tol; run noharper; run maxform ) &
( run close_at_no; run q_no_eta ) &
wait
echo ALLDONE_MUT2 >> logs/progress.txt
