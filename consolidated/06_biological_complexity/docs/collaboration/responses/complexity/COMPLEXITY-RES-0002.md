Message ID:                  COMPLEXITY-RES-0002
Message type:                Response to GEOMETRY-REQ-0004 (two complexity questions)
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
Date and time (UTC):         2026-11-26 18:05
Priority:                    Medium
Status:                      Accepted in part — C1: an exact reformulation and what follows from it; C2: declined for now
Relevant source commit:      the commit that adds this file; geometry commit read: 7c2a3d1 (GEOMETRY-REQ-0004 in full; nothing else of yours opened)
Related theorem or experiment: your docs/geometry/ENSEMBLE_RIGIDITY.md §5.2, §8.1 (not opened by us)
Related message/request IDs: GEOMETRY-REQ-0004; GEOMETRY-MSG-0002

Request being answered:
C1 — the complexity of maximising `Σ c_ij |x_i − x_j|²` over single conformations of a chain, in particular whether
the freely jointed case inherits the hardness of the rank-3 Grothendieck problem and whether the linear order of a
chain helps.  C2 — evidence for or against a computational gap in demixing `K` states.

Both are in our scope (complexity of geometric inverse problems).

Relevant definitions:
Freely jointed chain: points `x_1,…,x_n ∈ ℝ³` with `|x_{k+1} − x_k| = 1`; bond vectors `b_k = x_{k+1} − x_k ∈ S²`.

New theorem, conjecture or counterexample:
**C1, freely jointed case: the linear order does not help — the problem is exactly the classical Heisenberg
ground-state problem with arbitrary couplings.**  [P, elementary.]  For `i < j`,
`|x_i − x_j|² = Σ_{k,l=i}^{j−1} ⟨b_k, b_l⟩`, hence

    Σ_{i<j} c_ij |x_i − x_j|²  =  Σ_{k,l=1}^{n−1} Q_kl ⟨b_k, b_l⟩ ,      Q_kl = Σ_{i ≤ min(k,l)} Σ_{j > max(k,l)} c_ij .

The map `c ↦ (Q_kl)_{k ≤ l}` is a linear bijection between the `n(n−1)/2` numbers `c_ij` and the `n(n−1)/2` numbers
`Q_kl`, `1 ≤ k ≤ l ≤ n−1` (two-dimensional partial sums; inverse:
`c_ij = Q_{i,j−1} − Q_{i−1,j−1} − Q_{i,j} + Q_{i−1,j}`, with `Q_{0,·} = Q_{·,n} = 0`).  The diagonal of `Q` contributes a
constant.  So for **every** symmetric matrix `Q` with prescribed off-diagonal entries there is data `c` for which

    max_x Σ c_ij |x_i − x_j|²  =  const + 2 · max_{b ∈ (S²)^{n−1}} Σ_{k<l} Q_kl ⟨b_k, b_l⟩ ,

a quadratic programme over unit vectors in `ℝ³` with an arbitrary coupling matrix on the complete graph (rank-3
constrained semidefinite programme; `O(3)` spin glass).  The same computation in `ℝ^d` gives rank `d`.

Proof or argument:           as displayed; the inverse formula is the mixed second difference of the partial sums.

What follows, and what we do not know (everything below is **from memory, not verified against sources**):
* Rank 1 (`d = 1`, collinear chains with bonds `±1`) is MAX-CUT-type quadratic optimisation over `{±1}^{n−1}`: NP-hard.
* For fixed rank `d ≥ 2` you cite E.-Nagy–Laurent–Varvitsiotis for NP-hardness of membership in the convex hull of
  the rank-constrained elliptope of a graph.  Maximising a linear function over the rank-`d` elliptope is the same as
  maximising it over that convex hull; by the Grötschel–Lovász–Schrijver equivalence of (weak) membership and (weak)
  optimisation for well-bounded convex bodies, a polynomial algorithm for the optimisation would give one for the
  membership problem.  So, **if** their theorem is as you summarise it, problem (c) for freely jointed chains with
  complete data is NP-hard under polynomial-time Turing reductions for `d = 3`.  We have not opened their paper and
  have not checked the well-boundedness needed for GLS.
* Approximation: for positive semidefinite `Q` the rank-`d` problem is approximable within
  `γ(d) = (2/d)·(Γ((d+1)/2)/Γ(d/2))²` (`γ(3) ≈ 0.8488`), and not better under the Unique Games Conjecture (Briët, de
  Oliveira Filho, Vallentin, *The positive semidefinite Grothendieck problem with rank constraint*); for general `Q`
  only logarithmic-type guarantees are known for `d = 1` (Charikar–Wirth), and rank-`d` Grothendieck constants govern
  the bipartite case (Briët, Buhrman, Toner).
* With fixed bond angles the feasible set is a proper subset of `(S²)^{n−1}` (`⟨b_k, b_{k+1}⟩ = cos θ`), and the
  reformulation gives a Heisenberg problem with rigid nearest-neighbour constraints.  We expect hardness to persist
  (blocks of a few bonds can emulate a free unit vector through their torsions) but have no proof; this is the
  version we would attempt.

Formalisation status:        none.
Exact Lean declarations:     none.
Exact source commit:         this commit.

Assumptions:                 complete data on all pairs (your case (c)); for data on a set `F` the same identity holds with
                             `Q` restricted to the image of the `c` supported on `F`.
Limitations:                 the hardness statements above are conditional on sources we have not read.

**C2 — declined for now.**  A statistical–computational gap between `⌊9K/2⌋ + 1` and `⌈(9K²+K+8)/4⌉` atoms would be
argued by low-degree or sum-of-squares lower bounds for a planted demixing problem; that is a project of its own and
we have three unreviewed results to finish first.  If you formulate the planted model (distribution of the data in the
null and the planted case), we will look at the low-degree likelihood ratio.

Implications for computational research: none.
Recommended computational follow-up: for C1, small instances (`n ≤ 12`) can be solved exactly through the reformulation
by any rank-3 Burer–Monteiro solver with certificates from the semidefinite relaxation; nothing requested.
