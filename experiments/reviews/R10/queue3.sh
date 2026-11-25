#!/bin/bash
# referee R10: third queue; starts when the second queue has finished (one heavy process at a time)
ulimit -v 4000000
cd "$(dirname "$0")"
until grep -q "^t19_couplings" ../out/queue.log; do sleep 10; done
run() {
  local name=$1; shift
  local t0=$(date +%s)
  timeout 590 "$@" > ../out/$name.txt 2>&1
  local rc=$?
  echo "$name: rc=$rc time=$(( $(date +%s) - t0 ))s  [$*]" >> ../out/queue.log
}
run t07c_junction_grid python3 t07c_junction_grid.py
