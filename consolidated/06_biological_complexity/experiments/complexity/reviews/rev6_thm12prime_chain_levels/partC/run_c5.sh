#!/bin/bash
cd "$(dirname "$0")"
timeout 580 python3 -B c5_random_search.py 11 520 8  > log_c5_s11.txt 2>&1 &
timeout 580 python3 -B c5_random_search.py 12 520 10 > log_c5_s12.txt 2>&1 &
timeout 580 python3 -B c5_random_search.py 13 520 12 > log_c5_s13.txt 2>&1 &
wait
echo finished > log_c5_done.txt
