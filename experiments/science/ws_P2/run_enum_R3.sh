#!/bin/bash
# exact enumerations on the full staggered grid R3 (one-site threshold 0.60; 0.70 by restriction)
# usage: bash run_enum_R3.sh BB      (writes logs/enum_R3_<BB>.log)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
bb=$1
for res in S V F L K; do
  for n in 1 2 3 4 5 6 7 8 10 12 14 16; do
    out=$(python3 -B enum_fb.py ${res}${n} $bb --grid R3 --tau 0.60 --maxconf 1.1e6 2>&1 | grep -v Warn | grep -v "cw =")
    echo "$out"
    if echo "$out" | grep -q "too large"; then break; fi
  done
done
for n in 1 2 3 4 5 6 7; do
  out=$(python3 -B enum_fb.py LKSE:${n} $bb --grid R3 --tau 0.60 --maxconf 1.1e6 2>&1 | grep -v Warn | grep -v "cw =")
  echo "$out"
  if echo "$out" | grep -q "too large"; then break; fi
done
