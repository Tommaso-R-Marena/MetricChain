#!/bin/bash
ulimit -v 2000000
cd "$(dirname "$0")"
python3 g2_concat.py 8 4000 1 > ../out/g2_concat.txt 2>&1
python3 finite_packing.py 5000 > ../out/finite_packing_5000.txt 2>&1
echo done > ../out/run_misc.done
