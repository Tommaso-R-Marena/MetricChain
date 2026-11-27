#!/bin/bash
# referee R10: sequential queue (one heavy process at a time, each run under ten minutes)
ulimit -v 4000000
cd "$(dirname "$0")"
run() {  # name, command...
  local name=$1; shift
  local t0=$(date +%s)
  timeout 590 "$@" > ../out/$name.txt 2>&1
  local rc=$?
  echo "$name: rc=$rc time=$(( $(date +%s) - t0 ))s  [$*]" >> ../out/queue.log
}
run t06_branches python3 t06_branches.py
run t16_misc python3 t16_misc.py
run t07_junction python3 t07_junction.py
run t11_finite python3 t11_finite.py AB
run t15_smallcubes python3 t15_smallcubes.py
run t08_tables_53 python3 t08_tables.py 53
run t08_tables_65 python3 t08_tables.py 65
run t08_tables_67 python3 t08_tables.py 67
run t09_u03 python3 t09_u03.py 0.30
