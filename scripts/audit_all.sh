#!/usr/bin/env bash
# MetricChain single-command audit:
#   1. lake build (all modules under proofs/)            — must succeed, no "sorry" warnings
#   0. self-test: planted violations must be detected by the checks below
#   2. forbidden-token scan of proofs/ (all files)        — no sorry / admit / axiom / native_decide ...
#   3. axiom audit (proofs/AxiomAudit.lean)               — only propext, Classical.choice, Quot.sound;
#      every module under proofs/ must be imported there
#   4. Python falsification harness (+ mutation tests of the harness) + separation benchmarks
#      + reference checker (conformance vectors, fuzz)
#   5. every Lean declaration cited in docs/*.md exists in proofs/
# Usage: scripts/audit_all.sh [--full]     (--full runs the long falsification pass)
set -uo pipefail
cd "$(dirname "$0")/.."
source scripts/lean_env.sh || exit 1
FULL=0; [ "${1:-}" = "--full" ] && FULL=1
fail() { echo "AUDIT FAILED: $*" >&2; exit 1; }

# Forbidden constructs.  `sorry` is forbidden as a substring (this also covers `sorryAx`), in every
# file including AxiomAudit.lean; `stop` is the debugging tactic that closes goals without proof.
FORBIDDEN='sorry|(^|[^A-Za-z_.])admit($|[^A-Za-z_])|native_decide|^[[:space:]]*(private |protected )?axiom[[:space:]]|implemented_by|^[[:space:]]*unsafe[[:space:]]|ofReduceBool|^[[:space:]]*stop([[:space:]]|$)'
# Lean's warning for an incomplete proof (the quoting style has changed between versions).
SORRY_WARNING='declaration uses .?sorry.?'

echo "== [0/4] audit self-test: planted violations must be detected =="
ST=$(mktemp -d)
printf 'example : (1 : Nat) = 2 := sorry\n' > "$ST/Planted.lean"
lean "$ST/Planted.lean" > "$ST/out" 2>&1
grep -qE "$SORRY_WARNING" "$ST/out" \
  || fail "self-test: the incomplete-proof warning of this Lean version is not recognised"
for planted in 'theorem t : 1 = 2 := sorry' '  exact sorryAx _' 'example : 1 = 2 := by admit' \
               'theorem t : 1 = 2 := by native_decide' 'axiom bad : 1 = 2' '  stop'; do
  printf '%s\n' "$planted" | grep -qE "$FORBIDDEN" || fail "self-test: token scan misses: $planted"
done
for harmless in 'theorem admits_nothing : True := trivial' '#print axioms MetricChain.verify_sound' \
                '  -- the proof stops here'; do
  printf '%s\n' "$harmless" | grep -qE "$FORBIDDEN" && fail "self-test: token scan flags: $harmless"
done
echo "ok"

echo "== [1/4] lake build =="
BUILD_LOG=$(mktemp)
if ! lake build >"$BUILD_LOG" 2>&1; then tail -n 40 "$BUILD_LOG"; fail "lake build"; fi
tail -n 1 "$BUILD_LOG"
if grep -qE "$SORRY_WARNING" "$BUILD_LOG"; then grep -nE "$SORRY_WARNING" "$BUILD_LOG" | head; fail "incomplete proof in build"; fi
if grep -q "^error" "$BUILD_LOG"; then grep -n "^error" "$BUILD_LOG" | head; fail "errors in build log"; fi

echo "== [2/4] forbidden tokens in proofs/ =="
if grep -rnE "$FORBIDDEN" proofs/ --include='*.lean'; then
  fail "forbidden token found"
fi
echo "none"
echo "   Lean files: $(find proofs -name '*.lean' | wc -l), lines: $(cat $(find proofs -name '*.lean') | wc -l)"

echo "== [3/4] axiom audit =="
# The automatic audit only sees what AxiomAudit.lean imports: every module must be imported.
MISSING=""
for f in $(find proofs -name '*.lean' ! -name 'AxiomAudit.lean' | sort); do
  m=$(echo "${f%.lean}" | tr '/' '.')
  grep -q "^import $m\$" proofs/AxiomAudit.lean || MISSING="$MISSING $m"
done
[ -z "$MISSING" ] || fail "modules not imported by proofs/AxiomAudit.lean:$MISSING"
AX_LOG=$(mktemp)
if ! lake env lean proofs/AxiomAudit.lean >"$AX_LOG" 2>&1; then tail -n 30 "$AX_LOG"; fail "AxiomAudit.lean did not compile"; fi
if grep -qE "$SORRY_WARNING" "$AX_LOG"; then grep -nE "$SORRY_WARNING" "$AX_LOG" | head; fail "incomplete proof in AxiomAudit.lean"; fi
grep "AXIOM AUDIT OK" "$AX_LOG" || { tail -n 20 "$AX_LOG"; fail "automatic axiom audit did not report OK"; }
python3 - "$AX_LOG" <<'PY' || exit 1
import re, sys
text = open(sys.argv[1]).read()
allowed = {"propext", "Classical.choice", "Quot.sound"}
entries = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text, flags=re.S)
clean = re.findall(r"'([^']+)' does not depend on any axioms", text)
bad = []
for name, axs in entries:
    used = {a.strip() for a in axs.replace("\n", " ").split(",") if a.strip()}
    if not used <= allowed:
        bad.append((name, sorted(used - allowed)))
print(f"   headline theorems checked: {len(entries) + len(clean)}")
if bad:
    print("AUDIT FAILED: non-standard axioms:", bad, file=sys.stderr)
    sys.exit(1)
if len(entries) + len(clean) == 0:
    print("AUDIT FAILED: no #print axioms output found", file=sys.stderr)
    sys.exit(1)
# Lean diagnostics look like `path:line:col: error: ...` or `error(lean.xyz): ...`; a plain
# substring test would trip on declaration names such as `boltzmannAvg_prune_error`.
if re.search(r":\d+:\d+: error|(^|\n)error[:(]", text):
    print("AUDIT FAILED: errors in AxiomAudit output", file=sys.stderr)
    sys.exit(1)
PY

echo "== [4/4] Python falsification harness and benchmarks =="
if [ "$FULL" = 1 ]; then
  python3 experiments/falsify_conjectures.py 2>/dev/null | tail -n 80 || fail "falsification harness"
else
  python3 experiments/falsify_conjectures.py --quick 2>/dev/null | tail -n 80 || fail "falsification harness"
fi
[ "${PIPESTATUS[0]}" = 0 ] || fail "falsification harness reported a misbehaving test"
if [ -f experiments/mutation_tests.py ]; then
  python3 experiments/mutation_tests.py 2>/dev/null | tail -n 1 || fail "mutation tests"
  [ "${PIPESTATUS[0]}" = 0 ] || fail "a mutation of the harness was not caught (or the mutation list is stale)"
fi
if [ -f experiments/separation_benchmarks.py ]; then
  python3 experiments/separation_benchmarks.py --quick >/dev/null 2>&1 || fail "separation benchmarks"
  echo "separation benchmarks: ok"
fi
if [ -f experiments/reference_checker.py ]; then
  python3 experiments/reference_checker.py --selftest --quick >/dev/null 2>&1 \
    || fail "reference checker: conformance vectors or soundness fuzz"
  echo "reference checker (conformance vectors + soundness fuzz): ok"
  CERT_TMP=$(mktemp -d)
  python3 experiments/reference_checker.py --dump "$CERT_TMP" >/dev/null 2>&1 \
    && diff -rq "$CERT_TMP" experiments/certs >/dev/null 2>&1 \
    || fail "experiments/certs/ is out of date (regenerate with reference_checker.py --dump experiments/certs)"
  echo "stored conformance vectors match the reference checker: ok"
fi
if [ -d docs ] && ls docs/*.md >/dev/null 2>&1; then
  python3 scripts/check_doc_refs.py || fail "docs cite Lean declarations that do not exist"
fi
echo
echo "AUDIT PASSED"
