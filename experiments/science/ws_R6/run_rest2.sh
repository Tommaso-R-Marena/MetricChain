#!/bin/bash
# workstream R6: remaining campaigns, sequential, 2 processes at a time, short time limits (machine shared and loaded).
export OMP_NUM_THREADS=1
cd "$(dirname "$0")"
run() { timeout "$4" python3 campaign.py "$1" "$2" "$3" 2 > "logs/$1_$3.log" 2>&1; echo "$1 $3 exit $? ($(wc -l < data/$1_$3.jsonl) runs)" >> logs/progress.txt; }
run B_invalid 400 15 420
run D_2L 240 16 420
run B_reducedK 400 14 420
run D_2L_off 300 17 420
timeout 420 python3 e2e.py 600 21 1 > logs/e2e_21_K1.log 2>&1; echo "e2e 21 K1 exit $?" >> logs/progress.txt
timeout 240 python3 e2e.py 400 22 16 > logs/e2e_22_K16.log 2>&1; echo "e2e 22 K16 exit $?" >> logs/progress.txt
( timeout 400 python3 adversarial.py 0 ineq 400 31 > logs/adv_0_ineq.log 2>&1 ) &
( timeout 400 python3 adversarial.py 4 cap 2000 32 > logs/adv_4_cap.log 2>&1 ) &
wait
( timeout 400 python3 adversarial.py 2 calls 400 33 > logs/adv_2_calls.log 2>&1 ) &
( timeout 400 python3 adversarial.py 0 cap 400 34 > logs/adv_0_cap.log 2>&1 ) &
wait
echo ALLDONE >> logs/progress.txt
