#!/bin/bash
# R23: re-run of the audit's 15 scripts from a scratch copy, one at a time, and comparison with the stored outputs.
# Usage: bash rerun_audit_scripts.sh   (from ws_R23/)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
HERE="$(cd "$(dirname "$0")" && pwd)"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
LOG="$HERE/logs/rerun_audit_$STAMP.log"
OUT="$HERE/rerun_copy/out"
echo "R23 re-run of the audit scripts, started $(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$LOG"
nid=0; ndiff=0; nfail=0
run_one () {  # $1 script path, $2 stored output, $3 label
  local t0=$(date +%s.%N)
  timeout 1100 python3 -I -B "$1" > "$OUT/$3.txt" 2> "$OUT/$3.stderr"
  local rc=$?
  local t1=$(date +%s.%N)
  local secs=$(python3 -c "print(f'{$t1-$t0:.1f}')")
  if [ $rc -ne 0 ]; then nfail=$((nfail+1)); echo "$3: exit code $rc after $secs s (stderr: $(head -c 300 "$OUT/$3.stderr" | tr '\n' ' '))" >> "$LOG"; return; fi
  if cmp -s "$OUT/$3.txt" "$2"; then nid=$((nid+1)); echo "$3: exit 0, $secs s, output IDENTICAL to the stored one ($(wc -l < "$2") lines, sha256 $(sha256sum "$2" | cut -c1-16))" >> "$LOG"
  else ndiff=$((ndiff+1)); echo "$3: exit 0, $secs s, output DIFFERS from the stored one: $(diff "$OUT/$3.txt" "$2" | grep -c '^[<>]') differing lines" >> "$LOG"; diff "$OUT/$3.txt" "$2" | head -20 >> "$LOG"; fi
}
for k in 01_envelope_checks 02_sandwich_dependence 03_near_sharp_sites 04_second_order_known_part 05_numbers 06_misc; do
  run_one "$HERE/rerun_copy/AA1/aa1_$k.py" "$HERE/rerun_copy/stored/AA1/out_$k.txt" "AA1_$k"
done
run_one "$HERE/rerun_copy/tree/experiments/audit/AA1/aa1_07_lean_names.py" "$HERE/rerun_copy/stored/AA1/out_07_lean_names.txt" "AA1_07_lean_names"
for s in s1_tail_lemma_beyond_uniform s2_ratio_without_triangle s3_ferromagnetic_chain_harder_than_cube s4_recompute_quoted_numbers s5_two_letter_concavity_scan s6_degenerate_regimes s7_polynomial_factors s8_fibre_averages_with_interactions; do
  short=$(echo $s | cut -d_ -f1)
  run_one "$HERE/rerun_copy/AA2/$s.py" "$HERE/rerun_copy/stored/AA2/out_$short.txt" "AA2_$short"
done
echo "SUMMARY: identical $nid, differing $ndiff, failed $nfail, of 15" >> "$LOG"
echo "finished $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
echo "END rerun_audit_scripts" >> "$LOG"
cat "$LOG"
