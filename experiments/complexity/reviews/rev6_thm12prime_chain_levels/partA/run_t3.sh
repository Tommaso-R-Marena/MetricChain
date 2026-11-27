#!/bin/bash
cd "$(dirname "$0")"
for s in 1 2 3; do timeout 590 python3 t3_mutation.py 8000 $s 12 > log_t3_s$s.txt 2>&1; done
timeout 590 python3 t3_mutation.py 6000 4 13 > log_t3_s4.txt 2>&1
echo finished > log_t3_done.txt
