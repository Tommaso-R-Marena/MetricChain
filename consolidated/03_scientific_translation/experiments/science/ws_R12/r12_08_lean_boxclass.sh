#!/usr/bin/env bash
# R12 — compile a COPY of the theory division's proofs/Frontiers/BoxClass.lean (9408e33) against OUR tree.
# Allowed by the brief because its only project import, proofs.Frontiers.QueryLowerBound, is byte-identical in
# our tree and in the export (checked with diff -q, see NOTES.md).  The copy is the file plus an appended block
# of `#print axioms` commands.  No `lake build`: `lake env lean` only.
# One command:  bash r12_08_lean_boxclass.sh
set -u
export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"
cd /home/user/MetricChain
EXP=/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_9408e33
diff -q proofs/Frontiers/QueryLowerBound.lean "$EXP/proofs/Frontiers/QueryLowerBound.lean" && echo "QueryLowerBound.lean: identical in our tree and in the export"
head -n 513 experiments/science/ws_R12/lean/BoxClass_copy_9408e33.lean | diff -q - "$EXP/proofs/Frontiers/BoxClass.lean" && echo "copy: first 513 lines identical to the export's BoxClass.lean"
( time timeout 1100 lake env lean experiments/science/ws_R12/lean/BoxClass_copy_9408e33.lean ) 2>&1
echo "lean exit status: $?"
echo "R12_08_DONE"
