#!/bin/sh
# R9 follow-up (b): RE-RUN OF THE THEORY DIVISION'S CODE — not my code, not a replication.
# Runs their two scripts t4_head_tail.py and t4_lattice_index.py unchanged from the read-only export of theory commit
# 24a3c27 (the second one executes their harness experiments/falsify_conjectures.py as a module), with the working
# directory inside ws_R9 and bytecode writing off, and compares the outputs byte by byte with the output files they
# published.  A log out/r9b_rerun_<script>.txt is written only if the script ended with exit status 0.
# usage: sh r9b_rerun_theirs.sh [path of the export]
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
E2=${1:-/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_24a3c27}
D=$E2/experiments/coordinator_checks/limit_shape_review
W=$HERE/out/tmp_r9b_rerun
rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 1
CMP=$W/compare.txt
: > "$CMP"
ok=1
for s in t4_head_tail t4_lattice_index; do
    t0=$(date +%s)
    PYTHONDONTWRITEBYTECODE=1 timeout 900 python3 -B "$D/$s.py" > "$W/$s.txt" 2> "$W/$s.err"
    st=$?
    t1=$(date +%s)
    if [ $st -eq 0 ]; then
        if cmp -s "$W/$s.txt" "$D/out_$s.txt"; then res="output identical (cmp) to their published out_$s.txt"; else res="output DIFFERS from their published out_$s.txt"; ok=0; fi
        mv "$W/$s.txt" "$HERE/out/r9b_rerun_$s.txt"
    else
        res="NOT COMPLETED"; ok=0
    fi
    echo "$s.py (their code, unchanged, from the export): exit status $st, $((t1 - t0)) s, stderr $(wc -c < "$W/$s.err") bytes; $res" >> "$CMP"
done
echo "files left in the working directory besides this log and the two stderr files: $(ls "$W" | grep -v -e compare.txt -e '\.err$' | wc -l)" >> "$CMP"
echo "__pycache__ directories in the export after the runs: $(find "$E2" -name __pycache__ | wc -l)" >> "$CMP"
if [ $ok -eq 1 ]; then mv "$CMP" "$HERE/out/r9b_rerun_compare.txt"; cd "$HERE"; rm -rf "$W"; echo "done: out/r9b_rerun_compare.txt"; else echo "NOT all runs completed and identical; see $W"; fi
