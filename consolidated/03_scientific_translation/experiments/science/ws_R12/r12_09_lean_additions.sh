#!/usr/bin/env bash
# R12 — machine-check of the reviewer's own small additions (R12_REPORT §1: m1, m3, m5):
# experiments/science/ws_R12/lean/R12Additions.lean, which imports Mathlib only.  `lake env lean`, no build.
# One command:  bash r12_09_lean_additions.sh
set -u
export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"
cd /home/user/MetricChain
( time timeout 1100 lake env lean experiments/science/ws_R12/lean/R12Additions.lean ) 2>&1
echo "lean exit status: $?"
echo "R12_09_DONE"
