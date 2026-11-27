#!/bin/bash
# long chains: exact constants of pair-additive residuals, lower bounds for GB (an_long.py)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
run() { python3 -B an_long.py "$@" 2>&1 | grep -v Warn | grep -v "cw ="; }
run K8 H 0.70; run K12 H 0.70; run K16 H 0.70; run K24 H 0.70
run S12 E 0.70; run S24 E 0.70; run S12 H 0.70; run S24 H 0.70
run L24 H 0.60; run L32 H 0.60
run LKSE:8 H 0.60; run LKSE:12 H 0.60; run LKSE:16 H 0.60
run K8 E 0.70; run K12 E 0.70; run K16 E 0.70
run LKSE:8 E 0.60; run LKSE:8 P2 0.60
run V16 E 0.70; run F16 H 0.60
