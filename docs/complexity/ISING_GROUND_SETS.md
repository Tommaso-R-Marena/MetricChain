# When are K spin configurations exactly the ground states of an Ising pair energy?

Working paper of the complexity division, 2026-11-26.  Written in answer to question **E-C1** of the
Ensemble Identifiability division (ENSEMBLE-MSG-0003 §4):

> "Deciding whether `K` given sign vectors are exactly the ground states of some Ising energy with
> independent pair features is a linear programme with exponentially many constraints whose separation
> problem is a ground-state problem.  Is the decision problem co-NP-hard for `K ≥ 4`?  (For `K ≤ 3` the
> answer is always yes.)"

Register: `THEOREMS.md` CX-T16–CX-T19, CX-T25, CX-T28, CX-T29.  **Revised 2026-11-26 after the internal
adversarial review `COMPLEXITY-REV-0004`** (what changed: §10; internal AI review, not peer review).
Corollary 5a, Propositions 12, 13, 13′ and Theorem 14 were added after that review and were examined in the
internal review `COMPLEXITY-REV-0005`, which found the mathematics correct and two attributions missing
(Propositions 13 and 13′ are known in substance; what changed: §10).  Labels: [P] paper proof, [X] exact finite computation with certificates verified in
rational arithmetic, [K] known, cited.

## 0. Answer

* **For every fixed `K` the problem is solvable in linear time** (Theorem 2): whether the configurations
  are exposed depends only on the *set of column types* — which of the `2^{K−1}` possible patterns
  `±(x^1_i,…,x^K_i)` occur among the sites — not on how many sites carry each pattern.  So for fixed `K` the
  problem is a finite table and is not co-NP-hard unless P = NP.
* `K = 4` (Theorem 3, [X + P]): four configurations are exposed **unless their site-wise product is
  constant** (and they are not all the states of their three merged sites).  `K = 5`: the complete table
  (130 non-degenerate orbits of type sets, 6 of them not exposed; §4).  The one orbit not explained by a
  constant product consists of the five *singleton* states, the first member of a second infinite family
  of obstructions (Proposition 12).
* For `K` part of the input the problem is in co-NP (Theorem 1) and is **decidable in time `2^{O(K)}·poly(n)`**
  (Corollary 5a, pointed out by the referee), hence in polynomial time for `K = O(log n)`.  **Whether it is
  co-NP-hard for larger `K` we do not know**; the referee could not decide it either.
* **A natural variant is classified completely** (added after the review): the configurations are exactly
  the ground states of a pair energy that has a *sum-of-squares certificate of degree 2* if and only if
  their linear span contains no other sign vector (Proposition 13 — in substance a corollary of
  Laurent–Poljak's description of the faces and normal cones of the elliptope); deciding this is
  **co-NP-complete**, takes time `2^K·poly(n)`, and — assuming the exponential time hypothesis — not
  `2^{o(K)}·poly(n)` (Theorem 14; the reduction was found by the referee of REV-0004).  For uniformly random
  configurations the condition fails with probability `4·C(K,3)(3/4)^n` up to exponentially smaller terms,
  for every `K ≤ n − 1` [K: Odlyzko 1988 for `K ≤ n − 10n/ln n`; Irmatov 2024 for `K ≤ n − 1`]; Proposition 13′
  is an elementary explicit bound for `K ≤ n/20`.
* §5 gives further structure: an exact criterion in `K` dimensions (Theorem 6), sufficient conditions
  (Corollary 7, the isometric condition), families of obstructions (Lemmas 8, 9), and a class of instances
  with enough symmetry for which "exposed" is "no other sign vector in the span" (Proposition 10) — for
  sets of characters of `F_2^r`: "the frequency set is a Sidon set".
* **Prior art (rewritten after the review; §7).**  The object is the face lattice of the cut polytope.
  Corollary 7 is a published theorem (Laurent–Poljak 1995/96, Theorem 4.2), Proposition 5 follows from
  their description of the faces of the elliptope, the `K = 4` obstruction and the tables up to five types
  are in the literature on small cut polytopes, and Tropp (2018) proves that `r ≤ √(cn)` random
  configurations generate a simplicial face of the elliptope with high probability.  We claim no novelty
  for §§2–4, for Proposition 5 and Corollary 7, for Proposition 13 (it follows in two lines from
  Laurent–Poljak's Theorems 2.7 and 2.9; its energy is the projection rule of associative memories) or for
  Proposition 13′ (a weak form of Odlyzko's theorem of 1988) — the last two attributions were supplied by the
  referee of REV-0005.  For Theorem 6, Lemma 9, Proposition 10 with the Sidon criterion and Theorem 14 neither
  the referees nor we found a source, which is not evidence of novelty.

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
its size is doubly exponential in `K`.  For growing `K` one does not use the table: Corollary 5a decides an
instance in time `2^{O(K)}·poly(n)`.  The first version said here "this does not help when `K` grows" and
overlooked that — REV-0004, finding 3.)

*Remark (fields).*  An energy with fields `Σ h_i x_i` is a pair energy with one additional site whose spin
is fixed to `+` (its column is constant), so Theorem 2 and everything below apply to energies with fields
verbatim (REV-0004, finding 6; the first version said that the twin argument changes).  A *restricted
interaction graph* does change it.

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
four states — the first version called it sporadic; it is not (REV-0004, finding 4; Proposition 12
below):

```
x^1 = + + + + +      x^2 = + + − − −      x^3 = + − + + −      x^4 = + − + − +      x^5 = + − − + +
```

with the exact certificate `⅙P(++++−) + ⅙P(++−−+) + ⅓P(+−+++) + ⅙P(+−+−−) + ⅙P(+−−+−)
= ⅙P(x^1) + ⅙P(x^2) + ⅓P(x^3) + ⅙P(x^4) + ⅙P(x^5)`.  Conversely three orbits contain four states with
constant product and are exposed (the transformed states of Lemma 8 are again in `V`).

Negating site 2 in all five states (and `x^2` as a whole) turns them into `−++++`, `+−+++`, `++−++`, `+++−+`,
`++++−`: the five states with a single minus sign.

**Proposition 12 (singleton states) [P; observation and proof of the referee].**  Let `m ≥ 4` and let `s^i`
be the state on `m` sites with a minus sign exactly at site `i`.  Neither `{s^1,…,s^m}` nor
`{s^1,…,s^m, 𝟙}` is exposed.  For `m ≥ 5` no four of these states have a constant product.

*Proof.*  Both sets are invariant under all permutations of the sites.  If `J` exposes such a set `V`,
then so does `J∘π` for every permutation `π`, and so does the average `J̄` over all `π` (each
`E_{J∘π} − min` is `≥ 0` and vanishes exactly on `V`).  But `J̄` is constant, `J̄_ij = λ`, and
`E(x) = λ((Σ_i x_i)² − m)/2` has as its ground states only `𝟙` (`λ < 0`), all states (`λ = 0`), or the states
with `|Σ x_i| ≤ 1` (`λ > 0`); as `|Σ_j s^i_j| = m − 2 ≥ 2`, none of these sets is `V`.  The product of four
singleton states is negative at exactly four sites.  ∎

(`span_algorithm.py singletons` confirms this for `m ≤ 8`.)  The two families — four states with constant
product, singleton states — do not exhaust the obstructions: the referee reports that for `K = 6`, of 2 046
sampled type sets that are not exposed, 465 contain neither four states with constant product nor five
states that are singletons on the sites where they differ.

## 5. Structure for general `K`

Let `M` be the `K × m` sign matrix whose rows are the states on the `m` types (after Theorem 2), `L ⊆ ℝ^m`
its row space, and identify a type with its column `t ∈ {±1}^K`.  A vector `c ∈ ℝ^K` gives the element
`M^T c ∈ L`, whose entry at the type `t` is `c·t`.

**Proposition 5 [P].**  If `V` is not exposed, then `L` contains a sign vector that is not `±` a state of
`V`; in the certificate of Theorem 1 every `y_j` lies in `L`.

*Proof.*  In matrix form the certificate reads `Σ_j μ_j y_j y_j^T = Σ_k α_k x^k x^{kT}`.  For `z ⊥ L` the
right-hand side gives `0`, so `Σ_j μ_j (y_j·z)^2 = 0` and every `y_j ⊥ z`.  ∎

The converse fails (if the types are linearly independent, `L` is everything and `V` can be exposed).
Proposition 5 is not new: by Laurent–Poljak (their Theorem 2.7, as used in the proof of their Theorem 4.1)
the smallest face of the elliptope containing a matrix `X_0` is `{X : ker X ⊇ ker X_0}`, and for
`X_0 = (1/K) Σ_k x^k x^{kT}` the cut matrices in it are the `yy^T` with `y ∈ L`.

**Corollary 5a (decision in time `2^{O(K)}·poly(n)`) [P; pointed out by the referee, REV-0004 finding 3].**  `L`
contains at most `2^{r−1}` states, `r = dim L ≤ K` (a vector of `L` is determined by its entries at `r` sites
whose columns are linearly independent), and they can be listed in time `O(2^r rn)` after a Gaussian
elimination.  By Proposition 5 the certificate of Theorem 1 can be sought among these states only — a
linear programme with at most `2^{K−1} + K` variables and `O(n²)` equations.  So "is `V` exposed?" is decided
in time `2^{O(K)}·poly(n)`: **in polynomial time for `K = O(log n)`.**  (The list alone, hence the span problem
of Theorem 14, takes time `2^K·poly(n)` literally.  For the linear programme a polynomial-time method gives
`2^{O(K)}·poly(n)`; the bound `2^K·poly(n)` written in the previous version would need a method whose cost is
linear in the number of variables — REV-0005, finding 9.)

(`span_algorithm.py`: exact arithmetic for the list; both answers certified — "not exposed" by the
certificate of Theorem 1, "exposed" by a rational `J` separating `V` strictly from the other sign vectors
of `L`.  It agrees with the linear programme over all states on all 255 type sets for `K = 4` and on 900
random type sets for `K = 5, 6, 7`; the referee compared 3 895 instances.  `K = 12`, `n = 80`: 6 seconds.)

**Proposition 13 (certificates of degree 2) [K in substance — a corollary of Laurent–Poljak, see below; the
proof given is self-contained].**  The following are equivalent.
(i) Some pair energy `E_J` has ground-state set exactly `V`, and `E_J − min E_J` is, on the cube, a sum of
squares of polynomials of degree at most 1 (a sum-of-squares certificate of degree 2; equivalently the
semidefinite relaxation over the elliptope is exact for `E_J` — strong duality with dual attainment holds
because `X = I` is strictly feasible).
(ii) `L` contains no sign vector other than `±` the states of `V`.
In that case `E(x) = x^T(I − Π_L)x = dist(x, L)²`, with `Π_L` the orthogonal projector onto `L`, is such an
energy; it has rational coefficients.

*Proof.*  (ii) ⇒ (i): `x^T(I − Π_L)x = ‖x − Π_L x‖²` is a sum of squares of linear forms; on the cube it is a
constant plus a pair energy (`x_i² = 1`); and it vanishes exactly at the sign vectors of `L`.  (i) ⇒ (ii):
let `E_J − E_0 = Σ_i (a_i·x + b_i)²` on the cube.  As `E_J` is even, averaging with `x ↦ −x` gives
`E_J − E_0 = x^T A x + Σ_i b_i²` with `A = Σ_i a_i a_i^T`.  At a ground state both terms vanish; so `b = 0`
and `A x^k = 0` for all `k`; hence `A` vanishes on `L`, and every sign vector of `L` is a ground state.  ∎

*Attribution (REV-0005, finding 8).*  The first version listed Proposition 13 under "no source found".  It
follows in two lines from the report of Laurent and Poljak that this note already cites for Proposition 5:
their Theorem 2.7 (every face of the elliptope is `F_W = {X : ker X ⊇ W}`, and the smallest face containing
`X_0` is `{X : ker X ⊇ ker X_0}`) and their Theorem 2.9 (the normal cone of a face is
`{D − M : D diagonal, M ⪰ 0, ⟨M, A⟩ = 0}` — these `D − M` are exactly the certificates of degree 2); their
Example 3.8 uses that the cut matrices of `F_W` are the `ff^T` with `f ⊥ W`.  (Theorems 2.7, 2.9 and Example 3.8
as read by the referee of REV-0005, pp. 1–7 of the report; we read pp. 13–14 only.)  The referee did not find
the statement verbatim in the language of sums of squares.  The energy `x^T(I − Π_L)x` is the projection rule
(pseudo-inverse rule) of associative memories, for which the question "which other sign vectors lie in the span
of the stored patterns" was asked by Kanter and Sompolinsky (Phys. Rev. A 35 (1987) 380; not read by anyone
here).

So the gap between Proposition 5 ("not exposed ⇒ another sign vector in `L`") and its failing converse is
exactly the gap between degree 2 and higher degree: **a set with another sign vector in its span can still
be exposed, but then no exposing pair energy has a certificate of degree 2.**  On the `K = 5` table (ii)
holds for 21 053 of the 60 973 exposed type sets.  `degree2_certificates.py` checks the
statement with exact arithmetic on random sets (the zero set of `x^T(I − Π_L)x` over all states).

**Proposition 13′ (random states; an elementary bound) [P; superseded by the known theorem quoted after the
proof].**  If `x^1,…,x^K` are independent and uniform in `{±1}^n`, then

```
P( L contains a sign vector other than ± x^k )  ≤  2^{K−n} + C(n,K)·2^K·(3/4)^{n−K} ,
```

which is at most `2^{K−n} + e^{−0.038 n}` for `K ≤ n/20`.

*Proof.*  A subspace of dimension `d` contains at most `2^d` sign vectors, so `x^k` lies in the span of the
previous ones with probability at most `2^{k−1−n}`: the rank is less than `K` with probability at most
`2^{K−n}`.  If the rank is `K`, some set `I` of `K` sites has an invertible `K × K` matrix `M_I`, and a sign
vector `y = M^T c` of `L` is determined by `I` and `y_I ∈ {±1}^I` (`c = M_I^{−T} y_I`).  If `c` has a single
non-zero entry then `y = ± x^k`.  Otherwise, for each of the `n − K` other sites the entry `c·t` (with `t` an
independent uniform column) is `±1` with probability at most `3/4`: fix all coordinates of `t` but two with
non-zero coefficients; the four sums take at least three different values, at most two of which are `±1`,
and a value taken twice counts for two of the four outcomes.  A union bound over `I` and `y_I` gives the
second term.  With `C(n,K) ≤ (en/K)^K` and `K = cn`, the exponent is
`n[c(1 + ln(1/c) + ln 2) + (1 − c) ln(3/4)]`, increasing in `c` and equal to `−0.0389 n` at `c = 1/20`.  ∎

*The known theorem (REV-0005, finding 7; we had missed it).*  The probability `P(K,n)` that the span of `K`
independent uniform sign vectors contains another sign vector is the subject of A. M. Odlyzko, *On subspaces
spanned by random selections of ±1 vectors*, J. Combin. Theory Ser. A 47 (1988) 124–133, written for exactly
this question about associative memories:

```
P(K,n)  =  4·C(K,3)·(3/4)^n  +  O(K⁴ (5/8)^n)  +  O((7/10)^n)          for  K ≤ n − 10n/ln n     [K: Odlyzko 1988],
P(K,n)  =  4·C(K,3)·(3/4)^n  +  O(K⁴ (5/8)^n)  +  O((5/8 + o(1))^n)    for  K ≤ n − 1            [K: Irmatov 2024, arXiv:2405.05082].
```

(Both as quoted in Irmatov's Theorems 1.1 and 1.2, read by the referee and, on 2026-11-26, by a fetch of ours;
Odlyzko's paper itself could not be opened by either — its bibliographic data are given from the referee's
report.)  So the leading term is the event that some `±x^a ± x^b ± x^c` is a sign vector — each of these
`4·C(K,3)` vectors (up to a global sign) is one with probability exactly `(3/4)^n` — and **the condition of
Proposition 13 holds with probability tending to 1 for every `K ≤ n − 1`**: the question "up to which `K`" that the
previous version left open has this answer, and its sentence that these vectors "dominate", supported there by
simulations, is a theorem.  Proposition 13′ remains only as a bound with explicit constants and a five-line
proof.

For comparison [K, Tropp 2018, Theorems 2.9–2.11 and Fact 2.7; read by us]: the stronger property that
`conv{x^k x^{kT}}` is a (simplicial) face of the elliptope holds with probability at least
`1 − K² exp(−n/K²)`, and never for `K(K−1) > 2(n−1)`.

*For small systems the event is common.*  In simulations (`degree2_certificates.py`, 60 trials each) the span
contained another sign vector in 12 % of the cases for `n = 12, K = 3` (leading term `4·(3/4)^12 = 13 %`), 13 % for
`n = 16, K = 4` (leading term 16 %), 85 % for `n = 12, K = 6`, 77 % for `n = 16, K = 8`, and always for `K ≥ 3n/4`
at these sizes — the asymptotic statement above is far from effective there (the terms `K⁴(5/8)^n` are not
small).  So for the sizes of an explicit enumeration a random set of states is typically exposed (Corollary 7
needs many types, but the exact decision says so) **without** being exposed by an energy with a certificate
of degree 2; the bound of Proposition 13′ only becomes effective for `n` in the hundreds
(`n = 100, K = 5`: `0.003`; `n = 200, K = 10`: `4·10^{−5}`).

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

**Corollary 7 is a published theorem** [K]: Laurent and Poljak, *On the facial structure of the set of
correlation matrices* (CWI report BS-R9501, 1995; journal version 1996), Theorem 4.2: if `f_1,…,f_k ∈ {±1}^n`
are linearly independent and the vectors `f_h∘f_{h'}` (`h < h'`) together with `𝟙` are linearly independent,
then `conv{f_h f_h^T}` is a face of the elliptope — and a face of the elliptope whose vertices are cut
matrices is a face of the cut polytope.  Their Theorem 4.1 adds that such a face is a simplex and that
`C(k,2) ≤ n − 1`; their Corollary 4.5 is the case in which all `2^{k−1}` types occur.  (We read pp. 13–14 of
the report; REV-0004, finding 2.)  The proof above is theirs in our notation, with Proposition 13 in the
background: under the hypothesis the span contains no other sign vector.

**A second sufficient condition** [K; reported by the referee from the survey of Deza and Laurent,
*Applications of cut polyhedra*, §2.5 — "every isometric subgraph of the hypercube is ℓ1-rigid"; not read
by us].  Gauge some state `x^{k_0}` to `𝟙`, so that the types become points of the cube `{0,1}^{K−1}`.  If any
two types are joined by a chain of types that changes one coordinate at a time and has length equal to
their Hamming distance, then `V` is exposed.  On the `K = 5` table this covers 15 977 type sets, Corollary 7
covers 5 425, one of the two 19 233, and condition (ii) of Proposition 13 covers 21 053, of the 60 973
exposed ones; none of the three conditions holds for a set that is not exposed (`span_algorithm.py
conditions`; the first two numbers are also the referee's).

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

*Proof* (missing in the first version; REV-0004, finding 8).  Let `x̃^k` be `x^k` with the sites of `S`
negated.  Then `Σ_k p_k P(x̃^k) = Σ_k p_k P(x^k)`: the entries with both sites in `S` or both outside are
unchanged, the others change sign and sum to zero.  If some `x̃^k ∉ V`, move the terms with `x̃^k ∈ V` to the
right-hand side and divide by the remaining weight: a certificate as in Theorem 1.  ∎

**Proposition 10 (instances with a pair-separating symmetry) [P].**  Suppose the types span `ℝ^K`, and
let `D` be a group of diagonal sign matrices `d` such that (i) `d∘t` is a type (up to sign) for every type
`t`, and (ii) for all `k ≠ l` some `d ∈ D` has `d_k d_l = −1`.  Then `V` is exposed iff `C = ∅`, i.e. iff
the span of the states contains no sign vector other than `±` the states.

*Proof.*  If `c ∈ C` then every `d∘c ∈ C`, and the average of `(d∘c)(d∘c)^T` over `D` has off-diagonal
entries `c_kc_l·avg_d(d_kd_l) = 0`: Theorem 6.  The converse is Proposition 5.  ∎

*Example (characters).*  Sites `F_2^r`, states the characters `χ_h(a) = (−1)^{h·a}` for `h` in a set
`H ⊆ F_2^r`.  The matrices `d_a = diag(χ_h(a))_{h∈H}` satisfy (i), (ii), so the characters `{χ_h : h ∈ H}` are
exposed iff no Boolean function on `F_2^r` other than `±χ_h`, `h ∈ H`, has its Walsh spectrum supported on
`H`.  Since `f^2 = 1` gives `Σ_{h+h'=s} f̂(h) f̂(h') = 0` for `s ≠ 0`, the support of a Boolean
function that is not `±` a character contains four different elements with zero sum; conversely `½(χ_{h_1}+χ_{h_2}+χ_{h_3}−χ_{h_4})` is
Boolean when `h_1+h_2+h_3+h_4 = 0`.  Hence: **the characters are exposed iff `H` is a Sidon set** (no four
different elements with zero sum) — verified [X] for all 247 subsets of `F_2^3` with at least two elements
and 12 random subsets of `F_2^4` (`test_theory.py`).

## 6. Complexity

| version | status |
|---|---|
| `K` fixed | linear time (Theorem 2); not co-NP-hard unless P = NP |
| `K = O(log n)` | polynomial time (Corollary 5a) |
| `K` part of the input, "is `V` exposed?" | in co-NP (Theorem 1); time `2^{O(K)}·poly(n)` (Corollary 5a); polynomial sufficient conditions for "exposed" (Corollary 7, the isometric condition) and for "not exposed" (Lemma 8: `O(K^4 n)`); **hardness open** |
| `K` part of the input, "is `V` exposed by an energy with a certificate of degree 2?" (⇔ no other sign vector in the span) | **co-NP-complete**; time `2^K·poly(n)`; not `2^{o(K)}·poly(n)` under ETH (Theorem 14) |

**Theorem 14 (the span problem) [P; the reduction was found by the referee of REV-0004 and checked by us].**
SPAN: *given `K` pairwise different states, does their linear span contain a sign vector other than `±` these
states?*  SPAN is NP-complete.  Consequently:
(a) deciding whether `V` satisfies the equivalent conditions of Proposition 13 is co-NP-complete;
(b) SPAN is solvable in time `2^K·poly(n)` (Corollary 5a) and, assuming the exponential time hypothesis, not
in time `2^{o(K)}·poly(n)`;
(c) every instance produced by the reduction is exposed, so the reduction says nothing about the
complexity of "is `V` exposed?".

*Proof.*  SPAN is in NP (the sign vector is the certificate).  We reduce from positive 1-in-3-SAT [K;
Schaefer 1978; Garey–Johnson, problem LO4, with the remark that it stays NP-complete without negations —
cited from memory]: given clauses `A_1,…,A_M`, each a set of three of the variables `1,…,N`, every variable
in some clause, is there a set `U` of variables with `|U ∩ A_i| = 1` for all `i`?  Take the states `x^1,…,x^N`,
`x^z`, `𝟙`, and as sites the sets `∅`, `{k}` (`k ≤ N`), `A_i`, `A_i ∪ {z}`, and `A_i ∪ A_j ∪ {z}` (`i < j`); the state
`x^k` (resp. `x^z`) is `−1` exactly on the sites that contain `k` (resp. `z`).  The states are pairwise different
and linearly independent.  Let `v = Σ_k c_k x^k + c_z x^z + c_0 𝟙` be a sign vector; replacing `v` by `−v` we may
assume that its entry at the site `∅` is `+1`.  The site `{k}` gives `1 − 2c_k = ±1`, so `c_k ∈ {0,1}`; let
`U = {k : c_k = 1}`.  The site `A_i` gives `|U ∩ A_i| ≤ 1`, and the site `A_i ∪ {z}` gives
`|U ∩ A_i| + c_z ∈ {0,1}`, so `c_z ∈ {−1, 0, 1}`.
*`c_z = 0`:* if `U` had two elements, in clauses `A_i` and `A_j`, the site `A_i` (if `i = j`) or `A_i ∪ A_j ∪ {z}`
would give an entry `≤ −3`; so `|U| ≤ 1` and `v` is `𝟙` or some `x^k`.
*`c_z = 1`:* `|U ∩ A_i| = 0` for all `i`, so `U = ∅` and `v = x^z`.
*`c_z = −1`:* `|U ∩ A_i| = 1` for all `i`; conversely, for such a `U` the vector
`Σ_{k∈U} x^k − x^z + (2 − |U|)𝟙` has entries `±1` at all sites (at `A_i ∪ A_j ∪ {z}`:
`3 − 2|U ∩ (A_i ∪ A_j)| ∈ {1, −1}`) and is not `±` a state.
So the span contains another sign vector iff the instance is satisfiable.  (a) follows with Proposition 13.
(b): the reduction has `K = N + 2` and `n = O(N + M²)` sites, and positive 1-in-3-SAT has no algorithm of
running time `2^{o(N)}` under ETH: by the sparsification lemma [K; Impagliazzo–Paturi–Zane, cited from memory]
3-SAT has no `2^{o(N+M)}` algorithm, Schaefer's clause gadget turns a 3-SAT clause into a constant number of
1-in-3 clauses with a constant number of new variables, and a negated variable `x′ = ¬x` is forced by three
positive clauses `R(x,x′,a)`, `R(x,x′,b)`, `R(a,b,c)` with new variables `a, b, c` (exactly one of `x, x′, a` and
exactly one of `x, x′, b` is true, so `a = b`; then `R(a,b,c)` forces `a = b = 0`, hence exactly one of `x, x′` is
true) — both gadgets have constant size, so the number of variables of the positive instance is linear in
`N + M` (the two gadgets as spelled out by the referee of REV-0005, finding 10).  (c): in the notation of Theorem 6 every `c ∈ C` has `c_z = −1` and
`c_k = 1` for `k` in a non-empty set `U`, so the entries `(k,z)` of `cc^T` are `≤ 0` and one of them is `−1`; no
convex combination of such matrices is diagonal, and `V` is exposed.  ∎

(`span_algorithm.py reduction`: on 60 random instances the other sign vectors of the span are exactly the
vectors of the exact hitting sets, and every instance is exposed; the referee ran the same check with
independent code.)

**What a hardness proof for "is `V` exposed?" would need.**  By (c), hardness cannot come from the span
condition alone: it has to come from the condition of Theorem 6 that some convex combination of the
matrices `cc^T` is diagonal — for every pair `k ≠ l` the products `c_kc_l` must cancel over the certificate
(the referee's formulation).  By Proposition 10 the span condition is the whole story on instances with a
pair-separating symmetry, and any instance can be given such a symmetry by tensoring the states with
different characters, `x^k ↦ x^k ⊗ χ_{h_k}`; but with labels `h_k` forming a Sidon set the result is always
exposed (each restriction `y(i,·)` of a sign vector of the span is a Boolean function with spectrum in
the Sidon set, hence `±` a character), and the most symmetric instances (characters) are decided by the
Sidon criterion.  We did not find a reduction, and neither did the referee.

**Formulation with cut metrics (corrected).**  Gauge `x^1 = 𝟙`.  The other states are cuts `S_2,…,S_K` of the
set `T` of types, and `d = Σ_{k≥2} δ(S_k)` is the Hamming metric of `T ⊆ {0,1}^{K−1}`.  Since the faces of the cut
polytope through the vertex `P(𝟙)` are the faces of the cut cone, **`V` is exposed iff every representation
of `d` as a non-negative combination of cut semimetrics uses only the cuts `S_2,…,S_K`.**  ℓ1-rigidity of `T`
— uniqueness of the representation — is this property *together with* the linear independence of
`δ(S_2),…,δ(S_K)`, i.e. the face is a simplex.  The first version of this note said "exposed iff the
representation is unique"; that is wrong (REV-0004, finding 1): all eight states on four sites are
exposed (`J = 0`) and their metric has several representations; another counterexample of the referee is
the twelve roots of `x_1x_2 + x_1x_3 + x_2x_3 ≥ −1` on five sites.

## 7. Prior art and limitations

How each source was inspected (2026-11-26).  "The referee" is the referee of COMPLEXITY-REV-0004, who
downloaded the texts; "we" read the pages named from those downloads.

| source | inspected | what it contains for this note |
|---|---|---|
| M. Laurent, S. Poljak, *On the facial structure of the set of correlation matrices*, CWI report BS-R9501 (1995); journal version SIAM J. Matrix Anal. Appl. 17 (1996) (reference as given by the referee) | pp. 13–14 of the report read by us (Theorem 4.1 with proof; Theorem 4.2 with its proof up to Claim 4.3); abstract and p. 15 by the referee | Theorem 4.2 = Corollary 7; Theorem 4.1 (such faces are simplices, `C(k,2) ≤ n − 1`); Corollary 4.5 (all types present); faces of the elliptope described by kernels ⇒ Proposition 5 |
| J. Tropp, *Simplicial faces of the set of correlation matrices*, arXiv:1801.00749v1 | pp. 1–6 read by us (abstract, §1, §2 with Facts 2.5–2.8, 2.12 and Theorems 2.9–2.11); §§1–3 by the referee | `r` uniformly random states generate a simplicial face of the elliptope — hence of the cut polytope — with probability `≥ 1 − r² exp(−n/r²)`, also `≥ 1 − 4 exp((r² − c n/16)/4)` with an absolute `c ≥ 0.0003`; no simplicial face of the elliptope has more than about `√(2n)` vertices.  Directly relevant to the Ensemble division's random conformers |
| M. Deza, M. Laurent, *Applications of cut polyhedra*, report LIENS-92-18 | by the referee (§2.5, the rigidity examples, Table 1, the section on the equidistant metric); **not by us** | ℓ1-rigid = on a simplicial face; the path metric of `K_4` is not ℓ1-rigid (the `K = 4` obstruction); isometric subgraphs of the hypercube are ℓ1-rigid |
| A. Deza, M. Deza, report LIENS-95-1 (face lattice of the cut polytope on five nodes) | by the referee (§1, §3); **not by us** | `f_3 = 1780`, so 40 four-sets of vertices are not faces — the number Theorem 3 gives on five sites (we recomputed: of the 1 820 four-subsets of the 16 states, 1 780 are exposed and 40 are not, all with constant product).  The referee notes a misprint in the report's `f_7` |
| N. Wang, J. Rauh, H. Massam, arXiv:1603.04843 | by the referee (introduction, §2.2); **not by us** | the same decision problem appears in statistics as the recognition of facial sets (existence of the maximum-likelihood estimate); no hardness statement found there |
| Deza–Laurent–Poljak, *The cut cone III*; Deza–Laurent, *The cut cone: simplicial faces and linear dependencies*; the book *Geometry of Cuts and Metrics* | abstract / bibliographic record only (referee); the book was not accessible | — |
| Laurent–Poljak (the report above), Theorems 2.7, 2.9, Example 3.8 | pp. 1–7 and 12–15 as page images by the referee of REV-0005; **not by us** beyond pp. 13–14 | faces of the elliptope are given by kernels; normal cones are `{D − M}` ⇒ Proposition 13 in two lines |
| A. M. Odlyzko, *On subspaces spanned by random selections of ±1 vectors*, J. Combin. Theory Ser. A 47 (1988) 124–133 | **not opened** (HTTP 503/403 for the referee of REV-0005 and for us); statement known through Irmatov's quotation | `P(K,n) = 4C(K,3)(3/4)^n + O(K⁴(5/8)^n) + O((7/10)^n)` for `K ≤ n − 10n/ln n` ⇒ supersedes Proposition 13′ |
| A. A. Irmatov, *On linear-combinatorial problems associated with subspaces spanned by {±1}-vectors*, arXiv:2405.05082v1 (2024) | abstract and pp. 1–2 by the referee of REV-0005; abstract and Theorems 1.1, 1.2 by a fetch of ours | the same asymptotics for all `K ≤ n − 1`, error `O((5/8 + o(1))^n)`; quotes Odlyzko's theorem; says the question comes from Kanter and Sompolinsky's associative memories |
| I. Kanter, H. Sompolinsky, *Associative recall of memory without errors*, Phys. Rev. A 35 (1987) 380 | **not read** by anyone here (reference as given by the referee of REV-0005) | the projection rule; origin of the question on sign vectors in the span |

* **Not found**, by the referee (searches listed in the report) or by us: a complexity result on
  recognising faces of the cut polytope from a vertex list; Theorem 6 in this form; Lemma 9; Proposition 10
  with the Sidon criterion; Theorem 14.  A failure to find them is not evidence of novelty.  (Proposition 13
  stood in this list until REV-0005: it is a corollary of Laurent–Poljak's Theorems 2.7 and 2.9, and the fact
  that the sign vectors in the span are ground states of the projection energy is classical in the theory of
  associative memories.)
* Everything concerns the complete set of pair features (with or without fields; §3, remark).  A restricted
  interaction graph changes the twin argument (twins must be twins in the graph).
* "Exposed" means exactly the global ground states.  Stability under single flips is a different, easy
  (linear-programming) condition.
* The tables are exact computations of this division, recomputed by the referee with independent code.
  Internal AI review is not academic peer review.

## 8. Reproduction (`experiments/complexity/ising_faces/`, Python 3 + `numpy`, `scipy`)

| program | what it does | time |
|---|---|---|
| `faces.py` | `is_exposed(vectors)`: twin reduction, linear programme, exact verification of the certificate | — |
| `table_k4.py` | all 255 type sets for `K = 4`, 15 orbits | 2 s |
| `table_k5.py` | 150 orbits for `K = 5` (log: `table_k5.log`) | 17 s |
| `span_rule.py` | Proposition 5 and Corollary 7 on all orbits for `K = 4, 5`; shows that the converse of Proposition 5 fails | seconds |
| `test_theory.py` | Theorem 2 (full system against reduced system), the `K = 4` rule on random instances with `n ≤ 9`, Proposition 5, Corollary 7, the Sidon criterion | 30 s |
| `span_algorithm.py [agree, singletons, conditions, reduction, timing]` | Corollary 5a (the `2^K` algorithm, exact) and its agreement with the full linear programme; Proposition 12 for `m ≤ 8`; the counts of the sufficient conditions on the `K = 5` table; the reduction of Theorem 14 on 60 instances; timings | ≈ 2 min |
| `degree2_certificates.py` | Proposition 13: the zero set of `x^T(I − Π_L)x` over all states, exact; frequencies for Proposition 13′ | minutes |

**Coverage of our own tests** (REV-0004, finding 7).  `test_theory.py` tests Theorem 2 on 300 random
instances, of which 218 are degenerate, 79 exposed and 3 not exposed, and it gauges anti-twins away before
solving; Corollary 7 on 3 random cases; the Sidon criterion on 12 subsets of `F_2^4`.  That is thin.  The
referee's independent tests are much wider: Theorem 2 on 885 instances with true anti-twins (552 not
exposed), with the construction of the proof checked for `c = 1/1000, 1, 1000`; 1 301 random instances for
`K = 4,…,7`; Lemma 8 on 225 cases and Lemma 9 on 148; the Sidon criterion on all 247 subsets of `F_2^3`, 60
of `F_2^4` and 200 of `F_2^5`; Proposition 10 on 300 twisted character instances; 3 847 type sets for
`K = 6`; and the face numbers of the cut polytope on five nodes as an external anchor.  The referee's
programs are kept in `experiments/complexity/reviews/rev4_ising_nanuq/`.

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

## 10. Changes after the review COMPLEXITY-REV-0004

| finding | change |
|---|---|
| 1 (major): "exposed ⇔ the Hamming metric decomposes into cut metrics in exactly one way" is false for faces that are not simplices | §6, "Formulation with cut metrics (corrected)" |
| 2 (major): Corollary 7 is Laurent–Poljak's Theorem 4.2, Proposition 5 follows from their description of faces; further prior art (Tropp; Deza–Laurent; Deza–Deza; facial sets); a second known sufficient condition | attributions at Proposition 5 and Corollary 7; the isometric condition in §5; §0 and §7 rewritten with the way each source was inspected; registers CX-T16–T19 |
| 3: Proposition 5 gives an algorithm in time `2^K·poly(n)`; "does not help when `K` grows" was wrong | Corollary 5a, `span_algorithm.py`; complexity table |
| 4: the sixth orbit of the `K = 5` table is not sporadic | Proposition 12 (singleton states), with the referee's proof; the caveat that the two families are not exhaustive |
| 5: "another sign vector in the span" is NP-complete, but those instances are exposed; a necessary condition; tensoring with characters | Theorem 14 and the paragraph after it; combined with the new Proposition 13 it classifies the degree-2 variant |
| 6: "with fields the twin argument changes" was inaccurate | remark in §3 |
| 7: thin tests; a floating-point rank where an exact test was promised | `span_rule.py` now uses the exact routine; coverage paragraph in §8 |
| 8: Lemma 9 had no proof; "non-linear" should be "not ± a character" | proof added; wording corrected |

Added after that review: Proposition 13, Proposition 13′ and the consequences (a), (b) of Theorem 14.

**Changes after the review COMPLEXITY-REV-0005** (Corollary 5a, Propositions 12, 13, 13′, Theorem 14, the corrected
formulation with cut metrics).  The referee found the mathematics correct (Proposition 12 for `m = 4..8` by the
full linear programme; Proposition 13 on 400 instances; Theorem 14 re-derived case by case and tested on 820
instances) and the attributions incomplete:

| finding | change |
|---|---|
| 7 (major, prior art): Proposition 13′ is a weak form of Odlyzko's theorem (1988); "up to which `K`" is answered there and by Irmatov (2024) | the known theorem is quoted after Proposition 13′, which is relabelled as an elementary bound; §0; §7 |
| 8 (major, attribution): Proposition 13 follows from Laurent–Poljak's Theorems 2.7 and 2.9 and was listed under "no source found" | relabelled "[K] in substance"; attribution paragraph after the proof; §0; §7 |
| 9: "time `2^K·poly(n)`" for the exposedness decision needs a linear-programming method linear in the number of variables | `2^{O(K)}·poly(n)` in §0, Corollary 5a and the table; `2^K·poly(n)` kept for the span problem, where it is literal |
| 10: the ETH statement of Theorem 14(b) can be made self-contained; one line on strong duality in Proposition 13(i) | both added |

The referee's strongest objection, in its words: "Proposition 13 is Laurent–Poljak 1993/95 restated with the 1980s
projection rule.  Proposition 13′ is a weak form of Odlyzko 1988, written for exactly this memory model.
Theorem 14 is a routine Partition-style reduction which, by its own item (c), says nothing about the original
question E-C1.  That question is still open."  We agree with each sentence.
