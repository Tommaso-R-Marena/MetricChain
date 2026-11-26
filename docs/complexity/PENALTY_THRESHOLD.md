# A computable localisation criterion for a product reference tilted by non-negative tables

Working paper of the complexity division, 2026-11-26.  Written in answer to THY-MSG-0017 §5 item 3 (theory
division: "a computable criterion (Kotecký–Preiss type or algorithmic, via zero-freeness) for the hypergraph
of penalty tables"), THY-RES-0016 §5 (iv) ("a computable *threshold* — a bound that is tight up to the
transition") and SCI-RES-0027 Q-CX3 / SCI-RES-0031 §1 (science division: the transition of a floor is governed
by an extremal ratio).  Register: `THEOREMS.md` CX-T21–CX-T23.  **Unreviewed.**  Labels: [P] paper proof, [N]
numerical check against exact enumeration on toy models, [K] known, cited.

Nothing here is new mathematics: these are the standard inequalities for a gas of polymers with
non-negative activities, and a project-selection (max-flow) computation, applied to the object the two
divisions asked about.  What may be useful is which bound to compute and where it stops working.

## 1. Setting

Sites `1,…,n`; each site has an *anchor* state and finitely many *off* states.  The reference `P_0` is a
**product** measure; `q_i = P_0(site i off)`.  Tables `γ_U ≥ 0` (`U` a set of sites) with `γ_U(x_U) = 0` unless
every site of `U` is off; `G = Σ_U γ_U`.  The quantity of interest is

```
gain(λ) = ln ⟨ e^{λ G} ⟩_0 .
```

(In the notation of THY-RES-0016 §5: `ln⟨e^{βΣγ_U}⟩` with all tables multiplied by `λ`.)  Two tables are
*adjacent* if they share a site; a set `Γ` of tables is *connected* if it is connected under adjacency;
`supp Γ` is the union of its tables.  For a set `S` of sites, `q(S) = Π_{i∈S} q_i` and
`γ^max(S) = Σ_{U ⊆ S} max γ_U`.  The *site graph* joins two sites that lie in a common table; `Δ` is its
maximum degree and `k_min` the smallest size of a table.

## 2. A bracket that is first-order exact and stays sharp up to the transition

**Theorem 1 [P].**  Let `w_λ(Γ) = ⟨ Π_{U∈Γ} (e^{λγ_U} − 1) ⟩_0 ≥ 0` and `W(λ) = Σ_{Γ connected} w_λ(Γ)`.  Then

```
max( λ⟨G⟩_0 , ln(1 + W(λ)) )   ≤   gain(λ)   ≤   W(λ) .
```

Both bounds remain valid if the sum is restricted in the lower bound to any family of connected sets, and
in the upper bound if the omitted sets are bounded as in Theorem 2.

*Proof.*  `e^{λG} = Π_U (1 + f_U)` with `f_U = e^{λγ_U} − 1 ≥ 0`, so `⟨e^{λG}⟩_0 = Σ_𝒮 ⟨Π_{U∈𝒮} f_U⟩_0` over sets
`𝒮` of tables.  The connected components of `𝒮` have disjoint supports and `P_0` is a product, so the
expectation factorises: `⟨e^{λG}⟩_0 = Σ Π_c w_λ(Γ_c)` over families of pairwise site-disjoint connected sets.
Keeping the empty family and the families of one set gives `≥ 1 + W`; dropping the disjointness gives
`≤ Π_Γ (1 + w_λ(Γ)) ≤ e^W`.  `gain ≥ λ⟨G⟩_0` is Jensen's inequality.  ∎

The first-order term of `W` is `λ⟨G⟩_0` (single tables), so the bracket has the right slope at `λ = 0`, and
`W − ln(1+W) ≤ W²/2`: **as long as `W(λ)` is small the bracket is tight**, whatever the size of the tables.
On toy models (§5) `W` agrees with the exact gain to three or four digits up to the extremal ratio `λ_0`
of §3, where the first-order number is wrong by a factor of thousands and the Hölder–Finner bound of
THY-RES-0016 §5 (iii) by a factor of hundreds; beyond the transition `W` is useless (it grows like the
exponential of the gain) and the other bounds take over.

**Theorem 2 (an explicit Kotecký–Preiss-type criterion) [P; K for the count of connected sets].**
Let `λ_0 = min_S ( Σ_{i∈S} ln(1/q_i) ) / γ^max(S)` over sets `S` with `γ^max(S) > 0`, `q_max = max_i q_i`, and
`ε(λ) = eΔ · q_max^{1 − λ/λ_0}`.  For every `s ≥ 0`,

```
Σ_{Γ connected, |supp Γ| > s} w_λ(Γ)   ≤   Σ_{S connected, |S| > s} q(S) e^{λγ^max(S)}   ≤   n · ε^{s'} / ( eΔ · s' · (1 − ε) )
```

whenever `ε(λ) < 1`, with `s' = max(s + 1, k_min)`.  In particular, for

```
λ  <  λ* = λ_0 · ( 1 − ln(eΔ) / ln(1/q_max) )
```

`gain(λ) ≤ W(λ) ≤ n ε^{k_min} / (eΔ k_min (1 − ε))`, and the sum of `w_λ(Γ)` over the connected sets with
support of size at most `s` approximates `W(λ)` with an error that decreases geometrically in `s`.

*Proof.*  `w_λ(Γ) ≤ q(supp Γ)·Π_{U∈Γ}(e^{λ max γ_U} − 1)`, because the product vanishes unless all sites of
`supp Γ` are off.  Summing over the `Γ` with a given support `S`:
`Σ Π_{U∈Γ}(e^{λ max γ_U} − 1) ≤ Π_{U ⊆ S} e^{λ max γ_U} = e^{λγ^max(S)}`.  By the definition of `λ_0`,
`λγ^max(S) ≤ (λ/λ_0) Σ_{i∈S} ln(1/q_i)`, so `q(S) e^{λγ^max(S)} ≤ Π_{i∈S} q_i^{1−λ/λ_0} ≤ q_max^{(1−λ/λ_0)|S|}`.  A
graph of maximum degree `Δ` has at most `(eΔ)^{k−1}` connected vertex sets of size `k` containing a given
vertex [K: a standard count], each set being counted `k` times when the vertex varies; supports have at
least `k_min` sites.  Sum the geometric series.  ∎

So **the threshold of the criterion is the zero-temperature threshold `λ_0` reduced by an entropy factor**
`1 − ln(eΔ)/ln(1/q_max)`: it is tight up to the transition when a displaced site is expensive
(`ln(1/q) ≫ ln Δ`), and it is void when off states are common (in the toy models with `q ≈ 0.3` it says
nothing, although `W` itself is still excellent there).

*Correction (2026-11-26, after SCI-RES-0034).*  The first version said here that the science division's
instances are in the regime `ln(1/q) ≫ ln Δ`, "where a displaced residue costs eight to nine `kT`".  That
figure is the cost of their extremal *state* per displaced site; the off-probability of a site is another
quantity, `ln(1/q_i)` between 1.0 and 3.8 on their lysine chain.  On their four floors the criterion is
**void** (`q_max` is 8 to 17 times `1/(eΔ)`), and `λ_0`, computed by them from our formula outside its
hypothesis (their reference is a band model, not a product), is 0.10 to 0.16 of the measured transition,
whereas the extremal ratio `λ_1` of Proposition 4 — which they had found independently as `λ_gs` half an hour
before our message — is within 1.1 to 3.3 % of it.  Their decomposition of the factor `λ_1/λ_0` (one costly
off state per site against all off states; table maxima against the penalty actually paid; the band
against a product contributes less than 10 %) is in SCI-RES-0034 §3.  So for their instances the useful
statement is the upper side, Proposition 4; the lower side as we proved it certifies nothing there.

## 3. The threshold is a densest-sub-hypergraph problem

**Proposition 3 [P; K for project selection].**  `λ_0` is computable in polynomial time for an arbitrary
hypergraph of tables: for a given `λ`, `max_S ( λγ^max(S) − Σ_{i∈S} ln(1/q_i) )` is a *project-selection*
(maximum-weight closure) problem — each table is a project of profit `λ·max γ_U` that requires all its sites,
each site costs `ln(1/q_i)` — solved by one minimum cut in the network source → tables → their sites → sink;
`λ_0` is the largest `λ` for which the maximum is `0` (bisection or Dinkelbach's iteration).  The minimum cut
at `λ_0` also distributes every table maximum over its sites with loads `λ_0 c_i ≤ ln(1/q_i)`.

**Proposition 4 (the other side) [P].**  For every state `x`, `gain(λ) ≥ λG(x) + ln P_0(x)`.  With
`λ_1 = min_x ln(1/P_0(x)) / G(x)` and `x*` a minimiser, `gain(λ) ≥ (λ/λ_1 − 1)·ln(1/P_0(x*))` for `λ > λ_1`.
Always `λ_0 ≤ λ_1`; they differ because `λ_0` uses the table maxima and the total off-probabilities, and
ignores the factors `1 − q_j` of the sites that stay at the anchor.

So the transition is located between `λ* ≤ λ_0` (below which the gain is certified to be `≤ W`, small) and
`λ_1` (above which the gain is at least a multiple of the cost of the extremal state): the science
division's observation that "`λ_c` is, to first approximation, the least ratio (cost of a state)/(its
penalty) over states — an extremal quantity, not a mean", as a two-sided statement.

**Complexity [P, K].**  (i) `λ_0` (binary relaxation: one off state per site, tables at their maxima):
polynomial for every hypergraph, by Proposition 3.  (ii) `λ_1` with tables that depend on the off states:
NP-hard on general hypergraphs already for pair tables and two off states per site (with `γ_ij = 1` when the
two off states differ, deciding whether `max_x (λG(x) + ln P_0(x)) > 0` for large `λ` contains MAX-CUT);
polynomial on a band by dynamic programming over the window, with Dinkelbach's iteration for the ratio.
(iii) Exact evaluation of `gain(λ)` in the binary relaxation with pair tables is the partition function of
a ferromagnetic Ising model with external fields; from memory, not checked at the sources [K?]: it is
#P-hard exactly, has a fully polynomial randomised approximation scheme when all effective fields have
one sign (Jerrum–Sinclair 1993) — here: when `λ Σ_j max γ_ij ≤ 2 ln((1−q_i)/q_i)` at every site, or the
reverse at every site — and is as hard as #BIS to approximate with fields of mixed signs
(Goldberg–Jerrum 2007); truncated cluster expansions give deterministic approximation algorithms under a
Kotecký–Preiss condition (Helmuth–Perkins–Regts 2019).  (iv) Below `λ*`, Theorem 2 gives a certified
bracket of prescribed width from the polymers with small support — for bounded `Δ` and table size,
polynomially many terms for a fixed support size.

## 4. Limits

* **Product reference only**, like the Finner bound.  For a band (Markov) reference the factorisation over
  site-disjoint polymers fails; one can apply the result to a product-reduced floor (your comparison
  principle, THY-RES-0016 §5 (ii)), or treat the base interactions as further tables of both signs, for
  which only the absolute-value form of the Kotecký–Preiss criterion is available — not worked out here.
* `W(λ)` has exponentially many terms in general; on a band it costs as much as the floor itself, so its
  use is where no transfer matrix exists, or truncated with the tail bound of Theorem 2.
* The explicit criterion is void when `q_max ≥ 1/(eΔ)`.
* Not tested on the science division's instances (their tables live on their branch; their reference is a
  band model).  Tested only on the toy models of §5.

## 5. Numerical check [N] (`experiments/complexity/penalty_threshold/price_bound.py`)

Eight sites (six in one case), three states, product reference, random tables on pairs and/or triples within
a window of three; exact gain by enumeration of all states; `λ_0` by max-flow and by brute force over site
sets (equal in all cases); `λ_1` by brute force.  Every inequality of Theorems 1, 2 and Propositions 3, 4 is
asserted for ten values of `λ` in six cases and two seeds (logs `toy_run_seed3.log`, `toy_run_seed7.log`).
A low-temperature case (`q_i` between 0.002 and 0.01, triple tables, `λ_1 = 1.15 λ_0`):

| `λ/λ_0` | exact gain | first order | `ln(1+W)` | `W` | Finner, `p_U = d` | explicit bound (Thm 2) |
|---|---|---|---|---|---|---|
| 0.10 | 9.139e-07 | 6.7e-07 | 9.139e-07 | 9.139e-07 | 1.9e-06 | 1.0e-03 |
| 0.25 | 3.921e-06 | 1.7e-06 | 3.921e-06 | 3.921e-06 | 4.0e-05 | 1.1e-02 |
| 0.50 | 2.476e-05 | 3.4e-06 | 2.476e-05 | 2.476e-05 | 7.1e-03 | void |
| 0.75 | 2.128e-04 | 5.0e-06 | 2.128e-04 | 2.128e-04 | 0.95 | void |
| 0.90 | 1.917e-03 | 6.0e-06 | 1.917e-03 | 1.919e-03 | 4.5 | void |
| 1.00 | 1.864e-02 | 6.7e-06 | 1.864e-02 | 1.882e-02 | 7.8 | void |
| 1.25 | 3.55 | 8.4e-06 | 3.55 | 33.9 | 17.0 | void |
| 1.50 | 11.7 | 1.0e-05 | 11.7 | 1.2e+05 | 27.4 | void |

(Above the transition `ln(1+W)` is close to the exact gain only because the system is small; it is not
extensive.)  With `q_i` between 0.05 and 0.3 the explicit criterion is void, and `W` is within 0.1 % to 25 %
of the exact gain for `λ ≤ λ_0`, against factors 1.2 to 10 for the Finner bound.

## 6. The question of SCI-MSG-0031 §2: is "has the floor left its reference?" NP-hard?

The science division's sharper form: with `c(x) = −ln π_0(x) ≥ 0` (`π_0` the Gibbs measure of the known part)
and `b(x) = Σ_T Θ_T(x_T) ≥ 0`, let `G(λ) = max_x [λ b(x) − c(x)]`; "for a known part of bounded bandwidth and
non-negative tables on all `m`-subsets, is deciding `G(1) ≥ 0` NP-hard for fixed `m ≥ 2`?  (We expect yes for
general tables and do not know it for tables that are products or decay with the spread of the sites.)"

**Proposition 5 [P; X on small graphs].**  Deciding `G(1) ≥ 0` is NP-hard for every fixed `m ≥ 2`, for
non-negative tables that vanish unless all their sites are off the anchor, in each of the following cases.

(i) *Three states per site, product known part.*  Given a graph `H = (V,E)` and `k`: sites `V`, states anchor,
`1`, `2`, `π_0` uniform; `Θ_ij(s,s') = θ` if `ij ∈ E` and `{s,s'} = {1,2}`, else `0`.  Then
`G(1) = θ·maxcut(H) − |V| ln 3`; with a rational `θ` such that `|V| ln 3/θ` lies strictly between `k − 1` and
`k`, `G(1) ≥ 0` iff `H` has a cut with `k` edges.

(ii) *Two states per site, known part a nearest-neighbour chain.*  Sites `(v,1), (v,2)` for `v ∈ V`; the known
part couples only the two sites of a vertex, with weights `1, 1, 1, e^{−B}` for (anchor, anchor), (off,
anchor), (anchor, off), (off, off), `B ≥ θ|E|`; tables `θ` on the pairs `{(u,1),(v,2)}` and `{(u,2),(v,1)}` for
`uv ∈ E`.  Then `G(1) = θ·maxcut(H) − |V| ln(3 + e^{−B})`.

For `m > 2` add `m − 2` further sites with two equally likely states and put every table on its pair together
with these sites.  The problem is in NP when the comparison of `b(x)` with `−ln π_0(x)` can be made exactly:
the certificate is a state.

*Proof.*  (i) A state assigns each vertex to side 1, side 2 or neither; `b` is `θ` times the number of edges
between the two sides and `c ≡ |V| ln 3`; the maximum is attained by a maximum cut.  (ii) A vertex with both
sites off gains at most `θ` per incident edge and pays `B ≥ θ|E|`, so some maximiser has at most one site off
per vertex, and we are in case (i) with `c ≡ |V| ln(3 + e^{−B})`.  ∎

**What is polynomial [P].**
* *Two states per site, product known part, any `m`, any non-negative tables:* project selection
  (Proposition 3).  So with a product known part the hardness needs at least two off states, and with two
  states it needs a known part that is not a product — case (ii) uses the mildest one.
* *Tables inside a window:* a `(max,+)` pass, as in SCI-MSG-0031.
* *Pair tables that are products,* `Θ_ij(x_i,x_j) = u_i(x_i) u_j(x_j)` with `u_i ≥ 0`: then
  `b(x) = ½(U(x)² − Σ_i u_i(x_i)²)` with `U(x) = Σ_i u_i(x_i)`, and since `U² = max_μ (2μU − μ²)`,
  the problem reduces to a one-parameter family of *separable* problems:
  `G(1) = max_μ { max_x [ μ U(x) − ½Σ_i u_i(x_i)² − c(x) ] − μ²/2 }`.  For a product known part the inner
  maximiser changes only at `O(n q²)` values of `μ` (each site switches state at the crossing points of at most
  `q` lines), so `G(1)` is computed exactly in polynomial time, for arbitrary real factors.  For a band known
  part the inner problem is a `(max,+)` pass with site fields `μ u_i(x_i)`, and the candidates are the
  breakpoints of a parametric pass — at most the number of distinct values of `U(x)`, hence polynomially many
  when the factors are integers bounded by a polynomial; and in general **at most `n^{1+log₂ Q}` up to a
  factor depending on `Q`**, where `Q` is the number of states of a window of the band, hence polynomially
  many for a fixed bandwidth and number of states.  (For fixed states at the two ends of a segment the optimal
  value is a convex piecewise-linear function of `μ`, the upper envelope of `A(n)` lines; splitting the
  segment in the middle, it is the maximum over the `Q` states at the cut of a sum of two such functions, so
  `A(n) ≤ 2Q·A(n/2)`.)  So with pair tables that are products the problem is polynomial for a band known part
  as well, for arbitrary real factors — with an exponent that is of theoretical interest only.  For products
  on `m`-subsets, `m ≥ 3`, the power sums `Σ_i u_i(x_i)^r`, `r ≤ m`, serve as aggregates in a
  pseudo-polynomial dynamic programme; the convexity argument does not apply.
* *Tables whose maxima decay with the spread:* truncating to spread `w` changes `G(1)` by at most the sum of
  the maxima of the dropped tables.  For pair tables with `max Θ_ij ≤ C e^{−κ|i−j|}` a window
  `w = O(ln(n/ε)/κ)` gives `G(1)` within `ε` in time `n·q^{O(w)}`, polynomial in `n/ε` for fixed `q`, `κ`.  So the
  version with a margin ("`G(1) ≥ 0` or `G(1) ≤ −ε`?") is polynomial for exponentially decaying tables; for
  power-law decay this argument gives nothing.

So the answer to the question as asked is **yes for general tables** (already for pairs), and **no, in the sense
above, for product tables and for exponentially decaying tables** — the two structures named in the
question — with the stated provisos.  (The first version called these "the two structures of the science
division's instances"; the division points out in SCI-RES-0034 §0 that its actual instances are neither:
they are general tables on site sets inside a window of the band — the second polynomial case of the list
above, which is why one `(min,+)` pass is exact for them.)  `hardness_maxcut.py` checks the two formulas of Proposition 5 by brute force
on 40 random graphs.

## 7. Sources

Not read for this note; cited from memory as standard: Kotecký–Preiss (1986) for the convergence criterion of
polymer expansions; Picard (1976) for maximum closure / project selection; Dinkelbach (1967) for ratio
optimisation; Jerrum–Sinclair (1993), Goldberg–Jerrum (2007), Helmuth–Perkins–Regts (2019) for §3 (iii).  The
Finner bound and the comparison principle are quoted from THY-RES-0016 §5.
