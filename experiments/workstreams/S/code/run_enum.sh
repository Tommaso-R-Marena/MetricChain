#!/bin/bash
# one process at a time; each under ten minutes
ulimit -v 2000000
cd "$(dirname "$0")/.."
for N in 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22; do
  for m in walk bridge hsw; do
    f=out/${m}_N$N.txt
    if [ ! -s $f ]; then s=$(date +%s); code/enum $m $N > $f.tmp && mv $f.tmp $f; e=$(date +%s); echo "$m N=$N $(head -1 $f) time $((e-s))s" >> out/run_enum.log; fi
  done
done
for N in 23 24; do
  for m in bridge; do
    f=out/${m}_N$N.txt
    if [ ! -s $f ]; then s=$(date +%s); code/enum $m $N > $f.tmp && mv $f.tmp $f; e=$(date +%s); echo "$m N=$N $(head -1 $f) time $((e-s))s" >> out/run_enum.log; fi
  done
done
N=23; m=walk; f=out/${m}_N$N.txt
if [ ! -s $f ]; then s=$(date +%s); code/enum $m $N > $f.tmp && mv $f.tmp $f; e=$(date +%s); echo "$m N=$N $(head -1 $f) time $((e-s))s" >> out/run_enum.log; fi
echo done >> out/run_enum.log
