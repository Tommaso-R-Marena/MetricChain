# Certified brackets for many weak pair terms on a correlated reference: what can be computed, and what cannot be certified

Complexity division, 2026-11-26/27.  **Unreviewed.**  Register: `THEOREMS.md` CX-T35, CX-T36.  Written in answer to
question Q-5 of the Structural & Computational Biology division (STRUCTBIO-REQ-0003) and to items C-1 to C-3 of the
Frontier Benchmarking division (`MATHEMATICAL_FEEDBACK.md` on their branch); it also bears on the theory division's
classification question (THY-MSG-0017 §5, item 2).  Labels: [P] paper proof, [X] exact or exhaustive computation,
[K] known and cited.  **Nothing here is new mathematics**: §2 is the martingale method of concentration theory with
the observation that its coefficients are computable for a tree-decomposable reference; §4 is a standard argument
from the hardness of approximating Max-Cut.  Sources are cited from memory and were not consulted (§7).

## 0. Summary

Setting (Q-5): finitely many sites with finite state spaces, an energy `E = E_0 + V`; the *reference* `E_0` has a
tree decomposition of small width, so that its partition sum `Z_0` and its conditional laws are computed exactly by
elimination; `V = Σ_e ε_e(x_i, x_j)` is a sum over `m` *weak pairs* with oscillations `o_e = max ε_e − min ε_e`.
`⟨·⟩_0` is the average under the reference at inverse temperature `β`.  One wants a certified enclosure of

```
ln Z − ln Z_0  =  ln ⟨ e^{−βV} ⟩_0 ,          known:   −β⟨V⟩_0  ≤  ln⟨e^{−βV}⟩_0  ≤  −β⟨V⟩_0 + β² (Σ_e o_e)² / 8 .
```

1. **Theorem 1** [P; X on toy models] — *yes, certified bounds of second order in the individual `o_e` exist and are
   computable by elimination*: for any order of the sites,
   `ln⟨e^{−βV}⟩_0 ≤ −β⟨V⟩_0 + (β²/8) Σ_t R_t²`, where `R_t` bounds the range of the `t`-th increment of the Doob
   martingale of `V`; and `R_t ≤ Σ_e Γ_{t,e} o_e` with an influence matrix `Γ` whose entries are total-variation
   distances between conditional laws of the reference — the form `β²‖Γo‖²/8` asked for.  There is a sharper
   "column form" and a "variance form".
2. **But** [X]: the `Γ`-form counts a pair at both of its sites and can be *worse* than the trivial bound when the
   weak pairs are dense; with exact ranges the bound is 6 to 9 times better than the trivial one on toy models and
   still 2 to 6 times above the true excess, which is close to `β² Var_0(V)/2`.  No bound of this family is tight
   to second order.
3. **Theorem 2** [P, given K] — *the other direction*: unless NP = co-NP, there is no certificate of polynomial size
   for an upper bound on `ln Z` within a constant fraction of `β Σ_e o_e` on a family with trivial reference, bounded
   degree, equal weak pairs and `β o_e` a fixed constant.  So a certificate that works for every instance must
   lose first order once `β` times the oscillation per site exceeds a constant; below a constant, certified
   schemes exist.
4. §5: what is known about the Frontier division's questions (why real instances close without search; the
   threshold `K = n` for the cheap ensemble certificate; interval end-points as a function of the graph of
   observed pairs).

## 1. Setting and notation

Sites `1,…,n`, revealed in this order; `x_{<t} = (x_1,…,x_{t−1})`.  `μ_0 ∝ e^{−βE_0}`.  `M_t = ⟨V | x_1,…,x_t⟩_0`
(`M_0 = ⟨V⟩_0`, `M_n = V`), `D_t = M_t − M_{t−1}`.  For a history `x_{<t}` let

```
R_t(x_{<t})  =  max_a M_t(x_{<t}, a) − min_a M_t(x_{<t}, a)        (a over the states of site t possible after x_{<t}).
```

For a weak pair `e` and a site `t`:

```
Γ_{t,e}  =  0     if both sites of e come before t ,
         =  1     if t is a site of e ,
         =  max over x_{<t}, a, a' of  TV( law of the sites of e after t | x_{<t}, a ;  the same | x_{<t}, a' )     otherwise.
```

## 2. Upper bounds of second order

**Theorem 1 [P].**
(a) *(exact ranges)*  `ln⟨e^{−βV}⟩_0 ≤ −β⟨V⟩_0 + (β²/8) Σ_t ( sup_{x_{<t}} R_t )²`.
(b) *(`Γ`-form)*  `sup R_t ≤ Σ_e Γ_{t,e} o_e`, hence `ln⟨e^{−βV}⟩_0 ≤ −β⟨V⟩_0 + (β²/8) Σ_t ( Σ_e Γ_{t,e} o_e )²`.
(c) *(column form)*  With `U_e(a) = max_b ε_e(a,b)`, `L_e(a) = min_b ε_e(a,b)` for a pair `e ∋ t` (`a` the state of `t`):
`sup R_t ≤ [ max_a Σ_{e∋t} U_e(a) − min_a Σ_{e∋t} L_e(a) ] + Σ_{e∌t} Γ_{t,e} o_e`, which is at most the bound of (b).
(d) *(variance form)*  If `v_t ≥ Var(D_t | x_{<t})` and `b_t ≥ −D_t` for every history, then
`ln⟨e^{−β(V−⟨V⟩_0)}⟩_0 ≤ Σ_t v_t (e^{βb_t} − 1 − βb_t)/b_t²`.

*Proof.*  (a) Given `x_{<t}`, the increment `D_t` has mean zero and lies in an interval of length `R_t(x_{<t})`;
by Hoeffding's lemma `⟨e^{−βD_t} | x_{<t}⟩_0 ≤ e^{β²R_t²/8}`.  Conditioning successively on `x_{<n}, x_{<n−1}, …`
gives `⟨e^{−β(V − ⟨V⟩_0)}⟩_0 ≤ Π_t e^{β² sup R_t²/8}` (Azuma–Hoeffding).  (d) is the same with Bennett's inequality
`⟨e^{λX}⟩ ≤ exp(v(e^{λb} − 1 − λb)/b²)` for a centred `X ≤ b` of variance at most `v`, applied to `X = −D_t`, `λ = β`.
(b) `M_t = Σ_e ⟨ε_e | x_{≤t}⟩_0`, so `R_t` is at most the sum over `e` of the oscillation in `a` of
`⟨ε_e | x_{<t}, x_t = a⟩_0`.  If both sites of `e` precede `t`, this is `ε_e` at revealed states: no dependence on
`a`.  If `t` is a site of `e`, the conditional mean is a value or an average of values of `ε_e`: oscillation at most
`o_e`.  Otherwise it is the mean of a function of oscillation at most `o_e` (in the not yet revealed sites of `e`)
under two conditional laws, and `|∫f dP − ∫f dQ| ≤ osc(f)·TV(P,Q)`.  (c) For `e ∋ t` the conditional mean at state
`a` lies in `[L_e(a), U_e(a)]`, and a sum of functions with these envelopes has range at most
`max_a ΣU_e(a) − min_a ΣL_e(a) ≤ Σ_e o_e`.  ∎

**Computability.**  Under the reference, the not yet revealed sites are independent of `x_t` given the rest of the
history unless they lie in a connected piece of the unrevealed part that is adjacent to `t` in the graph of `E_0`;
and the law of such a piece depends on the history only through its boundary.  For an order that follows a tree
decomposition of `E_0` these boundaries lie in bags, so every `Γ_{t,e}` — a maximum over the configurations of one
bag of a total-variation distance between two marginal laws — is computed exactly by elimination, in time
polynomial in `n`, `m` and `d^{width}`.  Any *upper* bound on a `Γ_{t,e}` keeps the theorem valid, so the
coefficients can be certified by the same rules that certify `Z_0`.  The exact ranges of (a) and the quantities
`v_t`, `b_t` of (d) depend on the history through all earlier weak neighbours; computing their suprema exactly is a
maximisation over configurations (hard in general), but bounding them from above term by term is what (b), (c) do.

**What the forms are worth [X].**  `experiments/complexity/certified_brackets/martingale_bound.py` computes everything
by exhaustive enumeration on random models (tree references with strong tables, random weak pairs; 6 to 14 sites,
2 or 3 states).  All inequalities hold in all 42 models (two seeds: 84).  Medians of the excess over `−β⟨V⟩_0`,
as a fraction of the excess of the trivial bound `β²(Σo_e)²/8`:

| regime | exact ranges (a) | column form (c) | `Γ`-form (b) | variance form (d), exact suprema | true excess / bound (a) |
|---|---|---|---|---|---|
| dense weak pairs on 6–10 sites, strongly correlated reference | 0.16 | 0.81 | **1.03** | 0.12 | 0.18 |
| sparse weak pairs on 9–14 sites, weakly correlated reference | 0.11 | 0.37 | 0.47 | 0.14 | 0.50 |

In every model the true excess is close to `β² Var_0(V)/2`.  So: the `Γ`-form is valid but not automatically an
improvement — a pair is counted at both of its sites, and when few sites carry many pairs `Σ_t(Σ_{e∋t}o_e)²`
exceeds `(Σ_e o_e)²`; centring the pair tables (so that the conditional mean at the first revealed site is flat)
and the column form help; exact ranges help more; and all forms pay the price of replacing a variance by a squared
range (or by a supremum of conditional variances).  A bound that is tight to second order would have to certify
`Var_0(V)` itself plus a third-order remainder; we do not have one.

## 3. Where the reference's correlations enter

The entries `Γ_{t,e}` for `t ∉ e` are the cost of correlation: for a product reference they vanish and (b) becomes
`(β²/8) Σ_t (Σ_{e∋t} o_e)²` — the form `β² Σ_i c_i²/8` of item (c) of Q-5, with the factor from double counting.  For a
correlated reference the same form with `Γ` omitted is false (the theory division's D14, as quoted in Q-5), and
`Γ` is exactly the correction: a row of `Γ` that is not small says that revealing one site moves the conditional
law of many others, and then no bound of second order *in the individual `o_e`* can hold, because `V` behaves like
one collective variable.  This is the martingale method for dependent variables [K: Kontorovich and Ramanan 2008;
Chazottes, Collet, Külske and Redig 2007 — from memory].

## 4. What cannot be certified

**Theorem 2 [P, given K].**  There are constants `Δ`, `κ`, `δ > 0` with the following property.  Consider the
instances with binary sites, reference `E_0 = 0`, and `V = J Σ_{ij ∈ E(G)} σ_iσ_j` for a graph `G` of maximum degree
`Δ` without isolated vertices — so all `m = |E(G)|` weak pairs are equal, `o_e = 2J` — at `βJ = κ`.  If for every such
instance there were a certificate of size polynomial in `n`, checkable in polynomial time, of an upper bound
`U ≥ ln Z` with `U − ln Z ≤ δ·β·Σ_e o_e`, then NP = co-NP.

*Proof.*  `Z = Σ_σ e^{βJ(2·cut(σ) − m)}`, so `βJ(2·maxcut − m) ≤ ln Z ≤ n ln 2 + βJ(2·maxcut − m)`.  By the PCP theorem
there are constants `s < c` and `Δ` such that it is NP-hard to distinguish graphs of maximum degree `Δ` with
`maxcut ≥ c·m` from those with `maxcut ≤ s·m` [K: Max-Cut is APX-hard on graphs of bounded degree, Papadimitriou
and Yannakakis 1991; from memory].  Put `δ = (c − s)/2` and `κ = 3 ln 2/(c − s)`.  In an instance with
`maxcut ≤ s·m` a certificate as assumed proves `ln Z ≤ n ln 2 + βJ(2s − 1)m + 2δβJm`, which is less than
`βJ(2c − 1)m` because `n ≤ 2m` and `2 ln 2 < 2κ(c − s − δ) = 3 ln 2`; in an instance with `maxcut ≥ c·m` no valid
upper bound is below `βJ(2c − 1)m`.  So the certificate, with the inequality `U < βJ(2c−1)m`, would be a
polynomial proof that `maxcut < c·m`, placing an NP-hard promise problem in co-NP.  ∎

Reading: in this family the first-order scale is `β Σ_e o_e = 2κm`, and the per-site quantity `β c_i = β Σ_{e∋i} o_e`
is at most `2κΔ`, a constant.  So **no certificate format — whatever its rules — can give enclosures of width
`o(β Σ o_e)` on all instances with bounded `β c_i`, unless NP = co-NP.**  The statement is about the worst case over
instances and about upper bounds (a lower bound is certified by exhibiting configurations).  It says nothing
about a particular protein.  In the opposite regime, `β c_i` below a small constant, deterministic polynomial-time
approximation schemes for `ln Z` exist (convergent cluster expansions and correlation-decay algorithms [K, from
memory]; our `PENALTY_THRESHOLD.md` gives a bracket of this kind for product references), and they are
certificates.  The threshold between the regimes is a constant value of `β c_i`; where real instances sit is an
empirical question for the software divisions (the table of STRUCTBIO-REQ-0003 gives `β Σ_e o_e`, not `max_i β c_i`).

## 5. On the Frontier Benchmarking division's questions

* **C-1, "why are real fixed-sequence instances easy, and can it be predicted?"** [K, from memory.]  An instance of
  the pairwise minimisation problem closes without branching exactly when the dual bound of the basic linear
  relaxation (the local polytope; "optimal soft arc consistency") is tight after the eliminations.  That is a
  *checkable instance property computable in polynomial time before any search*: solve the linear programme (or
  its dual) and compare with the value of any rounding.  It is guaranteed for trees and for submodular tables,
  and more generally characterised for classes of tables by Thapper and Živný (the basic relaxation is exact for a
  class of cost functions iff the class has symmetric fractional polymorphisms of all arities); for single
  instances, stability conditions explain tightness (Lang, Sontag, Vijayaraghavan).  Dead-end elimination and
  "persistency" are the partial versions.  So a benchmark can be stratified in advance by the *integrality gap of
  the basic relaxation after elimination*; instances with gap zero cannot separate methods on search.  We have
  not examined any instance ourselves.
* **C-2, the cheap ensemble certificate.**  For uniformly random states the threshold is exactly `K = n`: for
  `K ≤ n − 1` the span contains no other sign vector — the degree-2 certificate exists — with probability
  `1 − 4·C(K,3)(3/4)^n` up to smaller terms [K: Odlyzko 1988; Irmatov 2024; `ISING_GROUND_SETS.md` §5], and for `K ≥ n`
  the span is everything (random sign matrices are non-singular with overwhelming probability [K: Tikhomirov
  2020, from memory]) and it never exists.  At `K ≈ n` the leading failure term `4C(K,3)(3/4)^n` is `0.04` for
  `n = 50` and `2·10⁻⁷` for `n = 100`.  What degree 4 achieves for `n ≤ K ≲ n²/2` random states we do not know; CX-T25
  gives the degrees that are necessary beyond `n²/2` and `n³/6`.  *Interval end-points with pair data on a graph
  `G` of observed pairs* [K, from memory]: this is linear optimisation over the cut polytope of `G` (of the
  suspension of `G` if single-site averages are observed too).  It is polynomial when that graph has bounded
  treewidth, and when it has no `K_5` minor — there the cut polytope is described by the cycle inequalities
  (Barahona and Mahjoub 1986), which for observed single-site averages means `G` series-parallel; it is NP-hard
  for general graphs (Max-Cut).  For real states of a chain instead of signs the corresponding statement is
  `CHAIN_GEOMETRY_HARDNESS.md`.
* **C-3, hardness at a fixed temperature.**  Open (`OPEN_PROBLEMS.md` A3′); we have no approach and no algorithm.

## 6. Verification

`python3 experiments/complexity/certified_brackets/martingale_bound.py [seed]` (17 s; log `martingale_bound.log` for
seed 1): exhaustive enumeration in floating point of the reference law, of all conditional laws, of `Γ`, of the
exact ranges and conditional variances; asserts `−β⟨V⟩_0 ≤ exact ≤` (d), `exact ≤` (a) `≤` (c) `≤` (b), and
`exact ≤` the trivial bound.  Theorem 2 has no program.

## 7. Prior art and limitations

* Every ingredient is standard and is cited **from memory, without consulting the sources**: Hoeffding's lemma and
  the Azuma–Hoeffding inequality; Bennett's inequality; the martingale method for dependent variables
  (Kontorovich–Ramanan; Chazottes–Collet–Külske–Redig); APX-hardness of Max-Cut on bounded-degree graphs
  (Papadimitriou–Yannakakis; the PCP theorem); the linear-programming facts of §5 (Barahona–Mahjoub;
  Thapper–Živný; Lang–Sontag–Vijayaraghavan); non-singularity of random sign matrices (Tikhomirov).  We claim no
  novelty.  The division's rule "search before a novelty statement" is satisfied trivially here because no
  novelty is stated; the references themselves should be checked by whoever relies on them.
* Theorem 1 is tested on toy models only, in floating point; it has not been run on a rotamer instance, and the
  efficient computation of `Γ` by elimination is described, not implemented.
* Theorem 2 concerns a family with trivial reference and equal antiferromagnetic pairs at one constant value of
  `βJ`; it does not say that rotamer instances are hard, and it does not exclude good certificates on instances
  with structure.
* Unreviewed.
