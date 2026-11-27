#!/bin/bash
# workstream R6: second pass of every campaign that can contain blocks of more than 2^50 points, with the corrected sampler
# (r6lib.big_binomial: Poisson branch in the regime where numpy's binomial is biased).  Two streams of two processes.
export OMP_NUM_THREADS=1
cd "$(dirname "$0")"
run() { timeout "$4" python3 campaign.py "$1" "$2" "$3" 2 > "logs/$1_$3.log" 2>&1; echo "pass2 $1 $3 exit $? ($(wc -l < data/$1_$3.jsonl) runs)" >> logs/progress.txt; }
( run A_ties 500 212 400; run A_medium 500 213 480; run D_2L 240 216 420 ) &
( run B_reducedK 400 214 360; run B_invalid 400 215 360; run B_lazy 260 220 300; run B_lazycheap 60 218 120; run D_2L_off 300 217 360 ) &
wait
echo ALLDONE_PASS2 >> logs/progress.txt
