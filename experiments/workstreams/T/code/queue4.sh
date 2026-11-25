#!/bin/bash
# final sequential queue (after queue3): re-runs with the extended binary search, and the remaining multi-block points
cd "$(dirname "$0")"
ulimit -v 4000000
run() { out="$1"; shift; echo "### $* -> $out"; t0=$SECONDS; timeout 595 python3 "$@" > "../out/$out" 2>&1; echo "exit $? after $((SECONDS-t0))s: $(tail -1 ../out/$out)"; }
run t10_sweep_U_bJ1.5_e0_c.txt t10_sweeps.py U 1.5 0.0 0.3,0.27,0.25,0.2
run t13_multiblock_bJ1.5_u1_c.txt t13_multiblock.py 1.5 1.0 0.02,0.04
run t10_sweep_U_bJ1.5_e0.2_a.txt t10_sweeps.py U 1.5 0.2 1.0,0.45,0.3,0.25
echo "### queue4 done"
