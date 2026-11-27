#!/bin/bash
# workstream R6: second pass of the three adversarial searches in the cells with n_o >= 80 (corrected sampler).
# Starts when the second stream of run_pass2.sh has finished, so that at most four of my processes run at a time.
export OMP_NUM_THREADS=1
cd "$(dirname "$0")"
until grep -q "pass2 D_2L_off" logs/progress.txt; do sleep 5; done
( R6_ADV_SECONDS=210 python3 adversarial.py 0 ineq 400 231 > logs/adv2_0_ineq.log 2>&1; echo "adv2 0 ineq exit $?" >> logs/progress.txt ) &
( R6_ADV_SECONDS=210 python3 adversarial.py 2 calls 400 233 > logs/adv2_2_calls.log 2>&1; echo "adv2 2 calls exit $?" >> logs/progress.txt ) &
wait
R6_ADV_SECONDS=210 python3 adversarial.py 0 cap 400 234 > logs/adv2_0_cap.log 2>&1; echo "adv2 0 cap exit $?" >> logs/progress.txt
echo ALLDONE_ADV2 >> logs/progress.txt
