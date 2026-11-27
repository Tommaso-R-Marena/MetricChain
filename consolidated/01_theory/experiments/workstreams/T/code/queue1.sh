#!/bin/bash
# sequential queue (one heavy process at a time; every job under ten minutes; ulimit -v 4000000)
cd "$(dirname "$0")"
ulimit -v 4000000
run() { out="$1"; shift; echo "### $* -> $out"; t0=$SECONDS; timeout 595 python3 "$@" > "../out/$out" 2>&1; echo "exit $? after $((SECONDS-t0))s: $(tail -1 ../out/$out)"; }
run t07_smallcubes_bJ1.5_u1.txt t07_smallcubes.py 1.5 0.0 1.0 bJ1.5_u1 3,4,5,6
run t08_families_bJ1.5_u1_n96.txt t08_families.py 1.5 0.0 1.0 bJ1.5_u1 96
run t08_families_bJ1.5_u1_n144.txt t08_families.py 1.5 0.0 1.0 bJ1.5_u1 144 12
run t03_blocks_bJ1.5_u1_e0_k4.txt t03_blocks.py 1.5 0.0 1.0 0.0 4 1 50
run t03_blocks_bJ1.5_u1_e0.02_k3.txt t03_blocks.py 1.5 0.0 1.0 0.02 3 2 60
run t10_sweep_J_u1_e0_a.txt t10_sweeps.py J 1.0 0.0 0.9,1.0,1.05,1.1,1.12,1.14
run t10_sweep_J_u1_e0_b.txt t10_sweeps.py J 1.0 0.0 1.16,1.2,1.3,1.4,1.5,1.75
run t10_sweep_U_bJ1.5_e0_a.txt t10_sweeps.py U 1.5 0.0 1.0,0.6,0.45,0.4
run t10_sweep_U_bJ1.5_e0_b.txt t10_sweeps.py U 1.5 0.0 0.35,0.3,0.25,0.2
echo "### queue1 done"
