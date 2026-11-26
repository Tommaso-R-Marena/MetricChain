#!/usr/bin/env bash
# Workstream L3: compile each file on its own (never `lake build`), record exit codes and axioms.
# Usage: bash experiments/science/ws_L3/check_all.sh     (from /home/user/MetricChain)
export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"
cd /home/user/MetricChain || exit 1
D=/home/user/MetricChain/experiments/science/ws_L3
LOG=$D/check_log.txt
{
  echo "check_all.sh  $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
  echo "lean: $(lean --version)"
  echo "TheoremA.lean identical to the output of assemble.py: $(python3 - <<'PY'
import os
here = "/home/user/MetricChain/experiments/science/ws_L3"
comp = open(os.path.join(here, "Compensation.lean")).read()
body = comp[comp.index("/-! ## Part 1:"):comp.index("end ScienceL3")]
head = open(os.path.join(here, "parts", "TheoremA_head.txt")).read()
tail = open(os.path.join(here, "parts", "TheoremA_tail.txt")).read()
marker = "/-! # Parts 1–6: repeated verbatim from `Compensation.lean` -/\n\n"
print(open(os.path.join(here, "TheoremA.lean")).read() == head + marker + body + tail)
PY
)"
  for f in Compensation TheoremA A16Rearrangement ChainRuleCube; do
    echo
    echo "=== $f.lean  ($(wc -l < $D/$f.lean) lines, $(grep -c '^theorem ' $D/$f.lean) theorems)"
    echo "forbidden tokens (sorry/admit/native_decide/axiom declarations): $(grep -cE '\bsorry\b|\badmit\b|native_decide|^axiom ' $D/$f.lean)"
    start=$(date +%s)
    lake env lean $D/$f.lean > $D/scratch/$f.out 2>&1
    code=$?
    end=$(date +%s)
    echo "exit code: $code   ($((end-start)) s)"
    echo "errors: $(grep -c 'error' $D/scratch/$f.out)   warnings: $(grep -c 'warning' $D/scratch/$f.out)"
    echo "#print axioms lines: $(grep -c 'depends on axioms' $D/scratch/$f.out);  not equal to [propext, Classical.choice, Quot.sound]: $(grep 'depends on axioms' $D/scratch/$f.out | grep -vc 'depends on axioms: \[propext, Classical.choice, Quot.sound\]')"
    cat $D/scratch/$f.out
  done
} > $LOG 2>&1
grep -E '^===|exit code|errors:|axioms lines|forbidden|identical' $LOG
