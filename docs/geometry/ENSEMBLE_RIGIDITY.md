# Second-moment rigidity of conformational ensembles

**Geometric Inference, Rigidity and Inverse Problems Division — cycle 1 report.**
Branch `research/geometric-inference`.  Labels as in `docs/collaboration/README.md`:
**[V]** machine-checked in Lean (declaration named), **[P]** paper proof in this file,
**[P, exact]** paper proof whose finite part is an exact computation (script named; rational or
modular arithmetic, no floating point), **[K]** known result (cited), **[N]** numerical evidence
only, **[C]** conjecture.  Nothing in this file has been refereed by another division (the
Science division's review is running: its SCI-RES-0029).  An internal adversarial review of
the fifth-checkpoint version (commit `e8e2582`) is preserved verbatim in
`docs/collaboration/messages/geometry/GEOMETRY-REV-0001.md`; it found no false theorem, four
statements that said more than was proved and sixteen minor defects, all corrected here and
listed in `docs/geometry/DEAD_ENDS.md` DG-13 … DG-17 (the text added after `e8e2582` — Theorem
G′, the new form of Theorem C(c), the corrections themselves — has not been reviewed).  The
novelty assessment (what is known, what is a reformulation, what we did not find in print)
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
   (§4, Theorems A, B).  A single conformation that spans space (is not planar) is the only
   ensemble with its `M` iff its constrained edge directions lie on no conic at infinity (for
   `K = 1` this is a reinterpretation of a classical lemma of rigidity theory).  A `K`-state mixture is the only
   ensemble — among **all** probability distributions on conformations, with any number of
   states — with its `M`, as soon as the only quadrics through the constrained edge
   directions of the stacked framework are the `K − 1` trivial ones.
4. **Sharp thresholds** (§5, Theorem C).  For freely jointed chains the conic condition holds
   generically iff the chain has at least `(9K² + K + 2)/2` bonds [P, all `K`].  For chains
   with fixed bond lengths and bond angles it holds generically iff
   `n ≥ ⌈(9K² + K + 8)/4⌉` atoms: 5, 12, 23, 39, 60, … [P, exact for `K ≤ 20` at one bond
   geometry and `K ≤ 12` at a second; the threshold `(9K² − 5K + 6)/2` — twice the sharp
   one for large `K` — for every `K` and every bond angle, the same at all positions; the
   sharp threshold for all `K`, and anything for position-dependent bond angles, is open].
5. **A polynomial-time demixing algorithm with a certificate** (§6): eigen-decomposition of the
   centred `M`, one linear system, one symmetric eigenproblem.  The certificate of uniqueness
   is a rank.
6. **A global quantitative theorem** (§7, Theorem G): under the conic condition
   `W₂(ν, μ)² ≤ C·‖M(ν) − M(μ)‖` for *every* ensemble `ν`, with an explicit dual certificate
   (a positive semidefinite "ensemble stress"); the exponent is optimal.  With incomplete
   averaged data, a positive semidefinite stress of the stacked framework supported on the
   measured pairs certifies identifiability (Theorem F) — for `K = 1` this is the classical
   sufficient condition for universal rigidity.
7. **A rigidity notion for averaged data** (§8, Theorem E): *second-moment rigidity* — no
   ensemble of other conformations has the averaged squared distances of `X` on the measured
   pairs.  With (C₁) the conic condition of the single conformation (`𝒩(X) = 0`),

       universal rigidity and (C₁)  ⇒  second-moment rigidity  ⇒  global rigidity and (C₁).

   (C₁) cannot be dropped on the left: if measurements and constraints together form a
   complete graph the framework is universally rigid for a trivial reason, while a cis/trans
   mixture has the same averaged data (Example 3.3; machine-checked instance
   `universal_not_secondMomentRigid`).  The second implication is strict [P, exact witness]:
   a globally rigid conformation with (C₁) whose averaged data are reproduced by an ensemble
   of other conformations.  For chains with at most 6 atoms the first is an equivalence,
   because there every Hilbert-space chain is an ensemble average of chains in `ℝ³`
   (Theorem D); from 7 atoms on the set of realizable averaged data is strictly smaller than
   its semidefinite relaxation [P, exact witness], and numerically the first implication is
   strict as well — a 7-atom chain that is second-moment rigid although a four-dimensional
   framework has the same measured lengths [N].
8. **How little data suffices** (§5.3–5.5): within the family of `K`-state ensembles, complete
   averaged data are generically *locally* identifying exactly from the parameter count
   `n ≥ 2K + 3` on, and averaged distances of sequence separation at most `K + 3` are
   locally identifying, while for `K ≥ 2` separation `K + 2` never is (for one state
   separation 3 suffices) [P, exact for `K ≤ 8` at two bond geometries]; among all ensembles
   a separation of `3K + 1` suffices for mixtures that satisfy (CC) and whose stacked
   configuration has every `3K + 1` consecutive points affinely independent [P; the second
   hypothesis is generic for every `K`, by the proof of Theorem C(c)].
9. **Two states, completely** (§5.5, Theorem I).  A generic two-state ensemble is identifiable
   among all ensembles from `n = 10` atoms on [P, exact: a Gröbner-basis computation shows
   that the only chains that are linear images of the stacked configuration are the two
   states]; at `n = 7, 8` it is **not** — explicit ensembles of 9 to 11 *other* chains have
   the same averaged data to `10⁻¹⁴` [N] — although it is locally identifiable among
   two-state ensembles there; `n = 9` is identifiable in every instance computed [N]; the
   linear certificate needs `n ≥ 12`.  So "identifiable among all ensembles" (10 proved; 9 in
   every instance computed), "locally identifiable among two-state ensembles" (7) and
   "certifiable by linear algebra" (12) are three different thresholds.  Whether a two-state
   ensemble with 7 to 9 atoms is the only *two-state* ensemble with its data globally, not
   only locally, is not proved (direct searches found no other [N]).  For `K = 3` the first
   threshold is numerically 14 (at 13 atoms it depends on the instance); in general
   `⌊9K/2⌋ + 1` is a conjecture.

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

**Lemma 2.1 (stacking) [V for finite mixtures: `MetricChain.Geometry.stacked_sqdist`; the `L²`
form P].**  For a finite mixture
`μ = Σ_k w_k δ_{X_k}` put `z_i = (√w_k · x_i^{(k)})_{k=1..K} ∈ ℝ^{dK}`.  Then
`M(μ)_ij = |z_i − z_j|²`.  For an arbitrary ensemble the same holds with
`z_i = (x ↦ x_i) ∈ L²(μ; ℝ^d)` (after fixing `x_1 = 0`).  ∎

So `M(μ)` is always a Euclidean distance matrix; its embedding dimension is `dK` for a generic
`K`-mixture with `n − 1 ≥ dK`.  The states are the coordinate blocks of `z`; write `E_k` for the
orthogonal projection of `ℝ^{dK}` onto block `k`.  The edge vectors of `z` satisfy

    eᵀ E_k e = w_k ℓ_e²,     |e|² = ℓ_e²        (e an E₀-edge vector of z).            (2.1)

Hence `𝒩(z)` always contains the `(K − 1)`-dimensional space of **trivial quadrics**

    𝒯 = { Σ_k s_k E_k : Σ_k w_k s_k = 0 }.

**Lemma 2.2 (every competing ensemble consists of linear images of `z`) [P; for finite
competing mixtures V: `MetricChain.Geometry.state_is_linear_image`, `exists_linearMap_of_gram_eq`].**  Let
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
`X^{(c)}` is the collinear configuration given by the `c`-th coordinates; and
`D(X) = ½D(√2·X) + ½D(point)`.  So, with no statewise constraint, no configuration with two
distinct points is determined by its squared distances among ensembles — although it is
determined among configurations.
(b) Let `μ = Σ w_k δ_{X_k}` with stacked configuration `z` spanning `ℝ^{dK}`, `K ≥ 2`.  For every
`Q ∈ O(dK)` and all weights `w'_k > 0` with sum one, the blocks of `zQ` divided by `√w'_k`
are the states of a `K`-state mixture `μ_{Q,w'}` with `M(μ_{Q,w'}) = M(μ)`; the family of their
classes has dimension `dim O(dK) − K·dim O(d) + (K − 1) = d²K(K − 1)/2 + K − 1` (10 for two
states in space).
(c) With statewise constraints `E₀`, `μ_{Q,w'}` is an ensemble on `𝒞` iff every block projection
`Q E_k Qᵀ / w'_k` lies in `𝒫(z)` (which fixes the weights).  ∎

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
(Example 3.3); a generic chain with `n ≥ 5` atoms satisfies it, for every bond angle in
`(0, π)` that is the same at all positions and any bond lengths (Theorem C(c) with `K = 1`;
exact witnesses at two bond geometries: `experiments/geometry/exact_conic_rank.py`).  A
generic freely jointed chain satisfies it iff it has at least 6 bonds.

### 4.2 Finite mixtures

**Theorem B (identifiability of a mixture among all ensembles) [P; the statement on states
against finite competing mixtures V: `MetricChain.Geometry.mixture_identifiable_stacked`].**  Let `μ = Σ_{k=1}^K w_k δ_{X_k}`, `w_k > 0`, with
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

Machine-checked **[V]** (`finite_mixture_identifiable`): let `z` be a configuration whose
differences from a base point span an inner product space carrying pairwise orthogonal
blocks of dimension `d ≥ 1` with component maps, and assume (CC) in the form "every symmetric
bilinear form vanishing on the constrained edge vectors of `z` is block-scalar".  If a
**finite** mixture of configurations in a space of dimension at most `d` has the squared
distances of `z` on average (all pairs) and each of its states of positive weight has the
edge lengths of `z` on the constrained pairs, then every such state `Y` satisfies
`|Y_i − Y_{i'}|² = c·|comp_{k₀}(z_i − z_{i'})|²` for one block `k₀` and one `c ≥ 0`.  In
coordinates **[V]** (`mixture_identifiable_stacked`): for states `X_k` in a space of dimension
`d ≥ 1` with weights `w_k > 0`, `Σ w_k = 1`, common lengths on the constrained pairs (one of
them non-zero), and `z` their stacked configuration in the `ℓ²` product with its coordinate
blocks, every state of positive weight of a competing finite mixture has all pairwise
distances equal to those of one `X_{k₀}`.  The hypotheses are satisfiable with two different
states, and the theorem is used end to end, in `line_mixture_example` (the straight and the
folded three-point unit chain on the line, weights ½; (CC) and the spanning condition are
proved in Lean for this instance: `line_conic`, `line_span`).  The proof in Lean follows the
proof above: the linear isometry from equal Gram matrices (`exists_linearMap_of_gram_eq`),
its components (`state_is_linear_image`), and the block argument (`mixture_state_of_conic`,
`block_rigidity`).  What remains on paper: competing ensembles that are not finitely
supported (the `L²` version of Lemma 2.2), the weights of the competing mixture, and (CC)
itself for three-dimensional chains (an exact computation outside Lean, Theorem C).

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
If `μ = Σ w_k δ_{X_k}`, with pairwise non-congruent states and positive weights, is
identifiable (in particular under (CC), which implies both), then `D(X_1), …, D(X_K)` are
affinely independent and their convex hull is a face of `𝒦 = conv D(𝒞)`.

*Proof.*  If `Σ a_k D(X_k) = 0`, `Σ a_k = 0`, then `μ_t = Σ (w_k + t a_k)δ_{X_k}` is an ensemble
with `M(μ_t) = M(μ)` for small `t`, so `[μ_t] = [μ]`, and `a = 0` because the `X_k` are pairwise
non-congruent.  Let `Φ` be the smallest face of `𝒦` containing `M(μ)`; `M(μ)` is in its
relative interior, so for `y ∈ Φ` there are `y' ∈ Φ` and `t ∈ (0, 1]` with
`M(μ) = t y + (1 − t) y'`; `y = M(ν_y)`, `y' = M(ν_{y'})`, and identifiability of `μ` forces
`ν_y` to be carried by the classes `[X_k]`, i.e. `y ∈ conv{D(X_k)}`.  Conversely
`conv{D(X_k)} ⊂ Φ`: a face that contains a relative interior point of a simplex contains the
simplex.  ∎

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
`−5/13` (112.6°) and `1 ≤ K ≤ 20`, or cosine `−1/3` (109.47°) and `1 ≤ K ≤ 12`: (CC) holds for
generic `K`-tuples of chains iff `2n − 3 ≥ D_K`, i.e.

    n ≥ n₀(K) = ⌈(9K² + K + 8)/4⌉ = 5, 12, 23, 39, 60, 85, 114, 148, 187, 230, 277, 329, …, 907 (K = 20).

The same holds for bond geometries outside a proper analytic subset of the space of bond
geometries.
(c) *Bond lengths and angles, every `K` and every bond angle in `(0, π)`* **[P]**.  Let `r_N`
be the generic rank of the conic system of `K` chains with `N = n − 1` bonds (one bond angle
for all positions and states).  Then
(i) the increments `r_{N+1} − r_N ∈ {0, 1, 2}` are non-increasing in `N`;
(ii) `r_{N+1} > r_N` as long as `r_N < D_K`;
(iii) `r_N = 2N − 1` for `N ≤ 3K`.
Hence `r_N ≥ min(N + 3K − 1, D_K)`, and (CC) holds for generic `K`-tuples as soon as

    n ≥ D_K − 3K + 2 = (9K² − 5K + 6)/2 = 5, 16, 36, 65, 103, …

(sharp for `K = 1`; twice the sharp value of (b) for large `K`).
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
each `K` in these ranges, chains with rational torsion half-angle tangents
at which the rank of the conic system, computed modulo a prime after an exact evaluation in
`ℚ` respectively `ℚ(√2)`, equals `D_K` at `n = n₀(K)`.  A ring homomorphism to a field cannot
increase a rank, so the rank over the number field is `D_K`.  The rank is attained on the
complement of a proper analytic subset of the torus of torsions (and of the space of bond
geometries, on which the entries depend analytically as well); adding atoms adds conditions,
so the rank stays `D_K` for `n > n₀(K)`.  For `2n − 3 < D_K` the count forbids (CC).  ∎

*Proof of (c).*  Notation.  `M = (S²)^K`; `γ` the cosine of the angle `α ∈ (0, π)` between
consecutive bond vectors, `σ = sin α`; for `p ∈ M`, `A(p) = {q ∈ M : q^{(k)}·p^{(k)} = γ for all k}`
(a product of `K` circles), `V(p) = ⊕_k (p^{(k)})^⊥` (dimension `2K`), so that
`A(p) = (γp + V(p)) ∩ M` and the differences of points of `A(p)` span `V(p)`.  The stacked bond
vectors of `K` chains are the points of the path space
`𝒫_N = {(p_1, …, p_N) : p_{i+1} ∈ A(p_i)}`, a compact connected real-analytic manifold (an
iterated bundle of tori over `M`); dropping the first or the last point is a surjective
submersion `𝒫_{N+1} → 𝒫_N`.  Given the bond conditions, the second-neighbour conditions are
`p_iᵀSp_{i+1} = 0`; so the conic system of a path `π` is the set of functionals
`λ_{p_i}: S ↦ p_iᵀSp_i` (`i ≤ N`) and `λ_{p_ip_{i+1}}: S ↦ p_iᵀSp_{i+1}` (`i < N`), with span
`W(π)` and common kernel `𝒩(π) ⊇ 𝒯`.  `r_N = max_π dim W(π)` is attained on an open dense
subset `U_N ⊂ 𝒫_N` (the complement of a proper analytic subset), and preimages of the `U`'s
under the submersions are open and dense.

**Lemma R (reachability).**  For `u, v ∈ S²` and `m ≥ m₀ := max(2, ⌈π/min(α, π − α)⌉)` there is
a sequence `u = û_0, …, û_m = v` with consecutive angles `α`.  *Proof.*  The set reachable from
`u` in `m` steps is `{v : ∠(u, v) ∈ J_m}` with `J_1 = {α}` and
`J_{m+1} = ∪_{ρ ∈ J_m} [|ρ − α|, min(ρ + α, 2π − ρ − α)]` (spherical triangle inequality,
all intermediate values attained by continuity).  By induction, for `α ≤ π/2`,
`J_m = [0, min(mα, π)]` for `m ≥ 2`; for `α > π/2`, with `β = π − α`,
`J_m = [0, min(mβ, π)]` for even `m` and `[max(0, π − mβ), π]` for odd `m`.  In both cases
`J_m = [0, π]` iff `m ≥ m₀`.  ∎

*(i).*  Take a path `(p_1, …, p_{N+2})` such that it, `(p_1, …, p_{N+1})`,
`σ = (p_2, …, p_{N+1})` and `(σ, p_{N+2})` have the generic ranks of their lengths (open dense
conditions).  Let `Y` be the span of the two functionals at the new end,
`λ_{p_{N+2}}` and `λ_{p_{N+1}p_{N+2}}`.  For subspaces `A ⊂ A'`,
`dim(A' + Y) − dim A' ≤ dim(A + Y) − dim A`.  With `A = W(σ) ⊂ A' = W(p_1, …, p_{N+1})` the left
side is `r_{N+2} − r_{N+1}` and the right side is `r_{N+1} − r_N`.  (The generic ranks form the
rank function of a matroid on the conditions that is invariant under shifts along the chain;
(i) is its submodularity.)

*(ii).*  Suppose `r_{N+1} = r_N`.  By (i), `r_{N'} = r_N` for all `N' ≥ N`.  Let `π ∈ U_N` and let
`(π, q_1, …, q_m)` be any continuation.  Its rank is at most `r_{N+m} = r_N = dim W(π)`, so its
span is `W(π)`: every `S ∈ 𝒩(π)` satisfies `q_jᵀSq_j = 0`.  By Lemma R every point of `M` is
some `q_m`.  So `F_S ≡ 0` on `M`, i.e. `S ∈ 𝒯` (proof of (a)): `𝒩(π) = 𝒯`, `r_N = D_K`.

*(iii).*  It suffices to find, for `N ≤ 3K`, one path with linearly independent
`p_1, …, p_N ∈ ℝ^{3K}`: then `Σ a_ip_ip_iᵀ + Σ c_i(p_ip_{i+1}ᵀ + p_{i+1}p_iᵀ) = PCPᵀ` with `P`
injective and `C` tridiagonal vanishes only for `C = 0`.  Induction on the length `j < 3K`:
paths with independent points form a non-empty open set `O_j`; we show that for some path in
`O_j` the torus `A(p_j)` is not contained in `Π_j = span(p_1, …, p_j)`.  Otherwise
`V(p_j) ⊂ Π_j` on `O_j`.  Then `j ≥ dim(V(p_j) + ℝp_j) = 2K + 1`, and every `ν ⊥ Π_j` is
orthogonal to `V(p_j)`, i.e. `ν^{(k)} = μ_kp_j^{(k)}`, with `Γμ = 0` for the `j × K` matrix
`Γ_{ik} = p_i^{(k)}·p_j^{(k)}`; as `dim Π_j^⊥ = 3K − j ≥ 1`, `Γ` has a kernel on `O_j`.  But `Γ`
has rank `K` on a non-empty open set of `𝒫_j` (which meets `O_j`): build the path backwards
from `p_j`; the row `i = j` is `(1, …, 1)`, and for `m ≥ 2` the entry `Γ_{j−m,k}` ranges, as
`p_{j−m}^{(k)}` moves on its circle about `p_{j−m+1}^{(k)}`, over a non-degenerate interval
(for `m = 2` the interval `[cos 2α, 1]`; for `m ≥ 3` whenever `p_j^{(k)} ≠ ±p_{j−m+1}^{(k)}`),
independently for each `k`.  A box in `ℝ^K` is not contained in a proper subspace, so the
rows `j, j − 2, …, j − K` can be made independent (`j − K ≥ 1`).  Contradiction.

*Conclusion.*  By (iii) `r_{3K} = 6K − 1`; by (ii) the rank then grows by at least one per
bond until it is `D_K`, which happens at the latest for `N = D_K − 3K + 1` bonds.  ∎

**Remark (two equivalent forms of the conic condition).**  (1) *Jacobi matrices.*  A linear
relation among the `2N − 1` conditions is a symmetric tridiagonal `N × N` matrix `J` with
`PJPᵀ = 0`, `P` the `3K × N` matrix of stacked bond vectors: the row space of `P` — the span of
the `3K` coordinate sequences of the bond vectors — is totally isotropic for `J`.  So
`r_N = 2N − 1 − dim{J tridiagonal : PJPᵀ = 0}`, and (d) says that no Jacobi matrix has this
property as long as `2N − 1 ≤ D_K`.  (2) *Squares of codes.*  `r_N` is the dimension of the
componentwise (Schur) square of the `3K`-dimensional space of functions on the constrained
pairs spanned by the coordinates of the stacked edge vectors; for a generic `3K`-dimensional
code of length `2N − 1` this is `min(2N − 1, 3K(3K + 1)/2)`, and (d) says that chain codes
behave like generic ones apart from the `K − 1` relations `|e^{(k)}|² = |e^{(1)}|²`.

Evidence for (d): the exact computation of (b); numerically the same threshold at bond angle
111° for `K ≤ 4` (`experiments/geometry/run_checks.py`, test `conic_threshold_float`).

### 5.2 What the thresholds mean

| | 1 state | 2 states | 3 states | `K` states |
|---|---|---|---|---|
| parameter count allows local identifiability within `K`-state ensembles (complete data; Theorem H) | `n ≥ 4` | `n ≥ 7` | `n ≥ 9` | `n ≥ 2K + 3` (`K ≥ 2`) |
| identifiable among all ensembles | `n ≥ 5` **[P]** | `n ≥ 10` **[P, exact]** (Theorem I); `n = 9` **[N]**; fails for `n ≤ 8` **[N]** | `n ≥ 14` **[N]** | `n ≥ ⌊9K/2⌋ + 1` **[C]** |
| conic condition (CC): linear certificate, polynomial-time demixing **[P, exact]** | `n ≥ 5` | `n ≥ 12` | `n ≥ 23` | `n ≥ ⌈(9K²+K+8)/4⌉` |

The middle row is where the set `𝒫(z)` of chains that are linear images of the stacked
configuration is expected to contain nothing but the `K` states: counting the unknowns of
`A` modulo `O(3)` against the equations, `9K − 3 < 2n − 3`.  This count is a heuristic — the
affine space `I + 𝒩(z)` is not generic, and the complex solution set is larger than the real
one (§5.5).  Where we can check it, it predicts correctly where `𝒫(z)` reduces to the states
(`K = 2`: `n = 10`, Theorem I; `K = 3`: `n = 14` numerically), but identifiability itself can
start earlier: for `K = 2` at `n = 9`, `𝒫(z)` has 2 to 10 further points and the ensemble is
still identifiable in every instance computed (6 by us, 18 by the referee, GEOMETRY-REV-0001);
for `K = 3` at `n = 13` the referee found one instance that is not identifiable and one
without an alternative.  The observed values 5, 9, 14 for `K = 1, 2, 3` equal `⌈9K/2⌉`.  Between the second
and the third row identifiability holds but the certificate is not linear: a gap between
what the data determine and what the algorithm of §6 extracts.

**Remark 5.1 (the gap is a MinRank problem) [the reduction P; the complexity statements K, from
memory of the literature].**  Finding the states from `M` below the conic threshold is:
*find the matrices of rank at most 3 in the affine space `I + 𝒩(z)` of symmetric `3K × 3K`
matrices* — the MinRank problem with target rank 3.  Its dimension `dim 𝒩(z) = 9K(K+1)/2 −
(2n − 3)` runs from about `4.5K² − 9K` at the (conjectured) identifiability threshold down to
`K − 1` at the conic threshold, where the problem is linear (the rank-3 points are read off
the eigenspaces of one element of `𝒩(z)`, §6).  (An earlier version claimed that the
Kipnis–Shamir linearisation of the kernel formulation becomes determined exactly at the conic
threshold; the count does not support this — GEOMETRY-REV-0001, m15 — and the sentence is
withdrawn.)  MinRank is NP-hard in general (Buss–Frandsen–Shallit
1999); for zero-dimensional instances of fixed target rank `r` on `N × N` matrices the known
bounds on the degree of regularity of the minors system are of order `r(N − r)`
(Faugère–Safey El Din–Spaenlehauer), here `≈ 9K`, i.e. a cost `K^{O(K)}`: polynomial for a
fixed number of states — this is how Theorem I was proved for two — and, by the known
general-purpose algorithms, not polynomial in `K`.  Whether the structure of `𝒩(z)` (it
contains `𝒯`; the solutions are orthogonal projectors) allows better is a question for the
Complexity division (GEOMETRY-REQ-0004, C2).

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

So for `2 ≤ K ≤ 8`, at the two bond geometries, the minimal sequence separation of averaged
data that identifies `K` states locally is `K + 3`: from two states on, **each additional
state costs one more unit of range**.  The step from one state to two costs two units: for
`K = 1` separation `3 = K + 2` already gives a square Jacobian of full rank
(`d²_{i,i+3} = A_i − B_i cos θ_i`).  For `K ≥ 9` and for other bond geometries sufficiency is
not proved.  Theorem H is local: it says nothing about `K`-state ensembles far from the given
one (mirror images and permutations of states give the same shape distribution; other
coincidences are not excluded by the argument).

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

The second hypothesis of Theorem F′ (every `3K + 1` consecutive stacked points affinely
independent, i.e. every `3K` consecutive stacked bond vectors linearly independent) is
generic for chains with fixed bond lengths and one bond angle in `(0, π)`, for every `K`
**[P]**: by the proof of Theorem C(c)(iii) a generic path of `3K` stacked bond vectors is
linearly independent, and a generic `K`-tuple of chains has this property in each of its
finitely many windows.  (An earlier version did not prove this; the referee pointed it out
and checked it exactly for `K ≤ 4`, GEOMETRY-REV-0001 m8; our exact check, together with
(CC) at `n₀(K)` for `K ≤ 5` at two bond geometries: `exact_general_position.py`.)  It fails,
like (CC), when all states are helices (§12).

Between `K + 3` (local, within `K`-state ensembles) and `3K + 1` (global, among all
ensembles) we know nothing; see `PROOF_OBLIGATIONS.md`, O-4.  The stress certificates of
Theorem F (§7.1) cannot help here: **a stress supported on pairs of sequence separation at
most `dK` vanishes** whenever every `dK + 1` consecutive stacked points are affinely
independent [P; the referee's observation].  Indeed the first row of a banded `Ω` with
`Ω𝟙 = 0` and `Ωz = 0` is an affine dependency among the points `1, …, w + 1 ≤ dK + 1`, hence
zero; by symmetry the first column vanishes, and the argument repeats with row 2.  So on
sequence-local data Theorem F needs separation `dK + 1` at least, where Theorem F′ already
applies.

### 5.5 Two states: the complete picture

For `K = 2` it is convenient to use the unweighted stack `z̃ = (X_1 | X_2) ∈ (ℝ⁶)^n` (weights
rescale the blocks): a chain that is a linear image of the stacked configuration corresponds
to a symmetric `6 × 6` matrix `P` of rank at most 3 with `ẽᵀPẽ = ℓ_e²` on the `2n − 3`
constrained edge vectors, and the two states are the block projectors `E_1, E_2`.  Let
`L = {P : ẽᵀPẽ = c·ℓ_e² for some scalar c}`, a linear space of dimension `25 − 2n`
generically for `n ≤ 11` (and 2 from `n = 12` on, by (CC)), and `V = {[P] ∈ ℙ(L) : rank P ≤ 3}`, a projective scheme cut out by the
`4 × 4` minors.

**Theorem I (two states, identifiability among all ensembles) [P, exact].**  Unit bonds,
bond-angle cosine `−5/13` (and bond geometries outside a proper algebraic subset).  For
generic pairs of chains with `n ≥ 10` atoms and all weights, `𝒫(z) = {E_1/w_1, E_2/w_2}` —
even among complex symmetric matrices — and therefore the two-state ensemble is identifiable
from averaged squared distances among all ensembles.

*Proof.*  It suffices to treat `n = 10`: for a longer chain the conditions of its first ten
atoms are among its conditions.  For `n = 10`, `ℙ(L) ≅ ℙ⁴`.
*A structural point at infinity.*  Let `u_1, …, u_9 ∈ ℝ⁶` be the stacked bond vectors,
`a ⊥ u_1, …, u_5` and `b ⊥ u_5, …, u_9`.  Every constrained edge vector lies in `a^⊥ ∪ b^⊥`
(the 1–3 vectors `u_i + u_{i+1}` with `i ≤ 4` in the first hyperplane, those with `i ≥ 5` in
the second), so `S = abᵀ + baᵀ ∈ L` with `c = 0`, and `rank S = 2`.  At a matrix of rank at
most 2 every `4 × 4` minor vanishes to second order (the adjugate of a `4 × 4` matrix of
rank at most 2 is zero), so the ideal of `V` lies in the square of the maximal ideal of
`[S]` in `ℙ⁴`: the local length of `V` at `[S]` is at least `1 + 4 = 5`.  Hence, whenever
`V` is finite, `length V ≥ 1 + 1 + 5 = 7`, with equality iff `V = {[E_1], [E_2], [S]}`,
`E_1, E_2` reduced.
*The witness.*  `experiments/geometry/exact_nonlinear_threshold.py 10 0 0`: for one pair of
chains with rational torsion half-angle tangents, a Gröbner basis over `ℚ` (Singular) gives
`dim V = 0` and `deg V = 7` (the same over `𝔽_32003` for four pairs).
*Genericity.*  Over the Zariski-open set of parameters where `dim L = 5` and `a, b` are
defined, the schemes `V` form a closed subscheme of a `ℙ⁴`-bundle, proper over the base.
Fibre dimension is upper semicontinuous, so the fibres are finite near the witness; there
the projection is finite and the fibre length is upper semicontinuous, so it is at most 7
near the witness, and at least 7 by the structural point.  Hence on a non-empty Zariski-open
set `V = {[E_1], [E_2], [S]}`, and the only points with `c ≠ 0` are the block projectors.
Theorem B′ (⇐) concludes.  ∎

For `n = 11, 12` two hyperplanes cannot contain the ten or eleven stacked bond vectors, and
the same script finds `deg V = 2`: the two block projectors, reduced, and nothing else.

**What happens below [N].**
* `n = 9`: `V` is finite in the affine chart (48 complex points for the referee's witnesses);
  a few further real, positive semidefinite points exist (further chains that are linear
  images of `z`) — 4 to 6 in our six instances at 111°, between 2 and 10 in the referee's
  nine instances at 97° — but in all instances computed no mixture representing the identity
  puts mass on them (linear program, `explore_below.py 9`): the ensemble is still
  identifiable.
* `n = 7, 8`: `𝒫(z)` has dimension `18 − 2n` (a surface for `n = 8`, four-dimensional for
  `n = 7`), its convex hull has the identity in its interior, and **the ensemble is not
  identifiable**: in all six instances computed a
  mixture of 9 (`n = 8`) or 11 (`n = 7`) chains, none of them one of the two states,
  reproduces every averaged squared distance to `10⁻¹⁴` with bond lengths correct to
  `10⁻¹⁵` (`explore_below.py 7 8`; reproduced by the referee with independent code).  By
  Theorem H the same ensemble is *locally* the only two-state ensemble with its data; whether
  it is the only two-state ensemble globally is not proved (the referee's direct search over
  two-state ensembles at `n = 7, 8, 9` found no other [N]).  So the number of states is a
  prior that restores at least local identifiability.

So for two states three notions separate: locally identifiable among two-state ensembles
(`n ≥ 7`), identifiable among all ensembles (`n ≥ 10`, and 9 in the instances computed),
certifiable by the linear system of §6 (`n ≥ 12`).

For `K ≥ 3` the scheme at infinity is positive-dimensional at the conjectured threshold
(two hyperplanes spanned by `3K − 1` consecutive stacked bonds cover up to `6K − 3` bonds,
more than the `⌊9K/2⌋` present), and we have only numerical evidence: for `K = 3` a
one-parameter family of further chains at `n = 13` and none at `n = 14, 15`
(`explore_misc.py k3`).

### 5.6 Laws instead of means (with the Ensemble Identifiability Division's Theorem E5)

The Ensemble division proves (its report, Theorem E5 and Corollary E6; unrefereed; we
re-derived the proof): if the algebraic matroid of a polynomial feature map is connected and
no feature is constant, a generic finite ensemble — any number of states — is determined,
among all Borel probability measures, by the one-dimensional **laws** of the features, up to
the fibres of the feature map; if the matroid is not connected there are *chimeras*.  The
proof uses only that images of irreducible varieties are irreducible and that the Jacobian
of a splice is block diagonal, so it applies to the chain variety, which is parametrised
rationally by the half-angle tangents of the torsions; the matroid is then that of the
squared distances as functions of the torsions (for generic bond data: the contraction of
the rigidity matroid by the constrained edges).

**Theorem J [P, given E5/E6 of the Ensemble division].**  Chains with fixed bond lengths and
non-degenerate bond angles, `n ≥ 5`.
(a) The matroid of the squared distances of sequence separations 3 and 4 is connected, and
these distances determine a generic chain up to congruence.  Hence a generic finite
ensemble of chains, with any number of states and any weights, is determined modulo
congruence, among all ensembles of chains, by the laws of the distances `d_{i,i+3}` and
`d_{i,i+4}`.
(b) For a single separation `s ≥ 3` the squared distances `d_{i,i+s}` are algebraically
independent functions of the torsions: the matroid is free, and no ensemble with two or
more generic states is determined by the laws of these distances — for `s = 3` because every
splice of two states is again a chain (the signs of the torsions are free as well); for
`s ≥ 4` already because one separation does not determine a single generic chain up to
congruence (whether *real* chimeras exist for `s ≥ 4` depends on the image of the real chain
variety, which is not a product, and is not claimed).

*Proof.*  (a) `d²_{i,i+3} = A_i − B_i cos θ_i` with `B_i ≠ 0`: the `n − 3` features `b_i = (i, i+3)`
form a basis.  `e_i = (i, i+4)` depends on `θ_i` and `θ_{i+1}` only, and on each of them (the
torsion `θ_i` moves atom `i` alone relative to the others, and atom `i + 4` is off its axis
for generic `θ_{i+1}`; symmetrically for `θ_{i+1}`); so `B − b_i + e_i` and `B − b_{i+1} + e_i` are
bases (triangular Jacobians) and the fundamental circuit of `e_i` is `{e_i, b_i, b_{i+1}}`.  The
fundamental graph is the path `b_1 − e_1 − b_2 − ⋯ − b_{n−3}`, connected; a matroid whose
fundamental graph with respect to one basis is connected is connected.  Injectivity:
`d_{i,i+3}` gives `|θ_i|` and `d_{i,i+4}` the relative sign of `θ_i` and `θ_{i+1}`.
(b) `d²_{i,i+s}` depends on the torsions `θ_i, …, θ_{i+s−3}` and, generically, on `θ_i`; the
Jacobian of the `n − s` features with respect to `θ_1, …, θ_{n−s}` is triangular with non-zero
diagonal.  For `s = 3` the image of the chain variety is the product of the intervals
`[A_i − |B_i|, A_i + |B_i|]`, so splices are realised (E5(b)); for `s ≥ 4` the `n − s`
distances cannot determine the `n − 3` torsions.  ∎

`experiments/geometry/matroid_connectivity.py` decides connectivity for other patterns by an
exact computation (the matroid of a rational witness modulo a prime is a weak image of the
generic one, so "connected of full rank" and "free" at the witness are proofs): at `n = 12`
every pair of separations among `3, …, 7` that we tried is connected, as are all pairs,
`n` or more random pairs, and "separation 3 plus the end-to-end distance"; single
separations, the distances from one end, and `n − 3` random pairs are free.

**Means against laws.**  For averaged squared distances the necessary sequence separation
grows with the number of states (`K + 3`, Theorem H); for the laws of the distances
separation 4 suffices for every `K`.  The price of a mean is exactly the dependence on `K`.

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

Moreover the certificate is sound for every realizable input [P; the referee's observation,
GEOMETRY-REV-0001 m10]: if `M = M(ν)` for *some* ensemble `ν` on `𝒞`, `rank G = dK`, and the
solution space of step 2 has dimension `K − 1`, then `ν` is a `K`-mixture satisfying (CC) and
DEMIX returns it.  (Step 1 refuses inputs whose stacked configuration does not have rank
`dK`, e.g. mixtures of ideal helices — §12.)

*Proof.*  `G` is the Gram matrix of the centred stacked configuration, so `Z = z_c Q₀` for some
`Q₀ ∈ O(dK)`, and `𝒩(Z) = Q₀ᵀ 𝒩(z) Q₀ = Q₀ᵀ 𝒯 Q₀`.  A generic element is
`T = Q₀ᵀ(Σ s_k E_k)Q₀` with distinct `s_k`, whose eigenspaces are the images of the blocks; so
`Z Q_k = √w_k X_k R_k` with `R_k ∈ O(d)`, and (2.1) gives the weights.
Soundness.  By Lemma 2.2 (with `Z` in the place of `z`) the identity is the barycentre of a
probability measure on the compact set `𝒫(Z) ⊂ I + 𝒩(Z)`, an affine space of dimension `K − 1`;
by Carathéodory `I = Σ_{j=1}^{m} v_jP_j` with `m ≤ K`, `v_j > 0`, `P_j ∈ 𝒫(Z)`.  Each `P_j` has
rank at most `d` and the sum has rank `dK`, so `m = K`, the ranks are `d` and the ranges are
independent.  A vector orthogonal to the ranges of `P_j`, `j ≠ 1`, satisfies `u = v_1P_1u`; such
vectors form a space of dimension `d` inside the range of `P_1`, hence equal to it: the
ranges are mutually orthogonal and `v_jP_j` are the orthogonal projections onto them.  So `Z`
is, up to a rotation, the stacked configuration of the `K`-mixture with states
`Y_j = ZA_jᵀ` (`A_jᵀA_j = P_j`) and weights `v_j`, whose trivial quadrics already fill the
`(K − 1)`-dimensional space `𝒩(Z)`: it satisfies (CC), and Theorem B identifies `ν` with it.  ∎

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

*Instances with incomplete data* **[N; the referee's semidefinite programme,
`experiments/geometry/review1/k_stress.py`]**.  The first versions of this report had no
instance of Theorem F with incomplete data.  For two generic states with `n = 14` and `16`
atoms such a stress exists when `F` is the band `3 ≤ |i − j| ≤ 7` or `≤ 8` (smallest non-zero
eigenvalue `3·10⁻⁴` to `5·10⁻²`, kernel exactly `span(𝟙, z)`), and for 45 or 55 random pairs
out of the 66 unconstrained ones at `n = 14`; it does not exist for the bands `≤ 5` and
`≤ 6` — in agreement with §5.4: no stress at all is supported within separation `dK = 6`.
So for sequence-local data Theorem F starts exactly where Theorem F′ does; its use is for
*scattered* measured pairs.

### 7.2 Complete data: a global stability theorem

Let `d_P(X, Y) = min_g ‖X − gY‖_F` (minimum over isometries; `√n ·` RMSD after optimal
superposition) and let `W₂` be the 2-Wasserstein distance between shape distributions with
respect to `d_P`.

**Theorem G (global quantitative rigidity of ensembles) [P].**  Let `μ = Σ w_k δ_{X_k}` satisfy
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
`D(X) − D(X_k) = L_k(Δ) + D(Δ)` with `L_k` linear and `‖D(Δ)‖_F ≤ 2n‖Δ‖²`; and
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

**Theorem G′ (the same conclusions without the conic condition) [P; for two states P, exact].**
The proof of Theorem G uses (CC) in three places only, and each can be replaced by a weaker
hypothesis on the mixture `μ` with stacked configuration `z` spanning `ℝ^{dK}`, `n − 1 > dK`:

  (H)  `𝒫(z) = {E_k/w_k}` — the only chains that are linear images of `z` are the states
       (this is (a));
  (H′) `𝒩(z) ∩ T_k = {0}` for every `k`, where `T_k` is the space of symmetric matrices whose
       blocks `(l, l')` with `l, l' ≠ k` vanish — the states are *reduced* points of the
       rank-`d` locus of `I + 𝒩(z)` (this gives (b): the symmetric part of `Π_kᵀB` lies in
       `𝒩(z) ∩ T_k`);
  (J)  the Jacobian of the `K`-state parametrisation is injective modulo isometries (this is
       the bracketed step of (d)).

Under (H), (H′), (J) all of Theorem G(a)–(e) holds with the same certificate `φ`.  (CC)
implies the three ((H) by Theorem B; `𝒯 ∩ T_k = 0`; (J) by the bracketed argument).  **For two
states and generic chains with `n ≥ 10` atoms the three hold without (CC):** (H) is
Theorem I; (H′) is the reducedness of the two points established in its proof (the rank-3
locus is smooth at a point of rank exactly 3, so the tangent space of the scheme there is
`𝒩(z) ∩ T_k`); (J) is Theorem H(a).  So the global bound `W₂² ≤ C‖ΔM‖` holds from 10 atoms
on, two atoms before the linear certificate exists.  (For `n = 9` we do not know; for
`n ≤ 8` there is no identifiability to stabilise.)

The certificate `φ` is linear in the data: `∫ φ dν` is computed from `M(ν)` alone, it vanishes
for `μ`, and it bounds the mean squared distance of `ν` from the `K` states.  It is the
ensemble analogue of the energy of a positive semidefinite stress.  `κ` is defined by a global
infimum; its local value at `X_k` — the smallest eigenvalue of `Π^⊥` on the flex space of
`X_k` — is a linear-algebra quantity, a certified global lower bound is a global optimisation
over `𝒞` (not attempted; `PROOF_OBLIGATIONS.md`, O-5).  **The local value is not an estimate of
`κ`** [N; the referee's computation, `review1/d_certificate.py`]: in six two-state instances
with 12 to 18 atoms the smallest ratio `φ/min_k d_P²` found by global search is attained at a
chain *far* from both states (a near-affine image of the stack) and is 2 to 12 times smaller
than the smaller local value (e.g. `0.0023` against `0.028` at `n = 14`); the constant
`√(n − 1 − 3K)/(2κ)` of (c) is then between 47 and 570 in these instances.  Until `κ` has a
certified lower bound, (c) and (d) are qualitative statements.  The smoothness of `𝒞` near the
states is used in (d) only; (a)–(c) hold without it (referee's remark).

---

## 8. Realizability of averaged data, and second-moment rigidity

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

### 8.2 Second-moment rigidity

*Terminology.*  The Ensemble Identifiability Division calls a graph *ensemble rigid* when
generic finite ensembles of its frameworks are determined by the **laws** of the edge lengths,
and proves that this is generic global rigidity (its Theorem E7).  The notion below asks for
more — determination by the **means** of the squared lengths, on a conformation space with
statewise constraints — and we call it *second-moment rigidity* (our first checkpoint said
"ensemble rigidity"; renamed to avoid the clash, GEOMETRY-RES-0001).

Let `F` be a set of pairs.  A conformation `X ∈ 𝒞` is **`F`-second-moment rigid** if `δ_X` is
identifiable from the averaged squared distances on `F`: no ensemble of conformations other
than copies of `X` reproduces `D(X)` on `F`.  Recall that the bar framework `(F ∪ E₀, X)` is
*globally rigid* if every configuration in `ℝ^d` with the same lengths on `F ∪ E₀` is
congruent to `X`, and *universally rigid* if this holds in every dimension.

**Theorem E (a hierarchy) [P; for finite mixtures the reduction step of (a) and the first
half of (b) are V: `MetricChain.Geometry.secondMomentRigid_of_universal`,
`MetricChain.Geometry.globallyRigid_of_secondMomentRigid`].**
Let `X ∈ 𝒞` span `ℝ^d` affinely.
(a) If `(F ∪ E₀, X)` is universally rigid and `𝒩(X) = 0`, then `X` is `F`-second-moment rigid.
(b) If `X` is `F`-second-moment rigid, then `(F ∪ E₀, X)` is globally rigid and `𝒩(X) = 0`.
(c) If `𝒦 = 𝒮` (Theorem D(a): e.g. chains with `n ≤ 6`), then `X` is `F`-second-moment rigid iff
`(F ∪ E₀, X)` is universally rigid and `𝒩(X) = 0`.
(d) The converse of (b) fails: there are globally rigid chains with `𝒩(X) = 0` that are not
`F`-second-moment rigid.

*Proof.*  (a) The Hilbert configuration of a competing `ν` has the lengths of `X` on
`F ∪ E₀`, so it is congruent to `X`, `M(ν) = D(X)`, and Theorem A applies.  (b) A configuration
with the same lengths is a one-state ensemble; and if `0 ≠ S ∈ 𝒩(X)`, the mixture of the two
affine images `X_±` of Theorem A has the same averaged data on all pairs.  (c) If `X` is
`F`-second-moment rigid and `y` is a Hilbert-space configuration with the lengths of `X` on
`F ∪ E₀`, then `D(y) ∈ 𝒮 = 𝒦` is the averaged data of an ensemble of conformations, which
agrees with `X` on `F`; so that ensemble is `δ_{[X]}` and `D(y) = D(X)`.  (d) By (c), for chains with six atoms (bond lengths and angles are those of `X`; `|E₀| = 9`)
it suffices to find `X` with `𝒩(X) = 0` such that `(F ∪ E₀, X)` is globally rigid and not
universally rigid.  Take `F = {14, 25, 36, 16}`, 13 bars in all.  For the rational
configuration

    X⁰ = (0,0,0), (1,0,0), (1,2,0), (3,1,2), (2,−1,3), (4,2,1)

exact arithmetic gives **[P, exact: `experiments/geometry/exact_hierarchy_witness.py`]**:
the rigidity matrix has rank 12, so the equilibrium stress is unique up to scale; its stress
matrix has rank `2 = n − 4` and is indefinite (diagonal entries `−2` and `55/8`; sum of the
principal `2 × 2` minors `−5761/128`); the nine `E₀`-edge vectors lie on no conic.  These are
open conditions, so they hold for every configuration `X` near `X⁰`, in particular for one
with algebraically independent coordinates.  For such a generic `X`: a stress matrix of rank
`n − d − 1` implies global rigidity (Connelly 2005); a generic universally rigid framework
has a positive semidefinite stress matrix of rank `n − d − 1` (Gortler–Thurston 2014), which
is impossible when the only stress is indefinite.  So `(F ∪ E₀, X)` is globally rigid, not
universally rigid, `𝒩(X) = 0`, and by (c) `X` is not `F`-second-moment rigid.  ∎

(The first versions of this proof asserted the existence of such a generic framework and
gave only a floating-point instance with unit bonds, which is not generic, so that the cited
theorems did not apply to it; the gap was found, and the exact witness supplied, by the
referee — GEOMETRY-REV-0001, M3.)  An explicit instance with unit bonds, `F` as above, and a
two-state ensemble of other chains with the same averaged data, computed to 12 digits, is in
`experiments/geometry/hierarchy_example.py` **[N]**; for a second such instance the referee
found numerically that the four measured-pair equations have exactly two solutions on the
torus of torsions, `X` and its mirror image.

**Second-moment rigidity is strictly weaker than universal rigidity [N; O-3].**  A sufficient
condition for `F`-second-moment rigidity that does not involve other dimensions: `X` is the
unique maximiser over `𝒞` (conformations in `ℝ^d`) of `H_c = Σ_{ij ∈ F} c_ij |x_i − x_j|²` for
some couplings `c` — then `D(X)|_F` is an exposed point of the realizable set, and any ensemble
with the averaged data of `X` on `F` has mean `H_c` equal to the maximum.  Universal rigidity
asks for a maximiser in every dimension (a positive semidefinite stress).  For a 7-atom chain
with five measured pairs the stress `ω` of `(F ∪ E₀, X)` is unique up to scale, `X` is critical
for `c = ±ω|_F`, and the constrained Hessian on the four flexes is `±2 tr(VᵀΩV)`: `X` is a
strict local maximiser in `ℝ³` whenever this form is definite on the flexes, also when `Ω` is
indefinite on `ℝ⁷`.  A search over 15 000 random instances
(`experiments/geometry/explore_er3.py`) finds such strict local maximisers with indefinite
stress in about 2 % of them, and about one in fifteen of these is a global maximiser.
Instance A of `er_not_ur_instance.py` (torsions `1.5174, −1.0463, 2.7120, −1.6744`;
`F = {15, 16, 25, 27, 37}`): stress eigenvalues `−1, −0.523, +0.071` (normalised), flex
Hessian negative definite, `H_c(X) = 1.17018` against at most `1.16769` on a grid of `24⁴`
points and `1.15499` for the best other local maximum in 2 000 searches, and a framework in
`ℝ⁴` with the lengths of `X` on `F ∪ E₀` to `10⁻¹⁵` and singular values
`2.89, 1.61, 0.85, 0.15`.  So, numerically, `X` is second-moment rigid on `F` and not
universally rigid.  What is missing for a theorem is a certified global maximum on the
4-torus (margin `0.015`, smallest curvature `0.006`): requested in GEOMETRY-REQ-0006.

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

*Relation to the Ensemble Identifiability Division's first checkpoint* (branch
`research/ensemble-identifiability`, commit `a570520`, 2026-11-26 16:48 UTC — six minutes
before our first commit (16:54 UTC); read by us at 17:19 UTC, after our second).
* Its Theorem E1 (an ensemble is determined by means of observables iff its support is the
  ground-state set of an energy in their span, with affinely independent features) is the
  general principle of which our Corollary 4.2 and Theorem G(a) are instances; our
  certificate `φ(X) = ‖Π^⊥X‖²` is the chain counterpart of its `‖P^⊥x‖²` for pair
  correlations on the cube (its Theorem E10).  The two were found independently on the same
  afternoon; the priority of the general statement is theirs.
* Its Corollary E1.3 — mean squared edge lengths determine no ensemble of frameworks, by a
  random rescaling — is Proposition 3.1 with another construction, on the **unconstrained**
  configuration space.  Theorems A, B and I are the statement that the conclusion reverses
  as soon as every state obeys statewise constraints: on a chain variety the mean squared
  distances do determine generic single conformations (`n ≥ 5`) and generic mixtures.
* Its Theorem E7 (determination by the *laws* of the edge lengths = generic global rigidity)
  and our Theorem E fit together: laws ⇔ global rigidity; means ⇒ global rigidity together
  with the conic condition `𝒩(X) = 0`, and means ⇐ universal rigidity together with
  `𝒩(X) = 0`.  The converse of the first fails on chains [P, exact witness: Theorem E(d)];
  that of the second fails numerically [N: instance A].  (Earlier versions of this paragraph,
  of the Summary and of the register said "universal ⇒ second-moment ⇒ global" without the
  conic condition; that is false — GEOMETRY-REV-0001, M1; `DEAD_ENDS.md` DG-13.)

*Not found in print (searches of 2026-11-26; an absence in searches is not a proof of
novelty).*  Theorem B and B′ (identifiability of a mixture among all ensembles from averaged
squared distances via the trivial-quadric condition); the thresholds of Theorem C; the
algorithm DEMIX; Theorem G (global `W₂` stability with the explicit certificate); Theorem F for
`K ≥ 2`; second-moment rigidity as a notion, and Theorem E (its place between global and
universal rigidity once the conic condition is added to both);
Theorem D for chains with bond angles and the exact rank-4 witness; Theorem H (range `K + 3`); Theorem I and the separation of the three thresholds for two states.

**Corollary 9.1 (a consequence for reconstruction with unknown orientations) [P, given K].**
Observe `y = g·X_κ + σξ`: a conformation drawn from `μ`, rotated by a Haar-random `g ∈ O(3)`
(or `SO(3)`), labelled atoms, Gaussian noise.  Then `E[y_i y_jᵀ] = ⅓⟨⟨x_i, x_j⟩⟩_μ I₃ + σ²δ_ij I₃`:
the second moment of the data determines exactly `M(μ)` (for centred conformations), and
nothing else.  Hence under (CC) the distribution of shapes — conformations modulo rotations
*and reflections* — is a function of the second moment, whereas without statewise
constraints no mixture with `K ≥ 2` is (Proposition 3.1).  The second moment is blind to an
independent reflection of each state, so what it can determine depends on the group:
* *rotations and reflections, `O(3)`:* the estimand is the shape distribution; without
  constraints moments of order at least 4 are needed (the third moment vanishes), with
  (CC) order 2 suffices;
* *proper rotations, `SO(3)`:* the estimand of Proposition 9.2 is `μ` up to a proper
  rotation of each state.  Order 2 with (CC) gives it up to a reflection of each state — `2^K`
  assignments of handedness remain — and the third moment is still needed for those; only
  for the reflection-blind estimand do the constraints lower the order from 3 to 2.
In the framework of Bandeira, Blum-Smith, Kileel, Perry, Weed and Wein the number of samples
needed at noise level `σ → ∞` grows like `σ^{2q}` with `q` the smallest moment order that
determines the orbit of the signal; their `q` is defined for a group orbit, so the statements
above are about `q` for the estimands named.  We did not re-derive the sample-complexity
theorem; the statement is conditional on it (hypotheses as listed by the Ensemble division,
ENSEMBLE-RES-0001 §5: additive Gaussian noise, uniformly random group elements, fixed
dimension, the high-noise limit, generic signals).  (An earlier version said "the constraints
lower the order from `q = 3` to `q = 2`" without naming group or estimand; GEOMETRY-REV-0001,
M4.)

**Proposition 9.2 (without constraints the third moment is needed, and suffices) [P].**  In
the same model with proper rotations and **no** statewise constraints, let `μ = Σ w_k δ_{X_k}`
be a mixture of labelled configurations (anchored at a common origin) whose stacked points
span `ℝ^{3K}`.  The second moment determines `M(μ)` only (Proposition 3.1: a family of
mixtures of dimension `9K(K−1)/2 + K − 1`).  The third moment,
`E[y_i ⊗ y_j ⊗ y_l] = (τ_ijl/6)·ε` with `τ_ijl = Σ_k w_k det(x_i^{(k)}, x_j^{(k)}, x_l^{(k)})` and `ε`
the alternating tensor, determines in addition the alternating 3-form
`T = Σ_k w_k^{-1/2} vol_k` on the stacked space (`vol_k` the volume form of block `k`), and
`{v : rank(i_v T) ≤ 2}` is the union of the coordinate blocks.  Hence second and third
moments together determine `μ` up to a proper rotation of each state.  (For rotations *and*
reflections the third moment vanishes and order four is needed.)

*Proof.*  The only `SO(3)`-invariant 3-tensors are multiples of `ε`, and contracting with `ε`
gives the determinant; Gaussian noise contributes terms with a factor `E[g x] = 0`.
`det(x_i^{(k)}, x_j^{(k)}, x_l^{(k)}) = w_k^{-3/2} vol_k(z_i, z_j, z_l)`, so `τ_ijl = T(z_i, z_j, z_l)`, and a
3-form is determined by its values on a spanning set.  For `v = Σ_k v_k` with `v_k` in block
`k`, `i_v T = Σ_k w_k^{-1/2} i_{v_k} vol_k` is a sum of 2-forms of rank 2 with supports in
different blocks, so its rank is twice the number of non-zero `v_k`.  The blocks give the
states, `T` restricted to a block gives `w_k^{-1/2}` and the orientation.  ∎

`experiments/geometry/third_moment.py`: for `K = 2, 3` the linear system for `T` has full rank
(20, 84) and the contraction ranks are `2` on block vectors, `4` on two-block vectors and
`4` respectively `6` on generic vectors.

---

## 10. Machine-checked statements

`proofs/Geometry/EnsembleRigidity.lean` (Lean 4.31, Mathlib v4.31.0; zero warnings; axioms
`propext`, `Classical.choice`, `Quot.sound` only; imported by `proofs/AxiomAudit.lean`, which
now walks 5110 declarations).

| declaration (namespace `MetricChain.Geometry`) | statement | used in |
|---|---|---|
| `stacked_sqdist` | `‖z_i − z_j‖² = Σ_k w_k ‖x_i^{(k)} − x_j^{(k)}‖²` for the stacked configuration in the `ℓ²` product | Lemma 2.1 |
| `stress_energy_eq`, `mixture_energy_eq` | for symmetric `Ω` with zero row sums, `yᵀΩy = −½ Σ Ω_ij (y_i − y_j)²`; the `Ω`-energy of a finite mixture is linear in its averaged squared distances | Theorems F, G |
| `stress_certificate` | `Ω ⪰ 0`, zero row sums, annihilating a reference mixture; a second finite mixture with the same averaged squared distances on the support of `Ω` has every coordinate of every state of positive weight in `ker Ω` | Theorem F (first half of the proof) |
| `block_coeff_nonneg`, `block_rigidity` | a linear map into a space of dimension `≤ d` whose squared norm is `c₁‖u‖² + c₂‖u'‖²` on two orthogonal blocks of dimension `d ≥ 1` has `c₁ = 0` or `c₂ = 0` (and `c_k ≥ 0`) | Theorems B, F, G ("one block only") |
| `exists_linearMap_of_gram_eq`, `state_is_linear_image` | families with equal Gram matrices are related by a linear inner-product-preserving map; every state of positive weight of a finite mixture with the averaged squared distances of a spanning configuration `z` is a linear image of `z` | Lemma 2.2 (finite mixtures) |
| `finite_mixture_identifiable` | Theorem B against finite competing mixtures, end to end, with abstract orthogonal blocks: every state of positive weight lives on one block | Theorem B |
| `mixture_identifiable_stacked` | Theorem B in coordinates: states `X_k`, weights `w_k`, stacked configuration in the `ℓ²` product; every state of positive weight of a competing finite mixture has the distance matrix of some `X_{k₀}` | Theorem B |
| `line_mixture_example` (`line_conic`, `line_span`, `line_states_differ`) | all hypotheses of `mixture_identifiable_stacked` hold for two different states (straight and folded three-point unit chains on the line), and the theorem applies | non-vacuity, two states |
| `conic_condition_line` | the conic hypothesis is satisfiable (one block, the line) | non-vacuity |
| `mixture_state_of_conic` | under the conic condition (every symmetric bilinear form vanishing on the edge vectors is block-scalar) a linear map into dimension `≤ d` that preserves the edge lengths is a scaled isometry on one block and zero on the others | Theorem B, from Lemma 2.2 on |
| `sqdist_midpoint_of_conic` | affine flexes: maps `A_±` preserving edge lengths with the midpoint identity | Theorem A (iii)⇒(ii), Theorem E(b) |
| `globallyRigid_of_secondMomentRigid` | second-moment rigidity (finite mixtures) implies global rigidity on `F ∪ E₀` | Theorem E(b) |
| `secondMomentRigid_of_universal` | universal rigidity of `(F ∪ E₀, x)` reduces `F`-second-moment rigidity to second-moment rigidity for complete averaged data (the hypothesis `SecondMomentRigid E₀ univ x` is the conic condition and cannot be dropped) | Theorem E(a) |
| `universal_not_secondMomentRigid` | three points `(1, 0, i)` in the plane, constraints the path, measured pair the ends: universally rigid on `F ∪ E₀` and **not** `F`-second-moment rigid — the hypothesis above is necessary (the referee's counterexample, GEOMETRY-REV-0001 M1) | Theorem E(a), sharpness |
| `fourAtom_virtual_value_witness`, `block_rigidity_nonvacuous` | two elementary identities (a number between `a` and `b` is a convex combination of them; `‖u‖² = 1·‖u‖² + 0·‖u'‖²`); they illustrate Example 3.3 and the conclusion of `block_rigidity` but do not instantiate the hypotheses of a theorem — the instance that does is `line_mixture_example` | Example 3.3 |

Not machine-checked: the measure-theoretic (`L²`) version of Lemma 2.2 and hence Theorem B
against arbitrary ensembles; the weights of the competing mixture in Theorem B; Theorem B′; everything about genericity and thresholds (Theorems C,
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
python3 experiments/geometry/exact_nonlinear_threshold.py 10 0 0   # Theorem I (needs Singular; 80 s over Q)
python3 experiments/geometry/explore_below.py 7 8 9  # two states below the threshold [N]
python3 experiments/geometry/demix.py                # algorithm DEMIX on synthetic ensembles
python3 experiments/geometry/exact_hierarchy_witness.py   # Theorem E(d), exact witness
python3 experiments/geometry/exact_general_position.py 5  # hypothesis of Theorem F' (exact)
python3 experiments/geometry/exact_conic_rank.py 20 13 rational angles   # Theorem C(b), K = 13..20 (3 min)
python3 experiments/geometry/hierarchy_example.py    # Theorem E(d), numerical instance
python3 experiments/geometry/er_not_ur_instance.py A # second-moment rigid, not universally rigid [N; 3 minutes]
python3 experiments/geometry/matroid_connectivity.py 12   # Theorem J and the table of patterns (exact)
python3 experiments/geometry/mutation_checks.py      # the tests detect planted errors
```

## 12. Limitations

* Averaged *squared* distances are one specific linear observable.  Nothing here applies to
  averages of other functions of distance (inverse sixth powers, contact frequencies,
  scattering curves beyond their low-angle limit); for those the stacked configuration is not
  a Euclidean framework.  Where the observable is measured (low-angle scattering with pairs
  of labels) the datum is usually a block sum `⟨C, M⟩`, not single entries (Science division,
  SCI-RES-0029 §2).
* **The mechanism needs the statewise constraints to hold exactly and identically in all
  states.**  Nothing is proved for bond data known to finite accuracy or varying between
  states.
* **Finite mixtures only.**  (CC) needs `3K ≤ n − 1`; an ensemble with any continuous spread is
  outside every identifiability theorem of this report (Theorem G only bounds its distance
  to a mixture that satisfies (CC), and its exponent means that a symmetric broadening of a
  state by `ε` is invisible at order `ε`).
* Identifiability is for exact data.  The quantitative theorem (G) has a constant defined by
  a global infimum that we do not compute; numerically it is 2 to 12 times smaller than its
  local values (§7.2), so (c)–(d) are qualitative until it is certified.
* **Which conformations are excluded by "generic".**  Generic statements exclude a proper
  analytic subset that we do not describe completely.  Known members:
  (i) *planar* conformations (for one state `𝒩(X) ≠ 0`);
  (ii) *helices*: for `K ≥ 2` states of constant torsion the stacked configuration has rank
  `2K + 1`, not `3K` (the coordinates of the bond vectors of a helix are spanned by a
  constant and one harmonic), and `dim 𝒩(z) = 7` for two helices at every length checked
  (`n = 12, …, 40`): (CC), DEMIX and Theorem G never apply to mixtures of ideal helices
  (a single helix has `𝒩 = 0`; a helix plus a generic chain satisfies (CC); a two-helix
  mixture was still identifiable in the referee's computations — `review1/m_helix.py`);
  (iii) *states that share rigid segments*: two states that differ in a single torsion are
  never identified, at any length, and (CC) fails whenever two states differ in at most
  three torsions (Science division, SCI-RES-0029 §3: `dim 𝒩(z) ≥ 21 − 6s + s(s − 1)/2` for
  `s ≤ 4` shared segments).  These are the commonest two-state motions; the theorems of this
  report are about states that differ everywhere.
* The sharp threshold of Theorem C(b) is proved for `K ≤ 20` at one bond geometry and
  `K ≤ 12` at a second by exact computation; for all `K` it is a conjecture (a threshold twice
  as large is proved).  Identifiability among all ensembles below the conic threshold is
  proved for two states only (Theorem I, one bond geometry and generic ones); for three
  states it is numerical, beyond that a conjecture.  The non-identifiability at `n = 7, 8` and
  the identifiability at `n = 9` are numerical (six instances each by us; three and eighteen
  by the referee).
* Theorem H is local and within the `K`-state family; it says nothing about ensembles with a
  different number of states or far away, and its sufficiency part is an exact computation
  for `K ≤ 8` at two bond geometries.
* No noise model, no statistics, no algorithmic guarantee for DEMIX under perturbation.
* The parts of this text written after commit `e8e2582` (Theorem G′, the present form of
  Theorem C(c), the corrections made after the internal review) have been checked by their
  author only.
