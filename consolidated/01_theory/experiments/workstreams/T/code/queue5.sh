#!/bin/bash
# after queue4: the case u = 0.3 (narrow barrier-top piece) at small positive accuracies
cd "$(dirname "$0")"
ulimit -v 4000000
run() { out="$1"; shift; echo "### $* -> $out"; t0=$SECONDS; timeout 595 python3 "$@" > "../out/$out" 2>&1; echo "exit $? after $((SECONDS-t0))s: $(tail -1 ../out/$out)"; }
run t13_multiblock_bJ1.5_u0.3.txt t13_multiblock.py 1.5 0.3 0.0001,0.0003,0.0006,0.001
run t04_table_bJ1.5_u0.3.txt t04_table.py 1.5 0.0 0.3 0.0,0.0001,0.0003,0.0006,0.001
echo "### queue5 done"
