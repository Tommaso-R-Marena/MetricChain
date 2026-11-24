# L2 prior-art check: relaxations on the torus, verified arithmetic, free-energy sandwich, decomposition bounds, certified integration

Literature check performed on 2026-11-24 for the MetricChain program (internal coordinates = torsion torus `T^M` plus discrete basin labels; `E = E_0 + Delta`, with `E_0` a tractable tree/chain-structured reference and `Delta` a black-box, non-decomposable residual). Covers candidate claims C6, C7 and C8.

## Reading guide

- **Verdicts.** `KNOWN` (a citation states it), `KNOWN-IN-SPIRIT / FOLKLORE` (an immediate corollary or a routine combination of cited results, or stated in a neighbouring field), `NO MATCH FOUND` (the listed searches did not surface it; this is not a proof of novelty).
- **Evidence tags.** `[V]` = checked online in this session (publisher / arXiv / repository record, abstract, or full text). A quoted theorem number or formula was read in the paper itself (full text, abstract or introduction) unless the entry says it is quoted via a survey or a search summary. `[unverified-from-memory]` = recalled but not confirmed online in this session; treat as a lead, not as a citation.
- **Baseline.** Each topic is compared against the strongest contemporary work found (2015-2026), not only the classical baselines named in the brief.
- **Lean ecosystem.** Statements about Lean 4 libraries reflect READMEs, Reservoir pages, generated docs and Zulip archives as fetched on 2026-11-24. These projects change monthly; re-check before relying on any detail.
- **Own derivations.** A few short arguments are mine (marked "reviewer's derivation"). They are there to show why a claim is or is not a corollary of the cited literature, and they have not been refereed.

## 0. Verdicts at a glance

| Item | Short statement | Verdict | Confidence |
|---|---|---|---|
| C6(a) | State of the art for convex underestimators, convergence order, cluster problem | KNOWN (mature field; torsion-space deterministic global optimization dates to 1994-2005) | High |
| C6(b) | SOS / moment hierarchies for trigonometric polynomials; exact certificates | KNOWN (rates: Bach-Rudi 2023; exact certificates: univariate only). Gaps with NO MATCH: multivariate exact rational certificates on `T^M` with bit bounds; rates for chain-sparse trigonometric hierarchies | High / Medium |
| C6(c) | Torus as the variety `prod {c_i^2+s_i^2=1}`; kinematics, distances, 12-6 LJ rational; exact rational certificate checking | Every ingredient KNOWN; the assembled molecular-energy pipeline with exact certificates: NO MATCH FOUND | Medium |
| C6(d) | Formally verified interval arithmetic / global optimization; what Lean 4 has | KNOWN (Coq, HOL Light, PVS; in Lean 4: girving/interval, LeanCert, leanprover/sos and others) | High, but fast-moving |
| C7, sandwich, product reference | Jensen lower bound + bounded-differences MGF upper bound | KNOWN-IN-SPIRIT (one-line corollary of textbook results; the same inequality is used for model-bias UQ; not found stated as a free-energy-perturbation bound) | High |
| C7, dependent references | `K = (1-theta)^-2`-type constants | KNOWN | High |
| C7, sharpness | Worst case over the bounded-difference class is additive and two-level | KNOWN-IN-SPIRIT (Rio 2013, Lemma 4.1 gives the exact extremal function; attainment is implicit; no explicit statement found) | Medium-High |
| C7, Bobkov-Gotze | Uniform sub-Gaussian bound for Lipschitz residuals iff T1 | KNOWN | High |
| C8(a) | Holder / TRW bounds; "temperature-rescaling" form | KNOWN (it is Holder's inequality; weights are explicitly called temperatures in the weighted mini-bucket literature) | High |
| C8(b) | Do K*, BBK*, MARK* bound the voxel integral? | They do not (KNOWN; verified for MARK*). Rigorous voxel-integral bounds in provable protein design: NO MATCH FOUND | Medium-High |
| C8(c) | Non-asymptotic Laplace bounds; certified quadrature with Hessian envelopes | Laplace bounds KNOWN. Gaussian/erf-envelope quadrature of `exp(-beta E)`: FOLKLORE ingredients, no direct match | Medium |
| C8(d) | Complexity lower bounds | KNOWN (Bakhvalov 1959; Hinrichs et al. 2014; Holzmuller-Bach 2025 specifically for log-partition) | High |
| C8(e) | Stopping rules for ranking partition functions; best-arm identification; instance-optimal refinement | KNOWN-IN-SPIRIT (BBK*, marginal MAP, explorable uncertainty, input-thrifty algorithms, NRA instance optimality). A competitive-ratio theorem for partition-function ranking: NO MATCH FOUND | Medium |

---

## C6. Relaxations on the torus and verified arithmetic

### C6(a) Convex underestimators, convergence order, cluster problem

**Closest prior art.**

*The alpha-BB family.*
- Adjiman, Dallwig, Floudas, Neumaier, "A global optimization method, alphaBB, for general twice-differentiable constrained NLPs - I. Theoretical advances", Comput. Chem. Eng. 22(9):1137-1158 (1998); Part II by Adjiman, Androulakis, Floudas, 22(9):1159-1179. `[V]`
- Akrotirianakis and Floudas, "A new class of improved convex underestimators for twice continuously differentiable constrained NLPs", J. Glob. Optim. 30(4):367-390 (2004), doi:10.1007/s10898-004-6455-4; companion computational paper J. Glob. Optim. 29:249-264 (2004). Exponential relaxation terms, convexity verified by interval arithmetic, tighter than alpha-BB. `[V]`
- Skjal, Westerlund, Misener, Floudas, "A generalization of the classical alphaBB convex underestimation via diagonal and nondiagonal quadratic terms", J. Optim. Theory Appl. 154(2):462-490 (2012), doi:10.1007/s10957-012-0033-6. Non-diagonal perturbation Hessian, interval Gerschgorin test, optimal parameters by an LP. `[V]`
- Skjal and Westerlund, J. Glob. Optim. 58(3):411-427 (2014): parameters optimized for average rather than maximal underestimation error. `[V]` for venue and content; the title "New methods for calculating alphaBB-type underestimators" is `[unverified-from-memory]`.
- Hladik, "On the efficient Gerschgorin inclusion usage in the global optimization alphaBB method", arXiv:1307.2786, and "The effect of Hessian evaluations in the global optimization alphaBB method", arXiv:1307.2791. `[V]`
- Kazazakis and Adjiman, "Arbitrarily tight alphaBB underestimators of general non-linear functions over sub-optimal domains", J. Glob. Optim. 71(4):815-844 (2018), doi:10.1007/s10898-018-0632-3 (mu-subenergy transformation). `[V]`
- Nerantzis and Adjiman, "Tighter alphaBB relaxations through a refinement scheme for the scaled Gerschgorin theorem", J. Glob. Optim. 73(3):467-483 (2019), doi:10.1007/s10898-018-0718-y. `[V]`
- **Trigonometric-specific:** Caratzoulas and Floudas, "Trigonometric convex underestimator for the base functions in Fourier space", J. Optim. Theory Appl. 124(2):339-362 (2005), doi:10.1007/s10957-004-0940-2. A three-parameter underestimator `-a sin[k(x-x_s)] + b` for `alpha sin(x+s)`, applicable to trigonometric polynomials of arbitrary dimension and degree; the maximal separation grows linearly with domain size. `[V]`

*Deterministic global optimization in torsion space (direct ancestors of "certified optimization of chain molecules in torsion angles").*
- Maranas and Floudas, "Global minimum potential energy conformations of small molecules", J. Glob. Optim. 4:135-170 (1994), doi:10.1007/BF01096720. Energy minimized over an independent set of torsion angles with epsilon-convergence by convex lower bounding. `[V]`
- Androulakis, Maranas, Floudas, "Prediction of oligopeptide conformations via deterministic global optimization", J. Glob. Optim. 11:1-34 (1997). `[unverified-from-memory]` for the bibliographic details.
- Klepeis and Floudas, "Free energy calculations for peptides via deterministic global optimization", J. Chem. Phys. 110(15):7491-7512 (1999), doi:10.1063/1.478652. alpha-BB in torsion space plus free energies by a harmonic approximation (met- and leu-enkephalin). This is the closest historical precedent for "deterministic optimization plus free energy on a torsion torus"; the entropy part is an approximation, not a bound. `[V]`
- Lin and Stadtherr, "Deterministic global optimization of molecular structures using interval analysis", J. Comput. Chem. 26:1413-1420 (2005), doi:10.1002/jcc.20285. Interval methods with a "mathematical and computational guarantee" on Lavor's torsion-angle test problems. `[V]` The test-function reference I recall is Lavor and Maculan, Numer. Algorithms 35:287-300 (2004), doi:10.1023/B:NUMA.0000021763.84725.b9 (the DOI appeared in search results; authors and pages are `[unverified-from-memory]`).
- Kuznetsov and Sahinidis, "New bounds and formulations for the deterministic global optimization of Lennard-Jones clusters", J. Glob. Optim. (2025), doi:10.1007/s10898-025-01476-7. Current state of the art for LJ: new distance bounds, symmetry breaking, a new convex underestimator; first general-purpose-solver proofs for the 5- and 6-atom clusters and two previously open instances. `[V]` Follow-ups: Lecomte, arXiv:2607.09555 (July 2026; certified refinement of the diameter bound, "re-verified in directed-rounding arithmetic") `[V]`; Shen, arXiv:2611.09925 (2026; exact global-optimality and uniqueness for 7-particle LJ and Thomson) `[V, abstract only]`.

*Convergence order and the cluster problem.*
- Bompadre and Mitsos, "Convergence rate of McCormick relaxations", J. Glob. Optim. 52(1):1-28 (2012), doi:10.1007/s10898-011-9685-2. Propagation rules for convergence order under addition, multiplication and composition; no gain over the underlying interval bounds unless factor relaxations have high pointwise order. `[V]` The statement that alpha-BB guarantees quadratic (second-order) convergence is part of that abstract as I recall it: `[unverified-from-memory]`.
- Bompadre, Mitsos, Chachuat, "Convergence analysis of Taylor models and McCormick-Taylor models", J. Glob. Optim. 57(1):75-114 (2013), doi:10.1007/s10898-012-9998-9. `[V]`
- Najman and Mitsos, "Convergence analysis of multivariate McCormick relaxations", J. Glob. Optim. 66:597-628 (2016). `[unverified-from-memory]`
- Du and Kearfott, "The cluster problem in multivariate global optimization", J. Glob. Optim. 5:253-265 (1994), doi:10.1007/BF01096455. `[V]`
- Wechsung, Schaber, Barton, "The cluster problem revisited", J. Glob. Optim. 58(3):429-438 (2014), https://dspace.mit.edu/handle/1721.1/103614. A threshold on the convergence-order prefactor eliminates the cluster problem for second-order relaxations. `[V]`
- Kannan and Barton, "The cluster problem in constrained global optimization", J. Glob. Optim. 69(3):629-676 (2017), doi:10.1007/s10898-017-0531-z: first-order schemes may suffice at constrained minima. Companion: "Convergence-order analysis of branch-and-bound algorithms for constrained problems", J. Glob. Optim. 71(4):753-813 (2018). `[V]`
- Bandit-side analogue: Munos, "Optimistic optimization of a deterministic function without the knowledge of its smoothness", NIPS 24:783-791 (2011): DOO/SOO, with complexity governed by the near-optimality dimension. `[V]`
- Information-based complexity: Holzmuller and Bach (see C8(d)) give `Theta(B n^{-m/d})` for optimization of `C^m` functions with norm bound `B`, the benchmark that any relaxation scheme on `T^M` is measured against. `[V]`

**Verdict.** KNOWN. The field is mature, and deterministic global optimization of molecules in torsion coordinates with rigorous lower bounds is thirty years old (Floudas group; Lin-Stadtherr). A MetricChain claim in this area can only be new through (i) the handling of the black-box residual, (ii) torus-specific structure, or (iii) machine-checked certificates.

Two consequences worth stating explicitly:
1. On a torus every minimizer is an interior, unconstrained minimizer, so the unconstrained cluster analysis (Du-Kearfott; Wechsung et al.) applies and the constrained-case relief of Kannan-Barton is unavailable. A scheme that is only first-order in `Delta` (Lipschitz or bounded-difference information) will cluster.
2. McCormick, alpha-BB and Taylor-model relaxations need symbolic access or Hessian enclosures. For a truly black-box `Delta` they do not apply; for a white-box neural `Delta` the contemporary competitor is neural-network bound propagation (interval/linear relaxation of networks, embedded-network global optimization), `[unverified-from-memory]` as to specific references.

**Confidence.** High.

**How to sharpen.**
1. *A composite convergence-order theorem with a resolution limit.* Treat `E_0` exactly on each box (dynamic programming gives an "infinite-order" bound) and `Delta` by a first-order bound with Lipschitz constant `L`. Reviewer's heuristic: boxes within distance `sqrt(eps/kappa)` of a minimizer with curvature `kappa` must have width at most `eps/L` to be fathomed, so the scheme is cluster-free down to a tolerance of order `L^2/kappa` and exponential below it. Prove this, together with a matching oracle lower bound in the model "exact `E_0`, Lipschitz-only `Delta`". The cluster literature assumes one convergence order for the whole scheme; a two-component statement was not found.
2. *Torus-native lower bounding inside branch and bound.* Use trigonometric underestimators (Caratzoulas-Floudas) or SOS-on-torus bounds with exponential convergence (Bach-Rudi, C6(b)) as the bounding step, state the convergence order in geodesic box width, and benchmark on the Lavor/Lin-Stadtherr torsion test set and against Kuznetsov-Sahinidis for LJ.

### C6(b) Sum-of-squares and moment hierarchies for trigonometric polynomials

**Closest prior art.**
- Dumitrescu, *Positive Trigonometric Polynomials and Signal Processing Applications*, Springer (2007; second edition 2017). Gram-matrix parametrization and bounded-degree SOS relaxations for multivariate trigonometric polynomials. `[unverified-from-memory]` for edition details; a 2026 paper cited below confirms that the trigonometric SOS hierarchy originated in signal processing.
- Bach and Rudi, "Exponential convergence of sum-of-squares hierarchies for trigonometric polynomials", SIAM J. Optim. 33(3):2137-2159 (2023), doi:10.1137/22M1540818, arXiv:2211.04889. Unconstrained minimization on the torus: `O(1/s^2)` for the degree-`s` relaxation with no assumptions, and exponential convergence when there are finitely many global minimizers with invertible Hessians; extension to polynomials on the hypercube. `[V]` This is the result any torus relaxation claim must be compared with.
- Laurent and Slot, "An effective version of Schmudgen's Positivstellensatz for the hypercube", Optim. Lett. (2023), arXiv:2109.09528: `O(1/r^2)` via the polynomial kernel method (Jackson kernel). `[V]` Baldi and Slot, "Degree bounds for Putinar's Positivstellensatz on the hypercube", arXiv:2302.12558. `[V]` Gribling, de Klerk, Vera, "Revisiting the convergence rate of the Lasserre hierarchy for polynomial optimization over the hypercube", arXiv:2505.00544 (2025). `[V]`
- Sparse hierarchies: Korda, Magron, Rios-Zertuche, "Convergence rates for sums-of-squares hierarchies with correlative sparsity", Math. Program. 209:435-473 (2025), doi:10.1007/s10107-024-02071-6, arXiv:2303.14824: rates depend on the largest clique rather than the ambient dimension. `[V]` Wang, Magron, Lasserre, TSSOS, arXiv:1912.08899; Magron and Wang, *Sparse polynomial optimization: theory and practice*, arXiv:2208.11158. `[V]`
- Unit-modulus (complex) formulation: Josz and Molzahn, "Lasserre hierarchy for large scale polynomial optimization in real and complex variables", SIAM J. Optim. 28(2):1017-1048 (2018), arXiv:1709.04376 (optimal power flow with thousands of variables). `[V]` Wang and Magron, arXiv:2308.14631. `[V, listing]`
- Exact certificates: Magron, Safey El Din, Schweighofer, Vu, "Exact SOHS decompositions of trigonometric univariate polynomials with Gaussian coefficients", arXiv:2202.06544 (v1 2022, v2 2023). **Univariate only.** Three algorithms (complex root isolation; SDP with compensation; rounding-projection in the style of Peyrl-Parrilo), bit complexity polynomial in the degree and linear in the coefficient bitsize. `[V]` Venue: ISSAC; one index gives ISSAC 2022 and another returns doi:10.1145/3597066.3597072 (the ISSAC 2023 prefix), not resolved here. Multivariate real-variable counterparts: Magron and Safey El Din, arXiv:1802.10339 and arXiv:1811.10062; Magron, Safey El Din, Vu, arXiv:2107.11825. `[V, listing]`
- Recent use on `T^M`: Sakos, Varvitsiotis, Korpas, Lin, "Global optimization for parametrized quantum circuits", arXiv:2603.21757 (March 2026): trigonometric moment/SOS hierarchies over the `M`-torus with a flat-extension check, for a constant number of parameters. `[V]`

**Verdict.** KNOWN for the hierarchy, its rates, and the identification of trigonometric polynomials with polynomials on a product of circles. Two gaps where the searches returned nothing:
- (i) multivariate exact rational SOS/SOHS certificates on `T^M` with a priori bit-size bounds (the published exact algorithm for the trigonometric setting is univariate);
- (ii) convergence rates for sparse (chain- or tree-structured) trigonometric hierarchies; Korda et al. treat the real-variable Schmudgen/Putinar setting.

**Confidence.** High for KNOWN; medium for the gaps (searched: "exact rational SOS multivariate trigonometric Hermitian squares torus", "sparse moment-SOS trigonometric torus 2024-2026", "TSSOS unit modulus").

**How to sharpen.**
1. Prove a Bach-Rudi-type rate (ideally the exponential rate under non-degenerate minimizers) for the correlatively sparse trigonometric hierarchy whose cliques are sliding windows of consecutive torsions, and show exactness at bounded order for tree-structured `E_0` (the SOS counterpart of dynamic programming).
2. Give a multivariate exact-certificate algorithm on `T^M` (rounding-projection modulo the ideal generated by `c_i^2+s_i^2-1`) with bit-size bounds, designed so that the output is checkable by a kernel-level Lean checker (see C6(d)).

### C6(c) The torus as a real variety; polynomial kinematics; rational Lennard-Jones; exact rational certificates

**Closest prior art, by ingredient.**

*Kinematics on a product of circles is the standard algebraic formulation.*
- Wampler and Sommese, "Numerical algebraic geometry and algebraic kinematics", Acta Numerica 20:469-567 (2011), doi:10.1017/S0962492911000067. Full text checked: "One way to convert the trigonometric equations to polynomials is to introduce ... variables x_i = cos phi_i, y_i = sin phi_i ... and the trigonometric identities"; for spatial chains, joint angles on the "six-torus" are handled by "unit circle representations"; tangent half-angle and isotropic coordinates are the listed alternatives. `[V]`
- Emiris and Mourrain, "Computer algebra methods for studying and computing molecular conformations", Algorithmica 25:372-402 (1999), doi:10.1007/PL00008283: conformations of cyclic molecules as polynomial systems (distance geometry, sparse resultants). `[V]`
- Coutsias, Seok, Jacobson, Dill, "A kinematic view of loop closure", J. Comput. Chem. (2004), doi:10.1002/jcc.10416: six-torsion loop closure reduced to a univariate polynomial of degree 16. `[V]`

*Polynomial optimization and SOS certificates for kinematic chains (robotics).*
- Trutman, Safey El Din, Henrion, Pajdla, "Globally optimal solution to inverse kinematics of 7DOF serial manipulator", arXiv:2007.12550 (IEEE RA-L 2022): Lasserre relaxations after a symbolic reduction to degree 2; the second relaxation suffices. `[V]`
- Amice, Dai, Werner, Zhang, Tedrake, "Finding and optimizing certified, collision-free regions in configuration space for robot manipulators", arXiv:2205.03690 (WAFR 2022). Full text checked: forward kinematics "assumes the form of the trigonometric polynomial", becomes "the following rational function" under the tangent half-angle substitution, and a "Sum-of-Squares program" (Putinar) certifies regions. `[V]` Journal follow-up: Dai et al., arXiv:2302.12219. `[V]`
- Khoo, Singer, Cowburn, "Integrating NOE and RDC using sum-of-squares relaxation for protein structure determination", J. Biomol. NMR 68(3):163-185 (2017), doi:10.1007/s10858-017-0108-7, arXiv:1604.01504: SOS relaxations for the pose of an articulated protein backbone (restraint fitting, not a force-field energy). `[V]`

*Rational objectives and pair-potential energies.*
- Bugarin, Henrion, Lasserre, "Minimizing the sum of many rational functions", Math. Program. Comput. 8(1):83-111 (2016), doi:10.1007/s12532-015-0089-z, arXiv:1102.4954: a moment hierarchy for sums of many rational terms that avoids a common denominator. `[V]` Dual SOS hierarchy: Guo, Wang, Zheng, arXiv:2405.09419 (2024). `[V, listing]`
- de Laat, "Moment methods in energy minimization: new bounds for Riesz minimal energy problems", Trans. Amer. Math. Soc., doi:10.1090/tran/7976 (arXiv journal reference: 2019), arXiv:1610.04905: a converging moment hierarchy lower-bounding ground-state energies of interacting particles (five points on the sphere computed numerically; whether the SDP bounds were made rigorous was not checked). `[V]`
- LJ clusters in Cartesian coordinates with convex underestimators rather than SOS: Kuznetsov-Sahinidis 2025 (C6(a)). `[V]`

*Exact rational certificates and proof-assistant checking.*
- Rounding-projection and exact Positivstellensatz certificates: the Magron-Safey El Din papers listed in C6(b). `[V, listing]` Peyrl and Parrilo, Theor. Comput. Sci. 409 (2008). `[unverified-from-memory]`
- Li, Xiong, Yang, "A proof of the Dittert conjecture in dimension 4 via an exact constrained sum-of-squares certificate", arXiv:2607.29191 (2026): an exact rational constrained SOS certificate (152 + 136 x 16 squares), checked by exact LDL^T over Q and "formally verified using the Lean proof assistant". `[V, abstract]` This is a direct 2026 precedent for exact SOS certificates checked in Lean, in a non-molecular setting.
- Lean 4 SOS tactics exist (C6(d)): `leanprover/sos`, Sostactic. `[V]`
- Ugwuanyi, Jones, Velkey, Josephson, "Benchmarking energy calculations using formal proofs" (LeanLJ), Mol. Phys. (2025), doi:10.1080/00268976.2025.2539421, arXiv:2505.09095: Lennard-Jones energy evaluation with periodic boundaries formalized in Lean 4. Energy evaluation only; no optimization or certificates. `[V]`

**Verdict.** Each ingredient is KNOWN and standard: the unit-circle representation of joint angles, polynomial or rational forward kinematics, SOS certificates on such varieties, moment hierarchies for sums of rational functions, exact rational certificates, and Lean checking of SOS identities. For the assembled pipeline, namely torsion-space molecular energies (kinematics composed with 12-6 LJ and torsional terms) treated as rational functions on `prod {c_i^2+s_i^2=1}` with exact rational certificates checked without transcendental functions, the verdict is NO MATCH FOUND.

Searches: "polynomial optimization sum of squares molecular conformation torsion cos sin Lennard-Jones certificate"; "Lasserre hierarchy molecular conformation / protein folding / distance geometry"; "SOS / semidefinite relaxation Lennard-Jones cluster certified global minimum"; "torsion c_i^2+s_i^2=1 polynomial system loop closure polynomial optimization conformational energy"; "SOS protein side-chain continuous dihedral global certificate"; "Lean 4 Lennard-Jones formal verification".

**Confidence.** Medium. The idea is natural, and the absence may reflect that it does not scale rather than that nobody has thought of it.

**Technical caveats that a referee will raise (reviewer's derivations).**
- *Rational coefficients need rational bond-angle sines and cosines.* The tetrahedral angle has `cos = -1/3` but `sin = 2 sqrt(2)/3`. Either fix bond angles at rational points of the circle (for example `tan(theta/2) = 41/29` gives 109.455 degrees) and state the theorem for that model, or work over a real quadratic field.
- *Degree structure.* Because rotations preserve norms, a squared interatomic distance is multi-affine in the pairs `(c_j, s_j)` of the intervening torsions (degree one in each, total degree equal to the number of intervening torsions). A 12-6 term is then rational with denominator of degree six times that number. A common denominator over all pairs is out of the question, which is exactly the situation Bugarin-Henrion-Lasserre address.
- *Poles.* The LJ energy is infinite on the clash set, so certificates must be stated for `p - gamma q >= 0` with care on the zero set of `q`.
- *Coulomb terms* are algebraic, not rational (`1/r`); they need an auxiliary variable with `r^2 = d(c,s)`.
- *Transcendental-free checking holds for optimization only.* Partition functions need the Haar measure of arcs, which involves arctangents of rationals; enclosures are easy but not transcendental-free.

**How to sharpen.**
1. *Rational-arc branch-and-bound certificates.* Use boxes that are products of arcs with rational endpoints on the circle, so that every leaf bound is a statement in Q checkable by kernel-level rational arithmetic. Pair this with the exact-SOS route only for the low-degree, chain-sparse part. No precedent for rational-arc certificates of molecular energies was found.
2. *Make the statement about a specific rational model and prove the degree and sparsity structure* (multi-affine squared distances; clique structure of the chain) as lemmas, then give a size bound for the certificate in terms of `M` and the interaction range. This turns a modelling remark into a theorem that the robotics and SOS literature does not contain.

### C6(d) Formally verified interval arithmetic and global optimization, with emphasis on Lean 4

**Outside Lean (closest prior art).**
- **Coq/Rocq, CoqInterval.** Martin-Dorel and Melquiond, "Proving tight bounds on univariate expressions with elementary functions in Coq", J. Autom. Reason. (2016), doi:10.1007/s10817-015-9350-4: a reflexive tactic for bounds on univariate (and quasi-multivariate) expressions with elementary functions. `[V]` Mahboubi, Melquiond, Sibut-Pinote, "Formally verified approximations of definite integrals", J. Autom. Reason. 62(2):281-300 (2019), doi:10.1007/s10817-018-9463-7 (conference version ITP 2016): verified enclosures of definite integrals via rigorous polynomial approximations and adaptive splitting, including some improper integrals. `[V]` A Lean Zulip participant sized CoqInterval at about 40k lines. `[V]`
- **HOL Light, Flyspeck.** Solovyev and Hales, "Formal verification of nonlinear inequalities with Taylor interval approximations", NFM 2013, LNCS 7871:383-397, arXiv:1301.1702: multivariate polynomial and non-polynomial inequalities on rectangular domains, interval arithmetic with Taylor approximations, about 3000 times slower than the unverified C++ check. `[V]` Hales et al., "A formal proof of the Kepler conjecture", arXiv:1501.02155. `[V]`
- **PVS.** Narkawicz and Munoz, "A formally verified generic branching algorithm for global optimization", VSTTE 2013, LNCS 8164:326-343, doi:10.1007/978-3-642-54108-7_17: a generic verified branch-and-bound that can be instantiated. Munoz and Narkawicz, "Formalization of Bernstein polynomials and applications to global optimization", J. Autom. Reason. (2013), doi:10.1007/s10817-012-9256-3. `[V]`
- **SOS and SDP certificates in Coq.** Magron, Allamigeon, Gaubert, Werner, "Formal proofs for nonlinear optimization", arXiv:1404.7282 (J. Formaliz. Reason. 2015). `[V]` Martin-Dorel and Roux, "A reflexive tactic for polynomial positivity using numerical solvers and floating-point computations", CPP 2017, pp. 90-99, doi:10.1145/3018610.3018622 (ValidSDP). `[V]`
- Isabelle's `approximation` method and affine arithmetic were mentioned in the Lean Zulip discussion. `[V]` for the mention; specific references `[unverified-from-memory]`.

**What the Lean 4 libraries actually prove.**

| Library | Numbers | What is proved | Functions | Automation and trust | Not provided (as far as found) |
|---|---|---|---|---|---|
| `girving/interval` (Geoffrey Irving, Adomas Baliuka, Michael George; Apache-2.0) `[V]` | Software floating point `Floating`: 64-bit mantissa and 64-bit exponent, with `nan`. "All arithmetic is conservatively rounded up or down." Built because "Lean's `Float` is untrusted". | Enclosure only: typeclasses `Approx A R`, `ApproxAdd`, `ApproxField` state that `Interval` (and complex `Box`) operations conservatively contain the real result. The author's announcement: "(almost) no results saying that the intervals are tight". | Field operations; `exp`, `log`, powers by power series (February 2024). The current tree also has modules named `Sincos`, `Sqrt`, `Hyperbolic`, `Pi`, `Log2`, `Series`, `Division` (module names seen; theorem statements not inspected). | An `interval` tactic for constant real inequalities (June 2024), originally via `native_decide` (which trusts the compiler); kernel `decide` works in some cases. The library proofs add no axioms and do not rely on hardware floats. | Multivariate Taylor models; branch-and-bound or global-optimization certificates. Main use: verified Mandelbrot computations. |
| `LeanCert` (Alejandro Radisic; Apache-2.0; v1.0 announced 12 January 2026; releases archived on Zenodo, e.g. doi:10.5281/zenodo.21681348) `[V]` | Rational, dyadic and affine interval evaluation over a reified expression type. No hardware or IEEE floats; the rational backend is exact (how the dyadic backend rounds was not inspected). | Certificate architecture: untrusted search, an executable checker, and proved soundness ("golden") theorems lifting checker success to statements over the reals. For global optimization, a branch-and-bound over boxes with `globalMinimize_lo_correct` (conclusion as displayed in the generated docs: `(globalMinimize e B cfg).bound.lo <= Core.Expr.eval rho e` for every environment `rho` in the box `B`, under a supported-expression hypothesis) and `globalMinimize_hi_achievable`; analogous statements for the dyadic and affine variants. Also root existence/uniqueness (bisection, Newton, Krawczyk), definite-integral bounds, forward-mode automatic differentiation, and neural-network certificate infrastructure. | `exp`, `log`, `sin`, `cos`, `sqrt`, `atan`, `atanh`, `erf` (README); Taylor remainders in Lagrange form. | One `leancert` tactic with trust modes: `native` (default, `native_decide`, which additionally trusts the compiler), `kernel` (`decide +kernel`), `auto`. A Python SDK for candidate search. | Completeness ("not a complete decision procedure"). In a third-party build of the docs (possibly outdated), the division-enabled evaluator `evalOnBoxCoreDiv` carries the note "No formal correctness proof yet; returns sound but possibly wide bounds". |
| `leanprover/sos` v0.1.0 (updated September 2026; builds on Lean 4.33.1) `[V]` | Rational certificates. | Harrison-style SOS: Putinar-form SDP solved by CSDP (FFI), Gram matrix rounded to Q, rational LDL^T, and the final identity checked by `decide +kernel`, so success does not depend on the solver. Hypotheses are used as multipliers; optional Positivstellensatz refutations. | Polynomial (in)equalities over the reals; goals over N, Z, Q are lifted. | `by sos`, and `by sos?` to emit a witness term. | Algebraic-number certificates; automatic degree escalation. |
| Sostactic (community; Python backend; April 2026) `[V, listing]` | Rational. | SOS-based tactics for polynomial inequalities. | Polynomials. | Tactics. | Not examined. |
| Mathlib `[V]` | Exact. | `norm_num`, `positivity`, `linarith`/`nlinarith`, `linear_combination`, `interval_cases` (finite integer cases). `polyrith` is no longer functional: its documentation states that the external Sage server was shut down and points to `grobner`. | n/a | n/a | No interval-arithmetic tactic in Mathlib itself was found. |
| Flean (`minusgix/flean`) `[V]` | IEEE 754 formats. | All five rounding modes with error bounds, error-free transformations, Kahan summation, correctly rounded `exp` and `log`. | n/a | Library. | Interval layer. |
| FloatLib (George, Adkisson, Anandkumar, arXiv:2609.19352, September 2026) `[V]` | Arbitrary-precision binary/decimal floats, posits. | Each backend proved equal to an encoded specification; links to real rounding and error bounds. | n/a | Library. | Interval layer not mentioned in the abstract. |
| DSLean (Rowney, Ahuja, Avigad, Welleck, arXiv:2602.18657) `[V]` | External solver certificates. | Bridges Lean to external solvers for interval arithmetic (Gappa, per the paper as summarized by search), ODEs, and ideal membership. | n/a | Tactics. | n/a |

**Direct answers to the brief.**
- *Floats with directed rounding?* Yes in `girving/interval` (software floats with proved conservative rounding). LeanCert avoids hardware floats and computes with rational and dyadic numbers.
- *Taylor models?* Univariate Taylor or power-series enclosures with remainder bounds exist in both. Full multivariate Taylor models with verified polynomial arithmetic, in the sense of Makino-Berz or of the Flyspeck Taylor intervals, were not found in Lean 4.
- *Global optimization certificates?* Yes in LeanCert (branch and bound over boxes with correctness theorems), for expressions in its supported language. No Lean library was found that certifies optimization or integration of a molecular energy, or that handles a black-box residual.
- *SOS?* Yes: `leanprover/sos`, Sostactic, and the Lean-verified certificate of arXiv:2607.29191.

**Verdict.** KNOWN. Verified interval arithmetic and verified branch-and-bound exist in Coq, HOL Light, PVS and now Lean 4. A MetricChain contribution here would be an application (a verified certificate for a chain-molecule energy), not new infrastructure.

**Confidence.** High for the description as fetched; the ecosystem moves fast. One practical observation: LeanCert's archived releases are numbered v4.32.x (apparently following the Lean version) and `sos` is reported to build on Lean 4.33.1, whereas this repository pins Lean and Mathlib v4.31.0, so neither can be assumed to be a drop-in dependency.

**How to sharpen.**
1. State clearly which trust base the certificates use. Kernel-checked rational certificates (rational-arc boxes, exact SOS identities) are a stronger claim than `native_decide` and would distinguish the work from LeanCert's default mode.
2. Aim at what the libraries lack: a verified enclosure of a partition-function integral (LeanCert and CoqInterval bound one-dimensional integrals of expressions; no verified multidimensional Boltzmann integral was found), or a verified certificate for a tree-structured `E_0` whose checking cost is linear in `M`.

---

## C7. Free-energy sandwich via concentration

Claim under review: for a reference Gibbs measure `mu_0` and a residual with bounded differences `c_i`,

    -beta <Delta>_0  <=  ln(Z/Z_0)  <=  -beta <Delta>_0 + (beta^2/8) K sum_i c_i^2,

with `K = 1` for product references and `K` of type `(1-theta)^-2` for Markov or Dobrushin references; sharpness by additive two-level residuals; and the Bobkov-Gotze equivalence with T1.

### C7.1 The sandwich for product references

**Closest prior art.**
- Lower bound: Jensen, i.e. the Gibbs-Bogoliubov inequality. Isihara, "The Gibbs-Bogoliubov inequality", J. Phys. A 1(5):539-548 (1968), doi:10.1088/0305-4470/1/5/305. `[V]` Free-energy perturbation identity: Zwanzig, J. Chem. Phys. 22(8):1420-1426 (1954), doi:10.1063/1.1740409. `[V]`
- Upper bound: `ln(Z/Z_0) + beta <Delta>_0` is the log moment generating function of the centred residual under `mu_0`, and the bounded-differences bound `lambda^2 sum c_i^2 / 8` is the lemma behind McDiarmid's inequality. Hoeffding, J. Amer. Statist. Assoc. 58:13-30 (1963); McDiarmid, "On the method of bounded differences", LMS Lecture Note Series 141 (1989). `[V, via the reference list of Rio 2013]`
- The same inequality used for uncertainty quantification: Gourgoulias, Katsoulakis, Rey-Bellet, Wang, "How biased is your model? Concentration inequalities, information and model bias", IEEE Trans. Inf. Theory 66(5), from p. 3080 (2020), arXiv:1706.10260. Full text checked: Proposition 17 is the McDiarmid MGF bound `exp((c^2/8) sum d_k^2)`, Theorem 18 turns it into `|E_P psi - E_Q psi| <= (sum d_k^2)^{1/2} sqrt(2 sum R(Q_i||P_i))`, and the paper names the Donsker-Varadhan / Gibbs variational formula as the key ingredient; Theorem 2 shows tightness of the underlying information inequality over KL balls. It bounds model bias `E_Q f - E_P f`, not `ln(Z/Z_0)`; molecular dynamics is listed as future work. `[V]`
- Related scalable inequalities with statistical-mechanics applications (phase diagrams): Katsoulakis, Rey-Bellet, Wang, J. Comput. Phys. 336:513-545 (2017), doi:10.1016/j.jcp.2017.02.020, arXiv:1605.04184. `[V]`
- Thermodynamic language for concentration, in the opposite direction: Maurer, "Thermodynamics and concentration", Bernoulli 18(2):434-454 (2012), doi:10.3150/10-BEJ341, arXiv:1205.1595, writes the log-Laplace transform as an integral of thermal entropy over inverse temperature and derives a strong form of the bounded-difference inequality. `[V]`

**Has it been used in statistical physics, molecular simulation, or graphical models?**
- *Molecular simulation.* The two-sided bound in circulation is the classical one, `<U>_perturbed <= Delta F <= <U>_reference`, which needs an average in the perturbed ensemble: Delle Site, Ciccotti, Hartmann (J. Stat. Mech. 2017, as cited by the next item); Reible, Hartmann, Delle Site, "Two-sided Bogoliubov inequality to estimate finite size effects in quantum molecular simulations", Lett. Math. Phys. 112:97 (2022), doi:10.1007/s11005-022-01586-3, arXiv:2111.10282; Reible, Much, Verch, Schutte, Delle Site, arXiv:2608.07246 (August 2026, von Neumann algebra version). `[V]` Jensen-gap bounds motivated by exponential averaging: Gao, Sitharam, Roitberg, arXiv:1712.05267. `[V, abstract]` Cumulant truncations of the Zwanzig formula are used as approximations; no paper was found that bounds the truncation error by a bounded-differences (Hoeffding or McDiarmid) argument.
- *Graphical models and machine learning.* (a) Mean-field error bounds control the Gibbs-Bogoliubov gap at the optimal product measure for Ising-type models: Jain, Koehler, Risteski, STOC 2019, arXiv:1808.07226 (`F - F* <= 3 n^{2/3} ||J||_F^{2/3}`); Eldan, arXiv:1811.11530; Jain, Koehler, Mossel, arXiv:1802.06126. `[V]` These are deeper results in a narrower model class and do not need bounded differences of a black box. (b) Stochastic sandwiches: Grosse, Ghahramani, Adams, "Sandwiching the marginal likelihood using bidirectional Monte Carlo", arXiv:1511.02543. `[V]` (c) Probabilistic bounds combining variational upper bounds with importance sampling: Liu, Fisher, Ihler, NIPS 2015. `[V, abstract]` (d) Variational upper and lower bounds on free-energy differences with learned transport: FEAT, arXiv:2504.11516 (2025). `[V, listing]`
- *Not found:* the inequality displayed above stated as a free-energy perturbation bound for molecular or graphical-model partition functions. Searches: "free energy perturbation rigorous upper bound bounded differences McDiarmid Hoeffding cumulant error bound"; "Gibbs-Bogoliubov lower bound complement Hoeffding sub-Gaussian second order two-sided"; "log partition function upper bound bounded differences McDiarmid Jensen product measure mean field error"; "rigorous bounds free energy reference potential neural network correction".

**Verdict.** KNOWN-IN-SPIRIT. Mathematically it is a one-line corollary of two textbook facts, and the identical inequality (with the Gibbs variational principle named) is used for model-bias UQ by Gourgoulias et al. Its presentation as a certified second-order free-energy perturbation bound for `E_0 + Delta` was not found.

**Confidence.** High.

**Practical caveat (reviewer's arithmetic).** The gap is extensive: at 298 K, with `c_i = 0.5` kcal/mol on `M = 100` torsions, `beta c = 0.84` and the gap is about 8.8 nats, or 5.2 kcal/mol. The bound certifies free energies only when `c_i` is well below `kT/sqrt(M)`, or after localization (below).

### C7.2 Dependent references

**Closest prior art.**
- Kontorovich and Ramanan, "Concentration inequalities for dependent random variables via the martingale method", Ann. Probab. 36(6):2126-2158 (2008), doi:10.1214/07-AOP384, arXiv:math/0609835. `[V]`
- Kontorovich and Raginsky, "Concentration of measure without independence: a unified approach via the martingale method", arXiv:1602.00721 (2016; IMA volume). Full text checked. Theorem 4.2: `P(|f - E f| >= t) <= 2 exp(-2 t^2 / ||Gamma delta(f)||_2^2)` with `Gamma` built from Wasserstein matrices; this is the form with the Hoeffding-sharp constant, hence an MGF bound `lambda^2 ||Gamma c||^2 / 8`. Markov chains: `Gamma_ij <= theta_i ... theta_{j-1}` (their eq. 42), so `||Gamma|| <= 1/(1-theta)`. Corollary 5.3: under Dobrushin uniqueness, `Gamma = (D)^T` with `D = sum_m C^m`. The authors state that they recover Kontorovich-Ramanan "with an improved constant" and that "the same inequality, but with a worse constant in the exponent, was obtained by Kulske". `[V]`
- Kulske, Commun. Math. Phys. 239:29-51 (2003), doi:10.1007/s00220-003-0841-5; Chazottes, Collet, Kulske, Redig, Probab. Theory Relat. Fields 137:201-225 (2007), doi:10.1007/s00440-006-0026-1, arXiv:math/0503483 (coupling matrix; Gaussian bound under uniform control of the coupling). `[V]`
- Marton, Ann. Probab. 24(2):857-866 (1996) and later papers; Samson, Ann. Probab. 28(1):416-461 (2000); Djellout, Guillin, Wu, Ann. Probab. 32(3B):2702-2732 (2004), Theorem 2.11; Wu, Ann. Probab. 34(5):1960-1989 (2006); Paulin, Electron. J. Probab. 20:1-32 (2015). `[V, via the survey's reference list]`
- A competing scaling: Chatterjee, "Stein's method for concentration inequalities", Probab. Theory Relat. Fields 138:305-321 (2007), arXiv:math/0604352. As quoted in the survey (eq. 45): `P(|f - E f| >= t) <= 2 exp(-(1 - ||C||_2) t^2 / sum alpha_i^2)`. `[V]` In the claim's normalization this corresponds to `K = 2/(1 - ||C||_2)`: worse by a factor two when there is no dependence, but with a first power rather than a square of the gap, so it wins when `||C||_2 > 1/2`. The MGF form of Chatterjee's result is `[unverified-from-memory]`.
- Tree-structured rather than chain references: Kontorovich, "Obtaining measure concentration from Markov contraction", Markov Process. Related Fields (2012), is in the survey's reference list and supplies the contraction estimate `theta_i <= (R_i - r_i)/(R_i + r_i)` for chain-structured pair potentials (as quoted in the survey). `[V, via the survey]` A dedicated result for Markov tree processes by the same author is `[unverified-from-memory]`.

**Verdict.** KNOWN. **Confidence.** High.

### C7.3 Sharpness: the worst case is additive and two-level

**Closest prior art.**
- Rio, "On McDiarmid's concentration inequality", Electron. Commun. Probab. 18(44):1-11 (2013), doi:10.1214/ECP.v18-2659. Full text checked. Lemma 4.1: for a separately 1-Lipschitz function of independent variables on spaces of diameters `Delta_k`,

      log E exp(tZ - tE Z) <= l(Delta_1 t) + ... + l(Delta_n t),
      l(t) = sup_{r in [0,1]} [ log(1 + r(e^t - 1)) - t r ]
           = (t - log t - 1) + t/(e^t - 1) + log(1 - e^{-t}),

  with maximizer `r_t = (e^t - t - 1)/(t(e^t - 1))`, expansion `l(t) = t^2/8 - t^4/576 + O(t^6)` (Remark 2.3), `l(t) <= t^2/8`, and `l(t) = t - log t - 1 + o(1)` for large `t`. The bracket is exactly the claim's `ln(p e^{beta c(1-p)} + (1-p) e^{-beta c p})` with `p = r`, `t = beta c`. Rio's proof bounds each martingale increment by the two-point (Bernoulli) extremal and then maximizes over `r`. For the tail lower bound he uses additive sums `T_n = sum Delta_k b_k` of independent Bernoulli variables. Remark 2.2: the Legendre transform of `l` is Vajda's tight lower bound on relative entropy in terms of total variation, i.e. the sharp form of Pinsker's inequality. `[V]`
- Owhadi, Scovel, Sullivan, McKerns, Ortiz, "Optimal uncertainty quantification", SIAM Rev. 55(2):271-345 (2013), doi:10.1137/10080782X, arXiv:1009.0679. Poses the exact extremal problem over the McDiarmid class (product measures, componentwise oscillations `D_i`, mean constraint) at the level of tail probabilities, reduces it to measures on a hypercube, and solves it in closed form for small dimension. Theorem 5.2 (two variables): the optimum is `0` if `a >= D_1 + D_2`, `(D_1 + D_2 - a)^2/(4 D_1 D_2)` if `|D_1 - D_2| <= a <= D_1 + D_2`, and `1 - a/max(D_1, D_2)` otherwise; when `D_2 + a <= D_1` "the optimal bound does not depend on D_2". `[V]` So at the tail level the extremal function is not additive in general, in contrast with the MGF level.
- Bentkus, "On Hoeffding's inequalities", Ann. Probab. 32(2):1650-1673 (2004), arXiv:math/0410159: tails of bounded-difference martingales dominated by a constant times the tail of an i.i.d. Bernoulli sum. `[V]` Bentkus, Israel J. Math. 158:1-17 (2007), doi:10.1007/s11856-007-0001-2 (separately Lipschitz functions on product spaces) and Pinelis, Electron. J. Probab. 11:1049-1070 (2006): Gaussian-tail refinements, cited by Rio; abstracts not accessible in this session. `[V, bibliographic only]`
- Sharp sub-Gaussian constant of a Bernoulli variable (Kearns-Saul): Berend and Kontorovich, "On the concentration of the missing mass", Electron. Commun. Probab. 18(3):1-7 (2013). `[V]` The explicit constant `(1-2p)/(4 ln((1-p)/p))` is `[unverified-from-memory]`.

**Is the exact-extremality statement in the literature?** The exact per-coordinate extremal function and the tensorized bound are in Rio's Lemma 4.1. That the bound is attained by additive two-level functions is immediate from the proof and from Rio's own additive Bernoulli example, but no sentence was found that states "the supremum of the MGF over the bounded-difference class is attained by additive two-level functions", and none for a fixed product measure where the supremum is restricted to the achievable values `p = mu_i(A_i)`. Searches: "sharpness McDiarmid inequality optimal bounded differences extremal moment generating function supremum attained sum independent Bernoulli separately Lipschitz"; Rio 2013 and its reference list; OUQ.

Reviewer's derivation showing why it is a corollary (and that the claim is correct):
1. In the Doob martingale of a product measure, the increment at step `i`, as a function of `x_i` for fixed past, has oscillation at most `c_i` and mean zero under `mu_i`. Hence the conditional MGF is at most `exp(Lambda_i)`, where `Lambda_i` is the supremum of `ln E_{mu_i} exp(lambda(g - E g))` over `g` with oscillation at most `c_i`. Induction gives `sum_i Lambda_i`; additive functions attain it because the MGF factorizes.
2. The map `g -> E exp(lambda(g - E g))` is convex. On functions measurable with respect to a finite partition it is maximized at a vertex of the cube, i.e. at `g = c_i 1_A`; uniform approximation by simple functions extends this to all bounded measurable `g`. So `Lambda_i = sup_A ln(p e^{lambda c_i (1-p)} + (1-p) e^{-lambda c_i p})`, `p = mu_i(A)`.
3. For atomless marginals (the torsion-angle case, where reference marginals have densities) all `p` in `[0,1]` are achievable and `Lambda_i = l(lambda c_i)`, Rio's function, in closed form.

Two corrections to the claim as worded: write `sup` rather than `max` over `A_i` for general marginals; and note that the result is specific to the MGF, since the tail-probability extremal problem has non-additive solutions (OUQ, Theorem 5.2). An ad hoc numerical check during this review (random 3 x 3 product measures, constrained maximization with restarts; not archived) never exceeded the additive formula and matched it to rounding error in five of six trials.

**Verdict.** KNOWN-IN-SPIRIT / FOLKLORE. The exact bound is KNOWN (Rio 2013, Lemma 4.1; two-point extremal from Hoeffding 1963); the attainment statement is implicit; the fixed-measure version was not found but is a short corollary.

**Confidence.** Medium-High.

### C7.4 Bobkov-Gotze equivalence

**Closest prior art.** Bobkov and Gotze, "Exponential integrability and transportation cost related to logarithmic Sobolev inequalities", J. Funct. Anal. 163(1):1-28 (1999), doi:10.1006/jfan.1998.3326. `[V]` As restated in the Kontorovich-Raginsky survey (full text checked): the sub-Gaussian estimate `log E exp(lambda(f - E f)) <= c lambda^2/2` holds for all 1-Lipschitz `f` if and only if `W_1(mu, nu) <= sqrt(2 c D(nu||mu))` for all `nu`; products with the weighted Hamming metric satisfy it with `c = (1/4) sum alpha_i^2` by rescaled Pinsker plus tensorization. `[V]` General convex-cost version: Gozlan and Leonard, "Transport inequalities. A survey", Markov Process. Related Fields 16:635-736 (2010), arXiv:1003.3852 (theorem number not checked). `[V, bibliographic]` Dependent tensorization: Djellout-Guillin-Wu, Theorem 2.11; survey Theorem 4.3. `[V]`

**Verdict.** KNOWN. **Confidence.** High. Note that the non-Gaussian sharp version is also known in the one-coordinate case: Rio's Remark 2.2 identifies the dual of `l` with Vajda's tight Pinsker bound.

### How to sharpen C7 into something new

1. **State it as an optimal-recovery (OUQ) theorem with Rio's function, and extend it to dependent references.** For a product reference with atomless marginals, given only `<Delta>_0` and the bounded differences `c`, the set of attainable values of `ln(Z/Z_0)` is exactly the interval from `-beta <Delta>_0` to `-beta <Delta>_0 + sum_i l(beta c_i)` (reviewer's derivation: scale the extremal residual about its mean to sweep the interval). This replaces `beta^2 c^2/8` by a closed form that grows only linearly in `beta` at low temperature (`l(10) = 6.70` against `12.5`). For Markov, tree or Dobrushin references the same two-point argument applied to the Wasserstein-matrix increments of Kontorovich-Raginsky gives `sum_i l(beta (Gamma c)_i)`; this combination was not found. For tree-structured `E_0`, compute `Gamma` exactly by dynamic programming instead of the worst-case `(1-theta)^-1`, and compare with Chatterjee's `(1-theta)^-1` scaling.
2. **Add the matching impossibility result and a localized version.** (a) Show that in the black-box bounded-difference model no estimator using polynomially many reference samples can certify `ln(Z/Z_0)` much more tightly than the sandwich, using the `exp(KL)` sample-size threshold for importance sampling: Chatterjee and Diaconis, Ann. Appl. Probab. 28(2):1099-1135 (2018), doi:10.1214/17-AAP1326 `[V]`; compare Jarzynski, Phys. Rev. E 73:046105 (2006), arXiv:cond-mat/0603185 `[V, abstract]`. (b) Apply the sandwich cell by cell in a branch-and-bound partition, with cell-local oscillations, so that the gap is second order in cell width; and replace `<Delta>_0` by a Monte Carlo estimate under the exactly samplable tree reference with a sub-Gaussian confidence radius `sqrt(sum c_i^2 ln(2/delta)/(2n))`, giving a probabilistically certified sandwich. A variance-sensitive (Bennett or Bernstein) refinement with exactly computed conditional variances would address the extensivity caveat.

---

## C8. Decomposition bounds and certified integration

### C8(a) Holder and tree-reweighted bounds; the temperature-rescaling form

**Closest prior art.**
- Wainwright, Jaakkola, Willsky, "A new class of upper bounds on the log partition function", IEEE Trans. Inf. Theory 51(7):2313-2335 (2005) (UAI 2002 version; arXiv:1301.0610). `[V]`
- Liu and Ihler, "Bounding the partition function using Holder's inequality", ICML 2011, pp. 849-856: weighted mini-bucket, giving upper and lower bounds on the partition function. `[V]` (Upper bounds use non-negative weights summing to one; that the lower bounds come from the reverse Holder inequality is `[unverified-from-memory]`.) The weighted or "power" sum `(sum_x f(x)^{1/w})^w` reduces to the sum at `w = 1` and to the maximum as `w -> 0`. Dechter's UC Irvine course slides (ICS-276, spring 2019, lecture 10, slide "The Power Sum and Holder Inequality", text extracted in this session) say: "'Temperature' interpolates between sum & max". `[V]`
- Minka, "Divergence measures and message passing", MSR-TR-2005-173: contains an appendix on Holder inequalities and an alternate proof of the tree-reweighted upper bound. `[V, table of contents]`
- Continuous variables: Bouchard and Lakshminarayanan, "Approximate inference with the variational Holder bound", arXiv:1506.06100 (2015). Theorem 1: `integral gamma_1 gamma_2 <= ||gamma_1 Psi||_{alpha_1} ||gamma_2/Psi||_{alpha_2}` for any positive pivot `Psi`, `1/alpha_1 + 1/alpha_2 = 1`; the log of the bound is convex in `log Psi`; applies "on discrete and continuous spaces"; generalizes Liu-Ihler; conjectured to contain TRW. `[V]`
- Search-based anytime bounds: Lou, Dechter, Ihler, "Anytime anyspace AND/OR search for bounding the partition function", AAAI 2017, doi:10.1609/aaai.v31i1.10667; "Dynamic importance sampling for anytime bounds of the partition function", NIPS 2017. `[V]`
- Lower bounds: Ruozzi, "The Bethe partition function of log-supermodular graphical models", NIPS 2012, arXiv:1202.6035 (Bethe partition function is a lower bound; resolves a conjecture of Sudderth, Wainwright, Willsky). `[V]`
- Statistical mechanics: convexity of the pressure in the interaction is the same inequality. Gallavotti and Miracle-Sole (Commun. Math. Phys. 5, 1967) state "The function Phi -> P_Lambda(Phi) is convex. The proof is standard". `[V, snippet]` Textbook treatments in Ruelle and in Friedli-Velenik: `[unverified-from-memory]`.
- SOS-based upper bounds on log-partition functions: Bach, "Sum-of-squares relaxations for information theory and variational inference", Found. Comput. Math. (2024), doi:10.1007/s10208-024-09651-0, arXiv:2206.13285. `[V]`

**Is the temperature-rescaling form known?** Yes. With `F_beta(E) = -(1/beta) ln integral exp(-beta E)`, Holder with exponents `1/rho` and `1/(1-rho)` gives

    F_beta(E1 + E2) >= F_{beta/rho}(E1) + F_{beta/(1-rho)}(E2),

which is the weighted mini-bucket bound with `f_r = exp(-beta E_r)` and weights `w = (rho, 1-rho)`; the limit `rho -> 1` gives the sum-max mini-bucket bound, and `beta -> infinity` gives the dual-decomposition bound `min(E1+E2) >= min E1 + min E2`. No source was found that writes it verbatim as "parts at colder temperatures" for molecular free energies (searched: "Holder inequality partition function sum of two Hamiltonians free energy lower bound rescaled temperatures"), but that is a change of notation.

**Verdict.** KNOWN. **Confidence.** High.

**How to sharpen.**
1. The known theory already optimizes over weights and over reparametrizations (cost shifting in Liu-Ihler; the pivot of Bouchard-Lakshminarayanan). A new result would need the continuous torus setting with a black-box part, for example a bound on the looseness of the optimized Holder split of `E_0 + Delta` in terms of the bounded differences of `Delta`, linking C8(a) to C7.
2. Prove a tightness or rate statement for the annealed decomposition on chains (for example, exactness when `Delta` is itself tree-decomposable on a compatible tree, and a quantitative gap otherwise) rather than restating the inequality.

### C8(b) Provable partition-function algorithms in protein design: do they bound the integral over a continuous voxel?

**Closest prior art.**
- K* (Lilien, Stevens, Anderson, Donald, J. Comput. Biol. 2005) and MinDEE/K* (Georgiev, Lilien, Donald, J. Comput. Chem. 2008). `[unverified-from-memory]` for bibliographic details.
- Ojewole, Jou, Fowler, Donald, "BBK* (Branch and Bound over K*)", J. Comput. Biol. 25(7):726-739 (2018), doi:10.1089/cmb.2017.0267: multi-sequence bounds; runtime sublinear in the number of sequences. `[V]`
- Jou, Holt, Lowegard, Donald, "Minimization-Aware Recursive K* (MARK*)", J. Comput. Biol. 27(4):550-564 (2020), https://pmc.ncbi.nlm.nih.gov/articles/PMC7185359. Main text checked: "Let E_X(c) be the minimized energy of a conformation c", and the partition function is the discrete sum `Z_X(s) = sum_c exp(-E_X(c)/RT)` (their Eq. 1); the guarantee is "within a (1 - epsilon) factor of the true partition function" so defined; the bounds are on minimized energies of sets of conformations. No integral over a continuous voxel appears in the main text (the supplement was not read). `[V]`
- Hallen and Donald, "Protein design by provable algorithms", Commun. ACM (2019), https://pmc.ncbi.nlm.nih.gov/articles/PMC6788629. Full text checked: a voxel's energy is "generally the continuously minimized energy"; "continuous entropy" appears only in a footnote as a modelling improvement that LUTE could accommodate. `[V]`
- Viricel, Simoncini, Barbe, Schiex, "Guaranteed weighted counting for affinity computation: beyond determinism and structure", CP 2016, LNCS 9892:733-750 (`Z*_epsilon`): guaranteed discrete partition functions by branch and bound with pruning of negligible mass. `[V]`
- Lowegard, Frenkel, Holt, Jou, Ojewole, Donald, PLoS Comput. Biol. 16(6) (2020), doi:10.1371/journal.pcbi.1007447 (FRIES, EWAK*). `[V]` OSPREY documentation (COFFEE): the SOFEA component gives up the epsilon guarantee because it discards nodes. `[V]` Childs, McBride, Donald, CCK*, bioRxiv 10.1101/2025.11.21.689740 (2025): the most recent K*-family paper found; K* is used as is. `[V, abstract]`
- Outside protein design, harmonic and mode-integration methods (mining minima and relatives) approximate well integrals without rigorous error bounds. `[unverified-from-memory]`

**Verdict.** That the K* family uses minimized energies and guarantees an epsilon-approximation of the resulting discrete sum is KNOWN (verified for MARK*; the Hallen-Donald review describes BBK* as giving "the same guarantees of accuracy as K*"). A rigorous two-sided bound on the integral of `exp(-beta E)` over a continuous rotamer or torsion voxel, inside a provable design algorithm: NO MATCH FOUND. Searches: "protein design partition function continuous rotamer voxel integral continuous entropy provable bound"; "Hallen Donald continuous entropy voxel integration EPIC LUTE CATS"; "configurational integral rigorous enclosure interval arithmetic torsional"; the MARK* and CACM full texts.

**Confidence.** Medium-High. The supplementary material of MARK* and the full BBK* text were not read, and an obscure thesis could exist.

**How to sharpen.**
1. Prove voxel-integral bounds that slot into the existing machinery: trivially `integral <= vol(voxel) exp(-beta E_min)`, and `integral >= vol(S) exp(-beta (E_min + delta))` for any certified subset `S` of the sublevel set `{E <= E_min + delta}`; refine both by curvature envelopes (C8(c)) and show the K*-style epsilon guarantee survives with these weights. That would be the first provable continuous-entropy-aware variant.
2. Exhibit a small explicit instance where the minimized-energy sum and the true integral rank two states differently (narrow deep well against broad shallow well), and show that certified integral bounds resolve it. This makes the gap concrete for the protein-design audience.

### C8(c) Non-asymptotic Laplace bounds and certified quadrature with Hessian envelopes

**Closest prior art.**
- Kasprzak, Giordano, Broderick, "How good is your Laplace approximation of the Bayesian posterior? Finite-sample computable error bounds for a variety of useful divergences", J. Mach. Learn. Res. 26(87):1-81 (2025), arXiv:2209.14992: closed-form computable bounds in total variation, Wasserstein-1 and an integral probability metric. `[V]`
- Katsevich, "The Laplace approximation accuracy in high dimensions: a refined analysis and new skew adjustment", arXiv:2306.07262; "The Laplace asymptotic expansion in high dimensions", arXiv:2406.12706; Katsevich and Spokoiny, arXiv:2509.07952 (2025). `[V]`
- Spokoiny, "Dimension free non-asymptotic bounds on the accuracy of high dimensional Laplace approximation", SIAM/ASA J. Uncertain. Quantif. 11(3):1044-1068 (2023), arXiv:2204.11038. `[V]`
- Explicit two-sided bounds on the integral itself: Inglot and Majerski, "Simple upper and lower bounds for the multivariate Laplace approximation", J. Approx. Theory 186:1-11 (2014), doi:10.1016/j.jat.2014.06.011; Majerski, arXiv:1511.00302; McClure and Wong (1983), cited by Spokoiny. `[V]`
- Verified integration: Mahboubi-Melquiond-Sibut-Pinote (C6(d)); LeanCert's certified partition bounds for definite integrals. `[V]` Interval-verified Gaussian-type integrals appear in 2026 computer-assisted proofs (for example arXiv:2609.37479 and arXiv:2608.11158, seen in search results only).
- Region-bound-driven exact sampling, which needs the same per-box bounds: Maddison, Tarlow, Minka, "A* sampling", NIPS 2014, arXiv:1411.0030. `[V]` Adaptive rejection sampling hulls: `[unverified-from-memory]`.
- Rate benchmark: Holzmuller-Bach (C8(d)): on the class of `C^2` integrands (`m = 2`) the optimal deterministic rate is `n^{-2/d}`, so envelope quadrature driven by Hessian bounds is rate-optimal on that class and cannot escape the curse of dimensionality without further structure.

**Verdict.** Non-asymptotic Laplace error bounds are KNOWN and active (2022-2025), but they target unimodal or locally quadratic integrands and mostly bound distances between distributions. The Gaussian or erf envelope idea (if the Hessian is sandwiched between diagonal bounds on a box, the Boltzmann factor is sandwiched between exponentials of separable quadratics whose box integrals are products of error functions) is FOLKLORE: each step is standard, and the global version `(2 pi/L)^{d/2} <= Z e^{f(x*)} <= (2 pi/m)^{d/2}` for `m I <= Hessian <= L I` is routinely used. No paper was found that applies it as a certified branch-and-bound quadrature for molecular partition functions. Searches: "rigorous verified enclosure integral exp(-f) interval arithmetic partition function normalizing constant Bayesian evidence branch-and-bound Taylor model quadratic bounds"; "configurational integral rigorous enclosure".

**Confidence.** Medium.

**How to sharpen.**
1. Combine certified enumeration of all wells (from the optimization branch and bound) with explicit two-sided Laplace bounds in each well (Inglot-Majerski, Katsevich) and envelope quadrature elsewhere, and prove an end-to-end error and cost theorem in terms of `beta`, curvature bounds and the number of wells.
2. Use the structure: integrate `E_0` exactly by transfer operators and envelope only `Delta`, so that the cost depends on the dimension through the bounded differences of `Delta` rather than through `M` directly. Exploiting structure of this kind is the natural way around the `n^{-2/d}` barrier.

### C8(d) Complexity lower bounds

**Closest prior art.**
- Bakhvalov, "On the approximate calculation of multiple integrals" (1959); English translation J. Complexity 31(4):502-516 (2015), doi:10.1016/j.jco.2014.12.003. `[V]` Survey: Novak, "Some results on the complexity of numerical integration", arXiv:1409.6714. `[V]`
- Hinrichs, Novak, Ullrich, Wozniakowski, "The curse of dimensionality for numerical integration of smooth functions", Math. Comp. 83:2853-2863 (2014), doi:10.1090/S0025-5718-2014-02855-X, arXiv:1211.0871; part II, J. Complexity 30(2):117-143 (2014), arXiv:1304.3372 (even for infinitely differentiable classes); "Product rules are optimal for numerical integration in classical smoothness spaces", arXiv:1604.00261. `[V]`
- **Holzmuller and Bach, "Convergence rates for non-log-concave sampling and log-partition estimation", J. Mach. Learn. Res. 26(249):1-72 (2025), arXiv:2303.03237.** Full text (first half) checked. For `f` in `C^m([0,1]^d)` with norm at most `B` and `L_f = log integral exp(f)`: with deterministic (also adaptive) evaluation points the optimal log-partition error is `Theta(B n^{-m/d})` (Theorem 7); with stochastic points the upper bound is `O(min{B n^{-m/d}, exp(C B n^{-m/d}) B n^{-1/2-m/d}})` (Theorem 9), with a lower bound `Omega(B n^{-m/d}) - d log(1+3B)` (Proposition 10); `B` plays the role of inverse temperature. `[V]` This is the most directly relevant contemporary statement: it concerns exactly the quantity (a log-partition function of a smooth non-log-concave energy) that MetricChain wants to certify.
- Ge, Lee, Lu, "Estimating normalizing constants for log-concave distributions: algorithms and lower bounds", STOC 2020, pp. 579-586, doi:10.1145/3357713.3384289, arXiv:1911.03043: an algorithm with about `d^{4/3} kappa + d^{7/6} kappa^{7/6}/eps^2` gradient queries and a lower bound of about `d^{1-o(1)}/eps^{2-o(1)}`. `[V]`
- Chewi, de Dios Pont, Li, Lu, Narayanan, "Query lower bounds for log-concave sampling", J. ACM (2024), doi:10.1145/3673651, arXiv:2304.02599. `[V]`
- He and Zhang, "On the query complexity of sampling from non-log-concave distributions", arXiv:2502.06200 (COLT 2025): tight `(LM/(d eps))^{Theta(d)}`. `[V]`
- Guo, Tao, Chen, "Complexity analysis of normalizing constant estimation: from Jarzynski equality to annealed importance sampling and beyond", arXiv:2502.04575 (ICLR 2026): oracle complexity about `d beta^2 A^2/eps^4` in terms of the action `A` of the annealing path; no lower bound in the abstract. `[V]`

**Verdict.** KNOWN. **Confidence.** High.

**How to sharpen.**
1. Do not restate the curse of dimensionality. Prove a structured lower bound for the class "tree-structured `E_0` known exactly plus `Delta` with bounded differences `c`", showing which parameter (for example `sum l(beta c_i)` or an effective dimension of `Delta`) replaces `d` in the exponent. Reviewer's remark: in the pure bounded-difference class, deterministic point queries carry no information about integrals, so the natural models are Lipschitz `Delta` (deterministic) or sampling access (randomized); see the C7 suggestion.
2. Give matching upper and lower bounds in that class; this would be a genuine addition to Holzmuller-Bach, whose classes are isotropic.

### C8(e) Stopping rules for certifying the largest partition function; best-arm identification; instance optimality

**Closest prior art.**
- *Protein design.* BBK* (above): a single provable upper bound covers many sequences at once, so provably suboptimal sequences are never evaluated individually. `[V]` My recollection of the mechanics (best-first search over partial sequences, with single-sequence bounds refined incrementally and re-queued until the top sequences are certified) is `[unverified-from-memory]`. Hallen and Donald, "COMETS (Constrained Optimization of Multistate Energies by Tree Search)", J. Comput. Biol. (2016), https://pmc.ncbi.nlm.nih.gov/articles/PMC4876521: provable multistate design with linear combinations of state energies. `[V]` FRIES/EWAK* and the OSPREY COFFEE tools (above). `[V]` These prove correctness of the output; no competitive or instance-optimality statement about refinement effort was seen in the abstracts and summaries checked.
- *Graphical models.* The problem "maximize over some variables the partition function over the others" is marginal MAP. Marinescu, Dechter, Ihler, "AND/OR search for marginal MAP" (UAI 2014); Lou, Dechter, Ihler, "Anytime anyspace AND/OR best-first search for bounding marginal MAP" (AAAI 2018); later anytime variants (AAAI 2017, IJCAI 2018, AAAI 2019). `[V]`
- *Stochastic best-arm identification.* Even-Dar, Mannor, Mansour, J. Mach. Learn. Res. 7:1079-1105 (2006); Kalyanakrishnan, Tewari, Auer, Stone, "PAC subset selection in stochastic multi-armed bandits" (LUCB), ICML 2012, pp. 655-662; Garivier and Kaufmann, "Optimal best arm identification with fixed confidence", COLT 2016, PMLR 49:998-1027. `[V]` Application to allocating molecular dynamics runs among binding poses: Terayama et al., Bioinformatics 34(5):770-778 (2018), doi:10.1093/bioinformatics/btx638. `[V]`
- *Non-stochastic best-arm identification.* Jamieson and Talwalkar, "Non-stochastic best arm identification and hyperparameter optimization", AISTATS 2016, PMLR 51:240-248, arXiv:1502.07943. Full text checked: arms are deterministic sequences converging to limits with envelopes `gamma_i(t)`; Successive Halving succeeds with budget `z = 2 ceil(log2 n) max_i i (1 + gamma^{-1}((nu_i - nu_1)/2))` (Theorem 1); without knowledge of the envelopes no certificate is possible; the case of known envelopes with a certified stopping rule is not analysed, and there is no formal lower bound. `[V]`
- *Deterministic refinement with competitive guarantees.*
  - Kirkpatrick, "Hyperbolic dovetailing", ESA 2009, LNCS 5757:516-527, doi:10.1007/978-3-642-04128-0_46: an interleaving strategy whose competitive ratio is within a logarithmic factor of optimal, applied to "input-thrifty" algorithms that minimize the input precision needed to decide a predicate. `[V, abstract]`
  - Tseng and Kirkpatrick, "Input-thrifty extrema testing", ISAAC 2011, LNCS 7074:554-563, doi:10.1007/978-3-642-25591-5_57: inputs are bit streams of increasing precision; if some algorithm decides with cost `c`, theirs uses `O(c lg min{c, n})`, and the logarithmic factor cannot be removed. `[V, abstract]` This is the closest match to "instance-optimal deterministic interval refinement".
  - Explorable uncertainty (a query reveals the exact value): Kahan, "A model for data in motion", STOC 1991, pp. 265-277, doi:10.1145/103418.103449; Khanna and Tan, "On computing functions with uncertainty", PODS 2001, pp. 171-182, doi:10.1145/375551.375577; Erlebach and Hoffmann, "Query-competitive algorithms for computing with uncertainty", Bull. EATCS 116:22-39 (2015) (witness sets; 2-competitive algorithms and matching lower bounds); Erlebach et al., arXiv:2101.05032 (round-competitive). `[V]`
  - Instance optimality of bound-driven top-k: Fagin, Lotem, Naor, "Optimal aggregation algorithms for middleware", J. Comput. Syst. Sci. 66:614-656 (2003), arXiv:cs/0204046: the threshold algorithm and the no-random-access algorithm are instance optimal within their classes, and the paper also proves impossibility results (its Theorem 6.4). `[V]` That the no-random-access algorithm halts by comparing upper and lower score bounds is `[unverified-from-memory]`.
  - Operators over functions that iteratively refine bounds: Denny and Franklin, "Adaptive execution of variable-accuracy functions", VLDB 2006, pp. 547-558. `[V, abstract]`
  - Best-first search optimality: Dechter and Pearl, J. ACM 32(3):505-536 (1985), doi:10.1145/3828.3830; Ibaraki, Int. J. Comput. Inf. Sci. 5(4):315-344 (1976), doi:10.1007/BF00998631 (best-bound search minimizes the number of decomposed subproblems). `[V]`

**Verdict.** KNOWN-IN-SPIRIT. Bound racing for partition-function ranking exists (BBK*, marginal MAP search); competitive analysis against the cheapest certificate exists for progressively refined inputs (Kirkpatrick; Tseng-Kirkpatrick), for reveal-the-value queries (explorable uncertainty) and for top-k aggregation (Fagin et al.); best-first optimality is classical. No source was found that (i) connects partition-function ranking in protein design to best-arm identification, or (ii) proves a competitive-ratio or instance-optimality theorem for deterministic certified-interval refinement in multi-state free-energy ranking. Searches: "best arm identification free energy calculations ligand ranking bandit"; "deterministic interval refinement anytime bounds identify maximum instance optimal competitive ratio"; "query-competitive computing with uncertainty minimum selection"; "marginal MAP anytime bounds"; "input-thrifty extrema testing".

**Confidence.** Medium. The theoretical-computer-science literature on computing with uncertainty is large and was only sampled.

**How to sharpen.**
1. Formalize the refinement-oracle model (each macrostate carries a nested sequence of certified intervals indexed by work; the algorithm sees only the current intervals), define the instance cost as the cheapest certificate in hindsight, and prove tight competitive bounds for a leader-and-challenger (LUCB-like) rule. Position the result against Tseng-Kirkpatrick, where a logarithmic factor is unavoidable for a disjunctive predicate; ranking is conjunctive, so a constant factor may be achievable, and settling that is the contribution.
2. Treat the actual objective: design scores are ratios of partition functions across states, so the certificate involves products and quotients of intervals. A competitive analysis for ratio objectives (and for epsilon-relaxed stopping) was not found.

---

## Cross-cutting observations

- **Where the searches came up empty.** (1) Rigorous bounds on the integral of the Boltzmann factor over continuous torsion voxels with a non-decomposable energy term. (2) The free-energy sandwich phrased as an exact attainable interval, with Rio's function, including dependent references. (3) Exact rational, proof-assistant-checked certificates for torsion-space molecular energies. (4) Rates for chain-sparse trigonometric SOS hierarchies. (5) Competitive-ratio results for certified ranking of partition functions.
- **Where the claims should be toned down.** C6(a), C6(d), C7.2, C7.4, C8(a) and C8(d) are established results; C7.1 and C7.3 are short corollaries of them. Presenting any of these as new would not survive a referee who knows Rio 2013, Kontorovich-Raginsky 2017, Liu-Ihler 2011 or Holzmuller-Bach 2025.
- **Strongest contemporary competitors to cite and beat.** Bach-Rudi 2023 (torus SOS rates); Kuznetsov-Sahinidis 2025 (deterministic LJ optimization); LeanCert 2026 and `leanprover/sos` 2026 (Lean certificates); Gourgoulias et al. 2020 (concentration-based information bounds); Holzmuller-Bach 2025 (log-partition complexity); MARK* 2020 and BBK* 2018 (provable partition functions); Tseng-Kirkpatrick 2011 (competitive refinement).

## Search log (main queries by topic)

- **C6(a).** alpha-BB and its generalizations (author and title queries); "Convergence rate of McCormick relaxations"; "cluster problem" constrained and unconstrained; Kazazakis/Nerantzis-Adjiman; "Trigonometric convex underestimator Fourier space"; deterministic global optimization of Lennard-Jones clusters 2025-2026; Maranas-Floudas, Klepeis-Floudas, Lin-Stadtherr.
- **C6(b).** Bach-Rudi; Laurent-Slot and Baldi-Slot rates; "trigonometric polynomial optimization sparse moment-SOS torus 2024-2026"; exact SOHS certificates (univariate and multivariate); correlative sparsity rates; complex moment hierarchy.
- **C6(c).** SOS / Lasserre with "molecular conformation", "protein folding", "distance geometry", "Lennard-Jones", "torsion", "side-chain dihedral"; algebraic kinematics (Wampler-Sommese, Emiris-Mourrain); SOS inverse kinematics and certified collision-free regions; sums of rational functions; moment methods for energy minimization; Lean and Lennard-Jones.
- **C6(d).** Repository and Reservoir pages for `girving/interval`, `alerad/leancert`, `leanprover/sos`, `minusgix/flean`; Lean Zulip archives ("Verified software floating point", "An interval tactic for constant real inequalities", "LeanCert - Verified Computation & Interval Arithmetic"); Mathlib `polyrith` status; CoqInterval, Flyspeck, PVS branch and bound, ValidSDP; FloatLib, DSLean.
- **C7.** McDiarmid sharpness and extremal problems (Rio, Bentkus, Pinelis, OUQ); concentration for dependent variables (Kontorovich-Ramanan, Kontorovich-Raginsky, Chazottes et al., Kulske, Chatterjee); Bobkov-Gotze and transport inequalities; free energy perturbation with "bounded differences", "McDiarmid", "Hoeffding"; "Gibbs-Bogoliubov" two-sided and second-order bounds; two-sided Bogoliubov inequality in molecular simulation; mean-field error bounds; Jensen-gap bounds; information inequalities for UQ; importance-sampling sample size.
- **C8(a).** Wainwright-Jaakkola-Willsky; Liu-Ihler and the power sum; variational Holder bound; Minka's Holder proof of TRW; Holder inequality for sums of Hamiltonians at rescaled temperatures; convexity of the pressure; AND/OR search bounds; Bethe lower bound.
- **C8(b).** BBK*, MARK*, K*, `Z*_epsilon`, FRIES/EWAK*, COMETS, OSPREY documentation, CCK*; "continuous entropy" and "voxel integral" in protein design; rigorous enclosures of configurational integrals.
- **C8(c).** Kasprzak-Giordano-Broderick; Katsevich; Spokoiny; Inglot-Majerski; verified integration; rigorous enclosures of `exp(-f)` integrals by interval arithmetic or branch and bound; A* sampling.
- **C8(d).** Bakhvalov; Hinrichs-Novak-Ullrich-Wozniakowski; Ge-Lee-Lu; Chewi et al.; Holzmuller-Bach; query complexity for non-log-concave sampling and normalizing constants 2024-2026.
- **C8(e).** Best-arm identification (LUCB, successive elimination, track-and-stop, non-stochastic); bandits for free-energy or pose ranking; marginal MAP anytime bounds; query-competitive computing with uncertainty; input-thrifty algorithms and hyperbolic dovetailing; instance-optimal top-k aggregation; variable-accuracy operators; optimality of A* and best-bound search.

## Limitations of this check

- Abstract-level verification only for many items; full texts were read for Rio 2013, Kontorovich-Raginsky 2016, Wampler-Sommese 2011 (relevant passages), Gourgoulias et al. 2020 (first two thirds), Jamieson-Talwalkar 2016, Holzmuller-Bach 2025 (first half), MARK* (main text), the Hallen-Donald review, and Amice et al. 2022.
- Not accessible in this session: the abstract of Bentkus 2007 (paywall redirect), the ICML 2011 PDF of Liu-Ihler (404; content confirmed through secondary sources and course slides), the bioRxiv full text of CCK* (rate limit; abstract obtained through the bioRxiv API).
- Items tagged `[unverified-from-memory]` should be checked before being cited.
- Web search was general-purpose; no systematic database query (MathSciNet, zbMATH, Scopus) was run.
