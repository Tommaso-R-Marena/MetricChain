#!/bin/bash
cd "$(dirname "$0")"
( time timeout 590 python3 -B level2_all_orders_explicit.py 500 6 12 8 ) > rerun_explicit_500_6_12_8.log 2>&1
( time timeout 590 python3 -B level2_all_orders.py 13 10 ) > rerun_all_orders_13_10.log 2>&1
echo finished > rerun_done.txt
