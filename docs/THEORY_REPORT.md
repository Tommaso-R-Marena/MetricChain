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
| D3 | **Partition-function kernel** with leaf/branch/thermal-prune rules; enclosure of the real `Z`, end to end from interval energy tables | `zverify_sound`, `zverifyTop_sound`, `Z_encloses_partitionFn`, `certified_partition_of_intervals` **[V]** | verified checkers exist for exact model counting only; this rule set: no match found |
| D4 | **Voxel enclosure**: continuous Boltzmann integrals → rational kernel, with the volume (entropy) factor, end to end for pairwise torsion energies on product voxels (table enclosures + outward-rounded factors + accepted certificates ⇒ two-sided bound on the integral); separable (second-order) envelopes factor an `M`-dimensional voxel integral into `M` one-dimensional ones | `voxel_boltzmann_bounds`, `pairwise_voxel_weight_bounds`, `certified_torsion_partition`, `separable_voxel_bounds` **[V]** | `K*`-family algorithms bound a sum of minimised voxel energies; rigorous voxel-*integral* bounds inside a provable design algorithm: no match found (rigorous enclosures of integrals as such are standard verified numerics) |
| D5 | Hölder decomposition with temperature rescaling | `partitionFn_holder`, `freeEnergy_holder` **[V]** | **known** (weighted mini-bucket) |
| C1 | Hoffman–Wielandt and von Neumann trace inequality (real symmetric) | `hoffman_wielandt` **[V]** | **classical** (1953); formalization |
| C2 | Trace-enhanced spectral obstruction: `min_X ‖D̂ − Δ(X)‖²_F ≥ 4 Σ_{k>r} λ_k² + (4/(r+1)) (Σ_{k>r} λ_k)²` | `rank_psd_trace_obstruction`, `sstress_lower_bound` **[V]** | **known** with these constants (Sonthalia et al. 2021; K-identity in Tsang–Pereira 2016); machine-checked here down to Hoffman–Wielandt (we know of no earlier formalization) |
| C3 | Cycle-holonomy obstruction; SE(3) translation holonomy with lever arms | `norm_holProd_le_sum`, `norm_holTrans_le` **[V]** | triangle bound **known** (Lerman–Shi 2022, Lemma 1); a sharp non-abelian Hodge-type bound is open |
| C4 | **Finite-angle torsion → RMSD**: exact coaxial cost `2S − 2√(S² − 4 I_A I_B sin²(φ/2)) ≤ 4 min(I_A,I_B) sin²(φ/2)`; chain rule; envelope for Lipschitz residuals invariant under a group of motions containing the axis rotations (`SE(3)` or `E(3)`), down to membership in the kernel's residual class | `exists_coaxial_angle`, `coaxial_cost_le_min`, `rigidWithin_torsion_chain`, `residual_torsion_chain_in`, `residual_torsion_move_uniform`, `verifyR_sound_invariant` **[V]** | small-angle content classical (Pitzer–Gwinn; Eckart); finite-angle closed form and chained bound: no match found |
| B1 | Outward rounding, rational intervals, certified `exp`, rational circle atlas | `Core/Rounding.lean` **[V]** | infrastructure; verified interval libraries exist (LeanCert, girving/interval) |
| E1 | **Master Soundness Theorems** for the tropical, residual and sum–product kernels; the top-level kernels check their own side conditions (consistency of interval anchor data — which is exactly non-emptiness of the residual class — and nonnegative factors) | `verify_sound`, `verifyITop_sound`, `IProblem.consistent_iff_nonempty`, `certified_gap`, `zverifyTop_sound` **[V]** | no *native* verified checker for cost-function-network / MAP / DEE certificates found; such runs can in principle be encoded as pseudo-Boolean proofs and checked with existing verified checkers, so the gap concerns native witnesses and their checking cost (`prior_art/L1` §C4(ii)) |
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
of several known results.  The results of the second research phase (§§10–12; rows G1–G11 of §10), which
were developed in response to that assessment and were themselves reviewed by a second independent
referee (`reviews/R2`), are classified separately there.

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
medium confidence).  The natural sharpening — replacing the `ℓ¹` chain by the Eckart-frame metric
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
box the true optimum lies in `[L, E(a) + v]`.

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
CakePB, PBLean), MIP (VIPR, exact SCIP, LeanVIPR) and exact model counting (Bryant et al. 2023,
Lean 4).  Neither OSPREY nor toulbar2 emits checkable proofs, and no verified checker for
cost-function-network / MAP lower bounds, DEE steps or approximate partition-function bounds was
found (`prior_art/L1` §C4(ii)).  The kernels here are *native* certificates for that problem
class: a reparameterisation is a linear-size witness for a local-polytope bound, a DEE step is a
pair `(r, t)` with link bounds, a thermal step adds a ratio.  LeanCert-style verified interval
evaluation is complementary: it can supply the continuous leaves (table entries as enclosures of
energies over voxels) that the present kernels take as input.

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
  `o(n)` terms that make it useless at any size one could simulate, at extensive accuracies
  only.  All upper bounds rest on Harper's theorem, which is cited, and on paper reductions
  to it.
* **The profile format answers a narrower question than §11.14 asked** (§11.17).  Certificates
  that do not grow with the chain exist for residuals that are functionals of pair-distance
  statistics, at extensive accuracy, and the bound that says so is numerically vacuous; a
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
| G7 | **Finite temperature**: thermal contact interval; free-energy certificates are quantizers of the Gibbs ensemble in exponential slack distortion; entropy bound; Hölder exponential-weights converse; exact exponent `R_β = max_Q R(Q; s, (F[Q] − F))` for accuracies that are not exponentially small | `gibbsProb_range_eq`, `mean_slack_le`, `card_ge_entropy`, `thermal_exp_weights`, `thermal_product_exp_weights`, `thermal_binary_exponential` **[V]**; exponent formula **[P]** | contact interval and fixed-`β` duality **known in spirit**; the exponent formula is a corollary of Merhav's (2011) theorem on exponential moments of distortion; the identification of certificate size with it, and the one-shot converses: no match found |
| G8 | **Second-order envelopes**: with bounded mixed differences, `n(k−1)+1` evaluations on a star give an exact pairwise sandwich; the extremal extensions are pairwise models; certified-minimiser criterion; order `m` in general.  The remainder is quadratic in the Hamming distance, so this is a way out only under weak second-order coupling (D32) | `secondOrder_remainder`, `pairwise_sandwich`, `verify_sound_secondOrder`, `secondOrder_envelope_exact`, `secondOrder_certified_minimizer_iff`, `higherOrder_remainder`, `higherOrder_remainder_sharp` **[V]** | anchored (cut-HDMR) decomposition **known**; as a certified uncertainty class with an exact reduction to the pairwise kernel: no match found |
| G10 | **Sampled free-energy sandwich**: `N` independent samples of a product reference pin `ln(Z/Z₀)` to `±\|β\|η + β²Σc_i²/8` outside an event of probability `2e^{−2Nη²/Σc_i²}` — polynomially many random evaluations where deterministic certification needs exponentially many | `sample_mean_two_sided`, `sampled_free_energy_sandwich`, `sampled_free_energy_sandwich_of_sample_size` **[V]** | standard concentration (Chernoff bound for a sub-Gaussian mean); stated as the constructive counterpart of G7 |
| G9 | **Compositional partition kernel**: cut rule and elimination rule (exact on every chain, with one leaf), with exponential separations from the elementary rules for every chain length — for certificates whose lower end is exact, and relative to the given representation of the instance (D33) | `zverify2_sound`, `WInstance.Z_cut`, `cut_rule_separation`, `WInstance.Z_elim1`, `WInstance.Z_elim2`, `zverify2Top_chainCert`, `chain_separation`, `ferroChain_separation` **[V]** | repair of the kernel; variable elimination is classical; the separation is the formal counterpart of E2 at finite temperature |
| G11 | **Query complexity of every algorithm**: sensitive alternatives must be detected (any class, any functional; deterministic and randomised), with a hedged spot-check converse; for the minimum, the instance-wise deterministic complexity *equals* the size of a value certificate, and every randomised algorithm (finite mixture) pays `(1−2δ)` times each fractional covering bound — attained by the hedged spot-check up to `ln(1/δ)`; for `ln Z`, a soft-gap radius for every algorithm and an upper bound for randomised ones in the same quantity, a lower bound on the randomised exponent with an upper bound in the same quantity, a machine-checked exponential gap between deterministic and randomised cost at the zero residual of the cube, and there a sharp worst-case accuracy threshold and the exponent in every accuracy regime | `exists_query_ne`, `prob_query_ne_ge`, `expected_queries_ge_packing`, `spotCheck_correct`, `instance_query_complexity`, `expected_queries_ge_exp_weights_min`, `binary_randomized_exponential`, `thermal_queries_strict_cover`, `thermal_queries_bracket`, `thermal_expected_queries_ge`, `thermal_product_randomized`, `cube_thermal_randomized_bound`, `detection_weight_ge`, `thermal_spotCheck_correct`, `cube_deterministic_lower_bound`, `exists_query_ne_pair`, `hedgedSpotCheck_correct`, `min_hedgedSpotCheck_correct`, `thermal_exact_dip_randomized`, `cube_exact_dip_randomized` **[V]**; single-letter forms and the upper bounds on the cube **[P + K]** | method **known** (radius of information; instance complexity; fractional block sensitivity as a bound on randomised query complexity); that randomisation helps for `ln Z` only above an accuracy scale is **known** for smoothness classes (Holzmüller–Bach 2025, §2.2); the instance-wise randomised bound with gap radii, the soft gap, and the exact threshold and accuracy diagram on the cube: not found |
| G12 | **Beyond the cube at finite temperature**: every slack-Lipschitz function is the centre of an admissible perturbation that must be detected (generalised dips), with a single-letter lower bound on product landscapes that is a game over the vertices of the Lipschitz polytope of a site — single dips are not extremal for three or more states; a two-reference sandwich that tensorises, the sharp accuracy threshold of every additive instance, and the worst-case threshold of the whole class without a hint, for every alphabet (the smallest oscillation of the tilted site pressure; for two-state sites the largest chord gap of the pressure) | `genDip_admissible`, `log_sum_exp_genDip_ge`, `genDip_expected_queries_ge_exp_weights`, `twoMeasureBound_pow`, `twoMeasureLower_pow`, `product_sandwich`, `product_mass_ge`, `detect_weight_le` **[V]**; product assembly, thresholds, the minimax identity and the algorithmic reading **[P]**; the matching upper bound of the exponent **[P]**, checked by an independent referee (R4) | found by independent workstreams (A, B; D confirms) and, for the hint-free threshold of general alphabets, in their synthesis; tools **known** (Chernoff and packing; tensorisation of exponential-moment inequalities; for the upper bound of the exponent: inherently typical subsets, Ahlswede–Yang–Zhang; isoperimetric exponents of two product measures, Ahlswede–Zhang, Yu — read by the referee); the upper bound of the exponent is a new statement with a known proof, and may follow from the fixed-measure theorem used as a black box; its evaluation as a matrix game, the lower bound, the thresholds and the application were not found |
| G13 | **Normal form**: a known part is the gradient part of an asymmetric envelope — value certificates of `(d, f, g)` are exactly the point certificates of `(σ, 0, f^d + g)`, `σ` the reduced cost of `d` under the Pasch–Hausdorff envelope `f^d`; a centre-form bound for best-first search valid for every admissible residual; best-first search is unboundedly worse than the smallest certificate on the line once there is a known part | `isValueCertificate_iff_normalForm`, `inf_add_phEnv_eq`, `certUB_normalForm`, `client_eq_centre`, `not_cocovered_centre` **[V]**; the search bound **[P]**; the line families computed | workstream C, verified by its reviewer; elementary (Johnson reweighting, min-plus adjointness); the packaging for certification apparently new; for `f ≡ 0`, symmetric `d` the covering characterisation and the hardness gadget are **known** (Hetland 2020), and the search bound is the known packing argument |
| G14 | **Dense second-order classes**: a second-order dip; the uncertainty after any evaluations is at least `c·C(d+1, 2)` at Hamming distance `d` from the evaluated set; unions of stars give exactly the best single-star bound; covering sandwich for the certificate size; full exponent for constants of order one, a rate–distortion exponent with a square-root budget and a transition at `e/γ = 1/4` for mean-field constants; a three-legged spider beats the star | `SecondOrderDip.dip_mixedDiffBound`, `SecondOrderDip.dip_witness`, `SecondOrderDip.stars_do_not_combine` **[V]**; sandwich, asymptotics, spider **[P]**, verified by a reviewer with linear programmes over the whole class | workstream E (D found the dips independently); the `Θ(n²)` law is **known** for approximate modularity (Chierichetti–Dasgupta–Kumar 2020); the covering sandwich, the non-combination of stars and the spider were not found |
| G15 | **Free energies beyond first-order product classes**: second-order classes have a transition at the Curie–Weiss coupling `βc₂n = 4` (polynomial below by Dobrushin uniqueness, exponential above by droplets); the accuracy threshold on the torus of angles is `Σ_i ln(sinh b_i/b_i)`; Boltzmann averages are uncertifiable on most of their a-priori range; the constant of the soft-gap sampler does not depend on the residual | `SecondOrderDip.dip_mixedDiffBound`, `sum_gibbs_exp_softGap_indep`, `spotCheck_const_le_cover` **[V]**; the three theorems **[P]**, re-derived by a reviewer | workstreams D and G; the two-regime picture and the order in fixed dimension are **known** (Holzmüller–Bach 2025); the transition for second-order classes, the torus threshold and the result on averages were not found (the reviewer's literature search was cut short) |
| G16 | **Chain geometry**: the verified torsion-to-RMSD constants grow like `m^{3/2}` with the distance to the chain end (lever-arm law); with constants growing like any positive power, weighted-Hamming envelopes make certification exponential with almost full exponent; used directly, the RMSD envelope costs a stretched exponential `exp(Θ̃(√N))` at the zero residual; contact residuals force growing constants in every torsion-Hamming envelope | **[P]** from machine-checked bounds (`card_ge_exp_weights`, `expected_queries_ge_exp_weights_min`, `thermal_expected_queries_ge`); two constants numerical | workstream G, checked by a reviewer with own geometry code; lever-arm effects are folklore in molecular modelling, the quantitative consequences for certification were not found (no literature search was possible in the review) |
| G17 | **Chains as known parts**: one evaluation certifies iff every contiguous droplet is sharp (`c ≤ τ`, a minimum-ratio cycle; `2h` for the Ising ferromagnet); the exponent of homogeneous chains is `sup_ν R_ν(e(ν))` over stationary processes; the transfer-matrix (Boltzmann) bound vanishes on the window `2h < c ≤ 2(J+h)`; the soft gap of a chain is a pinned free energy | **[P]**, re-derived by a reviewer (no Lean) | workstream B; the exactness criterion at zero field is **known** (Gray's critical distortion); the droplet criterion, the exponent theorem and the vacuous window were not found (no literature search was possible in the review) |

| G18 | **Without a hint on the cube**: the exponent of non-adaptive algorithms is `min{KL(ρ‖½) : KL(ρ‖p_u) ≤ ε₁}` at extensive accuracies and `KL(p_u‖½)` at every fixed accuracy — plain Monte Carlo attains it on the whole class (tail lemmas: above a threshold the mass is at most the excess of a dip on a ball of the size of the super-level set, below it at least that of a cone around such a ball), and no non-adaptive algorithm does better (cones against cones with a flattened bottom); two independent samples give a certified bracket that needs no hint at the zero residual for `ε > 2`; an adaptive algorithm that is correct on the class needs `n + 3` evaluations on a cone (for adaptive algorithms see G20) | `nonadaptive_expected_queries_ge`, `cube_nonadaptive_bound` (conditional on two finite sums), `weight_le_of_outside`, `sum_le_truncated_add_tail`, `weight_ge_of_inside`, `sum_truncated_ge` **[V]**; Harper's theorem **[K]**; the reductions to it, the closed forms, all exponents and the probabilistic statements **[P]** | cycle 10, refereed (`reviews/R5`); the sample size `e^{KL(π‖uniform)}` at one instance is **known** (Chatterjee–Diaconis 2018) and the *method* of the non-adaptive lower bound — hidden cone centres, Bakhvalov averaging, defeated by adaption — is **known** (Mathé–Novak 2007, for log-concave densities with a Lipschitz logarithm); the exponent on the cube for `ln Z` and the matching class-wide upper bound were not found |
| G19 | **Correlated uncertainty**: for residuals that are linear in known features with coefficients in a box, the envelope is a pulled-back weighted `ℓ¹` distance, every linear combination of evaluations brackets the value at a new point by the unexplained part of its feature vector (worst case over the data: the `ℓ¹` distance to the span, against the distance to the nearest point for the first-order class of the same envelope), and rank-many evaluations determine everything; pair-additive residuals with unknown Lipschitz radial functions are linear in cumulative pair-count profiles, their envelope is a transport distance between pair-distance distributions, sharpness is stochastic dominance, and at extensive accuracy certificates in this format exist whose size does not depend on the chain length; a kernel certifies minima for all coefficient vectors consistent with evaluated anchors | `linRes_sub_le`, `linRes_sub_attained`, `linRes_span_upper`, `linRes_span_lower`, `linRes_span_exact`, `sumClass_span_upper`, `sumClass_span_lower`, `pairRes_eq_cum`, `pairRes_sub_le`, `pairRes_span_upper`, `pairRes_span_upper_enclosure`, `pairRes_sharp`, `verifyLTop_sound`, `contactTriangle_bound` **[V]**; exactness (duality), the transport form, the entropy bound and everything about chain length **[P]** | cycle 10, refereed (`reviews/R6`) except the kernel; the linear theory is **known** (optimal recovery: Smolyak, Micchelli–Rivlin; set-membership estimation; robust linear programming), the features are those of linear contact potentials (Maiorov–Crippen 1992; Tobi et al. 2000), the distance is **known** as a descriptor distance (Osada et al. 2002; bag of bonds), the entropy of monotone functions is classical; its reading as the exact envelope of a residual class next to a known part, and the consequences for certificates, were not found; **none of it is deep** |
| G20 | **Adaptivity replaces the hint**: on the cube class the worst-case exponent of adaptive randomised algorithms without a hint is the hinted exponent `θ_hint(ε₁) = KL((Λ₁+ε₁)/u‖½)`, strictly below the non-adaptive `θ_na`.  A two-level "layer-cake" algorithm — uniform outer sample, brackets of the fibre averages refined only as far as a one-sided test against a ladder of levels requires, the tail lemma once at the top — turns bracket procedures with exponent function `T` into ones with `R[T]`; by the identity `θ_na(e + θ_hint(e)) = θ_hint(e)` (that is, `KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁`) the hinted exponent is a fixed point of `R`, every nonincreasing `T ≤ R[T]` lies below it, and the iteration from `θ_na` converges to it; on radial instances a direct adaptive algorithm has the hinted exponent | `superSolution_le_hint`, `iterates_lt_hint_add`, `step_from_hint_le`, `klBin_shift`, `cubePair`, `cube_iterates_lt_hint_add`, `cube_hint_superSolution`, `LayerCake.mean_le_upper`, `LayerCake.upper_le_width`, `LayerCake.close_points_bound` **[V]** (analysis of the recursion, abstractly and for the exponent functions of the cube; validity and width of the bracket; the two algebraic inequalities behind the cost); the algorithm's number of evaluations, the induction over levels and all asymptotics **[P]** | cycle 10, refereed (`reviews/R7`: "proved with gaps", the gaps written into the text; no error found in the cost accounting beyond one closure rule); the two-level algorithm and the recursion are due to workstream H, the oracle-relative form, the identity and the convergence proof to the coordinator; relatives of the algorithm are nested sampling, multilevel splitting and nested simulation, adaption with polynomial gains is known in information-based complexity (Heinrich; Kunsch–Novak–Wnuk) — a certified version with a worst-case exponent, and the statement that adaption recovers the value of a hint exactly, were **not found** (abstracts only) |

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
found.
Each rests on textbook tools (type covering, Hölder, telescoping, linear-programming duality);
the proofs are short.  The second referee's verdict on G1–G10 — "a coherent note, not a
theorem-driven paper" — is reproduced in §12 together with what a publication would still
need.

**The picture after cycle 10, in one table.**  What each *kind of knowledge about the
residual* costs, in evaluations of the residual, for an accuracy that is a fixed fraction
of the system size (`n` sites, or `N` beads).  Every entry is a theorem of this report with the
status given there; the table adds nothing, it only puts side by side what was proved in
different sections.

| what is known about the residual `g` | certificate / deterministic procedures | randomised, told the instance in advance ("hint": the task is *verification*) | randomised, no hint, sample fixed in advance | randomised, no hint, adaptive (*search*) |
|---|---|---|---|---|
| **first-order**: `g(x) − g(y) ≤ d(x,y)`, weighted Hamming `d`, product landscape | a covering by slack balls (`isCertificate_iff_cover`); exponential, `exp(nR*)`, unless every site is sharp (Theorems 11.6–11.9); `2^{n(1−o(1))}` on the cube at the zero residual | `exp(n θ_hint(ε₁))` below an accuracy threshold, a bounded number above it (Theorems 11.25, 11.28); single-letter game value at additive instances (11.27) | cube, zero known part: `exp(n θ_na(ε₁))`, `θ_na > θ_hint` (Theorems 11.44, 11.45) | cube, zero known part: `exp(n θ_hint(ε₁))` — the hint is worth nothing (Theorem 11.54) |
| **second-order**: mixed differences bounded by `c_ij` | a star of `n + 1` evaluations determines `g` up to `Σ c_ij` over the changed pairs (`secondOrder_remainder`); with dense constants of order one the cost is exponential again (Theorem 11.31, D40) | a transition at finite temperature (Theorem 11.33) | — | — |
| **linear in `p` known features**, coefficients in a box | `rank ≤ p` evaluations determine `g` everywhere; before that, every linear combination of evaluations gives a bracket (`linRes_span_upper`, `linRes_span_exact`); a kernel for minima (`verifyLTop_sound`) | no lower bound known (a generic evaluation sees every perturbation) | — | — |
| **pair-additive with `L`-Lipschitz radial functions** (chains) | number of evaluations bounded independently of `N` at extensive accuracy, by a numerically vacuous bound; polynomial on lattices at every accuracy (Proposition 11.49) | — | — | — |
| **first-order in a per-torsion envelope** (chains) | `exp(Θ(N))`: the verified constants grow with the lever arm (Theorem 11.37, D42) | — | — | — |

Three readings.  (i) *The kind of class decides, not its size*: the same weighted `ℓ¹` distance
costs `2^{n(1−o(1))}` as an envelope and `n` evaluations as the feature distance of a linear class
(§11.17).  (ii) *Verification against search*: with a hint the task is to verify a claimed
instance, without it to search; for deterministic certification of a minimum, search can be
unboundedly more expensive than the smallest certificate even on the line (§11.11, D39),
whereas for randomised estimation of `ln Z` on the cube class the worst-case costs of the two
have the same exponent — provided the search is adaptive.  (iii) *What is missing* is every
entry marked "—", all of the last three columns outside the cube with a zero known part,
and constants everywhere.

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
available to us only through an automatic summary, so its exact conditions are **[K, not
verified in detail]**.  What was not found is the identification — the complexity of
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
min-plus product, with `d⊗g = g` on the class; the reviewer judged the packaging new for this
problem.  Harness XI.14 (all evaluated sets of random instances, including asymmetric envelopes
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

**Theorem 11.36 (lever-arm law) [P upper bound; lower constant numerical].**  The verified
constants of Theorem 4.6 satisfy `c_i ≥ 0.824·Λ b m_i^{3/2}` (`Λ = L/√N`) for every position, and
the smallest constants for which the weighted-Hamming envelope is valid are at least
`0.186·Λ b m_i^{3/2}` (computed for `m ≤ 10⁵`; a proved bound has the same power with a smaller
constant).  The cause is geometric: the moment of inertia of an arm of `m` atoms about a
torsion axis grows like `m³` for extended and helical conformations.

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
referee).  The first-order class of `d_P` is the class of Lipschitz functionals of the
pair-distance statistics.
(c) After evaluations, for every `λ`:
`|g(y) − Σ_i λ_i v_i| ≤ L Σ_τ ‖N^y_τ − Σ_i λ_i N^{x_i}_τ‖_{L¹}` (`pairRes_span_upper`, `pairRes_span_lower`;
with an enclosure of the profile of `y` over a voxel of conformations in place of the profile,
`pairRes_span_upper_enclosure`).  As in Theorem 11.47(b), each end is exact after its own
optimisation, and the half-width is at most `L` times the `L¹` distance from the profile of `y`
to the *span* of the evaluated profiles, with equality at the zero data.

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
extensive accuracy whose number of evaluations does not depend on the chain length, and that
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

The off-lattice profile column still grows geometrically at these sizes: the saturation
promised by Proposition 11.49(a) is not visible below `N ≈ 16` except in the three-feature
lattice model.

*Prior art.*  Theorem 11.47(a)–(c) is optimal recovery of a linear functional from linear
information over a box (Smolyak; Micchelli–Rivlin 1977) in its worst-case part and plain
linear-programming duality — the feasible-set intervals of set-membership estimation
(Milanese–Vicino 1991), robust linear programming with box uncertainty (Soyster 1973) — in its
data-dependent part.  Potentials that are linear in pair counts per type and distance bin,
determined by linear inequalities over decoys, are those of Maiorov–Crippen (1992; known to
us through Tobi–Shafran–Linial–Elber 2000, who use exactly these features).  The size of the
coefficients as an "extrapolation grade" is the D-optimality criterion of active learning for
potentials that are linear in features (Podryabinkin–Shapeev 2017; their grade is the `ℓ^∞`
size of the multipliers, the transport term of (d) a weighted `ℓ¹` size).  The `L¹` distance of
cumulative distance distributions as an earth mover's distance between shapes is in Osada et
al. (2002), sorted pair descriptors compared in `ℓ¹` are the "bag of bonds" (Hansen et al.
2015), and Wasserstein distances between radial distribution functions are used as
structural similarity scores; the entropy of monotone functions is classical
(Birman–Solomyak; van de Geer), as are greedy reduced bases (Binev et al. 2011;
DeVore–Petrova–Wojtaszczyk 2013; their use for greedily chosen evaluation points in
worst-case recovery is the `P`-greedy algorithm, Santin–Haasdonk 2017), the width of a box in
`ℓ¹` (Pietsch 1974; Stesin 1975) and transport with a boundary reservoir (Figalli–Gigli 2010).
Not found in print, and immediate once named: the profile distance read as the *exact*
envelope of the class of unknown Lipschitz pair potentials next to a known part, the count
of evaluations that follows, and the comparison with the first-order class of the same
envelope.  Verification status of each citation: `prior_art/L8_linear_classes.md`.

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

**Theorem 11.53 (the recursion converges to the hinted exponent) [V] (`HintRecursion.lean` for an abstract pair of exponent functions; `CubeHintPair.lean` for the functions of the cube).**
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
2024).  **That adaption can remove an exponential barrier of non-adaptive randomised methods
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

---

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
   in cycle 10* (§§11.16, 11.18): non-adaptive algorithms have the exponent
   `θ_na(ε₁) = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ ε₁}` (and `KL(p_u‖½)` at every fixed accuracy), adaptive
   ones the hinted exponent `θ_hint(ε₁) = KL((Λ₁+ε₁)/u ‖ ½)`.  Open: (i) **bounded accuracy** —
   the adaptive upper bound is for `ε = ε₁n`; at `ε = O(1)` the adaptive exponent lies between
   `h = θ_hint(0+)` and `a = θ_na(0+)`, and the nested brackets have accuracy `gn + O(log n)` by
   construction; (ii) **finite sizes** — the `o(n)` terms of `k` nested levels are not
   quantified, and at `n = 32` the algorithm loses to plain Monte Carlo on every instance;
   is there an adaptive algorithm that wins at sizes that can be simulated, or a lower bound
   showing that the gain needs `n ≫ 1/θ_hint`?  (iii) **instance by instance** — the zero
   function is the hardest instance with a hint (a corollary of Theorem 11.54); is there an
   adaptive algorithm without a hint that matches the hinted cost at *every* instance up to
   `e^{o(n)}`, cheap instances included?  (iv) **other spaces** — the proof needs a tail lemma on the outer
   block (an isoperimetric inequality with nested extremal sets), Lipschitz fibre averages,
   and a distance that is additive over blocks; product measures and larger alphabets with
   a weighted Hamming distance should be within reach (asymptotic isoperimetry of
   Ahlswede–Zhang; from memory), whereas for Euclidean Lipschitz functions on Gaussian space
   neither the lower bound (half-spaces are detected from far away) nor the algorithm (blocks
   are not cheaper) transfers, and no exponent is known to us;
   (v) **a machine-checked count** — the number of evaluations of the two-level algorithm is
   a paper proof, in a part of the argument where three wrong versions preceded the right one.
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
   bound that is numerically vacuous.  Open: (a) the true entropy and widths of the profile
   sets of chains, i.e. the size at which the independence of the chain length sets in (not
   reached at 16 beads except in a three-feature lattice model), and a thermodynamic limit
   theorem for certificate sizes (workstream P, §5); (b) an upper bound for the class
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
that could not be read in full).  Principal
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
