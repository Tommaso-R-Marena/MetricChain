"""Mutation tests of run_checks.py: each planted error must make exactly the named test fail
(the unmutated test must pass, the mutant must run to its end without an exception, and the
harness itself must report the failure) -- the three conditions of the theory division's
mutation runner (docs/DEAD_ENDS.md D55 item 12, D57 item 1).

Usage: python3 mutation_checks.py
"""
import os
import subprocess
import sys

MUTATIONS = [
    ("stack_no_sqrt", "stacking_identity"),
    ("collinear_no_scale", "obstruction_collinear"),
    ("four_atom_weights", "four_atom_mixture"),
    ("midpoint_asymmetric", "affine_flex_midpoint"),
    ("threshold_minus_one", "conic_threshold_float"),
    ("drop_angle_edges", "conic_threshold_float"),
    ("demix_wrong_block", "demix_recovers"),
    ("band_K_plus_2", "jacobian_exact"),
    ("demix4_principal_only", "demix4_below_conic"),
    ("demix4_exact_ignore_structural", "demix4_exact_witness"),
    ("lemma_R_minus_one", "lemma_R_reachability"),
    ("profile_drop_angle_edges", "conic_rank_profile"),
    ("general_position_one_more", "general_position_exact"),
    ("hierarchy_semidefinite_neighbour", "hierarchy_exact_witness"),
    ("hinge_cc_from_two", "hinge_conic_dimensions"),
    ("hinge_wrong_mirror", "hinge_cube"),
    ("hinge_two_candidates", "hinge_candidates_exact"),
    ("halfturns_identifiable", "hinge_halfturns"),
    ("certificate_wrong_projector", "dual_certificate"),
    ("six_atoms_is_seven", "six_atoms_have_a_quadric_in_4d"),
    ("threshold_I_at_eleven", "nonlinear_threshold_exact"),
    ("below_claims_identifiable", "two_states_below_threshold"),
    ("single_separation_connected", "matroid_patterns"),
    ("kink_half", "kink_formula"),
    ("bound_a_too_strong", "local_data_bound_a"),
    ("bound_b_too_strong", "local_data_bound_b"),
    ("helix_exponent_one", "helix_beam_law"),
    ("tube_bound_too_strong", "tube_bound_helix"),
    ("procrustes_first_power", "local_procrustes_lemma"),
    ("theorem_L_without_S", "theorem_L0_instances"),
    ("procrustes_gram_constant", "procrustes_gram_lemma"),
    ("theorem_L_drop_sep4", "theorem_L_any_Y"),
    ("theorem_Lplus_first_order", "theorem_L_sharp_constant"),
    ("benchmark_second_solution_weights", "benchmark_suite_labels"),
    ("label_count_off_by_one", "label_patterns_linear"),
    ("label_quartic_one_fewer", "label_patterns_exact"),
    ("labels_rotation_not_orthogonal", "sparse_labels_second_solution"),
    ("affine_hull_separation_two", "chain_affine_hull"),
    ("third_moment_generic_rank", "third_moment_blocks"),
]


def run(test, mut):
    env = dict(os.environ)
    if mut:
        env["GEOM_MUT"] = mut
    else:
        env.pop("GEOM_MUT", None)
    here = os.path.dirname(os.path.abspath(__file__))
    r = subprocess.run([sys.executable, os.path.join(here, "run_checks.py"), "--quick", "--only", test],
                       capture_output=True, text=True, env=env, cwd=here)
    return r.returncode, r.stdout


def main():
    caught = 0
    baseline = {}
    for mut, test in MUTATIONS:
        if test not in baseline:
            code, out = run(test, "")
            baseline[test] = (code == 0 and "PASS" in out)
        code, out = run(test, mut)
        crashed = "EXCEPTION" in out
        ok = baseline[test] and code != 0 and "FAIL" in out and not crashed
        caught += ok
        print(f"{'caught' if ok else 'MISSED'}  {mut:30s} -> {test:36s} baseline {'passes' if baseline[test] else 'FAILS'}"
              f"{'; mutant crashed' if crashed else ''}")
    print(f"{caught} of {len(MUTATIONS)} mutations caught")
    return 0 if caught == len(MUTATIONS) else 1


if __name__ == "__main__":
    sys.exit(main())
