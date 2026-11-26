#!/bin/bash
# slot B = three short runs (helix control Leu16, width decomposition, last sampler check), then ball parts 0, 1, 2 of 6
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cd "$(dirname "$0")"
python3 -B p6_02_sandwich.py L16 H 0.60 --m 4,5,6 > logs/p6_02_sandwich_L16_H_t0.60.log 2>&1
python3 -B p6_07_decompose.py V20 P2 0.70 5 8 > logs/p6_07_decompose_V20_P2_m5_w8.log 2>&1
python3 -B p6_07_decompose.py V20 P2 0.70 4 8 > logs/p6_07_decompose_V20_P2_m4_w8.log 2>&1
python3 -B p6_04_sampler.py V10 P2 0.70 5 B 9 --enumcheck --reps 60 --N 1200 > logs/p6_04_sampler_enum_V10_P2_m5_B_w9.log 2>&1
for i in 0 1 2; do python3 -B p6_03a_ball.py V50 E 0.70 3 --part $i --of 6 > logs/p6_03a_ball_V50_E_M3_part${i}of6.log 2>&1; done
echo "SLOT B DONE $(date)" > logs/v50_slotB.done
