#!/bin/bash
# first-order (per-site) certificates of the minimum on real instances (an_cover.py), domain X_tau
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
run() { python3 -B an_cover.py "$@" 2>&1 | grep -v Warn; }
for r in GB ff03-ff14SB; do
  run fb_S4_E_R3_t0.60 0.70 $r; run fb_S4_H_R3_t0.60 0.70 $r; run fb_K3_H_R3_t0.60 0.70 $r
  run fb_LKSEc4_H_R3_t0.60 0.60 $r; run fb_L12_H_R3_t0.60 0.60 $r; run fb_V8_E_R3_t0.60 0.70 $r
done
run fb_F8_H_R3_t0.60 0.60 GB; run fb_L14_H_R3_t0.60 0.60 GB; run fb_LKSEc5_H_R3_t0.60 0.60 GB
run fb_K3_H_R3_t0.60 0.60 GB; run fb_S5_H_R3_t0.60 0.70 GB
