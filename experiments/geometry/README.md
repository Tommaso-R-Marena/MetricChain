# experiments/geometry — Geometric Inference division

| file | what | arithmetic |
|---|---|---|
| `geomlib.py` | chain builders (floating point; exact over any field), quadric systems, modular rank, Tonelli square roots | — |
| `run_checks.py` | harness: 31 tests of the statements of `docs/geometry/ENSEMBLE_RIGIDITY.md` (`--quick`, `--only NAME`) | mixed |
| `mutation_checks.py` | 19 planted errors (`GEOM_MUT`), each must fail its test | — |
| `exact_conic_rank.py [Kmax]` | Theorem C(b): rank of the conic system at the sharp threshold, two bond geometries, with and without bond angles | exact (mod p; `ℚ` and `ℚ(√2)`) |
| `exact_jacobian_rank.py [Kmax]` | Theorem H: full column rank of the Jacobian of averaged squared distances (complete data; separation `K + 3`) | exact (mod p) |
| `exact_4d_extreme.py` | Theorem D(b): a rational 7-atom chain in `ℝ⁴` on no quadric cone | exact (rational) |
| `exact_nonlinear_threshold.py [n] [seed] [char]` | Theorem I: degree of the rank-≤3 locus for two states (`n = 10`: `7 = 1 + 1 + 5`; `n = 11, 12`: 2); **needs Singular** | exact (Gröbner basis over `ℚ` or `𝔽_p`) |
| `explore_below.py 7 8 9` | two states below the threshold: competing ensembles by a linear program over sampled points of `𝒫(z)` | floating point |
| `demix.py` | algorithm DEMIX with its certificate; demonstration table | floating point |
| `hierarchy_example.py` | Theorem E(d): a globally rigid 6-atom chain and a two-state ensemble with the same averaged data | floating point (residuals `10⁻¹⁵`) |
| `matroid_connectivity.py [n]` | Theorem J: algebraic matroids of distance patterns on the chain variety and of bars between two rigid bodies; connectivity via fundamental graphs | exact (mod p; weak-image argument) |
| `er_not_ur_instance.py A B` | two 7-atom chains that are second-moment rigid and not universally rigid (grid + local searches + 4D realisation) | floating point |
| `explore_er3.py seed trials` | inverse search producing such candidates | floating point |
| `torsion_sharpness.py` | exact kink cost on a rod against discrete chains; worst conformations for one torsion move (GEOMETRY-RES-0002) | floating point |
| `local_data_bounds.py` | Theorem K (`LOCAL_DATA_STABILITY.md`): the three bounds on instances | floating point |
| `local_data_stability.py` | table of `s_7` against `n` for helices and coils with the upper bounds | floating point |
| `third_moment.py` | Proposition 9.2: the 3-form of mean triple products and its contractions | floating point |
| `explore_jacobian.py` | exploration: generic Jacobian ranks (found the thresholds of Theorem H) | floating point |
| `explore_spurious.py K n…` | exploration: chains that are linear images of the stacked configuration (non-linear threshold, G1.21) | floating point |
| `explore_misc.py lp\|k3\|4d` | exploration: uniqueness at `K = 2, n = 9`; `K = 3`; four-dimensional chains | floating point |
| `explore_er2.py seed trials` | exploration: search for second-moment rigid, not universally rigid 7-atom chains (O-3) | floating point |
| `exact_hierarchy_witness.py` | Theorem E(d): exact rational witness (rigidity rank 12, indefinite stress matrix of rank 2, no conic); `--mutate` uses a neighbour with a semidefinite stress and must fail | exact (fractions) |
| `exact_general_position.py [Kmax]` | hypothesis of Theorem F′: every `3K + 1` consecutive stacked points affinely independent, with (CC) at `n₀(K)` | exact (mod p) |
| `review1/` | the internal referee's own scripts, logs and Lean checks (GEOMETRY-REV-0001), unmodified; see its README | — |

Requirements: Python 3 with `numpy`, `scipy` (the exact scripts need only the standard library
and `numpy` for the modular elimination).  Seeds are fixed; every script prints what it
checked and exits non-zero on failure.
