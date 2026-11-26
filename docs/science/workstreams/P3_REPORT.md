# Workstream P3 (science division) — a floor by analysis: certified constants of the GBn2 remainder, and a certified `ln Z` beyond enumeration size

Report of an independent workstream of the Scientific Discovery, Translation & Independent
Validation Division.  Branch `research/scientific-translation`.  Everything is in
`experiments/science/ws_P3/` (running notes: `NOTES.md`; logs: `logs/`; results: `out/`).
Written 2026-11-25/26.

Labels: **[P]** proved here (paper proof; I say whether and how it was checked numerically),
**[M]** measured on the named model with the stated protocol (exact unless stated),
**[N]** numerical evidence, **[K]** known and cited with reading level, **[C]** conjecture,
**[H]** heuristic, **[V]** machine-checked by the theory division (I cite its Lean name and did
not re-run Lean).  Units: kcal/mol; `k_BT = 0.596161 kcal/mol` (300 K); free energies in nats.
Every guarantee below is **model-relative**: it is a statement about a finite function defined
by OpenMM 8.6.1's ff14SB and GBn2 expressions on a rigid synthetic peptide with a three-state
grid per side-chain dihedral and a fixed ideal backbone.  No sequence was varied or optimised.

---

## How far I got

All four numbered items of the brief were carried out; of the optional item 5, part (a) is
done and part (b) (OBC2) is done on a small sample.  In order:

1. **Theorem with recipe** — done (§2): an exact remainder identity for the anchored
   expansion (Proposition 1), a chain rule for mixed differences (Lemma 2), a rigorous
   term-by-term bound on mixed differences of any order of the GBn2 energy (Theorem 3), its
   sum over *all* subsets of a given order in closed form (Proposition 4), certified floor and
   ceiling functions `m₋ ≤ E ≤ m₊` that are banded pairwise models (Theorem 5), and a
   floating-point error budget with interval enclosures of every derivative (§2.6).  All
   inequalities were checked against exact enumeration: no violation in any of the
   ⟨NVIOL⟩ enumerated states.
2. **How tight** — done, and the answer for *analysis alone* is negative (§2.8, §3.2): the
   third-order constants certified without any evaluation of `g` are **33–1 400 times** the
   constants P2 measured (apolar 200–1 400, polar and aromatic 40–170, charged 33–160).  The
   reason is identified and quantified.
3. **What the floor buys** — done (§3.3–3.4): `ρ`, the exact cost number `Z(m₋)/Z(E) − 1` and
   deterministic brackets for apolar, polar and charged peptides of 3–16 residues, for three
   truncation orders.
4. **One instance beyond enumeration** — done (§3.5): ⟨BIG⟩.
5. Optional (a) `Σ c_i²` — §3.6; (b) OBC2 — §3.7.

What I did **not** do is listed in the last section.

---

## 1. Verdicts in one paragraph

**Is a floor certifiable by analysis for the remainder P2 measured?  By analysis alone: yes,
rigorously, and uselessly; by analysis plus polynomially many evaluations: yes, and usefully
on extended backbones.**  (i) A bound on the third-order constants `c_ijk` of the GBn2
polarisation energy that uses only the descreening tables and derivative enclosures —
no evaluation of `g` at all — is proved here and is valid in all 562 triples of 44 of P2's
instances, but it exceeds the measured constants by a factor 200–1 400 for apolar side chains
(Val, Leu), 40–170 for Ser and Phe, 33–160 for Lys and the heteropolymer; the resulting
floor `f + I₂g − Σγ_i[x_i ≠ x⁰_i]` (P2's Statement 5(d) with certified constants) has
`ρ = 13–37 kcal/mol` already at 6–8 valines and a cost number `Z(m)/Z(g) − 1` of `10⁹–10¹³`:
it certifies nothing.  (ii) The loss has one cause: the cross term of GB is a sum over
`O(30 N)` atom pairs carrying `q_pq_q` of both signs that cancels to about 1 % (for Val₆: self
part −640, cross part +600, total −37 kcal/mol), and a term-by-term bound cannot see the
cancellation; the self part alone is bounded within a factor 0.5–30 of the measured total.  Every
analytic device that keeps signed sums at a reference point gains one factor of the small
parameter of the problem (the relative change of a Born radius under one rotamer flip) — and
that is exactly what one more order of the anchored expansion gains, with no loss at all.
(iii) Hence the recipe that works: **evaluate `g` exactly on the Hamming ball of radius
`m − 1` about an anchor** (`Σ_{j<m} C(n,j)(k−1)^j` evaluations, polynomial in `n`), and bound
only the remainder beyond order `m − 1` by the term-by-term bound, summed over *all* `m`-subsets
in closed form.  The certified remainder constant `Γ_m` falls by a factor 30–50 per order on
extended backbones (Val on strand, `n = 12`: `Γ₃, Γ₄, Γ₅, Γ₆ = 36.9, 1.56, 0.039, 0.0008`
kcal/mol), by 11–20 for Leu on strand and PPII, and only by 5–7 on the helix (Leu₁₆:
`1819, 370, 60, 8.0`), where the recipe fails at every order I could afford.
(iv) With `m = 4` or `5` the certified floor and ceiling are *banded pairwise functions*
`m₋ ≤ E ≤ m₊`; their partition functions are computed exactly by transfer matrix and bracket
`ln Z(E)` deterministically; sampling from `π_{m₋}` tightens the bracket with a bound valid at
every `N`.  ⟨VERDICT-NUMBERS⟩  (v) The theory division's formula is confirmed on real
numbers in the direction that matters: what decides feasibility is the certified floor, and a
floor that is a *function* (site penalties `γ_i`) is far cheaper than a constant (for Val₆ on
the strand the cost number falls from 1.07 to 0.008 at `m = 4`), because the Gibbs measure
rarely leaves the neighbourhood of the anchor.  What remains assumed in every statement: the
force field and the GB model themselves, the rotamer grid, the rigid geometry, the fixed
backbone; and that the peptides are small and solvent-exposed.

---

## 2. Precise statements

### 2.0 Setting and notation

**The function.**  `X = ∏_{i=1}^n X_i`, `X_i` the finite set of admissible rotamers of
residue `i` (P2's pruned product domain `X′` at clash threshold τ; my `p3core.pruned_domain`
reproduces P2's domain in all 24 comparisons).  `E = f + g`: `f` the ff14SB vacuum energy,
exactly `c₀ + Σ_i h_i(x_i) + Σ_{i<j} J_ij(x_i, x_j)` (P2 Statement 1; I use P2's tables);
`g` the GBn2 polarisation energy as OpenMM 8.6.1's `GBSAGBn2Force` defines it (read from
`openmm/app/internal/customgbforces.py`, [full text]).  With `r` in nm, `κ = 138.935485·(1 − 1/78.5)`
kJ nm/mol, atoms `p` with charge `q_p`, offset radius `or_p`, `rad_p = or_p + 0.0195141`,
scaled radius `sr_p` and coefficients `α_p, β_p, γ_p`:

```
I_p   = Σ_{q≠p} [ Ivdw(r_pq; or_p, sr_q) + 0.826836 · Ineck(r_pq; p, q) ]                (descreening integral)
Ivdw  = [r + sr_q − or_p ≥ 0] · ½ (1/L − 1/U + ¼ (r − sr_q²/r)(1/U² − 1/L²) + ½ ln(L/U)/r),  U = r + sr_q, L = max(or_p, |r − sr_q|)
Ineck = [rad_p + rad_q + 0.68 − r ≥ 0] · m0(p,q) / (1 + 100 (r − d0(p,q))² + 0.3·10⁶ (r − d0(p,q))⁶)
b_p(I) := 1/B_p = 1/or_p − tanh(α_p ψ − β_p ψ² + γ_p ψ³)/rad_p,   ψ = or_p · I                (inverse Born radius)
g     = −κ [ ½ Σ_p q_p² b_p(I_p) + Σ_{p<q} q_p q_q h(ℓ_p + ℓ_q; r_pq) ],   ℓ_p := ln B_p = −ln b_p(I_p),
h(w; r) := (r² + e^w exp(−r² e^{−w}/4))^{−1/2}          (= 1/f_GB with B_pB_q = e^w).
```

*The mathematical object* is this real-valued expression evaluated on the double-precision
coordinates produced by P2's builder and on the double-precision parameters and neck tables
read from OpenMM's force object, all taken as exact real numbers.  My own evaluator
(`p3core.GBModel`) agrees with OpenMM's Reference (double) platform to `1.8·10⁻¹¹` kcal/mol on 840
fresh assignments of 14 systems, with a table-free evaluation to `5.8·10⁻¹²`, with P2's
evaluator to `1.6·10⁻¹¹` [M, `t01_validate.py`], and with a 40-digit evaluation of the same
expression to `1.8·10⁻¹²` [M, `t03_fp.py`].

**The neck and the tanh, honestly.**  The "tabulated" part of the neck correction is the pair
`(m0, d0)` as a function of the two *radii* (a 21×21 table, interpolated bilinearly in the radii
once per pair of radius classes); as a function of the distance the neck term is the closed
rational expression above, with a **jump** at `r = rad_p + rad_q + 0.68 nm`.  On a rotamer grid
every interatomic distance is a number, so the neck enters only through table entries and no
derivative of it is ever needed.  (For continuous χ the jump would defeat any Lipschitz
argument; that case is not treated.)  The `tanh` rescaling is the only place where a
derivative bound of a non-elementary composite is needed; it is enclosed by interval Taylor
arithmetic (§2.6).

**The structural fact** (P2 Statement 8; re-derived).  On a fixed backbone every atom moves
with at most one site.  Write `l(p) ∈ {0, 1, …, n}` for the *host* of atom `p` (0: fixed).
Then

* `l(p) = 0`:   `I_p(x) = I⁰_p + Σ_i A^p_i(x_i)`;
* `l(p) = l ≥ 1`:   `I_p(x) = S^p_l(x_l) + Σ_{i≠l} T^p_{li}(x_l, x_i)`,

i.e. *for a fixed state of its own host, `I_p` is a sum of one-site functions of the other
sites*; `r_pq` depends on the states of `l(p)` and `l(q)` only.  The tables `I⁰, A, S, T` are
built by `p3core.GBModel._tables` in `O(N² k)` pair evaluations (`N` atoms, `k` states per site).

**Mixed differences.**  For `T ⊆ [n]`, a base point `z ∈ X` and `y_T ∈ X_T`:
`Δ_T g(z; y_T) := Σ_{U ⊆ T} (−1)^{|T|−|U|} g(y_U, z_{−U})`.  Class constant (P2):
`c_T := sup_{z, y_T} |Δ_T g(z; y_T)|`.  Fix an **anchor** `x⁰`; `S(x) := {i : x_i ≠ x⁰_i}`;
**anchored term** `d_T(x_T) := Δ_T g(x⁰; x_T)`; **anchored-pair constant**
`c_T^anch := sup { |Δ_T g(z; y_T)| : z_T = x⁰_T }` (`≤ c_T`); anchored interpolant
`I_M g(x) := Σ_{T ⊆ S(x), |T| ≤ M} d_T(x_T)`, which uses `g` on the Hamming ball of radius `M`
about `x⁰` only.

### 2.1 Proposition 1 [P; checked numerically] — the remainder is a sum of `m`-th order differences at partially switched base points

*For every `g : X → ℝ`, every anchor, every `x` and every `m ≥ 1`, with the sites ordered,*

```
g(x) − I_{m−1} g(x) = Σ_{T ⊆ S(x), |T| = m} Δ_T g(z^{T,x}; x_T),      z^{T,x}_i = x_i (i < min T),  x⁰_i (otherwise).
```

*Consequently `|g(x) − I_{m−1}g(x)| ≤ Σ_{T ⊆ S(x), |T| = m} c_T^anch`.*

*Proof.*  (a) *Context expansion.*  If `V ∩ T = ∅` and `z′` is `z` with the sites of `V`
replaced by `x_V`, then `Δ_T g(z′; x_T) = Σ_{U ⊆ V} Δ_{T∪U} g(z; x_{T∪U})`: for `V = {v}` this is
the definition of the mixed difference over `T ∪ {v}`, and the general case follows by
induction on `|V|`.  With `T = ∅`, `z = x⁰`, `V = S(x)`: `g(x) = Σ_{U ⊆ S(x)} d_U(x_U)`.
(b) Hence `g − I_{m−1}g = Σ_{U ⊆ S, |U| ≥ m} d_U`.  Send each such `U` to the set `T` of its `m`
largest elements; then `U = T ∪ U′` with `U′ ⊆ V_T := {i ∈ S : i < min T}`, and every pair
`(T, U′)` of this kind arises exactly once.  So the sum equals
`Σ_{|T| = m} Σ_{U′ ⊆ V_T} d_{T∪U′}`, and by (a) with base `x⁰` and `V = V_T` the inner sum is
`Δ_T g(z^{T,x}; x_T)`. ∎

*Checks.*  `t05_identity.py`: both sides agree to `1.8·10⁻¹³` kcal/mol for `g_GB` of Val₆/PPII
(40 random `x`, every `m`) and to `7·10⁻¹⁵` for a random function on a `3×4×2×3×3` grid.
*Relation to the theory division.*  The inequality with the class constants `c_T` in place of
`c_T^anch` is its Theorem 11.18 [V, `higherOrder_remainder`]; the identity, and the fact that only
anchored pairs of states and only contexts that differ from the anchor *before* `min T`
occur, are what is added here.  For anchored (referential, cut-HDMR) decompositions of
functions of continuous variables, error analyses of the truncation are in print (§4); I did
not look for this identity in that literature beyond the abstracts cited there.

### 2.2 Lemma 2 [P; checked numerically in its two corollaries] — a chain rule for mixed differences

*Let `u = (u_1, …, u_r) : X → ℝ^r`, `T ⊆ [n]`, `z ∈ X`, `y_T ∈ X_T`, and let `Ψ` be of class
`C^{|T|}` on an open convex set containing the convex hull `K` of the `2^{|T|}` points
`u(y_U, z_{−U})`, `U ⊆ T`.  Then*

```
|Δ_T (Ψ∘u)(z; y_T)|  ≤  Σ_{π ∈ Part(T)}  Σ_{a : π → [r]}  sup_K |∂_{a(B₁)} ⋯ ∂_{a(B_|π|)} Ψ| · ∏_{B ∈ π} D_B(u_{a(B)}),
D_B(v) := max_{U ⊆ T∖B} |Δ_B v((y_U, z_{−U}); y_B)|.
```

*Proof.*  Let `ũ(t) := Σ_{U ⊆ T} u(y_U, z_{−U}) ∏_{i∈U} t_i ∏_{i∈T∖U} (1 − t_i)` on `[0,1]^T` (the
multilinear interpolant of the `2^{|T|}` values) and `F := Ψ∘ũ`.  `F` is `C^{|T|}`, `ũ(t) ∈ K`, and
`F(1_U) = Ψ(u(y_U, z_{−U}))`, so by the fundamental theorem of calculus in each coordinate
`Δ_T(Ψ∘u)(z; y_T) = ∫_{[0,1]^T} ∂_T F(t) dt`.  By the multivariate Faà di Bruno formula for a
derivative in distinct variables (induction on `|T|`: a new variable either differentiates the
outer function, creating a singleton block with a new index, or differentiates one existing
factor `∂_B ũ_a`, enlarging the block `B`),
`∂_T F = Σ_π Σ_a (∂_{a(π)}Ψ)(ũ) ∏_{B∈π} ∂_B ũ_{a(B)}`.  Since `ũ` is multilinear, `∂_B ũ_a` does not
depend on `t_B`, is multilinear in `t_{T∖B}`, and its value at the vertex `1_U`, `U ⊆ T∖B`, is
`Δ_B u_a((y_U, z_{−U}); y_B)`; so `|∂_B ũ_a(t)| ≤ D_B(u_a)` on the cube. ∎

**Corollary L1** (one inner function, additive in the sites of `T`: `u = c + Σ_i a_i(x_i)`).
All `D_B` with `|B| ≥ 2` vanish, only the partition into singletons survives:
`|Δ_T φ(u)| ≤ sup_{[u⁻, u⁺]} |φ^{(|T|)}| · ∏_{i∈T} |a_i(y_i) − a_i(z_i)|`.
(Checked on 2 000 random cases with `φ = tanh`, orders 1–4.)

**Corollary L2** (`Ψ = h(u_1 + u_2)`, `u_1 = ℓ_p∘I_p`, `u_2 = ℓ_q∘I_q`, both `I` additive in the
sites of `T`).  With `δ^p_i := |C^p_i(y_i) − C^p_i(z_i)|` the change of the contribution of site
`i` to `I_p`, and `L^p_k := sup |ℓ_p^{(k)}|`, `H_k := sup |∂_w^k h|` over the relevant intervals,

```
|Δ_T h(ℓ_p + ℓ_q)|  ≤  Σ_{π ∈ Part(T)}  H_{|π|} ∏_{B∈π} ( L^p_{|B|} ∏_{i∈B} δ^p_i  +  L^q_{|B|} ∏_{i∈B} δ^q_i ),
```

because `D_B(ℓ_p + ℓ_q) ≤ D_B(ℓ_p) + D_B(ℓ_q)` and `D_B(ℓ_p) ≤ L^p_{|B|} ∏_{i∈B} δ^p_i` by L1.

**Remark L3** (a site that hosts one of the atoms).  If `l ∈ T`, then
`Δ_T F(z; y_T) = Δ_{T∖l} F|_{x_l = y_l} − Δ_{T∖l} F|_{x_l = z_l}`, so
`|Δ_T F| ≤ W(y_l) + W(z_l)` with `W(b)` a bound for `T∖{l}` at host state `b`.  This step is
where one order of smallness is given up: a rotamer change of the host moves the atom itself,
and no cancellation between the two positions is claimed.

### 2.3 Theorem 3 [P; valid against enumeration in every subset tested] — term-by-term bound on mixed differences of GBn2, any order `m ≥ 3`

For an atom `p` and a state `b` of its host (no state if `l(p) = 0`) let
`[I⁻, I⁺]` be the hull of `I_p` over all states of the other sites, `δ^{p,b}_i` the oscillation
(class mode) or the largest deviation from the anchor state (anchored mode) of the
contribution of site `i ≠ l(p)` to `I_p`, `Bd_k := sup_{[I⁻,I⁺]} |b_p^{(k)}|`,
`L_k := sup_{[I⁻,I⁺]} |ℓ_p^{(k)}|`, `[ℓ⁻, ℓ⁺] ⊇ ℓ_p([I⁻, I⁺])`; for two atoms in host states
`(b, b′)`, `H_k := sup { |∂_w^k h(w; r_pq)| : w ∈ [ℓ_p⁻ + ℓ_q⁻, ℓ_p⁺ + ℓ_q⁺] }`.  For a set `B` of
sites containing neither host define

```
σ_p(B)   := (κ/2) q_p² · Bd_{|B|} · ∏_{i∈B} δ^p_i,
θ_pq(B)  := κ |q_p q_q| · Σ_{π ∈ Part(B)} H_{|π|} ∏_{β∈π} ( L^p_{|β|} ∏_{i∈β} δ^p_i + L^q_{|β|} ∏_{i∈β} δ^q_i ).
```

*Then for every `T` with `|T| = m ≥ 3`, every base point and every `y_T`,*

```
|Δ_T g(z; y_T)|  ≤  Σ_p Σ_{states of l(p) met} σ_p(T ∖ {l(p)})  +  Σ_{p<q} Σ_{states of l(p), l(q) met} θ_pq(T ∖ {l(p), l(q)}),
```

*where "states met" means: the single state `z_l` if the host `l ∉ T`, and the two states
`z_l, y_l` if `l ∈ T`.*  (For `m ≥ 3` the reduced sets are never empty.)

*Proof.*  `g` is a sum over atoms and pairs.  For the self term of `p`: if `l(p) ∉ T`, apply L1
to `φ = b_p`, `u = I_p`; if `l(p) ∈ T`, apply L3 and then L1 for `T∖{l(p)}` at each of the two host
states.  For a pair: fix the states of the hosts that lie in `T` (L3, two states each: up to four
combinations), then `r_pq` is constant and L2 applies to the remaining set. ∎

Two computable forms follow by taking suprema.

* **Class mode** (`termwise.TermBound`, per subset): `ĉ_T ≥ c_T` — oscillations for `δ`; hosts
  outside `T`: maximum over the host state, taken block by block (fixed–site, site–site′);
  hosts in `T`: the two largest values.  Cost per subset: `O(N² k²·Bell(m))`.
* **Anchored mode** (`gfbound.GFBound`): `ĉ_T ≥ c_T^anch` — deviations from the anchor state
  for `δ`; a host outside `T` has *type X* (all ingredients maximised over its states); a host
  in `T` contributes *type A* (its anchor state) plus *type N* (ingredients maximised over the
  non-anchor states).

*Checks.*  Class mode: `ĉ_T ≥ c_T` (P2's enumerated value) in all 562 triples of 44 instances
(`t04_tight.py`, asserted).  Anchored mode: `ĉ_T ≥ c_T^anch` (my enumeration) in all subsets of
orders 3, 4, 5 of Val₅/E (`t02_gf.py`); and indirectly in every enumerated run of §3.3
(the exact remainder lies inside the certified interval at every state).

*What the theorem does not bound.*  Second-order constants `c_ij` of `g`: for `|T| = 2` a pair of
atoms in the two side chains of `T` is left with an empty set — the direct screened
interaction of two side chains is a genuine two-body term, which is why it is evaluated, not
bounded.

### 2.4 Proposition 4 [P; verified to `2·10⁻¹⁶` relative] — the sum over all `m`-subsets in closed form

*For a pair of atom instances with free sites `𝔽` (all sites except the two hosts),*

```
Σ_{B ⊆ 𝔽, |B| = s} θ_pq(B)  =  κ|q_pq_q| · Σ_{a+b=s} e_{a,b}(δ^p, δ^q) · Σ_{r₁, r₂} H_{r₁+r₂} · Bell_{a,r₁}(L^p) · Bell_{b,r₂}(L^q),
```

*where `e_{a,b}` is the coefficient of `u^a v^b` in `∏_{i∈𝔽} (1 + u δ^p_i + v δ^q_i)` and
`Bell_{a,r}(L_1, L_2, …)` is the partial Bell polynomial (the sum over partitions of an `a`-set
into `r` blocks of the product of `L_{|block|}`; `Bell_{0,0} = 1`).  Likewise
`Σ_{|B| = s} σ_p(B) = (κ/2) q_p² Bd_s · e_s(δ^p)`.*

*Proof.*  Expand each block factor of `θ_pq(B)` into its two summands, i.e. label every block
`p` or `q`.  A labelled partition of `B` is the same as a splitting `B = B_p ⊔ B_q` together
with a partition of `B_p` and one of `B_q`; its weight factorises as
`∏_{B_p} δ^p_i ∏_{B_q} δ^q_i` times the block weights.  Summing the block weights over partitions
with `r₁` and `r₂` blocks gives the two Bell polynomials; summing the `δ`-products over
disjoint pairs `(B_p, B_q)` of sizes `(a, b)` gives `e_{a,b}`. ∎

So `Γ_m := Σ_{|T| = m} ĉ_T` (anchored mode) costs `O(n m²)` operations per pair of atom
instances, `O(N² n m² )` in all after `O(N² k²)` kernel suprema — no subset is enumerated.
`gfbound.GFBound.total(m)` implements it; `total(m, T)` evaluates the same expression for one
subset, and the two agree to `2·10⁻¹⁶` over all subsets (`t02_gf.py`).  Site-resolved penalties
`γ_i := (1/m) Σ_{T∋i, |T|=m} ĉ_T = (Γ_m − Γ_m^{(−i)})/m` cost `n + 1` such evaluations; they
satisfy `Σ_{T ⊆ S, |T| = m} ĉ_T ≤ Σ_{i∈S} γ_i` for every `S` (each `T ⊆ S` is counted `m` times
`1/m`; the other subsets only add) — P2's counting argument of its Statement 5(d), at order `m`.

### 2.5 Theorem 5 [P; checked by enumeration at every state of every enumerated instance] — a certified floor and ceiling that are banded pairwise functions

**Recipe** (inputs: sequence, backbone, grid, τ; truncation order `m ≥ 3`; band width `w`).

1. *Tables* `I⁰, A, S, T` and the pair tables of `f`.  Cost `O(N² k)` (+ `O(N² k²)` for site–site blocks).
2. *Anchor* `x⁰`: any state (I use coordinate descent on `E`; validity does not depend on it).
3. *Remainder constant* `Γ_m` or site penalties `γ_i` (Proposition 4, derivative enclosures of §2.6).
4. *Evaluations*: `g` on the Hamming ball of radius `m − 1` about `x⁰`,
   `N_ball = Σ_{j<m} C(n,j)(k−1)^j` evaluations; from them all `d_U`, `|U| < m`, by inclusion–exclusion.
5. *Models.*  With `P_ij := J_ij + d_ij`:

```
m_∓(x) = c₀ + g(x⁰) ∓ (Γ_m + ε_fp)                                   [or ∓ Σ_i γ_i [x_i ≠ x⁰_i] ∓ ε_fp]
         + Σ_i (h_i + d_i)(x_i) + Σ_{j−i ≤ w} P_ij(x_i, x_j)
         + Σ_{j−i > w} ( a^∓_ij(x_i) + b_ij(x_j) )                   b_ij = column mean of P_ij, a^∓_ij = row min / max of P_ij − b_ij
         + Σ_{3 ≤ |U| < m} red^∓_U(x_a, x_b)                         min / max of d_U over the other sites of U; (a, b) ⊆ U the in-band
                                                                      pair with the smallest slack (a one-site function if there is none).
```

*Claim: `m₋(x) ≤ E(x) ≤ m₊(x)` for every `x ∈ X`; both are pairwise with pairs of separation
at most `w`.*

*Proof.*  `E = f + g`; `g = Σ_{|U|<m} d_U + R` with `|R| ≤ Σ_{T ⊆ S(x), |T|=m} c_T^anch ≤ Σ_{T ⊆ S(x)} ĉ_T`
(Proposition 1, Theorem 3), which is at most `Γ_m` and at most `Σ_{i∈S(x)} γ_i` (§2.4).  Every
replaced term is replaced by a pointwise minorant (majorant): `P_ij ≥ a⁻_ij(x_i) + b_ij(x_j)`
by construction, `d_U ≥ red⁻_U`.  The allowance `ε_fp` covers the rounding of the evaluated
values (§2.6). ∎

6. *Exact partition functions and sampling.*  Eliminating the sites in order with a message
   over the next `w` sites gives `ln Z(m_∓)` in `O(n k^{w+1})` operations, the maximum of
   `m₊ − m₋` (max-plus), and exact independent samples of `π_{m₋}` by backward sampling.

**Consequences.**  (a) *Deterministic bracket:* `ln Z(m₊) ≤ ln Z(E) ≤ ln Z(m₋)`, with
`0 ≤ E − m₋ ≤ ρ_cert := max_x (m₊ − m₋)(x)`; also `min m₋ ≤ min E ≤ min m₊`.
(b) *Two-sided remainder beyond the specified pairwise approximation `I₂g`* (item 1(b) of the
brief): for every `x`,
`−Σ_{3≤|U|<m} max(−d_U)⁺ − Γ_m ≤ g(x) − I₂g(x) ≤ Σ_{3≤|U|<m} max(d_U)⁺ + Γ_m`; for `m = 3` this
is `|g − I₂g| ≤ Γ₃`, obtained from tables alone plus the `1 + Σ(k_i−1) + Σ_{i<j}(k_i−1)(k_j−1)`
evaluations that define `I₂g`.
(c) *Sampling:* `ln Z(E) = ln Z(m₋) + ln 𝔼_{π_{m₋}} W`, `W := e^{−β(E − m₋)} ∈ [e^{−βρ_cert}, 1]`
(§2.7).

*Checks.*  In every enumerated instance of §3.3 the script evaluates `E`, `m₋`, `m₊` at
**all** states: ⟨NVIOL-DETAIL⟩; the transfer-matrix `ln Z(m₋)` equals the enumerated one to
`≤ 2·10⁻¹³`.

### 2.6 Where floating point enters, and how each place is covered

| quantity | how obtained | rigour |
|---|---|---|
| `sup |b_p^{(k)}|`, `sup |ℓ_p^{(k)}|`, `k ≤ 6`, on a cell of `I` | interval Taylor series of `b_p(X + t)`, `−ln b_p(X + t)` (`mpmath.iv`, 80 bits, outward rounding), in the Taylor form `Σ_{j<2} σ^j/j!·|φ^{(k+j)}(c)| + σ²/2·sup_X|φ^{(k+2)}|` about the cell midpoint | rigorous enclosure (correctness of `mpmath.iv` assumed); stored as doubles rounded up; enclosure / sampled maximum = 1.0000002–1.00006 |
| `sup |∂_w^k h(w; r)|`, `k ≤ 6` | `∂_w^k h = (2/r)·ζ_k(D)`, `D = r²e^{−w}/4`, `ζ_k = √D·η_k`, `η_0 = (4D + e^{−D})^{−1/2}`, `η_{k+1} = −η_k/2 − Dη_k′`; each `η_k` is an explicit finite sum of monomials `c·D^a e^{−bD}(4D + e^{−D})^{−c′/2}` with exact rational coefficients; on cells of `ln D`: Taylor form of order 3 using `dζ_k/d ln D = −ζ_{k+1}`; first cell `[0, 10⁻⁵]` by plain interval evaluation, tail `[80, ∞)` by a monotone majorant | rigorous enclosure; ratio to sampled maximum 1.00001–1.0001 |
| query of an interval | maximum over all cells meeting the interval widened by `10⁻⁹` relative | covers rounding of the interval's own end points |
| table differences `δ` | double subtraction `+ 2·10⁻¹⁰ nm⁻¹`; hull end points `± n·2·10⁻¹⁰` | measured error of a table entry against 40-digit arithmetic: `6·10⁻¹⁵ nm⁻¹` [M] — allowance 4 orders larger |
| sums and products of non-negative doubles in `Γ_m` | final factor `(1 + 10⁻⁹)` | at most `~10⁴` operations of relative error `2⁻⁵³` each, no cancellation |
| each evaluated `g(x)` on the ball | double precision; allowance `ε_g = 10⁻⁷` kcal/mol per value, i.e. `ε_fp = ε_g Σ_U 2^{|U|}` in the models | a-priori worst case for a recursive sum of `~10⁵` terms with `Σ|term| ~ 5·10³` is `~3·10⁻⁸`; measured error `≤ 1.8·10⁻¹²` [M] |
| transfer matrix | double precision log-sum-exp | relative error of `Z` `≲ 10⁻¹²` (sums of positive terms) [H: not budgeted formally; four orders below every reported digit] |

*Checkable hypotheses of the certificate, all checked at run time:* (H1) every descreening
integral lies in the enclosure grid `[0, 24] nm⁻¹` (an exception is raised otherwise; it was
raised once, for Leu at τ = 0.60 with the first grid `[0, 16]`, which is how the grid got its
size); (H2) distinct atoms have `r > 0` (otherwise the bound is `+∞`, never wrong);
(H3) `b_p > 0`, automatic for GBn2 since `b_p > 1/or_p − 1/rad_p > 0`.  **No minimal-distance
hypothesis is needed**: the clash filter of the domain enters only through the size of the
constants.  *Assumed and not proved:* IEEE-754 double arithmetic; that the libm functions
used in the *evaluation* of `g` are accurate to well within the allowance (they are not used in
the enclosures); the correctness of `mpmath.iv`; the correctness of my code (tested as
described, not verified).

### 2.7 Brackets from samples that are valid at every `N`

Let `W_1, …, W_N` be i.i.d. copies of `W = e^{−β(E − m₋)}` under `π_{m₋}`, `μ := 𝔼W = Z(E)/Z(m₋)`,
`w_min := e^{−βρ_cert} ≤ W ≤ 1` (certified, Theorem 5).

* **Hoeffding [K, classical; from memory, the statement is the textbook one].**  With
  probability `≥ 1 − δ`: `|W̄ − μ| ≤ (1 − w_min) √(ln(2/δ)/(2N))`.
* **Lemma R [P] (sample-range bound).**  Let `M_N = max_i W_i`, `m_N = min_i W_i`,
  `ε_N := 1 − (δ/2)^{1/N}` (`≤ ln(2/δ)/N`).  With probability `≥ 1 − δ`:
  `m_N − (m_N − w_min) ε_N ≤ μ ≤ M_N + (1 − M_N) ε_N`.
  *Proof.*  Let `t* := inf{t : ℙ(W > t) ≤ ε_N}`.  Then `ℙ(W ≥ t*) ≥ ε_N`, and
  `ℙ(W > M_N) > ε_N` forces `M_N < t*`, i.e. all `N` samples below `t*`, which has probability
  `≤ (1 − ε_N)^N = δ/2`.  On the complement,
  `μ ≤ M_N ℙ(W ≤ M_N) + 1·ℙ(W > M_N) ≤ M_N + (1 − M_N) ε_N`.  The lower side is symmetric with
  `W ≥ w_min`. ∎
  This is the elementary form of the theory division's "spot check": it is sharp when `W` is
  nearly constant (a floor that is a constant shift of a good model) and then has width
  `O(1/N)` instead of `O(1/√N)`; it is useless when `W` is spread out.
* **Gibbs–Bogoliubov side.**  `ln Z(E) ≥ ln Z(m₋) − β 𝔼_{π_{m₋}}(E − m₋)` (Jensen), and with
  probability `≥ 1 − δ/2`, `𝔼(E − m₋) ≤ mean + ρ_cert √(ln(2/δ)/(2N))`.

Neither bound uses a normal approximation.  The samples are produced by inverse-CDF backward
sampling from double-precision conditional tables with numpy's PCG64 generator: "exact
samples" means exact up to that arithmetic (total-variation error of order `n·2⁻⁵²` per sample
[H]); the deterministic bracket of Theorem 5 does not depend on any random number.

### 2.8 Negative statements

**N1 [M + P].**  *Analysis alone — tables, ranges, interval enclosures, no evaluation of `g` —
certifies third-order constants that are 33–1 400 times the measured ones* (§3.2), and the floor
built from them is useless beyond two or three residues (§3.3, column `m = 3`).
*Reason [M, `x01`, `x02`, `x03`].*  Split `g` into its self part and its cross part.  (a) The
self part is bounded tightly: within ×1.3–3.3 of its own exact constant at third order
(Ser₃, Ser₄, Val₆ on the strand, Leu₆ on the helix; sampled suprema).  (b) The cross part is
bounded only within ×80–270 of its own constant, because the bound sums `|q_pq_q|` over all
pairs within the range of the kernel (`∂_w h` decays like `e^{−r²/4B_pB_q}`: about 30 neighbours
per atom), while the exact sum is a sum of screened interactions between nearly neutral groups
(C=O, N–H, CH₃).  (c) In the exact function self and cross parts cancel to about 1 % at zeroth
order (Val₆/E: self −640, cross +600, total −37 kcal/mol; single-site ranges: self 14.7,
cross 14.8, total 1.1 for Leu₆/H) and still by a factor 1.5–5 at third order.  A bound that
treats atom pairs one at a time has no access to (b) or (c).
*Why the obvious repairs do not help by more than one small factor each [H, with the numbers of
§3.1].*  Keeping signed sums exact at a reference state (frozen-radius fields, first-order
response computed with signs, …) leaves a term-by-term remainder that is smaller by one power
of the relative change of a Born radius under one rotamer flip.  Measured on the certified
constants, that power is a factor 30–50 per order for Val, 11–20 for Leu on extended backbones,
5–7 for Leu on the helix.  Recovering a factor 500 therefore needs two more orders — which is
what `m = 5` does, by evaluation rather than by algebra.

**N2 [M].**  *On the helix the recipe fails at every affordable order:* Leu₁₆/H has
`Γ₃, Γ₄, Γ₅, Γ₆ = 1 819, 370, 60, 8.0` kcal/mol, i.e. `e^{βΓ₆} ≈ e^{13.5}` while the ball of radius 5
already has 6 885 of the 65 536 states.  The helix is the geometry in which every side chain
has many neighbours within the range of the kernel; P2's measured `Σc_ijk = 7.4` kcal/mol for the
same instance says that the *true* third-order budget is large there as well.

**N3 [P].**  *The certificate is not "by analysis" in the sense of P2's next step 2.*  It needs
`N_ball` evaluations of `g`.  They are polynomially many and no joint state space is enumerated,
but the claim "a floor by analysis" holds only in the combined form of Theorem 5.

### 2.9 What is certified, by what

| statement | status |
|---|---|
| `m₋ ≤ E ≤ m₊` on all of `X`, for the instances of §3.3–3.5 | [P] Proposition 1, Lemma 2, Theorem 3, Proposition 4, Theorem 5 + interval enclosures + stated floating-point allowances; not machine-checked; verified at every state wherever `X` could be enumerated |
| `ln Z(m₊) ≤ ln Z(E) ≤ ln Z(m₋)`, `min m₋ ≤ min E ≤ min m₊` | follows; `ln Z(m_∓)` in double precision |
| sampled brackets | [P]/[K] §2.7, probability `≥ 1 − δ` over the sampler |
| anything about a real peptide in water | **not claimed** |
