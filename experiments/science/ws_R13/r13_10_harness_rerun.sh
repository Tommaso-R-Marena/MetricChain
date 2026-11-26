#!/usr/bin/env bash
# R13 item 3 — RE-RUN (their code, unchanged, read-only export of the theory branch at 63e36f7) of the harness blocks
# named in THY-RES-0011: XI.21, XVIII.8, XXV.1, XXV.2, XXV.3, in full mode (the harness's default seed 20261124),
# bytecode off (-B), isolated mode (-I).  The harness writes no file (checked with grep before running).
# One command:  bash r13_10_harness_rerun.sh > out/harness_rerun.log 2>&1
set -u
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
EXP=/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_63e36f7
H="$EXP/experiments/falsify_conjectures.py"
sha256sum "$H"
date -u
for id in "XI.21 " "XVIII.8 " "XXV.1 " "XXV.2 " "XXV.3 "; do
  echo "### cmd: python3 -I -B $H --only \"$id\"   (full mode)"
  ( time timeout 1150 python3 -I -B "$H" --only "$id" ) 2>&1
  echo "exit $?"
done
date -u
echo "R13_10_DONE"
