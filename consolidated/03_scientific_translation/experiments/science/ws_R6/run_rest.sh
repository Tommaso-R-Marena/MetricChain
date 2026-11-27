#!/bin/bash
# workstream R6: remaining simulated-oracle campaigns (2 processes), started after A_medium finishes.
export OMP_NUM_THREADS=1
cd "$(dirname "$0")"
while pgrep -f "campaign.py A_medium" > /dev/null; do sleep 5; done
echo "A_medium 13 ended (timeout or done)" >> logs/progress.txt
run() { timeout "$4" python3 campaign.py "$1" "$2" "$3" 2 > "logs/$1_$3.log" 2>&1; echo "$1 $3 exit $?" >> logs/progress.txt; }
run B_invalid 420 15 900
run D_2L 240 16 900
run B_reducedK 450 14 900
run D_2L_off 300 17 900
echo ALLDONE >> logs/progress.txt
