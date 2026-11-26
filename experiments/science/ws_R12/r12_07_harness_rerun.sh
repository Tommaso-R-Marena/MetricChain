#!/usr/bin/env bash
# R12 item 7 — RE-RUN (their code, unchanged, read-only export of the theory branch at 9408e33) of the
# harness blocks named in THY-RES-0010: XI.19, XI.20, XXIV.6 ... XXIV.10, in full mode (400 trials/test,
# the harness's default seed 20261124), bytecode off, isolated mode.
# One command:  bash r12_07_harness_rerun.sh   (writes to standard output)
set -u
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
EXP=/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_9408e33
H="$EXP/experiments/falsify_conjectures.py"
sha256sum "$H"
for id in "XI.19 " "XI.20 " "XXIV.6 " "XXIV.7 " "XXIV.8 " "XXIV.9 " "XXIV.10 "; do
  echo "### cmd: python3 -I -B $H --only \"$id\"   (full mode)"
  ( time timeout 1100 python3 -I -B "$H" --only "$id" ) 2>&1
  echo "exit $?"
done
echo "R12_07_DONE"
