## 1. The statements, with proofs

**Setting (workstream P3's and P8's notation; nothing is changed).**  `X = ∏_i X_i`, anchor `x⁰`,
`S(x) = {i : x_i ≠ x⁰_i}`, `X*_U := ∏_{i∈U} (X_i ∖ {x⁰_i})` for a set `U` of sites.  `g = Σ_τ τ` is the sum
of the self terms `t_pp` and pair terms `t_pq` of the solvent energy; `𝓗(τ)` is the set of hosts
of `τ` (0, 1 or 2 sites); a *block* `𝔅` is a set of terms with a common host set `𝓗` (P8's
blocks: self terms of side chain `l`; pairs "fixed atom – `l`" and pairs inside `l`; pairs
between `l` and `l′`; and the two blocks without a host).  `I_{m−1}` is the anchored interpolant
of order `m − 1`.  For an atom `p` and a state `c` of its host, P3's per-state data
(`gfbound.GFBound.per_state`) are: the hull `[I⁻, I⁺]_{p,c}` of `I_p` over **all** states of the
other sites, the derivative suprema `Bd^{p,c}_k`, `L^{p,c}_k` over that hull, the range of `ℓ_p`,
and for two atoms in host states `c = (b, b′)` the kernel suprema `H^c_k` at the distance `r_pq`
of those states.  On `{x_{l(p)} = c}`, `I_p = const + Σ_{i≠l(p)} C^{p,c}_i(x_i)` (P3's structural
fact).  The **increment** of site `i` for atom `p` is

```
δ^{p,c}_i(y) := |C^{p,c}_i(y) − C^{p,c}_i(x⁰_i)|  (+ P3's table allowance),      δ̄^{p,c}_i := max_{y∈X_i} δ^{p,c}_i(y)   (P3's δ^{p,c}_i).
```

For a host-state assignment `c` on `𝓗(τ)`, a non-empty set `B` of sites with `B ∩ 𝓗(τ) = ∅`
and `y_B ∈ X_B`:

```
Θ_c(τ; B; y_B) := (κ/2) q_p² · Bd^{p,c}_{|B|} · ∏_{i∈B} δ^{p,c}_i(y_i)                                                            (τ = t_pp),
Θ_c(τ; B; y_B) := κ|q_p q_q| Σ_{π∈Part(B)} H^c_{|π|} ∏_{β∈π} ( L^{p,c}_{|β|} ∏_{i∈β} δ^{p,c}_i(y_i) + L^{q,c}_{|β|} ∏_{i∈β} δ^{q,c}_i(y_i) )     (τ = t_pq),
```

and `Θ̄_c(τ; B)` the same with every `δ(y_i)` replaced by `δ̄` — P8's `Θ_c(τ; B)`, which does not
depend on `y_B`.  `Θ_c ≤ Θ̄_c` (every ingredient is non-negative and `Θ` is non-decreasing in each).

### Lemma T′ [K: P3's Theorem 3 for one term, as P3's proof gives it — with the increments P3's Corollary L2 is stated with]

*Let `τ` be a term, `T ⊆ [n]` with `B := T ∖ 𝓗(τ) ≠ ∅`, `z ∈ X` with `z_T = x⁰_T`, `y_T ∈ X_T`, and
`𝒞(T; z, y)` the set of assignments `c` with `c_l = z_l` for `l ∈ 𝓗(τ) ∖ T` and `c_l ∈ {x⁰_l, y_l}` for
`l ∈ 𝓗(τ) ∩ T`.  Then*

```
|Δ_T τ(z; y_T)|  ≤  Σ_{c ∈ 𝒞(T; z, y)}  Θ_c(τ; B; y_B)   ≤   Σ_{c ∈ 𝒞(T; z, y)}  Θ̄_c(τ; B).
```

*Proof.*  P8's Lemma T, read with the increments that occur.  For a host `l ∈ T`,
`Δ_T F(z; y_T) = Δ_{T∖l} F|_{x_l=y_l} − Δ_{T∖l} F|_{x_l=x⁰_l}` (P3's Remark L3); applied to every host in
`T` this writes `Δ_T τ(z; y_T)` as a signed sum over `c ∈ 𝒞(T; z, y)` of `Δ_B τ_c(z; y_B)`, `τ_c` being
`τ` with its hosts held at `c`.  For fixed `c`, `r_pq` is constant and `I_p`, `I_q` are constants
plus sums of one-site functions `C^{p,c}_i`, `C^{q,c}_i` of the sites of `B`, with all values in the
hulls of the states `c` **whatever the other sites do**.  The mixed difference `Δ_B` from `z_B =
x⁰_B` to `y_B` involves each site `i ∈ B` in exactly two states, `x⁰_i` and `y_i`.  P3's Corollary L1
(`|Δ_B φ(u)| ≤ sup|φ^{(|B|)}| ∏_{i∈B} |a_i(y_i) − a_i(z_i)|` for `u = c + Σ_i a_i(x_i)`) gives the self
term with `a_i = C^{p,c}_i`; P3's Corollary L2 gives the pair term, and it is *stated* with
`δ^p_i := |C^p_i(y_i) − C^p_i(z_i)|` ("the change of the contribution of site `i` to `I_p`", P3_REPORT
§2.2): `D_β(ℓ_p) ≤ L^p_{|β|} ∏_{i∈β} δ^p_i` at every vertex, because the increment of an additive
function does not depend on the vertex.  The second inequality is monotonicity.  ∎

*What is whose.*  Nothing in Lemma T′ is new mathematics: P3's theorem is a statement with the
actual increments; P3's computable forms (`gfbound`, `termwise`) and P8's (`p8sr`) take `δ̄`.  I
re-derived L1, L2, L3 from P3_REPORT §2.2 (one page) and did not find an evaluation with the
actual increments in P3, P5, P6 or P8 (searched: `ws_P3/gfbound.py` line 110 and `termwise.py`
line 128 take `…max(axis=0)` over the states of the non-host site; `ws_P8/p8sr.py`, `p8lib.py` and
P6's `p6lib.py` use that array; P8's exploration `x01_ff_proto.py` likewise; P5's `s2_family.py`
uses single increments only for two-state sites, where they coincide).

### Theorem R (the remainder bound, resolved by state) [P; checked at every state, block by block, §2]

*For `|T| = m ≥ 3`, a block `𝔅` with host set `𝓗`, and `y_T ∈ X*_T` define*

```
Θ²_{𝔅,T}(y_T) := Σ_{c ∈ 𝒞_y(T)} Σ_{τ∈𝔅} Θ_c(τ; T∖𝓗; y_{T∖𝓗}),          Θ¹_{𝔅,T}(y_T) := Σ_{c ∈ 𝒞_y(T)} Σ_{τ∈𝔅} Θ̄_c(τ; T∖𝓗),
𝒞_y(T) := { c :  c_l = x⁰_l  (l ∈ 𝓗 ∖ T),   c_l ∈ {x⁰_l, y_l}  (l ∈ 𝓗 ∩ T) },          Θ^s_T := Σ_𝔅 Θ^s_{𝔅,T}     (s = 1, 2).
```

*(`Θ¹` depends on `y_T` through the states of the hosts of the block that lie in `T`; `Θ²` through all
of `y_T`.)  Then for every `x ∈ X`, every `m ≥ 3`, every block and `s = 1, 2`*

```
Σ_{τ∈𝔅} |τ(x) − I_{m−1}τ(x)|  ≤  Σ_{T ⊆ S(x), |T| = m} Θ²_{𝔅,T}(x_T)  ≤  Σ_{T ⊆ S(x), |T| = m} Θ¹_{𝔅,T}(x_T),
hence      |g(x) − I_{m−1}g(x)|  ≤  Σ_{T ⊆ S(x), |T| = m} Θ^s_T(x_T).                                                   (R)
```

*Proof.*  Steps (a) and (b) of P8's Theorem AH, word for word; step (c), the maximum, is not
taken.  (a) P3's remainder identity holds for every total order `≺` of the sites:
`F(x) − I_{m−1}F(x) = Σ_{T ⊆ S(x), |T| = m} Δ_T F(z^{T,x}; x_T)`, `z^{T,x}_i = x_i` if `i ≺ min_≺ T` and `x⁰_i`
otherwise; `I_{m−1}` does not depend on the order and is linear.  (b) For a term `τ` take an order
with the hosts of `τ` last.  For `T ⊆ S(x)` and a host `l ∉ T`: `T` has at least `m − 1 ≥ 2` elements
outside `𝓗(τ)`, all before `l`, so `z^{T,x}_l = x⁰_l`; and `z^{T,x}_i = x⁰_i` for `i ∈ T`.  Lemma T′ with
`z = z^{T,x}` and **`y_T = x_T`** gives `𝒞(T; z, y) = 𝒞_x(T)` and
`|Δ_T τ(z^{T,x}; x_T)| ≤ Σ_{c∈𝒞_x(T)} Θ_c(τ; T∖𝓗; x_{T∖𝓗})`.  Sum over `T ⊆ S(x)`, over the terms of the block
(same hosts, same order, same `𝒞_x(T)`), and over the blocks (`g = Σ τ`, `I_{m−1}g = Σ I_{m−1}τ`).  ∎

*Why the bound of `T` may depend on `x_T` at all.*  In the identity of step (a) the term of `T` is
a mixed difference **between `x⁰_T` and `x_T`**: each site of `T` occurs in its anchor state and in
its *actual* state, in no other.  The sites outside `T` occur only through the context `z^{T,x}`,
and every ingredient is a supremum over all contexts.  P8's constant is the maximum over `y_T` of
(a block-wise majorant of) `Θ¹_T(y_T)`; nothing forces that maximum.

**Corollary J (state-independent constants) [P].**  `ĉ^{J,s}_T := max_{y_T ∈ X*_T} Θ^s_T(y_T)` satisfies the
hypothesis of the pipeline, `|g − I_{m−1}g|(x) ≤ Σ_{T⊆S(x)} ĉ^{J,s}_T`, and
`ĉ^{J,2}_T ≤ ĉ^{J,1}_T ≤ ĉ^{SAb}_T` (P8's constant is the sum over the blocks of the block-wise maxima
of `Θ¹_{𝔅,T}`; a maximum of a sum is at most the sum of the maxima).

### Proposition P (tables) [P; elementary — the generalisation of P3's site form and P6's Lemmas A, A′ to state-dependent shares]

*Let `Φ_T : X*_T → [0, ∞)`, `|T| = m`, satisfy `|g − I_{m−1}g|(x) ≤ Σ_{T ⊆ S(x)} Φ_T(x_T)` for all `x`
(Theorem R: `Φ = Θ¹` or `Θ²`).*

*(a) Allocation.  For every `T` let `w_{T,U} ≥ 0`, `∅ ≠ U ⊆ T`, with `Σ_U w_{T,U} = 1`.  Put*

```
c_{T,U}(b_U) := max{ Φ_T(y_T) : y_T ∈ X*_T, y_U = b_U }      (b_U ∈ X*_U),
γ_U(b_U) := Σ_{T ⊇ U} w_{T,U} c_{T,U}(b_U)   for b_U ∈ X*_U,        γ_U(b_U) := 0   if some b_i = x⁰_i.
```

*Then `Σ_{T ⊆ S(x)} Φ_T(x_T) ≤ Σ_U γ_U(x_U)` for every `x`.*

*(b) Reduction.  Let `γ : X_U → [0, ∞)` vanish unless all sites of `U` are off the anchor, and
`λ_V ≥ 0`, `∅ ≠ V ⊊ U`, `Σ_V λ_V = 1`.  With `γ^{→V}(b_V) := max{ γ(b_V, y_{U∖V}) : y_{U∖V} ∈ X*_{U∖V} }` for
`b_V ∈ X*_V` and `0` otherwise:  `γ(x_U) ≤ Σ_V λ_V γ^{→V}(x_V)` for every `x`.*

*Proof.*  (a) Let `T ⊆ S(x)`.  Then `x_T ∈ X*_T`, **and for every `U ⊆ T` the actual `x_T` is one of
the points over which the maximum `c_{T,U}(x_U)` is taken, because the coordinates of `U` are held
at their actual values**; so `Φ_T(x_T) ≤ c_{T,U}(x_U)` for each `U`, and with the weights
`Φ_T(x_T) ≤ Σ_{U⊆T} w_{T,U} c_{T,U}(x_U)`.  Summing over `T ⊆ S(x)` and exchanging the sums,
`Σ_{U ⊆ S(x)} Σ_{T : U ⊆ T ⊆ S(x)} w_{T,U} c_{T,U}(x_U) ≤ Σ_{U ⊆ S(x)} γ_U(x_U) = Σ_U γ_U(x_U)`: the inequality
adds the non-negative terms of the `T ⊄ S(x)`, the equality uses `γ_U(x_U) = 0` for `U ⊄ S(x)`.
(b) If `U ⊄ S(x)` the left side is `0`.  Otherwise `x_{U∖V} ∈ X*_{U∖V}` is admissible in every maximum.  ∎

*The one line the brief asks for.*  A table `γ_i(x_i)` is a valid penalty for a set `T ∋ i`
because `c_{T,i}(x_i)` is a maximum over the states of the **other** sites of `T` at the actual
state of `i`, and the actual state `x_T` is among them; a state-independent constant is the
same maximum taken over `x_i` as well.

*What each table maximises over.*  `c_{T,U}(b_U)`: over the non-anchor states of the sites of
`T ∖ U`.  Inside `Φ_T` itself: stage 1 — the increments of every site of `T` *as a non-host site*
are maximal over all its states, including the sites of `U` (a site of `U` is resolved only as
a host); stage 2 — nothing; both stages — hosts outside `T` at the anchor (Theorem AH), all
derivative suprema and hulls over all contexts.

*The forms used below* (each is (a), followed by (b) where a tuple does not fit the band).
`w` is the band; "in band": `|i − j| ≤ w`; "in window": `max − min ≤ w`.

| form | (a): tuples and weights | (b): what does not fit |
|---|---|---|
| **S** site | `U = {i}`, `w_{T,i} = 1/m`: `γ_i(b) = (1/m) Σ_{T∋i} c_{T,i}(b)` | — |
| **B** banded pair | all pairs of `T`, weight `1/C(m,2)` | a pair beyond the band: one half of `max_{b_j} γ_ij(·, b_j)` to site `i`, one half of `max_{b_i} γ_ij(b_i, ·)` to site `j` |
| **T** banded triple | all triples of `T`, weight `1/C(m,3)` | a triple outside the window: one third of its maximum over each of its sites to the pair of the two others; then the pairs as in B |
| **W** window | one tuple per `T`, weight 1: `T` itself if it fits a window, else one maximal sub-tuple of `T` that fits | — |

With `Φ_T ≡ ĉ_T` forms S, B, T are P3's site form and P6's Lemmas A and A′ (their proofs are
the case of constant tables), and W is an allocation in the sense of the theory division's
Proposition 11.18f (any sub-tuple of `T` may be charged: `[T ⊆ S(x)] ≤ ∏_{i∈K}[x_i ≠ x⁰_i]`), which
workstream P8 estimated to first order ("least-occupied in-window sub-tuple", its §4.1) and
which, by the reports I read (P8 §4.1; addendum A17 (17)–(18)), had not been run as a bracket;
the choice of the sub-tuple is guided by an uncertified Gibbs sample and does not affect
validity.  In B and T the reduction (b) is applied to the *summed*
table `γ_U`, which is at least as tight as applying it subset by subset (a maximum of a sum is
at most the sum of the maxima); with constant tables the two coincide.

**Corollary S (the sandwich) [P].**  If `pen(x) := Σ_U γ_U(x_U)` is built by Proposition P from a `Φ`
of Theorem R, then `|g − I_{m−1}g|(x) ≤ pen(x)` pointwise, so the coordinator's window models with
`∓(pen + P6's floating-point allowances)` in place of `∓(state-independent penalties + allowances)`
satisfy `m₋ ≤ E ≤ m₊` on all of `X`: their validity argument (P3's Theorem 5; `window_model.py`,
docstring) uses the penalty only through that pointwise inequality.  Every table entry is
multiplied by P3's factor `1 + 10⁻⁹`: an entry is a sum of at most `C(n, m)` maxima of values of
`Φ_T`, each of them a sum of non-negative doubles that P8's code has already rounded up by the
same factor; the relative rounding error of such sums is orders of magnitude below `10⁻⁹`.
