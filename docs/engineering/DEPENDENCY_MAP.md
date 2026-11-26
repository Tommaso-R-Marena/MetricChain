# Dependency map: what each engineering result rests on

Every computational claim of the engineering branch is tied here to the exact mathematical
statements it uses, their epistemic status **at the pinned theory commit** (`d81eb8a` unless a
section names another), and the
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

## Algorithm 2L⁺ (ENG-RES-0008; `src/metricchain_eng/twolevel/`, `experiments/eng/twolevel/`)

Pinned to the text of `docs/workstreams/K_REPORT.md` at theory commit `63efc69` (statuses as
of that commit).

| engineering claim | rests on | status upstream | hypotheses the computation must meet | what connects program and statement |
|---|---|---|---|---|
| "the run evaluated is a run of Algorithm 2L⁺" | `K_REPORT.md` §2.2 (the algorithm), §2.1 (tables), errata m1, m10 of referee R8 | definition | parameters in the ranges of Theorem 11.56; ladder `x₀ = 2un_i > … > x_L`, `x_L ≤ b` (checked by `Params`) | (i) the mean run reproduces 324 + 18 published rows of the workstream; (ii) a literal, sampled implementation that shares only the tables stops at the same level with the same sample and the same number of evaluations; (iii) Python reference = C kernel on random instances |
| "no claim of the theorem is violated on the instances searched" | Theorem 11.56 (i)–(vi) — the statement **under test** | [P], refereed (R8: "proved") | mean runs: counts replaced by their means; inner procedures replaced by the behaviours "bottom" / "top" (valid brackets) | every claim is evaluated on every run by the kernel; a mutation (no Harper term) is detected |
| the number of evaluations `1 + max_j M_j + Σ_l calls_l C_l`, with `calls` from sliding maxima of the sample sizes | step 1 of the algorithm (a point moves to the next rung iff its bracket straddles the level and the tolerance) | definition; the closed form is an engineering derivation (module docstring of `meanrun.py`) | nested brackets; the same trivial-bracket offset for all outer points (product instances) | the literal implementation counts calls one by one and agrees |
| the inner cost `C_l` | Proposition 11.57(a) (= K0): the two-sample bracket and its sample size | [P], refereed | `η = min(½, tanh(x/4))`, `K = ⌈3(1+η)η⁻² ln(4/δ′)⌉`, `δ′ = δ/(4LM̄)` | the "plain bracket" column of the workstream's table is reproduced |
| "the worst case approaches the claimed exponent" | `K_REPORT.md` (3.1) (Theorem K2) | [P], refereed | the cell's own `φ` and finite ladder | `alg2l.claimed_exponent`; a fine ladder at the best `φ` gives `τ₂` to 3 % (test) |
| "for the outer loop, radial instances with ball level sets are the whole class up to partial shells" | Harper's vertex-isoperimetric theorem and nestedness of neighbourhoods of initial segments | [K] for Harper; **the reduction itself is an unrefereed engineering argument** (ENG-RES-0008 §5) | fixed inner behaviour; law of `W` only | none beyond the argument; consistent with the data (general profiles never beat monotone ones by more than `0.002·na`) |
| hinted lower bound and plain-bracket columns | Theorem 11.25(a) | [V] (one-shot form) | — | reproduce the workstream's columns to the digits printed |

## Off-lattice distance entropy and single-flip bounds (ENG-RES-0009)

| engineering claim | rests on | status upstream | connection |
|---|---|---|---|
| "`14d_j − 15 ≤ c_j ≤ 70(d_j + 3)` in all 36 cases" | Proposition 11.74 (statement under test) | [P], no separate referee | exact single-flip constants of X-002 |
| the distance entropy `σ(ρ)` | definition in THY-REQ-0008 item 5; the profile distance of `P_REPORT.md` Proposition 2 | [P] | enumeration of X-004, extended to 14 torsions; 13 torsions reproduce the published counts |

## Exact sampling and the literal runs repeated (ENG-RES-0013 §§1, 2, 4; `src/metricchain_eng/twolevel/sampling.py`)

| result | depends on | status of the dependency |
|---|---|---|
| X-006b: 585 000 literal runs without a failure; frequencies with `K` scaled down | Theorem 11.56 (statement under test); the exact sampler; oracle inner brackets | **[P; refereed R8; reviewed SCI-REV-0007]**; the sampler's exactness is a paper argument of ours (Poissonisation with collision thinning), tested against exact laws, **not reviewed by anyone**; one of its branches (means above `10⁹` at more than `2³¹` trials) still calls numpy |
| that X-006 was exposed and X-006b is not | the measurement of numpy's defect (`binomial_bias.py`) | measured here; first reported by the Scientific Discovery Division (SCI-REV-0007 §4) |
| the cost bound under an invalid inner behaviour | the abort rule before each inner call (erratum m1 of referee R8) | **[P]** |
| the lowered cap on stored runs | THY-RES-0004 §3 | **[P; unrefereed; reviewed with one gap closed in SCI-REV-0007 §2]** |

## `C_max` against the non-adaptive lower bound (ENG-RES-0013 §3; X-009)

| result | depends on | status of the dependency |
|---|---|---|
| the separation table and its crossovers | Theorem 11.56 (`C_max`); Theorem 11.45(b) (`LB_na`); the science division's definitions (`R6_REPORT.md` §7) | **[P]**; **[V given two finite sums]**; the two implementations are independent and agree in 72 numbers |

## Type classes (ENG-RES-0012; X-008)

| result | depends on | status of the dependency |
|---|---|---|
| exact `q*_ball` on `T_k` | the definitions of THY-REQ-0010; the distance of a ball's point to its complement in the class | the distance formula is ours, **[P]**, brute-forced on five small classes |
| comparison with the limits | the three limits quoted in THY-REQ-0010 | theirs, **[P]** (theory report §11.25, not read here) |

## Not yet connected (stated so that nobody assumes otherwise)

* The mean runs of X-005 say nothing about fluctuations of the counts; X-006 addresses the
  outer loop only and with oracle brackets, so the event (V1) of the proof of Theorem 11.56 —
  validity of real inner brackets — is tested by no engineering computation.
* Three nested levels and the extensive regime of §11.18 have not been computed here.
* No engineering result so far uses the certificate kernels (`verify`, `verifyITop`,
  `zverifyTop`, `verifyLTop`).  The correspondence between the Python reference checker and
  the Lean definitions is established upstream on 16 conformance vectors only; engineering
  item E-1 (ENG-RES-0004) is the plan to test it on generated inputs.
* Nothing computed here says anything about a physical system.  All chains are synthetic
  lattice models with a made-up energy (`#gauche`).
