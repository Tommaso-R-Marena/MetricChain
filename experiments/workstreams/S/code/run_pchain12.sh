#!/bin/bash
ulimit -v 2000000
cd "$(dirname "$0")/.."
for p in 0 1 2 3; do
  f=out/pchain_K12_part$p.txt
  if [ ! -s $f ]; then s=$(date +%s); code/pchain 12 $p 4 > $f.tmp && mv $f.tmp $f; e=$(date +%s); echo "K=12 part $p $(head -1 $f | cut -c1-80) time $((e-s))s" >> out/run_pchain12.log; fi
done
echo done >> out/run_pchain12.log
