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
quoted below (B1–B7) are from one run of `experiments/separation_benchmarks.py` (seed 7), whose
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
3. **Two semirings, one certificate algebra.**  The same rules (reparameterise, branch, dominate,
   decompose) are sound for minimum energies (`(min,+)`) and for partition functions (`(+,×)`),
   with dominance acquiring the temperature-dependent factor `1 + e^{−βγ}` (§3.1, §6).
4. **Weight-domain and rational-atlas semantics.**  Partition-function certificates live in the
   domain of rational Boltzmann factors; torsion circles are covered by four rational charts
   `t ↦ ((1−t²)/(1+t²), 2t/(1+t²))`, `|t| ≤ 1/2`, so checkers need no transcendental functions (§5).

### 0.2 Results at a glance

| # | Result | Lean | Novelty assessment after prior-art review |
|---|---|---|---|
| A1 | **Contact-set theorem**: `x` can be optimal for some admissible residual ⇔ `E₀(x) ≤ E₀(y) + d(y,x) ∀y` | `robust_minimizer_iff` **[V]** | elementary (McShane/Lipschitz duality); formulation for dominance pruning with a black-box residual: no match found |
| A2 | **Sharp-minimum theorem**: `x` optimal for every admissible residual ⇔ `d(x,y) ≤ E₀(y) − E₀(x) ∀y` | `robust_certified_iff` **[V]** | as A1 |
| A3 | **Query-model theorem**: with evaluated anchors, `x` can be optimal ⇔ contact ∧ `E₀(x)+L(x) ≤ E₀(y)+U(y) ∀y` (`L, U` McShane envelopes) | `robust_minimizer_with_anchors_iff` **[V]** | optimality statement for pruning intervals not found in the literature (iMinDEE is the one-anchor, discrete-envelope case) |
| A4 | **Exact robust interval** for `min(E₀+Δ)` and for `Z_β(E₀+Δ)`, all β | `robust_min_bracket`, `robust_partition_bracket` **[V]** | elementary; not found stated |
| A5 | **Witness-size lower bound**: an ε-certificate must evaluate the residual on every state with gap `< (1−κ)σ − ε` | `anchor_necessary`, `anchor_card_lower_bound` **[V]** | discrete counterpart of certified Lipschitz optimisation bounds; not found for structured discrete landscapes |
| A6 | Energy window is the exact limit with global bounds only | `energy_window_exact` **[V]** | known in spirit (energy-window DEE); exactness statement makes the "bottleneck" information-theoretic |
| A7 | Local differential envelopes ⇒ global envelope; differential DEE is sound | `admissible_of_single_site`, `differential_dee_sound` **[V]** | MinDEE range terms are a special case; general form not found |
| A8 | Goldstein = exact dominance margin; gauge invariant; = gauge-optimal Desmet | `goldstein_isLeast`, `goldstein_gauge_invariant`, `desmet_optimalGauge` **[V]** | **known/folklore** (Shekhovtsov 2014/2016); negative answer to the seeded "dual-reparameterised pruning" conjecture |
| D1 | **Dominance transport / thermal DEE**: `Z(A) ≤ e^{−βγ} Z(S)`; pruning changes `ln Z` by `≤ ln(1+e^{−βγ})` | `partition_transport`, `freeEnergy_prune_bracket`, `thermal_dee` **[V]** | inequality folklore; as a certificate rule for partition functions: no match found |
| D2 | **Free-energy sandwich** `−β⟨Δ⟩₀ ≤ ln(Z/Z₀) ≤ −β⟨Δ⟩₀ + β² Σc_i²/8`; the worst residual in the bounded-difference class is additive and two-level; `1/8` is optimal | `bounded_differences_sandwich`, `exists_two_level_worst_residual`, `mcdiarmid_no_better_constant` **[V]** | inequality known in spirit (Jensen + McDiarmid; Rio 2013 for the sharp function); the attainment statement is implicit in the literature and is stated and machine-checked here |
| D3 | **Partition-function kernel** with leaf/branch/thermal-prune rules; enclosure of the real `Z` | `zverify_sound`, `Z_encloses_partitionFn` **[V]** | verified checkers exist for exact model counting only; this rule set: no match found |
| D4 | **Voxel enclosure**: continuous Boltzmann integrals → rational kernel, with the volume (entropy) factor; separable (second-order) envelopes factor an `M`-dimensional voxel integral into `M` one-dimensional ones | `voxel_boltzmann_bounds`, `certified_voxel_partition`, `separable_voxel_bounds` **[V]** | `K*`-family algorithms use minimised voxel energies; rigorous voxel-integral bounds: no match found |
| D5 | Hölder decomposition with temperature rescaling | `partitionFn_holder`, `freeEnergy_holder` **[V]** | **known** (weighted mini-bucket) |
| C1 | Hoffman–Wielandt and von Neumann trace inequality (real symmetric) | `hoffman_wielandt` **[V]** | **classical** (1953); formalization |
| C2 | Trace-enhanced spectral obstruction: `min_X ‖D̂ − Δ(X)‖²_F ≥ 4 Σ_{k>r} λ_k² + (4/(r+1)) (Σ_{k>r} λ_k)²` | `rank_psd_trace_obstruction`, `sstress_lower_bound` **[V]** | **known** with these constants (Sonthalia et al. 2021; K-identity in Tsang–Pereira 2016); first machine-checked proof, down to Hoffman–Wielandt |
| C3 | Cycle-holonomy obstruction; SE(3) translation holonomy with lever arms | `norm_holProd_le_sum`, `norm_holTrans_le` **[V]** | triangle bound **known** (Lerman–Shi 2022, Lemma 1); a sharp non-abelian Hodge-type bound is open |
| C4 | **Finite-angle torsion → RMSD**: exact coaxial cost `2S − 2√(S² − 4 I_A I_B sin²(φ/2)) ≤ 4 min(I_A,I_B) sin²(φ/2)`; chain rule; envelope for invariant Lipschitz residuals | `exists_coaxial_angle`, `coaxial_cost_le_min`, `rigidWithin_torsion_chain`, `residual_torsion_chain` **[V]** | small-angle content classical (Pitzer–Gwinn; Eckart); finite-angle closed form and chained bound: no match found |
| B1 | Outward rounding, rational intervals, certified `exp`, rational circle atlas | `Core/Rounding.lean` **[V]** | infrastructure; verified interval libraries exist (LeanCert, girving/interval) |
| E1 | **Master Soundness Theorems** for the tropical, residual and sum–product kernels | `verify_sound`, `verifyR_sound`, `certified_gap`, `zverify_sound` **[V]** | no verified checker for this problem class found |
| E2 | Exponential separation: sum-free certificates need exactly `2^m` leaves on `m` frustrated triangles, `2m` suffice with `sum`; LP gap of the triangle | `sumFree_exponential`, `sumFree_tight`, `sum_linear`, `sum_rule_separation`, `triangle_no_leaf_certificate` **[V]** | **known phenomenon** (Basu et al. 2023; Jeroslow 1974); formalized for this kernel incl. DEE steps |

The honest reading of the last column: the *mathematical* content of most individual statements
is elementary, classical, or — as three independent literature checks established — already in
print (A8, D2, D5, C1, C2, E2).  What the program contributes is (i) the envelope formulation and
the exact, closed characterisations A1–A5 that it makes possible; (ii) temperature-aware dominance
and voxel enclosures as *certificate rules* (D1, D3, D4); (iii) finite-angle torsion-to-RMSD
certificates and the resulting envelope for SE(3)-invariant residuals (C4); and (iv) a
machine-checked certificate algebra and library covering all of it, including first
formalizations of several known results.

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
    F_β(S) − β^{-1} ln(1 + e^{−βγ}) ≤ F_β(A ∪ S) ≤ F_β(S),

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

Consequently *dual reparameterisation cannot improve dominance pruning for pairwise energies on
product domains*.  This answers the seeded question of Direction A in the negative and locates
where dual methods do matter:

* **Higher-order terms [P].**  With 3-body terms the difference energy at site `i` is a pairwise
  model on the *link graph* of `i` (vertices: neighbours; edges: pairs sharing a 3-body term with
  `i`).  Exact dominance is the minimisation of that model: linear time when the link graph is a
  forest (e.g. chain-local terms `T_{i−1,i,i+1}`, whose link graph is a path on four sites),
  exponential only in its treewidth in general, and coNP-hard without restriction (given a
  pairwise model `g` on the neighbours put `T(r,·,·) = g`, `T(t,·,·) = 0`; then `t` dominates `r`
  iff `min g ≥ 0`).  Any dual bound on the link model yields a sound criterion between the nested
  sum-of-minima rule and exact dominance.
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

So a configuration is certifiably optimal *without evaluating the residual anywhere* iff the
white-box energy grows away from it at least as fast as the envelope — a stability condition of
Bilu–Linial type measured in the envelope metric.

**Theorem 2.5 (McShane brackets) [V].**  Let the residual be evaluated on a finite anchor set `A`
with consistent values `v`.  The envelopes

    L(y) = max_{a∈A} [v(a) − d(a,y)],      U(y) = min_{a∈A} [v(a) + d(y,a)]

are admissible, interpolate `v`, and satisfy `L ≤ g ≤ U` for every admissible `g` agreeing with
`v` (`lowerEnv_admissible`, `upperEnv_admissible`, `lowerEnv_eq_of_mem`, `lowerEnv_le`,
`le_upperEnv`).  Hence for every finite `S` and every `β ≥ 0`

    min_S (f + L) ≤ min_S (f + g) ≤ min_S (f + U),
    Z_β(f + U; S) ≤ Z_β(f + g; S) ≤ Z_β(f + L; S),

and both ends are attained inside the class: **no certificate using the same information can
report a tighter interval** (`robust_min_bracket`, `robust_partition_bracket`).

With the site-additive envelope and one anchor `a`, `f + L = v(a) + [E₀ − Σ_i δ_i(a_i, ·)]` is
again a pairwise model: *the residual's envelope is absorbed into the one-body tables*.  This is
the reduction used by the residual kernel (`PairInstance.anchored`, §6) and it means every
decomposable-energy algorithm lifts to the residual problem at the cost of one modified instance
per anchor.

**Theorem 2.6 (query model: exact pruning with evaluated anchors) [V].**  With anchors `(A, v)`
as above,

    ∃ g admissible with g|_A = v and x ∈ argmin(f + g)
        ⇔   (∀y, f(x) ≤ f(y) + d(y,x))   ∧   (∀y, f(x) + L(x) ≤ f(y) + U(y)).

*Proof.*  (⇒) The first condition is Theorem 2.3; the second is `L(x) ≤ g(x)`, `g(y) ≤ U(y)`.
(⇐) Put `γ = L(x)` and `g(y) = min(U(y), γ + d(y,x))`: a minimum of two admissible functions is
admissible; `g = v` on `A` because `γ + d(a,x) ≥ v(a)`; `g(x) = γ` because `L ≤ U`; and
`f(x) + γ ≤ f(y) + g(y)` is exactly the two hypotheses. ∎

The set violating one of the two conditions is therefore the **exact** set of configurations that
may be discarded after the given evaluations.  For an anchor `y` the second condition reads
"optimistic value of `x` ≤ evaluated value of `y`", i.e. *lower bound ≤ incumbent*: with one
anchor and the discrete envelope this is the pruning interval of minimised DEE (iMinDEE), which
Theorem 2.6 shows to be optimal in the query model and extends to arbitrary envelopes and any
number of evaluations.

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

*Prior art.*  McShane–Whitney extension and Piyavskii–Shubert Lipschitz optimisation are
classical; MinDEE's range terms (Georgiev–Lilien–Donald 2008) are a bounded-difference envelope
in Desmet form and iMinDEE's pruning interval (Gainza–Roberts–Donald 2012) is a one-anchor
instance; LUTE/EPIC (Hallen et al.) treat non-pairwise energies with *fitted*, uncertified
residuals; many-body DEE (LuCore et al. 2015) truncates the expansion without carrying the
remainder into the test.  A dominance/pruning theory for an abstract black-box residual with an
envelope, exactness statements, or a query-model optimality theorem were not found
(`prior_art/L1` §C2).

### 2.4 Witness-size lower bound

**Theorem 2.7 (anchors are necessary) [V].**  Let the true residual `g` be `κ`-Lipschitz for the
envelope (`g(x) − g(y) ≤ κ d(x,y)`, `κ ≤ 1`), let `A` be the anchor set of an `ε`-certificate
(`min_A (f+g) − ε ≤ f + L` everywhere), and let `E* ≤ min_A (f+g)`.  If `y` is `σ`-separated from
all other anchors and `(f+g)(y) − E* < (1−κ)σ − ε`, then `y ∈ A`.  With uniform separation `σ`,

    |A|  ≥  #{ y : (f+g)(y) − E* < (1 − κ) σ − ε }.

*Proof.*  If `y ∉ A`, `L(y) ≤ g(y) − (1−κ)σ`, so the certified bound is at most
`(f+g)(y) − (1−κ)σ`, while the incumbent is at least `E*`. ∎

For the weighted Hamming envelope `σ = min_i c_i`.  The bound has a direct physical reading:
*the number of residual evaluations any certificate must contain is at least the number of
states in the energy shell of width `(1−κ) c_min − ε` above the optimum* — the microcanonical
count at the resolution of the envelope.  A loose envelope (small `κ`, i.e. certified constants
much larger than the residual's true variation) is paid for in entropy.  Benchmark B2 (8 states):
with `κ = 0, ε = 0` the bound forces 5.9 anchors on average against a brute-force optimum of
6.25; with `κ = 0.9, ε = 0.2` it forces none while the optimum is 2.2 — the bound is tight for
loose envelopes and vacuous for nearly extremal residuals, as it should be.

This is the structured, discrete counterpart of instance-dependent certification bounds for
Lipschitz optimisation (Bachoc, Cesari, Gerchinovitz, NeurIPS 2021); see §7 for its consequences
for architectures.

---

## 3. Direction D — partition functions and free energies

### 3.1 Thermal dead-end elimination

Theorem 2.1 on a product box (`thermal_dee` **[V]**): if `t ∈ D_i`, `t ≠ r` and
`E(x[i↦t]) + γ ≤ E(x)` for all `x` in the box with `x_i = r`, then deleting `r` multiplies the
partition function of the box by a factor in `[(1+e^{−βγ})^{-1}, 1]`.  In the weight domain the
same rule is checked factor by factor (`PruneZOK`, `zprune_sound` **[V]**): if
`w_i(r) ≤ q₀ w_i(t)` and `W_ij(r,s) W_ji(s,r) ≤ q_j W_ij(t,s) W_ji(s,t)` for all `s ∈ D_j`, then
`Z ≤ (1 + q₀ ∏_j q_j) Z'`.  Rounds compose multiplicatively, so a pruning schedule with margins
`γ_k` certifies `0 ≤ ln Z − ln Z_pruned ≤ Σ_k ln(1 + m_k e^{−βγ_k})` (`m_k` states mapped to one
survivor in round `k`).

### 3.2 The free-energy sandwich

Let `μ₀ ∝ e^{−βE₀}` be the reference ensemble and `⟨·⟩₀` its expectation.

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

So one reference expectation plus the envelope constants pin `ln Z` in an interval of width
`β² Σ c_i²/8`, quadratically smaller than the trivial `β Σ c_i` when `β c_i < 8`; and the worst
non-decomposable residual is a fully decomposable one — the exact supremum of the gap over the
class is `Σ_i max_{A_i} ln(p_i e^{βc_i(1−p_i)} + (1−p_i) e^{−βc_i p_i})`, `p_i = μ_i(A_i)`.

*Sharper and more general forms [K].*  The exact extremal function is Rio's
`ℓ(t) = sup_r [ln(1 + r(e^t − 1)) − tr] ≤ t²/8` (Rio 2013, Lemma 4.1): the gap is at most
`Σ_i ℓ(β c_i)`, which grows only linearly in `β` at low temperature (benchmark B4: at `βc = 10`,
`Σℓ = 40.2` against the Gaussian bound `75` and `36.1` attained by the worst additive residual for
the sampled reference).  For Markov or Dobrushin references the constants become
`‖Γ c‖²` with `Γ` a Wasserstein matrix, `‖Γ‖ ≤ (1−θ)^{-1}` (Kontorovich–Ramanan 2008;
Kontorovich–Raginsky 2016).  A uniform bound `ln⟨e^{−β(Δ−⟨Δ⟩)}⟩₀ ≤ β²C/2` over all admissible
residuals is *equivalent* to the transport inequality `W_{1,d}(ν, μ₀) ≤ (2C·KL(ν‖μ₀))^{1/2}`
(Bobkov–Götze 1999): the envelope metric of §2 is exactly the cost in which the reference
ensemble must satisfy T₁.  The same inequality is used for model-bias quantification by
Gourgoulias et al. (2020); we found no statement of it as a certified free-energy-perturbation
bound, but claim no mathematical novelty for (a)–(c), (e).  Statement (d) is implicit in Rio's
proof and in his additive Bernoulli examples; the literature check found no explicit statement,
in particular none for a *fixed* product reference, where the supremum is restricted to the
achievable masses `p_i = μ_i(A_i)`.  It is specific to the moment generating function: for tail
probabilities the extremal problem has non-additive solutions (Owhadi et al. 2013).

*Limitation.*  The gap is extensive: with `c_i = 0.5` kcal/mol on 100 torsions at 298 K it is
≈ 5 kcal/mol.  The sandwich certifies free energies only for `β c_i ≪ M^{-1/2}`, or after
localisation — applying it cell by cell in a branch-and-bound partition, where cell-local
oscillations make the gap second order in the cell width.

### 3.3 Exact interval with evaluated anchors

Theorem 2.5 at finite temperature: `Z_β(E₀+U) ≤ Z ≤ Z_β(E₀+L)`, attained.  With one anchor and
the site-additive envelope both ends are partition functions of pairwise models with modified
one-body tables (two transfer-matrix computations when `E₀` is a chain).

### 3.4 Certified partition functions: weight domain, kernel, voxels

*Weight domain.*  A `WInstance` stores rational Boltzmann factors.  If two instances bracket the
true factors, their exact rational partition sums bracket the real partition function
(`Z_encloses_partitionFn` **[V]**).  The brackets come from the certified rational enclosure of
`exp` (`exp_enclosure`, `contains_boltzmann` **[V]**, §5).

*Kernel.*  `zverify` returns a rational interval for `Z` over a box from a certificate built
from three rules — factorised leaf (pair factors replaced by certified constants, the remaining
product measure summed exactly as `∏_i Σ_a w_i(a)`), branch (additivity over the states of a
site), thermal prune — and `zverify_sound` **[V]** proves `lo ≤ Z ≤ hi`.

*Voxels.*  For a measurable voxel `V` of finite volume with `E_lo ≤ E ≤ E_hi` on `V`,

    vol(V) e^{−βE_hi} ≤ ∫_V e^{−βE} ≤ vol(V) e^{−βE_lo}        (`voxel_boltzmann_bounds` [V]),

and over a finite family of disjoint voxels indexed by the configurations of a box, rational
instances whose weights bracket the voxel integrals have partition sums that bracket the
continuous integral (`Z_encloses_voxel_integral`, `certified_voxel_partition` **[V]**).  The
factor `vol(V)` is the conformational entropy of the voxel, which the minimised-energy surrogate
`e^{−βE_min}` used by the `K*` family omits; with it the same enumeration yields a two-sided
bound on the *integral*.

*Second order: separable envelopes [V] + Taylor step [P].*  If on a product voxel `∏_i s_i` the
energy is bracketed by separable functions, `Σ_i φ_i(x_i) ≤ E(x) ≤ Σ_i ψ_i(x_i)`, then

    ∏_i ∫_{s_i} e^{−βψ_i}  ≤  ∫_{∏ s_i} e^{−βE}  ≤  ∏_i ∫_{s_i} e^{−βφ_i}

(`separable_voxel_bounds` **[V]**, Fubini on the box), and if `ψ_i ≤ φ_i + w_i` the two products
differ by at most the factor `exp(β Σ_i w_i)` (`separable_voxel_ratio` **[V]**).  A second-order
Taylor expansion with a diagonal Hessian enclosure `m·I ⪯ ∇²E ⪯ M·I` on a box with centre `c` and
half-widths `h_i`,
`E(c) + g·u + (m/2)|u|² ≤ E(c+u) ≤ E(c) + g·u + (M/2)|u|²`, is exactly such a pair of separable
envelopes with `w_i = (M−m) h_i²/2` **[P]** (the Taylor step is standard and not formalized).
Consequences: (i) an `M`-dimensional voxel integral is certified by `M` one-dimensional
Gaussian-type integrals, each enclosed by one-dimensional voxel sums (`voxel_riemann_enclosure`),
so a second-order certificate costs `M ×` (1-D resolution) per voxel instead of an
`M`-dimensional refinement; (ii) the relative width is `exp(β (M−m) Σ h_i²/2)`, so accuracy
`1+ε` needs `N ≈ vol · (β (M−m) d / (8 ln(1+ε)))^{d/2}` voxels.  The exponent `d/2` cannot be
improved in the Hessian-interval oracle model: information-based lower bounds for integration of
`C^k` classes (Bakhvalov 1959) and, specifically for log-partition functions, `Θ(B n^{−m/d})`
(Holzmüller–Bach 2025) give matching rates **[K]**.

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
after a given set of evaluations.  We leave the instance-optimality question open and record
only the elementary observation that with width functions `w(n)` shared by all states uniform
racing stops once `2 w(n) < gap`, i.e. within the factor `w^{-1}(g/2)/w^{-1}(g)` of the offline
optimum — a factor `2^{d/2}` for second-order voxel refinement in dimension `d`, which is the
real obstacle in high dimension.

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

**Attribution.**  This bound, with the same constants, is Proposition 1 together with the
relaxation inequality of Sonthalia, Van Buskirk, Raichel and Gilbert, *How can classical
multidimensional scaling go wrong?* (NeurIPS 2021), restated in Deng et al. (NeurIPS 2024,
Thm 6); Sonthalia et al. also compute the sign-constrained relaxation exactly in `O(n³)`, which
is at least as strong as the closed form.  We had derived it independently before the literature
check (`prior_art/L3` §C10) and **claim no novelty for the inequality**.  What is contributed is
the machine-checked proof — including the Hoffman–Wielandt inequality and the von Neumann trace
inequality for real symmetric matrices, formalized from Birkhoff's theorem and the rearrangement
inequality (`HoffmanWielandt.lean` **[V]**) — and its use as a realizability *certificate* for
predicted distance matrices (blueprint §8.1).  A proof by compression to `range(G)` does not work
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
  with the trace shift is within a factor `O(√L)` of the optimal s-stress.
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
integer lattice, and a sharp non-abelian Hodge-type lower bound is, to our knowledge, open.

### 4.4 Torsion errors and superposition RMSD: reduced moments of inertia

`RigidWithin X Y c` means that some rigid motion `g` achieves `Σ_i |X_i − gY_i|² ≤ c²`
(so the RMSD after superposition is at most `c/√N`).

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
`N^{-1/2} Σ_k 2 √(min(I_A,I_B)_k) |sin(δ_k/2)|` in Kabsch RMSD, the inertias being those of the
intermediate conformations.  Compared with the naive lever-arm bound (rotate the distal part, no
re-superposition) the certificate is ≈ 2–2.5× tighter on idealised chains (benchmark B7); it is a
worst-case (`ℓ¹`) bound and overestimates independent random errors by `≈ √m` (`DEAD_ENDS.md`
D10).

**Corollary 4.7 (envelope of an invariant residual) [V] (`InvariantEnvelope.lean`).**  If a
residual `Δ` is invariant under rigid motions and `Λ`-Lipschitz in the `ℓ²` configuration
distance, then `|Δ(X) − Δ(Y)| ≤ Λ c` whenever `RigidWithin X Y c`; in particular one torsion
move changes it by at most `Λ · 2√(2 I_red)|sin(δ/2)|` (`residual_torsion_move`,
`residual_torsion_chain`).  This turns an equivariant architecture with a Cartesian Lipschitz
certificate into the bounded-difference envelope required in §2 and §6.

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

**Partition-function kernel [V] (`zverify_sound`, §3.4).**

All three kernels are evaluated on concrete instances by `decide +kernel` (Lean's trusted kernel,
no compiler in the trusted base, no extra axioms): `triangle_verified`, `triangle_rejects`,
`biased_verified`, `triangleResidual_verified`, `triangleZ_exact`.

### 6.2 Verification cost and witness size

Each `leaf`, `prune`, `sum` node is checked by one pass over the instance tables restricted to
the current domains — `O(Σ_i |D_i| + Σ_{i≠j} |D_i||D_j|)` rational comparisons — and a `branch`
node by one list traversal; the verifier never minimises or searches.  A node's witness is the
dual solution (`O(nk)` messages per neighbour pair) or `O(n)` link bounds.  This is the regime
"large witness, linear-time check"; a witness without dual solutions would be smaller but force
the checker to solve an LP (the hint trade-off familiar from LRAT-style proof formats).

### 6.3 The decomposition rule is necessary (known phenomenon, formalized)

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
(d) With `sum`, `2m` leaves suffice for every `m ≥ 1` (`sum_linear`), hence for `m ≥ 3` there is
an accepted certificate strictly smaller than every accepted sum-free certificate
(`sum_rule_separation`).

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

We prove no new expressivity or mixing theorem; the following are consequences of §§2–3.

1. **An architecture is certifiable only through the envelope it exports, and the price of the
   envelope is quantified.**  For an energy `E₀ + Δ_θ` with a learned residual, every guarantee
   above uses `Δ_θ` only via `d` and anchors.  Theorem 2.7 turns the looseness `1−κ` of a
   certified envelope into a lower bound on the number of network evaluations any certificate
   needs: the number of states in an energy shell of width `(1−κ) c_min`.  Theorem 3.1 turns the
   same constants into a free-energy uncertainty `β² Σ c_i²/8` that is sharp.  Design rule:
   *put steep, structured physics (sterics, electrostatics) in the explicit part and constrain
   the residual to have small certified per-site variation*; unbounded Lipschitz constants are
   incompatible with certification, not merely inconvenient.
2. **Expressivity/certifiability trade-off.**  Tight envelopes need the residual's variation to
   be attributable to few sites (small `c_i`) — a restriction of the hypothesis class.  The
   contact-set theorem shows what is gained: the possibly-optimal set shrinks from the energy
   window to the contact set (benchmark B1).
3. **Chirality.**  Any function of pairwise distances is invariant under reflections, so
   distance-based certificates (Theorem 4.3, §4.2) are blind to chirality by construction; frame
   data (§4.3) are not.  This is the realizability-side counterpart of the known incompleteness
   of distance-only invariant networks.
4. **Sampling.**  Thermal dominance and the robust partition bracket give deterministic control
   of ensemble weights without sampling; the T₁ equivalence (§3.2) identifies the property of a
   reference sampler's stationary law that makes second-order free-energy corrections uniformly
   valid.  Convergence-rate theory for torsional diffusion or Langevin samplers on `T^M` is
   outside what was established here.

---

## 8. Limitations

* **Certification, not solution.**  Membership in the contact set, and the query-model criterion,
  are themselves optimisation problems; the theorems say what a certificate must and may contain,
  not how to find it.
* **Finite configuration spaces.**  §§2–3 are stated for finite sets; continuous variables enter
  through voxel enclosures (zeroth order and the separable-envelope step formalized; the Taylor
  step that produces second-order envelopes from Hessian bounds is on paper).
* **Extensivity** of the free-energy sandwich (§3.2).
* **Worst-case geometry bounds** (Theorem 4.6 is `ℓ¹`; Theorem 4.3 is tight only for symmetric
  inputs and within `√((L+2)/2)` in general).
* **No claim of practical performance.**  All experiments are synthetic and small; they check
  tightness and scaling of bounds, not solver speed.
* **Unformalized statements** are marked [P] or [K]: the link-graph dichotomy, the Taylor step
  and the complexity count for second-order voxels, dependent-reference sandwiches and Rio's
  sharp function,
  the Procrustes–Gram corollary, the T₁ equivalence.
* **Certified numerics outside Lean.**  Eigenvalue enclosures needed to *evaluate* the spectral
  bound of §4.1 on data are standard verified numerics but are not part of the development.

---

## 9. Index of machine-checked statements

| file | main declarations |
|---|---|
| `proofs/Core/Basic.lean` | `partitionFn`, `freeEnergy`, `partitionFn_anti`, `freeEnergy_mono` |
| `proofs/Core/Rounding.lean` | `roundDown_le`, `le_roundUp`, `roundUp_sub_roundDown_le`, `QInterval.contains_add/mul/sq/inv/outward`, `exp_enclosure`, `contains_exp`, `contains_boltzmann`, `circle_rational_atlas`, `contains_circParam` |
| `proofs/Frontiers/EnvelopeDuality.lean` | `robust_minimizer_iff`, `robust_certified_iff`, `lowerEnv_admissible`, `upperEnv_admissible`, `robust_min_bracket`, `robust_partition_bracket`, `robust_minimizer_with_anchors_iff`, `anchor_necessary`, `anchor_card_lower_bound`, `admissible_of_single_site`, `differential_dee_sound`, `energy_window_exact` |
| `proofs/Frontiers/Dominance.lean` | `partition_transport`, `partition_prune_bracket`, `freeEnergy_prune_bracket`, `min_transport`, `thermal_dee`, `PairModel.energy_update`, `goldstein_isLeast`, `goldstein_gauge_invariant`, `exactMargin_reparam`, `desmet_reparam_le`, `desmet_optimalGauge` |
| `proofs/Frontiers/FreeEnergySandwich.lean` | `gibbs_bogoliubov`, `hoeffding_upper`, `free_energy_sandwich`, `partition_ratio_sandwich`, `bounded_differences_sandwich`, `additive_extremal`, `exists_two_level_worst_residual`, `balanced_additive_gap`, `log_cosh_bounds`, `mcdiarmid_no_better_constant` |
| `proofs/Frontiers/HolderDecomposition.lean` | `partitionFn_holder`, `freeEnergy_holder` |
| `proofs/Frontiers/PartitionCertificate.lean` | `zverify`, `zverify_sound`, `zprune_sound`, `Z_encloses_partitionFn`, `triangleZ_exact` |
| `proofs/Frontiers/VoxelEnclosure.lean` | `voxel_boltzmann_bounds`, `voxel_riemann_enclosure`, `Z_encloses_voxel_integral`, `certified_voxel_partition` |
| `proofs/Frontiers/SeparableVoxel.lean` | `setIntegral_pi_prod`, `separable_voxel_bounds`, `separable_voxel_ratio` |
| `proofs/Frontiers/HoffmanWielandt.lean` | `trace_mul_le_sum_sorted_eigenvalues`, `hoffman_wielandt` |
| `proofs/Frontiers/Realizability.lean` | `K_identity`, `K_lower_bound`, `rank_psd_trace_obstruction`, `sstress_lower_bound`, `simplex_sstress_lower_bound`, `simplex_not_realizable` |
| `proofs/Frontiers/Holonomy.lean` | `norm_mul_div_mul_le`, `norm_holProd_le_sum`, `norm_holProd_sq_le`, `norm_holTrans_le`, `exists_assignment_attaining_holonomy` |
| `proofs/Frontiers/TorsionRMSD.lean` | `RigidWithin`, `rigidWithin_chain`, `coaxial_cost_eq`, `exists_coaxial_angle`, `coaxial_cost_le_min`, `reduced_le_coaxial_cost`, `IsTorsionMove.rigidWithin`, `rigidWithin_torsion_chain` |
| `proofs/Frontiers/InvariantEnvelope.lean` | `invariant_lipschitz_of_rigidWithin`, `residual_torsion_move`, `residual_torsion_chain` |
| `proofs/Frontiers/ProofComplexity.lean` | `leaf_two_config`, `triangle_no_leaf_certificate`, `triangles_energy_opt`, `sumFree_exponential`, `sumFree_tight`, `sum_linear`, `sum_rule_separation` |
| `proofs/CertificateAlgebra.lean` | `verify`, `verify_sound`, `verifyR`, `verifyR_sound`, `certified_gap`, kernel-evaluated examples |
| `proofs/AxiomAudit.lean` | `#audit_axioms MetricChain`, non-vacuity witnesses |

---

## 10. References

Full bibliographic details, DOIs and verification status of each citation are in
`prior_art/L1_pruning_certificates.md`, `L2_relaxations_partition.md` and
`L3_realizability_geometry.md`.  Principal sources:

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
