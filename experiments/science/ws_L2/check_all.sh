#!/usr/bin/env bash
# Workstream L2: check every Lean file on its own (one at a time), record output and exit codes.
# Usage:  bash experiments/science/ws_L2/check_all.sh     (from anywhere; never runs `lake build`)
export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"
cd /home/user/MetricChain || exit 1
DIR=/home/user/MetricChain/experiments/science/ws_L2
LOG=$DIR/check_log.txt
: > "$LOG"
for f in Sandwich Referee Window; do
  echo "=== lake env lean $DIR/$f.lean   (start $(date -u +%H:%M:%S) UTC)" >> "$LOG"
  lake env lean "$DIR/$f.lean" >> "$LOG" 2>&1
  echo "exit code: $?   (end $(date -u +%H:%M:%S) UTC)" >> "$LOG"
done
echo "=== forbidden tokens (sorry / admit / native_decide / axiom declarations), per file" >> "$LOG"
for f in Sandwich Referee Window; do
  echo "$f.lean: $(grep -c -w -E 'sorry|admit|native_decide' "$DIR/$f.lean") token(s); $(grep -c -E '^[[:space:]]*axiom ' "$DIR/$f.lean") axiom declaration(s); $(grep -c '^#print axioms' "$DIR/$f.lean") '#print axioms' line(s)" >> "$LOG"
done
echo "=== summary" >> "$LOG"
echo "axiom lines: $(grep -c 'depends on axioms' "$LOG"); of which exactly [propext, Classical.choice, Quot.sound]: $(grep -c 'depends on axioms: \[propext, Classical.choice, Quot.sound\]' "$LOG")" >> "$LOG"
echo "lines with 'error': $(grep -c 'error' "$LOG"); lines with 'warning': $(grep -c 'warning' "$LOG")" >> "$LOG"
