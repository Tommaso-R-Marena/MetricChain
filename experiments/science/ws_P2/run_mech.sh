#!/bin/bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
run() { python3 -B an_mech.py "$@" 2>&1 | grep -v Warn | grep -v "cw ="; }
run fb_S5_E_R3_t0.60 0.70; run fb_S5_H_R3_t0.60 0.70; run fb_S5_H_R3_t0.60 0.60
run fb_L12_H_R3_t0.60 0.60; run fb_F8_H_R3_t0.60 0.60
run fb_K3_H_R3_t0.60 0.70; run fb_K3_H_R3_t0.60 0.60; run fb_K4_H_R3_t0.60 0.70
run fb_LKSEc4_H_R3_t0.60 0.60; run fb_LKSEc5_H_R3_t0.60 0.60
run fb_V8_E_R3_t0.60 0.70; run fb_K3_E_R3_t0.60 0.70
