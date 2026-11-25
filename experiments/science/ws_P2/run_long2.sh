#!/bin/bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
run() { python3 -B an_long.py "$@" 2>&1 | grep -v Warn | grep -v "cw ="; }
run S12 P2 0.70; run S24 P2 0.70; run K8 P2 0.70; run K12 P2 0.70; run L32 E 0.60; run L32 P2 0.60; run V24 E 0.70; run V24 P2 0.70; run LKSE:16 H 0.60
