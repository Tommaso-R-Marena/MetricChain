#!/usr/bin/env bash
# Workstream L4: compile each file on its own (never `lake build`), record exit codes and axioms.
# Usage: bash experiments/science/ws_L4/check_all.sh     (from anywhere)
# One Lean process at a time.  Writes check_log.txt; raw compiler output in scratch/<File>.out.
export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"
cd /home/user/MetricChain || exit 1
D=/home/user/MetricChain/experiments/science/ws_L4
LOG=$D/check_log.txt
mkdir -p $D/scratch
{
  echo "check_all.sh  start $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
  echo "lean: $(lean --version)"
  echo "mathlib: $(grep -A3 '"name": "mathlib"' lake-manifest.json | grep -E '"rev"|"inputRev"' | tr -d ' \n')  $(git -C .lake/packages/mathlib rev-parse HEAD 2>/dev/null)"
  echo "RemainderIdentityTheory.lean identical to the output of assemble.py: $(python3 -B - <<'PY'
import importlib.util, os
here = "/home/user/MetricChain/experiments/science/ws_L4"
spec = importlib.util.spec_from_file_location("assemble", os.path.join(here, "assemble.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
print(open(os.path.join(here, "RemainderIdentityTheory.lean")).read() == mod.build())
PY
)"
  for f in RemainderIdentity RemainderIdentityTheory BennettTwoPoint; do
    echo
    echo "=== $f.lean  ($(wc -l < $D/$f.lean) lines, $(grep -c '^theorem ' $D/$f.lean) theorems, $(grep -cE '^(noncomputable )?def ' $D/$f.lean) definitions; sha256 $(sha256sum $D/$f.lean | cut -c1-16))"
    echo "imports: $(grep '^import ' $D/$f.lean | tr '\n' ' ')"
    echo "forbidden tokens (sorry/admit/native_decide/unsafe/implemented_by/axiom declarations): $(grep -cE '\bsorry\b|\badmit\b|native_decide|\bunsafe\b|implemented_by|^axiom ' $D/$f.lean)"
    start=$(date +%s)
    lake env lean $D/$f.lean > $D/scratch/$f.out 2>&1
    code=$?
    end=$(date +%s)
    echo "exit code: $code   ($((end-start)) s)"
    echo "errors: $(grep -c 'error' $D/scratch/$f.out)   warnings: $(grep -c 'warning' $D/scratch/$f.out)   output lines that are not '#print axioms' lines: $(grep -vc 'depends on axioms' $D/scratch/$f.out)"
    echo "#print axioms lines: $(grep -c 'depends on axioms' $D/scratch/$f.out) (commands in the file: $(grep -c '^#print axioms' $D/$f.lean));  with an axiom outside {propext, Classical.choice, Quot.sound}: $(grep 'depends on axioms' $D/scratch/$f.out | sed 's/.*depends on axioms: \[//; s/\]//' | tr ',' '\n' | sed 's/^ *//' | grep -vcE '^(propext|Classical\.choice|Quot\.sound)$');  exactly the three: $(grep -c 'depends on axioms: \[propext, Classical.choice, Quot.sound\]' $D/scratch/$f.out)"
    cat $D/scratch/$f.out
  done
  echo
  echo "check_all.sh  end $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
} > $LOG 2>&1
grep -E '^===|exit code|errors:|axioms lines|forbidden|identical|start|end ' $LOG
