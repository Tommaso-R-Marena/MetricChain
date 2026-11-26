#!/usr/bin/env bash
# R12 item 7 (addition) — RE-RUN of the theory division's mutation tests for the harness groups XXIV and XI
# (their code, unchanged, from the read-only export at 9408e33).  The driver writes one scratch copy of the
# harness ("mutant.py") into a temporary directory; TMPDIR is pointed into this workstream's directory so that
# nothing is written anywhere else, and the scratch directory is removed afterwards.
# One command:  bash r12_07b_mutations.sh
set -u
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
HERE=/home/user/MetricChain/experiments/science/ws_R12
EXP=/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_9408e33
mkdir -p "$HERE/tmp_mutants"
export TMPDIR="$HERE/tmp_mutants"
sha256sum "$EXP/experiments/mutation_tests.py" "$EXP/experiments/falsify_conjectures.py"
for grp in XXIV XI; do
  echo "### cmd: python3 -I -B $EXP/experiments/mutation_tests.py $grp"
  ( time timeout 1100 python3 -I -B "$EXP/experiments/mutation_tests.py" "$grp" ) 2>&1
  echo "exit $?"
done
rm -rf "$HERE/tmp_mutants"
echo "R12_07B_DONE"
