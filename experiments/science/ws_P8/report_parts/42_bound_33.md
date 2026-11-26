### 3.3 The sharper forms: statements and proofs

**Notation (P3's, with the host state written out).**  `X = ∏_i X_i`, anchor `x⁰`, `S(x) = {i : x_i ≠ x⁰_i}`.
Every atom `p` has a *host* `l(p)` (the site it moves with; none for a fixed atom).  A **term** `τ` is
a pair term `t_pq = −κ q_p q_q h(ℓ_p + ℓ_q; r_pq)` (`p < q`) or a self term `t_pp = −(κ/2) q_p² b_p`;
`g = Σ_τ τ`; `𝓗(τ)` is its set of hosts (0, 1 or 2 sites; two atoms of one side chain have one).
For an atom `p` and a state `b` of its host (P3's "instance"; `gfbound.GFBound.per_state`):
`[I⁻, I⁺]_{p,b}` contains `I_p(x)` for all `x` with `x_{l(p)} = b`;
`δ^{p,b}_i ≥ max_{y∈X_i} |C^{p,b}_i(y) − C^{p,b}_i(x⁰_i)|` for `i ≠ l(p)`, where `I_p = const + Σ_{i≠l(p)} C^{p,b}_i(x_i)` on
`{x_{l(p)} = b}` (P3's structural fact);
`Bd^{p,b}_k ≥ sup |b_p^{(k)}|`, `L^{p,b}_k ≥ sup |ℓ_p^{(k)}|` over that hull, `[ℓ⁻, ℓ⁺]_{p,b} ⊇ ℓ_p(hull)`; and for two atoms in
host states `c = (b, b′)`: `H^c_k ≥ sup{|∂_w^k h(w; r)| : w ∈ [ℓ⁻_{p,b} + ℓ⁻_{q,b′}, ℓ⁺_{p,b} + ℓ⁺_{q,b′}]}`, `r = r_pq` in those states.
For a host-state assignment `c = (c_l)_{l∈𝓗(τ)}` and a set `B` of sites, `B ∩ 𝓗(τ) = ∅`, `B ≠ ∅`:

```
Θ_c(τ; B) :=  (κ/2) q_p² Bd^{p,c}_{|B|} ∏_{i∈B} δ^{p,c}_i                                                              (τ = t_pp),
Θ_c(τ; B) :=  κ|q_p q_q| Σ_{π∈Part(B)} H^c_{|π|} ∏_{β∈π} ( L^{p,c}_{|β|} ∏_{i∈β} δ^{p,c}_i + L^{q,c}_{|β|} ∏_{i∈β} δ^{q,c}_i )        (τ = t_pq).
```

**Lemma T [K: this is P3's Theorem 3 for one term, exactly as P3's proof gives it; proof repeated].**
*Let `τ` be a term, `T ⊆ [n]` with `T ∖ 𝓗(τ) ≠ ∅`, `z ∈ X` with `z_T = x⁰_T`, `y_T ∈ X_T`.  Let `𝒞(T; z, y)` be the set
of assignments `c` with `c_l = z_l` for `l ∈ 𝓗(τ) ∖ T` and `c_l ∈ {x⁰_l, y_l}` for `l ∈ 𝓗(τ) ∩ T`.  Then*

```
|Δ_T τ(z; y_T)|  ≤  Σ_{c ∈ 𝒞(T; z, y)}  Θ_c(τ; T ∖ 𝓗(τ)).
```

*Proof.*  For `l ∈ T`, `Δ_T F(z; y_T) = Δ_{T∖l} F|_{x_l = y_l} − Δ_{T∖l} F|_{x_l = x⁰_l}` (the definition of the mixed
difference; P3's Remark L3).  Applying this to each host in `T` writes `Δ_T τ(z; y_T)` as a signed sum
over `c ∈ 𝒞(T; z, y)` of `Δ_B τ_c(z; y_B)`, `B = T ∖ 𝓗(τ)`, where `τ_c` is `τ` with its hosts held at `c` (hosts
outside `T` are at `z_l` in all `2^{|T|}` evaluations).  For fixed `c` the distance `r_pq` is a constant
and `I_p`, `I_q` are sums of one-site functions of the sites of `B`, with all values in the hulls of
the states `c`.  For a self term, P3's Corollary L1 (`φ = b_p`) gives
`|Δ_B b_p(I_p)| ≤ sup|b_p^{(|B|)}| ∏_{i∈B} |C_i(y_i) − C_i(x⁰_i)| ≤ Bd_{|B|} ∏ δ_i`.  For a pair term, P3's Lemma 2 with
`Ψ(u_1, u_2) = h(u_1 + u_2; r)`, `u_1 = ℓ_p∘I_p`, `u_2 = ℓ_q∘I_q` gives
`|Δ_B h| ≤ Σ_π sup|h^{(|π|)}| ∏_{β∈π} (D_β(u_1) + D_β(u_2))` with `D_β(u_1) ≤ L^p_{|β|} ∏_{i∈β} δ^p_i` by L1 at every vertex
(Corollary L2).  ∎

**Proposition S [not new as a bound: P3's Theorem 3 without the merging step of P3's closed form —
see "what is whose" below; checked against exact constants, §3.4].**  Call a set `𝔅` of terms with one
common host set `𝓗` a *block* (a single term is a block).  For `|T| = m ≥ 3` put

```
Θ^S_𝔅(T)  :=  max_u  Σ_{c ∈ 𝒞_u(T)}  Σ_{τ∈𝔅}  Θ_c(τ; T ∖ 𝓗),
```

*the maximum over `u = (u_l)_{l∈𝓗}` with `u_l ∈ X_l` for `l ∉ T` and `u_l ∈ X_l ∖ {x⁰_l}` for `l ∈ T`, where `𝒞_u(T)` is the
set of `c` with `c_l = u_l` (`l ∉ T`) and `c_l ∈ {x⁰_l, u_l}` (`l ∈ T`).  Then*

1. *for all `z` (with `z_T = x⁰_T`) and `y_T`:  `Σ_{τ∈𝔅} |Δ_T τ(z; y_T)| ≤ Θ^S_𝔅(T)`;*
2. *for every partition `𝒫` of the terms into blocks, `ĉ^{S,𝒫}_T := Σ_{𝔅∈𝒫} Θ^S_𝔅(T) ≥ c_T^anch(g_s)` for every sign
   pattern `s` of the charges (`g_s` as in P5's Proposition 7); a finer partition gives a larger
   number; every one of them is at most P3's `ĉ_T`, summand by summand;*
3. *hence (P3's Proposition 1) `|g(x) − I_{m−1} g(x)| ≤ Σ_{T ⊆ S(x), |T| = m} ĉ^{S,𝒫}_T` for every `x`.*

*Proof.*  1: Lemma T for each `τ ∈ 𝔅`; all terms of a block have the same `𝒞(T; z, y)`, namely `𝒞_u(T)`
with `u_l = z_l` (`l ∉ T`), `u_l = y_l` (`l ∈ T`); if `y_l = x⁰_l` for some `l ∈ T` the left side is zero.  2: sum
over the blocks, triangle inequality; only `|q_p q_q|` and `q_p²` enter `Θ`; a maximum of a sum is at
most the sum of the maxima; and each `Θ_c` is non-decreasing in every ingredient, while P3's types
take, ingredient by ingredient, the maximum over all states (X), over the non-anchor states (N) or
the anchor's value (A), so `Σ_{c∈𝒞_u} Θ_c(τ; ·)` is at most P3's sum over the corresponding types.  ∎

Two partitions are used below: singletons (variant **S**: the maximum is taken pair by pair —
validated term by term) and P3's own blocks (variant **Sb**: self terms of one side chain; pairs
"fixed atom–side chain `l`" together with pairs inside `l`; pairs between two side chains).

**Theorem AH (anchored hosts) [P; I did not find it in P3, P5 or P6; checked at every state for
every pair term, §3.4].**  *Define `Θ^{SA}_𝔅(T)` as `Θ^S_𝔅(T)` with `u_l := x⁰_l` for the hosts `l ∉ T` (no maximum over
the states of a host outside `T`), and `ĉ^{SA,𝒫}_T := Σ_{𝔅∈𝒫} Θ^{SA}_𝔅(T)`.  Then for every `x ∈ X`, every `m ≥ 3` and
every block `𝔅`*

```
Σ_{τ∈𝔅} |τ(x) − I_{m−1} τ(x)|  ≤  Σ_{T ⊆ S(x), |T| = m} Θ^{SA}_𝔅(T),        hence        |g(x) − I_{m−1} g(x)|  ≤  Σ_{T ⊆ S(x), |T| = m} ĉ^{SA,𝒫}_T .
```

*The same holds with P3's types in place of the state-wise maximum (host outside `T`: type A; host
in `T`: types A + N): `ĉ^{AH}_T`, whose sum over all `T` is P3's closed form with "X" replaced by "A".*

*Proof.*  (a) *P3's Proposition 1 holds for every total order `≺` of the sites:*
`F(x) − I_{m−1}F(x) = Σ_{T ⊆ S(x), |T| = m} Δ_T F(z^{T,x}; x_T)`, `z^{T,x}_i = x_i` if `i ≺ min_≺ T` and `x⁰_i` otherwise.  (P3's
proof: `F − I_{m−1}F = Σ_{U ⊆ S, |U| ≥ m} d_U`; send `U` to the set `T` of its `m` largest elements; then
`U = T ∪ U′` with `U′ ⊆ {i ∈ S : i ≺ min T}`, each pair `(T, U′)` arises once, and the inner sum over `U′` is
`Δ_T F(z^{T,x}; x_T)` by the context expansion.  Nothing in it uses which order is meant; P3 itself uses
the statement "with site `i` placed last" in its §3.7.)  The interpolant `I_{m−1}` does not depend on
the order and is linear in `F`.
(b) Fix a term `τ` and take an order in which the hosts of `τ` are the last `|𝓗(τ)|` sites.  Let
`T ⊆ S(x)`, `|T| = m ≥ 3`, and `l ∈ 𝓗(τ) ∖ T`.  `T` has at least `m − 1 ≥ 2` elements outside `𝓗(τ)` (it can
contain at most the other host), and each of them precedes `l`; so `min_≺ T ≺ l`, i.e. **`z^{T,x}_l = x⁰_l`:
in all `2^m` evaluations of `Δ_T τ(z^{T,x}; x_T)` a host that is not in `T` sits in its anchor state.**
For `i ∈ T`, `z^{T,x}_i = x⁰_i`, so Lemma T applies with `z = z^{T,x}`, `y_T = x_T`: `𝒞(T; z, y) = 𝒞_u(T)` with
`u_l = x⁰_l` (`l ∉ T`) and `u_l = x_l ≠ x⁰_l` (`l ∈ T ⊆ S(x)`).  Hence
`|τ(x) − I_{m−1}τ(x)| ≤ Σ_{T ⊆ S(x)} |Δ_T τ(z^{T,x}; x_T)| ≤ Σ_{T ⊆ S(x)} Σ_{c∈𝒞_u(T)} Θ_c(τ; T∖𝓗)`.
(c) All terms of a block have the same hosts, so the same order serves them and `u` is the same
for all of them at a given `x` and `T`; summing over `τ ∈ 𝔅` and taking the maximum over the `u_l`,
`l ∈ 𝓗 ∩ T`, gives the first inequality; summing over the blocks and using `g = Σ_τ τ`,
`I_{m−1} g = Σ_τ I_{m−1} τ` gives the second.  The statement with P3's types follows by monotonicity
as in Proposition S.  ∎

*What Theorem AH does **not** say.*  `ĉ^{SA}_T` is not a bound of the anchored constant `c_T^anch(g)`,
which takes the supremum over **all** contexts: it bounds the mixed differences that occur in the
remainder identity when each term is expanded in its own order.  (Measured: on Lys₅ the summand
of `ĉ^{SA}_T` is *below* the exact all-context constant of the term in 26 190 of 120 048 cases, and
never below the exact constant with the hosts outside `T` at the anchor — §3.4.)  What the
certificate needs is exactly the displayed inequality — hypothesis (H1) of P6's report — so P3's
Theorem 5, P6's Lemmas A, A′ and Proposition P6.1 and the coordinator's window models apply to
the new constants word for word.

*What is whose.*  Lemma T is P3's Theorem 3.  **The state-wise maximum of Proposition S is in P3's
record**: its report §2.3 lists two computable forms — "class mode (`termwise.TermBound`, per
subset) … hosts outside `T`: maximum over the host state, taken block by block …" and "anchored
mode (`gfbound.GFBound`) … type X (all ingredients maximised over its states) … type A plus type N" —
and `ws_P3/termwise.py` takes the maximum over host states of the bound, block by block, with an
anchored branch.  P3 used it only in class mode at order 3 (its comparison with P2's constants);
its single-term sharpness test ran `GFBound` on Val₅ and Ser₄ (at most nine states and four moving
atoms per site), where the merging costs little; and every certificate and every `Γ_m` since —
P3's own, P5's, P6's, the coordinator's tables — uses the closed form `GFBound`, because only it
sums over all subsets without enumerating them.  What is new here: (i) the measurement that this
merging step, not the far pairs, is where the bound loses for lysine (§3.2) — a factor 19, 57,
165 at twelve residues at orders 4, 5, 6 for the block-wise state-wise maximum alone ('Sb'; §3.5);
(ii) Theorem AH, which adds little at twelve residues (20, 60, 172 with it) and more for short
chains and for hosts outside `T` (table T3); (iii) that the subsets *can* be enumerated at
twelve residues (0.1 s each) with an evaluation that needs no sum over set partitions (below);
(iv) validation term by term and state by state against exact constants.

*How the constants are computed* (`ws_P8/p8sr.py`; a subclass chain of P3's `GFBound`, P3's
directory untouched).  Every ingredient is P3's own, per host state (`GFBound.site[l].per_state[b]`,
`GFBound._supH_states`), so the interval enclosures, the table allowance and the final
outward-rounding factor `1 + 10⁻⁹` are unchanged; the only new arithmetic is sums and products of
non-negative doubles and maxima.  For one free set `B`, `|B| = s`,
`Σ_π H_{|π|} ∏_β (L^p ∏δ^p + L^q ∏δ^q) = Σ_{a+b=s} e_{a,b}(B) · M_{a,b}`, `M_{a,b} = Σ_{r₁,r₂} H_{r₁+r₂} Bell_{a,r₁}(L^p) Bell_{b,r₂}(L^q)`
(P3's Proposition 4 restricted to the sites of `B`: `e_{a,b}(B)` is the coefficient of `u^a v^b` in
`∏_{i∈B} (u δ^p_i + v δ^q_i)`); the `M_{a,b}` do not depend on `B` and are cached for all pairs of host states,
so a subset costs `O(s²)` array operations per block.  Variant 'P3' of the same code (P3's types)
reproduces P3's own summands to `10⁻¹⁵` on every enumerated instance and P3's closed-form `Γ_m`
of the twelve-residue peptides to `2·10⁻¹⁵` (§3.4, §3.5); variant 'Sb' reproduces P3's
`termwise.TermBound` in anchored mode to `10⁻¹⁵` on every subset of the enumerated instances
(check B5 of §3.4) and on a sample of sixteen subsets at twelve residues (§3.5; there 0.4–0.9 s
per subset including the set-up of the caches, where P3's set-partition sum takes 1.0–2.8 s; in
the full runs 0.07–0.10 s per subset).  There is no closed form over `T` for the state-wise
maximum (the maximum is inside the sum); `Σ_T ĉ^{AH}_T` has one (`AHBound.total_ah`).
