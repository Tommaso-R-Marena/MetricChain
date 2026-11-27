#!/bin/bash
# referee R10: second queue (one heavy process at a time, each run under ten minutes)
ulimit -v 4000000
cd "$(dirname "$0")"
run() {
  local name=$1; shift
  local t0=$(date +%s)
  timeout 590 "$@" > ../out/$name.txt 2>&1
  local rc=$?
  echo "$name: rc=$rc time=$(( $(date +%s) - t0 ))s  [$*]" >> ../out/queue.log
}
run t07b_junction_scan python3 t07b_junction_scan.py
run t11_finite_A python3 t11_finite.py A
run t18_pair python3 t18_pair.py
run t04b_e0_seed5 python3 t04b_slp_alt.py 1.5 0 1 0 5 30 520
run t04b_e0.02_seed6 python3 t04b_slp_alt.py 1.5 0 1 0.02 6 30 520
run t04b_e0.05_seed7 python3 t04b_slp_alt.py 1.5 0 1 0.05 7 30 520
run t04b_e0.0015_seed8 python3 t04b_slp_alt.py 1.5 0 1 0.0015 8 30 520
run t12_convex_A012 python3 t12_convex.py A 7 0,1,2
run t12_convex_A34 python3 t12_convex.py A 7 3,4
run t12_convex_BCD python3 t12_convex.py BCD 7
run t17_convex_general_0 python3 t17_convex_general.py 0
run t17_convex_general_1 python3 t17_convex_general.py 1
run t17_convex_general_2 python3 t17_convex_general.py 2
run t13_T3b_u1 python3 t13_T3b_sets.py 1.0 50 1
run t13_T3b_u4 python3 t13_T3b_sets.py 4.0 50 2
run t04b_B0.05_e0 python3 t04b_slp_alt.py 1.5 0.05 1 0 9 30 520
run t04b_B0.05_e0.02 python3 t04b_slp_alt.py 1.5 0.05 1 0.02 10 30 520
run t19_couplings python3 t19_couplings.py
