#!/bin/bash
# sequential queue (one heavy process at a time; every job under ten minutes; ulimit -v 4000000)
cd "$(dirname "$0")"
ulimit -v 4000000
run() { out="$1"; shift; echo "### $* -> $out"; t0=$SECONDS; timeout 595 python3 "$@" > "../out/$out" 2>&1; echo "exit $? after $((SECONDS-t0))s: $(tail -1 ../out/$out)"; }
run t10_sweep_J_u1_e0_a.txt t10_sweeps.py J 1.0 0.0 0.9,1.0,1.05,1.1,1.12,1.14
run t10_sweep_J_u1_e0_b.txt t10_sweeps.py J 1.0 0.0 1.16,1.2,1.3,1.4,1.5,1.75
run t10_sweep_U_bJ1.5_e0_a.txt t10_sweeps.py U 1.5 0.0 1.0,0.6,0.45,0.4
run t10_sweep_U_bJ1.5_e0_b.txt t10_sweeps.py U 1.5 0.0 0.35,0.3,0.25,0.2
run t14_finite3_S2_e0.05.txt t14_finite3.py 1.5 1.0 0.05 S2 0.318 150,300,600,1200
run t14_finite3_S3_e0.05.txt t14_finite3.py 1.5 1.0 0.05 S3 0.1553,0.2841 150,300,600
run t14_finite3_S4_e0.05.txt t14_finite3.py 1.5 1.0 0.05 S4 0.2104,0.2752,0.0662 150,300
run t06_finite_bJ1.5_u1_e0.05.txt t06_finite.py 1.5 0.0 1.0 0.05 1.0 0.318 0.318 150,300,600,1200
run t06_finite_bJ1.5_u1_eps1_shell_pu.txt t06_finite.py 1.5 0.0 1.0 0.0 1.0 0.2689 0.2689 250,500,1000,2000,4000
run t06_finite_bJ1.5_u1_X0.0251012.txt t06_finite.py 1.5 0.0 1.0 0.0251012 0.0 0.298 0.298 250,500,1000,2000,4000
run t06_finite_bJ1.5_u1_e0.01.txt t06_finite.py 1.5 0.0 1.0 0.01 0.0 0.2847 0.2847 250,500,1000,2000,4000
run t06_finite_bJ0.5_B0.3_e0.3E.txt t06_finite.py 0.5 0.3 1.0 0.029737 0.0 0.0 0.0 500,1000,2000,4000 0.4282
run t06_finite_bJ0.5_B0.3_X.txt t06_finite.py 0.5 0.3 1.0 0.041422 0.0 0.0 0.0 500,1000,2000,4000 0.4282
run t06_finite_field_p0.1_u2_H.txt t06_finite.py -99 0.1 2.0 0.0636884 0.0 0.0 0.0 500,1000,2000,4000 0.5373
run t06_finite_field_p0.1_u2_zero.txt t06_finite.py -99 0.1 2.0 0.0636884 0.0 0.0 0.0 500,1000,2000,4000 0.3994
run t06_finite_field_p0.1_u2_na.txt t06_finite.py -99 0.1 2.0 0.0636884 0.0 0.0 0.0 500,1000,2000,4000 0.517
run t11_instances_add.txt t11_instances.py 1.5 0.0 1.0 0.0 add
run t11_instances_flat.txt t11_instances.py 1.5 0.0 1.0 0.0 flat
run t11_instances_roof.txt t11_instances.py 1.5 0.0 1.0 0.0 roof
run t11_instances_rand.txt t11_instances.py 1.5 0.0 1.0 0.0 rand
run t02_convex_table_u1_a.txt t02_convex.py table 1.0 -2.0,-1.0
run t02_convex_table_u1_b.txt t02_convex.py table 1.0 0.0,0.5
run t02_convex_table_u1_c.txt t02_convex.py table 1.0 0.9,1.0
run t01_control.txt t01_control.py
run t12_crosscheck_bJ1.5_u1_e0.txt t12_crosscheck.py 1.5 0.0 1.0 0.0 1001
run t04_table_bJ1.5_u1_DE.txt t04_table.py 1.5 0.0 1.0 0.0,0.02 1
run t10_sweep_J_u1_e0.02.txt t10_sweeps.py J 1.0 0.02 1.0,1.1,1.2,1.3,1.5
run t03_blocks_bJ1.5_B0.05_u1_e0_k3.txt t03_blocks.py 1.5 0.05 1.0 0.0 3 3 60
run t03_blocks_bJ1.5_u0.3_e0_k3.txt t03_blocks.py 1.5 0.0 0.3 0.0 3 4 60
run t04_table_bJ1.5_B0.05_u1.txt t04_table.py 1.5 0.05 1.0 0.0,0.01,0.02
run t13_multiblock_bJ1.2_u1.txt t13_multiblock.py 1.2 1.0 0.0,0.02,0.04
run t13_multiblock_bJ2.0_u1.txt t13_multiblock.py 2.0 1.0 0.0,0.01,0.03
echo "### queue3 done"
