#!/bin/bash
# workstream R6: after run_rest2.sh has finished: Algorithm 2L with the theorem's constants (re-run with the fixed checker),
# and the lazy-oracle campaign with steep costs at a larger number of runs.
export OMP_NUM_THREADS=1
cd "$(dirname "$0")"
while ! grep -q ALLDONE logs/progress.txt; do sleep 5; done
rm -f data/D_2L_16.jsonl
timeout 420 python3 campaign.py D_2L 240 16 2 > logs/D_2L_16.log 2>&1; echo "D_2L 16 (rerun) exit $? ($(wc -l < data/D_2L_16.jsonl) runs)" >> logs/progress.txt
timeout 300 python3 campaign.py B_lazy 200 20 2 > logs/B_lazy_20.log 2>&1; echo "B_lazy 20 exit $? ($(wc -l < data/B_lazy_20.jsonl) runs)" >> logs/progress.txt
echo ALLDONE3 >> logs/progress.txt
