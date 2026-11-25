# MetricChain — Theory Report

**Foundational theory, formal guarantees and certificate paradigms for fixed-sequence articulated
SE(3) heteropolymer chains.**

Scope: mathematics, statistical physics, general-purpose certified computation, synthetic
evaluation.  No biological sequence engineering, no target-specific optimisation, no experimental
data.  Every theorem marked **[V]** is machine-checked in Lean 4 + Mathlib (`proofs/`, zero
`sorry`, axioms `propext`, `Classical.choice`, `Quot.sound` only); **[P]** marks statements proved
here on paper only; **[K]** marks known results that are cited.  The falsification status of every
claim is in `experiments/falsify_conjectures.py`; refuted or repaired claims are in
`DEAD_ENDS.md`.  Literature checks with search logs are in `prior_art/`.  All benchmark numbers
quoted below (B1–B13) are from one run of `experiments/separation_benchmarks.py` (seed 7), whose
output is stored in `benchmarks_output.txt`.

---

## 0. Summary

### 0.1 What changed relative to the provisional formulation

1. **The residual is an element of an envelope class, not "arbitrary".**  A non-decomposable
   correction `Δ_res` enters every guarantee only through an *envelope*
   `d : X × X → ℝ` (zero on the diagonal, triangle inequality, possibly asymmetric) with
   `Δ(x) − Δ(y) ≤ d(x, y)`, plus its values at evaluated *anchors*.  Global bounds, per-site
   differential envelopes and certified Lipschitz constants are all instances (§2.3).
2. **Certification is separated from search.**  All guarantees are statements about
   *certificates* checked by small verified kernels with exact rational arithmetic (§6); solvers
   are untrusted.
3. **Two semirings, parallel certificate rules.**  The leaf (reparameterise / factorise), branch
   and dominate rules exist both for minimum energies (`(min,+)`) and for partition functions
   (`(+,×)`), with dominance acquiring the temperature-dependent factor `1 + e^{−βγ}` (§3.1, §6).
   In the first phase the decomposition rule was a kernel rule only in `(min,+)` (its Hölder
   analogue, §3.5, is one-sided); the second phase added two-sided *cut* and exact *elimination*
   rules to the partition kernel (§11.8), without which it has no sub-exponential exact
   certificates even on chains (§3.4).
4. **Weight-domain and rational-atlas semantics.**  Partition-function certificates live in the
   domain of rational Boltzmann factors; torsion circles are covered by four rational charts
   `t ↦ ((1−t²)/(1+t²), 2t/(1+t²))`, `|t| ≤ 1/2`, so checkers need no transcendental functions (§5).

### 0.2 Results at a glance

| # | Result | Lean | Novelty assessment after prior-art review |
|---|---|---|---|
| A1 | **Contact-set theorem**: `x` can be optimal for some admissible residual ⇔ `E₀(x) ≤ E₀(y) + d(y,x) ∀y` | `robust_minimizer_iff` **[V]** | **known in substance**: solvability of a system of difference constraints (no negative cycle) = non-empty `c`-subdifferential for the cost `c = d` = "possibly optimal" under interval-type uncertainty (`reviews/R1` Q3, `prior_art/L5` P3); the formulation with a white-box part next to the envelope class was not found in the provable-design literature |
| A2 | **Sharp-minimum theorem**: `x` optimal for every admissible residual ⇔ `d(x,y) ≤ E₀(y) − E₀(x) ∀y` | `robust_certified_iff` **[V]** | **known in substance**: tightness of the shortest-path closure (Kantorovich–Rubinstein extremal function); sharp minimum of modulus 1 ⇔ minimiser under every 1-Lipschitz perturbation (Polyak 1979; Burke–Ferris 1993); "necessarily optimal" |
| A3 | **Query-model theorem**: with evaluated anchors, `x` can be optimal ⇔ contact ∧ `E₀(x)+L(x) ≤ E₀(y)+U(y) ∀y` (`L, U` McShane envelopes) | `robust_minimizer_with_anchors_iff` **[V]** | **rediscovery** for `E₀ ≡ 0`, symmetric `d`: Malherbe–Vayatis 2017, Lemma 8 ("potential maximizers"); in general A1 on the one-point extension of the envelope (minimal simple temporal network, §11.1).  iMinDEE's pruning interval is the special case of a one-sided bound and one evaluated conformation; the statement with a white-box part was not found in the provable-design literature |
| A4 | **Exact robust interval** for `min(E₀+Δ)` and for `Z_β(E₀+Δ)`: bracket between the two McShane envelopes (every `β ≥ 0`), and every value in between is attained by an admissible residual | `robust_min_bracket`, `robust_partition_bracket`, `robust_min_interval_exact`, `robust_partition_interval_exact` **[V]** | **known**: McShane 1934 / semi-Lipschitz extension; minimal network of a simple temporal network (Dechter–Meiri–Pearl 1991); the interval is the set of consistent values of optimal recovery (Micchelli–Rivlin; Sukharev; Novak 1988) |
| A5 | **Witness-size lower bound**: an ε-certificate *whose incumbent is an evaluated anchor* must evaluate the residual on every state with gap `< (1−κ)σ − ε` | `anchor_necessary`, `anchor_card_lower_bound` **[V]** | **rediscovery**: the `(1 − Lip f/L)` adversary of Bachoc–Cesari–Gerchinovitz 2021, Thm 2, at the finest scale only; superseded by the covering characterisation G1 below |
| A6 | Energy window is the exact limit with global bounds only | `energy_window_exact` **[V]** | known in spirit (energy-window DEE); exactness statement makes the "bottleneck" information-theoretic |
| A7 | Local differential envelopes ⇒ global envelope; differential DEE is sound | `admissible_of_single_site`, `differential_dee_sound` **[V]** | MinDEE range terms are a special case; general form not found |
| A8 | Goldstein = exact dominance margin; gauge invariant; = gauge-optimal Desmet | `goldstein_isLeast`, `goldstein_gauge_invariant`, `desmet_optimalGauge` **[V]** | **known/folklore** (Shekhovtsov 2014/2016); negative answer to the seeded "dual-reparameterised pruning" conjecture *for single-site, context-independent tests only* (multi-site improving maps do depend on the gauge, §2.2) |
| D1 | **Dominance transport / thermal DEE**: `Z(A) ≤ e^{−βγ} Z(S)`; pruning changes `ln Z` by `≤ ln(1+e^{−βγ})` (`ln(1+m e^{−βγ})` for an `m`-to-one map) | `partition_transport`, `freeEnergy_prune_bracket`, `partition_prune_bracket_fibers`, `thermal_dee` **[V]** | inequality folklore; as a certificate rule for partition functions: no match found |
| D2 | **Free-energy sandwich** `−β⟨Δ⟩₀ ≤ ln(Z/Z₀) ≤ −β⟨Δ⟩₀ + β² Σc_i²/8` **for a product reference** (for an arbitrary reference only the Hoeffding form `β²(b−a)²/8`, `b−a ≤ Σc_i`, holds: `DEAD_ENDS.md` D14); the worst residual in the bounded-difference class is additive and two-level; `1/8` is optimal | `bounded_differences_sandwich`, `bounded_differences_sandwich_any_reference`, `correlated_reference_counterexample`, `exists_two_level_worst_residual`, `mcdiarmid_no_better_constant` **[V]** | **known**: Jensen + McDiarmid; Rio 2013 for the sharp function; the additive two-level extremal for a fixed product measure is in Alon–Boppana–Spencer 1998 and Bobkov–Houdré–Tetali 2006 (`prior_art/L6` T2, which corrects the earlier "implicit in the literature"); formalization new.  For dependent references the extremal residual is *not* additive in general (`DEAD_ENDS.md` D25) |
| D3 | **Partition-function kernel** with leaf/branch/thermal-prune rules; enclosure of the real `Z`, end to end from interval energy tables | `zverify_sound`, `zverifyTop_sound`, `Z_encloses_partitionFn`, `certified_partition_of_intervals` **[V]** | verified or proof-producing checkers exist for exact weighted and unweighted model counting (CPOG, Lean 4), for approximate counting with probabilistic guarantees (Tan et al. 2024: Isabelle/HOL with CakeML), for solution enumeration (McCreesh et al. 2026: VeriPB/CakePB) and for exact stochastic-SAT values through two-sided implication proofs (Cheng–Luo–Jiang 2024); a verified checker for *deterministic two-sided bounds on a weighted sum* with this rule set was not found (state of the field as read by the science division, `SCI-REV-0006` W1; our earlier wording, "exact model counting only", was out of date) |
| D4 | **Voxel enclosure**: continuous Boltzmann integrals → rational kernel, with the volume (entropy) factor, end to end for pairwise torsion energies on product voxels (table enclosures + outward-rounded factors + accepted certificates ⇒ two-sided bound on the integral); separable (second-order) envelopes factor an `M`-dimensional voxel integral into `M` one-dimensional ones | `voxel_boltzmann_bounds`, `pairwise_voxel_weight_bounds`, `certified_torsion_partition`, `separable_voxel_bounds` **[V]** | `K*`-family algorithms bound a sum of minimised voxel energies; rigorous voxel-*integral* bounds inside a provable design algorithm: no match found (rigorous enclosures of integrals as such are standard verified numerics) |
| D5 | Hölder decomposition with temperature rescaling | `partitionFn_holder`, `freeEnergy_holder` **[V]** | **known** (weighted mini-bucket) |
| C1 | Hoffman–Wielandt and von Neumann trace inequality (real symmetric) | `hoffman_wielandt` **[V]** | **classical** (1953); formalization |
| C2 | Trace-enhanced spectral obstruction: `min_X ‖D̂ − Δ(X)‖²_F ≥ 4 Σ_{k>r} λ_k² + (4/(r+1)) (Σ_{k>r} λ_k)²` | `rank_psd_trace_obstruction`, `sstress_lower_bound` **[V]** | **known** with these constants (Sonthalia et al. 2021; K-identity in Tsang–Pereira 2016); machine-checked here down to Hoffman–Wielandt (we know of no earlier formalization) |
| C3 | Cycle-holonomy obstruction; SE(3) translation holonomy with lever arms | `norm_holProd_le_sum`, `norm_holTrans_le` **[V]** | triangle bound **known** (Lerman–Shi 2022, Lemma 1); a sharp non-abelian Hodge-type bound is open |
| C4 | **Finite-angle torsion → RMSD**: exact coaxial cost `2S − 2√(S² − 4 I_A I_B sin²(φ/2)) ≤ 4 min(I_A,I_B) sin²(φ/2)`; chain rule; envelope for Lipschitz residuals invariant under a group of motions containing the axis rotations (`SE(3)` or `E(3)`), down to membership in the kernel's residual class | `exists_coaxial_angle`, `coaxial_cost_le_min`, `rigidWithin_torsion_chain`, `residual_torsion_chain_in`, `residual_torsion_move_uniform`, `verifyR_sound_invariant` **[V]** | small-angle content classical (Pitzer–Gwinn; Eckart); the closed form is the residual of a planar weighted Procrustes problem, `2(S − |I_A + I_B e^{iφ}|)` (classical), and the chained bound *without* re-superposition is a published certificate in robot motion planning (Schwarzer–Saha–Latombe 2005, Lemma 2; `SCI-REV-0006` W10); as a bound on the Kabsch cost of a torsion move, with the chained form: not found |
| B1 | Outward rounding, rational intervals, certified `exp`, rational circle atlas | `Core/Rounding.lean` **[V]** | infrastructure; verified interval libraries exist (LeanCert, girving/interval) |
| E1 | **Master Soundness Theorems** for the tropical, residual and sum–product kernels; the top-level kernels check their own side conditions (consistency of interval anchor data — which is exactly non-emptiness of the residual class — and nonnegative factors) | `verify_sound`, `verifyITop_sound`, `IProblem.consistent_iff_nonempty`, `certified_gap`, `zverifyTop_sound` **[V]** | the residual kernel certifies a bound for *every* residual of an envelope class consistent with interval anchor data and decides non-emptiness of the class; no counterpart was found — every proof-logging system read certifies a statement about one instance (a comparison of statements plus an absence in searches, not a proof of novelty; `SCI-REV-0006` M1).  For the pairwise kernel: no proof logging for cost-function-network / MAP / DEE solvers was found (toulbar2 1.0.0 has none), but its ingredients have verified checkers in the pseudo-Boolean setting (linear-programming bounds through Farkas certificates, dominance; checking within a factor 20 of solving time, Koops et al. 2025; importable into Lean 4, PBLean 2026) and certificates made of equivalence-preserving transformations exist for MaxSAT (Py–Cherif–Habet 2022, unverified checker); whether a native format is cheaper has not been measured (§6.4; `prior_art/L1` §C4(ii); `SCI-REV-0006` W2 — our earlier wording made checking cost the reason for native certificates) |
| E2 | Exponential separation: sum-free certificates need exactly `2^m` visited leaves on `m` frustrated triangles, `2m` suffice with `sum`; the separation persists for node counts (`m ≥ 4`) and for the full description length (`sum` nodes charged for the sub-instances they embed: at most `147 m³` against at least `2^m`, `m ≥ 21`); LP gap of the triangle | `sumFree_exponential`, `sumFree_tight`, `sum_linear`, `sum_rule_separation`, `sum_rule_separation_size`, `sum_rule_separation_dataSize`, `triangle_no_leaf_certificate` **[V]** | **known phenomenon** (Basu et al. 2023; Jeroslow 1974); formalized for this kernel incl. DEE steps |

The honest reading of the last column, after an independent referee report (`reviews/R1`) and six
literature checks (`prior_art/L1`–`L6`): the *mathematical* content of the individual statements
above is elementary, classical, or already in print.  A1–A5 are the standard theory of difference
constraints / Lipschitz extension / optimal recovery, stated for a white-box part next to the
envelope class (A3 and A5 are rediscoveries of published statements); A8, D2, D5, C1, C2, C3, E2
are known results.  What this part of the program contributes is (i) the envelope *formulation* —
a known additive part next to a difference-constraint class — as the interface between explicit
models and non-decomposable residuals; (ii) temperature-aware dominance and voxel enclosures as
*certificate rules* (D1, D3, D4); (iii) finite-angle torsion-to-RMSD certificates and the
resulting envelope for SE(3)-invariant residuals (C4); and (iv) a machine-checked certificate
algebra and library covering all of it, including formalizations (to our knowledge new in Lean)
of several known results.  The results of the later research phases (§§10–12; rows G1–G24 of §10), which
were developed in response to that assessment and were reviewed by further independent
referees (`reviews/R2` – `R9`), are classified separately there; §0.3 is a map of them.

### 0.3 The later phases at a glance (details, proofs and labels in §§10–12)

| topic | main statements | where | status |
|---|---|---|---|
| certification geometry | certificates = coverings by slack balls; exponents on product landscapes at zero and finite temperature; hardness; best-first search | §§11.1–11.9 | machine-checked cores; refereed (R2) |
| query complexity of all algorithms | lower bounds for every randomised algorithm (dips, generalised dips), thresholds, the accuracy diagram on the cube, the exact exponent with a hint | §11.10 | one-shot lower bounds machine-checked; the rest paper proofs, refereed (R3, R4) |
| second-order and correlated uncertainty | quadratic law for dense second-order classes; classes that are linear in features; pair-distance profiles for chains and their kernel | §§11.7, 11.12, 11.17 | inequalities and kernel machine-checked; refereed (R6, R_P) |
| algorithms **without a hint** on the cube | non-adaptive exponent `θ_na` (Monte Carlo is optimal); adaptive exponent = the hinted one, at extensive and at every bounded accuracy | §§11.16, 11.18, 11.19 | recursion and bracket algebra machine-checked; algorithms paper proofs, refereed (R5, R7, R8) |
| a **known part** (field) | single-letter exponents; the right sample is flat in the order parameter; the hardest instance is additive, not the zero residual; a new asymptotic isoperimetric theorem | §11.20 | paper proofs, refereed (R9); shift identity machine-checked |
| the common structure | the shear law; every game function yields a pair, and the level recursion converges | §11.21 | machine-checked |
| **chains in the thermodynamic limit** | a convex limit shape for profile sets of bridges; certificate sizes of bridges converge to its covering number off a countable, unidentified set of accuracies; every limit point of the certificate sizes of all walks at `(L, ε₁) = (1, ½)` lies between 116 and 3 627 (first version: "bounds `50 … 3 627`"); rate exactly `N^{-1/3}` at the compact end of the shape, `N^{-1/2}` or better at interior points | §11.22 | abstract limit theorems machine-checked; lattice lemmas paper proofs checked with independent code; reviewed by the Scientific Discovery Division (SCI-REV-0002: no false theorem; headline reworded; lower bound raised from 50 to 116 with the section's own tools); conjecture for unrestricted walks |
| a **known part with interactions** (a function of the type: mean-field models) | by symmetry alone, for every `n`: flat-histogram sampling is optimal non-adaptively and the flat-histogram instance is the hardest symmetric one; a single-letter theorem for every rate function; with two phases the extremal perturbations are shells in the barrier class, beyond a small accuracy on part of the coordinates only; ferromagnets are never harder than the uniform cube, also for adaptive algorithms without a hint | §11.23 | the every-`n` lower bounds machine-checked; paper proofs, numbers re-computed with independent solvers; **refereed (R10; two major and fifteen minor findings applied)**; adaptive exponent open beyond ferromagnets up to the junction with the uniform cube |
| **rounds of adaptivity** | a ladder with `L` rungs is `L` rounds, so the adaptive exponent is approached to within any `η > 0` with a number of rounds independent of `n` (whether a fixed number of rounds reaches it is open); two rounds beat every fixed sample (`≤ 0.624a` at `u = 1`) and provably do not reach the adaptive exponent (`≥ 0.359a = 1.37h`): a hierarchy with at least three levels | §11.24 | the two-round indistinguishability lemma machine-checked; paper proofs checked against Theorem 11.56 and re-computed by the coordinator; refereed (Scientific Discovery Division, SCI-REV-0003): no critical finding, one major (the cost bound of the batched schedule held on the good event only; a stopping rule was added) and nine minor points, all corrected; the division's strengthening — the two-round lower bound for the expected cost at one instance — machine-checked (its file, compiled here); three rounds open |
| **slices** (every known part that is a function of the type, against the uniform cube) | among pairs of binary variables with a given odds ratio the mutual information is largest at uniform marginals; hence inside every type class binary centres suffice and the game function is dominated by the cube's, with equality for the class `½`: **for fixed samples, and with a hint at instances that are functions of the type, no function-of-type known part has a larger exponent than the uniform cube, and without a field and with one phase — antiferromagnets included — these two exponents are the cube's**; for adaptive algorithms without a hint the comparison is proved for ferromagnets and fields only (§§11.20, 11.23) and is otherwise a conjecture (two letters; with three or more letters the comparison fails at small slopes: a known part that removes letters can make the problem harder); algorithms reduce to type classes (`n + 1` terms, each with a constant known part) | §11.25 | the coordinator's paper proofs, checked numerically; deterministic core of the reduction machine-checked; **reviewed by the Scientific Discovery Division (SCI-REV-0001: the mathematics sound; the headline, which first claimed all exponents, narrowed to two of three; a proof step at negative accuracies supplied)**; the reading as exponents rests on §11.23; the adaptive exponent of a single type class is a conjecture |
| **heteropolymer product landscapes** (a fixed sequence of site types, any alphabets, single-site known parts, envelopes that need not be symmetric) | the sketch of §11.20 is a chain of theorems: joint-type-stratified sampling is optimal among fixed samples for every `n`; the three exponents are `R̂(e) = max_t[Σ_jλ_jF*_j(t) − te]` (hinted at the hardest instance = adaptive without a hint), `θ_na = R̂∘S^{−1}`, with one common slope for all site types; **the site function is a Rényi capacity, `F*_j(t) = (1−t)C_t`, of the channel "vertex of the site's Lipschitz polytope ↦ its Gibbs law", so — asymptotically, in the worst case over the class — a fixed sample of `e^{nθ}` points certifies the accuracy rate `E_sp(θ)` (the sphere-packing exponent; `0 < θ < a`) and adaptivity gains exactly `θ` (for `0 < θ < h`)**; exponents of site types do not add; with three or more letters `F*` need not be concave and the uniform site law need not be the hardest | §11.26 | the general inequalities behind the every-`n` lower bounds and two elementary steps of the Rényi form machine-checked (the product step for several site types is on paper); paper proofs by a workstream, the upper bounds by transfer of Theorems 11.78(b), 11.52, 11.54, 11.64; every number re-computed by the coordinator with an own implementation; **Theorems 11.99 and 11.101 reviewed by the Scientific Discovery Division (SCI-REV-0005): proved — the adaptive upper bound after two gaps in its written proof were closed**; nothing of the nested algorithm simulated |
| evaluations **together with local ensemble-averaged data** (a question of the Scientific Discovery Division) | on the cube class, free knowledge of all `k`-body marginals of the Gibbs measure changes neither the adaptive exponent (their theorem) nor the non-adaptive one (ours), for `k = o(n/ln n)` | §11.27 | a short paper proof using their orthogonal-array lemma; exact enumeration at `n = 7`; not refereed; zero known part only |
| **observable free energies**: the range of a ratio `Z(A)/Z(B)` of two macrostate weights over the residual class (a question of the Scientific Discovery Division) | an exact dual: a transport plan with gains from `B` to `A` certifies the ratio, and only the constraints from `B` to `A` matter; closed forms — one state; the two sides of a threshold on the cube (the extremal residual is the maximal field; `±n·ln cosh(u/2)` for the two halves); **every pair of a lower and an upper set when the known part is submodular (the two uniform fields are extremal: the sandwich theorem of the Scientific Discovery Division)**; one-coordinate macrostates on product spaces; a max–min formula with transport costs at the exponential scale | §11.28 | the certificate half machine-checked (`MacroRatio.lean`); the sandwich theorem machine-checked by that division, its file adopted (`MonotoneSandwich.lean`); strong duality and the reductions on paper, checked numerically (harness XXIII); **reviewed and replicated by that division (SCI-RES-0005): Theorems 11.105–11.107 stand**; the range only — nothing on the number of evaluations; prior art (six searches by that division at summary level): for a separable envelope Theorem 11.105 is the classical closed form of the density-ratio class |
| a **one-body marginal oracle with a field** (the second question of that division) | **for the class nothing changes**: with a free exact one-body oracle the adaptive exponent is `R^max` and the non-adaptive one `θ_na`, for every `n` — the hard instance is a mixture of two product ensembles whose one-body averages equal those of the same mixture with a hidden dip (the division's compensation lemma); **at a given instance the oracle helps**: at the zero residual the exponent drops, by between `5.3 %` and `7.6 %` at `p = ¼`, `u = 1`, `e = 0.02` and by most of it for strong fields (a bracket; the exact value is open) | §11.29 | our criterion (paper proof, brute force on `Q_10`); **the two consequences are the division's theorems (SCI-RES-0006), which replaced two conjectures of ours — one true for another reason, one with a wrong formula and two wrong numbers**; every step re-derived and the finite statements and numbers replicated with our own code (harness XXIII.7); not machine-checked |
| **sup-norm (box) classes around a known part whose Gibbs measure can be sampled exactly** (the division's request P-T3: a certificate theory for remainders that are small in a typical norm) | the cost of certifying `ln Z` is `Θ((Z(lo)/Z(r) − 1)/ε)` — the Boltzmann factor of the free-energy distance from the instance to the floor of the class, divided by the accuracy — with matching bounds for all randomised algorithms, **independent of the size of the system**; the Gibbs–Bogoliubov side costs `w² ln(1/δ)/(2ε²)` samples; deterministic certificates cost the entropy of the known part; minima do not share the benefit; a sup-norm bound caps the cost of every first-order class; the typical norm sets the width of the bracket, the floor sets the number of samples below which nothing is certified | §11.30 | the dip and bump bounds, the detection lemma, the spot check on every class inside the box, and the lower bound for all algorithms machine-checked (`BoxClass.lean`); the rest elementary paper proofs; harness XXIV, DEAD.28; not refereed; elementary and classical in spirit — no novelty claimed beyond the placement; prior art at search-summary level (`docs/prior_art/L10_box_classes.md`) |

What none of this establishes is listed in §8; the strongest open questions are in §12 and,
in priority order, in `docs/RESEARCH_LOG.md` ("Resume here").

---

## 1. Setting and notation

A fixed-sequence chain with `L` units has discrete basin labels `b_i ∈ B_i` and torsions
`θ_i ∈ C_i(b_i) ⊂ T^{d_i}`.  After voxelisation of the continuous boxes (states = (basin, voxel)
pairs) a configuration is `x = (x_1, …, x_n) ∈ ∏ D_i` and

    E(x) = E₀(x) + Δ(x),        E₀(x) = Σ_i h_i(x_i) + Σ_{i≠j} J_ij(x_i, x_j)   (+ 3-body terms),

with `E₀` explicit and `Δ` the non-decomposable residual.  `Z_β(E; S) = Σ_{x∈S} e^{−βE(x)}` and
`F_β = −β^{-1} ln Z_β` (`Core/Basic.lean`).  Continuous integrals are connected to these finite
sums by the voxel enclosure theorem (§3.4); nothing in §§2–3 depends on how the finite
configuration space arose.

An **envelope** is a function `d` with `d(x,x) = 0` and `d(x,z) ≤ d(x,y) + d(y,z)`; a residual
is **admissible** if `Δ(x) − Δ(y) ≤ d(x,y)` for all `x, y` (`IsEnvelope`, `Admissible`).
Symmetry is not required: asymmetric envelopes encode one-sided differential information.

| information about `Δ` | envelope |
|---|---|
| `lo ≤ Δ ≤ hi` | discrete: `d(x,y) = (hi−lo)·[x≠y]` (`discreteEnvelope`) |
| single-site differential envelopes `Δ(x[i↦a]) − Δ(x) ≤ δ_i(a, x_i)` | site-additive: `d(x,y) = Σ_i δ_i(x_i, y_i)` (`siteEnvelope`, `admissible_of_single_site`) |
| bounded differences `c_i` | weighted Hamming: `δ_i(a,b) = c_i [a≠b]` |
| certified Lipschitz constants `Λ_i` in torsion space | `d = Σ_i Λ_i · dist_T(θ_i, θ'_i)` (and sums with the above) |

`admissible_of_single_site` **[V]** is the local-to-global step: single-site envelopes imply
admissibility for the site-additive envelope (induction on the set of differing sites).  Raw
differential tables must be transitively closed first (`DEAD_ENDS.md` D3).

---

## 2. Direction A — dominance, gauges and residual envelopes

### 2.1 Dominance transport

**Theorem 2.1 (transport) [V].**  Let `A, S` be finite sets of configurations, `T : A → S`
injective, `E(Tx) + γ ≤ E(x)` on `A`, `β ≥ 0`.  Then `Z_β(A) ≤ e^{−βγ} Z_β(S)`.  If moreover
`A ∩ S = ∅`,

    Z_β(S) ≤ Z_β(A ∪ S) ≤ (1 + e^{−βγ}) Z_β(S),
    F_β(S) − β^{-1} ln(1 + e^{−βγ}) ≤ F_β(A ∪ S) ≤ F_β(S)        (β > 0, S ≠ ∅),

and for `γ ≥ 0` every `x ∈ A ∪ S` has a `y ∈ S` with `E(y) ≤ E(x)`.

*Proof.*  `Σ_A e^{−βE(x)} ≤ e^{−βγ} Σ_A e^{−βE(Tx)} = e^{−βγ} Σ_{T(A)} e^{−βE} ≤ e^{−βγ} Z(S)` by
injectivity and positivity. ∎  (`partition_transport`, `partition_prune_bracket`,
`freeEnergy_prune_bracket`, `min_transport`.)

Only injectivity of `T` matters.  Classical DEE is `T(x) = x[i ↦ t]` on `A = {x_i = r}`; *split*
DEE lets the dominator depend on the context, `T(x) = x[i ↦ t(x)]`, and is still injective
(`update_dep_injOn`); pair elimination and symmetry-based dominance are further instances.  The
zero-temperature statement is the classical soundness of DEE; the finite-temperature statement is
its deformation — pruning with margin `γ` costs at most `β^{-1} ln(1+e^{−βγ})` of free energy
(`thermal_dee` on product domains).  Used as a certificate rule this bound does not grow with the
*number* of pruned conformations, in contrast with the count-times-Boltzmann-factor bound `p*`
of the `K*` algorithm (benchmark B6: certified `Δ ln Z` between `4·10⁻⁴` and `1` where the count
bound is `0.1–3.6`).

*Prior art.*  The inequality is the worst case of the free-energy-perturbation identity
(Zwanzig 1954) and a Peierls-type injection argument; DEE with an energy window (Leach–Lemon
1998; X-DEE, Kloppmann et al. 2007) keeps near-optimal states but gives no multiplicative
partition-function guarantee; `K*` (Georgiev–Lilien–Donald 2008), `Z*_ε` (Viricel et al. 2016)
and AND/OR search (Lou–Dechter–Ihler 2017) bound neglected mass, not dominance ratios.  We found
no use of dominance as a temperature-aware certificate rule (`prior_art/L1` §C3).

### 2.2 Goldstein's criterion is exact and gauge invariant (a negative result)

For a pairwise model write `localE_i(a; x) = h_i(a) + Σ_{j≠i} [J_ij(a,x_j) + J_ji(x_j,a)]`.

**Theorem 2.2 [V].**  (a) `E(x[i↦a]) = base_i(x) + localE_i(a; x)` with `base_i` independent of
`a` (`energy_update`); hence `E(x[i↦r]) − E(x[i↦t]) = h_i(r) − h_i(t) + Σ_{j≠i} link_j(x_j)` is
separable in the neighbours.  (b) Over a product domain the Goldstein value
`h_i(r) − h_i(t) + Σ_{j≠i} min_{s∈D_j} link_j(s)` is the least element of the set of energy
differences (`goldstein_isLeast`).  (c) It is invariant under every reparameterisation
(`goldstein_gauge_invariant`, `exactMargin_reparam`).  (d) Desmet's bounds criterion never
exceeds it in any gauge and equals it at the explicit gauge
`m_{j→i}(s) = J_ij(t,s) + J_ji(s,t)` (`desmet_reparam_le`, `desmet_optimalGauge`).

Consequently *dual reparameterisation cannot improve single-site dominance tests with a
context-independent dominator (Goldstein-type tests) for pairwise energies on product domains*.
This answers the seeded question of Direction A in the negative **for that class of tests only**,
and locates where dual methods do matter:

* **Multi-site improving maps [K].**  A map `p : X → X` with `E(p(x)) ≤ E(x)` for all `x`
  (Shekhovtsov's maximum persistency, which subsumes Goldstein's test) can be certified by a
  reparameterisation bound although no single-site test fires, and whether the term-wise test
  for a given map succeeds *does* depend on the gauge.  Example (referee report `reviews/R1`,
  item 3): binary ferromagnetic chain, `n = 6`, `h_i = (0, 1)`, `J = 3·[x_i ≠ x_{i+1}]`: no state
  is single-site dominated and the pair `(1,1)` is never pair-dominated, yet `x ↦ 0…0` is
  improving and is certified by one LP-dual bound.  The sentence above must therefore not be read
  as "the gauge does not help dominance-type pruning".

* **Higher-order terms [V + P].**  With 3-body terms the difference energy at site `i` is a
  pairwise model on the *link graph* of `i` (vertices: neighbours; edges: pairs sharing a 3-body
  term with `i`).  *Exact dominance factorises over the connected components of the link graph*:
  if the difference energy is a constant plus a sum of functions each depending on one block of
  sites, the exact margin over a product domain is the constant plus the sum of the block minima
  (`isLeast_sum_of_block_separable`, `exact_margin_of_block_separable` **[V]**; harness I.4).
  The verified statement is the abstract one — block-separability of the difference energy is its
  hypothesis; that a model with 3-body terms has this form, with blocks the connected components
  of the link graph, is immediate but is not formalized (no 3-body model is defined in Lean) **[P]**.
  Goldstein is the case of singleton blocks; chain-local terms `T_{i−1,i,i+1}` give one block of
  at most four sites (a path), so exact dominance stays cheap for chain molecules; in general the
  cost is exponential only in the treewidth of the link graph.  Without restriction exact
  dominance is coNP-hard **[P]**: given a pairwise model `g` on the neighbours put
  `T(r,·,·) = g`, `T(t,·,·) = 0`; then `t` dominates `r` iff `min g ≥ 0`.  Any dual bound on a
  block yields a sound criterion between the nested sum-of-minima rule (LuCore et al. 2015) and
  exact dominance.
* **Non-product domains** (pair pruning, steric filters): exact dominance contains constraint
  satisfaction.
* **Bound-based pruning** (lower bound of a slice against an incumbent) — gauge dependent by
  nature; this is the `leaf` rule of the kernel.

*Prior art.*  Exactness for pairwise models and reparameterisation invariance are in Shekhovtsov
(CVPR 2014; CVIU 2016, Thm 3.3) and de Givry–Prestwich–O'Sullivan (CP 2013); the literal
"sup of Desmet over gauges = Goldstein" sentence was not found but is a corollary.  We claim no
novelty beyond the formalization.

### 2.3 Envelope duality: exact characterisations under a non-decomposable residual

Let `f = E₀` on a set `X` with envelope `d`.

**Theorem 2.3 (contact set) [V].**
`∃ g admissible, x ∈ argmin (f + g)`  ⇔  `∀y, f(x) ≤ f(y) + d(y,x)`.

*Proof.*  (⇒) `f(x) − f(y) ≤ g(y) − g(x) ≤ d(y,x)`.  (⇐) `g = d(·, x)` is admissible by the
triangle inequality, `g(x) = 0`, and `f(y) + d(y,x) ≥ f(x)`. ∎

The right-hand side says that `x` lies on the contact set of `f` with its Pasch–Hausdorff
envelope `f^d(x) = inf_y [f(y) + d(y,x)]`, the largest `d`-Lipschitz minorant of `f`.  The
extremal residual is the envelope itself.

**Theorem 2.4 (sharp minimum) [V].**
`∀ g admissible, x ∈ argmin (f + g)`  ⇔  `∀y, d(x,y) ≤ f(y) − f(x)`.

*Proof.*  (⇐) `f(y) + g(y) − f(x) − g(x) ≥ d(x,y) − (g(x) − g(y)) ≥ 0`.  (⇒) `g = −d(x,·)` is
admissible by the triangle inequality, and optimality of `x` for it reads
`f(x) ≤ f(y) − d(x,y)`. ∎

So a configuration is certifiably optimal *without evaluating the residual anywhere* iff the
white-box energy grows away from it at least as fast as the envelope — a sharp minimum of modulus
one in the envelope quasi-metric (Polyak; Burke–Ferris), equivalently a stability condition of
Bilu–Linial type.

**Theorem 2.5 (McShane brackets) [V].**  Let the residual be evaluated on a finite anchor set `A`
with consistent values `v`.  The envelopes

    L(y) = max_{a∈A} [v(a) − d(a,y)],      U(y) = min_{a∈A} [v(a) + d(y,a)]

are admissible, interpolate `v`, and satisfy `L ≤ g ≤ U` for every admissible `g` agreeing with
`v` (`lowerEnv_admissible`, `upperEnv_admissible`, `lowerEnv_eq_of_mem`, `lowerEnv_le`,
`le_upperEnv`).  Hence for every finite `S` and every `β ≥ 0`

    min_S (f + L) ≤ min_S (f + g) ≤ min_S (f + U),
    Z_β(f + U; S) ≤ Z_β(f + g; S) ≤ Z_β(f + L; S),

(`robust_min_bracket`, `robust_partition_bracket`).  Conversely, for consistent data every value
of the first interval is `min_S (f + g)` and every value of the second is `Z_β(f + g; S)` for
some admissible `g` agreeing with `v` — take `g = (1−λ)L + λU` and apply the intermediate value
theorem in `λ` (`robust_min_interval_exact`, `robust_partition_interval_exact`).  The set of
possible values is therefore *exactly* the interval: **no certificate using the same information
can report a tighter one**.  In the language of optimal recovery this is the statement that the
set of consistent values of a continuous functional on a convex class is an interval whose end
points are attained at the extremal (McShane) extensions.

With the site-additive envelope and one anchor `a`, `f + L = v(a) + [E₀ − Σ_i δ_i(a_i, ·)]` is
again a pairwise model: *the residual's envelope is absorbed into the one-body tables*.  This is
the reduction used by the residual kernel (`PairInstance.anchored`, §6) and it means every
decomposable-energy algorithm lifts to the residual problem at the cost of one modified instance
per anchor.  With several anchors `min_S (f + L) = min_x max_a [v(a) + (E₀ − d(a,·))(x)]` is a
minimum of a *maximum* of pairwise models; solving one modified instance per anchor gives only
`max_a min_x`, which reaches the exact value through branching (the residual kernel chooses an
anchor per leaf).

**Theorem 2.6 (query model: exact pruning with evaluated anchors) [V].**  With anchors `(A, v)`
as above,

    ∃ g admissible with g|_A = v and x ∈ argmin(f + g)
        ⇔   (∀y, f(x) ≤ f(y) + d(y,x))   ∧   (∀y, f(x) + L(x) ≤ f(y) + U(y)).

*Proof.*  (⇒) The first condition is Theorem 2.3; the second is `L(x) ≤ g(x)`, `g(y) ≤ U(y)`.
(⇐) Put `γ = L(x)` and `g(y) = min(U(y), γ + d(y,x))`: a minimum of two admissible functions is
admissible; `g = v` on `A` because `γ + d(a,x) ≥ v(a)`; `g(x) = γ` because `L ≤ U`; and
`f(x) + γ ≤ f(y) + g(y)` is exactly the two hypotheses. ∎

The set violating one of the two conditions is therefore the **exact** set of configurations that
are minimisers for *no* admissible residual consistent with the evaluations.  (A rule that only
has to preserve the minimum *value* may discard more because of ties: for `X = {x, y}`, `d = 1`,
`E₀ = (0, 1)` the state `y` satisfies both conditions — it ties with `x` for `g(y) − g(x) = −1` —
although `x` is a minimiser for every admissible `g`.  The exact criterion for that notion is the
anchored sharp-minimum condition of §11.2; the kernel's non-strict prune rule removes such
states.)  For an anchor `y` the second condition reads
"optimistic value of `x` ≤ evaluated value of `y`", i.e. *lower bound ≤ incumbent*.  The pruning
interval of minimised DEE (iMinDEE) is the special case in which the only envelope information
is a one-sided bound `Δ ≥ lo` — a virtual anchor `x₀` with `v(x₀) = lo`, `d(x₀, ·) = 0` and
`d(·, x₀)` large, which is why envelopes are allowed to be asymmetric — and one conformation has
been evaluated: then `L ≡ lo` off the anchor and condition 2 is `E₀(x) + lo ≤ E(x̂)`.
Theorem 2.6 shows that this rule is optimal (up to ties) in the query model and extends it to
arbitrary envelopes and any number of evaluations.

**Corollaries [V].**
* *Energy window* (`energy_window_exact`): with global bounds only, `x` can be optimal iff
  `E₀(x) ≤ E₀(y) + (hi − lo)` for all `y`.  The classical "global residual bottleneck" is
  information-theoretic: every sound rule must keep the whole window.
* *Differential DEE* (`differential_dee_sound`): if `E₀(x[i↦t]) + δ_i(t,r) < E₀(x)` for all `x`
  with `x_i = r`, no such `x` is optimal for any admissible residual.  This is the contact
  criterion restricted to single-site moves with a context-independent dominator; split and
  multi-site versions follow from the same theorem with other transport maps.

*Benchmark B1* (random chain models, 6 sites × 3 states, residual with bounded differences `c`):
fraction of (site, state) pairs that can be discarded —

| `c` | DEE, global oscillation | DEE, differential | exact, global oscillation (window) | exact, envelope (contact set) |
|---|---|---|---|---|
| 0.05 | 0.13 | 0.16 | 0.63 | 0.65 |
| 0.20 | 0.04 | 0.13 | 0.46 | 0.59 |
| 0.40 | 0.03 | 0.14 | 0.24 | 0.48 |
| 0.80 | 0.00 | 0.08 | 0.04 | 0.32 |

The envelope retains pruning power where global bounds have none; single-site dominance rules
capture only a fraction of what either information class permits, which is the quantitative
motivation for bound-based certificates (§6).

*Prior art — corrected after the referee report (`reviews/R1`, items 2 and Q3; `prior_art/L4`,
`L5`).*  The first search (`prior_art/L1` §C2) covered the dead-end-elimination / cost-function
network literature only, and its "not found" verdict holds only there.  As mathematics,
Theorems 2.3–2.6 are the classical theory of systems of difference constraints, of which the
admissible class is the solution set (a *polytrope* / Lipschitz polytope of a finite quasi-metric
space / simple temporal network; §11.1):

| statement | follows from |
|---|---|
| Thm 2.3 | no-negative-cycle criterion for difference constraints (Bellman–Ford; Rockafellar's feasible-differential theorem); `∂^c E₀(x) ≠ ∅ ⇔ E₀(x) = E₀^{cc}(x)` for the cost `c = d` (abstract convexity); "possibly optimal" (Inuiguchi–Sakawa; Aissi–Bazgan–Vanderpooten 2009) |
| Thm 2.4 | tightness of the shortest-path closure, `max_g (g(x) − g(y)) = d(x,y)` (Kantorovich–Rubinstein extremal function); sharp minima (Polyak 1979; Burke–Ferris 1993); "necessarily optimal" |
| Thm 2.5, bracket | McShane 1934; semi-Lipschitz extension for asymmetric `d` (Romaguera–Sanchis; Mustăţa; Cobzaş); minimal network of a simple temporal network and its decomposability (Dechter–Meiri–Pearl 1991) |
| Thm 2.5, exactness | convexity of the consistent set (optimal recovery: Micchelli–Rivlin; Traub–Woźniakowski; Sukharev and Piyavskii–Shubert for Lipschitz classes; Novak 1988) |
| Thm 2.6 | Thm 2.3 on the one-point extension of the envelope (§11.1); for `E₀ ≡ 0` and symmetric `d` it is Lemma 8 of Malherbe–Vayatis (ICML 2017, "potential maximizers") |
| energy window | Thm 2.3 for the discrete metric; possibly-optimal test under interval uncertainty |

Within provable design: MinDEE's range terms (Georgiev–Lilien–Donald 2008) are a
bounded-difference envelope in Desmet form and iMinDEE's pruning interval
(Gainza–Roberts–Donald 2012) is a one-anchor instance; LUTE/EPIC (Hallen et al.) treat
non-pairwise energies with *fitted*, uncertified residuals; many-body DEE (LuCore et al. 2015)
truncates the expansion without carrying the remainder into the test.  What is left that does not
follow from the classical theory is the *formulation* — a known additive part next to the
Lipschitz class, which produces the contact condition and makes white-box-sharp states free —
and the machine-checked statements.

### 2.4 Witness-size lower bound

**Theorem 2.7 (anchors are necessary) [V].**  Let the true residual `g` be `κ`-Lipschitz for the
envelope (`g(x) − g(y) ≤ κ d(x,y)`, `κ ≤ 1`), let `A` be the anchor set of an `ε`-certificate
(`min_A (f+g) − ε ≤ f + L` everywhere), and let `E* ≤ min_A (f+g)`.  If `y` is `σ`-separated from
all other anchors and `(f+g)(y) − E* < (1−κ)σ − ε`, then `y ∈ A`.  With uniform separation `σ`,

    |A|  ≥  #{ y : (f+g)(y) − E* < (1 − κ) σ − ε }.

*Proof.*  If `y ∉ A`, `L(y) ≤ g(y) − (1−κ)σ`, so the certified bound is at most
`(f+g)(y) − (1−κ)σ`, while the incumbent is at least `E*`. ∎

For the weighted Hamming envelope `σ = min_i c_i`.  The theorem concerns **one certificate
format**: the incumbent is the best *evaluated* anchor and the bound is the McShane lower
envelope.  For that format the number of residual evaluations is at least the number of states in
the energy shell of width `(1−κ) c_min − ε` above the optimum — the microcanonical count at the
resolution of the envelope; a loose envelope (small `κ`) is paid for in entropy.  Benchmark B2
(8 states): with `κ = 0, ε = 0` the bound forces 5.9 anchors on average against a brute-force
optimum of 6.25; with `κ = 0.9, ε = 0.2` it forces none while the optimum is 2.2.

**Correction (referee report `reviews/R1`, item 1; `DEAD_ENDS.md` D21).**  Earlier versions of
this report read the theorem as "*any* certificate must evaluate every state of the shell".  That
is false for certificates of an ε-optimal *configuration*: for `X = {0,1}`, `d = 1`,
`E₀ = (0, 5)`, `Δ ≡ 0` the shell is `{0}`, yet Theorem 2.4 certifies `x = 0` for every admissible
residual with no evaluation at all.  States separated from the candidate by the white-box part
alone cost nothing.  The true statements are:

* *value certificates* (`min(E₀+U) − min(E₀+L) ≤ ε`) **[V]**: `A` contains every `y` with
  `(E₀+Δ)(y) − min(E₀+Δ) < (1−κ)σ − ε`;
* *configuration certificates* for `x̂` (every consistent residual makes `x̂` ε-optimal) **[P]**:
  `A` contains every `y ≠ x̂` with `E₀(y) − E₀(x̂) < d(x̂,y) − ε` **and**
  `(E₀+Δ)(y) − (E₀+Δ)(x̂) < (1−κ)σ − ε`.

Here "`y` is `σ`-separated" means `d(a,y) ≥ σ` for the anchors `a ≠ y` — distances *from* the
anchors *to* `y`; for asymmetric envelopes the transposed reading is false (second referee, m9).
Moreover the theorem is only the first layer (radii below the separation `σ`) of a covering
statement which has a converse.  Both points are the subject of §11: the three certificate
notions are characterised exactly as covering conditions in a *slack quasi-metric* and have the
same minimal size, the covering number or one more (Theorems 11.3–11.5), and the single
forced-point count above is replaced by linear-programming and rate–distortion bounds with a
matching upper bound for product landscapes (Theorems 11.6–11.9).  By §11.10 the same bounds
hold for every algorithm, not only for certificates of these formats.

The mechanism of Theorem 2.7 is the `(1 − Lip f/L)` adversary of Bachoc, Cesari and Gerchinovitz
(NeurIPS 2021, Thm 2), at the finest scale; the notion of a minimal certificate goes back to
Danilin (1971), Hansen–Jaumard–Lu (1991, "best possible algorithm") and Baran–Demaine (2004,
"proof sets").

---

## 3. Direction D — partition functions and free energies

### 3.1 Thermal dead-end elimination

Theorem 2.1 on a product box (`thermal_dee` **[V]**): if `t ∈ D_i`, `t ≠ r` and
`E(x[i↦t]) + γ ≤ E(x)` for all `x` in the box with `x_i = r`, then deleting `r` multiplies the
partition function of the box by a factor in `[(1+e^{−βγ})^{-1}, 1]`.  In the weight domain the
same rule is checked factor by factor (`PruneZOK`, `zprune_sound` **[V]**): if
`w_i(r) ≤ q₀ w_i(t)` and `W_ij(r,s) W_ji(s,r) ≤ q_j W_ij(t,s) W_ji(s,t)` for all `s ∈ D_j`, then
`Z ≤ (1 + q₀ ∏_j q_j) Z'`.  If the dominance map is at most `m`-to-one instead of injective the
factor becomes `1 + m e^{−βγ}` (`partition_prune_bracket_fibers` **[V]**; harness I.6).  Rounds compose
multiplicatively, so a pruning schedule with margins `γ_k` certifies
`0 ≤ ln Z − ln Z_pruned ≤ Σ_k ln(1 + m_k e^{−βγ_k})` (`m_k` states mapped to one survivor in
round `k`).

*Observables.*  The same margin controls ensemble averages: if the pruned set carries at most
the fraction `ρ` of the survivors' weight, every observable bounded by `B` changes its Boltzmann
average by at most `2Bρ`; for a dominance step, by at most `2B e^{−βγ}`
(`boltzmannAvg_prune_error`, `boltzmannAvg_dominance_error` **[V]**; harness I.5).  Certified
pruning therefore gives certified ensemble properties, not only free energies.

### 3.2 The free-energy sandwich

Let `μ₀` be a reference ensemble with expectation `⟨·⟩₀` and `Z/Z₀ = ⟨e^{−βΔ}⟩₀`.  Parts (a), (b)
hold for an arbitrary reference (in particular `μ₀ ∝ e^{−βE₀}` with pairwise `E₀`); parts (c)–(e)
require a **product** reference `μ₀ = ⊗_i μ_i` (independent sites, e.g. a mean-field or
one-body reference).

**Theorem 3.1 [V] (`FreeEnergySandwich.lean`).**
(a) (Gibbs–Bogoliubov) `ln(Z/Z₀) ≥ −β⟨Δ⟩₀` (`gibbs_bogoliubov`, `partition_ratio_sandwich`).
(b) (Hoeffding) if `a ≤ Δ ≤ b` then `ln(Z/Z₀) ≤ −β⟨Δ⟩₀ + β²(b−a)²/8` (`hoeffding_upper`,
`free_energy_difference_sandwich` for the corresponding statement about `F − F₀`).
(c) (McDiarmid tensorisation) if `μ₀` is a product measure on `n` sites and `Δ` has bounded
differences `c_i`, then `ln(Z/Z₀) ≤ −β⟨Δ⟩₀ + β² Σ_i c_i² / 8` (`bounded_differences_sandwich`,
via the martingale step `two_factor_tensorization`).
(d) (**the worst case is decomposable**) for every product reference, every `β` and all
constants `c_i ≥ 0` there are subsets `A_i` of site states such that the additive two-level
residual `Δ⋆(x) = Σ_i c_i·[x_i ∈ A_i]` has the largest Jensen gap `ln(Z/Z₀) + β⟨Δ⟩₀` among **all**
residuals with bounded differences `c` (`exists_two_level_worst_residual`; the single-site step
is a convex maximisation over a cube, attained at a vertex — `convexOn_centered_mgf`,
`exists_two_level_site_extremal`).
(e) (sharp constant) for the balanced two-level reference the gap is exactly
`Σ_i ln cosh(β c_i/2)` (`balanced_additive_gap`), `u²/(2+u²) ≤ ln cosh u ≤ u²/2`
(`log_cosh_bounds`), and for every `K < 1/8` the bound with `K` in place of `1/8` is false
(`mcdiarmid_no_better_constant`).

So for a product reference one reference expectation plus the envelope constants pin `ln Z` in
an interval of width `β² Σ c_i²/8`, quadratically smaller than the trivial `β Σ c_i` when
`β c_i < 8`; and the worst non-decomposable residual is a fully decomposable one — the exact
supremum of the gap over the class is
`Σ_i max_{A_i} ln(p_i e^{βc_i(1−p_i)} + (1−p_i) e^{−βc_i p_i})`, `p_i = μ_i(A_i)`.

*The product hypothesis cannot be dropped [V].*  For a correlated reference the width
`β² Σ c_i²/8` is false: two perfectly correlated binary sites (`μ₀` uniform on `{00, 11}`),
`Δ = x₁ + x₂`, `c = (1,1)`, `β = 1` give the gap `ln cosh 1 ≈ 0.434 > 0.25`
(`correlated_reference_counterexample`; harness `DEAD.5`; `DEAD_ENDS.md` D14).  What survives for
an arbitrary reference is (b) with the full range `b − a ≤ Σ_i c_i`, i.e. the width
`β² (Σ_i c_i)²/8` (`bounded_differences_sandwich_any_reference`,
`kl_reference_target_le_any_reference` **[V]**; harness III.6) — linear instead of square-root
accumulation over sites; intermediate widths for weakly dependent references are quoted below
as [K].

*The gap is a relative entropy [V] (`EnsembleDivergence.lean`).*  With `μ₀` the reference
ensemble and `μ ∝ μ₀ e^{−βΔ}` the target ensemble, `ln(Z/Z₀) + β⟨Δ⟩₀ = KL(μ₀ ‖ μ)` exactly
(`kl_reference_target_eq_gap`).  Therefore `0 ≤ KL(μ₀ ‖ μ) ≤ β²(b−a)²/8`, and
`≤ β² Σ_i c_i²/8` for product references (`kl_reference_target_le_hoeffding`,
`kl_reference_target_le_bounded_differences`): the envelope constants certify how well a sampler
of the reference ensemble approximates the target ensemble, and by Pinsker's inequality **[K]**
every observable bounded by `B` shifts by at most `B β (Σ_i c_i²)^{1/2}/2` for a product
reference (`B β (b−a)/2` in general).

*Sharper and more general forms [K].*  The exact extremal function is Rio's
`ℓ(t) = sup_r [ln(1 + r(e^t − 1)) − tr] ≤ t²/8` (Rio 2013, Lemma 4.1): the gap is at most
`Σ_i ℓ(β c_i)`, which grows only linearly in `β` at low temperature (benchmark B4: at `βc = 10`,
`Σℓ = 40.2` against the Gaussian bound `75` and `36.1` attained by the worst additive residual for
the sampled reference).  For Markov or Dobrushin references the constants become
`‖Γ c‖²` with `Γ` a Wasserstein matrix, `‖Γ‖ ≤ (1−θ)^{-1}` (Kontorovich–Ramanan 2008;
Kontorovich–Raginsky 2016).  A uniform bound `ln⟨e^{−β(Δ−⟨Δ⟩)}⟩₀ ≤ β²C/2` over all admissible
residuals **and all `β ∈ ℝ`** is *equivalent* to the transport inequality
`W_{1,d}(ν, μ₀) ≤ (2C·KL(ν‖μ₀))^{1/2}` (Bobkov–Götze 1999): the envelope metric of §2 is exactly
the cost in which the reference ensemble must satisfy T₁.  The quantifier over `β` matters: at a
fixed `β` a smaller constant can suffice (for Bernoulli(0.02) with the discrete metric the T₁
constant is `1/(2φ(p)) = 0.1233`, `φ(p) = ln((1−p)/p)/(1−2p)`, while the best constant at
`β = 1` is `0.028`; `reviews/R1`, item 6); and for an asymmetric envelope `W_{1,d}` is not
symmetric, so the cost must be transposed for `β < 0`.  The fixed-`β` duality that replaces the
equivalence is Theorem 11.14.  The same inequality is used for model-bias quantification by
Gourgoulias et al. (2020); we found no statement of it as a certified free-energy-perturbation
bound, but claim no mathematical novelty for (a)–(e).  Statement (d) was first classified as
"implicit in Rio's proof"; the third literature check (`prior_art/L6`, T2) found it in print:
Alon–Boppana–Spencer (1998) and Bobkov–Houdré–Tetali (2006) prove that the Laplace functional of
a product graph is the product of the single-factor functionals, `L_{Gⁿ}(t) = L_G(t)ⁿ`, with
additive extremals, and that indicators are extremal on the complete graph for an arbitrary
fixed measure.  Only the formalization is new.  The statement is specific to the moment
generating function (for tail probabilities the extremal problem has non-additive solutions,
Owhadi et al. 2013) **and to product references**: for two ternary sites with a correlated law a
non-additive residual has a strictly larger gap than every additive one (`1.2818` against
`1.2767` at `β = 2`; harness `DEAD.9`, `DEAD_ENDS.md` D25), and on the even-weight strings of the
3-cube the supremum `ln cosh(β/2)` is not attained by an additive function.  Whether additivity
survives for *binary* Markov trees is open (it held in 21 000 random binary 3-chains examined
in `prior_art/L6`).

*Limitation.*  The gap is extensive: with `c_i = 0.5` kcal/mol on 100 torsions at 298 K it is
≈ 5 kcal/mol.  The sandwich certifies free energies only for `β c_i ≪ M^{-1/2}`, or after
localisation — applying it cell by cell in a branch-and-bound partition, where cell-local
oscillations make the gap second order in the cell width.

### 3.3 Exact interval with evaluated anchors

Theorem 2.5 at finite temperature: `Z_β(E₀+U) ≤ Z ≤ Z_β(E₀+L)`, with every value in between
attained (`robust_partition_interval_exact`).  With one anchor and
the site-additive envelope both ends are partition functions of pairwise models with modified
one-body tables (two transfer-matrix computations when `E₀` is a chain).

### 3.4 Certified partition functions: weight domain, kernel, voxels

*Weight domain.*  A `WInstance` stores rational Boltzmann factors.  If two instances bracket the
true factors, their exact rational partition sums bracket the real partition function
(`Z_encloses_partitionFn` **[V]**).  The brackets come from the certified rational enclosure of
`exp` (`exp_enclosure`, `contains_boltzmann` **[V]**, §5), and this step is itself part of the
verified pipeline: the two instances are *computed* from rational interval tables enclosing the
energies (`WInstance.lowerOfIntervals`, `WInstance.upperOfIntervals`), and
`certified_partition_of_intervals` **[V]** concludes `lo ≤ Z_real ≤ hi` from two accepted
certificates with no hypothesis about Boltzmann factors.  Kernel-evaluated instance
(`triangle_real_partition_enclosure`): the frustrated triangle at `β = 1` has
`Z = 2e^{−3} + 6e^{−1} ∈ [2.3068, 2.3069]`, proved in Lean from the integer energy tables alone.

*Kernel.*  `zverify` returns a rational interval for `Z` over a box from a certificate built
from three rules — factorised leaf (pair factors replaced by certified constants, the remaining
product measure summed exactly as `∏_i Σ_a w_i(a)`), branch (additivity over the states of a
site), thermal prune — and `zverify_sound` **[V]** proves `lo ≤ Z ≤ hi` for instances with
nonnegative factors.  The top-level entry point `zverifyTop` checks nonnegativity itself, so
`zverifyTop_sound` **[V]** has no side condition; `negativeW_unguarded` exhibits a negative-factor
instance on which the bare rule checker returns an interval that misses `Z`.

*Limitation of this rule set (referee report `reviews/R1`, item 4; `DEAD_ENDS.md` D22).*  The
tropical leaf carries a dual solution and is exact on trees; the factorised leaf of the
partition kernel replaces every pair factor by constants, and a thermal prune always widens the
interval.  An *exact* enclosure therefore needs constant pair factors on every leaf box, i.e.
full enumeration: `2ⁿ` leaves for a two-state chain of `n` sites, whose partition function a
transfer matrix computes in `O(n k²)` operations (the referee's exhaustive search over all
certificates for `n ≤ 5` confirms that with half as many leaves the best achievable ratio
`hi/lo` is still `≥ 1.22`).  With these three rules alone the pipeline "certified partition
functions for chain molecules" has no sub-exponential certificates.  The repair — two further
verified rules, a *cut* rule for (nearly) independent subsystems and an *elimination* rule that
sums out a site with at most two neighbours — exact on every chain (machine-checked), on the
tree and ring instances evaluated by the kernel, and by a paper argument on all interaction
graphs of treewidth at most two — is in §11.8.

*Voxels.*  For a measurable voxel `V` of finite volume with `E_lo ≤ E ≤ E_hi` on `V`,

    vol(V) e^{−βE_hi} ≤ ∫_V e^{−βE} ≤ vol(V) e^{−βE_lo}        (`voxel_boltzmann_bounds` [V]),

and over a finite family of disjoint voxels indexed by the configurations of a box, rational
instances whose weights bracket the voxel integrals have partition sums that bracket the
continuous integral (`Z_encloses_voxel_integral`, `certified_voxel_partition` **[V]**; these two
statements take the bracketing of each voxel integral as a hypothesis).  The factor `vol(V)` is
the conformational entropy of the voxel, which the minimised-energy surrogate `e^{−βE_min}` used
by the `K*` family omits; with it the same enumeration yields a two-sided bound on the
*integral*.

*Closing the pipeline [V] (`VoxelBridge.lean`).*  The bracketing hypothesis is discharged for the
case the kernels are built for.  Let the torsion coordinates carry a product measure `⊗_i ν_i`,
let site `i` have measurable cells `s_i(a)` of finite measure, pairwise disjoint in `a`, and let
the energy be pairwise, `E(θ) = Σ_i u_i(θ_i) + Σ_{i≠j} U_ij(θ_i, θ_j)`.  If real tables
`M^lo ≤ M^hi` enclose `u_i` and `U_ij` on the cells, and two rational weight instances satisfy,
entry by entry,

    w^lo_i(a) ≤ ν_i(s_i(a)) e^{−β h^hi_i(a)},   W^lo_ij(a,b) ≤ e^{−β J^hi_ij(a,b)},
    ν_i(s_i(a)) e^{−β h^lo_i(a)} ≤ w^hi_i(a),   e^{−β J^lo_ij(a,b)} ≤ W^hi_ij(a,b)

(what `contains_boltzmann` and outward rounding deliver), then each configuration's weights
bracket the Boltzmann integral over its product voxel (`pairwise_voxel_weight_bounds`), and two
accepted certificates give

    lo(I^lo)  ≤  ∫_{⋃_x V_x} e^{−βE} d(⊗ν)  ≤  hi(I^hi)        (`certified_torsion_partition`),

with no hypothesis about voxel integrals; over the full box the domain of integration is the
whole product `∏_i ⋃_a s_i(a)` (`certified_torsion_partition_full`).  In the form
`certified_torsion_partition_top` the certificates are checked by `zverifyTop` (no nonnegativity
hypothesis) and the enclosures are needed only on the cells of the box, so cells removed from
the domains — e.g. sterically excluded ones, where the energy need not be bounded — need no
energy enclosure (their table entries are unconstrained; the published factors must still
bracket the Boltzmann factors of whatever table values are chosen there).  What remains are
measurability of the cells and energy terms, the table enclosures of `u_i`, `U_ij` on the cells
(the output of interval evaluation, an input here), and the displayed entrywise inequalities.
For cells that are arcs with rational chart endpoints the latter are computable: the angular
measure `2(arctan t₂ − arctan t₁)` has the rational enclosure `(t₂−t₁)·2/(1+T²) ≤ · ≤ 2(t₂−t₁)`
for `|t| ≤ T` (`two_arctan_sub_bounds`), and `chartArc_onebody_brackets` combines it with the
certified exponential.  That upper bound does not improve when an arc is subdivided; the
convergent form `(t₂−t₁)·2/(1+m²)` with `m ≤ |t|` on the arc (`two_arctan_sub_bounds_of_sq`) is
available in executable form for arcs on one side of the chart origin
(`chartArc_onebody_brackets_pos`, `chartArc_onebody_brackets_neg`), where the ratio of the two
volume bounds is `(1+t₂²)/(1+t₁²) → 1`.  Only the base chart is formalized; the cells of the
three rotated charts are translates by multiples of `π/2`.  Three kernel-evaluated instances are in `VoxelBridge.lean`
(`exact_witness`, `pair_witness`, and `chart_witness`: the torsion potential `cos θ` on two
chart arcs, with all tables, volume bounds and Boltzmann brackets computed by the interval
layer).

*Second order: separable envelopes [V] + Taylor step [P].*  If on a product voxel `∏_i s_i` the
energy is bracketed by separable functions, `Σ_i φ_i(x_i) ≤ E(x) ≤ Σ_i ψ_i(x_i)`, then

    ∏_i ∫_{s_i} e^{−βψ_i}  ≤  ∫_{∏ s_i} e^{−βE}  ≤  ∏_i ∫_{s_i} e^{−βφ_i}

(`separable_voxel_bounds` **[V]**, Fubini on the box), and if `ψ_i ≤ φ_i + w_i` the two products
differ by at most the factor `exp(β Σ_i w_i)` (`separable_voxel_ratio` **[V]**).  A second-order
Taylor expansion with a scalar spectral Hessian enclosure `m·I ⪯ ∇²E ⪯ M·I` on a box with centre `c` and
half-widths `h_i`,
`E(c) + g·u + (m/2)|u|² ≤ E(c+u) ≤ E(c) + g·u + (M/2)|u|²`, is exactly such a pair of separable
envelopes with `w_i = (M−m) h_i²/2` **[P]** (the Taylor step is standard and not formalized).
Consequences: (i) an `M`-dimensional voxel integral is certified by `M` one-dimensional
Gaussian-type integrals, each enclosed by one-dimensional voxel sums (`voxel_riemann_enclosure`),
so a second-order certificate costs `M ×` (1-D resolution) per voxel instead of an
`M`-dimensional refinement; (ii) the relative width is `exp(β (M−m) Σ h_i²/2)`, so accuracy
`1+ε` needs `N ≈ vol · (β (M−m) d / (8 ln(1+ε)))^{d/2}` voxels (note the factor `d^{d/2}`).  For
the class in which *only* `m·I ⪯ ∇²E ⪯ M·I` is known and the energy is accessed by point
evaluations, information-based lower bounds for integration of `C^k` classes (Bakhvalov 1959)
and, for log-partition functions, `Θ(B n^{−m/d})` (Holzmüller–Bach 2025) give the same exponent
`d/2` **[K]**.  This is *not* an optimality statement for the scheme above (`reviews/R1`,
item 7): an oracle returning Hessian enclosures on boxes is not a point oracle; for `C³` energies
its widths shrink with the box and a third-order enclosure would need only `N ∼ ε^{−d/3}` voxels,
at the price of non-separable Gaussian box integrals.  In the scheme above second order is caused
by the scalar sandwich (which discards off-diagonal Hessian terms to keep the envelopes
separable), not by a lack of information.

### 3.5 Decomposition at finite temperature [K, V]

`Z_β(E₁+E₂) ≤ Z_{β/ρ}(E₁)^ρ Z_{β/(1−ρ)}(E₂)^{1−ρ}` and
`F_β(E₁+E₂) ≥ F_{β/ρ}(E₁) + F_{β/(1−ρ)}(E₂)` (`partitionFn_holder`, `freeEnergy_holder`): the
parts are evaluated at *colder* temperatures, and the bound tends to the tropical sum rule
`min(E₁+E₂) ≥ min E₁ + min E₂` as `β → ∞`.  This is Hölder's inequality, i.e. the weighted
mini-bucket bound (Liu–Ihler 2011; tree-reweighted: Wainwright–Jaakkola–Willsky 2005).

### 3.6 Stopping rules and multi-state ranking (open)

Certifying which of several macrostates has the largest partition function is a refinement race
between intervals.  Bound racing exists (`BBK*`; marginal-MAP search) and competitive analysis of
progressively refined inputs exists (Tseng–Kirkpatrick 2011: a logarithmic factor is
unavoidable), but no competitive-ratio theorem for partition-function ranking was found.  The
exact interval of Theorem 2.5 is the right primitive: it states what *any* certificate can know
after a given set of evaluations.  We leave the instance-optimality question open.  An earlier
version recorded "uniform racing is within the factor `w^{-1}(g/2)/w^{-1}(g)` of the offline
optimum"; that sentence is withdrawn (`reviews/R1`, item 8; `DEAD_ENDS.md` D23): the benchmark was
undefined; for two states and a convex width function `w` the cheapest separating allocation *is*
the uniform one (`w(n₁) + w(n₂) ≤ g`, Jensen), so the ratio is one and the factor `2^{d/2}` was an
artefact of comparing with the lower bound `w^{-1}(g)`; and for `K > 2` states with unequal gaps
uniform refinement *without elimination* costs `K·w^{-1}(g_min/2)` against about
`2·w^{-1}(g_min/2)`, an unbounded ratio `≈ K/2`.  The stated factor is an upper bound only for
racing with elimination.

---

## 4. Direction C — realizability and geometric stability

### 4.1 Trace-enhanced spectral obstruction to low-dimensional realizability (known; formalized)

Let `D̂` be a hollow symmetric matrix of predicted *squared* distances between `L` points,
`J = I − 11ᵀ/L`, `Ĝ = −½ J D̂ J`, `λ_1 ≥ … ≥ λ_L` the eigenvalues of `Ĝ`, and for a configuration
`Y ∈ ℝ^{L×r}` let `Δ(Y)` be its squared-distance matrix.

**Lemma 4.1 (K-identity) [V, K].**  For symmetric `E` with zero row sums,
`Σ_{ij} (E_ii + E_jj − 2E_ij)² = 4‖E‖_F² + 2L Σ_i E_ii² + 2 (tr E)² ≥ 4‖E‖_F² + 4 (tr E)²`
(`K_identity`, `K_lower_bound`).  This identity is in Tsang–Pereira (2016, §3).

**Theorem 4.2 (rank-constrained PSD approximation with trace penalty) [V].**  For symmetric `A`
with sorted eigenvalues `λ_k` and `G ⪰ 0` with `rank G ≤ r`,

    ‖G − A‖_F² + (tr G − tr A)²  ≥  Σ_{k>r} λ_k² + (1/(r+1)) (Σ_{k>r} λ_k)²

(`rank_psd_trace_obstruction`).  *Proof.*  By Hoffman–Wielandt, `‖G−A‖_F² ≥ Σ_k (μ_k − λ_k)²`
with `μ` the sorted eigenvalues of `G`, which vanish beyond `r`; `tr G − tr A = Σ_k (μ_k − λ_k)`;
with `x_k = μ_k − λ_k` (`k ≤ r`) and `τ = Σ_{k>r} λ_k`, Cauchy–Schwarz on the `r+1` numbers
`x_1, …, x_r, τ − Σ x_k` gives `τ² ≤ (r+1)(Σ x_k² + (τ − Σ x_k)²)`. ∎

**Theorem 4.3 (s-stress lower bound; non-realizability certificate) [V, K].**  For every
`Y ∈ ℝ^{L×r}`,

    ‖D̂ − Δ(Y)‖_F²  ≥  4 Σ_{k>r} λ_k² + (4/(r+1)) (Σ_{k>r} λ_k)²

(`sstress_lower_bound`; for `r = 3`: `4 Σ_{k>3} λ_k² + τ²`).  *Proof.*  `D̂ − Δ(Y) = −K(E)` with
`E = G(Y) − Ĝ` centred symmetric and `G(Y) = (JY)(JY)ᵀ ⪰ 0` of rank `≤ r`; apply Lemma 4.1 and
Theorem 4.2. ∎

**Attribution.**  This bound is Proposition 1 together with the relaxation inequality of
Sonthalia, Van Buskirk, Raichel and Gilbert, *How can classical multidimensional scaling go
wrong?* (NeurIPS 2021), restated in Deng et al. (NeurIPS 2024, Thm 6), with the same constants
**when `λ_r(Ĝ) ≥ 0`**.  When `λ_r(Ĝ) < 0` it is strictly weaker than their Proposition 1, whose
constants also count the wrong-signed kept eigenvalues (for `D̂ = −2(11ᵀ − I)`, `L = 4`, `r = 3`
the bound here is `5`, theirs `21`, the optimum `48`; `reviews/R1`, item 9); the Lean theorem
could be strengthened by keeping `μ_k ≥ 0`.  Sonthalia et al. also compute the sign-constrained
relaxation exactly in `O(n³)`, which is at least as strong as the closed form.  We had derived
the bound independently before the literature check (`prior_art/L3` §C10) and **claim no novelty
for the inequality**.  What is contributed is a machine-checked proof — including the
Hoffman–Wielandt inequality and the eigenvalue trace inequality for real symmetric matrices
(usually attributed to Ky Fan, Richter and Theobald; von Neumann's inequality is the
singular-value version), formalized from Birkhoff's theorem and the rearrangement inequality
(`HoffmanWielandt.lean` **[V]**) — and its use as a realizability *certificate* for predicted
distance matrices (blueprint §8.1).  A proof by compression to `range(G)` does not work
(`DEAD_ENDS.md` D4).

The first term is the classical-MDS *strain* bound; the second is the *tail trace*, the spectral
signature of an additive-constant or scale error in the distances.

* **Gain over the strain bound.**  Under a uniform bias `D̂ = Δ(X₀) + c(11ᵀ − I)` the strain
  bound is `c √(L−4)` while the trace-enhanced bound is `≈ cL/2` and the optimum is `≤ cL`.
  Measured (benchmark B3): ratio 1.41, 2.0, 2.83, 4.0 at `L = 8, 16, 32, 64`; best configuration
  found within 8–20 % of the bound.  For zero-mean noise the tail trace is ≈ 0 and the two bounds
  coincide.
* **Equality (corrected).**  Equality needs the trace-shifted classical solution
  `G* = Σ_{k≤r} (λ_k + τ/(r+1)) u_k u_kᵀ` to be PSD *and* the residual `G* − Ĝ` to have constant
  diagonal.  A sufficient condition is that the top-`r` spectral subspace is a union of full
  eigenspaces invariant under a vertex-transitive symmetry group of `D̂` (regular polygons with
  `r = 2`: harness IV.3, relative gap `< 10⁻¹²`).  It is **not** enough that `D̂` be
  vertex-transitive: for the regular simplex with `L = 5`, `r = 3` the bound is `1.25` and the
  minimum is `≈ 1.304` (harness DEAD.4; `DEAD_ENDS.md` D12); circulant inputs with `r = 3` are
  strict for the same reason (the cut splits a degenerate eigen-pair).
* **Explicit certificate [V].**  For the regular simplex (all squared distances 1) the bound
  equals `L(L−1−r)/(r+1)` (`simplex_certificate_eq`, `simplex_sstress_lower_bound`); in
  particular no three collinear points are closer than `3/2` in s-stress to an equilateral
  triangle, and the simplex on `L > r+1` points is not realizable in `ℝ^r`
  (`simplex_not_realizable`).
* **Two-sided [K].**  `4‖E‖² + 4(tr E)² ≤ ‖K(E)‖² ≤ 4L‖E‖²` on centred symmetric matrices
  (Tsang–Pereira 2016; the singular values of `K` are `2`, `√(2L)`, `2√L`), so classical scaling
  with the trace shift is within a factor `O(√L)` of the optimal s-stress **provided the
  trace-shifted solution is positive semidefinite** (`λ_r + τ/(r+1) ≥ 0`); without that
  hypothesis the ratio is unbounded by this argument (same example: ratio² `9.6 > (L+2)/2 = 3`).
* **Open.**  The discarded term is the diagonal variance `2L‖diag E − (tr E/L)1‖²`; a lower bound
  retaining a provable share of it, a complete characterisation of equality, and certificates for
  *weighted or incomplete* distance data with bond-length constraints (what structure predictors
  actually emit) were not found in the literature and are not provided here.

### 4.2 Distances versus superposition

* `Σ_{ij} (D_ij(X) − D_ij(Y))² ≤ 2L · min_g ‖X − gY‖_F²`, i.e. dRMSD `≤ √2 ·` RMSD **[K, H]**
  (reverse triangle inequality and centring of the optimal residual; folklore — with the
  pair-normalised dRMSD the sharp constant is `√(2N/(N−1))`, attained by dilations).
* Conversely, for centred `X` of full rank 3 **[K, H]**:
  `min_{g ∈ E(3)} ‖X − gY‖_F² ≤ ‖Δ(X) − Δ(Y)‖_F² / (8(√2−1) σ₃(X)²)`,
  a corollary of the Procrustes–Gram lemma of Tu et al. (2016, Lemma 5.4) and
  `‖G(X) − G(Y)‖_F ≤ ½‖Δ(X) − Δ(Y)‖_F` (a theorem of the same shape is in Arias-Castro,
  Javanmard, Pelletier 2020); `σ₃(X)² = L ·` (smallest principal moment of the
  gyration tensor).  The bound degenerates for flat molecules, correctly (out-of-plane buckling
  changes distances to second order), and it concerns alignment *including reflections*:
  distances cannot see chirality, frames can.
* Frame-aligned error matrices `P_ij` give `RMSD ≤ min_i (L^{-1} Σ_j P_ij²)^{1/2}` and
  `TM ≥ max_i L^{-1} Σ_j (1 + (P_ij/d₀)²)^{-1}` because each frame defines one admissible
  superposition **[K]** (this is the pTM construction, Jumper et al. 2021, SI 1.9.7).  No
  rigorous guarantee from local scores (lDDT) to global RMSD was found.

### 4.3 Holonomy obstructions on frame graphs

**Theorem 4.4 [V] (`Holonomy.lean`).**  In a group with a conjugation-invariant norm (e.g. SO(3)
with the geodesic angle), for a closed cycle with vertex frames `x_0, …, x_m = x_0` and measured
edge transforms `ĝ_k`,

    ‖ĝ_0 ĝ_1 ⋯ ĝ_{m−1}‖  ≤  Σ_k ‖ĝ_k (x_k^{-1} x_{k+1})^{-1}‖,
    ‖hol‖² ≤ m Σ_k ‖err_k‖².

The holonomy of the measurements is a lower bound on the total edge error of *any* assignment of
absolute frames.  (Known: Lerman–Shi 2022, Lemma 1; the statement here is for arbitrary groups
with a conjugation-invariant norm and is instantiated for linear isometries with the chordal
norm.)

SE(3) has no bi-invariant metric; its semidirect structure gives instead:

**Theorem 4.5 (translation holonomy with lever arms) [V].**  With measured relative rotations
`R̂_k` (errors `ρ_k` in operator norm) and translations `t̂_k`, accumulated rotations
`P_k = R̂_0 ⋯ R̂_{k−1}` and `t_hol = Σ_k P_k t̂_k`, for every closed assignment of frames and
positions

    ‖t_hol‖ ≤ Σ_k ‖t̂_k − t_k^{true}‖ + Σ_k (Σ_{l<k} ρ_l) ‖t̂_k‖.

Rotational errors early in the cycle are amplified by the length of the remaining path.  The two
inequalities define, per cycle, a polyhedral set of admissible (rotation error, translation
error) profiles; in the abelian case the least-squares error is exactly `hᵀ(CCᵀ)^{-1}h` in cycle
space (discrete Hodge decomposition) **[K]**; for angle-valued data this holds only modulo the
integer lattice, and a sharp non-abelian Hodge-type lower bound is, to our knowledge, open; the
closest known results are the two-sided spectral (Cheeger-type) bounds for synchronisation of
Bandeira, Singer and Spielman (2013) and semidefinite dual certificates (`prior_art/L3`).

### 4.4 Torsion errors and superposition RMSD: reduced moments of inertia

`RigidWithin X Y c` means that some isometry `g` of the ambient space (possibly improper)
achieves `Σ_i |X_i − gY_i|² ≤ c²`, so that the RMSD after superposition by an isometry is at
most `c/√N`; `RigidWithinIn G X Y c` restricts `g` to a group `G` of motions.  Every statement
below holds in the restricted form for any `G` that contains the rotations about the torsion
axes (`IsTorsionMove.rigidWithinIn_exact`, `IsTorsionMove.rigidWithinIn_min`,
`rigidWithinIn_torsion_chain_min`), because the superposing motion constructed in the proofs is
a rotation about the torsion axis.

**Theorem 4.6 [V] (`TorsionRMSD.lean`).**
(a) *Chain rule.*  `RigidWithin` composes additively: if `X^{(k)}`, `X^{(k+1)}` are within `c_k`
for `k < m`, then `X^{(0)}`, `X^{(m)}` are within `Σ_k c_k` (`rigidWithin_chain`; Minkowski plus
isometry invariance; also for superpositions restricted to a submonoid of motions).
(b) *Exact coaxial cost.*  Rotating a set `B` of unit-mass atoms by `φ` about an axis while `A`
stays fixed, and re-superposing by a rotation `ψ` about the same axis, costs
`2 I_A (1−cos ψ) + 2 I_B (1−cos(φ−ψ))` (`coaxial_cost_eq`); its minimum over `ψ` is

    C(φ) = 2S − 2√(S² − 4 I_A I_B sin²(φ/2)),     S = I_A + I_B

(`exists_coaxial_angle`, `coaxial_cost_ge`), with `I_A, I_B` the moments of inertia about the
axis.
(c) *Two-sided reduced-inertia bounds.*
`4 I_red sin²(φ/2) ≤ C(φ) ≤ 4 min(I_A, I_B) sin²(φ/2) ≤ 8 I_red sin²(φ/2)`,
`I_red = I_A I_B/(I_A + I_B)` (`reduced_le_coaxial_cost`, `coaxial_cost_le_min`,
`min_inertia_le_two_reduced`, `coaxial_cost_le_reduced`).
(d) *Torsion moves.*  A single torsion move by `δ` is within
`2√(min(I_A,I_B)) |sin(δ/2)| ≤ 2√(2 I_red) |sin(δ/2)|` (`IsTorsionMove.rigidWithin_min`,
`IsTorsionMove.rigidWithin`); a sequence of moves is within the sum
(`rigidWithin_torsion_chain`), and the superposition distance is Lipschitz in each torsion angle
with constant `√(2 I_red)` (`rigidWithin_torsion_chain_abs`).

Hence torsion changes `δ_k` move the structure by at most
`N^{-1/2} Σ_k 2 √(min(I_A,I_B)_k) |sin(δ_k/2)|` in RMSD after optimal superposition by a motion
of `G` (`rigidWithinIn_torsion_chain_min` **[V]**), the inertias being those of the intermediate
conformations.  For `G` the proper rigid motions this is the Kabsch (proper-rotation) RMSD
**[P]**: the group `SE(3)` itself is not defined in the development, the verified statement is
for an arbitrary group containing the axis rotations.  Compared with the naive lever-arm bound
(rotate the distal part regardless of its weight, no re-superposition) the certificate is
≈ 2–2.5× tighter on idealised chains (benchmark B7).  That baseline is weak: against the obvious
choice — superpose the heavier side exactly, cost `4 min(I_A, I_B) sin²(φ/2)` — the exact coaxial
cost gains at most a factor `√2` in RMSD, since `C(φ) ≥ 4 I_red sin²(φ/2) ≥ 2 min(I_A,I_B)
sin²(φ/2)` (`reviews/R1`, item 11).  The bound is a worst-case (`ℓ¹`) bound and overestimates
independent random errors by `≈ √m` (`DEAD_ENDS.md` D10).

**Corollary 4.7 (envelope of an invariant residual) [V] (`InvariantEnvelope.lean`).**  Let `G` be
a group of rigid motions and let the residual `Δ` be `G`-invariant and `Λ`-Lipschitz in the `ℓ²`
configuration distance.  Then `|Δ(X) − Δ(Y)| ≤ Λ c` whenever some motion of `G` superposes `Y`
onto `X` within `c` (`invariant_lipschitz_of_rigidWithinIn`).  If `G` contains the rotations
about the torsion axis — as the proper motions `SE(3)` do **[P]**, and a fortiori all isometries
`E(3)` — one torsion move changes the residual by
at most `Λ · 2√(2 I_red)|sin(δ/2)|` (`residual_torsion_move_in`, `residual_torsion_chain_in`;
`residual_torsion_move`, `residual_torsion_chain` are the `E(3)` case).  `I_red` is the reduced
inertia at the current conformation; with a conformation-independent bound `I_red ≤ Ī_i` for
torsion `i` the constant is the uniform `c_i = Λ · 2√(2 Ī_i)` (`residual_torsion_move_uniform`),
and then `Δ ∘ emb` lies in the residual class of the certificate kernel for any published
constants `≥ c_i` and anchor values `≤ Δ` (`residualLowerClass_of_invariant_lipschitz`), so an
accepted residual certificate bounds `E + Δ ∘ emb` (`verifyR_sound_invariant`; for interval
anchor data and the top-level kernel, `verifyITop_sound_invariant`).  This turns an
invariant architecture with a Cartesian Lipschitz certificate and an inertia bound into the
bounded-difference envelope required in §2 and §6.  (The bound `Ī_i` is a modelling input: e.g.
the axial inertia of the lighter side of the torsion, bounded over the conformations considered.)
The generalisation from all isometries to a group `G` has verified content: for `G` the group
generated by the rotations about one axis and the signed height difference along that axis —
a residual that is *not* invariant under the mirror reflection — the bound applies
(`signed_offset_residual_torsion_bound`, with `Δz_not_rigidInvariant`), whereas the `E(3)` statements
do not.  That a particular architecture is invariant under all proper motions is an input.

*Prior art.*  The small-angle content is classical: the reduced moment of inertia of internal
rotation (Pitzer–Gwinn 1942), optimal superposition and the Eckart conditions (Kudin–Dymarsky
2005), the torsion-space metric tensor (Gō–Scheraga 1976; Noguti–Gō 1983), the zero-momentum
property of superposed torsion updates (DiffDock, Prop. 1), and the one-body formula
`RMSD² = (4/W) sin²(α/2) I(n)` (Popov–Grudinin 2014).  The finite-angle two-body closed form
`C(φ)` as a bound on the Kabsch cost and the chained bound were not found (`prior_art/L3` §C13,
medium confidence).  Two classical relatives, pointed out by the science division
(`SCI-REV-0006` W10): `C(φ) = 2(S − |I_A + I_B e^{iφ}|)` is the residual of a *planar* weighted
Procrustes problem (equivalently `2S` times the weighted circular variance of the two angles
`0, φ`); and the chained bound without re-superposition — a weighted `ℓ¹` bound `Σ_i R_i|Δq_i|`
with lever arms `R_i`, in the supremum norm over the points of a link — is Lemma 2 of
Schwarzer–Saha–Latombe (2005), where it certifies that a path segment of an articulated robot
is free of collisions.  Not there: superposition, reduced inertias, the root-mean-square norm.
The natural sharpening — replacing the `ℓ¹` chain by the Eckart-frame metric
tensor at finite angles — is open.

---

## 5. Direction B — exact arithmetic and the rational torus

We did not attempt new relaxation theorems: α-BB and its generalisations, convergence orders and
the cluster problem are mature (Adjiman et al. 1998; Skjäl et al. 2012; Bompadre–Mitsos 2012;
Kannan–Barton 2017), sum-of-squares rates on the torus are known (Bach–Rudi 2023), and verified
interval branch-and-bound exists in Lean 4 (LeanCert 2026; girving/interval).  What the program
needs from this direction is a *sound numerical semantics* for its certificates
(`Core/Rounding.lean` **[V]**):

* **Outward rounding.**  `roundDown p q = ⌊q 2^p⌋/2^p ≤ q ≤ ⌈q 2^p⌉/2^p = roundUp p q`, width
  `≤ 2^{−p}`, monotone; `QInterval` with `add, neg, sub, mul, scale, sq, inv, hull, outward` and a
  containment theorem for each.
* **Certified exponential.**  `expLo n k q ≤ exp q ≤ expHi n k q` for `|q| ≤ 2^k`, `n ≥ 1`
  (Taylor polynomial with Mathlib's remainder after `k` halvings, then repeated squaring);
  `contains_boltzmann` encloses `exp(−β e)` for an enclosed energy `e`.
* **Rational atlas of the circle.**  Every unit vector is a quarter turn of
  `((1−t²)/(1+t²), 2t/(1+t²))` for some `|t| ≤ 1/2` (`circle_rational_atlas`).  In these charts
  `cos θ_i`, `sin θ_i`, forward kinematics, squared distances and torsional terms are rational
  functions of `t` with rational coefficients (for bond geometries given by rational points of
  the circle), and the 12-6 Lennard-Jones term is rational in `r²`; the arc measure is
  `2 dt/(1+t²)`.  Square roots (Coulomb) and exponentials (screening, Boltzmann factors) enter
  only through enclosures that a checker verifies by multiplication.

Caveats recorded by the literature check: bond-angle sines are irrational in general (use
enclosing rational points and outward rounding), Lennard-Jones poles must be excluded by a
certified positive lower bound on `r²` (the `inv` rule requires `0 < lo`), and total arc lengths
involve `π` (only rational bounds are needed).  Every ingredient is standard; the assembled
transcendental-free pipeline for chain energies was not found in the literature.

---

## 6. Direction E — certificate algebra

### 6.1 Kernels and Master Soundness Theorems

`CertificateAlgebra.lean` defines rational pairwise instances on `n` sites with `k` states,
domains as lists of surviving states, and certificates

    leaf u p m | branch i children | prune i r t ℓ rest | sum I₁ I₂ L₁ L₂ c₁ c₂ .

* `leaf`: messages `m`; checks `u_i ≤ h_i(a) + Σ_j m_ij(a)`,
  `2 p_ij ≤ J_ij(a,b) + J_ji(b,a) − m_ij(a) − m_ji(b)` on the current domains and
  `L ≤ Σ u + Σ p` (the pairwise LP dual bound with the dual solution supplied);
* `branch`: one child per surviving state of a site;
* `prune`: DEE with claimed per-neighbour bounds `ℓ_j` of the link terms and a required margin;
* `sum`: `I ≥ I₁ + I₂` termwise on the box, `L ≤ L₁ + L₂`, each part certified separately.

**Master Soundness Theorem [V] (`verify_sound`).**
`verify c I D L = true  ⟹  ∀ x ∈ ∏ D,  L ≤ E_I(x)`.

**Residual kernel [V] (`verifyR_sound`, `certified_gap`).**  A residual problem consists of the
pairwise part, bounded-difference constants `c`, and evaluated anchors.  Certificates may branch,
prune by *differential* DEE (margin `≥ c_i`), or select an anchor and hand the anchored pairwise
minorant to the kernel above.  If `verifyR c P D L = true` then for **every** residual `g` with
those bounded differences and anchor values, `L ≤ E(x) + g(x)` on the box; with an anchor in the
box the true optimum lies in `[L, E(a) + v]`.  The quantifier is the point: one accepted
certificate is a statement about a whole class of energy functions, where proof logging as
practised certifies a statement about one given instance (§6.4).

*Side conditions are checked, not assumed: interval anchor data.*  `verifyR` checks rules only;
if the published data are unsatisfiable — a negative constant, or two anchors whose values
differ by more than the envelope allows — its soundness theorem holds vacuously
(`inconsistentResidual_unguarded`: the bound `41/4` is accepted on a problem whose pairwise
minimum is `1`).  The top-level kernel `verifyITop` therefore takes *interval* anchor data: at
each anchor `x_p` the residual is published as `lo_p ≤ Δ(x_p) ≤ hi_p`, the upper value being
optional (an exactly known value is `lo = hi`; a floating-point evaluation is
`[fl − err, fl + err]`).  The decidable condition

    c ≥ 0   and   lo_p − hi_q ≤ Σ_i c_i [x_p,i ≠ x_q,i]   for all ordered pairs with an upper value

(`IProblem.Consistent`) is *exactly* non-emptiness of the class of residuals with these data
(`IProblem.consistent_iff_nonempty` **[V]**; the McShane lower envelope of the lower values is
the witness).  A legitimate producer always satisfies it, and incompatible evaluations are
rejected even after rounding (`inconsistentInterval_rejected`).  `verifyITop_sound` **[V]**: if
the kernel accepts, the class is non-empty, and for every member `L ≤ E + Δ` on the box and
`E(x_p) + Δ(x_p) ≤ E(x_p) + hi_p` at every anchor with an upper value — so an anchor inside the
box brackets the optimum in `[L, E(x_p) + hi_p]`.  The rule checker only ever uses the lower
values (`verifyR_sound_lower` **[V]**).  Two special cases have their own names: exact values
(`verifyRTop`, `verifyITop_ofExact`) and lower values only (`verifyRLowerTop`,
`verifyITop_ofLower`); in the latter no upper value is published, so nothing but `c ≥ 0` can be
checked and no upper bound on the optimum is certified — it should be used only when upper
evaluations are genuinely unavailable.

**Real-valued energies [V] (`verify_sound_real`, `verifyR_sound_real`).**  If the published
rational instance is a termwise *lower* instance of a real pairwise model (every table entry
rounded down, §5), an accepted certificate bounds the true real energy — with or without the
unknown residual.  This is the minimisation counterpart of `Z_encloses_partitionFn`: floating
point may be used upstream of the certificate provided the published tables are rounded down
and, for residual problems, the published constants are rounded up and the anchor intervals
outward (lower values down, upper values up).

**Partition-function kernel [V] (`zverify_sound`, `zverifyTop_sound`, §3.4).**

All three kernels are evaluated on concrete instances by `decide +kernel` (Lean's trusted kernel,
no compiler in the trusted base, no extra axioms): `triangle_verified`, `triangle_rejects`,
`biased_verified`, `triangleResidual_verifiedTop`, `inconsistentResidual_rejected`,
`negativeEnvelope_rejected`, `triangleInterval_verified`, `inconsistentInterval_rejected`,
`triangleZ_exactTop`, `negativeW_rejected`.

### 6.2 Verification cost and witness size

Each `leaf`, `prune`, `sum` node is checked by one pass over the instance tables restricted to
the current domains — `O(Σ_i |D_i| + Σ_{i≠j} |D_i||D_j|)` rational comparisons, i.e.
`O(Σ_i |D_i|·deg(i) + Σ_{i≠j} |D_i||D_j|)` arithmetic operations including the message sums —
and a `branch` node by one list traversal; the verifier never minimises or searches.  A node's
witness is the dual solution (`O(k)` messages per ordered pair of sites, i.e. `n²k` rationals per
leaf in the format used) or `O(n)` link bounds.  This is the regime
"large witness, linear-time check"; a witness without dual solutions would be smaller but force
the checker to solve an LP (the hint trade-off familiar from LRAT-style proof formats).

### 6.3 The decomposition rule is necessary relative to pairwise-LP leaves (known phenomenon, formalized)

The separation below is relative to the leaf rule of this kernel (pairwise reparameterisation,
i.e. the local-polytope LP) and is proved on a *disconnected* family.  A stronger leaf — e.g. one
with triplet consistency — certifies `m` triangles in a single leaf, so "necessary" is a
statement about this rule set, not about decomposition as such (`reviews/R1`, item 12); lower
bounds for connected families (triangles coupled weakly along a chain) and for
decomposition-aware certificates are open.

**Theorem 6.1 [V] (`ProofComplexity.lean`).**  (a) *Two-configuration weak duality*
(`leaf_two_config`): for an accepted leaf with bound `L`, any two configurations `x, x'` of the
box and any crossing pattern `χ`, `4L ≤ 2 Σ_i (h_i(x_i) + h_i(x'_i)) + Σ_{i≠j} Pat_ij`, where
`Pat_ij` evaluates the symmetrised pair table on `(x_i,x_j),(x'_i,x'_j)` or on the crossed pairs
`(x_i,x'_j),(x'_i,x_j)`.  (b) Every leaf on the full domain of the frustrated triangle certifies
at most `0`, although the optimum is `1` (`triangle_leaf_gap`, `triangle_no_leaf_certificate`):
pure reparameterisation certificates are incomplete.  (c) For `m` disjoint frustrated triangles
(optimum `m`, `triangles_energy_opt`), every certificate without `sum` that the kernel accepts
for the bound `m` visits at least `2^m` leaves — including certificates that use DEE steps
(`sumFree_exponential`, `sumFree_size_exponential`); the bound is attained (`sumFree_tight`).
Approximation does not help much: certifying any bound `L ≥ m − d` still needs `2^{m−d}` leaves
(`sumFree_gap_exponential`), and the exact sum-free complexity of the bound `K ≤ m` is `2^K`
(`sumFree_complexity`).
(d) With `sum`, `2m` visited leaves suffice for every `m ≥ 1` (`sum_linear`), hence for `m ≥ 3`
there is an accepted certificate that visits fewer leaves than every accepted sum-free
certificate (`sum_rule_separation`).  Leaves are not the whole cost — a `sum` node stores two
sub-instances — so the separation is also proved for the node count (`4m − 1` against `≥ 2^m`,
`m ≥ 4`: `sum_rule_separation_size`) and for the description length `Cert.dataSize`, which
charges every node for all rational table entries it stores: at most `147 m³` with `sum`, at
least `2^m` without, hence strictly smaller for `m ≥ 21` (`sum_rule_separation_dataSize`; harness VII.1 searches all
sum-free certificates with and without the prune rule up to `m = 5`, VII.2 recomputes the
description lengths).

*Proof idea of (c).*  Call a block *untouched* while all its sites have both states.  For a
domain with a witness of block energy `≤ 1` everywhere, (a) with `x'` the complement of `x` on
untouched blocks shows that a leaf certifies at most the number of touched blocks; a DEE step
cannot fire inside an untouched block (its Goldstein margin is `−2`) and preserves the invariant
elsewhere; a branch on an untouched block keeps the invariant for both children and decreases
the count by one.  Induction gives `2^{#untouched}` visited leaves.

The separation is the tree-like versus DAG-like one known for branch-and-bound (Jeroslow 1974;
Basu–Conforti–Di Summa–Jiang 2023, Thm 2.2, for exactly this family in the independent-set
formulation, with `2^{m+1} − 2` nodes) and exploited by AND/OR search (Dechter–Mateescu 2007).
It is included because it is the precise reason the `sum` constructor belongs to the algebra,
and, to our knowledge, it had not been machine-checked for an LP-dual/DEE certificate system.
Open: size bounds for decomposition-aware certificates on *weakly coupled* chains.

### 6.4 Relation to existing certified solving

Proof logging with verified checkers is routine for SAT, pseudo-Boolean optimisation (VeriPB,
CakePB; importable into Lean 4 by PBLean), MIP (VIPR, exact SCIP, LeanVIPR) and exact model
counting (Bryant et al. 2023, Lean 4); since 2024 there are formally verified certificates for
approximate model counting (Tan et al. 2024) and since 2026 for solution enumeration (McCreesh
et al. 2026), and a two-sided certificate scheme with pruning exists for stochastic SAT
(Cheng–Luo–Jiang 2024).  Neither OSPREY nor toulbar2 emits checkable proofs, and no proof
logging for cost-function-network / MAP lower bounds, DEE steps or deterministic two-sided
bounds on partition functions was found (`prior_art/L1` §C4(ii); re-searched in November 2026 by
the science division, `SCI-REV-0006`, whose reading level for each source is recorded in its
report A2 §4.1 — we have not re-read the sources of this paragraph that are dated after 2023).

*What this does and does not mean.*  The kernels here are *native* certificates for that
problem class: a reparameterisation is a linear-size witness for a local-polytope bound, a DEE
step is a pair `(r, t)` with link bounds, a thermal step adds a ratio.  For the pairwise kernel
the ingredients have verified checkers in the pseudo-Boolean setting: a reparameterisation
bound is a linear-programming bound of the 0–1 encoding (a Farkas certificate), a DEE step has
the form of a dominance step; formally verified pseudo-Boolean optimisation with such bounds is
reported to check within a factor 20 of solving time (median 1.43; Koops et al. 2025), native
MaxSAT proof logging with a median overhead below 2 % (van Doren et al. 2025; unverified
checker), and certificates made of equivalence-preserving transformations — reparameterisations,
in the Boolean case — exist for MaxSAT (Py–Cherif–Habet 2022; unverified checker).  Nobody has
written such a proof for a cost-function network; but whether a native format is cheaper than
that route has not been measured (a comparison is proposed to the engineering division in
`SCI-REV-0006` §7), and an argument from checking cost — the first version of this section and
`prior_art/L1` leaned on a factor 43 for certified branch-and-bound MaxSAT — is out of date.
The kernels here are sound without `native_decide`, which the Lean route through PBLean needs,
and evaluation inside the Lean kernel does not scale (§12, item 7): the trade-off between
trust base and scale is unmeasured as well.

*What has no counterpart in the systems read.*  Every proof-logging system above certifies a
statement about *one instance* ("this solution is optimal for this formula", "the count is
`n`").  The residual kernel certifies `L ≤ E(x) + g(x)` for *every* residual `g` of an envelope
class consistent with interval anchor data, and decides non-emptiness of that class
(`verifyITop_sound`, `IProblem.consistent_iff_nonempty` **[V]**) — closer to robust optimisation,
where certificates are dual solutions of robust counterparts, than to proof logging.  This, and
the deterministic two-sided bound on a weighted sum of §3.4, is what distinguishes the kernels;
the evidence is a comparison of statements for the systems read and an absence in searches,
not a proof of novelty (`SCI-REV-0006` M1).

LeanCert-style verified interval evaluation is complementary: it can supply the continuous
leaves (table entries as enclosures of energies over voxels) that the present kernels take as
input.

---

## 7. Challenge 4 — what the theory implies for architectures and samplers

We prove no new expressivity or mixing theorem; the following are consequences of §§2–3 and
§11.

1. **An architecture is certifiable only through the envelope it exports, and the price of the
   envelope is quantified.**  For an energy `E₀ + Δ_θ` with a learned residual, every guarantee
   above uses `Δ_θ` only via `d` and anchors.  The looseness `1−κ` of a certified first-order
   envelope is paid in evaluations: the evaluated set must cover every configuration within
   slack radius `gap + ε` (Theorem 11.4), which on product landscapes means *one* evaluation if
   every site is sharp and exponentially many otherwise, with exponent
   `max_t Σ_i [ln Z_i^{gap}(t) − ln Z_i^{slack}(t)]` (Theorems 11.7–11.9), and at finite
   temperature at least `exp(entropy)` evaluations (Theorem 11.13).  Theorem 3.1 turns the
   same constants into a free-energy uncertainty: `β² Σ c_i²/8` relative to a product
   (independent-site) reference, with the constant `1/8` optimal, and `β² (Σ c_i)²/8` relative
   to an arbitrary one (approached as `β → 0` by perfectly correlated sites, harness III.6; no
   sharpness theorem is formalized for this case).  Design rule:
   *put steep, structured physics (sterics, electrostatics) in the explicit part and constrain
   the residual to have small certified per-site variation*; unbounded Lipschitz constants are
   incompatible with certification, not merely inconvenient.
2. **Expressivity/certifiability trade-off.**  Tight envelopes need the residual's variation to
   be attributable to few sites (small `c_i`) — a restriction of the hypothesis class.  The
   contact-set theorem shows what is gained: the possibly-optimal set shrinks from the energy
   window to the contact set (benchmark B1).
   **The kind of envelope matters more than its size (§11.7).**  A bound on the *non-additive*
   part of the residual — mixed second differences `c_ij` — makes `n(k−1)+1` evaluations on a
   star sufficient for an exact reduction to a pairwise problem (Theorems 11.16–11.17), whereas
   no first-order constant, however small, avoids the exponential price at a non-sharp site.
   The reduction is useful under weak coupling only — sparse constants, or row sums `Σ_j c_ij`
   below the scale of the gaps; with dense constants of order one the remainder of the star
   envelope is quadratic in the Hamming distance and nothing is gained (§11.7, `DEAD_ENDS.md`
   D32).
   For a learned residual this suggests exporting certified mixed-difference constants (e.g.
   from an architecture that is a sum of one- and two-site terms plus a small bounded
   higher-order remainder) rather than per-site Lipschitz constants.  Certifying such constants
   for a concrete network is not part of this development.
3. **Chirality.**  Any function of pairwise distances is invariant under reflections, so
   distance-based certificates (Theorem 4.3, §4.2) are blind to chirality by construction; frame
   data (§4.3) are not.  This is the realizability-side counterpart of the known incompleteness
   of distance-only invariant networks.
4. **Sampling.**  (a) A sampler of the reference ensemble is a certified approximate sampler of
   the target: `KL(reference ‖ target)` is exactly the sandwich gap
   (`kl_reference_target_eq_gap` **[V]**), hence at most `β² Σ c_i²/8` when the reference is a
   product measure (constant `1/8` optimal) and at most `β² (b−a)²/8 ≤ β² (Σ c_i)²/8` for any
   reference, e.g. a tree-structured or autoregressive sampler.  (b) Thermal dominance
   bounds the change of every bounded observable under pruning by `2B e^{−βγ}`
   (`boltzmannAvg_dominance_error` **[V]**), and the robust partition bracket controls ensemble
   weights deterministically.  (c) The transport–entropy duality (§3.2, Theorem 11.14) identifies
   the property of a reference sampler's stationary law that makes second-order corrections
   uniformly valid.  (d) A reference *average* of the residual is exponentially more informative
   for free energies than the same number of pointwise evaluations used deterministically
   (§11.6, last paragraph).
   Convergence-rate (mixing) theory for torsional diffusion or Langevin samplers on `T^M` is
   outside what was established here.

---

## 8. Limitations

* **Certification, not solution.**  Membership in the contact set, and the query-model criterion,
  are themselves optimisation problems; the theorems say what a certificate must and may contain,
  not how to find it.
* **Finite configuration spaces.**  §§2–3 are stated for finite sets; continuous variables enter
  through voxel enclosures (zeroth order formalized end to end for pairwise energies on product
  voxels, and the separable-envelope step formalized; the Taylor step that produces second-order
  envelopes from Hessian bounds is on paper, and voxel enclosures of the *tables* themselves —
  interval evaluation of the energy terms over cells — are an input).
* **Extensivity** of the free-energy sandwich (§3.2), and its **product-reference hypothesis**:
  the `Σ c_i²` width is proved (and true) only for independent-site references; for correlated
  references the formalized bound is the Hoeffding width `(Σ c_i)²`.
* **Envelope constants are inputs.**  The certificates are sound *given* bounded-difference
  constants (and, for Corollary 4.7, a Lipschitz constant and inertia bounds).  Certifying such
  constants for a concrete learned residual is not part of this development.
* **Worst-case geometry bounds** (Theorem 4.6 is `ℓ¹`; Theorem 4.3 is tight only for symmetric
  inputs, and within `√((L+2)/2)` only when the trace-shifted solution is positive semidefinite).
* **The exponent theorems of §11 are half formal.**  The lower bounds (Theorems 11.8, 11.13,
  11.23, 11.24 and their product forms) are machine-checked for every system size; the matching
  upper bounds (Theorems 11.9, 11.15, 11.25(b,c)) are paper proofs through the type covering
  lemma or Harper's theorem, for independent sites of finitely many types; numerically, the
  single-letter identities and, for two-state sites, exact layer and ball counts were checked,
  not achievability at finite size in general.  Theorem 11.15 needs accuracies that are not
  exponentially small (`DEAD_ENDS.md` D29), and so do the soft-gap exponents of §11.10 (D35);
  only on the cube at the zero residual are all accuracy regimes treated (Theorem 11.25).
* **The query-complexity statements are instance-wise, and beyond the cube they are bounds.**
  The costs of §11.10 are those of algorithms that are correct on the whole class but tailored
  to one instance (a hint); no algorithm attains them on all instances.  Thresholds are
  worst-case statements over the instances of a class.  At finite temperature, beyond the
  uniform cube, single dips are not the extremal perturbations when sites have three or more
  states (D38), so the dip exponent `R^rand_β` and its threshold `ε₁^crit` are lower bounds only;
  the generalised exponent `R^gen_β` of Theorem 11.27 is a machine-checked lower bound whose
  tightness rests on a paper proof checked by one referee; the thresholds of Theorem 11.28 are
  proved for identical sites at additive instances.
  "Every randomised algorithm" means every finite mixture of the abstract deterministic
  algorithms of `QueryLowerBound.lean`.
* **Evaluations are counted, not computation.**  §11 counts residual evaluations; by §11.10 the
  lower bounds hold for every algorithm, also randomised.  Finding a small certificate is
  NP-hard (Theorem 11.10), no search procedure is instance-optimal (`DEAD_ENDS.md` D26), and
  *checking* a certificate with anchors `A` on a product space is a `min_y max_{a ∈ A}` problem
  over pairwise models — coNP-hard in general (covering radius) and, in the non-sharp regime,
  over an exponentially large `A`; the kernels avoid this only through explicit
  branch-and-bound certificates (§6).
* **Second-order envelopes are an interface without an instance, and help only under weak
  coupling.**  No concrete residual with certified mixed-difference constants is provided, and
  the remainder of the star envelope grows with the square of the Hamming distance: with dense
  constants the exponential covering problem returns (§11.7; `DEAD_ENDS.md` D32).
* **The route from chain geometry to certificates does not scale as built.**  The verified
  per-torsion constants of §4.4 grow like `m^{3/2}` with the distance to the chain end, and with
  growing constants a weighted-Hamming envelope makes certification exponential with almost
  full exponent (§11.14).  The kernels remain sound; what fails is the hope that this envelope
  format makes long chains certifiable.  §§11.13–11.14 are paper results of independent
  workstreams, re-derived by reviewers but not machine-checked, and they ignore excluded
  volume.
* **Without a hint, exponents only, and only on the cube** (§§11.16, 11.18).  The exponent of
  non-adaptive algorithms is `θ_na`, that of adaptive ones `θ_hint` — the latter by a nested
  algorithm whose cost analysis is a paper proof (machine-checked are the analysis of its
  recursion, for the cube's own exponent functions, and the validity and width of its
  bracket, not its number of evaluations), with
  `o(n)` terms that make it useless at any size one could simulate.  The extension to every
  bounded accuracy (§11.19: exponent `h` against `a` non-adaptively) is a paper proof by a
  workstream, refereed ("proved": R8) and run with three nested levels only on cubes of ten
  coordinates and, at large size, at the flat instance; below the exponential scale nothing
  is known without a hint.  How many rounds of adaptivity the exponent `h` needs is known only
  in part (§11.24, a workstream's paper proofs, refereed by the Scientific Discovery
  Division, SCI-REV-0003: no critical finding; the cost bound of the batched schedule held
  on the good event only and needed a stopping rule): for every `η > 0` a number of rounds
  independent of `n` suffices for `h + η` — whether a fixed number suffices for `h` is open,
  and our first version said "suffices" without the `η` —, two rounds do not reach `h`, and
  for three or more rounds there is no lower bound above `h` and no algorithm better than a
  slowly converging recursion.  The two-round separation is asymptotic: no finite size is
  known at which a two-round lower bound exceeds the cost of a known adaptive algorithm.
  All upper bounds rest on Harper's
  theorem, which is cited, and on paper reductions to it.  The one step beyond the uniform
  cube — a field as known part, §11.20 — is a workstream's paper proof, refereed (R9: the
  isoperimetric theorem and the non-adaptive exponent proved; the adaptive upper bound
  proved after two gaps in the algorithmic proof were closed); it rests on a new asymptotic
  isoperimetric statement proved by the method of types whose error term is of the poor
  kind (`n^{-1/8}` from the proof), gives exponents at extensive accuracies only, its nested
  algorithm uses a table of numbers for which no formula is known and has never been
  simulated end to end, and that a single tilted product measure is strictly worse than the
  type-uniform sample is established numerically in three examples at extensive
  accuracies only — at vanishing accuracy the best one *ties* with it in the lower bound
  (capacity = information radius; an observation of the Scientific Discovery Division).
* **A known part with interactions is understood only when it is a function of the type,
  and there only in part** (§11.23).  The section is a workstream's paper proof that has
  been checked and re-computed by the coordinator and **refereed (R10)**; the referee
  found one general statement false (the junction with the uniform cube at large slopes)
  and one interval unproved at its upper end, in a section whose numbers the coordinator
  had re-computed — at one slope only (`DEAD_ENDS.md` D53).  What is proved
  for every `n` uses nothing but permutation symmetry (the flat-histogram sample among
  non-adaptive algorithms; the flat-histogram instance among *symmetric* instances).  The
  exponents are a single-letter supremum whose value is known for convex rate functions
  only: with two phases the value at vanishing accuracy is a number supported by searches
  (`0.0251012` at `βJ = 1.5`, `u = 1`, between proved bounds `0.0251012` and `0.0291391`), and
  beyond a small accuracy only lower bounds from profiles with up to seven block types are
  known.  **The exponent of adaptive algorithms without a hint is open for interacting
  known parts, with one exception** — the nested algorithm does not transfer; the route
  through a mixture of fields gives the uniform cube's exponent as an upper bound for
  ferromagnets (Proposition 11.81(c), given Theorem 11.64; the completion of the
  workstream's sketch follows the referee and has not been refereed in turn), which is
  exact where the single-letter value equals the uniform cube's (no field and `βJ ≤ 1`;
  with two phases up to a junction that is known numerically only) and not tight beyond;
  the repair proposed in §11.23 is unproved — and so is the statement that the
  flat-histogram instance is the hardest of *all* instances.  §11.25 (the coordinator's paper proofs,
  reviewed by the Scientific Discovery Division, SCI-REV-0001) adds an upper bound that
  needs no assumption on the interaction — the uniform cube's — for **two of the three
  exponents**, the hinted one of symmetric instances and the non-adaptive one, and equality
  for interactions without a field and with one phase (the first version said "for the
  three exponents", meaning the three items of Corollary 11.91; finding M1 of the review);
  for adaptive algorithms it only *reduces* the question to the uniform measure on one
  type class, where the adaptive exponent is a conjecture (the proof of Theorem 11.56 has
  not been redone on products of type classes), and it does not close the gap between
  the single-letter lower bound and the bound from type classes when exits that change
  the type matter (a field; two phases beyond the junction).
* **For observable free energies — differences between macrostates — only the range is
  understood, not the cost of narrowing it** (§11.28; the coordinator's paper proofs,
  reviewed and replicated by the Scientific Discovery Division, which also searched the
  prior art at summary level: for a separable envelope the theorem is the classical
  closed form of the density-ratio class).  The duality is exact on every finite space
  with a quasi-metric envelope, but the programme has as many variables as the two
  macrostates have states; closed forms exist for one state, for thresholds of the order
  parameter on the cube, for one-coordinate macrostates with independent sites, and at
  the exponential scale for macrostates defined by the type.  For a pairwise known part
  only a bracket with a site-local certificate is proved; for macrostates defined by a
  counting statistic (a number of contacts) nothing beyond the general duality.  The
  query complexity of certifying a ratio is open.
* **The one class whose cost does not grow with the system presupposes what nobody has
  for a physical remainder** (§11.30; elementary; **unrefereed**).  Box classes need exact
  samples from the Gibbs measure of the known part — available for product measures and
  for known parts of small treewidth, not for a general pairwise function — and a
  *certified* floor, a bound on how far below the known function the truth can lie, which
  for no force-field term exists today; the measured sup-norm remainders of the
  Scientific Discovery Division are observations on enumerated or sampled sets, not
  floors.  The certificates are probabilistic and no kernel of this repository checks
  them.  The result is about `ln Z` of the whole domain; neither minima nor ratios of
  macrostate weights are covered.
* **Local averaged data** (§§11.27, 11.29): the statements are about exact marginals given
  for free; that they change no class exponent is proved on the cube without a known
  part (all orders `k = o(n/ln n)`) and with a field for one-body marginals only (the
  Scientific Discovery Division's theorem, not machine-checked); the exponent *at an
  instance* with such data is known only up to a bracket.
* **For more than two letters and several site types the theory is a workstream's paper
  proof by transfer** (§11.26; **reviewed by the Scientific Discovery Division,
  SCI-REV-0005: Theorems 11.99 and 11.101 proved, the adaptive upper bound after two gaps in
  its written proof were closed; the count of evaluations of Theorem 11.52 is inherited,
  and the nested algorithm has never been simulated for more than two letters**).  The
  lower bounds hold for every `n` and rest on machine-checked inequalities (the product
  step for several site types is on paper); the upper bounds re-use the proofs of Theorems 11.78(b),
  11.52, 11.54 and 11.64 with the changed steps written out, inherit the status of Theorem
  11.78(b), have an error term of the poor kind (`n^{−1/(2q_max+2)}` from the proof) and give
  exponents at extensive accuracies only.  The numbers are for sites with at most four
  letters and chains with at most two site types.  Two things that hold for two letters
  are **false** beyond: the site function need not be concave (so the best split of an
  accuracy between site types is not exact), and the uniform site law need not be the
  hardest — a field, or a known part that removes letters, can make certification harder
  (Proposition 11.103: at slope `0.5` a three-letter site with one rare letter is harder
  than the two-letter cube, by `0.03 %`; no site law exceeds the ceiling `u²/32` at vanishing
  accuracy); which known part is the hardest for a given envelope is open.  The
  dictionary with channel coding (Theorem 11.99) is an identity between formulas; no
  coding theorem is used, and whether it is known in the literature on Monte Carlo
  complexity has only been looked for in two searches by the workstream and four by the
  reviewer of SCI-REV-0005, all at the level of snippets.  The model assumes the density of states of
  the known part and free uniform sampling inside its level sets: it says nothing about
  producing a flat-histogram ensemble by a Markov chain, where the flat ensemble is known
  not to be optimal.  A function of the type has no spatial structure; for short-range
  interactions nothing is proved.
* **The profile format answers a narrower question than §11.14 asked** (§11.17).  Certificates
  that do not grow with the chain exist for residuals that are functionals of pair-distance
  statistics, at extensive accuracy, and the bound that says so is numerically vacuous —
  **at every size that has been enumerated the certificates do grow** (linearly in the chain
  length on the lattice through 27 beads, geometrically off-lattice through 15 beads; they
  are small in absolute terms only when the per-pair constant is small).  For the lattice
  chain the limit is now understood in part (§11.22, corrected after the review SCI-REV-0002
  of the Scientific Discovery Division; the first version of this item said "the plateau
  is between 50 and 3 627 evaluations … and is reached only at `10³`–`10⁵` beads"): a limit
  shape exists **for bridges**; every limit point of the certificate sizes of all walks at
  `(L, ε₁) = (1, ½)` lies between 116 and 3 627 **[P, computer-assisted]**; that the sizes
  converge at all is proved for bridges off a countable, unidentified set of accuracies —
  `ε₁ = ½` is not known to lie outside it — and is a **conjecture** for unrestricted walks
  **[C]**; "a few hundred" for the limit and "`10³`–`10⁵` beads or more" for the chain length at
  which it is approached are estimates **[N]**, the second with no theorem in either
  direction; the body is known only between a proved inner volume `1.56` (`2.22` if a routing
  sketch holds) and an outer volume `3.125`; the section has been checked by the coordinator
  and reviewed by that division (no statement labelled as proved was found false), and
  only its abstract limit theorems are machine-checked, not the lattice lemmas that feed
  them; off-lattice there is only a heuristic estimate.  A
  remainder that is only bounded in a first-order envelope is paid at first-order prices (one
  bounded in the supremum norm costs an accuracy floor), chirality and sequence-specific
  terms are outside, the class is far smaller than an RMSD-Lipschitz class, and checking a
  certificate over voxels of torsions meets the lever arm again.  Whether a physical residual
  has a useful Lipschitz constant in this format is not addressed.
* **No claim of practical performance.**  All experiments are synthetic and small; they check
  tightness and scaling of bounds, not solver speed.
* **Unformalized statements** are marked [P] or [K]: the hardness half of the link-graph
  dichotomy, the Taylor step and the complexity count for second-order voxels,
  dependent-reference sandwiches and Rio's sharp function, the Procrustes–Gram corollary, the
  converse (Donsker–Varadhan) half of Theorem 11.14, the upper bounds of Theorems 11.9 and
  11.15, the complexity-theoretic reading of Theorem 11.10, the elimination rule beyond chains,
  attainment in Theorem 11.18 for non-zero ball data, the learn-then-cover remark, the
  single-letter and upper-bound parts of Theorems 11.24–11.25 (Harper's theorem is cited; the
  step that uses it is checked exhaustively for `n ≤ 4`), the hub-family bound for randomised
  algorithms, the Chebyshev bound for hint-free Monte Carlo, and, in Theorems 11.27–11.28, the
  assembly of the product lower bound from its two machine-checked ingredients, the
  identification of the best constant `γ(Q)` with a maximum over vertices, the algorithmic
  reading of the hitting bound and of the one-reference sandwich, the minimax identity, and
  the closed form for two-state sites; in §11.16, Lemma 11.43(b,c) (the reduction to Harper's
  theorem), Theorem 11.44, the closed forms and all exponents of Theorem 11.45, its parts (d)
  and (e), and Proposition 11.46; in §11.17, every exactness statement (linear-programming and
  Kantorovich–Rubinstein duality), the attainment and the transport form of the profile
  envelope for general distances and several types, and Proposition 11.49 except (c).
* **Certified numerics outside Lean.**  Eigenvalue enclosures needed to *evaluate* the spectral
  bound of §4.1 on data are standard verified numerics but are not part of the development.

---

## 9. Index of machine-checked statements

| file | main declarations |
|---|---|
| `proofs/Core/Basic.lean` | `partitionFn`, `freeEnergy`, `partitionFn_anti`, `freeEnergy_mono` |
| `proofs/Core/Rounding.lean` | `roundDown_le`, `le_roundUp`, `roundUp_sub_roundDown_le`, `QInterval.contains_add/mul/sq/inv/outward`, `exp_enclosure`, `contains_exp`, `contains_boltzmann`, `circle_rational_atlas`, `contains_circParam` |
| `proofs/Frontiers/EnvelopeDuality.lean` | `robust_minimizer_iff`, `robust_certified_iff`, `lowerEnv_admissible`, `upperEnv_admissible`, `robust_min_bracket`, `robust_partition_bracket`, `robust_min_interval_exact`, `robust_partition_interval_exact`, `robust_minimizer_with_anchors_iff`, `anchor_necessary`, `anchor_card_lower_bound`, `admissible_of_single_site`, `differential_dee_sound`, `energy_window_exact` |
| `proofs/Frontiers/Dominance.lean` | `partition_transport`, `partition_prune_bracket`, `partition_transport_fibers`, `partition_prune_bracket_fibers`, `freeEnergy_prune_bracket`, `min_transport`, `thermal_dee`, `boltzmannAvg_dominance_error`, `isLeast_sum_of_block_separable`, `exact_margin_of_block_separable`, `PairModel.energy_update`, `goldstein_isLeast`, `goldstein_gauge_invariant`, `exactMargin_reparam`, `desmet_reparam_le`, `desmet_optimalGauge` |
| `proofs/Frontiers/FreeEnergySandwich.lean` | `gibbs_bogoliubov`, `hoeffding_upper`, `free_energy_sandwich`, `partition_ratio_sandwich`, `bounded_differences_sandwich`, `additive_extremal`, `exists_two_level_worst_residual`, `balanced_additive_gap`, `log_cosh_bounds`, `mcdiarmid_no_better_constant` |
| `proofs/Frontiers/EnsembleDivergence.lean` | `klFin`, `tilt`, `kl_reference_target_eq_gap`, `kl_reference_target_le_hoeffding`, `kl_reference_target_le_bounded_differences`, `bounded_differences_sandwich_any_reference`, `kl_reference_target_le_any_reference`, `correlated_reference_counterexample` |
| `proofs/Frontiers/HolderDecomposition.lean` | `partitionFn_holder`, `freeEnergy_holder` |
| `proofs/Frontiers/PartitionCertificate.lean` | `zverify`, `zverify_sound`, `zverifyTop`, `zverifyTop_sound`, `zprune_sound`, `Z_encloses_partitionFn`, `triangleZ_exact`, `negativeW_rejected` |
| `proofs/Frontiers/IntervalInstance.lean` | `WInstance.lowerOfIntervals`, `WInstance.upperOfIntervals`, `Z_encloses_partitionFn_of_intervals`, `certified_partition_of_intervals`, `triangle_real_partition_enclosure` |
| `proofs/Frontiers/VoxelEnclosure.lean` | `voxel_boltzmann_bounds`, `voxel_riemann_enclosure`, `Z_encloses_voxel_integral`, `certified_voxel_partition` |
| `proofs/Frontiers/VoxelBridge.lean` | `pairwise_voxel_weight_bounds`, `certified_prodVoxel_partition`, `certified_torsion_partition`, `certified_torsion_partition_top`, `certified_torsion_partition_full`, `two_arctan_sub_bounds`, `chartArc_onebody_brackets`, witnesses `exact_witness`, `pair_witness`, `chart_witness` |
| `proofs/Frontiers/SeparableVoxel.lean` | `setIntegral_pi_prod`, `separable_voxel_bounds`, `separable_voxel_ratio` |
| `proofs/Frontiers/HoffmanWielandt.lean` | `trace_mul_le_sum_sorted_eigenvalues`, `hoffman_wielandt` |
| `proofs/Frontiers/Realizability.lean` | `K_identity`, `K_lower_bound`, `rank_psd_trace_obstruction`, `sstress_lower_bound`, `simplex_sstress_lower_bound`, `simplex_not_realizable` |
| `proofs/Frontiers/Holonomy.lean` | `norm_mul_div_mul_le`, `norm_holProd_le_sum`, `norm_holProd_sq_le`, `norm_holTrans_le`, `exists_assignment_attaining_holonomy` |
| `proofs/Frontiers/TorsionRMSD.lean` | `RigidWithin`, `rigidWithin_chain`, `coaxial_cost_eq`, `exists_coaxial_angle`, `coaxial_cost_le_min`, `reduced_le_coaxial_cost`, `IsTorsionMove.rigidWithin`, `rigidWithin_torsion_chain` |
| `proofs/Frontiers/InvariantEnvelope.lean` | `RigidInvariantIn`, `invariant_lipschitz_of_rigidWithinIn`, `residual_torsion_move_in`, `residual_torsion_chain_in`, `residual_torsion_move_uniform`, `residualLowerClass_of_invariant_lipschitz`, `verifyR_sound_invariant` (and the `E(3)` versions `residual_torsion_move`, `residual_torsion_chain`) |
| `proofs/Frontiers/ProofComplexity.lean` | `leaf_two_config`, `triangle_no_leaf_certificate`, `triangles_energy_opt`, `sumFree_exponential`, `sumFree_gap_exponential`, `sumFree_complexity`, `sumFree_tight`, `sum_linear`, `sum_rule_separation`, `sum_rule_separation_size`, `sum_rule_separation_dataSize` |
| `proofs/CertificateAlgebra.lean` | `verify`, `verify_sound`, `verifyR`, `verifyR_sound`, `verifyR_sound_lower`, `RProblem.Consistent`, `RProblem.consistent_iff_nonempty`, `verifyRTop`, `verifyRTop_sound`, `verifyRLowerTop`, `verifyRLowerTop_sound`, `IProblem.Consistent`, `IProblem.consistent_iff_nonempty`, `verifyITop`, `verifyITop_sound`, `verifyITop_ofExact`, `verifyITop_ofLower`, `certified_gap`, `certified_gap_interval`, `verify_sound_real`, `verifyR_sound_real`, kernel-evaluated examples |
| `proofs/Frontiers/CertificationGeometry.lean` | `slack`, `slack_isEnvelope`, `slack_ge_of_lipschitz`, `lowerEnv_eq_sub_slack`, `upperEnv_eq_add_slack`, `certLB_eq`, `IsCertificate`, `isCertificate_iff_cover`, `cover_of_certificate`, `certificate_of_cover`, `card_ge_of_weights`, `mem_of_forced`, `card_ge_of_fooling`, `card_ge_sum_inv`, `partition_bound`, `anchor_necessary'` |
| `proofs/Frontiers/CertificateNotions.lean` | `IsValueCertificate`, `IsConfigCertificate`, `isConfigCertificate_iff`, `isValueCertificate_of_isCertificate`, `cover_of_isValueCertificate`, `isConfigCertificate_of_isCertificate`, `isCertificate_insert_of_isConfigCertificate` |
| `proofs/Frontiers/ConditionalEnvelope.lean` | `condEnv`, `condEnv_isEnvelope`, `admissible_condEnv_iff`, `condEnv_attained`, `condEnv_isGreatest`, `condEnv_tower`, `condEnv_singleton`, `robust_minimizer_with_anchors_iff'`, `robust_certified_with_anchors_iff`, `worst_case_regret_isGreatest` |
| `proofs/Frontiers/CertificateComplexity.lean` | `single_evaluation_certificate_iff`, `domCertificate_iff`, `domCertificate_card`, `domCertificate_min_card`, `hamEnv`, `product_robust_optimal_iff`, `product_single_certificate_iff`, `sum_exp_hamEnv`, `partition_bound_hamming`, `product_partition_bound`, `homogeneous_certificate_dichotomy`, `binary_certificate_exponential`, `binary_full_certificate` |
| `proofs/Frontiers/ExponentialWeights.lean` | `card_ge_exp_weights`, `entropy_le_cross`, `card_ge_entropy`, `thermal_exp_weights` |
| `proofs/Frontiers/ProductRates.lean` | `product_exp_weights`, `product_rate_bound`, `gibbsProb_additive`, `thermal_product_exp_weights`, `thermal_binary_exponential`, `thermal_binary_sharp` |
| `proofs/Frontiers/BestFirst.lean` | `IsBestFirstRun`, `bestFirst_sep_a`, `bestFirst_sep_b`, `bestFirst_sep_c`, `not_cocovered`, `bestFirst_card_le_of_quasiSymm`, `bestFirst_card_le`, `bestFirst_certifies`, `bestFirst_card_le_sharp` |
| `proofs/Frontiers/ThermalRobustness.lean` | `gibbsProb`, `gibbsProb_le_contact`, `gibbsProb_ge_sharp`, `gibbsProb_range_eq`, `gibbsProb_range_with_anchors_eq`, `admissible_iff_weights`, `Zhi_eq`, `Zlo_eq`, `Zhi_le_of_bracket`, `mean_slack_le`, `card_ge_laplace`, `transport_le`, `logMGF_eq_tilt`, `logMGF_le_transport_entropy`, `gap_le_of_T1` |
| `proofs/Frontiers/SecondOrderEnvelope.lean` | `MixedDiffBound`, `starPart`, `pairRemainder`, `secondOrder_remainder`, `starPart_eq_of_additive`, `lowerModel`, `upperModel`, `pairwise_sandwich`, `verify_sound_secondOrder`, `secondOrder_envelope_exact`, `secondOrder_certified_minimizer_iff`, `secondOrder_witness` |
| `proofs/Frontiers/HigherOrderEnvelope.lean` | `mixedDiff`, `HigherDiffBound`, `anchoredInterp`, `anchored_decomposition`, `higherOrder_remainder`, `higherOrder_remainder_of_vanish`, `higherRemainder_higherDiffBound`, `higherOrder_remainder_sharp`, `secondOrder_remainder_of_higherOrder`, `higherOrder_witness` |
| `proofs/Frontiers/SampledSandwich.lean` | `sampleWeight`, `empMean`, `sample_mgf`, `sample_mean_two_sided`, `sandwich_of_mean_estimate`, `sampled_free_energy_sandwich`, `sampled_free_energy_sandwich_good`, `sampled_free_energy_sandwich_of_sample_size` |
| `proofs/Frontiers/PartitionProduct.lean` | `ZCert2`, `zverify2`, `zverify2_sound`, `zverify2Top_sound`, `WInstance.Z_cut`, `WInstance.Z_cut_eq`, `WInstance.Z_elim1`, `WInstance.Z_elim2`, `chainCert`, `zverify2Top_chainCert`, `zverify2_elementary_exact_leaves`, `cut_rule_separation`, `elimination_separation`, `chain_separation`, `ferroChain_separation`, kernel-evaluated instances (`twoTriangles_cut_exact`, `chain_elim_exact`, `tree_elim_exact`, `ring_elim_exact`) |
| `proofs/Frontiers/RefereeLemmas.lean` | `config_exchange`, `value_exchange`, `card_exchange_le`, `exact_free_energy_certificate_eq_univ`, `gaugeW`, `gauge_trivial_separation` (lemmas of the second referee) |
| `proofs/Frontiers/QueryLowerBound.lean` | `QueryAlgorithm`, `exists_query_ne`, `prob_query_ne_ge`, `card_queries_ge_packing`, `expected_queries_ge_packing`, `dip`, `dip_eq_sub`, `queries_cover_of_sensitive`, `expected_queries_ge_of_radius`, `expected_queries_ge_exp_weights`, `queries_strict_cover`, `queries_isValueCertificate`, `certificateAlgorithm_correct`, `instance_query_complexity`, `expected_queries_ge`, `expected_queries_ge_exp_weights_min`, `binary_randomized_exponential`, `min_spotCheck_correct`, `softGap`, `sum_exp_dip`, `log_sum_exp_dip_ge`, `thermal_queries_strict_cover`, `thermal_queries_bracket`, `thermal_expected_queries_ge`, `cube_thermal_randomized_bound`, `cube_thermal_randomized_exponential`, `spotCheck`, `spotCheck_correct` |
| `proofs/Frontiers/SoftGapBounds.lean` | `softGap_le_add_slack`, `detection_weight_ge`, `gibbs_weight_ne_ge`, `dipWeight`, `thermalSampler`, `thermal_spotCheck_correct`, `exists_thermal_spotCheck_sample_size`, `sum_dipWeight_eq`, `cube_deterministic_lower_bound`, `cube_dipWeight_sum`, `softGap_hamEnv_additive`, `thermal_product_randomized` |
| `proofs/Frontiers/QueryRefinements.lean` | `exists_query_ne_pair`, `prob_query_ne_pair`, `hedgedSpotCheck`, `hedgedSpotCheck_correct`, `hedged_window_up`, `min_hedgedSpotCheck_correct`, `cube_one_point_dip`, `cube_small_accuracy_randomized`, `cube_exact_randomized`, `thermal_exact_dip_randomized`, `cube_exact_dip_randomized`, `Referee3.pathoAlg_not_a_tree`, `Referee3.packing_factor_attained` (lemmas of the third referee, and the exact-dip bounds) |
| `proofs/Frontiers/GeneralisedDips.lean` | `genDip`, `genDip_admissible`, `genDip_ne_imp_lt`, `dip_eq_genDip`, `slack_lipschitz`, `softGapOf`, `softGap_eq_softGapOf`, `sum_exp_genDip`, `log_sum_exp_genDip_ge`, `genDip_sensitive`, `genDip_expected_queries_ge`, `genDip_expected_queries_ge_exp_weights`, `genDip_recovers_dips`, `TwoMeasureBound`, `twoMeasureBound_prod`, `twoMeasureBound_pow`, `mass_ge_of_twoMeasureBound`, `product_mass_ge`, `sumSig_lipschitz`, `genDip_product_effect`, `detect_weight_le`, `TwoMeasureLower`, `twoMeasureLower_prod`, `twoMeasureLower_pow`, `product_sandwich` (generalised dips; the two-measure sandwich and its mirror image; after workstream A) |
| `proofs/Frontiers/NormalForm.lean` | `reduce`, `reduce_isEnvelope`, `admissible_reduce_iff`, `slack_reduce`, `lowerEnv_reduce`, `upperEnv_reduce`, `phEnv`, `inf_add_phEnv_eq`, `reduce_phEnv_nonneg`, `certLB_normalForm`, `valueUB_normalForm`, `certUB_normalForm`, `isValueCertificate_iff_normalForm`, `isValueCertificate_normalForm_iff`, `client_eq_centre`, `gap_slack_lipschitz`, `not_cocovered_centre` (normal form; after workstream C) |
| `proofs/Frontiers/SecondOrderDip.lean` | `SecondOrderDip.dip`, `SecondOrderDip.dip_mixedDiffBound`, `SecondOrderDip.dip_center`, `SecondOrderDip.dip_eq_zero`, `SecondOrderDip.dip_witness`, `SecondOrderDip.star_upper`, `SecondOrderDip.stars_do_not_combine` (dense second-order classes; from workstream E's scratch files) |
| `proofs/Frontiers/SoftGapIndependence.lean` | `gibbs_mul_exp_softGap`, `sum_gibbs_exp_softGap_indep`, `sum_dipWeight_indep`, `spotCheck_const_le_cover` (the spot-check constant does not depend on the residual; from workstream G's scratch files) |
| `proofs/Frontiers/NonAdaptive.lean` | `nonadaptive_expected_queries_ge`, `cone_admissible`, `flatCone_admissible`, `cube_nonadaptive_bound`, `weight_le_of_outside`, `sum_le_truncated_add_tail` (non-adaptive lower bound; tail lemma; §11.16) |
| `proofs/Frontiers/LinearClass.lean` | `linRes`, `featEnv`, `featEnv_isEnvelope`, `linRes_sub_le`, `linRes_dev_admissible`, `linRes_sub_attained`, `linRes_span_upper`, `linRes_span_lower`, `linRes_span_exact`, `sumClass_span_upper`, `sumClass_sub_le`, `pairRes`, `cumCount`, `pairRes_eq_cum`, `profEnv`, `profEnv_isEnvelope`, `pairRes_sub_le`, `pairRes_admissible`, `pairRes_span_upper`, `pairRes_span_lower`, `pairRes_le_of_dominates`, `pairRes_sharp` (classes linear in features; pair-additive residuals; §11.17) |
| `proofs/Frontiers/LinearKernel.lean` | `PairInstance.addSmul`, `PairInstance.addSmul_energy`, `LProblem`, `LinResidualClass`, `LCert`, `dataTerm`, `verifyL`, `dataTerm_le_zero`, `verifyL_sound`, `verifyLTop`, `verifyLTop_sound`, `contactTriangle_verified`, `contactTriangle_no_anchor_rejects`, `contactTriangle_bound`, `contactTriangle_class_nonempty` (kernel for residuals linear in pairwise features; §11.17) |
| `proofs/Frontiers/HintRecursion.lean` | `StepLE`, `HintPair`, `StepLE.of_limit`, `StepLE.of_macro`, `StepLE.at_hint_fraction`, `superSolution_le_hint`, `step_from_hint_le`, `iterates_lt_hint_add`, `klBin_shift`, `gaussPair`, `gauss_hint_superSolution` (the level recursion of adaptive algorithms without a hint converges to the hinted exponent); `LayerCake.level_mul_exceed_le_mean`, `LayerCake.mean_le_layer_cake`, `LayerCake.mean_le_upper`, `LayerCake.upper_le_width`, `LayerCake.fibre_sum_le`, `LayerCake.close_points_bound`, `LayerCake.negligibility_threshold_le` (deterministic core of the two-level bracket; §11.18) |
| `proofs/Frontiers/CubeHintPair.lean` | `cubeP`, `cubeLam`, `cubeEstar`, `cubeA`, `cubeH`, `cubeHint`, `cubeNa`, `cubeNa_isLeast`, `cubeNa_isLeast_allRadii`, `cubeNa_add_cubeHint`, `cubeHint_lt_cubeNa`, `cubeEstar_eq_log_cosh`, `cubePair`, `cube_superSolution_le_hint`, `cube_iterates_lt_hint_add`, `cubeHintClip`, `cubePairClip`, `cube_step_from_hint_le`, `cube_hint_superSolution`, `cube_hintRecursion_witness` (the exponent functions of the cube satisfy `HintPair`; the hinted exponent is a fixed point of the recursion; workstream L; §11.18) |
| `proofs/Frontiers/BoundedAccuracy.lean` | `exactRec`, `stepLE_exact`, `Rstep_anti`, `exactRec_props`, `exactRec_reaches_hint`, `exactRec_reaches_hint_of_pair`, `exactRec_ge_hint`, `exactRec_tendsto_hint` (the level recursion of §11.18 defined in Lean; it never undercuts and converges to the hinted exponent), `bounded_iterates_lt`, `two_rung_bound`, `levels_reach_hint_at_zero`, `cube_levels_reach_hint_at_zero`, `cube_levels_reach_hint_at_zero_consistent` (the recursion at accuracy zero), `certified_lower_sum_le_mean`, `populated_part_le`, `close_points_bound'`, `width_le` (deterministic algebra of Algorithm 2L⁺; workstream K and the coordinator; §11.19) |
| `proofs/Frontiers/FieldShift.lean` | `klBin_tilt`, `cone_rate_eq`, `sphere_rate_eq`, `shift_identity` (the shift identity with a known field: rate of the cone law = mutual information + `KL(P_X‖π)` + hinted accuracy at the zero residual; workstream F; §11.20) |
| `proofs/Frontiers/TypeQuantiles.lean` | `upperSet`, `upperDensity`, `shadow_upperSet_subset`, `upShadow_upperSet_subset`, `upperDensity_succ_le`, `upperDensity_pred_le`, `Admissible`, `admissible_succ`, `admissible_pred`, `truncate`, `truncate_lipschitz_insert`, `truncate_lipschitz_erase`, `truncate_ne_iff`, `witness_admissible` (type-wise upper quantiles of a weight whose logarithm is Hamming-Lipschitz differ by at most the factor `e^u` between adjacent type classes — by the local LYM inequality — and the weight truncated at such levels stays in the class; Theorem 11.61(a) = Theorem 11.76(a), for every reference measure that is uniform on type classes; §§11.20, 11.23) |
| `proofs/Frontiers/SymmetricSampling.lean` | `exists_perm_smul_eq`, `card_perm_smul_mem_mul`, `symmetric_nonadaptive_queries_ge`, `truncated_weight_queries_ge`, `symmetric_nonadaptive_witness`, `perm_fraction_le`, `symmetric_queries_ge`, `symmetric_queries_witness` (for a class and a target that are invariant under permutations of the coordinates, two class members that differ on density at most `q` in every type class force `(1 − 2δ)/q` evaluations of every non-adaptive algorithm; with `TypeQuantiles.lean`: a weight against its type-wise truncation; Theorem 11.61(b)(i) for every reference measure that is uniform on type classes; and at an instance that is a function of the type, a class member that differs from it on density at most `q` per type class forces `(1 − 2δ)/q` evaluations of **every** algorithm, adaptive or not — Theorem 11.76(b); §§11.20, 11.23) |
| `proofs/Frontiers/TwoRounds.lean` | `TwoRound`, `TwoRound.output_eq_of_virtual`, `card_distinguished_le`, `prob_output_ne_ge`, `two_round_bound`, `two_round_witness` (a two-round algorithm — a first batch, a second batch that depends on the answers to the first, an output that depends on the answers to both — cannot tell apart two residuals that agree with a virtual residual on the first batch and with each other on the second batch asked under the virtual answers; with two hidden parameters, twins that coincide with a function of the first parameter on a set `W₁` and with each other on a set `W₂`, and points outside `W₁`, `W₂` for at most fractions `p₁`, `p₂` of the parameters: at most a fraction `M₁p₁ + M₂p₂` of the parameters is distinguished, so an `(ε/2, δ)`-correct randomised two-round algorithm — as machine-checked: a **finite mixture** of deterministic two-round algorithms whose second batch has at most `M₂` points for every function (Scientific Discovery Division, SCI-REV-0003, m8; the lemma needs the bound on the instances only, m3) — has `1 − 2δ ≤ M₁p₁ + M₂p₂`; a concrete instance: summing a function on `N` points needs `M₁ + M₂ ≥ (1 − 2δ)N`; Lemma 11.85 for two rounds; §11.24) |
| `proofs/Frontiers/TwoRoundsExpected.lean` | `card_distinguished_le_sum`, `two_round_expected_bound`, `two_round_expected_cost`, `two_round_bound_of_class` (the two-round indistinguishability bound without any assumption on batch sizes: `1 − 2δ ≤ E|B₁|·p₁ + E|B₂(v_{s₁})|·p₂`, the second batch taken on the virtual residuals — hence a lower bound for the expected number of evaluations at one instance, and a worst-case form in which the second batch is bounded only on a class that contains the virtual residuals; written by the Scientific Discovery Division with its review SCI-REV-0003, adopted unchanged and compiled here; Theorem R4.1 of §11.24) |
| `proofs/Frontiers/GroupSampling.lean` | `gdens`, `gdens_mono`, `gdens_smul`, `gdens_mul_card_orbit`, `lowDens_shift`, `regLevel`, `regLevel_admissible`, `regLevel_lowDens_le`, `regLevel_smul`, `truncate_admissible`, `truncate_gdens_le`, `group_nonadaptive_queries_ge`, `group_queries_ge`, `group_witness` (a finite group acting on the configurations with an invariant, possibly asymmetric envelope: the fraction of group elements sending a point into a set is its density in the orbit; for an admissible residual the low sets of two orbits satisfy the normalised matching inequality with the shift `d(a, b)`; levels of orbit density at most `q` regularise to invariant admissible levels; the truncated residual is admissible and differs on orbit density at most `q`; two members of an invariant class that differ on orbit density at most `q` force `(1 − 2δ)/q` non-adaptive evaluations, and `(1 − 2δ)/q` evaluations of every algorithm at an invariant instance; the remark after Theorem 11.76; §11.23) |
| `proofs/Frontiers/SliceRefinement.lean` | `sum_mem_bracket`, `bracket_width`, `argmax_deficit_le`, `deficit_ge`, `mean_le_of_biregular`, `lower_end_any` (reduction of algorithms to type classes for an exchangeable reference measure, Theorem 11.92: if every class carries a bracket and the class with the largest weighted upper end is always the one refined, the output bracket contains the sum and is at most `card` times as wide as the bracket of that class; that class is within its own bracket width of the largest term, so a class is refined only if its deficit is at most its bracket; Lipschitz class means bound the deficits from below by the gap between the weights and their Lipschitz minorant; and the double counting in a biregular bipartite graph that makes the class means Lipschitz — not formalised: that adjacent type classes of the cube form such a graph, the probabilistic validity of the brackets, the count of evaluations; §11.25) |
| `proofs/Frontiers/RenyiCentre.lean` | `scale_le_inv_sum`, `exists_ratio_le`, `eq_of_forall_ratio_ge`, `softmin_admissible` (the two elementary steps of Theorem 11.99: for a probability vector `P` and a positive vector `m` some ratio `P(a)/m(a)` is at most `1/Σm`, with equality in every coordinate only for `P = m/Σm` — so against a mixture of vertices no additive instance beats the one whose Gibbs law is the normalised power mean, the Rényi centre; and the class `{γ : γ(a) − γ(b) ≤ d(a,b)}` is closed under soft minima, for envelopes that need not be symmetric — so that instance is in the class; not formalised: the minimax theorem for the matrix game and the identification with the Rényi capacity; §11.26) |
| `proofs/Frontiers/MacroRatio.lean` | `macro_le_of_plan`, `macro_single_le`, `macro_le_card_mul`, `cone_admissible`, `macro_cone_ge`, `closed_pair_within_A`, `closed_pair_within_B`, `closed_pair_cross`, `two_point_witness` (the certificate half of Theorem 11.105: a transport plan with gains from `B` to `A` bounds `Z_g(A) ≤ λ·Z_g(B)` for every residual that is admissible from `B` to `A`; one state against a macrostate; both halves of the max–min sandwich; a pair closed under the two extensions is admissible in all four directions, so only the constraints from `B` to `A` matter) | §11.28 |
| `proofs/Frontiers/Scattering.lean` | `le_add_cube`, `sub_cube_le` (`|sin t − t cos t| ≤ t³/3` for `t ≥ 0`), `hasDerivAt_sinc`, `sinc_add_sq_monotoneOn`, `sinc_sub_sq_antitoneOn`, `abs_sinc_sub_le` (`|sinc b − sinc a| ≤ (b² − a²)/6`), `sinc_sqrt_lipschitz` (the radial function of the Debye formula is `q²/6`-Lipschitz in the squared distance), `debye_sum_sub_le`, `debye_sub_le` (two conformations, any matching of their pairs: the scattering intensities differ by at most `q²/3` times the matched `ℓ¹` distance of the squared distances), `debye_eq_of_matching`, `one_sub_sinc_le` — Theorem 11.48(d); the statement is the science division's (Proposition A2.1 of SCI-REV-0006) |
| `proofs/Frontiers/BoxClass.lean` | `Box`, `Zw`, `dip`, `bump`, `dip_nonneg`, `bump_nonneg`, `Zw_pos`, `Zw_sub_le_dip`, `Zw_sub_le_bump`, `sum_dip_eq`, `sum_bump_eq`, `sampler`, `sampler_nonneg`, `sampler_sum`, `detect_ge`, `detectProb`, `box_spotCheck_correct`, `dipAlt`, `dipAlt_mem`, `dipAlt_ne`, `Zw_dipAlt`, `logZ_dipAlt_gt`, `box_expected_queries_ge`, `jensen_bracket`, `centre_weights` (box classes `lo ≤ r ≤ hi` around a known function with weights `w`, Theorem 11.110: a member that differs from `r` on `D` changes the partition sum by at most the dip (bump) weight of `D`; every member whose `ln Z` differs by more than `η` is detected by the sampler `½ dip/U + ½ bump/V` with probability at least `min{1, ½ min((e^η − 1)Z/U, (1 − e^{−η})Z/V)}`; the spot check with that sampler is correct on every class contained in the box; `k` disjoint sets of dip weight above `(e^ε − 1)Z` force `(1 − 2δ)k` evaluations of every randomised algorithm; the Jensen lower end; the weights at the centre of a constant box) |
| `proofs/Frontiers/MonotoneSandwich.lean` (namespace `ScienceL2`; **written by the Scientific Discovery Division, adopted unchanged**) | `holley_cross_nonneg`, `holley_cross`, `updown_cross`, `sandwich_mean`, `macrostate_ratio`, `mean_range_eq_Icc`, `ratio_range_eq_Icc`, `mixRes_admissible`, `exists_admissible_ratio`, `envDist`, `field`, `field_admissible`, `neg_field_admissible`, `cube_sandwich_mean`, `cube_macrostate_ratio`, `cube_macrostate_ratio_compl`, `cube_mean_isLeast`, `cube_mean_isGreatest`, `cube_mean_range_eq_Icc`, `cube_ratio_range_eq_Icc`, `field_submodular`, `pairwise_submodular`, `chain_sandwich_mean`, `stepField_sandwich_mean`, `stepField_macrostate_ratio`, `cube_sandwich_strict_witness`, `cube_sandwich_fails_negative_beta` (Theorem 11.106a: for a submodular known part on a finite distributive lattice and an envelope that two functions saturate, the Gibbs measures of all admissible residuals lie between those of the two fields in the stochastic order — Holley's inequality from the four-functions theorem, for unnormalised weights; for a lower set against an upper set the ratio of macrostate weights fills exactly the interval between its values at the two fields; the cube with site constants, ordered alphabets with step fields; additive and ferromagnetic pairwise known parts are submodular; a witness with strict inequalities and a counterexample at negative `β`) |
| `proofs/Frontiers/GamePair.lean` | `HintShape`, `shiftInv`, `partner`, `HintShape.pair`, `HintShape.exists_pair`, `HintShape.superSolution`, `HintShape.Rstep_hint`, `HintShape.exactRec_reaches`, `HintShape.exactRec_tendsto`, `exactRec_congr`, `GameFunction`, `hinted`, `critical`, `GameFunction.hintShape_critical`, `GameFunction.pair`, `GameFunction.exactRec_reaches`, `GameFunction.exactRec_tendsto`, `GameFunction.not_forall_shift_eq`, `GameFunction.critical_eq_neg_L`, `toyGame_gameFunction`, `hinted_toyGame`, `partner_toyGame`, `gauss_exactRec_tendsto` (every game function yields a `HintPair`, and its exact level recursion converges to the hinted exponent; workstream M; §11.21) |
| `proofs/Frontiers/CoverStability.lean` | `Covers`, `HasCover`, `hasCover_mono`, `hasCover_of_close`, `hasCover_sandwich`, `upper`, `hasCover_upper_iff`, `twoPoints`, `hasCover_limit_point`, `not_hasCover_shifted`, `hasCover_shifted_of_close`, `approx_multiple`, `approx_extend`, `approx_nested`, `approx_nested_example` (covering numbers with position-dependent radii and internal centres are stable under perturbations of the client set, with the slack `(2L + e)η`; only the lower boundary matters; no convergence at a jump; the approximate-nestedness estimate behind Fekete's lemma for sets; §11.22) |
| `proofs/Frontiers/SetLimit.lean` | `lowerLimit`, `ApproxNested`, `isClosed_lowerLimit`, `mem_lowerLimit_of_tendsto`, `hausdorff_limit`, `scaled`, `SuperAdditive`, `SuperAdditive.approxNested`, `SuperAdditive.combination`, `SuperAdditive.hausdorff_limit`, `SuperAdditive.dist_limit_le`, `SuperAdditive.convex_limit`, `SuperAdditive.cover_sandwich`, `superAdditive_example`, `one_mem_limit_example` (Fekete's lemma for sets: the normalised sets of a family that is super-additive up to a bounded error converge in the Hausdorff sense to a compact convex set, with the one-sided rate `β/M`; the covering numbers of the finite sets are sandwiched by those of the limit at shifted accuracies; §11.22) |
| `proofs/AuditCommand.lean`, `proofs/AxiomAudit.lean` | `#audit_axioms proofs` (walk over every constant defined in a project module), headline `#print axioms`, named non-vacuity witnesses |

---

## 10. Second research phase: what changed after independent review

Checkpoint 477391f was sent to an independent mathematical referee (`reviews/R1_referee_report.md`)
and three further literature checks were run (`prior_art/L4`–`L6`).  The outcome, in one
paragraph: **no machine-checked statement was false, but the mathematics of the first phase is
elementary or classical in substance, four prose claims went beyond the theorems, and the
partition-function kernel was too weak for chains.**  The corrections are in place in §§0–8
(marked "corrected" or "referee report") and are recorded as `DEAD_ENDS.md` D21–D27.  The referee
named the one route to a mathematical contribution in the envelope cluster — *matching upper and
lower bounds on certificate size* — and that is what the second phase pursued (§11).

The second phase was then reviewed by a second independent referee (`reviews/R2_referee_report.md`).
Again no machine-checked statement was false; **one paper theorem was false as stated**
(Theorem 11.15, for exponentially small accuracies), four claims were overstated (the doubling
remark after Theorem 11.11, the planning formula of the blueprint, "second-order envelopes: the
way out", the scope of the partition-kernel separation), and Theorem 11.5 was true but not
sharp.  All of this is corrected below (marked "second referee") and recorded as
`DEAD_ENDS.md` D29–D33; the referee's four machine-checked lemmas are part of the development
(`RefereeLemmas.lean`).  The referee's two requests that went beyond corrections — an
algorithmic statement, and a probabilistic notion of certificate — are the subject of §11.10
(row G11).

| # | Result of the second phase | Lean | Classification after `prior_art/L4`–`L6` |
|---|---|---|---|
| G1 | **Certificates are coverings in the slack quasi-metric** `s(a,y) = d(a,y) − g(a) + g(y)`: `LB(A) = min_y [E(y) − s(A,y)]`; `A` certifies ⇔ every `y` lies within slack radius `E(y) − UB(A) + ε`; point, value and configuration certificates have the same minimal size, `N_cov` or `N_cov + 1` | `isCertificate_iff_cover`, `cover_of_certificate`, `certificate_of_cover`, `cover_of_isValueCertificate`, `value_exchange`, `config_exchange` **[V]** | **reformulation** of a known notion (minimal certificates / proof sets / `τ`: Hansen–Jaumard–Lu 1991, Baran–Demaine 2004, Bachoc et al. 2021); the slack form with a known part and an asymmetric envelope was not found |
| G2 | **Conditional envelope** `D_A(x,y) = min(d(x,y), U(x) − L(y))`: exact supremum of `g(x) − g(y)` over consistent residuals; anchored sharp-minimum theorem; worst-case regret | `condEnv_isGreatest`, `robust_certified_with_anchors_iff`, `worst_case_regret_isGreatest` **[V]** | **known** (minimal simple temporal network); stated for completeness |
| G3 | **Dual lower bounds** on certificate size: LP weights, forced points, fooling sets, volume, and the exponential-weights bound `e^{−tε} Σ_y v(y) ≤ \|A\| · max_a Σ_y v(y) e^{−t(s(a,y) − gap(y))}` | `card_ge_of_weights`, `card_ge_of_fooling`, `card_ge_sum_inv`, `card_ge_exp_weights`, `partition_bound` **[V]** | tools **known** (covering LP; Csiszár's dual bound on rate–distortion); the use for certificate size: no match found |
| G4 | **Dichotomy and exact exponent on product landscapes**: one evaluation suffices iff every site is sharp; otherwise the minimal certificate grows like `exp(n R*)`, `R* = max_P R(P; s − gap, 0)` | `product_single_certificate_iff`, `product_exp_weights`, `binary_certificate_exponential` **[V]** (lower bound, every `n`); upper bound **[P]** (type covering) | **no match found**; an application of the type covering lemma |
| G5 | **Hardness**: minimal exact certificates contain minimum dominating sets | `domCertificate_card`, `domCertificate_min_card` **[V]** | **known** for metric search with the same 0/1/2-distance gadget (Hetland 2020; found by workstream C); immediate |
| G6 | **Best-first search with resource augmentation**: at most `\|C\| + 1` evaluations for every cover `C` at radii `θ(gap + ε/6)`, `θ = (1−κ)/(4(1+κ))`; the `+1` is attained | `bestFirst_card_le`, `bestFirst_certifies`, `bestFirst_card_le_sharp` **[V]**; that some augmentation is necessary is shown by the hub family (harness `DEAD.6`), not by a theorem; the constants are not claimed tight | **partially known** (dimension one without augmentation; `ℝ^d` with doubling constants); the dimension-free metric form was not found.  With a known part the comparison class can be unboundedly larger than `N_cov` even on the line (D30) |
| G7 | **Finite temperature**: thermal contact interval; free-energy certificates are quantizers of the Gibbs ensemble in exponential slack distortion; entropy bound; Hölder exponential-weights converse; exact exponent `R_β = max_Q R(Q; s, (F[Q] − F))` for accuracies that are not exponentially small | `gibbsProb_range_eq`, `mean_slack_le`, `card_ge_entropy`, `thermal_exp_weights`, `thermal_product_exp_weights`, `thermal_binary_exponential` **[V]**; exponent formula **[P]** | contact interval and fixed-`β` duality **known in spirit**; the exponent formula is a corollary of an example in Merhav (2011, §4, eq. (37)), stated there as "a straightforward exercise" for memoryless finite-alphabet sources and additive distortion (section read in full by the science division, `SCI-REV-0006` W7); the identification of certificate size with it, and the one-shot converses: no match found |
| G8 | **Second-order envelopes**: with bounded mixed differences, `n(k−1)+1` evaluations on a star give an exact pairwise sandwich; the extremal extensions are pairwise models; certified-minimiser criterion; order `m` in general.  The remainder is quadratic in the Hamming distance, so this is a way out only under weak second-order coupling (D32) | `secondOrder_remainder`, `pairwise_sandwich`, `verify_sound_secondOrder`, `secondOrder_envelope_exact`, `secondOrder_certified_minimizer_iff`, `higherOrder_remainder`, `higherOrder_remainder_sharp` **[V]** | anchored (cut-HDMR) decomposition **known**; as a certified uncertainty class with an exact reduction to the pairwise kernel: no match found |
| G10 | **Sampled free-energy sandwich**: `N` independent samples of a product reference pin `ln(Z/Z₀)` to `±\|β\|η + β²Σc_i²/8` outside an event of probability `2e^{−2Nη²/Σc_i²}` — polynomially many random evaluations where deterministic certification needs exponentially many | `sample_mean_two_sided`, `sampled_free_energy_sandwich`, `sampled_free_energy_sandwich_of_sample_size` **[V]** | standard concentration (Chernoff bound for a sub-Gaussian mean); stated as the constructive counterpart of G7 |
| G9 | **Compositional partition kernel**: cut rule and elimination rule (exact on every chain, with one leaf), with exponential separations from the elementary rules for every chain length — for certificates whose lower end is exact, and relative to the given representation of the instance (D33) | `zverify2_sound`, `WInstance.Z_cut`, `cut_rule_separation`, `WInstance.Z_elim1`, `WInstance.Z_elim2`, `zverify2Top_chainCert`, `chain_separation`, `ferroChain_separation` **[V]** | repair of the kernel; variable elimination is classical; the separation is the formal counterpart of E2 at finite temperature |
| G11 | **Query complexity of every algorithm**: sensitive alternatives must be detected (any class, any functional; deterministic and randomised), with a hedged spot-check converse; for the minimum, the instance-wise deterministic complexity *equals* the size of a value certificate, and every randomised algorithm (finite mixture) pays `(1−2δ)` times each fractional covering bound — attained by the hedged spot-check up to `ln(1/δ)`; for `ln Z`, a soft-gap radius for every algorithm and an upper bound for randomised ones in the same quantity, a lower bound on the randomised exponent with an upper bound in the same quantity, a machine-checked exponential gap between deterministic and randomised cost at the zero residual of the cube, and there a sharp worst-case accuracy threshold and the exponent in every accuracy regime | `exists_query_ne`, `prob_query_ne_ge`, `expected_queries_ge_packing`, `spotCheck_correct`, `instance_query_complexity`, `expected_queries_ge_exp_weights_min`, `binary_randomized_exponential`, `thermal_queries_strict_cover`, `thermal_queries_bracket`, `thermal_expected_queries_ge`, `thermal_product_randomized`, `cube_thermal_randomized_bound`, `detection_weight_ge`, `thermal_spotCheck_correct`, `cube_deterministic_lower_bound`, `exists_query_ne_pair`, `hedgedSpotCheck_correct`, `min_hedgedSpotCheck_correct`, `thermal_exact_dip_randomized`, `cube_exact_dip_randomized` **[V]**; single-letter forms and the upper bounds on the cube **[P + K]** | method **known** (radius of information; instance complexity; fractional block sensitivity as a bound on randomised query complexity); that randomisation helps for `ln Z` only above an accuracy scale is **known** for smoothness classes (Holzmüller–Bach 2025, §2.2); the constants themselves are in print in another role: `n·ln cosh(βc/2)` is the maximal bias `B_max = N log cosh(ε/2)` of the one-sample Jarzynski estimator for `N` independent two-state units, and `nΛ₁` its free-energy change (Suárez–Silbey–Oppenheim, Phys. Rev. E 85, 051108 (2012), arXiv:1108.5783, eq. (31) and the bias formula; found by the Scientific Discovery Division, SCI-REV-0004); **not found: the role of that constant as a sharp complexity threshold with an exponential lower bound below it**, the instance-wise randomised bound with gap radii, the soft gap, and the accuracy diagram on the cube |
| G12 | **Beyond the cube at finite temperature**: every slack-Lipschitz function is the centre of an admissible perturbation that must be detected (generalised dips), with a single-letter lower bound on product landscapes that is a game over the vertices of the Lipschitz polytope of a site — single dips are not extremal for three or more states; a two-reference sandwich that tensorises, the sharp accuracy threshold of every additive instance, and the worst-case threshold of the whole class without a hint, for every alphabet (the smallest oscillation of the tilted site pressure; for two-state sites the largest chord gap of the pressure) | `genDip_admissible`, `log_sum_exp_genDip_ge`, `genDip_expected_queries_ge_exp_weights`, `twoMeasureBound_pow`, `twoMeasureLower_pow`, `product_sandwich`, `product_mass_ge`, `detect_weight_le` **[V]**; product assembly, thresholds, the minimax identity and the algorithmic reading **[P]**; the matching upper bound of the exponent **[P]**, checked by an independent referee (R4) | found by independent workstreams (A, B; D confirms) and, for the hint-free threshold of general alphabets, in their synthesis; tools **known** (Chernoff and packing; tensorisation of exponential-moment inequalities; for the upper bound of the exponent: inherently typical subsets, Ahlswede–Yang–Zhang; isoperimetric exponents of two product measures, Ahlswede–Zhang, Yu — read by the referee); the upper bound of the exponent is a new statement with a known proof, and may follow from the fixed-measure theorem used as a black box; its evaluation as a matrix game, the lower bound, the thresholds and the application were not found |
| G13 | **Normal form**: a known part is the gradient part of an asymmetric envelope — value certificates of `(d, f, g)` are exactly the point certificates of `(σ, 0, f^d + g)`, `σ` the reduced cost of `d` under the Pasch–Hausdorff envelope `f^d`; a centre-form bound for best-first search valid for every admissible residual; best-first search is unboundedly worse than the smallest certificate on the line once there is a known part | `isValueCertificate_iff_normalForm`, `inf_add_phEnv_eq`, `certUB_normalForm`, `client_eq_centre`, `not_cocovered_centre` **[V]**; the search bound **[P]**; the line families computed | workstream C, verified by its reviewer; elementary (Johnson reweighting, min-plus adjointness) and a **reformulation of a classical correspondence**: for symmetric `d` the reduced envelope is a *weightable quasi-metric* (equivalently a partial metric) whose weight is minus twice the regularised known part (Matthews; Künzi–Vajner; Deza–Deza–Vidali 2011; `SCI-REV-0006` W5); the equivalence of value certificates with point certificates of the reduced instance was not found; for `f ≡ 0`, symmetric `d` the covering characterisation and the hardness gadget are **known** (Hetland 2020), and the search bound is the known packing argument |
| G14 | **Dense second-order classes**: a second-order dip; the uncertainty after any evaluations is at least `c·C(d+1, 2)` at Hamming distance `d` from the evaluated set; unions of stars give exactly the best single-star bound; covering sandwich for the certificate size; full exponent for constants of order one, a rate–distortion exponent with a square-root budget and a transition at `e/γ = 1/4` for mean-field constants; a three-legged spider beats the star | `SecondOrderDip.dip_mixedDiffBound`, `SecondOrderDip.dip_witness`, `SecondOrderDip.stars_do_not_combine` **[V]**; sandwich, asymptotics, spider **[P]**, verified by a reviewer with linear programmes over the whole class | workstream E (D found the dips independently); the `Θ(n²)` law is **known** for approximate modularity (Chierichetti–Dasgupta–Kumar 2020); the covering sandwich, the non-combination of stars and the spider were not found |
| G15 | **Free energies beyond first-order product classes**: second-order classes have a transition at the Curie–Weiss coupling `βc₂n = 4` (polynomial below by Dobrushin uniqueness, exponential above by droplets); the accuracy threshold on the torus of angles is `Σ_i ln(sinh b_i/b_i)`; Boltzmann averages are uncertifiable on most of their a-priori range; the constant of the soft-gap sampler does not depend on the residual | `SecondOrderDip.dip_mixedDiffBound`, `sum_gibbs_exp_softGap_indep`, `spotCheck_const_le_cover` **[V]**; the three theorems **[P]**, re-derived by a reviewer | workstreams D and G; the two-regime picture and the order in fixed dimension are **known** (Holzmüller–Bach 2025); the transition for second-order classes, the torus threshold and the result on averages were not found (the reviewer's literature search was cut short) |
| G16 | **Chain geometry**: the verified torsion-to-RMSD constants grow like `m^{3/2}` with the distance to the chain end (lever-arm law); with constants growing like any positive power, weighted-Hamming envelopes make certification exponential with almost full exponent; used directly, the RMSD envelope costs a stretched exponential `exp(Θ̃(√N))` at the zero residual; contact residuals force growing constants in every torsion-Hamming envelope | **[P]** from machine-checked bounds (`card_ge_exp_weights`, `expected_queries_ge_exp_weights_min`, `thermal_expected_queries_ge`); two constants numerical | workstream G, checked by a reviewer with own geometry code; the growth law itself is a **known special case** — the constants are square roots of moments of inertia of the lighter arm; weighted-`ℓ¹` displacement bounds with per-joint lever arms are a published certificate in robot motion planning (Schwarzer–Saha–Latombe 2005, Lemma 2) and the growth of joint-space inertia with the number of bodies is documented in robotics (Featherstone 2004) (`SCI-REV-0006` W6; the name "law" should not read as a finding); the quantitative consequences for certification (Theorems 11.37–11.38) were not found, in searches that the science division itself calls thin |
| G17 | **Chains as known parts**: one evaluation certifies iff every contiguous droplet is sharp (`c ≤ τ`, a minimum-ratio cycle; `2h` for the Ising ferromagnet); the exponent of homogeneous chains is `sup_ν R_ν(e(ν))` over stationary processes; the transfer-matrix (Boltzmann) bound vanishes on the window `2h < c ≤ 2(J+h)`; the soft gap of a chain is a pinned free energy | **[P]**, re-derived by a reviewer (no Lean) | workstream B; the exactness criterion at zero field is **known** (Gray's critical distortion); the droplet criterion, the exponent theorem and the vacuous window were not found (no literature search was possible in the review) |

| G18 | **Without a hint on the cube**: the exponent of non-adaptive algorithms is `min{KL(ρ‖½) : KL(ρ‖p_u) ≤ ε₁}` at extensive accuracies and `KL(p_u‖½)` at every fixed accuracy — plain Monte Carlo attains it on the whole class (tail lemmas: above a threshold the mass is at most the excess of a dip on a ball of the size of the super-level set, below it at least that of a cone around such a ball), and no non-adaptive algorithm does better (cones against cones with a flattened bottom); two independent samples give a certified bracket that needs no hint at the zero residual for `ε > 2`; an adaptive algorithm that is correct on the class needs `n + 3` evaluations on a cone (for adaptive algorithms see G20) | `nonadaptive_expected_queries_ge`, `cube_nonadaptive_bound` (conditional on two finite sums), `weight_le_of_outside`, `sum_le_truncated_add_tail`, `weight_ge_of_inside`, `sum_truncated_ge` **[V]**; Harper's theorem **[K]**; the reductions to it, the closed forms, all exponents and the probabilistic statements **[P]** | cycle 10, refereed (`reviews/R5`); the sample size `e^{KL(π‖uniform)}` at one instance is **known** (Chatterjee–Diaconis 2018) and the *method* of the non-adaptive lower bound — hidden cone centres, Bakhvalov averaging, defeated by adaption — is **known** (Mathé–Novak 2007, for log-concave densities with a Lipschitz logarithm); **the two formulas are in print at the cone instance**: they are the "freezing" formulas of the Jarzynski estimator in the discrete random energy model (Suárez–Silbey–Oppenheim 2012, arXiv:1108.5783, eqs. (39)–(46) in the reading of the Scientific Discovery Division, SCI-REV-0004, which checked the agreement of the formulas to `4·10⁻¹⁵`; at bounded accuracy Chatterjee–Diaconis 2018, Theorem 3.4); **not found: the minimax statements** — that the cone is the worst instance of the class for plain Monte Carlo (the class-wide upper bound) and that no non-adaptive algorithm does better |
| G19 | **Correlated uncertainty**: for residuals that are linear in known features with coefficients in a box, the envelope is a pulled-back weighted `ℓ¹` distance, every linear combination of evaluations brackets the value at a new point by the unexplained part of its feature vector (worst case over the data: the `ℓ¹` distance to the span, against the distance to the nearest point for the first-order class of the same envelope), and rank-many evaluations determine everything; pair-additive residuals with unknown Lipschitz radial functions are linear in cumulative pair-count profiles, their envelope is a transport distance between pair-distance distributions, sharpness is stochastic dominance, and at extensive accuracy certificates in this format exist whose size does not depend on the chain length; a kernel certifies minima for all coefficient vectors consistent with evaluated anchors | `linRes_sub_le`, `linRes_sub_attained`, `linRes_span_upper`, `linRes_span_lower`, `linRes_span_exact`, `sumClass_span_upper`, `sumClass_span_lower`, `pairRes_eq_cum`, `pairRes_sub_le`, `pairRes_span_upper`, `pairRes_span_upper_enclosure`, `pairRes_sharp`, `verifyLTop_sound`, `contactTriangle_bound`, `sinc_sqrt_lipschitz`, `debye_sub_le` **[V]**; exactness (duality), the transport form, the entropy bound and everything about chain length **[P]** | cycle 10, refereed (`reviews/R6`) except the kernel; the linear theory is **known** (optimal recovery: Smolyak, Micchelli–Rivlin; set-membership estimation; robust linear programming), the features are those of linear contact potentials (Maiorov–Crippen 1992; Tobi et al. 2000), the distance is a **named object** — the Wasserstein-1 distance between global distance distributions, a standard lower bound of the Gromov–Wasserstein distance (Mémoli 2011; Mémoli–Needham 2022), also a descriptor distance (Osada et al. 2002; bag of bonds), whose zero set is Patterson homometry — and its reading as the support function of the class of Lipschitz pair potentials is Kantorovich–Rubinstein duality for that distance (`SCI-REV-0006` W3); the entropy of monotone functions is classical; the use next to a known part and the consequences for certificates were not found; Debye scattering curves of one conformation are members of the class (science division; Theorem 11.48(d)); **none of it is deep** |
| G20 | **Adaptivity replaces the hint**: on the cube class the worst-case exponent of adaptive randomised algorithms without a hint is the hinted exponent `θ_hint(ε₁) = KL((Λ₁+ε₁)/u‖½)`, strictly below the non-adaptive `θ_na`.  A two-level "layer-cake" algorithm — uniform outer sample, brackets of the fibre averages refined only as far as a one-sided test against a ladder of levels requires, the tail lemma once at the top — turns bracket procedures with exponent function `T` into ones with `R[T]`; by the identity `θ_na(e + θ_hint(e)) = θ_hint(e)` (that is, `KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁`) the hinted exponent is a fixed point of `R`, every nonincreasing `T ≤ R[T]` lies below it, and the iteration from `θ_na` converges to it; on radial instances a direct adaptive algorithm has the hinted exponent | `superSolution_le_hint`, `iterates_lt_hint_add`, `step_from_hint_le`, `klBin_shift`, `cubePair`, `cube_iterates_lt_hint_add`, `cube_hint_superSolution`, `LayerCake.mean_le_upper`, `LayerCake.upper_le_width`, `LayerCake.close_points_bound` **[V]** (analysis of the recursion, abstractly and for the exponent functions of the cube; validity and width of the bracket; the two algebraic inequalities behind the cost); the algorithm's number of evaluations, the induction over levels and all asymptotics **[P]** | cycle 10, refereed (`reviews/R7`: "proved with gaps", the gaps written into the text; no error found in the cost accounting beyond one closure rule); the two-level algorithm and the recursion are due to workstream H, the oracle-relative form, the identity and the convergence proof to the coordinator; relatives of the algorithm are nested sampling, multilevel splitting and nested simulation, adaption with polynomial gains is known in information-based complexity (Heinrich; Kunsch–Novak–Wnuk) — a certified version with a worst-case exponent, and the statement that adaption recovers the value of a hint exactly, were **not found** (abstracts only) |
| G21 | **Every bounded accuracy**: at every fixed accuracy, and down to accuracies `e^{-o(n)}`, the worst-case exponent of adaptive randomised algorithms without a hint on the cube class is `h = KL(Λ₁/u‖½)`, the hinted one, against `a = KL(p_u‖½)` for non-adaptive algorithms.  The two-level algorithm is modified so that a level costs only an arbitrarily small constant of accuracy: layer-cake *sum* as lower end, and the lower isoperimetric bound (Harper, two-sided tail lemma) inside the closure test, which is what certifies a bounded ratio at radii `p_u n_o − O(√n_o)`; the recursion continues to accuracy zero and contracts to `h` | `exactRec_tendsto_hint`, `exactRec_ge_hint`, `bounded_iterates_lt`, `cube_levels_reach_hint_at_zero`, `two_rung_bound`, `certified_lower_sum_le_mean`, `populated_part_le`, `close_points_bound'`, `width_le` **[V]** (the exact recursion; the contraction; the algebra of the bracket and of the count); the algorithm, its events, its cost and the assembly over the levels **[P]** | cycle 10, workstream K; **refereed (`reviews/R8`: "proved", no critical or major finding, ten minor points corrected)**; simulated with the constants of the theorem by the workstream, by the referee (15 000 runs; three nested levels with real inner brackets on small cubes; exact three-level cost at the flat instance) and in the harness (XVI.3); prior art from search summaries only |
| G22 | **With a known part (a field)**: on the `p`-biased cube the exponent of non-adaptive algorithms without a hint is `θ_na = max_m min{I(S;X) : D(P_{X|S}‖π_s|P_S) ≤ ε₁}`, attained by sampling uniformly on every type class and not by the Gibbs measure of the known part; the worst-case exponent of adaptive algorithms without a hint is `R^max = max_γ R_γ`, the hinted exponent of the hardest *additive* instance, which is strictly above the hinted exponent of the zero residual whenever `p ≠ ½`; the reference instance of the nested algorithm is the lower envelope of the additive instances (flat histogram), and the isoperimetric input is an asymptotic statement for that reference proved by the method of types | `shift_identity`, `klBin_tilt`, `exactRec_reaches_hint_of_pair`, `admissible_succ`, `admissible_pred`, `truncate_lipschitz_insert`, `symmetric_nonadaptive_queries_ge` **[V]** (the identity between the three rates; convergence of the exact recursion for any pair with the abstract properties; type-wise quantiles are Lipschitz, so the truncated weight stays in the class; the non-adaptive lower bound `(1 − 2δ)/q` for permutation-invariant problems); the single-letter formulas, the isoperimetric theorem, the abstract properties of the pair and everything about algorithms **[P]** | cycle 10, workstream F; **refereed (`reviews/R9`): the isoperimetric theorem and the non-adaptive exponent proved; the adaptive exponent — lower bound proved, upper bound proved after two gaps in the written proof of the algorithmic part were closed; no critical finding**; the coordinator's proof that a field always helps (Proposition 11.65(b)) refereed "proved"; central formulas re-computed by the coordinator and, independently, by the referee; prior art: the Ahlswede–Zhang summary read in full by the referee, otherwise abstracts and machine summaries (Bollobás–Leader; Yu) — the isoperimetric statement is not a black-box corollary of the fixed-measure theorem |
| G23 | **The structure behind G18–G22**: the shear law `x_na(θ) = e_hint(θ) + θ` (a non-adaptive sample of `e^{nθ}` points loses exactly `θ` of accuracy rate), and an abstract theorem: for every game function `F` on `[0,1]` the transform `R(e) = max_{t≤1}[F(t) − te]` and its sheared partner `R ∘ (id + R)^{-1}` form a pair to which the convergence theorem applies, `R` is a fixed point and lower barrier of the level operator, and the exact level recursion converges to `R`; the uniform cube, the biased cube and the toy pair `t(1−t)` are instances | `GameFunction.hintShape_critical`, `GameFunction.pair`, `HintShape.superSolution`, `GameFunction.exactRec_tendsto`, `gauss_exactRec_tendsto` **[V]**; that the exponent functions of a given problem are of this form **[P]** | cycle 10, workstream M (a formalisation task; statement by the coordinator after workstream F's Theorem F8); elementary convex analysis — the value is that the analytic core of two theorems is one machine-checked statement |
| G24 | **Chains in the thermodynamic limit** (the lattice chain of G19): the normalised sets `{(profile, #gauche)/N}` of bridges converge in the Hausdorff metric to a compact convex body — a limit shape with a convex least-gauche function — by a concatenation lemma with explicit constants and Fekete's lemma for sets, with the one-sided rate `168/(N+3)`; covering numbers with position-dependent radii are stable under Hausdorff convergence of truncated epigraphs, so the certificate sizes of bridges converge to a covering number of the limit shape (off a countable set of accuracies); for all walks: an outer polytope with exact dual certificates (cluster method), the bounds `116 ≤ liminf` (first version: 50, from one triangle of the body; raised by the Scientific Discovery Division with the section's own tools — explicit bridges, the one-sided rate, convexity — and re-verified by us), `limsup ≤ 3 627` at `(L, ε₁) = (1, ½)` in place of `10^{1387}`, and `26 437` for every chain length — bounds for limit points, not for a limit: no accuracy is known to lie outside the exceptional set; the shape converges at rate exactly `N^{-1/3}` at its compact end (Loomis–Whitney; the second-neighbour half follows with a better constant from Bezdek's theorem on contact numbers) and at least at rate `N^{-1/2}` at interior points, so enumeration cannot see the limit; single-flip constants are bounded below linearly | `SuperAdditive.hausdorff_limit`, `SuperAdditive.convex_limit`, `SuperAdditive.dist_limit_le`, `SuperAdditive.cover_sandwich`, `hasCover_sandwich`, `hasCover_upper_iff`, `not_hasCover_shifted` **[V]** (Fekete's lemma for sets and the stability of covering numbers, in abstract form); that lattice bridges satisfy the hypotheses and everything else about the lattice **[P]**, the polytopes and the numbers computer-assisted with exact certificates; equality of the limits for walks and bridges **[C]** | cycle 10, workstream S, in answer to a question of the Computational Research Division (`ENG-REQ-0001`); **checked by the coordinator — every proof re-derived, every computer-assisted statement re-computed with independent code — and reviewed by the Scientific Discovery Division (SCI-REV-0002: no statement labelled as proved found false; the practical headline reworded, the proved bracket tightened, a bookkeeping gap between the Lean hypotheses and their use closed on paper)**; the abstract limit theorem is a **known special case / reformulation**: a set-valued Fekete lemma is in print in exact form (Permuter–Weissman, arXiv:0708.0271, Lemma 23 and Corollary 24), and for an exact semigroup of lattice points the limit is a Newton–Okounkov body (Khovanskii; Kaveh–Khovanskii 2012), with a stronger approximation theorem — the version here allows a bounded error (SCI-REV-0002, SCI-REV-0006 W8; read by that division, not by us); limits of supermultiplicative models and the cluster method for lattice-gas ground states are **known**; the corresponding free-energy statement for self-attracting walks is open in the literature; the limit shape for this model, the stability lemma and the numbers were not found |
| G25 | **A known part with interactions, first case: a function of the type** (mean-field models, one phase or two): for every `n` and every exchangeable reference measure the type-stratified (flat-histogram) sample is optimal among non-adaptive algorithms up to a polynomial factor and the flat-histogram instance is the hardest instance that is a function of the type; the cost of every algorithm at such an instance has a single-letter exponent, a supremum over block profiles, for every rate function (isoperimetry for the type-uniform measure by the method of types); for a convex rate function binary centres suffice, the flat-histogram instance is as hard as the hardest additive one and there is a game function, so the pair identity holds; with two phases cones fail, the extremal perturbations are shells in the barrier type class, cones around self-consistent shells restore the pair identity, and beyond a small accuracy profiles that constrain only part of the coordinates beat every set around one centre; ferromagnets are never harder than the uniform cube and coincide with it up to a coupling beyond the critical one | `admissible_succ`, `admissible_pred`, `truncate_lipschitz_insert`, `symmetric_nonadaptive_queries_ge`, `symmetric_queries_ge` **[V]** (the truncation and both every-`n` lower bounds, for every permutation-invariant problem); `lowDens_shift`, `truncate_gdens_le`, `group_nonadaptive_queries_ge`, `group_queries_ge` **[V]** (the same for an arbitrary finite symmetry group with an invariant envelope); `GameFunction` and Theorem 11.66 **[V]** apply once its hypotheses are verified on paper; the hardest-symmetric-instance inequality, the single-letter theorem, the convex case and the ferromagnetic comparison **[P]**; the two-phase values **[N]** (each a proved lower bound); for ferromagnets an adaptive algorithm without a hint with at most the uniform cube's exponent **[P]**, given Theorem 11.64; binary optimality at vanishing accuracy and the adaptive exponent in general **[C]** | cycle 10, workstream T; proofs re-derived in part and all headline numbers re-computed by the coordinator with independent solvers; **refereed (R10: no critical finding; two major findings — the junction formula false at large slopes, an interval with an unproved end — and fifteen minor ones, all applied)**; tools **known** (method of types, inherently typical subsets, Sion's theorem, Hubbard–Stratonovich); prior art: flat-histogram methods (Berg–Neuhaus; Wang–Landau) and their dynamical non-optimality (Trebst–Huse–Troyer), worst-case optimal importance proposals for other criteria (Cérou–Héas–Rousset; He–Owen) — abstracts only; a minimax statement for certified estimates over a class of perturbations was not found |
| G26 | **Rounds of adaptivity** (uniform cube, no known part): the two-level algorithm can be scheduled so that a ladder with `L` rungs uses `L` rounds (the candidate set of a rung is computed from empirical levels of the previous one and is polynomially many times `e^{x_{l−1}}` points — on the good event, and in every run once the schedule stops when the set is larger: our first version said "deterministically", which was false without that rule, Scientific Discovery Division, SCI-REV-0003, M1), so `k` levels need `L^{k−1}` rounds independently of `n` and the round-limited exponents `τ^{(r)}` decrease to the adaptive exponent `h`; two rounds: `τ^{(2)} ≤ T^{(2)}(0)`, the golden ratio times `a` for small slopes; and `τ^{(2)} ≥ θ₂*(u) > h` for every slope, by an indistinguishability lemma for block-radial functions with hidden centres and a pair of instances in which a flat-histogram structure in one block dilutes the first batch while a dip in the other block opens exactly where a blind batch stops seeing each shell; radial instances need exactly two rounds | `card_distinguished_le`, `two_round_bound` **[V]** (the indistinguishability lemma for two rounds, in abstract form, for finite mixtures); its form for the expected cost at one instance, `two_round_expected_bound`, `two_round_expected_cost` (`TwoRoundsExpected.lean`, the Scientific Discovery Division's file); `certified_lower_sum_le_mean`, `width_le` and the other deterministic parts of Theorem 11.56 **[V]** are inherited by the batched schedule; the batching theorem, the application of the lemma to the twins, the lower bound **[P]**; the values of the recursion and the exact finite-`n` twins **[N]**; three rounds **[C]**/open | cycle 10, workstream U; checked against the proof of Theorem 11.56 and re-computed by the coordinator (two- and three-round upper bounds, `θ₂*`, exact twins up to `n = 3200`); refereed (Scientific Discovery Division, SCI-REV-0003: no critical finding, one major and nine minor points, corrected in §11.24); prior art: adaptivity hierarchies in property testing (Canonne–Gur), rounds in parallel convex optimisation (Nemirovski; Balkanski–Singer; Bubeck et al.), batched bandits and sparse recovery — summaries only; a round hierarchy for normalising constants over a Lipschitz class was not found |
| G27 | **Slices: every known part that is a function of the type against the uniform cube.**  Among pairs of binary variables with a given odds ratio the mutual information is largest when both marginals are uniform (equivalently, among binary channels with a given odds ratio the symmetric one has the largest capacity).  For the uniform measure on one type class: binary centres suffice, the exponent functions have closed forms, and the game function of every centre on every type class is dominated pointwise by the uniform cube's, with equality only for the class `½` and the centre type `½`.  Hence for every exchangeable known part and every symmetric instance the hinted exponent, the lower bound for all algorithms from symmetric instances and the non-adaptive exponent are at most the uniform cube's, with equality for every interaction without a field up to the junction (antiferromagnets included); the exponent of adaptive algorithms without a hint is **not** covered — for it the comparison with the cube is proved for ferromagnets and fields only (Proposition 11.81(c), Theorem 11.64) and is otherwise Conjecture 11.94.  Algorithms reduce to type classes: the class means are Lipschitz in the type, and optimistic refinement over the `n + 1` classes refines a class only as far as its deficit requires; with a random split a type class splits into type classes of the same density | `sum_mem_bracket`, `bracket_width`, `argmax_deficit_le`, `deficit_ge`, `mean_le_of_biregular` **[V]** (the deterministic core of the reduction and the double counting behind the Lipschitz property of the class means); the odds-ratio lemma, binary sufficiency (duality; at negative accuracies with the reviewer's vertex argument), the closed forms, the domination, the random-partition lemma **[P]**; the reading of the inequalities as exponents: given Theorems 11.78, 11.79 **[P, refereed: R10]**; the adaptive exponent of a type class **[C]** | cycle 10, the coordinator (after a workstream on the adaptive question ended without a report); the proofs checked numerically with independent code, harness XXI.1–4 with 21 mutations (profiles with more than two blocks at nonnegative accuracies only); **reviewed by the Scientific Discovery Division (SCI-REV-0001, 25 November 2026): no critical finding, the mathematics sound; four major findings — the summaries claimed every exponent where two of three are proved; the duality step did not cover negative accuracies (repaired, the statement stands); two false sentences in the remark on larger alphabets (corrected before the review); the lemma is in print — and twelve minor ones, all applied**; prior art: capacity of the binary asymmetric channel (textbook), bounds through the Bhattacharyya parameter — the comparison at a fixed odds ratio is **known**: Hasenclever–Scholz 2013 (arXiv:1302.6161), Proposition 8(a), found by the Scientific Discovery Division (SCI-REV-0004); the applications (binary sufficiency on a type class, domination by the cube, the reduction of algorithms) were not found in print by that division |
| G28 | **Heteropolymer product landscapes** — a fixed sequence of site types, any alphabets, single-site known parts, site envelopes that need not be symmetric.  By the symmetry of the sequence alone, for every `n`: the joint-type-stratified sample is optimal among fixed samples up to a polynomial factor and the flat-histogram instance is the hardest invariant one; the quotient envelope is the transport cost.  Single-letter theorem with labelled profiles and transport costs, for every known part that is a function of the joint type.  For product known parts: the flat-histogram instance is as hard as the hardest additive instance; labels are vertices of the sites' Lipschitz polytopes; the game functions of the site types add at one common slope; `F*_j(t) = (1−t)C_t`, the Rényi capacity of the vertex channel, the hardest instance being the Rényi centre; hence `θ_na` is the inverse sphere-packing exponent, `a` the Shannon capacity, and adaptivity (or a hint, at the hardest instance) gains exactly the rate, for rates below the fixed point `h` of that exponent — asymptotically and in the worst case over the class.  The adaptive exponent without a hint is the hinted exponent of the hardest additive instance.  Exponents of site types do not add; for three or more letters `F*` need not be concave and the uniform site law need not be the hardest; uniform sites group their letters, the hardest number of groups at slope `u` being about `e^{u/2}` | `group_nonadaptive_queries_ge`, `group_queries_ge`, `lowDens_shift`, `truncate_admissible` **[V]** (every-`n` lower bounds for any symmetry group), Theorems 11.22, 11.27(a), (b) **[V]** (the inequalities behind the lower bound at additive instances; the product step for several site types is on paper), `exists_ratio_le`, `eq_of_forall_ratio_ge`, `softmin_admissible` **[V]** (the Rényi centre); `GameFunction` ⇒ pair and recursion **[V]** (`GameFunction.pair`; for the start at complete enumeration `iterates_lt_hint_add`); everything else **[P]** — the upper bounds by transfer of Theorems 11.78(b), 11.52, 11.54, 11.64; numbers **[N]** with duality certificates; the grouping statement and the hardest-law statements **[N]** except the exact crossings | cycle 10, workstream W; re-computed by the coordinator with an own implementation (largest deviation `5·10⁻⁷`); one conjecture of the workstream refuted by the coordinator (the uniform law is not the hardest at small slopes), one remark of the coordinator corrected by the workstream's controls (uniform sites with four letters); **reviewed by the Scientific Discovery Division (SCI-REV-0005, with independent replication): Theorems 11.99 and 11.101 proved, 11.101(b) after two gaps in the written proof were closed (the isoperimetric statement for `μ_H`, now Theorem 11.97(c); families indexed by compositions); twelve minor corrections; from its reviews also a universal ceiling `F*(t) ≤ t(1−t)u²/8` and a three-letter site law that is harder than the two-letter cube at slope `0.5` (Proposition 11.103(d), (f))**; prior art: Rényi capacity and centre (Csiszár; Nakiboğlu), sphere-packing exponent (Csiszár–Körner), parallel channels (Gallager) — search summaries only; the identification of certification complexity with these exponents was not found |
| G29 | **Local ensemble-averaged data do not change the exponents of the cube class** (with the Scientific Discovery Division): besides evaluations, let the algorithm know all marginals of the Gibbs measure on at most `k` sites.  Their Theorem C: the hinted (= adaptive) exponent is unchanged.  Proposition 11.104: so is the non-adaptive exponent — cones symmetrised over a linear code with dual distance `k + 1` have exactly uniform `k`-body marginals, cost a factor `|C| ≤ (2n)^{⌈k/2⌉}` in the count and `ln|C|` in the accuracy | `group_nonadaptive_queries_ge` **[V]** (the two-point argument for any transitive group); the proposition **[P]**; exact enumeration at `n = 7` **[N]**; their Lemma A **[K]** (orthogonal arrays), their Theorem C not reviewed by us | cycle 10, the coordinator, answering SCI-MSG-0001 §7(a); not refereed; zero known part and exact marginals only |
| G30 | **Observable free energies: the robust range of a ratio of two macrostate weights** (a question of the Scientific Discovery Division).  `R⁺(A,B) = sup_g Z_g(A)/Z_g(B)` over the admissible residuals of a finite space with a quasi-metric envelope equals the least `λ` for which a transport plan with gains ships the weight of `A` from `λ` times the weight of `B`; only the constraints from `B` to `A` matter, and extremal residuals are pairs closed under the lowest extension to `A` and the highest to `B`.  Closed forms: one state (Theorem 11.12); the two sides of a threshold on the cube with any exchangeable known part (the maximal field; `±n·ln cosh(u/2)` for the two halves of the uniform cube); a macrostate defined by one coordinate (the single-site programme, exact for additive known parts, two-sided bounds with a site-local certificate for pairwise ones); at the exponential scale `max_{P∈𝒜}min_{Q∈ℬ}[W_d(Q,P) + I(Q) − I(P)]`, exact up to the logarithm of the number of type classes for every `n` | `macro_le_of_plan`, `macro_single_le`, `macro_le_card_mul`, `macro_cone_ge`, `closed_pair_cross` **[V]** (weak duality, the sandwich, closed pairs); strong duality (linear programming), the symmetric reduction, the one-coordinate bounds and the limit **[P]**; all checked numerically, harness XXIII.1–4 with 14 mutations, DEAD.26 **[N]** | cycle 10, the coordinator, answering SCI-REQ-0001 Q1; **reviewed and replicated by the Scientific Discovery Division (SCI-RES-0005): stands**; prior art by that division (six searches at summary level): **for a separable envelope the theorem is the classical closed form of the density-ratio class (DeRobertis–Hartigan 1981); the extension to envelopes with the triangle inequality was not found; the dual object (flows with gains) is classical** — its classification: a plausibly original generalisation of a known closed form; the range only, not the number of evaluations.  *With it, the division's own theorem* (Theorem 11.106a, **[V]** by its Lean file, adopted): for a submodular known part and monotone macrostates the two uniform fields are extremal — Holley's inequality; expected by the division to be folklore |
| G31 | **A one-body marginal oracle with a field** (the second question of the Scientific Discovery Division; the theorems are the division's).  With a free exact one-body oracle the class exponents are unchanged for every `n` — adaptive `R^max`, non-adaptive `θ_na`: the hard instance is a mixture of an additive instance and an extreme field whose one-body marginals equal those of the same mixture with a hidden dip (*compensation lemma*: one linear equation in the mixing weight).  At an instance the oracle helps: at the zero residual the exponent lies between a matched-shell lower bound and a tilt upper bound, both strictly below the value without the oracle for `p ≠ ½` | Proposition 11.109 (the criterion) **[P]**, ours; Theorem 11.109a and Proposition 11.109b **[P]/[N]**, the division's (SCI-RES-0006), every step of the former re-derived and the finite statements and numbers replicated by us (harness XXIII.5, XXIII.7 with 14 mutations) | cycle 10; **our first version had two conjectures in place of the theorems — one true for a different reason, one a formula that over-counts, with two wrong numbers** (`DEAD_ENDS.md` D56); not machine-checked; the exact instance-wise exponent is open; prior art (the division's search): density-ratio and oracle models of this kind not found |
| G32 | **Sup-norm (box) classes around a sampleable known part** (the division's request P-T3).  If the remainder next to a known function with exactly sampleable Gibbs measure is known only through pointwise bounds `lo ≤ r ≤ hi`, the cost of an `(ε/2, δ)`-certificate of `ln Z` at an instance is `Θ((Z(lo)/Z(r) − 1)/ε)` up to factors depending on `δ` — at the centre of a constant box `Θ((e^{ρ₋} − 1)/ε)`, independent of the size of the system; deterministic certificates cost the entropy of the known part; the Gibbs–Bogoliubov side costs `O(w²/ε²)`; a sup-norm bound caps the cost of every class it is intersected with | `Zw_sub_le_dip`, `Zw_sub_le_bump`, `detect_ge`, `box_spotCheck_correct`, `logZ_dipAlt_gt`, `box_expected_queries_ge`, `jensen_bracket` **[V]**; the two-point Jensen bound, the deterministic count, the consequences **[P]**; harness XXIV.1–5 with 14 mutations, DEAD.28 **[N]** | cycle 10, the coordinator; not refereed; **elementary: free-energy perturbation with a packing lower bound — classical in spirit, and the upper bound is a Bernoulli estimation problem in disguise; no novelty claimed beyond the placement next to the classes with exponential cost**; prior art at search-summary level only (`docs/prior_art/L10_box_classes.md`) |

Honest reading.  G2 and the identifications of §11.1 are known mathematics.  G1, G3, G5 are
clean reformulations and routine consequences.  The content that was not found in print is
(i) the identification of certificate complexity on product landscapes with a rate–distortion
exponent, its dichotomy (G4), and the finite-temperature counterpart in which the energy gap is
replaced by the free-energy gap of a macrostate (G7) — the exponent formulas themselves are
applications of the type covering lemma and, at finite temperature, of a known theorem of
source coding; (ii) the dimension-free form of the best-first bound (G6); (iii) second-order
envelope classes as a certified interface with a lossless pairwise reduction (G8); (iv) the
statement that these exponents are query complexities — they bound every algorithm, also
randomised ones — together with the randomised finite-temperature theory: the soft gap, a
lower bound on a third exponent, and, on the cube, an accuracy threshold that separates bounded
from exponential worst-case cost, with the exponent at the zero residual in every accuracy
regime (G11); (v) the extension beyond the cube (G12): the right family of perturbations
(generalised dips), the instance-wise threshold as the value of a single-site game with a
second reference measure, and the hint-free threshold of a product class as the smallest
oscillation of a tilted site pressure; (vi) the normal form (G13), which shows that the known
part was never a separate ingredient, and the covering sandwich for dense second-order classes
(G14), which closes the "way out" of §11.7 for constants of order one; (vii) the transition of
second-order classes at finite temperature, the continuum threshold and the hardness of
averages (G15), and what all of this predicts for the chain geometry the program started
from (G16) — the last being the finding with the most direct consequence for the blueprint:
the verified route through per-torsion constants cannot certify long chains; (viii) the first
results with an interacting known part (G17); (ix) the exact exponent of non-adaptive
algorithms without a hint on the cube (G18) — a known method for the lower bound, a routine
combination of truncation, an isoperimetric tail bound and Chernoff for the upper one;
(x) the transfer of classical optimal recovery to residual classes next to a known part
(G19), whose mathematical content is known and whose use here is to say precisely which
uncertainty is cheap: the correlated kind; (xi) the exponent of adaptive algorithms without
a hint (G20), which is the one statement of this report that is a sharp complexity theorem
with matching bounds for all algorithms of a natural model, and whose proof is not short —
its upper bound is a nested algorithm with a delicate count, read line by line by a referee,
tested by a simulation of its logic and by an evaluation in expectation up to `n = 10⁶`, and
machine-checked only in its deterministic parts.  The qualitative phenomenon (adaption
removes an exponential barrier of non-adaptive methods) is known for a log-concave class
(Mathé–Novak 2007); the exact exponent and its coincidence with the hinted one were not
found; (xii) its extension to every bounded accuracy (G21), by a modified algorithm that
uses the *lower* isoperimetric bound inside the closure test — a paper proof by a
workstream, simulated with its own constants by three parties, and refereed ("proved",
R8); (xiii) the first step beyond the uniform cube (G22): with a field the exponents
are again single-letter, "adaptive = hinted" persists as "the worst case without a hint is
the hardest case with a hint", and three natural guesses about what carries over — the
hardest instance, the sampler, the isoperimetric theorem needed — are false; a paper proof
by a workstream resting on a new asymptotic isoperimetric statement, refereed (R9: the
isoperimetric theorem proved; two gaps in the algorithmic part closed); (xiv) the common
analytic core of (xi)–(xiii) as one machine-checked statement about game functions (G23),
with the shear law as its one-sentence form; (xv) a limit theorem for the certificate
sizes of lattice chains (G24): an application of two known techniques — concatenation
with Fekete's lemma, and the cluster method for ground states — to an object that the
collaboration's data made it necessary to define; its value is that a "numerically
vacuous" existence bound is replaced by a bracket one can compute, and that it shows
that no enumerable chain is near the limit — the value at 27 beads is a factor of more than
7 below every limit point — while the chain length at which the limit is approached is an
estimate, not a theorem (the first version said "it says at which chain lengths a plateau
can be expected"; review SCI-REV-0002 of the Scientific Discovery Division); convergence is
proved for bridges off a countable set of accuracies and is a conjecture for unrestricted
walks; the abstract limit theorem is a known special case (row G24);
(xvi) the first known part with interactions (G25): what is new is
less the mean-field computation than two structural facts — that permutation symmetry
alone makes the flat-histogram ensemble the optimal fixed sample and its instance the
hardest symmetric one, for every `n`, and that at phase coexistence the extremal
perturbations are shells of barrier configurations, eventually on part of the system
only; the proofs are the method of types applied inside a type class; refereed (R10),
and the adaptive problem is open except for ferromagnets up to the junction with the
uniform cube; (xvii) rounds of adaptivity (G26): the upper bound is a
re-scheduling of an existing algorithm, the lower bound a coupling argument of the
pointer-chasing kind with a hard instance that is *not* of the nested kind such arguments
usually use — what separates two rounds from many here is dilution of a blind batch by a
flat histogram; one non-trivial step of a hierarchy is proved, the next is open;
(xviii) slices (G27): an elementary inequality about two-by-two tables and a duality
argument; what they buy is a statement without hypotheses on the interaction — for fixed
samples, and for algorithms that are told an instance that is a function of the order
parameter, a known part that depends on the configuration only through that parameter
never has a larger exponent than no known part at all — and the reduction of the open
adaptive problem to a homogeneous space; for adaptive algorithms without a hint the
comparison is a conjecture outside ferromagnets and fields (the restriction is the
Scientific Discovery Division's, SCI-REV-0001, M1: our first version claimed it for
certification as such); the inequality itself is in print (Hasenclever–Scholz
2013; found by the Scientific Discovery Division), only its application here is ours;
(xix) heteropolymer landscapes (G28): the proofs are transfers of proofs already in this
report, and the formulas — Rényi capacity, sphere-packing exponent, parallel channels —
are sixty years old; what is new, if anything, is the *identification*: certifying a
normalising constant over a Lipschitz class with a fixed sample is a covering problem for
the outputs of a channel whose input the sampler does not know, and adaptivity is worth
exactly the sampling rate (for rates below the fixed point `h`, at the exponential scale;
the two theorems behind this were reviewed and found proved by the Scientific Discovery
Division, SCI-REV-0005, which did not recognise the operational statement in print
either).  It also showed that three of our two-letter statements
(concavity, "a field always helps", "the uniform law is the hardest") are two-letter
statements;
(xx) observable free energies (G30): linear-programming duality for a linear-fractional
programme over a cone given by pairwise ratio bounds; the proofs are a few lines each.
What it buys is a change of target — from the total `ln Z`, which no experiment measures,
to differences between macrostates — and a certificate format for it.  The duality is
very likely known in the language of density-ratio classes or of generalised flows;
we have not searched.
Each rests on textbook tools (type covering, Hölder, telescoping, linear-programming duality);
the proofs are short.  The second referee's verdict on G1–G10 — "a coherent note, not a
theorem-driven paper" — is reproduced in §12 together with what a publication would still
need.

**An independent assessment of originality for the query-complexity rows** (Scientific
Discovery Division, SCI-REV-0004, 25 November 2026: full-text reading of the closest
sources where accessible, a search log of 23 queries, own numerical replications; a
review of originality, not of correctness).  Its classification, which we adopt in the
rows above: G27's lemma — **established prior art** (Hasenclever–Scholz 2013); G18's
exponent function and G11's threshold constant — **known special case** and **new
combination** (the formulas are in print at the cone instance: Suárez–Silbey–Oppenheim
2012, Chatterjee–Diaconis 2018; not found: the minimax statements and the role of the
constant as a sharp threshold); G20/G21, adaptive exponent = hinted exponent —
**plausibly original theorem** (not found in information-based complexity, normalising
constants, importance sampling, pure-exploration bandits, sampling-oracle counting or
nested simulation; concept precedents Mathé–Novak 2007, Karnin 2016, Garivier–Kaufmann
2016); G26, two rounds strictly between — **plausibly original**, conditional on the
former and at that time unrefereed (refereed since by the same division, SCI-REV-0003;
rounds for partition functions are studied in 2026 in the
*sampling-oracle* model, at polynomial scale and with the opposite conclusion: Guo, Liu,
Yang, Yin, Zhang; Harris, Kolmogorov, Liu, Yin, Zhang); G22 — **plausibly original
generalisation** (the sampler statement is the capacity-achieving output law / universal
mixture; Theorem 11.63 is a new variant of Ahlswede–Zhang / Yu by their method, not
settled against Yu's theorem); G23, the shear law and the game-function pair — a
**reformulation** (an exponential change of measure; restricted Legendre duality); G25,
first half — a **reformulation** (the invariance principle of design theory, Kiefer, plus
Bakhvalov averaging over the group, with one small new lemma: type-wise quantile
truncation is Lipschitz), second half (shells) unresolved.  **Its summary: one result
would survive a hostile referee — the exact exponents of adaptive and of non-adaptive
randomised algorithms for the normalising constant over the log-Lipschitz cone of the
Hamming cube, neither half alone — and possibly the two-round separation; every novelty
claim on Lemma 11.89, on the formula `θ_na`, on `ln cosh(u/2)` as a number and on "flat
histogram, not Gibbs" as a discovery has to go.**  They have gone, in this version.
What the review did not examine: whether Theorem 11.54 is true (the proof of the cost of
the nested algorithm was not re-derived), and the sources it lists as not accessed
(Novak's papers of 1988–1996, Harper 1966, Kiefer 1959, Ahlswede–Zhang 1999, Yu beyond the
abstract).

**The same for the kernels, the certification geometry and the chain results** (Scientific
Discovery Division, SCI-REV-0006, 25 November 2026: 41 logged searches, full text where
accessible, six statements of its own with proofs or exhaustive computations).  Its
classification, adopted in the rows above and in §0.2: residual kernel (a certificate valid
for a whole envelope class with anchors) — **plausibly original capability**, and the one to
put first; pairwise kernel with dead-end elimination, machine-checked — plausibly original
capability in a *narrow* sense (nativeness and Lean 4; every rule is known, and the
pseudo-Boolean route has verified checkers with measured, moderate overhead); partition
kernel — **new combination** (the sentence that verified checkers exist for exact counting
only was false as a description of the field); voxel-integral enclosures — plausibly
original capability with elementary mathematics; G1 — **reformulation**; G4, dichotomy and
rate–distortion exponent — **plausibly original theorem** (an application of type covering);
G7 — **known special case** for the formula (an example in Merhav 2011), plausibly original
identification with certificate size; G13 — **reformulation of a classical correspondence**
(weightable quasi-metrics); G16 — **known special case** for the growth law (moments of
inertia; a certificate in robot motion planning), consequences for certification plausibly
original; G19 — linear theory **established prior art**, the profile distance a
**reformulation of a named object** (a lower bound of the Gromov–Wasserstein distance), the
consequences for certificates a new combination; G24 — the abstract theorem a **known special
case / reformulation** (see §11.22), the limit shape of the lattice model a plausibly
original generalisation; C4 — plausibly original theorem, elementary, medium confidence.
**Its summary: mature and defensible as new are the class-wide residual kernel, the
certification consequences of the lever arm, the rate–distortion exponent and the limit
shape as an application; known objects under new names, now cited, are the normal form, the
profile distance, the abstract limit theorem, the lever-arm law and the finite-temperature
formula.**  It also contributed a statement that this report lacked — a measurable quantity
inside one of its classes (Theorem 11.48(d)) — and a negative finding that concerns every
use of pair-distance profiles: a profile does not identify a conformation, even on small
lattices, and the theorem usually quoted for the opposite does not cover chains (Theorem
11.48(b)).  Not accessed by the review: Mémoli 2011, the originals of Matthews and of
Künzi–Vajner, Featherstone 2004 beyond the abstract, the body of Tan et al. 2024.

**The picture after cycle 10, in one table.**  What each *kind of knowledge about the
residual* costs, in evaluations of the residual, for an accuracy that is a fixed fraction
of the system size (`n` sites, or `N` beads).  Every entry is a theorem of this report with the
status given there; the table adds nothing, it only puts side by side what was proved in
different sections.

| what is known about the residual `g` | certificate / deterministic procedures | randomised, told the instance in advance ("hint": the task is *verification*) | randomised, no hint, sample fixed in advance | randomised, no hint, adaptive (*search*) |
|---|---|---|---|---|
| **first-order**: `g(x) − g(y) ≤ d(x,y)`, weighted Hamming `d`, product landscape | a covering by slack balls (`isCertificate_iff_cover`); exponential, `exp(nR*)`, unless every site is sharp (Theorems 11.6–11.9); `2^{n(1−o(1))}` on the cube at the zero residual | `exp(n θ_hint(ε₁))` below an accuracy threshold, a bounded number above it (Theorems 11.25, 11.28); single-letter game value at additive instances (11.27) | cube, zero known part: `exp(n θ_na(ε₁))`, `θ_na > θ_hint` (Theorems 11.44, 11.45) | cube, zero known part: `exp(n θ_hint(ε₁))` — the hint is worth nothing (Theorem 11.54); also at every bounded accuracy, `exp(nh)` against `exp(na)` for a sample fixed in advance (Theorem 11.58, refereed); with a field as known part, `exp(nR^max(ε₁))`, the hinted exponent of the hardest additive instance, against `exp(nθ_na(ε₁))` for the best fixed sample, which is uniform on type classes (Theorems 11.61, 11.64, under review) |
| **second-order**: mixed differences bounded by `c_ij` | a star of `n + 1` evaluations determines `g` up to `Σ c_ij` over the changed pairs (`secondOrder_remainder`); with dense constants of order one the cost is exponential again (Theorem 11.31, D40) | a transition at finite temperature (Theorem 11.33) | — | — |
| **linear in `p` known features**, coefficients in a box | `rank ≤ p` evaluations determine `g` everywhere; before that, every linear combination of evaluations gives a bracket (`linRes_span_upper`, `linRes_span_exact`); a kernel for minima (`verifyLTop_sound`) | no lower bound known (a generic evaluation sees every perturbation) | — | — |
| **pair-additive with `L`-Lipschitz radial functions** (chains) | number of evaluations bounded independently of `N` at extensive accuracy, by a numerically vacuous bound; polynomial on lattices at every accuracy (Proposition 11.49).  **Not what one sees at any size that can be enumerated**: measured growth is linear in `N` on the lattice through 27 beads and geometric off-lattice through 15 beads (§11.17, data of the Computational Research Division).  For the lattice chain the limit is identified (§11.22): the covering number of a convex limit shape — proved for bridges off a countable, unidentified set of accuracies, conjectured for all walks; every limit point of the certificate sizes of all walks at `(L, ε₁) = (1, ½)` lies between 116 and 3 627 **[P, computer-assisted]**; a few hundred for the limit and `10³`–`10⁵` beads or more for the chain length at which it is approached are estimates **[N]** (wording after the review SCI-REV-0002; first version: "between 50 and 3 627 …, reached at `10³`–`10⁵` beads") | — | — | — |
| **first-order in a per-torsion envelope** (chains) | `exp(Θ(N))`: the verified constants grow with the lever arm (Theorem 11.37, D42) | — | — | — |

Three readings.  (i) *The kind of class decides, not its size*: the same weighted `ℓ¹` distance
costs `2^{n(1−o(1))}` as an envelope and `n` evaluations as the feature distance of a linear class
(§11.17).  (ii) *Verification against search*: with a hint the task is to verify a claimed
instance, without it to search; for deterministic certification of a minimum, search can be
unboundedly more expensive than the smallest certificate even on the line (§11.11, D39),
whereas for randomised estimation of `ln Z` on the cube class the worst-case costs of the two
have the same exponent — provided the search is adaptive.  (iii) *What is missing* is every
entry marked "—", all of the last three columns outside the cube with a zero known part,
a field (§11.20) or, in part, a mean-field known part (§11.23), and constants everywhere.

---

## 11. Certification geometry

Setting.  `X` finite, `d` an envelope, `f = E₀` known, `g` an unknown admissible residual,
`E = f + g`, `E* = min E`, `gap(y) = E(y) − E*`.  A procedure may evaluate `g` at points of its
choice; the cost is the number of evaluations.  `κ ∈ [0,1]` denotes a Lipschitz constant of the
true residual relative to the envelope, `g(x) − g(y) ≤ κ d(x,y)`; the published envelope is
loose when `κ < 1`.

### 11.1 The admissible class and conditioning (known mathematics)

The admissible class `{g : g(x) − g(y) ≤ d(x,y)}` is the solution set of a closed system of
difference constraints.  In five literatures it has five names — a *polytrope* (tropical
geometry; `d` is its own Kleene star), an *alcoved polytope* / *L-convex set* (discrete convex
analysis; `L♮` after pinning one value), the *Lipschitz polytope* of a finite quasi-metric space
(polar to the Kantorovich–Rubinstein polytope), a *difference-bound matrix* (program analysis)
and a *simple temporal network* (constraint reasoning) — and every statement of §2.3 is a
standard fact about it (`prior_art/L5`, P1–P3).

*Interval and correlated uncertainty in one object.*  Pointwise interval data `lo(x) ≤ g(x) ≤
hi(x)` are difference constraints to one extra "ground" node `o` with `g(o) = 0`
(`d(x,o) = hi(x)`, `d(o,x) = −lo(x)`); pure interval uncertainty is the case in which these are
the only constraints, and the envelope adds the *correlations* `g(x) − g(y) ≤ d(x,y)` between
points.  The extended system is consistent iff it has no negative cycle, and its shortest-path
closure gives the sharp bracket of every `g(x)` and of every difference — this is what
`IProblem.consistent_iff_nonempty` and the McShane brackets of §2.3 are for the weighted Hamming
envelope.  On the extended node set the envelope may take negative values; only the triangle
inequality and the zero diagonal are needed, which is why `IsEnvelope` does not ask for
nonnegativity.

Evaluations add constraints to one extra node, and the closure can be written down:

**Theorem 11.1 (conditional envelope) [V] (`ConditionalEnvelope.lean`).**  Let `g` be evaluated
on `A` with consistent values `v`, and let `L, U` be the McShane envelopes.  Then
`D_A(x,y) = min(d(x,y), U(x) − L(y))` is an envelope (`condEnv_isEnvelope`); a residual that
agrees with `v` on `A` is admissible for `d` iff it is admissible for `D_A`
(`admissible_condEnv_iff`); and `D_A(x,y)` is the largest value of `g(x) − g(y)` over the
consistent admissible residuals (`condEnv_isGreatest`, attained: `condEnv_attained`).
Conditioning in two steps equals conditioning once (`condEnv_tower`), and a single evaluation
leaves the envelope unchanged (`condEnv_singleton`): differences of the residual are informed
only by pairs of evaluations.

So evaluating the residual replaces `d` by the tropical rank-one update `D_A`, and every theorem
of §2.3 applies verbatim to `D_A`: the query-model theorem is the contact-set theorem for `D_A`
(`robust_minimizer_with_anchors_iff'`), and

**Theorem 11.2 (anchored sharp minimum; worst-case regret) [V].**  `x` minimises `f + g` for
every consistent admissible `g` iff `D_A(x,y) ≤ f(y) − f(x)` for all `y`
(`robust_certified_with_anchors_iff`); more generally the largest regret of declaring `x`
optimal is `max_y [f(x) − f(y) + D_A(x,y)]` (`worst_case_regret_isGreatest`).

This is the minimal-network theorem for simple temporal networks (Dechter–Meiri–Pearl 1991) with
one extra node.  (The "potential maximizers" lemma of LIPO — *some* consistent function is
optimised at `x` — is, for `f ≡ 0`, the query-model contact theorem of §2.3, Theorem 2.6; the
statement here quantifies over *all* consistent residuals.)  It is the exact criterion the
referee asked for in §2.4.

### 11.2 Slack, and three notions of certificate

The **slack** of the envelope inequality between `a` and `y` is

    s(a, y) = d(a, y) − g(a) + g(y) ≥ 0.

**Theorem 11.3 (slack geometry) [V] (`CertificationGeometry.lean`).**  `s` is an envelope
(`slack_isEnvelope`), `s ≥ (1−κ) d` (`slack_ge_of_lipschitz`), and with
`s(A,y) = min_{a∈A} s(a,y)`, `s(y,A) = min_{a∈A} s(y,a)`,

    L_A(y) = g(y) − s(A, y),     U_A(y) = g(y) + s(y, A),     min_y (f + L_A) = min_y [E(y) − s(A, y)]

(`lowerEnv_eq_sub_slack`, `upperEnv_eq_add_slack`, `certLB_eq`).  The uncertainty that remains
at `y` after the evaluations is the slack distance between `y` and the evaluated set; it does
not combine across evaluations — it is their minimum.

A **point certificate** is a set `A` with `UB(A) − LB(A) ≤ ε`, `UB(A) = min_A E` the best
evaluated energy and `LB(A) = min(f + L_A)`.

**Theorem 11.4 (certificates are coverings) [V].**  `A` is a point `ε`-certificate iff every `y`
has an evaluated point within slack distance `E(y) − UB(A) + ε` (`isCertificate_iff_cover`).
Hence every certificate covers each `y` within radius `gap(y) + ε` (`cover_of_certificate`), and
a cover with these radii that contains a minimiser is a certificate (`certificate_of_cover`):

    N_cov(ε) ≤ N_point(ε) ≤ N_cov(ε) + 1,

where `N_cov(ε)` is the least number of centres such that every `y` is within slack radius
`gap(y) + ε` of a centre — a covering problem in which **each point carries its own radius, its
optimality gap**.

**Theorem 11.5 (three notions, one number) [V] (`CertificateNotions.lean`,
`RefereeLemmas.lean`).**  A *value certificate* (`min(f+U_A) − min(f+L_A) ≤ ε`) and a
*configuration certificate* for a candidate `x` (`D_A(x,y) ≤ f(y) − f(x) + ε` for all `y`;
equivalently every consistent residual makes `x` `ε`-optimal, `isConfigCertificate_iff`)
satisfy: point ⟹ value ⟹ covering (`isValueCertificate_of_isCertificate`,
`cover_of_isValueCertificate`); point ⟹ configuration (`isConfigCertificate_of_isCertificate`);
and conversely, by exchanging one evaluated point, a value certificate, and a configuration
certificate with at least one evaluation, yield a point certificate of at most the same size
(`value_exchange`, `config_exchange`, `card_exchange_le`: replace the anchor that attains the
upper envelope at the minimiser of `f + U_A`, respectively at the candidate, by that point).
Therefore

    N_cov ≤ N_value = N_point ≤ N_cov + 1,        N_point = max(1, N_config).

The exchange lemmas are due to the second referee (`reviews/R2`, Appendix A); the previous
version of this theorem stated `N_value ≤ N_point` and `N_point ≤ N_config + 1` only.  This
settles the first major point of the first referee report: the witness-size bound of §2.4 is a
statement about point and value certificates; a configuration certificate saves an evaluation
only when none is needed at all (`N_config = 0`: the candidate is optimal for every admissible
residual, Theorem 2.4), although it may *consist* of different points — it can skip a state that
every point certificate evaluates (`config_certificate_skips_forced_point`, `DEAD_ENDS.md` D21).
Harness XI.1, XI.6.

*Prior art.*  The minimal certificate is the "best possible algorithm" `n_B` of
Hansen–Jaumard–Lu (1991), the "proof set" of Baran–Demaine (2004) and the quantity `τ` of
Bachoc–Cesari–Gerchinovitz (2021); the covering picture with radii proportional to the gap is
theirs (in `ℝ^d`, for `f ≡ 0`, symmetric `d`).  New here are only the form — a quasi-metric that
absorbs the true residual, a known part, asymmetric envelopes, an exact "iff" — and the
machine-checked statements.  One real change with a known part: gaps are no longer Lipschitz in
the envelope metric, so the problem is a *priority k-centre* problem with arbitrary client radii
(`prior_art/L4`, C1–C2).

### 11.3 Lower bounds: covering duality and exponential weights

For any covering relation, weak LP duality gives lower bounds on the number of centres.

**Theorem 11.6 [V].**  Let `A` cover every `y` (some `a ∈ A` with `s(a,y) ≤ gap(y) + ε`).
(a) *Weights* (`card_ge_of_weights`): `Σ_y w(y) ≤ |A|` for every `w ≥ 0` with total weight at
most one on the set covered by each centre.  Special cases: points that only themselves cover
are in `A` (`mem_of_forced`; this re-derives Theorem 2.7, `anchor_necessary'`); fooling sets
(`card_ge_of_fooling`); the volume form `Σ_y 1/M(y) ≤ |A|`, `M(y)` a bound on the sizes of the
covered sets that contain `y` (`card_ge_sum_inv`) — a discrete form of the integral
`∫ dx / vol B(x, gap(x)+ε)` of certified Lipschitz optimisation.
(b) *Exponential weights* (`card_ge_exp_weights`): for every `t ≥ 0` and every `v ≥ 0`,

    e^{−tε} Σ_y v(y)  ≤  |A| · max_a Σ_y v(y) e^{−t (s(a,y) − gap(y))}.

(c) *Partition-function bound* (`partition_bound`; the choice `v = e^{−t·gap}`):

    |A|  ≥  e^{−tε} · Σ_y e^{−t·gap(y)} / max_a Σ_y e^{−t·s(a,y)},

the partition function of the true landscape at inverse temperature `t` divided by the
partition function of a slack ball.  For the weighted Hamming envelope and a `κ`-Lipschitz
residual the denominator is at most `∏_i (1 + (k_i − 1) e^{−t(1−κ)c_i})`
(`partition_bound_hamming`).

The fractional covering number satisfies `N_frac ≤ N_cov ≤ (1 + ln max_a |S(a)|) N_frac`
(Lovász; Chvátal) **[K]**, and (a)–(c) are feasible dual solutions, so all bounds are at most
`N_frac` (harness XI.2, where the best exponential-weights bound reaches `0.99 N_frac`).  Bound
(b) is the Chernoff relaxation of the LP dual; it is Csiszár's (1974) dual lower bound on a
rate–distortion function, for the distortion `s(a,y) − gap(y)` — a distortion with a *credit*
equal to the gap of the point `y` that is being covered (`prior_art/L4` C4, `prior_art/L6` T7).  Its value lies
in the next theorem: it tensorises, and on product spaces it is exponentially tight.

### 11.4 Product landscapes: a dichotomy and the exact exponent

Let `X = ∏_i σ_i`, `f(x) = Σ_i φ_i(x_i)`, `d` the weighted Hamming envelope with constants `c_i`,
and (for the exponent) `g(x) = Σ_i γ_i(x_i)` additive with `|γ_i(a) − γ_i(b)| ≤ κ c_i`, `κ < 1`,
`c_i > 0` (so that distinct states have positive slack).  Write
`x*` for the minimiser of `E` and call site `i` **sharp** if `c_i ≤ φ_i(s) − φ_i(x*_i)` for all
`s ≠ x*_i`: every excitation of the *known* part costs at least the envelope constant.

**Theorem 11.7 (one evaluation) [V] (`CertificateComplexity.lean`).**  The single evaluation at
`x₀` is an exact certificate iff `c_i ≤ φ_i(s) − φ_i(x₀_i)` for every site `i` and every state
`s ≠ x₀_i` (`product_single_certificate_iff`, stated for the zero residual; by
`single_evaluation_certificate_iff` the criterion `d(x₀,y) ≤ f(y) − f(x₀) + ε` holds verbatim
for every residual and every envelope); this is also
the criterion for `x₀` to be optimal for every admissible residual (`product_robust_optimal_iff`),
so in that case no evaluation is needed for a configuration certificate.

**Theorem 11.8 (exponential lower bound) [V].**  For all `t ≥ 0`, all site weights `v_i ≥ 0` and
every `ε`-certificate `A`,

    ln |A|  ≥  Σ_i r_i(t; v_i) − tε,      r_i(t; v) = ln Σ_s v(s) − ln max_a Σ_s v(s) e^{−t ρ_i(a,s)},

with the single-site distortion `ρ_i(a,s) = s_i(a,s) − gap_i(s)` (`product_exp_weights`,
`product_rate_bound`; the Boltzmann choice `v_i = e^{−t·gap_i}` is `product_partition_bound`).
Example (`binary_certificate_exponential`): `n` two-state sites, excitation energy `1`, envelope
constants `2`, residual identically zero: every exact certificate has at least `(6/5)ⁿ`
evaluations, while the full enumeration is one (`binary_full_certificate`).

**Theorem 11.9 (exact exponent) [P + K].**  For `n` sites of finitely many types and
`ε = o(n)`,

    ln N_cov(ε) = Σ_i r*_i(t*) + o(n),     Σ_i r*_i(t*) = max_{t ≥ 0} Σ_i max_v r_i(t; v);

for identical sites `n⁻¹ ln N_cov → R* = max_P R(P; ρ, 0)`, the largest rate–distortion function
over single-site sources `P` at distortion level zero.  Moreover `R* = 0` iff the site is sharp,
and then `N_cov = 1`: **the number of evaluations is either one or exponential in the number of
non-sharp sites** (between `exp(Σ_{non-sharp} r_i(t; v_i) − tε)` for any common `t` and
`∏_{non-sharp} k_i`; with a bounded number of non-sharp sites it is bounded).  For identical
sites and zero residual the qualitative dichotomy is machine-checked
(`homogeneous_certificate_dichotomy`: either the single evaluation certifies for every `n`, or
some `ρ > 1` has `ρⁿ ≤ |A|` for every exact certificate).  For two-state
sites with excitation energy `e < c` and zero residual, with `ρ = e/c`,

    R* = max_μ [h(μ) − h(ρμ)] = max_{0<x<1} [ln(1+x) − ln(1+x^{1/ρ})]     (0.1882 nats per site at ρ = 1/2).

*Proof.*  Lower bound: Theorem 11.8, valid for every `n`; maximising over `t` and `v` gives
`max_P R(P; ρ, 0)` by the dual formula
`max_P R(P, D) = max_{t ≥ 0, w ≥ 0 : Σ_s w(s) e^{−tρ(a,s)} ≤ 1 ∀a} [ln Σ_s w(s) − tD]`
(Csiszár's dual form of `R(P,D)` and Gibbs' inequality in `P`); for a product of unequal sites
product weights with a common slope `t` are the best dual weights, because a source with memory
has a rate–distortion function no larger than the memoryless source with the same marginals.
Upper bound, identical sites: the type covering lemma (Csiszár–Körner, Lemma 9.1; Csiszár 1998,
Lemma VI.1), which is uniform in the type and in the distortion level, covers every type class
`T_P` at distortion zero by `exp(n R(P; ρ, 0) + o(n))` centres; there are polynomially many
types; the substitution `w ↦ w e^{−t·gap}` turns the credit distortion into the nonnegative
distortion `s` at the type-dependent level `E_P[gap]` (`prior_art/L6` T8); `R(P, D)` is
continuous at `D = 0` because every letter reproduces itself at zero slack.  Upper bound, sites
of finitely many types `j` with fractions `λ_j` (argument supplied by the second referee): for a
joint type `(P_j)` cover each `T_{P_j}` at a level `D_j` and take the product; among the
allocations with `Σ_j λ_j D_j = Σ_j λ_j E_{P_j}[gap_j]` the least total rate
`Σ_j λ_j R_j(P_j, D_j)` is attained, by convexity in each `D_j`, at a common slope `t` and equals
`max_t Σ_j λ_j [F_j(P_j, t) − t E_{P_j} gap_j]`, `F_j` the dual function of type `j`; maximising
over the joint type gives `max_t Σ_i max_v r_i(t; v)`.  Dichotomy: `r_i(t; v)` is concave in `t`, vanishes at `t = 0`, and its
derivative there is `min_a Σ_s v(s) ρ_i(a,s)`; so `max_v r_i > 0` for small `t` iff the zero-sum
game with payoff `ρ_i(a,s)` has positive value, and since the ground state is covered only by
itself the value is `≤ 0` iff the ground state covers every state, i.e. iff the site is sharp
(`ρ_i(x*_i, s) = c_i − (φ_i(s) − φ_i(x*_i))`; the residual drops out).  The hypothesis `κ < 1` is
needed here: for `φ = (0,0)`, `γ = (0,c)` the site is not sharp, yet the second letter covers
both at zero slack, `R* = 0` and `N_cov = 1 < N_point = 2`.  The binary formula is the
rate–distortion function of a Bernoulli source with Hamming distortion, in primal and dual
form. ∎

*Numerical confirmation.*  For the binary family the fractional cover number is sandwiched by
exact integer layer counts, `max_μ L_μ ≤ N_frac ≤ (n+1) max_μ L_μ`,
`L_μ = min_ν C(n,μ)/|S_ν ∩ layer μ|`; at `ρ = 1/2`: `n⁻¹ ln max_μ L_μ = 0.2073, 0.1994, 0.1947,
0.1919` for `n = 100, 200, 400, 800` against `R* = 0.1882`, and likewise at `ρ = 1/4, 3/4, 9/10`
(benchmark B8 up to `n = 400`; the values for `n = 800` are from a separate run recorded in
`RESEARCH_LOG.md`).  Harness XI.3 checks the lower bound and the
dichotomy by exact linear programming on small products.

*Reading.*  With only a first-order envelope, pointwise evaluations of the residual are either
unnecessary (all sites sharp: the white-box model already decides) or exponentially many in the
number of non-sharp sites are needed (machine-checked for identical sites with zero residual
and `ε = 0`; in general by the paper proof above).  With Boltzmann weights `v_i = e^{−t·gap_i}`
the bound is a free-energy difference, `r_i(t) = ln Z_i^{gap}(t) − ln Z_i^{slack}(t)`: the
single-site partition function of the landscape against that of a slack ball, at a common
inverse temperature `t`.  Two cautions (second referee, M2; `DEAD_ENDS.md` D31; harness
`DEAD.12`).  *The slope `t` is common to all sites*: maximising site by site overshoots — for
the two-state types `(e, c) = (0.5, 1)` and `(5, 10)` the per-site maxima add up to `0.3765` per
pair, the true exponent is `0.2329`.  *Boltzmann weights are optimal for two-state sites with
zero residual, and only a lower bound otherwise*: a three-state site with gaps `(0, 0.5, 3)`,
`c = 1` has `R* = 0.1882` (the optimal weights ignore the third state) against `0.1066`, and the
two-state site `φ = (0, 0.677)`, `γ = (0, 0.644)` has `R* = 0.0252` while the Boltzmann bound is
vacuous.  In general `max_v r_i(t; v)` is one linear program per site and `t`.  For interacting
known parts the one-shot bound of Theorem 11.6(c) gives the Boltzmann estimate with
`Σ_y e^{−t·gap(y)}` computed by a transfer matrix (blueprint §6.6).

### 11.5 Hardness, and what search can achieve

**Theorem 11.10 (minimal certificates contain dominating sets) [V].**  For a graph `G` on `V`
let `X = V ∪ {o}`, `d` the graph metric truncated at 2 with `o` at distance 2 from everything,
`f = 1` on `V`, `f(o) = 0`, `g ≡ 0`.  Then `A` is an exact certificate iff `o ∈ A` and `A ∩ V`
is a dominating set (`domCertificate_iff`); the minimal size is `1 + γ(G)`
(`domCertificate_card`, `domCertificate_min_card`).  Hence computing a minimal certificate is
NP-hard and hard to approximate within `(1−o(1)) ln |X|` **[K]** (dominating set; the greedy
cover of §11.3 matches this factor).

No algorithm can be instance-optimal with respect to `N_cov` **[P]**.  A certificate may consist
of a "hub" of large energy that covers many shallow states, which optimistic search never
evaluates (`DEAD_ENDS.md` D26; in `ℝ^d`, `d ≥ 2`, this is Baran's theorem); and even an algorithm
that looks for hubs must find the right one.  Take a far minimiser `x*`, `N` shallow states
(`f = 1.5`, mutual distance 2) and `M` hubs of large `f` at distance 1 from every shallow state
and 2 from each other, with `g = 0` except `g = −0.7` on all hubs but one: the good hub and `x*`
form a certificate for `ε = 0.1` (slack `1 ≤ 1.6` to every shallow state), a bad hub covers no
shallow state (slack `1.7`), and a shallow state covers only itself.  The algorithm knows `f`
and `d` but not which hub is good, so against an adversary every deterministic procedure makes
at least `min(M, N) + 1` evaluations, while `N_cov = 2`.  The comparison that does hold is with
covers at shrunk radii:

**Theorem 11.11 (best-first search, resource augmentation) [V] (`BestFirst.lean`).**  Let `d` be
symmetric and `g` `κ`-Lipschitz, `κ < 1`.  Best-first search (evaluate a minimiser of the current
lower bound `f + L_A` until `UB − LB ≤ ε`; Piyavskii–Shubert) stops after at most `|C| + 1`
evaluations, for **every** set `C` that covers each `y` within slack radius
`θ (gap(y) + ε/6)`, `θ = (1−κ)/(4(1+κ))` (`bestFirst_card_le`, `bestFirst_certifies`).  The
evaluated points are separated: for `1 ≤ j < k`, `gap_k − gap_j + ε < s(y_j,y_k)`,
`gap_k ≤ s(y_j,y_k)`, `gap_j − gap_k ≤ s(y_k,y_j)` (`bestFirst_sep_a/b/c`), so two of them never
share a centre of a shrunk cover (`not_cocovered`).  The `+1` is needed
(`bestFirst_card_le_sharp`, a two-point instance with `|C| = 1`); the constants `θ` and `ε/6` are
not claimed to be tight (the second referee found no violation with radii `2θ(gap + ε/6)` in
900 instances, and violations at `3θ`).

No doubling assumption is made — and none would help: **the comparison class can be unboundedly
larger than `N_cov`, even on the line** (second referee, M1; `DEAD_ENDS.md` D30; harness
`DEAD.11`).  For `X = {0} ∪ {2^{−i} : i ≤ m}`, `f(x) = x`, `g ≡ 0`, `ε = 2^{−m−3}` the point `0`
alone is a certificate (`N_cov = 1`), every cover at the shrunk radii has `m + 1` points, and
best-first search uses at most two evaluations.  The previous version's remark that in a
doubling space the shrinkage costs only a constant factor is false when the known part is not
constant; for `f ≡ 0`, where gaps are Lipschitz, it remains a conjecture (§12).  The theorem is
the case
`ρ = (1+κ)/(1−κ)` of `bestFirst_card_le_of_quasiSymm`, which needs only an envelope (possibly
asymmetric) whose slack is `ρ`-quasi-symmetric, `s(x,y) ≤ ρ s(y,x)`, with `θρ ≤ 1/4`.  Known special cases: dimension
one without augmentation (Hansen–Jaumard–Lu 1991: `n_P ≤ 2 n_B + 1` for bounding the value and
`n_PY ≤ 4 n_B + 1` for value and point, the counterpart of the point certificates used here);
`ℝ^d` up to `log(1/ε)` and
`exp(d)` factors (Bachoc et al. 2021); the proof is an adaptation of the 2-approximation for
priority k-centre (Plesník 1987) (`prior_art/L4`, C7).  The theorem is a worst-case statement:
on random instances (benchmark B9) best-first search uses about `3.0` evaluations against a
smallest cover of `2.0`–`2.4`, exceeding `N_cov + 1` in `3`–`13 %` of the runs, while the shrunk
covers it is compared with have `8`–`10` points; on the hub family it evaluates every leaf
(`17` evaluations against a certificate of `2`).  Harness XI.4 (with the hub family), `DEAD.6`.
A second bound, with the radius attached to the centre and valid for every admissible
residual, and line instances on which the search is unboundedly worse than the smallest
certificate, are in §11.11.

### 11.6 Finite temperature

**Theorem 11.12 (thermal contact) [V] (`ThermalRobustness.lean`).**  Over the admissible class
the Gibbs probability `π_g(x) = e^{−βE(x)}/Z` of a state ranges exactly over

    [ 1 / Σ_y e^{−β(f(y) − f(x) − d(x,y))} ,  1 / Σ_y e^{−β(f(y) − f(x) + d(y,x))} ],

the ends being attained by `g = −d(x,·)` and `g = d(·,x)` at every `β`
(`gibbsProb_range_eq`; with evaluations: `gibbsProb_range_with_anchors_eq`, in which `d` is
replaced by the conditional envelope).  As `β → ∞` the upper end tends to a positive limit iff
`x` is on the contact set, and the lower end tends to one iff `x` is a strict sharp minimum:
Theorems 2.3 and 2.4 are the zero-temperature limits.  In the weights `w = e^{−βg}` the class is the
polyhedral cone `w(y) ≤ e^{βd(x,y)} w(x)` (`admissible_iff_weights`), so robust Boltzmann
averages of any observable are linear-fractional programs with optima at polytrope vertices;
the closed form is special to single states (`prior_art/L5`, P5–P6).

**Theorem 11.13 (free-energy certificates are quantizers) [V].**  With `π` the Gibbs ensemble of
the true energy,

    Z(f + L_A)/Z = E_π e^{β s(A,Y)},        Z(f + U_A)/Z = E_π e^{−β s(Y,A)}

(`Zhi_eq`, `Zlo_eq`).  If the optimistic partition function is within `e^ε` of the true one — in
particular if `A` certifies `ln Z` to within `ε` (`Zhi_le_of_bracket`) — then:
(a) the mean slack distance from `A` is at most `ε/β` (`mean_slack_le`);
(b) *entropy bound* (`card_ge_entropy`): for every `t ≥ 0`,
`H(π) ≤ ln |A| + ln max_a Σ_y e^{−t s(a,y)} + tε/β`;
(c) *Hölder exponential-weights converse* (`thermal_exp_weights`; `card_ge_laplace` is the case
`p = 1/2`, `v = π`): for `p ∈ (0,1)`, `t = β(1−p)/p` and every `v ≥ 0`,

    Σ_y π(y)^{1−p} v(y)^p  ≤  (|A| · max_a Σ_y v(y) e^{−t s(a,y)})^p · e^{(1−p)ε}.

So the evaluated set is a quantizer of the Gibbs ensemble for the distortion `e^{βs}`, and its
size is at least `exp(entropy)` up to the partition sum of a slack ball.  As `β → ∞` with `ε/β`
fixed, (c) becomes Theorem 11.6(b) (with the weights `v e^{−t·gap}`).

**Theorem 11.14 (transport–entropy duality at fixed `β`) [V + K].**  For every reference `μ`,
every admissible `g` and every `β ≥ 0`, with the tilted measure `ν ∝ μ e^{βg}` and **any**
coupling `γ` of `(ν, μ)`,

    ln E_μ e^{β(g − E_μ g)} = β (E_ν g − E_μ g) − KL(ν‖μ) ≤ β Σ_{x,y} γ(x,y) d(x,y) − KL(ν‖μ)

(`logMGF_eq_tilt`; `transport_le` is weak Kantorovich duality, `E_ν g − E_μ g ≤ Σ γ d`;
`logMGF_le_transport_entropy`).  Minimising over couplings gives
`≤ β W_d(ν,μ) − KL(ν‖μ)` with `W_d` the transport cost, which by Kantorovich–Rubinstein duality
for quasi-metrics **[K]** equals `sup_{g admissible} (E_ν g − E_μ g)`.  Consequently a transport
inequality `Σ γ d ≤ √(2C·KL(ν‖μ))` for the coupling gives the sub-Gaussian bound `β²C/2`
(`gap_le_of_T1`).
Conversely every `ν` is matched by its Kantorovich potential (Donsker–Varadhan), so
`sup_g ln E_μ e^{β(g−E_μ g)} = sup_ν [β W_d(ν,μ) − KL(ν‖μ)]` **[K]** (Gozlan–Léonard 2007,
Cor. 7.11; Bobkov–Houdré–Tetali 2006).  This is the fixed-`β` statement that replaces the
Bobkov–Götze equivalence of §3.2; the orientation matters for asymmetric envelopes (for the
Boltzmann factor `e^{−βΔ}` the roles of `ν` and `μ` in `W_d` are exchanged).  It unifies the
passive bounds: the zero-evaluation free-energy gap of §3.2 is the transport–entropy conjugate
of the envelope, product references give `Σ c_i²` (Marton, McDiarmid), dependent references the
Wasserstein-matrix constants — and the extremal residual is then no longer additive
(`DEAD_ENDS.md` D25).  Harness XI.9.

**Theorem 11.15 (exact exponent at finite temperature) [V lower bound; P upper bound].**  For
`n` identical independent sites with single-site Gibbs measure `π`, slack `s` (positive off the
diagonal: `κ < 1`, `c > 0`) and accuracies `ε_n` that are neither extensive nor exponentially
small — `ε_n = o(n)` **and** `ln(1/ε_n) = o(n)`, e.g. `ε_n ≥ n^{−m}` — the least number of
evaluations in a certificate of `ln Z` to within `ε_n` satisfies

    n⁻¹ ln N_Z → R_β = max_Q R(Q; s, KL(Q‖π)/β)
               = max_{t ≥ 0, v ≥ 0} { ((β+t)/β) ln Σ_s π(s)^{t/(β+t)} v(s)^{β/(β+t)} − ln max_a Σ_s v(s) e^{−t s(a,s)} }.

The distortion allowed to a macrostate (type) `Q` is `KL(Q‖π)/β = F_β[Q] − F_β`, **its
free-energy gap**; as `β → ∞` it becomes the energy gap `Σ_s Q(s) gap(s)` and `R_β → R*`
(Theorem 11.9).  Always `R_β ≥ H(π)` (take `Q = π`): at finite temperature and sub-extensive
accuracy the number of evaluations is exponential in the thermodynamic entropy even when every
site is sharp.  Example (`thermal_binary_exponential`): two-state sites with excitation energy
`2`, envelope constants `1` — one evaluation certifies the ground state exactly
(`thermal_binary_sharp`) — at `β = ln 2`: every certificate of `ln Z` to within `ε` has at least
`e^{−ε} (6/5)ⁿ` evaluations.  (The hypothesis actually used, `Z(f+L_A) ≤ e^ε Z`, holds with
equality for the single evaluation of the ground state at `ε = n ln(6/5)`,
`thermal_binary_single_tight`; it involves the true `Z` and is not computable from the
evaluations — as a two-sided certificate that single evaluation has width `n ln(4/3)`.)

*Proof.*  Lower bound: Theorem 11.13(c) with product weights (`thermal_product_exp_weights`),
valid for every `n`; the maximum over `p` and `v` equals `max_Q R(Q; s, KL(Q‖π)/β)` by the dual
formula for `R(Q, D)` and the Gibbs variational principle in `Q` (the distortion level
`KL(Q‖π)/β` is linear in `ln π` and `ln Q`).  Upper bound: cover every type class `T_Q` at the
per-site distortion `D_Q = max(0, KL(Q‖π)/β − a_n)`,
`a_n = [(k+1) ln(n+1) + ln(4/ε_n)]/(nβ)` (type covering, which is uniform in the type and in the
level; a class with `D_Q = 0` is evaluated entirely, because the slack is positive off the
diagonal).  Here `a_n → 0` is exactly the hypothesis `ln(1/ε_n) = o(n)`.  Every `y ∈ T_Q` has
`e^{β s(A,y)} ≤ e^{nβD_Q}`, `π(T_Q) ≤ e^{−n KL(Q‖π)}`, and there are at most `(n+1)^k` types, so
the classes with `D_Q > 0` contribute at most `(n+1)^k e^{−nβ a_n} ≤ ε_n/4` to
`Z(f+L_A)/Z = Σ_Q π(T_Q) E[e^{βs} | T_Q]` and have total mass at most `ε_n/4`; hence
`Z(f+L_A)/Z ≤ 1 + ε_n/4` and `Z(f+U_A)/Z = E_π e^{−βs(Y,A)} ≥ π(A) ≥ 1 − ε_n/4`, and the two ends
differ by at most `ε_n` in logarithm (for `ε_n ≤ 1`).  The rate is
`max_Q R(Q; s, D_Q) + o(1) = R_β + o(1)` by continuity of the rate–distortion function. ∎

*The restriction on the accuracy is necessary* (second referee report, C1; `DEAD_ENDS.md` D29).
For `ε = 0` every certificate of `ln Z` is the whole space, `N_Z(0) = kⁿ`
(`exact_free_energy_certificate_eq_univ`), whereas `R_β < ln k` unless `π` is uniform.  More
generally a two-sided certificate forces `π(Aᶜ) ≤ ε/(1 − e^{−β s_min})`, so for `ε_n = e^{−λn}`
the evaluated set contains at least half of every type class with `KL(Q‖π) < λ` and the exponent
is at least `max{H(Q) : KL(Q‖π) < λ}`, which reaches `ln k` once `λ > KL(uniform‖π)`.  The
construction above with `a_n → λ/β` gives the upper bound
`max_Q R(Q; s, (KL(Q‖π) − λ)₊/β)` in that regime; whether it is attained is open.  (Theorem 11.9
has no such restriction: `ε = 0` is allowed there.)

The single-letter identity and the lower bound were checked
numerically (the two sides agree to `10⁻³` on a grid; `R_β = 0.666, 0.482, 0.216` at
`β = 1, 4, 40` for `e/c = 1/2`, approaching `R* = 0.188`, benchmark B8; harness XI.8 tests the
one-shot converse on every evaluated set of small instances).  For the sharp site of the
example above the exponent is `R_β = 0.514` (entropy `0.500`); the verified one-shot bound with
uniform weights gives `ln(6/5) = 0.182`.

*Attribution.*  The upper bound is an instance of a known source-coding theorem.  Merhav
("On optimum strategies for minimizing the exponential moments of a given cost function",
arXiv:1103.2882, 2011) shows that for fixed-rate lossy coding of a memoryless source `P` the
optimum exponential rate of `E exp(α n d)` is `max_Q [α D_Q(R) − D(Q‖P)]`, `D_Q(R)` the
distortion–rate function of `Q`, by type covering; the formula for `R_β` is the rate at which
this exponent vanishes for `P = π`, `α = β`, `d = s`.  (The guessing exponent
`max_Q [ρ R(D;Q) − D(Q‖P)]` of Arikan–Merhav 1998 is the same kind of object.)  We read the
general theorem and its variational identity in the paper; the rate–distortion example was
available to us only through an automatic summary.  The science division has since read the
section in full (`SCI-REV-0006` W7): the statement is an *example* of a general observation of
Merhav's §4 — if a strategy attains `n[λ(Q) + o(1)]` on every type class and no strategy does
better on a non-negligible fraction of it, then "it is then a straightforward exercise to
show, using the method of types" that the optimum exponent is `max_Q [αλ(Q) − D(Q‖P)]` (his
eq. (37)) — for memoryless finite-alphabet sources and additive distortion, with
`λ(Q) = D_Q(R)` by type covering.  So the formula for `R_β` is a corollary of an example, not
of a numbered theorem, and the attribution stands **[K, the relevant section read in full by
the science division]**.  What was not found is the identification — the complexity of
certifying a free energy under an envelope *is* this exponent, with the distortion budget of a
macrostate equal to its free-energy gap — and the one-shot converse of Theorem 11.13
(`prior_art/L4` C9, `prior_art/L6` T6).

*The contrast with linear information.*  One reference average `⟨Δ⟩₀` — a single *linear*
functional of the residual — pins `ln Z` to within `β² Σ c_i²/8` (Theorem 3.1), and `N` random
evaluations estimate it to `±(Σc_i² ln(2/δ)/(2N))^{1/2}` with confidence `1−δ`, independently of
the size of the state space **[K]**.  Deterministic point-wise certification to an extensive accuracy
`ε = nε₁` still costs exponentially many evaluations whenever `ε₁` is below a threshold — by
Theorem 11.13(b), `n⁻¹ ln |A| ≥ H(π) − ln(1 + (k−1)e^{−t(1−κ)c}) − tε₁/β` for every `t` — which
includes the accuracy `β²c²/8` per site of the sandwich when `βc` is small and the Gibbs entropy
is not (for a cold sharp site, `e^{−βe} ≲ βc/8`, the single evaluation of the ground state
already reaches that accuracy).  So at the accuracy of the sandwich the exponential price is
the price of *deterministic* information; Theorem 11.21 (§11.9) is the machine-checked
randomised statement.  Randomisation does not rescue at every accuracy: on the uniform cube
class, below the accuracy `n ln cosh(βc/2)` — which is strictly smaller than the width
`β²Σc_i²/8` of Theorem 11.21 — every algorithm needs exponentially many evaluations on the zero
residual, with a smaller exponent (Theorem 11.25, §11.10); for other product references this is
proved only below an instance-dependent accuracy (`ε₁^crit`, §11.10).

### 11.7 Second-order envelopes: a way out under weak coupling

A residual class with bounded *mixed* differences,

    |g(x^{i→a, j→b}) − g(x^{i→a}) − g(x^{j→b}) + g(x)| ≤ c_ij        (all x, i ≠ j, a, b),

bounds the non-additive part of the residual only.  In such a class information from different
evaluations *does* combine.

**Theorem 11.16 (star sandwich) [V] (`SecondOrderEnvelope.lean`).**  Let `x₀` be a reference
configuration and let `g` be evaluated on its star (`x₀` and its `Σ_i (k_i − 1)` single-site
neighbours).  With the additive interpolant `g_star(x) = g(x₀) + Σ_i [g(x₀^{i→x_i}) − g(x₀)]` and
symmetric `c`,

    |g(x) − g_star(x)| ≤ Σ_{i<j, both changed} c_ij        (`secondOrder_remainder`),

so `E₀ + g` lies between two *pairwise* models whose one-body tables contain the star
evaluations and whose pair tables are shifted by `∓ c_ij/2` on changed pairs
(`pairwise_sandwich`); a certificate of the lower model accepted by the tropical kernel bounds
the true energy (`verify_sound_secondOrder`).  If `c ≡ 0` the residual is determined by its star
(`starPart_eq_of_additive`).

**Theorem 11.17 (the sandwich is the exact envelope) [V].**  For symmetric nonnegative `c` the
two functions `g_star ∓ Σ_{i<j changed} c_ij` belong to the class and agree with `g` on the star
(`secondOrder_lower_attained`, `secondOrder_upper_attained`); so they are the least and greatest
elements of the set of residuals consistent with the star data
(`secondOrder_envelope_exact`) — a McShane–Whitney theorem for the second-order class, in which
the extremal extensions are pairwise models.  Consequently the robust problem is *exactly* a
pairwise problem (`secondOrder_robust_min_exact`), and `x₀` is a minimiser for every consistent
residual of the class iff it minimises its own lower pairwise model
(`secondOrder_certified_minimizer_iff`): a second-order sharp-minimum condition, in which the
*measured* single-site excitation energies of the full energy compete with the pair constants
`c_ij` only.  Harness XI.11 confirms exactness against a linear program over the whole class.

**Theorem 11.18 (order `m`) [V] (`HigherOrderEnvelope.lean`; harness XI.10).**  If all mixed
differences of order `m` over a set `T` of sites are bounded by `c_T` (`HigherDiffBound`), then
the anchored interpolant `I_{m−1} g` of order `m−1` (`anchoredInterp`: the truncated cut-HDMR /
many-body expansion at `x₀`, which uses `g` on the Hamming ball of radius `m−1` and is exact
there, `anchoredInterp_eq_of_card_lt`, by the Möbius identity `anchored_decomposition`)
satisfies `|g(x) − I_{m−1}g(x)| ≤ Σ_{T ⊆ changed sites, |T| = m} c_T` (`higherOrder_remainder`),
and for nonnegative constants the bound is attained at every configuration by a member of the
class with the same ball data.  (Machine-checked for zero ball data, where the member is the
remainder function itself, `higherOrder_remainder_sharp`, and for `m = 2` with arbitrary data,
`secondOrder_lower_attained`; for `m ≥ 3` with arbitrary data it is **[P]** — the interpolant has
no differences of order `m` — and was confirmed by linear programming for `m = 3`.)  For `m = 2`
it is Theorem 11.16
(`secondOrder_remainder_of_higherOrder`); a three-site instance of order three is
`higherOrder_witness`.  *Proof.*  `h = g − I_{m−1}g`
vanishes on the ball and has the same order-`m` differences.  Induct on `m` and on the number
`w` of changed sites: for a changed site `j`, `|h(x)| ≤ |h(x with j reset)| + |D_j h|`, and
`D_j h`, as a function of the other sites, vanishes on the ball of radius `m−2` and has
order-`(m−1)` differences bounded by `c_{T∪{j}}`. ∎  The anchored decomposition and its
remainder estimates are classical (Kuo–Sloan–Wasilkowski–Woźniakowski 2010; Griebel–Holtz 2010);
its use as a certified residual class with an exact reduction to a kernel was not found
(`prior_art/L5`, P9).

*Limitation: the remainder is quadratic in the distance* (second referee, M3; `DEAD_ENDS.md`
D32; harness `DEAD.13`).  The half-width of the star envelope, `Σ_{i<j changed} c_ij`, grows with
the square of the Hamming distance from the centre, and further evaluations of the same kind do
not remove this.  For `n` two-state sites with dense constants `c_ij = c`, the function
`−c·C(|x| − 1, 2)` belongs to the class, vanishes on the *whole Hamming ball of radius 2* around
`x₀ = 0` and equals `−c(w−1)(w−2)/2` at weight `w`; so with `f(x) = e|x|` and zero true residual
not even the `1 + n + C(n,2)` evaluations of that ball certify the minimiser once
`n ≥ 2e/c + 3`, and two stars at opposite corners do not once `n ≥ 6e/c + 6` (an explicit
member vanishing on both is given in the referee report).  A star certifies exactly when the
second-order sharp-minimum condition of Theorem 11.17 holds; for an additive known part a
sufficient condition is the **row-sum condition**
`½ Σ_{j ≠ i} c_ij ≤` (measured single-site excitation energy at site `i`, for every state)
**[P]** — then `Σ_{i ∈ S} Δ_i ≥ ½ Σ_{i ∈ S} Σ_{j ∈ S, j ≠ i} c_ij = Σ_{i<j ∈ S} c_ij` for every set
`S` of changed sites.  With non-sparse constants, star-type data lead back to a covering
problem, now with radius of order `(2·gap/c)^{1/2}`; whether other evaluation sets do better is
open.

*The resulting picture.*  First-order envelope: uncertainty is a distance to the evaluated set,
information is tropical (a minimum over evaluations), certification is covering, the price is
exponential unless the known part is sharp (Theorems 11.4, 11.9, 11.15) — for every algorithm
(§11.10).  Second-order envelope with weak coupling (row sums of the constants below the
measured excitation energies): `n(k−1)+1` evaluations determine the additive part exactly, the
remainder is a pairwise function, and certification returns to the pairwise kernel, whose own
cost is governed by the proof-complexity results of §6.  Away from that regime the star is
re-centred at the incumbent — a trust-region scheme without a guarantee of termination by
itself (blueprint §6.6).  What dense constants cost, exactly, is the subject of §11.12: no set
of evaluations escapes the quadratic law, the price is exponential unless the excitation
energies are of the order of `c·n`, and the star is not the best choice of `n+1` evaluations.

### 11.8 A partition-function kernel with decomposition rules

The referee's fourth major point (§3.4) is repaired in `PartitionProduct.lean` by extending the
certificate type to `ZCert2` with two rules.

**Theorem 11.19 (cut rule) [V].**  For a set `S` of sites and bounds `lo ≤ W_ij ≤ hi`,
`lo ≥ 0`, on the pair factors across the cut,
`Λ · Z_S · Z_{Sᶜ} ≤ Z ≤ Υ · Z_S · Z_{Sᶜ}` with `Λ, Υ` the products of the bounds
(`WInstance.Z_cut`), with equality when the cut factors are identically one
(`WInstance.Z_cut_eq`).  The extended checker is sound (`zverify2_sound`, `zverify2Top_sound`).
On two disjoint frustrated triangles one cut and 16 leaves give the exact value `169/16`
(`twoTriangles_cut_exact`), while every certificate without decomposition rules whose lower end
is exact has at least `64` leaves (`cut_rule_separation`; in general at least the number of
configurations of the box for positive rigid instances, `zverify2_elementary_exact_leaves`).

**Theorem 11.20 (elimination rule) [V].**  A site with at most two neighbours can be summed out
exactly into a one-body factor of its neighbour or a pair factor between its two neighbours
(`WInstance.Z_elim1`, `WInstance.Z_elim2`).  For **every** chain-structured instance on `m+1`
sites with nonnegative factors the explicit transfer-matrix certificate — `m` eliminations and
one leaf — is accepted by the kernel with the exact partition sum (`zverify2Top_chainCert`,
`chainCert_leaves`).  If the factors are positive and the instance is rigid, every certificate
built from the elementary rules (leaf, branch, thermal prune) whose lower end is exact has at
least `k^{m+1}` leaves (`chain_separation`); for the two-state ferromagnetic chain this is
`1` against `2^{m+1}` for every length (`ferroChain_separation`; `elimination_separation` is
the kernel-evaluated case of six sites).  Trees and cycles reduce in the same way
(`tree_elim_exact`, `ring_elim_exact`); in general the rule is exact on every interaction graph
reducible by removing sites of degree at most two (treewidth at most two) **[P]**.

`chain_separation` is the finite-temperature counterpart of the tropical separation of §6.3,
proved on a *connected* family, with two reservations (second referee, M4; `DEAD_ENDS.md` D33).
*It concerns exact lower endpoints only*: a certificate whose lower end is `(1 − 10⁻⁹) Z` is
outside the theorem, although approximate enclosures are the normal case at finite
temperature; a robust version is open.  *Its hypothesis `WInstance.Rigid` is a property of the
representation, not of the model*: it asks that one of the two ordered factors `W_ij`, `W_ji`
distinguishes the states of a site, and the instance with `W₀₁(a,b) = 2^{a+2b}`,
`W₁₀(b,a) = 2^{−(a+2b)}` — two independent uniform sites, every configuration of weight one —
satisfies it, so that the theorem requires four leaves for it (`gauge_trivial_separation`).
What is measured in such a case is that the leaf rule bounds the two orientations of a pair
separately; a normalisation of the instance would remove it.  For the ferromagnetic chain the
interaction is genuine and the statement is as intended.  The tropical kernel's `sum` rule and
these two rules are the same idea in two semirings; what remains open is a lower bound for
certificates that *do* use decomposition rules on frustrated connected families, an
approximate version of the separation, and a comparison with proof systems for model counting.
Harness XI.12.

### 11.9 Probabilistic certificates: the sampled sandwich

The lower bounds of §11.6 concern deterministic certificates built from pointwise evaluations.
Randomised evaluation of a *linear* functional of the residual behaves differently.

**Theorem 11.21 (sampled free-energy sandwich) [V] (`SampledSandwich.lean`).**  Let
`μ₀ = ⊗_i p_i` be a product reference on `n` sites, `Δ` a residual with bounded differences
`c_i`, `C = Σ_i c_i²`, and let `x⁽¹⁾, …, x⁽ᴺ⁾` be independent samples of `μ₀` with empirical mean
`m̂ = N⁻¹ Σ_k Δ(x⁽ᵏ⁾)`.  Then

    P( |m̂ − ⟨Δ⟩₀| ≥ η ) ≤ 2 exp(−2Nη²/C)                              (`sample_mean_two_sided`),

and outside an event of at most that probability

    −β m̂ − |β| η  ≤  ln(Z/Z₀)  ≤  −β m̂ + |β| η + β² C/8                 (`sampled_free_energy_sandwich`, `sampled_free_energy_sandwich_good`).

Hence `N ≥ C ln(2/δ)/(2η²)` samples give confidence `1 − δ`
(`sampled_free_energy_sandwich_of_sample_size`), and one sample size works for all alphabets,
all numbers of sites, all product references and all residuals with `Σ c_i² ≤ C₀`
(`exists_sampled_sandwich_sample_size`): the number of evaluations does not depend on the
number of states.  The proof is the Chernoff bound for
the sum of `N` independent copies, each sub-Gaussian by the tensorisation lemma behind
Theorem 3.1(c); probabilities are finite sums over sample tuples.  The statement presupposes
exact sampling from the product reference, exact evaluation of `Δ`, and a known `Z₀`; the floor
`β²C/8` of the width is not reduced by more samples.  Harness XI.13 (exact enumeration of
sample tuples).

*The contrast, on one instance.*  Take the landscape of `thermal_binary_exponential`: `n`
two-state sites, excitation energy `2`, envelope constants `1`, `β = ln 2`, the known part as
the (product) reference.  A deterministic certificate of `ln Z` to within `ε` needs at least
`e^{−ε} (6/5)ⁿ` evaluations (Theorem 11.15).  The sampled sandwich has width
`β²C/8 + 2βη = 0.0601 n + 1.39 η`; at that accuracy the deterministic bound is still
`exp(0.122 n − 1.39 η)`, whereas `n ln(2/δ)/(2η²)` samples suffice with confidence `1 − δ`.
So the exponential price of §11.6 is the price of *deterministic pointwise* certification under
a first-order envelope: a probabilistic guarantee from a reference average costs polynomially
many evaluations.  The verified kernels do not check randomness; a kernel for such
probabilistic certificates (sampled averages with verified concentration bounds) is not built
here.  §11.10 supplies its two foundations: a soundness theorem for spot-checked hints, and a
limit of what any randomised procedure can achieve — on the uniform cube class, below
`n ln cosh(βc/2)`, an exponential number of evaluations again in the worst case (at the zero
residual; Theorem 11.25).  Between that accuracy and the width `β²Σc_i²/8` of the sandwich above,
a bounded number of evaluations still suffices (Theorem 11.25(b)).

### 11.10 Algorithms, not certificates: query complexity

Sections 11.2–11.9 bound the size of a certificate of a given format.  The first referee asked
whether such bounds constrain every *algorithm*; the second asked for an algorithmic statement
and for a probabilistic notion of certificate (`reviews/R2`, §4, items 3 and 7).  This section
answers both.

*Model.*  A deterministic algorithm chooses evaluation points adaptively and returns a number.
Abstractly (`QueryAlgorithm`): for every residual a finite set of queried points and an output,
such that a residual which agrees with `g` on the points queried on `g` yields the same queries
and the same output — the only property of decision trees that is used.  The class is strictly
larger than the class of decision trees (the partial assignments `g|Q(g)` need only partition
the function space; `Referee3.pathoAlg_not_a_tree` is a partition that no query order
realises), which only strengthens the lower bounds; the upper bounds below are two-round
procedures.  A randomised algorithm is a *finite* probability space of deterministic ones (the
arguments are pointwise in the random seed and extend to arbitrary mixtures; the formal
statements cover finite ones).  An algorithm is *`ε/2`-correct* for a
functional `Φ` on a class if its output is within `ε/2` of `Φ` on every member (so `ε` is a
width, as for certificates), and *`(ε/2, δ)`-correct* if this holds with probability at least
`1 − δ` on every member.

**Theorem 11.22 (sensitive alternatives must be detected) [V] (`QueryLowerBound.lean`).**  Let
`Φ` be any functional and `G` any class of residuals.
(a) If a deterministic algorithm is `ε/2`-correct on `G`, then on every instance `g ∈ G` it
queries a point where `g'` differs from `g`, for every `g' ∈ G` with `|Φ(g') − Φ(g)| > ε`
(`exists_query_ne`).
(b) If a randomised algorithm is `(ε/2, δ)`-correct on `G`, every such `g'` is detected with
probability at least `1 − 2δ` (`prob_query_ne_ge`).
(c) Hence, for alternatives `g_j` of this kind and weights `w_j ≥ 0` such that every point
detects alternatives of total weight at most `B`,

    Σ_j w_j ≤ B · |Q(g)|   (deterministic),        (1 − 2δ) Σ_j w_j ≤ B · E|Q(g)|   (randomised)

(`card_queries_ge_packing`, `expected_queries_ge_packing`).
(d) *Pairs.*  More generally, for any two members `g₁, g₂ ∈ G` with `|Φ(g₁) − Φ(g₂)| > ε`, the run
on an arbitrary residual `g` must query a point where `g₁` or `g₂` differs from `g` — with
probability at least `1 − 2δ` for a randomised algorithm (`exists_query_ne_pair`,
`prob_query_ne_pair`; (a) and (b) are the case `g₂ = g`).
(e) *Converse: the hedged spot-check.*  The algorithm that is given `g` as a hint and a number
`o`, evaluates the residual at `N` independent points drawn from a distribution `q`, returns `o`
if all values agree with the hint and evaluates everything otherwise, is `(ε/2, δ)`-correct on
`G`, provided every `g' ∈ G` with `|Φ(g') − o| > ε/2` differs from `g` on a set of `q`-probability
at least `p` and `(1−p)^N ≤ δ`; on `g` itself it makes at most `N` evaluations
(`hedgedSpotCheck_correct`, `hedgedSpotCheck_card_le`; `spotCheck_correct` is the unhedged case
`o = Φ(g)`).

So the least expected number of evaluations *at an instance* `g`, among algorithms that are
correct on the whole class, is bracketed by two fractional hitting numbers, up to the factors
`1 − 2δ` and `ln(1/δ)`.  From below, by (d): the sets `D(g₁) ∪ D(g₂)`, `D(g') = {g' ≠ g}`, over all
pairs with `|Φ(g₁) − Φ(g₂)| > ε`.  This is the fractional relaxation of a value certificate: a set
`A` meets all these unions iff the values of `Φ` consistent with `g` on `A` have width at most
`ε`, and the least size of such a set is the deterministic instance complexity (for the
admissible class and the minimum: `N_value`, Theorem 11.23(a)).  From above, by (e): the sets
`D(g')` over all alternatives whose value lies outside a window of width `ε` around the best
hedge `o`.  A distribution that hits the second family hits the first (of two values more than
`ε` apart one lies outside the window), not conversely, and the two levels must not be
confused with those of the *unhedged* spot-check: that one has to detect alternatives at level
`ε/2`, the lower bound (b) counts alternatives at level `ε`, and the difference is not a
constant — a factor `e^{Θ(ε)}` on the cube (benchmark B10), unbounded at zero temperature
(`reviews/R3`, M1).  These are the counterparts, for real-valued classes, of notions of Boolean
query complexity: certificate complexity (instance complexity with a hint,
Grossman–Komargodski–Naor 2020) and fractional block sensitivity (equal to fractional
certificate complexity), which bounds randomised decision-tree complexity from below (Aaronson
2003; Tal 2013; Gilmer–Saks–Srinivasan 2016; Kulkarni–Tal 2016).  For deterministic algorithms
(a) is the radius-of-information argument of optimal recovery.  The method is known; what
follows is what it gives for the envelope class.  The factor `1 − 2δ` cannot be improved in
general (`Referee3.packing_factor_attained`: full evaluation with probability `1 − 2δ` and two
blind guesses attain (c) with equality).

*Dips.*  The alternatives used below are single **dips**,
`dip_{y,c}(a) = min(g(a), g(y) − c + d(a,y))`.  A dip is admissible (`dip_admissible`), lowers
`g` at `a` by exactly `(c − s(a,y))₊` (`dip_eq_sub`) — so it differs from `g` exactly on the
open slack ball `{a : s(a,y) < c}` — and by `c` at its centre.  If a dip of depth `r(y)` at `y`
changes `Φ` by more than `ε`, the queries must reach within slack `r(y)` of `y`
(`queries_cover_of_sensitive`), and the packing bounds hold for the balls of radii `r(y)`, also
in exponential-weights form (`expected_queries_ge_of_radius`, `expected_queries_ge_exp_weights`).

**Theorem 11.23 (the minimum: every algorithm pays the covering price) [V].**
(a) *Deterministic, exact.*  On an admissible instance `g` there is an algorithm, `ε/2`-correct
for `min(f+g')` on **every** admissible residual `g'`, that makes exactly `k` evaluations on `g`,
iff `g` has a value `ε`-certificate with `k` points (`instance_query_complexity`).  The queried
set of a correct algorithm is a value certificate (`queries_isValueCertificate`: both McShane
envelopes of the evaluated values are admissible and receive the same output); conversely
"evaluate `A`; if the values agree with those of `g` return the midpoint of the certified
interval, otherwise evaluate everything" is correct (`certificateAlgorithm_correct`).  With
Theorem 11.5, the best instance-wise number of evaluations is `N_value = N_point`, which is
`N_cov` or `N_cov + 1`.
(b) *Randomised.*  A dip of depth `gap(y) + ε'`, `ε' > ε`, lowers the minimum by at least `ε'`
(`inf_dip_le`).  Hence if a randomised algorithm is `(ε/2, δ)`-correct on the admissible class,
then on every instance and for all `t ≥ 0`, `v ≥ 0`, `ε' > ε`,

    (1 − 2δ) e^{−tε'} Σ_y v(y)  ≤  E|Q(g)| · max_a Σ_y v(y) e^{−t(s(a,y) − gap(y))}

(`expected_queries_ge_exp_weights_min`; weights form `expected_queries_ge`).  All lower bounds of
§§11.3–11.4 are of this form, so each of them holds for the expected number of evaluations of
every randomised algorithm with the extra factor `1 − 2δ` (on a finite space the open relation
`s < gap + ε'` for `ε'` slightly above `ε` is the closed relation `s ≤ gap + ε` of §11.3).  Example
(`binary_randomized_exponential`): on the binary landscape of Theorem 11.8,
`E|Q| ≥ (1 − 2δ)(6/5)ⁿ 2^{−ε}`.  The proof uses correctness on the instance and on one dip per
point only; under that hypothesis the factor `1 − 2δ` is attained (uniform metric: a mixture of
full evaluation and two blind guesses; harness XII.2).  For correctness on the whole class it
is not optimal in general: if `k` residuals (the instance among them) have pairwise
distinguishable values and agree outside a common set, that set is missed with probability at
most `kδ/(k−1)`, by the same argument **[P]**.

(c) *Randomised, converse.*  An admissible alternative whose minimum is lower by more than
`ρ` differs from the instance on a whole closed slack ball `{a : s(a,y) ≤ gap(y) + ρ}`, and one
whose minimum is higher by more than `η` differs at every `η`-minimiser
(`lower_alternative_differs_on_ball`, `higher_alternative_differs_on_minimisers`).  Hence, for
`0 < η < ε`, the hedged spot-check of Theorem 11.22(e) with output `E* − ε/2 + η` — which has to
detect the alternatives whose minimum is below `E* − (ε − η)` or above `E* + η`, and no others —
is `(ε/2, δ)`-correct on the whole class as soon as the sampling distribution gives probability
at least `p` to every closed ball `{a : s(a,y) ≤ gap(y) + ε − η}` and to the set of
`η`-minimisers, and `(1−p)^N ≤ δ` (`min_hedgedSpotCheck_correct`).  With an optimal fractional
cover mixed with a point mass at a minimiser, `p = 1/(N_frac(ε − η) + 1)`.  The unhedged version
(`min_spotCheck_correct`, `η = ε/2`) needs the balls at level `ε/2`, and `N_frac(ε/2)` can exceed
even the integral covering number at level `ε` without bound (uniform metric, `ε = 1.5 d`:
`N_cov(ε) = 1`, `N_frac(ε/2) = |X|`).

*Consequences.*  (i) At zero temperature randomisation gains the integrality gap of the covering
problem and no more: the least expected number of evaluations at an instance, among
`(ε/2, δ)`-correct algorithms, satisfies

    (1 − 2δ) N_frac(ε)  ≤  min_alg E|Q(g)|  ≤  ⌈ ln(1/δ) (N_frac(ε⁻) + 1) ⌉,

where `N_frac(ε⁻) = lim_{η↓0} N_frac(ε − η)` is the fractional covering number with open balls;
it equals `N_frac(ε)` except at the finitely many values of `ε` at which some `s(a,y) − gap(y)`
equals `ε`.  The lower bound holds for every algorithm, the upper bound for the hedged
spot-check, which is given the instance as a hint; `N_frac ≥ N_cov/(1 + ln |X|)`, and the exponent
`R*` of Theorem 11.9 is unchanged.  (ii) The question left open in the previous version of §12 —
can a procedure reach the exponent `R*` without knowing the residual? — has a simple answer on
additive instances **[P]**.  *Learn-then-cover*: evaluate a star (`n(k−1)+1` evaluations), form
the additive interpolant, compute a small cover for it (a type-covering code, or the greedy
cover, which loses a factor `1 + n ln k`), evaluate the cover and check the certificate; if the
check fails, fall back to any correct procedure.  This is correct on the whole first-order
class, and on an additive instance the interpolant *is* the residual (`starPart_eq_of_additive`),
so it uses `exp(nR* + o(n))` evaluations there; by (b) no algorithm, randomised or not, uses
fewer than `(1−2δ) exp(nR* − o(n))`.  So `R*` is the exponent of the query complexity on
additive instances, not only of a certificate size.  The pattern is general: *query complexity
≤ cost of learning a model of the residual + cost of verifying that model*, and the
verification cost — a covering number, or the hitting numbers of Theorem 11.22 — cannot be
avoided.  (iii) What no algorithm can do is stay
within a constant factor of `N_cov` on *all* instances: on the hub family of §11.5 (`M` hubs,
`N` shallow states, `N_cov = 2` at every instance with a good hub) every randomised decision
tree has `max_j E|Q(g_j)| ≥ ((1−2δ)²/8) min(M, N)` **[P]**.  The instance-wise bound cannot show
this (it is `2(1−2δ)` at each `g_j`); the proof uses correctness on a further instance, the one
without a good hub, where by (b) every shallow state is evaluated with probability `1 − 2δ`,
and the fact that the run on `g_j` follows the run on that instance until hub `j` is evaluated
(`reviews/R3`, Appendix B).  So the instance-wise costs of this section are attained by
algorithms tailored to the instance, not by one algorithm on all instances.

**Theorem 11.24 (the free energy: soft gaps) [V].**  For `β ≥ 0` define the **soft gap**

    Λ(y) = ln Z(f+g) − ln Z(f+U_y),        U_y(x) = g(y) + d(x,y)

(`softGap`): `β` times the free-energy excess of the most pessimistic landscape consistent with
the single value `g(y)`; `0 ≤ Λ(y) ≤ −ln π(y)` (`softGap_nonneg`, `softGap_le`).  A dip of depth
`c` at `y` multiplies `Z` by exactly `E_π e^{β(c − s(Y,y))₊}` (`sum_exp_dip`), which is at least
`e^{βc − Λ(y)}` (`log_sum_exp_dip_ge`).  Therefore:
(a) the queries of every deterministic algorithm that is `ε/2`-correct for `ln Z` reach within
slack `c` of every `y`, for every `c` with `βc > Λ(y) + ε` (`thermal_queries_strict_cover`);
(b) for every randomised `(ε/2, δ)`-correct algorithm, all radii `r(y)` with
`β r(y) > Λ(y) + ε`, all `t ≥ 0` and all `v ≥ 0`,

    (1 − 2δ) Σ_y v(y)  ≤  E|Q(g)| · max_a Σ_y v(y) e^{−t(s(a,y) − r(y))}

(`thermal_expected_queries_ge`);
(c) the queries of a deterministic `ε/2`-correct algorithm (`β > 0`) form a free-energy
certificate: the partition functions of the two McShane envelopes of the evaluated values agree
within `e^ε` (`thermal_queries_bracket`), so every bound of §11.6 on such certificates
(Theorems 11.13 and 11.15: the entropy bound, the Hölder converse, the exponent `R_β`) is a
bound on the number of evaluations of every deterministic algorithm;
(d) *the soft gap is a relaxation.*  It enters only through the inequality
`(c − s)₊ ≥ c − s`.  Without it (`thermal_exact_dip_randomized`): the packing bound of (b) holds
for all radii `r(y)` such that the dip itself is sensitive, `ln E_π e^{β(r(y) − s(Y,y))₊} > ε`.  The
two criteria agree when `e^ε − 1 ≳ 1` and differ widely for small `ε`: for `ε = 0`, `β > 0` and
positive slacks off the diagonal every dip of positive depth is sensitive, so every randomised
algorithm makes at least `(1 − 2δ)|X|` evaluations on that instance (machine-checked on the
cube, `cube_exact_randomized`) — the randomised counterpart of
`exact_free_energy_certificate_eq_univ` — whereas the soft-gap radius `Λ(y)/β` stays positive.

As `β → ∞` with `ε/β` fixed, `Λ(y)/β → min_x [gap(x) + s(x,y)]`, which is `gap(y)` when the known
part is admissible (and gives an equivalent family of covering constraints otherwise), and (b)
becomes Theorem 11.23(b): the zero-temperature covering theory is the limit of the *randomised*
finite-temperature theory.

On a product landscape both sides of (b) factorise (the soft gap of a configuration is the sum
of the single-site soft gaps `Λ₁(b) = −ln Σ_a π(a) e^{−β s(a,b)}`), so there are three
distortion budgets for a macrostate (type) `P`, and three exponents `max_P R(P; s, budget)`:

| problem | budget of `P` | exponent | status |
|---|---|---|---|
| minimum, all algorithms | `E_P[gap]` | `R*` | lower bound **[V]** for every `n`, also randomised; upper bound **[P]** |
| `ln Z`, deterministic, accuracy `ε_n = o(n)` with `ln(1/ε_n) = o(n)` | `KL(P‖π)/β = F[P] − F` | `R_β` | lower bound **[V]**, for every deterministic algorithm; upper bound **[P]** (Merhav) |
| `ln Z`, randomised, accuracy `nε₁` | `(E_P[Λ₁] + ε₁)/β` | `R^rand_β(ε₁)`: a **lower bound** on the exponent | **[V]** for every product landscape (`thermal_product_randomized`, with `softGap_hamEnv_additive`), **[P]** single-letter; upper bounds on the exponent: `U_β` **[V]** (Theorem 11.26, with a hint) and `R_β` **[P]**; the exponent itself is known only on the cube at the zero residual (Theorem 11.25) |

The deterministic budget carries an entropy credit, `KL(P‖π) = E_P[−ln π] − H(P)`, because a
deterministic algorithm must exclude dips at *all* points of a type class at once (the lower
envelope dips everywhere simultaneously), whereas a randomised one only has to detect each
fixed perturbation with constant probability.  (`R^rand_β` is called an exponent for brevity; it
is a lower bound on the randomised exponent, exact where Theorem 11.25 says so.)  Numerically
(benchmark B10) `R^rand_β ≤ R_β`,
both tend to `R*` as `β → ∞`, and `R^rand_β → 0` as `β → 0`; for the site of Theorem 11.9
(`e/c = 1/2`): `0.0275` against `0.666` at `β = 1`, `0.154` against `0.482` at `β = 4`, `0.1882`
against `0.216` at `β = 40`.  A sharp site (`R* = 0`) still has `R^rand_β > 0` at intermediate
temperatures (`0.013` at `β = 1` for `e/c = 2`).

*No sharp regime at finite temperature* **[P]**.  The bound `R^rand_β(ε₁)` vanishes exactly when
`ε₁ ≥ ε₁^crit = max_P min_a E_P[β s(a,·) − Λ₁]`, the value of a zero-sum game (the rate–distortion
function vanishes iff the budget reaches `min_a E_P s(a,·)`).  It depends on the instance.  At
the zero residual of a two-state site (symmetric slack `c`, excited-state probability `p`) the
game is solved by the uniform `P`:

    ε₁^crit = ½ ln(1 + 2p(1−p)(cosh βc − 1)) = ½ ln E_{a,b ∼ π⊗π} cosh(β s(a,b)),

which is positive for every `β > 0` and `0 < p < 1` (benchmark B10 compares it with the linear
program).  So below a positive accuracy per site, certifying `ln Z` at such an instance is
exponentially hard for every algorithm, even when every site is sharp for the minimum.  As
`β → ∞` the threshold tends to `0` for a sharp site (`e > c`) and grows like `β(c − e)/2` for a
non-sharp one; on the cube (`p = 1/2`) it is `ln cosh(βc/2)`, where it is also the point above
which a bounded number of random evaluations suffices on every instance (Theorem 11.25).  The
zero residual is not the worst additive instance in general (for `e/c = 1/2`, `β = 1`:
`0.11367` there, `0.11383` at the additive residual with site difference `−0.037c`; benchmark
B10), and at additive residuals of extreme slope the threshold tends to `0` — those instances
are determined by few evaluations.  For two-state sites `ε₁^crit` is the true threshold of the
instance, and its largest value over additive instances is the hint-free threshold of the
class; for sites with three or more states the dip bound is not the last word, and the
threshold is larger (Theorems 11.27–11.28).

**Theorem 11.25 (the cube: a sharp threshold, and the accuracy diagram at the zero residual) [V lower bounds; P + K upper bounds].**
Let `X = {0,1}ⁿ`, `f ≡ 0`, `d = c ·` Hamming distance, `u = βc > 0`, and consider algorithms that are
`(ε/2, δ)`-correct for `ln Z` on the whole class.  Write `Λ₁ = ln(2/(1+e^{−u}))` for the soft gap of
one site, `B(k)` for a Hamming ball of radius `k`, and

    Δ_k = ln( 1 + 2^{−n} Σ_{j ≤ k} C(n,j) (e^{u(k+1−j)} − 1) )

for the effect on `ln Z` of the dip of depth `c(k+1)` at the zero residual (it is supported on
`B(k)`).
(a) **[V]** *Lower bounds at the zero residual.*  If `ε < Δ_k`, then
`E|Q(0)| ≥ (1 − 2δ) 2ⁿ/|B(k)|` (`cube_exact_dip_randomized`; the machine-checked statement has the
two finite sums over the cube, whose closed forms above are elementary counting).  In
particular `E|Q(0)| ≥ (1 − 2δ) 2ⁿ` whenever `ε < Δ_0 = ln(1 + 2^{−n}(e^u − 1))`, e.g. for `ε = 0`
(`cube_small_accuracy_randomized`, `cube_exact_randomized`).  In soft-gap form
(`cube_thermal_randomized_bound`, for all `n`, `β`, `c`, `R` and `t ≥ 0`): if `ε + nΛ₁ < βR`, then
`E|Q(0)| ≥ (1 − 2δ) 2ⁿ e^{−tR} (1+e^{−tc})^{−n}`; with `ε = nε₁`, `R = ρnc` and the best `t`,

    n⁻¹ ln E|Q(0)|  ≥  ln 2 − h(ρ(ε₁)) − o(1),        ρ(ε₁) = (Λ₁ + ε₁)/u,

which is positive iff `ε₁ < ln cosh(u/2)` (note `Λ₁ + ln cosh(u/2) = u/2`).  A closed instance
(`cube_thermal_randomized_exponential`): `n = 4m`, `u = ln 16`, `ε < 0.2425 m`:
`E|Q(0)| ≥ (1 − 2δ)(27/16)^m`.
(b) **[P]** *Above the threshold, on every instance.*  If `ε₁ > ln cosh(u/2)`, a number of random
evaluations independent of the number of states suffices on every instance: with `m̂` the
empirical mean of `g` over uniform samples,
`ln Z ∈ [n ln 2 − βm̂ − βη, n ln 2 − βm̂ + βη + n ln cosh(u/2)]` outside an event of probability
`2e^{−2Nη²/(nc²)}` — the sandwich of Theorem 11.21 with the exact constant of the two-point
reference in place of `β²Σc_i²/8` (each martingale difference is a symmetric two-point variable
of half-width at most `c/2`, so `0 ≤ ln E e^{−β(g − Eg)} ≤ n ln cosh(u/2)`).
(c) **[P + K]** *Matching upper bounds at the zero residual.*  By Harper's vertex-isoperimetric
theorem, among the admissible residuals that vanish outside a set `D` of given size the lower
envelope of a Hamming ball has the largest partition function: `Z ≤ Σ_x e^{u dist(x, Dᶜ)}`, and
for every `t` the set `{x : dist(x, Dᶜ) > t}` is largest when `Dᶜ` is an initial segment of the
simplicial order (harness XII.5 checks all supports for `n ≤ 4`).  Hence an admissible
alternative that raises `ln Z` by more than `Δ_k` differs from `0` at more than `|B(k)|` points,
and one that lowers it by more than `η` at more than `(1 − e^{−η}) 2ⁿ` points.  The hedged
spot-check of Theorem 11.22(e) with uniform samples and output `ln Z(0) + ε/2 − η`, `0 < η < ε`,
therefore gives, with `k*(ε)` the least `k` such that `Δ_k > ε`,

    (1 − 2δ) · 2ⁿ/|B(k*(ε))|  ≤  min_alg E|Q(0)|  ≤  ⌈ ln(1/δ) · max( 2ⁿ/|B(k*(ε−η) − 1)| , 1/(1 − e^{−η}) ) ⌉

(`|B(−1)|` read as `1`; full evaluation, `2ⁿ`, is always available).  With `η = min(1, ε/2)` the
two sides agree, for **every** `n` and `ε > 0`, up to `ln(1/δ)/(1 − 2δ)` and a factor polynomial in
`n` — a constant depending only on `u` when `ε ≥ 2` — because `e^{Δ_{k+1}} − 1 ≥ e^u (e^{Δ_k} − 1)`
(so the two radii differ by `O(1 + 1/u)`) and `|B(k*(ε) − 1)| (e^u − 1) ≤ 2ⁿ (e^ε − 1)` (so `1/ε` never
dominates the lower bound by more than a factor `n + 1`).  Benchmark B10 evaluates both sides
exactly for `n ≤ 3200`.  Without the hedge (`η = ε/2`) the upper bound is larger by `e^{Θ(ε)}`
(`e^{30}` at `ε = 0.06n`, `n = 3200`), which is why the previous version of this theorem was not
proved at extensive accuracy.
(d) **[P]** *Exponents.*  Consequently `lim n⁻¹ ln min_alg E|Q(0)|` exists in each regime and
equals, with `η* = 1/(1+e^u)` and `λ_c = ln 2 − h(η*) = Λ₁ − uη*`:

| accuracy | exponent at the zero residual |
|---|---|
| `ε = nε₁`, `ε₁ > ln cosh(u/2)` | `0` (bounded cost, on every instance, by (b)) |
| `ε = nε₁`, `0 < ε₁ < ln cosh(u/2)` | `ln 2 − h((Λ₁ + ε₁)/u)` |
| `ε_n = o(n)` and `ln(1/ε_n) = o(n)` | `ln 2 − h(Λ₁/u)` |
| `ε = e^{−λn}`, `0 < λ ≤ λ_c` | `ln 2 − h((Λ₁ − λ)/u)` |
| `ε = e^{−λn}`, `λ_c ≤ λ ≤ ln 2` | `λ` |
| `ε = e^{−λn}` with `λ ≥ ln 2`, or `ε = 0` | `ln 2` |

(the exponent of `Δ_{κn}` is `h(κ) − ln 2` for `κ ≤ η*` — the volume of the ball — and
`uκ − Λ₁` for `κ ≥ η*`).  The third row is `0.0077, 0.029, 0.097, 0.156` at `u = 0.5, 1, 2, ln 16`.
The soft-gap bound of Theorem 11.24 gives the first three rows and nothing more: for
exponentially small accuracies it is a relaxation that is not attained, and the statement of
the previous version, that it is attained up to a polynomial factor for every `ε = o(n)`, was
false (third referee, C1; `DEAD_ENDS.md` D35; harness `DEAD.15`) — the same omission as in
Theorem 11.15.  In the regime `λ_c ≤ λ ≤ ln 2` the cost is of order `1/ε`: the price of seeing a
deficit of relative size `ε` by uniform sampling.

So on this class the accuracy `n ln cosh(βc/2)` — the largest Jensen gap of the class — is a
sharp threshold **for the worst case over instances**.  Above it, a bounded number of random
evaluations suffices on every instance; below it every algorithm, randomised or not, needs
exponentially many on the zero residual.  It is not a statement about every instance of the
class: the residual `c|x|` is determined by its values at `0…0` and `1…1` (both McShane envelopes
of these two values coincide), so with that hint two evaluations suffice at every accuracy and
temperature (third referee, M4).  A deterministic algorithm needs at least
`exp(n(ln 2 − h(ε₁/u)))` evaluations on the zero residual at accuracy `nε₁` and `2^{n(1−o(1))}` for
`ε = o(n)` (`cube_deterministic_lower_bound`): at this instance randomisation is worth the
accuracy `nΛ₁`, the soft gap.  For small `u` the exponent of the third row is `≈ u²/32`.
*Without a hint* the worst-case cost on this class is at least that and at most
`(cosh u)ⁿ/(δ(1 − e^{−ε/2})²)`: plain Monte Carlo over uniform samples, by Chebyshev's inequality,
since `E e^{−2β(g − Eg)} ≤ (cosh u)ⁿ` by the martingale argument of (b) and `E e^{−βg} ≥ e^{−βEg}`
**[P]**.  §11.16 replaces this Chebyshev bound: the value `e^{KL(π‖uniform)} ≈ e^{nu²/8}` at the
additive worst case (Chatterjee–Diaconis 2018) is the exact exponent of plain Monte Carlo on
the whole class and of every non-adaptive algorithm (Theorems 11.44–11.45), so the exponent
of algorithms without a hint lies between `≈ u²/32` and `≈ u²/8`; where between, for adaptive
algorithms, is open (§12).

**Theorem 11.26 (soft-gap sampling: an upper bound in the same quantity) [V].**  Let `β ≥ 0`.
(a) The soft gap is Lipschitz for `β` times the slack, `Λ(x) ≤ Λ(z) + β s(z,x)`
(`softGap_le_add_slack`): `Λ/β` is itself the profile of an admissible perturbation.
(b) *Detection weights.*  Let `w(z) = e^{−βE(z)} ((1+η) e^{Λ(z)} − 1)`.  Every admissible `g'` with
`Z(f+g') ≥ (1+η) Z(f+g)` differs from `g` on a set of weight at least `ηZ`
(`detection_weight_ge`).  Proof: if `e^{β(g−g')} ≤ (1+η) e^{Λ}` everywhere, compare term by term.
Otherwise some point `x₀` carries a dip deeper than its soft gap allows; `g'` then differs from
`g` on the whole slack ball of that depth around `x₀`, on which, by (a), the weights dominate
`e^{−βE(z)} ((1+η) e^{Λ(x₀) − βs(z,x₀)} − 1)`, and these sum to exactly `ηZ`.  An admissible `g'`
with a smaller partition function differs from `g` on Gibbs weight at least `Z − Z(f+g')`
(`gibbs_weight_ne_ge`).
(c) Hence the (unhedged) spot-check of Theorem 11.22(e) with the sampling distribution
`q = ½ π + ½ w/W` (`thermalSampler`), `η = e^{ε/2} − 1`, `W = Σ_z w(z)`, is `(ε/2, δ)`-correct for
`ln Z` on the whole admissible class as soon as `(1 − p)^N ≤ δ`,
`p = ½ min(ηZ/W, 1 − e^{−ε/2})` (`thermal_spotCheck_correct`).  Since
`W = (1+η) Z E_π e^{Λ} − Z` (`sum_dipWeight_eq`), `N = ⌈2 ln(1/δ) E_π[e^{Λ}] / (1 − e^{−ε/2})⌉`
samples suffice.

Together with Theorem 11.24, the least expected number of evaluations at an instance `g`, among
algorithms that are `(ε/2, δ)`-correct on the whole class, is bracketed by two functionals of
the soft gap:

    (1 − 2δ) · Pack{ slack balls of radius (Λ(y) + ε)/β }  ≤  min_alg E|Q(g)|  ≤  ⌈ 2 ln(1/δ) E_π[e^{Λ}] / (1 − e^{−ε/2}) ⌉

(the lower bound for every algorithm; the upper bound for the spot-check, which is given `g` as
a hint — see "Without a hint" below).

On a product landscape `E_π e^{Λ} = ∏_i Σ_b π_i(b) e^{Λ_i(b)}`, so at an additive instance the
randomised exponent lies between `R^rand_β` and `min(R_β, U_β)`,
`U_β = ln Σ_b π(b) / Σ_a π(a) e^{−βs(a,b)}`.  For the site of Theorem 11.9 (`e/c = 1/2`):
`U_β = 0.216, 0.365, 0.521` against the deterministic `R_β = 0.686, 0.666, 0.605` at
`β = 0.5, 1, 2` — there **randomisation provably lowers the exponent**; at `β = 4` the bound
(`0.630`) exceeds the deterministic exponent (`0.482`) and says nothing, and as `β → ∞` it does
not tend to `R*` (for this site it tends to `ln 2`).  On the cube class the separation holds at
every temperature and is machine-checked on both sides: every deterministic algorithm makes at
least `e^{−tε/β} 2ⁿ (1+e^{−tc})^{−n}` evaluations on the zero residual, for every `t ≥ 0`
(`cube_deterministic_lower_bound`; almost `2ⁿ` for bounded `ε`), while the spot-check needs
about `(2/(1+e^{−βc}))ⁿ` (`cube_dipWeight_sum`) — both are costs at the zero residual, and the
spot-check is given that residual as a hint.  The upper bound is crude — it charges every
point of the support with the deepest dip that point could carry alone, and it is not hedged —
and on the cube it is far from the exponent `ln 2 − h(Λ₁/u)` of Theorem 11.25(d) (`ln(2/(1+e^{−u}))`
against it: `0.380` against `0.029` at `u = 1`); closing the gap on general product landscapes
is the isoperimetric question of §12.  The factor `1/(1 − e^{−ε/2})` in the sample size is of
order `1/ε` for small `ε` and is not an artefact: it is the cost of the volume regime of
Theorem 11.25(d).  Harness XII.6; benchmark B10.

*Without a hint* **[P]**.  On instances whose residual is additive the hint can be learned:
evaluate a star, take the additive interpolant `ĝ` (admissible, and equal to `g` when `g` is
additive, `starPart_eq_of_additive`), and spot-check `ĝ` with the sampler of (c) computed from
`ĝ`, the number of samples being chosen after `ĝ` is known.  Whatever the instance, the output
is within `ε/2` with probability at least `1 − δ` (Theorem 11.26(c) applies to the hint `ĝ` and
every admissible `g`), and on additive instances the cost is `n(k−1) + 1 + N`.  So on additive
instances the exponential gap between randomised and deterministic cost holds for algorithms
that are given nothing but the known part and the envelope.

**Theorem 11.27 (generalised dips: what an algorithm must detect at finite temperature) [V; product form: P with machine-checked ingredients] (`GeneralisedDips.lean`).**
Single dips are not the only perturbations that have to be excluded.  Let `β ≥ 0` and let
`Φ : X → ℝ` be Lipschitz for the slack of the instance, `Φ(x) − Φ(y) ≤ s(x,y)` for all `x, y`.
(a) **[V]** For every `r` the residual `g − (r − Φ)₊` is admissible (`genDip_admissible`), differs
from `g` only on `{Φ < r}`, and

    ln Z(f + g − (r − Φ)₊) − ln Z(f+g)  =  ln E_π e^{β(r − Φ)₊}  ≥  βr − Λ(Φ),        Λ(Φ) = −ln E_π e^{−βΦ}

(`sum_exp_genDip`, `log_sum_exp_genDip_ge`).  The slack distances `Φ = s(·,y)` are of this kind and
give the dips and the soft gap `Λ(y)` of Theorem 11.24 (`dip_eq_genDip`, `softGap_eq_softGapOf`).
Every other `Φ` is a lower envelope `min_y [Φ(y) + s(·,y)]` of shifted distances, so a
generalised dip is a union of single dips with centre-dependent depths — the perturbations of
`DEAD_ENDS.md` D34.
(b) **[V]** Hence, for every finite family `(Φ_j, r_j)` with `β r_j > Λ(Φ_j) + ε`, all weights `w ≥ 0`
and all `t ≥ 0`, a randomised algorithm that is `(ε/2, δ)`-correct for `ln Z` on the admissible
class satisfies

    (1 − 2δ) Σ_j w_j  ≤  E|Q(g)| · max_a Σ_j w_j e^{−t(Φ_j(a) − r_j)}

(`genDip_expected_queries_ge_exp_weights`; packing form `genDip_expected_queries_ge`; for
`Φ_j = s(·,j)` this is Theorem 11.24(b), `genDip_recovers_dips`).
(c) **[P; ingredients V]** *Product landscapes.*  Let `X = Sⁿ` with identical sites, single-site
Gibbs law `π` and slack `s₁`, at an additive instance.  For a site function `φ` with
`φ(a) − φ(b) ≤ s₁(a,b)` put `σ_φ = φ − Λ(φ)/β`, so that `E_π e^{−βσ_φ} = 1`.  Let `M` be a probability
vector on finitely many such functions, draw a centre `φ⃗ ∼ M^{⊗n}` and take
`Φ(x) = Σ_i σ_{φ_i}(x_i)`.  It is Lipschitz for the product slack and `Λ(Φ) = 0`, so every radius
`r > ε/β` is sensitive (`sumSig_lipschitz`, `genDip_product_effect`), and by Markov's inequality a
fixed point lies in the supports of centres of total weight at most `e^{tr} ρ_t(M)ⁿ`,
`ρ_t(M) = max_a Σ_φ M(φ) e^{−tσ_φ(a)}` (`detect_weight_le`).  With (b): for every `n`, `t ≥ 0`, `M`,

    E|Q(g)|  ≥  (1 − 2δ) e^{−tε/β} ρ_t(M)^{−n},
    n⁻¹ ln E|Q(g)|  ≥  R^gen_β(ε₁) := max_{t ≥ 0} [ −ln val(K_t) − tε₁/β ],        K_t(a, φ) = e^{−tσ_φ(a)},

where `ε = nε₁` and `val` is the value of the matrix game in which the adversary mixes over the
vertices `φ` of the Lipschitz polytope `{φ : φ(a) − φ(b) ≤ s₁(a,b)}/ℝ` of the site and the
sampler chooses a letter.  With the adversary restricted to the distance functions `s₁(·,b)`
this is `R^rand_β` of Theorem 11.24.  (The Lean file proves the two ingredients for `n`-fold
products encoded as nested pairs; their combination with (b) is the paper step.)

*Consequences.*  (i) For a **two-state site** the polytope is a segment whose endpoints are the
two distance functions: `R^gen_β = R^rand_β`.  (ii) For **three or more states** the polytope has
further vertices — for the Hamming envelope one for every proper nonempty subset `B` of states,
`c·1[a ∉ B]`, whose generalised dip is *centred at the box* `∏ B_i` — and they can win.  On the
flat `k`-state site (`π` uniform, `u = βc`)

    R^gen_β(ε₁) = max_{1 ≤ m < k} D(ρ_m ‖ 1 − m/k)₊,        ρ_m = [ε₁ − ln(m/k + (1 − m/k)e^{−u})]/u

(`D` the binary relative entropy; `m = 1` are the single dips): for `k = 4`, `u = 1`, `ε₁ = 0` it
is `0.02914` (boxes of pairs) against `0.02841` (dips); for `k = 8`: `0.0309` against `0.0194`; three
states suffice (energies `(0,0,2)`, `β = c = 1`: `0.0290` against `0.0247`); for flat sites with `k`
even the ratio tends to `k²/(4(k−1))` as `u → 0` (each term is `≈ u²θ(1−θ)/8`, `θ = m/k`).  **So the conjecture of the previous revision — single dips are
extremal at the exponential scale on product landscapes — fails in general for sites with three
or more states** (independent workstream A; `DEAD_ENDS.md` D38; harness `DEAD.16`, XII.9, XII.11; benchmark B11, which also gives exact
binomial tails at `n = 20000`).  The flat three-state site is not a counterexample, and
numerically the gap closes as `β → ∞`: at zero temperature a sensitive perturbation contains a
sensitive single dip, which is why the zero-temperature theory is a covering theory.

*`R^gen_β` is the exponent* **[P; proof checked by an independent referee, not machine-checked]**
(workstream A, Theorem A; `reviews/R4_referee_report.md`).  For identical sites, an additive
instance, `ε_n/n → ε₁` and `ln(1/ε_n) = o(n)`, the sampler
`½πⁿ + ½·(uniform mixture over the type classes)` hits every sensitive set with probability
`e^{−nR^gen − o(n)}`; with the hedged spot-check of Theorem 11.22(e) the least expected number of
evaluations at the instance is therefore `exp(nR^gen_β(ε₁) + o(n))` — with the instance as a
hint, or after `n(k−1)+1` further evaluations on a star.  The proof is the method of inherently
typical subsets (a variant of the lemma of Ahlswede–Yang–Zhang, proved in the workstream
report) and of Ahlswede–Zhang and Yu for the isoperimetric exponent of two fixed product
measures, with the reference law chosen after the set; the referee re-derived every step,
found no gap (two terse passages around Sion's theorem, repaired in its report), and confirmed
the two finite-`n` identities and the single-letter optimisation with independent code.  What
is new is not the isoperimetric statement — used as a black box with a reference law that
depends on the measure exponent of the set, the fixed-measure theorem gives a bound that
coincides numerically with `R^gen_β` on the biased binary examples the referee computed — but its
evaluation as a matrix game over the Lipschitz vertices (which uses that for `t ≤ β` a maximum
over the Lipschitz polytope is attained at a vertex), the lower bound for every `n`, and the
application.  Consequences: single dips *are* extremal at the exponential scale for two-state
sites, so the values of `R^rand_β` quoted after Theorem 11.24 are exact exponents; no product
sampler attains the exponent on a biased site (`0.1655` against `0.1541` for `e/c = 1/2`, `β = 4`);
on flat sites the crossover below which boxes beat dips is `u_c(k) = ln C(k−1, 2)`, and the ratio
of the exponents tends to `(k+1)/4` for odd `k`.  The statement needs every one of its
hypotheses: identical sites, an additive instance, an accuracy that is not exponentially small,
a fixed error probability, and the hedge.

**Theorem 11.28 (the two-reference sandwich, and thresholds beyond the cube) [V core; P].**
(a) **[V]** *Tensorisation with two measures* (`twoMeasureBound_prod`, `twoMeasureBound_pow`).
Suppose that for one site, a reference law `Q` and a constant `γ`, every profile `h` with
`h(b) − h(a) ≤ s₁(a,b)` satisfies `E_π e^{βh} ≤ exp(β E_Q h + γ)`.  Then on `n` sites every profile
with `h(y) − h(x) ≤ Σ_i s₁(x_i, y_i)` satisfies

    ln E_{πⁿ} e^{βh}  ≤  β E_{Qⁿ} h + nγ

(condition on the last coordinate and apply the hypothesis to the `Q`-averaged profile).  The
least constant of a site is `γ(Q) = max_φ [β E_Q φ − Λ(φ)]`, the maximum over its Lipschitz
polytope, attained at a vertex because the functional is convex **[P]**.  In terms of
residuals: for every admissible `g'`,
`β E_{πⁿ}[g − g'] ≤ ln Z(f+g') − ln Z(f+g) ≤ β E_{Qⁿ}[g − g'] + nγ(Q)`.  With `Q = π` this is the
passive sandwich with its exact constant, the Jensen width `W₁ = γ(π)` (Theorem 11.21 has the
bound `β²c²/8` for it).
(b) **[V]** *Hitting* (`mass_ge_of_twoMeasureBound`, `product_mass_ge`).  A set `D` that supports a
profile `0 ≤ h ≤ H` with `ln E_{πⁿ} e^{βh} ≥ ε` has `Qⁿ(D) ≥ (ε − nγ)/(βH)`.  With `H = n s_max` and
`ε = nε₁`: at least `(ε₁ − γ)/(β s_max)`, whatever `n`.
(c) **[P]** *The threshold of an additive instance, for every alphabet and every `n`.*  Let
`ε₁^thr = min_Q γ(Q)`, attained at `Q*`.  If `ε₁ > ε₁^thr`, the hedged spot-check of Theorem 11.22(e)
with samples from `½πⁿ + ½Q*ⁿ` and output `ln Z(g) + ε/2 − η` is `(ε/2, δ)`-correct on the whole
class with

    N = ⌈ ln(1/δ) / p ⌉,        p = ½ min( (ε₁ − η/n − ε₁^thr)/(β s_max), 1 − e^{−η} )

samples — a number that does not grow with `n` (an alternative `g'` that raises `ln Z` by more
than `ε − η` either differs from `g` everywhere or, by (b) applied to the positive part of
`g − g'`, which is again an admissible profile and is bounded by `n s_max`, on a set of
`Q*ⁿ`-mass at least `(ε₁ − η/n − ε₁^thr)/(β s_max)`; one that lowers it by more than `η` differs on
Gibbs mass at least `1 − e^{−η}`).  If `ε₁ < ε₁^thr`, every algorithm makes at least `(1 − 2δ) e^{nR^gen_β(ε₁)}`
evaluations and `R^gen_β(ε₁) > 0` (Theorem 11.27(c): `−ln val(K_t)/t → ε₁^thr/β` as `t ↓ 0`).  On
additive instances the hint can be learned from a star, as in "Without a hint" above.  The
dip value `ε₁^crit = max_P min_a E_P[βs₁(a,·) − Λ₁]` of the previous revision is the same game
restricted to distance functions: `ε₁^crit ≤ ε₁^thr ≤ W₁`, with `ε₁^crit = ε₁^thr` for two-state sites
and, e.g., `0.0947 < 0.1197` for the three-state site `(0,0,2)`, `0.1074 < 0.1201` for the flat
four-state site (`β = c = 1`).  Between the two values the previous revision's conjecture
predicted polynomial cost; the cost is exponential.
(d) **[V inequality; P]** *No hint, any alphabet: one reference law.*  For a site with known part
`f₁` and envelope `d₁` let `𝓛 = {ψ : ψ(a) − ψ(b) ≤ d₁(a,b)}` be its admissible site functions and,
for a law `Q` on the site,

    F_Q(ψ) = ln Σ_a e^{−β(f₁(a) + ψ(a))} + β E_Q ψ        (the tilted site pressure: convex in ψ, affine in Q),
    M(Q) = max_𝓛 F_Q,        m(Q) = min_𝓛 F_Q.

Then **every** admissible residual `g` on `Sⁿ`, additive or not, satisfies

    n m(Q)  ≤  ln Z(f+g) + β E_{Qⁿ} g  ≤  n M(Q)

(`product_sandwich`: the upper bound is (a) with the envelope `d₁` in place of the slack, the
weights `e^{−βf₁}` in place of `π`, and `h = −g`; the lower bound is its mirror image, which
tensorises by the same argument, `twoMeasureLower_pow`).  No
reference instance occurs.  So an algorithm that samples `Qⁿ`, estimates the mean of `g`
(bounded differences; Hoeffding) and returns the midpoint is `(ε/2, δ)`-correct on the whole
class with a number of evaluations independent of `n` as soon as `ε₁ > M(Q) − m(Q)`
(`N ≥ 2β² d_max² ln(2/δ) / (n (ε₁ − M(Q) + m(Q))²)` samples).  Let

    ε₁* = min_Q [ M(Q) − m(Q) ]

(the smallest oscillation of the tilted site pressure over the class; a convex minimisation).
Conversely, with `ψ = φ + γ` the threshold of (c) at the additive instance `γ` reads
`ε₁^thr(γ) = min_Q [M(Q) − F_Q(γ)]`, and since `M(Q) − F_Q(γ)` is convex in `Q` and concave in `γ` on
compact convex sets, the minimax theorem gives

    sup_{γ ∈ 𝓛} ε₁^thr(γ)  =  min_Q [ M(Q) − m(Q) ]  =  ε₁*.

Hence below `ε₁*` every algorithm, with or without a hint, needs exponentially many evaluations
at some additive instance, and above it a bounded number suffices on every instance without
any hint: **`ε₁*` is the worst-case accuracy threshold of the class, for every alphabet.**  It
never exceeds the passive width at a reference instance (for `Q = π_γ`, `γ ∈ 𝓛`, the Gibbs
variational principle gives `m(Q) = F_Q(γ)`, and `M(Q) − m(Q)` is the Jensen width `W₁(γ)`), and
equals the smallest of them when the optimal `Q*` is the Gibbs law of a member of the class.
Three-state site `(0,0,2)`, `β = c = 1`: `ε₁^thr(0) = 0.11969 < ε₁* = 0.11988 < W₁(0) = 0.12208`
(harness XII.13, which also tests the sandwich on small products with random quasi-metric
envelopes and the minimax identity; benchmark B11).  The lower end `n m(Q)` is what makes one
reference law enough: pairing the Jensen bound under `π` with the upper bound under `Q` would
cost a transport term `β(E_π − E_Q)g`, which is why a second reference seemed useless without a
hint (a remark of workstream D that this statement corrects).
*Two remarks on scope* **[P]**.  (i) Nothing in the sandwich and in the minimax identity uses
the product structure: on any finite instance class, with `F_Q(ψ) = ln Z(f+ψ) + βE_Qψ` on the
whole space, `min_Q [max F_Q − min F_Q] = sup_γ min_Q max_ψ [F_Q(ψ) − F_Q(γ)]`, and above that width
(plus a margin `Δ`) `O(β² D² ln(1/δ)/Δ²)` samples of the optimal reference suffice, `D` the
diameter of the envelope.  What the product structure adds is that the optimal reference is a
product law, that the width is `n` times a single-site quantity, and that the cost below the
threshold is exponential.  (ii) For sites of finitely many types the sandwich tensorises site
by site, and the lower bound of Theorem 11.27(c) holds with a common `t` and the product of the
site constants; since every `−ln val(K_t^{(j)})` is linear at `t = 0`, the threshold of the class
is the average `Σ_j λ_j ε₁*^{(j)}` of the site thresholds over the type frequencies `λ_j` (unlike
the exponents, which do not add up site by site, D31).  The Lean file treats identical sites.
(iii) Dividing by `β` and letting `β → ∞` gives the same sandwich for the minimum:
`n m₀(Q) ≤ E_{Qⁿ} g − min(f+g) ≤ n M₀(Q)` with the extreme values of `E_Q ψ − min(f₁ + ψ)` over the
class.  For a two-state site with excitation energy `e` the smallest width is
`(c² − e²)₊/(2c)` per site: it vanishes exactly when the site is sharp (`e ≥ c`), which is the
dichotomy of Theorem 11.8 seen from the side of extensive accuracies, and `ε₁*/β` tends to this
value (`0.254, 0.361, 0.374` at `β = 4, 40, 400` for `e/c = 1/2`, limit `0.375`).
(e) **[P]** *Two-state sites: the largest chord gap of the pressure* (workstream B, Theorem B.12;
proof checked for this revision).  Let `f = e·M` on `{0,1}ⁿ` (`M` the number of excited sites)
with the class of `c`-Hamming-Lipschitz residuals, and let `P(θ) = ln(1 + e^{−β(e+θ)})` be the
pressure of the additive instance `θM`, `|θ| ≤ c`.  Then (d) is explicit:

    ε₁^thr(θM) = G(θ) := [(c+θ) P(c) + (c−θ) P(−c)]/(2c) − P(θ)        (the chord gap of `P` over `[−c, c]`),
    ε₁* = max_θ G(θ) = G(θ*),        P′(θ*) = [P(c) − P(−c)]/(2c),

the optimal reference is the Gibbs law `π_{θ*}` of the tilted instance, and the sandwich is
`0 ≤ ln Z(f+g) − [ln Z(f + θ*M) − β E_{π_{θ*}}(g − θ*M)] ≤ n ε₁*` (the Jensen gap of one site is convex
in the increment of `g − θ*M`, which lies in `[−c − θ*, c − θ*]`, and its two endpoint values are
the Bregman divergences `P(±c) − P(θ*) ∓ (c ∓ θ*)P′(θ*)`, both equal to `G(θ*)` because the tangent
at `θ*` is parallel to the chord).  For `e = 0` this is Theorem 11.25 (`θ* = 0`,
`ε₁* = ln cosh(u/2)`).  For `e ≠ 0` the hardest instance is not the zero residual and the best
reference is not the Gibbs measure of the known part: for `e/c = 1/2`, `β = 1`, `G(0) = 0.11367`,
the untilted width is `0.12246`, and `ε₁* = 0.11383` at `θ* = −0.037c` (harness XII.12; benchmark
B11).

So the picture of Theorem 11.25 extends beyond the cube, to every product landscape of
identical sites.  At an additive instance there is a sharp accuracy threshold, the value
`ε₁^thr` of a single-site game, between bounded and exponential cost for algorithms that know
the instance or can learn it.  For the class as a whole, and for algorithms that are given
nothing, the threshold is `ε₁* = sup_γ ε₁^thr(γ)`, the smallest oscillation of the tilted site
pressure; on the uniform cube both are `ln cosh(βc/2)`, the largest Jensen gap, and in general
`ε₁*` lies strictly below the passive width of the known part.  What the thresholds do not give
is the cost below them (Theorem 11.27 and the claim after it), and nothing is said here about
sites of several types or known parts with interactions.

*What is not proved.*  The exact randomised exponent beyond the cube at the zero residual
(Theorem 11.27 gives the lower bound `R^gen_β`; the matching upper bound is the unrefereed claim
above; the bracket `R^gen_β ≤ · ≤ min(R_β, U_β)` is what is established).  Thresholds and
exponents are statements about one instance; they need accuracies that are not exponentially
small and a hedged converse (Theorem 11.25).  Sites of several types, non-additive instances
and interacting known parts are not covered.  The model of randomness (finite mixtures of
deterministic algorithms) and of correctness (probability `1 − δ` on every instance, not on
average) are those of the theorems.  Harness XII.1–XII.12.

*Prior art* (`prior_art/L7`; the third referee's reading of the primary sources is recorded
there).  For deterministic certified algorithms on `ℝ^d` the necessity half of Theorem 11.23(a)
is the lower bound of Bachoc–Cesari–Gerchinovitz (2021), and the sufficiency half is the "best
possible algorithm" of Hansen–Jaumard–Lu (1991); the notion itself — the cost of the best
algorithm that is correct everywhere and is charged on one instance, for which it may be
tailored — is *instance complexity* (Grossman–Komargodski–Naor 2020, for Boolean decision
trees, deterministic and randomised), and Theorem 11.23(a) is its real-valued restatement.
Bachoc–Cesari–Gerchinovitz treat deterministic certification only and name certification with
a prescribed probability as an open direction; Theorem 11.23(b,c) is an answer in the finite
quasi-metric setting with exact evaluations.  That randomisation does not improve worst-case
rates for global optimisation over Lipschitz classes is classical (Nemirovski–Yudin 1983; Novak
1988; quoted as Theorem 7 in Holzmüller–Bach 2025).  For the free energy the closest work is
Holzmüller–Bach (JMLR 2025, §2.2), for smoothness classes on `[0,1]^d` in the worst case: with
stochastic evaluation points the log-partition problem has an *optimisation regime*, in which
the deterministic rate cannot be improved (by reduction to optimisation), and a *quadrature
regime*, in which Monte Carlo gains; their lower bounds also hide a bump where the algorithm
does not look, and a lower bound for stochastic algorithms outside the optimisation regime is
stated there as open.  So the qualitative phenomenon — randomisation helps for `ln Z` only
above an accuracy scale — is in print.  Lower bounds for estimating normalising constants
through hidden local perturbations also appear in Ge–Lee–Lu (2020) for log-concave densities
(polynomial in the dimension).  What we did not find: the instance-wise randomised bound with
gap radii and its hedged converse, the soft-gap radius, the three budgets, and the exact
threshold and accuracy diagram of Theorem 11.25 (the corner of the Holzmüller–Bach picture in
which the dimension grows and no approximation of the residual is affordable).  The proofs are
short.

### 11.11 A normal form: the known part is the gradient part of an asymmetric envelope

Found by workstream C and confirmed in full by its independent reviewer (`workstreams/C_REPORT.md`,
Theorem C1; `reviews/R_C_review.md`: all parts re-derived, exhaustive exact tests on 5100
instances and 216 300 evaluated sets).

**Theorem 11.29 (normal form) [V] (`NormalForm.lean`).**  For a potential `φ` let
`d^φ(a,y) = d(a,y) + φ(a) − φ(y)` be the *reduced cost* of the envelope (Johnson reweighting).
(a) *Gauge.*  `d^φ` is an envelope, `g` is admissible for `d` iff `φ + g` is admissible for `d^φ`,
and the slack and both McShane envelopes are gauge covariant (`reduce_isEnvelope`,
`admissible_reduce_iff`, `slack_reduce`, `lowerEnv_reduce`, `upperEnv_reduce`).
(b) *Regularisation.*  Let `f^d(y) = min_x [f(x) + d(x,y)]` be the Pasch–Hausdorff envelope of
the known part (§2.3).  Then `min(f + g') = min(f^d + g')` for **every** admissible `g'`
(`inf_add_phEnv_eq`), and `σ := d^{f^d} ≥ 0` is a quasi-metric (`reduce_phEnv_nonneg`).
(c) *Certificates.*  Put `E^d = f^d + g`.  For every evaluated set `A` the certified lower bound
of `(d, f, g)` is the certified lower bound of the instance `(σ, 0, E^d)` without known part, and
its value upper bound `min(f + U_A)` is both the value upper bound and the *incumbent*
`min_A E^d` of that instance (`certLB_normalForm`, `valueUB_normalForm`, `certUB_normalForm`).
Hence

    A is a value ε-certificate of (d, f, g)   ⟺   A is a point ε-certificate of (σ, 0, E^d)

(`isValueCertificate_iff_normalForm`), and in normal form value and point certificates coincide
(`isValueCertificate_normalForm_iff`).
(d) *Centre form.*  With `gap^d = E^d − E*`: `s(a,y) − gap^d(y) = σ(a,y) − gap^d(a)`
(`client_eq_centre`), so the covering relation can be read with the radius attached to the
evaluated point, `σ(a,y) ≤ gap^d(a) + ε`; and `gap^d` is 1-Lipschitz for the slack
(`gap_slack_lipschitz`), which the gap of the original instance is not.

So an instance with a known part *is* an instance without one, in an envelope whose
antisymmetric part is the gradient of the regularised known part: for symmetric `d`,
`σ(a,y) − σ(y,a) = 2(f^d(a) − f^d(y))`.  In the framework of this report, whose envelopes are not
assumed symmetric, "`f ≡ 0`" is without loss of generality for minima and for certificates (not
for free energies: `ln Z` is not invariant under the regularisation).  The mathematics is
elementary — Johnson's reweighting and the adjointness `min(f⊗d + g) = min(f + d⊗g)` of the
min-plus product, with `d⊗g = g` on the class — and the object has a name, which the first
version of this section did not give (science division, `SCI-REV-0006` W5): for symmetric `d`,
`σ(a,y) + w(a) = σ(y,a) + w(y)` with `w = −2f^d`, that is, `σ` is a *weightable quasi-metric* with
weight `−2f^d` (Matthews; Künzi–Vajner 1994; the linear correspondence with weighted semimetrics
and with partial metrics is in Deza–Deza–Vidali 2011), and the condition that makes `σ ≥ 0` is
"`f^d` is 1-Lipschitz for `d`".  Certification with a symmetric envelope and a known part is
certification without a known part on a weightable quasi-metric space.  What was not found in
that literature is the certificate statement itself (`isValueCertificate_iff_normalForm`); the
reviewer of workstream C had judged the packaging new for this problem.  Harness XI.14 (all evaluated sets of random instances, including asymmetric envelopes
and known parts that are far from Lipschitz).

**Proposition 11.30 (best-first search in centre form) [P; separation lemma V].**  (Workstream C,
Theorem C4, with the scope found by its reviewer.)  Suppose the reduced envelope is
quasi-symmetric, `σ(x,y) ≤ ρ σ(y,x)` for all `x, y` — which forces `f = f^d` (no state is dominated
in the known part) and, for symmetric `d`, `f` Lipschitz with constant `(ρ−1)/(ρ+1) < 1`.  Then
for **every** admissible residual, also at `κ = 1`, where Theorem 11.11 says nothing, best-first
search makes at most `|C|` evaluations for every set `C` such that

    ∀y ∃c ∈ C:   σ(c, y) ≤ θ (gap^d(c) + ε),        θ = 1/(2ρ+3)

(two evaluated points cannot share a centre: `not_cocovered_centre`).  For `f ≡ 0` and symmetric
`d` these are the balls `B(c, (gap(c) + ε)/5)`; this case is the packing argument known for
Piyavskii–Shubert search (Bouttier et al.; Bachoc et al.), and for `κ ≥ 1/3` it implies Theorem
11.11 without its `+1`.  The constant is nearly tight (violations at `1.2θ` under adversarial
tie-breaking, none found at `1.1θ`).  The hypothesis fails as soon as one state is dominated in
the known part — one sharp site of a product, one dead-end-elimination pair — and then only
Theorem 11.11 is available.

*What search cannot do, even on the line* (`DEAD_ENDS.md` D39; harness `DEAD.17`).  With `f ≡ 0`
on an interval, Hansen–Jaumard–Lu's theorem bounds Piyavskii–Shubert search by `4n_B + 1`.  With
a known part there is no such bound.  Points `x* = −D`, a hub `c = 0`, a grid to the right of the
hub, `f(x*) = 0`, `f(0) = G`, `f(t) = G + (1−η)t`, zero residual: `{x*, c}` is a certificate, and
best-first search makes `4, 5, 6, 6, 7, 8` evaluations for `η = 0.2, …, 0.00625` and `11` at
`η = 1/1280` — the lower bound is lowest at the far end, and the search halves its distance to
the hub at each step.  With the extremal residual `g = −|x|` (and one further point, so that the
conclusion does not depend on the starting rule) it makes `9, 16, 29, 55, 107, 212` evaluations
against a certificate of three points, about `1.3/η`.  These growth laws are computed, not
proved.  In the Dechter–Pearl classification of best-first strategies the situation is that of
an admissible but inconsistent heuristic: best-first search started at a centre of the reduced
envelope, with the value stopping rule, is not strictly dominated by any sequential correct
algorithm (their "type 3"), no algorithm is optimal in the stronger "type 2" sense, and
neither notion bounds the number of evaluations (workstream C, Theorem C3; the plain
best-first search of Theorem 11.11 *can* be strictly dominated).

*Prior art for §§11.2–11.5 found by this workstream.*  Hetland (2020), "Optimal metric search is
equivalent to the minimum dominating set problem": for metric range search — symmetric `d`, no
known part, exact queries — it has the dominating-set characterisation of the smallest query
set, the 0/1/2-distance gadget of Theorem 11.10 with `(1−ε) ln n` inapproximability, and an
informal adversary argument for Theorem 11.23(a).  Not there: the exchange lemma and the `+1`
of Theorem 11.5, the accuracy `ε`, a known part, asymmetric envelopes, and everything at finite
temperature.  The lower McShane envelope is the landmark (ALT) heuristic of Goldberg–Harrelson
and best-first search is AESA (Vidal) with the maximum in place of the sum.

### 11.12 Dense second-order classes: a quadratic law, and its price

§11.7 showed that under a second-order envelope one star of evaluations reduces certification
to a pairwise problem, and that with dense constants the remainder is quadratic in the Hamming
distance (D32); §12 asked whether the cost is then exponential.  It is.  Found by workstream E
and confirmed by its reviewer (`workstreams/E_REPORT.md`; `reviews/R_E_review.md`: every theorem
re-derived, linear programmes over the whole class for `n ≤ 6`, 40 050 850 simplices
re-enumerated for `n = 6`); workstream D found the same droplets independently.

Let `X = {0,1}ⁿ` (the statements hold for `k`-state sites), let the class consist of the residuals
whose mixed second differences are bounded by a dense constant `c`, and for an evaluated set
`A` let `w_A(y)` be the largest value at `y` of a class member that vanishes on `A`: the
uncertainty that remains at `y`.

**Theorem 11.31 (second-order dips; stars do not combine) [V] (`SecondOrderDip.lean`).**
(a) The function `b_{y,r}(x) = c·C(r − d_H(x,y), 2)₊` belongs to the class, equals `c·C(r, 2)` at `y`
and vanishes outside the Hamming ball `B(y, r−2)` (`dip_mixedDiffBound`, `dip_center`,
`dip_eq_zero`).  Hence for **every** evaluated set and every `y`

    w_A(y)  ≥  c·C(d_H(y, A) + 1, 2)

(`dip_witness`): every unevaluated point keeps an uncertainty of at least `c`, and the
uncertainty grows quadratically with the distance to the evaluated set, whatever was evaluated.
(b) If `A` is a union of stars with centres `A₀`, then `w_A(y) = c·C(d_H(y, A₀), 2)` exactly
(`star_upper`, `stars_do_not_combine`): several stars give the best single-star bound and
nothing more — information from different stars combines by a minimum, as in the first-order
class.

**Theorem 11.32 (the cost of dense second-order classes) [P; counts verified numerically].**
Let the true residual be additive, `f` arbitrary, and let `N₂` be the least number of evaluations
that certify the minimum within `ε`.  With `ρ₋(y) = max{d : c·C(d+1, 2) ≤ gap(y) + ε}`,
`ρ₊ = ρ₋ + 1`, and `K_∓` the least size of a code that covers every `y` within Hamming distance
`ρ_∓(y)`:

    K₋  ≤  N₂  ≤  (n+1) K₊ + 1  ≤  (n+1) K₋ + 1

(lower bound: Theorem 11.31(a); upper bound: stars at the code points and one minimiser), and
every randomised algorithm pays `(1 − 2δ)` times the fractional packing bound of the balls
`B(y, ρ₋(y))` (Theorem 11.22(c) applied to the dips).  So the covering radius
`(2·gap/c)^{1/2}` conjectured in §12 is exactly right, and no choice of evaluation set — covering
arrays, random sets, codes — escapes the quadratic law.  For `f = e|x|` and zero residual:
(i) *Constants of order one* (`e/c` fixed): `log₂ N₂ = n − Θ(√n log n)`.  The exponent is full;
second-order information saves only a factor `2^{Θ(√n log n)}`.
(ii) *Mean-field constants* `c = γ/n`, `λ = e/γ`, `ε = o(n)`:

    lim n⁻¹ ln N₂ = R₂(λ) := max { h(ω) − h(√(2λω)) : √(2λω) ≤ min(ω, 1−ω) },

positive iff `λ < 1/4` (`0.295, 0.078, 0.007` at `λ = 0.02, 0.1, 0.2`) — the rate–distortion
formula of Theorem 11.9 with a square-root budget; for `λ ≥ 1/4` two opposite stars (`2n+2`
evaluations) certify.  For bounded mixed differences of order `m` the same holds with
`(m! λω)^{1/m}` and the threshold `λ ≥ 2^{1−m}/m!`; `m = 1` is Theorem 11.9.
(iii) *Which `n+1` evaluations?*  Not the star: a balanced three-legged *spider* (three nested
chains from the reference configuration) certifies iff `e ≥ c·n/3`, the star only for
`e ≥ c(n−1)/2`; `n/3` is optimal among tree-shaped simplices, and conjecturally among all
(exhaustive for `n ≤ 6`).
(iv) *Recovery.*  With polynomially many evaluations the residual is known in sup norm only to
within `(1 − o(1))·c·n²/8`: a factor four better than one star (two opposite stars), and no more.
(v) *Sparse constants.*  The class is finite-dimensional, spanned by the monomials of the
cliques of the coupling graph: the cost is at most the number of cliques and at least
exponential in the clique number, and one star certifies under a maximum-density condition
that is weaker than the row-sum condition of §11.7.

Limits of these statements (reviewer): `N₂` is a certificate size, which equals the cost of the
best instance-tailored algorithm only up to `+1`; the randomised statement is the fractional
bound, not an exponent; the asymptotics (i), (ii) are paper proofs by type covering, checked by
exact layer counts up to `n = 2000`.  Prior art: for a one-sided local second-order class
("approximate modularity") Chierichetti–Dasgupta–Kumar have the `Θ(εn²)` law with the same
quadratic witness; the covering sandwich, the non-combination of stars and the spider were not
found there (their reviewer read that literature through summaries only).  Harness XI.15;
whether second-order structure changes the picture for free energies is the subject of
workstream D (a transition at the Curie–Weiss coupling `βcn = 4`), which is under review.

### 11.13 Free energies beyond first-order product classes

Three results of workstream D, each re-derived by its independent reviewer, who completed two
proof sketches and reproduced every table (`workstreams/D_REPORT.md`, Theorems 13, 6 and 12;
`reviews/R_D_review.md`).  They are paper proofs; the only machine-checked ingredient is the
droplet of Theorem 11.31.

**Theorem 11.33 (second-order classes at finite temperature: a transition at the Curie–Weiss
coupling) [P].**  Let `𝒢₂(c₂)` be the residuals on `{0,1}ⁿ` whose mixed second differences are
bounded by `c₂`, and `w = βc₂n`.
(a) *`w ≤ 4`: polynomially many evaluations, at every accuracy.*  Dobrushin's uniqueness
condition holds for every member of the class and along the whole annealing path (the
influence of one site on another is at most `tanh(βc₂/4)`, so the Dobrushin constant is at most
`1 − 1/n`).  Hence: evaluate a star, form the additive interpolant, anneal from it to the
residual in `⌈wn⌉` steps, sample each step by heat-bath Glauber dynamics (one evaluation per
update) — the output is within `ε/2` of `ln Z` with probability `1 − δ` on the whole class, with a
number of evaluations polynomial in `n`, `1/ε` and `ln(1/δ)` (about `n⁵ε^{−2}` at `w = 4`).  No hint
is needed.
(b) *`w > 4`: exponentially many for every algorithm.*  For `f ≡ 0` at the zero residual the
droplets of Theorem 11.31, `−c₂·C(r + 1 − d_H(x,y), 2)₊`, multiply `Z` by
`2^{−n} Σ_k C(n,k) e^{βc₂ C(r+1−k, 2)}`; if this exceeds `e^ε`, every algorithm makes at least
`(1 − 2δ) 2ⁿ/|B(r−1)|` evaluations.  With `r = ρn` the exponent of the ratio at `ρ = 1/2` is the
Curie–Weiss free energy `f_CW(w) = max_m [wm²/8 − I(m)]`, which is positive iff `w > 4`: for
`w > 4` and every accuracy per site below `f_CW(w)` the cost is exponential in `n`.
(c) With a first-order bound `c₁` as well, (a) is unchanged, and in (b) the threshold
`max_x [∫₀^x min(βc₁, ws) ds − (ln 2 − h(½ − x))]` vanishes iff `w ≤ 4` and increases to the
first-order threshold `ln cosh(βc₁/2)` of Theorem 11.25 as `w → ∞`.

So for free energies second-order structure does rescue certification, but only in the
high-temperature phase of the *class*: the boundary is the critical coupling of the mean-field
ferromagnet, the worst member of the class.  Compare Theorem 11.32 for the minimum, where the
boundary is at excitation energies of order `c·n`.  Scope (reviewer): (b) is asymptotic at
fixed `w` — at `w = 5` the bound is only `e^{3.9}` for `n = 2000`; the bookkeeping of (a) was a sketch
that the reviewer completed.

**Theorem 11.34 (a continuous space: the torus of torsion angles) [P].**  Let
`X = (ℝ/2πℤ)ⁿ` with the uniform reference, `f ≡ 0`, and the class of residuals with
`|g(x) − g(y)| ≤ Σ_i L_i |x_i − y_i|` (geodesic distance on each circle); `b_i = βL_iπ/2`.  The
largest Jensen gap of one site is `ln(sinh b_i/b_i)`, attained by the tent function, and
(a) for `ε > J := Σ_i ln(sinh b_i/b_i)`, `⌈8 Σ_i b_i² ln(2/δ)/(ε − J)²⌉` uniform random evaluations
give `ln Z` within `ε/2` with probability `1 − δ` on the whole class;
(b) for `ε < J` every algorithm satisfies, at every constant residual,
`ln E|Q| ≥ ln(1−2δ) + sup_{λ ≥ 0} [Σ_i Λ₁(λb_i) − λ(Σ_i Λ₁(b_i) + ε)]`, `Λ₁(b) = ln(2b/(1 − e^{−2b}))`, which
is exponential in `n` for extensive accuracy below the mean of `ln(sinh b_i/b_i)`.
This is Theorem 11.25 with the circle in place of the two-point space — the sites are
homogeneous, so the Gibbs law of the known part is the optimal reference of Theorem 11.28(d)
— and it is the form of the threshold that applies to torsion-angle coordinates.  In fixed
dimension the cost is of the known order `(βL/ln βL)^d` (Holzmüller–Bach); with one global
`ℓ₂` Lipschitz constant instead of per-coordinate ones the cost is dimension-free.

**Theorem 11.35 (Boltzmann averages are harder than free energies) [P].**  On the cube with
`f ≡ 0`, envelope `c·`Hamming and `u = βc`, let an algorithm return the mean magnetisation
`⟨|x|/n⟩` within `η` with probability `1 − δ` on the whole class.  Over the class the average
ranges over an interval of half-width `H(u) = ½ tanh(u/2)`.  Every algorithm needs exponentially
many evaluations at the zero residual for `η < ε_set(u)`, where `ε_set/H` rises from `1/√2` at
small `u` to `0.87` at `u = 8`: almost the whole a-priori range is uncertifiable, whereas for
`ln Z` the uncertifiable fraction of the a-priori width is `ln cosh(u/2)/(u/2)`, which tends to
zero at high temperature.  The extremal perturbations are generalised dips centred on *type
classes* (Theorem 11.27 with `Φ` the slack distance to a set of configurations with prescribed
magnetisations on two halves of the sites); single dips give only `O(u²)`, so they are not
extremal for this observable even on the binary cube.  A bounded number of samples suffices,
with the instance as a hint, above a level within one per cent of `ε_set` for `u ≥ 6`; at weak
coupling the interval between `H/√2` and `H` is open.

Smaller statements of the same report, also confirmed: free-energy differences between
uncoupled macrostates have the sum of the two thresholds (no cancellation); certifying a
ranking is cheap iff the margin exceeds the threshold of the loser; the quantity
`E_π e^{Λ}` that governs the soft-gap sampler does not depend on the residual (workstream G;
`sum_gibbs_exp_softGap_indep`, `spotCheck_const_le_cover` in `SoftGapIndependence.lean`).  One
heading of the report, "staged protocols cannot help on the first-order class", claims more
than its argument proves (staged protocols obey the lower bounds), and its remark on
hint-free procedures is corrected by Theorem 11.28(d).

### 11.14 What the theory says about chains: envelopes from torsion-space geometry

The program started from articulated chains (§4.4: a verified bound "changing torsion `i`
changes the superposition RMSD by at most `c_i`", which turns an RMSD-Lipschitz residual into a
weighted-Hamming envelope `Σ_i c_i [x_i ≠ y_i]`).  Workstream G asked what §§11.4–11.10 then
predict (`workstreams/G_REPORT.md`; `reviews/R_G_review.md`: no critical error, constants and
scope corrected as stated below).  Setting: `n` torsions with `k` rotamers each, `N = n + 3`
atoms, bond length `b`, a residual that is `L`-Lipschitz in RMSD, `m_i = min(i, n+1−i)`.  The
product-domain statements ignore excluded volume.

**Theorem 11.36 (lever-arm law) [P for the verified constants; the constant of the smallest valid ones numerical].**
The verified constants of Theorem 4.6, taken uniformly over the rotamer domain, are
`c_i^ver = 2Λ sin(δ/2)√(Ī(m_i))` (`Λ = L/√N`; `δ` the largest rotamer change; `Ī(m)` the largest
moment of inertia of an arm of `m` atoms about the torsion axis), and with `θ` the bond angle

    Ī(m) = ⅓ sin²(θ/2) b² m³ (1 + O(1/m)),        c_i^ver / (Λ b m_i^{3/2})  →  (2/√3) sin(δ/2) sin(θ/2).

The limit is `0.824` for `θ = 111°`, `δ = 120°`, and the ratio decreases to it, so
`c_i^ver ≥ 0.824·Λ b m_i^{3/2}` at every position; it is `2√2/3 = 0.943` for the tetrahedral angle
and `δ = 180°`.  (Upper bound: the distance of an atom from the axis is at most its distance
from the axis atom, and atoms two bonds apart are at the fixed distance `2b sin(θ/2)`; attained
asymptotically by an arm that is all-trans behind one gauche torsion, which is perpendicular
to the axis for the tetrahedral angle.  In the weaker reduced-inertia form `2√(2 I_red)` of
Theorem 4.6(d) the limit is larger by the factor `√2` when the other arm is much longer:
`4/3` in place of `2√2/3`.  Workstream G, §2.1(c)–(d); the science division obtained the two
values independently, `SCI-REV-0006` M4 — our first wording, "`c_i ≥ 0.824…`", hid that this is
an asymptotic equality.)  The smallest constants for which the weighted-Hamming envelope is
valid are at least `0.186·Λ b m_i^{3/2}` (computed for `m ≤ 10⁵`; a proved bound has the same
power with a smaller constant).  The cause is geometric — the moment of inertia of an arm of
`m` atoms about a torsion axis grows like `m³` on every domain that contains extended arms —
and it is not a finding of this report: per-joint lever arms as weights of a weighted-`ℓ¹`
displacement bound are a published certificate in robot motion planning
(Schwarzer–Saha–Latombe 2005, Lemma 2), and the growth of joint-space inertia with the number
of bodies is documented in robotics (Featherstone 2004; both through the science division,
`SCI-REV-0006` W6).  New here are the consequences for certification, Theorems 11.37–11.38.

**Theorem 11.37 (growing constants make the weighted-Hamming format exponential) [P from V].**
If `c_i ≥ c₀ m_i^γ` with `γ > 0`, then for an additive known part with total excitation energy `G`
and zero residual

    ln N_cov(ε)  ≥  n ln k − C_{k,γ} ((G + ε)/c₀)^{1/(1+γ)},

every randomised algorithm pays `(1 − 2δ)` times this, and the same holds for `ln Z` at any
extensive accuracy and fixed temperature (Theorems 11.6, 11.23, 11.24, with one common slope).
With the lever-arm law (`γ = 3/2`) only `O(N^{1/3})` sites near the two ends are sharp at fixed
`L`: **the verified chain-rule route of §4.4 cannot certify long chains.**  It is not rescued by
changing the metric as long as the format is kept: for contact-type residuals every envelope
in torsion-Hamming format has `c_i ≥ u₀⌊(m_i − 1)/2⌋` (a hairpin opened by one torsion changes
`Θ(m_i)` contacts; verified on the diamond lattice).

**Theorem 11.38 (the RMSD envelope used directly) [P; one constant numerical].**  For an
additive known part with excitation energy `e` per torsion, zero residual, and the envelope
`d = L·RMSD` itself (no chain rule), with `λ = Lb/e`:

    c·√(λN)  ≤  ln N_cov(0)  ≤  4.91 √(λN ln(e(k−1)n)) + ln(81(n+1))

(upper bound: a complete proof — cover the configurations with few excitations exactly and the
others by cells of small RMSD diameter; lower bound: a packing of block conformations whose
separation `Δ_s ≈ 0.066 s^{3/2} b` was computed, not proved; the reviewer's grids support
`c ≈ 0.043`).  Every randomised algorithm pays `(1 − 2δ)` times the lower bound.  So at the zero
residual, and for `Lb/e = o(N)`, certification under an RMSD envelope costs a *stretched*
exponential in the chain length, `exp(Θ̃(√N))`, where the weighted-Hamming format costs
`exp(Θ(N))`: at that instance most of the price of the chain-rule route is the `ℓ¹` relaxation,
not the RMSD assumption.  This is a statement about one instance and a wide bracket (at
`n = 1000`, `λ = 1`: between `e^{1.6}` and `e^{235}`), not a claim that chains are certifiable.

Consequences for the architecture (§7, blueprint §7): constants stay bounded only for
residuals that are local along the sequence or expressed in windowed local frames; an
extensive local residual forces `L` of order `N` in RMSD units; second-order structure in
torsion coordinates is dense and growing for tertiary contacts (one contact has interaction
order about `0.6` times the loop length), so §11.12 applies; leaving the product format —
envelopes in the contact-map metric, where sharpness is a condition per contact, or residual
classes that are linear in pair features, which need at most as many evaluations as features
— is where the theory leaves room.

### 11.15 Chains as known parts

Everything in §§11.4–11.10 that has an exponent or a threshold was proved for independent
sites.  Workstream B took a nearest-neighbour chain as known part (`workstreams/B_REPORT.md`;
`reviews/R_B_review.md`: the theorems below were re-derived and their tables reproduced; one
conjecture of the report was refuted).  Envelope `c·`Hamming throughout; `J`, `h` are the coupling
and field of the Ising chain.  Paper proofs; no Lean.

**Theorem 11.39 (one evaluation: the droplet criterion) [P].**  Let `x̂` minimise the known part.
The single evaluation at `x̂` certifies the minimum for every residual iff every *contiguous
droplet* is sharp: for every interval `I` and every `y` that differs from `x̂` exactly on `I`,
`f(y) − f(x̂) ≥ c|I|`; equivalently `c ≤ τ := min_y gap(y)/d_H(x̂, y)`, a minimum cost-to-time
ratio cycle, computable by one min-plus transfer-matrix product.  If `c > τ` the certificate
size grows exponentially, with an explicit base, also for every randomised algorithm (proved at
the zero residual).  For the ferromagnetic Ising chain `τ = 2h` whatever `J`; with a degenerate
or periodic ground state `τ = 0`: at zero field no chain is sharp for any `c > 0`.

**Theorem 11.40 (the exponent for homogeneous chains) [P; checked by a reviewer, no gap found].**
For a homogeneous nearest-neighbour chain, an additive residual with `κ < 1` and `ε_n = o(n)`
(exact certification included),

    lim n⁻¹ ln N_cov(n, ε_n)  =  sup_ν R_ν(e(ν)),

the supremum over stationary processes `ν`, with `e(ν)` the excitation energy per site and `R_ν`
the rate–distortion function of `ν` for the single-site slack; the same limit holds for point
certificates and for the fractional covering number, and `(1 − 2δ)` times it bounds every
randomised algorithm.  This settles the conjecture of §12 item 1(c).  The proof avoids
covering lemmas for Markov types, which that item had identified as the obstacle: block
coding with ordinary type covering, a convexity estimate for the boundary energies, and a
separate treatment of the low-energy shell.

**Proposition 11.41 (the transfer-matrix bound is vacuous on a window) [P].**  For the
ferromagnetic Ising chain with `c > 2h`, the bound `max_t [p(t) − ln(1 + e^{−tc})]` of §12 item
1(c) and of the blueprint — the Shannon lower bound with Boltzmann weights — is positive iff
`c > 2(J + h)`.  On the window `2h < c ≤ 2(J + h)` it is zero although certification is
exponential (Theorem 11.39); it is exact only when `cosh(ct/2) ≥ e^{2Jt} cosh(ht)` at its
optimum — at zero field this is Gray's critical distortion for binary symmetric Markov
sources, so that part is known — and below it the exponent is of the kind of the
rate–distortion function of a Markov source beyond critical distortion, for which no closed
form is known.  "Two-state sites: Boltzmann weights are always optimal" (Theorem 11.8) does not
survive a coupling.  A free block of length 12 gives the two-sided bracket
`0.215 ≤ R* ≤ 0.242` at `c = 4J`, `h = 0` (the Boltzmann bound gives `0.188`).

**Proposition 11.42 (finite temperature on a chain) [P].**  For a site-additive slack the soft
gap is a hidden-Markov log-likelihood: at the zero residual
`Λ(y) = −ln π̃(y) − n ln(1 + (k−1)q)`, `π̃` the law of a Gibbs sample observed through a memoryless
symmetric channel — for the Ising chain, the free-energy cost of a pinning field of magnitude
`c/2` with the signs of `y`, a ratio of two transfer-matrix partition functions.  The dip
threshold at the additive instance `θM` is the chord gap of the chain's pressure in the field,
`G(0) = p(h + c/2)`-type second differences in closed form; it increases from
`ln cosh(βc/2)` at `J = 0` to `βc/2` as `βJ → ∞`.

*What turned out false* (`DEAD_ENDS.md` D41).  The report conjectured that for pairwise binary
references the worst-case Jensen gap over Hamming-Lipschitz residuals is attained by an
additive residual, which would have given the upper half of the threshold for chains and the
exact worst-case free-energy gap of a chain reference (§12 item 5).  Its reviewer refuted it
with explicit instances — an antiferromagnetic complete graph on four sites (`0.99202` for the
best additive residual against `1.00985`; recomputed for this revision), a star (so additivity
already fails for binary Markov *trees*, which answers the question left open in D25), and a
tilted antiferromagnetic chain of three sites — and showed why random search had no power
against it (the violations occupy tuned regimes of relative volume below `10⁻⁴`).  No
counterexample was found for open chains without tilt.  For antiferromagnetic chains the best
additive residual is staggered, and the uniform chord gap is not the threshold of the class.
So for chains the one-reference sandwich of Theorem 11.28(d) holds as stated there — it does
not use the product structure — but its width is not a single-site quantity, and the threshold
is open.

### 11.16 Without a hint: Monte Carlo is exponent-optimal among non-adaptive algorithms

Theorem 11.25 left the cost of algorithms *without a hint* on the cube class between the
exponent `ln 2 − h(Λ₁/u) ≈ u²/32` of the zero residual and `ln cosh u ≈ u²/2` (Chebyshev), and
called the value `e^{KL(π‖uniform)}` of importance sampling a heuristic.  This section proves
that value on the whole class, shows that no non-adaptive algorithm does better — by the
method of Mathé–Novak (2007) for log-Lipschitz densities — and reduces the open question to
adaptivity.  Setting and notation of Theorem 11.25: `X = {0,1}ⁿ`, `f ≡ 0`, `d = c·`Hamming,
`u = βc`, algorithms that are `(ε/2, δ)`-correct for `ln Z` on the whole class; `w = e^{−βg}` is the
Gibbs weight, `A = 2^{−n} Σ_x w(x)`, `B(r)` a Hamming ball, `Δ_r` the effect of the dip on `B(r)` at
the zero residual (`e^{Δ_r} − 1 = 2^{−n} Σ_{j≤r} C(n,j)(e^{u(r+1−j)} − 1)`), `p_u = 1/(1+e^u)`, `KL(a‖b)` the
binary relative entropy; recall `ln cosh(u/2) = KL(½‖p_u)`.

*Status.*  Written in cycle 10 and refereed (`reviews/R5_referee_report.md`): no statement was
found false; three major defects — the first version said nothing at bounded accuracies, the
prior art for the lower bound was missing, and the labels claimed more machine-checking than
there is — are corrected below (`DEAD_ENDS.md` D43).  Lemma 11.43(c) and the present form of
Theorem 11.44 follow an appendix of that report; we re-derived and tested them (harness
XIII.2), and they have not been refereed a second time.

**Lemma 11.43 (tail lemmas) [(a) V; (b), (c) P + K] (`NonAdaptive.lean`).**
(a) *Any space, any envelope.*  Let `g` be admissible and `t > 0`.  If `w(z) ≤ t` then
`w(x) ≤ t e^{β d(z,x)}` for every `x`, and if `w(y) ≥ t` then `w(x) ≥ t e^{−β d(x,y)}`: an admissible
residual can neither fall nor rise faster than the envelope (`weight_le_of_outside`,
`weight_ge_of_inside`).  Hence, with `D = {w > t}` and `S = {w ≥ t}`,

    Σ_x w(x)  ≤  Σ_x min(w(x), t)  +  t Σ_{x ∈ D} (e^{β dist(Dᶜ, x)} − 1),        Σ_x min(w(x), t)  ≥  t Σ_x e^{−β dist(x, S)}

(`sum_le_truncated_add_tail`, `sum_truncated_ge`; `dist(Dᶜ, x) = min_{z∉D} d(z,x)`, in this
orientation also for asymmetric envelopes).  Both sums on the right depend only on the shape
of a level set.
(b) *The cube, above the threshold.*  If `∅ ≠ D ≠ X` and `|D| ≤ |B(r)|`, then
`Σ_{x∈D} (e^{u dist(x, Dᶜ)} − 1) ≤ 2ⁿ(e^{Δ_r} − 1)`, with equality for balls.  Proof: the erosions
`D_j = {x : dist(x, Dᶜ) ≥ j}` are the complements of the neighbourhoods `N^{j−1}(Dᶜ)`;
`|Dᶜ| ≥ |B(n−r−1)|`, so `|N^{j−1}(Dᶜ)| ≥ |B(n−r+j−2)|` by Harper's vertex-isoperimetric theorem
(initial segments of the simplicial order minimise the neighbourhood, hence
`|A| ≥ |B(k)| ⇒ |N^t(A)| ≥ |B(k+t)|`), i.e. `|D_j| ≤ |B(r+1−j)|`; and the sum is
`Σ_{j≥1} (e^{uj} − e^{u(j−1)}) |D_j|`.  So **the mass above a threshold is at most the excess of a
dip on a ball of the size of the super-level set**: `E(w − t)₊ ≤ t (e^{Δ_r} − 1)`; truncated
cones attain equality.  This is the isoperimetric step of Theorem 11.25(c), used there at the
zero residual only, applied to the level sets of an arbitrary member of the class.
(c) *The cube, below the threshold* (fifth referee).  If `|S| ≥ |B(k)|`, then
`2ⁿ E min(w, t) ≥ t·T_n(k)`, `T_n(k) = Σ_j C(n,j) e^{−u(j−k)₊}`: the sum `Σ_x e^{−u dist(x,S)}` is
increasing in every `|N^i(S)|`, and `|N^i(S)| ≥ |B(k+i)|` by Harper.
The reduction to Harper's theorem in (b) and (c) is a paper proof; the referee checked the
erosion bound for all subsets of the `n`-cube, `n ≤ 5`, and harness XIII.1–2 check (b) and (c) on
members of the class for `n ≤ 9`.

**Theorem 11.44 (plain Monte Carlo on the whole class) [P; uses Lemma 11.43].**
Let `X_1,…,X_M` be uniform, `Â = M⁻¹ Σ_i w(X_i)`, `1 ≤ K ≤ M`, `r` the least radius with
`|B(r)| ≥ 2ⁿK/M`, `t*` the upper `K/M`-quantile of `w`, and

    Γ′_n(r) = Σ_{j≤r} C(n,j)(e^{u(r+1−j)} − 1) / T_n(r−1)   (r ≥ 1),        Γ′_n(0) = 0.

For **every** residual of the class:
(a) `A ≤ (1 + Γ′_n(r)) · E min(w, t*)`.
(b) For `0 < η < 1`: `Â ≥ (1−η) A/(1 + Γ′_n(r))` outside an event of probability `e^{−η²K/2}`;
`Â ≤ A/δ₂` outside an event of probability `δ₂`; and `Â ≤ (1 + η + Γ′_n(r)/δ₃) A` outside an event
of probability `e^{−η²K/3} + δ₃`.
(c) `n⁻¹ ln Γ′_n(ρn) → KL(ρ‖p_u)` for `p_u ≤ ρ ≤ ½` and `→ −KL(ρ‖p_u)` for `0 < ρ < p_u`.  Hence
(i) at an extensive accuracy `ε = nε₁`, `0 < ε₁ < ln cosh(u/2)`, the estimate
`ln Â + ½[ln(2(1+Γ′_n(r))) − ln(1/δ₂)]` is `(ε/2, e^{−K/8} + δ₂)`-correct on the whole class as soon
as `ln(2(1+Γ′_n(r))) + ln(1/δ₂) ≤ ε`, and `e^{n θ_na(ε₁) + o(n)}` samples suffice, with

    θ_na(ε₁)  =  min { KL(ρ‖½) : KL(ρ‖p_u) ≤ ε₁ };

(ii) at every fixed accuracy `ε > 0` the plain estimate `ln Â` is correct on the whole class
with `e^{n KL(p_u‖½) + O(√n)}` samples (take `r = p_u n − O(√n)`, where `Γ′` is a small constant).

*Proof.*  `D = {w > t*}` has fewer than `2ⁿK/M ≤ |B(r)|` points and `{w ≥ t*}` has at least
`2ⁿK/M > |B(r−1)|`; Lemma 11.43(b) and (c) give
`E(w − t*)₊ ≤ t* (e^{Δ_r} − 1)` and `E min(w,t*) ≥ t* 2^{−n} T_n(r−1)`, which is (a) (for `r = 0` the set
`D` is empty).  Write `Â = Â_trunc + Â_exc`, the means of `min(w, t*)` and of `(w − t*)₊`.  The
variables `min(w(X_i), t*)/t* ∈ [0,1]` have total mean at least `K`: the multiplicative Chernoff
bounds give `(1−η) E min(w,t*) ≤ Â_trunc ≤ (1+η) E min(w,t*)` outside events of probability
`e^{−η²K/2}` and `e^{−η²K/3}`; `Â_exc ≥ 0` has mean at most `Γ′ A`: Markov.  (c) is Stirling's
formula: the numerator has exponent `h(ρ)` below `p_u` and `uρ + ln(1+e^{−u})` above, the
denominator `uρ + ln(1+e^{−u})` below `p_u` and `h(ρ)` above, and
`uρ + ln(1+e^{−u}) − h(ρ) = KL(ρ‖p_u)`.  ∎

The first version of this theorem bounded `E min(w,t*)` below by `t* K/M` only, i.e. had
`|B(r−1)|` in place of `T_n(r−1)`; the minimum over `r` of that quantity tends to `4eᵘ(eᵘ−1)`, so
the bound was void below an accuracy of about `ln(2(1+4eᵘ(eᵘ−1))) + ln(1/δ₂)` and the Chebyshev
bound of
Theorem 11.25 remained the only one there (referee, M1; benchmark B12 shows both versions at
`ε = 1`).  At `ε₁ → 0` the exponent is `KL(p_u‖½) = n⁻¹ KL(π_cone‖uniform)` (`≈ u²/8`), the sample
size that Chatterjee–Diaconis (2018) give for importance sampling at one instance, the cone;
by the tail lemmas the two geometric sums are attained by cones up to one unit of radius, so
their sample size holds on the whole class at the exponential scale and replaces `ln cosh u`.
Harness XIII.2 (the deterministic inequalities on members of the class; the Chernoff step by
simulation at small `K`, where failures do occur).

**Theorem 11.45 (non-adaptive algorithms) [(a) V; (b) V given two finite sums; closed forms, (c)–(e) P] (`nonadaptive_expected_queries_ge`, `cube_nonadaptive_bound`).**
Call an algorithm *non-adaptive* if its set of evaluated points does not depend on the
answers.
(a) *Any class, any functional.*  Let `(g_j, g'_j)` be pairs of class members with
`|Φ(g'_j) − Φ(g_j)| > ε` and `v ≥ 0` weights such that every point lies in difference sets
`{g'_j ≠ g_j}` of total weight at most `B`.  Then every randomised non-adaptive algorithm that
is `(ε/2, δ)`-correct on the class evaluates at least `(1 − 2δ) Σ_j v_j / B` points in
expectation.  (For adaptive algorithms only alternatives of one common instance can be
combined in this way, Theorem 11.22(c); here both members of the pair vary, because the
query set is the same on every instance.  Without that hypothesis the statement is false:
the referee gives a four-point example.)
(b) *The cube.*  For every centre `s` the cone `c·d_H(·, s)` and the cone with a flattened
bottom `max(c·d_H(·, s), cR)` are members of the class and differ exactly on the open ball
`{d_H(·, s) < R}` (machine-checked); flattening lowers `ln Z` by
`D_R = n ln(1+e^{−u}) − ln Σ_j C(n,j) e^{−u max(j,R)}` (elementary counting).  If `ε < D_R`, every
randomised non-adaptive algorithm needs at least `(1 − 2δ) 2ⁿ/|B(R−1)|` evaluations (the Lean
theorem has the drop of `ln Z` and the size of the ball as two finite sums over the cube).
(c) `n⁻¹ D_{ρn} → KL(ρ‖p_u)` for `p_u ≤ ρ ≤ ½`.  With Theorem 11.44: **the exponent of non-adaptive
algorithms on the cube class is `θ_na(ε₁)` at extensive accuracies and `KL(p_u‖½)` at every fixed
accuracy, and plain Monte Carlo attains it.**  This is a statement about exponents: at
`n = 4000`, `u = 1`, `ε = 1` the two bounds are `e^{0.134n}` and `e^{0.109n}` (benchmark B12).
(d) *Adaptivity defeats the construction.*  A point and its `n` neighbours determine the
centre `s` of a cone; if in addition `g(s̄) − g(s) = cn` at the antipode `s̄`, the two McShane
envelopes of these two values coincide, so `g` is that cone and `ln Z` is known exactly.  An
algorithm that makes these `n + 3` evaluations and otherwise falls back on any class-correct
procedure is correct on the whole class and costs `n + 3` on every cone (referee, Appendix D;
harness XIII.3), against `e^{188}` for non-adaptive ones at `n = 6400`, `u = 1`,
`ε₁ = ¼ ln cosh ½`.
(e) *Pre-drawn points with adaptive stopping.*  For algorithms that evaluate a sequence
fixed in advance and choose only when to stop,
`max_s E τ(cone_s) ≥ (1−2δ)² 2ⁿ/(2|B(R−1)|)` whenever `ε < D_R` (the first index at which the
sequence enters the ball of a uniformly random centre exceeds `m` with probability at least
`1 − m|B(R−1)|/2ⁿ`; referee, Appendix C): the same exponent in the worst case over cones —
although such an algorithm can be cheap elsewhere, Proposition 11.46.

*Prior art for the method.*  Mathé and Novak (2007) prove a lower bound for all non-adaptive
Monte Carlo methods on the class of log-concave densities with a Lipschitz logarithm by
Bakhvalov's averaging over densities `exp(−α‖y − y_i‖)` with hidden centres and integrands
supported near the centre, remark that one function value identifies the centre for an
adaptive method, and give an adaptive Metropolis algorithm of polynomial cost that uses
log-concavity.  Theorem 11.45(b) is that construction on the cube.  Not there: the cube, the
functional `ln Z`, a class without concavity, the exponent, and the matching upper bound on
the whole class (Theorem 11.44) — which we did not find elsewhere either.
*The formulas are in print at one instance* (found by the Scientific Discovery Division,
SCI-REV-0004, which read the sources in full; we verified the first formula and the
subject of the paper).  For `N` independent two-state units — the discrete random energy
model — Suárez, Silbey and Oppenheim (Phys. Rev. E 85, 051108 (2012), arXiv:1108.5783) compute
the bias of the Jarzynski estimator of a free-energy difference from `M = e^{γN}` samples:
`ΔF = N log(2/(1 + e^{−ε}))` is our `nΛ₁` (their eq. (31)), the maximal bias
`B_max = N log cosh(ε/2)` is our threshold `E` of §11.10, and their "freezing" formulas (eqs.
(39)–(46) in the division's reading) are `n·KL(ρ_θ‖p_u)` and `a = KL(p_u‖½)` — the accuracy and the
exponent of plain Monte Carlo *at the cone*, which is their system; at bounded accuracy
the sample size `e^{na}` there is Chatterjee–Diaconis (2018).  **So what is not in print, as
far as two divisions could find, is the minimax content:** that the cone is the worst
instance of the Lipschitz class for plain Monte Carlo (Theorem 11.44), and that no
non-adaptive algorithm does better (Theorem 11.45(b)).  The exponent function itself and
the constants `Λ₁`, `ln cosh(u/2)`, `KL(p_u‖½)` are not new.

**Proposition 11.46 (a certified bracket from two independent uniform samples) [P].**
Draw two independent uniform samples of size `M ≥ 2K`.  Let `t̂` be the `⌈K⌉`-th largest weight
in the first, `Â_t̂` the mean of `min(w, t̂)` over the second, and `r̂` the least radius with
`|B(r̂)| ≥ 2^{n+1}K/M`.  With `K = 24 ln(4/δ)`, outside an event of probability `δ`, on every
instance,

    Â_t̂ / (3/2)  ≤  A  ≤  2 Â_t̂ + t̂ (e^{Δ_r̂} − 1)

(the last term is absent if `r̂ = 0`).  (The `K`-th largest of `M` samples lies above the upper
`2K/M`-quantile and its super-level set has probability at least `K/2M`, outside events of
probability `e^{−K/4}` and `e^{−K/6}`; then Chernoff for the second sample and Lemma 11.43(b).)
At the zero residual `t̂ = Â_t̂`, so the bracket has logarithmic width
`ln(3/2) + ln(1 + e^{Δ_r̂})`: for `ε > 2` it is narrower than `ε` once
`M ≥ 2K·2ⁿ/|B(k*(ε − 2) − 1)|` (when `k*(ε−2) ≥ 1`) — the cost of the hinted spot-check of Theorem
11.25(c), up to the constant in the accuracy.  The algorithm that doubles `M`, uses
`K_i = 24 ln(4·2^i/δ)` at stage `i` (a union bound over the stages), and stops when the bracket
is narrower than `ε` is therefore correct on the whole class for every `ε > ln 3`; at the zero
residual it has the exponent of the best algorithm with a hint, for `ε > 2` and in particular
for extensive accuracies; and it never needs more than the Monte Carlo sample size of
Theorem 11.44 up to a polynomial factor.  (The bracket is never narrower than `ln 3`; with
`1 ± η` in place of `3/2` and `2`, and `K` of order `η⁻²`, smaller accuracies are reached at the
price of a factor `ε⁻²`.)  Harness XIII.5 (coverage by simulation; the width at the zero
residual).

So the picture for extensive accuracies `0 < ε₁ < ln cosh(u/2)` is:

| algorithms | exponent | status |
|---|---|---|
| with a hint, at the zero residual | `θ_hint = KL((Λ₁+ε₁)/u ‖ ½)` | Theorem 11.25 |
| non-adaptive (and, in the worst case over cones, pre-drawn points with adaptive stopping) | `θ_na = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ ε₁}` | Theorems 11.44–11.45 |
| adaptive, without a hint | between `θ_hint` and `θ_na` | **open** |

`θ_hint < θ_na` throughout (`ρ = (Λ₁+ε₁)/u` has `KL(ρ‖p_u) = ε₁ + ln 2 − h(ρ) > ε₁`); both vanish at
`ln cosh(u/2)` with the same leading term `2((ln cosh(u/2) − ε₁)/u)²`, and at `ε₁ → 0` they are
`0.0291` and `0.1109` for `u = 1` (`0.0077`, `0.0303` for `u = ½`; `0.0973`, `0.3278` for `u = 2`), a
factor that tends to `4` as `u → 0`.  At finite `n` the two sides of the second row are
`0.0293` (with `δ = 0.05`) and `0.0307` (total failure probability `0.10`) for `u = 1`,
`ε₁ = ¼ ln cosh(½)`, `n = 6400` (limit `0.0283`; harness XIII.4, benchmark B12).

*What adaptivity would have to do* (heuristics, not theorems).  The hard instances of the two
bounds are different: a *dip* hidden in the zero residual is found only by hitting its ball,
with or without adaptivity; a *flattened bottom* is hidden from uniform samples but not from an
algorithm that follows the slope of the cone.  In the families we examined by hand
(calculations not recorded) that are built from Hamming balls — populations of cones, a cone
on a mesa among many mesas, cones shadowed by shallower dips, decoys — uniform sampling
followed by local exploration costs at most `e^{nθ_hint}`: a structure that matters is deep, a
deep member of a Lipschitz class is wide, and structures that shadow a deep centre reveal it
by coincidences.  A proof needs an algorithm that learns a hint from an arbitrary member of
the class; a refutation needs a prior on which locating the critical difference set is hard
even with slopes.  The adaptive upper bound of Mathé–Novak uses log-concavity, which this
class lacks.  Neither a proof nor a refutation is known to us (workstream H).

### 11.17 Correlated uncertainty: classes that are linear in features, and pair-distance profiles for chains

§11.14 ended negatively for chains: every envelope in per-torsion format has constants that
grow with the lever arm.  The exponential lower bounds of §§11.4–11.10 are theorems about
*first-order* classes, which constrain a residual only through pairwise differences: what is
learned at one configuration says something about another only through the envelope distance
between the two, and certificates are coverings.  Physical residuals have more structure — a
sum of few-body terms with unknown radial functions is **linear in the unknown**, and its
uncertainty at different configurations is *correlated* through the coefficients.

*Status.*  Written in cycle 10 and refereed (`reviews/R6_referee_report.md`): no inequality
stated as a theorem was found false and every machine-checked label was confirmed; six major
defects of wording and scope are corrected below (`DEAD_ENDS.md` D43) — among them a comparison
of formats that was not like with like.  An independent workstream checked the statements on
rotamer chains and went further (`workstreams/P_REPORT.md`), and its report was itself
reviewed (`reviews/R_P_review.md`): all eighteen of its statements were re-derived and none
found false, every number quoted here was reproduced with independent code, four of them
were corrected, and several sentences of its summary — which this section had repeated —
were stronger than its theorems (`DEAD_ENDS.md` D44).  What is taken from the workstream is
marked.  Proposition 11.50 was added after the reviews and is not refereed.

**Theorem 11.47 (classes that are linear in features) [V; the exactness statements are linear-programming duality, K] (`LinearClass.lean`).**
Let `g(x) = Σ_α θ_α F_α(x)` with known features `F : X → ℝ^p` and unknown coefficients in a box,
`|θ_α − θ⁰_α| ≤ w_α`.
(a) *No evaluations.*  `sup_θ [g(x) − g(y)] = θ⁰·(F(x) − F(y)) + Σ_α w_α |F_α(x) − F_α(y)|`
(`linRes_sub_le`, `linRes_sub_attained`).  So, around its centre, the class is contained in the
first-order class of the **feature envelope** `d_F(x,y) = Σ_α w_α |F_α(x) − F_α(y)|`, a pulled-back
weighted `ℓ¹` distance (`featEnv_isEnvelope`, `linRes_dev_admissible`), and pairwise it is exactly
as wide.
(b) *After evaluations* `g(x_i) = v_i`, `i ≤ m`: for **every** `λ ∈ ℝ^m`

    | g(y) − Σ_i λ_i v_i − θ⁰·r |  ≤  Σ_α w_α |r_α|,        r = F(y) − Σ_i λ_i F(x_i)

(`linRes_span_upper`, `linRes_span_lower`).  Each end of the set of consistent values is
attained after its own optimisation: the largest is `min_λ [λ·v + θ⁰·r + w·|r|]`, the smallest
`max_λ [λ·v + θ⁰·r − w·|r|]` (duality of a linear program; harness XIV.1, also for data at a
vertex of the box).  The two optimal `λ` differ in general, so the width is **at most**
`2·min_λ w·|r|`, twice the weighted `ℓ¹` distance of `F(y)` to the span of the evaluated feature
vectors, with equality at the central data.  That distance is the *worst case over the data*
— the radius of information of a linear problem on a balanced convex set, attained at the
zero information by an affine rule (Smolyak; Micchelli–Rivlin 1977; Sukharev for classes that
are not symmetric) — while for given data the bracket can be narrower, down to a point (two
features suffice for an example; in random instances a seventh of the brackets is strictly
narrower).  McShane's bound is the case of a unit vector `λ`; that a first-order class "has
the distance to the nearest evaluated point" is likewise a statement about the worst case.
(c) *Rank.*  If `F(y)` lies in the span of the evaluated feature vectors, `g(y)` is determined
exactly (`linRes_span_exact`).  Hence `rank F ≤ p` evaluations determine the residual on all of
`X`: a certificate for the minimum, for `ln Z` and for every other functional, at every
accuracy, whatever the size of `X`.
(d) *With a remainder.*  Let `g = θ·F + ρ` with `ρ` in a first-order class of envelope `d`.  For
coefficients with `Σ_i λ_i = 1` (necessary: the remainder is defined up to a constant) the
upper end of (b) gains the term

    sup_ρ [ρ(y) − Σ_i λ_i ρ(x_i)]  =  the cost of transporting  δ_y + Σ_i λ_i⁻ δ_{x_i}  onto  Σ_i λ_i⁺ δ_{x_i}  at unit cost d

(Kantorovich–Rubinstein duality; workstream P, Theorem 14, with the minimum over `λ` exact).
Machine-checked is the bound by one transport plan — everything is shipped to or from `y`:
`Σ_i (λ_i⁺ d(y, x_i) + λ_i⁻ d(x_i, y))` (`sumClass_span_upper`), and for the lower end the
transposed term `Σ_i (λ_i⁺ d(x_i, y) + λ_i⁻ d(y, x_i))` (`sumClass_span_lower`; with the term of the
upper end the statement is false for asymmetric envelopes).  The plan through `y` can be
wasteful: for the star `x⁰, x⁰ ⊕ e_i` on the cube and a remainder of envelope `η·`Hamming it
gives `2k(k−1)η` at Hamming distance `k`, while the transport cost is `2(k−1)η` (referee,
attained).  So an additive residual plus a first-order remainder is determined by a star up
to a term *linear* in the distance; the quadratic law of §11.7 belongs to second-order
classes.

The first-order class of the *same* envelope is exponentially more expensive.  On the cube
with the features `F_i(x) = x_i` and `w_i = c`, the feature envelope is `c·`Hamming: its
first-order class is the cube class of §11.10 (every deterministic algorithm needs
`2^{n(1−o(1))}` evaluations at the zero residual, every randomised one exponentially many below
the threshold), and the linear class is the set of additive residuals with slopes in `[−c, c]`
(`n` evaluations; `n + 1` with a constant term).  The difference between "additive instances"
and "the class" that runs through Theorems 11.23–11.28 is this difference.

**Theorem 11.48 (pair-additive residuals: the envelope is a transport distance between pair-distance distributions) [the inequalities V on a grid of distances and for one pair type; attainment and the transport form P].**
Consider a chain with `N` beads, a finite set `𝒯` of pair types, squared pair distances
`s_pq(x)`, and residuals

    g(x) = Σ_{p<q} φ_{τ(p,q)}(s_pq(x)),        φ_τ  L-Lipschitz in s,   φ_τ(s) = 0  for  s ≥ S_c

with unknown radial functions (a known centre is part of `f`; `L` is a Lipschitz constant in
the *squared* distance, so terms that are steep at short range are outside).  Let `N^x_τ(s)` be
the number of pairs of type `τ` with `s_pq(x) ≤ s`, for `s < S_c` — the cumulative pair-count
profile.
(a) `g(x) = −Σ_τ ∫_0^{S_c} φ_τ′(s) N^x_τ(s) ds` (`pairRes_eq_cum`): the class is linear in the
profiles, with coefficient functions in an `L^∞` ball of radius `L`.  This is the textbook
energy equation of a pair-additive system after one integration by parts.
(b) Hence `sup_g [g(x) − g(y)] = L Σ_τ ‖N^x_τ − N^y_τ‖_{L¹[0,S_c]} =: d_P(x,y)` (`pairRes_sub_le`,
`pairRes_admissible`, `profEnv_isEnvelope` for the inequality; attained by `φ′ = −L·sgn(N^x − N^y)`).
Equivalently `d_P(x,y) = L Σ_τ ‖sort(s̃^x_τ) − sort(s̃^y_τ)‖_{ℓ¹}`, `s̃ = min(s, S_c)`: the
Wasserstein-1 distance between the multisets of squared distances truncated at the cutoff
(Kantorovich–Rubinstein duality on the line; harness XIV.4 compares the three forms on
lattice chains).  `d_P` is a pseudometric with large fibres: it is invariant under rigid
motions and reflections — so every member of the class takes the same value on a
conformation and its mirror image — and under permutations of beads that preserve the pair
types, and it vanishes between any two conformations with equal profiles (the 802 075
self-avoiding walks with 16 beads on the square lattice have 541 profiles at `S_c = 5`;
referee, reproduced by the science division with the convention "all pairs, squared distance
below 5" — 507 with the pairs of §11.22, chain separation at least 3).  The fibres have three
distinct sources (science division, `SCI-REV-0006` §4 and W4, by exhaustive enumeration):
*labels* — different chains through the same set of sites; *homometry* — non-congruent
conformations with the same complete multiset of distances, a classical subject (Patterson),
which occurs for lattice chains from 6 beads on: the walks through
`(0,0),(0,1),(0,2),(1,2),(1,3),(2,3)` and through `(0,0),(0,1),(1,1),(1,2),(1,3),(2,3)` have the
squared distances `1⁵2³4¹5³8¹10¹13¹` and are not congruent (re-checked here; harness XIV.5); and
*truncation* — the profile keeps only the pairs below the cutoff.  The theorem that a generic
configuration of points is determined by its distribution of distances (Boutin–Kemper 2004)
does not apply to chains: its genericity condition fails whenever two distances coincide
(their Lemma 1.8), as the bond lengths of a chain do.  The first-order class of `d_P` is the
class of Lipschitz functionals of the pair-distance statistics.
(c) After evaluations, for every `λ`:
`|g(y) − Σ_i λ_i v_i| ≤ L Σ_τ ‖N^y_τ − Σ_i λ_i N^{x_i}_τ‖_{L¹}` (`pairRes_span_upper`, `pairRes_span_lower`;
with an enclosure of the profile of `y` over a voxel of conformations in place of the profile,
`pairRes_span_upper_enclosure`).  As in Theorem 11.47(b), each end is exact after its own
optimisation, and the half-width is at most `L` times the `L¹` distance from the profile of `y`
to the *span* of the evaluated profiles, with equality at the zero data.
(d) *Scattering curves of one conformation are members of the class* (science division,
Proposition A2.1 of `SCI-REV-0006`; re-derived and re-computed here, harness XIV.5; the
Lipschitz constant machine-checked, `sinc_sqrt_lipschitz` **[V]**, `Scattering.lean`).  One pair
type.  For `N` equal point scatterers the orientationally averaged (Debye) intensity of a
conformation at wave number `q` is `I_x(q) = N + 2 Σ_{p<p′} sinc(q r_pp′(x))`, `sinc t = sin t/t`,
`r = √s`, and

    |I_x(q) − I_y(q)|  ≤  (q²/3) · Σ_k |s^x_(k) − s^y_(k)|        for all q ≥ 0

(sorted squared distances of all pairs; the sum is `d_P(x,y)/L` without truncation;
`debye_sub_le` **[V]** for any matching of the pairs).  Reason: `s ↦ sinc(q√s)` has Lipschitz
constant exactly `q²/6` on `s ≥ 0`, because `d/ds sinc(q√s) = (q²/2)(t cos t − sin t)/t³` at
`t = q√s` and `|sin t − t cos t| ≤ t³/3` (the derivative of the left side is `t sin t`), with
equality in the limit `t → 0` — the Guinier regime, where `I_x(q) ≈ N² − (q²/3) Σ_{p<p′} s_pp′`.
So for every fixed wave number the functional `x ↦ ½(I_x(q) − N)` is a member of the
pair-additive class with `L = q²/6` (take the cutoff at the largest possible squared distance
and subtract the known constant `sinc(q√S_c)` per pair), and (b), (c) and the kernel of
Proposition 11.50 apply verbatim to *scattering curves* in place of unknown energies: curves
evaluated at some conformations bracket the curve of a new conformation by the transport
distance of its profile to their span.  The fibres of the complete profile are exactly the
sets of conformations that no orientationally averaged scattering experiment can tell apart
(kinematic approximation, form factors independent of `q`); the two walks of (b) have
identical curves.  *Scope:* one conformation, not an ensemble — for an ensemble the
intensity is a Boltzmann average of a member of the class, to which Theorem 11.34 applies,
not this theorem — and squared distances without a cutoff: a truncated profile is not what
a scattering experiment measures.  This is the only place in the report where a measurable
quantity is a member of one of its classes; no experimental data are used.

**Proposition 11.49 (what the profile format costs) [P; (c) V].**  Suppose every conformation
has at most `zN/2` pairs within the cutoff (excluded volume; this excludes the phantom product
domains of §11.14).
(a) *Existence at extensive accuracy, first-order class of `d_P`* (pair-additivity is not
used).  For every known part, every residual of the class and every accuracy `ε = ε₁N`, the
minimum and `β⁻¹ ln Z` have certificates of size

    ln N_cov  ≤  ln 4 · |𝒯| · ⌈4 z L S_c / ε₁⌉,

independent of `N`.  (The profiles are nondecreasing with total mass at most `M = zN/2` over
all types.  Round every profile down to multiples of `q = M/(|𝒯|G)` and move each of the at most
`|𝒯|G` remaining jumps of size `q` up to the next of `G` grid points per type: the `L¹` error is at
most `2S_cM/G`, and at most `C(2|𝒯|G, |𝒯|G) ≤ 4^{|𝒯|G}` functions remain.  A maximal subset of
profiles that is `ε/2L`-separated is then a net of `d_P`-radius `ε/2` with at most
`4^{|𝒯|⌈4zNLS_c/ε⌉}` elements, and a net of radius `ρ` determines every value within `±ρ`.  This
is the classical entropy of monotone functions; the linear dependence on `|𝒯|` is due to
workstream P and the referee; harness XIV.4 checks the rounding.)  **This is an existence
statement, not a planning number**: it evaluates to `10^{93}`–`10^{2697}` at accuracies at which 8
to 7000 evaluations suffice in the referee's examples, because the a-priori diameter
overestimates the real one several times and that factor sits in the exponent.  With `G`
discrete distances `ln N_cov ≤ |𝒯|G ln(1 + 2|𝒯| z L S_c/ε₁)` (volume bound; referee), and the
number of profiles is at most `C(zN/2 + |𝒯|G, |𝒯|G)`, so the first-order class of `d_P` has
certificates of size polynomial in `N` at *every* accuracy on a lattice (workstream P).
(b) *The pair-additive class.*  If the squared distances below the cutoff take at most `G`
values, the class has at most `|𝒯|·G` features and by Theorem 11.47(c) at most `|𝒯|·G` evaluations
determine the residual exactly, at every accuracy.  On a lattice `G` does not depend on `N`
(for a nearest-neighbour contact energy with unknown strengths there is one feature per pair
type: the number of contacts of that type).  For chains on the rational torus of §5 `G` is
finite for every `N` but grows with `N` — `1, 1, 1, 2, 5, 14, 36` for `N = 4,…,10` in the referee's
model — so that count is not independent of the chain length there.  With continuous
distances, greedy reduced bases give `(8(1+κ)|𝒯| z L S_c/ε₁)²` evaluations at extensive accuracy
for residuals with `|φ′| ≤ κL` (the published greedy theorem of DeVore–Petrova–Wojtaszczyk 2013
in `L²` and Cauchy–Schwarz; derived independently by workstream P and by the referee, who has
the constant `256` for the worst-case bracket.  The cited corollary, 3.3(ii) of the arXiv
version, was read in full by the reviewer of workstream P and is quoted correctly; the
argument is that of the `P`-greedy algorithm of kernel interpolation, Santin–Haasdonk 2017).
(c) *Sharpness is stochastic dominance* **[V]** (`pairRes_le_of_dominates`, `pairRes_sharp`).  If
the known radial function rises by at least `L` per unit of squared distance below the cutoff
(an attraction at least as steep as the uncertainty), then known part plus residual is a
nonincreasing functional of the cumulative profile, and a conformation whose profile
dominates all others pointwise — `N^x_τ(s) ≥ N^y_τ(s)` for all `y`, `τ`, `s` — is optimal for every
residual of the class: no evaluation is needed.  In general the candidates are the
conformations on the Pareto front of the dominance order.
(d) *Fixed absolute accuracy.*  For the first-order class the argument of (a) gives only
`exp(O(N/ε))`, and on conformation spaces whose profiles can be varied freely this is the truth
at `f = g = 0`: `ln N_cov(ε) ≥ c·L m₁ ℓ N/ε` with an explicit small `c` (referee, by a
Gilbert–Varshamov packing of staircases; not re-derived by us).  So in the regime in which a
ground state is told from its competitors the first-order class of `d_P` is exponential in `N`
off-lattice in general — at most stretched-exponential for a gapped site-additive known part
at the zero residual (workstream P) — while the pair-additive class stays polynomial.
(e) *What is not covered, and what is not counted.*  If every pair is its own type, `d_P` is
the weighted `ℓ¹` distance of the squared-distance matrices clamped at `S_c` and the number of
features grows with `N²`: for a vanishing known part at the zero residual, on the product
domain, the first-order format is exponential again and the span format needs at least
`n − 2ε/(Lδ₁₄)` evaluations, one per torsion (`δ₁₄` the difference of the squared 1–4 distances;
workstream P, Proposition 12, by the classical width of a box in `ℓ¹`, Pietsch–Stesin; the
reviewer extends both to a gapped torsional known part when `Lδ₁₄ > 2e` and to self-avoiding
chains of the sizes at which every trans/gauche pattern occurs).  The summary "the cost is
governed by the number of independent features, not by the length of the chain" is a
heuristic: the proved upper bound for the span format is the rank, the proved lower bound
counts torsions, and the first-order format depends on `N` at a fixed number of features
(`5 → 21` evaluations with three features in the table below).  Chirality and everything
else that is not a function of the pair-distance statistics must be in the known part.
Many-body terms need profiles on higher-dimensional spaces (measures on triangles for
three-body terms, with a transport norm in place of the `L¹` distance of cumulative counts).
**What a remainder outside the class costs depends on how it is bounded.**  A remainder
bounded in the supremum norm by `η` costs an accuracy floor `η(1 + ‖λ‖₁)` and nothing else
(workstream P, Theorem 13).  A remainder that is only known to be first-order in an envelope
`η·d₀` is paid at first-order prices: the slack of the sum class at every conformation is at
least the sum of the two slacks, so a certificate is at least as large as the first-order
certificate of the remainder alone (workstream P, Corollary 15), and with a per-torsion `d₀`
whose constants grow with the lever arm the exponential cost of D42 returns **for every
fixed `η > 0`** — by Theorem 11.37 the leading term of the exponent does not depend on `η`,
which enters a sub-leading correction only (reviewer; the first version said "in proportion
to `η`", for which there is no theorem).  The chain-length independence therefore belongs to
residuals that are Lipschitz functionals of the pair-distance statistics, up to a sup-norm
remainder — not to chains, and not only to the exactly pair-additive class (part (a) uses no
pair-additivity).  No lower bound above two evaluations is proved for the sum class on the
measured instance; greedy covers have 2 to 21 points and prune to 2 to 17 (reviewer).
With a purely torsional known part none of the three formats has, in the measurements
(`n ≤ 12`), a one-evaluation threshold that is independent of `N`: a hairpin changes the
profile by an amount proportional to `N`, and the largest `L` at which one evaluation
certifies the lattice chain decays like `4.8/N` (reviewer; not a theorem).  Finally, all counts are evaluations of the residual: *checking* a certificate
requires a lower bound of `f + L_A` over all conformations, `L_A` depends on global pair
counts, and over voxels of torsions the enclosure of a pair distance widens with the lever
arm — the difficulty of §11.14 leaves the constants and returns in the checker (referee).
Whether a given physical residual lies in such a class with a useful `L` is an empirical
question that this report does not address.

**Proposition 11.50 (a kernel for residuals that are linear in pairwise features) [V] (`LinearKernel.lean`; not refereed).**
Let the features be pairwise tables with nonnegative entries (contact counts, cumulative pair
counts on a grid), the coefficients lie in a rational box, and `(a_i, v_i)` be evaluated
anchors.  A certificate is a subdivision of the coefficient box; at a leaf with box `[lo, hi]`
it carries multipliers `λ_i` and a certificate of the pairwise kernel of §6.1 for the instance
`E₀ + Σ_α lo_α F_α`, with value `m`.  The kernel accepts the bound `L` if at every leaf

    L  ≤  m  +  Σ_i λ_i v_i  −  Σ_α max(lo_α c_α, hi_α c_α),        c_α = Σ_i λ_i F_α(a_i),

and then `L ≤ E₀(x) + Σ_α θ_α F_α(x)` for every configuration and **every real coefficient
vector of the box that is consistent with the anchors** (`verifyL_sound`, `verifyLTop_sound`).
The first term uses `F ≥ 0`; the data term is a lower bound for `Σ_i λ_i (v_i − θ·F(a_i))`, which
vanishes on consistent coefficients and can be made large on a part of the box that
contradicts the anchors, so such parts are discharged without work.  Worked example
(`contactTriangle_bound`, verified by kernel evaluation): the frustrated triangle with a
contact term of unknown strength in `[−2, 2]`; without the evaluation the best bound is `−1`,
with one evaluation the kernel certifies `1`, which is attained, with two leaves.  This is
weak duality for the robust problem — the minimum over the coefficient polytope of a concave
function — and no more; what it adds to §6 is that correlated uncertainty is handled by the
existing pairwise kernel, leaf by leaf.  It addresses the last point of Proposition 11.49(e)
only for features that are pairwise in the *rotamer* variables.  Harness XIV.3 checks the
leaf bound against brute-force robust minima.

*How the formats compare* (the first version of this section set `exp(Θ(N))`, `exp(Θ̃(√N))` and
`exp(O(1))` side by side "at an extensive accuracy"; that was not like with like — Theorem
11.38 is a statement at `ε = 0`, and its `L` is a Lipschitz constant in RMSD, while `L` here is
per pair, so that an extensive pair-additive residual has an RMSD constant of order `N`;
referee, M2).  Like for like:

| residual class | accuracy | per-torsion Hamming | RMSD used directly | profile envelope `d_P` |
|---|---|---|---|---|
| RMSD-Lipschitz, constant fixed | `ε = 0`, zero residual | `exp(Θ(N))` (11.37) | `exp(Θ̃(√N))` (11.38) | not applicable (another class) |
| RMSD-Lipschitz, constant fixed | `ε₁N` | `exp(Θ(N))` (11.37) | `exp(O(Lb/ε₁))`, independent of `N` (blocks of beads snapped to a grid; referee, re-derived here) | not applicable |
| functional of pair statistics, per-pair `L` fixed (RMSD constant `∝ N`) | `ε₁N` | `exp(Θ(N))` | `exp(O(N))`; a matching lower bound is not proved | `exp(O(1))` (11.49(a)) |
| the same | fixed `ε`, or `ε = 0` | exponential | exponential | first-order class: `exp(O(N/ε))`, polynomial on lattices; pair-additive class: polynomial (11.49(b)) |

So a reader may conclude that a residual which is admissible for `d_P` has certificates at an
extensive accuracy whose number of evaluations is bounded independently of the chain length
(a bound that is far above anything measured: see below), and that
finitely many distances make a pair-additive residual exactly learnable; not that the profile
format beats the RMSD format on a common class at a common accuracy, not that its
certificates stay bounded at a fixed accuracy, and nothing about residuals that are not
functionals of pair-distance statistics.

*Measured on the same instances* (workstream P, reproduced and in four entries corrected by
its reviewer; known part `e·#gauche`, zero residual, `L = e`, exact certification of the
minimum; the Hamming entries hold for every valid vector of constants — the smallest valid
constant exceeds the largest gap, so no conformation is covered by another one):

| chain | per-torsion Hamming | profile envelope | span |
|---|---|---|---|
| diamond lattice, `S_c = 12`, `n = 8 → 12` torsions | all conformations (`5849 → 422 825`) | `10 → 21` | 2 throughout (rank 3) |
| off-lattice, `n = 5 → 10` | all conformations (`99 → 8115`) | `27 → 319` (`×1.5`–`1.9` per torsion) | between 3 and 10 |
| `ln Z`, lattice, `n = 8`, `ε = 0.01` | all 5849 | between 65 and 69 (of 90 profiles) | 3 |

*Chain length, measured further* (Computational Research Division, `ENG-RES-0002` and
`ENG-RES-0007` on branch `research/ubuntu-engineering` at `db56d05`: an independent
implementation, exhaustive enumeration, covers by integer programming with certified dual
bounds; it reproduces every published number of this table and of the workstream, closes
two brackets — 319 and 60 at ten torsions off-lattice — and extends them; **empirical
evidence [N], not re-derived here**).  Smallest certificates of the profile format, known
part `#gauche`, zero residual, `L = 1`; a pair `[a, b]` is a certified bracket:

| chain | sizes | `ε = 0` | `ε = N/4` | `ε = N/2` |
|---|---|---|---|---|
| diamond lattice, `S_c = 12` | `n = 5 → 24` torsions, `8 → 27` beads (`1.5·10¹¹` conformations, 4 532 profile classes at the largest size) | `5 → [80, 92]`, about `N²/10` | `4 → [28, 31]`, about one per torsion | `3 → 15`, about one per two torsions |
| off-lattice, `S_c = 16` | `n = 5 → 12`, `8 → 15` beads (47 141 conformations, 6 137 classes) | `27 → [757, 788]` | `19 → [251, 284]` | `9 → [109, 136]`, a factor 1.3–1.7 per torsion |

(With `L = 1/5`: at most 8 at `ε = 0` and 2 at `ε = N/2` on the lattice; 21 and 4 off-lattice.)
**There is no saturation at extensive accuracy at any size that can be enumerated, on
either model.**  On the lattice the profile set is still expanding — the largest `‖N^x‖₁` per
bead is 13.6 at 27 beads against a bulk bound of 35, about 38 % — so the covering problem at
accuracy `ε₁N` is not yet scale-invariant, and compactness approaches its bulk value with
surface corrections; a plateau should not be expected from enumeration at all (their
finite-size argument, from exact data).  Off-lattice the number of distinct distances below
the cutoff grows with the chain, the set to be covered is effectively infinite-dimensional,
and the plateau that Proposition 11.49(a) guarantees is of the order `exp(c·zLS_c/ε₁)`: with
`L = 1` geometric growth can continue for thousands of torsions before that bound bites.  So
the true and useful statement is: **the profile format is orders of magnitude cheaper than
the per-torsion format at every size measured (8 evaluations against at least 136 200 at 15
beads and accuracy `N/2` on the lattice), its cost grows with the chain at every such size,
and what governs it is the dimensionless ratio `zLS_c/ε₁`** — which is why the question
whether realistic residuals have a small per-pair constant in this format (§12 item 9(f)) is
the one that matters.  "Independent of the chain length" describes a regime that is not
reached.
Three further exact results of the same enumeration.  (i) *Every trans/gauche pattern is
realised by a self-avoiding conformation of the diamond-lattice chain, for every `n`*
(exhaustively for `n ≤ 24`; in general because even bonds can be restricted to two of the four
lattice directions and odd bonds to the other two in such a way that one coordinate
increases along every bond: the walk is then self-avoiding whatever the choices, and at
every torsion both a trans and a gauche continuation remain) — so the hypothesis under
which the lower bounds for per-torsion formats extend from product domains to
self-avoiding chains holds for all `n`, not only for the sizes checked before.  (ii) The
single-flip constants (largest profile distance between two conformations that differ in
one torsion) form a valid torsion-Hamming envelope at every size through 16 torsions,
exhaustively, and satisfy `c_j ≥ κ·d_j` with `d_j` the distance from the nearer chain end and
`14 ≤ κ ≤ 22` — linear growth from below, with a plateau at the centre of the chain, not a
linear law.  (iii) The traversal number `m(δ)` of workstream P (§3.2 of its report) is not
reproducible as defined — the starting point and the tie-breaking are unspecified — and the
exact covering numbers of the profile set keep increasing where `m(1)` had been read as
saturating at `N ≈ 13` (`DEAD_ENDS.md`, D46).
What the limit *is* — the normalised profile set with its lower boundary of gauche counts,
and the covering number of that limit object — is the question the other division put
back to the theory (`ENG-REQ-0001`); **§11.22 answers it in part**: a limit shape exists for
bridges **[P]** and is conjectured for all walks **[C]**; the certificate sizes of bridges
converge to its covering number off a countable, unidentified set of accuracies; for every
limit point of the certificate sizes of all walks at `(L, ε₁) = (1, ½)`: between 116 and 3 627
**[P, computer-assisted]**; our estimate of the limit is a few hundred and of the chain
length at which it is approached `10³`–`10⁵` beads or more **[N]** (wording of the review
SCI-REV-0002 of the Scientific Discovery Division, finding M1; the first version said "the
plateau is between 50 and 3 627 …, reached at `10³`–`10⁵` beads").

*Prior art.*  Theorem 11.47(a)–(c) is optimal recovery of a linear functional from linear
information over a box (Smolyak; Micchelli–Rivlin 1977) in its worst-case part and plain
linear-programming duality — the feasible-set intervals of set-membership estimation
(Milanese–Vicino 1991), robust linear programming with box uncertainty (Soyster 1973) — in its
data-dependent part.  Potentials that are linear in pair counts per type and distance bin,
determined by linear inequalities over decoys, are those of Maiorov–Crippen (1992; known to
us through Tobi–Shafran–Linial–Elber 2000, who use exactly these features).  The size of the
coefficients as an "extrapolation grade" is the D-optimality criterion of active learning for
potentials that are linear in features (Podryabinkin–Shapeev 2017; their grade is the `ℓ^∞`
size of the multipliers, the transport term of (d) a weighted `ℓ¹` size).  The distance `d_P` is
a named object (science division, `SCI-REV-0006` W3; our first version cited only descriptor
distances): the Wasserstein distance between *global distance distributions* of metric
measure spaces, a standard lower bound of the Gromov–Wasserstein distance (Mémoli 2011;
Mémoli–Needham 2022, where it is `L_{H,p}`; here `p = 1`, equally weighted beads and the
truncated squared distance in place of a metric), whose zero set is homometry in Patterson's
sense.  As an earth mover's distance between shapes it is in Osada et al. (2002), sorted pair
descriptors compared in `ℓ¹` are the "bag of bonds" (Hansen et al. 2015), and Wasserstein
distances between radial distribution functions are used as structural similarity scores; the entropy of monotone functions is classical
(Birman–Solomyak; van de Geer), as are greedy reduced bases (Binev et al. 2011;
DeVore–Petrova–Wojtaszczyk 2013; their use for greedily chosen evaluation points in
worst-case recovery is the `P`-greedy algorithm, Santin–Haasdonk 2017), the width of a box in
`ℓ¹` (Pietsch 1974; Stesin 1975) and transport with a boundary reservoir (Figalli–Gigli 2010).
The reading of the profile distance as the *exact* envelope (support function) of the class
of unknown Lipschitz pair potentials is Kantorovich–Rubinstein duality for that distance; we
did not see it stated as a statement about classes of potentials, and its use next to a known
part, the count of evaluations that follows and the comparison with the first-order class of
the same envelope were not found — all immediate once named.  That pair distances do not
determine a configuration of points is classical (Patterson; Jiao–Stillinger–Torquato 2010 for
pair statistics), and that scattering sees only the pair-distance distribution is the Debye
formula; the generic uniqueness theorem (Boutin–Kemper 2004) excludes chains, as said under
Theorem 11.48(b).  Verification status of each citation: `prior_art/L8_linear_classes.md`.

### 11.18 Adaptivity replaces the hint: the exponent of adaptive algorithms without a hint

§11.16 left one question open: non-adaptive algorithms without a hint have the exponent
`θ_na(ε₁) = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ ε₁}`, algorithms with a hint `θ_hint(ε₁) = KL((Λ₁+ε₁)/u ‖ ½)`,
and `θ_hint < θ_na` below the threshold `ε* = ln cosh(u/2)`.  Where between the two is the
exponent `θ*(ε₁)` of *adaptive* algorithms that are correct on the whole class and are given
nothing but the oracle?  This section answers: **at `θ_hint`.**  Notation of §11.16: `Q_n` the
cube, `L_u` the class of `u`-Lipschitz `ψ`, `w = e^{−ψ}`, `A = 2^{−n} Σ w`, accuracy `ε = ε₁n`, an
algorithm is correct if `|output − ln A| ≤ ε/2` with probability at least `1 − δ` for every
member of the class; `a := θ_na(0+) = KL(p_u‖½)`, `h := θ_hint(0+) = KL(Λ₁/u‖½)`.

*Status.*  Written in cycle 10 after §11.16 had been refereed.  Theorems 11.51 and 11.52 are
due to an independent workstream (`workstreams/H_REPORT.md`, Theorems H1 and H2), which also
found the recursion of Theorem 11.53 and conjectured its limit from numerics; the
oracle-relative form of Theorem 11.52, the identity (11.18.1) and the convergence proof are
the coordinator's.  **Paper proofs throughout, except the analysis of the recursion and the
deterministic core of the bracket (validity of the two ends, width), which are
machine-checked; the count of evaluations — the content of the theorem — is not.**
An independent referee read the draft (`reviews/R7_referee_report.md`): verdict on Theorem
11.54 "proved with gaps" — the statement is believed true, could not be broken, and no error
was found in the accounting of Theorem 11.52 beyond the closure gap; the gaps (an abort rule;
the induction over levels, which needs left limits in the accuracy and a ladder defined
relative to the inner dimension; prior art) are written into the text below, following the
referee.  What the referee did and did not check is listed at the end of the section.
The workstream
derived three wrong recursions before the right one, the coordinator's own first accounting
of a multilevel scheme was wrong as well, and the algorithm as first written here and in
the workstream's report closed too early on some inputs (`DEAD_ENDS.md` D45; found by harness
XV.3): the bookkeeping of "which tolerance enters which count" is the dangerous part, and it
is the part written out below.

**Theorem 11.51 (radial instances: adaptivity closes the whole gap) [P; workstream H].**  Let
`R_u ⊂ L_u` be the class of radial functions `ψ(x) = f(d(x, s))`, with an arbitrary centre `s`
and `|f(j+1) − f(j)| ≤ u` — it contains the zero function, every dip, the cone and the
flattened cones on which the non-adaptive lower bound of Theorem 11.45 was proved.  For
algorithms that are correct on `R_u`:
(a) non-adaptive algorithms have the exponent `θ_na(ε₁)` exactly (the lower bound of Theorem
11.45 uses members of `R_u` only);
(b) adaptive algorithms have the exponent `θ_hint(ε₁)` exactly:

    (1 − 2δ) 2ⁿ / |B(n, k*(ε))|   ≤   min_alg max_{ψ ∈ R_u} E#queries   ≤   (n+1) ⌈ ln(2n/δ) 2ⁿ / C(n, r_ε) ⌉ + 2n + 1,

where `k*(ε)` is the least `k` with `Δ_k > ε` and `r_ε = k*(ε) − O(1 + 1/u)`.
*Proof of the upper bound.*  Draw `M` uniform points and query each with its `n` neighbours.
The neighbours of a point at distance `j` from the centre take the value `f(j−1)` in the `j`
coordinates in which the point differs from `s` and `f(j+1)` in the others.  If some sampled
point has two distinct neighbour values, flipping one of the two value classes gives `s` or
its antipode; one monotone path from there (`n + 1` queries) reveals `f`, and `ln A` is computed
exactly.  Otherwise, with probability at least `1 − δ/2` every shell `r ≤ j ≤ n − r` contains a
sampled point (`r` the least radius with `M·C(n,r)/2ⁿ ≥ ln(2n/δ)`), so `f(j−1) = f(j+1)` there: `f`
is 2-periodic on `[r−1, n−r+1]` with the two observed values — the value at the first sampled
point and the common value of its neighbours, provided that point lies in that range, which
fails with probability `2B/2ⁿ`, `B = |B(n, r−2)|`; so the bound is stated for `4|B(n, r_ε − 2)|/2ⁿ ≤ δ`,
which holds for fixed `δ`, extensive accuracy and `n` large.  The alternating sum of binomial
coefficients over that range is negligible, and the two caps are bounded through the
Lipschitz condition from their rims, which gives `A` up to the factor
`[1 − 4B/2ⁿ, 1 + 4(e^{Δ_{r−2}} − 1) + 8B/2ⁿ]`.  The lower bound is Theorem 11.25(a)
at the zero function, whose competitors are dips.  ∎
The algorithm trusts the promise of radiality and is not an algorithm for `L_u`; the theorem
says where the hardness of Theorem 11.45 comes from (an unknown centre that a non-adaptive
sample cannot use), not how to remove it in general.  The profile `f(j) = (u/2)(−1)^j` shows
that the second branch is needed: no order of neighbours reveals the centre.

**Bracket procedures.**  A *bracket procedure* for dimension `d` with accuracy `x`, failure
probability `δ′` and cost `C` is a randomised adaptive algorithm that makes at most `C` queries
to any `ψ ∈ L_u` on `Q_d` and returns `L ≤ U` with `L ≤ A(ψ) ≤ U` and `U ≤ e^x L`, except with
probability `δ′`; the bound `C` on the number of queries holds always, not only on a good
event.  A family of bracket procedures — one for every `d`, `x > 0`, `δ′ > 0`, with a cost
`C(d, x, δ′)` that is nonincreasing in `x` and in `δ′` — has the *exponent function* `T` if
`limsup_d d^{−1} ln C(d, ξd, e^{−cd}) ≤ T(ξ)` for every `ξ > 0` and `c > 0`.  Two families are at hand:
one query gives a bracket of accuracy `2ud` (the oscillation of `ψ` is at most `ud`); and the
two-sample bracket of Proposition 11.46 is a family with exponent function `θ_na` (`0` from
`ε*` on) — this is Theorem 11.44 read as a statement about brackets.  The midpoint of a bracket
of accuracy `ε` is a correct output.

**Theorem 11.52 (one more level) [P; algorithm and proof for the two-sample inner bracket: workstream H].**
Let a family of bracket procedures have the nonincreasing exponent function `T`, and let
`0 < φ < 1`, `0 < β < g`, `η₀ > 0`.  Then there is a family with accuracy `gn + O(log n)` in
dimension `n` whose cost is, for every member of `L_u` and every failure probability `e^{−cn}`,
at most `exp(n(τ + η₀) + o(n))`,

    τ  =  sup_{γ ≥ β} [ min(γ, φ·θ_na((g − β)/φ))  +  (1 − φ)·T(γ/(1 − φ)) ].                     (11.18.2)

So if `T` is an exponent function of bracket procedures on the whole class, so is (up to an
arbitrarily small loss)

    R[T](g)  =  inf_{0<φ<1, 0<β<g}  sup_{γ ≥ β} [ min(γ, φ θ_na((g − β)/φ)) + (1 − φ) T(γ/(1 − φ)) ].

*The algorithm.*  Split the coordinates, `Q_n = Q_o × Q_i` with `n_o = ⌊φn⌋`, `n_i = n − n_o`, and
write `W(a) = 2^{−n_i} Σ_b e^{−ψ(a,b)}` for the fibre averages, so that `A = E_a W(a)`, and
`p(s) = P_a(W(a) > s)`.  Three facts:
(F1) every fibre `b ↦ ψ(a, b)` is `u`-Lipschitz on `Q_i`, so the inner procedures apply to it;
(F2) `a ↦ −ln W(a)` is `u`-Lipschitz on `Q_o` (compare the sums term by term; `fibre_sum_le`), so the
tail lemma 11.43 applies to `W`: if `p(s) ≤ |B(n_o, r)|/2^{n_o}` **with `r ≤ n_o − 1`** then
`E(W − s)₊ ≤ s·2^{−n_o}·E_r(n_o)`, where `E_r(n) = Σ_{j≤r} C(n,j)(e^{u(r+1−j)} − 1)` (the lemma needs a
point outside the super-level set; for `r = n_o` the statement is false);
(F3) *layer cake*: `s·p(s) ≤ A` for every `s` (`level_mul_exceed_le_mean`), and for nonnegative
levels `s₀ ≤ s₁ ≤ … ≤ s_j`

    A  ≤  s₀ + Σ_{i<j} s_{i+1} p(s_i) + E(W − s_j)₊        (`mean_le_layer_cake`).

Parameters: `G = gn`, levels `s_j = s₀ e^{j}`, `K = ⌈24 ln(2^{n+6} n³/δ)⌉`, a finite decreasing ladder
of inner accuracies with **fixed rates relative to the inner dimension**, `x_l = ξ_l n_i`,
`ξ₀ = 2u > ξ₁ > … > ξ_last = β/(1−φ)` with steps at most `η₀`, the tolerance `b := x_last` (`= βn + O(1)`), and
`J = ⌈2un + b + n_o ln 2 + 10⌉`.  One query at a reference point gives
`s₀ ≤ min W` with `max W ≤ s₀e^{2un}`.  A list `a₁, a₂, …` of independent uniform outer points is
kept; each carries a bracket of its fibre average that is only ever refined (by calling the
inner procedure at the next accuracy of the ladder and intersecting).  To *classify* a point
at level `j` means to refine its bracket `[L, U]` until `U ≤ s_j` ("low") or `L > s_j e^{−b}` ("high");
this ends at the latest at accuracy `x_last = b` (if both hold, either label will do).  The
algorithm keeps a certified lower bound
`ℓ ≤ A` (initially `s₀`) and runs through the levels `j = 0, 1, …`:

* `M := K`; repeat: classify `a₁, …, a_M`; let `N` be the number of high points and
  `q := min(1, 2 max(N, K)/M)`; if `N ≥ K` put `ℓ := max(ℓ, s_j e^{−b} N/(2M))`.
* *Closure test.*  Let `r` be the least radius with `|B(n_o, r)| ≥ 2^{n_o} q`.  If `r = n_o` no closure
  is attempted.  Otherwise put `tail := s_j 2^{−n_o} E_r(n_o)` (`tail := 0` if `2^{n_o} q < 1`); if
  `tail ≤ e^G ℓ`, stop and return `[ℓ, s₀ + Σ_{i<j} s_{i+1} q_i + tail]`, where `q_i` is the value of `q` with
  which level `i` was left.
* Otherwise, if `N ≥ K` (the level is *populated*) or `M ≥ M_j^neg := 2KJe·s_j/(ℓe^b)` (the level
  is *negligible*), go to the next level; else double `M`.
* *Abort.*  If the number of queries exceeds the bound of the cost proof below, or level
  `J + 1` is reached, or a point is not classified at `x_last` (an inner bracket wider than
  promised), stop and return the trivial bracket `[s₀, s₀e^{2un}]`.  On the good event none of
  this happens, so the failure probability is unchanged and the cost bound holds always.

*Proof.*  Good event: (V1) every inner bracket is valid; (V2) for every level `j` and every `M`
of the doubling sequence, if `M p(s_j) ≥ 2K` then at least `M p(s_j)/2` of `a₁..a_M` have `W > s_j`;
(V3) for all `j`, `M` and all `x ∈ b + ℕ`: at most `max(2M p(s_j e^{−x}), K/2)` of `a₁..a_M` have
`W > s_j e^{−x}`.  The levels depend only on the reference point, so (V2), (V3) are Chernoff
bounds for independent samples at `O(n³)` fixed thresholds (failure `e^{−K/4}` and `e^{−K/12}` each).
The inner calls are chosen adaptively, but the set of *potential* calls is deterministic —
`M ≤ 4K·2^{n_o}` always, since beyond `2K·2^{n_o}` points a level is populated or its tail is zero —
and each potential call can be given its own randomness in advance; with the inner failure
probability `δ/(2^{n+6}n³)` and the choice of `K` the total failure probability is at most `δ`
for `n ≥ n₀(η₀)`.

*Validity.*  By (V1) a point with `W > s_j` is classified high, and a high point has
`W > s_j e^{−b}`.  Hence `N ≥ #{W > s_j}` and (V2) gives `p(s_j) ≤ q`; if `N ≥ K`, (V3) with `x = b`
gives `p(s_j e^{−b}) ≥ N/(2M)` and so `s_j e^{−b} N/(2M) ≤ A` by (F3): `ℓ ≤ A` always.  The upper end
is (F3) with `p(s_i) ≤ q_i` and (F2) with `|{W > s_j}| ≤ 2^{n_o} q ≤ |B(n_o, r)|`, `r < n_o` (`mean_le_upper`).

*Width.*  A populated level has `s_{i+1} q_i = 4e^{b+1} · s_i e^{−b} N/(2M) ≤ 4e^{b+1} ℓ`, a negligible
one `s_{i+1} q_i ≤ e·s_i·2K/M_i^neg = e^b ℓ/J`; `s₀ ≤ ℓ`; `tail ≤ e^G ℓ`.  So the ratio of the two ends
is at most `1 + 4Je^{b+1} + e^b + e^G` (`upper_le_width`), and its logarithm at most `gn + ln(4eJ + 3)`.

*Termination within `J` levels.*  Above `max W · e^b` nothing is high, `ℓ` no longer changes,
`M_j^neg` grows by `e` per level, and once `M > 2K·2^{n_o}` the tail is zero.

*How large `M` gets.*  Put `Γ̃(r) = E_r(n_o)/|B(n_o, r−1)|` (`Γ̃(0) = e^u − 1`), so that
`2^{−n_o} E_r ≤ q Γ̃(r)` by the minimality of `r`.  Let `r†` be the largest `r ≤ n_o − 1` with
`Γ̃(r′) ≤ e^{G−b}/4` for all `r′ ≤ r`, and `M† = 2K·2^{n_o}/|B(n_o, r†)| = exp(nφ θ_na((g − β)/φ) + o(n))`.  At a populated
level `tail ≤ s_j q Γ̃(r) ≤ 4e^b ℓ Γ̃(r)`, at a negligible one `tail ≤ e^b ℓ Γ̃(r)/(eJ)`; so a level that
is left without stopping has `r > r†`, that is, `q_j > 2K/M†`.  Consequently
`M_j^neg ≤ 4Je² M†` at every level that is reached: `ℓ` never decreases, so `M_j^neg ≤ e·M_{j−1}^neg`;
if level `j − 1` was negligible then `M_{j−1}^neg ≤ M_{j−1} < M†`; if it was populated then
`ℓ ≥ s_{j−1} e^{−b} q_{j−1}/4`, whence `M_j^neg ≤ 8KJe²/q_{j−1} < 4Je² M†`.  Every `M` that is used is at
most `8Je² M†`.

*How many points are close to a level* — the count on which everything rests.  For every
earlier level `i < j`: `s_i p(s_i) ≤ s_i q_i ≤ 4e^b ℓ` (populated: by the update of `ℓ`; negligible:
`s_i q_i ≤ e^b ℓ/(eJ)`).  For `x ≥ b` let `s_i` be the largest level not above `s_j e^{−x}`; then

    2M_j^neg · p(s_j e^{−x})  ≤  (4KJe·s_j/(ℓe^b)) · (4e^b ℓ e^{x+1}/s_j)  =  16KJe² · e^x,

in which **the two factors `e^b` cancel** — the same tolerance is used for "high" and for
"negligible", and this is why.  With (V3): at most `32KJe² e^x + 4K` of the points used at
level `j` have `W > s_j e^{−x}`.  In words: the lower levels have certified that few fibres are
high, so by Markov's inequality few of the points sampled at level `j` can lie within a
factor `e^x` of it.

*Cost.*  A point with `W(a) = s_j e^{−G_a}`, `G_a ≥ 0`, is classified at level `j` at the first rung
`x_l ≤ max(G_a, b)` of the ladder: if `x_l ≤ G_a` then `U ≤ W e^{x_l} ≤ s_j`; if `x_l ≤ b` and `U > s_j` then
`L > s_j e^{−b}`.  A point above the level is classified at the first rung below `b + |G_a|`.  So the
points whose last rung at level `j` is `l ≥ 1` have `W > s_j e^{−x_{l−1}}`; by the count above their
number is at most `min(8Je² M†, 32KJe³ e^{x_{l−1}} + 4K)` (one factor `e` for rounding `x_{l−1}` up
into `b + ℕ`), and each costs at most `(l+1)·C(n_i, x_l, δ′)`, the cost being nonincreasing in the
accuracy.  Hence

    #queries  ≤  Σ_{j ≤ J} Σ_l  min( 8Je² M† ,  32KJe³ e^{x_{l−1}} + 4K ) · (l+1) · C(n_i, ξ_l n_i, δ′),

a sum of polynomially many terms; only the finitely many rates `ξ_l` occur, so the pointwise
definition of the exponent function suffices, and with `γ_l := (1−φ)ξ_l ≥ β` and `x_{l−1}/n ≤ γ_l + η₀ + o(1)`
the largest term has the exponent
`max_l [min(φ θ_na((g−β)/φ), γ_l + η₀) + (1−φ) T(γ_l/(1−φ))] ≤ τ + η₀`.  The bound holds on the good
event, and by the abort rule always.  It is attained up to `o(n)` by an outer landscape that
is flat and inner landscapes on which the inner procedure is at its worst (for `T = θ_na`:
`ψ(a,b) = u·d(b, s)`, or with centres that move with `a`) — `τ` is the exponent of this algorithm
and not only a bound for it (referee).  ∎

*What the algorithm does.*  It never estimates a mean of heavy-tailed values.  Level by
level it certifies that few fibres exceed the level — a one-sided statement, whose cost per
sampled point is governed by the *gap* between the point and the level — and it uses the
tail lemma once, at the top of the ladder, where the certified exceedance probability is
already that of a small ball.  At the exponential scale `A = max_s s·p(s)`.  No product
structure of `ψ` is used.

**Theorem 11.53 (the recursion converges to the hinted exponent) [V] (`HintRecursion.lean` for an abstract pair of exponent functions; `CubeHintPair.lean` for the functions of the cube; `BoundedAccuracy.lean` for the recursion itself, defined in Lean: `exactRec_tendsto_hint`).**
(a) *An identity.*  For `0 < ρ < 1`: `KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁` (`klBin_shift`).  Read at the
radius `ρn`: the accuracy that a non-adaptive sample of `e^{nθ}` points certifies is the accuracy
that the same number of points certifies with a hint, **plus `θ` itself** — without a hint,
a sample cannot exclude that a set of the size it has not seen carries all the weight.
Consequently, for `0 ≤ e < ε*`,

    θ_na( e + θ_hint(e) )  =  θ_hint(e),        in particular   θ_na(h) = h                      (11.18.1)

(`cubeNa_add_cubeHint`; here `θ_na` is `cubeNa`, defined through the largest feasible radius and
shown to be the minimum of the definition of §11.16 in `cubeNa_isLeast_allRadii`; also
`cubeHint_lt_cubeNa`: `θ_hint < θ_na` on `[0, ε*)`).

(b) *The hinted exponent is a fixed point.*  `R[θ_hint] = θ_hint` on `(0, ε*)`.
"`≤`" (`step_from_hint_le`, `cube_step_from_hint_le`): with `φ = g/(g + θ_hint(g))` and `β → 0` the outer sample has the
exponent `φ·θ_na(g/φ) = φ θ_hint(g)` by (11.18.1), the inner brackets are needed at accuracy rate at
most `g`, and `φ θ_hint(g) + (1−φ) θ_hint(g) = θ_hint(g)`: an outer sample and inner samples of the
hinted sizes, for the hinted accuracy on both blocks.  "`≥`" (`cube_hint_superSolution`): for any `φ`, `β` let `ρ_o` be
the outer radius (`φ KL(ρ_o‖½) = μ := φ θ_na((g−β)/φ)`) and take `γ = max(β, μ)` with inner radius `ρ_i`
(`uρ_i − Λ₁ = γ/(1−φ)`, or `ρ_i = ½`); by (a), `φ(uρ_o − Λ₁) ≤ g − β − μ`, so the mean radius
`ρ̄ = φρ_o + (1−φ)ρ_i` has `uρ̄ − Λ₁ ≤ g − β − μ + γ ≤ g`, and by convexity of `KL(·‖½)` the bracket is at
least `φ KL(ρ_o‖½) + (1−φ) KL(ρ_i‖½) ≥ KL(ρ̄‖½) ≥ θ_hint(g)` (also in the small-slope limit,
`gauss_hint_superSolution`; harness XV.1 checks it numerically).  Since `R` is monotone and `θ_na ≥ θ_hint`,
**no level of the recursion goes below the hinted exponent** — as it must not, by the lower
bound of Theorem 11.25(a); a wrong accounting of the algorithm typically violates this
(two of the workstream's superseded recursions did).
(c) *No fixed point above it.*  Let `T` be nonincreasing and bounded above with `T ≤ R[T]`.  Then
`T ≤ θ_hint` on `(0, ε*)` (`superSolution_le_hint`, `cube_superSolution_le_hint`).
(d) *Convergence.*  Let `T₁ = θ_na` and `T_{k+1} = min(T_k, R[T_k])`.  Then for every `g ∈ (0, ε*)`
and `η > 0` there is a `k` with `T_k(g) < θ_hint(g) + η` (`iterates_lt_hint_add`,
`cube_iterates_lt_hint_add`).
The abstract statements are about a pair of functions with the properties used — (11.18.1),
`e + θ_hint(e)` nondecreasing, `θ_na` continuous and bounded, `θ_hint(e) ≥ h − Le` (structure `HintPair`) —
and hold for the small-slope limit `θ_na(x) = (1 − √x)²`, `θ_hint(e) = (1 − e)²/4` (`gaussPair`) and for
the functions of the cube (`cubePair`, with `L = 1`; an independent Lean workstream, after the
referee had asked for it: the calculus is that `KL(·‖p_u)` is strictly increasing on `[p_u, ½]`,
`KL(·‖½)` strictly decreasing on `[0, ½]`, and the largest feasible radius depends
continuously on the accuracy).  In both cases the bound of (c) is attained
(`hintRecursion_witness`, `cube_hintRecursion_witness`).  One caveat that the formalisation
exposed: `θ_hint` as a formula increases again beyond `ε*`, so "(b), `≤`" is stated for the
exponent continued by zero from `ε*` on (`cubeHintClip`).  What is **not** in Lean is the
operator `R` itself: `StepLE θ_na T T′` states `T′ ≤ R[T]` without suprema, and that the iterates
`T_{k+1} = min(T_k, R[T_k])` satisfy the hypotheses of (d) — nonincreasing, nonnegative, bounded,
`T_{k+1} ≤ R[T_k]` — is immediate from the definition of `R` and is not formalised.
*Proof of (c).*  Three choices of parameters in `T ≤ R[T]`, with `S(x) := x + T(x)`:

    (i)   φ = g/h, β → 0:               T(g) ≤ sup_{0 < γ ≤ g} [ γ + (1 − g/h)·T(γ/(1 − g/h)) ]      (g < h);
    (ii)  φ fixed:                       T(g) ≤ (1 − φ) · sup_{0 < x ≤ φa/(1−φ)} S(x)                   for every g;
    (iii) φ = g/(g + θ_hint(g)), β → 0:   T(g) ≤ (θ_hint(g)/(g + θ_hint(g))) · sup_{0 < x ≤ g} S(x).

((i) and (iii) use (11.18.1) to evaluate the outer exponent, and the continuity of `θ_na` to
let `β → 0`.)  *Step I: `τ := sup T ≤ h`.*  Suppose `τ > h` and put `c = τ/h − 1`.  If `T(x) ≤ τ − σx`
near zero with `σ ≤ 1`, then (i) gives `T(g) ≤ (1 − g/h)τ + (1 − σ)g = τ − (σ + c)g` near zero: the
slope improves by `c`.  But (ii) allows no slope `σ ≥ 1`: it would give `T ≤ (1 − φ)τ` everywhere
for a small `φ`, contradicting the definition of `τ`.  Starting from `σ = 0` the slope exceeds
one after finitely many steps.  *Step II.*  Let `D = T − θ_hint` and `M(g) = sup_{x ≤ g} D(x)`.  Since
`x + θ_hint(x)` is nondecreasing, (iii) gives `D(g) ≤ (1 − φ*(g))·M(g)` with `φ*(g) = g/(g + θ_hint(g))`,
and Step I gives `D(x) ≤ h − θ_hint(x) → 0` as `x → 0`.  If `M(g₁) > 0`, then `D ≤ M(g₁)/2` near zero
and `D ≤ (1 − c₀) M(g₁)` on the rest of `(0, g₁]`, so `M(g₁) < M(g₁)`.  ∎  (d) follows by applying (c)
to `inf_k T_k`, which satisfies `T ≤ R[T]` because the `T_k` are nonincreasing functions — a
supremum over `γ` of a decreasing sequence of such functions is, up to any `η`, attained on a
finite grid.

**Theorem 11.54 (the adaptive exponent without a hint) [P: Theorems 11.25(a), 11.44, 11.52, 11.53].**
For every `u > 0`, `0 < ε₁ < ε*` and `0 < δ < ½`, the least number of evaluations with which a
randomised adaptive algorithm without a hint is correct on all of `L_u`, in the worst case
over the class, is

    exp( n·θ_hint(ε₁) + o(n) ),        θ_hint(ε₁) = KL( (Λ₁ + ε₁)/u ‖ ½ ),

the same exponent as with a hint at the hardest instance, while non-adaptive algorithms need
`exp(n·θ_na(ε₁) + o(n))` with `θ_na > θ_hint`.  *At the exponential scale a hint is worth nothing
to an adaptive algorithm, and everything that it is worth is lost by a non-adaptive one.*
*Proof.*  Lower bound: Theorem 11.25(a) at the zero function (an algorithm without a hint is
an algorithm with one); it bounds the expected number of evaluations at one instance, hence
the worst case, with the same convention for the accuracy.  Upper bound.  Fix `η > 0`; choose
`g < ε₁` with `θ_hint(g) ≤ θ_hint(ε₁) + η`, then `k` with `T_k(g) < θ_hint(g) + η` (Theorem 11.53(d)), then the
parameters of the `k − 1` levels, then let `n → ∞`.  *Base:* the two-sample brackets form a family
with exponent function `T₁ = θ_na` (`K = 24 ln(4/δ′) = O(d)`; cost `e^{dθ_na(ξ)+o(d)}` for `ξ < ε*` and `e^{o(d)}`
from `ε*` on).  *Assembly:* for a family with nonincreasing exponent function `T` and a tuple
`(φ, β, g, η₀)`, Theorem 11.52 gives procedures of accuracy `gd + ln(4eJ + 3)` in every dimension `d`;
enumerate a countable dense set of tuples and let the new procedure for `(d, x, δ′)` be the
cheapest among the old one and the first `d` tuples whose accuracy is at most `x`.  Its cost
is nonincreasing in `x` and `δ′`, and for fixed `ξ` every tuple with `g < ξ` is eventually admissible,
so the new family has the exponent function `T′ ≤ min(T, R[T])(·⁻) + η₀`, with a **left limit**
in the accuracy — nothing shows that the `T_k` are continuous.  *Shift:* if `T̃ ≤ T(·⁻) + η′` then
`R[T̃](g) ≤ R[T](g − ε) + ε + η′` for `0 < ε < g` (replace `β` by `β + ε` and `γ` by `γ − ε`; the outer exponent
is unchanged).  *Induction:* if the level-`k` family has `T̃_k ≤ T_k(·⁻) + η_k`, the level-`(k+1)` family
has `T̃_{k+1} ≤ T_{k+1}(·⁻) + η_k + 2η₀`.  So at accuracy `ε₁n` the level-`k` family costs
`exp(n(T_k(g) + kη′) + o(n))` for every `g < ε₁`, which suffices because `θ_hint` is continuous; and
the midpoint of a bracket of accuracy at most `ε₁n` is a correct output.  The `o(n)` at level
`k + 1` consists of polynomial factors and of the finitely many `o(n_i)` of level `k`; the
failure probability handed down is `δ/(2^{n+6}n³)` per level, still `e^{−O(kn)}` at the bottom.  (The
induction in this form is the referee's.)  ∎

*What this does and does not say.*
(1) It is a statement about exponents, with `o(n)` terms that come from `k` nested levels,
each with its own ladder and union bounds; `k → ∞` as the exponent approaches `θ_hint`.  An
earlier variant of the two-level algorithm was simulated by the workstream at `n = 32`: of 32
runs, 12 closed within the budget, with valid brackets, and on the three instances where
the comparison was made it needed far more evaluations than plain Monte Carlo for a wider
bracket.  The referee evaluated the corrected algorithm in expectation with exact binomial
arithmetic on 30 radial outer profiles and by adversarial search over profiles: the excess
of `n^{−1} ln(cost)` over `τ` falls from `0.029` at `n = 10³` to `0.0002` at `n = 10⁶`, never above the
explicit finite-`n` bound of the proof; and simulated the outer loop with adversarial inner
oracles in about 17 000 runs without a violation (with the closure rule of the first draft,
2 940 of 2 940 runs in the affected parameter range return a false bracket).  At small
sizes no level is ever left as negligible — that branch needs roughly `n_o h ≳ ln(2Je²)` — so a
small simulation must say which branches it exercised (harness XV.3 reaches it with a steep
slope and reports the counts).  **Nothing here is an algorithm one would run.**  With the constants of the proof
(and expectations in place of counts) the two-level algorithm overtakes the two-sample
bracket of Proposition 11.46 on the zero function, at `u = 1` and the accuracy rate `ε*/4`,
between `n = 2000` and `n = 5000` — where either needs more than `e^{70}` evaluations (benchmark
B13).  Numerically, at `u = 1` and a small accuracy, `T_k/θ_na = 0.50, 0.36, 0.32, 0.29, 0.28, 0.274,
0.271` for `k = 2, 3, 4, 5, 7, 10, 14` levels, against `θ_hint/θ_na = 0.268` (B13; at half the threshold
two levels already give `0.76` against `0.74`).
(2) Extensive accuracies only (`ε = ε₁n`, `0 < ε₁ < ε*`): the brackets have accuracy `gn + O(log n)`.
At a bounded accuracy the non-adaptive exponent is `a` (Theorem 11.44) and the hinted one `h`;
the adaptive exponent at accuracy `ε₁n` tends to `h` as `ε₁ → 0`, but at `ε = O(1)` it is only
known to lie between `h` and `a`.
(3) The cube, with the uniform reference measure and a class defined by one constant.  The
proof uses three things: the tail lemma (Harper's theorem) on subcubes; the fact that fibre
averages of a Lipschitz function are Lipschitz; and the **additivity of the Hamming distance
over blocks of coordinates**, by which a block of `φn` coordinates carries a problem of the
same kind and of size `φn` — this is what makes the outer sample cheap.  The analysis of the
recursion (Theorem 11.53) is abstract and would apply to any pair of exponent functions with
the identity (11.18.1), which only says that the hardest pair of instances for a
non-adaptive sample has all its mass on the set the sample has not seen.  But the third
ingredient is special, and so is the fact that on the cube every query point is a typical
point.  The small-slope limit of the two exponent functions, `(1 − √e)²` and `(1 − e)²/4`, looks
like a statement about Lipschitz functions on Gaussian space, and it is **not** one: there
a block of coordinates has the same Euclidean Lipschitz constant as the whole space, so
the two-level construction gains nothing as it stands; and the extremal sets of the
isoperimetric inequality are half-spaces, which an algorithm can detect with a few
evaluations far from the bulk, so that even the hinted lower bound does not transfer.
Nothing is claimed for continuous spaces.  Product reference measures and larger alphabets
with a weighted Hamming distance have all three ingredients at the exponential scale
(asymptotic isoperimetry of product measures; from memory, not read) and are not worked
out.
(4) Worst case over the class.  One consequence concerns algorithms *with* a hint: an
algorithm with a hint may ignore it, so by Theorem 11.54 no instance of the class costs a
hinted algorithm more than `exp(nθ_hint(ε₁) + o(n))` — **the zero function is the hardest
instance with a hint**, at the exponential scale (for additive instances this also follows
from the game formula of Theorem 11.27: workstream H).  What remains open is the comparison
instance by instance in the other direction: at an instance that is cheap with a hint — a
cone costs two evaluations — the nested algorithm is not shown to be cheap, and whether
some adaptive algorithm without a hint matches the hinted cost at *every* instance, up to
`e^{o(n)}`, is not known.
(5) The time-honoured relatives of the algorithm — nested sampling, multilevel splitting,
nested simulation with adaptive allocation — estimate the same layer-cake decomposition
with a constrained sampler or with mean-square criteria.  What was not found in print
(abstracts only): a certified one-sided version, the use of an isoperimetric tail lemma to
close the ladder, and a recursion for worst-case exponents.  In information-based complexity
adaption is known not to help for linear problems on convex symmetric classes and to help
by polynomial factors in some randomised linear settings (Heinrich 2024; Kunsch–Novak–Wnuk
2024).  *Where our problem sits* (Scientific Discovery Division, SCI-REV-0004, observation
(b); our earlier note in `prior_art/L7` — "`ln Z` is not linear, so 'adaption does not help'
does not apply" — was not the accurate explanation): in the weights `w = e^{−ψ}` the solution
operator `A(w) = E_π w` **is linear** and the class is a **convex cone**; what takes the
problem out of the reach of those theorems is that the class is **not symmetric**, the
error is **relative**, and the information is standard (function values).  For such
problems adaption is known to help by factors polynomial in the cardinality (Novak 1995,
as quoted by Krieg–Novak–Ullrich 2025; not read by us), and in these units the shear law of
§11.21 says how much here: the error factor of the best non-adaptive method with `N`
evaluations is `N^{1+o(1)}` times that of the best adaptive one, for `N ≤ e^{nh}` — **the adaption
gain equals the cardinality**.  The pattern "learn where to look, then verify" of §11.10
and of this section is the explore–verify scheme of Karnin (2016) and the
identification-as-cheap-as-verification phenomenon of Garivier–Kaufmann (2016), in
another regime (theirs: noisy observations, confidence `δ → 0`; here: exact evaluations,
fixed `δ`, exponents in `n`).  **That adaption can remove an exponential barrier of non-adaptive randomised methods
is not new**: Mathé–Novak (2007) — whose method gives the lower bound of §11.16 — show it for
integration against an unknown log-concave density with Lipschitz logarithm, by a
Metropolis walk ("the curse of dimension (for nonadaptive methods) can be broken by
adaption"), and zero finding (Sikorski 1982) is the textbook example for a nonlinear
problem.  What was not found: the exact exponents on a Hamming–Lipschitz class without
concavity and without a Markov chain, their coincidence with the hinted exponent, and the
recursion.  All of this is at the level of abstracts and search summaries; see
`prior_art/L7_query_complexity.md`.

*What the referee checked* (`reviews/R7_referee_report.md`).  Re-derived every line of Theorem
11.52 (good event and its probability, validity, width, termination, sample sizes, the
count, the cost sum); found the closure gap independently; closed the abort rule and the
induction on paper; compiled the Lean file and printed its axioms; verified by hand that
the functions of the cube satisfy the hypotheses of the abstract theorem, and the "≥" half
of Theorem 11.53(b) — both have since been machine-checked (`CubeHintPair.lean`); iterated the
recursion with own code to 64 levels (the excess over `θ_hint` halves with the grid spacing: a
discretisation artefact); ran the radial algorithm on full cubes.  *Not checked:* the algorithm end to end with real inner brackets, or with
three nested levels; non-radial outer landscapes in the evaluation of the cost (the referee
argues that only the law of the fibre averages matters); the uniformity of the `o(n)` terms
through `k` levels other than on paper; Theorems 11.25(a), 11.44, 11.45 and Proposition 11.46
beyond their statements; prior art beyond abstracts.  **The number of evaluations of the
algorithm therefore rests on a paper proof read by two parties and on numerical evidence
up to `n = 10⁶`, not on a machine check.**

### 11.19 Every bounded accuracy: the adaptive exponent without a hint is the hinted one

Theorem 11.54 is a statement about extensive accuracies `ε = ε₁n`.  The two-level algorithm
behind it loses a factor `4eJ + 3 = O(n)` in the ratio of its bracket at every level —
invisible at an extensive accuracy, fatal at a bounded one — and its closure test compares the
tail with the mass certified at *one* level.  What happens at a fixed accuracy `ε` was open
(§12 item 2(d) of the previous checkpoint): with a hint the exponent is
`h = θ_hint(0) = KL(Λ₁/u‖½)` (Theorem 11.25(d)); non-adaptive algorithms have
`a = KL(p_u‖½) > h` (Theorem 11.45); adaptive ones without a hint were only known to lie between.
Workstream K (`docs/workstreams/K_REPORT.md`) settles it: **the exponent is `h`, at every fixed
accuracy and down to accuracies `e^{-o(n)}`.**

**Status of this section.**  Paper proofs with explicit constants by workstream K, in full in
its report (§§2–4 there); read line by line by the coordinator; **refereed (R8,
`reviews/R8_referee_report.md`): "proved" — the referee re-derived the whole chain line by
line and found no critical and no major error; its ten minor points are corrected in the
text below** (see "What the referee checked" at the end of the section).  The theorems rest
on Harper's vertex-isoperimetric theorem, the binomial median and Chernoff–Hoeffding
bounds, which are cited, and on Theorems 11.25(a) and 11.53, which are machine-checked.
Machine-checked here (`BoundedAccuracy.lean`): the algebra of the bracket and of the count
(four lemmas), the iteration of the final theorem, and the exact recursion of §11.18 —
defined in Lean, with every hypothesis of the convergence theorem proved for it.  Not
machine-checked: the algorithm, its events, the Harper term, the closing radius, sample
sizes, termination, the cost, the tail lemmas, Harper's theorem.

*Notation.*  On an outer cube `Q_m`: `E_r(m) = Σ_{j≤r} C(m,j)(e^{u(r+1−j)} − 1)` (the constant of the
upper tail lemma 11.43(b): if `{W > t}` has at most `|B(m,r)|` points, `r ≤ m−1`, then
`E(W − t)₊ ≤ t·2^{-m}E_r(m)`), `T_m(k) = Σ_j C(m,j)e^{-u(j−k)₊}` (the constant of the lower tail lemma
11.43(c): if `{W ≥ t}` has at least `|B(m,k)|` points, then `E min(W, t) ≥ t·2^{-m}T_m(k)`);
`c_η = (1−η)/(1+η)`; and the two ratios

    Γ̃(r) = E_r(m)/|B(m, r−1)|   (Γ̃(0) = e^u − 1),        Γ″(r) = E_r(m)/T_m(κ(r)),

`κ(r)` the largest `k ≥ 0` with `|B(m,k)| ≤ max{1, c_η|B(m, r−1)|}`.  `Γ̃` is the *one-sided* ratio of
Theorem 11.52 (tail against the mass of the level itself); `Γ″` is *two-sided* (tail against the
Harper lower bound for the whole mean).

**Lemma 11.55 (where a bounded ratio can be certified) [P; workstream K, Lemma K.4; checked on
exact tables for `m ≤ 12 800` by the workstream and for `m ≤ 400` in exact arithmetic by the
coordinator].**  Let `m ≥ 1`, `0 < η ≤ ½`, `m₀ = ⌈u^{-1} ln(1/c_η)⌉`.
(a) `Γ̃(r) ≤ 2e^u·m` for `0 ≤ r ≤ p_u(m+1)`.  It is never small for `r ≥ 1`:
`min_{r≥1} Γ̃(r) = 4e^u(e^u−1)(1−o(1))` (numerical; slightly below the limit at finite `m`, and
`Γ̃(0) = e^u − 1`), and `Γ̃(⌊p_u m⌋) ≍ √m` (numerical; `≈ 2.6√m` at `u = 1`).
(b) For `0 ≤ r ≤ p_u m`:  `Γ″(r) ≤ 2e^{u(m₀+2)}·P(Bin(m, p_u) ≤ r) ≤ 2e^{u(m₀+2)}·exp(−2(p_u m − r)²/m)`.
(c) Hence for every constant `θ > 0`: `Γ″(r) ≤ θ` for all `r ≤ p_u m − √((m/2)ln(2e^{u(m₀+2)}/θ))`, and
the corresponding ball has `2^{-m}|B(m,r)| ≥ exp(−m·a − O(√m))`.
*Proof idea.*  (a) Ratios of consecutive binomial coefficients are at most `e^{-u}` up to
`p_u(m+1)`, so `E_r ≤ (r+1)e^uC(m,r)`.  (b) `C(m,j)e^{-uj} = (1+e^{-u})^m P(Bin(m,p_u) = j)` turns `E_r` into a
lower binomial tail and `T_m(k)` into an upper one, which is at least `½` for `k ≤ p_u m` (median of
the binomial law); `κ(r) ≥ r − 1 − m₀`; Hoeffding.  ∎

So the one-sided test cannot certify a bounded ratio at radii near `p_u m` — which is where
the outer sample has the exponent `φa` — and the two-sided one can.  (The coordinator's
sketch of this step, a "window" of radii in which the one-sided test succeeds, was wrong as
a mechanism: `DEAD_ENDS.md`, D46.)

**Theorem 11.56 (one more level, at the price of an arbitrarily small constant) [P, refereed (R8);
workstream K, Theorem K1; the algebra of the width and of the count V].**  *Algorithm 2L⁺* is the two-level algorithm of Theorem
11.52 with four changes (complete text and all constants: `K_REPORT.md` §2.2):

1. the lower end is `max{ℓ, Σ}`, `Σ = Σ_{populated i}(1 − e^{-λ})e^{-b}s_i·p̲_i` — a lower Riemann sum of the
   layer cake over *all* populated levels (`certified_lower_sum_le_mean` **[V]**), not the
   largest single term;
2. at every populated level the running bound is also raised to the **Harper term**
   `ℓ ≥ s_je^{-b}·2^{-n_o}T_{n_o}(k)`, `k` the largest radius with `|B(n_o,k)| ≤ max{1, 2^{n_o}p̲}` (Lemma 11.43(c)
   on the outer cube: a certified *fraction* of fibres above a level forces mass around them);
3. the negligibility threshold is `M_j^neg = ν·s_j/(ℓe^b)` with `ν = K·ν₀`,
   `ν₀ = (1−η)^{-1}max{(J+1)(e^λ−1)/η′, ν₁}` and a free `ν₁ ≥ 1`;
4. Chernoff factors `1 ± η` instead of `2^{±1}`, levels `s_j = s₀e^{jλ}` instead of `s₀e^j`, and the
   initial bound `ℓ = e^{-ψ₀}((1+e^{-u})/2)^n` (so that `s₀ ≤ (2p_u)^n ℓ`).

Let `0 < λ ≤ 1`, `0 < η ≤ ½`, `0 < η′ ≤ 1`, `θ > 0`, `ν₁ ≥ 1`, tolerance `b`, inner bracket procedures of
accuracies `2un_i = x₀ > x₁ > … > x_L`, `x_L ≤ b`, with costs `C_l` and failure probability
`δ′ = δ/(4LM̄)`.  Then Algorithm 2L⁺ is a bracket procedure for dimension `n` with failure
probability `δ`,

    accuracy  ln[ (2p_u)^n + e^b·( e^λ(1+η)/(1−η) + η′ + θ ) ],
    cost      C_max = 1 + 2M̄ + Σ_{l=1}^{L} min{ 2M̄ , (J+1)·cnt(x_{l−1}) }·C_l,

where `J = ⌈(2un + b + n_o ln 2)/λ⌉`, `K = O(η^{-2} ln(nL/δ))`, `cnt(x) = max{K, 2(1+η)²(1−η)^{-1}e^λ·ν·e^x}`,
`M̄ = 2(1+η)e^λν₀·K/((1−η)π†)`, `π† = 2^{-n_o}|B(n_o, r†)|`, and `r†` is the largest radius `≤ n_o − 1` such that
`Γ̃(r′) ≤ θ(1−η)ν₀` and `min{Γ̃(r′)/c_η, Γ″(r′)} ≤ θ` for all `r′ ≤ r†`.  (The cost bound holds always:
before every inner call the algorithm checks that the call does not take the number of
queries beyond `C_max`, and aborts with the trivial bracket otherwise; a pair with `L > U`,
which can only arise off the good event, is replaced by the trivial bracket as well —
referee R8, m1.)  On an event of probability
`≥ 1 − δ`: no abort; every certificate is true; and for every level reached and every `x > 0`
the count below holds.  *For every run, on or off that event* (the referee's observation):
every level that is left has closing radius above `r†`, every sample has at most `M̄` points,
and a bracket returned through the closure test has the stated width.  The count:

    M_j^neg · P(W > s_je^{-x})  ≤  (1+η)(1−η)^{-1}e^λ · ν · e^x        (the count; `close_points_bound'` [V]).

*What the statement says.*  The tolerance `b` is the accuracy of the finest inner bracket, and
it is the *only* quantity tied to it: one level adds `ln(e^λ(1+η)/(1−η) + η′ + θ) + o(1)` to the
accuracy, as small as one likes, at the price of factors `1/λ, 1/η², 1/η′, 1/θ` in the
polynomial part of the cost.  Everything exponential is in `1/π†` (the outer sample) and in
`e^{x_{l−1}}C_l` (the points within a factor `e^{x_{l−1}}` of a level, each of which needs an inner
bracket of accuracy `x_l`).
*Proof* (`K_REPORT.md` §2.4, nine steps; the architecture of Theorem 11.52).  Good event: every
potential inner call valid; Chernoff at the fixed thresholds `s_j`, `s_je^{-b}`, `s_je^{-x_l}` and the
sizes `K2^m`.  Validity: upper end by the layer cake and Lemma 11.43(b); lower end by the
Riemann sum, Markov and Lemma 11.43(c).  Width: four terms — `s₀ ≤ (2p_u)^nL`; populated levels
`≤ c_η^{-1}e^{λ+b}Σ` (`populated_part_le` **[V]**); negligible levels `≤ η′e^bℓ` by the threshold; tail
`≤ θe^bℓ` by the test (`width_le` **[V]**).  Closing radius: if a populated level fails the test,
then `min{Γ̃/c_η, Γ″} > θ` at its radius (the first through `ℓ ≥ s_je^{-b}p̲`, the second through the
Harper term); if a negligible one fails, `Γ̃ > θ(1−η)ν₀`.  Sample sizes: a level left as
negligible has `M < K/((1−η)π†)`, and the threshold of the next level is at most `e^λ` times
that, or — after a populated level — at most `ν e^λ/(c_ηπ†)`.  The count: the tolerance of "high"
and the tolerance of "negligible" are the same `b` and cancel, as in Theorem 11.52.
Termination at level `J` because nothing is high there and the threshold forces an empty
tail.  ∎

*Remark (the sample-size cap can be lowered to a constant multiple of `M†`)* **[P; coordinator,
in answer to the Computational Research Division, ENG-RES-0008; not refereed; harness
XVI.4].**  With `M† := K/((1−η)π†)`, the cap of the theorem is `M̄ = 2(1+η)e^λν₀M†`.  The division
found that in more than seven million runs, under a search over instances and inner
behaviours, no sample exceeded `1.8·M†`, while `M̄/M†` is of order `ν₀ ≈ J/η′` (`ln ν₀` between `8.9` and
`17.3` in its cells), and asked whether `M ≤ c·M†` can be proved.  It can.  Let `Δ := ⌈λ/u⌉`,
`π‡ := 2^{-n_o}|B(n_o, r† − Δ)|` and `M‡ := K/((1−η)π‡)` (`M‡ := K·2^{n_o}/(1−η)` if `r† < Δ`).  **In every run
every sample is `K` or has fewer than `2·max{e^λM†, M‡}` points**, and
`M‡/M† = |B(n_o, r†)|/|B(n_o, r†−Δ)| ≤ ((n_o+1)/(r†−Δ+1))^Δ`, which tends to `((1−ρ)/ρ)^Δ` when `r†/n_o → ρ`: at
a bounded accuracy, where `r† = p_un_o − O(√n_o)`, the cap is `2e^{uΔ}(1+o(1))·M†` (`2e·M†` for `u = 1`,
`λ ≤ 1`).  So `M̄` may be replaced by `2max{e^λM†, M‡}` in `C_max`, `m_max` and `δ′`: the first term of
`C_max` loses a factor of order `ν₀`; no exponent changes.
*Proof.*  `M` is doubled only after a pass that is unpopulated, fails the closure test and
has `M < M_j^neg`.  (1) *After a negligible level:* `M_j^neg ≤ e^λM_{j−1}^neg ≤ e^λM_{j−1} < e^λM†` (the
running bound does not decrease, and a negligible level that is left has `M < M†`), so
every sample of level `j` is below `2e^λM†`.  (2) *After a populated level `j − 1`* (level `0`
is populated at `M = K`): that level was left, so its closing radius exceeded `r†`; hence
`p̲_{j−1} > c_ηπ†`, the radius of its Harper term is at least `κ(r†+1)`, and
`ℓ ≥ s_{j−1}e^{-b}·max{c_ηπ†, 2^{-n_o}T_{n_o}(κ(r†+1))}`.  At an unpopulated pass of level `j` with `M ≥ M‡`,
`q = K/((1−η)M) ≤ π‡`, so the closing radius is `r ≤ r† − Δ`; and `E_{r−1} ≤ e^{-u}E_r` for every `r ≥ 1`
(compare the two sums term by term: `e^{u(r−i)} − 1 ≤ e^{-u}(e^{u(r+1−i)} − 1)`), so
`tail = s_j2^{-n_o}E_r ≤ s_{j−1}e^{λ−uΔ}·2^{-n_o}E_{r†} ≤ s_{j−1}·2^{-n_o}E_{r†}`.  By the definition of `r†`, either
`Γ″(r†) ≤ θ`, that is `E_{r†} ≤ θT_{n_o}(κ(r†)) ≤ θT_{n_o}(κ(r†+1))`, or `Γ̃(r†) ≤ c_ηθ`, that is
`E_{r†} ≤ c_ηθ|B(n_o, r†−1)| ≤ c_ηθ·2^{n_o}π†`; in both cases `tail ≤ θe^bℓ` and the algorithm stops.  (If
`r† < Δ`: a pass with `2^{n_o}q < 1` has an empty tail.)  So at level `j` the size is doubled
only below `M‡`.  ∎
In the constants of Theorem 11.52 the same argument gives **`M < 2e·M†` in place of `8Je²M†`**
(an unpopulated pass with `M ≥ max{M†, M_j^neg/(4Je)}` passes the closure test, and
`M_j^neg ≤ 4Je²M†`), so the first branch of the minimum in its cost bound loses the factor
`4Je`.  In the harness the cap is attained up to `9 %` (a sample of `3.7·M†` at `n_o = 24`, `u = ½`,
`λ = ½`, on a landscape "plateau, then cone", where the cap is `4.06·M†` and `M̄ = 627·M†`), so
the constant cannot be improved much by this argument; that the division's search stayed
below `1.8·M†` reflects its instances and its parameters, not a better bound.

*Remark (for the outer loop, radial landscapes are almost the whole class)* **[P; Computational
Research Division, ENG-RES-0008 §5; checked by us].**  The outer loop sees an instance only
through the law of the fibre averages, i.e. through the tail function `m(t) = |{W > t}|` on
the outer cube.  For a `u`-Lipschitz landscape `m` is nonincreasing and right-continuous
with `m(te^{-u}) ≥ ∂(m(t))`, `∂(k)` the size of the closed neighbourhood of the initial segment
of size `k` of the simplicial order (the neighbourhood of `{W > t}` lies in `{W > te^{-u}}`, and
Harper's theorem); conversely every such function is the tail function of a `u`-Lipschitz
landscape whose level sets are initial segments.  So with a fixed inner behaviour the
mean run on any instance is the mean run on an instance whose outer level sets are
initial segments, and monotone radial profiles — those with whole balls — differ from the
general case only by partial shells.  Our request THY-REQ-0001 had called radial
instances "a small subfamily of the class"; for the outer loop that was wrong.

With `λ = 1`, `η = ½`, `η′ = 1`, `ν₁ = 1` and `θ = e^{gn−b} − (3e+1) − (2p_u)^ne^{-b}` this is Theorem 11.52 again,
with accuracy *exactly* `gn` instead of `gn + O(log n)` (Corollary K1.b of the report), and the
levels of Theorem 11.54 can be assembled from it by asking each inner family only for an
accuracy rate slightly above its nominal one (Proposition E there) — an induction that
needs no left limits.

**Proposition 11.57 (exponents at a bounded accuracy) [P; workstream K, Propositions K0, K5 and
Theorem K2].**  Extend exponent functions to accuracy zero: `T(0)` is an exponent of a family of
bracket procedures *at bounded accuracy* if `limsup_d d^{-1} ln C(d, x, e^{-cd}) ≤ T(0)` for every fixed
`x > 0` and `c > 0`.
(a) *Base family.*  The two-sample bracket with the threshold at the `K`-th largest weight of
the first sample, closed by both tail lemmas, has ratio at most
`((1+η)/(1−η))·(1 + Γ″(r̂))`; with Lemma 11.55 its cost is `exp(d·a + O(√d))` at every fixed
accuracy: `T₁(0) = a`, and `T₁ = θ_na` on `(0, ∞)`.  (The reason given for this in the earlier text —
a bound `3 + 12Γ(r)` — does not work: that ratio is not bounded up to `p_u d`.)
(b) *One more level.*  If a family has the exponent function `T` on `[0, ∞)`, then for every
`0 < φ < 1` and rates `2u = ξ₀ > ξ₁ > … > ξ_{L−1} > 0` there is a family with the exponent function
`min(T(ξ), T′(0))` at `ξ > 0` (a procedure of bounded accuracy also serves every extensive one;
the workstream's "`T′ = T` on `(0, ∞)`" was not nonincreasing — referee R8, m2) and

    T′(0) ≤ max{ φa ,  max_{1≤l≤L−1} [ min(φa, (1−φ)ξ_{l−1}) + (1−φ)T(ξ_l) ] ,  min(φa, (1−φ)ξ_{L−1}) + (1−φ)T(0) }.

With a fine ladder the right-hand side is `sup_{γ≥0}[min(γ, φa) + (1−φ)T(γ/(1−φ))]` up to `ε′` — the
bracket of (11.18.2) at `g = β = 0` —, and with two rungs it is at most
`max{ φa + (1−φ)T(ξ) , (1−φ)(ξ + T(0)) }`.  (Theorem 11.56 with `b = x/2`,
`λ = η = η′ = θ = min(x/12, ⅓)`, `ν₁ = 2e^un_o/θ`, and Lemma 11.55(c): `r† ≥ p_un_o − O(√n_o)`, so
`M̄ = e^{φan + O(√n)}`.)  The same holds uniformly for accuracies `x_n → 0` with `ln(1/x_n) = o(n)`.
(c) *The necessary condition holds at accuracy zero:* if `T ≥ θ_hint` on `(0, ∞)`, then
`sup_{γ≥0}[min(γ, φa) + (1−φ)T(γ/(1−φ))] ≥ h` for every `φ` (take `γ = φa`: `φp_u + (1−φ)ρ_i = Λ₁/u` for the
inner radius `ρ_i = (Λ₁ + φa/(1−φ))/u`, and `KL(·‖½)` is convex).  No level undercuts the lower
bound.

**Theorem 11.58 (the adaptive exponent at every bounded accuracy) [P, refereed (R8): Theorems
11.25(a) and 11.53 (machine-checked), 11.56 and Proposition 11.57 (paper), Harper's theorem,
the binomial median and Chernoff–Hoeffding bounds (cited); workstream K, Theorem K3 and
Corollary K3′].**  For every `u > 0`,
every fixed `ε > 0` and `0 < δ < ½`, the least number of evaluations with which a randomised
adaptive algorithm without a hint is `(ε/2, δ)`-correct on all of `L_u(Q_n)` — in the worst case
over the class, and likewise in expectation — is

    exp( n·h + o(n) ),        h = KL(Λ₁/u ‖ ½).

The same holds for every sequence of accuracies `ε_n = o(n)` with `ln(1/ε_n) = o(n)` (no limit of
`ε_n` need exist).
*Proof.*  Lower bound: Theorem 11.25(a),(d), an algorithm without a hint being one with a
hint.  Upper bound: fix `0 < η < h`, put `φ = min(½, η/a)`, `ξ = min(ε*/2, φη)`.  There is a family whose
extensive exponent at the rate `ξ` is at most `h + η`: Theorem 11.53 for the exact recursion
(`exactRec_reaches_hint` **[V]**) gives a level `k` with `T_k(ξ/2) < θ_hint(ξ/2) + η/2 ≤ h + η/2`, and
the assembly gives a family with that exponent at the rate `ξ`.  Take the cheaper of it and
the base family (`t₀ ≤ a`) and apply Proposition 11.57(b) with two rungs `m` times:

    t_{m+1} ≤ max{ φa + (1−φ)(h + η) , (1−φ)(ξ + t_m) } ≤ max{ h + 2η , (1−φ)t_m + φη },

so `t_m ≤ η + max{h + η, (1−φ)^m a}` (`two_rung_bound` **[V]**), which is at most `h + 2η` for
`m ≥ ln(a/h)/φ`.  The midpoint of the logarithms of a bracket of ratio `e^ε` is `(ε/2, δ)`-correct.  ∎

*The picture for the cube class, complete at the exponential scale down to accuracies
`e^{-o(n)}`:*

| accuracy | non-adaptive | adaptive without a hint `=` with a hint at the hardest instance |
|---|---|---|
| `ε₁n`, `ε₁ ≥ ε*` | `0` | `0` |
| `ε₁n`, `0 < ε₁ < ε*` | `θ_na(ε₁)` (11.44, 11.45) | `θ_hint(ε₁)` (11.54) |
| `o(n)` and bounded below; in particular every fixed `ε` | `a` | `h` (**11.58**) |
| `→ 0` with `ln(1/ε) = o(n)` | `a` (lower bound: Theorem 11.45 with dips of radius `R`, `R/n → p_u`, since `D_R > ε_n` as soon as `KL(R/n‖p_u) < ln(1/ε_n)/n + o(1)`) | `h` (**11.58**) |
| `e^{-λn}` | not studied | open (with a hint: rows 4–6 of Theorem 11.25(d)) |

*Remarks.*  (1) **Depth is necessary for this family of algorithms, and bounded accuracy is
where the recursion converges most slowly.**  With `τ_k` the exponent of `k` levels at bounded
accuracy (`τ₁ = a`, `τ_{k+1} = inf_φ sup_{γ≥0}[min(γ, φa) + (1−φ)T_k(γ/(1−φ))]`):
`τ_k/a = 0.5006, 0.361, 0.311, 0.290, 0.280, …, 0.2631` for `k = 2, 3, 4, 5, 6, …, 40` at `u = 1`, against
`h/a = 0.2627`; `(τ_k − h)/a ≈ 0.65/k²`; `max_g(T_k − θ_hint)(g) = τ_k − h` **[N; workstream; `τ₂` re-computed by
the coordinator]**.  The algorithm of the proof has about `ln(a/h)·a/η` bounded levels on top of
an extensive family: nothing one would run.  *At the flat instance, with the outer
fraction `φ` tuned for that instance,* the exact cost of two
levels at accuracy `0.87` is `ln(cost)/(na) = 1.70, 0.70, 0.55, 0.52, 0.51` for
`n = 250, 10³, 4·10³, 1.6·10⁴, 6.4·10⁴` (limit `τ₂/a`), against `1.93, 1.35, 1.15, 1.07, 1.03` for the plain
bracket and never below the hinted lower bound.  **These are best-case numbers: the flat
instance is where the lower bound for every algorithm is proved, not where this
algorithm works hardest** (Computational Research Division, ENG-RES-0008: exact counts
for Algorithm 2L⁺ under a search over instances and inner behaviours; in `7 095 840` mean
runs no claim of Theorem 11.56 was violated).  With the flat-tuned `φ` a radial instance
"flat bulk with a slightly supercritical dip", or a cone, costs `e^{71}` times more
evaluations at `n = 1000` — as much as the plain bracket — and `e^{513}` times more at `n = 64 000`
(`u = 1`).  Tuned against the worst instance the best outer fraction is between `0.50` and
`0.60` at every size (`0.50` from `n = 4000` on), and the cost is `ln(cost)/(na) = 1.04` at `n = 1000`
and `0.537` at `n = 64 000` instead of `0.70` and `0.512`; the excess over the exponent claimed
for the same `φ` and ladder decreases with `n`, consistently with the `O(√n)` correction of
the theorem, and is below `0.01` in exponent units from `n = 32 000` on.  **So two levels beat
the plain bracket from `n ≈ 500` on at `u = 1` (from `n ≈ 250` at the flat instance; from
`n ≈ 1000` if `φ` is left at its flat-tuned value) and from `n ≈ 2000` on at `u = ½`**, where
either needs more than `e^{45}` evaluations.  The limit `τ₂` is a worst-case exponent and is
not affected; the three-level numbers at the flat instance quoted in THY-MSG-0007 carry
the same caveat, and no worst case has been computed for three levels.
(2) **Below the exponential scale nothing is known.**  With a hint the cost at the zero
function is `2ⁿ/|B(n, k*)|` up to a polynomial factor — exactly `2ⁿ/|D_min|` up to the factor
`1 − 2δ`, with `D_min` the complement of the largest initial segment of the simplicial order that
is still sensitive (Harper; observed and verified by exhaustive search for `n ≤ 4` by the
Computational Research Division, ENG-RES-0006).  Without a hint the upper bound is
`e^{nh + o(n)}` with an unquantified `o(n)` (heuristically not better than `n^{3/4}`: each bounded
level loses `e^{O(√n)}`, and `η → 0` needs `≈ 1/η` levels).  Whether `e^{nh + O(√n)}` or even
`poly(n)·2ⁿ/|B(n,k*)|` can be reached without a hint, and whether a restricted class
(a bounded number of levels, or of rounds of adaptivity) has a lower bound matching `τ_k`, is
open.  (For rounds see §11.24: two rounds lie strictly between `h` and `a`; no lower bound
matching the level values is known.)
(3) Remark (4) of §11.18 extends: at the exponential scale a hint is worth nothing to an
adaptive algorithm at any accuracy with `ln(1/ε) = o(n)`, and the zero function is the hardest
instance with a hint there too.  The comparison instance by instance is as open as before.
(4) The new ingredient is the *lower* isoperimetric bound, used inside the algorithm.  It is
Harper's theorem on the outer sub-cube again, so the remark on other spaces (§11.18, (3))
is unchanged.

*Falsification harness.*  XVI.1 (Lemma 11.55 on exact tables), XVI.2 (the level at accuracy
zero: no undercut, the two-rung iteration), XVI.3 (the coordinator's own implementation of
the outer loop of Algorithm 2L⁺ with the constants of the theorem and a simulated inner
oracle: validity, width, certificates, closing radius, sample sizes and the count, on small
cubes and on radial landscapes); twelve mutations, all detected.

*Machine-checked* (`BoundedAccuracy.lean`).  The exact recursion: `exactRec` (definition),
`stepLE_exact`, `Rstep_anti`, `exactRec_props`, `exactRec_reaches_hint`; the lower barrier
`exactRec_ge_hint` and the convergence `exactRec_tendsto_hint` (so Theorem 11.53 holds for the
recursion as defined, with no hypothesis).  At accuracy zero: `two_rung_bound` is the iteration
in the proof of Theorem 11.58; `bounded_iterates_lt`, `levels_reach_hint_at_zero`,
`cube_levels_reach_hint_at_zero` (consistency of the hypotheses:
`cube_levels_reach_hint_at_zero_consistent`) are the convergence `τ_k → h` of remark (1) for
abstract sequences — that the recursion at accuracy zero satisfies their two hypotheses
about `τ` is on paper.  The bracket:
`certified_lower_sum_le_mean`, `populated_part_le`, `close_points_bound'`, `width_le`.

*Numerical evidence* (workstream K; scripts and outputs in `experiments/workstreams/K/`).  The
outer loop of Algorithm 2L⁺ with the constants of the theorem and an adversarial simulated
inner oracle: 394 runs on enumerated cubes `Q_8 × Q_4` and radial landscapes `n_o ≤ 44`, and 1325
runs in the bounded regime on radial landscapes `n_o ≤ 600` with exact samples of up to
`4.6·10^{18}` outer points (864 levels left as negligible); every claim of Theorem 11.56 tested on
every run, no violation; five mutations (lower end without the sum; no Harper term; closure
at the whole-cube radius; threshold without `e^{-b}`; `q` without `1/(1−η)`) each detected.  The whole
algorithm with real inner two-sample brackets on `Q_12`–`Q_14`: 84 runs, `1.05·10⁷` inner brackets,
every bracket valid and within the width bound.  The outer loop in expectation on 17 radial
and 5 additive landscapes up to `n_o = 16 000`: 630 runs, no violation.  *Not exercised:* three
nested levels; non-radial outer landscapes with real fluctuations beyond `Q_8 × Q_4`; the cost
with inner costs at large `n` other than at the flat instance; the assembly over the levels
and the uniform version for `ε_n → 0` (the referee filled three of these gaps: see below).  Two
numerical traps are recorded in the report: a closing radius computed in floating point
for `q = 1` reproduces the closure gap of D45, and numpy's *multinomial* sampler loses the
far-tail cells at `n ≈ 2^{60}` (the workstream's remark that the binomial sampler fails as
well is false for the current generator interface — referee R8, m6).  A third, from the
referee: with the last inner accuracy exactly equal to the tolerance and a fibre average
exactly on a threshold, floating point can leave a point unclassified at the last rung;
use a generic ladder ratio or a tie rule.

*What the referee checked* (`reviews/R8_referee_report.md`; own code in
`experiments/reviews/R8/`, none of the workstream's).  Re-derived every step of Theorem 11.56
— good event and its probability, the Harper term and its radius, validity, width, closing
radius with all edge cases, sample sizes, the count, calls per rung, termination — of Lemma
11.55, the base bracket, the assembly over the levels (complete without left limits), the
level at bounded accuracy and the final iteration; read the Lean statements against the
paper (`exactRec` is the recursion (11.18.2), with no junk value of the infimum at positive
accuracies); checked that the lower bound has the exponent `h` in the three regimes.  Lemma
11.55 in exact rational arithmetic for `m ≤ 4000`.  Its own implementation of Algorithm 2L⁺
from the text: about 15 000 runs with an adversarial simulated oracle and the constants of
the theorem (non-radial cubes `n_o ≤ 9`, radial landscapes `n_o ≤ 520` with exact samples of
up to `2·10^{18}` points, the extensive regime with `θ ≤ e^{40}`, the bounded regime with all
constants down to `0.025`) — no claim violated, the good event never failed; 7 500 runs with
`K` reduced 8–40 times, where the events of the proof fail in up to 31 % of the runs — no
claim violated whenever they hold; five mutations detected on three engines.  With **real**
inner brackets: 475 two-level runs on `Q_12`, `Q_13`, and — for the first time — **three nested
levels** on `Q_9`, `Q_10` (16 outer and 9 920 middle runs, `2.3·10⁸` bottom brackets): every
bracket valid and within its certified width, no abort.  The exact cost at the flat instance
with real brackets, two levels (`ln(cost)/(na) = 0.514` at `n = 64 000`, `u = 1`) and **three
levels: `0.712, 0.460, 0.405, 0.379` at `n = 10³, 4·10³, 1.6·10⁴, 6.4·10⁴`** (limits
`τ₂/a = 0.500`, `τ₃/a = 0.361`; hinted lower bound `0.263`, never undercut) — the first evidence
at large `n` that a further level lowers the cost at a bounded accuracy, at the one instance
where the lower bound is proved; the same at target accuracies down to `0.05`.  *Not
checked:* the Lean proofs line by line; Harper's theorem and the binomial median in the
original papers; non-radial outer landscapes beyond `n_o = 9`; three levels at large `n`
other than at the flat instance, and four levels; accuracies tending to zero other than on
paper, for the base bracket and at the flat instance; the frequency of failure of the good
event from below (it never failed).  *Corrections made after the report:* the abort rule
and the exponent function of Proposition 11.57(b) (above); "never small" restricted to
`r ≥ 1`; the remark on numpy; labels that said "machine-checked core" where four algebraic
lemmas are meant; one line for the non-adaptive row of the table; D46 items 5, 6.
*Prior art added by the referee* (search summaries; one abstract): adaptive inner sampling by
distance to a threshold in nested simulation (Broadie–Du–Moallemi; Giles–Haji-Ali) — the idea
"refine a sample only as far as its distance to the level requires", with mean-square
criteria; extremal Lipschitz functions of deviation problems on the cube as distance
functions to Harper's sets (Bobkov–Houdré–Tetali; Dzindzalieta) — the mechanism of the tail
lemmas.

*Prior art.*  Searched by the workstream from search summaries only: relative-error
estimation of a mean from exactly observed samples (Dagum–Karp–Luby–Ross 2000), nested
sampling, multilevel splitting, level-set estimation with interval-valued evaluations.  Not
found at that depth: a certified bounded-ratio estimator of a mean from *bracketed* samples
with a ladder of levels, or the use of a lower isoperimetric bound to close such a ladder.
"Not found", not "new".

### 11.20 With a known part: a field changes the hardest instance and the right sampler

§§11.16–11.19 are about the uniform cube: no known part.  The first step beyond it is a
known part that is a field, `f(x) = θ|x|`, i.e. the `p`-biased product measure
`π = Bernoulli(p)^{⊗n}`, `θ = ln((1−p)/p)`, as reference.  §12 item 2(d) of the previous
checkpoints guessed that "product measures should be within reach" through the asymptotic
isoperimetry of a fixed product measure.  Workstream F (`docs/workstreams/F_REPORT.md`) shows
that this guess points at the wrong object, and gives the exponents.  **Everything carries
over with one change that matters: the reference of algorithms without a hint is not the
instance `g = 0`, and the sampling law is not the Gibbs measure `π` of the known part.**

**Status of this section: refereed (R9, `docs/reviews/R9_referee_report.md`; no critical
finding).**  Paper proofs by workstream F (in full in its report, §3); the coordinator
re-computed the central formulas with own code
(`experiments/coordinator_checks/f_spot_checks.py`).  The independent referee re-derived every
proof line by line and re-computed every formula and table with own code (22 scripts,
`experiments/reviews/R9/`).  Verdicts: **Theorem 11.61 (non-adaptive exponent) proved;
Theorem 11.63 (the isoperimetric statement — new, the only isoperimetric input, the critical
part) proved; Theorem 11.64 (adaptive exponent): lower bound proved for every `n`, upper bound
proved with two gaps in the written proof of the algorithmic part, both closed** — (M1) the
induction over the levels needs left limits in the accuracy and is the induction of Theorem
11.54, not the compressed sentence of the workstream's report; (M2) with a strong field
(`|θ| > u`) the union bound over inner calls of the one-level algorithm needs a smaller inner
failure probability.  Both repairs are written into the proof of Theorem 11.64 below; neither
changes an exponent.  Proposition 11.65(a), (c) proved; **the coordinator's proof of
Proposition 11.65(b) proved** (every step re-derived and tested).  Twelve minor findings, all
applied here (errata at the head of `docs/workstreams/F_REPORT.md`); the two that concern
statements made elsewhere: a finite-`n` side remark of the workstream was false in general,
and its table for single product samplers was inaccurate by up to 4 % (D47, item 5).
Machine-checked: the shift identity (`FieldShift.lean`, for a two-letter centre and interior
profiles); the convergence of the level recursion for *any* pair of exponent functions with
the abstract properties (`iterates_lt_hint_add`, `exactRec_reaches_hint_of_pair`, and for
every game function Theorem 11.66), the properties themselves being a paper proof here.
*Standard reached:* one careful independent paper check; of the algorithmic part nothing has
been simulated end to end with a field, and the `o(n)` of every upper bound that uses Theorem
11.63 is of the poor (typical-subset) kind — the proof gives `ω_n` of order `n^{-1/8}`, the
numerical evidence is `c·ln n/n`.

*Setting and notation.*  `q = 1 − p`, `u > 0`, class `L_u` of `u`-Lipschitz residuals `ψ` on `Q_n`,
`A(ψ) = E_π e^{-ψ}`, target `ln A`, accuracy `ε = ε₁n`.  One site: soft gaps
`Λ(0) = −ln(q + pe^{-u})`, `Λ(1) = −ln(p + qe^{-u})`, `Λ_m = (1−m)Λ(0) + mΛ(1)`.  A cone `u·d(·, s)` has the
product Gibbs law `π_s`.  For a centre `s` and a point `x` let `(S, X)` be a pair of letters
drawn from the empirical law of `(s_i, x_i)`: `m = P(S = 1)` is the type of the centre,
`P(X ≠ S)` the normalised distance, `P_X` the type of the point.  Additive instances
`ψ_γ = γ|x|`, `|γ| ≤ u`, `Z_γ = q + pe^{-γ}`.  The *game function* of `ψ_γ` (Theorem 11.27(c) for this
class) is `F(γ, t) = −ln val(K_t^γ)`, `K_t^γ(a, b) = exp(−t[u·1[a≠b] − Λ(b) − γa − ln Z_γ])`, and

    R_γ(e) = max_{0≤t≤1}[F(γ,t) − te],    R_0 := R_{γ=0},    F*(t) = max_{|γ|≤u} F(γ,t),    R^max(e) = max_{0≤t≤1}[F*(t) − te],
    E = sup_{0<t≤1} F*(t)/t,    h = R^max(0),    S(e) = e + R^max(e),    θ_na(x) = R^max(S^{-1}(x)),    a = θ_na(0+).

`v(κ) = max_{|γ|≤u}[−γκ − ln Z_γ]` is `KL(κ‖p)` on the window of Gibbs means of the additive
instances and is continued with slopes `±u` outside.  The **flat-histogram instance**

    ψ_H(x) = min_{|γ|≤u}[γ|x| + n ln Z_γ] = −n·v(|x|/n)

(the lower envelope of the normalised additive instances) is a member of `L_u`; its Gibbs
law `μ_H` is, up to a factor `n + 1`, uniform over the types of the window and uniform inside
each type class — the normalised-maximum-likelihood mixture of the tilted product measures.

**Theorem 11.59 (hinted exponents with a field; `g = 0` is not the hardest instance)
[(a) refereed earlier: Theorem 11.27 and workstream A; (b)–(d) P, workstream F, Theorem F2;
refereed (R9): proved].**
(a) For every `n` and `|γ| ≤ u`, every randomised algorithm that is `(ε/2, δ)`-correct on `L_u` —
with or without a hint, adaptive or not — makes at least `(1 − 2δ)e^{−tε + nF(γ,t)}` evaluations in
expectation at `ψ_γ`, for every `t ≥ 0`; with a hint `exp(nR_γ(ε₁) + o(n))` suffice there.
(b) *Closed form.*  With the total field `λ = θ + γ`, `λ_± = θ ± u` and `C(x) = 2cosh(x/2)`:

    F(γ,t) = ln{ [ sinh(t(λ₊−λ)/2)·C(λ₋)^t + sinh(t(λ−λ₋)/2)·C(λ₊)^t ] / sinh(tu) } − t·ln C(λ);

`F(γ,0) = F(γ,1) = 0` and `F(γ,t) ≤ 0` for `t ≥ 1`.
(c) *Max–min forms*, for `e ≥ 0`:

    R_0(e)   = max_m min{ I(S;X) : u·P(X≠S) − Λ_m ≤ e }  =  max_m [ h(m) − h((Λ_m + e)/u) ]₊ ,
    R^max(e) = max_m min{ I(S;X) : u·P(X≠S) − Λ_m + v(P_X) ≤ e } ,
    θ_na(x)  = max_m min{ I(S;X) : D(P_{X|S} ‖ π_s | P_S) ≤ x }            (x > 0),

so the hinted exponent at `g = 0` is that of Hamming balls around centres of an optimal type
`m* ≠ ½` (a rate–distortion function), and `a = max_m I_{π_s}(S;X)`.
(d) If `p ≠ ½`, then `∂F/∂γ(0,t) ≠ 0` for every `0 < t < 1` (sign of `p − ½`), hence `F* > F(0,·)` on
`(0,1)`, the class threshold `E` exceeds the threshold `E_0` of `g = 0`, and
**`R^max(e) > R_0(e)` for every `0 ≤ e < E`**: the hardest instance with a hint is an additive
instance `γ*|x|` whose residual partly cancels the field (`γ*θ < 0`: Proposition 11.65(b)).  For `p = ½` all three functions are those of §§11.16–11.18.

**Lemma 11.60 (the shift identity with a field) [V for a two-letter `S` and interior profiles;
the boundary cases by continuity, on paper] (`shift_identity`, `klBin_tilt`, `cone_rate_eq`,
`sphere_rate_eq`; workstream F, Theorem F3).**  For every joint law of `(S, X)`,

    D(P_{X|S} ‖ π_s | P_S)  =  I(S;X)  +  KL(P_X ‖ π)  +  u·P(X ≠ S)  −  Λ(P_S).

*Non-adaptive accuracy = exponent of the sample + hinted accuracy at `g = 0` + `KL(P_X‖π)`.*  In
the uniform case the optimal profile has `P_X = π` and the last term vanishes (the identity
of §11.18, `klBin_shift`).  With a field it does not: `u·P(X≠S) − Λ(P_S) + KL(P_X‖π)` is the hinted
accuracy of a *different* instance — a dip of the flat-histogram instance `H` — which is why
the identity `θ_na(e + θ_hint(e)) = θ_hint(e)` holds with `θ_hint := R^max` and **fails with `R_0`**
(a level recursion built on the pair `(θ_na, R_0)` falls 3 % of `a` below the lower bound
after ten levels at `p = 0.1`, `u = 2`: the necessary condition of D45 has power here).

**Theorem 11.61 (non-adaptive algorithms without a hint, with a field) [P; workstream F, Theorem
F4; (d) given Theorem 11.63; refereed (R9): proved].**  For `ψ ∈ L_u` and `0 < q < 1` let `ψ^{tr,q}` be `ψ` truncated at its
type-wise upper `q`-quantiles (weight `min(w, t_{|x|})`, `t_κ` the smallest value of `w` on the type
class `T_κ` above which `w` has density at most `q` there), and
`ε_n^{tr}(q) = sup_{ψ∈L_u} ln[A(ψ)/A(ψ^{tr,q})]`.
(a) *Type-wise quantiles are Lipschitz* **[V]** (`admissible_succ`, `admissible_pred`,
`truncate_lipschitz_insert`, `truncate_lipschitz_erase`, `truncate_ne_iff`): `t_{κ±1} ≤ e^u t_κ` (couple
adjacent type classes by flipping one coordinate — the local LYM inequality), so
`ψ^{tr,q} ∈ L_u`, and it differs from `ψ` on a set of density at most `q` in every type class.
This part does not involve the reference measure at all.
(b) *One extremal function bounds the complexity from both sides, for every `n`, with no
isoperimetry.*  If `ε < ε_n^{tr}(q)`, every non-adaptive `(ε/2, δ)`-correct algorithm makes at least
`(1 − 2δ)/q` evaluations (the pairs `(ψ∘σ, ψ^{tr,q}∘σ)` over random permutations `σ` in Theorem
11.45(a); **[V]** for every permutation-invariant class and target:
`symmetric_nonadaptive_queries_ge`, `truncated_weight_queries_ge`); conversely `M` uniform points from *each* type class with importance weights
`π(T_κ)` are accurate to `ε_n^{tr}(q) + O(1)` once `Mq ≳ log n`.
(c) `ε_n^{tr}(e^{−nθ}) ≥ n·min{D(P_{X|S}‖π_s|P_S) : I(S;X) ≤ θ + O(log n/n)} − O(log n)` for every centre
type (cones truncated at type-dependent radii), and (d) `ε_n^{tr}(e^{−nθ}) ≤ n·S((R^max)^{-1}(θ)) + o(n)`.
Hence **the exponent of non-adaptive algorithms is `θ_na(ε₁)`** for `0 < ε₁ < E`, attained by
sampling uniformly on every type class — equivalently, importance sampling from `μ_H`.
*Product samplers: worse at extensive accuracies, not at vanishing accuracy* **[lower bound:
P, elementary; the comparison with `θ_na` at extensive accuracies: numerical; the equality
at vanishing accuracy: P, an observation of the Scientific Discovery Division].**  A non-adaptive algorithm whose points are i.i.d. from one product measure
`Bernoulli(r)^{⊗n}` — plain Monte Carlo from `π` is `r = p` — makes at least
`(1 − 2δ)·exp(n·max(φ₀, φ₁)(ε₁) − O(log n))` evaluations, where for the constant centre `s ∈ {0ⁿ, 1ⁿ}`,
with `r_s` the sampler's and `η_s` the cone's Gibbs probability that a letter differs from the
centre, `φ_s(x) = KL(ρ‖r_s)` and `ρ ∈ (η_s, r_s)` solves `KL(ρ‖η_s) = x` (`φ_s = 0` if there is no such `ρ`).
(*Proof.*  The cone `u·d(·, s)` and its truncation `u·max(d(·, s), ρn)` are in `L_u`, differ only on
the ball of radius `ρn`, whose sampler measure is `e^{−nKL(ρ‖r_s) + O(log n)}`, and differ in `ln A` by
`nKL(ρ‖η_s) − O(log n)`, by the tilt identity `uρ + KL(ρ‖p_s) = Λ_s + KL(ρ‖η_s)` (`klBin_tilt`); an
algorithm none of whose points falls into the ball cannot tell them apart.  ∎  The referee
observed that the constant centres are the worst ones for a product sampler — objective and
constraint of the workstream's formula are linear in the centre type — so `max(φ₀, φ₁)` is that
formula in closed form.)  At vanishing accuracy this is `n^{-1}max_s KL(π_s‖π)` for plain Monte
Carlo — up to 2.9 times `a` in the table below — and at `(p, u, ε₁) = (0.1, 2, 0.05E)`, `(0.1, 2, 0.25E)`,
`(0.3, 1, 0.25E)` it is `0.2743`, `0.1430`, `0.0348` against `θ_na = 0.1020`, `0.0440`, `0.0243`; the best
single `r` gives `0.1033`, `0.0451`, `0.0244` there (referee; `0.1035`, `0.0453`, `0.0245` in the
coordinator's re-computation, `experiments/coordinator_checks/r9_product_sampler_check.py`):
**plain Monte Carlo from the Gibbs measure of the known part is exponentially worse; the best
single tilted product measure is worse by 0.5–3 % of the exponent in these examples.**  That
`min_r max(φ₀, φ₁) > θ_na` whenever `p ≠ ½` is not proved in general — and **at vanishing accuracy
it is false: there the two are equal** (SCI-REV-0004, observation (a); re-computed by us,
harness XVII.5).  The Gibbs laws of the cones are the output laws of the memoryless
channel `W(·|b)` = letter law of a cone whose centre has the letter `b`; `a = θ_na(0⁺) = max_m I(S; X)`
is its capacity; `max(φ₀, φ₁)(0⁺) = max_b KL(W(·|b)‖Bernoulli(r))`; and capacity = information
radius: the minimum over `r` is `a`, attained at the capacity-achieving *output* marginal
`r*` (`r* = 0.4308, 0.3607, 0.2225, 0.1124` against `p = 0.3775, 0.2689, 0.1192, 0.0474` at `u = 2`; it is
neither `p` nor the optimal centre type).  So the lower bound above does not separate
`Bernoulli(r*)^{⊗n}` from the type-stratified sample at vanishing — hence at every bounded —
accuracy, and at cone instances the sample size `e^{na}` suffices for it (Chatterjee–Diaconis
2018).  **A strict separation of product samplers from the flat histogram can only be a
statement about extensive accuracies.**  Whether `Bernoulli(r*)^{⊗n}` is exponent-optimal on
the whole class at bounded accuracy was listed here as open, and expected to need the tail
function of the reference `γ*|x|` (`γ* = logit p − logit r*`; the analogue of Theorem 11.63).
**It was closed by the Scientific Discovery Division: it is, for every `n`, and no tail
function is needed.**

**Proposition 11.61a (the product sampler with the capacity-achieving output marginal is
exponent-optimal at every bounded accuracy) [P; Proposition A1.1 of the Scientific Discovery
Division — SCI-RES-0001 §2, SCI-MSG-0011 §4; each step re-derived by us and checked by exact
enumeration, harness XVII.6; steps (i), (ii) machine-checked by that division for general
site classes (SCI-MSG-0014, its `Window.lean`; not adopted here), (iii), (iv) on paper].**
Let `a₀ = σ(logit p − u)`, `a₁ = σ(logit p + u)` be the letter laws of the two extreme cones
(`σ` the logistic function), `r*` the point with `KL(a₀‖r*) = KL(a₁‖r*)`, and `a` that common value
(the information radius of the two letter laws: the capacity `a = θ_na(0⁺)` above).  For every
`ψ ∈ L_u` with Gibbs law `ν_ψ ∝ πe^{−ψ}` and `Q = Bernoulli(r*)^{⊗n}`:
(i) every conditional law of a coordinate of `ν_ψ` given a prefix is Bernoulli with
parameter in `[a₀, a₁]` (the two partial sums differ by a factor in `[e^{−u}, e^{u}]`);
(ii) hence, by the chain rule and convexity, `KL(ν_ψ‖Q) ≤ n·max{KL(a₀‖r*), KL(a₁‖r*)} = na`, with
equality for the cones with constant centre;
(iii) the log-likelihood ratio `ln dν_ψ/dQ` is a sum of `n` terms with conditional means at
most `a` and ranges at most `2u` (because `r*` lies between `a₀` and `a₁`), so by the
Azuma–Hoeffding inequality `ν_ψ(ln dν_ψ/dQ > na + s) ≤ exp(−s²/(2nu²))`;
(iv) for `M` independent samples from `Q` and every `τ`, the importance-sampling estimate
`Â` of `A = E_πe^{−ψ}` satisfies `E|Â/A − 1| ≤ √(τ/M) + 2ν_ψ(dν_ψ/dQ > τ)` (truncate the density
ratio at `τ`: the truncated part has second moment at most `τ`; the first step of the proof
of Chatterjee–Diaconis' Theorem 1.1).
With `τ = e^{na+s}`, `M = e^{na+s+2t}`, `t = ln(2/(δε′))`, `s = u√(2n ln(4/(δε′)))`, `ε′ = 1 − e^{−ε/2}`, and
Markov's inequality: **`exp(na + O(u√(n ln(1/(δε)))))` samples from `Bernoulli(r*)^{⊗n}` are
`(ε/2, δ)`-correct on the whole class**, for every `n`.  With the lower bound `a` for all
non-adaptive algorithms at vanishing accuracy this is the exponent of non-adaptive
algorithms at every bounded accuracy, **attained by a product measure** — the Gibbs measure
of the additive instance `γ*|x|` — as well as by the type-stratified sample.  It does not
touch extensive accuracies, where the separation of product samplers from the flat
histogram stands as stated above.  (The division's argument replaces tail functions by a
martingale bound for the likelihood ratio.  We had also overlooked its first statement of
the result, SCI-RES-0001 §2.)

**Lemma 11.62 (tail lemma relative to a reference instance) [P; elementary].**  Let `ψ₀ ∈ L_u`
with weights `w₀`, Gibbs law `μ₀` and *slack* `s₀(x,y) = u·d(x,y) + ψ₀(x) − ψ₀(y) ≥ 0`.  For `ψ ∈ L_u`
(or a fibre average) put `ŵ = w/w₀`.  Then `A(ψ) = A(ψ₀)·E_{μ₀}ŵ`, `ŵ(x) ≤ ŵ(y)e^{s₀(x,y)}`, and for
every level `t` with `μ₀(ŵ > t) ≤ q < 1`

    E_{μ₀}(ŵ − t)₊ ≤ t·Ξ₀(q),        Ξ₀(q) = max{ Σ_{x∈D} μ₀(x)(e^{s₀(x→Dᶜ)} − 1) : D ⊊ Q_n, μ₀(D) ≤ q },

with equality for the deepest dip of the reference on `D`.  For `ψ₀ = 0`, `p = ½` this is Lemma
11.43(b), and Harper's theorem evaluates `Ξ₀`.  In general `Ξ₀` is a finite maximum over
subsets for which no closed form is claimed.

**Theorem 11.63 (asymptotic isoperimetry for the flat-histogram reference) [P; workstream F,
Theorem F6 — new; refereed (R9): proved].**  There is `ω_n → 0`, depending on `p, u` only, such that for
all `n`, all real `e` and all `D ⊊ Q_n`:

    Σ_{x∈D} μ_H(x)·e^{s_H(x→Dᶜ)} ≥ e^{ne}      ⟹      μ_H(D) ≥ exp(−n[R^max(e − ω_n) + ω_n]).

*Every set that is `e`-sensitive for the flat-histogram instance is hit by its Gibbs law — the
type-uniform mixture — with probability at least `e^{−nR^max(e) − o(n)}`*; equivalently (for
`θ = −n^{-1}ln μ_H(D) > ω_n`) the tail function of `H` has the exponent `(R^max)^{-1}`.  So `H` and
the hardest additive instance are equally hard.  (What the proof gives for `ω_n`: beyond
`n₀(p, u)` — `n > 4u⁴ln²3` and a condition on the window — a leading term `2n^{-1/8}`; below it the
trivial `ω_n = u`.  On every family of sets examined, by the workstream and by the referee,
the least admissible `ω` is below `0.5·ln n/n`.)
*Proof idea* (report §3.4).  The method of types, as in Theorem A(ii) of workstream A: an
inherently typical subset (a weighted variant of the Ahlswede–Yang–Zhang lemma, with its own
eight-line proof in the report) of the class of `D` on which the exit budget
`B(x) = min_{y∉D}[v(κ_y) + u·d(x,y)/n]` is constant; a single-letter lemma — for every law `P_{UX}`
there is a kernel `X → X′` with `u·P(X′≠X) + v(P_{X′}) ≤ B` and `I(X′;U) ≤ R^max(B − D(P_{X|U}‖π|P_U))`, by
minimax (the problem with a budget that depends on the type of the exit point collapses to
the maximum over `γ` of the single-instance problems); the kernel applied letter by letter
moves the typical subset into `D`; chain rule and data processing against a product measure
`Qⁿ` with `Q` in the window, where `μ_H ≥ Qⁿe^{−o(n)}`.  ∎
No finite-`n` extremal statement is available or used; exact vertex isoperimetry in the
biased cube is known for down-sets only (Bollobás–Leader 1991; abstract), and super-level
sets of Lipschitz functions are not monotone.  *Relation to the fixed-measure theorem*
(referee, who read the Ahlswede–Zhang summary in full): the statement is not a black-box
corollary of the asymptotic isoperimetry of a fixed product measure — the enlargement here
is an intersection over `γ` of additive-cost conditions that must hold for the same point,
with a budget that depends on the type of the exit point; the proof is the converse proof
of Ahlswede–Zhang / Yu with the product reference law chosen *after* the set and restricted
to its typical set, which is what lets `μ_H` dominate it.  New, as far as both readings go:
the reference `H`, the type-dependent budget, and the collapse of the single-letter problem
to `max_γ R_γ`.

**Theorem 11.64 (adaptive algorithms without a hint, with a field) [P: Theorems 11.59(a), 11.63,
Lemma 11.62, the two-level theorem relative to a reference, and the convergence theorem;
workstream F, Theorems F7–F9; refereed (R9): lower bound proved, upper bound proved after the
two repairs marked (M1), (M2) below].**  For every `p ∈ (0,1)`, `u > 0`, `0 < ε₁ < E`, `0 < δ < ½`, the least
worst-case number of evaluations of a randomised adaptive algorithm without a hint that is
`(ε₁n/2, δ)`-correct on `L_u` is

    exp( n·R^max(ε₁) + o(n) ),        R^max(ε₁) = max_{|γ|≤u} R_γ(ε₁),

**the hinted exponent of the hardest additive instance `γ*(ε₁)|x|`**, while non-adaptive
algorithms need `exp(nθ_na(ε₁) + o(n))`, `θ_na(ε₁) = R^max(S^{-1}(ε₁)) > R^max(ε₁)`.
*Proof.*  Lower bound: Theorem 11.59(a) at `γ*`.  Upper bound: (i) *one more level.*  The
two-level algorithm of Theorem 11.52 *relative to the reference `H`* — outer points sampled
from `μ_H` on the outer block, brackets and levels for `Ŵ = W/w_H`, closure by Lemma 11.62 with
(an upper bound of) the tail function of `H` and never at `q = 1` — has, for one tuple
`(φ, β, g, η₀)`, the accuracy `gn + O(log n)` and the cost exponent `τ + η₀` of (11.18.2) with the
present `θ_na` (Theorem 11.63 gives the exponent of the tail function; it is used on compact
sets of `θ > 0` only).  **(M2)** Its good event needs one change against Theorem 11.52: the
number of potential inner calls is `4K/min μ_H = 4K·Z_H·e^{c₁n_o}`, with `c₁ = ln 2` if `|θ| ≤ u` and
`c₁ = ln(1 + e^{|θ|−u}) > ln 2` if `|θ| > u`, so the inner failure probability handed down is
`δe^{−c₁n}/(2⁶n⁴)` and `K = ⌈24 ln(2⁶n³/δ)⌉` (the definition of an exponent function allows every
failure probability `e^{−cd}`, and `K` stays `O(n)`); alternatively the union is taken over the
calls actually made, at most the abort threshold.  (ii) *The pair.*  `(θ_na, R^max)` satisfies
`HintPair θ_na R^max a h E` (convex analysis of `R^max(e) = max_{t≤1}[F*(t) − te]`: convex,
nonincreasing, slopes in `[−1, 0]`; `S` an increasing homeomorphism; the bound `t ≤ 1` in the
game formula is exactly the slope condition; in abstract form this is Theorem 11.66 **[V]**).
(iii) *The levels.*  **(M1)** Start from enumeration (`T₁ ≡ ln 2`) and put `T_{k+1} = min(T_k, R[T_k])`,
`R` the operator of §11.18 built on the present `θ_na`.  The induction written in the proof of
Theorem 11.54 (*Assembly* of the procedures of (i) into a family, whose exponent function is
bounded by `min(T, R[T])(·⁻) + η₀` — with a left limit, nothing shows that the `T_k` are
continuous; *Shift*; *Induction*) uses of the one-level theorem only its accuracy, its cost
exponent for a finite ladder of rates, and the monotonicity of `θ_na` and of `T`, so it applies
verbatim and gives: for every `k`, `η′ > 0` and `g < ξ` a family whose exponent at `ξ` is at most
`T_k(g) + kη′`.  By `iterates_lt_hint_add` **[V]** (given (ii); the bound on `T₁` is a separate
hypothesis there) `T_k(g) < R^max(g) + η` for large `k`; let `g ↑ ε₁` and use the continuity of
`R^max`.  (Started at the non-adaptive exponent instead of enumeration, the same recursion is
`exactRec`, and `exactRec_reaches_hint_of_pair`, `GameFunction.exactRec_tendsto` **[V]** give its
convergence.)  ∎
So **"adaptive = hinted" persists with a known part, in the form: the worst case without a
hint equals the hardest case with a hint** — and the hardest case is not the zero residual.

**Proposition 11.65 (instance-optimality in the field; a field always helps) [P; (a), (c):
workstream F, Theorem F10; (b): the coordinator, after the workstream's numerical
observation; all three refereed (R9): proved — "the uniform cube is the hardest case" in (b)
is conditional on Theorems 11.61 and 11.64].**  (a) *Not in the worst case:* for `θ ≠ 0` the worst-case exponent `R^max(ε₁)` of adaptive
algorithms without a hint is strictly larger than the hinted exponent `R_0(ε₁)` of the
instance `(f, g = 0)`; between `E_0` and `E` the instance `g = 0` is cheap with a hint while the
class is exponentially hard.  (b) *A field always helps, and the hardest residual always
works against it.*  For every `0 < t < 1` the function `θ ↦ F*(t; θ)` is even and strictly
decreasing on `[0, ∞)`, and its maximiser has `γ*·θ < 0` for `θ ≠ 0`.  Hence `R^max(e; θ)`, the class
threshold `E(θ)`, `θ_na(x; θ)` and `a(θ)` are nonincreasing in `|θ|`: the uniform cube is the
hardest case, for adaptive and for non-adaptive algorithms.  (The workstream had this as a
numerical observation on a grid of 121 fields, and `γ*θ < 0` to first order.)
*Proof of (b)* (every step checked numerically: `experiments/coordinator_checks/field_monotone_proof_check.py`).
Write `x = θ + γ` for the total field and, in the cosh form of Theorem 11.59(b),
`F(γ,t) = ln ρ_θ(θ+γ)` with `ρ_θ = I_θ/C^t`, where `I_θ` solves `I″ = (t/2)²I` on the window `[θ−u, θ+u]` and
equals `C^t` at its ends.  (i) Since `(C^t)″ = (t/4)C^t[1 − (1−t)tanh²(x/2)]`, the ratio satisfies

    ρ″ + t·tanh(x/2)·ρ′ + (t(1−t)/4)·sech²(x/2)·ρ = 0,        ρ = 1 at both ends,   ρ > 0.

At a critical point `ρ″ < 0`, so every critical point is a strict local maximum; there is one
(`ρ = 1` at both ends and `ρ` is not constant), and two would force a local minimum in between:
there is exactly one, `x* = θ + γ*`, and `F*(t; θ) = ln ρ_θ(x*)`.  (ii) Let `A_u ∈ (0, 1)` be the average of `tanh`
over `[(θ−u)/2, (θ+u)/2]`, `θ > 0`.  Then `∂_γF(0,t) = (t/2)[tanh(tuA_u/2)/tanh(tu/2) − tanh(θ/2)]`; the
quotient is increasing in `t` (convexity of `sinh`) and equals `tanh(θ/2)` at `t = 1`, so the
derivative is negative for `t < 1`, and by (i) `γ* < 0`.  (iii) `γ*` is a nondegenerate interior
maximum, so by the envelope theorem `dF*/dθ` is the partial derivative in `θ` at `γ*`; inserting
the first-order condition and `cosh a ± sinh a·tanh b = cosh(a ± b)/cosh b`, the inequality
`dF*/dθ ≤ 0` becomes

    ln cosh Q − ln cosh P  ≥  (1−t)·[ ln cosh((θ+u)/2) − ln cosh((θ−u)/2) ],
    P = (θ−u)/2 + t(u−γ*)/2,     Q = (θ+u)/2 − t(u+γ*)/2,

that is: *the average of `tanh` over `[P, Q]` is at least its average over
`[(θ−u)/2, (θ+u)/2]`*.  The first interval lies inside the second, has length `(1−t)u`, and its
centre `(θ − tγ*)/2` is strictly to the right of `θ/2` because `γ* < 0` and `t > 0` — which, `tanh`
being strictly increasing, makes the inequality strict: `dF*/dθ < 0` for `θ > 0`.  (The referee
notes that the first-order condition is not needed if the derivative in `θ` is taken at fixed
total field `x`.)  (iv) For an odd increasing
function `f` that is concave on `[0, ∞)` and `c ≥ 0`, the average of `f` over `[c−r, c+r]` is
nonincreasing in `r` (for `r ≤ c` by concavity; for `r > c` it is `(2r)^{-1}∫_{r−c}^{r+c} f`, whose
derivative has the sign of `r[f(r+c) − f(r−c)] − ∫_{r−c}^{r+c} f ≤ (r−c)f(r+c) − (r+c)f(r−c) ≤ 0`,
by the trapezoid bound for a concave function and because `f(x)/x` is nonincreasing).  So a
sub-interval with the same centre has at least the average of the whole interval, and
moving it to the right increases its average.  The statements about `R^max`, `E`, `θ_na` and `a`
follow because each is a pointwise nondecreasing functional of `F*`
(`θ_na(x) = sup_{τ<1}(F*(τ) − τx)/(1 − τ)`).  ∎
(c) *Yes at symmetric
instances:* the type-stratified two-sample bracket (per type class: threshold at the `K`-th
largest weight of one sample, truncated mean over a second, tail by Lemma 11.62 with a
maximum over sets of bounded type-wise density) is valid on all of `L_u`, and with doubling
and adaptive stopping its cost at every permutation-symmetric instance — in particular at
`g = 0` and at every additive instance — is within a polynomial factor of the least cost of
any correct algorithm at that instance at accuracy `ε − ln 3`.  Its two bounds are the same
combinatorial function, so no isoperimetry is used.  Instance-optimality at non-symmetric
instances is open, as in §11.18.

*Numbers* (workstream F; the first three rows re-computed by the coordinator at
`(p, u) = (0.1, 2)` and `(0.3, 1)`).  Exponents at vanishing extensive accuracy, `u = 2`:

| `θ` | `0` | `0.5` | `1` | `2` | `3` |
|---|---|---|---|---|---|
| hint at `g = 0`: `R_0(0+)` | `.0973` | `.0929` | `.0811` | `.0487` | `.0230` |
| adaptive, no hint `=` hint at the hardest instance: `R^max(0+)` | `.0973` | `.0938` | `.0839` | `.0542` | `.0272` |
| `γ*` | `0` | `−.170` | `−.330` | `−.583` | `−.734` |
| non-adaptive, type-uniform sample: `a` | `.3278` | `.3162` | `.2836` | `.1841` | `.0928` |
| plain Monte Carlo from `π` | `.3278` | `.4078` | `.4621` | `.4338` | `.2732` |

Exact binomial sums (certified sensitive sets, so each number is a valid lower bound on a
cost) approach the formulas like `0.35`–`0.41·ln n/n`: at `p = 0.1`, `u = 2`, `ε₁ = 0.3E`, `n = 64 000`,
`0.019568` against `R_0 = 0.019497` and `0.023337` against `R^max = 0.023270` — at that size every
algorithm, with or without a hint, needs `(1−2δ)e^{0.0233n}` evaluations at `γ*|x|`, while
`e^{0.0196n}·poly` suffice with a hint at `g = 0`.

*Remarks.*  (1) What the field changes, in one sentence: the sampler must be uniform on type
classes (a mixture of all tilted product measures), the reference instance must be the
lower envelope `H` of the additive instances, and the hardest instance tilts the field
towards zero.  Four natural guesses are false (`DEAD_ENDS.md`, D47): that the identity holds
with the hinted exponent of `g = 0`; that `g = 0` is the hardest instance; that `π` is the right
sampler; and — the coordinator's — that what is needed is a Harper-type theorem for a fixed
product measure (the asymptotic isoperimetry of a fixed product measure is the tail lemma
of plain `π`-sampling and gives the worse exponents).
(2) The nested algorithm is an algorithm in the query-complexity sense only: it uses the
numbers `Ξ_H(q)`, finite maxima over subsets of the outer cube, which cost no evaluations
but for which no formula is known.  It needs only an upper bound `Ξ̄ ≥ Ξ_H` that vanishes
below the least point mass (validity and exponent survive), and the proof of Theorem 11.63
gives an explicit one — with the useless rate `n^{-1/8}`.  A finite-`n` bound with the right
exponent and a usable error term — a weighted Harper-type inequality for the type-uniform
measure and the slack of `H` — would make it practical.  On small cubes the exact maximisers
are not always balls with type-dependent radii around one centre: the exact `Ξ_H` exceeds the
best such set by a factor up to `2.08` on `Q_4` (`p = 0.2`, `u = 4`; the workstream's "at most 2"
was true only for its nine cases with `u ≤ 2`).
(3) *Why this sampler: it is the universal one.*  `μ_H ∝ max_{|γ|≤u} π_γ` is the
normalised-maximum-likelihood (Shtarkov) distribution of the one-parameter exponential
family of field-tilted product measures `π_γ`, and its normalising sum is polynomial
(`1 ≤ Z_H ≤ n + 1`).  Hence, trivially and for every `n`, `μ_H(D) ≥ π_γ(D)/(n + 1)` for every set `D`
and every `|γ| ≤ u`: a sample from `μ_H` is, up to a polynomial factor, a sample from every
tilted product measure at once — exactly as the Shtarkov code is, up to its regret, the
best code for every member of the family.  The hinted sampler of an additive instance is
built from `π_γ` and the type-uniform mixture (Theorem 11.27), so the minimax-regret
distribution of universal coding is the minimax sampler here, and the least favourable
instance `H` is the one whose Gibbs law it is.  This reading suggests what to try beyond
independent sites — the normalised-maximum-likelihood mixture of the field-tilted Gibbs
measures of an *interacting* known part, i.e. an ensemble that is flat in the order
parameter conjugate to the field — but there nothing is proved: the universality of the
sampler against tilted measures carries over verbatim, the statement that the hardest
instance is additive (Theorem 11.63) does not.
(5) *Beyond a field: every known part that is a function of the type.*  Parts (a) and (b)
of Theorem 11.61 never use that the reference measure is a product measure — only that
it is uniform on type classes, i.e. that the known part is `f(x) = n·φ(|x|/n)` (mean-field
models, with or without a phase transition).  So for every such known part and every `n`:
the weight truncated at its type-wise `q`-quantiles is in the class and differs from the
original on density at most `q` per type class (**[V]**, `TypeQuantiles.lean` — the local LYM
inequality); hence every non-adaptive algorithm needs `(1 − 2δ)/q` evaluations at the
accuracy `ε_n^{tr}(q)` (**[V]** for every permutation-invariant class and target,
`SymmetricSampling.lean`); every algorithm, adaptive or not, needs `(1 − 2δ)/q` evaluations
at an instance that is itself a function of the type whenever some class member differs
from it by more than `ε` in the target and on density at most `q` in every type class
(**[V]**, `symmetric_queries_ge` — the every-`n` lower bound from a permutation-invariant family
of dips); and `M` uniform points from each type class, weighted with the
known `π(T_κ)`, are accurate to `ε_n^{tr}(q) + O(1)` once `Mq ≳ log n` (**[P]**: Chernoff and
Markov, as in (b)).  **A sample that is flat in the order parameter — the multicanonical
ensemble — is therefore optimal among fixed samples, up to a polynomial factor, for a
certified estimate over the Lipschitz class around any mean-field known part.**  What the
exponent `n^{-1}ln(1/q)` is as a function of the accuracy, and what adaptive algorithms can
do, depends on the rate function of the type: **this is §11.23** (for a convex rate
function everything of this section except the nested algorithm carries over; with two
phases the extremal functions are cones around shells in the barrier type class, not
single cones).
(4) Larger alphabets, an arbitrary single-site known part and sites of several types: the
same statement with the game function of Theorem 11.27(c) and the Lipschitz polytope of
additive instances in place of `[−u, u]` is a **sketch** (report, Proposition F12); with several
site types the exponents do not add (`0.0086` against the average `0.0098` in an example).
Known parts with interactions: nothing.  Bounded accuracies with a field: only the lower
bound `a` for non-adaptive algorithms (Theorem 11.61(b), (c)); the upper bounds here are at
accuracies `o(n)`, not `O(1)`, and §11.19 is for the uniform cube.

*Falsification harness.*  XVII.1 (closed form against the game value; shift identity; the
hinted exponent at the zero residual in both forms; the uniform cube at `p = ½`; the strict
gain of the hardest additive instance; the pair identity), XVII.2 (type-wise quantiles),
XVII.3 (Lemma 11.62 with the exact tail function of `H` on the 4-cube, all 65 534 subsets),
XVII.4 (the steps of the proof of Proposition 11.65(b)); ten mutations, all detected — among
them the false guesses of D47.

*Machine-checked.*  `FieldShift.lean`: `klBin_tilt`, `cone_rate_eq`, `sphere_rate_eq`, `shift_identity`.
`TypeQuantiles.lean`: Theorem 11.61(a) — the density of `{w > e^u τ}` in a type class is at
most that of `{w > τ}` in either adjacent class (`upperDensity_succ_le`, `upperDensity_pred_le`),
hence admissible thresholds propagate with the factor `e^u`, and the truncated weight
stays in the class.  `SymmetricSampling.lean`: Theorem 11.61(b)(i) — the lower bound
`(1 − 2δ)/q` for non-adaptive algorithms from a pair of class members that differ on
density at most `q` in every type class, for every permutation-invariant class and
target (a uniformly random permutation sends a configuration to a uniformly random
configuration of its type: `card_perm_smul_mem_mul`).  Neither file mentions the reference
measure: the two statements hold for every known part that is a function of the type.
`BoundedAccuracy.lean`: `exactRec_reaches_hint_of_pair` (the exact recursion built on any
nonnegative nonincreasing `θ_na` that forms a `HintPair` with `θ_hint` comes within `η` of
`θ_hint`).  *Not machine-checked:* `HintPair` for the pair `(θ_na, R^max)`, the formulas of
Theorem 11.59, everything about algorithms.

*Numerical evidence* (workstream F; scripts and outputs in `experiments/workstreams/F/`,
`run_all.sh`).  Single-letter formulas against each other to `10⁻¹¹…10⁻¹⁵`; exact binomial sums
for dips of `g = 0`, of `γ*|x|`, of `H` and for flattened cones up to `n = 4000` (four parameter
sets) and `n = 64 000`; the single-letter lemma of Theorem 11.63 by direct minimisation over
kernels for about 1900 laws; Theorem 11.63 on 1829 profile sets of six shapes at `n ≤ 2000`
and on all 65 534 subsets of `Q_4`; the two-level logic relative to `H` on a small outer block
with the exact tail function (198 runs valid; closing at `q = 1` and forgetting the weights
`1/w_H` are detected); the level recursion with the pair `(θ_na, R^max)` never below `R^max` and
within `0.5 %` of `a` after twelve levels.  *The referee's own numerics* (own code, nothing
imported; `experiments/reviews/R9/`): the single-letter formulas independently of duality
(a linear-programming game solver against the closed and the cosh form: `5·10⁻¹¹`; the max–min
forms: `2·10⁻⁹`; the pair identity holds with `R^max` and fails with `R_0`); the single-letter
lemma by primal minimisation over kernels for 800 laws, with equality to `10⁻¹²` at the
generalised dip for accuracies of both signs; the typical-subset lemma and the chain-rule
step exactly on 210 instances; Lemma 11.62 on `Q_4` with the exact tail function (26 000
thresholds); **Theorem 11.63 on all subsets of `Q_3` and `Q_4`, by annealing on `Q_5`, `Q_6`, and
exactly on 3 494 sets at `n = 80…240` from families the workstream did not test** — unions of 2
and of 16 balls with different centres, lenses, half-spaces, slabs, ellipsoids and boxes
without a centre — and by annealing over arbitrary profile masks: the least admissible `ω`
is at most `0.47·ln n/n` and decreases with `n`; unions of two balls gain nothing at the
exponential scale over one ball, centreless families are worse; no counterexample.  Exact
sums to `n = 4000` approach `R_0`, `R^max`, `R^max`, `θ_na` from above with an excess of
`0.2…0.7·ln n/n`.  *Not tested by anyone:* Theorem 11.63 on sets without any symmetry for
`n > 6`; the nested algorithm end to end with a field (the workstream's simulation uses
simulated inner brackets, which is why it could not see (M2)); the uniformity of the `o(n)`
terms through the levels.

*Prior art* (read by the workstream as abstracts or machine summaries; the referee read the
three-page Ahlswede–Zhang summary in full and made seven further searches).  Exact
isoperimetry in the `p`-biased cube for down-sets (Bollobás–Leader 1991); the asymptotic
isoperimetric problem for fixed product measures (Ahlswede–Zhang — stated for cardinalities,
with the inherently typical subset lemma attributed to Ahlswede–Yang–Zhang 1997; Yu,
arXiv:2205.07596, two product measures and an additive cost); vertex isoperimetry inside one
slice (Johnson graph) does not apply, because the neighbourhoods here cross slices.  Not
found at that depth: an isoperimetric statement for a mixture over types with a
type-dependent enlargement; a nested hint-free algorithm with a known part; the exponent
`max_γ R_γ`; exact adaptive and non-adaptive exponents for integration against a product
measure over a Hamming–Lipschitz class.  "Not found", not "new".

### 11.21 The structure behind §§11.16–11.20: the shear law, and every game function yields a pair

The uniform cube (§§11.16–11.19) and the biased cube (§11.20) have the same skeleton, and
the part of it that is pure analysis is now a machine-checked theorem about arbitrary
"game functions" (workstream M, `docs/workstreams/M_REPORT.md`).

**The shear law.**  Draw the cost exponent `θ` against the accuracy rate.  In both cases the
curve of algorithms with a hint — which is also that of adaptive algorithms without one —
and the curve of non-adaptive algorithms are related by

    x_na(θ)  =  e_hint(θ)  +  θ :

*with a budget of `e^{nθ}` evaluations a non-adaptive algorithm certifies an accuracy rate
that is worse by exactly `θ`.*  Equivalently `θ_na(e + R(e)) = R(e)`, or `R(x − θ_na(x)) = θ_na(x)`:
the graph of the non-adaptive exponent is the graph of the hinted exponent `R` sheared to
the right by its own height.  On the uniform cube this is the identity
`KL(ρ‖p_u) = KL(ρ‖½) + (uρ − Λ₁)` at the radius `ρ` of the ball that a sample of `e^{nKL(ρ‖½)}` points
does not see; with a field it is Lemma 11.60 read at the flat-histogram reference.  The
reason is the same in both: a sample of `e^{nθ}` points from the Gibbs law of the reference
misses sets of measure `e^{−nθ}`; an algorithm that knows where to look (a hint) or learns it
(adaptivity) pays only for the *effect* of such a set, a non-adaptive one also pays for
never having seen it, and measure and effect multiply.
*In the units of information-based complexity* (a rewriting due to the Scientific
Discovery Division, SCI-REV-0004): with `N = e^{nθ}` evaluations, `ε_na(N) = ε_ad(N) + ln N + o(n)`
for budgets `N ≤ e^{nh}` — the multiplicative error of the best non-adaptive method is
`N^{1+o(1)}` times that of the best adaptive one.  This is a statement about the two minimax
errors (the non-adaptive lower bound and the adaptive one are attained at different
pairs of instances — a cone against its truncation, the flat instance against a dip),
not about any single instance.  As an identity it is the exponential change of measure
`KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁`, which is in print in the form "`ln M` + frozen energy" for the
Jarzynski estimator of the discrete random energy model (Suárez–Silbey–Oppenheim 2012,
eq. (39) in the division's reading); Theorem 11.66 below is restricted Legendre duality
packaged for the recursion.

**Theorem 11.66 (every game function yields a pair, and its level recursion converges) [V]
(`GamePair.lean`: `GameFunction.hintShape_critical`, `GameFunction.pair`,
`GameFunction.exactRec_tendsto`; workstream M).**  Let `F : [0,1] → ℝ` be a *game function*:
continuous, `F(0) = F(1) = 0`, `F(t) ≤ L(1 − t)`, `F(t) ≤ E·t` with `E = sup_{t>0} F(t)/t > 0`.  Put

    R(e) = max_{0≤t≤1} [F(t) − t·e]        (the hinted exponent),        S(e) = e + R(e)        (the shear).

(a) `R` is convex and nonincreasing with slopes in `[−1, 0]` — the restriction `t ≤ 1` *is* the
slope condition —, `R(e) ≥ max(0, −e)`, and `R = 0` exactly on `[E, ∞)`.  `S` is nondecreasing,
vanishes on `(−∞, e_c]` and is strictly increasing on `[e_c, ∞)`, where `e_c < 0` is the largest
zero of `S`; `R(e_c) = −e_c`, and `e_c = −L` if the constant `L` is sharp.
(b) The non-adaptive partner `θ_na := R ∘ S^{-1}` is continuous and nonincreasing on `(0, ∞)`,
`θ_na(x) = min{R(e) : e + R(e) ≤ x}`, `R < θ_na ≤ a := −e_c` on `[0, E)`, `θ_na = 0` from `E` on, and
`(θ_na, R)` is a `HintPair` with the constants `a`, `h = R(0)`, `E`.
(c) `R` is a fixed point and a lower barrier of the level operator of §11.18 built on `θ_na`,
and for **any** function `θ_na` that obeys the shear law wherever `e + R(e) > 0`, the exact level
recursion `T₁ = θ_na`, `T_{k+1} = min(T_k, R[T_k])` **converges to `R` at every accuracy rate `g > 0`**.
(d) *Witness.*  `F(t) = t(1 − t)` is a game function with `E = L = 1`; `R(e) = ((1−e)/2)²` on `[−1, 1]`
and `θ_na(x) = (1 − √x)²` — the toy pair of `HintRecursion.lean` — so nothing above is vacuous
(`toyGame_gameFunction`, `hinted_toyGame`, `partner_toyGame`, `gauss_exactRec_tendsto`).

*What it buys.*  The convergence of the level recursion — Theorem 11.53, and step (ii)–(iii)
of Theorem 11.64 — is machine-checked for every problem whose hinted exponent is the
transform of a game function and whose non-adaptive exponent obeys the shear law.  For the
uniform cube `F(t) = Λ(tu) − t·Λ(u)`, `Λ(s) = ln(2/(1+e^{-s}))` (`CubeHintPair.lean` does that case by
hand); for the biased cube `F = F*` of Theorem 11.59, where the game-function properties of
`F*` and the shear law (Theorem 11.59(c), Lemma 11.60) are paper statements; for identical
sites with larger alphabets the same would follow from the sketch of §11.20, remark (4).
*What the formalisation showed on the way.*  The two ends of the game function carry the
two extreme exponents: `E = sup_{t>0} F(t)/t` is the threshold accuracy (`t → 0`), and
`a = sup_{t<1} F(t)/(1 − t)` is the non-adaptive exponent at vanishing accuracy (`t → 1`), while
`h = max_t F(t)` is the adaptive one.  The hypothesis "`θ_na(e + R(e)) = R(e)` wherever the shear
is nonnegative" would be unsatisfiable (`S ≡ 0` below `e_c`, where `R` varies):
`GameFunction.not_forall_shift_eq`.  And the monotonicity of the shear is not needed for the
pair itself.

*What a problem must supply* — a summary of Theorems 11.52/11.56 and 11.64, not a new theorem.
(I1) A lower bound `e^{nR(ε₁) − o(n)}` for every algorithm at some instance, with `R` the
transform of a game function (Theorem 11.27: generalised dips).  (I2) A reference instance
in the class whose Gibbs law can be sampled and whose tail function — the largest effect of
a dip of the reference on a set of given measure — has the exponent `R^{-1}`: the
isoperimetric input (Harper's theorem on the uniform cube; Theorem 11.63, by types,
refereed, with a field).  (I3) Fibres: the restriction to a block of coordinates stays
in the class, and fibre averages are Lipschitz relative to the reference (Lemma 11.62).
Then non-adaptive algorithms have the exponent `R ∘ S^{-1}` and adaptive ones `R`; the first
half of that sentence needs (I1), (I2) and a truncation argument, the second (I1)–(I3), the
nested algorithm, and Theorem 11.66.  The least favourable instance is the reference, and
the optimal fixed sample is its Gibbs law.

---

### 11.22 Chains in the thermodynamic limit: a limit shape for profile sets, and the limit of certificate sizes

§11.17 ended with a question that the Computational Research Division put back to the
theory (`ENG-REQ-0001`): at extensive accuracy the smallest certificates of the profile format
grow with the chain at every size that can be enumerated, Proposition 11.49(a) gives a
bound that does not depend on the chain length (a bound, not a limit), of the order
`10^{1387}` — *what is the limit, and when is it
reached?*  Workstream S (`docs/workstreams/S_REPORT.md`) answers this for the diamond-lattice
chain of §11.17: there is a **limit shape** — a compact convex body of profile densities
carrying a convex function, the least gauche density — the certificate sizes of
*bridges* converge to a covering number of that object for all accuracies outside a
countable set that is not identified, and the shape converges with a surface correction of
exact order `N^{-1/3}` at its compact end.  For unrestricted walks one inclusion and all
bounds are proved and equality of the limits is a conjecture, of the kind that is open in
the literature for the free energy of self-attracting walks.
**What this says about the numbers, in three parts** (wording of the review SCI-REV-0002 of
the Scientific Discovery Division, finding M1; the first version of this paragraph said
"the plateau lies between 50 and 3 627 evaluations at `(L, ε₁) = (1, ½)` and is reached at
chain lengths of `10³`–`10⁵` beads", which joined a theorem, a conjecture and an estimate in
one sentence).  (i) *Theorem* **[P, computer-assisted]**: every limit point of the certificate
sizes of all walks at `(L, ε₁) = (1, ½)` lies between 116 and 3 627; the sizes are at most
`26 437` at every chain length and at least 26 at 1 000 beads.  (ii) *Conjecture-dependent*
**[C]**: that the sizes converge — that there is a plateau at all — is proved for bridges
off the exceptional set of accuracies, to which `ε₁ = ½` may belong, and for the chains that
were measured it needs Conjecture 11.75 in addition.  (iii) *Estimate* **[N]**: the limit is
a few hundred, and the chain length at which it is approached is `10³`–`10⁵` beads or
more; no theorem bounds that length from above or from below.

**Status of this section.**  Paper proofs by workstream S; **every proof below was re-derived
by the coordinator, and every computer-assisted statement was re-computed with independent
code** (`experiments/coordinator_checks/s_check1.py` … `s_check7.py`, outputs next to them: the
finite inequalities on all profile classes up to 27 beads; the concatenation lemma on 48 058
concatenations of bridges with an own implementation; both linear programmes re-formulated and
re-solved, the eleven dual certificates of the site programme verified and fifteen own
certificates of the marked programme found, all in exact rational arithmetic; lamellae,
hairpins, volume bounds, packings and exact covering numbers; the explicit bridge with
166 199 beads).  No discrepancy was found; two lower bounds were
slightly improved.  **Reviewed by the Scientific Discovery Division** (SCI-REV-0002, 25
November 2026; its report `docs/science/workstreams/R2_REPORT.md` and its code
`experiments/science/ws_R2/` are on the branch `research/scientific-translation`; an enumerator
written before reading ours, Lemma 11.68 tested by it on all 270 997 444 ordered pairs of
bridges with at most 13 beads, both linear programmes re-formulated with certificates of
its own): **no statement labelled as proved was found false.**  Two major findings, both
applied here: the practical headline joined a theorem, a conjecture and an estimate (M1;
reworded above and wherever it was quoted), and the proved bracket was not the one in the
table (M2: the lower bounds of Theorem 11.71(c) are raised with the section's own tools,
and the inner volume `2.2`, which rests on a sketch, gives way to a proved `1.56`).  Eight
minor findings (m1–m8) and five statements of the reviewer (N1–N5) are marked where they
enter; two further statements come from that division's review of prior art (SCI-REV-0006):
Proposition 11.69a and Bezdek's constant in Proposition 11.73.  Before adoption we
re-verified with own lattice code: N1; the ten explicit bridges, from coordinates; the four
packings and the inner volume, in exact rational arithmetic; the count behind m1; the
exhaustive maxima of m3; the arithmetic of N4 and of Bezdek's constant; and we re-derived
Proposition 11.69a.  Not re-derived by us: N5.  **Machine-checked**
(`CoverStability.lean`, `SetLimit.lean`): the two soft theorems in abstract form — Fekete's
lemma for sets (a family that is super-additive up to a bounded error has normalised sets
that converge in the Hausdorff sense to a compact convex set, with the one-sided rate
`β/M`), the stability of covering numbers under such convergence, and their combination
(the covering numbers of the finite sets are sandwiched by those of the limit at shifted
accuracies).  The declarations take the family at every index `M ≥ 1` and normalise by
`M = N + 3`; the first version left the link to the lattice implicit (finding m1; it is a
paper step, now in the proof of Theorem 11.69).
**Not machine-checked:** everything about the lattice — in particular that
the sets of bridges satisfy the hypotheses (Lemmas 11.67, 11.68) — and all numbers.  The model is the synthetic lattice chain with a made-up known part; the
section is about the mathematics of the limit, not about any real system.

*Setting.*  Diamond lattice with bond vectors `±a₀, …, ±a₃`, `a₀ = (1,1,1)`, `a₁ = (1,−1,−1)`,
`a₂ = (−1,1,−1)`, `a₃ = (−1,−1,1)`.  A *walk* with `N` beads is an injective sequence of sites with
consecutive sites bonded; `n = N − 3` torsions; torsion `i` is trans iff `|x_{i+3} − x_i|² = 19` and
gauche iff it is `11`.  Cutoff `S_c = 12`: the squared distances below it are `3, 8, 11`, and the
profile is `h(x) = (h₃, h₈, h₁₁)`, `h_d = #{p < q : q − p ≥ 3, |x_q − x_p|² = d}`; `g(x)` is the number of
gauche torsions.  By Theorem 11.48(b) the envelope of the class of unknown `L`-Lipschitz pair
potentials is `L` times the `L¹` distance of the cumulative profiles,

    ‖Δh‖_c := 5|Δh₃| + 3|Δh₃ + Δh₈| + |Δh₃ + Δh₈ + Δh₁₁| ,

(for a single profile `‖h‖_c = 9h₃ + 4h₈ + h₁₁ = ‖N^x‖₁`; **for differences it is not
`9|Δh₃| + 4|Δh₈| + |Δh₁₁|`** — the coordinator's brief said so; D48).  With the known part
`e·g(x)` and the zero residual, a set `A` of conformations certifies the minimum to accuracy `ε`
iff every conformation `y` has an `a ∈ A` with `L‖h(a) − h(y)‖_c ≤ e·g(y) + ε`; `N^P_cov(ε)` is the least
size of such a set (the quantity measured in §11.17; re-computed here by exact set cover:
8 and 11 at 15 and 21 beads, `L = e = 1`, `ε = N/2`).  A *bridge* is a walk whose first bead is
strictly lowest and whose last bead is highest in the coordinate `y`; `N^{P,br}_cov` is the same
covering problem with clients and centres restricted to bridges.  Densities: `(h, g)/N`, in the
box `[0,1]×[0,5]×[0,6]×[0,1]`, with the norm `‖p‖_c + |g|`.

**Lemma 11.67 (the profile is a function of the site set; local counting) [P; exhaustively
for `n ≤ 9` by two independent codes].**  Let `S` be the set of sites of a walk with `N` beads,
`e_d(S)` the number of unordered pairs of `S` at squared distance `d`, and `d_S(m)` the number of
occupied neighbours of a lattice site `m`.  Then
`h₃ = e₃(S) − (N − 1)`, `h₈ = e₈(S) − (N − 2)`, `h₁₁ = e₁₁(S)`, and
`e₃(S) = ½Σ_{m∈S} d_S(m)`, `e₈(S) = Σ_m C(d_S(m), 2)` — the sum over **all** lattice sites, occupied
or not — and `2e₁₁(S)` is the number of gauche four-site paths `(u, v, w, z)` with `u, z ∈ S` (two
sites at squared distance 11 are opposite corners of a six-ring and are joined by exactly
two three-bond paths).  So the profile part of the problem is a ground-state problem for a
*lattice gas* with pair interactions on three shells; the chain enters through traceability
of the site set and through `g`, which is a minimum over Hamiltonian paths of a fixed set — a
stiffness optimisation at fixed shape.  (Pairs at chain separation 1 and 2 are always at
squared distances 3 and 8.)

**Lemma 11.68 (concatenation of bridges, with explicit constants) [P].**  For bridges `x¹, x²`
with `N₁, N₂ ≥ 3` beads there is a bridge with `N₁ + N₂ + 3` beads whose `(h₃, h₈, h₁₁, g)` exceeds the sum
of those of `x¹` and `x²` by a vector `(δ₃, δ₈, δ₁₁, δ_g)` with

    0 ≤ δ₃ ≤ 1,     0 ≤ δ₈ ≤ 9,     0 ≤ δ₁₁ ≤ 14,     δ_g ∈ {0, 1},

of norm at most `β = 60`; appending one bead to a bridge changes `(h, g)` by a vector in
`[0,1]×[0,3]×[0,6]×[0,1]`, of norm at most `β′ = 28`.
*Proof.*  Three facts about the lattice: every bond changes the height `y` by exactly `±1`, and
every site has two up-bonds and two down-bonds; a site has 4 second neighbours at each of
the relative heights `−2, 0, 2` and third neighbours `4, 4` at heights `±1` and `2, 2` at heights `±3`,
so sites whose heights differ by 4 or more are farther apart than the cutoff; the lattice
symmetries that preserve the order of heights act simply transitively on the eight ordered
pairs (up-bond out of a site, up-bond out of its end point).  Let `P` be the last bead of `x¹`,
at height `H`, `b` its last bond (an up-bond) and `b′` the bond before.  Put the linker
`ℓ₁ = P + c₁`, `ℓ₂ = ℓ₁ + b`, `ℓ₃ = ℓ₂ + c₁` and `Q = ℓ₃ + b`, where `c₁ = b′` if `b′` is an up-bond and `c₁` is an
up-bond out of `P` otherwise; the first two bonds of `x²` are up-bonds, and there is exactly
one height-preserving symmetry `φ` that maps `x²₀` to `Q` and these two bonds to `(c₁, b)`.  The walk
`x¹, ℓ₁, ℓ₂, ℓ₃, φ(x²)` is a bridge: `x¹` lies at heights `≤ H`, the linker at `H+1, H+2, H+3`, `φ(x²)` at
heights `≥ H + 4` with `Q` its only bead at `H + 4`.  The six new torsions have the bond triples
`(b′, b, c₁)`, then `(b, c₁, b)` and `(c₁, b, c₁)` alternately — all trans except the first, which is
gauche iff `b′` is a down-bond.  By the second fact no bead of `x¹` is within the cutoff of a
bead of `φ(x²)`, so by Lemma 11.67 the errors are the pairs between the linker and the two
pieces minus the chain neighbours across the junctions, all non-negative, and the upper
bounds are a count of the neighbours of `ℓ₁, ℓ₂, ℓ₃` at admissible heights (`ℓ₁` is at squared
distance 19 from `Q` because the torsion between them is trans).  ∎
(Own check: all pairs of bridges with at most 7 beads and 3 000 random pairs with at most 10:
the symmetry is unique in every case, the errors lie in the stated intervals, and
`δ_g = [b′ is a down-bond]`; the observed maxima at these sizes are
`(0, 2, 4, 1)`.  *Exhaustively* (Scientific Discovery Division, SCI-REV-0002, m3: all
270 997 444 ordered pairs of bridges with at most 13 beads, no failure; the first version
of this remark called the proved constants "worst cases that need many beads near the top
level"): **`δ₃ = 1` is attained**, from 12 beads on, and the maxima are `(1, 6, 8, 1)`, norm 41,
for `N₁, N₂ ≤ 13` and `(1, 6, 9, 1)`, norm 43, for `N₁ ≤ 16`, `N₂ ≤ 8`.  Re-computed by us through the
decomposition that the proof uses — the error is a term that depends on `(x¹, c₁)` only
plus a term that depends on `x²` only; the identity checked on 57 025 concatenations built
from coordinates — which also gives `(1, 8, 11, 1)`, norm 53, for all pairs with
`N₁, N₂ ≤ 16`; the second term reaches its proved bound `(0, 3, 4)` at 14 beads.)

**Theorem 11.69 (a limit shape for bridges) [the abstract theorem — convergence,
compactness, convexity, the one-sided rate `β/M` for every family with (C), (E), (B) — V:
`SuperAdditive.hausdorff_limit`, `SuperAdditive.convex_limit`, `SuperAdditive.dist_limit_le`; that
bridges satisfy (C), (E), (B) is Lemma 11.68, P].**  Let `𝒟_N^{br} ⊂ ℝ⁴` be the set of `(h(x), g(x))/N`
over bridges with `N` beads.  There is a compact **convex** set `K^{br}` in the box with
`d_H(𝒟_N^{br}, K^{br}) → 0` (Hausdorff distance), and **every point of `𝒟_N^{br}` lies within `168/(N+3)`
of `K^{br}`**.  Consequently `𝒦 := {p : (p, g) ∈ K^{br}}` is a compact convex body of profile densities
(it has interior points: Proposition 11.72(d)),
`γ(p) := min{g : (p, g) ∈ K^{br}}` is a convex function `𝒦 → [0, 1]`, and the truncated epigraphs of the
finite-size functions `h/N ↦ γ_N^{br}(h)/N` (least gauche count of a bridge with profile `h`)
converge in the Hausdorff metric to `{(p, t) : p ∈ 𝒦, γ(p) ≤ t ≤ 1}`.
*Proof.*  *Fekete's lemma for sets.*  Let non-empty sets `Q_M ⊂ ℝ^d` satisfy: (C) for `q₁ ∈ Q_{M₁}`,
`q₂ ∈ Q_{M₂}` there is `q ∈ Q_{M₁+M₂}` with `|q − q₁ − q₂| ≤ β`; (E) for `q ∈ Q_M` there is `q′ ∈ Q_{M+1}` with
`|q′ − q| ≤ β′`; (B) `|q| ≤ RM`.  Then `E_M := Q_M/M` converges in the Hausdorff metric to a compact
convex `K`, and `E_M ⊂ K + B̄(β/M)` for every `M`.  Indeed, writing `M = km + r` and using (C) `k − 1`
times and (E) `r` times, every point of `E_m` is within `β/m + m(β′ + R)/M` of `E_M`; along
`M_{j+1} = M_j²` this produces, from any `q ∈ E_m`, a Cauchy sequence whose limit `q*` is within
`2(β + β′ + R)/m` of `q` and is approached by *every* `E_M` (apply the same estimate between `√M_j`
and `M ∈ [M_j, M_j²)`); so the set `K₋` of points approached by all `E_M` attracts all cluster
points, the two notions of limit coincide, and uniform convergence on the compact limit
follows from pointwise convergence of the 1-Lipschitz distance functions.  The one-sided
bound: `q ∈ Q_M` has `q_k ∈ Q_{kM}` with `|q_k/(kM) − q/M| < β/M` for every `k`.  Convexity: by (C), for
`q_m, q′_m ∈ E_m` and integers `a, b` the point `(aq_m + bq′_m)/(a + b)` is within `2β/m` of `K`.
*Application.*  `Q_M :=` the set of `(h, g)` of bridges with `M − 3` beads, `M ≥ 6`: (C) and (E) are
Lemma 11.68, `R = 36`; passing from `q/(N+3)` to `q/N` costs at most `3R/(N+3)`, in all
`(β + 3R)/(N+3) = 168/(N+3)`.
*Bookkeeping for the machine-checked form* (Scientific Discovery Division, SCI-REV-0002,
m1; the first version did not say it).  `SuperAdditive` quantifies (C), (E), (B) over all
indices `M ≥ 0`, and `SuperAdditive.hausdorff_limit` and `SuperAdditive.cover_sandwich`
assume `Q_M ≠ ∅` for all `M ≥ 1`, while the lattice gives `Q_M` from `M = 6` on.  Put
`Q_M := {0}` for `0 ≤ M ≤ 5`.  Then (B) and (E) are immediate (`Q_6 = {0}`: a bridge with three
beads has no pair and no torsion), and (C) holds with the same `β`: for `M₁, M₂ ≤ 5` take
`0`, which is the `(h, g)` of the rod when `M₁ + M₂ ≥ 6`; for `M₁ = k ≤ 5 < 6 ≤ M₂` append `k` beads
to the bridge in the zigzag of the linker, which by the height count of Lemma 11.68 costs
at most `(1, 6, 10; 1)` — one bond; three second neighbours each for `ℓ₁` and `ℓ₂`; `6 + 2 + 2`
third neighbours; the torsion `(b′, b, c₁)` — of norm `44 ≤ β` (`28`, `42`, `44` for
`k = 1, 2, ≥ 3`; checked by us on all 52 420 extensions of bridges with at most 11 beads).  The limit does not depend on the
first five sets.  Two more paper steps separate the Lean statements from the theorem: the
normalisation (`scaled Q M` is `(h, g)/(N+3)`: the term `3R/(N+3)` above, and for covers the
accuracy `ε₁N/(N+3)` in place of `ε₁`) and the norm (`cover_sandwich` uses
`max(‖Δp‖, |Δg|)`, the constants were computed for the sum, which is the larger).
The map from a set to its truncated epigraph is 1-Lipschitz for
the Hausdorff distance.  ∎
The estimate is one-sided: finite sets never stick out of the limit by more than `168/(N+3)`.
How fast they fill it is another question.  At the boundary the abstract hypotheses give
no rate (for `d = 1`, where the limit is a point, a super-additive sequence can converge
arbitrarily slowly), and Proposition 11.73 settles one boundary point.  In the interior
they do give one (the first version said here "nothing in this argument says how fast they
fill it"; corrected by the Scientific Discovery Division, SCI-REV-0006, finding M2):

**Proposition 11.69a (interior points are approached at rate `M^{-1/2}`) [P; Proposition A2.2
of the Scientific Discovery Division, SCI-REV-0006; proof re-derived by us; not
machine-checked].**  Let `Q_M ⊂ ℝ^d` satisfy (C), (E), (B) and `E_M = Q_M/M → K`.  If `E_m`
contains `d + 1` points whose convex hull contains `p`, then for every `M ≥ (d + 1)m`

    dist(p, E_M)  ≤  β/m + (d + 1)(β′ + R)·m/M .

If `p` is an interior point of `K`, such points exist for all `m ≥ m₀(p)`, and with `m ≈ √M`,
for all large `M`,

    dist(p, E_M)  ≤  c·M^{-1/2} + (d + 1)(β′ + R)/M ,        c = 2√(β(d + 1)(β′ + R)) ,

uniformly on compact subsets of the interior.  For bridges (`d = 4`, `M = N + 3`): `c ≈ 277`.
*Proof.*  Let `p = Σλ_i q_i/m` with `q_i ∈ Q_m`, `λ_i ≥ 0`, `Σλ_i = 1`, and `k_i = ⌊λ_i M/m⌋`; some
`k_i ≥ 1`.  By (C), used `Σk_i − 1` times, there is a point of `Q_{M′}`, `M′ = mΣk_i > M − (d + 1)m`,
within `β(Σk_i − 1) ≤ βM/m` of `Σk_i q_i`; by (E), used `M − M′` times, a point `q′ ∈ Q_M` within
a further `(d + 1)mβ′`; and `|Σk_i q_i/M − p| ≤ (d + 1)(m/M)R` because `0 ≤ λ_i − k_i m/M < m/M`
and `|q_i/m| ≤ R`.  For an interior point take a simplex in `K` with `p` in its interior: by
the convergence `E_m` has points near its vertices, and `p` stays in their hull.  ∎
So the rate `N^{-1/3}` of Proposition 11.73 is a *boundary* effect — it is proved at the
crystal vertex, an extreme point — while the interior fills at least at rate `N^{-1/2}`;
`m₀(p)` is not effective.  The proposition is not empty here: `K^{br}` has interior points in
`ℝ⁴` (the four exact points of Proposition 11.72(d) lie on the hyperplane
`g = 9p₃ − 3p₈ + p₁₁`, while at the density of an explicit bridge with 22 351 beads
`g − 9p₃ + 3p₈ − p₁₁ = 4.3`, against an uncertainty of `0.02`).  For an exact semigroup of
lattice points the classical theorem gives the rate `1/M` (see *Prior art* below).

**Lemma 11.70 (covering numbers are stable under Hausdorff convergence of truncated
epigraphs) [(a), (b) and the example of (d) V: `hasCover_upper_iff`, `hasCover_of_close`,
`hasCover_sandwich`, `hasCover_limit_point`, `not_hasCover_shifted`; (c) and the limit
statement of (d) P, elementary].**  For a compact `F ⊂ V × [0, G]` (`V` a finite-dimensional normed
space) let `N(F, ε)` be the least number of centres `a` among the first components of points of
`F` such that every `(p, g) ∈ F` has a centre with `L‖a − p‖ ≤ e·g + ε`, and `F^↑` the truncated epigraph
`{(p, t) : (p, g) ∈ F, g ≤ t ≤ G}`.
(a) `N(F, ε) = N(F^↑, ε)`: only the lower boundary matters.
(b) If `d_H(F, F′) ≤ η` (distance `max(‖Δp‖, |Δg|)`), then for every `ε`

    N(F′, ε + (2L + e)η)  ≤  N(F, ε)  ≤  N(F′, ε − (2L + e)η).

(c) `ε ↦ N(F, ε)` is nonincreasing, finite for `ε > 0` and right-continuous; so it has at most
countably many jumps.
(d) If `d_H(F_N^↑, F^↑) → 0`, then `N(F, ε) ≤ liminf N(F_N, ε) ≤ limsup N(F_N, ε) ≤ N(F, ε−)` for every `ε`: the
covering numbers converge at every `ε` that is not a jump of `N(F, ·)`, and they can fail to
converge at a jump (`F = {(0,0), (1,0)}`, `F_N = {(0,0), (1 + 1/N, 0)}`, `ε = L`).
*Proof.*  (b): move each centre of an optimal cover of `F` to a point of `F′` within `η`; a client of
`F′` is within `η` of a client of `F`, whose centre has moved by at most `η`:
`L‖a′ − p′‖ ≤ 2Lη + e·g + ε ≤ e·g′ + ε + (2L + e)η`.  (c): a maximal `ε/L`-separated subset of the compact
set of first components is a finite cover; right-continuity by compactness of the `k`-tuples
of centres.  (d) from (a)–(c).  ∎
*The convergence that matters* is therefore neither that of the whole sets (all gauche
counts) nor that of the graphs of the lower boundaries, but Hausdorff convergence of the
truncated epigraphs: convergence of the profile sets together with epi-convergence of the
least gauche densities.

**Theorem 11.71 (the limit of certificate sizes) [(a): the two-sided inequality V in
abstract form, `SuperAdditive.cover_sandwich`, given Lemma 11.68; the rest P; the numbers
computer-assisted].**  Put
`N_∞(ε₁) := N(K^{br}, ε₁) = min{|A| : A ⊂ 𝒦, ∀p ∈ 𝒦 ∃a ∈ A : L‖a − p‖_c ≤ eγ(p) + ε₁}`.
(a) *Bridges.*  For every `ε₁ > 0`

    N_∞(ε₁) ≤ liminf_N N^{P,br}_cov(ε₁N) ≤ limsup_N N^{P,br}_cov(ε₁N) ≤ N_∞(ε₁−),

with equality throughout — **the certificate sizes converge to the covering number of the
limit shape** — for all `ε₁` outside an at most countable set, the set of jumps of `N_∞`,
which is not identified because `K^{br}` is not known: **no accuracy is known to be
non-exceptional, in particular not `ε₁ = ½` or `¼`**, and at an exceptional accuracy only
the two-sided inequality is proved (Scientific Discovery Division, SCI-REV-0002, m2); and
for every `N`,
`N_∞(ε₁ + (2L+e)d_N) ≤ N^{P,br}_cov(ε₁N) ≤ N_∞(ε₁ − (2L+e)d_N)` with `d_N = d_H(𝒟_N^{br}, K^{br}) → 0`: *the covering
number at chain length `N` is the limiting one at an accuracy shifted by `(2L + e)d_N`*.
(b) *All walks, unconditionally.*  Every subsequence of the truncated epigraphs of walks
has a further subsequence converging to a compact `F*` with `(K^{br})^↑ ⊂ F* ⊂ 𝒦₂ × [0,1]` (`𝒦₂` the
polytope of Proposition 11.72), along which `N^P_cov(ε₁N) → N(F*, ε₁)` off a countable set.  If
points `(p_i, g_i) ∈ K^{br}`, `i ≤ k`, satisfy `L‖p_i − p_j‖_c > e(g_i + g_j) + 2ε₁` pairwise, then
`liminf_N N^P_cov(ε₁N) ≥ k` (no centre covers two of them); and for every `N`, `N^P_cov(ε₁N)` is at most
the largest number of profile densities at pairwise distance `> ε₁/L`, hence at most
`vol(X + B(ε₁/2L))/vol B(ε₁/2L)` for every convex `X` that contains them (`B` a ball of `‖·‖_c`).
(c) *Numbers* (`e = 1`; measured at 27 beads: 15, 28–31, 2, 3):

| `(L, ε₁)` | upper bound for **every** `N` (bulk box) | upper bound for the limsup (`𝒦₂`) | lower bound for the liminf (packing in the hull of the proved points of `K^{br}`; in brackets the first version, in `T₀`) | proved at `N = 1 000` / `5 000` | estimate of the limit, if there is one **[N]** | Proposition 11.49(a) |
|---|---|---|---|---|---|---|
| `(1, ½)` | 26 437 | 3 627 | **116** (50; 52) | ≥ 26 / ≥ 35 | 150–350 | `10^{1387}` |
| `(1, ¼)` | 191 833 | 23 272 | **451** (157; 162) | ≥ 53 / ≥ 77 | `≈ 10³` | `10^{2774}` |
| `(⅕, ½)` | 392 | 93 | **8** (7) | ≥ 5 / ≥ 6 | 7–10 | `10^{277}` |
| `(⅕, ¼)` | 2 195 | 393 | **19** (14) | ≥ 9 / ≥ 12 | 20–35 | `10^{555}` |

(*The lower bounds for the liminf* **[P, computer-assisted; Scientific Discovery Division,
SCI-REV-0002, findings M2 and N3; re-verified by us: the ten bridges from coordinates with
own lattice code, the four packings and their pairwise condition in exact rational
arithmetic with own code, the argument by hand]**.  The first version of this column — 50,
157, 7, 14, with the coordinator's own greedy packings 52 and 162 — used only the triangle
`T₀` of Proposition 11.72, where `γ = 0`.  But Theorem 11.69 turns every explicit bridge
with `N` beads into a point of `K^{br}` within `168/(N+3)` of its density, and `K^{br}` is
convex.  Take the four exact points of Proposition 11.72(d) — rod, row of stems, crystal,
helix — and the densities `q_i` of ten explicit bridges: the nine periodic systems of
`S_REPORT.md` §4.2 cut from a box of side 64 (12 041 to 33 988 beads) and the bridge with
166 199 beads of Proposition 11.72(e); `δ_i = 168/(N_i + 3) ≤ 0.014`, and `δ_i = 0` for the
exact points.  A convex combination `(p, g) = Σλ_i q_i` is within `d = Σλ_iδ_i` of a point of
`K^{br}`, so `k` combinations with

    L‖p_k − p_l‖_c  >  e(g_k + g_l) + 2ε₁ + max(L, e)(d_k + d_l)        for all pairs

give `k` points of `K^{br}` that satisfy the hypothesis of (b).  The reviewer's packings have
116, 451, 8 and 19 points (an own greedy search of ours in the same hull, verified in the
same way: 106, 413, 8, 19); they are greedy, not optimal, and use nothing about periodic
systems or routing.  (With finite verified walks, the rod and the helix alone the reviewer
reports at least 100 at `(1, ½)`; not re-verified by us.)  The proved `8` cuts the estimate
`7–10` of the sixth column to `8–10`.  *The upper bounds* are volume ratios rounded to the
nearest integer — `26 437.0`, `191 833.0`, `392.2`, `2 194.6` for the box and `3 626.5`,
`23 272.0`, `92.5`, `392.8` for `𝒦₂` — so the floors `2 194`, `3 626`, `92`, `392` are valid as
well (m5).  *None of the four accuracies is known to be non-exceptional* (m2): the columns
bound `liminf` and `limsup`, not a limit.  "Proved at `N`": explicit lamellae
prolonged by a tail to exactly `N` beads, exact counts, pairwise uncoverable — so **the growth
seen up to 27 beads provably continues**: at least 22 and 43 evaluations at 500 beads where
15 and 28–31 suffice at 27.  The estimates of the sixth column are covering numbers of an inner
model of the limit shape — the hull of all periodic chain systems with at most 12 sites
per cell, which lies in `K^{br}` only if the routing sketch of Proposition 11.72 holds —
bracketed by a packing and a greedy cover on a grid; they are not bounds, and they estimate
a limit whose existence at these accuracies is not proved.)
*Proof.*  (a) Theorem 11.69 and Lemma 11.70.  (b) Blaschke selection, Lemma 11.70(d), the
triangle inequality, and a volume count (a maximal separated set is an internal net, and
`e·γ ≥ 0`).  ∎
So for this model Proposition 11.49(a)'s `10^{1387}` is replaced by a bracket `[116, 3 627]` for
every limit point of the certificate sizes of all walks **[P, computer-assisted]** — a
factor 31 between its ends, with the value at 27 beads (15) a factor of more than 7 below
every limit point — and by `26 437` for every chain length.  That the sizes converge is
proved for bridges off the exceptional set of accuracies and is a conjecture for all walks
**[C]**.  That the limit is a few hundred, 10 to 40 times the values at 27 beads, is an
estimate **[N]**; what is proved about that ratio is that it lies between `116/15 ≈ 8` and
`3 627/15 ≈ 240`.  (The first version had the bracket `[50, 3 627]` and went on: "The plateau is
real, it is in the hundreds, and it is 10 to 40 times the values at 27 beads".  Withdrawn
after the review SCI-REV-0002 of the Scientific Discovery Division, findings M1 and M2: at
this accuracy "real" is a theorem for neither class of chains.)

**Proposition 11.72 (what the limit shape looks like: outer bounds for every walk, inner
points from explicit bridges) [P; computer-assisted with exact certificates].**
Write `p = (p₃, p₈, p₁₁)` for a profile density.
(a) *By hand.*  For every walk `h₈ ≥ 4h₃ − 2`, `h₈ ≥ 6h₃ − N − 4`, `h₈ ≤ 2h₃ + 3N + 3` (Lemma 11.67
and, for `0 ≤ d ≤ 4`: `C(d,2) ≥ 2d − 3` and `≥ 3d − 6` on occupied sites for the first two; for
the third, `C(d,2) ≤ 3d/2` on vacant sites and `C(d,2) ≤ (5d − 8)/2` on occupied sites with
`d ≥ 2`, with `3/2` more for each of the at most two beads with `d = 1` — the first version
quoted `≤ 3d/2` alone, which gives no more than `e₈ ≤ 6N`; Scientific Discovery Division,
SCI-REV-0002, m4): the `(p₃, p₈)` projection of every limit point lies
in `conv{(0,0), (½,2), (1,5), (0,3)}`.
(b) *Eleven inequalities for all finite site sets.*  For a finite set of `N` sites, `n_E` of
which have fewer than two occupied neighbours, and each row `(c; b; M)` of

    (−1,0,0; 0; ½)   (4,−1,0; 0; 5)   (6,−1,0; 1; 6)   (−2,1,0; 3; 2)   (−1,1,−1; 0; 3)   (−1,2,−1; 3; 4)
    (−4,2,−1; 2; 6)   (3,4,−3; 5; 6)   (6,−2,1; 2; 6)   (0,−1,2; 7; 1)   (−3,0,2; 9; 3)

`c₃(e₃ − N) + c₈(e₈ − N) + c₁₁e₁₁ ≤ bN + 2M·n_E`; in particular `c·h ≤ bN + 4M + c₃ + 2c₈` for every walk.  The
polytope `𝒦₁ = {c·p ≤ b}` has 12 vertices and volume `3.2269` — 10.8 % of the bulk box.
(c) *With the chain marked.*  Every limit point `(p, q)` of `(h, g)/N` over walks satisfies the
rows of (b) with `(−4,2,−1; 2)` strengthened to `(−3,2,−1; 2)` and the further row `(−3,4,−3; 2)` — a
polytope `𝒦₂ ⊂ 𝒦₁` with the 12 vertices

    (0,0,0) (0,0,2) (0,1,4) (0,2,2) (0,2,9/2) (0,3,4) (0,3,9/2) (½,2,3/2) (½,2,3) (½,7/2,7/2) (½,4,9/2) (1,5,6)

and volume `3.125`, 10.4 % of the bulk box — and three lower bounds for the gauche density:

    q ≥ 2p₁₁ − 5p₃ − 8,        q ≥ 2p₁₁ − p₈ − 7,        q ≥ p₁₁ + p₈ − 4p₃ − 7 :

more than four third-neighbour pairs per bead force gauche torsions.
(d) *Inner points.*  The all-trans rod is a bridge for every `N`: `(0,0,0; 0) ∈ K^{br}`.
Rung-folded lamellae — an `M × Q` block of parallel all-trans stems of `ℓ` periods, traversed in
snake order, consecutive stems joined by a single lattice bond — are bridges with
`g ≤ 3(MQ − 1)`; hence `(½, 2, 3/2; 0)` (one row of stems) and `(1, 5, 6; 0)` (the crystal) belong to
`K^{br}`, and by convexity **`γ = 0` on the triangle `T₀ = conv{(0,0,0), (½,2,3/2), (1,5,6)}`**.
*A fourth exact point* **[P; found by the Scientific Discovery Division, SCI-REV-0002, N1;
verified by us with own lattice code for every `N ≤ 200` and up to 10 007 beads]**: the
all-gauche `4₁` helix — bond indices `0, 1, 2, 3, 0, 1, …`, every bond an up-bond — is a
bridge for every `N`, with `h = (0, 0, N − 3)` and `g = N − 3` (four bonds add up to
`(0, 4, 0)`, of squared length 16, above the cutoff).  So **`(0, 0, 1; 1) ∈ K^{br}`**.  It is off
the plane of `T₀`, hence `𝒦` contains a tetrahedron of volume `1/12` and has interior points —
which the word "body" in Theorem 11.69 presupposes and the first version did not argue
(m6).  The helix point lies on the *upper* boundary (`g ≤ h₁₁` for every walk); the least
gauche density near `(0, 0, 1)` is much smaller: an explicit bridge with 12 041 beads has
the density `(0.006, 0.078, 1.012; 0.110)`.
(e) *`γ` is not identically zero.*  An explicit bridge with 166 199 beads has
`2h₁₁ − 5h₃ − 8N = 37 401 = 0.225N`; by Theorem 11.69 a point `(p*, g*)` of `K^{br}` lies within `0.00101` of its
density, and by (c) `γ(p*) ≥ 0.22`.
*Proof of (b), (c).*  The cluster method for ground states of lattice gases.  For a lattice
bond `(v, w)` take the eight sites `v, w`, the other neighbours `u₁, u₂, u₃` of `v` and `z₁, z₂, z₃` of `w`,
labelled so that `(u_j, v, w, z_j)` is trans.  Let `μ` be the number of bonds with a given
occupation pattern of the cluster — both orientations, averaged over the point group —
divided by `2N`.  Then `μ(v occupied) = 1`; `μ` is invariant under the 12 symmetries of the
cluster; the marginal on the star of `v` is invariant under all permutations of the four
neighbours; and by Lemma 11.67 `e₃/N = 2μ(vw)`, `e₈/N = μ((C(d_v,2) + C(d_w,2))/2)`,
`e₁₁/N = μ(Σ_{j≠k} u_jz_k)`.  Each row is certified by integer multipliers `y₁,…,y₆` for the star
relations and `y₀ = b + c₃ + c₈` such that the symmetrised function
`c₃·2[v][w] + c₈(C(d_v,2)+C(d_w,2))/2 + c₁₁Σ_{j≠k}u_jz_k − Σ_k y_k r_k − y₀[v]` is `≤ 0` on every pattern in which the
occupied centres have at least two occupied neighbours, and `≤ M` otherwise; integrate
against `μ`.  For (c) the two chain bonds of every occupied centre are marked (340
configurations), the gauche density is `2μ(vw marked, continued at v and at w by bonds with
different indices)`, and the two ends of the chain carry mass `O(1/N)`.  ∎
(The eleven certificates of (b) were verified by the coordinator in exact arithmetic on all
255 non-empty patterns with own code; both programmes were re-formulated independently and
re-solved: their support functions coincide with those of `𝒦₁` and `𝒦₂` in 400 random directions
to `10⁻⁸`, the maxima of the three gauche functionals are `8, 7, 7`.  For (c) the coordinator
found own integer multipliers for the twelve rows and the three gauche bounds — 339
marked configurations, 13 star relations — and verified them in exact arithmetic
(`s_check7.py`); the workstream has its own exact certificates.)
*Finite-`N` form of (c)* **[a statement of the Scientific Discovery Division, SCI-REV-0002, N5:
P, computer-assisted with exact certificates of its own; not re-derived by us — we tested
the five inequalities on all bridges with at most 14 beads and on the explicit bridges,
where they are far from tight, and re-computed the volume counts from its constants]**.
For *every* walk with `N` beads

    −3h₃ + 2h₈ − h₁₁ ≤ 2N + 53,        −3h₃ + 4h₈ − 3h₁₁ ≤ 2N + 65,
    g ≥ 2h₁₁ − 5h₃ − 8N − 143,     g ≥ 2h₁₁ − h₈ − 7N − 70,     g ≥ h₁₁ + h₈ − 4h₃ − 7N − 128

(the certificates of (c) evaluated on the configurations whose centre is a chain end;
constants not optimised).  With the eleven finite rows of (b) this is an outer polytope
for every `N`, and the volume count of Theorem 11.71(b) becomes a bound for every chain with
at least `N` beads: at `L = 1`, `N^P_cov(N/2) ≤ 4 650`, `3 728`, `3 636`, `3 627` for chains with at
least `10²`, `10³`, `10⁴`, `10⁵` beads — the bound for the limsup in finite form.
*How much of the body is known.*  **Proved [P, computer-assisted; Scientific Discovery
Division, SCI-REV-0002, findings M2 and N2; re-computed by us in exact rational
arithmetic]:**

    1.56  ≤  vol 𝒦  ≤  3.125 ,

5.2 % to 10.4 % of the bulk box that Proposition 11.49(a) uses.  The upper bound is (c).  The
lower bound: let `C` be the hull of the four exact points of (d) and of the profile densities
of the ten explicit bridges named after Theorem 11.71(c), and `δ = 168/12 044`, the largest of
their `168/(N+3)`.  Each density is within `δ` of a point of `𝒦`, so — compare support
functions — `𝒦` contains the erosion `{x : x + δ𝔹_c ⊂ C}`, `𝔹_c` the unit ball of `‖·‖_c`: a
polytope of volume `1.5632` (`vol C = 1.6317`).  Three vertices of `𝒦₂` are proved to belong
to `𝒦`: rod, row of stems, crystal.  **Beyond that [N]:** exhaustive enumeration of
all periodic chain systems with at most 12 sites per cell (`1.2·10⁹` systems, 5 680 distinct
densities) gives an inner hull of volume `2.22` — if their densities are attained by
bridges, which is proved for lamellae only and is a sketch otherwise (a routing lemma for
`O(W²)` linkers on the surface of a box is missing; finite bridges built from nine such
systems approach the ideal densities like `1/W`).  So `vol 𝒦 ≈ 2.2` or more is expected, not
proved — a thin body in any case; two further vertices of `𝒦₂`, `(0,3,4)` and `(½,4,9/2)`, are
attained by periodic systems and approached within 10 % (in `‖·‖_c`) by explicit bridges with
22 351 and 27 144 beads; seven vertices of `𝒦₂` are not attained by any chain system with at
most 12 sites per cell; and the inner volume still grows with the cell size (`+4 %` from 11
to 12).  (The first version read "`2.2 ≲ vol 𝒦 ≤ 3.125` … with five vertices settled", which
counted the sketch as a proof: SCI-REV-0002, M2.)  At `(0, 12/5, 22/5)` the
bound of (c) and a periodic system agree: `γ = 4/5` there (given the sketch).

**Proposition 11.73 (the surface law: the shape converges at rate exactly `N^{-1/3}` at its
compact end) [P].**  For every finite set `S` of `N` sites `e₃(S) ≤ 2N − 2^{-2/3}N^{2/3}` and
`e₈(S) ≤ 6N − 3N^{2/3}`; hence for every walk

    ‖N^x‖₁ = 9h₃ + 4h₈ + h₁₁  ≤  35N − 17.6·N^{2/3} + 17 ,

every point of `𝒟_N` (walks or bridges) is at distance at least `17.6·N^{-1/3} − 17/N` from the crystal
vertex `(1,5,6; 0) ∈ K^{br}`, and `d_H(𝒟_N^{br}, K^{br}) ≥ 17.6·N^{-1/3} − 17/N`; lamellae with `M ≈ Q ≈ ℓ ≈ N^{1/3}` come
within `O(N^{-1/3})`.
*Proof.*  The bonds of types `a₀` and `a_f` (`f = 1, 2, 3`) partition the lattice into parallel rods;
a rod that meets `S` carries at least two bonds between an occupied and a vacant site; a
bond of type `a₀` lies on three such rods, one of type `a_f` on one; so the number `∂` of boundary
bonds satisfies `3∂ ≥ 2Σ_f ρ_f`, `ρ_f` the number of rods of family `f` that meet `S`.  The larger
sublattice part `S_A` has at least `N/2` sites, `ρ_f` is at least the size of its projection along
the rod direction, and by the Loomis–Whitney inequality the product of the three projections
is at least `|S_A|²`: `Σ_f ρ_f ≥ 3(N/2)^{2/3}`, `∂ ≥ 2(N/2)^{2/3}`, `e₃ = (4N − ∂)/2`.  The same count of lines
inside each face-centred sublattice gives the bound on `e₈`.  ∎
*The second-neighbour half is in the sphere-packing literature, with a better constant*
**[P from K: Bezdek's theorem as read by the Scientific Discovery Division (SCI-REV-0006,
findings W9 and M3, its Proposition A2.3), not read by us; the arithmetic re-done by us]**.
Two sites are at squared distance 8 exactly when they are nearest neighbours in the same
face-centred sublattice, so `e₈(S)` is the sum of the contact numbers of the two sublattice
parts of `S`, each a finite set of balls of the face-centred cubic lattice packing.  Bezdek
(2012, Theorem 1.1(ii)): `n ≥ 2` balls of a lattice packing have fewer than
`6n − (3(18π)^{1/3}/π)·n^{2/3} = 6n − 3.665…n^{2/3}` contacts.  Since `t ↦ t^{2/3}` is subadditive,
`e₈(S) < 6N − 3.665·N^{2/3}` for every set of `N ≥ 2` sites; along a walk the sublattices
alternate, both parts have at least `(N − 1)/2` sites, and `e₈(S) < 6N − 4.617·N^{2/3} + 3.1`.
With the bound on `e₃`, for every walk

    ‖N^x‖₁  ≤  35N − 24.1·N^{2/3} + 29.4 ,

and `17.6·N^{-1/3} − 17/N` may be replaced by `24.1·N^{-1/3} − 29.4/N` in the statement.  (The
first version gave `e₈(S) ≤ 6N − 3N^{2/3}` without naming this relative.  For the bound on
`e₃` that division found no source either.)
*When the shape is resolved* **[P; Scientific Discovery Division, SCI-REV-0002, N4; the
arithmetic re-done by us]**: `d_H(𝒟_N^{br}, K^{br}) ≥ 17.6·N^{-1/3} − 17/N ≥ ½ = ε₁/L` for every
`N ≤ 43 512` (and `≥ ¼` for every `N ≤ 3.4·10⁵`; with Bezdek's constant `≥ ½` for every
`N ≤ 1.1·10⁵`).  For all chains shorter than about `4·10⁴` beads the finite profile set
misses a part of the limit body by more than one covering radius of the instance
`(L, ε₁) = (1, ½)`.  This is a statement about the shape, not about the covering numbers,
which are not monotone under inclusion when the centres are internal.
*In the exact data* **[N]**: `max ‖N^x‖₁/N = 35(1 − k_N N^{-1/3})` with `1.71 ≤ k_N ≤ 1.86` for every `N` from 8
to 27 (lamellae: `k ≈ 2.5` up to 31 880 beads; proved: `k ≥ 0.50`, and `k ≥ 0.689` with Bezdek's
constant, each up to a term of order `N^{-2/3}`).  The finite-size table of the
other division — 38 % of the bulk extent at 27 beads — is this law: `1 − 1.84/3 = 0.39`.  Half
of the bulk extent needs about 47 beads, 80 % about 730, 90 % about 5 800: **enumeration
cannot see the limit**, and the right computational objects are the limit shape itself
(extreme points = ground states of three-shell lattice gases with a stiffness term) and
constructed conformations of `10²`–`10⁴` beads.  For the covering numbers the correct form of
"a correction of order `N^{-1/3}`" is the shift of the accuracy in Theorem 11.71(a): they are
integers, and for a non-exceptional `ε₁` their difference from the limit is eventually zero.

**Proposition 11.74 (single-flip constants) [P; the lower bound by an explicit family
computed for arms up to 30 and extended by periodicity].**  Let `c_j^{sf}` be the largest profile
distance between two conformations of the chain that differ in torsion `j` only, and
`d_j = min(j, n + 1 − j)`.  For `d_j ≥ 5`:

    14·d_j − 15  ≤  c_j^{sf}  ≤  70·(d_j + 3).

*Proof.*  Lower bound: the hairpin `t^a g g g t^b` (two adjacent stems joined by a rung) and the
conformation with the middle fold torsion set to trans: the hairpin has `(1, 4, 3)` pairs per
period of overlap, the opened one `O(1)`.  Upper bound: a flip moves the shorter arm rigidly,
only pairs (moved bead, fixed bead) change, and a moved bead has at most `2, 10, 12` partners
of the other side at the three distances.  ∎
The lower bounds for per-torsion formats (Theorem 11.37 with the envelope property of
single-flip constants) use the constants only through `Σ_j e^{−tLc_j}`, which is monotone: they
need **`c_j ≥ κd_j` and nothing else**, and that is now a theorem for this chain (`κ = 14`,
asymptotically).  A linear *law* is neither needed nor true: an arm of `d` beads can be
surrounded by up to eight stems of the other arm if `d ≪ n`, by one if `d ≈ n/2`, so the
expected form is `c_j ≈ nΦ(d_j/n)` with `Φ` concave **[C]** — the shape reported by the other
division (ratios `c_j/d_j = 58, 54, 41, 35, 32, 28, 24, 21` at 16 torsions).
*Checked against exact data* (Computational Research Division, ENG-RES-0009; exhaustive
single-flip constants for 3–16 torsions): the two bounds hold in all 36 pairs `(n, j)` with
`d_j ≥ 5` that exist up to 16 torsions (the lower bound is never closer than `21`, the
constants stay below `0.29` of the upper bound) — a check of the statement, not of the
proof.  **The conjectured scaling form is not visible at these sizes:** at fixed `d_j/n` the
ratio `c_j/n` still rises (at the centre of the chain from `7.25` at 8 torsions to `10.6` at
16), while at fixed small `d_j` the constant itself is nearly independent of `n`; the data
are closer to "a function of `d_j` with a plateau towards the centre".  The conjecture is
about a limit that enumerable chains have not reached, and it stays a conjecture.

**Conjecture 11.75 (unrestricted walks have the same limit shape) [C].**  `𝒟_N → K^{br}` in the
Hausdorff metric; all that certificates need is the weaker `𝒟_N^↑ → (K^{br})^↑`, and then
`lim_N N^P_cov(ε₁N) = N_∞(ε₁)` off a countable set (Lemma 11.70).
*What is proved towards it.*  (i) `K^{br} ⊂ liminf 𝒟_N`, and every limit point lies in
`𝒦₂ × [0,1]` above the three gauche bounds (Proposition 11.72).  (ii) *It is a ground-state
statement*: by convexity of `K^{br}` the conjecture holds iff for every energy
`E_u = −u₃h₃ − u₈h₈ − u₁₁h₁₁ − u_g g` — a pair interaction on three shells plus a stiffness term — walks
and bridges have the same ground-state energy per bead (for the epigraph version: every
such energy that does not reward gauche torsions).  This holds in every direction that
belongs to one of the three proved vertices — rod, one row of stems, crystal — about two
thirds of all directions for the measure on directions that the workstream used (`0.67`; the
figure depends on the measure — `0.77` for two other natural ones — and concerns directions
with `u_g ≤ 0` only: Scientific Discovery Division, SCI-REV-0002, m7, not re-computed by us);
in particular the largest numbers of pairs per bead at each
distance and the largest `‖N^x‖₁/N` are the same for walks and bridges in the limit.
(iii) *Decomposition principle*: a walk whose `(h, g)` agrees up to `η` with the sum over `k`
bridges of `N + O(η)` beads in total is within `(168k + 37η)/(N − η)` of `K^{br}`; so the conjecture is
equivalent to "every walk has the `(h, g)` of `o(N)` bridges up to `o(N)`" — the bridges need not
be pieces of the walk.  (iv) *No local surgery*: a site set that contains a double strand
(two adjacent parallel rods and nothing else over `2ℓ` levels) is not within `(ℓ − 3)/2` sites of
the site set of any bridge that starts below it (a parity argument: the bridge would have
to cross each level of the strand an even number of times).  So "expose a buried end by
changing `o(N)` sites" is false, and any proof must use convexity non-locally, as in (iii).
*The obstruction* (heuristic): after cutting a walk into pieces of size `W`, pieces with few
strands or with strand ends that are dense on their surface can be re-threaded cheaply;
the hard case is `1 ≪ k ≪ W²` strands that interact inside a piece and splay out at its
surface, at every scale.  No counterexample is known.
*Evidence* **[N]**: for `N` from 11 to 23 the distance from the profile set of walks to that
of bridges with one more bead is 3 to 6 units of `‖·‖_c` and does not grow (per bead it falls
from 0.5 to 0.22); the covering numbers of bridges equal those of walks zero to three beads
shorter (the first version said "two to three"; in the workstream's own table bridges and
walks agree at 8 and at 12 beads — SCI-REV-0002, m7).
At these sizes no end is buried deeper than one layer, so this has little power
against the mechanism above.
*In the literature* (workstream S; one paper read in full, the rest as abstracts): for
self-avoiding walks with a contact energy the limiting free energy is known to exist for
polygons at every interaction strength; for walks it is proved to exist, and to equal that
of polygons, only for repulsive interactions (existence also for weak attraction); equality
in the attractive regime is a standing conjecture, and the buried end is the obstacle there
too.  The present question is weaker (the support of the
joint density of `(h, g)`: ground states, no entropy), which is what makes the non-injective
argument (iii) available.

*What this changes in §11.17.*  The sentence "the certificates of the profile format are
bounded independently of the chain length at extensive accuracy, by a numerically vacuous
bound" now reads, for the lattice chain: bounded by `26 437` at every length; for every
limit point at `(L, ε₁) = (1, ½)`: between 116 and 3 627 **[P, computer-assisted]**; that the
sizes converge is proved for bridges off a countable, unidentified set of accuracies and is
a conjecture for all walks **[C]**; our estimate of the limit is a few hundred and of the
chain length at which it is approached `10³`–`10⁵` beads or more **[N]** (the first version said
"by `3 627` in the limit …, at least 50 in the limit, most likely a few hundred, reached at
`10³`–`10⁵` beads"; SCI-REV-0002, M1 and M2).
Off-lattice nothing of this is proved: there the profile is a function,
not a point of `ℤ³`, the number of resolvable degrees of freedom at accuracy `ε₁` is of the
order `S_c·M·L/ε₁` (`M` pairs per bead within the cutoff), and the plateau is exponential in
that number — which is why growth looks geometric at every size enumerated (a heuristic
estimate under stated assumptions gives `e^{50}` or more for `L = 1`; workstream S, §7.3).  The
conclusion of §11.17 stands and is sharper: what governs the cost is the dimensionless
ratio `L·S_c·M/ε₁`, polynomially on a lattice, exponentially off it — a heuristic reading,
not a theorem (SCI-REV-0002, m8: the first version left the sentence unlabelled).  On a
lattice the proved bound is a polynomial in `L/ε₁` whose degree is the number of distances
below the cutoff, which grows with `S_c`; off-lattice "exponentially" is the upper bound of
Proposition 11.49(a) together with the growth observed up to 15 beads, and no lower bound
of that form is proved at extensive accuracy.

*Falsification harness.*  XVIII.1 (site-set and local counting formulas, the by-hand and
the eleven inequalities on all walks up to 10 beads, lamellae and random finite site sets,
the isoperimetric bounds), XVIII.2 (the concatenation lemma: uniqueness of the placing
symmetry, bridge, error intervals, the gauche rule; one more bead), XVIII.3 (the stability
lemma on random finite sets, the extremal two-point instance on which the constant `2L + e`
is attained, and the failure of convergence at a jump), XVIII.4 (the cumulative norm
against the weighted form), XVIII.5 (hairpins and single flips), XVIII.6 (the eleven dual
certificates in exact arithmetic); 21 mutations, all detected; and the documented
refutation DEAD.18 — the weighted form of the coordinator's brief fails already between two
conformations with 7 beads.  Not in the harness: the marked programme of Proposition
11.72(c), the 166 199-bead bridge, the numbers of Theorem 11.71(c) (coordinator checks);
nor what the review SCI-REV-0002 added or used: the exhaustive test of Lemma 11.68 on all
pairs of bridges with at most 13 beads (four minutes of compiled code there), the helix
point, the packings behind the new lower bounds, the finite-`N` rows.

*Not done.*  Conjecture 11.75.  Whether `ε₁ = ½` or `¼` is a jump of `N_∞`.  The exact shape of
`𝒦` (proved inner volume `1.56`, `2.22` given the routing sketch, outer `3.125`; seven doubtful
vertices) and hence `N_∞` to better than the factor 31 of the proved bracket.  The routing
lemma that would put every periodic chain system into `K^{br}`.  Rings (a sketch).  Finite-`N`
constants for the marked programme of our own (the reviewer's are recorded in Proposition
11.72).  A rate for the whole body (the compact end is settled at `N^{-1/3}`, interior points
at `N^{-1/2}` or better, nothing uniform).  Any rigorous statement about *when* the covering
numbers are near their limit points.  Anything off-lattice.  Machine-checking of the
lattice lemmas 11.67, 11.68 and of Proposition 11.69a (the abstract limit theorems are
checked).

*Prior art* (workstream S; search summaries and abstracts except where stated; sharpened
by the Scientific Discovery Division, SCI-REV-0002 and SCI-REV-0006 W8 — what is said about
the two sources named first rests on *its* reading, we have read neither).  **The abstract
part of Theorem 11.69, "Fekete's lemma for sets", is a known special case / reformulation,
not a new theorem.**  In exact form — no error term, sets that contain the origin, dimension
two — a set-valued Fekete lemma is in print: Permuter–Weissman, *Capacity region of the
finite-state multiple access channel with and without feedback*, arXiv:0708.0271, Lemma 23
and Corollary 24 (read in full by the reviewer of SCI-REV-0002).  For an exact semigroup of
lattice points the limit is the **Newton–Okounkov body** of a graded semigroup (Khovanskii;
Kaveh–Khovanskii, Ann. of Math. 176 (2012), arXiv:0904.3350; introduction, §1.1 and Theorem
1.6 read by the reviewer of SCI-REV-0006), whose approximation theorem is *stronger*:
interior lattice points are eventually all attained, which gives the rate `1/M` in the
interior where Proposition 11.69a gives `M^{-1/2}`.  The version here allows a bounded additive
error and real points, has increments in place of "contains the origin", and an explicit
one-sided rate: a routine extension.  Whether the statistics of bridges can be re-bookkept
as an exact semigroup is a request of that division (SCI-REV-0006, T-4) that is not decided
here.
Limits and concave density functions for supermultiplicative models of walks and polygons
(Janse van Rensburg; Theorem 11.69 is the set-valued version for this model); the free
energy of interacting self-avoiding walks and polygons (Tesi, Janse van Rensburg,
Orlandini, Whittington 1996; Bennett-Wood et al. 1998, read in full: "little else has been
proved rigorously" for attraction; Ueltschi 2002 and Hammond–Helmuth for weak
self-attraction); the surface term of collapsed polymers (Owczarek, Prellberg, Brak 1993);
the cluster / configuration-polytope method for ground states of lattice gases
(Kanamori; Kaburagi–Kanamori; the "basic polytope method"), of which Proposition 11.72(b),
(c) are an application.  Not found: the site-set reduction used as a relaxation for profile
sets; the inequalities of Proposition 11.72; the limit shape for `(h, g)` of diamond-lattice
bridges; the stability lemma for covering numbers with position-dependent radii (it is
elementary); Proposition 11.74.  "Not found", not "new".  The Scientific Discovery Division
did not find the specific body, its inequalities or the identification of a limiting
certificate size with a covering number of it either (three generic searches, SCI-REV-0002;
SCI-REV-0006 classifies the limit shape of the lattice model as a plausibly original
generalisation); it did find the second-neighbour half of Proposition 11.73 (Bezdek 2012).

### 11.23 Known parts with interactions, first case: a function of the type (mean-field models, one phase or two)

§11.20 treated a known part with independent sites (a field).  The largest open item of the
query-complexity theory was a known part *with interactions*.  This section treats the first
case, in which the theory can be carried through almost completely: a known part that is a
function of the type, `f(x) = n·φ(|x|/n)` — the mean-field (Curie–Weiss) models, with one
phase or with two — so that the reference measure `π ∝ e^{−f}` is **exchangeable** (uniform
on every type class) but not a product measure.  Workstream T
(`docs/workstreams/T_REPORT.md`) did the work; four findings:

1. **Symmetry alone settles the non-adaptive problem and the hardest symmetric instance, for
   every `n`.**  For every exchangeable `π`: sampling uniformly in every type class (the
   flat-histogram, "multicanonical" sample) is optimal among non-adaptive algorithms up to a
   polynomial factor, and the flat-histogram instance `H` is the hardest instance among
   those that are functions of the type (Theorem 11.76).
2. **A single-letter theorem for every rate function.**  The cost of *every* algorithm at a
   symmetric instance, with or without a hint, has the exponent `R_λ(ε₁)`, a supremum over
   *block profiles* of a finite-dimensional minimum (Theorem 11.78); for a convex rate
   function (one phase) everything of §11.20 except the nested algorithm carries over
   (Theorem 11.80).
3. **With two phases the extremal perturbations are shells in the barrier type class — not
   cones, and beyond a small accuracy not even sets around one centre.**  The cone formulas
   of §11.20 fail by a factor of more than two; cones around *shells* restore the pair
   identity; and for accuracy rates above `e₀ ≈ 0.0018` profiles that constrain only part
   of the coordinates do strictly better than every set built around one centre
   (Proposition 11.82).
4. **Ferromagnets are never harder than the uniform cube, and a shallow barrier can be
   invisible:** for the zero-field model at moderate slopes (`u = 1`; `u ≤ 2` on the
   referee's grid) the exponents are *equal* to the uniform cube's up to a coupling
   `βJ*(e, u) > 1` beyond the critical one; for large slopes at small accuracies the
   junction comes earlier, but still beyond the critical coupling (Proposition 11.81).

Open: the exponent of adaptive algorithms without a hint for an interacting known part
(the nested algorithm of Theorem 11.64 does not transfer as it stands; for ferromagnets
it is at most the uniform cube's, Proposition 11.81(c)), and the value of the
single-letter supremum beyond `e₀` with two phases.

**Status of this section.**  Paper proofs by workstream T, **refereed** by the independent
referee R10 (`docs/reviews/R10_referee_report.md`; own code, three inner solvers that share
no approximation, about ninety numbers recomputed): **no critical finding**; every
statement labelled as proved is proved, some after small repairs that are now in the
text — in particular Theorem 11.78(b), the isoperimetric theorem for every rate function,
Theorem 11.79(d) and the whole convex case; **two major findings**, both applied here:
the global half of Proposition 11.81(b) was false as a general statement (true where it
had been computed), and the interval of Proposition 11.82(e) had an upper end that is not
proved; fifteen minor findings (two numbers wrong in the third digit, several unstated
routine steps, one loosely worded argument), all applied.  What the referee did not
check is listed in §10 of the report (the Lean files were read, not compiled; sets
without symmetry beyond `Q_4`; parts of the two-phase tables).  Before that, the coordinator had re-derived line by line the
proofs of Theorem 11.76, Lemma 11.77, Theorem 11.78(a), Theorem 11.79, Theorem 11.80(a) and
Proposition 11.81(a), read but not re-derived in full Theorems 11.78(b) and 11.80(b), (c),
and **re-computed every headline number with independent solvers**
(`experiments/coordinator_checks/meanfield_T/`: two inner solvers that share no approximation
— clippings with the minorant `v`, and a generic convex programme per exit type with `I` —
the binary optima, the free-block profiles at four accuracies, the junction with the
uniform cube at six couplings, the pair identity, cones against shell-cones, a one-phase
case with a field, ferromagnets against the uniform cube on 180 random profiles, the
threshold `u_top`, the failure of the pair identity at `u = 0.30`, the onset of the free
block in the coupling; all agreed with the workstream's numbers to the digits printed — the
coordinator's runs did not include the two numbers that the referee corrected in the
third digit (`e₀`, `a_cone`) and covered the junction at `u = 1` only, which is why they
did not find what the referee found; one error of the coordinator's
own first solver, of exactly the kind the workstream reports about its own, was found on
the way and is recorded in `DEAD_ENDS.md` D49; the lessons of the review are D53).  Machine-checked: Theorem 11.76(a) (the
truncation and the lower bound) and (b) (`TypeQuantiles.lean`, `SymmetricSampling.lean`), and
the same statements for an arbitrary symmetry group (`GroupSampling.lean`).
Everything about limits is a paper proof by the method of types with `e^{o(n)}` factors.

**Setting.**  `Q_n = {0,1}ⁿ` with the Hamming distance, `L_u` the `u`-Lipschitz functions,
`A(ψ) = E_π e^{−ψ}`, accuracy `ε = ε₁n`, cost = number of evaluations of `ψ`, as in §11.20.
`π` is *exchangeable*: `π(x) = p_{|x|}/C(n,|x|)` with `p_t = π(T_t) > 0`, `T_t = {|x| = t}`,
`J_t := −ln p_t`; `dens_t(D) := |D ∩ T_t|/|T_t|`, `maxdens(D) := max_t dens_t(D)`.  For
`f = nφ(|x|/n)` with `φ` Lipschitz, `J_t/n = I(t/n) + O(ln n/n)` with the rate function
`I := φ − h − min(φ − h)` (`h` the binary entropy; for a merely continuous `φ` the error is
`3 ln(n+1)/n + ω_φ(1/n)` with the modulus of continuity `ω_φ`, still `o(1)`, which is all
that the limit statements need); `v` is the largest `u`-Lipschitz minorant
of `I`, `V_n` that of `J` on the lattice (`|V_n(t) − n·v(t/n)| = O(ln n)` uniformly: the
every-`n` statements use the lattice instance `−V_n(|x|)`, the limit statements `−n·v(|x|/n)`,
and the two differ by a polynomial factor in every quantity below); the *contact set* is `{v = I}`.  Curie–Weiss:
`φ(κ) = −(βJ/2)(2κ−1)² − βB(2κ−1)`; `βJ = 0` is the field of §11.20.

*Symmetric instances and their landscapes.*  `ψ_g(x) = g(|x|)` with `|g(t+1) − g(t)| ≤ u`.  Its
**landscape** `Λ_g(t) := −g(t) + min_{t′}[J_{t′} + g(t′)]` is `u`-Lipschitz and `≤ J` with
equality somewhere, hence `Λ_g ≤ V_n`, with equality for the **flat-histogram instance**
`ψ_H := −V_n(|x|)`, whose Gibbs law is uniform on type classes and gives equal weight to all
contact types.  With `Z_g := Σ_t e^{−(J_t − Λ_g(t))} ∈ [1, n+1]`, the deepest dip
`ψ_g^D := max_{y∉D}[ψ_g(y) − u·d(·,y)]` on a set `D` satisfies `A(ψ_g^D)/A(ψ_g) = 1 + Φ_g(D)` with

    Φ_g⁺(D) := Φ_g(D) + μ_g(D) = Z_g^{−1} · Σ_{x∈D} π(x) · exp( min_{y∉D} [ u·d(x,y) + Λ_g(|y|) ] ).      (11.23.1)

*Block profiles.*  Partition the coordinates into `k` blocks of fractions `λ_j`; a point
has the block profile `μ = (μ_j)`, `μ_j` = fraction of ones in block `j`; `μ̄ = Σλ_jμ_j` is its
type.  `MI(μ) := h(μ̄) − Σ_jλ_jh(μ_j)` (the density exponent of the class of `μ` inside its type
class — the mutual information between block label and letter), `dist(ν, μ) := Σ_jλ_j|ν_j − μ_j|`
(Hamming distance between classes, per coordinate), `α(μ) := MI(μ) + I(μ̄)` (the `π`-exponent
of the class).  Two blocks are the ones and the zeros of a *centre* `s` of type `m` (the
profiles `z = (a, b)` of §11.20).  For a limiting landscape `λ` (`u`-Lipschitz, `λ ≤ I`,
touching; `λ = v` for `H`, `λ ≡ 0` for the zero residual, `λ_γ(κ) = −γκ − I*(−γ)` for the
additive instance `γ|x|`):

    V(μ, B; λ) := min{ MI(ν) : u·dist(ν, μ) + λ(ν̄) ≤ B },      r_μ(e) := V(μ, e + α(μ); λ),
    R_λ(e) := sup_μ r_μ(e)   (all finite block structures),      R_H := R_v,      R^{(2)} := the same over two blocks,
    n_μ(X) := min{ MI(ν) : MI(ν) + u·dist(ν, μ) + v(ν̄) − α(μ) ≤ X },      N(X) := sup_μ n_μ(X),
    G_μ(ν) := MI(ν) + I(ν̄) + u·dist(ν, μ),    𝒱(μ) := min_ν G_μ(ν),    θ_shell(X; μ₀) := min{ MI(ν) : G_{μ₀}(ν) − 𝒱(μ₀) ≤ X }.

`G_μ − 𝒱(μ)` is the rate function of the Gibbs law of the **shell-cone** `u·d(·, C_μ)` (`C_μ` the
class of `μ`); the centre itself, `μ₀ = (1, 0)`, gives the cone of §11.20.  A profile is
*self-consistent* if it is its own Gibbs shell, `𝒱(μ) = α(μ)`.

**Theorem 11.76 (what permutation symmetry alone gives; every `n`, every exchangeable `π`)
[(a): the truncation and the lower bound **[V]**, the upper bound **[P]**; (b) **[V]**; (c), (d) **[P]**;
workstream T, Theorems T1, T2, T4, Proposition T10].**
(a) *Non-adaptive algorithms.*  Let `ψ^{tr,q}` be `ψ` truncated at its type-wise `q`-quantiles
(Theorem 11.61) and `ε_n^{tr}(q) := sup_{ψ∈L_u} ln[A(ψ)/A(ψ^{tr,q})]` (nondecreasing in `q`: a larger
`q` lowers the thresholds and removes more weight).  If `ε < ε_n^{tr}(q)`, every
randomised non-adaptive `(ε/2, δ)`-correct algorithm makes at least `(1 − 2δ)/q`
evaluations; and the type-stratified sample — `⌈8 ln(2(n+1)/δ)/q⌉` uniform points from each
type class, `Â = Σ_t p_t·(`sample mean of `e^{−ψ}` over `T_t)` — is `(ε/2, δ)`-correct for every
`ε ≥ ε_n^{tr}(q) + ln(4/δ)`.  So **the type-stratified sample is optimal among non-adaptive
algorithms up to the factor `8(n+1)ln(2(n+1)/δ)/(1 − 2δ)` in the cost and `ln(4/δ)` in the
accuracy, with the extremal function `ε_n^{tr}`; no isoperimetry is used.**
(b) *All algorithms at a symmetric instance.*  If `ε < ln(1 + Φ_g(D))` for some `D ⊊ Q_n`, every
`(ε/2, δ)`-correct algorithm — adaptive or not, with any hint — makes at least
`(1 − 2δ)/maxdens(D)` evaluations in expectation at `ψ_g`.
(c) *The flat-histogram instance is the hardest symmetric instance.*  For every symmetric
instance and every `D`: `Z_g·Φ_g⁺(D) ≤ Z_H·Φ_H⁺(D)`, hence `Φ_g⁺(D) ≤ (n+1)·Φ_H⁺(D)` and
`ln(1 + Φ_g(D)) > ε ⟹ ln(1 + Φ_H(D)) > ε − ln(n+2)`: every lower bound that (b) gives at a
symmetric instance holds at `H` at the accuracy `ε − ln(n+2)`.  The factor cannot be
dropped (`Z_H/Z_g` is attained).
(d) *Instance-optimality at symmetric instances without a hint.*  The type-stratified
two-sample bracket of Proposition 11.65(c), with doubling and adaptive stopping, is valid on
`L_u` and its cost at every symmetric instance is within `16(n+1)K/(1 − 2δ)` of the least
cost of any correct algorithm at that instance at accuracy `ε − ln 3`.

*Proof.*  (a) is Theorem 11.61(a), (b) read for an exchangeable `π` (remark (5) of §11.20):
the coupling of adjacent type classes by one flip does not involve `π`, and `π` enters only
through `A(ψ∘σ) = A(ψ)`; for the upper bound, `E Â = A`, Markov's inequality from above, and
from below `dens_t{w ≥ t_t} ≥ q` gives each class mean `≥ ½E_{T_t}min(w, t_t)` outside
probability `e^{−K/8}` (multiplicative Chernoff), so `Â ≥ ½A(ψ^{tr,q})`.  (b) is Theorem 11.22(c)
for the alternatives `ψ_g^{σD}`, `σ` a uniform permutation: a point lies in `σD` with
probability `dens_{|x|}(D)` (machine-checked as `symmetric_queries_ge`).  (c) By (11.23.1),
`Λ_g ≤ V_n`, `Z_g ≥ 1`, `Z_H ≤ n+1`; then `1 + Φ_g ≤ 1 + (n+1)(Φ_H + μ_H(D)) ≤ (n+2)(1 + Φ_H)`.
(d) The proof of Proposition 11.65(c) uses `A = Σ_tp_tE_{T_t}w` and (b) only.  ∎

*Remark (an arbitrary symmetry group)* **[the truncation, the lower bound of (a) and (b):
[V], `GroupSampling.lean`; the rest [P]; coordinator].**  Nothing in Theorem 11.76 is
specific to permutations of the coordinates of a cube.  Let `X` be a finite configuration
space with an envelope `d` (not necessarily symmetric) and `Γ` a finite group acting on `X`
with `d(σx, σy) = d(x, y)` and `π(σx) = π(x)`; let `N_orb` be the number of orbits, and read
"density in a type class" as density in an orbit, `dens_x(S) = |S ∩ Γx|/|Γx|` — the
probability that a uniformly random group element sends `x` into `S` (`gdens_mul_card_orbit`).
(a′) *Normalised matching from invariance alone:* for an admissible residual `ψ` and any
two points `a`, `b`, the orbit density of `{ψ < c − d(a,b)}` at `b` is at most that of `{ψ < c}`
at `a` (`lowDens_shift`: if `ψ(σb)` is that low, admissibility between `σa` and `σb` forces
`ψ(σa) < c`; on the cube this is the local LYM inequality, and no coupling of adjacent
orbits has to be constructed).  Hence levels with orbit density at most `q` can be
regularised to an invariant, admissible level function with the same property
(`regLevel_admissible`, `regLevel_lowDens_le`, `regLevel_smul`), the residual truncated at
them is admissible and differs from `ψ` on orbit density at most `q` (`truncate_admissible`,
`truncate_gdens_le`), every non-adaptive algorithm needs `(1 − 2δ)/q` evaluations at the
accuracy of the truncation (`group_nonadaptive_queries_ge`), and the *orbit-stratified*
sample is optimal among non-adaptive algorithms up to the factor
`8N_orb ln(2N_orb/δ)/(1 − 2δ)` (**[P]**, Chernoff and Markov as above).
(b′) Every algorithm needs `(1 − 2δ)/max_x dens_x(D)` evaluations at an invariant instance
(`group_queries_ge`).
(c′) On the orbit space with `J_O = −ln π(O)` and the quotient envelope
`δ(O, O′) = min{d(x, y) : x ∈ O, y ∈ O′}` (it satisfies the triangle inequality because `Γ` acts by
isometries), the instance `−V`, `V(O) := min_{O′}[J_{O′} + δ(O′, O)]`, is the hardest invariant
instance up to the factor `N_orb` (**[P]**, the same three lines).
*Conventions for a non-symmetric envelope* (referee R10, D13; on the cube they are
invisible): the triangle inequality of `d` is a hypothesis throughout (it is one of
`regLevel_admissible`); admissible means `ψ(x) − ψ(y) ≤ d(x, y)`; the deepest dip on `D` is
`max_{y∉D}[ψ(y) − d(y, x)]`, in this order of the arguments, so the exponent in (11.23.1) reads
`min_{y∉D}[d(y, x) + Λ_g(Γy)]`; and a landscape satisfies `Λ(O) − Λ(O′) ≤ δ(O′, O)` — it is the
*negative* of an admissible function, so `V` above is the largest minorant of `J` whose
negative is an admissible residual, not the largest admissible minorant.  A shorter
route to the truncation than the regularisation of arbitrary invariant levels: the
orbit-wise quantile `t(x) := max{c : dens_x{ψ < c} ≤ q}` is invariant and, by (a′) with
`c = t(a)`, satisfies `t(a) − t(b) ≤ d(a, b)`.
Examples: the symmetric group on the cube (types: this section); the uniform cube with
all its isometries (one orbit: a uniform sample is optimal among fixed samples up to the
constant `8 ln(2/δ)/(1 − 2δ)` for every `n`, and constants are the hardest invariant
instances — the every-`n` form of §11.16, in which Harper's theorem is needed only to
*evaluate* `ε_n^{tr}`); larger alphabets, sites of several types, two sublattices, mean-field
Potts models with their colour symmetry.  The statement is empty when the number of
orbits is exponential — lattice models with translations only, Markov chains along the
sequence: there symmetry alone says nothing.

**Lemma 11.77 (the inner problem) [P; workstream T, Lemmas T6, T7].**
(a) *Clipping.*  For fixed exit type and distance the minimum of `MI(ν)` is attained at a
clipping `ν_j = min(max(μ_j, c_lo), c_hi)`; hence `V(μ, B; λ)` is a two-parameter problem for
every number of blocks, and for a `u`-Lipschitz landscape the constraint is monotone in
each threshold, so the minimum lies on the boundary curve of the feasible set.
(b) *`v` or `I`.*  `min{MI(ν) : u·dist(ν, μ) + v(ν̄) ≤ B} = min{MI(ν) : u·dist(ν, μ) + I(ν̄) ≤ B}`, with
a minimiser whose type is a contact type; the same in `n_μ` and `𝒱`.
*Proof.*  (a) For a fixed type, minimising `MI` is maximising the strictly concave
`Σλ_jh(ν_j)` over a polytope; the Karush–Kuhn–Tucker conditions with multipliers `η` (type)
and `τ ≥ 0` (distance) read `h′(ν_j) = η ± τ` on the blocks that are raised or lowered, and
`h′` is strictly decreasing.  (b) "`≤`" since `v ≤ I`.  If `ν` is feasible on the left and
`v(ν̄) = I(κ*) + u|ν̄ − κ*|`, thin `ν` to the type `κ*` (`ν″_j = ν_jκ*/ν̄` if `κ* < ν̄`, the mirror image
otherwise): `dist(ν″, ν) = |ν̄ − κ*|`, and `MI(ν″) ≤ MI(ν)` by data processing (the letter is
passed through a channel that does not look at the block).  No convexity is used.  ∎

**Theorem 11.78 (the single-letter theorem for every rate function) [P; workstream T,
Theorem T3; (a) for every `n`; (b) by the method of types — the proof of Theorem 11.63
with Lemma T applied inside one type class; refereed by R10, which went through the six
steps against the proofs of Theorems 11.44 and 11.63 and found only cosmetic repairs].**  Let `λ` be a landscape and
`ψ_n = −nλ(|x|/n)` its instance.
(a) *Lower bound, every `n`.*  Let `μ` be a block profile with `k` blocks on the lattice, `C` its
class, `B > λ(μ̄) + ln 2/n`, and `D` the union of the classes `c′` with
`u·ℓ¹(c′, C)/n + λ(`type`(c′)/n) < B`.  Then

    ln(1 + Φ(D)) ≥ n(B − α_n(μ)) − ln 2 − ln Z,        maxdens(D) ≤ (n+1)^k · exp(−n·V(μ, B; λ))

(`α_n(μ) := −n⁻¹ln π(C)`, `Z ≤ (n+1)^{1+c_φ}` for Lipschitz `φ`), so by Theorem 11.76(b) every algorithm makes at
least `(1 − 2δ)(n+1)^{−k}e^{n·V(μ,B;λ)}` evaluations at `ψ_n` whenever `ε < n(B − α_n(μ)) − ln 2 − ln Z`
(and `D ≠ Q_n`, which holds as soon as the bound on `maxdens` is below one):
the exponent of the instance is at least `R_λ(ε₁⁺)` (lattice approximations of the block
fractions and of `μ` are routine).
(b) *Isoperimetry for the type-uniform measure.*  There is `ω_n → 0`, depending on `(φ, u)`
only, such that for all `n`, all `e` and all `D ⊊ Q_n`

    Φ⁺(D) ≥ e^{ne}      ⟹      maxdens(D) ≥ exp( −n[ R̄_λ(e − ω_n) + ω_n ] ),        R̄_λ(e) := max(R_λ(e), −e).

Consequently the hedged spot-check of Theorem 11.22(e), with samples from
`½μ_n + ½·(`uniform over types, uniform inside each type class`)`, costs `e^{nR_λ(ε₁)+o(n)}` at `ψ_n`
(at continuity points of `R_λ`; for `H` every `ε₁ > 0` is one, by Theorem 11.79(d)): **the hinted exponent of every symmetric instance of every
function-of-type known part is `R_λ(ε₁)`; by Theorem 11.76(c), (d) the largest of them is
`R_H(ε₁)`, it is attained at the flat-histogram instance, and at symmetric instances it is
attained without a hint.**

*Proof.*  (a) For `x ∈ C`, `y ∉ D`: `u·d(x,y)/n + λ(κ_y) ≥ B`, because the `ℓ¹` distance of block
counts bounds the Hamming distance from below; by (11.23.1) `Φ⁺(D) ≥ π(C)e^{nB}/Z`, and the
points of `C` have slack above `ln 2`, so `Φ(D) ≥ ½π(C)e^{nB}/Z`.  Every class of `D` satisfies
the constraint of `V`, has density at most `(n+1)e^{−n·MI}` in its type class, and there are at
most `(n+1)^{k−1}` classes per type.
(b) The six steps of the proof of Theorem 11.63, with two changes.  *Step 1:* split `D` by
the value of the exit budget `B(x) = min_{y∉D}[λ(κ_y) + u·d(x,y)/n]` **and by the type of `x`**
(polynomially many pieces) and keep the piece `C ⊂ T_k` with the largest `π(C)e^{nB}`.
*Step 2:* apply the lemma on inherently typical subsets (Lemma T of workstream A, a
statement about an arbitrary product measure and an arbitrary set) to `C` with the product
measure `Bernoulli(k/n)^{⊗n}`, **which is uniform on `T_k`, as `π` is**; it yields labels and a
joint type `P_{UX}` with `P_X = Bernoulli(k/n)` exactly, so the exponent of the piece is
`I(X;U) + I(P_X) = α(μ)` for the block profile `μ_u = P(X = 1 | U = u)`.  *Steps 3–5* (shallow
pieces give the term `−e`; a kernel that realises the minimiser of `V`; the chain rule) are
unchanged, and **the definition of `R_λ` as a supremum over all `P_{UX}` replaces the evaluation
lemma of §11.20** — whether the supremum can be evaluated is a separate question (Theorem
11.80, Proposition 11.82).  *Step 6* is simpler than for a product measure: every product
measure `Qⁿ` satisfies `Qⁿ(y) ≤ e^{−nh(|y|/n)} ≤ 1/|T_{|y|}|`, so `Qⁿ(D) ≤ (n+1)·maxdens(D)` — the
type-uniform measure dominates every product measure up to `n+1`; no typical set, no
window and no continuity of `I − v` are needed.  *Bookkeeping* (referee R10, m3; the
workstream's last line said "`R_λ` is nonincreasing", which is not automatic at negative
accuracies, where the set of admissible profiles grows with `e`): what is used is that
`R̄_λ` is nonincreasing and that `r_μ(x) ≤ R̄_λ(e′)` whenever `μ` is admissible at some `x ≥ e′` —
if `μ` is admissible at `e′` this is monotonicity of `r_μ`, and if not, `MI(μ) < −e′` and
`r_μ(x) ≤ MI(μ)` (the exit `ν = μ`).  The factor `1/(1 − θ_n)` of the typical-subset lemma
multiplies a mutual information `≤ ln 2`, so the error is `O(θ_n)` for all real `e`; for the
finitely many `n` with `θ_n ≥ 1` the trivial `ω_n = ½(sup I + u) + c·ln(n+1)/n` serves.  ∎

**Theorem 11.79 (non-adaptive algorithms: cones around shells) [P; workstream T, Theorems
T5, T8, Lemma T8′].**
(a) *Truncated shell-cones, every `n`.*  For a block profile `μ` with `k` blocks, `ψ = u·d(·, C_μ)`
and `q = e^{−nθ}`:
`ln[A(ψ)/A(ψ^{tr,q})] ≥ n[min{G_μ(ν) : MI(ν) ≤ θ + (k+1)ln(n+1)/n} − 𝒱(μ)] − c_k ln(n+1) − c′_φ`; by Theorem
11.76(a) non-adaptive algorithms have an exponent at least `θ_shell(ε₁⁺; μ)` for every `μ`.
(b) *Shell-cones against dips.*  For every block structure
`sup_{μ₀} θ_shell(X; μ₀) = sup_μ n_μ(X)`, and the left supremum may be restricted to
self-consistent shells: for the Gibbs shell `μ*` of `μ₀` (a minimiser of `G_{μ₀}`),
`θ_shell(X; μ₀) ≤ n_{μ*}(X) = θ_shell(X; μ*)`, and `μ*` is self-consistent.  Moreover
`n_μ(X) = min{r_μ(e) : e + r_μ(e) ≤ X}` over the accuracies `e` at which `μ` is admissible
(`e + α(μ) ≥ v(μ̄)`; at the others `n_μ(X) ≤ MI(μ) < −e`), hence
`N(X) ≤ min{R̄_H(e) : e + R̄_H(e) ≤ X}`.
(c) *Upper bound.*  `n⁻¹ε_n^{tr}(e^{−nθ}) ≤ θ + R̄_H^{−1}(θ) + o(1)` (with the left limit `R̄_H^{−1}(θ⁻)` at a
jump, i.e. at a flat piece of `R̄_H`): the shear law of §11.21 as an
upper bound.  So the exponent of non-adaptive algorithms satisfies
`N(ε₁⁺) ≤ θ_na(ε₁) ≤ inf{θ : θ + R̄_H^{−1}(θ) < ε₁}`.  **The upper bound needs the value of the full
supremum `R_H`**: a lower bound of `R_H` — the best binary centre, say — bounds `θ_na` from
above only where it is known to equal `R_H` (this is what went wrong in the first version
of Proposition 11.82(e)).
(d) *Regularity, for every rate function.*  For all `e′ < e`: `R̄_H(e) ≥ R_H(e′) − (e − e′)`.  Hence
`R̄_H` is nonincreasing and 1-Lipschitz and the shear `S̄(e) := e + R̄_H(e)` is nondecreasing —
the slope condition of a `HintPair` needs no convexity.  Consequently
**`θ_na = R_H∘S^{−1}`, the pair identity `θ_na(e + R_H(e)) = R_H(e)`, holds wherever the shear is
strictly increasing and equality holds in the last inequality of (b)** (the *witness
condition*: profiles `μ` with `r_μ(e) → R_H(e)` whose own shear `e′ + r_μ(e′)` exceeds `S(e)` for
all `e′ > e`).  Neither is automatic without convexity: Proposition 11.82(e).
*Proof.*  (a) `e^{−ψ}` is constant on profile classes; in every type class one class above
the quantile has density `≥ q/(n+1)^{k−1}`, and the classes of density below
`q/(n+1)^k` contribute at most `q·t_t` each; no unimodality is needed.  (b) is the triangle
inequality: `G_{μ₀}(ν) − G_{μ₀}(μ*) ≤ G_{μ*}(ν) − α(μ*)` for all `ν`, and
`𝒱(μ) ≤ G_μ(μ) = α(μ)`; with Lemma 11.77(b).  (c) The proof of Theorem 11.61(d):
`A(ψ) − A(ψ^{tr}) ≤ T·Z_H·Φ_H⁺(D)` for `D = {w > t_{|x|}}`, `A(ψ^{tr}) ≥ qT`, `T = max_tp_tt_t`, and
Theorem 11.78(b).  (d) Let `D` be `e′`-sensitive with `maxdens(D) = q` and take the union `D′` of
`N = ⌈e^{n(e−e′)}⌉` independently and uniformly permuted copies of `D` (`Nq ≤ 1`).  A point lies in
`k` copies with probability at most `1/k!`, so with positive probability no point lies in
more than `n` copies; then `Φ_H⁺(D′) ≥ n⁻¹Σ_iΦ_H⁺(σ_iD) = (N/n)Φ_H⁺(D) ≥ e^{ne}/n` (the slack out of `D′` is
at least the slack out of each copy, and `H` is symmetric), while `maxdens(D′) ≤ Nq`; now
Theorem 11.78(a) for the existence of `D` and (b) for `D′`.  (Theorem 11.78(a) yields sets
for `r_μ(e′ + η)`, every `η > 0`, so the inequality comes out first for the left limit
`R̄_H(e⁻)`; a nonincreasing function that satisfies it for left limits has no jumps.
`Nq ≤ 1` may be assumed, since otherwise the right-hand side is negative.)  ∎
*Reading.*  Unions of permuted copies of a sensitive set are what profiles with fewer
constraints are — a cylinder over a free block is the union of the shells whose centres
differ on that block.  This is why the supremum over **all** block structures, and not
the one over binary centres, is the right exponent function: for a single profile
`e ↦ r_μ(e)` can fall faster than with slope `−1`; `R_H` cannot.
A truncated cone around a point is as good as the dip whose Gibbs shell it
has.  When the cone's Gibbs measure sits in a well while the hard dips sit on the barrier,
the cone is the wrong function; the right one is a cone around a self-consistent shell.
Self-consistency has the local form `|φ′(μ̄) + logit μ_j| ≤ u` for every block — the cone law in
the mean-field effective field of the shell's own type.

**Theorem 11.80 (a convex rate function: §11.20 without the nested algorithm) [P; workstream
T, Theorem T9; refereed by R10: (a), (b), (c) proved — (c) after a repair of one argument
and with a strengthening, both below; (d): "`≤`" proved, "`=`" numerical: to `10⁻¹¹` in ten
cases of the workstream and to `5·10⁻⁹` in fourteen of the referee's, twelve of them not of
Curie–Weiss type].**  Let `I` be convex (Curie–Weiss with `βJ ≤ 1` and any
field; every antiferromagnet).
(a) `V(μ, B; v) = sup_{|γ|≤u} V(μ, B; λ_γ)`; hence `R_H = sup_{|γ|≤u} R_γ`: **the flat-histogram
instance is exactly as hard as the hardest additive instance** (`v = max_γλ_γ`, and Sion's
theorem twice; the minimising side is compact, so no Slater condition is needed, and
`γ ↦ V(μ, B; λ_γ)` is only lower semicontinuous a priori — hence "sup").
(b) **Binary centres suffice**, `R_γ = R_γ^{(2)}` and `R_H = R_H^{(2)}`: for fixed `γ` and Lagrange
parameter the value depends on the law of the block types linearly, and the function to
be maximised is strictly concave on two outer pieces and strictly convex between them,
so a supporting line of its concave envelope touches it in at most two points.
(c) **There is a game function:** `F*(t) := sup_{|γ|≤u} sup_μ min_ν[MI(ν) + t(u·dist(ν,μ) + λ_γ(ν̄) − α(μ))]`
satisfies the hypotheses of `GameFunction`, `R̄_H(e) = R̂(e) := max_t[F*(t) − te]` **for every real
`e`** (so `R_H = R̂` for `e ≥ 0`) and
`N(x) = max_{τ<1}(F*(τ) − τx)/(1 − τ)`; so Theorem 11.66 **[V]** applies: `R̄_H` is convex with
slopes in `[−1, 0]`, the pair identity `N(e + R̄_H(e)) = R̄_H(e)` holds, and with Theorems 11.78,
11.79 **the exponent of non-adaptive algorithms is `θ_na = R̄_H∘S̄^{−1}`, attained by the
type-stratified sample, and the hinted exponent of `H` and of the hardest additive
instance is `R_H`.**
*Three points of the proof* (referee R10).  (1) The workstream proved `R_H = R̂` for `e ≥ 0`
and `R̄_H ≤ R̂` in general (for `τ ≥ 1` and an admissible profile the bracket is at most
`−e = F*(1) − e`).  The equality for all `e`, which the formula for `θ_na` below `R_H(0)`
needs: for `e₀` above the accuracy `e_c` at which `R̂` reaches the line `−e`, put `X = Ŝ(e₀)`;
then `N(X) = R̂(e₀)` by the formula for `N`, and `N(X) ≤ R̄_H(e)` for every `e` with
`e + R̄_H(e) ≤ X` (Theorem 11.79(b)), which `e = e₀` satisfies because `R̄_H ≤ R̂`; so
`R̂(e₀) ≤ R̄_H(e₀) ≤ R̂(e₀)`; for `e ≤ e_c` both sides are `−e`.  (2) `E > 0` (a field of
`GameFunction`): for `μ = (κ₀ + η, κ₀ − η)` with equal weights around a minimiser `κ₀` of `I` and
`γ = 0`, `MI(ν) ≥ ½(ν₁ − ν₂)²` and `dist(ν, μ) ≥ η − ½|ν₁ − ν₂|` give
`F*(t) ≥ t(uη − O(η²)) − (tu)²/8`, whence `E ≥ uη − O(η²) > 0` (the workstream's sentence
"every constant `ν` is at distance `≥ η`" was not an argument: the minimiser is not
constant).  (3) Statements about `θ_na` compare game functions, i.e. Lagrangians at all
slopes, not only the values `r_μ(e)` at `e ≥ 0`; the comparisons of Proposition 11.81(a) hold
for the Lagrangian by the same two arguments.
(d) The cone formulas of §11.20 hold with `Λ_m := min_z[MI + I(κ_z) + uρ]`:
`R_H(e) = max_m min{MI(z) : uρ(z) + v(κ_z) − Λ_m ≤ e}`, `θ_na(x) = max_m min{MI(z) : J_m(z) ≤ x}`
("`=`" is numerical; the referee indicates a proof for differentiable `φ`: at the saddle
of (b) the tangency conditions `logit M_hi = u − φ′(m̄)`, `logit M_lo = −u − φ′(m̄)` are the
stationarity conditions of the cone functional, and when the contacts are in the outer
pieces the exit is coordinatewise beyond the shell, so that the triangle inequality of
"`≤`" is an equality — not written out).
*What fails:* the closed form of the game function (the soft gap is not additive in the
sites), the clean every-`n` product bound `e^{−tε+nF}` (a polynomial factor is lost), and
**Theorem 11.64** — see "adaptive algorithms" below.
*Numbers* (`u = 1`; cone formulas, checked against the sup–min): with `B = 0` each of the
couplings computed, `βJ ∈ {−40, −8, −2, −1, 0, 0.5, 0.9, 1}`, has exactly the uniform cube's
values (`R_H(0⁺) = 0.029139`, `a = 0.110944`) —
**an interaction without a field and with one phase changes neither the hinted exponent
of `H` nor the exponent of non-adaptive algorithms** (proved: for `0 ≤ βJ ≤ 1` by
Proposition 11.81(a), and for every symmetric convex rate function, antiferromagnets
included, by Corollary 11.91(ii); the first version said "changes no exponent" — for
adaptive algorithms without a hint the equality is proved for `0 ≤ βJ ≤ 1` only, Proposition
11.81(c): Scientific Discovery Division, SCI-REV-0001, M1); with a field every exponent is below the uniform
cube's and `R_H > R_0` strictly; near the critical coupling the gap between the class and
the zero residual is large (`βJ = 1`, `βB = 0.1`: `R_H(0⁺) = 0.02796` against `R_0(0⁺) = 0.02027`), and
the hardest additive residual cancels the field exactly (`γ* = 2βB`).

**Proposition 11.81 (ferromagnets) [(a) P, given Proposition 11.65(b) and the evaluation
lemma of Theorem 11.63 (both refereed); (b): the local statement P, the global one
numerical **and true only in a range of slopes and accuracies** (referee R10, finding M1:
as first stated, for all `(e, u)`, it was false); (c) P, given Theorem 11.64: the
workstream's sketch with the referee's completion, checked by the coordinator, not
refereed in turn; workstream T, T9(e), §6.6, T12].**
(a) *Never harder than the uniform cube.*  If `φ` is concave (ferromagnetic interaction of
any strength, any field — also with two phases), then for all `e`

    R_H(e) ≤ R_unif(e) := KL((Λ₁ + e)/u ‖ ½),      Λ₁ = ln(2/(1 + e^{−u})),

and for `B = 0`, `0 ≤ βJ ≤ 1` there is equality.
(b) *The junction is beyond the critical coupling.*  Let `ρ := (Λ₁ + e)/u`,
`c₂ := 1/(2ρ(1−ρ)) − 2`, `L := ln((1−ρ)/ρ)` and `βJ*(e, u) := 1 + u·c₂/(2L)` (`= 1.1250` at `u = 1`,
`e = 0`).  For `B = 0`, at the uniform cube's optimal profile `μ* = (½; p_u, p_u)` the symmetric
exit is a strict local minimum iff `βJ < βJ*` **[P]**.  *Where it is also the global minimum*
**[N]**: at `u = 1` (`e = 0, 0.02, 0.04`: workstream and coordinator); on the referee's grid
(couplings `1 + f(βJ* − 1)`, `f ≤ 0.99`) for `u ≤ 2` at seven accuracies between `0.9e_c` and
`0.9E_unif`, at `e = 0` for `u ≤ 6`, and for every `u ≤ 8` when `e ≥ 0.3E_unif`
(`e_c = u·p_u − Λ₁ < 0` is the accuracy at which `R_unif` meets the line `−e`).  There
**`R_H(e) = R_unif(e)` for `1 < βJ ≤ βJ*` although there are two phases**, and `R_H < R_unif`
beyond (`0.0290694` at `βJ = 1.14`, `0.0251012` at `1.5`, `0.0230260` at `1.75`; `u = 1`, `e = 0`).
*Where it is not* (referee R10, M1): for large slopes at small or negative accuracies a
**far exit** undercuts the symmetric one below `βJ*`.  The constant profile at a well `κ_w`
(`MI = 0`) is feasible for `μ*` as soon as

    I(½) ≥ E_unif(u) − e + u·(p_u − κ_w)₊,        E_unif(u) = ln cosh(u/2)

(from `u·dist(κ_w𝟙, μ*) + I(κ_w) ≤ e + KL(p_u‖½) + I(½)` and `u(½ − p_u) − KL(p_u‖½) = ln cosh(u/2)`; the
cheapest constant exit sits at the edge of the well's contact interval and is slightly
cheaper still), i.e. as soon as the barrier is as high as what is left of the uniform
cube's threshold, and then `r_{μ*}(e) = 0`.  Example: `u = 8`, `e = 0`, `βJ = 8.2632 < βJ* = 8.3366`:
`I(½) = 3.438 > E_unif = 3.307`, the constant exit costs `4.000` against the budget `4.129`,
`r_{μ*}(0) = 0`, and the best profile found — the binary shell `(½; 0.0292, 0.0292)` at the edge
of the cliff where the constant exits stop being feasible; 16 multi-block starts give
nothing better — has `0.36742` against `R_unif(0) = 0.39854`; likewise `u = 4`,
`e = 0.6e_c = −0.3618`, `βJ = 4.9578 < βJ* = 4.9978`: `0.41763` against `0.41857` (23 starts); eight
further cells of the grid.  That the uniform cube's profile loses its value there is an
explicit feasible exit (re-computed by the coordinator; DEAD.25 of the harness); that
`R_H` itself is below `R_unif` rests on the comparison chain of (a) — a profile that
restored `R_unif` would have to be an optimal profile of the uniform cube of type `½` — and
on those searches, not on a proof.  On the grid the failure occurs exactly in the cells
where the displayed inequality holds at `βJ*`, so **the junction is at `min{βJ*(e, u), βJ_w(e, u)}`**,
`βJ_w` the coupling at which a constant exit becomes feasible for `μ*` **[N]**; for `u = 1` the
second number is far away (`I(½) = 0.010` at `βJ*` against `0.120`), and in every cell
computed the junction is beyond the critical coupling.
(c) *Adaptive algorithms: never more than the uniform cube.*  For a ferromagnetic
Curie–Weiss known part (`βJ ≥ 0`, any field) there is an adaptive algorithm without a hint
whose cost exponent is at most `R_unif(ε₁)`.  Hence **the adaptive exponent without a hint
lies in `[R_H(ε₁), R_unif(ε₁)]`, and it equals `R_unif(ε₁)` — the first interacting known parts for
which it is determined — wherever `R_H = R_unif`: for `B = 0` and `0 ≤ βJ ≤ 1` (proved), and with
two phases up to the junction of (b) (numerical).**
*Proof of (c).*  By the Hubbard–Stratonovich transformation a ferromagnetic Curie–Weiss
measure is a mixture of fields, `π = ∫ν(dy)·Bernoulli(p_y)^{⊗n}` with
`p_y = e^{y+βB}/(2cosh(y+βB))` and `ν(dy) ∝ exp(−n[y²/(2βJ) − ln 2cosh(y+βB)])dy`, so
`A(ψ) = ∫ν(dy)A_y(ψ)` for the same residual (checked numerically to `6·10⁻¹⁵` by the referee).
Since `A_y/A_{y′} ≤ e^{un}` and `ν(|y| > Y) ≤ e^{−n(u+1)}` for a fixed `Y`, the fields `|y| ≤ Y` suffice, and
since `|∂_y ln A_y| ≤ 2n`, a grid of mesh `n⁻²` reproduces the integral up to `1 + O(1/n)`.  The
workstream ran the algorithm of Theorem 11.64 at every grid field and lacked the
uniformity in `p` of its `o(n)`.  The referee's completion avoids it: take a *finite* net
`y_j` of `[−Y, Y]` with cells of radius `Δ`, independent of `n`; for `y` in the cell of `y_j`,

    A_y(ψ) = C_n(y, y_j) · A_{y_j}( ψ − 2(y − y_j)|x| ),      C_n = e^{−(y−y_j)n}·(cosh(y_j+βB)/cosh(y+βB))ⁿ,

the tilted residual belongs to `L_{u+2Δ}`, and an evaluation of it is an evaluation of `ψ`.
So the algorithm of Theorem 11.64 for the field `p_{y_j}` and the class `L_{u+2Δ}`, at the
accuracy `ε − 1` and the confidence `δ` divided by the number of grid fields, serves every
grid field of the cell; only finitely many pairs `(p_{y_j}, u + 2Δ)` occur, so the `o(n)` is
uniform, and the brackets combine with the weights of `ν`.  The exponent is at most
`max_jR^max_{p_{y_j}, u+2Δ}(ε₁) ≤ R^max_{½, u+2Δ}(ε₁)` (Proposition 11.65(b)), which tends to `R_unif(ε₁)` as
`Δ → 0`.  ∎  (Not tight in general, and nothing for antiferromagnets: a negative coupling
is not a positive mixture of fields.)
*Proof of (a).*  A concave `φ` is the lower envelope of its tangents, and
`θκ − h(κ) = KL(κ‖p_θ) − ln(1 + e^{−θ})` with `logit p_θ = −θ`; so `I = min_θ[KL(·‖p_θ) + c(θ)]` with
equality at a supergradient `θ ∈ ∂φ(κ)`, and for every pair of profiles
`I(ν̄) − I(μ̄) ≤ KL(ν̄‖p₀) − KL(μ̄‖p₀)`, `p₀` the effective field at the type of `μ`: the feasible
set of `r_μ(e)` contains that of the field `p₀` (Lemma 11.77(b)), so
`r_μ(e) ≤ R^max_{p₀}(e) ≤ R^max_{½}(e)` (if `μ` is not admissible for the field problem, then
`e + MI(μ) < 0` and `r_μ(e) ≤ MI(μ) < −e ≤ R^max(e)`; the same two steps applied to the Lagrangian
compare the game functions, which is what statements about `θ_na` need: Theorem 11.80,
point (3)).  Equality: for a symmetric convex `I` the feasible set of
the uniform cube's optimal profile is convex and invariant under the reflection that
exchanges the two blocks, `MI` is convex, so there is a minimiser of type `½`, where the
constraint is the uniform cube's.  ∎

**Proposition 11.82 (two phases: what the supremum looks like) [numbers **[N]**, every value
a proved lower bound for all algorithms at `H` by Theorem 11.78(a); re-computed by the
coordinator].**  Curie–Weiss, `βJ = 1.5`, `B = 0`, `u = 1` (wells at `κ = 0.0707`, `0.9293`, barrier
`I(½) = 0.1152`, contact set `[0.020, 0.980]`: the flat-histogram instance lifts the whole
barrier).

| accuracy rate `e` | cone formula | zero residual | best binary centre `R^{(2)}(e)` | shell `x` | best profile found | structure | uniform cube |
|---|---|---|---|---|---|---|---|
| `−0.05` | | | `0.0575961` | `0.2821` | `=` | binary | `0.0590497` |
| `0` | `0.0107007` | `0.0087471` | **`0.0251012`** | `0.29803` | `=` | binary (all searches) | `0.0291391` |
| `0.002` | | | `0.0240304` | | `0.0240419` | free block, `λ_f = 0.140` | `0.0281676` |
| `0.01` | `0.0061622` | `0.0047744` | `0.0199399` | `0.30170` | `0.0203817` | free block, `λ_f = 0.140` | `0.0244503` |
| `0.02` | `0.0028153` | `0.0020627` | `0.0152765` | `0.30553` | `0.0161548` | free block, `λ_f = 0.141`, `x = 0.2774` | `0.0201820` |
| `0.05` | `0` | `0` | `0.0046265` | `0.31795` | `0.0063875` | seven block types (referee R10; `0.0063867` with five) | `0.0098646` |

(a) *Cones fail.*  At `e = 0` the cone formula gives `0.01070`, the best dip around one centre
`0.025101`.  The optimal dips have their Gibbs shell **in the barrier type class**, at
distance `xn ≈ 0.30n` from a centre of type `½`, and two tied, asymmetric cheapest exits
(towards either well); a cone's own Gibbs shell sits in a well.
(b) *The pair identity holds with shells and fails with cones:*
`n_{μ*}(e + R^{(2)}(e)) = R^{(2)}(e)` to `10⁻⁸` for `−0.108 ≤ e ≤ 0.064`; the truncated cone around the
shell attains it, the truncated cone around a point gives `0.0020` at `S(0)`.  At vanishing
accuracy `a = θ_na(0⁺) = KL(p_u‖½) = 0.110944`, the uniform cube's value (shells `(½; x, x)` are
self-consistent exactly for `x ≥ p_u`; `≤` by Proposition 11.81(a)), against `0.04435` from cones
(the mutual information of the cone's Gibbs shell, largest at a centre of type `½`, where
the shells in the two wells tie; the first version had `0.0446`, the value of the
*metastable* shell at `m ≈ 0.5025` — referee R10, m12, re-computed by the coordinator).
(c) *Beyond `e₀ = 0.001804` one centre is not enough.*  Profiles with a **free block** — a
shell on about 86 % of the coordinates, the remaining coordinates unconstrained — have
larger values than every binary centre: `+0.05 %` at `e = 0.002`, `+5.7 %` at `0.02`, `+38 %` at
`0.05` (where the best profiles found have five to seven block types: the number of atoms
grows with the accuracy).  The binary branch and
the diluted branch are two local maxima that cross at `e₀`; the free block appears with a
finite weight.  *In the coupling*, at a fixed accuracy `e > 0`, there are three regimes:
an **invisible barrier** (`βJ ≤ βJ*(e, u)`: the uniform cube's exponents), **tilted dips
around one centre** (`βJ* < βJ ≤ βJ**`), and **diluted dips** (`βJ > βJ**`), with
`βJ** ≈ 1.124` at `e = 0.02` and `≈ 1.10` at `e = 0.04` (against `βJ* = 1.103`, `1.082`; `u = 1`); the
weight of the free block then grows continuously from zero (`0.034`, `0.072`, `0.141` at
`βJ = 1.2, 1.3, 1.5`, `e = 0.02`).  What the free block does: on the constrained coordinates
it multiplies the destabilising curvature `2(βJ − 1)` of the landscape by `1 − λ_f` and adds
`2λ_f` from the entropy of mixing — the symmetric exit of the diluted uniform-cube profile
is a strict local minimum iff `βJ < 1 + u(c₂ + 2λ_f)/(2L(1 − λ_f))` **[P, local]**.  At `e = 0` no free
block was found at any coupling tried (`1.15 ≤ βJ ≤ 2`).
(d) *The hardest additive instance is far below `H`:* it is the zero residual, with
`0.0087471`, 35 % of `R_H(0)`; the field-tilted Gibbs measures of a two-phase known part never
sit on the barrier, so the flat-histogram ensemble is **not** their
normalised-maximum-likelihood mixture here (the conjecture of §11.20, remark (3), is right
about the ensemble and wrong about its derivation beyond convex `I`).
(e) *Other parameters.*  A field that keeps two wells changes little (`βB = 0.05`:
`R^{(2)}(0) = 0.0250232`, asymmetric barrier shell; the free block appears there too: at
`e = 0.02` a three-block profile has `0.0160758` against `0.0152121` for the best binary centre,
and none was found at `e = 0` — referee R10).  If the barrier is steeper than `u` on its
flanks the contact set breaks into pieces, and as long as the top of the barrier is a
contact point — `u ≥ u_top = 0.2815`, the largest slope of a chord from the top — the optimal
dips are still barrier shells with `0.81`–`0.83` of the uniform cube's exponent; when the
top leaves the contact set (`u < u_top`) the barrier disappears from the problem, the
optimal dips sit in a well, the cone formula is right again and the exponent drops to
27 % of the uniform cube's.  **Close to the threshold the pair identity fails for cones
around profile classes:** at `u = 0.30`, where the piece of the contact set at the top is
narrow (`[0.4745, 0.5255]`), `R^{(2)}(0) = 0.0022646` on the shell `x = 0.4409`, which is only
marginally self-consistent — the Gibbs measure of the cone around it is on the verge of
escaping into a well, `n_μ(S(0)) = 0` for it — and the best cone found around a shell
(symmetric shells, general binary profiles, profiles with a free block) certifies
`0.00184 = 0.81·R^{(2)}(0)` at the accuracy `S^{(2)}(0) = 0.0022646` (re-computed by the coordinator:
`0.001839` at `x = 0.4514`; by the referee three ways: `0.00184002` at `x = 0.45138`).  **What is
proved there** (referee R10, M2; the first version of this item gave the interval
`[0.00184, 0.00226]`, whose upper end is `R^{(2)}(0)`, a *lower* bound of `R_H(0)`): the exponent of
non-adaptive algorithms at that accuracy lies in `[0.00184, 0.00338]`, the upper end from
`R̄_H ≤ R̂_unif` (Proposition 11.81(a), Theorem 11.79(c): `R_unif(S_unif^{−1}(0.0022646)) = 0.003377`).  The
interval `[0.00184, 0.00226]` holds *if* `R_H = R^{(2)}` on a left neighbourhood of `0` at this
slope — the analogue of (C1), supported by one three-block search of the workstream and
24 multi-block runs of the referee that return the binary shell.  So three things can
happen: functions other than cones around profile classes do better; the shear bound
of Theorem 11.79(c) is not attained when a second phase carries more weight than the
classes at the quantile; or `R_H(0) > R^{(2)}(0)` at this slope.
(f) *Exact sums.*  At `n = 4000` and bounded accuracy every algorithm needs
`(1 − 2δ)e^{0.02508n}` evaluations at `H` (the exact sum gives `0.025087`) and every non-adaptive algorithm `(1 − 2δ)e^{0.1017n}`
(cones around shells; cones around points certify `e^{0.0435n}`); at `ε = 0.05n + 1` and `n = 600`
the neighbourhood of a three-block class certifies `e^{0.00573n}` against `e^{0.00520n}` for the
best capped set around one centre.

**Conjecture 11.83 and open problems [C].**
(C1) For `e ≤ e₀` — in particular at vanishing accuracy — the supremum is attained at the
binary barrier shell: `R_H(0⁺) = 0.0251012` at `βJ = 1.5`, `u = 1`.  Proved: `0.0251012 ≤ R_H(0⁺) ≤ 0.0291391`.
*Not refuted by the referee:* 86 searches with methods independent of the workstream's
and the coordinator's (differential evolution over 3, 4 and 5 blocks; Nelder–Mead; a
sequential linear programme over the *law* of the block types, which moves finite mass
in one step) find nothing above `0.0251012`, and the binary optimum is a critical point of
the linearised problem over all laws (LP optimum `0.02510118` against `0.02510117`) — which
excludes improving directions to first order only, since the exit values are convex in
the law.
(O2) The value of `R_H(e)` for `e > e₀`: is the supremum attained by finitely many block
types?  (For a *fixed* exit type the inner value is convex in the law of the block types,
so two block types suffice against any one exit; the number of block types is driven by
the number of exit types that tie, and the minimum over exit types cannot be convexified
because `v` is not convex.  The referee's seven-atom profile at `e = 0.05` supports the doubt
that finitely many suffice.)
(O3) Without convexity `R̄_H` is 1-Lipschitz and the shear nondecreasing (Theorem 11.79(d));
open are the *strict* monotonicity of the shear and the witness condition, i.e. whether
`θ_na = R_H∘S^{−1}` for every rate function.  (O5) The exponent of non-adaptive algorithms
where the witness condition fails for cones around profile classes (`u = 0.30`: proved to
lie in `[0.00184, 0.00338]`; in `[0.00184, 0.00226]` if binary centres are optimal there;
Proposition 11.82(e)).
(O4) **The adaptive exponent without a hint**, for every interacting known part, convex or
not.  Conjecture: it is `R_H(ε₁)`; equivalently `H` is the hardest instance among *all*
instances.  Proved: the lower bound `R_H`; the non-adaptive upper bound; for ferromagnets
the truth lies in `[R_H, R_unif]` (Proposition 11.81(c), given Theorem 11.64), so the
conjecture holds wherever `R_H = R_unif`; for every function-of-type known part the problem
reduces to type classes (§11.25, Theorem 11.92, Conjecture 11.94).

*Adaptive algorithms: what fails in the nested algorithm, and a possible repair.*  The
one-level theorem behind Theorem 11.64 needs, for a split of the coordinates into an
outer and an inner block, that fibre averages `W(a) = E_{π(·|a)}e^{−ψ(a,·)}` are `u`-Lipschitz in the
outer point.  For an interacting `π` the conditional law of the inner block depends on the
type of the outer point, and already for a residual that does not depend on `a` the
function `−ln W` changes by `φ′(κ_ψ) − φ′(κ_π)` per outer flip (the total types selected by the
instance and by the known part on the fibre): it is Lipschitz only with the constant
`u + osc φ′`, and the excess depends on the instance (workstream T, §8.1).  For a field `φ′` is
constant — this is where the product structure was used.  *Coordinator's remark* **[C]**,
not proved (the workstream commissioned on it failed without output; the coordinator
took the question up in §11.25, which reduces it to type classes: Theorem 11.92,
Conjecture 11.94): for an
exchangeable `π`, **given the type of the inner block the two blocks are independent**
(the inner block is uniform on its slice), so
`A = Σ_{t_i} Σ_a ω_{t_i}(a)·W_{t_i}(a)` with `W_{t_i}(a)` the mean of `e^{−ψ(a,·)}` over the inner slice
`T_{t_i}` — exactly `u`-Lipschitz in `a` — and `ω_{t_i}` an exchangeable weight on the outer cube.
Resolving the inner block by its type therefore restores the property that fails,
within the class "exchangeable known part, Lipschitz residual", at the price of inner
problems on slices whose accuracy is needed only relative to the fibre total.  Whether
the resulting recursion has `R_H` as its limit is open.  The referee sees no obstruction
and names what would have to be supplied: (1) the inner problems live on slices (no
one-flip coupling inside a slice), so the family must be enlarged to products of slices
and the recursion is no longer scale-free — the pair `(θ_na, R_H)` becomes a family indexed
by the conditional rate functions, and the machine-checked convergence theorem does not
apply as it stands; (2) the accuracy must be allocated over the inner types (`t_i ↦ W_{t_i}(a)`
is itself log-`u`-Lipschitz, but the weights `ω_{t_i}` change with `t_i`); (3) the cost of an
outer point is a maximum over inner types and outer instances that need not be realised
by one residual, so the limit may exceed `R_H`.

*Interpretation.*  For a known part that is a function of an order parameter, with its
density of states known, the ensemble that is uniform inside every level set and flat
over the levels — the multicanonical ensemble of Berg and Neuhaus, the target
of Wang–Landau sampling — is (i) the sampling law of a non-adaptive certified estimator
that is optimal up to a polynomial factor for every `n` (what Theorem 11.76(a) proves is
this for the sample stratified over **all** `n + 1` level sets; that the levels outside
the window of contact types may be dropped at the exponential scale is not proved
here), and (ii) flat over the window of contact types, the Gibbs law of the
hardest symmetric instance; and (iii) at phase coexistence the perturbations that are
hardest to exclude live on shells of barrier configurations.  *What this does not say:*
the class is an idealised Hamming–Lipschitz class; the density of states of the known
part is assumed known and the type-uniform sample free — the practical difficulty of
flat-histogram methods, producing the flat ensemble by a Markov chain, is not touched,
and in that literature the flat histogram is known *not* to be optimal for the dynamics
(Trebst–Huse–Troyer); exponents only; "hardest instance" among symmetric instances only.

*Extensions (workstream T, §10; not written out).*  Theorem 11.76 holds for every symmetry
group with polynomially many orbits (the remark after it; machine-checked in its lower
half): two sublattices, mean-field Potts models.  Theorem 11.78 by the same proof (sketch); its
evaluation is not immediate (for `q ≥ 3` the inner problem is a transport problem, and a
first-order transition has a non-convex rate function).

*Harness.*  Block XIX of `experiments/falsify_conjectures.py`: XIX.1 (Theorem 11.76(c) and
formula (11.23.1) by brute force on `Q_4`–`Q_6` for random exchangeable measures, instances and
sets; the factor `Z_H/Z_g` exceeds one), XIX.2 (Lemma 11.77: clippings against full grids of
exit profiles with `v` and with `I`; thinning), XIX.3 (Proposition 11.82: the barrier shell,
local maximality, the pair identity through `r_μ`, shell-cone against point-cone, the cone
formula, the free block at `e = 0.02` and its absence at `e = 0`), XIX.4 (Proposition 11.81(b)
at `u = 1`, `e = 0`: `βJ*`, equality with the uniform cube below it and strict inequality above, the
second-order coefficient), XIX.5 (Theorem 11.78(a): class-level exact sums against brute
force on `Q_8`, `Q_10`, and the two bounds at `n = 60, 120`), XIX.6 (Theorem 11.79(b):
self-consistency of barrier shells exactly beyond `p_u`, and the two triangle-inequality
statements exactly on a grid); 21 mutations, all detected; and the documented refutations
DEAD.19 (binary centres do not suffice with two phases), DEAD.20 (cones around points
fall short of shells), DEAD.22 (near the threshold `u_top` cones around shells fall
short as well) and DEAD.25 (the junction is not at `βJ*` for every slope: at `u = 8`, `e = 0` a
constant exit undercuts the uniform cube's shell below `βJ*`; controls at `u = 1, 2`), with
one or two mutations each.

*Prior art* (workstream T; search summaries and abstract pages only, nothing read in
full; the referee found no statement attributed to a source contradicted by its
abstract).  The multicanonical ensemble (Berg–Neuhaus 1992); Wang–Landau sampling (2001);
performance limits of flat-histogram methods and the non-optimality of the flat ensemble
for round-trip times (Dayal et al. 2004; Trebst–Huse–Troyer 2004); worst-case optimal
importance proposals for a relative-entropy criterion (Cérou–Héas–Rousset 2022) and minimax
mixture weights (He–Owen 2014), the closest statements in form; lower bounds for
non-adaptive integration of densities with Lipschitz logarithm (Mathé–Novak 2007, behind
Theorem 11.45).  Not found: a statement that the flat-histogram ensemble is
minimax-optimal for a *certified* estimate of a partition function over a class of
perturbations of a known part; exact non-adaptive or hinted exponents for such a class;
shells of barrier configurations as extremal perturbations.  "Not found", not "new".
*The Scientific Discovery Division's reading* (SCI-REV-0004): the first half of Theorem
11.76 — an invariant problem has an optimal invariant (here: type-stratified) sample — is
a **reformulation** of the invariance principle of the theory of experimental design
(invariant designs are optimal; Kiefer) combined with Bakhvalov's averaging over the
group, with one small new lemma, that type-wise quantile truncation preserves the
Lipschitz class (Theorem 11.61(a)); whether the second half (shells at coexistence) is in
print it could not resolve.

*Not done.*  The adaptive exponent (O4) beyond the cases of Proposition 11.81(c).  The value
of the supremum beyond `e₀` (O2) and binary optimality below it (C1).  The non-adaptive
exponent where cones around profile classes fall short (O5).  A proof that `R_H < R_unif`
between the junction `min{βJ*, βJ_w}` and `βJ*` at large slopes, and of the junction formula
itself.  The equality "cone
formula = sup–min" for convex `I` beyond twenty-four numerical cases (a proof for
differentiable `φ` is indicated in Theorem 11.80(d), not written out).  A referee's check
of the completion of Proposition 11.81(c).  Asymmetric two-phase models
with free blocks.  Product samplers and plain Monte Carlo for interacting known parts.
Bounded accuracies beyond the two lower bounds.  Machine-checking of anything in this
section beyond Theorem 11.76(a), (b).

### 11.24 Rounds of adaptivity: two rounds lie strictly between a fixed sample and full adaptivity

§§11.16–11.19 left a gap in the middle: without a hint a sample fixed in advance costs
`e^{na}` at a bounded accuracy, a fully adaptive algorithm `e^{nh}` (`a = KL(p_u‖½)`,
`h = KL(Λ₁/u‖½)`, `h/a ≈ ¼` for small slopes), and the adaptive algorithms as written
interleave evaluations and decisions `Θ(n²)` times.  How much adaptivity is needed?  An
*`r`-round algorithm* asks `r` batches of evaluations, each chosen after the answers to the
earlier ones; `τ^{(r)}` denotes the exponent of the least cost of `r`-round algorithms at a
bounded accuracy on the cube class `L_u` (uniform measure, no known part), so `τ^{(1)} = a`
(Theorems 11.44, 11.45) and `lim_r τ^{(r)} ≥ h`.  For `r ≥ 2` the limit in `n` is not shown to
exist: "`τ^{(r)} ≤ X`" is a statement about the `limsup` of `n⁻¹ ln` of the least cost,
"`τ^{(r)} ≥ X`" about the `liminf` (the workstream's convention, which our first version
omitted — Scientific Discovery Division, SCI-REV-0003, m6).  Workstream U
(`docs/workstreams/U_REPORT.md`):

1. **The nested algorithms need a number of rounds that does not depend on `n`:** a ladder
   with `L` rungs can be run in `L` rounds, `k` levels with `L` rungs each in `L^{k−1}` rounds
   (Theorem 11.84).  Hence `τ^{(r)} → h` as `r → ∞` (not: `τ^{(r)} = h` for some `r` — that is
   open), and two rounds already beat every fixed sample:
   `τ^{(2)} ≤ 0.624a` at `u = 1` (the golden ratio `0.618a` for small slopes).
2. **Two rounds do not reach the adaptive exponent:** `τ^{(2)} ≥ θ₂*(u) > h` for every slope
   (`θ₂* = 0.359a = 1.37h` at `u = 1`), by a new family of instances in which a
   flat-histogram structure in one block of coordinates *dilutes* the first batch
   (Theorem 11.86).  The bound holds for the expected number of evaluations at one
   instance, the flat histogram of a block (Corollary R4.2 below, the Scientific Discovery
   Division's strengthening).  From `n ≈ 800` on (`u = 1`, accuracy 1) the two-round lower
   bound exceeds the lower bound that holds for all algorithms (`e^{0.037n}` against
   `e^{0.030n}` at `n = 3200`).  **These are two lower bounds; the separation from adaptive
   algorithms is asymptotic, and none is shown at such a size:** there the known adaptive
   algorithms cost more than either (`e^{0.061n}` with two levels, `e^{0.051n}` with three, at
   `n = 4000`, a bounded accuracy and the flat instance — §11.19, referee R8), and the
   two-round algorithm has not been evaluated at any finite `n`.  (Our first version — "at
   `n = 3200` … two rounds need `e^{0.037n}` evaluations, against the lower bound `e^{0.030n}`
   that … is attained in the exponent by adaptive ones" — read as a separation at that
   size: Scientific Discovery Division, SCI-REV-0003, m5.)
3. So `a = τ^{(1)} > τ^{(2)} > h = lim τ^{(r)}`: the hierarchy has at least three levels.
   Whether three rounds reach `h` is open; the natural continuation of the two-round
   family hides nothing from a third batch.

**Status of this section.**  Paper proofs by workstream U, **refereed** by the Scientific
Discovery Division (SCI-REV-0003; the full report, `docs/science/workstreams/R4_REPORT.md`,
and its code are on the branch `research/scientific-translation`; by its account the
exponents, the twins on type grids and on whole cubes and the asymptotic check were coded
before it opened our code): **no critical finding; one major finding** — Theorem 11.84(ii)
claimed its bound on the candidate sets, and with it the cost bound of the batched
schedule, "in every run", but it holds on the good event only; a stopping rule before
each stage repairs it and is now part of the statement — **and nine minor ones**, all
applied: eight below, marked where they stand, and one (a slip in the workstream's proof
of Claim B) in the errata of `U_REPORT.md`.  No exponent, no inequality between exponents
and no number of the section changed.  The referee's verdicts: Theorem 11.84 proved with
that rule, given Theorems 11.56, 11.58 and Proposition 11.57; Lemma 11.85 proved, and for
two rounds the machine-checked statements say what the prose says; Theorem 11.86 proved,
every step re-derived and both tables replicated; Corollary 11.87 and Proposition
11.88(a)–(c) proved; 11.88(d): the lower half proved, the upper half a sketch as labelled;
11.88(e) and the three-block continuation not examined; the values of the recursion for
four and more rounds replicated by nobody.  The division added a strengthening, stated
below as its Theorem R4.1 and Corollary R4.2.  (The coordinator's own check of Theorem
11.84, described next, had not caught the major finding: it followed Claims A and B on
the good event and never asked what an inner procedure may return off it.)  Before the review
the coordinator had checked Theorem 11.84 line by line against the proof of Theorem 11.56 in
`K_REPORT.md` §2 (both claims of its proof use only steps 2, 6 and 7 of that proof and one
additional family of Chernoff events), re-derived Lemma 11.85 (in a slightly different
form, below) and Theorem 11.86, and re-computed with own code
(`experiments/coordinator_checks/rounds_U/`): the two-round upper bound at five slopes, the
three-round value, the asymptotic lower bound `θ₂*` at five slopes, and **the exact
finite-`n` twins of Theorem 11.86 from its statement** (own implementation; the Lipschitz
property, the coincidence on what the batches see and the gap are asserted in the code).
Not re-computed: the values of the recursion for more than three rounds, and the
negative results on nested structures.  Machine-checked: Lemma 11.85 for two rounds, in
abstract form and for randomness with finite support (`TwoRounds.lean`); its form for the
expected cost at one instance (`TwoRoundsExpected.lean`: the Scientific Discovery
Division's file, adopted unchanged and compiled here, in the axiom audit); the application
to the twins and everything about algorithms are paper proofs.

**Theorem 11.84 (a ladder is as many rounds as it has rungs) [P, given Theorem 11.56;
workstream U, Theorem U1 and Corollaries U1.1–U1.3; refereed (SCI-REV-0003): proved with the
stopping rule, which our first version lacked].**  In the setting of Theorem 11.56 let
the inner procedure `I_l` of rung `l` be an `r_l`-round procedure.  The following batched
schedule B2L⁺ has `r_1 + … + r_L` rounds: *stage 1* evaluates the reference point, the
trivial brackets and `I_1` on the fibres of all `M_max = K2^{m_max}` outer points; *stage `l`*
computes from the stored brackets of rung `l − 1` the empirical levels

    λ_j := max{ ℓ₀ , c_η(1+η)^{−1}e^{−b} · max{ s_{i′}·N_L(i′, M)/M : i′ < j, M ∈ ℳ, N_L(i′, M) ≥ K } },      M̂_j := max{ K , 2ν s_j/(λ_j e^b) }

(`N_L(i′, M)` the number of the first `M` points whose stored lower end exceeds `s_{i′}`), the
candidate set `C_l := {i ∈ C_{l−1} : ∃j, i ≤ M̂_j, U_i > s_j, L_i ≤ s_je^{−b}}`, **stops and returns
the trivial bracket `[s₀, s₀e^{2un}]` if `|C_l| > N_l := K + (J+1)·max{K, 4(1+η)c_η^{−1}e^λν e^{x_{l−1}}}`**
(the *stopping rule*, applied before any evaluation of stage `l`; the workstream's variant,
"if a stored bracket of rung `l − 1` has ratio above `e^{x_{l−1}}`", serves as well), and
otherwise runs `I_l` on the fibres of `C_l` in parallel; the output is Algorithm 2L⁺ run as
a computation on the stored brackets, and the trivial bracket if that computation asks
for a pair `(i, l)` with `i ∉ C_l`.
With `L + 3` in place of `L + 2` in the constant `K`, for every `ψ ∈ L_u`:
(i) with probability at least `1 − δ` the output is exactly the bracket of Algorithm 2L⁺
with the same random choices (*Claim A:* on the good event every call `(i, l)` of the
sequential algorithm has `i ∈ C_l`, and the stopping rule does not fire); (ii) `|C_l| ≤ N_l`
whenever every stored bracket of rung `l − 1` has ratio at most `e^{x_{l−1}}` (*Claim B*: a
deterministic statement about the stored brackets, whose hypothesis holds on the good
event), and `N_l ≤ 3(J+1)·cnt(x_{l−1})`; so, **by the stopping rule, in every run** stage `l` runs
`I_l` on at most `N_l` fibres and the cost is at most
`1 + M_max(1 + C_1) + Σ_{l≥2} 3(J+1)cnt(x_{l−1})·C_l`.
*Correction (Scientific Discovery Division, SCI-REV-0003, finding M1).*  Our first version
had no stopping rule and claimed `|C_l| ≤ N_l` "in every run".  That was false.  An inner
procedure may return a bracket wider than promised with probability `δ′` — its own trivial
bracket, for instance; then a member's lower end need not exceed `s_je^{−x_{l−1}}`, the count
of Claim B fails, and `C_l` can be all of `C_{l−1}` (the division's demonstration, re-run by
us with identical output: `|C_2| = 393 216 = M_max` against `N_2 = 79 931` when all calls of
rung 1 return the trivial bracket, with reduced constants;
with the unreduced constants of the theorem at the flat instance, `u = 1`, outer dimension
`60` of `n = 80`, a check of ours gives `|C_2| = M_max = 2.2·10¹²` against `N_2 = 4.4·10⁹`
(`experiments/coordinator_checks/rounds_U/m1_stopping_rule.py`)).
Such runs have probability at most `δ`, and no exponent and no statement "with probability
`1 − δ`" was affected.  But the definition of a bracket procedure (§11.18) asks for a cost
bound that holds always, and every level built on a batched procedure — the recursion
(a), the schedules behind (c) — multiplies by that bound: it is the gap that referee R7
found in Theorem 11.52 and referee R8 in Theorem 11.56.
**Every exponent statement derived from Theorem 11.56 for a fixed choice of the levels and
their ladders — Proposition 11.57, and the algorithms in the proofs of Theorems 11.54 and
11.58 for a fixed `η > 0` — therefore holds for an algorithm whose number of rounds is the
product of the ladder lengths of its levels, independently of `n`.**  This is less than
the statements `exp(nθ + o(n))` of Theorems 11.54 and 11.58, whose algorithms have a number
of levels that grows as the exponent is approached: what is proved is that for every
`η > 0` there is `r(η) < ∞`, independent of `n`, with `τ^{(r(η))} ≤ h + 3η` (workstream U,
Corollary U1.3); whether `τ^{(r)} = h` for a finite `r` is open question (1) below.  (Our first
version of the sentence had no such restriction and, read literally, asserted it —
Scientific Discovery Division, SCI-REV-0003, m1.)  Consequences:
(a) *The recursion in `r`.*  With `T^{(1)} = θ_na` (`T^{(1)}(0) = a`) and, for `r ≥ 2`,

    T^{(r)}(g) = min{ T^{(r−1)}(g) , inf max{ μ + (1−φ)T^{(r_1)}(ξ_1) , max_{2≤l≤L} [ min(μ, (1−φ)ξ_{l−1}) + (1−φ)T^{(r_l)}(ξ_l) ] } }

(infimum over `φ`, ladders `ξ_1 > … > ξ_L` and `r_1 + … + r_L ≤ r` **with every `r_l ≤ r − 1`** —
the workstream's restriction, which our first version dropped: without it a one-rung
ladder with `r_1 = r` defines `T^{(r)}` through itself (SCI-REV-0003, m2); `μ = φθ_na((g − β)/φ)`,
`ξ_L = β/(1−φ)` for `g > 0`, and `μ = φa`, `ξ_L = 0` for `g = 0`): `τ^{(r)} ≤ T^{(r)}(0)`.
(b) *Two rounds:* `τ^{(2)} ≤ T^{(2)}(0) = min_{φ,ξ} max{φa + (1−φ)θ_na(ξ), min(φa, (1−φ)ξ) + (1−φ)a} < a` — a
bracket of accuracy `ξn_i` in every fibre, then a bracket of bounded accuracy in the
polynomially-many-times-`e^{ξn_i}` fibres that are still undecided.  `T^{(2)}(0)/a = 0.618`
(`= (√5 − 1)/2`, small-slope limit), `0.620`, `0.624`, `0.641`, `0.665` at `u = 0.5, 1, 2, 3`.
(c) *Convergence:* `τ^{(r)} → h`; numerically `T^{(r)}(0)/a = 0.624, 0.541, 0.481, 0.440, 0.421, 0.379, 0.354, 0.335`
for `r = 2, 3, 4, 6, 8, 16, 32, 64` at `u = 1` (`h/a = 0.263`; grid values, upper bounds for the
recursion; the first two re-computed by the coordinator, and `T^{(3)}(0) ≤ 0.5403a` by the
Scientific Discovery Division with a witness — the ladder `(1,1,1)` at `φ = 0.512`,
`ξ_1 = 0.631a`, `ξ_2 = 0.107a`, which gives `0.54026a` when we evaluate the three terms; **the
values for `r ≥ 4` rest on one grid computation of the workstream and have no stored
witness** — its output keeps, for each `r`, the value and the outer fraction, not the
ladders and the allocation of rounds with which the value could be checked in
milliseconds: SCI-REV-0003, m9) — a gap of about
`0.37a/(log₂ r)^{0.8}` in this range.  No lower bound on the rate.
*Proof of Claims A, B.*  A: by Theorem 11.56(iv) a call during level `j` at a pass of size
`M ≥ i` has `M ≤ max{K, 2ν s_j/(ℓ_je^b)}`, `ℓ_j` the running lower bound at the entry of level `j`; it
suffices that `ℓ_j ≥ λ_j`.  If `N_L(i′, M′) ≥ K` the points counted have `W > s_{i′}`, so the
additional Chernoff events (upper tails at the thresholds `s_j`; this is the change of `K`)
give `p(s_{i′}) ≥ N_L(i′, M′)/((1+η)M′)`; level `i′` was left before level `j`, so by steps 2 and 7
of the proof of Theorem 11.56 `ℓ_j ≥ c_ηe^{−b}s_{i′}q_{i′} ≥ c_ηe^{−b}s_{i′}p(s_{i′})`.  B: a member `i > K`
with witness `j` has `K < i ≤ 2ν s_j/(λ_je^b)` and `U_i > s_j`, hence — **here, and only here,
the hypothesis that its stored bracket has ratio at most `e^{x_{l−1}}` is used** —
`L_i ≥ U_ie^{−x_{l−1}} > s_je^{−x_{l−1}}`.  If no level lies below `s_je^{−x_{l−1}}`, then
`i ≤ 2ν s_j/(ℓ₀e^b) < 2νe^{x_{l−1}}`.  Otherwise the member is counted in `N_L(i′, M*)` for the
largest level `i′` with `s_{i′} ≤ s_je^{−x_{l−1}}` and the least `M* ∈ ℳ` that is at least
`min{M_max, 2ν s_j/(λ_je^b)}`; `M* ≥ 2K` because that minimum is at least `i > K`, so
`M* < 4ν s_j/(λ_je^b)`; and either fewer than `K` points are counted, or the definition of `λ_j`
as a maximum of *empirical* quantities bounds the count by
`(1+η)c_η^{−1}e^bλ_jM*/s_{i′} < 4(1+η)c_η^{−1}e^λν e^{x_{l−1}}`.  Summing over the `J + 1` levels and
adding the at most `K` members `i ≤ K` gives `N_l`.  *The cost in every run:* by the
stopping rule stage `l ≥ 2` runs `I_l` on at most `N_l` fibres, stage 1 on `M_max`, and the
bounds `C_l` of the inner procedures hold always.  *The rule does not fire on the good
event:* there every stored bracket is valid and of ratio at most `e^{x_{l−1}}`, so Claim B
applies, and by Claim A the output computation never asks for a missing pair.  ∎

**Lemma 11.85 (what `r` batches can see) [for two rounds **[V]**: `card_distinguished_le`,
`two_round_bound` (`TwoRounds.lean`), for arbitrary point sets, hidden parameters and sets
`𝒲_t`, and for randomness with finite support, that is for finite mixtures of
deterministic algorithms (SCI-REV-0003, m8); general `r` **[P]**; workstream U, Lemma U2;
the proof below is the coordinator's version].**
Split the coordinates into `r` blocks, `Q_n = Q_{n_1} × … × Q_{n_r}`, and
call `ψ_s(x) = F(d(x¹, s¹), …, d(x^r, s^r))` *block-radial* with centres `s = (s¹, …, s^r)`; it is in
`L_u` iff `F` changes by at most `u` when one argument changes by one, and `A(ψ_s)` does not
depend on `s`.  Let `F, F′` be two such functions and `𝒲_1, …, 𝒲_r` sets of types
`(d_1, …, d_r)` such that (a) `F = F′` on every `𝒲_t`, and (b) for `t < r`, on `𝒲_t` the function `F`
depends on `(d_1, …, d_t)` only.  Put
`p_t := max_{d_1..d_{t−1}} P((d_1, …, d_{t−1}, D_t, …, D_r) ∉ 𝒲_t)` for independent `D_j ∼ Bin(n_j, ½)`.
Then for every randomised `r`-round algorithm whose batch `t` has at most `M_t` points in
every run on an instance `ψ_s` — nothing is assumed about its batches after other
sequences of answers; "with batch sizes at most `M_1, …, M_r`" in our first version was
ambiguous for `r ≥ 3` and more than is needed for `r = 2` (SCI-REV-0003, m3) — and
uniformly random centres, the transcripts on `ψ_s` and `ψ′_s` differ with probability at most
`Σ_t M_tp_t`; so if the algorithm is `(ε/2, δ)`-correct on `L_u` and `|ln A(F) − ln A(F′)| > ε`, then
`Σ_t M_tp_t ≥ 1 − 2δ`.
*Proof.*  Fix the coins.  Define a *virtual run*: batch `t` is answered by a function `G_t` of
the distances to `s¹, …, s^t` only that agrees with `F` on `𝒲_t` (for `t = r`: by `F`).  By
construction the virtual batch `t` is a function of the coins and of `s¹, …, s^{t−1}`, hence
independent of `s^t, …, s^r`, so each of its points has a type outside `𝒲_t` with probability
at most `p_t`, whatever its distances to the earlier centres.  Let `Ẽ_t` be the event that
all points of the virtual batch `t` have types in `𝒲_t`.  On `Ẽ_1 ∩ … ∩ Ẽ_{t−1}` the real runs
on `ψ_s` and on `ψ′_s` coincide with the virtual run up to and including the points of batch
`t`, by induction on `t` and (a), (b); in particular the virtual batch `t` is then batch `t`
of a real run on `ψ_s` and has at most `M_t` points.  (The virtual run answers different
batches by different functions `G_t`, so for `r ≥ 3` it is not a run on one function and
the bound `M_t` cannot be applied to it directly: the referee's observation.)  The virtual
batch `t` is a function of the coins and of `s¹, …, s^{t−1}`; so the probability of
`Ẽ_1 ∩ … ∩ Ẽ_{t−1} ∩ Ẽ_t^c` is at most the probability that it has at most `M_t` points and one
of them has a type outside `𝒲_t`, which is at most `M_tp_t`.  Hence `Ẽ := ∩_tẼ_t` fails with
probability at most `Σ_tM_tp_t`, and on `Ẽ` the two real runs coincide with the virtual run
throughout.  ∎  (For two rounds the virtual second batch is the second batch of a run on
one function, `x ↦ G_1(d(x¹, s¹))`, and no bound on batch sizes is needed: Theorem R4.1 below.
Nothing is assumed about what the algorithm learns: it
is given more than it can know.  `r = 1` reproduces the bound `a` of Theorem 11.45 with a
flat histogram against its truncation, and with `F = 0` against a critical dip the lemma
gives `h` for every number of rounds.)

**Theorem 11.86 (two rounds do not reach the hinted exponent) [P; workstream U, Theorem U3;
the finite-`n` statements by exact computation, re-computed by the coordinator].**  Let
`f(ρ) = KL(ρ‖½)`, `k(ρ) = KL(ρ‖p_u)`, `D(θ) := u·f^{−1}(θ) − Λ₁` (the accuracy rate certified with a
hint by `e^{nθ}` evaluations) and `x_na(θ) := D(θ) + θ` (the same for a fixed sample: the shear
law).  For blocks of fractions `φ₁ + φ₂ = 1` put

    Ξ(θ, φ₁) := min_{0 ≤ c ≤ min(θ, φ₁a)} [ φ₁·x_na(c/φ₁) + φ₂·D((θ − c)/φ₂) ].

If `Ξ(θ, φ₁) > 0` and `θ < φ₂a`, then for every accuracy rate `ε₁ < γ := min{Ξ, φ₂k(y¹)}`
(`φ₂f(y¹) = θ`) and all large `n` every two-round algorithm that is `(ε/2, δ)`-correct on `L_u(Q_n)`
for some `ε ≤ ε₁n` uses, in some run on one of the twins below, a batch with at least
`(1 − 2δ)e^{nθ}/(2(n+1)²)` evaluations — and makes at least `(1 − 2δ)e^{nθ}/(n+1)²` evaluations in
expectation on one explicit member of the class (Corollary R4.2 below).  Hence
`τ^{(2)} ≥ θ₂*(u) := sup{θ : Ξ(θ, φ₁) > 0, θ < φ₂a for some φ₁}`, and **`θ₂*(u) > h` for every `u > 0`**:

| `u` | `→ 0` | `0.5` | `1` | `2` | `3` |
|---|---|---|---|---|---|
| `θ₂*/a` | `0.346` | `0.349` | `0.359` | `0.394` | `0.440` |
| `θ₂*/h` | `1.38` | `1.38` | `1.37` | `1.33` | `1.28` |
| best `φ₁` | `0.65` | `0.65` | `0.64` | `0.61` | `0.56` |
| `T^{(2)}(0)/a` (upper bound) | `0.618` | `0.620` | `0.624` | `0.641` | `0.665` |

*The twins.*  `P_j = Bin(n_j, ½)`, `c_j = −ln P_j`, budget `T = nθ`.  What a blind batch of `e^{nθ}`
points sees: `W₁ = {c₁(d₁) + c₂(d₂) ≤ T}`; what a batch that knows the first centre sees:
`V₂ = {c₂(d₂) ≤ T} ⊃ W₁`.  Let `g_j := −`(the largest `u`-Lipschitz minorant of
`ln P_j(`mode`) − ln P_j`) — the *flat histogram* of block `j`: on the shells
`p_u ≲ d/n_j ≲ 1 − p_u` every shell has the same mass.  `F_deep :=` the lower McShane envelope
of `g₁(d₁)` from `W₁` (the deepest `u`-Lipschitz function that equals `g₁` on `W₁`),
`F_cap := max(F_deep, g₁ + g₂)`, and `F_D`, `F_S` equal `F_cap` on `V₂` and continue it outside in the
second argument at slope `−u`, respectively `+u`.  Both are in `L_u`, they coincide on `V₂`, and
on `W₁` they depend on `d₁` only: Lemma 11.85 applies with `𝒲_1 = W₁`, `𝒲_2 = V₂`,
`p₁ ≤ (n+1)²e^{−nθ}`, `p₂ ≤ (n+1)e^{−nθ}`.  `A(F_S) ≤ (n+1)²` (every type has mass at most one),
while `ln A(F_D) ≥ nγ − o(n)`: the mass of the type `(p_u, p_u)`, where the dip of the second
block is fully developed.
*Why `θ₂* > h`.*  `f` is convex, so `E_θ(c) ≥ c + D(θ)` (Jensen); at `θ = h`, `D(h) = 0`, and at `c = 0`
Jensen's inequality is strict: `Ξ(h, φ₁) > 0` for every `φ₁`, and `h < φ₂a` for `φ₁ < 1 − h/a`.
*What the instance is.*  A radial function of the first block that makes every shell
equally heavy, and on each shell a dip in the second block that starts exactly where a
blind sample stops seeing that shell (a point of shell `z` has probability `e^{−nφ₁f(z)}`, so
the sample sees the second block there only down to the radius `ρ^s(z)` with
`φ₂f(ρ^s) = θ − φ₁f(z)`).  After round 1 the algorithm knows the first centre; in round 2 it can
look at every shell with full strength and sees the rim of the dip — but the mass sits
deeper, where the twin has no dip.  A third round reads it off **[sketch]**: an algorithm
that knows the two blocks — the three-round algorithm for block-radial functions of
Proposition 11.88(d) — costs `e^{nh+o(n)}` on this instance.  For algorithms that are correct
on all of `L_u` the best three-round bound is `T^{(3)}(0) ≤ 0.541a`, far above `θ₂*` (our first
version had neither the label nor the restriction — SCI-REV-0003, m4).
**The mechanism is dilution of the first batch by a
structure that is not localised, not nesting of basins.**
*Exact sums* (accuracy 1; `E = −n⁻¹ln(p₁ + p₂)` for the largest budget at which the gap of the
twins exceeds 1; last column: the exponent of the lower bound for *all* algorithms,
Theorem 11.25(a), at the same accuracy; coordinator's implementation, splits
`n₁/n ∈ {0.45, …, 0.65}`; the workstream's numbers with a slightly different second set are
`0.0339`, `0.0360`, `0.0366`, and `0.0382` at `n = 12 800`):

| `u = 1`, `n` | `E` (two rounds) | all algorithms | | `u = 2`, `n` | `E` (two rounds) | all algorithms |
|---|---|---|---|---|---|---|
| `400` | `0.0301` | `0.0348` | | `200` | `0.1129` | `0.1116` |
| `800` | `0.0341` | `0.0323` | | `400` | `0.1152` | `0.1044` |
| `1600` | `0.0354` | `0.0309` | | `1600` | `0.1212` | `0.0993` |
| `3200` | `0.0368` | `0.0301` | | | | |

**Theorem R4.1 and Corollary R4.2 of the Scientific Discovery Division (two rounds: the
expected cost, at one instance) [R4.1: V — `card_distinguished_le_sum`,
`two_round_expected_bound`, `two_round_expected_cost`, `two_round_bound_of_class`
(`TwoRoundsExpected.lean`: the division's file from `experiments/science/ws_R4/lean/` on the
branch `research/scientific-translation`, which imports our `TwoRounds.lean` and nothing
else; adopted unchanged, read by us against the prose and compiled here; in the axiom
audit).  R4.2: P, re-derived by us from R4.1.  SCI-REV-0003, §4].**
In the proof of Lemma 11.85 for two rounds the second batch is only ever counted when the
first batch is answered by the virtual function; so no bound on batch sizes is needed.
*R4.1.*  In the abstract setting of `two_round_bound` — twins `g_{s₁s₂}`, `g′_{s₁s₂}` that agree with
a residual `v_{s₁}` on `W₁` and with each other on `W₂`, every point outside `W₁` for at most a
fraction `p₁` of the pairs `(s₁, s₂)` and outside `W₂` for at most a fraction `p₂` of the `s₂` —
every finite mixture of two-round algorithms that is `(ε/2, δ)`-correct on a class
containing the twins, whose targets differ by more than `ε`, satisfies

    1 − 2δ  ≤  E|B₁|·p₁ + E|B₂(v_{s₁})|·p₂ ,

where `B₂(v_{s₁})` is the second batch when the algorithm runs on `v_{s₁}` and the second
expectation is over the coins and a uniform `s₁`: **no assumption on batch sizes**.  In
particular the expected number of evaluations on the instance `v_{s₁}`, averaged over `s₁`, is
at least `(1 − 2δ)/max(p₁, p₂)`; and in the worst-case form the second batch need only be
bounded on a class that contains the `v_{s₁}`.  *R4.2.*  In Theorem 11.86 the virtual function
is `ψ⁰_{s¹}(x) := g₁(d(x¹, s¹))`, the flat histogram of the first block, and it is **a member
of `L_u`**.  Hence, under the hypotheses of Theorem 11.86, every randomised two-round
algorithm that is `(ε/2, δ)`-correct on `L_u(Q_n)` for some `ε ≤ ε₁n` makes, **in expectation,
at least `(1 − 2δ)e^{nθ}/(n+1)²` evaluations on the instance `ψ⁰_{s¹}`** — on average over its
centre, hence at some centre.  (The counting hypotheses hold with equality, `s ↦ x ⊕ s`
being a bijection of the cube, and `p₁, p₂ ≤ (n+1)²e^{−nθ}`; for randomness without finite
support the exchange of the two sums in the proof of R4.1 is an integral over the coins —
that step is on paper.)  So `τ^{(2)} ≥ θ₂*` holds for the expected cost, without Markov's
inequality, and the hard instance is named: for two rounds the flat histogram of a block
plays the part that the zero function plays for adaptive algorithms in Theorem 11.25(a).
Like the zero function there, it is trivial with a hint — `A(ψ⁰_{s¹})` does not depend on
the centre —; the cost is the price of being correct on the twins.  At finite `n` the rows
of the table above hold for this expected cost with `E′ := −n⁻¹ ln max(p₁, p₂) ≥ E` in place
of `E`.  Open: whether `e^{nθ₂* + o(n)}` evaluations suffice at this instance for a two-round
algorithm that is correct on `L_u`.

**Corollary 11.87 (the hierarchy) [P, given Theorems 11.84, 11.86, 11.44, 11.45, 11.58].**  For
every `u > 0`: `a = τ^{(1)} > T^{(2)}(0) ≥ τ^{(2)} ≥ θ₂*(u) > h = lim_{r→∞} τ^{(r)}`.  At `u = 1`
the two-round exponent has `liminf ≥ 0.359a` and `limsup ≤ 0.624a` (the limit is not shown
to exist; our first version wrote `τ^{(2)} ∈ [0.359a, 0.624a]` — SCI-REV-0003, m6).  Some `r₀`
has `τ^{(r₀)} < τ^{(2)}` **[P]**, because `τ^{(r)} → h < θ₂*`; that `r₀ = 48` will do,
`τ^{(48)} ≤ 0.342a`, is **[N]**: the number comes from the grid recursion of the workstream,
has no stored witness and has been re-computed by nobody (SCI-REV-0003, m9).

**Proposition 11.88 (what a round can and cannot do) [P unless marked; workstream U,
Propositions U6, U7, U9, U10].**
(a) *Conditional covering.*  To hit a ball of radius `κn` whose centre is uniform on the
sphere of radius `σn` around a known point costs `exp(n·(f(κ) − f(σ))₊ + o(n))` points, and no
less; the knowledge of the point is worth exactly the factor `e^{nf(σ)}`.
(b) *Balls hide only what they contain.*  For a plateau `B(s₁, R)` at level `−D` and a cone
around `s₂` that dips `uK` below it: if `d(s₁, s₂) + K ≤ R` the dip is invisible outside
`B(s₂, K)`; if `d(s₁, s₂) + K ≥ R + 3` it is read off from the antipode of `s₁` and its `n`
neighbours.
(c) *Radial instances need exactly two rounds:* on the radial class `τ^{(1)} = a` and
`τ^{(2)} = h` (the algorithm of Theorem 11.51 is two batches).
(d) *Block-radial functions on two known blocks* — a class between the radial class and
`L_u`: two rounds do not reach `h` (Theorem 11.86: its twins belong to the class), three do
**[sketch]**.
(e) *Nested basins do not separate two rounds from many* **[sketch + numerical, an
idealised game]**: for max–min nests of cones with independent hidden centres the
two-round value found by random search over up to four levels is exactly `h`, attained
by a single dip — a deep structure is wide, and what a blind batch of `e^{nh}` points has
not reached is cheap from where it stands.  The three-block continuation of the twins
of Theorem 11.86 hides nothing from a third batch at the budget `e^{nh}` **[numerical,
small-slope limit]**.

*Open.*  (1) Is `τ^{(3)} = h`?  Either answer would be new: a three-round algorithm reaching
`h` on all of `L_u` would have to use local information, which the nested algorithms never
do; a three-round lower bound needs a family that is not a chain of blocks.  (2) The
value of `τ^{(2)}` in `[θ₂*, T^{(2)}(0)]`, and whether the limit exists; whether two rounds can
do with `e^{nθ₂* + o(n)}` evaluations *at* the flat-histogram instance (Corollary R4.2).
(3) Strict monotonicity of `τ^{(r)}` and the rate of
`τ^{(r)} → h`.  (4) The same questions with a known part.

*Harness.*  Block XX of `experiments/falsify_conjectures.py`: XX.1 (Theorem 11.86: the twins
on type grids — Lipschitz property, coincidence on `V₂`, dependence on `d₁` only on `W₁`,
`A(F_S) ≤ (n+1)²`, and a gap above 1 at a budget whose exponent exceeds the bound for all
algorithms; and on whole cubes `Q_12`: the twins as functions of the points), XX.2 (Lemma
11.85 by simulation of the type process with an adversarial second batch; the asymptotic
formula: `E_θ(c) ≥ c + D(θ)`, `Ξ(h, φ₁) > 0`, `θ₂*` at three slopes), XX.3 (Theorem 11.84(b), (c): the
two-round value by direct minimisation, the golden ratio in the small-slope limit, the
balance formula, the three-round value, and the lower barrier `T^{(2)} ≥ θ_hint`), XX.4
(Proposition 11.88(a) by exact counting and (b) by brute force), XX.5 (Theorem 11.84, Claim B
as repaired: for adversarial arrays of stored brackets of ratio at most `e^x` the candidate
set has at most `N` members; with trivial brackets it is everything, and the stopping rule
fires); mutations detected for each; and the documented refutations DEAD.21 (two rounds
reach the adaptive exponent) and DEAD.27 (the candidate sets are small in every run — the
first version of Theorem 11.84(ii)).
In §11.23's block the documented refutation DEAD.22 was added with the final report (cones
around profile classes attain the non-adaptive exponent whenever the top of the barrier
is a contact point: false at `u = 0.30`).

*Prior art* (workstream U; search summaries only).  Adaptivity hierarchies in property
testing (Canonne–Gur 2017) and pointer chasing; rounds in parallel convex optimisation
(Nemirovski 1994; Balkanski–Singer; Bubeck et al.; Diakonikolas–Guzmán), whose hard
instances — maxima of functions each revealing one new direction — are the analogue of
the nested structures that do *not* work here; round–cost trade-offs in batched bandits
and adaptive sparse recovery; a two-batch algorithm for kernelised normalising constants
(Cai–Scarlett 2024).  Not found: a round hierarchy for normalising constants over a
Lipschitz class, or dilution by a flat histogram as the separating mechanism.  "Not
found", not "new".  *Added on the evidence of the Scientific Discovery Division*
(SCI-REV-0004; abstracts read by us): rounds of adaptivity for partition functions are a
topic of 2026 in the *sampling-oracle* model — an oracle returns samples from the Gibbs
measure at a chosen inverse temperature — where a non-adaptive annealing schedule loses
only a logarithmic factor and two rounds match sequential algorithms (Harris, Kolmogorov,
Liu, Yin, Zhang, arXiv:2604.01263; Guo, Liu, Yang, Yin, Zhang, arXiv:2609.20337): polynomial
scale, another oracle, and the opposite conclusion; no hierarchy for value queries was
found by the division either.

### 11.25 Slices: for fixed samples, and with a hint at symmetric instances, no known part that is a function of the type is harder than the uniform cube; reduction of algorithms to slices

§11.23 left three things open for known parts that are functions of the type: whether an
antiferromagnet without a field — in the limit, the uniform measure on a single type
class — has exactly the uniform cube's exponents (the workstream proved "`≥`" and found
"`=`" numerically; §12, item 2(d)(v)(δ)); the comparison with the uniform cube for
interactions that are not ferromagnetic; and adaptive algorithms without a hint
(Conjecture 11.83).  This section settles the first two — for two of the three exponents,
the hinted one of symmetric instances and the non-adaptive one; see "What this covers"
after Corollary 11.91 — by one elementary inequality
about two-by-two tables, and reduces the third to a single homogeneous space: **inside a
type class the known part is constant, across type classes there are only `n + 1` terms.**

*Status.*  The coordinator's own work (cycle 10), written after the workstream that was
commissioned for the adaptive question ended without a report (`workstreams/README.md`,
row V; `DEAD_ENDS.md` D51).  **Paper proofs**, checked numerically step by step with code that
shares nothing with the proofs (`experiments/coordinator_checks/slices/`; harness XXI.1–6
with 28 mutations) — with one hole (SCI-REV-0001, m12; the first version said "each step
checked numerically"): our scripts and harness XXI.2 test profiles with more than two
blocks for the hinted function `r` at accuracies `e ≥ 0` only — not at `e < 0`, where the proof
of Theorem 11.90(a) had a gap, and not for the non-adaptive function `n`.  Both cases are
covered by the reviewer's scripts (`experiments/science/ws_R1/thm_1190a_blocks.py` on its
branch) and were re-computed when the corrections were applied
(`experiments/coordinator_checks/slices/m2_check.py`, `minor_checks.py`; harness XXI.6 for
`r` at `e < 0`).  The deterministic core
of Theorem 11.92(b) is machine-checked (`proofs/Frontiers/SliceRefinement.lean`).
**Reviewed** by the Scientific Discovery Division (SCI-REV-0001, 25 November 2026; workstream
R1, `docs/science/workstreams/R1_REPORT.md` on its branch: own derivations, own code written
before ours was opened, a verbatim copy of the Lean file compiled): **no critical finding,
"the mathematics is sound"; four major findings** — M1: the headline said more than
Corollary 11.91 proves (two of three exponents; narrowed in the title, in "What this
covers", in Corollary 11.91(ii) and in the *Reading*); M2: the proof of Theorem 11.90(a) did
not cover negative accuracies (repaired there; the statement is true); M3: two false
statements in the first version of the remark on more than two letters (corrected at the
eleventh checkpoint, before the review reached us); M4: Lemma 11.89 is in print — **and
twelve minor ones**, applied where they are cited as m1–m12.  Lemma 11.89 and Theorem 11.90
are statements about explicit variational formulas and do not depend on §11.23; Corollary
11.91 is an inequality between the formulas of §11.23 and is an inequality between
*exponents* only through Theorems 11.78 and 11.79 (refereed "proved" by R10).  Conjecture 11.94 is a conjecture.

**Lemma 11.89 (odds ratio) [known: Hasenclever–Scholz 2013, Proposition 8(a) — see "Prior art"
below; the proof given here was found independently].**  Let `(B, X)` be a pair of binary random variables with
positive probabilities `P_{bx}` and log odds ratio `ln[P₁₁P₀₀/(P₁₀P₀₁)] = 2s ≥ 0`.  Then

    I(B; X)  ≤  ln 2 − h(σ(s))  =  K(s/2),        σ(s) = 1/(1 + e^{−s}),    K(x) := x·tanh x − ln cosh x,

with equality iff `s = 0` or both marginals are uniform.  Equivalently: **among
binary-input binary-output channels with a given odds ratio the symmetric one has the
largest capacity** (and in the capacity-achieving joint law of an asymmetric one the field
of the input is opposite to the field of the channel and weaker, `−h₂ < h₁ < 0` in the
notation of the proof; the input *distribution* nevertheless favours the more reliable
symbol — `μ = EB > 0` for `h₂ > 0` in every case computed **[N]**, as for the Z-channel.  The first
version said that the input "leans against the channel's bias", which is true of the field
and false of the distribution: Scientific Discovery Division, SCI-REV-0001, m1).

*Proof.*  Write the table as an Ising pair, `P(b, x) ∝ exp(Jbx + h₁b + h₂x)`, `b, x = ±1`,
`J = s/2 > 0`; the channel `B → X` is `(J, h₂)`, the input law is fixed by `h₁`, and
`I(0, 0) = ln 2 − h(σ(2J))`.  Put `φ = ln cosh`,

    δ(h) := ½[φ(h+J) − φ(h−J)],      T(h) := J[tanh(h+J) + tanh(h−J)] − 2δ(h),      Δ(h) := tanh(h+J) − tanh(h−J) > 0;

`δ` and `T` are odd, `Δ` is even, `δ` is strictly increasing with `|δ| < J`.
(1) *The information density.*  `P_B(b) ∝ e^{h₁b}·2cosh(h₂ + Jb)` and `ln 2cosh(h₂ + Jb) = const + δ(h₂)b`,
likewise for `X`; so `ι := ln[P/(P_BP_X)] = Jbx − δ(h₂)b − δ(h₁)x + const`.
(2) *The gradient.*  In an exponential family `∂_θE_θg_θ = Cov(g_θ, T_θ) + E∂_θg_θ`, and the
three scores have mean zero, so `∂I/∂h₁ = Cov(ι, B)`.  With `μ = EB` and
`E[X | B = ±1] = tanh(h₂ ± J)`: `Cov(BX, B) = ½(1−μ²)[tanh(h₂+J) + tanh(h₂−J)]`,
`Cov(X, B) = ½(1−μ²)Δ(h₂)`, hence

    ∂I/∂h₁ = ½(1 − μ²)·[ T(h₂) − δ(h₁)Δ(h₂) ],        ∂I/∂h₂ = ½(1 − ν²)·[ T(h₁) − δ(h₂)Δ(h₁) ]      (ν = EX).

(3) `T(h) < 0` *for* `h > 0`.  With `a = h + J > |b|`, `b = h − J`: `T = ½(a−b)(tanh a + tanh b) − ∫_b^a tanh`.
If `b ≥ 0`, `tanh` is strictly concave on `[b, a]` and the integral exceeds the trapezoid.
If `b < 0`, `∫_b^a tanh = ∫_{|b|}^a tanh ≥ ½(a − |b|)(tanh a + tanh|b|)`, which exceeds
`½(a + |b|)(tanh a − tanh|b|)` by `a|b|·(tanh|b|/|b| − tanh a/a) > 0`.
(4) *The kernel:* `−T(h) < δ(h)Δ(h)` *for* `h > 0`.  With `α = e^{2a} > β = e^{2b}`, `αβ > 1`, the
difference of the two sides is, identically,

    −T − δΔ = [ (αβ + 2β + 1)·ln((α+1)/(β+1)) − β(α+1)·ln(α/β) ] / ((α+1)(β+1)),

and with `X = 1/(1+α)`, `Y = 1/(1+β)` (`0 < X < Y`, `X + Y < 1`) its negativity is
`X ln(Y/X) < (1−Y) ln((1−X)/(1−Y))`.  Put `Z = 1 − Y > X` and `W = Y − X > 0`: the two sides are
`−g_W(X)` and `−g_W(Z)` for `g_W(t) := t·ln(t/(t+W))`, and `g_W′(t) = W/(t+W) − ln(1 + W/t) < 0`.
(5) *The capacity decreases with the field of the channel.*  For fixed `h₂ > 0`, `I` is
maximal in `h₁` where `δ(h₁) = T(h₂)/Δ(h₂) < 0` (by (2), (3)), i.e. at `h₁ = −k` with `k > 0` and
`δ(k) = g(h₂)`, `g := −T/Δ`.  By (4) `g < δ` on `(0, ∞)`, so `δ(k) < δ(h₂)`, `k < h₂`, and
`g(k) < δ(k) < δ(h₂)`.  (Two facts that the envelope theorem needs, SCI-REV-0001, m2: the root
exists and is unique because `δ` maps `(0, ∞)` increasingly onto `(0, J)` and
`0 < g(h₂) < δ(h₂) < J` by (3) and (4); and it is a non-degenerate maximum,
`∂²I/∂h₁² = −½(1 − μ²)·δ′(h₁)·Δ(h₂) < 0` there, so the maximiser is differentiable in `h₂`.)
By the envelope theorem and (2),
`dC/dh₂ = ½(1−ν²)[T(−k) − δ(h₂)Δ(k)] = ½(1−ν²)Δ(k)[g(k) − δ(h₂)] < 0`.
(6) `C` is even in `h₂`, so `I(h₁, h₂) ≤ C(h₂) ≤ C(0) = I(0, 0)`, with equality only for
`h₂ = 0` and `h₁ = 0` (the mutual information is strictly concave in the input law).  ∎

*Remark (a four-line proof, and a pointwise form of the lemma)* **[P; Scientific Discovery
Division, SCI-REV-0001 §4, workstream R1; re-derived by us line by line and re-computed].**
On the fibre of tables with given marginals, `T_c(b, x) = p_bq_x + c·bx` (`b, x = ±1`), the log
odds ratio `ω = 2s` satisfies `dω/dc = S := Σ_{b,x} 1/T_c(b, x)`, and
`dI/dc = Σ_{b,x} bx·ln T_c(b, x) = ω` (thermodynamic integration; the terms with the marginals
cancel), so `I = ∫₀^ω ω′ dω′/S(ω′)`.  With `d₊ := T₊₊ + T₋₋ ≥ 2g₊` and `d₋ := T₊₋ + T₋₊ ≥ 2g₋`
(arithmetic and geometric means; `g₊² := T₊₊T₋₋`, `g₋² := T₊₋T₋₊`), `d₊ + d₋ = 1` and
`g₊/g₋ = e^{ω/2}`:

    S = (d₊ + d₋)(d₊/g₊² + d₋/g₋²) ≥ 8 + 4(g₊/g₋ + g₋/g₊) = 16·cosh²(ω/4),

with equality iff both marginals are uniform.  Hence
`I ≤ ∫₀^ω ω′ dω′/(16cosh²(ω′/4)) = K(ω/4) = K(s/2)`, with the equality case of the lemma.  ∎
The pointwise step says more than the lemma: **among two-by-two tables with a given odds
ratio the harmonic mean `4/S` of the four cells is largest for the table with uniform
marginals.**  On the ray of a centre `(m, κ)` of the slices below, the table (block, letter)
is `T_c` with the marginals `(m, κ)` and `c = ℓ/2`, so `F′ = s`, `F″ = S/4` and

    Ψ″_{m,κ}(s) = 4/S ≤ ¼·sech²(s/2) = Ψ_c″(s)   for all s ≥ 0        (curvature domination),

with equality at some `s > 0` only if `m = κ = ½`.  This gives Theorem 11.90(c) in one line and
without the mutual information, and shows that the gap to the cube is nondecreasing in
the slope (see the proof there).  Checked numerically by the reviewer (`lemma_1189.py`,
`thm_1190.py` on its branch) and re-computed for this correction
(`experiments/coordinator_checks/slices/minor_checks.py`): `S ≥ 16cosh²(ω/4)` on `2·10⁴`
random tables, the two derivatives against differences, `Ψ″ = 4/S` against second
differences of the Legendre transform.

*Prior art: the lemma is known.*  It is Proposition 8(a) of Hasenclever and Scholz,
*Comparing measures of association in 2×2 probability tables* (arXiv:1302.6161, 2013; Open
Stat. Probab. J. 2016): in their coordinates `x = ln√(odds ratio)`, `y`, `z` (the two margins)
the signed mutual information at fixed `x ≠ 0` "has exactly one maximum at the origin
`(y, z) = (0, 0)`", the table with uniform margins — the statement above with `x = s`,
including the equality case.  Found by the Scientific Discovery Division (SCI-REV-0004,
workstream A1; the proposition was then read by us in the full text of the arXiv
version; its proof, in an appendix, was not).  The first version of this section said
"not found in two searches; may well be folklore"; our two searches had been for
capacities of channels, not for measures of association.  The division also gives a
five-line proof (two exponential tilts that keep the odds ratio; the chord slope of
`ln(1 − cx)` decreases; `docs/science/workstreams/A1_REPORT.md` §2.1 on its branch), shorter
than the one above, which is kept because the harness checks each of its steps; a second
proof of the division, by thermodynamic integration, is the remark above (SCI-REV-0001).  The
capacity of the binary asymmetric channel and its non-uniform optimal input are textbook
material (bounds through the Bhattacharyya parameter: Kesal 2017, by title and abstract).
**What is ours in this section is therefore the application** — Theorem 11.90, Corollary
11.91 and the reduction of Theorem 11.92 — which the division did not find in print.

**Slices.**  Fix `κ ∈ (0, 1)` and `u > 0`, and consider block profiles *inside the type class of
density `κ`* (`μ̄ = ν̄ = κ`; then `MI(μ) = Σ_jλ_jKL(μ_j‖κ)`):

    r^κ_μ(e) := min{ MI(ν) : ν̄ = κ,  u·dist(ν, μ) ≤ e + MI(μ) },            R^κ(e) := sup_μ r^κ_μ(e),
    n^κ_μ(X) := min{ MI(ν) : ν̄ = κ,  MI(ν) + u·dist(ν, μ) − MI(μ) ≤ X },      N^κ(X) := sup_μ n^κ_μ(X)

(suprema over feasible profiles; these are `V`, `r_μ`, `n_μ` of §11.23 for the uniform measure
on one type class, where no exit can change the type).  Two blocks are the ones and the
zeros of a centre of type `m`; the profiles of type `κ` then form one ray,
`(κ + ℓ/(2m), κ − ℓ/(2(1−m)))`, on which `dist` is `|ℓ − ℓ′|` and

    F_{m,κ}(ℓ) := m·KL(κ + ℓ/2m ‖ κ) + (1−m)·KL(κ − ℓ/(2(1−m)) ‖ κ),      Ψ_{m,κ}(s) := max_{ℓ≥0}[sℓ − F_{m,κ}(ℓ)],
    F*_{m,κ}(t) := t·Ψ_{m,κ}(u) − Ψ_{m,κ}(tu),            F*_c(t) := t·ln cosh(u/2) − ln cosh(tu/2)

(`Ψ_{m,κ}(s) = min{mΛ_κ(θ₁) + (1−m)Λ_κ(θ₂) : θ₁ − θ₂ = 2s}`, `Λ_κ(θ) = ln(1 − κ + κe^θ) − κθ`; for
`m = κ = ½`: `F = KL(½ + ℓ‖½)`, `Ψ = ln cosh(s/2)`, `F* = F*_c`, the game function of the uniform
cube, whose two functions are `R̂_c(e) := max_{0≤t≤1}[F*_c(t) − te]`, which is
`R_unif(e) = KL((Λ₁+e)/u‖½)` for `−K(u/2) ≤ e ≤ ln cosh(u/2)`, and
`θ_na^{cube}(X) = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ X} = max_{0≤τ<1}(F*_c(τ) − τX)/(1−τ)`).
Outside that range the two forms of the first differ: the game form `R̂_c(e)` is `−e` below
it and `0` above, the `KL` form is larger on both sides (and not defined below `−Λ₁`);
wherever negative accuracies occur in this section the cube's function is `R̂_c`
(SCI-REV-0001, m5: the first version equated the two forms for all `e`).

**Theorem 11.90 (a slice is never harder than the cube) [P; coordinator; part (a) at negative
accuracies with the repair of the Scientific Discovery Division, SCI-REV-0001, M2].**
(a) *Binary centres suffice on a slice:* `R^κ(e)` for `e ≥ −h(κ)` and `N^κ(X)` for `X ≥ 0` are
suprema over two-block profiles (for `e < −h(κ)` no profile of type `κ` is feasible).
(b) *Closed forms.*  For a centre of type `m`, the suprema over its shells `ℓ ≥ 0` are

    V_{m,κ}(e) = F_{m,κ}( (Ψ_{m,κ}(u) − e)₊/u ) = max_{0≤t≤1}[F*_{m,κ}(t) − te]   (e ≥ 0),
    N_{m,κ}(X) = F_{m,κ}(ℓ_X) = max_{0≤τ<1}(F*_{m,κ}(τ) − τX)/(1 − τ),      uℓ_X − F_{m,κ}(ℓ_X) = Ψ_{m,κ}(u) − X,  ℓ_X ≤ ℓ*,

where `ℓ*` maximises `uℓ − F_{m,κ}(ℓ)` (the Gibbs shell of the cone); the game form of `V` holds
for all `e ≥ −F_{m,κ}(ℓ_max)`, `ℓ_max` the end of the ray, and is `−e` for `e ≤ −F_{m,κ}(ℓ*)`;
below `−F_{m,κ}(ℓ_max)` no shell of the centre is feasible (`F_{m,κ}(ℓ_max) ≤ h(κ)`, with
equality for `m = κ`).
The half `ℓ < 0` of the ray consists of the shells of the antipodal centre, of type `1 − m`;
over the whole ray the closed form would be false (`0.0202` against `0.1441` at
`(m, κ, u) = (0.83, 0.166, 4)`, `e = 0`), which is harmless after the supremum over `m`.
(SCI-REV-0001, m3, m4: the first version said "over its shells" and "for all real `e`".)
(c) *Domination.*  For all `κ`, `m` and `0 ≤ t ≤ 1`: `F*_{m,κ}(t) ≤ F*_c(t)`, with equality for some
`t ∈ (0, 1)` only if `m = κ = ½`.  Hence

    R^κ(e) = sup_m V_{m,κ}(e) ≤ R̂_c(e)   (e ≥ −h(κ)),        N^κ(X) = sup_m N_{m,κ}(X) ≤ θ_na^{cube}(X)   (X ≥ 0),

with equality for `κ = ½` (at `m = ½`) and strict inequality for `κ ≠ ½` wherever the right
side is positive and, for `R^κ`, `e > −K(u/2)` — for `−h(κ) ≤ e ≤ −K(u/2)` both sides are `−e`
(SCI-REV-0001, m6; the first version claimed strictness wherever the right side is
positive): **the slice of density `½` has exactly the uniform cube's functions,
every other slice has smaller ones.**
*Numbers* (`u = 1`, `e = 0`; `R^κ(0)`, the best centre type for `R^κ(0)`, `N^κ(0⁺)`):
`κ = 0.5`: `0.029139` (`m = 0.500`), `0.110944`;  `0.45`: `0.028856` (`0.477`), `0.109898`;  `0.4`: `0.028005` (`0.454`), `0.106755`;
`0.3`: `0.024588` (`0.408`), `0.094080`;  `0.2`: `0.018842` (`0.362`), `0.072574`;  `0.1`: `0.010688` (`0.316`), `0.041588`
(`experiments/coordinator_checks/slices/out_slice_table.txt`, also for `u = 2`).
**The best centre of an off-centre slice does not lie in the slice** (its type is between
`κ` and `½`).  The centre types printed are those for `R^κ(0)`; `N^κ(0⁺) = sup_m F_{m,κ}(ℓ*)` is
attained at other ones — `m = 0.471`, `0.442`, `0.383`, `0.325`, `0.266` for `κ = 0.45, …, 0.1`
(the same file prints them, to `10⁻⁴`).  And `N^κ` has a square-root cusp at zero,
`N^κ(X) = N^κ(0⁺) − Θ(√X)` (at `κ = 0.3`: `N^κ(10⁻¹²) = N^κ(0⁺) − 5.8·10⁻⁷`), so `0⁺` means the limit
`F(ℓ*)` and must not be evaluated at a small positive `X`: `out_slice_check1.txt`, item (e),
has `0.110924` for `0.110944` for that reason (SCI-REV-0001, m11; re-computed).

*Proof.*  (a) For a profile with blocks `(λ_j, μ_j)`, `r^κ_μ(e)` is a convex programme in `ν` with
the Slater point `ν = μ`, so

    r^κ_μ(e) = max_{t≥0, ξ} [ Σ_jλ_j g_{t,ξ}(μ_j) − te ],      g_{t,ξ}(x) := min_{y∈[0,1]}[KL(y‖κ) + tu|y − x| + ξ(y − κ)] − t·KL(x‖κ).

For fixed `(t, ξ)` this is linear in the law `ρ = Σ_jλ_jδ_{μ_j}` of the block densities, a
finitely supported law with mean `κ`, and every such law is a mixture of laws with mean `κ`
on at most two points.  So, for `e ≥ 0`, where every profile is feasible,
`sup_μ r^κ_μ(e) = sup_{t,ξ}sup_ρ[E_ρg_{t,ξ} − te]` is a supremum over
two-point laws, i.e. (duality again) over two-block profiles.  The same for `n^κ` and
`X ≥ 0`, whose Lagrangian is
`Σ_jλ_j[(1+τ)KL(ν_j‖κ) + τu|ν_j − μ_j| + ξ(ν_j − κ) − τKL(μ_j‖κ)] − τX` (again every profile is
feasible; at `X = 0` read "sup" for "max" in the dual).
*Negative accuracies* (Scientific Discovery Division, SCI-REV-0001, M2; the first version
gave the argument above for all `e`).  For `e < 0` a profile is feasible iff
`E_ρKL(·‖κ) ≥ −e` — a *second* linear constraint on `ρ`, which the decomposition into two-point
laws ignores: the two-point components of a feasible law can be infeasible, and for an
infeasible law the dual function is unbounded (`t → ∞`), so that the chain above, read
literally, gives `R^κ(e) ≤ +∞`.  The repair.  Let `−h(κ) ≤ e < 0` and fix `(t, ξ)` and a finite
support.  The laws on that support with mean `κ` and `E_ρKL(·‖κ) ≥ −e` form a polytope, and the
linear functional `ρ ↦ E_ρg_{t,ξ}` is largest at a vertex.  A vertex has at most three atoms,
and if it has three the second constraint is active: `MI(μ) = −e`, the budget `e + MI(μ)` is
zero, the only exit is `ν = μ`, and `r^κ_μ(e) = −e`.  By weak duality
`E_ρg_{t,ξ} − te ≤ r^κ_μ(e)` at every vertex, and the duality displayed above holds for every
profile with `e + MI(μ) > 0` (if `e + MI(μ) = 0`, then `r^κ_μ(e) = −e` anyway); hence
`R^κ(e) ≤ max(R^{κ,(2)}(e), −e)`, where `R^{κ,(2)}` is the supremum over two-block profiles.  And
`R^{κ,(2)}(e) ≥ −e`: on the ray of the centre `m = κ`, `F` takes every value in `[0, h(κ)]`, and
the shell with `F = −e` has the value `−e`.  So `R^κ = R^{κ,(2)}` on `e ≥ −h(κ)`; for `e < −h(κ)` no
profile is feasible.  (Numerically at `e < 0`: the reviewer's best profiles with
three to five blocks equal the two-block supremum to nine digits; re-computed for this
correction (`experiments/coordinator_checks/slices/m2_check.py`, `m2_check_margin.py`;
harness XXI.6) with a linear programme over all laws on a grid of block densities, any
number of blocks, at nine `(κ, u, e)` — the optimum is a two-atom law, or a three-atom law
with zero budget and the value `−e`.)
(b) On the ray, `F` is convex and increasing in `ℓ ≥ 0` with `F′` onto `[0, ∞)`.  The shell at
`ℓ` has the value `F((ℓ − (e + F(ℓ))/u)₊)`, and `ℓ − (e + F(ℓ))/u` is largest, `(Ψ(u) − e)/u`, at `ℓ*`.
Since `F = Ψ*` and the maximiser `s = F′((Ψ(u)−e)/u)` is at most `F′(ℓ*) = u`, the value is
`max_{s≤u}[s(Ψ(u) − e)/u − Ψ(s)]`, the game form with `s = tu`; for `e < −F(ℓ*)` only shells with
`F(ℓ) ≥ −e` are feasible and, as long as there are any (`e ≥ −F(ℓ_max)`), both sides equal `−e`.
For `n`: the feasible exits of the shell `ℓ_μ`
are `{ℓ ≤ ℓ_μ : uℓ − F(ℓ) ≥ uℓ_μ − F(ℓ_μ) − X}`, smallest for `ℓ_μ = ℓ*`; the game form is the
Lagrangian of `min{F(ℓ) : F(ℓ) − uℓ + Ψ(u) − X ≤ 0}` with the multiplier `τ/(1−τ)`.
(c) `F′_{m,κ}(ℓ) = ½[logit(κ + ℓ/2m) − logit(κ − ℓ/(2(1−m)))]`: at the point of slope `s` the
two-by-two table (block, letter) has log odds ratio `2s`, and its mutual information is
`F(ℓ(s)) = sΨ′(s) − Ψ(s)`.  By Lemma 11.89, `sΨ′_{m,κ}(s) − Ψ_{m,κ}(s) ≤ K(s/2) = sΨ_c′(s) − Ψ_c(s)` with
`Ψ_c := ln cosh(·/2)`; so `D := Ψ_c − Ψ_{m,κ}` satisfies `(D(s)/s)′ = (sD′ − D)/s² ≥ 0`, hence
`D(tu) ≤ t·D(u)` for `0 < t ≤ 1`, which is the claim; equality forces uniform marginals,
`m = κ = ½`.  (In one formula: since `(Ψ(s)/s)′ = I(s)/s²` with `I(s)` the mutual information at
slope `s`, **the game function is an integral of the mutual information along the tilting
path, `F*(t) = tu·∫_{tu}^{u} I(s) s^{−2} ds`**, and the lemma bounds the integrand.)
*In one line* (Scientific Discovery Division, SCI-REV-0001 §4; the remark after Lemma 11.89):
`D″ = Ψ_c″ − Ψ″_{m,κ} ≥ 0` and `D(0) = D′(0) = 0`, so `D` is convex and `D(tu) ≤ t·D(u)` —
without the mutual information; and the gap `F*_c(t) − F*_{m,κ}(t) = t·D(u) − D(tu)` is
nondecreasing in `u`, its derivative being `t·[D′(u) − D′(tu)] ≥ 0`.  The suprema over `m` are
attained (the values are continuous in `m` and vanish at the ends for `e ≥ 0` and for `N`;
for `e < 0` the game forms tend to `−e` there, a value that the centre `m = κ` attains).  ∎

*Remark (a type class is a member of the class of §11.23, softly pinned)* **[P, given
Theorems 11.78–11.80].**  The uniform measure on a type class is the limit `M → ∞` of the
exchangeable known parts `φ_M(κ′) = M|κ′ − κ|`, and for `M > u + |logit κ|` nothing depends on
`M`: the rate function `I_M` is convex, `|I_M′| > u` away from `κ`, so `κ` is the only contact type
and `I_M ≥ u|· − κ|`; by Lemma 11.77(b) the exits may be taken of type `κ`, so `r_μ = r^κ_μ` for
profiles of type `κ`, and a profile of another type is dominated by its thinning `μ″` to
`κ` (`dist(μ″, μ) = |μ̄ − κ|`, `MI(μ″) ≤ MI(μ)`, and the budget grows by `I_M(μ̄) − u|μ̄ − κ| ≥ 0`).  Hence
`R_H = R^κ` and `N = N^κ` for a pinned type, and §11.23 applies to it as it stands: **the hinted
exponent of the flat-histogram instance of a pinned type is `R^κ`, the exponent of
non-adaptive algorithms is `N^κ = R^κ∘(S^κ)^{−1}`** (Theorem 11.80: `I_M` is convex), and Theorem
11.90 evaluates both in closed form and compares them with the cube.  For the uniform
measure on the type class itself (`p_t = 0` off the class) the same proofs apply; only the
standing assumption `p_t > 0` of §11.23 is not met.

**Corollary 11.91 (every known part that is a function of the type) [the inequalities: P,
coordinator; their reading as exponents: given Theorems 11.78, 11.79].**  Let `π` be
exchangeable as in §11.23, with *any* continuous `φ` — ferromagnetic or not, with a convex
rate function or not, with any number of phases — and let `λ` be any landscape.  Then for
every block profile `μ` of type `κ`, all `e ≥ −h(κ)` and all `X ≥ 0`:

    r_μ(e) ≤ r^κ_μ(e + (I−λ)(κ)) ≤ R^κ(e),        n_μ(X) ≤ n^κ_μ(X + (I−v)(κ)) ≤ N^κ(X),

hence

    R_λ(e) ≤ sup_κ R^κ(e + (I−λ)(κ)) ≤ R̂_c(e),      N(X) ≤ θ_na^{cube}(X),      R̄_H(e) ≤ R̂_c(e) = max_{0≤t≤1}[F*_c(t) − te]

for all real `e` and all `X ≥ 0` (the supremum runs over the types that have admissible
profiles, `e + (I−λ)(κ) ≥ −h(κ)`; `R̂_c = R_unif` for `−K(u/2) ≤ e ≤ ln cosh(u/2)`).

So, by Theorems 11.76, 11.78, 11.79: **the hinted exponent of every symmetric instance, the
lower bound for all algorithms that symmetric instances give, and the exponent of
non-adaptive algorithms never exceed the uniform cube's — whatever the interaction.**
*What this covers, and what it does not* (Scientific Discovery Division, SCI-REV-0001, M1;
the first version of the title, of (ii) below and of the summaries in the README, in §0
and in §10 said "no known part … is harder than the uniform cube" and "changes no
exponent" without restriction).  The theory has three exponents; covered are two — the
hinted one, for instances that are functions of the type, and the one of non-adaptive
algorithms.  **Not covered is the exponent `θ*` of adaptive algorithms without a hint**, the
one that is small on the cube, where it equals the hinted one (Theorems 11.54, 11.58).
For it and an interacting known part the proved bounds are `R_H ≤ θ* ≤ θ_na ≤ θ_na^{cube}`, and
`θ* ≤ R_unif` for ferromagnetic Curie–Weiss known parts (Proposition 11.81(c), given Theorem
11.64) and for a field (Theorem 11.64 with Proposition 11.65(b)); for every other
interaction "at most as hard as the cube" is Conjecture 11.94.  Example: at `u = 1` and
vanishing accuracy the cube has `θ* = 0.029139`, an antiferromagnet without a field
`θ* ∈ [0.029139, 0.110944]`.  Further: the accuracies are extensive, `ε = ε₁n`, nothing is said
at bounded accuracy; and "hardest instance" means among symmetric instances (O4 of
Conjecture 11.83).
(i) Proposition 11.81(a) holds for every `φ`, and its proof no longer uses Proposition
11.65(b); for a field (`βJ = 0`) this is a second proof that the uniform cube is the hardest
case.
(ii) **For a symmetric convex rate function — `B = 0` and `βJ ≤ 1`, every antiferromagnet
included — `R_H = R_unif` and `θ_na = θ_na^{cube}` exactly: an interaction without a field
and with one phase changes neither the hinted exponent of `H` nor the exponent of
non-adaptive algorithms.**  ("`≥`" is Proposition 11.81(a): the uniform cube's optimal profile has
an exit of minimal `MI` inside its own type class.  This closes item (δ) of §12 for these
two exponents.  The exponent of adaptive algorithms without a hint is then at least
`R_unif` — Theorems 11.76(b), 11.78(a), every `n` — equal to it for `0 ≤ βJ ≤ 1` by Proposition
11.81(c), and for an antiferromagnet only known to lie in `[R_unif, θ_na^{cube}]`.
SCI-REV-0001, M1: the first version said "changes no exponent".)
(iii) The same equality holds whenever the uniform cube's optimal profile keeps its
cheapest exit inside the type class `½` and `½` is a contact type — with two phases up to
the junction of Proposition 11.81(b), which is at `min{βJ*, βJ_w}` on the referee's grid: at
`βJ*` for `u = 1` and for `u ≤ 2`, earlier for large slopes at small or negative accuracies,
where a constant exit at a well — an exit that leaves the type class — becomes feasible
first (referee R10, M1; the first version of that proposition placed the junction at
`βJ*` for all slopes).
*Proof.*  Restricting the exits to `ν̄ = μ̄` shrinks the feasible sets of `r_μ` and `n_μ`, and on
them `u·dist + λ(κ) ≤ e + MI(μ) + I(κ)` is the constraint of `r^κ_μ` at the accuracy
`e + (I−λ)(κ) ≥ e`; feasibility of the two problems is the same condition (`λ` is
`u`-Lipschitz).  Then Theorem 11.90, part (a) with its repair at negative accuracies: on
`e ≥ −h(κ)`, `R^κ(e) ≥ −e` (the shell with `F = −e` of the centre `m = κ`), so
`r^κ_μ(e′) ≤ R^κ(e)` for `e′ = e + (I−λ)(κ)` also when `μ` is feasible at `e′` but not at `e` —
then `r^κ_μ(e′) ≤ MI(μ) < −e`; and `R^κ(e′) ≤ R̂_c(e′) ≤ R̂_c(e)`, `R̂_c` being nonincreasing.
(SCI-REV-0001, M2: negative accuracies are needed here — the non-adaptive half evaluates
`R̄_H^{−1}` near `e = −K(u/2)`, which is `−0.11` at `u = 1`.)  `R̄_H = max(R_H, −e)` and the game
form of `F*_c` is at
least `−e`.  For the non-adaptive exponent, `R̄_H ≤ R̂_c` pointwise gives
`θ + R̄_H^{−1}(θ) ≤ θ + R̂_c^{−1}(θ)` and Theorem 11.79(c) the bound.  ∎

*What the corollary does not say.*  The bound `sup_κR^κ(e + (I−λ)(κ))` ignores exits that change
the type, and these matter: for a field `p = 0.3` at `u = 1` it is `0.029139` (the type `½` is a
contact type) against the true `R^max(0) = 0.025034`; with two phases at `βJ = 1.5` it is
`0.029139` against `R_H(0) ≥ 0.0251012`.  The slices are an upper bound for the class, exact in
the symmetric cases (ii), (iii).

*Remark (more than two letters: the comparison fails)* **[coordinator; corrected at the
eleventh checkpoint and continued in Proposition 11.103].**  For an alphabet of `q ≥ 3`
letters with the Hamming envelope, and *with letters as labels*, the pair (letter of the
centre, letter of the configuration) at slope `s` is a *Potts pair*, `P(b, x) ∝ a_b c_x e^{s·1[b=x]}`,
and the game function of a centre on a composition class is again `tu·∫_{tu}^{u} I(s) s^{−2} ds`
**[P]**.  But uniform marginals do not maximise `I(s)`: to second order `I(s) ≈ s²(k−1)/(2k²)`
for the uniform law on `k` letters — largest for `k = 2` **[P]** — and on three letters,
numerically, the mutual information of a Potts pair never exceeds the larger of its
values for the uniform laws on two and on three letters, which cross at `s = 0.5194`
(harness XXI.5).  So **with three letters a known part that pins the composition onto two
of them, or a field that nearly removes a letter, makes certification harder than no
known part at small slopes** — at vanishing accuracy the uniform two-letter law beats the
uniform three-letter law exactly for `u < ln 2` (`0.007673` against `0.007425` at `u = 0.5`); the
two-letter law is not the hardest three-letter site law either, and laws near it lie on
both sides of it (Proposition 11.103(d), as corrected after the reviews SCI-REV-0001 §5 and
SCI-REV-0005 of the Scientific Discovery Division).  Corollary 11.91 and Proposition 11.65(b)
are statements about two letters.
*Correction.*  The first version of this remark (tenth checkpoint) also listed
"uniform `k`-ary cubes" for `k = 4` with the values of single dips on letters (`0.006552` at
`u = 0.5`, `0.028405` at `u = 1`) and offered "the hardest known part is a uniformly weighted
sub-alphabet" as the natural replacement.  Both were wrong beyond three letters and near
the threshold: from four letters on the Lipschitz polytope of a site has vertices that
are not distance functions (indicator functions of sets of letters), the uniform
four-letter site has the *two*-letter values `0.007673`, `0.029139` by grouping its letters
in pairs, and at `u = 1` the three-letter law `(0.05, 0.5, 0.45)` has a larger threshold than
every uniform law on a sub-alphabet (workstream W).  What is true is in Proposition
11.103(d), (e) (`DEAD_ENDS.md` D52).

**Theorem 11.92 (algorithms: reduction to slices; every `n`) [P; the deterministic core of
(b) **[V]**: `sum_mem_bracket`, `argmax_deficit_le`, `deficit_ge`; coordinator].**  Let `π` be exchangeable,
`A_t(ψ) := |T_t|^{−1}Σ_{x∈T_t}e^{−ψ(x)}`, so that `A = Σ_tp_tA_t`, and `d_t := ln[max_jp_jA_j/(p_tA_t)]` the
*deficit* of the type class `t`.
(a) For `ψ ∈ L_u`, `t ↦ ln A_t(ψ)` is `u`-Lipschitz (a uniform point of `T_{t+1}` with a uniformly
chosen one switched off is uniform on `T_t`).  Hence `d_t ≥ J_t − V_n(t)`, with equality for all
`t` at the flat-histogram instance.
(b) *Optimistic refinement.*  Let a bracket procedure be given for every type class: on
request `(t, l)` it returns `L ≤ A_t ≤ U` with `U ≤ e^{x_l}L` except with probability `δ′`, for a
ladder `x₀ > x₁ > … > x_m` (one evaluation gives `x₀ = 4u·min(t, n−t)`).  Keep the intersection
of the brackets of each class; repeat: let `k` maximise `p_tU_t`; if the bracket of `k` has
the width `x_m`, stop and return `[max_tp_tL_t, (n+1)·p_kU_k]`; otherwise refine `k` by one
rung.  Outside a failure probability `(n+1)mδ′`: the output is a valid bracket for `A` of
width at most `x_m + ln(n+1)`, and **a type class is refined from the width `x_{l−1}` only if
`d_t ≤ x_{l−1}`** — when it is the maximiser, `max_jp_jA_j ≤ p_tU_t ≤ e^{x_{l−1}}p_tA_t`.  The cost is at
most `n + 1 + Σ_tΣ_{l : x_{l−1} ≥ d_t}C_t(x_l)`, the `n + 1` being the initial brackets, one
evaluation per class.  (SCI-REV-0001, m7: the first version omitted them.  Also: the failure
probability presupposes that the initial brackets are deterministic — they are — and that
each request `(t, l)` is answered once, with randomness of its own; and the Lean statement
`sum_mem_bracket` has the lower end `p_kL_k` where the procedure returns `max_tp_tL_t` — both are
valid, `A ≥ p_tA_t ≥ p_tL_t` for every `t` (`lower_end_any` **[V]**, the reviewer's lemma, added to
`SliceRefinement.lean`).)
(c) *Exponents.*  If the type class of density `κ` has bracket procedures with the exponent
function `τ_κ` (uniformly in `κ` on compact subsets of `(0,1)`), then adaptive algorithms without
a hint have, for the class `L_u` and the known part `π`, an exponent at most
`sup_κ τ_κ(max(ε₁, (I−v)(κ))⁻)`, and at a symmetric instance with landscape `λ` at most
`sup_κ τ_κ(max(ε₁, (I−λ)(κ))⁻)`: a type class far below the maximum is only looked at coarsely
(and the classes with `min(κ, 1−κ) ≤ ε₁/4u` need one evaluation each).  *What (c) yields today*
(SCI-REV-0001, m8): the only bracket procedures available for a type class are fixed
samples, `τ_κ = N^κ` (given Theorems 11.79, 11.80), and with them the bound is
`sup_κ N^κ(max(ε₁, (I−v)(κ)))` — at least `N(ε₁)` (Corollary 11.91), and equal to `θ_na^{cube}(ε₁)`
whenever `½` is a contact type: nothing beyond Theorem 11.79(c).  A new exponent comes out
of (c) only with adaptive procedures on a type class, i.e. with Conjecture 11.94(iii).
*Proof.*  (a) Double counting over the edges between `T_t` and `T_{t+1}`; then
`max_jp_jA_j ≥ p_jA_te^{−u|j−t|}` for all `j`.  (b) `A ≥ p_kA_k ≥ p_kL_k` and
`A ≤ (n+1)max_tp_tA_t ≤ (n+1)p_kU_k`; the rest is in the statement.  (c) A ladder with steps
`η` in the rate; `η → 0`.  ∎

**Lemma 11.93 (random partitions of a slice; every `n`) [P; coordinator].**  Let `O` be a
uniformly random set of `n_o` coordinates, `T_k(O; j) := {x ∈ T_k : |x ∩ O| = j}` (the product of
the type class `j` of the outer block and the type class `k − j` of the inner block),
`A_{k;j}(O)` the mean of `e^{−ψ}` over it, and `H(j) := C(n_o, j)C(n − n_o, k − j)/C(n, k)`.
(i) For every `O`: `A_k = Σ_jH(j)A_{k;j}(O)`, and the logarithm of the inner-slice mean,
`a ↦ ln W_j(a)`, is `u`-Lipschitz on the outer slice.
(ii) `E_O A_{k;j}(O) = A_k` for every `j` (a uniform point of `T_k(O; j)` for a uniform `O` is uniform
on `T_k`).  Hence for every set `S` of outer types and every `ψ`, with probability at least
`1 − δ″` over `O`: `Σ_{j∉S}H(j)A_{k;j}(O) ≤ (H(Sᶜ)/δ″)·A_k`; with `S = {|j − n_ok/n| ≤ √(n ln(4/δ″)/2)}` the
other products carry at most half of `A_k`.
So with a random partition only the polynomially many type pairs within `O(√(n ln n))` of
the proportional split matter, and a slice splits into slices *of the same density*.  ∎
*Remark (not part of the lemma and not proved here).*  With a fixed partition this is
false: the centre of the hard instance can have any outer type — all its ones inside `O`,
say — and all pairs of block densities in a window would have to be treated (SCI-REV-0001,
m10: in the first version this sentence stood inside the lemma, before the `∎`).

**Conjecture 11.94 (a slice behaves like a cube; the adaptive exponent of a function-of-type
known part) [C].**  For the uniform measure on the type class of density `κ`:
(i) the hinted exponent of the zero residual is `R^κ` (lower bound: the classes of Theorem
11.78(a), every `n`; upper bound: Theorem 11.78(b) inside one type class);
(ii) the exponent of non-adaptive algorithms is `N^κ = R^κ∘(S^κ)^{−1}` (`sup_mF*_{m,κ}` is a game
function, so Theorem 11.66 **[V]** gives the pair identity);
— *(i) and (ii) are not conjectures for a softly pinned type: there they are Theorems
11.78–11.80 (refereed), by the remark after Theorem 11.90; they are listed here because they are
what (iii) builds on;* —
(iii) **the exponent of adaptive algorithms without a hint is `R^κ`**: Algorithm 2L⁺ of
§§11.18–11.19 with every split drawn at random (Lemma 11.93), the sum over the typical type
pairs taken by Theorem 11.92(b), and the tail lemma of the cube (Harper) replaced by the
isoperimetric statement of (i); the level recursion is that of §11.19 with `(N^κ, R^κ)` in
place of `(θ_na, θ_hint)`, and its convergence is `HintShape.exactRec_tendsto` **[V]**.
*Consequence, if (iii) holds:* for every function-of-type known part the exponent `θ*` of
adaptive algorithms without a hint satisfies

    R_H(ε₁)  ≤  θ*(ε₁)  ≤  sup_κ R^κ( max(ε₁, (I−v)(κ)) )  ≤  R_unif(ε₁),

with equality throughout in the cases (ii), (iii) of Corollary 11.91 — in particular
**`θ* = R_unif` for every interaction without a field up to the junction**.  For
ferromagnets this much is Proposition 11.81(c), which is proved (given Theorem 11.64)
through mixtures of fields; (iii) would give it for every interaction, antiferromagnets
included.  What a proof of (iii) would have to supply — none of it is written, so whether
an idea is missing as well is not known (SCI-REV-0001, m9; the first version said
"written work, not an idea") — is the proof of Theorem 11.56 gone through with product
slices in place of product cubes (expected: the three facts (F1)–(F3) of Theorem 11.52
hold verbatim; the
closure test needs the tail bound in the form of an exponent with an `o(n)` slack; a failed
random split underestimates a fibre mean, with probability `1/poly`, independently for
each outer point).  **The exact adaptive exponent between `R_H` and the slice bound, when
they differ (a field; two phases beyond the junction), remains open**: it needs exits that
change the type, i.e. information across type classes, which the reduction of Theorem
11.92 discards.  Nesting by the type of the inner block keeps it at the top level only
(given the type of the inner block the outer block carries an exchangeable law with the
rate function `I(φτ_o + (1−φ)τ_i) + h(κ) − φh(τ_o) − (1−φ)h(τ_i)`, all levels below are slices), and
leads to a recursion over rate functions that we could not close.

*Reading.*  For a system with one order parameter and a residual of bounded sensitivity
(an idealised class; the density of states of the known part is assumed known), **for
fixed samples and for algorithms that are told an instance that is a function of the
order parameter**: the whole difficulty of certifying a free energy can be accounted for
one value of the order parameter at a time, each value is at most as hard as the
unconstrained system at half filling, and the known interaction enters only through
*which* values have to be looked at closely — never through a harder geometry.  For
adaptive algorithms without a hint this is Conjecture 11.94(iii); proved there is only
the comparison with the uniform cube for ferromagnets and for fields (Proposition
11.81(c), Theorem 11.64).  (SCI-REV-0001, M1, m9: the first version had no restriction.)

*Harness.*  XXI.1 (Lemma 11.89 on random tables and every step of its proof), XXI.2
(closed forms; binary centres against profiles with three to five blocks, the inner
problem solved by clipping without duality — for the hinted function at accuracies
`e ≥ 0` only, not at `e < 0` and not for the non-adaptive function: SCI-REV-0001, m12),
XXI.3 (domination; the numbers above;
Curie–Weiss known parts with two phases, an antiferromagnet and a field against their
slices and the cube), XXI.4 (Theorem 11.92 and Lemma 11.93 by exact enumeration on cubes of
dimension 8 and 9), XXI.5 (the integral form of Theorem 11.90(c) and the remark on more than
two letters), and — added with the review — XXI.6 (Theorem 11.90(a) at negative accuracies:
feasibility, the value `−e` of the profiles with zero budget, mixtures whose two-point
components are infeasible, random profiles with three to five blocks against the
two-block supremum); 28 mutations, all detected.  An earlier grid computation of the coordinator's had
`0.0281`, `0.0247`, `0.0189` for the slices `0.4`, `0.3`, `0.2` — the inner minimum on a grid is
biased upward and the outer maximum selects the bias (D51; the lesson of D49, item 7, a
second time).


### 11.26 Heteropolymer product landscapes: several site types, any alphabets, asymmetric envelopes — and a dictionary with channel coding

§§11.16–11.21 are about two-state sites of one kind.  The landscapes the certificate
formats were built for have sites of several types along a fixed sequence, more than two
states per site, single-site known parts and site envelopes that need not be symmetric;
for these the theory without a hint existed only as a sketch (§11.20, remark (4);
workstream F, Proposition F12).  This section turns the sketch into theorems, finds that
the single-site ingredient is a classical object of information theory — and records
where intuition from two letters fails.

*Status.*  Workstream W (`docs/workstreams/W_REPORT.md`; scripts and outputs
`experiments/workstreams/W/`).  **Paper proofs by one author; Theorems 11.99 and 11.101
reviewed by the Scientific Discovery Division, with independent replication
(SCI-REV-0005; its detailed report is `docs/science/workstreams/R5_REPORT.md` on the branch
`research/scientific-translation`): no critical finding; Theorem 11.99 proved; Theorem
11.101(a) proved; Theorem 11.101(b) proved with two gaps in the written proof, both
closed — the isoperimetric statement in the form the nested algorithm needs was stated
in the workstream's report only (M1; now Theorem 11.97(c)), and the level induction used
an undefined notion and an unproved uniformity over compositions (M2; now in Theorem
11.101).  No exponent changed.  The twelve minor findings are corrected where they are
marked below, or in the errata at the head of the workstream's report.  Nothing of the
nested algorithm has been simulated**; the review took the count of evaluations of
Theorem 11.52 and Theorem 11.78(b) as given, and of Propositions 11.100, 11.102, 11.103 it
replicated numbers and re-proved the crossing identity of 11.103(e), no more.  The upper
bounds are proofs *by transfer* of Theorems 11.78(b) (refereed "proved" by R10,
`docs/reviews/R10_referee_report.md`, there Theorem T3(b); our first version cited that
report before it was in the tree — SCI-REV-0005, m10),
11.52, 11.54 and 11.64 (refereed for two states), with every changed step written out in
the workstream's report and, since the review, the steps that carry the transfer also
here.  The coordinator re-derived Theorem 11.99 and the dictionary, Lemma W1.0,
Propositions 11.100(a) and the lower bound of Theorem 11.101; read Lemma 11.96 and
Theorems 11.97, 11.98, 11.101; **re-computed with an own implementation written from the
statements** the vertices, the Rényi form against the linear-programming value of the
game and against a blind search, every number of the table below, the non-additivity, the
pair identity and both negative results (`experiments/coordinator_checks/sites_W/`; largest
deviation from the report `5·10⁻⁷`, its rounding); and **refuted one conjecture of the
report** by scanning small slopes (Proposition 11.103(d)).  After the review we
re-derived Theorem 11.97(c), the uniformity argument of Theorem 11.101, the ceiling and
the comparison with the cube of Proposition 11.103, and re-computed with own code and
with the harness helpers the numbers of the corrections (the slope jump of Proposition
11.100, the data points and ratios of Proposition 11.103(d), (f), the Lipschitz bound of
Theorem 11.101, the two numbers of the conventions); the reviewer's own replication
statistics are quoted as reported.  Machine-checked are *the general inequalities
behind* the every-`n` lower bounds (`lowDens_shift`, `truncate_admissible`,
`group_nonadaptive_queries_ge`, `group_queries_ge` of `GroupSampling.lean`; Theorems 11.22 and
11.27(a), (b)) and the two elementary steps of Theorem 11.99
(`proofs/Frontiers/RenyiCentre.lean`); the product step for several site types
(independent vertex labels, Markov's inequality, the identification with `nΣ_jλ_jF_j`) and
the evaluation for truncated cones are paper steps, as the headers of Theorems 11.95
and 11.101 say (our first version of this paragraph said "machine-checked: the every-`n`
lower bounds" — SCI-REV-0005, m3).  Not re-run by the
coordinator: the exact sums over joint types and the brute-force runs of the report.

**Setting.**  Sites `i = 1..n` with types `τ(i) ∈ {1..m}` (a fixed sequence), `n_j` sites of type
`j`, `λ_j = n_j/n`.  Site type `j`: alphabet `𝒮_j` with `q_j ≥ 2` letters, site law `π_j` of full
support, site envelope `d_j ≥ 0` with zero diagonal and the triangle inequality, **not
necessarily symmetric**.  `X = Π_i𝒮_{τ(i)}`, `π = ⊗_iπ_{τ(i)}`, `d(x,y) = Σ_id_{τ(i)}(x_i,y_i)`, the class
`𝒞 = {ψ : ψ(x) − ψ(y) ≤ d(x,y)}`, `A(ψ) = E_πe^{−ψ}`, accuracy `ε₁n`, cost = evaluations.
*Orientation:* in `d(x,y)` the first argument is the point at which `ψ` may be larger; the
slack of an instance is `s₀(y,x) = d(y,x) − ψ₀(y) + ψ₀(x)` (`y` outside a dip, `x` inside), and
transposing it is wrong (2 582 violations of the tail lemma in 13 328 brute-force cases).
`L_j := {γ : γ(a) − γ(b) ≤ d_j(a,b)}` is the *Lipschitz polytope* of the site (compact modulo
constants), `𝒱_j` its vertices, `π_γ ∝ π_je^{−γ}` the Gibbs law of `γ`, `ψ_γ(x) = Σ_iγ_{τ(i)}(x_i)` the
additive instances.  A *joint type* is the tuple of empirical laws of `x` on the sites of
each type; `W_j(P′,P) = max_{φ∈𝒱_j}[E_{P′}φ − E_Pφ]` is the (oriented) transport cost.

**Theorem 11.95 (what the symmetry of the sequence gives; every `n`) [the truncation, the
lower bound of (a) and (b): **[V]** (`lowDens_shift`, `truncate_admissible`,
`group_nonadaptive_queries_ge`, `group_queries_ge`); the rest P; workstream W, Theorem W1].**
The group `Γ = Π_jS_{n_j}` permutes sites of the same type; its orbits are the joint-type
classes, `N_orb = Π_jC(n_j + q_j − 1, q_j − 1)` of them.  The quotient envelope is *exactly* the
transport cost, `min{d(x,y) : x ∈ T_P, y ∈ T_{P′}} = nΣ_jλ_jW_j(P_j,P′_j)` (transportation polytopes
with integer marginals have integer vertices).  Theorem 11.76 (a)–(d) holds with joint
types for types and `N_orb` for `n + 1`: the **joint-type-stratified sample** is optimal among
non-adaptive algorithms up to `8N_orb ln(2N_orb/δ)/(1−2δ)` in the cost and `ln(4/δ)` in the
accuracy; every algorithm needs `(1−2δ)/maxdens(D)` evaluations at an invariant instance;
the flat-histogram instance `ψ_H = −V_n(P_x)`, `V_n(P) = min_{P′}[J_{P′} + δ(P′,P)]`, is the hardest
invariant instance up to `N_orb + 1`; the stratified two-sample bracket is
instance-optimal at invariant instances.  (The exact orbit-wise quantiles are admissible
without the regularisation of the Lean file; `V_n` is admissible for the *transposed*
quotient envelope.)

**Lemma 11.96 (inherently typical subsets with site types) [P; workstream W, Lemma T′].**
Lemma T of §11.20 holds for a product measure `⊗_iρ_{τ(i)}` on `X` with the site type adjoined to
the label: label sets of size `≤ (M+1)^{q_j}`, a subset of relative measure
`≥ Π_j(n_j+1)^{−q_j(M+1)^{q_j}}` of constant joint type of (site type, label, letter), and the
chain-rule defect `I(X_I; V | U_I, T_I) ≤ q_max/M + Σ_jq_j(M+1)^{q_j}ln(n+1)/n`.
The `ρ_j` need not have full support: the alphabet of type `j` is restricted to the support
of `ρ_j`.  That is how the lemma is applied in Theorem 11.97 — to the joint type of a piece,
which may miss letters; the workstream states it for full support (SCI-REV-0005, m6).

**Theorem 11.97 (the single-letter theorem for instances that are functions of the joint
type) [P; (a) for every `n`; (b), (c) by the method of types, a transfer of Theorem 11.78(b);
workstream W, Theorem W2; (c) re-derived by the reviewer of SCI-REV-0005 and by us].**
The known part may be any `n·φ(P_x)`, `φ` continuous (a product
measure, or a mean-field heteropolymer); `I = φ − H − min`, `v(P) = min_{P′}[I(P′) + W(P′,P)]`.  For
a landscape `λ` (admissible for the transposed transport cost, `λ ≤ I`, touching) and
*labelled profiles* `μ` — joint laws of (site type `T`, label `U`, letter `X`) —

    R_λ(e) = sup_μ min{ I(X′; U | T) : E d_T(X′, X) + λ(P_{X′|T}) ≤ e + I(X; U | T) + I(P_{X|T}) }

is (a) a lower bound for the exponent of every algorithm at the instance `−nλ(P_x)`, for
every `n` (explicit classes; `maxdens ≤ (n+1)^{c_μ}e^{−nV}`), and (b) its hinted exponent
(isoperimetry for the orbit-uniform measure, `ω_n → 0` uniformly in the composition).
Three steps of the proof of Theorem 11.78(b) change: Lemma 11.96 for Lemma T, applied
with the product measure `⊗_iP_{τ(i)}` that is uniform on the joint-type class; optimal
couplings as kernels and Hoeffding's inequality for the transport cost and all letter
counts; `N_orb` for `n + 1`.  The error term is worse than for two letters
(`n^{−1/(2q_max+2)}` from the proof).
(c) *Product measure, reference `H`: the form the nested algorithm needs* **[P; workstream
W, Theorem W2(c); re-derived by the reviewer of SCI-REV-0005 and by us].**  Let `π` be the
product measure, `ψ_H(x) = −n·v(P_x)` the flat-histogram instance, `μ_H ∝ πe^{−ψ_H}`,
`s_H(y,x) = d(y,x) − ψ_H(y) + ψ_H(x)`, `Φ_H⁺(D) = Σ_{x∈D}μ_H(x)·exp(min_{y∉D}s_H(y,x))`, and `R̂` the
function of Theorem 11.98 for the composition of the chain.  There are numbers `ω_n → 0`
that depend on `n` and on `(m, q_max, D_max, π_min)` only — `D_max = max_{j,a,b}d_j(a,b)`,
`π_min = min_{j,a}π_j(a)`; **not on the composition** `(n_j/n)_j` — such that for every chain of `n`
sites of these types, every real `e` and every `D ⊊ X`

    Φ_H⁺(D) ≥ e^{ne}      ⟹      μ_H(D) ≥ exp( −n·[ R̂(e − ω_n) + ω_n ] );

equivalently, for `θ > ω_n`: `μ_H(D) ≤ e^{−nθ}` implies `n^{−1}·ln Φ_H⁺(D) ≤ R̂^{−1}(θ − ω_n) + ω_n`
— the tail function of `H` has the exponent `R̂^{−1}`, uniformly over compositions.  Both
upper bounds of this section rest on this statement (Theorems 11.98(d), 11.101(b)), and
on its uniformity, because the blocks of the nested algorithm have compositions that
are only asymptotically `λ`.  It differs from (b) in the measure — `μ_H` in place of the
largest orbit density — and in the function — the evaluated `R̂` in place of a supremum.
*Our first version had (a) and (b) only and referred, in Theorem 11.101, to "Theorem
11.97 in the form for `μ_H`", which was stated and proved in the workstream's report
alone: Scientific Discovery Division, SCI-REV-0005, finding M1.*
*Proof of (c)* — the steps of (b) for `λ = v`; what differs is marked ▶.  With
`Z_H = E_πe^{−ψ_H} ∈ [1, N_orb]`: `Φ_H⁺(D) = Z_H^{−1}Σ_{x∈D}π(x)e^{nB(x)}`,
`B(x) = min_{y∉D}[v(P_y) + d(y,x)/n] ∈ [0, 2D_max]`.  Fix the piece `C ⊂ D` of constant joint
type `P` and constant `B` (rounded to a multiple of `1/n`) with the largest `π(C)e^{nB}`; with
`α_C` the density exponent of `C` in its class, `e ≤ B − I(P) − α_C + o(1)`, and every `y` with
`v(P_y) + d(y,x)/n < B` for some `x ∈ C` lies in `D`.  Lemma 11.96 for `ρ = ⊗_iP_{τ(i)}` gives
`C̃ ⊂ C` and a labelled profile `μ` with letter marginal `P` and `I(X;U|T) ≤ α_C + o(1)`.  Let
`κ = n^{−1/4}`.  If `B < v(P) + 3κ` (shallow piece), `μ_H(D) ≥ μ_H(C̃) = π(C̃)e^{nv(P)}/Z_H` gives
the exponent `−e + o(1)`, and `R̂(e) ≥ −e`.  Otherwise:
▶ *Evaluation.*  For every labelled profile `μ` with letter marginal `μ̄` and every
`B′ ≥ v(μ̄)`, the least `I(X′;U|T)` over kernels with `E d_T(X′,X) + v(P_{X′|T}) ≤ B′` is at most
`R̂(B′ − α(μ))`, `α(μ) = I(X;U|T) + I(μ̄)`.  Indeed, by Sion's theorem (twice, as in Theorem
11.98(a)) it is the supremum over slopes `τ ≥ 0` and additive instances `γ` of the
Lagrangian of Theorem 11.98(b) minus `τ(B′ − α(μ))`; for `τ ≤ 1` the Lagrangian is at most
`F*(τ)`, and for `τ ≥ 1` the kernel that changes nothing bounds the difference by `α(μ) − B′`;
both bounds are at most `R̂(B′ − α(μ))`.  Take `B′ = B − 2κ`.
▶ *Window step.*  If the exit type `P′ = P_{X′|T}` is not in the window `{v = I}`, let `P″`
minimise `I(P″) + W(P″,P′)` and pass `X′` through an optimal coupling of `P″` and `P′` (a kernel
that depends on the site type and the letter only).  Then `I(P″) ≤ v(P″)`, so `P″` is in the
window and `v(P″) = v(P′) − W(P″,P′)`; the transport cost grows by at most `W(P″,P′)` (triangle
inequality, in this order) and the mutual information does not grow.  So the exit type
`Q` may be taken in the window, where every letter has probability at least `π_min·e^{−D_max}`.
With `κ₁ = κ/((2 + m·q_max)·max(D_max, 1))`, Hoeffding's inequality — the cost within `nκ₁D_max`
and each of the at most `m·q_max` letter counts within `nκ₁` of its mean, outside probability
`p_n = 2(1 + m·q_max)e^{−2nκ₁²}` — puts the random exit `X′ⁿ` into `D` and into the set `G` of points
whose letter counts are within `nκ₂` of those of `Q`, `κ₂ = κ/(2 + m·q_max)`; the chain rule,
conditional on the site type, gives `n^{−1}D(P_{X′ⁿ}‖Q^⊗) ≤ I(X′;U|T) + η_{M,n}` with the defect
`η_{M,n}` of Lemma 11.96.
▶ *The measure `μ_H`.*  `π(y) = e^{−n[H(P_y) + I(P_y)]}` and `Q^⊗(y) ≤ e^{−nH(P_y)}` give
`μ_H(y) ≥ Q^⊗(y)·e^{−n(I − v)(P_y)}/N_orb`, and `I − v` is small near the window, uniformly in the
composition: `(I − v)(P) = Σ_jλ_j·min_{γ∈L_j}KL(P_j‖π_γ) ≤ Σ_jλ_j·χ²(P_j‖Q_j)` for `Q` in the
window, so on `G`, `(I − v)(P_y) ≤ ω′ := m·κ₂·[q_max·e^{D_max}/π_min + ln(1/π_min)]` (a site type
with `λ_j < κ₂` contributes at most `λ_j·ln(1/π_min)`).  Data processing for the event `D ∩ G`
gives `−n^{−1}ln μ_H(D) ≤ [I(X′;U|T) + η_{M,n} + ln 2/n]/(1 − p_n) + ω′ + n^{−1}ln N_orb`, and
`I(X′;U|T)` is at most `R̂(e − 2κ − o(1))` and at most `ln q_max`.  ∎
*The error term.*  With `M = ⌈n^{1/(2q_max+2)}⌉` in Lemma 11.96 the proof gives
`ω_n ≤ q_max·n^{−1/(2q_max+2)} + c·n^{−1/4}` for `n ≥ n₀`, with `c` and `n₀` depending on
`(m, q_max, D_max, π_min)` (below `n₀` the statement is trivial with `ω_n = D_max`): the leading
term is the rounding in Lemma 11.96 and involves `q_max` only; `m`, `D_max` and `π_min` enter
through `ω′`, `p_n` and `ln N_orb ≤ m(q_max − 1)·ln(n+1)`.  (The workstream bounds `I − v` by uniform
continuity, which gives no rate; the `χ²` bound is ours.  Two constants of the
workstream's proof are corrected in the errata of its report: SCI-REV-0005, m5, m6.)
The true size of `ω_n` is not known: on the workstream's test families, `n ≤ 72`, the least
admissible `ω` is at most `0.42·ln n/n`.

**Theorem 11.98 (product known parts: evaluation) [P; workstream W, Theorem W3(a), (b),
(d), (e)].**  For `γ ∈ ΠL_j` and `t ≥ 0` let `F_j(γ,t) := −ln val(K)`, `K(a,φ) = (π_φ(a)/π_γ(a))^t` the game
in which the sampler mixes letters and the adversary mixes vertices `φ ∈ 𝒱_j`;
`F*_j(t) := max_γF_j(γ,t)`, `F*(t) := Σ_jλ_jF*_j(t)`, `R̂(e) := max_{0≤t≤1}[F*(t) − te]`.
(a) *The flat-histogram instance is exactly as hard as the hardest additive instance*
(`v = max_γv_γ`; Sion's theorem twice).
(b) *Vertex labels suffice, and the site types share one slope:* for every additive
instance and `0 ≤ τ ≤ 1` the supremum over labelled profiles of the Lagrangian is
`Σ_jλ_jF_j(γ_j,τ)`, attained by labels that are vertices of `L_j` (at most `q_j` per type) with
the Gibbs law of the vertex as letter law.  Hence `R_H = R̂` on `e ≥ 0`, and
**`F*(t) = Σ_jλ_jF*_j(t)` with one common `t`.**  (The problem separates over site types
because `MI(ν) = min_QΣKL(ν_{ju}‖Q_j)`; then Kantorovich duality, Sion, the Gibbs variational
principle — the terms `τKL(μ_{ju}‖π_j)` cancel — and `−ln Σ_aQ(a)(π_φ(a)/π_γ(a))^τ` has no interior
local maximum on a face of `L_j` for `τ ≤ 1`.)
(c) `F*` *is a game function* with the sharp constants `E = Σ_jλ_jE_j` and `a = Σ_jλ_ja_j`, so
Theorem 11.66 **[V]** applies: `R̂` is convex with slopes in `[−1, 0]`, `(θ_na, R̂)` with
`θ_na := R̂∘S^{−1}`, `S(e) = e + R̂(e)`, is a pair (`GameFunction.pair`), and the level recursion
reaches `R̂`: started at `θ_na` it converges (`GameFunction.exactRec_tendsto`); started at any
bounded family — complete enumeration, the start of Theorem 11.101 — it comes within
every `η > 0` of `R̂` on `(0, E)` (`iterates_lt_hint_add` with this pair; our first version
cited Theorem 11.66 for both starts: SCI-REV-0005, m7).
(d) *Non-adaptive algorithms:* their exponent is `θ_na(ε₁)`, attained by the
joint-type-stratified sample; the lower bound holds for every `n` (generalised cones
`Σ_iφ_i(x_i)` with vertex labels, truncated at the orbit-wise quantiles — the argument of
Theorem 11.79(a); no unimodality is needed); the matching upper bound is asymptotic
(`n → ∞` along compositions tending to `λ`) and rests on Theorem 11.97(c), with the
uniformity written out in Theorem 11.101.

**Theorem 11.99 (the site function is a Rényi capacity; a dictionary with channel coding)
[P; the two elementary steps of the proof **[V]**: `exists_ratio_le`, `eq_of_forall_ratio_ge`,
`softmin_admissible`; workstream W, Theorem W3(c), Remark W3.1; re-derived by the coordinator;
reviewed (SCI-REV-0005): proved — re-derived there, and confirmed by three numerically
independent routes on 56 pairs of a site and a slope to `10⁻¹²`].**  For a site
`(π_j, d_j)` let the *vertex channel* send a vertex `φ ∈ 𝒱_j` to its Gibbs law `π_φ`.  For `0 < t < 1`

    F*_j(t) = max_{M∈Δ(𝒱_j)} −t·ln Σ_a ( Σ_φ M(φ)π_φ(a)^t )^{1/t} = min_Q max_φ (1−t)·D_t(π_φ‖Q) = (1−t)·C_t ,

`C_t` the Rényi capacity (= Rényi radius) of order `t` of the vertex channel; **the hardest
additive instance at slope `t` is the one whose Gibbs law is the Rényi centre**,
`π_{γ*} ∝ (Σ_φM*(φ)π_φ^t)^{1/t}`; `a_j = lim_{t↑1}F*_j(t)/(1−t)` is the Shannon capacity and
`E_j = lim_{t↓0}F*_j(t)/t = min_Q max_φ KL(Q‖π_φ)`.  With Gallager's function *maximised
over the input law of every site type separately, at a common `ρ`*,
`E_0(ρ) = Σ_jλ_j max_{M_j}E_0^{(j)}(ρ, M_j) = ρ·Σ_jλ_jC_{1/(1+ρ)}(𝒲_j)`,
`E_0^{(j)}(ρ, M) = −ln Σ_a(Σ_φM(φ)π_φ(a)^{1/(1+ρ)})^{1+ρ}`, and the sphere-packing exponent
`E_sp(θ) = sup_{ρ≥0}[E_0(ρ) − ρθ]`:

    F*(t) = t·E_0((1−t)/t),     R̂(e) = sup_{ρ≥0}(E_0(ρ) − e)/(1+ρ),     θ_na = E_sp^{−1},     E = E_sp(0⁺),     a = capacity.

**With a budget of `e^{nθ}` evaluations a fixed sample certifies the accuracy rate `E_sp(θ)`,
for `0 < θ < a`; an adaptive algorithm, or one with a hint, certifies `E_sp(θ) − θ`, for
`0 < θ < h`** (the shear law of §11.21) — asymptotically, at the exponential scale and at
extensive accuracy, in the worst case over the class; with a hint it is a statement
about the hardest instance.  `h = R̂(0)` is the fixed point `E_sp(h) = h`; for `h ≤ θ < a` the
expression `E_sp(θ) − θ` is `≤ 0` (`−0.008` at `θ = 0.3a` on the cube with `u = 1`), a fixed sample
still certifies the extensive rate `E_sp(θ)` and an adaptive algorithm reaches every
extensive accuracy.  (Our first version gave neither the ranges nor the mode, and wrote
`max_ρ` for the supremum, which for `e ≥ E` is a limit: Scientific Discovery Division,
SCI-REV-0005, m1.)  "One common slope" is the rule for
parallel channels (`E_0` is additive); the uniform cube is the binary symmetric channel
with crossover `p_u = 1/(1 + e^u)`: `a = ln 2 − h(p_u)`, `E = ln cosh(u/2)`, `E_sp(θ) = KL(ρ‖p_u)` at
`KL(ρ‖½) = θ` — the formulas of §11.16.
*Proof of the first identity.*  By the minimax theorem
`F_j(γ,t) = max_M min_a t·ln(π_γ(a)/m_M(a))`, `m_M := (Σ_φMπ_φ^t)^{1/t}`.  For a probability vector `P`
and a positive vector `m`, `min_a ln(P(a)/m(a)) ≤ −ln Σ_am(a)` with equality iff `P ∝ m` (if
`P ≥ c·m` then `1 ≥ cΣm`).  So `F_j(γ,t) ≤ max_M[−t ln Σm_M]`, with equality iff `π_γ ∝ m_{M*}`, and that
instance is in the class: `γ*(a) = −t^{−1}ln Σ_φM(φ)e^{−tφ̃(a)}` and `L_j` is closed under soft minima.
`−t ln Σ_am_M(a)` is `(1−t)` times Sibson's information of order `t`, whose maximum over `M` is
the Rényi radius (Csiszár).  ∎
*Why the sphere-packing exponent appears.*  The Gibbs law of a generalised cone with
label sequence `φ⃗` is the output law of the vertex channel for the input `φ⃗`; a sample of
`e^{nθ}` points per joint type sees exactly the outputs whose empirical mutual information
with `φ⃗` is at most `θ`; truncating the cone removes the rest — which carries almost all of
the Gibbs mass — and what remains has Gibbs mass `exp(−n·min{D(V‖W|M) : I(M,V) ≤ θ})`: the
Csiszár–Körner form of `E_sp`, after the maximum over the label law `M`.  (Our first version
attributed this mass to "the rest": SCI-REV-0005, m2; found independently by the same
division's workstream A1, SCI-RES-0003.)  A fixed sample has to
*cover* the outputs of a channel it does not know the input of.
*Conventions for Theorem 11.99* (so that nobody inserts the wrong function; Scientific
Discovery Division, SCI-REV-0005, §2 and m4; the identities re-derived and the numbers
re-computed by us).  (1) `D_t(P‖Q) = (t−1)^{−1}·ln Σ_aP(a)^tQ(a)^{1−t}`, natural logarithms,
`0 < t < 1`.  (2) The programme `max_M −t·ln Σ_a(Σ_φM(φ)π_φ(a)^t)^{1/t}` is `(1−t)` times *Sibson's*
information of order `t` of the vertex channel, maximised over the input law; its
maximum is the Rényi radius `min_Q max_φ D_t(π_φ‖Q)`, which is also the maximum of
*Augustin's* information `I^A_t(M) = min_QΣ_φM(φ)D_t(π_φ‖Q)`.  At a fixed label law `M` the two
differ — Sibson `≤` Augustin for `t < 1`, by Jensen's inequality — and this matters in one
place: the exponent of a *given* generalised cone with label law `M` (Theorem 11.98(d)) is
the Csiszár–Körner form `min{D(V‖W|M) : I(M,V) ≤ θ} = sup_{ρ≥0}ρ·[I^A_{1/(1+ρ)}(M) − θ]`, which is at
least Gallager's `sup_{ρ≥0}[E_0(ρ, M) − ρθ]` and in general strictly larger (by up to `1.8·10⁻³`
for eight random `M` on the `path` site below; equal at the optimal `M`).  (3) `E_0(ρ)` is
therefore to be read as `Σ_jλ_j max_{M_j}E_0^{(j)}(ρ, M_j)` — maximised per site type, at a common
`ρ = (1−t)/t`.  The identities of the display are algebra and need no concavity of `F*`.
(4) "A fixed sample certifies `E_sp(θ)`" is for `0 < θ < a`; "adaptive, or with a hint,
certifies `E_sp(θ) − θ`" only for `0 < θ < h`.

**Proposition 11.100 (the exponents of site types do not add; `F*` need not be concave)
[inequalities P; numbers N, certified by duality brackets; workstream W, Proposition
W3.2].**  With `R_j` the exponent of a chain of sites of type `j` alone,

    R̂(e) ≤ min_{Σλ_je_j = e} Σ_jλ_jR_j(e_j) ≤ Σ_jλ_jR_j(e);

the first is an equality iff the `F*_j` coincide with their concave envelopes at the common
slope, the second iff the `R_j` have a common slope at `e`.  What adds: the game functions at
a common slope, the thresholds `E`, the capacities `a`.  For two letters `F*_j` is concave
in every case computed — 100 sites of the workstream, 500 random sites of the reviewer of
SCI-REV-0005, 500 random sites with asymmetric envelopes of ours; slopes `0.02 … 0.98` —
and there is no proof.  As a one-parameter statement **[C]**: `max_p E_0(ρ, p)` is concave
in `ρ` for every binary-input binary-output channel.  **For three letters it need not
be:** for a site with triangle envelope `(1, 1.5, 2)` the optimal label structure switches
discontinuously at `t_c = 0.378` (from two dips and an "anti-dip" to three dips), `F*` has a
convex kink there — a slope jump of `+0.0056`, from `0.054049` to `0.059631` at `t_c = 0.377987`;
the workstream's report prints `+0.0052`, which is a second difference on a grid of step
`5·10⁻⁴` (SCI-REV-0005, m8; re-computed by us in three ways) — and `R̂` a corner at `0.1996·E`.
For the uniform four-letter Hamming site the same happens
between groupings of the letters (Proposition 11.103(e)).  In a chain of half binary, half
three-state sites the average at a common accuracy overestimates `R̂` by `8.5 %`, `47 %`,
`172 %`, `1365 %` at `e/E = 0.3, 0.5, 0.7, 0.9`.

**Theorem 11.101 (adaptive algorithms without a hint) [lower bound: P from machine-checked
pieces, every `n`; upper bound: P by transfer of Theorems 11.52, 11.54, 11.64; reviewed
(SCI-REV-0005): (a) proved, (b) proved with two gaps in the written proof, closed below;
the count of evaluations of Theorem 11.52 is inherited; nothing simulated; workstream W,
Proposition W4.0, Theorem W4].**
(a) *Every algorithm, every `n`:* at the additive instance `γ`, at least
`(1−2δ)·exp(−tε + nΣ_jλ_jF_j(γ_j,t))` evaluations for every `t ≥ 0` (Theorems 11.22(c), 11.27(a),
(b) **[V]** with independent vertex labels site by site, and Markov's inequality).
(b) *Fix the site types, fractions `λ_j > 0`, `0 < ε₁ < E` and `0 < δ < ½`.  Along chains with
compositions tending to `λ`, the least worst-case cost of adaptive algorithms without a
hint that are `(ε₁n/2, δ)`-correct on the class is `exp(n·R̂(ε₁) + o(n))`* — the hinted exponent
of the hardest additive instance, whose Gibbs laws are the Rényi centres of order `t*(ε₁)`
— while non-adaptive algorithms need `exp(nθ_na(ε₁) + o(n))`.  The `o(n)` depends on the site
types and on `(λ, ε₁, δ)`, not on the sequence of chains: it is uniform over all chains
whose composition is within `η` of `λ`, as `η → 0`.  (`λ_j > 0` is the hypothesis of the
workstream's Theorem W4; neither the reviewer nor we see where the argument uses it —
every error term depends on `(m, q_max, D_max, π_min)` only — but the case of vanishing
fractions has not been written out.  Our first version stated neither `δ`, nor the
fractions, nor the uniformity: SCI-REV-0005, m9.)
Changed against Theorem 11.64: the outer block takes a fraction `φ` of the sites of *every*
type; fact (F2) uses the product structure of `π` (the step that fails with interactions);
the tail lemma relative to a reference holds verbatim in the orientation `s(y→x)`; the
number of points `2^{n_o}` becomes `1/min μ_H ≤ e^{c₁n_o}`, `c₁ = ln(1/π_min) + 1` (repair (M2) of
§11.20 is needed for every site law); Harper's function becomes an upper bound for the
tail function of `H`, whose exponent is Theorem 11.97(c) (a bound for `I − v` near the
window replaces the quadratic bound of the binary proof); families of procedures are
indexed by compositions, in the sense defined next.  As in §§11.18–11.20: exponents at
extensive accuracies, with unboundedly many nested levels; not an algorithm to run.
*Families indexed by compositions, and the uniformity that the level induction needs*
**[P; the definition (G1), the claim (G2) and the bound (L) are the reviewer's — Scientific
Discovery Division, SCI-REV-0005, finding M2, `R5_REPORT.md` §4.6 — re-derived by us, (L)
checked numerically; one constant corrected].**  Our first version said "families of
procedures are indexed by compositions" and no more; the workstream's proof speaks of
exponent functions "defined along sequences of compositions tending to `λ`" without a
definition, and claims the bound on the outer sample "uniformly over the compositions
of the outer block" because `R̂` is continuous in `λ`, while the quantity that enters is
`θ_na`.  The level induction applies the one-level theorem to inner blocks whose
compositions differ from `λ` at every level, so without a uniform statement the
"verbatim" transfer of Theorem 11.54 is not a proof — the same kind of gap as (M1) of
referee R9 for two letters.
(G1) *Definition.*  A chain is a vector `n⃗ = (n_1, …, n_m)` of numbers of sites, `|n⃗| = Σ_jn_j`.  A
*family* gives, for every chain, every accuracy `x > 0` and every failure probability `δ′`,
a bracket procedure on that chain whose cost `C(n⃗, x, δ′)` is nonincreasing in `x` and in `δ′`.
`T` is an *exponent function of the family at `λ`* if for all `ξ, c > 0`

    lim_{η↓0} limsup_{N→∞} sup{ |n⃗|^{−1}·ln C(n⃗, ξ|n⃗|, e^{−c|n⃗|}) : |n⃗| ≥ N, ‖n⃗/|n⃗| − λ‖₁ ≤ η }  ≤  T(ξ),

equivalently: along every sequence of chains with compositions tending to `λ`.  If a
chain is within `η` of `λ`, its inner block (`n_j − ⌊φn_j⌋` sites of type `j`) is within
`η + 2m/((1−φ)|n⃗|)` and its outer block within `η + 2m/(φ|n⃗| − m)` of `λ` (the reviewer writes `m`
for `2m`, which fails for one large and several small types; immaterial).
(G2) *The outer sample, uniformly.*  Let `λ°` be the composition of the outer block (`n_o`
sites), `x > 0`, `ω′ := ω_{n_o} + ln 4/n_o` with `ω_n` of Theorem 11.97(c), and `x > 2ω′`.  If
`θ > θ_na^{λ°}(x − 2ω′) + ω′`, then every proper subset `D` of the outer block's space with
`μ_H(D) ≤ e^{−n_oθ}` has `Φ_H(D) ≤ e^{−n_oθ}·e^{n_ox}/4`.  For otherwise Theorem 11.97(c) gives
`θ ≤ R̂(e′) + ω′` with `e′ := x − θ − ω′`, hence `S(e′) = e′ + R̂(e′) ≥ x − 2ω′` and
`θ_na(x − 2ω′) = R̂(S^{−1}(x − 2ω′)) ≥ R̂(e′) ≥ θ − ω′` (all functions for the composition `λ°`;
`R̂` is nonincreasing and `S` increasing).  So the threshold of the closure test satisfies
`q† ≥ exp(−n_o[θ_na^{λ°}(x − 2ω′) + ω′])`, for all rates at once: no restriction to compact sets
of rates is needed.
(L) *`θ_na` is Lipschitz in the composition.*  From `θ_na^λ(x) = sup_{0≤τ<1}(F*_λ(τ) − τx)/(1−τ)`,
`F*_{λ′} − F*_λ = Σ_j(λ′_j − λ_j)F*_j` and `0 ≤ F*_j(τ) ≤ a_j(1−τ)`:

    | θ_na^{λ′}(x) − θ_na^{λ}(x) |  ≤  ‖λ′ − λ‖₁ · max_j a_j        for all x > 0

(with the harness helpers `st_theta_na`, `st_a` on three chains the left side is at most
`0.29` of the right side; with own code on 20 000 random pairs of compositions of the four
example sites, `0.31`), and `θ_na^λ` is continuous on `(0, ∞)` (`GameFunction.pair` **[V]**, field
`na_cont`).  Hence `M† = 2K/q† ≤ exp(nφ·θ_na^λ((g−β)/φ) + o(n))` uniformly over chains with
compositions near `λ`, and the one-level theorem holds for families in the sense of (G1):
if a family has the nonincreasing exponent function `T` at `λ`, then for all `0 < φ < 1`,
`0 < β < g`, `η₀ > 0` there are procedures of accuracy `gn + O(log n)` and cost at most
`exp(n(τ + 2η₀) + o(n))`, `τ` as in (11.18.2) with the present `θ_na`, uniformly near `λ` — the
inner blocks are near `λ` by (G1), only finitely many rates occur, and the outer sample
is controlled by (G2) and (L).  With this the induction written in the proof of Theorem
11.54 (assembly, shift, induction; left limits in the accuracy) goes through verbatim.
*Levels and the Lean statement* (SCI-REV-0005, m7).  The base family is complete
enumeration, `T₁ ≡ Σ_jλ_j ln q_j` — not the non-adaptive exponent — and
`T_{k+1} = min(T_k, R[T_k])`.  The machine-checked statement that covers this start is
`iterates_lt_hint_add` (`HintRecursion.lean`; its hypothesis `hbdd` asks only that `T₁` be
bounded) with the `HintPair` supplied by `GameFunction.pair` (`GamePair.lean`; no concavity of
`F*` among its hypotheses), exactly as in the proof of Theorem 11.64; that `min(T, R[T])`
satisfies the step inequality is `stepLE_exact` (`BoundedAccuracy.lean`).
`GameFunction.exactRec_tendsto` — Theorem 11.66(c) — is about the recursion started at `θ_na`
and is not the statement used here.  The bounds (G2), (L) also serve the non-adaptive
upper bound of Theorem 11.98(d) along sequences of compositions.

**Proposition 11.102 (asymmetric envelopes) [P; N for the example; workstream W, Theorem
W6, Proposition W6.1].**  Everything above is stated and proved for envelopes that need
not be symmetric, in the orientation fixed in the setting (the slack of an additive
instance is asymmetric even for a metric: the hinted theory was already a theory of
quasi-metrics).  For two letters an asymmetric envelope `(u₁, u₂)` is the symmetric one with
`u = (u₁+u₂)/2` and the site law tilted by `(u₂−u₁)/2` (the normal form of §11.11; `3·10⁻¹⁶`).  For
three letters the antisymmetric part need not be a gradient, and the zero residual can
be far from the hardest instance (`R_0/R̂ = 0.75` at `e = 0` and `0.15` at `0.7E` in the example
below).  One must not symmetrise: `max(d, dᵀ)` enlarges the class, `min(d, dᵀ)` shrinks it.

**Proposition 11.103 (known parts that are functions of the joint type; which site law is
hardest) [(a)–(c): P, workstream W, Propositions W7.1–W7.3(a); (d): N, certified by
duality, workstream W for the threshold, the coordinator for `h` and `a`, corrected after
SCI-REV-0001 §5 and SCI-REV-0005 §7; (e): the identity P, the rest N, coordinator; (f): P,
the reviewer's of SCI-REV-0001, re-derived by us].**
(a) *What of §11.23 transfers* to a known part `nφ(P_x)` with any alphabets and site types:
Theorems 11.76, 11.78, Lemma 11.77(b) (by an optimal coupling instead of thinning), Theorem
11.79; for a convex rate function also the collapse to additive instances and the game
function.  *Not:* clipping (Lemma 11.77(a)), "binary centres suffice" (vertex labels, at
most `q_j`, for product measures; open with interactions), the Rényi form, the nested
algorithm.
(b) *Mean-field Potts, convex regime:* at the colour-symmetric profile the value is the
flat product site's, for every coupling (`0.03065363` at `u = 1`, `q = 3`; by symmetry).
(c) *Ferromagnets:* `R_H ≤ sup_p R̂_{product site with law p}` over the effective site laws.
(d) **"A field always helps" (Proposition 11.65(b)) and Corollary 11.91 are statements
about two letters.**  For three letters with the Hamming envelope the uniform site law
is not the hardest: *near the threshold* at `u = 1`, `E = 0.119499` for the uniform law
against `0.120196` for `π = (0.05, 0.5, 0.45)` and `0.120115` for the two-letter cube; *at
vanishing accuracy for small slopes*, site laws close to `(½, ½, 0)` *tend to* the two-letter
values as the third letter becomes rare, and `h₂ > h₃` **exactly when `u < ln 2`** (`0.007673`
against `0.007425` at `u = 0.5`; the crossing at `ln 2` is exact by (e), that it is the only
one is numerical), `a₂ > a₃` when `u < 0.5194` (`0.011125` against `0.010582` at `u = 0.3`).  **Nor is
the two-letter cube the supremum:** at `u = 0.5` a *rare third state*, `π = (0.05, 0.5, 0.45)`, has
`h = 0.0076752`, `a = 0.0303217`, `E = 0.0309316`, each above the cube's `0.0076729`, `0.0302999`,
`0.0309298` — it is the maximum of all three on the grid of 171 laws — and the law
`(0.04502, 0.45679, 0.49819)`, where a local search for the largest `h` ends, has `h = 0.0076753`,
an excess of `0.03 %` over the cube (certified by a primal value); whereas `(0.02, 0.49, 0.49)`
is below the cube in `h` and `E` (`0.0076722`, `0.0309220`) and above it in `a` **[N; the first two
data points are the Scientific Discovery Division's (SCI-REV-0005 §7; SCI-REV-0001 §5),
re-computed by us with the harness helpers and with own code; the third is ours]**.
One half of this is a theorem **[P; the reviewer's of SCI-REV-0005, re-derived by us]**:
*for the Hamming envelope every site law that gives some set `A` of letters the weight `½`
has `F*(t) ≥ F*_cube(t)` for all `t`*, hence is at least as hard as the two-letter cube in `h`,
`a`, `E`, `R̂` and `θ_na` — the two box vertices `∓u·1_A` have Gibbs laws that differ only through
the indicator of `A`, on which they form the binary symmetric channel with crossover
`1/(1 + e^u)`; the strict excess is numerical.  (Our first version said that site laws
close to `(½, ½, 0)` "have the two-letter values"; so "the hardest known part is a
uniformly weighted sub-alphabet" fails at vanishing accuracy and for `u < ln 2` too.)
At `u = 1` and `u = 2` the uniform law does maximise `h` and `a` on a grid of 171 laws
(workstream; at `u = 1` re-computed by the reviewer and by us: grid maxima `0.030572`,
`0.122951` at `(0.3, 0.35, 0.35)` against `0.030654`, `0.123284` for the uniform law).  **So with
three or more letters a known part — a field, or one that pins the composition — can
make certification harder than no known part.**
(e) *Uniform sites group their letters.*  For the uniform law on `q` letters with the
Hamming envelope the vertices are the indicator functions of subsets ("boxes"), and for
`q = 3, 4` and `u ∈ {0.5, 1, 2, 3}` each of `E`, `a`, `h` equals the largest of its values for single
dips on `k` equally weighted groups of letters, `k | q`:

    h_k = max_t[tΨ_k(u) − Ψ_k(tu)],    a_k = ln k − H(p_k, (1−p_k)/(k−1), …),    E_k = Ψ_k(u),    Ψ_k(s) = ln((e^s + k − 1)/k) − s/k,   p_k = e^u/(e^u + k − 1)

(`q = 4`, `u = 1`: `h = h₂ = 0.029139`, `a = a₄ = 0.117993`, `E = E₂ = 0.120115` — three different
groupings for the three quantities, hence a label switch along `t`).  **Exactly at
`e^u = k(k−1)`, `h_k = h_{k+1}`** (there the optimal mismatch fractions of the two cubes add up to
one), so among equal groupings the hardest number of groups at slope `u` is the `k` with
`(k−1)(k−2) ≤ e^u ≤ k(k−1)`, about `e^{u/2}`: *a site with many equivalent states is, for
certification at vanishing accuracy, a site with about `e^{u/2}` states.*  Whether unequal
groupings can win for larger `q`, and the corresponding statement for type classes, are
open; the remark in §11.25 on Potts pairs is the letters-as-labels part of this.
(f) *A universal ceiling.*  For every site — any alphabet, any site law, any envelope,
symmetric or not — with `D = max_{a,b}d(a,b)` (`D = u` for the Hamming envelope) and `0 ≤ t ≤ 1`

    F*(t) ≤ t(1−t)·D²/8,        hence        h ≤ D²/32,      E ≤ D²/8,      a ≤ D²/8,

and for a chain the same with `Σ_jλ_jD_j²` for `D²`.  *Proof.*  Take `Q = π` in the radius form of
Theorem 11.99: for `φ` in the Lipschitz polytope, `(1−t)·D_t(π_φ‖π) = tΛ(1) − Λ(t)` with
`Λ(s) = ln E_πe^{−sφ}`, and `Λ″(s)` is the variance of `φ` under a tilted law, at most
`(max φ − min φ)²/4 ≤ D²/4` (Hoeffding's lemma); a function that vanishes at `0` and `1` and whose
second derivative is at least `−c` is at most `c·t(1−t)/2`.  ∎  The two-letter cube attains the
ceiling to leading order as `u → 0` (`h = 0.9993·u²/32` at `u = 0.1`).  So with three or more
letters a field *can* make certification harder than no field, but never by more than
the distance of the unconstrained site from the ceiling: the uniform three-letter
Hamming site is below it, in `h`, by `11 %` as `u → 0` (`Ψ₃(s) ≈ s²/9` against `s²/8`), by `5.0 %` at
`u = 0.5`, `1.9 %` at `u = 1`, `5.8 %` at `u = 2` **[N]**.  (The statement for the Hamming envelope is
the Scientific Discovery Division's, SCI-REV-0001 §5; the extension to every envelope is
the same proof.  Checked on 40 sites — cubes, uniform and non-uniform Hamming sites with
`u` from `0.1` to `3`, the example sites, twelve random asymmetric sites — with the dual values
of the harness helper `st_renyi` and of an own implementation: largest ratio `0.9996`.  As
a statement about exponents it has the status of Theorems 11.98, 11.99 and 11.101.)

**A worked example** [N; every optimum certified by a duality bracket `≤ 2·10⁻⁹` and
re-evaluated by a primal solver (workstream); re-computed by the coordinator; replicated
by the reviewer of SCI-REV-0005 with an own library — largest deviation `5·10⁻⁷`, the
rounding of the table].  Sites:
`bin` (two states, `π = (0.7, 0.3)`, `u = 1`); `path` (three states on a path with steps `0.8`, `1.6`,
`π = (0.5, 0.3, 0.2)`); `tri` (triangle `1, 1.5, 2`, `π = (0.2, 0.5, 0.3)`); `asym`
(`d = [[0,1,2],[0.5,0,1.5],[1,0.5,0]]`, `π = (0.5, 0.3, 0.2)`); `mix` = half `bin`, half `path`;
`mix2` = `0.4` `bin`, `0.6` `tri`.

| chain | `E` | `a` | `h = R̂(0)` | `R̂(0.3E)` | `θ_na(0.3E)` | zero residual `R_0(0)` | best binary coarse-graining / deletion at `e = 0` |
|---|---|---|---|---|---|---|---|
| `bin` | `0.103131` | `0.095301` | `0.025034` | `0.012209` | `0.019941` | | |
| `path` | `0.400622` | `0.294791` | `0.089589` | `0.043375` | `0.066899` | `0.080032` | `0.048586` / `0.115369` |
| `tri` | `0.284907` | `0.247541` | `0.066729` | `0.032077` | `0.051124` | `0.065233` | `0.053168` / `0.094950` |
| `asym` | `0.191059` | `0.166046` | `0.045407` | `0.022108` | `0.035544` | `0.033856` | `0.024685` / `0.058646` |
| `mix` | `0.251877` | `0.195046` | `0.057275` | `0.027759` | `0.043288` | `0.052360` | |
| `mix2` | `0.212197` | `0.186645` | `0.050050` | `0.024122` | `0.038641` | `0.049065` | |

The hardest instance moves the site law to the Rényi centre of its window (`path`:
`(0.5, 0.3, 0.2) → (0.473, 0.246, 0.281)`); the optimal labels of `path` are the dips at the two
*ends* of the path, each with the full three-level profile.  **A three-state site is not
its worst two-state reduction:** coarse-graining two states (a subclass, hence a lower
bound) gives `54 %`–`80 %` of the exponent and too small a threshold; deleting a state (not a
bound) gives `129 %`–`142 %`.  Exact sums over joint types (workstream; `n ≤ 480`) approach the
formulas like `c·ln n/n`: e.g. on `mix` at `n = 480` and accuracy `0.3En + 1 = 37.3` every algorithm
needs at least `(1−2δ)·1.9·10⁶` evaluations at the hardest additive instance.

*Reading for design* (interpretation; an idealised class).  (1) The certification cost of
a heteropolymer landscape is not a sum over site types at a common accuracy: the types
share a *slope*, and a type that is past its own threshold still contributes.  (2) The
quantity to control per site is a capacity of the family of site laws that the allowed
perturbations can produce — not the number of states: many equivalent states are
cheaper than a few (item (e)), and removing states can make things worse.  (3) One-sided
information (an asymmetric envelope) is as tractable as two-sided information and must
not be symmetrised.

*Harness.*  XXII.1 (vertices; the Rényi form against the game and its dual bound, on the
example sites and on random sites with asymmetric envelopes; the values of `h`), XXII.2 (one
common slope; non-additivity; pair identity; the dictionary on the cube; the normal form
of an asymmetric two-letter envelope), XXII.3 (which site law is hardest: the three-letter
threshold, small slopes, the exact crossings `e^u = k(k−1)`, uniform three and four
letters), XXII.5 (added with the review: the ceiling `t(1−t)u²/8`; the comparison with the
cube for site laws with weight `½` on a set of letters; the two data points at `u = 0.5` on
either side of the cube; the slope jump `+0.0056` at the kink of the triangle site; the
Lipschitz bound of `θ_na` in the composition), XXI.5 (the integral form of the game function;
Potts pairs), DEAD.23 (`F*` concave), DEAD.24 (the uniform site law is the hardest); XXII.4
belongs to §11.27; 29 mutations in block XXII, each caught for the intended reason.  The
scripts with which the corrections of the review were checked are in
`experiments/coordinator_checks/sites_W/review_R5/`.

*Prior art* (verification status: search summaries only — two searches by the workstream).
Rényi capacity, radius and centre, and `E_0(ρ) = ρC_{1/(1+ρ)}`: Csiszár (1995); Nakiboğlu (2019,
*The Rényi capacity and center*).  The sphere-packing exponent in the constant-composition
form: Csiszár–Körner; Nakiboğlu (2019, *The sphere packing bound via Augustin's method*).
Additivity of `E_0` over parallel channels: Gallager.  Not found by the workstream or in
this report's earlier sections: the identification of the complexity of certifying a
normalising constant over a Lipschitz class with these exponents.  "Not found", not
"new"; the Scientific Discovery Division was asked to look (THY-REQ-0011) and did not
recognise the operational statement in print either (SCI-REV-0005 §7: four searches at
the level of snippets; its search in full texts is SCI-RES-0003).  Two readings from its
review say what the dictionary is; both identities are elementary and were re-derived
by us, the attributions are the reviewer's and were not checked: the shear law is the
Neyman–Pearson identity `D(V‖P) − D(V‖Q) = E_V ln(dQ/dP)`, and `E_sp` is Hoeffding's trade-off
`min{D(V‖P) : D(V‖Q) ≤ θ} = sup_ρρ·[D_{1/(1+ρ)}(P‖Q) − θ]` between the two error exponents of
testing a vertex law `P` against a centre `Q`, with the divergence replaced by the radius —
the sampling rate is the type-II exponent, the accuracy rate the type-I exponent.  The
non-concavity of `max_M E_0(ρ, M)` for channels with more inputs than outputs — our "label
switch" — is, according to the reviewer, textbook material (Gallager 1968; from the
reviewer's memory).

*Not done.*  A referee for what the review SCI-REV-0005 did not cover — Propositions
11.100, 11.102, 11.103(a)–(c), the consequence of Theorem 11.97(b) for hinted algorithms,
the count of evaluations inherited from Theorem 11.52 — and, as the reviewer recommends,
for Theorem 11.97(c) together with Theorem 11.78(b).  A finite-`n` form of Theorem
11.97(c): exact tail functions of the reference `H` on chains small enough for exhaustive
search (the reviewer's request R5-E1 to the engineering division), and the true size of
`ω_n`.  The nested algorithm end to end.  Alphabets with more than four
letters and more than two site types numerically.  Upper bounds at bounded accuracy.
Non-convex functions of the joint type (the first-order transition of the Potts model).
Concavity of `F*` for two letters.  Which site law, and which pinned composition, is the
hardest for a given envelope.


### 11.27 Evaluations together with local ensemble-averaged data (a question of the Scientific Discovery Division)

The Scientific Discovery Division (branch `research/scientific-translation`, commit `9c4bf96`,
SCI-MSG-0001 §4 and `docs/science/INFERENCE_LIMITS.md` there) considers a second kind of
information: besides evaluations of the residual, the algorithm is given, exactly and for
free, all marginals of the Gibbs measure `μ_ψ ∝ e^{−ψ}` on sets of at most `k` sites — an
idealisation of local experimental data.  Its Lemma A: *if `C ⊂ F₂ⁿ` is a linear code whose
dual has minimum distance at least `k + 1`, every probability measure invariant under
translation by `C` has exactly uniform marginals on every set of at most `k` coordinates*
(a coset of such a code is an orthogonal array of strength `k`; **[K]**).  Its Theorem C: on
the cube class with zero known part such an oracle divides the lower bound for all
algorithms at the zero residual by at most `|C| ≤ (2n)^{⌈k/2⌉}`, so the hinted (= adaptive)
exponent is unchanged.  It asked whether the same holds for the non-adaptive exponent
`θ_na` of §11.16, where the hard instances are cones with a hidden centre, which one-body
marginals reveal.  It does:

**Proposition 11.104 (a marginal oracle does not change the non-adaptive exponent on the
cube) [P; coordinator, with Lemma A of the Scientific Discovery Division; the finite
statements checked by exact enumeration, harness XXII.4].**  Cube `Q_n`, zero known part,
class `L_u`.  Let `C` be as in Lemma A, `ψ = u·d(·, a)` a cone, `ψ^{tr} = max(ψ, ur)` its truncation at
the radius `r`, and `ρ := A(ψ)/A(ψ^{tr})`.  If `ε < ln(1 + (ρ − 1)/|C|)`, every randomised non-adaptive
algorithm that receives all marginals of `μ_ψ` of order at most `k` and is `(ε/2, δ)`-correct on
`L_u` makes at least

    (1 − 2δ) · 2ⁿ / ( |C| · |B(n, r−1)| )

evaluations.  With duals of BCH codes, `|C| ≤ (2n)^{⌈k/2⌉}`: **the exponent `θ_na` is unchanged by
free local ensemble-averaged data of every order `k = o(n/ln n)`**; with Theorem C of the
other division, so are both exponents of §§11.16–11.19.
*Proof.*  Let `ψ_C := u·d(·, a + C)` (a distance to a set, hence in `L_u`) and
`ψ_C^{tr} := max(ψ_C, ur)`; in weights, `w_C = max_{c∈C}w_c` with `w_c` the cone at `a + c`, and
`w_C^{tr} = min(w_C, e^{−ur})`.  Both are invariant under translation by `C`, so by Lemma A their
Gibbs measures have uniform marginals of order `k`: the oracle answers identically on
both, and also on their images under any translation and permutation of the coordinates
(the image of `C` is a code with the same dual distance).  They differ on
`{d(·, a + C) < r}`, at most `|C|·|B(n, r−1)|` points.  And
`A(w_C) − A(w_C^{tr}) = E(w_C − e^{−ur})₊ ≥ E(w_0 − e^{−ur})₊`, `A(w_C^{tr}) ≤ |C|·A(w_0^{tr})`, so
`A(ψ_C)/A(ψ_C^{tr}) ≥ 1 + (ρ − 1)/|C|`.  Now the argument of Theorem 11.61(b)(i) for the group of
translations and permutations, which acts transitively: a fixed sample point lies in the
image of the difference set with probability `|C||B(n, r−1)|/2ⁿ`, and outside that event the
values *and the oracle's answers* coincide.  ∎
*Remarks.*  (1) What local data do reveal is the centre of a *single* cone; the adversary
answers by hiding it among `|C|` centres that no `k`-body statistic can tell from none.
(2) For a field as known part, translation by a code does not preserve the reference
measure; the natural setting is one type class with designs in the Johnson scheme
(§11.25).  Open.  (3) The general two-oracle model — evaluations of the residual and
expectations of a restricted family of observables under its Gibbs measure — has the two
ends the other division names (linear classes: rank-many evaluations, §11.17; exponential
families: rank-many expectations) and nothing in between.  Open, and theirs.
(4) The Scientific Discovery Division proved the same statement independently, on the
same day, as its "Theorem 4′" (non-adaptive algorithms need `(1 − 2δ)·2ⁿ/(|C|·|B(R−1)|)` whenever
`ε < D_R − ln|C|`; SCI-REQ-0001); the two proofs use the same symmetrised cones.  Its
follow-up question — what a one-body oracle is worth *with a field*, where translations
are not symmetries — is its SCI-REQ-0001, Q2, and is being worked on.


### 11.28 Observable free energies: the robust range of a ratio of macrostate weights (a question of the Scientific Discovery Division)

Everything from §11.6 on is about the total `ln Z`.  The Scientific Discovery Division
objected (SCI-MSG-0001 §5; SCI-REQ-0001, Q1) that this is not what an experiment compares
with: `ln Z(f+g) − ln Z(f)` is not an observable, and the observable free energies are
*differences between macrostates*, `−ln[Z(A)/Z(B)]`.  (An earlier version of this paragraph
also quoted the division's sentence that the total `ln Z` is fixed by a caloric curve
without any model; the division withdrew it — SCI-MSG-0008 §1(b), SCI-RES-0005 §4: that
needs the caloric curve down to `β = 0` on the model's own configuration space, and
calorimetry measures the energy of all degrees of freedom.  The motivation of this
section does not need it.)  It asked for the exact range of such a ratio over the residual class,
for its extremal residuals, and for a certificate.  This section answers that question
for the *range* (what a certificate can assert); the number of evaluations needed to
narrow it is not treated.  The division contributed the first reduction (its addendum
A3: the residual on `A` is a lower extension from `B`) and a three-point example in which
the extremal residual is constant on neither macrostate; our earlier answer to it
(THY-RES-0003 §3: "we have no closed form") is superseded.

**Status of this section.**  The coordinator's paper proofs, written in answer to the
request; **not refereed**.  Machine-checked (`proofs/Frontiers/MacroRatio.lean`): the
certificate half of Theorem 11.105 — weak duality, the plan for a single state, both
halves of the max–min sandwich, and the admissibility of closed pairs.  Strong duality is
linear-programming duality **[P]**.  Every statement was checked numerically before it
was written (`experiments/coordinator_checks/ratios/`; harness block XXIII).  **Reviewed
and replicated by the Scientific Discovery Division** (SCI-RES-0005: Theorems 11.105–11.107
re-derived, 11.105 and 11.106 replicated with its own code on 400 and 24 instances, the
Lean file compiled there; of Theorem 11.108 two steps were checked, its limit and its
numbers were not) — no finding above "minor"; its four remarks are applied below.
**Prior art** (searched by that division, not by us: six searches at the level of search
summaries and abstract pages, no full text opened — SCI-RES-0005 §2).  *For a separable
envelope the theorem is classical:* if `e^{d(x,y)} = U(y)/L(x)` for `x ≠ y` with two positive
functions `L ≤ U` (densities relative to `w`), the class is the **density-ratio class** of
robust Bayesian analysis — all measures between a lower and an upper one, up to a
constant (DeRobertis–Hartigan 1981) — and the programme of Theorem 11.105(a) has the
closed form `R⁺(A,B) = Σ_A wU/Σ_B wL` (`t = U` on `A`, `t = L` on `B`), the textbook range of a
posterior odds (the division's positioning; re-derived by us: a separable envelope
satisfies the triangle inequality, and every constraint from `B` to `A` is tight at this
`t`).  **Theorem 11.105 is the extension from separable envelopes to envelopes with the
triangle inequality**, where there is no closed form and what survives is the reduction
to the constraints from `B` to `A`, the closed pairs and the transport dual.  The dual
object is classical as well (flows with gains: Jewell 1962), and the same cone for a
metric `d` is the setting of metric differential privacy (Chatzikokolakis et al. 2013),
used there for mechanisms and not for the range of a ratio of two events.  Two leads
are unresolved: credal sets from comparative probability judgements, and the cones of
the Birkhoff–Hilbert-metric method for decay of correlations (the latter from the
division's memory only).  The division's classification: Theorem 11.105 a plausibly
original generalisation of a known closed form with a classical dual; "not found in six
searches at summary level" is all that is claimed.

**Setting.**  `X` finite, weights `w = e^{−f} > 0`, an envelope `d ≥ 0` with `d(x,x) = 0` and the
triangle inequality, not necessarily symmetric; residuals are admissible if
`g(x) − g(y) ≤ d(x,y)`.  `A, B ⊂ X` are disjoint and non-empty, `Z_g(S) := Σ_{x∈S} w(x)e^{−g(x)}`, and

    R⁺(A, B) := sup{ Z_g(A)/Z_g(B) : g admissible }.

The free-energy difference `ΔF_g := −ln[Z_g(A)/Z_g(B)]` ranges exactly over the interval
`[−ln R⁺(A,B), ln R⁺(B,A)]`: the admissible residuals form a convex, hence connected, set,
and both ends are attained (Theorem 11.105(b)) — **by different residuals**, so the
interval of a difference of two free energies is not the difference of the intervals of
the two free energies.

**Theorem 11.105 (duality for the robust ratio) [(c) weak duality, (d) upper bound, (e), and
the admissibility in (b): [V] `macro_le_of_plan`, `macro_single_le`, `macro_le_card_mul`,
`macro_cone_ge`, `closed_pair_within_A`, `closed_pair_within_B`, `closed_pair_cross`; the rest P].**
(a) *Only the constraints from `B` to `A` matter.*

    R⁺(A, B) = max{ Σ_{y∈A} w(y)t(y) / Σ_{z∈B} w(z)t(z) :  t > 0 on A ∪ B,  t(y) ≤ e^{d(z,y)} t(z) for all z ∈ B, y ∈ A }

(`t = e^{−g}`): the constraints inside `A`, inside `B`, from `A` to `B`, and all constraints
through states outside `A ∪ B` can be dropped.
(b) *Closed pairs.*  Call `g` on `A ∪ B` *closed* if `g(y) = max_{z∈B}[g(z) − d(z,y)]` on `A` (the lowest
values that `g|_B` allows) and `g(z) = min_{y∈A}[g(y) + d(z,y)]` on `B` (the highest that `g|_A`
allows).  From any residual that satisfies the constraints of (a), the lowest extension
to `A` followed by the highest extension to `B` produces a closed pair with a ratio at
least as large; a closed pair is admissible on `A ∪ B` in all four directions; the maximum
in (a) is attained at a closed pair.  *Closed is necessary for optimality, not
sufficient* (a remark of the Scientific Discovery Division, SCI-RES-0005 §1): on the
cube with the envelope `u·`Hamming and **any** known part, the maximal field `g = −u|x|` is a
closed pair for every up-set `A` and its complement `B` (every state of `A` lies above the
all-zero state, which is in `B`; every state of `B` below the all-one state, which is in
`A`); it is optimal for exchangeable known parts with a threshold (Theorem 11.106) and
for submodular known parts (Theorem 11.106a), and not optimal in a large fraction of
random frustrated instances (**[N]**; the division's count: 49, 66 and 81 % at `n = 3, 4, 5`;
ours: 17 of 25, harness XXIII.6).  The fixed points of the improvement map are not all
maxima.
(c) *Transport with gains.*

    R⁺(A, B) = min{ λ :  ∃ ψ ≥ 0 on B × A,   Σ_{y∈A} e^{d(z,y)} ψ(z,y) ≤ λ·w(z)  (z ∈ B),   Σ_{z∈B} ψ(z,y) ≥ w(y)  (y ∈ A) }.

Read `ψ(z,y)` as mass delivered at `y` from `z`; delivering it costs `e^{d(z,y)}ψ(z,y)` at `z`; `λ` is
the factor by which the weight of `B` must be scaled to cover `A`.  **Every feasible pair
`(ψ, λ)` is a certificate: `Z_g(A) ≤ λ·Z_g(B)` for every admissible `g`** (three lines; **[V]**).
(d) *One state.*  `R⁺({y}, B) = w(y)/Σ_{z∈B} w(z)e^{−d(z,y)}` (Theorem 11.12 is the case `B = X∖{y}`), and
`R⁺(A, {z}) = Σ_{y∈A} w(y)e^{d(z,y)}/w(z)`.
(e) *Max–min sandwich.*  With `M := max_{y∈A} min_{z∈B} e^{d(z,y)}·w(y)/w(z)`:

    M/|B|  ≤  R⁺(A, B)  ≤  |A|·M ;

the lower bound is attained by the **cone** `g = d(·, y)` around a maximising state `y ∈ A`,
the upper bound by the plan in which every state of `A` is served by its best state of `B`.

*Proof.*  (c), weak duality: for admissible `g`,
`Z_g(A) ≤ Σ_yΣ_z ψ(z,y)e^{−g(y)} ≤ Σ_zΣ_y ψ(z,y)e^{d(z,y)}e^{−g(z)} ≤ λΣ_z w(z)e^{−g(z)}`, using
`e^{−g(y)} ≤ e^{d(z,y)}e^{−g(z)}`; only the constraints from `B` to `A` were used.  Strong duality:
normalise `Σ_B w t = 1` (Charnes–Cooper); the programme of (a) is linear, feasible (`t`
constant) and bounded, and its dual is the programme of (c).
(b) Let `g` satisfy the constraints of (a).  Its lowest extension `g′` to `A` is `≤ g` on `A`
(the constraints say `g(y) ≥ g(z) − d(z,y)`), so the numerator does not decrease; the
highest extension `g″` to `B` of `g′|_A` is `≥ g` on `B`, so the denominator does not increase; and
`g′|_A` is still the lowest extension of `g″|_B` (it is compatible with `g″|_B`, and `g″ ≥ g` on `B`).
So `(g′|_A, g″|_B)` is closed.  A closed pair is admissible inside `A` (a maximum of the
functions `y ↦ g(z) − d(z,y)`, each of which is, by the triangle inequality), inside `B`
(a minimum of the functions `z ↦ g(y) + d(z,y)`), and from `A` to `B`: with `z′` attaining the
maximum for `y` and `y′` attaining the minimum for `z`,
`g(y) − g(z) = [g(z′) − g(y′)] − d(z′,y) − d(z,y′) ≤ d(z′,y′) − d(z′,y) − d(z,y′) ≤ d(y,z)`.
(a) A closed pair extends from `A ∪ B` to an admissible residual on `X` (McShane:
`g(x) := min_{v∈A∪B}[g(v) + d(x,v)]`), so the relaxed maximum is attained by an admissible
residual; the reverse inequality is trivial.  (d) For one state the plan
`ψ(z,y) = λw(z)e^{−d(z,y)}` is feasible with the stated `λ`, and the cone `g = d(·, y)` attains it;
the second formula is the lowest extension from the single state `z`.
(e) Lower bound: the cone `g = d(·, y)` is admissible, `Z_g(A) ≥ w(y)`, and
`Z_g(B) = Σ_z w(z)e^{−d(z,y)} ≤ |B|·max_z w(z)e^{−d(z,y)}`.  Upper bound: the plan
`ψ(z,y) = w(y)·1[z = z(y)]`, `z(y)` a minimiser, has `λ = max_z Σ_{y: z(y)=z} e^{d(z,y)}w(y)/w(z) ≤ |A|·M`.  ∎

*Remarks.*  (1) The division's reduction is the first half of (b); its three-point
example (`A = {x₁, x₂}`, `B = {y}`, `d(x₁,y) = 1`, `d(x₂,y) = d(x₁,x₂) = 10`) is the second formula of (d):
the extremal residual is `g(x_i) = g(y) − d(y, x_i)`, which differs by `9` between the two
states of `A`.  (2) The extremal residuals are cones in the simplest cases only; in
general they are closed pairs — "distance functions between the two macrostates,
alternately from one and from the other" — and the programme has to be solved.  (3) The
sandwich (e) loses the *entropy of the macrostates* (`ln|A|`, `ln|B|`) and nothing else; it
is the reason why at the exponential scale the answer is a max–min (Theorem 11.108).

**Theorem 11.106 (symmetry; the two sides of a threshold) [P].**  Let a finite group act on
`X` preserving `w`, `d`, `A` and `B`.  Then an optimal residual can be chosen invariant, and
`R⁺(A,B)` is the value of the same programme on the orbit space, with the orbit weights and
the distances `δ(O, O′) = min{d(x,y) : x ∈ O, y ∈ O′}`; Theorem 11.105(e) holds with `|A|`, `|B|`
the numbers of orbits.  In particular, on the cube with an exchangeable reference
measure (weights `W_j = π(T_j)` of the type classes — any known part that is a function of
the type), the envelope `u·`Hamming and macrostates that are unions of type classes, the
programme lives on the `n + 1` types with the distances `u|j − k|`.
*If every type of `B` lies below every type of `A`* — the two sides of a threshold of the
order parameter, with or without a gap between them — **the extremal residual is the
maximal field** `g = −u|x|`, the only closed invariant pair:

    R⁺(A, B) = Σ_{j∈A} W_j e^{uj} / Σ_{k∈B} W_k e^{uk},        n⁻¹ ln R⁺ → max_{κ∈𝒜}[uκ − I(κ)] − max_{κ∈ℬ}[uκ − I(κ)].

In the mirror case — every type of `B` above every type of `A` — the extremal residual is
the minimal field `g = +u|x|` by the same argument, so `R⁺(B, A)` of a threshold pair is
attained at `+u|x|`.  So the robust interval of the free-energy difference between the two
sides of a threshold, `[−ln R⁺(A,B), ln R⁺(B,A)]`, is spanned by the two extreme fields `∓u`
(the uniqueness of the *invariant* closed pair is what the argument uses; closed pairs
that are not invariant may exist and are not optimal); for the two halves of the uniform
cube it is `±n·ln cosh(u/2)·(1 + o(1))` — the threshold constant of §11.10 once more.  *For
a band between two parts of `B`* no field is extremal; in the examples the optimum is a
cone around a type class of the band.
*Proof.*  In the weights `t` the constraints are linear and the objective is a ratio of
two linear functionals; after normalisation the set of optimal `t` is convex and
invariant, so the average of an optimal `t` over the group is optimal and invariant.  For
invariant `t` the binding constraint between two orbits is the one with the least
distance.  Threshold case: put `G(k) := g(k) + uk` on the types of `B` and `H(j) := g(j) + uj` on those
of `A`; the two closure equations read `H(j) = max_kG(k)` for all `j` and `G(k) = min_jH(j)` for all
`k`, so `g + u·`type is constant on `A ∪ B`.  ∎

**Theorem 11.106a (monotone macrostates: the two uniform fields are extremal) [V on the cube
and on ordered alphabets — the sandwich theorem of the Scientific Discovery Division
(SCI-MSG-0009; ordered alphabets: SCI-MSG-0011 §2), machine-checked by it (SCI-MSG-0014) and
adopted here unchanged as `proofs/Frontiers/MonotoneSandwich.lean`: `holley_cross`,
`cube_sandwich_mean`, `cube_macrostate_ratio`, `cube_mean_isLeast`, `cube_mean_isGreatest`,
`cube_ratio_range_eq_Icc`, `pairwise_submodular`, `stepField_sandwich_mean`; the formula for the
width: P; the Holley step re-derived by us and the statement replicated with the linear
programmes of Theorem 11.105, harness XXIII.6].**  `X = {0,1}ⁿ` with the coordinatewise order;
the envelope has constants `c_i^↑` for raising and `c_i^↓` for lowering site `i`
(`d(x,y) = Σ_{x_i>y_i}c_i^↑ + Σ_{x_i<y_i}c_i^↓`, with `c_i^↑ + c_i^↓ ≥ 0` — otherwise the class is empty); the
known part `f` is **submodular**, `f(x∨y) + f(x∧y) ≤ f(x) + f(y)` — every additive `f`, every
pairwise `f` with couplings `J_ijx_ix_j`, `J_ij ≤ 0`.  Put `h^↑(x) = Σ_ic_i^↑x_i`, `h^↓(x) = Σ_ic_i^↓x_i`.  Then
for every admissible `g`

    μ_{f + h^↑}  ≼  μ_{f + g}  ≼  μ_{f − h^↓}        (stochastic order),

and both ends are members of the class.  Hence for every lower set `A` and every non-empty
upper set `B` — complementary or not — the ratio `Z_g(A)/Z_g(B)` is largest at `g = h^↑` and
smallest at `g = −h^↓`, and takes every value in between: **the extremal residuals are the
two uniform fields, the same for every pair of monotone macrostates and every increasing
observable**; and for `c^↑ = c^↓ = c` the width of the range is
`ln R⁺(A,B) + ln R⁺(B,A) = ∫_{−1}^{1}Σ_ic_i(⟨x_i⟩_{B,t} − ⟨x_i⟩_{A,t})dt`, the means taken in
`μ_{f + th}(·|B)` and `μ_{f+th}(·|A)`: a site contributes its constant times the difference of
its mean occupation between the two macrostates, and uncertainty common to both cancels.
*Proof (the division's).*  Holley's inequality: `μ₂(x∨y)μ₁(x∧y) ≥ μ₁(x)μ₂(y)` for all `x, y`
implies `μ₁ ≼ μ₂`.  For `μ₁ = μ_{f+h^↑}`, `μ₂ = μ_{f+g}` the condition reads
`[f(x∨y) + f(x∧y) − f(x) − f(y)] + [g(x∨y) − g(y)] ≤ h^↑(x) − h^↑(x∧y)`: the first bracket is
`≤ 0`; `x∨y` differs from `y` exactly on `{x_i = 1, y_i = 0}`, where it is raised, so the second
is at most `Σ_{x_i=1,y_i=0}c_i^↑`, which is the right-hand side.  The other end is symmetric.
The width: `∂_t ln[Z_{f+th}(A)/Z_{f+th}(B)] = ⟨h⟩_{B,t} − ⟨h⟩_{A,t}`.  ∎
(In the Lean file the Holley step is the four-functions theorem in cross-multiplied form
for unnormalised weights; the theorem is stated on any finite distributive lattice with
an envelope that two functions saturate, the cube and ordered alphabets being instances;
`β ≥ 0` is needed, and a two-site witness shows that the inequalities can be strict.)
*Relation to Theorems 11.105, 11.106.*  For threshold macrostates of the uniform cube the
two results give the same formula, `R⁺ = P[Bin(n, p_u) < m]/P[Bin(n, p_u) ≥ m]` (the cross-check
proposed in SCI-RES-0004 §3; it agrees).  Neither contains the other: Theorem 11.106 holds
for every exchangeable known part, submodular or not, but only for unions of type classes
on the two sides of a threshold; this theorem holds for every pair of a lower and an
upper set, but needs submodularity.  A common generalisation — a condition under which
the maximal field is the *optimal* closed pair — is known to neither division.
**Both hypotheses are needed** (**[N]**, harness XXIII.6 in its full mode): the field is
optimal to `10⁻¹⁵` in all 22 random instances with both hypotheses, and strictly suboptimal
in 17 of 25 instances with a frustrated known part and in 12 of 22 with a macrostate
that is not monotone (the division reports the same on 900 linear programmes).  In those
cases the extremal residual is a closed pair of Theorem 11.105(b) and the certificate a
transport plan with gains.  On ordered alphabets with site envelopes that are additive
along the order the same holds with step fields; for the discrete envelope on three or
more unordered states (rotamers) the fields give valid but not attained bounds (the
division, SCI-MSG-0011 §2) — there the dual description of Theorem 11.105 is what
remains.  *Prior art:* Holley's inequality (1974) is textbook material; the division did
not find the sandwich stated and expects it to be folklore.

**Theorem 11.107 (a macrostate defined by one coordinate) [P].**  Let `X = Π_i S_i` with a
site-additive envelope `d = Σ_i d_i` and let `A = {x_i ∈ A_i}`, `B = {x_i ∈ B_i}` for one site `i`.
(a) *Additive known part.*  `R⁺(A,B)` is the value of the single-site programme of site `i`
with its own weights: the other sites drop out, and the extremal residual depends on
`x_i` only.
(b) *Pairwise (or any) known part.*  With `R_i⁺[v]` the single-site value for weights `v` on
`S_i`,

    R_i⁺[ marginal weights of x_i ]   ≤   R⁺(A, B)   ≤   max_r R_i⁺[ w(·, r) ],

`r` running over the configurations of the other sites.  The upper bound is certified by
a plan that moves the one coordinate only, `ψ((b,r),(a,r)) = ψ_r(b,a)` — **a certificate that a
pairwise kernel can check site by site, because `w(a,r)/w(b,r)` depends on `r` through the
neighbours of `i` only**.  Both inequalities are strict in general (**[N]**: strict in the
random pairwise instances of harness XXIII.3 and of `experiments/coordinator_checks/ratios/`;
no example is written out here).
*Proof.*  Lower bound: residuals that depend on `x_i` only are admissible iff they are
`d_i`-admissible, and for them the ratio is the single-site ratio with the marginal
weights.  Upper bound: for each `r` take an optimal single-site plan for the weights
`w(·, r)`; the union over `r` is feasible for Theorem 11.105(c) with `λ = max_rλ_r`.  For an
additive known part the conditional weights are proportional to the marginal ones.  ∎
Plans that move a block of sites around `i`, conditional on the boundary of the block,
give a decreasing sequence of certified upper bounds; the exact value for a pairwise
known part on a tree is a natural next question (the programme has exponentially many
variables, the certificate need not).

**Theorem 11.108 (the exponential scale) [P].**  Let the reference measure be exchangeable
on `Sⁿ` (a product measure `π^{⊗n}`, or any known part that is a function of the type), the
envelope site-additive with one site quasi-metric `d₁`, and `A_n`, `B_n` unions of type
classes.  The distance between two type classes is `n·W_{d₁}(Q, P)`, the transport cost between
their types (the transportation polytope with integer marginals has integer vertices).
For every `n`, with `W_P` the weight of the class of type `P`,

    M_n − ln|ℬ_n|  ≤  ln R⁺(A_n, B_n)  ≤  M_n + ln|𝒜_n|,        M_n := max_{P∈𝒜_n} min_{Q∈ℬ_n} [ n·W_{d₁}(Q, P) + ln W_P − ln W_Q ],

`|𝒜_n|, |ℬ_n| ≤ (n+1)^{|S|−1}` the numbers of type classes.  Hence, if the types have the rate
function `I` (`KL(·‖π)` for a product measure; the rate function of §11.23 for a mean-field
known part) and `𝒜`, `ℬ` are the closures of their interiors,

    lim n⁻¹ ln R⁺(A_n, B_n)  =  max_{P∈𝒜} min_{Q∈ℬ} [ W_{d₁}(Q, P) + I(Q) − I(P) ],

**attained by a cone around the type class of the maximising `P`**: the perturbation that
favours `A` most lowers the energy towards the most favourable macroscopic configuration
of `A`, and `B` answers from the configuration from which that is cheapest to reach.
*Proof.*  Theorem 11.106 for the symmetric group and Theorem 11.105(e) on the orbit
space.  ∎
*Numbers.*  Three letters with the law `(0.5, 0.3, 0.2)`, an asymmetric site envelope,
`𝒜 = {mean of h ≥ 1.25}`, `ℬ = {mean of h ≤ 0.5}` for `h = (0, 1, 2)`: the continuum value is `0.4142`
(at `P* = (0.20, 0.35, 0.45)`, `Q* ≈ (0.60, 0.29, 0.10)`); `M_n/n = 0.4210, 0.4062, 0.4081, 0.4114, 0.4124`
at `n = 12, 24, 48, 96, 144`; the bracket [best cone, best-source plan] for `n⁻¹ln R⁺` is
`[0.4742, 0.5471]` at `n = 12` (exact value by the linear programme: `0.4838`), `[0.4298, 0.4490]`
at `n = 96`, `[0.4256, 0.4400]` at `n = 144` — both ends above the limit by `0.33·ln n/n` and
`0.75·ln n/n`.  Cube, band macrostate (`𝒜 = [0.45, 0.55]` between `ℬ = [0, 0.3] ∪ [0.7, 1]`, uniform
measure, `u = 1`): limit `0.2823`; at `n = 50` the exact value `0.2767` is that of the best
cone around a type class.

*What this section does not do.*  (i) The **number of evaluations** needed to certify
`ln[Z(A)/Z(B)]` to a given accuracy — the counterpart of §§11.10–11.19 — is open.  Two remarks
for whoever takes it up.  First, by McShane's lemma the residuals restricted to a
macrostate are exactly the admissible functions on it, and lowering `ln Z_g(A)` by `ε` needs
a change on a constant fraction of the Gibbs measure of `A`, which sampling finds; so the
hard alternatives are again dips, in one of the two macrostates, and their effect is
measured against that macrostate's own weight — a rare macrostate is sensitive to small
dips.  Second, **a macrostate is not a world of its own**: a dip in `A` must be admissible
against the states outside `A` as well, which act as exits — at the interface a dip has
no depth at all — and a dip that straddles the interface raises both weights and may
change the ratio by nothing (centred on the interface of the two halves of the uniform
cube it does).  So the answer is not "the earlier theory on each macrostate with a wall
around it"; that only bounds the sensitivity from above.  For macrostates that are far
apart the coupling disappears (§11.13: the two thresholds add).  (ii) The exact value for a pairwise known part and a
macrostate defined by a counting statistic (a number of contacts): Theorem 11.107(b)
brackets one coordinate only.  (iii) Macrostates that overlap or are defined softly (by
a weight function) are a ratio of two linear functionals as well and have the same
duality with `w` replaced by the two weight functions; not written out.  (iv) Nothing
here is about chains with geometric envelopes; the theorem is as general as its
hypotheses (a finite space, a quasi-metric envelope).

*Harness.*  Block XXIII: XXIII.1 (Theorem 11.105 on random finite spaces with asymmetric
envelopes: the full programme, the bipartite one and the dual agree; closed pairs;
weak duality; one state; the sandwich), XXIII.2 (Theorem 11.106: the programme on `Q_n`
against the programme on types; the maximal field for separated macrostates; a band),
XXIII.3 (Theorem 11.107: exact for additive known parts, strict two-sided bounds for
pairwise ones), XXIII.4 (Theorem 11.108: transport distances between type classes, the
every-`n` sandwich, the bracket by cone and plan, the continuum value); and the
documented refutation DEAD.26 (the extremal residual is not constant on the two
macrostates, and the signed distance to the interface is not admissible).


### 11.29 Local data with a known part: the instance decides (the second question of the Scientific Discovery Division)

§11.27 showed that on the uniform cube free knowledge of all `k`-body marginals of the
Gibbs measure changes no exponent, and the proof used the translations of the cube.
The Scientific Discovery Division asked (SCI-REQ-0001, Q2) what happens with a field,
where there is no such symmetry: *is the exponent with a one-body marginal oracle the
hinted exponent restricted to dips whose excess mass has the one-body marginals of the
reference, and is it strictly below `R^max` of Theorem 11.64?*  Its concern: "on the uniform
cube local data are worthless only because of its symmetry".  The answer has two halves
with opposite signs: **for the class nothing changes — both exponents are those without
the oracle, for every `n` — and at a given instance the oracle does help.**

**Status and history of this section.**  Proposition 11.109 (a criterion) is ours.  Its
first version (thirteenth checkpoint) went on with two conjectures: (e) at the zero
residual the exponent with the oracle is `sup{r_μ(e) : μ̄ = p}`, about `3.5 %` below `R_0(e)` at a
test point; (f) the class exponent is unchanged, by a flat-histogram instance with a
logarithmic well.  Within hours the division's workstream F settled both (SCI-RES-0006,
its report `docs/science/workstreams/SF_REPORT.md` on its branch): **(f) is true, proved by
a different instance and in a stronger form** (Theorem 11.109a); **(e) holds in direction
only** — its formula is an upper bound that no known construction attains, and its two
numbers were wrong (Proposition 11.109b).  Theorem 11.109a and Proposition 11.109b are
the division's; here every step of the proofs given was re-derived, and the finite
statements and all numbers quoted were replicated with our own code
(`experiments/coordinator_checks/oracle_field_review/`; harness XXIII.7).  Not refereed
beyond that; not machine-checked (the division has been asked for a Lean statement).

**Proposition 11.109 (a one-body marginal oracle with a field: the criterion) [P;
coordinator; found independently by the division (its Lemmas 0, 1, 3(i)); harness XXIII.5].**
Cube `Q_n`, reference `π = Bernoulli(p)^{⊗n}`, class `L_u`; besides evaluations of `ψ` the
algorithm is given all one-body marginals
`μ_ψ(x_i = 1)` of `μ_ψ ∝ πe^{−ψ}`, exactly and for free.
(a) *The window.*  For every `ψ ∈ L_u` and every site, `μ_ψ(x_i = 1) ∈ [p₋, p₊]`, `logit p_± = logit p ± u`;
all sites are at the upper (lower) end only for the field `ψ = −u|x| + const` (`+u|x| + const`).
(b) *Invariant instances show one number.*  If `ψ` is invariant under a group of
permutations of the coordinates that is transitive on the sites — the cyclic shift
suffices — all its one-body marginals equal the mean type `κ̄(ψ) := E_{μ_ψ}|x|/n`.
(c) *The matching criterion.*  Let `ψ₀` be symmetric, `D′ ⊊ Q_n` invariant under the cyclic
shift, `ψ₁` the deepest dip of `ψ₀` on `D′`, `Φ := A(ψ₁)/A(ψ₀) − 1 > 0` and `ν ∝ π(e^{−ψ₁} − e^{−ψ₀})` the
normalised excess measure.  Then

    κ̄(ψ₁) − κ̄(ψ₀)  =  Φ/(1 + Φ) · [ type(ν) − κ̄(ψ₀) ],

so the oracle answers identically at `ψ₀`, at `ψ₁` and at the image of `ψ₁` under every
permutation of the coordinates **iff the excess mass of the dip has the mean type of the
null**.
(d) *The lower bound that survives.*  If the criterion holds and `ε < ln(1 + Φ)`, every
`(ε/2, δ)`-correct algorithm with the oracle — adaptive or not, with any hint — makes at
least `(1 − 2δ)/maxdens(D′)` evaluations at `ψ₀`.  For `D′` the union of the `n` cyclic shifts of
a set `D`: `maxdens(D′) ≤ n·maxdens(D)` and `Φ⁺_{ψ₀}(D′) ≥ Φ⁺_{ψ₀}(D)`.
Nothing in (c), (d) uses that `ψ₁` is the *deepest* dip on `D′`: they hold for every member
`ψ₁ ≤ ψ₀` that agrees with `ψ₀` outside `D′` (a remark of the division, and the key to Theorem
11.109a).
*Proof.*  (a) `μ_ψ(x_i = 1)/μ_ψ(x_i = 0) = [p/(1−p)]·Σ_r π(r)e^{−ψ(1,r)}/Σ_r π(r)e^{−ψ(0,r)}` and
`e^{−ψ(1,r)} ∈ e^{±u}e^{−ψ(0,r)}` for every `r`.  (b) The marginals are permuted by the group and
their average is the mean type.  (c) `πe^{−ψ₁} = πe^{−ψ₀} + A(ψ₀)Φ·ν`, so
`μ_{ψ₁} = (μ_{ψ₀} + Φν)/(1 + Φ)`; both `ψ₀` and `ψ₁` are invariant under the cyclic shift, so (b)
applies to both, and the image of `ψ₁` under a permutation `τ` is invariant under the
conjugate shift and has the same mean type.  (d) Theorem 11.22(c) for the alternatives
`ψ₁∘τ`, `τ` a uniform permutation: a fixed point lies in `τD′` with probability
`dens_{|x|}(D′)`, and outside that event the values *and the oracle's answers* coincide with
those of the null.  The union: a point lies in at most `n` shifts, and the slack out of
the union is at least the slack out of each shift (the argument of Theorem
11.79(d)).  ∎
*Brute force* (`Q_10`, `p = ¼`, `u = 1`; harness XXIII.5).  The identity of (c) holds to `10⁻¹²`.
For the cyclic union of the balls of radius 2 around the shifts of a centre of type
`3/10`, the mismatch along the additive instances changes sign at `γ = −0.0187`: there the
oracle's answers at null and alternative agree to `10⁻¹⁵` in every coordinate while `ln A`
differs by `1.136` (at `γ = 0`, where the excess type is `0.2520` against `p = 0.25`: `1.165`).  For
balls of radius 1 around centres of type `5/10` the excess type (`0.41`–`0.48`) is above the
mean type of every additive instance and there is no root: these dips are visible to
the oracle at every such instance.  At this size the symmetrised sets fill whole type
classes, so the illustration is about the oracle's answers, not about exponents.

**Theorem 11.109a (compensation: the class exponents are unchanged by a one-body oracle)
[P; the Scientific Discovery Division, workstream F — Lemmas 2, 3 and Theorems A, B of
SCI-RES-0006; every step re-derived by us; exact enumeration for `n ≤ 10` and exact sums
over joint types up to `n = 3200` with our own code, harness XXIII.7].**  Write `w = e^{−ψ}`; in
the weights the class is a convex cone, closed under sums and pointwise maxima.  Let
`w̃_γ := e^{−γ|x|}/(q + pe^{−γ})ⁿ` be the normalised additive instance (`πw̃_γ = π_γ^{⊗n}`, of mean type
`p_γ`), `c̃_s` the normalised cone weight (`πc̃_s = π_s`, of mean type `c₀(m) := (1−m)p₋ + m·p₊` for a
centre of type `m`), and `ω := p₊ − p₋` the width of the window of Proposition 11.109(a).
(a) *Compensation lemma.*  Let `w` and `w + Δ` (`Δ ≥ 0`, `Δ ≢ 0`) be members that are invariant
under the cyclic shift, with masses `A_w`, `A_Δ` under `π` and mean types `c_w`, `c_Δ`.  If `c_Δ` lies
strictly between `c_w` and an end `p₂ ∈ {p₋, p₊}` of the window, put

    b := A_w (c_Δ − c_w)/(p₂ − c_Δ)  > 0

and let `w̃` be the extreme additive instance of mean type `p₂` (`γ = ±u`).  Then
`w₀ := w + b·w̃` and `w₁ := w₀ + Δ` are members, **all one-body marginals of both equal `c_Δ`**,
they differ exactly on `{Δ > 0}`, and `A(w₁)/A(w₀) = 1 + (A_Δ/A_w)·(p₂ − c_Δ)/(p₂ − c_w)`.
(b) *The excess of a dip sits on the cone law.*  For the dip `max(w̃_γ, e^r c̃_s)` of depth
`r > 0` at a centre of type `k/n` on the additive base `γ`, the excess
`Δ_{s,r} = (e^r c̃_s − w̃_γ)₊` has mass `E_{k,r} ∈ [e^r − 1, e^r]` and mean type `c_{k,r}` with
`|c_{k,r} − c₀(k/n)| ≤ 1/(e^r − 1)`.
(c) *Adaptive algorithms, every `n`.*  Let `|γ| ≤ u`, `1 ≤ k ≤ n − 1`, `m = k/n`,
`ω_m := ω·min(m, 1−m)`, and `r` with `κ := ω_m − 1/(e^r − 1) > 0`; put `β := ω/κ`.  There are an
end `p₂` of the window and `b ∈ [0, β]` such that at the instance
`ψ₀ = −ln(w̃_γ + b·w̃) ∈ L_u` every randomised algorithm with the exact one-body oracle —
adaptive, with any hint — that is `(ε/2, δ)`-correct on `L_u` for some
`ε < ln(1 + (e^r − 1)/(1 + β))` makes in expectation at least

    (1 − 2δ) / (n·H_{k,r})   ≥   (1 − 2δ)·e^{−tr}·ρ_t(m; γ)^{−n} / (n(n+1))        for every t ≥ 0

evaluations, where `H_{k,r}` is the largest fraction of the centres of type `k/n` whose dip
contains a given point and `ρ_t(m; γ) = max_a[(1−m)(π_0(a)/π_γ(a))^t + m(π_1(a)/π_γ(a))^t]` (`π_0`, `π_1`
the two letter laws of the cones; `min_m ρ_t(m; γ) = e^{−F(γ,t)}`, the game function of Theorem
11.59).  In particular, for every `ε > 0` and `0 ≤ t ≤ 1`, with a suitable `r`: at least
`(1 − 2δ)·e^{−tε}·ρ_t(m; γ)^{−n}/(C_m·n(n+1))` evaluations, `C_m = 1 + 2/min(m, 1−m) + 2/ω_m` — to be
compared with `(1 − 2δ)e^{−tε + nF(γ,t)}` without the oracle (Theorem 11.59(a)).
(d) *Non-adaptive algorithms, every `n`.*  Let `s` be a centre of type `m = k/n`, `0 < q < 1`,
and `A_t ≤ 1` the mass of the normalised cone truncated at its type-wise upper
`q`-quantiles (Theorem 11.61(a)).  If `A_t < ω_m/2`, every non-adaptive algorithm with the
oracle that is `(ε/2, δ)`-correct for some `ε < ln(1/A_t) − ln(2/ω_m)` makes at least
`(1 − 2δ)/(n·q)` evaluations.
(e) *Hence*, with the upper bounds of Theorems 11.64 and 11.61, which ignore the oracle:
**for `0 < ε₁ < E` the exponent of adaptive algorithms with a free exact one-body oracle is
`R^max(ε₁)` and that of non-adaptive ones is `θ_na(ε₁)`; at every bounded accuracy they are
`h` and at least `a`** — the values without the oracle.  The hard instance is
`−ln(w̃_{γ*} + b·w̃_{∓u})`: its Gibbs measure is a mixture of two product measures,
`(π_{γ*}^{⊗n} + b·π_{∓u}^{⊗n})/(1 + b)` — an ensemble whose one-body averages equal those of the same
ensemble with a hidden dip added.
*Proof.*  (a) The mean type of `πw₀` is `(A_wc_w + b·p₂)/(A_w + b)`, which equals `c_Δ` by the
choice of `b`; `μ_{w₁}` is a mixture of `μ_{w₀}` and the normalised excess, both of mean type
`c_Δ`; `w₀` and `w₁` are invariant under the cyclic shift, so each of their one-body marginals
is the mean type (Proposition 11.109(b)); they are members because the class is a cone in
the weights; `A(w₀) = A_w + b = A_w(p₂ − c_w)/(p₂ − c_Δ)`.
(b) `π·Δ_{s,r} = e^rπ_s − min(e^rπ_s, π_γ^{⊗n})`.  With `J ∈ [0, 1]` the mass of the minimum and `c_J` its
mean type: `E = e^r − J` and `E·c = e^rc₀ − Jc_J`, so `c − c₀ = J(c₀ − c_J)/(e^r − J)`.
(c) For a centre `s` of type `k/n` let `Δ̄_s` be the average of the excesses `Δ_{σ^js, r}` over the
`n` cyclic shifts `σ^j`.  Then `w̃_γ + Δ̄_s` is an average of members, hence a member; it is
invariant under the shift; its excess has mass `E_{k,r}` and mean type `c_{k,r}`, and support
the union of the `n` shifted supports.  By (b), `c_{k,r}` lies in the window at distance at
least `κ` from both ends (`c₀(m)` is at distance at least `ω_m` from them).  Apply (a) with
`w = w̃_γ`, `Δ = Δ̄_s` and `p₂` the end of the window beyond `c_{k,r}` as seen from `p_γ`:
`b = (c_{k,r} − p_γ)/(p₂ − c_{k,r}) ≤ ω/κ`, **the same `b` for every centre of the type**.  So the
null `w₀ = w̃_γ + b·w̃` and the alternatives `w₀ + Δ̄_s` are members with the same answers
`(c_{k,r}, …, c_{k,r})` of the oracle, and `ln A` differs by `ln(1 + E_{k,r}/(1 + b)) > ε`.  On the
event that no evaluated point lies in the support of `Δ̄_s` the run at the null and the run
at the alternative coincide — the oracle's answers included — so that support is hit
with probability at least `1 − 2δ` (Theorem 11.22(c)); a point lies in the supports of at
most `n·H_{k,r}·|T_k|` alternatives.  The second form: the uniform law on the centres of type
`k/n` is `Bernoulli(m)^{⊗n}` conditioned on an event of probability at least `1/(n+1)`, and for
independent centre letters Markov's inequality gives
`P(Φ_s(x) < r) ≤ e^{tr}ρ_t(m; γ)ⁿ` for `Φ_s(x) = Σ_i ln(π_γ(x_i)/π_{s_i}(x_i))`, whose sublevel set is
the support of the dip.  The last display: `r := ln(1 + max{2/ω_m, (1 + 2/min(m, 1−m))(e^ε − 1)})`
plus a little.
(d) Let `c̄_s`, `c̄_s^{tr}` be the averages over the cyclic shifts of the normalised cone and of
its truncation; both are members and invariant.  (a) with `w = c̄_s^{tr}` (mass `A_t`, mean type
`c_t`) and `Δ = c̄_s − c̄_s^{tr} ≥ 0`: since `c₀(m) = A_tc_t + (1 − A_t)c_Δ`, `|c_Δ − c₀(m)| ≤ A_t`, so `c_Δ` is in
the window at distance at least `ω_m/2` from its ends, and
`A(w₁)/A(w₀) ≥ (ω_m/2)/A_t`.  All the pairs, over the centres of the type, have the same
answers of the oracle, so the law of the evaluated set is the same for all of them
(Theorem 11.45(a) with the oracle's answer as a constant); a fixed point lies in the
difference set of a random centre's pair with probability at most `n·q`.
(e) (c) at a saddle `(γ*, t*, m*)` of `R^max` (lattice approximation of `m*` costs a constant
factor), and (d) with Theorem 11.61(c).  ∎

*Why this works where our well did not.*  Our first argument modified the flat-histogram
instance by a pointwise *maximum* (a well) and took its deepest dips: the excess then
moves with the tuning parameter, so the matching equation of Proposition 11.109(c) needs
a continuity argument and a concentration statement that we could not prove, and the
well costs a polynomial factor (whence "`ε ≫ ln n`").  The division adds a *sum*: the excess
`Δ̄_s` is fixed, the null is moved by an admixture of an extreme additive instance, and the
matching equation is **linear in the weight `b`** — no homotopy, no concentration, a loss
of a factor `(1 + b)·n`, every `n` and every accuracy, and non-adaptive algorithms as well.
*The trap* recorded in the first version (and in `DEAD_ENDS.md` D54 item 3) stays a trap:
along the additive instances `γ|x|`, `|γ| ≤ u`, the mismatch of the *deepest dip* vanishes at both
ends `γ = ±u` without changing sign (there the instance has no slack in one direction).
It does not arise here, because the extreme instance enters as an admixture, not as the
end of a homotopy.  The division had itself expected (f) for a wrong reason — that the
hardest additive instance is self-consistent — and withdrew it: the excess of a dip has
the type of the cone law, not that of the dip's rim.
*Numbers* (**[N]**, ours; `(p, u) = (0.3, 1)`, `e = 0.3E`, exact sums over joint types).
`R^max = 0.012210`; the exponent `n⁻¹ln[1/(n·H_{k,r})]` of the bound of (c) at the saddle is
`0.00069`, `0.00889`, `0.01044` at `n = 400, 1600, 3200` (the division, with its choice of `r`:
`0.010542` at `n = 3200`): it approaches `R^max` from below, the difference being the factor `n`
of the cyclic union and the usual polynomial corrections.

**Proposition 11.109b (at an instance the oracle helps: the tilt inequality and a
bracket) [(a) P; (b) P given Theorem 11.78(b); (c) a proof sketch of the division's,
supported by its exact sums — of it we re-derived the Laplace step only; (d) and all
numbers N — the Scientific Discovery Division, workstream F, its Propositions C, D; (a)
re-derived and the numbers at the test point re-computed by us, harness XXIII.7].**  For an additive instance `ψ_γ` let `R_γ^{orc}(e)` be the exponent of the
least cost at `ψ_γ` of algorithms with the oracle that are correct on the class and are
given `γ` as a hint; `θ = ln(q/p)` is the field and `R_γ(e; θ)` the hinted exponent without the
oracle at that field.
(a) *Tilt inequality.*  If `ψ′ ∈ L_u` has the one-body marginals of `ψ_γ`, then for every real
`λ`, with the reference `π^{(λ)} := Bernoulli(p^{(λ)})^{⊗n}`, `logit p^{(λ)} = logit p + λ`, and the same
functional `A^{(λ)}` for it:

    ln A^{(λ)}(ψ′) − ln A^{(λ)}(ψ_γ)  ≥  ln A(ψ′) − ln A(ψ_γ) − n·c_γ(λ),        c_γ(λ) := ln(1 − p_γ + p_γe^λ) − λp_γ ≥ 0.

*Two matched instances are still far apart when the field is changed.*
(b) *An algorithm that uses the oracle.*  Given the hint `γ`: reject it if the oracle's
answers are not `(p_γ, …, p_γ)`; otherwise run the spot check of the hint with samples from
`½π_γ^{⊗n} + ½·`(uniform on types, uniform inside each type class).  An alternative that passes
the first test is matched; by (a) it differs from `ψ_γ` by at least `n(e − c_γ(λ))` in `ln A^{(λ)}`
for every `λ`, so by the isoperimetric theorem *at the shifted field* its difference set
is hit often enough:

    R_γ^{orc}(e)  ≤  U_γ(e) := inf_λ R̄_γ(e − c_γ(λ); θ − λ),

where for negative arguments `R̄(e′) = max(R(e′), −e′)` as in Theorem 11.78(b), which applies
because an additive instance at any field is a symmetric instance of a function-of-type
known part.  Since `c_γ′(0) = 0` while `∂_θR_γ ≠ 0` for `p ≠ ½` (**[N]**: in every case computed),
`U_γ(e) < R_γ(e)`: **for `p ≠ ½` the oracle strictly lowers the exponent of the zero residual**,
and its threshold.
(c) *Matched alternatives, from below.*  For a centre of type `m` and the shell of points
with the fractions `v₁`, `v₀` of ones on the centre's ones and zeros, the smallest member
with a prescribed lift on the shell is a dip *around the shell*; its excess mass sits on
that shell iff `v₀, v₁ ∈ [p₋, p₊]` (the Laplace principle for `π·e^{−u·d(·, shell)}`: a block law stays
at `v` iff `|logit v − logit p| ≤ u`; otherwise the mass sits on the nearest shell inside the
window).  Mixing two such families whose excess types bracket `p_γ` — one linear equation,
as in Theorem 11.109a(a) — gives matched alternatives, and

    R_γ^{orc}(e)  ≥  V_γ(e) := sup{ f(m, v₀, v₁; e) :  v₀, v₁ ∈ [p₋, p₊],  (1−m)v₀ + m·v₁ = p_γ },
    f(m, v₀, v₁; e) := min{ I(M, V′) :  Σ_φ M(φ)[ u|v′_φ − v_φ| + γ(v_φ − v′_φ) ] ≤ e + D(V‖π_γ|M) }.

(d) *The formula of our first version over-counts.*  The supremum of `f` over all profiles
of mean type `p_γ`, *without* the window — our `sup{r_μ(e) : μ̄ = p}` — coincides with the tilt
bound `U_γ(e)` (to six digits in the cases computed, as Lagrangian duality suggests), and
its maximiser has a block law outside the window: for that profile the excess mass does
not sit on the profile class, "`μ̄ = p`" is not "the excess mass has type `p`", and the dip is
visible to the oracle.  So

    V_γ(e)  ≤  R_γ^{orc}(e)  ≤  U_γ(e)  <  R_γ(e),

and which end is the truth is open (the division conjectures the lower; what is missing
is an isoperimetric upper bound that knows the window).  Restricting further to plain
cone dips whose centre type solves `c₀(m) = p_γ` — the condition quoted in the first version
as "the division's" — gives a valid lower bound that is far from the truth.
*Proof of (a).*  `A^{(λ)}(ψ) = (q + pe^λ)^{−n}·E_π[e^{λ|x|}e^{−ψ}]` for every `ψ`.  At `ψ_γ` the expectation is
`A(ψ_γ)(1 − p_γ + p_γe^λ)ⁿ`.  At `ψ′` it is `A(ψ′)·E_{μ_{ψ′}}e^{λ|x|} ≥ A(ψ′)e^{λnp_γ}` by Jensen's inequality,
because the mean type of `μ_{ψ′}` is `p_γ`.  Divide.  ∎
*At the test point of the first version* (`p = ¼`, `u = 1`, `e = 0.02`, zero residual; window
`[p₋, p₊] = [0.1092, 0.4754]`; **[N]**, ours, agreeing with the division's to the digits shown
except where noted): `R_0(e) = 0.013669`, at cones of centre type `0.4555` (first version:
"`0.0134`", the best of a grid of seven types); `U_0(e) = 0.012941` at `λ = −0.148`, equal to the
unrestricted supremum, whose maximiser `(m; v₀, v₁) = (0.450; 0.0956, 0.4386)` has `v₀ < p₋` (first
version: "`0.0129`", there offered as the value); `V_0(e) = 0.012635` with one block at `p₋` (the
division: `0.012630`); plain cone dips of the forced centre type: `0.0057`.  **The oracle
lowers the exponent of the zero residual by between `5.3 %` and `7.6 %` there** (first version:
"about `3.5 %`").  For strong fields it removes much more: at `(p, u) = (0.1, 2)`, `e = 0.2E_0`, the
division finds `0.0154 ≤ R_0^{orc} ≤ 0.0163` against `R_0 = 0.0268`, and beyond `e = 0.7E_0` the whole
exponent (its table; not re-computed by us).

*For `k`-body marginals with a field* the route of Theorem 11.109a needs `k` matching
conditions instead of one — the first `k` factorial moments of the type under the excess
measure and under the null — and symmetric families of size polynomial in `n`.  The
division (its Proposition E; **not checked by us**) reports: for `k = 2`, with nulls that are
mixtures of additive instances, a single family of dips can never be matched (its excess
lies below the parabola `c₂ = c₁²`), two centre types about `√n` apart can, and an exact
construction at `n = 13` under the affine group agrees in all `13 + 78` marginals; `k ≥ 3` is
its conjecture; with all marginals of every order known only to an absolute precision
`τ` the adaptive bound loses a factor polynomial in `1/τ`.  The design families needed
exist (Kuperberg–Lovett–Peled, Theorem 1.3 — read by the division, not by us).

*What this says about the division's concern.*  With a field, local averaged data are
still worthless against the worst instance of the class, but for a different reason
than on the uniform cube: not because symmetric hiding places exist for every dip, but
because the class contains instances — mixtures of two product ensembles — whose own
averages already equal those of the same instance with a hidden dip.  At an instance
that the user believes in — the known part itself, `ψ = 0` — the data do exclude dips: a
few per cent of the exponent for weak fields, most or all of it for strong ones.  The
meaningful statement about measurements is therefore instance-wise, as the division
suspected.


### 11.30 Sup-norm remainders around a sampleable known part: the typical norm sets the bracket, the floor sets the bill

*Origin.*  The Scientific Discovery Division measured, on a rigid grid model of short
polyalanine chains (its message SCI-RES-0002; a pilot, **[M]** in its labels, none of whose
numbers is a certified constant), that a continuum-solvent term is far outside the per-site
classes of this report — `βc_i = 12–53`, growing with the chain — while it stays within a few
`k_BT`, in supremum norm, of an explicitly pair-additive function, within a fraction of `k_BT`
in root mean square, and has a Jensen gap of 2–3 nats where the class bound is 71–178.  Its
request P-T3, ranked first among its proposals for new theory (SCI-MSG-0010): *is there a
certificate theory with an exponential-moment bound under the Gibbs measure of the known
function in place of a sup bound — what must be certified, and can it be estimated by
sampling with a guarantee?*  This section answers it for the simplest class in which the
question makes sense.  The mathematics is elementary and classical in spirit (free-energy
perturbation, Zwanzig 1954; Monte Carlo integration); what it adds to this report is a class
in which the cost of `ln Z` **does not depend on the size of the system**, with matching
bounds, and the exact form of the one assumption that sampling cannot replace.  Coordinator's
own work, in answer to that request; **not refereed**.

*Setting.*  `X` finite; energy `E = f̂ + r` in units of `k_BT`.  The function `f̂` is *known and
tractable*: its partition function `Z₀` is known and independent samples from its Gibbs
measure `π ∝ e^{−f̂}` can be drawn exactly (a product measure; a chain with nearest-neighbour
couplings, by the elimination rules of §3.4; any known part of bounded treewidth).  The
remainder `r` is evaluated on demand and is known a priori only through pointwise bounds,

    lo(x) ≤ r(x) ≤ hi(x)      (the box class 𝓑;   lo ≡ −ρ₋, hi ≡ ρ₊:  one-sided sup norms).

`Z(r) = Σ_x e^{−f̂(x) − r(x)}`, so `Z(r)/Z₀ = E_π e^{−r}`.  At an instance `r` the *dip weight* of
a point is `dip(x) = π(x)(e^{−lo(x)} − e^{−r(x)})` and its *bump weight*
`bump(x) = π(x)(e^{−r(x)} − e^{−hi(x)})`: what the partition sum can gain or lose there.  Their
totals are `U = (Z(lo) − Z(r))/Z₀` and `V = (Z(r) − Z(hi))/Z₀`.  Algorithms are
`(ε/2, δ)`-correct for `ln Z` on the class, as everywhere in §11.9–§11.10.

**Theorem 11.110 (box classes) [(a), (b), (e) P; (c), (d) V] (`BoxClass.lean`).**
(a) *What must be certified.*  `ln Z(r) − ln Z₀ = ln E_π e^{−r}`, and

    −E_π r  ≤  ln E_π e^{−r}  ≤  −E_π r + L(w),      L(w) = ln((e^w − 1)/w) − 1 + w/(e^w − 1)  ≤  w²/8,

`w = sup hi − inf lo` the width of the box; `L(w)` is the largest Jensen gap of a random
variable of range `w`, attained by a two-point law (lower end: `jensen_bracket` **[V]**).  With
the known function fixed, the free energy is therefore determined by two numbers of the
remainder under `π`: its mean — a linear functional, the Gibbs–Bogoliubov bound — and its
centred cumulant generating function `K = ln E_π e^{−(r − E_π r)} ∈ [0, L(w)]`.  A typical-norm
statement about the remainder is a bound on `K`.
(b) *Deterministic certificates cost the entropy of the known part.*  After evaluations on
`Q` the possible values of `ln Z` fill exactly the interval between "ceiling off `Q`" and
"floor off `Q`".  At the centre of a constant box (`r ≡ 0`: the known function is right) an
`ε`-certificate must therefore contain all but the fraction
`q* = (e^ε − 1)/(e^{ρ₋} − e^{ε−ρ₊} + e^ε − 1)` of the mass of `π`, and the most probable states
do it with the fewest evaluations: for a product measure or a chain that is
`e^{S(π)(1+o(1))}` states.  The class has no geometry — an evaluation says nothing about any
other point — so there is nothing for a kernel to exploit.
(c) *A sampling certificate* (`Zw_sub_le_dip`, `Zw_sub_le_bump`, `detect_ge`,
`box_spotCheck_correct`).  A member of the box that differs from `r` only on `D` raises the
partition sum by at most the dip weight of `D` and lowers it by at most its bump weight.
Hence every member with `|ln Z′ − ln Z| > η` differs from `r` on a set of probability at least

    p(η) = min{ 1,  ½ · min( (e^η − 1)·Z/(Z(lo) − Z),  (1 − e^{−η})·Z/(Z − Z(hi)) ) }

under the sampler `q = ½·dip/U + ½·bump/V`, and the spot check of the hint `r` with
`N = ⌈ln(1/δ)/p(ε/2)⌉` independent samples of `q` is `(ε/2, δ)`-correct for `ln Z` **on every
class contained in the box**, with at most `N` evaluations at the hint.  Since
`Z − Z(hi) ≤ Z`:

    N  ≤  ⌈ 2 ln(1/δ) · max( (Z(lo)/Z(r) − 1)/(e^{ε/2} − 1),  1/(1 − e^{−ε/2}) ) ⌉ .

(d) *Lower bound for every algorithm* (`logZ_dipAlt_gt`, `box_expected_queries_ge`).  A set
whose dip weight exceeds `(e^ε − 1)·Z(r)/Z₀`, lowered to the floor, changes `ln Z` by more than
`ε`; if there are `k` pairwise disjoint such sets, every randomised algorithm that is
`(ε/2, δ)`-correct on the box makes at least `(1 − 2δ)k` evaluations on `r` in expectation.
If no single point has that much dip weight, a greedy packing gives
`k ≥ ⌊(Z(lo)/Z(r) − 1)/(2(e^ε − 1))⌋`.
(e) *Consequences.*  For instances at which no single state can change `ln Z` by `ε`:

    (1 − 2δ) ⌊ (Z(lo)/Z(r) − 1) / (2(e^ε − 1)) ⌋   ≤   min_alg E|Q(r)|   ≤   ⌈ 2 ln(1/δ) max( (Z(lo)/Z(r) − 1)/(e^{ε/2} − 1), 1/(1 − e^{−ε/2}) ) ⌉ ,

so **the cost of certifying a free energy in a box class is the Boltzmann factor of the
free-energy distance from the instance to the floor of the class, divided by the accuracy** —
`Z(lo)/Z(r) = E_{π_r} e^{r − lo}`, the functional `E_π e^{Λ}` of Theorem 11.26 with the local soft
gap `Λ = r − lo` — and the two bounds differ by a factor that depends on `ε` and `δ` only.  At
the centre of a constant box this is `Θ((e^{ρ₋} − 1)/ε)`: the number of states, the entropy of
`π`, the ceiling `ρ₊` and every per-site constant are absent.  The sampler there is `π` itself.

*Three readings.*  (1) **The floor is the one assumption that sampling cannot replace.**
The lower bound (d) uses only dips and grows without bound as `ρ₋ → ∞` (until it reaches the
number of states): however many samples agree with the known function, a deep well of
`π`-mass `1/N` may have been missed, and a bound on how far *below* the known function the
truth can lie is what makes `N` finite.  A constant that is fitted or sampled is not such a
bound (the science division's pilot: sup-norm remainders estimated on samples were exceeded
on held-out conformations by factors up to ten).  (2) **Free energies are cheap from above
and expensive from below.**  The lower end of (a) is a mean: by Hoeffding's inequality
**[K]**, `⌈w² ln(1/δ)/(2ε²)⌉` samples of `r` under `π` certify `ln Z ≥ ln Z₀ − r̄ − ε` with
probability `1 − δ`, a number polynomial in the width; everything beyond that bound — the
cumulant `K` — is paid for at the rate (e).  This is the familiar asymmetry of free-energy
perturbation, here with matching bounds.  (3) **Minima do not share the benefit.**  For
`min(f̂ + r)` one hidden state suffices, sampling does not help, and a certificate must
contain every state with `f̂(x) + lo(x) < min(f̂ + r) − ε` — in a constant box, all states of
the known function within `ρ₋` of the optimum.  In this class a free energy at positive
temperature is cheaper than a minimum, by randomisation.

**Corollary 11.111 (a sup-norm bound caps the cost of every class) [P from V].**  Let `𝒞` be
any class of remainders and `𝒞_ρ = 𝒞 ∩ 𝓑`.  At a hint `r ∈ 𝒞_ρ` the spot check with the mixture
of the sampler of Theorem 11.110(c) and any sampler that is valid for `𝒞` (for a first-order
class: the thermal sampler of Theorem 11.26) is correct on `𝒞_ρ` with at most twice the
smaller of the two sample sizes.  On the cube with per-site slope `u = 1` and the additional
bound `|g| ≤ 3 k_BT`, the cost at the zero residual is at most `1088` evaluations at
`ε = 0.2`, `δ = 0.05` for every `n`, where the first-order class alone costs
`e^{n·0.0291 − o(n)}` (Theorem 11.25): from `n ≈ 240` on the sup-norm bound is the smaller one
(harness XXIV.4).  The hard alternatives of a first-order class are dips of extensive depth;
a sup-norm bound removes them.

*Without a hint.*  The spot check verifies a proposed remainder.  Without one, the sample
mean of `e^{−r(x_i)}`, `x_i` independent draws from `π`, with
`m = ⌈3 e^{w} ln(2/δ)/(1 − e^{−ε/2})²⌉` samples is `(ε/2, δ)`-correct on the whole box
(multiplicative Chernoff bound for a variable in `[0, e^{ρ₋}]` with mean at least `e^{−ρ₊}`
**[K]**): worst case `e^{w}/ε²`, which is the right order at members whose weight is dominated
by rare deep dips.  Instance-wise, an empirical Bernstein inequality (Maurer–Pontil 2009,
Theorem 4 — **[K]**, the form confirmed from a search summary of the paper, the paper not
opened: `docs/prior_art/L10_box_classes.md`; its coverage is tested by simulation in harness
XXIV.5) turns the same samples into a bracket for `E_π e^{−r}` of half-width

    √(2 V̂ ln(4/δ)/m)  +  7 (e^{ρ₋} − e^{−ρ₊}) ln(4/δ) / (3(m − 1)),

`V̂` the sample variance of `e^{−r}`: **the typical norm of the remainder sets the width of the
bracket, the floor of the class sets the number of samples below which nothing is
certified.**  The naive interval "mean ± two standard errors" is not a certificate: at a
member with a rare deep dip the sample variance is zero with probability close to
`e^{−mp}` (harness DEAD.28; `DEAD_ENDS.md` D56).

*What this does and does not say about the measured residual.*  With the science division's
numbers as an illustration: if the remainder of its 36-type pair-additive fit at five
residues (`0.26` kcal/mol RMS, `2.2` kcal/mol maximum, i.e. `3.7 k_BT`) had a *certified* floor
of `3.7 k_BT`, then `ln Z` would be certified within `0.1` nats at confidence `0.95` by about
`2 ln 20 · e^{3.7}/(e^{0.05} − 1) ≈ 4.7·10³` evaluations, whatever the chain length; with a
floor of `15.6 k_BT` (its largest remainder of an explicitly pair-additive function, eight
residues) by about `7·10⁸`.  Three things are missing between this and a statement about a
molecule, and the theorem says which: (i) a certified floor, by analysis of the functional
form of the remainder — not by fitting; (ii) exact sampling from the known function, which
needs a known part that is tractable *in the chosen variables* — an atom-pair-additive
function is not nearest-neighbour in backbone torsions, so either the tractable part is
smaller and the box wider, or the variables are different.  (The division has since made
the measurement it ranked first, SCI-MSG-0015: in rotamer variables on a fixed backbone
the vacuum force field is *exactly* residue-pairwise and the solvent term is pairwise to
`10⁻²`–`10⁻¹` kcal/mol for neutral side chains.  A pairwise function can be sampled exactly
when its interaction graph has small treewidth, not in general; and the width of the box
depends on how the energy is split between known part and remainder — moving a pairwise
term from one to the other changes it — which is the division's observation for the
second-order interface, and holds here for the same reason.)  (iii) The result concerns
`ln Z` of the whole domain at positive temperature, not minima, and not differences of
macrostates — for which §11.28 gives the range but not the cost.

*Prior art* (`docs/prior_art/L10_box_classes.md`: three searches by us at the level of
search summaries, no full text opened; a review has been requested from the science
division).  Free-energy perturbation and its one-sided convergence are textbook material
(Zwanzig 1954; the exponential-averaging bias).  *How many samples the exponential average
needs to converge at a given pair of ensembles* is known: of the order of the exponential
of the dissipation of the reverse process (Jarzynski 2006), i.e. of a relative entropy
(Chatterjee–Diaconis 2018, cited for §11.20).  That is a statement about an estimator at
one instance.  The statement here is about a **certificate against a class**, and the two
differ exactly where it matters: at the centre of the box the exponential average has
zero variance and converges with one sample, and certifying its value still costs
`(e^{ρ₋} − 1)/ε` evaluations.  The identity and the two-point bound in (a) are Hoeffding's
lemma in its sharp form.  For the *sampling* model — an algorithm that can only draw
independent copies of a `[0,1]`-valued variable — the optimal number of samples for a
relative `(ε, δ)`-approximation of its mean is `Θ(max(σ², εμ)·ln(1/δ)/(ε²μ²))` (Dagum, Karp,
Luby, Ross 2000: optimal up to a constant for every variable, per the abstract; **the
displayed form of the rate is from memory**; a later note reports a gap in the proof of
that paper's stopping-rule theorem, which we do not use), whose zero-variance case is the
rate `1/(εμ)` of (e).  The model here is different in that the algorithm knows `π` and
chooses its points — so the lower bound needs the packing argument and the hypothesis on
single states — but the answer is the same, and we claim no novelty beyond the placement
of the statement in this framework: a class without geometry, in which Theorems 11.24 and
11.26 are tight with explicit constants, next to the classes of §§11.4–11.27 in which the
cost is exponential in the size of the system.

*Harness.*  Block XXIV: XXIV.1 (the Jensen bracket and its two-point extremum; the exact
range after evaluations; the mass a deterministic certificate needs), XXIV.2 (dip and bump
weights bound the change of `Z`, with equality at the ends of the box; the detection
probability — in the linear relaxation between `p` and `2p`, both ends attained; the spot
check), XXIV.3 (the lower bound and the size-free bracket at four sizes from `4·10³` to
`4·10⁵` states), XXIV.4 (Corollary 11.111 on the cube), XXIV.5 (coverage of the empirical
Bernstein bracket; a simulation), DEAD.28 (the naive interval), with 15 mutations.


## 12. Strongest unresolved questions, and what a publication would need

1. **The exponent theorems (11.9, 11.15).**  The lower bounds are machine-checked for every `n`;
   the upper bounds are paper proofs resting on the type covering lemma.  A publication needs
   (a) a careful write-up of the credit-distortion reduction and of the heterogeneous case
   (sites of unequal type; only finitely many types are covered here); (b) the second-order
   term (the polynomial prefactor visible in the layer counts); (c) interacting known parts.
   For a chain with pairwise `E₀`, Hamming envelope `c` and zero residual the partition-function
   bound gives, by the Gibbs variational principle,
   `n⁻¹ ln N ≥ max_t [p_E(t) − ln(1+(k−1)e^{−tc})] = sup_ν [h(ν) − h_b(δ_ν) − δ_ν ln(k−1)]`,
   `δ_ν = e_ν/c`, the supremum over stationary measures `ν` with `δ_ν ≤ (k−1)/k` (the constraint
   `t ≥ 0`; without it the right-hand side can exceed the left), entropy rate `h(ν)` and mean
   excitation energy `e_ν` per site, `p_E` the pressure (computable from the transfer matrix).
   This is the *Shannon lower bound* of the rate–distortion function of the process `ν` at
   distortion `δ_ν`, and we expect the true exponent to be `sup_ν R_ν(δ_ν)` — equal to the bound
   when the optimal `ν` is below its critical distortion, as for binary symmetric Markov sources
   (Gray 1970), and strictly larger otherwise.  None of this is proved here, and it is further
   from proof than it sounds: type covering for Markov types with a distortion budget fixed by
   the pair marginal is not an off-the-shelf lemma (second referee).  For independent sites the
   same remark explains when the Boltzmann choice of weights in Theorem 11.8 is optimal
   (two-state sites with zero residual: always) and when general weights are needed.
   *Added in cycle 9:* for homogeneous chains the exponent is `sup_ν R_ν(e(ν))` (Theorem 11.40),
   by a proof that avoids Markov-type covering; the Shannon lower bound above vanishes on a
   window (Proposition 11.41).  Open: a computable form of the exponent below the critical
   distortion; inhomogeneous chains; the finite-temperature exponents of a chain.
   (c') the exponent of Theorem 11.15 for exponentially small accuracies `ε_n = e^{−λn}`: between
   `max(R_β, max{H(Q) : KL(Q‖π) < λ})` and `max_Q R(Q; s, (KL(Q‖π) − λ)₊/β)`.
   (d) a careful comparison with the source-coding literature on exponential moments
   of distortion and on guessing (Merhav 2011; Arikan–Merhav 1998): Theorem 11.15 is a
   corollary of the former, read here only in part; whether the zero-temperature statement with
   its credit distortion and the dichotomy also appear there in some form is not settled.
2. **Algorithms.**  On additive instances the exponent `R*` is reached without knowing the
   residual (learn-then-cover), and no algorithm, randomised or not, does better
   (Theorem 11.23).  Open:
   (a) instances that are only approximately additive — the cover computed from the
   interpolant must be robust to the pair remainder;
   (b) **the randomised exponent at finite temperature.**  On the cube at the zero residual
   it is known in every accuracy regime (Theorem 11.25).  At additive instances of identical
   sites it is `R^gen_β(ε₁)` (Theorem 11.27: lower bound for every `n`; upper bound by a paper
   proof that an independent referee checked).  For a publication the proof needs a careful
   write-up and a machine check of at least its single-letter part; the relation to the
   fixed-measure isoperimetric theorem (is the black-box bound always equal to the game
   value?) is open, as are sites of several types, exponentially small accuracies beyond the
   cube, non-additive instances and interacting known parts;
   (c) **thresholds.**  Settled for identical independent sites: at additive instances
   (Theorem 11.28(c)) and, without a hint, for the whole class and every alphabet (Theorem
   11.28(d): the smallest oscillation of the tilted site pressure; closed form for two-state
   sites in (e); finitely many site types by averaging).  Open: the cost of non-additive
   instances below the class threshold; chains as known parts — the one-reference sandwich
   and the minimax identity hold there too, but the width is no longer a single-site
   quantity (workstream B gives a lower threshold by a transfer-matrix formula and a
   conjecture for the upper half);
   (d) **algorithms without a hint** on the cube class.  *Settled at the level of exponents
   in cycle 10* (§§11.16, 11.18, 11.19): non-adaptive algorithms have the exponent
   `θ_na(ε₁) = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ ε₁}` (and `a = KL(p_u‖½)` at every fixed accuracy), adaptive
   ones the hinted exponent `θ_hint(ε₁) = KL((Λ₁+ε₁)/u ‖ ½)` — at extensive accuracies (Theorem
   11.54, refereed) and at every bounded accuracy down to `e^{-o(n)}` (`h = θ_hint(0)`, Theorem
   11.58, refereed: R8).  Open: (i) **below the exponential scale** — with a hint the cost
   at the zero function is `2ⁿ/|B(n,k*)|` up to a polynomial factor; without one the upper
   bound is `e^{nh + o(n)}` with an unquantified `o(n)` (heuristically not better than `n^{3/4}`).
   Can `e^{nh + O(√n)}`, or `poly(n)·2ⁿ/|B(n,k*)|`, be reached without a hint, or is there a
   lower bound `e^{nh + ω(log n)}`?  Any such bound must come from non-flat instances (on the
   flat one the doubling two-sample bracket stops at the hinted cost up to a polynomial
   factor).  (ii) **Depth** — `k` nested levels have the exponent `τ_k > h` at bounded accuracy,
   `(τ_k − h)/a ≈ 0.65/k²` numerically; is there a lower bound for a restricted class (a bounded
   number of levels, or of rounds of adaptivity) that matches `τ_k`?  **Rounds** (§11.24;
   refereed, SCI-REV-0003): every nested algorithm with fixed levels needs a number of
   rounds independent of `n`; the two-round exponent is at least `0.359a` (`liminf`) and at
   most `0.624a` (`limsup`) at `u = 1` — strictly between the fixed-sample and the adaptive
   exponent, asymptotically: no separation at a finite size is shown — and **whether
   three rounds, or any fixed number, reach `h` is open**; so are the existence and the
   value of the two-round exponent, what two rounds cost *at* the flat-histogram instance
   (where the lower bound holds for the expected cost), strict monotonicity in the number
   of rounds, and the rate of convergence.
   And **finite sizes** — two
   levels beat the plain bracket only from `n ≈ 500` on at bounded accuracy and `u = 1`
   (beyond `e^{45}` evaluations; `n ≈ 250` at the flat instance only — the worst instance at
   finite `n` is not the flat one, ENG-RES-0008, and which instance maximises the cost of
   Algorithm 2L⁺ at a given `n` is not known beyond that division's search) and from
   `n ≈ 2000` at extensive ones; is there an adaptive algorithm that
   wins at sizes that can be simulated, or a lower bound showing that the gain needs
   `n ≫ 1/θ_hint`?  (iii) **instance by instance** — the zero function is the hardest instance
   with a hint (a corollary of Theorems 11.54 and 11.58); is there an adaptive algorithm
   without a hint that matches the hinted cost at *every* instance up to `e^{o(n)}`, cheap
   instances included?  (iv) **exponentially small accuracies** `ε = e^{-λn}`: the hinted
   exponents of rows 4–6 of Theorem 11.25(d) are not known to be attained without a hint.
   (v) **other spaces** — *a field as known part is done at the level of exponents* (§11.20,
   refereed: R9): the tail lemma is taken relative to a reference instance, the reference is
   the lower envelope of the additive instances, and the isoperimetric input is an
   asymptotic statement for that reference, not the isoperimetry of a fixed product measure
   (which gives the worse exponents of plain sampling from the Gibbs measure of the known
   part — the guess of the earlier checkpoints was wrong in this respect, D47).  Open there:
   a finite-`n` bound for the tail function of the reference with a usable error term (the
   proof gives `n^{-1/8}`; numerically it is `O(ln n/n)`, and on the 4-cube the exact maximisers
   are not always one-centre balls: ratio `2.08`) — a weighted Harper-type inequality; bounded
   accuracies; a proof that no single tilted product measure attains the non-adaptive
   exponent at extensive accuracies when `p ≠ ½` (numerical in three examples), and whether
   the product measure with the capacity-achieving marginal attains it on the whole class
   at bounded accuracy (it does at cone instances; Theorem 11.61); an end-to-end simulation of the
   nested algorithm with a field; instance-optimality beyond symmetric
   instances; larger alphabets and sites of several types — **§11.26: theorems by transfer,
   reviewed (SCI-REV-0005: proved; two gaps in the written proof of the adaptive upper
   bound closed)** (open there: a referee for Theorem 11.97(c) together with Theorem
   11.78(b); a finite-`n` form of Theorem 11.97(c) with a usable error term — exact tail
   functions of the reference on chains small enough for exhaustive search; a simulation
   of the nested algorithm; concavity of `F*` for two letters, that is, of `max_p E_0(ρ, p)`
   in `ρ` for binary-input binary-output channels; which site law
   and which pinned composition is the hardest; alphabets beyond four letters and more
   than two site types numerically; whether the channel-coding dictionary yields anything
   beyond names — bounds on `E_0`, algorithms for `C_t`, strong-converse analogues); **known parts with
   interactions** — for functions of the type (mean-field models) §11.23 settles the
   non-adaptive problem and the hinted exponent of symmetric instances for every rate
   function (refereed, R10); open there, in order of importance: (α) *the adaptive exponent
   without a hint* (conjecture: the single-letter value `R_H` of the flat-histogram
   instance; the nested algorithm fails because fibre averages are not Lipschitz relative
   to a reference.  §11.25 reduces the question to the uniform measure on one type class
   (Theorem 11.92), where the conjecture is that the proof of Theorem 11.56 goes through
   with random splits (Conjecture 11.94); that would give the uniform cube's exponent as
   an upper bound for *every* interaction and the exact exponent for interactions
   without a field.  **Two things are open: redoing the proof of Theorem 11.56 on
   products of type classes, and — when exits that change the type matter — the exact
   exponent between `R_H` and the bound from type classes**, which needs information
   across type classes; nesting by the type of the inner block leads to a recursion over
   rate functions that we could not close.  For ferromagnets the uniform cube's exponent
   is already an upper bound, through mixtures of fields: Proposition 11.81(c)); (β) the value
   of the single-letter supremum with two phases beyond the accuracy `e₀` at which sets
   around one centre stop being extremal, and a proof that they are extremal below it;
   (γ) without convexity: strict monotonicity of the shear and the witness condition for
   the pair identity, which fails for cones around profile classes near the threshold at
   which the top of the barrier leaves the contact set (there the non-adaptive exponent is
   proved to lie in `[0.00184, 0.00338]` only); (γ′) the junction with the uniform cube: a
   proof that it is at `min{βJ*, βJ_w}` — the smaller of the coupling at which the symmetric
   exit of the uniform cube's profile stops being a local minimum and the coupling at
   which a constant exit at a well becomes feasible — and that `R_H < R_unif` beyond it
   (Proposition 11.81(b); the second would follow from uniqueness of the uniform cube's
   optimal profile among laws of block types of type `½`); (δ) ~~whether an
   antiferromagnet without a field — in the limit a single slice — has exactly the
   uniform cube's exponents~~ **settled in §11.25 for two of the three exponents**, the
   hinted one of `H` and the non-adaptive one (Corollary 11.91: yes, and no function-of-type
   known part exceeds them; reviewed by the Scientific Discovery Division, SCI-REV-0001,
   whose finding M1 this restriction is — for adaptive algorithms without a hint an
   antiferromagnet is only known to lie between these two exponents:
   item (α)); (ε) mean-field Potts models and two
   order parameters (a sketch); (ζ) larger alphabets: the comparison
   with the uniform cube **fails** for three or more letters (§11.25, remark; Proposition
   11.103(d): at small slopes a known part that pins the composition onto two letters is
   harder than none, a field with one rare letter is harder still — by `0.03 %` at slope
   `0.5` — and near the threshold a field can be; Proposition 11.103(f) bounds every site
   law by the ceiling `u²/32`); open: *which* site law and
   which pinned composition is the hardest for a given envelope (for the Hamming envelope
   the evidence points to groupings of the letters into about `e^{u/2}` equally weighted
   classes at vanishing accuracy, Proposition 11.103(e), but not near the threshold, and a
   law with one rare letter can exceed every equal grouping by a small margin).  For known parts with *spatial* structure (short-range
   interactions; Markov chains along the sequence) nothing is proved; the natural next
   step is the method of types for Markov chains, where "uniform on type classes" still
   holds for pair types but the one-flip coupling of adjacent classes is no longer exact.
   The conjecture of the earlier checkpoints, that the minimax fixed sample is the
   normalised-maximum-likelihood mixture of the field-tilted Gibbs measures, is right
   about the ensemble only for convex rate functions (D49).  For Euclidean Lipschitz functions on Gaussian space
   neither the lower bound (half-spaces are detected from far away) nor the algorithm (blocks
   are not cheaper) transfers, and no exponent is known to us; (vi) **a machine-checked
   count** — the number of evaluations of the two-level algorithms (Theorems 11.52, 11.56) is
   a paper proof, in a part of the argument where five wrong versions preceded the right
   one; the Computational Research Division has been asked to attack it with real inner
   brackets and three nested levels (THY-REQ-0001).
   This is a tractability question for integrating `e^{−βg}` over a Lipschitz class in high
   dimension, and the natural bridge to the open lower bound of Holzmüller–Bach (2025) for
   stochastic log-partition estimation outside the optimisation regime;
   (e) for `f ≡ 0` in doubling spaces, does the resource-augmented bound of Theorem 11.11
   convert into `≤ K·N* + 1` without the `log(1/ε)` of Bachoc et al. (`prior_art/L4`, sketched,
   unverified)?  With a known part it does not (D30), and the search itself is unboundedly
   worse than the smallest certificate even on the line (§11.11, D39).  For asymmetric
   envelopes Theorem 11.11 needs a quasi-symmetry constant of the slack, which can be
   arbitrarily bad, and its constants `θ`, `ε/6` are probably not tight; the centre-form bound
   of Proposition 11.30 covers `κ = 1` but not dominated states.  Is there a search rule with a
   guarantee against the certificate size on product landscapes (the exponent of best-first
   search there is only bracketed, workstream C)?
3. **Complexity classification of the exact criteria** (referee, Q4.1(iv)).  For pairwise `E₀`
   and site-additive `d`, "is configuration `x` possibly optimal" is a pairwise minimisation;
   "is state `r` of site `i` possibly optimal" is an `∃∀` question — is it `Σ₂ᵖ`-hard, and
   polynomial on chains?  On succinct product spaces even *verifying* a certificate is
   coNP-hard in general (covering radius); the kernels avoid this only through explicit
   branch-and-bound certificates.
4. **Second-order classes.**  The question of the previous version — is the cost under dense
   constants exponential, as the covering radius `(2·gap/c)^{1/2}` suggests? — is answered in
   §11.12: yes, with a covering sandwich, and polynomially many evaluations suffice only when
   the excitation energy is at least a quarter of `c·n`.  Open: the simplex conjecture (is the
   three-legged spider the best `n+1` evaluations?); the window `n/4 ≲ e/c < n/3`; the cost for
   sparse constants beyond the clique bounds; re-centring with a termination guarantee; a
   box-restricted class; certified constants `c_ij` for one concrete residual — without which
   the interface is hypothetical.
5. **Dependent references.**  The exact worst-case free-energy gap for a Markov-chain
   reference: additivity fails in general (D25), and it fails for binary pairwise models and
   binary Markov trees as well (D41); for open binary chains without tilt no counterexample
   is known; a two-sided bracket from transfer matrices (best additive two-level residual
   below, Wasserstein-matrix bound above) is unwritten.
6. **Proof complexity of the extended kernels.**  Lower bounds for connected families
   (triangles coupled along a chain) for cut-free and for decomposition-aware certificates; an
   approximate version of the partition-kernel separation and a representation-independent
   notion of rigidity (§11.8); comparison with MICE/CPOG for model counting and with
   pseudo-Boolean proof logging.
7. **Engineering** (referee, Q2): a certificate producer and experiments at realistic sizes; a
   compiled checker with a refinement proof (kernel evaluation by `decide +kernel` does not
   scale); certified envelope constants for a real residual.

8. **Probabilistic certificates.**  A kernel that checks a spot-check transcript against
   verifier-side randomness, with `hedgedSpotCheck_correct` as its soundness theorem.  The
   detection probability `p` must itself be certified: for the minimum it is a minimum over
   closed slack balls and the set of near-minimisers (harness XII.4, XII.7); for free energies
   it is an isoperimetric quantity (item 2(b)) — at additive instances above the threshold the
   two-reference sandwich certifies it by a single-site computation.
9. **Envelopes for chains** (§§11.14, 11.17).  *Partly answered in cycle 10*: residual classes
   that are linear in pair-distance profiles have per-pair constants and, at extensive
   accuracy, certificates whose number of evaluations does not depend on the chain length —
   for a class that is much smaller than the RMSD-Lipschitz classes of §11.14, and with a
   bound that is numerically vacuous.  *Data received in cycle 10* (Computational Research
   Division): no saturation at any enumerated size — linear growth on the lattice through
   27 beads, geometric growth off-lattice through 15 beads (§11.17).  Open: (a) **a
   thermodynamic limit theorem for certificate sizes.**  For the zero residual and a known
   part that is a function of the gauche count, the cover problem depends on the chain only
   through the set of pairs (profile, fewest gauche torsions realising it); if that set,
   divided by `N`, converges, the certificate size at accuracy `ε₁N` should converge to a
   covering number of the limit with position-dependent radii (`ENG-REQ-0001`).  Is there a
   limit shape, is it convex (concatenation suggests it; the obstruction is a chain end
   buried in a compact piece), how large is the plateau, and at what chain length is it
   approached?  *Answered in part for the lattice chain in §11.22* (workstream S; reviewed by the
   Scientific Discovery Division, SCI-REV-0002, whose wording this is): a compact convex
   limit shape exists for bridges; the certificate sizes of bridges converge to its covering
   number off a countable, unidentified set of accuracies; for every limit point of the
   certificate sizes of all walks at `(L, ε₁) = (1, ½)`: between 116 and 3 627 **[P,
   computer-assisted]**; that the sizes of all walks converge is a conjecture **[C]**; our
   estimate of the limit is a few hundred and of the chain length at which it is approached
   `10³`–`10⁵` beads or more **[N]** — the shape has a surface correction of exact order `N^{-1/3}`
   at its compact end, but no theorem bounds that chain length in either direction (the
   first version said "for all walks the plateau is between 50 and 3 627 … and is approached
   at `10³`–`10⁵` beads").  **Still open:** (a0) whether `ε₁ = ½` or `¼` is a jump of the limiting
   covering number, and any rigorous statement about *when* the covering numbers are near
   their limit points;
   (a1) *Conjecture 11.75* — unrestricted walks have the same limit shape as bridges;
   equivalently, walks and bridges have the same ground-state energy per bead for every
   three-shell pair energy with a stiffness term; equivalently, every walk has the
   `(profile, #gauche)` of `o(N)` bridges up to `o(N)`.  Local surgery cannot prove it (a double
   strand is rigid); what is missing is a bound on the cost of a multi-scale decomposition.
   The free-energy analogue for self-attracting walks is a standing open problem; this
   question is weaker.  (a2) The exact body: seven vertices of the outer polytope are
   attained by no periodic chain system with at most 12 sites per cell — either a
   second-level cluster programme (two-shell cluster, six-ring) removes them or larger
   cells attain them (`THY-REQ-0008`); with it `N_∞` to better than a factor of ten.  (a3) The
   routing lemma that puts every periodic chain system into the limit set (a sketch).
   (a4) A rate for the whole body (the compact end is settled at `N^{-1/3}`; interior points
   are approached at rate `N^{-1/2}`, Proposition 11.69a, and at rate `1/N` if the bridges can be
   re-bookkept as an exact semigroup — SCI-REV-0006, T-4).  (a5) Anything
   off-lattice: there the profile is a function, the plateau is exponential in
   `L·S_c·M/ε₁`, and only a heuristic estimate exists; a prediction of the measured growth
   rate per torsion needs the distance-entropy function of the profile classes.  The
   Computational Research Division has measured it up to 14 torsions (ENG-RES-0009): at
   `L = 1` the entropy per torsion of a profile ball of radius `N/2` is `0.33` and still rising
   by `0.013` per torsion — the value `0.39` that we had inferred from the growth of the
   covering numbers (THY-RES-0002) is a statement about a limit these sizes have not
   reached, neither established nor excluded; at `L = ⅕` it has nearly converged at `0.65`
   (inferred: `0.6`); and the number of pairs per bead within the cutoff is `3.1` at 17 beads
   against the bulk value of about `63` on which the heuristic plateau estimate rests —
   **every enumerable chain is at one twentieth of the bulk coordination**.  (a6) The
   abstract limit theorems are machine-checked (`CoverStability.lean`, `SetLimit.lean`); the
   two lattice lemmas that feed them — the site-set reduction and the concatenation of
   bridges — are not.  (b) an upper bound for the class
   "pair-additive plus a small first-order remainder" that matches the lower bound "the two
   slacks add", or a proof that the cost is a product; (c) randomised algorithms for linear
   classes — all lower bounds there are for deterministic schemes at the zero residual, and a
   generic evaluation sees every perturbation, so the dip construction has no analogue;
   (d) the cost of *checking* a certificate in the profile format over voxels of torsions,
   where the lever arm returns; (e) profiles for three-body terms; (f) whether a physically
   motivated residual has a useful Lipschitz constant in this format — the interface is
   hypothetical until one instance is certified.  Unchanged from cycle 9: close the bracket of
   Theorem 11.38 (constants two orders of magnitude apart; lower bound at the zero residual
   only; excluded volume ignored), prove the lower constant of the lever-arm law, and a lower
   bound for the RMSD format when its constant is extensive.
10. **Second-order classes at finite temperature** (Theorem 11.33): sharpen the polynomial
   bound below the Curie–Weiss coupling; non-homogeneous constants (Dobrushin's condition is
   then a row-sum condition); `k`-state sites; the continuous analogue and its relation to the
   smoothness classes of Holzmüller–Bach.  **Observables other than `ln Z`** (Theorem 11.35):
   close the interval between `H/√2` and `H` for the magnetisation at weak coupling.
11. **Observable free energies** (§11.28; the question of the Scientific Discovery
   Division that we rank first among the new ones).  The *range* of a ratio of two
   macrostate weights is settled as a duality; open are, in order: (a) **the number of
   evaluations** needed to certify `ln[Z(A)/Z(B)]` to a given accuracy — with a hint, the
   counterpart of Theorem 11.25; without one, of Theorems 11.45 and 11.54 — where the
   sensitive alternatives are no longer dips on small sets alone: a perturbation that
   moves weight between the two macrostates matters at first order, and the constraints
   from `B` to `A` couple the two partition functions; (b) the exact range for a pairwise
   known part (on a tree by dynamic programming?) and for macrostates defined by a
   counting statistic; (c) the range and the cost for chains with geometric envelopes
   (§11.17), where macrostates are sets of conformations and the envelope is a profile
   distance; (d) prior art — *answered at summary level by the Scientific Discovery
   Division (SCI-RES-0005)*: for a separable envelope Theorem 11.105 is the closed form
   of the density-ratio class; the general duality was not found; two leads are
   unresolved (credal sets from comparative probabilities; cones of the
   Birkhoff–Hilbert-metric method); (e) soft macrostates (weight functions) and more than
   two of them; (f) a common generalisation of Theorems 11.106 and 11.106a — a condition
   under which the maximal field is the optimal closed pair.
12. **Local data with a field** (§11.29).  The class exponents are settled (Theorem
   11.109a).  Open: (a) the exact exponent *at an instance* with a one-body oracle — the
   bracket `V ≤ R^{orc} ≤ U` of Proposition 11.109b; the division conjectures the lower end,
   and what is missing is an isoperimetric upper bound that knows the window of one-body
   marginals (a type-resolved Theorem 11.63); (b) marginals of order `k ≥ 3` with a field
   (the division's conjecture); (c) a machine-checked compensation lemma (asked of the
   division).
13. **Remainders that are small in a typical norm** (§11.30).  For box classes the cost
   is settled up to constants and is independent of the size of the system.  Open, in
   the order of their value for applications: (a) **a certified floor** for a physical
   remainder — a bound on how far below the known function the truth can lie, by
   analysis of the functional form, not by fitting (for a generalized-Born term: an
   interval evaluation of its mixed differences, the route proposed in SCI-MSG-0015);
   (b) classes between the box and the first-order classes — a box *with* geometry (the
   intersection is treated in Corollary 11.111; a moment constraint under `π`, e.g.
   `E_π e^{−2(r − r̄)} ≤ κ`, is not: with a floor it is a box, without one a single hidden
   state defeats every sampler); (c) the cost of a *ratio* of macrostate weights in a box
   class — the first instance of item 11(a) without geometry; (d) known parts that can
   only be sampled approximately (a Markov chain with a certified mixing time).

As it stands, the second phase contains one cluster with the shape of a research contribution —
*the query complexity of certifying ground states and free energies under envelope
uncertainty*: an exact covering characterisation (certificate size = instance-wise deterministic
complexity), a dichotomy and exponents at zero and finite temperature with one variational
formula and three budgets, lower bounds for every randomised algorithm with a hedged converse,
an accuracy threshold and the complete accuracy diagram on the cube, hardness, a
resource-augmented guarantee for best-first search, and second-order classes — with every
one-shot lower bound machine-checked.

*The second referee's assessment* of this cluster without §11.10 (`reviews/R2`, §4), which we
accept: "a coherent note, not a theorem-driven paper".  It is not publishable as mathematics or
information theory, because after the reformulation each step is a short application of a
standard tool (type covering, Merhav's theorem, Chernoff and Hölder, the dominating-set
reduction, a packing argument, a discrete Taylor remainder); it could be a short note for the
certified-optimisation audience, or a formalisation paper.  Of the seven things the referee
found missing, this revision supplies four: the corrected statement of Theorem 11.15 and the
missing step of Theorem 11.9; the positioning (the exponents are corollaries); an algorithmic
statement (lower bounds for all algorithms; learn-then-cover on additive instances); and a
probabilistic notion with matching limits (spot-checked hints; Theorems 11.24–11.25).  Still
missing: a step beyond product landscapes (a pairwise chain as known part); a regime in which
best-first search is provably within a constant of `N_cov`, or tight constants; a lower bound
and one certified instance for second-order classes; and, new, the exact randomised exponent
(item 2(b)).

*The fifth and sixth referees' assessments* of §§11.16–11.17 (`reviews/R5`, `reviews/R6`), which
we accept.  §11.16: Lemma 11.43(a) is elementary and (b) a routine corollary of Harper's
theorem; Theorem 11.44 was not found in print and is a routine combination of truncation at a
quantile, an isoperimetric tail bound, Chernoff and Markov; the method of Theorem 11.45 is
known, its hard family is that of Mathé–Novak (2007) moved to the cube, and the exact
non-adaptive exponent on the cube for `ln Z` is apparently new.  §11.17: the linear theory is
known (optimal recovery, set-membership estimation, robust linear programming), the profile
distance is known as a descriptor distance, the entropy bound is the classical one for
monotone functions, and what was not found — the profile distance as the exact envelope of a
residual class next to a known part, with the count of evaluations — is immediate once
named.  Neither section changes the verdict of the earlier referees; §11.17 answers the
question of §11.14 for a narrower class than the one that was asked about.

*The third referee's assessment* of §11.10 (`reviews/R3`, §4), which we accept: the section does
not change the verdict.  Theorem 11.22 is the indistinguishability argument with a union bound
— fractional block sensitivity transplanted to real-valued classes; Theorem 11.23(a) is the
definition of a certificate read as instance complexity; Theorems 11.23(b) and 11.24 insert one
explicit family of alternatives.  The section makes the note more complete, and "randomisation
is worth at most the integrality gap for the minimum but has a threshold for `ln Z`" is a clean
message for the certified-optimisation audience, where the randomised case is named as open.
Theorem 11.25 was, as submitted, too thin (one class, one instance, part (c) wrong at one end
and unproved at the other); the referee named five ways to make it a contribution.  This
revision carries out the first — the complete accuracy diagram at the zero residual with a
hedged converse, lower bounds machine-checked.  Workstreams A and B address the third and the
fourth (Theorems 11.27–11.28: the conjecture refuted, the right family of perturbations, the
instance-wise threshold for every alphabet, the hint-free threshold of two-state classes;
verified here except for the matching upper bound of the exponent, which is not yet
refereed).  The second (hint-free
algorithms) and the fifth (the bridge to smoothness classes) are open (item 2(d)).  The referee
also found the same error for the second time — an asymptotic statement claimed for all
`ε = o(n)` although it fails for exponentially small accuracies (R2-C1 in Theorem 11.15, R3-C1 in
Theorem 11.25(c)) — and four overstatements of scope ("the sandwich", "the cube class", "the best
algorithm"); the corrections are in §11.10, in the README and in `DEAD_ENDS.md` D35–D37.

---

## 13. References

Full bibliographic details, DOIs and verification status of each citation are in
`prior_art/L1_pruning_certificates.md`, `L2_relaxations_partition.md`,
`L3_realizability_geometry.md` and, for §§10–12, `L4_certified_optimisation_and_recovery.md`,
`L5_polytropes_interval_uncertainty.md`, `L6_transport_entropy_and_information_limits.md`,
`L7_query_complexity.md`, `L8_linear_classes.md` (each with its search log and a list of sources
that could not be read in full), and `L9_review_additions.md` for the sources that entered
through the Scientific Discovery Division's reviews, with whose reading each rests on.
Principal
sources:

*Pruning and certificates.*  Desmet, De Maeyer, Hazes, Lasters (1992); Goldstein (1994); Leach &
Lemon (1998); Looger & Hellinga (2001); Kloppmann, Ullmann, Becker (2007); Georgiev, Lilien,
Donald (2008); Gainza, Roberts, Donald (2012); de Givry, Prestwich, O'Sullivan (2013);
Shekhovtsov (2014; 2016); LuCore et al. (2015); Hallen, Jou, Donald (2017); Hallen et al. (2018);
Hallen & Donald (2019); Jeroslow (1974); Dechter & Mateescu (2007); Basu, Conforti, Di Summa,
Jiang (2023); Cheung, Gleixner, Steffy (2017); Bogaerts, Gocht, McCreesh, Nordström (2023);
Bryant, Nawrocki, Avigad, Heule (2023).

*Partition functions and concentration.*  Zwanzig (1954); Isihara (1968); Hoeffding (1963);
McDiarmid (1989); Bobkov & Götze (1999); Wainwright, Jaakkola, Willsky (2005); Kontorovich &
Ramanan (2008); Liu & Ihler (2011); Rio (2013); Owhadi et al. (2013); Kontorovich & Raginsky
(2016); Viricel et al. (2016); Lou, Dechter, Ihler (2017); Ojewole et al. (2018); Jou et al.
(2020); Gourgoulias, Katsoulakis, Rey-Bellet, Wang (2020); Bakhvalov (1959); Holzmüller & Bach
(2025).

*Relaxations and verified numerics.*  Adjiman, Dallwig, Floudas, Neumaier (1998); Skjäl,
Westerlund, Misener, Floudas (2012); Bompadre & Mitsos (2012); Bach & Rudi (2023); Solovyev &
Hales (2013); Martin-Dorel & Melquiond (2016); LeanCert (Radisic, 2026); girving/interval.

*Geometry.*  Schoenberg (1935); Hoffman & Wielandt (1953); Mardia (1978); Cailliez (1983);
Dokmanić et al. (2015); Tsang & Pereira (2016); Sonthalia, Van Buskirk, Raichel, Gilbert (2021);
Deng et al. (2024); Tu et al. (2016); Arias-Castro, Javanmard, Pelletier (2020); Pitzer & Gwinn
(1942); Kabsch (1976); Kudin & Dymarsky (2005); Popov & Grudinin (2014); Noguti & Gō (1983);
Bandeira, Singer, Spielman (2013); Rosen, Carlone, Bandeira, Leonard (2019); Lerman & Shi (2022);
Jumper et al. (2021); Bachoc, Cesari, Gerchinovitz (2021).

*Certification geometry (§§10–12).*  Difference constraints, temporal networks, polytropes:
Dechter, Meiri, Pearl (1991); Miné (2001); Joswig & Kulas (2010); Murota (2003);
Gordon & Petrov (2017); Tran (2017).  Lipschitz extension and robust optimality: McShane (1934);
Cobzaş (2013, semi-Lipschitz functions); Polyak (1979); Burke & Ferris (1993); Aissi, Bazgan,
Vanderpooten (2009); Malherbe & Vayatis (2017).  Certified Lipschitz optimisation and optimal
recovery: Piyavskii (1972); Shubert (1972); Danilin (1971); Sukharev (1971); Hansen, Jaumard, Lu
(1991); Baran & Demaine (2004); Baran, Demaine, Katz (2008); Novak (1988); Micchelli & Rivlin
(1977); Traub, Wasilkowski, Woźniakowski (1988); Munos (2011); Bouttier, Cesari, Gerchinovitz
(2020); Bachoc, Cesari, Gerchinovitz (2021); Plesník (1987); Gørtz & Wirth (2006).  Covering and
rate–distortion: Lovász (1975); Chvátal (1979); Csiszár (1974; 1998); Csiszár & Körner (2011,
Lemma 9.1); Kostina & Verdú (2012); Polyanskiy & Wu (2025); Arikan & Merhav (1998, guessing
subject to distortion); Merhav (2011, exponential moments of a cost function; 2025).  Transport–entropy:
Marton (1996); Bobkov, Houdré, Tetali (2006); Alon, Boppana, Spencer (1998); Gozlan & Léonard
(2007; 2010); Djellout, Guillin, Wu (2004); Paulin (2015).  Robust Bayes and ratio classes:
DeRobertis & Hartigan (1981); Wasserman (1992); Walley (1997); Kairouz, Oh, Viswanath (2016).
Anchored decompositions: Rabitz & Aliş (1999); Kuo, Sloan, Wasilkowski, Woźniakowski (2010);
Griebel & Holtz (2010).  Query complexity and isoperimetry (§11.10): Aaronson (2003, randomised
certificate complexity); Tal (2013); Gilmer, Saks, Srinivasan (2016); Kulkarni & Tal (2016,
fractional block sensitivity); Nemirovski & Yudin (1983); Harper (1966); Ge, Lee, Lu (2020);
Chatterjee & Diaconis (2018); Grossman, Komargodski, Naor (2020, instance complexity);
Holzmüller & Bach (2025); Ahlswede, Yang, Zhang (1997, inherently typical subsets); Ahlswede &
Zhang (1999); Yu (2024, isoperimetric exponents of product measures).  Search and normal form
(§11.11): Hetland (2020); Dechter & Pearl (1985); Goldberg & Harrelson (2005); Vidal (1986);
Johnson (1977).  Second-order classes (§11.12): Chierichetti, Dasgupta, Kumar (2020, approximate
modularity); Feige, Feldman, Talgam-Cohen (2017).  Verification status of these additions:
`reviews/R4_referee_report.md`, `R_C_review.md`, `R_E_review.md`.  Without a hint (§11.16):
Mathé & Novak (2007, simple Monte Carlo and the Metropolis algorithm); Chatterjee & Diaconis
(2018); Harper (1966); Dzindzalieta (2013); Krieg, Novak, Ullrich (2025); Heinrich (2024); Cai
& Scarlett (2024).  Linear classes and pair-distance profiles (§11.17): Smolyak (1965);
Micchelli & Rivlin (1977); Milanese & Vicino (1991); Soyster (1973); Maiorov & Crippen (1992);
Tobi, Shafran, Linial, Elber (2000); Podryabinkin & Shapeev (2017); Osada, Funkhouser,
Chazelle, Dobkin (2002); Hansen et al. (2015, bag of bonds); Figalli & Gigli (2010); Birman &
Solomyak (1967); van de Geer (2000); Binev et al. (2011); DeVore, Petrova, Wojtaszczyk (2013);
Henderson (1974).  Verification status: `prior_art/L7_query_complexity.md` (addendum),
`prior_art/L8_linear_classes.md`, `reviews/R5_referee_report.md`, `R6_referee_report.md`.
Mean-field known parts and flat-histogram sampling (§11.23): Berg & Neuhaus (1992,
multicanonical ensemble); Wang & Landau (2001); Dayal, Trebst, Wessel, Würtz, Troyer,
Sabhapandit, Coppersmith (2004, performance limitations of flat-histogram methods); Trebst,
Huse, Troyer (2004, optimising the ensemble for equilibration); Cérou, Héas, Rousset (2022,
worst-case optimal importance proposals); He & Owen (2014, optimal mixture weights);
Hesterberg (1995, defensive mixtures); Hinrichs (2010).  Verification status: search
summaries and abstract pages only (workstream T, `docs/workstreams/T_REPORT.md` §9).
Rounds of adaptivity (§11.24): Canonne & Gur (2017, an adaptivity hierarchy theorem for
property testing); Nemirovski (1994, parallel complexity of non-smooth convex
optimisation); Balkanski & Singer (2018); Bubeck, Jiang, Lee, Li, Sidford (2019);
Diakonikolas & Guzmán (2018); Agarwal, Agarwal, Assadi, Khanna (2017); Gao, Han, Ren, Zhou
(2019); Price & Woodruff (2012); Cai & Scarlett (2024); Novak (2023 survey on adaption).
Verification status: search summaries only (workstream U, `docs/workstreams/U_REPORT.md` §7).
Slices and the odds-ratio lemma (§11.25): **Hasenclever & Scholz (2013; arXiv:1302.6161;
Open Stat. Probab. J. 2016), *Comparing measures of association in 2×2 probability
tables* — Proposition 8(a) is Lemma 11.89** (found by the Scientific Discovery Division;
the statement read by us in the arXiv full text, the proof not); the capacity of the binary asymmetric channel is
textbook material (e.g. Mondelli, Hassani, Urbanke 2014, *How to achieve the capacity of
asymmetric channels*, for the non-uniform optimal input); Kesal (2017, *Generalized bounds
on the capacity of the binary-input channels*, bounds through the Bhattacharyya
parameter).  Verification status of these two: titles and search summaries only; our two
searches for the comparison at a fixed odds ratio (among channel capacities) found
nothing, the Scientific Discovery Division found it among measures of association.
Added on the evidence of SCI-REV-0004 (the division read them in full where accessible;
*we* verified only what is said here): Suárez, Silbey, Oppenheim (2012, *Phase transition
in the Jarzynski estimator of free energy differences*, Phys. Rev. E 85, 051108,
arXiv:1108.5783 — subject, eq. (31) and the bias formula verified by us; §11.10, §11.16);
Karnin (2016, verification-based solutions for structured bandits) and Garivier & Kaufmann
(2016, optimal best-arm identification with fixed confidence) for "explore, then verify"
(§11.18; not opened by us); Guo, Liu, Yang, Yin, Zhang (2026, arXiv:2609.20337) and Harris,
Kolmogorov, Liu, Yin, Zhang (2026, arXiv:2604.01263) on non-adaptive and two-round
annealing in the sampling-oracle model (§11.24; abstracts read by us); Beh & Morio (2026)
on minimax proposals, Idais & Schwabe and Kiefer (1959) on invariant designs (§11.23),
Williams (2022) for the value of the mutual information at uniform margins, Novak (1995)
as quoted in Krieg–Novak–Ullrich (2025) on adaption for non-symmetric classes — named by
the division, not checked by us.
Heteropolymer product landscapes and the channel-coding dictionary (§11.26): Csiszár
(1995, generalized cutoff rates and Rényi's information measures: the definitions of the
Rényi capacity coincide with the Rényi radius); Sibson (1969, information radius);
Nakiboğlu (2019, *The Rényi capacity and center*; 2019, *The sphere packing bound via
Augustin's method*); Gallager (1968, `E_0` and parallel channels); Csiszár & Körner
(the constant-composition form of the sphere-packing exponent).  Verification status:
search summaries only (workstream W, `docs/workstreams/W_REPORT.md` §13); the proofs of
§11.26 do not depend on these sources.

*Added from the science division's review of originality* (`SCI-REV-0006`; reading level of
each source in its report `docs/science/workstreams/A2_REPORT.md` §4 on the branch
`research/scientific-translation`; not re-read by us).  Proof logging and verified counting:
Koops, Le Berre, Myreen, Nordström, Oertel, Tan, Vinyals (CP 2025); van Doren, Antonopoulos,
Piskac (ASE 2025); Py, Cherif, Habet (2022); Tan, Yang, Soos, Myreen, Meel (CAV 2024);
McCreesh, Nordström, Oertel, Tan (CP 2026); Cheng, Luo, Jiang (IJCAI 2024); Szeider (2026,
PBLean).  Weightable quasi-metrics and partial metrics: Matthews (1992); Künzi & Vajner
(1994); Deza, Deza, Vidali (2011).  Lever arms in robotics: Schwarzer, Saha, Latombe (2005);
Featherstone (2004).  Distance distributions and reconstruction from distances: Mémoli (2011);
Mémoli & Needham (2022); Boutin & Kemper (2004); Jiao, Stillinger, Torquato (2010).
