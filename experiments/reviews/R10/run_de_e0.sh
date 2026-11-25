#!/bin/bash
# sequential DE runs at e = 0 (bJ=1.5, B=0, u=1); each run under ten minutes
ulimit -v 4000000
cd "$(dirname "$0")"
for spec in "3 11 14 160" "4 12 12 200" "5 13 10 240" "3 21 14 160" "4 22 12 200"; do
  set -- $spec
  timeout 590 python3 t05_de.py 1.5 0 1 0 $1 $2 $3 $4 > ../out/t05_de_e0_k$1_seed$2.txt 2>&1
  tail -3 ../out/t05_de_e0_k$1_seed$2.txt
done
