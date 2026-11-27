#!/bin/bash
# coordinator: workstream R6's second pass (run_pass2.sh: the same campaigns, numbers of runs, seeds and time limits) with the
# sampler guard lowered to n > 10^14.  Two streams of two processes.  Outputs in this scratch directory.
export OMP_NUM_THREADS=1
cd "$(dirname "$0")"
run() { timeout "$4" python3 campaign.py "$1" "$2" "$3" 2 > "logs/$1_$3.log" 2>&1; echo "pass3 $1 $3 exit $? ($(wc -l < data/$1_$3.jsonl) runs)" >> logs/progress.txt; }
( run A_ties 500 212 400; run A_medium 500 213 480; run D_2L 240 216 420 ) &
( run B_reducedK 400 214 360; run B_invalid 400 215 360; run B_lazy 260 220 300; run B_lazycheap 60 218 120; run D_2L_off 300 217 360 ) &
wait
echo ALLDONE_PASS3 >> logs/progress.txt
