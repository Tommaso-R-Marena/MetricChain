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
| `hinge_pairs.py [seed] [nstart]` | `HINGE_ENSEMBLES.md` Theorem M: two states that differ in two torsions — the cube of eight linear images of the stack, the parity relation, the linear programme, a search over all chains; `dim 𝒩(z)` for one to five hinges | floating point |
| `hinge_multistate.py [seed] [nstart]` | exploration: three states at two to four hinges (candidates by search, linear programme) | floating point |
| `exact_hinge_candidates.py` | Theorem M: the scheme of candidate assemblies has degree 8 (two hinges) and 2 (three hinges), reduced, over `ℚ` | exact (Singular) |
| `hinge_halfturns.py` | Theorem M (b)(iii), (d): identifiable iff at most one of `R_1`, `R_2`, `R_1R_2` is a half-turn (linear programme over the eight candidates) | floating point |
| `hinge_fourier_rank.py` | Lemma M1: the squared distances span `2s² + 1` functions of `s` hinge angles; products of non-adjacent hinges are not among them | floating point |
| `local_data_upper.py` | `LOCAL_DATA_STABILITY.md`: Lemma P; Theorem L for arbitrary competitors with every step of its proof (separations 4 to 7); Theorem L⁺ (sharp constant in its range); Proposition L₀ (the earlier form); Theorem K(c) (tube bound) | floating point |
| `local_data_guarantees.py` | the table of `LOCAL_DATA_STABILITY.md` §6: what Theorems L and L⁺ certify on idealised helix-like and strand-like traces (constants, certified range, first-order amplification) | floating point |
| `exact_demix4.py [--verify] [K n [geometry [seed]]]` | **Theorem I′**: at rational witnesses, modulo a prime below `2^16`, the `4 × 4` minors on the space `L` of the linear system have rank `C(m+3,4) − K` (`K = 2, n = 11`; `K = 3, n = 17`; `K = 4, n = 30`) or `C(m+3,4) − K − m` with the structural point (`K = 2, n = 10`; `K = 3, n = 16`); only lower bounds on ranks are used; `--verify` repeats the rank on the pivot rows in integer arithmetic at a second prime; `--mutate` runs two planted errors (the structural point ignored; principal minors only), neither of which may prove | exact (mod p); default run about 6 min, `4 30` about 27 min |
| `demix4.py` | Proposition 6.2 in floating point: the certificate `h_4 = K` and the recovery of states and weights below the conic threshold (the algorithm of Johnston–Lovitz–Vijayaraghavan applied to `L`); refuses at `K = 2, n = 10` | floating point |
| `minrank_prediction.py [Dmax [Kmax]]` | Hilbert function of the symmetric matrices of rank at most 3 (checked against the Harris–Tu degree), regularity, and the heuristic thresholds of the higher levels (§6.2) | exact integers; a heuristic, not a proof |
| `label_patterns.py` | `LABEL_PATTERNS.md`: only a subset of the points is observed — the linear certificate and DEMIX on 14 patterns (certified iff the number of labelled pairs at chain separation 1 or 2 is at least `(9K²+K+2)/2`); explicit second solutions for sparse labels (a rotation of the labelled stack, chains fitted to rounding); regularity ranks | floating point |
| `exact_label_patterns.py [--mutate]` | `LABEL_PATTERNS.md` Theorem P2 (d), (e) and Proposition P4: exact conic ranks on random label patterns and subsets (`K ≤ 3`), the one-state exception, the quartic certificate on patterns of two states | exact (mod p); under a second |
| `robust_demix.py [--table]` | `ROBUST_DEMIXING.md`: computable noise and tolerance bounds for demixing — the constants of a reference (`numbers`), Lemma N0 and Theorem N1 on arbitrary chains (`chain_report`), Theorem N2 (`theorem_N2`), the first-order constants and Theorem N3 (`first_order`, `theorem_N3`), the a-posteriori procedure (`reference`, `polish`, `a_posteriori`), the count of states (`count_states`), the tolerance family and its constant (`tolerance_constant`).  Without arguments: every inequality of every proof on competitors, about 2.5 minutes, ends with ALL OK; `--table`: the table of §8 |
| `distant_fits.py` | `LOCAL_DATA_STABILITY.md` §6 (i): configurations far from an idealised trace that fit its sequence-local distances — an independent replication of finding F1 of the Science division's review SCI-REV-0028 (local optimisation; upper bounds for the smallest error) |
| `stress_route.py` | `DEAD_ENDS.md` DG-26: the factor paid by a positive semidefinite stress of maximal rank on idealised traces, against the factor of Theorem L |
| `benchmark_instances.py [--write]` | `docs/geometry/BENCHMARKS.md`: 23 labelled synthetic instances in six classes (uniquely determined; not determined, with the second solution; determined only locally; no efficient certificate known; ill-conditioned; outside the assumptions); re-derives every label it can and fails otherwise; `--write` regenerates `benchmark_suite/*.json` and `MANIFEST.json` | floating point; about 1 min |
| `benchmark_suite/` | the pinned instances (JSON) and their SHA-256 manifest; checked by the harness test `benchmark_suite_labels` | data |
| `review1/` | the internal referee's own scripts, logs and Lean checks (GEOMETRY-REV-0001), unmodified; see its README | — |

Requirements: Python 3 with `numpy`, `scipy` (the exact scripts need only the standard library
and `numpy` for the modular elimination).  Seeds are fixed; every script prints what it
checked and exits non-zero on failure.
