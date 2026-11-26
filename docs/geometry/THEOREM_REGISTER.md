# Theorem register — Geometric Inference division

One row per statement.  Label: **V** machine-checked (declaration in
`proofs/Geometry/EnsembleRigidity.lean`, namespace `MetricChain.Geometry`), **P** paper proof,
**P-exact** paper proof with an exact computation (script), **K** known, **N** numerical, **C**
conjecture.  "Review": the internal adversarial review GEOMETRY-REV-0001 (a subagent of this
division — not an independent division) unless another division is named.  Novelty column:
see `PRIOR_ART.md`; "not found" is an absence in summary-level searches.

| id | statement (short) | where | label | evidence / script | review | novelty |
|---|---|---|---|---|---|---|
| G1.1 | stacking: `M(μ)` is the squared-distance matrix of the stacked configuration | `ENSEMBLE_RIGIDITY.md` Lemma 2.1 | V `stacked_sqdist` | test `stacking_identity` | REV-0001 | known |
| G1.2 | competing ensembles consist of linear images of `z`; `AᵀA ∈ 𝒫(z)` | Lemma 2.2 | P | — | REV-0001 | standard argument |
| G1.3 | without statewise constraints: collinear decomposition; `O(dK)`-orbit of mixtures | Prop. 3.1 | P | `obstruction_collinear`, `obstruction_rotation`, `bcc_example` | REV-0001 | known / elementary |
| G1.4 | one state: identifiable ⇔ no conic at infinity ⇔ not a midpoint | Theorem A | P; (iii)⇒(ii) V `sqdist_midpoint_of_conic` | `affine_flex_midpoint`, `four_atom_mixture` | REV-0001 | (ii)⇔(iii) known; (i) reinterpretation |
| G1.5 | mixture with only trivial quadrics is identifiable among all ensembles | Theorem B | P; core V `block_rigidity`, `block_coeff_nonneg` | `trivial_quadrics_only`, `demix_recovers` | REV-0001 | not found |
| G1.6 | exact criterion: unique barycentric representation of `I` on `𝒫(z)` | Theorem B′ | P | `explore_misc.py lp` (N) | REV-0001 | not found |
| G1.7 | identifiable mixtures span simplicial faces of `conv D(𝒞)` | Cor. 4.2 | P | — | REV-0001 | not found (relative: Tropp 2018) |
| G1.8 | freely jointed: (CC) generic iff `n − 1 ≥ (9K²+K+2)/2`, all `K` | Theorem C(a) | P | `conic_threshold_exact` (bonds only) | REV-0001 | not found |
| G1.9 | bond lengths + angles: (CC) generic iff `n ≥ ⌈(9K²+K+8)/4⌉`, `K ≤ 12`, two geometries | Theorem C(b) | P-exact | `exact_conic_rank.py 12` | REV-0001 | not found |
| G1.10 | same, every `K`, every homogeneous geometry, `n ≥ m₀(D_K − 1) + 2` | Theorem C(c), Lemma R | P | `lemma_R_reachability` | REV-0001 | not found |
| G1.11 | sharp threshold for every `K` and geometry | Theorem C(d) | C | G1.9; `conic_threshold_float` at 111° | — | — |
| G1.12 | DEMIX returns the ensemble under (CC) | Prop. 6.1 | P | `demix.py`, `demix_recovers`, `demix_refuses_below_threshold` | REV-0001 | not found |
| G1.13 | stress certificate for incomplete averaged data | Theorem F | P; core V `stress_certificate`, `stress_energy_eq`, `mixture_energy_eq` | — | REV-0001 | `K = 1` known; `K ≥ 2` not found |
| G1.14 | separation `3K + 1` suffices among all ensembles | Theorem F′ | P | `trilateration_band` | REV-0001 | application of trilateration |
| G1.15 | global `W₂² ≤ C‖ΔM‖` with explicit certificate `φ`; optimal exponent; (CC) ⇒ infinitesimal identifiability | Theorem G | P | `dual_certificate`, `quadratic_growth_local`, `infinitesimal_identifiability_under_CC`, `w2_exponent_is_sharp` | REV-0001 | not found |
| G1.16 | `𝒦 = 𝒮` when `|E₀| ≤ 9` (chains: `n ≤ 6`; freely jointed: `n ≤ 10`) | Theorem D(a) | P from K | `six_atoms_have_a_quadric_in_4d` | REV-0001 | freely jointed known; chain reading not found |
| G1.17 | `𝒦 ⊊ 𝒮` for chains with `n ≥ 7` | Theorem D(b) | P-exact | `exact_4d_extreme.py` | REV-0001 | not found |
| G1.18 | universal ⇒ ensemble ⇒ global rigidity; equivalence when `𝒦 = 𝒮`; strictness of the second | Theorem E | P; two steps V `secondMomentRigid_of_universal`, `globallyRigid_of_secondMomentRigid`; instance N | `hierarchy_example.py` | REV-0001 | not found |
| G1.19 | complete data: local identifiability within `K` states iff `n ≥ 2K + 3`, `2 ≤ K ≤ 8` | Theorem H(a) | P-exact | `exact_jacobian_rank.py 8` | REV-0001 | not found |
| G1.20 | separation `K + 3` locally identifies `K` states (`n ≥ (K²+3K+4)/2`), `K + 2` never; `K ≤ 8` | Theorem H(b) | P-exact | `exact_jacobian_rank.py 8`, `band_K_plus_2_never` | REV-0001 | not found |
| G1.21 | identifiable among all ensembles from `n = ⌊9K/2⌋ + 1` for `K ≥ 3` | §5.2, §5.5 | N (`K = 3`: `n = 14, 15`), C | `explore_misc.py k3` | — | — |
| G1.25 | two states: generic ensembles with `n ≥ 10` atoms are identifiable among all ensembles (only the two states are linear images of the stack, also over ℂ) | Theorem I | P-exact | `exact_nonlinear_threshold.py 10 0 0` (Gröbner basis over ℚ, Singular: degree `7 = 1 + 1 + 5`), four witnesses mod 32003; test `nonlinear_threshold_exact` | — (after REV-0001 was commissioned) | not found |
| G1.26 | two states: not identifiable among all ensembles at `n = 7, 8` (mixtures of 9–11 other chains with the same data); identifiable at `n = 9` in the instances computed | §5.5 | N (six instances each) | `explore_below.py 7 8 9`; test `two_states_below_threshold` | — | not found |
| G1.22 | second moment of randomly rotated labelled data determines exactly `M(μ)`; bond constraints lower the moment order | Cor. 9.1 | P given K (sample-complexity theorem not re-derived) | `second_moment_of_rotated_data` | REV-0001 | instance of a known principle |
| G1.23 | membership in the realizable set is NP-hard for general pair sets (star constraints) | §8.1 | K | — | — | known (E.-Nagy–Laurent–Varvitsiotis) |
| G1.24 | second-moment rigid conformations that are not universally rigid exist (`n = 7`) | §8.2 | N (two instances: unique 3D maximiser by grid `24⁴` + 2 000 local searches, indefinite stress, explicit 4D realisation); a certified optimum is requested (GEOMETRY-REQ-0006) | `explore_er3.py`, `er_not_ur_instance.py A B` | — | not found |
| G1.27 | laws of the distances of separations 3 and 4 determine every generic finite ensemble of chains (any `K`); a single separation never does | Theorem J | P, given the Ensemble division's E5/E6 (unrefereed) | `matroid_connectivity.py` (exact), test `matroid_patterns` | — | E5/E6 are the Ensemble division's; the chain statement is an application |
| G1.28 | exact small-angle Kabsch cost of one kink on a straight rod: `I_red φ² (1 − 3x(1−x))`; the coaxial cost of theory report Theorem 4.6 overestimates it by up to 4, the min-inertia bound by up to 8 (in cost); at the worst conformation (arms perpendicular to the axis, parallel) the verified constant is within `√2` | GEOMETRY-RES-0002 | P (rod model, small angle), N (discrete chains; worst conformations by optimisation) | `torsion_sharpness.py`, test `kink_formula` | — | free–free beam; elementary |
| G2.1 | any configuration, any pattern of sequence range `K`: `s_7(R)² ≤ (5π²/3)K(K+1)(2K+1)/n²`, so `C_inf ≥ n/(10K^{3/2})` | `LOCAL_DATA_STABILITY.md` Theorem K(a) | P | tests `local_data_bound_a` | — | known in substance (algebraic connectivity of banded graphs; `a_d ≤ a_1`) |
| G2.2 | torsion–distance duality: one torsion move changes the range-`K` distances by at most `2 sin(δ/2) b √T_K`, `T_K ≤ K⁴/48`; hence `C_glob ≥ κ_p(δ)/(b√T_K)` with `κ_p` the exact per-torsion superposition constant | Theorem K(b) | P | `local_data_bounds.py`, test `local_data_bound_b` | — | not found (elementary) |
| G2.3 | helices with all pairs of separation `≤ K`: `s_7 = c/n²`; the softest mode is torsional | Theorem K(c) | N | `local_data_stability.py`, test `helix_beam_law` | — | beam scaling known |
| G2.4 | long-range data are necessary for a length-independent constant: `K ≳ n^{2/3}` always, `n^{3/4}`–`n^{4/5}` on extended chains | Corollary K.1 | P from G2.1, G2.2; last clause N | — | — | — |

## Counts

Lean: 1 file, 11 declarations cited above (plus 6 definitions), zero warnings.
Harness: 30 tests (`run_checks.py`), 18 mutations (`mutation_checks.py`), all caught.
Exact computations: `exact_conic_rank.py` (96 witnesses for `K ≤ 12`), `exact_jacobian_rank.py`
(30 witnesses for `K ≤ 8`), `exact_4d_extreme.py` (1 witness), `exact_nonlinear_threshold.py`
(1 witness over ℚ, 4 modulo a prime; needs Singular).
