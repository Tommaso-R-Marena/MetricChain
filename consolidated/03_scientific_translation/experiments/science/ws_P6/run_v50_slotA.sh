#!/bin/bash
# Val50 on the strand, order 4: slot A = in-band pair sums (closed form), then ball parts 3, 4, 5 of 6
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cd "$(dirname "$0")"
python3 -B p6_01_pairsums.py V50 E 0.70 4 --w 8 > logs/p6_01_pairsums_V50_E_m4_w8.log 2>&1
for i in 3 4 5; do python3 -B p6_03a_ball.py V50 E 0.70 3 --part $i --of 6 > logs/p6_03a_ball_V50_E_M3_part${i}of6.log 2>&1; done
echo "SLOT A DONE $(date)" > logs/v50_slotA.done
