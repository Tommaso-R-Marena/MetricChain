# Second-moment rigidity of conformational ensembles

**Geometric Inference, Rigidity and Inverse Problems Division — cycle 1 report.**
Branch `research/geometric-inference`.  Labels as in `docs/collaboration/README.md`:
**[V]** machine-checked in Lean (declaration named), **[P]** paper proof in this file,
**[P, exact]** paper proof whose finite part is an exact computation (script named; rational or
modular arithmetic, no floating point), **[K]** known result (cited), **[N]** numerical evidence
only, **[C]** conjecture.  Nothing in this file has been refereed by another division; the
internal adversarial review is `docs/collaboration/messages/geometry/GEOMETRY-REV-0001.md`, and
the novelty assessment (what is known, what is a reformulation, what we did not find in print)
is §9 and `docs/geometry/PRIOR_ART.md`.

Scope: mathematics of abstract articulated systems.  "Chain" means a sequence of points with
prescribed consecutive distances; no sequence, no target, no experiment.

---

## 0. Summary

An *ensemble* is a probability distribution over conformations of one articulated system.
Many indirect observations are linear in the ensemble; the simplest geometric one is the matrix
of **ensemble-averaged squared distances** `M_ij = ⟨|x_i − x_j|²⟩` (in polymer physics: the
mean-square internal distances).  The question of this report: *what does `M` determine, when
every conformation obeys the same local constraints (bond lengths, bond angles)?*

1. **An ensemble is one framework in a higher dimension** (§2, stacking).  `M` is the Euclidean
   distance matrix of a single configuration `z` in `ℝ^{3K}` (or a Hilbert space), the states
   being its coordinate blocks.  Everything below is rigidity theory of `z`.
2. **Without statewise constraints averaged squared distances identify nothing** (§3): every
   configuration has the same `M` as a three-state ensemble of collinear ones, and a
   `K`-state mixture sits in an `O(3K)`-orbit of equivalent mixtures.  This is an obstruction
   for distributions that is absent for single configurations.
3. **Statewise constraints restore identifiability, and the mechanism is a conic condition**
   (§4, Theorems A, B).  A single conformation is the only ensemble with its `M` iff its
   constrained edge directions lie on no conic at infinity (for `K = 1` this is a
   reinterpretation of a classical lemma of rigidity theory).  A `K`-state mixture is the only
   ensemble — among **all** probability distributions on conformations, with any number of
   states — with its `M`, as soon as the only quadrics through the constrained edge
   directions of the stacked framework are the `K − 1` trivial ones.
4. **Sharp thresholds** (§5, Theorem C).  For freely jointed chains the conic condition holds
   generically iff the chain has at least `(9K² + K + 2)/2` bonds [P, all `K`].  For chains
   with fixed bond lengths and bond angles it holds generically iff
   `n ≥ ⌈(9K² + K + 8)/4⌉` atoms: 5, 12, 23, 39, 60, … [P, exact for `K ≤ 12` at two bond
   geometries; a weaker threshold of the same order for every `K` and every geometry; the
   sharp threshold for all `K` is a conjecture].
5. **A polynomial-time demixing algorithm with a certificate** (§6): eigen-decomposition of the
   centred `M`, one linear system, one symmetric eigenproblem.  The certificate of uniqueness
   is a rank.
6. **A global quantitative theorem** (§7, Theorem G): under the conic condition
   `W₂(ν, μ)² ≤ C·‖M(ν) − M(μ)‖` for *every* ensemble `ν`, with an explicit dual certificate
   (a positive semidefinite "ensemble stress"); the exponent is optimal.  With incomplete
   averaged data, a positive semidefinite stress of the stacked framework supported on the
   measured pairs certifies identifiability (Theorem F) — for `K = 1` this is the classical
   sufficient condition for universal rigidity.
7. **A new rigidity notion between global and universal rigidity** (§8, Theorem E):
   *ensemble rigidity*.  Universal rigidity ⇒ ensemble rigidity ⇒ global rigidity; the
   second implication is strict (a rigid conformation whose averaged data are reproduced
   exactly by a two-state ensemble of other conformations); for chains with at most 6 atoms
   the first is an equivalence, because there every Hilbert-space chain is an ensemble
   average of chains in `ℝ³` (Theorem D); from 7 atoms on the set of realizable averaged data
   is strictly smaller than its semidefinite relaxation [P, exact witness].
8. **How little data suffices** (§5.3–5.4): within the family of `K`-state ensembles, complete
   averaged data are generically locally identifying exactly from the parameter count
   `n ≥ 2K + 3` on, and averaged distances of sequence separation at most `K + 3` are
   locally identifying, while separation `K + 2` never is [P, exact for `K ≤ 8`]; among all
   ensembles a separation of `3K + 1` suffices [P]; numerically, identifiability among all
   ensembles starts at `n = ⌊9K/2⌋ + 1`, far below the threshold of the linear certificate
   [N for `K = 2, 3`; C in general].

Machine-checked core: `proofs/Geometry/EnsembleRigidity.lean` (§10).  Scripts:
`experiments/geometry/` (§11).

---

## 1. Setting

Throughout `d ≥ 2` is the ambient dimension (`d = 3` in all statements about chains), `[n]`
the set of points ("atoms"), and `E₀` a connected graph on `[n]` with lengths `ℓ_e > 0`: the
**statewise constraints**.  The **conformation space** is

    𝒞 = 𝒞_d(E₀, ℓ) = { x ∈ (ℝ^d)^n : |x_i − x_j| = ℓ_ij for all ij ∈ E₀ },

assumed non-empty.  Two configurations are *congruent* if an isometry of `ℝ^d` (reflections
included) maps one to the other; `[x]` is the congruence class ("shape").  Since `E₀` is
connected, `𝒞` modulo translations is compact.

* **Chains.**  `E₀^{BA} = {i, i+1} ∪ {i, i+2}` (bond lengths `b_i` and 1–3 distances `c_i`,
  i.e. bond angles; the free parameters are the `n − 3` torsions) and `E₀^{B} = {i, i+1}`
  (freely jointed).  A bond geometry is non-degenerate if every bond angle lies in `(0, π)`.
* **Ensembles.**  An ensemble is a Borel probability measure `μ` on `𝒞`; `[μ]` is its image on
  shapes.  Its **mean squared-distance matrix** is `M(μ)_ij = ∫ |x_i − x_j|² dμ(x)`.  For a
  configuration `X`, `D(X)_ij = |x_i − x_j|²`, so `M(δ_X) = D(X)` and `M(μ) = ∫ D dμ`.
  The set of all realizable averaged data is `𝒦 = { M(μ) } = conv D(𝒞)`, a compact convex set.
* **Edge vectors.**  For a configuration `z` of `[n]` in a Euclidean space, its
  `E₀`-edge vectors are `z_j − z_i`, `ij ∈ E₀`.  For `z` in `ℝ^m`,

      𝒩(z) = { S ∈ Sym(m) : eᵀ S e = 0 for every E₀-edge vector e of z }

  is the space of **quadrics through the constrained edge directions** ("conics at infinity"
  in the language of rigidity theory).
* **Identifiability.**  `μ` is **identifiable from averaged squared distances** (on a set `F`
  of pairs; all pairs if `F` is not named) if every ensemble `ν` on `𝒞` with
  `M(ν)_ij = M(μ)_ij` for `ij ∈ F` satisfies `[ν] = [μ]`.  Note the quantifier: `ν` ranges over
  all probability measures, not over mixtures with a prescribed number of states.

---

## 2. Stacking: an ensemble is a framework in a higher dimension

**Lemma 2.1 (stacking) [V: `MetricChain.Geometry.stacked_sqdist`].**  For a finite mixture
`μ = Σ_k w_k δ_{X_k}` put `z_i = (√w_k · x_i^{(k)})_{k=1..K} ∈ ℝ^{dK}`.  Then
`M(μ)_ij = |z_i − z_j|²`.  For an arbitrary ensemble the same holds with
`z_i = (x ↦ x_i) ∈ L²(μ; ℝ^d)` (after fixing `x_1 = 0`).  ∎

So `M(μ)` is always a Euclidean distance matrix; its embedding dimension is `dK` for a generic
`K`-mixture with `n − 1 ≥ dK`.  The states are the coordinate blocks of `z`; write `E_k` for the
orthogonal projection of `ℝ^{dK}` onto block `k`.  The edge vectors of `z` satisfy

    eᵀ E_k e = w_k ℓ_e²,     |e|² = ℓ_e²        (e an E₀-edge vector of z).            (2.1)

Hence `𝒩(z)` always contains the `(K − 1)`-dimensional space of **trivial quadrics**

    𝒯 = { Σ_k s_k E_k : Σ_k w_k s_k = 0 }.

**Lemma 2.2 (every competing ensemble consists of linear images of `z`) [P].**  Let
`z ∈ (ℝ^m)^n` span `ℝ^m` affinely, with `|z_i − z_j| = ℓ_ij` on `E₀`, and let `ν` be an ensemble
on `𝒞` with `M(ν) = D(z)`.  Then there is a measurable `A : 𝒞 → ℝ^{d×m}` such that for
`ν`-almost every `x`

    x_j − x_i = A(x)(z_j − z_i)  for all i, j,     A(x)ᵀA(x) ∈ 𝒫(z),      ∫ AᵀA dν = I_m,

where `𝒫(z) = { P ∈ I + 𝒩(z) : P ⪰ 0, rank P ≤ d }`.

*Proof.*  Normalise `x_1 = 0` and let `ζ_i = (x ↦ x_i − x_1) ∈ H = L²(ν; ℝ^d)` (bounded
functions).  `|ζ_i − ζ_j|²_H = M(ν)_ij = |z_i − z_j|²`, so the Gram matrices of
`(ζ_i)` and of `(z_i − z_1)` agree (polarisation).  Therefore `T(z_i − z_1) = ζ_i` defines a
linear isometry `T : ℝ^m → H` (well defined on the spanning set because a vanishing linear
combination on the left has norm zero on the right).  Let `A(x)` be the matrix whose `c`-th
column is a representative of `T e_c`; then `Tv = A(·)v` in `H`, so
`x_i − x_1 = A(x)(z_i − z_1)` for almost every `x`, simultaneously for the finitely many `i`,
and `vᵀv' = ⟨Tv, Tv'⟩ = ∫ vᵀAᵀAv' dν`.  For `ij ∈ E₀` and almost every `x`,
`ℓ_ij² = |x_j − x_i|² = eᵀA(x)ᵀA(x)e` with `e = z_j − z_i`, and `|e|² = ℓ_ij²`; so
`A(x)ᵀA(x) − I ∈ 𝒩(z)`.  `AᵀA` is positive semidefinite of rank at most `d`.  ∎

**Remark 2.3 (ellipsoid fitting).**  `P ∈ 𝒫(z)` says that the degenerate quadric
`{v : vᵀPv = 1}` — an elliptic cylinder with a `d`-dimensional cross-section — passes through
the normalised edge vectors `e/ℓ_e`.  The states of a mixture are `K` such cylinders,
`E_k / w_k`, and the identity is their barycentre.  Identifiability is the statement that
there is no other way to write the unit sphere as an average of rank-`d` cylinders through
these points (Theorem B′).

---

## 3. The obstruction: averaged squared distances without statewise constraints

**Proposition 3.1 [P; elementary].**
(a) For every configuration `X` in `ℝ^d`, `D(X) = (1/d) Σ_{c=1}^d D(√d · X^{(c)})`, where
`X^{(c)}` is the collinear configuration given by the `c`-th coordinates.  So, with no
statewise constraint, no configuration of affine dimension `≥ 2` is determined by its squared
distances among ensembles — although it is determined among configurations.
(b) Let `μ = Σ w_k δ_{X_k}` with stacked configuration `z` spanning `ℝ^{dK}`, `K ≥ 2`.  For every
`Q ∈ O(dK)` the blocks of `zQ` define a `K`-state mixture `μ_Q` with `M(μ_Q) = M(μ)`; the
family `{[μ_Q]}` has dimension `dim O(dK) − K·dim O(d) = d²K(K − 1)/2` (9 for two states
in space).
(c) With statewise constraints `E₀`, `μ_Q` is an ensemble on `𝒞` iff every block projection
`Q E_k Qᵀ / w'_k` lies in `𝒫(z)`.  ∎

(a) and (b) are the factor-rotation indeterminacy of a second-moment statistic.  They are
the reason why §4 needs statewise constraints, and (c) is how the constraints enter.

**Example 3.2 (freely jointed chains that are mixtures of rods).**  A freely jointed chain all
of whose bond vectors are of the form `(±1, ±1, ±1)·b/√3` has the same `M` as the equal-weight
mixture of three straight-or-folded rods (its three coordinate sequences scaled by `√3`), each
of which is a freely jointed chain in `ℝ³`.

**Example 3.3 (four atoms).**  For a chain of four atoms with torsion `θ`,
`d_14² = A − B cos θ`.  Every non-planar conformation has the same `M` as the mixture of the
cis and the trans conformation with weights `(1 + cos θ)/2`, `(1 − cos θ)/2`, although the
conformation is globally rigid (determined up to congruence by `d_14`).  This is the familiar
"virtual structure" of ensemble-averaged restraints; Theorem A says exactly when it cannot
happen.

---

## 4. Identifiability

### 4.1 One state: the conic criterion

**Theorem A [P; (ii)⇒(i) is the new reading, (ii)⇔(iii) is classical — §9].**  Let `X ∈ 𝒞`
span `ℝ^d` affinely.  The following are equivalent.

  (i) `δ_X` is identifiable from averaged squared distances: every ensemble `ν` on `𝒞` with
      `M(ν) = D(X)` is supported on the congruence class of `X`.
 (ii) `𝒩(X) = {0}`: the constrained edge directions of `X` lie on no conic at infinity.
(iii) `D(X)` is not the midpoint of `D(X₊)` and `D(X₋)` for two conformations
      `X₊, X₋ ∈ 𝒞` that are not congruent to `X`.

*Proof.*  (ii)⇒(i): Lemma 2.2 with `z = X`, `m = d`: for almost every `x`,
`A(x)ᵀA(x) − I ∈ 𝒩(X) = 0`, so `A(x) ∈ O(d)` and `x` is congruent to `X`.
(i)⇒(iii) is trivial.  (iii)⇒(ii): let `0 ≠ S ∈ 𝒩(X)` and `t > 0` with `I ± tS ≻ 0`; put
`A_± = (I ± tS)^{1/2}` and `X_± = (A_± x_i)_i`.  For an `E₀`-edge vector `e`,
`|A_± e|² = eᵀ(I ± tS)e = |e|²`, so `X_± ∈ 𝒞`; and
`D(X_±)_ij = |x_i − x_j|² ± t (x_i − x_j)ᵀS(x_i − x_j)`, whose average is `D(X)`.  A quadratic
form that vanishes on all differences of an affinely spanning set vanishes (it vanishes on a
basis `v_i = p_i − p_0` and on all `v_i − v_j`), so `D(X_±) ≠ D(X)`.  ∎

The affine images `X_±` are the *affine flexes* of rigidity theory.  Machine-checked **[V]**
(`MetricChain.Geometry.sqdist_midpoint_of_conic`): for a symmetric matrix `S` vanishing on the
edge vectors with `I ± S ⪰ 0` there are linear maps `A_±` that preserve the squared lengths of
the edge vectors and satisfy `|A_+v|² − |v|² = vᵀSv`, `|A_+v|² + |A_−v|² = 2|v|²` for all `v`
(the square roots are obtained from the factorisation of a positive semidefinite matrix; the
last sentence of the proof — the images are not congruent to `X` — is on paper).

**Corollary 4.1 (chains) [P, exact].**  `Sym(3)` has dimension 6, a chain with fixed bond
lengths and angles has `2n − 3` constrained edges.  Every chain with 4 atoms violates (ii)
(Example 3.3); a generic chain with `n ≥ 5` atoms satisfies it (witness:
`experiments/geometry/exact_conic_rank.py`, `K = 1`).  A generic freely jointed chain
satisfies it iff it has at least 6 bonds.

### 4.2 Finite mixtures

**Theorem B (identifiability of a mixture among all ensembles) [P; core V:
`MetricChain.Geometry.block_rigidity`].**  Let `μ = Σ_{k=1}^K w_k δ_{X_k}`, `w_k > 0`, with
stacked configuration `z ∈ (ℝ^{dK})^n`, and assume the **conic condition**

    𝒩(z) = 𝒯          (the only quadrics through the constrained edge directions of z
                       are the trivial ones; equivalently dim 𝒩(z) = K − 1).              (CC)

Then `μ` is identifiable from averaged squared distances: if `ν` is any ensemble on `𝒞` with
`M(ν) = M(μ)`, then `ν`-almost every conformation is congruent to one of `X_1, …, X_K`, and the
class of `X_k` has `ν`-probability `w_k`.

*Proof.*  (CC) implies that `z` spans `ℝ^{dK}` affinely: otherwise some `v ≠ 0` is orthogonal to
all differences and `vvᵀ ∈ 𝒩(z)`, but a block-scalar matrix has rank `0` or `≥ d ≥ 2`.  Apply
Lemma 2.2: for almost every `x`, `P = A(x)ᵀA(x) ∈ I + 𝒯`, i.e. `P = Σ_k c_k E_k` with
`Σ_k w_k c_k = 1`.  `P ⪰ 0` gives `c_k ≥ 0`, and `rank P = d·#{k : c_k ≠ 0} ≤ d` leaves exactly
one non-zero coefficient, `c_κ = 1/w_κ`, `κ = κ(x)`.  Then `A(x)` vanishes on the other blocks
and `√w_κ A(x)` restricted to block `κ` is orthogonal, so
`x_i − x_1 = R(x)(x_i^{(κ)} − x_1^{(κ)})` with `R(x) ∈ O(d)`.  Finally
`I = ∫ AᵀA dν = Σ_k ν(κ = k) E_k / w_k` gives `ν(κ = k) = w_k`.  ∎

The step "a positive semidefinite block-scalar form of rank at most `d` is supported on one
block" is the machine-checked `block_rigidity`: stated without matrices, for a linear map
`A` into a `d`-dimensional space whose quadratic form `|Av|²` is `Σ_k c_k |E_k v|²`.

**Theorem B′ (exact criterion) [P].**  Let `μ` be a `K`-mixture whose stacked configuration `z`
spans `ℝ^{dK}` affinely.  Then `μ` is identifiable from averaged squared distances iff the
identity `I_{dK}` has exactly one representation as the barycentre of a probability measure on
`𝒫(z)`, namely `Σ_k w_k δ_{E_k/w_k}`.

*Proof.*  (⇐) By Lemma 2.2 a competing `ν` induces the probability measure `ρ = (AᵀA)_* ν` on
`𝒫(z)` with barycentre `I`; if `ρ = Σ w_k δ_{E_k/w_k}` the last three sentences of the previous
proof apply.  (⇒) Let `ρ' ≠ Σ w_k δ_{E_k/w_k}` have barycentre `I`.  If `supp ρ'` were contained
in `{E_k/w_k}`, the linear independence of the `E_k` would give `ρ' = Σ w_kδ_{E_k/w_k}`; so
`supp ρ'` contains a point outside, and by Tchakaloff's theorem (applied separately to `ρ'`
restricted to a small closed ball `B` around that point, disjoint from `{E_k/w_k}`, and to its
complement) there is a finitely supported `ρ'' = Σ_j c_j δ_{P_j}` on `𝒫(z)` with barycentre `I`
and `ρ''(B) > 0`.  Choose `A_j ∈ ℝ^{d×dK}` with `A_jᵀA_j = P_j` and let
`Y_j = (A_j(z_i − z_1))_i`.  `Y_j ∈ 𝒞` because `eᵀP_je = |e|² = ℓ_e²`, and
`Σ_j c_j D(Y_j)_{ii'} = (z_i − z_{i'})ᵀ(Σ c_jP_j)(z_i − z_{i'}) = M(μ)_{ii'}`.  `Y_j` is
congruent to `X_k` iff `P_j − E_k/w_k` vanishes on all differences of `z`, i.e. iff
`P_j = E_k/w_k`.  So `ν' = Σ c_j δ_{Y_j}` has `M(ν') = M(μ)` and `[ν'] ≠ [μ]`.  ∎

**Corollary 4.2 (simplicial faces; neighbourliness of the hull of the chain variety) [P].**
If `μ = Σ w_k δ_{X_k}` is identifiable (in particular under (CC)), then
`D(X_1), …, D(X_K)` are affinely independent and their convex hull is a face of
`𝒦 = conv D(𝒞)`.

*Proof.*  If `Σ a_k D(X_k) = 0`, `Σ a_k = 0`, then `μ_t = Σ (w_k + t a_k)δ_{X_k}` is an ensemble
with `M(μ_t) = M(μ)` for small `t`, so `[μ_t] = [μ]`, and `a = 0` because the `X_k` are pairwise
non-congruent.  Let `Φ` be the smallest face of `𝒦` containing `M(μ)`; `M(μ)` is in its
relative interior, so for `y ∈ Φ` there are `y' ∈ Φ` and `t ∈ (0, 1]` with
`M(μ) = t y + (1 − t) y'`; `y = M(ν_y)`, `y' = M(ν_{y'})`, and identifiability of `μ` forces
`ν_y` to be carried by the classes `[X_k]`, i.e. `y ∈ conv{D(X_k)}`.  ∎

---

## 5. Thresholds

### 5.1 The conic condition for generic chains

Write `D_K = dim Sym(3K) − (K − 1) = (9K² + K + 2)/2`.  (CC) says that the `|E₀|` linear
conditions `eᵀSe = 0` on `Sym(3K)` have rank `D_K`; it is impossible when `|E₀| < D_K`.  The
dimension of `𝒩(z)` does not depend on the weights (`z = z̃·diag(√w_k I₃)` with `z̃` the
unweighted stack, and `𝒩(z) = diag(w_k^{-1/2})𝒩(z̃)diag(w_k^{-1/2})`), so (CC) is a property
of the `K`-tuple of conformations.

**Theorem C.**
(a) *Freely jointed chains, every `K`* **[P]**.  For `K` generic freely jointed chains (CC)
holds iff the number of bonds satisfies `n − 1 ≥ D_K = (9K² + K + 2)/2` (6, 20, 43, 75, 116, …).
(b) *Bond lengths and angles, sharp* **[P, exact]**.  For unit bonds and bond angle with cosine
`−5/13` (112.6°) or `−1/3` (109.47°), and `1 ≤ K ≤ 12`: (CC) holds for generic `K`-tuples of
chains iff `2n − 3 ≥ D_K`, i.e.

    n ≥ n₀(K) = ⌈(9K² + K + 8)/4⌉ = 5, 12, 23, 39, 60, 85, 114, 148, 187, 230, 277, 329.

The same holds for bond geometries outside a proper analytic subset of the space of bond
geometries.
(c) *Bond lengths and angles, every `K` and every homogeneous non-degenerate geometry*
**[P]**.  Let `α = π −` (bond angle), `β = min(α, π − α)`, `m₀ = max(2, ⌈π/β⌉)` (`m₀ = 3` for
bond angles between 60° and 120°).  Then (CC) holds for generic `K`-tuples as soon as
`n ≥ m₀(D_K − 1) + 2`.
(d) **[C]** The threshold `n₀(K)` of (b) is valid for every `K` and every non-degenerate bond
geometry.

*Proof of (a).*  For unit vectors `p = (û^{(1)}, …, û^{(K)}) ∈ (S²)^K` and `S ∈ Sym(3K)` let
`F_S(p) = Σ_{k,l} û^{(k)ᵀ} S_{kl} û^{(l)}`.  `F_S ≡ 0` on `(S²)^K` iff `S_{kl} = 0` for `k ≠ l`
(the cross terms are bilinear in independent unit vectors) and `S_kk = s_k I` with `Σ s_k = 0`
(a quadratic form that is constant on the sphere is a multiple of the identity).  So the
functions `F_S` form a space of dimension `D_K`.  For a space of functions of finite dimension
`D` on a set, points `p_1, …, p_N` can be chosen one at a time so that the evaluations at them
are linearly independent, as long as `N ≤ D` (if the evaluations so far do not span, some
non-zero function of the space vanishes at all chosen points; add a point where it does
not).  The bond directions of `K` freely jointed chains with `N` bonds are an arbitrary point
of the connected real-analytic manifold `((S²)^K)^N`, and "rank `D_K`" is the non-vanishing of
some minor, an analytic function that is not identically zero: it holds on an open dense set.
Unequal bond lengths rescale rows.  ∎

*Proof of (b).*  `rank ≤ D_K` always.  `experiments/geometry/exact_conic_rank.py` exhibits, for
each `K ≤ 12` and each of the two geometries, chains with rational torsion half-angle tangents
at which the rank of the conic system, computed modulo a prime after an exact evaluation in
`ℚ` respectively `ℚ(√2)`, equals `D_K` at `n = n₀(K)`.  A ring homomorphism to a field cannot
increase a rank, so the rank over the number field is `D_K`.  The rank is attained on the
complement of a proper analytic subset of the torus of torsions (and of the space of bond
geometries, on which the entries depend analytically as well); adding atoms adds conditions,
so the rank stays `D_K` for `n > n₀(K)`.  For `2n − 3 < D_K` the count forbids (CC).  ∎

*Proof of (c).*  **Lemma R.**  For `u, v ∈ S²` and `m ≥ m₀` there is a sequence
`u = û_0, …, û_m = v` with consecutive angles `α`.  *Proof.*  The set reachable from `u` in
`m` steps is `{v : ∠(u, v) ∈ J_m}` with `J_1 = {α}` and
`J_{m+1} = ∪_{ρ ∈ J_m} [|ρ − α|, min(ρ + α, 2π − ρ − α)]` (spherical triangle inequality,
all intermediate values attained by continuity).  By induction, for `α ≤ π/2`,
`J_m = [0, min(mα, π)]` for `m ≥ 2`; for `α > π/2`, with `β = π − α`,
`J_m = [0, min(mβ, π)]` for even `m` and `[max(0, π − mβ), π]` for odd `m`.  In both cases
`J_m = [0, π]` iff `m ≥ max(2, ⌈π/β⌉)`.  ∎
Hence the bond directions with indices `0, m₀, 2m₀, …` of each of the `K` chains can be
prescribed arbitrarily and independently.  By the argument of (a), `D_K` of these stacked
directions can be chosen with independent evaluations; this needs `m₀(D_K − 1) + 1` bonds.
The rank is then `D_K` at one point of the torus of torsions, hence generically.  ∎

Evidence for (d): the exact computation of (b); numerically the same threshold at bond angle
111° for `K ≤ 4` (`experiments/geometry/run_checks.py`, test `conic_threshold_float`).

### 5.2 What the thresholds mean

| | 1 state | 2 states | 3 states | `K` states |
|---|---|---|---|---|
| parameter count allows local identifiability within `K`-state ensembles (complete data) | `n ≥ 4` | `n ≥ 7` | `n ≥ 9` | `n ≥ 2K + 3` (`K ≥ 2`) |
| identifiable among all ensembles, observed **[N]** / conjectured **[C]** | `n ≥ 5` | `n ≥ 10` | `n ≥ 14` | `n ≥ ⌊9K/2⌋ + 1` |
| conic condition (CC): linear certificate, polynomial-time demixing **[P, exact]** | `n ≥ 5` | `n ≥ 12` | `n ≥ 23` | `n ≥ ⌈(9K²+K+8)/4⌉` |

The middle row is where `𝒫(z)`, cut out of an affine space of dimension `dim 𝒩(z)` by the
rank condition (codimension 6 for `K = 2`), is expected to contain nothing but the forced
points: counting the unknowns of `A` modulo `O(3)` against the equations,
`9K − 3 < 2n − 3`.  Observed (`experiments/geometry/explore_spurious.py`, multi-start
Levenberg–Marquardt over `A`): for `K = 2`, `n = 9` there are 4–6 further real chains that are
linear images of `z`, none of which can carry mass in a representation of `I` (linear program,
`explore_misc.py lp`); for `n ≥ 10` only the two states are found; for `K = 3` a
one-parameter family at `n = 13` and only the three states for `n ≥ 14`.  We have no proof;
an exact elimination for `K = 2`, `n = 10` would give one (`PROOF_OBLIGATIONS.md`, O-2).
Between the second and the third row identifiability (conjecturally) holds but our only
certificate is non-linear — a gap between what the data determine and what the linear
algorithm of §6 extracts.

### 5.3 Local identifiability within `K`-state ensembles

Let `Φ_F : (torsions of K chains, K − 1 weights) → (M_ij)_{ij ∈ F}`.  It has
`K(n − 3) + K − 1` parameters.

**Theorem H [P, exact for `K ≤ 8`].**  Unit bonds, bond angle with cosine `−5/13` or `−1/3`.
(a) *Complete averaged data.*  For `2 ≤ K ≤ 8` the Jacobian of `Φ` has full column rank at
generic points iff `n ≥ 2K + 3`.
(b) *Sequence-local averaged data.*  Let `F_w = {ij : 3 ≤ |i − j| ≤ w}`.  For `1 ≤ K ≤ 8` the
Jacobian of `Φ_{F_w}` has full column rank at generic points if `w ≥ K + 3` and
`n ≥ (K² + 3K + 4)/2`; for `K ≥ 2` it never has full column rank if `w ≤ K + 2`, whatever `n`.
(c) Full column rank at a point implies that `Φ_F` is injective near it: the ensemble is
determined by the `F`-averaged data among `K`-state ensembles in a neighbourhood.

*Proof.*  Necessity is a count: (a) `K(n − 2) − 1 ≤ (n − 2)(n − 3)/2` fails at `n = 2K + 2`
for `K ≥ 2`; (b) the data number `Σ_{s=3}^{w}(n − s)`, and for `w = K + 2`, `K ≥ 2` this is
smaller than `K(n − 2) − 1` for every `n`.  Sufficiency at the smallest `n`:
`experiments/geometry/exact_jacobian_rank.py` (rational witnesses, rank modulo a prime of the
exactly evaluated Jacobian; at the threshold of (b) the system is square).  Larger `n`:
**extension lemma.**  Adding atom `n + 1` adds `K` torsions and the data `M_{i,n+1}`; the old
data do not depend on the new torsions, so the Jacobian is block triangular,
`[[J_n, 0], [∗, B]]`, with `B_{ik} = ∂M_{i,n+1}/∂θ^{(k)}_{new}` proportional to the signed volume
of the tetrahedron `(i, n−1, n, n+1)` in state `k`, i.e. to the height of atom `i` of state `k`
above the plane of its last three atoms.  For one chain the vector of heights of the `w − 2`
atoms preceding the last three is a function of the last `w − 2` torsions with a triangular
Jacobian with non-zero diagonal at generic points, so its values fill an open set, and `K ≤ w − 2`
chains can be chosen with linearly independent height vectors: `B` has rank `K` at some point.
"`J_n` has full column rank" and "`B` has rank `K`" are each the non-vanishing of an analytic
function that is not identically zero on a connected analytic manifold, so they hold together
somewhere, and then `J_{n+1}` has full column rank.  More data at the same `n` only add rows.
(c) is the inverse function theorem applied to a square subsystem.  ∎

So the minimal sequence separation of averaged data that can identify `K` states (locally)
is exactly `K + 3`: **each additional state costs one more unit of range**, and nothing else.

### 5.4 Sequence-local data, among all ensembles

**Theorem F′ [P].**  Let `μ` be a `K`-mixture satisfying (CC) whose stacked configuration `z`
has every `dK + 1` consecutive points affinely independent.  Then `μ` is identifiable from the
averaged squared distances of sequence separation at most `dK + 1` (together with the
statewise constraints).

*Proof.*  Let `ν` agree with `μ` on these pairs and let `ζ` be its Hilbert configuration
(Lemma 2.1).  The first `dK + 1` points of `ζ` and of `z` have equal mutual distances, so after
an isometric identification they coincide and span an affine subspace `𝔸` of dimension `dK`.
A point of a Hilbert space is determined by its distances to an affinely spanning set of `𝔸`
when these distances are realised by a point of `𝔸` (they determine the orthogonal projection
to `𝔸` and the distance from `𝔸`, which is zero).  Point `dK + 2` has prescribed distances to
its `dK + 1` predecessors; inductively `ζ = z` up to isometry, `M(ν) = M(μ)`, and Theorem B
applies.  ∎

Between `K + 3` (local, within `K`-state ensembles) and `3K + 1` (global, among all
ensembles) we know nothing; see `PROOF_OBLIGATIONS.md`, O-4.

---

## 6. A demixing algorithm with a certificate

**Algorithm DEMIX.**  Input: a symmetric matrix `M` and the statewise data `(E₀, ℓ)`.
1. `G = −½ J M J` (`J` the centring projection); eigen-decomposition; `r = rank G`; if `d ∤ r`
   stop; `K = r/d`; `Z = V_r Λ_r^{1/2}` (`n × dK`).
2. Solve the homogeneous linear system `eᵀSe = 0` (`e` the `E₀`-edge vectors of `Z`) on
   `Sym(dK)`.  **Certificate:** its solution space has dimension exactly `K − 1`.
3. Take a generic `T` in the solution space; its eigenvalues have multiplicity `d`; let `Q_k`
   be orthonormal bases of its eigenspaces.
4. Output `w_k = |Z_e Q_k|²/ℓ_e²` (any edge `e`) and `X_k = Z Q_k/√w_k`.

**Proposition 6.1 [P].**  If `M = M(μ)` for a `K`-mixture `μ` satisfying (CC), DEMIX returns
`μ` up to congruence of the states, and by Theorem B no other ensemble has the same `M`.
The cost is one eigen-decomposition of order `n`, a linear system with `|E₀|` equations in
`dK(dK + 1)/2` unknowns and an eigen-decomposition of order `dK`.

*Proof.*  `G` is the Gram matrix of the centred stacked configuration, so `Z = z_c Q₀` for some
`Q₀ ∈ O(dK)`, and `𝒩(Z) = Q₀ᵀ 𝒩(z) Q₀ = Q₀ᵀ 𝒯 Q₀`.  A generic element is
`T = Q₀ᵀ(Σ s_k E_k)Q₀` with distinct `s_k`, whose eigenspaces are the images of the blocks; so
`Z Q_k = √w_k X_k R_k` with `R_k ∈ O(d)`, and (2.1) gives the weights.  ∎

Floating-point behaviour (`experiments/geometry/demix.py`, test `demix_recovers`): exact
recovery at the thresholds `n₀(K)` for `K = 2, 3, 4` (state RMSD `≤ 2·10⁻⁷`, weights to
`10⁻¹³`), errors proportional to the perturbation of `M` with a constant governed by the
smallest non-trivial singular value `s*` of the linear system, which is small exactly at the
threshold (`s* ≈ 7·10⁻³` at `K = 2, n = 12` against `9·10⁻²` at `n = 16`).  This is a statement
about one implementation on synthetic instances, not a stability theorem; the stability
theorem is §7.

---

## 7. Stress certificates and a global quantitative theorem

### 7.1 Incomplete averaged data: the ensemble stress

**Theorem F (stress certificate) [P; core V: `MetricChain.Geometry.stress_certificate`].**
Let `μ = Σ w_k δ_{X_k}` satisfy (CC), with stacked configuration `z`, and let `F` be a set of
pairs such that the vectors `(D(X_k)_ij)_{ij ∈ F}`, `k = 1..K`, are affinely independent.
Suppose there is a symmetric matrix `Ω` with

    Ω ⪰ 0,   Ω𝟙 = 0,   Ω_ij = 0 unless i = j or ij ∈ F ∪ E₀,   ker Ω = span(𝟙, columns of z).

Then `μ` is identifiable from the averaged squared distances on `F`.

*Proof.*  For a configuration `X` (an `n × d` matrix) and `Ω𝟙 = 0`,
`tr(XᵀΩX) = −½ Σ_{i≠j} Ω_ij |x_i − x_j|²`.  Let `ν` agree with `μ` on `F`; on `E₀` both have
`M_ij = ℓ_ij²`.  So `∫ tr(XᵀΩX) dν = −½ Σ Ω_ij M(ν)_ij = −½ Σ Ω_ij M(μ)_ij = tr(zᵀΩz) = 0`.
`Ω ⪰ 0` forces `ΩX = 0` for almost every state: its coordinate columns lie in
`span(𝟙, columns of z)`, i.e. `x_i = t + A z_i`.  The statewise constraints give
`AᵀA ∈ 𝒫(z)`, and the proof of Theorem B shows that the state is congruent to some `X_κ`.
Then `Σ_k (ν(κ = k) − w_k) D(X_k)_ij = 0` on `F`, and affine independence gives the
weights.  ∎

For `K = 1` this is the classical sufficient condition for universal rigidity (a positive
semidefinite equilibrium stress matrix of rank `n − d − 1`, edge directions on no conic at
infinity — Connelly; see §9), read for ensembles.  For `K ≥ 2` it says: *a mixture is
identifiable if its stacked framework is super-stable in `ℝ^{dK}` up to the block-orthogonal
group.*  `(Ω, rank of the conic system)` is an independently checkable certificate: one
`LDLᵀ` factorisation and two ranks in exact arithmetic.

### 7.2 Complete data: a global stability theorem

Let `d_P(X, Y) = min_g ‖X − gY‖_F` (minimum over isometries; `√n ·` RMSD after optimal
superposition) and let `W₂` be the 2-Wasserstein distance between shape distributions with
respect to `d_P`.

**Theorem G (global quantitative ensemble rigidity) [P].**  Let `μ = Σ w_k δ_{X_k}` satisfy
(CC) on a conformation space that is a smooth manifold near each `X_k` (chains with
non-degenerate bond angles), with `n − 1 > dK`.  Let `Π^⊥` be the orthogonal projection of
`ℝ^n` onto the orthogonal complement of `span(𝟙, columns of z)` and
`φ(X) = ‖Π^⊥ X‖_F² = −½ ⟨Π^⊥, D(X)⟩`.  Then
(a) `φ ≥ 0` on all configurations, and on `𝒞` it vanishes exactly on the classes `[X_k]`;
(b) `κ := inf_{X ∈ 𝒞} φ(X)/min_k d_P(X, X_k)² > 0`;
(c) for every ensemble `ν` on `𝒞`:
    `∫ min_k d_P(X, X_k)² dν ≤ (√(n − 1 − dK) / (2κ)) · ‖M(ν) − M(μ)‖_F`;
(d) there is a constant `C_μ` with `W₂([ν], [μ])² ≤ C_μ ‖M(ν) − M(μ)‖_F` for every ensemble
    `ν` on `𝒞`;
(e) the exponent cannot be improved: there are ensembles `ν_ε → μ` with
    `W₂([ν_ε], [μ])² ≥ c ‖M(ν_ε) − M(μ)‖_F`, `c > 0`.

*Proof.*  (a) `φ(X) = 0` iff the columns of `X` lie in `span(𝟙, z)`, i.e. `X` is an affine image
of `z`; on `𝒞` the proof of Theorem B applies.
(b) By compactness of `𝒞` modulo congruence and continuity it suffices to exclude a sequence
`X_j → [X_k]` with `φ(X_j)/ρ_j² → 0`, `ρ_j = d_P(X_j, X_k)`.  Align optimally:
`X_j = X_k + ρ_j V_j`, `‖V_j‖ = 1`, `V_j` orthogonal to the infinitesimal isometries at `X_k`
(first-order optimality of the alignment); pass to a limit `V`.  The constraints give
`2 e·(V_j)_e + ρ_j |(V_j)_e|² = 0` on `E₀`, so `V` is an infinitesimal flex of `(E₀, X_k)`.
`φ(X_j) = ρ_j²‖Π^⊥V_j‖²` because `Π^⊥X_k = 0`, so `Π^⊥V = 0`: `V = zBᵀ + 𝟙tᵀ` with
`B ∈ ℝ^{d×dK}`.  For a stacked edge vector `e`, the edge of `X_k` is `Π_k e/√w_k` (`Π_k` the
coordinate projection to block `k`) and the edge of `V` is `Be`; the flex condition
`(Π_k e)·(Be) = 0` says that the symmetric part of `Π_kᵀB` lies in `𝒩(z) = 𝒯`.  `Π_kᵀB` has
non-zero rows only in block `k`; a block-scalar symmetrisation forces its blocks outside
`(k, k)` to vanish, then `s_l = 0` for `l ≠ k`, then `s_k = 0` by `Σ w_l s_l = 0`; so `B`
is supported on block `k` with a skew block: `V` is an infinitesimal isometry.  Contradiction.
(c) `∫ φ dμ = 0`, so `∫ φ dν = −½⟨Π^⊥, M(ν) − M(μ)⟩ ≤ ½‖Π^⊥‖_F ‖M(ν) − M(μ)‖_F`, and
`φ ≥ κ min_k d_P(·, X_k)²`.
(d) Write `η = ‖M(ν) − M(μ)‖_F`, `Q = ∫ min_k d_P² dν ≤ C₁η`, and let `ν_k` be the mass of the
`k`-th nearest-state cell.  For `X` in cell `k`, optimally aligned, `X = X_k + Δ`,
`D(X) − D(X_k) = L_k(Δ) + D(Δ)` with `L_k` linear and `‖D(Δ)‖ ≤ 4‖Δ‖²`; and
`Δ = τ + O(‖Δ‖²)` with `τ` tangent to `𝒞` at `X_k` (smoothness).  Hence
`M(ν) − M(μ) = Σ_k (ν_k − w_k)D(X_k) + Σ_k L_k(τ̄_k) + R`, `‖R‖ ≤ C₂Q`, with `τ̄_k` tangent.  The
linear map `(a, τ̄) ↦ Σ a_k D(X_k) + Σ L_k(τ̄_k)` on `{Σ a_k = 0} × ∏(T_{X_k}𝒞 ⊖ isometries)` is
injective: **(CC) implies infinitesimal identifiability.**  [If it vanishes, the derivative of
the stacked Gram matrix vanishes, so the derivative of the stacked configuration is `zΞ` with
`Ξ` skew; evaluating the flex condition of each state on the stacked edge vectors shows
that the symmetric part of `ΞE_k`, minus `(a_k/2w_k)E_k`, lies in `𝒩(z) = 𝒯`; block-scalarity
kills the off-diagonal blocks of `Ξ`, and the trace condition of `𝒯` gives `a_k = 0`.]  So
`Σ|ν_k − w_k| ≤ C₃(η + Q)`.  Transport every conformation to its nearest state (cost `Q`), then
move the excess mass between states (cost at most `diam² · ½Σ|ν_k − w_k|`):
`W₂² ≤ 2Q + diam²·C₃(η + Q) ≤ C_μ η`.
(e) Replace the state `X_1 = X(θ)` by the two states `X(θ ± εv)` with weights `w_1/2`: `M`
changes by `O(ε²)` (the first-order terms cancel) and `W₂² = w_1 ε² |∂_v X|²(1 + o(1))`.  ∎

The certificate `φ` is linear in the data: `∫ φ dν` is computed from `M(ν)` alone, it vanishes
for `μ`, and it bounds the mean squared distance of `ν` from the `K` states.  It is the
ensemble analogue of the energy of a positive semidefinite stress.  `κ` is defined by a global
infimum; its local value at `X_k` — the smallest eigenvalue of `Π^⊥` on the flex space of
`X_k` — is a linear-algebra quantity, a certified global lower bound is a global optimisation
over `𝒞` (not attempted; `PROOF_OBLIGATIONS.md`, O-5).

---

## 8. Realizability of averaged data, and ensemble rigidity

### 8.1 The set of realizable averaged data and its semidefinite relaxation

Let `𝒮 = 𝒮(E₀, ℓ)` be the set of all squared-distance matrices of configurations in Euclidean
spaces of arbitrary dimension satisfying the `E₀`-constraints ("Hilbert-space conformations").
`𝒮` is a compact spectrahedron, and by Lemma 2.1 `𝒦 = conv D(𝒞) ⊆ 𝒮`: every averaged data set
passes the semidefinite (Schoenberg) test with the statewise constraints imposed on the
averages.

**Theorem D [P; (a) from a known bound, (b) with an exact witness].**
(a) If `|E₀| < (d + 1)(d + 2)/2` then `𝒦 = 𝒮`.  In space: if `|E₀| ≤ 9`.  In particular for
chains with fixed bond lengths and angles and `n ≤ 6` atoms, and for freely jointed chains
with `n ≤ 10` atoms: *a matrix of averaged squared distances is realizable by an ensemble of
conformations iff it is a Euclidean distance matrix with the prescribed bond data.*
(b) For chains with fixed bond lengths and angles and `n ≥ 7` (unit bonds, bond-angle cosine
`−5/13`; generic bond geometry), `𝒦 ⊊ 𝒮`: there are Euclidean distance matrices with the
prescribed bond data that are not the averaged data of any ensemble.

*Proof.*  (a) `𝒮` is the convex hull of its extreme points; an extreme point of a spectrahedron
cut out by `m` linear equations has rank `r` with `r(r + 1)/2 ≤ m` (Barvinok 1995, Pataki
1998), here `m = |E₀|`; so `r ≤ d`, i.e. extreme points are conformations in `ℝ^d`.
(b) A point of `𝒮` of rank `r`, realised by `y` in `ℝ^r`, is extreme iff `𝒩(y) = 0` (a
perturbation within the face is `y(I ± S)^{1/2}`).  An extreme point of `𝒮` that lies in
`𝒦 = conv D(𝒞) ⊆ 𝒮` is an extreme point of `𝒦`, hence belongs to the compact set `D(𝒞)`, hence
has rank at most 3.  `experiments/geometry/exact_4d_extreme.py` constructs a chain with 7 atoms
in `ℝ⁴` with rational coordinates (unit quaternions), bond vectors spanning `ℝ⁴`, and with
`rank = 10 = dim Sym(4)` for the 11 conditions `eᵀSe = 0`: a rank-4 extreme point of `𝒮`.
Longer chains: prolong it.  ∎

(a) is the statement that the extreme Gram dimension of the constraint pattern is at most
`d`; for freely jointed chains it is the classical fact that correlation matrices of order at
most 9 are mixtures of correlation matrices of rank at most 3 (§9).  The chain version, and
the reading "semidefinite feasibility = ensemble realizability for short chains", are the
contribution.  For a general pair set `F` deciding membership in the projection of `𝒦` is
NP-hard already for star-shaped statewise constraints, by the theorem of E.-Nagy, Laurent and
Varvitsiotis on the convex hull of the rank-constrained elliptope (§9).

### 8.2 Ensemble rigidity

Let `F` be a set of pairs.  A conformation `X ∈ 𝒞` is **`F`-ensemble-rigid** if `δ_X` is
identifiable from the averaged squared distances on `F`: no ensemble of conformations other
than copies of `X` reproduces `D(X)` on `F`.  Recall that the bar framework `(F ∪ E₀, X)` is
*globally rigid* if every configuration in `ℝ^d` with the same lengths on `F ∪ E₀` is
congruent to `X`, and *universally rigid* if this holds in every dimension.

**Theorem E (a hierarchy) [P; for finite mixtures the reduction step of (a) and the first
half of (b) are V: `MetricChain.Geometry.ensembleRigid_of_universal`,
`MetricChain.Geometry.globallyRigid_of_ensembleRigid`].**
Let `X ∈ 𝒞` span `ℝ^d` affinely.
(a) If `(F ∪ E₀, X)` is universally rigid and `𝒩(X) = 0`, then `X` is `F`-ensemble-rigid.
(b) If `X` is `F`-ensemble-rigid, then `(F ∪ E₀, X)` is globally rigid and `𝒩(X) = 0`.
(c) If `𝒦 = 𝒮` (Theorem D(a): e.g. chains with `n ≤ 6`), then `X` is `F`-ensemble-rigid iff
`(F ∪ E₀, X)` is universally rigid and `𝒩(X) = 0`.
(d) The converse of (b) fails: there are globally rigid chains with `𝒩(X) = 0` that are not
`F`-ensemble-rigid.

*Proof.*  (a) The Hilbert configuration of a competing `ν` has the lengths of `X` on
`F ∪ E₀`, so it is congruent to `X`, `M(ν) = D(X)`, and Theorem A applies.  (b) A configuration
with the same lengths is a one-state ensemble; and if `0 ≠ S ∈ 𝒩(X)`, the mixture of the two
affine images `X_±` of Theorem A has the same averaged data on all pairs.  (c) If `X` is
`F`-ensemble-rigid and `y` is a Hilbert-space configuration with the lengths of `X` on
`F ∪ E₀`, then `D(y) ∈ 𝒮 = 𝒦` is the averaged data of an ensemble of conformations, which
agrees with `X` on `F`; so that ensemble is `δ_{[X]}` and `D(y) = D(X)`.  (d) By (c): take
`n = 6` and `F` such that `(F ∪ E₀, X)` is globally but not universally rigid — a generic
framework with a one-dimensional space of equilibrium stresses whose stress matrix has rank
`n − 4` but is indefinite (Gortler–Healy–Thurston; Gortler–Thurston).  An explicit instance
with `F = {14, 25, 36, 16}` and a two-state ensemble of other chains with the same averaged
data, computed to 12 digits, is in `experiments/geometry/hierarchy_example.py` **[N for the
instance]**.  ∎

**Open (O-3).**  Is the first implication strict when `𝒦 ≠ 𝒮` — is there an
`F`-ensemble-rigid conformation whose framework is not universally rigid?  A sufficient
condition for `F`-ensemble-rigidity that does not imply universal rigidity: `X` is the unique
maximiser over `𝒞` (conformations in `ℝ^d`) of `Σ_{ij ∈ F} c_ij |x_i − x_j|²` for some
couplings `c` — then `D(X)|_F` is an exposed point of the realizable set.  Universal rigidity
asks for the same in every dimension.  A numerical search over 7-atom chains is recorded in
`RESEARCH_LOG.md`; no certified example yet.

---

## 9. Prior art and novelty assessment (summary; details and search log in `PRIOR_ART.md`)

*Known, and used as such.*
* The stacking lemma is the direct-sum property of Euclidean distance matrices
  (Schoenberg); "an average of squared distances is a squared distance in a higher
  dimension" is folklore.  **[K]**
* Conics at infinity, affine flexes and their role in universal rigidity: Connelly (1982,
  2005); Alfakih; Gortler–Thurston 2014 (a generic universally rigid framework has a positive
  semidefinite stress matrix of maximal rank); Connelly–Gortler 2015.  Theorem A (ii)⇔(iii) is
  this theory; the equivalence with (i), and Theorem F for `K = 1`, are reinterpretations.
  **[K in substance]**
* Rank of extreme points of spectrahedra: Barvinok 1995, Pataki 1998; extreme correlation
  matrices: Grone–Pierce–Watkins 1990, Li–Tam 1994.  Convex hull of the rank-constrained
  elliptope, extreme Gram dimension, NP-hardness of membership: E.-Nagy, Laurent,
  Varvitsiotis 2012–2014.  Theorem D(a) for freely jointed chains is a case of these.  **[K]**
* Simplicial faces of the elliptope spanned by rank-one matrices: Tropp 2018; the link between
  faces of the elliptope and ellipsoid fitting: Saunderson, Chandrasekaran, Parrilo, Willsky
  2012.  Our Remark 2.3 and Corollary 4.2 are relatives (rank-`d` generators, structured
  point sets), not consequences.  **[K, related]**
* Non-uniqueness of distributions with given mean squared distances without statewise
  constraints: e.g. the maximum-entropy construction of Shi and Thirumalai 2023 notes it;
  Proposition 3.1 is elementary.  **[K]**
* Extra distance constraints between neighbouring points restoring identifiability in a
  *different* mixture-type model (two homologous chains in one frame, ambiguous sums of
  inter- and intra-chain terms): Belyaeva, Kubjas, Sun, Uhler 2022; Cifuentes, Draisma,
  Henriksson, Korchmaros, Kubjas 2024.  Related in spirit; the model, the data and the
  theorems are different (there squared distances do *not* give finite identifiability).
  **[K, related]**
* Second moments suffice under a prior: Bendory–Edidin and co-authors (sparse signals;
  generic semi-algebraic priors) for multi-reference alignment.  Our Corollary 9.1 is an
  instance with a specific, non-generic prior and a mixture.  **[K, related]**

*Not found in print (searches of 2026-11-26; an absence in searches is not a proof of
novelty).*  Theorem B and B′ (identifiability of a mixture among all ensembles from averaged
squared distances via the trivial-quadric condition); the thresholds of Theorem C; the
algorithm DEMIX; Theorem G (global `W₂` stability with the explicit certificate); Theorem F for
`K ≥ 2`; ensemble rigidity as a notion between global and universal rigidity, Theorem E;
Theorem D for chains with bond angles and the exact rank-4 witness; Theorem H (range `K + 3`).

**Corollary 9.1 (a consequence for reconstruction with unknown orientations) [P, given K].**
Observe `y = g·X_κ + σξ`: a conformation drawn from `μ`, rotated by a Haar-random `g ∈ O(3)`
(or `SO(3)`), labelled atoms, Gaussian noise.  Then `E[y_i y_jᵀ] = ⅓⟨⟨x_i, x_j⟩⟩_μ I₃ + σ²δ_ij I₃`:
the second moment of the data determines exactly `M(μ)` (for centred conformations), and
nothing else.  Hence under (CC) the shape distribution is a function of the second moment,
whereas without statewise constraints no mixture with `K ≥ 2` is (Proposition 3.1).  In the
framework of Bandeira, Blum-Smith, Kileel, Perry, Weed and Wein — the number of samples needed
at noise level `σ` grows like `σ^{2q}` with `q` the smallest moment order that determines the
orbit — the constraints lower the order from `q ≥ 3` to `q = 2`.  We did not re-derive the
sample-complexity theorem; the statement is conditional on it.

---

## 10. Machine-checked statements

`proofs/Geometry/EnsembleRigidity.lean` (Lean 4.31, Mathlib v4.31.0; zero warnings; axioms
`propext`, `Classical.choice`, `Quot.sound` only; imported by `proofs/AxiomAudit.lean`, which
now walks 5 0xx declarations — the exact number is in `docs/collaboration/status/geometry.md`).

| declaration (namespace `MetricChain.Geometry`) | statement | used in |
|---|---|---|
| `stacked_sqdist` | `‖z_i − z_j‖² = Σ_k w_k ‖x_i^{(k)} − x_j^{(k)}‖²` for the stacked configuration in the `ℓ²` product | Lemma 2.1 |
| `stress_energy_eq`, `mixture_energy_eq` | for symmetric `Ω` with zero row sums, `yᵀΩy = −½ Σ Ω_ij (y_i − y_j)²`; the `Ω`-energy of a finite mixture is linear in its averaged squared distances | Theorems F, G |
| `stress_certificate` | `Ω ⪰ 0`, zero row sums, annihilating a reference mixture; a second finite mixture with the same averaged squared distances on the support of `Ω` has every coordinate of every state of positive weight in `ker Ω` | Theorem F (first half of the proof) |
| `block_coeff_nonneg`, `block_rigidity` | a linear map into a space of dimension `≤ d` whose squared norm is `c₁‖u‖² + c₂‖u'‖²` on two orthogonal blocks of dimension `d ≥ 1` has `c₁ = 0` or `c₂ = 0` (and `c_k ≥ 0`) | Theorems B, F, G ("one block only") |
| `sqdist_midpoint_of_conic` | affine flexes: maps `A_±` preserving edge lengths with the midpoint identity | Theorem A (iii)⇒(ii), Theorem E(b) |
| `globallyRigid_of_ensembleRigid` | ensemble rigidity (finite mixtures) implies global rigidity on `F ∪ E₀` | Theorem E(b) |
| `ensembleRigid_of_universal` | universal rigidity of `(F ∪ E₀, x)` reduces `F`-ensemble rigidity to ensemble rigidity for complete averaged data | Theorem E(a) |
| `fourAtom_not_ensembleRigid_witness`, `block_rigidity_nonvacuous` | non-vacuity | Example 3.3 |

Not machine-checked: Lemma 2.2 (the linear isometry from equal Gram matrices; the measurable
version), the conclusion of Theorem A (ii)⇒(i) and of Theorem B from `block_rigidity`
(assembling the blocks), Theorem B′, everything about genericity and thresholds (Theorems C,
D, H: exact computations outside Lean), Theorem G.  `UniversallyRigid` in the Lean file
quantifies over inner product spaces of one universe; `SameShape` is equality of all pairwise
distances (for point configurations in Euclidean spaces: congruence).

---

## 11. Reproduction

```
python3 experiments/geometry/run_checks.py           # all tests below (about one minute)
python3 experiments/geometry/exact_conic_rank.py 12  # Theorem C(b)
python3 experiments/geometry/exact_jacobian_rank.py 8# Theorem H
python3 experiments/geometry/exact_4d_extreme.py     # Theorem D(b)
python3 experiments/geometry/demix.py                # algorithm DEMIX on synthetic ensembles
python3 experiments/geometry/hierarchy_example.py    # Theorem E(d), numerical instance
python3 experiments/geometry/mutation_checks.py      # the tests detect planted errors
```

## 12. Limitations

* Averaged *squared* distances are one specific linear observable.  Nothing here applies to
  averages of other functions of distance (inverse sixth powers, contact frequencies,
  scattering curves); for those the stacked configuration is not a Euclidean framework.
* Identifiability is for exact data.  The quantitative theorem (G) has a constant defined by a
  global infimum that we do not compute, holds under the conic condition only, and its
  exponent means that a symmetric broadening of a state by `ε` is invisible at order `ε`.
* Generic statements exclude a proper analytic subset of conformations that we do not
  describe.  Planar and other symmetric conformations can violate (CC) at any length.
* The sharp threshold of Theorem C(b) is proved for twelve values of `K` at two bond
  geometries by exact computation; for all `K` it is a conjecture.  The threshold for
  identifiability among all ensembles below the conic threshold is numerical.
* Theorem H is local and within the `K`-state family; it says nothing about ensembles with a
  different number of states or far away.
* No noise model, no statistics, no algorithmic guarantee for DEMIX under perturbation.
