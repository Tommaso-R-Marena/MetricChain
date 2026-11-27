#!/bin/bash
cd "$(dirname "$0")"
: > b_direct_part2.out
python3 b_direct.py 12 3 400 7 97 hetero >> b_direct_part2.out 2>&1
for n in 13 14; do
  for seed in 0 1; do
    python3 b_direct.py $n 2 800 $seed >> b_direct_part2.out 2>&1
    python3 b_direct.py $n 3 500 $seed >> b_direct_part2.out 2>&1
  done
  python3 b_direct.py $n 2 500 7 97 hetero >> b_direct_part2.out 2>&1
  python3 b_direct.py $n 3 300 7 97 hetero >> b_direct_part2.out 2>&1
done
echo "=== power checks (theorem B makes no claim) ===" >> b_direct_part2.out
for n in 8 7 9 10 11; do
  for seed in 0 1; do
    python3 b_direct.py $n 2 800 $seed >> b_direct_part2.out 2>&1
    python3 b_direct.py $n 3 500 $seed >> b_direct_part2.out 2>&1
  done
  python3 b_direct.py $n 4 150 0 >> b_direct_part2.out 2>&1
done
python3 b_direct.py 13 4 120 0 >> b_direct_part2.out 2>&1
python3 b_direct.py 14 4 120 0 >> b_direct_part2.out 2>&1
echo DONE >> b_direct_part2.out
