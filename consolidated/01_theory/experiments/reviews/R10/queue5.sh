#!/bin/bash
ulimit -v 4000000
cd "$(dirname "$0")"
until grep -q "^t20_zero_field" ../out/queue.log; do sleep 10; done
run() {
  local name=$1; shift
  local t0=$(date +%s)
  timeout 590 "$@" > ../out/$name.txt 2>&1
  local rc=$?
  echo "$name: rc=$rc time=$(( $(date +%s) - t0 ))s  [$*]" >> ../out/queue.log
}
run t21_e0.05 python3 t21_e005.py 0.05
