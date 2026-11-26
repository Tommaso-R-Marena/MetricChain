#!/usr/bin/env bash
# Runner for the kernel-evaluation experiment (see README.md).
#
#   ./run.sh file <path.lean> [timeout_s]      run ONE Lean file under the limits
#   ./run.sh size <ENC> <n> <k> [gen.py opts]  generate and run the positive file of one size
#   ./run.sh controls <ENC> <n> <k>            generate and run the negative controls and the
#                                              `decide` / `rfl` tactic variants of one size
#   ./run.sh ladder <ENC> <n,k> <n,k> ...      sizes in the given order, stop at the first failure
#   ./run.sh tactics <ENC> <n> <k>             only the `decide` / `rfl` variants of one size
#   ./run.sh all                               everything, in the order reported in README.md
#   ./run.sh clean-large                       delete generated files larger than 1 MB
#
# Exactly one `lean` process runs at a time.  Every run is
#
#   cd <repo>; ( ulimit -v $VLIMIT_KB; measure.py --rss-kill-kb $RSS_KILL_KB -- \
#                timeout $TLIMIT lean --profile <file> ) > logs/<name>.log 2>&1
#
# Limits (the machine is shared):
#   * VLIMIT_KB=12000000   `ulimit -v`.  NOT 6000000: lean 4.31 reserves 6 x 1 GiB of address
#                          space for thread stacks before it allocates anything (VmPeak 7.2 GB
#                          at 0.5 GB resident), so under `ulimit -v 6000000` it aborts with
#                          "failed to create thread".  12 GB of address space leaves about 5.3 GB
#                          for real allocations.
#   * RSS_KILL_KB=5000000  measure.py polls the resident set size and kills the run above 5 GB.
#   * TLIMIT=600           seconds (`timeout`); 120 for the `decide` / `rfl` variants.
#
# `/usr/bin/time` is not installed here; measure.py reports the same kernel accounting
# (wait4 `ru_maxrss`) plus a polled peak.  `--profile` only adds timing lines to the log.
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
REL="experiments/coordinator_checks/kernel_eval"
export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"

VLIMIT_KB="${VLIMIT_KB:-12000000}"
RSS_KILL_KB="${RSS_KILL_KB:-5000000}"
TLIMIT="${TLIMIT:-600}"
KEEP_LARGE="${KEEP_LARGE:-0}"     # 1: keep every generated file
LARGE_BYTES=1000000               # generated files above this size are deleted after their run
EPHEMERAL="${EPHEMERAL:-0}"       # 1 (set for side experiments): delete whatever the size
GEN="$REL/generated"
LOGS="$HERE/logs"
mkdir -p "$HERE/generated" "$LOGS"

# run_file <file relative to the repo root> [timeout]  ->  0 iff lean exited with status 0
run_file() {
  local f="$1" t="${2:-$TLIMIT}" name log status
  name="$(basename "$f" .lean)${LOGTAG:-}"
  log="$LOGS/$name.log"
  (
    cd "$REPO" || exit 99
    ulimit -v "$VLIMIT_KB"
    python3 "$HERE/measure.py" --rss-kill-kb "$RSS_KILL_KB" -- timeout "$t" lean --profile "$f"
  ) > "$log" 2>&1
  status=$?
  {
    echo "RUN file: $f"
    echo "RUN bytes: $(stat -c %s "$REPO/$f" 2>/dev/null)"
    echo "RUN sha256: $(sha256sum "$REPO/$f" 2>/dev/null | cut -d' ' -f1)"
    echo "RUN limits: ulimit -v $VLIMIT_KB kB, rss kill $RSS_KILL_KB kB, timeout $t s"
    echo "RUN lean: $(lean --version)"
    echo "RUN status: $status"
  } >> "$log"
  printf '%-34s status %-3s %s\n' "$name" "$status" \
    "$(grep -E 'MEASURE (wall_seconds|max_rss_kb|polled_peak_rss_kb)' "$log" | sed 's/MEASURE //' | tr '\n' ' ')"
  case "$f" in
    "$GEN"/*)
      if [ "$KEEP_LARGE" != 1 ] && { [ "$EPHEMERAL" = 1 ] ||
           [ "$(stat -c %s "$REPO/$f" 2>/dev/null || echo 0)" -gt "$LARGE_BYTES" ]; }; then
        rm -f "$REPO/$f"        # regenerable with gen.py (same bytes: compare RUN sha256)
        echo "RUN note: generated file deleted after the run (regenerable with gen.py)" >> "$log"
      fi ;;
  esac
  return $status
}

gen() { ( cd "$REPO" && python3 "$REL/gen.py" --out "$GEN" "$@" ) > /dev/null; }

run_size() {  # ENC n k [gen opts]
  local enc="$1" n="$2" k="$3"; shift 3
  local suffix=""
  local a prev=""
  for a in "$@"; do [ "$prev" = "--suffix" ] && suffix="$a"; prev="$a"; done
  gen --n "$n" --k "$k" --enc "$enc" "$@" || return 98
  run_file "$GEN/${enc}_n${n}_k${k}${suffix}.lean"
}

run_controls() {  # ENC n k
  local enc="$1" n="$2" k="$3" v
  gen --n "$n" --k "$k" --enc "$enc" --controls || return 98
  for v in negL negU negP negJ negJ0 negL_claimtrue; do
    run_file "$GEN/${enc}_n${n}_k${k}_${v}.lean"
  done
  for v in tac_decide tac_rfl; do
    run_file "$GEN/${enc}_n${n}_k${k}_${v}.lean" 120
  done
  return 0
}

run_tactics() {  # ENC n k : only the `decide` / `rfl` variants, 120 s each
  local enc="$1" n="$2" k="$3" v
  gen --n "$n" --k "$k" --enc "$enc" --tactic-variants || return 98
  for v in tac_decide tac_rfl; do
    run_file "$GEN/${enc}_n${n}_k${k}_${v}.lean" 120
  done
  return 0
}

run_ladder() {  # ENC "n,k" ...
  local enc="$1" nk; shift
  for nk in "$@"; do
    if ! run_size "$enc" "${nk%,*}" "${nk#*,}"; then
      echo "$enc: stopped after n=${nk%,*} k=${nk#*,} (failed, timed out or over the memory limit)"
      return 0
    fi
  done
}

case "${1:-}" in
  file)      shift; f="$(realpath --relative-to="$REPO" "$1")"; run_file "$f" "${2:-$TLIMIT}" ;;
  size)      shift; run_size "$@" ;;
  controls)  shift; run_controls "$@" ;;
  ladder)    shift; run_ladder "$@" ;;
  tactics)   shift; run_tactics "$@" ;;
  clean-large)
    find "$HERE/generated" -name '*.lean' -size +${LARGE_BYTES}c -print -delete ;;
  all)
    run_file "$REL/baseline_empty.lean"       # what `lean` itself costs
    # the limit that was asked for: lean cannot even start under it (see README.md)
    VLIMIT_KB=6000000 LOGTAG=_ulimit6000000 run_file "$REL/baseline_empty.lean"
    # negative controls and tactic variants at the smallest size (E3: at the extra tiny size)
    for enc in E1 E4 E2 E2h; do run_controls "$enc" 16 2; done
    run_controls E3 8 2
    # size ladders, one encoding after the other, each stopped at its first failure
    run_ladder E1  8,2 16,2 16,4 32,4 32,8 48,8
    run_ladder E4  8,2 16,2 16,4 32,4 32,8 48,8
    run_ladder E2  8,2 16,2 16,4 32,4 32,8 48,8
    run_ladder E2h 8,2 16,2 16,4 32,4 32,8 48,8
    run_ladder E3  8,2 16,2
    # side experiments (see README.md, "What failed, and what limits it"); their generated files
    # are deleted after the run
    EPHEMERAL=1
    run_size E2h 16 2 --chunk-fields 0 --suffix _oneliteral    # one numeral per table:
    run_size E2h 16 4 --chunk-fields 0 --suffix _oneliteral    #   elaboration time is quadratic
    run_size E2h 32 4 --chunk-fields 0 --suffix _oneliteral
    run_size E4 32 4 --list-chunk 0 --suffix _oneliteral       # one list literal per table
    run_size E4 32 8 --list-chunk 0 --suffix _oneliteral       #   (heartbeat limit)
    run_size E1 16 4 --plain-def --list-chunk 0 --suffix _plaindef   # code generator fails
    run_size E1 16 2 --plain-int-numerals --list-chunk 0 --suffix _plainnumerals  # `[-5, 3, …]`
    run_size E1 32 4 --messages random --suffix _randmsg       # nonzero messages
    run_size E4 32 4 --messages random --suffix _randmsg
    run_size E2h 32 4 --messages random --suffix _randmsg
    run_size E2 16 2 --messages random --suffix _randmsg
    run_size E3 8 2 --messages random --suffix _randmsg
    run_tactics E4 32 4                                        # `decide` / `rfl` at a larger size
    run_tactics E2 32 4
    run_size E1 32 8 --data-only --suffix _dataonly            # tables only, no theorem:
    run_size E4 48 8 --data-only --suffix _dataonly            #   the cost of parsing and
    run_size E2h 48 8 --data-only --suffix _dataonly           #   elaborating the tables
    EPHEMERAL=0
    run_file "$REL/pitfall_thunk_chain.lean" 120
    run_file "$REL/pitfall_thunk_forced.lean" 120
    run_file "$REL/pitfall_thunk_forced_single.lean" 120
    python3 "$HERE/collect.py"
    ;;
  *)
    sed -n '2,13p' "$0"; exit 2 ;;
esac
