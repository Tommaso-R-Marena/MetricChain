# Optimising pair data over one chain conformation: hard in the worst case — also with fixed bond angles — and where it is easy

Complexity division, 2026-11-26; **revised 2026-11-27 after the internal review COMPLEXITY-REV-0006** (every
derivation found correct; one corollary cited a theorem that does not give the accuracy claimed; the literature
on fixed-angle chains was missing — both repaired, §2b and §7; internal AI review, not peer review).  Register:
`THEOREMS.md` CX-T32, CX-T33; the gadget inequalities are kernel-checked (CX-V6).  Written in answer to
the Geometry division's question C1 (GEOMETRY-REQ-0004; our first answer was COMPLEXITY-RES-0002) and to the
research owner's directive on algorithmic feasibility ("tractability of articulated systems").  Labels: [P] paper
proof, [X] exact computation, [N] numerical evidence, [K] known and cited.

**The central hardness statement is not ours.**  That the underlying problem — unit vectors in a fixed dimension
maximising a quadratic form, "vector Max-Cut" — is NP-hard was conjectured by Lovász and proved for dimension 3 by
Kallaugher, Parekh, Thompson, Wang and Yirka (2024) and for every fixed dimension, with hardness of
approximation, by Piddock (preprint, October 2025); see §7.  We found a short proof on the day this note was
written, believed for an hour that it might be new, and found these papers by searching before anything was
published.  What the note contributes is the translation to chains (§1), the observation that fixed bond angles
do not help (§3), the tractable regime (§4), and two short self-contained derivations of the known hardness
(§2, §2a) that a reader can check in a few minutes.

## 0. Summary

A *chain* is a sequence of points `x_1,…,x_n ∈ ℝ^3` with unit bonds, `|x_{k+1} − x_k| = 1`; `b_k = x_{k+1} − x_k`.
For data `c = (c_ij)_{i<j}` consider

```
CHAIN:        maximise   Σ_{i<j} c_ij |x_i − x_j|²        over chains,
CHAIN(θ):     the same over chains with a fixed angle θ between consecutive bond vectors (torsions free).
```

(The usual bond angle is `π − θ`; the tetrahedral value is `θ ≈ 70.5°`.  Chains may intersect themselves: steric
constraints are not modelled.)

1. **Theorem 1** [K; our proof P; N].  The ground-state problem of the classical Heisenberg model with arbitrary
   couplings, `max Σ_{k<l} Q_kl ⟨b_k, b_l⟩` over unit vectors in `ℝ^3`, is strongly NP-hard: for every graph `G` there
   are integer couplings of size `O(|E|)` on `5|V| + 4` spins whose optimum is `10Λ(2|V|+1) + 2·maxcut(G) − |E|`.
   **Proposition 1a** [K; our proof P; N]: the same for unit vectors in `ℝ^k`, every `k ≥ 1`, already for the
   antiferromagnetic model on an unweighted graph (vector Max-Cut), by an exact identity
   `OPT_{k+1}(H') = 25nL + 9·OPT_k(H)`.
2. **Corollary 2** [P].  CHAIN is strongly NP-hard: it *is* the Heisenberg problem, by a linear bijection between
   the data `c` and the couplings `Q` (COMPLEXITY-RES-0002).  This removes the condition "if the cited theorems are
   as summarised" from that message.  By Piddock's theorem there is moreover a constant `α < 1` such that
   approximating the maximum within the factor `α` is NP-hard (Remark in §2a).  **Corollary 5** [P, given K]: the
   question as the Geometry division asked it — is a complete table of averaged squared distances that of some
   ensemble of freely jointed chains? — is NP-hard in the weak sense under Turing reductions (§2b; for
   polynomially small accuracy this rests on a theorem that we have not read).
3. **Theorem 3** [P; N].  CHAIN(θ) is strongly NP-hard for every fixed `θ ∈ (0, π)`: every `m`-th bond of a
   fixed-angle chain is a free unit vector, `m = ⌈π / min(θ, π − θ)⌉` (`m = 3` for the tetrahedral angle).
   **Fixing the bond angles does not make the problem easier in the worst case.**
4. **Proposition 4** [P].  What does make it easier is the *range* of the data: if `c_ij = 0` for `j − i > w`, the
   collinear version is solved exactly in time `O(n·w·2^w)`, and CHAIN(θ) is approximated within an additive error
   `ε·Σ|Q|` in time `O(n·w·(πw/ε)^{w−1})` by dynamic programming over torsion angles.  The hard instances need data
   between atoms far apart along the chain (a number of data points linear in the size of the graph suffices),
   and under the exponential time hypothesis the exact problem has no algorithm of running time
   `2^{o(w)}·poly(n)`.

None of this is a statement about typical instances, about positive semidefinite objectives (for which constant
approximation ratios are known, §7), or about ensembles of conformations.

## 1. From data to couplings

For `i < j`, `x_j − x_i = Σ_{k=i}^{j−1} b_k`, so `|x_i − x_j|² = Σ_{k,l=i}^{j−1} ⟨b_k, b_l⟩` and

```
Σ_{i<j} c_ij |x_i − x_j|²  =  Σ_{k,l=1}^{n−1}  Q̃_kl ⟨b_k, b_l⟩ ,         Q̃_kl = Σ_{i ≤ min(k,l)}  Σ_{j > max(k,l)}  c_ij .      (1)
```

The map `c ↦ (Q̃_kl)_{k ≤ l}` is a linear bijection, with inverse
`c_ij = Q̃_{i,j−1} − Q̃_{i−1,j−1} − Q̃_{i,j} + Q̃_{i−1,j}` (terms with an index `0` or `n` are zero): the mixed second
difference of the partial sums.  The diagonal `Q̃_kk` contributes the constant `Σ_k Q̃_kk`.  So for any symmetric `Q`
with zero diagonal the data `c` belonging to `Q̃ = Q` give
`Σ c_ij|x_i − x_j|² = 2 Σ_{k<l} Q_kl ⟨b_k, b_l⟩`; integer `Q` give integer `c`, and each non-zero `Q_kl` produces at
most four non-zero data points.  If `c_ij = 0` for `j − i > w`, then `Q̃_kl = 0` for `|k − l| ≥ w`.  (Identity and
inverse checked numerically on random chains, `heisenberg_reduction.py` part 3.)

## 2. The Heisenberg ground-state problem in `ℝ^3` (couplings of both signs)

`HEIS`: given a symmetric integer matrix `Q` with zero diagonal and an integer `τ`, is
`max { F(b) = Σ_{k<l} Q_kl ⟨b_k, b_l⟩ : b_k ∈ ℝ^3, |b_k| = 1 } ≥ τ`?

**Lemma (orthogonality gadget) [P; X].**  For `t ∈ [−1,1]` let `h(t) = √(25 + 24t) + √(25 − 24t)`.  Then
`h(t) ≤ 10 − t²`, with equality only at `t = 0`.  Consequently, if two new spins `a, a'` are coupled to spins `p, q`
by `Q_{ap} = 3Λ`, `Q_{aq} = 4Λ`, `Q_{a'p} = 3Λ`, `Q_{a'q} = −4Λ` and to nothing else, their optimal contribution is
`Λ(|3p + 4q| + |3p − 4q|) = Λ·h(⟨p,q⟩) ≤ Λ(10 − ⟨p,q⟩²)`: it is `10Λ` exactly when `p ⟂ q`.

*Proof.*  `h² = 50 + 2√(625 − 576t²)` and `(10 − t²)² = 100 − 20t² + t⁴`; so the claim is
`√(625 − 576t²) ≤ 25 − 10t² + t⁴/2`, and squaring (both sides are positive) it becomes
`0 ≤ 76t² + 125t⁴ − 10t⁶ + t⁸/4`, true on `[−1,1]` with equality only at `0`.  ∎

**Theorem 1 [K — see §7; this proof P].**  Let `G = (V, E)` be a graph with `n` vertices and at least one edge, and
`Λ = 4|E|`.  Take spins `u_v` (`v ∈ V`), two *poles* `z_1, z_2`, and the spins of the following gadgets: couplings `−1`
between `u_v` and `u_w` for every edge; an orthogonality gadget of strength `Λ` between `u_v` and `z_i` for all `v` and
`i = 1, 2`; and one between `z_1` and `z_2`.  Then

```
max F  =  10Λ(2n + 1) + 2·maxcut(G) − |E| .
```

There are `5n + 4` spins and the couplings are integers of absolute value at most `16|E|`.  Hence HEIS is strongly
NP-hard (MAX-CUT is NP-complete [K, Karp 1972]).

*Proof.*  Maximising over the gadget spins first, `max F` is the maximum over `u, z` of

```
Λ [ Σ_v ( h(t_{v1}) + h(t_{v2}) ) + h(s) ]  −  Σ_{vw ∈ E} ⟨u_v, u_w⟩ ,          t_{vi} = ⟨u_v, z_i⟩,   s = ⟨z_1, z_2⟩ .
```

*Lower bound.*  `z_1 = e_1`, `z_2 = e_2`, `u_v = σ_v e_3` with `σ` a maximum cut: all `t`, `s` vanish and the edge term is
`2·maxcut − |E|`.

*Upper bound, case `|s| ≤ ½`.*  Let `e` be a unit vector orthogonal to `z_1, z_2`, and write `u_v = a_v e + p_v` with
`p_v ∈ span(z_1,z_2)`.  With `τ_v = t_{v1}² + t_{v2}²`:
`|p_v|² = (t_{v1}² + t_{v2}² − 2s t_{v1}t_{v2})/(1 − s²) ≤ τ_v/(1 − |s|) ≤ 2τ_v`.  Let `σ_v = ±1` be the sign of `a_v`
(`+1` if `a_v = 0`).  For an edge `vw`: `−⟨u_v,u_w⟩ = −a_va_w − ⟨p_v,p_w⟩`.  If `σ_vσ_w = 1`,
`−a_va_w = −1 + (1 − |a_v||a_w|) ≤ −1 + |p_v|² + |p_w|²` (as `x² + y² − xy ≤ 1` for `x, y ∈ [0,1]` — a convex function,
`≤ 1` at the four corners — and `1 − a_v² = |p_v|²`); if `σ_vσ_w = −1`, `−a_va_w ≤ 1`.  And
`−⟨p_v,p_w⟩ ≤ ½(|p_v|² + |p_w|²)`.  So `−⟨u_v,u_w⟩ ≤ −σ_vσ_w + (3/2)(|p_v|² + |p_w|²)`, and summing over the edges,

```
− Σ_E ⟨u_v,u_w⟩  ≤  (2·cut(σ) − |E|) + 3 d_max Σ_v τ_v .
```

By the Lemma the gadget part is at most `Λ[10(2n+1) − Σ_v τ_v]`.  As `Λ ≥ 3 d_max`, the total is at most
`10Λ(2n+1) + 2·maxcut − |E|`.

*Case `|s| > ½`.*  The gadget between the poles loses more than `Λ/4 = |E|`, the edge term is at most `|E|`, and
`2·maxcut − |E| ≥ 0`: the total is below `10Λ(2n+1) ≤ 10Λ(2n+1) + 2·maxcut − |E|`.  ∎

**Corollary 2 [P].**  CHAIN — deciding whether `max Σ c_ij|x_i − x_j|² ≥ τ` for integer data — is strongly NP-hard.
(Section 1 with the matrix of Theorem 1; a chain with `5|V| + 5` atoms.)

## 2a. Every dimension, antiferromagnetic couplings on an unweighted graph: an exact lifting

For a simple graph `H = (V,E)` and `k ≥ 1` let

```
OPT_k(H)  =  max { − Σ_{vw ∈ E} ⟨x_v, x_w⟩ :  x_v ∈ ℝ^k, |x_v| = 1 } .
```

(`(|E| + OPT_k(H))/2 = max Σ_E |x_v − x_w|²/4` is the value of *vector Max-Cut* in `ℝ^k`, called `Max-Cut_k` or `MC_k` in
the literature; `OPT_1(H) = 2·maxcut(H) − |E|`.)

**Lemma (blow-up) [P].**  Let `Γ` be a graph with a positive integer multiplicity `m_C` at every vertex `C`, and let
`Γ[m]` be the simple graph in which `C` is replaced by `m_C` pairwise non-adjacent copies and adjacent vertices by
complete bipartite graphs.  Then `OPT_k(Γ[m]) = max_x − Σ_{CC' ∈ E(Γ)} m_C m_{C'} ⟨x_C, x_{C'}⟩`.

*Proof.*  "≥": give all copies of `C` the vector `x_C`.  "≤": in an optimal configuration of `Γ[m]`, the copies of `C`
have the same neighbours, hence the same field `h_C` (the sum of the vectors of the neighbours), and contribute
`−⟨y, h_C⟩ ≤ |h_C|` each; replacing all of them by one unit vector `y` with `−⟨y,h_C⟩ = |h_C|` does not decrease the
objective and does not change the other copies.  Doing this for one `C` after the other gives an optimal
configuration that is constant on the copies of every vertex.  ∎

**Lemma (right-angle triangle) [P; X].**  For unit vectors `p, q` with `t = ⟨p,q⟩`,

```
g(t)  :=  max_{|r| = 1}  − [ 12 ⟨p,q⟩ + 15 ⟨r,p⟩ + 20 ⟨r,q⟩ ]  =  5 √(25 + 24t) − 12t   ≤   25 − t² ,
```

with equality only at `t = 0`.  (The weights `12 = 3·4`, `15 = 5·3`, `20 = 5·4` are those of the blow-up of a triangle
with multiplicities `3, 4, 5`: an antiferromagnetic triangle with these multiplicities has its optimum at
`3p + 4q + 5r = 0`, a right angle between `p` and `q`.)

*Proof.*  The maximum over `r` is `|15p + 20q| = 5√(25+24t)`.  As `25 + 12t − t² ≥ 12 > 0` on `[−1,1]`, the inequality is
equivalent to `25(25 + 24t) ≤ (25 + 12t − t²)²`, i.e. to `0 ≤ t²(94 − 24t + t²)`.  ∎

**Proposition 1a (exact lifting) [K as a hardness statement — §7; this identity and proof P; N].**  Let `H` have `n`
vertices and maximum degree `Δ ≥ 1`, let `k ≥ 1` and `L ≥ 4.5(k+1)Δ`.  Let `H'` be the blow-up of the graph with
vertices `U_v` (`v ∈ V`; multiplicity 3), `Z_l` (`l = 1,…,L`; multiplicity 4), `R_{v,l}` (multiplicity 5) and edges
`U_vU_w` for `vw ∈ E`, `U_vZ_l`, `R_{v,l}U_v`, `R_{v,l}Z_l` for all `v, l`.  Then `H'` is a simple graph with `3n + 4L + 5nL`
vertices, and

```
OPT_{k+1}(H')  =  25·n·L  +  9·OPT_k(H) .
```

*Proof.*  By the two lemmas, `OPT_{k+1}(H')` is the maximum over unit vectors `u_v, z_l ∈ ℝ^{k+1}` of
`−9 Σ_E ⟨u_v,u_w⟩ + Σ_{v,l} g(⟨u_v,z_l⟩)`.
*Lower bound.*  `z_l = e_{k+1}` for all `l` and `u_v = (x_v, 0)` with `x` optimal for `H` in `ℝ^k`.
*Upper bound.*  Let `M = Σ_l z_l z_l^T`, a positive semidefinite matrix of order `k+1` and trace `L`, and `f` a unit
eigenvector for its largest eigenvalue `λ_1 ≥ L/(k+1)`.  By the lemma,
`Σ_{v,l} g(⟨u_v,z_l⟩) ≤ 25nL − Σ_v u_v^T M u_v ≤ 25nL − λ_1 Σ_v s_v²` with `s_v = ⟨u_v, f⟩`.  Write `u_v = s_v f + q_v`,
`q_v ⟂ f`, `|q_v| ≤ 1`.  Then `−Σ_E ⟨u_v,u_w⟩ = −Σ_E s_vs_w − Σ_E ⟨q_v,q_w⟩`.  The first sum is at most
`½ Σ_E (s_v² + s_w²) ≤ (Δ/2) Σ_v s_v²`.  The second is a function of the `q_v` — vectors in the unit ball of the
`k`-dimensional space `f^⊥` — that is affine in each `q_v` separately; replacing one `q_v` after the other by a
maximiser on the sphere shows that it is at most its maximum over unit vectors, `OPT_k(H)`.  Together:
`≤ 25nL + 9·OPT_k(H) + (9Δ/2 − L/(k+1)) Σ_v s_v²`, and the bracket is `≤ 0`.  ∎

**Consequence [K].**  Starting from Max-Cut on simple graphs (`k = 1`) and applying the proposition `k − 1` times
gives, for every fixed `k`, a polynomial-time reduction of Max-Cut to the threshold problem for `OPT_k` on simple
unweighted graphs (the degree of the polynomial grows with `k`: `|V(H')| ≈ 22.5(k+1)nΔ` and `Δ(H') ≥ 8n`); the
thresholds to be distinguished differ by `2·9^{k−1}`.  So vector Max-Cut in `ℝ^k` is NP-hard
for every fixed `k` — the theorem of Piddock (and of Kallaugher et al. for `k = 3`), obtained there with different
gadgets and, in Piddock's case, with hardness of approximation, which our identity does not give by itself (the
additive term `25nL` dominates).  We do not know whether this exact identity, or the right-angle triangle with
multiplicities `3, 4, 5`, is in the literature, and claim no novelty for it.

**Remark (hardness of approximation for chains) [K-corollary].**  For a graph `G` on the bonds, the data `c` with
`Q̃_kl = −½` for adjacent `k ≠ l`, `Q̃_kl = 0` for the other pairs `k ≠ l`, and `Q̃_kk = deg(k)/2` give
`Σ c_ij |x_i − x_j|² = Σ_{kl ∈ E} (1 − ⟨b_k,b_l⟩)`, twice the vector Max-Cut value of `G` in `ℝ^3`.  By Piddock's
Theorem 3 (Max-Cut_3 is APX-complete; preprint, not yet peer reviewed as far as we know) there is a constant
`α < 1` such that approximating the maximum of CHAIN within the factor `α` is NP-hard.  With Theorem 3 below the
same holds for CHAIN(θ).

(`maxcut_k_lifting.py`: the inequality for `g` as a polynomial inequality on a rational grid [X]; the identity for
six small graphs from `k = 1` to `2`, three from `2` to `3` and two from `3` to `4`: attained by the explicit
configuration and never exceeded by 26–41 numerical maximisations each [N]; with too few poles (`L = 1`) the same
test finds violations, as it should; and three explicit unweighted graphs `H'` with 132, 351 and 522 vertices
maximised over all their vertices without assuming that copies are equal [N].)

## 2b. Back to the question as asked: realizability of averaged data

The Geometry division's C1 asks whether given numbers `m_ij` are the averaged squared distances `⟨|x_i − x_j|²⟩` of
some ensemble (probability distribution) of chains; the optimisation problem above is its dual.

**Corollary 5 (complete data, freely jointed chains) [P, given K].**  Let `m = (m_ij)_{i<j}` be given for all pairs of
the `n` atoms, and put `m_ii = 0`.  An ensemble of freely jointed chains with `⟨|x_i − x_j|²⟩ = m_ij` for all `i < j`
exists if and only if `m_{i,i+1} = 1` for all `i` and the symmetric matrix `G(m)` of order `n − 1` with unit diagonal and

```
G_kl  =  ½ ( m_{k,l+1} + m_{k+1,l} − m_{k,l} − m_{k+1,l+1} )        (k < l)
```

lies in the convex hull `conv E_3` of the Gram matrices of `n − 1` unit vectors in `ℝ^3`.  Deciding this in the weak
sense (accept if `G(m)` is in the body, reject if it is at distance at least `δ` from it) is NP-hard under
polynomial-time Turing reductions when `δ` is part of the input, written in binary; and for `δ^{-1}` polynomial in
`n` provided the sharper reduction quoted at the end of the proof is as reported.

*Proof.*  `⟨b_k,b_l⟩ = ½(|x_k − x_{l+1}|² + |x_{k+1} − x_l|² − |x_k − x_l|² − |x_{k+1} − x_{l+1}|²)`, so the averaged Gram
matrix of the bonds of an ensemble is `G(m)`; conversely `m_ij = Σ_{k,l=i}^{j−1} G_kl` recovers `m` from a symmetric
matrix with diagonal `m_{k,k+1}`, so an ensemble whose averaged Gram matrix is `G(m)` has the data `m`.  The body
`conv E_3` is convex, contains the cross-polytope `{Σ|G_kl| ≤ 1}` (the matrix with a single off-diagonal pair `±1` is the
average of the cut matrices `xx^T` over the sign vectors with `x_k = ±x_l`), hence a ball of radius `C(n−1,2)^{−1/2}`
around `0`, and lies in the ball of radius `C(n−1,2)^{1/2}`.  For such bodies weak optimisation of linear functionals
reduces in polynomial time to weak membership [K: Grötschel, Lovász, Schrijver, *Geometric Algorithms and
Combinatorial Optimization*, the equivalence of weak membership and weak optimisation for centred well-bounded
convex bodies; cited from memory], and weak optimisation over `conv E_3` — maximising `Σ Q_kl G_kl`, to additive
accuracy `½`, for integer `Q` — is NP-hard by Theorem 1 (thresholds are integers).  That equivalence is
polynomial in the *encoding length* of the accuracy, so it gives the statement for `δ` in binary — possibly
exponentially small.  For polynomially small `δ` one needs a reduction with polynomial loss: for
`B(p,r) ⊆ K ⊆ B(0,R) ⊂ ℝ^m`, weak optimisation with error `ε` reduces to weak membership with error
`r³ε³ / (2¹³·3³·m⁵·R⁴·(R+r))` [K: Y.-K. Liu, thesis (2007), Proposition 2.8, as used by S. Gharibian, Quantum Inf.
Comput. 10 (2010) 343–360, arXiv:0810.4507 — found by the referee of REV-0006, who read a summary of Gharibian's
paper; **not read by us**].  With `m = C(n−1,2)`, `R = 1/r = √m` and `ε^{-1}` polynomial this error is
polynomially small.  ∎

(The first version claimed `δ^{-1}` polynomial on the strength of the first citation alone — REV-0006, finding 1.)

So C1 with complete data is hard for freely jointed chains although membership in `E_3` itself (one conformation)
is a rank computation: the difficulty is the convex hull.  (For a graph `F` of pairs given in the input, E.-Nagy,
Laurent and Varvitsiotis prove hardness of membership in `conv E_k(F)` directly, without the Turing reduction —
§7.)  For chains with a fixed bond angle the optimisation problem is hard as well (Theorem 3), but we have not
verified the technical conditions of the equivalence (the affine hull of the body and an inscribed ball), and do
not state the corollary for them.

## 3. Fixed bond angles do not help

**Lemma (free every `m`-th bond) [P].**  Let `θ ∈ (0,π)`, `ψ = min(θ, π − θ)` and `m = ⌈π/ψ⌉` (so `m ≥ 2`).  For any two unit
vectors `p, q` there are unit vectors `p = w_0, w_1, …, w_m = q` with `⟨w_i, w_{i+1}⟩ = cos θ` for all `i`.

*Proof.*  First let `θ ≤ π/2`, so `ψ = θ`.  We keep the invariant "the spherical distance `d` from the current point
to `q` is at most `rψ`, where `r ≥ 2` is the number of steps left"; it holds at the start because `mψ ≥ π`.  While
`r > 2`: if `r` is odd or `d > 2ψ`, step by `ψ` along a great circle towards `q` (any great circle through the point
if `d = 0` or `d = π`); the new distance is `|d − ψ| ≤ (r−1)ψ`.  Otherwise (`r ≥ 4` even, `d ≤ 2ψ`) step to any point
at distance `ψ` and back (two steps, the point is unchanged, `d ≤ 2ψ ≤ (r−2)ψ`).  When two steps are left, `d ≤ 2ψ`,
and a point at distance `ψ` from both ends of an arc of length `d ≤ 2ψ ≤ π` exists (at distance `φ` from the midpoint
of the arc, perpendicular to it, with `cos φ = cos ψ / cos(d/2)`; if `d = π`, then `ψ = π/2` and any point orthogonal
to the ends will do).  If `θ > π/2`, apply this with `ψ = π − θ` to `p` and `(−1)^m q`, and negate the points with odd
index: consecutive inner products become `−cos ψ = cos θ`.  ∎

(REV-0006, finding 8: the distinction by the parity of `r` is not needed — stepping towards `q` whenever more
than two steps remain already keeps `d ≤ rψ`; `m` is best possible, since `m − 1` steps stay within distance
`(m−1)ψ < π`; and the lemma is a special case of the classical closing condition for spherical polygons, which
the referee quotes from memory without a primary source.)

**Theorem 3 [P].**  For every fixed `θ ∈ (0,π)`, CHAIN(θ) is strongly NP-hard.

*Proof.*  Given `Q` on `N` spins, consider chains with `(N−1)m + 1` bonds and couplings only between the bonds
`1, 1+m, 1+2m, …` ("designated"), equal to `Q`.  By the Lemma, applied independently to each gap between consecutive
designated bonds, the designated bonds of fixed-angle chains range over all of `(S²)^N`.  So the maximum over
fixed-angle chains is the Heisenberg optimum of `Q`, and the data `c` are given by §1 (integers; a number of
non-zero data points proportional to the number of non-zero couplings).  ∎

(`heisenberg_reduction.py` parts 4, 5: the construction of the Lemma for six angles, and one instance end to end
— the triangle graph becomes a chain with 56 atoms and tetrahedral angles whose objective at the explicit
optimum equals the threshold 841.  The program takes `Q̃ = Q/2`, so that the objective is `F` and the data `2c`
are integers; with the integer data of §1 (`Q̃ = Q`) the objective is `2F` and the threshold 1682.)

## 4. Where it is easy: short-range data

**Proposition 4 [P].**  Suppose `c_ij = 0` whenever `j − i > w`, `w ≥ 2`.
(a) For collinear chains (`b_k = ±1`) the maximum is computed exactly in time `O(n·w·2^w)`.
(b) For chains with a fixed angle `θ` and every `ε > 0`, a chain whose value is within `ε·Σ_{k≠l}|Q̃_kl|` of the maximum
of CHAIN(θ) is computed in time `O(n·w·T^{w−1})`, `T = ⌈π(w−2)/ε⌉ + 1`.

*Proof.*  By §1 only bonds at distance less than `w` are coupled.  (a) Dynamic programming over the signs of the last
`w − 1` bonds.  (b) The inner products of `w` consecutive bonds are functions of the `w − 2` torsion angles between
them.  Restrict every torsion angle to the `T` multiples of `2π/T`, and run the dynamic programme whose state is the
last `w − 2` torsion angles: `O(n·T^{w−1})` transitions, each evaluating `O(w)` inner products.  Rounding the torsion
angles of an optimal chain to the grid changes each by at most `π/T`; changing one torsion angle by `δ` rotates the
part of the chain behind it by `δ` about a bond, which changes any `⟨b_k,b_l⟩` by at most `δ`; at most `w − 2` torsion
angles lie between two coupled bonds; so every coupled inner product changes by at most `(w−2)π/T ≤ ε`.  ∎

So the cost is governed by the range `w` of the data along the chain, exponentially, and not by the length `n`.

**Remark (the exponential dependence on `w` cannot be removed for the exact problem) [P, given K].**  The instance
of Theorem 1 has `5|V| + 4` spins, so a chain of length linear in `|V|` (also with fixed bond angles, by Theorem 3),
and `w` is at most the length.  Max-Cut has no algorithm of running time `2^{o(|V|)}` under the exponential time
hypothesis [K; a standard consequence of the sparsification lemma, cited from memory].  Hence, under that
hypothesis, no algorithm decides the threshold problem of CHAIN or CHAIN(θ) in time `2^{o(w)}·poly(n)`.  This says
nothing about approximation schemes with a different trade-off between `w` and `ε`.

## 5. What this means for software, and what it does not

* A routine that optimises **one** conformation of a chain against arbitrary pair data of this kind has no
  polynomial worst-case guarantee unless P = NP, with or without fixed bond angles, and (by Piddock's theorem) no
  polynomial-time approximation scheme either; the hard instances have long-range data.
* Structure that provably helps: short range along the chain (Proposition 4).  Structure known from the literature
  to help with approximation: a positive semidefinite coupling matrix (§7).
* Structure that does **not** help in the worst case: the linear order of the chain (§1), fixed bond angles
  (Theorem 3), integer data of polynomial size (strong NP-hardness), couplings of one sign (Proposition 1a:
  antiferromagnetic couplings on an unweighted graph suffice).
* Nothing is claimed about random or experimental data, about discrete torsion states, about steric exclusion, or
  about ensembles; and an NP-hardness result says nothing about the sizes at which an exact method stops being
  practical.  The value of a *given* conformation is trivial to check; what is hard is a certificate of
  optimality (an upper bound can be certified by the semidefinite relaxation, which is exact only in special
  cases).

## 6. Verification

`experiments/complexity/chain_geometry/heisenberg_reduction.py`: (1) the gadget inequality of §2 on a rational grid,
as a polynomial inequality [X]; (2) for six small graphs (19–29 spins), the formula of Theorem 1 is attained by the
explicit configuration, and 60 numerical maximisations from random starts never exceed it and reach it [N];
(3) the identity (1) and its inverse on 30 random chains; (4) the construction of the Lemma of §3 for
`θ = 70.5°, 60°, 90°, 109.5°, 35°, 150°` (deviation of the constructed angles below `10⁻¹³`); (5) an instance end to end.
`maxcut_k_lifting.py`: §2a, as described there.  Numerical maximisation from random starts can only fail to find
a violation; the proofs are the paper proofs above.

## 7. Prior art and limitations

| source | how inspected (2026-11-26) | what it contains for this note |
|---|---|---|
| J. Kallaugher, O. Parekh, K. Thompson, Y. Wang, J. Yirka, *Complexity classification of product state problems for local Hamiltonians*, arXiv:2401.06725v2 (January 2025; conference version reported as ITCS 2025) | abstract and §1 through a page-reading sub-agent (about a quarter of the text; its report read, not the paper) | Theorem 1.5: "MC_3 is NP-complete" (vector Max-Cut in `ℝ^3`, unit weights; by a reduction from 3-colouring); "it has been conjectured by Lovász that MC_k is NP-complete for all constants k≥1 … no proof has been given for any k>1"; product-state problems for all 2-local interaction sets, with couplings of both signs.  **This contains Theorem 1 of this note** (a product state of the Heisenberg interaction is a configuration of unit vectors in `ℝ^3`), after scaling the couplings; their Theorem 1.5 is for a promise version (a completeness value and a gap of order `m^{-2}`), and a footnote credits an earlier unpublished proof for product states of Quantum Max-Cut to J. Wright (2022) |
| S. Piddock, *Quantum Max-Cut is NP hard to approximate*, arXiv:2510.07995v1 (9 October 2025; preprint, no journal reference) | full text of v1 through a page-reading sub-agent (its report read, not the paper) | Theorem 3: "There is a PTAS reduction from Max-Cut_k to Max-Cut_{k+1}.  Therefore Max-Cut_k is APX-complete for all (constant) k≥1", on unweighted graphs; gadgets: unit triangles (which fix the angle `2π/3` to a reference vector) and a bipartite expander; "no other hardness results are known for k≠1,3" before it.  **This contains Proposition 1a as a hardness statement, and more** (hardness of approximation) |
| M. E.-Nagy, M. Laurent, A. Varvitsiotis, *Complexity of the positive semidefinite matrix completion problem with a rank constraint*, arXiv:1203.6602 | introduction through a page-reading sub-agent (its report read) | membership in the rank-`k` elliptope `E_k(G)` is NP-hard for `k ≥ 2`, **and so is membership in its convex hull** — the closest prior art for the realizability question with data on a graph of pairs; "It is believed that linear optimization over conv E_k(G) is also hard for any fixed k" — the question that the two papers above answer |
| L. Lovász, *Graphs and Geometry* (2019), p. 236 | **not read**; known through the two papers above | the conjecture that vector Max-Cut is NP-hard in every fixed dimension |
| J. Briët, F. de Oliveira Filho, F. Vallentin, the positive semidefinite Grothendieck problem with rank constraint | **from memory**, as in COMPLEXITY-RES-0002; cited by both papers above for the approximation algorithm | constant approximation ratios for positive semidefinite objectives |
| distance geometry of protein-like chains (Saxe 1979; Lavor, Liberti, Maculan and co-authors) | search summaries only | NP-hardness of the *feasibility* problem for exact distances; a different problem from the optimisation considered here |
| **fixed-angle chains** ("freely rotating chains"): M. Soss, G. Toussaint, J. Math. Chem. 27 (2000) 303–318; E. Demaine, S. Eisenstat, WADS 2011; E. Demaine, H. Ito, J. Lynch, R. Uehara, arXiv:2212.12450; N. Benbernou, J. O'Rourke, arXiv:0801.0258; C. Borcea, I. Streinu, *Extremal reaches in polynomial time*, SoCG 2011 | found by the referee of REV-0006 from search summaries and one abstract page; **full texts opened by nobody here** | flattening a fixed-angle chain and its minimum / maximum flat span are NP-hard (strongly, also for equal lengths); the maximum span in space is polynomial for equal angles; **the largest and smallest end-to-end distance of a chain in space with fixed lengths and angles are computed in polynomial time** (Borcea–Streinu).  The last is CHAIN(θ) with the single datum `c_{1n} = ±1`.  So the hardness of Theorem 3 comes from many pairs with data of both signs, not from the fixed angle.  According to the referee none of these papers contains Theorem 3 |

* Two searches on 2026-11-26 before the proofs were written found neither of the first two sources; a third and a
  fourth, aimed at "rank-constrained Grothendieck problem" and "vector Max-Cut", found them.  The order matters:
  for an hour the lifting of §2a looked like a proof of an open conjecture.  It is a second proof of a theorem
  of 2025.
* We claim: the translation to chains (§1, elementary), Theorem 3 (elementary), Proposition 4 (elementary), and
  self-contained derivations of known hardness results.  The referee of REV-0006 searched the literature on
  fixed-angle chains (row above) and for the lifting identity and the 3-4-5 triangle, and found neither Theorem 3
  nor the identity; searches only, which proves nothing.
* The referee's strongest objection, in its words: "Everything hard here is known.  The translation to chains is
  a change of variables.  Theorem 3 shows only that the model is unphysical: a phantom chain with couplings of
  both signs and of size `|E|` between every `m`-th bond, the fixed angle being bought off with `m − 1` idle bonds
  per spin."  (The objection continues with the two points repaired above: the uncited literature and the
  citation behind Corollary 5.)  We agree that the instances are artificial; the theorem is a worst-case
  statement about guarantees, not about typical data.
* Theorem 1 and Proposition 1a are threshold statements; membership in NP is not claimed (the optimum is
  irrational in general; Kallaugher et al. and Piddock treat this through additive accuracy).
* Reviewed internally once (COMPLEXITY-REV-0006: Theorem 1 on 11 further graphs with adversarial starts,
  Proposition 1a on 14 liftings up to dimension 5, the lemma of §3 on 6 420 cases, all identities); not peer
  reviewed.  The dynamic programme of Proposition 4 is not implemented.
