# Workstream P3 (science division) — a floor by analysis: certified constants of the GBn2 remainder, and a certified `ln Z` beyond enumeration size

> **Coordinator's note added 2026-11-26 (workstream P4; SCI-REV-0012 §5).**  "Everything is on P2's pruned
> product" (§5 item 6 below).  For Val, Leu and Ser that product is the whole clash-free domain, and the
> twenty-residue certificate is unaffected.  For **Phe, Lys and the heteropolymer** it is a greedily pruned
> sub-product which, as workstream P4 found, does not contain the energy minimum of the clash-free domain
> in 14 of 40 analyses: the certified sandwiches, cost numbers and ratios reported below for these three
> families are statements about the sub-domain.  The repair is P4's: the true minimiser first, then the
> largest reset-closed domain around it (not a product in general — the banded transfer matrices of §2.5
> would have to carry the exclusions).


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

All four numbered items of the brief were carried out, both optional ones on a small scale,
and the two additions the coordinator sent during the work.  In order:

1. **Theorem with recipe** — done (§2): an exact remainder identity for the anchored
   expansion (Proposition 1), a chain rule for mixed differences (Lemma 2), a rigorous
   term-by-term bound on mixed differences of any order of the GBn2 energy (Theorem 3), its
   sum over *all* subsets of a given order in closed form (Proposition 4), certified floor and
   ceiling functions `m₋ ≤ E ≤ m₊` that are banded pairwise models (Theorem 5), and a
   floating-point error budget with interval enclosures of every derivative (§2.6).  All
   inequalities were checked against exact enumeration: no violation in any of the
   5 512 504 enumerated states.
2. **How tight** — done, and the answer for *analysis alone* is negative (§2.8, §3.2): the
   third-order constants certified without any evaluation of `g` are **33–1 400 times** the
   constants P2 measured (apolar 200–1 400, polar and aromatic 40–170, charged 33–160).  The
   reason is identified and quantified.
3. **What the floor buys** — done (§3.3–3.4): `ρ`, the exact cost number `Z(m₋)/Z(E) − 1` and
   deterministic brackets for apolar, polar and charged peptides of 3–16 residues, for three
   truncation orders.
4. **One instance beyond enumeration** — done (§3.5): Ace-Val₂₀-NMe on polyproline II, `3²⁰ = 3.49·10⁹` assignments: certified deterministic bracket `ln Z ∈ [518.2332, 518.2937]` from 87 441 evaluations, `[518.2598, 518.2648]` with 50 000 samples (δ = 0.05), and a certified global minimum.
5. Optional (a) `Σ c_i²` — §3.7; (b) OBC2, and an ablation of the neck term — §3.8.
6. **Two additions requested by the coordinator during the work** — done (§2.9, §3.6): certified inputs of the
   Bennett bracket (a one-sided floor of the remainder beyond a stated pairwise model, a certified
   variance bound, the resulting `W`), the same with a window of 1 or 2 along the chain, and the
   sampled statistics of the remainder at 20 residues next to the enumerated ones at 6–12.

What I did **not** do is listed in the last section.

---

## 1. Verdicts in one paragraph

**Is a floor certifiable by analysis for the remainder P2 measured?  By analysis alone:
rigorously yes, usefully only for serine on the strand.  By analysis of the tail plus
polynomially many evaluations: yes on extended backbones, with a certified `ln Z` at 20
residues; no on the helix.**  (i) A bound on the third-order constants `c_ijk` of the GBn2
polarisation energy that uses only the descreening tables and interval enclosures of
derivatives — no value of `g` — is proved here [P] and holds in all 672 triples of 44 of P2's
instances [M], but it exceeds the measured constants by a factor **200–1 400 for apolar side
chains (Val, Leu), 90–170 for Phe, 40–100 for Ser, 33–77 for Lys, 90–160 for the
heteropolymer**.  The floor built from it — P2's Statement 5(d),
`f + I₂g − Σγ_i[x_i ≠ x⁰_i]`, with certified constants — has an exact cost number
`Z(m)/Z(E) − 1` of 0.4, 1.1, 2.3 for Ser₄, Ser₅, Ser₆ on the strand (a working certificate:
1 009 evaluations of 531 441, and an exact certificate of the minimum), but 16, `10³`, `10⁵` for
Val₆, Val₈, Val₁₀ on the strand (a factor 8 per residue — faster than the domain grows),
`10⁴–10¹¹` for Val on polyproline II and `10²–10⁸⁹` on helices and for charged side chains.
(ii) The loss has one cause [M]: the cross term of GB is a sum over all atom pairs within the
range of the kernel, carrying `q_pq_q` of both signs, that cancels to about 1 % (Val₆: self
part −640, cross part +600, total −37 kcal/mol), and a term-by-term bound cannot see the
cancellation.  Term by term the bound is nearly sharp: with all charges but one pair switched
off it is within a median factor 1.1–6 of the exact constant and never below it (1 118 cases).
Every analytic device that keeps signed sums at a reference gains one power of the small
parameter (the relative change of a Born radius under one rotamer flip) — which is exactly
what one more order of the anchored expansion gains, without any loss.  (iii) Hence the recipe
that works [P]: **evaluate `g` on the Hamming ball of radius `m − 1` about an anchor**
(`Σ_{j<m} C(n,j)(k−1)^j` evaluations) **and bound only the remainder beyond order `m − 1`**, by the
same term-by-term bound summed over *all* `m`-subsets in closed form (seconds for 40 residues).
The certified remainder constant `Γ_m` grows linearly with the chain and falls by a factor
21–51 per order for Val on strand and PPII (`n = 12`, strand: `Γ₃ … Γ₆ = 36.9, 1.56, 0.039, 0.0008`
kcal/mol), 11–22 for Leu on strand and PPII, and only 5–8 for Leu on the helix (`n = 16`: 1 819,
370, 60, 8.0), where the recipe fails at every order tried.  (iv) With `m = 4` or `5` the
certified floor and ceiling are banded pairwise functions `m₋ ≤ E ≤ m₊` with exact partition
functions and exact samplers.  For Ace-Val₂₀-NMe on polyproline II (`3²⁰ = 3.49·10⁹` assignments): with `m = 4`, 9 921 evaluations of `g` certify `ln Z(E) ∈ [517.484, 519.220]` deterministically and, with 50 000 exact samples of `π_{m₋}`, `[518.2442, 518.2759]` at confidence 0.95; with `m = 5`, 87 441 evaluations (`2.5·10⁻⁵` of the domain) certify **`ln Z(E) ∈ [518.2332, 518.2937]` with no sampling**, `[518.2598, 518.2648]` with the samples; all brackets intersect; and `min E = −306.56871 ± 10⁻⁵` kcal/mol is certified at the anchor.  In 160 enumerated runs (5.5 million state checks) the sandwich was never violated and the true `ln Z` lay inside every bracket.  (v) The theory division's formula
is confirmed on real numbers where it matters: the cost is the Boltzmann weight of the distance
to the *certified floor*, and a floor that is a function is far cheaper than a constant (Val₁₀
on the strand at `m = 4`: cost number 6.3 with the constant `Γ₄`, 0.022 with site penalties;
Lys₄ on the helix: 3.2 against 0.48), because the ensemble rarely leaves the neighbourhood of
the anchor.  With `m = 4` and site penalties the certificate is cheaper than enumeration from 4
(Ser) to 7 (Val) residues on, and its cost number reaches `10⁶` only near 230 residues for Val on
PPII [H: extrapolated exponent].  (vi) For the coordinator's Bennett bracket the same sandwich
gives all inputs exactly and without sampling: a one-sided floor `r ≥ 0` of `r = β(E − m₋)`, the
bounds `b ≤ 𝔼u`, `Var r ≤ 𝔼u²` with `u = β(m₊ − m₋)` an explicit banded function; at 20 residues
`b_cert = 0.061 k_BT`, `s²_cert = 4.8·10⁻³`, `W = 2.4·10⁻³` nats; on enumerated instances `W_cert` is
within 4–26 times the true Jensen gap at `m ≥ 4`, and the remainder statistics at 20 residues
are predicted within 2–9 % (mean, floor) and 7–26 % (variance) by linear extrapolation from
8–12 residues.  (vii) The neck correction of GBn2 is what makes its constants large: without
it they fall by a factor 10–70, and OBC2's are 2–8 times smaller for apolar side chains.
What remains assumed in every statement: the force field and the GB model themselves, the
rotamer grid, the rigid geometry, the fixed backbone, small exposed peptides; and — until
someone machine-checks it — my proofs, my code and a floating-point allowance.

---

## 2. Precise statements

### 2.0 Setting and notation

**The function.**  `X = ∏_{i=1}^n X_i`, `X_i` the finite set of admissible rotamers of
residue `i` (P2's pruned product domain `X′` at clash threshold τ; my `p3core.pruned_domain`
reproduces P2's domain in all 26 comparisons).  `E = f + g`: `f` the ff14SB vacuum energy,
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
(`p3core.GBModel`) agrees with OpenMM's Reference (double) platform to `1.8·10⁻¹¹` kcal/mol on 280
fresh assignments of 14 systems (20 each), with a table-free evaluation to `5.8·10⁻¹²` on the same states, with P2's
evaluator to `1.6·10⁻¹¹` on 840 [M, `t01_validate.py`], and with a 40-digit evaluation of the same
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

*Checks.*  Class mode: `ĉ_T ≥ c_T` (P2's enumerated value) in all 672 triples of 44 instances
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
**all** states: 160 enumerated runs, 5 512 504 state checks, **no violation**; the transfer-matrix `ln Z(m₋)` equals the enumerated one to
`≤ 5·10⁻¹³`.

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
self part is bounded tightly: within a factor 1.3–4 of its own exact constant at third order
(Ser₃, Ser₄, Val₆ on the strand, Leu₆ on the helix; sampled suprema).  (b) The cross part is
bounded only within a factor 60–430 of its own constant (80–190 in the sums over triples), because the bound sums `|q_pq_q|` over all
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
constants, that power is a factor 22–46 per order for Val, 11–22 for Leu on extended backbones,
5–8 for Leu on the helix.  Recovering a factor 500 therefore needs two more orders — which is
what `m = 5` does, by evaluation rather than by algebra.

**N2 [M].**  *On the helix the recipe fails at every affordable order:* Leu₁₆/H has
`Γ₃, Γ₄, Γ₅, Γ₆ = 1 819, 370, 60, 8.0` kcal/mol, i.e. `e^{βΓ₆} ≈ e^{13.5}` while the ball of radius 5
already has 6 885 of the 65 536 states.  The helix is the geometry in which every side chain
has many neighbours within the range of the kernel; P2's measured `Σc_ijk = 7.4` kcal/mol for the
same instance says that the *true* third-order budget is large there as well.

**N3 [P].**  *The certificate is not "by analysis" in the sense of P2's next step 2.*  It needs
`N_ball` evaluations of `g`.  They are polynomially many and no joint state space is enumerated,
but the claim "a floor by analysis" holds only in the combined form of Theorem 5.

### 2.9 Proposition 6 [P; checked by enumeration] — certified inputs of the floor-plus-variance (Bennett) bracket

*(Added at the coordinator's request during the work: a certified one-sided floor of the
remainder beyond a stated pairwise model, a certified bound of its variance under that
model, and the resulting `W(b, s²)`; addendum A17, part 7.)*

Let `m₋ ≤ E ≤ m₊` be the models of Theorem 5 and `u := β(m₊ − m₋) ≥ 0` — an **explicit banded
pairwise function**, known without evaluating `E` anywhere outside the ball.

*(i) Model `m := m₋`, remainder `r := β(E − m₋)`.*  Then on all of `X`
`lo := 0 ≤ r ≤ u`; hence, with expectations under `π_{m₋}`,

```
b := 𝔼 r − inf r  ≤  b_cert := 𝔼 u,            Var r  ≤  𝔼 r²  ≤  s²_cert := 𝔼 u².
```

*(ii) Midpoint model `m₀ := (m₋ + m₊)/2`, `r₀ := β(E − m₀)`.*  Then `|r₀| ≤ u/2`, so the constant
`lo₀ := −βρ_cert/2` is a floor of `r₀`, and under `π_{m₀}`

```
b  ≤  b_cert := (𝔼 u + βρ_cert)/2,             Var r₀  ≤  s²_cert := 𝔼 u² / 4.
```

*(iii) Both moments are computed exactly* (up to double rounding of sums of positive terms): the
elimination of Theorem 5 is run over polynomials of degree 2, i.e. the conditional means of
the partial sum of `u` and of its square are propagated with the message
(`pwmodel.BandModel.moments`; cost `O(n k^{w+1})`).
*(iv) Consequently* (Bennett's inequality in its sharp two-point form, [K] classical, as stated
in addendum A17(7); `W` is non-decreasing in both arguments because the class
`{Y ≤ b, 𝔼Y = 0, Var Y ≤ s²}` grows with them)

```
0  ≤  K := ln Z(E) − ln Z(m) + 𝔼_{π_m} r  ≤  W(b_cert, s²_cert),     W(b, s²) = ln[(b² e^{−s²/b} + s² e^{b})/(b² + s²)],
```

*and with `N` samples of `π_m` and Chebyshev's inequality with the **certified** variance, with
probability `≥ 1 − δ`:*
`ln Z(E) ∈ [ln Z(m) − r̄ − t, ln Z(m) − r̄ + t + W(b_cert, s²_cert)]`, `t = √(s²_cert/(Nδ))`.

*Proof.*  (i) and (ii) are the sandwich `m₋ ≤ E ≤ m₊` read in units of `k_BT`; `𝔼r ≤ 𝔼u`
because `r ≤ u` pointwise; `Var r ≤ 𝔼r²`.  (iv) Apply Bennett's bound to `Y = 𝔼r − r ≤ b`. ∎

*Checks.*  In every enumerated run the script computes the exact `b`, `Var r`, `K` of both
models and asserts `b ≤ b_cert`, `Var r ≤ s²_cert`, `0 ≤ K ≤ W(b, Var r) ≤ W(b_cert, s²_cert)`,
and compares the transfer-matrix moments of `u` with direct sums (agreement `< 10⁻⁹` relative):
no failure (§3.6).

*What decides the size of the certified inputs.*  `u` consists of twice the remainder
penalties plus the slack of the minorants of the evaluated terms of order `3 … m−1`; it knows
nothing about the *actual* remainder, which is 250–800 times smaller than its certified bound.
With a **constant** remainder bound `u ≈ 2βΓ_m` everywhere, so `b_cert ≈ 2βΓ_m`, `s²_cert ≈ (2βΓ_m)²`
however concentrated `r` is: the route is then no better than the range.  With **site penalties**
`u` vanishes at the anchor and grows with the number of sites off the anchor, and the certified
`b` and `s²` are small whenever `π_m` stays near the anchor.  This is the same lesson as for the
floor itself: the certificate must be a function, not a constant.

### 2.10 What is certified, by what

| statement | status |
|---|---|
| `m₋ ≤ E ≤ m₊` on all of `X`, for the instances of §3.3–3.5 | [P] Proposition 1, Lemma 2, Theorem 3, Proposition 4, Theorem 5 + interval enclosures + stated floating-point allowances; not machine-checked; verified at every state wherever `X` could be enumerated |
| `ln Z(m₊) ≤ ln Z(E) ≤ ln Z(m₋)`, `min m₋ ≤ min E ≤ min m₊` | follows; `ln Z(m_∓)` in double precision |
| sampled brackets | [P]/[K] §2.7, probability `≥ 1 − δ` over the sampler |
| anything about a real peptide in water | **not claimed** |

---

## 3. Numerics: what was computed, sizes, results, how to re-run

All scripts are in `experiments/science/ws_P3/`; run them from there with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B <script>`.  P2's modules
(`scbuild.py`, `fbmodel.py`) and P's (`pepbuild.py`, `fastff.py`) are imported read-only for the
geometry, the clash scores, the tables of `f` and — for bulk evaluations only — P2's block
evaluator of `g` (five times faster than mine; every run re-checks 48 random states against my
own evaluator, deviation `< 10⁻⁸` asserted, `≤ 3·10⁻¹¹` observed).  The machine was shared (load
7–14 on 4 cores during the runs), so wall times are upper bounds.

| script | what | output |
|---|---|---|
| `p3core.py`, `t01_validate.py` | my GBn2/OBC2 evaluator with self/cross split and descreening tables; validation on fresh states against OpenMM (Reference, double), a table-free evaluation and P2's evaluator | `logs/t01_validate_gbn2.log` |
| `t03_fp.py` | `g` and the tables against 40-digit arithmetic | `logs/t03_fp.log` |
| `mixdiff.py`, `x01_explore.py` | exact mixed differences by enumeration: self part, cross part, context dependence, orders 1–5 | `logs/x01_explore.log` |
| `dfun.py`, `encl.py` | closed-form derivatives; rigorous enclosure tables (`mpmath.iv`) | `cache/atom_*.npz`, `cache/zeta_*.npz` |
| `termwise.py`, `x02_termwise.py`, `x03_breakdown.py`, `t04_tight.py`, `run_tight.sh` | per-subset bound, class mode; exploration with sampled suprema; the rigorous comparison with P2's enumerated `c_ijk` | `logs/x02*.log`, `logs/x03*.log`, `logs/t04_tight_*.log`, `out/tight_*.json` |
| `gfbound.py`, `t02_gf.py`, `t06_pairtest.py`, `x04_gamma.py`, `x05_neck.py` | anchored mode summed over all subsets; tests (generating function = explicit sums; bound ≥ exact; single-term sharpness); `Γ_m` for long chains; ablation of the neck term | `logs/t02_gf_V5E.log`, `logs/t06_pairtest.log`, `logs/x04_gamma_*.log`, `logs/x05_neck.log` |
| `t05_identity.py` | Proposition 1 and Corollary L1 numerically | `logs/t05_identity.log` |
| `pwmodel.py`, `run_floor.py`, `run_batch.sh`, `batch_*.txt` | anchored terms from the ball, banded models, transfer matrix, exact sampling, moments; the end-to-end pipeline with enumeration checks | `logs/floor_*.log`, `out/floor_*.json` |
| `mk_tables.py`, `mk_report.py` (`fill_text*.py`: one-off helpers that inserted text blocks into this report) | tables | `out/tables.md`, `out/report_tables.md` |

To re-run everything: `python3 -B t01_validate.py gbn2; python3 -B t03_fp.py V6 E 0.70 3;
python3 -B t05_identity.py; python3 -B t02_gf.py V5 E 0.70 5; python3 -B t06_pairtest.py V5 E 0.70 60;
bash run_tight.sh; for b in A2 B2 F G H; do bash run_batch.sh batch_$b.txt logs/floor_batch_$b.log; done;
bash run_batch.sh batch_D.txt logs/floor_big_V20.log; python3 -B mk_report.py`.  (The first run
builds the enclosure tables: about 4 minutes.  Batches `A`, `B` contain the constant-bound
runs of Val that were made first — they were stopped after the Val runs and continued as `A2`, `B2`;
`C`, `E` are superseded by `F`; superseded JSON files are kept in `out/intermediate/` and `out/prebennett/`.
Three runs aborted in the *reporting* step, after their enumeration check had passed, because
`e^{−βρ_cert}` underflows: Leu₈/H and Leu₁₂/H at `m = 3`, LKSE₅/H at `m = 3`; they are not in the tables.)

**Totals.**  <!--T:stats-->
164 runs of `run_floor.py` (160 with full enumeration: 5,512,504 state checks of `m₋ ≤ E ≤ m₊`, **0 violations**; the transfer-matrix `ln Z(m₋)` equals the enumerated one to `5e-13`; the anchor from coordinate descent is the global minimiser of `E` in 160 of 160; the true `ln Z` lies inside the Hoeffding bracket in 160 of 160 runs, inside the sample-range bracket in 160 of 160, inside the Bennett bracket in 132 of 132)
<!--/T:stats-->

### 3.1 What has to be bounded [M, exact enumeration, `x01_explore.py`]

Anchor `x⁰ = argmin E`; sums over all subsets of the given order; kcal/mol.

| instance | Σ `c_T` order 3: total / self part / cross part | at the anchor context only | Σ order 4 (total) | Σ order 5 | `g − I₂g` | `g − I₃g` |
|---|---|---|---|---|---|---|
| Ser₄/E τ.70 (6 561) | 0.0096 / 0.0138 / 0.0118 | 0.0094 | 2.5·10⁻⁴ | — | [−0.0026, 0.0030] | [−8·10⁻⁵, 1·10⁻⁴] |
| Ser₄/H τ.70 (2 916) | 0.082 / 0.026 / 0.075 | 0.082 | 2.3·10⁻⁴ | — | [−0.016, 0.047] | [−8·10⁻⁵, 1.3·10⁻⁴] |
| Val₆/E τ.70 (729) | 0.031 / 0.086 / 0.075 | 0.027 | 0.0022 | 4.3·10⁻⁵ | [−0.0041, 0.0049] | [−3.3·10⁻⁴, 5.2·10⁻⁴] |
| Leu₆/H τ.60 (64) | 0.27 / 0.60 / 0.68 | 0.16 | 0.061 | 0.0042 | [−0.019, 0.057] | [−0.030, 0.004] |
| Leu₈/H τ.60 (256) | 1.23 / 1.26 / 1.75 | 0.75 | 0.29 | 0.029 | [−0.067, 0.249] | [−0.088, 0.012] |

My enumeration reproduces P2's constants where both exist (Ser₃/E `c₁₂₃ = 4.026·10⁻³`; Val₆/E
max 5.850·10⁻³, sum 3.075·10⁻²; P2: 4.03·10⁻³, and the same two numbers in its JSON) — an
**independent replication** of those entries with different code for `g`, the domain and the
differences.  Three facts set the task: the sums of exact constants fall by a factor 14–50 per order
for Val and Ser on the strand but only 4–14 for Leu on the helix; the self and the cross part are each as large as or
larger than the total already at third order; and the dependence of `Δ_T g` on the context is
weak on the strand (0–20 %) and strong for some helix triples.

### 3.2 How tight is analysis alone? [M: rigorous bound against P2's enumeration, `t04_tight.py`]

Class-mode bound `ĉ_ijk` of Theorem 3 with the interval enclosures — tables only, no value of
`g` — against P2's enumerated `c_ijk` on its product domain `X′` (kcal/mol):

<!--T:tight-->
| side chain, backbone, τ | n | triples | measured (P2) max `c_ijk`; Σ | certified by analysis max `ĉ_ijk`; Σ | Σ certified / Σ measured | per triple: min / median / max | self part alone / measured Σ |
|---|---|---|---|---|---|---|---|
| V, E, 0.70 | 3, 4, 6, 8 | 81 | 0.00585; 0.048 | 2.83; 23.3 | 423–485 | 217 / 459 / 700 | 9.1–10.3 |
| V, P2, 0.70 | 4, 6, 8 | 80 | 0.00639; 0.0913 | 1.84; 18.8 | 206–218 | 84 / 226 / 618 | 3.0–3.5 |
| L, E, 0.60 | 4, 6, 8 | 80 | 0.00544; 0.0686 | 9.97; 90.8 | 1323–1420 | 306 / 1184 / 3862 | 23.9–30.6 |
| L, H, 0.60 | 4, 6, 8 | 80 | 0.0689; 1.23 | 20.1; 346 | 280–706 | 101 / 579 / 2769 | 1.9–5.9 |
| L, P2, 0.60 | 4, 6, 8 | 80 | 0.0157; 0.184 | 5.14; 56.3 | 306–382 | 113 / 383 / 2128 | 4.9–7.0 |
| F, E, 0.60 | 4, 6 | 14 | 0.0345; 0.0553 | 3.4; 6.15 | 89–111 | 52 / 148 / 495 | 2.8–3.3 |
| F, H, 0.60 | 4, 6 | 24 | 0.0906; 0.313 | 10.3; 45.2 | 124–144 | 88 / 153 / 599 | 1.5–1.8 |
| F, P2, 0.60 | 4, 6 | 24 | 0.0874; 0.754 | 19.9; 116 | 153–170 | 92 / 149 / 246 | 4.4–5.2 |
| S, E, 0.70 | 3, 4, 5, 6 | 35 | 0.00432; 0.0217 | 0.446; 2.23 | 103–104 | 41 / 104 / 154 | 2.6–2.7 |
| S, H, 0.60 | 6 | 20 | 0.2; 1.75 | 11.2; 82.5 | 47–47 | 29 / 49 / 102 | 0.8–0.8 |
| S, H, 0.70 | 4, 5, 6 | 34 | 0.0537; 0.23 | 1.67; 12.3 | 38–53 | 29 / 56 / 169 | 0.8–0.8 |
| S, P2, 0.70 | 4, 6 | 24 | 0.00272; 0.0171 | 0.244; 1.49 | 87–96 | 41 / 99 / 150 | 2.8–3.0 |
| K, E, 0.70 | 3, 4 | 5 | 0.193; 0.53 | 13.2; 31.2 | 59–77 | 42 / 66 / 77 | 0.8–1.2 |
| K, H, 0.60 | 4 | 4 | 1.9; 4.08 | 82.4; 291 | 71–71 | 43 / 89 / 107 | 0.6–0.6 |
| K, H, 0.70 | 3, 4 | 5 | 0.144; 0.251 | 6.51; 14.3 | 39–57 | 39 / 58 / 109 | 0.5–0.7 |
| K, P2, 0.60 | 4 | 4 | 10.2; 13.4 | 231; 448 | 33–33 | 23 / 78 / 168 | 0.8–0.8 |
| K, P2, 0.70 | 4 | 4 | 2.39; 2.97 | 52.8; 102 | 34–34 | 22 / 86 / 142 | 0.8–0.8 |
| LKSE, E, 0.60 | 6 | 20 | 0.151; 0.58 | 20.6; 92.5 | 160–160 | 85 / 196 / 624 | 4.9–4.9 |
| LKSE, H, 0.60 | 4, 5, 6 | 34 | 0.709; 3.41 | 43.6; 306 | 89–141 | 38 / 112 / 372 | 1.3–2.6 |
| LKSE, P2, 0.60 | 6 | 20 | 0.454; 2.2 | 45.4; 223 | 101–101 | 58 / 119 / 326 | 2.9–2.9 |

(Σ columns: the longest chain of the row.  672 triples in all.)
<!--/T:tight-->

`ĉ_ijk ≥ c_ijk` in every triple (asserted).  **Ratio certified/measured, per class of side
chain: apolar (Val, Leu) 200–1 400; aromatic (Phe) 90–170; polar (Ser) 40–100; charged (Lys)
33–77; the heteropolymer 90–160.**  By the brief's own criterion this is a negative result.  The
last column shows where the loss is: the self part of the bound alone is 0.5–30 times the
measured total, the rest is the cross part.

*The loss is cancellation, not slack in the inequalities* [M, `t06_pairtest.py`].  With all
charges set to zero except those of one atom or one pair of atoms, `g` is a single term and
nothing can cancel.  For 108 random single terms (Val₅/E and Ser₄/H) and all subsets of order 3
and 4 — 1 118 cases — the certified bound is never below the exact constant and exceeds it by
a median factor **1.1** (self term, fixed atom), **1.8–2.5** (self term, side-chain atom),
**1.8–2.3** (pair of fixed atoms), **2.7–3.9** (fixed atom and side-chain atom), **3.0–6.3**
(two atoms of one side chain), **4.2–5.5** (atoms of two side chains); the smallest ratios are
1.00–2.0.  Term by term the theorem is nearly sharp; summed over the pairs of a neutral
molecule it is two to three orders of magnitude too large.

### 3.3 Certified remainder constants `Γ_m` [P + rigorous numerics; `gfbound.py`, `x04_gamma.py`, `run_floor.py`]

`Γ_m = Σ_{|T| = m} ĉ_T` in anchored mode, kcal/mol (divide by 0.596 for `k_BT`); anchor from
coordinate descent on `E`.  No value of `g` enters except the `≈ n·k` evaluations of the descent.

<!--T:gamma-->
| side chain, backbone, τ | n | Γ₃ | Γ₄ | Γ₅ | Γ₆ | Γ₃/Γ₄, Γ₄/Γ₅, Γ₅/Γ₆ |
|---|---|---|---|---|---|---|
| V, E, 0.70 | 6 | 13 | 0.432 | 0.00663 | 5.7·10^-5 | 30, 65, 117 |
| V, E, 0.70 | 8 | 20.9 | 0.807 | 0.0171 | 2.9·10^-4 | 26, 47, 59 |
| V, E, 0.70 | 10 | 28.9 | 1.19 | 0.028 | — | 24, 42 |
| V, E, 0.70 | 12 | 36.9 | 1.56 | 0.039 | 8.4·10^-4 | 24, 40, 46 |
| V, E, 0.70 | 16 | 52.8 | 2.32 | 0.0609 | 0.0014 | 23, 38, 44 |
| V, E, 0.70 | 20 | 68.8 | 3.08 | 0.0828 | 0.00195 | 22, 37, 42 |
| V, E, 0.70 | 30 | 109 | 4.97 | 0.138 | 0.00334 | 22, 36, 41 |
| V, E, 0.70 | 40 | 148 | 6.86 | 0.192 | 0.00473 | 22, 36, 41 |
| V, P2, 0.70 | 6 | 11.4 | 0.374 | 0.00613 | — | 30, 61 |
| V, P2, 0.70 | 8 | 18.5 | 0.717 | 0.0163 | — | 26, 44 |
| V, P2, 0.70 | 10 | 25.7 | 1.07 | 0.0271 | — | 24, 39 |
| V, P2, 0.70 | 12 | 33 | 1.42 | 0.0381 | 7.5·10^-4 | 23, 37, 51 |
| V, P2, 0.70 | 20 | 61.9 | 2.82 | 0.0822 | 0.0018 | 22, 34, 46 |
| V, P2, 0.70 | 30 | 98.1 | 4.58 | 0.137 | 0.00311 | 21, 33, 44 |
| L, E, 0.60 | 6 | 57.5 | 3.77 | 0.114 | — | 15, 33 |
| L, E, 0.60 | 8 | 95.4 | 7.29 | 0.313 | 0.0109 | 13, 23, 29 |
| L, E, 0.60 | 12 | 172 | 14.5 | 0.75 | — | 12, 19 |
| L, E, 0.60 | 16 | 248 | 21.8 | 1.19 | 0.0595 | 11, 18, 20 |
| L, E, 0.60 | 24 | 401 | 36.3 | 2.07 | 0.109 | 11, 18, 19 |
| L, E, 0.60 | 32 | 554 | 50.8 | 2.96 | 0.158 | 11, 17, 19 |
| L, H, 0.60 | 6 | 132 | 12.9 | 0.776 | 0.0216 | 10, 17, 36 |
| L, H, 0.60 | 8 | 357 | 49.3 | 4.98 | 0.347 | 7, 10, 14 |
| L, H, 0.60 | 12 | — | 189 | 26.9 | 2.99 | 7, 9 |
| L, H, 0.60 | 16 | 1.82e+03 | 370 | 60.4 | 8.03 | 5, 6, 8 |
| L, H, 0.60 | 24 | 3.47e+03 | 769 | 140 | 21.6 | 5, 5, 7 |
| L, P2, 0.60 | 6 | 33.7 | 1.95 | 0.0564 | — | 17, 35 |
| L, P2, 0.60 | 8 | 56.6 | 3.91 | 0.162 | — | 14, 24 |
| L, P2, 0.60 | 12 | 103 | 7.97 | 0.404 | — | 13, 20 |
| L, P2, 0.60 | 16 | 150 | 12.1 | 0.652 | 0.0296 | 12, 19, 22 |
| L, P2, 0.60 | 24 | 243 | 20.3 | 1.15 | 0.0552 | 12, 18, 21 |
| F, E, 0.60 | 4 | 8.73 | 0.334 | — | — | 26 |
| F, E, 0.60 | 6 | 7.91 | 0.249 | 0.00528 | — | 32, 47 |
| S, E, 0.70 | 3 | 0.286 | — | — | — |  |
| S, E, 0.70 | 4 | 0.729 | 0.00685 | — | — | 106 |
| S, E, 0.70 | 5 | 1.49 | 0.0234 | 1.5·10^-4 | — | 64, 153 |
| S, E, 0.70 | 6 | 2.26 | 0.0418 | — | — | 54 |
| S, H, 0.70 | 4 | 4.13 | 0.0391 | — | — | 106 |
| S, H, 0.70 | 5 | 8.98 | 0.212 | 0.00239 | — | 42, 89 |
| S, H, 0.70 | 6 | — | 0.849 | — | — |  |
| K, H, 0.70 | 3 | 13.6 | — | — | — |  |
| K, H, 0.70 | 4 | 33.6 | 0.854 | — | — | 39 |
| LKSE, H, 0.60 | 4 | 125 | 5.25 | — | — | 24 |
| LKSE, H, 0.60 | 5 | — | 29.1 | 1.53 | — | 19 |
| LKSE, H, 0.60 | 6 | — | 143 | — | — |  |
<!--/T:gamma-->

*Findings.*  (i) `Γ_m` grows linearly with the chain on extended backbones: Val on the strand,
`n = 30 → 40`: 3.99, 0.189, 0.0055, 0.00014 kcal/mol per residue for `m = 3, 4, 5, 6`.
(ii) It falls by a factor 21–51 per order for Val at 12–40 residues on strand and PPII (more
for shorter chains), 11–22 for Leu on strand and PPII, and only 5–8 for Leu on the helix at
16–24 residues, where `Γ₆` is still 8 kcal/mol at 16 residues and 22 kcal/mol at 24.  (iii) The cost is negligible: `Γ₃ … Γ₆` of a 40-residue chain (652 atoms)
take 15, 15, 27 and 49 s; the site penalties `γ_i` take `n + 1` such evaluations.
(iv) Against the exact sums of anchored constants (Val₅/E, enumeration): `Γ₃, Γ₄, Γ₅` are 794,
412 and 244 times too large — the looseness of §3.2 is there at every order, and is paid once.

### 3.4 What the floor buys: `ρ`, the cost number, the brackets [M: exact enumeration of `E` against the certified models]

For each instance: `m₋ ≤ E ≤ m₊` from Theorem 5 with truncation order `m`; then, by enumeration
of all states, `ρ = max(E − m₋)` and the theory division's cost number `Z(m₋)/Z(E) − 1`
(`= 𝔼_{π_E} e^{β(E − m₋)} − 1`); `ρ_cert = max(m₊ − m₋)` and the deterministic bracket need no
enumeration.  Sampled brackets: `N = 20 000`, `δ = 0.05`.

**(a) Constant remainder bound** (`m₋ = model − Γ_m`); a selection of chain lengths — all 88 runs are in `out/report_tables.md`:

<!--T:floor_const_sel-->
| instance | \|X\| | m | ball: evaluations (% of X) | Γ_m (kT) | `ρ = max(E − m₋)` exact; certified (kT) | cost number `Z(m₋)/Z(E) − 1` | deterministic bracket `ln Z(m₋) − ln Z(m₊)` (nats) | Hoeffding; sample-range bracket (nats) |
|---|---|---|---|---|---|---|---|---|
| V6/E τ0.70 | 729 | 3 | 73 (10) | 21.7 | 21.8; 43.5 | 2.8·10^9 | 43.5 | 38.8; 13.1 |
| V6/E τ0.70 | 729 | 4 | 233 (32) | 0.725 | 0.741; 1.47 | 1.07 | 1.45 | 0.0306; 0.00109 |
| V6/E τ0.70 | 729 | 5 | 473 (65) | 0.0111 | 0.0285; 0.0467 | 0.0113 | 0.0224 | 8.9·10^-4; 0.00112 |
| V10/E τ0.70 | 5.9·10^4 | 3 | 201 (0.34) | 48.5 | 48.5; 96.9 | 1.1·10^21 | 96.9 | 92.3; 39.9 |
| V10/E τ0.70 | 5.9·10^4 | 4 | 1161 (2) | 1.99 | 2.02; 4.02 | 6.31 | 3.98 | 0.138; 0.00676 |
| V10/E τ0.70 | 5.9·10^4 | 5 | 4521 (7.7) | 0.047 | 0.0799; 0.142 | 0.0489 | 0.0955 | 0.00267; 0.00549 |
| V12/E τ0.70 | 5.3·10^5 | 4 | 2049 (0.39) | 2.62 | 2.66; 5.3 | 12.8 | 5.25 | 0.265; 0.00799 |
| V6/P2 τ0.70 | 729 | 3 | 73 (10) | 19.1 | 19.1; 38.1 | 1.9·10^8 | 38.1 | 33.5; 10.5 |
| V6/P2 τ0.70 | 729 | 4 | 233 (32) | 0.627 | 0.659; 1.29 | 0.874 | 1.26 | 0.0261; 0.0251 |
| V6/P2 τ0.70 | 729 | 5 | 473 (65) | 0.0103 | 0.0418; 0.0611 | 0.0109 | 0.0215 | 0.00115; 0.0249 |
| V10/P2 τ0.70 | 5.9·10^4 | 3 | 201 (0.34) | 43.2 | 43.2; 86.4 | 5.7·10^18 | 86.4 | 81.7; 34.6 |
| V10/P2 τ0.70 | 5.9·10^4 | 4 | 1161 (2) | 1.79 | 1.84; 3.66 | 4.98 | 3.58 | 0.112; 0.0292 |
| V10/P2 τ0.70 | 5.9·10^4 | 5 | 4521 (7.7) | 0.0455 | 0.104; 0.18 | 0.0487 | 0.0945 | 0.00331; 0.0284 |
| V12/P2 τ0.70 | 5.3·10^5 | 4 | 2049 (0.39) | 2.38 | 2.45; 4.86 | 9.79 | 4.76 | 0.206; 0.0411 |
| L8/E τ0.60 | 256 | 3 | 37 (14) | 160 | 160; 320 | 3.0·10^69 | 320 | 315; 151 |
| L8/E τ0.60 | 256 | 4 | 93 (36) | 12.2 | 12.3; 24.5 | 2.1·10^5 | 24.5 | 19.9; 3.66 |
| L8/E τ0.60 | 256 | 5 | 163 (64) | 0.524 | 0.57; 1.14 | 0.69 | 1.05 | 0.0221; 2.1·10^-4 |
| L12/E τ0.60 | 4.1e+03 | 3 | 79 (1.9) | 288 | 288; 576 | 1.5·10^125 | 576 | 572; 280 |
| L12/E τ0.60 | 4.1e+03 | 4 | 299 (7.3) | 24.4 | 24.4; 48.9 | 3.9·10^10 | 48.8 | 44.2; 15.8 |
| L12/E τ0.60 | 4.1e+03 | 5 | 794 (19) | 1.26 | 1.34; 2.68 | 2.53 | 2.52 | 0.0631; 6.1·10^-4 |
| L16/E τ0.60 | 6.6·10^4 | 4 | 697 (1.1) | 36.5 | 36.6; 73.3 | 7.5·10^15 | 73.1 | 68.6; 28 |
| L16/E τ0.60 | 6.6·10^4 | 5 | 2517 (3.8) | 2 | 2.11; 4.24 | 6.42 | 4.01 | 0.141; 0.00135 |
| L8/H τ0.60 | 256 | 4 | 93 (36) | 82.7 | 83.5; 167 | 8.4·10^35 | 165 | 162; 74.2 |
| L8/H τ0.60 | 256 | 5 | 163 (64) | 8.35 | 9.38; 18.3 | 4.23e+03 | 16.7 | 13.7; 0.833 |
| L8/H τ0.60 | 256 | 6 | 219 (86) | 0.583 | 1.64; 2.86 | 0.799 | 1.17 | 0.0326; 0.268 |
| L12/H τ0.60 | 4.1e+03 | 4 | 299 (7.3) | 316 | 319; 637 | 2.7·10^137 | 633 | 633; 308 |
| L12/H τ0.60 | 4.1e+03 | 5 | 794 (19) | 45.1 | 48.6; 95.9 | 4.0·10^19 | 90.3 | 91.2; 36.8 |
| L12/H τ0.60 | 4.1e+03 | 6 | 1586 (39) | 5.01 | 8.59; 15.9 | 151 | 10 | 11.7; 0.342 |
| L8/P2 τ0.60 | 256 | 3 | 37 (14) | 94.9 | 95; 190 | 1.7·10^41 | 190 | 185; 86.3 |
| L8/P2 τ0.60 | 256 | 4 | 93 (36) | 6.55 | 6.73; 13.4 | 700 | 13.1 | 8.88; 0.168 |
| L8/P2 τ0.60 | 256 | 5 | 163 (64) | 0.272 | 0.457; 0.843 | 0.313 | 0.545 | 0.0144; 0.0485 |
| L12/P2 τ0.60 | 4.1e+03 | 3 | 79 (1.9) | 173 | 173; 345 | 9.2·10^74 | 345 | 341; 164 |
| L12/P2 τ0.60 | 4.1e+03 | 4 | 299 (7.3) | 13.4 | 13.7; 27.2 | 6.4·10^5 | 26.7 | 22.6; 4.82 |
| L12/P2 τ0.60 | 4.1e+03 | 5 | 794 (19) | 0.677 | 1.01; 1.9 | 0.972 | 1.36 | 0.0322; 0.0534 |
| L16/P2 τ0.60 | 6.6·10^4 | 4 | 697 (1.1) | 20.3 | 20.7; 41.3 | 6.3·10^8 | 40.5 | 36.6; 11.7 |
| L16/P2 τ0.60 | 6.6·10^4 | 5 | 2517 (3.8) | 1.09 | 1.59; 2.99 | 2 | 2.2 | 0.0548; 0.0538 |
| F6/E τ0.60 | 384 | 3 | 69 (18) | 13.3 | 13.3; 26.5 | 5.7·10^5 | 26.5 | 21.9; 4.67 |
| F6/E τ0.60 | 384 | 4 | 195 (51) | 0.418 | 0.478; 0.913 | 0.519 | 0.836 | 0.0175; 0.00162 |
| F6/E τ0.60 | 384 | 5 | 330 (86) | 0.00886 | 0.0694; 0.0956 | 0.00894 | 0.0178 | 0.00177; 0.00165 |
| S4/E τ0.70 | 6.56e+03 | 3 | 417 (6.4) | 1.22 | 1.23; 2.45 | 2.4 | 2.45 | 0.0596; 0.00536 |
| S4/E τ0.70 | 6.56e+03 | 4 | 2465 (38) | 0.0115 | 0.0194; 0.0335 | 0.0116 | 0.0231 | 6.4·10^-4; 0.00317 |
| S5/E τ0.70 | 5.9·10^4 | 3 | 681 (1.2) | 2.5 | 2.5; 4.99 | 11.1 | 4.99 | 0.233; 0.00695 |
| S5/E τ0.70 | 5.9·10^4 | 4 | 5801 (9.8) | 0.0393 | 0.0503; 0.0942 | 0.0402 | 0.0788 | 0.0018; 0.00452 |
| S5/E τ0.70 | 5.9·10^4 | 5 | 26281 (45) | 2.6·10^-4 | 0.0113; 0.0162 | 3.9·10^-4 | 7.6·10^-4 | 3.1·10^-4; 0.00451 |
| S6/E τ0.70 | 5.3·10^5 | 4 | 11249 (2.1) | 0.0701 | 0.0835; 0.161 | 0.0728 | 0.141 | 0.00307; 0.00494 |
| S4/H τ0.70 | 2.92e+03 | 3 | 276 (9.5) | 6.93 | 7.01; 13.9 | 1.02e+03 | 13.9 | 9.31; 0.195 |
| S4/H τ0.70 | 2.92e+03 | 4 | 1316 (45) | 0.0656 | 0.163; 0.239 | 0.0691 | 0.138 | 0.00436; 0.0209 |
| S5/H τ0.70 | 1.7·10^4 | 3 | 411 (2.3) | 15.1 | 15.1; 30.1 | 3.5·10^6 | 30.1 | 25.5; 6.48 |
| S5/H τ0.70 | 1.7·10^4 | 4 | 2696 (15) | 0.356 | 0.496; 0.868 | 0.433 | 0.723 | 0.016; 0.0377 |
| S5/H τ0.70 | 1.7·10^4 | 5 | 9496 (54) | 0.004 | 0.145; 0.166 | 0.00726 | 0.0186 | 0.00295; 0.0381 |
| S6/H τ0.70 | 1.0·10^5 | 4 | 4751 (4.5) | 1.42 | 1.6; 3.09 | 3.18 | 2.86 | 0.0767; 0.0624 |
| K3/H τ0.70 | 2.35e+03 | 3 | 493 (21) | 22.9 | 23.1; 45.7 | 8.6·10^9 | 45.7 | 41.1; 14.3 |
| K4/H τ0.70 | 1.6·10^4 | 3 | 721 (4.4) | 56.3 | 56.7; 113 | 2.9·10^24 | 113 | 108; 47.7 |
| K4/H τ0.70 | 1.6·10^4 | 4 | 5310 (32) | 1.43 | 1.75; 3.21 | 3.19 | 2.86 | 0.0772; 0.0137 |
| LKSE:4/H τ0.60 | 7.25e+03 | 3 | 798 (11) | 210 | 210; 420 | 1.4·10^91 | 420 | 415; 201 |
| LKSE:4/H τ0.60 | 7.25e+03 | 4 | 4374 (60) | 8.81 | 9.04; 17.9 | 6.69e+03 | 17.6 | 13.3; 0.819 |
| LKSE:5/H τ0.60 | 1.5·10^4 | 4 | 5172 (36) | 48.9 | 50.4; 99.9 | 4.2·10^21 | 98.8 | 95.3; 41.3 |
| LKSE:5/H τ0.60 | 1.5·10^4 | 5 | 11628 (80) | 2.57 | 4.11; 7.42 | 30.8 | 6.1 | 0.63; 0.981 |
| LKSE:6/H τ0.60 | 2.2·10^5 | 4 | 16912 (7.8) | 240 | 252; 492 | 7.7·10^104 | 482 | 488; 234 |
<!--/T:floor_const_sel-->

**(b) Site penalties** (`m₋ = model − Σ_i γ_i[x_i ≠ x⁰_i]`).  For `m = 3` this is P2's Statement
5(d) — `f + I₂g − Σγ_i[x_i ≠ x⁰_i]` — with constants certified by analysis alone:

<!--T:floor_site-->
| instance | \|X\| | m | ball: evaluations (% of X) | Γ_m (kT) | `ρ = max(E − m₋)` exact; certified (kT) | cost number `Z(m₋)/Z(E) − 1` | deterministic bracket `ln Z(m₋) − ln Z(m₊)` (nats) | Hoeffding; sample-range bracket (nats) |
|---|---|---|---|---|---|---|---|---|
| V4/E τ0.70 | 81 | 3 | 33 (41) | 8.78 | 8.79; 17.6 | 0.476 | 0.431 | 0.0284; 8.79 |
| V4/E τ0.70 | 81 | 4 | 65 (80) | 0.166 | 0.176; 0.342 | 0.00202 | 0.00395 | 0.00486; 0.0836 |
| V6/E τ0.70 | 729 | 3 | 73 (10) | 21.7 | 21.8; 43.5 | 16.4 | 2.92 | 0.348; 21.8 |
| V6/E τ0.70 | 729 | 4 | 233 (32) | 0.725 | 0.741; 1.47 | 0.00815 | 0.0153 | 0.0149; 0.333 |
| V8/E τ0.70 | 6.56e+03 | 3 | 129 (2) | 35.1 | 35.1; 70.2 | 1.13e+03 | 7.11 | 65.6; 35.1 |
| V8/E τ0.70 | 6.56e+03 | 4 | 577 (8.8) | 1.35 | 1.38; 2.74 | 0.015 | 0.0271 | 0.0182; 0.519 |
| V8/E τ0.70 | 6.56e+03 | 5 | 1697 (26) | 0.0287 | 0.0536; 0.0939 | 2.9·10^-4 | 5.8·10^-4 | 0.00115; 0.0149 |
| V10/E τ0.70 | 5.9·10^4 | 3 | 201 (0.34) | 48.5 | 48.5; 96.9 | 9.6·10^4 | 11.6 | 92.3; 42.3 |
| V10/E τ0.70 | 5.9·10^4 | 4 | 1161 (2) | 1.99 | 2.02; 4.02 | 0.022 | 0.039 | 0.0193; 0.711 |
| V4/P2 τ0.70 | 81 | 3 | 33 (41) | 7.51 | 7.53; 15 | 10.5 | 3 | 0.223; 7.53 |
| V4/P2 τ0.70 | 81 | 4 | 65 (80) | 0.131 | 0.147; 0.279 | 0.0201 | 0.0393 | 0.00476; 0.133 |
| V6/P2 τ0.70 | 729 | 3 | 73 (10) | 19.1 | 19.1; 38.1 | 1.5·10^4 | 10.6 | 33.5; 16 |
| V6/P2 τ0.70 | 729 | 4 | 233 (32) | 0.627 | 0.657; 1.29 | 0.118 | 0.213 | 0.0156; 0.635 |
| V6/P2 τ0.70 | 729 | 5 | 473 (65) | 0.0103 | 0.0405; 0.0611 | 0.00225 | 0.00422 | 0.00114; 0.0321 |
| V8/P2 τ0.70 | 6.56e+03 | 3 | 129 (2) | 31.1 | 31.1; 62.2 | 6.1·10^7 | 19.4 | 57.6; 22.7 |
| V8/P2 τ0.70 | 6.56e+03 | 4 | 577 (8.8) | 1.2 | 1.24; 2.47 | 0.256 | 0.425 | 0.0221; 1.01 |
| V8/P2 τ0.70 | 6.56e+03 | 5 | 1697 (26) | 0.0273 | 0.0686; 0.119 | 0.00578 | 0.011 | 0.00216; 0.0487 |
| V10/P2 τ0.70 | 5.9·10^4 | 3 | 201 (0.34) | 43.2 | 43.2; 86.4 | 2.8·10^11 | 28.2 | 81.7; 34.6 |
| V10/P2 τ0.70 | 5.9·10^4 | 4 | 1161 (2) | 1.79 | 1.84; 3.66 | 0.416 | 0.642 | 0.0265; 1.43 |
| V10/P2 τ0.70 | 5.9·10^4 | 5 | 4521 (7.7) | 0.0455 | 0.104; 0.18 | 0.00965 | 0.0185 | 0.00319; 0.0589 |
| V20/P2 τ0.70 | 3.5·10^9 | 4 | 9921 (0.00028) | 4.73 | —; 9.66 | ≈ 1.61 (sampled) | 1.74 | 0.0317; 3.3 |
| V20/P2 τ0.70 | 3.5·10^9 | 5 | 87441 (0.0025) | 0.138 | —; 0.51 | ≈ 0.0318 (sampled) | 0.0605 | 0.00501; 0.128 |
| L8/E τ0.60 | 256 | 3 | 37 (14) | 160 | 160; 320 | 0.102 | 0.097 | 0.0211; 56.6 |
| L8/E τ0.60 | 256 | 4 | 93 (36) | 12.2 | 12.3; 24.5 | 1.7·10^-7 | 3.4·10^-7 | 0.00965; 1.8·10^-4 |
| L8/E τ0.60 | 256 | 5 | 163 (64) | 0.524 | 0.569; 1.14 | 1.7·10^-7 | 3.4·10^-7 | 0.00656; 1.3·10^-4 |
| L12/E τ0.60 | 4.1e+03 | 3 | 79 (1.9) | 288 | 288; 576 | 13.5 | 2.68 | 0.285; 155 |
| L12/E τ0.60 | 4.1e+03 | 4 | 299 (7.3) | 24.4 | 24.4; 48.9 | 1.7·10^-7 | 3.4·10^-7 | 0.00965; 1.8·10^-4 |
| L12/E τ0.60 | 4.1e+03 | 5 | 794 (19) | 1.26 | 1.33; 2.68 | 1.7·10^-7 | 3.4·10^-7 | 0.00899; 1.7·10^-4 |
| L16/E τ0.60 | 6.6·10^4 | 5 | 2517 (3.8) | 2 | 2.11; 4.24 | 1.7·10^-7 | 3.4·10^-7 | 0.00951; 1.8·10^-4 |
| L8/H τ0.60 | 256 | 4 | 93 (36) | 82.7 | 83.5; 167 | 3.9·10^9 | 22.6 | 162; 66.1 |
| L8/H τ0.60 | 256 | 5 | 163 (64) | 8.35 | 9.38; 18.3 | 0.883 | 0.923 | 0.0362; 3.12 |
| L8/P2 τ0.60 | 256 | 3 | 37 (14) | 94.9 | 95; 190 | 1.8·10^28 | 65.3 | 185; 86.4 |
| L8/P2 τ0.60 | 256 | 4 | 93 (36) | 6.55 | 6.73; 13.4 | 0.316 | 0.391 | 0.0253; 4.48 |
| L8/P2 τ0.60 | 256 | 5 | 163 (64) | 0.272 | 0.457; 0.843 | 0.00744 | 0.0146 | 0.011; 0.173 |
| L12/P2 τ0.60 | 4.1e+03 | 3 | 79 (1.9) | 173 | 173; 345 | 1.4·10^55 | 127 | 341; 164 |
| L12/P2 τ0.60 | 4.1e+03 | 4 | 299 (7.3) | 13.4 | 13.7; 27.2 | 0.916 | 0.846 | 0.0366; 7.14 |
| L12/P2 τ0.60 | 4.1e+03 | 5 | 794 (19) | 0.677 | 1.01; 1.9 | 0.0176 | 0.0338 | 0.0166; 0.292 |
| L16/P2 τ0.60 | 6.6·10^4 | 5 | 2517 (3.8) | 1.09 | 1.59; 2.99 | 0.0282 | 0.0536 | 0.0188; 0.427 |
| F4/E τ0.60 | 144 | 3 | 48 (33) | 14.6 | 14.7; 29.3 | 17.9 | 3.57 | 0.366; 11 |
| F4/E τ0.60 | 144 | 4 | 108 (75) | 0.561 | 0.626; 1.27 | 0.0746 | 0.139 | 0.0148; 0.281 |
| S4/E τ0.70 | 6.56e+03 | 3 | 417 (6.4) | 1.22 | 1.23; 2.45 | 0.419 | 0.626 | 0.0249; 1.23 |
| S4/E τ0.70 | 6.56e+03 | 4 | 2465 (38) | 0.0115 | 0.0194; 0.0335 | 0.00304 | 0.00604 | 6.3·10^-4; 0.0146 |
| S5/E τ0.70 | 5.9·10^4 | 3 | 681 (1.2) | 2.5 | 2.5; 4.99 | 1.13 | 1.27 | 0.041; 2.5 |
| S5/E τ0.70 | 5.9·10^4 | 4 | 5801 (9.8) | 0.0393 | 0.0503; 0.0942 | 0.01 | 0.0199 | 0.00174; 0.0432 |
| S5/E τ0.70 | 5.9·10^4 | 5 | 26281 (45) | 2.6·10^-4 | 0.0113; 0.0162 | 1.7·10^-4 | 3.2·10^-4 | 3.1·10^-4; 0.00469 |
| S6/E τ0.70 | 5.3·10^5 | 3 | 1009 (0.19) | 3.79 | 3.8; 7.58 | 2.29 | 1.91 | 0.0636; 3.79 |
| S6/E τ0.70 | 5.3·10^5 | 4 | 11249 (2.1) | 0.0701 | 0.0835; 0.161 | 0.0175 | 0.0345 | 0.00291; 0.0735 |
| S4/H τ0.70 | 2.92e+03 | 3 | 276 (9.5) | 6.93 | 7.01; 13.9 | 188 | 7.55 | 9.66; 6.95 |
| S4/H τ0.70 | 2.92e+03 | 4 | 1316 (45) | 0.0656 | 0.161; 0.239 | 0.0384 | 0.0792 | 0.00423; 0.0881 |
| S5/H τ0.70 | 1.7·10^4 | 3 | 411 (2.3) | 15.1 | 15.1; 30.1 | 2.3·10^5 | 15.8 | 25.5; 9.77 |
| S5/H τ0.70 | 1.7·10^4 | 4 | 2696 (15) | 0.356 | 0.475; 0.868 | 0.22 | 0.394 | 0.0136; 0.38 |
| S5/H τ0.70 | 1.7·10^4 | 5 | 9496 (54) | 0.004 | 0.144; 0.166 | 0.00542 | 0.015 | 0.00295; 0.0413 |
| K3/H τ0.70 | 2.35e+03 | 3 | 493 (21) | 22.9 | 23.1; 45.7 | 2.7·10^8 | 20.6 | 41.1; 14.3 |
| K4/H τ0.70 | 1.6·10^4 | 3 | 721 (4.4) | 56.3 | 56.7; 113 | 4.5·10^21 | 51 | 108; 47.8 |
| K4/H τ0.70 | 1.6·10^4 | 4 | 5310 (32) | 1.43 | 1.75; 3.21 | 0.478 | 0.695 | 0.0273; 1.44 |
| LKSE:4/H τ0.60 | 7.25e+03 | 3 | 798 (11) | 210 | 210; 420 | 2.5·10^89 | 208 | 415; 201 |
| LKSE:4/H τ0.60 | 7.25e+03 | 4 | 4374 (60) | 8.81 | 9.04; 17.9 | 253 | 7.34 | 13.6; 8.82 |
| LKSE:5/H τ0.60 | 1.5·10^4 | 4 | 5172 (36) | 48.9 | 50.4; 99.9 | 1.2·10^15 | 36.6 | 95.3; 41.5 |
<!--/T:floor_site-->

*Reading.*  (i) *Constant bound.*  The cost number is `e^{βΓ_m}` to within a few per cent, as the theory division's formula
says for the centre of a constant box.  `m = 3`: `10³–10¹²⁵` — nothing.  `m = 4`: Val 0.2–13 for 4–12 residues (growing like `e^{0.32 n}`: `10³` near
22 residues), Ser 0.01–0.07 on the strand and 0.07–3.2 on the helix, Phe 0.5–0.75, Lys₄ on the helix 3.2, Leu `3–10¹⁶`, the heteropolymer
`7·10³–10¹⁰⁵`.  `m = 5`: Val ≤ 0.05, Leu on strand and PPII 0.1–6.4 at 6–16 residues, Leu on the helix `3–10¹⁹`.
(ii) *Site penalties* — the floor as a function.  The cost number falls by orders of magnitude because the Gibbs measure rarely leaves the
neighbourhood of the anchor: Val₁₀ on the strand at `m = 4`, 6.3 → 0.022; Val₁₀ on PPII, 5.0 → 0.42; Lys₄ on the helix, 3.2 → 0.48; Leu₁₂ on PPII at
`m = 5`, 0.97 → 0.018.
(iii) *P2's Statement 5(d) with constants certified by analysis alone* (`m = 3`, site penalties, ball of radius 2).  It **works for serine on
the strand**: cost number 0.42, 1.13, 2.29 for 4, 5, 6 residues — at six residues 1 009 evaluations of 531 441, deterministic bracket 1.9 nats,
Hoeffding bracket 0.064 nats with 20 000 samples — and for a frozen ensemble (Leu₈ on the strand, 0.10).  It **fails for valine**: 0.48, 16,
`1.1·10³`, `9.6·10⁴` on the strand and 10.5, `1.5·10⁴`, `6.1·10⁷`, `2.8·10¹¹` on PPII for 4, 6, 8, 10 residues — a factor 8 to 60 per residue, faster
than the domain itself grows (a factor 3) — for Phe₄ on the strand (18), and for everything on the helix and everything charged (`10²–10⁸⁹`).
(iv) *Growth with length* (site penalties; fitted exponent of `1 + cost` per residue; extrapolations are [H]).  `m = 3`: Ser/E 0.42 per residue
(`10⁶` near 36 residues), Val/E 2.2, Val/PPII 4.2.  `m = 4`: Val/E 0.002, Ser/E 0.008, Val/PPII 0.035–0.06 (0.42 at 10 residues, 1.6 at 20 by
sampling; `10⁶` near 230 residues), Leu/PPII about 0.09, Ser/H about 0.16.  `m = 5`: Val/PPII 0.002 (0.032 at 20 residues), Leu/PPII 0.003.
(v) *When is the certificate cheaper than enumeration, and when impossible?*  Count `N_ball` plus the samples for a bracket of 0.1 nats at
`δ = 0.05` (Hoeffding: about `740 (1 + cost)²`).  With `m = 4` and site penalties this is below `k^n` from **4 residues on for Ser (k = 9) and
from 7 on for Val (k = 3)**; from there on the gap widens exponentially (Val₂₀: 9 921 + 50 000 evaluations against `3.5·10⁹`).  "Impossible"
(cost number above `10⁶`): with analysis-only constants from 3 (Lys), 6 (Ser on the helix), 8 (Val on PPII) and 12 (Val on the strand)
residues on, and near 36 for Ser on the strand [H]; with `m = 4` near 230 residues for Val on PPII [H], near 90 for Ser on the helix [H], at 5
for the heteropolymer [M]; with `m = 5` not within any length I can extrapolate to for Val and Leu on extended backbones, while for Leu on
the helix the constant-bound cost number is already `4·10¹⁹` at 12 residues (site penalties: 0.9 at 8 residues; not run at 12).
(vi) *The same models certify the minimum* (`min m₋ ≤ min E ≤ E(x⁰)`).  With site penalties the minimum of `m₋` is attained at the anchor —
an exact certificate of `min E`, up to the floating-point allowance — in 5 of 21 runs at `m = 3` (Ser₄, Ser₅, Ser₆, Val₄ and Leu₈ on the strand:
these are certificates of the minimum by P2's Statement 5(d) with *no enumerated constant*), in 19 of 23 at `m = 4` (all Val and Ser instances
including the helix, Leu on strand and PPII, Lys₄ on the helix, Val₂₀ on PPII) and in 13 of 14 at `m = 5`; the exceptions are Phe₄/E
(0.04 kcal/mol), Leu₈ on the helix (12.8 at `m = 4`, 0.009 at `m = 5`) and the heteropolymer (3.4–21).  In all 160 enumerated runs the anchor
is the true minimiser.

### 3.5 One instance beyond enumeration, end to end [P for the validity; M for the numbers]

**Instance.**  Ace-Val₂₀-NMe (a fixed synthetic homopeptide), backbone polyproline II `(−75°, +145°)`, grid R3, τ = 0.70:
332 atoms, 20 sites, 3 admissible rotamers at every site, `|X| = 3²⁰ = 3 486 784 401`.  (One GB evaluation costs 2–4 ms on the loaded machine:
enumeration would take 80–160 days.)  Chosen before any of its numbers were seen, because Val on PPII is the apolar ensemble with the most
entropy among those P2 enumerated (mean number of sites off the anchor: 3.6–4.3 here).
**What was done, in the order of the brief.**  (i) Certified constants: `Γ₄ = 2.82`, `Γ₅ = 0.0822` kcal/mol, site penalties `γ_i ≤ 0.175` and
`≤ 0.0055` (25–98 s).  (ii) The ball of radius 3 (9 921 states) or 4 (87 441 states; 447 s, cached for the other runs); banded lower and upper
models `m_∓` with band `w`; the pairs beyond the band are **not dropped**: `J_ij + d_ij` is split exactly into its column means plus a
remainder whose row minimum (maximum) goes into `m₋` (`m₊`) — so the far pairs sit in the certified remainder `u = β(m₊ − m₋)`.  Exact
`ln Z(m_∓)` and exact samples by transfer matrix over `w` sites (`3⁹` states for `w = 8`).  (iii) `N = 50 000` samples of `π_{m₋}`, `E` evaluated at
each (22 739–29 321 distinct states; `E ≥ m₋` held at every one).  (iv) Brackets valid at every `N` (§2.7, Proposition 6), `δ = 0.05`.
(v) Gibbs–Bogoliubov side.

<!--T:big-->
| run | band w | m | ball evaluations (fraction of X) | Γ_m kcal/mol; max γ_i | deterministic bracket of `ln Z(E)` | width | N | Hoeffding bracket (δ = 0.05) | width | Bennett bracket (certified b, s²) | width | Gibbs–Bogoliubov lower bound | wall time (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| V20/P2 | 8 | 4 | 9921 (2.8e-06) | 2.82; 0.175 | [517.4843, 519.2199] | 1.74 | 50000 | [518.2442, 518.2759] | 0.0317 | [518.1162, 519.7132] | 1.6 | 518.1035 | 200 |
| V20/P2 | 1 | 5 | 87441 (2.5e-05) | 0.0822; 0.0055 | [517.8792, 518.3699] | 0.491 | 50000 | [518.2575, 518.2670] | 0.00954 | [518.2516, 518.3892] | 0.138 | 518.2541 | 224 |
| V20/P2 | 2 | 5 | 87441 (2.5e-05) | 0.0822; 0.0055 | [518.1350, 518.3458] | 0.211 | 50000 | [518.2584, 518.2662] | 0.00783 | [518.2576, 518.2906] | 0.0329 | 518.2566 | 741 |
| V20/P2 | 8 | 5 | 87441 (2.5e-05) | 0.0822; 0.0055 | [518.2332, 518.2937] | 0.0605 | 50000 | [518.2598, 518.2648] | 0.00501 | [518.2608, 518.2659] | 0.00514 | 518.2591 | 249 |
<!--/T:big-->

*Reading.*  (i) Every bracket is a statement about the same number — the deterministic ones certified outright, each sampled one valid with probability at least 0.95 — and they all intersect: the intersection of the twelve
intervals of the table (and of the four sample-range brackets and Gibbs–Bogoliubov bounds in the logs) is `[518.2608, 518.2648]`.  (ii) At `m = 5` and band 8 the **deterministic** bracket (0.06 nats) needs no random
number; sampling narrows it twelvefold (Hoeffding 0.0050, Bennett with certified floor and variance 0.0051, Gibbs–Bogoliubov lower bound
518.2591).  At `m = 4` the deterministic bracket is 1.7 nats and sampling is what makes the certificate useful (0.032 nats); the Bennett
route does not help there (§3.6).  (iii) Narrowing the band to a next-nearest-neighbour chain (`w = 2`) widens the deterministic bracket
to 0.21 nats and leaves the sampled one at 0.008.  (iv) **The global minimum is certified** by the band-8 models at both orders:
`min m₋ = −306.568720 ≤ min E ≤ E(x⁰) = −306.568715` kcal/mol, i.e. the coordinate-descent anchor is a minimiser of `E` over `3.49·10⁹`
assignments up to the floating-point allowance — P2's third-order certificate with a pairwise kernel, at a size where nothing can be
enumerated, with certified constants.  (v) Cost: `m = 4`: 200 s in all (constants 25 s, ball 23 s, 50 000 evaluations at the samples
149 s); `m = 5`: 741 s the first time (ball 447 s), 224–249 s for each further band.  (vi) *What remains assumed:* the model itself
(ff14SB, GBn2 as OpenMM defines it), the rotamer grid and clash filter, the fixed ideal backbone and rigid geometry; the paper proofs and
the code; the floating-point allowances of §2.6; for the sampled brackets, the independence and exactness of the samples.

### 3.6 Certified inputs of the Bennett bracket; the window; do the remainder statistics extrapolate? [P + M]

(Proposition 6; the coordinator's two additions.)  `r = β(E − m)`; all numbers in `k_BT` and
nats; site-penalty models; "enum." = exact, by enumeration of the instance; the last column
is from `N` samples of `π_{m₋}`; band = window of the pairwise model (pairs beyond it are in `u`).
A selection — the full table (both models for every site-penalty run) is in `out/report_tables.md`.

<!--T:bennett_sel-->
| instance | m | band | model | `b_cert` | `b` enum. | `s²_cert` | `Var r` enum. | `W(b_cert, s²_cert)` (nats) | `W` with enum. `b, s²` | true gap `K` | sampled: mean r; var r; min r (N) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| V6/E τ0.70 | 3 | 5 | m₋ | 18.7 | 9.36 | 429 | 19.6 | 18.1 | 7.66 | 6.5 | — |
| V6/E τ0.70 | 3 | 5 | m₀ | 22 | 0.00685 | 0.931 | 3.8·10^-12 | 15.7 | 1.9·10^-12 | 1.9·10^-12 | — |
| V8/E τ0.70 | 5 | 7 | m₋ | 5.8·10^-4 | 2.9·10^-4 | 5.0·10^-6 | 1.2·10^-6 | 2.5·10^-6 | 5.8·10^-7 | 5.8·10^-7 | 2.9·10^-4; 1.1·10^-6; 1.7·10^-7 (20000) |
| V8/E τ0.70 | 5 | 7 | m₀ | 0.0473 | 0.00843 | 1.2·10^-6 | 1.1·10^-9 | 6.3·10^-7 | 5.7·10^-10 | 5.7·10^-10 | — |
| V10/E τ0.70 | 4 | 9 | m₋ | 0.0486 | 0.0243 | 0.0247 | 0.00559 | 0.0106 | 0.00261 | 0.00258 | — |
| V10/E τ0.70 | 4 | 9 | m₀ | 2.03 | 0.0111 | 0.00473 | 1.5·10^-9 | 0.00525 | 7.3·10^-10 | 7.3·10^-10 | — |
| V6/P2 τ0.70 | 5 | 1 | m₋ | 0.0887 | 0.0077 | 0.00804 | 1.5·10^-4 | 0.00401 | 7.2·10^-5 | 7.2·10^-5 | 0.0158; 1.5·10^-4; 0.00804 (20000) |
| V6/P2 τ0.70 | 5 | 1 | m₀ | 0.149 | 0.0527 | 0.00201 | 1.0·10^-4 | 0.00105 | 5.1·10^-5 | 5.0·10^-5 | — |
| V6/P2 τ0.70 | 5 | 2 | m₋ | 0.0295 | 0.00565 | 0.0011 | 2.7·10^-5 | 5.5·10^-4 | 1.4·10^-5 | 1.4·10^-5 | 0.011; 2.7·10^-5; 0.00534 (20000) |
| V6/P2 τ0.70 | 5 | 2 | m₀ | 0.0785 | 0.0333 | 2.7·10^-4 | 5.3·10^-5 | 1.4·10^-4 | 2.7·10^-5 | 2.7·10^-5 | — |
| V6/P2 τ0.70 | 5 | 5 | m₋ | 0.00423 | 0.00225 | 4.2·10^-5 | 7.4·10^-6 | 2.1·10^-5 | 3.7·10^-6 | 3.7·10^-6 | 0.00223; 7.2·10^-6; 1.7·10^-7 (20000) |
| V6/P2 τ0.70 | 5 | 5 | m₀ | 0.0327 | 0.011 | 1.0·10^-5 | 4.8·10^-7 | 5.3·10^-6 | 2.4·10^-7 | 2.4·10^-7 | — |
| V8/P2 τ0.70 | 5 | 1 | m₋ | 0.145 | 0.0142 | 0.0215 | 3.1·10^-4 | 0.0107 | 1.5·10^-4 | 1.5·10^-4 | 0.0283; 3.0·10^-4; 0.0141 (20000) |
| V8/P2 τ0.70 | 5 | 1 | m₀ | 0.246 | 0.0859 | 0.00536 | 1.6·10^-4 | 0.00289 | 8.2·10^-5 | 7.9·10^-5 | — |
| V8/P2 τ0.70 | 5 | 2 | m₋ | 0.0543 | 0.0091 | 0.00353 | 7.1·10^-5 | 0.00176 | 3.5·10^-5 | 3.5·10^-5 | 0.0207; 6.9·10^-5; 0.0116 (20000) |
| V8/P2 τ0.70 | 5 | 2 | m₀ | 0.143 | 0.0529 | 8.7·10^-4 | 7.6·10^-5 | 4.6·10^-4 | 3.8·10^-5 | 3.8·10^-5 | — |
| V8/P2 τ0.70 | 5 | 7 | m₋ | 0.0111 | 0.00578 | 2.3·10^-4 | 3.0·10^-5 | 1.1·10^-4 | 1.5·10^-5 | 1.5·10^-5 | 0.00574; 3.0·10^-5; 1.7·10^-7 (20000) |
| V8/P2 τ0.70 | 5 | 7 | m₀ | 0.0649 | 0.0144 | 5.6·10^-5 | 7.9·10^-7 | 2.9·10^-5 | 4.0·10^-7 | 4.0·10^-7 | — |
| V10/P2 τ0.70 | 4 | 9 | m₋ | 0.753 | 0.377 | 0.808 | 0.0607 | 0.328 | 0.0323 | 0.0291 | 0.376; 0.0594; 1.7·10^-7 (20000) |
| V10/P2 τ0.70 | 4 | 9 | m₀ | 2.15 | 0.0186 | 0.155 | 1.3·10^-6 | 0.165 | 6.8·10^-7 | 6.7·10^-7 | — |
| V10/P2 τ0.70 | 5 | 1 | m₋ | 0.202 | 0.0214 | 0.0417 | 4.9·10^-4 | 0.0207 | 2.5·10^-4 | 2.4·10^-4 | 0.0411; 4.8·10^-4; 0.0198 (20000) |
| V10/P2 τ0.70 | 5 | 1 | m₀ | 0.345 | 0.119 | 0.0104 | 2.2·10^-4 | 0.00577 | 1.1·10^-4 | 1.1·10^-4 | — |
| V10/P2 τ0.70 | 5 | 2 | m₋ | 0.0798 | 0.0133 | 0.00739 | 1.3·10^-4 | 0.00368 | 6.4·10^-5 | 6.4·10^-5 | 0.0307; 1.2·10^-4; 0.0175 (20000) |
| V10/P2 τ0.70 | 5 | 2 | m₀ | 0.209 | 0.0749 | 0.00183 | 9.8·10^-5 | 9.8·10^-4 | 5.0·10^-5 | 4.9·10^-5 | — |
| V10/P2 τ0.70 | 5 | 9 | m₋ | 0.0186 | 0.00964 | 5.7·10^-4 | 6.4·10^-5 | 2.8·10^-4 | 3.2·10^-5 | 3.2·10^-5 | 0.00956; 6.2·10^-5; 1.7·10^-7 (20000) |
| V10/P2 τ0.70 | 5 | 9 | m₀ | 0.099 | 0.019 | 1.4·10^-4 | 1.1·10^-6 | 7.3·10^-5 | 5.6·10^-7 | 5.5·10^-7 | — |
| V12/P2 τ0.70 | 5 | 2 | m₋ | 0.106 | 0.0176 | 0.0127 | 1.9·10^-4 | 0.00629 | 9.7·10^-5 | 9.6·10^-5 | 0.041; 1.9·10^-4; 0.0234 (20000) |
| V12/P2 τ0.70 | 5 | 2 | m₀ | 0.276 | 0.0968 | 0.00312 | 1.2·10^-4 | 0.00171 | 6.2·10^-5 | 6.0·10^-5 | — |
| V20/P2 τ0.70 | 4 | 8 | m₋ | 2.11 | — | 5.27 | — | 1.51 | — | — | — |
| V20/P2 τ0.70 | 4 | 8 | m₀ | 5.69 | — | 0.922 | — | 2.2 | — | — | — |
| V20/P2 τ0.70 | 5 | 1 | m₋ | 0.492 | — | 0.245 | — | 0.118 | — | — | 0.108; 0.00151; 0.0484 (50000) |
| V20/P2 τ0.70 | 5 | 1 | m₀ | 0.856 | — | 0.061 | — | 0.0397 | — | — | — |
| V20/P2 τ0.70 | 5 | 2 | m₋ | 0.213 | — | 0.0488 | — | 0.0241 | — | — | 0.0838; 4.9·10^-4; 0.0475 (50000) |
| V20/P2 τ0.70 | 5 | 2 | m₀ | 0.555 | — | 0.012 | — | 0.00721 | — | — | — |
| V20/P2 τ0.70 | 5 | 8 | m₋ | 0.061 | — | 0.00478 | — | 0.00237 | — | — | 0.0315; 2.9·10^-4; 8.6·10^-6 (50000) |
| V20/P2 τ0.70 | 5 | 8 | m₀ | 0.285 | — | 0.00118 | — | 6.5·10^-4 | — | — | — |
| L16/E τ0.60 | 5 | 15 | m₋ | 3.4·10^-7 | 5.7·10^-14 | 1.5·10^-13 | 8.5·10^-15 | 7.3·10^-14 | 4.1·10^-15 | 3.5·10^-13 | 1.7·10^-7; 0; 1.7·10^-7 (20000) |
| L16/E τ0.60 | 5 | 15 | m₀ | 2.12 | 0.0179 | 3.5·10^-14 | 1.8·10^-32 | 4.1·10^-14 | 8.9·10^-33 | 5.0·10^-13 | — |
| L8/H τ0.60 | 5 | 7 | m₋ | 1.73 | 0.872 | 5.13 | 0.547 | 1.28 | 0.271 | 0.24 | 0.87; 0.533; 1.7·10^-7 (20000) |
| L8/H τ0.60 | 5 | 7 | m₀ | 9.6 | 0.169 | 0.522 | 4.3·10^-5 | 4.43 | 2.3·10^-5 | 2.1·10^-5 | — |
| L16/P2 τ0.60 | 5 | 15 | m₋ | 0.0579 | 0.0289 | 0.0124 | 0.00225 | 0.0059 | 0.00111 | 0.00109 | 0.0288; 0.00229; 1.7·10^-7 (20000) |
| L16/P2 τ0.60 | 5 | 15 | m₀ | 1.52 | 0.0887 | 0.0028 | 1.6·10^-6 | 0.00249 | 8.2·10^-7 | 8.0·10^-7 | — |
| F4/E τ0.60 | 4 | 3 | m₋ | 0.149 | 0.0746 | 0.043 | 0.0052 | 0.0204 | 0.0026 | 0.00259 | 0.0741; 0.00522; 1.7·10^-7 (20000) |
| F4/E τ0.60 | 4 | 3 | m₀ | 0.704 | 0.0446 | 0.00998 | 4.6·10^-11 | 0.00635 | 2.3·10^-11 | 2.3·10^-11 | — |
| S5/E τ0.70 | 5 | 4 | m₋ | 3.2·10^-4 | 1.7·10^-4 | 5.5·10^-7 | 1.4·10^-7 | 2.7·10^-7 | 6.8·10^-8 | 6.8·10^-8 | 1.7·10^-4; 1.4·10^-7; 1.7·10^-7 (20000) |
| S5/E τ0.70 | 5 | 4 | m₀ | 0.00828 | 0.00489 | 1.4·10^-7 | 2.9·10^-8 | 6.9·10^-8 | 1.5·10^-8 | 1.5·10^-8 | — |
| S6/E τ0.70 | 3 | 5 | m₋ | 2.96 | 1.48 | 11.3 | 0.621 | 2.39 | 0.394 | 0.29 | 1.49; 0.62; 1.7·10^-7 (20000) |
| S6/E τ0.70 | 3 | 5 | m₀ | 4.72 | 0.00658 | 1.33 | 8.3·10^-9 | 1.95 | 4.1·10^-9 | 4.1·10^-9 | — |
| S6/E τ0.70 | 4 | 5 | m₋ | 0.0349 | 0.0174 | 0.00188 | 1.7·10^-4 | 9.4·10^-4 | 8.4·10^-5 | 8.4·10^-5 | 0.0174; 1.7·10^-4; 1.7·10^-7 (20000) |
| S6/E τ0.70 | 4 | 5 | m₀ | 0.0978 | 0.00623 | 4.6·10^-4 | 3.5·10^-8 | 2.4·10^-4 | 1.8·10^-8 | 1.8·10^-8 | — |
| S5/H τ0.70 | 4 | 4 | m₋ | 0.409 | 0.202 | 0.196 | 0.00708 | 0.093 | 0.00374 | 0.00354 | 0.202; 0.00703; 1.7·10^-7 (20000) |
| S5/H τ0.70 | 4 | 4 | m₀ | 0.631 | 0.046 | 0.0462 | 1.9·10^-5 | 0.0278 | 9.4·10^-6 | 9.3·10^-6 | — |
| S5/H τ0.70 | 5 | 4 | m₋ | 0.0151 | 0.00542 | 4.2·10^-4 | 2.8·10^-5 | 2.1·10^-4 | 1.4·10^-5 | 1.4·10^-5 | 0.00538; 2.8·10^-5; 1.7·10^-7 (20000) |
| S5/H τ0.70 | 5 | 4 | m₀ | 0.0903 | 0.0459 | 1.0·10^-4 | 1.8·10^-5 | 5.4·10^-5 | 9.3·10^-6 | 9.2·10^-6 | — |
| K4/H τ0.70 | 4 | 3 | m₋ | 0.876 | 0.438 | 1.16 | 0.098 | 0.439 | 0.0518 | 0.0471 | 0.439; 0.0973; 1.7·10^-7 (20000) |
| K4/H τ0.70 | 4 | 3 | m₀ | 1.95 | 0.121 | 0.206 | 3.9·10^-7 | 0.194 | 2.0·10^-7 | 1.9·10^-7 | — |
| LKSE:4/H τ0.60 | 4 | 3 | m₋ | 14.6 | 7.31 | 224 | 2.58 | 14 | 4.24 | 1.77 | 7.31; 2.57; 1.7·10^-7 (20000) |
| LKSE:4/H τ0.60 | 4 | 3 | m₀ | 12.4 | 0.117 | 16.2 | 3.3·10^-7 | 10.1 | 1.7·10^-7 | 1.6·10^-7 | — |
<!--/T:bennett_sel-->

*Reading.*  (i) *The request is met in full, without sampling and without enumeration:* a certified one-sided floor (`r ≥ 0` for
`m₋`; `r₀ ≥ −βρ_cert/2` for the midpoint model), a certified bound of the mean and of the variance (exact moments of the explicit function
`u`), and `W(b_cert, s²_cert)`.  (ii) *How far are the certified inputs from the enumerated ones?*  For the model `m₋` at `m ≥ 4`: `b_cert/b = 2.0`
throughout (because `𝔼u ≈ 2𝔼r`), `s²_cert/Var r = 4–15`, and with all pairs in the band **`W_cert` is 4–26 times the true gap `K`** (median about 9) (e.g. Val₁₀/PPII, `m = 5`:
`2.8·10⁻⁴` against `3.2·10⁻⁵` nats; Ser₅/E, `m = 5`: `2.7·10⁻⁷` against `6.8·10⁻⁸`).  For the midpoint model the true gap is `10⁻⁹–10⁻⁵` and
the certified `W` is `10⁻⁷–10⁻³`: looser relative to the truth (the certificate cannot see that `r₀` is almost constant) but small in
absolute terms.  (iii) *At 20 residues* (no enumeration possible): `m = 5`, band 8: **`b_cert = 0.061 k_BT`, `s²_cert = 4.8·10⁻³`,
`W = 2.4·10⁻³` nats** for `m₋` (midpoint model: `0.29`, `1.2·10⁻³`, `6.5·10⁻⁴`); the Bennett bracket with a Chebyshev mean on the certified variance is
`[518.2608, 518.2659]`, as narrow as Hoeffding's with the same samples, and it would be 0.011 nats wide with 5 000 samples and 0.03 with 500.  With `m = 4`
the certified `b` and `s²` are 2.1 and 5.3 and the route is useless (W = 1.5 nats) although Hoeffding's bracket is 0.03 nats — the certified
variance pays for the looseness of `γ_i` quadratically.  With analysis-only constants (`m = 3`) it is useless everywhere except Ser on the
strand (Ser₆: `W_cert = 2.4` nats, true gap 0.29).
(iv) *The window.*  With band 2 (a next-nearest-neighbour chain; the pairs beyond the window are in `u`) the certified inputs at 20 residues
are `b = 0.21`, `s² = 0.049`, `W = 0.024` nats (midpoint: `W = 0.0072`); with band 1: 0.49, 0.25, 0.12 (0.040).  The enumerated statistics of my
midpoint model agree with the coordinator's ANOVA chain on the same peptides — Val₈/PPII: band 1 `b = 0.086`, `σ = 0.013` (ANOVA chain
`w = 1`: 0.127, 0.011); band 2: 0.053, 0.0087 (0.058, 0.0071); all pairs: 0.014, 0.0009 (0.012, 0.0018) — so a banded anchored model is, like
the ANOVA chain, essentially the whole ensemble, and it comes with a certificate.
(v) *Do the remainder statistics extrapolate?*  Yes, linearly in the chain length, for `r = β(E − m₋)` under `π_{m₋}` (Val on PPII, `m = 5`):

<!--T:extrap-->
| band | quantity (kT) | n = 6 (enum.) | 8 (enum.) | 10 (enum.) | 12 (enum.) | linear extrapolation of the last two to n = 20 | n = 20 (50 000 samples) | certified at n = 20: `b_cert`; `s²_cert` |
|---|---|---|---|---|---|---|---|---|
| 1 | mean of r | 0.0157 | 0.0283 | 0.0412 | — | 0.106 | 0.108 | 0.492; 0.245 |
| 1 | variance of r | 1.5·10^-4 | 3.1·10^-4 | 4.9·10^-4 | — | 0.00141 | 0.00151 |  |
| 1 | smallest r | 0.00804 | 0.0141 | 0.0198 | — | 0.0484 | 0.0484 |  |
| 2 | mean of r | 0.011 | 0.0207 | 0.0308 | 0.041 | 0.0819 | 0.0838 | 0.213; 0.0488 |
| 2 | variance of r | 2.7·10^-5 | 7.1·10^-5 | 1.3·10^-4 | 1.9·10^-4 | 4.5·10^-4 | 4.9·10^-4 |  |
| 2 | smallest r | 0.00534 | 0.0116 | 0.0175 | 0.0234 | 0.0468 | 0.0475 |  |
| all pairs (8 at n = 20) | mean of r | 0.00225 | 0.00578 | 0.00964 | — | 0.0289 | 0.0315 | 0.061; 0.00478 |
| all pairs (8 at n = 20) | variance of r | 7.4·10^-6 | 3.0·10^-5 | 6.4·10^-5 | — | 2.3·10^-4 | 2.9·10^-4 |  |
| all pairs (8 at n = 20) | smallest r | 1.7·10^-7 | 1.7·10^-7 | 1.7·10^-7 | — | 1.7·10^-7 | 8.6·10^-6 |  |
<!--/T:extrap-->

The linear extrapolation from the two longest enumerated chains predicts the sampled mean and the sampled minimum at 20 residues within
2–9 % and the variance within 7–26 % (the variance is slightly super-linear).  (vi) The full table (both models, every site-penalty run) is in
`out/report_tables.md`; in all 132 enumerated runs `b ≤ b_cert`, `Var r ≤ s²_cert`, `0 ≤ K ≤ W(b, Var r) ≤ W_cert` (asserted).

### 3.7 Optional (a): `Σ_i c_i²` of the certified remainder

For the remainder `R = g − I_{m−1}g`, the argument of Proposition 1 with site `i` placed last in
the ordering gives `R(x) − R(x′) = R_i(x) − R_i(x′)` when `x, x′` differ at site `i` only, with
`|R_i| ≤ Σ_{T∋i, |T|=m} ĉ_T = m γ_i`; hence the **certified one-site oscillations**
`c_i(R) ≤ 2 m γ_i` [P; `c_i^{exact} ≤ c_i^{cert}` checked in every enumerated run of the table].

<!--T:osc-->
| instance | m | max certified `c_i = 2mγ_i` (kT) | `Σ_i c_i²` certified (kT²) | max exact `c_i` (kT) | `Σ_i c_i²` exact (kT²) |
|---|---|---|---|---|---|
| V4/E τ0.70 | 3 | 16.1 | 729 | 0.00859 | 2.0·10^-4 |
| V4/E τ0.70 | 4 | 0.331 | 0.439 | 6.8·10^-4 | 1.1·10^-6 |
| V6/E τ0.70 | 3 | 30.9 | 3.18e+03 | 0.00959 | 3.9·10^-4 |
| V6/E τ0.70 | 4 | 1.33 | 6.18 | 0.00136 | 5.7·10^-6 |
| V8/E τ0.70 | 3 | 37.1 | 6.28e+03 | 0.00987 | 5.9·10^-4 |
| V8/E τ0.70 | 4 | 2.08 | 17.1 | 0.00181 | 1.3·10^-5 |
| V8/E τ0.70 | 5 | 0.0514 | 0.0116 | 5.1·10^-5 | 1.2·10^-8 |
| V10/E τ0.70 | 3 | 39.5 | 9.49e+03 | 0.00994 | 7.9·10^-4 |
| V10/E τ0.70 | 4 | 2.39 | 29.7 | 0.00184 | 2.0·10^-5 |
| V4/P2 τ0.70 | 3 | 13.7 | 525 | 0.0167 | 8.0·10^-4 |
| V4/P2 τ0.70 | 4 | 0.261 | 0.272 | 8.4·10^-4 | 1.9·10^-6 |
| V6/P2 τ0.70 | 3 | 27.1 | 2.44e+03 | 0.0214 | 0.00229 |
| V6/P2 τ0.70 | 4 | 1.13 | 4.56 | 0.00234 | 1.7·10^-5 |
| V6/P2 τ0.70 | 5 | 0.0196 | 0.00181 | 1.9·10^-5 | 1.8·10^-9 |
| V8/P2 τ0.70 | 3 | 33.5 | 4.95e+03 | 0.0243 | 0.00358 |
| V8/P2 τ0.70 | 4 | 1.83 | 13.4 | 0.00331 | 4.1·10^-5 |
| V8/P2 τ0.70 | 5 | 0.0485 | 0.0105 | 3.2·10^-5 | 5.2·10^-9 |
| V10/P2 τ0.70 | 3 | 35.4 | 7.56e+03 | 0.0253 | 0.00487 |
| V10/P2 τ0.70 | 4 | 2.16 | 23.9 | 0.00355 | 6.7·10^-5 |
| V10/P2 τ0.70 | 5 | 0.0719 | 0.0245 | 4.2·10^-5 | 1.0·10^-8 |
| V20/P2 τ0.70 | 4 | 2.35 | 79.3 | — | — |
| V20/P2 τ0.70 | 5 | 0.0922 | 0.109 | — | — |
| L8/E τ0.60 | 3 | 170 | 1.3·10^5 | 0.0121 | 7.3·10^-4 |
| L8/E τ0.60 | 4 | 18.5 | 1.38e+03 | 0.0147 | 8.2·10^-4 |
| L8/E τ0.60 | 5 | 0.922 | 3.85 | 2.3·10^-4 | 2.3·10^-7 |
| L12/E τ0.60 | 3 | 190 | 2.8·10^5 | 0.0121 | 0.00117 |
| L12/E τ0.60 | 4 | 23.5 | 3.68e+03 | 0.0154 | 0.00177 |
| L12/E τ0.60 | 5 | 1.65 | 15.8 | 2.7·10^-4 | 5.1·10^-7 |
| L16/E τ0.60 | 5 | 1.82 | 29.4 | 2.7·10^-4 | 7.9·10^-7 |
| L8/H τ0.60 | 4 | 101 | 5.6·10^4 | 0.112 | 0.0564 |
| L8/H τ0.60 | 5 | 12.3 | 885 | 0.00812 | 2.6·10^-4 |
| L8/P2 τ0.60 | 3 | 103 | 4.6·10^4 | 0.0487 | 0.0131 |
| L8/P2 τ0.60 | 4 | 9.78 | 393 | 0.00376 | 5.4·10^-5 |
| L8/P2 τ0.60 | 5 | 0.471 | 1.02 | 6.5·10^-4 | 1.6·10^-6 |
| L12/P2 τ0.60 | 3 | 115 | 1.0·10^5 | 0.0492 | 0.0229 |
| L12/P2 τ0.60 | 4 | 13 | 1.1e+03 | 0.00394 | 1.2·10^-4 |
| L12/P2 τ0.60 | 5 | 0.882 | 4.54 | 9.1·10^-4 | 4.9·10^-6 |
| L16/P2 τ0.60 | 5 | 1.01 | 8.8 | 9.2·10^-4 | 8.3·10^-6 |
| F4/E τ0.60 | 3 | 24.5 | 1.94e+03 | 0.119 | 0.0365 |
| F4/E τ0.60 | 4 | 1.12 | 5.03 | 0.00492 | 9.2·10^-5 |
| S4/E τ0.70 | 3 | 2.23 | 14.1 | 0.00669 | 1.4·10^-4 |
| S4/E τ0.70 | 4 | 0.023 | 0.00211 | 3.1·10^-4 | 2.0·10^-7 |
| S5/E τ0.70 | 3 | 4.49 | 47.8 | 0.00729 | 2.1·10^-4 |
| S5/E τ0.70 | 4 | 0.0775 | 0.0201 | 3.2·10^-4 | 4.1·10^-7 |
| S5/E τ0.70 | 5 | 5.1·10^-4 | 1.3·10^-6 | 1.2·10^-6 | 5.3·10^-12 |
| S6/E τ0.70 | 3 | 5.05 | 92.6 | 0.00753 | 2.8·10^-4 |
| S6/E τ0.70 | 4 | 0.122 | 0.0562 | 4.6·10^-4 | 6.4·10^-7 |
| S4/H τ0.70 | 3 | 13.2 | 474 | 0.0878 | 0.0208 |
| S4/H τ0.70 | 4 | 0.131 | 0.0689 | 3.1·10^-4 | 2.9·10^-7 |
| S5/H τ0.70 | 3 | 24.2 | 1.76e+03 | 0.091 | 0.0273 |
| S5/H τ0.70 | 4 | 0.654 | 1.65 | 0.00198 | 1.2·10^-5 |
| S5/H τ0.70 | 5 | 0.00801 | 3.2·10^-4 | 5.7·10^-5 | 1.4·10^-8 |
| K3/H τ0.70 | 3 | 45.7 | 6.28e+03 | 0.236 | 0.167 |
| K4/H τ0.70 | 3 | 105 | 3.0·10^4 | 0.309 | 0.267 |
| K4/H τ0.70 | 4 | 2.86 | 32.8 | 0.00568 | 1.1·10^-4 |
| LKSE:4/H τ0.60 | 3 | 386 | 4.4·10^5 | 0.342 | 0.212 |
| LKSE:4/H τ0.60 | 4 | 17.6 | 1.24e+03 | 0.0189 | 8.3·10^-4 |
| LKSE:5/H τ0.60 | 4 | 84.2 | 3.1·10^4 | 0.0938 | 0.0325 |
<!--/T:osc-->

*Reading.*  `Σ_i c_i²` of the *certified* oscillations is `10⁻⁶–0.06 (k_BT)²` for Ser on the strand at `m = 4, 5`, 0.002–0.025 for
Val₆–Val₁₀ at `m = 5` and **0.109 at 20 residues** (so `D₂ ≤ Σc_i²/2 ≤ 0.055` for a product reference: `e^{D₂} ≤ 1.06`), 1–29 for Leu at `m = 5`;
at `m = 4` it is 4–30 for Val₆–Val₁₀, 79 for Val₂₀, 33 for Lys₄, 400–4 000 for Leu; at `m = 3` `10¹–10⁵`.  The *exact* oscillations of the
remainder are 200–2 000 times smaller than the certified ones (their squares sum to `10⁻¹²–0.3`).  Comparison of the two routes on the same
certified data: at `m = 5` both are cheap (floor: cost number 0.03 at 20 residues; moment: `e^{D₂} ≤ 1.06`); at `m = 4` the floor with site
penalties still works (cost number 1.6 at 20 residues) while the moment bound from worst-case oscillations does not (`D₂ ≤ 40`): the floor
is weighted by how often the measure actually leaves the anchor, the oscillation bound is not.

### 3.8 Optional (b): OBC2 [M, small sample]

My evaluator handles OBC2 (`GBSAOBC2Force`: no neck term, `tanh(ψ − 0.8ψ² + 4.85ψ³)`, offset
0.009 nm) with the same code; against OpenMM's Reference platform on fresh states the deviation
is `3·10⁻¹²` kcal/mol (Val₄/E, 12 states).  Same pipeline, same domains:

<!--T:obc2-->
| instance | \|X\| | m | ball: evaluations (% of X) | Γ_m (kT) | `ρ = max(E − m₋)` exact; certified (kT) | cost number `Z(m₋)/Z(E) − 1` | deterministic bracket `ln Z(m₋) − ln Z(m₊)` (nats) | Hoeffding; sample-range bracket (nats) |
|---|---|---|---|---|---|---|---|---|
| V6/E τ0.70 | 729 | 3 | 73 (10) | 7.53 | 7.53; 15.1 | 1.86e+03 | 15.1 | 10.5; 0.295 |
| V6/E τ0.70 | 729 | 4 | 233 (32) | 0.14 | 0.144; 0.286 | 0.151 | 0.281 | 0.00549; 2.9·10^-4 |
| V6/E τ0.70 | 729 | 5 | 473 (65) | 0.00133 | 0.00487; 0.00801 | 0.00141 | 0.00282 | 1.5·10^-4; 2.5·10^-4 |
| L8/E τ0.60 | 256 | 4 | 93 (36) | 3.47 | 3.58; 7.05 | 31.2 | 6.95 | 0.64; 0.00592 |
| L8/E τ0.60 | 256 | 5 | 163 (64) | 0.112 | 0.22; 0.336 | 0.118 | 0.224 | 0.00613; 5.9·10^-5 |
| S4/E τ0.70 | 6.56e+03 | 3 | 417 (6.4) | 1.27 | 1.28; 2.53 | 2.55 | 2.53 | 0.0628; 0.0107 |
| S4/E τ0.70 | 6.56e+03 | 4 | 2465 (38) | 0.00811 | 0.024; 0.0344 | 0.0082 | 0.0163 | 6.6·10^-4; 0.00614 |

| instance | \|X\| | m | ball: evaluations (% of X) | Γ_m (kT) | `ρ = max(E − m₋)` exact; certified (kT) | cost number `Z(m₋)/Z(E) − 1` | deterministic bracket `ln Z(m₋) − ln Z(m₊)` (nats) | Hoeffding; sample-range bracket (nats) |
|---|---|---|---|---|---|---|---|---|
| V8/P2 τ0.70 | 6.56e+03 | 4 | 577 (8.8) | 0.231 | 0.237; 0.472 | 0.0317 | 0.0615 | 0.00746; 0.171 |
| V8/P2 τ0.70 | 6.56e+03 | 5 | 1697 (26) | 0.00294 | 0.00927; 0.0163 | 5.1·10^-4 | 0.001 | 3.1·10^-4; 0.00551 |
<!--/T:obc2-->

*Reading.*  (i) The whole pipeline runs unchanged for OBC2 and passes the same checks (9 runs, sandwich never violated).
(ii) OBC2's certified constants are **2–8 times smaller than GBn2's for apolar side chains** (Val₆/E: `Γ₃, Γ₄, Γ₅ = 4.49, 0.084, 0.00079` against
12.96, 0.432, 0.0066 kcal/mol; Leu₈/E: 40.8, 2.07, 0.067 against 95.4, 7.29, 0.313) and about equal for serine (Ser₄/E: 0.755, 0.0048 against
0.729, 0.0068).  (iii) *The neck correction is what makes GBn2's constants large* [N, an ablation that is not a model anyone uses:
`x05_neck.py`, GBn2 with `m0 := 0`]: without the neck term `Γ₃, Γ₄, Γ₅` fall by factors 10, 26, 74 for Val₆/E (1.24, 0.017, `9·10⁻⁵`), by 12, 27,
69 for Leu₈/E and by 6 and 12 for Ser₄/E; the largest change of `ln B` under a single rotamer flip at the anchor — the small parameter of
§2.8 — is 0.27 with the neck, 0.06 without, 0.15 for OBC2 (Val₆/E).  The neck integral is a sharply peaked function of the distance (width
about 1 Å), so a rotamer flip switches whole neck contributions on and off.  So yes: the size of every constant in this report depends on
the neck correction, by about an order of magnitude per order of the expansion; the *structure* of the analysis does not.

### 3.9 Controls

1. Evaluator: OpenMM Reference (double), table-free evaluation, P2's evaluator, 40-digit
   arithmetic (§2.0).  2. Domains: `pruned_domain` = P2's `shape_pruned` in 26 of 26 cases.
3. P2's constants reproduced by my enumeration (§3.1).  4. Proposition 1 to `2·10⁻¹³` (§2.1).
5. Enclosures against sampled maxima (ratio `≥ 1`, `≤ 1.0001`).  6. Generating function against
explicit sums over subsets, `2·10⁻¹⁶`.  7. Bound against exact constants: class mode 672
triples, anchored mode all subsets of orders 3–5 of Val₅/E, single terms 1 118 cases — no
violation.  8. Sandwich `m₋ ≤ E ≤ m₊` at every state of every enumerated instance; transfer
matrix against enumeration; transfer-matrix moments against direct sums; Bennett inequalities
(see Totals).  9. Several certificates of the same number: for Val₂₀/PPII the brackets of orders 4 and 5 and of bands 1, 2, 8 all intersect (§3.5).
*Not a control:* nothing here was checked by a second person or by a proof assistant.

---

## 4. Prior art, with a search log

I extended P2's search (its §4: Simonson/Archontis/Gaillard on pairwise GB, Marshall–Mayo on
pairwise PB, LUTE, exact solvers, provable partition functions — all of which I take from P2's
report and did **not** re-read) only where the new statements need it.  Reading level of every
item below: **[abstract]** (the record returned by the literature tool); nothing was read in full.

| # | tool, query | hits | read |
|---|---|---|---|
| 1 | PubMed: `generalized Born many-body error bound pairwise` | 0 | — |
| 2 | PubMed: `Born radii rigorous bounds` | 1 (PMID 18821791) | not opened |
| 3 | PubMed: `interval arithmetic protein energy bounds rotamer` | 0 | — |
| 4 | Consensus: "rigorous upper and lower bounds on generalized Born effective radii or many-body error of pairwise decomposition of generalized Born solvation energy" | 3 shown | 3 abstracts |
| 5 | Consensus: "provable bounds partition function protein design non-pairwise energy function sparse tuple expansion residual guarantee" | 3 shown | 3 abstracts |
| 6 | Consensus: "anchored decomposition cut-HDMR truncation error bound mixed differences" | 3 shown | 3 abstracts |

**What these say [K, abstract].**
* On the accuracy of GB as a model: Onufriev, Case & Bashford, *J. Comput. Chem.* (2002),
  "Effective Born radii in the generalized Born approximation: the importance of being
  perfect" (with exact radii the standard `f_GB` reproduces Poisson-equation pair terms well);
  Mongan et al., *J. Chem. Phys.* (2007), "Analysis of integral expressions for effective Born
  radii"; Onufriev et al., *J. Chem. Phys.* (2011), "A strategy for reducing gross errors in the
  generalized Born models of implicit solvation" (errors above `2 k_BT` in individual pair terms
  relative to the Poisson equation even with perfect radii).  These concern the distance of GB
  from the Poisson equation — a *physical* error that no statement of this report touches.
* On sparse or banded pairwise models and guarantees: Jain et al., *PLoS Comput. Biol.* (2017),
  "A critical analysis of computational protein design with sparse residue interaction graphs"
  (distance and energy cutoffs change the optimum; comparison on 136 problems); Jou et al.,
  *J. Comput. Biol.* (2016), "BWM*" (dynamic programming over a branch decomposition of a sparse
  residue interaction graph); Hallen et al., *Commun. ACM* (2019), "Protein design by provable
  algorithms" (review).  These guarantees are relative to a *given* pairwise energy; the step
  from a many-body energy to a pairwise one is where they apply a fit or a cutoff.
* On truncated anchored decompositions: Rahman, *Math. Comp.* (2014), "Approximation errors in
  truncated dimensional decompositions" (expected-error bounds for referential = anchored
  decompositions, and their comparison with ANOVA decompositions).

**From memory, unverified** (no source opened in this workstream): the multivariate Faà di Bruno
formula (proved inline for the case used); Hoeffding's and Bennett's inequalities (textbook
forms); the GBn2 model of Nguyen, Roe and Simmerling and the OBC model of Onufriev, Bashford
and Case (what I used is OpenMM's source, read in full for the two classes concerned).

**How this report relates to it.**  I did not find, in these 9 abstracts and in the literature
quoted by P2, (a) a rigorous sup-norm bound on the part of a generalized-Born energy that lies
beyond a pairwise function of rotamers, (b) interval enclosures of the derivatives of the GB
rescaling and kernel used for such a bound, or (c) a certified two-sided bracket of a partition
function whose energy contains a GB term.  **This is not a claim of novelty**: six queries, read
at abstract level, in a literature (protein design) that is outside the programme's scope and
that I did not survey.  The mathematical ingredients are standard: anchored (cut-HDMR)
expansions, the Faà di Bruno formula, elementary symmetric and Bell polynomials, interval
automatic differentiation, transfer matrices, Hoeffding and Bennett.  What may be worth a
proper search by the division is the combination "exact low orders by evaluation + term-by-term
tail in closed form over all subsets" as a *certificate*, and the remainder identity of
Proposition 1 with anchored constants.

---

## 5. What I did not settle

1. **Compact geometries.**  On the helix the certified constants decay by 4–8 per order and
   the recipe fails (N2).  A buried side chain has even more neighbours.  Nothing here says
   that a certificate exists there at polynomial cost.
2. **Whether the looseness is intrinsic.**  I have no theorem saying that every bound that
   treats atom pairs separately must lose the factor measured in §3.2; I have a mechanism and
   a sharpness test (§3.2).
3. **A better analytic tail.**  Signed sums over rigid neutral groups at reference radii
   (first-order response exact, second order term by term) should gain one power of the small
   parameter (§6).  Not attempted.
4. **Certified class constants `c_ijk` (all pairs of states, all contexts) within a small
   factor of P2's.**  I certify sums of *anchored* constants through the expansion; per-triple
   class constants I certify only by analysis alone (§3.2, loose).
5. **A proof of the floating-point allowance for evaluated values of `g`** (§2.6): it is an
   allowance with a measured margin of five orders of magnitude.
6. **Continuous χ, finer grids, relaxed geometry, non-product domains.**  Everything is on P2's
   pruned product of a three-state grid.
7. **Polar and charged chains beyond 6 residues** (Ser to 6, Lys to 4, heteropolymer to 6).
8. **Optimal models.**  The minorants of the evaluated terms of order 3 and 4 are row minima,
   not optimal pairwise minorants; the anchor is a local minimum from coordinate descent, with
   no optimisation of the anchor or use of several anchors; the allocation of `ĉ_T` to sites is
   uniform (`1/m` each).
9. **Machine checking.**

---

## 6. The three most promising next steps

1. **Group-wise signed tails.**  Replace the term-by-term bound at the truncation order by one
   in which, for each atom `p` and each rigid group `Q` (a backbone peptide unit; a side chain
   in a given rotamer), the kernel sums `Σ_{q∈Q} q_q ∂_w^k h(ℓ̄_p + ℓ̄_q; r_pq)` are evaluated
   *with signs* at reference Born radii and only the deviations from the reference are bounded
   term by term.  The sharpness test of §3.2 says the single-term inequalities are within 1.1–6
   of exact, so the whole factor 250–800 is available in principle; each exact order in the
   deviation gains one power of the small parameter.  This is what decides the helix and the
   buried case.
2. **A checkable certificate.**  The certificate of Theorem 5 is a finite object: tables,
   `γ_i`, ball values, two banded models.  A stand-alone checker in exact or interval arithmetic
   (inputs as rationals; the enclosures recomputed; the sandwich verified term by term) would
   remove "correctness of my code" from the assumptions, and Proposition 1 with Lemma 2 is a
   small formalisation target next to the existing `higherOrder_remainder`.
3. **The same pipeline on an ensemble that is not rigid**: continuous χ within rotamer wells
   (the tables become interval-valued; the neck cutoff must be handled by splitting cells at
   the jump), or a public folded backbone with a rotamer library.  The exposed-peptide numbers
   here are the easy end.

---

## 7. Requests

### To the theory division

**P3-T1 (state the remainder as an identity, with anchored constants).**  Proposition 1:
`g − I_{m−1}g = Σ_{T ⊆ S(x), |T| = m} Δ_T g(z^{T,x}; x_T)` with `z^{T,x}` = `x` before `min T`, the
anchor elsewhere.  It strengthens `higherOrder_remainder` in two ways that matter numerically:
only pairs `(x⁰_i, x_i)` occur (anchored constants; a factor up to `2^m` in the `δ`'s), and only
contexts that differ from the anchor before `min T`.  Together with the allocation lemma at
order `m` (`γ_i = (1/m) Σ_{T∋i} c_T` gives `Σ_{T ⊆ S} c_T ≤ Σ_{i∈S} γ_i` — your P2-T1 at general
order) it is the whole combinatorial content of Theorem 5.

**P3-T2 (the cost formula for a floor that is a function).**  Your §11.30 preview states the cost
at the centre of a *constant* box as `Θ((e^{ρ₋} − 1)/ε)`.  On real numbers the difference
between a constant floor and a site-wise one is the whole story: Val₆ on the strand at `m = 4`
has cost number 1.07 with the constant `Γ₄` and 0.008 with site penalties; Val₁₀ on PPII 4.98
against 0.42 (§3.4).  Please state (e) for a floor `lo(x)` — the instance cost is
`𝔼_{π_g} e^{g − lo} − 1` in every case — and say whether the lower bound survives for the
structured class that a certificate of this kind actually defines:
`{g : |g − Σ_{|U|<m} d_U| ≤ Σ_{T ⊆ S(x), |T| = m} ĉ_T}` with the `d_U` *known* on the ball.

**P3-T3 (a sandwich gives Bennett's inputs for free).**  Proposition 6: from `m₋ ≤ E ≤ m₊` with
`u = β(m₊ − m₋)` tractable, `b ≤ 𝔼_{π_{m₋}}u` and `Var ≤ 𝔼_{π_{m₋}}u²`, both exactly computable.
Two questions: (i) which of the three brackets — `[ln Z(m₊), ln Z(m₋)]` (deterministic),
Hoeffding with range `1 − e^{−βρ}`, Bennett with `(𝔼u, 𝔼u²)` plus a Chebyshev mean — is optimal
for which regime of `(𝔼u, 𝔼u², max u, N)`; in my runs each of them wins somewhere (§3.5–3.6);
(ii) is there a version of the Bennett bracket that uses the pointwise bound `0 ≤ r ≤ u(x)`
directly (an extremal problem with a state-dependent ceiling) rather than only two moments of `u`?

**P3-T4 (query complexity with a ball).**  The certificate uses `N_ball = Σ_{j<m} C(n,j)(k−1)^j`
deterministic evaluations and then `N` random ones.  Is `N_ball` necessary for the class of
functions whose order-`m` anchored constants are bounded by given `ĉ_T`?  (For `m = 2` this is
your star; for `m = 3` P2's ball.)

### To the engineering division

**P3-E1 (specification: a certificate checker for Theorem 5).**
*Motivation.*  Remove "the workstream's code is right" from the assumptions of §2.10.
*Inputs.*  For one instance: the coordinates per (site, state) and fixed atoms; the GB
parameters and neck tables; the anchor; the ball values of `g`; `γ_i`; the two banded models
(`out/floor_*.json` holds the summary; `run_floor.py` can dump the rest).
*Formulation.*  (1) Recompute the descreening tables in interval arithmetic; (2) recompute the
enclosure tables of `encl.py` or verify them cell by cell; (3) recompute `γ_i` by Proposition 4
with outward rounding; (4) re-evaluate `g` on the ball in interval arithmetic; (5) verify
`red⁻_U ≤ d_U ≤ red⁺_U` entry-wise and the additive splits of the far pairs; (6) recompute
`ln Z(m_∓)` with rational or interval transfer matrices.
*Validation.*  Val₆/E, `m = 4`, site penalties: `γ = (0.0431, 0.0739, 0.0989, 0.0992, 0.0743,
0.0430)` kcal/mol, ball of 233 states, `ln Z(m₋) = 198.0761`, `ln Z(m₊) = 198.0609`, exact
`ln Z(E) = 198.068008`.
*Stopping condition.*  The checker accepts the instance of §3.5.
*Resources.*  Interval evaluation of `g` costs about 10 s per state with `mpmath` at 332 atoms;
87 441 states need a compiled interval library — hence the request.

**P3-E2 (a faster evaluator with a proven rounding bound).**  The ball of radius 4 for 50
residues is `3.7·10⁶` evaluations of an 800-atom energy.  A compiled evaluator with pairwise or
compensated summation would make `m = 5` routine at 50–100 residues and turn the allowance
`ε_g` into a theorem.

---

## What I did not check

* **No proof was machine-checked.**  Propositions 1, 4, 6, Lemma 2, Theorems 3, 5 are paper
  proofs, checked numerically as stated at each of them.
* **The floating-point allowance for evaluated values of `g`** (`10⁻⁷` kcal/mol each) is not
  proved for the summation order of the evaluator used; measured errors are `≤ 2·10⁻¹²`.  The
  transfer-matrix arithmetic is not budgeted formally.  The enclosures rely on `mpmath.iv`.
* **My code was not reviewed by anyone.**  Its checks are those of §3.9; in the largest instance
  (§3.5) the sandwich cannot be checked by enumeration — there the evidence is the agreement of
  certificates of different order and band, and the 200 000 sampled states of the four runs (22 739–29 321 distinct per run) at each of
  which `E ≥ m₋` held.
* **P2's tables of `f` and its geometry builder** were used as they are (P2 validated them
  against OpenMM; I re-validated only `g`, the domains, and — through the totals — nothing of
  `f` separately).
* **The independence of the sampler.**  The brackets with a `δ` assume i.i.d. exact samples;
  numpy's generator and double-precision conditional tables were used and not tested beyond
  the 160 enumerated runs in which the truth fell inside every bracket.
* **Only one large instance**, one anchor, one seed; **only three backbones**, ideal and rigid;
  **only exposed peptides**; charged systems only up to 4–6 residues.
* **Prior art** at abstract level only; one PubMed hit not opened.
* **Physical meaning.**  Nothing here bears on whether GBn2 describes water.
