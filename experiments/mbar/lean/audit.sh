#!/usr/bin/env bash
# Division 9 Lean audit: build, forbidden-token scan, axiom audit.  Usage: ./audit.sh
# Pins: lean-toolchain (leanprover/lean4:v4.31.0), lake-manifest.json (Mathlib fabf563a...).
# On a fresh clone run `lake exe cache get` here first (or link .lake/packages to an existing fetch).
set -uo pipefail
cd "$(dirname "$0")"
export PATH="$HOME/.elan/bin:$PATH"
mkdir -p logs
fail() { echo "AUDIT FAILED: $*" >&2; exit 1; }
FORBIDDEN='sorry|(^|[^A-Za-z_])admit($|[^A-Za-z_])|native_decide|\+native|bv_decide|ofReduceBool|^[[:space:]]*(private |protected )?axiom[[:space:]]|implemented_by|^[[:space:]]*unsafe[[:space:]]|(^|[^A-Za-z_.])stop($|[^A-Za-z_])|#guard_msgs|^[[:space:]]*example([[:space:]]|:|$)'
echo "== [1/3] forbidden-token scan =="
if grep -nE "$FORBIDDEN" MBAR.lean MBAR/*.lean; then fail "forbidden token"; fi
echo "none found"
echo "== [2/3] lake build =="
{ lean --version; lake build MBAR 2>&1 | grep -vE '^(✔|ℹ) \[[0-9]+/[0-9]+\] (Built|Replayed) (Mathlib|Batteries|Aesop|Qq|Plausible|ProofWidgets|ImportGraph|LeanSearchClient|Cli|Lean|Init|Std)'; echo "lake exit: ${PIPESTATUS[0]}"; } > logs/build.log
grep -q "lake exit: 0" logs/build.log || fail "build failed (see logs/build.log)"
if grep -qiE "declaration uses .?sorry.?|^error|^warning" logs/build.log; then fail "warnings or errors in build"; fi
tail -3 logs/build.log
echo "== [3/3] axiom audit =="
lake env lean MBAR/AxiomAudit.lean > logs/axioms.log 2>&1 || fail "axiom audit did not run"
BAD=$(grep -E "depends on axioms" logs/axioms.log | grep -vE "^\S+ depends on axioms: \[(propext|Classical\.choice|Quot\.sound)(, (propext|Classical\.choice|Quot\.sound))*\]$" || true)
[ -z "$BAD" ] || fail "non-standard axioms: $BAD"
N=$(grep -cE "depends on axioms|does not depend on any axioms" logs/axioms.log)
echo "$N declarations audited; only propext / Classical.choice / Quot.sound"
wc -l MBAR/*.lean | tail -1
echo "AUDIT PASSED"
