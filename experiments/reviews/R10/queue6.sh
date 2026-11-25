#!/bin/bash
ulimit -v 4000000
cd "$(dirname "$0")"
until grep -q "^t21_e0.05" ../out/queue.log; do sleep 10; done
run() {
  local name=$1; shift
  local t0=$(date +%s)
  timeout 590 "$@" > ../out/$name.txt 2>&1
  local rc=$?
  echo "$name: rc=$rc time=$(( $(date +%s) - t0 ))s  [$*]" >> ../out/queue.log
}
run t22_u03_multi python3 t22_u03_multi.py 0.0
