# When are K spin configurations exactly the ground states of an Ising pair energy?

Working paper of the complexity division, 2026-11-26.  Written in answer to question **E-C1** of the
Ensemble Identifiability division (ENSEMBLE-MSG-0003 §4):

> "Deciding whether `K` given sign vectors are exactly the ground states of some Ising energy with
> independent pair features is a linear programme with exponentially many constraints whose separation
> problem is a ground-state problem.  Is the decision problem co-NP-hard for `K ≥ 4`?  (For `K ≤ 3` the
> answer is always yes.)"

Register: `THEOREMS.md` CX-T16–CX-T19.  **Unreviewed.**  Labels: [P] paper proof, [X] exact finite
computation with certificates verified in rational arithmetic, [K] known, cited.

## 0. Answer

* **For every fixed `K` the problem is solvable in linear time** (Theorem 2): whether the configurations
  are exposed depends only on the *set of column types* — which of the `2^{K−1}` possible patterns
  `±(x^1_i,…,x^K_i)` occur among the sites — not on how many sites carry each pattern.  So for fixed `K` the
  problem is a finite table and is not co-NP-hard unless P = NP.
* `K = 4` (Theorem 3, [X + P]): four configurations are exposed **unless their site-wise product is
  constant** (and they are not all the states of their three merged sites).  `K = 5`: the complete table
  (130 non-degenerate orbits of type sets, 6 of them not exposed; §4).
* For `K` part of the input the problem is in co-NP (Theorem 1).  **Whether it is co-NP-hard we do not
  know.**  §5 gives the structure we found: an exact criterion in `K` dimensions (Theorem 6), a
  polynomial-time sufficient condition (Corollary 7), two families of obstructions (Lemmas 8, 9), and a
  class of instances with enough symmetry for which the answer is "no other sign vector in the span"
  (Proposition 10) — for sets of characters of `F_2^r` this is "the frequency set is a Sidon set".
* Prior art: the object is the face lattice of the cut polytope; that any three vertices form a face and
  that four need not is classical, and the `K = 4` rule is very probably in the literature on simplicial
  faces of the cut cone (§7).  We claim no novelty for §§2–4 beyond answering the complexity question.

## 1. Setting

Sites `1,…,n`.  A *state* is `x ∈ {+1,−1}^n`; `x` and `−x` are identified.  For a real symmetric matrix
`J` with zero diagonal, `E_J(x) = Σ_{i<j} J_ij x_i x_j` (all pairs may be coupled; no fields).  A set
`V = {x^1,…,x^K}` of pairwise different states is **exposed** if for some `J` the minimum of `E_J` over all
states is attained exactly on `V`.

Write `P(x) = (x_i x_j)_{i<j} ∈ ℝ^{C(n,2)}`, so that `E_J(x) = ⟨J, P(x)⟩`.  The polytope
`conv{P(x)}` is the cut polytope in `±1` coordinates; `V` is exposed iff `P(V)` is the vertex set of one
of its faces.  `V^c` denotes the states not in `V`.

## 2. A criterion, and membership in co-NP

**Theorem 1 [P].**  `V` is exposed iff `aff P(V) ∩ conv P(V^c) = ∅`.  Hence "`V` is not exposed" has a
certificate of polynomial size — at most `C(n,2) + 1` states `y_j ∉ V` with rational weights `μ_j > 0`,
`Σμ_j = 1`, and rationals `α_k`, `Σα_k = 1`, with `Σ_j μ_j P(y_j) = Σ_k α_k P(x^k)` — and the problem
"is `V` exposed?" is in co-NP, for `K` part of the input.

*Proof.*  `V` is exposed iff the system `⟨J,P(x^k)⟩ − E_0 = 0` (`k ≤ K`), `⟨J,P(y)⟩ − E_0 ≥ 1` (`y ∈ V^c`) in
the unknowns `(J, E_0)` is solvable.  By Farkas' lemma it is unsolvable iff there are reals `α_k` and
`μ_y ≥ 0`, not all `μ_y` zero, with `Σ_k α_k P(x^k) + Σ_y μ_y P(y) = 0` and `Σ_k α_k + Σ_y μ_y = 0`; divide
by `Σμ_y` and change the sign of `α`.  A basic solution has at most `C(n,2) + 1` non-zero `μ_y` and
entries of polynomial bit length.  ∎

## 3. Only the set of column types matters

Sites `i`, `j` are **twins** if `x^k_i = x^k_j` for all `k`, or `x^k_i = −x^k_j` for all `k`.  The *type* of a
site is its column `(x^1_i,…,x^K_i)` up to sign; twins are the sites of equal type.

**Theorem 2 (twin reduction) [P].**  Let `T` contain one site of every type.  Then the restrictions
`x^k|_T` are pairwise different, and `V` is exposed iff `V|_T = {x^k|_T}` is exposed (as a set of states
of the sites `T`).

*Proof.*  Replacing `x_j` by `−x_j` in all states (and `J_ij` by `−J_ij`) changes nothing, so we may assume
that twins have equal columns.  If `x^k|_T = ± x^l|_T` then `x^k = ± x^l`.  Let `t(i) ∈ T` be the
representative of `i`, and for a state `y` of `T` let `ŷ_i = y_{t(i)}` be its lift.
*If `V` is exposed by `J`:* `E'(y) := E_J(ŷ) = Σ_{s<s'} (Σ_{t(i)=s, t(j)=s'} J_ij) y_s y_{s'} + const` is a pair
energy on `T`; its minimum over states of `T` is attained exactly at the `y` with `ŷ ∈ V`, i.e. on `V|_T`.
*If `V|_T` is exposed by `J'`:* let `E(x) = E_{J'}(x|_T) − c·Σ_{i<j twins} x_i x_j` with any `c > 0`.
States in which all twins agree are the lifts, with energy `E_{J'}(y) − c·N_tw` (`N_tw` the number of twin
pairs), minimal exactly on the lifts of `V|_T`, which are the `x^k`; a state in which some twins disagree
has energy at least `min E_{J'} − c·N_tw + 2c`.  ∎

**Corollary [P].**  For fixed `K` there are at most `2^{K−1}` types, so "is `V` exposed?" is a function of
the set of types present — a table with at most `2^{2^{K−1}}` entries — and is decided in time `O(nK)`
plus a table look-up.  In particular, for no fixed `K` is the problem NP-hard or co-NP-hard unless
P = NP.  The table is invariant under permuting the `K` states and negating single states.

(The table itself is computed by finitely many linear programmes with up to `2^{2^{K−1}−1}` constraints;
its size is doubly exponential in `K`.  This does not help when `K` grows.)

## 4. The tables for `K = 4` and `K = 5`

`experiments/complexity/ising_faces/faces.py` decides a type set exactly: a floating-point linear
programme proposes either a matrix `J` or a pair `(μ, α)` as in Theorem 1, and the proposal is rationalised
and **verified in exact arithmetic** (for `J`: all states enumerated).

**Theorem 3 (`K = 4`) [X for "exposed", P for "not exposed"].**  Let `x^1,…,x^4` be pairwise different
states.  They are exposed, except when the site-wise product `x^1∘x^2∘x^3∘x^4` is constant **and** four
different column types occur.  (If the product is constant and at most three types occur, the four states
are all the states of the three merged sites.)

*Proof.*  By Theorem 2 there are 255 non-empty sets of types (`x^1` normalised to all `+`).  `table_k4.py`
decides each: 96 are degenerate (two of the states coincide), 157 exposed, and 2 not exposed — the sets
`{abc = +1}` and `{abc = −1}` of all four types with constant product.  (The 255 sets form 15 orbits under
the symmetry group of order 192; every set was also decided directly.)  The two negative cases also follow
from Lemma 8.  ∎

**`K = 5` [X].**  `table_k5.py`: 150 orbits of non-empty type sets under the symmetry group of order 1920,
130 of them non-degenerate; exposed in all but **6 orbits** (746 of the 61 719 non-degenerate type sets).
Five of the six contain four states with constant product (Lemma 8).  The sixth has five types and no such
four states:

```
x^1 = + + + + +      x^2 = + + − − −      x^3 = + − + + −      x^4 = + − + − +      x^5 = + − − + +
```

with the exact certificate `⅙P(++++−) + ⅙P(++−−+) + ⅓P(+−+++) + ⅙P(+−+−−) + ⅙P(+−−+−)
= ⅙P(x^1) + ⅙P(x^2) + ⅓P(x^3) + ⅙P(x^4) + ⅙P(x^5)`.  Conversely three orbits contain four states with
constant product and are exposed (the transformed states of Lemma 8 are again in `V`).

## 5. Structure for general `K`

Let `M` be the `K × m` sign matrix whose rows are the states on the `m` types (after Theorem 2), `L ⊆ ℝ^m`
its row space, and identify a type with its column `t ∈ {±1}^K`.  A vector `c ∈ ℝ^K` gives the element
`M^T c ∈ L`, whose entry at the type `t` is `c·t`.

**Proposition 5 [P].**  If `V` is not exposed, then `L` contains a sign vector that is not `±` a state of
`V`; in the certificate of Theorem 1 every `y_j` lies in `L`.

*Proof.*  In matrix form the certificate reads `Σ_j μ_j y_j y_j^T = Σ_k α_k x^k x^{kT}`.  For `z ⊥ L` the
right-hand side gives `0`, so `Σ_j μ_j (y_j·z)^2 = 0` and every `y_j ⊥ z`.  ∎

The converse fails (if the types are linearly independent, `L` is everything and `V` can be exposed).

**Theorem 6 (criterion in `K` dimensions) [P].**  Suppose the states are linearly independent (the types
span `ℝ^K`).  Let `C` be the set of `c ∈ ℝ^K`, other than `±e_1,…,±e_K`, with `c·t ∈ {+1,−1}` for every type
`t`.  Then `V` is **not** exposed iff some convex combination of the matrices `c c^T`, `c ∈ C`, is diagonal.

*Proof.*  The sign vectors of `L` other than `±V` are the `M^T c`, `c ∈ C`, with `c` unique.  The certificate
of Theorem 1 becomes `M^T (Σ_j μ_j c_j c_j^T − diag(α)) M = 0`, and `M^T Q M = 0` forces `Q = 0` because
`M^T` is injective.  The condition `Σ α_k = 1` is automatic: `t^T(Σ μ_j c_jc_j^T)t = Σμ_j (c_j·t)^2 = 1`.  ∎

**Corollary 7 (a polynomial-time sufficient condition) [P].**  If the function `1` and the `C(K,2)`
functions `t ↦ t_k t_l` (`k < l`) are linearly independent on the set of types, then `V` is exposed.

*Proof.*  The types span `ℝ^K` (if `u·t = 0` on the types, expand `(u·t)^2 = 0`).  For `c ∈ ℝ^K` with
`(c·t)^2 = 1` on the types, `Σ c_k^2 − 1 + 2Σ_{k<l} c_k c_l t_k t_l = 0`, hence `c_k c_l = 0` for `k ≠ l` and
`Σ c_k^2 = 1`: `c = ±e_k`.  So `C = ∅`; apply Proposition 5.  ∎

**Lemma 8 (four states with constant product) [P].**  Let `x^1,…,x^4 ∈ V` have `x^1∘x^2∘x^3∘x^4 = 𝟙` (negate
one of them if the product is `−𝟙`).  Then `y^k = ½(x^1+x^2+x^3+x^4) − x^k`, `k = 1,…,4`, are states,
`Σ_k P(y^k) = Σ_k P(x^k)`, and `V` is not exposed unless all four `y^k` belong to `V`.

*Proof.*  At every site an even number of the four entries are `−1`; the sum is `4`, `0` or `−4` and
`y^k_i` is `1`, `−x^k_i` or `−1`.  `Σ_k y^k y^{kT} = Σ_k x^k x^{kT}` because `y = (½𝟙𝟙^T − I)x` and `½𝟙𝟙^T − I` is
orthogonal in dimension 4.  If some `y^k ∉ V`, move the `y^k` that are in `V` to the right-hand side: a
certificate as in Theorem 1.  ∎

More generally any orthogonal `K × K` matrix `O` for which `OM` is a sign matrix with a row outside `±V`
shows that `V` is not exposed.

**Lemma 9 (decoupling) [P].**  If for some weights `p_k > 0` and some set `S` of sites
`Σ_k p_k x^k_i x^k_j = 0` for all `i ∈ S`, `j ∉ S`, then flipping the sites of `S` in every state preserves
the pair correlations of the ensemble `p`; so `V` is not exposed unless that flip maps `V` to itself.

**Proposition 10 (instances with a pair-separating symmetry) [P].**  Suppose the types span `ℝ^K`, and
let `D` be a group of diagonal sign matrices `d` such that (i) `d∘t` is a type (up to sign) for every type
`t`, and (ii) for all `k ≠ l` some `d ∈ D` has `d_k d_l = −1`.  Then `V` is exposed iff `C = ∅`, i.e. iff
the span of the states contains no sign vector other than `±` the states.

*Proof.*  If `c ∈ C` then every `d∘c ∈ C`, and the average of `(d∘c)(d∘c)^T` over `D` has off-diagonal
entries `c_kc_l·avg_d(d_kd_l) = 0`: Theorem 6.  The converse is Proposition 5.  ∎

*Example (characters).*  Sites `F_2^r`, states the characters `χ_h(a) = (−1)^{h·a}` for `h` in a set
`H ⊆ F_2^r`.  The matrices `d_a = diag(χ_h(a))_{h∈H}` satisfy (i), (ii), so the characters `{χ_h : h ∈ H}` are
exposed iff no Boolean function on `F_2^r` other than `±χ_h`, `h ∈ H`, has its Walsh spectrum supported on
`H`.  Since `f^2 = 1` gives `Σ_{h+h'=s} f̂(h) f̂(h') = 0` for `s ≠ 0`, the support of a non-linear Boolean
function contains four different elements with zero sum; conversely `½(χ_{h_1}+χ_{h_2}+χ_{h_3}−χ_{h_4})` is
Boolean when `h_1+h_2+h_3+h_4 = 0`.  Hence: **the characters are exposed iff `H` is a Sidon set** (no four
different elements with zero sum) — verified [X] for all 247 subsets of `F_2^3` with at least two elements
and 12 random subsets of `F_2^4` (`test_theory.py`).

## 6. Complexity

| version | status |
|---|---|
| `K` fixed | linear time (Theorem 2); not co-NP-hard unless P = NP |
| `K` part of the input | in co-NP (Theorem 1); polynomial sufficient conditions for "exposed" (Corollary 7) and for "not exposed" (Lemma 8: `O(K^4 n)`); **hardness open** |

What a hardness proof would need, as far as we can see: by Proposition 10 it suffices to show that
"does the span of given sign vectors contain another sign vector?" is NP-hard on instances with a
pair-separating symmetry.  The most symmetric such instances (characters) are easy by the Sidon
criterion, and the further constraints we tried (twisting spectra by functions of two or three linear
forms) are linear over `F_2`; we did not find a reduction.  Equivalent formulation, with `x^1 = 𝟙`: is the
Hamming metric on a given subset `T` of the cube `{0,1}^{K−1}` decomposable into cut metrics in exactly one
way (ℓ1-rigidity of a subset of the hypercube, with the given embedding)?

## 7. Prior art and limitations

* Not searched systematically.  One web search (2026-11-26; "cut polytope 3-neighbourly simplicial faces
  four cuts …") returned: the cut polytope is 3-neighbourly and not 4-neighbourly (statements of this in
  papers of Deza and co-authors and in Ziegler's lectures on 0/1-polytopes, seen as search snippets only),
  and the title of Deza–Laurent, *The cut cone: simplicial faces and linear dependencies* (not read).  The
  `K = 4` rule of Theorem 3 is in all likelihood contained in that literature, and the ℓ1-rigidity
  formulation of §6 is quoted from memory of Deza–Laurent, *Geometry of Cuts and Metrics* (not consulted).
  We did not find, and did not look hard for, a complexity result on recognising faces of the cut polytope
  from an explicit vertex list.
* Everything concerns the complete set of pair features.  With a restricted interaction graph, or with
  fields, the twin argument changes (twins must be twins in the graph).
* "Exposed" means exactly the global ground states.  Stability under single flips is a different, easy
  (linear-programming) condition.
* The tables are exact computations of this division; nothing here has been reviewed.

## 8. Reproduction (`experiments/complexity/ising_faces/`, Python 3 + `numpy`, `scipy`)

| program | what it does | time |
|---|---|---|
| `faces.py` | `is_exposed(vectors)`: twin reduction, linear programme, exact verification of the certificate | — |
| `table_k4.py` | all 255 type sets for `K = 4`, 15 orbits | 2 s |
| `table_k5.py` | 150 orbits for `K = 5` (log: `table_k5.log`) | 17 s |
| `span_rule.py` | Proposition 5 and Corollary 7 on all orbits for `K = 4, 5`; shows that the converse of Proposition 5 fails | seconds |
| `test_theory.py` | Theorem 2 (full system against reduced system), the `K = 4` rule on random instances with `n ≤ 9`, Proposition 5, Corollary 7, the Sidon criterion | 30 s |

## 9. Addendum: sums of squares and question E-C2 (ENSEMBLE-MSG-0004 §4)

"Is there a known lower bound on the sum-of-squares degree needed to certify that given sign vectors are
exactly the ground states of a given four-body energy?"

**Proposition 11 (interpolation bound) [P].**  Let `E ≥ 0` on the cube `{±1}^n` be a sum of squares of
polynomials of degree at most `d'` (modulo `x_i² = 1`), and let `Z` be its zero set.  Then every summand
vanishes on `Z`, so (a) `Z` is the common zero set, on the cube, of polynomials of degree at most `d'`; and
(b) if `E` is not identically zero, some non-zero multilinear polynomial of degree at most `d'` vanishes on
`Z`; in particular `|Z| < D_{d'} = Σ_{j ≤ d'} C(n,j)` whenever the points of `Z` are in general position for
degree `d'` (the evaluations of the monomials of degree at most `d'` at the points of `Z` have rank
`min(|Z|, D_{d'})`).  Conversely, for a set `V` that is the common zero set of the polynomials of degree at
most `d'` vanishing on it, the sum of the squares of a basis of these polynomials is an energy of order at
most `2d'` with a certificate of degree `2d'` and ground-state set exactly `V`.

*Proof.*  `0 = E(v) = Σ_i s_i(v)²` at every `v ∈ Z`.  ∎

So for `K` conformers in general position, certifying a non-zero energy that vanishes on them needs
sum-of-squares degree at least `2d'` with `D_{d'} > K`: degree 4 up to `K ≈ n²/2` (the range of the natural
certificate), **at least 6 beyond `n²/2`, at least 8 beyond `n³/6`**.  This is a gap that grows with `K`, but in
the range `K = O(n³)` of the Ensemble division's table only up to degree 8; it does not show that degree 6 or
8 suffices — the natural certificate of degree `2d'` is an energy of order `2d'`, not a four-body energy, and
whether a *four-body* energy exposing `K > n²/2` random conformers has a certificate of degree 6 we do not
know.

**Known bounds [K; from search snippets and memory, sources not read].**  Worst case over polynomials:
Laurent (2003) — for `n` odd, level `⌊n/2⌋` of the Lasserre hierarchy is not exact for the cut polytope of the
complete graph (a pair energy: `(Σx_i)² ≥ 1`), and Fawzi–Saunderson–Parrilo (2016) that level `⌈n/2⌉` always
suffices for quadratics; Sakaue–Takeda–Kim–Ito (2017) — level `⌈(n+2d−1)/2⌉` suffices for polynomials of
degree `2d` on the cube; Kurpisz–Leppänen–Mastrolilli (arXiv:1605.03019) — that level is necessary for some
polynomial of degree `2d` when `n` is odd.  So for four-body energies the worst-case degree is `(n+3)/2`
levels: a gap linear in `n` exists, for specific energies whose ground-state sets we have not examined (the
pair example has exponentially many ground states).  Average case: degree `Ω(n)` is needed to certify the
ground energy of random sparse 3- or 4-body parity energies (Grigoriev 2001; Schoenebeck 2008), with
degree–density trade-offs for all constraint densities (Kothari–Mori–O'Donnell–Witmer 2017); these concern
the value of the ground energy, not the ground-state set, and energies with far fewer terms than `n²`.

