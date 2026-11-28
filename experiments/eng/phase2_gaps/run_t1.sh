#!/usr/bin/env bash
# T1 driver: the twelve later certificates x three checkers, 20-minute limit per run (timeout is recorded, not extended).
#   bash experiments/eng/phase2_gaps/run_t1.sh <python> <sb-worktree> <tables-root>
# <tables-root>/tables_v2/*.npz and <tables-root>/tables_v2-lib/*.npz come from export_tables_v2.py.
# The three checkers run in parallel (one process each, one thread each); within a checker the runs are sequential.
set -u
PY=$1; SB=$2; TR=$3
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=$HERE/results/t1_runs.jsonl
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
run_checker() {
  local ck=$1
  for model in v2 v2-lib; do
    for id in 1CRN 5PTI 1BPI 1PGA 2IGD 1UBQ; do
      local line
      line=$(timeout 1200 "$PY" "$HERE/t1_check.py" --checker "$ck" --tables "$TR/tables_$model/$id.npz" \
             --cert "$SB/experiments/structbio/gmec_dev/certs/$model/$id.mincert.json" --sb "$SB" 2>"$TR/t1_${ck}_${model}_${id}.err")
      local rc=$?
      if [ $rc -eq 0 ]; then
        echo "{\"model\": \"$model\", \"pdb_id\": \"$id\", ${line#\{}"
      else
        echo "{\"model\": \"$model\", \"pdb_id\": \"$id\", \"checker\": \"$ck\", \"exit_code\": $rc, \"timeout\": $([ $rc -eq 124 ] && echo true || echo false)}"
      fi
    done
  done > "$HERE/results/t1_${ck}.jsonl"
}
run_checker files & run_checker indep & run_checker sb &
wait
cat "$HERE"/results/t1_files.jsonl "$HERE"/results/t1_indep.jsonl "$HERE"/results/t1_sb.jsonl > "$OUT"
