#!/bin/bash
# Workstream F: all numerical checks, one after another (each python run is below ten minutes, memory cap 4 GB;
# about 45 minutes in total).  Outputs: out_*.txt.
cd "$(dirname "$0")"
ulimit -v 4000000
run() { out=$1; shift; echo "\$ $*" > "$out"; ( time "$@" ) >> "$out" 2>&1; echo "done $out"; }
run out_t01.txt python3 t01_basic.py
run out_t03.txt python3 t03_precise.py
run out_t04.txt python3 t04_na.py
run out_t05.txt python3 t05_birad_bruteforce.py
: > out_t08_finite_large.txt
for args in "0.1 2.0 0.3" "0.3 1.0 0.3" "0.05 2.0 0.1" "0.2 4.0 0.3"; do python3 t08_finite_large.py $args 1000,2000,4000 >> out_t08_finite_large.txt 2>&1; done; echo "done out_t08_finite_large.txt"
run out_t09.txt python3 t09_hamming_g0.py 0.1 2.0 0.3 500,1000,2000,4000,8000,16000,32000
run out_t09_64000.txt python3 t09_hamming_g0.py 0.1 2.0 0.3 64000
run out_t10.txt python3 t10_additive_large.py 0.1 2.0 0.3 1000,4000,16000 both
run out_t10_star_64000.txt python3 t10_additive_large.py 0.1 2.0 0.3 64000 star
run out_t11.txt python3 t11_pair.py
run out_t12_p0.1_u2.txt python3 t12_recursion.py 0.1 2.0 12
run out_t12_p0.3_u1.txt python3 t12_recursion.py 0.3 1.0 12
run out_t13.txt python3 t13_field.py
run out_t14.txt python3 t14_two_level_H.py 14 96
run out_t15.txt python3 t15_tail_lemma_ref.py
run out_t16.txt python3 t16_single_letter_sup.py
run out_t17.txt python3 t17_misc.py
run out_t18.txt python3 t18_exact_vs_family.py
run out_t19.txt python3 t19_field_monotone.py
run out_t20.txt python3 t20_product_samplers.py
run out_t21.txt python3 t21_checks.py
run out_field_table.txt python3 t22_field_table.py
echo '$ python3 t23_ctl_profile_sets.py 600 ; python3 t23_ctl_profile_sets.py 2000' > out_t23.txt
python3 t23_ctl_profile_sets.py 600 >> out_t23.txt 2>&1; python3 t23_ctl_profile_sets.py 2000 >> out_t23.txt 2>&1; echo "done out_t23.txt"
run out_t24.txt python3 t24_ctl_convergence.py 500,1000,2000,4000
echo ALL DONE
