#!/bin/bash
cd "$(dirname "$0")"
: > b_direct.out
for n in 12 13 14; do
  for seed in 0 1 2; do
    python3 b_direct.py $n 2 1200 $seed >> b_direct.out 2>&1
    python3 b_direct.py $n 3 800 $seed >> b_direct.out 2>&1
  done
  python3 b_direct.py $n 4 400 0 >> b_direct.out 2>&1
  python3 b_direct.py $n 2 800 7 97 hetero >> b_direct.out 2>&1
  python3 b_direct.py $n 3 600 7 97 hetero >> b_direct.out 2>&1
done
echo "=== power checks ===" >> b_direct.out
for n in 8 9 10 11; do
  for seed in 0 1; do
    python3 b_direct.py $n 2 1200 $seed >> b_direct.out 2>&1
    python3 b_direct.py $n 3 1200 $seed >> b_direct.out 2>&1
    python3 b_direct.py $n 4 800 $seed >> b_direct.out 2>&1
  done
done
echo DONE >> b_direct.out
