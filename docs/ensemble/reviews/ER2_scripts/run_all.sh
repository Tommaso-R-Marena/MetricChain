#!/bin/sh
# ER2: regenerate every output in out/ (about 35 minutes on one core; seeds fixed).
# Run from this directory.  Nothing is written outside out/.  The scripts c44_*.py and repo_f6_population.py
# import functions of experiments/ensemble read-only.
cd "$(dirname "$0")" || exit 1
mkdir -p out
run() { o="$1"; shift; ( "$@" ) > "out/$o" 2>&1; echo "[exit $?]" >> "out/$o"; }
run e13_polytope.txt                python3 -B e13_polytope.py
run e15_union_bound.txt             python3 -B e15_union_bound.py
run e15_local_search.txt            python3 -B e15_local_search.py
run e15t_interacting.txt            python3 -B e15t_interacting.py
run e15t_triangle_exact.txt         python3 -B e15t_triangle_exact.py
run e15t_association.txt            python3 -B e15t_association.py
run e15t_tree_parent.txt            python3 -B e15t_tree_parent.py
run e16_double_cone.txt             python3 -B e16_double_cone.py
run e17_noise.txt                   python3 -B e17_noise.py
run e22_e23_checks.txt              python3 -B e22_e23_checks.py
run e7p_platform.txt                python3 -B e7p_platform.py
run c44_validation_n10.txt          python3 -B c44_cutting_plane_validation.py 10 40 9 10 11 12 13 14
run c44_validation_n12.txt          python3 -B c44_cutting_plane_validation.py 12 30 11 12 13 14 15 16 17
run c44_validation_n14.txt          python3 -B c44_cutting_plane_validation.py 14 8 14 15 16 17 18
run c44_accept_margins.txt          python3 -B c44_accept_margins.py 12 40 11 12 13 14 15
run c44_full_lp_instancewise.txt    python3 -B c44_full_lp_instancewise.py
run c44_replicate_rows.txt          python3 -B c44_replicate_rows.py
run repo_f6_population.txt          python3 -B repo_f6_population.py
# the repository's own scripts, re-run unchanged (compare with experiments/ensemble/output.txt)
REPO="$(python3 -B -c 'import er2_common; print(er2_common.repo_root())')"
run rerun_finite_temperature_checks.txt python3 -B "$REPO/experiments/ensemble/finite_temperature_checks.py"
run rerun_platform_checks.txt           python3 -B "$REPO/experiments/ensemble/platform_checks.py"
# Lean (needs the compiled module proofs.Ensemble.ThermalUnionBound):
#   (cd "$REPO" && lake env lean docs/ensemble/reviews/ER2_scripts/ER2_lean_audit.lean) > out/lean_audit.txt
