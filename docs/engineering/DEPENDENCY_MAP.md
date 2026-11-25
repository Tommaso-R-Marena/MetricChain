# Dependency map: what each engineering result rests on

Every computational claim of the engineering branch is tied here to the exact mathematical
statements it uses, their epistemic status **at the pinned theory commit `d81eb8a`**, and the
hypotheses of those statements that the computation has to satisfy.  Labels as in
`docs/collaboration/README.md` ([V] machine-checked, [P] paper proof, [K] cited, [N]
numerical, [C] conjecture; [X], [X\*], [R], [S], [E] for engineering results).

A theorem about a mathematical object is not a guarantee about a program.  The last column
says what connects the two in each case — or that nothing does yet.

## Chain covering (ENG-RES-0002; `src/metricchain_eng/chains/`, `experiments/eng/chain_cover/`)

| engineering claim | rests on | status upstream | hypotheses the computation must meet | what connects program and statement |
|---|---|---|---|---|
| "a set of evaluations certifies the minimum to accuracy ε iff slack balls of radius gap + ε cover the space" is the definition of the covering numbers computed | theory report Theorem 11.4; Lean `isCertificate_iff_cover` | [V] | envelope is a quasi-metric; known part and residual as in the theorem | the cover relation is evaluated in exact rational arithmetic (`cover_matrix_P`); unit test against a direct `Fraction` evaluation |
| the profile distance `L‖N^x − N^y‖₁` is an envelope of the pair-additive class | Lean `pairRes_sub_le` (`proofs/Frontiers/LinearClass.lean`); P_REPORT Proposition 2 | [V] inequality; [P] reviewed for "exact envelope" | residual pair-additive with `L`-Lipschitz radial functions in the squared distance, zero beyond the cutoff | `l1_matrix` computes the integral of the step-function difference; unit test integrates the step functions directly |
| the covering number is a set cover **on profile classes**, the binding member of a class being one with the fewest gauche torsions | elementary: the cover condition `d_P(a,y) ≤ gap(y) + ε` depends on `y` through `(profile, #gauche)` only, for known part `e·#gauche` and zero residual | engineering argument (two lines; stated in the module docstring) | zero residual; known part a function of `#gauche` alone | reproduces all 24 published covering numbers of P_REPORT §3.3 (obtained there on conformations, by a different implementation) |
| the enumerated objects are the chains of the workstream | P_REPORT §0 ("dia") | definition | tetrahedral angle, torsions 180°/±60°, self-avoidance, pairs with `q − p ≥ 3` | (i) class tables equal those of an independent internal-coordinate construction for `n ≤ 7` (`tests/eng/test_chains.py`); (ii) conformation and class counts equal the published sequences for `n = 5…13` |
| minimum covers are optimal | — | — | — | two independent solvers (HiGHS, CP-SAT) on an instance reduced by exact dominance rules; reductions and solvers checked against brute force on random instances; label **[X\*]** |
| chain-length independence at extensive accuracy (what the data are compared with) | theory report Proposition 11.49(a); P_REPORT Theorem 7 | [P], refereed (R6), reviewed (R_P); bound numerically vacuous | z-condition | none needed: the computation tests the *visibility* of the statement at finite size, not the statement |

## Generic chain (ENG-RES-0007; `src/metricchain_eng/chains/generic_chain.py`, `generic_analysis.py`)

| engineering claim | rests on | status upstream | hypotheses the computation must meet | what connects program and statement |
|---|---|---|---|---|
| the profile distance of two off-lattice conformations is the `ℓ¹` distance of their sorted truncated squared distances | P_REPORT Proposition 2 (one-dimensional Wasserstein distance) | [P], reviewed | same number of pairs of each type (fixed sequence) | unit test: the sorted-vector formula equals the integral of `|N^x − N^y|` on random pairs of classes |
| covers on classes with radii `gmin + ε` | as for the lattice chain | engineering argument | zero residual; known part a function of `#gauche` | 16 published covering numbers reproduced |
| the cover relation is decided correctly in floating point | — | — | — | tie analysis: no comparison within `2.9·10⁻⁸` of equality except five exact ties at `n = 11` (reported, counted as covered); rounding error of a distance ≈ `10⁻¹³`; label **[X\*]** |

## Uniform-cube hitting numbers (ENG-RES-0006; `experiments/eng/fc_uniform_cube/`)

| engineering claim | rests on | status upstream | hypotheses | connection |
|---|---|---|---|---|
| `FC_n(ε) = 2ⁿ / min{|D| : D sensitive}` on the uniform cube | theory report Theorem 11.22; vertex-transitivity | [V] for the lower-bound mechanism (`expected_queries_ge_packing`); the reduction to the uniform sampler is the standard symmetrisation | uniform measure, Hamming slack, zero residual | — |
| the largest non-sensitive complement of size `M` is a simplicial initial segment | Harper's vertex-isoperimetric theorem | [K] | — | brute force over all subsets for `n ≤ 4` (72 parameter cases): **[X]** there, [K] beyond |

## Audit replication (ENG-RES-0005)

| engineering claim | rests on | connection |
|---|---|---|
| "the verified state of `d81eb8a` is reproducible on an independent machine" | `scripts/audit_all.sh` at `d81eb8a`, unmodified | the script's own exit status and counts; the harness under three further seeds on a third platform; byte comparison of benchmark output |

## Not yet connected (stated so that nobody assumes otherwise)

* No engineering result so far uses the certificate kernels (`verify`, `verifyITop`,
  `zverifyTop`, `verifyLTop`).  The correspondence between the Python reference checker and
  the Lean definitions is established upstream on 16 conformance vectors only; engineering
  item E-1 (ENG-RES-0004) is the plan to test it on generated inputs.
* Nothing computed here says anything about a physical system.  All chains are synthetic
  lattice models with a made-up energy (`#gauche`).
