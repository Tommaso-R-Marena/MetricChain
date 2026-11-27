#!/bin/bash
# several seeds of t1_thm12prime.py; each run well below 10 minutes
cd "$(dirname "$0")"
for s in 1 2 3 4; do timeout 590 python3 t1_thm12prime.py 3000 $s 13 13 0 > log_t1_random_s$s.txt 2>&1; done
for s in 21 22 23 24; do timeout 590 python3 t1_thm12prime.py 3000 $s 14 14 1 > log_t1_targeted_s$s.txt 2>&1; done
echo finished > log_t1_done.txt
